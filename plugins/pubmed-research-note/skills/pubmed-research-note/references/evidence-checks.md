# Evidence Checks — provenance, appraisal, counter-evidence, dose and safety, confidence, claim check

Read before your first search, and again before you show the report. These six checks are
what make a report *correct*, not only well shaped. They exist because measured runs of this
skill were 92–95% accurate at the claim level, and the errors sat exactly where they hurt
most: in the verdict, the adjudication, and the summary sentences — not in the per-study
paragraphs. An abstract hid a null result that only the full text reported. The first label
found was sixteen years out of date and missed a warning the current label carries. Each
check below closes one of those holes.

None of them changes the report's machine-read shape: the dated count line, the preface
block and the `## Sources` line grammar stay exactly as SKILL.md defines them. New rigor goes
into the prose, or inside a Sources line's topic phrase.

---

## 1. Provenance — every number comes from a record opened in this run

- **The rule.** Every number in the report comes from a record you fetched in this run: an
  abstract, a PMC full text, a registry results page, a label. Never from memory — not even a
  number you are sure of.
- **Full text for load-bearing studies.** For each study the verdict rests on, open the full
  text whenever PMC or an open-access copy has it (`convert_article_ids` → PMCID →
  `get_full_text_article`). Abstracts drop null secondary outcomes, dropout and harms; the
  depth contract cannot be met from an abstract alone. When no full text is obtainable, say
  so in the same sentence as the number: `(abstract only)`.
- **Tag second-hand and derived numbers in the same sentence.**
  - `registry results, unpublished` — a number read from a ClinicalTrials.gov results page
    with no paper behind it.
  - `as reported in <the review, described>` — a primary trial's number taken from a
    review's table, not from the trial's own report. Describe the review ("as reported in a
    2013 meta-analysis of 8 RCTs"), never by author and year — prose stays citation-free.
  - `calculated` — an NNT, absolute difference or percentage you derived; give the inputs.
- **Mark inference.** A mechanism, a causal reading or a generalisation the sources do not
  state is introduced with `my inference:` — so the reader can tell your reasoning from the
  evidence. Mechanism prose built from pharmacology is legitimate and needs no number; it
  needs this marker when it goes beyond what a cited source says.
- **Introduce every cited study by design and n** — "a 304-patient double-blind RCT", not
  "a VA study".
- **Look for notices.** When `get_article_metadata` shows a correction, a retraction, or an
  "Update in" link (a preprint later published), use the final version and say so.

## 2. Appraisal — risk of bias and replication for each load-bearing study

Each load-bearing study's paragraph carries a one-line risk-of-bias judgement and its
replication status. Name the tool the judgement follows, by design:

| Design | Judge by | The line names |
|---|---|---|
| RCT | RoB 2 domains | the weakest domain: randomisation / allocation concealment, deviations (blinding), missing data (attrition, ITT), outcome measurement, selective reporting |
| Non-randomised study | ROBINS-I (ROBINS-E for exposures) | confounding control, selection, exposure/outcome measurement |
| Systematic review / meta-analysis | AMSTAR 2 critical domains | protocol, search date, RoB of included studies used in the synthesis, primary-study overlap with any other review you cite |
| Mendelian randomisation | instrument checks | instrument strength (F-statistic), pleiotropy-robust methods, power for the effect you would care about |

Take the judgement from the study's own methods and limitations — or from a review that rated
it — never from its reputation. Record funding and conflicts of interest when they bear on
the result.

For a **load-bearing meta-analysis**, also report:

- heterogeneity — I² with τ² or a prediction interval, and its named source if the authors
  found one;
- small-study effects — funnel plot or Egger result, or "not assessable (<10 studies)";
- **subgroup credibility** before a subgroup becomes a condition of the verdict: was it
  pre-specified, is it a within-trial comparison, is it plausible, has it replicated? A
  subgroup that fails these is hypothesis-generating and is written that way.

Three meta-analyses that pool the same trials are one piece of evidence, not three. Say how
much they overlap before you call them replication.

## 3. Counter-evidence — search against the provisional verdict

Once you have a provisional verdict, run **one deliberately adversarial search against it**:
search for the strongest evidence for the *opposite* conclusion.

- Provisional verdict positive → search the null and negative literature
  (`AND (negative OR null OR "failed to" OR "no significant")`, or the known large trial by
  name).
- Provisional verdict null, negative or "debunked" → search the positive literature:
  meta-analyses and prospective designs that report an effect
  (`AND (Meta-Analysis[Publication Type] OR systematic[sb])` with the outcome, then a
  prospective-cohort search when the claim is observational).
- Then a **recency sweep**: for each load-bearing sub-question, search for systematic
  reviews newer than the newest one you cite (`sort: pub_date`, `date_from` = that review's
  date).

The report **names the strongest opposing study or synthesis** and, in one or two sentences,
says why it does not change the verdict — its design, its effect metric (for example a
within-group pre–post effect versus a between-group one), its population, or its risk of
bias. If it *does* change the verdict, the verdict changes. "All the evidence points one
way" is a claim you may make only after this search came back empty — and then say that it
did.

## 4. Dose and safety — whenever the verdict names a dose or endorses an agent

This step is mandatory when the verdict names a dose, a range or a titration, or recommends
an agent. It is where a report can hurt a patient, so it does not run from memory.

- **Open an official label in this run.** Name, in the sentence, the regulator and country,
  the label's own revision date, and whether the use is on-label or off-label. Order of
  sources:
  1. **Thai FDA** first (the user practises in Thailand): `firecrawl search "<drug>
     เอกสารกำกับยา site:fda.moph.go.th"`, then scrape the ndi.fda.moph.go.th drug-detail page
     or the label PDF it lists. The direct NDI URL is script-driven and often returns 404;
     search first.
  2. **US FDA**: DailyMed SPL (`https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name=<drug>`
     → the setid → the SPL's DOSAGE AND ADMINISTRATION and WARNINGS sections); openFDA
     `label.json` as fallback.
  3. **EMA**: the EPAR product information (SmPC sections 4.1–4.6).
  Cite the document you actually read — not a neighbouring one (an RMP is not an SmPC).
  When a label could not be checked (no Thai registration found, a fetch failed), say so
  in the dose sentence itself: "Thai FDA label not checked in this run".
- **Use the newest label.** A search hit can be an archived version (the measured case: a
  2009 DailyMed label missing a warning the 2025 label carries). Use the newest version on
  the regulator's own site — DailyMed's current SPL version for that product, the latest
  approval date on the Thai FDA drug page, the current EPAR. Cite an older label only as
  superseded, and say what changed when it matters.
- **Off-label and supplement doses** trace to the trials that tested that dose: name the
  design, n and population, and tie every efficacy figure you quote to the dose arm that
  produced it. If you recommend a dose different from the arms that produced the figure,
  say so and why. If no label exists, or the drug is not available in Thailand, say that
  plainly.
- **Safety communications.** Sweep regulator safety communications for the agent (FDA,
  EMA, MHRA, Thai FDA). For an agent with no drug label — a supplement, a herbal — this
  sweep is the safety evidence: include national food-safety and toxicology agencies. A
  live safety action is part of the verdict.
- **A marked safety block.** When the verdict doses or endorses an agent, the report carries
  a clearly marked safety section (its own heading, e.g. `## Safety — contraindications,
  interactions, monitoring`) listing, for each endorsed agent: contraindications, boxed
  warnings, key interactions, required monitoring, and pregnancy/lactation — each item with
  its reason, in numbers where the source gives them, and sourced. An item you did not
  assess is written as `not assessed`, never left out. When nothing applies, say so in one
  line ("No contraindication or interaction identified in the evidence searched"). Downstream renderers (the
  clinical-infographic skill) build their safety banner from this block, so silence here
  reads as "nothing to avoid".
- **In `## Sources`**, a label line keeps the web grammar with the revision inside the
  topic phrase: `<topic> (<regulator> label, revised YYYY-MM) — <URL> (accessed YYYY-MM-DD)`.

## 5. Confidence — graded, per outcome, in both directions

The verdict carries its confidence as the literal label `Confidence:` followed by one level
of one fixed scale, the GRADE certainty levels: **high | moderate | low | very low**. "Very
low" means no adequate study exists and the honest answer is *unknown*. (`moderate-low` and
`moderate-high` are retired — they are not on the scale.)

- **Rate the outcome that drives the decision**, not the evidence in general. Start from
  design (randomised evidence starts high; observational and Mendelian-randomisation
  evidence starts low), then:
  - **downgrade** for risk of bias, inconsistency, indirectness, imprecision (the CI crosses
    the decision threshold or the minimal important difference) and publication or
    small-study bias;
  - **upgrade** observational evidence for a large effect or a dose–response.
- **"Not higher because <domain>"** — the clause names the downgrading domain(s). When the
  rating could be challenged as too harsh, add "not lower because …".
- **Several outcomes of different certainty** (efficacy high, the patient-relevant outcome
  low, long-term safety very low) get a compact certainty table — outcome → effect (absolute,
  at a stated baseline risk) → certainty → reason — and the headline confidence follows the
  decision-driving outcome. Never let a strong surrogate hide a weak patient outcome.
- **Indirectness is symmetric.** A population, dose, comparator or endpoint gap that makes
  you discount evidence *for* a claim discounts evidence *against* it by the same rule. A
  null in 75-year-olds is as indirect for 40-year-olds as a positive result would be.
- **Absence of evidence is very low certainty, not a negative finding.** "Not tested at
  adequate size" and "tested and did not hold" are different verdicts.

## 6. Claim check — between Write and Show

After the report is written and before it is shown or filed, check it against its sources.
Errors enter when you summarise and generalise, so this check targets the sentences that do
that.

1. **Build a claim ledger** (working notes, not part of the report) covering: the verdict,
   the confidence clause, every adjudication sentence, every heading, every summary or
   closing sentence, and every number.
2. **For each entry, re-open the source passage** — the results, and the methods and
   limitations for quality words — and check:
   - the number, its unit, its comparator and its arm;
   - the population the number came from (a generalisation such as "women on drug X" must
     match the people who produced the figure; a subgroup n is not the total n);
   - design and quality words (double-blind, "verified", ITT, "the only", "every") against
     the study's own methods and limitations;
   - primary versus secondary endpoint, the source's own certainty rating, and publication
     status;
   - each heading and summary sentence against the numbers beneath it.
3. **Fix every mismatch**, or mark it `[unverified]` in its own sentence. Then re-read the
   verdict and the closing line against the confidence clause.
4. **Prefer an independent pass.** When a subagent is available, give it the report and the
   fetched records and ask it to check the ledger; a second reader catches what the writer
   cannot.

The Close reports the result in its existing two lines: "claim check: N claims checked,
N fixed, N marked [unverified]".
