---
description: "W0 smoke seed (S09-W0-1). Mined from skills/firecrawl/evals/evals.json id 2 (positive-trigger-deliverable-gated-by-intent-lock), prompt verbatim. Output/process case for Path C. Today's step 1 is 'confirm the workflow and final artifact with the user' (through intent-lock, which is not loaded in an isolated run), before any evidence is collected; so the run ends asking for that confirmation, not with a finished brief. Section 4.1's tool_order grader (intent-lock before firecrawl) needs intent-lock loaded and its OPTIONAL-fallback grader is the W1/W3 target; neither is seeded. Read-only tools."
tags: [firecrawl, output, smoke]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 20
---

Use firecrawl to build me a competitive intel brief on the top teletherapy platforms.
