# Critique 2: sequencing, feasibility, risk, simplicity, alternatives

Date: 2026-09-24. Scope: `plan.md` in full; specs S05, S07, S12, S15 and S21 in full; the relevant steps of S08, S10, S11, S13, S14, S16, S17 and S19; `eval-format.md`; `interfaces.md`; architecture §5–§12 and Appendix A.

Both repos were used read-only. Probes ran on copies in the scratchpad, with CLI 2.1.281:

| Probe | Result |
|---|---|
| `yaml.safe_load` on every learn-hub SKILL.md | concept-animation, ingest-animation, ingest-article and ingest-infographic fail. atomize-book is 1,075 chars and ingest-slides is 1,150 chars. |
| `yaml.safe_load` on micky intent-lock SKILL.md | fails at line 3, col 574 ("mapping values are not allowed here") |
| `claude plugin validate --strict <copy of .claude/skills>` | "No manifest found in directory", exit 1 |
| `claude plugin validate --strict <dir holding skills/>` | "Validating components … Validation passed", exit 0. It passes even with the 4 YAML-invalid skills. |
| `claude plugin validate --strict` on the micky catalog and on each plugin (copies) | all pass today |
| `which bwrap socat` | no output (neither tool is installed) |
| `eval-format.md:115,261` | `scaffold_script` runs only when `--scaffold` is passed |
| `eval-format.md:195` | when Bash is granted, Linux needs bubblewrap and socat; without them each run is refused and scores 0 |

## Summary

| Id | Sev | Area | Owner decision |
|---|---|---|---|
| C2-01 | high | Eval runners never pass `--scaffold`, so safety cases pass without their fixtures | no |
| C2-02 | medium | Eval runs that grant Bash need bubblewrap and socat, which are not installed | no |
| C2-03 | high | The one-branch-per-wave model conflicts with cloud enablement in the middle of a wave | yes |
| C2-04 | high | The refusal check runs the real `apply-sync.mjs` against the production DB | no |
| C2-05 | high | `check:skills` fails on every run (measured) | no |
| C2-06 | high | 5 YAML-invalid skills break the W0 gates, and the trigger-lock seeds miss them | no |
| C2-07 | high | No step records the regression baseline, and no tool can compute it | no |
| C2-08 | high | Verbatim moves are made by hand and checked only by 8-word fragments | no |
| C2-09 | medium | The gotcha map uses stale line numbers; no freeze; CLAUDE.md can grow back | no |
| C2-10 | medium | vault-keeper writes to the learn-hub inbox in W1, before the inbox contract exists | no |
| C2-11 | low | The empty-vault W1 stopgap keeps a delete step with no definition of "landed" | no |
| C2-12 | medium | Unfixed alignment plugins load in the cloud for all of W3 | yes |
| C2-13 | medium | The new validator lands after the change it should guard, as one large commit | no |
| C2-14 | medium | The skeleton commit is no longer "move only" and cannot be reviewed as one commit | no |
| C2-15 | medium | The ratchet exit gate ("fewer entries") cannot pass | no |
| C2-16 | medium | The h-coverage grep fails at W1 on rows split across two waves | no |
| C2-17 | medium | The cost of evals and live-trigger runs is not budgeted | yes |
| C2-18 | medium | Windows could load plugins in place from W1, which removes 12 release steps | yes |
| C2-19 | medium | The visual audit is built twice, plus a parity harness to keep the two equal | yes |
| C2-20 | medium | No commit-time enforcement where the work happens | no |
| C2-21 | medium | Rollbacks ignore live-DB side effects; the W3 per-family revert is undefined | no |
| C2-22 | medium | digest-report calls a parser CLI that does not exist | no |
| C2-23 | medium | Move the learn-hub CLAUDE.md stage (b) diet before W1 | yes |
| C2-24 | low | The plan does not say which session type each block needs | no |
| C2-25 | low | Two vault-keeper scripts are planned for a vault of 16 files | yes |
| C2-26 | low | Two implementations of the rewrite gate; the h-coverage file is mirrored | no |
| C2-27 | low | The atomize-book freeze window is longer than needed | no |
| C2-28 | low | Step rollbacks assume nothing has been committed yet | no |
| C2-29 | low | Some OWNER steps are read-only commands an executor can run | no |
| C2-30 | low | The check b = no path breaks W2 | no |
| C2-31 | low | Running W3 and W4 in parallel can confound W4's live-trigger scores | no |

## Findings

### C2-01 · high · Eval runners never pass `--scaffold`

- **Where.**
  - S12 §2.7 I17 (the `eval.sh` and `eval-project-skill.sh` invocations), S12-W0-3 and S12-W0-4.
  - Cases that depend on a scaffold:
    - S01 `misread-capture-append-writes-ledger`;
    - S07 `sink-resolution-from-learn-hub-cwd-asks` and `verify-before-delete-fixture-inbox`;
    - S13 `sync-preflight-before-apply`;
    - S15 `bare-invocation-survey`;
    - S16 `audit-before-write`;
    - S17 `inbox-survey-and-ask`.
  - Plan §3, W1 exit gate "Bare ingest-article asks".
- **Problem.**
  - A `scaffold_script` runs only when `--scaffold` is passed (`eval-format.md:115,261`). Without the flag, each of these cases starts in an empty workspace.
  - "Must not" safety graders then pass with nothing to test. Examples: the `not_contains` rm-regex, "no Write", "no sync Bash", and "no premature delete".
  - `tool_order` graders fail.
  - The W1 exit gate reads "pass" when no fixture was ever created.
- **Fix.**
  - Add `--scaffold` to both base invocations in S12 §2.7. `eval-format` says the flag is for suites you wrote yourself, which these are.
  - In S12-W0-3 and S12-W0-4, add a canary case `evals/_canary/scaffold-runs/`. Its scaffold writes `sentinel.txt`, and a `file_exists` grader requires that file.
  - Run the canary once at W0 exit. It must pass.

### C2-02 · medium · Eval runs that grant Bash need bubblewrap and socat, which are not installed

- **Where.**
  - S11-W0-5 (setup script v1) and S11-W0-9 (check d).
  - Every §4.4 that passes `--allow-tools "Bash…"`: S05, S07, S13 and S17.
- **Problem.**
  - `eval-format.md:195`: when Bash is granted, Linux needs bubblewrap and socat. Without them, every run is refused and scores 0. Native Windows has no sandbox backend at all.
  - `which bwrap socat` prints nothing in this container.
  - Check d tests only "eval enabled" and "an http mock answers".
  - Smoke cases that use Bash would score 0, and the gates would read that as a regression.
- **Fix.**
  - Setup script v1 (S11-W0-5): install `bubblewrap` and `socat`.
  - Check d (S11-W0-9): add one canary case with `--allow-tools "Bash(echo *)"`. It must score 1.
  - Plan §0: state that eval runs happen only in the cloud environment or under WSL2.

### C2-03 · high · The one-branch-per-wave model conflicts with cloud enablement in the middle of a wave

- **Where.**
  - Plan §0 rule 2.
  - Plan §3 rows: W1-66 (V2), W2-54, W2-56 and W2-57 (V3, V4, V5), and W3-1 (V6).
  - S11 line 509: a "new session" is on the default branches.
  - S11 line 832: "cloud sessions clone the default branch".
  - S11-W1-2: "pushed to origin/master".
  - Architecture §7 (rollback).
- **Problem.**
  - All wave work stays on `rewrite/w<n>` and merges at wave exit. Cloud sessions load master.
  - So V2, set before the W1 merge, loads master's vault-keeper. That copy still has the walk-up (H08, H09) and an empty-vault that deletes assets (H11).
  - V3 loads master's pubmed-research-note and comprehensive-review, which still hard-code the MCP prefix (K4) and have no fallback.
  - The rule "a plugin reaches the cloud only after it is fixed" fails at every V step made in the middle of a wave.
  - The model also keeps the W1 harm fixes (H25, H34, H35) off learn-hub master for the whole wave. Meanwhile other sessions push to master every day, which causes drift and conflicts in CLAUDE.md, package.json and settings.json.
- **Fix. Owner decision; options, recommended first.**
  - **(a) Per-block PRs.**
    - Use one short branch per spec block: the rows up to and including a release or a V-step dependency. Merge it to master when it is green.
    - A V step or a Windows refresh runs only after `git merge-base --is-ancestor <dep-sha> origin/master` succeeds for each of its dependencies.
    - The wave tag marks the last merge.
    - Wave rollback: revert the wave's PR merges, newest first, from a list kept in the wave record.
    - At W1 and W2, merge the learn-hub blocks before the micky blocks that write into them.
  - **(b) Keep wave branches.**
    - Move every V step and Windows step to after the wave merge.
    - Merge learn-hub before micky at the W1 and W2 exits, and state this in §3.

### C2-04 · high · The refusal check runs the real `apply-sync.mjs` against the production DB

- **Where.** S13-W1-4 (commands and done-when); S13 §5 criterion 9; plan §3, W1 exit "Sync refuses unready".
- **Problem.**
  - The only guard is the preflight code that this same step adds.
  - The guard can fail in two ways: readiness finds Chromium another way (for example, puppeteer's own cache), or the new code has a bug. Either way, the command upserts the working tree to the shared Supabase project.
  - That working tree is a wave branch that can be behind master. learn-hub CLAUDE.md documents this stale-overwrite failure: the TaskStop and stale-branch gotchas.
  - The command also breaks §0 rule 10: it calls the sync script outside an OWNER step.
  - Overriding environment variables does not help. `apply-sync.mjs` reads `.env.local` itself, not `process.env` (learn-hub CLAUDE.md, SessionStart gotcha).
- **Fix.**
  - S13-W1-4: add `--preflight-only` to `apply-sync.mjs`. It runs `runPreflight` and exits with its code before any Supabase client exists.
  - Add a vitest case that injects the client factory and asserts that `main()` calls the preflight first.
  - Change the check in S13-W1-4, S13 §5 criterion 9 and the W1 exit gate to `PUPPETEER_EXECUTABLE_PATH=/nonexistent node scripts/apply-sync.mjs --preflight-only; echo $?`. Expected: `2`.

### C2-05 · high · `check:skills` fails on every run (measured)

- **Where.** S21 §2.7 I22 (the `check:skills` command); S21-W0-2 done-when; plan §0 rule 5 (every learn-hub step); the standard exit gate.
- **Problem.**
  - `claude plugin validate --strict .claude/skills` exits 1: "No manifest found in directory".
  - The `.claude` form ("Validating components in …") exits 0. It also passes the 4 YAML-invalid skills, so the CLI does not check frontmatter YAML. Only skill-lint catches that.
- **Fix.**
  - Change I22 to `node scripts/lib/skill-lint.mjs && claude plugin validate --strict .claude && (learn-hub-session part unchanged)`.
  - S21-W0-2 done-when: record the command's output and exit code.
  - Optional: write `test:py` and `check:skills` as small node scripts, so they also run under npm's Windows shell. cmd.exe cannot run the bash `for` loop.

### C2-06 · high · 5 YAML-invalid skills break the W0 gates, and the trigger-lock seeds miss them

- **Where.**
  - S21-W0-1 done-when ("exits 0 on the current 11 skills") and S21-W0-2.
  - S12-W0-1 and S12-W0-2 (`triggers extract`).
  - S10-W0-1 and S10-W0-1b.
  - Plan rows 19–20 (their order) and §8 Q9.
- **Problem.**
  - Five skills fail `yaml.safe_load`:
    - learn-hub: concept-animation, ingest-animation, ingest-article, ingest-infographic;
    - micky: intent-lock.
  - Two learn-hub descriptions exceed 1,024 chars: atomize-book (1,075) and ingest-slides (1,150). Architecture §9 also lists ingest-article at 1,137.
  - So skill-lint exits 1 at W0, and `check:skills` fails every learn-hub step until W1.
  - S21-W0-1 runs before S12-W0-2. skill-lint check 9 (the ratchet) is therefore skipped, and no step seeds these entries.
  - A strict-YAML `triggers extract` cannot read these 5 descriptions, and no done-when checks lock coverage per skill. The lock then misses the phrases of the very skills that W1 and W3 rewrite. intent-lock carries Thai triggers.
- **Fix.**
  1. Add a new first W0 step in each repo: fold the 5 descriptions to `description: >-` with identical text.
     - Done-when: `yaml.safe_load` returns the same string that a raw-line read returns.
     - This moves H43's W1 fix earlier and applies the same fold to the other four.
     - It removes S10-W0-1b, the W0 ratchet-reading code in validate.py, and §8 Q9.
  2. Run S12-W0-2 before S21-W0-1.
  3. S21-W0-2: seed the learn-hub ratchet from `skill-lint --json` for the 3 over-cap descriptions. S17-W1-2, S17-W1-8 and S19-W1-8 close these entries.
  4. S12-W0-1 and S12-W0-2 done-when: every SKILL.md has at least one lock entry, or is listed as having no phrases.

### C2-07 · high · No step records the regression baseline, and no tool can compute it

- **Where.**
  - Plan standard gate "Smoke ≥ pre-rewrite baseline".
  - S12-W0-5 (counts files only), S12-W3-5 and S12-W5-1.
  - Architecture §6.4.
  - S15-W2-7 and S16-W2-7 ("no baseline").
- **Problem.**
  - S12-W0-0 tags `pre-rewrite` before any seed case exists, so the tag holds no cases.
  - No step runs the seed cases and records their scores. `baseline.md` holds sizes only.
  - The §6.4 method needs today's case dirs copied into the old plugin tree, whose layout differs after W3. `eval.sh` has no such mode.
  - So the R77 release gate cannot be computed.
  - For units with no seed cases, the smoke gate is undefined: concept-animation, ml-concept-lab, decision-interview, plan-critique, digest-report, ingest-visual and atomize-book.
- **Fix.**
  1. New step S12-W0-8, after S12-W0-5 and S12-W0-6: run `eval.sh --smoke` and `eval-project-skill.sh --smoke` on the 10 seeded units while the skill text is still unchanged. Write the per-case pass rates to `baseline.md` under `## W0 smoke`.
  2. Add `--against <ref>` to both runners:
     - `git worktree add` the ref;
     - copy today's `evals/<skill>/` dirs into the old plugin dir that holds `<skill>` (look it up by skill name);
     - run with the same flags and print the with-arm score.
     - S12-W3-5 and S12-W5-1 use this mode.
  3. Redefine the per-wave smoke gate:
     - seeded units: at or above their W0 score;
     - unseeded units: every grader passes (as S15 and S16 already say).
  - Count the extra old-version runs in the eval budget (C2-17).

### C2-08 · high · Verbatim moves are made by hand and checked only by 8-word fragments

- **Where.** S21-W4a-2, S21-W4a-3, S21-W4b-1, S13-W4-1, S19-W4-2 … S19-W4-6 (S19-W4-3 renumbers during the move), and risk K11.
- **Problem.**
  - An agent is to copy "verbatim", through Write and Edit, about 240 KB of CLAUDE.md text and about 1,000 lines of atomize-book.
  - The exactly-once check compares only the first 8 words of each heading. A changed number, a dropped sentence or a merged line inside a block still passes.
  - S19-W4-2 says "diff the moved text" but gives no command.
  - S19-W4-3 renumbers in the same commit as the move, so no diff can prove the text is unchanged.
  - `gotchas-archive.md` is also a hand copy, so it can carry the same errors.
  - S10-W3-10 already uses the right pattern: save a copy, then compare bytes.
- **Fix.**
  - Move by script, not by hand. Add learn-hub `scripts/move-blocks.mjs --map docs/rewrite/gotcha-map.md`:
    - it cuts each block, from its heading line to the line before the next heading;
    - it appends the block to its destination with the provenance comment;
    - its test proves that `sha256` of the sorted blocks is the same before and after the move.
  - Each W4 move step uses that byte check as its done-when.
  - atomize-book: in each step, `diff <(sed -n '<a>,<b>p' <saved copy>) <moved part>` must be empty.
  - Split S19-W4-3 into a move commit and a separate renumber commit.
  - Generate `gotchas-archive.md` with the same script from `git show wave-2:CLAUDE.md`, or drop it: the `wave-2` tag already holds the text.

### C2-09 · medium · The gotcha map uses stale line numbers; no freeze; CLAUDE.md can grow back

- **Where.**
  - S21 §2.4 and S21-W4a-1; plan §0 rule 3; the scope of the S19-W4-1 freeze.
  - S21 keeps "Documentation upkeep" unchanged. learn-hub `CLAUDE.md:3120` reads "New trap discovered → add it to Gotchas".
- **Problem.**
  - Most learn-hub feature sessions add a gotcha to CLAUDE.md. By W4, the 136 line numbers from 2026-09-24 will not match, and rule 3 then stops every W4 step.
  - Headings added after today have no row in the map, so the exactly-once check cannot account for them.
  - After W4, the unchanged upkeep rule sends new traps back into CLAUDE.md. Nothing checks the 32 KB target, so it erodes.
- **Fix.**
  1. Key map rows by heading text. S21-W4a-1 regenerates the map from the live file at W4 entry and classifies any new heading.
  2. Extend the S19-W4-1 freeze to "no edits to `## Gotchas` or `## Pages`" from S21-W4a-1 to S21-W4b-1.
  3. In S21-W4b-1, rewrite the upkeep line to: "New trap → add it to the file that `docs/rewrite/gotcha-map.md` names for its area; CLAUDE.md keeps pointers only." Add a skill-lint check that fails when `CLAUDE.md` exceeds 32,768 bytes.
  4. Plan §0 rule 3: if the quoted text still occurs exactly once (`grep -Fc` prints 1), use its new line and note that in the commit. Stop only when the text is gone or matches more than once.

### C2-10 · medium · vault-keeper writes to the learn-hub inbox in W1, before the inbox contract exists

- **Where.** S07-W1-1 (resolution step 2 returns `destination: inbox`), S07-W1-3, S11-W1-1 (V2), S15-W2-1.
- **Problem.**
  - The cloud environment has `LEARN_HUB_DIR` from W0 (S11-W0-5). After S07-W1-3, every vault-keeper save in the cloud resolves to `research-notes/`.
  - The W1 skill has no inbox-writing logic yet: `.meta.json`, the filing sentences and the slug rule arrive at S07-W2-1, and I09 arrives at S15-W2-1.
  - So the W1 save can write MOCs, an index and artifacts into learn-hub. This reverses W2's rule "consumers before producers".
- **Fix.**
  - S07-W1-1: add `--vault-only` to `sink.py resolve`. It skips step 2. Test it in `test_sink.py`.
  - S07-W1-3: Step 0 calls `sink.py resolve --vault-only`.
  - S07-W2-1: remove the flag, in the same commit that adds the filing sentences.

### C2-11 · low · The empty-vault W1 stopgap keeps a delete step with no definition of "landed"

- **Where.** S07-W1-2; empty-vault `SKILL.md:71-93` today.
- **Problem.** S07-W1-2 deletes Step 2 (the hand-off) and Step 3's verification language, but keeps Steps 4 and 5, which delete the verified files. "Landed" then has no procedure, and the model may invent one.
- **Fix.**
  - S07-W1-2 also replaces Steps 3–5 with: "Stop after the manifest. Nothing is transferred or deleted until the W2 transfer lands."
  - Done-when adds `grep -c 'Delete the verified files'` = 0.

### C2-12 · medium · Unfixed alignment plugins load in the cloud for all of W3

- **Where.** S11-W3-1 (V6 at W3 entry); S10-W3-1 depends on S11-W3-1; plan OQ4; S11 §8.4.
- **Problem.**
  - At W3 entry, V6 (the folder path) loads master's tree: 14 old plugins, including intent-lock, decision-interview and plan-critique with H01–H04 still open.
  - They stay loaded in every cloud session until the W3 merge, weeks later.
  - S10-W3-1 depends on S11-W3-1 only to keep one done-when path valid. Commits on the branch do not need the new env value.
  - A missing path is skipped with a "Path not found" line, and the session still exits 0 (architecture Appendix B1, probe P1).
- **Fix. Owner decision; options, recommended first.**
  - **(a) Union value V5'.**
    - Set V5' = V5 plus the family folder paths `/home/user/micky-psych-tools/plugins/{alignment,evidence,visuals}`.
    - Wave-branch model: add all three at W3 entry. Master sessions do not have these dirs and load V5; W3-branch sessions load the families.
    - Per-PR model (C2-03 a): add alignment only once S01's rewrite is on master.
    - Switch to V6 together with the last merge. Drop the S10-W3-1 → S11-W3-1 dependency.
    - The OQ4 exception for the four plugins goes away.
  - **(b) Keep the plan.** V6 at W3 entry, plus the OQ4 exception.

### C2-13 · medium · The new validator lands after the change it should guard, as one large commit

- **Where.** S08-W3-1 (placed after S10-W3-2); plan W2 exit (no `--cross-repo` check, §8 Q12); CX-36.
- **Problem.**
  - One commit creates validate.py (16 VAL checks, including cross-repo), release.py and 5 lists, and also edits the manifest and health.sh and deletes two files.
  - It waits for the skeleton only so that S10-W3-2's done-when path stays valid (CX-36). As a result, the largest W3 change is checked by the old W0 validator, and W2's cross-repo gate has no implementation.
  - The skeleton does not move plugin-creator.
- **Fix.**
  - Split S08-W3-1 into four steps:
    - (a) validate.py at `plugins/plugin-creator/scripts/`, its tests, and a ratchet seed for its new checks;
    - (b) the lists;
    - (c) the health.sh switch;
    - (d) release.py and the deletion of `scripts/bump.py`.
  - Run (a)–(c) at W2 exit, after S15-W2-6 and S05-W2-1. Keep (d) in W3, because the W2 release steps still call bump.py.
  - Change S10-W3-2's done-when to `$VALIDATE --repo .`.
  - This closes §8 Q12.

### C2-14 · medium · The skeleton commit is no longer "move only" and cannot be reviewed as one commit

- **Where.** S10-W3-1 + S10-W3-2 (one commit); the plan §0 rule 4 exception; risk K18.
- **Problem.**
  - After CX-1, CX-2 and CX-3, this one commit does all of the following:
    - moves 10 plugins and deletes their `commands/` dirs;
    - creates 7 alias skills and 3 manifests;
    - removes duplicate scripts and renames README/CHANGELOG files;
    - moves `.mcp.json`, `examples/` and the ledger;
    - rewrites marketplace.json.
  - K18's mitigation ("move-unchanged only") no longer holds. A reviewer cannot separate the moves from the new content.
- **Fix.**
  - Use one PR with 4 commits, each green under the pre-commit hook:
    - one commit per family (alignment, evidence, visuals): create the family `plugin.json`, `git mv` the members, delete the old dirs, and update that family's marketplace entries and `renames` rows;
    - then one commit: add the alias skills and delete every `commands/` dir.
  - Review the moves with `git diff -M100% --stat --diff-filter=R`. To revert, revert the PR merge.
  - Remove the exception from §0 rule 4.

### C2-15 · medium · The ratchet exit gate ("fewer entries") cannot pass

- **Where.** Plan §3 standard gate ("fewer entries than at entry"); plan §5, `ratchet.json` row; S08-W3-1 (it seeds existing violations as ratchet entries).
- **Problem.**
  - The micky ratchet starts empty and gains one entry in W0, so it grows.
  - W1 and W2 close nothing in micky: the only entry is intent-lock, which is fixed in W3. "Fewer" fails in both waves.
  - S08-W3-1 seeds new check ids in W3, so the count can grow in W3 too.
  - Plan §5 does not list S08-W3-1 as a writer of `ratchet.json`.
- **Fix.**
  - New gate: `ratchet verify` exits 0, and no check id's count grew, except check ids first seeded in this wave by named steps (S12-W0-1, S21-W0-2, S08-W3-1).
  - List, per wave, the entries that must close.
  - Add S08-W3-1 to the `ratchet.json` row in §5.
  - With C2-06's W0 folds, micky has no ratchet entry at W0.

### C2-16 · medium · The h-coverage grep fails at W1 on rows split across two waves

- **Where.** Plan §3 standard gate `grep -E '^- \[ \] H.*wave: W<n>'`; S12 §2.3 seed format; Appendix A rows H07 (W1/W3), H10 (W1/W2) and H11 (W1/W2).
- **Problem.**
  - Either the seed copies the Wave cell, and these rows read `wave: W1/W2`, or, as in S12 §2.3's example (`H07 … wave: W1`), it drops the second wave.
  - In the first case, the W1 grep matches the rows while they are open. A checkbox cannot record "W1 part closed", so either W1 exit fails or the rows are ticked early.
  - In both cases, W2 and W3 stop checking the rest of the fix.
- **Fix.**
  - Seed each split row as two lines: `H10a … wave: W1` and `H10b … wave: W2`. Do the same for H07 and H11.
  - Anchor the gate regex at the line end: `wave: W<n>$`.
  - The W0 gate count becomes 52 instead of 49.

### C2-17 · medium · The cost of evals and live-trigger runs is not budgeted

- **Where.** Plan §2 "Eval cost points"; OQ3; S12-W3-2 and -3; S12-W4-2 and -3; S12 §4.4 ("once more at W5"); S12-W3-5; S12-W5-1.
- **Problem.** Estimates (method shown):

  | Item | Runs | Notes |
  |---|---|---|
  | One live-trigger pass | 5 families × 20 queries × 3 runs = 300 `claude -p` | each run pays about 108k tokens before the W4 diet (architecture §9) |
  | All live-trigger passes | W3 before and after, W4 before and after (2 families, 120 each), W5 | about 1,140 |
  | Release at W3 | about 16 skills × 5 cases × 3 runs × 2 arms | about 480 |
  | Release at W5 | about 30 skills, same formula | about 900 |
  | Old-version arm (C2-07) | added on top of the release runs | — |

  OQ3 budgets only the smoke runs and check d.
- **Fix. Owner decision; options, recommended first.**
  - **(a) Cut the counts.**
    - Measure before/after with `run_eval` only. Drop `run_loop` and the 60/40 split, which serve description tuning, not measurement.
    - Run each query once; run 3 times only the queries whose outcome flips.
    - Release: `--runs 3` for the gate skills and the report writers, `--runs 1` for the others.
    - OQ3 sets one number per cost point: per smoke run, per release run, per live pass.
  - **(b) Keep the architecture's counts** and budget them in OQ3.

### C2-18 · medium · Windows could load plugins in place from W1, which removes 12 release steps

- **Where.**
  - OD2 timing; S11-W3-2, S11-W1-2 and S11-W2-5; plan §8 Q14.
  - W1 release steps: S04-W1-3, S06-W1-5, S07-W1-4, S08-W1-2, S09-W1-2.
  - W2 release steps: S01-W2-2, S02-W2-2, S03-W2-5, S04-W2-3, S05-W2-6 (the bump part only), S06-W2-2, S07-W2-6.
- **Problem.**
  - Architecture §7: in-place loads ignore versions.
  - Before W3, releases exist only to push fixes to the Windows marketplace install.
  - Windows already runs all 14 unfixed plugins today, so loading in place adds no exposure. Fixes would then arrive with `git pull`.
- **Fix. Owner decision; options, recommended first.**
  - **(a) Switch Windows at W1 entry**, after check g = yes:
    - Windows user variable = the `<micky>\plugins` folder, plus the learn-hub plugins path once the V5 content exists;
    - uninstall the marketplace copies;
    - delete the 12 W1/W2 release steps, S11-W1-2, S11-W2-5 and Q14;
    - set each plugin's version once, with release.py, at W3;
    - each step still writes its CHANGELOG entry under `## Unreleased`;
    - keep the Windows checkouts on master and do rewrite work in a worktree (K9, S11 G5).
  - **(b) Keep the OD2-a timing** and switch at W3.

### C2-19 · medium · The visual audit is built twice, plus a parity harness to keep the two equal

- **Where.**
  - S05-W2-1 and -2: the check-html.mjs own port (26 codes, Playwright render and drive, three copies).
  - S05 I07-J: the parity fixture.
  - S16-W2-1 and -2: `audit:visual` (puppeteer).
  - S08: the VAL cross-repo parity check; plan §8 Q7.
- **Problem.**
  - Architecture §5.5: ingest-visual runs `audit:visual` on every visual before filing and refuses on failure. The producer-side port only pre-checks what the consumer checks again.
  - The port exists for sessions without a learn-hub clone. Both Windows and the cloud set `LEARN_HUB_DIR` (S11-W0-5, S11-W0-10).
  - The duplicate costs:
    - about 780 ported lines;
    - two browser drivers;
    - 3 byte-identical copies during W2;
    - a parity fixture and a cross-repo check.
- **Fix. Owner decision; options, recommended first.**
  - **(a) Delegate only.**
    - check-html.mjs delegates to `audit:visual`, and keeps a static subset of at most 60 lines: doctype, `lang`, color-scheme, `min-height:100dvh`, no `prefers-color-scheme:dark`, no external URL.
    - Without learn-hub it returns `incomplete`, which the producers already handle.
    - code-explainer keeps its own static check.
    - Drop the render port, the parity fixture, the VAL parity check and S05-W2-2's copies. Keep one copy under concept-animation until W3.
  - **(b) Keep the architecture's port** and the parity fixture.

### C2-20 · medium · No commit-time enforcement where the work happens

- **Where.**
  - Architecture §8 "Mechanical enforcement" (a pre-commit hook in both repos).
  - No spec adds a learn-hub pre-commit step; learn-hub `.githooks/` holds only `post-merge`.
  - In the cloud, micky's `core.hooksPath` is set only by S08's W3 hook.
  - S12 §4.4 says pre-commit runs the ratchet and lock checks through "S10/S13's wiring", but S13 has no such wiring.
- **Problem.**
  - In learn-hub, nothing stops a daily owner session from rewording a locked trigger or adding a lint violation between waves.
  - In W0–W2, micky cloud sessions commit without hooks unless the executor remembers to set them.
- **Fix.**
  - New step S21-W0-3: add learn-hub `.githooks/pre-commit`, written in node so it is portable. It runs `skill-lint.mjs` when `.claude/skills/**` or `CLAUDE.md` is staged. session-start already sets `core.hooksPath`.
  - Plan §0 step 2: until S08's hook lands, a cloud session runs `git -C /home/user/micky-psych-tools config core.hooksPath .githooks` before its first commit.

### C2-21 · medium · Rollbacks ignore live-DB side effects; the W3 per-family revert is undefined

- **Where.**
  - Plan §3 rollback text for W1, W2 and W3.
  - S14-W1-1: the owner deletes orphan rows.
  - S13-W1-10: live sync of an edit to a real note.
  - S07-W2-7: digest and sync of a real report.
  - Architecture §7.
- **Problem.**
  - Reverting a wave merge does not undo Supabase writes.
  - After a W2 revert, the rehearsal's notes stay in the DB while their vault files, which sit on the reverted branch, disappear. This is the "DB rows outlive their /vault source" trap.
  - W3 runs on one branch, and its family steps share files: ratchet.json, the lock, CLAUDE.md and the family README/CHANGELOG. A per-family revert is therefore not defined.
- **Fix.**
  1. S14-W1-1: the default is restore (`restore-vault-from-db.mjs --verify`). Before any delete, export the row to a JSON file.
  2. S13-W1-10 and S07-W2-7: commit the vault files they create directly to learn-hub master, not to the wave branch. The W1 and W2 rollback text says: "keep these commits; revert only the tooling".
  3. W3 rollback text: either per-family PRs (C2-03 a, C2-14), or "revert the W3 merge; to undo one family, revert its commit range listed in the W3 exit record, then rerun health".

### C2-22 · medium · digest-report calls a parser CLI that does not exist

- **Where.** S15 §2.3 row 3 (`node scripts/lib/report-parse.mjs <path> --json`); S15 §2.5 ("library only … no CLI"); S15-W2-2, which depends only on S15-W2-1.
- **Problem.** A module with no main prints nothing and exits 0. The skill's classify step would get empty output, silently.
- **Fix.**
  - S15-W2-5: add a guarded CLI to `report-parse.mjs`. `--json <path>` prints the ReportParse object and exits 1 when the parse throws. Add a vitest case for it.
  - S15-W2-2 depends on S15-W2-5.

### C2-23 · medium · Move the learn-hub CLAUDE.md stage (b) diet before W1

- **Where.** OD11 staging (stage a, then stage b, both in W4); the dependencies of S21-W4b-1.
- **Problem.**
  - Until W4, every multi-repo session and every live-trigger run pays about 67k tokens for learn-hub CLAUDE.md (architecture §9).
  - Stage (b) moves Pages plus the 70 app gotchas, about 140 KB by S21's section sizes. It needs only W0 check e, not any W2 or W3 work.
- **Fix. Owner decision; options, recommended first.**
  - **(a) Run stage (b) right after W0 check e = yes**, before W1, using the C2-08 mover and the C2-09 freeze. Stage (a) stays in W4.
    - This saves about 35k tokens per session for about 18 sessions.
    - It also brings the W3 trigger measurements closer to the final context.
  - **(b) Keep both stages in W4.**

### C2-24 · low · The plan does not say which session type each block needs

- **Where.** Plan §2 sessions table; plan §0.
- **Problem.** The plan assumes multi-repo sessions throughout. micky-only blocks do not need learn-hub: W0 micky tooling, the W1 micky fixes and most of W3. In a micky-only session they would avoid about 67k tokens each.
- **Fix.**
  - Add a "session" column to the §3 tables:
    - `micky-only` for rows that touch only micky (with `LEARN_HUB_DIR` unset, the cross-repo checks warn instead of fail);
    - `multi` for cross-repo rows and V steps.

### C2-25 · low · Two vault-keeper scripts are planned for a vault of 16 files

- **Where.** S07-W2-3 (`vault_index.py`); S07-W2-4 (`drain_plan.py`, 4 subcommands); S07-W2-5 (12 cases); S07-W2-7 (rehearsal); the OD4 revisit at W5.
- **Problem.**
  - `vault/` holds 16 files: 7 artifacts, no notes, no assets.
  - The sink sends every output to the inbox whenever `LEARN_HUB_DIR` validates, which it does in the cloud and on Windows. So the micky vault receives output only from sessions without a learn-hub clone.
  - Defect vault-keeper-8 (medium) needs one prose rule, not a script.
- **Fix. Owner decision; options, recommended first.**
  - **(a) Cut and defer.**
    - Cut `vault_index.py`; state the dangling-versus-broken link rule in prose.
    - Defer `drain_plan.py` to W5. Build it only if the OD4 revisit keeps the vault.
    - In W2, copy the 7 artifacts to `research-notes/` once, with the owner watching, and keep the no-delete stopgap (C2-11).
    - H10 and H11 then close on the W1 stopgap plus the one-time copy.
  - **(b) Keep the plan.**

### C2-26 · low · Two implementations of the rewrite gate; the h-coverage file is mirrored

- **Where.** S12-W0-1 and -2 (`rewrite_gate.py` and `rewrite-gate.mjs`, mirrored 1:1); plan §0 rule 9 (one commit per closure, plus mirroring at each wave exit); S12 acceptance criterion 6.
- **Problem.**
  - The seed, close, remove and measure subcommands run only during the rewrite, by an executor who has both clones.
  - Long term, learn-hub needs only `verify`.
  - Rule 9 adds about 49 closure commits plus a copy step at each wave exit. It also contradicts "one step = one commit".
- **Fix.**
  - Keep `rewrite_gate.py` as the only generator; for learn-hub files, run it with `--repo /home/user/learn-hub`.
  - In learn-hub, keep a `verify` of at most 40 lines for the ratchet and the lock, inside skill-lint check 9.
  - Keep one `h-coverage.md`, in micky `docs/rewrite/`.
  - Close rows once per wave, at exit, from plan §7's table.

### C2-27 · low · The atomize-book freeze window is longer than needed

- **Where.** S19-W4-1 (the freeze runs from W4 start to S12-W4-T); plan W4 order (S19-W4-8 sits at row 13, after unrelated rows).
- **Problem.** Only S19-W4-2 … S19-W4-9 touch atomize-book. The freeze also spans the gotcha moves, ingest-article, pdf-pipeline, verify, the live-trigger runs, and any wait for W3 when the waves run in parallel.
- **Fix.**
  - The freeze runs from the start of S19-W4-2 until S19-W4-9 passes.
  - Schedule S19-W4-2 … 6, S19-W4-8, S19-W4-7 and S19-W4-9 back to back, in one session.

### C2-28 · low · Step rollbacks assume nothing has been committed yet

- **Where.** Plan §0 steps 4–5; many spec rollbacks: `git checkout -- …`; S15-W2-3 `git checkout HEAD~1 -- plugins/digest-report`; S16-W2-4 and S16-W2-6.
- **Problem.** Rule 4 commits before rule 5 runs the checks. After a commit, `git checkout --` does nothing, and `HEAD~1` is correct only right after that commit.
- **Fix.** Plan §0: run the done-when and repo checks before committing. On failure, apply the spec's rollback to the working tree. After a commit, the rollback is `git revert <sha>`.

### C2-29 · low · Some OWNER steps are read-only commands an executor can run

- **Where.** S15-W2-OWNER (a read-only Supabase MCP query); S16-W2-OWNER (`npm run audit:visual` with Chromium); the tag steps.
- **Problem.** There are 31 OWNER steps for one owner. These particular steps need no owner authority: cloud sessions have the Supabase MCP and Chromium.
- **Fix.**
  - Mark these as executor steps.
  - Keep OWNER for env edits, Windows steps, live writes, deletes and the tag that ends a wave.

### C2-30 · low · The check b = no path breaks W2

- **Where.** S11-W2-4 (skipped if b = no); S07-W2-7, which depends on S11-W2-4; plan W2 exit gates "LH plugins folder" and "Load once: 11 entries".
- **Problem.** When b = no, S14-W2-1 and V5 are skipped. S07-W2-7's dependency then never completes, and two W2 gates fail.
- **Fix.**
  - S07-W2-7 depends on "S11-W2-4 or its skip record".
  - When b = no, the W2 gates expect an absent or empty `learn-hub/plugins` and 10 entries.

### C2-31 · low · Running W3 and W4 in parallel can confound W4's live-trigger scores

- **Where.** Plan §2 "W3 ∥ W4"; S12-W4-2 and -3 (families 4 and 5 list micky skills as expected routes).
- **Problem.** If W3 merges between S12-W4-2 and S12-W4-3, micky description changes shift the family 4 and 5 scores.
- **Fix.** Either:
  - run S12-W4-2 and -3 with micky checked out at tag `wave-2` (`git -C /home/user/micky-psych-tools checkout wave-2` in that session); or
  - run both before the W3 merge.
