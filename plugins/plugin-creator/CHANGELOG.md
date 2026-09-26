# Changelog

## 0.3.1 — 2026-09-26

- **The SKILL template no longer loads as a skill.** `references/templates/SKILL.md` is now
  `SKILL.template.md`. Some Claude surfaces search `skills/` deeper than one level and load
  any `SKILL.md` they find, so the unfilled template appeared as a live skill named
  `skill-name` whose description was the `{{placeholder}}` text: listing noise and a
  random-trigger risk. The scaffold step maps `SKILL.template.md` to
  `skills/<skill>/SKILL.md`.
- **The rule is enforced.** `scripts/validate.py` now fails on a `SKILL.md` (any case)
  outside `skills/<skill>/`. `authoring-rules.md` states `SKILL.md` as a reserved file name,
  replacing the false note that nested folders are never loaded as skills; refine-plugin's
  blocker tier and the audit checklist list the rule.
- **The version lives in `plugin.json` only.** The scaffold registers a catalog entry with
  no `version` (step 4 and `templates/marketplace-entry.json`), and `authoring-rules.md`
  drops the entry/plugin.json parity rule. refine-plugin's "version parity" blocker now
  means a `version` found in the catalog entry, and its release step runs
  `bump.py <plugin> <level> --write` and fills the CHANGELOG heading it adds; before, it
  ran without `--write`, a dry run that wrote nothing.
- **W0 smoke cases re-seeded to that contract.** Fixture catalogs carry no version; the
  stub `validate.py` and `bump.py` mirror the real scripts; graders check that no catalog
  `version` is written and that `plugin.json` reaches `0.1.1`; the explicit-invoke case
  plants a frontmatter name mismatch instead of a parity break.

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
