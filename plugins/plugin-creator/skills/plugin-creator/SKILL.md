---
name: plugin-creator
description: Scaffold a new customized plugin into the micky-psych-tools marketplace. Use when the user says "make me a plugin", "create a plugin", "scaffold a plugin", "scaffold a skill/command/agent", "new plugin", "add a plugin to the marketplace", or runs /new-plugin. Elicits a short fixed checklist (name, purpose, component type, trigger phrases, category), then generates plugin.json, the chosen component skeletons (skill, command, agent, hooks, or MCP wiring), registers the plugin in marketplace.json, and runs validate.py so the result passes every marketplace rule. Not for editing or versioning an existing plugin (hand-edit the files, then run scripts/bump.py), and not for installing, enabling, or managing plugins (that is Claude Code's built-in /plugin command).
---

# plugin-creator

Scaffold a new plugin into the **micky-psych-tools** marketplace so it passes
`scripts/validate.py` on the first run. This skill is marketplace-aware: it writes
into `plugins/<name>/`, registers the catalog entry, and validates.

Read `references/authoring-rules.md` before writing — it holds the hard rules every
generated plugin must satisfy. Fill from `references/templates/` rather than writing
files from scratch.

## Scope

- **Do:** create a brand-new plugin (skill, command, agent, hooks, or MCP wiring — any
  combination) inside this marketplace, register it, validate it.
- **Don't:** modify an existing plugin (hand-edit its files, then run `scripts/bump.py`),
  or install/enable/manage plugins (that's Claude Code's built-in `/plugin`).

## Procedure

Work the steps in order. Do not skip the guard or the validation.

### 1. Elicit — fixed checklist

Ask for each slot. If invoked via `/new-plugin <seed>`, pre-fill `purpose` from the
seed and only ask the gaps. Ask conversationally but cover every slot:

1. **name** — kebab-case, becomes the plugin dir + plugin.json name + catalog name.
2. **purpose** — one line: what it does.
3. **component type(s)** — one or more of: `skill`, `command`, `agent`, `hooks`,
   `mcp-wiring`. Multiple allowed in one plugin.
4. **trigger phrases** — the literal phrases that should fire it (needed for skill/agent
   descriptions). Skip if only command/hooks/mcp components.
5. **category** — read `.claude-plugin/marketplace.json`, collect the distinct `category`
   values already in use across `plugins[]`, and offer those plus free-text for a new one.

Version is fixed at `0.1.0`. Keywords are **derived** (3–6, from purpose + trigger
phrases) and shown for a quick confirm — don't ask for them separately.

For **mcp-wiring**, also ask for the existing server's `url` and `type`. Never generate
server code — only write the `.mcp.json` that references a server the user already runs.

### 2. Guard — before writing anything

- Reject the name if it isn't kebab-case (`^[a-z0-9]+(-[a-z0-9]+)*$`).
- Check `plugins/<name>/` and every entry in `.claude-plugin/marketplace.json`. If the
  name already exists → **stop, report it, ask for a different name.** Never overwrite.

### 3. Scaffold — from templates

Create `plugins/<name>/` and fill placeholders from `references/templates/`:

- Always: `.claude-plugin/plugin.json`.
- Per chosen component: `skills/<skill>/SKILL.md`, `commands/<cmd>.md`,
  `agents/<agent>.md`, `hooks/hooks.json`, `.mcp.json`.

For every **skill or agent** description, follow the recipe in
`references/authoring-rules.md` (action-first, third person, embed the verbatim trigger
phrases, a Use-when clause and a Not-for clause) and **enforce 200–1024 chars** — if the
draft is under 200, expand with more trigger phrasings before writing. Commands and hooks
get a plain one-line description.

### 4. Register

Add the plugin's entry to `.claude-plugin/marketplace.json`:
`{ name, source: "./plugins/<name>", version: "0.1.0", description, category, keywords }`.
The entry `version` MUST equal the plugin.json `version` — this parity is a hard rule.

### 5. Validate

Run the marketplace validator from the repo root:

```
python scripts/validate.py   # fall back to: python3 scripts/validate.py
```

**Do not claim success unless it prints `all checks passed`.** If it fails, report the
exact failing checks and the paths written — do not leave a silent half-plugin.

### 6. Refresh the router

Regenerate the router: `python scripts/route.py` (never hand-edit `ROUTING.md`).

### 7. Stop before commit

Print the validate output and a suggested conventional commit; do not stage or commit — the user reviews and commits.

```
git add plugins/<name> .claude-plugin/marketplace.json ROUTING.md
git commit -m "feat: add <name> plugin"
```

Do not run `bump.py` — a new plugin starts at `0.1.0`.
