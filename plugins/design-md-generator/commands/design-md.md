---
description: Generate a spec-valid DESIGN.md from a website URL, a text brief, a codebase path, or a reference kit to remix
argument-hint: [url | brief | project path | kit to remix]
---

Run the `design-md-generator` skill now.

- `$ARGUMENTS` is a URL: **site** mode, extract real tokens from that site.
- `$ARGUMENTS` is a path, or "this project": **codebase** mode.
- `$ARGUMENTS` names a brand or kit to adapt ("like Linear but warm"): **remix** mode.
- Any other `$ARGUMENTS`: a **brief**.
- `$ARGUMENTS` empty: ask which of the four sources to use, then proceed.

The skill owns the whole procedure: gather evidence, then build tokens, write prose, lint
and report. This command is only the manual trigger.
