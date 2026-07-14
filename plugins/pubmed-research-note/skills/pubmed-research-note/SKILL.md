---
name: pubmed-research-note
description: >-
  Answers a clinical decision from primary literature and delivers a verdict-first, quantified
  report shaped to the decision, not the topic. Use when asked to "research", "what does the
  literature say about", "search PubMed for", "is X true", "should I use X for Y" — or whether
  a drug, device, or intervention is worth using, building a service around, or teaching. Thai
  triggers: "หางานวิจัย", "ทบทวนหลักฐาน", "ค้น PubMed", "จริงหรือเปล่า". Orchestrates PubMed,
  ClinicalTrials.gov, Open Library, Wikipedia, Firecrawl. ALWAYS runs intent-lock FIRST to lock the
  decision and scope before searching — skip only on explicit opt-out ("just search"). By
  default writes the report, shows it inline, and files it to the vault via vault-keeper;
  atomic notes ONLY on "atomize" / "ทำโน้ต". NOT for: whole-disorder / "comprehensive review
  of X" reviews (comprehensive-review); daily multi-domain sweeps (psych-paper-digest);
  non-biomedical research (deep-research); MCQ/CRQ/Essay generation; grading; one-line lookups.
---

# PubMed → Decision Instrument

You are not writing an encyclopedia article about a topic. You are answering a decision a
psychiatrist is about to make. Write it as if it will be read once, under time pressure, at
the point of decision — even though it is now also shown inline and filed to the vault for
later reference.

Everything below follows from that single fact. A report that is *comprehensive* but does
not resolve the decision has failed. A report that resolves the decision in four sentences
and shows its working has succeeded, however short.

There is no fixed set of frames to sort the request into, and no fixed template to pour it
into. Both were removed on purpose. What replaces them is a small habit of thought — build
the decision, then let the report take the shape the decision demands — carried by the
two guides this skill leans on: [references/decision-brief.md](references/decision-brief.md)
for the decision, [references/report-craft.md](references/report-craft.md) for the report.
Read both before you write.

## The one commitment — the spine is the decision, never the topic

The report's headings are minted from the **decision**, not from the subject matter. This is
the single commitment everything else depends on, and it is worth understanding *why* rather
than obeying as a rule.

When a heading would sit comfortably in an encyclopedia article on the topic — *Mechanism,
Epidemiology, Diagnosis, Clinical features, Pathophysiology, Adverse effects, Special
populations, Controversies, History, Overview* — that heading is the **tell** that you have
stopped answering the decision and started surveying the topic. It is not a banned word to
route around; it is a symptom. The reader arrived with a decision already in hand. A
topic-shaped survey hands the synthesis back to them — it makes them do the work you were
supposed to do. That is the failure this skill exists to prevent, and no quantity of PMIDs
rescues it.

Mechanism and adverse effects are *inputs* to a verdict, not sections of a report. They
appear as prose, subordinate to the decision, wherever the argument needs them. They are
never the skeleton. If a topic outline is shaping your draft, the report has already
reverted to Wikipedia — start again from the decision.

## Step 0 — Lock the decision first (intent-lock)

**Every research request routes through `intent-lock` FIRST — always, before any search.**
This is the mandatory first step, not a conditional one. The interview locks *what is being
asked* — the decision, the shape a good answer takes, the scope, the anti-goal — so the
decision is **built with the user** rather than guessed from their wording. Never infer the
decision from ambiguous phrasing and proceed: that inference is the single most expensive
error this skill makes (it is how a "comprehensive review" gets silently collapsed into a
narrow one the user never asked for), and it is exactly what the gate exists to remove.

**The only bypass is an explicit opt-out** — the user says "just search" / "don't interview
me" / "ไม่ต้องถาม", or hands over an already-locked decision. An opt-out must be the user's own
words; never infer one from an ordinary "research this and file it." On a genuine opt-out, and
only then, you build the decision brief yourself and name it in one line at the top of the
report.

Whether locked by intent-lock or, on opt-out, built by you, the output of this step is a
**decision brief** — see the next section. Read
[references/decision-brief.md](references/decision-brief.md) before your first search.

## The decision brief — built fresh, never chosen from a menu

Every good decision has the same anatomy. The brief is that anatomy, filled in for *this*
request:

- **The decision** — what the user will do differently, in one sentence. Never the topic.
- **The verdict's shape** — what a good answer physically looks like for this decision (a
  dose plus what not to promise; a build/don't plus the conditions, in the units the service
  uses; a true/false/unsettled plus why the disagreement exists; a sentence you can say aloud
  plus its expiry; a probability plus a threshold). Named for this request, not picked from a
  list.
- **What settles it** — the kind of evidence that actually decides *this* question.
- **What must be counted** — the numbers without which the verdict is hollow.
- **Mandatory checks** — e.g. the publication-bias sweep when an action or a claim's live
  status is at stake.
- **The anti-goal** — the specific way *this* report would satisfy the literal request and
  still fail.

The first four come from the interview or, on opt-out, from you; the evidence-side slots you
derive from them. This brief is not one of four boxes — it is made to measure every time, and
it is what both the search and the report shape are built against. The full guide, with what a
good fill looks like for each slot and how to handle a request that carries two readings, is
[references/decision-brief.md](references/decision-brief.md).

## Pairing with intent-lock

`intent-lock` is a **separate installed plugin**. It decides *what is being asked*; this skill
decides *what the evidence says about it* — never re-implement the interview here. **Chain to
it first on every request, unconditionally**, as Step 0 above requires. It is not a fallback
for hard cases; it is the default entry point, and the decision it locks is what you then
research.

`intent-lock` self-regulates, so this costs nothing on the easy case: when the request is
already unambiguous it constructs no rival readings, asks no questions, and passes straight to
the work — an already-precise query is not punished with an interview it does not need. When
the request is a bare topic, spans readings, or hides a scope the user has not stated, the
interview is where that gets settled — before a single search, while correction is still free.

**The one bypass is an explicit opt-out**: the user says "just search" / "don't interview me"
/ "ไม่ต้องถาม", or hands over a decision they have already locked. Honour it — do not force an
interview on someone who has waved it off. But the opt-out must be the user's own words; never
infer one from "research this and file it" or any other ordinary request, because inferring
the waiver is the mistake the gate exists to prevent.

When a delivered report comes back as "not what I wanted", that is a `misread-capture` event —
route there, do not treat it as a revision request and re-run the search.

Full contract — the trigger rule, what intent-lock must have fixed before search begins, what
may never be re-asked, and where `[ASSUMED]` lives in the report — is
[references/intent-lock-pairing.md](references/intent-lock-pairing.md).

## Where output goes

The default pipeline is **write → show → file**, then a standing **infographic offer**.
Run each step every time unless the user opts out of it — the infographic offer additionally
stands down when a one-page render would not serve the report.

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
4. **Offer the infographic — the autolink (default):** as the last step — whether or not the
   report was vaulted — surface the handoff to the **clinical-infographic** plugin in one line:
   this report can be rendered into a single-page, print-ready clinical-reference infographic
   (color-coded columns, stat tiles, and a "medications to avoid" safety banner when the report
   carries contraindications). Clinical-infographic reuses *this session's* report directly as
   its source — no re-search, no re-adjudication — so the render is one step away: run
   `/infographic`, or say "make an infographic". Hand the report over on the user's go-ahead;
   **never render the HTML here** — visual layout is clinical-infographic's job, and issuing a
   rendered view is not this skill's. Skip the offer only on an explicit "no infographic", or
   when a one-page render would not serve the report.

**No filesystem:** step 2 still applies — render inline — then say explicitly that nothing
was written and nothing was filed.

Filing the report as an artifact is **not** the same as **atomize**: atomic notes (distilled,
linkable one-idea notes in `notes/`) stay opt-in and word-gated — see **Atomize** below.
Never fabricate a write you did not perform. Never invent a vault path.

## Source engines

Five engines, five distinct jobs. Prefer the MCP server when connected; otherwise use the
web fallback. Read [references/tool-catalog.md](references/tool-catalog.md) before the first
call.

- **PubMed — the backbone.** Guidelines, meta-analyses, RCTs. Most of the verdict rests
  here. Aim for **6–12 well-chosen primary sources**, not 40 abstracts.
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
  abbreviation. **Barred from shaping the outline.** Never a citable source. If you find
  yourself reading its section list, stop.
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
  with no number in it is decoration.
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

## The report — shaped to the decision

There is no fixed template. The report is the **verdict, shown its working**, and it takes
whatever shape carries *this* decision from evidence to action in the fewest sections that
still earn their place. The full guide — the principles, how to mint headings from the brief,
and worked example shapes — is [references/report-craft.md](references/report-craft.md).
The commitments that hold across every shape:

- **The verdict leads.** The action comes first — a reader who stops after the opening still
  got what they came for. State it in ≤3 sentences: what to do, at what dose/scale/wording,
  what NOT to promise, and an explicit confidence (high | moderate | moderate-low | low) with
  the one clause it is not higher.
- **Headings come from the decision, not the topic** — see *The one commitment* above.
- **Every section carries numbers** — see *The citation discipline*.
- **Adjudicate, don't list.** When trials disagree, say which one you believe and why (size,
  control quality, blinding, funding, population, endpoint validity), in the flow of the
  argument. A neutral catalogue of both sides is a loss of nerve, not balance.
- **As long as the decision needs, no longer.** A contested claim may resolve in three
  sections; a service decision may earn five. Length is earned by the decision's complexity,
  never by the topic's breadth.
- **Close the loop.** Name the boundary conditions where the verdict inverts (with the harms,
  in numbers), and what live or forthcoming evidence would change it — completed-unpublished
  and ongoing registered trials with expected readout. If nothing would change it, say so;
  that is a finding.

Directly under the title, a dated line, then the intent-lock preface block:

```markdown
# <Decision, stated as a decision> 
*<YYYY-MM-DD> · PubMed N · trials N · books N*

> Assumed: <each ASSUMED item from intent-lock, as a decision made for you>
> Reframed: <the reframe, if it was accepted>
> Skipped: <anything below the admission threshold that could plausibly bite>
```

Include the preface block only when intent-lock ran. When it did not, replace it with a
single line naming the decision and the reading it beat. The reader must always know which
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

Two lines, then the offer. Line one: what was delivered, `PubMed N · trials N · books N`, the
verdict's confidence level, and any `[unverified]` gap. Line two: where it now lives — the
report file, the inline copy shown above, and the vault artifact path returned by vault-keeper
(or note the vault save was skipped). Then the one-line infographic offer — the report is ready
to render as a clinical-reference infographic (`/infographic`). Nothing else.

## Signs the report has drifted

Not a checklist to pass — a set of tells that the report has slid back toward the encyclopedia
it exists to replace. If one shows up, the fix is upstream, in the decision or the shape:

- A heading names a topic domain (*Mechanism, Epidemiology, Adverse effects…*) instead of
  advancing the decision.
- The evidence reads as a list of findings rather than one argued line from evidence to
  verdict.
- Trials disagree and the report lays out both without saying which it believes and why.
- The verdict is absent, hedged into uselessness, or arrives after the evidence.
- A section contains no number, or an inline citation clutters the prose.
- A `## Sources` entry carries an author, journal, publication year, or PMID (a firecrawl
  web document's access date is not a publication year).
- The report is padded past what the decision needed, or shaped by the topic's breadth
  instead of the decision's complexity.
- A research request went to search without first routing through intent-lock, absent an
  explicit user opt-out — or the decision was guessed from ambiguous wording, or an opt-out
  was assumed from a request the user never actually opted out of.
- An intent-lock `[ASSUMED]` item reached the report without appearing in the preface block,
  or a question intent-lock already settled was re-asked after it locked.
- The publication-bias sweep was skipped on a question where an action or a claim's live
  status was at stake.
- Atomic notes were distilled into the vault without the word *atomize* (filing the whole
  report as an artifact is a default step and is *not* gated this way).
- The finished report was not rendered inline, or was not handed to vault-keeper to file —
  absent an explicit opt-out like "don't vault this".
