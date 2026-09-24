---
description: "W0 smoke seed (S09-W0-1). Mined from skills/firecrawl/evals/evals.json id 1 (positive-trigger-scrape-known-url), prompt verbatim. Trigger positive. Today's Path A with a known URL goes straight to scrape and keeps the exact URL with the output. Read-only tools (section 4.4 grants none), so the run can describe the scrape but not execute it."
tags: [firecrawl, trigger, smoke]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 10
---

Scrape https://stripe.com/pricing into clean markdown for me.
