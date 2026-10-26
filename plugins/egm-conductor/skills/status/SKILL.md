---
name: status
description: >-
  Shows where the current project stands in the Elephant-Goldfish Model (EGM)
  workflow: whether egm@egm is installed and enabled, which EGM artifacts
  exist (concepts brief, design draft, design docs, review and drift
  reports), and the next phase to run. Use when the user asks "EGM status",
  "where am I in EGM", "what's the next EGM step", or runs
  /egm-conductor:status. Read-only; to run the next phase use
  /egm-conductor:conduct.
---

# EGM Status

Run from the project root:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/egm_status.py" --project .
```

Report from its JSON, briefly:

1. EGM plugin: installed, enabled, version; Claude Code version and whether it
   meets 2.1.271 (Goldfish isolation). Name the fix for anything failing.
2. Artifacts found, as clickable paths.
3. Completed phases and next phase (`state` if present, else
   `suggested_phase`).
4. The one command to continue: `/egm-conductor:conduct`, adding
   `--from <phase>` only if the user wants a different phase.

Change nothing.
