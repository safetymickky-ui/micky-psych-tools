# idea-to-3d

Turn a one-line character or prop idea into a clean, rigged, multi-clip `.glb` + `.blend` +
preview contact sheet. Every stage is reviewed by an independent critic and revised before
you see it.

```text
idea → Stage 1: concept images            ─ A1 ─ [Checkpoint A]
     → turnarounds                         ─ A2
     → Stage 2: image-to-3D (Meshy)        ─ B  ─ [Checkpoint B]
     → Stage 3: remesh, rig & clips (Meshy)
     → Stage 4: clean-up, merge, check & sheet (headless Blender) ─ C ─ [Checkpoint C]
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

## The critic loop

| Role | What it does | Spends credits |
| --- | --- | --- |
| maker (`idea3d-maker` agent) | runs a stage skill | only what you approved |
| critic (`critique.py` → Gemini via `agy`) | judges the gate's files against a rubric, returns PASS/REVISE + issues | no |
| critic fallback (`idea3d-critic` agent) | same job when Gemini is unavailable or declined | no |
| reviser (`idea3d-reviser` agent) | applies free fixes, asks for paid ones | no (no Meshy tools) |

Gates: A1 judges the concept set, A2 the turnarounds (before Stage 2 spends credits), B the
Meshy tries, C the rig, clips and Blender finish together. The loop ends on PASS or after 2
revise rounds; the checkpoint shows any open issues. Fixes that spend credits run only after
a yes. Rubrics: `skills/idea-to-3d/references/rubrics/`. Protocol:
`skills/idea-to-3d/references/loop.md`.

The first question covers Meshy and Gemini together; `pipeline_state.py set-critic` records
the answer and `critique.py` refuses to run without it. Gemini CLI's personal login is
retired (`IneligibleTierError`), so the critic goes through the Antigravity CLI `agy`
(model `gemini-4-argon-medium`).

## Requirements

- **Windows**, **Blender 5.2** at `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`
  (or `$env:BLENDER_EXE`).
- **Node.js 22+** and **Python 3.12+** with Pillow.
- **`MESHY_API_KEY`** in your user environment — never in a file:
  ```powershell
  [Environment]::SetEnvironmentVariable("MESHY_API_KEY", "<your-meshy-api-key>", "User")
  ```
  The bundled `meshy` MCP server (`scripts/run-meshy-mcp.mjs`) reads it at launch.
- **The Antigravity CLI `agy`, logged in**, for the Gemini critic and free image generation.
  Without it the Claude critic runs and images come from Meshy (9 credits each).

## Use

Ask for a 3D model of an idea ("make a fox knight with a lantern as a rigged 3D model") or
run the `idea-to-3d` skill. Work goes to `work/<slug>/` in the current folder.

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
- Claude Code has no image-generation tool, so `scripts/generate_image.py` makes concepts and
  turnarounds through the Antigravity CLI for 0 credits (prompt via `--prompt-file`,
  reference images via `--ref`). Meshy `nano-banana-pro` (9 credits per image, approval
  first) is the paid fallback, and you can supply your own images.
- A full standard run (2 tries, 3 clips) costs about 79 Meshy credits with the free image
  route, about 133 when the images come from Meshy.

## Tests

```bash
python -m unittest discover -s plugins/idea-to-3d/tests -p "test_critic.py" -v
python -m unittest discover -s plugins/idea-to-3d/tests -p "test_generate_image.py" -v
python -m unittest discover -s plugins/idea-to-3d/tests -p "test_pipeline.py" -k Unit -v
```

## Antigravity copy

`C:\Users\User\Desktop\repo\idea-to-3d` is the same pipeline for Antigravity. It pulls the
files listed in `core-files.txt` from here with `scripts/sync-core.ps1`; this copy is the
source of truth.
