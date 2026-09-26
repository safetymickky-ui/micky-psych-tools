#!/usr/bin/env bash
# Fixture marketplace (eval scaffold): a catalog, two valid plugins, and stub
# scripts/{validate,route,bump}.py that enforce the marketplace's mechanical rules.
# The version lives in plugin.json only; catalog entries carry none.
# Planted: firecrawl's SKILL.md frontmatter says name: fire-crawl in directory
# skills/firecrawl (a mechanical blocker); its description has no Not-for clause.
set -euo pipefail
mkdir -p .claude-plugin scripts
cat > .claude-plugin/marketplace.json <<'EOF'
{
  "name": "micky-psych-tools",
  "owner": {"name": "fixture"},
  "plugins": [
    {"name": "vault-keeper", "source": "./plugins/vault-keeper", "description": "Fixture plugin.", "category": "productivity", "keywords": ["vault", "notes", "index"]},
    {"name": "pubmed-research-note", "source": "./plugins/pubmed-research-note", "description": "Fixture plugin.", "category": "research", "keywords": ["pubmed", "evidence", "psychiatry"]},
    {"name": "firecrawl", "source": "./plugins/firecrawl", "description": "Fixture plugin.", "category": "productivity", "keywords": ["firecrawl", "web-scraping", "crawl"]}
  ]
}
EOF
mkdir -p plugins/vault-keeper/.claude-plugin plugins/vault-keeper/skills/vault-keeper
cat > plugins/vault-keeper/.claude-plugin/plugin.json <<'EOF'
{
  "name": "vault-keeper",
  "version": "0.4.0",
  "description": "Fixture plugin.",
  "author": {"name": "fixture"},
  "keywords": ["vault", "notes", "index"]
}
EOF
cat > plugins/vault-keeper/skills/vault-keeper/SKILL.md <<'EOF'
---
name: vault-keeper
description: Files, indexes, links, and retrieves any skill's output in the shared vault at the marketplace repo root. Use when the user says "save this to the vault", "vault this", "index the vault", or "search my vault". Not for producing the artifact itself; the source skill does that.
---

# vault-keeper

Fixture skill body.
EOF
mkdir -p plugins/pubmed-research-note/.claude-plugin plugins/pubmed-research-note/skills/pubmed-research-note
cat > plugins/pubmed-research-note/.claude-plugin/plugin.json <<'EOF'
{
  "name": "pubmed-research-note",
  "version": "1.7.0",
  "description": "Fixture plugin.",
  "author": {"name": "fixture"},
  "keywords": ["pubmed", "evidence", "psychiatry"]
}
EOF
cat > plugins/pubmed-research-note/skills/pubmed-research-note/SKILL.md <<'EOF'
---
name: pubmed-research-note
description: Answers a clinical question from primary literature with a quantified, adjudicated evidence report and a clearly marked verdict. Use when asked to "research", "what does the literature say about", or "search PubMed for". Not for whole-disorder reviews (comprehensive-review).
---

# pubmed-research-note

Fixture skill body.
EOF
mkdir -p plugins/firecrawl/.claude-plugin plugins/firecrawl/skills/firecrawl
cat > plugins/firecrawl/.claude-plugin/plugin.json <<'EOF'
{
  "name": "firecrawl",
  "version": "0.2.0",
  "description": "Fixture plugin.",
  "author": {"name": "fixture"},
  "keywords": ["firecrawl", "web-scraping", "crawl"]
}
EOF
cat > plugins/firecrawl/skills/firecrawl/SKILL.md <<'EOF'
---
name: fire-crawl
description: 'Routes general-web data requests to the right Firecrawl path: live CLI tools (search, scrape, interact, crawl, map), app-code integration with the SDK, workflow deliverables, credential auth, REST-only, or the keyless free tier. Use when the user says "firecrawl", "scrape this page", "search the web", or "crawl these docs".'
---

# firecrawl

Fixture skill body.
EOF
cat > scripts/validate.py <<'EOF'
#!/usr/bin/env python3
"""Fixture validator (eval scaffold): the marketplace's mechanical rules only. The version
lives in plugin.json only; catalog entries carry none, so nothing is compared."""
import json, os, re, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cat = json.load(open(os.path.join(root, ".claude-plugin", "marketplace.json"), encoding="utf-8"))
kebab = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
fails, warns = [], []
for e in cat.get("plugins", []):
    name = e.get("name", "")
    if not kebab.match(name):
        fails.append(f"{name}: name is not kebab-case")
    if not str(e.get("source", "")).startswith("./"):
        fails.append(f"{name}: source is not a ./ relative path")
    src = os.path.join(root, e.get("source", ""))
    pj = os.path.join(src, ".claude-plugin", "plugin.json")
    if not os.path.isfile(pj):
        fails.append(f"{name}: missing .claude-plugin/plugin.json")
        continue
    p = json.load(open(pj, encoding="utf-8"))
    if p.get("name") != name:
        fails.append(f"{name}: plugin.json name {p.get('name')!r} != catalog name")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(p.get("version", ""))):
        fails.append(f"{name}: plugin.json version {p.get('version')!r} is not semver")
    skills = os.path.join(src, "skills")
    for s in sorted(os.listdir(skills)) if os.path.isdir(skills) else []:
        md = os.path.join(skills, s, "SKILL.md")
        text = open(md, encoding="utf-8").read() if os.path.isfile(md) else ""
        m = re.match(r"---\n(.*?)\n---", text, re.S)
        fm = m.group(1) if m else ""
        nm = re.search(r"^name:\s*(\S+)", fm, re.M)
        if not nm or nm.group(1) != s:
            fails.append(f"{name}/{s}: frontmatter name does not match its directory")
        d = re.search(r"^description:\s*(.+)$", fm, re.M)
        n = len(d.group(1).strip()) if d else 0
        if n > 1024:
            fails.append(f"{name}/{s}: description {n} chars (hard cap 1024)")
        elif n < 200:
            warns.append(f"{name}/{s}: description {n} chars is short; under ~200 triggers unreliably")
    for dirpath, _, files in os.walk(src):
        for f in files:
            parts = os.path.relpath(os.path.join(dirpath, f), src).split(os.sep)
            if f.lower() == "skill.md" and not (len(parts) == 3 and parts[0] == "skills"):
                fails.append(f"{name}: {'/'.join(parts)} is a SKILL.md outside skills/<skill>/")
for w in warns:
    print("WARN", w)
for f in fails:
    print("FAIL", f)
print("all checks passed" if not fails else f"{len(fails)} check(s) failed")
sys.exit(1 if fails else 0)
EOF
cat > scripts/route.py <<'EOF'
#!/usr/bin/env python3
"""Fixture router (eval scaffold): regenerate ROUTING.md from the catalog."""
import json, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cat = json.load(open(os.path.join(root, ".claude-plugin", "marketplace.json"), encoding="utf-8"))
lines = ["# ROUTING (generated by scripts/route.py)", ""]
lines += [f"- {e['name']}: {e.get('description', '')}" for e in cat.get("plugins", [])]
open(os.path.join(root, "ROUTING.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("ROUTING.md written")
EOF
cat > scripts/bump.py <<'EOF'
#!/usr/bin/env python3
"""Fixture bump (eval scaffold): the version lives in plugin.json only (catalog entries
carry none). A dry run unless --write; --write validates, writes plugin.json, adds a
"## <version> — <date>" heading to the plugin's CHANGELOG.md, then validates again."""
import datetime, json, os, subprocess, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if a != "--write"]
if len(args) != 2 or args[1] not in ("patch", "minor", "major"):
    print("usage: bump.py <plugin> patch|minor|major [--write]")
    sys.exit(1)
name, level = args
cat = json.load(open(os.path.join(root, ".claude-plugin", "marketplace.json"), encoding="utf-8"))
entry = next((e for e in cat.get("plugins", []) if e.get("name") == name), None)
pdir = os.path.join(root, entry["source"]) if entry else os.path.join(root, "plugins", name)
pj = os.path.join(pdir, ".claude-plugin", "plugin.json")
if not os.path.isfile(pj):
    print(f"unknown plugin: {name}")
    sys.exit(1)
p = json.load(open(pj, encoding="utf-8"))
old = p["version"]
ma, mi, pa = (int(x) for x in old.split("."))
new = {"patch": f"{ma}.{mi}.{pa + 1}", "minor": f"{ma}.{mi + 1}.0", "major": f"{ma + 1}.0.0"}[level]
print(f"{name}: {old} -> {new}")
if "--write" not in sys.argv[1:]:
    print("dry run: nothing written; re-run with --write to apply")
    sys.exit(0)
validate = [sys.executable, os.path.join(root, "scripts", "validate.py")]
if subprocess.call(validate) != 0:
    print("validate.py failed before the bump; nothing written")
    sys.exit(1)
p["version"] = new
with open(pj, "w", encoding="utf-8") as f:
    json.dump(p, f, indent=2)
    f.write("\n")
cl = os.path.join(pdir, "CHANGELOG.md")
text = open(cl, encoding="utf-8").read() if os.path.isfile(cl) else "# Changelog\n"
head, sep, rest = text.partition("\n## ")
with open(cl, "w", encoding="utf-8") as f:
    f.write(head.rstrip("\n") + "\n\n" + f"## {new} — {datetime.date.today().isoformat()}\n\n"
            + ("## " + rest if sep else ""))
print("wrote plugin.json and CHANGELOG.md")
sys.exit(subprocess.call(validate))
EOF
chmod +x scripts/*.py
