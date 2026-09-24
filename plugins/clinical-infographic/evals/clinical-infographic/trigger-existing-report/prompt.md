---
description: "W0 smoke seed (S06-W0-1). Mined from skills/clinical-infographic/evals/evals.json id 1 (renders-existing-vault-report-and-files-asset), prompt verbatim. Trigger positive on 'make an infographic'. The PPGL report the prompt names does not exist in this run (no session report, no vault, no upstream plugin loaded), so today's Step 0 forbids rendering from unsourced memory: no HTML may be written. The smoke run passes -- --allow-tools \"Write,Bash(node *)\" (S06 section 4.4), which is what makes the no-render grader bite."
tags: [clinical-infographic, trigger, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Write, "Bash(node *)"]
max_turns: 25
timeout_seconds: 600
---

Make an infographic of the PPGL perioperative management report.
