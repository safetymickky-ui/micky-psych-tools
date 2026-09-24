#!/usr/bin/env python3
"""Check the delivery log and the plugins a session actually loaded (spec S11, interface I16).

    delivery_log.py check [--log PATH] [--setup PATH] [--strict] [--json]
    delivery_log.py current --env ID [--var NAME] [--log PATH]
    delivery_log.py live [--from FILE|-] [--env ID] [--expect auto|a,b,c]
                         [--project-roots A,B] [--strict] [--log PATH]

check    parses docs/rewrite/delivery-log.md and docs/rewrite/cloud-setup.sh against rules
         DL1-DL19. Exit 0 no errors (warnings allowed unless --strict, which turns every
         warning into an error), 1 rule errors, 2 usage error or unreadable log.
current  prints the latest logged value of one variable (default CLAUDE_CODE_PLUGIN_DIRS)
         for one environment. Exit 0 printed, 1 no row, 2 usage error.
live     reads `claude plugin list --json` (run here, or --from a file / stdin) and applies
         rules L1-L7. Exit 0 ok, 1 rule errors, 2 usage error, 3 claude not found or its
         output is not a JSON array.

Stdlib only; reads files, never writes. Defaults for --log and --setup are the files under
docs/rewrite/ of the repo that holds this script.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_LOG = os.path.join(ROOT, "docs", "rewrite", "delivery-log.md")
DEFAULT_SETUP = os.path.join(ROOT, "docs", "rewrite", "cloud-setup.sh")

LOG_HEADER = ["#", "date", "environment", "variable", "previous", "new", "reason", "evidence", "rollback"]
CHECK_HEADER = ["check", "question", "answer", "evidence", "date", "fallback taken"]
SECTIONS = ("## Environments", "## W0 mechanism checklist", "## Log")
ENV_RE = re.compile(r"^(cloud|windows):[A-Za-z0-9._-]+$")
PATH_VARS = ("LEARN_HUB_DIR", "MICKY_TOOLS_DIR", "BOOK_ROOT", "ARTICLE_INBOX_DIR", "PUPPETEER_EXECUTABLE_PATH")
PLAIN_VARS = ("CLAUDE_CODE_PLUGIN_DIRS",) + PATH_VARS + (
    "PUPPETEER_SKIP_DOWNLOAD", "FIRECRAWL_API_KEY", "setup-script", "network-access")
PREFIX_VARS = (re.compile(r"^marketplace:[A-Za-z0-9._-]+$"), re.compile(r"^installs:[A-Za-z0-9._-]+$"),
               re.compile(r"^enabled:[A-Za-z0-9._-]+@[A-Za-z0-9._-]+$"))
SECRET_RES = [re.compile(p) for p in (r"fc-[A-Za-z0-9]{8,}", r"sk-[A-Za-z0-9]{8,}",
                                      r"eyJ[A-Za-z0-9_-]{10,}", r"service_role")]
REASON_RE = re.compile(r"^(W[0-5]|probe|fix|rollback of #\d+)")
CODE_RE = re.compile(r"^`([^`]*)`$")
TILDE_MSG = "~ resolves to /root in cloud (probe P1)"
RELATIVE_MSG = "Claude Code skips a relative path with no error line (N1)"


class Findings:
    def __init__(self):
        self.errors, self.warnings = [], []

    def error(self, rule, message, row=None):
        self.errors.append({"rule": rule, "row": row, "message": message})

    def warn(self, rule, message, row=None):
        self.warnings.append({"rule": rule, "row": row, "message": message})


# ------------------------------------------------------------------ parsing

def split_row(line):
    """Cells of a markdown table row; an escaped \\| stays inside its cell."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", body)]


def section_lines(lines, heading):
    """Lines after `heading` up to the next '## ' heading."""
    out, inside = [], False
    for line in lines:
        if line.strip() == heading:
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside:
            out.append(line)
    return out


def table(lines):
    """(header cells, [row cells]) of the first table in lines, or (None, [])."""
    rows, header, seen_sep = [], None, False
    for line in lines:
        if not line.strip().startswith("|"):
            if header is not None:
                break
            continue
        cells = split_row(line)
        if header is None:
            header = cells
        elif not seen_sep and all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
            seen_sep = True
        else:
            rows.append(cells)
    return header, rows


def unticked(cell):
    return cell[1:-1] if len(cell) >= 2 and cell.startswith("`") and cell.endswith("`") else cell


def code_value(cell):
    m = CODE_RE.match(cell)
    return m.group(1) if m else None


def env_kind(env):
    return env.split(":", 1)[0]


def parse_log(text):
    lines = text.replace("\r\n", "\n").split("\n")
    _, env_rows = table(section_lines(lines, "## Environments"))
    envs = [unticked(r[0]) for r in env_rows if r]
    check_header, check_rows = table(section_lines(lines, "## W0 mechanism checklist"))
    log_header, log_rows = table(section_lines(lines, "## Log"))
    return {"lines": lines, "envs": envs, "env_rows": env_rows, "check_header": check_header,
            "check_rows": check_rows, "log_header": log_header, "log_rows": log_rows}


def latest_values(log_rows):
    """{env: {variable: new value}} from well-formed rows, last row wins."""
    cur = {}
    for r in log_rows:
        if len(r) != 9:
            continue
        env, var, new = unticked(r[2]), unticked(r[3]), code_value(r[5])
        if new is not None:
            cur.setdefault(env, {})[var] = new
    return cur


# ------------------------------------------------------------------ value rules

def dirs_problems(value, kind):
    """DL8 messages for one CLAUDE_CODE_PLUGIN_DIRS value of an environment kind."""
    probs = []
    if kind == "cloud":
        if ";" in value:
            probs.append("cloud value must not contain ';' (cloud separates with ':')")
        if "\\" in value:
            probs.append("cloud value must not contain a backslash")
        sep = ":"
    else:
        sep = ";"
    if value.endswith(sep):
        probs.append(f"trailing '{sep}' separator")
    segments = value.split(sep)
    seen = set()
    for seg in segments:
        if seg == "":
            probs.append("empty segment")
            continue
        if seg != seg.strip():
            probs.append(f"segment {seg!r} has surrounding spaces")
        s = seg.strip()
        if s.startswith("~"):
            probs.append(f"segment {s!r}: {TILDE_MSG}")
        elif kind == "cloud" and not s.startswith("/"):
            probs.append(f"segment {s!r}: {RELATIVE_MSG}")
        elif kind == "windows":
            if not re.match(r"^[A-Za-z]:\\", s):
                if re.match(r"^[A-Za-z]:", s) or s.startswith(("\\", "/")):
                    probs.append(f"segment {s!r} must start with a drive, like C:\\")
                else:
                    probs.append(f"segment {s!r}: {RELATIVE_MSG}")
            elif ":" in s[2:]:
                probs.append(f"segment {s!r} has ':' after the drive (Windows separates with ';')")
        if ".." in re.split(r"[\\/]", s):
            probs.append(f"segment {s!r} contains '..'")
        if s in seen:
            probs.append(f"segment {s!r} listed twice")
        seen.add(s)
    return probs


def is_abs_path(value, kind):
    if kind == "cloud":
        return value.startswith("/") and ":" not in value
    return bool(re.match(r"^[A-Za-z]:\\", value)) and ";" not in value


def value_problem(var, value, kind, first_of_pair):
    """DL6/DL8/DL9/DL10 problem for one previous/new value, as (rule, message) or None."""
    if var == "CLAUDE_CODE_PLUGIN_DIRS":
        if value == "(unset)":
            return None
        if value == "(unrecorded)":
            return None if first_of_pair else ("DL6", "(unrecorded) is allowed only in the first row of a pair")
        probs = dirs_problems(value, kind)
        return ("DL8", "; ".join(probs)) if probs else None
    if var in PATH_VARS:
        if value in ("(unset)", "(unrecorded)") or is_abs_path(value, kind):
            return None
        return ("DL9", f"{var} must be (unset) or one absolute {kind} path, got {value!r}")
    if var == "PUPPETEER_SKIP_DOWNLOAD":
        return None if value in ("(unset)", "1") else ("DL6", "PUPPETEER_SKIP_DOWNLOAD is (unset) or 1")
    if var == "FIRECRAWL_API_KEY":
        return None if value in ("(set)", "(unset)") else (
            "DL10", "FIRECRAWL_API_KEY is logged only as (set) or (unset), never the key")
    if var == "setup-script":
        return None if value in ("(none)", "(unrecorded)") or re.fullmatch(r"setup_version=\d+", value) else (
            "DL6", "setup-script is (none), (unrecorded) or setup_version=<n>")
    if var == "network-access":
        return None if value in ("none", "trusted", "full", "custom") else (
            "DL6", "network-access is none, trusted, full or custom")
    if var.startswith("marketplace:"):
        ok = value == "(absent)" or re.match(r"^(directory:.+|github:[^/\s]+/[^/\s]+|git:\S+)$", value)
        return None if ok else ("DL6", "marketplace value is (absent), directory:<path>, github:<o>/<r> or git:<url>")
    if var.startswith("installs:"):
        ok = value == "(none)" or re.fullmatch(r"[A-Za-z0-9._-]+(,[A-Za-z0-9._-]+)*", value)
        return None if ok else ("DL6", "installs value is (none) or comma-separated plugin names")
    if var.startswith("enabled:"):
        return None if value in ("(unset)", "true", "false") else ("DL6", "enabled value is (unset), true or false")
    return None


# ------------------------------------------------------------------ expansion

def plugin_name(dirpath):
    try:
        with open(os.path.join(dirpath, ".claude-plugin", "plugin.json"), encoding="utf-8") as fh:
            name = json.load(fh).get("name")
    except (OSError, ValueError, AttributeError):
        return None
    return name if isinstance(name, str) else os.path.basename(os.path.normpath(dirpath))


def expand_segment(seg):
    """Plugin names one CLAUDE_CODE_PLUGIN_DIRS segment loads."""
    if os.path.isfile(os.path.join(seg, ".claude-plugin", "plugin.json")):
        return [plugin_name(seg)]
    names = []
    for child in sorted(os.listdir(seg)):
        path = os.path.join(seg, child)
        if os.path.isdir(path) and os.path.isfile(os.path.join(path, ".claude-plugin", "plugin.json")):
            names.append(plugin_name(path))
    return names


def expand(value, sep):
    """(names, absent segments) for a path-list value."""
    segs = [s for s in value.split(sep) if s]
    absent = [s for s in segs if not os.path.isdir(s)]
    if absent:
        return None, absent
    names = []
    for s in segs:
        names += expand_segment(s)
    return names, []


def this_kind():
    return "windows" if os.name == "nt" else "cloud"


# ------------------------------------------------------------------ check

def check(log_text, setup_path, strict=False, bash=None):
    f = Findings()
    doc = parse_log(log_text)
    lines = doc["lines"]

    for heading in SECTIONS:  # DL1
        n = sum(1 for line in lines if line.strip() == heading)
        if n != 1:
            f.error("DL1", f"section '{heading}' appears {n} times; it must appear exactly once")

    for env in doc["envs"]:  # DL4 placeholders
        if "<" in env:
            f.warn("DL4", f"environment id {env!r} in ## Environments: placeholder not filled")

    for i, cells in enumerate(doc["env_rows"] + doc["check_rows"] + doc["log_rows"]):  # DL10 anywhere
        for cell in cells:
            for rx in SECRET_RES:
                if rx.search(cell):
                    f.error("DL10", f"a table cell matches the secret pattern {rx.pattern}; never log a key")

    # DL14 checklist
    if doc["check_header"] is not None and doc["check_header"] != CHECK_HEADER:
        f.error("DL14", "the checklist header must be | " + " | ".join(CHECK_HEADER) + " |")
    checklist = {}
    for cells in doc["check_rows"]:
        if len(cells) != 6:
            f.error("DL14", f"checklist row {cells[:1]} needs 6 cells, has {len(cells)}")
            continue
        key, _q, answer, evidence, _date, fallback = cells
        if key in checklist:
            f.error("DL14", f"checklist row {key} appears twice")
        checklist[key] = answer
        if answer not in ("pending", "yes", "no"):
            f.error("DL14", f"checklist row {key}: answer must be pending, yes or no, got {answer!r}")
        elif answer == "pending":
            f.warn("DL14", f"checklist row {key} is pending")
        else:
            if not evidence:
                f.error("DL14", f"checklist row {key}: a {answer} answer needs evidence")
            if answer == "no" and not fallback:
                f.error("DL14", f"checklist row {key}: a no answer needs 'fallback taken'")
    for key in "abcdefgh":
        if key not in checklist:
            f.error("DL14", f"checklist row {key} is missing")

    # Log rows
    if doc["log_header"] != LOG_HEADER:
        f.error("DL2", "the Log header must be | " + " | ".join(LOG_HEADER) + " |")
    last = {}
    prev_date = None
    for idx, cells in enumerate(doc["log_rows"], start=1):
        if len(cells) != 9:
            f.error("DL2", f"row has {len(cells)} cells, needs 9", idx)
            continue
        num, date, env, var, previous, new, reason, evidence, rollback = cells
        env, var = unticked(env), unticked(var)
        if num != str(idx):
            f.error("DL3", f"# is {num!r}, expected {idx} (no gaps)", idx)
        try:
            d = datetime.date.fromisoformat(date)
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
                raise ValueError
            if prev_date and d < prev_date:
                f.error("DL3", f"date {date} is earlier than the row before", idx)
            prev_date = d
        except ValueError:
            f.error("DL3", f"date {date!r} is not YYYY-MM-DD", idx)
        if not ENV_RE.match(env):
            f.error("DL4", f"environment {env!r} must match cloud:<id> or windows:<id>", idx)
        elif env not in doc["envs"]:
            f.error("DL4", f"environment {env!r} is not listed in ## Environments", idx)
        if not (var in PLAIN_VARS or any(rx.match(var) for rx in PREFIX_VARS)):
            f.error("DL5", f"variable {var!r} is not one the log tracks", idx)
        kind = env_kind(env)
        first = (env, var) not in last
        vals = {}
        for label, cell in (("previous", previous), ("new", new)):
            v = code_value(cell)
            if v is None:
                f.error("DL6", f"{label} must be one code span, like `(unset)`", idx)
                continue
            vals[label] = v
            prob = value_problem(var, v, kind, first)
            if prob:
                f.error(prob[0], f"{label}: {prob[1]}", idx)
        if "previous" in vals and not first and vals["previous"] != last[(env, var)]:
            f.error("DL7", f"previous {vals['previous']!r} != new {last[(env, var)]!r} of the last "
                           f"{env} {var} row", idx)
        if "new" in vals:
            last[(env, var)] = vals["new"]
        if not REASON_RE.match(reason):
            f.error("DL11", "reason must start with W0..W5, probe, fix or 'rollback of #N'", idx)
        if not evidence:
            f.error("DL12", "evidence is empty", idx)
        elif evidence.strip().lower() == "pending":
            f.warn("DL12", "evidence is pending", idx)
        if not rollback:
            f.error("DL13", "rollback is empty", idx)

    current = latest_values(doc["log_rows"])

    # DL15: expand the latest value of each environment of this machine's kind
    for env, variables in sorted(current.items()):
        value = variables.get("CLAUDE_CODE_PLUGIN_DIRS")
        if value in (None, "(unset)", "(unrecorded)") or env_kind(env) != this_kind():
            continue
        names, absent = expand(value, ":" if env_kind(env) == "cloud" else ";")
        if names is None:
            for seg in absent:
                f.warn("DL15", f"{env}: segment {seg} not found here; not expanded here")
            continue
        dupes = sorted({n for n in names if names.count(n) > 1})
        for n in dupes:
            f.error("DL15", f"{env}: plugin {n} is reached twice by CLAUDE_CODE_PLUGIN_DIRS")

    # Setup file: DL16-DL18
    setup_text = None
    if not os.path.isfile(setup_path):
        f.error("DL16", f"setup file {setup_path} not found")
    else:
        with open(setup_path, encoding="utf-8") as fh:
            setup_text = fh.read()
        bash = bash if bash is not None else shutil.which("bash")
        if not bash:
            f.warn("DL16", "bash is not on PATH; bash -n was not run")
        else:
            res = subprocess.run([bash, "-n", setup_path], capture_output=True, text=True)
            if res.returncode != 0:
                f.error("DL16", "bash -n failed: " + " ".join(res.stderr.split())[:200])
        versions = re.findall(r"(?m)^SETUP_VERSION=(\S*)$", setup_text)
        if len(versions) != 1 or not re.fullmatch(r"\d+", versions[0]):
            f.error("DL17", "the setup file needs exactly one SETUP_VERSION=<integer> line")
        else:
            for env, variables in sorted(current.items()):
                v = variables.get("setup-script", "")
                m = re.fullmatch(r"setup_version=(\d+)", v)
                if env_kind(env) == "cloud" and m and m.group(1) != versions[0]:
                    f.error("DL17", f"SETUP_VERSION={versions[0]} but {env} logs setup_version={m.group(1)}")
        for repo_path in ("/home/user/learn-hub", "/home/user/micky-psych-tools"):
            if repo_path in setup_text:
                f.error("DL18", f"the setup file names {repo_path}; it may run before the clone")
        for rx in SECRET_RES:
            if rx.search(setup_text):
                f.error("DL18", f"the setup file matches the secret pattern {rx.pattern}")
        nonempty = [line for line in setup_text.split("\n") if line.strip()]
        if not nonempty or nonempty[-1].strip() != "exit 0":
            f.error("DL18", "the last non-empty line of the setup file must be 'exit 0'")

    # DL19 (strict only), once the checklist is answered
    if strict and checklist and all(v in ("yes", "no") for v in checklist.values()):
        for env, variables in sorted(current.items()):
            if env_kind(env) == "cloud" and any("/opt/w0-probe" in v for v in variables.values()):
                f.error("DL19", f"{env} still carries /opt/w0-probe; remove the probe (S11-W0-11)")
        if setup_text is not None and "w0-probe" in setup_text:
            f.error("DL19", "the setup file still holds the w0-probe block; ship version 2")

    if strict:
        f.errors += f.warnings
        f.warnings = []
    return {"ok": not f.errors, "rows": len(doc["log_rows"]), "errors": f.errors,
            "warnings": f.warnings, "checklist": {k: checklist.get(k, "missing") for k in "abcdefgh"},
            "current": current}


# ------------------------------------------------------------------ live

def skill_names(install_path):
    d = os.path.join(install_path or "", "skills")
    if not os.path.isdir(d):
        return []
    return sorted(n for n in os.listdir(d) if os.path.isfile(os.path.join(d, n, "SKILL.md")))


def live(entries, environ, log_text=None, env=None, expect=None, project_roots=None,
         strict=False, synced_dir=None):
    f = Findings()
    dirs = environ.get("CLAUDE_CODE_PLUGIN_DIRS", "")
    names = {}
    disabled, loaded = [], []
    for e in entries:
        pid = str(e.get("id", ""))
        name = pid.split("@", 1)[0]
        names.setdefault(name, []).append(e)
        if e.get("errors") or e.get("errorDetails"):  # L1
            f.error("L1", f"{pid}: {e.get('errors') or e.get('errorDetails')}")
            continue
        if e.get("enabled") is False:
            disabled.append(pid)
        else:
            loaded.append(name)
    dupes = sorted(n for n, es in names.items() if len(es) > 1)
    for n in dupes:  # L2
        paths = ", ".join(str(x.get("installPath")) for x in names[n])
        f.error("L2", f"plugin {n} is loaded {len(names[n])} times: {paths}")

    if env is not None:  # L3
        if log_text is None:
            f.error("L3", "no delivery log to compare with")
        else:
            logged = latest_values(parse_log(log_text)["log_rows"]).get(env, {}).get("CLAUDE_CODE_PLUGIN_DIRS")
            if (logged or "(unset)") != (dirs or "(unset)"):
                msg = f"$CLAUDE_CODE_PLUGIN_DIRS is {dirs or '(unset)'!r}; the log says {logged!r} for {env}"
                (f.error if strict else f.warn)("L3", msg)

    segs = [os.path.normcase(os.path.normpath(s)) for s in dirs.split(os.pathsep) if s]
    for e in entries:  # L4
        pid = str(e.get("id", ""))
        if not pid.endswith("@inline") or e.get("errors"):
            continue
        ip = os.path.normcase(os.path.normpath(str(e.get("installPath", ""))))
        if not any(ip == s or ip.startswith(s.rstrip(os.sep) + os.sep) for s in segs):
            f.error("L4", f"{pid}: installPath {e.get('installPath')} is under no CLAUDE_CODE_PLUGIN_DIRS segment")

    expected = None
    if expect:  # L5
        if expect == "auto":
            got, absent = expand(dirs, os.pathsep) if dirs else ([], [])
            if got is None:
                f.error("L5", "cannot expand CLAUDE_CODE_PLUGIN_DIRS here; missing: " + ", ".join(absent))
                got = []
            expected = sorted(set(got))
        else:
            expected = sorted({x.strip() for x in expect.split(",") if x.strip()})
        have = set(loaded)
        disabled_names = {d.split("@", 1)[0] for d in disabled}
        for n in expected:
            if n in have:
                continue
            if n in disabled_names:
                f.error("L5", f"{n}: present but disabled (defaultEnabled:false or a user setting)")
            else:
                f.error("L5", f"{n}: expected but not loaded")
        for n in sorted(have - set(expected)):
            f.error("L5", f"{n}: loaded but not expected")

    roots = project_roots
    if roots is None:
        roots = [r for r in (environ.get("LEARN_HUB_DIR"), environ.get("MICKY_TOOLS_DIR")) if r]
    project = {}
    for r in roots:
        d = os.path.join(r, ".claude", "skills")
        if os.path.isdir(d):
            for n in os.listdir(d):
                if os.path.isdir(os.path.join(d, n)):
                    project.setdefault(n, r)
    synced_dir = synced_dir or os.path.join(os.path.expanduser("~"), ".claude", "skills", "synced")
    synced = set()
    if os.path.isdir(synced_dir):
        for sid in os.listdir(synced_dir):
            sub = os.path.join(synced_dir, sid)
            if os.path.isdir(sub):
                synced.update(n for n in os.listdir(sub) if os.path.isdir(os.path.join(sub, n)))
    for e in entries:
        if e.get("errors"):
            continue
        for s in skill_names(e.get("installPath")):
            if s in project:  # L6
                f.error("L6", f"{e.get('id')}: skill {s} collides with project skill "
                              f"{os.path.join(project[s], '.claude', 'skills', s)}")
            if s in synced:  # L7
                f.warn("L7", f"{e.get('id')}: skill {s} shares its name with a claude.ai-synced skill")

    return {"ok": not f.errors, "entries": len(entries), "loaded": sorted(set(loaded)),
            "expected": expected, "duplicates": dupes, "disabled": sorted(disabled),
            "errors": [{"rule": x["rule"], "message": x["message"]} for x in f.errors],
            "warnings": [{"rule": x["rule"], "message": x["message"]} for x in f.warnings]}


# ------------------------------------------------------------------ CLI

def build_parser():
    p = argparse.ArgumentParser(prog="delivery_log.py", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="check the delivery log and the setup script (DL1-DL19)")
    c.add_argument("--log", default=DEFAULT_LOG)
    c.add_argument("--setup", default=DEFAULT_SETUP)
    c.add_argument("--strict", action="store_true", help="every warning becomes an error")
    c.add_argument("--json", action="store_true")
    q = sub.add_parser("current", help="print the latest logged value of one variable")
    q.add_argument("--env", required=True)
    q.add_argument("--var", default="CLAUDE_CODE_PLUGIN_DIRS")
    q.add_argument("--log", default=DEFAULT_LOG)
    v = sub.add_parser("live", help="check `claude plugin list --json` (L1-L7)")
    v.add_argument("--from", dest="source", help="a JSON file, or - for stdin")
    v.add_argument("--env")
    v.add_argument("--expect", help="auto, or comma-separated plugin names")
    v.add_argument("--project-roots", help="comma-separated roots holding .claude/skills")
    v.add_argument("--strict", action="store_true")
    v.add_argument("--log", default=DEFAULT_LOG)
    return p


def read_text(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main(argv=None, environ=None, out=None):
    out = out if out is not None else sys.stdout
    environ = dict(os.environ) if environ is None else environ
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code in (0, None) else 2

    if args.cmd == "check":
        try:
            text = read_text(args.log)
        except OSError as exc:
            print(f"delivery_log: cannot read {args.log}: {exc}", file=sys.stderr)
            return 2
        res = check(text, args.setup, strict=args.strict)
        if args.json:
            out.write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
        else:
            for x in res["errors"]:
                out.write(f"ERROR {x['rule']}" + (f" row {x['row']}" if x["row"] else "") + f": {x['message']}\n")
            for x in res["warnings"]:
                out.write(f"WARN  {x['rule']}" + (f" row {x['row']}" if x["row"] else "") + f": {x['message']}\n")
            state = " ".join(f"{k}={v}" for k, v in res["checklist"].items())
            out.write(f"delivery log: {res['rows']} row(s), {len(res['errors'])} error(s), "
                      f"{len(res['warnings'])} warning(s); checklist {state}\n")
        return 0 if res["ok"] else 1

    if args.cmd == "current":
        try:
            text = read_text(args.log)
        except OSError as exc:
            print(f"delivery_log: cannot read {args.log}: {exc}", file=sys.stderr)
            return 2
        value = latest_values(parse_log(text)["log_rows"]).get(args.env, {}).get(args.var)
        if value is None:
            print(f"delivery_log: no {args.var} row for {args.env}", file=sys.stderr)
            return 1
        out.write(value + "\n")
        return 0

    # live
    if args.source:
        try:
            raw = sys.stdin.read() if args.source == "-" else read_text(args.source)
        except OSError as exc:
            print(f"delivery_log: cannot read {args.source}: {exc}", file=sys.stderr)
            return 2
    else:
        claude = shutil.which("claude")
        if not claude:
            print("delivery_log: claude not found on PATH", file=sys.stderr)
            return 3
        res = subprocess.run([claude, "plugin", "list", "--json"], capture_output=True, text=True)
        raw = res.stdout
    try:
        entries = json.loads(raw)
    except ValueError:
        entries = None
    if not isinstance(entries, list):
        print("delivery_log: `claude plugin list --json` output is not a JSON array", file=sys.stderr)
        return 3
    log_text = None
    if args.env:
        try:
            log_text = read_text(args.log)
        except OSError:
            log_text = None
    roots = [r for r in args.project_roots.split(",") if r] if args.project_roots else None
    res = live(entries, environ, log_text, args.env, args.expect, roots, args.strict)
    out.write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
