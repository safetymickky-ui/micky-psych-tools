---
name: concept-animation
description: >-
  Creates an animation that illustrates a given concept — one self-contained HTML file
  (inline CSS/SVG/JS, nothing external) that plays in any browser, unfolding the concept
  scene by scene: mechanisms, pathways, processes, algorithms, statistical ideas. Use when
  the user says "animate this concept", "create an animation", "make an animation of X",
  "animated explainer", "show it moving", "ทำแอนิเมชัน", "ภาพเคลื่อนไหว", or runs /animate.
  Runs intent-lock first to lock the concept to one reading. Any concept is in scope, but
  when the content is clinical the fidelity contract fires: drugs, doses, thresholds, and
  outcomes come from a sourced report (this session, the vault via vault-keeper, or
  generated first by comprehensive-review / pubmed-research-note) — never invented. Files
  the finished animation to the vault as an asset via vault-keeper. NOT for: static
  one-page summaries (clinical-infographic), data charts (dataviz), video/GIF rendering,
  or producing the underlying evidence (the research plugins own that).
---

# Concept Animation — the sequence is the explanation

You turn a concept into a short, self-contained **HTML animation** that teaches by
unfolding. The deliverable is one `.html` file — inline CSS, SVG, and JS, no external
anything — that opens offline in any browser and plays the concept scene by scene, with
synchronized captions and player controls. Motion is used for what prose can only assert:
order, causality, flow, accumulation, transformation, feedback.

## Prime directive — motion must explain, never decorate

The failure mode this skill exists to prevent is **decorative motion**: things move, nothing
is explained. An animation is trusted more than a paragraph *because* it shows — so a wrong
sequence teaches a wrong mechanism, confidently. Therefore:

- **Every animated property makes a claim.** Appearance = enters the story; movement along a
  path = transport/flow; morph = state change; sequence = order/causality; parallel motion =
  independence; a loop = a cycle. If a motion's claim cannot be named, cut the motion.
- **The final frame is the whole story.** Pausing at the end must leave a complete, labelled
  summary diagram on screen — the animation's own "summary slide".
- **Clinical fidelity, when it fires.** If the concept carries clinical facts — drugs, doses,
  receptor occupancies, thresholds, outcomes — those facts come from a sourced report and keep
  their units and qualifiers. Nothing quantitative is invented to make a scene read.
- **Schematics stay honest.** Illustrative curves, axes, and magnitudes are labelled
  *illustrative — not measured data*, for clinical and non-clinical concepts alike.

Read [references/animation-grammar.md](references/animation-grammar.md) before storyboarding
or writing a line of code — it holds the motion vocabulary, scene architecture, technical
contract, and accessibility rules.

## Step 0 — Intent-lock gate (mandatory)

Run the **intent-lock** skill first — explicit opt-out only ("just animate it"). A concept
named in one line ("animate receptor occupancy") has many animations inside it; the interview
exists to pick one before the storyboard is drawn. The animation-shaping forks it should
settle: the one **"aha"** the animation exists to produce, the audience and register, the
depth (overview vs mechanism-level), and the scope boundary (what stays out of frame).
Runtime, palette, and pacing default from the grammar — they are not interview material.

## Step 1 — Source the content

Any concept is in scope. Two lanes, chosen by what will appear on screen:

- **Clinical lane** — the animation will show drugs, doses, thresholds, occupancies, or
  outcome numbers. Resolve a sourced report, in order, and never author clinical facts here:
  1. **A report produced this session** — just written or pointed at. Use it directly.
  2. **An existing vault artifact** — query **vault-keeper** for a matching review or decision
     report. If one fits, it is the single source of truth; do not re-research it.
  3. **None exists → generate first.** A whole-topic mechanism → **comprehensive-review**; a
     single decision or protocol → **pubmed-research-note**. Those plugins own their own
     searches and citation discipline — let them.
- **General lane** — mechanisms, algorithms, statistical ideas, and other non-clinical
  concepts animate from established knowledge. No invented precision: no fake data points or
  fabricated axis values presented as measured; schematic values carry the illustrative label.

## Step 2 — Storyboard before code

Write the storyboard as text first: **3–8 scenes, one idea per scene.** For each scene —
what enters, what moves, what the caption says, and **what claim the motion makes** (from the
grammar's vocabulary). Name the signature moment: the single transition that produces the
"aha" locked in Step 0, and build the storyboard so everything before it sets it up.

The storyboard is the fidelity checkpoint: every clinical fact in it maps to the source
report before any HTML exists. A scene that needs an unsourced number loses the number, not
the fidelity rule.

## Step 3 — Build the animation

Build to the technical contract in the grammar. The load-bearing rules:

- **Self-contained, always.** One HTML file, inline `<style>`, `<script>`, and SVG — no
  external CSS, JS, fonts, images, or CDN. It must open offline, identically, anywhere.
- **A scene controller, not a fire-and-forget loop.** Play/Pause, Restart, and Prev/Next
  scene controls, keyboard operable, with a scene indicator; pausing freezes everything
  coherently.
- **Captions are synchronized DOM text** — one sentence per scene, on screen at least twice
  its reading time, never overlapping the action.
- **`prefers-reduced-motion` is mandatory:** with motion reduced, the scenes render as a
  stepped storyboard that carries the full argument without animation.
- **Accessibility is not optional.** Color is never the only signal; contrast meets WCAG AA;
  headings are semantic; informative SVGs are labelled.
- **A footer that keeps it honest** — the source report's title and counts (clinical lane) or
  *illustrative — established knowledge* (general lane), the render date, and for clinical
  content: *teaching aid, not a substitute for clinical judgment or local protocol.*

## Step 3.5 — Render & verify before filing

An animation that was never watched is a guess. Render the HTML in a headless browser and
screenshot **each scene's hold plus the final frame**: nothing clipped or overlapping,
captions legible, the sequence reading in the order the storyboard claims, the final frame a
complete labelled summary. Fix and re-render until it holds. The **final-frame PNG is a
companion deliverable** alongside the HTML. This is a layout check, never a content one.

## Step 4 — Where output goes

1. **Write** the finished animation as a single `.html` file (plus the final-frame PNG) in
   the working directory.
2. **Surface it** — show the file so the user can open and play it; never merely name a path.
3. **File it via vault-keeper.** The animation is a rendered **asset**: hand it to
   **vault-keeper** to place in `vault/assets/` — wired into the source report's MOC under
   `## Assets` when a source report exists, a standalone asset otherwise. Vault-keeper owns
   every path, dedup, and MOC wiring — never resolve a vault path or write into `vault/`
   from this skill. Skip only on an explicit "don't vault this".

**No filesystem:** return the HTML inline and say explicitly that nothing was written or
filed. Never claim a save that did not happen.

## Handoffs

- **intent-lock** — the mandatory Step 0 gate; not re-run by downstream plugins this skill
  invokes (they own their own gates when they generate).
- **comprehensive-review / pubmed-research-note** — generate the sourced clinical content
  when none exists; this skill never duplicates their searches or issues a clinical verdict.
- **vault-keeper** — every vault write, per Step 4.
- **clinical-infographic** — the static sibling: a print-ready one-page summary is its job;
  route "infographic" requests there. An animation can accompany an infographic of the same
  source; neither replaces the other.

## Close

Two lines in chat: what was animated and from which source (report title, or "established
knowledge — illustrative"), the scene count and runtime, the file path, the vault asset path
returned by vault-keeper (or that the save was skipped), and any gap omitted rather than
animated. The HTML file is the deliverable — never restate its content as prose.

## Failure conditions

This skill has failed if:

- A motion decorates instead of explains — an animated property whose claim cannot be named.
- A clinical drug, dose, or number appeared that is not traceable to the source report, or
  lost its units or a safety-critical qualifier in animation.
- A value was invented to make a scene read, or a schematic rendered without its
  *illustrative — not measured data* label.
- The sequence implies an order or causality the source (or established knowledge) does not
  support.
- The HTML references any external CSS, JS, font, image, or CDN — it is not self-contained.
- There is no `prefers-reduced-motion` fallback, color is the only signal for a meaning, or
  contrast/heading semantics fail accessibility.
- The animation was filed without being rendered and eyeballed scene by scene.
- Clinical content was animated with no traceable source when comprehensive-review or
  pubmed-research-note should have generated it first.
- A vault path was resolved or a file written into `vault/` by this skill instead of
  vault-keeper, or a save was claimed that did not happen.
- Intent-lock was skipped without the user's explicit opt-out.
