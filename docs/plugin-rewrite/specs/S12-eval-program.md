# Spec S12: eval and validation program — layout, runners, safety nets, trigger sets, conversion

| Field | Value |
|---|---|
| Repos | both |
| Units (today → target) | 16 `evals.json` files (118 real cases + 1 template, 2 cases; §1.1) → `plugins/<p>/evals/<skill>/<case>/` (micky), `learn-hub/evals/<skill>/<case>/` (learn-hub) case dirs per I17. `scripts/eval.sh` (micky, new). `scripts/eval-project-skill.sh` (learn-hub, new). `docs/rewrite/{ratchet.json,triggers.lock.json,baseline.md,h-coverage.md}` + generators (both, new). The 5 contested-family live trigger sets. The 20-prompt routing smoke set. |
| Waves | W0 (safety nets, runners, W1-unit smoke seeds); W3 (family conversion + live triggers before/after the description pass, release run at exit); W4 (learn-hub project-skill cases via the wrapper); W3/W5 exits (routing smoke); W5 (full release pass) |
| Owner decisions assumed | OD14-a (smoke/wave, free graders, 1 run, `--ablation none`; two-arm release at W3/W5 exits only); owner answers OQ2-a, OQ3, OQ8-a, OQ11-a (all confirmed 2026-09-24) |
| Defects closed | 0 of 0 assigned — no inventory defects of its own; serves the other specs (§1.4 has the OBS lines) |
| Interfaces owned | I17 |
| Interfaces consumed | I16 (S11), I18 (S10), I19 (S08), I20 (S08) |
| Depends on specs | S10 (I18: `validate.py` ratchet.json seeds against), S08 (I19/I20: W3 validator reads ratchet/lock; scaffold template follows this layout), S11 (I16: W0-d account check), S21 (I22: learn-hub `package.json` entries). Every other spec consumes I17 for its own conversion; S13/S17/S18/S07/S04/S06 author the W0 smoke-seed content whose shape only is defined here. |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

16 `evals.json` files exist (`find <repo> -name evals.json`), all `{skill_name, evals:[{id,name,prompt,expected_output,files:[],assertions:[]}]}`. Every case has `"assertions": []` (re-opened: `intent-lock/…:1-45`, `empty-vault/…:1-53`, `clinical-infographic/…:1-37`). No runner exists (`ls micky-psych-tools/scripts` → only `bump.py route.py validate.py`; no `.sh` under `learn-hub/scripts`); `docs/rewrite/` absent in both repos.

| Path | Cases | Converts to |
|---|---|---|
| micky `pubmed-research-note/…/evals.json` | 17 | S03 |
| micky `comprehensive-review/…/evals.json` | 5 | S04 |
| micky `psych-paper-digest/…/evals.json` | 12 | S04 |
| micky `intent-lock/skills/intent-lock/evals.json` | 8 | S01 |
| micky `intent-lock/skills/misread-capture/evals.json` | 5 | S01 |
| micky `plan-critique/…/evals.json` | 6 | S02 |
| micky `vault-keeper/skills/vault-keeper/evals.json` | 6 | S07 |
| micky `vault-keeper/skills/empty-vault/evals.json` | 6 | S07 |
| micky `clinical-infographic/…/evals.json` | 4 | S06 |
| micky `code-explainer/…/evals.json` | 6 | S06 |
| micky `firecrawl/…/evals.json` | 8 | S09 |
| micky `plugin-creator/…/templates/evals.json` | 2 (template, excluded from 118) | S08 (regenerated) |
| learn-hub `pubmed-research-note/…/evals.json` (fork) | 17 | dropped — fork retired W2 (H48) |
| learn-hub `comprehensive-review/…/evals.json` (fork) | 5 | dropped — fork retired W2 (H49) |
| learn-hub `intent-lock/skills/intent-lock/evals.json` (fork) | 8 | dropped — ledger merges to S01 (H06), W2 |
| learn-hub `intent-lock/skills/misread-capture/evals.json` (fork) | 5 | dropped — same fork retirement |

The 4 learn-hub files are byte-identical to their micky originals (`measure.py file`), confirming OBS "forks copied their evals byte-for-byte". Arithmetic: 83 real micky cases (11 files) + 35 fork cases (4 files, dropped) = **118**; the template's 2 cases sit outside that (OBS: "plugin-creator … ships an evals template for others").

`decision-interview`, `ml-concept-lab`, `concept-animation`, `sync-vault`, `ingest-article`, `pdf-pipeline` have **no** `evals.json` today — confirmed absent from the `find` list — so their cases are wholly new, authored by S02, S05, S13, S17, S18 against this spec's layout.

### 1.2 Descriptions

Not applicable — S12 owns no `SKILL.md`. For §4.3, full frontmatter was read for `intent-lock`, `misread-capture`, `decision-interview`, `plan-critique` (family 1); `pubmed-research-note`, `comprehensive-review`, `psych-paper-digest` (family 2 micky half); `clinical-infographic`, `concept-animation`, `ml-concept-lab`, `code-explainer` (family 3); `pdf-pipeline`, `ingest-article`, `ingest-slides`, `atomize-book` (family 4); plus `vault-keeper`, `firecrawl`. The synced counterparts come from this session's own listing, not files under `~/.claude/skills/synced/` (a different set).

### 1.3 Defects

None assigned (task line: "Defect prefixes: none — this spec has no inventory defects of its own"). No table row required by the self-check.

### 1.4 Other findings

OBS lines touching these units (`digests/S12.md:10-18`, quoted short):

- "decision-interview has none, no runner exists, and there are no should-trigger/should-not-trigger query sets." (alignment)
- "vault-keeper 6, empty-vault 6, firecrawl 8 … plugin-creator and refine-plugin have no evals at all, although the plugin ships an evals template for others." — matches §1.1.
- "atomize-book's Python helpers do have 354 stdlib unittest cases … but `npm test` does not run them."
- "Only CI (4 cases) and CE (6 cases) have evals/evals.json … CI eval #1 depends on a vault artifact (PPGL) that no longer exists." — CI=clinical-infographic, CE=code-explainer; the stale-PPGL case is dropped in §4.2.
- "34 evals across the 3 upstream skills (17/5/12) … Both forks copied their evals byte-for-byte." — 17+5+12 = pubmed-research-note+comprehensive-review+psych-paper-digest, matching §1.1.
- "The two forks now disagree on the digest gate." — the fork evals test a filing path this rewrite does not resurrect; dropped.

No new facts beyond the digest; §1.1 re-derives the 118-cases figure.

## 2. Target state

### 2.1 Location and tree

```
micky-psych-tools/
  scripts/ validate.py bump.py route.py health.sh eval.sh    # eval.sh new (W0)
  scripts/rewrite_gate.py test_rewrite_gate.py                # new (W0)
  docs/rewrite/ratchet.json triggers.lock.json baseline.md h-coverage.md   # new (W0)
  plugins/<family>/evals/<skill>/<case>/{prompt.md|case.yaml, graders/*.md}   # new (W3)
  plugins/evidence/evals/mocks/{pubmed,clinical-trials}/<tool>.md, fixtures/report-*.md   # owned by S03/S04
  .gitignore  # `evals/results/` line — owned by S10 (R48)

learn-hub/
  scripts/eval-project-skill.sh                                # new (W0)
  scripts/rewrite-gate.mjs scripts/lib/rewrite-gate.mjs rewrite-gate.test.mjs   # new (W0)
  docs/rewrite/ratchet.json triggers.lock.json baseline.md h-coverage.md   # new (W0)
  evals/<skill>/<case>/{prompt.md|case.yaml, graders/*.md}    # new (W4)
```

No `evals.json` remains after conversion (R70); no template evals under `references/`.

### 2.2 Frontmatter

Not applicable. Every example `prompt.md` in §4.1 uses only eval-format.md's documented keys; `expected_output` (the old key) never appears — mining renames it to a human-only `description:` or drops it (never to `expected_outcome` unless short).

### 2.3 Body outline

The four new file bodies:

**`ratchet.json`** — flat `{check_id, path, message}` array, one file per repo, plus a `"schema": 1` field (CX-19) so a consumer can detect a future format change instead of guessing keys:
```json
{"schema":1,"generated_at":"…","repo":"micky-psych-tools","entries":[
  {"check_id":"R70","path":"plugins/decision-interview/skills/decision-interview","message":"no evals/ (needs >=3, R71)"}
]}
```
S12-W0-1 writes the file with an empty `entries` array; the first entry (`yaml-parse`, intent-lock) is seeded by S10-W0-1b only (critique P4). A new `check_id` starts with today's violations pre-listed (`seed`); a listed pair **warns**, an unlisted one **fails**; a fix deletes its entry (`close`); the file may only shrink (`verify` fails if a `check_id`'s count grows versus the last commit, except a first-time `seed --new`); at W5 it is empty and checks become plain failures.

**`triggers.lock.json`** — every quoted phrase + every bare slash token from every `description`/`when_to_use`, plus a `removed` ledger and a `"schema": 1` field (CX-19):
```json
{"schema":1,"phrases":[
  {"phrase":"interview me","kind":"quoted","skill":"intent-lock","field":"description"},
  {"phrase":"/critique-plan","kind":"slash","skill":"plan-critique","field":"description"}
],"removed":[]}
```
`kind: quoted` reuses `measure.py`'s `QUOTE_RE` so the lock and `measure.py`'s reported phrases never disagree. `kind: slash` is a bare `/[a-z][a-z0-9-]*` token not already inside a quote — most slash mentions are unquoted prose (confirmed in `plan-critique`, `misread-capture`), so the quote regex alone misses them. `verify` fails if a recorded phrase no longer scans and is not in `removed`; `remove` is append-only, mirroring R87's rename ledger. Scan roots (critique F7): micky `plugins/*/skills/*/SKILL.md`; learn-hub `.claude/skills/*/SKILL.md` and `plugins/*/skills/*/SKILL.md`. When a frontmatter block fails `yaml.safe_load` (today: micky intent-lock; learn-hub concept-animation, ingest-animation, ingest-article, ingest-infographic), `extract` and `verify` read the `description:` value with a raw-line reader instead, so those skills' phrases are locked too (critique C2-06). `extract --skill <s>` limits a run to one skill; `remove --skill <s> --reason <r>` retires every phrase of a deleted or renamed skill; `remove --phrase <p> --skill <s> --reason <r>` retires one phrase.

**`baseline.md`** — one dated section per wave exit (W0/W3/W4/W5), a table of §9's "Now (evidence)" rows: both CLAUDE.md sizes, MEMORY.md, ROUTING.md, listing entries/chars, always-on tokens, synced listing, total paid tokens, per-description over-cap list, named skills' token sums. Cells needing an interactive session (`/doctor`, `/skill-doctor`) are `MANUAL — owner records after a real session`, never fabricated. Three more sections, which `baseline measure` never rewrites: `## W0 smoke` (per-case pass rates of the seeded units, S12-W0-8), `## Owner records` (one bullet per OWNER or verification step whose result has no other home: step id, date, result; the delivery log accepts only variable rows, I16.4 — critique P17) and `## W5 decisions` (S12-W5-3).

**`h-coverage.md`** — Appendix A (H01–H49) as a checklist:
```
- [ ] H07 plugin-creator-1 — cwd-bound; imperative description; stale Not-for — closed: no — wave: W1
```
Seeded once (W0) by parsing Appendix A rows (`^\| H\d\d \|`) out of `architecture.md`. A row whose Appendix A wave is split (H07 W1/W3, H10 W1/W2, H11 W1/W2) is seeded as two lines, `H07a … wave: W1` and `H07b … wave: W3` (likewise H10a/b, H11a/b), so each wave's gate sees only its own part: 52 lines (critique C2-16). A wave's exit gate re-parses this file's checkbox state (`grep -E '^- \[ \] H.*wave: W<n>$'`), never the architecture (frozen source vs. living record). micky's copy is canonical; rows close once per wave, inside the wave's tag step, and the file is then copied byte for byte to learn-hub (critique P33, C2-26).

### 2.4 References

None — S12 ships no `references/` (it is not a skill).

### 2.5 Scripts

| Script | Repo | CLI | Input | Exit codes | Tests |
|---|---|---|---|---|---|
| `scripts/eval.sh` | micky | `--smoke <plugin> [--against <ref>] [-- <extra args>]` / `--release <plugin> [--against <ref>] [-- <extra args>]`; `--against <ref>` runs today's `evals/<skill>/` case dirs against the plugin dir that held `<skill>` at `<ref>` (a `git worktree` of `<ref>`; the old dir is found by skill name, so it works across the W3 family move) and prints its with-arm score (critique C2-07); reads `EVAL_MODEL`, `EVAL_JUDGE_MODEL`, `EVAL_BUDGET` (unset→usage error; the value is the cap S12-W0-9 recorded for that mode, OQ3); `--release` passes `--runs 3` for `alignment` and `evidence` (the gate skills and the report writers) and `--runs 1` for every other plugin (OQ11-a); `--help` | `<plugin>` is the bare directory name under `plugins/` (never a path — the script prefixes `plugins/` itself, CX-46); everything after `--` is appended verbatim to the `claude plugin eval` call (e.g. `--allow-tools Write`, F3) | passthrough of `claude plugin eval`'s code; 2 on usage error | manual: 1 smoke run, W0 exit |
| `scripts/eval-project-skill.sh` | learn-hub | `eval-project-skill.sh <skill> --smoke\|--release [--against <ref>] [-- <args>]`; `--help`. `--against <ref>` copies `.claude/skills/<skill>/` from a `git worktree` of `<ref>` instead of the checkout (exit 3 "no baseline at <ref>" when the skill did not exist there). `--smoke`/`--release` set the same pinned `EVAL_MODEL`/`EVAL_JUDGE_MODEL`/`EVAL_BUDGET` flags `eval.sh` uses (CX-46); `--release` passes `--runs 1`, since no learn-hub project skill is a gate skill or a report writer (OQ11-a); other args pass through after `--`, or bare (kept for backward compatibility with a plain `<skill> [-- <args>]` call). | a name under `.claude/skills/` | 2 if skill absent; else passthrough | manual: 1 run vs `sync-vault`, W0 exit |
| `scripts/rewrite_gate.py` | micky | `rewrite_gate.py {ratchet,triggers,h-coverage,baseline} {seed,verify,close,remove,measure} [--repo .] [--write]`; `--help` per subcommand | `ratchet seed --check <id> --from <violations.json>`; `close --check --path`; `triggers extract [--skill <s>]`; `triggers remove --reason <r>` with `--skill <s>` (all phrases of a skill) or `--phrase <p> --skill <s>` (one phrase); `h-coverage seed --from <architecture.md>`; `close --id --wave`; `baseline measure --plugin-dir <p>` (repeatable) | 0 ok; 1 `verify` found a violation; 2 usage | `test_rewrite_gate.py` (unittest): shrink-only invariant, quoted+slash extraction, h-coverage round-trip, baseline degrade-to-MANUAL |
| `scripts/rewrite-gate.mjs` + `lib/rewrite-gate.mjs` | learn-hub | same 4 subcommands/flags, mirrored 1:1 so both repos share one schema | same | same | `rewrite-gate.test.mjs` (vitest), same 4 cases, run by `npm test` |

Dry run by default (`--write` commits); `--help` no side effects; JSON on stdout; UTF-8, trailing newline. Repo-root tooling, invoked `python3 scripts/rewrite_gate.py …` / `node scripts/rewrite-gate.mjs …`, matching `validate.py`'s precedent.

Both are also **importable libraries**, not only CLIs (CX-19): `scripts/rewrite_gate.py` exposes its subcommand functions (`ratchet_verify`, `triggers_verify`, `h_coverage_close`, …) for a caller in the same process, and `scripts/lib/rewrite-gate.mjs` exposes the Node twins. S08's W3 validator imports the Python functions for its VAL-06 ratchet check instead of re-implementing shrink/lock logic; S21's `skill-lint.mjs` check 9 imports `scripts/lib/rewrite-gate.mjs` the same way. Both file formats carry `"schema": 1` (§2.3) so an importing caller can detect a schema change instead of guessing keys.

### 2.6 Handoffs

None (I01/I04/I09/I11 own caller sentences). S12 defines a **smoke-seed requirement** (widened by CX-4: architecture §10 W0 item 3 seeds 3 smoke cases per W1 unit at W0, and I16.3 condition 4 needs a passing smoke suite before V2 and V3, not only before the original 7 units' own waves). By the W0 exit, each of these 10 units carries ≥3 `smoke` cases, each authored by its own spec in a dedicated W0 step:

| unit(s) | step | spec |
|---|---|---|
| vault-keeper, empty-vault | S07-W0-1 | S07 |
| psych-paper-digest | S04-W0-1 | S04 |
| comprehensive-review | S04-W0-2 | S04 |
| pubmed-research-note | S03-W0-1 | S03 |
| clinical-infographic | S06-W0-1 | S06 |
| plugin-creator | S08-W0-1 | S08 |
| firecrawl | S09-W0-1 | S09 |
| sync-vault | S13-W0-1 | S13 |
| ingest-article | S17-W0-1 | S17 |
| pdf-pipeline | S18-W0-1 | S18 |

The 7 units with a convertible `evals.json` (vault-keeper, empty-vault, psych-paper-digest, comprehensive-review, clinical-infographic, pubmed-research-note, firecrawl) re-tag 3 mined cases; the other 3 (no prior file, §1.1: sync-vault, ingest-article, pdf-pipeline; plus plugin-creator, whose only prior file is the scaffold template dropped in §4.2) write 3 new ones. Later eval steps extend these same dirs rather than replacing them.

### 2.7 Interfaces

**Owned: I17 — Eval program.**
- **Case layout:** `plugins/<p>/evals/<skill>/<case>/{prompt.md|case.yaml, graders/*.md}` (micky); `learn-hub/evals/<skill>/<case>/{…}`, run through `eval-project-skill.sh`. One directory per case, tagged from `smoke|trigger|negative|output|release` (multiple tags allowed; `--tag` unions).
- **Trigger grader regex:** `input_match: '"skill"\s*:\s*"(?:[\w-]+:)?<skill>"'` on `tool_used`/`tool:Skill`; a negative uses the same regex with `min:0, max:0, arm:both`.
- **`disable-model-invocation: true` (dmi) skills (CX-53):** a dmi skill removes its description from context, so a natural-language trigger case cannot fire it by design. Its positive case uses an explicit `/<name>` prompt instead (the slash-command form still invokes the skill); its negative cases stay natural-language near-misses, asserting the skill does NOT fire on prose alone. S20 follows this for `vault-coverage` and `check-repetition`.
- **`scripts/eval.sh` CLI:** `--smoke <plugin> [-- <args>]` → `claude plugin eval plugins/<p> --scaffold --tag smoke --ablation none --runs 1 --model "$EVAL_MODEL" --judge-model "$EVAL_JUDGE_MODEL" --max-cost-usd "$EVAL_BUDGET" --no-publish --json evals/results/<p>-smoke-<ts>.json <args>`. `--release <plugin> [-- <args>]` → `--scaffold --runs <n> --threshold 0.8` (n = 3 for `alignment` and `evidence`, 1 otherwise — OQ11-a), same models, `--trust-plugin --no-publish --json evals/results/<p>-release-<ts>.json <args>` (base invocation quoted verbatim from architecture §6.6, arch lines 581–582; the `<args>` passthrough after `--` is added by CX-46/F3, so a caller needing `--allow-tools Write` or similar for a case's `allowed_tools` can pass it explicitly). `<p>` is always the bare plugin directory name; the script itself prepends `plugins/`.
- **`scripts/eval-project-skill.sh` CLI:** builds a throwaway plugin under `$(mktemp -d)` — `.claude-plugin/plugin.json` (`{"name":"<skill>-eval-shim","version":"0.0.0"}`), `skills/<skill>/` copied from `.claude/skills/<skill>/`, `evals/<skill>/` copied if present. `--smoke`/`--release` set the same pinned model/budget flags as `eval.sh`'s two modes; runs `claude plugin eval <tmpdir> --scaffold <resolved flags> "$@"`, `trap 'rm -rf "$tmp"' EXIT` (CX-46). Both runners always pass `--scaffold`: the suites are owner-written, the documented condition, and without it every `scaffold_script` case starts in an empty workspace, so its "must not" graders pass with nothing to test (critique C2-01). Eval runs happen only in the cloud environment (setup step 4 installs bubblewrap and socat) or under WSL2: native Windows has no sandbox backend for Bash-granted cases (critique C2-02).
- **`docs/rewrite/{ratchet.json,triggers.lock.json,baseline.md,h-coverage.md}` formats + generators:** §2.3/§2.5.
- **Live trigger families + query sets:** §4.3 (the 5 families, 20 queries each), run with the routing-smoke method (critique F4): for each query, `claude -p "<query>" --output-format stream-json --verbose` from the multi-repo root (plus the `--add-dir` flags S12-W0-6 recorded, if any); read the first `Skill` tool_use `input.skill` and compare it with the expected name (no Skill call = "none"); one run per query (OQ11-a); a query whose outcome differs from the previous pass of the same set (it flips) runs 3 more times and passes when at least 2 of those 3 match. Each pass stops at the live-pass cap S12-W0-9 recorded (OQ3). Never skill-creator `run_eval`/`run_loop`: they measure a temporary command clone that competes with the real skill.
- **Routing smoke set:** §4.3 (20 prompts, expected skill, destructive-misroute flag).

**Consumed:**
- **I16 (S11):** `CLAUDE_CODE_PLUGIN_DIRS` schedule and W0-d (`claude plugin eval` enabled; fallback = skill-creator runner). Every invocation below **ASSUMES** d passed; if not, §3's W0 steps still build the layout, but no live run proceeds until S11 records d=yes.
- **I18 (S10):** W0-fixed `validate.py`/`bump.py`/`health.sh`/`.gitignore`. **ASSUMES** S10's W0 lands before S12-W0-1's ratchet seed — seeding the pre-fix (crashing, H13) validator would seed nothing.
- **I19 (S08):** the W3 validator reads `ratchet.json`/`triggers.lock.json`. **ASSUMES** S08 calls this spec's `verify` subcommands rather than re-implementing them — S08 to confirm.
- **I20 (S08):** the house skill shape §4.3's `Use when …` lines are drawn from. **ASSUMES** §1.2/§4.3 read the CURRENT descriptions; S08's house-shape pass may reword them, requiring a second §4.3 run (already required by §6.3).

## 3. Change steps

### W0

**S12-W0-0 (new, CX-40)** · both · OWNER · depends on: none (first W0 step, both repos)
- Actions: `git tag pre-rewrite && git push origin pre-rewrite` in micky-psych-tools and in learn-hub.
- Done when: `git ls-remote origin pre-rewrite` prints one line in each repo.
- Rollback: `git push origin --delete pre-rewrite` in each repo (only before any other step relies on the tag).

**S12-W0-1** · micky · depends on: S10-W0-1
- Files: create `scripts/rewrite_gate.py`, `scripts/test_rewrite_gate.py`, `docs/rewrite/ratchet.json`, `triggers.lock.json`, `h-coverage.md`.
- Change: implement the 4 subcommand groups (§2.5). `h-coverage seed` parses Appendix A from `architecture.md` (split rows as §2.3); `triggers extract` scans the micky roots of §2.3, with the raw-line fallback for YAML-invalid frontmatter; `ratchet.json` is written with no entries (S10-W0-1b seeds `yaml-parse`, critique P4).
- Commands: `python3 -m unittest scripts.test_rewrite_gate`; `rewrite_gate.py h-coverage seed --from docs/plugin-rewrite/architecture.md --write`; `rewrite_gate.py triggers extract --write`.
- Done when: `grep -c '^- \[' docs/rewrite/h-coverage.md` → 52; `triggers.lock.json` has ≥1 `kind: slash` entry; every micky `SKILL.md` has ≥1 lock entry or is listed in the command's output as having no phrases (intent-lock included, critique C2-06); `ratchet.json` `entries` is `[]`.
- Rollback: delete the 5 new files.

**S12-W0-2** · learn-hub · depends on: none within S12
- Files: create `scripts/rewrite-gate.mjs`, `scripts/lib/rewrite-gate.mjs`, `rewrite-gate.test.mjs`, `docs/rewrite/{ratchet.json,triggers.lock.json,h-coverage.md}`.
- Change: same 4 subcommands, Node stdlib, pure logic in `lib/`. `triggers extract` scans the learn-hub roots of §2.3 with the raw-line fallback. `h-coverage seed` reads `$MICKY_TOOLS_DIR/docs/plugin-rewrite/architecture.md` (cross-repo path); degrades with a stderr line if absent.
- Commands: `npm test -- rewrite-gate`; `rewrite-gate.mjs h-coverage seed --from "$MICKY_TOOLS_DIR/docs/plugin-rewrite/architecture.md" --write`; `rewrite-gate.mjs triggers extract --write`.
- Done when: `npm test` green; `h-coverage.md` 52 lines, content-identical to micky's; every learn-hub `SKILL.md` (both roots) has ≥1 lock entry or is listed as having no phrases (the 4 YAML-invalid skills included, critique C2-06).
- Rollback: delete the new files.

**S12-W0-3** · micky · depends on: S12-W0-1
- Files: create `scripts/eval.sh`.
- Change: `--smoke`/`--release` per §2.7's quoted invocations (both with `--scaffold`), plus `--against <ref>` (§2.5); `set -euo pipefail`; `mkdir -p evals/results`.
- Commands: `bash -n scripts/eval.sh`; `chmod +x scripts/eval.sh`.
- Done when: syntax check exits 0; no-args run prints usage, exits 2; `grep -c -- '--scaffold' scripts/eval.sh` ≥ 2; `--help` names `--against`.
- Rollback: delete the file.

**S12-W0-4** · learn-hub · depends on: S12-W0-2
- Files: create `scripts/eval-project-skill.sh`; edit learn-hub `README.md` (one scripts-table row; critique F12).
- Change: per §2.7 (with `--scaffold`) and §2.5 (`--against <ref>`); `trap 'rm -rf "$tmp"' EXIT`.
- Commands: `bash -n scripts/eval-project-skill.sh`; `chmod +x scripts/eval-project-skill.sh`.
- Done when: no-args exits 2; unknown skill exits 2 with a "not found" message; `grep -c -- '--scaffold' scripts/eval-project-skill.sh` ≥ 1; `--help` names `--against`.
- Rollback: delete the file.

**S12-W0-5** · both · depends on: S03-W0-1, S04-W0-1, S04-W0-2, S06-W0-1, S07-W0-1, S08-W0-1, S09-W0-1, S13-W0-1, S17-W0-1, S18-W0-1 (CX-4)
- Files: none (checklist item).
- Commands: per unit in the §2.6 table, `find . -path "*/evals/<unit>/*" -name prompt.md | xargs grep -l 'tags:.*smoke' | wc -l` — each must print ≥3.
- Done when: all 10 counts ≥3.
- Rollback: not applicable.

**S12-W0-6 (OWNER)** · both · depends on: S11-W0-9
- The owner confirms `claude plugin eval` is enabled — checklist row d, which S11-W0-9 already wrote in `delivery-log.md` (with the Bash-and-scaffold canary). If "no": record the fallback choice in `docs/rewrite/baseline.md` `## Owner records`; behavioural cases then use the skill-creator runner; the static layer is unaffected.
- Check i (critique F4): in a new multi-repo session, run `cd /home/user && claude -p "List every skill you can invoke and every CLAUDE.md file in your context. Names only." --output-format stream-json --verbose` and compare with the answer of the platform-started session (checklist row a, step 2). If the `claude -p` child sees fewer skills or CLAUDE.md files, re-run with `--add-dir /home/user/micky-psych-tools --add-dir /home/user/learn-hub` until they match. Record the flags that make them match in `## Owner records`; the live trigger and routing-smoke runs (S12-W3-2…-4, S12-W4-2/-3, S12-W5-2) use them.

**S12-W0-7 (new, CX-40)** · both · depends on: S12-W0-1, S12-W0-2
- Files: edit `docs/rewrite/baseline.md` in each repo (created empty by this step if the file does not already exist).
- Change: `rewrite_gate.py baseline measure --write` / `rewrite-gate.mjs baseline measure --write`, writing the W0 dated section (§2.3) from the repo's current state — CLAUDE.md sizes, listing entries, always-on tokens, etc.; cells needing an interactive session stay `MANUAL`.
- Commands: `python3 scripts/rewrite_gate.py baseline measure --write` (micky); `node scripts/rewrite-gate.mjs baseline measure --write` (learn-hub).
- Done when: `docs/rewrite/baseline.md` has one dated `## W0` section in each repo.
- Rollback: `git revert <this commit>`.

**S12-W0-8 (new, critique C2-07)** · both · depends on: S12-W0-5, S12-W0-6, S11-W0-9, S12-W0-9
- Files: edit `docs/rewrite/baseline.md` in each repo (`## W0 smoke` section, §2.3).
- Change: record the smoke baseline while every skill's text is still unchanged. micky: `bash scripts/eval.sh --smoke <p> -- --trust-plugin <args>` for pubmed-research-note, psych-paper-digest, comprehensive-review, clinical-infographic, vault-keeper, plugin-creator, firecrawl. learn-hub: `scripts/eval-project-skill.sh <s> --smoke -- --trust-plugin <args>` for sync-vault, ingest-article, pdf-pipeline. Write each case's pass rate and the case-set hash (`sha256sum` of the sorted `prompt.md` and `graders/*.md` of that skill).
  - `--trust-plugin`: neither runner passes it in smoke mode, and the learn-hub shim is a new temp dir every run, so a non-interactive run would stop at the first-run trust prompt (W0 executor finding, 2026-09-24). The suites are owner-written, the condition `--scaffold` already relies on.
  - `<args>` per unit, from the seed cases' own grants (Q33-a: per-command Bash, never the whole tool): pubmed-research-note, psych-paper-digest, comprehensive-review `--allow-tools Write`; clinical-infographic `--allow-tools "Write,Bash(node *)"`; vault-keeper (both skills) S07 §4.4's grant; plugin-creator `--allow-tools "Write,Edit,Bash(python3 *)"` (`scaffold-output`, `fix-then-release`); firecrawl none; sync-vault S13 §4.4's grant; ingest-article `--allow-tools "Bash(ls *),Bash(find *)"`; pdf-pipeline none.
  - Expected failures, recorded as the baseline rather than fixed: pdf-pipeline `slides-routing` (today's skill routes slide decks to atomize-book, H32).
- Done when: `## W0 smoke` lists all 10 units in the repo that owns them, each with ≥3 case rows; each run stays within the smoke-run cap S12-W0-9 recorded.
- Rollback: `git revert <this commit>`.

**S12-W0-9 (new, OQ3)** · micky · OWNER · depends on: S11-W0-9, S12-W0-7
- Files: edit micky `docs/rewrite/baseline.md` (`## Owner records`).
- Change: the owner sets the three eval caps from the cost per run that the check-d probe reported (S11-W0-9, `$E/w0d.json` and `$E/w0d2.json`; plan §8 Q30): `EVAL_BUDGET` for one smoke run, `EVAL_BUDGET` for one release run, and a USD cap for one live-trigger pass (OQ11-a: one number per cost point). Record the three values and the measured cost per run. Every later `eval.sh`/`eval-project-skill.sh` call exports the matching `EVAL_BUDGET`; a live pass stops when its cap is reached.
- Done when: the three caps and the probe's measured cost are in `## Owner records`. No cap is set before the probe runs.
- Rollback: not applicable (a record; a later record replaces it).

**S12-W0-T (new, CX-40)** · both · OWNER · depends on: every other W0 step in both repos (S10-W0-1…11, S11-W0-1…11, S12-W0-0…9, S21-W0-1…5, S21-W4a-1, S21-W4a-4, S21-W4b-1 (stage b before W1, OQ14-a), and the 10 smoke-seed steps of §2.6)
- Actions: close this wave's h-coverage rows in micky (`python3 scripts/rewrite_gate.py h-coverage close --id <H> --wave W0 --write`, one commit), copy `docs/rewrite/h-coverage.md` to learn-hub (one commit), then `git tag wave-0 && git push origin wave-0` in each repo, once its W0 steps are merged (critique P33).
- Done when: `git ls-remote origin wave-0` prints one line in each repo; `cmp` of the two `h-coverage.md` files exits 0.
- Rollback: `git push origin --delete wave-0` in each repo (only before a later wave tag depends on it).

### W1

**S12-W1-T (new, CX-40)** · both · OWNER · depends on: every W1 step in both repos
- Actions: close the W1 h-coverage rows in micky and copy the file to learn-hub (as S12-W0-T), then `git tag wave-1 && git push origin wave-1` in each repo, once its W1 steps are merged.
- Done when: `git ls-remote origin wave-1` prints one line in each repo; the two `h-coverage.md` files are identical.
- Rollback: `git push origin --delete wave-1` in each repo.

### W2

**S12-W2-T (new, CX-40)** · both · OWNER · depends on: every W2 step in both repos
- Actions: close the W2 h-coverage rows in micky and copy the file to learn-hub (as S12-W0-T), then `git tag wave-2 && git push origin wave-2` in each repo, once its W2 steps are merged.
- Done when: `git ls-remote origin wave-2` prints one line in each repo; the two `h-coverage.md` files are identical.
- Rollback: `git push origin --delete wave-2` in each repo.

### W3

**S12-W3-1** · micky · depends on: S01-W3-6, S02-W3-1, S03-W3-6, S04-W3-5, S04-W3-6, S05-W2-5, S06-W1-3, S07-W2-5, S08-W3-8, S09-W3-3
- Files: none directly (each family spec writes its case dirs against §4.2).
- Commands: `find plugins -name evals.json` (must print nothing).
- Done when: zero `evals.json` remain in micky.
- Rollback: not applicable.

**S12-W3-2 (live triggers, BEFORE)** · micky · depends on: S10-W3-2, S12-W0-6 (or the fallback) [CX-37]
- Commands: each family's set (§4.3) with the routing-smoke method (critique F4): for each query, `CLAUDE_CODE_PLUGIN_DIRS=/home/user/micky-psych-tools/plugins:/home/user/learn-hub/plugins claude -p "<query>" --output-format stream-json --verbose` from the multi-repo root (plus the `--add-dir` flags S12-W0-6 recorded, if any) — the variable is set for the child only, because under OQ10-a the families join the cloud value one at a time; read the first `Skill` tool_use `input.skill` and compare it with the expected name (no Skill call = "none"); one run per query (OQ11-a). Never skill-creator `run_eval`/`run_loop`: they measure a temporary command clone that competes with the real skill; in a multi-repo cloud session, against the CURRENT descriptions.
- Done when: a before-score is on record for every skill, all 5 families.
- Rollback: not applicable (measurement).

**S12-W3-3 (live triggers, AFTER)** · micky · depends on: S12-W3-2, and every family's description-pass step (CX-37): S01-W3-2, S02-W3-2, S02-W3-3, S03-W3-4, S04-W3-3, S05-W3-2, S06-W3-2, S08-W3-2, S08-W3-3, S09-W3-1
- Commands: re-run §4.3's sets, same method and the same child-only `CLAUDE_CODE_PLUGIN_DIRS`; a query whose outcome differs from its BEFORE outcome runs 3 more times, and at least 2 of those 3 must match (OQ11-a).
- Done when: no family's after-score falls below before by more than the 0.5-threshold noise band; a regression is reported to the owning family spec.
- Rollback: revert the description edit in the owning family's repo.

**S12-W3-4 (routing smoke, W3 exit)** · both · depends on: S12-W3-3, S11-W3-1 (V6: everything delivered, OQ10-a)
- Commands: run the 20-prompt routing smoke set (§4.3) with `claude -p`, multi-repo, everything delivered; read which skill fired per transcript.
- Done when: ≥17/20 correct AND 0 of the 3 destructive-flagged prompts misroute.
- Rollback: not applicable (gate); a fail blocks W3 exit until the owning family spec fixes phrasing and this step re-runs.

**S12-W3-5 (release run, W3 exit)** · micky · depends on: S12-W3-1, S12-W3-2, S12-W3-3, S12-W3-4
- Commands: `bash scripts/eval.sh --release <plugin> -- <the spec's §4.4 extra args>` per `alignment`, `evidence`, `visuals`, `firecrawl`, `plugin-creator`, `vault-keeper` (runs per OQ11-a: 3 for alignment and evidence, 1 for the rest); then the same with `--against pre-rewrite` for the baseline arm (critique C2-07).
- Done when: every with-arm score ≥ its `--against pre-rewrite` score (R77); a skill with no plugin at `pre-rewrite` needs every grader to pass.
- Rollback: a plugin below baseline is not released; its family spec reverts the change.

**S12-W3-T (new, CX-40)** · both · OWNER · depends on: every W3 step in both repos
- Actions: close the W3 h-coverage rows in micky and copy the file to learn-hub (as S12-W0-T), then `git tag wave-3 && git push origin wave-3` in each repo, once its W3 steps are merged.
- Done when: `git ls-remote origin wave-3` prints one line in each repo; the two `h-coverage.md` files are identical.
- Rollback: `git push origin --delete wave-3` in each repo.

### W4

**S12-W4-2 (new, CX-37)** · cloud · depends on: S12-W0-6 (or the fallback)
- Commands: Family 4 ({pdf-pipeline, ingest-article, ingest-slides, atomize-book, AS:pdf, AS:bullet-reconstruct}) and Family 5 ({atomize-book, digest-report, AS:obsidian-knowledge-vault}), same method as S12-W3-2 (the routing-smoke method), against the CURRENT (pre-W4) descriptions.
- Done when: a before-score is on record for every skill in both families.
- Rollback: not applicable (measurement).

**S12-W4-1** · learn-hub · depends on: S13-W1-9, S17-W4-3, S18-W4-4, S19-W4-9
- Commands: `for s in sync-vault ingest-article ingest-slides pdf-pipeline atomize-book vault-coverage check-repetition; do scripts/eval-project-skill.sh "$s" --smoke; done`.
- Done when: all 7 have ≥3 cases and a passing smoke run.
- Rollback: not applicable.

**S12-W4-3 (new, CX-37)** · cloud · depends on: S17-W4-4, S18-W4-5
- Commands: re-run Family 4 and Family 5's sets (§4.3), same method as S12-W4-2, after the PDF and atomize-book families' W4 description edits land.
- Done when: no family's after-score falls below before by more than the 0.5-threshold noise band; a regression is reported to the owning spec (S17, S18 or S19).
- Rollback: revert the description edit in the owning spec's repo.

**S12-W4-T (new, CX-40)** · learn-hub · OWNER · depends on: every W4 step
- Actions: close the W4 h-coverage rows in micky and copy the file to learn-hub (as S12-W0-T); `git tag wave-4 && git push origin wave-4`. The atomize-book import freeze already ended when S19-W4-9 passed (critique C2-27).
- Done when: `git ls-remote origin wave-4` prints one line; the two `h-coverage.md` files are identical.
- Rollback: `git push origin --delete wave-4`.

### W5

**S12-W5-1 (full release pass)** · both · depends on: W3, W4 exits
- Commands: `bash scripts/eval.sh --release <plugin>` per micky plugin, then with `--against pre-rewrite`; `scripts/eval-project-skill.sh <skill> --release`, then with `--against pre-rewrite`, per learn-hub project skill.
- Done when: every plugin/skill ≥ its `--against pre-rewrite` score (or every grader passes where no baseline exists).

**S12-W5-2 (routing smoke, W5 exit)** · both · depends on: S12-W5-1
- Commands: re-run the 20-prompt set with everything from both repos delivered.
- Done when: ≥17/20 and 0 destructive misroutes.

**S12-W5-3 (new, critique P13)** · both · depends on: S12-W5-1, S04-W5-1, S07-W5-1, S09-W5-1
- Files: `docs/rewrite/ratchet.json` (both repos); `scripts/rewrite_gate.py`, `scripts/lib/rewrite-gate.mjs` (+ tests); micky `docs/rewrite/baseline.md`.
- Change: (1) close every remaining ratchet entry — each must already be fixed; a still-failing entry blocks this step and goes back to its owning spec. (2) Make the checks fail hard: once `entries` is empty, a listed pair no longer turns a failure into a warning, and `ratchet seed` refuses to add entries (architecture §10 W5 exit). (3) Write `## W5 decisions` in micky `baseline.md`: gridgeist (S09-W5-1), lit-watch (S04-W5-1), OD4 (S07-W5-1), OD13, each with date and evidence — this is the architecture's "decision log".
- Done when: `ratchet verify` reports 0 entries in both repos; a test proves an unlisted and a formerly listed violation both fail; `grep -c '^## W5 decisions' docs/rewrite/baseline.md` = 1.
- Rollback: `git revert <this commit>`.

## 4. Evals

### 4.1 Cases

S12 owns no skill under test; the 3 cases below demonstrate the **conversion method** (§4.2) using `intent-lock`'s `evals.json` (§1.1). `intent-lock` is a gate, so the third case is the picker-absent fallback (R80, H02), not a plain output case. S01 ships the authoritative version under `plugins/alignment/evals/intent-lock/`; this is the shape S01 conforms to.

**Case 1 — trigger positive** (mined from id 1, `explicit-interview-me-trigger`)

`plugins/alignment/evals/intent-lock/trigger-interview-me/prompt.md`
```markdown
---
tags: [intent-lock, trigger]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 10
---

Interview me before you build this — I want the dashboard redesign spec locked down first.
```

`.../graders/skill-fired.md`
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?intent-lock"'
weight: 2
---
```

`.../graders/no-artifact.md`
```markdown
---
type: llm
weight: 1
---

PASS if the final response has no portable spec artifact to copy elsewhere, and no phase-0
internals (cold read, prediction v0, convergence gates) are narrated.
FAIL if a standalone artifact is produced, or phase-0 internals are printed.
```

**Case 2 — near-miss negative** (mined from id 8, `negative-scaffolding-request-plugin-creator-territory`)

`plugins/alignment/evals/intent-lock/negative-plugin-creator-territory/prompt.md`
```markdown
---
tags: [intent-lock, negative]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 10
---

/new-plugin — I want to scaffold a new plugin for tracking client invoices.
```

`.../graders/no-intent-lock.md`
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?intent-lock"'
min: 0
max: 0
arm: both
weight: 3
---
```

**Case 3 — gate picker-absent fallback** (new; R80/EVL-22/H02 — `allowed_tools` omits `AskUserQuestion` by construction)

`plugins/alignment/evals/intent-lock/fallback-no-picker/prompt.md`
```markdown
---
tags: [intent-lock, fallback]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 10
---

Build me the full reporting pipeline — pull from all our data sources, clean it, and
generate the exec summary however makes sense.
```

`.../graders/assumed-line.md`
```markdown
---
type: regex
target: last_message
pattern: '^Assumed: .+ — say if wrong\.'
flags: m
weight: 3
---
```

`.../graders/no-stall.md`
```markdown
---
type: llm
weight: 2
---

PASS if the run takes the broadest reading and states it in one `Assumed:` line rather than
stalling or asking in prose with no picker available.
FAIL if the run stalls, asks in prose, or guesses silently with no `Assumed:` line.
```

Remaining mined `intent-lock` cases (no full contents):

| Name | Tags | Prompt gist | Graders |
|---|---|---|---|
| `trigger-lock-the-goal` | trigger | "Lock the goal before we start: migration script." | `tool_used` (fired), `llm` (uncapped rounds) |
| `trigger-thai-lock-pao-mai` | trigger | Thai ล็อคเป้าหมาย | `tool_used` (fired), `llm` (Thai register) |
| `unprompted-offer-expensive-ambiguous` | output | No trigger phrase; expensive+ambiguous pipeline | `llm` (offers alignment, no silent guess) |
| `trigger-ask-me-until-you-understand` | trigger | "Ask me until you understand… don't guess." | `tool_used`, `llm` (no prose Qs, no scope creep) |
| `negative-precise-one-line-request` | negative | "Rename `usrId` to `userId`." | `tool_used` (min:0,max:0,arm:both) |

### 4.2 Conversion

All 16 files (ordered by owning spec):

| Old file | Cases | Converts to | Notes |
|---|---|---|---|
| `intent-lock/skills/intent-lock` | 8 | S01 → `plugins/alignment/evals/intent-lock/` | Mined 1:1 (§4.1); +1 new fallback case |
| `intent-lock/skills/misread-capture` | 5 | S01 → `.../misread-capture/` | Mined 1:1, graders hand-written (EVL-04) |
| `plan-critique/…` | 6 | S02 → `plugins/alignment/evals/plan-critique/` | Mined; +1 pressure case (R80, hurry+authority+sunk cost) |
| `pubmed-research-note/…` | 17 | S03 → `plugins/evidence/evals/pubmed-research-note/` | Mined to 3–5 (EVL-04); MCP cases get `evals/mocks/{pubmed,clinical-trials}/*.md` (S03, R75) |
| `comprehensive-review/…` | 5 | S04 → `plugins/evidence/evals/comprehensive-review/` | Mined 1:1 |
| `psych-paper-digest/…` | 12 | S04 → `plugins/evidence/evals/lit-watch/` | Mined to 3–5, renamed with the skill; window-math cases become regex over `sweep.py` state |
| `clinical-infographic/…` | 4 | S06 → `plugins/visuals/evals/clinical-infographic/` | 3 mined; id 1 (depends on the gone PPGL artifact) **dropped**, replaced with a synthetic fixture |
| `code-explainer/…` | 6 | S06 → `plugins/visuals/evals/code-explainer/` | Mined to 3–5; byte-fidelity assertion via `check-html.mjs --kind code-explainer --source` (S06-W3-3; OQ13-a) |
| `vault-keeper/skills/vault-keeper` | 6 | S07 → `plugins/vault-keeper/evals/vault-keeper/` | Mined; 3 re-tagged `smoke` |
| `vault-keeper/skills/empty-vault` | 6 | S07 → `.../empty-vault/` | Mined 1:1 (process cases, `tool_order` fits, EVL-10); 3 re-tagged `smoke` |
| `firecrawl/…` | 8 | S09 → `plugins/firecrawl/evals/firecrawl/` | Mined down to 3–5 |
| `plugin-creator/…/templates/evals.json` | 2 (template) | S08 | **Dropped** — not a skill's suite; S08's scaffold writes a real `evals/<skill>/trigger-basic/` case |
| learn-hub `intent-lock/skills/intent-lock` (fork) | 8 | — | **Dropped** — fork retired W2 (H06 ledger merge into S01) |
| learn-hub `intent-lock/skills/misread-capture` (fork) | 5 | — | **Dropped** — same |
| learn-hub `comprehensive-review` (fork) | 5 | — | **Dropped** — fork retired W2 (H49) |
| learn-hub `pubmed-research-note` (fork) | 17 | — | **Dropped** — fork retired W2 (H48); tested a filing path that no longer exists |

`decision-interview`, `ml-concept-lab`, `concept-animation` have no prior file — S02/S05 author 3–5 new cases. `sync-vault`, `ingest-article`, `pdf-pipeline` likewise (S13, S17, S18) — also 3 of the 7 W1 smoke-seed units (§2.6).

### 4.3 Live triggers

Two runners: isolated (§4.1/§4.2) and live (the routing-smoke method of §2.7, below). Shape `{query, should_trigger}` per skill — `should_trigger` is `true` only on that skill's own rows, `false` on every other row. Thai queries marked `[TH]`; `AS:`=`anthropic-skills:` (synced).

**Family 1 — {intent-lock, decision-interview, plan-critique, misread-capture}**

- Interview me before you build this — lock down the migration script scope first. → intent-lock
- [TH] ล็อคเป้าหมายก่อนนะ ผมอยากได้ระบบแจ้งเตือนสำหรับแอปคลินิก → intent-lock
- Ask me everything at once before touching the auth refactor. → decision-interview
- [TH] ถามมาทีเดียวให้ครบ ก่อนจะแก้ database schema → decision-interview
- Here's my Q3 launch plan — poke holes in it. → plan-critique
- [TH] วิจารณ์แผนนี้ให้หน่อย มันมีจุดอ่อนตรงไหนบ้าง → plan-critique
- You wasted my time — asked for a summary, got a full report. → misread-capture
- That's not what I asked for — record it so it doesn't recur. → misread-capture
- Stress-test my rollout plan before the team sees it. → plan-critique
- Resolve all open decisions in this ticket at once. → decision-interview
- /new-plugin — scaffold a plugin for invoice tracking. → plugin-creator
- Rename `usrId` to `userId` in src/auth.ts. → —
- Make an infographic of the PPGL report. → clinical-infographic
- Search PubMed for evidence on lithium and renal function. → pubmed-research-note
- Run today's paper digest. → lit-watch
- Just use your judgement — no need to ask. → —
- Explain what this function does. → code-explainer
- Empty the vault. → empty-vault
- Animate the mechanism of SSRIs. → concept-animation
- Sync the vault to Supabase. → sync-vault

**Family 2 — {pubmed-research-note, comprehensive-review, lit-watch, AS:psych-paper-digest, AS:deep-research, AS:daily-random-review}**

- Should I use bupropion for smoking cessation with a seizure history? → pubmed-research-note
- [TH] หางานวิจัยเรื่อง ketamine กับ treatment-resistant depression ให้หน่อย → pubmed-research-note
- Write a comprehensive review of bipolar II — whole chapter, all modalities. → comprehensive-review
- [TH] รีวิวทั้งโรค schizoaffective disorder ให้หน่อย → comprehensive-review
- Run today's literature digest across my watchlist. → lit-watch
- [TH] มีเปเปอร์ใหม่ไหมวันนี้ → lit-watch
- Give me today's psych paper digest, 8–12 papers across subspecialties. → AS:psych-paper-digest
- Pick a random unreviewed board topic and generate a full review. → AS:daily-random-review
- Research the competitive landscape for AI note apps and write a report. → AS:deep-research
- Compare EHR vendors on cost/support/integration — write it up. → AS:deep-research
- Scrape this drug label page and summarize it. → firecrawl
- Explain the pharmacokinetics code in this Python script. → code-explainer
- Grade my last CRQ answer. → AS:exam-analysis
- Empty the vault of my catatonia notes. → empty-vault
- Just give me a one-line answer, no report needed. → —
- Chart my clinic's patient volume by quarter. → dataviz
- Critique my research proposal outline. → plan-critique
- Turn this lecture PDF into notes. → ingest-slides
- Ingest this PDF of a journal article. → ingest-article
- Add lithium to my watchlist. → —

**Family 3 — {clinical-infographic, concept-animation, ml-concept-lab, code-explainer, dataviz}**

- Make a clinical infographic of this antipsychotic dosing report. → clinical-infographic
- [TH] สรุปเป็นอินโฟกราฟิกให้หน่อย → clinical-infographic
- Animate the HPA axis feedback loop step by step. → concept-animation
- [TH] ทำแอนิเมชันอธิบาย mechanism ของ SSRI → concept-animation
- Build an explorable — drag the learning rate, watch gradient descent converge. → ml-concept-lab
- [TH] ทำภาพอธิบายแบบโต้ตอบสำหรับ backpropagation → ml-concept-lab
- Walk me through this recursive function, line by line. → code-explainer
- [TH] อธิบายโค้ดนี้ทีละบรรทัด → code-explainer
- Chart our monthly no-show rate by clinic. → dataviz
- Plot this CSV of lab values over time. → dataviz
- Write a comprehensive review of ADHD pharmacotherapy. → comprehensive-review
- Refactor this function, remove the duplicate loop. → —
- Design a landing page for our clinic's app. → gridgeist
- Search PubMed for evidence on stimulant misuse. → pubmed-research-note
- Render a video file, not an interactive page. → —
- Give me a static one-pager of clinic KPIs. → dataviz
- Sync the new figures to Supabase. → sync-vault
- Empty the vault of the animation assets. → empty-vault
- Audit this code for bugs before shipping. → —
- Critique the plan I wrote for this feature. → plan-critique

**Family 4 — {pdf-pipeline, ingest-article, ingest-slides, atomize-book, AS:pdf, AS:bullet-reconstruct}**

- I uploaded a PDF — get it into Learn. → pdf-pipeline
- Here's a PDF, process it into Learn. → pdf-pipeline
- Ingest this article PDF into the hub. → ingest-article
- Reconstruct and add this study to Articles. → ingest-article
- Digest this PsychiTalk deck into the hub. → ingest-slides
- Review this deck slide by slide for high-yield content. → ingest-slides
- Extract this textbook into vault notes. → atomize-book
- Add this book to the Learn hub — make notes from this textbook. → atomize-book
- Merge these two PDFs, rotate page 3. → AS:pdf
- Bulletise this dense review, drop the references. → AS:bullet-reconstruct
- Write a comprehensive review of PTSD treatment. → comprehensive-review
- Make an infographic from this PDF report. → clinical-infographic
- Grade my exam answers from this PDF. → AS:exam-analysis
- Interview me before deciding this book's outline. → intent-lock
- Reformat this report into a clean printable PDF. → AS:document-to-pdf
- Summarize this PDF into three sentences, nothing more. → —
- Extract tables from this scanned PDF via OCR. → AS:pdf
- Combine five chapter PDFs into one file. → AS:pdf
- Animate the concept from chapter 3 of this book. → concept-animation
- Sync the vault — notes are already written. → sync-vault

**Family 5 — {atomize-book, digest-report, AS:obsidian-knowledge-vault}**

- Extract this textbook and atomize it into vault notes. → atomize-book
- Add this book to the Learn hub — make notes from this textbook. → atomize-book
- Chapter 4's notes missed the treatment section — expand them. → atomize-book
- Re-sync the vault after hand-editing a few notes. → atomize-book
- Digest the report the micky vault just handed you. → digest-report
- File this vault evidence report as atomic Learn notes. → digest-report
- Convert this chapter into atomic, wikilinked Obsidian notes. → AS:obsidian-knowledge-vault
- Build a knowledge graph from this chapter for Thai Board prep, in Obsidian. → AS:obsidian-knowledge-vault
- Atomize this chapter into Obsidian, not the Learn hub. → AS:obsidian-knowledge-vault
- Check coverage of the CBT textbook already imported. → atomize-book
- Ingest this journal article PDF into the Articles tab. → ingest-article
- Process these lecture slides into the hub. → ingest-slides
- Sync my edited vault notes to Supabase. → sync-vault
- Save this report to the psych vault with a MOC entry. → vault-keeper
- Pick a random board topic, review it into my Obsidian vault. → AS:daily-random-review
- Empty my psych vault into Learn — I'm done with it. → empty-vault
- Make an infographic of the notes just atomized. → clinical-infographic
- Critique the note structure I drafted. → plan-critique
- Check repetition in the notes just imported. → check-repetition
- Interview me on which chapters to prioritize before atomizing. → intent-lock

**Routing smoke set (20 prompts, `claude -p`, everything delivered)**

- Prompt → Expected skill | Destructive risk
- /new-plugin — scaffold a plugin for invoice tracking. → plugin-creator | no
- Rename `usrId` to `userId` in src/auth.ts. → none | no
- Empty the vault. → empty-vault | **yes**
- Sync the vault to Supabase. → sync-vault | **yes**
- Just use your judgement — no need to ask. → none | no
- Search PubMed for evidence on lithium and renal function. → pubmed-research-note | no
- Run today's literature digest. → lit-watch | no
- Chart our monthly no-show rate by clinic. → dataviz | no
- Refactor this function, remove the duplicate loop. → none | no
- Grade my last CRQ answer. → AS:exam-analysis | no
- Give me a one-line answer, no report needed. → none | no
- Ingest this journal article PDF into the Articles tab. → ingest-article | no
- Merge these two PDFs, rotate page 3. → AS:pdf | no
- Summarize this PDF into three sentences, nothing more. → none | no
- Add this book to the Learn hub — make notes from this textbook. → atomize-book | no
- Pick a random board topic, review it into my Obsidian vault. → AS:daily-random-review | no
- Check repetition in the notes just imported. → check-repetition | no
- Empty my psych vault into Learn — I'm done with it. → empty-vault | **yes**
- Critique the plan I wrote for this feature. → plan-critique | no
- You wasted my time — record that so it doesn't happen again. → misread-capture | no

Acceptance (§6.3 point 3, J2 graft #10): ≥17/20 correct AND 0 of the 3 destructive-flagged rows ever misfire.

### 4.4 Commands

| Command | What | When |
|---|---|---|
| `bash scripts/eval.sh --smoke <plugin>` | free-grader run, `--ablation none --runs 1`, pinned models, `--max-cost-usd $EVAL_BUDGET` | every wave, per touched plugin (OD14-a) |
| `bash scripts/eval.sh --release <plugin>` | two arms, `--runs 3` for alignment and evidence (gate skills, report writers) and `--runs 1` for the rest (OQ11-a), `--threshold 0.8`, `--trust-plugin`, capped by the release-run cap (S12-W0-9) | W3 and W5 exits only |
| `scripts/eval-project-skill.sh <skill> --tag smoke` | throwaway-plugin smoke run | every wave touching that learn-hub skill |
| `scripts/eval-project-skill.sh <skill> --release` (`--runs 1`, OQ11-a) | throwaway-plugin release run | W4, W5 exits |
| `rewrite_gate.py ratchet verify` / Node twin | shrink-only check | every commit (micky: `health.sh --fast` in the S10-W0-10 pre-commit; learn-hub: the S21-W0-3 pre-commit) |
| `rewrite_gate.py triggers verify` / Node twin | no silent phrase removal | every commit |
| `claude -p "<query>" --output-format stream-json --verbose` × 1 per query, a flipped query × 3 more (OQ11-a), first `Skill` tool_use (critique F4), capped per pass (S12-W0-9) | live trigger accuracy | before/after each family's description pass; once more at W5 |
| `claude -p "<prompt>"` × 20, multi-repo | routing smoke | W3, W5 exits |

## 5. Acceptance criteria

1. `find micky-psych-tools learn-hub -name evals.json` returns nothing after W3 (micky) / W4 (learn-hub).
2. Every case dir under `plugins/*/evals/*/*/` and `learn-hub/evals/*/*/` has `prompt.md` (or `case.yaml`) and ≥1 file under `graders/`.
3. No `prompt.md` uses `expected_output` — `grep -rl expected_output plugins/*/evals learn-hub/evals` prints nothing.
4. `docs/rewrite/ratchet.json` exists in both repos; from W5 onward `.entries` is `[]`.
5. `docs/rewrite/triggers.lock.json` exists in both repos, `.phrases.length > 0`; `triggers verify` exits 0 on a clean tree.
6. `docs/rewrite/h-coverage.md` has 52 rows (H07, H10, H11 split in two) in both repos, content-identical; micky's copy is canonical.
7. `docs/rewrite/baseline.md` has one dated section per wave exit in both repos.
8. `scripts/eval.sh` and `scripts/eval-project-skill.sh` exist, executable, `bash -n` clean.
9. The 5 family sets and the routing smoke set are committed as fixtures (e.g. `docs/rewrite/live-triggers/*.json`) matching §4.3's tables verbatim.
10. The W3 and W5 routing smoke runs both record ≥17/20 and 0 destructive misroutes.
11. Every unit in the §2.6 table (10 skills) has ≥3 `smoke`-tagged cases by the W0 exit.
12. `git ls-remote origin pre-rewrite` and `wave-0` through `wave-4` each print one line, in each repo they apply to (CX-40).
13. `docs/rewrite/baseline.md` has a `## W0` dated section in both repos before any other wave's section (CX-40).

## 6. Trigger lock

Not applicable per-skill — S12 owns no `SKILL.md`. The lock **mechanism** is owned here (§2.3, §2.7); `triggers.lock.json` scans every other spec's skill, not hand-authored. The W0 seed found `kind: quoted` (English+Thai) and `kind: slash` entries across the 17 skills read for §1.2/§4.3 — slash confirmed unquoted in `plan-critique`, `misread-capture`, `pubmed-research-note`, and 9 others. Per-skill kept/moved/removed decisions belong to each unit's own §6 table; they consume I17's `verify`, not redefine it.

## 7. Risks and OD sensitivity

| Risk | Effect on S12's units |
|---|---|
| K7 — description edits drop a trigger or shift routing between siblings | Caught by §4.3's before/after runs and `triggers verify`; blocks the owning family's W3 step |
| K10 — `claude plugin eval` unavailable, noisy judges, rate-limit zeros | Gated by W0-d (S11); the static layer (layout/ratchet/lock/`tool_used`/`regex`/`file_exists`) works regardless. Judge noise mitigated by pinning `--judge-model` and R73 (regex for long output) |
| K16 — scope creep: a light edit becomes re-voicing | `ratchet verify` catches a new unlisted violation mid-wave; prose re-voicing with no new check failure stays review-only (R81) |

**OD sensitivity (OD14):**
- **(a), assumed:** smoke per wave + two-arm release at W3/W5 exits only — §3 reflects it (`--release` only in S12-W3-5, S12-W5-1).
- **(b)** smoke only: those steps drop `--release`; R77's comparison becomes owner review of two transcripts; §5 criterion 10 loses its score basis.
- **(c)** full two-arm every wave: every `smoke` command in §4.4 becomes `--release`; `EVAL_BUDGET` rises (~700 agent runs, architecture §11 OD14).

## 8. Open questions

1. **CLOSED (CX-19).** S08's W3 validator calls this spec's `verify` subcommands rather than re-implementing shrink/lock logic. `scripts/rewrite_gate.py` and `scripts/lib/rewrite-gate.mjs` now expose their subcommand functions as an importable library (§2.5) specifically so S08 and S21 can import instead of re-implementing.
2. **ASSUMES:** the W0 ratchet seed finds few/zero violations because S10's W0 work lands first (S12-W0-1's dependency); if delayed, S12-W0-1 waits.
3. **ASSUMES:** the architecture's 5 contested families (§6.3) are exhaustive (not re-derived here). A later 6th pairing (e.g. `atomize-book` vs `vault-coverage`'s "check coverage of X") is a candidate for the W3/W5 routing-smoke results to surface.
4. **Settled, not a conflict:** "118 cases" (architecture line 317) vs. this spec's raw sum of 16 files (120) is resolved in §1.1 — the gap is the `plugin-creator` scaffold template's 2 cases, not one of the "118 real" ones. OBS sub-totals (digest lines 11, 17) corroborate.
5. **Check that settles S12-W0-6 (OWNER):** whether `claude plugin eval` is enabled (I16-d) is unknown here — settled by S11's W0 run, recorded in `delivery-log.md`; §3's dependent steps (S12-W3-2..S12-W5-2) name the fallback rather than assume yes.
6. **CLOSED (OQ2-a, 2026-09-24) — F3 (factcheck.md).** `eval-format.md` strips `Bash`/`Write`/`Edit`/`WebFetch`/`WebSearch` from a case's session unless `--allow-tools` is passed to `claude plugin eval`; several specs' cases need those tools (S01, S02, S05, S06, S07, S08). This spec resolves it by giving `eval.sh`/`eval-project-skill.sh` an args passthrough after `--` (CX-46, §2.5/§2.7), so an affected spec's §4.4 states the extra flag explicitly (as S03 already did by hand) rather than needing a second runner. Owner confirms this is the intended fix rather than, e.g., a fixed always-on `--allow-tools` set on every run.
