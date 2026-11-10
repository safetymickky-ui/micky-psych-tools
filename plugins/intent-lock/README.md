# intent-lock

Locks what you want before expensive work, checks the finished work against that lock,
and keeps a ledger of misreads that survives between chats.

Two skills:

- **`intent-lock`**: interview, lock, work, check, log.
- **`misread-capture`**: logs a correction you make after delivery, then redoes the work.

## What a run looks like

1. It reads your active checks from the Misread Ledger.
2. It asks picker questions in at most 3 rounds. Round 1 settles what kind of output you
   want, what you will use it for, and how deep and wide it goes. It asks nothing when the
   request already answers these.
3. It writes the lock and starts work. It does not ask permission.
4. Before delivery it compares the work with the lock and fixes every drift it finds.
5. It logs drifts and interview errors to the ledger.
6. You get 3 to 5 lock lines on top of the output: the locked goal, what was assumed, and
   what the check found.

## The Misread Ledger

The ledger is a pinned artifact page with its own database:
https://claude.ai/artifact/6JeVKcDeh53yvFsNcMt73f

- **Checks** are sentences that the next run reads first: "When <trigger>, <thing to verify
  or ask>". At most 10 are active.
- **Log entries** are of three kinds: a drift caught before delivery, a correction you made
  after delivery, and an interview error found by the audit.
- Claude writes entries and checks without asking. You can edit, retire, restore and delete
  them on the page.

Version 0.4.3 kept the ledger in a plugin file. That file is a per-session copy, so new
entries were lost. Nothing is stored in plugin files now.

## Limits

- A picker that is never answered produces no work. The app gives Claude no turn until you
  answer. This is why round 1 is short and asks the questions that decide the output.
- In a scheduled run nobody can answer, so the skill asks nothing and states every
  unconfirmed default in the lock lines.
- The check before delivery is done by the same model that did the work, unless a subagent
  tool is available. It catches structural drift well and subtle drift less well.

## Plugins that call intent-lock

comprehensive-review, pubmed-research-note, concept-animation, ml-concept-lab,
vi-stock-screen-research, tutor and code-explainer call this skill as their first step.
Its siblings are `decision-interview`, which owns decisions that appear during the work,
and `plan-critique`, which owns critique of an existing plan.
The interface they rely on is unchanged: the skill name, the explicit opt-out, and the
assumptions returned as `[ASSUMED]` items.

## Install

```
/plugin marketplace add <owner>/micky-psych-tools
/plugin install intent-lock@micky-psych-tools
```
