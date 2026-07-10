# MEMORY — micky-psych-tools living state

Fast-moving state for this marketplace. `CLAUDE.md` holds the stable conventions;
this file holds what changes. Update it whenever you release, add a plugin, or close
a milestone.

## Identity

- Personal Claude Code plugin marketplace. Owner: Thanawat Suharit (Micky).
- Remote: `origin` → https://github.com/safetymickky-ui/micky-psych-tools (**private**), branch `master`.
- Installed to Claude Code as marketplace `micky-psych-tools` (user scope).
- GitHub account `safetymickky-ui` (gh authed, `repo` scope).

## Current versions — 2026-07-10

| item                  | version |
| --------------------- | ------- |
| marketplace catalog   | 1.3.0   |
| pubmed-research-note   | 1.2.0   |
| intent-lock           | 0.4.0   |
| plugin-creator        | 0.3.0   |
| vault-keeper          | 0.2.0   |

A version MUST be identical in `plugins/<name>/.claude-plugin/plugin.json` and its
`.claude-plugin/marketplace.json` entry — if they drift, Claude Code silently offers no
update. Never hand-edit versions; bump with `python3 scripts/bump.py <plugin> patch|minor|major`.

## Plugins at a glance

- **pubmed-research-note** — clinical decision from primary literature; verdict-first,
  quantified, trial-registry-checked evidence reports; vault notes on request only. Chains to
  intent-lock when a request carries no decision; delegates vault writes to vault-keeper.
- **intent-lock** — pre-build alignment gate; interrogate a request to one reading, then build.
  Ships `intent-lock` (the interview) + `misread-capture` (the compounding misread ledger).
- **plugin-creator** — meta-plugin: `/new-plugin` scaffolds, `/refine-plugin` audits/refines,
  `/route` regenerates `ROUTING.md` and routes a request to the owning skill/command. Create and
  refine keep the router in sync automatically.
- **vault-keeper** — shared knowledge-vault manager for repo-root `vault/`; four jobs: init, save,
  index, query. The single place every skill's output lands.

## Recent milestones

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
