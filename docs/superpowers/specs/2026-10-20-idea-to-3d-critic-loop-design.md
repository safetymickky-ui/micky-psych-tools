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
| 5 | Gemini wiring | Script wrapper `critique.py` (not an MCP server, not an agent shelling out) |
| 6 | Gemini route | Antigravity CLI `agy -p` with `gemini-4-argon-medium` — Gemini CLI personal OAuth is retired (see Current state) |

## Current state

- Source: Antigravity plugin at `C:\Users\User\Desktop\repo\idea-to-3d` (v1.0.0; 5 skills:
  `idea-to-3d`, `concept-art`, `image-to-3d`, `rig-animate`, `blender-finish`; scripts;
  `rules/idea-to-3d.md`; `LESSONS_LEARNED.md`; tests). Claude Code runs a copy in
  `~/.claude/skills/` adapted by `~/.claude/rules/idea-to-3d.md` §6.
- Not in the marketplace catalog. `plugins/idea-to-3d/` holds only a git-ignored
  `__pycache__` — delete it when the port lands.
- Gemini CLI 0.33.1 is installed but its `oauth-personal` login now fails with
  `IneligibleTierError` ("migrate to the Antigravity suite"). Probed 2026-10-20:
  `agy -p <prompt> --output-format json --mode plan --model gemini-4-argon-medium
  --json-schema <file> --add-dir <dir>` read a PNG named by absolute path in the prompt and
  returned `{"status":"SUCCESS","response":...,"structured_output":{...}}` in ~50 s.
- The Meshy MCP server is already registered at user scope as `meshy`; the plugin does not
  bundle a second copy (two servers would duplicate every Meshy tool).
- v1 `export-check.py --report` writes `work/<slug>/out/quality_report.json` (the
  `check-glb` result) — gate C reads it.
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

| Gate id | Before | Critic inputs (under `work/<slug>/`) | Rubric criteria |
|---|---|---|---|
| A1 | Checkpoint A | `idea.md`, `preview/concepts.png` | fidelity to brief (silhouette, hex palette, proportions, materials); Meshy-readiness (plain background, full body uncropped, A/T-pose for humanoids, low perspective); variety across candidates |
| A2 | Stage 2 credits | `idea.md`, `images/front.png`, `images/side.png`, `images/back.png` | one view per image; turnaround consistency (side/back match front); Meshy-readiness |
| B | Checkpoint B | `idea.md`, `images/front.png`, `preview/tries.png` | geometry fidelity to concept; texture fidelity; artifacts (holes, melted face/hands, floating fragments, fused limbs); symmetry; pose fit for rigging |
| C | Checkpoint C | `idea.md`, `images/front.png`, `preview/sheet.png`, `out/quality_report.json` | deformation per clip (tearing, candy-wrapper, intersections); clip readability; scale/grounding/orientation; texture seams; every `check-glb` check passing |

Gate A is split: A1 judges the concept set before the pick, A2 the turnarounds after it
(turnarounds feed Meshy, so they are checked before credits are spent at gate B). Each gate
id has its own rubric file.

### Fix catalogue (free vs paid)

| Gate | Free (reviser applies) | Paid (reviser requests, user approves) |
|---|---|---|
| A1, A2 | rewrite `idea.md` / image prompts | regenerate an image: 9 cr each (`nano-banana-pro`; in Antigravity the `image-generator` path is free, so the fix is free there) |
| B | clean or crop input images (background, framing); choose the other try | new try: 15 cr (`meshy-6-lite`) or 30 cr (`meshy-7.1` 4K) |
| C | re-run Blender with `import-merge.py` options (`--height`, `--max-triangles`, `--clips`, `--procedural-rig`, `--scripted-robot`), then `export-check.py` and `render-sheet.py` | re-rig 5 cr; re-animate 3 cr per action |

A fix that needs a code change to a plugin script is out of the reviser's reach: it is
declined with "needs plugin change" and stays open at the checkpoint.

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

The critic produces four fields; `critique.py` validates them and adds `round`, `critic`,
`model` and `reason` before writing the canonical file.

```json
{
  "gate": "A1|A2|B|C",
  "verdict": "PASS|REVISE",
  "scores": [ { "criterion": "<criterion>", "score": 1 } ],
  "issues": [
    { "id": "B-1", "severity": "blocker|major|minor", "criterion": "<criterion>",
      "evidence": "<what in which image>", "fix": "<concrete change>", "credits": 0 }
  ]
}
```

Shapes are kept to what Gemini structured output handles reliably: a list instead of a
score map, and one integer `credits` (`0` = free fix, else Meshy list price) instead of a
union type. `score` is 1–5. PASS is invalid while any blocker or major issue is listed;
REVISE needs at least one issue. `critique.py` enforces both.

Reviews are written to `work/<slug>/reviews/<gate>-r<round>.json` and appended to
`pipeline.json["reviews"]`. Round 0 judges the maker's output; rounds 1 and 2 follow each
revise round. `pipeline_state.py review-history <slug> [--gate <id>]` prints the log.

## `critique.py`

```
python critique.py <slug> <gate> [--round <n>] [--model <id>] [--timeout 240] [--work-root .]
python critique.py <slug> <gate> --from-file <raw.json> --critic claude-fallback --reason "<why>"
```

1. Resolves the gate's input files; a missing input is a usage error (exit 1).
2. Builds the prompt: rubric `references/rubrics/<gate>.md` + text inputs inline
   (`idea.md`, `quality_report.json`) + absolute paths of the PNGs + "judge only what you
   see; output only the JSON object".
3. Runs `agy -p <prompt> --output-format json --mode plan --disable-slash-commands
   --model <model> --json-schema references/review.schema.json --add-dir <work dir>`
   with the timeout. Model: `--model`, else `IDEA3D_CRITIC_MODEL`, else
   `gemini-4-argon-medium`. Binary: `IDEA3D_AGY`, else `agy` on `PATH`.
4. Takes `structured_output` (else the last JSON object in `response`), validates it,
   and on failure retries once with the errors appended.
5. Writes the review file, records it in `pipeline.json`, prints the path.

`--round` defaults to the number of reviews already recorded for that gate.
`--from-file` skips step 3–4's call and validates a review the Claude critic wrote, so
both critics go through one validator.

Exit codes: `0` review written · `1` usage error · `2` critic unavailable (binary
missing, non-zero exit, status ≠ SUCCESS, timeout) · `3` invalid review twice. On `2` or
`3` the orchestrator dispatches the Claude critic, then records its review with
`--from-file --critic claude-fallback --reason "<exit code + message>"`.

Default timeout 240 s (a one-image probe took ~50 s); the calling shell gets a 10-minute
limit. No key is involved: `agy` uses the user's own Antigravity login.

## Layout

### Shared core (identical bytes in both copies)

```
skills/idea-to-3d/
  references/loop.md             loop protocol: gates, rounds, PASS/REVISE, free vs paid, logging
  references/roles/maker.md      maker brief
  references/roles/reviser.md    reviser rules + output format
  references/roles/critic.md     Claude-fallback critic instructions
  references/rubrics/A1.md A2.md B.md C.md
  references/review.schema.json
  scripts/critique.py
  scripts/pipeline_state.py      + reviews log, review-history
tests/test_critic.py, tests/fake_agy.py
```

Core files never name a platform tool (`AskUserQuestion`, `ask_question`, `Read`,
`view_file`); they say "ask the user with the question tool" and let each orchestrator
`SKILL.md` map it.

### Claude Code — `plugins/idea-to-3d/` in this marketplace (source of truth)

- The five skills ported from the Antigravity repo, with the `~/.claude/rules/idea-to-3d.md`
  §6 adaptations applied in place (`AskUserQuestion`, `Read` on PNGs, Meshy
  `nano-banana-pro` fallback for images) and the credit/safety rules folded into the
  orchestrator `SKILL.md`, so the plugin does not depend on a user-scope rules file.
- `agents/idea3d-maker.md`, `agents/idea3d-reviser.md`, `agents/idea3d-critic.md` — thin
  wrappers: frontmatter + "follow `references/roles/<role>.md`".
- `.claude-plugin/plugin.json` (ported at 1.0.0, then `bump.py major` → 2.0.0), no
  `.mcp.json` (uses the user-scope `meshy` server), `README.md`, `CHANGELOG.md`,
  `LICENSE` (MIT), catalog entry in `.claude-plugin/marketplace.json` (≤ 500 chars),
  a `CLAUDE.md` plugins-list entry, `ROUTING.md` regenerated.
- Version set through `scripts/bump.py`, never by hand.
- Agents receive the absolute path of their role file in the dispatch prompt (the
  orchestrator knows its own base directory); `<plugin_root>` in the skills means the
  plugin directory two levels above the skill's base directory.
- The reviser agent is given no Meshy tools, so it cannot spend credits even by mistake.

### Antigravity — `C:\Users\User\Desktop\repo\idea-to-3d`

- Orchestrator dispatches its generic subagent with `references/roles/<role>.md` as the brief.
  The critic still runs as `critique.py` (it calls `agy` itself), so both platforms use
  the same Gemini route.
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
The answer is stored with `pipeline_state.py set-critic <slug> gemini|claude`;
`critique.py` refuses to call Gemini (exit 1) until it is recorded, and exits 2 when it
is `claude`, which sends the gate to the Claude critic.

## Error handling

- Gemini unavailable or bad output → Claude critic fallback (exit codes above).
- Reviser fix breaks a script (non-zero Blender exit) → revert to the pre-round artifacts,
  log the failed fix as an open issue, continue to the next round or the checkpoint.
- User declines a paid request → issue stays open and is listed at the checkpoint.
- Resume in a new conversation: `review-history` shows the last gate and round; the loop
  continues from there, never re-running a recorded paid task.

## Testing

- `critique.py` with a fake `agy` (`tests/fake_agy.py`): valid review; malformed then
  valid (retry); malformed twice (exit 3); timeout, non-zero exit, status ≠ SUCCESS and
  missing binary (exit 2); PASS with a blocker rejected; `--from-file` path.
- Schema validated against fixture reviews (valid and invalid).
- `pipeline_state.py` `record-review` / `review-history` round-trip.
- Core parity: test hashes the shared-core files in both copies (Antigravity side).
- Marketplace: `bash scripts/health.sh` prints `health: OK`.
- One live acceptance run per platform on a cheap idea (`meshy-6-lite` tracer) before release.

## Out of scope

- Changing the Meshy or Blender pipeline steps themselves.
- Automatic paid retries without user approval.
- More than one external reviewer, or voting between critics.
