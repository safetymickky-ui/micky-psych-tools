#!/usr/bin/env python3
"""Bump one plugin's version: plugin.json plus a CHANGELOG entry. Dry run by default.

The version lives in `plugins/<name>/.claude-plugin/plugin.json` only (the catalog
carries none). Claude Code reads it from there, and `claude plugin validate --strict`
catches a manifest without one.

    python3 scripts/bump.py pubmed-research-note patch            # dry run: prints the plan
    python3 scripts/bump.py pubmed-research-note minor --write    # validates, then writes

--write, in order:
  1. runs scripts/validate.py and aborts with no write when it fails;
  2. writes the new version to plugin.json (UTF-8, no \\u escapes, trailing newline);
  3. adds "## <new> — <date>" above the newest entry of plugins/<name>/CHANGELOG.md
     (creates the file with a "# Changelog" header when absent);
  4. runs scripts/validate.py again and exits with its code. A failure here leaves the
     files bumped: the pre-check passed, so the write itself caused the problem, and
     reporting it beats discarding a concurrent manual edit.

Exit codes: 0 ok; 1 unknown plugin or level, or a validation failure.
"""
import argparse
import datetime
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEVELS = ("major", "minor", "patch")


def bump(version, level):
    major, minor, patch = (int(x) for x in version.split("."))
    if level == "major":
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    if level == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"unknown level: {level} (use major|minor|patch)")


def plugin_dir(root, name):
    """The plugin's directory: its catalog source when listed, else plugins/<name>."""
    mkt = os.path.join(root, ".claude-plugin", "marketplace.json")
    try:
        with open(mkt, encoding="utf-8") as fh:
            entries = json.load(fh).get("plugins", [])
        entry = next((p for p in entries if isinstance(p, dict) and p.get("name") == name), None)
        if entry and isinstance(entry.get("source"), str):
            return os.path.normpath(os.path.join(root, entry["source"]))
    except (OSError, ValueError, AttributeError):
        pass
    return os.path.join(root, "plugins", name)


def changelog_stub(new, date):
    return f"## {new} — {date}\n\n"


def add_changelog_entry(path, new, date):
    """Insert the stub above the newest `## ` entry (after the title), or create the file."""
    stub = changelog_stub(new, date)
    if not os.path.isfile(path):
        text = "# Changelog\n\n" + stub
    else:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        idx = 0 if text.startswith("## ") else text.find("\n## ")
        if idx == -1:
            text = text.rstrip("\n") + "\n\n" + stub
        else:
            cut = idx if idx == 0 else idx + 1
            text = text[:cut] + stub + text[cut:]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def run_validator(root):
    return subprocess.call([sys.executable, os.path.join(root, "scripts", "validate.py")])


def main(argv=None, root=ROOT, today=None, validator=None, out=None):
    out = out if out is not None else sys.stdout
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("plugin")
    parser.add_argument("level", help="major | minor | patch")
    parser.add_argument("--write", action="store_true", help="validate, then write (default: dry run)")
    args = parser.parse_args(argv)
    validator = validator or run_validator
    date = today or datetime.date.today().isoformat()

    if args.level not in LEVELS:
        out.write(f"unknown level: {args.level} (use major|minor|patch)\n")
        return 1
    pdir = plugin_dir(root, args.plugin)
    man_path = os.path.join(pdir, ".claude-plugin", "plugin.json")
    if not os.path.isfile(man_path):
        out.write(f"unknown plugin: {args.plugin} (no {os.path.relpath(man_path, root)})\n")
        return 1
    with open(man_path, encoding="utf-8") as fh:
        man = json.load(fh)
    old = man.get("version", "")
    try:
        new = bump(old, args.level)
    except ValueError:
        out.write(f"{args.plugin}: version {old!r} in plugin.json is not x.y.z\n")
        return 1
    changelog = os.path.join(pdir, "CHANGELOG.md")

    out.write(f"{args.plugin}: {old} -> {new}\n")
    if not args.write:
        out.write(f"dry run: would write plugin.json and add to {os.path.relpath(changelog, root)}:\n")
        out.write(changelog_stub(new, date))
        out.write("re-run with --write to apply\n")
        return 0

    if validator(root) != 0:
        out.write("validate.py failed before the bump; nothing written\n")
        return 1
    man["version"] = new
    with open(man_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(man, ensure_ascii=False, indent=2) + "\n")
    add_changelog_entry(changelog, new, date)
    out.write(f"wrote {os.path.relpath(man_path, root)} and {os.path.relpath(changelog, root)}\n")
    code = validator(root)
    if code != 0:
        out.write(f"validate.py failed after the bump (exit {code}); the files stay bumped\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
