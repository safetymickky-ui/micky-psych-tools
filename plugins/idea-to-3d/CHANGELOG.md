# Changelog

## 2.0.0 — 2026-10-20

Every stage is now checked before the user sees it: maker → independent critic → reviser.

- **Gates A1, A2, B, C.** A1 judges the concept set, A2 the turnarounds (before Stage 2
  spends credits), B the Meshy tries, C the rig, clips and Blender finish together.
  Rubrics with criteria, severity and a free/paid fix catalogue live in
  `skills/idea-to-3d/references/rubrics/`.
- **Gemini critic.** `scripts/critique.py` sends a gate's files to Gemini
  (`gemini-4-argon-medium`) through the Antigravity CLI (`agy -p --mode plan
  --json-schema`), validates the review and logs it in `pipeline.json`. Gemini CLI's
  personal login is retired (`IneligibleTierError`), so it is not used.
- **Fallback.** On exit 2/3 the `idea3d-critic` Claude agent reviews the same files; its
  review goes through the same validator (`--from-file`).
- **Reviser.** The `idea3d-reviser` agent applies free fixes and returns credit-spending
  fixes as requests; it has no Meshy tools. Paid fixes run only after a yes.
- **Free images.** `scripts/generate_image.py` makes concepts and turnarounds through the
  Antigravity CLI for 0 credits (prompt via `--prompt-file`, reference images via `--ref`);
  Meshy `nano-banana-pro` (9 credits per image) is the paid fallback. A full run drops from
  ≈133 to ≈79 credits.
- **Gate A2 question.** Turnarounds that end a gate with open issues are shown to the user
  before Stage 2 spends credits.
- **Stop rule.** PASS, or 2 revise rounds, then the checkpoint lists any open issues.
- **Consent.** The first question now covers Meshy and Gemini; `set-critic` records the
  answer and `critique.py` refuses to run without it.
- Shared core listed in `core-files.txt`; the Antigravity repo pulls it with
  `scripts/sync-core.ps1`.

## 1.1.0 — 2026-10-20

- Actionforge integration for the animation stage. New graph
  `skills/blender-finish/scripts/stage4-animate.act` chains import-merge → export-check →
  render-sheet and exits 1 on the first failing Blender step. The graph passes Actionforge's
  `validate_graph`.
- Bundled the `actionforge-app` MCP (Graph Builder, HTTP, no auth) in `.mcp.json` for editing
  and validating the graph.
- Running the graph needs the `actrun` CLI, which is optional and not bundled.

## 1.0.0 — 2026-10-19

- Initial marketplace release, ported from the Antigravity `idea-to-3d` plugin.
- Five skills: `idea-to-3d` (orchestrator), `concept-art`, `image-to-3d`, `rig-animate`,
  `blender-finish`, each with its pipeline scripts.
- Bundled `meshy` MCP server (`scripts/run-meshy-mcp.mjs`) that reads `MESHY_API_KEY` from
  the environment or `HKCU\Environment` at launch — no key in any config file.
- Pipeline rules moved to `skills/idea-to-3d/references/pipeline-rules.md`, with a Claude
  Code tool mapping (§6): `ask_question` → `AskUserQuestion`, `view_file` → `Read`, Meshy
  `nano-banana-pro` fallback for concept images.
