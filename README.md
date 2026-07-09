# micky-psych-tools

A personal Claude Code plugin marketplace. One installer: you.

## Register it once

**Local (recommended for a single-owner marketplace).** No git host, no push, no public repo:

```bash
/plugin marketplace add /absolute/path/to/micky-psych-tools
/plugin install pubmed-research-note@micky-psych-tools
```

**GitHub (only if you need it on more than one machine).** Claude Code fetches marketplaces
directly from the host, so a GitHub-sourced marketplace must be a **public** repo:

```bash
git init && git add -A && git commit -m "init"
git remote add origin git@github.com:<you>/micky-psych-tools.git && git push -u origin main
/plugin marketplace add <you>/micky-psych-tools
/plugin install pubmed-research-note@micky-psych-tools
```

Relative `source` paths (`./plugins/…`) resolve only when the marketplace is added via git or
a local path. Serving `marketplace.json` from a bare URL breaks them silently.

## Update it

```bash
python3 scripts/bump.py pubmed-research-note patch   # edit files first, then bump
# git commit && git push        # GitHub-sourced only
/plugin marketplace update micky-psych-tools
/plugin update pubmed-research-note@micky-psych-tools
```

`bump.py` writes the new version to `plugin.json` **and** the marketplace entry, then runs the
validator. Editing only one of the two is the failure this repo is shaped to prevent: Claude
Code compares the catalog version to what's installed, sees no change, and offers no update.
Your edits are on disk, live, and ignored.

For a local-path marketplace you can skip the bump while iterating — `/plugin marketplace update`
re-reads the directory. Bump when you want the version to mean something.

## Validate before you register

```bash
python3 scripts/validate.py          # always available
claude plugin validate .claude-plugin/marketplace.json   # if the CLI is installed
```

The validator enforces two things the CLI does not: `SKILL.md` descriptions must be
200–1024 characters, and every plugin's manifest version must equal its marketplace entry.

## Plugins

- **pubmed-research-note** — answers a clinical decision from primary literature. Verdict-first,
  quantified, trial-registry-checked. Vault notes only on the word *atomize*.

  **Requires `intent-lock`,** which is not vendored here and never should be — a second copy
  would drift from the one you maintain and collide on the skill name. If you want both from one
  command, add a second entry to `.claude-plugin/marketplace.json` whose `source` points at
  intent-lock's real location (a `github` source, or another relative path if you move it in
  here as its own plugin). Nothing resolves the dependency automatically; if `intent-lock` is
  absent, a bare topic will chain into a handoff that goes nowhere and quietly search anyway.
