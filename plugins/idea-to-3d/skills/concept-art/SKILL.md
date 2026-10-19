---
name: concept-art
description: Generate 3D character or prop concept art and Meshy-ready turnaround views (front, side, back) using Nano Banana Pro. Trigger when the user asks to make concept art for a 3D model, expand a character brief into turnaround sheets, or run Stage 1 of /idea-to-3d.
---

# Stage 1: Concept Images (`concept-art`)

Turns a one-line idea into an expanded character brief (`work/<slug>/idea.md`), 3–4 concept variations for **Checkpoint A**, and clean turnaround views (`front.png`, `side.png`, `back.png`) ready for Meshy.

## Step 1: Expand the Idea into `work/<slug>/idea.md`

Initialize `work/<slug>/pipeline.json` (if not already present) and write `work/<slug>/idea.md` containing:
- **Name & Slug:** Short kebab-case slug.
- **Silhouette & Proportions:** Overall shape, humanoid vs. non-humanoid, real-world height in meters (`Height: 1.65 m` or `Height: 0.15 m`).
- **Colour Palette:** Key colours with explicit hex codes (e.g., `#F5F5F7` pearl shell, `#4285F4` royal blue accents).
- **Materials:** Surface finishes (matte cloth, brushed metal, glossy ceramic, emissive cyan screen).
- **Mood & Personality:** 1–2 sentences describing attitude and rest expression.
- **Style:** `"polished 3D render, soft studio lighting, smooth rounded shapes, Pixar-like charm, clean silhouette"`.
- **Target Animation Clips:** `idle` plus 2–3 fitting actions (e.g., `walk`, `wave`, `cheer`).

> [!TIP]
> **Procedural Blender Option:** Round, hard-surface, symmetric characters (such as a hovering spherical robot lab assistant) often come out cleaner when built directly by Blender script than from image-to-3D. If the idea fits that shape, note it in `idea.md` and offer a pure scripted Blender build as an option at **Checkpoint A**.

## Step 2: Generate 3 or 4 Concept Candidates

1. **Primary path (Antigravity `image-generator` subagent / `generate_image` — 0 Meshy credits):**
   - Invoke the `image-generator` subagent (or reuse an active `image-generator` subagent conversation via `send_message`) to produce 3–4 distinct concept variations:
     - `ImageName`: `<slug>_concept_1`, `<slug>_concept_2`, `<slug>_concept_3` (and optionally `<slug>_concept_4`)
     - `AspectRatio`: `"1:1"`
   - Note: `generate_image` normalizes hyphens in `ImageName` to underscores on disk (`<slug_with_underscores>_concept_1_<epoch>.jpg`). The `PostToolUse` hook (`scripts/save-image.ps1`) matches both forms and converts each image into `work/<slug>/images/concept-1.png` .. `concept-4.png`.
2. **Fallback path (if `generate_image` / `image-generator` is unavailable):**
   - Ask the user for approval first via `ask_question` (**9 credits per image**), then call `meshy_text_to_image` with `ai_model: "nano-banana-pro"` and `aspect_ratio: "1:1"`, and download via `meshy_download_model` into `work/<slug>/images/`.
3. Build the comparison sheet `work/<slug>/preview/concepts.png` (supports `path=Label`, `Label=path`, or `--images` / `--labels`):
   ```powershell
   python "<plugin_root>/skills/concept-art/scripts/make-concept-sheet.py" --out "work/<slug>/preview/concepts.png" --title "<slug>: Concept Candidates (Checkpoint A)" "work/<slug>/images/concept-1.png=Concept 1" "work/<slug>/images/concept-2.png=Concept 2" "work/<slug>/images/concept-3.png=Concept 3"
   ```

## Step 3: Checkpoint A (MUST Call `ask_question` and Wait for User)

1. Call `view_file` on `work/<slug>/preview/concepts.png` to inspect the candidates.
2. Call the **`ask_question`** tool (with your recommended concept first, prefixed with `(Recommended)`) stating:
   - Which concept you recommend and why (plus the scripted Blender option if hard-surface/symmetric).
   - What it costs to continue (combine the concept choice and Stage 2 credit/upload approval in the options):
     - Turnaround generation (`front.png`, `side.png`, `back.png`) via Nano Banana `image-generator`: **0 Meshy credits**.
     - Uploading turnaround images to `meshy.ai` for Stage 2 Image-to-3D: **60 credits** for 2 tries with `meshy-7.1` at 4K texture (30 credits each), or **15 credits** for a single `meshy-6-lite` tracer try.
3. Record the decision with `pipeline_state.py record-checkpoint <slug> A --approved true --choice concept-<n>`.


## Step 4: Generate Meshy Turnaround Views (`front.png`, `side.png`, `back.png`)

From the user's chosen concept (`work/<slug>/images/concept-<n>.png`), pass that file path in `ImagePaths` (or `reference_file_paths` in `meshy_image_to_image`) so the character stays identical across views:

1. **`front.png` (`ImageName`: `<slug>_front`):**
   - **Strict Meshy prompt rules (§4 Stage 1 & §7.1):**
     - **Exactly ONE view per image** (never a multi-panel grid — multi-panel sheets produce muddled meshes).
     - Full body (or head-and-shoulders if a bust), centered in frame with margin around it, nothing cut off, nothing occluding it in front.
     - Plain solid light grey background (`#D8D8DC`), soft even studio lighting, **no cast shadows on the ground or background**.
     - Square `1:1`, at least `1024x1024` px.
     - **Humanoids:** Stand in a clean **A-pose** (or T-pose) with arms held away from the torso and fingers separated so `meshy_rig` can auto-rig cleanly.
2. **`side.png` (`ImageName`: `<slug>_side`) and `back.png` (`ImageName`: `<slug>_back`):**
   - Pass both the chosen concept and `work/<slug>/images/front.png` in `ImagePaths`.
   - Same exact character, proportions, colours, lighting, plain light grey background, and scale:
     - `side.png`: Orthogonal 90° profile view, full body centered.
     - `back.png`: Orthogonal 180° rear view, full body centered.
3. Normalize and verify all three images and render `work/<slug>/preview/turnaround.png`:
   ```powershell
   python "<plugin_root>/skills/concept-art/scripts/make-concept-sheet.py" --normalize --out "work/<slug>/preview/turnaround.png" --title "<slug>: Meshy Turnaround Inputs" "work/<slug>/images/front.png=Front (1024px)" "work/<slug>/images/side.png=Side (1024px)" "work/<slug>/images/back.png=Back (1024px)"
   ```

Stage 1 is complete when `work/<slug>/images/front.png`, `side.png`, and `back.png` exist, match the chosen concept, and each holds a single clean view at $\ge 1024\text{ px}$.
