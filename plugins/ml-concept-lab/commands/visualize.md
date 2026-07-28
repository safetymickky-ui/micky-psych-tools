---
description: Build an interactive, live-computed explorable (one self-contained HTML file) for a machine-learning, AI, or computer-science concept — intent-lock gated, driven and verified headless, filed to the vault via vault-keeper
argument-hint: [ML/AI/CS concept — e.g. "gradient descent", "self-attention", "Dijkstra"]
---

Run the `ml-concept-lab` skill now.

- `$ARGUMENTS` names a concept → that is the concept to build the lab for; the intent-lock
  Step 0 gate still runs to pick which of its several possible explorables this one is.
- `$ARGUMENTS` names a whole area ("transformers", "sorting") → treat it as a topic, and let
  the gate narrow it to one lab with one misconception to kill.
- `$ARGUMENTS` empty → ask which ML / AI / CS concept to build, then proceed.

The skill owns the whole procedure — intent-lock gate → pick the form from the concept's
family → write the lab spec (model, state, views, controls and the question each asks,
presets, invariants) → build the self-contained HTML (real algorithm running in the page,
linked views, transport controls, self-check panel, reduced-motion path) → drive it headless
and verify (console clean, every control to both extremes, every preset, self-checks passing,
fits one screen) → file it to the vault as an asset via vault-keeper. This command is only
the manual trigger.

If the request turns out to be a watch-only animation, a chart of the user's own data, or a
clinical topic, hand it to `concept-animation`, `dataviz`, or `clinical-infographic` instead
of building a weaker version here.
