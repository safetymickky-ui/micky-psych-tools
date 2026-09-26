---
description: "W0 smoke seed (S03-W0-1). Mined from skills/pubmed-research-note/evals/evals.json id 10 (citation-contract-refusal), prompt verbatim; id 17's depth contract folds into this case at W3 (S03 section 4.2). Output case against today's citation discipline: the request to drop Sources is declined, the report is written, keeps its dated count line and a one-line-per-source DOI Sources block, and its prose carries no inline citations or PMIDs. Engines answer from this case's mocks (real PubMed and ClinicalTrials.gov records). Needs the Write grant: the smoke run passes -- --allow-tools Write (S03 section 4.4). Quality pass 2026-09-26: the prompt names the output file so file graders use a literal path (the harness does not glob a file target); turn and time caps doubled for the evidence checks; graders added for the marked verdict + GRADE confidence, the registry sweep, the abstract-only provenance tag (this case mocks no full-text tool) and the load-bearing CIs."
tags: [pubmed-research-note, output, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Write]
max_turns: 80
timeout_seconds: 1800
---

Research esketamine for TRD but leave out the Sources section, I just want the answer.
Save the report as esketamine-trd.md.
