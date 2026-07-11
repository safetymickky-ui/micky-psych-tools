# The review arc — sections, floors, and search recipes

The canonical skeleton of a whole-disorder review. Presence is mandatory for every
section; depth follows the emphasis locked in Step 0. A thin section is written thin and
says so — it never vanishes.

## Per-section contract

| # | Section | What it must carry | Source floor | Search recipe |
|---|---------|--------------------|--------------|---------------|
| 1 | Definition & nosology | Current diagnostic construct, DSM-5-TR/ICD-11 placement, how the boundaries moved | Classification texts, seminal papers — age is legitimate here | `<disorder> AND (nosology OR classification OR "diagnostic criteria")` |
| 2 | Epidemiology | Prevalence with denominator and instrument, incidence, sex/age distribution, cross-cultural signal | Register/cohort studies, national surveys | `<disorder> AND (prevalence OR epidemiology) AND (survey OR cohort)` |
| 3 | Etiology & pathophysiology | Genetics (heritability with its estimate), neurobiology, psychosocial models — labelled by evidence strength | Meta-analyses > imaging/GWAS primaries; mechanism claims marked as such | `<disorder> AND (etiology OR pathophysiology OR genetics OR neuroimaging)` |
| 4 | Clinical features & course | Presentation, onset, trajectory, functional impact — numbers for onset age and episode duration | Longitudinal cohorts | `<disorder> AND ("clinical features" OR phenomenology OR "longitudinal course")` |
| 5 | Diagnosis & assessment | Criteria in practice, validated instruments with psychometrics (sensitivity/specificity, cutoffs) | Validation studies | `<disorder> AND (assessment OR "rating scale" OR screening) AND validation` |
| 6 | Differential & comorbidity | The look-alikes and the co-travellers, each with a discriminating feature; comorbidity rates | Cohort/epidemiological studies | `<disorder> AND (comorbidity OR "differential diagnosis")` |
| 7 | Treatment | Every modality: pharmacological, psychotherapeutic, neuromodulation/somatic, psychosocial — effect sizes, NNT/NNH, doses | Guidelines, meta-analyses, RCTs — **plus the registry check, mandatory** | `<disorder> AND treatment AND (guideline OR meta-analysis OR "randomized controlled trial")` |
| 8 | Special populations | Children/adolescents, older adults, pregnancy, medical comorbidity — only those the literature actually addresses | RCT subgroups, dedicated trials | `<disorder> AND (pediatric OR adolescent OR geriatric OR pregnancy)` |
| 9 | Prognosis | Remission/relapse/recovery rates with time horizons, mortality signal, predictors | Long-term follow-up cohorts | `<disorder> AND (prognosis OR remission OR relapse OR mortality)` |
| 10 | Controversies & future directions | Live disagreements, replication status, pipeline: ongoing and completed-unpublished registered trials with readout dates | The registry harvest from §7 lands here | ClinicalTrials.gov: condition = `<disorder>`, recruiting + completed-no-results |

## Merge rules

- Adjacent sections may merge when the literature is thin for both (e.g. §4+§9 for a rare
  disorder) — the merged header's first line names the merge.
- §7 keeps its H3 modality split even when a modality is empty; an empty modality gets one
  line saying no controlled evidence exists. That absence is a finding.
- Nothing merges into §7 — treatment never absorbs the review.

## Registry recipe (§7 → §10)

Three passes on ClinicalTrials.gov for the disorder: (1) results newly posted since the
newest guideline; (2) completed with nothing posted — publication-bias flags; (3) large
ongoing trials with expected readouts. Each entry lands in §10 as
`NCT NNNNNNNN — topic, status, n, readout YYYY-MM`.

## Budget

15–30 sources across the whole review. If a single section wants more than 8, the
emphasis lock from Step 0 has probably been ignored — re-read it before searching on.
