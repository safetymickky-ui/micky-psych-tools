---
name: comprehensive-review
description: >-
  Writes a comprehensive, textbook-chapter academic review of a whole psychiatric disorder
  or topic from primary literature — covering definition, epidemiology, pathophysiology,
  clinical features, diagnosis, comorbidity, treatment across ALL modalities, course and
  prognosis, with the chapter's structure designed to fit the topic, never silently
  narrowed to a treatment essay. Use when the user says "comprehensive review of X", "full
  review of X", "whole-disorder review", "academic review", "review the whole topic",
  "รีวิวทั้งโรค", or runs /comprehensive-review. Runs intent-lock FIRST to lock scope and
  emphasis — explicit opt-out only. Searches PubMed and ClinicalTrials.gov
  itself; deliverable: an md file filed to the vault via vault-keeper under the disorder's
  MOC — chat gets a short summary, not the whole chapter. NOT for: answering a single
  clinical decision or "should I use X for Y" (pubmed-research-note); watchlist
  surveillance (psych-paper-digest); writing into vault/ directly (vault-keeper owns paths).
---

# Whole-Disorder Review — the chapter, not the verdict

You are writing the chapter a good textbook would carry if it were rewritten from this
year's primary literature. The deliverable is an **md file that lives in the vault** — a
reference the user returns to for months — not a chat answer and not a decision instrument.

The boundary with `pubmed-research-note` is **scope, not shape**: that skill answers one
focused question or decision; this one covers a whole disorder or topic. Both now design
their own structure — what separates them is what they owe the reader. This skill owes
*coverage*: the whole territory of the disorder, at real depth.

## Prime directive — coverage is the contract, structure is yours

The failure mode this skill exists to prevent is **silent narrowing**: a "comprehensive
review" that quietly becomes a treatment essay because treatment is where the trials are.
The contract is that every domain of the disorder gets covered — a domain the literature
has left thin is written thin *and says so*, one honest paragraph naming what exists, but
it is never silently dropped. Depth may vary by locked emphasis; coverage may not.

**How that coverage is organized is yours to design.** The canonical arc in
[references/review-arc.md](references/review-arc.md) is a coverage map and a proven default
order — not a mandatory skeleton. Sections may be reordered, split, merged, renamed, or
nested to fit the disorder in front of you; sub-headings (H3, H4) are legal anywhere they
help the reader. A device, a drug class, or a treatment modality reshapes the map to its
own anatomy. What survives every reshaping: each coverage domain is either present
somewhere in the chapter or consciously excluded and named in the preface.

## The depth contract

The chapter is a reference, and a reference the reader has to re-research has failed:

- **Load-bearing studies get the full treatment.** The pivotal trials, the definitive
  cohorts, the meta-analyses a section's claims rest on — each reported with design,
  population, n, comparator, endpoint, and effect size with CI, as a developed paragraph.
  Supporting literature may be grouped and summarized; the studies carrying a section may
  not be compressed to clauses.
- **Mechanism and background are woven in.** Pathophysiology, pharmacology, why a finding
  makes biological sense — wherever they help the reader understand rather than merely
  memorize.
- **Sources are capped by relevance, never by count.** Gather as many well-chosen sources
  as the chapter needs. Never drop a load-bearing study to keep the bibliography tidy, and
  never pad with abstracts that add nothing — the filter is *does this source change or
  deepen a section*, not a number.

## Step 0 — Run intent-lock first (before any tool call)

**Every review request routes through `intent-lock` FIRST — always, before any search.**
The frame itself is already fixed by choosing this skill — comprehensive, whole-disorder,
academic — so the interview is not about frame. It locks what still varies: **audience and
register** (self-study, teaching, publication-grade), **emphasis** (which domains carry
the depth), **length**, and **explicit exclusions**. Boundaries with sibling skills are
settled there too: a request that turns out to be one decision in disguise routes to
`pubmed-research-note` before a single search is spent.

**The only bypass is an explicit opt-out** — "just write it" / "don't interview me" /
"ไม่ต้องถาม" — in the user's own words, never inferred. On opt-out, default to: clinician
self-study register, balanced emphasis, and full coverage.

`intent-lock` self-regulates: an already-precise request gets no interview. Every
`[ASSUMED]` item it leaves lands in the review's preface block.

## Step 1 — Map the coverage, then design the outline

Read [references/review-arc.md](references/review-arc.md) before outlining. The ten
coverage domains:

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

Then **design the chapter's outline for this topic**: the canonical order is a good
default, but the structure that best carries this disorder wins — split a domain across
two sections, fold two thin domains into one (say so in the section's first line), nest
freely, reorder where the argument reads better. Locked exclusions from Step 0 are listed
in the preface, never just omitted. The one structural rule kept from the old contract:
**treatment never absorbs the review** — however the outline is shaped, the non-treatment
domains keep their standing.

## Step 2 — Search per domain

The plugin bundles both engines with stable prefixes — no ToolSearch hunt:
`mcp__plugin_comprehensive-review_pubmed__<tool>` and
`mcp__plugin_comprehensive-review_clinical-trials__<tool>`. Per-domain search recipes and
source floors are in [references/review-arc.md](references/review-arc.md).

- **PubMed — every domain.** Guidelines, meta-analyses, and RCTs anchor treatment;
  cohort and register studies anchor epidemiology and course; seminal older papers are
  legitimate for nosology and history. Gather **as many well-chosen sources as the chapter
  needs** — capped by relevance, never by count; a load-bearing study is never dropped for
  bibliography tidiness.
- **ClinicalTrials.gov — mandatory for treatment coverage.** Completed-but-unpublished
  and ongoing registered trials belong with *Controversies & future directions* (or
  wherever the designed outline puts the forward look); treatment coverage written without
  the registry check has failed.
- **Firecrawl — guideline and regulatory full texts, where a section needs them.**
  Documents outside PubMed/CT.gov — a guideline body's full text on its own site (NICE,
  APA, WFSBP), a regulator's label or safety communication, gray literature — are fetched
  via the `firecrawl` plugin (`firecrawl search` / `firecrawl scrape`; WebFetch fallback,
  never blocks the run). It widens *where* documents come from, never the evidence bar:
  PubMed stays every domain's backbone, and no clinical claim is sourced from a blog.

## The citation contract

Inherited from the house rules, binding here too:

- **Prose runs clean** — no `(Author Year)`, no PMIDs mid-sentence, no `[3]`.
- **Numbers stay inline, always** — prevalence with its denominator, effect size with its
  CI, NNT/NNH, relapse rates. **No section may exist without a number in it** (Definition
  & nosology is the one permitted exception when the literature offers none). Load-bearing
  studies additionally get the full per-study treatment of the depth contract.
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

## <First section of the outline you designed>
…the chapter follows the outline designed in Step 1 — the coverage domains all present
(or consciously excluded in the preface), in the structure that fits this topic…

## Sources
- <topic this source carries> — [doi:10.xxxx/yyyy](https://doi.org/10.xxxx/yyyy)
- NCT NNNNNNNN — <topic>, <status>, n=NNN, readout <YYYY-MM>
```

Sub-headings (H3, H4) are legal anywhere they genuinely help navigation — a long section
is **subdivided, not amputated**: never cut real content to keep a section short. Each
section is argued narrative in the house style — evidence adjudicated in the flow of the
prose, not listed.

## Where output goes

The deliverable is the vault artifact. Two steps, both defaults:

1. **Write** the finished review as a single md file.
2. **File** it via the **vault-keeper** skill as an **artifact** — pass title
   (`<Disorder> — Comprehensive Review`), body, target type `artifact`, and the disorder
   as suggested MOC topic. Vault-keeper owns paths, dedup, MOC wiring, and the index —
   never resolve a vault path or write into `vault/` from this skill. Skip only on an
   explicit "don't vault this".

**Chat gets the Close, not the chapter.** Render the full review inline only when the
user asks to see it here. **No filesystem:** render inline instead, and say explicitly
that nothing was filed.

## Handoffs

- **intent-lock** — the mandatory Step 0 gate; never re-implement the interview here.
- **pubmed-research-note** — the adjudicator. When the review surfaces a live decision
  ("so *should* I use X?"), or the request was one decision in disguise, route there. The
  treatment coverage reports the evidence landscape; it never issues a patient-level
  verdict.
- **vault-keeper** — every vault write, per Where output goes.
- **firecrawl** — the general-web document engine, for sources outside PubMed/CT.gov
  (guideline org full texts, regulator labels, gray literature). It fetches — clean
  markdown with URL + access date; this skill adjudicates.
- **psych-paper-digest** — not chained; surveillance is a different job.

## Close

Two lines in chat: what was reviewed, `PubMed N · trials N · sections N`, the vault path
returned by vault-keeper (or that the save was skipped), any merged or thin domains, and
any `[unverified]` gaps. The file is the deliverable — never restate the chapter inline.

## Failure conditions

This skill has failed if:

- A coverage domain was silently dropped, or a locked exclusion went unnamed in the
  preface.
- The review narrowed to treatment-only (or any single domain) without the user locking
  that scope in Step 0 — or treatment absorbed the review's structure.
- A load-bearing study was compressed to a clause — a name and a conclusion with no
  design, population, n, or effect size — or real content was cut to keep a section short.
- A load-bearing source was dropped, or depth cut, to satisfy a source count.
- Any search ran before intent-lock, absent an explicit opt-out in the user's own words.
- A section (other than Definition & nosology) contains no number.
- An inline citation appeared in prose, or a `## Sources` entry carries an author,
  journal, publication year, or PMID (a firecrawl web document's access date is not a
  publication year).
- Treatment coverage shipped without the ClinicalTrials.gov check.
- A patient-level verdict was issued instead of handing the decision to
  pubmed-research-note.
- A vault path was resolved or written by this skill instead of vault-keeper.
- The finished review was not filed to the vault, absent an explicit opt-out — or the
  whole chapter was dumped into chat in place of the Close.
- An intent-lock `[ASSUMED]` item reached the review without appearing in the preface
  block.
