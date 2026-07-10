---
name: refine-plugin
description: Audit and refine an EXISTING plugin or skill in the micky-psych-tools marketplace. Use when the user says "improve my plugin", "refine this skill", "audit my plugin", "audit this skill", "tighten the trigger description", "review my plugin", "fix version parity", "polish this skill", or runs /refine-plugin. Reports findings in two tiers — mechanical blockers (version parity, kebab-case, semver, description 200-1024 chars, MCP type/url, frontmatter name matches directory) and quality/triggering (weak or vague description, missing Not-for clause, trigger phrases absent from the description, bloated procedure) — each with a before/after fix, applies only the fixes you approve, then bumps the version via scripts/bump.py and validates. Not for creating a new plugin (use /new-plugin) or installing, enabling, or managing plugins (that is Claude Code's built-in /plugin command).
---

# refine-plugin

Audit and refine an **existing** plugin or skill in the **micky-psych-tools** marketplace,
then bump + validate. This is the counterpart to the `plugin-creator` skill: that one
creates, this one improves. It edits in place — it never creates a new plugin.

Read the mechanical rules from the sibling skill's
`../plugin-creator/references/authoring-rules.md` (single source of truth — do not copy
them). Read `references/audit-checklist.md` for the quality tier.

## Scope

- **Do:** audit + refine an existing plugin, or a single skill within one, in this
  marketplace — descriptions, structure, version parity, mechanical rule violations.
- **Don't:** create a new plugin (hand off: "use /new-plugin"), or install/enable/manage
  plugins (Claude Code's built-in `/plugin`).

## Procedure

### 1. Select the target

From `/refine-plugin <name>` if given. Otherwise list the plugins under `plugins/*` (and
their skills) and ask which to refine. The target is a whole plugin or one named skill.

### 2. Guard

- The target must **exist**. If it doesn't → stop, say so; if the user wants something new,
  hand off to `/new-plugin`. Never create.
- If the target is **outside this marketplace** (e.g. a global `~/.claude/skills/*`), you
  can audit and report but CANNOT `bump.py`/`validate.py` it — run **audit-only** and say
  so explicitly.

### 3. Audit — two tiers

Read the target's files. Produce findings in two ranked, tagged tiers:

- **[BLOCKER] mechanical** (from `authoring-rules.md`): version parity broken, non-kebab
  name, bad semver, skill/agent description outside 200–1024, missing `description` in a
  command's or agent's frontmatter, MCP server missing `type`/`url`, `source` not `./`,
  skill frontmatter `name` != directory.
- **[QUALITY] triggering / clarity** (from `references/audit-checklist.md`): description
  not action-first, trigger phrases missing from the description, no Use-when / Not-for
  clause, vague or bloated SKILL.md, redundant reference files.

For each finding give: the file, the problem, and a **before/after** fix. Rank blockers
first. If nothing is wrong, say so plainly — do not invent findings.

### 4. Apply on confirm

Present the findings and apply ONLY the fixes the user approves (per finding or in a
batch). Show nothing as done that wasn't applied.

### 5. Bump — only if edits were applied and target is in-marketplace

Propose a level from the change nature — **patch** (wording/mechanical), **minor**
(behavior/capability), **major** (breaking). On confirmation run from the repo root:

```
python scripts/bump.py <plugin> <level>   # fall back to python3
```

`bump.py` raises `plugin.json` + the catalog entry together and validates. If no edits
were applied, do not bump. For an out-of-marketplace audit-only run, there is no bump.

### 6. Refresh the router

If edits were applied to an in-marketplace target: regenerate the router — `python
scripts/route.py` (never hand-edit `ROUTING.md`). Skip for an audit-only run or when no
edits were applied.

### 7. Stop before commit

Stage the changes and STOP before committing — the user reviews and commits.

```
git add plugins/<plugin> ROUTING.md
git commit -m "refactor(<plugin>): refine <target>"
```
