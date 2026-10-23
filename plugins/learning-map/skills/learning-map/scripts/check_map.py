#!/usr/bin/env python3
"""Check a learning map before it is written to the Learn page.

    python3 check_map.py <map.json> [--source <material.txt>] [--id <map-id>]

--source  the text of the material as read; every number in a pearl whose basis is
          "material" must appear in it.
--id      the map id the map will be saved under; checked against the slug rule.

Prints JSON {"ok", "errors", "warnings", "counts"} on stdout. Exit codes: 0 ok, 1 the map
breaks the contract, 2 usage error (a file is missing or is not JSON).
"""
import argparse
import json
import re
import sys

KINDS = {"paper", "chapter", "book", "article", "lecture", "video", "slides", "guideline",
         "code", "other"}
PEARL_TYPES = {"finding", "method", "caveat", "concept", "practice"}
BASES = {"material", "inference"}
STEP_KINDS = {"deeper", "wider", "apply", "challenge"}
YOU = {"own", "brush", "new"}
LEVEL_RANGE = {2: (3, 10), 1: (1, 10), 0: (1, 8)}
MAX_ITEMS = 25
PEARLS_RANGE = (5, 12)
PATH_RANGE = (3, 7)
MAX_INFERENCE = 3
GIST_MAX = 600
SIZE_WARN = 100_000
SIZE_MAX = 240_000

ITEM_ID = re.compile(r"^[a-z][a-z0-9-]{0,15}$")
MAP_ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LINK = re.compile(r"https?://|www\.|\bdoi\s*:|\b10\.\d{4,9}/", re.I)
NUMBER = re.compile(r"(?<![\d.])\.?\d+(?:[.,·]\d+)*")
DASHES = str.maketrans({"−": "-", "–": "-", "—": "-", "·": ".",
                        " ": " ", " ": " ", " ": " "})


def text(v):
    return v.strip() if isinstance(v, str) else ""


def norm_source(raw):
    """Normalise dashes, middle dots and thin spaces; also drop thousands separators."""
    s = raw.translate(DASHES)
    return s, re.sub(r"(?<=\d),(?=\d{3}\b)", "", s)


def number_in(token, sources):
    tok = token.replace("·", ".")
    plain = re.sub(r"(?<=\d),(?=\d{3}\b)", "", tok)
    cands = {tok, plain}
    for c in list(cands):
        if c.startswith("."):
            cands.add("0" + c)        # .05 written as 0.05
        elif c.startswith("0."):
            cands.add(c[1:])          # 0.05 written as .05
    for cand in cands:
        pat = re.compile(r"(?<![\d.])" + re.escape(cand) + r"(?![\d])")
        if any(pat.search(s) for s in sources):
            return True
    return False


def check(m, source_text=None, map_id=None):
    errors, warnings = [], []
    err, warn = errors.append, warnings.append

    if map_id is not None:
        if not (MAP_ID.match(map_id) and len(map_id) <= 40):
            err(f"map id {map_id!r}: kebab-case, letters a-z, digits and '-', at most 40 chars")

    if not isinstance(m, dict):
        return {"ok": False, "errors": ["the map is not a JSON object"], "warnings": [],
                "counts": {}}

    for key in ("title", "field", "gist"):
        if not text(m.get(key)):
            err(f"{key}: missing or empty")
    if len(text(m.get("gist"))) > GIST_MAX:
        err(f"gist: {len(text(m.get('gist')))} chars (max {GIST_MAX})")
    if m.get("kind") not in KINDS:
        err(f"kind: {m.get('kind')!r} is not one of {sorted(KINDS)}")
    if not DATE.match(text(m.get("date"))):
        err("date: must be YYYY-MM-DD")
    src = m.get("source")
    if not isinstance(src, dict):
        err("source: missing (needs cite and read)")
    else:
        for key in ("cite", "read"):
            if not text(src.get(key)):
                err(f"source.{key}: missing or empty")
        url = src.get("url")
        if url not in (None, "") and not re.match(r"^https?://\S+$", str(url)):
            err("source.url: must be an http(s) URL")
        if text(src.get("read")) and "full" not in text(src.get("read")).lower():
            warn(f"source.read is {text(src.get('read'))!r}: the page will flag the map as partial")

    # ---- ladder
    ladder = m.get("ladder")
    items = {}
    if not isinstance(ladder, list) or not ladder:
        err("ladder: missing or empty")
        ladder = []
    for i, it in enumerate(ladder, 1):
        where = f"ladder[{i}]"
        if not isinstance(it, dict):
            err(f"{where}: not an object")
            continue
        iid = it.get("id")
        if not isinstance(iid, str) or not ITEM_ID.match(iid):
            err(f"{where}: id {iid!r} must be short lowercase (a-z, 0-9, '-')")
            continue
        if iid in items:
            err(f"{where}: duplicate id {iid!r}")
            continue
        where = f"ladder {iid}"
        lvl = it.get("level")
        if lvl not in (0, 1, 2) or isinstance(lvl, bool):
            err(f"{where}: level must be 0, 1 or 2")
            continue
        for key in ("name", "field", "primer", "why"):
            if not text(it.get(key)):
                err(f"{where}: {key} missing or empty")
        if lvl == 2 and not text(it.get("where")):
            err(f"{where}: level 2 items need 'where' (the place in the material)")
        for key in ("name", "primer", "why", "where"):
            if LINK.search(text(it.get(key))):
                err(f"{where}: {key} carries a link or DOI; the ladder is concepts only")
        if len(text(it.get("primer"))) > 500:
            warn(f"{where}: primer is {len(text(it.get('primer')))} chars; one to three sentences")
        you = it.get("you")
        if you is not None and you not in YOU:
            err(f"{where}: you must be one of {sorted(YOU)} or left out")
        needs = it.get("needs", [])
        if not isinstance(needs, list) or not all(isinstance(n, str) for n in needs):
            err(f"{where}: needs must be a list of ids")
            needs = []
        items[iid] = {"level": lvl, "needs": needs}

    needed = set()
    for iid, it in items.items():
        seen = set()
        for n in it["needs"]:
            if n in seen:
                err(f"ladder {iid}: needs {n!r} twice")
            seen.add(n)
            if n == iid:
                err(f"ladder {iid}: needs itself")
            elif n not in items:
                err(f"ladder {iid}: needs unknown id {n!r}")
            elif items[n]["level"] >= it["level"]:
                err(f"ladder {iid} (level {it['level']}): needs {n!r} (level {items[n]['level']}); "
                    "edges must point to a lower level")
            else:
                needed.add(n)
    for iid, it in items.items():
        if it["level"] < 2 and iid not in needed:
            err(f"ladder {iid} (level {it['level']}): nothing above it needs it; drop it or move it")

    counts = {f"level{lv}": sum(1 for it in items.values() if it["level"] == lv) for lv in (0, 1, 2)}
    for lv, (lo, hi) in LEVEL_RANGE.items():
        n = counts[f"level{lv}"]
        if not lo <= n <= hi:
            err(f"ladder: level {lv} has {n} items (allowed {lo}-{hi})")
    if len(items) > MAX_ITEMS:
        err(f"ladder: {len(items)} items (max {MAX_ITEMS})")
    yous = [it.get("you") for it in ladder if isinstance(it, dict)]
    if any(y is not None for y in yous) and any(y is None for y in yous):
        warn("ladder: 'you' is set on some items only; set it on all or none")

    # ---- pearls
    pearls = m.get("pearls")
    if not isinstance(pearls, list):
        err("pearls: missing")
        pearls = []
    if not PEARLS_RANGE[0] <= len(pearls) <= PEARLS_RANGE[1]:
        err(f"pearls: {len(pearls)} (allowed {PEARLS_RANGE[0]}-{PEARLS_RANGE[1]})")
    sources = norm_source(source_text) if source_text is not None else None
    inference = 0
    for i, p in enumerate(pearls, 1):
        where = f"pearl {i}"
        if not isinstance(p, dict):
            err(f"{where}: not an object")
            continue
        body = text(p.get("text"))
        if not body:
            err(f"{where}: text missing or empty")
        if not text(p.get("where")):
            err(f"{where}: where missing (the place in the material)")
        if p.get("type") not in PEARL_TYPES:
            err(f"{where}: type {p.get('type')!r} is not one of {sorted(PEARL_TYPES)}")
        if p.get("basis") not in BASES:
            err(f"{where}: basis must be 'material' or 'inference'")
        if p.get("basis") == "inference":
            inference += 1
        if LINK.search(body):
            err(f"{where}: carries a link or DOI; the source link belongs in source.url")
        uses = p.get("uses", [])
        if not isinstance(uses, list):
            err(f"{where}: uses must be a list of ladder ids")
            uses = []
        for u in uses:
            if u not in items:
                err(f"{where}: uses unknown ladder id {u!r}")
        if sources is not None and p.get("basis") == "material" and body:
            for tok in NUMBER.findall(body.translate(DASHES)):
                if not number_in(tok, sources):
                    err(f"{where}: number {tok} is not in the source text; copy the material's number")
    if inference > MAX_INFERENCE:
        err(f"pearls: {inference} inference pearls (max {MAX_INFERENCE})")

    # ---- path
    path = m.get("path")
    if not isinstance(path, list):
        err("path: missing")
        path = []
    if not PATH_RANGE[0] <= len(path) <= PATH_RANGE[1]:
        err(f"path: {len(path)} steps (allowed {PATH_RANGE[0]}-{PATH_RANGE[1]})")
    kinds = []
    for i, s in enumerate(path, 1):
        where = f"path step {i}"
        if not isinstance(s, dict):
            err(f"{where}: not an object")
            continue
        for key in ("topic", "why", "question"):
            if not text(s.get(key)):
                err(f"{where}: {key} missing or empty")
        if s.get("kind") not in STEP_KINDS:
            err(f"{where}: kind {s.get('kind')!r} is not one of {sorted(STEP_KINDS)}")
        kinds.append(s.get("kind"))
        for key in ("topic", "why", "question"):
            if LINK.search(text(s.get(key))):
                err(f"{where}: {key} carries a link or DOI; the path is concepts only")
        for lid in s.get("ladder", []) if isinstance(s.get("ladder", []), list) else []:
            if lid not in items:
                err(f"{where}: ladder id {lid!r} is not in the ladder")
        for pn in s.get("pearls", []) if isinstance(s.get("pearls", []), list) else []:
            if not (isinstance(pn, int) and not isinstance(pn, bool) and 1 <= pn <= len(pearls)):
                err(f"{where}: pearl number {pn!r} is out of range")
    if path and "deeper" not in kinds:
        err("path: needs at least one 'deeper' step")
    if path and not ({"wider", "challenge"} & set(kinds)):
        err("path: needs at least one 'wider' or 'challenge' step")

    size = len(json.dumps(m, ensure_ascii=False).encode("utf-8"))
    if size > SIZE_MAX:
        err(f"map is {size} bytes (max {SIZE_MAX}; the store caps a document at 256 KiB)")
    elif size > SIZE_WARN:
        warn(f"map is {size} bytes; keep it under about {SIZE_WARN}")

    counts.update({"pearls": len(pearls), "path": len(path), "bytes": size})
    return {"ok": not errors, "errors": errors, "warnings": warnings, "counts": counts}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check a learning map before saving it to Learn.")
    ap.add_argument("map")
    ap.add_argument("--source", help="text file of the material as read")
    ap.add_argument("--id", dest="map_id", help="the map id it will be saved under")
    args = ap.parse_args(argv)
    try:
        with open(args.map, encoding="utf-8") as f:
            m = json.load(f)
        source_text = None
        if args.source:
            with open(args.source, encoding="utf-8") as f:
                source_text = f.read()
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [f"cannot read input: {exc}"]}))
        return 2
    result = check(m, source_text, args.map_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
