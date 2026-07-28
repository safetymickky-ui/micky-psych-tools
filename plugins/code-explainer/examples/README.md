# code-explainer — worked example

`async-retry-with-backoff.html` explains **`withRetry`**, a 45-line async retry helper with
exponential backoff, full jitter and `AbortSignal` support. One self-contained file: inline
CSS, inline JS, inline SVG, no fonts, no CDN, no `fetch`.

**Open it:** double-click the `.html`, or `open async-retry-with-backoff.html`. It works
offline and it works with JavaScript off.

## What it demonstrates about the contract

- **All three mandatory modes.** Linked line ↔ card highlighting over 11 annotated ranges;
  a 12-step debug-style walkthrough (Restart · Prev · Play · Next, full keyboard map); a
  hand-authored control-flow SVG in the panel's `FLOW` tab, cross-linked to the same ranges.
- **A fourth mode:** the `STATE` tab traces `attempt`, `ceiling`, `delay` and `lastError`
  across all 12 steps, and doubles as a third click-to-jump index.
- **Execution order ≠ source order.** `sleep` is bound at line 7 (step 2) but its body does
  not run until step 10, when line 40 calls it — the walkthrough scrolls *back up* the file,
  and the band covers only the lines that actually run at that moment.
- **No invented runtime values.** The delay is `Math.random() * ceiling`, so the trace prints
  the interval `0 … ceiling`, never a millisecond figure, and the caption says it was
  hand-traced. A dash means the binding does not exist at that step — including bindings that
  have already left scope (`ceiling` after the `catch`, `attempt` after the loop).
- **Defects named, not smoothed:** every error is retried identically; the abort listener
  survives when the timer wins the race; the abort check outside the `try` is called out as
  deliberate; `retries = 3` means four attempts.
- **Progressive enhancement and a11y:** no-JS shows the code, all 11 cards, the 12-step list,
  the diagram and the trace; `prefers-reduced-motion` disables auto-advance and all animation;
  AA contrast everywhere outside the syntax tokens.

`async-retry-with-backoff.preview.png` is a headless Chromium render of that same file at
1366 × 768 — nothing is drawn by hand, so the screenshot and the artefact cannot drift.
