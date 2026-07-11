# MEMORY — micky-psych-tools living state

Fast-moving state for this marketplace. `CLAUDE.md` holds the stable conventions;
this file holds what changes. Update it whenever you release, add a plugin, or close
a milestone.

## Identity

- Personal Claude Code plugin marketplace. Owner: Thanawat Suharit (Micky).
- Remote: `origin` → https://github.com/safetymickky-ui/micky-psych-tools (**private**), branch `master`.
- Installed to Claude Code as marketplace `micky-psych-tools` (user scope).
- GitHub account `safetymickky-ui` (gh authed, `repo` scope).

## Current versions — 2026-07-11

| item                  | version |
| --------------------- | ------- |
| marketplace catalog   | 1.4.0   |
| pubmed-research-note   | 1.4.0   |
| intent-lock           | 0.4.0   |
| plugin-creator        | 0.3.0   |
| vault-keeper          | 0.2.0   |
| psych-paper-digest    | 0.1.0   |

A version MUST be identical in `plugins/<name>/.claude-plugin/plugin.json` and its
`.claude-plugin/marketplace.json` entry — if they drift, Claude Code silently offers no
update. Never hand-edit versions; bump with `python3 scripts/bump.py <plugin> patch|minor|major`.

## Plugins at a glance

- **pubmed-research-note** — clinical decision from primary literature; verdict-first,
  quantified, trial-registry-checked evidence reports. Default output pipeline: write md →
  show inline → file to vault as an artifact via vault-keeper; atomic notes on "atomize" only.
  ALWAYS runs intent-lock first as a mandatory Step 0 gate (explicit opt-out only — "just
  search"); the frame falls out of the interview, never inferred. Delegates vault writes to vault-keeper.
- **intent-lock** — pre-build alignment gate; interrogate a request to one reading, then build.
  Ships `intent-lock` (the interview) + `misread-capture` (the compounding misread ledger).
- **plugin-creator** — meta-plugin: `/new-plugin` scaffolds, `/refine-plugin` audits/refines,
  `/route` regenerates `ROUTING.md` and routes a request to the owning skill/command. Create and
  refine keep the router in sync automatically.
- **vault-keeper** — shared knowledge-vault manager for repo-root `vault/`; four jobs: init, save,
  index, query. The single place every skill's output lands.
- **psych-paper-digest** — watchlist literature surveillance; sweeps PubMed + ClinicalTrials.gov
  since `last_swept`, triages Act / Read / Suppressed, never adjudicates (Act items hand off to
  pubmed-research-note). Skill + `/digest [domain]`; state in `.psych-paper-digest.json`.

## Recent milestones

- **2026-07-11** — pubmed-research-note **1.4.0**: intent-lock is now a **mandatory Step 0 gate**
  before any search (was conditional — only fired on bare topics, frame-ties, or expensive runs).
  The frame now *falls out of the interview* instead of being inferred; the only bypass is an
  explicit opt-out ("just search" / "don't interview me"), which must be the user's own words —
  an opt-out may never be inferred from an ordinary "research this and file it." Prompted by an
  IED report that silently collapsed a "comprehensive review" request into an Rx-only decision.
  Rewrote Step 0, the intent-lock pairing section + trigger table (`references/intent-lock-pairing.md`),
  and the failure conditions; logged the misread to the intent-lock ledger as a new active prior.
  `route.py` regenerated. Then re-ran the IED vault artifact *through* the new gate: intent-lock
  locked an academic, whole-disorder frame, so the Rx-only artifact was replaced by a comprehensive
  academic review (`intermittent-explosive-disorder-review`) and its MOC promoted to a whole-disorder
  `Intermittent Explosive Disorder MOC`.
- **2026-07-10** — pubmed-research-note **1.3.0**: output is now a three-step default
  pipeline — write the md report, render it inline in the chat, then file it to the vault as
  an artifact via vault-keeper (was working-directory only, vault opt-in). Atomic-note
  distillation stays word-gated on "atomize"; failure conditions, Close, manifest + SKILL
  descriptions and ROUTING.md updated to match. First real report — the difficult-to-treat-
  depression Rx note — filed to the vault under a new `Depression — Treatment MOC`.
- **2026-07-10** — Added **psych-paper-digest 0.1.0** (fifth plugin; catalog → 1.4.0), built
  via the plugin-creator flow from a profile-based brainstorm. Fills the temporal gap next to
  pubmed-research-note: pull-based decision research vs scheduled watchlist surveillance —
  the carve-out named in pubmed's description since 1.2.0 now resolves to a real plugin.
- **2026-07-10** — Full four-plugin audit produced an 11-task improvement plan
  (`docs/superpowers/plans/2026-07-10-improve-all-plugins.md`), EXECUTED same day (branch
  `improve-all-plugins`, 22 commits). Fixed: intent-lock misread-ledger path collision,
  pubmed sandbox-only paths + vault-logic duplication (now delegates to vault-keeper via a
  producer→vault-keeper handoff), `route.py` routing on first sentence not Use-when, validator
  gaps. Released pubmed 1.2.0, intent-lock 0.4.0, plugin-creator 0.3.0, vault-keeper 0.2.0,
  catalog 1.3.0. `validate.py` now also checks per-skill evals + command/agent frontmatter
  descriptions. Merged to `master` (`57e470e`).

## Open threads

- Local branch `improve-all-plugins` still present — delete once its merge into `master` is confirmed.

## Health check

- `python3 scripts/validate.py` → must print `all checks passed`.
- `python3 scripts/route.py` → regenerates `ROUTING.md` (never hand-edit the router).
