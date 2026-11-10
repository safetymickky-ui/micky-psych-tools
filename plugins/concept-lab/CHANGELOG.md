# Changelog

## 1.2.0 — 2026-11-10

Second round of owner feedback on the backpropagation page: right track; make the picture and
the interaction more appealing, typeset and colour the maths, add a little more substance.

- **Maths:** formulas in native MathML, colour-coded by kind of quantity, with a matching
  number line under each; labels on the picture use the same symbols and colours.
- **Step card:** two or three sentences (was one or two), a formula block, and an optional
  small figure drawn from the model.
- **Picture:** values and strength encoded in the drawing (fill level, line thickness),
  direction arrows with moving dots, SVG built once so changes animate, a phase bar.
- **Interaction:** swipe the card, the Next button previews the next step's title, the card
  eases in.
- New palette role `--weight`. Example `examples/backprop.html` rebuilt to these rules.

## 1.1.0 — 2026-11-10

Owner feedback on the first real page (backpropagation): no guide to where to look, not step
by step, controls below a long scroll, a crowded view, a generic look.

- **Guided walkthrough is the default form.** The page opens on step 1; each step has one
  highlighted focus, the rest is dimmed, and parts appear only when introduced. Back/Next
  replace Play/Step/Reset.
- **Step card** replaces the status line: a short title, one or two beginner sentences, one
  calculation line.
- **No scrolling on a phone.** Four parts on one screen (390×700); Back/Next in a fixed bottom
  bar.
- **Fewer controls.** No sliders by default (free-play with at most 2 only on request); 0–4
  "what if" cases, on the last step.
- **Uncrowded view rules:** explicit label positions, one label per line, at most 10 pieces of
  full-strength text.
- **Warm look:** new warm dark palette, serif headings, pill buttons; neon and dashboard chrome
  are not allowed.
- **verify.mjs** now walks every step and every case, and fails on a page taller than the
  phone screen, off-screen controls, overlapping / covered / clipped labels, too much text, and
  a Play button in a walkthrough. `window.__lab` gains `steps` and `at()`.
- Example replaced: `examples/backprop.html` (the 1.0.0 `learning-rate.html` free-play example
  no longer fits the contract and was removed).

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
