# Pairing with intent-lock

`intent-lock` is a separate installed plugin. This file is the contract between the two, not a
copy of it. Never bundle, never re-implement, never paraphrase its phases here.

## Why they compose

Both skills exist because of the same fact: **the user leaves the tab.** They ask, they close
the window, and they return to finished output. `intent-lock` protects the window before the
work; the verdict-first report protects the reading after it. Run alone, each has a blind spot
the other covers — an interview that produces an encyclopedia, or a perfectly-spined report
answering a question nobody asked.

## Trigger table

| Situation | Chain intent-lock? |
|---|---|
| Bare topic, no decision ("review DLPFC", "tell me about lurasidone") | **Yes** |
| Two frames tie on cost after the Step 0 asymmetry rule | **Yes** |
| Service decision, formulary change, SOP, anything reused | **Yes** |
| Quick check, obvious frame ("is prazosin still first-line for PTSD nightmares?") | No — search |
| User typed `/intent-lock` | **Yes**, unconditionally |
| User explicitly says "just search" / "don't interview me" | No |

Scope the interview by **reuse count × cost of a wrong frame**, exactly as `intent-lock` says.
A one-off Truth check earns one round. A protocol for a service earns the cap.

## What intent-lock must have fixed before search begins

At `GOAL UNIFIED`, these are closed. Search cannot begin until all five exist:

1. **The frame** — Rx, Service, Truth, or Teaching. Exactly one.
2. **The decision** — the concrete thing that will be done differently.
3. **The verdict slot** — what shape the answer takes (a dose, a build/don't, a true/false, a
   spoken sentence).
4. **The scope boundary** — what is explicitly out.
5. **The anti-goal** — the report that satisfies the literal request and still fails.

Anything the interview did not settle is an `[ASSUMED]` item and travels to the preface block.

## What must never be re-asked

Everything above. The interview *was* the permission. After `GOAL UNIFIED`:

- Do not ask whether to proceed.
- Do not ask the user to confirm the frame you were handed.
- Do not ask for a detail a stated default already covers.
- Do not surface a clarifying question inside the report.

Re-asking is not caution. It is a second interview conducted after the user has stopped
reading, and it wastes the only correction window they had.

## Where the assumptions live

`intent-lock` Phase 3 says the assumptions are the first thing the user reads. In this skill's
default runtime the deliverable is a **file**, and the chat recap is two lines — so the
`Assumed / Reframed / Skipped` block goes **inside the report**, directly under the date line
and above `## Verdict`. It does not go only in the chat, where it will scroll away unread.

When intent-lock did not run, that block is replaced by one line naming the frame and the rival
it beat. The reader must always know which question was answered.

## Frames and reframes

`intent-lock`'s Phase 0 reframe operates on the *request*; this skill's Step 0 operates on the
*frame*. They can conflict. When the reframe is accepted, it governs — the reframed request is
re-classified into a frame from scratch, because a better-shaped request often lands in a
different frame than the one the user's original wording implied. Never carry a frame across a
reframe.

## When the report still misses

A rejected report is a `misread-capture` event, not a revision request. Capture the user's
diagnosis in their own words. Do not explain what you understood, do not defend the spine, do
not draft the entry for them. The next run reads the ledger.
