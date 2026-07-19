---
description: Create a self-contained HTML animation that illustrates a concept — intent-lock gated, clinical facts only from sourced reports, filed to the vault via vault-keeper
argument-hint: [concept, or path/title of a sourced report]
---

Run the `concept-animation` skill now.

- `$ARGUMENTS` names a concept → that is the concept to animate; the intent-lock Step 0
  gate still runs to lock its one reading.
- `$ARGUMENTS` points at an existing report/review (a vault title, a file path, or "the
  report above") → animate from that sourced content.
- `$ARGUMENTS` empty → ask what concept to animate, then proceed.

The skill owns the whole procedure — intent-lock gate → source the content (clinical facts
only from a sourced report; generate one via comprehensive-review / pubmed-research-note
when none exists) → storyboard → build the self-contained HTML animation (scene controller,
captions, reduced-motion fallback) → render & verify scene by scene → file to the vault as
an asset via vault-keeper. This command is only the manual trigger.
