# Critique lenses — the nine passes

Run all nine, in this order, over the whole plan — even after the first fatal finding,
so the fork interview batches instead of dripping. Each lens lists what it hunts, the probes to run, and the
classic failure it exists to catch. A lens that finds nothing reports nothing; never pad.

Finding format, every lens the same:

```
[FATAL|COSTLY|FRICTION] <where in the plan> — <what breaks>: <why, evidence or reasoning>.
  → Repair: <the dominant fix>          # or
  → Fork: <repair A> vs <repair B> — trades on <the owner-held priority>.
```

## 1. Goal-fit

Does every step serve the stated goal — and what goal does the plan *actually* optimize?

- For each step: which goal clause does it serve? A step serving none is scope creep or a
  hidden goal; name which.
- Reconstruct the goal implied by the plan's weighting of effort. If it differs from the
  stated goal, that gap is usually the plan's biggest finding.
- Classic catch: a "migration plan" that is 80% building the new thing and 20% migrating.

## 2. Completeness

What did the plan forget?

- Walk the goal backwards: what must be true on the last day that no step produces?
- Missing: rollback/undo paths, communication to affected people, handover, the step after
  the last step (who operates this?), approvals and lead times, the boring prerequisite.
- Classic catch: the plan ends at "launch" and nothing owns week two.

## 3. Sequencing & dependencies

Is the order survivable?

- Draw the dependency chain. Which steps are silently serialized that could run in
  parallel? Which parallel steps secretly share a resource (the same person, the same
  week)?
- What must be *learned* early but is scheduled late? The riskiest unknown belongs at the
  front, where failing is cheap.
- Classic catch: the irreversible commitment (announce, sign, spend) scheduled before the
  test that would justify it.

## 4. Feasibility

Can the named resources actually do this in the named time?

- Per step: who does it, how long has that taken before, what else are they doing?
- Find the step that is secretly a project — the one-line item hiding 60% of the work.
- Single points of failure: one person, one vendor, one machine, one week of slack.
- Classic catch: a timeline that only works if nothing else happens for a month.

## 5. Risk

What kills it?

- Premortem: it is six months later and the plan failed — write the three most likely
  post-mortems, then check whether the plan defends against any of them.
- External dependencies (approvals, other teams, vendors, regulators): what happens to the
  plan when each slips?
- Which failures are detectable early, and does the plan look for them?
- Classic catch: every risk listed is one the plan's author can control; the fatal ones
  never are.

## 6. Hidden assumptions

What does the plan treat as true without evidence?

- List every load-bearing "surely": demand exists, the data is clean, the dependency
  ships on time, the exam covers what it covered last year.
- For each: what is the cheapest test, and can it move before the steps that depend on it?
- Classic catch: the assumption is inherited from an older plan whose context is gone.

## 7. Verifiability

How would the owner know it is working — before the end?

- Milestones must be outcomes, not activities: "interviewed 10 users" is an activity;
  "3 users pre-ordered" is an outcome.
- Success criteria that cannot fail are not criteria. What observation would say *stop*?
- Kill criteria and checkpoints: where are the dates on which continuing is re-decided?
- Classic catch: a six-month plan whose first falsifiable signal arrives in month five.

## 8. Simplicity

What is here for the plan rather than the goal?

- Which 20% of the steps buy 80% of the outcome — and what would a plan of only those look
  like? The delta is the over-engineering budget.
- Steps that exist to look rigorous (a matrix nobody will read, a phase that only renames
  work) are cut candidates.
- Classic catch: process imported from a bigger organisation than the one executing.

## 9. Alternatives

What is the plan not taken?

- Construct at least one materially different shape — different order, different scope,
  buy instead of build, half the size in half the time — and say plainly why the current
  plan beats it or loses to it. If it loses, that is a fork for the owner, not a rewrite:
  the alternative is offered, never imposed.
- If the owner adopts the alternative, the adopted shape becomes the object: flesh out its
  concrete steps — each tracing to that interview answer — and re-run lenses 1–8 over the
  adopted shape before delivery. Winning the comparison is not a critique of the winner.
  New forks this pass surfaces go back to the interview under its normal termination rules.
- Classic catch: the plan is the first idea, formatted.

## Severity

- **FATAL** — left in place, the plan fails its own stated goal.
- **COSTLY** — the plan survives but pays real time, money, or trust it didn't need to.
- **FRICTION** — drag, confusion, rework; worth fixing when the fix is cheap.

Severity ranks the findings report and orders the interview's leverage; it never
overrides dependency order.
