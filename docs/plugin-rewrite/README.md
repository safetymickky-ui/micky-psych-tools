# Plugin rewrite — research, target architecture and execution plan

**Quality pass (2026-09-26):** S06-W1-1 done ahead of wave and S03-W3-2 partly done (K13) on branch `claude/pubmed-clinical-infographic-quality-ei2th0` — see `docs/rewrite/baseline.md` `## Owner records`.

**Status (2026-09-24):** phases 1–3 done. The owner confirmed the owner decisions and
answered the owner questions on 2026-09-24 (`plan.md` §1); the plan and the specs already
reflect the answers (Q33 answered (a) the same day). W0 executor steps are done on branch `claude/skill-plugin-rewrite-plan-cckyld` in both repos: micky S10-W0-1…10, S11-W0-1…3, S11-W0-8, S11-W0-9 (check d = yes), S12-W0-1, S12-W0-3, S12-W0-7 and the 7 smoke-seed steps; learn-hub S21-W0-1…3, S12-W0-2, S12-W0-4, S11-W0-4, S11-W0-6 (probe branch pushed), S12-W0-7 and the 3 smoke-seed steps; S12-W0-5 counts ≥3 for all 10 units. The W0 owner actions still ahead, in `plan.md` §4 order: merge the two W0 PRs; push the `pre-rewrite` tag from your own machine (S12-W0-0; the cloud session's git proxy refused the tag push with HTTP 403, so the tag exists only in that container), set up and check the cloud environment (S11-W0-5, S11-W0-7), confirm `claude plugin eval` (S12-W0-6), set the eval caps from the W0-d probe (S12-W0-9), run Windows check g (S11-W0-10), move the cloud to V1 (S11-W0-11) and tag `wave-0` (S12-W0-T).

**Scope:** every plugin and skill in both repos:
- micky-psych-tools: 14 plugins, 18 skills, 12 commands, `scripts/`, `ROUTING.md`,
  `CLAUDE.md`, `MEMORY.md`.
- learn-hub: the `learn-hub-local` marketplace (8 plugins, including forks of
  intent-lock, pubmed-research-note and comprehensive-review) and 11 project skills in
  `.claude/skills/`.

## What is here

| File | What it is |
| --- | --- |
| `plan.md` | **Start here to execute.** The execution plan: 296 change steps from the 21 specs (280 active, 16 dropped by the owner answers), in waves W0–W5, each with its dependencies, entry and exit gates, and rollback. §1 lists the owner decisions (OD1–OD14) and owner questions (OQ1–OQ16) with their answers; §4 lists the 42 owner-only steps. |
| `specs/S01…S21` | One rewrite spec per unit group: current state with measured descriptions, defects with `path:line` evidence, target frontmatter and body outline, scripts, handoffs, change steps (one commit each), eval cases with graders, acceptance criteria, trigger lock, risks, open questions. |
| `coverage.md` | Every one of the 313 defects → spec → fix step → wave. Generated; rebuild with `python3 phase3/gen_coverage.py evidence/defect-index.txt coverage.md`. |
| `critique-log.md` | The 89 findings of the plan critique and what happened to each (applied to a spec or the plan, or turned into an owner question). |
| `phase3/` | Support files for the specs: `interfaces.md` (the 27 cross-spec interfaces I01–I27 and their owners), `spec-template.md`, `eval-format.md` (the `claude plugin eval` format extract), `measure.py` (description and body metrics), `gen_coverage.py`. `phase3/reviews/` holds the review records: cross-spec consistency (`cx.md`), fact check, the two reconcile passes and the two critique lenses. Those records cite `phaseB/`, which is now `phase3/reviews/`. |
| `architecture.md` | The design the plan implements. The target architecture. It covers topology and delivery per environment, a disposition for every unit, the cross-repo pipeline contract, evals, versioning, context budgets, migration waves W0–W5, owner decisions OD1–OD14 and risks. Appendix A maps all 49 HIGH defects to a wave. |
| `rubric.md` | 92 authoring rules (R1–R92), each with its source claim ids, how it is enforced, and MUST/SHOULD. It also lists the conflicts between sources and where the repos' conventions diverge from the rules. |
| `proposals/` | The three competing architectures the synthesis was built from: purist, risk-first, workflow-first. |
| `evidence/claims-digest.txt` | 259 best-practice claims. Each has a source URL and quote, and an adversarial check verdict: 228 confirmed, 30 partial with corrected wording, 1 refuted. |
| `evidence/defects-digest.txt`, `defect-index.txt` | 313 inventory defects (49 high, 131 medium, 133 low), each with file:line evidence. |
| `evidence/phase1-results.json` | Raw phase-1 output: research claims plus verification, and the inventory. |
| `evidence/phase2-judges.json` | The rubric summary, the two judges' scores and graft lists, and the synthesis summary. |

The documents cite `wf1/` and `wf2/`. Those were the working directories: `wf1/` is
now `evidence/phase1-results.json`, and `wf2/` is this folder.

## How it was made

1. **Research** in five dimensions: official skill authoring, plugin/marketplace
   structure, evals (`claude plugin eval`, skill-creator), community exemplars, and this
   repo's own conventions. Each dimension was followed by an independent agent that
   re-opened every source to check the quote and the claim.
2. **Inventory** of every unit in both repos, in six groups, with measured description
   lengths, body sizes, cross-plugin dependencies, forks and diffs, and defects.
3. **Rubric**, then **three independent architecture proposals**, then **two judges**
   who spot-checked each proposal's facts (19 errors found and fixed), then **a
   synthesis**.

## Headline findings

- **Nothing from either marketplace loads in the cloud multi-repo sessions you use.**
  `claude plugin list` returns "No plugins installed", and only the claude.ai-synced
  skills load. The learn-hub catalog is not registered in any environment. In a
  multi-repo session, learn-hub's `.claude/settings.json` hooks do not load either.
- **The forks and cross-repo contracts are broken in both directions.** Examples:
  empty-vault looks for a deleted `digest-report` directory, the report `## Sources`
  format does not match digest-report's input contract, and callers expect intent-lock
  fields that were removed in 0.3.0.
- **Current Claude Code guidance diverges from the repo conventions.**
  - Commands are merged into skills.
  - The docs advise setting a version in `plugin.json` only, never in both files.
  - `claude plugin eval` uses `evals/<case>/prompt.md` plus graders. The 118 existing
    `evals.json` cases all have `assertions: []`, and none has ever run.
  - The skill listing shares a budget of 1% of the context window, and most
    descriptions sit at the 1,024-character cap.
- **Two renderers still carry layout bugs that learn-hub already fixed downstream.**
  concept-animation and ml-concept-lab still prescribe the `100dvh` stage collapse, and
  clinical-infographic still ships a dark-mode block.

## Owner decisions

The architecture and the specs assume the recommended option for each of OD1–OD14
(`architecture.md` §11). The ones that change the most:
- **OD1/OD2:** how plugins reach cloud and Windows sessions. The recommendation is the
  `CLAUDE_CODE_PLUGIN_DIRS` environment variable.
- **OD3:** whether to merge plugins into the families `alignment`, `evidence` and
  `visuals`.
- **OD5:** publishing to Supabase is opt-in.
- **OD7:** rename micky's `psych-paper-digest` to `lit-watch` to end the name collision
  with the claude.ai skill.
- **OD9:** slash names survive as alias skills.

The plan critique added ten owner questions (OQ7–OQ16) on top of the six from the specs.
The ones that change the most work:
- **OQ7:** branch model. One short branch per spec block, merged to master when green
  (recommended), or one branch per wave.
- **OQ11:** eval run counts. About 1,140 live-trigger runs and 1,380 release runs at the
  architecture's counts; the recommendation cuts most re-runs.
- **OQ12:** load Windows plugins in place from W1. This drops 12 interim release steps and
  two Windows install-refresh steps.
- **OQ13:** build the visual audit once (in learn-hub) instead of twice.
- **OQ15:** cut or defer two vault-keeper scripts for a vault of 16 files.

## Phase 3 — how the plan was made

1. **Specs.** 21 specs were written in parallel against a fixed template
   (`phase3/spec-template.md`) and an interface registry (`phase3/interfaces.md`). Each
   claim about today's files was re-opened in the repo, and each description was measured
   with `phase3/measure.py`.
2. **Checks.** One agent checked consistency across the specs (62 findings). One
   fact-checked them against both repos (10 findings). Two agents applied both lists to
   the specs.
3. **Plan.** One agent ordered every step into waves and checked that each step id
   appears exactly once.
4. **Critique.** Two independent critics reviewed the plan and the riskiest specs. One
   covered goal fit, completeness, verifiability and hidden assumptions (22 findings).
   The other covered sequencing, feasibility, risk and simplicity (31 findings). A repair
   agent then handled 89 findings: the critics' 53, the planner's 35 and one left over
   from reconciling. It applied 77 to the specs or the plan and turned 12 into owner
   questions. Three were partly rejected; the log gives the reason for each.
5. **Final checks:**
   - 285 step ids are defined, and each is in `plan.md` §3 exactly once.
   - No reference to a step id is dangling.
   - All 313 defects map to a spec, and all 49 HIGH defects have a closing step.

Known limits:
- Line numbers in the specs were true on 2026-09-24. Other sessions keep editing
  learn-hub, so the plan's §0 rule 3 tells the executor to locate quoted text when a
  line number has moved.
- `specs/S11-delivery-environment.md` is about 90 KB, over the 40 KB spec target. It
  was checked by the consistency, fact-check and critique passes, but it had no
  dedicated spec-level verification.
- §8 of the plan lists the facts that could not be checked from a cloud session
  (Windows behaviour, environment settings). Each names the check that settles it.

## How to execute

1. Do the W0 owner actions as their rows come up (`plan.md` §4); the ODs and OQs are answered.
2. Run the steps of W0 in table order. For each step, open its spec at the step id and
   follow its files, commands, done-when and rollback. One step is one commit in one
   repo.
3. Close a wave only when its exit gates pass (the standard gates in `plan.md` §3, plus
   the wave's own). Then move to the next wave:
   W0 → W1 → W2 → {W3, W4} → W5.
