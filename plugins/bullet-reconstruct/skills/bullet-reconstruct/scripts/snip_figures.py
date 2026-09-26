#!/usr/bin/env python3
"""snip_figures.py — crop every captioned figure and table out of a PDF as PNG snips.

Why a crop and not only `pdfimages`: many PDFs draw their tables (and often their
charts) as vector rules, boxes and text. They contain zero embedded images, so an
image extractor finds nothing. This script renders the page and crops the region.

How it works, per page:
  1. Find caption labels: a word Figure / Fig. / Table / Box / Scheme / Chart / Exhibit
     followed by a number, that starts a line segment in its column (bold labels rank
     first). Column-aware: two-column pages are not merged into one line.
  2. Grow the caption block into the graphics beside it (rules, boxes, curves, raster
     images) in the same column, step by step while the next object is within --gap pt.
  3. Render that region at --dpi, trim the white margin, save <kind>-<number>.png.
  4. Also save large raster images that have no caption. Skip icons and logos (smaller
     than --min-pt, or the same size on 2+ pages).
A caption with no graphic next to it (a text-only table) is listed as skipped: fold its
content into the bullets instead.

Usage:
  python3 snip_figures.py source.pdf --out snips [--dpi 300] [--gap 24] [--pages 2-5]

Writes <out>/*.png and <out>/manifest.json, prints one line per snip. Exit 0 when the
run completed (even with zero snips), 2 on a usage or input error.
Needs pdfplumber (it renders through its bundled pypdfium2) and Pillow.
"""
import argparse
import json
import os
import re
import sys

try:
    import pdfplumber
    from PIL import Image, ImageChops
except ImportError as exc:  # pragma: no cover
    sys.exit(f"missing dependency: {exc.name} (python3 -m pip install pdfplumber pillow)")

LABELS = {"figure": "figure", "fig": "figure", "fig.": "figure", "table": "table",
          "box": "box", "scheme": "scheme", "chart": "chart", "exhibit": "exhibit"}
LABEL_RE = re.compile(r"^(figure|fig\.?|table|box|scheme|chart|exhibit)\.?$", re.I)
JOINED_RE = re.compile(r"^(fig\.?|figure|table)(\d+[a-z]?)[.:|]?$", re.I)
NUM_RE = re.compile(r"^([A-Z]?\d+[A-Za-z]?)[.:|,]?$")
LINE_TOL = 2.5      # pt: words within this vertical distance share a line
COL_GUTTER = 10.0   # pt: a word further left than this belongs to another column
CONT_GAP = 5.0      # pt: max gap between caption lines
EDGE_PAD = 6.0      # pt: padding around the cropped region


def parse_pages(spec, n):
    if not spec:
        return list(range(n))
    out = set()
    for part in spec.split(","):
        a, _, b = part.partition("-")
        lo, hi = int(a), int(b or a)
        out.update(range(max(lo, 1) - 1, min(hi, n)))
    return sorted(out)


def same_line(a, b):
    return abs(a["top"] - b["top"]) <= LINE_TOL


def union(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def is_bold(page, word):
    for ch in page.chars:
        if abs(ch["top"] - word["top"]) <= LINE_TOL and word["x0"] - 0.5 <= ch["x0"] <= word["x1"]:
            name = ch.get("fontname", "")
            return any(k in name for k in ("Bold", "Black", "Semibold", "Heavy", "Demi"))
    return False


def find_captions(page, words):
    """Caption starts: (label, number, kind, bold, word_index)."""
    found = []
    for i, w in enumerate(words):
        text = w["text"].strip()
        m = JOINED_RE.match(text)
        if m:
            kind, num = LABELS[m.group(1).lower().rstrip(".")], m.group(2)
        elif LABEL_RE.match(text) and i + 1 < len(words) and same_line(w, words[i + 1]) \
                and 0 <= words[i + 1]["x0"] - w["x1"] <= 8 and NUM_RE.match(words[i + 1]["text"].strip()):
            kind = LABELS.get(text.lower().rstrip("."), "figure")
            num = NUM_RE.match(words[i + 1]["text"].strip()).group(1)
        else:
            continue
        # must start a line segment in its column: nothing just to its left on this line
        crowded = any(same_line(w, o) and 0 <= w["x0"] - o["x1"] < COL_GUTTER
                      for o in words if o is not w)
        if crowded:
            continue
        found.append({"kind": kind, "num": num, "bold": is_bold(page, w), "i": i})
    return found


def caption_block(words, start):
    """Bounding box and text of the caption that starts at words[start]."""
    w0 = words[start]
    seg = [w0]
    for o in sorted((o for o in words if same_line(o, w0) and o["x0"] > w0["x0"]), key=lambda o: o["x0"]):
        if o["x0"] - seg[-1]["x1"] > COL_GUTTER:
            break
        seg.append(o)
    left, right = w0["x0"], max(o["x1"] for o in seg)
    lines, bottom = [seg], max(o["bottom"] for o in seg)
    while True:
        nxt = [o for o in words if bottom < o["top"] <= bottom + CONT_GAP
               and o["x0"] >= left - 2 and o["x1"] <= right + 2]
        if not nxt:
            break
        top0 = min(o["top"] for o in nxt)
        line = sorted((o for o in nxt if abs(o["top"] - top0) <= LINE_TOL), key=lambda o: o["x0"])
        lines.append(line)
        bottom = max(o["bottom"] for o in line)
    flat = [o for ln in lines for o in ln]
    box = (left, min(o["top"] for o in flat), right, max(o["bottom"] for o in flat))
    text = ""
    for ln in lines:
        part = " ".join(o["text"] for o in ln)
        if text.endswith("-") and part[:1].islower():
            text = text[:-1] + part          # line-break hyphen: "homeo-" + "stasis"
        else:
            text = f"{text} {part}".strip()
    return box, text


def graphics(page):
    objs = []
    for kind in ("rects", "lines", "curves", "images"):
        for o in getattr(page, kind):
            if o["x1"] - o["x0"] > 0.97 * page.width and o["bottom"] - o["top"] > 0.97 * page.height:
                continue  # page frame
            objs.append({"box": (o["x0"], o["top"], o["x1"], o["bottom"]), "kind": kind})
    return objs


def grow(region, col, objs, gap):
    """Add graphic objects in the caption's column that sit within `gap` pt, repeatedly."""
    used, g_box = set(), None
    changed = True
    while changed:
        changed = False
        for k, o in enumerate(objs):
            if k in used:
                continue
            x0, top, x1, bottom = o["box"]
            overlap = min(x1, col[1]) - max(x0, col[0])
            if overlap < 0.5 * min(max(x1 - x0, 1.0), col[1] - col[0]):
                continue
            dist = max(top - region[3], region[1] - bottom, 0)
            if dist <= gap:
                region = union(region, o["box"])
                g_box = o["box"] if g_box is None else union(g_box, o["box"])
                used.add(k)
                changed = True
    return region, g_box, used


def render(page, box, dpi):
    x0 = max(box[0] - EDGE_PAD, 0)
    top = max(box[1] - EDGE_PAD, 0)
    x1 = min(box[2] + EDGE_PAD, page.width)
    bottom = min(box[3] + EDGE_PAD, page.height)
    im = page.crop((x0, top, x1, bottom), strict=False).to_image(resolution=dpi).original.convert("RGB")
    diff = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255)))
    bbox = diff.point(lambda v: 255 if v > 12 else 0).getbbox()
    if bbox:
        pad = 12
        im = im.crop((max(bbox[0] - pad, 0), max(bbox[1] - pad, 0),
                      min(bbox[2] + pad, im.width), min(bbox[3] + pad, im.height)))
    return im


def overlap_frac(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    if w <= 0 or h <= 0:
        return 0.0
    small = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
    return (w * h) / small if small > 0 else 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--out", default="snips")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--gap", type=float, default=24.0, help="max pt between caption and graphics")
    ap.add_argument("--min-pt", type=float, default=72.0, help="skip uncaptioned images smaller than this")
    ap.add_argument("--pages", default="", help="e.g. 2-5,8 (1-based)")
    args = ap.parse_args()
    if not os.path.isfile(args.pdf):
        sys.exit(f"not a file: {args.pdf}")
    os.makedirs(args.out, exist_ok=True)

    snips, skipped, names = [], [], set()
    with pdfplumber.open(args.pdf) as pdf:
        pages = parse_pages(args.pages, len(pdf.pages))
        # logos/headers: raster images of one size that recur on 2+ pages
        sizes = {}
        for pi in pages:
            for im in pdf.pages[pi].images:
                key = (round(im["x1"] - im["x0"]), round(im["bottom"] - im["top"]))
                sizes.setdefault(key, set()).add(pi)
        repeated = {k for k, v in sizes.items() if len(v) >= 2}

        for pi in pages:
            page = pdf.pages[pi]
            words = page.extract_words(keep_blank_chars=False, use_text_flow=False)
            objs = graphics(page)
            taken = []
            caps = sorted(find_captions(page, words), key=lambda c: not c["bold"])
            for c in caps:
                label = f"{c['kind'].capitalize()} {c['num']}"
                cbox, ctext = caption_block(words, c["i"])
                region, g_box, used = grow(cbox, (cbox[0] - 4, cbox[2] + 4), objs, args.gap)
                if g_box is None or (g_box[3] - g_box[1]) < 12:
                    skipped.append({"label": label, "page": pi + 1,
                                    "reason": "no graphic next to the caption (text-only table, or an in-text mention)"})
                    continue
                if any(overlap_frac(region, t) > 0.5 for t in taken):
                    continue  # a stronger caption already owns this region
                taken.append(region)
                base = f"{c['kind']}-{c['num'].lower()}"
                name = base if base not in names else f"{base}-p{pi + 1}"
                names.add(name)
                im = render(page, region, args.dpi)
                path = os.path.join(args.out, name + ".png")
                im.save(path, optimize=True)
                snips.append({"file": os.path.basename(path), "kind": c["kind"], "label": label,
                              "page": pi + 1, "caption": ctext, "bbox_pt": [round(v, 1) for v in region],
                              "size_px": list(im.size)})
            # uncaptioned raster images
            for k, im in enumerate(page.images):
                box = (im["x0"], im["top"], im["x1"], im["bottom"])
                w, h = box[2] - box[0], box[3] - box[1]
                if w < args.min_pt or h < args.min_pt:
                    continue
                if (round(w), round(h)) in repeated:
                    continue
                if any(overlap_frac(box, t) > 0.5 for t in taken):
                    continue
                name = f"image-p{pi + 1}-{k + 1}"
                pic = render(page, box, args.dpi)
                pic.save(os.path.join(args.out, name + ".png"), optimize=True)
                snips.append({"file": name + ".png", "kind": "image", "label": "", "page": pi + 1,
                              "caption": "", "bbox_pt": [round(v, 1) for v in box], "size_px": list(pic.size)})

    with open(os.path.join(args.out, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump({"source": os.path.basename(args.pdf), "dpi": args.dpi, "snips": snips,
                   "skipped": skipped}, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    for s in snips:
        print(f"snip  p{s['page']:<3} {s['file']:<24} {s['caption'][:70]}")
    for s in skipped:
        print(f"skip  p{s['page']:<3} {s['label']:<24} {s['reason']}")
    print(f"{len(snips)} snip(s), {len(skipped)} skipped -> {os.path.join(args.out, 'manifest.json')}")


if __name__ == "__main__":
    main()
