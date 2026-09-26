#!/usr/bin/env python3
"""coverage_check.py — the measured gate for a bullet-reconstruct run.

Reads units.json: the substantive units enumerated from the SOURCE before the bullets
were written, each scored against the reconstruction. Reports

    loss = (missing + distorted + 0.5 * partial) / total      PASS when loss < --ceiling

What makes it measured rather than self-reported:
  --output FILE   the reconstruction (.md or .html). A unit scored present/partial whose
                  `anchors` (its numbers, names, key terms) do not all occur in FILE is
                  downgraded: some anchors found -> partial, none found -> missing.
  --source FILE   the source as plain text. Every number in the reconstruction must occur
                  in the source (number words such as "seven" count as 7); a number that
                  does not is a FAIL (changed or invented). --allow lists deliberate ones.
Also reports unit density (units per 1,000 source words). Under --min-density (default 10)
is a WARN: units that coarse make the loss % meaningless.

Usage:
  python3 coverage_check.py units.json --output notes.md --source source.txt
  python3 coverage_check.py units.json --ceiling 0.05

units.json:
  {"source": "label",
   "units": [{"id": 1, "unit": "one checkable fact", "anchors": ["39.7", "ISI"],
              "status": "present|partial|missing|distorted", "note": "optional"}]}

Exit 0 on PASS, 1 on FAIL, 2 on a usage or input error.
"""
import argparse
import html
import json
import re
import sys

VALID = ("present", "partial", "missing", "distorted")
WEIGHT = {"present": 0.0, "partial": 0.5, "missing": 1.0, "distorted": 1.0}
NUMBER_WORDS = ("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                "fourteen fifteen sixteen seventeen eighteen nineteen twenty").split()
NUM_RE = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)*")


def die(msg):
    print(msg, file=sys.stderr)
    sys.exit(2)


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        die(f"cannot read {path}: {exc}")


def plain(text):
    """Visible text: drop data URIs, tags, entities and markdown emphasis; unify dashes and
    spaces; lowercase. Applied to anchors and output alike, so both compare the same way."""
    text = re.sub(r"data:[a-z]+/[a-z0-9.+-]+;base64,[A-Za-z0-9+/=]+", " ", text)
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|])", r"\1", text)   # markdown escapes: STAR\*D
    text = re.sub(r"[*`]|(?<!\w)__|__(?!\w)", "", text)            # **bold**, *em*, `code`, __bold__
    text = re.sub(r"[‐-―−]", "-", text).replace(" ", " ")
    return re.sub(r"\s+", " ", text).lower()


def numbers(text, words_to_digits=False):
    if words_to_digits:
        for i, w in enumerate(NUMBER_WORDS):
            text = re.sub(rf"\b{w}\b", str(i), text)
    return {m.group().replace(",", "") for m in NUM_RE.finditer(text)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("units_file")
    ap.add_argument("--output", help="the reconstruction (.md or .html)")
    ap.add_argument("--source", help="the source as plain text")
    ap.add_argument("--ceiling", type=float, default=0.10, help="max loss (default 0.10)")
    ap.add_argument("--min-density", type=float, default=10.0, help="units per 1,000 source words")
    ap.add_argument("--allow", default="", help="comma-separated numbers the notes derive on purpose")
    args = ap.parse_args()

    try:
        data = json.loads(read(args.units_file))
    except ValueError as exc:
        die(f"invalid JSON in {args.units_file}: {exc}")
    units = data.get("units", []) if isinstance(data, dict) else []
    if not units:
        die("no units. Enumerate substantive units from the SOURCE first (one per claim, number or named entity).")

    out_text = plain(read(args.output)) if args.output else None
    src_raw = read(args.source) if args.source else None

    rows, downgraded, no_anchor = [], [], 0
    for u in units:
        status = str(u.get("status", "")).strip().lower()
        if status not in VALID:
            die(f"unit id={u.get('id')!r}: status {u.get('status')!r} is not one of {list(VALID)}")
        anchors = [a for a in u.get("anchors", []) if isinstance(a, str) and a.strip()]
        if not anchors:
            no_anchor += 1
        if out_text is not None and anchors and status in ("present", "partial"):
            found = [a for a in anchors if plain(a) in out_text]
            new = status
            if not found:
                new = "missing"
            elif len(found) < len(anchors) and status == "present":
                new = "partial"
            if new != status:
                lost = [a for a in anchors if a not in found]
                downgraded.append((u.get("id"), status, new, lost))
                status = new
        rows.append((u.get("id"), u.get("unit", ""), status, u.get("note", "")))

    total = len(rows)
    counts = {s: sum(1 for r in rows if r[2] == s) for s in VALID}
    loss = sum(WEIGHT[r[2]] for r in rows) / total
    passed = loss < args.ceiling

    bad_numbers = []
    if src_raw is not None and args.output:
        allowed = {a.strip() for a in args.allow.split(",") if a.strip()}
        src_nums = numbers(plain(src_raw), words_to_digits=True)
        bad_numbers = sorted(n for n in numbers(out_text) - src_nums - allowed)
        if bad_numbers:
            passed = False

    bar = "=" * 60
    print(bar)
    print(f"Source        : {data.get('source', '(unnamed source)')}")
    print(f"Total units   : {total}   ({no_anchor} without anchors: self-graded only)")
    print(f"  present     : {counts['present']}")
    print(f"  partial     : {counts['partial']}   (half loss each)")
    print(f"  missing     : {counts['missing']}")
    print(f"  distorted   : {counts['distorted']}   (full loss each: changed number, name or direction)")
    print(f"Loss          : {loss:6.1%}   (ceiling {args.ceiling:.0%})")
    if src_raw is not None:
        n_words = len(src_raw.split())
        density = total / (n_words / 1000) if n_words else 0.0
        warn = "  WARN: too coarse, split units" if density < args.min_density else ""
        print(f"Unit density  : {density:.1f} per 1,000 source words{warn}")
        if args.output:
            print(f"Numbers       : {'all found in source' if not bad_numbers else 'NOT in source: ' + ', '.join(bad_numbers)}")
    if out_text is None:
        print("Output check  : skipped (no --output): statuses are self-reported")
    print(f"RESULT        : {'PASS' if passed else 'FAIL: fix the items below, then re-run'}")
    print(bar)
    if downgraded:
        print("\nDowngraded by the anchor check (scored higher than the output supports):")
        for i, old, new, lost in downgraded:
            print(f"  id={i}: {old} -> {new}; not in output: {', '.join(lost)}")
    gaps = [r for r in rows if r[2] != "present"]
    if gaps:
        print("\nUnits to reinstate or correct:")
        for i, text, s, note in gaps:
            print(f"  [{s.upper():>9}] id={i}: {text}" + (f"  ({note})" if note else ""))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
