---
description: Summarize what was done in this session as one page (a private artifact, or an HTML file)
argument-hint: [focus | file]
---

Run the `session-recap` skill now.

- `$ARGUMENTS` is empty → recap the whole session and publish it as a private artifact.
- `$ARGUMENTS` names a part of the work (`/recap the data cleaning`) → the page holds only
  that part and says what was left out.
- `$ARGUMENTS` is `file` (or holds "html file", "don't publish") → build the HTML file and
  send it; do not publish.

The skill owns the whole procedure: collect the session record → write `recap.json` →
`build_recap.py` (checks, then renders) → publish or send the file → reply with the link and
the open items. This command is only the manual trigger.
