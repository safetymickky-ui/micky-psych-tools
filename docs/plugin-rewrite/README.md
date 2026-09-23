# Plugin rewrite — research and target architecture (work in progress)

**Status (2026-09-23):** phases 1–2 of 3 done. Paused at the owner's request, before
phase 3. **This folder is NOT the plan yet.** It holds the evidence and the target
architecture that the plan will be built from.

**Scope:** every plugin and skill in both repos:
- micky-psych-tools: 14 plugins, 18 skills, 12 commands, `scripts/`, `ROUTING.md`,
  `CLAUDE.md`, `MEMORY.md`.
- learn-hub: the `learn-hub-local` marketplace (8 plugins, including forks of
  intent-lock, pubmed-research-note and comprehensive-review) and 11 project skills in
  `.claude/skills/`.

## What is here

| File | What it is |
| --- | --- |
| `architecture.md` | **Start here.** The target architecture. It covers topology and delivery per environment, a disposition for every unit, the cross-repo pipeline contract, evals, versioning, context budgets, migration waves W0–W5, owner decisions OD1–OD14 and risks. Appendix A maps all 49 HIGH defects to a wave. |
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

## Owner decisions to make before phase 3

These are OD1–OD14 in `architecture.md` §11. The architecture assumes the recommended
option for each, and says what changes if you pick differently. The ones that change
the most:
- **OD1/OD2:** how plugins reach cloud and Windows sessions. The recommendation is the
  `CLAUDE_CODE_PLUGIN_DIRS` environment variable.
- **OD3:** whether to merge plugins into the families `alignment`, `evidence` and
  `visuals`.
- **OD5:** publishing to Supabase is opt-in.
- **OD7:** rename micky's `psych-paper-digest` to `lit-watch` to end the name collision
  with the claude.ai skill.
- **OD9:** slash names survive as alias skills.

## Phase 3 (not started)

1. Write per-plugin rewrite specs from `architecture.md`. Each spec covers the new
   description (measured), the body outline (keep / cut / move to references / convert
   to script), the defects it fixes, the eval cases with graders, and acceptance
   criteria. Then adversarially verify each spec.
2. Assemble the execution plan, run an adversarial critique pass, and commit it here.
