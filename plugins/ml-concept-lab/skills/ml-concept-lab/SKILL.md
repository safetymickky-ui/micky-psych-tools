---
name: ml-concept-lab
description: >-
  Builds an interactive explorable that illustrates a machine-learning, AI, or
  computer-science concept — one self-contained HTML file (inline CSS/SVG/Canvas/JS)
  in which the real algorithm runs live and the learner drives it: gradient descent,
  backprop, attention, k-means, sorting, Dijkstra, big-O, Q-learning. Use when the user
  says "visualize this concept", "interactive visualization", "make an interactive demo",
  "explorable", "let me play with the parameters", "show me how X works", "animate this
  algorithm", "ทำภาพอธิบายแบบโต้ตอบ", or runs /visualize. Intent-lock runs first to pick one
  explorable out of the many in a topic; every number on screen is computed by the running
  algorithm, never hand-drawn, and the controls reach the regime where it breaks. Files it
  to the vault as an asset via vault-keeper. NOT for:
  a watch-only linear animation (concept-animation), charting a dataset the user already
  has (dataviz), clinical concepts (clinical-infographic), or web UI design (gridgeist).
---

# ML Concept Lab — the learner runs the algorithm

You turn a machine-learning, AI, or computer-science concept into one **interactive
explorable**: a single `.html` file — inline CSS, SVG/Canvas, and JS, no external anything —
that opens offline, implements the concept's actual algorithm in the page, and hands the
learner the controls. They move a slider, the algorithm re-runs, the picture changes, and
the concept is learned from its *behaviour* rather than from a caption describing it.

Three things ship together in one artifact, and none of them is optional:

- **Visualization** — the algorithm's state drawn as a picture (parameter space, network,
  attention matrix, array, graph, grid).
- **Interaction** — controls that change the algorithm's inputs and re-run it live.
- **Animation** — the algorithm stepping through time, with play / pause / step / reset.

## Prime directive — the picture is computed, not drawn

The failure mode this skill exists to prevent is the **fake demo**: a hand-drawn curve that
merely looks like gradient descent, an "attention matrix" of made-up numbers, a sort that
plays a canned sequence of swaps. It teaches confidently and it teaches wrong — and the
learner cannot tell, because a fake demo and a real one look identical until you poke them.

So: **the algorithm runs in the page.** Every number, curve, colour, and frame on screen is
the output of that running implementation, computed from the current control values. Nothing
is hardcoded to "look right".

Corollaries:

- **No canned frames.** If a view can't be produced by the model, cut the view — don't fake it.
- **Real scale where real scale fits; a labelled toy model where it doesn't.** A 175B-parameter
  LLM does not run in a browser tab. Attention over a 6-token sentence with `d_k = 4` does, and
  it is the *same computation*. Say so on the page: what the toy preserves and what it drops.
- **Determinism is part of honesty.** Randomness runs through one seeded PRNG with the seed
  visible and editable, so the same seed reproduces the same run and "it looked different last
  time" is never the explanation.
- **Published numbers are sourced or absent.** Benchmark scores, parameter counts, paper
  results, and complexity claims about real systems either carry their source or don't appear.
  Numbers the page *computes itself* need no source — they are reproducible on screen.

## Second directive — every control is a question, and one of them must break it

An explorable is a set of questions the learner can ask. A control that answers no question
is decoration; a control that cannot reach a failure regime is a lie of omission.

- **Name the question each control asks** before you add it — *"what if the learning rate is
  too big?"*, *"what if k is smaller than the number of true clusters?"*, *"what if the graph
  has a negative edge?"* If the question can't be named, cut the control.
- **The failure regime is reachable and instructive.** Sliders extend into divergence,
  overfitting, thrashing, worst-case input. The lesson usually lives at the broken end;
  clamping the range to the pretty regime is the most common way this skill fails.
- **Ship 3–5 presets** that jump straight to the instructive regimes, each named for what it
  shows: *"lr too high → diverges"*, *"k = 2 merges two clusters"*, *"already-sorted input →
  quadratic"*. A learner who moves nothing must still meet the point.

Read [references/build-contract.md](references/build-contract.md) before writing code — it
holds the technical contract, the correctness self-checks, and accessibility. Read
[references/concept-patterns.md](references/concept-patterns.md) before choosing the views —
it maps each concept family to the visualization, controls, and failure regimes that work.
`examples/learning-rate-and-conditioning.html` is a worked lab built to both; copy its shape
rather than starting from a blank file.

## Step 0 — Intent-lock gate (mandatory)

Run the **intent-lock** skill first — explicit opt-out only ("just build it"). "Visualize
transformers" contains a dozen different explorables; "show me gradient descent" contains at
least four. The interview settles:

- **The one misconception the explorable kills** — the single wrong belief a learner walks in
  with, that poking this page destroys. This is the spec's spine.
- **Audience and prerequisite level** — what maths and notation may appear unexplained.
- **Depth** — intuition-level (the shape of the behaviour) vs mechanism-level (the actual
  update rule, on screen, with its terms labelled).
- **Scope boundary** — what stays out of the lab, so it doesn't grow into a course.

Palette, layout, runtime, and control styling come from the build contract — they are not
interview material.

## Step 1 — Choose the form from the concept's family

Look the concept up in `references/concept-patterns.md` (optimization · neural-network
internals · transformers & LLM internals · classical ML · probability & information ·
algorithms & data structures · complexity & systems · reinforcement learning). Each family
names its canonical views, the controls that matter, the invariants worth asserting, and the
failure regimes worth reaching.

A concept that isn't listed still follows the method: **what is the state, what changes it,
and what picture makes the change visible?** Answer those three and the form follows.

Prefer **2–3 linked views over one busy view.** Linked views are the format's real power:
the same state drawn twice (parameter space *and* data space; the array *and* the operation
counter; the attention matrix *and* the sentence) is how a learner connects a mechanism to
its consequence. Every view updates from the same state on the same tick — a view that can
disagree with another view is a bug, not a design choice.

## Step 2 — Write the lab spec before any code

Text first, ~15 lines, and get it right before the file exists:

1. **Concept + the misconception it kills** (from Step 0).
2. **The model** — the exact algorithm, in the form it will be implemented: the update rule,
   the loss, the recurrence, the transition. Write the equation out; you are about to type it.
3. **State** — the variables that define one frame, and what one "step" advances.
4. **Views** — 2–3, each named, each saying which part of the state it draws.
5. **Controls** — each with the question it asks and its range, *including the broken end*.
6. **Presets** — 3–5 named regimes.
7. **Invariants** — what must be true every step, and how the page checks it (Step 3's
   self-check panel).
8. **Scale caveat** — what the toy drops versus the real system, in one sentence, if a toy.

The spec is the correctness checkpoint: if you cannot write the update rule down, you cannot
implement it, and a plausible-looking implementation of a rule you didn't check is exactly
the fake demo the prime directive forbids.

## Step 3 — Build to the contract

Full rules in `references/build-contract.md`. The load-bearing ones:

- **One self-contained HTML file.** Inline `<style>`, `<script>`, SVG; Canvas for anything
  redrawn per frame or dense (heatmaps, contours, particle-scale point clouds), SVG for
  structure that needs labels and accessibility (graphs, networks, matrices). No external CSS,
  JS, fonts, images, or CDN — no libraries at all, so the maths is yours and inspectable.
- **One state object, one `step()`, one `render()`.** `step()` advances the model and touches
  no DOM; `render()` draws state and mutates nothing. Every view reads the same state, so
  pausing freezes a coherent frame and stepping is exactly one unit of the algorithm.
- **Controls: Play/Pause, Step, Reset, the presets, and the parameter inputs**, all real
  `<button>` / `<input>` elements, all keyboard-operable, each showing its live value. Changing
  a parameter mid-run re-runs from a defined point — never silently keeps stale state.
- **A visible self-check panel.** The invariants from the spec, asserted live on the actual
  running values and rendered as pass/fail chips: gradients against finite differences,
  probabilities summing to 1, a sorted output actually sorted, a shortest path actually
  shortest, energy/loss monotone where theory says monotone. This is the page proving it isn't
  faking — and it catches your own implementation bugs before the learner does.
- **Step counter and cost counter.** Steps, comparisons, swaps, iterations, FLOP-equivalents —
  whatever the concept's cost unit is. Complexity claims come from the counter, not from prose.
- **`prefers-reduced-motion` is mandatory:** auto-play and transitions off, the explorable
  fully usable by stepping, no information lost.
- **Accessibility is not optional:** colour never the only signal, WCAG AA contrast, real
  headings, labelled informative SVG, an `aria-live` region announcing the current step's state.
- **A footer that keeps it honest:** what is computed live, the toy-scale caveat, the seed,
  sources for any external number, the render date.

## Step 3.5 — Drive it and verify, before filing

A screenshot proves layout; an explorable needs its *interaction* proven. Drive the page in a
headless browser (Chromium + Playwright — the recipe is in the build contract):

1. **Console clean** — no errors, no unhandled rejections, across the whole run.
2. **Every control exercised to both extremes**, including the broken end. The page must not
   crash, freeze, or render `NaN`/`Infinity` as if it were a value — divergence is *reported*,
   not leaked.
3. **Every preset loaded** and screenshotted; each must actually show what its name claims.
4. **Play → pause → step → reset** returns to a clean initial state, and the step counter agrees
   with the number of steps taken.
5. **Self-checks pass** in the rendered page, not just in your reasoning.
6. **Fits one screen at 1366×768** with no page scroll (the Learn hub embeds these in an iframe
   of `height: calc(100svh - 6rem)`), and again with reduced motion forced on.

Fix and re-drive until it holds. Export a **preview PNG** of the most instructive state (usually
a preset showing the failure regime) as a companion deliverable. This pass fixes how things run
and sit on screen — never what the model computes.

## Step 4 — Where output goes

1. **Write** the explorable as a single `.html` file (plus the preview PNG) in the working
   directory.
2. **Surface it** — show the file so the user can open and drive it; never merely name a path.
3. **File it via vault-keeper.** The explorable is a rendered **asset**: hand it to
   **vault-keeper** for `vault/assets/`, wired into a related report's MOC when one exists, a
   standalone asset otherwise. Vault-keeper owns every path, dedup, and MOC wiring — never
   resolve a vault path or write into `vault/` from this skill. Skip only on an explicit
   "don't vault this".

**No filesystem:** return the HTML inline and say explicitly that nothing was written or filed.
Never claim a save that did not happen.

## Handoffs

- **intent-lock** — the mandatory Step 0 gate.
- **concept-animation** — the watch-only sibling. A linear, narrated, no-controls explainer is
  its job, and clinical concepts are its lane, not this one. Route "just animate it" there; an
  explorable and an animation of the same concept can coexist.
- **dataviz** (skill) — charting a dataset the user already has. Here the data is generated by
  the model and the chart is its live output; a request to plot *their* numbers goes there.
- **gridgeist** — general web-interface design. This skill owns only the explorable's own layout.
- **firecrawl** — one-off fetch when an external published number (a paper's result, a spec's
  constant) must be cited rather than omitted. This skill ships no search engines.
- **vault-keeper** — every vault write, per Step 4.

## Close

Two lines in chat: the concept and the misconception the lab kills, the views and controls
built (with the failure regime a learner should try first), the self-checks that passed, the
file path, the vault asset path returned by vault-keeper (or that the save was skipped), and
any scale caveat. The HTML file is the deliverable — never restate the concept as prose.

## Failure conditions

This skill has failed if:

- Anything on screen was hand-authored to look like output instead of computed by the model —
  a canned frame sequence, a drawn curve, a plausible-looking matrix of invented numbers.
- The implemented algorithm doesn't match the concept's canonical definition (a "quicksort"
  that isn't, a softmax without max-subtraction, a gradient that never faced a finite-difference
  check), or an invariant was claimed but not asserted in the page.
- No control reaches the regime where the algorithm breaks, or a control exists whose question
  can't be named.
- The page has no interaction (that is concept-animation's artifact) or no animation of the
  algorithm advancing (that is a static diagram).
- A toy model is presented at real scale, or a benchmark/parameter/complexity claim about a real
  system appears without a source.
- Randomness is unseeded, so runs are irreproducible and a learner cannot compare two settings.
- Views disagree because they read different state, or pausing leaves a half-updated frame.
- The HTML references any external CSS, JS, font, image, CDN, or library — it is not
  self-contained.
- There is no `prefers-reduced-motion` path, colour is the only signal, or contrast/heading
  semantics fail accessibility.
- It was filed without being driven: controls untouched, presets unloaded, console unread.
- A vault path was resolved or a file written into `vault/` by this skill instead of
  vault-keeper, or a save was claimed that did not happen.
- Intent-lock was skipped without the user's explicit opt-out.
