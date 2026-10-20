---
name: blender-finish
description: Stage 4 sub-skill for the idea-to-3d pipeline. Runs headless Blender 5.2 to clean topology, normalize scale and grounding (Z=0 in Blender, Y=0 in glTF), merge Meshy or procedural animation clips onto a single armature, atomically export and verify work/<slug>/out/<slug>.glb against the quality gates, and render work/<slug>/preview/sheet.png for Checkpoint C.
---

# Stage 4: Headless Blender 5.2 Clean-up, Merge & Contact Sheet (`blender-finish`)

`<plugin_root>` is this plugin's directory: two levels above this skill's base directory. Use it as an absolute path in every command.

Use this skill for **Stage 4** of the `/idea-to-3d` pipeline (after Stage 3 completes or when using `--procedural-rig` / `--scripted-robot` fallback).

## 1. Blender Executable & Invocation Rules

Always run Blender 5.2 headless with `--factory-startup` and `--python-exit-code 1` so any open GUI Blender session is untouched and Python errors fail loudly:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python-exit-code 1 -P <script.py> -- <args>
```
**Never use `&&` in PowerShell.**

## 2. Step-by-Step Workflow

### Step 1: Import, Clean, Merge Clips & Save `.blend` (`import-merge.py`)

#### Mode A: Merge Meshy Rigged + Animated GLBs (Standard Humanoid Flow)
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python-exit-code 1 -P "<plugin_root>/skills/blender-finish/scripts/import-merge.py" -- --out "work/<slug>/blender/<slug>.blend" --rigged "work/<slug>/meshy/<slug>-rigged.glb" --clip "idle=work/<slug>/meshy/<slug>-clip-idle.glb" --clip "walk=work/<slug>/meshy/<slug>-clip-walk.glb" --clip "wave=work/<slug>/meshy/<slug>-clip-wave.glb" --height 1.7 --max-triangles 40000
```

#### Mode B: Procedural Rig & Keyframed Clips Fallback (Non-Humanoid / Auto-Rig Failure)
If the character is non-humanoid (or `meshy_rig` failed), pass the remeshed mesh (`--mesh`) and `--procedural-rig`. Set `--clips` to `expected_clips` from `pipeline.json`, comma-joined. A non-humanoid defaults to `idle` alone, because the procedural `wave` bends rigid props out of shape:
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python-exit-code 1 -P "<plugin_root>/skills/blender-finish/scripts/import-merge.py" -- --out "work/<slug>/blender/<slug>.blend" --mesh "work/<slug>/meshy/<slug>-remesh.glb" --procedural-rig --clips "idle" --height 1.7 --max-triangles 40000
```

#### Mode C: Pure Scripted Robot Character + Rig (`--scripted-robot`)
For symmetric hard-surface spherical robots (or zero-credit verification):
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python-exit-code 1 -P "<plugin_root>/skills/blender-finish/scripts/import-merge.py" -- --out "work/<slug>/blender/<slug>.blend" --scripted-robot --clips "idle,wave" --height 0.35 --max-triangles 40000
```

---

### Step 2: Atomic Export & Quality Verification (`export-check.py` & `check-glb.py`)

Run `export-check.py` inside headless Blender 5.2. It opens `work/<slug>/blender/<slug>.blend`, verifies materials/UVs/bone motion, exports to `work/<slug>/out/<slug>.tmp.glb` with WebP textures and Action clips, runs `check-glb.py`, and atomically replaces `work/<slug>/out/<slug>.glb` only when every check passes:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python-exit-code 1 -P "<plugin_root>/skills/blender-finish/scripts/export-check.py" -- --blend "work/<slug>/blender/<slug>.blend" --out "work/<slug>/out/<slug>.glb" --report "work/<slug>/out/quality_report.json"
```

#### Quality Gates Enforced:
1. File size `<= 8 MB` (or `max_bytes` in `pipeline.json`).
2. Triangle count `<= triangle_budget` in `pipeline.json` (default `40,000`).
3. Rigged with a skeleton skin (`skins` and `joints` present).
4. Expected animation clips exist (`idle` plus at least 1 action clip), spelled exactly with no `.001` duplicate suffixes. When `expected_clips` in `pipeline.json` (or `--clips`) names one clip, as a non-humanoid's `["idle"]` does, that one clip passes without `--allow-single-clip`.
5. Every animation channel targets only skin joints (never morph target weights or non-joint nodes) and moves bones across its frame range.
6. Every mesh has `UVMap` and a `Principled BSDF` material (`mean RGB > 0.02`, not solid black), and all embedded GLB textures are `image/webp` or `image/png`.
7. No cameras or punctual lights (`KHR_lights_punctual`) in the exported `.glb`.
8. Grounded at origin (`min Y ~ 0` in glTF `+Y` up) and height matches `idea.md` / `pipeline.json`.

---

### Step 3: Render Checkpoint C Contact Sheet (`render-sheet.py`)

Render the 4 views (`Front`, `3/4`, `Side`, `Back`) × 3 frames (`start`, `mid`, `end`) contact sheet across all clips into `work/<slug>/preview/sheet.png`:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python-exit-code 1 -P "<plugin_root>/skills/blender-finish/scripts/render-sheet.py" -- --blend "work/<slug>/blender/<slug>.blend" --out "work/<slug>/preview/sheet.png" --concept "work/<slug>/images/front.png"
```

---

### Optional: Run Steps 1–3 as One Actionforge Graph (`stage4-animate.act`)

[`stage4-animate.act`](./scripts/stage4-animate.act) is an Actionforge graph that chains Steps 1–3: `import-merge` → `export-check` → `render-sheet`. If any Blender step exits non-zero, the graph prints the failure and exits 1. Steps 1–3 above stay the reference behaviour. Use the graph for repeatable re-runs (for example, re-merging after swapping a clip). You can also open it in the Actionforge editor to see the pipeline, or step through it.

- **Env:** `IDEA3D_SLUG` (required), `IDEA3D_PLUGIN_ROOT` = `<plugin_root>` (required), `IDEA3D_BLENDER` (optional; defaults to the Blender 5.2 path above).
- **Args after `--`:** the Step 1 mode args (Mode A, B or C) without `--out`. The graph builds `--out`, and every Step 2–3 path, from the slug.
- **Run** from the workspace that holds `work/<slug>/`. This needs the `actrun` CLI on PATH (see the README):
  ```powershell
  $env:IDEA3D_SLUG = "<slug>"; $env:IDEA3D_PLUGIN_ROOT = "<plugin_root>"
  actrun "<plugin_root>/skills/blender-finish/scripts/stage4-animate.act" -- --scripted-robot --clips "idle,wave" --height 0.35 --max-triangles 40000
  ```
- **Editing the graph:** use the bundled `actionforge-app` MCP. Call `search_nodes` / `describe_node` to find nodes. Then call `validate_graph` on the full YAML before saving: it must return `Graph is valid.` `.act` files are YAML, and the schema rejects unknown top-level keys, so keep notes in `#` comments. When you modify an existing `.act`, follow the server's lock protocol: put `locked_by: claude` on the first line while editing, and remove it once the graph validates.

> **Critic loop:** under the orchestrator, gate C (`../idea-to-3d/references/loop.md`) runs before this checkpoint; it also judges Stage 3's rig and clips. A maker subagent stops here.

### Step 4: Inspection Gate & Checkpoint C (MUST Call `AskUserQuestion`)

1. Call `Read` on `work/<slug>/preview/sheet.png` to visually inspect the dedicated left `Concept` column and all 4 views × 3 frames per clip (verifying zero mesh tearing on procedural rigs and clear limb motion on humanoid rigs).
2. Show the PNG to the user first (send it with the session's file-sending tool, e.g. `SendUserFile` with `display: "render"`, when one exists; otherwise give its absolute path) and put the absolute path in the question text.
3. Call the **`AskUserQuestion`** tool presenting `work/<slug>/preview/sheet.png`, `work/<slug>/out/<slug>.glb`, `work/<slug>/blender/<slug>.blend`, and the passing `export-check.py` / `check-glb.py` report, and wait for **Checkpoint C** approval.
4. Once approved, record Checkpoint C in `work/<slug>/pipeline.json`:
   ```powershell
   python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-checkpoint <slug> C --approved true --notes "Final GLB and preview sheet approved"
   ```

