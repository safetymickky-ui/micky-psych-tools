---
description: Recommend which marketplace skill/plugin fits a request, from ROUTING.md
argument-hint: [describe what you want to do]
---

Read `ROUTING.md` at the marketplace repo root — it is the generated router
(`scripts/route.py` builds it from the catalog and every plugin's components).

Before consulting the table, always run `python scripts/route.py` first (fall back to
`python3`) — it is idempotent and cheap, and it is the only way to pick up edited skill
descriptions (which change ROUTING.md without touching marketplace.json).

If `$ARGUMENTS` is empty, ask the user for one line describing what they want to do.

Match `$ARGUMENTS` against the **Use when** column of the Quick index, then confirm
against the plugin's fuller entry under **Plugins**. Recommend the single best route
(and at most one runner-up if it is genuinely close). For each recommendation give:

- the **Route** exactly as ROUTING.md lists it — a `skill` name or a `/command`,
- one line on why it fits the request,
- how to trigger it: a skill fires from its description (just proceed with the task,
  or name it), a command is run with its slash.

If nothing matches, say so plainly and suggest `/new-plugin` to build one — do not
force a poor fit.
