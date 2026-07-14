---
name: comprehensive-review
description: >-
  Writes a comprehensive, textbook-chapter academic review of a whole psychiatric disorder
  or topic from primary literature — the full arc: epidemiology, pathophysiology, clinical
  features, diagnosis, comorbidity, treatment across ALL modalities, course and prognosis —
  never collapsed into a treatment-only report. Use when the user says "comprehensive review
  of X", "full review of X", "whole-disorder review", "academic review", "review the whole
  topic", "รีวิวทั้งโรค", or runs /comprehensive-review. Runs intent-lock FIRST to lock scope,
  audience, and emphasis — explicit opt-out only. Searches PubMed and ClinicalTrials.gov
  itself; the deliverable is an md file filed to the vault via vault-keeper under the
  disorder's MOC — chat gets a short summary, not the whole chapter. NOT for: answering a
  single clinical decision or "should I use X for Y" (pubmed-research-note); watchlist
  surveillance (psych-paper-digest); writing into vault/ directly (vault-keeper owns paths).
---

# Whole-Disorder Review — the chapter, not the verdict

You are writing the chapter a good textbook would carry if it were rewritten from this
year's primary literature. The deliverable is an **md file that lives in the vault** — a
reference the user returns to for months — not a chat answer and not a decision instrument.

This skill is the deliberate inverse of `pubmed-research-note`. There, the spine is the
decision and topic-domain headings are forbidden. Here, **the disorder is the spine** and
those same headings — epidemiology, pathophysiology, diagnosis — are exactly the skeleton.
Neither skill may do the other's job.

## Prime directive — breadth is the contract

The failure mode this skill exists to prevent is **silent narrowing**: a "comprehensive
review" that quietly becomes a treatment essay because treatment is where the trials are.
Every section of the arc is owed coverage. A section the literature has left thin is
written thin *and says so* — one honest paragraph naming what exists — but it is never
silently dropped. Depth may vary by locked emphasis; presence may not.

## Step 0 — Run intent-lock first (before any tool call)

**Every review request routes through `intent-lock` FIRST — always, before any search.**
The frame itself is already fixed by choosing this skill — comprehensive, whole-disorder,
academic — so the interview is not about frame. It locks what still varies: **audience and
register** (self-study, teaching, publication-grade), **emphasis** (which sections carry
the depth), **length**, and **explicit exclusions**. Boundaries with sibling skills are
settled there too: a request that turns out to be one decision in disguise routes to
`pubmed-research-note` before a single search is spent.

**The only bypass is an explicit opt-out** — "just write it" / "don't interview me" /
"ไม่ต้องถาม" — in the user's own words, never inferred. On opt-out, default to: clinician
self-study register, balanced emphasis, and the full arc.

`intent-lock` self-regulates: an already-precise request gets no interview. Every
`[ASSUMED]` item it leaves lands in the review's preface block.

## Step 1 — Map the arc

Read [references/review-arc.md](references/review-arc.md) before outlining. The canonical
sections, in order:

1. Definition & nosology
2. Epidemiology
3. Etiology & pathophysiology
4. Clinical features & course
5. Diagnosis & assessment
6. Differential diagnosis & comorbidity
7. Treatment — pharmacological, psychotherapeutic, neuromodulation/somatic, psychosocial
8. Special populations
9. Prognosis
10. Controversies & future directions

Adjacent thin sections may merge (say so in the section header's first line); none may
vanish. Locked exclusions from Step 0 are listed in the preface, never just omitted.

## Step 2 — Search per section

The plugin bundles both engines with stable prefixes — no ToolSearch hunt:
`mcp__plugin_comprehensive-review_pubmed__<tool>` and
`mcp__plugin_comprehensive-review_clinical-trials__<tool>`. Per-section search recipes and
source floors are in [references/review-arc.md](references/review-arc.md).

- **PubMed — every section.** Guidelines, meta-analyses, and RCTs anchor treatment;
  cohort and register studies anchor epidemiology and course; seminal older papers are
  legitimate for nosology and history. Aim for **15–30 well-chosen sources across the
  whole review** — a chapter, not a bibliography dump.
- **ClinicalTrials.gov — mandatory for the treatment section.** Completed-but-unpublished
  and ongoing registered trials belong in *Controversies & future directions*; a treatment
  section written without the registry check has failed.
- **Firecrawl — guideline and regulatory full texts, where a section needs them.**
  Documents outside PubMed/CT.gov — a guideline body's full text on its own site (NICE,
  APA, WFSBP), a regulator's label or safety communication, gray literature — are fetched
  via the `firecrawl` plugin (`firecrawl search` / `firecrawl scrape`; WebFetch fallback,
  never blocks the run). It widens *where* documents come from, never the evidence bar:
  PubMed stays every section's backbone, and no clinical claim is sourced from a blog.

## The citation contract

Inherited from the house rules, binding here too:

- **Prose runs clean** — no `(Author Year)`, no PMIDs mid-sentence, no `[3]`.
- **Numbers stay inline, always** — prevalence with its denominator, effect size with its
  CI, NNT/NNH, relapse rates. **No section may exist without a number in it** (Definition
  & nosology is the one permitted exception when the literature offers none).
- **`## Sources` is one line per source**: the topic it supports, then the DOI link.
  Registry entries: `NCT NNNNNNNN — topic, status, n, readout`. Web documents fetched via
  firecrawl: `<topic> — <URL> (accessed YYYY-MM-DD)`, DOI preferred when one exists. No
  authors, journals, years, or PMIDs. Anything unsourced is `[unverified]` in place,
  never quietly asserted.

## The review

```markdown
# <Disorder> — Comprehensive Review
*<YYYY-MM-DD> · PubMed N · trials N · sections N*

> Assumed: <each ASSUMED item from intent-lock>
> Skipped: <locked exclusions, named>

## Definition & nosology
…each arc section as an H2, in order…

## Treatment
### Pharmacological
### Psychotherapeutic
…

## Sources
- <topic this source carries> — [doi:10.xxxx/yyyy](https://doi.org/10.xxxx/yyyy)
- NCT NNNNNNNN — <topic>, <status>, n=NNN, readout <YYYY-MM>
```

H3 sub-headings are allowed **only inside Treatment** (by modality). Everywhere else a
section too long to follow is cut, not chunked. Each section is argued narrative in the
house style — evidence adjudicated in the flow of the prose, not listed.

## Where output goes

The deliverable is the vault artifact. Three steps, all defaults:

1. **Write** the finished review as a single md file.
2. **File** it via the **vault-keeper** skill as an **artifact** — pass title
   (`<Disorder> — Comprehensive Review`), body, target type `artifact`, and the disorder
   as suggested MOC topic. Vault-keeper owns paths, dedup, MOC wiring, and the index —
   never resolve a vault path or write into `vault/` from this skill. Skip only on an
   explicit "don't vault this".
3. **Offer the infographic — the autolink (default):** after filing, surface the
   **clinical-infographic** handoff in one line — this review can be rendered into a
   single-page, print-ready clinical reference (color-coded phase/theme columns, stat tiles,
   and a "medications to avoid" safety banner when the review carries contraindications).
   Clinical-infographic reuses *this
   session's* review directly as its source — no re-search — so the render is one step away:
   run `/infographic`, or say "make an infographic". Hand the review over on the user's
   go-ahead; **never lay out the HTML here** — visual layout is clinical-infographic's job.
   Skip only on an explicit "no infographic".

**Chat gets the Close, not the chapter.** Render the full review inline only when the
user asks to see it here. **No filesystem:** render inline instead, and say explicitly
that nothing was filed.

## Handoffs

- **intent-lock** — the mandatory Step 0 gate; never re-implement the interview here.
- **pubmed-research-note** — the adjudicator. When the review surfaces a live decision
  ("so *should* I use X?"), or the request was one decision in disguise, route there. The
  treatment section reports the evidence landscape; it never issues a patient-level verdict.
- **clinical-infographic** — the render layer, the downstream autolink. Once the review is
  filed, offer to turn it into a one-page, print-ready clinical-reference infographic; it
  reuses this session's review directly (no re-search). Hand over the filed review on the
  user's go-ahead — never lay out the HTML here.
- **vault-keeper** — every vault write, per Where output goes.
- **firecrawl** — the general-web document engine, for sources outside PubMed/CT.gov
  (guideline org full texts, regulator labels, gray literature). It fetches — clean
  markdown with URL + access date; this skill adjudicates.
- **psych-paper-digest** — not chained; surveillance is a different job.

## Close

Two lines in chat: what was reviewed, `PubMed N · trials N · sections N`, the vault path
returned by vault-keeper (or that the save was skipped), any merged or thin sections, and
any `[unverified]` gaps. The file is the deliverable — never restate the chapter inline. Close
with the one-line infographic offer — the review is ready to render (`/infographic`).

## Failure conditions

This skill has failed if:

- An arc section was silently dropped, or a locked exclusion went unnamed in the preface.
- The review narrowed to treatment-only (or any single section) without the user locking
  that scope in Step 0.
- Any search ran before intent-lock, absent an explicit opt-out in the user's own words.
- A section (other than Definition & nosology) contains no number.
- An inline citation appeared in prose, or a `## Sources` entry carries an author,
  journal, publication year, or PMID (a firecrawl web document's access date is not a
  publication year).
- The treatment section shipped without the ClinicalTrials.gov check.
- A patient-level verdict was issued instead of handing the decision to
  pubmed-research-note.
- A vault path was resolved or written by this skill instead of vault-keeper.
- The finished review was not filed to the vault, absent an explicit opt-out — or the
  whole chapter was dumped into chat in place of the Close.
- An H3 appeared outside Treatment, or an intent-lock `[ASSUMED]` item reached the review
  without appearing in the preface block.
