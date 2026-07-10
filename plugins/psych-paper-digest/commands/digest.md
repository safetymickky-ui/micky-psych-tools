---
description: Run the psych-paper-digest sweep now — all watchlist domains, or one domain passed as argument
argument-hint: [domain]
---

Run the `psych-paper-digest` skill now.

- `$ARGUMENTS` empty → sweep every domain in `.psych-paper-digest.json`.
- `$ARGUMENTS` names a watchlist domain (e.g. `/digest child-adhd`) → sweep only that
  domain; every other domain's `last_swept` stays untouched.
- No config file yet → run the skill's init flow first (elicit the watchlist, confirm the
  drafted queries, write the config), then run the inaugural sweep in the same turn.

The skill owns the whole procedure — window → sweep → triage → render → mark swept. This
command is only the manual trigger for it.
