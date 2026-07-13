---
description: Empty the shared vault into the Learn hub — move, verify, then delete; whole vault or one topic passed as argument
argument-hint: "[topic]"
---

Run the `empty-vault` skill now.

- `$ARGUMENTS` empty → drain the WHOLE vault.
- `$ARGUMENTS` names a topic/MOC (e.g. `/empty-vault panic-disorder`) → drain only that
  topic's artifacts, notes, and assets; every other MOC's content stays untouched.

The skill owns the whole procedure — resolve both roots → inventory + manifest → hand each
report to learn-hub's `digest-report` skill → verify the Supabase landing → double-gated
delete (git-committed + explicit confirmation) → prune MOCs and rebuild `index.md`. This
command is only the manual trigger for it.
