---
description: "W0 smoke seed (S07-W0-1). Mined from skills/empty-vault/evals/evals.json ids 1 and 3 (move-verify-delete-in-order, scoped-empty-leaves-rest-untouched): section 4.1's prompt and fixture, plus a marketplace marker (today's Step 0 resolves the vault beside .claude-plugin/marketplace.json) and a git commit, so the only gate left standing is verification. learn-hub's digest-report skill is not loaded, so no report can verify its landing, and today's contract (move -> verify -> delete, never reordered) means nothing is deleted: the artifact, index.md and the MOC survive, no delete command runs, and nothing is written into the Learn checkout. The drain_plan.py tool_order graders of section 4.1 are target behaviour (W2) and are not seeded. Needs -- --allow-tools \"Write,AskUserQuestion,Bash(ls *),Bash(mkdir *),Bash(git status *),Bash(git log *),Bash(git diff *)\"."
tags: [empty-vault, process, smoke]
allowed_tools: [Read, Glob, Grep, Write, Bash, Skill, AskUserQuestion]
max_turns: 20
timeout_seconds: 600
---

The learn-hub checkout for this run is at ./fixture-learn-hub (relative to cwd).

/empty-vault panic-disorder
