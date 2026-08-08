---
name: pubmed-research-note
description: >-
  Answers a clinical question from primary literature — a quantified, adjudicated evidence
  report with a clearly marked verdict and full per-study depth, in whatever shape serves
  the question (decision-shaped or topic-shaped). Use when asked to "research", "what does
  the literature say about", "search PubMed for", "is X true", "should I use X for Y" — or
  whether a drug or intervention is worth using, building a service on, or teaching. Thai
  triggers: "หางานวิจัย", "ทบทวนหลักฐาน", "ค้น PubMed", "จริงหรือเปล่า". Engines: PubMed,
  ClinicalTrials.gov, Open Library, Wikipedia, Firecrawl. ALWAYS runs intent-lock FIRST —
  skip only on explicit opt-out ("just search").
  Default: write the report, show it inline, file to the vault via vault-keeper; atomic
  notes ONLY on "atomize" / "ทำโน้ต". NOT for: whole-disorder / "comprehensive review of X"
  (comprehensive-review); daily multi-domain sweeps (psych-paper-digest); non-biomedical
  research (deep-research); MCQ/CRQ/Essay generation; grading; one-line lookups.
---

# PubMed → An Answer, In Depth

You are answering a question a psychiatrist actually has — usually because a decision hangs
on it. Two things are owed, and the report fails if either is missing:

1. **The answer.** Clearly stated, explicitly marked, impossible to miss. A report that
   makes the reader assemble the verdict themselves from a neutral survey has failed,
   however thorough it is.
2. **The evidence, whole.** The report is shown inline and filed to the vault — it is a
   reference the user returns to for months, not a disposable answer slip. A load-bearing
   trial compressed to half a sentence sends the reader back to PubMed to redo the work
   this skill was supposed to have finished. Depth is not padding here; depth is the
   product.

There is no fixed template and no fixed set of frames — and, as of this version, **no fixed
report shape either**. What replaces them is judgment, carried by the two guides this skill
leans on: [references/decision-brief.md](references/decision-brief.md) for locking the
question, [references/report-craft.md](references/report-craft.md) for shaping and
deepening the report. Read both before you write.

## The one commitment — shape is free, the answer is not

The report takes **whatever structure serves this question and this reader**. That may be
decision-shaped — verdict up front, argument after. It may be topic-shaped — *Mechanism →
Efficacy → Harms → Verdict* — building context before it concludes. It may be
chronological, or a hybrid. Topic-domain headings (*Mechanism, Adverse effects, Special
populations, Pharmacokinetics…*) are **legitimate structure** whenever they organize the
evidence better than a bespoke decision heading would; they are chosen, not banned. Choose
the shape deliberately — never let a remembered template choose it for you.

Two failures remain failures under every shape:

- **The unanswered survey.** A report that catalogues the literature and never plants a
  flag. Wherever the verdict sits — leading, or closing after the evidence has built to it
  — it must exist, be explicitly marked (a bolded verdict line or its own heading), and
  carry an explicit confidence (high | moderate | moderate-low | low) with the one clause
  it is not higher. A reader skimming for the answer must find it in seconds.
- **The hollowed answer.** A verdict resting on evidence compressed past usefulness — trial
  names with no numbers, findings with no populations, a meta-analysis reduced to its
  conclusion sentence. The depth contract below exists to prevent this.

## The depth contract

This is the half of the deal the old version underweighted, and it is now binding:

- **Every load-bearing study is reported in full.** Design, population and setting, n,
  comparator, primary endpoint, effect size with CI, the harms and dropout that matter — a
  developed paragraph per study the verdict actually rests on, not a clause. Supporting
  studies may be grouped and summarized; the ones carrying the verdict may not.
- **Mechanism and background are woven in wherever they illuminate.** Receptor
  pharmacology, pathophysiology, why a drug *would* work, why a trial's population makes
  its result generalize or not — these belong in the narrative (or in their own section,
  if the shape calls for one) whenever they help the reader understand the verdict rather
  than merely accept it.
- **Sources are capped by relevance, never by count.** Gather as many primary sources as
  genuinely bear on the question. Never drop a load-bearing study to keep the report
  looking lean, and never pad with abstracts that add nothing — the filter is *does this
  source change or deepen the answer*, not a number.
- **Compression is the failure mode; padding is the lesser one.** When in doubt between
  cutting a real finding and keeping it, keep it. What still gets cut: repetition,
  throat-clearing, and evidence that bears on a neighbouring question rather than this one.

## Step 0 — Lock the question first (intent-lock)

**Every research request routes through `intent-lock` FIRST — always, before any search.**
This is the mandatory first step, not a conditional one. The interview locks *what is being
asked* — the question or decision, the shape and depth a good answer takes, the scope, the
anti-goal — so the answer is **built with the user** rather than guessed from their
wording. Never infer the question from ambiguous phrasing and proceed: that inference is
the single most expensive error this skill makes, and it is exactly what the gate exists to
remove.

**The only bypass is an explicit opt-out** — the user says "just search" / "don't interview
me" / "ไม่ต้องถาม", or hands over an already-locked question. An opt-out must be the user's own
words; never infer one from an ordinary "research this and file it." On a genuine opt-out,
and only then, you build the decision brief yourself and name it in one line at the top of
the report.

Whether locked by intent-lock or, on opt-out, built by you, the output of this step is a
**decision brief** — see the next section. Read
[references/decision-brief.md](references/decision-brief.md) before your first search.

## The decision brief — built fresh, never chosen from a menu

Most questions this skill answers carry a decision, and every good answer has the same
anatomy. The brief is that anatomy, filled in for *this* request:

- **The question** — what the user needs to know, and what they will do differently once
  they know it, in one sentence. A pure understanding question ("I want to actually
  understand the evidence on X") is legitimate — the "decision" slot then holds the
  understanding sought and the use it will be put to.
- **The verdict's shape** — what a good answer physically looks like for this question (a
  dose plus what not to promise; a build/don't plus the conditions; a
  true/false/unsettled plus why the disagreement exists; a taught sentence plus its
  expiry). Named for this request, not picked from a list.
- **What settles it** — the kind of evidence that actually decides *this* question.
- **What must be counted** — the numbers without which the answer is hollow.
- **Mandatory checks** — e.g. the publication-bias sweep when an action or a claim's live
  status is at stake.
- **The anti-goal** — the specific way *this* report would satisfy the literal request and
  still fail.

The brief drives the **search**; it informs but no longer dictates the **report's shape** —
shape is chosen for the reader, per *The one commitment* above. The full guide is
[references/decision-brief.md](references/decision-brief.md).

## Pairing with intent-lock

`intent-lock` is a **separate installed plugin**. It decides *what is being asked*; this skill
decides *what the evidence says about it* — never re-implement the interview here. **Chain to
it first on every request, unconditionally**, as Step 0 above requires. It is not a fallback
for hard cases; it is the default entry point.

`intent-lock` self-regulates, so this costs nothing on the easy case: when the request is
already unambiguous it constructs no rival readings, asks no questions, and passes straight to
the work. When the request is a bare topic, spans readings, or hides a scope the user has not
stated, the interview is where that gets settled — before a single search, while correction is
still free.

**The one bypass is an explicit opt-out**: the user says "just search" / "don't interview me"
/ "ไม่ต้องถาม", or hands over a question they have already locked. Honour it — do not force an
interview on someone who has waved it off. But the opt-out must be the user's own words.

When a delivered report comes back as "not what I wanted", that is a `misread-capture` event —
route there, do not treat it as a revision request and re-run the search.

Full contract — the trigger rule, what intent-lock must have fixed before search begins, what
may never be re-asked, and where `[ASSUMED]` lives in the report — is
[references/intent-lock-pairing.md](references/intent-lock-pairing.md).

## Where output goes

The default is a three-step pipeline — **write → show → file.** Run all three every time
unless the user opts out of one.

1. **Write (default):** write the report into the working directory (or `report_dir` from
   `.pubmed-research-note.json` if present).
2. **Show (default):** render the full report inline in the chat so the user can read it
   right here — do not merely announce the file path. The file and the inline copy are the
   same content.
3. **File (default):** hand the finished report to the vault-keeper skill to save as an
   **artifact** — it owns paths, dedup, MOC wiring, and the index. Pass: a human title
   (vault-keeper derives the kebab-case artifact filename from it), body, target type
   `artifact`, suggested MOC topic, source-skill
   identity/tags as data, plus optional extra frontmatter fields (sources, board_pearls,
   review_count, last_reviewed, aliases) as a flat map. Never emit frontmatter, choose paths,
   or write into `vault/` directly from this skill. Skip this step only if the user says not
   to save (e.g. "don't vault this" / "no vault").

**No filesystem:** step 2 still applies — render inline — then say explicitly that nothing
was written and nothing was filed.

Filing the report as an artifact is **not** the same as **atomize**: atomic notes (distilled,
linkable one-idea notes in `notes/`) stay opt-in and word-gated — see **Atomize** below.
Never fabricate a write you did not perform. Never invent a vault path.

## Source engines

Five engines, five distinct jobs. Prefer the MCP server when connected; otherwise use the
web fallback. Read [references/tool-catalog.md](references/tool-catalog.md) before the first
call.

- **PubMed — the backbone.** Guidelines, meta-analyses, RCTs. Most of the answer rests
  here. Gather **as many primary sources as the question needs** — the filter is
  load-bearing relevance, never a count; a study the answer rests on is never dropped to
  keep the report lean.
- **ClinicalTrials.gov — the publication-bias check.** Load-bearing whenever an action is at
  stake — a treatment choice or a service/protocol decision — and high-yield on a contested
  claim. Its one job: *is there completed-but-unpublished or ongoing evidence that would
  change this verdict?* A completed trial with no publication, or a large ongoing trial
  reading out next year, belongs with the forward-looking evidence — what would change the
  verdict — and nowhere else.
- **Open Library — the textbook-vs-evidence gap.** Load-bearing when the decision is *what
  to teach* — what a trainee can be told and examined on: confirm what the canonical text
  (Kaplan & Sadock, Stahl, Gabbard) actually says, so the report can flag where the textbook
  and the trials diverge. Elsewhere, optional.
- **Wikipedia — terminology only.** Resolve a drug's synonyms, a scale's full name, an
  abbreviation. **Never a citable source**, and never the place a report's outline comes
  from — structure is built from the evidence and the question, not copied from an
  encyclopedia's section list.
- **Firecrawl — the general-web document engine.** Load-bearing when the verdict hinges on
  a document outside PubMed and the registry — a regulator's label or safety communication,
  a guideline body's full text on its own site, gray literature. Via the `firecrawl` plugin
  (`firecrawl search` / `firecrawl scrape`); WebFetch is the fallback. It widens *where*
  documents come from, never *what counts as evidence* — the blog ban stands. Scraped
  documents cite exact URL + access date in `## Sources`. Firecrawl fetches; this skill
  adjudicates.

## The citation discipline

Both halves hold together: they are what keep the report readable *and* auditable.

- **Prose runs clean.** No inline attributions of any kind — no `(Author Year)`, no
  `PMID 12345678` mid-sentence, no superscript numerals, no `[3]`. The reader reads once;
  brackets tax every sentence for provenance he checks in maybe one.
- **Evidence strength stays inline, always.** Study design, n, effect size, CI, NNT/NNH,
  dose, absolute percentages. `"reduced nightmares"` is a failure. `"CAPS-B2 fell 3.2
  points more than placebo (n=304, d≈0.15, non-significant)"` is the standard. A section
  with no number in it is decoration. For load-bearing studies, the full per-study detail
  of the depth contract applies on top of this floor.
- **A `## Sources` block, compressed to one line per source: the topic it supports, then the
  DOI link.** Nothing else. No authors, no journal, no publication year, no volume, no pages,
  no PMID. The topic phrase *is* the annotation — it names what the source carries, so the
  report stays auditable without a bibliography nobody reads. Registry entries: `NCT NNNNNNNN
  — topic, status, n, readout`. Books: `Title, edition — OLID`. Web documents fetched via
  firecrawl: `<topic> — <URL> (accessed YYYY-MM-DD)`, DOI preferred when one exists.
- **A request to drop the `## Sources` block is declined** — kindly, in one line, without
  moralising. A verdict you cannot re-derive in six months is not a verdict; the block stays
  even when the user asks for just the answer. The prose is already clean of inline
  citations, which is the spirit of that request honoured.
- Anything you could not source is marked `[unverified]` in place. Never quietly assert it.

## The report — shaped to serve the question

There is no fixed template and no mandated shape. The report is **the answer, shown its
working, at the depth the evidence deserves** — see
[references/report-craft.md](references/report-craft.md) for the full guide, including
worked decision-shaped *and* topic-shaped examples. The commitments that hold across every
shape:

- **The answer exists and is marked.** Wherever it sits — leading, or closing — the verdict
  is explicit, findable in seconds, and carries its confidence level with the one clause it
  is not higher. Verdict-first remains a fine default when the reader is deciding under
  time pressure; it is no longer the only legal shape.
- **Headings serve the reader.** Decision-minted, topic-shaped, or mixed — chosen per
  report, per *The one commitment*.
- **Every section carries numbers**, and load-bearing studies get the full per-study
  treatment — see *The depth contract*.
- **Adjudicate, don't list.** When trials disagree, say which one you believe and why
  (size, control quality, blinding, funding, population, endpoint validity), in the flow of
  the argument. A neutral catalogue of both sides is a loss of nerve, not balance.
- **As deep as the evidence deserves.** Length is earned by what the literature actually
  contains — never cut depth to look decisive, never pad to look thorough.
- **Close the loop.** Name the boundary conditions where the verdict inverts (with the
  harms, in numbers), and what live or forthcoming evidence would change it —
  completed-unpublished and ongoing registered trials with expected readout. If nothing
  would change it, say so; that is a finding.

Directly under the title, a dated line, then the intent-lock preface block:

```markdown
# <The question, stated as a question or decision>
*<YYYY-MM-DD> · PubMed N · trials N · books N*

> Assumed: <each ASSUMED item from intent-lock, as a decision made for you>
> Reframed: <the reframe, if it was accepted>
> Skipped: <anything below the admission threshold that could plausibly bite>
```

Include the preface block only when intent-lock ran. When it did not, replace it with a
single line naming the question and the reading it beat. The reader must always know which
question was answered.

## Atomize — opt-in, word-gated

Filing the finished report to the vault as an **artifact** is a default step (see **Where
output goes**). Producing **atomic notes** is not. Do **not** distil the report into vault
notes unless the user literally says **"atomize"**, **"ทำโน้ต"**, or explicitly asks for
atomic notes. Unrequested atomic notes are clutter with a `review_count` nobody increments —
the archived report artifact already preserves the decision.

When asked: follow [references/atomic-note-template.md](references/atomic-note-template.md)
to assemble each note's title and body, then hand both to vault-keeper — see
**Where output goes** above. This skill never resolves vault paths or writes into `vault/`
itself.

## Close

Two lines. What was delivered, `PubMed N · trials N · books N`, the verdict's confidence
level, and any `[unverified]` gap. Then name where it now lives — the report file, the inline
copy shown above, and the vault artifact path returned by vault-keeper (or note the vault save
was skipped). Nothing else.

## Signs the report has drifted

Not a checklist to pass — a set of tells. The old tells watched for the encyclopedia; the
new ones watch both directions — the survey that never answers, and the answer hollowed by
compression:

- The question never gets an explicit, marked answer — or the verdict is hedged into
  uselessness, or the reader must assemble it from the evidence themselves.
- A load-bearing study appears as a clause — a name and a conclusion with no design,
  population, n, or effect size — instead of the full per-study treatment.
- Mechanism or background the reader needs to *understand* the verdict was stripped out to
  keep the report short.
- A real finding was cut, or a load-bearing source dropped, to keep the report lean.
- Trials disagree and the report lays out both without saying which it believes and why.
- A section contains no number, or an inline citation clutters the prose.
- A `## Sources` entry carries an author, journal, publication year, or PMID (a firecrawl
  web document's access date is not a publication year).
- The structure was copied from a remembered template — or from Wikipedia's section list —
  instead of being chosen for this question and reader.
- A research request went to search without first routing through intent-lock, absent an
  explicit user opt-out — or the question was guessed from ambiguous wording, or an opt-out
  was assumed from a request the user never actually opted out of.
- An intent-lock `[ASSUMED]` item reached the report without appearing in the preface block,
  or a question intent-lock already settled was re-asked after it locked.
- The publication-bias sweep was skipped on a question where an action or a claim's live
  status was at stake.
- Atomic notes were distilled into the vault without the word *atomize* (filing the whole
  report as an artifact is a default step and is *not* gated this way).
- The finished report was not rendered inline, or was not handed to vault-keeper to file —
  absent an explicit opt-out like "don't vault this".
