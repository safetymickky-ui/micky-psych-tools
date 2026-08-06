# Plugin brainstorm — 2026-08-06

Twelve candidate plugins generated against the owner profile and scored for overlap against the
13 existing marketplace plugins plus the user-level psychiatry skills (`exam-analysis`,
`crq-essay-review`, `daily-random-review`, `obsidian-knowledge-vault`, `psych-case-reconstruct`,
`gcal-shift-schedule`, `expert-psychiatry-presentations`).

Scores are profileFit / novelty / feasibility / impact, each 1–5.

## The headline finding — the exam loop is open at the generate end

The study pipeline runs **discover → atomize → sit → grade → weakness map**, and every stage has an
owner except one. Nothing authors the questions.

Worse, this is a live routing bug, not just a gap. Three skills explicitly disclaim item
generation, and the one pointer that names a destination points at a plugin that does not do it:

> `obsidian-knowledge-vault` — "NOT for generating quiz questions (use comprehensive-review)"

`comprehensive-review` writes whole-disorder textbook chapters. It has never generated an exam
item and its description says nothing about doing so. That pointer is dangling and should be
repointed at whatever fills this gap (or dropped) regardless of which plugin gets built next.

## Ranked candidates

| # | Plugin | Score | Verdict | Closest existing | Overlap |
| --- | --- | --- | --- | --- | --- |
| 1 | `board-item-forge` | 19 | keep | comprehensive-review (stale pointer only) | low |
| 2 | `clinical-algorithm` | 18 | keep | clinical-infographic | low |
| 3 | `case-formulator` | 18 | keep | psych-case-reconstruct | low |
| 4 | `risk-scaffold` | 18 | sharpen → pair with #3 | case-formulator | medium |
| 5 | `thai-psychoed-handout` | 18 | keep | clinical-infographic | medium |
| 6 | `long-case-viva` | 17 | keep | crq-essay-review | low |
| 7 | `recall-deck` | 17 | keep | obsidian-knowledge-vault | low |
| 8 | `recall-engine` | 16 | merge into #7 | recall-deck | — |
| 9 | `journal-club-appraisal` | 14 | ship as a 2nd skill inside pubmed-research-note | pubmed-research-note | medium |
| 10 | `residency-logbook` | 13 | sharpen or skip | gcal-shift-schedule | low |
| 11 | `psych-med-sanity` | 11 | kill | — | low |
| 12 | `call-load-analyzer` | 9 | fold into gcal-shift-schedule | gcal-shift-schedule | high |

---

## 1. `board-item-forge` — 19 — recommended next build

**Authors exam-faithful Thai-board practice items, then stops.**

MCQ with a clinical vignette lead-in and a one-line rationale on *every* distractor (why it is
plausible-but-wrong — that is the pedagogical payload, not the trivia); CRQ stems with itemized
model answers and explicit mark allocation per point; Essay prompts with weighted outline rubrics;
OSCE/long-case station briefs with examiner marking schemes and a standardized-patient script.
Thai-English code-switched to match how the real exam and his notes read, tagged to a board
blueprint code, and wikilinked back to the source note.

- **Boundary:** stops dead at producing questions + answer keys. Grading goes back to
  `exam-analysis` and `crq-essay-review`; explanatory prose goes back to `comprehensive-review`.
- **Pipeline:** intent-lock Step 0 → facts from a named vault note or sourced report (or route to
  `comprehensive-review` / `daily-random-review` to create one first) → item bank filed via
  `vault-keeper` → sat attempts drop into `exam-analysis`, whose weakness map loops back in as the
  next generation target. This is the missing ASSESS stage that closes the loop.
- **Hard gate:** every keyed-correct answer and distractor rationale must trace to a named source.
  A fabricated "correct" answer is worse than no item.
- **Components:** one skill + `/forge-items [topic-or-note]`; references hold the blueprint map,
  per-format templates, and a difficulty calibration rubric.

**Why this one first:** highest score, the clearest structural hole, uniquely tied to the exam he
is actually sitting, and it makes three existing skills more useful the day it ships.

## 2. `clinical-algorithm` — 18

**A sourced guideline rendered as a traversable decision tree.**

The render family has no branching target: `clinical-infographic` is a poster you scan,
`concept-animation` a linear film you watch, `ml-concept-lab` a live-computed CS explorable. But
guidelines *are* branching procedures ("inadequate response at 4 weeks and X → switch vs augment").
This renders one as a self-contained interactive HTML tree — click a node for its sourced
rationale, dose and monitoring; highlight a path; every node carries its contraindication escape
hatch — plus a validated Mermaid source (the Mermaid MCP is already wired in-session).

- **Load-bearing rule:** if a topic has no real branching it degrades into a poster — refuse and
  redirect to `clinical-infographic`. Unsourced branches are refused, never invented.
- **Highest feasibility of the top five (5/5)** — it reuses the render family's source-resolution
  order and vault filing verbatim.

## 3 + 4. `case-formulator` + `risk-scaffold` — 18 each — ship as ONE plugin, two skills

These scored equally and were generated by the same lens; the critic flagged that they will fight
in the router if shipped separately. The house pattern already solves this — `intent-lock` ships
`intent-lock` + `misread-capture`, `vault-keeper` ships `vault-keeper` + `empty-vault`.

**`case-formulator`** — the reasoning step `psych-case-reconstruct` deliberately refuses. A fixed
arc over a supplied case: problem list → ranked DDx with supporting features, features-*against*,
the one discriminating question that moves each, and a mandatory can't-miss-organic-mimic row
(delirium, thyroid, substance/withdrawal, autoimmune, structural) → a Predisposing/Precipitating/
Perpetuating/Protective × Bio/Psych/Social grid → a Thai-English formulation narrative → a workup
skeleton. Every ward admission, every OPD new patient, and the board long-case need exactly this.

**`risk-scaffold`** — the deep single-axis ER/on-call instrument: static / dynamic / protective
factors with acute warning signs split from chronic baseline, a formulation narrative that
explicitly refuses single-score reduction, a modifiable-factor → intervention map, a
Stanley-Brown-style safety plan, and a chart-ready Thai-English risk note. Structured professional
judgment, not a SAD-PERSONS number.

- **Split of labour:** `case-formulator` carries a one-line risk axis and delegates depth here.
- **Safety scaffolding is mandatory for both:** stamped as a study/formulation aid and a
  decision-support *draft* the resident reviews and signs, never a care order; vault filing of
  identifiable cases defaults OFF.
- `psych-med-sanity` (killed, below) survives only as a mechanism-class sub-step of the workup here.

## 5. `thai-psychoed-handout` — 18

**Lay-Thai patient/family psychoeducation from a sourced report.** Every artifact in the
marketplace is clinician-facing and English-technical. Nothing produces the sheet he hands a
family at discharge: what the condition or drug is, what to expect, common side effects, a
mandatory danger-signs box, when to come back — grade-6 Thai, stigma-aware, family-as-caregiver
framing.

- **Audience and register are the entire identity.** A machine-checkable reading-level gate plus a
  hard ban on prescriber-facing content (dosing tables, avoid-lists) is the only thing keeping it
  from being a second `clinical-infographic`. That boundary must be enforced, not merely stated.
- Facts still come only from a sourced report; renders as printable Thai HTML (+ optional PDF);
  files as a patient-education asset via `vault-keeper`.
- Framed and rendered as a clinician-authored draft he signs before anyone receives it.

## 6. `long-case-viva` — 17

**A live Thai examiner for the oral.** Presents a station with a hidden marking scheme, probes turn
by turn — deeper on strong answers, graded hints on weak ones — enforces a soft timer, plays
examiner and standardized patient without breaking role, then debriefs in examiner Thai with a
per-axis score tied mark-by-mark to what he actually said, model answers for dropped points, and a
weakness handoff.

Genuinely a new genre for this repo: every render plugin is a one-shot artifact, and
`intent-lock` / `decision-interview` interview about the *task*, not simulate an *exam*. It is also
the one board format he cannot rehearse alone.

**Feasibility is the catch (3/5)** — stateful adaptive probing against a hidden scheme is the
hardest build in the batch. Natural fit as a second skill added to `board-item-forge`'s plugin at
v0.2.0 rather than a parallel v0.1.0: forge makes the written items, viva rehearses the oral.

## 7 (+8). `recall-deck` — 17 — absorbing `recall-engine`

Two lenses independently found the same orphaned transform: notes are authored
(`obsidian-knowledge-vault`) and weaknesses are mapped (`exam-analysis`), but nothing projects
either into retrieval practice. They proposed two scopes, and the lean one wins.

**Ship the export transform.** Pull atomic notes for a topic — or a weakness list seeded by
`exam-analysis` — via `vault-keeper` query; project them into cloze deletions over doses and
criteria, Q→A cards from headers and wikilink targets, and "list the N features of X" prompts;
tag every card to the board blueprint; keep the source backlink on the card back; dedup against
prior exports so re-runs only add new material. Emit an Anki-importable CSV plus a printable md
quiz.

**Do not build the SM-2 scheduler** (`recall-engine`, 16). An in-repo JSON forgetting-curve ledger
plus Google Calendar writes plus Anki export is three engineering concerns bolted together, and a
buggy interval update silently corrupts the whole curve. Anki is already a world-class SRS engine
— export to it and let it schedule. Weakness-biased selection and blueprint tagging are what make
this his and not a generic notes→Anki exporter; leave calendar blocks as an opt-in add-on at most.

## 9. `journal-club-appraisal` — 14 — not a plugin

A per-paper RoB2 / ROBINS-I / QUADAS-2 / AMSTAR-2 table + GRADE + discussion questions is a real
deliverable `pubmed-research-note` does not make — dissecting *one* study is a different reading
task from synthesizing *many* into a decision. But it borrows that plugin's fetch engines,
intent-lock gate and vault filing wholesale, which makes it thin as a standalone 14th plugin.

**Ship it as a second skill co-located inside `pubmed-research-note`,** holding the boundary at
single-paper methodological appraisal and handing any "so should I use it" synthesis back to the
host skill.

## 10. `residency-logbook` — 13 — only if ingestion is automatic

Tracking cases, procedures and EPAs against the Thai Board eligibility matrix is genuinely unowned
and board-specific, but it is a stateful ledger, not a knowledge artifact, and sustained manual
logging is a behavioural commitment a skill cannot enforce. It goes stale in a month and becomes
dead weight.

**Build it only if entries are auto-derived** from `psych-case-reconstruct` outputs and a Google
Calendar read, so nothing is hand-entered. Lock the requirement matrix as owner-verified config and
forbid any drift toward being a clinical record.

## 11. `psych-med-sanity` — 11 — killed

An unsourced LLM pass over drug interactions and reconciliation is the highest fabrication-harm
surface in the batch, the least owner-unique idea (Lexicomp and UpToDate own this outright), and it
violates the repo's load-bearing never-fabricate-a-clinical-fact culture with no engine available
to ground it — per-pair interaction magnitudes are not literature-search answerable. A
self-authored reference table would be a liability, not a plugin.

## 12. `call-load-analyzer` — 9 — fold into `gcal-shift-schedule`

Generic calendar analytics wearing a lab coat. It reads back the exact events
`gcal-shift-schedule` writes, is tightly coupled to that skill's encoding, exploits none of the
owner's leverage, and is once-a-month value. The load / rest-violation report belongs as an
"analyze" mode on the skill that already owns the roster. Drop the swap optimizer.

---

## Recommendation

Build **`board-item-forge`** next, with the source-fidelity gate as a hard rule rather than a
caveat, and repoint the dangling `use comprehensive-review` quiz pointer at it. Add
**`long-case-viva`** as its second skill once the item formats are proven.

If a second plugin is wanted in parallel, **`clinical-algorithm`** is the safest build — highest
feasibility, cleanest boundary, and it fills the render family's one missing information structure.
