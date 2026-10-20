# Gate C — rig, clips and Blender finish

Inputs: `idea.md`, `images/front.png`, `preview/sheet.png` (concept column, then 4 views ×
start/mid/end frames for each clip), `out/quality_report.json` (the `check-glb.py` result).

## Criteria

Give one score (1–5) for each:

- `checks` — `quality_report.json` has `"ok": true` and an empty `errors` list. Each entry in `errors` is one `blocker` issue; each `warnings` entry is at most `minor`.
- `deformation` — in every clip frame: no tearing, candy-wrapper twists, collapsed shoulders or hips, limbs passing through the body.
- `clip-readability` — each non-idle clip shows its motion across start/mid/end (walk: legs alternate; wave: raised hand moves). `idle` only needs a natural standing pose without deformation. Identical frames in a non-idle clip are `major`.
- `placement` — feet on the ground line, model faces the Front view; height is judged from `quality_report.json` `summary.height_m`, not the image.
- `texture-seams` — no visible seams, stretched UVs or missing texture regions.

## Severity

- `blocker` — any entry in `quality_report.json` `errors`, or a clip that tears the mesh.
- `major` — visible deformation or a clip that does not read as its name.
- `minor` — small seams, subtle interpenetration. Do not judge timing, speed or foot sliding: the sheet has only three frames per clip.

## Verdict and scores

- `PASS` when no `blocker` or `major` issue remains; minor issues may still be listed. Otherwise `REVISE`.
- Score each criterion: 5 no issue · 4 minor issues only · 3 one major · 2 several majors · 1 a blocker.
- Use the criterion ids above verbatim in `scores` and `issues[].criterion`, one score per criterion.
- One issue per defect; `id` is `<gate>-<n>` (`A1-1`, `C-3`); `credits` is the price from the list below, 0 for a free fix.
- A fix the user must decide (a different build, a different pick) has credits 0 and its `fix` starts with "user choice:".

## Fixes and their credits

- Re-run `import-merge.py` with different options, then `export-check.py` (same `--height`, `--max-triangles`, `--clips`) and `render-sheet.py` (same `--clips`): 0. Name the option: `--height <m>`, `--max-triangles <n>`, `--clip <name>=<glb>` (drop or swap a Meshy clip; pass the matching `--clips` to `export-check.py`), `--clips <list>` (procedural rigs only).
- Switch to a procedural rig (`--mesh <remesh.glb> --procedural-rig`) or a scripted build (`--scripted-robot`): 0, `fix` starts with "user choice:" — it replaces the Meshy rig (no leg bones) or the whole model, so it is offered at the checkpoint, never applied automatically.
- Re-rig with `meshy_rig`: 5 + 3 per `meshy_animate` clip that must be redone on the new rig. Name what changes (e.g. `height_meters`, a new remesh first: +5); an unchanged re-run gives the same rig.
- Animate a different action with `meshy_animate`: 3. Name the replacement `action_id` from `meshy_list_animations`; repeating the same action on the same rig gives the same motion.
- A fix that needs a code change to a plugin script: credits 0 and start `fix` with "needs plugin change:" — the reviser cannot apply it and it stays open at the checkpoint.

Write `evidence` as "<clip>, <view>, <frame>: <what you see>" or "quality_report: <error text verbatim>".
