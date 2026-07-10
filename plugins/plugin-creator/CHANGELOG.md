# Changelog

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
