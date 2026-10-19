# Changelog

## 0.2.0 — 2026-10-19

- New `design-md-apply` skill: builds any UI or Artifact from the active DESIGN.md (tokens
  → CSS variables / Tailwind theme with dark mode, component specs, Do's and Don'ts,
  off-system value check).
- New SessionStart hook (`hooks/design_context.py`): announces the nearest project
  DESIGN.md, else the personal default `~/.claude/DESIGN.md`, every session.
- Lint commands use the `designmd` bin (`npx -p @google/design.md designmd lint`). The
  `design.md` bin name opens the `.md` file association on Windows and silently lints
  nothing.

## 0.1.0 — 2026-10-19

- Initial release: `design-md-generator` skill + `/design-md` command. Four source modes
  (site, brief, codebase, remix), Stitch-spec token front matter + ordered sections,
  mandatory `@google/design.md` lint, no-overwrite diff flow.
