# Changelog

## 1.0.0 — 2026-10-19

- Initial marketplace release, ported from the Antigravity `idea-to-3d` plugin.
- Five skills: `idea-to-3d` (orchestrator), `concept-art`, `image-to-3d`, `rig-animate`,
  `blender-finish`, each with its pipeline scripts.
- Bundled `meshy` MCP server (`scripts/run-meshy-mcp.mjs`) that reads `MESHY_API_KEY` from
  the environment or `HKCU\Environment` at launch — no key in any config file.
- Pipeline rules moved to `skills/idea-to-3d/references/pipeline-rules.md`, with a Claude
  Code tool mapping (§6): `ask_question` → `AskUserQuestion`, `view_file` → `Read`, Meshy
  `nano-banana-pro` fallback for concept images.
