---
description: "W0 smoke seed (S06-W0-1). Mined from skills/clinical-infographic/evals/evals.json id 3 (fidelity-safety-banner-and-unverified-gaps); prompt as section 4.1 words it (the old parenthetical became a fixture). scaffold.sh writes review.md, a synthetic sourced report built only from facts already in plugins/clinical-infographic/examples/ppgl-perioperative-management.html, with two absolute contraindications, doses with units and titration qualifiers, and one [unverified] figure. Graders assert today's contract on the written HTML: the critical-safety banner, both contraindications, numbers with their units, a self-contained file, and the Sources mapping in the footer. Section 4.1's no-dark-block grader is NOT seeded: today's references/infographic-template.html ships a prefers-color-scheme:dark block, so light-lock is target behaviour. Needs -- --allow-tools \"Write,Bash(node *)\". Quality pass 2026-09-26: the prompt names the output file so every file grader reads a literal path (the harness does not glob a file target — the old *.html graders threw on every run); new grader: the Step 2.6 fidelity script ran."
tags: [clinical-infographic, output, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Write, "Bash(node *)"]
max_turns: 40
timeout_seconds: 1200
---

Turn this review into an infographic. It lists two absolute contraindications, doses with
units and titration qualifiers, and one figure marked [unverified].
Save it as ppgl-infographic.html.
