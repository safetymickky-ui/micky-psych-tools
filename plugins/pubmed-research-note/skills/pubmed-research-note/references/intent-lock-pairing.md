# Pairing with intent-lock

`intent-lock` is a separate installed plugin. This file is the contract between the two, not a
copy of it. Never bundle, never re-implement, never paraphrase its phases here.

## Why they compose

Both skills exist because of the same fact: **the user leaves the tab.** They ask, they close
the window, and they return to finished output. `intent-lock` protects the window before the
work; the verdict-first report protects the reading after it. Run alone, each has a blind spot
the other covers — an interview that produces an encyclopedia, or a perfectly-spined report
answering a question nobody asked.

## Trigger rule

**Chain intent-lock first on every request. The only exception is an explicit opt-out.**

| Situation | Chain intent-lock? |
|---|---|
| Any research request — the default | **Yes, always, first** |
| Bare topic, no decision ("review DLPFC", "tell me about lurasidone") | **Yes** |
| Two or more readings could apply | **Yes** |
| Service decision, formulary change, SOP, anything reused | **Yes** |
| Quick check, seemingly obvious decision ("is prazosin still first-line for PTSD nightmares?") | **Yes** — intent-lock self-skips the questions if it is truly unambiguous, so this costs nothing |
| User typed `/intent-lock` | **Yes**, unconditionally |
| User explicitly says "just search" / "don't interview me" / hands over a locked decision | **No** — honour the opt-out |

The old model chained only on hard cases and let you infer the decision on "obvious" ones.
That inference is exactly how a "comprehensive review" gets silently collapsed into a narrow
report the user did not ask for. The gate now runs first every time; **`intent-lock`'s own
admission threshold — not your judgement about whether this request "deserves" an interview —
decides whether any questions actually get asked.** Do not infer an opt-out from an ordinary
"research this for me"; the opt-out must be the user's explicit words. Once the interview
locks the decision, scope the evidence work by **reuse count × cost of a wrong reading**,
exactly as `intent-lock` says.

## What intent-lock must have fixed before search begins

At `GOAL UNIFIED`, these are closed. Search cannot begin until all four exist — they are the
*what-the-user-wants* half of the decision brief (the evidence-side slots you derive yourself;
see `references/decision-brief.md`):

1. **The decision** — the concrete thing that will be done differently, in one sentence. Never
   the topic.
2. **The verdict's shape** — what a good answer physically looks like for this decision (a
   dose, a build/don't-with-conditions, a true/false/unsettled, a spoken sentence, a
   probability). Named for this request, not chosen from a menu.
3. **The scope boundary** — what is explicitly out.
4. **The anti-goal** — the report that satisfies the literal request and still fails.

Anything the interview did not settle is an `[ASSUMED]` item and travels to the preface block.

## What must never be re-asked

Everything above. The interview *was* the permission. After `GOAL UNIFIED`:

- Do not ask whether to proceed.
- Do not ask the user to confirm the decision you were handed.
- Do not ask for a detail a stated default already covers.
- Do not surface a clarifying question inside the report.

Re-asking is not caution. It is a second interview conducted after the user has stopped
reading, and it wastes the only correction window they had.

## Where the assumptions live

`intent-lock` Phase 3 says the assumptions are the first thing the user reads. In this skill's
default runtime the deliverable is a **file**, and the chat recap is two lines — so the
`Assumed / Reframed / Skipped` block goes **inside the report**, directly under the date line
and above the verdict. It does not go only in the chat, where it will scroll away unread.

When intent-lock did not run, that block is replaced by one line naming the decision and the
reading it beat. The reader must always know which question was answered.

## Reframes and the decision

`intent-lock`'s Phase 0 reframe operates on the *request*; this skill's Step 0 builds the
*decision brief*. They can conflict. When the reframe is accepted, it governs — the brief is
rebuilt from the reframed request from scratch, because a better-shaped request often carries a
different decision than the one the user's original wording implied. Never carry a decision
brief across a reframe.

## When the report still misses

A rejected report is a `misread-capture` event, not a revision request. Capture the user's
diagnosis in their own words. Do not explain what you understood, do not defend the spine, do
not draft the entry for them. The next run reads the ledger.
