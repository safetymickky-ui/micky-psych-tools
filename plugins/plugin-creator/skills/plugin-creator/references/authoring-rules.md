# Authoring rules — what every generated plugin must satisfy

Distilled from `scripts/validate.py` and the repo `CLAUDE.md`. A rule marked **[FAIL]**
makes `validate.py` fail; **[WARN]** makes it warn only. Unmarked rules come from
CLAUDE.md: the script does not check them, but they still bind.

## Names

- Plugin `name` is **kebab-case**: `^[a-z0-9]+(-[a-z0-9]+)*$`. **[FAIL]**
- These three must be identical: the `plugins/<name>/` directory, `plugin.json` `name`,
  and the marketplace entry `name` (`plugin.json` vs entry: **[FAIL]**).
- A **skill's** frontmatter `name` must equal its own directory name
  (`skills/<skill>/SKILL.md` → `name: <skill>`). **[FAIL]**

## Versions

- `version` is semver `\d+\.\d+\.\d+` **[FAIL]** and lives in `plugin.json` **only**; the
  marketplace entry carries none. New plugins start at **`0.1.0`**.
- Later releases go through `python3 scripts/bump.py <plugin> patch|minor|major --write`
  (a dry run without `--write`). It validates, writes the new version to `plugin.json` and
  adds a `## <version> — <date>` CHANGELOG heading to fill in. Never edit a version by hand.

## Marketplace entry

- Lives in `.claude-plugin/marketplace.json` under `plugins[]`.
- `source` is a **relative path starting `./`** → `./plugins/<name>`. **[FAIL]**
- Fields: `name`, `source`, `description`, `category`, `keywords[]`. No `version`.

## Skill / agent descriptions

- **Hard cap 1024 chars** for skill and agent descriptions. **[FAIL]**
- **Aim for 200+ chars**: under ~200 triggers unreliably. **[WARN]** for a skill;
  `validate.py` does not check an agent's floor.
- Frontmatter must parse as **strict YAML**. **[FAIL]** Wrap the description in double
  quotes when it contains `: ` (a colon and a space), the usual cause.
- The description is the ONLY thing that decides when the skill/agent fires. Recipe:
  - **Third person, action-first** — "Scaffolds a…", not "This skill will…".
  - **Embed the verbatim trigger phrases** the user gave.
  - **A "Use when…" clause and a "Not for…" clause** — negative scope sharpens triggering.

## Command / agent frontmatter presence

- Every `commands/*.md` and every `agents/*.md` file must have a **non-empty
  `description`** field in its frontmatter. **[FAIL]**
- Commands do NOT trigger on description, so no length requirement applies to them — a
  plain one-liner is fine, it just has to exist.
- Agents DO trigger on description (same mechanism as skills), so the 1024-char cap
  applies too **[FAIL]**; aim for 200+ as for a skill.
- Hooks have no description field and are not checked here.

## MCP wiring (never generate a server)

- `plugin.json` references the file: `"mcpServers": "./.mcp.json"`.
- Each server in `.mcp.json` is either **http/sse** (`{ "type": "http", "url": "…" }`) or
  **stdio** (`{ "command": "…", "args": [ … ] }`). Any other shape **[FAIL]**.
- Only wire a server the user already runs — do not author server code.

## Folder layout

```
plugins/<name>/
  .claude-plugin/plugin.json
  .mcp.json                 # only if mcp-wiring
  skills/<skill>/SKILL.md   # + optional references/
  commands/<cmd>.md
  agents/<agent>.md
  hooks/hooks.json
```

`validate.py` validates only the immediate children of `plugins/<name>/skills/` as
skills, but some Claude surfaces search deeper and load any file named `SKILL.md` as a
skill: plugin-creator's own `references/templates/SKILL.md` once appeared as a live skill
named `skill-name`. So `SKILL.md` is a reserved file name, and only
`skills/<skill>/SKILL.md` may carry it. Give a skill-shaped template, example or fixture
another name (`SKILL.template.md`). A `SKILL.md` (any case) anywhere else in the plugin
**[FAIL]**.

## Done means

`python scripts/validate.py` (or `python3 …`) prints `all checks passed`. Nothing less.
