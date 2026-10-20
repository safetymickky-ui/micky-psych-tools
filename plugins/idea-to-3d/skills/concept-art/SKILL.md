---
name: concept-art
description: Generate 3D character or prop concept art and Meshy-ready turnaround views (front, side, back) free through Antigravity (agy), or Meshy Nano Banana Pro as a paid fallback. Trigger when the user asks to make concept art for a 3D model, expand a character brief into turnaround sheets, or run Stage 1 of /idea-to-3d.
---

# Stage 1: Concept Images (`concept-art`)

`<plugin_root>` is this plugin's directory: two levels above this skill's base directory. Use it as an absolute path in every command.

Turns a one-line idea into an expanded character brief (`work/<slug>/idea.md`), 3–4 concept variations for **Checkpoint A**, and clean turnaround views (`front.png`, `side.png`, `back.png`) ready for Meshy.

## Step 1: Expand the Idea into `work/<slug>/idea.md`

Initialize `work/<slug>/pipeline.json` (if not already present) and write `work/<slug>/idea.md` containing:
- **Name & Slug:** Short kebab-case slug.
- **Silhouette & Proportions:** Overall shape, humanoid vs. non-humanoid, real-world height in meters (`Height: 1.65 m` or `Height: 0.15 m`).
- **Colour Palette:** Key colours with explicit hex codes (e.g., `#F5F5F7` pearl shell, `#4285F4` royal blue accents).
- **Materials:** Surface finishes (matte cloth, brushed metal, glossy ceramic, emissive cyan screen).
- **Mood & Personality:** 1–2 sentences describing attitude and rest expression.
- **Style:** `"polished 3D render, soft studio lighting, smooth rounded shapes, Pixar-like charm, clean silhouette"`.
- **Target Animation Clips:** `idle` plus 2–3 fitting actions (e.g., `walk`, `wave`, `cheer`); a rigid non-humanoid prop gets `idle` only.

> [!TIP]
> **Procedural Blender Option:** Round, hard-surface, symmetric characters (such as a hovering spherical robot lab assistant) often come out cleaner when built directly by Blender script than from image-to-3D. If the idea fits that shape, note it in `idea.md` and offer a pure scripted Blender build as an option at **Checkpoint A**.

## Step 2: Generate 3 or 4 Concept Candidates

1. **Image route (Claude Code), free first.** Run one call per concept (about 70–90 s each, 0 credits; Bash `timeout: 600000`). It runs only when the user agreed to Google (`pipeline_state.py set-critic <slug> gemini`); the prompt, built from `idea.md`, goes to Google. Write it to `work/<slug>/prompts/concept-<n>.txt` first (prompts hold quotes and backticks that break shell quoting), then:
   ```powershell
   python "<plugin_root>/skills/idea-to-3d/scripts/generate_image.py" <slug> --out images/concept-<n>.png --prompt-file "<abs path of work/<slug>/prompts/concept-<n>.txt>" --work-root <root>
   ```
   Exit 0 means the image is written; exit 2 means the route is unavailable.
2. **Paid fallback, only when `generate_image.py` exits 2 or the user declined Google:** Meshy `nano-banana-pro`, 9 credits per image. Get credit approval first: the orchestrator asks; when this skill runs on its own, ask with `AskUserQuestion`. Call `meshy_text_to_image` once per concept with `ai_model: "nano-banana-pro"`, `aspect_ratio: "1:1"` and the same prompt, and record each `task_id` with `pipeline_state.py record-task <slug> concept-<n> ...` the moment it is created. Poll each task with `meshy_get_task_status` (`wait: true`, `timeout_seconds: 150`) and download it with `meshy_download_model` (`save_to: "work/<slug>/images/concept-<n>.png"`). If a file is a JPEG, convert it to PNG with Pillow before building the sheet.
3. Build the comparison sheet `work/<slug>/preview/concepts.png` (supports `path=Label`, `Label=path`, or `--images` / `--labels`):
   ```powershell
   python "<plugin_root>/skills/concept-art/scripts/make-concept-sheet.py" --out "work/<slug>/preview/concepts.png" --title "<slug>: Concept Candidates (Checkpoint A)" "work/<slug>/images/concept-1.png=Concept 1" "work/<slug>/images/concept-2.png=Concept 2" "work/<slug>/images/concept-3.png=Concept 3"
   ```

> **Critic loop:** under the orchestrator, gate A1 (`../idea-to-3d/references/loop.md`) runs before this checkpoint and gate A2 runs after Step 4. A maker subagent stops here and hands back to the orchestrator.

## Step 3: Checkpoint A (MUST Call `AskUserQuestion` and Wait for User)

1. Call `Read` on `work/<slug>/preview/concepts.png` to inspect the candidates.
2. Show the PNG to the user first (send it with the session's file-sending tool, e.g. `SendUserFile` with `display: "render"`, when one exists; otherwise give its absolute path) and put the absolute path in the question text.
3. Call the **`AskUserQuestion`** tool (recommended concept first, its label ending with "(Recommended)") stating:
   - Which concept you recommend and why (plus the scripted Blender option if hard-surface/symmetric).
   - What it costs to continue (combine the concept choice and Stage 2 credit/upload approval in the options; under the orchestrator these are two questions in one call, see its Checkpoint A step):
     - Turnaround generation (`front.png`, `side.png`, `back.png`): **0 credits** on the free route (`generate_image.py`), **27 credits** (3 × 9) on the Meshy route (`meshy_image_to_image`, `nano-banana-pro`).
     - Uploading turnaround images to `meshy.ai` for Stage 2 Image-to-3D: **60 credits** for 2 tries with `meshy-7.1` at 4K texture (30 credits each), or **15 credits** for a single `meshy-6-lite` tracer try.
4. Record the decision with `pipeline_state.py record-checkpoint <slug> A --approved true --choice concept-<n>`.


## Step 4: Generate Meshy Turnaround Views (`front.png`, `side.png`, `back.png`)

From the user's chosen concept (`work/<slug>/images/concept-<n>.png`), generate each view with the free route first, passing the concept as `--ref` so the character stays identical across views (Bash `timeout: 600000`). Write each view's prompt (the framing rules below + the view) to `work/<slug>/prompts/<view>.txt` first, then:

```powershell
python "<plugin_root>/skills/idea-to-3d/scripts/generate_image.py" <slug> --out images/front.png --prompt-file "<abs path of work/<slug>/prompts/front.txt>" --ref "<abs path of work/<slug>/images/concept-<n>.png>" --work-root <root>
```

Only when `generate_image.py` exits 2 or the user declined Google, use Meshy instead: `meshy_image_to_image` with the concept path in `reference_file_paths` (`ai_model: "nano-banana-pro"`, `aspect_ratio: "1:1"`, 9 credits per view, approval first; record each task with `pipeline_state.py record-task <slug> view-<front|side|back> ...` the moment it is created; download each result with `meshy_download_model` and `save_to`). The framing rules below go into the prompt text on either route.

`front.png` is regenerated (not just copied) so it meets the framing rules; on either route, if the chosen concept already meets them, copy it to `front.png` instead and skip that image (saves one image generation).

1. **`front.png` (saved as `work/<slug>/images/front.png`):**
   - **Strict Meshy prompt rules:**
     - **Exactly ONE view per image** (never a multi-panel grid — multi-panel sheets produce muddled meshes).
     - Full body (or head-and-shoulders if a bust), centered in frame with margin around it, nothing cut off, nothing occluding it in front.
     - Plain solid light grey background (`#D8D8DC`), soft even studio lighting, **no cast shadows on the ground or background**.
     - Square `1:1`, at least `1024x1024` px.
     - **Humanoids:** Stand in a clean **A-pose** (or T-pose) with arms held away from the torso and fingers separated so `meshy_rig` can auto-rig cleanly.
2. **`side.png` (saved as `images/side.png`) and `back.png` (saved as `images/back.png`):**
   - Pass both the chosen concept and `work/<slug>/images/front.png` as `--ref` (free route) or in `reference_file_paths` (Meshy route).
   - Same exact character, proportions, colours, lighting, plain light grey background, and scale:
     - `side.png`: Orthogonal 90° profile view, full body centered.
     - `back.png`: Orthogonal 180° rear view, full body centered.
3. Normalize and verify all three images and render `work/<slug>/preview/turnaround.png`:
   ```powershell
   python "<plugin_root>/skills/concept-art/scripts/make-concept-sheet.py" --normalize --out "work/<slug>/preview/turnaround.png" --title "<slug>: Meshy Turnaround Inputs" "work/<slug>/images/front.png=Front (1024px)" "work/<slug>/images/side.png=Side (1024px)" "work/<slug>/images/back.png=Back (1024px)"
   ```

Stage 1 is complete when `work/<slug>/images/front.png`, `side.png`, and `back.png` exist, match the chosen concept, and each holds a single clean view at $\ge 1024\text{ px}$.
