---
description: "W0 smoke seed (S07-W0-1). Mined from skills/empty-vault/evals/evals.json id 1 (move-verify-delete-in-order), prompt verbatim. Trigger positive on 'empty the vault'. The workspace is empty (no vault, no learn-hub), so today's move -> verify -> delete order means nothing may be deleted. Needs -- --allow-tools \"Write,Bash,AskUserQuestion\" (S07 section 4.4)."
tags: [empty-vault, trigger, smoke]
allowed_tools: [Read, Glob, Grep, Bash, Skill, AskUserQuestion]
max_turns: 15
---

Empty the vault.
