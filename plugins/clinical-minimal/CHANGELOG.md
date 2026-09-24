# Changelog — clinical-minimal

## 0.1.0 — 2026-09-24

- Initial release, moved from the standalone `~/.claude/skills/clinical-minimal` skill.
- Design system tokens and rules (brand book: Clinical Minimal Design System artifact), `cm.py` helpers,
  `render.ps1`.
- Per-slide verification layer: `slidecheck.py` + `slideprobe.ps1`, review marks tied to each slide's layout.
- Picture selection algorithm: `imgpick.py` (filter, score incl. subject fill, placed preview, judge, choose).
- Fixed SKILL.md frontmatter: the description is a YAML block scalar (it failed to parse before).
