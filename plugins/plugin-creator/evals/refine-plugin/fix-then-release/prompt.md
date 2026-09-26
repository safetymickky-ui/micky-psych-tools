---
description: "W0 smoke seed (S08-W0-1), re-seeded 2026-09-26 for the plugin.json-only version contract (CP-27). New case, prompt verbatim from section 4.1. scaffold.sh writes a fixture marketplace whose gridgeist description has no Use-when clause. Process case against today's procedure: the fix is applied to SKILL.md, then the release goes through scripts/bump.py --write (today's tool; release.py is W3 target behaviour, not seeded) at patch level for a wording change: plugin.json moves to 0.1.1 and the plugin's CHANGELOG gains a heading, the catalog stays version-free, and no version is edited by hand. Needs -- --allow-tools \"Write,Edit,Bash(python3 *)\" at the smoke run."
tags: [refine-plugin, output, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Edit, "Bash(python3 *)"]
max_turns: 25
timeout_seconds: 900
---

Audit the gridgeist plugin's description for the missing Use-when clause, fix it, and
release the change.
