# Changelog

## 1.0.0 — 2026-11-10

Redesign, with the shape picked by the owner in a two-round picker interview.

- **Renamed** `ml-concept-lab` → `concept-lab`. `/visualize` stays.
- **Scope:** any concept (was ML/AI/CS only). Clinical content follows the sourced-report rule.
- **Three modes:** computed (model runs live), authored (reveal / branch / sort / compare)
  for concepts with no runnable model, labelled as authored, and watch (scene-by-scene
  animation).
- **Merged `concept-animation` into this plugin** as watch mode: `/animate` and the animation
  grammar moved here; watch pages follow the same phone-first contract and `verify.mjs`. The
  old TMS example, built to the fixed-height layout, was dropped (it is in git history).
- **Page:** phone first, one column, scroll allowed, 44 px touch targets; minimal (one main
  view, at most 3 controls, 2–4 presets, one status line, one-line footer); dark kept. The
  readout row, self-check chips, shortcut legend, seed field and long footer are gone.
- **Destination:** each lab is published as its own artifact; no vault filing unless asked.
- **Checks** moved off the page into `window.__lab.checks()`.
- **Fixed** (defects ml-concept-lab-1…9): the fixed-height layout that collapsed the view in
  embedded frames; the verify recipe that could not find a global Playwright and tested one
  viewport (now `scripts/verify.mjs`, phone + desktop, both motion modes); the relative-error
  gradient check that failed falsely at an optimum; the contradictory clinical routing; the
  wrong example path; the doctype-less example; missing evals.
- Pattern catalog: added statistics, pharmacology and clinical quantities, computational
  psychiatry, and the authored-mode patterns. Example rebuilt as `examples/learning-rate.html`.

## 0.1.0 — initial release

no contemporaneous entry; see `git log` around this version.
