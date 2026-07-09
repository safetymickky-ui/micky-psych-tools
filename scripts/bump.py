#!/usr/bin/env python3
"""Bump a plugin's version in BOTH places, then validate.

Version lives in two files that must never disagree: the plugin's own
`.claude-plugin/plugin.json`, and its entry in the marketplace catalog. If they
drift, Claude Code compares the catalog version against what's installed, sees
no change, and silently offers no update. The plugin is "updated" and nothing
happens. This script is the whole reason that failure mode can't occur.

    python3 scripts/bump.py pubmed-research-note patch
    python3 scripts/bump.py pubmed-research-note minor
    python3 scripts/bump.py pubmed-research-note major
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MKT = os.path.join(ROOT, ".claude-plugin", "marketplace.json")


def bump(version, level):
    major, minor, patch = (int(x) for x in version.split("."))
    if level == "major":
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    if level == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise SystemExit(f"unknown level: {level} (use major|minor|patch)")


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    plugin_name, level = sys.argv[1], sys.argv[2]

    mkt = json.load(open(MKT, encoding="utf-8"))
    entry = next((p for p in mkt["plugins"] if p["name"] == plugin_name), None)
    if entry is None:
        raise SystemExit(f"{plugin_name} is not listed in the marketplace")

    man_path = os.path.join(ROOT, entry["source"], ".claude-plugin", "plugin.json")
    man = json.load(open(man_path, encoding="utf-8"))

    old = man["version"]
    new = bump(old, level)

    man["version"] = new
    entry["version"] = new  # the line that prevents the silent no-op update

    json.dump(man, open(man_path, "w", encoding="utf-8"), indent=2)
    json.dump(mkt, open(MKT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    print(f"{plugin_name}: {old} -> {new}  (plugin.json + marketplace.json)\n")
    sys.exit(subprocess.call([sys.executable, os.path.join(ROOT, "scripts", "validate.py")]))


if __name__ == "__main__":
    main()
