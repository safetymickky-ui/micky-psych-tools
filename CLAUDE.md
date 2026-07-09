# micky-psych-tools — plugin marketplace

Personal Claude Code plugin marketplace. Single owner: Thanawat Suharit (Micky).
This repo is BOTH the marketplace and the home of every plugin in it.

## Layout

```
.claude-plugin/marketplace.json   # catalog — every plugin listed here
plugins/<name>/
  .claude-plugin/plugin.json       # plugin manifest (name, version, author, keywords)
  .mcp.json                        # optional — MCP servers (referenced from plugin.json)
  skills/<skill>/SKILL.md          # skill(s): frontmatter (name, description) + body
  commands/<cmd>.md                # optional — slash commands
  agents/<agent>.md                # optional — subagents
scripts/validate.py                # full marketplace + plugin validation
scripts/bump.py                    # version bump in BOTH manifest + catalog
```

## Hard rules (these have bitten before)

- **Version lives in two files.** A plugin's version in `plugins/<name>/.claude-plugin/plugin.json`
  MUST equal its entry in `.claude-plugin/marketplace.json`. If they drift, Claude Code sees
  no version change and silently offers no update. NEVER edit a version by hand — run
  `python3 scripts/bump.py <plugin> patch|minor|major` (it edits both, then validates).
- **SKILL.md description cap:** hard limit 1024 chars; aim well under. Too short (<~200) triggers
  unreliably. The description is the ONLY thing that decides when the skill fires — invest in it.
- **`name` is kebab-case** and must match: plugin dir name == plugin.json name == marketplace entry.
  Skill frontmatter `name` == its directory name.
- **`source` is a relative path** (`./plugins/<name>`) in the marketplace entry.

## Workflow for adding / changing a plugin

1. Scaffold under `plugins/<name>/` following the layout above.
2. Add the entry to `.claude-plugin/marketplace.json` (name, source, version, description, category, keywords).
3. `python3 scripts/validate.py` — must print `all checks passed`.
4. Bump with `scripts/bump.py` when releasing, never by hand.
5. Commit (conventional commits: `feat:`, `fix:`, `refactor:`…). One logical change per commit.

## Plugins

- **pubmed-research-note** — clinical decision from primary literature; verdict-first evidence reports.
- **intent-lock** — pre-build alignment gate; interrogate a request to one reading, then build.
- **plugin-creator** — meta-plugin: scaffolds new customized plugins into THIS marketplace
  (manifest + skill/command/agent/hooks/mcp-wiring skeleton + catalog entry + validation).
  Skill + `/new-plugin` command; elicit-first fixed checklist; auto-register + auto-validate,
  stops before commit. Authoring rules + templates under its `skills/plugin-creator/references/`.

## Style

Follow the user's global CLAUDE.md. Keep plugins simple — solve the real task, no premature
abstraction. Prefer editing existing plugins over adding new files.
