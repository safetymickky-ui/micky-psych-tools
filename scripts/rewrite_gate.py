#!/usr/bin/env python3
"""Safety nets for the plugin rewrite (spec S12, interface I17): ratchet, trigger lock,
h-coverage checklist and baseline measurements, for micky-psych-tools.

    rewrite_gate.py ratchet init [--write]
    rewrite_gate.py ratchet seed --check <id> [--from <violations.json>] [--new] [--write]
    rewrite_gate.py ratchet verify [--base <git-ref>]
    rewrite_gate.py ratchet close --check <id> --path <path> [--write]
    rewrite_gate.py triggers extract [--skill <s>] [--write]
    rewrite_gate.py triggers verify
    rewrite_gate.py triggers remove --reason <r> --skill <s> [--phrase <p>] [--write]
    rewrite_gate.py h-coverage seed --from <architecture.md> [--write]
    rewrite_gate.py h-coverage close --id <Hnn[a|b]> --wave <Wn> [--write]
    rewrite_gate.py baseline measure [--wave W0] [--plugin-dir <dir>]... [--learn-hub <dir>] [--write]

Every command takes --repo <path> (default: the repo that holds this script).
Dry run by default: --write is the only flag that changes a file. Output is JSON on
stdout. Exit codes: 0 ok, 1 a verify found a violation or a change was refused,
2 usage error.

Files (docs/rewrite/, all UTF-8 with a trailing newline):
  ratchet.json        {"schema":1,"generated_at","repo","entries":[{check_id,path,message}]}
                      A listed (check_id, path) warns; an unlisted one fails. The file may
                      only shrink: verify fails when a check_id's count grows against the
                      base commit, except a check_id the base does not have (first seed).
  triggers.lock.json  {"schema":1,"phrases":[{phrase,kind,skill,field}],"removed":[...]}
                      kind quoted = text in "..." or curly quotes (measure.py's QUOTE_RE);
                      kind slash = a bare /command token outside quotes. verify fails when a
                      locked phrase no longer scans and was not retired with remove.
  h-coverage.md       Appendix A (H01-H49) of architecture.md as a checklist; split waves
                      (W1/W3, W1/W2) become two rows Hnna / Hnnb.
  baseline.md         one dated "## <wave> — <date>" section per wave exit. measure never
                      touches "## W0 smoke", "## Owner records" or "## W5 decisions".

The functions below are importable (ratchet_verify, triggers_verify, h_coverage_close, ...).
"""
import argparse
import datetime
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = 1
RATCHET = os.path.join("docs", "rewrite", "ratchet.json")
LOCK = os.path.join("docs", "rewrite", "triggers.lock.json")
HCOV = os.path.join("docs", "rewrite", "h-coverage.md")
BASELINE = os.path.join("docs", "rewrite", "baseline.md")
SKILL_GLOBS = ("plugins/*/skills/*/SKILL.md",)
FIELDS = ("description", "when_to_use")

# Same expression as docs/plugin-rewrite/phase3/measure.py, so the lock and measure.py agree.
QUOTE_RE = re.compile(r'"([^"\n]{1,120})"|“([^”\n]{1,120})”')
SLASH_RE = re.compile(r"(?<![\w/.:~-])(/[a-z][a-z0-9-]*)(?![\w/-]|\.\w)")
FM_RE = re.compile(r"^---\n(.*?)\n---[ \t]*(?:\n|$)", re.S)


class UsageError(Exception):
    pass


class Refused(Exception):
    pass


# ---------------------------------------------------------------- shared helpers

def today():
    return datetime.date.today().isoformat()


def repo_name(repo):
    path = os.path.join(repo, ".claude-plugin", "marketplace.json")
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh).get("name") or os.path.basename(os.path.abspath(repo))
    except (OSError, ValueError, AttributeError):
        return os.path.basename(os.path.abspath(repo))


def read_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def dump_json(data):
    """Pretty JSON, but every element of a list of objects on one line (diff-friendly)."""
    if not isinstance(data, dict):
        return json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    parts = []
    for key, value in data.items():
        k = json.dumps(key, ensure_ascii=False)
        if isinstance(value, list) and value and all(isinstance(v, dict) for v in value):
            items = ",\n".join("    " + json.dumps(v, ensure_ascii=False) for v in value)
            parts.append(f"  {k}: [\n{items}\n  ]")
        else:
            parts.append(f"  {k}: {json.dumps(value, ensure_ascii=False)}")
    return "{\n" + ",\n".join(parts) + "\n}\n"


def write_text(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def rel(repo, path):
    return os.path.relpath(path, repo).replace(os.sep, "/")


def split_frontmatter(text):
    """(frontmatter text or None, body). CRLF-safe."""
    text = text.replace("\r\n", "\n")
    m = FM_RE.match(text)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def yaml_error(fm_text):
    """None when the block is a valid YAML mapping, else a one-line error."""
    if yaml is None:
        return "PyYAML is not installed"
    try:
        data = yaml.safe_load(fm_text)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        problem = getattr(exc, "problem", None)
        if problem and mark is not None:
            return f"{problem} (file line {mark.line + 2}, column {mark.column + 1})"
        return " ".join(str(exc).split())
    if data is not None and not isinstance(data, dict):
        return f"frontmatter is a {type(data).__name__}, not a mapping"
    return None


def raw_field(fm_text, key):
    """Read one top-level scalar with a raw-line reader (for YAML-invalid frontmatter)."""
    lines = fm_text.split("\n")
    for i, line in enumerate(lines):
        m = re.match(rf"^{re.escape(key)}:\s*(.*)$", line)
        if not m:
            continue
        value = m.group(1).strip()
        block = value in (">", ">-", ">+", "|", "|-", "|+")
        parts = [] if block else [value]
        for nxt in lines[i + 1:]:
            if nxt.startswith((" ", "\t")) or (block and not nxt.strip()):
                parts.append(nxt.strip())
            else:
                break
        text = " ".join(p for p in parts if p)
        if not block and len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
            text = text[1:-1]
        return text
    return None


def frontmatter_fields(path):
    """({field: text}, parse_mode) for a SKILL.md; parse_mode is 'yaml' or 'raw-line'."""
    with open(path, encoding="utf-8") as fh:
        fm_text, _ = split_frontmatter(fh.read())
    if fm_text is None:
        return {}, "none"
    if yaml is not None and yaml_error(fm_text) is None:
        data = yaml.safe_load(fm_text) or {}
        return {k: data[k] for k in FIELDS if isinstance(data.get(k), str)}, "yaml"
    out = {}
    for key in FIELDS:
        value = raw_field(fm_text, key)
        if value is not None:
            out[key] = value
    return out, "raw-line"


# ---------------------------------------------------------------- ratchet

def empty_ratchet(repo, date=None):
    return {"schema": SCHEMA, "generated_at": date or today(), "repo": repo_name(repo), "entries": []}


def load_ratchet(repo):
    path = os.path.join(repo, RATCHET)
    if not os.path.isfile(path):
        raise Refused(f"{RATCHET} not found (create it with S12-W0-1)")
    return read_json(path)


def ratchet_schema_errors(data):
    errors = []
    if not isinstance(data, dict):
        return ["ratchet.json is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append(f"schema is {data.get('schema')!r}, expected {SCHEMA}")
    entries = data.get("entries")
    if not isinstance(entries, list):
        return errors + ["entries is not a list"]
    seen = set()
    for i, e in enumerate(entries):
        if not isinstance(e, dict) or not all(isinstance(e.get(k), str) and e.get(k) for k in
                                              ("check_id", "path", "message")):
            errors.append(f"entries[{i}] needs non-empty string check_id, path and message")
            continue
        key = (e["check_id"], e["path"])
        if key in seen:
            errors.append(f"entries[{i}] duplicates {key[0]} {key[1]}")
        seen.add(key)
    return errors


def ratchet_counts(data):
    counts = {}
    for e in (data or {}).get("entries", []) or []:
        if isinstance(e, dict) and e.get("check_id"):
            counts[e["check_id"]] = counts.get(e["check_id"], 0) + 1
    return counts


def compare_ratchet(base, current):
    """Shrink-only rule. base None = no earlier file (everything is a first seed)."""
    errors = []
    base_counts = ratchet_counts(base) if base is not None else {}
    cur_counts = ratchet_counts(current)
    for check_id, n in sorted(cur_counts.items()):
        if base is not None and check_id in base_counts and n > base_counts[check_id]:
            errors.append(f"{check_id}: {base_counts[check_id]} -> {n} entries; the ratchet may only "
                          "shrink (fix the new violation instead of listing it)")
    return errors


def collect_yaml_parse(repo):
    """Current yaml-parse violations: every plugin skill/command/agent frontmatter."""
    found = []
    patterns = ("plugins/*/skills/*/SKILL.md", "plugins/*/commands/*.md", "plugins/*/agents/*.md")
    for pattern in patterns:
        for path in sorted(glob.glob(os.path.join(repo, pattern))):
            with open(path, encoding="utf-8") as fh:
                fm_text, _ = split_frontmatter(fh.read())
            if fm_text is None:
                continue
            err = yaml_error(fm_text)
            if err:
                found.append({"path": rel(repo, path), "message": f"yaml-error: {err}"})
    return found


COLLECTORS = {"yaml-parse": collect_yaml_parse}


def git_show(repo, ref, path):
    """Text of path at ref, or None when git, the ref or the file is unavailable."""
    try:
        res = subprocess.run(["git", "-C", repo, "show", f"{ref}:{path.replace(os.sep, '/')}"],
                             capture_output=True, text=True, encoding="utf-8")
    except OSError:
        return None
    return res.stdout if res.returncode == 0 else None


def ratchet_init(repo, write=False, date=None):
    path = os.path.join(repo, RATCHET)
    if os.path.exists(path):
        raise Refused(f"{RATCHET} exists; it is created once")
    data = empty_ratchet(repo, date)
    if write:
        write_text(path, dump_json(data))
    return {"ok": True, "action": "init", "entries": 0, "written": write}


def ratchet_seed(repo, check_id, source=None, new=False, write=False, date=None):
    data = load_ratchet(repo)
    if check_id in ratchet_counts(data):
        raise Refused(f"{check_id} already has entries; the ratchet may only shrink "
                      "(close fixed entries; never re-seed)")
    if source:
        raw = read_json(source)
        items = raw.get("entries", raw) if isinstance(raw, dict) else raw
        if not isinstance(items, list):
            raise UsageError("--from must hold a JSON list of {path, message}")
    elif check_id in COLLECTORS:
        items = COLLECTORS[check_id](repo)
    else:
        raise UsageError(f"no built-in collector for {check_id}; pass --from <violations.json>")
    added = []
    for item in items:
        if not isinstance(item, dict) or not item.get("path"):
            raise UsageError("each violation needs a path")
        added.append({"check_id": check_id, "path": item["path"],
                      "message": item.get("message") or check_id})
    data["entries"] = data.get("entries", []) + added
    data["generated_at"] = date or today()
    if write:
        write_text(os.path.join(repo, RATCHET), dump_json(data))
    return {"ok": True, "action": "seed", "check_id": check_id, "new": bool(new),
            "added": added, "written": write}


def ratchet_close(repo, check_id, path, write=False, date=None):
    data = load_ratchet(repo)
    entries = data.get("entries", [])
    keep = [e for e in entries if not (e.get("check_id") == check_id and e.get("path") == path)]
    if len(keep) == len(entries):
        raise Refused(f"no ratchet entry {check_id} {path}")
    data["entries"] = keep
    data["generated_at"] = date or today()
    if write:
        write_text(os.path.join(repo, RATCHET), dump_json(data))
    return {"ok": True, "action": "close", "check_id": check_id, "path": path, "written": write}


def ratchet_verify(repo, base_ref="HEAD", base=None, base_given=False):
    """Schema + shrink-only against base_ref (or an explicit base dict when base_given)."""
    current = load_ratchet(repo)
    errors = ratchet_schema_errors(current)
    warnings = []
    if not base_given:
        text = git_show(repo, base_ref, RATCHET)
        base = None
        if text is None:
            warnings.append(f"no {RATCHET} at {base_ref}; every check_id counts as a first seed")
        else:
            try:
                base = json.loads(text)
            except ValueError:
                warnings.append(f"{RATCHET} at {base_ref} is not valid JSON; not compared")
    if not errors:
        errors += compare_ratchet(base, current)
    listed = {(e["check_id"], e["path"]) for e in current.get("entries", []) if isinstance(e, dict)}
    for check_id, collect in COLLECTORS.items():
        if not any(c == check_id for c, _ in listed):
            continue
        live = {v["path"] for v in collect(repo)}
        for c, p in sorted(listed):
            if c == check_id and p not in live:
                warnings.append(f"{c} {p} is fixed; close it: rewrite_gate.py ratchet close "
                                f"--check {c} --path {p} --write")
    return {"ok": not errors, "counts": ratchet_counts(current), "errors": errors, "warnings": warnings}


# ---------------------------------------------------------------- trigger lock

def find_skills(repo):
    """{skill name: SKILL.md path} over the micky scan roots."""
    out = {}
    for pattern in SKILL_GLOBS:
        for path in sorted(glob.glob(os.path.join(repo, pattern))):
            out.setdefault(os.path.basename(os.path.dirname(path)), path)
    return out


def phrases_in(text):
    """[(phrase, kind)] in order of appearance: quoted phrases, then bare slash tokens."""
    text = text or ""
    found = []
    for m in QUOTE_RE.finditer(text):
        found.append((m.group(1) if m.group(1) is not None else m.group(2), "quoted"))
    unquoted = QUOTE_RE.sub(lambda m: " " * len(m.group(0)), text)
    for m in SLASH_RE.finditer(unquoted):
        found.append((m.group(1), "slash"))
    return found


def scan_skill(skill, path):
    fields, mode = frontmatter_fields(path)
    rows, seen = [], set()
    for field in FIELDS:
        for phrase, kind in phrases_in(fields.get(field, "")):
            key = (phrase, kind, skill, field)
            if key not in seen:
                seen.add(key)
                rows.append({"phrase": phrase, "kind": kind, "skill": skill, "field": field})
    return rows, mode


def scan_repo(repo, only=None):
    skills = find_skills(repo)
    if only is not None and only not in skills:
        raise UsageError(f"skill {only} not found under {', '.join(SKILL_GLOBS)}")
    rows, modes = [], {}
    for skill in sorted(skills):
        if only is not None and skill != only:
            continue
        found, mode = scan_skill(skill, skills[skill])
        rows += found
        modes[skill] = mode
    return rows, modes


def entry_key(e):
    return (e.get("phrase"), e.get("kind"), e.get("skill"), e.get("field"))


def load_lock(repo):
    path = os.path.join(repo, LOCK)
    if not os.path.isfile(path):
        return {"schema": SCHEMA, "phrases": [], "removed": []}
    return read_json(path)


def triggers_extract(repo, skill=None, write=False):
    lock = load_lock(repo)
    scanned, modes = scan_repo(repo, skill)
    known = {entry_key(e) for e in lock.get("phrases", [])}
    added = [e for e in scanned if entry_key(e) not in known]
    live = {entry_key(e) for e in scanned}
    missing = [e for e in lock.get("phrases", [])
               if (skill is None or e.get("skill") == skill) and entry_key(e) not in live]
    counts = {}
    for e in scanned:
        counts[e["skill"]] = counts.get(e["skill"], 0) + 1
    no_phrases = sorted(s for s in modes if not counts.get(s))
    lock["schema"] = SCHEMA
    lock["phrases"] = lock.get("phrases", []) + added
    lock.setdefault("removed", [])
    if write:
        write_text(os.path.join(repo, LOCK), dump_json(lock))
    return {"ok": not missing, "added": len(added), "total": len(lock["phrases"]),
            "per_skill": counts, "no_phrases": no_phrases,
            "raw_line_fallback": sorted(s for s, m in modes.items() if m == "raw-line"),
            "missing": missing, "written": write}


def triggers_verify(repo):
    path = os.path.join(repo, LOCK)
    if not os.path.isfile(path):
        return {"ok": False, "errors": [f"{LOCK} not found (run triggers extract --write)"],
                "warnings": []}
    lock = read_json(path)
    errors, warnings = [], []
    if lock.get("schema") != SCHEMA:
        errors.append(f"schema is {lock.get('schema')!r}, expected {SCHEMA}")
    skills = find_skills(repo)
    scanned, _ = scan_repo(repo)
    live = {entry_key(e) for e in scanned}
    locked = set()
    for e in lock.get("phrases", []):
        locked.add(entry_key(e))
        if e.get("skill") not in skills:
            errors.append(f"skill {e.get('skill')} not found for locked phrase {e.get('phrase')!r}; "
                          f"retire it: triggers remove --skill {e.get('skill')} --reason <r> --write")
        elif entry_key(e) not in live:
            errors.append(f"{e.get('skill')} {e.get('field')}: locked {e.get('kind')} phrase "
                          f"{e.get('phrase')!r} no longer scans; restore it or retire it: triggers "
                          f"remove --phrase {json.dumps(e.get('phrase'), ensure_ascii=False)} "
                          f"--skill {e.get('skill')} --reason <r> --write")
    unlocked = sorted({f"{s}: {p!r}" for (p, k, s, f) in live - locked})
    if unlocked:
        warnings.append(f"{len(unlocked)} phrase(s) not in the lock yet (triggers extract --write): "
                        + "; ".join(unlocked[:10]) + (" ..." if len(unlocked) > 10 else ""))
    return {"ok": not errors, "locked": len(lock.get("phrases", [])),
            "removed": len(lock.get("removed", [])), "errors": errors, "warnings": warnings}


def triggers_remove(repo, reason, skill, phrase=None, write=False, date=None):
    if not reason or not reason.strip():
        raise UsageError("--reason is required")
    lock = load_lock(repo)
    hit = [e for e in lock.get("phrases", [])
           if e.get("skill") == skill and (phrase is None or e.get("phrase") == phrase)]
    if not hit:
        raise Refused(f"no locked phrase for skill {skill}" + (f" matching {phrase!r}" if phrase else ""))
    drop = {entry_key(e) for e in hit}
    lock["phrases"] = [e for e in lock["phrases"] if entry_key(e) not in drop]
    stamp = date or today()
    lock.setdefault("removed", [])
    lock["removed"] += [dict(e, reason=reason, date=stamp) for e in hit]
    if write:
        write_text(os.path.join(repo, LOCK), dump_json(lock))
    return {"ok": True, "removed": hit, "written": write}


# ---------------------------------------------------------------- h-coverage

HCOV_HEADER = """# HIGH-defect coverage (H01-H49)

Appendix A of `docs/plugin-rewrite/architecture.md` as a checklist (spec S12, I17).
Canonical copy: micky-psych-tools; learn-hub holds a byte-for-byte copy. Rows split
across two waves are H<nn>a (first wave) and H<nn>b (second wave). Close rows only
in the wave's tag step: `python3 scripts/rewrite_gate.py h-coverage close --id <H> --wave <Wn> --write`.

"""
ROW_RE = re.compile(r"^- \[( |x)\] (H\d\d[ab]?) (.*) — closed: (no|yes) — wave: (W\d)$")


def parse_appendix_a(text):
    rows = []
    for line in text.split("\n"):
        if not re.match(r"^\| H\d\d \|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            raise UsageError(f"Appendix A row has {len(cells)} cells, expected 6: {line[:60]}")
        hid, inventory, defect, _evidence, _fix, wave = cells
        waves = wave.split("/")
        if not all(re.fullmatch(r"W\d", w) for w in waves) or len(waves) > 2:
            raise UsageError(f"{hid}: unreadable wave {wave!r}")
        if len(waves) == 1:
            rows.append((hid, inventory, defect, waves[0]))
        else:
            rows.append((hid + "a", inventory, defect, waves[0]))
            rows.append((hid + "b", inventory, defect, waves[1]))
    return rows


def h_coverage_render(rows):
    body = "".join(f"- [ ] {hid} {inv} — {defect} — closed: no — wave: {wave}\n"
                   for hid, inv, defect, wave in rows)
    return HCOV_HEADER + body


def h_coverage_seed(repo, source, write=False):
    path = os.path.join(repo, HCOV)
    if os.path.exists(path):
        raise Refused(f"{HCOV} exists; it is seeded once (close rows instead)")
    with open(source, encoding="utf-8") as fh:
        rows = parse_appendix_a(fh.read())
    if not rows:
        raise UsageError(f"no Appendix A rows (| Hnn |) in {source}")
    text = h_coverage_render(rows)
    if write:
        write_text(path, text)
    return {"ok": True, "rows": len(rows), "written": write}


def h_coverage_close(repo, hid, wave, write=False):
    path = os.path.join(repo, HCOV)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    ids = []
    for i, line in enumerate(lines):
        m = ROW_RE.match(line)
        if not m:
            continue
        ids.append(m.group(2))
        if m.group(2) != hid:
            continue
        if m.group(5) != wave:
            raise Refused(f"{hid} is assigned to {m.group(5)}, not {wave}")
        if m.group(1) == "x":
            raise Refused(f"{hid} is already closed")
        lines[i] = f"- [x] {hid} {m.group(3)} — closed: yes — wave: {wave}"
        if write:
            write_text(path, "\n".join(lines))
        return {"ok": True, "closed": hid, "wave": wave, "written": write}
    near = [i for i in ids if i.startswith(hid)]
    raise UsageError(f"no row {hid}" + (f"; did you mean {', '.join(near)}?" if near else ""))


# ---------------------------------------------------------------- baseline

MANUAL = "MANUAL — owner records after a real session"
KEEP_SECTIONS = ("## W0 smoke", "## Owner records", "## W5 decisions")


def file_stats(path):
    """(bytes, lines, est tokens) or None when the file is absent."""
    if not path or not os.path.isfile(path):
        return None
    with open(path, "rb") as fh:
        data = fh.read()
    text = data.decode("utf-8", errors="replace")
    lines = text.count("\n") + (0 if text.endswith("\n") or not text else 1)
    return len(data), lines, round(len(text) / 4)


def fmt_stats(stats):
    if stats is None:
        return "absent"
    b, lines, tok = stats
    return f"{b:,} B / {lines:,} lines / ~{tok:,} tok"


def description_chars(path):
    fields, _ = frontmatter_fields(path)
    return len(fields.get("description", "")) + len(fields.get("when_to_use", ""))


def listing(paths):
    entries = [(p, description_chars(p)) for p in paths]
    return len(entries), sum(n for _, n in entries), entries


def learn_hub_root(repo, given=None):
    """A validated learn-hub checkout (package.json name + scripts/apply-sync.mjs) or None."""
    candidates = [given, os.environ.get("LEARN_HUB_DIR"),
                  os.path.join(os.path.dirname(os.path.abspath(repo)), "learn-hub")]
    for cand in candidates:
        if not cand:
            continue
        try:
            with open(os.path.join(cand, "package.json"), encoding="utf-8") as fh:
                ok = json.load(fh).get("name") == "learn-hub"
        except (OSError, ValueError, AttributeError):
            continue
        if ok and os.path.isfile(os.path.join(cand, "scripts", "apply-sync.mjs")):
            return cand
    return None


def parse_tokens(text):
    """'~1.5k' -> 1500, '~280' -> 280."""
    m = re.fullmatch(r"~?([\d.,]+)(k?)", text.strip())
    if not m:
        return None
    value = float(m.group(1).replace(",", ""))
    return round(value * 1000) if m.group(2) else round(value)


def plugin_details(claude, plugin_dir):
    """{'always_on': int, 'components': [(name, always_on, on_invoke)]} or None.

    A skill and a command may share a name, so components is a list, not a dict."""
    name = os.path.basename(os.path.normpath(plugin_dir))
    manifest = os.path.join(plugin_dir, ".claude-plugin", "plugin.json")
    try:
        name = read_json(manifest).get("name") or name
    except (OSError, ValueError, AttributeError):
        pass
    cfg = tempfile.mkdtemp(prefix="rewrite-gate-cfg-")
    try:
        env = dict(os.environ, CLAUDE_CONFIG_DIR=cfg)
        res = subprocess.run([claude, "--plugin-dir", os.path.abspath(plugin_dir), "plugin", "details", name],
                             capture_output=True, text=True, encoding="utf-8", env=env, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    finally:
        shutil.rmtree(cfg, ignore_errors=True)
    if res.returncode != 0:
        return None
    return parse_details(res.stdout)


def parse_details(text):
    m = re.search(r"Always-on:\s*(~?[\d.,]+k?)\s*tok", text)
    if not m:
        return None
    comps = []
    in_table = False
    for line in text.split("\n"):
        if re.match(r"^\s*component\s+always-on\s+on-invoke", line):
            in_table = True
            continue
        if in_table:
            cols = line.split()
            if len(cols) == 3 and parse_tokens(cols[1]) is not None:
                comps.append((cols[0], parse_tokens(cols[1]), parse_tokens(cols[2])))
            elif line.strip():
                in_table = False
    return {"always_on": parse_tokens(m.group(1)), "components": comps}


def measure(repo, wave="W0", plugin_dirs=None, learn_hub=None, claude="auto",
            synced_dir=None, date=None):
    """Return the markdown section for one wave. claude=None forces the MANUAL path."""
    date = date or today()
    if claude == "auto":
        claude = shutil.which("claude")
    lh = learn_hub_root(repo, learn_hub)
    rows = []

    mk_claude = file_stats(os.path.join(repo, "CLAUDE.md"))
    mk_memory = file_stats(os.path.join(repo, "MEMORY.md"))
    routing = file_stats(os.path.join(repo, "ROUTING.md"))
    lh_claude = file_stats(os.path.join(lh, "CLAUDE.md")) if lh else None
    rows.append(("micky CLAUDE.md", fmt_stats(mk_claude), "wc -c; tokens = chars / 4"))
    rows.append(("learn-hub CLAUDE.md", fmt_stats(lh_claude) if lh else "n/a — learn-hub checkout not found",
                 f"{lh}/CLAUDE.md" if lh else "set LEARN_HUB_DIR or --learn-hub"))
    rows.append(("micky MEMORY.md", fmt_stats(mk_memory), "wc -c"))
    rows.append(("ROUTING.md", fmt_stats(routing), "wc -c"))

    mk_skills = sorted(glob.glob(os.path.join(repo, "plugins/*/skills/*/SKILL.md")))
    mk_cmds = sorted(glob.glob(os.path.join(repo, "plugins/*/commands/*.md")))
    mk_agents = sorted(glob.glob(os.path.join(repo, "plugins/*/agents/*.md")))
    n_mk, c_mk, mk_entries = listing(mk_skills + mk_cmds + mk_agents)
    rows.append(("micky authored listing entries",
                 f"{n_mk} entries ({len(mk_skills)} skills, {len(mk_cmds)} commands, {len(mk_agents)} agents) "
                 f"/ {c_mk:,} description chars",
                 "description + when_to_use, plugins/*/{skills,commands,agents}"))
    lh_listing = None
    if lh:
        lh_skills = sorted(glob.glob(os.path.join(lh, ".claude/skills/*/SKILL.md")))
        lh_listing = listing(lh_skills)
        rows.append(("learn-hub project-skill listing (loads in cloud)",
                     f"{lh_listing[0]} entries / {lh_listing[1]:,} description chars", ".claude/skills/*/SKILL.md"))
    else:
        rows.append(("learn-hub project-skill listing (loads in cloud)", "n/a — learn-hub checkout not found", ""))

    dirs = plugin_dirs or sorted(d for d in glob.glob(os.path.join(repo, "plugins", "*"))
                                 if os.path.isfile(os.path.join(d, ".claude-plugin", "plugin.json")))
    details = {}
    if claude:
        for d in dirs:
            details[os.path.basename(os.path.normpath(d))] = plugin_details(claude, d)
    measured = {k: v for k, v in details.items() if v}
    if claude and measured and len(measured) == len(dirs):
        total_on = sum(v["always_on"] for v in measured.values())
        rows.append(("micky always-on (plugin details sum)", f"~{total_on:,} tok over {len(dirs)} plugins",
                     "claude --plugin-dir <p> plugin details <p>, isolated CLAUDE_CONFIG_DIR"))
    else:
        missing = sorted(set(os.path.basename(os.path.normpath(d)) for d in dirs) - set(measured))
        why = "claude CLI not found" if not claude else f"plugin details failed for {', '.join(missing)}"
        rows.append(("micky always-on (plugin details sum)", f"{MANUAL} ({why})", "claude plugin details"))

    synced_dir = synced_dir or os.path.join(os.path.expanduser("~"), ".claude", "skills", "synced")
    synced = sorted(glob.glob(os.path.join(synced_dir, "*", "*", "SKILL.md")))
    if synced:
        n_s, c_s, _ = listing(synced)
        rows.append(("claude.ai-synced listing", f"{n_s} entries / {c_s:,} description chars", synced_dir))
    else:
        rows.append(("claude.ai-synced listing", f"{MANUAL} (no {synced_dir} on this machine)", ""))

    parts = [("learn-hub CLAUDE.md", lh_claude[2] if lh_claude else None),
             ("micky CLAUDE.md", mk_claude[2] if mk_claude else 0),
             ("MEMORY.md", mk_memory[2] if mk_memory else 0),
             ("ROUTING.md", routing[2] if routing else 0),
             ("learn-hub listing", round(lh_listing[1] / 4) if lh_listing else None),
             ("synced listing", round(listing(synced)[1] / 4) if synced else None)]
    known = [(k, v) for k, v in parts if v is not None]
    unknown = [k for k, v in parts if v is None]
    total = sum(v for _, v in known)
    rows.append(("Total paid before work, multi-repo cloud (estimate)",
                 f"~{total:,} tok" + (f" (without {', '.join(unknown)})" if unknown else ""),
                 " + ".join(f"{k} {v:,}" for k, v in known)))

    over_cap = [(rel(repo, p), n) for p, n in mk_entries if n > 1024]
    near_cap = [(rel(repo, p), n) for p, n in mk_entries if 1000 <= n <= 1024]
    soft = [(rel(repo, p), n) for p, n in mk_entries if n > 600]
    rows.append(("micky descriptions over 1,024 chars",
                 ", ".join(f"{p} ({n})" for p, n in over_cap) or "none", "hard cap"))
    rows.append(("micky descriptions at 1,000-1,024 chars", f"{len(near_cap)}: " + ", ".join(
        f"{p.split('/')[-2] if p.endswith('SKILL.md') else p.split('/')[-1]} ({n})" for p, n in near_cap)
                 if near_cap else "none", ""))
    rows.append(("micky descriptions over 600 chars (soft cap)", f"{len(soft)} of {n_mk}", ""))
    rows.append(("/doctor listing cost and overflow", MANUAL, "checklist row f"))
    rows.append(("/skill-doctor", MANUAL, "Windows, W5"))

    out = [f"## {wave} — {date}", "",
           f"Written by `python3 scripts/rewrite_gate.py baseline measure --wave {wave} --write` "
           f"({repo_name(repo)}). Tokens = chars / 4 unless the source is `plugin details`. "
           "MANUAL cells need an interactive session; the owner fills them in.", "",
           "| Surface | Value | Source |", "|---|---|---|"]
    out += [f"| {a} | {b} | {c} |" for a, b, c in rows]

    out += ["", "Per plugin (`plugin details`):", "", "| Plugin | always-on | on-invoke per component |",
            "|---|---|---|"]
    for d in dirs:
        key = os.path.basename(os.path.normpath(d))
        info = details.get(key)
        if info:
            comps = ", ".join(f"{c} ~{on_inv:,}" for c, _, on_inv in sorted(info["components"])
                              if on_inv is not None)
            out.append(f"| {key} | ~{info['always_on']:,} | {comps or '—'} |")
        else:
            out.append(f"| {key} | {MANUAL} | — |")

    out += ["", "Named skills (body = SKILL.md after frontmatter; references = every file under "
            "`references/`):", "", "| Skill | body lines | body tok | references tok |", "|---|---|---|---|"]
    for skill in ("intent-lock", "pubmed-research-note", "firecrawl", "ml-concept-lab"):
        hits = [p for p in mk_skills if os.path.basename(os.path.dirname(p)) == skill]
        if not hits:
            out.append(f"| {skill} | absent | — | — |")
            continue
        with open(hits[0], encoding="utf-8") as fh:
            _, body = split_frontmatter(fh.read())
        ref_tok = 0
        for rp in glob.glob(os.path.join(os.path.dirname(hits[0]), "references", "**", "*"), recursive=True):
            if os.path.isfile(rp):
                ref_tok += file_stats(rp)[2]
        out.append(f"| {skill} | {body.count(chr(10)) + 1:,} | ~{round(len(body) / 4):,} | ~{ref_tok:,} |")
    return "\n".join(out) + "\n"


def baseline_measure(repo, wave="W0", plugin_dirs=None, learn_hub=None, write=False,
                     claude="auto", synced_dir=None, date=None):
    if not re.fullmatch(r"W\d", wave):
        raise UsageError("--wave must be W0..W9")
    section = measure(repo, wave, plugin_dirs, learn_hub, claude, synced_dir, date)
    path = os.path.join(repo, BASELINE)
    existing = ""
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            existing = fh.read()
    text = replace_section(existing, wave, section)
    if write:
        write_text(path, text)
    return {"ok": True, "wave": wave, "written": write, "section": section}


def replace_section(existing, wave, section):
    """Insert or replace the '## <wave> — <date>' section; every other section is kept."""
    if not existing.strip():
        existing = ("# Baseline measurements\n\nOne dated section per wave exit (spec S12, I17). "
                    "`baseline measure` rewrites only its own dated section.\n")
    head = re.compile(rf"^## {re.escape(wave)} — \d{{4}}-\d{{2}}-\d{{2}}$", re.M)
    m = head.search(existing)
    if not m:
        return existing.rstrip("\n") + "\n\n" + section
    nxt = re.compile(r"^## ", re.M).search(existing, m.end())
    end = nxt.start() if nxt else len(existing)
    tail = existing[end:]
    return existing[:m.start()] + section + ("\n" + tail if tail else "")


# ---------------------------------------------------------------- CLI

def build_parser():
    p = argparse.ArgumentParser(prog="rewrite_gate.py", description=__doc__.split("\n\n")[0])
    groups = p.add_subparsers(dest="group", required=True)

    def action(group, name, help_text):
        sp = group.add_parser(name, help=help_text)
        sp.add_argument("--repo", default=ROOT, help="repo root (default: this script's repo)")
        return sp

    r = groups.add_parser("ratchet", help="shrink-only list of known violations").add_subparsers(
        dest="action", required=True)
    s = action(r, "init", "create an empty ratchet.json")
    s.add_argument("--write", action="store_true")
    s = action(r, "seed", "list today's violations of a new check id")
    s.add_argument("--check", required=True)
    s.add_argument("--from", dest="source")
    s.add_argument("--new", action="store_true", help="assert this check id has no entries yet")
    s.add_argument("--write", action="store_true")
    s = action(r, "verify", "schema + shrink-only against a git ref")
    s.add_argument("--base", default="HEAD")
    s = action(r, "close", "delete a fixed entry")
    s.add_argument("--check", required=True)
    s.add_argument("--path", required=True)
    s.add_argument("--write", action="store_true")

    t = groups.add_parser("triggers", help="trigger-phrase lock").add_subparsers(dest="action", required=True)
    s = action(t, "extract", "add every scanned phrase to the lock")
    s.add_argument("--skill")
    s.add_argument("--write", action="store_true")
    action(t, "verify", "fail when a locked phrase no longer scans")
    s = action(t, "remove", "retire phrases (append-only ledger)")
    s.add_argument("--reason", required=True)
    s.add_argument("--skill", required=True)
    s.add_argument("--phrase")
    s.add_argument("--write", action="store_true")

    h = groups.add_parser("h-coverage", help="Appendix A checklist").add_subparsers(dest="action", required=True)
    s = action(h, "seed", "create h-coverage.md from architecture.md Appendix A")
    s.add_argument("--from", dest="source", required=True)
    s.add_argument("--write", action="store_true")
    s = action(h, "close", "close one row in its wave")
    s.add_argument("--id", dest="hid", required=True)
    s.add_argument("--wave", required=True)
    s.add_argument("--write", action="store_true")

    b = groups.add_parser("baseline", help="baseline.md measurements").add_subparsers(dest="action", required=True)
    s = action(b, "measure", "write the dated section for one wave")
    s.add_argument("--wave", default="W0")
    s.add_argument("--plugin-dir", action="append", dest="plugin_dirs")
    s.add_argument("--learn-hub")
    s.add_argument("--write", action="store_true")
    return p


def dispatch(args):
    g, a, repo = args.group, args.action, args.repo
    if g == "ratchet":
        if a == "init":
            return ratchet_init(repo, args.write)
        if a == "seed":
            return ratchet_seed(repo, args.check, args.source, args.new, args.write)
        if a == "verify":
            return ratchet_verify(repo, args.base)
        return ratchet_close(repo, args.check, args.path, args.write)
    if g == "triggers":
        if a == "extract":
            return triggers_extract(repo, args.skill, args.write)
        if a == "verify":
            return triggers_verify(repo)
        return triggers_remove(repo, args.reason, args.skill, args.phrase, args.write)
    if g == "h-coverage":
        if a == "seed":
            return h_coverage_seed(repo, args.source, args.write)
        return h_coverage_close(repo, args.hid, args.wave, args.write)
    res = baseline_measure(repo, args.wave, args.plugin_dirs, args.learn_hub, args.write)
    if args.write:
        res.pop("section")
    return res


def main(argv=None):
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code in (0, None) else 2
    try:
        result = dispatch(args)
    except UsageError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    except (Refused, OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=1))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=1))
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    sys.exit(main())
