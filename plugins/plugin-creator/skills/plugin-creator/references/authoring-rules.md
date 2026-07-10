# Authoring rules — what every generated plugin must satisfy

Distilled from `scripts/validate.py` and the repo `CLAUDE.md`. If a scaffold breaks any
of these, `validate.py` fails and the plugin is not done.

## Names

- Plugin `name` is **kebab-case**: `^[a-z0-9]+(-[a-z0-9]+)*$`.
- These three must be identical: the `plugins/<name>/` directory, `plugin.json` `name`,
  and the marketplace entry `name`.
- A **skill's** frontmatter `name` must equal its own directory name
  (`skills/<skill>/SKILL.md` → `name: <skill>`).

## Versions

- `version` is semver `\d+\.\d+\.\d+`. New plugins start at **`0.1.0`**.
- **Parity rule (the one that bites):** the marketplace entry `version` must equal the
  plugin.json `version`. If they drift, Claude Code offers no update silently. New plugins
  set both to `0.1.0`; later changes go through `scripts/bump.py`, never by hand.

## Marketplace entry

- Lives in `.claude-plugin/marketplace.json` under `plugins[]`.
- `source` is a **relative path starting `./`** → `./plugins/<name>`.
- Fields: `name`, `source`, `version`, `description`, `category`, `keywords[]`.

## Skill / agent descriptions

- Length **200–1024 chars** for BOTH skill and agent descriptions (hard cap 1024; under
  ~200 triggers unreliably). `validate.py` enforces this range for every `skills/*/SKILL.md`
  and every `agents/*.md`.
- The description is the ONLY thing that decides when the skill/agent fires. Recipe:
  - **Third person, action-first** — "Scaffolds a…", not "This skill will…".
  - **Embed the verbatim trigger phrases** the user gave.
  - **A "Use when…" clause and a "Not for…" clause** — negative scope sharpens triggering.

## Command / agent frontmatter presence

- Every `commands/*.md` and every `agents/*.md` file must have a **non-empty
  `description`** field in its frontmatter — `validate.py` checks this for both.
- Commands do NOT trigger on description, so no length requirement applies to them — a
  plain one-liner is fine, it just has to exist.
- Agents DO trigger on description (same mechanism as skills), so on top of presence,
  `validate.py` also enforces the 200–1024 length gate from the section above.
- Hooks have no description field and are not checked here.

## MCP wiring (never generate a server)

- `plugin.json` references the file: `"mcpServers": "./.mcp.json"`.
- `.mcp.json` shape: `{ "mcpServers": { "<id>": { "type": "...", "url": "..." } } }`.
- Every server entry must have both `type` and `url`. Only wire a server the user already
  runs — do not author server code.

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

Only the immediate children of `plugins/<name>/skills/` are scanned as skills. Nested
folders (e.g. a skill's own `references/`) are not validated as skills.

## Done means

`python scripts/validate.py` (or `python3 …`) prints `all checks passed`. Nothing less.
