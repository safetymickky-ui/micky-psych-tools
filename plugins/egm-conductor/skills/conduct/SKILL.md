---
name: conduct
description: >-
  Drives the whole Elephant-Goldfish Model (EGM) spec-driven workflow end to
  end from one entry point: preflight, optional codebase bootstrap,
  brainstorm, draft, Goldfish review and resolve, human PR gate,
  implementation against the approved spec, and drift report. Tracks progress
  in .egm-conductor/state.json so it resumes where it left off. Use when the
  user says "run EGM end to end", "take this idea through EGM", "egm
  pipeline", "spec-driven this feature", "continue the EGM flow", "next EGM
  step", or runs /egm-conductor:conduct. Not for running one EGM stage the
  user named alone (they can type /egm:egm-review etc.), and not when the
  egm@egm plugin is missing and the user declines to install it.
argument-hint: "[idea text | path/to/design.md] [--from <phase>] [--auto]"
---

# EGM Conductor

You are the conductor. EGM (`egm@egm`) owns the content of every stage; you own
order, handoffs, state, and the gates between stages. Never rewrite or shortcut
an EGM stage: run its own `SKILL.md` as written.

## Arguments

`$ARGUMENTS` may hold, in any order:

- free text: the idea to brainstorm (starts at `brainstorm`)
- a path to an existing `.md`: a brief or design doc (starts at `draft` for a
  brief, `review` for a file under `docs/designs/`)
- `--from <phase>`: force the start phase (one of the phases below)
- `--auto`: skip the conductor's own between-phase confirmations and run the
  review as `uninterrupted`. It never skips EGM's own gates inside brainstorm
  and draft, or the human gate.

## Step 0: Locate EGM and read the project

Run, with the project root as working directory:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/egm_status.py" --project .
```

From its JSON take:

- `egm.root` → call it **EGM_ROOT**. Use only this path. Never guess a cache
  version or glob for another copy.
- `suggested_phase`, `artifacts`, `state`.

Stop and fix before anything else when:

- `egm.installed` is false → tell the user to install, or install on their yes:
  `claude plugin marketplace add google/elephant-goldfish-model` then
  `claude plugin install egm@egm`. A new install needs a Claude Code restart
  before the `egm:egm-*` agent types exist.
- `egm.enabled` is false → `claude plugin enable egm@egm`, then restart.
- `claude_cli.ok` is false → Claude Code is older than 2.1.271, so Goldfish
  isolation (`omitClaudeMd`) is not verified. Say so; continue only if the
  user accepts unisolated reviews.

Then read `EGM_ROOT/docs/claude.md` once. It governs every stage below.

## How to run an EGM stage

EGM skills set `disable-model-invocation: true`, so the `Skill` tool refuses
them. For each stage:

1. Read `EGM_ROOT/skills/<skill_dir>/SKILL.md` with the Read tool.
2. Treat every `${CLAUDE_PLUGIN_ROOT}` in it as **EGM_ROOT** (not this
   plugin's root). Resolve its `references/` against that skill's directory,
   and `agents/`, `resources/`, `docs/` against EGM_ROOT.
3. Follow it in this main thread, passing the inputs from the phase table.
4. Goldfish reviewers: spawn the registered types with the Agent tool,
   `subagent_type: "egm:egm-<name>"` (`egm-synthesizer`, `egm-zoom-out`,
   `egm-comprehension`, `egm-design` (the design critic), `egm-implementation-readiness`,
   `egm-structural`, `egm-style`, `egm-codebase-details`,
   `egm-bootstrap-orchestrator`). Fresh agent each time; never fork or resume
   one. Pass absolute paths only.
5. The stage is over when its own handoff gate is answered. Then record state
   (below) and run the conductor gate.

While you follow brainstorm, draft, review, resolve, or bootstrap, their
execution rules apply in full, including the no-production-code guard. Those
rules end when the stage ends; the `implement` phase is where code is written.

## Phases

| # | Phase | Runs | Input | Done when |
|---|-------|------|-------|-----------|
| 0 | `preflight` | Step 0 | — | EGM located, CLI ok |
| 1 | `bootstrap` (optional) | `egm_bootstrap` | `path` = project root; `target_filename: "EGM.md"` if human READMEs exist and must not change | READMEs or EGM.md written up the tree |
| 2 | `brainstorm` | `egm_brainstorm` | the idea text | `concepts_brief.md` final, handoff gate answered |
| 3 | `draft` | `egm_draft` | `concepts_brief.md` path, or the brief/doc given | `docs/designs/<feature>.md` written |
| 4 | `review` | `egm_review` (it calls `egm_review_loop` and `egm_resolve` itself; read those `SKILL.md` files the same way when it says to) | `TargetFile` = design doc; `Step` = `interactive`, or `uninterrupted` with `--auto` | report(s) written and findings resolved or rejected by the user |
| 5 | `human_gate` | conductor | design doc | user confirms a human approved it |
| 6 | `implement` | conductor | approved design doc | code + tests match its Implementation section |
| 7 | `drift` | `egm_drift_report` | `docs/designs` | `<date>_DRIFT_REPORT.md` written |

**Bootstrap is offered, not assumed.** Offer it only when the project already
has source code and neither `docs/designs/` nor README coverage of its
directories. Skip it for greenfield work.

**Brainstorm → draft handoff.** If brainstorm's gate picks "Publish as RFC",
the next draft input is `docs/designs/<feature>.md`. If it picks "stop", end the
run and record `phase: "brainstorm"`.

**Review.** When EGM asks for `GoldfishContext`, offer the files the design doc
does not already link that the Elephant relied on (for example a root README or
`EGM.md`). Never pass URLs; save the page to a file and pass its path.

**Human gate.** EGM does not replace human review. Ask the user whether to:

- open a PR with the design doc (only on their explicit yes: new branch,
  commit only the design doc and `SITEMAP.md`, push, `gh pr create`), or
- record that a human already approved it, or
- stop here and resume later with `/egm-conductor:conduct`.

Do not enter `implement` until the user says the spec is approved.

**Implement.** The design doc is the plan. Prefer a fresh session that gets
only the design doc path, so the coder is not biased by design-time chat;
offer that first, or implement here if the user wants. Either way:

1. Read the design's Implementation section and every file it names.
2. Work through its steps in order, writing the tests it specifies alongside
   the code, and run them.
3. If the code must deviate from the spec, stop and ask: change the doc or the
   code. Never let them silently diverge.
4. Finish by running the `drift` phase scoped to this one design doc.

**Drift.** After the report, offer to schedule it weekly (EGM's recommended
cadence) with the scheduled-tasks tool. Create the schedule only on a yes.

## State

After each phase, write `.egm-conductor/state.json` in the project root:

```json
{
  "feature": "<feature name>",
  "phase": "<next phase to run>",
  "completed": ["preflight", "brainstorm"],
  "artifacts": {
    "concepts_brief": "concepts_brief.md",
    "design_doc": "docs/designs/<feature>.md",
    "reports": ["consolidated_review_report.md"],
    "pr": "<url or null>"
  },
  "egm_version": "<egm.version>",
  "updated": "<YYYY-MM-DD>"
}
```

Offer once per project to add `.egm-conductor/` to `.gitignore`. On resume,
trust the state file, but check that every artifact it names still exists; if
one is missing, tell the user and restart from the phase that produces it.

## Conductor gate (between phases)

Unless `--auto`, after each phase ask one question with AskUserQuestion:
continue to the next phase (first option), redo this phase, or stop and save.
Point to the artifact by path; never paste its content into chat. With
`--auto`, announce the next phase in one line and continue, but still stop at
`human_gate` and wherever an EGM skill asks the user something.

## Rules

- One phase at a time; never run two EGM stages in parallel.
- Keep review stages 5→9 sequential, as EGM requires.
- Artifacts go to the project (or the `EGM artifact directory:` folder named in
  `CLAUDE.md`/`AGENTS.md`), never the session scratchpad.
- Do not commit or push anything except as approved at the human gate.
