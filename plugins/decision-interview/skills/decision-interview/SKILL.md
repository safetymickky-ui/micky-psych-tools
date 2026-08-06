---
name: decision-interview
description: Mid-task decision gate — fires after the goal is locked, when execution surfaces decisions only the user can make (scope forks, trade-offs, destructive or irreversible steps, missing preferences), and resolves them all in one batched option-picker interview. Use when, mid-task, the user says "resolve all decisions", "ask me everything at once", "batch your questions", "what do you need from me", "collect your questions", "ถามมาทีเดียวให้ครบ", or runs /resolve-decisions — and unprompted, the moment two or more decisions accumulate or a single decision blocks the work now. Sweeps the task end to end, triages by whether the answers change the work, asks in dependency order with a recommended option first, and records resolutions in a decision ledger that governs the rest of the session. Not for pre-build alignment (intent-lock), a delivered misread (misread-capture), critiquing or improving a user's existing plan (plan-critique), or decisions the code, conversation, or repo conventions already settle.
---

# Decision Interview

The scarcest resource in a session is the user's attention. Every scattered question is an interruption that may never be answered; every silent guess is a liability that surfaces later as rework. This skill converts both into one visit: sweep every open decision, drop the ones that don't deserve the user, ask the rest in one batched interview, record the answers, and keep working under them.

**Intent-lock ends where this begins.** Intent-lock converges on what the request *means* before work starts. This skill runs after that: the reading is locked, execution is underway, and the work itself has surfaced concrete decisions inside the locked goal — which file wins, whether to overwrite, which trade-off to take. Interrogating the goal again here is a failure; resolving execution decisions is the job.

## When it fires

- The user asks: "resolve all decisions", "ask me everything at once", "batch your questions", "what do you need from me", or runs `/resolve-decisions`.
- Unprompted: the moment a second above-threshold decision accumulates mid-task, or a single decision blocks work now. One decision alone is not an interview — run the sweep anyway (it is cheap), and if it comes back with a single `[ASK]`, ask it through a one-question picker call, state any defaults the sweep produced in the same message, and record the answer as a resolution like any other. The fast path skips the multi-round machinery, never the ledger's governance.
- A blocking decision does not wait its turn. If work is stopped now, sweep first regardless — the sweep costs a minute and prevents the second interview — then put the blocker at the head of round 1. One exception: if the blocker itself depends on another surviving decision, the dependency rule wins — the upstream fork leads round 1 and the blocker follows in the next round.

## Procedure

### 1. Sweep — find every decision before asking about any

The whole value of the interview is completeness: an interview that misses a decision and comes back an hour later has failed at its one job. Before any question, walk the task end to end and enumerate from three sources:

- **Blockers** — points where work has stopped, or will stop, without an answer.
- **Silent defaults** — decisions you were about to make on the user's behalf. Each is a decision; write it down.
- **Lookahead** — decisions the remaining plan will predictably surface. Read the plan to its end; the second interview is the one you were supposed to prevent.

Keep the sweep as an internal ledger, one line per decision — it is working state, never printed:

```
[ASK]     1. Config format — JSON vs YAML: changes every file the scaffold writes.
[DEFAULT] 2. Test runner → pytest (repo already uses it; not asked)
[ASK]     3. Existing data/ dir — overwrite or merge: destructive, always asked.
```

### 2. Triage — the admission threshold

A decision earns a question only if the competing answers produce **materially different work** — different structure, different deliverable, different sources, or more than roughly a fifth of the effort. Everything below the line gets a stated default and no question. Two overrides:

- **Destructive, irreversible, or outward-facing actions always earn a question**, regardless of size: delete, overwrite, publish, send, spend, force-push — anything a later undo cannot reach. These are never defaulted.
- **Already answered is not a decision.** If the conversation, the code, the repo's conventions, or the user's stated preferences resolve it, resolve it there and name the source. Making the user repeat themselves teaches them to stop answering. For destructive items, answered means the user explicitly chose it — a stated default or an assumption inherited from an earlier gate does not qualify, and the item re-enters the interview.

Padding the interview with sub-threshold preferences is the failure mode that kills batching: the user answers four preference questions, hits fatigue, and abandons the fork that mattered.

### 3. Order — dependencies first, then leverage

- A decision whose answer creates or kills other decisions goes in the earliest round; its dependents wait. Never ask a question whose relevance hangs on an unanswered earlier one — a dead-branch question wastes a slot and shows the user you didn't think.
- Within a round, highest-leverage first.

### 4. Ask — one batched interview through the option-picker

Every question goes through the interactive option-picker, never prose. Per round:

- **One picker call per round, up to four questions per call** (the tool's ceiling). More than four surviving decisions → multiple rounds in dependency order, not a bigger round.
- **Options are concrete outcomes, not labels.** "Merge into the existing dir, keep both on conflict" — never "Option B". The user is choosing what happens and should be able to see it.
- **Recommend in every question.** Your recommended option goes first, marked "(Recommended)", with the reason in its description. The mark is a service, not a nudge: the user can clear the whole interview by tapping recommendations and disagree exactly where they disagree.
- **multiSelect where several answers can hold at once** (scope inclusions, features to keep); single-select for true forks.
- **A typed answer beats the option set.** Free text is the user's actual decision; the options were your guesses at it.

### 5. Record — the decision ledger

After the last round, print one compact ledger — the only ceremony this skill allows:

```
Decided: config = YAML · data/ = merge, keep both on conflict.
Defaults: pytest (repo convention) · module layout unchanged — say if wrong.
```

The ledger governs the rest of the session:

- **A resolved decision is never re-asked.** Not in this task, not rephrased, not "just to confirm".
- **Resolutions generalize.** A later decision the recorded rule already covers takes the rule; asking again is re-asking.
- **New above-threshold decisions batch again** — a fresh sweep, not a drip of one-offs — unless one is blocking now, in which case it leads the new round.

### 6. Resume

Return to the work in the same turn the ledger prints. The interview was the permission; asking "shall I proceed" spends the attention the whole skill exists to save.

## Autonomous fallback — when nobody can answer

An unattended session, an interrupted picker, an abandoned round: silence is a stop, not a license to wait.

- **Reversible decisions** take the recommended default and are recorded in a `Decided without you:` ledger at the top of the delivered output — each with its one-line reason, each catchable after the fact.
- **Destructive, irreversible, or outward-facing decisions are never defaulted.** Halt that thread and leave a written decision request as its deliverable: the decision, the concrete options, your recommendation and the reason. Finish everything the halt doesn't block.

## Not for

- **What the request means** — that is intent-lock, the front gate, and it runs before work starts. If the decisions you are collecting are readings of the goal rather than forks inside it, stop and run intent-lock instead.
- **A misread discovered after delivery** — that is misread-capture.
- **A plan the user presents for critique or improvement** — that is plan-critique. Its batched interview owns the forks its critique surfaces; this skill takes over only when execution of the revised plan begins and surfaces new forks.
- **Decisions the agent can settle itself.** The code, the conversation, and the conventions answer most "decisions"; interviewing for those is offloading work, not resolving it. The interview carries only what genuinely belongs to the user.
