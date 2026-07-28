# Examples — worked output of `ml-concept-lab`

A reference lab that shows the plugin's contract in practice. Open the `.html` in any browser
(fully self-contained — no network, no libraries) and drive it; the `.preview.png` is a static
capture of the failure preset.

## `learning-rate-and-conditioning.html` — optimization & training dynamics

*Learning rate & conditioning — when does gradient descent converge?* The misconception it
kills: **"training diverged, so the model is wrong."** It usually isn't. The step size or the
conditioning is wrong, and the same model converges once you fix either.

### What is actually computed in the page

Nothing on screen is drawn to look like gradient descent — all of it is gradient descent:

- **The model** — least squares on 40 generated points, `L(w,b) = mean((w·x + b − y)²)`,
  evaluated from the data's five moments so the whole surface can be swept cheaply.
- **The loss field** — the heat map and contour bands are `L` evaluated on a grid, not an ellipse
  drawn to look like one; change the data and the picture changes with it.
- **The update** — heavy ball, `v ← μv − η∇L; θ ← θ + v`, with the exact analytic gradient.
- **λmax and the stability bound** — the Hessian's largest eigenvalue and `2/λmax` computed from
  the data, shown live in the readout. That bound is the whole lesson, and it is a *number the
  page derived*, not a rule of thumb printed on it.
- **The optimum ★** — the closed-form normal-equation solution, so the learner can see how far
  descent still is from an answer that exists in one step for *this* model and in no steps at all
  for a real one.

### The three linked views

**Parameter space** (loss field + trajectory + optimum) — the mechanism. **Data space** (points,
fitted line, residuals) — the consequence: what this (w, b) actually claims about the world.
**Loss vs step**, log-scaled, with the best-possible loss as a dashed floor — the verdict. All
three render from one state object on the same tick.

### The controls, and the question each one asks

| Control | Question |
| --- | --- |
| learning rate (log, 1e-5 → 3.2) | Does step size decide *whether* it converges, or only how fast? |
| momentum | What does inertia buy in a narrow valley? |
| batch | What does the noise in stochastic gradients actually do to the path? |
| noise σ | Where does the best possible loss sit, and why isn't it zero? |
| standardize x | Why does rescaling an input change everything? (λmax: **2.0** standardized vs **903.9** raw) |
| seed | Is this run a fact or an accident? |
| click the loss surface | Does where you start decide where you end? |

### The five presets, and the failure regimes they reach

1. **converges** — η 0.1, standardized: straight in, gradient numerically zero at step 102.
2. **too small, stalls** — η 1e-4: monotone, correct, and still nowhere near the optimum at the
   3000-step cap. Correct and useless are different failures.
3. **too large, diverges** — η 1.2 against a computed bound of 1.000: the loss climbs a straight
   line on a log axis to 1e12 and the run is halted at step 38 with a banner naming the cause.
   `NaN` never reaches the screen — the state is *reported* as diverged.
4. **unscaled x, ravine** — the same algorithm on raw x: bound collapses to 0.0022, the descent
   plunges along the steep direction and then crawls, still 1.09 from the optimum at the cap.
5. **ravine + momentum** — identical learning rate, μ = 0.9: **7.5e-4** from the optimum instead
   of 1.09. Same problem, same step size, one line of extra state.

### The self-check panel — the page proving it isn't faking

Four chips, asserted live on the running values: the analytic gradient against a central finite
difference (absolute difference, because near a stationary point a *relative* error measures
floating-point cancellation rather than correctness — a bug this example's own verification pass
caught); the closed-form optimum being a stationary point of the same loss; the monotone-descent
guarantee while η is under the bound (and an explicit *n/a* when momentum, mini-batching, or an
oversized η puts the run outside the regime where the guarantee holds); and that no non-finite
value is being rendered as a number.

### Verified, not assumed

Driven headless in both motion modes (`prefers-reduced-motion: no-preference` and `reduce`):
every preset loaded and screenshotted, every range control pushed to both extremes, the step
counter checked against the number of Step clicks, reset checked to return to zero, all four
self-checks green, no console errors, no `NaN` on screen, and no page scroll at 1366×768.
Under reduced motion there is no autoplay — presets run to completion instantly and stepping
still works, so nothing exists only in motion.
