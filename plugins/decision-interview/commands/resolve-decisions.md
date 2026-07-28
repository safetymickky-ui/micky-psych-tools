---
description: Sweep the current task for every open decision that needs the user and resolve them all in one batched interview
argument-hint: [task or scope]
---

Run the `decision-interview` skill now.

- `$ARGUMENTS` names a task or scope (e.g. `/resolve-decisions the migration plan`) →
  sweep just that.
- `$ARGUMENTS` empty → sweep the whole current task.

The skill owns the whole procedure — sweep → triage → order → picker interview →
decision ledger → resume. This command is only the manual trigger for it.
