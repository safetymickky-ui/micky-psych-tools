# Build contract — how an explorable is made

SKILL.md decides *what* to build; this file decides *how*, so two labs from this plugin feel
like the same instrument. Every rule here exists because breaking it produced a lab that
either lied or stopped being usable.

## The anatomy

A lab has a fixed grammar. Order and role are fixed; not every part is large.

1. **Masthead** — the concept as an `<h1>`, and one subtitle line stating *the question this
   page answers* ("How does the learning rate decide whether training converges?").
2. **Stage** — the 2–3 linked views. This is the page; it gets the leftover vertical space.
3. **Readout** — the live state in numbers: step counter, cost counter, the two or three
   quantities the concept turns on. Monospace, tabular figures, fixed decimals, units. Also
   the `aria-live="polite"` region.
4. **Control deck** — transport (Play/Pause · Step · Reset), the parameter inputs each with
   its live value, the preset buttons, and the seed field.
5. **Self-check panel** — the invariant chips (below).
6. **Footer** — the honesty line (below).

## The engine — one state, one step, one render

```js
const S = { /* everything that defines a frame */ };   // the single source of truth
function reset()  { /* rebuild S from controls + seed  */ }
function step()   { /* advance S by exactly one unit; touch no DOM */ }
function render() { /* draw S; mutate nothing          */ }
```

- **`step()` is one unit of the algorithm** — one gradient update, one k-means iteration, one
  comparison, one node expansion. The step counter and the Step button mean exactly that unit,
  so a learner can count what they see.
- **Every view renders from `S` on the same tick.** Two views that can disagree are a bug.
- **The loop is a `requestAnimationFrame` driver with a logical rate** (`stepsPerSecond`, or
  `ticksPerFrame` for cheap steps) — the model's speed must not depend on the display's
  refresh rate. Pause stops the driver, never mid-`step()`.
- **A parameter change re-runs from a defined point.** Either `reset()` (most cases) or a
  documented hot-swap (changing the learning rate mid-descent is itself instructive — then say
  on screen that it changed at step *n*). Never leave state that no longer matches the controls.
- **Divergence is a reported state, not a crash.** After each step, if a tracked value is not
  finite (or exceeds a sane bound), set `S.status = 'diverged'`, stop the driver, keep the last
  finite frame on screen, and show a banner naming what blew up and at which step. `NaN` and
  `Infinity` are never rendered as if they were values. *This is a feature* — it is how the
  learner meets the failure regime.

## Determinism — one seeded PRNG, seed on screen

`Math.random()` is banned: it makes two runs incomparable, which destroys the whole point of a
control. Route all randomness through one seeded generator, expose the seed, and offer a
"new seed" button.

```js
function mulberry32(a) {                 // 32-bit, fast, good enough for teaching
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
let rng = mulberry32(S.seed);            // re-created in reset(), never elsewhere
const gauss = () => Math.sqrt(-2 * Math.log(1 - rng())) * Math.cos(2 * Math.PI * rng());
```

## Canvas or SVG — pick per view, never mix inside one

| Use **Canvas** for | Use **SVG** for |
| --- | --- |
| Redrawn every frame | Structure that changes on events |
| Heatmaps, contour fields, density, decision-boundary fills | Graphs, networks, trees, matrices (≲ 200 labelled cells) |
| More than ~200 marks (point clouds, particle sets) | Anything a screen reader must read |
| Trajectories accumulating over thousands of steps | Anything needing per-element `<title>`, focus, or hit-testing |

Canvas must scale for device pixel ratio or it renders blurry on every modern screen:

```js
function fit(cv) {                        // call on init and from a ResizeObserver
  const dpr = window.devicePixelRatio || 1, r = cv.getBoundingClientRect();
  cv.width = Math.round(r.width * dpr); cv.height = Math.round(r.height * dpr);
  cv.getContext('2d').setTransform(dpr, 0, 0, dpr, 0, 0);   // draw in CSS pixels
}
```

## Numbers on screen

- Fixed decimals and `font-variant-numeric: tabular-nums`, so a changing value doesn't jitter.
- Units always. A bare `0.03` is not a learning rate, a loss, or a second.
- **Log scale where the interesting range spans orders of magnitude** — learning rate, loss,
  epsilon, n. Slider position maps to `10 ** t`; the axis says it is logarithmic.
- Quantities the learner will compare across runs get the same precision every run.

## The self-check panel — the page proving it isn't faking

Assert the spec's invariants **on the values actually running**, every *k* steps, and render
each as a pass/fail chip with its measured residual (`✓ ∇ vs finite-diff  rel err 3.1e-9`).
A failing chip is a bug in your implementation — fix it; never hide the panel.

A menu, by family:

| Concept | Invariant to assert live |
| --- | --- |
| Anything with gradients | Analytic ∇ vs central finite difference, max relative error < 1e-5 |
| Softmax / attention / classifiers | Σp = 1 within 1e-9; still finite with logits of ±800 (max-subtraction present) |
| Gradient descent (convex loss) | Loss non-increasing whenever the step size is within the stable range |
| Least squares | Converged (w, b) matches the closed-form normal-equation solution |
| PCA | Components orthonormal; reconstruction error equals the tail eigenvalue sum |
| k-means | Objective non-increasing at every assign/update half-step |
| Sorting | Output is non-decreasing **and** a permutation of the input (a multiset check) |
| Search / shortest path | No edge can still be relaxed; equals brute force on a small instance |
| Graph traversal | Every reachable node visited exactly once |
| Hashing | Reported load factor equals occupied/size; lookups find every inserted key |
| Sampling / MCMC | Empirical mean → target mean within the stated tolerance as n grows |
| Q-learning / DP | Bellman residual → 0; greedy policy matches the value function |

## Complexity honesty

- Cost claims come from a **live counter** (comparisons, swaps, expansions, distance
  evaluations) — never from prose, and never inferred from wall-clock time in a browser.
- A 12-element demo does not demonstrate an asymptote. If the lab makes a growth claim, run the
  algorithm at several *n* and plot measured counts against the claimed curve.
- Worst-case input is reachable (already-sorted for naive quicksort, adversarial keys for a hash
  table). A lab that only ever shows the average case teaches the average case as if it were law.

## Performance budget

- 60 fps target: keep per-frame work under ~8 ms, measured, not assumed.
- **Recompute heavy fields only when their inputs change** — a contour/heatmap grid is a
  parameter-change job, cached to an offscreen canvas and blitted per frame.
- Preallocate; no per-frame array or object churn in the hot loop. Typed arrays for grids.
- Cap *n* so the worst case stays interactive, and show the cap rather than hiding it.
- No Web Workers, no libraries — self-containment first; keep the model small enough not to need them.

## Layout — fits one screen, no page scroll

Labs get embedded in fixed-height viewers (the Learn hub uses an iframe of
`height: calc(100svh - 6rem)`); a document taller than the viewport pushes the control deck
below the fold, which makes an *interactive* page unusable. So:

- `.wrap { height: 100dvh; display: flex; flex-direction: column }` — **never** `min-height`.
- The stage takes the remainder: `flex: 1 1 auto; min-height: 0`.
- Canvases size from their box (`width: 100%; height: 100%`) plus the `fit()` above, driven by a
  `ResizeObserver`; SVG stages use a ≈4:3 `viewBox` with `preserveAspectRatio="xMidYMid meet"`.
- Control deck and footer are fixed-height rows, never pushed.
- Verify at 1366×768 (Step 3.5) that `documentElement.scrollHeight <= innerHeight`.

## Palette — a dark instrument, roles not decoration

Each colour means one thing across every view; a learner who learns "amber = the parameters"
in view A must find it true in view B.

| Role | Token | Hex |
| --- | --- | --- |
| Background / panel / line | `--bg` / `--panel` / `--line` | `#0a1020` / `#0f1830` / `#22345c` |
| Text / muted / faint | `--ink` / `--muted` / `--faint` | `#eaf0ff` / `#a9b7d6` / `#7f8fb4` |
| Data — the inputs, the world | `--data` | `#3fd6dc` (cyan) |
| Model — parameters, weights, the thing being learned | `--model` | `#ffb84d` (amber) |
| Update — gradients, moves, the step just taken | `--update` | `#c39cff` (violet) |
| Good — converged, correct, check passed | `--ok` | `#5fe39a` (green) |
| Bad — diverged, error, check failed | `--bad` | `#ff6b6b` (red) |

Colour is never the only signal: every series also carries a label, a shape, or a dash pattern;
every failure state also carries a word. All text meets WCAG AA on its own background.

## Accessibility

- **Keyboard for everything.** Space = play/pause, → or `.` = step, R = reset, number keys =
  presets. Print the shortcuts on the page. All controls are real `<button>` / `<input>` with
  labels and visible focus rings.
- **`aria-live="polite"` readout** announcing the current step's key numbers (throttled — one
  announcement per second at most, not per frame).
- Informative SVG: `role="img"` with `<title>` and a `<desc>` stating what it shows. Decorative
  sub-elements `aria-hidden`.
- **`prefers-reduced-motion: reduce`**: no autoplay, no transitions, no trajectory tweening — the
  lab is fully usable by stepping, and no information exists only in motion.
- Real heading structure, `lang` set, no clickable `<div>`s.

## The honesty footer

One small block, always present:

> Everything on this page is computed live in your browser by the implementation in this file —
> `{one line naming the model}`. Random values come from seed `{seed}`; the same seed reproduces
> this run. {Toy-scale caveat: what it preserves, what it drops.} {Sources for any external
> number.} Rendered {date}.

## Verify recipe — drive it headless

Chromium is available (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`; never run
`playwright install`). If the installed `playwright` package expects a different browser build
than the one on disk, pass the binary explicitly —
`chromium.launch({ executablePath: '/opt/pw-browsers/chromium-<build>/chrome-linux/chrome' })` —
rather than downloading anything. Adapt selectors, keep the six checks.

```js
// verify.mjs — node verify.mjs ./lab.html
import { chromium } from 'playwright';
const url = 'file://' + process.argv[2].replace(/^\.\//, process.cwd() + '/');

for (const motion of ['no-preference', 'reduce']) {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1366, height: 768 }, reducedMotion: motion });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', m => m.type() === 'error' && errors.push(m.text()));
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(url);

  // 1. presets: load each, screenshot, confirm it renders what its name claims
  for (const b of await page.$$('[data-preset]')) {
    const name = await b.getAttribute('data-preset');
    await b.click(); await page.waitForTimeout(1200);
    await page.screenshot({ path: `shot-${motion}-${name}.png` });
  }

  // 2. every parameter to both extremes, including the broken end
  for (const r of await page.$$('input[type=range]')) {
    for (const end of ['min', 'max']) {
      const v = await r.getAttribute(end);
      await r.evaluate((el, v) => { el.value = v; el.dispatchEvent(new Event('input', { bubbles: true })); }, v);
      await page.waitForTimeout(900);
    }
  }

  // 3. transport: play → pause → step → reset, and the counter agrees
  await page.click('#play'); await page.waitForTimeout(1500); await page.click('#play');
  await page.click('#reset');
  const before = await page.textContent('#stepCount');
  await page.click('#step'); await page.click('#step');
  const after = await page.textContent('#stepCount');
  console.log(`[${motion}] steps ${before} -> ${after} (expect +2)`);

  // 4. self-checks pass in the page, 5. no NaN leaked, 6. no page scroll
  const report = await page.evaluate(() => ({          // browser scope — no Node variables in here
    checksFailed: [...document.querySelectorAll('[data-check]')].filter(e => e.dataset.pass !== 'true').map(e => e.textContent.trim()),
    nanOnScreen: /\b(NaN|Infinity|undefined)\b/.test(document.body.innerText),
    scrolls: document.documentElement.scrollHeight > window.innerHeight + 1,
  }));
  console.log(`[${motion}]`, report, 'console errors:', errors);
  await browser.close();
}
```

Green means: no console errors, no failing check, no `NaN` on screen, no page scroll, the step
counter honest, and every preset showing what it promises — in both motion modes.
