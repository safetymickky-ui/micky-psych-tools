# micky-psych-tools — plugin marketplace

Personal Claude Code plugin marketplace. Single owner: Thanawat Suharit (Micky).
This repo is BOTH the marketplace and the home of every plugin in it.

**`CLAUDE.md` holds stable conventions; `MEMORY.md` holds living state** (current
versions, recent milestones, open threads). `MEMORY.md` is not required reading: open it
when you need that state, and update it whenever you release, add a plugin, or close a
milestone.

## Routing (note)

Skills route from their own descriptions. `ROUTING.md` is an optional index of every
skill and command, not required reading; `/route "<request>"` names the skill or
command that owns a request. `ROUTING.md` is GENERATED — never hand-edit it.
`scripts/route.py` writes it from the catalog + every plugin's components, and
`/new-plugin` and `/refine-plugin` rerun it automatically.

## Layout

```
.claude-plugin/marketplace.json   # catalog — every plugin listed here
plugins/<name>/
  .claude-plugin/plugin.json       # plugin manifest (name, version, author, keywords)
  README.md                        # what the plugin does, how to use it
  CHANGELOG.md                     # top entry == plugin.json version
  LICENSE                          # MIT (gridgeist keeps upstream's)
  .mcp.json                        # optional — MCP servers (referenced from plugin.json)
  hooks/hooks.json                 # optional — plugin hooks
  skills/<skill>/SKILL.md          # skill(s): frontmatter (name, description) + body
  skills/<skill>/references/       # optional — files the skill body links to
  evals/<skill>/<case>/            # eval cases (plugin root, one dir per case)
  commands/<cmd>.md                # optional — slash commands
  agents/<agent>.md                # optional — subagents
scripts/validate.py                # full marketplace + plugin validation
scripts/bump.py                    # version bump in plugin.json + CHANGELOG (dry run unless --write)
scripts/route.py                   # generates ROUTING.md from the catalog + every plugin's components
ROUTING.md                         # generated router — never hand-edit
vault/                             # shared knowledge vault — managed by vault-keeper
```

## Hard rules (these have bitten before)

- **Version lives in `plugin.json` only.** `plugins/<name>/.claude-plugin/plugin.json` holds
  the plugin's version; the catalog entry in `.claude-plugin/marketplace.json` carries none.
  NEVER edit a version by hand — run `python3 scripts/bump.py <plugin> patch|minor|major --write`
  (without `--write` it is a dry run; with it, it validates, writes plugin.json and adds a
  CHANGELOG entry).
- **SKILL.md description cap:** hard limit 1024 chars; aim well under. Too short (<~200) triggers
  unreliably. The description is the ONLY thing that decides when the skill fires — invest in it.
- **Catalog description cap: 500 chars** — the plugin's entry in `marketplace.json`. The
  claude.ai plugin sync leaves out any plugin over it (5 were dropped on 2026-10-12);
  `validate.py` fails on it. (`plugin.json` descriptions are not held to it by the sync.)
- **`name` is kebab-case** and must match: plugin dir name == plugin.json name == marketplace entry.
  Skill frontmatter `name` == its directory name.
- **`source` is a relative path** (`./plugins/<name>`) in the marketplace entry.
- **`SKILL.md` is a reserved file name.** Only `skills/<skill>/SKILL.md` may carry it: some
  surfaces load any `SKILL.md` they find as a skill, so a nested template once showed up as
  a live skill named `skill-name`. Name templates and fixtures otherwise
  (`SKILL.template.md`); `validate.py` fails on a stray one.

## Workflow for adding / changing a plugin

1. Scaffold under `plugins/<name>/` following the layout above.
2. Add the entry to `.claude-plugin/marketplace.json` (name, source, description, category, keywords; no version).
3. `bash scripts/health.sh` must be green.
4. Bump with `python3 scripts/bump.py <plugin> patch|minor|major --write` when releasing, never by hand.
5. Commit (conventional commits: `feat:`, `fix:`, `refactor:`…). One logical change per commit.
6. Update `MEMORY.md` (versions table, milestones) when releasing.

Optional: `python3 scripts/route.py` regenerates `ROUTING.md` after a skill or command
description changes (`/new-plugin` and `/refine-plugin` do this automatically).

## Health check — run before every commit

- `bash scripts/health.sh` — must print `health: OK`. It runs `validate.py`,
  `claude plugin validate --strict` on the catalog and every plugin, the ratchet and
  trigger-lock checks, and the script unit tests. `--fast` skips the tests; the
  pre-commit hook runs it (enable once per clone: `git config core.hooksPath .githooks`).

## Plugins

- **pubmed-research-note** — answers a clinical question from primary literature; quantified,
  adjudicated evidence reports with a clearly marked verdict and full per-study depth, in
  whatever shape serves the question (decision-shaped or topic-shaped — no fixed frames, no
  fixed shape); runs intent-lock first to build a bespoke decision brief; five engines
  (PubMed backbone, CT.gov, Open Library, Wikipedia, firecrawl for general-web documents —
  labels, guidelines); delegates vault saving to vault-keeper.
- **intent-lock** — pre-build alignment gate: picker questions on kind of output, use, and depth
  and breadth in at most 3 rounds, then work; the finished work is checked against the written
  lock before delivery and 3–5 lock lines sit on top of the output. Drifts, interview errors and
  corrections are logged to the "Misread Ledger" artifact (database collections `checks` and
  `entries`), never to plugin files. Two skills (`intent-lock`, `misread-capture`), no commands.
- **plugin-creator** — meta-plugin: scaffolds new customized plugins into THIS marketplace
  (manifest + skill/command/agent/hooks/mcp-wiring skeleton + catalog entry + validation), and
  refines existing ones. Two skills (`plugin-creator`, `refine-plugin`) + three commands
  (`/new-plugin`, `/refine-plugin`, `/route`); elicit-first fixed checklist; auto-register +
  auto-validate, stops before commit. `/route` regenerates ROUTING.md and routes a request to
  the owning skill or command. Authoring rules + templates under its
  `skills/plugin-creator/references/`.
- **vault-keeper** — shared knowledge-vault manager for the repo-root `vault/`; five jobs: init,
  save, index, query, empty. Other plugins delegate vault writes to it rather than writing vault
  files themselves. The `empty-vault` skill (+ `/empty-vault [topic]`) drains the vault into the
  Learn hub — each artifact is handed to learn-hub's `digest-report` skill to become atomic Learn
  notes, and files are deleted only after a verified Supabase sync, a git-committed state, and
  explicit confirmation (move → verify → delete, never reordered).
- **psych-paper-digest** — watchlist-driven literature surveillance; windowed PubMed +
  ClinicalTrials.gov sweeps triaged into Act / Read / Suppressed, rendered as a read-once
  digest. Triage only, never adjudication: Act items hand off to pubmed-research-note; vault
  saves delegate to vault-keeper on explicit request only (unlike the other writers, which
  file by default). One skill + `/digest [domain]` command; config + `last_swept` state in
  `.psych-paper-digest.json`.
- **comprehensive-review** — whole-disorder academic literature reviews at textbook-chapter
  breadth: ten coverage domains from definition to controversies, with the chapter's
  structure designed per topic (coverage is the contract, structure is free) and
  load-bearing studies in full per-study depth — never silently narrowed to a treatment
  essay. Intent-lock is the mandatory Step 0 gate; searches PubMed +
  ClinicalTrials.gov itself (guideline/regulator full texts via firecrawl when a section
  needs them); the deliverable is an md file filed to the vault via vault-keeper.
  Decisions route to pubmed-research-note. One skill + `/comprehensive-review [topic]` command.
- **clinical-infographic** — the pipeline's last mile: renders a SOURCED report into a
  professional, print-ready medical summary infographic for clinical reference (one
  self-contained HTML file — color-coded columns, stat tiles, a mandatory "medications to
  avoid" safety banner). Ships no search engines by design and never fabricates a clinical
  fact — deep-integrates with comprehensive-review / pubmed-research-note (reuse an existing
  report or generate one first) and files the HTML as an asset via vault-keeper. One skill +
  `/infographic [topic-or-source]` command; fidelity contract + design system under its
  `skills/clinical-infographic/references/`.
- **firecrawl** — Firecrawl onboarding and routing for general-web data: search the web, scrape
  clean markdown, interact with live pages, crawl and map sites via the Firecrawl CLI or API.
  The skill body is Firecrawl's official AI-onboarding guide kept verbatim (one install
  command, three vendor skill segments, six usage paths A–F). Deep-integrated with the
  pipeline: the general-web evidence engine for pubmed-research-note and comprehensive-review
  (regulator labels, guideline full texts, gray literature — fetch-only, clean markdown +
  URL + access date, adjudication stays with the caller); Path C deliverables gate through
  intent-lock and file to the vault via vault-keeper on explicit request. Boundary:
  biomedical literature stays with pubmed-research-note / comprehensive-review /
  psych-paper-digest — mixed requests are split, not grabbed. Keys never enter the repo —
  `FIRECRAWL_API_KEY` lives in the environment. One skill, no commands.
- **code-explainer** — explains given code as one self-contained interactive HTML page:
  the source on the left in a VS Code-styled editor (Dark Modern, gutter, pre-tokenised
  syntax), the explanation on the right, cross-linked over one `data-range` id space.
  Three mandatory modes — hover/click line↔explanation highlighting, a debug-style
  step-through in *execution* order, and a clickable inline SVG flow diagram — plus an
  optional STATE trace for algorithmic code. Accuracy contract: source reproduced byte for
  byte, real defects named not smoothed, no invented runtime values, `& < >` escaped before
  tokenising. Intent-lock gates only ambiguous asks (a whole repo, several concerns); the
  vault is opt-in, not the default. Not a review or a refactor. One skill +
  `/explain-code [code-or-path]`; shell + contract + working template under its
  `skills/code-explainer/references/`.
- **concept-lab** (1.0.0 renamed ml-concept-lab and merged concept-animation into it) — one page
  for one concept, any field (ML, statistics, computational psychiatry, pharmacology, clinical).
  Shape locked by the owner on 2026-11-10 and corrected the same day (1.1.0) after the first
  real page: a **guided walkthrough** — the page opens on step 1, each step highlights one
  focus and dims the rest, a step card explains it in one or two beginner sentences plus one
  calculation line, Back/Next sit in a fixed bottom bar, the whole page fits one phone screen
  (390×700, no scrolling), no Play button, no sliders by default, 0–4 "what if" cases on the
  last step, a warm dark palette with serif headings; since 1.2.0 formulas are native MathML,
  colour-coded to match the picture, cards run two or three sentences, and the picture encodes
  values and direction and animates between steps; since 1.3.0 every step has things to tap
  (any part of the picture and any term or symbol opens a pop-up; the calculation is revealed
  line by line) with lively, meaningful motion; published as its own artifact (no vault
  filing unless asked). Free-play (≤2 sliders) only on request. Three modes: **computed** (the
  model is computed in the page; nothing drawn by hand), **authored** (reveal / branch / sort /
  compare for concepts with no model, labelled with its source) and **watch** (a
  scene-by-scene animation; motion must explain, never decorate).
  Clinical facts come only from a sourced report (session / vault / generated first via
  comprehensive-review or pubmed-research-note). Checks run in the page but are not shown
  (`window.__lab.checks()`); `scripts/verify.mjs` walks every step and case at phone and desktop
  size in both motion modes (no-scroll, touch size, overlapping or covered labels, text
  budget) and must exit 0 before publishing, and the step screenshots must then be looked at. Intent-lock is the mandatory Step 0
  gate. One skill + `/visualize [concept]` and `/animate [concept-or-source]`; build contract,
  pattern catalog (12 families) and animation grammar under `skills/concept-lab/references/`,
  worked lab under `examples/`. Since 1.4.0 three **field packs** under
  `skills/concept-lab/references/fields/` (endocrinology, general psychiatry, computational
  psychiatry) are read first in Step 1 for a concept in their field: each names the picture per
  kind of concept, the misconception, the "what if" cases, the default reader, colour roles and
  the field's source rules (endocrine clinical facts go through pubmed-research-note). Packs
  hold no clinical numbers, and add no skill, command or trigger phrase. Boundary: static
  clinical one-pagers stay with clinical-infographic, charts of the user's own data with
  dataviz.
- **plan-critique** — adversarial critique of an existing plan that ends in a better plan:
  nine lenses (goal-fit, completeness, sequencing, feasibility, risk, hidden assumptions,
  verifiability, simplicity, alternatives) find where it breaks, every finding carries a
  repair or a fork, repairs with one right answer are applied, and every fork only the
  plan's owner can decide (scope cuts, deadline vs quality, risk appetite) is resolved in
  a relentless batched option-picker interview — uncapped rounds, dependency order,
  recommended repair first, ended only by saturation, a user stop, or the two-empty-rounds
  guard. Verdict-first delivery: verdict line → findings by severity → the full revised
  plan under a decision ledger; every change traces to a finding or an answer, the goal
  never moves. Third gate in the alignment family: intent-lock owns pre-build request
  meaning, decision-interview owns the agent's own mid-execution decisions, this owns an
  existing plan artifact. Autonomous fallback mirrors decision-interview; vault filing via
  vault-keeper on explicit request only. One skill + `/critique-plan [plan-or-path]`; lens
  catalog under its `skills/plan-critique/references/`.
- **decision-interview** — mid-task decision gate: when the agent hits decisions only the
  user can make, it sweeps the task end to end (blockers, silent defaults, lookahead),
  triages against an admission threshold (destructive/irreversible/outward-facing actions
  always ask; sub-threshold items get stated defaults; already-answered items are resolved
  in place, never re-asked of the user), and resolves everything in one batched
  option-picker interview — dependency order, recommended option first, resolutions
  recorded in a decision ledger that governs the rest of the session. Autonomous fallback:
  reversible decisions take the recommended default surfaced in a "Decided without you"
  ledger; destructive ones halt with a written decision request. The execution-phase
  sibling of intent-lock (which owns pre-build alignment; misread-capture owns
  post-delivery). One skill + `/resolve-decisions [task or scope]` command.

- **clinical-minimal** — the user's personal Office design system ("Clinical Minimal") for every
  .docx/.pptx/.xlsx: white page, one clinical-teal accent, Leelawadee UI (Thai + English), no personal
  branding. Decides how a file looks while the calling plugin decides what it says. Ships `cm.py` build
  helpers, `slidecheck.py` + `slideprobe.ps1` (per-slide verification: PowerPoint lays the deck out,
  automatic FAIL/WARN rules, then a recorded full-size visual review per slide — exit 0 required before
  delivery) and `imgpick.py` (picture selection: brief → Google Images candidates → filter → score incl.
  subject fill → contact sheet as placed → visual judgement → choose, credits recorded). Brand book is the
  Clinical Minimal Design System artifact. Windows + Microsoft Office required. One skill, no commands.
- **bullet-reconstruct** — bounded-loss distillation of a dense source into scannable bullets, delivered
  as one self-contained HTML with the source's figures and tables embedded as image snips. The <10% loss
  cap is measured: units frozen from the source first, anchors checked in the output, numbers traced to
  the source (`coverage_check.py`). `snip_figures.py` crops captioned regions (vector tables included);
  `build_html.py` renders `notes.md`. One skill, no commands; script tests under the plugin's `tests/`.
- **vi-stock-screen-research** — value-investing stock work for Thai SET and US stocks, first plugin
  in the `finance` category. Screen: quality at a fair price on TradingView (ROIC, F-score, Altman Z,
  debt/equity, liquidity and size floors per market), top 10 by ROIC rank + earnings-yield rank, then
  it stops — the user picks one ticker. Deep research: a full company review, never narrowed to a
  valuation (Verdict · Business · Industry · Moat · Management · 10-year financials · Valuation ·
  Risks · Sell triggers), every number source-tagged, the buy/sell decision left to the user. Data
  order: TradingView → Jitta in the user's Chrome when fewer than 8 fiscal years → 56-1 One Report /
  10-K for governance. Output is a multi-page Word report + an Excel valuation model built through
  clinical-minimal. Intent-lock is the mandatory Step 0 gate in both modes; TradingView MCP bundled
  in `.mcp.json`; no vault filing. One skill + `/vi-screen` and `/vi-research`; screen criteria and
  report contract under its `skills/vi-stock-screen-research/references/`.

- **tutor** — teaches a new field chunk by chunk in the way the owner locked on 2026-10-12: a
  picker interview before every chunk (what he knows, why, how deep; no guess), then the chunk
  taught one small idea per message ("say next"), answer first, anchored to what he already owns,
  examples computed in code and code that really ran, numbered options after the last step. No quizzes, checks or reviews;
  exercises only on "give me an exercise", with a scaffold that fades over four levels. Routes
  by scope: a field starts a track (intent-lock, then a self-report owns-check picker), a single
  concept gets one chunk. Every lesson is saved to the "Tutor tracker" artifact: the page reads
  `tracks/` and `lessons/` from its own database, the skill writes through ArtifactData with
  version pins, finds the page by its title and recreates it from `assets/tracker.html`. Four
  domain packs under `skills/tutor/references/packs/` (comp-psych `cp`, python-r `py`, ml-dl
  `dl`, math-stats `ms`; seeds computed in Python, resources opened 2026-10-12). Not filed to
  the vault. One skill + `/tutor [track or topic]`.
- **design-md-generator** — generates a spec-valid DESIGN.md (Google Stitch format: YAML token front
  matter + ordered `##` sections) from one of four sources: a site URL (observed CSS only, never invented),
  a brief (labelled invented), a codebase (Tailwind/`:root`/components), or a remixed kit
  (awesome-design-md via `gh api`, or the user-scope designmd MCP, read-only unless asked). Lint with
  `npx -p @google/design.md designmd lint` is mandatory; an existing DESIGN.md is never overwritten (DESIGN.next.md +
  diff). Applies automatically: a SessionStart hook announces the nearest project DESIGN.md (else the
  personal default `~/.claude/DESIGN.md`), and the `design-md-apply` skill builds every UI/Artifact from it
  (tokens → CSS vars/Tailwind with dark mode, component specs, off-system check). Two skills +
  `/design-md [url|brief|path|kit]`; spec digest + per-mode recipes under
  `skills/design-md-generator/references/`. Lint via the `designmd` bin (the `design.md` bin is broken on Windows).
- **idea-to-3d** — one-line idea → textured, rigged, animated `.glb` + preview sheet: concept
  art, image-to-3D, remesh/rig/clips on Meshy (bundled `meshy` MCP; Actionforge graph for Stage 4), finishing in headless
  Blender 5.2, three user checkpoints. Each stage passes a maker → critic → reviser loop first:
  free concept/turnaround images through `agy` (`generate_image.py`; Meshy `nano-banana-pro`
  as paid fallback) and an independent Gemini critic (`critique.py` via the Antigravity CLI `agy`; the
  `idea3d-critic` Claude agent as fallback) at gates A1/A2/B/C, free fixes applied by the
  `idea3d-reviser` agent (no Meshy tools), credit-spending fixes only on approval, PASS or 2
  revise rounds. Five skills + three agents, no commands. Shares its critic core
  (`core-files.txt`) with the Antigravity repo `Desktop/repo/idea-to-3d`, which pulls it via
  `scripts/sync-core.ps1` — this copy is the source of truth.
- **learning-map** — one material (paper, chapter, lecture, URL, PDF, pasted text) in, one
  learning map out: the prerequisite knowledge as a dependency ladder (Level 0 foundations →
  Level 1 core → Level 2 what the material assumes), 5–12 learning pearls anchored to the
  material, and a 3–7 step concepts-only path to explore next (no sources, by the owner's
  choice). `check_map.py` gates every save (ladder shape, counts, no links in ladder or path,
  pearl numbers found in the material's text). Every map is saved to the "Learn" artifact
  (database collection `maps`; found by exact title + `learning-map` meta marker, created from
  `assets/learn.html`), not to the vault. Hand-offs (tutor, pubmed-research-note,
  bullet-reconstruct, concept-lab) are numbered options, never run unasked. One skill +
  `/learning-map [material]`.
- **egm-conductor** — master controller for Google's Elephant-Goldfish Model (`egm@egm`, a
  separate upstream plugin it depends on, never vendored): preflight → optional bootstrap →
  brainstorm → draft → Goldfish review + resolve → human approval gate → implement against the
  approved design doc → drift report, with progress in the project's `.egm-conductor/state.json`.
  EGM skills refuse the Skill tool (`disable-model-invocation`), so the conductor reads each EGM
  `SKILL.md` from the install path in `installed_plugins.json` (`scripts/egm_status.py`) and
  follows it, spawning the registered `egm:egm-*` agents. `--auto` skips only its own
  confirmations. Two skills (`conduct`, `status`), no commands.
- **visual-lock** — the look interview before a visual build, fourth gate in the alignment family
  (intent-lock owns what is wanted; this owns how it looks). Eight slots (canvas, layout, density,
  emphasis, colour, type, graphics, motion), each filled from the user's words, then a fixed look
  (a plugin's design contract, a project `DESIGN.md`, the page being edited), then a saved rule,
  and asked only when still open. Shape locked by the owner on 2026-11-10: choices are saved for
  reuse, and questions come in words first — picker, at most 2 rounds (1 after intent-lock), no
  recommendation on taste — with one sample sheet of 2–4 rendered variants (real content, true
  canvas size, at most two slots varied) only when words cannot settle a choice. The spec holds
  measurable values; the render is checked against it before delivery; 2–4 look lines go with
  the delivery. The user's choices and later corrections are saved to the "Look Book" artifact
  (database collections `rules` and `builds`; found by exact title + `visual-lock` meta marker,
  created from `assets/look-book.html` at the first save), never to plugin files. A rule is
  scoped to a kind of output and widens to `any` when the same choice is made for a second kind.
  One skill + `/visual-lock [what to build | show | forget | reset]`; slots, sample-sheet and
  Look Book references under `skills/visual-lock/references/`.
- **session-recap** — one page that says what was done in this session, made only on request
  (shape locked by the owner on 2026-11-10: one private artifact page per session; an HTML file
  when asked or when no Artifact tool exists). Order: outcome → still open → done (status,
  evidence, the check that verified it) → decisions (by the user, Claude or a default) → checks →
  what changed → what was asked. Accuracy contract: only what the session record shows, exact
  status words, "verified" only behind a check that passed, no praise, no secrets, no
  patient-identifiable detail. `build_recap.py` checks `recap.json` and renders nothing when a
  rule is broken (exit 0 required before delivery); English and Thai headings; no tables. No
  intent-lock gate and no vault filing. One skill + `/recap [focus | file]`; contract under
  `skills/session-recap/references/`, script tests under the plugin's `tests/`.

## Style

Follow the user's global CLAUDE.md. Keep plugins simple — solve the real task, no premature
abstraction. Prefer editing existing plugins over adding new files.

## Agent skills

### Issue tracker

Issues live in GitHub Issues (`safetymickky-ui/micky-psych-tools`) via the `gh` CLI;
external PRs are not a triage surface. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary — each role uses its canonical name (`needs-triage`, `needs-info`,
`ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
