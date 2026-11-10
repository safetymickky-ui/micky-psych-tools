# Build contract — how a lab page is made

SKILL.md decides *what* to build. This file decides *how*, so every lab feels like the same
instrument. The owner locked the shape on 2026-11-10 and corrected it the same day after the
first real page (backpropagation): he did not know where to look first, the page was not
step by step, the controls were below a long scroll, the view was crowded, and the look was
generic. Every rule below answers one of those.

## The default form is a guided walkthrough

A lab is a sequence of **steps**. The page opens on step 1. Each step shows one new thing,
points at it, and says in plain words what it is. The reader moves with **Back** and **Next**.

- **One focus per step.** The one or few elements the step is about are highlighted (the focus
  colour plus a soft halo). Everything else on the view is dimmed. The reader always knows
  where to look.
- **Progressive disclosure.** A value, label or part appears at the step that introduces it,
  not before. Step 1 never shows the finished picture.
- **The first steps introduce the parts** (what an input is, what a weight is) before anything
  is computed. The level decides how many such steps; a beginner gets one per kind of part.
- **5–14 steps.** Fewer is a single picture; more is two labs.
- **No Play button.** The reader sets the pace. Play is allowed only in watch mode, and in a
  free-play lab whose model runs for many iterations.
- **The last step sums up** in two sentences and offers the "what if" cases (below).

**Free-play form** (sliders that re-run the model) is the exception: only when the user asks
to "play with the parameters", or the level is advanced and the lesson is a regime change that
needs a continuous control. It follows every other rule here.

## The page — four parts, all on one phone screen

1. **Header** — the concept as a small `<h1>`, a step counter ("Step 3 of 12") and the phase bar.
2. **Main view** (`.view`) — one SVG or canvas.
3. **Step card** (`#status`, `aria-live="polite"`) — a short title, two or three short
   sentences, and for a step that computes something its formula and numbers.
4. **Bottom bar** — Back and Next, always visible, fixed to the bottom of the screen.

Nothing else. No readout row, no check chips, no legend block, no footer paragraph, no
shortcut list. The source line (see "Source line") sits inside the last step's card.

**No-scroll rule:** at 390×700 (a phone inside the app's viewer) the whole page fits and every
control can be reached without scrolling, at every step. Desktop gets the same column, centred.

```css
html { color-scheme: dark; }
body { margin: 0; background: var(--bg); color: var(--ink); }
.wrap { max-width: 560px; margin: 0 auto; min-height: 100svh;
        padding: 12px 16px calc(84px + env(safe-area-inset-bottom));   /* room for the bar */
        display: flex; flex-direction: column; gap: 10px; }
.view { width: 100%; aspect-ratio: 4 / 3; max-height: 44svh; }      /* never flex: 1 */
.bar  { position: fixed; left: 0; right: 0; bottom: 0; display: flex; gap: 10px;
        padding: 10px 16px calc(10px + env(safe-area-inset-bottom)); background: var(--bg); }
```

- The document starts with `<!DOCTYPE html>`, sets `lang`, and has
  `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- The view sizes itself with `aspect-ratio` and `max-height`. Never let it take "the rest" of
  a fixed-height wrapper; in an embedded frame that collapses it to zero.
- The step card has a fixed `min-height` sized for the longest step, so the bar and the view
  do not jump between steps.
- No sideways scroll at 390 px.

## The step card — enough to learn from, not more

- **Title:** two to five words naming the part or the action ("Hidden unit h1", "The error").
- **Body:** two or three short sentences. Say what the part *does* in common words, then one
  sentence of substance: why it is so, what it is called, or what it means for the next step.
  A term appears with its meaning the first time ("δ, the blame signal").
- **Formula** (when the step computes something): the rule in symbols, typeset as real maths,
  then the same rule with the live numbers under it. See "Maths" below.
- **Small figure** (optional, at most 104 px wide, floated right of the body): one curve or
  picture that the words lean on, such as the squash curve with this unit's point and slope.
  It is drawn from the model, like everything else.
- Body 15–16 px; nothing under 13 px. The card has a fixed `min-height` for the longest step.

## Maths — typeset and colour-coded

- **Symbols are typeset with native MathML** (`<math>`, `<mfrac>`, `<msub>`, `<mover>`), not
  plain text and not a library. It renders fractions, subscripts and hats properly on a phone
  and keeps the page self-contained. Font stack:
  `"STIX Two Math", "Cambria Math", "Latin Modern Math", math, serif`, about 19 px.
- **One colour per kind of quantity, the same in the formula, in the numbers under it and on
  the picture:** values of units and inputs in `--data`, weights in `--weight`, blame and
  gradients in `--update`, the result of the step in `--focus`, new values in `--ok`.
- **The number line** repeats the formula with the live values, coloured the same way, with
  the result in bold. It is HTML text, so it wraps on a narrow screen.
- A symbol in the formula carries the same name as its label on the picture (`w₁` in the
  formula is the line labelled `w₁`).
- Calculus notation (∂L/∂w) may appear once, next to the plain-words rule, never instead of it.

## An uncrowded view

- **At most 10 pieces of text are at full strength in the view at once** (names, values and
  labels together). A line shows one label at a time (its weight, or its gradient, never
  both); the calculation line carries the rest. Labels of dimmed lines are hidden, not dimmed.
- **No two labels overlap, and no label is covered by a shape.** Give every label an explicit
  position; do not rely on a formula along the edge. `verify.mjs` fails on overlapping text.
- Spread the parts over the whole view; leave at least a label's height between neighbours.
- Text in the view is at least 13 px on a 390 px screen (for a 400-wide `viewBox`, 15 units).
- Dimmed elements sit at about 30% opacity. Focus elements get the focus colour, a thicker
  stroke and a halo; the halo may pulse slowly, and does not move under reduced motion.

## A picture that carries meaning, and moves gently

- **Encode values in the drawing, and say so once in a card:** a circle fills to its value, a
  thicker line is a stronger weight. No decoration that means nothing.
- **Show direction.** When something travels (values forward, blame backward), the lines it
  travels on carry an arrowhead and slowly moving dots, coloured for what travels. The
  arrowhead stays under reduced motion; the dots stop.
- **Build the SVG once and restyle it per step** (classes, text, transforms). Then highlights,
  dimming and fill levels fade and grow between steps. A view rebuilt on every step cannot.
- **The card eases in** on each step (a short fade and rise). Buttons press down slightly.
- A **phase bar** under the title names the stages of the walkthrough ("Parts · Forward ·
  Backward · Update") and fills as the reader moves. It is orientation, not a control.

## Things to tap inside every step

A walkthrough is not a slide show. Every step gives the reader something to do besides Next.
The owner picked these three kinds on 2026-11-10; a lab has all three unless one cannot apply.

- **Tap a part of the picture.** Every unit and line is tappable (`data-part`, `role="button"`,
  `tabindex="0"`, an `aria-label`; lines get a wide transparent hit stroke). A pop-up names the
  part, gives its current value, and says in one or two sentences what it does *now*: text
  chosen from the computed model and from what the reader has been shown so far (a unit not
  yet worked out says which step fills it; a weight whose gradient is known says which way it
  would move the loss). The tapped part is outlined while its pop-up is open.
- **Tap a term or a symbol.** Terms in the card text are inline buttons (`class="term"`, dotted
  underline), and every symbol in a formula carries `data-term`. Tapping opens a short
  definition from one `GLOSS` table: a title and one to three sentences. A tap near a small
  symbol counts (nearest symbol within about 28 px).
- **Tap to reveal the calculation.** A step that computes something shows its formula first and
  a button (`id="reveal"`: "Tap to work it out"). Each tap reveals one line of the number
  work. The picture follows the reveal: the unit's value, a gradient label or a blame label
  appears when the line that produces it is revealed, not before. Next still works without
  revealing; a step the reader has passed counts as fully revealed.

**The pop-up** (`id="pop"`, one element, reused): it springs out of the thing tapped; a pop-up
about a picture part sits just under the picture so it never hides the picture; a pop-up about
a word sits above the word when there is room. It stays inside the screen, closes on a tap
anywhere, on Escape and on a step change, and has no buttons of its own.

**Lively motion, each with a meaning:**

- a pop-up and a revealed line spring in (overshoot easing, about 0.4–0.5 s);
- a result counts up to its value, in the card and in the picture;
- a unit bumps when it gets its value, and its fill rises;
- a dot travels along a line once when a value is passed forward or blame is passed back.

Under `prefers-reduced-motion` all of these happen at once, with no movement.

## Controls — few, and built for a thumb

- **Back / Next** (`id="prev"`, `id="next"`): real buttons, at least 48 px tall. Next is the
  primary button and the wider one, and shows the next step's title in small type under
  "Next". On the last step it reads "Start again".
- **Swipe** the card left for the next step and right for the previous one.
- **"What if" cases** (`<button data-preset="name">`, 0–4; three fit one row on a phone): shown
  on the last step only. "Start again" returns to the first case. Each
  changes the inputs and jumps back to the step where its effect first shows. Each is named
  for the situation ("Input is zero"), and the steps it affects say what changed and why.
- **Sliders and other inputs: none for a beginner or intermediate reader.** At most 2 in a
  free-play lab, full width, with the live value and unit shown.
- Every button and chip is at least 44×44 px, with a visible focus ring. No clickable `<div>`.
  A term inside a sentence is the one exception to the size rule. The reveal button may look
  like one line of text, but its hit area is still 44 px tall.
- Keyboard: → and Space go forward, ← goes back. Not printed on the page.
- Canvases that take input use pointer events and `touch-action: none` on the canvas only.

## The engine — one state, computed, then shown step by step

```js
const S = { k: 0, /* inputs of the current case */ };
function compute() { /* run the whole model for the current case; touch no DOM */ }
const STEPS = [ { focus: [...], title, body(m), calc(m) }, ... ];
function render()  { /* draw what steps 0..k have introduced; highlight STEPS[k].focus */ }
```

- The model is computed in full by `compute()`. A step only decides what is *shown*. Every
  number in a card or on the view is read from the computed model, never typed in.
- Step text that depends on the case is chosen by a computed condition ("the output equals the
  target, so the blame is 0"), not hard-coded per preset.
- A breakdown is a reported state: `NaN`, `Infinity` and `undefined` never reach the screen.
- Randomness goes through one seeded generator (`mulberry32`); `Math.random()` is not used.
- Authored mode uses the same shape: `CONTENT` items with a `source` each; a step shows one.

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

## Canvas or SVG

- **SVG** for structure with labels (networks, pathways, cards, small matrices). It is the
  default for a walkthrough, because parts must be highlighted and dimmed one by one.
- **Canvas** for fields, heat maps and more than about 200 marks. Scale it for the device
  pixel ratio (`canvas.width = cssWidth * devicePixelRatio`, then `setTransform(dpr,0,0,dpr,0,0)`).

## Checks — in the page, not on the page

```js
window.__lab = {
  mode: 'computed',            // 'computed' | 'authored' | 'mixed' | 'watch'
  steps: STEPS.length,         // walkthrough and watch pages
  at: () => S.k,               // the current step, counted from 0
  checks() { return [ { name: 'gradients vs finite difference', pass: true, detail: '3e-11' } ]; }
};
```

`checks()` asserts on the values actually running:

- **Gradients** — analytic against a central finite difference, as an **absolute** difference
  with a noise floor: `diff <= max(1e-6 * scale, 20 * EPSILON * max(1, |f|) / h)`.
- **Probabilities** — sum to 1 within 1e-9; finite with extreme inputs.
- **Closed forms** — where one exists, the running model agrees with it.
- **Monotone quantities** — what theory says cannot rise does not rise.
- **Sorting / search / paths** — output ordered and a permutation of the input.
- **Pharmacology** — the curve passes through its defining points and stays in its bounds.
- **Authored content** — every item has a `source`; every branch ends at an outcome.
- **Always** — no tracked value is non-finite unless the state says so.

A failing check is a bug in the lab. Fix the lab; never drop the check.

## Look — warm and hand-made, not a dashboard

The page should feel like a notebook by lamplight: warm, soft, quiet.

| Role | Token | Hex |
| --- | --- | --- |
| Background / card / raised / line | `--bg` / `--panel` / `--panel2` / `--line` | `#1f1a17` / `#2a2320` / `#352c28` / `#4d4139` |
| Text / muted / faint | `--ink` / `--muted` / `--faint` | `#f3e9dc` / `#cdbba8` / `#a08e7e` |
| Focus — where to look now | `--focus` | `#f0c36b` (honey) |
| Data — the inputs, the world, the patient | `--data` | `#9cc3b1` (sage) |
| Weights — the numbers that learning changes | `--weight` | `#e0a9bd` (dusty rose) |
| Change — the signal, the blame, the gradient | `--update` | `#e59572` (terracotta) |
| Good — the new value, correct, in range | `--ok` | `#b3cf8a` (moss) |
| Bad — broke, wrong, out of range | `--bad` | `#e57f6f` (clay red) |

- **Type:** headings and step titles in a serif stack
  (`"Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif`); body in the system sans
  stack. No monospace, no all-caps labels, no letter-spacing tricks.
- **Shapes:** radius 16–20 px on cards, pill buttons, strokes 2.5–3 px with round caps.
- **Not allowed:** neon cyan or violet, navy-black backgrounds, gradients, glows on text,
  glass panels, chips that look like status badges, emoji as icons.
- Each colour means one thing across the page. Colour is never the only signal: a focus also
  has a halo and a thicker stroke, and a bad state also has words.
- All text meets WCAG AA on its background.

## Motion and accessibility

- `prefers-reduced-motion: reduce` — no pulsing, no transitions. Nothing is lost, because the
  reader steps by hand anyway.
- The step card is the `aria-live="polite"` region.
- The view has `role="img"` and an `aria-label` that says what it shows.
- One `<h1>`; real buttons.

## Source line

One short sentence inside the last step's card, in the faint colour:

- **Computed:** "Everything here is computed in this page: `{model in a few words}`. `{Toy note.}`"
- **Authored:** "Written content, not computed. Source: `{report title, date}`."
- **Watch:** "Animation, illustrative." or "Animation from: `{report title, date}`."
- **Clinical content** adds: "Teaching aid, not a substitute for clinical judgment or local protocol."

## Watch mode

Same page and look. The step card is the scene caption, and the bar holds Back, Play/Pause
(`id="play"`), Next and Restart (`id="restart"`). See [animation-grammar.md](animation-grammar.md).

## Verify — `scripts/verify.mjs`

`node "${CLAUDE_PLUGIN_ROOT}/scripts/verify.mjs" ./lab.html [--out DIR]`

It finds Playwright itself (local or global) and the Chromium under
`PLAYWRIGHT_BROWSERS_PATH`; never run `playwright install`. For phone (390×700) and desktop
(1280×800), with motion on and reduced, it:

1. loads the page and collects console errors and network requests;
2. checks structure: doctype, viewport tag, one `<h1>`, `.view`, `#status`, `#prev`, `#next`,
   `window.__lab` with 5–14 steps, at most 2 inputs, at most 4 presets, no Play button outside
   watch mode;
3. walks every step with Next. At each step it checks the start state, taps `#reveal` until
   the calculation is complete and checks again after every line, taps one term and one part
   of the picture and checks the pop-up (it opens, has text, stays on screen, closes on
   Escape). In every state it fails on: an empty card; `NaN`, `Infinity` or
   `undefined` on screen; sideways scroll; on phone, a page taller than the screen or a button
   outside it; a touch target under 44 px; **two overlapping text labels in the view, or a
   label outside it or covered by a shape**; more than 10 pieces of full-strength text;
4. saves `shot-<size>-step<n>.png` for every step;
5. clicks every "what if" case, walks it to the end the same way, and saves its last step;
6. goes Back to step 1 and checks the page returns to its first state;
7. calls `window.__lab.checks()` for the base case and for every preset, and fails on any
   `pass: false`.

Exit code 0 means all of it held. Then look at the phone screenshots yourself, step by step:
is it clear where to look, does the card say what the highlight shows, is anything cramped?
The script cannot judge that.
