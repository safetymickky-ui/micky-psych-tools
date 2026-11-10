# Build contract — how a lab page is made

SKILL.md decides *what* to build. This file decides *how*, so every lab feels like the same
instrument. The shape (phone first, minimal, dark, own artifact) was locked by the owner on
2026-11-10.

## The page — five parts, in this order

1. **Title** — the concept as an `<h1>`, and one line under it: the question the page answers.
2. **Main view** — one canvas or SVG. A second view only when the lesson is the link between
   two pictures.
3. **Status line** — one sentence in plain words about what is happening now, with at most two
   numbers ("Diverged at step 38: learning rate 1.2 is above the limit 1.0."). It is the
   `aria-live="polite"` region. It replaces the readout row, the banner, and the check chips.
4. **Controls** — presets first (2–4 chips), then at most 3 parameter controls, then transport
   (Play · Step · Reset) only when the model advances in time.
5. **Footer** — one or two short sentences (below).

**Watch mode** uses the same five parts: the main view is the animated SVG, the status line is
the scene caption, and the controls are only the player (Play · Prev · Next · Restart and a
scene indicator). See [animation-grammar.md](animation-grammar.md).

Nothing else is on the page. No readout row, no self-check panel, no keyboard legend, no seed
field, no speed selector, no side notes. If a number matters, it goes in the status line or on
the view as a label.

## Layout — phone first, scroll allowed

```css
html { color-scheme: dark; }
body { margin: 0; background: var(--bg); color: var(--ink); }
.wrap {
  max-width: 720px; margin: 0 auto;
  padding: 16px 16px calc(24px + env(safe-area-inset-bottom));
  display: flex; flex-direction: column; gap: 12px;
}
.view { width: 100%; aspect-ratio: 4 / 3; max-height: 52svh; }   /* never flex: 1 */
```

- The document starts with `<!DOCTYPE html>`, sets `lang`, and has
  `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- **The view sizes itself** with `aspect-ratio` and a `max-height`. Do not give the wrapper a
  fixed `height` and let the view take "the rest": in an embedded frame that collapses the
  view to zero height.
- **First-screen rule:** at 390×844 the title, the whole main view, and the first control are
  visible without scrolling. Everything else may sit below.
- No sideways scroll at 390 px. Preset chips wrap; they never overflow.
- Desktop gets the same column, centred. No second layout.
- Body text 16 px, secondary text no smaller than 13 px.

## Controls — built for a thumb

- Every button, chip, and slider has a hit area of at least **44×44 px**.
- Sliders are full-width, one per row: label on the left, live value with its unit on the right,
  the `<input type="range">` under them.
- Real `<button>` and `<input>` elements with labels and a visible focus ring. No clickable `<div>`.
- Presets are `<button data-preset="name">` and show `aria-pressed`. Loading a preset sets the
  controls, resets the run, and plays it (or shows its end state under reduced motion).
- Canvases that take input use **pointer events** (`pointerdown` / `pointermove` / `pointerup`)
  and `touch-action: none` on the canvas only, so the rest of the page still scrolls.
- Keyboard still works (Space = play/pause, → = step, R = reset) but is not printed on the page.
- Values that span orders of magnitude use a log slider (`value = 10 ** t`).

## The engine — one state, one step, one render

```js
const S = { /* everything that defines a frame */ };
function reset()  { /* rebuild S from the controls */ }
function step()   { /* advance S by exactly one unit; touch no DOM */ }
function render() { /* draw S; mutate nothing */ }
```

- `step()` is one unit of the model (one update, one iteration, one comparison, one dose).
- Every view renders from `S` on the same tick.
- The loop is `requestAnimationFrame` with a logical rate, so speed does not depend on the display.
- **A control change re-runs from a defined point** (normally `reset()`). No stale state.
- **A breakdown is a reported state.** When a tracked value stops being finite or passes a sane
  bound, set `S.status`, stop the loop, keep the last finite frame, and say what broke in the
  status line. `NaN`, `Infinity`, and `undefined` never reach the screen.
- **Randomness** goes through one seeded generator (`mulberry32` below), re-created in `reset()`.
  `Math.random()` is not used.

```js
function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
```

Authored mode uses the same engine: `S` holds which item is open, which branch was taken, or
where each card sits; `step()` is one user action; `render()` draws it. The content lives in
one `const CONTENT = [...]` array, each item with its `source` field.

## Canvas or SVG

- **Canvas** for anything redrawn every frame, fields and heat maps, more than about 200 marks.
  Scale it for the device pixel ratio or it is blurry on every phone:

```js
function fit(cv) {                         // call from render(), and from a ResizeObserver
  const dpr = window.devicePixelRatio || 1, r = cv.getBoundingClientRect();
  cv.width = Math.round(r.width * dpr); cv.height = Math.round(r.height * dpr);
  const ctx = cv.getContext('2d'); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  return { ctx, w: r.width, h: r.height };   // draw in CSS pixels
}
```

- **SVG** for structure with labels: graphs, trees, small matrices, pathways, cards.
- Heavy fields are recomputed only when their inputs change, cached, and blitted per frame.
- Labels drawn on a canvas are at least 12 px.

## Checks — in the page, not on the page

Every lab exposes its checks for the verify script and shows none of them:

```js
window.__lab = {
  mode: 'computed',                        // or 'authored', 'mixed', 'watch' (then also scenes: n)
  checks() { return [ { name: 'gradient vs finite difference', pass: true, detail: '3.6e-7' } ]; }
};
```

`checks()` asserts on the values actually running. What to assert:

- **Anything with gradients** — analytic gradient against a central finite difference, compared
  as an **absolute** difference with a noise floor: pass when
  `diff <= max(1e-6 * scale, 20 * EPSILON * max(1, |f|) / h)`. A relative error fails falsely at
  an optimum, where the gradient itself is zero.
- **Probabilities** — sum to 1 within 1e-9; still finite with extreme inputs.
- **Closed forms** — where one exists (least squares, a steady state, a half-life), the running
  model agrees with it.
- **Monotone quantities** — a loss or objective that theory says cannot rise does not rise.
- **Sorting / search / paths** — output is ordered and a permutation of the input; no edge can
  still be relaxed.
- **Pharmacology and dose–response** — the curve passes through its defining points (50% effect
  at EC50, half the concentration after one half-life) and stays inside its bounds (0–100%).
- **Authored content** — every item has a non-empty `source`; every branch ends at an outcome;
  every sortable card has exactly one correct place.
- **Always** — no tracked value is non-finite unless the status says so.

A failing check is a bug in the lab. Fix the lab; never drop the check.

## Palette — dark, and each colour means one thing

| Role | Token | Hex |
| --- | --- | --- |
| Background / panel / line | `--bg` / `--panel` / `--line` | `#0a1020` / `#0f1830` / `#22345c` |
| Text / muted / faint | `--ink` / `--muted` / `--faint` | `#eaf0ff` / `#a9b7d6` / `#7f8fb4` |
| Data — the inputs, the world, the patient | `--data` | `#3fd6dc` (cyan) |
| Model — the parameter, the thing the user sets | `--model` | `#ffb84d` (amber) |
| Change — the step just taken, the current selection | `--update` | `#c39cff` (violet) |
| Good — converged, correct, in range | `--ok` | `#5fe39a` (green) |
| Bad — broke, wrong, out of range | `--bad` | `#ff6b6b` (red) |

Colour is never the only signal: a series also has a label or a shape, and a bad state also has
words in the status line. All text meets WCAG AA on its background. System font stack only.

## Motion and accessibility

- `prefers-reduced-motion: reduce` — no autoplay and no transitions. A preset shows its end
  state at once, and Step still advances one unit. No information exists only in motion.
- The status line is `aria-live="polite"`, updated at most once per second while running.
- Canvases and informative SVG have `role="img"` and an `aria-label` that says what is shown.
- Real headings; one `<h1>`.

## Footer — one or two sentences

- **Computed:** "Computed live in this page: `{the model, in a few words}`. `{Toy-scale note if
  any.}`"
- **Authored:** "Authored content, not computed. Source: `{report title, date}`."
- **Watch:** "Animation, illustrative." or "Animation from: `{report title, date}`."
- **Clinical content, any mode,** adds: "Teaching aid, not a substitute for clinical
  judgment or local protocol."

## Verify — `scripts/verify.mjs`

`node "${CLAUDE_PLUGIN_ROOT}/scripts/verify.mjs" ./lab.html [--out DIR]`

The script finds Playwright itself (local or global install) and the Chromium under
`PLAYWRIGHT_BROWSERS_PATH`; never run `playwright install`. For each of phone (390×844) and
desktop (1280×800), with motion on and reduced, it:

1. loads the page and collects console errors;
2. checks structure: doctype, one `<h1>`, at most 3 parameter controls, 2–4 presets (watch
   mode: no controls or presets, the four player buttons, 3–8 scenes), nothing loaded from
   outside the file;
3. checks layout: no sideways scroll; on phone, the main view (`.view`) and the first control
   end inside the first screen; every button, chip, and slider is at least 44 px tall;
4. clicks every preset, waits, and saves `shot-<size>-<preset>.png` (watch mode: steps through
   every scene and saves `shot-<size>-scene<n>.png`);
5. moves every slider to both ends, toggles every checkbox, and runs Play → Pause → Step → Reset
   when those buttons exist;
6. after each action, fails on `NaN`, `Infinity`, or `undefined` in the page text;
7. calls `window.__lab.checks()` and fails on any `pass: false` or a missing `__lab`.

Exit code 0 means every check held in all four runs. The screenshots still need eyes: the
script cannot tell whether a preset shows what its name says.

The page must use these hooks so the script can find things: `.view` on the main view,
`data-preset` on preset buttons, `id="play"`, `id="step"`, `id="reset"` on transport buttons
that exist (watch mode: `id="play"`, `id="prev"`, `id="next"`, `id="restart"`), `id="status"`
on the status line, and `window.__lab`.
