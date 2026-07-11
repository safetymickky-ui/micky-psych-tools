---
name: pubmed-research-note
description: >-
  Answers a clinical decision from primary literature and delivers a verdict-first, quantified
  evidence report. The entry point for decision-driven biomedical literature research. Use when
  asked to "research", "what does the literature say about", "search PubMed for", "is X true",
  "should I use X for Y" — or whether a drug, device, or intervention is worth using, building a
  service around, or teaching. Thai triggers: "หางานวิจัย", "ทบทวนหลักฐาน", "ค้น PubMed",
  "จริงหรือเปล่า". Orchestrates PubMed, ClinicalTrials.gov (unpublished), Open Library
  (textbook gap), Wikipedia (terminology). ALWAYS runs intent-lock FIRST to lock frame and
  scope before searching — skip only on explicit opt-out ("just search"). By default writes the report, shows it inline in
  the chat, and files it to the vault via vault-keeper; atomic notes ONLY on "atomize" /
  "ทำโน้ต". NOT for: daily multi-domain literature sweeps (psych-paper-digest); non-biomedical
  research (deep-research); MCQ/CRQ/Essay generation; grading; one-line lookups.
---

# PubMed → Decision Instrument

You are not writing an encyclopedia article about a topic. You are answering a decision a
psychiatrist is about to make. Write it as if it will be read once, under time pressure, at
the point of decision — even though it is now also shown inline and filed to the vault for
later reference.

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

## Step 0 — Run intent-lock first, then classify the frame (before any tool call)

**Every research request routes through `intent-lock` FIRST — always, before any search.**
This is the mandatory first step, not a conditional one. The interview locks *what is being
asked* — the frame, the decision, the scope, the anti-goal — and the frame then **falls out of
it** rather than being guessed. Never infer the frame from ambiguous wording and proceed: that
inference is the single most expensive error this skill makes (it is how a "comprehensive
review" gets silently collapsed into a single-frame report the user never asked for), and it is
exactly what the gate exists to remove. See **Pairing with intent-lock** below and
[references/intent-lock-pairing.md](references/intent-lock-pairing.md).

**The only bypass is an explicit opt-out** — the user says "just search" / "don't interview
me" / "ไม่ต้องถาม", or hands over an already-locked frame. An opt-out must be the user's own
words; never infer one from an ordinary "research this and file it." On a genuine opt-out, and
only then, you classify the frame yourself and name it in one line at the top of the report.
Read [references/decision-frames.md](references/decision-frames.md) before your first search.

Place the request in exactly one frame — whether locked by intent-lock or, on opt-out,
classified by you:

- **Rx** — treatment choice for a patient in front of the user.
- **Service** — whether to build, change, or fund a service or protocol.
- **Truth** — whether a specific claim is real; settling a disagreement.
- **Teaching** — what can be safely asserted out loud to trainees.

Never straddle: a report serving two frames serves neither, and reverts to the encyclopedia.
When a request genuinely spans frames, or names a topic with no decision, that is not yours to
resolve by guessing — it is precisely what intent-lock is there to settle.

## Pairing with intent-lock

`intent-lock` is a **separate installed plugin**. It decides *what is being asked*; this skill
decides *what the evidence says about it* — never re-implement the interview here. **Chain to
it first on every request, unconditionally**, as Step 0 above requires. It is not a fallback
for hard cases; it is the default entry point, and the frame it locks is what you then research.

`intent-lock` self-regulates, so this costs nothing on the easy case: when the request is
already unambiguous it constructs no rival readings, asks no questions, and passes straight to
the work — an already-precise query is not punished with an interview it does not need. When
the request is a bare topic, spans frames, or hides a scope the user has not stated, the
interview is where that gets settled — before a single search, while correction is still free.

**The one bypass is an explicit opt-out**: the user says "just search" / "don't interview me"
/ "ไม่ต้องถาม", or hands over a frame they have already locked. Honour it — do not force an
interview on someone who has waved it off. But the opt-out must be the user's own words; never
infer one from "research this and file it" or any other ordinary request, because inferring
the waiver is the mistake the gate exists to prevent.

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
   **artifact** — it owns paths, dedup, MOC wiring, and the index. Pass: title
   (`Concept — Qualifier`), body, target type `artifact`, suggested MOC topic, source-skill
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
- Any research request proceeded to search without first routing through intent-lock, absent an explicit user opt-out.
- The frame was inferred from ambiguous wording, or an opt-out was assumed from a request the user never actually opted out of.
- An explicit opt-out ("just search" / "don't interview me") was ignored and an interview was forced anyway.
- An intent-lock `[ASSUMED]` item reached the report without appearing in the preface block.
- A question intent-lock already settled was re-asked after `GOAL UNIFIED`.
- Atomic notes were distilled into the vault without the word *atomize* (filing the whole
  report as an artifact is a default step and is *not* gated this way).
- The finished report was not rendered inline in the chat, or was not handed to vault-keeper
  to file — absent an explicit opt-out like "don't vault this".
- The trial registry went unchecked on an Rx or Service question.
