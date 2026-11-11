# Field pack — endocrinology

Read this before choosing the view for any endocrine concept. It narrows the menu in
[concept-patterns.md](../concept-patterns.md); the build contract and every rule of the
skill still apply.

## Field rules

- **Default reader:** an endocrinology fellow. Anatomy, hormone names and routine terms may
  appear unexplained; the page teaches the *model* (how the loop behaves, how a test
  separates two states), not the gland. Offer this as the default level at the intent-lock
  gate; the user's answer wins.
- **General lane:** physiology that every textbook agrees on: which hormone drives which, the
  sign of each feedback, the qualitative shape of a curve, what moves first.
- **Clinical lane:** every cut-off, dose, sampling time, test protocol, diagnostic criterion
  and reference range. These come from a sourced report (a society guideline or a primary
  paper, through **pubmed-research-note**; **comprehensive-review** covers psychiatric topics
  only). A page that needs one and has no source shows the shape without the number and
  labels it *illustrative*.
- **Units and ranges:** use the unit system of the source and name it; never convert
  silently. Reference ranges depend on the assay and the laboratory, so a range on the page
  carries its source or the word *illustrative*.
- **Colour roles:** one colour per tier of an axis (releasing hormone, trophic hormone,
  target hormone), the same in the formula, the numbers and the picture. Feedback arrows take
  the colour of the hormone that carries the signal.
- **Toy scale, said once in the footer:** a toy loop keeps the direction and sign of each
  signal and the order in which levels change. It drops pulsatility, binding proteins,
  half-lives and the days-to-weeks time scale unless the lesson is about one of those.

## Families

### E1. Feedback axes (computed)

*HPA (CRH → ACTH → cortisol) · thyroid (TRH → TSH → T4/T3) · gonadal (GnRH → LH/FSH → sex
steroids, inhibin) · GH (GHRH and somatostatin → GH → IGF-1) · prolactin (held down by
dopamine: the axis that runs on inhibition)*

- **State** — the level at each tier, the set point, the strength of the feedback.
- **Model** — a negative-feedback loop: the drive to each tier falls as the target hormone
  rises. Any saturating inhibition will do; say which form is typed.
- **View** — the loop drawn top to bottom, three tiers. Fill shows a level, arrow thickness
  shows a drive, the feedback arrow thins as it bites.
- **What-if cases** — the gland fails (target low, trophic high) · the pituitary fails (both
  low) · hormone given from outside (target high, trophic suppressed) · the gland secretes on
  its own (target high, trophic suppressed) against a driven gland (both high) · the stalk is
  cut (prolactin rises while the other pituitary hormones fall).
- **Invariants** — at rest, drive and feedback balance; stronger feedback gives a lower
  resting trophic level; with no gland output the trophic level sits at its ceiling.
- **The misconception to kill** — that a trophic hormone "in the normal range" means the
  pituitary is working. A trophic level is read against the target hormone: normal is wrong
  when the target is low.
- **Also here** — the thyroid's steep response: a small change in free T4 moves TSH many
  times over. View: free T4 against TSH on a log axis. Slope figures are clinical lane.

### E2. Dynamic tests (computed shape, sourced protocol)

*Stimulation tests for suspected deficiency · suppression tests for suspected excess · water
deprivation · glucose load*

- **State** — the baseline level, the stimulus, the response over time, and one hidden
  quantity the test is probing (reserve, or autonomy).
- **View** — a time line with the stimulus marked and the response traced after it. The
  expected response is a band, drawn from the source or labelled *illustrative*.
- **What-if cases** — a healthy response · no reserve (flat) · a gland that still answers
  because the failure above it is recent (the test looks normal and is wrong) · an autonomous
  source that does not suppress.
- **Invariants** — the response starts after the stimulus, never before; with zero reserve
  the trace does not rise.
- **The misconception to kill** — that one random level answers the question. Suspect too
  little, stimulate; suspect too much, suppress.
- **Clinical lane** — the agent, dose, sampling times and cut-offs of every named test.

### E3. Rhythms and pulses (computed)

*The cortisol day · pulsatile GnRH and LH · night-time GH · melatonin*

- **State** — the hormone level across 24 hours, the time of a sample, the pulse frequency.
- **View** — a 24-hour trace with a sample marker; the reading under the marker is shown
  beside the day's mean.
- **What-if cases** — sample at the peak against the trough · a flattened rhythm that has
  lost its trough · a shifted day (night work) · the same total dose given in pulses against
  continuously (continuous GnRH switches the axis off).
- **Invariants** — the day's mean does not depend on when the sample is taken; a continuous
  signal of the same mean gives a different downstream response from a pulsed one.
- **The misconception to kill** — that a single sample is "the level".

### E4. Glucose and insulin (computed)

*Secretion against sensitivity · the response to a glucose load · counter-regulation · what
HbA1c averages*

- **State** — insulin sensitivity, insulin secretion, glucose over time.
- **Views** — secretion plotted against sensitivity, a hyperbola with the person as a point
  on or off it · glucose over time after a load.
- **What-if cases** — sensitivity falls and secretion rises to match (the point slides along
  the curve, glucose stays normal) · secretion fails to match (the point drops off the curve)
  · HbA1c for a steady year against a recent change.
- **Invariants** — on the curve, secretion × sensitivity is constant; HbA1c is a weighted
  average in which recent weeks count for more.
- **The misconception to kill** — that a high insulin level shows a healthy beta cell.
  Insulin is read against sensitivity.
- **Clinical lane** — diagnostic thresholds, insulin action profiles, hypoglycaemia
  thresholds, the weights behind HbA1c.

### E5. Calcium, PTH and vitamin D (computed)

- **State** — serum calcium, PTH, the set point, the three fluxes (bone, kidney, gut).
- **Views** — PTH against calcium, a falling S-curve with the person as an operating point ·
  three organs with flux arrows.
- **What-if cases** — the curve shifts right (PTH not suppressed although calcium is high) ·
  a source outside the parathyroids (calcium high, PTH suppressed) · too little vitamin D
  (calcium held by a raised PTH) · no PTH.
- **Invariants** — PTH falls as calcium rises along one curve; a shifted set point moves the
  curve, not the rule.
- **The misconception to kill** — that a "normal" PTH with a high calcium is normal.
- **Clinical lane** — every threshold and ratio that separates the causes.

### E6. Water and sodium (computed)

- **State** — plasma osmolality, vasopressin, urine concentration, water in and out.
- **View** — vasopressin against osmolality, a straight line above a threshold · urine
  concentration following it.
- **What-if cases** — no vasopressin against a kidney that ignores it (told apart by the
  response to a given dose) · vasopressin that does not switch off at low osmolality ·
  drinking beyond the kidney's ability to dilute.
- **Invariants** — below the threshold vasopressin is off; urine cannot be more dilute than
  the kidney's floor.
- **The misconception to kill** — that low sodium means sodium has been lost. It is usually
  water that has been kept.
- **Clinical lane** — test thresholds, correction rates, doses.

### E7. Hormone action at the cell (computed or watch)

*Membrane receptors (fast, second messengers) against nuclear receptors (slow, gene
transcription) · free against bound hormone · resistance*

- **Views** — the cascade as scenes (watch mode) · two pools, bound and free, with the
  feedback loop reading only the free pool.
- **What-if cases** — binding protein rises (total goes up, free returns to where it was once
  the loop has settled) · a receptor that does not answer (hormone high, effect low).
- **Invariants** — the loop regulates the free level; total = free + bound.
- **The misconception to kill** — that the total level is the active level.

### E8. Classifications and work-ups (authored)

*Thyroid function patterns · an adrenal incidentaloma work-up · a thyroid nodule pathway ·
the MEN syndromes · screening for secondary hypertension · types of diabetes*

Use family 12: **Reveal** or **Sort** for a pattern grid, **Branch** for a work-up,
**Sort / match** for syndromes, **Compare** for two conditions that are confused. All of it
is clinical lane: each item carries its source, and the footer says the page is authored.

## Picking the family

| The concept is about | Family | Mode |
|---|---|---|
| Who drives whom, and reading two levels together | E1 | computed |
| What a test shows and why it can mislead | E2 | computed shape, sourced numbers |
| When a sample is taken | E3 | computed |
| Reading insulin or HbA1c | E4 | computed |
| Calcium and PTH read together | E5 | computed |
| Thirst, urine and sodium | E6 | computed |
| How a hormone acts, free and bound | E7 | computed or watch |
| A classification or a step-by-step work-up | E8 | authored |
| A drug's kinetics or dose–response | family 10 in concept-patterns.md | computed |
