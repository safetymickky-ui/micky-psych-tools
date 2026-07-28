---
name: code-explainer
description: >-
  Explains given code as one interactive, self-contained HTML page — the original code on
  the left in a VS Code-styled editor (Dark+ theme, line numbers, syntax highlighting), the
  explanation on the right, cross-linked line by line. Use when the user says "explain this
  code", "explain the given code", "walk me through this function", "annotate this code",
  "code walkthrough", "what does this code do", "อธิบายโค้ดนี้", or runs /explain-code.
  Ships three linked modes: hover/click line↔explanation highlighting, a step-through
  walkthrough in execution order, and an inline SVG flow diagram. Explains only what the
  code actually does — source reproduced verbatim, real defects named, no invented runtime
  values. NOT for: writing or refactoring code, auditing it for bugs, static clinical
  one-pagers (clinical-infographic), or concept animations (concept-animation).
---

# Code Explainer — the code on the left, the reason on the right

You turn a piece of given code into one **self-contained HTML explainer**: the source on
the left in an editor that looks like VS Code, the explanation on the right, and the two
wired to each other so the reader never has to hold a line number in their head. The
deliverable is a single `.html` file that opens offline in any browser.

Two references carry the detail. Read both before writing a line of markup:

- [references/vscode-shell.md](references/vscode-shell.md) — the chrome, the exact Dark+
  palette, the closed syntax-token set, layout and typography.
- [references/explanation-contract.md](references/explanation-contract.md) — the three
  mandatory interactive modes, the fidelity rules, escaping, accessibility, verification.

[references/explainer-template.html](references/explainer-template.html) is the working
skeleton — start from it rather than from a blank file.

## Prime directive — the artefact is only worth its accuracy

A page this polished is believed. Every failure mode of this skill is the same failure:
**something on screen that the code does not actually do.** So:

- **The code is reproduced verbatim** — byte for byte, whitespace and comments included.
  Never reformat, rename, re-indent, or quietly fix it on the way in.
- **Explain the code, not the intent.** If behaviour depends on a caller, a config value,
  or library semantics you have not read, the card says so.
- **Defects get named, never smoothed.** An off-by-one, a swallowed exception, an
  unawaited promise — flag it where it lives.
- **No invented runtime values**, in the state trace or in prose.

## Step 0 — Scope gate (conditional)

Explain immediately when the ask is already one reading: a snippet or a single file, one
evident concern, an audience you can infer.

Run the **intent-lock** skill first when it is not — and say why in one line before you
do. It is not, when:

- the target is a whole directory, several files, or "this repo";
- the code holds more than one concern and "explain it" could mean any of them;
- the audience or depth genuinely changes the artefact — someone learning the language,
  a reviewer arriving cold, a maintainer chasing one behaviour;
- the ask is a bare "explain this" with no code attached and no obvious referent.

Fast path or gated, three things must be settled before Step 2 — **what the reader should
be able to do afterwards**, **the depth** (what it does · how it works · why it is built
this way), and **the boundary** (what stays out of frame). Infer them and state them in
one line on the fast path; interview for them when the gate fires.

## Step 1 — Take the code in

Resolve where the source actually is, in this order: pasted in the message → a file path
in the repo (read it) → a file the user names loosely (find it, then confirm which one).
Never explain code you have not read in full.

Then read it properly before decomposing: entry points, control flow, what is called from
where, what mutates, what is async, what can throw, and what the code depends on that is
not in front of you. Run it or trace it if a state table is coming.

**Size:** up to ~200 lines is one explainer. Beyond that, explain the load-bearing
section and say on screen what was cut — a 900-line file annotated line by line is a
wall, not an explanation. Several files means several explainers, or one after
intent-lock has picked the thread.

## Step 2 — Plan the ranges and the steps, before any HTML

Write the plan as text first. It is quick, and it is where accuracy is decided.

1. **Annotated ranges** — cut the code into 4–12 ranges, one idea each, on real
   boundaries (a guard, a loop, a branch, a call). Every line of code lands in exactly one
   range, or in none deliberately.
2. **Execution order** — order the ranges the way the code *runs*, not the way it is
   written. Hoisting, callbacks, `await` resumption points, decorators, recursion: where
   run order diverges from source order, that divergence is usually the most valuable
   thing on the page. Keep it, and say it.
3. **The diagram** — pick the shape from the table in the contract (control flow, call
   graph, data flow, state, containment) and sketch its nodes against the same ranges.
4. **State trace?** — algorithmic code yes, config and glue no.
5. **Each card's claim** — one sentence per range saying what the reader learns. A range
   whose sentence is "sets up variables" is not a range; merge it.

## Step 3 — Build the page

From `references/explainer-template.html`, to the contract. The load-bearing rules:

- **One file, self-contained** — inline `<style>`, `<script>`, and SVG. No external CSS,
  JS, font, image, or CDN.
- **Pre-tokenise the syntax yourself.** You emit `<span class="t-key">` markup as you
  write the file; there is no runtime highlighter to ship. Map every language onto the
  closed token set in `vscode-shell.md`.
- **Escape `&`, `<`, `>` before wrapping in spans** — generics, JSX, HTML snippets and
  shifts vanish otherwise. This is the quiet corrupter; check the rendered page, not your
  source.
- **All three modes wired to one id space** (`data-range`): linked highlighting,
  step-through, flow diagram. A diagram that does not cross-link is decoration.
- **No-JS still reads**, `prefers-reduced-motion` honoured, colour never the only signal,
  focus rings visible.
- **A footer that keeps it honest** — the source file (path, or *pasted snippet*), the
  language, the line count and any truncation, the generation date, and *explains the code
  as written — not a review or a correctness guarantee.*

## Step 3.5 — Render and verify

An explainer that was never opened is a guess. Render it headless and walk the
verification checklist at the foot of the contract: initial frame clean at 1366×768, every
step advancing correctly, both link directions working, no-JS readable, and the rendered
code re-read against the source for escaping and truncation damage. Fix and re-render
until it holds. **The final screenshot is a companion deliverable** next to the HTML.

Layout and wiring are what rendering proves. Accuracy is proved only by re-reading the
explanation against the code.

## Step 4 — Where the output goes

1. **Write** the `.html` (plus the screenshot) into the working directory.
2. **Surface it** — show the file so the user can open it; never merely name a path.
3. **Vault only on request.** These are usually working artefacts, so nothing is filed by
   default. When the user asks to keep it, hand it to **vault-keeper** as an asset —
   vault-keeper owns every path and MOC wiring; never resolve a vault path or write into
   `vault/` from here.

**No filesystem:** return the HTML inline and say plainly that nothing was written.

## Handoffs

- **intent-lock** — the Step 0 gate when the ask has more than one reading.
- **vault-keeper** — every vault write, on request only.
- **concept-animation** — explaining an *idea* that happens to have code in it (how a
  scheduler works, what backpressure is) belongs there; explaining *this* code belongs
  here.
- **clinical-infographic** — static one-page clinical summaries, not code.
- **gridgeist** — if the user wants the explainer restyled away from VS Code entirely.
- Code *review*, refactoring, or bug-hunting is not this skill. Explain what is there; if
  a defect surfaces, name it in the card and offer the fix as a separate piece of work.

## Close

Two lines in chat: what was explained (file or snippet, language, line count), the range
and step counts, which diagram was chosen and why, the file path, and anything deliberately
left out of frame — plus any defect the explanation had to name. The HTML is the
deliverable; never restate its contents as prose.

## Failure conditions

This skill has failed if:

- The rendered code differs from the source in any byte — reformatted, re-indented,
  renamed, silently truncated, or mangled by unescaped `&`/`<`/`>`.
- A card describes behaviour the code does not have, or narrates a real defect as
  intended behaviour.
- A runtime value, trace row, or complexity claim was invented rather than traced or run.
- The step order was tidied back into source order where the code actually runs otherwise.
- The flow diagram is not cross-linked to the ranges, or is a picture of something the
  code does not do.
- The file references any external CSS, JS, font, image, or CDN.
- Nothing works without JavaScript, `prefers-reduced-motion` is ignored, colour is the
  only signal for the current step, or focus rings were removed.
- A VS Code affordance was rendered that does nothing, or an editor feature was faked.
- It was handed over without being rendered and stepped through.
- A vault path was resolved or a file written into `vault/` from here instead of
  vault-keeper, or a save was claimed that did not happen.
