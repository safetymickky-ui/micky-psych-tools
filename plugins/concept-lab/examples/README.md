# Examples

## `learning-rate.html` — computed mode

*When does gradient descent converge, and when does it blow up?*

- **Model** — least squares `y = w·x + b` on 40 seeded points, exact gradient, momentum update.
  The stability limit `2/λmax` and the closed-form optimum are computed from the data.
- **Main view** — the loss surface over (w, b) with the descent path on it.
- **Controls (3)** — learning rate (log slider, reaches divergence) · momentum · standardize x.
- **Presets (4)** — Converges · Too large (diverges, reported in the status line) · Unscaled x
  (the ravine: correct direction, too slow) · + momentum (same learning rate, reaches the optimum).
- **Checks** (`window.__lab.checks()`) — gradient vs finite difference, closed-form optimum is
  stationary, loss never rises inside the stable range, no non-finite value.

Verify it: `node ../scripts/verify.mjs learning-rate.html`
