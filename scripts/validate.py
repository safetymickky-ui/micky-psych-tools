#!/usr/bin/env python3
"""Validate the marketplace and every plugin in it.

Runs the checks `claude plugin validate` runs, plus the two that have actually
bitten: the SKILL.md description length cap, and version drift between a
plugin's own manifest and its marketplace entry.

    python3 scripts/validate.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILURES = []


def check(condition, message):
    print(("  PASS  " if condition else "  FAIL  ") + message)
    if not condition:
        FAILURES.append(message)


def frontmatter(path):
    """Parse YAML frontmatter without requiring pyyaml.

    Only two fields matter here — name and description — and description may be
    a folded block scalar (`>-`), so fold continuation lines into one string.
    """
    text = open(path, encoding="utf-8").read()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None
    fields, key = {}, None
    for line in match.group(1).split("\n"):
        header = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        if header:
            key = header.group(1)
            value = header.group(2).strip()
            fields[key] = "" if value in (">-", ">", "|", "|-") else value
        elif key and line.startswith("  "):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def main():
    mkt_path = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
    print("marketplace")
    check(os.path.isfile(mkt_path), ".claude-plugin/marketplace.json exists at repo root")
    mkt = json.load(open(mkt_path, encoding="utf-8"))
    check(bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", mkt.get("name", ""))),
          f"marketplace name is kebab-case: {mkt.get('name')}")
    check("owner" in mkt and "name" in mkt["owner"], "owner.name present")
    check(isinstance(mkt.get("plugins"), list) and mkt["plugins"], "plugins[] is a non-empty list")

    for entry in mkt["plugins"]:
        name = entry.get("name", "<unnamed>")
        print(f"\nplugin: {name}")

        # source must resolve. relative paths only work for git/local marketplaces,
        # never for a marketplace distributed as a bare URL.
        src = entry.get("source", "")
        check(isinstance(src, str) and src.startswith("./"),
              f"source is a relative path: {src}")
        pdir = os.path.join(ROOT, src)
        check(os.path.isdir(pdir), f"source directory exists: {src}")
        if not os.path.isdir(pdir):
            continue

        man_path = os.path.join(pdir, ".claude-plugin", "plugin.json")
        check(os.path.isfile(man_path), ".claude-plugin/plugin.json exists")
        man = json.load(open(man_path, encoding="utf-8"))
        check(man.get("name") == name, "plugin.json name matches marketplace entry")
        check(bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", man.get("name", ""))), "name is kebab-case")
        check(bool(re.fullmatch(r"\d+\.\d+\.\d+", man.get("version", ""))),
              f"version is semver: {man.get('version')}")

        # the check that stops silent staleness: a bumped plugin whose catalog
        # entry still advertises the old version will not offer an update.
        check(entry.get("version") == man.get("version"),
              f"marketplace entry version {entry.get('version')} == plugin.json {man.get('version')}")

        for declared in ("commands", "agents", "hooks", "skills"):
            if declared in man and isinstance(man[declared], str):
                check(os.path.exists(os.path.join(pdir, man[declared])),
                      f"declared {declared} path exists")

        if "mcpServers" in man and isinstance(man["mcpServers"], str):
            mcp_path = os.path.join(pdir, man["mcpServers"])
            check(os.path.isfile(mcp_path), f"declared mcpServers file exists: {man['mcpServers']}")
            mcp = json.load(open(mcp_path, encoding="utf-8"))
            check(all("url" in s and "type" in s for s in mcp.get("mcpServers", {}).values()),
                  "every mcp server has type and url")

        skills_dir = os.path.join(pdir, "skills")
        if os.path.isdir(skills_dir):
            for skill in sorted(os.listdir(skills_dir)):
                sp = os.path.join(skills_dir, skill, "SKILL.md")
                check(os.path.isfile(sp), f"skills/{skill}/SKILL.md exists")
                if not os.path.isfile(sp):
                    continue
                fm = frontmatter(sp)
                check(fm is not None, f"skills/{skill}: frontmatter parses")
                if not fm:
                    continue
                check(fm.get("name") == skill, f"skills/{skill}: frontmatter name matches directory")
                n = len(fm.get("description", ""))
                check(n <= 1024, f"skills/{skill}: description {n} chars (hard cap 1024)")
                check(n >= 200, f"skills/{skill}: description {n} chars (min 200 for reliable triggering)")
                ev = os.path.join(skills_dir, skill, "evals", "evals.json")
                if os.path.isfile(ev):
                    json.load(open(ev, encoding="utf-8"))
                    print(f"  PASS  skills/{skill}/evals/evals.json is valid JSON")

        for comp in ("commands", "agents"):
            cdir = os.path.join(pdir, comp)
            if os.path.isdir(cdir):
                for fname in sorted(os.listdir(cdir)):
                    if not fname.endswith(".md"):
                        continue
                    fm = frontmatter(os.path.join(cdir, fname)) or {}
                    check(bool(fm.get("description")),
                          f"{comp}/{fname}: frontmatter description present")
                    if comp == "agents":
                        n = len(fm.get("description", ""))
                        check(200 <= n <= 1024,
                              f"agents/{fname}: description {n} chars in 200-1024")

    print()
    if FAILURES:
        print(f"{len(FAILURES)} failure(s):")
        for f in FAILURES:
            print("  - " + f)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
