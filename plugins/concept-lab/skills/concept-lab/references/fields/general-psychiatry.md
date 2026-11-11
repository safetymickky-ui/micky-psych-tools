# Field pack — general psychiatry

Read this before choosing the view for any concept in clinical psychiatry. It narrows the
menu in [concept-patterns.md](../concept-patterns.md); the build contract and every rule of
the skill still apply.

## Field rules

- **Default reader:** a board-certified psychiatrist. Clinical background may appear
  unexplained; the page earns its place by showing what experts still get wrong or what is
  hard to explain to a trainee. When the page is for residents or students the intent-lock
  gate says so, and the level drops.
- **Clinical lane is the rule here.** Criteria, thresholds, scale cut-offs, response and
  relapse rates, doses, interactions and pathway steps all come from a sourced report:
  **comprehensive-review** for a whole disorder, **pubmed-research-note** for one decision.
  Nothing clinical is written from memory.
- **General lane is narrow:** the logic of how criteria combine, arithmetic the page computes
  from sourced inputs (NNT, predictive value, overlap of two distributions), and textbook
  definitions of measurement terms.
- **Diagnostic criteria are paraphrased, never copied.** DSM and ICD wording is under
  copyright: state each criterion in the page's own words and cite the manual.
- **No patient.** A case on the page is invented and says so. Nothing from a real person.
- **Mechanism claims are graded.** A proposed mechanism is labelled as proposed, with its
  source; it is never drawn as if it were established anatomy.
- **Colour roles:** one colour per state of illness (well, symptomatic, in episode) on a
  course diagram; one colour per group on a comparison. Status colours always carry a word.

## Families

### P1. Illness course over time (computed schematic, or watch)

*Response, remission, recovery, relapse, recurrence · prodrome to first episode · partial
remission with residual symptoms · staging · rapid cycling*

- **State** — severity over time, the thresholds that define each term, the treatment phase.
- **View** — one severity curve across months with the thresholds as bands. Each term is a
  region or an event on that one curve.
- **What-if cases** — treatment stopped early (symptoms return inside the same episode: a
  relapse) against a new episode after recovery (a recurrence) · improvement that never
  crosses the remission line · many short episodes in a year.
- **Invariants** — every term is decided by the curve and the thresholds, never typed onto
  the picture; remission implies response, not the reverse.
- **The misconception to kill** — that response and remission, or relapse and recurrence,
  are the same word.
- **Lanes** — the scheme is general; the thresholds and durations are clinical and sourced.
  A curve with no patient data behind it is labelled *illustrative*.

### P2. Criteria logic (computed)

*"k of n" symptom rules · required core symptoms · duration, impairment and exclusion gates ·
how different two patients with the same diagnosis can be*

- **State** — which symptoms are present, the rule, the gates.
- **Views** — a row of symptom tiles feeding a counter and a chain of gates · a count of the
  symptom combinations that satisfy the rule.
- **What-if cases** — two presentations that both meet the rule and share one symptom · one
  symptom short of the count · every symptom present and an exclusion gate closed.
- **Invariants** — the count of qualifying combinations is computed, not typed (5 of 9 gives
  256; requiring one of two core symptoms leaves 227); a closed gate overrides any count.
- **The misconception to kill** — that one diagnosis names one kind of patient.
- **Clinical lane** — the criteria themselves, paraphrased and cited.

### P3. Numbers that drive decisions (computed from sourced inputs)

*What a rating scale measures · response against remission on a score · effect size · NNT and
NNH · what a positive screen means at a given base rate*

- **Views** — two overlapping distributions for an effect size · an icon array for NNT · a
  natural-frequency tree for a screening test.
- **What-if cases** — the same test in a low-prevalence setting (most positives are false) ·
  a "significant" effect whose distributions nearly coincide · a 50% fall in score that still
  sits above the remission cut-off.
- **Invariants** — NNT = 1 / absolute risk difference; the tree's branches add up to the
  population; predictive value falls with prevalence at fixed sensitivity and specificity.
- **The misconception to kill** — that a significant result is a large one, or that a
  positive screen is a diagnosis.
- **Clinical lane** — every event rate, cut-off, sensitivity and specificity typed into the
  page.

### P4. Drugs in practice

Kinetics, occupancy and dose–response belong to **family 10** in concept-patterns.md. This
field adds what family 10 does not hold:

- **Onset lag (computed schematic)** — receptor occupancy within hours against clinical
  change over weeks, on one time axis. Misconception: day-one occupancy is day-one effect.
- **Switching (authored or computed)** — a cross-taper as two overlapping curves; the
  schedule is sourced.
- **Adverse-effect profiles (authored, Compare)** — effects grouped by the receptor that
  produces them, across two or three drugs.
- **Interactions (authored Reveal, or the clearance toggle of family 10).**

### P5. Formulation and psychological models (authored, sometimes computed)

*The four-P grid · defense mechanisms by maturity · stress and vulnerability · the cognitive
cycle of panic or depression · attachment patterns · stages of change*

- **Patterns** — **Sort** for a hierarchy or a grid, **Reveal** for a set of patterns,
  **Branch** for stages, and watch mode for a cycle that feeds itself.
- **Stress–vulnerability is computed:** liability plus stress against a threshold, with the
  person as a point. What-if: the same stress on two liabilities.
- **The misconception to kill** — named per concept in the lab spec; for a cycle, that it
  has a first cause.

### P6. Differentials and pathways (authored)

*Conditions that are confused (delirium, dementia, depression; serotonin syndrome and
neuroleptic malignant syndrome; bipolar disorder and borderline personality disorder) · a
first-episode work-up · steps of a capacity or risk assessment*

- **Patterns** — **Compare** with one switch that changes the case, or **Branch** walked one
  finding at a time. Presets include the route where the common shortcut goes wrong.
- **All clinical lane.** Every distinguishing feature and every step carries its source.

### P7. Bridges to computational psychiatry

A symptom explained by a model parameter (reward learning in anhedonia, the balance of
habitual and goal-directed control in compulsivity, the weight given to prior beliefs in
psychosis, estimates of volatility in anxiety). Build the model from
[computational-psychiatry.md](computational-psychiatry.md). The claim that links the symptom
to the parameter is a published finding: it carries its source and the word *proposed*.

## Picking the family

| The concept is about | Family | Mode |
|---|---|---|
| How an illness unfolds, and the words for it | P1 | computed schematic or watch |
| How a diagnosis is put together | P2 | computed |
| A scale, an effect size, NNT, a screening result | P3 | computed, sourced inputs |
| A drug's level, occupancy or dose–response | family 10 | computed |
| Onset, switching, side-effect profiles | P4 | authored or computed |
| A psychological model or a formulation frame | P5 | authored, sometimes computed |
| Two conditions told apart, or a work-up | P6 | authored |
| A symptom as a model parameter | P7, then the comp psych pack | computed |
