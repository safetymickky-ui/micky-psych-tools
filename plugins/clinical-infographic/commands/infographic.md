---
description: Render a professional medical summary infographic (self-contained HTML) for clinical reference from a sourced report, review, or topic
argument-hint: [topic, or path/title of a review or research report]
---

Run the `clinical-infographic` skill now.

- `$ARGUMENTS` names a clinical topic, or points at an existing report/review (a vault title,
  a file path, or "the report above") → seed the infographic with it.
- `$ARGUMENTS` empty → ask what to turn into an infographic (a topic, or a specific
  report/review), then proceed.

The skill owns the whole procedure — acquire **SOURCED** content (reuse an existing
comprehensive-review or pubmed-research-note artifact, or run those plugins FIRST to generate
it; never fabricate clinical facts) → render the self-contained, print-ready HTML infographic
with color-coded columns, stat tiles, and a critical-safety banner → file it to the vault as an
asset via vault-keeper. This command is only the manual trigger.
