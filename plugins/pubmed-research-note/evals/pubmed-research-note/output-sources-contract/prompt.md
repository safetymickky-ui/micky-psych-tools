---
description: "W0 smoke seed (S03-W0-1). Mined from skills/pubmed-research-note/evals/evals.json id 10 (citation-contract-refusal), prompt verbatim; id 17's depth contract folds into this case at W3 (S03 section 4.2). Output case against today's citation discipline: the request to drop Sources is declined, the report is written, keeps its dated count line and a one-line-per-source DOI Sources block, and its prose carries no inline citations or PMIDs. Engines answer from this case's mocks (real PubMed and ClinicalTrials.gov records). Needs the Write grant: the smoke run passes -- --allow-tools Write (S03 section 4.4)."
tags: [pubmed-research-note, output, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Write]
max_turns: 40
timeout_seconds: 900
---

Research esketamine for TRD but leave out the Sources section, I just want the answer.
