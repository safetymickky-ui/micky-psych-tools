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
  reports; chains to intent-lock when a request carries no decision; delegates vault saving to
  vault-keeper.
- **intent-lock** — pre-build alignment gate; interrogate a request to one reading, then build.
- **plugin-creator** — meta-plugin: scaffolds new customized plugins into THIS marketplace
  (manifest + skill/command/agent/hooks/mcp-wiring skeleton + catalog entry + validation), and
  refines existing ones. Two skills (`plugin-creator`, `refine-plugin`) + three commands
  (`/new-plugin`, `/refine-plugin`, `/route`); elicit-first fixed checklist; auto-register +
  auto-validate, stops before commit. `/route` regenerates ROUTING.md and routes a request to
  the owning skill or command. Authoring rules + templates under its
  `skills/plugin-creator/references/`.
- **vault-keeper** — shared knowledge-vault manager for the repo-root `vault/`; four jobs: init,
  save, index, query. Other plugins delegate vault writes to it rather than writing vault files
  themselves.
- **psych-paper-digest** — watchlist-driven literature surveillance; windowed PubMed +
  ClinicalTrials.gov sweeps triaged into Act / Read / Suppressed, rendered as a read-once
  digest. Triage only, never adjudication: Act items hand off to pubmed-research-note; vault
  saves delegate to vault-keeper. One skill + `/digest [domain]` command; config + `last_swept`
  state in `.psych-paper-digest.json`.

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
