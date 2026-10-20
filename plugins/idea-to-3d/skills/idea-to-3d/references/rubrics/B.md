# Gate B — Meshy image-to-3D tries

Inputs: `idea.md`, `images/front.png` (the approved front view), `preview/tries.png` (each try
rendered front, three-quarter, side and a face close-up, labelled "Try 1", "Try 2").

Judge each try against the front view and the brief. Rate the gate by its **best** try:
issues on the weaker try are `minor` unless no try is usable.

## Criteria

Give one score (1–5) for each:

- `geometry` — silhouette and proportions match the front view in every view on the sheet (the back is not rendered); nothing missing or extra.
- `artifacts` — no holes, melted or smeared face or hands, fused limbs or fingers, floating fragments, spikes, paper-thin parts.
- `texture` — colours match the brief's hex palette; no smeared, mirrored or misplaced texture.
- `symmetry` — left and right match where the design is symmetric.
- `rig-readiness` — humanoids: clear A- or T-pose, limbs separated from the body, hands open; non-humanoids: parts that must move are separate enough to bend.

## Severity

- `blocker` — no try can go on to rigging (both have a melted face, fused arms, or large holes).
- `major` — the best try has a defect a viewer notices at full-body size.
- `minor` — close-up flaws, small colour drift, defects only on the weaker try.

## Verdict and scores

- `PASS` when no `blocker` or `major` issue remains; minor issues may still be listed. Otherwise `REVISE`.
- Score each criterion: 5 no issue · 4 minor issues only · 3 one major · 2 several majors · 1 a blocker.
- Use the criterion ids above verbatim in `scores` and `issues[].criterion`, one score per criterion.
- One issue per defect; `id` is `<gate>-<n>` (`A1-1`, `C-3`); `credits` is the price from the list below, 0 for a free fix.
- A fix the user must decide (a different build, a different pick) has credits 0 and its `fix` starts with "user choice:".

## Fixes and their credits

- Recommend a different try at the checkpoint: 0, `fix` starts with "user choice:" — say which and why.
- Input clean-up (recrop, re-pad, regenerate a view) only helps with a new try: describe it inside that try's `fix`, not as a separate free issue.
- New try with `meshy_multi_image_to_3d`, `meshy-7.1`, 4K texture: 30. Name the setting or input to change (for example `pose_mode: "a-pose"`, a regenerated side view).
- New tracer try with `meshy-6-lite`: 15.

Write `evidence` as "Try N, <view>: <what you see>". One issue per defect.
