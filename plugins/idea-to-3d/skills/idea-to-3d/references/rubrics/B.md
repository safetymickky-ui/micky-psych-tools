# Gate B — Meshy image-to-3D tries

Inputs: `idea.md`, `images/front.png` (the approved front view), `preview/tries.png` (each try
rendered front, three-quarter, side and a face close-up, labelled "Try 1", "Try 2").

Judge each try against the front view and the brief. Rate the gate by its **best** try:
issues on the weaker try are `minor` unless no try is usable.

## Criteria

Give one score (1–5) for each:

- `geometry` — silhouette and proportions match the front view from every angle; nothing missing or extra.
- `artifacts` — no holes, melted or smeared face or hands, fused limbs or fingers, floating fragments, spikes, paper-thin parts.
- `texture` — colours match the brief's hex palette; no smeared, mirrored or misplaced texture.
- `symmetry` — left and right match where the design is symmetric.
- `rig-readiness` — humanoids: clear A- or T-pose, limbs separated from the body, hands open; non-humanoids: parts that must move are separate enough to bend.

## Severity

- `blocker` — no try can go on to rigging (both have a melted face, fused arms, or large holes).
- `major` — the best try has a defect a viewer notices at full-body size.
- `minor` — close-up flaws, small colour drift, defects only on the weaker try.

## Fixes and their credits

- Pick the other try: 0 — say which and why.
- Clean or recrop the input images before a re-run: 0, but it only helps together with a new try.
- New try with `meshy_multi_image_to_3d`, `meshy-7.1`, 4K texture: 30. Name the setting or input to change (for example `pose_mode: "a-pose"`, a regenerated side view).
- New tracer try with `meshy-6-lite`: 15.

Write `evidence` as "Try N, <view>: <what you see>". One issue per defect.
