# Changelog — egm-conductor

## 0.1.0 — 2026-10-26

- Initial release: two skills, `conduct` (`/egm-conductor:conduct [idea | design.md] [--from <phase>] [--auto]`)
  and `status` (`/egm-conductor:status`, read-only).
- Runs Google's Elephant-Goldfish Model end to end: preflight → optional bootstrap →
  brainstorm → draft → review (+resolve) → human approval gate → implement → drift report.
- Reads each EGM `SKILL.md` from the installed `egm@egm` path (EGM skills refuse the Skill
  tool) and spawns the registered `egm:egm-*` Goldfish agents for reviews.
- `scripts/egm_status.py` locates EGM via `installed_plugins.json`, checks Claude Code ≥ 2.1.271
  (Goldfish isolation), scans EGM artifacts, and suggests the next phase.
- Progress saved in `.egm-conductor/state.json` in the project, so a run resumes.
- `--auto` skips only the conductor's own confirmations; EGM's questions and the human gate
  always stop.
