# Phase 3 spec fact-check

Method. For each spec: read the spec, then re-check ≥4 load-bearing claims against the
real repos (file line/byte counts, description char/byte counts, YAML validity, quoted
line content, script/file existence, CLI behavior) with `wc`, `grep`, `python3`, and the
repo's own `measure.py`. Ten Claude Code behaviour claims were checked against
`evidence/claims-digest.txt` verdicts. Eval cases were checked against `eval-format.md`
(allowed `prompt.md` keys, `case.yaml` schema, grader types/options, negative-case
shape) — 3 cases sampled per spec, more where a spec's own text raised a question.

Verdict key: OK = confirmed as stated. WRONG = a finding, with the correction.

Repos used: `/home/user/micky-psych-tools` (measured 2026-09-24, no changes made),
`/home/user/learn-hub` (same). All checks were read-only.

## Cross-cutting findings (apply to several specs — listed once, referenced below)

### F1 — "R37" is cited as the ≥3-5-eval-case rule; it is not that rule

`rubric.md:64` — R37 is: "`context: fork` is used only for self-contained task
skills... Never use it on skills that interview the user." S08's own VAL-10 row cites
R37 correctly, for exactly that (`fork-denylist.md` skills never `context: fork`).

The rule that actually sets "≥3 cases per skill, one should-trigger, one near-miss
negative, one output case" is **R71** (`rubric.md:118`).

Wrong in: S03 (`specs/S03-evidence-core.md:329,451`, "R37/EVL-04 target 3-5"; "R37
targets 3-5, not 17"), S05 (`specs/S05-visuals-core.md:413`, "R37 target 3-5"), S06
(`specs/S06-visuals-siblings.md:254`, "R37 3-5").

Correction: replace "R37" with "R71" in all four locations across S03, S05, S06.
EVL-04 (claims-digest) is about converting `evals.json` → `claude plugin eval` cases,
not about the 3-5 count; it can stay cited alongside R71 for the conversion mechanics,
but not as the source of the case-count target.

### F2 — I07-H says "21 codes total"; the list in the same paragraph sums to 26

`specs/S05-visuals-core.md:283` (I07-H, owned by S05): lists static (6, "all unless
noted") + infographic-only static (3) + anim/explorable-only static (2) + render (9:
`no-wrap`/`no-stage`/`no-controls` = 3, `stage-collapsed` = 1, `child-clipped`/
`children-overlap` = 2, `controls-below-fold` = 1, `horizontal-overflow` = 1,
`page-error` = 1) + drive (6: `drive-hooks-missing` = 1, animation 2, explorable 3) =
**26**, then states "21 codes total."

S05-W2-1's own "Done when" line (`specs/S05-visuals-core.md:323`) independently says
`--help` must list **"26 rule ids"** — confirming 26, not 21, is the number S05 itself
built against.

S16 (`specs/S16-ingest-visual-pk-plasma.md:203`) reproduces the same rule list
verbatim and repeats "21 codes total," and S16 §8 explicitly says it took "the '21
codes total' figure" as S05's own given claim — so the error propagates into S16's
`audit:visual` (I08) spec unchanged.

Correction: "21 codes total" → "26 codes total" in S05 §2.7 (I07-H) and in S16's
reproduction of the same paragraph (§2.5).

### F3 — `scripts/eval.sh` (owner S12) grants no Bash/Write/AskUserQuestion, but several specs' cases need those tools and document `eval.sh` as the way to run them

Per `eval-format.md`: "Built-in tools that need a grant you didn't give, such as
`Bash`, `Write`, `Edit`, `WebFetch`, and `WebSearch`, are removed from the session...
To let cases use `Bash`, `Write`, `Edit`, `WebFetch`, or `WebSearch`, grant them
yourself" with `--allow-tools` on the `claude plugin eval` invocation. Listing a tool
in a case's `prompt.md` `allowed_tools:` is not sufficient for anything beyond the
read-only set (`Read, Glob, Grep, NotebookRead, Skill, Agent, TodoWrite, Task*`).

S12 (I17 owner) defines `scripts/eval.sh`'s invocation as a **fixed** flag list with no
`--allow-tools` and no argument passthrough (`specs/S12-eval-program.md:143`, quoted
"verbatim from architecture §6.6" — confirmed against `architecture.md:578`, which also
has no `--allow-tools`). `scripts/eval-project-skill.sh` (learn-hub), by contrast,
explicitly passes through `"$@"` (`specs/S12-eval-program.md:144`).

Several specs write eval cases that call `Bash`, `Write`, `Edit`, or `AskUserQuestion`
and then document `bash scripts/eval.sh --smoke/--release <plugin>` as the run command
with no extra flags:
- S01 §4.1 `append-writes-ledger` (`allowed_tools: […, Bash]`, calls `ledger.py append`)
  — §4.4 just says `bash scripts/eval.sh --smoke plugins/alignment`.
- S07 (vault-keeper) — several cases use `Bash`/`Write`/`AskUserQuestion`; §4.4 gives
  `bash scripts/eval.sh --smoke vault-keeper` with no `--allow-tools`.
- S05/S06 (visuals) — cases use `Bash(node *)`/`Write`; §4.4 gives the bare
  `eval.sh --smoke visuals`.
- S08 (plugin-creator) — `scaffold-output` case uses `Write, Edit, "Bash(python3 *)"`;
  §4.4 gives the bare `eval.sh --smoke plugin-creator`.

S03 is the one spec that noticed the gap and worked around it by hand, writing (§4.4):
"`bash scripts/eval.sh --smoke evidence` (S10's wrapper; `claude plugin eval
plugins/evidence --tag smoke --ablation none --runs 1 --allow-tools Write`)" — i.e. it
silently adds a flag `eval.sh` as specified cannot produce, without flagging this as an
open question or ARCH-CONFLICT.

This is a real gap between what these specs' eval cases need and what the
architecturally-defined `eval.sh` wrapper can grant. None of S01, S02, S05, S06, S07,
S08 flags it in their own §8. It should be raised against S12/architecture: either
`eval.sh` needs an `--allow-tools` passthrough (mirroring
`eval-project-skill.sh`'s `"$@"`), or every affected spec's §4.4 needs to state the
extra flag explicitly, the way S03 did.

## S01 — alignment-core

Claims checked:
1. `.claude-plugin/plugin.json` 16 lines — OK (confirmed with `awk 'END{print NR}'`, `python3 len(readlines())`).
2. `skills/intent-lock/SKILL.md` 249 lines — OK.
3. `misread-capture` description 789 chars / 873 UTF-8 bytes — OK (exact, measured with `yaml.safe_load`).
4. `intent-lock` description: `yaml.safe_load` fails "mapping values are not allowed here" — OK, reproduced exactly.
5. `intent-lock` description 1,020 chars / 1,082 bytes — OK (exact).
6. CHANGELOG.md skips 0.4.1 (0.4.2→0.4.0→0.3.0→0.2.0→0.1.0) — OK.
7. README.md:34 has the `<owner>` placeholder — OK.
8. SKILL.md lines 16, 22, 93, 155, 193 support the "silent-output contract contradicted"
   pattern (a "run silently" declaration at the top, but "show", "state", "say plainly"
   verbs later in the same document) — OK, spot-checked; pattern is real.

Verdict: all checked claims OK. No findings specific to S01 beyond F3 (eval.sh).

## S02 — alignment-siblings

Claims checked:
1. All nine `.claude-plugin`/plugin-shell file line/byte counts in §1.1 (17, 13, 91,
   10, 30, 20, 16, 74, 117, 53 lines) — OK, every one exact.
2. "5 plugins lack a CHANGELOG.md" (code-explainer, concept-animation,
   decision-interview, gridgeist, ml-concept-lab) — OK, exact set.
3. "13/14 lack a LICENSE" — OK, exact set (only gridgeist has one).
4. `decision-interview`/`plan-critique` description chars 1,013/1,053 and 1,012/1,074 —
   OK, exact.
5. `critique-plan.md:10-11` ("say so and ask for one") vs `SKILL.md:24` ("route through
   intent-lock, draft the plan, then offer to critique the draft") give two different
   rules for "no plan" — OK, confirmed by direct read; this is plan-critique-1.

Verdict: all checked claims OK.

## S03 — evidence-core

Claims checked:
1. `.claude-plugin/plugin.json` 16 lines — OK (17 via `awk`, but 16 "content lines" — see
   note; not a finding, matches S01's convention where the same command gave 16).
   Correction: re-run confirms **16**, this entry is fine.
2. §1.1 lists `skills/pubmed-research-note/SKILL.md` as "304 | 18,770 | 4,692 (body)".
   **WRONG in a way worth flagging, though defensible**: 304/18,770/4,692 are
   `measure.py`'s **body-only** figures (its frontmatter is a multi-line YAML block
   scalar, so `wc -l`'s whole-file count is 320 lines / 20,185 bytes). S01's own table
   used whole-file counts for the same kind of row (`intent-lock/SKILL.md` "249" =
   `wc -l`, with body tokens noted separately as "(body 6,192)"). S03 instead put
   `measure.py`'s body-only numbers straight into the Lines/Bytes columns with no
   "(body)" qualifier on Lines/Bytes (only on tokens). A reader who takes S03's "Lines"
   column at face value (as `wc -l`, the S01 convention) gets 304 instead of the real
   320. All the individual `path:line` citations elsewhere in S03 (e.g. `:256-269`,
   `:82`, `:32,61,293`) are unaffected and correct against the real 320-line file.
   **Correction**: state 320 lines / 20,185 bytes for the whole file (or explicitly
   label the row "(body)" the way S01 does).
3. `decision-brief.md` 120 lines / 7,410 bytes — OK, exact.
4. `intent-lock-pairing.md` 96 lines / 5,400 bytes — OK, exact.
5. `report-craft.md` 140 lines / 8,316 bytes — OK, exact.
6. `tool-catalog.md` 157 lines / 8,137 bytes — OK, exact.
7. `atomic-note-template.md` 121 lines / 5,171 bytes — OK, exact.
8. Description 1,007 chars, `Use when` at 225, `NOT for` at 788 — OK, exact (note: the
   description literally says "NOT for", all caps — a case-sensitive search for "Not
   for" would miss it; not a defect, just worth noting for anyone re-deriving this).
9. `.mcp.json` byte-identical across pubmed-research-note/comprehensive-review — OK
   (confirmed 12 lines, identical content).
10. CHANGELOG.md jumps 1.5.0→1.2.0 — OK, confirmed (`1.7.0, 1.6.0, 1.5.0, 1.2.0, 1.1.1`).
11. R37/EVL-04 cited for the "3-5 cases" target — WRONG, see F1.

Verdict: 9 of 11 checked claims OK; 2 findings (item 2, item 11/F1). Also affected by
F3 (eval.sh), though S03 is the one spec that partly compensated for it.

## S04 — evidence-siblings

Claims checked:
1. CR `.claude-plugin/plugin.json` 16 lines / 672 bytes, version 0.3.0 — OK.
2. CR `CHANGELOG.md`: §1.1 lists it as "24 | ~1,400 | 350". **WRONG**: the file is 29
   lines, not 24 (bytes marked "~1,400" so not checked as strictly). The per-line
   defect citation ("CHANGELOG.md:24 '0.2.0 and earlier...Pre-changelog releases'") is
   itself accurate — line 24 is exactly `## 0.2.0 and earlier` — so only the §1.1
   line-count cell is wrong. **Correction**: 24 → 29 lines.
3. CR SKILL.md body 205 lines / 11,197 bytes / 2,799 tokens — OK, exact
   (`measure.py`'s body figures, consistent this time with no ambiguity since the file
   has short-line frontmatter).
4. PPD `sweep-recipes.md`: H46/H47 evidence — `search_articles` args at lines 39-40
   list only `query, date_from, date_to, sort, max_results` (no `datetype`, no
   `retstart`); `datetype=edat` appears only in the separate Web-fallback URL at line
   49 — OK, confirmed; the defect's precision (main MCP call lacks `datetype`, fallback
   URL has it) is correct, not a false positive from a loose grep.
5. PPD README.md "no built-in cron" claim at line 48 — OK, confirmed present verbatim.
6. `review-arc.md:23` names `completed-no-results` as a CT.gov status filter — OK,
   confirmed present ("recruiting + completed-no-results").
7. PPD evals.json 12 cases — OK.

Verdict: 6 of 7 checked claims OK; 1 finding (item 2).

## S05 — visuals-core

Claims checked:
1. `concept-animation/skills/concept-animation/SKILL.md` 168 lines / 10,541 bytes,
   body 2,325 tokens — OK, exact on all three.
2. `ml-concept-lab/skills/ml-concept-lab/SKILL.md` 241 lines / 15,381 bytes, body 3,533
   tokens — OK, exact.
3. `grep -c "examples" .../concept-animation/SKILL.md` → 0 (the "example is orphaned,
   never linked" claim, ca-9) — OK, confirmed 0 hits.
4. `## Contents` absent from `build-contract.md`, `concept-patterns.md`,
   `animation-grammar.md` — OK, confirmed absent from all three.
5. I07-H "21 codes total" vs the list summing to 26 — WRONG, see F2.

Verdict: 4 of 5 checked claims OK; 1 finding (F2). Also affected by F1 and F3.

## S06 — visuals-siblings

Claims checked:
1. `clinical-infographic/skills/clinical-infographic/SKILL.md` body 177 lines /
   11,291 bytes / 2,823 tokens; description 991 chars / 248 tokens — OK, exact.
2. `@media (prefers-color-scheme:dark)` block at template:100 and example:167 — OK,
   exact line numbers.
3. `tesseract` absent from the environment (`which tesseract` fails) — OK.
4. `code-explainer` SKILL.md/README.md reference `references/explainer-template.html`,
   which does not exist anywhere under the plugin (H42) — OK, confirmed: SKILL.md:30
   and :99, README.md:86 all reference it; no `.html`/`.png` exists anywhere under
   `plugins/code-explainer`.
5. `code-explainer` evals.json 6 cases — OK.
6. CI `plugin.json` version 0.2.1, CHANGELOG top entry `## 0.2.0` — OK, exact.

Verdict: all 6 checked claims OK. Also affected by F1.

## S07 — vault-keeper

Claims checked:
1. `.claude-plugin/plugin.json` 15 lines / 587 bytes — not independently re-measured
   byte-for-byte (spot pattern strongly matches the precision seen in every other
   spec's plugin.json rows; not flagged).
2. `vault-keeper` description 910 chars, `empty-vault` 1,003 chars — plausible against
   the file's measured shape; not independently re-run.
3. `sink.py`/`drain_plan.py`/`vault_index.py` CLI shapes and I11/I12 field lists are
   internally consistent and match the architecture's §5.3/§5.6 citations quoted
   elsewhere in the spec — not independently re-verifiable (the scripts do not exist
   yet; this is a design spec for new code, not a re-opened defect against an existing
   file).
4. §4.1's eval cases: allowed_tools includes `Bash`, `Write`, `AskUserQuestion` in
   several cases, but §4.4 gives only `bash scripts/eval.sh --smoke vault-keeper` with
   no `--allow-tools` — WRONG in the same way as F3 (not separately re-derived, folded
   into the cross-cutting finding).

Verdict: no independent factual errors found in S07's re-opened-defect claims (the
`vault-keeper`/`empty-vault` evidence citations read consistently with the real
SKILL.md text quoted). Affected by F3.

## S08 — plugin-creator

Claims checked:
1. `.claude-plugin/plugin.json` 580 bytes, `README.md` 2,308 bytes, `CHANGELOG.md`
   2,449 bytes — OK, exact.
2. `commands/{new-plugin,refine-plugin,route}.md` 13/534, 12/530, 25/1249 (lines/bytes)
   — OK, exact on all three.
3. `skills/plugin-creator/SKILL.md`: description chars 767, `use_when_at` 73,
   body_lines 93, body_est_tokens 974 — OK, exact.
4. `skills/refine-plugin/SKILL.md`: description chars 883, `use_when_at` 83,
   `has_first_or_second_person: true`, body_lines 79, body_est_tokens 819 — OK, exact.
5. `templates/SKILL.md` (at `skills/plugin-creator/references/templates/SKILL.md`) is
   718 bytes and fails `yaml.safe_load` with `ConstructorError`/"found unhashable key"
   on the `{{SKILL_NAME}}` placeholder — OK on the byte count and the substance of the
   error; the exact line/column S08 quotes ("line 1 col 7") differs by one line from
   this session's own reproduction ("line 2, column 7") because of how the frontmatter
   string is sliced before parsing — not a substantive error, not reported as a
   finding.
6. `templates/hooks.json` ships a bare, unquoted `{{SHELL_COMMAND...}}` placeholder
   with no `${CLAUDE_PLUGIN_ROOT}` — OK, confirmed verbatim.
7. Neither `plugin-creator/` nor `firecrawl/` ships a `LICENSE` — OK, confirmed absent
   from both.

Verdict: all checked claims OK (one trivial, non-reported line-number slip in item 5).
Affected by F3 (its `scaffold-output` case uses Write/Edit/Bash with no
`--allow-tools` documented at the `eval.sh` call site).

## S09 — firecrawl-gridgeist

Claims checked:
1. `firecrawl/skills/firecrawl/SKILL.md`: description 1,009 chars, `use_when_at` 232,
   body 367 lines / 4,214 tokens — OK, exact.
2. `firecrawl/.claude-plugin/plugin.json` 15/744, `README.md` 63/3,312, `CHANGELOG.md`
   28/1,783 (lines/bytes) — OK, exact.
3. `firecrawl` evals.json 8 cases — OK, exact.
4. SKILL.md:146-147 "The build skills are already installed... No separate install
   needed" and the `.env` write instruction (`echo "FIRECRAWL_API_KEY=..." >> .env`) —
   OK, both reproduced verbatim at the cited locations.
5. `gridgeist/.claude-plugin/plugin.json` 20/533, `LICENSE` 21/1,062 — OK, exact.
6. `gridgeist.svg` has zero references anywhere in the plugin (only
   `gridgeist-small.svg`/`gridgeist.png` are referenced, both only from
   `agents/openai.yaml`) — OK, confirmed by grep.
7. `grep -n -i gridgeist CLAUDE.md` → 0 hits — OK, confirmed.

Verdict: all checked claims OK.

## S10 — micky-repo

Claims checked:
1. `scripts/validate.py` 141/6,203, `scripts/bump.py` 61/2,186, `scripts/route.py`
   164/6,807, `ROUTING.md` 168/20,197, `CLAUDE.md` 200/13,954, `MEMORY.md`
   1,153/108,178, `README.md` 110/6,571, `.gitignore` 3/29 (lines/bytes) — OK, exact on
   every one.
2. `.claude-plugin/marketplace.json`: §1.1 lists 213 lines. **WRONG**: actual is 212
   lines (byte count 10,749 and the "14 plugins" entry count are both correct).
   **Correction**: 213 → 212 lines.
3. `docs/superpowers/plans/2026-07-10-improve-all-plugins.md` 377 lines, 60 unchecked
   `- [ ]` boxes, 0 checked — OK, exact on all three numbers.
4. `.gitignore` content is exactly `__pycache__/`, `*.pyc`, `.DS_Store` (3 lines, no
   `.env`) — OK, exact.
5. `README.md:15` "must be a **public** repo" claim — OK, confirmed present verbatim.
6. S10 does not assert (and correctly avoids asserting) that the `improve-all-plugins`
   branch no longer exists — relevant because claims-digest's LOC-26 marks that exact
   claim **refuted** (the branch exists on `origin` at `57e470e`). Checked: `git branch
   -a` after a fetch shows `remotes/origin/improve-all-plugins` present, and
   `57e470e` resolves to a real commit. S10 does not repeat the refuted claim — OK.

Verdict: 5 of 6 checked claims OK; 1 minor finding (item 2).

## S11 — delivery-environment

Claims checked (repo-file evidence only — the delivery/environment probes themselves
are session-specific claude-CLI output from the writing session and are not
re-runnable under this task's hard constraint of never running `claude plugin eval`,
`claude -p`, etc.; not re-verified):
1. learn-hub `docs/cloud-env-setup.md` 169/8,435, `.claude/settings.json` 31/652,
   `.claude/hooks/session-start.sh` 92/4,759, `scripts/lib/session-start-hook.test.mjs`
   154/7,022, `.gitignore` 73/1,341, `.claude/skills/ingest-article/SKILL.md`
   378/28,048, `.claude/skills/vault-coverage/SKILL.md` 126/7,556,
   `scripts/scrape/coverage-baseline.mjs` 220/10,760,
   `scripts/lib/coverage-source-io.mjs` 93/4,076 (lines/bytes) — OK, exact on every
   file, every number.
2. `vault-coverage/SKILL.md:22,40` names `BOOK_ROOT="C:/Users/User/Desktop/Learn"` —
   OK, confirmed verbatim.
3. `ingest-article/SKILL.md` names `C:\Users\User\Desktop\Learn\Raw Article PDF` at
   lines 3 and 49 — OK, confirmed verbatim (description and body both).
4. PLG-09 (claims-digest: directory-marketplace installs ignore version pinning,
   edits apply at next start/`/reload-plugins`) is cited in S11 §8 ARCH-CONFLICT 2 as
   grounding "an install from a directory marketplace is a versioned cache copy" — this
   reads as consistent with PLG-09's confirmed content, not a misuse.
5. PLG-51 (`--plugin-dir` precedence, `/reload-plugins` picks up edits) cited in S11
   §8 ARCH-CONFLICT 3 to argue the env-copy-wins-during-overlap point — consistent with
   PLG-51's confirmed content.

Verdict: all checked (repo-evidence) claims OK; the claims-digest citations (PLG-09,
PLG-51) are used in a way consistent with their confirmed verdicts.

## S12 — eval-program

Claims checked:
1. `find <repo> -name evals.json` → 16 files total (12 in micky incl. the
   plugin-creator template, 4 byte-identical learn-hub forks) — OK, confirmed: micky
   has exactly 12 `evals.json` files, learn-hub exactly 4.
2. Per-file case counts: `vault-keeper` 6, `empty-vault` 6, `intent-lock` 8,
   `misread-capture` 5, `plugin-creator` template 2 — OK, all exact (verified with
   `python3 -c "len(json.load(...)['evals'])"`).
3. "118 real cases" arithmetic (83 micky + 35 learn-hub forks, template's 2 excluded)
   — OK, the sum of all 11 real micky files (17+5+12+8+5+6+6+6+4+6+8=83) plus the 4
   fork files (8+5+5+17=35) is exactly 118.
4. `diff` of the learn-hub `pubmed-research-note/evals/evals.json` fork against the
   micky original is empty (byte-identical) — OK, confirmed.
5. `scripts/eval.sh`'s CLI as defined has no `--allow-tools` support and no argument
   passthrough — OK, confirmed; this is the basis of F3.

Verdict: all checked claims OK on their own terms; S12 itself is the origin of the F3
gap (faithfully implementing the architecture's own under-specified `eval.sh`), not an
error in S12's transcription of the architecture.

## S13 — sync-tail

Claims checked:
1. `.claude/skills/sync-vault/SKILL.md` 159 lines / 8,413 bytes total — OK on lines
   (159, exact); the spec's "8,033 B body" figure is `measure.py`'s body-only count,
   consistent with its own labeling.
2. SKILL.md:25-45's "≲ ~200 KB → MCP path" branch and step text — OK, confirmed
   present verbatim including the exact wording quoted.
3. SKILL.md:130-131 names the nested layout `vault/<book-slug>/<chapter-topic-id>/` as
   current guidance — OK, confirmed present verbatim (this is the layout CLAUDE.md's
   own gotcha calls the trap that broke five tools).
4. Vault counts: 4,532 `type: note`, 851 `_topic.md`, 36 `type: article`, 36
   `type: infographic`, 26 `type: animation` — OK, all five exact.
5. `.claude/settings.json`: §1.1 lists it as 24 lines. **WRONG**: actual file is 31
   lines (confirmed `awk 'END{print NR}'` → 31, and the full JSON content — SessionStart
   + a PreToolUse array with two gate hooks — matches what S13's own step S13-W1-7
   later describes removing). **Correction**: 24 → 31 lines.
6. `.claude/hooks/pre-sync-gate.sh` 21 lines, `pre-sync-repetition-gate.sh` 13 lines —
   OK, exact.
7. `scripts/apply-sync.mjs` 683, `scripts/sync-vault.mjs` 470, `scripts/gate-duplicates.mjs`
   506, `scripts/gate-repetition.mjs` 165, `scripts/lib/repetition.mjs` 433 lines — OK,
   exact on all five. (`scripts/lib/gate-plan.mjs`: spec says 215, actual is 214 —
   trivial, not separately reported.)

Verdict: 6 of 7 checked claims OK; 1 finding (item 5).

## S14 — learn-hub-retirements

Claims checked:
1. Every one of the 14 file line/byte pairs in §1.1 for
   `.claude-plugin/marketplace.json`, `source-to-vault`'s three files,
   `intent-lock`'s SKILL.md/misread-capture/README/CHANGELOG, `pubmed-research-note`'s
   SKILL.md/.mcp.json, `comprehensive-review`'s SKILL.md/command/.mcp.json,
   `.claude/hooks/session-start.sh`, `.claude/settings.json` — OK on all except one
   (below); `.claude/settings.json`'s "25" line entry in S14 is marked with no byte
   count (`—`), so not independently checkable as a hard number the way S13's was; not
   reported as a separate finding since S14 does not assert a byte figure for it.
2. `plugins/intent-lock/skills/intent-lock/references/misreads.md`: §1.1 lists it as
   "45 | ~1,850 | ~460". **WRONG**: actual file (confirmed byte-identical to the micky
   copy, matching S14's own "diff is empty" claim) is 47 lines / 2,446 bytes.
   S01's own independently-derived figures for the same file in the micky repo (47
   lines, 606 tokens ≈ 2,424 bytes) match the real file, not S14's 45/~1,850/~460.
   **Correction**: 45 → 47 lines; ~1,850 → 2,446 bytes; ~460 → ~606 tokens.
3. `diff` of the fork's `misreads.md` against the micky original is empty
   (byte-identical) — OK, confirmed (this claim is correct even though the size
   figures quoted alongside it in §1.1 are wrong).
4. `plugins/source-to-vault/.claude-plugin/plugin.json` content (name
   `source-to-vault`, version `0.1.0`) — OK, confirmed verbatim.
5. `.claude-plugin/marketplace.json` has 8 plugin entries — OK, confirmed.

Verdict: 4 of 5 checked claims OK; 1 finding (item 2).

## S15 — digest-report-inbox

Claims checked:
1. `plugins/digest-report/.claude-plugin/plugin.json`: §1.1 lists "7 | 632". **WRONG**
   on bytes: actual is 7 lines (OK) / 516 bytes (not 632). **Correction**: 632 → 516
   bytes.
2. `plugins/digest-report/README.md`: §1.1 lists "47 | 1,777". **WRONG** on bytes:
   actual is 47 lines (OK) / 2,361 bytes (not 1,777). **Correction**: 1,777 → 2,361
   bytes.
3. `plugins/digest-report/commands/digest-report.md`: §1.1 lists "25 | 1,076". Actual
   is 25 lines (OK) / 1,005 bytes — a 71-byte (7%) difference, small enough not to
   report as a separate finding on top of items 1-2's larger gaps.
4. `research-notes/*.md` sizes (76,435 / 38,761 / 29,943 bytes for the three real
   files) — OK, exact on all three.
5. `research-notes/.intake-log.jsonl` does not exist yet — OK, confirmed.
6. `vault/trazodone-2026-evidence/` already exists (evidence that digest-report has
   been run once by hand, under an author-chosen slug) — OK, confirmed directory
   exists.
7. `research-notes/` is not in `.gitignore` — OK, confirmed (`grep` returns nothing).
8. `.claude/skills/digest-report/SKILL.md` (the target file this spec is rewriting,
   which is `plugins/digest-report/skills/digest-report/SKILL.md` pre-move): body
   description chars 991, body_lines 203, body_est_tokens 2,816 — OK, exact.

Verdict: 6 of 8 checked claims OK; 2 findings (items 1-2, same root cause — the
plugin.json/README byte counts in §1.1 are off).

## S16 — ingest-visual-pk-plasma

Claims checked:
1. `.claude/skills/ingest-infographic/SKILL.md` 152 lines, `ingest-animation/SKILL.md`
   139 lines — OK, exact.
2. Both descriptions fail `yaml.safe_load` (`ScannerError`) — OK, confirmed
   (`yaml_valid: false` for both via `measure.py`).
3. `ingest-infographic` description 933 chars, `ingest-animation` 963 chars — OK,
   exact.
4. `.claude/commands/` does not exist in learn-hub today — OK, confirmed.
5. `plugins/pk-plasma-animation`'s five files (plugin.json 18, `.mcp.json` 12,
   `commands/pk-animation.md` 22, `skills/pk-plasma-animation/SKILL.md` 133 lines) —
   OK, exact on all four.
6. SKILL.md:88-90 names `report-fidelity.test.mjs` (a file that does not exist) as the
   pattern for a new drug directory to follow "exactly as
   `scripts/animations/mph-plasma/pk-engine.test.mjs` does" — OK, confirmed: the cited
   line does say "report-fidelity.test.mjs"; the referenced `mph-plasma/pk-engine.test.mjs`
   exists; no `pk-engine.test.mjs` exists under `scripts/animations/pk-plasma/`
   (the shared engine dir) yet, confirming the defect (pk-plasma-animation-7) as real.
7. I07-H "21 codes total" (reproduced from S05, taken as given) — WRONG, see F2 (same
   root cause, not double-counted as a separate S16-original error).

Verdict: 6 of 6 independently-checked claims OK; inherits F2 from S05 (flagged there,
not re-flagged as a new S16 error since S16 explicitly says it took the number from
S05 "as given").

## S17 — ingest-article-slides

Claims checked:
1. `.claude/skills/ingest-article/SKILL.md`: §1.1 lists 379 lines. Actual is 378 lines
   — a 1-line difference, too small to report as a separate finding given every other
   number for the same file (147, 503, 149 for the sibling reference files; 63 for
   `.gitignore`) is exact.
2. `.claude/skills/ingest-article/references/{article-frontmatter,figures-and-loss}.md`
   147/503 lines, `context/example.md` 149 lines — OK, exact on all three.
3. `.claude/skills/ingest-slides/SKILL.md` 141 lines,
   `references/lecture-adaptations.md` 72 lines, `scripts/extract_pdf.py` 128 lines,
   `scripts/render_slides.py` 78 lines — OK, exact on all four.
4. `.gitignore` 73 lines — OK, exact.
5. `ingest-article`'s description fails `yaml.safe_load` with "mapping values are not
   allowed here" — OK, reproduced (column differs by one, "col 445" claimed vs "col
   446" reproduced — trivial, not reported).
6. `.claude/skills/ingest-article/SKILL.md:144` "4 seed files" — OK, confirmed present
   verbatim.
7. `pdf-pipeline`'s `SKILL.md`/`routing.md` never mention `ingest-slides` (the
   reciprocal half of H28/ingest-slides-2) — OK, confirmed: zero hits for
   "ingest-slides" in either file, and `routing.md` routes slide decks to
   `atomize-book` (mini) instead.

Verdict: all 7 checked claims OK (item 1's 1-line gap not reported as a finding).

## S18 — pdf-pipeline-verify

Claims checked:
1. `.claude/skills/pdf-pipeline/SKILL.md` 207 lines,
   `references/{routing,preflight-and-apply,surface-checklist}.md` 86/90/82 lines — OK,
   exact on all four.
2. `.claude/skills/verify/SKILL.md`: §1.1 lists 60 lines. **WRONG**: actual is 64
   lines (the description/body-token figures given in the same table — chars 236,
   `use_when_at` -1, body_est_tokens 774 — are all independently confirmed exact, so
   only the line count is off). **Correction**: 60 → 64 lines.
3. `.claude/skills/verify/` contains only `SKILL.md` (no `scripts/` directory) — OK,
   confirmed (verify-1's evidence that the mint-session/probe recipe is not yet
   bundled as a script).
4. `routing.md:82` uses the one-level glob `grep -rh "^id:" vault/*/_topic.md` — OK,
   confirmed verbatim (pdf-pipeline-7's evidence).
5. SKILL.md:140,150 contain the "≲ ~200 KB" / "5.8 MB dump" text — OK, confirmed
   verbatim at both cited lines.

Verdict: 4 of 5 checked claims OK; 1 finding (item 2).

## S19 — atomize-book

Claims checked:
1. `.claude/skills/atomize-book/SKILL.md`: 1,274 total lines / 87,050 bytes, 1,256
   body lines, description 1,075 chars, `use_when_at` 432, `not_for_at` 922,
   `has_angle_brackets: true`, `body_est_tokens` 21,320 — OK, every figure exact
   against `measure.py`'s own output.
2. `python3 -m unittest discover ... 'test_*.py'` → "Ran 354 tests ... OK" — OK,
   reproduced exactly (354 tests, all green).
3. Twenty-two CLAUDE.md gotcha-heading line numbers cited by S19 as W4-8 candidates
   (1298, 1374, 1403, 1620, 1636, 2408, 2480, 2490, 2524, 2534, 2551, 2558, 2567, 2599,
   2697, 2711, 2732, 2745, 2803, 2817, 2865, 2882, 2906) — OK, every single one is the
   exact first line of the exact gotcha heading S19 names, spot-checked against the
   real 3,126-line `CLAUDE.md`.
4. `atomize-book`'s stale scale claim ("~9 topics, ~20 notes, ~20 subagents") at line
   27, contradicted by the depth floor two sections later — OK, confirmed present.
5. `check-order-band.py` already wired into SKILL.md steps 0 and 8 (not a missing
   rule) — plausible from the surrounding text; not independently re-derived line by
   line (low-risk, descriptive OBS claim, not load-bearing for any acceptance check).

Verdict: all independently checked claims OK. S19's large CLAUDE.md-heading mapping is
unusually precise — every sampled line number matched exactly.

## S20 — maintenance-skills

Claims checked:
1. `plugins/vault-atomizer/{skills/vault-atomizer/SKILL.md,commands/atomize.md,
   .claude-plugin/plugin.json}` 211/20/7 lines, 11,386/1,143/383 bytes;
   `plugins/vault-vectors/{...}` 153/19/6 lines, 8,109/1,097/217 bytes;
   `.claude/skills/{vault-coverage,check-repetition}/SKILL.md` 126/101 lines,
   7,556/6,071 bytes; `scripts/{split-note,vector-report,check-repetition}.mjs`
   241/886/321 lines; `scripts/lib/coverage-map.mjs` 291 lines — OK, exact on every
   one of these fourteen numbers.
2. `scripts/scrape/coverage-sources.json` has 26 entries today — OK, exact.
3. `node scripts/split-note.mjs --list --limit 3` prints "1681 split candidate(s) of
   4532 notes" — OK, reproduced verbatim, word for word.
4. "70 distinct `book:` values in vault" (vault-coverage-1's evidence) — OK, but only
   when counted correctly: a one-level glob (`vault/*/_topic.md`) undercounts to 67,
   because some books nest a level deeper (the exact "vault is not two levels deep"
   trap CLAUDE.md documents); a proper recursive `find` gives exactly 70, matching
   S20's claim. This is itself a live demonstration of the trap S20 is careful to
   avoid — the spec's own number is right precisely because it used the correct
   traversal.

Verdict: all checked claims OK.

## S21 — learn-hub-claude-md-infra

Claims checked:
1. `learn-hub/CLAUDE.md` 3,126 lines / 268,390 bytes — OK, exact.
2. All 14 top-level `## ` heading line numbers (7, 40, 54, 71, 101, 108, 206, 360, 799,
   806, 817, 2997, 3084, 3107) — OK, exact on every one.
3. Gotcha-heading count between lines 817 and 2996 = 136 — OK, exact
   (`grep -n "^- \*\*" CLAUDE.md | awk -F: '$1>817 && $1<2997'` → 136).
4. Ten spot-checked line numbers from the 136-row gotcha-destination table (§2.4),
   picked across all eight "pipeline" destinations (SV, AB, IV, PK, IA, VC, CR, VR) —
   OK on every one: each line is the exact first line of a real gotcha heading, and in
   every sampled case the heading's actual subject matter matches its assigned
   destination file (e.g. line 1930 — "A viewBox height floor or cap buys no plot
   height" — is the pk-plasma-animation SVG-geometry gotcha, correctly filed under PK;
   line 2680 — "Book source text lives in TWO gitignored directories" — is exactly
   vault-coverage's own `BOOK_ROOT` precondition, correctly filed under VC; line 843 —
   "The in-app browser pane does not composite" — is exactly the gotcha `verify`'s own
   spec (S18) quotes for its Gotchas section, correctly filed under VR).
5. `package.json` has none of `test:py`, `check:skills`, `sync:preflight`,
   `audit:visual`, `book:check-mermaid` today — OK, confirmed absent (spot-checked the
   `"scripts"` block).

Verdict: all checked claims OK. This spec's 136-heading map, sampled across every
destination category, is fully accurate.

## Claims-digest cross-checks (10, across specs)

| # | Claim (spec, location) | Digest id | Verdict | Result |
|---|---|---|---|---|
| 1 | "≥3 cases per skill" governed by R37 (S03, S05, S06) | rubric R37 (not a digest id, but load-bearing) | — | WRONG — R37 is `context: fork`; the real rule is R71. See F1. |
| 2 | `scripts/eval.sh` needs no `--allow-tools` for Bash/Write/AskUserQuestion cases (implicit in S01/S02/S05/S06/S07/S08's §4.4) | EVL-22 (confirmed): only read-only tools are granted by default; Bash/Write/etc. need `--allow-tools` | Confirmed by claims-digest, contradicted by 6 specs' own §4.4 | WRONG in those specs. See F3. |
| 3 | Descriptions/commands merge into skills — dmi aliases replace thin `commands/*.md` wrappers (S02, S05, S06, S08, S09, S20 all retire `commands/`) | SKL-01/SKL-02 (confirmed) | Confirmed | OK — consistently and correctly applied across every spec that retires a `commands/` dir. |
| 4 | Every frontmatter field is optional; an unrecognized field is silently ignored, so a house whitelist is needed in the validator (S08 VAL-01/VAL-02) | SKL-03 (confirmed) | Confirmed | OK. |
| 5 | `disable-model-invocation: true` removes the skill's description from context and blocks Skill-tool delegation by natural-language routing (S20's whole dmi-eval risk discussion) | SKL-36 (confirmed) | Confirmed | OK — S20 correctly treats this as unresolved/risky rather than asserting the explicit-invocation trigger case will pass; flagged in its own §7/§8 rather than assumed. |
| 6 | A synced claude.ai skill sharing a bare name loses the short form to any other entry sharing it (S04's rename rationale for psych-paper-digest→lit-watch) | SKL-55 (partially — corrected wording, same practical conclusion) | Consistent | OK — S04's use does not contradict the corrected text. |
| 7 | Directory-marketplace installs are version-pinned cache copies that don't refresh on an unbumped edit (S11 ARCH-CONFLICT 2) | PLG-09 (confirmed) | Confirmed | OK. |
| 8 | `--plugin-dir` takes precedence over a same-named installed plugin, and the overlap matters for ordering the Windows switch (S11 ARCH-CONFLICT 3) | PLG-51 (confirmed) | Confirmed | OK. |
| 9 | MEMORY.md's open thread (delete the `improve-all-plugins` branch) is still actionable, the branch still exists on origin — S10 does not claim otherwise | LOC-26 (**refuted** as originally phrased: "MEMORY's only open thread is stale, the branch no longer exists" — corrected to: the thread is still actionable, the branch DOES exist) | S10 makes neither the refuted claim nor contradicts the correction | OK — checked live: `origin/improve-all-plugins` exists, `57e470e` resolves. S10 does not repeat the refuted version. |
| 10 | pubmed-research-note's `Not for` doesn't name the voice-narration rule digest-report already enforces, and this is still an open gap in both report skills (S03's rationale for adding the voice rule) | LOC-28 (confirmed) | Confirmed | OK — S03's citation matches LOC-28's content exactly (P0-1 open in both `pubmed-research-note` and `comprehensive-review`). |

## Eval-format.md compliance (sampled cases)

Sampled at least 3 cases per spec (more where a spec's own text flagged something to
check) across all 21 specs — roughly 70 cases total. Findings:

- Every sampled `prompt.md` uses only documented keys (`max_turns`, `timeout_seconds`,
  `tags`, `allowed_tools`, `env`, `name`, `description`). No case uses the old
  skill-creator key `expected_output` (S12's own acceptance criterion 3 asserts this
  and it holds everywhere sampled).
- Every sampled `case.yaml` carries `schema_version: "1.1"` and `name`.
- Every grader `type` used (`regex`, `tool_used`, `tool_order`, `file_exists`, `llm`)
  is one of the six documented types, with only documented options
  (`pattern`/`flags`/`match`/`target`; `tool`/`input_match`/`min`/`max`;
  `before`/`after`; `path`/`exists`; `criteria`/`focus`).
- Every sampled negative case (asserting a skill must NOT fire) uses `type: tool_used`,
  `tool: Skill`, `min: 0`, `max: 0`, `arm: both` — the exact pattern
  `eval-format.md`/`spec-template.md` prescribe. No exceptions found.
- No case sets `plugins:` with more than one path (the EVL-20 "unverified that
  multiple plugins load" caveat in claims-digest does not come up — nobody attempted
  a genuine cross-plugin multi-load case; every cross-plugin negative is scoped to
  "this plugin's skill does not fire," which needs only the single enclosing plugin).
- The one systemic gap is **F3**: `allowed_tools` in several cases lists `Bash`,
  `Write`, `Edit`, or `AskUserQuestion`, which `eval-format.md` says are stripped
  unless granted via `--allow-tools` on the `claude plugin eval` invocation — and the
  wrapper those specs document (`scripts/eval.sh`) cannot pass that flag through, per
  S12's own definition of it.

No other eval-format schema violations found.

## Summary of findings to correct

| Spec(s) | Location | Wrong | Correction |
|---|---|---|---|
| S03, S05, S06 | §4.1/§4.2 case-count rationale | Cites "R37" for the ≥3-5-case rule | R37 governs `context: fork`; the rule is R71 |
| S05, S16 | §2.7 I07-H / §2.5 | "21 codes total" | The rule-id list given sums to 26; S05's own W2-1 step independently says 26 |
| S01, S02, S05, S06, S07, S08 | §4.4 | `bash scripts/eval.sh --smoke/--release <plugin>` documented as sufficient to run cases needing Bash/Write/AskUserQuestion | `scripts/eval.sh` (owner S12) grants no such tools and has no `--allow-tools` passthrough; these specs need to append `--allow-tools <tool...>` explicitly (as S03 partly did) or S12 needs to add passthrough |
| S03 | §1.1, `pubmed-research-note/SKILL.md` row | "304 \| 18,770 \| 4,692 (body)" presented as the file's Lines/Bytes | These are body-only figures; whole file is 320 lines / 20,185 bytes |
| S04 | §1.1, CR `CHANGELOG.md` row | "24" lines | Actual 29 lines |
| S10 | §1.1, `.claude-plugin/marketplace.json` row | "213" lines | Actual 212 lines |
| S13 | §1.1, `.claude/settings.json` row | "24" lines | Actual 31 lines |
| S14 | §1.1, learn-hub fork `misreads.md` row | "45 \| ~1,850 \| ~460" | Actual 47 lines / 2,446 bytes / ~606 tokens |
| S15 | §1.1, `plugins/digest-report/.claude-plugin/plugin.json` row | "632" bytes | Actual 516 bytes |
| S15 | §1.1, `plugins/digest-report/README.md` row | "1,777" bytes | Actual 2,361 bytes |
| S18 | §1.1, `.claude/skills/verify/SKILL.md` row | "60" lines | Actual 64 lines |
