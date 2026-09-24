# Spec S10: micky-psych-tools repo — W0 tooling, catalog, W3 skeleton PR and context diet

| Field | Value |
|---|---|
| Repos | micky-psych-tools |
| Units (today → target) | `scripts/{validate,bump,route}.py` (W0 fixes); `scripts/health.sh`, `.githooks/pre-commit` (new); `marketplace.json`; `.gitignore`; `README.md`; `CLAUDE.md`; `MEMORY.md` (+ `docs/history.md`); `ROUTING.md` (retired W3); per-plugin README/CHANGELOG/LICENSE backfill; the W3 skeleton PR (`alignment`/`evidence`/`visuals` moves) |
| Waves | W0, W3, W5 |
| Owner decisions assumed | OD1(a, ref only), OD2(a), OD3(a), OD6(a), OD7(a), OD9(a), OD10(a), OD12(a); owner answers OQ1-a, OQ10-a, OQ12-a, OQ16-a (all confirmed 2026-09-24) |
| Defects closed | 27 of 27 assigned (HIGH: H13) |
| Interfaces owned | I18, I23, I24 |
| Interfaces consumed | I16 (owner S11), I17 (owner S12), I19 (owner S08), I20 (owner S08) |
| Depends on specs | S11 (I16, read-only), S12 (I17, ratchet.json before S10-W0-1's exit check), S08 (I19/I20 consume this spec's W0 output) |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| Path | Lines | Bytes | Est. tokens | Role |
|---|---|---|---|---|
| `scripts/validate.py` | 141 | 6,203 | 1,550 | marketplace + plugin validator |
| `scripts/bump.py` | 61 | 2,186 | 546 | version bump (plugin.json + catalog entry) |
| `scripts/route.py` | 164 | 6,807 | 1,694 | generates `ROUTING.md` |
| `ROUTING.md` | 168 | 20,197 | 4,923 | generated router (retired W3) |
| `.claude-plugin/marketplace.json` | 212 | 10,749 | 2,680 | catalog, 14 plugins |
| `CLAUDE.md` | 200 | 13,954 | 3,462 | always-loaded project instructions |
| `MEMORY.md` | 1,153 | 108,178 | 26,717 | mandated-first-read living state + history |
| `README.md` | 110 | 6,571 | 1,632 | repo README |
| `.gitignore` | 3 | 29 | 7 | `__pycache__/`, `*.pyc`, `.DS_Store` only |
| `docs/superpowers/plans/2026-07-10-improve-all-plugins.md` | 377 | — | — | superseded plan; 60 unchecked `- [ ]` boxes (measured with `grep -c`), 0 checked |
| `docs/agents/{issue-tracker,triage-labels,domain}.md` | — | — | — | kept unchanged; CLAUDE.md points to them |
| `scripts/health.sh` | 0 (new) | — | — | fast/full repo health check |
| `.githooks/pre-commit` | 0 (new) | — | — | runs `health.sh --fast` |

Per-plugin manifest/doc presence (measured with a `python3` loop over `plugins/*/.claude-plugin/plugin.json` + `ls`):

| Plugin | version | CHANGELOG.md | LICENSE | README.md | CHANGELOG top vs version |
|---|---|---|---|---|---|
| pubmed-research-note | 1.7.0 | yes | no | yes | matches; gap 1.3.0/1.4.0 (between 1.2.0, 1.5.0) |
| intent-lock | 0.4.2 | yes | no | yes | matches; gap 0.4.1 (between 0.4.0, 0.4.2) |
| plugin-creator | 0.3.0 | yes | no | yes | matches |
| vault-keeper | 0.4.0 | yes | no | yes | top 0.2.0 ≠ 0.4.0; 0.3.0/0.4.0 missing |
| psych-paper-digest | 0.1.1 | yes | no | yes | top 0.1.0 ≠ 0.1.1 |
| comprehensive-review | 0.3.0 | yes | no | yes | matches |
| clinical-infographic | 0.2.1 | yes | no | yes | top 0.2.0 ≠ 0.2.1 |
| firecrawl | 0.2.0 | yes | no | yes | matches |
| concept-animation | 0.1.1 | **no** | no | **no** | — |
| gridgeist | 0.1.0 | **no** | **yes** | **no** | vendored; LICENSE is upstream's |
| code-explainer | 0.1.0 | **no** | no | yes | — |
| ml-concept-lab | 0.1.0 | **no** | no | **no** | — |
| decision-interview | 0.1.1 | **no** | no | **no** | — |
| plan-critique | 0.1.0 | yes | no | yes | matches |

### 1.2 Descriptions

This spec owns no `SKILL.md`, `commands/`, or `agents/` files — its units are repo tooling, the catalog, and top-level docs. Section 1.2/2.2/2.3 are not applicable; the W3 skeleton PR *moves* other specs' skill files unchanged (§2.1, §3) but does not author or edit their frontmatter. The one description this spec edits is the marketplace's own top-level `description` field (§2.1, unchanged text, W3 adds `$schema`).

### 1.3 Defects

| Id | Sev | H# | Evidence (re-opened) | Problem (short) | Fix step | Wave |
|---|---|---|---|---|---|---|
| validate.py-1 | H | H13 | `:50-51`, `:72-73`, `:89-92` (`check(isfile)` then unconditional `json.load`) | `check()` only prints, never stops execution: missing/malformed file crashes instead of FAIL; some PASS/FAIL not counted | S10-W0-1 | W0 |
| validate.py-2 | M | — | `:4` docstring; `README.md:57-59` | Docstring/README overstate coverage vs the real CLI (which now does YAML, hooks, dupes, author, and version drift) | S10-W0-1, -6 | W0 |
| validate.py-3 | M | — | `:25-44` `frontmatter()` regex parser | Hand-rolled parser: literal quote-counting, CRLF-broken, no invalid-YAML detection; duplicated in `route.py:25-44` | S10-W0-1 | W0 |
| validate.py-4 | M | — | `:93` `all("url" in s and "type" in s ...)` | Rejects stdio `{command,args}` MCP servers; ignores auto-discovered `.mcp.json`; never opens `hooks/hooks.json` | S10-W0-1 (stdio only) | W0; rest deferred to S08 (I19) |
| validate.py-5 | L | — | 0 hits for placeholder/evals-schema/CHANGELOG-vs-version/README/name-format checks in 141 lines | Cheap mechanical checks absent | S08-W3-1 (the plugin-creator validator adds them, I19) | W3 |
| validate.py-6 | L | — | `:110` `check(n >= 200, ...)` | House heuristic (min length) reported as hard FAIL | S10-W0-1 | W0 |
| route.py / ROUTING.md-1 | M | — | 20,197 B ROUTING.md; `CLAUDE.md:12-15` mandate | Lossy token-heavy copy (29/29 cues verbatim substrings, no Not-for); CLAUDE.md mandates reading it first | S10-W0-5 (demote), S10-W3-9 (retire) | W3 |
| route.py / ROUTING.md-2 | M | — | `:114-164` `main()`, no `sys.argv` use anywhere | `--help`/any arg ignored; regenerates and overwrites `ROUTING.md` | S10-W0-4 | W0 |
| route.py / ROUTING.md-3 | M | — | `:145` version in header; `bump.py` never reruns `route.py`; `CLAUDE.md:54-57` order | `ROUTING.md` embeds versions; a release leaves stale ones in it | S10-W0-4 (drop versions from output) | W0 |
| route.py / ROUTING.md-4 | L | — | `:54-77` `use_when()` docstring states phrasing constraints; regex-based | Fragile cue extraction; constraints live only in a docstring | S10-W3-9 (route.py deleted) | W3 |
| route.py / ROUTING.md-5 | L | — | `CLAUDE.md:15`; `plugins/plugin-creator/commands/route.md:24` | On no match, tells Claude to scaffold a new plugin | S10-W3-8 (line deleted with routing section) | W3 |
| bump.py-1 | M | — | `:53` `json.dump(..., indent=2)`, no `ensure_ascii=False`, no newline | `\uXXXX` escapes + no trailing newline, noisy diffs | S10-W0-2 | W0 |
| bump.py-2 | M | — | `:47-57` writes only `man['version']`/`entry['version']`; `marketplace.json:3` top version untouched; `MEMORY.md:14-36` hand table | Updates only 2 of the version-bearing surfaces; never touches CHANGELOG, MEMORY's table, ROUTING, catalog top version | S10-W0-2 | W0 |
| bump.py-3 | L | — | `:4-8` stated reason vs the CLI's own drift warning (plugin.json wins) | Stale reasoning for parity, though equal values were still good hygiene | S10-W0-2 (parity concept removed) | W0 |
| bump.py-4 | L | — | `:53-57` writes before validating; no `--dry-run` | No dry run, no rollback: a failed validation leaves files bumped | S10-W0-2 | W0 |
| marketplace.json-1 | L | — | 9 of 14 `plugin.json` descriptions differ from the catalog entry's (measured, `python3` diff over all 14 pairs) | Summaries drift between `plugin.json` and the catalog entry | S10-W3-1 | W3 |
| marketplace.json-2 | L | — | top keys `name,version,description,owner,plugins`; `owner={"name":…}` only; no `$schema`; no trailing newline | Missing `$schema`, `owner.email`, provenance fields; no trailing newline | S10-W0-3 (newline), S10-W3-1 (`$schema`) | W3 |
| marketplace.json-3 | L | — | `:3` `"version": "1.16.0"`; no `mkt["version"]` write anywhere in `bump.py` | Catalog top-level version bumped by hand; no tool manages it | S10-W0-3 | W0 |
| README.md (root)-1 | M | — | `:53-54` command has no `--strict` | Drift/warnings pass with exit 0; root-only run never opens plugin content | S10-W0-6 | W0 |
| README.md (root)-2 | M | — | `:57-59` "the CLI does not [check parity]" | False for CLI 2.1.280 (`--strict` warns) | S10-W0-6 | W0 |
| README.md (root)-3 | L | — | `:14-15` "must be a **public** repo"; `MEMORY.md:10` "(**private**)" | Contradicted by this repo's own recorded state | S10-W0-6 | W0 |
| README.md (root)-4 | L | — | `:18` `git add -A`; `.gitignore` (3 lines, no `.env`) | Stages everything while `.env` (firecrawl's key) is not ignored | S10-W0-7, S10-W0-6 | W0 |
| CLAUDE.md (micky-psych-tools)-1 | M | — | `:7` "Read `MEMORY.md` first"; MEMORY ~26.7k tok; `:12-15` route-first mandate | Mandates reading ~27k + ~5k tok before any request | S10-W0-5 (wording), S10-W3-8 (removed) | W3 |
| CLAUDE.md (micky-psych-tools)-2 | M | — | `grep gridgeist CLAUDE.md` → 0 hits; `marketplace.json`, `README.md:29`, `MEMORY.md:27` all list it | Hand-maintained plugin list omits gridgeist | S10-W3-8 (catalog section deleted) | W3 |
| CLAUDE.md (micky-psych-tools)-3 | L | — | `:54-57` workflow order; `:61-64` health check lists only validate.py/route.py | Stale versions after bump (moot once route drops versions); health check omits `--strict` | S10-W0-5 | W0 |
| CLAUDE.md (micky-psych-tools)-4 | L | — | `:110-118` "three vendor skill segments" | Stale firecrawl fact, lives entirely in the deleted catalog section | S10-W3-8 | W3 |
| CLAUDE.md (micky-psych-tools)-5 | L | — | `:21-36` layout omits README/CHANGELOG/LICENSE/evals/references/hooks | Layout diagram incomplete vs what plugins actually ship | S10-W0-5 | W0 |

**Count: 27 of 27, each appearing once.** No deferral beyond the two above (validate.py-4's non-stdio half, validate.py-5), both scoped to S08's W3 validator rewrite (I19).

### 1.4 Other findings

- OBS (frontmatter portability, re-verified: `yaml.safe_load` against every `plugins/*/skills/*/SKILL.md`): **1 of 17** fails strict YAML — `plugins/intent-lock/skills/intent-lock/SKILL.md`, "mapping values are not allowed here" at line 2 col 574. S10-W0-1's switch to `yaml.safe_load` makes this file FAIL where the old parser passed it — a regression risk for S01/S02 unless ratcheted (§8).
- OBS (repo-root script coupling): plugin-creator's own skills call these scripts by repo-root-relative paths (`skills/plugin-creator/SKILL.md:78,86`, `skills/refine-plugin/SKILL.md:64,73`, `commands/route.md:9`, `commands/refine-plugin.md:12`, all `grep`-confirmed) — this is H07, owned by S08. This spec's W0 fixes keep the scripts working at the repo root; S08's W3 step moves them and rewrites the calls (I18 consumer).
- OBS (identical `.mcp.json` copies, `diff`-verified): pubmed-research-note/comprehensive-review/psych-paper-digest's `.mcp.json` are byte-identical. The skeleton PR keeps one and deletes the other two with no content loss.
- OBS: `docs/superpowers/plans/2026-07-10-improve-all-plugins.md` has 60 unchecked `- [ ]` boxes, 0 checked, though the architecture states all 11 tasks are done. S10-W3-11 adds a header note only.
- OBS (duplicated summaries): plugin summaries live on six surfaces (`plugin.json`, `marketplace.json`, `README.md`, CLAUDE.md's Plugins section, `MEMORY.md:38-157`, `ROUTING.md`). This spec removes three as hand-maintained copies (CLAUDE.md's catalog in S10-W3-8, ROUTING.md in S10-W3-9, entry `description` in S10-W3-1, R88); `plugin.json` (S01–S08) and MEMORY's blurb (deleted wholesale in S10-W3-10) are out of scope.
- NEW: `state/` does not exist today. The W3 skeleton PR creates it (`state/misreads.md` moved from `plugins/intent-lock/skills/intent-lock/references/misreads.md`; `state/lit-watch/` empty for S04).

## 2. Target state

### 2.1 Location and tree (after the last wave that touches these units, W3)

```
.claude-plugin/marketplace.json   $schema, name, owner, description; entries {name, source, category, keywords};
                                   no versions; append-only renames{}
plugins/
  alignment/ evidence/ visuals/    content owned by S01/S02, S03/S04, S05 — this spec moves dirs in, unchanged
  vault-keeper/ firecrawl/ gridgeist/ plugin-creator/   unchanged locations, content owned elsewhere
state/               misreads.md; lit-watch/   created here (W3), populated by S01/S02, S04
scripts/health.sh    new (W0)
.githooks/pre-commit new (W0), runs `health.sh --fast`
docs/rewrite/         ratchet.json triggers.lock.json delivery-log.md baseline.md h-coverage.md   (S12/S11 own)
docs/history.md       new (W3), MEMORY's "Recent milestones" moved verbatim
docs/superpowers/plans/2026-07-10-improve-all-plugins.md   header note: "superseded by docs/rewrite/"
CLAUDE.md ≤5 KB · MEMORY.md living section ≤6 KB · README.md
```

Removed by this spec: `route.py`, `ROUTING.md`, the mandated-read wording, MEMORY's versions table. Removed by OTHER specs: the 9 old plugin dirs' remaining content (their skill/reference/script content is those specs' unit — this spec only moves the directories, §3 W3).

### 2.2 Frontmatter

Not applicable — see §1.2.

### 2.3 Body outline

Not applicable — see §1.2.

### 2.4 References

| File | Purpose | Load condition | Size target |
|---|---|---|---|
| `CLAUDE.md` | conventions, layout, placement rules, health command, delivery pointer | always loaded | ≤5 KB (§9; R92's ≤2,000-tok is the stricter alternative, §7) |
| `MEMORY.md` (living section) | identity, delivery facts, open threads, current wave | on demand, not mandated | ≤6 KB |
| `docs/history.md` | content-filing log (moved from "Recent milestones") | on demand | unchanged length, moved verbatim |
| `README.md` | register/update/validate instructions, plugin list | read by a human | unchanged length target; corrected content |
| `docs/rewrite/ratchet.json` | S12's file; this spec appends one entry (intent-lock YAML) | read by `validate.py` every run | — |

### 2.5 Scripts

| Name | CLI | Input | Stdout | Exit codes | Tests |
|---|---|---|---|---|---|
| `validate.py` | `python3 scripts/validate.py` (no args in W0; `--repo`/`--cross-repo`/`--versions`/`--fix-seams` are S08's W3 additions) | repo tree | `PASS`/`FAIL`/`WARN` lines, final `all checks passed` or `N failure(s)` | 0 / 1 | new: guarded-load crash cases (missing mkt/man/`.mcp.json`), CRLF frontmatter, stdio MCP, sub-200-char WARN, intent-lock ratchet |
| `bump.py` | `python3 scripts/bump.py <plugin> <major\|minor\|patch> [--write]` | plugin + level | old→new version, validator output on `--write` | 0 / 1 (unknown plugin/level, post-write validation failed) | new: dry run no-op, `--write` UTF-8+newline no `\u`, failed post-write reported (files stay bumped, §7) |
| `route.py` | `python3 scripts/route.py [-h\|--help]` (argparse; `--help` writes nothing) | catalog + components | regenerates `ROUTING.md` | 0 | new: `--help` leaves `ROUTING.md` byte-identical |
| `health.sh` | `bash scripts/health.sh [--fast]` | none | human-readable | 0 / 1 | none of its own — wraps `validate.py`'s tests + `claude plugin validate --strict` |
| `.githooks/pre-commit` | invoked by git, no args | none (runs the full fast check, does not diff) | none | 0 / 1 | smoke-tested via a scratch commit in the W0 exit gate |

### 2.6 Handoffs

Not applicable — this spec's units are not skills and issue no OPTIONAL cross-plugin handoffs.

### 2.7 Interfaces

**I18 — W0 tooling in place (owned).** By W0 exit, in micky-psych-tools: `validate.py` has no crash path (every load guarded, every result counted via `check()`), CRLF-safe `yaml.safe_load` frontmatter, a stdio MCP server passes, no length floor (only the ≤1,024 ceiling), version-parity check removed, a WARN-not-FAIL path for `docs/rewrite/ratchet.json` (I17) entries; `bump.py` edits `plugin.json` only + a CHANGELOG stub, dry run by default, validates before `--write`, UTF-8 + newline; `route.py` uses `argparse`, `--help` writes nothing, no versions in `ROUTING.md`; `health.sh [--fast]` and `.githooks/pre-commit` exist and call `validate.py` + `claude plugin validate --strict` (root + every plugin) + (full mode) unit tests. Consumers: **S08** edits this base in its W3 move (validate.py → `plugins/plugin-creator/scripts/`, gains `--repo`/`--cross-repo`/`--versions`/`--fix-seams`; bump.py → `release.py`). **S12** reuses the unittest file names via its own `unittest discover`.

**I23 — W3 skeleton PR (owned).** One reversible commit set: (1) creates `plugins/{alignment,evidence,visuals}/skills/`; (2) `git mv`s each source plugin's skill dir into its family (table, S10-W3-2); (3) deletes every member's `commands/` dir (R34) AND, in the SAME commit, creates the 7 family alias skills that replace them — text copied verbatim from S02/S04/S05/S06 §2.2 (CX-1, so the typed forms never go missing even for one commit); (4) keeps one `.mcp.json` for evidence (from pubmed-research-note, byte-identical to the other two, §1.4), deletes the duplicates; (5) moves the misread ledger to `state/misreads.md` (`state/lit-watch/` is NOT created here — S04-W3-1 creates it directly when it writes the migrated config, CX-62); (6) moves every plugin-root directory except `skills/`/`.claude-plugin/`/`commands/` (references/, scripts/, evals/<skill>/, examples/ — to the FAMILY ROOT for visuals, CX-32 — one family LICENSE) and each member's `README.md`/`CHANGELOG.md` into the family dir under a source-suffixed name — consolidation into ONE README/CHANGELOG per family is NOT done here, it is S01/S03+S04/S05's own W3 step (CX-2); (7) deletes each now-empty source dir only once `find plugins/<p> -type f` lists nothing but `.claude-plugin/plugin.json` (CX-2 — a forgotten file blocks the delete rather than vanishing with it); (8) creates the three family `.claude-plugin/plugin.json` (`$schema`, `name`, `version: "1.0.0"`, `description`, `author`, `keywords` — CX-3); (9) adds `renames` entries (R87) for all 10, plus the OD7-a skill rename inside evidence (content, owned by S04). Consumers: S01–S07's W3 content steps depend on this step.

**I24 — `marketplace.json` shape (owned).** W0 (S10-W0-3): every entry's and the top-level `version` key deleted; trailing newline. W3 (S10-W3-1): top-level `$schema` added (**ASSUMES** the literal value Claude Code's own `plugin marketplace init` writes — not verified here, §8); top-level `description` kept; each entry reduced to `{name, source, category, keywords}` (no `description`, R88); `renames` added, append-only, no cycles. Consumer: S08's `validate.py --repo` (I19) checks this shape, does not redefine it.

**Consumed.** I16 (S11) — under OQ10-a the cloud value switches to the folder paths only with the last W3 family merge (S11-W3-1), and S11-W3-5 drops the per-plugin segments the skeleton removes; S10-W3-2 needs no environment change first. This spec never touches `delivery-log.md`. I17 (S12) — `docs/rewrite/ratchet.json` is `{generated_at, repo, entries:[{check_id,path,message}]}`, read/written via S12's `rewrite_gate.py` library (CX-19; no longer an ASSUMES). I19 (S08) — CLOSED (was an ASSUMES): S08-W3-1 now explicitly edits `scripts/health.sh` to call the new plugin-creator `validate.py` location, keeping S11-W0-3's own two lines (CX-11/CX-39). I20 (S08) — the frontmatter key whitelist and description-order rule are enforced by S08's W3 validator, not this spec's W0 fix.

## 3. Change steps

### W0

**S10-W0-1 — Fix `validate.py`: guarded loads, counted checks, CRLF-safe YAML, stdio MCP, no floor.**
- Repo · depends on: none (`ratchet.json` read defensively — absent = empty, no S12 dependency).
- Files: edit `scripts/validate.py`.
- Change: replace `frontmatter()` (`:25-44`) with a CRLF-safe reader (`.replace("\r\n","\n")`) calling `yaml.safe_load` on the extracted block, returning `("yaml-error", str(e))` on a `YAMLError` instead of raising. In `main()`, turn every `check(isfile(X))` → unconditional load pair (`:50-51, 72-73, 90-92`) into a guarded `if not isfile: check(False,...); continue`; wrap remaining `json.load(open(...))` in `try/except` → counted FAIL (closes H13's uncounted-PASS half at `:111-114`). `:93`: accept `"command" in s` too (stdio MCP). Delete `:110`'s floor and `:81-82`'s parity check. Add: load `docs/rewrite/ratchet.json` if present (default `{"entries": []}`, S12's own schema — CX-19); a `"yaml-error"` result whose path appears in an `entries[]` row with `check_id: "yaml-parse"` prints `WARN`. Fix the docstring (`:2-9`).
- Commands: `python3 -c "import ast; ast.parse(open('scripts/validate.py').read())"`; `python3 scripts/validate.py`; `python3 -m unittest discover -s scripts -p 'test_validate.py' -q` (new file, same commit).
- Done when: `python3 scripts/validate.py` exits 1 with exactly one `FAIL`, a `yaml-error` naming `plugins/intent-lock/skills/intent-lock/SKILL.md` (no ratchet entry exists yet; S10-W0-1b seeds it), and no length-floor line; the new unittest passes. Until S10-W0-1b lands, this one FAIL is the only allowed repo-check failure (critique P4).
- Rollback: `git revert`.

**S10-W0-1b — Seed `docs/rewrite/ratchet.json` with the one known YAML violation.**
- Repo · depends on: S10-W0-1, S12-W0-1 (CX-19 — `rewrite_gate.py` must exist before this step calls it).
- Files: `docs/rewrite/ratchet.json` (written by the command below, via S12's own tool — this step creates no file logic of its own).
- Change: `python3 scripts/rewrite_gate.py ratchet seed --check yaml-parse --write` — adds an `entries[]` row `{check_id: "yaml-parse", path: "plugins/intent-lock/skills/intent-lock/SKILL.md", message: "..."}` via S12's `rewrite_gate.py` (CX-19 — not a hand-written `{"yaml-parse":[paths]}` map).
- Commands: `python3 -c "import json; d=json.load(open('docs/rewrite/ratchet.json')); assert any(e['check_id']=='yaml-parse' for e in d['entries'])"`; `python3 scripts/validate.py`.
- Done when: the assertion passes; `python3 scripts/validate.py` exits 0 and prints `all checks passed` plus one `WARN` naming `plugins/intent-lock/skills/intent-lock/SKILL.md`, and no length-floor line. This step is the only writer of the `yaml-parse` entry; S12-W0-1 creates `ratchet.json` with no entries (critique P4).
- Rollback: `git revert` (a single-key add reverts cleanly if no other spec touched the same line).

**S10-W0-2 — Rewrite `bump.py`.**
- Repo · depends on: S10-W0-1 (`--write` calls `validate.py`), S10-W0-1b (so `validate.py` exits 0), S10-W0-3 (the dry-run test expects a catalog without versions).
- Files: edit `scripts/bump.py`.
- Change: add `argparse` (`plugin`, `level` positional; `--write`, default off = dry run). Dry run prints `{plugin}: {old} -> {new}` plus the CHANGELOG stub text; no file changes. `--write`: (1) run `validate.py` first, abort with no write on failure; (2) write `plugin.json` only (the `entry["version"]`/`marketplace.json` write is deleted — S10-W0-3 already removed that key); (3) prepend `## {new} — {date}\n\n` to `plugins/<p>/CHANGELOG.md` (create with a `# Changelog\n\n` header if absent); (4) `json.dump(..., ensure_ascii=False, indent=2)` + trailing `\n`; (5) re-run `validate.py` and report its exit code (no rollback on a post-write failure — §7).
- Commands: `python3 scripts/bump.py pubmed-research-note patch` (dry run; `git diff` empty); `... --write` in a scratch branch, `git diff .../plugin.json` (no `\u`, trailing newline), then `git checkout -- plugins/pubmed-research-note`.
- Done when: dry run makes no changes; `--write` edits exactly `plugin.json` + `CHANGELOG.md`; `python3 -m unittest discover -s scripts -p 'test_bump.py' -q` passes (new file).
- Rollback: `git revert`.

**S10-W0-3 — Strip marketplace.json versions.**
- Repo · depends on: none (must land before S10-W0-2's dry-run test).
- Files: edit `.claude-plugin/marketplace.json`.
- Change: delete the top-level `"version"` line (`:3`) and every entry's `"version"` line (14); trailing newline.
- Commands: `python3 -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); assert 'version' not in d and all('version' not in p for p in d['plugins'])"`.
- Done when: assertion passes; `python3 scripts/validate.py` still exits 0.
- Rollback: `git revert`.

**S10-W0-4 — Fix `route.py`: argparse, no versions in output.**
- Repo · depends on: none.
- Files: edit `scripts/route.py`.
- Change: add `argparse.ArgumentParser().parse_args()` at the top of `main()` (an unrecognized flag or `-h`/`--help` exits 0 via argparse before `open(MKT)` runs, so nothing writes). `:145`: delete `f" _v{p['version']}_"` from the header (category still renders).
- Commands: `python3 scripts/route.py --help` then `git status --short` (no `ROUTING.md` change); `python3 scripts/route.py` then `grep -c '_v[0-9]' ROUTING.md` (`0`).
- Done when: both match.
- Rollback: `git revert`.

**S10-W0-5 — Edit CLAUDE.md: version rule, mandate demotion, workflow/health order, layout diagram.**
- Repo · depends on: S10-W0-1..4.
- Files: edit `CLAUDE.md`.
- Change: `:38-42` → "**Version lives in `plugin.json` only.**… run `python3 scripts/bump.py <plugin> patch|minor|major --write`." `:10-19` demote the routing mandate to a note (not required reading); delete the "run `/new-plugin`" sentence. `:50-59` make `route.py` optional, not numbered; add "`bash scripts/health.sh` must be green". `:61-64` → `bash scripts/health.sh`. `:21-36` add `README.md`, `CHANGELOG.md`, `LICENSE`, `evals/<skill>/<case>/`, `references/`, `hooks/hooks.json` to the layout tree — the diagram line reads `evals/<skill>/<case>/` (CX-23; plugin-root `evals/`, matching I17's layout — vault-keeper's own `evals/` sits at the plugin root too, not nested under `skills/`).
- Commands: `wc -c CLAUDE.md`.
- Done when: `grep -n "Read \`MEMORY.md\` first\|route it first" CLAUDE.md` shows the mandate wording gone; `grep -n "scripts/health.sh" CLAUDE.md` finds it twice.
- Rollback: `git revert`.

**S10-W0-6 — Fix README.md.**
- Repo · depends on: S10-W0-1, S10-W0-7.
- Files: edit `README.md`.
- Change: `:54` add `--strict` (plus a second line validating a `plugins/<name>` dir — root alone never opens plugin content). `:57-59` replace the false parity claim with the corrected coverage split. `:14-15` "must be a **public** repo" → "works with a **private** repo too… (installed from a private GitHub remote today)". `:18` keep `git add -A`, note above it that `.gitignore` now excludes `.env`/`.firecrawl/`.
- Commands: `grep -n "must be a" README.md`; `grep -n "\-\-strict" README.md`.
- Done when: both match.
- Rollback: `git revert`.

**S10-W0-7 — `.gitignore`.**
- Repo · depends on: none.
- Files: edit `.gitignore`. Change: append `.env`, `.firecrawl/`, `plugins/*/evals/results/`.
- Commands: `cat .gitignore`.
- Done when: all three lines present; `git check-ignore -v .env` matches.
- Rollback: `git revert`.

**S10-W0-8 — Per-plugin README/CHANGELOG/LICENSE backfill.**
- Repo · depends on: none.
- Files: per plugin, one commit (or split, both revert the same way).

Backfill-note body for every inserted gap entry: "no contemporaneous entry; see `git log` around this version."

| Plugin | CHANGELOG action | LICENSE | README |
|---|---|---|---|
| pubmed-research-note | insert `## 1.4.0`, `## 1.3.0` between `1.5.0` and `1.2.0` | add | keep |
| psych-paper-digest | insert `## 0.1.1` above `0.1.0` | add | keep |
| vault-keeper | insert `## 0.4.0`, `## 0.3.0` above `0.2.0` | add | keep |
| intent-lock | insert `## 0.4.1` between `0.4.2` and `0.4.0` | add | keep |
| clinical-infographic | insert `## 0.2.1` above `0.2.0` | add | keep |
| code-explainer, concept-animation, decision-interview, ml-concept-lab | create, `## <version> — initial release` | add | keep (code-explainer) / create (other 3, one paragraph from the catalog description) |
| gridgeist | create, `## 0.1.0 — vendored` | already has one (untouched) | create (notes it is vendored) |
| plugin-creator, comprehensive-review, firecrawl, plan-critique | none (top already == version) | add | keep |

- LICENSE text: identical MIT, owner "Thanawat Suharit (Micky)", 2026 (OQ1-a, confirmed 2026-09-24; matches gridgeist's own).
- Repo-level tooling CHANGELOG (plan OQ16-a, confirmed 2026-09-24): create `docs/rewrite/CHANGELOG.md` with a `# Changelog` header and one `## Unreleased` entry for the W0 tooling. Every repo tooling step in S10, S11 and S12 (scripts/, docs/rewrite/, CLAUDE.md, README.md) adds its entry there.
- Commands: presence check per file; `grep -c '^## ' plugins/<p>/CHANGELOG.md`.
- Done when: §1.1's table shows `yes` everywhere except gridgeist's already-`yes` LICENSE, and every CHANGELOG top matches `plugin.json`.
- Rollback: `git revert`.

**S10-W0-9 — `scripts/health.sh`.**
- Repo · depends on: S10-W0-1, S12-W0-1 (`rewrite_gate.py` must exist for the verify lines).
- Files: create `scripts/health.sh`.
- Change:
```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/validate.py
claude plugin validate --strict .claude-plugin/marketplace.json
for d in plugins/*/; do claude plugin validate --strict "$d"; done
python3 scripts/rewrite_gate.py ratchet verify
python3 scripts/rewrite_gate.py triggers verify
if [ "${1:-}" != "--fast" ]; then
  python3 -m unittest discover -s scripts -p 'test_*.py' -q
  [ -n "${LEARN_HUB_DIR:-}" ] && [ -f "$LEARN_HUB_DIR/package.json" ] && \
    echo "cross-repo checks: not yet available (owner S08, I19 --cross-repo)"
fi
echo "health: OK"
```
- Commands: `chmod +x scripts/health.sh`; `bash scripts/health.sh --fast`; `bash scripts/health.sh`.
- Done when: both exit 0 and print `health: OK`; `--fast` runs `ratchet verify` and `triggers verify`, so the pre-commit hook (S10-W0-10) enforces plan §0 rules 6–7 on every commit (critique F8).
- Rollback: `git revert`.

**S10-W0-10 — `.githooks/pre-commit`.**
- Repo · depends on: S10-W0-9.
- Files: create `.githooks/pre-commit`: `#!/usr/bin/env bash`, `set -euo pipefail`, `cd "$(git rev-parse --show-toplevel)"`, `bash scripts/health.sh --fast`.
- Commands: `chmod +x .githooks/pre-commit`.
- Done when: `bash .githooks/pre-commit` exits 0 from the repo root.
- Rollback: `git revert`.

**S10-W0-11 (OWNER) — Enable the hook once per clone.**
- `git config core.hooksPath .githooks`.
- Done when: the config prints `.githooks`; a scratch commit with a deliberately broken `validate.py` is blocked.

### W3

**S10-W3-1 — `marketplace.json` W3 shape.**
- Repo · depends on: S10-W0-3. OQ10-a dropped the dependency on S11-W3-1: commits on the skeleton branch do not need the new environment value; the `renames` this step adds still let a later `claude plugin marketplace update` follow the rename (architecture §7; CX-34).
- Files: edit `.claude-plugin/marketplace.json`.
- Change: add top-level `"$schema": "<ASSUMES — §8>"`; reduce every entry to `{name, source, category, keywords}` (drop `description`); add `renames` (table below).

| old name | new name/location |
|---|---|
| `intent-lock` | `alignment` |
| `decision-interview` | `alignment` |
| `plan-critique` | `alignment` |
| `pubmed-research-note` | `evidence` |
| `comprehensive-review` | `evidence` |
| `psych-paper-digest` | `evidence` |
| `clinical-infographic` | `visuals` |
| `concept-animation` | `visuals` |
| `ml-concept-lab` | `visuals` |
| `code-explainer` | `visuals` |

- Commands: `claude plugin validate --strict .claude-plugin/marketplace.json` — must run after S10-W3-2 lands too (a `renames` target that doesn't exist yet fails validation; same commit or same PR, in order).
- Done when: the CLI passes; `python3 -c "import json; assert len(json.load(open('.claude-plugin/marketplace.json'))['plugins'])==7"` (alignment, evidence, visuals, vault-keeper, firecrawl, gridgeist, plugin-creator).
- Rollback: `git revert` (one PR with S10-W3-2, per I23's "reversible in one revert").

**S10-W3-2 — The skeleton move (I23).**
- Repo · depends on: S10-W3-1 (same commit).
- Files: one `git mv <old> plugins/<family>/skills/<skill>` per row, plus the extra moves noted:

| Plugin (old dir) | Family | Extra moves |
|---|---|---|
| intent-lock (2 skills: intent-lock, misread-capture) | alignment | `skills/intent-lock/references/misreads.md` → `state/misreads.md` |
| decision-interview, plan-critique | alignment | — |
| pubmed-research-note | evidence | `.mcp.json` → `plugins/evidence/.mcp.json` |
| comprehensive-review, psych-paper-digest | evidence | `.mcp.json` deleted (byte-identical dup, §1.4) |
| clinical-infographic, concept-animation, ml-concept-lab | visuals | `examples/` → `plugins/visuals/examples/` (plugin root, not the skill's own dir — CX-32, matching architecture §3.2's `${CLAUDE_PLUGIN_ROOT}/examples/` and S05's own reference to that path) |
| code-explainer | visuals | — |

Then, for all 10: for each member plugin, move every plugin-root directory EXCEPT `skills/`, `.claude-plugin/`, `commands/` to the family root at the same relative path (`references/`, `scripts/` — keeping one copy of any file byte-identical across members, `evals/<skill>/`, one family `LICENSE` per S10-W0-8's backfill); `git rm -r --ignore-unmatch plugins/<p>/commands`; `git mv plugins/<p>/README.md plugins/<family>/README-<p>.md` (and `CHANGELOG.md`, covering the S10-W0-8 backfilled files too — these per-member files are consolidated into one family README/CHANGELOG/LICENSE by S01-W3-5 (alignment), S03-W3-7 (evidence), S05-W3-5 (visuals), not by this step); `git rm -r plugins/<p>` for each old dir, but ONLY once `find plugins/<p> -type f` lists nothing but `.claude-plugin/plugin.json` (CX-2 — a plugin-root file this step forgot to move must block the delete, not silently vanish with it). `mkdir -p plugins/{alignment,evidence,visuals}/skills` runs first. In the same commit, create the three family `.claude-plugin/plugin.json` files (`$schema`, `name`, `version: "1.0.0"` — a fresh major, no history to carry forward — `description`, `author`, `keywords`; CX-3) AND the 7 family alias skills (`plugins/alignment/skills/{critique-plan,resolve-decisions}/SKILL.md`, `plugins/evidence/skills/digest/SKILL.md`, `plugins/visuals/skills/{infographic,animate,visualize,explain-code}/SKILL.md`), text copied verbatim from S02 §2.2 (critique-plan, resolve-decisions), S04 §2.2 (digest), S05 §2.2 (animate, visualize), S06 §2.2 (infographic, explain-code) — CX-1, so `/critique-plan`, `/resolve-decisions`, `/animate`, `/visualize` exist the instant the old `commands/` wrappers are deleted, not later.
- Commands: `git status --short | grep -c '^R'` (rename count); `find plugins/intent-lock plugins/decision-interview plugins/plan-critique plugins/pubmed-research-note plugins/comprehensive-review plugins/psych-paper-digest plugins/clinical-infographic plugins/concept-animation plugins/ml-concept-lab plugins/code-explainer` — all "No such file or directory"; `find plugins/{alignment,evidence,visuals}/skills -maxdepth 1 -name SKILL.md -path '*critique-plan*' -o -path '*resolve-decisions*' -o -path '*digest*' -o -path '*infographic*' -o -path '*animate*' -o -path '*visualize*' -o -path '*explain-code*' | wc -l` = 7.
- Done when: `find plugins -maxdepth 1 -type d | sort` lists exactly the 7 family/standalone dirs; `ls plugins/{alignment,evidence,visuals}/skills` show 4+2, 3+1, 4+4 dirs (members + aliases); the 7-alias find above = 7; `validate.py`/`route.py` (present until S10-W3-9) run without crashing.
- Commit shape (critique C2-14): S10-W3-1 and S10-W3-2 land as ONE PR of three commits, one per family, in the order alignment, evidence, visuals. Each commit holds that family's marketplace entries and `renames` rows (S10-W3-1), its `plugin.json`, its `git mv`s and extra moves, its alias skills, and the deletion of its old plugin dirs (with their `commands/`), and passes `bash scripts/health.sh --fast`. Review the moves with `git diff -M100% --stat --diff-filter=R`. The done-when above is checked after the third commit.
- Rollback: `git revert` the PR merge (all three families), or one family's commit.

**W3 steps 3 to 7 are not this spec's.** The family content rewrites (alignment's `interview-protocol.md`/`lock-record.md`/intent-lock subtraction/misread-capture/`ledger.py`; evidence's `report-contract.md`/`engines.md`/decision-brief fix/`sweep.py`/`sources_lint.py`; visuals' `html-artifact-contract.md`/`render-verify.md`/code-explainer fix/ML trim; firecrawl split; gridgeist `UPSTREAM.md`; plugin-creator self-containment) belong to S01–S08 (architecture §10 W3 items 3-6). This spec resumes at the repo-wide description pass's context diet.

**S10-W3-8 — Micky context diet: CLAUDE.md ≤5 KB.**
- Repo · depends on: S10-W3-2; S01-W3-6, S02-W3-4, S03-W3-7, S04-W3-6, S05-W3-5, S06-W3-4, S07-W3-1, S08-W3-9, S09-W3-4 (every content spec's last W3 step — referenced facts must be final; CX-34, replacing the informal "S01–S08" — this step lands near the END of W3).
- Files: rewrite `CLAUDE.md`.
- Change: full rewrite to ≤5 KB (R92's stricter ≤2,000-tok alternative, §7). Kept: layout diagram (family tree, `state/`, `docs/rewrite/`); placement rules T1-T6 (≤10 lines); `bash scripts/health.sh`; a delivery pointer to `docs/rewrite/delivery-log.md` (owner S11); the `docs/agents/*` pointers (LOC-24). Removed entirely: the "Plugins" catalog section (closes CLAUDE.md-2, -4); the MEMORY/ROUTING mandate wording (closes CLAUDE.md-1, route.py/ROUTING.md-1); the numbered Workflow list; every mention of `ROUTING.md`/`route.py`/`/route` (closes route.py/ROUTING.md-5).
- Commands: `wc -c CLAUDE.md`; `grep -c "Read \`MEMORY.md\` first\|ROUTING.md\|route.py\|/route\b" CLAUDE.md` (`0`).
- Done when: `wc -c` ≤ 5,120; the grep prints `0`.
- Rollback: `git revert`.

**S10-W3-9 — Delete `ROUTING.md`, `scripts/route.py` (sole deleter of both — CX-15).**
- Repo · depends on: S08-W3-7, S10-W3-8 (S08-W3-7 already deletes `plugins/plugin-creator/commands/` and its own route mentions — CX-15 narrows that step's scope to plugin-creator only, so this step is the ONLY place `ROUTING.md`/`scripts/route.py` are deleted, after S10-W3-8's CLAUDE.md rewrite has already stopped naming them).
- Files: `git rm ROUTING.md scripts/route.py`.
- Commands: `find /home/user/micky-psych-tools -name 'ROUTING.md' -o -name 'route.py'` — no output; `find /home/user/micky-psych-tools -path '*/commands/route.md'` — no output (S08-W3-7 already removed it).
- Done when: both empty; `bash scripts/health.sh --fast` still exits 0.
- Rollback: `git revert`.

**S10-W3-10 — MEMORY.md split.**
- Repo · depends on: S10-W3-8, S11-W3-2 (CX-39 — S11-W3-2 writes the delivery line at `MEMORY.md:11` at W1 entry, OQ12-a; this step must not overwrite it and keeps S11's line at `MEMORY.md:11` untouched).
- Files: rewrite `MEMORY.md`; create `docs/history.md`.
- Change: move `MEMORY.md:157-1137` ("Recent milestones", ~980 lines) verbatim into `docs/history.md` under a one-line header. Rewrite `MEMORY.md` to ≤6 KB: keep "Identity" (7-12) INCLUDING S11-W3-2's delivery line at `:11` verbatim; keep "Machine toolchain" (1137-1145), "Open threads" (1146-1148); delete "Current versions" (14-36, replaced by `validate.py --versions`, I19/S08 — not implemented here, only the table removed + a pointer line added); delete "Plugins at a glance" (38-157, R88); rewrite "Health check" to `bash scripts/health.sh`; add a "Current wave" line.
- Commands: `wc -c MEMORY.md`; `wc -l docs/history.md`; `diff <(sed -n '157,1137p' <saved-copy>) <(sed -n '2,$p' docs/history.md)` (save a pre-edit copy under the scratch dir, not `/tmp`) — byte-for-byte check.
- Done when: `wc -c MEMORY.md` ≤ 6,144; the diff is empty (R89/K11 "verbatim moves only").
- Rollback: `git revert`.

**S10-W3-11 — Archive the superseded plan.**
- Repo · depends on: none. Files: edit `docs/superpowers/plans/2026-07-10-improve-all-plugins.md`. Change: add a one-line header "completed; superseded by `docs/rewrite/`" (boxes are not ticked or re-verified).
- Commands: `head -3 docs/superpowers/plans/2026-07-10-improve-all-plugins.md`.
- Done when: the header line is present. Rollback: `git revert`.

### W5

**S10-W5-1 — Update MEMORY's living section with final numbers.**
- Repo · depends on: W3 and W4 exit (§10 W5 entry gate).
- Files: edit `MEMORY.md`. Change: "Current wave" → "W5"; one line recording the measured §9 totals once S12/the owner supplies them.
- Commands: `wc -c CLAUDE.md MEMORY.md`.
- Done when: the numbers match a fresh `wc -c` run.
- Rollback: `git revert`.

## 4. Evals

### 4.1 Cases

This spec owns no skill, so it adds no `claude plugin eval` cases. Its regression coverage is `scripts/test_validate.py`, `scripts/test_bump.py` (new, run by `python3 -m unittest discover -s scripts -p 'test_*.py'`), plus the `--help`/dry-run smoke commands per step in §3.

### 4.2 Conversion

No `evals.json` belongs to these units.

### 4.3 Live triggers

None. The routing-mandate removal is verified structurally (§3 grep checks); S12 owns the live routing smoke that exercises routing without the mandate (architecture §10 W3 exit).

### 4.4 Commands

| When | Command | Expected |
|---|---|---|
| every commit (fast path, via the hook) | `bash scripts/health.sh --fast` | exit 0, `health: OK` |
| before every commit not caught by the hook, and at every wave exit | `bash scripts/health.sh` | exit 0, `health: OK` |
| after any `validate.py`/`bump.py`/`route.py` edit | `python3 -m unittest discover -s scripts -p 'test_*.py' -q` | `OK` |
| after S10-W3-1/2 | `claude plugin validate --strict .claude-plugin/marketplace.json` | exit 0 |
| after S10-W3-8 | `wc -c CLAUDE.md` | ≤ 5,120 |
| after S10-W3-10 | `wc -c MEMORY.md` | ≤ 6,144 |

## 5. Acceptance criteria

1. `python3 scripts/validate.py` exits 0, shows the intent-lock entry as `WARN` not `FAIL`, no length-floor line — run it.
2. `validate.py` raises no uncaught exception when `mkt_path`/`man_path`/a declared `.mcp.json` is missing — unit test against a scratch fixture (`scripts/tests/fixtures/`).
3. `route.py --help` leaves `ROUTING.md` unmodified — `git status --short`.
4. `bump.py <plugin> patch` (no `--write`) makes zero file changes — `git diff --stat`.
5. `bump.py <plugin> patch --write` produces no `\uXXXX` in `plugin.json`, a trailing newline, and a new CHANGELOG entry — `grep -c '\\u'` = 0; `tail -c1 | xxd` = `0a`.
6. `marketplace.json` carries no `version` anywhere; post-W3 each entry is exactly `{name, source, category, keywords}` — the `python3 -c` assertions in §3.
7. `health.sh` and `health.sh --fast` both exit 0 on a clean checkout.
8. `.githooks/pre-commit` blocks a commit when `validate.py` would fail — S10-W0-11's scratch test.
9. Every plugin has a README, CHANGELOG (top == `plugin.json` version), and LICENSE — the loop in §1.1, re-run after S10-W0-8.
10. `CLAUDE.md` ≤5,120 bytes, no mandated-read wording — `wc -c` + `grep -c` in S10-W3-8.
11. `MEMORY.md`'s living section ≤6,144 bytes; `docs/history.md` holds the milestones verbatim — S10-W3-10's `wc -c` + `diff`.
12. `ROUTING.md`, `route.py`, every `commands/` dir absent after W3 — the `find` in S10-W3-9 plus `find plugins -type d -name commands`.
13. `find plugins -maxdepth 1 -type d` lists exactly the 7 family/standalone dirs after S10-W3-2.
14. All 27 assigned defects appear exactly once in §1.3, each with a wave and a fix step (self-check).

## 6. Trigger lock

Not applicable — no skill description or trigger phrase changes. (`/route`'s deletion is a slash command, not a description-driven trigger.)

## 7. Risks and OD sensitivity

| Risk | Note |
|---|---|
| Strict `yaml.safe_load` (S10-W0-1) fails `plugins/intent-lock/skills/intent-lock/SKILL.md`, which the old parser passed | Mitigated by the ratchet entry (S10-W0-1b); harmless no-op once S01/S02 fixes that file, in either order. |
| §2.7 I24's `$schema` value is unverified | Low risk — an unresolvable `$schema` string does not block `claude plugin validate`; §8 flags confirmation before S10-W3-1. |
| The skeleton PR (S10-W3-2) touches 10 plugins | Mitigated by K18: move-unchanged, one revert restores it, the folder-path route (S11/I16) needs no env edit on revert. |
| `bump.py --write` does not roll back on a post-write validation failure | Deliberate: the pre-check is R85's actual fix; a post-write failure means the write itself introduced a new problem, and surfacing it beats discarding a concurrent manual edit. |
| **OD3 (assumed a, merge families)**, if (b) 14 shells kept | The skeleton PR (S10-W3-1/2) does not happen; catalog keeps 14 version-less entries, no `renames`; CLAUDE.md's ≤5 KB target gets harder (§9 rises to ≤5,000 tok). |
| **OD9 (assumed a, dmi aliases)**, if (b) capability names only | S10-W3-2's `commands/` deletion is unchanged; the difference is entirely S02/S04/S05/S06's content. |
| **OD10 (assumed a, user-only maintenance skills)**, if (b) all model-invocable | Only affects S10-W5-1's recorded always-on total, not this spec's steps. |

## 8. Open questions

1. **CLOSED** (I17, §2.7; was an ASSUMES — CX-19): `ratchet.json`'s schema and the `rewrite_gate.py` import are now stated in S10-W0-1/-1b above.
2. `ASSUMES` (I24, §2.7): the `$schema` value. Not verified (no network access this session). Check: run `claude plugin marketplace init` in a scratch dir and read the value it emits, before S10-W3-1.
3. **CLOSED** (I19, §2.7; was an ASSUMES): S08-W3-1 confirmed to edit `scripts/health.sh`'s invocation path directly (CX-11).
4. ARCH-CONFLICT: none. The apparent tension (architecture §10 W0 lists only "strip entry versions"; this spec's task instructions add "and the top-level version") is not a conflict — §2.2's target tree and §7 both confirm the top-level version is eventually deleted; this spec performs it earlier (W0), which does not contradict the target state.
5. **CLOSED (OQ1-a, 2026-09-24).** The LICENSE text backfilled in S10-W0-8 is MIT, owner "Thanawat Suharit (Micky)", 2026 (matches gridgeist's).
6. Depends on S11: the exact wording of the "delivery pointer" line in S10-W3-8's rewritten `CLAUDE.md` (§3) should match whatever short phrase S11's own spec settles on for referring to `docs/rewrite/delivery-log.md` — not verified against S11's final text here beyond what its §2.7 (already read) shows; a final wording pass against S11's committed language is a cheap follow-up at execution time, not before.

(also wrote: none — this is the only spec S10 authored)
