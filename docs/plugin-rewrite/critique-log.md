# Critique log

Date: 2026-09-24. Inputs: `phase3/reviews/critique-1.md` (22 findings), `phase3/reviews/critique-2.md` (31), the planner findings of the `plan:write` result (35) and the unapplied `reconcile:1` finding (1).

| Count | Findings |
|---|---|
| Total | 89 |
| Applied to spec | 65 |
| Applied to plan | 12 |
| Owner question | 12 |
| Rejected | 0 |

Counting rule: each finding counts once, under its main disposition. "Owner question" when the owner must still choose, even where the specs already carry the recommended option. Otherwise the place of the main repair: "spec" (most spec repairs also have matching plan edits) or "plan". Partial rejections (C2-06 fix 1, C2-13 W2 move, C2-26 single generator) are stated in the row; no finding was rejected as a whole.

Batch ids name the edit scripts in `tmp/crit/`: e01–e09 ran in the first pass; e10 (S21) had not run; this pass ran it in full (all 17 replacements, one anchor corrected, plus the two new steps S21-W0-3 and S21-W4a-4); e11 and p01–p04 are this pass's spec and plan edits. Every "applied" spec repair can be seen with `diff tmp/crit/specs.orig/<spec> specs/<spec>`.

New owner questions (plan §1): OQ7 branch model · OQ8 baseline cadence · OQ9 W4 CLAUDE.md freeze · OQ10 alignment plugins in cloud during W3 · OQ11 eval run counts · OQ12 Windows in-place loading from W1 · OQ13 one visual audit · OQ14 stage (b) diet before W1 · OQ15 vault-keeper scripts · OQ16 micky tooling CHANGELOG.

| Source | Id | Severity | Where | Problem | Disposition |
|---|---|---|---|---|---|
| critique-1 | F1 | high | plan §0 rule 2; S11-W1-1/-2, S11-W2-3, S11-W3-5, S13-W1-10 | The wave branch merges at exit, but cloud and Windows steps need the fixes on master mid-wave. | owner question OQ7; plan §0 rule 2 says the model is pending OQ7 |
| critique-1 | F2 | high | plan §3 smoke gate; S12-W3-5, S12-W5-1 | No step produces the pre-rewrite baseline the gates compare against. | owner question OQ8 (cadence). Tooling applied: spec S12 (S12-W0-8, `--against <ref>`; e06); plan §3 smoke and release gates |
| critique-1 | F3 | high | S12 runners; S11 setup script; plan W1 exit | Bash-granted and scaffold cases cannot run; the gate drops grants; the W1 gate filters out its own case; env vars are stripped. | applied: spec S11 (setup step 4, check-d canary; e05), S12 (`--scaffold`; e06), S13 and S17 (smoke tags, grants, no env block; e07, e09); plan §3 smoke gate and W1 exit gates |
| critique-1 | F4 | high | arch §6.3; S12-W3-2/-3, S12-W4-2/-3 | skill-creator `run_eval` measures a clone that competes with the real skill. | applied: spec S12 (routing-smoke method for live trigger runs; check i in S12-W0-6; e06); fact to confirm: plan §8 Q26 |
| critique-1 | F5 | high | S13 §2.5 `checkChromium` | The preflight refuses every Windows sync. | applied: spec S13 (bundled-browser fallback + test case; e07), S11 (S11-W1-2 runs `ready.mjs` on Windows; e05); fact to confirm: plan §8 Q28 |
| critique-1 | F6 | high | S13-W1-4; plan W1 exit | The refusal check runs the real `apply-sync.mjs` with live credentials. | applied: spec S13 (`--preflight-only`, pure `gateOnPreflight`, injectable client factory, vitest case; e07); plan §3 W1 exit gate, §0 rule 10. The throwaway-worktree form was not needed: `--preflight-only` exits before any Supabase client exists |
| critique-1 | F7 | medium | 20 specs' §6; S04-W3-3; S12 §2.5 | Trigger-lock removals have no commands; S04 uses undefined flags; learn-hub scan roots are undefined. | applied: spec S12 (scan roots, `--skill` forms; e06), S04 (S04-W3-3 commands; e02); plan §0 rule 7 and the §5 lock table (per-step commands) |
| critique-1 | F8 | medium | plan §0 rules 6–7; S10-W0-9; S12 §4.4 | Ratchet and lock are not checked per commit; learn-hub has no pre-commit. | applied: spec S10 (`--fast` runs both verifies; e04), S21 (new S21-W0-3; e10), S12 §4.4 (e06); plan §3 W0 row, §0 step 5 |
| critique-1 | F9 | medium | S21 `test:py`; S13 readiness; plugin hooks | Windows: npm runs cmd.exe, `python3` may not exist, hooks call bash. | applied: spec S21 (`test-py.mjs`, `check-skills.mjs`; e10), S13 (`checkPyMuPDF` interpreter search; e07), S11 (toolchain lines, S11-W3-2 hook check; e05); fact to confirm: plan §8 Q25 |
| critique-1 | F10 | medium | S13 I14 done-marker | The marker on disk skips per-session setup in a reused container. | applied: spec S13 (marker holds the session key; new test case; e07) |
| critique-1 | F11 | medium | S13 §2.5 `runPreflight` | Gate subprocesses run without cwd; a crash becomes a silent empty string. | applied: spec S13 (absolute path, `cwd: root`, `gate unavailable` line, test; e07) |
| critique-1 | F12 | medium | LH README.md:159-163, CLAUDE.md; plan §0 rule 8 | No learn-hub README/CLAUDE.md upkeep; W4 would move stale text. | applied: spec S13-W1-7 (README and CLAUDE.md; e07), S21-W0-2 (e10), S13-W1-5, S16-W2-2, S19-W1-4, S12-W0-4 (README rows; e11); plan §0 rule 8, §5 README row |
| critique-1 | F13 | medium | S21-W4a-1 … S21-W4b-1 | Other sessions edit learn-hub CLAUDE.md during the W4 surgery. | owner question OQ9 (freeze). Map by heading text and byte check applied in S21 (e10) under both options |
| critique-1 | F14 | medium | S19-W4-9; plan W4 row 15 | The chapter re-run needs `Book/` (Windows only) and has no pre-split baseline. | applied: spec S19 (S19-W4-0, S19-W4-9 OWNER on Windows, verdict comparison; e09), S17 (S17-W4-0, S17-W4-5; e09); plan §3 W4 rows and gates, §4 |
| critique-1 | F15 | medium | plan §0 step 3 | "Stop on any line drift" stalls a repo with about 10 commits a day. | applied: plan §0 step 3 (locate by quoted text; stop only when absent or ambiguous) |
| critique-1 | F16 | medium | plan §2 W3 ∥ W4 | Parallel W4 confounds the W3 before/after trigger scores. | applied: plan §2 (hold W4 merges to learn-hub master from S12-W3-2 until S12-W3-4 ends) |
| critique-1 | F17 | medium | S14-W1-1 | The orphan audit covers all orphans and offers raw SQL deletes. | applied: spec S14 (read-only; restore or leave; no delete in W1; e08); plan §1 OQ5, §3 W1 row, §4 |
| critique-1 | F18 | low | plan §3 ratchet gate | "Fewer entries than at entry" cannot pass in W0 or in waves that seed checks. | applied: plan §3 standard gate (per check id, named first-time seeds), §0 rule 6 |
| critique-1 | F19 | medium | plan links; specs `<wf3>/`; S01 §4.4 | Phase-3 files exist only in /tmp. | applied: plan §3 W0 entry (commit the package to micky `docs/plugin-rewrite/` before S12-W0-0), §0 step 3; specs S13, S17, S18, S21 call `$MICKY_TOOLS_DIR/docs/plugin-rewrite/phase3/measure.py` (e07, e09); S01 drops `check_evals.py` (e01) |
| critique-1 | F20 | low | coverage.md; plan §7 | Many rows lack a step id; the no-step lists disagree. | applied: plan §3 W0 entry (regenerate coverage.md with a parser that fails on a row with neither step id nor reason), §7 (named steps for four rows) |
| critique-1 | F21 | low | S21-W1-4 | The done-when grep does not match the sentence the step adds. | applied: spec S21 (`sole owner of the sync`; e10) |
| critique-1 | F22 | low | S13-W1-6 and other done-whens | `claude plugin validate --strict` checks neither YAML strictness nor the 1,024 cap. | applied: spec S21 (`check:skills` runs skill-lint first; e10), S13-W1-6 (`measure.py` + `validate --strict .claude`; e07) |
| critique-2 | C2-01 | high | S12 §2.7 runners; scaffold cases; W1 gate | The runners never pass `--scaffold`, so safety cases pass with empty fixtures. | applied: spec S12 (both runners pass `--scaffold`; e06), S11 (check-d canary; e05); plan §3 W0 gate "Eval canary" |
| critique-2 | C2-02 | medium | S11-W0-5, S11-W0-9; §4.4 with Bash grants | bubblewrap and socat are absent, so Bash-granted runs are refused. | applied: spec S11 (setup step 4, canary; e05), S12 (note; e06); plan §0 rule 10; fact to confirm: plan §8 Q24 |
| critique-2 | C2-03 | high | plan §0 rule 2; plan V-step rows; S11-W1-2 | One branch per wave conflicts with cloud enablement in the middle of a wave. | owner question OQ7 |
| critique-2 | C2-04 | high | S13-W1-4; S13 §5 criterion 9; plan W1 exit | The refusal check runs the real `apply-sync.mjs` against the production DB. | applied: spec S13 (`--preflight-only`, criterion 9; e07); plan §3 W1 exit gate, §0 rule 10 |
| critique-2 | C2-05 | high | S21 I22 `check:skills`; S21-W0-2 | `claude plugin validate --strict .claude/skills` exits 1 on every run. | applied: spec S21 (`check-skills.mjs` validates `.claude`; e10), S13-W1-6 (e07) |
| critique-2 | C2-06 | high | S21-W0-1/-2; S12-W0-1/-2; S10-W0-1b | Five YAML-invalid skills break the W0 gates and the lock seeds miss them. | applied: spec S21 (S21-W0-1 expects today's failures; S21-W0-2 seeds the LH ratchet and depends on S12-W0-2; e10), S12 (raw-line read of `description:`; every SKILL.md locked or listed; e06); plan §3 W0 rows, §5. The W0 fold of the five descriptions (fix 1) was not taken: the raw-line read locks the phrases without editing skills in W0 |
| critique-2 | C2-07 | high | plan smoke gate; S12-W0-5, S12-W3-5, S12-W5-1 | No step records the regression baseline, and no tool computes it. | applied: spec S12 (S12-W0-8, `--against <ref>`, redefined gates; e06); plan §3 smoke and release gates; cadence is OQ8 |
| critique-2 | C2-08 | high | S21-W4a-2/-3, S21-W4b-1, S13-W4-1, S19-W4-2…6 | Verbatim moves are made by hand and checked only by 8-word fragments. | applied: spec S21 (S21-W4a-4 `move-blocks.mjs`, archive by script, byte check; e10), S13-W4-1 (e07), S19 (move-proof `diff`, S19-W4-3b; e09); plan §3 W4 rows and gate |
| critique-2 | C2-09 | medium | S21 §2.4, S21-W4a-1; plan §0 rule 3; CLAUDE.md upkeep line | The gotcha map uses stale line numbers; no freeze; CLAUDE.md can grow back. | applied: spec S21 (map by heading text from the W4-entry file; upkeep line; skill-lint check 10; e10); plan §0 step 3 (fix 4), §3 W4 size gate. Freeze (fix 2) is OQ9 |
| critique-2 | C2-10 | medium | S07-W1-1, S07-W1-3, S07-W2-1 | vault-keeper writes to the learn-hub inbox in W1, before the inbox contract exists. | applied: spec S07 (`--vault-only` in W1, removed by S07-W2-1; e02) |
| critique-2 | C2-11 | low | S07-W1-2 | The empty-vault stopgap keeps a delete step with no definition of "landed". | applied: spec S07 (Steps 3–5 replaced; grep in done-when; e02) |
| critique-2 | C2-12 | medium | S11-W3-1; S10-W3-1; plan OQ4 | Unfixed alignment plugins load in the cloud for all of W3. | owner question OQ10 |
| critique-2 | C2-13 | medium | S08-W3-1; plan W2 exit | The new validator lands after the change it guards, as one large commit. | applied: spec S08 (one PR of four commits; e11); plan §0 step 4. Moving parts (a)–(c) into W2 rejected: the W2 release steps still call root `scripts/validate.py` and `bump.py`, and plan §3 W2 already has a cross-repo gate (P-11) |
| critique-2 | C2-14 | medium | S10-W3-1 + S10-W3-2; plan §0 rule 4; K18 | The skeleton commit is no longer move-only and cannot be reviewed as one commit. | applied: spec S10 (one PR, one commit per family, `git diff -M100%`; e04); plan §0 step 4, §6 K18. The aliases go into each family commit instead of a fourth commit |
| critique-2 | C2-15 | medium | plan §3 ratchet gate; plan §5; S08-W3-1 | "Fewer entries" cannot pass; S08-W3-1 is not listed as a ratchet writer. | applied: plan §3 standard gate, §0 rule 6, §5 ratchet rows (S08-W3-1, S21-W0-2 added) |
| critique-2 | C2-16 | medium | plan h-coverage gate; S12 §2.3; H07, H10, H11 | Rows split across two waves break the per-wave grep. | applied: spec S12 (split rows, 52 lines; e06); plan §3 gate regex with `$`, W0 gate 52, W1–W3 HIGH rows, §7 |
| critique-2 | C2-17 | medium | plan §2; OQ3; S12 live and release runs | The cost of evals and live-trigger runs is not budgeted. | owner question OQ11 |
| critique-2 | C2-18 | medium | OD2 timing; 12 W1/W2 release steps; S11-W1-2, S11-W2-5 | Windows could load plugins in place from W1, which removes 12 release steps. | owner question OQ12 |
| critique-2 | C2-19 | medium | S05-W2-1/-2; S16-W2-1/-2; S08 VAL parity | The visual audit is built twice, plus a parity harness. | owner question OQ13 |
| critique-2 | C2-20 | medium | arch §8; learn-hub `.githooks/`; micky cloud hooksPath | No commit-time enforcement where the work happens. | applied: spec S21 (S21-W0-3; e10); plan §0 step 2 (cloud `core.hooksPath` line); fact to confirm: plan §8 Q29 |
| critique-2 | C2-21 | medium | plan rollbacks; S14-W1-1, S13-W1-10, S07-W2-7 | Rollbacks ignore live-DB writes; the W3 per-family revert is undefined. | applied: spec S14 (no delete; e08), S13-W1-10 and S07-W2-7 (vault files committed to master; e07, e02); plan §3 W1, W2 and W3 rollback text |
| critique-2 | C2-22 | medium | S15 §2.3, §2.5; S15-W2-2 | digest-report calls a parser CLI that does not exist. | applied: spec S15 (guarded `--json` CLI + test; S15-W2-2 depends on S15-W2-5; e08); plan §3 W2 row |
| critique-2 | C2-23 | medium | OD11 staging; S21-W4b-1 | Move the learn-hub CLAUDE.md stage (b) diet before W1. | owner question OQ14 |
| critique-2 | C2-24 | low | plan §2, §0 | The plan does not say which session type each block needs. | applied: plan §2 (session-type rule derived from the Repo column; no new column) |
| critique-2 | C2-25 | low | S07-W2-3, S07-W2-4, S07-W2-5 | Two vault-keeper scripts are planned for a vault of 16 files. | owner question OQ15 |
| critique-2 | C2-26 | low | S12-W0-1/-2; plan §0 rule 9 | Two implementations of the rewrite gate; the h-coverage file is mirrored. | applied: spec S12 (micky copy canonical; tag steps close rows and copy the file; e06); plan §0 rule 9, §5. Rest rejected: learn-hub keeps the Node twin because its pre-commit (S21-W0-3) and ratchet seed (S21-W0-2) run in sessions that may not hold a micky clone |
| critique-2 | C2-27 | low | S19-W4-1; plan W4 order | The atomize-book freeze window is longer than needed. | applied: spec S19 (freeze from S19-W4-2 until S19-W4-9; e09), S12-W4-T (e06); plan §2, §3 W4 order, §4 |
| critique-2 | C2-28 | low | plan §0 steps 4–5; spec rollbacks | Step rollbacks assume nothing has been committed yet. | applied: plan §0 step 4 (checks before commit; after a commit, `git revert <sha>`) |
| critique-2 | C2-29 | low | S15 and S16 OWNER steps; tag steps | Some OWNER steps are read-only commands an executor can run. | applied: spec S15, S16 (S15-W2-8, S16-W2-8 as executor steps; e08); plan §3 W2 rows, §4. Tag steps stay OWNER |
| critique-2 | C2-30 | low | S11-W2-4; S07-W2-7; plan W2 gates | The check b = no path breaks W2. | applied: spec S07 (S07-W2-7 depends on S11-W2-4 or its skip record; e11); plan §3 W2 row and gates |
| critique-2 | C2-31 | low | plan §2; S12-W4-2/-3 | Parallel W3 can confound the W4 trigger scores. | applied: plan §2 (micky at `wave-2` for S12-W4-2/-3, or both before the W3 merge) |
| planner | P-01 | high | S09 §3; S12-W0-5, S11-W1-1 | Step S09-W0-1 (firecrawl smoke seeds) does not exist. | applied: spec S09 (S09-W0-1; e03); plan §3 W0 and W1 rows, §8 Q10 |
| planner | P-02 | high | S03-W0-1, S04-W0-1/-2, S06-W0-1, S07-W0-1, S08-W0-1 | W0 seeds sit under `evals/smoke/`, not the I17 layout S12-W0-5 checks. | applied: specs S03, S04, S06, S07, S08, S09 (I17 paths, smoke tags, done-when = S12-W0-5 check; e02, e03) |
| planner | P-03 | high | S08-W3-1 health.sh; arch §6.6 | `unittest discover -s plugins` runs 0 tests and passes. | applied: spec S08 (per-directory loop that fails on `Ran 0 tests`; e03) |
| planner | P-04 | medium | S10-W0-1, S10-W0-1b, S12-W0-1 | S10-W0-1 expects a ratchet entry that is seeded later; two steps seed it. | applied: spec S10 (exit 1, then exit 0 + WARN; single seeder; e04), S12 (empty ratchet; e06); plan §3 W0 notes, §8 Q9 |
| planner | P-05 | medium | S01-W3-5, S03, S05, S07-W3-1 | No release step after the W3 family rewrites or for vault-keeper. | applied: specs S01, S03, S05, S07 (S01-W3-7, S03-W3-8, S05-W3-6, S07-W3-2; e01, e02); plan §3 W3 rows, §5, §8 Q13 |
| planner | P-06 | medium | S19 §3, S20 §3; S12-W4-1 | No step writes the eval cases S12-W4-1 needs. | applied: spec S19 (S19-W4-10), S20 (S20-W2-5; e09); plan §3 rows, S12-W4-1 dependencies, §8 Q15 |
| planner | P-07 | medium | S13-W1-9, S17-W1-12, S17-W4-3, S18-W1-9, S18-W4-4 | Case counts ignore the W0 seed directories. | applied: specs S13, S17, S18 and the micky seed steps (seeds named as §4.1 cases; counts restated; e02, e03, e07, e09) |
| planner | P-08 | medium | S06-W3-1 | Wrong examples path; missing dependency on S05-W3-5. | applied: spec S06 (e02); plan §3 W3 row, §8 Q18 |
| planner | P-09 | medium | S11-W3-4, S09-W3-1 | The firecrawl question is asked after the change it decides. | applied: spec S09, S11 (asked as OQ6 at W3 entry; S09-W3-1 depends on the answer; e03, e05); plan §3 W3 row |
| planner | P-10 | medium | S13-W4-1 | A 6 KB cap conflicts with a verbatim move of about 12 KB. | applied: spec S13 (cap dropped; byte check; e07); plan §8 Q22 |
| planner | P-11 | medium | arch §10 standard gates; S08-W3-1 | The `--cross-repo` gate is required from W2 but built in W3. | applied: plan §3 standard gate and W2 gate note (the two W2 contract checks are the gate), §8 Q12 |
| planner | P-12 | medium | S04 OD8-a; S04-W2-4 | No OWNER step for the edit of the synced daily-random-review skill. | applied: spec S04 (S04-W2-5; e02); plan §3 W2 row, §4, §8 Q21 |
| planner | P-13 | medium | W5 (S04, S07, S12) | No W5 steps for lit-watch usage, OD4, ratchet hard-fail and the decision log. | applied: specs S04, S07, S12 (S04-W5-1, S07-W5-1, S12-W5-3; e02, e06); plan §3 W5 rows and gates, §4, §8 Q17 |
| planner | P-14 | medium | S17 W4; arch §10 W4 exit | No step re-runs one article end to end. | applied: spec S17 (S17-W4-0, S17-W4-5; e09); plan §3 W4 rows and gates, §8 Q16 |
| planner | P-15 | low | S15 §3, S16 §3 | Two OWNER steps have no step id. | applied: spec S15, S16 (S15-W2-8, S16-W2-8; e08); plan §0, §3, §4, §5 |
| planner | P-16 | low | nine W1/W2 release steps | Release steps list marketplace.json and keep a stale conditional. | applied: specs S01, S02, S03, S04, S06, S07, S08 (e01–e03); plan §5, §8 Q14 |
| planner | P-17 | low | S04-W2-4, S07-W2-7, S12-W0-6 | OWNER results go to the delivery log, which accepts only variable rows. | applied: specs S04, S07, S12, S13, S15, S16 (`baseline.md` `## Owner records`; e02, e06, e07, e08); plan §3 W1 gate, §5 |
| planner | P-18 | low | S04-W3-3 | Lock CLI flags do not match S12. | applied: spec S04 (e02), S12 (`--skill` forms; e06) |
| planner | P-19 | low | S01-W3-4 | Missing dependency on S01-W3-3. | applied: spec S01 (e01); plan §3 W3 row |
| planner | P-20 | low | S01-W3-5 | `head -1 CHANGELOG.md` reads the `# Changelog` header. | applied: spec S01 (version check moved to S01-W3-7, first `## ` line; e01) |
| planner | P-21 | low | S10-W0-2, S10-W0-3 | Missing dependency on S10-W0-3. | applied: spec S10 (e04); plan §3 W0 row |
| planner | P-22 | low | S10-W3-9 | `python3 scripts/health.sh` runs a bash script with Python. | applied: spec S10 (`bash`; e04) |
| planner | P-23 | low | S21-W1-4 | The grep text does not match the sentence (same as F21). | applied: spec S21 (e10) |
| planner | P-24 | low | S14-W2-1, S14 §8 | LICENSE is missing from the file list. | applied: spec S14 (e08) |
| planner | P-25 | low | S08 §8 Q1 vs S08-W3-1 | Two paths for the committed lists. | applied: spec S08 (e03) |
| planner | P-26 | low | S07 §8 Q4, S09 §8 Q4, S11 §8.9, S02 §8 Q4–Q5 | Stale §8 items. | applied: specs S02, S07, S09, S11 (marked closed; e01–e05) |
| planner | P-27 | low | S03-W3-2; arch K13 | "Klaeng" stays in distributable text. | applied: spec S03 (S03-W3-2, S03-W3-6; e02); plan §3 W3 row, §6 K13, §8 Q20 |
| planner | P-28 | low | S10 §1.3 | Two defect rows name no step id. | applied: spec S10 (e04), S08 and S09 rows (e03); plan §7, §8 Q19 |
| planner | P-29 | low | S18-W4-2 vs S21-W4a-2 | The verify gotchas would exist twice. | applied: spec S18 (e09); plan §3 W4 row, §5 |
| planner | P-30 | low | S19-W4-2; S05-W3-4 | Missing dependencies on S19-W4-1 and S08-W3-1. | applied: spec S19, S05 (e09, e02); plan §3 W3 and W4 rows |
| planner | P-31 | low | S11-W2-2, S11-W2-3 | Missing dependencies on the eval-case steps. | applied: spec S11 (e05); plan §3 W2 rows |
| planner | P-32 | low | micky repo-level CHANGELOG | No home for tooling CHANGELOG entries. | owner question OQ16 (S10-W0-8 assumes option (a); e04) |
| planner | P-33 | low | S12 h-coverage; acceptance 6 | No step mirrors h-coverage closures across repos. | applied: spec S12 (micky copy canonical; tag steps close and copy; e06); plan §0 rule 9, §5 |
| planner | P-34 | low | phaseB/coverage.md | coverage.md was generated before reconciliation. | applied: plan §3 W0 entry (regenerate before the package commit) |
| planner | P-35 | low | S10-W3-1 + S10-W3-2 | Two step ids share one commit. | applied: plan §0 step 4 (declared exception: one PR of three commits); spec S10 commit shape (e04) |
| reconcile-1 | R-01 | low | S09 §8 item 6; S09-W3-1's `defaultEnabled: false` | Keeping or dropping `defaultEnabled: false` on firecrawl is an owner trade-off. | owner question OQ6 (already in plan §1; S09-W3-1 depends on the answer, P-09) |

## Checks after the repairs

- Step ids: 285 defined in the specs' §3, each defined once; 285 rows in plan §3, each id once; 0 missing, 0 duplicates, 0 dangling references in plan.md or any spec (`tmp/crit/check_ids2.py`).
- Plan links to `specs/` resolve to the 21 files in `specs/`. The links to `architecture.md`, `coverage.md` and `phase3/…` resolve after the W0-entry package commit (F19).
- No `<wf3>` placeholder remains in plan.md or any spec. The lines that open with two spaces and a closing backtick are wrapped code spans that were already in the pre-repair specs, not failed replacements.
