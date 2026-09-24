"""Image selection for Clinical Minimal decks: filter → score → preview as placed → judge → choose.

    python imgpick.py fetch  img/brief.json [slot]        download, filter, score; one sheet per slot
    python imgpick.py judge  img/brief.json <slot> "3=3,2,2 5=2,1,2 1=0"
    python imgpick.py choose img/brief.json               pick winners → img/<slot>.jpg|png + sources.json

brief.json (paths relative to it):
{"slots": {"title": {
    "subject": "lithium carbonate tablets or capsules",   # what must be VISIBLE, concretely
    "must": ["lithium"], "any": ["tablet", "capsule", "pill"], "avoid": ["battery", "mining"],
    "kind": "photo" | "diagram",                          # photo = cropped to fill, diagram = shown whole
    "box": [7.33, 7.5],                                   # placed size in inches
    "queries": ["lithium carbonate tablets", "lithium pills close up"],
    "candidates": [[url, w, h, title, page, domain], ...] # from the Google Images snippet in SKILL.md
}}}

Judge each candidate on its sheet tile (it shows the picture exactly as it will sit in the box):
  subject 0–3: 3 shows this slide's specific subject · 2 clearly related, recognisable without the title
               · 1 only the general field (generic pills, lab, brain) · 0 unrelated or misleading
  clean   0–2: 2 clean · 1 minor text/logo at an edge · 0 watermark, brand/packaging as the subject, ad copy,
               or paragraphs of text that cannot be read at the placed size
  crop    0–2: 2 subject whole and fills the box · 1 tight, or some empty margin · 0 subject cut off, or small
               in a big empty field (fill under ~25% on the sheet)
  "n=0" rejects candidate n. Winners need subject ≥ 2, clean ≥ 1, crop ≥ 1. If none passes: new, more
  specific queries, or switch the slot's kind (a good diagram cropped as a photo fails on crop), then
  fetch that slot again.
"""
from __future__ import annotations

import io
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

BLOCK = re.compile(r"shutterstock|istock|alamy|dreamstime|123rf|depositphotos|gettyimages|adobe|ftcdn|"
                   r"sciencephoto|vectorstock|freepik|pinterest|pinimg|facebook|fbsbx|instagram|tiktok|"
                   r"ytimg|youtube|x\.com|twimg|lookaside|stock", re.I)
TRUSTED = re.compile(r"\.gov(\.|$)|\.edu(\.|$)|\.ac\.|nhs\.uk|who\.int|wikimedia|wikipedia|ncbi|nih\.|"
                     r"medlineplus|nice\.org|nature\.com|bmj\.|thelancet|nejm|psychiatry\.org|rcpsych|nami\.org|"
                     r"mayoclinic|clevelandclinic|hopkinsmedicine|msdmanuals|merckmanuals|radiopaedia|"
                     r"britannica|cancer\.gov|heart\.org|achaheart", re.I)
HEALTH = re.compile(r"health|medic|clinic|hospital|pharm|psych|doctor|nurse|anatomy|verywell|webmd|"
                    r"medscape|drugs\.com|\.org$", re.I)
SHOP = re.compile(r"/shop|/products?/|/cart|amazon|ebay|walmart|etsy|aliexpress|/p/|buy|store|price", re.I)
WEIGHTS = {"rel": 0.30, "trust": 0.20, "res": 0.15, "crop": 0.15, "quality": 0.20}
PPI_GOOD = 150


def _tokens(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower())


def text_relevance(slot, meta) -> float:
    hay = _tokens(" ".join(meta))
    has = lambda t: re.search(rf"\b{re.escape(_tokens(t).strip())}", hay) is not None
    must = slot.get("must", [])
    must_share = sum(map(has, must)) / len(must) if must else 1.0
    any_hits = sum(map(has, slot.get("any", [])))
    return 0.5 * must_share + 0.5 * min(1.0, any_hits / 2)


def trust(domain: str, page: str) -> float:
    if TRUSTED.search(domain):
        return 1.0
    if SHOP.search(page) or SHOP.search(domain):
        return 0.15
    return 0.6 if HEALTH.search(domain) else 0.4


def kept_share(iw, ih, bw, bh) -> float:
    """Photo: share of the picture left after cropping to the box. Diagram: share of the box it fills."""
    a, b = iw / ih, bw / bh
    return min(a / b, b / a)


def effective_ppi(iw, ih, bw, bh, kind) -> float:
    """Pixels per inch once placed: photos are scaled to cover the box, diagrams to fit inside it."""
    return min(iw / bw, ih / bh) if kind == "photo" else max(iw / bw, ih / bh)


def quality(img) -> tuple[float, dict]:
    """Sharpness, contrast and 'white cutout' look (product shots on white read badly as a panel)."""
    import numpy as np
    from PIL import ImageFilter
    g = img.convert("L")
    g.thumbnail((512, 512))
    a = np.asarray(g, dtype=float)
    lap = np.asarray(g.filter(ImageFilter.FIND_EDGES), dtype=float).var()  # ~300 soft … 3000+ crisp
    border = np.concatenate([a[:6].ravel(), a[-6:].ravel(), a[:, :6].ravel(), a[:, -6:].ravel()])
    white_border = float((border > 245).mean())
    sharp = min(1.0, lap / 1500)
    contrast = min(1.0, a.std() / 50)
    score = 0.6 * sharp + 0.4 * contrast
    return score, {"sharp": round(sharp, 2), "contrast": round(contrast, 2), "white_border": round(white_border, 2)}


def subject_fill(tile) -> float:
    """Share of the placed tile that is not flat background (the border colour). A small product on a
    big white field, or a thin diagram letterboxed in a tall box, scores low and looks empty on the slide."""
    import numpy as np
    a = np.asarray(tile.convert("RGB"), dtype=int)
    border = np.concatenate([a[:4].reshape(-1, 3), a[-4:].reshape(-1, 3), a[:, :4].reshape(-1, 3),
                             a[:, -4:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    return float((np.abs(a - bg).sum(axis=2) > 40).mean())


def dhash(img) -> int:
    import numpy as np
    px = np.asarray(img.convert("L").resize((9, 8)), dtype=int).ravel()
    return sum(1 << i for i in range(64) if px[(i // 8) * 9 + i % 8] > px[(i // 8) * 9 + i % 8 + 1])


def placed(img, box, kind, height=300):
    """The picture as it will look in its box: cropped to fill (photo) or letterboxed on white (diagram)."""
    from PIL import Image
    bw, bh = box
    w = int(height * bw / bh)
    img = img.convert("RGB")
    iw, ih = img.size
    if kind == "photo":
        if iw / ih > bw / bh:
            nw = int(ih * bw / bh); img = img.crop(((iw - nw) // 2, 0, (iw + nw) // 2, ih))
        else:
            nh = int(iw * bh / bw); img = img.crop((0, (ih - nh) // 2, iw, (ih + nh) // 2))
        return img.resize((w, height))
    tile = Image.new("RGB", (w, height), "white")
    img.thumbnail((w, height))
    tile.paste(img, ((w - img.width) // 2, (height - img.height) // 2))
    return tile


# ---------------------------------------------------------------- fetch
def fetch(brief_path: Path, only: str | None = None):
    from PIL import Image, ImageDraw, ImageFont
    sys.path.insert(0, str(Path(__file__).parent))
    import cm
    brief = json.loads(brief_path.read_text("utf-8"))
    root = brief_path.parent
    font = ImageFont.truetype("C:/Windows/Fonts/LeelawUI.ttf", 15)
    for name, slot in brief["slots"].items():
        if only and name != only:
            continue
        slot.pop("judge", None)  # candidate numbers change on a new fetch
        cand_dir = root / "_cand" / name
        shutil.rmtree(cand_dir, ignore_errors=True)
        cand_dir.mkdir(parents=True, exist_ok=True)
        kind, box = slot.get("kind", "photo"), slot["box"]
        rows, seen_urls = [], set()
        for c in slot.get("candidates", []):
            url, w, h, title, page, domain = (c + [""] * 6)[:6]
            page = page.replace("\\u003d", "=").replace("\\u0026", "&")
            domain = domain or urlparse(page or url).netloc
            if url in seen_urls:
                continue
            seen_urls.add(url)
            r = {"url": url, "title": title, "page": page, "domain": domain}
            avoid = [t for t in slot.get("avoid", []) if _tokens(t).strip() in _tokens(f"{title} {url} {page}")]
            if BLOCK.search(url) or BLOCK.search(domain):
                r["rejected"] = "stock/social site"
            elif avoid:
                r["rejected"] = f"avoid term: {avoid[0]}"
            elif w and h and effective_ppi(w, h, *box, kind) < 90:
                r["rejected"] = f"too small ({w}×{h} for a {box[0]}×{box[1]} in box)"
            else:
                r["rel"] = round(text_relevance(slot, [title, url, page]), 2)
            rows.append(r)
        live = sorted((r for r in rows if "rejected" not in r), key=lambda r: -r["rel"])
        for r in live[12:]:
            r["rejected"] = "text relevance below the top 12"
        live = live[:12]
        hashes = []
        for i, r in enumerate(live, 1):
            try:
                data = cm.download_image(r["url"], cand_dir / "tmp").read_bytes()
                img = Image.open(io.BytesIO(data)); img.load()
            except Exception as e:  # dead link, HTML instead of an image, 403
                r["rejected"] = f"download failed: {type(e).__name__}"; continue
            iw, ih = img.size
            dh = dhash(img)
            if any(bin(dh ^ other).count("1") <= 6 for other in hashes):
                r["rejected"] = "duplicate of a better-ranked candidate"; continue
            hashes.append(dh)
            ext = "png" if img.mode in ("RGBA", "LA", "P") or kind == "diagram" else "jpg"
            f = cand_dir / f"{i:02d}.{ext}"
            (img.convert("RGBA") if ext == "png" else img.convert("RGB")).save(f, quality=92)
            q, qd = quality(img)
            fill = subject_fill(placed(img, box, kind, 200))
            q *= min(1.0, fill / 0.35)  # mostly empty once placed
            ppi = effective_ppi(iw, ih, *box, kind)
            r.update(file=f.name, px=[iw, ih], ppi=round(ppi), quality=round(q, 2), q=qd, fill=round(fill, 2),
                     trust=trust(r["domain"], r["page"]), res=round(min(1.0, ppi / PPI_GOOD), 2),
                     crop=round(max(0.0, min(1.0, (kept_share(iw, ih, *box) - 0.4) / 0.5)), 2))
            if ppi < 90:
                r["rejected"] = f"too small after download ({iw}×{ih})"; continue
            r["auto"] = round(sum(WEIGHTS[k] * r[k] for k in WEIGHTS), 3)
        (cand_dir / "tmp").unlink(missing_ok=True)
        slot["scored"] = rows
        ranked = sorted((r for r in rows if "auto" in r and "rejected" not in r), key=lambda r: -r["auto"])[:8]
        slot["shortlist"] = [r["file"] for r in ranked]
        _sheet(cand_dir, ranked, box, kind, font, name, slot["subject"])
        rej = sum("rejected" in r for r in rows)
        print(f"{name}: {len(rows)} candidates, {rej} rejected, shortlist {len(ranked)} → {cand_dir / 'sheet.png'}")
    brief_path.write_text(json.dumps(brief, indent=1, ensure_ascii=False), "utf-8")


def _sheet(cand_dir, ranked, box, kind, font, name, subject):
    from PIL import Image, ImageDraw
    tiles = [placed(Image.open(cand_dir / r["file"]), box, kind) for r in ranked]
    if not tiles:
        return
    tw, th, cols, pad = tiles[0].width, tiles[0].height, 4, 14
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + pad) + pad, 40 + rows * (th + 64 + pad)), "white")
    dr = ImageDraw.Draw(sheet)
    dr.text((pad, 10), f"{name}: {subject}  ({kind}, {box[0]}×{box[1]} in, shown as placed)", fill=(27, 35, 43),
            font=font)
    for i, (r, t) in enumerate(zip(ranked, tiles)):
        x, y = pad + (i % cols) * (tw + pad), 40 + (i // cols) * (th + 64 + pad)
        sheet.paste(t, (x, y))
        dr.rectangle([x, y, x + tw - 1, y + th - 1], outline=(200, 205, 210))
        n = int(r["file"][:2])
        dr.text((x, y + th + 4), f"#{n}  auto {r['auto']:.2f}  fill {r['fill']:.0%}  {r['ppi']} ppi",
                fill=(27, 35, 43), font=font)
        dr.text((x, y + th + 24), r["domain"][:40], fill=(74, 85, 97), font=font)
        dr.text((x, y + th + 42), (r["title"] or "")[:44], fill=(99, 110, 122), font=font)
    sheet.save(cand_dir / "sheet.png")


# ---------------------------------------------------------------- judge / choose
def judge(brief_path: Path, slot_name: str, spec: str):
    brief = json.loads(brief_path.read_text("utf-8"))
    slot = brief["slots"][slot_name]
    marks = slot.setdefault("judge", {})
    for item in spec.split():
        n, _, v = item.partition("=")
        vals = [int(x) for x in v.split(",")]
        marks[str(int(n))] = (vals + [0, 0, 0])[:3]
    brief_path.write_text(json.dumps(brief, indent=1, ensure_ascii=False), "utf-8")
    print(f"{slot_name}: judged {len(marks)} candidates")


def choose(brief_path: Path) -> int:
    from PIL import Image
    brief = json.loads(brief_path.read_text("utf-8"))
    root = brief_path.parent
    src_path = root / "sources.json"
    sources = json.loads(src_path.read_text("utf-8")) if src_path.exists() else {}
    missing = []
    for name, slot in brief["slots"].items():
        by_n = {int(r["file"][:2]): r for r in slot.get("scored", []) if r.get("file") and "auto" in r}
        best = None
        for n, (subj, clean, crop) in ((int(k), v) for k, v in slot.get("judge", {}).items()):
            r = by_n.get(n)
            if not r or subj < 2 or clean < 1 or crop < 1 or "rejected" in r:
                continue
            final = 0.35 * r["auto"] + 0.65 * (0.6 * subj / 3 + 0.2 * clean / 2 + 0.2 * crop / 2)
            if not best or final > best[0]:
                best = (final, n, r, (subj, clean, crop))
        if not best:
            missing.append(name); continue
        final, n, r, marks = best
        src = root / "_cand" / name / r["file"]
        dst = root / f"{name}{src.suffix}"
        shutil.copyfile(src, dst)
        site = r["domain"].removeprefix("www.")
        sources[name] = {"file": dst.name, "url": r["url"], "page": r["page"], "site": site,
                         "title": r["title"], "credit": f"Image: {site}", "subject": slot["subject"],
                         "auto": r["auto"], "judge": dict(zip(("subject", "clean", "crop"), marks)),
                         "final": round(final, 3), "px": r["px"], "kind": slot.get("kind", "photo")}
        print(f"{name}: #{n} {site}  final {final:.2f}  → {dst.name}")
    src_path.write_text(json.dumps(sources, indent=1, ensure_ascii=False), "utf-8")
    if missing:
        print("No candidate passed for: " + ", ".join(missing) +
              ". Search again with new queries (more specific subject, 'diagram'/'illustration'/'photo'), "
              "or give the slide a diagram instead of a picture.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # Windows console is cp1252
    a = sys.argv[1:]
    if len(a) in (2, 3) and a[0] == "fetch":
        fetch(Path(a[1]), a[2] if len(a) == 3 else None)
    elif len(a) == 4 and a[0] == "judge":
        judge(Path(a[1]), a[2], a[3])
    elif len(a) == 2 and a[0] == "choose":
        sys.exit(choose(Path(a[1])))
    else:
        print(__doc__); sys.exit(2)
