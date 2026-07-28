# micky-psych-tools — plugin marketplace

Personal Claude Code plugin marketplace. Single owner: Thanawat Suharit (Micky).
This repo is BOTH the marketplace and the home of every plugin in it.

**`CLAUDE.md` holds stable conventions; `MEMORY.md` holds living state** (current
versions, recent milestones, open threads). Read `MEMORY.md` first to know where things
stand, and update it whenever you release, add a plugin, or close a milestone.

## Routing — pick the right tool first

Before acting on any request one of these plugins could serve, **route it first**:
consult the generated `ROUTING.md` (or run `/route "<request>"`) and hand off to the
skill or command it names — do not do the work ad hoc when a plugin already owns it.
If nothing fits, run `/new-plugin` to build one.

`ROUTING.md` is a GENERATED artifact — never hand-edit it. `scripts/route.py` writes it
from the catalog + every plugin's components, and `/new-plugin` and `/refine-plugin`
rerun it automatically, so the router never drifts.

## Layout

```
.claude-plugin/marketplace.json   # catalog — every plugin listed here
plugins/<name>/
  .claude-plugin/plugin.json       # plugin manifest (name, version, author, keywords)
  .mcp.json                        # optional — MCP servers (referenced from plugin.json)
  skills/<skill>/SKILL.md          # skill(s): frontmatter (name, description) + body
  commands/<cmd>.md                # optional — slash commands
  agents/<agent>.md                # optional — subagents
scripts/validate.py                # full marketplace + plugin validation
scripts/bump.py                    # version bump in BOTH manifest + catalog
scripts/route.py                   # generates ROUTING.md from the catalog + every plugin's components
ROUTING.md                         # generated router — never hand-edit
vault/                             # shared knowledge vault — managed by vault-keeper
```

## Hard rules (these have bitten before)

- **Version lives in two files.** A plugin's version in `plugins/<name>/.claude-plugin/plugin.json`
  MUST equal its entry in `.claude-plugin/marketplace.json`. If they drift, Claude Code sees
  no version change and silently offers no update. NEVER edit a version by hand — run
  `python3 scripts/bump.py <plugin> patch|minor|major` (it edits both, then validates).
- **SKILL.md description cap:** hard limit 1024 chars; aim well under. Too short (<~200) triggers
  unreliably. The description is the ONLY thing that decides when the skill fires — invest in it.
- **`name` is kebab-case** and must match: plugin dir name == plugin.json name == marketplace entry.
  Skill frontmatter `name` == its directory name.
- **`source` is a relative path** (`./plugins/<name>`) in the marketplace entry.

## Workflow for adding / changing a plugin

1. Scaffold under `plugins/<name>/` following the layout above.
2. Add the entry to `.claude-plugin/marketplace.json` (name, source, version, description, category, keywords).
3. `python3 scripts/validate.py` — must print `all checks passed`.
4. Regenerate the router: `python3 scripts/route.py` (any change to a skill/command description
   alters ROUTING.md; `/new-plugin` and `/refine-plugin` do this automatically).
5. Bump with `scripts/bump.py` when releasing, never by hand.
6. Commit (conventional commits: `feat:`, `fix:`, `refactor:`…). One logical change per commit.
7. Update `MEMORY.md` (versions table, milestones) when releasing.

## Health check — run before every commit

- `python3 scripts/validate.py` — must print `all checks passed`.
- `python3 scripts/route.py` — regenerates `ROUTING.md` after any skill/command description change.

## Plugins

- **pubmed-research-note** — clinical decision from primary literature; verdict-first evidence
  reports whose shape follows the decision, not the topic; runs intent-lock first to build a
  bespoke decision brief (no fixed frames); five engines (PubMed backbone, CT.gov, Open
  Library, Wikipedia, firecrawl for general-web documents — labels, guidelines); delegates
  vault saving to vault-keeper.
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
  breadth: a ten-section arc from definition to controversies, never collapsed into a
  treatment-only report. Intent-lock is the mandatory Step 0 gate; searches PubMed +
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
