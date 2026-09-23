# Target architecture: plugin and skill rewrite (micky-psych-tools + learn-hub)

**Date:** 2026-09-23. **CLI:** Claude Code 2.1.280.

**Basis.** Phase-1 evidence in `wf1/`:
- Research claims `SKL/PLG/EVL/COM/LOC-nn`. Where the verdict was `partially`, the `corrected_claim` wording is used. LOC-26 is refuted and not used.
- Verifier missed practices `MP-PLG-n`.
- 313 inventory defects, cited as `INV <unit>-<n>`. The 49 HIGH defects are numbered H01–H49 (Appendix A).
- The rubric (`wf2/rubric.md`, rules R1–R92).

**How this was synthesized.**
- The judges split:
  - J1 scored risk-first 46, workflow-first 45, purist 44, and picked risk-first.
  - J2 scored workflow-first 46, purist 45, risk-first 41, and picked workflow-first.
  - Combined scores: workflow-first 91, purist 89, risk-first 87.
- Both graft lists pull in the same direction.
  - J1's grafts move risk-first toward workflow-first/purist on the **end state**: mechanical sync safety, state out of the plugin tree, plugin.json-only versions, family merges, and the CLAUDE.md diet.
  - J2's grafts import risk-first's **migration discipline** into workflow-first: harm-first waves, per-plugin enablement, ratchet, trigger-lock, the H-coverage map, consumers-first ordering, and aliases.
- This document therefore takes **workflow-first's topology** (delivery as a property of the checkout, family plugins, a file-drop inbox, hooks travelling in a plugin). It reaches that topology through **risk-first's waves and safety net**, and absorbs both graft lists.
- Every factual error the judges found was re-checked against the source and fixed (Appendix B).

**Probe labels.**
- `P1`–`P8`: probes run for this synthesis.
- `V1`–`V4`: workflow-first's probes.
- `RF-A1`–`RF-A6`: risk-first Appendix A.
- `J`: judge probes.
- All are listed in Appendix C.

---

## 1. Thesis

1. Most of the 49 HIGH defects are broken **seams**: contracts between units, delivery, and state paths. On the owner's main surface, the multi-repo cloud session, nothing from either marketplace loads (LOC-42), while the units that do load carry the destructive defects (H25, H34, H35, H11).
2. Delivery becomes a **property of the checkout**. Both repos' `plugins/` load in place from absolute paths through `CLAUDE_CODE_PLUGIN_DIRS` (MP-PLG-8, P1). learn-hub's session setup travels in a hooks-only plugin, which fires from `/home/user` (P2). The sync's safety gates move **inside the sync script**, so no layout can skip them.
3. Each capability has **one home**.
   - micky holds the reusable families `alignment`, `evidence` and `visuals`, plus `vault-keeper` (the output sink), `firecrawl`, `gridgeist` and a self-contained `plugin-creator`.
   - learn-hub holds repo-bound **project skills**.
   - The forks, `source-to-vault`, the learn-hub catalog, ROUTING.md and all 12 commands go.
4. The cross-repo handoff is a **file drop** into learn-hub's git-tracked `research-notes/` inbox. Each interface has one owner, the consumer is a tolerant reader, publishing to live Supabase is always opt-in, and compounding state (ledger, `last_swept`) lives in git.
5. The order is **risk-first**:
   1. W0: safety net.
   2. W1: stop active harm in the units that already load.
   3. W2: reconnect the pipeline.
   4. W3 and W4: consolidate.
   - A plugin reaches the cloud only after it is fixed.
   - Always-paid context falls from about 108k tokens to about 16k.

---

## 2. Target topology and delivery

### 2.1 Placement rules (everything below follows from these)

| # | Rule | Source |
|---|---|---|
| T1 | A capability usable outside one specific repo ships in a **micky plugin**. | plugins.md "plugins vs standalone"; PLG-22 |
| T2 | A procedure that reads or writes one repo's scripts, DB or layout is a **project skill in that repo** (`.claude/skills/`). | PLG-47 corrected (`.claude/skills` carry over into cloud sessions); observed in this session |
| T3 | Skills that share a contract, script or MCP server live in **one plugin**. Shared files sit at the plugin root and are linked one level deep with "Before step N, read X". No symlinks, no `../`. | PLG-22, PLG-23, SKL-16, SKL-18, COM-38 |
| T4 | Across plugins and across repos, a skill is reached **by name**, marked OPTIONAL, with an inline fallback. There are **no `dependencies` entries**: an unsatisfied dependency disables the dependent plugin (V4, RF-A2), and delivery grows plugin by plugin. | COM-36, COM-37, V4 |
| T5 | A plugin exists in learn-hub only if it must **fire hooks in multi-repo sessions**, where project hooks never load (PLG-47 corrected, RF-A3). | P2 |
| T6 | State that must compound across ephemeral cloud VMs lives in **git** (micky `state/`), never in `${CLAUDE_PLUGIN_ROOT}` (PLG-24, PLG-57). It lives in `${CLAUDE_PLUGIN_DATA}` only for caches. | PLG-24, OD6 |

### 2.2 micky-psych-tools (target tree)

```
.claude-plugin/marketplace.json  $schema, name, owner, description; entries {name, source, category, keywords};
                                 no versions; append-only renames{} (OD3)
plugins/
  alignment/        skills: intent-lock, misread-capture, decision-interview, plan-critique
                    alias skills (dmi, OD9): critique-plan, resolve-decisions
                    references/interview-protocol.md  (threshold, destructive always-ask, AskUserQuestion mechanics,
                                                       one silence rule, autonomous fallback, stop sovereignty)
                    references/lock-record.md         (callee contract: slots intent-lock returns; the one-line
                                                       "Assumed: … — say if wrong." hand-back)
                    scripts/ledger.py (+tests)        (append/list/retire; grammar, ordering, cap)
  evidence/         skills: pubmed-research-note, comprehensive-review, lit-watch (was psych-paper-digest, OD7)
                    alias skill (dmi): digest
                    .mcp.json    ← the ONLY PubMed + ClinicalTrials.gov declaration in both repos (today: 6 copies, P4)
                    references/report-contract.md  (Sources grammar with ONE NCT form, Assumed line, depth contract,
                                                    engine-failure policy, report frontmatter incl. contract: report/1)
                    references/engines.md          (runtime tool resolution, E-utilities edat+retstart, CT.gov AREA RANGE,
                                                    firecrawl fetch-only)
                    scripts/sweep.py  sources_lint.py (+tests);  evals/mocks/{pubmed,clinical-trials}/*.md
  visuals/          skills: clinical-infographic, concept-animation, ml-concept-lab, code-explainer
                    alias skills (dmi): infographic, animate, visualize, explain-code
                    references/html-artifact-contract.md  render-verify.md
                    scripts/check-html.mjs (+tests)  ← FALLBACK port of learn-hub's audits (§4.3)
  vault-keeper/     skills: vault-keeper (output-sink owner), empty-vault (dmi)
                    references/vault-layout.md; scripts/sink.py vault_index.py drain_plan.py (+tests)
  firecrawl/        skill: firecrawl (slim router) + references/vendor-onboarding-<fetch-date>.md (OD12); defaultEnabled:false
  gridgeist/        vendored verbatim + UPSTREAM.md (repo, sha, date)
  plugin-creator/   skills: plugin-creator (+ alias new-plugin, dmi), refine-plugin (dmi)
                    scripts/validate.py release.py (+tests); references/ (house rubric, templates — valid YAML)
                    hooks/hooks.json: SessionStart (remote only) → set core.hooksPath=.githooks on $MICKY_TOOLS_DIR
                    when the marker matches and no value is set (same rule learn-hub's hook follows)
state/              misreads.md; lit-watch/{config.json, last_swept.json, digests/}      (git-tracked, OD6)
vault/              .vault-id ("micky-psych-vault") + content (kept as fallback sink, OD4)
scripts/health.sh  scripts/eval.sh            (thin repo wrappers; §6, §8)
.githooks/pre-commit                          (runs health.sh --fast)
docs/rewrite/       ratchet.json triggers.lock.json delivery-log.md baseline.md h-coverage.md
CLAUDE.md ≤5 KB · MEMORY.md living section ≤6 KB (not mandated) · docs/history.md · README.md
```

Removed:
- the 14 old plugin directories (their content moves into the families);
- all 12 `commands/` files;
- `scripts/{validate,route,bump}.py` (validate and bump move into plugin-creator; route is deleted);
- `ROUTING.md`;
- every `evals/evals.json`, after conversion (R70).

### 2.3 learn-hub (target tree)

```
.claude-plugin/                 DELETED (learn-hub-local catalog; never registered — H14)
plugins/learn-hub-session/      hooks-only plugin (T5)
  .claude-plugin/plugin.json    hooks/hooks.json: SessionStart → hooks/run.sh
  hooks/run.sh                  root = $LEARN_HUB_DIR → else ${CLAUDE_PLUGIN_ROOT}/../.. ; require marker
                                (package.json "name":"learn-hub" + scripts/apply-sync.mjs) else exit 0 with a message;
                                exec .claude/hooks/session-start.sh with LEARN_HUB_DIR exported
.claude/settings.json           SessionStart kept (single-repo sessions); PreToolUse gates REMOVED (moved into the sync)
.claude/hooks/session-start.sh  root from LEARN_HUB_DIR → marker-checked CLAUDE_PROJECT_DIR → own path;
                                idempotent via a done-marker, so a double registration costs nothing
.claude/skills/
  model-invocable: pdf-pipeline, ingest-article, ingest-slides, atomize-book, digest-report, ingest-visual,
                   sync-vault (sole owner of the sync/revalidate/verify tail), verify
  user-only (dmi, OD10): vault-atomizer, vault-vectors, vault-coverage, check-repetition, pk-plasma-animation
.claude/rules/*.md              path-scoped app gotchas (OD11-b; fallback docs/gotchas/*.md if W0 check (e) fails)
research-notes/                 INBOX (git-tracked): <slug>.md reports; visuals/<slug>.html + <slug>.meta.json;
                                .intake-log.jsonl (append-only handshake, §5)
Raw Article PDF/                ingest-article drop folder (ARTICLE_INBOX_DIR default); gitignored
evals/<skill>/<case>/           project-skill eval cases; scripts/eval-project-skill.sh (throwaway-plugin wrapper, §6)
scripts/ready.mjs               readiness report (node_modules, .env.local, Chromium, PyMuPDF, poppler) + fix text
scripts/lib/sync-preflight.mjs  pure preflight (readiness refusal, fetch-staleness warning, dup + repetition gates)
npm scripts                     sync:preflight · audit:visual · test:py · check:skills (skill-lint + validate --strict)
docs/vault-format.md            note/topic/sidecar format (moved from CLAUDE.md; linked by every pipeline skill)
docs/gotchas-archive.md         verbatim old CLAUDE.md text (not loaded)
CLAUDE.md ≤32 KB (OD11-b)
```

### 2.4 Ownership map (one owner per job and per contract)

| Job or contract | Owner | Consumers (reach it by…) |
|---|---|---|
| Pre-build alignment; mid-task decisions; plan critique; misread capture; lock record | `alignment` | evidence and visuals skills, firecrawl Path C, pk-plasma-animation, all by skill name, OPTIONAL with the fallback sentence (§4.2) |
| Decision report; whole-topic review; watchlist sweep; report format; PubMed/CT.gov MCP | `evidence` | digest-report (tolerant reader, §5); pk-plasma-animation (brief → `pubmed-research-note` by name); claude.ai `daily-random-review` (OD8) |
| Clinical sheet; watch-only animation; explorable; code explainer; HTML artifact contract | `visuals` | ingest-visual (inbox); producers of source reports |
| Where finished outputs land (sink); micky vault; micky → learn-hub transfer | `vault-keeper` | every micky producer, "file via `vault-keeper`", OPTIONAL with fallback |
| General-web fetch engine | `firecrawl` | evidence (fetch-only contract restated in `engines.md`) |
| Marketplace validation, release, scaffolding | `plugin-creator` | both repos' health checks |
| Inbox layout + intake handshake | learn-hub `digest-report` (`references/inbox-contract.md`) | vault-keeper's sink, empty-vault, ingest-visual |
| Visual layout and self-containment (executable truth) | learn-hub audits (`scripts/lib/animation-responsive.mjs`, `infographic-responsive.mjs`, `src/lib/animation-layout.ts`) behind `npm run audit:visual` | ingest-visual (always); visuals producers (via `$LEARN_HUB_DIR`; `check-html.mjs` is the fallback) |
| Sync / revalidate / verify / purge tail | learn-hub `sync-vault` + `apply-sync.mjs` preflight | all 7 learn-hub writers link to it and never restate it (8 restatements today, 4 contradictory apply rules) |
| Book / article / slide authoring; figure, loss, depth and QC tooling | learn-hub `atomize-book` (scripts stay in place), `ingest-article`, `ingest-slides`, `pdf-pipeline` (front door) | `npm run book:*` aliases and `npm run test:py` |
| Session setup in multi-repo cloud | `learn-hub-session` plugin (+ cloud setup script) | none |

### 2.5 Delivery route per environment

| Environment | micky plugins | learn-hub skills | Hooks and setup | Mechanism and source |
|---|---|---|---|---|
| **Cloud, multi-repo** (starts at `/home/user`; the owner's main surface) | `CLAUDE_CODE_PLUGIN_DIRS` set **on the cloud environment**. Final value: `/home/user/micky-psych-tools/plugins:/home/user/learn-hub/plugins`. During migration, per-plugin absolute paths (§2.7). Loads as `<name>@inline`, in place, from the checked-out branch. | `.claude/skills/*` load from the clone (observed) | `learn-hub-session` SessionStart hook: npm install, `.env.local`, core.hooksPath, `PUPPETEER_EXECUTABLE_PATH` via `CLAUDE_ENV_FILE`. The cloud **setup script** installs VM tooling. The sync's own preflight enforces the gates. | MP-PLG-8 (env var; project settings can't set it); RF-A1 and V1 (folder of plugins loads in place); **P1: paths must be absolute**, because `HOME=/root` makes `~/micky-psych-tools/plugins` report `× Path not found: /root/micky-psych-tools/plugins`. PLG-47 corrected (repo hooks and `.mcp.json` not read; `.claude/skills` load). **P2:** plugin SessionStart and PreToolUse hooks fire from `/home/user`, with `CLAUDE_PROJECT_DIR=/home/user`. |
| **Cloud, single-repo learn-hub** | Same variable. The micky paths print `× Path not found`; the other paths still load and the exit code is 0 (P1). | `.claude/skills/*` | settings.json SessionStart **and** the plugin hook both fire; the done-marker makes the second one a no-op | PLG-47; P1 |
| **Cloud, single-repo micky** | Same variable | none | plugin-creator hook sets core.hooksPath | P1 |
| **Local Windows** (any cwd) | **OD2-a (assumed): from W3 entry**, a user environment variable `CLAUDE_CODE_PLUGIN_DIRS=<micky>\plugins;<learn-hub>\plugins` (`;` separator, absolute paths), after the marketplace copies are uninstalled. **Until W3:** the current user-scope marketplace install. MEMORY.md:11 says only "Installed … as marketplace `micky-psych-tools` (user scope)". W0 determines whether the source is a local directory (in place, PLG-09) or GitHub (cached; fixes need `release.py` + `claude plugin marketplace update`). | `.claude/skills/*` when cwd is inside learn-hub. Cross-repo work needs no learn-hub skill in a micky-cwd session, because producers only drop files into the inbox (§5). | settings.json hooks run (single repo); session-start is remote-only (V9), so a no-op locally; gates run inside the sync | MP-PLG-8 (`;` on Windows), PLG-09, LOC-39, PLG-51 (`--plugin-dir`/env copy beats a same-named installed plugin) |
| **claude.ai / Cowork / routines on sessions without the clones** | None by default (**OD13-a**). Option: a portable build of selected skills uploaded as claude.ai-synced plugins. A same-named in-place plugin wins in Code sessions (RF-A5). | n/a | n/a | PLG-47 corrected (synced plugins); SKL-04 (portable = six spec keys, no `!` injection) |
| **claude.ai-synced skills in every Code session** | 22 skills, 15,385 description chars (P3, V6). They load in Code sessions and compete in the listing. | | | SKL-55 (collision rules), SKL-08 (listing budget) |
| **`claude plugin eval` runs** | The plugin directory is the target; runs are isolated (no CLAUDE.md, no other plugins) | A throwaway plugin wraps the project skill (§6.5) | none | EVL-19, EVL-46 corrected |

**Why not claude.ai sync for micky in the cloud (OD1-b).** Synced plugins are downloaded copies, not in place. Every change would need a re-upload, which recreates the fork-drift class (LOC-33, LOC-34). It also breaks the `state/` and vault-in-git model. It stays the fallback if the W0 canary fails.

**Why not `extraKnownMarketplaces` or `@skills-dir`.** Cloud sessions do not install repo-enabled plugins, and multi-repo sessions read no settings.json (PLG-47 corrected). `@skills-dir` plugins load only from the primary working directory, which is `/home/user` here (PLG-50, RF-A4).

### 2.6 Environment variables and setup script

| Variable | Cloud environment value | Windows (user env var) | Read by |
|---|---|---|---|
| `CLAUDE_CODE_PLUGIN_DIRS` | §2.7 schedule; final `/home/user/micky-psych-tools/plugins:/home/user/learn-hub/plugins` | from W3 (OD2-a): `<micky>\plugins;<learn-hub>\plugins` | Claude Code (v2.1.280+) |
| `LEARN_HUB_DIR` | `/home/user/learn-hub` | the learn-hub checkout (W0 confirms; the ingest-article inbox path suggests `C:\Users\User\Desktop\Learn`) | vault-keeper `sink.py`, empty-vault, visuals (audit), learn-hub hooks |
| `MICKY_TOOLS_DIR` | `/home/user/micky-psych-tools` | the micky checkout | alignment `ledger.py`, lit-watch, vault-keeper, plugin-creator |
| `PUPPETEER_EXECUTABLE_PATH` / `PUPPETEER_SKIP_DOWNLOAD` | `/opt/pw-browsers/chromium` / `1` | unset | mermaid prebake, thumbs, audit:visual |
| `ARTICLE_INBOX_DIR` | unset → `<learn-hub>/Raw Article PDF/` (gitignored) | same default (keeps the owner's drop-folder habit) | ingest-article |
| `BOOK_ROOT` | unset → vault-coverage reports "Book/ absent — cannot run here" as a finding | the checkout's `Book/` | vault-coverage |
| `FIRECRAWL_API_KEY` | environment credential (existing) | existing | firecrawl; never written to `.env` (INV firecrawl-3) |

- Each value is validated against a **marker** before any write:
  - learn-hub: `package.json` `"name": "learn-hub"` plus `scripts/apply-sync.mjs`;
  - micky: `.claude-plugin/marketplace.json` `"name": "micky-psych-tools"`;
  - vault: `vault/.vault-id`.
  - If a marker is missing, the skill stops and asks. A headless run instead writes to cwd and opens its output with `Assumed: …` (R47, R53).
- **Setup script** (cloud environment; VM tooling only, since it may run before the clone, U2):
  - `pip install pymupdf pypdf pdfplumber`
  - `apt-get install -y poppler-utils`
  - a pinned `firecrawl-cli` (if OD12-a)
- **Nothing repo-dependent runs in the setup script.** Pipeline skills also run `node scripts/ready.mjs --json` as an explicit Step 0 command. That is a normal command, **not** a `!` injection: injected commands are permission-checked and abort the whole invocation outside auto mode (SKL-35 corrected).

### 2.7 Cloud enablement rule during migration (the delivery log)

A plugin's absolute path joins the environment's `CLAUDE_CODE_PLUGIN_DIRS` only when all of these hold:
1. all its HIGH defects are closed;
2. every handoff it makes has the §4.2 fallback, or its target is already enabled;
3. no same-named unit loads from another source (V2: same-named plugins from two paths **both** load);
4. its smoke suite passes.

Every change goes in `docs/rewrite/delivery-log.md` with the previous value, so rollback is one edit.

| Point | Value added | Why then |
|---|---|---|
| W0 | `/home/user/micky-psych-tools/plugins/gridgeist` (canary) | the least-coupled plugin; proves the route (§10 W0 check a) |
| W1 exit | `…/plugins/vault-keeper`, `…/plugins/firecrawl`, `…/plugins/plugin-creator` | handoff-free after their W1 fixes |
| W2 exit | `…/pubmed-research-note`, `…/comprehensive-review`, `…/clinical-infographic`, `…/ml-concept-lab`, `…/code-explainer`, `…/concept-animation` (atomic swap with the learn-hub copy), and the folder `/home/user/learn-hub/plugins` **after** the forks are deleted | runtime MCP resolution and fallbacks are in place; the forks and the CA copy are gone |
| W3 entry | replace all micky per-plugin paths with the folder `/home/user/micky-psych-tools/plugins` | the folder path absorbs the family renames with no further env edits. It also loads the four plugins not yet enabled (intent-lock, decision-interview, plan-critique, psych-paper-digest); their callers already carry fallbacks, and W3 rewrites them first. |

### 2.8 Collisions with claude.ai-synced skills

| Collision | Fix | Evidence |
|---|---|---|
| `psych-paper-digest`: micky watchlist triage vs `anthropic-skills:psych-paper-digest` (daily 8–12 papers) | Rename the micky skill to `lit-watch` (W3, inside the `evidence` merge; `renames` covers the plugin) and keep `/digest` as a dmi alias (OD7-a, OD9-a). Reciprocal Not-for clauses. | SKL-55 corrected; INV psych-paper-digest-6 |
| `daily-random-review` "chains into the comprehensive-review … skills internally", with ZERO citations, writing to `Finish/Micky/` | Add a comprehensive-review Not-for naming it. The owner edits the synced skill to "follow the structure below" (OD8-a). Until then, the §4.2 fallback lets its unattended runs complete (W2 exit test). | V8 (synced SKILL.md:12-13, :128) |
| `obsidian-knowledge-vault` ("atomize", "make notes from") vs atomize-book / vault-atomizer / the pubmed "atomize" gate | Every "atomize" description names its **input** (book file / note id / finished report) plus reciprocal Not-for. The pubmed publish gate word becomes **"digest"**. vault-atomizer becomes user-only. | LOC-31 (P0-2 open) |
| `bullet-reconstruct` vs ingest-article's "bullet-reconstruct this"; `pdf` vs pdf-pipeline | Drop the trigger (W1). pdf-pipeline is scoped to "get a PDF into the Learn hub", with a Not-for naming `anthropic-skills:pdf`. | INV ingest-article-10 |

The validator keeps a committed list of synced names (R7) and fails on a new collision.

---

## 3. Disposition table (every unit)

**Conventions.**
- `dmi` = `disable-model-invocation: true`. This makes the skill user-only: its description leaves Claude's listing and the name remains typeable (SKL-36).
- Waves are defined in §10.
- "Rest of INV \<unit\>" means every remaining medium and low defect of that unit closes in the wave that rewrites it (risk-first rule). A deferral must be listed in the ratchet with a reason.
- Every rewritten skill ends in the house shape:
  - description = capability clause + `Use when …` + `Not for … (use plugin:skill)`, ≤1,024 chars hard, ≤600 soft (R3–R5);
  - `metadata.profile: cc` (OD13);
  - standing rules first (R12);
  - conditional references (R14);
  - `## Gotchas` (R23);
  - no version narration (R18);
  - ≥3 eval cases (R71).

### 3.1 micky-psych-tools plugins (14)

| Unit | Today | Disposition | Target | Reason | Defects fixed |
|---|---|---|---|---|---|
| pubmed-research-note | 1.7.0; 1 skill; `.mcp.json` (one of 6 identical copies, P4); loads on Windows only | rewrite in place (W2), merge (W3) | `evidence` (renames entry) | Shares MCP, report contract and engines with CR and lit-watch. Only same-plugin files can be shared (PLG-22). The NCT grammar exists in 3 variants. | H44, H45 (skill rows); INV pubmed-research-note-5, -8 |
| comprehensive-review | 0.3.0; 1 skill + `/comprehensive-review`; `.mcp.json` | rewrite (W2), merge (W3) | `evidence` | Near-verbatim copies of pubmed's depth, citation and firecrawl contracts | INV comprehensive-review-2, -4 |
| psych-paper-digest | 0.1.1; 1 skill + `/digest`; `.mcp.json`; state in cwd (lost in cloud) | fix (W1), merge + rename skill (W3) | `evidence`, skill `lit-watch` (OD7) | Same engines; name collision (SKL-55) | H46, H47; INV psych-paper-digest-6 |
| intent-lock | 0.4.2; intent-lock + misread-capture; Step 0 of 5+ skills | merge (W3) | `alignment` | The three gates copy threshold, picker and fallback with drift (INV alignment obs.) | H01–H05 (skill rows) |
| decision-interview | 0.1.1; 1 skill + cmd; no README, CHANGELOG or evals | merge (W3) | `alignment` | Same family; silence and question-cap drift | INV decision-interview-1, -4, -5 |
| plan-critique | 0.1.0; 1 skill + cmd | merge (W3) | `alignment` | Same family; opposite silence wording | INV plan-critique-4 |
| clinical-infographic | 0.2.1; 1 skill + `/infographic` | fix (W1), filing (W2), merge (W3) | `visuals` | The shared HTML contract is 38% of its body (INV renderers obs.) | H36, H37; INV clinical-infographic-6, -7 |
| concept-animation | 0.1.1; 1 skill + `/animate` | rewrite (W2), merge (W3) | `visuals`: **sole owner**, absorbing the learn-hub copy | The stage-collapse fix exists only in the learn-hub copy (LOC-34) | H38, H39 |
| ml-concept-lab | 0.1.0; 1 skill + `/visualize` | rewrite (W2), merge (W3) | `visuals` | Same collapse rule; broken verify | H40, H41; INV ml-concept-lab-9 |
| code-explainer | 0.1.0; 1 skill + `/explain-code` | fix (W1), merge (W3) | `visuals` | Shared HTML contract; missing template | H42; INV code-explainer-6 |
| firecrawl | 0.2.0; 4.2k-token "verbatim" vendor body | refresh (W1), split (W3) | `firecrawl` (slim) + dated vendor reference; `defaultEnabled: false` (R30); OD12 | Stale vendor text in load-bearing places; writes the key into cwd `.env` | H12; INV firecrawl-2..10 |
| gridgeist | 0.1.0; vendored MIT | keep (W3 metadata only) | `gridgeist` + `UPSTREAM.md`; drop the Codex `agents/openai.yaml` and unused assets; W5 usage decides whether it stays delivered (OD10) | Healthy; content stays verbatim to avoid forking upstream | INV gridgeist-1..4 |
| plugin-creator | 0.3.0; 2 skills, 3 commands; calls repo-root `scripts/*.py` that the cache never holds | guard (W1), rewrite (W3) | self-contained `plugin-creator`: `scripts/validate.py` and `release.py` inside; remote SessionStart hook sets micky `core.hooksPath` | The root cause of H07 is scripts outside the plugin (R44) | H07; INV plugin-creator-2..14 |
| vault-keeper | 0.4.0; 2 skills + `/empty-vault`; root via walk-up or `${CLAUDE_PLUGIN_ROOT}/../..` | rewrite (W1 resolver, W2 sink and transfer) | `vault-keeper`: output-sink owner (OD4-a) | Root resolution wrong both ways (LOC-35, LOC-36); dead drain handshake | H08, H09, H10, H11; INV vault-keeper-5..15 |

### 3.2 micky-psych-tools skills (17 + scaffold template)

| Unit | Today | Disposition | Target | Reason (evidence) | Defects fixed |
|---|---|---|---|---|---|
| pubmed-research-note | Body ~4.7k tok + ~5.9k mandatory refs. `Reframed:` preface (SKILL.md:263). Hard-coded MCP prefix with "No ToolSearch step" (tool-catalog.md:25-28). No path when intent-lock or vault-keeper is absent. Decision brief says "first four" + "last three" over 6 headings (P6). | rewrite: **W2** (preface, fallback, runtime MCP, sink, gate word "digest", `contract: report/1`); **W3** (move; 6-slot brief: interview fixes slots 1, 2, 6, scope boundary rides in the lock record, skill derives 3–5, `intent-lock-pairing.md:49-57` aligned; dedupe opt-out ×4 and depth ×4; body ≤4k, mandatory refs ≤3k) | `evidence:pubmed-research-note` | Stale against intent-lock 0.4.2; contract drift | H44, H45; INV pubmed-research-note-3..14 (PMID-in-Sources contradiction, prefix, absent-dep path, NCT grammar, slug rule, "never invent a vault path", repetition) |
| comprehensive-review | "No section without a number" vs thin domains (SKILL.md:132-133 vs :35-36); no engine-failure policy; cites nonexistent "house rules"; output location unspecified | rewrite: W2 (fallback, sink, report contract copy aligned *interim*), W3 (move; the interim copy is deleted in favour of `evidence/references/report-contract.md`; thin domain = one sourced sentence naming what exists; "source floors" → "evidence types"; Not-for `anthropic-skills:daily-random-review`; Thai-trigger eval) | `evidence:comprehensive-review` | INV CR set | INV comprehensive-review-1..12 |
| psych-paper-digest | Windows on `pdat` (sweep-recipes.md:39-40); `max_results 50` with no pagination; dedup vs newest digest only; window math in prose; state in cwd | fix W1: `datetype: edat`, `retstart` pagination to exhaustion with a per-domain cap and the unscreened count in the header, CT.gov `AREA[…]RANGE`, dedup against every overlapping digest, UTC+7 stated. W3: rename `lit-watch`, `scripts/sweep.py` (window, pagination, dedup, filenames), state → `state/lit-watch/`, Not-for vs the synced digest; `context: fork` only if evals show a gain (R37) | `evidence:lit-watch` (+ `/digest` alias) | SKL-55; R63 | H46, H47; INV psych-paper-digest-3..13 |
| intent-lock | 6.2k body (~8.1k on invoke); silent contract contradicted in 11 places, patched by "reinterpret" (SKILL.md:16,22 vs :49…:206); claude.ai picker types; no picker-absent fallback; version narration | rewrite **by subtraction** (W3) to ≤2,000-token body; mechanics in `interview-protocol.md` (AskUserQuestion: 1–4 questions, 2–4 options, `multiSelect`, automatic Other); picker absent or errored → autonomous fallback; returns `lock-record.md` slots; "craft my prompt" resolved (a prompt is allowed when the user names it as the deliverable); description procedure-free | `alignment:intent-lock` | R11 gate ≤2k; R53 | H01, H02; INV intent-lock-6..8, -11..14, -16 |
| misread-capture | Ledger written under `${CLAUDE_PLUGIN_ROOT}` (SKILL.md:39); `Prior:` has no eliciting question; promised "review/edit" mode absent | rewrite (W3): Q1 "what did you want instead" → `Axis missed`; Q2 "what should I check next time before starting" → `Prior`; `scripts/ledger.py` → `$MICKY_TOOLS_DIR/state/misreads.md` (OD6); offers a commit after appending; newest first; review/edit mode implemented as `ledger.py list/retire` | `alignment:misread-capture` | PLG-24, PLG-57, LOC-37 | H03, H04; INV intent-lock-9, -10 |
| decision-interview | Unprompted trigger drops the materiality threshold; undetectable fallback; no evals | rewrite (light, W3) on `interview-protocol.md`; fallback on picker absent or errored; README, CHANGELOG, evals | `alignment:decision-interview` | R20, R53 | INV decision-interview-1..6 |
| plan-critique | Command vs skill disagree on the no-plan case; hand-off unreachable; 807/854-char mega-bullets | rewrite (light, W3): no plan → intent-lock drafts; split bullets; shared silence vocabulary; misread-capture carve-out; lens names match the reference; lens list out of the description | `alignment:plan-critique` | R19, R4 | INV plan-critique-1..8 |
| clinical-infographic | Template and example ship `prefers-color-scheme:dark` (template:100-104); `.mech` strip cramps (template:74-75,:93); AA claim false; sub-12px text; assets dead-end in `vault/assets` | fix **W1**: remove the dark block, add `:root{color-scheme:light}`, stack `.mech` at the mobile breakpoint, darken c2/c3, enforce ≥12px, in template and example. **W2**: render/verify via `audit:visual` (fallback `check-html.mjs`); filing via the sink to `research-notes/visuals/`. **W3**: move; `lessons-learned.md` → CHANGELOG history; SKILL points at the example | `visuals:clinical-infographic` | learn-hub's `auditInfographicResponsive` flags both | H36, H37; INV clinical-infographic-3..10 |
| concept-animation | Prescribes `.wrap{height:100dvh}` + `min-height:0` stage (grammar:46,:48); single 1366×768 fit check; doctype-less example; no ML boundary | rewrite **W2**: port learn-hub's grammar (`min-height:100dvh`, `.wrap>*{flex:0 0 auto}`, stage `max(220px,min(38dvh,280px))`, flex-basis 0, full document + `color-scheme`); verify at five viewports incl. 844×390 with sort-by-top overlap check (via `audit:visual`); keep micky's sourcing discipline; filing via the sink; reciprocal Not-for with ml-concept-lab. W3: move | `visuals:concept-animation` | LOC-34 | H38, H39; INV concept-animation-3..10 |
| ml-concept-lab | Same collapse rule (build-contract:140-141); verify recipe fails on ESM playwright (:195-197); relative-error gradient check; clinical routing contradicts itself; wrong example path; ~10.8k per full load | rewrite **W2**: layout port, verify via `audit:visual` / `check-html.mjs` (Playwright resolved with `createRequire` from `npm root -g`, Chromium from env), absolute-difference gradient check with a noise floor, clinical → concept-animation, example via `${CLAUDE_PLUGIN_ROOT}/examples/`. W3: move; body + mandatory ≤5k | `visuals:ml-concept-lab` | | H40, H41; INV ml-concept-lab-3..9 |
| code-explainer | Points at `references/explainer-template.html`, which never existed (**SKILL.md:30, :99**; README.md:86-87; references/ holds only `explanation-contract.md` and `vscode-shell.md`) | fix **W1**: remove every pointer and say "build from `vscode-shell.md` + `explanation-contract.md`"; validator dead-link rule. W3: move; byte-fidelity check into `check-html.mjs`; theme named "Dark Modern" consistently; ML boundary. Template only if an eval shows a gain | `visuals:code-explainer` | R13 | H42; INV code-explainer-2..6 |
| firecrawl | Stale vendor guide (build skills need `firecrawl setup build`; `ask` → `doctor`; keyless scope); writes `.env` | refresh **W1** with a `fetched: <date> <url>` stamp; never write `.env` (key from environment); gitignore `.firecrawl/`. **W3** split: ≤1.5k-token router (marketplace contract, credential hygiene, path table) + `references/vendor-onboarding-<date>.md` on demand. Headless fallbacks for the browser flow. | `firecrawl:firecrawl` (OD12) | SKL-19; R45 | H12; INV firecrawl-2..10 |
| gridgeist | Lean (~1.1k tok) | keep | unchanged body | Vendored | none (content) |
| plugin-creator | Cwd-bound; imperative description; stale Not-for; scaffold fails its own audit; stdio MCP forbidden | guard **W1**: root = `MICKY_TOOLS_DIR` → marker; else stop. **W3**: scripts inside the plugin; third-person description; Not-for → refine-plugin; the scaffold writes README, CHANGELOG, one `evals/<skill>/trigger-basic/` case and alias-free skills (no `commands/`); hooks template in exec form with `${CLAUDE_PLUGIN_ROOT}`; stdio allowed | `plugin-creator:plugin-creator` | R44 | H07; INV plugin-creator-2..13 |
| refine-plugin | Bumps without a CHANGELOG entry; second-person description | rewrite (W3): release through `release.py` (plugin.json + CHANGELOG); dmi (OD10) | `plugin-creator:refine-plugin` | R35, R85 | INV plugin-creator-3, -5 |
| templates/SKILL.md (plugin-creator reference) | `{{PLACEHOLDER}}` breaks YAML (PyYAML ConstructorError) | rewrite (W3): quoted placeholders; house shape; `argument-hint`; `metadata.profile`; validator fails on leftover `{{` outside `templates/` | `plugin-creator/references/templates/SKILL.md` | R2 | INV plugin-creator-6 |
| vault-keeper | Root via walk-up (matches learn-hub) or `../../vault` (wrong in the cache) (SKILL.md:28-29); "four jobs" vs five; index job in prose; Obsidian links by title | rewrite **W1**: `scripts/sink.py` resolver (§5.3) replaces both heuristics; `vault/.vault-id`. **W2**: sink routes reports and assets to the learn-hub inbox when `LEARN_HUB_DIR` validates (OD4-a); `vault_index.py`; five jobs stated once; Obsidian aliases | `vault-keeper:vault-keeper` | R47; PLG-58 corrected | H08, H09; INV vault-keeper-6..10, -13..15 |
| empty-vault | Looks for the deleted `.claude/skills/digest-report/` marker (SKILL.md:36-37); deletes assets that learn-hub waits for (:54-57); Windows fallback path | **W1** stopgap: dmi; learn-hub detection via `LEARN_HUB_DIR` → marker → ask; **never delete assets** (listed as "held"). **W2**: becomes a *transfer*: `drain_plan.py` plan → validate → copy into the inbox → verify sha → learn-hub commit (on confirmation) → delete only verified items; kinds with no receiver (code-explainer, other) are held forever | `vault-keeper:empty-vault` (typed `/empty-vault` kept) | R22, R35; LOC-35 | H10, H11; INV vault-keeper-5, -11, -12 |

### 3.3 micky-psych-tools commands (12)

All `commands/` directories are deleted in W3 (R34). Argument handling moves to `argument-hint` and `$ARGUMENTS` on the target skill. Where the short name differs from the skill name, a **dmi alias skill** keeps the habit at zero listing cost. The alias is a 5-line `SKILL.md` that says "Invoke `<plugin:skill>` with: $ARGUMENTS" (OD9-a). A bare skill name resolves unless it is shadowed (PLG-17).

| Command | Today | Disposition | Target | Reason | Defects fixed |
|---|---|---|---|---|---|
| `/comprehensive-review` | wrapper | retire (W3) | skill `evidence:comprehensive-review` (bare name unchanged), `argument-hint: "[disorder or topic]"` | wrapper | — |
| `/digest` | wrapper | retire → alias | alias skill `evidence:digest` → lit-watch | habit + rename | INV psych-paper-digest-6 |
| `/infographic` | wrapper; summary lags the skill | retire → alias | `visuals:infographic` | habit | INV clinical-infographic (commands drift) |
| `/animate` | wrapper; collides with the learn-hub copy's trigger | retire → alias | `visuals:animate` | habit | — |
| `/visualize` | wrapper; stale "fits one screen" | retire → alias | `visuals:visualize` | habit | INV ml-concept-lab (command drift) |
| `/explain-code` | contradicts Step 0 on empty args | retire → alias | `visuals:explain-code` | habit | INV code-explainer (command drift) |
| `/critique-plan` | contradicts the skill on the no-plan case | retire → alias | `alignment:critique-plan` | habit | INV plan-critique-1 |
| `/resolve-decisions` | wrapper | retire → alias | `alignment:resolve-decisions` | habit | — |
| `/new-plugin` | omits the router step | retire → alias | `plugin-creator:new-plugin` | habit | INV plugin-creator-12 |
| `/refine-plugin` | wrapper | retire | skill `plugin-creator:refine-plugin` (dmi; same name) | — | — |
| `/empty-vault` | wrapper; kebab → MOC mapping undefined | retire | skill `vault-keeper:empty-vault` (dmi; same name); `drain_plan.py` defines the mapping | — | INV vault-keeper-15 |
| `/route` | reads, then regenerates ROUTING.md; writes to answer a read-only question | retire | none: descriptions + reciprocal Not-for + trigger evals (R91) | router deleted | INV plugin-creator-14; INV route.py / ROUTING.md-1..5 |

### 3.4 micky-psych-tools repo files

| Unit | Today | Disposition | Target | Reason | Defects fixed |
|---|---|---|---|---|---|
| `scripts/validate.py` | Tracebacks on bad JSON (:72-73, :111-114); hand-rolled YAML; rejects stdio MCP; 200-char floor as a failure | fix **W0** (guarded loads, counted checks, CRLF-safe, `yaml.safe_load`, ratchet + trigger-lock, no version parity); move + rewrite **W3** | `plugins/plugin-creator/scripts/validate.py` (§8) | R29, R65 | H13; INV validate.py-2..6 |
| `scripts/route.py` | Writes on `--help`; versions in output; shapes description wording | fix **W0** (argparse, no versions); retire **W3** | none | R91; LOC-08, LOC-09 | INV route.py / ROUTING.md-1..5 |
| `scripts/bump.py` | Dual write; ASCII escapes; no newline; writes before validating; no CHANGELOG | rewrite **W0**: plugin.json only, CHANGELOG stub, dry run by default (`--write`), validate first, UTF-8 + newline. Move **W3** | `plugins/plugin-creator/scripts/release.py` | R83, R85; J1 graft | INV bump.py-1..4 |
| `ROUTING.md` | ~5k tokens mandated per request; 29/29 cues verbatim; 0 Not-for | demote W0 (mandate stays until the W3 description pass), retire **W3** | none | R90, R91 | INV route.py / ROUTING.md-1, -3 |
| `CLAUDE.md` (micky) | 13,954 B; 69% plugin catalog (gridgeist missing); mandates MEMORY + ROUTING; "version in two files" rule | edit **W0** (version rule → plugin.json only); rewrite **W3** to ≤5 KB: layout, placement rules, health command, delivery pointer; no catalog (points to marketplace.json), no mandated reads; the Agent-skills pointers (`docs/agents/*`, lazily created `CONTEXT.md` / `docs/adr/`, LOC-24) kept | `CLAUDE.md` | R88, R90, R92 | INV CLAUDE.md (micky-psych-tools)-1..5 |
| `MEMORY.md` | 108,178 B, ~27k tok mandated; ~30 of 51 milestones are content filings; versions table | split **W3**: living section ≤6 KB (identity, delivery facts, open threads, current wave), read on demand; history → `docs/history.md`; versions table deleted (`validate.py --versions` generates it) | `MEMORY.md` + `docs/history.md` | LOC-25; R88, R90 | — |
| `README.md` (root) | Validation lacks `--strict`; "must be public"; `git add -A` with `.env` not ignored | rewrite **W0** (commands, private-repo note) and **W3** (install per environment §2.5; no catalog copy) | `README.md` | LOC-40 | INV README.md (root)-1..4 |
| `.claude-plugin/marketplace.json` | Entry versions; 9/14 descriptions drift; hand-bumped top-level version | **W0**: strip entry versions (J1 graft; PLG-06; the CLI catches drift, LOC-03). **W3**: `$schema`, top-level `description`, entries `{name, source, category, keywords}`, descriptions omitted (plugin.json is the single source), `renames` for the families | marketplace.json | R33, R83, R87 | INV marketplace.json-1..3 |
| `.gitignore` | Lacks `.env`, `.firecrawl/`, eval results | fix **W0** | adds `.env`, `.firecrawl/`, `plugins/*/evals/results/` | R48; EVL-26 | INV firecrawl-3, README-4 |
| `docs/agents/*.md` | issue-tracker, triage-labels, domain | keep | unchanged; CLAUDE.md points to them | healthy | — |
| `docs/superpowers/plans/2026-07-10-improve-all-plugins.md` | all 11 tasks done, 61 unchecked boxes | archive note (W3) | header "completed; superseded by docs/rewrite/" | LOC-27 | — |
| `vault/` | 7 artifacts, 6 MOCs, empty `assets/` | keep (OD4-a) + `.vault-id` (W1) | fallback sink; drained by empty-vault's transfer | OD4 | — |
| per-skill `evals/evals.json` (12 files in micky, 4 in learn-hub; 118 cases, all `assertions: []`) | inert, ungraded | convert per family (W3/W4): prompts mined as case seeds; graders hand-written; files deleted | `plugins/<p>/evals/<skill>/<case>/` | R70; EVL-04 corrected | INV *-evals (e.g. intent-lock-16, pubmed-research-note-13) |
| per-plugin README / CHANGELOG | 5 plugins lack a CHANGELOG (LOC-23); several skip versions | **W0** backfill (pubmed 1.3.0/1.4.0, psych-paper-digest 0.1.1, vault-keeper 0.3/0.4, intent-lock 0.4.1, clinical-infographic 0.2.1) + first CHANGELOGs | one README, CHANGELOG and LICENSE per plugin | R45, R85 | INV pubmed-research-note-7, vault-keeper-9, … |

### 3.5 learn-hub plugins (8), their commands and the catalog

| Unit | Today | Disposition | Target | Reason | Defects fixed |
|---|---|---|---|---|---|
| `learn-hub-local` catalog | never registered or enabled; fails `--strict` (no description) | retire (**W2**; `claude plugin marketplace remove` first if W0 finds it installed on Windows) | none | nothing left to list | H14; INV learn-hub-local-2..6 |
| intent-lock (fork: 2 skills + second `misreads.md`) | identical except README; splits the ledger | retire (**W2**): merge its ledger entries into micky's ledger first | `alignment` (micky) | V2 double-load; LOC-33 | H06; INV intent-lock (learn-hub clone)-2..4 |
| pubmed-research-note (fork) | the only delta is the filing path (LOC-33); evals fail by construction; writes the report twice | retire (**W2**, the same wave the sink lands) | `pubmed-research-note` + vault-keeper sink → inbox | forks drift | H48; INV pubmed fork-2..9 |
| comprehensive-review (fork) + `/comprehensive-review` | digest + live Supabase sync by default | retire (**W2**) | `comprehensive-review` + sink; publish only on "digest" (OD5) | production writes by default | H49; INV CR fork-2..6 |
| digest-report (+ `/digest-report`) | not loaded anywhere; demands inline citations that producers forbid; PowerShell process check; conflicting "pending reports" semantics | convert to project skill + rewrite (**W2**) | `.claude/skills/digest-report` (model-invocable): **owner of the inbox contract**; tolerant reader (`## Sources` + legacy inline PMIDs); bare invocation = survey then stop; "digest `<report>`" = digest; writes the intake log; Linux/Windows-portable process check; `source:` topic field; `\$` rule; links to sync-vault | H15, H16; R60 | H15, H16; INV digest-report-3..12 |
| source-to-vault (skill `ingest-source`, `/ingest`) | prod rows with no /vault file; no-arg batch ingest of `Book/`; routing collision; omits embedding/diagrams/images | retire (**W1**) | superseded by pdf-pipeline → atomize-book / ingest-article | active hazard | H17, H18, H19, H20; INV source-to-vault-5..10 |
| vault-atomizer (+ `/atomize`) | never loaded; foreground sync; stale stats; graph reference | convert to project skill (**W2**), user-only | `.claude/skills/vault-atomizer` (dmi); sync via sync-vault (background); `/atomize` **dropped** (collides with atomize-book, OD9) | LOC-31 | INV vault-atomizer-1..8 |
| vault-vectors (+ `/vectors`) | never loaded; command contradicts the skill on syncing; `--no-report` undefined | convert to project skill (**W2**), user-only | `.claude/skills/vault-vectors` (dmi; typed as `/vault-vectors`, alias `/vectors` per OD9) | | INV vault-vectors-1..6 |
| pk-plasma-animation (+ `/pk-animation`, `.mcp.json`) | never loaded; hand-built upsert; brief's Sources format contradicts pubmed; eager refs; duplicate MCP | convert to project skill (**W2**), user-only | `.claude/skills/pk-plasma-animation` (dmi; alias `/pk-animation`); **no `.mcp.json`**; research via `pubmed-research-note` by name (OPTIONAL-with-stop); brief defers to `report-contract`; filing via `ingest-visual`; lazy refs; absorbs the learn-hub CA copy's builder pattern | R41, R58 | INV pk-plasma-animation-1..9 |

### 3.6 learn-hub project skills (11)

| Unit | Today | Disposition | Target | Reason | Defects fixed |
|---|---|---|---|---|---|
| atomize-book | 1,256 lines, ~21.3k tok; `[[topic-id]]` self-contradiction (:295-296 vs :1027-1029); stale whole-vault sync economics; 4 drafting rules missing (`\$`, equation-as-PNG, stadium ban, `LIVE_GROUPS`); one-level glob; description 1,075 chars | fix **W1**: one topic-id rule (chapter reference; body only; never repointed; never in `links:`); background `sync:apply` via sync-vault; the four rules into the drafting spec + note-format; find-based id check; mermaid via `scripts/check-mermaid.mjs`; description ≤1,024 without the sync trigger; "add to `coverage-sources.json` and `LIVE_GROUPS`" checklist item. **W4** split (freeze window): body ≤500 lines / ≤5k tok; reference-grade sections moved **verbatim** to `references/{extract,figures,measure,qc,traps}.md` with "Read X before step N"; gotchas from CLAUDE.md into `references/gotchas.md`. **Python stays where it is** (354 tests; `npm run test:py` added) | `.claude/skills/atomize-book` | R11, R19; LOC-46 | H21, H22, H23, H24; INV atomize-book-5..14 |
| ingest-article | Windows inbox + repo-relative deletes, not ignored (:3, :49, :51, :348); source-cover command cannot run; `diagrams {}` fallback; ~18.7k tok per run; description 1,137 chars, invalid YAML, "bullet-reconstruct this" trigger | fix **W1**: a bare invocation **surveys the inbox and asks** before ingesting or deleting; `ARTICLE_INBOX_DIR` (default `Raw Article PDF/`) + gitignore; source-cover fixed (pass a notes dir) or dropped; the required `measure-loss` flags in the reference; bake columns omitted, never `{}`; check-mermaid; description ≤1,024, folded YAML, trigger dropped; `ready.mjs` preflight. **W4**: conditional references (≤6k mandatory) | `.claude/skills/ingest-article` | R25–R27, R51 | H25, H26; INV ingest-article-3..10 |
| ingest-slides | Script paths wrong from the repo root (:62, :71); pdf-pipeline routes decks elsewhere; applies none of ingest-article's gates; 1,150-char description | fix **W1**: `${CLAUDE_SKILL_DIR}/scripts/…`; check-figures + measure-loss applied; sync via sync-vault; description ≤1,024; "grilling" remnants removed; `ready.mjs` | `.claude/skills/ingest-slides` (kept separate: vision OCR is a distinct job; lower churn than purist's merge) | R49, R9 | H27, H28; INV ingest-slides-3..7 |
| ingest-infographic | Dead empty-vault contract (:3, :137-138); "targeted upsert == npm run sync" (:116-118); stale `/infographic` route; invalid YAML | fix **W1** (YAML; sync-vault; `/visualization`); merge **W2** | `.claude/skills/ingest-visual` (kind `infographic`) | ~70% shared with ingest-animation | H29, H30; INV ingest-infographic-3..6 |
| ingest-animation | Dead contract; no stage-collapse or quirks-mode check; invalid YAML | fix **W1** (YAML); merge **W2** | `ingest-visual` (kinds `animation`, `explorable`); runs `npm run audit:visual` (auditAnimationLayout + doctype / color-scheme) and **refuses and returns** a failure to its author | CLAUDE.md animation gotchas | H31; INV ingest-animation-2..4 |
| pdf-pipeline | Slides → atomize-book (:98; routing.md:42,:60); impossible ≲200 KB apply rule (:138-141 vs :150); nested vault path; graph/card-wall checks; stale preflight premise | fix **W1**: decks → ingest-slides; apply = `sync:apply` via sync-vault only; flat layout; stale surfaces removed; Not-for `anthropic-skills:pdf`; `ready.mjs`. **W4**: `scripts/classify_pdf.py` (DOI/abstract/TOC/ISBN/page count → suggested route) | `.claude/skills/pdf-pipeline` (the single broad PDF trigger) | R63 | H32, H33; INV pdf-pipeline-3..8 |
| sync-vault | Recommends the nested layout (:126-132); default `npm run sync` + MCP path, unusable at vault size (:32-34); whole-table count verification; deletion ignores `purge:hidden` / `merge_note_history` | rewrite **W1**, first: flat layout; default = `git fetch` + merge check → `npm run sync:preflight` (foreground, ~10 s; read the warnings) → `npm run sync:apply` as a **background job with a log** (no inner `&`); success = `EXIT=0` + `Upserted … note(s)`; per-provenance verification; deletion via `purge:hidden` / `merge_note_history`; revalidate; Not-for. The operational gotchas (TaskStop zombie, background exit-code trap, fetch-first) move here **verbatim** in W4 | `.claude/skills/sync-vault`: **sole owner** of the tail | R22; the CLAUDE.md sync gotchas | H34, H35; INV sync-vault-3..5 |
| vault-coverage | Windows `BOOK_ROOT` (SKILL.md:40); source map covers 26 of 70 books | fix **W1** (`BOOK_ROOT` env; absent = finding); user-only (W2); atomize-book's checklist adds map entries | `.claude/skills/vault-coverage` (dmi) | R47 | INV vault-coverage-1..3 |
| check-repetition | No Not-for vs detect-duplicates / atomize-book §7b; revalidation inconsistency | rewrite (light, W2): Not-for; revalidate via sync-vault; user-only | `.claude/skills/check-repetition` (dmi) | R8 | INV check-repetition-1, -2 |
| verify | Cites `mint-session`/`probe` scripts that never existed; no triggers or Not-for | rewrite **W4**: bundle `scripts/mint-session.mjs`, `scripts/probe.mjs` (the prose recipe made executable); triggers + Not-for (browser pane, chrome-devtools isolated world) | `.claude/skills/verify` | R63 | INV verify-1, -2 |
| concept-animation (learn-hub copy) | Invalid strict YAML; newer on layout, older on structure; bare `min()` floor; 4 viewports; `npm run sync`; stale builder path; duplicates ingest-animation | fix YAML **W1**; merge → retire **W2** by atomic swap: layout fixes → `visuals:concept-animation`; filing → `ingest-visual`; builder pattern → pk-plasma-animation references. The copy is deleted only after a **branch session** without it confirms micky CA loads | retired | LOC-34; R62 | H43; INV concept-animation (learn-hub copy)-2..8 |

### 3.7 learn-hub CLAUDE.md, hooks, and new operational units

| Unit | Today | Disposition | Target | Reason | Defects fixed |
|---|---|---|---|---|---|
| `learn-hub/CLAUDE.md` | 3,126 lines, 268,390 B (~67k tok); in context from session start in multi-repo sessions (observed); 58 of 136 gotcha headings are pipeline procedure; drifts from the skills in both directions | factual corrections **W1** (figure disposition list, `book:file-figures`, pk-plasma location, sync-vault as owner of the tail); split **W4**, stage (a): pipeline gotchas → owning skill `references/gotchas.md` verbatim; vault format → `docs/vault-format.md`. Stage (b), per OD11: app gotchas + Pages → `.claude/rules/*.md` with `paths:`. **Exit artefacts:** `docs/rewrite/gotcha-map.md` (every one of the 136 headings → destination, none dropped) and `docs/gotchas-archive.md` | ≤32 KB (OD11-b) | R89, R92; memory.md "under 200 lines" | INV project-skills obs. "gotcha drift" |
| `.claude/settings.json` hooks | SessionStart + 2 PreToolUse(Bash) gates; never load in multi-repo sessions | **W1**: PreToolUse gates removed (they run inside the sync preflight; saves two node spawns per Bash call, LOC-44). **W2**: SessionStart kept for single-repo sessions, duplicated by the plugin for multi-repo, idempotent | settings.json (SessionStart only) | RF-A3; P2 | multi-repo safety (R3 risk) |
| `.claude/hooks/session-start.sh` | `cd "$CLAUDE_PROJECT_DIR"` = `/home/user` in multi-repo (V9) | fix **W1**: root = `LEARN_HUB_DIR` → marker-checked `CLAUDE_PROJECT_DIR` → own path; done-marker; the ready line also prints `claude --version` and the loaded plugins | same path (tests keep working) | V9 | — |
| `.claude/hooks/pre-sync-gate.sh`, `pre-sync-repetition-gate.sh` | PreToolUse gates | retire (**W1**) → `scripts/lib/sync-preflight.mjs` calls the same pure modules (`gate-plan.mjs`, `repetition.mjs`); warn-only semantics unchanged | inside `apply-sync.mjs` / `sync-vault.mjs` + `npm run sync:preflight` | runs identically on Windows and in every cloud layout (J1/J2 graft) | — |
| `plugins/learn-hub-session` (new) | — | new (**W2**) | hooks-only plugin (§2.3). A **declared exception to R44/R47**: repo-bound, loaded only in place, marker-guarded (a cached copy exits without acting) | T5; P2 | — |
| `scripts/ready.mjs`, `sync-preflight.mjs`, `audit:visual` CLI, `skill-lint.mjs`, `eval-project-skill.sh`, `check-contract.mjs` (new) | — | new (W0–W2), each with vitest tests | §4, §6, §8 | R63, R68 | LOC-30 P1-1 closed |

---

## 4. Shared-content strategy

### 4.1 Inside a plugin: the family is the unit of sharing

- A family's contracts are stated **once** at the plugin root (`references/`, `scripts/`). Each SKILL.md links only the files it needs, one level deep, with a load condition ("Before the first question, read `interview-protocol.md`") (SKL-16, SKL-18, R13, R14).
- This survives a cache copy (PLG-22) and needs no symlinks (PLG-23).

| Family file | Replaces (today's duplication) |
|---|---|
| `alignment/references/interview-protocol.md` | Threshold, destructive always-ask, picker mechanics and fallback, copied ×3 with drift. One silence rule: "a rejected, unavailable or errored picker routes to the autonomous fallback". The question-cap rationale is stated once: intent-lock 3 by design, siblings 4 by tool ceiling (INV decision-interview-4, -5; plan-critique-4). |
| `alignment/references/lock-record.md` (purist; J1 graft #10) | The drifted `Assumed/Reframed/Skipped` preface (H05, H44). It defines the slots intent-lock returns: deliverable, question, scope in/out, emphasis, audience, exclusions, assumed defaults. It also defines the single hand-back line `Assumed: <reading> — say if wrong.` |
| `evidence/references/report-contract.md` | The Sources grammar (topic → DOI/URL; no authors, journal, year or PMID, per pubmed SKILL.md:219-221) with **one** NCT line form, replacing 3 variants (INV pubmed-research-note-8). Also: no inline citations, the depth contract, the engine-failure policy (PubMed down = fatal; registry down = named gap), report frontmatter (`contract: report/1`), and the voice rule (LOC-28 P0-1). `sources_lint.py` enforces the mechanical half. |
| `evidence/references/engines.md` | Tool resolution (§4.4), E-utilities (`datetype=edat`, `retstart`), CT.gov v2 `AREA[…]RANGE`, the firecrawl fetch-only contract |
| `visuals/references/html-artifact-contract.md` | ~265 near-duplicate lines across the 4 renderers (INV renderers obs.). It summarizes and **points to** learn-hub's executable audit (§4.3). |
| `vault-keeper/references/vault-layout.md` | The vault layout, restated in 6 places today (INV vault-keeper-13) |

### 4.2 Across plugins: by name, OPTIONAL, with a fallback. No `dependencies`.

- No plugin declares `dependencies`. RF-A2 and V4: a declared dependency that is absent **disables** the dependent plugin, and delivery grows plugin by plugin (§2.7).
- Since nothing is REQUIRED, R56 is met in substance: every cross-plugin reference is an OPTIONAL handoff with a fallback (R57, R58).
- The single handoff sentence lives in `lock-record.md` §Handoff. Callers carry it verbatim, as a one-line restatement (the only permitted duplication):

> Run `<plugin:skill>` (OPTIONAL). If it is not available in this session — or it needs an interactive picker and none exists here (subagent, headless, scheduled run) — do not stall: take the broadest reading that fits the request and open the output with one line `Assumed: <reading> — say if wrong.`

- Filing uses the same pattern: "file via `vault-keeper` (OPTIONAL). If absent, write to `$LEARN_HUB_DIR/research-notes/` when its marker validates, otherwise to cwd, and say where."

### 4.3 Across repos: one owner per interface, no text copies

| Interface | Owner (file) | Consumer obligation | Drift check |
|---|---|---|---|
| Inbox layout, intake log, collision suffix `-2` | learn-hub `digest-report/references/inbox-contract.md` | vault-keeper's `sink.py` restates only the two target paths | validator: vault-keeper names `research-notes/` and `research-notes/visuals/` exactly |
| Report format (`contract: report/1`) | micky `evidence/references/report-contract.md` | digest-report is a **tolerant reader**: `## Sources` lines, legacy inline PMIDs, missing `contract` = legacy | `learn-hub/scripts/check-contract.mjs` runs digest-report's pure parser over `$MICKY_TOOLS_DIR/plugins/evidence/evals/fixtures/*.md` when present. Absent micky: a warning, not a failure. |
| Visual layout + self-containment | learn-hub audits behind `npm run audit:visual -- <file> --json` | visuals producers call it through `$LEARN_HUB_DIR`. `visuals/scripts/check-html.mjs` is a **fallback port** used only when learn-hub is absent (J1 graft #9). | **parity fixture**: the 4 example HTMLs + 2 known-bad fixtures must get the same verdict from both tools; run at W2 exit and whenever either side changes |
| Alignment hand-back line | `alignment/references/lock-record.md` | callers print exactly one `Assumed:` line and never `Reframed:` | regex grader in every caller's evals |
| Vault → hub transfer + handshake | learn-hub (the consumer defines its input): `inbox-contract.md` §Intake log | empty-vault reads `.intake-log.jsonl` and the learn-hub git state; it never deletes an unverified item | vault-keeper evals with a scaffolded fixture inbox (EVL-23) |

**Direction rule: consumers before producers.** A contract change lands on the consumer side first, accepting old and new (tolerant reader), then on the producer side (W2 step order).

### 4.4 MCP: one declaration, runtime resolution

- `evidence/.mcp.json` is the only PubMed/CT.gov declaration. Today there are 6 byte-identical copies, md5 `1b35ee7c…`: micky pubmed-research-note, comprehensive-review, psych-paper-digest; learn-hub pubmed fork, CR fork, pk-plasma-animation (P4).
- pk-plasma-animation loses its copy (W2).
- Until W3 merges them, the three micky copies stay, and the runtime rule below makes their duplication harmless (MP-PLG-2 endpoint dedup).
- The rule lives in `engines.md` and replaces every hard-coded `mcp__plugin_<p>_…` and "No ToolSearch step" (R41):

> Use the PubMed / ClinicalTrials tool present in this session: `mcp__PubMed__*` / `mcp__Clinical_Trials__*` (connector) or `mcp__plugin_*_pubmed__*` / `mcp__plugin_*_clinical-trials__*` (plugin). If neither is listed, run ToolSearch for "pubmed" once. If still none, use E-utilities / CT.gov API v2 via WebFetch.

### 4.5 Deterministic contracts become tested scripts (R63–R68)

| Script | Replaces prose in |
|---|---|
| `evidence/scripts/sweep.py` | lit-watch window math, 90-day cap, config read/write, `last_swept` advance, pagination, dedup across overlapping digests, filenames |
| `evidence/scripts/sources_lint.py` | the Sources grammar, the one NCT form, no inline citations |
| `alignment/scripts/ledger.py` | ledger append, list and retire; grammar; ordering; cap |
| `vault-keeper/scripts/{sink,vault_index,drain_plan}.py` | root and sink resolution; index rebuild and orphan report; transfer plan → validate → execute |
| `visuals/scripts/check-html.mjs` | self-contained, reduced-motion, doctype / color-scheme, light-lock, strip rule, five-viewport stage / overlap / controls (fallback port) |
| `plugin-creator/scripts/{validate,release}.py` | house rules; bump + CHANGELOG |
| learn-hub `sync-preflight.mjs`, `ready.mjs`, `audit:visual`, `classify_pdf.py`, verify's `mint-session.mjs` / `probe.mjs` | the sync precondition prose; the PDF routing tables; the verify recipe |

Every script provides:
- `--help` with no side effects;
- JSON on stdout and diagnostics on stderr;
- meaningful exit codes;
- dry run by default for writes;
- UTF-8 output with a trailing newline;
- an interpreter-prefixed invocation (`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/x.py`, COM-46) plus a matching narrow `allowed-tools` rule (SKL-33, R36);
- unit tests run by the health check.

### 4.6 Not shared, on purpose

- gridgeist (third-party; not merged into a family).
- learn-hub's audits: called, not copied, except for the one fallback port with its parity fixture.
- CLAUDE.md gotchas: moved to exactly one home, never duplicated into skills.
- atomize-book's Python: stays in place, reached by `npm run book:*`.

---

## 5. Cross-repo pipeline contract (report → vault → learn-hub)

### 5.1 Flow

```
micky producers (any session)                sink (vault-keeper sink.py)                    learn-hub (git-tracked inbox)                 learn-hub intake → app
evidence:pubmed-research-note ─┐                                                    ┌─▶ research-notes/<slug>.md ──"digest <report>"──▶ digest-report ─┐
evidence:comprehensive-review ─┼─ report .md ─▶ LEARN_HUB_DIR valid? ──yes──────────┤                                                                   ├─▶ /vault ─▶ sync-vault ─▶ Supabase
visuals:{infographic,animation,─┘  .html+.meta.json  │                                └─▶ research-notes/visuals/<slug>.* ─"file <asset>"─▶ ingest-visual ─┘   (preflight gates;
  explorable}                                         └─no─▶ micky vault/ (MICKY_TOOLS_DIR + .vault-id) ──/empty-vault (transfer)──▶ inbox          background; verify)
pk-plasma-animation (learn-hub) ──────────────────────────────────────────────────────────────────────────────────────────▶ ingest-visual
code-explainer / other kinds ─────▶ held in micky vault/assets (no receiver; never deleted by empty-vault)
```

### 5.2 Producers

| Producer | Output | Kind | Default destination (OD4-a) | Publish trigger |
|---|---|---|---|---|
| `evidence:pubmed-research-note` | report `.md` | `decision` | inbox if `LEARN_HUB_DIR` validates, else micky vault | "digest `<report>`" (OD5-a) |
| `evidence:comprehensive-review` | report `.md` | `topic` | same | same |
| `evidence:lit-watch` | digest `.md` | `digest` | `state/lit-watch/digests/` (triage only; filed to the inbox on explicit request) | Act items → pubmed-research-note |
| `visuals:clinical-infographic` | `.html` + `.meta.json` | `infographic` | `research-notes/visuals/` or micky `vault/assets/` | "file `<asset>`" |
| `visuals:concept-animation`, `visuals:ml-concept-lab` | `.html` + `.meta.json` | `animation` / `explorable` | same | same |
| `visuals:code-explainer` | `.html` | `code-explainer` | cwd; vault is opt-in (held; no learn-hub receiver) | none |
| learn-hub `pk-plasma-animation` | generated animation | `animation` | direct to `ingest-visual` | its own build step |

### 5.3 Sink resolution (`vault-keeper/scripts/sink.py`, tested)

1. An explicit destination in the request.
2. `LEARN_HUB_DIR`, or the `learn_hub_root` userConfig when loaded as an installed plugin (MP-PLG-3), **validated by marker** (`package.json` `"name": "learn-hub"` + `scripts/apply-sync.mjs`) → learn-hub inbox.
3. `MICKY_TOOLS_DIR`, validated by `vault/.vault-id` = `micky-psych-vault` → micky vault.
4. Otherwise stop and ask. In a non-interactive run: write to cwd and open with `Assumed: written to <path> — no hub or vault resolved`.
- No cwd walk-up and no `${CLAUDE_PLUGIN_ROOT}/../..` (fixes H08, H09; R47).
- The sink replaces risk-first's "git toplevel of cwd" rule, which fails in multi-repo sessions because `/home/user` is not a repo.

### 5.4 Formats

**Report** (`research-notes/<slug>.md`):
- Frontmatter: `title`, `kind: decision|topic|digest`, `topic`, `source_skill`, `created`, `contract: report/1`.
- The first body line is the single `Assumed:` line when defaults were taken.
- The prose carries no inline citations.
- It ends with `## Sources` per the report contract.
- The slug is deterministic from the title. On collision: `-2`, `-3`.

**Visual asset** (`research-notes/visuals/<slug>.html` + `<slug>.meta.json`):
- `.meta.json` fields: `{kind, title, description, topic_hint, source_report, producer, created, audit: {tool, verdict}}`.
- The HTML follows the html-artifact contract. It is a full document (`<!DOCTYPE html>`, `lang`, `color-scheme`, painted `html,body`). Sheets are light-locked.

**Git.**
- `research-notes/` is git-tracked (verified: not ignored).
- The producer offers a commit in learn-hub after writing, because cloud VMs are ephemeral.

### 5.5 Consumers

| Consumer | Accepts | Does | Never |
|---|---|---|---|
| `digest-report` | any `.md` in the inbox: `report/1`, or legacy (inline PMIDs) | A bare invocation surveys un-landed reports (sha not in the intake log) and **stops**. "digest `<report>`" writes atomic notes to `/vault`: per-note `sources:` = report basename + the Sources lines the note covers; `source:` topic field; `\$` money rule. Then **delegates** publishing to sync-vault. | publishes without the explicit word; restates the sync tail |
| `ingest-visual` | `research-notes/visuals/*.html` + `.meta.json`; direct calls from pk-plasma-animation | Runs `npm run audit:visual`. On failure it **refuses and returns** the findings to the author (it never silently fixes). It writes the `type: infographic|animation` sidecar into the topic dir, then delegates to sync-vault. | files an asset whose audit fails; files an unknown kind |
| `sync-vault` | a vault change | `sync:preflight` → background `sync:apply` → `EXIT=0` + `Upserted …` → revalidate → per-provenance verification | runs as the default in any other skill's text |

### 5.6 Handshake

- `research-notes/.intake-log.jsonl` is an append-only record, one line per intake: `{file, sha256, consumer, action: digested|filed|refused, rows, commit, at}`.
- A consumer writes its line only after sync-vault's per-provenance verification.
- empty-vault's **transfer** (dmi, W2) runs in this order:
  1. `drain_plan.py` writes a manifest (item → kind → receiver → destination).
  2. It validates: `LEARN_HUB_DIR` marker, receiver exists for the kind, no inbox collision.
  3. It copies into the inbox and verifies the sha.
  4. It offers a learn-hub commit.
  5. It deletes from the micky vault **only** items whose sha is present in the committed inbox.
  6. Kinds with no receiver are listed as held and never deleted.
- The Supabase sync stays learn-hub's business. empty-vault no longer calls digest-report across repos. That removes the dead handshake (H10, H11, H29, H31).
- Re-digest protection: digest-report skips any report whose sha is already logged as `digested`.

### 5.7 Publishing and safety

- Only `sync-vault` publishes, and only on an explicit "digest" / "publish" (OD5-a).
- The live Supabase project is shared with board-prep-hub.
- `apply-sync.mjs` runs `sync-preflight.mjs` first:
  1. **Readiness**: `node_modules`, `.env.local` or env vars, a resolvable Chromium. On failure it exits 2 and names `bash .claude/hooks/session-start.sh`.
  2. **Staleness**: HEAD behind `origin/master` → warning.
  3. The duplication and repetition **gates**, warn-only.
- The same modules the PreToolUse hooks used now run everywhere: Windows, single-repo and multi-repo cloud, and headless.

---

## 6. Evals strategy

### 6.1 Layout

- Plugin skills: `plugins/<p>/evals/<skill>/<case>/{prompt.md | case.yaml, graders/*.md}`, grouped by skill, tagged `smoke | trigger | negative | output | release` and filtered with `--tag` / `--case` (EVL-02, EVL-06; R70).
- MCP mocks: `plugins/evidence/evals/mocks/{pubmed,clinical-trials}/<tool>.md` (EVL-24).
- Fixtures: `plugins/evidence/evals/fixtures/report-*.md` (also used by learn-hub's contract check, §4.3).
- learn-hub project skills: `learn-hub/evals/<skill>/<case>/`, run through the wrapper (§6.5).
- No `evals.json` stays in either repo after conversion (R70).

### 6.2 Minimum per skill, before its rewrite lands (evaluation first: SKL-43, COM-27)

| Case type | Grader pattern | Source |
|---|---|---|
| Trigger positive: a realistic multi-step prompt using a locked phrase (a Thai one where it exists) | `tool_used: Skill`, `input_match: '"skill"\s*:\s*"(?:[\w-]+:)?<skill>"'` | EVL-16 corrected |
| Near-miss negative from the sibling family | `tool_used Skill` with `min: 0, max: 0, arm: both` | EVL-15 |
| Output contract | regex over the written file (`{source: file}`) + `file_exists`. Examples: exactly one `Assumed:` line and no `Reframed:`; `## Sources` grammar via `sources_lint.py` → file → regex (EVL-09); safety banner present and no `prefers-color-scheme:dark`; `min-height:100dvh`; nothing written under `/plugins/cache/` | EVL-09, EVL-11, EVL-13 |
| Process | `tool_order` for verify-before-delete (empty-vault), survey-before-ingest (ingest-article), preflight-before-sync (sync-vault) | EVL-10, R22 |
| Gates (intent-lock, decision-interview, plan-critique, empty-vault) | A pressure scenario (hurry + authority + sunk cost) **plus the fallback**. Eval runs grant only read-only tools, so AskUserQuestion is absent and the case exercises exactly the path that is broken today (H02). | COM-28 corrected, EVL-22, R80 |
| MCP-dependent (evidence) | mocks with fixed PMIDs/NCTs. `expect:` asserts `datetype: edat` and `retstart` for lit-watch (H46, H47) and aborts on violation. | EVL-24, R75 |
| Post-delivery (misread-capture) | `context.history_file` | EVL-23 |

- At least 3 cases per skill (R71). Safety graders carry the dominant `weight` (R73).
- `llm` graders only for short outputs, with concrete PASS/FAIL rubrics (EVL-11).
- The 118 existing cases are **mined**: only the skeleton converts (`name` → case dir, `prompt` → body, `expected_output` → `expected_outcome`), graders are hand-written, and the target is 3–5 cases per skill (EVL-04 corrected, EVL-05).

### 6.3 Trigger evals (two runners, two questions: R78)

1. **Isolated** (`claude plugin eval`): can the description win on its own? The positive and negative cases above.
2. **Live** (skill-creator `run_eval` / `run_loop.py`): does it win against the real sibling set? 20 queries per contested family (8–10 should-trigger, 8–10 near-miss), 60/40 train/held-out, 3 runs, 0.5 threshold (EVL-38). Run **in a real multi-repo cloud session**, so the 22 synced skills and the project skills compete (EVL-39). Families:
   - {intent-lock, decision-interview, plan-critique, misread-capture};
   - {pubmed-research-note, comprehensive-review, lit-watch, `anthropic-skills:psych-paper-digest`, `anthropic-skills:deep-research`, `anthropic-skills:daily-random-review`};
   - {clinical-infographic, concept-animation, ml-concept-lab, code-explainer, dataviz};
   - {pdf-pipeline, ingest-article, ingest-slides, atomize-book, `anthropic-skills:pdf`, `anthropic-skills:bullet-reconstruct`};
   - {atomize-book, digest-report, `anthropic-skills:obsidian-knowledge-vault`}.
3. **Live routing smoke** at the W3 and W5 exits: 20 near-miss prompts run with `claude -p` in a multi-repo session with everything delivered, reading which skill fired from the transcript. Acceptance: ≥17/20 correct and **0 destructive misroutes** (risk-first; J2 graft #10).
- **Trigger lock:** `triggers.lock.json` (W0, both repos) records every quoted phrase, including Thai and slash phrases, from every description and `when_to_use`. Dropping one fails validation unless the lock records the removal with a reason.

### 6.4 Regression method

- Baseline = **the old version**, not "no plugin" (EVL-30, COM-30): `git worktree add` of tag `pre-rewrite`, same cases, compare with-arm scores.
- Holistic outputs (reports, the interview) additionally get a blind A/B through skill-creator's comparator (EVL-35).
- Verification always runs in fresh sessions or subagents (SKL-44, EVL-43), across at least two model tiers the owner uses (R79).
- A body move that drops a case score is **reverted**, not fixed forward.

### 6.5 learn-hub project skills

- `learn-hub/scripts/eval-project-skill.sh <skill>` builds a **throwaway plugin** in a temp dir (`.claude-plugin/plugin.json` + `skills/<skill>` copied + `evals/<skill>` copied) and runs `claude plugin eval` on it. The target shape is documented; the skill tree gets no manifest, and multi-repo loading is untouched (J2 graft #9, EVL-46 corrected, R82).
- Skills that need Supabase or `.env.local` get evals for their **decision steps** only: routing, the inbox survey-and-ask, the refusal to run `npm run sync`, the audit refusal in ingest-visual. Their deterministic cores stay under vitest and `unittest`.

### 6.6 CI commands and cost control

| Command | What |
|---|---|
| micky `bash scripts/health.sh [--fast]` | `validate.py --repo .` (includes `claude plugin validate --strict` on the root + each plugin dir); `python3 -m unittest discover -s plugins -p 'test_*.py'`; `node --test plugins/*/scripts/`; `--cross-repo $LEARN_HUB_DIR` when present. `--fast` is the pre-commit subset. |
| micky `bash scripts/eval.sh --smoke <plugin>` | `claude plugin eval plugins/<p> --tag smoke --ablation none --runs 1 --model <pinned> --judge-model <pinned> --no-publish --json <out> --max-cost-usd $EVAL_BUDGET` |
| micky `bash scripts/eval.sh --release <plugin>` | two arms, `--runs 3 --threshold 0.8`, pinned models, `--trust-plugin --no-publish --json`, `--max-cost-usd` (EVL-25) |
| learn-hub `npm test && npm run test:py && npm run check:skills` | vitest (incl. skill-lint, preflight, contract parser); the atomize-book 354 unittests (not run by `npm test` today, EVL-41); `claude plugin validate --strict` on `.claude/skills` and `plugins/learn-hub-session` |

- Cost: a smoke run per touched plugin per wave (free graders only). Release runs at the W3 and W5 exits (OD14).
- Before reading a score drop as a regression, check the error column for rate-limit zeros.
- `evals/results/` is gitignored (EVL-26, EVL-27).
- Precondition: `claude plugin eval` is enabled on the account (W0 check d). If not, the skill-creator runner is the fallback.

---

## 7. Versioning and release

- **Semver lives in plugin.json only** (R83, PLG-06; J1 graft #6).
  - Marketplace entries carry no `version` from W0.
  - The top-level catalog version is deleted.
  - Drift cannot recur: the CLI catches it (LOC-03), and there is nothing left to drift against.
  - Commit-SHA versioning is rejected because `--strict` fails a plugin.json without a version (MP-PLG-1).
- **`release.py <plugin> patch|minor|major`** (W0 as `bump.py`, W3 moved into plugin-creator):
  - dry run by default; `--write` validates first;
  - edits plugin.json (UTF-8, trailing newline) and prepends `## x.y.z — <date>` to the plugin CHANGELOG;
  - prints `claude plugin tag <plugin> --dry-run`.
  - The validator fails when the CHANGELOG's top entry ≠ the plugin.json version (R85). W0 backfills the missing entries (§3.4).
- **In-place loads ignore versions** (PLG-09, R84). Versions are history labels, not update triggers, so bumps may batch at a wave's end.
  - Exception: while Windows still runs a GitHub-sourced install (W0 check g), a fix reaches it only through `release.py` + `claude plugin marketplace update`.
- **Semver meaning:**
  - major = a skill renamed or removed, or an incompatible contract change (lock record, `report/N`, sink payload);
  - minor = a behaviour change (triggers, output, filing) or a new skill or mode;
  - patch = a fix.
- **Renames** (append-only, R87):
  - `intent-lock`, `decision-interview`, `plan-critique` → `alignment`;
  - `pubmed-research-note`, `comprehensive-review`, `psych-paper-digest` → `evidence`;
  - `clinical-infographic`, `concept-animation`, `ml-concept-lab`, `code-explainer` → `visuals`.
  - Many-to-one renames validate (J probe; re-confirmed on the real catalog in W0 check c).
  - Under OD2-a they are a record only (no installs remain to migrate). Under OD2-b they migrate the Windows installs.
- **Tags** (`claude plugin tag`, `{plugin}--v{version}`) are optional. They are required only if OD13-b uploads a portable build, in which case the tag records exactly what was uploaded (PLG-39, PLG-40).
- **learn-hub:** `learn-hub-session` is versioned the same way. Project skills are unversioned (git history is the version; the repo CHANGELOG records changes as today). This closes polish-plan P1-2 (LOC-30).
- **Rollback:** each wave is one branch per repo, merged at wave exit, with tags `pre-rewrite` and `wave-N` in both repos. Rollback = `git revert` of the wave merge + the previous `CLAUDE_CODE_PLUGIN_DIRS` value from `delivery-log.md`.

---

## 8. Validation tooling (what replaces and extends validate.py)

**Where it lives.**
- `plugins/plugin-creator/scripts/validate.py` (W3; W0 fixes the old script in place).
- It is self-contained, so the plugin's skills can call it from anywhere (R44).
- Modes: `--repo <path>` (micky or learn-hub profile, auto-detected by marker), `--cross-repo <path>`, `--versions` (generated table; replaces MEMORY's), `--fix-seams` (none destructive).
- learn-hub runs its own small **vitest skill-lint** (`scripts/lib/skill-lint.mjs`; closes P1-1, LOC-30) for the subset that applies there, so `npm test` never depends on the micky checkout.
- The micky validator's `--repo ../learn-hub` adds the cross-repo checks when both clones are present.

| Check | Rubric | Mode |
|---|---|---|
| `claude plugin validate --strict` on the marketplace root, every `plugins/<p>` in both repos, and learn-hub `.claude/skills` (a root-only run never opens SKILL.md) | R29 | fail |
| Every `json.load` guarded, errors counted; CRLF-safe; `yaml.safe_load` of every frontmatter; frontmatter key whitelist; no leftover `{{` outside `templates/` | R2, R65 | fail |
| Name == dir, 1–64 chars, kebab, no `claude`/`anthropic`; unique across both repos + the committed synced-name list | R1, R7 | fail |
| Description ≤1,024 hard; ≤600 warn; capability → `Use when` → `Not for` order; `Use when` within ~250 chars; no `I/you/your` outside quotes; no `<`/`>`; description + `when_to_use` ≤1,536 | R3–R5 | fail / warn |
| Reciprocal Not-for between declared sibling pairs | R8 | fail |
| **Trigger lock** intact (`triggers.lock.json`) | R78 support | fail |
| Body ≤500 lines and ≤5,000 tok (chars/4); gates ≤2,000 warn; every `references/` / `scripts/` / `assets/` / `examples/` file linked from SKILL.md; every link and `${CLAUDE_*}` path resolves; files >100 lines have `## Contents` | R11, R13, R15 | fail (ratchet) |
| No `${CLAUDE_PLUGIN_ROOT}/..`, no writes targeting `${CLAUDE_PLUGIN_ROOT}`, no `C:\`, `/home/user` or backslash paths in skill text (declared exception: `learn-hub-session/hooks/run.sh`); scripts invoked through an interpreter; no hard-coded `mcp__plugin_` prefix | R32, R44, R46, R47, R49, R41 | fail |
| No `dependencies` anywhere; cross-plugin references marked OPTIONAL with a fallback sentence | R56–R58 (T4) | fail |
| No `commands/`; alias skills must carry dmi and a ≤10-line body; listed side-effect skills (empty-vault, refine-plugin, release) carry dmi; `context: fork` denylist (alignment family) | R34, R35, R37 | fail |
| plugin.json has `$schema`, semver `version`, `author`, `keywords`, no path fields; firecrawl `defaultEnabled: false`; entries have no `version`/`description`; `renames` has no cycles; README + LICENSE + CHANGELOG present; CHANGELOG top == version | R30, R33, R45, R83, R85, R87 | fail |
| Evals: ≥3 cases per skill incl. one trigger positive, one near-miss negative, one output; every case has an outcome grader and a process grader; no `evals.json`; `evals/results/` gitignored; runner present | R70–R72, R76 | fail (ratchet until W3/W4) |
| Mandated-read grep in CLAUDE.md files ("read MEMORY first", "consult ROUTING"); no hand-maintained version tables; always-loaded token budgets | R88, R90, R92 | fail |
| Cross-repo: the vault-keeper sink names inbox paths exactly; the report fixture parses with digest-report's parser; `check-html.mjs` parity fixture verdicts equal `audit:visual` | R59–R62 | fail when both clones are present, else warn |
| Unit tests of every bundled script (unittest, `node --test`, vitest, atomize-book `test:py`) | R68 | fail |
| `metadata.profile` declared; `portable` skills use only the six spec keys and no `!` injection | R54 | fail |

**The ratchet** (`docs/rewrite/ratchet.json`, both repos; W0; J2 graft #3):
- Every new check starts with today's violations listed.
- A listed violation warns and a new one fails.
- A wave must delete the entries it fixes, and the file may only shrink.
- At W5 it must be empty, and the checks become plain failures.
- This lets strict checks land on day one without blocking on known HIGH defects.

**Mechanical enforcement** (R69):
- `.githooks/pre-commit` in both repos runs the fast subset.
- learn-hub's session-start already sets `core.hooksPath`. For micky, plugin-creator's remote-only SessionStart hook does it in cloud; locally it is set once per clone.
- The full `health.sh` / `npm run check:skills` runs at every wave exit.

---

## 9. Context-budget targets

Measured with:
- `claude --plugin-dir <p> plugin details <p>` (PLG-52, LOC-19; this does **not** reflect dmi, RF-A6);
- `/doctor` for listing cost and overflow;
- `/skill-doctor` after 2–4 weeks of use (SKL-08, EVL-40);
- `wc -c` / chars ÷ 4 in the validator.

W0 records the baselines; W3, W4 and W5 re-measure.

| Surface | Now (evidence) | Target | Lever |
|---|---|---|---|
| learn-hub CLAUDE.md: in context from session start in multi-repo sessions (observed) | 268,390 B / 3,126 lines (~67k tok) | **≤32 KB (~8k tok)** with OD11-b; ~40k tok (workflow-first estimate) with OD11-a only | W4 split + gotcha map (R89) |
| micky CLAUDE.md | 13,954 B (~3.5k tok); 69% catalog | ≤5 KB (~1.2k tok; R92 ≤2k) | W3 rewrite |
| micky MEMORY.md (mandated first read) | 108,178 B (~27k tok) | 0 mandated; living section ≤6 KB, read on demand | W3 split (R90) |
| ROUTING.md (mandated per request) | 20,197 B (~5k tok) | 0 (deleted) | W3 (R91) |
| Repo listing entries | 55 authored entries / 33,856 chars; in cloud today only 11 load (8,726 chars) | **≤23 model-invocable entries, ≤10,500 description chars** (avg ≤450); ~15 user-only names at ≈0 description chars | merges; commands → aliases (dmi); forks and source-to-vault gone; maintenance user-only (OD10); ≤600-char soft cap |
| micky always-on (`plugin details` sum) | 6,579 tok (V5, LOC-19) | ≤3,000 tok (≤700 per family plugin) | W3 |
| claude.ai-synced listing | 22 entries / 15,385 chars (P3, V6) | unchanged by this plan; the owner may turn off unused synced skills on claude.ai (project `skillOverrides` is not read in multi-repo sessions) | owner only |
| **Total paid before work, multi-repo cloud** | **≈108k tok** as loaded today (67 + 3.5 + 27 + 5 + 2.2 listing + 3.8 synced); ≈115k if every authored entry loaded | **≈16k tok** (8 + 1.2 + 2.6 listing + 3.8 synced) with OD11-b; ≈48k with OD11-a | |
| Per-description | 8 micky at 1,003–1,022 chars; 3 learn-hub over 1,024 (1,075 / 1,137 / 1,150) | ≤1,024 hard, ≤600 soft; key use case within ~250 chars | W1 (learn-hub over-caps), W3/W4 pass |
| intent-lock on invoke (Step 0 of 5+ skills) | 6.2k body (~8.1k on invoke) | ≤2,000 body + `interview-protocol.md` ≤1,500 at question time | W3 |
| atomize-book body | 1,256 lines / ~21.3k tok | ≤500 lines / ≤5k tok; refs load per step | W4 (H24) |
| ingest-article per run | ~6.7k body + ~12k mandatory refs (~18.7k) | ≤9k after W1; ≤6k mandatory after W4 | conditional refs |
| pubmed-research-note per run | 4.7k body + 5.9k mandatory refs | body ≤4k; mandatory ≤3k | W3 dedupe |
| firecrawl on invoke | ~6.2k (body 4.2k) | body ≤1.5k; vendor reference on demand | W3 split |
| ml-concept-lab full load | ~10.8k | body + mandatory ≤5k | W3 |
| Any SKILL.md | none enforced | ≤500 lines / ≤5k tok hard; standing rules within the first 5k tokens (post-compaction re-attach, SKL-40) | validator |
| Reference files | several >300 lines without a TOC (figures-and-loss 503 lines) | TOC above 100 lines; none >400 lines as a target | W4 |

---

## 10. Migration waves

Dependency graph: **W0 → W1 → W2 → {W3, W4} → W5**. W4 may start at the W2 exit, in parallel with W3, only if the owner wants to. The default is sequential, to respect a single owner's capacity.

**Standard exit gates** (every wave):
- micky `scripts/health.sh` green;
- learn-hub `npm test && npm run test:py && npm run check:skills` green;
- `validate.py --cross-repo` green (from W2);
- smoke evals of every touched skill at or above the `pre-rewrite` baseline;
- the ratchet shrank by the fixed entries;
- the trigger lock is intact;
- a CHANGELOG entry in each touched repo;
- `delivery-log.md` updated;
- **the report → vault → learn-hub pipeline is no worse than at wave entry**;
- the Appendix A rows assigned to the wave are closed in `docs/rewrite/h-coverage.md`.

### W0: Ground truth and safety net (no skill behaviour change)

- **Entry:** both repos clean on the default branch; OD1, OD2 (provisional) and OD14 answered; tag `pre-rewrite` in both repos.
- **Work:**
  1. micky tooling:
     - validate.py crash fix and counted checks (H13), CRLF-safe `yaml.safe_load`, stdio MCP allowed, 200-char floor → no floor.
     - bump.py → plugin.json-only + CHANGELOG + dry run + UTF-8.
     - Strip marketplace entry versions.
     - CLAUDE.md "two files" rule → "plugin.json only".
     - route.py argparse, no versions.
     - `health.sh`, `eval.sh`, `.githooks/pre-commit`.
     - CHANGELOG backfill + first CHANGELOGs.
     - `.gitignore`.
     - README validation command with `--strict`.
  2. Safety nets (both repos): `ratchet.json`, `triggers.lock.json`, `baseline.md` (listing chars, `plugin details`, body sizes), `h-coverage.md` (Appendix A as a checklist).
  3. learn-hub: `skill-lint.mjs` + tests, `npm run test:py`, `eval-project-skill.sh`. Seed smoke suites (3 cases each) for the W1 units: sync-vault, ingest-article, pdf-pipeline, vault-keeper, empty-vault, psych-paper-digest, clinical-infographic.
  4. Cloud environment (owner): the setup script and the env vars `LEARN_HUB_DIR`, `MICKY_TOOLS_DIR`, `PUPPETEER_EXECUTABLE_PATH`, `PUPPETEER_SKIP_DOWNLOAD`, plus the canary `CLAUDE_CODE_PLUGIN_DIRS=/home/user/micky-psych-tools/plugins/gridgeist` (**absolute**, P1).
  5. **Mechanism checklist.** Each item is answered yes or no with evidence, and each "no" has a named fallback:

| # | Check | Fallback on "no" |
|---|---|---|
| a | A new platform-started multi-repo session shows `gridgeist@inline` loaded | Stop all cloud-delivery steps; re-ask OD1 (claude.ai sync) before W1 exit |
| b | A probe plugin's SessionStart + PreToolUse hooks fire in a platform-started multi-repo session (pre-probed in `claude -p` from `/home/user`, P2) | No hooks plugin: SessionStart duties via setup script + env vars + preflight refusal text; safety is already mechanical in the preflight |
| c | Many-to-one `renames` validates on a scratch copy of the real catalog (J probe OK on a toy) | Omit `renames` (the env-var route needs none); record the mapping in README |
| d | `claude plugin eval` is enabled on the account; an http-server mock answers | skill-creator runner for behavioural cases; static + unit layers unchanged |
| e | learn-hub `.claude/skills` load eagerly (observed) and nested `.claude/rules` with `paths:` load in multi-repo sessions (U4) | App gotchas go to `docs/gotchas/*.md` with a pointer index in CLAUDE.md |
| f | `/doctor` listing cost and overflow in a multi-repo session; `/skill-doctor` locally | Record only; it sets the W3/W4 description budget |
| g | Windows: `claude --version` ≥ 2.1.280; `claude plugin marketplace list` (micky source type; is learn-hub-local installed?); a user env var loads a canary | Stay on the marketplace install (OD2-b); GitHub source → switch it to a local directory |
| h | Whether the setup script runs before the clone (U2) | Design already assumes it does; nothing repo-dependent in it |

- **Exit:**
  - health green on untouched content (new checks fail only on new violations; existing ones are ratcheted);
  - smoke suites run end to end;
  - checklist a–h answered;
  - baselines recorded.
  - **If (a) fails, W1 cloud steps are skipped and OD1 is re-asked.**
- **Rollback:** revert the W0 merges; unset the env vars (delivery log). Only tooling and data files changed.

### W1: Stop active harm in units that load today (current names and layout)

- **Entry:** W0 exit.
- **Work, learn-hub first (consumer side):**
  1. `sync-vault` rewrite + `sync-preflight.mjs` + `npm run sync:preflight`; PreToolUse gate hooks removed; `session-start.sh` root resolution + done-marker; `ready.mjs` (H34, H35).
  2. `ingest-article` (H25, H26).
  3. `pdf-pipeline` (H32, H33).
  4. `ingest-slides` (H27, H28).
  5. `atomize-book` content fixes (H21, H22, H23).
  6. `ingest-infographic` (H30 + YAML); `ingest-animation` YAML; learn-hub CA YAML (H43).
  7. `vault-coverage` `BOOK_ROOT`.
  8. Retire `source-to-vault` (H17–H20).
  9. CLAUDE.md factual corrections.
- **Work, micky:**
  1. `vault-keeper` `sink.py` resolver + `vault/.vault-id` (H08, H09).
  2. `empty-vault` stopgap: dmi, new detection, assets held (H10 detection, H11 hold).
  3. `plugin-creator` root guard (H07).
  4. `psych-paper-digest` search fixes (H46, H47).
  5. `clinical-infographic` light-lock + strip + contrast (H36, H37).
  6. `firecrawl` refresh (H12).
  7. `code-explainer` pointers at SKILL.md:30/:99 + README:86-87 (H42).
  8. Release the touched plugins.
- **Cloud:** after smoke passes, add vault-keeper, firecrawl, plugin-creator (§2.7).
- **Exit (plus the standard gates):**
  - A bare ingest-article → survey + question, no deletion.
  - sync-vault chooses preflight + background `sync:apply`.
  - vault-keeper from a learn-hub cwd → marker mismatch → asks.
  - The CI template and example pass learn-hub `auditInfographicResponsive`; a grep for `prefers-color-scheme:dark` is empty.
  - **One owner-approved live sync** of a trivial vault edit in a multi-repo cloud session, through the preflight, confirming `count(*) where diagrams <> '{}'` did not drop.
  - Assets are now held rather than deleted.
- **Rollback:** revert the per-repo W1 merge (restores the settings.json gates and the old skills); restore the env var from the log.

### W2: Reconnect the cross-repo pipeline (consumers → producers)

- **Entry:** W1 exit; OD4 and OD5 answered.
- **Work (each step its own commit, in order):**
  1. **learn-hub consumers:**
     - `inbox-contract.md`;
     - `digest-report` → `.claude/skills` with the tolerant reader + intake log + survey-then-stop (H15, H16);
     - `ingest-visual` = merge of ingest-infographic + ingest-animation, with `npm run audit:visual` refuse-and-return (H29, H31);
     - vault-atomizer, vault-vectors, pk-plasma-animation → `.claude/skills` user-only (pk-plasma drops its `.mcp.json`);
     - `check-repetition` Not-for + user-only;
     - `plugins/learn-hub-session`;
     - `check-contract.mjs`.
  2. **micky producers (interim, in current plugin dirs):**
     - the report contract in pubmed-research-note references; CR's copy aligned (deleted in W3);
     - the single `Assumed:` line (H05, H44);
     - the §4.2 fallback sentence in every caller;
     - runtime MCP resolution;
     - the sink via vault-keeper; publish word "digest"; `contract: report/1`.
  3. **micky renderers:**
     - concept-animation absorbs the learn-hub copy's grammar + five-viewport verify (H38, H39);
     - ml-concept-lab (H40, H41);
     - clinical-infographic filing via the sink;
     - `check-html.mjs` fallback port + parity fixture.
  4. **vault-keeper:** the sink routes to the inbox; empty-vault becomes a transfer with `drain_plan.py` (H10, H11 closed).
  5. **Retire the forks:**
     - Merge the learn-hub intent-lock fork's ledger entries into micky's ledger (H06).
     - Delete the pubmed and CR forks (H48, H49) and the `learn-hub-local` catalog (H14). Run `claude plugin marketplace remove learn-hub-local` first on Windows if W0-g found it.
  6. **Cloud:**
     - Add the research-writer and renderer paths.
     - **Atomic swap for concept-animation.** Confirm micky CA loads in a **branch session** of learn-hub without the copy, then merge the copy's deletion.
     - Add the folder `/home/user/learn-hub/plugins`, which by now contains only `learn-hub-session` (V2).
- **Exit (plus the standard gates):**
  - The parity fixture agrees; the micky CA and ML examples pass `auditAnimationLayout` with `[]`.
  - **Rehearsal:** a fixture report in the micky vault → `/empty-vault` transfer → inbox → "digest" (one owner-approved real report) → sync → provenance count matches.
  - A report written in a multi-repo session lands in `research-notes/` and is **not** digested without "digest".
  - One unattended `daily-random-review` run completes with micky CR loaded (via the fallback, or after the OD8 edit).
  - `claude plugin list` shows each plugin **once**; `/doctor` shows no overflow.
- **Rollback:** revert the W2 merges (the forks come back from the tag); restore the env var. The inbox is git-tracked, so no report is lost.

### W3: micky consolidation and rewrites (eval-driven)

- **Entry:** W2 exit; OD3, OD6, OD7, OD9, OD10, OD12 answered.
- **Work:**
  1. **Delivery switch.** Replace the micky per-plugin paths with the folder `/home/user/micky-psych-tools/plugins` (§2.7). Windows moves to OD2's route (under OD2-a: set the env var, then uninstall the marketplace copies).
  2. **Skeleton, moved unchanged in one reversible PR:**
     - `alignment`, `evidence` (+ `lit-watch` rename, `state/lit-watch/`), `visuals`;
     - one `.mcp.json`; `renames`;
     - commands deleted → alias skills (dmi) + `argument-hint`;
     - misread ledger → `state/misreads.md` (location half of H03).
  3. **alignment:** `interview-protocol.md`, `lock-record.md`; intent-lock by subtraction (H01, H02); misread-capture + `ledger.py` (H03, H04); decision-interview and plan-critique light rewrites.
  4. **evidence:** `report-contract.md` dedup (CR's copy deleted), `engines.md`; decision-brief 6-slot fix (H45); pubmed dedupe; CR fixes; `sweep.py`, `sources_lint.py`, mocks; Not-for vs the synced digests.
  5. **visuals:** `html-artifact-contract.md` once; `render-verify.md`; code-explainer fidelity script and naming; ML trim; CI `lessons-learned` → CHANGELOG.
  6. `firecrawl` split (OD12); gridgeist `UPSTREAM.md`; `plugin-creator` self-contained (`validate.py`, `release.py` moved; scaffold; template); refine-plugin dmi.
  7. **Description pass** for every micky skill (R3–R5, reciprocal Not-for, synced collisions, trigger lock intact), with live trigger evals before and after (§6.3).
  8. **micky context diet:** CLAUDE.md ≤5 KB without mandates; ROUTING.md, route.py and `/route` deleted; MEMORY split; `validate.py --versions`.
  9. Eval conversion per family (3–5 cases per skill) + old-vs-new A/B.
  - Order: alignment first, because evidence and visuals depend on the lock record.
- **Exit (plus the standard gates):**
  - a release eval run (two arms) per family at or above the `pre-rewrite` baseline;
  - the **live routing smoke**: ≥17/20 and 0 destructive misroutes;
  - `/doctor` shows no overflow; micky always-on ≤3,000 tok;
  - no `commands/` directory remains;
  - every Appendix A row assigned to W≤3 is closed.
- **Rollback:**
  - Family PRs are separate, so revert per family.
  - The folder path absorbs layout reverts with no env edit.
  - Windows under OD2-a: the same.
  - Windows under OD2-b: `claude plugin marketplace update` (renames migrate).

### W4: learn-hub consolidation and context diet

- **Entry:** W2 exit (W3 not required); OD11 answered; **a freeze window agreed for atomize-book imports** (LOC-46: the most-churned skill).
- **Work:**
  1. CLAUDE.md stage (a): pipeline gotchas → owning skill `references/gotchas.md` **verbatim**; vault format → `docs/vault-format.md`; pointers left; `gotcha-map.md` (all 136 headings) + `gotchas-archive.md`.
  2. Stage (b) per OD11: app gotchas + Pages → `.claude/rules/*.md` (or `docs/gotchas/` if W0-e was "no").
  3. atomize-book split (H24), verbatim, "Read X before step N".
  4. ingest-article conditional references (≤6k mandatory).
  5. verify scripts bundled.
  6. pdf-pipeline `classify_pdf.py`.
  7. sync-vault receives its operational gotchas.
  8. learn-hub description pass + trigger evals (PDF front door, atomize family).
  9. Project-skill eval cases via the wrapper.
- **Exit (plus the standard gates):**
  - learn-hub CLAUDE.md ≤32 KB (OD11-b).
  - A grep shows every mapped heading exists **exactly once** in its destination.
  - The atomize-book unittests are green.
  - **One book chapter and one article are re-run end to end** with no regression in the loss, depth or figure gates.
- **Rollback:** revert; `gotchas-archive.md` still holds the old text verbatim.

### W5: Hardening, telemetry, deferred decisions

- **Entry:** W3 and W4 exit.
- **Work:**
  - a full release eval pass in both repos;
  - the live routing smoke with everything loaded;
  - after 2–4 weeks of use, `/skill-doctor` + `/doctor` → decide user-only or retire (gridgeist, lit-watch);
  - revisit OD4 (retire the micky vault after one final transfer if the owner now chooses "staging");
  - OD13-b portable build if wanted (tag + upload);
  - empty the ratchet;
  - update MEMORY's living section with the final numbers.
- **Exit:**
  - the ratchet file is empty and its checks fail hard;
  - every §9 target is met or has a recorded reason;
  - the decision log is updated.
- **Rollback:** not applicable (decisions and measurements only).

---

## 11. Owner decisions

Each decision states the option the architecture **assumes**, and what changes if the owner picks differently.

| # | Question | Options | Recommendation (assumed) | Trade-off | If the owner picks differently |
|---|---|---|---|---|---|
| OD1 | How do repo plugins reach **cloud** sessions? | (a) `CLAUDE_CODE_PLUGIN_DIRS` on the cloud environment(s), absolute paths, in place; (b) claude.ai-synced uploads; (c) none | **(a)**, if the W0 canary passes | (a): no copies, always the checked-out branch (a branch session tests a rewrite for free), one env edit per §2.7 row per environment. A session that doesn't clone micky has no micky tools. (b): works without the clone and in Cowork, but every change is a re-upload (fork drift again); `state/` and vault-in-git break. (c): the main surface stays empty. | (b): add tags + an upload step to `release.py`; skills get `portable`/`cc` profiles; `state/` and the sink move to userConfig paths per machine (ledger stops compounding in cloud); `learn-hub-session` cannot ship that way, so the §10 W0-b fallback applies. (c): W2's cloud rehearsal moves to Windows. |
| OD2 | How do plugins load on **Windows**? | (a) user env var `CLAUDE_CODE_PLUGIN_DIRS` (`;`), marketplace copies uninstalled at W3 entry; (b) local-directory marketplaces (in place), learn-hub keeping a one-entry catalog for `learn-hub-session` | **(a)** | (a): one mechanism and one delivery log for both surfaces; no install state; needs CLI ≥2.1.280 (W0-g). (b): keeps the `/plugin` UI, per-plugin enable/disable and userConfig prompts; `renames` migrate installs; learn-hub needs a registered catalog again (with a top-level description to pass `--strict`). | (b): learn-hub keeps `.claude-plugin/marketplace.json` listing only `learn-hub-session`; W3 relies on `renames` + `marketplace update`; userConfig becomes the primary root source on Windows (env var second). |
| OD3 | Merge micky plugins into **families** (alignment, evidence, visuals)? | (a) merge in W3 (skill names unchanged; plugin names change; `renames`); (b) keep all 14 plugin shells | **(a)** | (a): one copy of each contract, one `.mcp.json`, no copy machinery; plugin names in `/plugin` and namespaced forms change (`/evidence:pubmed-research-note`; the bare `/pubmed-research-note` still works, PLG-17). (b): zero rename churn, but shared text needs generated copies + `sync_shared.py` + parity, and three `.mcp.json` stay. | (b): add `shared/` canonical files + `sync_shared.py --check` to the validator (risk-first §5); `renames` and the W3 skeleton step drop out; the §9 always-on target rises to ≤5,000 tok. |
| OD4 | Role of the **micky `vault/`** | (a) keep as the fallback sink + transfer source (vault-keeper stays); (b) staging only: one final transfer, then retire vault-keeper, empty-vault and `vault/` | **(a) now; revisit at W5** with usage data (J2 graft #12) | (a): outputs of sessions without learn-hub land somewhere durable (git-tracked, commit offer); keeps the Obsidian-browsable store; one extra skill pair. (b): simplest; one store; but outputs without learn-hub fall back to cwd, which is lost in an ephemeral VM unless committed (J1 fatal flaw). | (b): the W5 transfer drains `vault/` into the inbox; `sink.py` shrinks into a 10-line step inside each producer family (inbox or cwd); `vault-keeper` gets `renames: null`; §9 always-on falls by ~0.8k tok. |
| OD5 | After a report is written, what happens by default? | (a) inbox only; publish on "digest"/"publish"; (b) digest + sync to live Supabase by default | **(a)** | (a): live-DB writes stay deliberate (the project is shared with board-prep-hub) and match digest-report's own contract; costs one word. (b): one step shorter; production writes on every review (H49). | (b): producers call digest-report + sync-vault after writing (a REQUIRED-with-stop handoff); the W2 exit test inverts; the rehearsal writes to Supabase every time. |
| OD6 | Where does **compounding personal state** live (misread ledger, lit-watch config, `last_swept`, digests)? | (a) git-tracked `micky/state/` (private repo), commit offered after each write; (b) `${CLAUDE_PLUGIN_DATA}` per machine; (c) a private path outside both repos, per machine | **(a)** | (a): the only option that compounds across Windows and cloud; priors sit in git history; each capture is a small commit. (b): private and simple, but resets in every cloud VM. (c): private, but no cloud. | (b)/(c): `ledger.py` and `sweep.py` read a userConfig/env path; cloud sessions start fresh each time (document it in README); the validator's "no writes under `${CLAUDE_PLUGIN_ROOT}`" rule is unchanged. |
| OD7 | The two **`psych-paper-digest`** skills | (a) rename the micky skill `lit-watch` (+ `/digest` alias); (b) rename the claude.ai skill (e.g. `daily-psych-digest`); (c) keep both names, sharpen the Not-for clauses | **(a)** | (a): removes the collision at once (SKL-55); the synced skill keeps bare `/psych-paper-digest`. (b): no plugin change, but breaks any routine that names the synced skill. (c): two overlapping descriptions compete for "what's new". | (b): the micky skill keeps its name inside `evidence`; an owner edit on claude.ai; routines checked. (c): trigger-eval acceptance for that family is relaxed to "no destructive misroute". |
| OD8 | `daily-random-review` "chains into" comprehensive-review (textbook, zero citations, Obsidian board vault) | (a) the owner edits the synced skill to "follow the structure below", and CR gains a Not-for; (b) allow CR as an optional evidence update inside board-prep | **(a)** | Opposite evidence bases and stores (V8). Only the owner can edit a synced skill (SKL-55; skills.md). | (b): CR gains a "board-prep mode" (textbook-sourced, no Sources block, writes nothing to the inbox), with its own eval; the W2 unattended-run test asserts that mode. |
| OD9 | **Slash names** after commands go | (a) keep short verbs as dmi **alias skills** (`/digest`, `/animate`, `/infographic`, `/visualize`, `/explain-code`, `/critique-plan`, `/resolve-decisions`, `/new-plugin`, learn-hub `/vectors`, `/pk-animation`); drop `/atomize` (collides) and `/ingest` (retired hazard); (b) capability names only; (c) rename skills to the verbs | **(a)** (J2 graft #11) | (a): habits survive at zero listing cost (SKL-36), at the price of ~10 extra `/` menu entries. (b): leanest menu; muscle memory breaks. (c): less descriptive skill names in the listing and in grader regexes. | (b): delete the alias skills and add a README migration table. (c): rename skills, update evals and the trigger lock, and add `renames` notes. |
| OD10 | **User-only** maintenance skills | (a) mixed: producers and gates model-invocable; vault-atomizer, vault-vectors, vault-coverage, check-repetition, pk-plasma-animation, refine-plugin, empty-vault user-only; gridgeist and lit-watch decided at W5 by usage; (b) everything model-invocable | **(a)** | (a): saves listing budget and stops accidental runs; "check coverage of X" no longer auto-routes (type `/vault-coverage`). (b): natural-language routing for everything; ~3–4k more listing chars; overflow risk (SKL-08). | (b): remove dmi from those skills, add them to the live trigger families, raise the listing target to ≤14,000 chars. |
| OD11 | How deep does the learn-hub **CLAUDE.md** restructure go? | (a) only skill-owned material (58 pipeline gotchas, vault format); (b) also app gotchas + Pages into path-scoped `.claude/rules/` | **(b), staged** (a first, then b, in W4) | (a): little risk to the file maintained daily, but ~40k tok stay always loaded. (b): reaches ~8k tok but reorganizes that file; depends on W0-e. | (a): W4 stops after stage (a); the §9 total becomes ≈48k; `.claude/rules/` is not created. |
| OD12 | **firecrawl** as a marketplace plugin | (a) keep a slim router (≤1.5k tok) + a dated vendor reference; `defaultEnabled: false`; (b) retire it, keeping only the fetch contract in `evidence/engines.md` and using the vendor's own skill/CLI | **(a)** (2 of 3 proposals; lower risk) | (a): one entry point the owner controls; vendor text must be re-fetched when stale. (b): staleness ends for good, but general-web requests depend on the vendor's distribution reaching each environment, and its install adds a same-named `firecrawl` skill (INV firecrawl-2). | (b): `renames: {firecrawl: null}`; the setup script still installs the CLI; the evidence engines doc carries the fetch recipe. |
| OD13 | Any of these tools on **claude.ai** (phone, Cowork, routines without clones)? | (a) none for now; (b) a portable build of selected skills (e.g. pubmed-research-note) uploaded as synced plugins | **(a)** | (b): phone/Cowork access, but each upload is a copy needing tags, the six-key limit (SKL-04), no `!` injection, and unverified upload mechanics (U6). | (b): those skills get `metadata.profile: portable` and stricter validation (R54); `release.py` tags + uploads; the in-place copy wins in Code sessions (RF-A5). |
| OD14 | **Eval spend** | (a) smoke per wave (free graders, 1 run, `--ablation none`, `--max-cost-usd` set by the owner) + two-arm release runs at the W3 and W5 exits; (b) smoke only; (c) full two-arm every wave | **(a)** | A full two-arm pass over ~23 skills × 5 cases × 3 runs is ~700 agent runs (EVL-27). (a) buys regression detection at the riskiest points. (b) cannot show that a rewrite didn't regress holistic quality. | (b): A/B for holistic skills becomes owner review of two outputs. (c): add `--release` to every wave exit and raise the budget. |

---

## 12. Risks and mitigations

| # | Risk | Likelihood / impact | Mitigation |
|---|---|---|---|
| K1 | `CLAUDE_CODE_PLUGIN_DIRS` does not load in platform-started sessions; a path is written with `~` (resolves to `/root`, P1); clone paths differ; the CLI is older than 2.1.280 | medium / high | W0-a canary; **absolute paths only** (validator lints the delivery log); `× Path not found` lines are read at every exit (they print; exit 0); the session-start ready line prints `claude --version` + loaded plugins; OD1-b fallback |
| K2 | Listing overflow once ~23 repo skills join 22 synced ones; the least-invoked lose their descriptions (SKL-08) | medium / high | per-wave enablement; aliases and maintenance skills are dmi; ≤600-char soft cap; `/doctor` at every exit; the owner may disable unused synced skills |
| K3 | Multi-repo sessions skip project hooks: no Chromium or `.env.local` → the diagrams-wipe precondition; silent gates | high today / high | **mechanical**: preflight readiness refusal + gates inside `apply-sync.mjs` (W1); hooks plugin (W2) for convenience; the W1 exit live sync checks the `diagrams` count |
| K4 | MCP endpoint dedup changes the callable prefix once plugins load | high if unfixed / medium | runtime resolution (W2) lands **before** research writers join the cloud path |
| K5 | Same-named units load twice (V2): forks, the CA copy, Windows marketplace copies next to env-var paths | medium / medium | forks deleted before `learn-hub/plugins` joins; CA atomic swap verified in a branch session; Windows copies uninstalled at the W3 switch; exit gate "each plugin listed once" |
| K6 | `daily-random-review` unattended runs hit CR's Step 0 and the sink once CR loads in cloud | medium / medium | §4.2 fallback; OD8 edit; the W2 exit runs one unattended pass |
| K7 | Description edits drop a Thai or slash trigger, or shift routing between siblings | medium / high | trigger lock; near-miss negatives; old-vs-new comparison; live routing smoke (W3, W5) |
| K8 | Cross-repo contract drift returns | medium / medium | one owner per interface; tolerant reader; `contract: report/N`; the `check-contract.mjs` + parity fixture in `validate.py --cross-repo` |
| K9 | In-place loading means uncommitted edits or a broken branch are live behaviour | medium / medium | rewrites on branches; the owner's default checkout stays on master; pre-commit validation; a branch session is the test harness |
| K10 | `claude plugin eval` unavailable (early access), noisy judges, rate-limit zeros, mocks diverging from real PubMed | medium / low | W0-d; regex/tool graders first; pinned models; error-column check; owner-approved live runs for research skills at the W2 rehearsal |
| K11 | Knowledge loss when 3,126 CLAUDE.md lines and 1,256 atomize-book lines are redistributed (the repo's own lesson: a worklist from one pattern inherits its blind spots) | medium / high | verbatim moves only; `gotcha-map.md` covering all 136 headings; `gotchas-archive.md`; an exactly-once grep; a re-run of one chapter + one article |
| K12 | atomize-book churn collides with W4 (LOC-46) | medium / medium | freeze window; per-file PRs; 354 unittests as the guard; scripts not moved |
| K13 | Personal data in git (ledger) and personal context (e.g. "Klaeng") in distributable text | low (private repo) / low | OD6; personal context removed from skills in W3 |
| K14 | Windows specifics: CRLF frontmatter, backslash paths, PowerShell-only checks | medium / medium | CRLF-safe validator; path lint; process checks rewritten portably (INV digest-report-8) |
| K15 | PDF tooling absent in cloud | high today / medium | setup script (W0) + `ready.mjs` Step 0 naming the install command (R51) |
| K16 | Scope creep: a "light" edit turns into re-voicing | medium / medium | each wave's diff is reviewed against §3; a change outside it needs a named defect or a failing eval |
| K17 | Plugin hooks do not fire in platform-started multi-repo sessions (U1; pre-probed P2) | low / low | safety does not depend on them (K3); W0-b fallback |
| K18 | The W3 skeleton PR (moves + renames + command removal) is large | medium / medium | move-unchanged only (no rewrites in that PR); one revert restores it; the folder path means no env edits on revert |

---

## 13. Explicit non-goals

- **No monorepo.** The two repos stay separate, joined by four named interfaces (§4.3). Merging micky into learn-hub would couple the portable marketplace to a deployed app and its CLAUDE.md.
- **No re-voicing** of skill bodies that have no defect. Style churn invalidates the owner's mental model without fixing anything (COM-21).
- **atomize-book's Python is not relocated** (purist's `tools/source/` move is rejected). It gains `npm run test:py` and npm aliases only.
- **No `plugin.json` `dependencies`, no symlinks, no shared third repo, no `sync_shared.py`** (unless OD3-b).
- **No router of any kind.** ROUTING.md and `/route` are deleted, not replaced.
- **No custom eval runner.** `claude plugin eval` and skill-creator only. There are no committed `evals.json`.
- **No change to gridgeist content** and no edits to vendored text beyond a dated refresh.
- **No commit-SHA versioning** and no version in marketplace entries.
- **No edits to claude.ai-synced skills by the agent.** Only the owner can edit them (OD7-b, OD8).
- **No app-code changes** beyond:
  - the sync preflight;
  - `ready.mjs`;
  - the `audit:visual` CLI;
  - `check-contract.mjs`;
  - `skill-lint.mjs`;
  - the eval wrapper;
  - the npm script aliases.
  - Product features, schema and Supabase migrations are out of scope.
- **No portable claude.ai builds** unless OD13-b.
- **No merges beyond the three families plus ingest-visual.** The purist's `vault-audit` merge and its `ingest-slides → ingest-article` merge are rejected (trigger breadth, SKL-56; churn in the most-churned area).
- **No automatic Supabase publishing** from any producer (OD5-a).
- **No retirement of the micky vault** before the W5 decision point (OD4).

---

## Appendix A: HIGH-defect coverage map (H01–H49)

Numbering follows the inventories' order: alignment, infra, learn-hub plugins, learn-hub project skills, renderers, research writers. J1 verified all 49. This table is the W0 checklist `docs/rewrite/h-coverage.md`.

| H | Inventory id | Defect (short) | Evidence | Fix | Wave |
|---|---|---|---|---|---|
| H01 | intent-lock-1 | silent contract contradicted in 11 places | SKILL.md:16,22 vs :49,:67,:93,:155,:166-167,:193,:196,:206 | delete the lines (subtraction); no reinterpret patch | W3 |
| H02 | intent-lock-2 | picker contract not executable in CC; no fallback | :136, :160-162, :189-190 | AskUserQuestion mechanics + fallback (`interview-protocol.md`) | W3 |
| H03 | intent-lock-3 | ledger in the plugin tree cannot compound | misread-capture SKILL.md:39 | `state/misreads.md` via `ledger.py` + commit offer | W3 |
| H04 | intent-lock-4 | `Prior:` has no eliciting question | misread-capture :26, :30-35, :47, :55 | Q2 elicits the check | W3 |
| H05 | intent-lock-5 | callers expect Reframed/Skipped | intent-lock:226 vs pubmed:263-265, CR:147-148 | single `Assumed:` line; `lock-record.md` | W2 |
| H06 | intent-lock (learn-hub clone)-1 | fork splits the ledger | two `misreads.md` | merge entries, delete fork | W2 |
| H07 | plugin-creator-1 | repo-bound, no precondition | SKILL.md:9-10 | W1 marker guard; W3 scripts inside the plugin | W1/W3 |
| H08 | vault-keeper-1 | `${CLAUDE_PLUGIN_ROOT}/../../vault` wrong in cache | SKILL.md:29 | `sink.py` resolver + `.vault-id` | W1 |
| H09 | vault-keeper-2 | walk-up matches learn-hub | SKILL.md:28 | marker-validated env/userConfig; ask | W1 |
| H10 | vault-keeper-3 | stale learn-hub marker in empty-vault | SKILL.md:36-37 | W1 env → marker → ask; W2 transfer | W1/W2 |
| H11 | vault-keeper-4 | empty-vault deletes assets that have receivers | SKILL.md:54-57 | W1 hold; W2 transfer + intake log | W1/W2 |
| H12 | firecrawl-1 | stale "verbatim" vendor guide | SKILL.md:146-147, :127, :330 | refresh + dated stamp; W3 split | W1 |
| H13 | validate.py-1 | tracebacks; uncounted PASS | validate.py:72-73, :111-114 | guarded loads, counted checks | W0 |
| H14 | learn-hub-local-1 | catalog never registered | settings.json hooks only | plugins → project skills; catalog deleted | W2 |
| H15 | digest-report-1 | input contract vs `## Sources` producers | SKILL.md:88-90 vs pubmed SKILL.md:211 | tolerant reader | W2 |
| H16 | digest-report-2 | not loaded anywhere | plugin not enabled; `.claude/skills` copy deleted | back to `.claude/skills` | W2 |
| H17 | source-to-vault-1 | prod rows without vault files | SKILL.md:8-10, :140-141 | retire | W1 |
| H18 | source-to-vault-2 | no-arg batch ingest of `Book/` | SKILL.md:27-28, :128-129 | retire | W1 |
| H19 | source-to-vault-3 | routing collision, no negative scope | SKILL.md:3 | retire | W1 |
| H20 | source-to-vault-4 | omits embedding/diagrams/images | SKILL.md:116 | retire | W1 |
| H21 | atomize-book-1 | `[[topic-id]]` contradiction | :295-296 vs :1027-1029, :1063-1067 | one chapter-reference rule | W1 |
| H22 | atomize-book-2 | stale sync economics | :1116-1117, :1265-1267 | background `sync:apply` via sync-vault | W1 |
| H23 | atomize-book-3 | 4 drafting rules missing | 0 grep hits (CLAUDE.md:2489, :2511, :1325) | add to the drafting spec + note-format | W1 |
| H24 | atomize-book-4 | ~21.3k-token body | 1,256 lines | verbatim split to references | W4 |
| H25 | ingest-article-1 | Windows inbox; bare invocation deletes; not ignored | SKILL.md:3, :49, :51, :348 | survey-and-ask; `ARTICLE_INBOX_DIR`; gitignore | W1 |
| H26 | ingest-article-2 | source-cover command cannot run | figures-and-loss.md:455-458 vs measure-source-cover.mjs:70 | correct invocation or drop | W1 |
| H27 | ingest-slides-1 | wrong script paths | SKILL.md:62, :71 | `${CLAUDE_SKILL_DIR}` | W1 |
| H28 | ingest-slides-2 | routing conflict with pdf-pipeline | pdf-pipeline SKILL.md:98 | pdf-pipeline routes decks to ingest-slides | W1 |
| H29 | ingest-infographic-1 | dead empty-vault contract | SKILL.md:3, :137-138 | inbox + intake log (ingest-visual) | W2 |
| H30 | ingest-infographic-2 | "targeted upsert == npm run sync" | SKILL.md:116-118 | delegate to sync-vault | W1 |
| H31 | ingest-animation-1 | dead empty-vault contract | SKILL.md:3, :123-125 | inbox + intake log (ingest-visual) | W2 |
| H32 | pdf-pipeline-1 | slides → atomize-book | SKILL.md:98; routing.md:42, :60 | route to ingest-slides | W1 |
| H33 | pdf-pipeline-2 | impossible apply rule | SKILL.md:138-141 vs :150 | `sync:apply` via sync-vault | W1 |
| H34 | sync-vault-1 | recommends nested layout | SKILL.md:126-132 | flat layout | W1 |
| H35 | sync-vault-2 | default `npm run sync` path; no traps | SKILL.md:32-34, :65-72 | preflight + background `sync:apply` | W1 |
| H36 | clinical-infographic-1 | dark block in template + example | template:100-104; example:167 | light-lock | W1 |
| H37 | clinical-infographic-2 | `.mech` cramps on phones | template:74-75, :93 | mobile stacking | W1 |
| H38 | concept-animation-1 | stage-collapse layout rule | animation-grammar.md:46, :48 | port learn-hub grammar | W2 |
| H39 | concept-animation-2 | single-viewport fit check | SKILL.md:145-150 | five viewports via `audit:visual` | W2 |
| H40 | ml-concept-lab-1 | stage-collapse layout rule | build-contract.md:140-141 | same port | W2 |
| H41 | ml-concept-lab-2 | verify recipe fails (ESM playwright) | build-contract.md:195-197, :202 | `audit:visual` / `check-html.mjs` | W2 |
| H42 | code-explainer-1 | template never existed | **SKILL.md:30, :99**; README.md:86-87 | remove pointers; dead-link rule | W1 |
| H43 | concept-animation (learn-hub copy)-1 | invalid strict YAML | SKILL.md:3 | folded `>-` (then retired in W2) | W1 |
| H44 | pubmed-research-note-1 | Reframed preface stale | SKILL.md:263; pairing:86-90 | single `Assumed:` line | W2 |
| H45 | pubmed-research-note-2 | decision-brief slot arithmetic (4 + 3 over 6 headings) | decision-brief.md:11-12 (headings at L16, 31, 50, 71, 78, 90); intent-lock-pairing.md:49-57 | interview fixes slots 1, 2, 6 (scope boundary rides in the lock record); skill derives 3–5; pairing aligned | W3 |
| H46 | psych-paper-digest-1 | pdat vs edat | sweep-recipes.md:39-40 | `datetype: edat` | W1 |
| H47 | psych-paper-digest-2 | silent truncation at 50 | :39-40 vs :92-93 | `retstart` pagination + counted cap | W1 |
| H48 | pubmed-research-note (learn-hub fork)-1 | evals fail by construction | evals.json:56, :128 | retire fork | W2 |
| H49 | comprehensive-review (learn-hub fork)-1 | default digest + live sync | SKILL.md:166-176 | retire fork; publish opt-in (OD5) | W2 |

Per wave: W0 closes 1 (H13); W1 closes 26 (+ H10 and H11 partly); W2 closes 16; W3 closes 5 (+ H07 root cause); W4 closes 1. Total **49**.

---

## Appendix B: Corrections applied to the proposals (judge findings re-checked)

| # | Source | Error | Checked against | Corrected statement used here |
|---|---|---|---|---|
| B1 | purist §2.5 | `CLAUDE_CODE_PLUGIN_DIRS=~/micky-psych-tools/plugins` | **P1** (`HOME=/root`; the probe printed `inline[0]: × Path not found: /root/micky-psych-tools/plugins`, exit 0, and the other path loaded) | Absolute `/home/user/micky-psych-tools/plugins` (§2.5, §2.6); validator lint |
| B2 | workflow-first §2.1 | micky installed "as a cached copy (MEMORY.md:11)" | **P7**: MEMORY.md:11 reads "Installed to Claude Code as marketplace `micky-psych-tools` (user scope)." | Source type unknown; W0-g determines it |
| B3 | workflow-first V3, §2.1 | a nonexistent path "is skipped with no error / silently" | **P1**, RF-A1 | `claude plugin list` prints `× Path not found: …`; the other paths load; exit 0 |
| B4 | workflow-first §7, G1 | learn-hub CLAUDE.md "loads on first read of a learn-hub file" | observed: both repos' CLAUDE.md are in this session's context from the start | Counted as always-paid in multi-repo sessions (§9) |
| B5 | workflow-first | H45 (pubmed-research-note-2, decision-brief slot arithmetic) missing from the disposition | inventory; **P6** (decision-brief.md:11-12 "first four … last three" over 6 headings) | §3.2 pubmed row; Appendix A H45 (W3) |
| B6 | risk-first §8, R2 | "21" claude.ai-synced skills | **P3**: `~/.claude/skills/synced/<uuid>/` holds 22 skill dirs + `manifest.json` | 22 (§2.5, §9) |
| B7 | risk-first §1 | project skills "demonstrably load in every session type" | risk-first's own §2.3 table | They load when the repo is the session's project or cloned in multi-repo cloud; not in a local session whose cwd is outside learn-hub (§2.5 Windows row) |
| B8 | risk-first §1 | "moving the servers into one plugin would force a `dependencies` entry" | purist / workflow-first topology | True only without family merges. `evidence` co-locates all three MCP consumers, so no dependency is needed (§4.4) |
| B9 | all three (inherited) | code-explainer template pointer at SKILL.md:67-68, :136 | **P5**: `grep` gives SKILL.md:30 and :99; README.md:86-87; `references/` holds `explanation-contract.md`, `vscode-shell.md` | Lines corrected in §3.2 and Appendix A; defect unchanged |
| B10 | purist | `.mcp.json` "byte-identical ×5"; pk-plasma's is "the 4th copy" | **P4**: md5 `1b35ee7c…` on 6 files: micky pubmed, CR, psych-paper-digest; learn-hub pubmed fork, CR fork, pk-plasma-animation | 6 identical copies (§4.4) |
| B11 | purist §2.6 | ``!`node … ready.mjs --json \|\| true` `` is safe because of `\|\| true` | SKL-35 corrected: injected commands are permission-checked, and outside auto mode anything short of allow aborts the invocation | No `!` injection; `ready.mjs` is an explicit Step 0 command (§2.6) |
| B12 | risk-first §5.5 | the output sink is resolved from the git toplevel of cwd | multi-repo sessions start at `/home/user`, which is not a repo (J2) | Env var + marker resolver in `sink.py` (§5.3) |
| B13 | workflow-first §2.2 | declares same-folder `dependencies` (`evidence → alignment`, …) | V4 / RF-A2 (an absent dependency disables); §2.7 per-plugin enablement | No dependencies anywhere; OPTIONAL handoffs with a fallback (T4) |

---

## Appendix C: Verification log and open items

**Probes run for this synthesis** (CLI 2.1.280, this cloud VM):

- **P1.** `CLAUDE_CONFIG_DIR=<scratch> CLAUDE_CODE_PLUGIN_DIRS='~/micky-psych-tools/plugins:/home/user/micky-psych-tools/plugins/gridgeist' claude plugin list` printed `gridgeist@inline … √ loaded` and `inline[0]: × Path not found: /root/micky-psych-tools/plugins`, exit 0.
- **P2.** A probe plugin with `hooks/hooks.json` (SessionStart + PreToolUse(Bash)) was loaded via `CLAUDE_CODE_PLUGIN_DIRS`, and `claude -p` was run from `/home/user`. Both hooks fired. The hook environment had `CLAUDE_PLUGIN_ROOT` = the plugin dir, `CLAUDE_PROJECT_DIR=/home/user`, `PWD=/home/user`, and `CLAUDE_ENV_FILE` set. This confirms the hooks-plugin premise and that root resolution must not use `CLAUDE_PROJECT_DIR`.
- **P3.** `ls ~/.claude/skills/synced/*/` shows 22 skill directories + `manifest.json`.
- **P4.** md5 of every `.mcp.json` in both repos: six files, all `1b35ee7cb2da4228dfdb9540c1bb616b`.
- **P5.** `grep -n explainer-template` gives code-explainer SKILL.md:30, :99 and README.md:86. `references/` = `explanation-contract.md`, `vscode-shell.md`.
- **P6.** decision-brief.md:11 reads "fixes the first four slots … You derive the last three". There are six `##` slot headings (L16, 31, 50, 71, 78, 90).
- **P7.** MEMORY.md:11 wording (B2).
- **P8.** `HOME=/root`; `/home/user` holds `learn-hub` and `micky-psych-tools`. `research-notes/` is not gitignored. `package.json` `"name": "learn-hub"`. learn-hub `session-start.sh` exits unless `CLAUDE_CODE_REMOTE`, and `cd`s to `CLAUDE_PROJECT_DIR`. `.claude/settings.json` holds SessionStart + two PreToolUse gates.

**Inherited probes:**
- V1–V4 (workflow-first): a folder of plugins loads from both clones in place; same-named plugins from two paths both load; an absent dependency disables; a same-folder dependency loads.
- RF-A1–RF-A6 (risk-first): env var semantics; dependency disables; multi-repo skips repo hooks; `@skills-dir` primary-cwd only; synced loses to a same-named in-place plugin; dmi on a command passes `--strict`, and `plugin details` does not reflect dmi.
- J (judges): many-to-one renames validate; same-folder dependencies load; a plugin SessionStart fires from `/home/user`.

**Open items**, each resolved in W0 (§10 checklist):
- **U1.** Plugin hooks in a *platform-started* multi-repo session. `claude -p` has passed (P2); the fallback is designed.
- **U2.** Whether the setup script runs before or after the clone. The design assumes it may run before.
- **U3.** The Windows user env var and CLI version (W0-g).
- **U4.** Nested `.claude/rules` with `paths:` in multi-repo sessions (W0-e).
- **U5.** Many-to-one `renames` on the real catalog (W0-c).
- **U6.** claude.ai personal upload mechanics (only if OD13-b).
- **U7.** Whether `userConfig` is prompted for env-var or `--plugin-dir` loads. The env var is the primary source; userConfig is second (R47).
