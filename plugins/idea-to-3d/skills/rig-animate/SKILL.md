---
name: rig-animate
description: Remesh a 3D model to animation-ready quad topology (20,000-30,000 faces), auto-rig humanoids, and generate animation clips (idle, walk, actions) using Meshy MCP tools (meshy_remesh, meshy_rig, meshy_list_animations, meshy_animate). Trigger when remeshing, rigging, or animating a 3D model in Meshy or running Stage 3 of /idea-to-3d.
---

# Stage 3: Remesh, Rig, and Animate (`rig-animate`)

`<plugin_root>` is this plugin's directory: two levels above this skill's base directory. Use it as an absolute path in every command.

Converts the raw ~300,000-face image-to-3D mesh into an animation-friendly quad mesh (20,000–30,000 faces), and for humanoid characters auto-rigs and generates animation clips in Meshy. For non-humanoid characters (such as round hovering robots or creatures Meshy cannot auto-rig), remeshes the model and hands off to Stage 4 (`blender-finish`) to rig and animate by script in headless Blender.

## Step 1: Select Animations & Confirm Cost

1. **Read `work/<slug>/pipeline.json` first:**
   ```powershell
   python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" show <slug>
   ```
   - Never re-create any task (`remesh`, `rig`, `anim-<name>`) already recorded in `pipeline.json`.
2. **If humanoid (`is_humanoid: true`), look up preset animation IDs (free):**
   - Call `meshy_list_animations` with `search: "idle"`, `category: "DailyActions"`, or `category: "BodyMovements"` (free).
   - Pick an `idle` clip plus 2 or 3 actions that fit `work/<slug>/idea.md` (note: `meshy_rig` already includes `walk` and `run` for free!).
3. **Ask the user to confirm credits before calling paid tools:**
   - `meshy_remesh`: **5 credits** (`topology: "quad"`, `target_polycount: 25000`).
   - If humanoid:
     - `meshy_rig`: **5 credits** (includes free walking and running GLBs).
     - `meshy_animate`: **3 credits per action** (list the exact action names and IDs).
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

## Step 4: Animate Actions (`meshy_animate` — 3 credits each)

For each chosen preset action (e.g., `idle` [`action_id: 0`], `wave` [`action_id: 28` = `Big Wave Hello`]):

1. Call `meshy_animate` (pass **only** `rig_task_id` and `action_id` — **never** pass `fps`, which is rejected by the MCP schema):
   ```json
   {
     "rig_task_id": "<rig_task_id>",
     "action_id": 0
   }
   ```
2. Record the `task_id` immediately under `anim-<clip_name>`:
   ```powershell
   python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-task <slug> anim-<clip_name> --task-id <anim_task_id> --tool meshy_animate --task-type animation --credits 3 --status IN_PROGRESS --output "work/<slug>/meshy/<slug>-clip-<clip_name>.glb"
   ```
3. Poll with `meshy_get_task_status` (`task_id: "<anim_task_id>"`, `task_type: "animation"`, `wait: true`, `timeout_seconds: 150`).
4. Call `meshy_download_model` (`task_id: "<anim_task_id>"`, `task_type: "animation"`, `format: "glb"`) to retrieve the signed `Animation_*_withSkin.glb` URL, then download it using [`download-asset.py`](./scripts/download-asset.py):
   ```powershell
   python "<plugin_root>/skills/rig-animate/scripts/download-asset.py" "<animation_glb_url>" "work/<slug>/meshy/<slug>-clip-<clip_name>.glb"
   ```
5. Update each task's status to `SUCCEEDED` and advance stage to `blender-finish`.

