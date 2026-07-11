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

## The "next time" checklist (the one-screen version)

1. Acquire sourced content (unchanged) — and ask the extractor for the **not-in-source** list.
2. **Name the one signature visual** the report implies (a journey? a decision? a mechanism?).
3. Draft **diagrams first** from the scaffolds; use prose cards only for the residue.
4. Keep every number's units/qualifiers; label every schematic **illustrative**; carry all
   contraindications to the safety banner.
5. **Render → look → (OCR) → fix.** Only then file via vault-keeper (when installed). Offer a PNG.

The through-line: the clinical contract was never the problem — **the visual defaults were.**
Move the defaults toward diagrams and toward looking at the result, and the second-pass rework
becomes the first pass.
