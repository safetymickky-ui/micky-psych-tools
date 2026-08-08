# The coverage map — domains, floors, and search recipes

The ten coverage domains of a whole-disorder review, with what each owes the reader and
how to search it. **This is a coverage map and a proven default order — not a mandatory
skeleton.** Every domain must be covered somewhere in the chapter or consciously excluded
in the preface; how the coverage is organized — order, splits, merges, nesting, names —
is designed per topic in Step 1. A thin domain is written thin and says so — it never
vanishes.

## Per-domain contract

| # | Domain | What it must carry | Source floor | Search recipe |
|---|---------|--------------------|--------------|---------------|
| 1 | Definition & nosology | Current diagnostic construct, DSM-5-TR/ICD-11 placement, how the boundaries moved | Classification texts, seminal papers — age is legitimate here | `<disorder> AND (nosology OR classification OR "diagnostic criteria")` |
| 2 | Epidemiology | Prevalence with denominator and instrument, incidence, sex/age distribution, cross-cultural signal | Register/cohort studies, national surveys | `<disorder> AND (prevalence OR epidemiology) AND (survey OR cohort)` |
| 3 | Etiology & pathophysiology | Genetics (heritability with its estimate), neurobiology, psychosocial models — labelled by evidence strength | Meta-analyses > imaging/GWAS primaries; mechanism claims marked as such | `<disorder> AND (etiology OR pathophysiology OR genetics OR neuroimaging)` |
| 4 | Clinical features & course | Presentation, onset, trajectory, functional impact — numbers for onset age and episode duration | Longitudinal cohorts | `<disorder> AND ("clinical features" OR phenomenology OR "longitudinal course")` |
| 5 | Diagnosis & assessment | Criteria in practice, validated instruments with psychometrics (sensitivity/specificity, cutoffs) | Validation studies | `<disorder> AND (assessment OR "rating scale" OR screening) AND validation` |
| 6 | Differential & comorbidity | The look-alikes and the co-travellers, each with a discriminating feature; comorbidity rates | Cohort/epidemiological studies | `<disorder> AND (comorbidity OR "differential diagnosis")` |
| 7 | Treatment | Every modality: pharmacological, psychotherapeutic, neuromodulation/somatic, psychosocial — effect sizes, NNT/NNH, doses, with load-bearing trials in full per-study detail | Guidelines, meta-analyses, RCTs — **plus the registry check, mandatory** | `<disorder> AND treatment AND (guideline OR meta-analysis OR "randomized controlled trial")` |
| 8 | Special populations | Children/adolescents, older adults, pregnancy, medical comorbidity — only those the literature actually addresses | RCT subgroups, dedicated trials | `<disorder> AND (pediatric OR adolescent OR geriatric OR pregnancy)` |
| 9 | Prognosis | Remission/relapse/recovery rates with time horizons, mortality signal, predictors | Long-term follow-up cohorts | `<disorder> AND (prognosis OR remission OR relapse OR mortality)` |
| 10 | Controversies & future directions | Live disagreements, replication status, pipeline: ongoing and completed-unpublished registered trials with readout dates | The registry harvest from §7 lands here | ClinicalTrials.gov: condition = `<disorder>`, recruiting + completed-no-results |

## Structuring the chapter

- The table's order is a proven default for a classic disorder; a device, drug class, or
  treatment modality reshapes the map to its own anatomy (past runs have mapped
  "etiology" → mechanism of action, "clinical features" → what the treatment must target,
  "diagnosis" → patient selection). The domains persist under new names; name the mapping
  in the preface or the section's first line.
- Domains may split into several sections, or fold together when the literature is thin
  for both (e.g. §4+§9 for a rare disorder) — a merged section's first line names the
  merge.
- Sub-headings (H3/H4) are legal anywhere they help navigation. A long section is
  subdivided, not amputated — never cut real content to shorten it.
- An empty treatment modality gets one line saying no controlled evidence exists. That
  absence is a finding.
- **Treatment never absorbs the review** — however the outline is shaped, the
  non-treatment domains keep their standing.

## Registry recipe (§7 → §10)

Three passes on ClinicalTrials.gov for the disorder: (1) results newly posted since the
newest guideline; (2) completed with nothing posted — publication-bias flags; (3) large
ongoing trials with expected readouts. Each entry lands with the forward-looking coverage
as `NCT NNNNNNNN — topic, status, n, readout YYYY-MM`.

## Depth, not budget

There is no source ceiling. Gather as many well-chosen sources as the chapter needs —
past reviews have run from ~20 to 65+ when the locked emphasis demanded drug-by-drug
breadth. The filter is *does this source change or deepen a section*, never a number.
Two disciplines replace the old budget:

- **Load-bearing studies get the full treatment** — design, population, n, comparator,
  endpoint, effect size with CI, as a developed paragraph. Supporting literature may be
  grouped; the studies carrying a section may not be reduced to clauses.
- **Emphasis still governs proportion.** If a domain the user de-emphasized in Step 0 is
  swallowing the search, re-read the lock before searching on — depth follows the locked
  emphasis, coverage stays universal.
