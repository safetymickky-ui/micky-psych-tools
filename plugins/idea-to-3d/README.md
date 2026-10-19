# idea-to-3d

Turn a one-line character or prop idea into a clean, rigged, multi-clip `.glb` + `.blend` +
preview contact sheet.

```text
idea → Stage 1: concept images            → [Checkpoint A]
     → Stage 2: image-to-3D (Meshy)        → [Checkpoint B]
     → Stage 3: remesh, rig & clips (Meshy)
     → Stage 4: clean-up, merge, check & sheet (headless Blender) → [Checkpoint C]
```

## Install

```text
/plugin install idea-to-3d --marketplace safetymickky-ui/micky-psych-tools
```

## Skills

| skill | stage |
| --- | --- |
| `idea-to-3d` | orchestrator — `/idea-to-3d <idea>` runs all four stages |
| `concept-art` | 1 — character brief, 3–4 concepts, front/side/back turnaround |
| `image-to-3d` | 2 — Meshy multi-image-to-3D tries + comparison render |
| `rig-animate` | 3 — Meshy remesh, auto-rig, animation clips |
| `blender-finish` | 4 — Blender clean-up, clip merge, quality gates, contact sheet |

Every paid Meshy call is confirmed first (tool, model, credit cost), every task id is
recorded in `work/<slug>/pipeline.json` so a timeout never double-charges, and each
checkpoint waits for the user. Rules: `skills/idea-to-3d/references/pipeline-rules.md`.

## Requirements

- **Blender 5.2** at `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`
  (or `$env:BLENDER_EXE`).
- **Node.js 22+** and **Python 3.12+**.
- **`MESHY_API_KEY`** in your user environment — never in a file:
  ```powershell
  [Environment]::SetEnvironmentVariable("MESHY_API_KEY", "<your-meshy-api-key>", "User")
  ```
  The bundled `meshy` MCP server (`scripts/run-meshy-mcp.mjs`) reads it at launch.

## Actionforge (optional)

The plugin also bundles Actionforge's Graph Builder MCP (`actionforge-app`, HTTP, no auth).
It is used to edit and validate `skills/blender-finish/scripts/stage4-animate.act`. That graph
runs Stage 4's animation pipeline (clip merge → export + quality gates → contact sheet) as one
graph that stops on the first failing step. Running the graph needs the `actrun` CLI from
<https://www.actionforge.dev/download>. Check its SHA256 against that page before use. The
Windows zips served on 2026-10-20 did not match the published hashes and were not installed.
The skills work without it.

## Notes

- Built for Windows / PowerShell.
- No image-generation tool in Claude Code: Stage 1 uses Meshy `nano-banana-pro`
  (9 credits per image, approval first) or images you supply.
- A full standard run (2 tries, 3 clips) costs about 80 Meshy credits.
