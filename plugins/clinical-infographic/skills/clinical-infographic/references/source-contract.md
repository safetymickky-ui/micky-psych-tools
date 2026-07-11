# The source contract — deep integration, zero fabrication

The one rule that makes a clinical infographic safe to trust: **every mark on it traces back
to a sourced report.** This file is how that rule is kept. Read it before Step 0.

## Why this skill has no search engines

`clinical-infographic` deliberately ships **no PubMed / ClinicalTrials.gov wiring**. That is
not an omission — it is the guardrail. If the renderer could search, it could also *decide*,
and a compact, confident layout is the worst possible place for an unadjudicated clinical
claim. So the division of labour is hard:

| | Owns | Never does |
|---|---|---|
| comprehensive-review | whole-topic sourced content, its own citations | visual layout |
| pubmed-research-note | a decision's verdict + working, its own citations | visual layout |
| **clinical-infographic** | **the visual layout of already-sourced content** | **search, adjudicate, or author a clinical fact** |

The infographic is the *last mile* of the research pipeline, not a shortcut around it.

## Source precedence (Step 0)

Resolve a source in this order; stop at the first that fits:

1. **This session's report.** The user just ran `comprehensive-review` / `pubmed-research-note`,
   or pasted / pointed at a report ("the report above", a file path). Render it directly.
2. **An existing vault artifact.** Ask **vault-keeper** to `query` for a review or decision
   report on the topic (title / MOC / tag match). A fitting one is the single source of truth —
   do not re-research a topic the vault already answers.
3. **Nothing sourced exists → generate first.** Choose the engine by what the infographic is:
   - **Whole-topic / disorder reference** (multiple phases or themes, the full picture) →
     **comprehensive-review**. Its md chapter becomes the render skeleton.
   - **One decision or protocol** (a single call, a peri-op prep, a first-line choice) →
     **pubmed-research-note**. Its verdict + working become the render skeleton.

   Never skip step 3 into authoring facts yourself. "I'll just summarise what I know about X"
   is the exact failure the guardrail exists to stop.

## The fidelity contract (Step 1 → Step 2)

When you turn the report's prose into cards, tiles, and a banner, these transforms are the
**only** ones allowed:

- **Condense wording** — shorten a sentence to a directive, keeping its clinical content.
- **Promote a figure** — lift a number already in the report into a stat tile.
- **Regroup** — cluster the report's points under the columns it already implies.

Everything else is forbidden:

- **No new facts.** If a drug, dose, target, or rate is not in the report, it does not appear.
- **No stripped qualifiers.** "Metoprolol only after ≥3 days of alpha-blockade" never becomes
  "give metoprolol". The condition is the point.
- **No rounded-away uncertainty.** A range stays a range; a "non-significant" stays labelled;
  an effect size keeps its CI where the report gave one.
- **No dropped contraindications.** Every "avoid / contraindicated / do not use" in the source
  is carried to the safety banner. Cutting one for layout balance is a safety event, not a
  design choice.
- **No laundered gaps.** A `[unverified]` or explicitly-thin point is omitted or marked as a
  gap — never rendered as a confident tile.

If honouring all of this leaves a panel that will not fit, the panel shrinks or splits — the
*content* does not bend.

## Provenance carried into the render

Pull these from the source and put them in the footer so the infographic stays auditable:

- The source report's **title** and **date**, and its counts (`PubMed N · trials N`).
- Its **`## Sources` mapping** — the claim→DOI / NCT lines — as a collapsed Sources list.
- The standing disclaimer line: *clinical reference aid — not a substitute for clinical
  judgment or local protocol.*

A clinician who spots a surprising tile must be able to trace it back in one hop. If the source
list cannot support the tiles on the page, the tiles are wrong, not the list.

## Handoff parameters

- **To comprehensive-review / pubmed-research-note (generate):** the topic or decision, plus a
  note that the output will be rendered as a one-page clinical reference (so emphasis and
  brevity are welcome). Let their intent-lock gate run — do not pre-empt it.
- **To vault-keeper (file):** the finished `.html` as an **asset**, a title `<Topic> —
  Infographic`, a short companion-note body (what it summarises, link to the source artifact),
  and the **source report's MOC topic** so the infographic hangs off the same map as its source.
