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
- **intent-lock** — pre-build alignment gate; interrogate a request to one reading, then build.
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
- **concept-animation** — creates an animation that illustrates a given concept: one
  self-contained HTML file (inline CSS/SVG/JS, no external anything) that unfolds the concept
  scene by scene with synchronized captions, player controls, and a mandatory reduced-motion
  fallback. Motion must explain, never decorate — every animated property makes a nameable
  claim, and the final frame is a complete labelled summary. Intent-lock is the mandatory
  Step 0 gate; any concept is in scope, but clinical facts come only from sourced reports
  (session / vault / generated first via comprehensive-review or pubmed-research-note) —
  never invented. Files the animation as an asset via vault-keeper. One skill + `/animate
  [concept-or-source]` command; motion grammar under its
  `skills/concept-animation/references/`.
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
- **ml-concept-lab** — the interactive sibling of concept-animation, for machine-learning, AI,
  and computer-science concepts: one self-contained HTML **explorable** in which the real
  algorithm runs live in the page and the learner drives it (visualization + interaction +
  animation in one artifact). Prime directive: **the picture is computed, not drawn** — no
  canned frames, seeded randomness with the seed on screen, a live self-check panel asserting
  the algorithm's invariants (gradients vs finite differences, closed forms, sort/path
  correctness), and controls that must reach the regime where the algorithm breaks. Intent-lock
  is the mandatory Step 0 gate; verification means *driving* the page headless, not just
  screenshotting it; files the HTML as an asset via vault-keeper. One skill + `/visualize
  [concept]` command; build contract + a per-family pattern catalog under its
  `skills/ml-concept-lab/references/`, worked lab under `examples/`. Boundary: watch-only
  animations and clinical topics stay with concept-animation, charts of the user's own data
  with dataviz.
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
