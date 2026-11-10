# concept-lab

Builds one interactive page that teaches one concept by letting you drive it. Any field:
machine learning, statistics, computational psychiatry, pharmacology, clinical concepts.

- **Phone first, minimal, dark.** One main view, 1–3 controls, 2–4 presets, one status line.
- **Computed mode** — the real model runs live in the page; nothing is drawn by hand.
- **Authored mode** — for concepts with no model (reveal, branch, sort, compare); labelled as
  authored, with its source.
- **Watch mode** — a scene-by-scene animation with captions and a player (`/animate`). This
  replaces the former `concept-animation` plugin.
- **Clinical facts** come only from a sourced report (session, vault, or generated first by
  comprehensive-review / pubmed-research-note).
- **Each lab is its own artifact.** Nothing is filed to the vault unless you ask.

Use: `/visualize <concept>` or `/animate <concept>`, or say "make an interactive page for …". Intent-lock runs first.

`scripts/verify.mjs` drives a finished page at phone and desktop size and fails on any
contract breach. `examples/learning-rate.html` is a worked lab.

Renamed from `ml-concept-lab` in 1.0.0, which also merged `concept-animation` into it.
