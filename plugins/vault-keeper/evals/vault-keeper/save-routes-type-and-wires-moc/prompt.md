---
description: "W0 smoke seed (S07-W0-1). Mined from skills/vault-keeper/evals/evals.json id 1 (save-routes-type-and-wires-moc); prompt verbatim except that the report the user refers to now names its fixture file, which scaffold.sh writes (an eval run starts in an empty workspace). scaffold.sh also writes a marketplace marker and an empty vault scaffold. Graders assert today's save job: Step 0 resolves vault/ beside .claude-plugin/marketplace.json; the report lands in artifacts/ under a kebab name, the one-idea note in notes/, a '<Topic> MOC.md' is created (never 'MOC — <Topic>') and reachable from index.md, and nothing is written outside vault/. Needs -- --allow-tools \"Write,Bash,AskUserQuestion\" (S07 section 4.4)."
tags: [vault-keeper, trigger, output, smoke]
allowed_tools: [Read, Glob, Grep, Write, Bash, Skill]
max_turns: 20
timeout_seconds: 600
---

Save this to the vault: a full evidence report on lithium for suicide prevention (long document, read top-to-bottom: ./lithium-suicide-prevention.md), and separately this one-idea summary: 'Lithium reduces suicide attempts in bipolar disorder, NNT ~15 over 18 months.'
