---
description: "W0 smoke seed (S08-W0-1), re-seeded 2026-09-26 for the plugin.json-only version contract (CP-27). New case (refine-plugin has no evals.json), prompt verbatim from section 4.1. refine-plugin is model-invocable today (no disable-model-invocation), so the prompt names it in prose. scaffold.sh writes a fixture marketplace whose firecrawl plugin carries one planted mechanical blocker (SKILL.md frontmatter name fire-crawl in directory skills/firecrawl; the old plant, plugin.json 0.2.0 vs catalog 0.1.0, cannot exist once the catalog carries no version) and one quality gap (no Not-for clause). Graders assert today's two-tier audit report with both planted findings: the name mismatch inside the [BLOCKER] tier, ranked above [QUALITY], and the Not-for clause called missing, not just named. Read-only tools; nothing is applied without approval."
tags: [refine-plugin, trigger, smoke]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 15
---

Run refine-plugin on the firecrawl plugin — audit it for anything weak.
