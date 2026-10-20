# Gate C — rig, clips and Blender finish

Inputs: `idea.md`, `images/front.png`, `preview/sheet.png` (concept column, then 4 views ×
start/mid/end frames for each clip), `out/quality_report.json` (the `check-glb.py` result).

## Criteria

Give one score (1–5) for each:

- `checks` — every check in `quality_report.json` passes (scale, triangles, size, clips, materials).
- `deformation` — in every clip frame: no tearing, candy-wrapper twists, collapsed shoulders or hips, limbs passing through the body.
- `clip-readability` — each clip reads as its name (idle breathes, walk steps, wave waves) from the front and three-quarter views.
- `placement` — the model stands on the ground, faces front, and its height matches `idea.md`.
- `texture-seams` — no visible seams, stretched UVs or missing texture regions.

## Severity

- `blocker` — any failed check in `quality_report.json`, or a clip that tears the mesh.
- `major` — visible deformation or a clip that does not read as its name.
- `minor` — small seams, slight foot sliding, subtle interpenetration.

## Fixes and their credits

- Re-run `import-merge.py` with different options, then `export-check.py` and `render-sheet.py`: 0. Name the option: `--height <m>`, `--max-triangles <n>`, `--clips <list>`, `--procedural-rig` (non-humanoids, or when the Meshy rig tears), `--scripted-robot`.
- Re-rig with `meshy_rig`: 5.
- Re-animate one clip with `meshy_animate`: 3 per action. Name the action.
- A fix that needs a code change to a plugin script: credits 0 and start `fix` with "needs plugin change:" — the reviser cannot apply it and it stays open at the checkpoint.

Write `evidence` as "<clip>, <view>, <frame>: <what you see>" or "quality_report: <check>".
