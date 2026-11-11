# concept-lab

Builds one interactive page that teaches one concept by letting you drive it. Any field:
machine learning, statistics, computational psychiatry, pharmacology, clinical concepts.

- **A guided walkthrough.** The page opens on step 1; each step highlights one thing and
  explains it in beginner words; Back and Next sit at the bottom. No Play button, no sliders
  by default, a few "what if" cases on the last step.
- **Phone first, no scrolling, warm dark look.**
- **Computed mode** — the real model runs live in the page; nothing is drawn by hand.
- **Authored mode** — for concepts with no model (reveal, branch, sort, compare); labelled as
  authored, with its source.
- **Watch mode** — a scene-by-scene animation with captions and a player (`/animate`). This
  replaces the former `concept-animation` plugin.
- **Clinical facts** come only from a sourced report (session, vault, or generated first by
  comprehensive-review / pubmed-research-note).
- **Each lab is its own artifact.** Nothing is filed to the vault unless you ask.
- **Field packs** (since 1.4.0) — endocrinology, general psychiatry and computational
  psychiatry each have a pack under `skills/concept-lab/references/fields/`. For a concept in
  one of those fields the skill reads the pack first: it names the picture that fits, the
  misconception to remove, the "what if" cases, the default reader and where the field's
  clinical facts must come from. Same commands, same triggers. The packs hold no clinical
  numbers; cut-offs, doses and protocols still need a sourced report for each page.

Use: `/visualize <concept>` or `/animate <concept>`, or say "make an interactive page for …". Intent-lock runs first.

`scripts/verify.mjs` drives a finished page at phone and desktop size and fails on any
contract breach. `examples/backprop.html` is a worked lab.

Renamed from `ml-concept-lab` in 1.0.0, which also merged `concept-animation` into it.
