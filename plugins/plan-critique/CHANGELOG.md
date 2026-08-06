# Changelog — plan-critique

## 0.1.0 — 2026-08-06

- Initial release: one skill (`plan-critique`) + `/critique-plan [plan-or-path]`.
- Nine-lens adversarial critique (goal-fit, completeness, sequencing, feasibility, risk,
  hidden assumptions, verifiability, simplicity, alternatives) with a
  repair-or-fork contract on every finding; lens catalog under
  `skills/plan-critique/references/critique-lenses.md`.
- Relentless batched option-picker interview for owner-held forks: dependency order,
  concrete revised-plan outcomes as options, recommended repair first, uncapped rounds
  ended only by saturation, a user stop, or the two-empty-rounds guard.
- Verdict-first delivery: verdict line → findings by severity → the full revised plan
  under a decision ledger; every change traces to a finding or an interview answer.
- Autonomous fallback: reversible forks take the recommended repair in a
  `Decided without you:` ledger; destructive/irreversible/outward-facing steps are never
  defaulted — carried as marked decision points.
- Boundary: existing plans only — drafting routes through intent-lock, the agent's own
  mid-task decisions to decision-interview, evidence verdicts to pubmed-research-note.
- 6 evals (2 positive incl. Thai triggers, 4 negative).
