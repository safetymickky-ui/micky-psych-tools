# plan-critique

Adversarial critique of an **existing plan** that ends in a **better plan**. Nine lenses
(goal-fit, completeness, sequencing, feasibility, risk, hidden assumptions, verifiability,
simplicity, alternatives) find where the plan breaks; repairs with one right answer are
applied directly; every fork only the plan's owner can decide — scope cuts, deadline vs
quality, risk appetite — is resolved in a relentless batched option-picker interview,
uncapped until saturation or the user stops it. Deliverable: a verdict-first critique plus
the full revised plan under a decision ledger.

## Components

- **skill `plan-critique`** — the whole procedure: object gate → yardstick → nine lenses →
  triage repairs vs forks → batched interview → verdict + revised plan. Lens catalog in
  `skills/plan-critique/references/critique-lenses.md`.
- **`/critique-plan [plan-or-path]`** — manual trigger; empty argument critiques the plan
  most recently shown or produced in the session.

## Where it sits

The third gate in the alignment family:

- **intent-lock** — pre-build: what does the *request* mean? Never proposes better.
- **plan-critique** — a *plan* exists: proposing better **is** the job; the goal stays
  the user's.
- **decision-interview** — mid-execution: the *agent's own* decisions, swept and batched.

Not for drafting a plan from a bare goal, code review, prose editing, evidence
adjudication (pubmed-research-note), or executing the plan. Vault filing via vault-keeper
on explicit request only.
