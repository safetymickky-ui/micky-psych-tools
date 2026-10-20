---
name: idea-to-3d
description: Turns a one-line character or prop idea into a textured, rigged, animated 3D model (.glb) plus a preview sheet (/idea-to-3d). Use when the user wants a 3D character, prop, mascot or figure made from an idea or a concept image, says "make this a 3D model", "idea to 3D", "rig and animate it", or resumes a work/<slug> pipeline. Runs concept art, image-to-3D, remesh/rig/animation on Meshy and headless Blender finishing across three user checkpoints; before each one an independent Gemini critic (Antigravity CLI, Claude fallback) reviews the stage and a reviser fixes it. Spends Meshy credits only after explicit approval. Not for 3D-printing prep or hand-editing an open Blender scene.
---

# Idea to 3D Orchestrator (`/idea-to-3d`)

Turns a one-line idea into an animated `.glb` (`work/<slug>/out/<slug>.glb`) and a preview
sheet (`work/<slug>/preview/sheet.png`). Every stage's output is judged by an independent
critic and revised before the user sees it.

```text
idea → Stage 1 concepts ─ gate A1 ─ [Checkpoint A] ─ turnarounds ─ gate A2
     → Stage 2 image-to-3D ─ gate B ─ [Checkpoint B]
     → Stage 3 remesh, rig, clips → Stage 4 Blender finish ─ gate C ─ [Checkpoint C]

gate = critique.py (Gemini) → reviser (free fixes) → paid fixes only after a yes
       → critique again; ends on PASS or after 2 revise rounds
```

Before starting, read [references/pipeline-rules.md](references/pipeline-rules.md) (credits,
idempotency, consent, Meshy schema notes, Blender discipline, the Claude Code tool mapping in
§6 — binding at every stage) and
[references/loop.md](references/loop.md) (the gate protocol).

<!-- platform:begin -->
## Platform: Claude Code

- `<plugin_root>` is this plugin's directory: two levels above this skill's base directory. Use absolute paths in every command.
- `<root>` is the absolute path of the project folder that holds `work/` (the session's working directory unless the user names another). Run every command from it.
- **Ask the user** = `AskUserQuestion`, recommended option first with a label ending in "(Recommended)". Only you (the main thread) ask; subagents cannot.
- **Look at a PNG** = `Read` on the file. That shows it to you only.
- **Show the user a PNG** = `SendUserFile` with `display: "render"` when the session has it; otherwise give its absolute path. Do this before every checkpoint question, and put the absolute path in the question text.
- **Image route** (concepts, turnarounds, image fixes) — free first: `python "<plugin_root>/skills/idea-to-3d/scripts/generate_image.py" <slug> --out <path under work/<slug>/, e.g. images/concept-1.png> --prompt-file <abs path of the prompt file> [--ref <abs path> ...] --work-root <root>` via `Bash` with `timeout: 600000` (about 70–90 s per image, 0 credits). Write the prompt to `work/<slug>/prompts/<name>.txt` with the Write tool, then pass `--prompt-file <abs path>`: prompts built from `idea.md` contain quotes and backticks that break shell quoting. Turnarounds pass the chosen concept as `--ref`, and `images/front.png` as well for side and back. It runs only when the user agreed to Google (`critic` is `gemini`). If it exits 2, or the user chose not to send anything to Google, use Meshy `nano-banana-pro` at 9 credits per image after approval — `meshy_text_to_image` for concepts, `meshy_image_to_image` with `reference_file_paths` for turnarounds and fixes (a turnaround set is 27 credits). Image fixes on the free route are free-route requests (credits 0, `"route": "free"`): pass the reviser `free_image_route` = the `generate_image.py` command form above (with `--prompt-file`); on the Meshy route every image fix is a paid request. When a maker reports that `generate_image.py` exited 2, rerun the free route once for the missing images only. If it fails again, ask for Meshy `nano-banana-pro` for exactly the missing images (9 each) and re-dispatch the maker with that budget. A `"route": "free"` fix that hits exit 2 becomes a paid request (9 credits per image) in the next question; never re-dispatch it on the free route.
- **Roles:**

| Role | Run it as | Credits |
|---|---|---|
| maker | `Agent` with `subagent_type: "idea-to-3d:idea3d-maker"`; the prompt gives the role file `<plugin_root>/skills/idea-to-3d/references/roles/maker.md`, the rules file `<plugin_root>/skills/idea-to-3d/references/pipeline-rules.md`, slug, work root, plugin root, the stage `SKILL.md` path and steps, and the approved budget; for a fix also the request, its `change` text and the step key ([loop.md](references/loop.md)); for a `"route": "free"` fix, budget "none" and the `generate_image.py` command form from the Image route line | approved budget only |
| critic | `Bash`: `python "<plugin_root>/skills/idea-to-3d/scripts/critique.py" <slug> <gate> --work-root <root>` with `timeout: 600000` | none |
| critic fallback | `Agent` with `subagent_type: "idea-to-3d:idea3d-critic"`; the prompt gives `references/roles/critic.md`, gate, rubric, inputs, and the absolute out path `<root>/work/<slug>/critic-tmp/<gate>-r<r>.raw.json` | none |
| reviser | `Agent` with `subagent_type: "idea-to-3d:idea3d-reviser"`; the prompt gives `references/roles/reviser.md`, the rules file `references/pipeline-rules.md`, slug, work root, plugin root, gate, round, the review path `critique.py` printed, rubric, stage skill, `maker_commands` (the `commands` from the stage's last maker report), and `free_image_route` (when the user agreed to Google) | none (it has no Meshy tools) |

- Never judge a gate yourself: the critic is the script or the critic agent.
<!-- platform:end -->

## Workspace & State (`work/<slug>/pipeline.json`)

```text
work/<slug>/
├── pipeline.json     idea, slug, stage, Meshy task ids with settings & credits, chosen try,
│                     checkpoint answers, critic consent, review log, file paths
├── idea.md           the idea expanded into a brief (look, hex colours, pose, height, style)
├── images/           concept-1.png..concept-4.png, chosen-concept.png (copy of the chosen one),
│                     front.png, side.png, back.png
├── meshy/            <slug>-try-<n>.glb, chosen as <slug>-meshy.glb, <slug>-remesh.glb, rigged & clip GLBs
├── blender/          <slug>.blend
├── out/              <slug>.glb, quality_report.json
├── preview/          concepts.png, turnaround.png, tries.png, sheet.png
└── reviews/          <gate>-r<n>.json critic reviews, reviser backups
```

Manage state with `pipeline_state.py`:

```powershell
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" init <slug> --idea "<idea>" --height <meters> [--non-humanoid] --clips "idle,walk,wave" --work-root <root>
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" show <slug> --work-root <root>
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" get-task <slug> <step_key> --work-root <root>
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-task <slug> <step_key> --task-id <id> --tool <tool> --task-type <type> --credits <n> --status <status> --work-root <root>
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-checkpoint <slug> <A|B|C> --approved true --choice "<choice>" --work-root <root>
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" set-critic <slug> gemini|claude --work-root <root>
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" review-history <slug> [--gate A1|A2|B|C] --work-root <root>
```

## Execution Protocol

### 0. Start or resume

- Derive `<slug>` (lowercase kebab-case, e.g. `fox-knight`).
- If `work/<slug>/pipeline.json` exists, run `show` and `review-history` and resume from the current stage, any unapproved checkpoint, any in-progress Meshy `task_id`, or the last gate round.
- Otherwise run `init` and write `work/<slug>/idea.md` yourself (concept-art Step 1). `init` can be rerun after `idea.md` is written to set `--height`, `--clips` and `--non-humanoid`.

### 1. Stage 1 — concepts, gate A1, Checkpoint A, turnarounds, gate A2

1. Ask the user, in one question, to approve concept generation and the outside services. Say that the images and brief go to Gemini (Google, through the Antigravity CLI) for image generation and review, and that later the 3D inputs go to Meshy (`meshy.ai`). Give the cost from the Platform image route. Options:
   - (Recommended) 3 concepts, free through Antigravity; Gemini reviews each stage (images and brief go to Google, later the 3D inputs go to Meshy).
   - 4 concepts, same.
   - 3 concepts, nothing to Google: images through Meshy (27 credits) and the Claude critic.
   Record the answer with `set-critic <slug> gemini` or `set-critic <slug> claude`.
2. Dispatch the maker for concept-art Step 2 with the approved budget. It writes `images/concept-<n>.png` and `preview/concepts.png`.
3. Run gate A1 ([loop.md](references/loop.md)).
4. **Checkpoint A** — look at `preview/concepts.png` and show it to the user, then make one question call with two questions (the question tool allows at most 4 options per question): the concept (recommended first, with the reason and the gate A1 summary; add the scripted Blender build option when `idea.md` flags it, within 4 options), and the Stage 2 tier, together with what continuing costs — the turnarounds (0 credits on the free route, 27 on the Meshy route) and Stage 2 (`2 × meshy-7.1` 4K = 60 credits, or `1 × meshy-6-lite` = 15). Record with `record-checkpoint <slug> A --approved true --choice concept-<n> --notes "stage2: <tier and credits, e.g. 2 x meshy-7.1 4K = 60>" --work-root <root>`, and copy the chosen concept to `images/chosen-concept.png` (gate A2 compares the turnarounds against it).
5. Dispatch the maker for concept-art Step 4 (turnarounds), naming the chosen concept (`concept-<n>`), with the approved budget. It must also build the turnaround sheet `preview/turnaround.png` (Step 4.3, the `--normalize` command), which the after-A2 question shows.
6. Run gate A2. Its paid fixes (regenerating a view) are asked as in loop.md.
7. **After gate A2** — if it ended PASS, go to Stage 2. Otherwise (open issues at the cap, failed or declined fixes, unapproved paid fixes, or an unreviewed gate), look at `preview/turnaround.png` and show it to the user, then ask in one question, with the gate A2 summary and the open issues: (Recommended) continue to Stage 2 with the budget approved at Checkpoint A / stop here / any `user choice:` fix. Record the answer without touching the Checkpoint A pick: `record-checkpoint <slug> A --approved true --choice concept-<n> --notes "<the Checkpoint A notes>; A2: <answer>" --work-root <root>` (the same `concept-<n>`). On "stop", record it the same way with `A2: stop` and end the run; never set `--approved false` here.

### 2. Stage 2 — image-to-3D, gate B, Checkpoint B

1. Dispatch the maker for image-to-3d Steps 2–3 with the Stage 2 budget approved at Checkpoint A. It writes the tries and `preview/tries.png`.
2. Run gate B.
3. **Checkpoint B** — look at `preview/tries.png` and show it to the user, then ask in one question: which try (recommended first, with the gate B summary), together with the Stage 3 cost (`meshy_remesh` 5 + `meshy_rig` 5 + `meshy_animate` 3 per action, naming the clips from `idea.md`, or remesh only, 5, for non-humanoids). Record with `record-checkpoint <slug> B` and copy the chosen try to `meshy/<slug>-meshy.glb`.

### 3. Stage 3 — remesh, rig, clips

Dispatch the maker for rig-animate Steps 2–4 (Step 2 only for non-humanoids) with the Stage 3 budget: the remesh, the rig and one `meshy_animate` call per approved clip named in the budget. The maker looks up each `action_id` with the free `meshy_list_animations` (rig-animate Step 1.2). No gate here: the rig and clips
are judged at gate C once Blender renders them.

### 4. Stage 4 — Blender finish, gate C, Checkpoint C

1. Dispatch the maker for blender-finish Steps 1–3 (free). `export-check.py` must be run with `--report "work/<slug>/out/quality_report.json"`.
   When `actrun` is on PATH, Steps 1–3 can run as one Actionforge graph instead (`blender-finish/scripts/stage4-animate.act`, which stops on the first failing step); the blender-finish skill gives its env vars and args.
2. Run gate C. Re-rig (5) and re-animate (3 per action) fixes come back as paid requests.
3. **Checkpoint C** — look at `preview/sheet.png` and show it to the user, then ask: approve, or request changes. Show the `check-glb.py` result and the gate C summary. Record with `record-checkpoint <slug> C`.

## Guardrails

- Every credit-spending call needs the user's yes in this run, with tool, model and credits named.
- Never re-create a Meshy task recorded in `pipeline.json`; poll it.
- The critic never sees the maker's or reviser's messages.
- Stop at every checkpoint until the user answers.
