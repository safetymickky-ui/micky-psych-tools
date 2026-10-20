---
name: image-to-3d
description: Generate textured 3D models (.glb) from turnaround or front concept images using Meshy (meshy_multi_image_to_3d or meshy_image_to_3d), render a side-by-side comparison sheet in headless Blender, and present Checkpoint B. Trigger when turning an image into a 3D model or running Stage 2 of /idea-to-3d.
---

# Stage 2: Image to 3D (`image-to-3d`)

`<plugin_root>` is this plugin's directory: two levels above this skill's base directory. Use it as an absolute path in every command.

Generates textured 3D model tries from Stage 1's images using the Meshy MCP server, renders them side by side with headless Blender 5.2, and stops at **Checkpoint B** for the user to choose the best try.

## Step 1: Pre-Flight Check (`pipeline.json`, Upload Consent & Credit Confirmation)

1. **Read `work/<slug>/pipeline.json` first:**
   ```powershell
   python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" show <slug>
   ```
   - If `try-1` or `try-2` is already recorded in `pipeline.json`, **never call the create tool again** — poll the existing `task_id` with `meshy_get_task_status` instead.
2. **Ask for upload consent & credit approval before calling Meshy:**
   - Tell the user:
     - **Upload notice:** `work/<slug>/images/front.png` (and `side.png`, `back.png`) will be uploaded to Meshy (`meshy.ai`).
     - **Tool & settings:**
       - `meshy_multi_image_to_3d` (when `front.png`, `side.png`, and `back.png` exist) or `meshy_image_to_3d` (from `front.png` only).
       - `ai_model`: `"meshy-7.1"` (or `"meshy-6-lite"` for a 15-credit tracer bullet run).
       - `should_texture`: `true`, `enable_pbr`: `true`, `texture_resolution`: `"4k"` (2K on `meshy-6-lite`), `image_enhancement`: `true`.
       - For humanoids that will be rigged: `pose_mode`: `"a-pose"` (or `"t-pose"`).
       - Ask explicitly before enabling Ultra geometry (`geometry_resolution: "2k"` or `"4k"`, +5 credits) or `"8k"` textures (+5 credits).
     - **Credits:** **30 credits per try** (2 tries = **60 credits** total; or 15 credits for 1 `meshy-6-lite` try).
   - **Wait for the user's explicit yes.**

## Step 2: Create, Record, Poll, and Download Tries

For each try ($n = 1, 2$):

1. Call `meshy_multi_image_to_3d` with:
   ```json
   {
     "file_paths": [
       "<abs_path>/work/<slug>/images/front.png",
       "<abs_path>/work/<slug>/images/side.png",
       "<abs_path>/work/<slug>/images/back.png"
     ],
     "ai_model": "meshy-7.1",
     "should_texture": true,
     "enable_pbr": true,
     "texture_resolution": "4k",
     "image_enhancement": true,
     "target_formats": ["glb"]
   }
   ```
   *(Or `meshy_image_to_3d` with `file_path: "<abs_path>/work/<slug>/images/front.png"` if single-view.)*
   > [!IMPORTANT]
   > - Always pass **`file_paths`** (for `meshy_multi_image_to_3d`) or **`file_path`** (for `meshy_image_to_3d`) when using local files — never `image_urls` or `image_paths`.
   > - For humanoids, pass `pose_mode: "t-pose"` or `"a-pose"`. For non-humanoids, omit `pose_mode` or pass `""` — never `"none"`.
2. **Immediately record the returned `task_id`** in `work/<slug>/pipeline.json`:
   ```powershell
   python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-task <slug> try-<n> --task-id <task_id> --tool meshy_multi_image_to_3d --task-type multi-image-to-3d --credits 30 --status IN_PROGRESS --output "work/<slug>/meshy/<slug>-try-<n>.glb"
   ```
   - If the create call times out or errors, check `meshy_list_tasks` before retrying so a created task is never billed twice.
3. Poll with `meshy_get_task_status` (`task_id`, `task_type: "multi-image-to-3d"`, `wait: true`, `timeout_seconds: 150` — safely below the 3m0s MCP client deadline). If outcome is `TIMEOUT` or `context deadline exceeded`, call `meshy_get_task_status` again with the **same** `task_id`.
4. Download the finished textured GLB with `meshy_download_model` (always use **`save_to`**, never `output_path`):
   ```json
   {
     "task_id": "<task_id>",
     "task_type": "multi-image-to-3d",
     "format": "glb",
     "save_to": "<abs_path>/work/<slug>/meshy/<slug>-try-<n>.glb"
   }
   ```
5. Update the task status to `SUCCEEDED` in `pipeline.json`.

## Step 3: Render Side-by-Side Comparison (`work/<slug>/preview/tries.png`)

Run headless Blender 5.2 with [`render-meshy.py`](./scripts/render-meshy.py) to render `front`, `three-quarter`, `side`, and `face` close-up views at identical height and framing:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python-exit-code 1 -P "<plugin_root>/skills/image-to-3d/scripts/render-meshy.py" -- "work/<slug>/preview/tries.png" "work/<slug>/images/front.png" "work/<slug>/meshy/<slug>-try-1.glb=Try 1 (Meshy 7.1 4K)" "work/<slug>/meshy/<slug>-try-2.glb=Try 2 (Meshy 7.1 4K)"
```

## Step 4: Checkpoint B (MUST Call `AskUserQuestion` and Wait for User)

1. Call `Read` on `work/<slug>/preview/tries.png` to inspect both tries across all 4 angles.
2. Show the PNG to the user first (send it with the session's file-sending tool, e.g. `SendUserFile` with `display: "render"`, when one exists; otherwise give its absolute path) and put the absolute path in the question text.
3. Call the **`AskUserQuestion`** tool (recommended try first, its label ending with "(Recommended)"):
   - Note that Meshy's automatic UVs give the face a small share of the texture map, so judge geometry sharpness on the close-up column.
   - Include the Stage 3 credit approval in the options:
     - `meshy_remesh` (to 20k–30k quads): **5 credits**
     - `meshy_rig` (for humanoids, includes walk & run free): **5 credits**
     - `meshy_animate` (for humanoids, e.g. `idle` + actions): **3 credits per action**
     - Or **30 credits** if the user wants an additional `meshy-7.1` try.
4. Once approved, copy the chosen try to `work/<slug>/meshy/<slug>-meshy.glb` and record Checkpoint B:
   ```powershell
   Copy-Item -LiteralPath "work/<slug>/meshy/<slug>-try-<n>.glb" -Destination "work/<slug>/meshy/<slug>-meshy.glb" -Force
   python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-checkpoint <slug> B --approved true --choice <n>
   ```

