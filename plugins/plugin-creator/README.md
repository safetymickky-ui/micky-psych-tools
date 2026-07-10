# plugin-creator

Meta-plugin: the lifecycle toolkit for **this marketplace itself**. It scaffolds new
plugins into `micky-psych-tools`, audits and refines existing ones, and recommends which
skill or command already owns a given request.

## Commands

- **`/new-plugin`** — scaffold a brand-new plugin: elicit a fixed checklist, generate the
  chosen component skeleton (skill/command/agent/hooks/MCP wiring), register it in
  `marketplace.json`, and validate.
- **`/refine-plugin`** — audit and refine an existing plugin or skill, then bump + validate.
- **`/route`** — recommend which skill/plugin fits a request, from the generated
  `ROUTING.md`.

## Skills

- **`plugin-creator`** — the elicit-and-scaffold skill behind `/new-plugin`.
  Marketplace-aware: writes into `plugins/<name>/`, registers the catalog entry, runs
  `scripts/validate.py`, and regenerates `ROUTING.md`.
- **`refine-plugin`** — the audit-and-refine skill behind `/refine-plugin`. Reports
  findings in two tiers (mechanical blockers, quality/triggering), applies only the fixes
  the user approves, then bumps via `scripts/bump.py` and validates.

## Standards and templates

Every plugin this toolkit scaffolds or refines is judged against:

- `skills/plugin-creator/references/authoring-rules.md` — the mechanical rules
  `scripts/validate.py` actually enforces (single source of truth), plus the
  description-writing recipe.
- `skills/refine-plugin/references/audit-checklist.md` — the quality tier: judgment
  checks a rule-passing plugin can still fail (commands, catalog coverage, router sync,
  plugin docs).
- `skills/plugin-creator/references/templates/` — the skeleton files `/new-plugin` fills
  in: `plugin.json`, `marketplace-entry.json`, `SKILL.md`, `command.md`, `agent.md`,
  `hooks.json`, `.mcp.json`, `evals.json`.

Both commands end the same way: regenerate the router (`python scripts/route.py` — never
hand-edit `ROUTING.md`), stage the changes, and stop before commit — the user always
reviews and commits.

## Install

```
/plugin marketplace add <owner>/micky-psych-tools
/plugin install plugin-creator@micky-psych-tools
```

Local development:

```
/plugin marketplace add .
/plugin install plugin-creator@micky-psych-tools
```
