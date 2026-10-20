# idea-to-3d v2 — maker → Gemini critic → reviser loop

Date: 2026-10-20 · Owner: Thanawat Suharit · Status: approved design, awaiting spec review

## Problem

`idea-to-3d` v1.0.0 runs each stage once and shows the first pass to the user at a
checkpoint. First passes are often weak (concept drifts from the brief, Meshy tries with
melted faces or holes, clips that tear the mesh). The user wants every stage checked by an
independent reviewer and revised before they see it, with Gemini (via Gemini CLI) as the
reviewer.

## Decisions (locked with the user)

| # | Decision | Choice |
|---|---|---|
| 1 | Where the v2 lives | Both: a new Claude Code plugin in this marketplace **and** the Antigravity repo, sharing one core |
| 2 | Which stages loop | All 4 stages; free fixes auto-apply, any fix that spends Meshy credits asks the user first |
| 3 | Stop rule | Stop on PASS or after 2 revise rounds, then go to the checkpoint with remaining issues listed |
| 4 | Gemini fails | Fall back to a Claude critic subagent with the same rubric and schema; record which critic ran |
| 5 | Gemini wiring | Script wrapper `critique.py` calling headless `gemini -p` (not an MCP server, not an agent shelling out) |

## Current state

- Source: Antigravity plugin at `C:\Users\User\Desktop\repo\idea-to-3d` (v1.0.0; 5 skills:
  `idea-to-3d`, `concept-art`, `image-to-3d`, `rig-animate`, `blender-finish`; scripts;
  `rules/idea-to-3d.md`; `LESSONS_LEARNED.md`; tests). Claude Code runs a copy in
  `~/.claude/skills/` adapted by `~/.claude/rules/idea-to-3d.md` §6.
- Not in the marketplace catalog. `plugins/idea-to-3d/` holds only a git-ignored
  `__pycache__` — delete it when the port lands.
- Gemini CLI 0.33.1 is installed (`oauth-personal`); headless `-p`, `--approval-mode plan`
  (read-only), `-o json`, images attached with `@path`.
- Antigravity plugins ship no agent definitions (`agy agents` lists none); subagents are
  dispatched at runtime with a brief.

## Architecture

```
orchestrator (main thread — the only place that can ask the user or approve credits)
 └ per gate:
   maker      → runs the existing stage skill → artifacts + preview PNG
   critic     → critique.py → Gemini (read-only; sees artifacts + brief, never the maker's reasoning)
                 └ exit ≠ 0 → Claude critic subagent, same rubric + schema
   PASS   → checkpoint
   REVISE → reviser: applies FREE fixes, returns PAID fixes as requests
            → orchestrator asks the user for paid ones → re-preview → critic again
   cap: PASS or 2 revise rounds → checkpoint shows remaining issues + review history
```

### Gates

Three critique gates cover all four stages. Stage 3 output (rig, clips) only becomes
visible once Blender renders it, so it is judged at gate C together with Stage 4.

| Gate | Before | Critic inputs | Rubric criteria |
|---|---|---|---|
| A | Checkpoint A | `idea.md`, `preview/concepts.png`; after the pick, `images/front.png`, `side.png`, `back.png` | fidelity to brief (silhouette, hex palette, proportions, materials); Meshy-readiness (plain background, full body uncropped, A/T-pose for humanoids, low perspective); turnaround consistency (side/back match front) |
| B | Checkpoint B | `idea.md`, `images/front.png`, `preview/tries.png` | geometry fidelity to concept; texture fidelity; artifacts (holes, melted face/hands, floating fragments, fused limbs); symmetry; pose fit for rigging |
| C | Checkpoint C | `idea.md`, `images/front.png`, `preview/sheet.png`, `check-glb.py` report | deformation per clip (tearing, candy-wrapper, intersections); clip readability; scale/grounding/orientation; texture seams; every `check-glb` check passing |

Gate A runs twice: once on the concept set before the pick, once on the turnarounds after
it (turnarounds feed Meshy, so they are checked before credits are spent at gate B).

### Fix catalogue (free vs paid)

| Gate | Free (reviser applies) | Paid (reviser requests, user approves) |
|---|---|---|
| A | rewrite `idea.md` / image prompts | regenerate an image: 9 cr each (`nano-banana-pro`) |
| B | clean or crop input images (background, framing); choose the other try | new try: 15 cr (`meshy-6-lite`) or 30 cr (`meshy-7.1` 4K) |
| C | Blender script parameters: scale, origin, grounding, weight falloff, procedural-rig parameters, clip trimming | re-rig 5 cr; re-animate 3 cr per action |

A paid request names the exact Meshy tool, model and credit cost. The orchestrator
batches all paid requests of a round into one `AskUserQuestion` (recommended option
first). Every existing credit rule still holds: record each task id the moment it is
created, never re-create a recorded task.

### Roles

- **Maker** — runs the stage skill. Its brief carries the credit budget the user approved
  at the previous checkpoint; it may not spend beyond it. Returns artifact paths.
- **Critic** — `critique.py` (Gemini). Independent: receives only the artifacts, the brief
  and the rubric. Fallback is the `idea3d-critic` Claude subagent with the same inputs.
- **Reviser** — receives the review JSON. Applies every free fix, re-runs the stage's
  preview script, and returns `{applied[], paid_requests[]}`. Never calls a paid Meshy tool.

### Review JSON (`references/review.schema.json`)

```json
{
  "gate": "A|B|C",
  "round": 0,
  "critic": "gemini|claude-fallback",
  "model": "<model id>",
  "verdict": "PASS|REVISE",
  "scores": { "<criterion>": 1 },
  "issues": [
    { "id": "B-1", "severity": "blocker|major|minor", "criterion": "<criterion>",
      "evidence": "<what in which image>", "fix": "<concrete change>",
      "cost": "free" }
  ]
}
```

`scores` are 1–5. `cost` is `"free"` or an integer credit count. Verdict is PASS when no
blocker or major issue remains (the critic may not PASS with a blocker open; `critique.py`
enforces it).

Reviews are written to `work/<slug>/reviews/<gate>-r<round>.json` and recorded in
`pipeline.json` via new `pipeline_state.py` subcommands `record-review` and
`review-history`.

## `critique.py`

```
python critique.py <slug> <gate> --round <n> [--model <id>] [--timeout 150]
```

1. Loads `references/rubrics/<gate>.md`, `idea.md` and the gate's images.
2. Builds the prompt: rubric + brief + `@path` image references + the schema + "output only JSON".
3. Runs `gemini -p <prompt> --approval-mode plan -o json -m <model>` with the timeout.
   Model defaults to the Gemini CLI default; overridden by `--model` or `IDEA3D_CRITIC_MODEL`.
4. Extracts the response, validates it against the schema, enforces the PASS rule.
   On invalid JSON, retries once with the validation error appended.
5. Writes the review file and prints its path.

Exit codes: `0` valid review written · `2` Gemini unavailable (missing binary, auth,
quota, timeout) · `3` schema failed twice. On `2` or `3` the orchestrator dispatches the
Claude critic and records `critic: "claude-fallback"` with the reason.

Never passes any API key on the command line or writes one to disk.

## Layout

### Shared core (identical bytes in both copies)

```
skills/idea-to-3d/
  references/loop.md             loop protocol: gates, rounds, PASS/REVISE, free vs paid, logging
  references/roles/maker.md      maker brief template
  references/roles/reviser.md    reviser rules
  references/roles/critic.md     Claude-fallback critic instructions
  references/rubrics/A.md B.md C.md
  references/review.schema.json
  scripts/critique.py
  scripts/pipeline_state.py      + record-review, review-history
```

### Claude Code — `plugins/idea-to-3d/` in this marketplace (source of truth)

- The five skills ported from the Antigravity repo, with the `~/.claude/rules/idea-to-3d.md`
  §6 adaptations applied in place (`AskUserQuestion`, `Read` on PNGs, Meshy
  `nano-banana-pro` fallback for images) and the credit/safety rules folded into the
  orchestrator `SKILL.md`, so the plugin does not depend on a user-scope rules file.
- `agents/idea3d-maker.md`, `agents/idea3d-reviser.md`, `agents/idea3d-critic.md` — thin
  wrappers: frontmatter + "follow `references/roles/<role>.md`".
- `.claude-plugin/plugin.json` (v2.0.0), `.mcp.json` (meshy), `README.md`, `CHANGELOG.md`,
  `LICENSE` (MIT), catalog entry in `.claude-plugin/marketplace.json` (≤ 500 chars),
  a `CLAUDE.md` plugins-list entry, `ROUTING.md` regenerated.
- Version set through `scripts/bump.py`, never by hand.

### Antigravity — `C:\Users\User\Desktop\repo\idea-to-3d`

- Orchestrator dispatches its generic subagent with `references/roles/<role>.md` as the brief.
- `scripts/sync-core.ps1` copies the shared-core file list from the marketplace copy;
  the Antigravity repo never edits core files directly.
- `plugin.json` 2.0.0; `rules/idea-to-3d.md` gains the loop and Gemini-consent rules;
  install via the existing `sync-plugin.ps1`.

After both land, `~/.claude/rules/idea-to-3d.md` §6 and the `~/.claude/skills/` copies are
superseded by the marketplace plugin; removing them is a separate, user-confirmed step.

## Consent and privacy

Gemini receives the brief and preview images. The first-upload consent at Checkpoint A
changes from "Meshy" to "Meshy and Gemini (Google)". Images of real people still need
explicit permission. If the user declines Gemini, the run uses the Claude critic for every
gate and records why.

## Error handling

- Gemini unavailable or bad output → Claude critic fallback (exit codes above).
- Reviser fix breaks a script (non-zero Blender exit) → revert to the pre-round artifacts,
  log the failed fix as an open issue, continue to the next round or the checkpoint.
- User declines a paid request → issue stays open and is listed at the checkpoint.
- Resume in a new conversation: `review-history` shows the last gate and round; the loop
  continues from there, never re-running a recorded paid task.

## Testing

- `critique.py` with a fake `gemini` executable on `PATH`: valid review; malformed then
  valid (retry); malformed twice (exit 3); timeout and missing binary (exit 2); PASS with a
  blocker rejected.
- Schema validated against fixture reviews (valid and invalid).
- `pipeline_state.py` `record-review` / `review-history` round-trip.
- Core parity: test hashes the shared-core files in both copies (Antigravity side).
- Marketplace: `bash scripts/health.sh` prints `health: OK`.
- One live acceptance run per platform on a cheap idea (`meshy-6-lite` tracer) before release.

## Out of scope

- Changing the Meshy or Blender pipeline steps themselves.
- Automatic paid retries without user approval.
- More than one external reviewer, or voting between critics.
