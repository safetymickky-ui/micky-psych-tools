---
name: concept-lab
description: >-
  Builds one page that teaches one concept, any field (ML, statistics, pharmacology; field
  packs for psychiatry, computational psychiatry, endocrinology): a step-by-step walkthrough
  on one phone screen; each step highlights one thing in plain words, or a watch-only
  animation. Computed mode runs the real model; authored mode covers concepts with no
  model. Use when the user says "visualize this concept", "interactive visualization",
  "make an interactive demo", "make it interactive", "interactive page", "explorable", "let
  me play with the parameters", "ทำภาพอธิบายแบบโต้ตอบ", "ทำแบบโต้ตอบ", "animate this
  concept", "create an animation", "make an animation of X", "animated explainer", "show it
  moving", "ทำแอนิเมชัน", "ภาพเคลื่อนไหว", or runs /visualize or /animate. Intent-lock runs
  first; clinical facts come only from a sourced report; each page is its own artifact. NOT
  for: a static one-page summary (clinical-infographic), a chart of the user's own data
  (dataviz), or explaining a code listing (code-explainer).
---

# Concept Lab — one concept, one page

You turn one concept into one **page**: a single self-contained `.html` file that the user
opens on a phone. Usually the user drives it and learns from what the page does in response;
when they ask for an animation, the page plays the concept scene by scene.

The owner locked this shape on 2026-11-10, and corrected it the same day after the first real
page. Do not drift from it:

- **Any concept is in scope.** ML, statistics, computational psychiatry, pharmacology,
  clinical concepts, anything else.
- **A guided walkthrough, step by step.** The page opens on step 1. Each step shows one new
  thing, highlights it so the reader knows where to look, and explains it in two or three
  short beginner-friendly sentences: enough substance to learn from, not a textbook page. The
  reader moves with Back and Next (or a swipe). No Play button.
- **Maths looks like maths.** Formulas are typeset with native MathML and colour-coded: one
  colour per kind of quantity, the same in the formula, in the numbers and on the picture.
- **Something to tap in every step.** Any part of the picture and any dotted term or symbol
  opens a short pop-up; a step that computes something hides its number work until the reader
  taps to reveal it, line by line. Motion is lively and each motion means something.
- **A picture that means something.** Fill, thickness and arrows encode values, strength and
  direction; highlights and levels change smoothly between steps.
- **Never the whole picture at once.** Parts and numbers appear at the step that introduces
  them; everything a step is not about is dimmed. The view is never crowded.
- **Phone first, no scrolling.** The whole page fits one phone screen; Back and Next sit in a
  bar at the bottom, always in thumb reach.
- **Few controls.** No sliders for a beginner or intermediate reader. Up to three or four
  "what if" cases appear on the last step.
- **Warm, not generic.** A warm dark palette, serif headings, soft shapes. No neon, no
  dashboard chrome.
- **Its own artifact.** Each lab is published as a separate artifact page. Nothing goes to the
  vault unless the user asks.

Read [references/build-contract.md](references/build-contract.md) before writing code and
[references/concept-patterns.md](references/concept-patterns.md) before choosing the view. For
watch mode, also read [references/animation-grammar.md](references/animation-grammar.md).
`${CLAUDE_PLUGIN_ROOT}/examples/backprop.html` is a worked lab built to both; start from its
shape.

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

## Three rules that make it teach

- **One focus per step.** Before writing a step, name the one thing the reader should look at
  and the one sentence that says what it does. If a step needs two focuses, it is two steps.
- **Words, then the rule, then the numbers.** Say what a part does in common words first. Then
  show the rule as a typeset formula, and under it the same rule with the live numbers, in the
  same colours. The view does not have to carry every number.
- **The instructive case is one tap away.** The "what if" cases on the last step jump to the
  situations that change the lesson (the answer is already right, an input is zero, a unit is
  saturated; or, in authored mode, the items people confuse). Each jumps back to the step
  where its effect first shows, and those steps say what changed and why. A breakdown is
  reported in words, never rendered as `NaN`.

**Free-play form** (sliders that re-run the model, at most two) is the exception: only when the
user asks to "play with the parameters", or the level is advanced and the lesson needs a
continuous control. It keeps every other rule.

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
- **Level** — what maths, notation, or clinical background may appear unexplained. A field
  pack's default reader is the option to offer first; the user's answer wins.
- **Scope edge** — what stays out, so the lab does not grow into a course.

In watch mode the question becomes the one "aha" the animation must produce.

Mode, view, palette, and layout are decided by this skill and the contract, not by the interview.

## Step 1 — Choose mode and form

**Field pack first.** When the concept belongs to one of these fields, read its pack before
anything else in this step:

| Field | Pack |
|---|---|
| Endocrinology | [references/fields/endocrinology.md](references/fields/endocrinology.md) |
| General (clinical) psychiatry | [references/fields/general-psychiatry.md](references/fields/general-psychiatry.md) |
| Computational psychiatry | [references/fields/computational-psychiatry.md](references/fields/computational-psychiatry.md) |

A pack names, for its field, the picture that fits each kind of concept, the misconception to
remove, the "what if" cases, the default reader, the colour roles, and which facts are
clinical lane and where they must come from. It narrows the menu; it does not replace
`references/concept-patterns.md` or the contract. A concept that sits in two fields (a
hormone axis in depression) takes the picture from the field the question is about and the
source rules of both.

State the mode and why in one line. Then take the form from `references/concept-patterns.md`.
For a concept not listed: *what is the state, what one action changes it, what single picture
makes the change visible?*

One main view. A second view is allowed only when the lesson is the link between two pictures
(mechanism next to consequence), and then both read the same state on the same tick.

## Step 2 — Write the lab spec before any code

In text, before the file exists:

1. The concept and the question the page answers.
2. Mode. Computed: the model as it will be typed (update rule, formula, recurrence). Authored:
   the content items and the source of each.
3. The main view: its parts, and an explicit position for every part and every label.
4. **The step list** (5–14 steps). For each step: the focus, a two-to-five-word title, the two
   or three sentences, the formula and its number line if it computes something, and which
   lines carry direction arrows. The first steps introduce the
   parts; the last sums up.
5. The "what if" cases (0–4), each with the step it jumps to and what the steps will say.
   Also: the glossary entries (each term and symbol, one to three sentences), and for each
   kind of picture part the sentence its pop-up says in each state.
6. Checks: the invariants `window.__lab.checks()` will assert (contract, "Checks").
7. Source line.

Watch mode replaces items 4–5 with a **storyboard**: 3–8 scenes, and for each one what enters,
what moves, the caption, and the claim the motion makes. Every clinical fact in the spec maps
to the source report before any HTML exists.

If the update rule cannot be written down here, it cannot be implemented honestly. Stop and
resolve that before coding.

## Step 3 — Build to the contract

Full rules are in `references/build-contract.md`. The load-bearing ones:

- One self-contained HTML file starting with `<!DOCTYPE html>`; inline CSS and JS; no
  libraries, fonts, images, or CDN.
- Four parts on one phone screen: header with a step counter, the main view, the step card,
  the bottom bar with Back and Next. No scrolling at 390×700.
- `compute()` runs the whole model; a step only decides what is shown and highlighted. Every
  number on the page is read from the computed model.
- Focus elements get the focus colour and a halo; the rest is dimmed; labels of dimmed parts
  are hidden. At most 10 pieces of full-strength text in the view; no overlapping labels.
- The three kinds of tap from the contract: picture parts, terms and symbols, and the
  calculation revealed line by line, with the picture following the reveal.
- The warm palette and serif headings from the contract; formulas in MathML with the colour
  code; the SVG built once and restyled per step so changes animate.
- Checks run in the page but are not shown: `window.__lab` exposes `mode`, `steps`, `at()` and
  `checks()` for the verify script.
- Watch mode: the motion vocabulary, scene pacing and player are in
  `references/animation-grammar.md`.

## Step 4 — Drive it and verify

Run the bundled script; do not paste a verify script into the session:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/verify.mjs" ./lab.html
```

It drives the page at phone (390×700) and desktop (1280×800) sizes, in both motion modes. It
walks every step and every "what if" case and exits non-zero on any failure: console errors, a
page taller than the phone screen, a control off screen or under 44 px, overlapping, covered or
clipped labels, too much full-strength text, a Play button in a walkthrough, sliders beyond the
limit, `NaN`/`Infinity`/`undefined` on screen, or a failing check. It saves one screenshot per
step.

Then **look at the phone screenshots yourself, every step**, and ask the owner's three
questions: is it clear where to look first, does the card explain what is highlighted in
beginner words, and is anything cramped? The script passed a first backpropagation page whose
labels sat behind the nodes; only the screenshots showed it. Fix and re-run until it exits 0
and the screenshots hold. This pass changes how the page runs and sits on screen, never what
the model computes or what the source says.

## Step 5 — Publish

1. Publish the file as **its own artifact** with the Artifact tool: title = the concept, in
   the user's words. A change to an existing lab republishes the same artifact; a new concept
   is a new artifact.
2. When no Artifact tool is available, send the `.html` file to the user and say in one line
   that it was not published.
3. File to the vault (via **vault-keeper**, as an asset) only when the user asks.

Never claim a publish or a save that did not happen.

## Reply in chat

Short: the concept and the question the page answers, the "what if" case to try first, and the mode
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

- The page opens on the finished picture, or a step has no single highlighted focus, so the
  reader does not know where to look.
- A step's text assumes a term it has not explained, is a bare one-liner with nothing to
  learn from, or runs past three short sentences.
- A formula is shown as plain text, or its colours do not match the picture.
- A step offers nothing to tap but Next: no tappable parts, no tappable terms, or a
  calculation that is already worked out when the step opens.
- A pop-up hides the part it explains, runs off the screen, or states something the reader
  has not been shown yet.
- On a phone the page needs scrolling, Back/Next are not in thumb reach, or a control is too
  small to touch.
- The view is crowded: overlapping or covered labels, more than 10 pieces of full-strength
  text, a line carrying two labels at once.
- A walkthrough has a Play button, or a beginner page has sliders.
- The page looks like a generic dashboard: neon accents, navy-black, monospace readouts,
  all-caps labels.
- In computed mode, anything on screen was drawn by hand to look like output, or the
  implemented model does not match the concept's definition.
- Authored content is presented as computed, or carries no source line.
- A clinical drug, dose, threshold, or number is not traceable to the source report.
- No "what if" case reaches the situation that changes the lesson, or a case does not say what
  changed.
- In watch mode, a motion decorates (its claim cannot be named), the sequence implies an order
  or cause the source does not support, the last scene is not a complete labelled summary, or
  a schematic lacks its *illustrative* label.
- `NaN`, `Infinity`, or `undefined` reaches the screen, or a breakdown is shown without words.
- The page loads anything external, or lacks `<!DOCTYPE html>`.
- It was published without `verify.mjs` exiting 0 and the screenshots being looked at.
- Intent-lock was skipped without the user's explicit opt-out.
- It was written into `vault/` unasked, or a publish was claimed that did not happen.
