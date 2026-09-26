---
description: "W0 smoke seed (S08-W0-1), re-seeded 2026-09-26 for the plugin.json-only version contract (CP-27). New case, prompt verbatim from section 4.1. scaffold.sh writes a fixture marketplace with stub validate/route/bump scripts. Output/process case against today's procedure: plugin.json and the skill are scaffolded under plugins/citation-format/, the catalog entry is registered with no version (the version lives in plugin.json only, 0.1.0 for a new plugin), validate.py runs after the files are written, and bump.py is not run for a new plugin. Section 4.1's no-command-dir grader is left for the W3 house shape. Unlike section 4.4's note on smoke cases, this one needs -- --allow-tools \"Write,Edit,Bash(python3 *)\" at the smoke run."
tags: [plugin-creator, output, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, "Bash(python3 *)"]
max_turns: 30
timeout_seconds: 900
---

Scaffold a new plugin called "citation-format": a skill that formats a DOI into APA or
Vancouver style. Category "productivity". Trigger phrases: "format this citation", "cite
this DOI". Use sensible defaults for anything else — don't ask me more questions.
