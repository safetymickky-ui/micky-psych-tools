---
description: Build one interactive page for one concept (any field) — phone-first, minimal, dark; the real model runs live, or authored content when there is no model; published as its own artifact
argument-hint: [concept — e.g. "gradient descent", "receptor occupancy", "defense mechanisms"]
---

Run the `concept-lab` skill now.

- `$ARGUMENTS` names a concept → build the lab for it. The intent-lock Step 0 gate still runs,
  to pick the one question the page answers.
- `$ARGUMENTS` names a whole area ("transformers", "antipsychotics") → treat it as a topic and
  let the gate narrow it to one lab.
- `$ARGUMENTS` empty → ask which concept, then proceed.

The skill owns the whole procedure: intent-lock → mode (computed or authored) and form → lab
spec → build to the contract → `scripts/verify.mjs` → publish as its own artifact. This
command is only the manual trigger.

For a watch-only animation use `/animate` (the same skill, watch mode). A static clinical
summary goes to `clinical-infographic`, and a chart of the user's own data to `dataviz`.
