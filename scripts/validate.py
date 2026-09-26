#!/usr/bin/env python3
"""Validate the marketplace catalog and every plugin it lists.

What it checks, per run:
  - marketplace.json loads, has a kebab-case name, owner.name and a non-empty plugins[];
  - per entry: relative `source`, the directory exists, plugin.json loads, its name
    matches the entry and is kebab-case, its version is semver, declared component
    paths exist, a declared mcpServers file loads and every server is either http/sse
    (`type` + `url`) or stdio (`command`);
  - per skill: SKILL.md exists, its frontmatter parses as strict YAML (CRLF-safe),
    `name` matches the directory, description <= 1,024 chars (a description under 200
    chars is a WARN, never a failure), and a legacy evals/evals.json is valid JSON;
  - per command/agent: frontmatter parses and carries a description (agents <= 1,024);
  - per plugin: no file named SKILL.md (any case) outside skills/<skill>/, because some
    surfaces load every SKILL.md they find as a skill.

Every result is counted: a missing or malformed file is a FAIL line, never a
traceback. A YAML failure on a file listed in docs/rewrite/ratchet.json under
check_id "yaml-parse" prints WARN instead of FAIL (known, ratcheted violation).

It does NOT run `claude plugin validate --strict`; scripts/health.sh does both.

    python3 scripts/validate.py
"""
import json
import os
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only on a machine without PyYAML
    yaml = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEBAB = r"[a-z0-9]+(-[a-z0-9]+)*"
DESC_CAP = 1024
DESC_WARN_BELOW = 200
FM_RE = re.compile(r"^---\n(.*?)\n---[ \t]*(?:\n|$)", re.S)


class Report:
    """Collects PASS / FAIL / WARN lines. Every check goes through check() or warn()."""

    def __init__(self, out=None):
        self.out = out if out is not None else sys.stdout
        self.failures = []
        self.warnings = []

    def say(self, line=""):
        self.out.write(line + "\n")

    def check(self, condition, message):
        self.say(("  PASS  " if condition else "  FAIL  ") + message)
        if not condition:
            self.failures.append(message)
        return bool(condition)

    def warn(self, message):
        self.say("  WARN  " + message)
        self.warnings.append(message)


def yaml_error_text(exc):
    """One-line YAML error: the problem plus its position inside the frontmatter block."""
    problem = getattr(exc, "problem", None)
    mark = getattr(exc, "problem_mark", None)
    if problem and mark is not None:
        # mark.line is 0-based within the block, and the block starts on file line 2
        return f"{problem} (file line {mark.line + 2}, column {mark.column + 1})"
    return " ".join(str(exc).split())


def frontmatter(path):
    """Return the frontmatter of a markdown file.

    dict                       -> parsed YAML mapping
    None                       -> no frontmatter block
    ("yaml-error", message)    -> the block is not valid YAML (or not a mapping)
    CRLF line endings are normalised before parsing.
    """
    with open(path, encoding="utf-8") as fh:
        text = fh.read().replace("\r\n", "\n")
    match = FM_RE.match(text)
    if not match:
        return None
    if yaml is None:
        return ("yaml-error", "PyYAML is not installed (python3 -m pip install pyyaml)")
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return ("yaml-error", yaml_error_text(exc))
    if data is None:
        return {}
    if not isinstance(data, dict):
        return ("yaml-error", f"frontmatter is a {type(data).__name__}, not a mapping")
    return data


def load_json(report, path, label):
    """Load a JSON file; a missing or malformed file is a counted FAIL, returns None."""
    if not report.check(os.path.isfile(path), f"{label} exists"):
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        report.check(False, f"{label} is valid JSON ({' '.join(str(exc).split())})")
        return None
    return data


def load_ratchet(report, root):
    """Ratcheted (known) violations: {(check_id, path)}. Absent file = none listed."""
    path = os.path.join(root, "docs", "rewrite", "ratchet.json")
    if not os.path.isfile(path):
        return set()
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        entries = data.get("entries", []) if isinstance(data, dict) else None
        if not isinstance(entries, list):
            raise ValueError("'entries' is not a list")
        return {(e.get("check_id"), e.get("path")) for e in entries if isinstance(e, dict)}
    except (OSError, ValueError) as exc:
        report.check(False, f"docs/rewrite/ratchet.json is readable ({' '.join(str(exc).split())})")
        return set()


def rel(root, path):
    return os.path.relpath(path, root).replace(os.sep, "/")


def parsed_frontmatter(report, root, ratchet, path):
    """Frontmatter as a dict, or None after reporting why (FAIL, or WARN if ratcheted)."""
    fm = frontmatter(path)
    rpath = rel(root, path)
    if fm is None:
        report.check(False, f"{rpath}: frontmatter block present")
        return None
    if isinstance(fm, tuple):
        message = f"{rpath}: yaml-error: {fm[1]}"
        if ("yaml-parse", rpath) in ratchet:
            report.warn(message + " (ratcheted: yaml-parse)")
        else:
            report.check(False, message)
        return None
    report.check(True, f"{rpath}: frontmatter parses")
    return fm


def check_mcp(report, pdir, ref):
    mcp = load_json(report, os.path.join(pdir, ref), f"declared mcpServers file {ref}")
    if mcp is None:
        return
    servers = mcp.get("mcpServers", {}) if isinstance(mcp, dict) else None
    if not report.check(isinstance(servers, dict), f"{ref}: mcpServers is an object"):
        return
    for sname, spec in sorted(servers.items()):
        ok = isinstance(spec, dict) and (
            ("url" in spec and "type" in spec) or "command" in spec)
        report.check(ok, f"{ref}: server {sname} is http/sse (type + url) or stdio (command)")


def check_skills(report, root, ratchet, pdir):
    skills_dir = os.path.join(pdir, "skills")
    if not os.path.isdir(skills_dir):
        return
    for skill in sorted(os.listdir(skills_dir)):
        sdir = os.path.join(skills_dir, skill)
        if not os.path.isdir(sdir):
            continue
        sp = os.path.join(sdir, "SKILL.md")
        if not report.check(os.path.isfile(sp), f"skills/{skill}/SKILL.md exists"):
            continue
        fm = parsed_frontmatter(report, root, ratchet, sp)
        if fm is None:
            continue
        report.check(fm.get("name") == skill, f"skills/{skill}: frontmatter name matches directory")
        desc = fm.get("description")
        desc = desc if isinstance(desc, str) else ""
        n = len(desc)
        report.check(n <= DESC_CAP, f"skills/{skill}: description {n} chars (hard cap {DESC_CAP})")
        if n < DESC_WARN_BELOW:
            report.warn(f"skills/{skill}: description {n} chars is short; under ~{DESC_WARN_BELOW} "
                        "chars triggers unreliably")
        ev = os.path.join(sdir, "evals", "evals.json")
        if os.path.isfile(ev):
            load_json(report, ev, f"skills/{skill}/evals/evals.json")


def check_skill_md_placement(report, root, pdir):
    """SKILL.md is a reserved name: only skills/<skill>/SKILL.md may carry it. Some surfaces
    load every SKILL.md they find, so a nested one (a template, an example) becomes a
    stray skill. Matched case-insensitively: on Windows, skill.md opens as SKILL.md."""
    stray = []
    for dirpath, dirnames, filenames in os.walk(pdir):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
        for fname in filenames:
            if fname.lower() != "skill.md":
                continue
            path = os.path.join(dirpath, fname)
            parts = os.path.relpath(path, pdir).split(os.sep)
            if not (len(parts) == 3 and parts[0] == "skills"):
                stray.append(rel(root, path))
    for path in sorted(stray):
        report.check(False, f"{path}: only skills/<skill>/SKILL.md may be named SKILL.md "
                            "(some surfaces load it as a skill); rename it, e.g. SKILL.template.md")
    if not stray:
        report.check(True, "no SKILL.md outside skills/<skill>/")


def check_components(report, root, ratchet, pdir):
    for comp in ("commands", "agents"):
        cdir = os.path.join(pdir, comp)
        if not os.path.isdir(cdir):
            continue
        for fname in sorted(os.listdir(cdir)):
            if not fname.endswith(".md"):
                continue
            fm = parsed_frontmatter(report, root, ratchet, os.path.join(cdir, fname))
            if fm is None:
                continue
            desc = fm.get("description")
            desc = desc if isinstance(desc, str) else ""
            report.check(bool(desc), f"{comp}/{fname}: frontmatter description present")
            if comp == "agents":
                report.check(len(desc) <= DESC_CAP,
                             f"agents/{fname}: description {len(desc)} chars (hard cap {DESC_CAP})")


def check_plugin(report, root, ratchet, entry):
    name = entry.get("name", "<unnamed>") if isinstance(entry, dict) else "<not an object>"
    report.say(f"\nplugin: {name}")
    if not report.check(isinstance(entry, dict), "catalog entry is an object"):
        return
    # source must resolve. relative paths only work for git/local marketplaces,
    # never for a marketplace distributed as a bare URL.
    src = entry.get("source", "")
    if not report.check(isinstance(src, str) and src.startswith("./"),
                        f"source is a relative path: {src}"):
        return
    pdir = os.path.join(root, src)
    if not report.check(os.path.isdir(pdir), f"source directory exists: {src}"):
        return

    man = load_json(report, os.path.join(pdir, ".claude-plugin", "plugin.json"),
                    ".claude-plugin/plugin.json")
    if man is None:
        return
    if not report.check(isinstance(man, dict), "plugin.json is an object"):
        return
    report.check(man.get("name") == name, "plugin.json name matches marketplace entry")
    report.check(isinstance(man.get("name"), str) and bool(re.fullmatch(KEBAB, man["name"])),
                 "name is kebab-case")
    version = man.get("version")
    report.check(isinstance(version, str) and bool(re.fullmatch(r"\d+\.\d+\.\d+", version)),
                 f"version is semver: {version}")

    for declared in ("commands", "agents", "hooks", "skills"):
        if isinstance(man.get(declared), str):
            report.check(os.path.exists(os.path.join(pdir, man[declared])),
                         f"declared {declared} path exists: {man[declared]}")

    if isinstance(man.get("mcpServers"), str):
        check_mcp(report, pdir, man["mcpServers"])

    check_skills(report, root, ratchet, pdir)
    check_skill_md_placement(report, root, pdir)
    check_components(report, root, ratchet, pdir)


def run(root=ROOT, out=None):
    """Validate the repo at `root`; returns the Report (failures, warnings)."""
    report = Report(out)
    report.say("marketplace")
    if yaml is None:
        report.check(False, "PyYAML is installed (python3 -m pip install pyyaml)")
    ratchet = load_ratchet(report, root)
    mkt = load_json(report, os.path.join(root, ".claude-plugin", "marketplace.json"),
                    ".claude-plugin/marketplace.json at repo root")
    if mkt is None:
        return report
    if not report.check(isinstance(mkt, dict), "marketplace.json is an object"):
        return report
    report.check(isinstance(mkt.get("name"), str) and bool(re.fullmatch(KEBAB, mkt["name"])),
                 f"marketplace name is kebab-case: {mkt.get('name')}")
    owner = mkt.get("owner")
    report.check(isinstance(owner, dict) and "name" in owner, "owner.name present")
    plugins = mkt.get("plugins")
    if not report.check(isinstance(plugins, list) and bool(plugins), "plugins[] is a non-empty list"):
        return report
    for entry in plugins:
        check_plugin(report, root, ratchet, entry)
    return report


def main(root=ROOT, out=None):
    report = run(root, out)
    report.say()
    if report.failures:
        report.say(f"{len(report.failures)} failure(s):")
        for f in report.failures:
            report.say("  - " + f)
        return 1
    suffix = f" ({len(report.warnings)} warning(s))" if report.warnings else ""
    report.say("all checks passed" + suffix)
    return 0


if __name__ == "__main__":
    sys.exit(main())
