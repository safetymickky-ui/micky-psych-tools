---
description: "W0 smoke seed (S07-W0-1). Mined from skills/vault-keeper/evals/evals.json id 3 (init-skipped-when-populated), prompt verbatim. scaffold.sh builds a populated vault (index.md exists and lists a MOC; the other dirs hold only .gitkeep). Today's init job: 'populated means vault/index.md exists', so init is skipped: index.md is neither rewritten nor overwritten and nothing new is scaffolded. Needs -- --allow-tools \"Write,AskUserQuestion,Bash(ls *),Bash(mkdir *),Bash(git status *),Bash(git log *),Bash(git diff *)\" so the no-write graders bite."
tags: [vault-keeper, output, smoke]
allowed_tools: [Read, Glob, Grep, Write, Bash, Skill]
max_turns: 12
---

Initialize the vault for me.
