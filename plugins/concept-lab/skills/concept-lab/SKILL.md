---
name: concept-lab
description: >-
  Builds one page that teaches one concept, any field (ML, statistics, computational
  psychiatry, pharmacology, clinical): an interactive page the user drives, or a watch-only
  animation. Phone-first, minimal, dark. Computed mode runs the real model live; authored
  mode covers concepts with no model; watch mode unfolds the concept scene by scene. Use
  when the user says "visualize this concept", "interactive visualization", "make an
  interactive demo", "make it interactive", "interactive page", "explorable", "let me play
  with the parameters", "ทำภาพอธิบายแบบโต้ตอบ", "ทำแบบโต้ตอบ", "animate this concept",
  "create an animation", "make an animation of X", "animated explainer", "show it moving",
  "ทำแอนิเมชัน", "ภาพเคลื่อนไหว", or runs /visualize or /animate. Intent-lock runs first; clinical facts
  come only from a sourced report; each page is its own artifact. NOT for: a static
  one-page summary (clinical-infographic), a chart of the user's own data (dataviz), or
  explaining a code listing (code-explainer).
---

# Concept Lab — one concept, one page

You turn one concept into one **page**: a single self-contained `.html` file that the user
opens on a phone. Usually the user drives it and learns from what the page does in response;
when they ask for an animation, the page plays the concept scene by scene.

The owner locked this shape on 2026-11-10. Do not drift from it:

- **Any concept is in scope.** ML, statistics, computational psychiatry, pharmacology,
  clinical concepts, anything else.
- **Phone first.** One column, page scroll allowed, touch-size controls. Desktop gets the same
  column, centred.
- **Minimal.** One main view, 1–3 controls, 2–4 presets, one status line, a one-line footer.
  No readout row, no self-check chips, no keyboard-shortcut legend, no long footer.
- **Dark.** The palette in the build contract; no light theme.
- **Its own artifact.** Each lab is published as a separate artifact page. Nothing goes to the
  vault unless the user asks.

Read [references/build-contract.md](references/build-contract.md) before writing code and
[references/concept-patterns.md](references/concept-patterns.md) before choosing the view. For
watch mode, also read [references/animation-grammar.md](references/animation-grammar.md).
`${CLAUDE_PLUGIN_ROOT}/examples/learning-rate.html` is a worked lab built to both; start from
its shape.

## Three modes — pick by the request and the concept

- **Computed mode** — the concept has a model that can run in the page (an update rule, a
  distribution, a dose–response curve, a recurrence). The model runs live; every number and
  mark on screen is its output at the current control values. Nothing is drawn to look right.
- **Authored mode** — the concept has no runnable model (defense mechanisms, a diagnostic
  pathway, a classification). The interaction is over content written by hand: reveal, branch,
  sort or match, compare. The footer says the content is authored and names its source.

- **Watch mode** — the user asked for an animation, or to watch rather than drive (`/animate`,
  "animate", "show it moving"). The page unfolds the concept in 3–8 scenes with one caption
  each and a player (Play, Prev, Next, Restart); no parameter controls and no presets. Every
  motion makes a nameable claim (enters, flows, changes state, causes), and the last scene is
  the complete labelled summary. Schematic curves and magnitudes are labelled *illustrative*.

Interactive is the default: a request that names no form gets computed or authored mode. A
page that would have a Play button and nothing else is watch mode; say so and build it as one.

A lab may mix computed and authored (a computed curve plus authored labels), and then the
footer names both.
Never present authored content as computed, and never fake a computation: if a view cannot be
produced by the model, it is authored and labelled, or it is cut.

## Two rules that make it teach

- **Every control is a question.** Name the question before adding the control ("what if the
  learning rate is too big?", "what if occupancy passes 80%?", "which defense is this?"). A
  control with no question is cut. Three controls is the ceiling; speed and zoom do not count
  and are usually left out.
- **The instructive regime is reachable, and a preset jumps to it.** In computed mode the
  controls reach the place where the model breaks or changes behaviour, and a breakdown is
  reported in the status line, never rendered as `NaN`. In authored mode the presets jump to
  the cases people confuse. A user who touches nothing but one preset must still meet the point.

## Content fidelity

- **Clinical lane** — the page will show drugs, doses, thresholds, occupancies, criteria, or
  outcome numbers. Every such fact comes from a sourced report, resolved in this order, and is
  never written from memory:
  1. a report produced or pointed at in this session;
  2. an existing vault report (ask **vault-keeper** to query);
  3. none exists → generate it first with **comprehensive-review** (a whole topic) or
     **pubmed-research-note** (one decision or protocol).
  The footer names the report and carries: *teaching aid, not a substitute for clinical
  judgment or local protocol.*
- **General lane** — established, non-clinical knowledge. Numbers the page computes need no
  source. A published number about a real system (a benchmark, a parameter count) carries its
  source or does not appear.
- **Toy scale is said once**, in the footer: what the toy keeps and what it drops.
- **Randomness is seeded** in the code, so the same page gives the same run. The seed is not
  shown unless "new data" is one of the controls.

## Step 0 — Intent-lock gate (mandatory)

Run the **intent-lock** skill first; skip only on an explicit opt-out ("just build it"). One
topic holds many possible labs. The interview settles:

- **The one question the page answers**, or the one wrong belief it removes. This is the spine.
- **Level** — what maths, notation, or clinical background may appear unexplained.
- **Scope edge** — what stays out, so the lab does not grow into a course.

In watch mode the question becomes the one "aha" the animation must produce.

Mode, view, palette, and layout are decided by this skill and the contract, not by the interview.

## Step 1 — Choose mode and form

State the mode and why in one line. Then take the form from `references/concept-patterns.md`.
For a concept not listed: *what is the state, what one action changes it, what single picture
makes the change visible?*

One main view. A second view is allowed only when the lesson is the link between two pictures
(mechanism next to consequence), and then both read the same state on the same tick.

## Step 2 — Write the lab spec before any code

About ten lines, in text:

1. The concept and the question the page answers.
2. Mode. Computed: the model as it will be typed (update rule, formula, recurrence). Authored:
   the content items and the source of each.
3. The main view, and what it draws.
4. Controls (at most 3), each with its question and its range, including the instructive end.
5. Presets (2–4), each named for what it shows.
6. The status line: the sentence it shows in the normal case and in the broken case.
7. Checks: the invariants `window.__lab.checks()` will assert (contract, "Checks").
8. Footer line.

Watch mode replaces items 4–6 with a **storyboard**: 3–8 scenes, and for each one what enters,
what moves, the caption, and the claim the motion makes. Name the signature moment. Every
clinical fact in the storyboard maps to the source report before any HTML exists.

If the update rule cannot be written down here, it cannot be implemented honestly. Stop and
resolve that before coding.

## Step 3 — Build to the contract

Full rules are in `references/build-contract.md`. The load-bearing ones:

- One self-contained HTML file starting with `<!DOCTYPE html>`; inline CSS and JS; no
  libraries, fonts, images, or CDN.
- Phone-first single column; page scroll is allowed; the main view keeps a fixed aspect ratio
  and, with the title and the first control, fits the first phone screen.
- Touch targets at least 44 px; real `<button>` and `<input>` elements; pointer events on
  canvases.
- One state object, one `step()`, one `render()`. A control change re-runs from a defined point.
- One status line (`aria-live`), in plain words with at most two numbers.
- Checks run in the page but are not shown: `window.__lab.checks()` returns them for the
  verify script.
- `prefers-reduced-motion`: no autoplay; presets show their end state at once.
- Watch mode: the motion vocabulary, scene pacing and player are in
  `references/animation-grammar.md`; the caption is the status line.

## Step 4 — Drive it and verify

Run the bundled script; do not paste a verify script into the session:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/verify.mjs" ./lab.html
```

It drives the page at phone (390×844) and desktop (1280×800) sizes, in both motion modes, and
exits non-zero on any failure: console errors, sideways scroll, a touch target under 44 px,
the main view or first control outside the first phone screen, more than 3 controls or 4
presets, `NaN`/`Infinity`/`undefined` on screen, or a failing check. It saves one screenshot
per preset, or per scene in watch mode. Then **look at the phone screenshots yourself** and
confirm each preset shows what its name says, and each scene what its caption says. Fix and re-run until it exits 0. This pass changes how the page runs and
sits on screen, never what the model computes or what the source says.

## Step 5 — Publish

1. Publish the file as **its own artifact** with the Artifact tool: title = the concept, in
   the user's words. A change to an existing lab republishes the same artifact; a new concept
   is a new artifact.
2. When no Artifact tool is available, send the `.html` file to the user and say in one line
   that it was not published.
3. File to the vault (via **vault-keeper**, as an asset) only when the user asks.

Never claim a publish or a save that did not happen.

## Reply in chat

Short: the concept and the question the page answers, the preset to try first, and the mode
(with the source report when authored or clinical). The page is the deliverable; do not
restate the concept as prose.

## Handoffs

- **intent-lock** — the Step 0 gate.
- **clinical-infographic** — a static, print-ready one-page clinical summary.
- **code-explainer** — a code listing explained line by line.
- **dataviz** (skill) — a chart of data the user already has.
- **comprehensive-review / pubmed-research-note** — produce the sourced report the clinical
  lane needs. This skill runs no literature search of its own.
- **vault-keeper** — vault queries for a source report, and vault filing on request.

## Failure conditions

This skill has failed if:

- The page shows more than one screen of panels: a readout row, check chips, a shortcut legend,
  a multi-line footer, more than 3 controls, or more than 4 presets.
- On a phone the page scrolls sideways, a control is too small to touch, or the main view and
  first control are not on the first screen.
- In computed mode, anything on screen was drawn by hand to look like output, or the
  implemented model does not match the concept's definition.
- Authored content is presented as computed, or carries no source line.
- A clinical drug, dose, threshold, or number is not traceable to the source report.
- No control or preset reaches the instructive regime, or a control's question cannot be named.
- In watch mode, a motion decorates (its claim cannot be named), the sequence implies an order
  or cause the source does not support, the last scene is not a complete labelled summary, or
  a schematic lacks its *illustrative* label.
- `NaN`, `Infinity`, or `undefined` reaches the screen, or a breakdown is shown without words.
- The page loads anything external, or lacks `<!DOCTYPE html>`.
- It was published without `verify.mjs` exiting 0 and the screenshots being looked at.
- Intent-lock was skipped without the user's explicit opt-out.
- It was written into `vault/` unasked, or a publish was claimed that did not happen.
