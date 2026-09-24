---
description: "W0 smoke seed (S04-W0-2). Mined from skills/comprehensive-review/evals/evals.json id 5 (depth-over-compression), prompt verbatim; section 4.2 folds id 5 into this case. Output/process case against today's contract: searches before writing, runs the ClinicalTrials.gov check, writes one md file whose header carries 'PubMed N · trials N · sections N', a one-line-per-source DOI Sources block, and no inline citations. The report/1 frontmatter grader of section 4.1 is target behaviour (W2) and is not seeded. Engines answer from this case's mocks (real records). The file needs the Write grant (-- --allow-tools Write)."
tags: [comprehensive-review, output, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Write]
max_turns: 60
timeout_seconds: 1800
---

Comprehensive review of treatment-resistant schizophrenia — make it the reference I actually study from, not a summary.
