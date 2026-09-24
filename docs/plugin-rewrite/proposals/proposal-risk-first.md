# Proposal: risk-first incremental rewrite of micky-psych-tools + learn-hub plugins and skills

Angle: **risk-first incremental**. Basis: phase-1 evidence in `scratchpad/wf1/` (research claims SKL/PLG/EVL/COM/LOC with verifier verdicts; `partially` claims used in their corrected wording; LOC-26 refuted and unused) and the six inventories (313 defects, 49 HIGH). HIGH defects are numbered H01–H49 in the order the inventories list them (§4 maps every one). Date 2026-09-23, Claude Code 2.1.280.

Mechanisms checked in this session beyond the research files (Appendix A): `CLAUDE_CODE_PLUGIN_DIRS` loads plugins in place, accepts a folder of plugins, and reports a missing path without blocking the others (run locally on CLI 2.1.280). A declared plugin `dependencies` entry **disables** the dependent plugin when the dependency is missing (docs, `plugin-dependencies.md`). Multi-repo cloud sessions **do not run** a repo's `.claude/settings.json` hooks (docs, `cloud-environments.md`). `disable-model-invocation: true` on a command file passes `claude plugin validate --strict` (scratch copy).

---

## 1. Thesis

**Most of the 49 HIGH defects are broken seams between units, not bad writing inside one unit.** They sort by primary cause (§4 has the per-defect list):

| Class | HIGH defects | Count |
|---|---|---|
| A. Contract broken between units or repos, including fixes that never propagated between forks | H05 H06 H10 H11 H15 H29 H31 H36 H37 H38 H39 H40 H44 H48 H49 | 15 |
| B. Delivery, state or path: the unit doesn't load, or it resolves the wrong place | H03 H07 H08 H09 H14 H16 | 6 |
| C. Production-write or destructive hazard | H17 H18 H20 H25 | 4 (H09, H11 and H49 also write or delete) |
| D. Instruction inside one unit that is wrong, stale or can't be executed | H01 H02 H04 H12 H13 H21 H22 H23 H26 H27 H30 H33 H34 H35 H41 H42 H43 H45 H46 H47 | 20 |
| E. Routing collision | H19 H28 H32 | 3 |
| F. Size | H24 | 1 |

Classes A and B cover 21 of the 49. No amount of rewording fixes them. They need three things: one owner per contract, a delivery route that actually loads the unit, and a mechanical check that the two sides still agree. Class D needs targeted edits, mostly deletions. Only one HIGH defect is about size alone. A ground-up rewrite of 30+ skills would therefore spend most of its risk on the part that is least broken.

**Two observed facts set the order of work.**

1. **In cloud sessions nothing from either marketplace loads.** `claude plugin list` shows "No plugins installed" (LOC-42). The learn-hub-local catalog is registered nowhere (H14; `learn-hub/.claude/settings.json` holds hooks only). Every "mandatory Step 0 intent-lock", "hand to vault-keeper" and "run digest-report" instruction therefore dead-ends silently in the cloud (COM-37).
2. **The units that do load today carry the destructive defects.** The learn-hub project skills load everywhere, and the micky plugins load on Windows at user scope. Examples: ingest-article's bare invocation ingests and then deletes PDFs in a folder that isn't gitignored (H25). sync-vault's default path is `npm run sync` plus a nested layout (H34, H35). empty-vault deletes assets that have receivers (H11). vault-keeper's walk-up can resolve learn-hub's `vault/` (H09). So the first work is stopping active harm in units that load. Turning delivery on comes second, and each plugin is switched on only after it is fixed.

**Architectural stance: the smallest set of moves that closes every HIGH defect.**

- **micky-psych-tools is declared a *load-in-place* marketplace.** On Windows it installs as a local-directory marketplace (PLG-09, LOC-39). In the cloud it loads through `CLAUDE_CODE_PLUGIN_DIRS` pointing at the clone (PLG missed practice; verified locally, Appendix A). Once in-place loading is the precondition, `${CLAUDE_PLUGIN_ROOT}/../..` is the repo root. vault-keeper's vault (H08, H09), plugin-creator's scripts (H07) and the misread ledger (H03) then resolve to the git checkout in every environment. Each of those skills gets a guard that detects a cached copy (the path contains `/plugins/cache/`) and stops instead of writing into the cache (PLG-22, PLG-24).
- **learn-hub's repo-bound plugins become plain project skills** (`.claude/skills/`). Project skills are the one surface that demonstrably loads in every session type (observed in this session; cloud carry-over table: ".claude/skills/, .claude/agents/, .claude/commands/ — Yes", PLG-47). The five native plugins call repo scripts by relative path anyway, so packaging bought only namespacing (learnhub-plugins group observation).
- **The three learn-hub forks are retired, not maintained.** Upstream gains a small per-repo output-sink adapter: one committed JSON file in learn-hub. The forks never load anywhere (H14), their evals fail by construction (H48), and one of them syncs to live Supabase by default (H49). Their only real delta is the filing path (LOC-33).
- **Shared contracts are copied byte-for-byte with parity checks, not referenced by path.** Cached plugins can't read `../` (PLG-22, COM-38), symlinks don't survive Windows checkouts or `--plugin-dir` copies reliably (PLG-23), and Anthropic's own docx/pptx skills duplicate shared files byte-identically (COM-39). learn-hub already uses "byte-identical twin + parity test" for mermaid-split and tag-canon.

**What we deliberately do NOT change, and why**

| Keep as is | Reason |
|---|---|
| All 14 micky plugin names, 17 skill names, 12 slash-command names (`/digest`, `/animate`, `/infographic`, `/visualize`, `/explain-code`, `/critique-plan`, `/resolve-decisions`, `/new-plugin`, `/refine-plugin`, `/route`, `/empty-vault`, `/comprehensive-review`) | These are the owner's typed habits. A plugin's name is its stable identifier, and renaming needs a `renames` map (PLG-44). No HIGH defect requires a rename. |
| Every quoted trigger phrase, Thai phrases verbatim | Descriptions are the only routing signal (SKL-12). A generated trigger-lock (§6) makes dropping a phrase a validator failure. |
| No plugin merges (e.g. no single "alignment" plugin) | A merge needs `renames`, reinstalls and re-learning. Shared text is handled by copy + parity instead (§5). |
| Dual-file version rule and bump.py's dual write | The docs advise against it because a stale plugin.json can mask the entry (PLG-06). Here bump.py plus validate.py plus `validate --strict` (LOC-03) make drift mechanically impossible. Changing it buys conformance, not safety. |
| Three identical `.mcp.json` files (pubmed-research-note, comprehensive-review, psych-paper-digest) | Plugin MCP servers and connectors are deduplicated by endpoint, so only one connection is made (PLG missed practice). Moving the servers into one plugin would force a `dependencies` entry, and that **disables** the dependent plugin whenever the dependency is absent (Appendix A). Fix the hard-coded tool prefix instead (§5.4). |
| No plugin.json `dependencies` anywhere | Same reason: a declared dependency turns "Step 0 skipped" into "whole research plugin disabled" (`dependency-unsatisfied`). Soft handoffs plus a stated fallback degrade better (COM-37). |
| skill-creator `evals/evals.json` files (118 cases) | They are harmless prompt inventories that ship inert (EVL-47). Selected cases are converted into `claude plugin eval` cases rather than deleted (§6). |
| ROUTING.md and route.py (demoted, not deleted) | `/route` is a habit. The generated table stays useful to a human. Only the "consult before any request" mandate goes (LOC-09). |
| No `when_to_use` field; descriptions stay ≤1024 chars | The field is Claude Code-only (SKL-04), and neither the house parser (LOC-06) nor claude.ai sync would read it. Freeing room by cutting procedure text out of descriptions is lower risk. |
| atomize-book's Python scripts stay where they are | 354 passing tests, ingest-article's call paths and CLAUDE.md commands all depend on those paths. Moving them to a neutral home is churn with no HIGH defect behind it. |
| gridgeist (vendored) content | It has no HIGH defect. Record the upstream commit only. |
| Skill bodies without HIGH defects are not re-voiced | Voice and style churn invalidates the owner's mental model without fixing anything (COM-21). |

---

## 2. Target topology

### 2.1 Ownership: one owner per job

| Job | Owner (repo : unit) | Consumers that hand off by skill name |
|---|---|---|
| Decision-shaped evidence report | micky : `pubmed-research-note` | psych-paper-digest (Act items), pk-plasma-animation (research brief), plan-critique (evidence questions) |
| Whole-topic review | micky : `comprehensive-review` | clinical-infographic / concept-animation (generate-first), claude.ai `daily-random-review` (chains by name) |
| Watchlist surveillance | micky : `psych-paper-digest` (local only, §2.3) | none |
| Pre-build alignment / mid-task decisions / plan critique / misread capture | micky : `intent-lock`, `decision-interview`, `plan-critique`, `misread-capture` | pubmed-research-note, comprehensive-review, concept-animation, ml-concept-lab, code-explainer, firecrawl Path C |
| Static clinical sheet / watch-only animation / explorable / code explainer / UI design | micky : `clinical-infographic` / `concept-animation` (the **only** copy) / `ml-concept-lab` / `code-explainer` / `gridgeist` | none |
| General-web fetch engine | micky : `firecrawl` | research writers |
| micky vault: file, index, query | micky : `vault-keeper` | all micky producers |
| Drain micky vault into learn-hub | micky : `empty-vault` → learn-hub `digest-report` (reports), `ingest-infographic`, `ingest-animation` (assets) | none |
| Marketplace tooling | micky : `plugin-creator`, `refine-plugin`, `scripts/{validate,route,bump,sync_shared,health}` | none |
| Front door for any PDF | learn-hub : `pdf-pipeline` → `ingest-article` / `ingest-slides` / `atomize-book` | none |
| Report → atomic notes | learn-hub : `digest-report` (project skill again) | empty-vault, micky producers via sink adapter on "atomize" |
| Asset filing into the hub | learn-hub : `ingest-infographic`, `ingest-animation` | empty-vault, micky renderers via sink adapter, pk-plasma-animation |
| **Sync / revalidate / verify tail** | learn-hub : `sync-vault` (**sole owner**; the other 7 skills link here instead of restating it) | all learn-hub writers |
| Corpus maintenance | learn-hub : `vault-atomizer`, `vault-vectors`, `vault-coverage`, `check-repetition`, `verify` | none |
| Drug PK animation builder | learn-hub : `pk-plasma-animation` (project skill) | none |
| Shared contracts (report format, alignment interview, HTML artifact, vault handoff) | micky : `shared/` canonical copies; generated copies in consumers; learn-hub copies checked across repos | see §5 |

### 2.2 Pipeline after Wave 2

```
micky producers ──(sink resolved per repo: .output-sink.json absent → micky default)──┐
  pubmed-research-note, comprehensive-review, clinical-infographic,                   │
  concept-animation, ml-concept-lab                                                   │
                                                                                      ▼
 [micky default] vault-keeper → micky vault/{artifacts,assets}        [learn-hub] research-notes/ (reports)
            │                                                          │   ingest-infographic / ingest-animation (assets)
            ▼ /empty-vault (move → verify → delete, double-gated)       ▼ "atomize"
   reports → digest-report ─┐   assets → ingest-infographic / ingest-animation
                            ▼                     ▼
                     learn-hub /vault ──> sync-vault (sync:apply, background, gates) ──> Supabase ──> app
```

Both routes exist today. Collapsing them into one is an owner decision (§10, D3), not a precondition.

### 2.3 Delivery route per environment

| Environment | micky plugins | learn-hub skills | Notes and evidence |
|---|---|---|---|
| Local Windows, any cwd | User-scope **local-directory** marketplace, loaded in place | none | Wave 0 confirms the source type (`claude plugin marketplace list`). If it is GitHub-sourced (cached copies), switch it (§10, D1). In place: edits apply with no bump (PLG-09). |
| Local Windows, cwd in learn-hub | Same as above | `.claude/skills/*` (14 skills after W3) and `.claude/commands/` aliases | Hooks run (single repo). |
| Cloud, multi-repo (starts at `/home/user`, the owner's normal mode) | `CLAUDE_CODE_PLUGIN_DIRS` on the cloud environment, one absolute path per **enabled** plugin (`/home/user/micky-psych-tools/plugins/<p>`), extended wave by wave | `.claude/skills/*` load (observed in this session) | Project/local settings can't set the variable; an environment variable can (plugins.md L317). Loads as `<name>@inline`, in place (Appendix A). **Hooks and settings.json are not read** in multi-repo sessions (cloud-environments.md L261, L468). learn-hub's SessionStart and pre-sync gates don't run, so sync-vault must check its own preconditions (§9, W1). |
| Cloud, single-repo learn-hub | Same variable; micky paths report "Path not found" and nothing else happens (Appendix A) | `.claude/skills/*` | learn-hub hooks run. |
| Cloud, single-repo micky | Same variable | none | none |
| `claude plugin eval` | Plugin directory target | Throwaway plugin wrapped around the project skill (§6.3) | Runs are isolated: no CLAUDE.md, no other plugins (EVL-19). |
| claude.ai-synced skills (`anthropic-skills:*`) | Unchanged | Unchanged | Collision rules: SKL-55. psych-paper-digest is handled in §10 D4. |

**Why not claude.ai account sync for micky in the cloud.** Synced plugins are downloaded copies (`~/.claude/plugins/synced/`), not in place. They also sync into terminal sessions, where the local marketplace copy wins and the synced one is reported "not loaded" (plugins-reference L454). The ledger and vault-in-git stance would then fail in the cloud. It remains the fallback if the Wave 0 cloud test of the environment variable fails.

**Why not `extraKnownMarketplaces` for learn-hub.** Cloud sessions don't install repo-enabled plugins, and multi-repo sessions don't read settings.json at all (PLG-47 corrected; cloud-environments.md L265).

**Why not `@skills-dir` plugins in learn-hub.** They load only from the *primary working directory's* `.claude/skills/` (plugins-reference L413). In multi-repo sessions that directory is `/home/user`, so they would not load.

### 2.4 The one handoff sentence every caller uses

Callers name partners by skill name and always state a fallback (COM-36, COM-37). No `@` paths and no hard dependencies. The canonical text lives in `shared/contracts/alignment-interview.md` §Handoff:

> Run the `<partner>` skill. If it isn't available in this session — or it needs an interactive picker and none exists here (subagent, headless, scheduled run) — do not stall: take the broadest reading that fits the request and open the output with one line `Assumed: <reading> — say if wrong.`

---

## 3. Disposition table (every unit)

Waves are defined in §9. "dmi" means adding `disable-model-invocation: true` to a thin command file. That keeps the slash name the owner types and takes the command out of Claude's routing listing (SKL-36; command files accept the field, SKL-01; verified to pass `--strict`, Appendix A).

### 3.1 micky-psych-tools plugins (14)

| Plugin | Disposition | Wave | Target | Reason (evidence) |
|---|---|---|---|---|
| pubmed-research-note | keep | W2 | plugins/pubmed-research-note | The name, triggers and `.mcp.json` stay. Its skill is fixed in place (below). It is the upstream that replaces the learn-hub fork (LOC-33). |
| intent-lock | keep | W3 | plugins/intent-lock | Two skills are rewritten (below). The plugin shell stays, because 5+ callers name it. |
| plugin-creator | keep | W1 guard, W3 rest | plugins/plugin-creator | H07 is fixed by an in-place root guard, not by moving it: the commands are habits and it only ever worked inside the repo. Converting it to a project skill was considered and deferred, since that needs a `renames: null` and gains nothing. |
| vault-keeper | keep | W1, W2, W4 | plugins/vault-keeper | Root resolution fix (H08, H09). empty-vault rewired (H10, H11). Index job becomes a script in W4. |
| psych-paper-digest | keep | W1, W3 | plugins/psych-paper-digest | Search recipe fixes (H46, H47). Local-only delivery: its `last_swept` state lives in cwd, which is ephemeral in the cloud, and a cloud copy would collide with `anthropic-skills:psych-paper-digest` (§10, D4). |
| comprehensive-review | keep | W2 | plugins/comprehensive-review | Targeted skill fix plus the sink adapter. It replaces the learn-hub fork (H49). |
| clinical-infographic | keep | W1, W2 | plugins/clinical-infographic | Template light-lock and strip stacking (H36, H37). Filing via the asset handoff (W2). |
| firecrawl | keep | W1 refresh, W4 split | plugins/firecrawl | Stale vendor text (H12). Body split into a slim router plus a dated vendor reference. |
| concept-animation | keep | W2 | plugins/concept-animation | Becomes the **single** owner. The learn-hub copy's layout fixes are merged in (H38, H39, LOC-34). |
| code-explainer | keep | W1 | plugins/code-explainer | Dangling template pointer removed (H42). |
| ml-concept-lab | keep | W2 | plugins/ml-concept-lab | Layout rule and verify recipe (H40, H41). |
| plan-critique | keep | W3 | plugins/plan-critique | Light consistency edits. No HIGH defect. |
| decision-interview | keep | W3 | plugins/decision-interview | Light edits plus the missing evals, README and CHANGELOG. No HIGH defect. |
| gridgeist | keep | W3 | plugins/gridgeist | Vendored. Record the upstream sha, add it to CLAUDE.md inventory, leave content alone. Exclude from cloud delivery unless used (listing budget). |

### 3.2 micky-psych-tools skills (18 SKILL.md files, including the plugin-creator template)

| Skill | Disposition | Wave | Change (smallest that closes the defects) | Evidence |
|---|---|---|---|---|
| pubmed-research-note | rewrite (targeted) | W2 (content), W4 (size) | Replace the `Assumed / Reframed / Skipped` preface with the single `Assumed:` line. Delete the "reframe governs" rule. Fix decision-brief slot arithmetic (3 fixed by the interview + 3 derived). Resolve MCP tools at runtime (§5.4). Output-sink adapter. Report filename slug rule, with nothing written to a non-repo cwd. Sources/NCT grammar from `shared/contracts/report-format.md`. PMID contradiction in atomic-note-template. Remove "Klaeng". NOT-for names the claude.ai daily digest precisely. Standard handoff/fallback sentence. W4: dedupe the opt-out (×4) and depth contract (×4) and trim mandatory reads. | H44 SKILL.md:263 vs intent-lock SKILL.md:226; H45 decision-brief.md:11-12, intent-lock-pairing.md:49-57; tool-catalog.md:25-28; atomic-note-template.md:23 |
| intent-lock | rewrite (by subtraction) | W3 | Delete the 11 contradictory "say/show/state" lines and the "read it as compute silently" patch (L22). Name AskUserQuestion's real mechanics: 1–4 questions, 2–4 options, `multiSelect`, automatic "Other"; drop `rank_priorities` and the manual escape. Add the picker-unavailable/errored fallback. Delete the unobservable "silence/abandoned picker" rules. Remove version-history narration. Fix the loop-guard logic. Resolve "craft my prompt" (the prompt as deliverable is allowed when the user says the prompt is the output). Load failure-conditions.md explicitly at the gate check. Cut procedure from the description. Ledger write rules move to misread-capture. | H01 SKILL.md:16,22 vs :49,:67,:93,:155,:166-167,:193,:196,:206; H02 :136,:160-162,:189-190 |
| misread-capture | rewrite | W3 | Two questions become (1) "what did you want instead" → `Axis missed`, and (2) "what should I check next time before starting" → `Prior`. Both are the user's words, so there is no third question and no drafting. Ledger location is the in-place repo file with a cached-copy guard. Offer a commit after appending. Newest-first order, as the file already is. Retirement only by user choice. Either implement "review/edit priors" as a listed mode or delete the promise. | H04 SKILL.md:26,:30-35,:47,:50,:55; H03 SKILL.md:39 |
| plugin-creator | rewrite (targeted) | W1 guard, W3 | W1 Step 0: the repo root is `${CLAUDE_PLUGIN_ROOT}/../..` only if its `.claude-plugin/marketplace.json` has `"name": "micky-psych-tools"`; otherwise stop. W3: third-person description; Not-for routes to refine-plugin; scaffold writes README, CHANGELOG and one `evals/<skill>/trigger-basic/` case; hooks template uses `${CLAUDE_PLUGIN_ROOT}` exec form; stdio MCP allowed. | H07 SKILL.md:9-10, guard :47-51; LOC-21, LOC-22 |
| refine-plugin | rewrite (targeted) | W3 | Bump goes through bump.py, which now writes the CHANGELOG stub. Third-person description. Checklist aligned with validate.py (README/CHANGELOG/evals become mechanical checks). | refine SKILL.md:58-68 vs audit-checklist.md:67-68 |
| plugin-creator/references/templates/SKILL.md | rewrite | W3 | Placeholders become quoted strings so the template is valid YAML. validate.py fails on leftover `{{` outside `templates/`. | templates/SKILL.md:2,:8 (PyYAML ConstructorError) |
| vault-keeper | rewrite (targeted) | W1, W4 | Step 0 order: (1) in-place root if the marketplace name matches; (2) walk up from cwd to a marketplace.json **named micky-psych-tools**; (3) otherwise stop and ask. Remove the claim that `${CLAUDE_PLUGIN_ROOT}/../../vault` is always equivalent. "Four jobs" → five. Add `asset` save rules plus a `source` field for the asset handoff. W4: index rebuild and orphan report as `scripts/vault_index.py`. | H08 SKILL.md:29, vault-layout.md:7; H09 SKILL.md:28 + learn-hub marketplace name `learn-hub-local` |
| empty-vault | rewrite (targeted) | W1 stopgap, W2 | W1: never delete assets; list them as "held — no verified receiver". Learn-root detection keys on files that exist in every wave: env `LEARN_HUB_DIR`, then a sibling of the micky root containing `scripts/apply-sync.mjs` + `.claude/skills/sync-vault/SKILL.md`, otherwise ask. Separately, check that digest-report is available (true from W2). Drop the Windows literal. W2: hand assets to `ingest-infographic` / `ingest-animation` by the vault `source` field and wait for their handshake before deleting. Notes are passed under digest-report's new "supplementary" input slot. | H10 SKILL.md:36-37; H11 SKILL.md:54-57 vs ingest-infographic SKILL.md:3,:136-137 |
| psych-paper-digest | rewrite (targeted) | W1, W4 | W1: `datetype: edat` on the MCP path. Paginate with `retstart` to exhaustion, capped per domain, and put the unscreened count in the header when the cap bites. CT.gov: `AREA[...]RANGE` date filter, and "has results" read from details. Dedup against every digest whose window overlaps, not only the newest. Vault discovery via vault-keeper's resolution. Explicit timezone (UTC+7). NOT-for boundary against the claude.ai daily digest. W4: window math, config and dedup become a script. | H46 sweep-recipes.md:39-40 vs :49; H47 :39-40 vs :92-93 |
| comprehensive-review | rewrite (targeted) | W2 | Reconcile the number rule with thin domains (thin domain = one sourced sentence naming what exists). Engine-failure policy copied from the shared report contract. "Source floors" → "evidence types". Replace the "house rules" pointer with the shared contract. Output via the sink adapter. `Assumed:` line. Handoff fallback. Eval for the Thai trigger. | inventory research-writers CR defects (SKILL.md:132-133, :103-124, :128) |
| clinical-infographic | rewrite (targeted) | W1, W2 | W1: remove the `prefers-color-scheme:dark` block and add `:root{color-scheme:light}` in template and example. Stack `.mech` on mobile. Fix header contrast (darken c2/c3). Enforce the ≥12px minimum in the template. W2: render/verify runs the shared HTML checker; asset handoff; `lessons-learned.md` moves to CHANGELOG history; SKILL points at the example. | H36 template:100-104; H37 template:74-75,:93 (learn-hub auditInfographicResponsive flags both) |
| firecrawl | rewrite + split | W1, W4 | W1: refresh the vendor text from firecrawl.dev (build skills need `firecrawl setup build`; `ask`→`doctor`; keyless scope is `/search/research/*` only) and stamp `fetched: 2026-09-23 <url>`. Gitignore `.env` and `.firecrawl/`. W4: slim router body (marketplace contract, credentials hygiene, path table) plus `references/vendor-guide.md` loaded on demand. | H12 SKILL.md:146-147,:127,:330 |
| concept-animation | rewrite (merge) | W2 | Take learn-hub's layout grammar and verify step: `min-height:100dvh`, `.wrap>*{flex:0 0 auto}`, stage floor `max(220px,min(38dvh,280px))` (the app guard's value, not the bare `min()`), full document plus color-scheme, **five** viewports including 844×390, sort-by-top overlap check. Keep micky's pipeline discipline (Handoffs, Close, Failure conditions, generate-first sourcing, third-person description). Source precedence adds "a learn-hub /vault note". Filing goes through the sink adapter to ingest-animation. Reciprocal NOT-for with ml-concept-lab. SKILL points at the (fixed) example. | H38 animation-grammar.md:46,:48; H39 SKILL.md:145-150; LOC-34 |
| code-explainer | rewrite (targeted) | W1, W4 | W1: remove every pointer to the nonexistent `explainer-template.html` and example (SKILL.md, README, CLAUDE.md) and say "build from vscode-shell.md + explanation-contract.md". validate.py dead-link check. W4 (optional, eval-gated): add the template. Theme name "Dark Modern". ml-concept-lab boundary. | H42 SKILL.md:67-68,:136; README.md:86-88 |
| ml-concept-lab | rewrite (targeted) | W2, W4 | Same layout port as concept-animation. The verify recipe becomes the shared checker, which resolves Playwright via `createRequire(npm root -g)`, runs five viewports and keeps `executablePath` from the environment. Gradient check uses absolute difference with a noise floor. Clinical concepts route to concept-animation (fixes the description contradiction). Example path via `${CLAUDE_PLUGIN_ROOT}/examples/`. W4: body ≤3.5k tokens. | H40 build-contract.md:140-141; H41 :195-197,:202 |
| plan-critique | rewrite (light) | W3 | Command and skill agree on the no-plan case (route to intent-lock and draft). Split the 807/854-char mega-bullets. Adopt the shared silence vocabulary. Add a misread-capture carve-out. Lens names match the reference. Trim the lens list from the description. | critique-plan.md:10-11 vs SKILL.md:24; SKILL.md:30,:50 |
| decision-interview | rewrite (light) | W3 | Unprompted trigger keeps "above-threshold". Fallback on picker error or absence. Shared silence vocabulary. Add evals, README, CHANGELOG. | SKILL.md:3 vs :15,:43; :81 |
| gridgeist | keep | none | No change to content. Record the upstream sha in the README. Leave `agents/openai.yaml` alone: it is inert, and removing it diverges from upstream. | renderers inventory (low only) |

### 3.3 micky-psych-tools commands (12)

All keep their names. Each becomes (a) dmi, so it is user-only and absent from Claude's listing, and (b) consistent with its skill. Nothing in the rewrite needs Claude to invoke a command. The "run /route" and "run /new-plugin" mandates are removed from CLAUDE.md in W3.

| Command | Disposition | Wave | Change |
|---|---|---|---|
| /comprehensive-review | keep (+dmi) | W3 | none else |
| /digest | keep (+dmi) | W3 | none else |
| /infographic | keep (+dmi) | W3 | Procedure summary mentions the signature visual and render/verify. |
| /animate | keep (+dmi) | W3 | none else |
| /visualize | keep (+dmi) | W3 | Remove the stale "fits one screen" rule. |
| /explain-code | keep (+dmi) | W3 | Empty args plus no referent → skill Step 0 (intent-lock), not "ask". |
| /critique-plan | keep (+dmi) | W3 | No-plan text aligned with the skill. |
| /resolve-decisions | keep (+dmi) | W3 | none else |
| /empty-vault | keep (+dmi) | W3 | Kebab topic → `<Topic> MOC.md` mapping stated. The skill itself stays model-invocable, because the Thai trigger "ล้าง vault" is a habit and the delete is already double-gated. |
| /new-plugin | keep (+dmi) | W3 | Summary includes the router-refresh step. |
| /refine-plugin | keep (+dmi) | W3 | Same. |
| /route | rewrite | W3 | Run `python3 scripts/route.py` (regenerate), then read and recommend. Read-only when the table is fresh (`--check`). Remove "if nothing fits, build a new plugin". |

### 3.4 micky-psych-tools infrastructure and docs

| Unit | Disposition | Wave | Change | Evidence |
|---|---|---|---|---|
| scripts/validate.py | rewrite (extend) | W0 | Never traceback: every `json.load` is guarded and counted. CRLF-safe frontmatter. Descriptions must be quoted or `>-` folded (strict-YAML portable) with the quotes excluded from length. ≤1024 hard; ≤900 and ≥250 house warnings, not failures. Skill name spec (SKL-06). CHANGELOG top entry == plugin.json version. No `{{` outside templates. Every relative link and `references/`/`scripts/` path mentioned in SKILL.md exists. No backslash paths. No bare `scripts/x` invocation without an interpreter (COM-46). Trigger-lock check (§6.1). Shared-copy parity (§5). stdio MCP allowed. `--project-skills <dir>` profile. It **also runs** `claude plugin validate --strict` per plugin and on the marketplace (PLG-10, PLG-11). | H13 validate.py:72-73,:111-114; infra inventory (CRLF, quoted-length bug) |
| scripts/route.py | rewrite | W0 (bugs), W3 (content) | argparse (`--help` no longer writes), `--check` for freshness, **no versions** in the output (fixes the stale-version defect), include each skill's NOT-for clause, share the frontmatter parser with validate.py through a small `scripts/_frontmatter.py`. | route.py:114-115,:145; LOC-08 |
| scripts/bump.py | rewrite | W0 | `ensure_ascii=False` plus a trailing newline. Validate *before* writing (dry-run by default, `--write`). Insert a `## x.y.z — <date>` CHANGELOG stub. Rerun route.py. `--catalog` bumps the top-level catalog version. Print the `claude plugin tag --dry-run` line (PLG-40). Keeps the dual write (§1). | bump.py:53-57; LOC-45 |
| scripts/sync_shared.py (new) | new | W2 | Copies `shared/**` into consumers per `shared/manifest.json`. `--check` is the parity gate. | §5 |
| scripts/health.sh (new) | new | W0 | One command: validate.py (which calls the CLI strict per plugin), route.py `--check`, sync_shared `--check`, optional `--cross-repo ../learn-hub`. | LOC-10 (no mechanical enforcement today) |
| scripts/eval.sh (new) | new | W0 | Wraps `claude plugin eval` with a pinned `--model`/`--judge-model`, `--no-publish`, `--max-cost-usd`, `--smoke` (free graders, `--ablation none`, runs 1) vs `--release`. | EVL-25, EVL-27 |
| ROUTING.md | keep (demoted, regenerated) | W3 | Human index only. No versions. Adds NOT-for boundaries. Still generated, never hand-edited. | LOC-09 |
| MEMORY.md | split | W4 | `MEMORY.md` ≤200 lines (identity, delivery facts, open threads, last ~5 milestones). Everything older → `docs/history/memory-archive.md`. Versions table replaced by `python3 scripts/validate.py --versions`. | LOC-25 (108 KB, ~27k tokens mandated read); LOC-27 (the 2026-07-10 plan is done, so archive it) |
| CLAUDE.md (micky) | rewrite | W3 | Remove the "route first" mandate (after W3 descriptions carry boundaries) and the "read MEMORY first" mandate (point to it instead). Replace the 69% plugin list with a pointer to marketplace.json and `/route` (fixes the gridgeist omission and drift). Add a Delivery section (in-place precondition, cloud env var, which plugins are cloud-enabled). Add the health check (`scripts/health.sh`) and layout (README, CHANGELOG, evals, shared). Workflow order becomes validate → bump (bump reruns route). | infra inventory CLAUDE.md defects; LOC-24 |
| .claude-plugin/marketplace.json | keep | W3 | Entry descriptions become the listing copy (PLG-42) and are aligned with plugin.json. Add owner email only if wanted. No `renames` needed. | infra inventory catalog defects |
| README.md (root), .gitignore | rewrite (small) | W0 | `validate --strict` per plugin. Private GitHub repos are supported (LOC-40). Gitignore `.env`, `.firecrawl/`, `plugins/*/evals/results/`. | infra README defects |

### 3.5 learn-hub plugins (8, plus their 6 commands and the catalog)

| Unit | Disposition | Wave | Target | Reason (evidence) |
|---|---|---|---|---|
| source-to-vault (skill `ingest-source`, command `/ingest`) | **retire** | W1 | delete `plugins/source-to-vault/`; fix the `.gitignore` comment | Writes production rows with no /vault file (H17), batch-ingests `Book/` with no confirmation (H18), collides with pdf-pipeline/atomize-book (H19), omits embedding/diagrams/images (H20). Superseded by pdf-pipeline → atomize-book/ingest-article. |
| digest-report (+ `/digest-report`) | convert-to-project-skill | W2 | `.claude/skills/digest-report/` (restores empty-vault's marker path) | Not loaded anywhere (H16). The input contract accepts the `## Sources` block plus legacy inline citations, and gains a "supplementary notes" slot (H15). The bare `/digest-report` means survey then stop; "digest the pending reports" means digest (resolves the command/skill conflict). Linux process check. `source:` topic field. `\$` escaping. Links to sync-vault instead of restating it. |
| vault-atomizer (+ `/atomize`) | convert-to-project-skill | W3 | `.claude/skills/vault-atomizer/` | Not loaded (H14). Sync via sync-vault (background), stale statistics removed, graph reference removed. The `/atomize` alias is **dropped** because it collides with atomize-book (P0-2, LOC-31) unless the owner uses it (§10, D6). |
| vault-vectors (+ `/vectors`) | convert-to-project-skill | W3 | `.claude/skills/vault-vectors/` (+ `.claude/commands/vectors.md` dmi alias if kept) | Not loaded. Command and skill contradictions fixed (sync-first, `--no-report`, timing). |
| pk-plasma-animation (+ `/pk-animation`) | convert-to-project-skill | W3 | `.claude/skills/pk-plasma-animation/` (+ `/pk-animation` dmi alias) | Not loaded. Research brief Sources format follows the shared report contract. Filing via ingest-animation, not a hand-built upsert. References load lazily (rebuild path reads none). No `.mcp.json` (research is delegated to pubmed-research-note). |
| intent-lock (fork) | retire (merge ledger) | W3 | micky intent-lock | The fork splits the ledger (H06) and is otherwise identical (LOC-33). Merge any learn-hub-only ledger entries into micky's before deleting. |
| pubmed-research-note (fork) | retire | W2 | micky pubmed-research-note + `learn-hub/.output-sink.json` | The evals fail by construction (H48). The only real delta is the filing path, which becomes config. Retired in the **same wave** as the adapter lands. |
| comprehensive-review (fork, + `/comprehensive-review`) | retire | W2 | micky comprehensive-review + sink adapter | Default digest plus live-Supabase sync (H49) disappears. Under the adapter, digest is gated on "atomize", consistent with pubmed and digest-report. |
| .claude-plugin/marketplace.json (`learn-hub-local`) | retire | W3 | delete `.claude-plugin/` | Nothing remains to list, and it was never registered (H14). Deleting it also removes the second "marketplace.json" that vault-keeper's walk-up could match (H09, belt and braces). If Wave 0 finds it installed on Windows, run `claude plugin marketplace remove learn-hub-local` first. |

### 3.6 learn-hub project skills (11)

| Skill | Disposition | Wave | Change | Evidence |
|---|---|---|---|---|
| atomize-book | split + rewrite (targeted) | W1 content, W4 split | W1: one rule for `[[topic-id]]`: it is a chapter reference, valid in the body, never repointed, never in `links:`. Sync economics: incremental `sync:apply` in the background via sync-vault; delete the `npm run sync` step. Add the four missing drafting rules: `\$` money, equation-as-PNG detection, stadium-node ban, LIVE_GROUPS/book-category fixture step. Fix the one-level-glob id check. Mermaid via `scripts/check-mermaid.mjs`. Drop the "re-sync the vault" trigger. Description ≤1024. W4: body ≤500 lines. Reference-grade sections move **verbatim** into `references/{figures,measurement,qc,traps}.md` with "Read X before step N" pointers. | H21 SKILL.md:295-296 vs :1027-1029,:1063-1067; H22 :1116-1117,:1265-1267; H23 (0 grep hits; CLAUDE.md:2489,:2511,:1325); H24 1,256 lines |
| ingest-article | rewrite (targeted) | W1, W4 | W1: a bare invocation **surveys the inbox and asks** before ingesting or deleting. Inbox path from env `ARTICLE_INBOX` (default repo-relative `Raw Article PDF/`), never a Windows literal. Gitignore it. Fix the source-cover command (pass `ch01.txt` or a notes dir) or drop it until the script accepts a file. Required measure-loss flags in the reference. Delete the `diagrams {}` fallback (bake columns are omitted, not emptied). Mermaid via check-mermaid.mjs. Description ≤1024, valid YAML, no "bullet-reconstruct this" trigger (collides with anthropic-skills). PyMuPDF preflight install. W4: mandatory references ≤9k tokens. | H25 SKILL.md:3,:49,:51,:348 + .gitignore; H26 figures-and-loss.md:455-458 vs measure-source-cover.mjs:70,:37-43 |
| ingest-slides | rewrite (targeted) | W1 | Script paths via `${CLAUDE_SKILL_DIR}/scripts/…`. pdf-pipeline routes decks here. Apply check-figures and measure-loss (it claims to reuse ingest-article "wholesale"). Sync via sync-vault (no `npm run sync`). Description ≤1024, no "grilling" leftovers. PyMuPDF preflight. | H27 SKILL.md:62,:71; H28 pdf-pipeline SKILL.md:98 |
| ingest-infographic | rewrite (targeted) | W1, W2 | W1: valid YAML. Delete "targeted upsert == npm run sync" and use sync-vault. Gallery is `/visualization`. One permitted-edits statement. W2: the empty-vault handshake is real again, so keep the trigger and document the asset handoff contract copy. | H29 SKILL.md:3,:137-138; H30 :116-118 |
| ingest-animation | rewrite (targeted) | W1, W2 | W1: valid YAML. Run `auditAnimationLayout` and the doctype/color-scheme check, and report (not silently fix) a failure back to the author. Use sync-vault. W2: handshake plus a NOT-for against authoring (concept-animation). | H31 SKILL.md:3,:123-125 |
| pdf-pipeline | rewrite (targeted) | W1 | Slide decks → ingest-slides. Apply path is `sync:apply` only, via sync-vault; delete the "≲200 KB → MCP" rule. Flat vault layout. Remove graph/card-wall checks and the stale preflight premise (the hook exists; multi-repo sessions call it by hand, per sync-vault). NOT-for vs `anthropic-skills:pdf`. | H32 SKILL.md:98, routing.md:42,:60; H33 :138-141 vs :150 |
| sync-vault | rewrite | W1 | Flat layout (delete the nested recommendation). Default = `git fetch` + merge check → precondition check → `npm run sync:apply` as a **background job with a log**, success read from `EXIT=0` plus the `Upserted … note(s)` line. The operational gotchas move here from CLAUDE.md. **Precondition step for multi-repo sessions, where hooks don't run:** if the `session-start: ready` line or `.env.local` / `node_modules` / `PUPPETEER_EXECUTABLE_PATH` is absent, run `CLAUDE_PROJECT_DIR=<repo> bash .claude/hooks/session-start.sh` and run `npm run similarity:gate` / the repetition gate by hand. Per-provenance verification instead of whole-table counts. Deletion via `purge:hidden` / `merge_note_history`. NOT-for. | H34 SKILL.md:126-132; H35 :32-34,:65-72; cloud-environments.md L468 |
| vault-coverage | keep | W1 | `BOOK_ROOT` from the environment, with no Windows literal. Say "cannot run where Book/ is absent" as a finding. atomize-book gains the "add to coverage-sources.json" step. | vault-coverage SKILL.md:40 |
| check-repetition | keep | W3 | Add a NOT-for (detect-duplicates, atomize-book §7b). Revalidate via `npm run revalidate`. | SKILL.md:88 |
| verify | rewrite (light) | W4 | Bundle `scripts/mint-session.mjs` and `scripts/probe.mjs` (the prose recipe made executable). Trigger phrases plus a NOT-for (browser pane, chrome-devtools isolated world). | SKILL.md:41-43 |
| concept-animation (learn-hub copy) | merge → retire | W2 | into micky `plugins/concept-animation` | Same-name collision and diverged fixes (LOC-34). Retired in the same wave its fixes land upstream **and** micky concept-animation is in the cloud `CLAUDE_CODE_PLUGIN_DIRS` list. Bare `/concept-animation` then resolves to the plugin skill (PLG-17), and `/animate` is unchanged. Its builder pattern moves to pk-plasma-animation's reference. |

### 3.7 learn-hub CLAUDE.md (as it relates to skills)

| Unit | Disposition | Wave | Change |
|---|---|---|---|
| learn-hub/CLAUDE.md | rewrite (sections only) | W1 facts, W5 relocation | W1: correct the statements the skills now contradict or that went stale: disposition list (6, not 4), public bucket → `book:file-figures`, `pk-plasma-animation` location, "clinical-infographic enforces light-lock" (true after W1). W5 (owner decision D5): move the ~58 pipeline/import gotchas **verbatim** into the owning skill's `references/gotchas.md` (atomize-book, ingest-article, sync-vault, vault-coverage), each leaving a one-line pointer. App gotchas stay. The Documentation-upkeep section says where new pipeline gotchas go. |

---

## 4. HIGH-defect coverage map (all 49)

| # | Unit | Defect (short) | Evidence | Fix | Wave |
|---|---|---|---|---|---|
| H01 | intent-lock | silent contract contradicted in 11 places | SKILL.md:16,22 vs :49…:206 | delete the lines, not a reinterpret patch | W3 |
| H02 | intent-lock | picker contract not executable in CC; no fallback | :136,:160-162,:189-190 | AskUserQuestion mechanics + fallback | W3 |
| H03 | intent-lock | ledger can't compound (plugin tree / cache) | misread-capture:39; one git change | in-place repo file + cache guard + commit offer | W3 |
| H04 | misread-capture | `Prior:` has no eliciting question | :26,:30-35,:47,:55 | Q2 elicits the check | W3 |
| H05 | callers | preface expects Reframed/Skipped | intent-lock:226 vs pubmed:263-265, CR:147-148 | single `Assumed:` line, shared contract | W2 |
| H06 | learn-hub intent-lock fork | split ledger | two misreads.md files | merge + retire fork | W3 |
| H07 | plugin-creator | repo-bound, no precondition | SKILL.md:9-10; cache lacks scripts/ | in-place root guard | W1 |
| H08 | vault-keeper | `${CLAUDE_PLUGIN_ROOT}/../../vault` wrong in cache | SKILL.md:29 | resolution order + cache guard | W1 |
| H09 | vault-keeper | walk-up matches learn-hub | SKILL.md:28 | marketplace name check + ask | W1 |
| H10 | empty-vault | stale learn-hub marker | SKILL.md:36-37 | detection on stable files (env/sibling/ask) in W1; digest-report available again in W2 | W1/W2 |
| H11 | empty-vault | deletes assets that have receivers | SKILL.md:54-57 | W1 hold assets; W2 handoff + handshake | W1/W2 |
| H12 | firecrawl | stale "verbatim" vendor guide | SKILL.md:146-147,:127,:330 | refresh + dated stamp; split W4 | W1 |
| H13 | validate.py | tracebacks; uncounted PASS | :72-73,:111-114 | guarded loads, counted checks | W0 |
| H14 | learn-hub catalog | never registered | settings.json hooks only | plugins → project skills; catalog deleted | W2/W3 |
| H15 | digest-report | input contract vs `## Sources` producers | SKILL.md:88-90 vs pubmed:211 | accept Sources block + legacy | W2 |
| H16 | digest-report | not loaded anywhere | plan doc:67 | back to .claude/skills | W2 |
| H17 | source-to-vault | prod rows without vault files | SKILL.md:8-10,:140-141 | retire | W1 |
| H18 | source-to-vault | no-arg batch ingest of Book/ | SKILL.md:27-28,:128-129 | retire | W1 |
| H19 | source-to-vault | routing collision | SKILL.md:3 | retire | W1 |
| H20 | source-to-vault | omits embedding/diagrams/images | SKILL.md:116 | retire | W1 |
| H21 | atomize-book | topic-id contradiction | :295-296 vs :1027-1029 | one rule per CLAUDE.md:2588 | W1 |
| H22 | atomize-book | stale sync economics | :1116-1117,:1265-1267 | defer to sync-vault | W1 |
| H23 | atomize-book | 4 drafting rules missing | 0 grep hits | add to drafting spec + note-format | W1 |
| H24 | atomize-book | 21.3k-token body | 1,256 lines | verbatim split to references | W4 |
| H25 | ingest-article | Windows inbox; bare invoke deletes; not ignored | :3,:49,:51,:348 | survey-and-ask, env path, gitignore | W1 |
| H26 | ingest-article | source-cover command can't run | figures-and-loss:455-458 | correct invocation or drop | W1 |
| H27 | ingest-slides | wrong script paths | :62,:71 | `${CLAUDE_SKILL_DIR}` | W1 |
| H28 | ingest-slides | routing conflict with pdf-pipeline | pdf-pipeline:98 | pdf-pipeline routes decks here | W1 |
| H29 | ingest-infographic | dead empty-vault contract | :3,:137-138 | empty-vault handoff (W2) | W2 |
| H30 | ingest-infographic | "targeted upsert == npm run sync" | :116-118 | use sync-vault | W1 |
| H31 | ingest-animation | dead empty-vault contract | :3,:123-125 | empty-vault handoff | W2 |
| H32 | pdf-pipeline | slides → atomize-book | :98; routing.md:42,:60 | route to ingest-slides | W1 |
| H33 | pdf-pipeline | impossible apply rule | :138-141 vs :150 | sync:apply via sync-vault | W1 |
| H34 | sync-vault | recommends nested layout | :126-132 | flat layout | W1 |
| H35 | sync-vault | default `npm run sync` path, no traps | :32-34,:65-72 | background sync:apply + preconditions | W1 |
| H36 | clinical-infographic | dark block in template | template:100-104 | light-lock | W1 |
| H37 | clinical-infographic | `.mech` cramps on phones | template:74-75,:93 | mobile stacking rule | W1 |
| H38 | concept-animation | stage-collapse layout rule | grammar:46,:48 | port learn-hub grammar | W2 |
| H39 | concept-animation | single-viewport fit check | SKILL:145-150 | 5-viewport shared checker | W2 |
| H40 | ml-concept-lab | stage-collapse layout rule | build-contract:140-141 | same port | W2 |
| H41 | ml-concept-lab | verify recipe fails (ESM playwright) | :195-197,:202 | shared checker | W2 |
| H42 | code-explainer | template never existed | SKILL:67-68,:136 | remove pointers + dead-link check | W1 |
| H43 | learn-hub concept-animation | invalid strict YAML | SKILL.md:3 | `>-` folded (fixed in W1 before merge-retire in W2) | W1 |
| H44 | pubmed-research-note | Reframed preface stale | SKILL:263; pairing:86-90 | single Assumed line | W2 |
| H45 | pubmed-research-note | decision-brief slot arithmetic | decision-brief:11-12 | 3+3 slots, pairing aligned | W2 |
| H46 | psych-paper-digest | pdat vs edat window | sweep-recipes:39-40 | datetype edat | W1 |
| H47 | psych-paper-digest | silent truncation at 50 | :39-40 vs :92-93 | retstart pagination + counted cap | W1 |
| H48 | learn-hub pubmed fork | evals fail by construction | evals.json:56,:128 | retire fork | W2 |
| H49 | learn-hub CR fork | default digest + live sync | SKILL.md:166-176 | retire fork; adapter gates on "atomize" | W2 |

The medium and low defects of every unit a wave touches are fixed in that same wave. They are listed in the inventories. Their fixes are the ones named in §3, and no separate plan is needed.

---

## 5. Shared-content strategy

### 5.1 Principle

**One canonical file, generated byte-identical copies, and a parity gate.** Paths across plugins are unusable once a plugin is cached (PLG-22, COM-38). Symlinks are fragile on Windows checkouts and are only partly preserved for local and `--plugin-dir` installs (PLG-23). Hard dependencies disable the dependent plugin (Appendix A). Anthropic's own exemplar skills duplicate shared files byte-identically (COM-39). learn-hub already runs this pattern for mermaid-split and tag-canon.

### 5.2 Canonical set (micky `shared/`)

| Canonical file | Content (deduplicated from…) | Copied into |
|---|---|---|
| `contracts/report-format.md` | Sources grammar (topic → DOI/URL, no authors/journal/year/PMID) with **one** NCT line form, the `Assumed:` preface line, no inline citations, the depth contract (per-study fields), engine-failure policy (PubMed down = fatal; registry down = named gap), firecrawl fetch-only policy. This merges four drifted copies (research-writers group obs.: NCT grammar in 3 variants, preface in 2). | pubmed-research-note, comprehensive-review, psych-paper-digest (NCT line only), pk-plasma-animation brief (learn-hub copy), digest-report (learn-hub copy; this is the consumer's input spec) |
| `contracts/alignment-interview.md` | Admission threshold, destructive/irreversible/outward-facing always-ask, AskUserQuestion mechanics (1–4 questions, 2–4 options, `multiSelect`, automatic Other), one silence rule ("a rejected or errored picker is not an answer → fallback"), the fallback (reversible → default plus `Assumed:`/"Decided without you"; destructive → written decision request), push-once, stop sovereignty, the §2.4 handoff sentence, and the question-cap rationale (intent-lock 3 by design, siblings 4 by tool ceiling, both stated). | intent-lock, decision-interview, plan-critique, plus the handoff paragraph in every intent-lock caller |
| `contracts/html-artifact.md` | Self-contained, reduced-motion, colour never the only signal and AA, full document plus `color-scheme`, light-lock for sheets, mobile strip stacking, animation layout floor, five viewports, honest footer, `illustrative — not measured data`. | clinical-infographic, concept-animation, ml-concept-lab, code-explainer |
| `contracts/vault-handoff.md` | vault-keeper payload slots (legal target types note/artifact/asset), asset `source` field, the empty-vault → learn-hub handoff table (report → digest-report; infographic → ingest-infographic; animation/explorable → ingest-animation; other assets held) and the handshake it waits for. | all micky producers, vault-keeper, empty-vault, learn-hub ingest-infographic/ingest-animation/digest-report (copies) |
| `scripts/check_html_artifact.mjs` | Deterministic checker: no external refs, reduced-motion block, doctype/color-scheme, dark-block scan for sheets, strip rule, and a Playwright five-viewport stage/overlap/controls probe (resolved via `createRequire` from `npm root -g`; Chromium from `PUPPETEER_EXECUTABLE_PATH`/`/opt/pw-browsers`). Every error names its fix (COM-15). | the four renderers' `scripts/` |

Each copy carries a first-line marker `<!-- GENERATED from micky-psych-tools/shared/<path> — edit the canonical, run scripts/sync_shared.py -->`, which is harmless in markdown and reminds editors. `validate.py` fails on any hash mismatch inside micky.

### 5.3 Across repos

- The learn-hub copies (report-format, vault-handoff, html-artifact) keep the same marker plus the source commit.
- `scripts/check_cross_repo.py --learn-hub <path>` in micky compares their hashes. It also asserts the handoff markers: `learn-hub/.claude/skills/digest-report/SKILL.md` exists, the ingest-* skills name the handshake, and `.output-sink.json` parses. It runs at every wave exit and whenever either repo edits a contract. Multi-repo cloud sessions hold both clones, so it can always run there.
- **Direction rule: consumers before producers.** A cross-repo contract change lands on the consumer side first, accepting both old and new forms (tolerant reader), then on the producer side. digest-report accepts the Sources block *and* legacy inline citations before any producer changes (W2 step order).
- **The render contract's executable truth stays in learn-hub** (`auditAnimationLayout`, `auditInfographicResponsive`, `src/lib/animation-layout.ts`). micky's checker ports the same predicates. A parity fixture keeps them aligned: the four example HTMLs plus two known-bad fixtures must get the same verdict from both tools. It is run at W2 exit and when either changes.

### 5.4 MCP tools: fix the text, not the wiring

The three `.mcp.json` files stay (§1). Every hard-coded `mcp__plugin_<p>_pubmed__…` plus "No ToolSearch step" is replaced by one resolution rule in `report-format.md`:

> Use the PubMed/ClinicalTrials tool that exists in this session: `mcp__PubMed__*` / `mcp__Clinical_Trials__*` (connector) or `mcp__plugin_*_pubmed__*` / `mcp__plugin_*_clinical-trials__*` (plugin). If neither is listed, run ToolSearch for "pubmed" once. If still none, fall back to E-utilities / CT.gov API v2 via WebFetch.

Endpoint deduplication means the callable prefix depends on which definition wins (PLG missed practice), so the prefix can't be hard-coded (SKL-53).

### 5.5 Per-repo output sink (replaces the three forks)

A committed `learn-hub/.output-sink.json`:

```json
{ "reports": { "dir": "research-notes", "file": "none", "atomize": "digest-report" },
  "assets":  { "infographic": "ingest-infographic", "animation": "ingest-animation" } }
```

Producers resolve the **git toplevel of cwd**:

- If `.output-sink.json` is there, obey it: a report is written to `research-notes/<slug>.md` and digested only on "atomize"; an asset is handed to the named ingest skill.
- If it is absent, use the micky default (vault-keeper).
- If cwd is not inside a repo (the multi-repo `/home/user` case), apply owner decision D3.

`.pubmed-research-note.json` `report_dir` stays honoured for backward compatibility. This is about 12 lines per producer and a file in one repo. It replaces two ~300-line forks and one diverged 200-line copy.

---

## 6. Evals strategy

### 6.1 Three layers

1. **Static, on every commit.** `scripts/health.sh` (micky) runs validate.py (house rules above), `claude plugin validate --strict` on every plugin directory and the marketplace (the marketplace-root run alone never opens SKILL.md: PLG-10, SKL-49), sync_shared `--check`, and route `--check`. learn-hub runs `claude plugin validate --strict .claude/skills`, `npm test`, and the atomize-book `python -m unittest` (not run by `npm test`, EVL-41). A new vitest `scripts/lib/skill-lint.mjs` completes learn-hub's own open P1-1 validator item (LOC-30): description ≤1024, strict YAML, dead `references/`/`scripts/` paths, no Windows literals, no `npm run sync` as a default step.
   **Ratchet:** every new house check starts with the current violations listed in `docs/rewrite/ratchet.json`. A listed violation warns and a new one fails. A wave must delete the entries it fixes, and the file may only shrink, so W0 can land strict checks without breaking on known HIGH defects such as H42's dead link or the three over-cap learn-hub descriptions.
   **Trigger-lock:** W0 extracts every quoted phrase from every current description into `triggers.lock.json` (micky and learn-hub). Any later edit that drops a locked phrase fails validation unless the lock file records the removal with a reason. This protects the Thai and slash triggers mechanically.
2. **Deterministic unit tests** for every new script: `check_html_artifact`, `vault_index`, the digest window/dedup/pagination math, the ledger append, sync_shared. Python uses stdlib `unittest` (micky's stdlib-only style). Node uses vitest (learn-hub). This follows "scripts over LLM judgment for mechanical checks" (EVL-41, COM-16).
3. **Behavioural evals** with `claude plugin eval` (v2.1.269+; CLI is 2.1.280). Cases live at `plugins/<p>/evals/<skill>/<case>/{prompt.md,graders/}` (EVL-02, EVL-06).

### 6.2 Minimum suite per skill before its rewrite lands (evaluation first: SKL-43, COM-27)

- **Trigger, positive:** a realistic, multi-step prompt using a locked phrase (including a Thai one where it exists). Grader: `tool_used: Skill` with `input_match '"skill"\s*:\s*"(?:[\w-]+:)?<skill>"'` (EVL-16 corrected).
- **Near-miss negative from the sibling family:** `tool_used Skill min:0 max:0 arm: both` (EVL-15). Families: intent-lock / decision-interview / plan-critique; pubmed / comprehensive-review / psych-paper-digest; concept-animation / ml-concept-lab / clinical-infographic / code-explainer; atomize-book / vault-atomizer / digest-report / ingest-article / pdf-pipeline / ingest-slides (the P0-2 "atomize" collision, LOC-31).
- **Output contract:** a regex over the written file for structural markers, not a haiku judge on long text (EVL-11). Examples: exactly one `Assumed:` line and no `Reframed:`; the `## Sources` grammar; a safety banner present and no `prefers-color-scheme:dark`; `min-height:100dvh`; nothing written into a cached plugin path.
- **Gates (intent-lock, decision-interview, plan-critique):** a pressure scenario (COM-28 corrected) plus the **fallback**. Eval runs grant only the listed read-only tools, so AskUserQuestion is absent and the case exercises exactly the fallback that is broken today (H02). The grader regexes for the `Assumed:` line and for the absence of a stall.
- **MCP-dependent skills:** `evals/mocks/pubmed/search_articles.md` etc. with fixed PMIDs. An `expect:` block asserts `datetype: edat` and `retstart` for psych-paper-digest (H46, H47) (EVL-24).
- **Conversion from evals.json:** only the skeleton converts mechanically (`name` → case dir, `prompt` → body, `expected_output` → `expected_outcome`). Graders are hand-written, because every `assertions` array is empty (EVL-04 corrected, EVL-05, EVL-29). Target is ~3–5 converted cases per skill, not all 118.

### 6.3 learn-hub project skills

Plain `.claude/skills` are documented only through skill-creator (EVL-46 corrected; the CLI's acceptance of a bare folder is undocumented and not relied on). `learn-hub/scripts/eval-project-skill.sh <skill>` builds a **throwaway plugin** in the scratchpad (`.claude-plugin/plugin.json`, `skills/<skill>` copied, `evals/<skill>` copied) and runs `claude plugin eval` on it. That is a documented target shape assembled at run time, so the skill tree gets no manifest and multi-repo loading is untouched. Pipeline skills that need Supabase or `.env.local` get evals only for the **decision steps**: routing, the inbox survey-and-ask, the refusal to run `npm run sync`. Their deterministic cores stay covered by unit tests (EVL-22).

### 6.4 Regression method for rewrites

The baseline is the **old version, not "no plugin"** (EVL-30, COM-30):

1. Snapshot `plugins/<p>` to the scratchpad at W0.
2. Run the same cases on the old and new directories and compare with-arm scores.
3. For holistic output (report quality, the intent-lock interview) add a blind A/B through skill-creator's comparator (EVL-35).

Verification runs never happen in the authoring session (SKL-44, EVL-43).

Cross-plugin routing can't be tested in isolated runs, because only one plugin loads (EVL-19, EVL-20 open). A **live routing smoke** covers it at W3 exit: 20 near-miss prompts run with `claude -p` and `CLAUDE_CODE_PLUGIN_DIRS` loading all delivered plugins, checking which skill fired in the transcript, in the spirit of skill-creator's run_eval (EVL-39).

### 6.5 Cost control

- Per-wave smoke: free graders only, `--ablation none`, `--runs 1`, `--max-cost-usd` (owner sets it, D8), and only on plugins touched in the wave.
- Release runs (W3 and W4 exits): two arms, `--runs 3`, `--threshold 0.8`, pinned `--model`/`--judge-model` (EVL-18, EVL-25, EVL-27).
- Check run errors for rate-limit zeros before reading a drop as a regression (EVL missed practice).
- `evals/results/` is gitignored.

---

## 7. Versioning and release

- **micky:** explicit semver, dual write kept (§1). Changes are mechanical only (bump.py rewrite):
  - `bump.py <plugin> patch|minor|major` (dry run) → `--write`. It validates first, writes both files with UTF-8 and a trailing newline, inserts the CHANGELOG stub, reruns route.py and prints the `claude plugin tag` line.
  - validate.py fails if CHANGELOG's top entry ≠ plugin.json version. This closes the gaps: pubmed missing 1.3.0/1.4.0, psych-paper-digest 0.1.1, vault-keeper 0.3/0.4, intent-lock 0.4.1, clinical-infographic 0.2.1. **W0 backfills** those entries from MEMORY.md.
  - Every plugin touched in a wave gets **minor** for a behaviour change (triggers, output, filing) and **patch** for fixes. The catalog top-level version gets **minor per wave** (`bump.py --catalog`).
  - Release tags `{plugin}--v{version}` via `claude plugin tag` are **optional**. No consumer pins ranges (PLG-39, PLG-40). Suggested only at W3 and W4 exits.
  - Since every environment loads in place, versions are history labels for the owner, not update triggers (PLG-09). That is why bumps may batch at the end of a wave rather than per commit.
- **learn-hub:** project skills stay unversioned (consistent with the repo). Each wave adds a repo CHANGELOG entry per the existing convention. The retired plugins and catalog leave no version surface behind. This resolves polish-plan P1-2 by removal (LOC-30).
- **Rollback:** each wave is one branch per repo, merged only at wave exit. Tags `pre-rewrite` and `wave-N` exist in both repos. Rollback is `git revert` of the wave merge plus restoring the previous `CLAUDE_CODE_PLUGIN_DIRS` value, which the owner keeps in `docs/rewrite/delivery-log.md`.

---

## 8. Context-budget targets (numbers)

| Surface | Baseline (evidence) | Target | Measured by |
|---|---|---|---|
| micky always-on (`claude plugin details`, 14 plugins) | ~6,579 tok (LOC-19) | ≤5,000 tok by W3; no plugin >600 | `claude --plugin-dir … plugin details`. It does **not** reflect dmi: `digest` shows ~40 tok with and without it (Appendix A). |
| micky skill descriptions, total | 15,953 chars (17 skills; 8 at 1,003–1,022, LOC-07) | ≤13,000 chars; none >900 (warn), none >1,024 (fail); trigger-lock intact | validate.py report |
| micky commands in Claude's listing | 12 entries | 0 (dmi) | `/doctor` (details doesn't show dmi) |
| learn-hub project-skill descriptions | 8,726 chars (11 skills; 3 over 1,024: 1,075/1,137/1,150) | ≤9,500 chars for the 14 skills after W3 (+4 moved in, −1 retired); none >1,024; none >900 except atomize-book ≤1,000 | skill-lint |
| Cloud multi-repo skill listing | unknown; ~30 skills + 21 synced claude.ai skills at ~900 chars each (SKL-08, COM-08) | **no description dropped** (`/doctor` shows no overflow) with all delivered micky plugins | owner runs `/doctor` and `/skill-doctor` at W0 and at each wave exit |
| intent-lock on invoke (loaded as Step 0 by 5+ skills) | ~8.1k tok (LOC-19); body 6.2k | ≤4,000 tok body + failure-conditions ≤700 | details, wc |
| pubmed-research-note per run | 4.7k body + 5.9k mandatory refs (research-writers) | body ≤4,000; mandatory per-run refs ≤4,000 | same |
| firecrawl on invoke | ~6.2k (LOC-19) | body ≤1,500; vendor reference on demand | same |
| atomize-book body | 1,256 lines / ~21.3k tok | ≤500 lines / ≤7,000 tok (interim cap); references load per step | wc, chars/4 |
| ingest-article per run | ~6.7k body + ~12k mandatory refs | ≤9,000 total mandatory | same |
| any SKILL.md body | none | ≤500 lines and ≤5,000 tok (warn; SKL-15), atomize-book excepted as above; standing rules in the first 5k tokens (post-compaction re-attach, SKL-40) | validate.py / skill-lint |
| micky CLAUDE.md | ~3.5k tok, 69% plugin list | ≤1,500 tok | wc |
| micky mandated reads per session | MEMORY ~27k + ROUTING ~5k per request | 0 mandated; MEMORY ≤3,000 tok when read | wc |
| learn-hub CLAUDE.md (always loaded; also loaded in multi-repo sessions, observed) | ~67k tok (3,126 lines) | ≤30k tok if D5 = move (W5) | wc |

---

## 9. Migration waves

Every wave exits with:

- `scripts/health.sh` green in micky;
- learn-hub `claude plugin validate --strict .claude/skills` + `npm test` + atomize-book unittests + skill-lint green;
- `scripts/check_cross_repo.py` green (from W2);
- smoke evals for every touched skill at or above the W0 baseline;
- a CHANGELOG entry in each touched repo.

No wave leaves the report → vault → learn-hub pipeline worse than it was at wave entry.

### W0 — Ground truth and safety net (no behaviour change)

- **Entry:** both repos clean on master. Tag `pre-rewrite`.
- **Work:**
  1. validate.py, route.py and bump.py bug fixes (H13); `health.sh`; `eval.sh`.
  2. Trigger-lock generation.
  3. CHANGELOG backfill, plus a first CHANGELOG.md for the 5 plugins that have none (LOC-23); README/.gitignore fixes.
  4. Ratchet file `docs/rewrite/ratchet.json` (see §6.1).
  5. learn-hub `skill-lint.mjs` + tests.
  6. Snapshot all plugins and skills (old-version baselines).
  7. Seed smoke suites (3 cases each) for the W1 units: vault-keeper, empty-vault, psych-paper-digest, clinical-infographic, ingest-article, sync-vault, pdf-pipeline.
  8. Record baseline numbers in `docs/rewrite/baseline.md`: descriptions, `plugin details`, body sizes.
  9. **Environment facts, with the owner:**
     - (a) On Windows: `claude plugin marketplace list`/`claude plugin list`. Is micky local-directory or GitHub? Is learn-hub-local installed? (D1, D6)
     - (b) Cloud: set `CLAUDE_CODE_PLUGIN_DIRS=/home/user/micky-psych-tools/plugins/gridgeist` on the environment (the least-coupled plugin; remove it after the test if unused). In a new multi-repo session confirm `gridgeist@inline` loads (`claude plugin list` shows it under session-only plugins). Record the result.
     - (c) Run `/doctor` in a cloud multi-repo session and record listing cost and overflow.
- **Exit:** everything above green on untouched content. New checks fail only on *new* violations; existing ones are listed in the ratchet and warn. Smoke suites run end to end. Env facts recorded. **If (b) fails, stop.** The cloud delivery route falls back to claude.ai sync, and D2 is re-asked before W2.

### W1 — Stop active harm in units that load today; retire the unloaded hazard

- **Entry:** W0 exit. Env facts known.
- **learn-hub work (consumer side):**
  1. sync-vault rewrite (H34, H35, multi-repo preconditions) **first**, because every other learn-hub fix links to it.
  2. ingest-article (H25, H26).
  3. pdf-pipeline (H32, H33).
  4. ingest-slides (H27, H28).
  5. atomize-book content fixes (H21, H22, H23).
  6. ingest-infographic / ingest-animation (H30, YAML), learn-hub concept-animation YAML (H43).
  7. vault-coverage, CLAUDE.md factual corrections.
  8. Retire source-to-vault (H17–H20).
- **micky work:**
  1. vault-keeper root resolution (H08, H09).
  2. empty-vault stopgap: hold assets, new learn-hub detection (H10, H11 part 1).
  3. plugin-creator guard (H07).
  4. psych-paper-digest search fixes (H46, H47).
  5. clinical-infographic light-lock and strip (H36, H37).
  6. firecrawl vendor refresh (H12).
  7. code-explainer pointers (H42).
  8. Bump the touched plugins.
- **Cloud delivery:** unchanged (only gridgeist from W0), so W1 changes nothing in the cloud listing.
- **Exit:**
  - Standard gates.
  - The W1 smoke cases show the new behaviour: ingest-article bare invocation → survey plus question, no deletion; sync-vault picks `sync:apply` in the background; vault-keeper from a learn-hub cwd → stop and ask.
  - The clinical-infographic template and example pass learn-hub's `auditInfographicResponsive`, and the grep for `prefers-color-scheme:dark` is empty.
  - **One live, owner-approved sync of a trivial vault edit** in a multi-repo cloud session runs through the new sync-vault precondition step and verifies the `diagrams` count did not drop (the diagrams-wipe class).
  - Pipeline status: equal or better. Assets are now kept rather than deleted, and nothing else in the pipeline changed.

### W2 — Reconnect the cross-repo pipeline; one upstream for research and renderers

- **Entry:** W1 exit. D3 answered (sink for non-repo cwd).
- **Order is consumers → producers, each step its own commit:**
  1. learn-hub: digest-report → `.claude/skills/` (H16) with a tolerant input contract (H15) and a supplementary-notes slot. Commit `.output-sink.json`. Add the handoff contract copies to ingest-infographic / ingest-animation (H29, H31 consumer side). Add auditAnimationLayout reporting to ingest-animation.
  2. micky: `shared/` canonical files plus `sync_shared.py`. Copies into consumers.
  3. micky: pubmed-research-note and comprehensive-review, targeted (H44, H45, H05, runtime MCP tools, sink adapter, handoff fallback).
  4. micky: renderers. concept-animation merge (H38, H39), ml-concept-lab (H40, H41), clinical-infographic checker plus filing, and `check_html_artifact.mjs` with its parity fixture against learn-hub's audits.
  5. micky: empty-vault full handoff (H11 part 2, H10 closed, since the digest-report path exists again).
  6. **Cloud delivery:** extend `CLAUDE_CODE_PLUGIN_DIRS` with vault-keeper, pubmed-research-note, comprehensive-review, firecrawl, clinical-infographic, concept-animation, ml-concept-lab, code-explainer. Log it in `docs/rewrite/delivery-log.md`.
  7. **Only after step 6 is confirmed in a new cloud session:** retire the learn-hub pubmed-research-note and comprehensive-review forks (H48, H49) and the learn-hub concept-animation copy (atomic swap).
- **Exit:**
  - Standard gates plus the cross-repo check and the checker parity fixture.
  - The micky CA and ML examples pass `auditAnimationLayout` with `[]`.
  - **Rehearsal:** a fixture report in the micky vault → `/empty-vault <fixture-topic>` runs manifest → digest-report → ingest-* handshake. It stops before any Supabase write unless the owner approves one real report, and then verifies provenance counts.
  - A report written in a learn-hub session lands in `research-notes/` and is **not** digested without "atomize".
  - `claude.ai daily-random-review` chaining into micky comprehensive-review completes in an unattended run through the fallback (risk R6).
  - `/doctor` shows no listing overflow.

### W3 — Alignment family, descriptions and boundaries; finish delivery; delete leftovers

- **Entry:** W2 exit. D4, D6, D7 answered.
- **Work:**
  1. intent-lock rewrite by subtraction (H01, H02) and misread-capture (H03, H04). Ledger: merge the learn-hub fork's entries, then retire the fork (H06).
  2. decision-interview and plan-critique light rewrites on the shared alignment contract.
  3. Description pass for **all** micky skills: remove procedure and mechanics text, add reciprocal NOT-for boundaries (CA↔ML, CE↔ML, PC↔misread-capture, psych-paper-digest ↔ claude.ai daily digest), third person (SKL-09, COM-04 reconciliation: one capability clause + triggers + NOT-for, no step sequence). Trigger-lock must stay intact. Trigger evals before and after.
  4. dmi on the 12 commands; `/route` rewrite; route.py content (NOT-for, no versions).
  5. learn-hub: vault-atomizer, vault-vectors and pk-plasma-animation → `.claude/skills` (+ aliases per D6). Delete the `learn-hub-local` catalog (H14).
  6. Remove the micky CLAUDE.md route-first and MEMORY-first mandates; add the Delivery section.
  7. **Cloud delivery:** add intent-lock, decision-interview, plan-critique and plugin-creator (and gridgeist only if used). psych-paper-digest stays local-only unless D4 says otherwise.
- **Exit:**
  - Standard gates.
  - **Release eval run** (two arms) on every micky plugin at or above the old-version baseline.
  - The live routing smoke (20 near-miss prompts) meets the owner's acceptance bar (default ≥17/20 correct and 0 destructive misroutes).
  - `/doctor` shows no overflow.
  - No `plugins/` directory is left in learn-hub.
  - The always-on total is ≤5,000 tok.

### W4 — Progressive disclosure and determinism (cost work, after correctness)

- **Entry:** W3 exit.
- **Work (all body moves are verbatim, with explicit "Read X before step N" triggers, SKL-18):**
  1. atomize-book split (H24) and ingest-article reference trimming.
  2. firecrawl split.
  3. pubmed-research-note dedupe.
  4. ml-concept-lab trim.
  5. Scripts: `vault_index.py`, digest window/dedup, verify's `mint-session`/`probe`.
  6. Optional code-explainer template (eval-gated).
  7. MEMORY split.
  8. Full eval suites (5 cases per skill).
- **Exit:**
  - Standard gates.
  - Release eval runs at or above the W3 scores. A move that drops a case score is reverted, not "fixed forward".
  - Every body ≤500 lines. Targets in §8 met.

### W5 — learn-hub CLAUDE.md relocation (only if D5 = move)

- **Entry:** W4 exit. The skills that receive gotchas have passing trigger evals (proof they load when needed).
- **Work:** move the ~58 pipeline/import gotchas verbatim into `references/gotchas.md` of atomize-book, ingest-article, sync-vault and vault-coverage, with one-line pointers. Update Documentation-upkeep.
- **Exit:** learn-hub CLAUDE.md ≤30k tok. A grep confirms that every moved heading exists exactly once in some skill reference. Standard gates.

---

## 10. Owner decisions (values or environment only)

| # | Question | Options | Recommendation | Trade-off |
|---|---|---|---|---|
| D1 | How should micky load on your Windows machine? (Wave 0 checks the current state.) | (a) local-directory marketplace (in place); (b) GitHub marketplace (cached copies) | **(a)** | In place, edits apply without bumps, and the vault, plugin-creator scripts and misread ledger resolve to the git checkout. The cost: whatever branch is checked out *is* what runs. With (b), every in-repo path must be guarded off, and the ledger can't live in git. |
| D2 | How should micky plugins reach cloud sessions? | (a) `CLAUDE_CODE_PLUGIN_DIRS` on your cloud environment(s), extended per wave; (b) enable the plugins on your claude.ai account (synced copies); (c) no micky plugins in the cloud | **(a)**, provided the W0 test passes | (a) is in place, works for multi-repo sessions, and needs one env-var edit per wave in each environment you use. (b) needs no env edits but gives copies, not in place: the ledger and vault-in-git break, and they also sync into terminal sessions. (c) keeps today's silent dead-ends. |
| D3 | In a cloud session that starts above both repos, where should a finished research report or rendered asset land by default? (Long term: keep both routes into the Learn hub?) | (a) ask once per session (option picker), then remember; (b) always the micky vault (vault-keeper, drained later by /empty-vault); (c) always learn-hub (`research-notes/` / ingest-*) | **(a)** now. Revisit collapsing to one route after W3. | (a) keeps both habits alive and costs one question per session. (b) and (c) are zero-question but break one of your two current workflows (the micky vault artifacts, or the research-notes/ flow you set up on 2026-08-11). |
| D4 | Two skills are named `psych-paper-digest`: your claude.ai daily digest (8–12 papers, 10 domains) and the micky watchlist digest (`/digest`). | (a) keep both names, sharpen both NOT-for boundaries, keep micky's local-only; (b) rename the claude.ai skill (e.g. `daily-psych-digest`); (c) rename the micky plugin (needs a `renames` entry; `/digest` unchanged) | **(a)**, plus **(b)** if no scheduled task or routine calls the claude.ai one by name | Without a rename, the listing keeps two overlapping descriptions and bare `/psych-paper-digest` runs micky's (SKL-55). Renaming the claude.ai skill is cheap but breaks any routine that names it. (c) disturbs an installed plugin id for little gain. |
| D5 | Should the ~58 pipeline/import gotchas leave learn-hub CLAUDE.md for the owning skills' references? | (a) move verbatim with one-line pointers (W5); (b) keep all in CLAUDE.md; (c) move without pointers | **(a)** | (a) saves ~35k always-loaded tokens in every learn-hub session, including multi-repo ones. The cost: a gotcha is seen only when its skill loads, and you add new pipeline gotchas to skill references instead of CLAUDE.md. (b) is status quo. (c) saves slightly more and loses discoverability. |
| D6 | Do you type `/atomize`, `/vectors`, `/pk-animation` or `/ingest` (i.e. is learn-hub-local installed on Windows)? | (a) keep dmi aliases for `/vectors` and `/pk-animation`, drop `/atomize` and `/ingest`; (b) keep all four; (c) drop all | **(a)** | `/atomize` collides with atomize-book, and `/ingest` belongs to a retired, hazardous plugin. Aliases cost nothing in Claude's listing (dmi) but add `/` menu entries. |
| D7 | Where should the misread ledger live? | (a) the in-place repo file, with an offer to commit after each capture (it crosses Windows and cloud); (b) `${CLAUDE_PLUGIN_DATA}` per machine (no git, no crossing, lost in ephemeral cloud containers); (c) a separate private file outside both repos, path configured per machine | **(a)** (the repo is private) | (a) is the only option that compounds across environments. The cost: personal priors live in git history, and each capture is a small commit. (b) is private and simple but is a fresh start per machine, which defeats its purpose. |
| D8 | Eval spend | (a) smoke per wave (free graders, one arm) + two-arm release runs at W3 and W4 exits, capped by `--max-cost-usd` you set; (b) smoke only; (c) full two-arm every wave | **(a)** | A full two-arm pass over ~20 skills × 5 cases × 3 runs is ~600 agent runs (EVL-27). (a) buys regression detection at the two riskiest points. (b) can't show that a rewrite didn't regress holistic quality. |

---

## 11. Risks

| # | Risk | Likelihood / impact | Mitigation |
|---|---|---|---|
| R1 | `CLAUDE_CODE_PLUGIN_DIRS` does not reach Claude Code in cloud sessions, or clone paths differ from `/home/user/<repo>`. Verified only locally. | medium / high (cloud delivery) | W0 gridgeist-only test. On failure, W2/W3 cloud steps pause and D2 is re-asked (claude.ai sync). W1 doesn't depend on it. |
| R2 | Listing overflow when ~17 micky skills join the cloud listing next to 14 learn-hub and 21 synced skills. The least-invoked skills lose their descriptions and stop auto-triggering (SKL-08, COM-08). | medium / high | Delivery grows per wave. dmi on commands. Description trims (§8). psych-paper-digest local-only, gridgeist optional. `/doctor` at each exit. |
| R3 | Multi-repo sessions don't run learn-hub hooks, so a sync without Chromium or `.env.local` leads to the diagrams-wipe class, and the duplication/repetition gates stay silent. | high (it is today's state) / high | The sync-vault precondition step (W1) runs the hook and gates by hand. The W1 exit includes a live, owner-approved sync check. |
| R4 | MCP endpoint dedup changes the callable tool prefix once plugins load in the cloud, so hard-coded prefixes fail and fall back to web. | high if unfixed / medium | Runtime tool resolution (§5.4) lands in W2 **before** the research writers join the cloud list. |
| R5 | Atomic swap of concept-animation: if any cloud environment lacks the env var, CA disappears there. | low / medium | The swap only runs after a new-session check in each environment the owner uses. Rollback is a revert plus the env-var log. |
| R6 | claude.ai `daily-random-review` chains into `comprehensive-review` by name. Once micky's copy loads in the cloud, unattended runs hit the intent-lock Step 0 and the vault filing. | medium / medium | The handoff fallback (§2.4) and the sink rule (D3). The W2 exit test is one unattended run. |
| R7 | Forks retired while learn-hub-local is installed on Windows leaves dangling installs. | low / low | W0 check (D6), then `claude plugin marketplace remove learn-hub-local` before deletion. |
| R8 | Description edits drop a habitual trigger (Thai) or shift routing between siblings. | medium / high | Trigger-lock validator. Near-miss negative evals. Old-vs-new comparison. The live routing smoke at W3. |
| R9 | Cross-repo contract drift reappears after the rewrite. | medium / medium | Copies plus the `check_cross_repo.py` gate, the consumers-first rule and the checker parity fixture. |
| R10 | In-place loading means uncommitted or experimental edits in the micky clone are live behaviour, locally and in the cloud. | medium / medium | Wave work happens on branches in a separate worktree. The owner's main checkout stays on master (the local marketplace points at it). |
| R11 | Eval noise: haiku judge variance, rate-limit zeros, mocks that diverge from real PubMed. | medium / low | Regex/tool graders first. Pinned models. Error-column check. Owner-approved live runs for research skills at W2. |
| R12 | Personal data in git (ledger) and personal context (Klaeng) in distributable text. | low (private repo) / low | D7. Klaeng removed from generic guidance. The ledger stays in the private repo. |
| R13 | Windows specifics: CRLF breaking frontmatter regexes, backslash paths, missing bash constructs. | medium / medium | validate.py is CRLF-safe and flags backslashes. The atomize-book BOOK loop moves into a script (W4). |
| R14 | PyMuPDF and other PDF tooling are absent in the cloud, so the PDF paths fail at run time. | high / medium | Preflight install steps in pdf-pipeline, ingest-article and ingest-slides (W1), plus an optional cloud setup-script line (owner). |
| R15 | Scope creep: a "light" edit becomes a re-voicing. | medium / medium | Each wave's diff is reviewed against §3's change list. Changes outside it need a named defect or a failing eval. |

---

## Appendix A — Checks run in this session (beyond the research files)

1. **`CLAUDE_CODE_PLUGIN_DIRS`**, CLI 2.1.280, run from the scratchpad with an isolated HOME:
   - With `/nonexistent/path:/home/user/micky-psych-tools/plugins/gridgeist`, `claude plugin list` printed `gridgeist@inline … Status: √ loaded` and `inline[0]: × Path not found: /nonexistent/path`, exit 0.
   - With `/home/user/micky-psych-tools/plugins` (a folder of plugins), all micky plugins loaded as `<name>@inline` with `Path:` pointing at the clone, i.e. in place.
   - Docs: "Project and local settings can't set this variable" (plugins.md L317); env-vars.md L334 gives the `:` separator and the absolute-path rule.
2. **Declared dependencies disable dependents:** plugin-dependencies.md — "You started a session without the dependency's `--plugin-dir` flag: Claude Code reports the dependency as not installed"; error `dependency-unsatisfied`: "A declared dependency is not installed, or it is installed but disabled."
3. **Multi-repo cloud sessions skip repo hooks:** cloud-environments.md L261 ("A session with several repositories … starts above the clones and doesn't read them") and L468 ("a session with several repositories doesn't load hooks from any repository's `.claude/settings.json`"). Skills, agents and commands in `.claude/` do carry over (L264).
4. **`@skills-dir` plugins load only from the primary working directory** (plugins-reference L413), so they are unusable for learn-hub in multi-repo sessions.
5. **Synced plugins vs other sources:** plugins-reference L454 — a same-named plugin from another source wins, and the synced copy is "not loaded".
6. **dmi on a command file:** a scratch copy of psych-paper-digest with `disable-model-invocation: true` added to `commands/digest.md` passed `claude plugin validate --strict` (exit 0). `claude plugin details` reports `digest ~40 tok` always-on with and without it, so listing savings from dmi must be measured with `/doctor`, not `plugin details`.
