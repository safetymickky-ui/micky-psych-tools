# Reconciliation pass 1 — S01–S10

Scope: specs `S01-alignment-core.md` … `S10-micky-repo.md`. Inputs: `phaseB/cx.md` (consistency
findings CX-1…CX-62), `phaseB/factcheck.md` (F1–F3 plus per-spec numeric corrections). Applied
every finding that names one of these ten specs; did the mechanical fixes (full step ids in
section 1.3 and in every `depends on`, size check). Read-only against both repos.

Format: finding id → spec(s) → what changed. Where a finding also names a spec outside S01–S10,
only the S01–S10 portion is listed here; the rest is that spec's own reconciliation pass.

## CX findings

- **CX-1** (alias skills created by S10's skeleton PR, not later) → **S10**: S10-W3-2 and the I23
  definition now create the 7 family alias skills in the same commit as the `commands/` delete,
  text copied verbatim from S02/S04/S05/S06 §2.2. **S04**: S04-W3-3 changed from "create
  `$P/skills/digest/SKILL.md`" to "verify it matches §2.2" (S10 creates it now). **S06**:
  S06-W3-4 changed from conditional-create to verify-only. **S02, S05**: no change (per the
  finding's own fix — S10 already creates their aliases from their existing §2.2 text).
- **CX-2** (S10-W3-2 dropping plugin-root files it doesn't explicitly move) → **S10**: S10-W3-2
  and I23 now say "move every plugin-root dir except `skills/`, `.claude-plugin/`, `commands/`"
  and gate the old-dir delete on `find plugins/<p> -type f` listing only `plugin.json`. **S01**:
  S01-W3-1 now confirms `lock-record.md` arrived and renames the caller name inside it. **S05**:
  S05-W3-1 changed from `git mv`-ing `CA/scripts/*` to verifying exactly one canonical
  `check-html.mjs` exists (deletes nothing itself).
- **CX-3** (family `plugin.json` has no owner) → **S10**: S10-W3-2 and I23 now create the three
  family `plugin.json` files (`$schema`, `version: "1.0.0"`, `description`, `author`,
  `keywords`). **S01**: S01-W3-5 changed from "create `plugin.json` (`version: 1.1.0`)" to "edit
  (not create); no hand-set version — released via `release.py alignment minor --write` after
  S08-W3-1". **S03**: new S03-W3-7 (evidence README/CHANGELOG/LICENSE merge, depends
  S03-W3-6, S04-W3-6). **S05**: new S05-W3-5 (same, for visuals, depends S05-W3-4). **S06**:
  S06-W3-1's dependency corrected to `S10-W3-2, S05-W3-1`.
- **CX-4** (no W0 smoke seeds) → new W0 steps, each 3 `smoke` cases against today's skill,
  depends `S12-W0-3`: **S07** S07-W0-1 (vault-keeper + empty-vault), **S04** S04-W0-1
  (psych-paper-digest) + S04-W0-2 (comprehensive-review), **S03** S03-W0-1
  (pubmed-research-note), **S06** S06-W0-1 (clinical-infographic), **S08** S08-W0-1
  (plugin-creator + refine-plugin), **S09** S09-W0-1 (firecrawl + gridgeist). "Waves" header
  rows updated on S03, S04, S06, S07, S08 to list W0.
- **CX-5** (H08/H09 don't really close in W1) → **S07**: new S07-W1-3 (depends S07-W1-1) —
  vault-keeper's Step 0 now calls `sink.py resolve` in place of the walk-up prose; the Step-0
  rewrite removed from S07-W2-1 (which now only adds the Handoff block + `.meta.json` asset
  filing). §1.3 rows vault-keeper-1/-2 (H08/H09) point at S07-W1-1 + S07-W1-3.
- **CX-6** (CR/PPD keep hard-coded MCP prefixes) → **S04**: S04-W1-1 and S04-W2-1 now replace
  the hardcoded `mcp__plugin_*` prefix text at the cited lines with S03's I05 resolution
  sentence, verbatim; done-when adds `grep -c "mcp__plugin_"` = 0.
- **CX-7** (I04 has no W2 text) → **S03**: new S03-W2-4 (depends S03-W2-1) creates
  `report-contract.md` and the 3 fixtures at the W2 (pre-move) path; S03-W3-1 now edits
  (not creates) `report-contract.md` since it already exists and moved with the skeleton;
  S03-W3-5 no longer recreates the fixtures. **S04**: S04-W2-2 now depends on S03-W2-4.
- **CX-8** (I11 filing sentence contradicts the architecture) → **S07** (owner): §2.6 now
  states two verbatim sentences — report (architecture §4.2) and visual (same pattern,
  `research-notes/visuals/`, both files named). **S05**: H-7 and **S06**: H-CI2 rewritten to
  adopt S07's visual sentence verbatim, with "Filing never publishes…" kept as a separate
  sentence. **S03, S04**: the I11 consumed-interface row now reads "report,
  `sink.py --kind report`".
- **CX-9** (asset kind stored twice, transfer drops `.meta.json`) → **S07**: `save` now writes
  `assets/<slug>.meta.json` (no `.kind` sidecar); I12's `hold_reason`/kind→receiver mapping
  read `kind` from `.meta.json`; a transferred asset item copies both files; S07-W2-1 and
  S07-W2-4 updated to match; tests updated.
- **CX-10** (audit verdicts: unrendered file could be filed as pass) → **S05**: §2.5 now says a
  non-empty `skipped` from a delegated `audit:visual` response forces `verdict: incomplete`
  (exit 3); `--kind code-explainer` is never delegated (I08 rejects it, exit 2).
- **CX-11** (validator path breaks at S08-W3-1) → **S08**: S08-W3-1 now also edits
  `scripts/health.sh` to call the new plugin-creator `validate.py` location (keeping S11-W0-3's
  two lines). **S05, S06, S08, S09**: every post-W3 `validate.py` command/acceptance line now
  reads `$VALIDATE --repo .` (defined as `python3 plugins/plugin-creator/scripts/validate.py`),
  with the pre-W3 repo-root form kept where the step actually runs before S08-W3-1.
- **CX-12** (release commands contradict I18 — no `--write`) → **S05** (S05-W2-6), **S08**
  (S08-W1-2), **S09** (S09-W1-2, S09-W3-4): all `bump.py`/`release.py` calls now pass
  `--write`; files = `plugin.json` + `CHANGELOG.md` only (not `marketplace.json`, already
  version-less from S10-W0-3); done-when adds "marketplace.json has no version". S08 §8 Q3
  (the "today's tool" ambiguity) deleted.
- **CX-13** (missing releases) → new release steps (`bump.py <p> <level> --write`): **S01**
  S01-W2-2 (intent-lock patch); **S02** S02-W2-2 (DI, PC patch); **S03** S03-W2-5
  (pubmed-research-note minor); **S04** S04-W1-3 (psych-paper-digest patch), S04-W2-3 (CR
  minor); **S06** S06-W1-5 (CI, CE patch), S06-W2-2 (CI minor); **S07** S07-W1-4 (minor),
  S07-W2-6 (minor).
- **CX-14** (misreads.md / .mcp.json defined twice) → **S01**: S01-W3-4 now reformats the
  `state/misreads.md` S10-W3-2 already moved there, instead of "creating" it; S01-W3-2 no
  longer deletes `misreads.md` (only `failure-conditions.md`). **S03**: S03-W3-1 drops the
  `.mcp.json` create-and-diff; done-when checks exactly one `.mcp.json` exists under `plugins`.
- **CX-15** (router deletion defined twice) → **S08**: S08-W3-7 now deletes only
  `plugins/plugin-creator/commands/` and this plugin's own route mentions — does **not** touch
  `scripts/route.py`/`ROUTING.md`. **S10**: S10-W3-9 is the sole deleter of both, depends
  `S08-W3-7, S10-W3-8`.
- **CX-16** (I01 name at W2 vs W3) → **S03, S04**: §2.6 now states the Step-0 sentence uses
  `intent-lock:intent-lock` at W2 and `alignment:intent-lock` from W3 (S03-W3-4/S04-W3-3).
  **S01**: I01's Handoff section gains a sentence allowing the bare skill name for callers that
  outlive the W3 rename. **S02**: kept the I01 sentence verbatim in the PC Step-0 handoff row,
  with "draft the plan, then offer to critique" as a separate sentence. **S09**: S09-W3-1 now
  depends on S10-W3-2 (the `alignment:intent-lock` name is only valid once the skeleton lands).
- **CX-18** (I20 contradicts architecture and itself) → **S08**: I20's frontmatter whitelist now
  allows `argument-hint` on any user-typeable skill, not just alias skills; the alias template
  quotes every placeholder (`name: "{{ALIAS_NAME}}"`, etc.); a dmi alias (disable-model-invocation
  + `Invoke …`-only body) is exempted from the order/`Use when` rules, capped at 150 chars —
  VAL-04 row updated to match.
- **CX-19** (ratchet/trigger-lock schema mismatch) → **S10**: S10-W0-1 now reads S12's
  `entries[]` schema; S10-W0-1b becomes `python3 scripts/rewrite_gate.py ratchet seed --check
  yaml-parse --write`, depends `S12-W0-1`. **S08**: VAL-06 and the Check-table intro now say
  ratchet/trigger-lock go through S12's `rewrite_gate.py` functions (imported, not
  reimplemented); §8 Q1 closed.
- **CX-20** (I25 invocation shape) → **S08**: VAL-14 and the I25 consumed row now read
  `node "$LEARN_HUB_DIR/scripts/check-contract.mjs" --dir
  "$MICKY_TOOLS_DIR/plugins/evidence/evals/fixtures" --json`, fail on exit 1; §8 Q2 closed.
- **CX-21** (committed lists have no owner) → **S08**: S08-W3-1 now creates
  `plugins/plugin-creator/references/lists/{synced-names,sibling-pairs,dmi-skills,
  fork-denylist,gate-skills}.md` from architecture §2.8/§6.3/OD9-OD10/§8; §8 Q1 text updated to
  say these are this spec's own, not S12's.
- **CX-22** (SessionStart hook test never fires in cloud) → **S08**: `hooks/hooks.json`'s guard
  changed from `test "$CLAUDE_CODE_REMOTE" = "1"` to `= "true"`.
- **CX-23** (eval layout deviates from I17) → **S07**: S07-W2-5, S07-W0-1, §2.1 tree, and the
  acceptance-criteria paths changed from `skills/<skill>/evals/<case>/` to
  `plugins/vault-keeper/evals/<skill>/<case>/`. **S10**: S10-W0-5's CLAUDE.md layout-diagram
  line changed from `skills/<skill>/evals/<case>/` to `evals/<skill>/<case>/`.
- **CX-27** (delivery log misused) → **S09**: S09-W5-1's evidence now records to this plugin's
  own `CHANGELOG.md`, not `docs/rewrite/delivery-log.md`.
- **CX-29** (H-11 handover has no step) → **S05**: §2.6 H-11's "Applied by S05-W2-7" changed to
  "Applied by S19-W2-1" (S19 is out of this pass's scope; the cross-reference is corrected).
- **CX-30** (atomic-swap check defined twice) → **S05**: S05-W2-7 deleted; S05-W2-8 rewritten
  to "push the learn-hub deletion branch" (depends `S05-W2-6, S16-W2-5`); every reference to
  "S05-W2-7/-8" elsewhere in the spec (§1.3 row, §2.1 tree note, §7 risk, §8 Q14) updated to
  say the merge/verification happens in S11-W2-3.
- **CX-32** (examples location contradicts architecture) → **S10**: S10-W3-2/I23 now move
  visuals members' `examples/` to the FAMILY root `plugins/visuals/examples/`, not the skill's
  own dir. **S06**: S06-W3-1 now also renames `examples/README.md` →
  `ppgl-perioperative-management.md` (matching S05-W2-4's ML rename) and fixes its link.
- **CX-33** (code-explainer `--source` flag has no implementer) → **S06**: S06-W3-3 now
  implements `--kind code-explainer --source <file>` directly in `V/scripts/check-html.mjs` +
  tests; the I07/§8 ASSUMES rows that said "S05 implements it" corrected to say this spec owns
  it (depends only on S05-W3-1 for the canonical script existing).
- **CX-34** (informal depends-on) → replaced with full step ids throughout: S01-W3-1 (→
  S10-W3-2), S01-W3-4 (→ S14-W2-2), S01-W3-5 (→ S02-W3-2, S02-W3-3), S02-W3-1/-2/-3 (→
  S10-W3-2), S03-W3-1 (→ S10-W3-2), S04-W3-1…4 (→ S10-W3-2), S05-W3-1 (→ S10-W3-2),
  S06-W3-1 (→ S10-W3-2), S05-W2-7 (deleted per CX-30), S07-W2-1/-4 (→ S15-W2-1), S07-W2-5
  (→ S12-W0-3), S07-W3-1 (→ S10-W3-2), S08-W3-1 (→ S10-W0-1/-2/-3), S08-W3-7 (→ S10-W0-4),
  S09-W3-1 (→ S08-W3-1), S10-W3-1 (→ S11-W3-1), S10-W3-8 (→ the 9 content specs' own last
  W3 step).
- **CX-35** (W2 "consumers before producers" not encoded) → depends-on additions: S03-W2-1 (+
  S15-W2-2), S04-W2-1 (+ S15-W2-2), S05-W2-3 (+ S16-W2-3), S05-W2-4 (+ S16-W2-3), S06-W2-1
  (+ S16-W2-3), S07-W2-1 (+ S15-W2-1).
- **CX-36** (W3 order: skeleton first, alignment before evidence/visuals) → depends-on
  additions: S03-W3-1/-2 (+ S01-W3-2), S04-W3-2 (+ S01-W3-2), S05-W3-1 (+ S01-W3-2), S06-W3-2
  (+ S01-W3-2), S07-W3-1/S08-W3-1/S09-W3-1/-2 (+ S10-W3-2).
- **CX-37** (live trigger runs not ordered) → depends-on additions of `S12-W3-2`: S01-W3-2,
  S02-W3-2, S02-W3-3, S03-W3-4, S04-W3-3, S05-W3-2, S06-W3-2, S08-W3-2, S08-W3-3, S09-W3-1.
- **CX-39** (same file, same/adjacent wave, no order) → **S08**: S08-W3-1 depends added
  `S11-W0-3` (both edit `scripts/health.sh`). **S10**: S10-W3-10 depends added `S11-W3-1`
  (both edit `MEMORY.md`; S10-W3-10 now explicitly preserves S11's delivery line at `:11`).
- **CX-42** (test files the health check never runs) → **S03**: `sources_lint.test.py` renamed
  to `test_sources_lint.py` (§2.1 tree, §2.5 Tests row, S03-W3-5, acceptance criteria).
  **S04**: `sweep.py.test.py` renamed to `test_sweep.py` (§2.1 tree, S04-W3-1, acceptance
  criteria).
- **CX-43** (W2 exit checks have no owner) → **S07**: new S07-W2-7 (OWNER; depends S07-W2-4,
  S15-W2-2, S14-W2-4, S11-W2-4) runs the fixture-report rehearsal and the no-digest check.
  **S04**: new S04-W2-4 (OWNER; depends S11-W2-2) runs the unattended `daily-random-review`
  check.
- **CX-44 / F2** ("21 codes total" vs the list summing to 26) → **S05**: I07-H and the parity
  text corrected to "26 codes total".
- **CX-45** (README/CHANGELOG/LICENSE created twice) → **S05** (S05-W2-6), **S08** (S08-W3-1),
  **S09** (S09-W3-1, S09-W3-2): changed from "create" to "edit" for files S10-W0-8 already
  backfills; depends-on gained `S10-W0-8`. **S07**: S07-W1-1 now writes `"license": "MIT"`
  explicitly (matches S10-W0-8's backfill); the OWNER question asking what license string to
  use, deleted.
- **CX-46** (runner call shapes) → **S01, S02**: §4.4 `eval.sh --smoke/--release` calls changed
  from `plugins/alignment` to bare `alignment`. **S03**: §4.4 changed to
  `eval.sh --smoke evidence -- --allow-tools Write` (passthrough via `--`, matching S12's
  wrapper).
- **CX-47** (S01/S02 circular-looking depends) → **S01**: S01-W3-5 depends corrected to
  `S02-W3-2, S02-W3-3` (not S02-W3-4, which would cycle).
- **CX-49** (S11 §2.6 sentences not carried) → item 1 (README "## Surfaces"): **S01** (S01-W3-5),
  **S03** (S03-W3-7, new step), **S05** (S05-W3-5, new step), **S08** (S08-W3-4, own README).
  item 4 (wave-exit "Ready for cloud delivery" line, per S11's exact I16 item 4 template read
  from S11's own spec): added to the last W3 step of **S01, S02, S03, S04, S05, S06, S07,
  S08, S09**, each filled with that plugin's own closed HIGH-defect ids.
- **CX-51** (`defaultEnabled: false` trade-off) → **S09**: new §8 item 6, **OWNER-QUESTION** —
  see "Findings requiring an owner decision" below.
- **CX-54** (lit-watch rename breaks the trigger lock) → **S04**: S04-W3-3 now re-keys
  `triggers.lock.json` via `rewrite_gate.py triggers remove/extract`, reason "renamed OD7-a".
- **CX-56** (S06-W1-1 done-when can't pass under `--input-type=module`) → **S06**: both
  occurrences of the `require('fs')`-under-ESM command rewritten to load `fs` via a second
  `import()`.
- **CX-57** (S08-W1-1 guard walks cwd up 3 parents) → **S08**: the guard now reads
  `MICKY_TOOLS_DIR` → marker, else stop — no cwd walk-up (matches R47/architecture §3.2).
- **CX-62** (`mkdir state/lit-watch` is a git no-op) → **S10**: dropped from S10-W3-2/I23;
  noted that S04-W3-1 creates the directory directly when it writes the migrated files.

## Factcheck findings

- **F1** (R37 cited for the ≥3-5-case rule; the real rule is R71) → **S03** (§4.1, §4.2), **S05**
  (§4.1), **S06** (§4.1): every "R37" reference for the case-count target replaced with "R71".
- **F2** — see CX-44 above (same fix, same root cause).
- **F3** (`scripts/eval.sh` grants no Bash/Write/AskUserQuestion by default) → §4.4 commands
  updated to pass `--allow-tools` (via S12's `--` passthrough) wherever a smoke- or
  release-tagged case needs more than the default read-only grant: **S01** (Bash, for
  `append-writes-ledger`), **S02** (confirmed none of the 10 cases need more — noted
  explicitly, no flag added), **S03** (Write), **S05** (Write for smoke; +`Bash(node *)` for
  release), **S06** (Write + `Bash(node *)`), **S07** (Write, Bash, AskUserQuestion — smoke
  case `verify-before-delete-fixture-inbox` needs all three), **S08** (Write, Edit,
  `Bash(python3 *)` for the release-only cases; smoke cases need nothing extra).
- **S03 §1.1** (pubmed-research-note/SKILL.md row gave body-only figures as the whole-file
  Lines/Bytes) → corrected 304/18,770 → 320/20,185.
- **S03 §1.3** (pubmed-research-note-7's fix step was "deferred") → corrected to `S10-W0-8`
  (the actual CHANGELOG-backfill step), wave W0.
- **S04 §1.1** (CR CHANGELOG.md row said 24 lines) → corrected to 29.
- **S04 §1.3** (psych-paper-digest-9's fix step was "deferred") → corrected to `S10-W0-8`,
  wave W0.
- **S10 §1.1** (marketplace.json row said 213 lines) → corrected to 212.

## Mechanical fixes (not tied to a specific finding id)

- **Section 1.3 fix-step columns**: rewrote to name full `Sxx-Wn-k` step ids in every row,
  across all ten specs. S01, S05, S06 needed a full rewrite (their "fix step"/"Problem → fix"
  columns held prose, no ids at all); S02, S03, S04, S07, S08, S09, S10 needed targeted fixes
  for rows still using an informal reference (`W1-1` without the spec prefix, `S10 W0` instead
  of a real step id, "deferred" with no step named).
- **`depends on` fields**: replaced every remaining informal reference (`"S10's skeleton-PR
  commit"`, `"S08"`, `"S12"`, `"S15"`, bare wave names) with a real step id, across all ten
  specs. Verified afterward with a repo-wide grep: no `depends on:` line in S01–S10 lacks a
  real `Sxx-Wn-k` id (the two accepted exceptions are `depends on: none` and S10-W5-1's
  wave-boundary gate `"W3 and W4 exit"`, which names a wave-exit gate, not a step).
- **Size**: S02–S08 and S10 are now over the nominal 40 KB target (34.7–53.4 KB). Every spec
  was already close to or over the line before this pass; every addition here is a finding fix
  or a mechanical correction the task required, so nothing was trimmed to stay under 40 KB —
  trimming any of it would drop required content, which the task explicitly permits leaving in.
  S05 is the largest (53.4 KB) because it is also the spec CX-1/CX-2/CX-3/CX-30 hit hardest.

## Findings requiring an owner decision

- **CX-51** (S09, `defaultEnabled: false` on firecrawl). The finding asks S11 to make this an
  explicit owner choice rather than a silent conditional; S09-W3-1 already follows whichever
  the owner picks. Recorded as `S09 §8 item 6, OWNER-QUESTION`: keep `defaultEnabled: false`
  plus a cloud setup-script enable block (fewer surprise tool loads), or drop the flag so
  firecrawl loads by default everywhere (always available). Only the owner can weigh that
  trade; I did not pick one.

No other finding naming an S01–S10 spec was left unapplied. Every CX-1…CX-62 and F1–F3 item
that named one of these ten specs has a corresponding edit above; items naming only specs
outside S01–S10 were left for those specs' own reconciliation pass, per the task's file scope.
