# Target architecture — "best-practice purist" angle

Scope: every plugin, skill, command and tooling unit in `/home/user/micky-psych-tools` (14 plugins,
17 skills + 1 template `SKILL.md`, 12 commands, `scripts/{validate,route,bump}.py`, `ROUTING.md`,
`MEMORY.md`, `CLAUDE.md`) and `/home/user/learn-hub` (8 plugins in `learn-hub-local`, 11 project
skills, `CLAUDE.md`, `.claude/hooks`). Evidence ids: research claims `SKL-/PLG-/EVL-/COM-/LOC-nn`
(corrected claims used where the verdict was not "confirmed"); defects cite the inventory's
`file:line`. Mechanisms not in the research files were verified against the official docs
downloaded this session (`code.claude.com/docs/en/*.md`, 2026-09-23) — see Appendix A.

---

## 1. Thesis

The two repos are built on the pre-2026 model of Claude Code extensibility: one plugin per idea,
a slash command in front of every skill, a hand-written router in front of the descriptions,
state written into the plugin tree, contracts copy-pasted between plugins, and two copies of the
same version. Current official guidance replaces every one of those:

1. **Commands are skills** (SKL-01, SKL-02, PLG-15, COM-42). Zero `commands/` directories.
2. **A plugin is a self-contained, cache-copyable unit** (PLG-22, COM-38): anything two skills
   share must live *inside the same plugin*. So plugins are drawn around **families that share
   contracts** — four family plugins plus one vendored third-party plugin — not around single
   skills.
3. **Project-specific procedures are standalone project skills, not plugins** (docs
   `plugins.md` "When to use plugins vs standalone": standalone `.claude/` is for
   "project-specific customizations"; plugins for "reusable across projects"). Everything that
   only works inside learn-hub (all 5 native learn-hub plugins, all 11 project skills) and the
   marketplace's own maintenance tooling become project skills in the repo they operate on.
   The learn-hub marketplace is dissolved.
4. **The description is the router** (COM-03, SKL-12). `ROUTING.md`, `route.py`, `/route` and
   the "route first" CLAUDE.md mandate are deleted; routing quality is *measured* with trigger
   evals (PLG-54, EVL-17, EVL-36) instead of engineered with a 200-char regex (LOC-08).
5. **Deterministic work is code, judgment is prose** (SKL-23, SKL-31, COM-15, COM-16): every
   rule a regex or script can check leaves the SKILL.md and becomes a bundled, `--help`-documented,
   tested script invoked through `${CLAUDE_SKILL_DIR}`/`${CLAUDE_PLUGIN_ROOT}` (SKL-32, SKL-33).
6. **Bodies are small, references are conditional** (SKL-15..18, SKL-40): SKILL.md ≤ 500 lines /
   ≤ 5k tokens (target ≤ 300 lines / ≤ 3k), references one level deep with explicit "read X when
   Y" triggers, standing rules in the first 5k tokens because only those survive compaction.
7. **One version field, one eval system per home, one owner per contract**: version in
   `plugin.json` only (PLG-06, LOC-02); behavioural evals in `claude plugin eval` format at the
   plugin root (EVL-01..03, PLG-53); PubMed/CT.gov MCP declared once (PLG-34, PLG missed-practice
   on endpoint dedup); every cross-repo contract has exactly one canonical file and a parity check.
8. **State lives outside the plugin tree** (PLG-24, PLG-57): caches and dependencies in
   `${CLAUDE_PLUGIN_DATA}` (docs: "installed dependencies … generated code, and caches"),
   durable user-authored state (the misread ledger) in a git-tracked file resolved through
   `userConfig` → environment variable → default, because cloud containers discard
   `~/.claude/plugins/data`.
9. **Delivery is explicit per environment**: in-place loading everywhere the micky checkout
   exists (local-directory marketplace locally, `CLAUDE_CODE_PLUGIN_DIRS` in cloud — PLG
   missed-practice, docs `env-vars.md:334`), and an optional claude.ai-synced release channel
   for sessions that do not clone micky (routines, Cowork, single-repo learn-hub sessions).

The result: 55 potential listing entries today (17 micky skills + 12 commands + 11 learn-hub
project skills + 9 learn-hub plugin skills + 6 plugin commands, of which only 11 actually load in
cloud — LOC-42) collapse to **25 entries that all load in every environment that needs them**, with
roughly one third of today's listing text, and no unit that silently depends on a file it cannot
reach.

---

## 2. Target topology

### 2.1 Five placement rules (the whole design follows from these)

| # | Rule | Source |
|---|------|--------|
| R1 | A capability usable outside one specific repo ships in a **plugin** of the micky-psych-tools marketplace. | plugins.md table; PLG-22 |
| R2 | A procedure that reads/writes one repo's scripts, DB or layout ships as a **project skill in that repo** (`<repo>/.claude/skills/`), resolving the repo root from `${CLAUDE_SKILL_DIR}` (always co-located). | plugins.md table; cloud-environments carry-over ("`.claude/skills/` … Yes") |
| R3 | Skills that share a contract, script or reference live in **one plugin**; the shared file sits at `${CLAUDE_PLUGIN_ROOT}/references|scripts/` and every SKILL.md links it directly (one level deep). No symlinks, no `../` escapes. | PLG-22, PLG-23, SKL-16, COM-38 |
| R4 | Across plugins, a skill is reached **by name**, never by path ("REQUIRED SUB-SKILL: `alignment:intent-lock`"), with a stated fallback when absent; hard needs are declared in `plugin.json` `dependencies`. | COM-36, COM-37, PLG-37 |
| R5 | Across repos, a contract has **one canonical file + an executable check**; the other repo carries a pinned copy with a provenance header and a parity test that runs whenever both clones are present. | COM-39 (byte-identical twins), learn-hub's existing parity-test pattern |

### 2.2 micky-psych-tools — target tree

```
.claude-plugin/marketplace.json      # $schema, name, owner, description, plugins[{name,source,category}], renames{}
.claude/skills/plugin-workbench/     # PROJECT skill (R2): new | refine | release | check
  SKILL.md
  scripts/check.py  release.py  evals_to_cases.py  (+ tests/)
  references/house-rubric.md  description-rubric.md  eval-authoring.md
  assets/skill-template.md           # valid-YAML template (replaces {{placeholders}})
CLAUDE.md                            # ≤ 60 lines: conventions + health check only
MEMORY.md                            # ≤ 120 lines: open threads + decisions (no versions table)
README.md                            # install per environment; no plugin catalog copy
state/misreads.md                    # durable misread ledger (git-tracked; see 2.6)
vault/.vault-id                      # marker "micky-psych-vault" (replaces walk-up heuristic)
vault/…                              # content, managed by vault-keeper
plugins/
  alignment/                         # was intent-lock + decision-interview + plan-critique
    .claude-plugin/plugin.json       # version here only; userConfig{ledger_file}
    README.md  CHANGELOG.md  LICENSE
    references/interview-protocol.md # AskUserQuestion mapping, admission threshold, destructive
                                     # always-ask, stop/silence, autonomous fallback, surfacing lines
    references/lock-record.md        # callee contract: the slots intent-lock returns to callers
    scripts/ledger.py (+ tests)      # append / list / retire / validate misread entries
    skills/intent-lock/  skills/misread-capture/  skills/decision-interview/  skills/plan-critique/
    evals/<skill>/<case>/…
  evidence/                          # was pubmed-research-note + comprehensive-review + psych-paper-digest (+ firecrawl contract)
    .claude-plugin/plugin.json       # dependencies: ["alignment"]; mcpServers: "./.mcp.json"
    .mcp.json                        # THE ONLY PubMed + ClinicalTrials.gov declaration in both repos
    references/evidence-contract.md  # depth contract, Sources grammar (one NCT grammar), voice rule
    references/engines.md            # tool resolution, E-utilities/CT.gov v2 fallbacks, firecrawl CLI fetch contract
    scripts/sources_lint.py  watch.py  eutils.py (+ tests)
    skills/pubmed-research-note/  skills/comprehensive-review/  skills/literature-watch/
    evals/…  evals/mocks/pubmed/*.md  evals/mocks/clinical-trials/*.md
  visual-explainers/                 # was clinical-infographic + concept-animation + ml-concept-lab + code-explainer
    .claude-plugin/plugin.json       # dependencies: ["alignment"]
    references/html-artifact-contract.md   # self-contained, full document + color-scheme, layout shell,
                                           # reduced motion, a11y, honest footer, "illustrative" label
    references/sourcing.md           # session → vault query → generate via evidence (clinical lane)
    scripts/check_html.mjs  render_verify.mjs  code_fidelity.mjs (+ tests)   # parity-pinned to learn-hub audits
    skills/clinical-infographic/  skills/concept-animation/  skills/ml-concept-lab/  skills/code-explainer/
    evals/…
  vault-keeper/                      # keeps its name; becomes the single OUTPUT-SINK owner
    .claude-plugin/plugin.json       # userConfig{vault_root, learn_hub_root, output_sink}
    references/vault-layout.md  learn-hub-handoff.md (canonical copy owned by learn-hub, see 4.3)
    scripts/vault.py  drain_plan.py (+ tests)
    skills/vault-keeper/  skills/empty-vault/
    evals/…
  gridgeist/                         # vendored third-party, kept verbatim + UPSTREAM.md (repo, sha, date)
```

Removed from micky: `plugins/{pubmed-research-note,comprehensive-review,psych-paper-digest,intent-lock,
decision-interview,plan-critique,clinical-infographic,concept-animation,ml-concept-lab,code-explainer,
plugin-creator,firecrawl}` (content moved or retired), all 12 `commands/*.md`, `scripts/route.py`,
`scripts/bump.py`, `scripts/validate.py`, `ROUTING.md`. `renames` in marketplace.json maps each former
plugin name to its family (PLG-44; docs: "Map each former name to its current name, or to null").

### 2.3 learn-hub — target tree

```
.claude-plugin/                      # DELETED (marketplace dissolved)
plugins/                             # DELETED
CLAUDE.md                            # ≤ 200 lines (docs memory.md: "target under 200 lines")
.claude/rules/*.md                   # path-scoped app gotchas (paths: frontmatter), e.g. reader-focus-band.md,
                                     # infographic-viewer.md, db-cache.md, pwa.md, supabase-migrations.md
.claude/agents/book-drafter.md  book-auditor.md  depth-expander.md  diagram-adder.md
.claude/skills/
  pdf-pipeline/        # front door for pdf/epub/deck: deterministic classify → route → verify tail via sync-vault
  atomize-book/        # SPLIT: orchestrator SKILL.md + references/{extract,manifest,figures,measure,dedupe,qc}.md
  ingest-article/      # absorbs ingest-slides (references/slides.md, scripts/render_slides.py, extract_pdf.py)
  file-visualization/  # merges ingest-infographic + ingest-animation (+ filing half of the concept-animation copy)
  digest-report/       # back from plugins/ (was never loaded as a plugin)
  split-note/          # was plugin vault-atomizer (renamed: removes the "atomize" collision, P0-2)
  pk-animation/        # was plugin pk-plasma-animation (no .mcp.json; research via evidence plugin)
  sync-vault/          # SINGLE owner of the sync tail (background run, tells, revalidate, verify, purge)
  vault-audit/         # merges vault-vectors + check-repetition + vault-coverage (modes, conditional refs)
  verify/              # bundles mint_session.mjs + probe.mjs instead of prose
tools/source/          # neutral home for extract-figures/check-figures/measure-loss/measure-depth/qc-gate…
                       # (moved out of atomize-book/scripts; npm aliases `book:*`; tests run by `npm run test:py`)
docs/contracts/        # pinned copies of micky contracts (report format) with provenance headers
research-notes/        # the learn-hub OUTPUT SINK for evidence reports (written by vault-keeper, 2.6)
inbox/articles/        # gitignored drop folder (replaces C:\Users\User\Desktop\Learn\Raw Article PDF)
```

### 2.4 Ownership map (one owner per contract)

| Contract / resource | Canonical owner | Consumers (reach it by…) |
|---|---|---|
| Interview protocol, lock record, misread ledger | `alignment` plugin | evidence, visual-explainers, pk-animation — by skill name `alignment:intent-lock` (declared dependency for the two plugins) |
| Evidence contract (depth, Sources grammar, voice rule), report file format | `evidence` plugin (`references/evidence-contract.md` + `scripts/sources_lint.py`) | learn-hub `digest-report` via pinned copy `docs/contracts/report-format.md` + vendored linter, parity-checked |
| PubMed / CT.gov MCP servers | `evidence/.mcp.json` | pk-animation calls `evidence:pubmed-research-note` with a brief; nobody else declares servers |
| Where finished outputs go (psych vault vs learn-hub `research-notes/`) | `vault-keeper` (output sink) | every producer "files via `vault-keeper:vault-keeper`"; producers never resolve paths |
| HTML artifact contract + layout/self-contained/strip audits | **learn-hub** (`scripts/lib/animation-responsive.mjs`, `infographic-responsive.mjs`, `src/lib/animation-layout.ts` — the app renders them) | `visual-explainers/scripts/check_html.mjs` = pinned port with parity test |
| Vault → Learn handoff (manifest, handshake, asset routing) | **learn-hub** `digest-report` + `file-visualization` (the consumer defines its input) | `vault-keeper:empty-vault` via pinned `references/learn-hub-handoff.md` |
| Sync tail (apply, gates, revalidate, verify, purge) | learn-hub `sync-vault` + `scripts/apply-sync.mjs` | all learn-hub skills link to it; none restates it |
| Figure/loss/depth/QC tooling | learn-hub `tools/source/` | atomize-book, ingest-article (npm aliases, not another skill's path) |
| Marketplace validation / release | micky `plugin-workbench` project skill | CLAUDE.md health check line |

### 2.5 Delivery route per environment

| Environment | micky plugins | micky project skill | learn-hub project skills | Provisioning |
|---|---|---|---|---|
| **Local Windows terminal/desktop** | User-scope **local-directory marketplace** (`claude plugin marketplace add <path>`), loads in place: edits live at next session or `/reload-plugins`, no bump (PLG-09); enables `/plugin` UI + `userConfig` prompts (vault_root, learn_hub_root, ledger_file) | Loads when cwd is micky | Loads when cwd is learn-hub; cross-repo work (empty-vault) starts in one repo with `--add-dir <other>` (docs skills.md:153: "loads the skills in that directory's `.claude/skills/`") | learn-hub SessionStart hook still runs (single repo) |
| **Cloud, multi-repo (both clones, starts at `/home/user`)** — the owner's normal case | Cloud-environment env var `CLAUDE_CODE_PLUGIN_DIRS=~/micky-psych-tools/plugins` (folder of plugins; `:`-separated; absolute or `~`; v2.1.280+ — env-vars.md:334, plugins.md:317; project settings cannot set it) — loads in place, always the checked-out branch | Loads from the clone | Load from the clone (observed this session; docs skills.md:142 warns nested repos may load lazily — verified in Wave 0) | Setup script provisions the VM (PyMuPDF, pypdf, poppler-utils) — docs cloud-environments.md:468: multi-repo sessions do not run project hooks, "Install dependencies … with a setup script instead"; env vars `MICKY_ROOT`, `LEARN_HUB_ROOT`, `MISREAD_LEDGER`, `PUPPETEER_EXECUTABLE_PATH`; learn-hub skills run a readiness probe (2.6) instead of relying on the SessionStart hook |
| **Cloud, single repo (learn-hub only)** | Absent unless the synced release channel exists (OD-1) | — | Load; project hooks run | SessionStart hook as today |
| **Routines, Cowork, cloud sessions without the micky clone** | Only as **claude.ai-synced plugins** (docs plugins-reference "Plugins synced from claude.ai"; PLG-47 corrected) — optional release channel (OD-1) | n/a | n/a (cloud routines on learn-hub load its `.claude/skills`) | — |
| **claude.ai chat** | Out of scope: plugin skills are declared Claude-Code-only (use `when_to_use`, `argument-hint`, `disable-model-invocation`, `allowed-tools` with `${CLAUDE_SKILL_DIR}`) — SKL-04 | | | |

Precedence is safe by construction: a `--plugin-dir`/`CLAUDE_CODE_PLUGIN_DIRS` or marketplace copy
beats a same-named synced copy (docs: "When an enabled plugin from any other source matches a synced
plugin's name, Claude Code loads that plugin"), so dev sessions always run HEAD and routines run the
last release.

### 2.6 Configuration, roots and state

One resolver per plugin that needs it (not shared across plugins — R3), identical algorithm, each
a tested script:

`userConfig` value → environment variable → marker search (from cwd upward and siblings) → **stop
and ask**. Never `${CLAUDE_PLUGIN_ROOT}/../..` (PLG-58 corrected; inventory-infra vault-keeper
SKILL.md:29 "high"), never "nearest `.claude-plugin/marketplace.json`" (vault-keeper SKILL.md:28,
matches learn-hub — LOC-36).

| Value | Declared in | Cloud value (env var on the environment) | Marker |
|---|---|---|---|
| `vault_root` | vault-keeper `userConfig` (type directory) | `MICKY_ROOT=/home/user/micky-psych-tools` | `vault/.vault-id` = `micky-psych-vault` |
| `learn_hub_root` | vault-keeper `userConfig` | `LEARN_HUB_ROOT=/home/user/learn-hub` | `package.json` name `learn-hub` + `scripts/apply-sync.mjs` (replaces the deleted `.claude/skills/digest-report/` marker — empty-vault SKILL.md:36-37, "high") |
| `output_sink` | vault-keeper `userConfig`, `options: ["auto","psych-vault","learn-hub"]`, default `auto` (learn-hub if resolvable) | (default) | — |
| `ledger_file` | alignment `userConfig` (type file) | `MISREAD_LEDGER=/home/user/micky-psych-tools/state/misreads.md` | default `${CLAUDE_PLUGIN_DATA}/misreads.md` only as last resort (ephemeral in cloud) |
| Node/Python deps for scripts | `${CLAUDE_PLUGIN_DATA}` (lazy install in the script, compare-manifest pattern from the docs) | same | — |

`userConfig` rows appear in `/config` and non-sensitive values substitute into skill content
(PLG-35 + docs); in cloud the user settings do not carry over (cloud-environments table), hence
the env-var tier. Secrets (FIRECRAWL_API_KEY) are an environment API credential, never in a repo
(inventory-infra firecrawl SKILL.md:270 writes the key into `.env`, "medium").

learn-hub readiness: every learn-hub pipeline skill starts with one line
`` !`node ${CLAUDE_SKILL_DIR}/../../../scripts/ready.mjs --json || true` `` (dynamic context;
SKL-35 corrected — `|| true`, absolute path, runs for repo skills in cloud) that reports
`node_modules`, `.env.local`, `PUPPETEER_EXECUTABLE_PATH`, PyMuPDF; Step 0 says "if not ready,
run `bash <root>/.claude/hooks/session-start.sh`". This replaces the silent dependence on a hook
that multi-repo sessions never run.

---

## 3. Disposition table — every unit

Legend for disposition: keep · rewrite · merge · split · move · retire · convert-to-project-skill ·
convert-to-script. "Rewrite" always means: to the house SKILL.md shape (§4.4), description rubric
(§4.5), budgets (§7) and eval gate (§5).

### 3.1 micky-psych-tools plugins (14)

| Unit | Disposition | Target | Reason (evidence) |
|---|---|---|---|
| pubmed-research-note (1.7.0) | merge | `plugins/evidence` (rename entry → evidence) | Depth/citation/Sources/firecrawl contracts copy-pasted into comprehensive-review with drift: NCT grammar 3 variants (SKILL.md:221-222 vs tool-catalog.md:100 vs psych-paper-digest SKILL.md:118-119); byte-identical `.mcp.json` ×5 (PLG-34, LOC-13) |
| comprehensive-review (0.3.0) | merge | `plugins/evidence` | Same shared contracts; cites nonexistent "house rules" (SKILL.md:128); no engine-failure policy (SKILL.md:103-124) that its sibling has |
| psych-paper-digest (0.1.1) | merge | `plugins/evidence` | Shares engines + E-utilities fallback (sweep-recipes L48-52) with pubmed-research-note |
| intent-lock (0.4.2, 2 skills) | merge | `plugins/alignment` | Admission threshold, destructive always-ask, fallback, picker mechanics copied ×3 across the gates with drift (inventory-alignment group obs.: "Silence is a stop" vs "not a stop verdict", cap 3 vs 4) |
| decision-interview (0.1.1) | merge | `plugins/alignment` | Same family; no evals/README/CHANGELOG (find → 3 files) |
| plan-critique (0.1.0) | merge | `plugins/alignment` | Same family; stop rules in one 807-char bullet (SKILL.md:50) duplicating siblings |
| clinical-infographic (0.2.1) | merge | `plugins/visual-explainers` | Shared HTML contract R1-R15 restated in 4 renderers, 265 near-duplicate lines (inventory-renderers group obs.) |
| concept-animation (0.1.1) | merge | `plugins/visual-explainers` | Same; layout bug shared with ML (grammar:46 vs build-contract:140) |
| ml-concept-lab (0.1.0) | merge | `plugins/visual-explainers` | Same; the only verify recipe fails as written (build-contract.md:195-197, ERR_MODULE_NOT_FOUND) |
| code-explainer (0.1.0) | merge | `plugins/visual-explainers` | Same tail sections; asymmetric boundary with ML |
| gridgeist (0.1.0, vendored MIT) | keep | `plugins/gridgeist` + `UPSTREAM.md` (repo, sha, date); delete `skills/gridgeist/agents/openai.yaml` + `assets/` | Third-party, different author/licence — must not merge into an owner family; Codex-only metadata is dead weight (openai.yaml:1-9); upstream revision unrecorded (MEMORY.md:615-618). Keep/drop per OD-7 |
| plugin-creator (0.3.0, 2 skills, 3 cmds) | convert-to-project-skill | `micky/.claude/skills/plugin-workbench` | Only works with cwd = micky root and repo scripts not shipped in the cache (inventory-infra "high": cache holds only .claude-plugin, commands, skills, README, CHANGELOG); scaffolding duplicates `claude plugin init` (PLG-05) |
| vault-keeper (0.4.0, 2 skills, 1 cmd) | rewrite | `plugins/vault-keeper` (name kept) — becomes output-sink owner | Root resolution wrong for installed copies and matches learn-hub (SKILL.md:28-29, "high"×2); index job is prose (SKILL.md:96-103); CHANGELOG two releases behind (0.2.0 vs 0.4.0) |
| firecrawl (0.2.0) | retire | Engine/fetch contract → `plugins/evidence/references/engines.md`; general web use → vendor's own distributed skills/CLI (OD-6) | "Verbatim" vendor guide stale in load-bearing places (SKILL.md:146-147 build skills, :127 `ask`→`doctor`, :330 keyless REST — "high"); 4.2k-token body, 320 vendor lines (SKILL.md:19-338); vendor install adds a same-named `firecrawl` skill (SKILL.md:33) |

### 3.2 micky-psych-tools skills (17 + template)

| Unit | Disposition | Target | Reason (evidence) + key rewrite points |
|---|---|---|---|
| pubmed-research-note | rewrite | `plugins/evidence/skills/pubmed-research-note` | Body 4.7k tok + 5.9k mandatory refs (inventory); stale `Reframed:` preface vs intent-lock 0.4.2 (SKILL.md:263 vs intent-lock SKILL.md:226, "high"); decision-brief 4+3≠6 slot arithmetic (decision-brief.md:11-12, "high"); hard-coded `mcp__plugin_pubmed-research-note_*` + "No ToolSearch step" (tool-catalog.md:25-28); no absent-dependency path (SKILL.md:82,150); voice rule missing (LOC-28 P0-1). Rewrite: brief slots = lock-record slots; shared contract by link; engine default + escape hatch (SKL-24); filing = "file via vault-keeper"; `effort: high` only if evals show gain (SKL-39) |
| comprehensive-review | rewrite | `plugins/evidence/skills/comprehensive-review` | "No section without a number" vs thin-domain rule (SKILL.md:132-133 vs :35-36); "source floors" ambiguity (SKILL.md:108 vs :57); CT.gov status `completed-no-results` does not exist (review-arc.md:23); output location unspecified (SKILL.md:168) |
| psych-paper-digest | rewrite (rename `literature-watch`, OD-5) | `plugins/evidence/skills/literature-watch` + `scripts/watch.py` | Windows on `pdat` not `edat` (sweep-recipes.md:39-40, "high"); silent 50-result truncation (sweep-recipes.md:39-40 vs :92-93, "high"); dedup only vs newest digest (sweep-recipes.md:80-82); unexecutable 3-sweep health rule (config-schema.md:55-56); name collision with `anthropic-skills:psych-paper-digest` (SKL-55 corrected). All window/config/dedup/filename logic → `watch.py` (SKL-31). Candidate for `context: fork` (SKL-38) — decided by eval |
| intent-lock | rewrite | `plugins/alignment/skills/intent-lock` | Silent contract contradicted in ≥11 places, patched by "reinterpret these verbs" (SKILL.md:22, "high"); claude.ai picker types (`rank_priorities`, SKILL.md:160-162) not AskUserQuestion; no fallback when picker is absent (subagents, headless, remote transport errors — MEMORY records 3 incidents; "high"); version-history narration (SKILL.md:24,95,99,101…); 6.2k tokens loaded as Step 0 by 5+ callers; `craft my prompt` trigger vs "never emit a prompt" (SKILL.md:3 vs :247). Rewrite: ≤ 2.5k tokens; picker semantics from `interview-protocol.md`; explicit callee mode returning the `lock-record.md` slots |
| misread-capture | rewrite | `plugins/alignment/skills/misread-capture` + `scripts/ledger.py` | Writes state into `${CLAUDE_PLUGIN_ROOT}` (SKILL.md:39 — PLG-57, LOC-37, "high"); `Prior:` has no eliciting question (SKILL.md:26-55, "high"); ledger contents violate its own rules (third person, ordering; misreads.md:34 vs :46); "review/edit priors" mode promised, absent. Ledger moves to `ledger_file` (2.6); script enforces grammar/ordering/cap-7 |
| decision-interview | rewrite | `plugins/alignment/skills/decision-interview` | Unprompted trigger drops the materiality threshold (SKILL.md:3 vs :15, :43); undetectable fallback conditions (SKILL.md:81); no evals |
| plan-critique | rewrite | `plugins/alignment/skills/plan-critique` | Command/skill disagree on no-plan case (critique-plan.md:10-11 vs SKILL.md:24); drafting hand-off to intent-lock unreachable (evals id 3); lens list duplicated ×8 with name drift; mega-bullets (SKILL.md:30, :50) |
| clinical-infographic | rewrite | `plugins/visual-explainers/skills/clinical-infographic` | Template ships a `prefers-color-scheme:dark` block learn-hub documents as a bug (infographic-template.html:100-104, "high"); `.mech` strip cramps on phones (template:74-75,93, "high"); AA contrast claim false (3.41:1 / 4.14:1); sub-12px text vs own minimum; assets dead-end in `vault/assets` (SKILL.md:143-146 vs empty-vault:55-56); lessons-learned.md is a narrative (SKL-25) |
| concept-animation | rewrite | `plugins/visual-explainers/skills/concept-animation` (absorbs learn-hub copy's layout fixes) | Prescribes the stage-collapse rule (animation-grammar.md:46,48 — 75/75 phone rows collapsed, "high"); single 1366×768 fit check proven blind (SKILL.md:145-150, "high"); stale viewer geometry; doctype-less example; no ML boundary; no evals |
| ml-concept-lab | rewrite | `plugins/visual-explainers/skills/ml-concept-lab` | Same layout bug (build-contract.md:140-141, "high"); verify recipe fails (build-contract.md:195-197, "high"); relative-error gradient check contradicts own example (build-contract.md:103 vs examples/README.md:63-66); clinical routing contradicts itself (SKILL.md:13-14 vs :237-239); wrong example path (SKILL.md:117-118); ~10.8k tokens per full load |
| code-explainer | rewrite | `plugins/visual-explainers/skills/code-explainer` + `scripts/code_fidelity.mjs` | Primary template never existed (SKILL.md:67-68,136, "high"); byte-fidelity check is prose (explanation-contract.md:145-146); `<button>` cards invalid HTML; Dark+ vs Dark Modern naming |
| gridgeist | keep | `plugins/gridgeist/skills/gridgeist` | Lean (1.1k tok), conditional references already correct; vendored text stays verbatim (edits would fork upstream) |
| plugin-creator | merge | `micky/.claude/skills/plugin-workbench` (mode `new`: wraps `claude plugin init` + house rubric + `claude plugin eval init --bare`) | Repo-bound (above); breaks its own description rule (authoring-rules.md:33 vs SKILL.md:3); scaffold fails its sibling audit (no README/CHANGELOG/evals — SKILL.md:57-59 vs audit-checklist.md:67-69); stale Not-for (LOC-22) |
| refine-plugin | merge | `plugin-workbench` (modes `refine`, `release`) | Bumps without CHANGELOG (SKILL.md:58-68 → vault-keeper CHANGELOG 2 releases behind); second-person description |
| templates/SKILL.md (plugin-creator reference) | retire | Replaced by `claude plugin init` scaffold + `plugin-workbench/assets/skill-template.md` | `{{PLACEHOLDER}}` is invalid YAML (templates/SKILL.md:2,8 — PyYAML ConstructorError); orphaned evals.json template |
| vault-keeper | rewrite | `plugins/vault-keeper/skills/vault-keeper` + `scripts/vault.py` | Root resolution (above, "high"×2); "Four jobs" vs five (SKILL.md:10 vs plugin.json:4); dangling-vs-broken link contradiction (SKILL.md:66-67 vs :101); Obsidian links by title with kebab filenames, no aliases; index rebuild as prose. New job: output-sink routing (psych vault ↔ learn-hub `research-notes/`) — removes the need for the learn-hub forks |
| empty-vault | rewrite | `plugins/vault-keeper/skills/empty-vault` + `scripts/drain_plan.py`; `disable-model-invocation: true`; `argument-hint: "[topic]"` | Stale learn-hub marker (SKILL.md:36-37, "high"); deletes assets learn-hub waits for (SKILL.md:55-57 vs ingest-infographic:136-137, "high"); Windows path (SKILL.md:39); `digest-report` unreachable (SKILL.md:63-64). Rewrite as plan-validate-execute (SKL-29): manifest file → validator → move → verify (provenance count) → delete on committed state; assets routed to `file-visualization` |
| firecrawl | retire | `plugins/evidence/references/engines.md` (fetch-only contract: clean markdown + URL + access date) | See 3.1; also 45 lines of the body are the only repo-specific value (SKILL.md:340-384) |

### 3.3 micky-psych-tools commands (12)

All thin wrappers fold into the target skill's frontmatter (`argument-hint`, `$ARGUMENTS`, named
`arguments`) — SKL-01, SKL-34, PLG-18, COM-42. The skill's bare `/name` keeps working unless shadowed
(PLG-17). LOC-17 corrected: 11 are wrappers, `/route` is a procedure.

| Unit | Disposition | Target | Reason |
|---|---|---|---|
| `/new-plugin` (plugin-creator) | merge | `plugin-workbench` `argument-hint: "new <purpose> \| refine <plugin> \| release <plugin> <patch\|minor\|major> \| check"` | Omits router step (new-plugin.md:12-13); duplicates skill |
| `/refine-plugin` | merge | `plugin-workbench` | Same |
| `/route` | retire | — (descriptions + NOT-for boundaries + trigger evals) | Reads then regenerates ROUTING.md (route.md:6 vs :9); writes to answer a read-only question; re-does native matching (LOC-09) |
| `/empty-vault` | merge | `vault-keeper:empty-vault` (`disable-model-invocation: true`, `argument-hint: "[topic]"`) | Wrapper; kebab→MOC mapping undefined (empty-vault.md) → handled by `drain_plan.py` |
| `/comprehensive-review` | merge | `evidence:comprehensive-review` `argument-hint: "[disorder or topic]"` | Wrapper |
| `/digest` | merge | `evidence:literature-watch` `argument-hint: "[domain]"` | Wrapper |
| `/infographic` | merge | `visual-explainers:clinical-infographic` | Wrapper; summary lags skill (omits signature visual, Step 2.5) |
| `/animate` | merge | `visual-explainers:concept-animation` | Wrapper; also collides with learn-hub copy's `/animate` trigger |
| `/visualize` | merge | `visual-explainers:ml-concept-lab` | Wrapper; repeats stale "fits one screen" checklist |
| `/explain-code` | merge | `visual-explainers:code-explainer` | Wrapper; contradicts skill on empty args (explain-code.md vs SKILL.md:95) |
| `/resolve-decisions` | merge | `alignment:decision-interview` | Wrapper |
| `/critique-plan` | merge | `alignment:plan-critique` | Wrapper; contradicts skill on no-plan case |

Short verbs (`/animate`, `/digest`…) are lost unless the owner chooses otherwise (OD-8).

### 3.4 micky-psych-tools repo tooling and docs

| Unit | Disposition | Target | Reason |
|---|---|---|---|
| `scripts/validate.py` | rewrite | `.claude/skills/plugin-workbench/scripts/check.py` | Crashes with traceback on malformed input (validate.py:72-73,111-114, "high"); hand-rolled YAML miscounts quoted descriptions (:41) and passes invalid YAML; rejects valid stdio MCP (:93, LOC-11/12); README overstates coverage vs CLI. New check.py = `claude plugin validate --strict --json` on marketplace root **and** every plugin dir **and** both `.claude/skills` dirs (SKL-49 corrected, PLG-10, PLG-11) + only the house rules the CLI lacks (list in §5.1) |
| `scripts/route.py` | retire | — | Lossy copy of descriptions (29/29 cues verbatim substrings, 15/29 truncated, 0 NOT-for — ROUTING defect "medium"); writes on `--help` (route.py:114-115); shapes description wording (LOC-08) |
| `ROUTING.md` | retire | — | ~5k tokens mandated per request (CLAUDE.md:12-14); stale versions after bump (route.py:145, bump.py:57); invisible in isolated evals anyway (EVL-19) |
| `scripts/bump.py` | rewrite | `plugin-workbench/scripts/release.py` | Dual-write contradicts docs (PLG-06, LOC-01/02); ASCII escapes + no trailing newline (bump.py:53, LOC-45); no CHANGELOG, no dry run, writes before validate (bump.py:53-57). release.py: edit `plugin.json` only (ensure_ascii=False, newline), prepend CHANGELOG stub, run check.py, `claude plugin tag --dry-run` then `--push` on confirmation (PLG-39, PLG-40) |
| `MEMORY.md` | rewrite | ≤ 120 lines: open threads, recorded decisions, cloud-environment settings; no versions table (plugin.json is truth), no plugin summaries, content-filing log → git history | 108 KB / 1,153 lines, mandated first read ~27k tok, ~31 of 51 milestones are vault filings (LOC-25); versions table duplicates manifests |
| `CLAUDE.md` (micky) | rewrite | ≤ 60 lines: layout (tree above), the five placement rules, health check `python3 .claude/skills/plugin-workbench/scripts/check.py`, commit convention, pointer to MEMORY.md (not mandated) | 69% is a plugin catalog duplicated on 6 surfaces with drift (gridgeist missing — LOC-24); mandates ROUTING + MEMORY reads (~32k tok); stale version-parity rule (CLAUDE.md:40) |
| `.claude-plugin/marketplace.json` | rewrite | `$schema`, `description`, entries `{name, source, category}` only, `renames` map, no top-level or entry versions | 9/14 descriptions drift from plugin.json (catalog defect); PLG-06, PLG-42 (one home for display text) |
| `README.md` (root) | rewrite | Install per environment (§2.5); `claude plugin validate --strict` per dir; no catalog copy | Wrong "must be public" (README:15, LOC-40); validation command lacks `--strict` (README:54) |
| `docs/superpowers/plans/2026-07-10-improve-all-plugins.md` | retire (archive note) | — | All 11 tasks done, 61 unchecked boxes (LOC-27) |

### 3.5 learn-hub plugins (8) + their commands + catalog

| Unit | Disposition | Target | Reason |
|---|---|---|---|
| `learn-hub-local` marketplace.json | retire | — | Never registered/enabled, so none of its plugins load (inventory-learnhub-plugins "high"; LOC-41); fails `--strict` (PLG-12); name collisions ×3 with micky |
| intent-lock (fork 0.4.2) | retire | consume `alignment` (micky) | Byte-identical except README; splits the ledger in two ("high" — two misreads.md); `decision-interview` hand-off target absent in learn-hub |
| pubmed-research-note (fork 1.7.0) | retire | consume `evidence:pubmed-research-note` + `vault-keeper` sink `learn-hub` | Fork is a filing-path delta implemented as a full copy (PLG-59 corrected, LOC-33); evals fail by construction (evals.json:56,128 vs fork SKILL.md:162, "high"); writes report twice (SKILL.md:153-159) |
| comprehensive-review (fork 0.3.0) | retire | same | Auto digest + live Supabase write by default ("high": fork SKILL.md:166-176 vs digest-report's own "on atomize" trigger) |
| digest-report (0.1.0) | convert-to-project-skill | `learn-hub/.claude/skills/digest-report` | Unreachable as a plugin while 5 routes name it ("high"); input contract demands inline citations producers forbid ("high": SKILL.md:88-90 vs pubmed SKILL.md:211) → rewritten against pinned `docs/contracts/report-format.md` (`## Sources` block); Windows `Get-CimInstance` (SKILL.md:174); stale ~40-min sync claim (:165-167) → link to sync-vault |
| source-to-vault (skill ingest-source) | retire | — (pdf-pipeline → atomize-book / ingest-article) | Writes production rows with no /vault source ("high"); no-arg batch-ingests `Book/` with auto-apply ("high"); trigger collision with no NOT-for ("high"); omits embedding/diagrams/images ("high") |
| vault-atomizer | convert-to-project-skill | `.claude/skills/split-note` (renamed) | Repo-bound; "atomize" name collision (P0-2, LOC-31); stale stats (SKILL.md:9-10); foreground sync (SKILL.md:157) → link to sync-vault; depth-floor conflict with atomize-book unresolved (P1-6) → one threshold constant shared in `tools/source/depth_lib` |
| vault-vectors | merge | `.claude/skills/vault-audit` (mode `vectors`, `references/vectors.md`) | Repo-bound; command contradicts skill on syncing (vectors.md:10 vs SKILL.md:54-57); stale counts; overlaps sync-vault step 6 |
| pk-plasma-animation | convert-to-project-skill | `.claude/skills/pk-animation` | Repo-bound (scripts/animations/pk-plasma); 4th copy of the MCP servers (.mcp.json:3-10); brief's Sources format contradicts pubmed-research-note (pubmed-research-plan.md:91 vs SKILL.md:219-221) → brief rewritten to evidence contract; filing delegated to `file-visualization` instead of hand-built upsert (SKILL.md:112-114) |
| `/digest-report` | merge | `digest-report` skill `argument-hint: "[report-path …]"` | Conflicting "pending reports" semantics with the skill (commands:11-20 vs SKILL.md:22-24) — skill defines: no-arg = survey then stop |
| `/ingest` (source-to-vault) | retire | — | Parent retired |
| `/atomize` (vault-atomizer) | merge | `split-note` `argument-hint: "[<note-id>] [--list] [--apply]"` | Name collision removed |
| `/vectors` | merge | `vault-audit` `argument-hint: "vectors [--audit\|--check] \| repetition [--prefix p] \| coverage [<book>]"` | Undefined `--no-report` flag, wrong timing promise |
| `/pk-animation` | merge | `pk-animation` `argument-hint` | Wrapper |
| `/comprehensive-review` (fork) | retire | — | Parent retired |

### 3.6 learn-hub project skills (11)

| Unit | Disposition | Target | Reason |
|---|---|---|---|
| atomize-book | split | `SKILL.md` ≤ 450 lines orchestrator (copyable checklist SKL-28, standing rules, gotchas that bite imports) + `references/{extract,manifest,figures,measure,dedupe,qc}.md` (TOC each) + `.claude/agents/{book-drafter,book-auditor,depth-expander,diagram-adder}.md` (from references/drafting-agent.md templates) + `tools/source/` for its Python | 1,256 lines / 21.3k tokens every trigger ("high"); self-contradiction on `[[topic-id]]` (SKILL.md:295-296 vs :1027-1029, :1063-1067 vs CLAUDE.md:2588, "high"); stale whole-vault sync economics (:1116-1117, "high"); four drafting rules missing (`\$`, EQ-as-PNG, stadium ban, LIVE_GROUPS — "high"); one-level glob contradicting itself (:80 vs :90-91); MCP-validator vs `scripts/check-mermaid.mjs`; five repeated bash array loops → one `run_gates.py`; PyMuPDF absent → setup script |
| ingest-article | rewrite | `.claude/skills/ingest-article` (+ absorbs ingest-slides) | Windows inbox + repo-relative `rm` ("high": SKILL.md:3,49,51,348) → `inbox/articles/` gitignored, deletion only in explicit `inbox` mode; `book:source-cover` command cannot run on an article ("high": figures-and-loss.md:455-458 vs measure-source-cover.mjs:70); description 1,137 chars + invalid YAML (SKL-51/52); ~18.7k tokens mandatory per run → conditional refs; `{}` diagrams fallback violates bake rule (SKILL.md:337-341); calls atomize-book scripts by path (SKILL.md:80) → `tools/source` npm aliases |
| ingest-slides | merge | `ingest-article` (`references/slides.md`, `scripts/render_slides.py`, `extract_pdf.py`) | Script paths wrong from repo root ("high": SKILL.md:62,71); reuses article schema "wholesale" but none of its gates (SKILL.md:22-24); pdf-pipeline routes decks elsewhere ("high"); 1,150-char description; "grilling" remnants |
| ingest-infographic | merge | `.claude/skills/file-visualization` | Structural twin of ingest-animation (~70% same); dead empty-vault trigger ("high": SKILL.md:3,137-138); wrong "targeted upsert = npm run sync" claim ("high": SKILL.md:116-118); stale `/infographic` route; invalid YAML |
| ingest-animation | merge | `.claude/skills/file-visualization` | Same dead trigger ("high"); misses the two universal animation defects (layout + quirks mode — SKILL.md:88-98) → file-visualization runs `auditAnimationLayout` and refuses/returns |
| concept-animation (learn-hub copy) | merge | authoring → micky `visual-explainers:concept-animation` (layout fixes upstreamed, LOC-34); filing/topic-id/sidecar → `file-visualization`; builder pattern → `pk-animation` | Duplicate name + triggers with micky (`/animate`); newer on layout, older on YAML/structure; stage floor `min()` without `max(220px,…)` (grammar:58); verify omits 844×390 (SKILL.md:129); `npm run sync` contradiction (SKILL.md:171); stale builder path (SKILL.md:94) |
| pdf-pipeline | rewrite | `.claude/skills/pdf-pipeline` + `scripts/classify_pdf.py` (DOI/abstract/TOC/ISBN/page-count probe → suggested route, judgment only on edge cases) | Sends decks to atomize-book mini, never names ingest-slides ("high": SKILL.md:98, routing.md:42,60); unmeetable apply rule (≲200 KB vs 5.8 MB, "high"); nested vault path trap (SKILL.md:36); stale surfaces (graph removed); duplicates sub-skills' tail against its own "delegate, don't duplicate" (SKILL.md:199) |
| sync-vault | rewrite | `.claude/skills/sync-vault` (single owner of sync ops) | Recommends the nested-layout trap ("high": SKILL.md:126-132 vs CLAUDE.md:2697); default MCP path unusable at vault size ("high": SKILL.md:32-34); operational traps (background job, EXIT=0 + Upserted, no `&` in run_in_background, TaskStop zombie, fetch-first, readiness) live only in CLAUDE.md:1680-1770; deletion ignores `merge_note_history`/purge:hidden. Gates move into `apply-sync.mjs` preflight (4.6) |
| vault-coverage | merge | `vault-audit` (mode `coverage`, `references/coverage.md`) | Windows `BOOK_ROOT` (SKILL.md:40) → env/arg; source map 26 vs 70 books (no import step adds entries) → atomize-book checklist item |
| check-repetition | merge | `vault-audit` (mode `repetition`, `references/repetition.md`) | No NOT-for vs sibling redundancy tools; revalidation inconsistency (SKILL.md:88) → link to sync-vault |
| verify | rewrite | `.claude/skills/verify` + `scripts/mint_session.mjs`, `scripts/probe.mjs` | Referenced scripts never bundled (SKILL.md:41-43, "medium"); no triggers / NOT-for (vs browser pane, chrome-devtools isolated world gotchas) |

### 3.7 learn-hub CLAUDE.md and hooks (as they relate to skills)

| Unit | Disposition | Target | Reason |
|---|---|---|---|
| learn-hub `CLAUDE.md` (3,126 lines, ~67k tok) | split | Core `CLAUDE.md` ≤ 200 lines (stack, access model, data-model summary, vault format, testing rule, doc-upkeep rule); ~58 pipeline gotchas → the owning skill's Gotchas section or a triggered reference (SKL-30, COM-18); app/component gotchas → `.claude/rules/*.md` with `paths:` (docs memory.md:51, :154-212); obsolete/historical narrative → `docs/gotchas-archive.md` (not loaded). A **mapping table** (every one of the 136 gotcha headings → destination) is an exit artefact | Docs: "target under 200 lines"; "If an entry is a multi-step procedure or only matters for one part of the codebase, move it to a skill or a path-scoped rule" (memory.md:51, :82); SKL missed-practice (procedures in CLAUDE.md belong in skills); gotcha drift in both directions (inventory-learnhub-project-skills group obs. a-d) |
| `.claude/settings.json` hooks + `.claude/hooks/pre-sync-*.sh` | rewrite | Duplication and repetition gates become the first step *inside* `apply-sync.mjs`/`sync-vault.mjs` (same warn-only semantics, same `isSyncCommand` module); SessionStart stays for single-repo sessions; readiness probe in skills for multi-repo | Multi-repo cloud sessions never load project hooks (cloud-environments.md:261,468); a gate inside the script runs identically on Windows, cloud and in any session layout; removes two node spawns per Bash call (LOC-44) |

---

## 4. Shared-content strategy

### 4.1 Inside a plugin (the default mechanism)

- Shared files live at the plugin root: `references/*.md`, `scripts/*`. Each SKILL.md links the
  ones it needs **directly** (`${CLAUDE_PLUGIN_ROOT}/references/interview-protocol.md`) with a
  load condition ("Read `interview-protocol.md` before asking the first question"; SKL-18, COM-12).
  This satisfies one-level-deep (SKL-16) and survives cache copies (PLG-22) because nothing leaves
  the plugin directory.
- Family contracts that move into plugin-level references (each stated **once**):
  - `alignment/references/interview-protocol.md`: admission threshold; destructive/irreversible/
    outward-facing always-ask; AskUserQuestion mapping (1–4 questions, 2–4 options, `multiSelect`,
    automatic "Other" — so no manual escape option, no `rank_priorities`); one family question cap
    with its rationale; silence semantics (one wording: "a rejected or unavailable picker routes to
    the autonomous fallback"); autonomous fallback (reversible → stated default in one
    `Assumed: … — say if wrong` line; destructive → written decision request and halt); ledger
    vocabulary (four things currently called "ledger" get four names).
  - `alignment/references/lock-record.md`: the callee contract — the slots intent-lock returns when
    another skill calls it (deliverable, question, scope in/out, emphasis, audience, exclusions,
    assumed defaults). Replaces the drifted `Assumed/Reframed/Skipped` preface.
  - `evidence/references/evidence-contract.md`: depth contract, `## Sources` grammar (one NCT line
    grammar), no inline citations, direct-voice rule (P0-1), numbers rule with the thin-domain
    exception resolved. `evidence/scripts/sources_lint.py` enforces the mechanical half.
  - `evidence/references/engines.md`: default engine + narrow escape hatches (SKL-24): PubMed via
    the plugin server, resolved by tool name (`search_articles`, …) not by a hard-coded prefix
    (inventory: prefix wrong whenever a connector wins; endpoint dedup — PLG missed-practice),
    E-utilities with `datetype=edat` + `retstart` pagination, CT.gov `advanced_query`
    `AREA[...]RANGE[...]`, PubMed-down = fatal, registry-down = degrade, firecrawl CLI fetch-only.
  - `visual-explainers/references/html-artifact-contract.md`: R1–R15 from the renderers inventory,
    stated once, with the learn-hub layout fixes (min-height floor, `.wrap>*{flex:0 0 auto}`,
    `max(220px,min(38dvh,280px))`, full document + `color-scheme`, light-lock for infographics).
  - `vault-keeper/references/vault-layout.md`: single source (today restated in 6 places).
- Scripts replace the policing prose (SKL-31, COM-15/16): every script has `--help`, JSON on
  stdout, diagnostics on stderr, meaningful exit codes, `--dry-run` for writes (SKL-32), and is
  invoked through the interpreter (`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/x.py`, COM-46) with a
  matching `allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/x.py *)` so no permission
  prompt (SKL-33). Every script ships unit tests run by check.py.

### 4.2 Between plugins in the marketplace

- Delegation by skill name with requirement markers and a fallback line (COM-36/37):
  "REQUIRED SUB-SKILL: `alignment:intent-lock` — if unavailable, run the declared-reading fallback
  in `evidence-contract.md` §Step 0". This fixes the "mandatory Step 0 with no absent path" defects
  (pubmed SKILL.md:82,126; comprehensive-review SKILL.md:64; inventory-alignment group obs.).
- `plugin.json` `dependencies` only for hard needs: `evidence → alignment`, `visual-explainers →
  alignment` (PLG-37). Filing (`vault-keeper`) and generate-first (`evidence` from visuals) stay
  soft references with fallbacks, because a declared dependency that is absent disables the
  dependent plugin (docs plugin-dependencies.md:120-121).
- Producers never resolve vault or learn-hub paths; they hand vault-keeper a payload
  (`type: report|asset|note`, title, topic, source skill, file) and vault-keeper routes it to the
  configured sink. That single change deletes the reason the learn-hub forks exist.

### 4.3 Across the two repos

| Contract | Canonical file | Pinned copy | Parity check |
|---|---|---|---|
| Report format (frontmatter + `## Sources`) | `micky/plugins/evidence/references/evidence-contract.md` §Report format + `scripts/sources_lint.py` | `learn-hub/docs/contracts/report-format.md` + `learn-hub/scripts/lib/sources-lint.*` (port) | check.py `--parity` (micky) and a vitest parity test (learn-hub) compare the provenance header's sha256 with the canonical file when the sibling clone is present; fixtures shared |
| HTML/layout audits | `learn-hub/scripts/lib/animation-responsive.mjs`, `infographic-responsive.mjs`, `src/lib/animation-layout.ts` | `micky/plugins/visual-explainers/scripts/check_html.mjs` (header: `generated from learn-hub@<sha>`) | Golden fixtures: the same HTML files must produce identical findings in both (learn-hub already proved the audits flag the micky examples) |
| Vault → Learn handoff | `learn-hub/docs/contracts/vault-handoff.md` (owned by digest-report + file-visualization) | `micky/plugins/vault-keeper/references/learn-hub-handoff.md` | Same sha check |

Why not symlinks or a shared third repo: symlinks out of a plugin are dropped or dereferenced only
on copy (PLG-23) and Windows checkouts default to `core.symlinks=false`; a third repo would need its
own delivery route in every environment. Byte-identical twins with a parity test are the pattern
Anthropic's own skills repo uses (COM-39) and learn-hub already uses (mermaid-split, tag-canon).

### 4.4 House SKILL.md shape (one template for all 25 skills)

```
---
name: <kebab == dir>
description: >-            # quoted/folded so strict YAML parses (SKL-51)
  <third-person capability clause, no steps>. Use when <situations, key nouns>. Not for <near
  sibling> (use <plugin:skill>).
when_to_use: <extra phrasings incl. Thai triggers>          # Claude-Code-only, counts to 1,536
argument-hint: "[…]"                                         # replaces commands/
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/* *) # narrow; never a fence (SKL-37)
disable-model-invocation: true                               # only destructive/user-timed skills
---
# <Title>
Purpose (≤3 lines)
## Standing rules        (≤10, each "do X, because Y" — SKL-22 corrected; caps only for
                           never-fabricate / move→verify→delete — COM-20)
## Checklist             (copyable — SKL-28)
## Steps                 (labelled high/medium/low freedom — SKL-23)
## Gotchas               (harvested from misreads/corrections — SKL-30, COM-18)
## Hand-offs             (REQUIRED SUB-SKILL lines + fallback)
## References            ("Read X when Y" only)
```
No version history, dates, measured counts or "the old version" narration in bodies (SKL-25;
inventory: pubmed SKILL.md:32,61,293; intent-lock SKILL.md:24,95,99; vault-atomizer:9-10).

### 4.5 Description rubric (resolves the SKL-09/SKL-10/COM-01/COM-04 conflict)

One short third-person capability clause (what, as a noun phrase — never a step sequence, per
COM-01/COM-02) + `Use when …` with the concrete nouns users type (COM-03, SKL-12) + `Not for …
(use X)` naming the nearest sibling (COM-06). Key use case inside the first 150 characters
(SKL-07). Extra phrasings go to `when_to_use`. No first/second person outside quotes (SKL-09).
The description is accepted only when its trigger evals pass (§5) — char counts are a budget,
not evidence (PLG-54, EVL-17).

---

## 5. Evals strategy

Four layers, each in its documented home (EVL-41), no runner the repo has to build.

### 5.1 Layer 1 — static (every change, free): `check.py`

`claude plugin validate --strict --json` on the marketplace root, **each** plugin dir, and both
`.claude/skills` dirs (a marketplace run never opens skill files — PLG-10, SKL missed-practice),
plus the house rules the CLI lacks:
1. Strict YAML parse of every SKILL.md/agent frontmatter (SKL-50/51) and a frontmatter field
   whitelist (typos are silently ignored — SKL-03).
2. Name == dir; 1–64 chars; no leading/trailing/double hyphen; no "claude"/"anthropic" (SKL-05/06).
3. Description ≤ 1,024 hard, ≤ 500 warn; description + `when_to_use` ≤ 1,536 hard, ≤ 800 warn;
   no first/second person outside quotes (warn).
4. Body ≤ 500 lines and ≤ 5,000 tokens (chars/4) hard; ≤ 300 lines warn (SKL-15).
5. Every `references/` file is linked from SKILL.md; no reference-to-reference chains; files > 100
   lines have a Contents block; every relative link and `${CLAUDE_*}` path resolves (would have
   caught code-explainer's missing template — inventory "high").
6. No `${CLAUDE_PLUGIN_ROOT}/..`, no writes targeting `${CLAUDE_PLUGIN_ROOT}`, no backslash or
   absolute user paths (`C:\Users`, `/home/user`) in skill text (SKL-27, PLG-21).
7. Scripts invoked through an interpreter (COM-46); no leftover `{{…}}`; no unescaped `$<digit>`
   in prose (SKL-34).
8. `plugin.json` has semver `version`; marketplace entries carry no `version`/`description`;
   CHANGELOG top entry == version; README present; no `commands/` directories.
9. Evals present per skill with the minimums in 5.3; no `evals.json` left in plugins; `evals/results/`
   gitignored (EVL-26).
10. Cross-repo parity hashes (§4.3).
11. Unit tests of every bundled script (pytest/unittest, `node --test`) — including learn-hub's
    354 atomize-book tests via `npm run test:py`, which `npm test` does not run today (EVL-41).

### 5.2 Layer 2 — behaviour: `claude plugin eval` at each plugin root

- Layout `plugins/<p>/evals/<skill>/<case>/{prompt.md|case.yaml, graders/*.md}`, grouped by skill
  (EVL-06), tags `smoke | trigger | negative | output | release`.
- Migration of the 118 existing cases (EVL-04 corrected): a converter (`evals_to_cases.py`) moves
  only the skeleton (`name` → case dir, `prompt` → body, `expected_output` → `expected_outcome`,
  never scored — EVL-05); **every grader is hand-authored after one real run** (all 118 have empty
  `assertions` — EVL-29, SKL-48). Cases that expect cross-plugin routing become "this skill must
  not fire" checks (`tool_used: Skill`, `min: 0, max: 0, arm: both` — EVL-15) because runs load only
  the plugin under test (EVL-19/20). Cases depending on world states (PubMed down, a reversal RCT)
  become MCP mocks.
- Grader design per case: one result grader + one process grader (EVL-10). Long outputs graded by
  regex over the written file, llm judges only for short outputs with PASS/FAIL rubrics (EVL-11);
  script outcomes via "run the checker, write the result, regex it" (EVL-09).
- Per-family specifics:
  - **alignment**: eval runs have no AskUserQuestion (allowlist — EVL-22), so cases test the
    fallback contract (single `Assumed:` line, no prose questions, destructive halts); the picker
    path is covered by skill-creator runs in a real session (5.4). `history_file` for
    misread-capture's post-delivery complaints (EVL-23).
  - **evidence**: `evals/mocks/pubmed/{search_articles,get_article_metadata,…}.md` and
    `mocks/clinical-trials/*.md` with fixed PMIDs/NCTs, `expect:` guards asserting `datetype`,
    pagination and date windows, `.replay/` committed for repeatable CI (EVL-24); graders:
    `sources_lint.py` result regex, verdict marker regex, `mock_calls` for the adversarial query.
    Bundling the servers in `evidence/.mcp.json` is what makes mocks possible (mock dir is keyed by
    the plugin's server name).
  - **visual-explainers**: `file_exists` on `*.html` + `check_html.mjs` result regex (self-contained,
    doctype, reduced-motion, layout, light-lock) (EVL-13); design quality by human review with
    skill-creator's static viewer (EVL-34).
  - **vault-keeper**: `scaffold_script` builds a writable fixture vault (EVL-23); `tool_order`
    asserts verify-before-delete for empty-vault; weights make the safety graders dominate (EVL-18).
- Cost discipline (EVL-27): `smoke` = free graders, `--runs 1 --ablation none`, ≤ 10 cases per
  plugin, run on every change to that plugin. `release` = all cases, 3 runs, two arms, `--threshold
  0.8`, pinned `--model` and `--judge-model`, `--no-publish`, `--max-cost-usd` (EVL-25). Δ is the
  release signal: a skill whose output cases show Δ ≈ 0 across a release run is a cut/shrink
  candidate (EVL-14, EVL-48).

### 5.3 Minimums per plugin skill

≥ 3 output cases (SKL-43, EVL-44), ≥ 2 trigger positives with the namespaced `input_match`
`'"skill"\s*:\s*"(?:[\w-]+:)?<skill>"'` (EVL-16 corrected), ≥ 2 near-miss negatives drawn from the
sibling's territory (EVL-36, COM-32), ≥ 1 pressure scenario for gate skills (COM-28 corrected).
Trigger prompts are substantive and multi-step (EVL-37).

### 5.4 Layer 3 — trigger competition in the real environment: skill-creator

Isolated plugin evals prove a description *can* win; they cannot see the other ~45 skills in the
owner's listing (EVL-19, EVL-39). For each contested set, a 20-query set (8–10 positive, 8–10
near-miss, 60/40 split, 3 runs, 0.5 threshold — SKL-14 corrected, EVL-38) run with
`anthropic-skills:skill-creator`'s description loop in a real cloud session with everything loaded:
- {intent-lock, decision-interview, plan-critique, misread-capture}
- {pubmed-research-note, comprehensive-review, literature-watch, anthropic-skills:psych-paper-digest,
  anthropic-skills:deep-research}
- {concept-animation, ml-concept-lab, clinical-infographic, code-explainer, dataviz}
- learn-hub {pdf-pipeline, ingest-article, atomize-book, anthropic-skills:pdf,
  anthropic-skills:bullet-reconstruct, anthropic-skills:obsidian-knowledge-vault}
- learn-hub {split-note, atomize-book, digest-report}; {vault-audit modes vs sync-vault}

### 5.5 Project skills (learn-hub + plugin-workbench)

`claude plugin eval` officially targets plugins and `@skills-dir` plugins only (EVL-46 corrected;
the bare-folder behaviour is undocumented), and project-scope `@skills-dir` plugins load only from
the primary working directory (docs plugins-reference:413) — which is `/home/user` in multi-repo
cloud sessions. So project skills use the documented alternative: skill-creator `evals/evals.json`
next to each skill with a pinned field name `expectations` (SKL-47, EVL-28) and non-empty
expectations enforced by check.py; deterministic cores keep their unit tests.

### 5.6 Method for the rewrite itself

Baseline = the current skill snapshot, not "no skill" (EVL-30); report-quality skills accepted by
blind A/B with skill-creator's comparator (EVL-35); verification never in the authoring session
(SKL-44, EVL-43); read transcripts, not just scores (COM-49); for every "never/always" rule, a
no-guidance control first — rules the control already obeys are deleted (COM-29).

---

## 6. Versioning and release

- **Version lives in `plugin.json` only**; marketplace entries and the catalog top level carry no
  version (PLG-06: "Avoid setting version in both"; LOC-02; Anthropic's own first-party entries
  mostly omit it — PLG-55). This deletes the dual-file ceremony and the CLAUDE.md hard rule built
  on an inverted rationale (bump.py:4-8 vs LOC-03).
- **Explicit semver, not commit-SHA**: strict validation warns on a missing version and exits 1
  (PLG missed-practice), and version ranges on `dependencies` resolve against release tags (PLG-39).
  In-place loads (local marketplace, `CLAUDE_CODE_PLUGIN_DIRS`) ignore versions anyway (PLG-09), so
  the version only has to be right at release time. (OD-9 if the owner prefers SHA.)
- **Release = `release.py <plugin> <level>`**: write plugin.json (preserving UTF-8 + trailing
  newline), prepend CHANGELOG entry (check.py fails if CHANGELOG top ≠ version — fixes the stale
  CHANGELOGs of vault-keeper, pubmed-research-note, psych-paper-digest, clinical-infographic,
  intent-lock), run check.py + the plugin's `smoke` evals, then `claude plugin tag <plugin>
  --dry-run` and `--push` on confirmation (PLG-40: tag refuses a dirty tree and version mismatch).
- Semver meaning: major = skill renamed/removed or contract (lock record, report format, sink
  payload) changed incompatibly; minor = new skill/mode/trigger; patch = wording/fix.
- **Renames**: append-only `renames` for every retired plugin name (PLG-44): `pubmed-research-note,
  comprehensive-review, psych-paper-digest → evidence`; `intent-lock, decision-interview,
  plan-critique → alignment`; `clinical-infographic, concept-animation, ml-concept-lab,
  code-explainer → visual-explainers`; `plugin-creator, firecrawl → null`.
- learn-hub project skills are unversioned (git SHA is the version; the repo CHANGELOG records
  changes as today). Cross-repo contract copies carry the canonical file's sha.
- Synced release channel (if OD-1 adopts it): the tagged release is what is uploaded/enabled on
  claude.ai; dev sessions shadow it via `CLAUDE_CODE_PLUGIN_DIRS`.

---

## 7. Context-budget targets

Measured baseline (this session; lenient frontmatter regex, chars):

| Surface | Now | Target |
|---|---|---|
| micky listing (17 skill descriptions + 12 command descriptions) | 16,215 + 1,405 = 17,620 chars (~4.4k tok) | 14 plugin skills + 1 project skill, 0 commands: ≤ 9,000 chars (~2.3k tok) |
| learn-hub listing (11 project skills; +16 plugin entries if they ever loaded) | 8,811 chars loaded (+7,826 not loaded) | 10 project skills ≤ 6,000 chars |
| Per-skill description | 8 micky skills at 1,003–1,022; 3 learn-hub over 1,024 (SKL-52 corrected) | ≤ 500 typical, ≤ 1,024 hard; description + `when_to_use` ≤ 800 typical, ≤ 1,536 hard |
| micky always-on (`claude plugin details`, sum) | ~6.6k tok (LOC-19) | ≤ 2.5k tok (≤ 700 per family plugin) |
| Largest SKILL.md bodies | atomize-book 21.3k tok / 1,256 lines; ingest-article 6.7k; intent-lock 6.2k; pubmed 4.7k; firecrawl 4.2k | every body ≤ 5k tok / 500 lines hard; target ≤ 3k tok / 300 lines; atomize-book ≤ 4.5k; intent-lock ≤ 2.5k |
| Mandatory on-invoke load (body + unconditional refs) | ingest-article ~18.7k; ML ~10.8k; pubmed ~10.6k | ≤ 6k tok per skill; all other refs conditional |
| First 5k tokens of each SKILL.md | standing rules scattered | all standing rules + gotchas inside the first 5k (SKL-40) |
| micky CLAUDE.md + mandated reads | ~3.5k + MEMORY ~27k + ROUTING ~5k | ≤ 60 lines (~0.8k tok), nothing mandated |
| learn-hub CLAUDE.md | 3,126 lines / ~67k tok every session | ≤ 200 lines (~3k tok); rest path-scoped or on-demand |
| Reference files | several > 300 lines without TOC (figures-and-loss 503 lines) | none > 400 lines; TOC above 100 lines |
| Listing entries in a full cloud session | 11 loaded (of 55 authored) + ~21 account skills | 25 authored, 25 loaded |

Measurement: `claude --plugin-dir <p> plugin details <name>` per plugin (PLG-52), `/doctor` for the
listing estimate and `/skill-doctor` for cost and never-invoked skills after two weeks of use
(SKL-08, EVL-40); check.py reports chars/tokens per skill. The 1%-of-context listing budget
(SKL-08) is recorded as a measured number in Wave 0, not assumed.

---

## 8. Migration waves

Each wave ends with check.py green and a commit; old plugins stay installable until their wave
exits (renames make the switch automatic). Tag `pre-rewrite` on both repos in Wave 0 as the eval
baseline and rollback point.

### Wave 0 — Baseline and verification (no behaviour change)
- **Entry**: owner answers OD-1…OD-9 (or accepts recommendations).
- **Work**: tag snapshots; record baselines (plugin details, `/doctor`, `/skill-doctor` locally,
  listing chars); verify every mechanism this design relies on but the research left open:
  (a) `CLAUDE_CODE_PLUGIN_DIRS` pointing at a folder of plugins loads all five in a multi-repo cloud
  session; (b) `renames` with several old names mapping to one new name validates; (c) plugin
  `dependencies` resolve when both plugins come from the same folder load; (d) `claude plugin eval`
  is available on the account (SKL open question: "early access") and mocks work for an `http`
  server; (e) learn-hub `.claude/skills` load eagerly in multi-repo sessions (docs skills.md:142
  says nested dirs may load lazily); (f) personal claude.ai plugin upload/marketplace mechanics (only
  needed if OD-1 = synced); (g) `/doctor` listing budget with everything loaded.
  First check.py (strict validate per dir + YAML parse) runs against the current tree.
- **Exit**: baseline table filled; each of (a)–(g) answered yes/no with evidence; a fallback chosen
  for any "no" (e.g. (a) no → list five absolute paths).

### Wave 1 — Stop the bleeding (live data-corrupting defects only, on the current layout)
- **Entry**: Wave 0 exit.
- **Work**: set cloud env vars + setup script (§2.5); retire `source-to-vault` from learn-hub's
  catalog; make comprehensive-review fork's digest opt-in; fix empty-vault's learn-hub marker and
  stop it deleting assets (hand to ingest-infographic/animation); backport learn-hub's layout rule
  into micky concept-animation + ml-concept-lab grammar and examples; remove the infographic dark
  block and stack the `.mech` strip; guard ingest-article inbox deletion behind explicit invocation
  and gitignore the folder; quote the 5 invalid-YAML descriptions (SKL-51); move the misread ledger
  write out of `${CLAUDE_PLUGIN_ROOT}` to `state/misreads.md`.
- **Exit**: no inventory defect of severity "high" that can corrupt data, delete files or write to
  the live DB remains; check.py strict-YAML clean.

### Wave 2 — Platform skeleton (move, don't rewrite)
- **Entry**: Wave 1 exit.
- **Work**: create `alignment`, `evidence`, `visual-explainers` by moving skills and references
  unchanged; add plugin-level shared files (first drafts); single `.mcp.json` in evidence; delete
  all 12 commands, adding `argument-hint`/`disable-model-invocation` to the target skills; new
  marketplace.json (entries `{name,source,category}`, `renames`, `$schema`, no versions); build
  `plugin-workbench` (check.py full rule set, release.py, evals_to_cases.py); delete route.py,
  ROUTING.md, bump.py, validate.py; rewrite micky CLAUDE.md/MEMORY.md/README; convert all 118 eval
  skeletons; resolver scripts + `vault/.vault-id`.
- **Exit**: `claude plugin validate --strict` passes for the marketplace and all 5 plugin dirs;
  check.py green except rules deferred to Wave 3 (body size, description budget, eval minimums —
  reported as warnings); in a cloud session all 14 plugin skills + plugin-workbench appear, every
  former slash name still resolves as a bare skill name or is listed in the migration note.

### Wave 3 — Rewrite the micky skills, eval-driven (per family: alignment → evidence → vault-keeper → visual-explainers)
- **Entry**: Wave 2 exit; family's eval skeleton in place.
- **Work per skill**: run the snapshot baseline; author graders after the first real run; rewrite to
  the house shape and rubric; move policing prose into scripts with tests; description loop (5.4)
  for contested sets; blind A/B for pubmed-research-note, comprehensive-review, literature-watch;
  release via release.py.
- **Exit per family**: every skill within §7 hard budgets; smoke suite 1.0 and release suite ≥ 0.8
  with Δ > 0 on the majority of output cases; skill-creator trigger sets ≥ 0.8 held-out accuracy;
  every inventory defect listed for that unit closed or explicitly waived in MEMORY.md; CHANGELOG +
  tag written.
- alignment exits first because evidence and visual-explainers depend on the lock record.

### Wave 4 — learn-hub consolidation (4a can run in parallel with Wave 3; 4b waits for evidence + vault-keeper exit)
- **4a (learn-hub internal)**: move Python tools to `tools/source/` with npm aliases and `test:py`;
  split atomize-book (references + `.claude/agents/`); merge ingest-slides → ingest-article, the two
  ingest-* filers → file-visualization; rewrite pdf-pipeline (+ classifier), sync-vault (single
  owner; gates inside apply-sync), verify (bundled scripts), vault-audit (three modes); convert
  split-note, pk-animation, digest-report to project skills; CLAUDE.md split with the gotcha mapping
  table; `.claude/rules/`; readiness probe; skill-creator evals per project skill.
- **4b (cross-repo)**: delete the three forks and the `learn-hub-local` marketplace once
  `vault-keeper` sink=`learn-hub` and the report-format contract + parity checks exist; retire the
  learn-hub concept-animation copy after its layout fixes are in visual-explainers; pk-animation
  uses `evidence:pubmed-research-note`.
- **Exit**: learn-hub has no `plugins/` or `.claude-plugin/`; learn-hub CLAUDE.md ≤ 200 lines and
  every one of the 136 gotcha headings has a recorded destination; learn-hub listing ≤ 6,000 chars;
  the pdf/ingest trigger set and the atomize collision set pass; parity checks green in a
  multi-repo session; one end-to-end run (report → research-notes → digest-report → sync → verify)
  recorded.

### Wave 5 — Release channel and telemetry
- **Entry**: Waves 3 and 4 exit.
- **Work**: if OD-1 includes the synced channel, publish tagged releases to claude.ai and confirm a
  routine sees them; after two weeks, `/skill-doctor` usage review → retire never-invoked skills
  (COM-47, EVL-40); re-run release suites on the next default-model change (EVL-48).
- **Exit**: usage report filed in MEMORY.md; any skill with zero invocations and Δ ≈ 0 either
  retired or given a recorded reason to stay.

---

## 9. Owner decisions

Only questions that turn on the owner's values or environment.

**OD-1 — Cloud delivery for sessions that do not clone micky-psych-tools.**
Options: (a) `CLAUDE_CODE_PLUGIN_DIRS` only — plugins exist only in sessions that clone micky;
(b) (a) plus a claude.ai-synced release channel for routines/Cowork/single-repo sessions;
(c) synced only.
Recommendation: (a) now, (b) only if the owner runs routines or learn-hub-only sessions that need
the evidence/visual skills. Trade-off: (b) is the documented cloud route (PLG-47 corrected) and
reaches every surface, but adds an upload/enable step per release and its personal-account
mechanics are unverified; (a) is zero-ceremony and always HEAD, but a session without the micky
clone silently has no plugins.

**OD-2 — Where finished work lands by default.**
Options: (a) learn-hub `research-notes/` (and visual assets filed into learn-hub) whenever learn-hub
is reachable, micky vault only as fallback; (b) always the micky vault, drained later by
empty-vault; (c) retire the micky vault entirely.
Recommendation: (a) via `output_sink: auto`. Trade-off: (a) removes a hop and the two-route
ambiguity the forks created, but the micky vault stops being the single place "every skill's output
lands" (MEMORY) and sessions without learn-hub write to a different place; (b) keeps one place but
keeps empty-vault as a mandatory second step; (c) is simplest but loses the offline/portable sink.

**OD-3 — Should a finished review/report be digested into the live Supabase DB automatically?**
Options: (a) only on an explicit "digest"/"atomize"; (b) by default unless "don't digest".
Recommendation: (a). Trade-off: (b) saves a command per report but writes to a shared production
project every run (fork SKILL.md:166-176, "high"); (a) costs one word.

**OD-4 — Misread ledger: keep the compounding ledger, and where.**
Options: (a) git-tracked `micky/state/misreads.md` (env var in cloud, userConfig locally);
(b) machine-local `${CLAUDE_PLUGIN_DATA}` (lost in every cloud session); (c) retire misread-capture.
Recommendation: (a). Trade-off: (a) makes priors compound across Windows and cloud but puts personal
diagnostic notes in the (private) repo history and needs a commit after each capture; (b) is
invisible to cloud sessions; (c) removes a skill whose ledger has changed once in git since
2026-07-11 despite many runs (inventory-alignment "high").

**OD-5 — The two "psych-paper-digest" skills.**
Options: (a) rename the plugin skill to `literature-watch` and keep both; (b) keep the watchlist
skill, disable the account skill; (c) keep the account skill, retire the watchlist skill.
Recommendation: (a), then decide (b)/(c) from `/skill-doctor` usage in Wave 5. Trade-off: (a) keeps
both habits but leaves two digest skills competing in the listing; (b)/(c) lose one workflow
(daily 8–12-paper roundup vs watchlist triage with Act/Read).

**OD-6 — Firecrawl as a marketplace plugin.**
Options: (a) retire; use the vendor's own skills/CLI for general web work and keep only the
fetch contract in evidence; (b) keep a slim routing skill (≤ 1k tokens) with the vendor guide as a
dated, fetched-on-demand reference.
Recommendation: (a). Trade-off: (a) ends the staleness problem permanently but general-web requests
in cloud depend on the vendor's distribution reaching that environment; (b) keeps one entry point
the owner controls at the cost of re-syncing vendor text.

**OD-7 — gridgeist.**
Options: (a) keep vendored with a pinned `UPSTREAM.md`; (b) drop from the marketplace.
Recommendation: (a) until the Wave 5 usage review, then (b) if never invoked. Trade-off: listing
budget and maintenance vs a design capability no family covers.

**OD-8 — Slash names after commands are retired.**
Options: (a) capability names (`/concept-animation`, `/literature-watch`, `/decision-interview`);
(b) rename skills to the short verbs (`/animate`, `/digest`, `/resolve-decisions`) so muscle memory
survives.
Recommendation: (a). Trade-off: (a) keeps names aligned with what the skill does (SKL-54) and with
eval grader regexes; (b) preserves typing habits but produces less descriptive skill names in the
listing.

**OD-9 — Versioning style.**
Options: (a) explicit semver in `plugin.json` + tags; (b) commit-SHA (no version anywhere).
Recommendation: (a). Trade-off: (a) keeps `--strict` validation clean and allows dependency ranges,
at the price of a `release.py` step; (b) has zero ceremony and is the docs' suggestion for
internal plugins under active development (PLG-08) but fails `--strict` (PLG missed-practice).

---

## 10. Risks

1. **`CLAUDE_CODE_PLUGIN_DIRS` is new and framed for testing** (v2.1.280). A path change in cloud
   clone layout makes every plugin vanish without error. Mitigation: Wave 0 (a); readiness line in
   plugin-workbench's check; OD-1(b) as the documented fallback.
2. **Consolidation shifts triggering.** Four renderers or four gates in one plugin still compete by
   description; cutting descriptions ~50% can under-trigger (SKL-11). Mitigation: trigger evals gate
   every description (5.3, 5.4); descriptions are not shortened below what the held-out set needs.
3. **`renames` and dependency behaviour are partially unverified** (multi-to-one renames; deps under
   folder loads and synced plugins). A declared dependency that is missing disables the dependent
   plugin. Mitigation: Wave 0 (b)(c); only two hard dependencies declared.
4. **`claude plugin eval` availability and cost** (early-access troubleshooting entries; ~700 agent
   runs if all cases run two-armed). Mitigation: smoke vs release tiers, `--max-cost-usd`,
   skill-creator as the fallback runner.
5. **Loss of hard-won knowledge** when 3,126 lines of learn-hub CLAUDE.md and 1,256 lines of
   atomize-book are redistributed — the repo's own lesson is that a worklist built from one pattern
   inherits its blind spots. Mitigation: the per-heading mapping table as an exit artefact; the old
   file kept as `docs/gotchas-archive.md`.
6. **Cross-repo parity only runs when both clones are present.** A Windows session in one repo can
   still drift. Mitigation: provenance sha checked by check.py/vitest even without the sibling
   (header vs a recorded canonical sha list updated at release).
7. **Windows specifics**: CRLF frontmatter, backslash paths, PowerShell vs bash snippets in skills.
   Mitigation: check.py rules 1 and 6; scripts in Python/Node, not shell arrays.
8. **Muscle memory and habits** (12 commands disappear, skills renamed). Mitigation: bare skill names
   still work (PLG-17); OD-8; a one-page migration note in README.
9. **Big restructure while learn-hub churns** (atomize-book 6 commits through 2026-09-20 — LOC-46).
   Mitigation: Wave 4a scheduled per skill, not as one branch; micky rewrites (stable since
   2026-08-08) go first.
10. **Merging vault-vectors/check-repetition/vault-coverage into `vault-audit`** may be too broad to
    trigger precisely (SKL-56). Mitigation: keep them as three project skills if the trigger set
    for the merged skill scores below the separate baseline.
11. **Secrets and personal data**: ledger in git (OD-4), `.env` writes (firecrawl), copyrighted
    inbox PDFs. Mitigation: env credentials, gitignored inboxes, check.py path rules.
12. **Eval green ≠ correct clinical content**: graders check structure; clinical fidelity still
    needs the owner's review and blind A/B (5.6). Scores are advisory when real MCP servers run
    (EVL missed-practice).

---

## Appendix A — mechanisms verified against the docs in this session (beyond the research files)

- `CLAUDE_CODE_PLUGIN_DIRS`: "Separate multiple paths with `:` on Unix or `;` on Windows. Give each
  path as an absolute path or start it with `~`" (env-vars.md:334); "Project and local settings
  can't set this variable" (plugins.md:317). Folder-of-plugins support follows from "each loaded the
  way a `--plugin-dir` flag loads it" + plugins.md folder rules (v2.1.265+) — verified by reading
  only; to be exercised in Wave 0.
- Multi-repo cloud sessions: project `.claude/settings.json` hooks and `.mcp.json` are not read;
  "Install dependencies for those sessions with a setup script instead" (cloud-environments.md:261,
  :468); setup scripts provision the VM and are cached (Setup scripts section).
- Plugins vs standalone: standalone `.claude/` "Best for … project-specific customizations"
  (plugins.md:13-24).
- CLAUDE.md sizing and path-scoped rules: "target under 200 lines" (memory.md:82); multi-step or
  area-specific entries belong in a skill or `.claude/rules/` with `paths:` (memory.md:51,
  :154-212); `.claude/rules/` carries into cloud sessions (cloud-environments carry-over table).
- Synced plugins: load in Cowork, cloud and signed-in terminal sessions; a same-named plugin from
  any other source wins over the synced copy (plugins-reference "Plugins synced from claude.ai");
  personal claude.ai uploads exist as a claude.ai marketplace (discover-plugins.md:296) — upload
  mechanics not verified.
- `${CLAUDE_PLUGIN_DATA}` intended for "installed dependencies … generated code, and caches"
  (plugins-reference.md:762) — hence not used for durable user state.
- `userConfig`: `default`, `options`, `/config` rows, non-sensitive substitution into skill content
  (plugins-reference.md:589-630).
- Dependencies with `--plugin-dir`: a missing dependency is reported as not installed
  (plugin-dependencies.md:106-121).
- `--add-dir` loads that directory's `.claude/skills/` (skills.md:153); nested `.claude/skills`
  below the start directory may load lazily (skills.md:142).
- `skillOverrides` values `on | name-only | user-invocable-only | off` (settings-reference) —
  available as a listing-budget lever for account skills the owner rarely uses.
