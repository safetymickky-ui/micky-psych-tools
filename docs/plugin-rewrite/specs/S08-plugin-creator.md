# Spec S08: plugin-creator, refine-plugin, validator and release tool

| Field | Value |
|---|---|
| Repos | micky-psych-tools |
| Units (today → target) | `plugins/plugin-creator` (skills `plugin-creator`,`refine-plugin`; commands `/new-plugin`,`/refine-plugin`,`/route`) + repo-root `scripts/{validate,bump}.py` → self-contained `plugin-creator`: skills `plugin-creator`(+alias `new-plugin`,dmi),`refine-plugin`(dmi); `scripts/{validate,release}.py`+tests; `references/`; `hooks/hooks.json` |
| Waves | W0 (smoke seeds, CX-4), W1 (root guard: `MICKY_TOOLS_DIR`→marker, else stop — H07), W3 (self-contained scripts; scaffold rewrite; templates; refine-plugin dmi; SessionStart hook; retire `/route`) |
| Owner decisions assumed | OD3-a (not merged into a family), OD9-a (`/new-plugin` kept as a dmi alias), OD10-a (refine-plugin dmi) |
| Defects closed | 14/14 assigned (HIGH: H07) |
| Interfaces owned | I19, I20 |
| Interfaces consumed | I16(S11), I17(S12), I18(S10), I24(S10), I25(S15) |
| Depends on specs | S10 (W0 fixed `validate.py`/`bump.py`, I18; marketplace shape, I24), S12 (eval layout, ratchet/trigger-lock formats, `eval.sh`, I17), S11 (W1-exit cloud enablement, I16), S15 (`check-contract.mjs`, I25) |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| Path | Lines | Bytes | Est. tok | Role |
|---|---|---|---|---|
| `.claude-plugin/plugin.json` | — | 580 | 145 | manifest |
| `README.md` | — | 2,308 | 577 | docs |
| `CHANGELOG.md` | — | 2,449 | 612 | docs |
| `commands/new-plugin.md` | 13 | 534 | 134 | wrapper |
| `commands/refine-plugin.md` | 12 | 530 | 133 | wrapper |
| `commands/route.md` | 25 | 1,249 | 312 | router cmd |
| `skills/plugin-creator/SKILL.md` | 93 | 4,745 | body 974 tok; description 767 chars/192 tok | scaffold skill |
| `.../references/authoring-rules.md` | — | 3,068 | 767 | mechanical rules |
| `.../templates/SKILL.md` | — | 718 | 180 | template — **breaks `yaml.safe_load`** (re-verified) |
| `.../templates/{plugin,marketplace-entry,hooks,.mcp}.json`,`agent.md` | — | 1,468 | 368 | templates, kept |
| `.../templates/command.md` | — | 213 | 53 | template (dropped, R34) |
| `.../templates/evals.json` | — | 762 | 191 | template (dropped, R70) |
| `skills/refine-plugin/SKILL.md` | 79 | 4,229 | body 819 tok; description 883 chars/221 tok | audit skill |
| `.../references/audit-checklist.md` | — | 4,367 | 1,092 | quality tier |
| `scripts/validate.py` (repo root; moves W3) | 142 | — | — | validator |
| `scripts/bump.py` (repo root; moves W3 → `release.py`) | 62 | — | — | bumper |
| `scripts/route.py` (repo root; retired) | 164 | — | — | router gen |

### 1.2 Descriptions

| Skill | Chars | Bytes | YAML valid? | `Use when` @ | `Not for`? | Quoted phrases |
|---|---|---|---|---|---|---|
| `plugin-creator` | 767 | 767 | yes | 73 | yes, wrong target (§1.3 #4) | "make me a plugin", "create a plugin", "scaffold a plugin", "scaffold a skill/command/agent", "new plugin", "add a plugin to the marketplace" |
| `refine-plugin` | 883 | 887 | yes | 83 | yes | "improve my plugin", "refine this skill", "audit my plugin", "audit this skill", "tighten the trigger description", "review my plugin", "fix version parity", "polish this skill" |

`refine-plugin`'s `has_first_or_second_person`=true (measured): "the fixes **you** approve" — not a quote. Both open imperative ("Scaffold…"/"Audit…"), not third person — breaks `authoring-rules.md:33`.

### 1.3 Defects

| id | sev (H#) | evidence (re-opened) | problem → fix (wave) |
|---|---|---|---|
| plugin-creator-1 | H, H07 | `SKILL.md:9-10,47-51` | no cwd check; guard checks only name/collision → writes into the wrong repo or fails at step 5 → S08-W1-1 (W1) |
| plugin-creator-2 | M | `SKILL.md:57-59` | scaffold's "Always" list has no README/CHANGELOG/evals; `templates/evals.json` unreferenced → S08-W3-4 (W3) |
| plugin-creator-3 | M | `authoring-rules.md:33` vs `plugin-creator SKILL.md:3` "Scaffold…"/`refine-plugin :3` "…fixes you approve" | both descriptions break their own third-person rule → S08-W3-2/3 (W3) |
| plugin-creator-4 | M | `SKILL.md:3` "hand-edit the files, then run bump.py" | misroutes edits to manual editing instead of `refine-plugin` → S08-W3-2 (W3) |
| plugin-creator-5 | M | `refine-plugin SKILL.md:58-68`; `audit-checklist.md:67-68` requires one entry/version | bumps with no CHANGELOG step → S08-W3-6 (release.py) (W3) |
| plugin-creator-6 | M | `templates/SKILL.md:2,8`; re-verified: `ConstructorError: found unhashable key` line 1 col 7 | `{{PLACEHOLDER}}` invalid YAML → half-filled breaks frontmatter → S08-W3-5 (W3) |
| plugin-creator-7 | M | `templates/hooks.json:9` bare `{{SHELL_COMMAND…}}`; no `${CLAUDE_PLUGIN_ROOT}` in refs | relative hook path breaks after install → S08-W3-5 (W3) |
| plugin-creator-8 | M | `authoring-rules.md:49-52` requires type+url; `validate.py:93` fails `{command,args}` (reproduced) | forbids stdio, which CC accepts; no `mcpServers` guidance → S08-W3-5/6 (W3) |
| plugin-creator-9 | L | `SKILL.md:65` vs `authoring-rules.md:45` | contradict on hooks descriptions → S08-W3-5, moot post-rewrite (W3) |
| plugin-creator-10 | L | `SKILL.md:63-64` "expand with more trigger phrasings" | length floor encourages padding → S08-W3-2, no floor (W3) |
| plugin-creator-11 | L | `plugin.json` 9 keywords vs `audit-checklist.md:60` "3–6"; entry has 5 + a different description | breaks own checklist, drifts from catalog → S08-W3-1 (W3) |
| plugin-creator-12 | L | `CLAUDE.md:58` mandates a step `SKILL.md` lacks; gridgeist missing from its list | scaffold skips repo bookkeeping → I19's generated-surfaces check (S08-W3-1) + S10-W3-8 (I24); no S08 SKILL change → S10-W3-8 (W3) |
| plugin-creator-13 | L | `authoring-rules.md` covers only names/versions/entry/description/MCP/layout | omits name limits, body-size, refs-one-level, dmi, `${CLAUDE_PLUGIN_ROOT}`, `dependencies` → S08-W3-5 (W3) |
| plugin-creator-14 | L, H07 share | `commands/route.md:6` reads `ROUTING.md`, `:9` says regenerate it first | writes to answer a read-only question → S08-W3-7, retire, R91 (W3) |

Count: **14/14** assigned. plugin-creator-12 carries no `S08-W…` step (fix is I19's own check + S10's file).

### 1.4 Other findings

- OBS coupling: tools outside the plugin dir, uncopied on install — H07's cause; W1 stops it, W3 closes.
- OBS validation split: `--strict`/`validate.py` check disjoint things (CLI: YAML/fields/hooks/author; `validate.py`: length/parity). I19 = "strict PLUS what it misses".
- OBS description saturation (marketplace-wide): 10/17 descriptions ≥990 chars — I19's R6 check, not new work here.
- OBS evals: 0 cases shipped despite an unused `evals.json` template — closed S08-W3-8.
- OBS portability (marketplace-wide): `intent-lock/skills/intent-lock/SKILL.md` fails `yaml.safe_load` today — surfaces as a ratchet entry (S12).
- OBS broken links: `validate.py` passes while other plugins reference uncommitted files — the VAL-07 case.
- NEW: neither `plugin-creator/` nor `firecrawl/` ships a `LICENSE` — VAL-11 requires one, added W3.

## 2. Target state

### 2.1 Location and tree (after W3)

```
plugins/plugin-creator/
  .claude-plugin/plugin.json   $schema,version,author,keywords(3-6); hooks:"./hooks/hooks.json"
  README.md  CHANGELOG.md  LICENSE
  hooks/hooks.json              SessionStart, remote-only, sets core.hooksPath (§2.6)
  scripts/
    validate.py  release.py     self-contained (I19 §2.5); no repo-root calls
    test_validate.py  test_release.py
  skills/
    plugin-creator/SKILL.md     model-invocable; house shape (I20)
      references/authoring-rules.md   rewritten (R1-18,23,30,32-37,41,44-49,54,56-58)
      references/templates/{plugin,marketplace-entry,SKILL,agent,alias-skill}.{md,json} {hooks,.mcp}.json
        (command.md, evals.json DROPPED — R34, R70)
    new-plugin/SKILL.md         dmi alias → plugin-creator (OD9-a)
    refine-plugin/SKILL.md      dmi (OD10-a); house shape
      references/audit-checklist.md   quality tier, trimmed of now-mechanical items
  evals/
    plugin-creator/{trigger-basic,negative-edit-existing,scaffold-output}/
    refine-plugin/{explicit-invoke,negative-new-plugin,fix-then-release}/
```

Removed: `commands/` (all 3), `templates/{command.md,evals.json}`. Repo-root
`validate.py`/`bump.py` gone (moved+renamed); `route.py`/`ROUTING.md` deleted.

### 2.2 Frontmatter

**`plugin-creator`** (model-invocable):
```yaml
---
name: plugin-creator
description: >-
  Scaffolds a new plugin into the micky-psych-tools marketplace — manifest, component
  skeleton, catalog entry, and validation, all in one pass. Use when the user says "make
  me a plugin", "create a plugin", "scaffold a plugin", "scaffold a skill/agent", "new
  plugin", "add a plugin to the marketplace", or runs /new-plugin. Elicits a short fixed
  checklist (name, purpose, component type, trigger phrases, category) first, then
  generates plugin.json, README, CHANGELOG, LICENSE, the chosen component (skill, agent,
  hooks, or MCP wiring — never a command) with one trigger-basic eval case, registers it
  in marketplace.json, and runs validate.py so the result passes every rule on the first
  try. Not for editing, refining, or versioning an EXISTING plugin (use refine-plugin),
  and not for installing, enabling, or managing plugins (Claude Code's built-in /plugin
  command).
metadata:
  profile: cc
---
```
Measured: 866 chars/216 tok, `Use when` @142, `Not for` @690, no `I/you/your`,
`has_angle_brackets: false`. A prior draft's procedural detail before `Use when` pushed its
offset to 460 (over R4's ~250), and its `<skill>` eval mention broke R3/R5's `<>` ban — both
caught by re-running `measure.py text` on the final draft, not assumed.

**`new-plugin`** (dmi alias, OD9-a):
```yaml
---
name: new-plugin
description: Alias for plugin-creator:plugin-creator. Not model-invoked; typed directly as /new-plugin.
disable-model-invocation: true
argument-hint: [optional one-line plugin idea]
metadata:
  profile: cc
---
```

**`refine-plugin`** (dmi, OD10-a):
```yaml
---
name: refine-plugin
description: >-
  Audits an existing plugin or skill in the micky-psych-tools marketplace and applies
  approved fixes. Use when the user says "improve my plugin", "refine this skill", "audit
  my plugin", "fix version parity", "polish this skill", or runs /refine-plugin. Reports
  findings in two ranked tiers — mechanical blockers (version parity, kebab-case, semver,
  description length, MCP type/url, frontmatter name==directory) and quality/triggering
  (weak description, missing Not-for, absent trigger phrases, bloated procedure) — each
  with a before/after fix, applies only the fixes the operator approves, then releases
  through release.py (plugin.json bump + CHANGELOG entry) and validates. Not for creating
  a new plugin (use plugin-creator), or installing, enabling, or managing plugins (Claude
  Code's built-in /plugin command).
disable-model-invocation: true
metadata:
  profile: cc
---
```
Measured: 813 chars/203 tok, `Use when` @100, `Not for` @675, third person,
`has_first_or_second_person: false`. Same R4 fix as plugin-creator's description above
(a prior draft's `Use when` sat at offset 479): capability outcome first, procedure after.

### 2.3 Body outline

**`plugin-creator/SKILL.md`** (target ≤3,800 chars / ≤950 tok):

| Source | Target | Action |
|---|---|---|
| `:1-14` intro | Intro | keep, trim to 2 sentences |
| `:16-21` Scope | `## Scope` | keep; Not-for → `refine-plugin` (fixes -4) |
| — | `## 0. Guard — repo root` | new: MICKY_TOOLS_DIR → marker, else stop (H07; lands W1, kept W3 with new script paths) |
| `:27-45` Elicit | `## 1. Elicit` | keep; component list drops `command` (R34) |
| `:47-51` Guard-name | `## 2. Guard — name` | keep, renumbered |
| `:53-65` Scaffold | `## 3. Scaffold` | rewrite: adds README/CHANGELOG/LICENSE/one eval case (-2); drops 200-char floor language (-10); points at `alias-skill.md` |
| `:67-71` Register | `## 4. Register` | keep; entry drops `version` (I24, S10) |
| `:73-82` Validate | `## 5. Validate` | keep; `${CLAUDE_PLUGIN_ROOT}/scripts/validate.py --repo .` |
| `:84-86` router refresh | — | cut (R91) |
| `:88-95` stop-before-commit | `## 6. Stop before commit` | keep, drops `ROUTING.md` |
| — | `## Not for` | keep, rewritten (-4) |
| — | `## Gotchas` | new (R23): placeholders pre-filled programmatically; stdio MCP now allowed |

**`refine-plugin/SKILL.md`** (target ≤3,200 chars / ≤800 tok):

| Source | Target | Action |
|---|---|---|
| `:1-14` intro | Intro | keep, third person |
| `:16-21` Scope | `## Scope` | keep |
| `:23-36` Select+Guard | `## 1-2` | keep |
| `:38-51` Audit | `## 3. Audit` | keep; points at shared `authoring-rules.md` |
| `:53-56` Apply | `## 4. Apply` | keep |
| `:58-68` Bump | `## 5. Release` | rewrite: `release.py <plugin> <level>` writes the CHANGELOG entry in the same step (-5); `--write` required, dry run otherwise |
| `:70-74` router refresh | — | cut (R91) |
| `:76-83` stop-before-commit | `## 6.` | keep |
| — | `## Gotchas` | new: out-of-marketplace target is audit-only, never call `release.py` |

### 2.4 References

| File | Purpose | Load condition | Size target |
|---|---|---|---|
| `references/authoring-rules.md` | mechanical rules both skills cite | "Read before writing" / "for the blocker tier" | ≤2,500 chars |
| `references/templates/*` | fill-in-the-blank skeletons | conditional, per component | `SKILL.md` +40 chars (quoted); new `alias-skill.md` ~250 chars |
| `references/audit-checklist.md` | quality tier | "Read for the quality tier" | ≤3,800 chars (mechanical items moved out) |

### 2.5 Scripts

#### `scripts/validate.py` (I19, owned)

```
validate.py --repo <path> [--cross-repo <path>]
validate.py --repo <path> --versions [--json <out>]
validate.py --repo <path> --fix-seams [--write]
validate.py --help
```
- `--repo` auto-detects profile by marker (micky `marketplace.json` name; learn-hub
  `package.json` name + `apply-sync.mjs`); profile-scopes checks (VAL-10/11/12 micky-only).
- `--cross-repo <path>`: also runs VAL-14 (both clones present), else a note, not a fail.
- `--versions`: `plugin | version | source` per plugin.json (`--json`: `[{name,version,source}]`) — replaces MEMORY.md's hand table (R88).
- `--fix-seams [--write]`: dry run by default; `--write` applies ONLY a missing `$schema`;
  a missing README/CHANGELOG/LICENSE stub when **entirely absent** (never overwrites); a
  missing `evals/results/` `.gitignore` line. Never touches description/version/body text/deletes.
- Exit: `0` clean/ratcheted-only; `1` a new failure; `2` usage error.
- `--json <out>`: `[{id,severity,path,message,ratcheted}]` alongside the PASS/FAIL stream.

**Check table.** `rule` cites the rubric ids it enforces verbatim (full rule text:
`docs/plugin-rewrite/rubric.md`, already read this session — not restated here) plus
whatever this design adds beyond the rubric (exact source of the committed lists, message
shape). Ratchet/trigger-lock reading and writing goes through S12's own library functions
(`rewrite_gate.py` for Python, imported — not reimplemented, CX-19): `ratchet.json` is
`{generated_at, repo, entries:[{check_id,path,message}]}`, `triggers.lock.json` is
`{phrases:[{phrase,kind,skill,field}], removed:[]}` — §8 Q1 closed, no longer an ASSUMES.

| id | rule (R = rubric.md id) | input | message | sev | ratchet (`↑`=same R-id as `rule`) |
|---|---|---|---|---|---|
| VAL-01 | R29: `claude plugin validate --strict --json` on marketplace root, every `plugins/<p>/`, learn-hub `.claude/skills` | shell out | `"<dir>: strict validate failed: <stderr>"` | fail | none |
| VAL-02 | R2: `yaml.safe_load` on every frontmatter; no `{{…}}` outside `templates/` | frontmatter | `"<path>: fails strict YAML"` / `"…: leftover {{"` | fail | ↑ |
| VAL-03 | R1: name charset/length/kebab/reserved words; R7: unique across both repos + `synced-names.md` | name fields | `"<path>: name '<n>' fails R1"` | fail | none |
| VAL-04 | R3-5: description order/offset/pronouns/`<>`/length; CX-18 exempts a dmi alias (`disable-model-invocation: true` + an `Invoke …`-only body) from the order/`Use when` rules, capping its description at 150 chars instead | description | `"<path>: description <reason>"` | fail (len/order/pronoun/`<>`); warn (>600) | ↑ |
| VAL-05 | R8: reciprocal `Not for`, pairs from `sibling-pairs.md` | description + pairs | `"<a> names <b>, not reverse"` | fail | ↑ |
| VAL-06 | R78 support: locked `quoted_phrases` still present, else an explicit removal | phrases vs lock | `"<skill>: dropped '<p>'"` | fail | reads `triggers.lock.json` via S12's `scripts/lib/rewrite-gate.mjs` functions, imported not reimplemented (CX-19; §8 Q1 closed) |
| VAL-07 | R11,13,15: body size, gate-skill cap, link resolution, `## Contents` | body + links | `"<path>: body N tok>5000"` / `"…: unlinked <f>"` | fail | ↑ |
| VAL-08 | R32,44,46,47,49: no PLUGIN_ROOT `..`/writes, no OS-specific paths (exc. `learn-hub-session/hooks/run.sh`), interpreter-prefixed scripts; R41: no `mcp__plugin_` prefix | body grep | `"<path>: <match>"` | fail | none |
| VAL-09 | R56-58: no `dependencies`; every cross-plugin mention carries `OPTIONAL` + the §4.2 fallback within 2 lines | plugin.json + body | `"<path>: <p:s> no fallback"` | fail | ↑ |
| VAL-10 | R34: no `commands/`; R35: alias/listed skills carry dmi (`dmi-skills.md`), alias body ≤10 lines; R37: `fork-denylist.md` skills never `context: fork` | dir+frontmatter+body | `"<plugin>: has commands/"` / `"…: alias no dmi"` | fail | ↑ |
| VAL-11 | R30: plugin.json shape, `defaultEnabled` list; R33: marketplace entry shape, no version, description parity; R83/87: version/renames; R45: README+LICENSE+CHANGELOG present; R85: CHANGELOG top == version (a leading `## Unreleased` section is skipped, OQ12-a) | plugin.json+marketplace.json+dir listing | `"<path>: <field> <reason>"` | fail | ↑ |
| VAL-12 | R70-72,76: ≥3 cases/skill, ≥1 outcome+process grader/case, no `evals.json`, `evals/results/` gitignored, runner present | `evals/` tree | `"<skill>: N case(s)"` / `"…: no process grader"` | fail | ↑, ratchet to W3/W4 |
| VAL-13 | R88,90,92: no mandated-read grep, no hand-maintained version table, micky CLAUDE.md/MEMORY-living ≤2,000 tok each | file text | `"<path>: <reason>"` | fail | ↑ |
| VAL-14 | (`--cross-repo`, both clones) sink.py names the two inbox paths exactly; fixtures parse under `check-contract.mjs`: `node "$LEARN_HUB_DIR/scripts/check-contract.mjs" --dir "$MICKY_TOOLS_DIR/plugins/evidence/evals/fixtures" --json`, fail on exit 1 (I25, CX-20); no `check-html.mjs` parity check (OQ13-a) | run + diff | `"<file>: <v1> vs <v2>"` | fail (both present); warn (else) | none |
| VAL-15 | R68: every `plugins/*/scripts/*` has an adjacent passing test file | run suites | `"<script>: no test"` / `"<n> failure(s)"` | fail | ↑ |
| VAL-16 | R54: `metadata.profile` set; `portable` uses only the 6 spec keys, no `` !`cmd` ``, no `<>` | frontmatter+body | `"<path>: <reason>"` | fail | ↑ |

Unit tests (`scripts/test_validate.py`): one fixture pair (`good`/`bad-<id>`) per VAL-id under
`scripts/fixtures/`; `--help` exits 0, no writes; `--fix-seams` w/o `--write` makes no change;
`--fix-seams --write` never touches an existing non-empty file. `python3 -m unittest discover
-s plugins/plugin-creator/scripts -p 'test_*.py'` (wired into `health.sh`, S10, I18).

#### `scripts/release.py` (I19, owned)

```
release.py <plugin> patch|minor|major [--write]
release.py --help
```
- Dry run by default: prints new version, plugin.json diff, CHANGELOG entry; exits 0, no write.
- `--write`: runs `validate.py --repo <root>` first (failure → print+exit 1, no write). On
  success edits plugin.json `version` (UTF-8, trailing newline), turns a leading `## Unreleased`
  section of CHANGELOG.md into `## x.y.z — <date>` (keeping its entries; OQ12-a), or, when there
  is none, prepends `## x.y.z — <date>` + the operator's summary, re-validates, prints `claude plugin tag <plugin>
  --dry-run`. Never edits marketplace.json (R83).
- Exit: `0` success; `1` pre-write validation failed or post-write CHANGELOG mismatch (rolled
  back); `2` usage error; `3` plugin not in the marketplace.
- `--json`: `{"plugin","old","new","changelog_path","written"}`.

Unit tests (`scripts/test_release.py`, ≥8 cases): dry run writes nothing; `--write` success
(both files updated, UTF-8, trailing newline); unknown plugin exits 3; invalid level exits 2;
pre-write validation failure blocks the write; printed tag line matches `<plugin>--v<version>`;
missing CHANGELOG.md fails loudly, never silently skips (closes -5).

### 2.6 Handoffs

None owed at runtime — plugin-creator/refine-plugin are self-contained meta-tooling with no
cross-plugin `OPTIONAL` calls. Received: `refine-plugin`'s own guard already hands off to
`/new-plugin` when the target doesn't exist; `plugin-creator` gains the mirror line for edits
(-4, §2.3).

`hooks/hooks.json` (this plugin's own SessionStart hook, architecture §2.2/§10 W3):
```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command",
        "command": "test \"$CLAUDE_CODE_REMOTE\" = \"true\" && test -n \"$MICKY_TOOLS_DIR\" && grep -q '\"name\": \"micky-psych-tools\"' \"$MICKY_TOOLS_DIR/.claude-plugin/marketplace.json\" 2>/dev/null && cd \"$MICKY_TOOLS_DIR\" && [ -z \"$(git config --get core.hooksPath)\" ] && git config core.hooksPath .githooks; exit 0"
      } ] }
    ]
  }
}
```
Remote-only (`CLAUDE_CODE_REMOTE`, matching architecture §2.2's "Cloud, single-repo micky:
plugin-creator hook sets core.hooksPath"); marker-checked; sets `core.hooksPath` only when
unset (a local override survives); exits 0 unconditionally (same rule as I14, S13).

### 2.7 Interfaces

#### I19 — Final validator and release tool (owned)

Fully defined in §2.5: `validate.py` (modes `--repo`, `--cross-repo`, `--versions`,
`--fix-seams`; VAL-01..16) and `release.py`. `scripts/health.sh` (S10, I18) calls
`validate.py --repo .` (+ `--cross-repo $LEARN_HUB_DIR` when it resolves) as its first step.

#### I20 — Skill house shape (owned)

**Frontmatter whitelist**: `name`, `description`, `metadata` (`profile: cc|portable`),
`disable-model-invocation`, `user-invocable`, `allowed-tools`, `context` (`fork`, denylisted
for alignment, VAL-10), `argument-hint` (any user-typeable skill, not only alias skills —
CX-18, matching architecture §3.3's move of argument handling to the target skill), `license`,
`compatibility` (`portable` only). Unknown keys fail under `--strict` (VAL-01).

**Description** = third-person capability clause (concrete nouns, no steps/engines/output
mechanics) + `Use when …` (verbatim phrases) + `Not for … (use <plugin:skill>)` naming every
sibling. ≤1,024 hard, ≤600 soft. No bare `I/you/your/my/we`, no `<>`. **Exception** (CX-18): a
skill with `disable-model-invocation: true` and a body that is only an `Invoke …` sentence
(a dmi alias) is exempt from the order/`Use when` rules — its description need only state what
it aliases, ≤150 chars.

**Body**: standing rules first (R12); numbered procedure; conditional reference pointers
(R14); `## Gotchas` last (R23); no version narration (R18). ≤500 lines/≤5,000 tok; a sub-step
"gate" skill SHOULD be ≤2,000 tok.

**Alias skill template** (`references/templates/alias-skill.md`, new — closes the OD9 gap;
every placeholder quoted, CX-18 — an unquoted `{{…}}` is what plugin-creator-6 broke on):
```markdown
---
name: "{{ALIAS_NAME}}"
description: "Alias for {{PLUGIN}}:{{SKILL}}. Not model-invoked; typed directly as /{{ALIAS_NAME}}."
disable-model-invocation: true
argument-hint: "[{{ARG_HINT}}]"
metadata:
  profile: cc
---

Invoke `{{PLUGIN}}:{{SKILL}}` with: $ARGUMENTS
```

**Consumed (ASSUMES unless noted; owner to confirm):**

| Interface | Owner | Assumption |
|---|---|---|
| I16 | S11 | plugin-creator joins `CLAUDE_CODE_PLUGIN_DIRS` at W1 exit (V2) once H07 closes and the smoke suite passes (I16.3 #4); this spec's W1 step is a dependency of S11's edit, not an env-var change itself. |
| I17 | S12 | Case layout `plugins/plugin-creator/evals/<skill>/<case>/`; tags `smoke\|trigger\|negative\|output\|release`; trigger-grader regex per §4.1; `ratchet.json`/`triggers.lock.json` formats (VAL check ratchet keys); committed lists `sibling-pairs.md`/`gate-skills.md`/`dmi-skills.md`/`fork-denylist.md`; `scripts/eval.sh` flags (§4.4). |
| I18 | S10 | S10's W0-fixed `validate.py`/`bump.py` (guarded loads, counted checks, `yaml.safe_load`, stdio allowed) is what S08-W3-1 moves, not today's version (§1.1). |
| I24 | S10 | marketplace.json entries carry `{name,source,category,keywords}` (no version) from W0, gain `$schema`/`renames` at W3, no later than S08-W3-1. |
| I25 | S15 | `check-contract.mjs` invoked as `node "$LEARN_HUB_DIR/scripts/check-contract.mjs" --dir "$MICKY_TOOLS_DIR/plugins/evidence/evals/fixtures" --json` (CX-20 — the CLI takes `--dir`/`--json`, no positional argument), non-zero exit (1) on parse failure. |

## 3. Change steps

`$VALIDATE` = `python3 plugins/plugin-creator/scripts/validate.py` (once S08-W3-1 lands). Every "Rollback: `revert`" below means `git revert <this commit>`.

### W0

**S08-W0-1** · depends on: S12-W0-3
- Files: create `plugins/plugin-creator/evals/{plugin-creator,refine-plugin}/<case>/{prompt.md,graders/*.md}` (3 cases per skill; I17 layout; every `prompt.md` carries `smoke` in `tags`; each case directory takes the name of one of §4.1's cases, so the later eval step extends these directories instead of adding new ones (critique P2, P7)).
- Change: seed the pre-rewrite smoke baseline for both skills.
- Commands / done when: S12-W0-5's check, run once per skill — `find . -path '*/evals/plugin-creator/*' -name prompt.md | xargs grep -l 'tags:.*smoke' | wc -l` ≥ 3, and the same for `refine-plugin` ≥ 3.
- Rollback: `git rm -r plugins/plugin-creator/evals/plugin-creator plugins/plugin-creator/evals/refine-plugin`.

### W1

**S08-W1-1 · micky · plugin-creator root guard (H07)**
- Depends on: none.
- Files: edit `skills/plugin-creator/SKILL.md`, `skills/refine-plugin/SKILL.md`.
- Change: insert as the first Procedure step in each (refine-plugin's existing `## 2. Guard`
  gains the same check ahead of its target-existence check):
  ```markdown
  ## 0. Guard — repo root

  Resolve root: `MICKY_TOOLS_DIR` if set and its `.claude-plugin/marketplace.json` has
  `"name": "micky-psych-tools"`; else STOP: "This skill only works inside the
  micky-psych-tools marketplace repo. Set MICKY_TOOLS_DIR, or run from that checkout."
  Write nothing. No cwd walk-up (CX-57 — architecture §3.2's W1 guard is
  `MICKY_TOOLS_DIR` → marker, else stop; R47 forbids the walk-up this draft had). Later
  script calls run from the resolved root.
  ```
  Everything else, incl. today's repo-root script paths, is unchanged (interim fix).
- Commands: `python3 -c "import yaml; yaml.safe_load(open('plugins/plugin-creator/skills/plugin-creator/SKILL.md',encoding='utf-8').read().split('---')[1])"` ; `grep -c "Guard — repo root" plugins/plugin-creator/skills/plugin-creator/SKILL.md plugins/plugin-creator/skills/refine-plugin/SKILL.md`
- Done when: both greps print `1`; `python3 scripts/validate.py` still prints `all checks passed`.
- Rollback: `revert`.

**S08-W1-2 · DROPPED (OQ12-a): micky · release the W1 fix.** Windows loads plugins in place from W1 entry (S11-W3-2), so this interim version bump is not needed; the change steps write their CHANGELOG entries under `## Unreleased`, and `release.py` sets the version once at W3.
- Depends on: S08-W1-1.
- Commands: `python3 scripts/bump.py plugin-creator patch --write` (CX-12).
- Files: `plugin.json`, `CHANGELOG.md` (entry: "Root guard: stop instead of writing into the wrong repo (H07 interim fix)."). `.claude-plugin/marketplace.json` is NOT touched — S10-W0-3 has already stripped entry versions from it (CX-12).
- Done when: `python3 scripts/validate.py` prints `all checks passed`; `plugin.json` version is `0.3.1`; `marketplace.json`'s `plugin-creator` entry carries no `version` key.
- Rollback: `revert`.

### W3

**S08-W3-1 · micky · self-contained scripts + manifest + health.sh**
- **Changed ahead of wave (2026-09-26, plugin-creator 0.3.1):** repo-root `scripts/validate.py` gained a per-plugin check that fails on any `SKILL.md` (any case) outside `skills/<skill>/` — a surface loaded the nested `templates/SKILL.md` as a live skill `skill-name` — with 3 tests in `scripts/test_validate.py`. Keep the check and its tests when commit (b) moves the validator into `plugins/plugin-creator/scripts/`.
- Depends on: S08-W1-1; S10-W0-1, S10-W0-2, S10-W0-3 (S10's W0-fixed `validate.py`/`bump.py` and entry-version strip, CX-34); S10-W3-2 (the skeleton move — CX-36); S11-W0-3 (both this step and S11-W0-3 edit `scripts/health.sh` — CX-39); S10-W0-8.
- Files: create `plugins/plugin-creator/scripts/{validate.py,release.py,test_validate.py,test_release.py}`; create `plugins/plugin-creator/references/lists/{synced-names,sibling-pairs,dmi-skills,fork-denylist,gate-skills}.md` (CX-21 — this spec owns these committed lists; derived from architecture §2.8 for synced names, §6.3's families for sibling pairs, OD9/OD10 for dmi skills, §8 for the fork denylist and gate skills); edit (not create — S10-W0-8 already backfills a LICENSE for every plugin that lacks one, CX-45) `plugins/plugin-creator/LICENSE` if S10-W0-8's text needs a plugin-creator-specific tweak, otherwise leave it untouched; edit `plugin.json` (`$schema`, keywords trimmed to 5, `hooks: "./hooks/hooks.json"`); delete repo-root `scripts/validate.py`, `scripts/bump.py`; edit `scripts/health.sh` (CX-11) to call `python3 plugins/plugin-creator/scripts/validate.py --repo .` (+ `--cross-repo "$LEARN_HUB_DIR"` when set), a per-directory unittest loop — `for d in plugins/*/scripts; do ls "$d"/test_*.py >/dev/null 2>&1 || continue; out=$(python3 -m unittest discover -s "$d" -p 'test_*.py' 2>&1) || { echo "$out"; exit 1; }; case "$out" in *'Ran 0 tests'*) echo "health: no tests ran in $d"; exit 1;; esac; done` (critique P3: `discover -s plugins` finds no test under `plugins/*/scripts/`, which have no `__init__.py`, and prints `Ran 0 tests … OK`), `node --test 'plugins/*/scripts/*.test.mjs'` — keeping S11-W0-3's two existing lines, not replacing them.
- Commands: `python3 plugins/plugin-creator/scripts/validate.py --help` ; `python3 -m unittest discover -s plugins/plugin-creator/scripts -p 'test_*.py' -v` ; `$VALIDATE --repo .` ; `bash scripts/health.sh --fast` ; `ls plugins/plugin-creator/references/lists`
- Done when: `--help` exits 0, no writes; unittest ends `OK`; `--repo .` reports pre-existing violations as ratchet entries, not hard failures; `health.sh --fast` exits 0; `bash scripts/health.sh` runs the loop and prints the test count of every `plugins/*/scripts` directory that holds `test_*.py`; all 5 list files exist.
- Commit shape (critique C2-13): one PR of four commits, each green under `bash scripts/health.sh --fast`, in this order: (a) the five list files; (b) `validate.py` + `test_validate.py`, with `rewrite_gate.py ratchet seed --new` for the new check ids; (c) the `health.sh` switch; (d) `release.py` + `test_release.py`, the `plugin.json` and LICENSE edits, and the deletion of root `scripts/validate.py` and `scripts/bump.py`. Review each commit on its own. The done-when above is checked after (d).
- Rollback: `revert` (the PR merge, or the last commits from (d) backwards).

**S08-W3-2 · micky · rewrite `plugin-creator/SKILL.md`**
- Depends on: S08-W3-1, S12-W3-2.
- Files: edit `skills/plugin-creator/SKILL.md` per §2.2/§2.3 in full.
- Commands: YAML-parse check (as W1-1) ; `$VALIDATE --repo .`
- Done when: YAML parses; `validate.py` no longer lists this file's failures.
- Rollback: `revert`.

**S08-W3-3 · micky · rewrite `refine-plugin/SKILL.md` + create `new-plugin` alias**
- Depends on: S08-W3-1, S12-W3-2.
- Files: edit `skills/refine-plugin/SKILL.md`; create `skills/new-plugin/SKILL.md` (§2.2 + `Invoke \`plugin-creator:plugin-creator\` with: $ARGUMENTS`); trim `references/audit-checklist.md` (drop now-mechanical bullets).
- Commands: `$VALIDATE --repo .`
- Done when: 0 failures for this plugin's non-eval checks.
- Rollback: `revert`.

**S08-W3-4 · micky · scaffold output gains README/CHANGELOG/LICENSE/evals; own README gains `## Surfaces`**
- Depends on: S08-W3-2.
- Files: add `templates/{readme.md,changelog.md,license.md}` stubs; extend `SKILL.md`'s
  `## 3. Scaffold` to write them plus `evals/<skill>/trigger-basic/` (one case; the operator
  adds cases 2-3 by hand, noted in the body); edit this plugin's OWN `README.md` to add a
  `## Surfaces` section naming every place its own summary appears (I16 item 1, CX-49).
- Commands: `$VALIDATE --repo .`; `grep -c "^## Surfaces" README.md`
- Done when: 0 failures; the grep = 1.
- Rollback: `revert`.

**S08-W3-5 · micky · templates fixed (valid YAML, no command template, alias template, hooks/MCP guidance)**
- **Changed ahead of wave (2026-09-26, plugin-creator 0.3.1):** `templates/SKILL.md` is now `templates/SKILL.template.md` (why: S08-W3-1's note). Read every `templates/SKILL.md` in this spec's target sections (§2.1, §2.4, this step, §5 item 4) as `templates/SKILL.template.md`; no template may be named `SKILL.md` again (validate.py fails on it).
- Depends on: S08-W3-1.
- Files: `templates/{SKILL.md,agent.md}` (quote placeholders), `templates/alias-skill.md` (new), delete `templates/{command.md,evals.json}`, `authoring-rules.md` (MCP + Hooks sections, missing best practices) — per §2.4/§1.3 (-6,-7,-8,-13) in full.
- Commands: YAML-parse `templates/SKILL.md` (now succeeds, was `ConstructorError`) ; `find plugins/plugin-creator/skills/plugin-creator/references/templates -name 'command.md' -o -name 'evals.json'` (expect empty).
- Done when: both commands confirm.
- Rollback: `revert`.

**S08-W3-6 · micky · MCP wiring guidance in the scaffold step**
- Depends on: S08-W3-5.
- Files: edit `SKILL.md`'s `## 3. Scaffold` — for `mcp-wiring`, also add `"mcpServers": "./.mcp.json"` to `plugin.json` (the template omits it, conditional on component choice).
- Commands: `$VALIDATE --repo .`
- Done when: 0 failures; closes -8's second half.
- Rollback: `revert`.

**S08-W3-7 · micky · retire `/route` and this plugin's own `commands/` (CX-15 — scope narrowed)**
- Depends on: S08-W3-2, S08-W3-3; S10-W0-4 (S10's W0 `route.py` fix, I18, cited per architecture §3.4 "fix W0 … retire W3").
- Files: delete `plugins/plugin-creator/commands/` (all 3) and route mentions inside `plugin-creator`'s own files (`SKILL.md`, `README.md`). Does **not** delete `scripts/route.py` or `ROUTING.md` — S10-W3-9 is the sole deleter of both (CX-15 — deleting them here, before S10's CLAUDE.md rewrite lands, would leave CLAUDE.md naming files that no longer exist).
- Commands: `grep -rn "route.py\|ROUTING.md" plugins/plugin-creator/` (expect 0) ; `test -f scripts/route.py` (still succeeds — this step does not touch it) ; `$VALIDATE --repo .`
- Done when: the grep is empty; `route.py`/`ROUTING.md` still exist; validator clean.
- Rollback: `revert`.

**S08-W3-8 · micky · eval conversion**
- Depends on: S08-W3-2, S08-W3-3.
- Files: create the 6 case dirs in §4.1 in full; confirm no `evals.json` remains.
- Commands: `find plugins/plugin-creator -iname 'evals.json'` (empty) ; `$VALIDATE --repo .`
- Done when: both confirm; the `R70-72,76:plugins/plugin-creator` ratchet entry is removed in the same commit (coordinate with S12).
- Rollback: `revert`.

**S08-W3-9 · micky · release the W3 rewrite**
- Depends on: S08-W3-1 … S08-W3-8.
- Commands: `python3 plugins/plugin-creator/scripts/release.py plugin-creator minor --write`
- Files: `plugin.json` (`0.3.1`→`0.4.0`), `CHANGELOG.md` (summarizes the move, template fix, dmi, router retirement). Wave exit: note, per S11's I16 item 4 template: "Ready for cloud delivery: HIGH defects due by this wave closed (H07); handoffs carry the §4.2 fallback or target an enabled plugin; no same-named unit elsewhere; smoke suite passed (<result path>)."
- Done when: post-write `validate.py` prints `all checks passed`; the marketplace entry carries no `version` (I24).
- Rollback: `revert`.

## 4. Evals

### 4.1 Cases

**`plugin-creator` case 1, `trigger-basic` (trigger positive):**

`evals/plugin-creator/trigger-basic/prompt.md`
```markdown
---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
tags: [trigger, smoke]
---

I want to add a plugin to the marketplace that turns a DOI into a formatted citation.
Scaffold it for me.
```
`evals/plugin-creator/trigger-basic/graders/skill-fired.md`
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?plugin-creator"'
weight: 2
---
```
`evals/plugin-creator/trigger-basic/graders/elicits-checklist.md`
```markdown
---
type: regex
target: last_message
pattern: '(kebab|name).{0,80}(purpose|category|trigger)'
flags: is
---
```

**`plugin-creator` case 2, `negative-edit-existing` (near-miss negative):**

`evals/plugin-creator/negative-edit-existing/prompt.md`
```markdown
---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
tags: [negative]
---

The description on my existing vault-keeper plugin is weak and doesn't mention its
Not-for clause. Can you tighten it up?
```
`evals/plugin-creator/negative-edit-existing/graders/no-plugin-creator.md`
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?plugin-creator"'
min: 0
max: 0
arm: both
---
```

**`plugin-creator` case 3, `scaffold-output` (output/process):**

`evals/plugin-creator/scaffold-output/prompt.md`
```markdown
---
max_turns: 20
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, "Bash(python3 *)"]
tags: [output]
---

Scaffold a new plugin called "citation-format": a skill that formats a DOI into APA or
Vancouver style. Category "productivity". Trigger phrases: "format this citation", "cite
this DOI". Use sensible defaults for anything else — don't ask me more questions.
```
`evals/plugin-creator/scaffold-output/graders/required-files.md`
```markdown
---
type: file_exists
path: "plugins/citation-format/.claude-plugin/plugin.json"
exists: true
---
```
`evals/plugin-creator/scaffold-output/graders/no-command-dir.md`
```markdown
---
type: file_exists
path: "plugins/citation-format/commands/**"
exists: false
---
```
`evals/plugin-creator/scaffold-output/graders/validate-order.md`
```markdown
---
type: tool_order
before: { tool: Write, input_match: "citation-format/.claude-plugin/plugin.json" }
after: { tool: Bash, input_match: "validate\\.py" }
weight: 2
---
```

**`refine-plugin` case 1, `explicit-invoke` (dmi — direct-invocation trigger case per §6.2's
gate/dmi pattern, not an unprompted-trigger case):**

`evals/refine-plugin/explicit-invoke/prompt.md`
```markdown
---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
tags: [trigger, smoke]
---

Run refine-plugin on the firecrawl plugin — audit it for anything weak.
```
`evals/refine-plugin/explicit-invoke/graders/skill-fired.md`
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?refine-plugin"'
weight: 2
---
```
`evals/refine-plugin/explicit-invoke/graders/two-tiers.md`
```markdown
---
type: regex
target: last_message
pattern: '(blocker|mechanical).{0,400}(quality|trigger)'
flags: is
---
```

**`refine-plugin` case 2, `negative-new-plugin` (near-miss negative):**

`evals/refine-plugin/negative-new-plugin/prompt.md`
```markdown
---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
tags: [negative]
---

I need a brand-new plugin for summarizing lab results. Nothing like it exists yet.
```
`evals/refine-plugin/negative-new-plugin/graders/no-refine-plugin.md`
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?refine-plugin"'
min: 0
max: 0
arm: both
---
```

**`refine-plugin` case 3, `fix-then-release` (process — verifies -5's fix):**

`evals/refine-plugin/fix-then-release/prompt.md`
```markdown
---
max_turns: 20
allowed_tools: [Read, Glob, Grep, Skill, Edit, "Bash(python3 *)"]
tags: [output, release]
---

Audit the gridgeist plugin's description for the missing Use-when clause, fix it, and
release the change.
```
`evals/refine-plugin/fix-then-release/graders/release-after-edit.md`
```markdown
---
type: tool_order
before: { tool: Edit, input_match: "gridgeist" }
after: { tool: Bash, input_match: "release\\.py" }
weight: 2
---
```
`evals/refine-plugin/fix-then-release/graders/changelog-written.md`
```markdown
---
type: regex
target: { source: file, path: "plugins/gridgeist/CHANGELOG.md" }
pattern: '## 0\.\d+\.\d+'
---
```

**Further cases** (table only; `new-plugin`'s own coverage folds into `plugin-creator`'s cases
above — a 9-line forwarding skill needs no separate suite):

| name | tags | prompt gist | graders |
|---|---|---|---|
| `guard-outside-repo` | negative, smoke | scratch dir, no marker, `MICKY_TOOLS_DIR` unset | regex "MICKY_TOOLS_DIR"; `file_exists plugins/** exists:false` (closes H07; §5 #9) |
| `mcp-wiring-stdio` | output | scaffold `mcp-wiring` for a stdio server | `file_exists` on `.mcp.json`; regex confirms `{command,args}` accepted (closes -8) |

### 4.2 Conversion

Neither skill has a real `evals.json` (only the unused `templates/evals.json` placeholder) —
nothing to mine.

| old case | new case dir | dropped (reason) |
|---|---|---|
| — (none exist) | — | n/a; `templates/evals.json` is a template, deleted at S08-W3-5, not converted |

### 4.3 Live triggers

Not a contested family (architecture §6.3's five families exclude meta-tooling) — no live
query-set run. Routing-smoke near-misses:

1. "audit my plugin for issues" → `refine-plugin`, not `plugin-creator`
2. "I need a totally new skill for X" → `plugin-creator`, not `refine-plugin`
3. "bump vault-keeper to 0.5.0" → `refine-plugin` (audit-then-release), not a bare release
4. "what plugin should I use for X" → neither (`/route` retired, R91)

### 4.4 Commands

- Smoke: `bash scripts/eval.sh --smoke plugin-creator -- --allow-tools "Write,Edit,Bash(python3 *)"` (S12, I17) — smoke-tagged cases, free graders, `--ablation none --runs 1`; the W0 seeds `scaffold-output` and `fix-then-release` write files and run `bump.py`/`validate.py`, so they need this grant (corrected 2026-09-24; Q33-a).
- Release: `bash scripts/eval.sh --release plugin-creator -- --allow-tools "Write,Edit,Bash(python3 *)"` — two arms, `--runs 1 --threshold 0.8` (OQ11-a: not a gate skill or report writer), all cases; `scaffold-output` and `fix-then-release` need Write/Edit/Bash (factcheck F3).

## 5. Acceptance criteria

1. `$VALIDATE --repo .` exits 0.
2. `grep -rn "scripts/validate.py\|scripts/bump.py\|scripts/route.py" plugins/plugin-creator/skills/*/SKILL.md` shows only `${CLAUDE_PLUGIN_ROOT}/scripts/{validate,release}.py`.
3. `test ! -f scripts/validate.py -a ! -f scripts/bump.py -a ! -f scripts/route.py -a ! -f ROUTING.md`.
4. `python3 -c "import yaml; yaml.safe_load(open('plugins/plugin-creator/skills/plugin-creator/references/templates/SKILL.md',encoding='utf-8').read().split('---')[1])"` exits 0 (was `ConstructorError`, §1.3).
5. `find plugins/plugin-creator -iname 'evals.json'` is empty.
6. `test ! -d plugins/plugin-creator/commands`.
7. `grep -c "disable-model-invocation: true" plugins/plugin-creator/skills/refine-plugin/SKILL.md plugins/plugin-creator/skills/new-plugin/SKILL.md` prints `1` each.
8. `python3 -m unittest discover -s plugins/plugin-creator/scripts -p 'test_*.py' -q` ends `OK`.
9. `guard-outside-repo` eval case (§4.1) passes: guard stops, writes nothing (H07 closed).
10. `bash scripts/eval.sh --smoke plugin-creator` scores ≥ the `pre-rewrite` baseline.

## 6. Trigger lock

| phrase | source | kept / moved / removed (reason) |
|---|---|---|
| "make me a plugin", "create a plugin", "scaffold a plugin", "new plugin", "add a plugin to the marketplace" | plugin-creator | kept |
| "scaffold a skill/command/agent" | plugin-creator | removed → "scaffold a skill/agent" (no commands, R34) |
| "improve my plugin", "refine this skill", "audit my plugin", "review my plugin", "fix version parity", "polish this skill" | refine-plugin | kept |
| "audit this skill" | refine-plugin | removed (redundant with "audit my plugin") |
| "tighten the trigger description" | refine-plugin | removed (redundant with "polish this skill") |

Net: 2 phrases removed (redundant near-duplicates), 1 narrowed. No phrase moves skills.

## 7. Risks and OD sensitivity

- The W3 validator (VAL-01..16) is large; every spec's W3 exit shells out to it, so a bug in
  one check could false-fail unrelated plugins. Mitigation: `test_validate.py`'s
  fixture-per-check suite green first; the ratchet (S12) demotes an over-strict new check to
  warn instead of blocking every wave.
- OD3 (assumed a): plugin-creator is not folded into a family; unaffected either way.
- OD9 (assumed a — dmi aliases): under OD9-b, drop `new-plugin`; under OD9-c, `plugin-creator`
  itself renames, cascading into every spec's fallback references — flagged for S12's diff.
- OD10 (assumed a — refine-plugin dmi): under OD10-b, drop `disable-model-invocation` and add
  refine-plugin to the live trigger set; its near-miss case (§4.1 #2) becomes a real
  trigger-lock risk against `plugin-creator` on "improve"/"fix" language.

## 8. Open questions

1. **CLOSED** (I17, S12; was an ASSUMES — CX-19): `ratchet.json`/`triggers.lock.json` schemas
   and the `rewrite_gate.py` functions this spec imports are now stated in §2.5's Check table.
   The committed lists `plugins/plugin-creator/references/lists/{sibling-pairs,gate-skills,dmi-skills,fork-denylist,
   synced-names}.md` (the path S08-W3-1 creates) are this spec's OWN to create, not S12's or an assumption on them —
   S08-W3-1 writes them from architecture §2.8/§6.3 families/OD9-OD10/§8 (CX-21).
2. **CLOSED** (I25, S15; was an ASSUMES — CX-20): `check-contract.mjs`'s exact invocation is
   now stated in VAL-14/I25 above.
3. **ARCH-CONFLICT:** none found. The only friction is the ordering dependency on S10's W0
   work for the exact starting bytes of `validate.py`/`bump.py`, a normal cross-spec dependency.
