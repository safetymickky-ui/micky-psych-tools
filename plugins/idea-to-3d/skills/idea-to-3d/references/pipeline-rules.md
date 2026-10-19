---
trigger: model_decision
description: Credit confirmation, task idempotency, checkpoint gating, external upload consent, and headless Blender discipline for /idea-to-3d and 3D character generation.
---

# Idea-to-3D Pipeline Rules

These rules apply whenever running `/idea-to-3d` or any of its stage skills (`concept-art`, `image-to-3d`, `rig-animate`, `blender-finish`).

## 1. Credits & Meshy API Safety

- **Always ask before spending credits.** Before calling any Meshy tool that costs credits, tell the user the **exact tool name**, **AI model**, and **credit cost**, and wait for an explicit **yes**.
- **Free calls require no confirmation:** `meshy_get_task_status`, `meshy_list_tasks`, `meshy_list_models`, `meshy_download_model`, `meshy_check_balance`, and `meshy_list_animations` are free and may be called directly.
- **Reference Credit Pricing (check Meshy MCP tool descriptions and https://docs.meshy.ai/en/api/pricing):**
  - `meshy_image_to_3d` / `meshy_multi_image_to_3d` with `meshy-7.1` (2K or 4K texture): **30 credits** (`meshy-6-lite`: **15 credits**; 8K texture: **+5 credits**; Ultra geometry `2k`/`4k`: **+5 credits**).
  - `meshy_remesh`: **5 credits**.
  - `meshy_rig`: **5 credits** (includes walking and running animations free).
  - `meshy_animate`: **3 credits** per action.
  - `meshy_text_to_image` / `meshy_image_to_image` with `nano-banana-pro`: **9 credits** each.
  - A full standard run with 2 tries and 3 clips costs approximately **80 credits**.
- **Never double-charge on timeouts or errors:**
  - Record every Meshy `task_id` in `work/<slug>/pipeline.json` the moment it is created.
  - Before any Meshy create call, read `work/<slug>/pipeline.json`: if a task is already recorded for that step, poll it with `meshy_get_task_status` — **never create it again**.
  - If a create call times out or errors, the task may still exist and be charged on Meshy: check `meshy_list_tasks` and `work/<slug>/pipeline.json` before calling the create tool again.
  - A `meshy_get_task_status` wait that returns `TIMEOUT` leaves the task running on Meshy; poll the **same** `task_id` again.
- **Secret hygiene:** Never write `MESHY_API_KEY` into any file, script, log, or chat reply.

## 2. Checkpoints, Interactive `ask_question` Tool & External Uploads

- **Always use the `ask_question` tool for every checkpoint and credit confirmation:**
  - Never stop with plain text alone when asking the user to pick a concept, pick a 3D try, approve credits/uploads, or approve the final GLB. Always invoke the `ask_question` modal tool with the recommended option listed first (`(Recommended) ...`).
  - Combine the checkpoint choice and the next stage's credit/upload confirmation into the `ask_question` options so the user can approve both in a single click.
- **Stop at every checkpoint until the user answers:**
  - **Checkpoint A (after concept images):** View `work/<slug>/preview/concepts.png` with `view_file`, then call `ask_question` presenting `concepts.png`, stating whether a scripted/procedural Blender build is recommended, stating the Stage 2 upload notice & credit cost (`2 × meshy-7.1` 4K = 60 credits, or 15 credits for 1 `meshy-6-lite` tracer try), and waiting for the user's pick.
  - **Checkpoint B (after image-to-3D tries):** View `work/<slug>/preview/tries.png` with `view_file`, then call `ask_question` presenting `tries.png` (front, three-quarter, side, and face close-up), stating the exact Stage 3 credit cost (`meshy_remesh` 5 cr + `meshy_rig` 5 cr + `meshy_animate` 3 cr/action, or 5 cr remesh-only for non-humanoids), and waiting for the user's pick.
  - **Checkpoint C (after Blender finish & validation):** View `work/<slug>/preview/sheet.png` with `view_file`, then call `ask_question` presenting `sheet.png` (Concept column + 4 views × 3 frames per clip) and the passing `check-glb.py` report, and waiting for the user's approval.
- **Record every checkpoint decision in `work/<slug>/pipeline.json`.**
- **External upload consent:** Uploading an image to Meshy sends it to an external service (`meshy.ai`). Before the **first upload of each idea**, inform the user that the image will be uploaded to Meshy and get an explicit **yes** via `ask_question`. Images of real people require explicit permission.

## 3. Meshy MCP Exact Parameter Schema & Polling Discipline

- **Exact Parameter Names (prevent `-32602` schema errors):**
  - `meshy_multi_image_to_3d`: pass local paths in **`file_paths`** (`[".../front.png", ".../side.png", ".../back.png"]`) — **never** `image_urls` (unless `https://` or data URI) and **never** `image_paths`.
  - `meshy_image_to_3d`: pass local path in **`file_path`** (`".../front.png"`).
  - `pose_mode` (`meshy_image_to_3d` / `meshy_multi_image_to_3d`): only **`"a-pose"`**, **`"t-pose"`**, or **`""`** are valid — **never** `"none"`.
  - `meshy_download_model`: pass destination path in **`save_to`** — **never** `output_path`. Note: for `task_type: "rigging"` and `task_type: "animation"`, `meshy_download_model` returns signed cloud URLs in its text output rather than writing directly to disk; download those `.glb` URLs using `skills/rig-animate/scripts/download-asset.py`.
  - `meshy_animate`: pass `{ "rig_task_id": "<id>", "action_id": <int> }` — **never** pass `fps` (unsupported key) and **never** guess `action_id` (always query `meshy_list_animations` first, which is free; `Idle` is `action_id: 0`, `Big Wave Hello` is `action_id: 28`).
- **Polling Timeout (`timeout_seconds: 150`):**
  - When calling `meshy_get_task_status` with `wait: true`, set `timeout_seconds: 150` (safely below the 3m0s MCP client hard deadline). If a poll times out (`TIMEOUT` or `context deadline exceeded`), call `meshy_get_task_status` again with the **exact same `task_id`** — never re-create the task.

## 4. Headless Blender & glTF Export Discipline

- **Always run Blender headless with `--python-exit-code 1`:**
  `"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python-exit-code 1 -P <script.py> -- <args>`
- **Never clear an open live Blender session:** Start headless scripts with `bpy.ops.wm.read_factory_settings(use_empty=True)`. Leave any open GUI Blender session untouched.
- **Atomic export & validation:** Always export to `work/<slug>/out/<slug>.tmp.glb`, run `check-glb.py`, and replace `work/<slug>/out/<slug>.glb` only when every check passes.
- **Clips move bones only:** Delete any stray/fake-user actions not named in the pipeline's clip list. Animation clips must only target skin joints (never shape key weights or non-bone nodes).

## 5. Git & Plugin Sync Hygiene

- **In the `idea-to-3d` plugin repository:** Commit only the plugin files, **never `work/`** or `meshy_output/`.
- **Updating the installed plugin on Windows:** When `idea-to-3d_meshy` is running in an active session, `agy plugin install --force` can fail mid-copy due to Windows file locks on `run-meshy-mcp.ps1`. Run `powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\User\Desktop\repo\idea-to-3d\scripts\sync-plugin.ps1"` to sync, validate, and enable the plugin safely.
- **In user projects tracking 3D assets in Git:** Track `.blend` and the chosen `<slug>-meshy.glb` in Git LFS; ignore raw tries (`*-try-*`) and Blender backups (`*.blend1`). Commit `.blend` files only at the end of a stage.


## 6. Claude Code Adaptation

These skills were first written for Antigravity. When running them in Claude Code:

- **`<plugin_root>`** = this plugin's install directory (two levels above any skill folder, `${CLAUDE_PLUGIN_ROOT}`). Scripts live at `<plugin_root>/skills/<skill>/scripts/`.
- **`ask_question`** → `AskUserQuestion` (recommended option first, label ending "(Recommended)").
- **`view_file`** → `Read` on the PNG.
- **`image-generator` subagent / `generate_image`** and the Antigravity `save-image.ps1` PostToolUse hook do not exist in Claude Code. Use the documented fallback — `meshy_text_to_image` / `meshy_image_to_image` (`nano-banana-pro`, 9 credits per image) after explicit approval, downloaded into `work/<slug>/images/` under the expected filenames — or ask the user for concept images.
- **Meshy MCP** ships in this plugin's `.mcp.json` (`scripts/run-meshy-mcp.mjs`), which reads `MESHY_API_KEY` from the environment or `HKCU\Environment` at launch. Check the live tool names and schemas before the first call; they can differ by server version.
- **§5 Plugin Sync** (`agy`, `sync-plugin.ps1`) is Antigravity-only; update this plugin through the marketplace instead.
