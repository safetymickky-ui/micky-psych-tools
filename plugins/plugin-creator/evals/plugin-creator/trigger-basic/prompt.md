---
description: "W0 smoke seed (S08-W0-1). New case (plugin-creator has no evals.json; the templates/evals.json placeholder is not a suite), prompt verbatim from section 4.1. scaffold.sh writes a fixture marketplace so today's Step 1 can read the catalog's categories. Trigger positive: the skill fires and opens with today's fixed elicitation checklist (name, purpose, component type, trigger phrases, category). Read-only tools, as section 4.4 says of smoke cases."
tags: [plugin-creator, trigger, smoke]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 12
---

I want to add a plugin to the marketplace that turns a DOI into a formatted citation.
Scaffold it for me.
