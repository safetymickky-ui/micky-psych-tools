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

On entering a gate, set `start` = the next round from `pipeline_state.py review-history <slug> --gate <gate>` (0 if none). Each critique's round `r` is read from the path `critique.py` prints (`<gate>-r<r>.json`); always hand the reviser that printed path. The cap counts this pass: revise only while `r − start < 2`.

1. **Critique.** Run `python "<plugin_root>/skills/idea-to-3d/scripts/critique.py" <slug> <gate> --work-root <root>`. It can take several minutes; allow up to 10. It prints the review path.
   - exit 0: read the review.
   - exit 2 or 3: dispatch the critic role (`roles/critic.md`) with the gate, the rubric path, the input files and the absolute output path `<root>/work/<slug>/critic-tmp/<gate>-r<r>.raw.json` (`r` = the next round from `review-history`; this folder is outside `reviews/`). Then run `python "<plugin_root>/skills/idea-to-3d/scripts/critique.py" <slug> <gate> --from-file <raw path> --critic claude-fallback --reason "exit <code>: <first stderr line>" --work-root <root>`. If that also fails, go to the checkpoint and say the gate is unreviewed.
   - exit 1: an input is missing or consent is not recorded. Fix that and rerun. If the rerun exits 1 again, go to the checkpoint and say the gate is unreviewed, quoting the stderr line.
2. **PASS** → go to the checkpoint.
3. **REVISE and `r − start < 2`** → dispatch the reviser (`roles/reviser.md`) with slug, work_root, plugin_root, gate, round, the review path `critique.py` printed, the rubric, the stage skill, and `maker_commands` (the `commands` list from the stage's last maker report).
   - If the reviser returns `paid_requests`, ask the user once, multi-select: one option per request (tool, model, credits, the issue it fixes; most severe first, marked recommended) plus "Skip paid fixes". If the question tool caps the number of options, offer the most severe requests and list the rest as open issues.
   - For each approved request, one at a time (never in parallel — `pipeline.json` writes are not locked), dispatch the maker with that request as its budget, the request's `change` text, and these steps:
     - A1 → concept-art Step 2 (concept generation) for the named concept, then rebuild `preview/concepts.png` (Step 2.3).
     - A2 → concept-art Step 4 (turnaround) for the named view, then the `--normalize` turnaround command (Step 4.3).
     - B → image-to-3d Step 2 (create) for one new try: if a `try-<n>` task recorded with settings `{"fix": "<issue id>"}` exists, poll it; otherwise use the next free `try-<n>` and record it with `--settings '{"fix": "<issue id>"}'`, then Step 3 (comparison render) listing every try.
     - C → rig-animate Steps 2–4 (remesh, rig, animate) for what the request names, then blender-finish Steps 1–3 (import-merge, export-check, render-sheet).
     - A paid fix that redoes a recorded step uses the step key `<step_key>-<issue id>` (for example `rig-C-2`, `anim-wave-C-3`, `concept-3-A1-1`).
   - After the makers finish, the gate's preview is current.
   - If the reviser's `inputs_changed` is false and no maker run wrote a gate input, go to the checkpoint — critiquing unchanged files again wastes a round.
   - Otherwise go back to step 1.
4. **REVISE and `r − start = 2`** → go to the checkpoint with the open issues.

## At the checkpoint

Show one short gate summary next to the usual checkpoint content:

```
Gate C: r0 gemini REVISE (1 blocker, 1 major) → fixed C-2 free (import-merge --height 1.2); re-rig approved (5 + 3 cr)
        r1 gemini PASS. Open issues: none. Fix credits spent: 8.
```

List every open issue with severity, evidence and the suggested fix with its credits. Open issues are the issues of the gate's last review, plus the reviser's `failed` and `declined` entries and any paid requests the user did not approve.

## Rules

- **Independence.** The critic receives files only — never the maker's or reviser's messages, never `pipeline.json` notes. The orchestrator never judges a gate itself. `critique.py` stages the gate's files in a temporary folder, so Gemini cannot open `reviews/` or `pipeline.json` either.
- **Credits.** `credits` in a review are Meshy list prices. If the platform has a free route for the same fix (a free image generator), the orchestrator names it in the reviser's dispatch prompt and the reviser writes the fix as a request with `credits: 0` and `"route": "free"`. A request with `credits: 0` needs no approval: the orchestrator dispatches the maker for it with the platform's free route. Every other credit-spending fix needs the user's yes in this run, and the maker may spend only what was approved.
- **Idempotency.** Paid fixes follow the pipeline rules: read `pipeline.json` before any Meshy create call and record every `task_id` the moment it exists.
- **Resume.** First finish any recorded Meshy task that is not SUCCEEDED (poll it, download it, rerun the gate's preview step). Then read `pipeline_state.py review-history <slug> --gate <gate>`. If the last review of the gate is REVISE and `reviews/backup-<gate>-r<r>/` does not exist, dispatch the reviser for it; otherwise run the critic again. Use the same `start` rule as on entry.
