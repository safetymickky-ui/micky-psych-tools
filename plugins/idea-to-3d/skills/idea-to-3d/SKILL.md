---
name: idea-to-3d
description: Turn a one-line character or prop idea into a textured, rigged, animated 3D model (.glb) and preview sheet (/idea-to-3d). Orchestrates concept art (Nano Banana), image-to-3D (Meshy), remeshing/rigging/animation (Meshy), and headless Blender cleanup, clip merging, validation, and preview rendering across three user checkpoints.
---

# Idea to 3D Orchestrator (`/idea-to-3d`)

This skill orchestrates the full 4-stage pipeline that turns a one-line idea into an animated `.glb` model (`work/<slug>/out/<slug>.glb`) and preview sheet (`work/<slug>/preview/sheet.png`).

```text
idea → Stage 1: concept images (Nano Banana) → [Checkpoint A]
     → Stage 2: image-to-3D (Meshy)          → [Checkpoint B]
     → Stage 3: remesh, rig & clips (Meshy)
     → Stage 4: clean-up, merge, check & sheet (Blender) → [Checkpoint C]
```

**Read [`references/pipeline-rules.md`](./references/pipeline-rules.md) first** — credit confirmation, task idempotency, checkpoint gating, upload consent, Meshy schema notes, and the Claude Code tool mapping (§6).

## Workspace & State (`work/<slug>/pipeline.json`)

All generated files for an idea live in the current workspace under `work/<slug>/`:

```text
work/<slug>/
├── pipeline.json     idea, slug, stage, every Meshy task id with settings & credits, chosen try,
│                     checkpoint answers, file paths
├── idea.md           the idea expanded into a character brief (look, hex colours, pose, height, style)
├── images/           concept-1.png..concept-4.png; chosen copied to front.png, plus side.png & back.png
├── meshy/            <slug>-try-<n>.glb, chosen as <slug>-meshy.glb, <slug>-remesh.glb, rigged & clip GLBs
├── blender/          <slug>.blend
├── out/              <slug>.glb
└── preview/          concepts.png, tries.png, sheet.png, per-view renders
```

Manage `work/<slug>/pipeline.json` with [`pipeline_state.py`](./scripts/pipeline_state.py):

```powershell
# Initialize or resume a pipeline run:
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" init <slug> --idea "<idea>" --height <meters> [--non-humanoid] --clips "idle,walk,wave"

# Inspect existing state when resuming in a new conversation:
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" show <slug>

# Look up whether a Meshy task was already created (NEVER recreate a recorded task):
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" get-task <slug> <step_key>

# Record a newly created Meshy task immediately:
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-task <slug> <step_key> --task-id <id> --tool <tool> --task-type <type> --credits <n> --status <status>

# Record a checkpoint decision (or combine with set-stage):
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-checkpoint <slug> <A|B|C> --approved true --choice "<choice>"
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" set-stage <slug> <stage> --checkpoint <A|B|C> --approved true --choice "<choice>"
```

## Execution Protocol

1. **Check for existing state first:**
   - Derive `<slug>` (lowercase kebab-case, e.g. `teacup-robot`, `fox-knight`).
   - If `work/<slug>/pipeline.json` exists, read it first and resume from the current `stage` and any unapproved checkpoint or in-progress Meshy `task_id`.
   - If starting fresh, run `pipeline_state.py init` and expand the brief into `work/<slug>/idea.md`.

2. **Stage 1 — Concept Images (`concept-art` skill):**
   - Follow [`../concept-art/SKILL.md`](../concept-art/SKILL.md).
   - Write `work/<slug>/idea.md` specifying shape, hex colours, materials, real-world height in meters (`Height: <X> m`), whether humanoid or non-humanoid, mood, and style (`"polished 3D render, soft studio lighting, Pixar-like"`).
   - Generate 3–4 distinct concept images (`<slug>_concept_1` .. `<slug>_concept_4`) via the `image-generator` subagent and lay out `work/<slug>/preview/concepts.png`.
   - If the character is round, hard-surface, and symmetric (like a hovering spherical robot), also offer a **pure scripted Blender build** as an option at Checkpoint A.
   - **STOP at Checkpoint A (MUST call `ask_question`):** View `work/<slug>/preview/concepts.png` with `view_file`, then call `ask_question` presenting `concepts.png` and combining the concept choice with Stage 2 upload & credit approval (`2 × meshy-7.1` 4K tries = 60 credits, or 15 credits for 1 `meshy-6-lite` tracer try).
   - Once the user picks a concept, record Checkpoint A in `pipeline.json`, copy the chosen concept to `work/<slug>/images/front.png`, and send a message (`send_message`) to the existing `image-generator` subagent with the chosen concept in `ImagePaths` to generate `side.png` and `back.png`.

3. **Stage 2 — Image to 3D (`image-to-3d` skill):**
   - Follow [`../image-to-3d/SKILL.md`](../image-to-3d/SKILL.md).
   - Verify upload consent & credit approval (60 credits for 2 `meshy-7.1` 4K tries) was obtained via `ask_question`.
   - Create the 2 tries using `meshy_multi_image_to_3d` with `file_paths: [".../front.png", ".../side.png", ".../back.png"]` (recording each `task_id` immediately in `pipeline.json`), poll to completion with `timeout_seconds: 150`, and download via `meshy_download_model` (`save_to`) as `work/<slug>/meshy/<slug>-try-1.glb` and `<slug>-try-2.glb`.
   - Render the side-by-side comparison sheet `work/<slug>/preview/tries.png` using `render-meshy.py`.
   - **STOP at Checkpoint B (MUST call `ask_question`):** View `work/<slug>/preview/tries.png` with `view_file`, then call `ask_question` presenting `tries.png` and combining the try selection with Stage 3 credit confirmation (`5 credits remesh + 5 credits rig + 3 credits × N actions`, or `5 credits remesh` only for non-humanoids).
   - Copy the chosen try to `work/<slug>/meshy/<slug>-meshy.glb` and record Checkpoint B in `pipeline.json`.

4. **Stage 3 — Remesh, Rig, Animate (`rig-animate` skill):**
   - Follow [`../rig-animate/SKILL.md`](../rig-animate/SKILL.md).
   - Call `meshy_list_animations` (free) to look up the exact `action_id` for `idle` (`0`) and any custom actions (e.g., `wave` = `28`) — never guess `action_id`.
   - Run `meshy_remesh` and download `work/<slug>/meshy/<slug>-remesh.glb`.
   - For humanoids in A/T-pose: run `meshy_rig`, download `work/<slug>/meshy/<slug>-rigged.glb` and the free `walk` GLB using `download-asset.py`, then run `meshy_animate` (`{ "rig_task_id": "<id>", "action_id": <int> }`, no `fps` key) for the chosen actions and download each clip GLB into `work/<slug>/meshy/`.
   - For non-humanoids (or characters Meshy cannot auto-rig): skip `meshy_rig`/`meshy_animate` and proceed to Stage 4 where `import-merge.py --procedural-rig` rigs and animates the remeshed model in headless Blender.

5. **Stage 4 — Finish in Blender (`blender-finish` skill):**
   - Follow [`../blender-finish/SKILL.md`](../blender-finish/SKILL.md).
   - Run `import-merge.py` in headless Blender 5.2 to merge all clips onto one armature (or build the procedural Blender armature and `idle` + action clips for non-humanoids), clean up scale/origin/grounding/orientation/seam vertices, and save `work/<slug>/blender/<slug>.blend`.
   - Run `export-check.py` in headless Blender 5.2 to export `work/<slug>/out/<slug>.tmp.glb`, run `check-glb.py`, and atomically replace `work/<slug>/out/<slug>.glb`.
   - Run `render-sheet.py` in headless Blender 5.2 to render `work/<slug>/preview/sheet.png` (concept image in dedicated left column beside 4 views × 3 frames per clip).
   - When `actrun` is on PATH, these three steps can run as one Actionforge graph instead (`blender-finish/scripts/stage4-animate.act`, which stops on the first failing step). See the blender-finish skill for its env vars and args.
   - **STOP at Checkpoint C (MUST call `ask_question`):** View `work/<slug>/preview/sheet.png` with `view_file`, then call `ask_question` presenting `sheet.png` and the `check-glb.py` verification output, and wait for the user's approval.
   - Once approved, record Checkpoint C in `pipeline.json`.

