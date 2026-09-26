# micky-psych-tools

A personal Claude Code plugin marketplace. One installer: you.

## Register it once

**Local (recommended for a single-owner marketplace).** No git host, no push, no public repo:

```bash
/plugin marketplace add /absolute/path/to/micky-psych-tools
/plugin install pubmed-research-note@micky-psych-tools
```

**GitHub (only if you need it on more than one machine).** The source must be a repo you can
clone with your own git credentials, so it works with a **private** repo too (this marketplace
is installed from a private GitHub remote today).

`.gitignore` excludes `.env` and `.firecrawl/` (firecrawl's API key and cache), so the
`git add -A` below does not stage them:

```bash
git init && git add -A && git commit -m "init"
git remote add origin git@github.com:<you>/micky-psych-tools.git && git push -u origin main
/plugin marketplace add <you>/micky-psych-tools
/plugin install pubmed-research-note@micky-psych-tools
```

Relative `source` paths (`./plugins/…`) resolve only when the marketplace is added via git or
a local path. Serving `marketplace.json` from a bare URL breaks them silently.

The examples above install `pubmed-research-note`; swap in any of the other thirteen —
`intent-lock`, `plugin-creator`, `vault-keeper`, `psych-paper-digest`, `comprehensive-review`,
`clinical-infographic`, `firecrawl`, `concept-animation`, `gridgeist`, `code-explainer`,
`ml-concept-lab`, `decision-interview`, or `plan-critique` (or any future plugin) by name —
the commands are identical for all of them.

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
python3 scripts/validate.py                                        # always available
claude plugin validate --strict .claude-plugin/marketplace.json    # the catalog
claude plugin validate --strict plugins/<name>                     # one plugin's content
```

The CLI covers the manifests, and `--strict` turns its warnings (a version mismatch among
them) into failures. A run on the catalog alone never opens a plugin's content, so validate
each `plugins/<name>` directory too. `validate.py` adds what the CLI does not check: every
file load counted rather than crashing, strict YAML frontmatter, the 1,024-character
`SKILL.md` description cap (under 200 is a warning), a description on every command and
agent, MCP server shapes (http/sse or stdio), and legacy `evals.json` validity. Versions live
in `plugin.json` only, so there is no catalog version left to compare.

## Plugins

Fourteen plugins, all vendored under `plugins/` and listed in `.claude-plugin/marketplace.json`:

- **pubmed-research-note** — answers a clinical question from primary literature. Quantified,
  adjudicated, trial-registry-checked evidence reports with a clearly marked verdict and full
  per-study depth, in whatever shape serves the question. Runs `intent-lock` first on every
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
  AI-onboarding guide (install command, skill segments, usage paths A–F) and serves as the
  general-web evidence engine for `pubmed-research-note` and `comprehensive-review`
  (regulator labels, guideline full texts — fetch-only, adjudication stays with the caller);
  deliverables gate through `intent-lock` and vault via `vault-keeper` on request. Biomedical
  literature stays with the PubMed-facing plugins, and API keys stay in the environment.
- **concept-animation** — turns a concept into a self-contained HTML animation that unfolds it
  scene by scene, with captions, player controls, and a reduced-motion fallback. Motion must
  explain, never decorate; clinical facts come only from sourced reports.
- **gridgeist** — design, redesign, and review web interfaces with a strong grid, precise
  typography, and product-specific visual systems. Vendored from upstream under MIT.
- **code-explainer** — explains given code as one self-contained interactive HTML page: the
  source in a VS Code-styled editor on the left, the explanation on the right, cross-linked
  line by line, with a step-through walkthrough and a flow diagram. Reproduces the source
  verbatim and never invents a runtime value.
- **ml-concept-lab** — the interactive sibling of `concept-animation` for machine-learning, AI,
  and computer-science concepts: a self-contained HTML explorable in which the real algorithm
  runs live and the learner drives it. Every number is computed rather than drawn, a self-check
  panel asserts the algorithm's invariants on screen, and the controls reach the regime where it
  breaks. Verified by being driven headless, then filed as a vault asset via `vault-keeper`.
- **decision-interview** — mid-task decision gate: sweeps the task for every decision only the
  user can make and resolves them all in one batched option-picker interview, recorded in a
  decision ledger. The execution-phase sibling of `intent-lock`.
- **plan-critique** — adversarial nine-lens critique of an existing plan that ends in a better
  plan: repairs with one right answer are applied, owner-held forks are resolved in a batched
  interview, and the full revised plan ships under a decision ledger.
- **bullet-reconstruct** — turns a dense paper, chapter or transcript into tight bullets with
  measured loss under 10% (units frozen first, anchors and numbers checked against the output),
  keeps its figures and tables as image snips, and delivers one self-contained HTML file.
