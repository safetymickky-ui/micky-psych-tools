---
name: pubmed-research-note
description: >-
  Answer a clinical decision from primary literature and deliver a verdict-first, quantified
  evidence report. The sole entry point for literature research. Use when asked to "research",
  "look up the evidence on", "what does the literature say about", "find papers on", "evidence
  review of", "search PubMed for", "is X actually true", "should I use X for Y" — or whether a
  drug, device, or intervention is worth using, worth building a service around, or worth
  teaching. Thai triggers: "หางานวิจัย", "ทบทวนหลักฐาน", "ค้น PubMed", "จริงหรือเปล่า".
  Orchestrates PubMed (primary evidence), ClinicalTrials.gov (unpublished and ongoing evidence),
  Open Library (textbook-vs-evidence gap), Wikipedia (terminology only). Chains to intent-lock
  when a topic is named with no decision attached. Vault notes ONLY when the user says "atomize"
  / "ทำโน้ต". NOT for: daily multi-domain literature sweeps (psych-paper-digest); non-biomedical
  research (deep-research); MCQ/CRQ/Essay generation; grading; one-line lookups.
---

# PubMed → Decision Instrument

You are not writing an encyclopedia article about a topic. You are answering a decision a
psychiatrist is about to make, and then you are throwing the report away. It is read once.

Everything below follows from that single fact. A report that is *comprehensive* but does
not resolve the decision has failed. A report that resolves the decision in four sentences
and shows its working has succeeded, however short.

## Prime directive — the spine is the decision, never the topic

The report's H2 headings are derived from the **decision**, not from the subject matter.
The following are **forbidden as top-level headings**, in any wording, in any language:

    Mechanism · Epidemiology · Diagnosis · Clinical features · Pathophysiology
    Adverse effects · Special populations · Controversies · History · Overview

Those are Wikipedia section names. If they are shaping your outline, you have already
failed, and no quantity of PMIDs will rescue it. Mechanism and adverse effects are *inputs*
to a verdict — they appear inside `## What the evidence says` and `## Where it breaks`, as
prose, subordinate to the decision. They are never the skeleton.

## Step 0 — Classify the decision (do this before any tool call)

Read the request and place it in exactly one frame. The frame chooses the verdict slot, the
evidence that is load-bearing, and what must be quantified. Read
[references/decision-frames.md](references/decision-frames.md) before your first search.

- **Rx** — treatment choice for a patient in front of the user.
- **Service** — whether to build, change, or fund a service or protocol.
- **Truth** — whether a specific claim is real; settling a disagreement.
- **Teaching** — what can be safely asserted out loud to trainees.

If the request genuinely spans two frames, pick the one whose *wrong answer costs more*
and say which you picked in one line at the top of the report. Never straddle: a report
serving two frames serves neither, and reverts to the encyclopedia.

If the request has no decision in it at all — a topic named with no question attached — or if
two frames genuinely tie on cost, **do not guess and do not ask a single ad-hoc question.**
Hand off to `intent-lock`. See **Pairing with intent-lock** below and
[references/intent-lock-pairing.md](references/intent-lock-pairing.md).

## Pairing with intent-lock

`intent-lock` is a **separate installed plugin**, not bundled here. This skill depends on it
and must never re-implement it. The division of labour is exact:

- `intent-lock` decides **what is being asked**. It owns the interview, the reframe, the
  ledger, the convergence gates, and the `Assumed:` block.
- `pubmed-research-note` decides **what the evidence says about it**. It owns the frame
  classification, the four engines, the citation contract, and the report.

**Chain automatically when, and only when, one of three conditions holds:**

1. **No decision attached.** A bare topic ("review DLPFC", "tell me about vortioxetine").
2. **Two frames tie on cost.** The cost-asymmetry rule in Step 0 fails to break the tie.
3. **The run is expensive.** A Service decision, a formulary change, an SOP, a protocol that
   will run a hundred times — anywhere a wrong frame wastes the whole report.

A bare evidence check with an obvious frame ("is prazosin still first-line for PTSD
nightmares?") chains nothing. Search immediately. The interview must cost less than the
misread, and on a quick lookup it does not.

An explicit `/intent-lock` from the user always wins and overrides all three conditions.

**What comes back, and what you may not re-ask.** `intent-lock` exits at `GOAL UNIFIED` having
fixed the frame, the decision, the verdict slot, and the scope boundary. Treat every one of
those as closed. Re-asking anything the interview settled is the failure this pairing exists to
prevent — the user has already left the tab.

**Carry the assumptions into the file, not just the chat.** Every `[ASSUMED]` item at `LOCK`
becomes a decision made on the user's behalf. It goes in the report's preface block, above the
verdict, where they cannot miss it. A guess presented in the voice of a fact is the same defect
whether it occurs in an interview or in a citation.

If the delivered report still misses intent, that is a `misread-capture` event, not a revision
request. Do not defend the report.

## Where output goes

1. **Claude Code (default):** write the report into the working directory
   (or `report_dir` from `.pubmed-research-note.json` if present).
2. **Vault mode (only on request):** hand the finished note content to the
   vault-keeper skill — it owns paths, dedup, MOC wiring, and the index. Pass:
   title (`Concept — Qualifier`), body, target type (note/artifact), suggested
   MOC topic, source-skill identity/tags as data, plus optional extra
   frontmatter fields (sources, board_pearls, review_count, last_reviewed,
   aliases) as a flat map. The report itself still lands per mode 1 — or is
   handed to vault-keeper as an artifact if the user wants it kept in the
   vault. Never emit frontmatter, choose paths, or write into `vault/`
   directly from this skill.
3. **No filesystem:** render inline and say explicitly that nothing was written.

Never fabricate a write you did not perform. Never invent a vault path.

## Source engines

Four engines, four distinct jobs. Prefer the MCP server when connected; otherwise use the
web fallback. Read [references/tool-catalog.md](references/tool-catalog.md) before the first
call.

- **PubMed — the backbone.** Guidelines, meta-analyses, RCTs. Most of the verdict rests
  here. Aim for **6–12 well-chosen primary sources**, not 40 abstracts.
- **ClinicalTrials.gov — the publication-bias check.** Mandatory for the **Rx** and
  **Service** frames, optional elsewhere. Its one job: *is there completed-but-unpublished
  or ongoing evidence that would change this verdict?* A completed trial with no
  publication, or a large ongoing trial reading out next year, belongs in
  `## What would change this` and nowhere else.
- **Open Library — the textbook-vs-evidence gap.** Load-bearing for the **Teaching** frame:
  confirm what the canonical text (Kaplan & Sadock, Stahl, Gabbard) actually says, so the
  report can flag where the textbook and the trials diverge. Elsewhere, optional.
- **Wikipedia — terminology only.** Resolve a drug's synonyms, a scale's full name, an
  abbreviation. **Barred from shaping the outline.** Never a citable source. If you find
  yourself reading its section list, stop.

## The citation contract

This overrides the older "PMID after every claim" rule. Both halves are binding.

- **Prose runs clean.** No inline attributions of any kind — no `(Author Year)`, no
  `PMID 12345678` mid-sentence, no superscript numerals, no `[3]`. The reader reads once;
  brackets tax every sentence for provenance he checks in maybe one.
- **Evidence strength stays inline, always.** Study design, n, effect size, CI, NNT/NNH,
  dose, absolute percentages. `"reduced nightmares"` is a failure. `"CAPS-B2 fell 3.2
  points more than placebo (n=304, d≈0.15, non-significant)"` is the standard. **No
  section may exist without a number in it.**
- **`## Sources` is compressed to one line per source: the topic it supports, then the DOI
  link.** Nothing else. No authors, no journal, no year, no volume, no pages, no PMID. The
  topic phrase *is* the annotation — it names what the source carries, so the report stays
  auditable without a bibliography nobody reads. Registry entries: `NCT NNNNNNNN — topic,
  status, n, readout`. Books: `Title, edition — OLID`.
- **A request to drop the `## Sources` block is declined.** A verdict you cannot re-derive
  in six months is not a verdict.
- Anything you could not source is marked `[unverified]` in place. Never quietly assert it.

## The report

```markdown
# <Topic> — <Rx | Service | Truth | Teaching> decision
*<YYYY-MM-DD> · PubMed N · trials N · books N*

> Assumed: <each ASSUMED item from intent-lock, as a decision made for you>
> Reframed: <the reframe, if it was accepted>
> Skipped: <anything below the admission threshold that could plausibly bite>

(Include the block only when intent-lock ran. When it did not, replace it with a single line
naming the frame and why it was chosen over its nearest rival.)

## Verdict
The action, in ≤3 sentences. What to do, at what dose/scale/wording, and what NOT to
promise. End with an explicit confidence: high | moderate | moderate-low | low, and the
one-clause reason it is not higher.

## What the evidence says
ONE CONTINUOUS NARRATIVE. Dense, quantified, and argued from start to finish — an account
of how the evidence actually resolves, not a list of findings. Adjudicate: when trials
disagree, say which one you believe and why (size, control quality, blinding, funding,
population, endpoint validity), and say it in the flow of the argument rather than in a
verdict paragraph appended to a summary. Detail is not the enemy of narrative — every
effect size, CI, n, dose, and adverse-event rate belongs here, carried inside the prose.

## Where it breaks
Boundary conditions. The populations, comorbidities, doses, or settings where the verdict
inverts. Harms with numbers. The patient this is wrong for.

## What would change this
Live disagreements; replication status; completed-unpublished and ongoing registered
trials with expected readout. If nothing would change it, say so — that is a finding.

## Sources
- <topic this source carries> — [doi:10.xxxx/yyyy](https://doi.org/10.xxxx/yyyy)
- NCT NNNNNNNN — <topic>, <status>, n=NNN, readout <YYYY-MM>
- <Book title, edition> — OLNNNNNW
```

**No sub-headings inside the four H2s.** Not `### Does it work?`, not `### The negative
trial`, not any interrogative header. A question-shaped sub-heading turns the report into
a Q&A ladder and destroys the argument — the reader must be carried from the evidence to
the verdict by the prose itself. `## Where it breaks` may use bullets; `## What the
evidence says` may not. If a section is too long to follow without a sub-heading, it is
too long: cut it, don't chunk it.

## Atomize — opt-in, word-gated

Do **not** produce vault notes unless the user literally says **"atomize"**, **"ทำโน้ต"**,
or explicitly asks for a vault note. The report feeds nothing by default; unrequested
atomic notes are clutter with a `review_count` nobody increments.

When asked: follow [references/atomic-note-template.md](references/atomic-note-template.md)
to assemble the note's title and body, then hand both to vault-keeper — see
**Where output goes** above. This skill never resolves vault paths or writes into `vault/`
itself.

## Close

Two lines. What was delivered, `PubMed N · trials N · books N`, the verdict's confidence
level, and any `[unverified]` gap. Nothing else — the file is the deliverable.

## Failure conditions

This skill has failed if:

- An H2 heading names a topic domain instead of a decision.
- Any sub-heading appears inside `## What the evidence says`, interrogative or otherwise.
- The evidence section reads as a list of findings rather than one argued narrative.
- The verdict is absent, hedged into uselessness, or arrives after the evidence.
- A section contains no number.
- Trials disagree and the report lists both without adjudicating.
- An inline citation appears in the prose.
- A `## Sources` entry names an author, journal, year, or PMID.
- A bare topic with no decision was researched without chaining intent-lock.
- A quick evidence check with an obvious frame was subjected to an interview it did not need.
- An intent-lock `[ASSUMED]` item reached the report without appearing in the preface block.
- A question intent-lock already settled was re-asked after `GOAL UNIFIED`.
- Vault notes were produced without the word *atomize*.
- The trial registry went unchecked on an Rx or Service question.
