# Examples

## `backprop.html` — guided walkthrough, computed mode

*How does one backward pass find the gradient of every weight?*

- **Model** — a 2-2-1 network, sigmoid units, squared-error loss, no biases. `compute()` runs
  the forward pass, the backward pass and one update; the steps only decide what is shown.
- **13 steps** — inputs → weights → h1 → h2 → output → error → blame at the output → gradient
  of a weight → blame travels back → the same rule for each hidden unit → update → summary.
- **Focus** — each step highlights its nodes or lines in honey with a halo; the rest is dimmed.
- **"What if" cases (3)** — Already right (blame 0, nothing moves) · Zero input (its weight
  gets gradient 0) · Big weights (a saturated unit lets almost no blame through).
- **Checks** — all 6 gradients vs finite difference, output inside 0–1, a step against the
  gradient does not raise the loss, all values finite.

Verify it: `node ../scripts/verify.mjs backprop.html`

There is no free-play, authored-mode or watch-mode example yet.
