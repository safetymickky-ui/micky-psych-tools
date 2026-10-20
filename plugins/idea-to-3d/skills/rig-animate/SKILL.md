---
name: rig-animate
description: Remesh a 3D model to animation-ready quad topology (20,000-30,000 faces), auto-rig humanoids, and generate animation clips (idle, walk, actions) using Meshy MCP tools (meshy_remesh, meshy_rig, meshy_list_animations, meshy_animate, meshy_text_to_motion). Trigger when remeshing, rigging, or animating a 3D model in Meshy or running Stage 3 of /idea-to-3d.
---

# Stage 3: Remesh, Rig, and Animate (`rig-animate`)

`<plugin_root>` is this plugin's directory: two levels above this skill's base directory. Use it as an absolute path in every command.

Converts the raw ~300,000-face image-to-3D mesh into an animation-friendly quad mesh (20,000–30,000 faces), and for humanoid characters auto-rigs and generates animation clips in Meshy. For non-humanoid characters (such as round hovering robots or creatures Meshy cannot auto-rig), remeshes the model and hands off to Stage 4 (`blender-finish`) to rig and animate by script in headless Blender.

## Step 1: Select Animations & Confirm Cost

1. **Read `work/<slug>/pipeline.json` first:**
   ```powershell
   python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" show <slug>
   ```
   - Never re-create any task (`remesh`, `rig`, `anim-bundle`, `motion-<name>`, `anim-<name>`) already recorded in `pipeline.json`.
2. **If humanoid (`is_humanoid: true`), look up preset animation IDs (free):**
   - Call `meshy_list_animations` with `search: "idle"`, `category: "DailyActions"`, or `category: "BodyMovements"` (free).
   - Pick an `idle` clip plus 2 or 3 actions that fit `work/<slug>/idea.md` (note: `meshy_rig` already includes `walk` and `run` for free, so never add their ids to the bundle!). All presets go into one Step 4 bundle, in the order you list them.
   - If `idea.md` asks for a motion that no preset fits (search two or three terms first), plan a custom clip for Step 5 instead: a short prompt (at most 400 characters) and a duration of 2–10 seconds.
3. **Ask the user to confirm credits before calling paid tools:**
   - `meshy_remesh`: **5 credits** (`topology: "quad"`, `target_polycount: 25000`).
   - If humanoid:
     - `meshy_rig`: **5 credits** (includes free walking and running GLBs).
     - `meshy_animate` bundle: **3 credits per action** in one call (list the exact action names and IDs, in bundle order).
     - Each custom clip: `meshy_text_to_motion` **10 credits** (`prime`) or **3 credits** (`swift`), plus **3 credits** for the `meshy_animate` call that applies it (**13** or **6** per clip). Give the prompt (it goes to Meshy), and say that it needs a biped rig and that Meshy keeps the motion for only 3 days, so Step 5 applies it straight away.
   - Wait for the user's explicit **yes**.

## Step 2: Remesh (`meshy_remesh` — 5 credits)

1. Check `pipeline_state.py get-task <slug> remesh`. If not yet created, call `meshy_remesh`:
   ```json
   {
     "input_task_id": "<chosen_try_task_id>",
     "topology": "quad",
     "target_polycount": 25000,
     "target_formats": ["glb"]
   }
   ```
2. Record the `task_id` immediately:
   ```powershell
   python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-task <slug> remesh --task-id <remesh_task_id> --tool meshy_remesh --task-type remesh --credits 5 --status IN_PROGRESS --output "work/<slug>/meshy/<slug>-remesh.glb"
   ```
3. Poll with `meshy_get_task_status` (`task_id: "<remesh_task_id>"`, `wait: true`) until `SUCCEEDED`.
4. Download with `meshy_download_model`:
   ```json
   {
     "task_id": "<remesh_task_id>",
     "task_type": "remesh",
     "format": "glb",
     "save_to": "<abs_path>/work/<slug>/meshy/<slug>-remesh.glb"
   }
   ```
5. Update `remesh` task status to `SUCCEEDED` in `pipeline.json`.

> **Non-humanoid path:** If the character is not a humanoid in A/T-pose (or if `meshy_rig` fails because the character lacks humanoid limbs), stop Stage 3 here, set stage to `blender-finish`, and proceed to Stage 4 where `import-merge.py --procedural-rig` builds a clean armature and animations in Blender.

## Step 3: Auto-Rig Humanoid (`meshy_rig` — 5 credits)

1. Call `meshy_rig`:
   ```json
   {
     "input_task_id": "<remesh_task_id>",
     "height_meters": 1.7
   }
   ```
   *(Use `target_height_m` from `pipeline.json`.)*
2. Record the `task_id` immediately:
   ```powershell
   python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-task <slug> rig --task-id <rig_task_id> --tool meshy_rig --task-type rigging --credits 5 --status IN_PROGRESS --output "work/<slug>/meshy/<slug>-rigged.glb"
   ```
3. Poll with `meshy_get_task_status` (`task_id: "<rig_task_id>"`, `task_type: "rigging"`, `wait: true`, `timeout_seconds: 150`).
4. Note: `meshy_download_model` for `task_type: "rigging"` returns signed cloud URLs in its text response (`Character_output.glb`, plus free `Animation_Walking_withSkin.glb` and `Animation_Running_withSkin.glb`) rather than writing directly to `save_to`. Download the `.glb` URLs into `work/<slug>/meshy/` using [`download-asset.py`](./scripts/download-asset.py):
   ```powershell
   python "<plugin_root>/skills/rig-animate/scripts/download-asset.py" "<rigged_character_glb_url>" "work/<slug>/meshy/<slug>-rigged.glb"
   python "<plugin_root>/skills/rig-animate/scripts/download-asset.py" "<walking_glb_url>" "work/<slug>/meshy/<slug>-clip-walk.glb"
   ```

## Step 4: Animate the Preset Bundle (`meshy_animate` with `action_ids` — 3 credits per action)

One call animates every chosen preset and returns one GLB with one clip per action, in `action_ids` order. Example: `idle` (`action_id: 0`) and `wave` (`action_id: 28` = `Big Wave Hello`).

1. Check `pipeline_state.py get-task <slug> anim-bundle`. If not yet created, call `meshy_animate` (pass **only** `rig_task_id` and `action_ids`, 1 to 10 unique ids; **never** pass `fps`, which the MCP schema rejects):
   ```json
   {
     "rig_task_id": "<rig_task_id>",
     "action_ids": [0, 28]
   }
   ```
2. Record the `task_id` immediately as **one** task under `anim-bundle`, with the clip names in `action_ids` order in `--settings` (Blender-finish names the clips from this list):
   ```powershell
   python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-task <slug> anim-bundle --task-id <anim_task_id> --tool meshy_animate --task-type animation --credits <3 x actions> --status IN_PROGRESS --settings '{"action_ids": [0, 28], "clips": ["idle", "wave"]}' --output "work/<slug>/meshy/<slug>-anim-bundle.glb"
   ```
3. Poll with `meshy_get_task_status` (`task_id: "<anim_task_id>"`, `task_type: "animation"`, `wait: true`, `timeout_seconds: 150`).
4. Call `meshy_download_model` (`task_id: "<anim_task_id>"`, `task_type: "animation"`, `format: "glb"`) to retrieve the signed GLB URL, then download it using [`download-asset.py`](./scripts/download-asset.py):
   ```powershell
   python "<plugin_root>/skills/rig-animate/scripts/download-asset.py" "<animation_glb_url>" "work/<slug>/meshy/<slug>-anim-bundle.glb"
   ```
5. Update the task's status to `SUCCEEDED`.

A single replacement clip (a gate C re-animate fix) is still a single `meshy_animate` call with `action_id`, recorded under `anim-<clip_name>-<issue id>` and saved as `work/<slug>/meshy/<slug>-clip-<clip_name>.glb`; blender-finish merges it as a separate clip.

## Step 5: Custom Motion (optional; `meshy_text_to_motion` + `meshy_animate` — 13 or 6 credits per clip)

Only for a clip approved in Step 1 that no preset fits, and only on a biped rig. Run both calls back to back: Meshy keeps the motion for 3 days.

1. Check `pipeline_state.py get-task <slug> motion-<clip_name>`. If not yet created, call `meshy_text_to_motion`:
   ```json
   {
     "prompt": "<the motion, at most 400 characters>",
     "duration": 4,
     "mode": "prime"
   }
   ```
   *(`mode: "swift"` costs 3 credits instead of 10; use the mode the user approved.)*
2. Record it immediately:
   ```powershell
   python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-task <slug> motion-<clip_name> --task-id <motion_task_id> --tool meshy_text_to_motion --task-type text-to-motion --credits <10 or 3> --status IN_PROGRESS --settings '{"mode": "prime", "duration": 4}'
   ```
3. Poll with `meshy_get_task_status` (`task_id: "<motion_task_id>"`, `task_type: "text-to-motion"`, `wait: true`, `timeout_seconds: 150`) until `SUCCEEDED`, and set its status.
4. Check `get-task <slug> anim-<clip_name>`. If not yet created, call `meshy_animate` with `{ "rig_task_id": "<rig_task_id>", "motion_task_id": "<motion_task_id>" }` and record it under `anim-<clip_name>` (`--tool meshy_animate --task-type animation --credits 3 --output "work/<slug>/meshy/<slug>-clip-<clip_name>.glb"`). If the motion task was recorded more than 3 days ago, it has expired: stop and report it, because a new motion needs a new approval.
5. Poll, download with `meshy_download_model` (`task_type: "animation"`) and `download-asset.py` into `work/<slug>/meshy/<slug>-clip-<clip_name>.glb`, as in Step 4, and set the status to `SUCCEEDED`.

When Steps 4 and 5 are done, advance the stage to `blender-finish`.

> **Critic loop:** Stage 3 has no gate of its own. Its rig and clips are judged at gate C (`../idea-to-3d/references/loop.md`) once Blender renders them; re-rig and re-animate fixes come back from there as paid requests.
