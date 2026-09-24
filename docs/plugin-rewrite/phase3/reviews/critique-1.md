# Critique 1: goal-fit, completeness, verifiability, hidden assumptions

Date: 2026-09-24. Target: `wf3/plan.md` and the specs it points to.

**Read in full:** plan.md; architecture.md §1–§13 and Appendices A–C; specs S01, S10, S13, S14, S19.
**Read in part:** S11, S12, S17, S04, S08, S21, S16, eval-format.md, coverage.md, summaries.json, reconcile-1/2.

**Checked by command (read-only; scratch files only):**
- `which bwrap socat`: both absent in the cloud image.
- `claude plugin validate --strict` on scratch plugins: it passes invalid PyYAML and a 1,150-char description.
- skill-creator `run_eval.py`: it measures a temporary clone of the skill.
- learn-hub:
  - `apply-sync.mjs` env loading;
  - gate CLI flags;
  - puppeteer usage;
  - `Book/` and `raw book/` absent in the cloud checkout;
  - README.md and CLAUDE.md text about the PreToolUse gate;
  - `git log` churn;
  - 354 atomize-book tests pass.
- coverage.md: rows that have no step id.

**Verdict:** The plan covers every unit in architecture §3. It does not yet reach a checkable end state, for four reasons:
- Its branch model contradicts its own cloud-enablement steps.
- The eval gates compare against a baseline that no step produces.
- The eval runners cannot run Bash-granted or scaffolded cases in this environment.
- The live trigger runner measures a copy of the skill, not the skill itself.

Two W1 steps also risk harm:
- On Windows, the new sync preflight refuses every sync.
- A done-when check runs the real sync against the live database.

## Findings index

| # | Sev | Where | Problem (short) | Owner decision |
|---|---|---|---|---|
| F1 | high | plan §0 rule 2; arch §7; S11-W1-1/-2, S11-W2-3, S11-W3-5, S13-W1-10 | Wave branch "merged at exit" vs steps that need fixes on master mid-wave | yes |
| F2 | high | plan §3 standard gates; S12-W3-5, S12-W5-1; §2.7 cond. 4 | "≥ pre-rewrite baseline": no step runs or records the baseline | yes |
| F3 | high | S12 eval.sh / eval-project-skill.sh; S11 setup script; plan W1 exit | Bash-granted cases refused (no bwrap/socat); scaffolds never run; env vars stripped; W1 gate filters out its own case | no |
| F4 | high | arch §6.3; S12-W3-2/-3, S12-W4-2/-3 | skill-creator `run_eval` measures a clone that competes with the real skill | no |
| F5 | high | S13 §2.5 `checkChromium`; arch §2.6 | Preflight refuses every Windows sync (Windows has no `PUPPETEER_EXECUTABLE_PATH`) | no |
| F6 | high | S13-W1-4 done-when; plan W1 exit "Sync refuses unready" | Test runs the real `apply-sync.mjs` with live credentials | no |
| F7 | medium | 20 specs' §6; S04-W3-3; S12 §2.5 | Trigger-lock removals have no commands; S04 uses undefined flags; LH scan roots undefined | no |
| F8 | medium | plan §0 rules 6–7; S10-W0-9; arch §8 R69; S12 §4.4 | Ratchet/lock not checked per commit; no learn-hub pre-commit | no |
| F9 | medium | S21 `test:py`; S13 readiness; hooks; S10 health.sh | Windows: npm runs cmd.exe; `python3` vs `python`; bash hooks | no |
| F10 | medium | S13 I14 done-marker | Marker on disk skips per-session setup in a reused container | no |
| F11 | medium | S13 §2.5 `runPreflight` | Gate subprocesses without cwd; a crash becomes silent "" | no |
| F12 | medium | learn-hub README.md:159-163, CLAUDE.md:2615-2651; plan §0 rule 8 | No learn-hub README/CLAUDE.md upkeep; stale text moved verbatim at W4 | no |
| F13 | medium | S21-W4a-1…W4b-1; S19-W4-1 freeze | CLAUDE.md edited 15×/month by other sessions during W4 surgery | yes |
| F14 | medium | S19-W4-9; plan W4 row 15 | Chapter re-run needs `Book/` (absent in cloud); no pre-split baseline | no |
| F15 | medium | plan §0 step 3 | "Stop on any line drift" stalls a repo with ~10 commits/day | no |
| F16 | medium | plan §2 "W3 ∥ W4" | Parallel W4 confounds W3 before/after trigger scores | no |
| F17 | medium | S14-W1-1 | Orphan audit covers all orphans; offers raw SQL deletes | no |
| F18 | low | plan §3 ratchet gate | "Fewer entries than at entry" fails in W0 and in waves that seed checks | no |
| F19 | medium | plan links; specs `<wf3>/…`; S01 §4.4 | Phase-3 files exist only in /tmp; linked repo paths do not exist | no |
| F20 | low | coverage.md; plan §7 | 104/313 rows lack a step id; the no-step list disagrees with plan §7 | no |
| F21 | low | S21-W1-4 done-when | Grep text does not match the sentence the step adds | no |
| F22 | low | S13-W1-6 and other done-when | `claude plugin validate --strict` does not check YAML strictness or the 1,024 cap | no |

## High

### F1. The branch model contradicts the cloud-enablement steps

**Problem.** The plan and the specs assume two different branch models.

*What the plan and architecture say:*
- Plan §0 rule 2: one branch per wave per repo (`rewrite/w<n>`).
- Architecture §7: "merged at wave exit".

*What the steps need:* the steps below load the default branch in the cloud (S11 notation: "on the default branches unless stated"), so they need the fixes on master mid-wave:
- S11-W1-1 enables vault-keeper, firecrawl and plugin-creator before `wave-1`. It checks what master loads, not the fixed code.
- S11-W1-2 says "pushed to `origin/master`".
- S11-W2-3 merges the CA-copy deletion "into learn-hub master" while micky CA's W2 rewrite sits on `rewrite/w2`. Result: a double load (K5), or V4 loads the unfixed CA.
- S11-W3-5 says "W3 skeleton merged" at W3 row 6.
- S13-W1-10's live sync must run through the new preflight, which is not on master yet.

*Other consequences:*
- The rollbacks ("revert the per-repo W1 merge"; W3 "revert per family") assume a merge shape the steps do not produce.
- If W3 merges early, two things break on live master:
  - `/digest` points to `evidence:lit-watch`, which does not exist until S04-W3-3 (22 rows later).
  - misread-capture still writes `${CLAUDE_PLUGIN_ROOT}/skills/intent-lock/references/misreads.md` after S10-W3-2 moved the ledger to `state/`, until S01-W3-3.

**Fix.** Pick one model and write it into plan §0.

- **(a) Recommended.** Merge one PR per unit to master when the unit's done-when and repo checks pass.
  - Every enablement or live row gets "merged to `origin/master`" in its Depends on.
  - The wave tag marks master at exit. Rollback reverts the listed PRs; the delivery log names them.
  - For W3:
    - S10-W3-2 writes the `digest` alias as "Invoke `evidence:psych-paper-digest`"; S04-W3-3 changes it to lit-watch.
    - S10-W3-2 leaves `misreads.md` in place; S01-W3-3 moves it in the same commit as the path change.
- **(b)** Keep one merge per wave. Do it before the exit gates. Move every S11 enablement row and S13-W1-10 after that merge. Families then load only at W3 exit.
- **(c)** Point cloud sessions at `rewrite/w<n>`. Not recommended: it conflicts with K9.

### F2. No step produces the "pre-rewrite baseline" that the eval gates compare against

**Problem.** Several gates compare scores to a pre-rewrite baseline:
- the plan's standard gate "smoke ≥ `pre-rewrite` baseline";
- S12-W3-5 and S12-W5-1 "with-arm ≥ baseline";
- architecture §2.7 condition 4.

No step produces that baseline:
- The W0 seed steps (S03-W0-1 … S18-W0-1) only write case files.
- S12-W0-7 records sizes, not scores.
- No step runs `git worktree add … pre-rewrite` or records a score.
- The runners cannot target old code:
  - `eval.sh` always prefixes `plugins/<p>`;
  - `eval-project-skill.sh` copies from the current checkout.
- After W3 the families (`alignment`, `evidence`, `visuals`) have no pre-rewrite plugin.
- Cases added in W1–W3 need a fresh baseline run on the old skill.
- OD14's "~700 runs" leaves these runs out. They roughly double release cost.

**Fix.**
1. Add S12-W0-8:
   - `git worktree add ../<repo>-pre pre-rewrite` in both repos.
   - Add `--plugin-dir <path>` to `eval.sh` and `--skill-dir <path>` to `eval-project-skill.sh`.
2. Define the baseline per skill: that skill's new case dirs, run against its old plugin or skill dir. Record it in `docs/rewrite/baseline.md` under `## Eval baseline`, with the case-set hash.
3. Every step that adds or changes cases re-runs the baseline for those cases in the same step.

**Owner options:**
- **(a) Recommended.** Smoke-case baselines whenever cases change (cheap), plus release-case baselines only at W3 and W5.
- **(b)** Replace "≥ baseline" with absolute pass thresholds per case.
- **(c)** Full baselines every wave.

### F3. The eval runners cannot run Bash-granted or scaffolded cases here

**Problem.**
1. **No sandbox tools.** `bubblewrap` and `socat` are absent in the cloud image; `which bwrap socat` returns nothing. eval-format.md:195 says a Bash grant without a sandbox backend refuses each run, which "usually scores 0". Affected cases:
   - S07 smoke (`--allow-tools "Write,Bash,AskUserQuestion"`). Its result gates S11-W1-1 (§2.7 condition 4).
   - S01 release (`--allow-tools Bash`), S05 release (`Bash(node *)`).
   - S13 `sync-preflight-before-apply` and S17 `inbox-survey-and-ask`.
2. **Scaffolds never run.** A `scaffold_script` runs only with `--scaffold` (eval-format.md:115, :261), and no spec or wrapper passes it. So these cases start in an empty workspace:
   - S01 `append-writes-ledger`;
   - S07 `verify-before-delete-fixture-inbox` (smoke);
   - S13 `sync-preflight-before-apply`;
   - S17 `inbox-survey-and-ask`.
3. **Grants are missing from the plan's gate.** The standard gate `bash scripts/eval.sh --smoke <p>` drops each spec's `-- --allow-tools …`.
4. **The W1 gate filters out its own case.** "Bare ingest-article asks" runs `--smoke`, but the case it cites is tagged `[ingest-article, process, output]`. `--tag smoke` excludes it.
5. **Environment variables are stripped.** Runs inherit only an allowlist plus `EVAL_*` (eval-format.md:249).
   - `LEARN_HUB_DIR`, `MICKY_TOOLS_DIR` and `ARTICLE_INBOX_DIR` are absent, so sink and ledger cases cannot use them.
   - S17 sets `EVAL_ARTICLE_INBOX_DIR`, which no skill reads.

**Fix.**
- Add `apt-get install -y bubblewrap socat` to `cloud-setup.sh` (next `SETUP_VERSION`).
- Add W0 check d2: one case that grants Bash and uses a scaffold runs and passes in a new cloud session.
- `eval.sh` and `eval-project-skill.sh` always pass `--scaffold`. The suites are owner-written, which is the documented condition.
- Plan gate text: "run the spec's §4.4 smoke command verbatim".
- Tag S17 `inbox-survey-and-ask` as `smoke`, or change the W1 gate to `--case inbox-survey-and-ask`.
- Rewrite cases that depend on an env var: the scaffold creates the marker files in the workspace, and the prompt names the path. Drop `EVAL_ARTICLE_INBOX_DIR`; the default relative path already works.

### F4. The live trigger runner measures a clone, not the real skill

**Problem.** skill-creator `run_eval.py` does not test the real skill:
- **It tests a clone.** It writes a temporary `.claude/commands/<skill>-skill-<id>.md` holding the description into the project root. It counts only calls to that clone (run_eval.py:44-68, :147-166).
- **The clone competes with the original.** In a multi-repo session (V6 folder path; learn-hub `.claude/skills`), the real skill with the same description is also loaded. Every real trigger counts as a miss.
- **It gives up early.** It returns false when the first tool call is anything but Skill or Read.
- **Families cannot be isolated.** After the merge, the siblings share one plugin. Removing the plugin also removes the competitors.
- **The load set is unverified.** A `claude -p` child started from `/home/user` may not load learn-hub `.claude/skills` or both CLAUDE.md files the way a platform-started session does. This also affects the routing smoke.

K7's before/after checks (S12-W3-2/-3, S12-W4-2/-3) therefore measure noise.

**Fix.**
- Run the live trigger families with the routing-smoke method: `claude -p "<q>" --output-format stream-json --verbose` from the multi-repo root.
  - Read the first `Skill` tool_use `input.skill` and match it against the real names.
  - 3 runs; 0.5 threshold; same query sets.
- Add W0 check i: a `claude -p` child from `/home/user` lists the same skills and CLAUDE.md as a platform-started session. If it does not, pass `--add-dir` for both clones and record the flags in S12.

### F5. The W1 preflight refuses every sync on Windows

**Problem.**
- S13 `checkChromium` is ok only if `PUPPETEER_EXECUTABLE_PATH` is set and exists.
- Architecture §2.6 sets that variable to "unset" on Windows.
- learn-hub puppeteer ^25 uses its own downloaded browser there; `mermaid-render.mjs` passes no `executablePath`.

So after S13-W1-4, every Windows `npm run sync:apply` exits 2. The owner syncs from Windows (see the CLAUDE.md TaskStop gotcha). `ready.mjs` also reports Chromium "FAIL" in every pipeline Step 0 on Windows.

**Fix.**
- `checkChromium(env, resolveBundled)`:
  - ok if the variable is set and the path exists;
  - else ok if `puppeteer.executablePath()` exists;
  - inject the resolver for tests.
- Add a test: variable unset + bundled browser present → ok.
- Add `node scripts/ready.mjs --json` on Windows to S11-W0-10 (check g).

### F6. A non-owner done-when check runs the real sync against the live database

**Problem.**
- S13-W1-4 done-when and the plan's W1 exit gate both run `PUPPETEER_EXECUTABLE_PATH=/nonexistent node scripts/apply-sync.mjs` in a checkout whose `.env.local` holds live credentials (the session-start hook creates it).
- Only a correct preflight stops a full live upsert into the project shared with board-prep-hub.
- This breaks plan §0 rule 10 (no `sync:apply` outside an OWNER step).
- If `checkChromium` falls back (as F5 requires), the command no longer refuses at all.

**Fix.**
- Run the refusal test in a throwaway worktree with a fake `.env.local`:
  - `NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:9`, dummy key;
  - `node_modules` symlinked.
  - Even a wrong pass then cannot reach Supabase.
- Add a vitest test of a pure gating function (`gateOnPreflight(result) → {proceed, exitCode, stderr}`) that `main()` calls.
- Change the W1 exit gate to the worktree form.

## Medium

### F7. The trigger-lock procedure is missing from the steps

**Problem.**
- Specs list removed or moved phrases in §6. Examples:
  - S03: 4;
  - S08: 5;
  - S14: 6 (whole forks);
  - S15: 3;
  - S19: 3 ("re-sync the vault", "import `<book>` …");
  - S17: "bullet-reconstruct this".
- Only S04-W3-3 runs a lock command.
- S04-W3-3 calls `triggers remove --skill …` and `triggers extract --skill … --reason`. S12 §2.5 defines only `triggers extract` and `triggers remove --phrase --reason`.
- S12-W0-2 does not say whether the learn-hub `triggers extract` scans `.claude/skills/*/SKILL.md`. If it does not, K7 has no guard for learn-hub. If it does, every W1/W2 deletion and edit fails `triggers verify` at wave exit.

**Fix.**
- In S12-W0-1/-2, define the scan roots:
  - micky: `plugins/*/skills/*/SKILL.md`;
  - learn-hub: `.claude/skills/*/SKILL.md` + `plugins/*/skills/*/SKILL.md`.
- Add `--skill` bulk forms to `remove` and `extract`.
- Add the exact `triggers remove` command to every step whose §6 row says removed or moved. Example: S14-W2-3/-4 remove the fork phrases with reason "fork retired, kept in micky".

### F8. Ratchet and trigger lock are not enforced per commit

**Problem.**
- Plan §0 rules 6–7 say a new violation "fails the step".
- The per-step checks do not run `ratchet verify` or `triggers verify`:
  - `health.sh --fast` (S10-W0-9);
  - `npm test && test:py && check:skills`.
- Architecture §8 (R69) requires `.githooks/pre-commit` in **both** repos. No spec creates the learn-hub one.
- S12 §4.4 claims pre-commit wiring "by S10/S13". Neither spec has it.

**Fix.**
- S10-W0-9 (after S12-W0-1): add `python3 scripts/rewrite_gate.py ratchet verify && python3 scripts/rewrite_gate.py triggers verify` to `--fast`.
- New S21-W0-3: `.githooks/pre-commit` in learn-hub, running `npm run check:skills` + `node scripts/rewrite-gate.mjs ratchet verify` + `triggers verify`. `session-start.sh` already sets `core.hooksPath`.

### F9. Windows toolchain assumptions are not checked

**Problem.**
1. **`test:py` fails under cmd.exe.** S21's `test:py` is a bash `for` loop. npm runs scripts with cmd.exe on Windows by default, which cannot parse it.
2. **`python3` may not exist.** `test:py`, `readiness.checkPyMuPDF` and micky `health.sh` call `python3`. learn-hub docs use `python`: CLAUDE.md has 0 hits for `python3`; atomize-book SKILL.md has 12 `python` calls and 0 `python3`.
3. **Hooks fire on Windows.** Under OD2-a (S11-W3-2), both plugin folders load on Windows. The `learn-hub-session` hook execs `bash`, and the plugin-creator hook uses POSIX `test`. Neither has been run on Windows.

**Fix.**
- Extend check g (S11-W0-10) with: `python3 --version`, `python --version`, `bash --version`, `npm config get script-shell`, `npm run test:py` (dry).
- Write `test:py` as `node scripts/test-py.mjs`:
  - try `python3`, then `python`, then `py -3`;
  - walk the dirs with `fs`.
- `checkPyMuPDF` uses the same interpreter search.
- S11-W3-2 done-when adds "a new Windows session starts with no hook error".

### F10. The session-start done-marker skips per-session setup

**Problem.**
- I14 writes `<root>/.claude/.session-start.done` to disk.
- The marker wraps the `CLAUDE_ENV_FILE` export of `PUPPETEER_EXECUTABLE_PATH`, which each session needs in its own env file, and the `.env.local` refresh.
- A second session in the same container (a resume or a reused VM) therefore skips both.
- The preflight then refuses to sync, which is safe but a false stop. A rotated key stays stale.

**Fix.**
- Store `$CLAUDE_ENV_FILE` (or the hook's stdin `session_id`) in the marker. Re-run the export and the `.env.local` step when it differs; skip only `npm install`.
- Add a test: second invocation with a new `CLAUDE_ENV_FILE` → the export is written.

### F11. Sync gates can fail silently inside the preflight

**Problem.**
- `runPreflight` spawns `node scripts/gate-duplicates.mjs` with no `cwd` (only the git call gets `cwd: root`). It maps any crash to `""`.
- From `/home/user`, or any cwd outside the repo, both gates crash and say nothing. That is the "silent gate" failure K3 names, in the layout the move was meant to fix.

**Fix.**
- `execFile(process.execPath, [join(root, "scripts/gate-duplicates.mjs"), "--json"], {cwd: root})`.
- On a crash, add the line `gate unavailable: <name> (<error>)`. Keep it warn-only.
- Add a vitest case: gate error input → the report names it.

### F12. learn-hub README.md and CLAUDE.md upkeep is missing

**Problem.**
- learn-hub rules require README.md and CLAUDE.md updates in the same change. Plan §0 rule 8 covers only CHANGELOG, and no spec edits learn-hub README.md.
- After S13-W1-7:
  - README.md:159-163 still says the gate "fires automatically before a sync via a `PreToolUse` hook … To bypass it, delete that hook entry".
  - CLAUDE.md:2615-2618 and :2649 still describe the PreToolUse gates.
- W4 then moves those gotchas "verbatim", so the stale text lands in `sync-vault/references/gotchas.md`.
- The README script table lacks:
  - `sync:preflight`, `test:py`, `check:skills`, `audit:visual`, `book:check-mermaid`;
  - `scripts/eval-project-skill.sh`.

**Fix.**
- S13-W1-7 edits the README paragraph and the two CLAUDE.md sentences in the same commit.
- Each step that adds an npm script adds its README row: S13-W1-5, S21-W0-2, S16-W2-2, S19-W1-4.
- Plan §0 rule 8 adds: "LH: README.md and CLAUDE.md upkeep in the same commit (learn-hub CLAUDE.md, Documentation upkeep)".
- W4 verbatim moves carry a one-line dated note where W1 made the text stale.

### F13. The W4 CLAUDE.md surgery runs while other sessions edit the file

**Problem.**
- learn-hub CLAUDE.md changed 15 times in the last 30 days; the repo had 320 commits.
- W4 makes 7 sequential CLAUDE.md edits (S21-W4a-3 → W4a-2 → S13-W4-1 → S19-W4-8 → S21-W4b-1) against a fixed count of 136 headings and fixed line ranges.
- The freeze (S19-W4-1) covers only atomize-book imports.
- CLAUDE.md does not use the union merge driver.
- A gotcha added mid-W4 is either missed by the map or lost in a conflict resolution (K11).

**Owner options:**
- **(a) Recommended.** Freeze all learn-hub CLAUDE.md edits from S21-W4a-1 to S21-W4b-1. New gotchas go to `docs/gotchas-inbox.md` and are merged after the freeze.
- **(b)** No freeze. Regenerate the map and diff the heading list against the W4-entry commit before S21-W4b-1 and at exit.
- **(c)** Accept the risk.

### F14. The W4 chapter re-run cannot run in the cloud

**Problem.**
- S19-W4-9 re-runs one chapter end to end. `Book/` and `raw book/` are gitignored and absent in the cloud checkout (checked), and no fixture chapter exists.
- The "pre-split baseline" it compares to is never recorded before W4.
- LLM drafting varies between runs, so "no regression in verdicts" is undefined for fresh drafts.
- Plan W4 row 15 carries no OWNER or Win tag.
- The architecture's article re-run (plan Q16) has the same problem: `Raw Article PDF/` exists only on Windows.

**Fix.**
- Add S19-W4-0 (before S19-W4-2, Windows, `BOOK_ROOT`): run `measure-loss.py`, `measure-depth.py` and `check-figures.py` on one imported chapter's existing notes. Save the JSON to `docs/rewrite/w4-chapter-baseline/`.
- S19-W4-9 (Win + OWNER):
  - re-run the same measurements through the new reference pointers;
  - run one fresh drafting pass;
  - compare gate verdicts (pass/fail per gate), not scores.
- Apply the same shape to the Q16 article re-run.

### F15. "Stop on any line drift" will stall execution

**Problem.**
- Plan §0 step 3 stops whenever "a quoted line or line number no longer matches".
- learn-hub gets about 10 commits a day, and specs anchor on line numbers. Examples:
  - S13-W4-1: CLAUDE.md 1685-1704;
  - S19: `SKILL.md:1051`.

**Fix.** "Locate by the quoted text. If it appears exactly once, proceed and record the new line in the commit message. Stop only if it is absent or ambiguous."

### F16. W3 ∥ W4 confounds the trigger evals

**Problem.**
- S12-W3-2, S12-W3-3 and S12-W3-4 run in a multi-repo session. There, learn-hub CLAUDE.md and the project-skill descriptions are in context.
- W4 changes both: the S21 diet and the S17/S18 descriptions.
- Run in parallel, the W3 before/after delta mixes both waves.

**Fix.** Add to plan §2: if W4 runs in parallel, hold W4 merges to learn-hub master from S12-W3-2 until S12-W3-4 ends. Alternatively, pin learn-hub to `wave-2` for those runs.

### F17. The S14-W1-1 audit is too broad and offers raw SQL deletes

**Problem.**
- `npm run vectors:check` "in DB, no vault file" counts every orphan. CLAUDE.md already records 13 from other causes.
- So the W1 owner step asks restore or delete for rows that source-to-vault may never have written.
- It offers "a manual `execute_sql` delete". S13's new rule (sync-vault-4) forbids that, because `progress` cascades.
- H17 closes when the skill is deleted; no DB change is needed.

**Fix.**
- S14-W1-1 becomes read-only: record the count and ids in the S14-W1-2 commit message.
- Restore only with `restore-vault-from-db.mjs --verify <topic-id>`, which writes files only.
- Deletion is out of W1. If wanted later, use app Hide → `npm run purge:hidden`.

### F19. Phase-3 files exist only in /tmp

**Problem.**
- The plan links `specs/…`, `coverage.md`, `phase3/interfaces.md`, `phase3/eval-format.md` and `phase3/measure.py` as repo paths. None exist in the repo.
- Specs cite `<wf3>/measure.py`, and S01 §4.4 cites `tmp/S01/check_evals.py`.
- The scratch dir is lost with the container.

**Fix.**
- Commit this layout: `docs/plugin-rewrite/{plan.md, coverage.md, specs/S01…S21, phase3/{interfaces.md, eval-format.md, spec-template.md, measure.py}}`.
- Replace `<wf3>/` with `docs/plugin-rewrite/phase3/` in the specs.
- Commit `check_evals.py` or drop the reference.
- Make it the first action before W0.

## Low

### F18. The ratchet wave gate cannot pass in some waves

**Problem.** "Fewer entries than at entry" has no entry file at W0. It fails in any wave that seeds new checks (S08-W3-1 seeds VAL-01…16 with `seed --new`) or closes none.

**Fix.** Gate = `ratchet verify` exits 0, and:
- for every `check_id` present at wave entry, the count is ≤ its entry count;
- entries for units the wave rewrote are gone.

### F20. coverage.md does not prove a closing step for each defect

**Problem.**
- The fix-step column reads "see spec" on 104 of 313 rows:
  - S05 26, S01 16, S06 16, S17 16, S07 12, S18 10, others 8.
- Three rows have no wave (plugin-creator-12, gridgeist-4, comprehensive-review-12). Plan §7 names a different three (validate.py-5, route.py-4, comprehensive-review-12).

**Fix.**
- Regenerate coverage.md with a parser that reads step ids from free-text cells.
- Plan §7 lists the no-step rows from the regenerated file.
- Fail generation if any row lacks both a step id and a stated reason.

### F21. The S21-W1-4 grep does not match its own sentence

**Problem.** The done-when greps "sole owner of this". The added sentence reads "sole owner of the sync → revalidate …". Correct work fails.

**Fix.** Grep for `sole owner of the sync`.

### F22. `claude plugin validate --strict` does not prove what done-when checks claim

**Problem.** A scratch plugin wrapping ingest-article (PyYAML `ScannerError`) and ingest-slides (1,150-char description) passes `--strict`. Only gross YAML breakage fails. Done-when checks that rely on it prove little. Example: S13-W1-6 "validator reports no error".

**Fix.**
- Use `measure.py` (`yaml_valid`, `description.chars`) or `skill-lint` for YAML and length checks.
- Keep `claude plugin validate` as a parse smoke only.

## Coverage of the four lenses

| Lens | Result |
|---|---|
| Goal-fit (arch §2–3 end state) | Every unit in §3 has a step. Missing or broken:<br>- learn-hub pre-commit (F8)<br>- learn-hub README (F12)<br>- W5 ratchet emptying (plan Q17)<br>- article re-run (Q16, F14)<br>- a working eval baseline and trigger method (F2, F4) |
| Completeness | Missing:<br>- trigger-lock commands (F7)<br>- doc upkeep (F12)<br>- baseline runs (F2)<br>- a Windows interpreter strategy (F9) |
| Verifiability | Gates that cannot run or pass here: F2, F3, F4, F14, F18, F21, F22 |
| Hidden assumptions | - cloud sandbox tools (F3)<br>- eval env allowlist (F3)<br>- `run_eval` semantics (F4)<br>- Windows Chromium, cmd.exe and python (F5, F9)<br>- container reuse (F10)<br>- concurrent CLAUDE.md edits (F13)<br>- book sources only on Windows (F14) |
