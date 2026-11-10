# Examples

## `backprop.html` — guided walkthrough, computed mode

*How does one backward pass find the gradient of every weight?*

- **Model** — a 2-2-1 network, sigmoid units, squared-error loss, no biases. `compute()` runs
  the forward pass, the backward pass and one update; the steps only decide what is shown.
- **13 steps** — inputs → weights → h1 → h2 → output → error → blame at the output → gradient
  of a weight → blame travels back → the same rule for each hidden unit → update → summary.
- **Focus** — each step highlights its nodes or lines in honey with a halo; the rest is dimmed.
- **Picture** — circles fill to their value, thicker lines are stronger weights, arrows and
  moving dots show values going forward and blame going backward. Built once, restyled per step.
- **Maths** — MathML formulas, colour-coded (values sage, weights rose, blame and gradients
  terracotta, result honey), with the live numbers under each; a small squash-curve figure
  shows each unit's point and slope.
- **Taps** — every unit and line opens a pop-up about what it is and does at this point; 16
  glossary terms and every formula symbol open a definition; each calculation is revealed
  line by line, and the unit's value, the gradients and the blame labels appear with it.
- **"What if" cases (3)** — Already right (blame 0, nothing moves) · Zero input (its weight
  gets gradient 0) · Big weights (a saturated unit lets almost no blame through).
- **Checks** — all 6 gradients vs finite difference, output inside 0–1, a step against the
  gradient does not raise the loss, all values finite.

Verify it: `node ../scripts/verify.mjs backprop.html`

There is no free-play, authored-mode or watch-mode example yet.
