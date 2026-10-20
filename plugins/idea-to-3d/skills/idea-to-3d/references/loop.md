# Critic loop protocol

Every stage's output is judged by an independent critic and revised before the user sees
it. This file is shared by the Claude Code and Antigravity copies of the plugin, so it never
names a platform tool: "ask the user" means the platform's question tool, "dispatch" means
its subagent tool, as mapped in the orchestrator's Platform section.

## Gates

| Gate | Runs | Critic inputs (under `work/<slug>/`) |
|---|---|---|
| A1 | after the concept candidates, before Checkpoint A | `idea.md`, `preview/concepts.png` |
| A2 | after the turnarounds, before Stage 2 spends credits | `idea.md`, `images/chosen-concept.png`, `images/front.png`, `images/side.png`, `images/back.png` |
| B | after the Meshy tries, before Checkpoint B | `idea.md`, `images/front.png`, `preview/tries.png` |
| C | after the Blender finish, before Checkpoint C (also judges Stage 3's rig and clips) | `idea.md`, `images/front.png`, `preview/sheet.png`, `out/quality_report.json` |

Rubrics: `references/rubrics/<gate>.md`. Schema: `references/review.schema.json`.

## Before the first gate

Record the user's answer to the Gemini question (asked together with the first Meshy
consent): `pipeline_state.py set-critic <slug> gemini` or `... claude`. `critique.py`
refuses to run until it is recorded.

## Steps at each gate

Round `r` starts at 0.

1. **Critique.** Run `python "<plugin_root>/skills/idea-to-3d/scripts/critique.py" <slug> <gate> --work-root <root>`. It can take several minutes; allow up to 10. It prints the review path.
   - exit 0: read the review.
   - exit 2 or 3: dispatch the critic role (`roles/critic.md`) with the gate, the rubric path, the input files and the output path `work/<slug>/reviews/<gate>-r<r>.raw.json`. Then run `critique.py <slug> <gate> --from-file <raw path> --critic claude-fallback --reason "exit <code>: <first stderr line>"`. If that also fails, go to the checkpoint and say the gate is unreviewed.
   - exit 1: an input is missing or consent is not recorded. Fix that and rerun.
2. **PASS** → go to the checkpoint.
3. **REVISE and r < 2** → dispatch the reviser (`roles/reviser.md`) with the review path.
   - If the reviser returns `paid_requests`, ask the user once for all of them: one option per request (tool, model, credits, issue it fixes, recommended first: the one fixing the most severe issue) plus "Skip paid fixes". For each approved request, dispatch the maker with that request as its budget.
   - If nothing changed a gate input (no free fix applied, no paid fix approved), stop and go to the checkpoint — critiquing unchanged files again wastes a round.
   - Otherwise set r = r + 1 and go back to step 1.
4. **REVISE and r = 2** → go to the checkpoint with the open issues.

## At the checkpoint

Show one short gate summary next to the usual checkpoint content:

```
Gate B: r0 gemini REVISE (1 blocker, 1 major) → fixed B-2 free; new try approved (30 cr)
        r1 gemini PASS. Open issues: none. Fix credits spent: 30.
```

List every open issue with severity, evidence and the suggested fix with its credits.

## Rules

- **Independence.** The critic receives files only — never the maker's or reviser's messages, never `pipeline.json` notes. The orchestrator never judges a gate itself. `critique.py` stages the gate's files in a temporary folder, so Gemini cannot open `reviews/` or `pipeline.json` either.
- **Credits.** `credits` in a review are Meshy list prices. If the platform has a cheaper route for the same fix (a free image generator), use it; the fix then needs no approval. Every other credit-spending fix needs the user's yes in this run, and the maker may spend only what was approved.
- **Idempotency.** Paid fixes follow the pipeline rules: read `pipeline.json` before any Meshy create call and record every `task_id` the moment it exists.
- **Resume.** `pipeline_state.py review-history <slug>` shows the last gate and round; continue from there.
