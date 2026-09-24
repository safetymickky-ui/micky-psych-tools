---
description: "W0 smoke seed (S08-W0-1). New case, prompt verbatim from section 4.1. scaffold.sh writes a fixture marketplace with stub validate/route/bump scripts. Output/process case against today's procedure: plugin.json and the skill are scaffolded under plugins/citation-format/, the catalog entry is registered at version 0.1.0 (today's parity rule), validate.py runs after the files are written, and bump.py is not run for a new plugin. Section 4.1's no-command-dir grader is left for the W3 house shape. Unlike section 4.4's note on smoke cases, this one needs -- --allow-tools \"Write,Edit,Bash(python3 *)\" at the smoke run."
tags: [plugin-creator, output, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, "Bash(python3 *)"]
max_turns: 30
timeout_seconds: 900
---

Scaffold a new plugin called "citation-format": a skill that formats a DOI into APA or
Vancouver style. Category "productivity". Trigger phrases: "format this citation", "cite
this DOI". Use sensible defaults for anything else — don't ask me more questions.
