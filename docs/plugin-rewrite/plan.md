# Plugin rewrite: execution plan

Date: 2026-09-24. Repos: micky-psych-tools (MK) and learn-hub (LH).
Source of truth for design: [architecture.md](architecture.md). This plan orders the 285 change steps of the 21 specs into waves W0–W5. The critique pass of 2026-09-24 is recorded in `critique-log.md`.

Specs: [S01](specs/S01-alignment-core.md) · [S02](specs/S02-alignment-siblings.md) · [S03](specs/S03-evidence-core.md) · [S04](specs/S04-evidence-siblings.md) · [S05](specs/S05-visuals-core.md) · [S06](specs/S06-visuals-siblings.md) · [S07](specs/S07-vault-keeper.md) · [S08](specs/S08-plugin-creator.md) · [S09](specs/S09-firecrawl-gridgeist.md) · [S10](specs/S10-micky-repo.md) · [S11](specs/S11-delivery-environment.md) · [S12](specs/S12-eval-program.md) · [S13](specs/S13-sync-tail.md) · [S14](specs/S14-learn-hub-retirements.md) · [S15](specs/S15-digest-report-inbox.md) · [S16](specs/S16-ingest-visual-pk-plasma.md) · [S17](specs/S17-ingest-article-slides.md) · [S18](specs/S18-pdf-pipeline-verify.md) · [S19](specs/S19-atomize-book.md) · [S20](specs/S20-maintenance-skills.md) · [S21](specs/S21-learn-hub-claude-md-infra.md).
Also: [coverage.md](coverage.md), [phase3/interfaces.md](phase3/interfaces.md) (I01–I27), [phase3/eval-format.md](phase3/eval-format.md), [phase3/measure.py](phase3/measure.py). The package was committed to micky `docs/plugin-rewrite/` on 2026-09-24 (the §3 W0-entry package commit), so these paths resolve.

## 0. How to use this plan

**What it is.** The order in which an executor session applies the specs. The spec holds the detail of each step: files, change, commands, done-when, rollback. This plan holds the order, the gates and the owner actions. When the plan and a spec disagree on order, the plan wins. When they disagree on content, the spec wins, unless §8 lists a pending fix for it.

**Order.** W0 → W1 → W2 → {W3, W4} → W5. Inside a wave, run the rows of the §3 table top to bottom. A row may run earlier only if every step in its "Depends on" cell is merged. S15-W2-8 and S16-W2-8 are executor steps: read-only checks in a cloud session.

**Repo codes.** MK = micky-psych-tools. LH = learn-hub. env = the claude.ai/code cloud environment. Win = the owner's Windows machine. cloud = a multi-repo cloud session. both = one commit in each repo.

**How to execute one step.**
1. Check the wave entry conditions (§3) and the step's "Depends on" cell. Every dependency must be merged (on the wave branch, or on master under OQ7-a). `+ X (plan)` marks an order the plan adds where the spec omits it. Never start a wave before its entry conditions hold.
2. Work on one branch per wave per repo: `rewrite/w<n>`. Branch from the default branch after `git fetch` (learn-hub CLAUDE.md: other sessions push to the same remote). Keep the default checkout on master (K9): whatever is checked out there is what every session loads. The branch model is pending OQ7; under OQ7-a, use one short branch per spec block instead. Until S08's W3 plugin hook sets it, a cloud session runs `git -C /home/user/micky-psych-tools config core.hooksPath .githooks` before its first micky commit: a new cloud clone does not keep S10-W0-11's setting (critique C2-20; §8 Q29).
3. Open the spec at the step. Run its read-only commands first. Specs call `measure.py` as `$MICKY_TOOLS_DIR/docs/plugin-rewrite/phase3/measure.py` (committed at W0 entry). If a quoted line or line number no longer matches the file, locate the quoted text: if `grep -Fc '<text>' <file>` prints 1, use its new line and record the new line number in the commit message; stop and ask only when the text is gone or occurs more than once (critique F15, C2-09).
4. Make exactly the change the step names. Run step 5's checks before you commit; if they fail, apply the spec's rollback to the working tree. After a commit, the rollback is `git revert <sha>` (critique C2-28). One step = one commit. Two exceptions: S10-W3-1 + S10-W3-2 land as one PR of three commits, one per family (S10 commit shape, C2-14); S08-W3-1 lands as one PR of four commits (S08 commit shape, C2-13). Commit message: `<type>(<spec>): <step id> <summary>`, conventional commits, English.
5. Run the step's done-when commands, then the repo checks:
   - MK: `bash scripts/health.sh --fast` (from S10-W0-9 on; before it, `python3 scripts/validate.py`). From S08-W3-1 on, the validator is `python3 plugins/plugin-creator/scripts/validate.py --repo .`.
   - LH: `npm test`; from S21-W0-2 on also `npm run test:py && npm run check:skills`. From S21-W0-3 on, the learn-hub pre-commit hook runs skill-lint, `ratchet verify` and `triggers verify` on commits that touch `.claude/skills/` or `CLAUDE.md`; micky's `health.sh --fast` runs both verifies from S10-W0-9 on (critique F8).
6. Ratchet rule: `docs/rewrite/ratchet.json` may only shrink. A new violation fails the step. The only additions are first-time seeds by S10-W0-1b, S21-W0-2 and S08-W3-1 (`ratchet seed --new`). When a step fixes a ratcheted entry, remove the entry in the same commit (`rewrite_gate.py ratchet close`; LH `node scripts/rewrite-gate.mjs ratchet close`).
7. Trigger lock rule: never drop or reword a phrase in `docs/rewrite/triggers.lock.json` silently. A phrase goes only through `triggers remove --phrase "<p>" --skill <s> --reason "<r>" --write` (a deleted or merged skill: `triggers remove --skill <s> --reason "<r>" --write`), in the same commit as the description edit, followed by `triggers verify`. MK runs `python3 scripts/rewrite_gate.py`, LH runs `node scripts/rewrite-gate.mjs`. §5's lock table names the step and command for every phrase a spec's §6 marks removed, narrowed or moved to another skill (critique F7).
8. CHANGELOG: LH — an entry under `## [Unreleased]` for every step that changes behaviour or tooling, plus tests for new logic (learn-hub CLAUDE.md rule). MK — the touched plugin's `CHANGELOG.md` (release steps write it through `bump.py --write` or `release.py --write`). MK repo-level tooling: `docs/rewrite/CHANGELOG.md`, created by S10-W0-8 (OQ16, assumed option (a)). LH also updates `README.md` (script table) and `CLAUDE.md` in the same commit when a step changes what they describe (learn-hub CLAUDE.md, Documentation upkeep; critique F12).
9. h-coverage: micky's `docs/rewrite/h-coverage.md` is canonical. A step that verifies a closure records its evidence in `docs/rewrite/baseline.md` under `## Owner records`. The wave's tag step (S12-W<n>-T) closes that wave's rows with `rewrite_gate.py h-coverage close --id Hnn --wave Wn --write` in one commit, then copies the file byte for byte to learn-hub (S12 §2.3; critique P33, C2-26).
10. Never run: `claude plugin eval` beyond the smoke and release commands the plan names, `npm run sync` or `sync:apply` outside an OWNER step (`apply-sync.mjs --preflight-only` is allowed: it exits before any Supabase client exists), anything that writes to Supabase, any edit to a claude.ai-synced skill. Eval runs happen only in the cloud environment (setup step 4 installs bubblewrap and socat) or under WSL2: native Windows has no sandbox backend for Bash-granted cases (critique C2-02).

**Stop and ask the owner** when:
- the row is marked OWNER;
- a done-when fails and the spec's rollback does not restore a green state;
- a step would write to the live database or edit a synced skill;
- a §1 question or a §8 item listed for this wave is still open;
- the change would reach outside the step's named files (K16).

## 1. Owner decisions

Every OD takes the architecture's recommended option. The executor does not start a wave until the owner has confirmed the ODs it needs.

| OD | Assumed option | Needed by |
|---|---|---|
| OD1 | (a) `CLAUDE_CODE_PLUGIN_DIRS` on the cloud environment, absolute paths | W0 entry; re-ask if check a = no |
| OD2 | (a) Windows user env var; marketplace copies uninstalled | W0 entry (provisional), W3 entry (S11-W3-2) |
| OD3 | (a) merge into families alignment, evidence, visuals | W3 entry (S10-W3-2) |
| OD4 | (a) keep micky `vault/` as fallback sink; revisit at W5 | W2 entry; W5 |
| OD5 | (a) inbox only; publish on "digest" | W2 entry |
| OD6 | (a) git-tracked `micky/state/` | W3 entry (S01-W3-4, S04-W3-1) |
| OD7 | (a) rename micky skill to `lit-watch`, keep `/digest` | W3 entry (S04-W3-3) |
| OD8 | (a) owner edits synced `daily-random-review`; CR gets a Not-for | W2 (before S04-W2-4) |
| OD9 | (a) short verbs as dmi alias skills | W3 entry (S10-W3-2); W2 for `/pk-animation`, `/vectors` |
| OD10 | (a) mixed user-only list | W2 (S20), W3 entry |
| OD11 | (b) staged CLAUDE.md restructure | W4 entry |
| OD12 | (a) slim firecrawl router, `defaultEnabled: false` | W3 entry (S09-W3-1) |
| OD13 | (a) no claude.ai builds | W5 |
| OD14 | (a) smoke per wave; two-arm release at W3 and W5 exits | W0 entry |

**Owner questions** (answer by the wave shown). OQ1–OQ6 come from the specs' §8; OQ7–OQ16 come from the critique pass (`critique-log.md`) and list their options, recommended first.

| # | Question | Source | Answer by |
|---|---|---|---|
| OQ1 | LICENSE text for the backfill: MIT, owner "Thanawat Suharit (Micky)", 2026? Default MIT. | S10 §8.5 | W0, before S10-W0-8 |
| OQ2 | Extra eval tools (`--allow-tools`) pass through `eval.sh -- …` per case, not as a fixed always-on set? | S12 §8.6 | W0, before S12-W0-3 |
| OQ3 | Eval budget: the `EVAL_BUDGET` / `--max-cost-usd` value (OD14) and the ≤ USD 0.50 check-d run | S11-W0-9, OD14 | W0, before S11-W0-9 |
| OQ4 | Enablement reading: "HIGH defects due by that wave", with named exceptions logged (vault-keeper at V2 with H10/H11 split; pubmed at V3 with H45 open; four alignment/PPD plugins at V6) | S11 §8.4 | W1 exit (S11-W1-1); re-confirm at S11-W2-2, S11-W3-1 |
| OQ5 | Per orphan row found by the source-to-vault audit: restore (`restore-vault-from-db.mjs --verify`) or leave. No delete in W1 (critique F17). | S14-W1-1 | W1 |
| OQ6 | firecrawl: keep `defaultEnabled: false` plus a setup-script enable block, or drop the flag | S09 §8.6, S11 §8.1 | W3 entry, before S09-W3-1 |
| OQ7 | Branch model (the wave branch conflicts with mid-wave cloud enablement). **(a) Recommended:** one short branch per spec block (the rows up to a release or a V-step dependency), merged to master when green; a V step or Windows refresh runs only after `git merge-base --is-ancestor <dep-sha> origin/master` holds for each dependency; the wave tag marks the last merge; rollback reverts the listed PR merges, newest first; at W1 and W2, learn-hub blocks merge before the micky blocks that write into them. **(b)** Keep one branch per wave; merge before the exit gates; move every V step, Windows step and S13-W1-10 after that merge. **(c)** Point cloud sessions at `rewrite/w<n>` (conflicts with K9). | critique F1, C2-03 | W0 entry |
| OQ8 | Eval baseline cadence. **(a) Recommended:** smoke baselines whenever cases change (S12-W0-8 records W0; a step that adds cases runs its smoke command with `--against pre-rewrite` for them), release baselines only at W3 and W5 (`--against pre-rewrite`). The specs implement (a). **(b)** Absolute pass thresholds per case instead of "≥ baseline". **(c)** Full baselines every wave. | critique F2 | W0, before S12-W0-8 |
| OQ9 | Other sessions edit learn-hub CLAUDE.md during W4. **(a) Recommended:** freeze its `## Gotchas` and `## Pages` from S21-W4a-1 to S21-W4b-1; new gotchas go to `docs/gotchas-inbox.md` and merge after. **(b)** No freeze: S21-W4a-1 builds the map from the W4-entry file and `move-blocks --check` compares against that commit (the specs do this under both options). **(c)** Accept the risk. | critique F13, C2-09 | W4 entry |
| OQ10 | Unfixed alignment plugins load in the cloud for all of W3. **(a) Recommended:** at W3 entry set V5' = V5 plus `/home/user/micky-psych-tools/plugins/{alignment,evidence,visuals}` (under OQ7-a, add each family once its rewrite is on master); switch to V6 with the last merge; drop S10-W3-1's dependency on S11-W3-1 and the OQ4 exception for the four plugins. **(b)** Keep V6 at W3 entry with the OQ4 exception. | critique C2-12 | W3 entry, before S11-W3-1 |
| OQ11 | Eval run counts (about 1,140 live-trigger runs, 480 + 900 release runs, plus the `--against` arm). **(a) Recommended:** run each trigger query once and re-run 3 times only the queries whose outcome flips; release `--runs 3` for gate skills and report writers, `--runs 1` for the rest; OQ3 sets one budget per cost point (smoke run, release run, live pass). **(b)** Keep the architecture's counts and budget them all in OQ3. | critique C2-17 | W0, with OQ3 |
| OQ12 | When Windows loads plugins in place. **(a) Recommended:** at W1 entry, after check g = yes: set the Windows variable, uninstall the marketplace copies, drop the 12 W1/W2 release steps, S11-W1-2 and S11-W2-5; each step still writes its CHANGELOG entry under `## Unreleased`; `release.py` sets versions once at W3; Windows checkouts stay on master and rewrite work runs in a worktree (K9). **(b)** Keep OD2-a timing: switch at W3 (S11-W3-2). | critique C2-18 | W1 entry |
| OQ13 | The visual audit is built twice (micky `check-html.mjs` port and learn-hub `audit:visual`). **(a) Recommended:** `check-html.mjs` delegates to `audit:visual` and keeps a static subset of at most 60 lines (doctype, `lang`, color-scheme, `min-height:100dvh`, no `prefers-color-scheme:dark`, no external URL), returning `incomplete` without learn-hub; drop the render port, the parity fixture, the VAL parity check and S05-W2-2's copies; code-explainer keeps its own static check. **(b)** Keep the architecture's port and parity fixture. | critique C2-19 | W2 entry, before S05-W2-1 |
| OQ14 | When the learn-hub CLAUDE.md stage (b) diet runs. **(a) Recommended:** right after W0 check e = yes, before W1 (S21-W4a-1, S21-W4a-4 and S21-W4b-1 with OQ9's answer); stage (a) stays in W4; saves about 35k tokens per session and brings the W3 trigger runs closer to the final context. **(b)** Keep both stages in W4. | critique C2-23 | W0 exit |
| OQ15 | vault-keeper scripts for a vault of 16 files. **(a) Recommended:** cut `vault_index.py` (state the dangling-versus-broken link rule in prose); defer `drain_plan.py` to W5 and build it only if S07-W5-1 keeps the vault; in W2, copy the 7 artifacts to `research-notes/` once with the owner watching and keep the W1 no-delete stopgap; H10b and H11b close on the stopgap plus the copy. **(b)** Keep S07-W2-3 and S07-W2-4 as specified. | critique C2-25 | W2 entry, before S07-W2-3 |
| OQ16 | Home of micky repo-level tooling CHANGELOG entries (was §8 Q11). **(a) Recommended:** `docs/rewrite/CHANGELOG.md`, created by S10-W0-8 (S10 assumes (a)). **(b)** A repo-root `CHANGELOG.md`. **(c)** Commit messages only. | planner P-32 | W0, before S10-W0-8 |

## 2. Critical path and effort

Critical path: W0 → W1 → W2 → W3 → W5. W4 is off the critical path when it runs in parallel with W3.

- **W3 ∥ W4.** W4 may start at W2 exit (architecture §10). No W4 step depends on a W3 step (checked). W3 touches only MK plus the env; W4 touches only LH. Shared: S12 live-trigger runs (separate families), the cloud session, owner time. Default is sequential; run in parallel only if the owner wants to. In parallel: hold W4 merges to learn-hub master from S12-W3-2 until S12-W3-4 ends, because the W3 trigger runs read learn-hub CLAUDE.md and the project-skill descriptions (critique F16); run S12-W4-2 and S12-W4-3 with micky checked out at tag `wave-2`, or both before the W3 merge (C2-31).
- W4 needs an atomize-book import freeze (S19-W4-1) from the start of S19-W4-2 until S19-W4-9 passes. The W4 table lists S19-W4-2 … S19-W4-9 back to back (critique C2-27); only S19-W4-9 needs Windows.
- Session type (critique C2-24): a row whose Repo is MK, with no V step and no cross-repo check, can run in a micky-only session (with `LEARN_HUB_DIR` unset, the cross-repo checks warn). Rows marked LH, both, env or cloud, and every V step, need a multi-repo session. Win rows run on the owner's Windows machine.
- W5 waits 2–4 weeks of use after W3 (S09-W5-1).

| Wave | Steps | OWNER steps | Executor sessions (estimate) |
|---|---|---|---|
| W0 | 46 | 8 | 3: MK tooling; LH tooling + seeds; checklist + smoke baseline |
| W1 | 68 | 6 | 4: sync tail; ingest/pdf/atomize text; micky fixes; exit |
| W2 | 63 | 9 | 5: LH consumers; producers; renderers; vault-keeper + forks; cloud |
| W3 | 67 | 4 | 6: skeleton; alignment; evidence; visuals; plugin-creator + firecrawl; diet + exit |
| W4 | 33 | 6 | 4: gotcha moves; atomize split; ingest/pdf/verify; Windows baselines and re-runs |
| W5 | 8 | 3 | 1 |
| Total | 285 | 36 | about 23 |

**Eval cost points (OD14).** Smoke runs every wave: free graders, 1 run, `--ablation none`, budget capped by OQ3. The two paid points are the two-arm release runs: **S12-W3-5** (W3 exit, 6 plugins) and **S12-W5-1** (W5, all plugins and project skills). A full two-arm pass is about 700 agent runs (EVL-27). Live trigger runs (S12-W3-2/-3, S12-W4-2/-3) and routing smokes (S12-W3-4, S12-W5-2) add session runs but no two-arm cost. The `--against pre-rewrite` baseline arm (critique C2-07) doubles each release pass, and S12-W0-8 adds one smoke pass at W0. Run counts are pending OQ11.

## 3. Waves

**Standard exit gates (every wave, architecture §10).** Each is a command or a record:

| Gate | Command / record | Expected |
|---|---|---|
| MK health | `bash scripts/health.sh` | prints `health: OK` |
| LH tests | `npm test && npm run test:py && npm run check:skills` | exit 0 |
| Cross-repo | `validate.py --cross-repo "$LEARN_HUB_DIR"` (from W3; at W2 the two contract checks in the W2 table are the gate, §8 Q12) | exit 0 |
| Smoke | the spec's §4.4 smoke command, verbatim (it carries the `--allow-tools` grants; both runners pass `--scaffold`), per touched unit | seeded units: each case at or above its `## W0 smoke` rate in `baseline.md`; unseeded units: every grader passes (critique C2-07, F3; OQ8) |
| Ratchet | `rewrite_gate.py ratchet verify` (MK) / `node scripts/rewrite-gate.mjs ratchet verify` (LH) | exit 0; no check id's count above its count at wave entry, except check ids first seeded in this wave by S10-W0-1b, S21-W0-2 or S08-W3-1; no entry left for a unit the wave rewrote (critique F18, C2-15) |
| Trigger lock | `… triggers verify` in both repos | exit 0 |
| Delivery log | `python3 scripts/delivery_log.py check --strict` | exit 0 |
| CHANGELOG | one entry per touched repo (§0 rule 8) | present |
| Pipeline | report → vault → learn-hub no worse than at entry | owner note |
| h-coverage | `grep -E '^- \[ \] H.*wave: W<n>$' docs/rewrite/h-coverage.md` (split rows H07a/b, H10a/b, H11a/b, critique C2-16) | no output |
| Tag | `git ls-remote origin wave-<n>` | one line per repo |

### W0 — Ground truth and safety net

**Entry.** Both repos clean on the default branch. OD1, OD2 (provisional), OD14, OQ1, OQ2, OQ3, OQ7, OQ8, OQ11, OQ16 answered. **Done 2026-09-24:** the plan package is committed to micky `docs/plugin-rewrite/`: `plan.md`, `critique-log.md`, `coverage.md`, `specs/S01…S21`, `phase3/{interfaces.md, eval-format.md, spec-template.md, measure.py}` (critique F19). `coverage.md` was regenerated from the reconciled specs by `phase3/gen_coverage.py` (313 of 313 defects mapped, 312 with a step id; the one without, comprehensive-review-12, states its reason in S04 §1.3) (F20, P-34). Re-run it after any spec edit: `python3 phase3/gen_coverage.py evidence/defect-index.txt coverage.md` from `docs/plugin-rewrite/`. S12-W0-0 is the first step (tag `pre-rewrite`).

| # | Step | Spec | Repo | What | Depends on | OWNER |
|---|---|---|---|---|---|---|
| 1 | S12-W0-0 | S12 | both | Tag `pre-rewrite` in both repos | — | yes |
| 2 | S10-W0-1 | S10 | MK | validate.py: guarded loads, counted checks, CRLF YAML, stdio MCP, no floor (H13) | — |  |
| 3 | S12-W0-1 | S12 | MK | `rewrite_gate.py`; ratchet, trigger lock, h-coverage (micky) | S10-W0-1 |  |
| 4 | S10-W0-1b | S10 | MK | Seed the `yaml-parse` ratchet entry | S10-W0-1, S12-W0-1 |  |
| 5 | S10-W0-3 | S10 | MK | Strip every `version` from marketplace.json | — |  |
| 6 | S10-W0-2 | S10 | MK | bump.py: plugin.json only, dry run, `--write`, CHANGELOG | S10-W0-1, S10-W0-1b, S10-W0-3 |  |
| 7 | S10-W0-4 | S10 | MK | route.py: argparse, no versions | — |  |
| 8 | S10-W0-7 | S10 | MK | `.gitignore` | — |  |
| 9 | S10-W0-8 | S10 | MK | Per-plugin README/CHANGELOG/LICENSE backfill; `docs/rewrite/CHANGELOG.md` (OQ16) | — |  |
| 10 | S10-W0-9 | S10 | MK | `scripts/health.sh` (`--fast` runs ratchet and lock verify) | S10-W0-1, S12-W0-1 |  |
| 11 | S10-W0-10 | S10 | MK | `.githooks/pre-commit` | S10-W0-9 |  |
| 12 | S10-W0-11 | S10 | MK | `git config core.hooksPath .githooks` | — | yes |
| 13 | S10-W0-5 | S10 | MK | CLAUDE.md: version rule, mandates demoted, layout | S10-W0-1…4 |  |
| 14 | S10-W0-6 | S10 | MK | README fixes (`--strict`, private repo) | S10-W0-1, S10-W0-7 |  |
| 15 | S12-W0-3 | S12 | MK | `scripts/eval.sh` (smoke/release, `--` passthrough) | S12-W0-1 |  |
| 16 | S11-W0-1 | S11 | MK | `delivery_log.py` + tests | — |  |
| 17 | S11-W0-2 | S11 | MK | `delivery-log.md` + `cloud-setup.sh` v1 | S11-W0-1 |  |
| 18 | S11-W0-3 | S11 | MK | health.sh runs the log checker | S10-W0-9, S11-W0-2 |  |
| 19 | S21-W0-1 | S21 | LH | `skill-lint.mjs` + tests (exit 1 on today's YAML and length failures) | — |  |
| 20 | S12-W0-2 | S12 | LH | `rewrite-gate.mjs`; ratchet, lock, h-coverage (learn-hub) | — |  |
| 21 | S21-W0-2 | S21 | LH | package.json `test:py`, `check:skills` (node scripts); seed the LH ratchet | S21-W0-1, S12-W0-2 |  |
| 22 | S21-W0-3 | S21 | LH | `.githooks/pre-commit`: skill-lint, ratchet and lock verify | S21-W0-2, S12-W0-2 |  |
| 23 | S12-W0-4 | S12 | LH | `scripts/eval-project-skill.sh` | S12-W0-2 |  |
| 24 | S12-W0-7 | S12 | both | `baseline.md` W0 section, both repos | S12-W0-1, S12-W0-2 |  |
| 25 | S11-W0-4 | S11 | LH | cloud-env-setup.md §3C | — |  |
| 26 | S11-W0-6 | S11 | LH | Rules probe branch `w0/rules-probe` (never merged) | — |  |
| 27 | S11-W0-5 | S11 | env+MK | Configure cloud env vars, setup script (installs bubblewrap, socat), V0 | S11-W0-2 | yes |
| 28 | S11-W0-7 | S11 | env+MK | Checks a, b, e, f, h (+ U7) | S11-W0-5, S11-W0-6 | yes |
| 29 | S11-W0-8 | S11 | MK | Check c (many-to-one `renames`) | S11-W0-2 |  |
| 30 | S11-W0-9 | S11 | MK | Check d (`claude plugin eval` enabled) + Bash-and-scaffold canary | S11-W0-2 | approve cost |
| 31 | S12-W0-6 | S12 | both | Record eval availability; check i (`claude -p` load set) | S11-W0-9 | yes |
| 32 | S11-W0-10 | S11 | Win+MK | Windows check g; Windows variables; MEMORY:11 | S11-W0-2 | yes |
| 33 | S03-W0-1 | S03 | MK | Smoke seeds: pubmed-research-note | S12-W0-3 |  |
| 34 | S04-W0-1 | S04 | MK | Smoke seeds: psych-paper-digest | S12-W0-3 |  |
| 35 | S04-W0-2 | S04 | MK | Smoke seeds: comprehensive-review | S12-W0-3 |  |
| 36 | S06-W0-1 | S06 | MK | Smoke seeds: clinical-infographic | S12-W0-3 |  |
| 37 | S07-W0-1 | S07 | MK | Smoke seeds: vault-keeper, empty-vault | S12-W0-3 |  |
| 38 | S08-W0-1 | S08 | MK | Smoke seeds: plugin-creator, refine-plugin | S12-W0-3 |  |
| 39 | S09-W0-1 | S09 | MK | Smoke seeds: firecrawl | S12-W0-3 |  |
| 40 | S13-W0-1 | S13 | LH | Smoke seeds: sync-vault | S12-W0-4 |  |
| 41 | S17-W0-1 | S17 | LH | Smoke seeds: ingest-article | S12-W0-4 |  |
| 42 | S18-W0-1 | S18 | LH | Smoke seeds: pdf-pipeline | S12-W0-4 |  |
| 43 | S12-W0-5 | S12 | both | Seed checklist: ≥3 smoke cases per unit | S03-W0-1, S04-W0-1, S04-W0-2, S06-W0-1, S07-W0-1, S08-W0-1, S09-W0-1, S13-W0-1, S17-W0-1, S18-W0-1 |  |
| 44 | S12-W0-8 | S12 | both | Record the W0 smoke baseline (`## W0 smoke`, 10 units) | S12-W0-5, S12-W0-6, S11-W0-9 |  |
| 45 | S11-W0-11 | S11 | env+MK | W0 exit: probe removed, V0→V1, setup v2 | S11-W0-7…10 | yes |
| 46 | S12-W0-T | S12 | both | Tag `wave-0` | all W0 | yes |

Notes: S10-W0-1's done-when is exit 1 with exactly one `yaml-error` FAIL (intent-lock); S10-W0-1b seeds the ratchet entry and turns it into one WARN. S21-W0-1's done-when is exit 1 listing today's learn-hub YAML and length failures; S21-W0-2 seeds them. S09-W0-1 seeds firecrawl. The S07 owner check "is `userConfig.learn_hub_root` prompted" runs inside S11-W0-7.

**Exit gates** (plus the standard gates; cross-repo not yet):

| Check | Command | Expected |
|---|---|---|
| Validator | `python3 scripts/validate.py` | exit 0; one `WARN` for intent-lock YAML; no length-floor line |
| Catalog | `python3 -c "import json;d=json.load(open('.claude-plugin/marketplace.json'));assert 'version' not in d and all('version' not in p for p in d['plugins'])"` | no error |
| bump dry run | `python3 scripts/bump.py pubmed-research-note patch; git diff --stat` | empty diff |
| Checklist | `python3 scripts/delivery_log.py check --strict`; `… check --json` | exit 0; rows a–h each `yes` or `no` |
| h-coverage | `grep -c '^- \[' docs/rewrite/h-coverage.md` (both repos) | 52 (H07, H10, H11 split in two), identical files |
| Eval canary | S11-W0-9's `$E/w0d2.json` (Bash grant + scaffold) | both `file_exists` graders pass |
| Smoke baseline | `grep -c '^## W0 smoke' docs/rewrite/baseline.md` (both repos) | 1 each; the 10 seeded units listed across the two repos |
| LH pre-commit | `test -x .githooks/pre-commit && node scripts/pre-commit.mjs` (LH) | exit 0 |
| Seeds | S12-W0-5 command per unit | ≥3 smoke cases for each of 10 units |
| Baseline | `grep -c '^## W0' docs/rewrite/baseline.md` (both repos) | 1 |
| Cloud (new session) | `echo "$CLAUDE_CODE_PLUGIN_DIRS"`; `head -n1 /var/log/cloud-setup.log`; `python3 -c "import fitz, pypdf, pdfplumber"`; `firecrawl --version` | `/home/user/micky-psych-tools/plugins/gridgeist`; `setup_version=2`; exit 0; `1.24.4` |
| H13 | h-coverage row H13 | closed |

If check a = no: skip every later cloud step, stay at V1, re-ask OD1 before W1 exit.

**Rollback.** Revert the W0 merges; set the cloud variables back per the delivery log. Only tooling and data files changed.

**`CLAUDE_CODE_PLUGIN_DIRS`.** Cloud: unset → V0 (gridgeist + probe) at S11-W0-5 → V1 (`/home/user/micky-psych-tools/plugins/gridgeist`) at S11-W0-11. Windows: unchanged (marketplace install).

### W1 — Stop active harm (learn-hub first)

**Entry.** W0 exit gates green; tag `wave-0` pushed.

| # | Step | Spec | Repo | What | Depends on | OWNER |
|---|---|---|---|---|---|---|
| 1 | S13-W1-1 | S13 | LH | `readiness.mjs` + tests (bundled-browser and `python` fallbacks) | — |  |
| 2 | S13-W1-2 | S13 | LH | `scripts/ready.mjs` | S13-W1-1 |  |
| 3 | S13-W1-3 | S13 | LH | `sync-preflight.mjs` + tests | S13-W1-1 |  |
| 4 | S13-W1-4 | S13 | LH | apply-sync runs the preflight (exit 2 on refusal; `--preflight-only`) | S13-W1-3 |  |
| 5 | S13-W1-5 | S13 | LH | package.json `sync:preflight` | S13-W1-3, S21-W0-2 |  |
| 6 | S13-W1-6 | S13 | LH | sync-vault SKILL.md rewrite (H34, H35) | S13-W1-2, S13-W1-3, S13-W1-5 |  |
| 7 | S13-W1-7 | S13 | LH | Remove PreToolUse gates + gate scripts; README, CLAUDE.md sentences | S13-W1-4 |  |
| 8 | S13-W1-8 | S13 | LH | session-start.sh root, done-marker, ready line; .gitignore | — |  |
| 9 | S13-W1-9 | S13 | LH | sync-vault eval cases (extend seeds) | S13-W0-1, S13-W1-6 |  |
| 10 | S13-W1-11 | S13 | LH | cloud-env-setup.md: `npm run sync:preflight` | S13-W1-5 |  |
| 11 | S17-W1-1 | S17 | LH | .gitignore `/Raw Article PDF/` | S13-W1-8 |  |
| 12 | S17-W1-2 | S17 | LH | ingest-article description (YAML) | — |  |
| 13 | S17-W1-3 | S17 | LH | ingest-article preflight + survey-and-ask inbox (H25) | S13-W1-2, S17-W1-1 |  |
| 14 | S17-W1-4 | S17 | LH | Seed-count text | — |  |
| 15 | S17-W1-5 | S17 | LH | Mermaid check → `check-mermaid.mjs` | — |  |
| 16 | S17-W1-6 | S17 | LH | Sync section → sync-vault sentence | S13-W1-6, S17-W1-5 |  |
| 17 | S17-W1-7 | S17 | LH | figures-and-loss.md flags; drop §5b (H26) | — |  |
| 18 | S17-W1-8 | S17 | LH | ingest-slides description (H28) | — |  |
| 19 | S17-W1-9 | S17 | LH | ingest-slides script paths + preflight (H27) | S13-W1-2 |  |
| 20 | S17-W1-10 | S17 | LH | extract_pdf / render_slides text | — |  |
| 21 | S17-W1-11 | S17 | LH | ingest-slides figure + loss gates; sync sentence | S13-W1-6 |  |
| 22 | S17-W1-12 | S17 | LH | ingest-article / ingest-slides eval cases | S17-W0-1, S17-W1-2, S17-W1-8 |  |
| 23 | S18-W1-1 | S18 | LH | routing.md: decks → ingest-slides (H32) | — |  |
| 24 | S18-W1-2 | S18 | LH | pdf-pipeline slides branch (H32) | S17-W1-8 |  |
| 25 | S18-W1-3 | S18 | LH | Preflight = `ready.mjs` | S13-W1-2 |  |
| 26 | S18-W1-4 | S18 | LH | Sync section → sync-vault (H33) | S13-W1-6 |  |
| 27 | S18-W1-5 | S18 | LH | preflight-and-apply.md: no manual SQL path | S13-W1-6 |  |
| 28 | S18-W1-6 | S18 | LH | surface-checklist.md fixes | S13-W1-6 |  |
| 29 | S18-W1-7 | S18 | LH | routing.md find-based glob | — |  |
| 30 | S18-W1-8 | S18 | LH | pdf-pipeline description | — |  |
| 31 | S18-W1-9 | S18 | LH | pdf-pipeline eval cases | S18-W1-1…8, S18-W0-1 |  |
| 32 | S19-W1-1 | S19 | LH | One chapter-reference rule (H21) | — |  |
| 33 | S19-W1-2 | S19 | LH | §9 → sync-vault sentence (H22) | S13-W1-6 |  |
| 34 | S19-W1-3 | S19 | LH | Four drafting rules (H23) | — |  |
| 35 | S19-W1-4 | S19 | LH | Id resolution, glob, check-mermaid; package.json | S13-W1-5 |  |
| 36 | S19-W1-5 | S19 | LH | Scale-guidance text | — |  |
| 37 | S19-W1-6 | S19 | LH | Point at `check-manifest.py --notes` | — |  |
| 38 | S19-W1-7 | S19 | LH | `ready.mjs` preflight | S13-W1-2 |  |
| 39 | S19-W1-8 | S19 | LH | Description + stale counts | — |  |
| 40 | S16-W1-1 | S16 | LH | ingest-infographic YAML, H30, `/visualization` | — |  |
| 41 | S16-W1-2 | S16 | LH | ingest-animation YAML | — |  |
| 42 | S05-W1-1 | S05 | LH | learn-hub concept-animation copy YAML (H43) | — |  |
| 43 | S20-W1-1 | S20 | LH | vault-coverage `BOOK_ROOT`, source map, stale text | — |  |
| 44 | S20-W1-1b | S20 | LH | Backfill `coverage-sources.json` (Windows, BOOK_ROOT) | S20-W1-1 | yes |
| 45 | S14-W1-1 | S14 | LH | Audit source-to-vault orphan rows (read-only); restore or leave | — | yes |
| 46 | S14-W1-2 | S14 | LH | Delete `plugins/source-to-vault` (H17–H20) | S14-W1-1 |  |
| 47 | S21-W1-1 | S21 | LH | CLAUDE.md figure disposition list | — |  |
| 48 | S21-W1-4 | S21 | LH | CLAUDE.md: sync-vault owner + delivery sentences | — |  |
| 49 | S07-W1-1 | S07 | MK | `sink.py` + `vault/.vault-id`; manifest fields | S10-W0-8 |  |
| 50 | S07-W1-2 | S07 | MK | empty-vault stopgap: dmi, marker→ask, hold assets | S07-W1-1 |  |
| 51 | S07-W1-3 | S07 | MK | vault-keeper Step 0 → `sink.py resolve` (H08, H09) | S07-W1-1 |  |
| 52 | S07-W1-4 | S07 | MK | Release vault-keeper | S07-W1-1…3 |  |
| 53 | S08-W1-1 | S08 | MK | plugin-creator root guard, no walk-up (H07) | — |  |
| 54 | S08-W1-2 | S08 | MK | Release plugin-creator | S08-W1-1 |  |
| 55 | S04-W1-1 | S04 | MK | PPD: edat, retstart, CT.gov RANGE, MCP resolution (H46, H47) | — |  |
| 56 | S04-W1-2 | S04 | MK | PPD README cron claim | — |  |
| 57 | S04-W1-3 | S04 | MK | Release psych-paper-digest | S04-W1-1, S04-W1-2 |  |
| 58 | S06-W1-1 | S06 | MK | CI light-lock, strip, contrast, 12 px (H36, H37) | — |  |
| 59 | S06-W1-2 | S06 | MK | code-explainer dead pointers (H42) | — |  |
| 60 | S06-W1-3 | S06 | MK | CI / CE eval cases | — |  |
| 61 | S06-W1-4 | S06 | MK | Validate | S06-W1-1, S06-W1-2 |  |
| 62 | S06-W1-5 | S06 | MK | Release CI, CE | S06-W1-1…3 |  |
| 63 | S09-W1-1 | S09 | MK | firecrawl vendor refresh (H12) | — |  |
| 64 | S09-W1-2 | S09 | MK | Release firecrawl | S09-W1-1 |  |
| 65 | S13-W1-10 | S13 | LH | Live sync of a trivial edit; diagrams count kept | S13-W1-1…9, S11-W0-11 | yes |
| 66 | S11-W1-1 | S11 | env+MK | Cloud V1→V2: vault-keeper, firecrawl, plugin-creator | S07-W0-1, S07-W1-3, S07-W1-4, S08-W0-1, S08-W1-2, S09-W0-1, S09-W1-2, S11-W0-11 | yes |
| 67 | S11-W1-2 | S11 | Win+MK | Windows: refresh installs; `ready.mjs` Chromium check | S04-W1-3, S06-W1-5, S07-W1-4, S08-W1-2, S09-W1-2, S13-W1-1, S13-W1-2 | yes |
| 68 | S12-W1-T | S12 | both | Tag `wave-1` | all W1 | yes |

**Exit gates:**

| Check | Command | Expected |
|---|---|---|
| Sync refuses unready | `PUPPETEER_EXECUTABLE_PATH=/nonexistent node scripts/apply-sync.mjs --preflight-only; echo $?`; `npx vitest run scripts/apply-sync.test.mjs` (LH) | `2`, no `Upserted` line; exit 0 (critique C2-04, F6) |
| No PreToolUse gates | `python3 -m json.tool .claude/settings.json \| grep -c PreToolUse` | `0` |
| Readiness | `node scripts/ready.mjs --json` | 5 checks |
| sync-vault picks preflight | `bash scripts/eval-project-skill.sh sync-vault --smoke -- --allow-tools Bash` (S13 §4.4; case `sync-preflight-before-apply` is smoke-tagged) | pass |
| Bare ingest-article asks | `scripts/eval-project-skill.sh ingest-article --smoke -- --allow-tools "Bash(ls *),Bash(find *)"` (S17 §4.4; case `inbox-survey-and-ask` is smoke-tagged); `grep -n 'C:\\Users\\User' .claude/skills/ingest-article/SKILL.md` | pass, no deletion; no output |
| vault-keeper marker | `python3 -m unittest plugins/vault-keeper/scripts/test_sink.py`; `grep -c '\.\./\.\./vault' plugins/vault-keeper/skills/vault-keeper/SKILL.md` | OK; `0` |
| Assets held | `grep -c 'Desktop.Learn\|digest-report' plugins/vault-keeper/skills/empty-vault/SKILL.md` | `0` |
| CI light-lock | `grep -c 'prefers-color-scheme:dark'` on the template and the example; S06-W1-1's `auditInfographicResponsive` command | `0`; `[]` |
| source-to-vault gone | `test ! -d plugins/source-to-vault` (LH) | true |
| Live sync | S13-W1-10 record in LH `baseline.md` `## Owner records` | `EXIT=0`, `Upserted …`, diagrams count not lower |
| Cloud V2 | `delivery_log.py live --env cloud:<id> --expect gridgeist,vault-keeper,firecrawl,plugin-creator` | `"ok": true` |
| HIGH rows | h-coverage W1 rows (26) + H07a, H10a, H11a | closed |

**Rollback.** Revert the per-repo W1 merge (or the W1 PR merges, OQ7-a). This restores the settings.json gates and the old skills. Set the cloud value back to V1. A revert does not undo Supabase writes: S13-W1-10's vault-note commit stays on learn-hub master because its row is live; revert only the tooling (critique C2-21).

**`CLAUDE_CODE_PLUGIN_DIRS`.** Cloud: V1 → V2 (adds vault-keeper, firecrawl, plugin-creator) at S11-W1-1. Windows: installs refreshed (S11-W1-2), variable unchanged.

### W2 — Reconnect the pipeline (consumers, then producers)

**Entry.** W1 exit gates green; OD4, OD5, OD8, OQ4, OQ13, OQ15 answered; tag `wave-1` pushed. Order inside the wave: learn-hub consumers → micky producers → renderers → vault-keeper → forks → cloud.

| # | Step | Spec | Repo | What | Depends on | OWNER |
|---|---|---|---|---|---|---|
| 1 | S15-W2-1 | S15 | LH | `inbox-contract.md` (I09, I10) | — |  |
| 2 | S15-W2-5 | S15 | LH | `report-parse.mjs` + guarded `--json` CLI + tests | — |  |
| 3 | S15-W2-2 | S15 | LH | digest-report project skill, tolerant reader (H15, H16) | S15-W2-1, S15-W2-5 |  |
| 4 | S15-W2-3 | S15 | LH | Delete `plugins/digest-report` | S15-W2-2 |  |
| 5 | S15-W2-4 | S15 | LH | Project-skill README | S15-W2-2 |  |
| 6 | S15-W2-6 | S15 | LH | `check-contract.mjs` + tests | S15-W2-5 |  |
| 7 | S15-W2-7 | S15 | LH | digest-report eval cases | S15-W2-2, S15-W2-5 |  |
| 8 | S15-W2-8 | S15 | LH | Provenance query against the Supabase project id (executor, read-only) | S15-W2-2 |  |
| 9 | S16-W2-1 | S16 | LH | `audit-visual.mjs` static module + tests | — |  |
| 10 | S16-W2-2 | S16 | LH | `audit:visual` CLI + render pass; npm script | S16-W2-1, S19-W1-4 |  |
| 11 | S16-W2-3 | S16 | LH | ingest-visual skill (audit before filing) | S16-W2-2 |  |
| 12 | S16-W2-4 | S16 | LH | Delete ingest-infographic, ingest-animation (H29, H31) | S16-W2-3 |  |
| 13 | S16-W2-5 | S16 | LH | pk-plasma-animation skill + `pk-animation` alias | S16-W2-3 |  |
| 14 | S16-W2-6 | S16 | LH | Delete `plugins/pk-plasma-animation` | S16-W2-5 |  |
| 15 | S16-W2-7 | S16 | LH | ingest-visual, pk-plasma eval cases | S16-W2-3, S16-W2-5 |  |
| 16 | S16-W2-8 | S16 | LH | `audit:visual` with real Chromium (executor) | S16-W2-2 |  |
| 17 | S19-W2-1 | S19 | LH | atomize-book visuals → inbox + ingest-visual | S16-W2-3 |  |
| 18 | S20-W2-1 | S20 | LH | vault-atomizer → project skill, dmi | — |  |
| 19 | S20-W2-2 | S20 | LH | vault-vectors → project skill, dmi, `/vectors` | — |  |
| 20 | S20-W2-3 | S20 | LH | vault-coverage dmi | S20-W1-1 |  |
| 21 | S20-W2-4 | S20 | LH | check-repetition Not-for, `npm run revalidate`, dmi | — |  |
| 22 | S20-W2-5 | S20 | LH | vault-atomizer, vault-vectors, vault-coverage, check-repetition eval cases | S12-W0-4, S20-W2-1…4 |  |
| 23 | S14-W2-1 | S14 | LH | `plugins/learn-hub-session` (skip if check b = no) | S11-W0-7, S13-W1-8 |  |
| 24 | S01-W2-1 | S01 | MK | Interim `lock-record.md` (I01) | — |  |
| 25 | S01-W2-2 | S01 | MK | Release intent-lock | S01-W2-1 |  |
| 26 | S02-W2-1 | S02 | MK | DI / PC OPTIONAL intent-lock handoff | — |  |
| 27 | S02-W2-2 | S02 | MK | Release DI, PC | S02-W2-1 |  |
| 28 | S03-W2-1 | S03 | MK | pubmed: `Assumed:` line, fallback, sink, report/1 (H44) | S15-W2-2 |  |
| 29 | S03-W2-2 | S03 | MK | tool-catalog: runtime MCP resolution | S03-W2-1 |  |
| 30 | S03-W2-3 | S03 | MK | intent-lock-pairing: no Reframed | S03-W2-1 |  |
| 31 | S03-W2-4 | S03 | MK | Interim `report-contract.md` + 3 fixtures | S03-W2-1 |  |
| 32 | S03-W2-5 | S03 | MK | Release pubmed-research-note | S03-W2-1…4 |  |
| 33 | S04-W2-1 | S04 | MK | CR: fallback, sink, Not-for, MCP resolution | S15-W2-2 |  |
| 34 | S04-W2-2 | S04 | MK | CR interim contract copy | S03-W2-4, S04-W2-1 |  |
| 35 | S04-W2-3 | S04 | MK | Release comprehensive-review | S04-W2-1, S04-W2-2 |  |
| 36 | S05-W2-1 | S05 | MK | `check-html.mjs` + tests + parity fixture (CA) | — |  |
| 37 | S05-W2-2 | S05 | MK | Copy `check-html.mjs` into ML, CI | S05-W2-1 |  |
| 38 | S05-W2-3 | S05 | MK | CA grammar port, 5-frame verify, filing (H38, H39) | S05-W2-1, S16-W2-3 |  |
| 39 | S05-W2-4 | S05 | MK | ML port, verify, gradient check (H40, H41) | S05-W2-2, S16-W2-3 |  |
| 40 | S05-W2-5 | S05 | MK | CA / ML eval cases | S05-W2-3, S05-W2-4 |  |
| 41 | S05-W2-6 | S05 | MK | CA / ML README, CHANGELOG; release | S05-W2-3, S05-W2-4, S10-W0-8 |  |
| 42 | S06-W2-1 | S06 | MK | CI render/verify via `check-html.mjs`; filing | S05-W2-2, S16-W2-3 |  |
| 43 | S06-W2-2 | S06 | MK | Release clinical-infographic | S06-W2-1 |  |
| 44 | S07-W2-1 | S07 | MK | Filing sentences; asset `.meta.json`; `aliases:` | S07-W1-3, S15-W2-1 |  |
| 45 | S07-W2-2 | S07 | MK | Job count, README target type, layout pointer | — |  |
| 46 | S07-W2-3 | S07 | MK | `vault_index.py` | S07-W2-1 |  |
| 47 | S07-W2-4 | S07 | MK | `drain_plan.py`; empty-vault = transfer (H10, H11) | S07-W2-1, S07-W2-3, S15-W2-1 |  |
| 48 | S07-W2-5 | S07 | MK | vault-keeper / empty-vault eval cases | S07-W2-1, S07-W2-4, S12-W0-3 |  |
| 49 | S07-W2-6 | S07 | MK | Release vault-keeper | S07-W2-1…5 |  |
| 50 | S14-W2-2 | S14 | MK | Confirm/merge fork ledger into micky (H06) | — |  |
| 51 | S14-W2-3 | S14 | LH | Delete learn-hub intent-lock fork | S14-W2-2 |  |
| 52 | S14-W2-4 | S14 | LH | Delete pubmed and CR forks (H48, H49) | S03-W2-1, S04-W2-1, S07-W2-1 |  |
| 53 | S11-W2-1 | S11 | Win+MK | Windows: remove `learn-hub-local` (if found) | — | yes |
| 54 | S14-W2-5 | S14 | LH | Delete `learn-hub-local` catalog (H14) | S11-W2-1, S14-W1-2, S14-W2-3, S14-W2-4, S15-W2-3, S16-W2-6, S20-W2-1, S20-W2-2 |  |
| 55 | S11-W2-2 | S11 | env+MK | Cloud V2→V3: pubmed, CR, CI, ML, CE | S03-W0-1, S03-W2-5, S04-W0-2, S04-W2-1, S04-W2-3, S05-W2-5, S05-W2-6, S06-W1-3, S06-W2-2 | yes |
| 56 | S05-W2-8 | S05 | LH | Push learn-hub branch deleting the CA copy | S05-W2-6, S16-W2-5 |  |
| 57 | S11-W2-3 | S11 | env+MK | Cloud V3→V4: CA atomic swap; merge that branch | S05-W2-5, S05-W2-8, S11-W2-2 | yes |
| 58 | S11-W2-4 | S11 | env+MK | Cloud V4→V5: `learn-hub/plugins`; `/doctor` | S11-W2-3, S14-W1-2, S14-W2-1, S14-W2-3…5, S15-W2-3, S16-W2-6, S20-W2-1, S20-W2-2 | yes |
| 59 | S07-W2-7 | S07 | both | Rehearsal + no-digest-without-the-word check | S07-W2-4, S11-W2-4 (or its skip record, check b = no), S14-W2-4, S15-W2-2 | yes |
| 60 | S04-W2-5 | S04 | claude.ai | OD8: owner edits the synced `daily-random-review` skill; record in MK `baseline.md` | S04-W2-1 | yes |
| 61 | S04-W2-4 | S04 | cloud | One unattended daily-random-review run | S11-W2-2, S04-W2-5 | yes |
| 62 | S11-W2-5 | S11 | Win+MK | Windows: refresh installs | S01-W2-2, S02-W2-2, S03-W2-5, S04-W2-3, S05-W2-6, S06-W2-2, S07-W2-6 | yes |
| 63 | S12-W2-T | S12 | both | Tag `wave-2` | all W2 | yes |

**Exit gates** (`validate.py --cross-repo` exists only from S08-W3-1; the two contract checks below are the W2 cross-repo gate, §8 Q12):

| Check | Command | Expected |
|---|---|---|
| Report contract | `node scripts/check-contract.mjs --json` (LH, default dir) | exit 0; `report/1` for 3 fixtures |
| Visual parity | `node plugins/concept-animation/scripts/check-html.mjs --parity --root . --own` (MK) | bad fixtures fail with the exact codes; examples pass or `incomplete` |
| Audit CLI | `npx vitest run scripts/lib/audit-visual.test.mjs`; `npm run -s audit:visual -- --help` (LH) | exit 0; exit 0 |
| Retirements | `test ! -d plugins/intent-lock -a ! -d plugins/pubmed-research-note -a ! -d plugins/comprehensive-review -a ! -e .claude-plugin/marketplace.json` (LH) | true |
| CA copy gone | `test ! -d /home/user/learn-hub/.claude/skills/concept-animation` | true |
| LH plugins folder | `ls /home/user/learn-hub/plugins` | `learn-hub-session` (absent or empty if check b = no, critique C2-30) |
| Rehearsal | S07-W2-7 record | provenance count matches; no digest without the word |
| Unattended run | S04-W2-4 record | completes |
| Load once | `delivery_log.py live --env cloud:<id> --expect auto`; `/doctor` | `"ok": true`, 11 entries (10 if check b = no); no overflow |
| HIGH rows | h-coverage W2 rows (16), H10b, H11b | closed |

**Rollback.** Revert the W2 merges; the forks come back from the tag. Set the cloud value back to V2. The inbox is git-tracked, so no report is lost. S07-W2-7's learn-hub vault files stay on master because their rows are live; a revert does not undo Supabase writes (critique C2-21).

**`CLAUDE_CODE_PLUGIN_DIRS`.** Cloud: V2 → V3 (adds pubmed, CR, CI, ML, CE) at S11-W2-2 → V4 (adds concept-animation) at S11-W2-3 → V5 (adds `/home/user/learn-hub/plugins`) at S11-W2-4, only if check b = yes. Windows: `learn-hub-local` removed (S11-W2-1), installs refreshed (S11-W2-5).

### W3 — micky consolidation (skeleton, then alignment, evidence, visuals)

**Entry.** W2 exit gates green; OD3, OD6, OD7, OD9, OD10, OD12, OQ6 and OQ10 answered; tag `wave-2` pushed. S08-W3-1 is placed right after the skeleton because every later W3 check uses its validator.

| # | Step | Spec | Repo | What | Depends on | OWNER |
|---|---|---|---|---|---|---|
| 1 | S11-W3-1 | S11 | env+MK | Cloud V5→V6 (folder paths); MEMORY:11 | W2 exit | yes |
| 2 | S11-W3-2 | S11 | Win+MK | Windows switch to the env var (OD2-a) | S11-W3-1 | yes |
| 3 | S11-W3-3 | S11 | MK | README install section | S11-W3-2 |  |
| 4 | S10-W3-1 | S10 | MK | marketplace.json W3 shape + `renames` (one PR with the next row) | S10-W0-3, S11-W3-1 |  |
| 5 | S10-W3-2 | S10 | MK | Skeleton PR, one commit per family: moves, root dirs, family manifests, 7 aliases | S10-W3-1 |  |
| 6 | S11-W3-5 | S11 | MK | Log: families load (8 entries) | S10-W3-2 |  |
| 7 | S08-W3-1 | S08 | MK | validate.py / release.py into plugin-creator; health.sh; lists (one PR, four commits) | S08-W1-2, S10-W0-1…3, S10-W0-8, S10-W3-2, S11-W0-3 |  |
| 8 | S12-W3-2 | S12 | MK | Live trigger evals BEFORE (5 families) | S10-W3-2, S12-W0-6 |  |
| 9 | S01-W3-1 | S01 | MK | `interview-protocol.md`; lock-record names | S10-W3-2 |  |
| 10 | S01-W3-2 | S01 | MK | intent-lock by subtraction (H01, H02) | S01-W3-1, S12-W3-2 |  |
| 11 | S01-W3-3 | S01 | MK | misread-capture + `ledger.py` (H04) | S01-W3-1 |  |
| 12 | S01-W3-4 | S01 | MK | Reformat `state/misreads.md` (H03) | S01-W2-1, S14-W2-2, S10-W3-2, S01-W3-3 |  |
| 13 | S02-W3-1 | S02 | MK | DI / PC eval cases | S10-W3-2 |  |
| 14 | S02-W3-2 | S02 | MK | decision-interview rewrite | S10-W3-2, S01-W3-1, S12-W3-2 |  |
| 15 | S02-W3-3 | S02 | MK | plan-critique rewrite | S10-W3-2, S01-W3-1, S12-W3-2 |  |
| 16 | S01-W3-5 | S01 | MK | alignment plugin.json, README, CHANGELOG | S01-W3-2, S01-W3-3, S02-W3-2, S02-W3-3 |  |
| 17 | S02-W3-4 | S02 | MK | README sections DI / PC | S02-W3-2, S02-W3-3, S01-W3-5 |  |
| 18 | S01-W3-6 | S01 | MK | intent-lock / misread-capture eval cases | S01-W3-2, S01-W3-3 |  |
| 19 | S01-W3-7 | S01 | MK | Release alignment (`release.py alignment minor`) | S08-W3-1, S01-W3-5, S01-W3-6, S02-W3-1, S02-W3-4 |  |
| 20 | S03-W3-1 | S03 | MK | `engines.md`; edit moved `report-contract.md` | S01-W3-2, S10-W3-2 |  |
| 21 | S03-W3-2 | S03 | MK | Decision brief: 6 slots (H45); drop "Klaeng" (K13) | S01-W3-2, S03-W3-1 |  |
| 22 | S03-W3-3 | S03 | MK | Dedupe the depth contract | S03-W3-1 |  |
| 23 | S03-W3-4 | S03 | MK | pubmed description | S03-W3-1, S12-W3-2 |  |
| 24 | S03-W3-5 | S03 | MK | `sources_lint.py`, mocks | S03-W3-1 |  |
| 25 | S03-W3-6 | S03 | MK | pubmed eval cases | S03-W3-1, S03-W3-5 |  |
| 26 | S04-W3-1 | S04 | MK | `sweep.py`; `state/lit-watch/` | S10-W3-2 |  |
| 27 | S04-W3-2 | S04 | MK | CR remaining fixes | S01-W3-2, S10-W3-2 |  |
| 28 | S04-W3-3 | S04 | MK | CR + lit-watch descriptions; rename; lock re-key | S10-W3-2, S12-W3-2 |  |
| 29 | S04-W3-4 | S04 | MK | triage-rubric pointer | S10-W3-2 |  |
| 30 | S04-W3-5 | S04 | MK | CR eval cases | S04-W3-3 |  |
| 31 | S04-W3-6 | S04 | MK | lit-watch eval cases | S04-W3-1, S04-W3-3 |  |
| 32 | S03-W3-7 | S03 | MK | evidence README / CHANGELOG / LICENSE | S03-W3-6, S04-W3-6 |  |
| 33 | S03-W3-8 | S03 | MK | Release evidence (`release.py evidence minor`) | S08-W3-1, S03-W3-2…4, S03-W3-7, S04-W3-2, S04-W3-4, S04-W3-5 |  |
| 34 | S05-W3-1 | S05 | MK | `html-artifact-contract.md`, `render-verify.md` | S01-W3-2, S10-W3-2 |  |
| 35 | S05-W3-2 | S05 | MK | CA / ML descriptions + handoffs | S05-W3-1, S12-W3-2 |  |
| 36 | S05-W3-3 | S05 | MK | ML size trim | S05-W3-1 |  |
| 37 | S05-W3-4 | S05 | MK | visuals plugin.json | S05-W3-1, S08-W3-1 |  |
| 38 | S05-W3-5 | S05 | MK | visuals README / CHANGELOG / LICENSE | S05-W3-4 |  |
| 39 | S06-W3-1 | S06 | MK | lessons-learned → CHANGELOG; example README rename | S05-W3-1, S05-W3-5, S10-W3-2 |  |
| 40 | S06-W3-2 | S06 | MK | CI / CE descriptions + handoffs | S01-W3-2, S06-W3-1, S12-W3-2 |  |
| 41 | S06-W3-3 | S06 | MK | CE fidelity; `--kind code-explainer --source` | S05-W3-1, S06-W3-2 |  |
| 42 | S06-W3-4 | S06 | MK | Verify the two visuals alias skills | S06-W3-1, S10-W3-2 |  |
| 43 | S05-W3-6 | S05 | MK | Release visuals (`release.py visuals minor`) | S08-W3-1, S05-W3-2, S05-W3-3, S05-W3-5, S06-W3-1…4 |  |
| 44 | S08-W3-2 | S08 | MK | plugin-creator SKILL.md rewrite | S08-W3-1, S12-W3-2 |  |
| 45 | S08-W3-3 | S08 | MK | refine-plugin rewrite + `new-plugin` alias | S08-W3-1, S12-W3-2 |  |
| 46 | S08-W3-4 | S08 | MK | Scaffold writes README/CHANGELOG/LICENSE/evals | S08-W3-2 |  |
| 47 | S08-W3-5 | S08 | MK | Templates: quoted placeholders, alias template | S08-W3-1 |  |
| 48 | S08-W3-6 | S08 | MK | MCP wiring in the scaffold | S08-W3-5 |  |
| 49 | S08-W3-7 | S08 | MK | Delete plugin-creator `commands/` only | S08-W3-2, S08-W3-3, S10-W0-4 |  |
| 50 | S08-W3-8 | S08 | MK | plugin-creator eval cases | S08-W3-2, S08-W3-3 |  |
| 51 | S08-W3-9 | S08 | MK | Release plugin-creator | S08-W3-1…8 |  |
| 52 | S09-W3-1 | S09 | MK | firecrawl router + dated vendor reference | S08-W3-1, S09-W1-2, S10-W0-8, S10-W3-2, S12-W3-2, OQ6 answer |  |
| 53 | S09-W3-2 | S09 | MK | gridgeist `UPSTREAM.md`; drop Codex file, assets | S10-W0-8 |  |
| 54 | S09-W3-3 | S09 | MK | firecrawl / gridgeist eval cases | S09-W3-1, S09-W3-2 |  |
| 55 | S09-W3-4 | S09 | MK | Release firecrawl, gridgeist | S09-W3-1…3 |  |
| 56 | S11-W3-4 | S11 | env+MK | firecrawl enablement per the owner answer | S09-W3-1 | yes |
| 57 | S07-W3-1 | S07 | MK | Delete the empty-vault command file | S07-W1-2, S10-W3-2 |  |
| 58 | S07-W3-2 | S07 | MK | Release vault-keeper | S07-W3-1, S08-W3-1 |  |
| 59 | S12-W3-3 | S12 | MK | Live trigger evals AFTER | S01-W3-2, S02-W3-2, S02-W3-3, S03-W3-4, S04-W3-3, S05-W3-2, S06-W3-2, S08-W3-2, S08-W3-3, S09-W3-1, S12-W3-2 |  |
| 60 | S10-W3-8 | S10 | MK | micky CLAUDE.md ≤5 KB | S01-W3-6, S02-W3-4, S03-W3-7, S04-W3-6, S05-W3-5, S06-W3-4, S07-W3-1, S08-W3-9, S09-W3-4, S10-W3-2 |  |
| 61 | S10-W3-9 | S10 | MK | Delete ROUTING.md, route.py | S08-W3-7, S10-W3-8 |  |
| 62 | S10-W3-10 | S10 | MK | MEMORY split → `docs/history.md` | S10-W3-8, S11-W3-1 |  |
| 63 | S10-W3-11 | S10 | MK | Archive the superseded plan | — |  |
| 64 | S12-W3-1 | S12 | MK | Check: no `evals.json` left in micky | S01-W3-6, S02-W3-1, S03-W3-6, S04-W3-5, S04-W3-6, S05-W2-5, S06-W1-3, S07-W2-5, S08-W3-8, S09-W3-3 |  |
| 65 | S12-W3-4 | S12 | both | Routing smoke (≥17/20, 0 destructive) | S11-W3-5, S12-W3-3 |  |
| 66 | S12-W3-5 | S12 | MK | Two-arm release eval per plugin | S12-W3-1…4 |  |
| 67 | S12-W3-T | S12 | both | Tag `wave-3` | all W3 | yes |

Note: S01-W3-7, S03-W3-8, S05-W3-6 and S07-W3-2 release alignment, evidence, visuals and vault-keeper with `release.py` after S08-W3-1 (critique P-05).

**Exit gates:**

| Check | Command | Expected |
|---|---|---|
| Validator | `python3 plugins/plugin-creator/scripts/validate.py --repo . --cross-repo "$LEARN_HUB_DIR"` | `all checks passed` |
| Layout | `find plugins -maxdepth 1 -mindepth 1 -type d \| sort` | alignment, evidence, firecrawl, gridgeist, plugin-creator, vault-keeper, visuals |
| No commands, no evals.json | `find plugins -type d -name commands`; `find plugins -name evals.json` | empty; empty |
| Router gone | `test ! -f ROUTING.md -a ! -f scripts/route.py` | true |
| Context diet | `wc -c CLAUDE.md MEMORY.md` | ≤ 5,120; ≤ 6,144 |
| Routing smoke | S12-W3-4 | ≥17/20 and 0 destructive misroutes |
| Release eval | S12-W3-5 | each plugin ≥ its `--against pre-rewrite` score; every grader passes where no baseline exists |
| Listing | `/doctor`; `rewrite_gate.py baseline measure` | no overflow; always-on ≤ 3,000 tok |
| Delivery | `live --expect auto` (cloud); Windows `claude plugin marketplace list --json` | 8 entries; no `micky-psych-tools` |
| HIGH rows | every row assigned to W0–W3 (H07b included) | closed |

**Rollback.** Revert the W3 merges, newest first. To undo one family, revert that family's commits (the skeleton's per-family commit and the family's later commits, listed in the W3 exit record), then run `bash scripts/health.sh`. `ratchet.json`, the lock, CLAUDE.md and README are shared by all families: revert their edits with the last family (critique C2-21). The folder path absorbs layout reverts with no env edit. Windows under OD2-a: the same.

**`CLAUDE_CODE_PLUGIN_DIRS`.** Cloud: V5 → V6 (`/home/user/micky-psych-tools/plugins:/home/user/learn-hub/plugins`) at S11-W3-1; 15 entries before the skeleton, 8 after (S11-W3-5). Windows: the user variable is set, then the marketplace copies are uninstalled (S11-W3-2). firecrawl enablement per OQ6 (S11-W3-4).

### W4 — learn-hub consolidation and context diet

**Entry.** W2 exit (W3 not required); OD11 and OQ9 answered; W0 check e answered (`.claude/rules` or `docs/gotchas/`); the owner agrees a freeze window for atomize-book imports (S19-W4-1).

| # | Step | Spec | Repo | What | Depends on | OWNER |
|---|---|---|---|---|---|---|
| 1 | S12-W4-2 | S12 | cloud | Live trigger evals BEFORE (PDF, atomize families) | S12-W0-6 |  |
| 2 | S19-W4-0 | S19 | Win+LH | Pre-split chapter baseline (`BOOK_ROOT`) | W2 exit | yes |
| 3 | S17-W4-0 | S17 | Win+LH | Pre-W4 article baseline | W2 exit | yes |
| 4 | S21-W4a-1 | S21 | LH | `gotcha-map.md`, keyed by heading text, built from the W4-entry CLAUDE.md | S21-W0-1 |  |
| 5 | S21-W4a-4 | S21 | LH | `move-blocks.mjs`: cut, archive, byte check | S21-W4a-1 |  |
| 6 | S21-W4a-3 | S21 | LH | `gotchas-archive.md` by script; pk-plasma line | S21-W4a-4, S21-W4a-1, S16-W2-6 |  |
| 7 | S21-W4a-2 | S21 | LH | `docs/vault-format.md`; 6 skills' gotchas (by script) | S21-W4a-3 |  |
| 8 | S13-W4-1 | S13 | LH | sync-vault gotchas: move + delete | S13-W1-6, S21-W4a-2 + S21-W4a-4 (plan) |  |
| 9 | S19-W4-1 | S19 | LH | Freeze atomize-book imports from S19-W4-2 until S19-W4-9 passes; save the pre-split SKILL.md | W2 exit, S19-W4-0 | yes |
| 10 | S19-W4-2 | S19 | LH | `references/extract.md` | S19-W1-1…8, S19-W4-1 |  |
| 11 | S19-W4-3 | S19 | LH | `references/figures.md` (verbatim move) | S19-W4-2 |  |
| 12 | S19-W4-3b | S19 | LH | Renumber `references/figures.md`; Contents | S19-W4-3 |  |
| 13 | S19-W4-4 | S19 | LH | `references/measure.md` | S19-W4-3 |  |
| 14 | S19-W4-5 | S19 | LH | `references/qc.md` | S19-W4-4 |  |
| 15 | S19-W4-6 | S19 | LH | `references/traps.md` | S19-W4-5 |  |
| 16 | S19-W4-8 | S19 | LH | atomize-book gotchas: move + delete | S21-W4a-2 + S21-W4a-4 (plan) |  |
| 17 | S19-W4-7 | S19 | LH | Final SKILL.md pass (H24) | S19-W4-2…6 |  |
| 18 | S19-W4-9 | S19 | Win+LH | Exit test: 354 tests; chapter re-run vs the S19-W4-0 baseline | S19-W4-7, S19-W4-0 | yes |
| 19 | S19-W4-10 | S19 | LH | atomize-book eval cases (3 smoke) | S12-W0-4, S19-W4-7 |  |
| 20 | S21-W4b-1 | S21 | LH | App gotchas + Pages → 13 `.claude/rules` files; upkeep line; size check | S13-W4-1, S19-W4-8, S21-W4a-2 |  |
| 21 | S17-W4-1 | S17 | LH | ingest-article conditional references | S17-W1-2, S21-W4a-2, S17-W4-0 |  |
| 22 | S17-W4-2 | S17 | LH | Measure ingest-article / -slides size | S17-W4-1 |  |
| 23 | S17-W4-3 | S17 | LH | 4 more eval cases | S12-W0-4, S17-W1-12 |  |
| 24 | S17-W4-5 | S17 | Win+LH | One article re-run end to end; compare gate verdicts | S17-W4-0…3 | yes |
| 25 | S18-W4-2 | S18 | LH | verify SKILL.md | S21-W4a-2 |  |
| 26 | S18-W4-3 | S18 | LH | verify scripts (lib + tests in `scripts/lib`) | S18-W4-2 |  |
| 27 | S18-W4-1 | S18 | LH | `classify_pdf.py` + tests (I26) | S18-W1-1 |  |
| 28 | S18-W4-4 | S18 | LH | verify + pdf-pipeline eval cases | S12-W0-4, S18-W1-9 |  |
| 29 | S17-W4-4 | S17 | LH | Hand trigger queries to S12 | S17-W1-2, S17-W1-8, S18-W4-1 |  |
| 30 | S18-W4-5 | S18 | LH | Hand trigger queries to S12 | S17-W4-4, S18-W1-8 |  |
| 31 | S12-W4-3 | S12 | cloud | Live trigger evals AFTER | S17-W4-4, S18-W4-5 |  |
| 32 | S12-W4-1 | S12 | LH | Project-skill smoke | S13-W1-9, S17-W4-3, S18-W4-4, S19-W4-9, S19-W4-10, S20-W2-5 |  |
| 33 | S12-W4-T | S12 | LH | Tag `wave-4` | all W4 | yes |

Note: S19-W4-0 and S17-W4-0 record the pre-W4 gate verdicts on Windows before any atomize-book or ingest-article change; S19-W4-9 and S17-W4-5 compare gate verdicts (pass/fail), not scores, because fresh drafting varies between runs (critique F14, P-14). S19-W4-10 and S20-W2-5 write the eval cases S12-W4-1 needs (P-06). Gotcha blocks move by script (`move-blocks.mjs`, S21-W4a-4), never by hand (C2-08).

**Exit gates:**

| Check | Command | Expected |
|---|---|---|
| CLAUDE.md size | `wc -c CLAUDE.md` (LH) | ≤ 32,768 |
| Exactly once | `node scripts/move-blocks.mjs --check` (LH) | exit 0: every mapped block from the W4-entry CLAUDE.md exists once across the destinations, byte-identical |
| Size guard | skill-lint check 10 (`CLAUDE.md` ≤ 32,768 bytes) inside `npm run check:skills` | exit 0 |
| Rules files | `ls .claude/rules/*.md \| wc -l` | 13 (or `docs/gotchas/` if check e = no) |
| atomize-book tests | `python3 -m unittest discover -s .claude/skills/atomize-book/scripts -p 'test_*.py'` | `Ran 354 tests … OK` |
| atomize-book size | `python3 $MICKY_TOOLS_DIR/docs/plugin-rewrite/phase3/measure.py skill .claude/skills/atomize-book/SKILL.md` | body ≤ 500 lines, ≤ 5,000 tok |
| ingest-article size | same for ingest-article | body ≤ 6,000 tok |
| Chapter re-run | S19-W4-9 (OWNER, Windows) against `docs/rewrite/w4-chapter-baseline/` | no gate verdict went from pass to fail |
| Article re-run | S17-W4-5 (OWNER, Windows) against `docs/rewrite/w4-article-baseline/` | no gate verdict went from pass to fail |
| Triggers | S12-W4-3 | no family below its before-score beyond noise |
| HIGH rows | H24 | closed |

**Rollback.** Revert. `docs/gotchas-archive.md` still holds every moved heading verbatim.

**`CLAUDE_CODE_PLUGIN_DIRS`.** No change.

### W5 — Hardening and deferred decisions

**Entry.** W3 and W4 exits; 2–4 weeks of use after W3.

| # | Step | Spec | Repo | What | Depends on | OWNER |
|---|---|---|---|---|---|---|
| 1 | S12-W5-1 | S12 | both | Full two-arm release pass, both repos | W3, W4 exits |  |
| 2 | S12-W5-2 | S12 | both | Routing smoke with everything loaded | S12-W5-1 |  |
| 3 | S09-W5-1 | S09 | MK | gridgeist usage decision | 2-4 weeks after W3 | yes |
| 4 | S04-W5-1 | S04 | MK | lit-watch usage decision (OD10) | 2-4 weeks after W3 | yes |
| 5 | S07-W5-1 | S07 | MK | Revisit OD4 with usage data | W3, W4 exits; 2-4 weeks after W3 | yes |
| 6 | S12-W5-3 | S12 | both | Empty the ratchet; checks fail hard; `## W5 decisions` | S12-W5-1, S04-W5-1, S07-W5-1, S09-W5-1 |  |
| 7 | S10-W5-1 | S10 | MK | MEMORY: final numbers | W3, W4 exits |  |
| 8 | S11-W5-1 | S11 | MK | Close the delivery record | W3, W4 exits, S09-W5-1 |  |

S04-W5-1 (lit-watch usage), S07-W5-1 (OD4 revisit) and S12-W5-3 (ratchet emptied, checks fail hard, `## W5 decisions` as the decision log) close the W5 items (critique P-13).

**Exit gates:**

| Check | Command | Expected |
|---|---|---|
| Ratchet empty | S12-W5-3; `ratchet verify` in both repos | 0 entries; a formerly listed violation now fails |
| Release pass | S12-W5-1 | every plugin and project skill ≥ its `--against pre-rewrite` score (every grader passes where no baseline exists) |
| Routing | S12-W5-2 | ≥17/20, 0 destructive |
| Delivery | `delivery_log.py check --strict`; latest rows | exit 0; V6 and the final Windows value |
| §9 targets | `baseline.md` W5 section | met, or a recorded reason |

**Rollback.** Not applicable (decisions and measurements).

**`CLAUDE_CODE_PLUGIN_DIRS`.** No change (a retired plugin needs no env edit under the folder path).

## 4. Owner action checklist

In order. "Plan" rows are not spec steps; they come from §1 and §8.

| # | Wave | Step | Action |
|---|---|---|---|
| 1 | before W0 | Plan | Confirm OD1, OD2 (provisional), OD14; answer OQ1, OQ2, OQ3, OQ7, OQ8, OQ11, OQ16 |
| 2 | W0 | S12-W0-0 | Tag `pre-rewrite` in both repos |
| 3 | W0 | S10-W0-11 | `git config core.hooksPath .githooks` in each micky clone |
| 4 | W0 | S11-W0-5 | Cloud env: add the 5 variables (V0) and paste setup script v1 |
| 5 | W0 | S11-W0-7 | Run checks a, b, e, f, h (+ the userConfig check for S07) |
| 6 | W0 | S11-W0-9 | Approve the check-d eval run (≤ USD 0.50) |
| 7 | W0 | S12-W0-6 | Confirm `claude plugin eval` availability |
| 8 | W0 | S11-W0-10 | Windows: check g; set Windows variables |
| 9 | W0 | S11-W0-11 | Cloud env: V0 → V1; paste setup script v2 |
| 10 | W0 | Plan | Answer OQ14 once check e is recorded |
| 11 | W0 | S12-W0-T | Tag `wave-0` |
| 12 | before W1 | Plan | Answer OQ12 |
| 13 | W1 | S20-W1-1b | Windows: backfill `coverage-sources.json` from `BOOK_ROOT` |
| 14 | W1 | S14-W1-1 | Run `npm run vectors:check`; decide restore or leave per orphan (OQ5; no delete in W1) |
| 15 | W1 | S13-W1-10 | Approve and watch one live sync; compare the diagrams count |
| 16 | W1 | Plan | Answer OQ4 before S11-W1-1 |
| 17 | W1 | S11-W1-1 | Cloud env: V1 → V2 |
| 18 | W1 | S11-W1-2 | Windows: refresh installs |
| 19 | W1 | S12-W1-T | Tag `wave-1` |
| 20 | before W2 | Plan | Confirm OD4, OD5, OD8; answer OQ13, OQ15 |
| 21 | W2 | S11-W2-1 | Windows: remove `learn-hub-local` if check g found it (before S14-W2-5) |
| 22 | W2 | S11-W2-2 | Cloud env: V2 → V3; confirm the OQ4 exception for pubmed |
| 23 | W2 | S11-W2-3 | Cloud env: V3 → V4; branch session; merge the CA-copy deletion |
| 24 | W2 | S11-W2-4 | Cloud env: V4 → V5; record `/doctor` |
| 25 | W2 | S07-W2-7 | Rehearsal: fixture report → transfer → "digest" → sync; no-digest check |
| 26 | W2 | S04-W2-5 | OD8: edit the claude.ai-synced `daily-random-review` skill; record it in MK `baseline.md` |
| 27 | W2 | S04-W2-4 | One unattended daily-random-review run |
| 28 | W2 | S11-W2-5 | Windows: refresh installs |
| 29 | W2 | S12-W2-T | Tag `wave-2` |
| 30 | before W3 | Plan | Confirm OD3, OD6, OD7, OD9, OD10, OD12; answer OQ6, OQ10 |
| 31 | W3 | S11-W3-1 | Cloud env: V5 → V6; confirm the OQ4 exception for the four W3 plugins |
| 32 | W3 | S11-W3-2 | Windows: set the user variable, verify, uninstall marketplace copies |
| 33 | W3 | S11-W3-4 | firecrawl enablement per OQ6 |
| 34 | W3 | S12-W3-T | Tag `wave-3` |
| 35 | before W4 | Plan | Confirm OD11; answer OQ9 |
| 36 | W4 | S19-W4-0 | Windows: record the pre-split chapter baseline (`BOOK_ROOT`) |
| 37 | W4 | S17-W4-0 | Windows: record the pre-W4 article baseline |
| 38 | W4 | S19-W4-1 | Freeze atomize-book imports from S19-W4-2 until S19-W4-9 passes |
| 39 | W4 | S19-W4-9 | Windows: chapter re-run; compare gate verdicts; end the freeze |
| 40 | W4 | S17-W4-5 | Windows: one article re-run; compare gate verdicts |
| 41 | W4 | S12-W4-T | Tag `wave-4` |
| 42 | W5 | S09-W5-1 | gridgeist usage decision from `/skill-doctor` |
| 43 | W5 | S04-W5-1 | lit-watch usage decision (OD10) |
| 44 | W5 | S07-W5-1 | Revisit OD4 with usage data |
| 45 | W5 | Plan | Confirm OD13 (S12-W5-3 records it under `## W5 decisions`) |

## 5. Shared files

Files edited by more than one spec, in merge order. Merge each step only after the one before it in the row.

| File | Steps, in merge order |
|---|---|
| MK `scripts/validate.py` → `plugins/plugin-creator/scripts/validate.py` | S10-W0-1 → S08-W3-1 (move + rewrite) |
| MK `scripts/health.sh` | S10-W0-9 → S11-W0-3 → S08-W3-1 |
| MK `.claude-plugin/marketplace.json` | S10-W0-3 → S10-W3-1 (W1/W2 release steps do not touch it) |
| MK `CLAUDE.md` | S10-W0-5 → S10-W3-8 |
| MK `README.md` | S10-W0-6 → S11-W3-3 |
| MK `MEMORY.md` | S11-W0-10 (line 11) → S11-W3-1 (line 11) → S10-W3-10 (keeps line 11) → S10-W5-1 |
| MK `docs/rewrite/ratchet.json` | S12-W0-1 (create, empty) → S10-W0-1b (seed `yaml-parse`) → S08-W3-1 (seed its new check ids) → every fixing step (close) → S12-W5-3 (empty; checks fail hard) |
| MK `docs/rewrite/CHANGELOG.md` | S10-W0-8 (create, OQ16) → every MK tooling step in S10, S11, S12 |
| MK `docs/rewrite/baseline.md` | S12-W0-7 → S12-W0-8 (`## W0 smoke`) → `## Owner records` (S04-W2-5, S04-W2-4, S07-W2-7) → wave-exit sections → S12-W5-3 (`## W5 decisions`) |
| MK `docs/rewrite/h-coverage.md` (canonical) | S12-W0-1 → each wave's tag step (S12-W0-T … S12-W4-T closes that wave's rows) |
| MK `docs/rewrite/triggers.lock.json` | S12-W0-1 → the MK rows of the lock table below, in wave order |
| MK `docs/rewrite/delivery-log.md`, `cloud-setup.sh` | S11 steps only, in S11 order (S11-W0-2 → … → S11-W5-1) |
| MK per-plugin `plugin.json` + `CHANGELOG.md` | S10-W0-8 (backfill) → each plugin's W1 and W2 release step → S10-W3-2 (move) → W3 release steps (S01-W3-7, S03-W3-8, S05-W3-6, S07-W3-2, S08-W3-9, S09-W3-4) |
| MK `…/intent-lock/references/misreads.md` → `state/misreads.md` | S14-W2-2 → S10-W3-2 (move) → S01-W3-4 |
| MK `plugins/intent-lock/references/lock-record.md` | S01-W2-1 → S10-W3-2 (move) → S01-W3-1 |
| MK `report-contract.md` + `evals/fixtures/` | S03-W2-4 → S10-W3-2 (move) → S03-W3-1 |
| MK `check-html.mjs` | S05-W2-1 → S05-W2-2 (copies) → S10-W3-2 (one copy kept) → S05-W3-1 → S06-W3-3 |
| MK family `plugin.json` | S10-W3-2 (create, 1.0.0) → S01-W3-5 (alignment) / S05-W3-4 (visuals) |
| MK family `README.md`, `CHANGELOG.md` | S10-W3-2 (per-member files) → alignment: S01-W3-5 → S02-W3-4 → S01-W3-7; evidence: S03-W3-7 → S03-W3-8; visuals: S05-W3-5 → S06-W3-1 → S05-W3-6 |
| LH `package.json` | S21-W0-2 → S13-W1-5 → S19-W1-4 → S16-W2-2 |
| LH `README.md` | S21-W0-2 → S12-W0-4 → S13-W1-5 → S13-W1-7 → S19-W1-4 → S16-W2-2 |
| LH `docs/rewrite/ratchet.json` | S12-W0-2 (create) → S21-W0-2 (seed skill-lint failures) → S05-W1-1, S16-W1-1, S16-W1-2, S17-W1-2, S17-W1-8, S19-W1-8 (close) → S12-W5-3 (empty) |
| LH `docs/rewrite/triggers.lock.json` | S12-W0-2 → the LH rows of the lock table below, in wave order |
| LH `docs/rewrite/baseline.md` | S12-W0-7 → S12-W0-8 → `## Owner records` (S13-W1-10, S15-W2-8, S16-W2-8) → wave-exit sections |
| LH `.gitignore` | S13-W1-8 → S17-W1-1 |
| LH `CLAUDE.md` | S13-W1-7 → S21-W1-1 → S21-W1-4 → S21-W4a-3 → S21-W4a-2 → S13-W4-1 → S19-W4-8 → S21-W4b-1 (W4 blocks move by `move-blocks.mjs`, S21-W4a-4) |
| LH `docs/cloud-env-setup.md` | S11-W0-4 → S13-W1-11 |
| LH `docs/rewrite/h-coverage.md` | S12-W0-2 → a byte copy of micky's canonical file at each wave's tag step |
| LH `atomize-book/SKILL.md` | S19-W1-1 … S19-W1-8 → S19-W2-1 → S19-W4-2 … S19-W4-8 |
| LH `ingest-article/SKILL.md` | S17-W1-2 … S17-W1-6 → S17-W4-1 (after S21-W4a-2 adds `references/gotchas.md`) |
| LH `pdf-pipeline/SKILL.md` | S18-W1-2, -3, -4, -6, -8 → S18-W4-1 |
| LH `verify/` | S21-W4a-2 (`references/gotchas.md`) → S18-W4-2 (SKILL.md points at it) |
| LH `vault-coverage/SKILL.md` | S20-W1-1 → S20-W2-3 → S21-W4a-2 (references) |

**Trigger-lock edits** (critique F7; §0 rule 7). Each step runs its lock command in the same commit as the description change, then `triggers verify`. MK: `python3 scripts/rewrite_gate.py triggers …`; LH: `node scripts/rewrite-gate.mjs triggers …`; add `--write`. `remove --phrase` takes `--skill <s> --reason "<spec> §6"`. A phrase that only moves inside its skill needs no command when `triggers verify` still finds it.

| Step | Repo | Skill | Lock command |
|---|---|---|---|
| S14-W1-2 | LH | `ingest-source` (source-to-vault) | `remove --skill ingest-source --reason "plugin retired (H17–H20)"` |
| S17-W1-2 | LH | ingest-article | `remove --phrase` "bullet-reconstruct this" and "reconstruct + add this study"; `extract --skill ingest-article` (records "reconstruct this study") |
| S19-W1-8 | LH | atomize-book | `remove --phrase` "import `<book>` into the vault" and "re-sync the vault" |
| S15-W2-3 | LH | digest-report | `remove --phrase` "digest this review into notes" and "atomize" (the plugin copy is gone; the project skill keeps the name) |
| S16-W2-3 | LH | ingest-visual | `extract --skill ingest-visual` |
| S16-W2-4 | LH | ingest-infographic, ingest-animation | `remove --skill <each> --reason "merged into ingest-visual"` |
| S16-W2-6 | LH | pk-plasma-animation | `remove --phrase` for each placeholder phrase S16 §6 marks "concrete examples substituted"; `extract --skill pk-plasma-animation` |
| S20-W2-1 | LH | vault-atomizer | `remove --phrase "/atomize"` |
| S14-W2-3 | LH | intent-lock, misread-capture (forks) | `remove --skill <each> --reason "fork retired; kept in micky"` |
| S14-W2-4 | LH | pubmed-research-note, comprehensive-review (forks) | `remove --skill <each> --reason "fork retired; kept in micky"` |
| S05-W2-8 | LH | concept-animation (learn-hub copy) | `remove --skill concept-animation --reason "copy deleted; micky skill kept"` |
| S03-W3-4 | MK | pubmed-research-note | `remove --phrase` "atomize", "ทำโน้ต", "comprehensive review of X" |
| S04-W3-3 | MK | comprehensive-review, lit-watch | the spec's re-key commands, plus `remove --phrase` for the CR and PPD phrases S04 §6 marks removed |
| S05-W3-2 | MK | ml-concept-lab | `remove --phrase` "show me how X works", "animate this algorithm" |
| S08-W3-2 | MK | plugin-creator | `remove --phrase "scaffold a skill/command/agent"`; `extract --skill plugin-creator` |
| S08-W3-3 | MK | refine-plugin | `remove --phrase` "audit this skill", "tighten the trigger description" |
| S09-W3-1 | MK | firecrawl | `remove --phrase "search the web"`; `extract --skill firecrawl` |

## 6. Risks

| K | Risk (architecture §12) | Mitigating steps |
|---|---|---|
| K1 | plugin dirs do not load; `~` paths; old CLI | S11-W0-5, S11-W0-7 (check a), S11-W0-10 (check g), S11-W0-1 (path rules), S13-W1-8 (ready line) |
| K2 | listing overflow | S11-W2-4 (`/doctor`), S12-W0-7 (baseline), all description steps, dmi flips (S07-W1-2, S20-W2-1…4, S08-W3-3), S12-W3-3 |
| K3 | multi-repo sessions skip project hooks | S13-W1-3, S13-W1-4 (gates inside apply-sync), S13-W1-8, S14-W2-1, S13-W1-10 (diagrams count) |
| K4 | MCP prefix changes once plugins load | S03-W2-2, S04-W1-1, S04-W2-1 before S11-W2-2 |
| K5 | same-named unit loads twice | S14-W2-3, S14-W2-4, S14-W2-5, S05-W2-8 + S11-W2-3, S11-W3-2, `live` L6 at S11-W2-4 and S11-W3-5 |
| K6 | unattended daily-random-review stalls | S04-W2-1 (Not-for, fallback), OD8 owner edit, S04-W2-4 |
| K7 | a description edit drops a trigger | S12-W0-1, S12-W0-2 (lock, both repos), §5 lock table, S10-W0-9 and S21-W0-3 (verify on every commit), S12-W3-2/-3, S12-W4-2/-3, S12-W3-4, S12-W5-2, S04-W3-3 (re-key) |
| K8 | contract drift | S03-W2-4, S15-W2-5, S15-W2-6, S05-W2-1 (parity), S08-W3-1 (cross-repo check) |
| K9 | in-place loading runs uncommitted edits | S10-W0-10, S10-W0-11, S11-W3-3 (worktree advice), §0 rule 2 |
| K10 | `claude plugin eval` unavailable or noisy | S11-W0-9 (+ Bash-and-scaffold canary), S12-W0-6 (fallback), S12-W0-3 (pinned models, `--scaffold`), S12-W0-8 (W0 smoke baseline) |
| K11 | knowledge loss in the CLAUDE.md and atomize-book moves | S21-W4a-1, S21-W4a-4 (`move-blocks.mjs`, byte check), S21-W4a-3 (archive by script), S21-W4b-1, S19-W4-2…6 (move-proof `diff`), S19-W4-3b (renumber split from the move), S19-W4-9, S10-W3-10 (verbatim diff) |
| K12 | atomize-book churn during W4 | S19-W4-1 (freeze from S19-W4-2 until S19-W4-9), per-file steps S19-W4-2…8 back to back, S19-W4-9 |
| K13 | personal data in git or skills | S01-W3-4, S04-W3-1 (`state/` in a private repo); S03-W3-2, S03-W3-6 ("Klaeng" removed) |
| K14 | Windows CRLF, paths, PowerShell | S10-W0-1 (CRLF-safe), S15-W2-2 (drops PowerShell), S17-W1-3, S20-W1-1, S11-W3-2 |
| K15 | PDF tooling absent in cloud | S11-W0-5 (setup script), S11-W0-11, S13-W1-2, S17-W1-3/-9, S18-W1-3, S19-W1-7 |
| K16 | scope creep | §0 "stop and ask"; every step names its files |
| K17 | plugin hooks do not fire | S11-W0-7 (check b), S14-W2-1 skipped if b = no, S13-W1-4 |
| K18 | the W3 skeleton PR is large | S10-W3-1 + S10-W3-2 as one PR of three per-family commits, each green, reviewed with `git diff -M100% --stat --diff-filter=R`; S11-W3-5 |

## 7. Coverage

From the specs' §1.3 tables, re-parsed 2026-09-24 against `evidence/defect-index.txt`: **313 of 313 defects mapped, each once** (49 high, 131 medium, 133 low).

| Spec | S01 | S02 | S03 | S04 | S05 | S06 | S07 | S08 | S09 | S10 | S13 | S14 | S15 | S16 | S17 | S18 | S19 | S20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Defects | 16 | 14 | 14 | 25 | 27 | 16 | 15 | 14 | 14 | 27 | 5 | 35 | 12 | 19 | 17 | 10 | 14 | 19 |

S11, S12 and S21 own no inventory defects. By wave of the last closing step (planner count, before the critique pass): W0 21, W1 78, W2 112, W3 93, W4 6; 3 have no step. The critique pass named steps for validate.py-5 (S08-W3-1), route.py/ROUTING.md-4 (S10-W3-9), plugin-creator-12 (S10-W3-8) and gridgeist-4 (S10-W3-1); comprehensive-review-12 stays accepted as is. The `coverage.md` regenerated at W0 entry restates these counts.

HIGH defects (Appendix A), closing steps and wave. All close in their Appendix A wave.

| H | Closing step(s) | Wave | H | Closing step(s) | Wave |
|---|---|---|---|---|---|
| H01 | S01-W3-2 | W3 | H26 | S17-W1-7 | W1 |
| H02 | S01-W3-1, S01-W3-2 | W3 | H27 | S17-W1-9 | W1 |
| H03 | S01-W3-3, S01-W3-4 | W3 | H28 | S17-W1-8 (+ S18-W1-1, -2) | W1 |
| H04 | S01-W3-3 | W3 | H29 | S16-W2-2, S16-W2-3, S16-W2-4 | W2 |
| H05 | S01-W2-1 (+ callers S03-W2-1, S04-W2-1); S01-W3-1 | W2 | H30 | S16-W1-1 | W1 |
| H06 | S14-W2-2 | W2 | H31 | S16-W2-3, S16-W2-4 | W2 |
| H07 | S08-W1-1; root cause S08-W3-1 | W1/W3 | H32 | S18-W1-1, S18-W1-2 | W1 |
| H08 | S07-W1-1, S07-W1-3 | W1 | H33 | S18-W1-4, S18-W1-5, S18-W1-6 | W1 |
| H09 | S07-W1-1, S07-W1-3 | W1 | H34 | S13-W1-6 | W1 |
| H10 | S07-W1-2; S07-W2-4 | W1/W2 | H35 | S13-W1-1 … S13-W1-6 | W1 |
| H11 | S07-W1-2; S07-W2-4 | W1/W2 | H36 | S06-W1-1 | W1 |
| H12 | S09-W1-1 | W1 | H37 | S06-W1-1 | W1 |
| H13 | S10-W0-1 | W0 | H38 | S05-W2-3 | W2 |
| H14 | S14-W2-5 | W2 | H39 | S05-W2-1, S05-W2-3 | W2 |
| H15 | S15-W2-2 | W2 | H40 | S05-W2-4 | W2 |
| H16 | S15-W2-1, S15-W2-2, S15-W2-3 | W2 | H41 | S05-W2-4 | W2 |
| H17 | S14-W1-1, S14-W1-2 | W1 | H42 | S06-W1-2 | W1 |
| H18 | S14-W1-2 | W1 | H43 | S05-W1-1 | W1 |
| H19 | S14-W1-2 | W1 | H44 | S03-W2-1 | W2 |
| H20 | S14-W1-2 | W1 | H45 | S03-W3-2 | W3 |
| H21 | S19-W1-1 | W1 | H46 | S04-W1-1 | W1 |
| H22 | S19-W1-2 | W1 | H47 | S04-W1-1 | W1 |
| H23 | S19-W1-3 | W1 | H48 | S14-W2-4 | W2 |
| H24 | S19-W4-2 … S19-W4-7 | W4 | H49 | S14-W2-4 | W2 |
| H25 | S17-W1-1, S17-W1-3 | W1 | | | |

Per wave: W0 1, W1 26 (+ H07a, H10a, H11a), W2 16 (+ H10b, H11b), W3 5 (+ H07b, the root cause), W4 1. Total 49, matching Appendix A; `h-coverage.md` holds 52 lines because H07, H10 and H11 are split (critique C2-16).

## 8. Open questions

Each item names the check that settles it and the wave by which it must be settled. Q9–Q22 were spec fixes found while planning; the critique pass applied them (`critique-log.md`), and Q11 is now OQ16. Q23 lists spec-to-spec checks. Q24–Q29 are facts that critique repairs rely on and that no one could check from this session.

| # | Question | Check that settles it | Wave |
|---|---|---|---|
| Q1 | W0 checklist a–h (plugin dirs load; hooks fire; `renames`; eval enabled; rules load; `/doctor`; Windows CLI; setup-script timing) | S11-W0-7 … S11-W0-10 records in the delivery log | W0 |
| Q2 | Is `userConfig.learn_hub_root` readable by an env-var-loaded plugin? (S07 §8 Q1, U7) | S11-W0-7 check b (`option_probe_dir=`) | W0 |
| Q3 | Can a multi-repo session pick a branch per repo? (S11 §8.7) | S11-W0-7 row e; each step carries a fallback | W0 |
| Q4 | Do single-repo sessions clone to `/home/user/<repo>`? `/doctor` in web sessions? (S11 §8.12, §8.13) | S11-W0-7 rows a2, f | W0 |
| Q5 | `$schema` literal for plugin.json and marketplace.json (S10 §8.2, S14 §8) | `claude plugin init` / `marketplace init` in a scratch dir | W2 (S14-W2-1) |
| Q6 | Does the smoke runner accept a zero-case plugin (`learn-hub-session`)? LICENSE for a hooks-only plugin? (S14 §8) | run `eval.sh --smoke` on a scratch zero-case plugin; S08 VAL rules | W2 (S11-W2-4) |
| Q7 | Do `audit:visual` code names equal the I07-H strings? Can the CA swap be verified headless? (S05 §8) | S05-W2-1 parity vs S16-W2-2 output; S11-W2-3 `live` | W2 |
| Q8 | firecrawl vendor rename `ask` → `doctor`; gridgeist upstream commit (S09 §8.1, §8.5) | `firecrawl --help` or the CLI README; diff against upstream HEAD | W3 (S09-W3-1, -2) |
| Q9 | Closed: S10-W0-1 now expects exit 1 with one `yaml-error` FAIL; S10-W0-1b is the only seeder and expects exit 0 with one WARN (planner P-04). Original: S10-W0-1's done-when needs the ratchet entry that S10-W0-1b seeds later; S12-W0-1 and S10-W0-1b both seed it | — | W0 |
| Q10 | Closed: S09-W0-1 added; every seed step writes I17 `evals/<skill>/<case>/` with `tags: [smoke]` and §4.1 case names (planner P-01, P-02). Original: W0 seeds: S09-W0-1 is missing; S03/S04/S06/S07/S08 seed under `evals/smoke/<case>` (S04-W0-2 inside the skill dir), not I17 `evals/<skill>/<case>` — S12-W0-5's `*/evals/<unit>/*` finds none, and S10-W3-2 would merge same-named seed cases of several plugins into one family `evals/smoke/` | — | W0 |
| Q11 | Moved to OQ16. Original: micky has no repo-level CHANGELOG for tooling steps (S10, S11, S12) | — | W0 |
| Q12 | Closed: the two W2 contract checks are the W2 cross-repo gate; `validate.py --cross-repo` starts at S08-W3-1 (planner P-11). Original: The standard gate `validate.py --cross-repo` "from W2" has no implementation until S08-W3-1 | — | W2 |
| Q13 | Closed: S01-W3-7, S03-W3-8, S05-W3-6, S07-W3-2 added (planner P-05). Original: No release step for alignment, evidence, visuals after W3, nor for vault-keeper after S07-W3-1 (cx.md planned S01-W3-7, S03-W3-8, S05-W3-6) | — | W3 |
| Q14 | Closed: the nine release steps touch only `plugin.json` + CHANGELOG and check that `marketplace.json` has no version (planner P-16). Original: Nine W1/W2 release steps list `marketplace.json` in Files and keep "or S10's form if its W0 landed first" | — | W1 |
| Q15 | Closed: S19-W4-10 and S20-W2-5 added (planner P-06). Original: No step writes eval cases for atomize-book (S19) or vault-atomizer, vault-vectors, vectors, vault-coverage, check-repetition (S20); S12-W4-1 needs them | — | W2 (S20), W4 (S19) |
| Q16 | Closed: S17-W4-0 and S17-W4-5 added, OWNER on Windows (planner P-14, critique F14). Original: Architecture W4 exit "one article re-run end to end" has no step | — | W4 |
| Q17 | Closed: S04-W5-1, S07-W5-1, S12-W5-3 added (planner P-13). Original: W5 has no step for lit-watch usage, the OD4 revisit, emptying the ratchet with hard-fail checks, or the decision log | — | W5 |
| Q18 | Closed: S06-W3-1 uses `V/examples/` and depends on S05-W3-5; S18-W4-2 depends on S21-W4a-2 and points at the moved file (planner P-08, P-29). Original: Wrong paths or order in specs: S06-W3-1 uses `V/skills/clinical-infographic/examples/` (S10-W3-2 moves examples to `V/examples/`) and lacks a dependency on S05-W3-5; S18-W4-2 duplicates the gotchas S21-W4a-2 moves into `verify/references/gotchas.md` | — | W3, W4 |
| Q19 | Closed: S10 §1.3 names S08-W3-1 and S10-W3-9 (planner P-28). Original: validate.py-5 and route.py/ROUTING.md-4 name no step in S10 §1.3 | — | W3 |
| Q20 | Closed: S03-W3-2 and S03-W3-6 remove "Klaeng" (planner P-27). Original: K13: "Klaeng" in pubmed `references/decision-brief.md` and `evals/evals.json`; no step removes it | — | W3 |
| Q21 | Closed: S04-W2-5 added, OWNER (planner P-12). Original: OD8-a needs an owner edit of the synced `daily-random-review`; no spec step | — | W2 |
| Q22 | Closed: S13-W4-1 drops the size cap and uses `move-blocks --check` (planner P-10). Original: S13-W4-1 caps `sync-vault/references/gotchas.md` at 6 KB, but its six candidate headings measure 12,025 bytes verbatim (S21's map assigns 20) | — | W4 |
| Q23 | Spec-to-spec checks: S02 §8 Q1–Q3; S03/S04 ASSUMES on I01 field names; S21 §8 (skill-lint vs validate.py) | read S01 I01–I03 and S08 I19 before the step | W3 |
| Q24 | Does `apt-get install -y bubblewrap socat` succeed in the cloud setup script, and does a Bash-granted `claude plugin eval` run then pass? | S11-W0-9 canary (`$E/w0d2.json`) | W0 |
| Q25 | On Windows: which of `python3`, `python`, `py -3` runs; is npm's script shell cmd.exe; does `bash` exist for the plugin hooks? | S11-W0-10 check g toolchain lines | W0 |
| Q26 | Does a `claude -p` child started from `/home/user` load the same skills and CLAUDE.md files as a platform-started session? | S12-W0-6 check i | W0 |
| Q27 | Which learn-hub descriptions exceed 1,024 chars once their YAML parses (architecture §9 lists ingest-article at 1,137)? S21-W0-1's expected failure list depends on it. | the S21-W0-1 run | W0 |
| Q28 | On the owner's Windows machine, does `puppeteer.executablePath()` point to an existing browser (S13 `checkChromium` fallback)? | S11-W1-2 `node scripts/ready.mjs --json` | W1 |
| Q29 | Does a new micky cloud clone keep `core.hooksPath` from an earlier session (§0 rule 2 assumes it does not)? | `git -C /home/user/micky-psych-tools config core.hooksPath` in a new cloud session | W0 |
