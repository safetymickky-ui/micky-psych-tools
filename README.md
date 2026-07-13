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

The examples above install `pubmed-research-note`; swap in any of the other seven —
`intent-lock`, `plugin-creator`, `vault-keeper`, `psych-paper-digest`, `comprehensive-review`,
`clinical-infographic`, or `firecrawl` (or any future plugin) by name — the commands are
identical for all of them.

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

The validator enforces things the CLI does not: `SKILL.md` description length (200–1024
characters), version parity between a plugin's manifest and its marketplace entry, per-skill
`evals.json` validity, and that every command/agent carries a frontmatter description.

## Plugins

Eight plugins, all vendored under `plugins/` and listed in `.claude-plugin/marketplace.json`:

- **pubmed-research-note** — answers a clinical decision from primary literature. Verdict-first,
  quantified, trial-registry-checked evidence reports. Runs `intent-lock` first on every
  request, and delegates vault saving to `vault-keeper`.
- **intent-lock** — pre-build alignment gate. Interrogates a request until it has exactly one
  reading, then builds it.
- **plugin-creator** — meta-plugin for this marketplace. Scaffolds new plugins (`/new-plugin`)
  and refines existing ones (`/refine-plugin`), and regenerates the router (`/route`).
- **vault-keeper** — shared knowledge-vault manager for the repo-root `vault/`. Other plugins
  delegate their vault writes to it instead of writing vault files themselves.
- **psych-paper-digest** — watchlist-driven literature surveillance: windowed PubMed +
  ClinicalTrials.gov sweeps triaged into a read-once digest. Act items hand off to
  `pubmed-research-note`; vault saves are opt-in, via `vault-keeper`.
- **comprehensive-review** — whole-disorder academic reviews at textbook-chapter breadth,
  gated by `intent-lock` and filed to the vault via `vault-keeper`; live decisions route to
  `pubmed-research-note`.
- **clinical-infographic** — renders a sourced report or review into a print-ready medical
  summary infographic (one self-contained HTML file), filed as a vault asset via
  `vault-keeper`. Never generates clinical facts itself.
- **firecrawl** — Firecrawl onboarding and routing for general-web data: search, scrape,
  interact, crawl, and map via the Firecrawl CLI or API. Packages the vendor's official
  AI-onboarding guide (install command, skill segments, usage paths A–F); biomedical
  literature stays with the PubMed-facing plugins, and API keys stay in the environment.
