# The explanation contract — interaction, fidelity, accessibility

`vscode-shell.md` says what it looks like. This says what it must *do* and what it may
never *claim*.

## The three mandatory modes

Every explainer ships all three. A file missing one is not done.

### 1. Linked line ↔ explanation highlighting

The core interaction. The code is divided into **annotated ranges**; each range has
exactly one explanation card.

- **Data model:** every gutter/line element carries `data-range="6-11"`; its card carries
  the same `data-range`. One shared id space, nothing else to keep in sync.
- **Hover** either side → both sides get the soft highlight (`--vsc-line-highlight` on the
  code, a raised border + accent left-edge on the card).
- **Click / Enter** either side → sticky selection: the pair stays lit, the other pane
  scrolls it into view (`scrollIntoView({block:'nearest'})`), and the step counter jumps
  to that range.
- Cards are real `<button>`s (or `tabindex="0"` with a key handler), reachable by Tab, and
  the selected card carries `aria-current="step"`.
- Ranges may nest or overlap only if the code genuinely nests; when they do, the innermost
  wins on hover.

### 2. Step-through walkthrough

A debug session, not a slideshow. **Steps run in execution order, which is often not
source order** — that divergence is frequently the single most valuable thing the artefact
teaches, so never reorder the steps back into source order for tidiness.

- Toolbar: **Restart · Prev · Play/Pause · Next** (see the debug toolbar in
  `vscode-shell.md`). Play auto-advances at a readable pace (≈ 4.5 s or reading-time,
  whichever is longer) and stops at the last step.
- The current step's range gets the `--vsc-stackframe` yellow band plus the `▶` gutter
  arrow; its card scrolls into view and takes `aria-current="step"`.
- **Keyboard:** `→`/`N` next, `←`/`P` prev, `Space` play/pause, `R` restart, `Home`/`End`
  first/last. Bind on `document`, but never swallow keys while focus is in a text field.
  List the map in a visible `?`/legend affordance or the footer — an unlisted shortcut
  does not exist.
- The live step index is announced: an `aria-live="polite"` region carrying
  `Step 3 of 8 — lines 12-17`.
- 4–12 steps. Fewer than 4 means the code did not need a walkthrough; more than 12 means
  the ranges are too fine — merge them.

### 3. Structure / flow diagram

Inline SVG in the bottom panel's `FLOW` tab. Pick the diagram the code's shape asks for:

| Code shape | Diagram |
| --- | --- |
| branching, loops, early returns | **control flow** — decision diamonds, loop back-edge |
| several functions calling each other | **call graph** — who invokes whom, recursion as a self-edge |
| transform pipeline, stream, reducer | **data flow** — value in, shape at each stage, value out |
| lifecycle, state machine, async phases | **state diagram** — states as nodes, events on edges |
| declarative config / schema / markup | **containment tree** — nesting, not sequence |

Rules:

- Every node carries `data-range` from the same id space. Clicking a node selects that
  range and jumps the walkthrough to it; the node matching the current step is highlighted
  as the walkthrough advances. **A diagram that is not cross-linked is decoration** — the
  whole reason it is here is that it is a second index into the same code.
- Hand-authored inline SVG. No Mermaid, no D3, no runtime layout engine. Use a `viewBox`
  and `preserveAspectRatio` so it scales inside the panel.
- Labels are real `<text>` in `--font-ui`, ≥ 11px, AA contrast. Edges get arrowheads via a
  `<marker>`; back-edges are visibly curved so a loop reads as a loop.
- `<title>` on the `<svg>` and on each node, plus `role="img"` and an `aria-label`
  summarising the flow in one sentence for the diagram as a whole.

## The optional fourth mode — variable state trace

A `STATE` tab beside `FLOW`, holding a table of how key values change across the steps.

- **Include it** for algorithmic code — loops, accumulators, recursion, sorting,
  reducers, retry counters. **Leave it out** for config, schema, markup, glue, and
  straight-line I/O; an empty or trivially-constant table is worse than no tab.
- Rows reveal as the walkthrough advances; the current step's row is highlighted.
- **Values must be real.** Either you actually executed the code, or you hand-traced it
  deterministically. Label the tab's caption accordingly — *traced by hand from the
  source* or *from an actual run* — and never present a guess as an observed value. If a
  value depends on I/O, randomness, or the clock, write it as a symbol (`t₀`, `<response>`)
  rather than inventing a number.

## Fidelity — what the explanation may never do

The artefact looks authoritative; that is exactly why it must be exact.

- **Explain only what the code does.** Not what it appears to intend, not what a
  well-written version would do. If behaviour depends on a caller, a config value, or a
  library's semantics you have not read, say so in the card — `depends on how X is
  called` is a complete and honest answer.
- **Name defects; never smooth them.** An off-by-one, a swallowed exception, a race, an
  unawaited promise, a resource never closed — flag it in its card (a `warn` treatment,
  and `.t-inv` on the token when it is a single token). The reader is trusting this to
  learn the code, so a bug narrated as a feature is the worst failure mode here.
- **No invented runtime values.** See the state-trace rule above; it applies to prose too.
- **Uncertainty is written down**, inline, as `[unverified]` — never quietly dropped and
  never smoothed into confident prose.
- **The code is reproduced verbatim.** Byte-for-byte, including whitespace, blank lines,
  and comments. Do not reformat, re-indent, rename, shorten, or "fix" it on the way in. If
  it is truncated for length, say so on screen at the cut point.

## Escaping — the failure that silently corrupts the artefact

Inside the code pane, `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;` **before** wrapping in
token spans. Miss this on a generic (`List<int>`), a JSX tag, an HTML snippet, or a `<<`
shift and the browser eats the code. Check the rendered output, not the source you wrote.

## Progressive enhancement and accessibility

- **No-JS is a real state.** Rendered without JavaScript, the page still shows the full
  code, correctly highlighted, and every explanation card in order, and the diagram.
  Build it that way — everything visible by default, and JS adds an `is-interactive` class
  on `<html>` that switches on stepping and linked highlighting.
- **`prefers-reduced-motion`** — no auto-advance, no scroll animation, no transitions.
  Stepping still works; it just cuts instead of eases.
- **Colour is never the only signal.** The current step is the yellow band *and* the `▶`
  arrow *and* the step counter *and* `aria-current`.
- Semantic headings, a visible focus ring (`--vsc-focus`, 2px, never `outline: none`),
  landmarks on the two panes, AA contrast everywhere outside the code tokens.
- **Self-contained, always.** One `.html` file: inline `<style>`, inline `<script>`,
  inline SVG. No external CSS, JS, font, image, or CDN; no `fetch`. It must open offline,
  identically, anywhere.

## Fit and responsiveness

- Fits **1366 × 768** with no page scroll: `100svh` grid, panes scroll internally.
- Below ~900px the panes stack — code first, explanation second, panel last — and the
  linked highlighting still works.
- Long lines wrap or scroll horizontally **inside the code pane only**; the document body
  never scrolls sideways.

## Verify before you hand it over

Render it headless, screenshot it, and check with your eyes:

1. Initial frame: chrome intact, nothing clipped or overlapping, no page scrollbar at
   1366×768.
2. Step through **every** step: the right range lights, the card scrolls in, the flow node
   highlights, the counter advances, the last step stops cleanly.
3. Hover and click a card and a diagram node: both directions link.
4. Reload with JS disabled: code and all cards still readable.
5. Re-read the code in the rendered page against the source, character by character, for
   escaping and truncation damage.

This is a layout and wiring check. It is never a substitute for re-reading the
explanation against the code.
