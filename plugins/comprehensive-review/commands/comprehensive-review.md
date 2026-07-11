---
description: Write a whole-disorder comprehensive review of the given psychiatric topic and file it to the vault
argument-hint: [disorder or topic]
---

Run the `comprehensive-review` skill now.

- `$ARGUMENTS` names the disorder or topic (e.g. `/comprehensive-review intermittent
  explosive disorder`) → seed the review with it.
- `$ARGUMENTS` empty → ask which disorder or topic to review, then proceed.

The skill owns the whole procedure — intent-lock gate → arc → per-section search → write →
file to the vault via vault-keeper. This command is only the manual trigger for it.
