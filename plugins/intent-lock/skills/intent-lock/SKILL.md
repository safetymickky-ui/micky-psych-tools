---
name: intent-lock
description: >-
  Locks what the user wants before expensive work, then checks the finished work against that lock. Use when the user says "interview me", "ask me until you understand", "make sure you don't misunderstand", "lock the goal", "craft my prompt", "what do I actually want", "ถามจนกว่าจะเข้าใจ", "ล็อคเป้าหมาย", and unprompted when a wrong reading of an expensive, reusable or ambiguous request would waste much work. Asks picker questions on kind of output, use, and depth and breadth, in at most 3 rounds. Then works without asking permission, puts 3-5 lock lines on top of the output, checks it against the lock before delivery, and logs drift and interview errors to the Misread Ledger. Never proposes a better request and never emits a prompt for use elsewhere. Not for quick or already-precise requests, mid-task execution forks (decision-interview), critiquing or improving an existing plan (plan-critique), or a correction after delivery (misread-capture).
---

# Intent Lock

This skill prevents two failures:

1. **The questions miss the point.** The interview asks about details and never asks what
   kind of output is wanted, what it is for, or how deep and wide it goes.
2. **The work drifts.** The goal was locked correctly, and the output still does not follow it.

The user often leaves the thread while the work runs. So the interview is short, the lock is
written down, and the finished work is checked against the lock before delivery.

## What the user sees

Only these three things:

1. Picker questions, in at most 3 rounds.
2. The lock lines, on top of the output (3 to 5 lines).
3. The work.

Do everything else silently. Do not narrate the steps, announce the skill, show a draft
reading, or print a checklist.

## Step 1. Load the checks

Read the active checks from the Misread Ledger before reading the request a second time.
`references/ledger.md` says where the ledger is and how to read it. This is one query.

Each check is a sentence of the form "When <trigger>, <thing to verify or ask>". For each
check whose trigger matches this request, do what it says: it either fills a slot in Step 2
or forces a question in Step 3. Remember which checks matched; Step 7 records them.

If the ledger cannot be reached, use `references/checks-snapshot.md` and continue.

## Step 2. Draft the lock

Fill these slots from the request, the conversation, attached files and memory. Do not ask
for anything these sources already answer.

- **Goal**: the user's instruction in the user's own vocabulary, one sentence.
- **Kind**: what type of output this is. Examples: a whole-topic review, a treatment
  verdict, a speculative model, a tool, the work itself or a prompt for later.
- **Use**: what the user will do with the output.
- **Depth and breadth**: how deep, how wide, and at what level.
- **Out**: what is excluded, if the user said so.
- **Form**: file type, layout, length, where it lives.
- **Caller slots**: any points the calling plugin says it needs locked.

Then find the open slots. Imagine two finished outputs that both satisfy the request as
written and that differ from each other. Each slot where they differ is **open**. If you
cannot build two different outputs, nothing is open: skip Step 3.

Take Form from the user's standing preferences and the calling plugin's defaults. Ask about
Form only when two forms would need materially different work.

## Step 3. Ask

**Round 1 covers the open slots in this order: Kind, Use, Depth and breadth.** A caller slot
or a ledger check may take a place only after these three are settled or already answered.

Rules for every question:

- Ask only when the possible answers lead to materially different work: a different
  structure, different sources, a different deliverable, or more than about a fifth of the
  effort. Give everything else a default and carry it to the lock as an assumption.
- Use the picker tool. Ask at most 3 questions in a round, in one call.
- Write each option as a concrete output: say what would be delivered, not an abstract
  label. "A full review of the disorder, all domains" is an option. "Comprehensive" is not.
- Offer 2 to 4 options. Every option is a reading of what the user said. Never offer
  something larger or better than what was asked.
- Make each question stand alone. The user may see only the picker and not earlier text.
- The picker's free-text choice is the escape. Add an explicit "None of these" option only
  when the picker has no free-text choice.
- Match the user's language. Use short plain sentences.

Rounds:

- **The limit is 3 rounds.** Use round 2 or 3 only for a slot that is still open, a new fork
  that an answer opened, a free-text answer that has two readings, or a contradiction
  between two things the user said. For a contradiction, name both sides and ask which one
  governs. Ask once.
- Stop early when no slot is open. Most requests need one round.
- Stop at once when the user says LOCK, "stop asking", "พอ" or anything with that meaning.
- After the last round, every slot that is still open takes its default and becomes an
  assumption.

Never do these:

- Ask permission to start, or ask the user to confirm the lock.
- Propose a better, larger or differently shaped request.
- Produce a prompt, spec or brief for the user to carry elsewhere.
- Ask a fourth round.

**When nobody can answer** (a scheduled or unattended run, or the user gave an explicit
opt-out such as "just do it", "don't interview me", "ไม่ต้องถาม"): ask nothing. Fill every
slot with its default and state the unconfirmed ones as assumptions. When the user is
present and no picker tool exists, ask the same questions as plain text under the same limits.

## Step 4. Lock

Write the lock when the questions end, and start the work in the same turn.

- For work with more than a few steps, save the full slot list to `intent-lock.md` in the
  working folder. Reread it before each major stage and before Step 6. Long work loses
  early instructions; the file does not.
- Give the lock, word for word, to every subagent that produces part of the work.
- Hand the assumptions to the calling plugin. They are its `[ASSUMED]` items. Callers that
  wait for `GOAL UNIFIED` continue here: the lock is that point.

## Step 5. Work to the lock

- Treat every answer the user gave as a requirement. An answer is never a suggestion.
- When the work raises a decision that the lock does not settle, do not reopen the
  interview. Use the `decision-interview` skill when it is installed. Otherwise choose the
  option closest to the lock and add it to the assumptions.
- Do not add sections, analyses or deliverables that the lock does not ask for.

## Step 6. Check before delivery

Compare the finished work with the lock, line by line, before the user sees it.

1. For the Goal, for each slot and for each picker answer, point to the specific part of
   the output that satisfies it. If you cannot point to a part, that is a drift.
2. Check that the structure fits the Kind. A whole-topic review covers the whole topic. A
   verdict states the verdict. A speculative model is not an evidence summary.
3. Check depth, breadth and level against the lock.
4. Check that nothing in the Out slot is present, and that nothing unrequested was added.

Fix every drift you find, then check that part again. If a drift cannot be fixed, such as a
missing source or a tool that failed, keep it for the lock lines.

Do the comparison for real. Never report a match without doing it. For long or reusable
work, when a subagent tool exists, give a fresh subagent only the lock and the output and
let it do this comparison.

## Step 7. Log

Do this before the final reply, in one write. `references/ledger.md` has the fields and rules.

- Log one `drift` entry for each drift found in Step 6, fixed or not.
- Audit the interview and log one `process` entry for each of these:
  - A question was asked whose answer did not change the work.
  - Kind, Use or Depth and breadth reached the lock as an assumption while a question was
    spent on something else.
  - An option proposed something the user never said.
  - An answer was given and the work did not use it.
- Add or sharpen a check for each entry, following the ledger rules.
- Update `fires`, `last_fired` and `fire_dates` on each check that matched in Step 1.

If there is nothing to log and no check matched, write nothing.

## The lock lines

Put 3 to 5 lines on top of the output, in the user's language:

1. The locked goal in one or two sentences, in the user's own words, including the kind,
   the use, and the depth and breadth.
2. The assumptions, with "say if wrong". Leave this line out when there are none.
3. The check result: the work matches the lock, or which drifts were fixed before
   delivery, or which drift is not fixed and why.

Write them as plain sentences. Do not start a line with a label such as "Goal:",
"Assumed:" or "Check:"; the user's standing preferences forbid lead-in labels. Example:

> You asked for a whole-disorder review of intermittent explosive disorder for your own
> study, at specialist depth, across all ten domains.
> I assumed English with Thai terms kept and about 3,000 words. Say if wrong.
> I compared the review with this before delivery and fixed one drift: the treatment
> section had grown to half the text, so I cut it to fit the other domains.

When the output is a file or an artifact, put the lock lines in the chat reply that
delivers it.

## After delivery

When the user's reply shows that the work missed what they wanted, use the
`misread-capture` skill. Do not defend the work.

## This skill has failed if

- Round 1 did not settle Kind, Use, and Depth and breadth, and none of them was already answered.
- A question was asked that could not change the work.
- A fourth round was asked, or a question came after the user said stop.
- Work started without a written lock, or the output was delivered without lock lines.
- The check line reported a match and the comparison was not done.
- A drift or an interview error was found and not logged.
- A better version of the request was proposed, or a prompt was emitted for use elsewhere.
- The user was asked for permission to start.
