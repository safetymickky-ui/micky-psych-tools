# Changelog

## 0.3.0 — 2026-07-10

- **Router routes on triggers, not summaries.** `route.py` now fills the routing cue from a
  component's `Use when…` clause (falling back to the first sentence) instead of always the
  first sentence, so rows carry real triggers rather than noun-phrase summaries. `/route` always
  regenerates `ROUTING.md` before reading it — the old "looks stale vs `marketplace.json`"
  heuristic could never detect an edited skill description.
- **Standards reconciled with the validator.** `authoring-rules.md` and `audit-checklist.md`
  now match what `validate.py` actually enforces (skill/agent description length, per-skill
  evals JSON, command/agent frontmatter description presence), with mechanical vs quality tiers
  labelled honestly. The checklist gained command, catalog-coverage, router-sync, and
  README/CHANGELOG-existence checks.
- **Template & scaffolding.** The SKILL template's `description` is a short placeholder again
  (the authoring recipe moved to a comment) so a literal fill can't produce a length-passing
  but useless trigger; added an `evals.json` template. The category prompt reads distinct
  categories from `marketplace.json` at runtime instead of a hardcoded snapshot.
- **Docs.** Deduped the router-refresh / stop-before-commit prose across both skills; added
  `README.md`. The catalog description now advertises `/route`.

## 0.2.0

Added the request router: `scripts/route.py` generates `ROUTING.md` (Use-when → plugin →
route) from the catalog and every plugin's skills/commands/agents. New `/route` command
reads it to recommend the right skill or command. `/new-plugin` and `/refine-plugin` rerun
`route.py` so the router never drifts out of sync with edited descriptions.

Routing matches against Use-when clauses, and `/route` always regenerates `ROUTING.md`
before reading it, so an edited-but-unrun description still routes correctly.

## 0.1.0

Initial lifecycle toolkit — two skills:

- `plugin-creator` (`/new-plugin`) scaffolds a new plugin into the marketplace: elicit a
  fixed checklist, generate the chosen component skeleton (skill/command/agent/hooks/MCP
  wiring), register the catalog entry in `marketplace.json`, and validate.
- `refine-plugin` (`/refine-plugin`) audits and refines an existing plugin or skill in two
  tiers (mechanical blockers, quality/triggering), applies only the approved fixes, then
  bumps via `scripts/bump.py` and validates.
