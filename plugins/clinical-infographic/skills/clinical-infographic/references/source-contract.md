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
- **Keep the source's verb while shortening** — "consider", "avoid", "not recommended",
  "contraindicated" stay the source's words; a shorter card never upgrades one into another.
- **Spell `mcg` for `µg`** — the one allowed spelling change (a `µ` can be misread as `m`).

Everything else is forbidden:

- **No new facts.** If a drug, dose, target, or rate is not in the report, it does not appear.
- **No stripped qualifiers.** "Metoprolol only after ≥3 days of alpha-blockade" never becomes
  "give metoprolol". The condition is the point.
- **No rounded-away uncertainty.** A range stays a range; a "non-significant" stays labelled;
  an effect size keeps its CI where the report gave one.
- **No dropped safety items.** Every contraindication, boxed warning, dangerous interaction,
  required monitoring and serious harm in the source reaches the safety band (below). Cutting
  one for layout balance is a safety event, not a design choice.
- **No laundered gaps.** A `[unverified]` or explicitly-thin point is omitted or marked as a
  gap — never rendered as a confident tile.
- **No unlabelled schematics.** An illustrative figure — a drawn curve, a timeline — that shows
  a *shape* rather than a measurement must say so (*illustrative — not measured data*) and may
  carry only numbers already in the report (a target threshold, a labelled band). A schematic
  drawn to a fabricated axis, or read as real data, is the same failure as an invented tile.

If honouring all of this leaves a panel that will not fit, the panel shrinks or splits — the
*content* does not bend.

## The safety band — by clinical class, not by keyword

The band is the most-trusted strip on the page, so what goes on it is decided by what an item
*is*, not by whether its sentence says "avoid". Gather safety content from wherever the source
put it: its marked safety block (pubmed-research-note writes one whenever its verdict doses or
endorses an agent), harms and adverse-effect sections, special populations, "where the verdict
inverts", and any label warnings it quotes. For a legacy report with no safety block, sweep the
full text for these classes. Then place each item by class:

| What the source states | Where it goes | Mark |
|---|---|---|
| Contraindication, boxed warning, "never / do not use" because of a harm | the CRITICAL SAFETY band | 🚫 |
| Warning or precaution, dangerous interaction, serious harm with its rate or NNH, pregnancy / lactation risk | the CRITICAL SAFETY band | ⚠ |
| Required monitoring — what, how often, the action threshold | a monitoring cell in the band (or a monitoring card) | ⏱ Monitor |
| No benefit shown — a null trial, futility, "stop buying" | a neutral panel headed "Not recommended — no benefit shown", with the source's reason — never the crimson band | — |
| A practice directive ("never promise X", "measure before Y") | a rule callout (`.card.rule`) | ⚠ rule |
| A boundary where the verdict inverts ("only if", "unless") | the ladder, branch or card that carries the condition | — |

- **Keep the source's modality.** A judgement ("I would not go above 15 mg"), a recommendation
  or an "outside the evidence" statement is never upgraded to a 🚫 prohibition. It goes under ⚠,
  or into a rule callout, worded with the source's own verb.
- **The "why" is the source's own reason** from the same passage — never an adjacent number
  that happens to sit nearby.
- **The header follows the content.** "CRITICAL SAFETY — MEDICATIONS / ACTIONS TO AVOID" when at
  least one 🚫 or ⚠ item exists; "MONITORING & CAUTIONS" when monitoring is all there is.
- **Coverage is always visible.** Under the header, one line says what the source assessed:
  "From the source's safety section. Not assessed in the source: <agents or items>." When the
  source carries no safety content at all, the band still renders, neutral: "Safety: the source
  report does not address contraindications or interactions — check the current label before
  prescribing." Silence on the page never reads as "nothing to avoid".
- **Thin source, stop and offer.** When the infographic will show a dose or endorse an agent and
  the source has no safety content for it, say so at Step 0 and offer a pubmed-research-note
  harms-and-interactions pass before rendering.
- **The Close** names the band's path (marked safety block, or full-text sweep) and its
  coverage line.

## Provenance carried into the render

Pull these from the source and put them in the footer so the infographic stays auditable:

- The source report's **title** and **date**, and its counts (`PubMed N · trials N`).
- Its **`## Sources` mapping** — the topic→DOI / NCT lines — as a collapsed Sources list.
  Upstream Sources map topics, not single claims, so a tile traces back through the topic
  phrase that covers it.
- The standing disclaimer line: *clinical reference aid — not a substitute for clinical
  judgment or local protocol.*

A clinician who spots a surprising tile must be able to trace it back in one hop. If the source
list cannot support the tiles on the page, the tiles are wrong, not the list.

## Handoff parameters

- **To comprehensive-review / pubmed-research-note (generate):** the topic or decision, plus a
  render brief: the output will also be rendered as a clinical reference, so it should carry —
  at its full normal depth, never shortened for the card — a marked verdict or key directives
  with confidence; doses with their label country; a marked safety block (contraindications,
  boxed warnings, key interactions, monitoring schedule and thresholds, pregnancy), each item
  sourced or marked "not assessed". Let their intent-lock gate run — do not pre-empt it.
- **To vault-keeper (file):** the finished `.html` (plus PNG) as an **asset**, a title
  `<Topic> — Infographic`, and the **source report's MOC topic** so the infographic hangs off
  the same map as its source — vault-keeper wires it into that MOC's `## Assets` section and
  links it from the source artifact when one exists. A short companion-note body is optional;
  supply one only when it adds something the MOC line cannot carry.
