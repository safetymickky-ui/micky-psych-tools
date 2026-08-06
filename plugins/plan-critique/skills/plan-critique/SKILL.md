---
name: plan-critique
description: Critiques an existing plan and rebuilds it stronger — runs nine adversarial lenses (goal-fit, gaps, sequencing, feasibility, risk, assumptions, verifiability, simplicity, alternatives) over a plan the user already has, applies the repairs with one right answer, and relentlessly interviews the user in batched option-picker rounds, uncapped until every fork only they can decide (scope cuts, deadline vs quality, risk appetite) is resolved or they stop it. Delivers a verdict-first critique plus the full revised plan under a decision ledger. Use when the user presents a plan and says "critique this plan", "review my plan", "improve this plan", "find weaknesses in my plan", "poke holes in my plan", "stress-test my plan", "is this plan any good", "วิจารณ์แผน", "ช่วยปรับแผนให้ดีขึ้น", or runs /critique-plan. Not for drafting a plan from a bare goal (intent-lock, then draft), pre-build request ambiguity (intent-lock), the agent's own mid-task execution decisions (decision-interview), or reviewing code or prose.
---

# Plan Critique

A plan is a stack of guesses formatted to look like a schedule. The cheapest place it can fail is on paper, before anything is spent — so this skill's job is to make it fail there: run the lenses until the plan breaks, repair what has one right answer, and put every fork that trades on the owner's priorities in front of the owner until each is resolved. The deliverable is never a list of complaints. It is the better plan.

**The object is a plan that already exists.** Intent-lock interrogates a *request* before work starts and is forbidden to propose a better one; decision-interview resolves the *agent's own* decisions mid-execution. This skill sits between them and inverts the first rule: handed an existing plan, proposing better **is the job** — but only the plan moves. The goal stays the user's goal. A critique that swaps in a better goal has failed exactly the way intent-lock fails by rewriting the request.

## When it fires

- The user presents a plan and asks for judgment or improvement: "critique this plan", "review my plan", "improve this plan", "find weaknesses / poke holes in my plan", "stress-test my plan", "is this plan any good", "วิจารณ์แผน", "ช่วยปรับแผนให้ดีขึ้น" — or runs `/critique-plan`.
- Unprompted: offer it (one line, don't seize) when the user shows a finished plan whose execution would be expensive and asks anything short of "execute it".
- If the user hands over a plan and says **execute it**, this skill stays silent — that is execution, and the forks execution surfaces belong to decision-interview.

## Procedure

### 0. Resolve the plan — the object gate

A plan can arrive as pasted text, a file, this session's plan-mode output, a roadmap, a protocol, or a vault artifact fetched via vault-keeper. Read it whole before the first judgment.

- **No plan, only an intention** ("plan my board prep") → stop. This skill critiques; it does not draft. Route the request through intent-lock, draft the plan, then offer to critique the draft.
- **The object is code, prose, or a report** → not this skill, say so and route onward.
- Collect what the plan states about its own goal, success criteria, constraints, resources, and deadline. What it fails to state is a finding, not a licence to guess.

### 1. The yardstick

A critique without a yardstick is taste. Establish what the plan is judged against: the goal, what success observably looks like, the binding constraints (time, money, people), and the owner's risk appetite. Take each from the plan or the conversation and name the source. A missing yardstick item that would change the critique is the **first interview round** — you cannot judge feasibility without knowing whether the deadline is real. Never invent a yardstick silently.

### 2. Critique — run the lenses

Run all nine lenses in `references/critique-lenses.md` — goal-fit, completeness, sequencing, feasibility, risk, hidden assumptions, verifiability, simplicity, alternatives — and run them all even after the first fatal finding, so the interview batches once instead of dripping.

Every finding carries: **where** in the plan · **what breaks** · **why** (evidence or reasoning, not vibes) · **severity** (fatal / costly / friction) · **a repair or a fork**. A finding without a repair or a fork is commentary, and commentary is cut. A finding whose soundness hangs on a factual or clinical claim is flagged, not adjudicated — evidence questions route to pubmed-research-note (clinical) or the owning research skill; this skill judges the plan's structure, never the facts inside it.

### 3. Triage — repairs vs forks

- **Repair** — one fix dominates and needs no value judgment from the owner → apply it to the revised plan and credit it in the findings.
- **Fork** — competing repairs produce materially different plans, or the repair trades on priorities only the owner holds (scope cuts, budget, deadline vs quality, what to drop, risk appetite) → the interview.
- **Always-fork overrides:** any plan step that is destructive, irreversible, or outward-facing in the real world — send, publish, spend, delete, announce, sign — earns a question about whether and when it stays, never a silent repair. And anything the conversation or the plan's own text already settles is resolved in place, source named, never asked.
- Sub-threshold preferences get a stated default in the ledger and no question. Padding the interview with preferences is how the fork that mattered gets abandoned.

### 4. The interview — relentless, batched, through the option-picker

- **Every question goes through the option-picker, never prose.** One call per round, up to four questions per call; more survivors mean more rounds in dependency order, not a bigger round.
- **Dependency order.** A fork that creates or kills other forks leads — "is the deadline movable" decides half the feasibility repairs. Never ask a question whose relevance hangs on an unanswered one.
- **Options are concrete revised-plan outcomes** — "cut the pilot, ship to all sites in week 3" — never labels. The recommended repair goes first, marked "(Recommended)", with the reason in its description. A typed answer beats the option set. multiSelect where several repairs can hold at once.
- **Relentless means uncapped rounds, not a lowered bar.** The interview ends on exactly three conditions: saturation (no fork above the threshold remains), the user stopping it ("stop", "LOCK", silence, an abandoned picker — all sovereign, instant, unargued), or two consecutive rounds that resolve nothing (say so plainly and convert the residue to recommended defaults). Extending the interview by promoting preferences into questions is the interview eating the plan it exists to improve.
- **Push once, then take the answer.** If the user picks a repair that fails their own stated goal, name both sides in one line, once. If they hold, the plan takes their answer and the finding stays in the report as theirs.

### 5. Deliver — verdict first, then the plan

- **Verdict line first:** sound / sound with repairs / needs rework / wrong plan for the goal — plus the single biggest problem, one sentence.
- **Findings by severity**, each closed by the repair applied, the fork's resolution, or an open flag.
- **The revised plan, whole** — a plan is used whole, never as a diff — with the decision ledger on top (`Decided: … · Defaults: … — say if wrong`) and any fork the user's stop left unresolved marked inline where it sits: `[OPEN — A vs B; recommended A because …]`.
- **Every change traces** to a finding or an interview answer. No silent rewrites, no additions no lens demanded, and the goal untouched.
- The critique is working material: file to the vault via vault-keeper **only on explicit request**.

## Autonomous fallback — when nobody can answer

An unattended session or an abandoned picker is a stop, not a licence to wait. Reversible forks take the recommended repair, surfaced in a `Decided without you:` ledger with one-line reasons. A fork whose branches include a destructive, irreversible, or outward-facing real-world step is never defaulted — the revised plan carries it as a marked decision point with the recommendation and reason, and the verdict names it. The critique ships either way; silence never downgrades it to commentary.

## Not for

- **Drafting a plan from a bare goal.** Nothing to critique yet — intent-lock the request, draft, then come back.
- **What a request means** — intent-lock, the front gate.
- **The agent's own mid-task decisions** — decision-interview; and when execution of the revised plan later surfaces new forks, they go there too.
- **Code review, prose editing, or evidence appraisal.** A plan *about* code is in scope; the code itself is not. Clinical evidence verdicts belong to pubmed-research-note.
- **Executing the plan.** The skill ends where the revised plan begins.
