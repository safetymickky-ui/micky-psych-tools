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

Before starting, read [references/rules.md](references/rules.md) (credits, idempotency,
consent, Blender discipline — binding at every stage) and
[references/loop.md](references/loop.md) (the gate protocol).

<!-- platform:begin -->
## Platform: Claude Code

- `<plugin_root>` is this plugin's directory: two levels above this skill's base directory. Use absolute paths in every command.
- **Ask the user** = `AskUserQuestion`, recommended option first with a label ending in "(Recommended)". Only you (the main thread) ask; subagents cannot.
- **Look at a PNG** = `Read` on the file. That shows it to you only.
- **Show the user a PNG** = `SendUserFile` with `display: "render"` when the session has it; otherwise give its absolute path. Do this before every checkpoint question, and put the absolute path in the question text.
- **Image route** (concepts, turnarounds, image fixes): Meshy `nano-banana-pro` at 9 credits per image — `meshy_text_to_image` for concepts, `meshy_image_to_image` with `reference_file_paths` for turnarounds and fixes. A turnaround set is 3 images = 27 credits. Every image costs credits, so every image fix is a paid request.
- **Roles:**

| Role | Run it as | Credits |
|---|---|---|
| maker | `Agent` with `subagent_type: "idea-to-3d:idea3d-maker"`; the prompt gives the role file `<plugin_root>/skills/idea-to-3d/references/roles/maker.md`, slug, work root, plugin root, the stage `SKILL.md` path and steps, and the approved budget | approved budget only |
| critic | `Bash`: `python "<plugin_root>/skills/idea-to-3d/scripts/critique.py" <slug> <gate> --work-root <root>` with `timeout: 600000` | none |
| critic fallback | `Agent` with `subagent_type: "idea-to-3d:idea3d-critic"`; the prompt gives `references/roles/critic.md`, gate, rubric, inputs, and the absolute out path `<root>/work/<slug>/critic-tmp/<gate>-r<r>.raw.json` | none |
| reviser | `Agent` with `subagent_type: "idea-to-3d:idea3d-reviser"`; the prompt gives `references/roles/reviser.md`, slug, work root, plugin root, gate, round, the review path `critique.py` printed, rubric, stage skill, and `maker_commands` (the `commands` from the stage's last maker report) | none (it has no Meshy tools) |

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
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" init <slug> --idea "<idea>" --height <meters> [--non-humanoid] --clips "idle,walk,wave"
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" show <slug>
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" get-task <slug> <step_key>
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-task <slug> <step_key> --task-id <id> --tool <tool> --task-type <type> --credits <n> --status <status>
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-checkpoint <slug> <A|B|C> --approved true --choice "<choice>"
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" set-critic <slug> gemini|claude
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" review-history <slug> [--gate A1|A2|B|C]
```

## Execution Protocol

### 0. Start or resume

- Derive `<slug>` (lowercase kebab-case, e.g. `fox-knight`).
- If `work/<slug>/pipeline.json` exists, run `show` and `review-history` and resume from the current stage, any unapproved checkpoint, any in-progress Meshy `task_id`, or the last gate round.
- Otherwise run `init` and write `work/<slug>/idea.md` yourself (concept-art Step 1).

### 1. Stage 1 — concepts, gate A1, Checkpoint A, turnarounds, gate A2

1. Ask the user, in one question, to approve concept generation and the outside services. Say that the images and brief go to Meshy (`meshy.ai`) and, for review, to Gemini (Google, through the Antigravity CLI). Give the cost from the Platform image route. Options:
   - (Recommended) 3 concepts, review by Gemini.
   - 4 concepts, review by Gemini.
   - 3 concepts, review by the Claude critic only (nothing goes to Gemini).
   Record the answer with `set-critic <slug> gemini` or `set-critic <slug> claude`.
2. Dispatch the maker for concept-art Step 2 with the approved budget. It writes `images/concept-<n>.png` and `preview/concepts.png`.
3. Run gate A1 ([loop.md](references/loop.md)).
4. **Checkpoint A** — look at `preview/concepts.png` and show it to the user, then ask in one question: which concept (recommended first, with the reason and the gate A1 summary), together with what continuing costs — the turnarounds (Platform image route) and Stage 2 (`2 × meshy-7.1` 4K = 60 credits, or `1 × meshy-6-lite` = 15). Offer the scripted Blender build when `idea.md` flags it. Record with `record-checkpoint <slug> A`, and copy the chosen concept to `images/chosen-concept.png` (gate A2 compares the turnarounds against it).
5. Dispatch the maker for concept-art Step 4 (turnarounds), naming the chosen concept (`concept-<n>`), with the approved budget.
6. Run gate A2. Its paid fixes (regenerating a view) are asked as in loop.md.

### 2. Stage 2 — image-to-3D, gate B, Checkpoint B

1. Dispatch the maker for image-to-3d Steps 2–3 with the Stage 2 budget approved at Checkpoint A. It writes the tries and `preview/tries.png`.
2. Run gate B.
3. **Checkpoint B** — look at `preview/tries.png` and show it to the user, then ask in one question: which try (recommended first, with the gate B summary), together with the Stage 3 cost (`meshy_remesh` 5 + `meshy_rig` 5 + `meshy_animate` 3 per action, naming the clips from `idea.md`, or remesh only, 5, for non-humanoids). Record with `record-checkpoint <slug> B` and copy the chosen try to `meshy/<slug>-meshy.glb`.

### 3. Stage 3 — remesh, rig, clips

Dispatch the maker for rig-animate Steps 2–4 (Step 2 only for non-humanoids) with the Stage 3 budget: the remesh, the rig and one `meshy_animate` call per approved clip named in the budget. The maker looks up each `action_id` with the free `meshy_list_animations` (rig-animate Step 1.2). No gate here: the rig and clips
are judged at gate C once Blender renders them.

### 4. Stage 4 — Blender finish, gate C, Checkpoint C

1. Dispatch the maker for blender-finish Steps 1–3 (free). `export-check.py` must be run with `--report "work/<slug>/out/quality_report.json"`.
2. Run gate C. Re-rig (5) and re-animate (3 per action) fixes come back as paid requests.
3. **Checkpoint C** — look at `preview/sheet.png` and show it to the user, then ask: approve, or request changes. Show the `check-glb.py` result and the gate C summary. Record with `record-checkpoint <slug> C`.

## Guardrails

- Every credit-spending call needs the user's yes in this run, with tool, model and credits named.
- Never re-create a Meshy task recorded in `pipeline.json`; poll it.
- The critic never sees the maker's or reviser's messages.
- Stop at every checkpoint until the user answers.
