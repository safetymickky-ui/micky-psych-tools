# Lessons learned — the PPGL run, and how to make the next infographic better

A worked retrospective from the first real end-to-end run of the pipeline
(`pubmed-research-note` → `clinical-infographic`) on *Perioperative Management of PPGL*.
It is kept here because the failures were **systematic, not topic-specific** — the same
mistakes will recur on the next report unless the skill defaults change. Each lesson below
names the fix that was folded back into this plugin.

## What the run produced

A sourced, phase-structured report (15 PubMed + 4 trials) and a self-contained HTML
infographic, filed to the vault. The clinical fidelity was right from the first pass — every
number kept its units and qualifiers, the safety banner carried the contraindications, and
three unsourced-but-classic items (sodium nitroprusside, "Roizen criteria", glucagon-as-crisis
-trigger) were correctly **excluded** rather than laundered in. That part of the contract held.

## What went well (keep doing)

- **Source extraction via a subagent.** Two open-access full texts were >80 KB; a subagent
  read them and returned verbatim numeric quotes, keeping the main context clean. This is the
  right move whenever full text is large — delegate the read, keep the numbers.
- **The publication-bias sweep earned its place.** ClinicalTrials.gov surfaced a *live* RCT
  (NCT05702944, omitting α-blockade in normotensive tumours) that became the report's
  "what would change this" — a forward-looking finding no abstract gave.
- **Fidelity-by-subtraction.** The subagent explicitly flagged what was *not* in the sources.
  That negative list is what let the render stay honest. Ask for it every time.

## Where it fell short (the fixes)

### 1. The first infographic was text-heavy — because the template is text-heavy
The v1 render was three columns of prose cards. It was accurate but read like a report in
columns, and the user's first reaction was *"more visualization, diagram and more."* The root
cause was not judgment — it was the **default**: the template shipped only columns/cards/tiles,
so that is what got filled. The biggest quality jump of the whole run (the haemodynamic
surge→crash curve, the escalation ladder, the surge/crash split) came only after a second,
user-prompted pass.
> **Fix:** the template now ships **reusable, commented diagram scaffolds** (hero timeline/
> curve, mechanism flow, escalation ladder, decision-flow, surge/crash split), and the design
> system has a **"beyond columns" diagram-grammar** section. Reach for a diagram *first*, prose
> only for what a diagram can't carry.

### 2. There was no "signature visual" step
Most clinical references have one defining picture — a physiologic *journey* over time, a
decision tree, a mechanism chain. Here it was the BP-vs-time curve, and it should have been the
first thing designed, not the last. The columns are the *detail*; the signature visual is the
*gestalt*.
> **Fix:** Step 1 now explicitly asks *"what is this report's one signature visual?"* before
> the columns are drawn.

### 3. Schematic figures created a new fidelity risk the contract didn't cover
A hand-drawn BP curve *looks* like data. The original fidelity rules ("no number not in the
source") didn't address illustrative figures, whose whole job is to show a shape, not a
measurement. The run handled it correctly by ad-hoc labelling ("illustrative — not measured
data"), but that was judgment, not a rule.
> **Fix:** new fidelity clause — **any schematic/illustrative figure must be labelled as such,
> carry only sourced numbers (e.g. the SBP 160 / MAP 60 thresholds), and never be drawn to a
> false axis.** Added to `source-contract.md` and `design-system.md`.

### 4. Layout correctness was only ever confirmed by rendering it
Nothing in the skill said to *look* at the output. The layout was verified by rendering a
screenshot (and later OCR'ing it to prove no text was clipped) — but that was initiative, not
procedure. An infographic that is never rendered is a guess.
> **Fix:** new **Step 2.5 — render & verify**: rasterise the HTML, eyeball the layout, and
> (optionally) OCR to confirm no clipped/overlapping text before filing. PNG export is now a
> named deliverable, not an afterthought.

### 5. Icons/diagrams need their own accessibility handling
The SVG curve needed `role="img"` + `<title>`/`<desc>`; the flow diagrams needed a sensible
reading order and must not lean on arrow glyphs alone. The column rules already covered
"colour is never the only signal" — the diagram rules did not.
> **Fix:** design-system diagram grammar spells out SVG `role="img"`/`<title>`/`<desc>`,
> logical DOM order for flows, and "never arrow-glyph-only" for meaning.

### 6. The template's dark mode and "medium" accents strand text — an OCR/contrast audit found it
Auditing the two psychopharmacology infographics (dose-occupancy, receptor-fingerprints) by
rendering them across light/dark × desktop/mobile and computing WCAG ratios surfaced three
**template-level** defects — so they were baked into anything generated from it, not one-offs:
- **A partial `@media (prefers-color-scheme:dark)` block.** It re-coloured only `--bg/--ink/
  --muted`, so under an OS dark theme every tinted table row, the whole safety-banner body, and
  the hardcoded SVG label colours became invisible light-on-light / dark-on-dark text (131–412
  contrast failures per page). These are *paper* references on a white surface — a dark mode has
  no business here, and a *partial* one is strictly worse than none.
- **"Medium" accents that fail white-on-colour.** The green header (`#3f8a6e` = 4.1), the heat-map
  `++` cells (`#4f86be` = 3.8), and the amber label (`#c9772e` = 3.4) all carried white/near-white
  text below 4.5:1. They *look* fine; they measure as failing.
- **An unwrapped wide table** scrolled the whole sheet sideways on a phone (482 px table, 390 px
  viewport) instead of scrolling inside its own box.
> **Fix:** the template is now **light-locked** (`color-scheme:light`, no dark block), its default
> accents are darkened to clear white-on-accent AA (`--c2 #3b8167`, `--c3 #a4601f`), it ships a
> `.tscroll` wrapper for wide tables, and design-system.md documents the **white-on-accent trap**
> + the light-lock rule. Step 2.5 now checks contrast and a simulated dark-OS render, not just
> clipping. (The app also neutralises any stray dark block defensively — but the document must be
> correct at source.)

## The "next time" checklist (the one-screen version)

1. Acquire sourced content (unchanged) — and ask the extractor for the **not-in-source** list.
2. **Name the one signature visual** the report implies (a journey? a decision? a mechanism?).
3. Draft **diagrams first** from the scaffolds; use prose cards only for the residue.
4. Keep every number's units/qualifiers; label every schematic **illustrative**; carry all
   contraindications to the safety banner.
5. **Light-lock** the sheet (`color-scheme:light`, no dark block); verify **white-on-accent ≥ 4.5**
   and wrap any wide table in `.tscroll`.
6. **Render → look → contrast-check → (OCR) → fix**, including a **dark-OS** render to prove the
   sheet stays light. Only then file via vault-keeper. Offer a PNG.

The through-line: the clinical contract was never the problem — **the visual defaults were.**
Move the defaults toward diagrams and toward looking at the result, and the second-pass rework
becomes the first pass.
