---
description: Create a watch-only animation of a concept (concept-lab watch mode) — scene by scene with captions and a player; intent-lock gated; clinical facts only from sourced reports; published as its own artifact
argument-hint: [concept, or path/title of a sourced report]
---

Run the `concept-lab` skill now, in **watch mode**.

- `$ARGUMENTS` names a concept → animate it. The intent-lock Step 0 gate still runs, to lock
  the one "aha" the animation must produce.
- `$ARGUMENTS` points at an existing report (a vault title, a file path, or "the report
  above") → animate from that sourced content.
- `$ARGUMENTS` empty → ask what concept to animate, then proceed.

The skill owns the whole procedure: intent-lock → source the content → storyboard → build to
the contract and the animation grammar → `scripts/verify.mjs` → publish as its own artifact.
