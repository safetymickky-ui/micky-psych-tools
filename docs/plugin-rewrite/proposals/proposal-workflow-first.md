# Target architecture: owner workflow and delivery first

**Angle.** Start from where the owner actually runs these tools, then decide where each capability lives so it loads there. Rewriting skill text comes second.
**Basis.** Phase-1 evidence in `wf1/` (claim ids `SKL/PLG/EVL/COM/LOC-nn`, used in their `corrected_claim` wording where the verdict was partial; LOC-26 refuted and unused) and inventory defects (cited `INV <unit> file:line`). Mechanisms not in the research were checked against the docs mirrored in `wf2/docs/` or with probes on Claude Code 2.1.280. These are tagged `V1…V12` and listed in the appendix, which also marks what is still **unverified**.

---

## 1. Thesis

The owner works on three surfaces:

- **Cloud multi-repo sessions.** Both repos are cloned under `/home/user` and the session starts above them.
- **Local Windows sessions.** micky-psych-tools is installed there as a user-scope marketplace.
- **claude.ai / Cowork.** 22 account-synced skills load there, and are synced into every Claude Code session too.

Today the setup fails on the owner's main surface:

- **None of the 14 micky plugins or the 8 learn-hub plugins loads in cloud** (LOC-42, PLG-47). The learn-hub-local marketplace is not registered anywhere (LOC-41).
- **learn-hub's SessionStart hook and sync gates don't run in multi-repo sessions** (PLG-47 corrected; V9). Those sessions therefore get no `npm install`, no `.env.local`, no `PUPPETEER_EXECUTABLE_PATH` and no duplication gate.
- **The fixes the owner made live in forks that never flow back upstream** (LOC-33, LOC-34).
- **The one cross-repo pipeline is broken at both ends** (LOC-35, INV digest-report-1).
- **Every session pays roughly 115k tokens of mandated or always-loaded text before doing any work** (section 8).

**The target makes delivery a property of the git checkout, not of the machine.** Six rules follow from that:

1. **Both repos' `plugins/` folders load in place on every surface** through `CLAUDE_CODE_PLUGIN_DIRS`.
   - Cloud: set as a cloud-environment variable.
   - Windows: set as a user environment variable.
   - This is verified for folder-of-plugins loading from both clones (V1), and a missing path is skipped silently (V3).
   - No copies, no marketplace install, no version bump to see a change (PLG-09).
2. **Each capability has exactly one home.**
   - micky-psych-tools holds everything reusable: gates, evidence writers, renderers, plugin tooling.
   - learn-hub holds everything bound to the app, its `/vault` and Supabase.
   - Forks are deleted, not synced. Two same-named plugins both load when both folders are on the path (V2), so the forks must go first.
3. **Cross-repo handoff is a file drop into learn-hub's inbox, never a skill call or a copied contract.**
   - micky producers write to `$LEARN_HUB_DIR/research-notes/`. learn-hub's intake skills own everything after that.
   - A handoff to a skill in the other repo is always optional by name, with a stated fallback. It is never a `dependencies` entry: an unsatisfied dependency disables the whole plugin (V4).
4. **Repo-bound hooks travel inside a plugin**, so they fire in multi-repo sessions.
5. **State that must compound across ephemeral cloud VMs lives in git**, not in `${CLAUDE_PLUGIN_ROOT}` or `${CLAUDE_PLUGIN_DATA}`.
6. **Always-loaded context drops from about 115k tokens to about 15k.**
   - Delete the parallel router (ROUTING.md) and the mandated reads.
   - Move skill-owned gotchas out of `CLAUDE.md` into the skills that need them.
   - Consolidate 55 listing entries into about 21 model-invocable ones.

---

## 2. Target topology

### 2.1 What loads where: today vs target

| Surface | Today (evidence) | Target delivery route |
|---|---|---|
| **Cloud, multi-repo** (cwd `/home/user`, both clones) | Only learn-hub `.claude/skills` and the 22 claude.ai skills load. `claude plugin list` is empty (LOC-42). Repo `.claude/settings.json` hooks and `.mcp.json` are not read (PLG-47 corrected). PDF libraries are absent (INV learn-hub project-skills obs "PDF tooling is absent"). | **Environment variables** (they reach every command, V7): `CLAUDE_CODE_PLUGIN_DIRS=/home/user/micky-psych-tools/plugins:/home/user/learn-hub/plugins`, `LEARN_HUB_DIR=/home/user/learn-hub`, `MICKY_TOOLS_DIR=/home/user/micky-psych-tools`, `PUPPETEER_EXECUTABLE_PATH=/opt/pw-browsers/chromium`, `PUPPETEER_SKIP_DOWNLOAD=1`. The existing Supabase variables stay (docs/cloud-env-setup.md). **Setup script** (VM tooling only, cached about 7 days, V7): `pip install pymupdf pypdf pdfplumber`, `apt-get install -y poppler-utils`, a pinned `firecrawl-cli`. **Plugin hooks** (learn-hub plugin): `npm install`, `.env.local`, `core.hooksPath` and the two sync gates. |
| **Cloud, single-repo** | The repo's own hooks load. Nothing is installed. | Same environment. The path of the repo that is not cloned is skipped silently (V3). The micky writers fall back to writing into cwd. Hooks are removed from learn-hub's `settings.json` so they don't fire twice. |
| **Local Windows** | micky installed as a user-scope marketplace, as a cached copy (MEMORY.md:11). Whether the source is a local directory or GitHub is unknown (LOC open question). The learn-hub-local marketplace is not registered (LOC-41). | A Windows **user environment variable** `CLAUDE_CODE_PLUGIN_DIRS=<micky>\plugins;C:\Users\User\Desktop\Learn\plugins` (`;` separator, documented V7), plus `LEARN_HUB_DIR` and `MICKY_TOOLS_DIR`. Then **uninstall the marketplace copies**, or the plugins renamed in W5 would load beside their old names. |
| **claude.ai / Cowork** | 22 synced skills (15,385 description chars, V6). None come from these repos. | No repo capability ships there by default (OD5). Only the name collisions get resolved (section 2.4). |

Why not the documented cloud route of claude.ai-synced plugins (PLG-47)? Every change would need a re-upload of a copy. That recreates the fork-drift failure class (LOC-33, LOC-34) and ties cloud sessions to whatever was last uploaded. The environment-variable route loads whatever commit the session checked out, including a feature branch. Test a rewrite on a branch session and master sessions keep the old tools. The trade-off: a session that does not clone micky gets no micky tools. OD1 records this.

### 2.2 Ownership map (target)

**micky-psych-tools: 6 plugins, 15 skills, 0 commands** (today: 14 plugins, 17 skills, 12 commands)

| Plugin | Skills | Owns (shared references inside the plugin; the only legal way to share files, PLG-22 and COM-38) |
|---|---|---|
| `alignment` (renames: intent-lock, decision-interview, plan-critique) | `intent-lock`, `misread-capture`, `decision-interview`, `plan-critique` | `references/interview-contract.md`: the admission threshold, destructive always-ask, picker mechanics on AskUserQuestion, the autonomous fallback, stop sovereignty. Today these are copied three times with drift (INV alignment obs). Also `references/handback.md`: the one-line `Assumed: … — say if wrong.` that callers print. |
| `evidence` (renames: pubmed-research-note, comprehensive-review, psych-paper-digest) | `pubmed-research-note`, `comprehensive-review`, `lit-watch` (was psych-paper-digest) | One `.mcp.json` (pubmed, clinical-trials). Today there are 3 micky + 3 learn-hub identical copies (LOC-13, PLG-34). `references/report-contract.md` covers the `## Sources` grammar, depth contract and citation discipline; the NCT grammar exists in 3 variants today (INV pubmed-research-note-8). `references/engines.md` covers tools by function, E-utilities/CT.gov fallbacks and the firecrawl fetch-only policy. `scripts/` holds lit-watch's window math, pagination and dedupe. |
| `visuals` (renames: clinical-infographic, concept-animation, ml-concept-lab, code-explainer) | `clinical-infographic`, `concept-animation`, `ml-concept-lab`, `code-explainer` | `references/html-artifact-contract.md`: self-contained, reduced-motion, a11y, `<!DOCTYPE>`/`color-scheme`, the learn-hub layout floor. Also `references/render-verify.md` and `scripts/check-html.mjs`. This replaces about 265 lines of near-duplicate tail (INV renderers obs). |
| `firecrawl` | `firecrawl` | A slim routing body plus `references/vendor-onboarding-<date>.md`. |
| `gridgeist` | `gridgeist` | Vendored as is. The Codex `openai.yaml` and assets are removed and the upstream commit is recorded. |
| `plugin-creator` | `plugin-creator`, `refine-plugin` | `scripts/validate.py`, `scripts/bump.py` and templates. These are self-contained and target either repo (section 2.5). |
| (repo, not a plugin) `state/` | — | `misreads.md` and `lit-watch/` (config, `last_swept`, digests). Private git holds the compounding state (OD8). |

**learn-hub: 1 plugin with 3 skills, plus 10 project skills, and no marketplace** (today: 8 plugins, 11 project skills)

| Home | Contents | Why here |
|---|---|---|
| `plugins/learn-hub` (loaded by the env var on every surface) | Skills: `digest-report`, `ingest-visual` (merges ingest-infographic and ingest-animation), `sync-vault`. Hooks: SessionStart ops, PreToolUse gates. | These are what the *other* repo's sessions must reach: the intake endpoints, the sync they require, and the hooks that must fire in multi-repo sessions. |
| `.claude/skills/` (load wherever learn-hub is cloned; locally when cwd is inside learn-hub) | `pdf-pipeline`, `ingest-article`, `ingest-slides`, `atomize-book`, `verify` (model-invocable). `vault-atomizer`, `vault-vectors`, `vault-coverage`, `check-repetition`, `pk-plasma-animation` (user-only, OD7). | App-internal authoring and maintenance. They need repo scripts, `.env.local` and `Book/`. A plugin wrapper only buys namespacing, at the cost of an install step nobody took (INV learn-hub plugins obs "INSTALLATION"). |

**Rule for choosing a home.** A capability becomes a *plugin* when it must be reachable from a session that did not start inside its repo, or when it carries hooks. Everything else bound to a repo is a *project skill*. Nothing depends on cwd.

### 2.3 The pipeline, redrawn as file contracts

```
micky producers                        learn-hub inbox (git-tracked)              learn-hub intake → app
evidence:pubmed-research-note ─┐
evidence:comprehensive-review ─┼─ report .md ─▶ $LEARN_HUB_DIR/research-notes/<slug>.md ──(on "digest"/"atomize")──▶ learn-hub:digest-report ─▶ /vault notes ─▶ learn-hub:sync-vault ─▶ Supabase
visuals:* (html)  ─────────────┴─ .html + .meta.json ▶ research-notes/visuals/<slug>.* ──────────────────────────▶ learn-hub:ingest-visual ─┘
          fallback when $LEARN_HUB_DIR is unset or its marker is missing: write into cwd and say so (COM-37)
```

- **Write → show → archive is the default. Publishing to live Supabase is opt-in (OD3).**
  - This follows the pubmed fork's atomize gate and digest-report's own trigger contract.
  - It removes the comprehensive-review fork's default live-DB write (INV CR-fork-1: fork SKILL.md:166-176).
- **Ownership of each contract.**
  - The inbox layout belongs to learn-hub (`digest-report/references/inbox-contract.md`).
  - The report format belongs to micky (`evidence/references/report-contract.md`).
  - digest-report is rewritten to consume `## Sources`: per-note `sources:` = report basename + the Sources lines whose topic the note covers. Legacy reports with inline PMIDs are still accepted.
  - This closes the contradiction between digest-report SKILL.md:88-90 and 115-116 on one side and pubmed-research-note SKILL.md:211 and comprehensive-review SKILL.md:130 on the other (INV digest-report-1).
- **The visual layout contract has one executable owner: learn-hub.**
  - The owner is the tested code in `scripts/lib/animation-responsive.mjs`, `infographic-responsive.mjs` and `src/lib/animation-layout.ts` (INV renderers obs "real source of truth is executable code in another repo").
  - learn-hub gets a thin CLI, `npm run audit:visual -- <file>`. `ingest-visual` always runs it; `visuals` producers run it through `$LEARN_HUB_DIR` when present and fall back to their own screenshot check otherwise.
  - This is how the stage-collapse fix finally reaches the producers (LOC-34; INV concept-animation-1; INV ml-concept-lab-1).
- **What this retires.** The pull-based drain (`empty-vault` walks micky `vault/`, finds learn-hub by a deleted directory, deletes the assets learn-hub waits for) goes away. So does the handshake nobody listens to.
  - INV vault-keeper-3: empty-vault SKILL.md:36-37.
  - INV vault-keeper-4: empty-vault SKILL.md:55-57.
  - INV ingest-infographic-1: SKILL.md:3, :136-137.
  - INV ingest-animation-1: SKILL.md:124.

### 2.4 Name collisions with claude.ai-synced skills

| Collision | Fix | Evidence |
|---|---|---|
| `psych-paper-digest`: the micky watchlist triage vs `anthropic-skills:psych-paper-digest` (daily 8–12 papers) | Rename the micky skill to **`lit-watch`**, with a `renames` entry (PLG-44). Make it user-only if OD4/OD7 choose that; its description then leaves the listing entirely (SKL-36). The triage rubric also becomes the declared owner of the "Act/Read/suppressed" rule that learn-hub's `docs/feed-highlights.md` already borrows. | SKL-55; INV psych-paper-digest-6. pubmed's NOT-for describes the *claude.ai* digest (INV pubmed-research-note description). docs/feed-highlights.md step 3 and the feed-highlights spec: "Triage, never adjudication (the `psych-paper-digest` rule)". |
| `daily-random-review` (claude.ai) says it "chains into the comprehensive-review … skills internally". It reads textbooks, requires ZERO citations and writes to `Finish/Micky/`. | Add a Not-for clause to `evidence:comprehensive-review`: "textbook-sourced board-prep reviews for the Obsidian board vault (anthropic-skills:daily-random-review)". The owner also edits the claude.ai skill to say "follow the structure below" instead of "chains into" (OD6). Synced skills can only be changed on claude.ai (V7). | V8: synced SKILL.md:12-13, :128, citation rule. comprehensive-review's citation contract is the opposite (INV CR). |
| `obsidian-knowledge-vault` ("atomize", "make notes from") vs atomize-book / vault-atomizer / pubmed's "atomize" gate | Every "atomize" description names its *input* (book file / note id / finished report) plus a reciprocal Not-for, including `anthropic-skills:obsidian-knowledge-vault`. pubmed's gate word becomes "digest". | LOC-31 (P0-2 open); INV atomize-book description |
| `bullet-reconstruct` vs ingest-article's trigger "bullet-reconstruct this"; `pdf` vs pdf-pipeline | Drop the trigger. Scope pdf-pipeline to "get a PDF into the Learn hub", with a Not-for pointing to `anthropic-skills:pdf`. | INV ingest-article-8; INV learn-hub project-skills obs "ROUTING OVERLAP" |

### 2.5 Repo-bound plugins

- **plugin-creator** today calls repo-root `scripts/*.py` that the installed cache never contains (INV plugin-creator-1). It also assumes the micky repo is cwd.
  - **Target:** `validate.py` and `bump.py` move into `plugins/plugin-creator/scripts/` and are invoked as `python3 ${CLAUDE_SKILL_DIR}/../../scripts/…` (SKL-33; COM-46).
  - The target repo comes from `--repo` or from the nearest `.claude-plugin/marketplace.json` / `plugins/` directory *with an explicit confirmation line*.
  - The same validator then serves learn-hub's plugin and `.claude/skills`. That closes learn-hub polish-plan P1-1 (LOC-30) without a second validator.
  - Its SessionStart hook sets `core.hooksPath .githooks` on the micky checkout in cloud, the way learn-hub already does. That makes the health check a git pre-commit hook instead of prose (LOC-10).
- **vault-keeper** resolves the vault by walking up from cwd or through `${CLAUDE_PLUGIN_ROOT}/../../vault`. That lands in the plugin cache or in learn-hub's `/vault` (LOC-35, LOC-36; INV vault-keeper-1, -2). **It is retired** (OD2).
  - If the owner keeps it, the root comes from `$MICKY_TOOLS_DIR/vault` plus a marker file, and the index job becomes a script (disposition alternative, OD2).
- **learn-hub hooks** move from `.claude/settings.json` into `plugins/learn-hub/hooks/hooks.json`.
  - The session-start script resolves the repo root from `${CLAUDE_PLUGIN_ROOT}`, not `$CLAUDE_PROJECT_DIR`. In a multi-repo session that variable is `/home/user`, so today's script would `cd` into the wrong directory (V9).
  - Plugin hooks load with `--plugin-dir`-style loads (documented, V7). **Probe in a live multi-repo session in W0.**

---

## 3. Disposition table (every unit)

Legend: `keep / rewrite / merge / split / move / retire / convert-to-project-skill / convert-to-script`. "→" is the target.

### 3.1 micky-psych-tools plugins (14)

| # | Unit | Disposition | Target | Reason (evidence) |
|---|---|---|---|---|
| P1 | `plugins/pubmed-research-note` | merge | `evidence` plugin | Shares MCP, contracts and handoffs with CR and lit-watch. The byte-identical `.mcp.json` is loaded 3–6 times (LOC-13, PLG-34). The NCT grammar exists in 3 variants (INV pubmed-8). Intra-family handoffs are co-loaded. |
| P2 | `plugins/comprehensive-review` | merge | `evidence` | The depth, citation and firecrawl contracts are near-verbatim copies of pubmed's (INV CR duplication_and_drift). |
| P3 | `plugins/psych-paper-digest` | merge | `evidence` (skill `lit-watch`) | Same engines. Collides by name with the claude.ai digest (SKL-55). |
| P4 | `plugins/intent-lock` | merge | `alignment` plugin | The three gates copy their shared mechanics with drift (INV alignment obs); only one plugin can share a reference file (PLG-22). |
| P5 | `plugins/decision-interview` | merge | `alignment` | As P4. It has no README, CHANGELOG or evals (INV decision-interview-1). |
| P6 | `plugins/plan-critique` | merge | `alignment` | As P4. Its silence semantics are opposite to its siblings' (INV plan-critique-4). |
| P7 | `plugins/clinical-infographic` | merge | `visuals` | The shared HTML contract and tail make up 38% of its body (INV renderers obs). Its light-lock and strip rules must match learn-hub's executable audit (INV CI-1, -2). |
| P8 | `plugins/concept-animation` | merge | `visuals` | It carries the stage-collapse layout rule; the fix exists only in learn-hub's copy (LOC-34; INV CA-1). |
| P9 | `plugins/ml-concept-lab` | merge | `visuals` | It has the same collapse rule and a broken verify recipe (INV ML-1, -2). |
| P10 | `plugins/code-explainer` | merge | `visuals` | Shared HTML contract. The template it references was never committed (INV CE-1). |
| P11 | `plugins/firecrawl` | rewrite | `firecrawl` (slim) | The "verbatim" vendor guide is stale in load-bearing places (INV firecrawl-1). The 4.2k-token body mostly covers paths the owner doesn't use (INV firecrawl-4). It writes the key into cwd `.env` (INV firecrawl-3). |
| P12 | `plugins/gridgeist` | keep | `gridgeist` (trim) | Lean and well scoped. Only dead Codex metadata and an unrecorded upstream revision need fixing (INV gridgeist-1, -3). |
| P13 | `plugins/plugin-creator` | rewrite | self-contained, serves both repos | Cwd- and repo-script-bound, so it breaks after install (INV plugin-creator-1). Its scaffold fails its own audit (INV plugin-creator-2). |
| P14 | `plugins/vault-keeper` | retire (W2, after the final drain) | learn-hub inbox (section 2.3) | Its root detection is wrong in both directions (INV vault-keeper-1, -2). The drain handshake is broken (INV vault-keeper-3, -4). Its Obsidian links don't resolve (INV vault-keeper-7). The staging vault duplicates the path the forks already use (INV research-writers obs "two parallel routes into the same /vault"). OD2 has the keep-and-fix alternative. |

### 3.2 micky-psych-tools skills (17 plus the scaffold template)

| # | Unit | Disposition | Target | Reason (evidence) |
|---|---|---|---|---|
| S1 | `pubmed-research-note/skills/pubmed-research-note` | rewrite | `evidence:pubmed-research-note` | The body is ~4.7k tokens plus ~5.9k of mandatory references (INV pubmed obs). It still requires a `Reframed:` line that intent-lock abolished (INV pubmed-1: SKILL.md:263 vs intent-lock SKILL.md:226). It hardcodes the MCP prefix with "No ToolSearch" (tool-catalog.md:25-28). It has no path for an absent dependency (INV pubmed-6). Target: sink via the inbox, tools by function (MP-PLG-2), conditional references. |
| S2 | `comprehensive-review/skills/comprehensive-review` | rewrite | `evidence:comprehensive-review` | Its "every section has a number" rule contradicts itself (INV CR-1). It has no engine-failure policy (INV CR-2) and cites nonexistent "house rules" (INV CR-5). It needs a Not-for covering daily-random-review (V8). |
| S3 | `psych-paper-digest/skills/psych-paper-digest` | rewrite + convert-to-script (mechanics) | `evidence:lit-watch` + `scripts/sweep.py` | Windows on pdat, not edat (INV ppd-1: sweep-recipes.md:39-40). Silently truncates at 50 results (INV ppd-2). Dedupes against the newest digest only (INV ppd-5). Window math is prose (INV ppd-12). Name collision (SKL-55). Its state lives in cwd, which dies with a cloud VM. |
| S4 | `intent-lock/skills/intent-lock` | rewrite | `alignment:intent-lock` (≤2k tokens) | At 6.2k tokens it is loaded by 5+ callers (INV alignment obs). Its silent contract contradicts itself in 11 places (INV intent-lock-1). It uses claude.ai picker types, has no AskUserQuestion fallback, and assumes "the user is usually on a phone" (SKILL.md:144; INV intent-lock-2). |
| S5 | `intent-lock/skills/misread-capture` | rewrite | `alignment:misread-capture` + `scripts/ledger-append.py` → `$MICKY_TOOLS_DIR/state/misreads.md` | The ledger is written under `${CLAUDE_PLUGIN_ROOT}` and forked across repos (PLG-57, LOC-37; INV intent-lock-3). The `Prior:` line has no eliciting question (INV intent-lock-4). |
| S6 | `decision-interview/skills/decision-interview` | rewrite | `alignment:decision-interview` | Its unprompted trigger drops the materiality threshold (INV DI-2). The fallback is undetectable (INV DI-3). It needs the shared interview contract. |
| S7 | `plan-critique/skills/plan-critique` | rewrite | `alignment:plan-critique` | Command and skill disagree on the no-plan case (INV PC-1). Hand-off to intent-lock is unreachable (INV PC-2). It uses mega-bullets (INV PC-3). |
| S8 | `clinical-infographic/skills/clinical-infographic` | rewrite | `visuals:clinical-infographic` | The template has a dark block and non-stacking strips (INV CI-1, -2). The palette claims AA and fails it (INV CI-3). It files to vault/assets, a dead end (INV CI-6). Target: hand off to `learn-hub:ingest-visual` through the inbox. |
| S9 | `concept-animation/skills/concept-animation` | rewrite (absorbs F11) | `visuals:concept-animation` | Takes the learn-hub copy's layout contract, 5-viewport check and full-document rule. Keeps upstream's portability. Its filing moves to ingest-visual (INV learn-hub CA duplication_and_drift). |
| S10 | `ml-concept-lab/skills/ml-concept-lab` | rewrite | `visuals:ml-concept-lab` | Collapse rule; verify import fails (INV ML-2); gradient check is wrong (INV ML-3); clinical routing contradicts itself (INV ML-4); example path is wrong (INV ML-5). |
| S11 | `code-explainer/skills/code-explainer` | rewrite | `visuals:code-explainer` | Its primary template does not exist (INV CE-1). The byte check is prose (INV CE-2). Target: commit the template or drop the claim; the byte check goes into `check-html.mjs`. |
| S12 | `firecrawl/skills/firecrawl` | split | `firecrawl` body (routing + contract + gotchas) + dated vendor reference | SKL-19 (mutually exclusive paths belong in separate files); INV firecrawl-1, -4. |
| S13 | `gridgeist/skills/gridgeist` | keep | unchanged body | Healthy (INV gridgeist strengths). Only the Codex metadata is removed. |
| S14 | `plugin-creator/skills/plugin-creator` | rewrite | `plugin-creator:plugin-creator` | Breaks its own description rule (LOC-21). Its Not-for is stale (LOC-22). No commands template, no `${CLAUDE_PLUGIN_ROOT}` guidance (INV plugin-creator-6). It scaffolds runnable eval cases, not `evals.json` (EVL-07). |
| S15 | `plugin-creator/skills/refine-plugin` | rewrite | `plugin-creator:refine-plugin` (user-only per OD7) | Bumps without a CHANGELOG entry (INV plugin-creator-5). Its target is either repo. |
| S16 | `vault-keeper/skills/vault-keeper` | retire | inbox contract (section 2.3) | See P14. |
| S17 | `vault-keeper/skills/empty-vault` | retire (after one final drain in W2) | — | Broken locator and asset deletion (LOC-35; INV vault-keeper-3, -4). A destructive flow that the model can invoke (SKL-36). |
| S18 | `plugin-creator/.../references/templates/SKILL.md` | rewrite | YAML-valid, spec-conformant template (quoted description, `argument-hint`, conditional reference pointers) | `{{PLACEHOLDER}}` breaks YAML (INV plugin-creator-6; SKL-50, -51). |

### 3.3 micky-psych-tools commands (12): all folded into skill frontmatter (SKL-01, PLG-15, COM-42)

| # | Unit | Disposition | Target |
|---|---|---|---|
| C1 | `plugin-creator/commands/new-plugin.md` | retire | `plugin-creator` skill, `argument-hint: "[purpose]"` |
| C2 | `plugin-creator/commands/refine-plugin.md` | retire | `refine-plugin` skill, `argument-hint: "[plugin]"` |
| C3 | `plugin-creator/commands/route.md` | retire | none (router removed, LOC-09). The only non-wrapper command (LOC-17 corrected). |
| C4 | `vault-keeper/commands/empty-vault.md` | retire | none (P14) |
| C5 | `psych-paper-digest/commands/digest.md` | retire | `lit-watch` skill, `argument-hint: "[domain]"` |
| C6 | `comprehensive-review/commands/comprehensive-review.md` | retire | skill `argument-hint` |
| C7 | `clinical-infographic/commands/infographic.md` | retire | skill `argument-hint`. Its procedure summary had already drifted (INV CI commands). |
| C8 | `concept-animation/commands/animate.md` | retire | skill `argument-hint` |
| C9 | `code-explainer/commands/explain-code.md` | retire | skill `argument-hint`. Contradicts Step 0 (INV CE commands). |
| C10 | `ml-concept-lab/commands/visualize.md` | retire | skill `argument-hint`. Carries the stale "fits one screen" rule (INV ML commands). |
| C11 | `decision-interview/commands/resolve-decisions.md` | retire | skill `argument-hint` |
| C12 | `plan-critique/commands/critique-plan.md` | retire | skill `argument-hint`. Contradicts the skill (INV PC-1). |

If OD7 keeps short names, add `disable-model-invocation: true` one-line alias stubs with no procedure text. Their descriptions then cost nothing in the listing (SKL-36).

### 3.4 micky-psych-tools repo files

| # | Unit | Disposition | Target | Reason (evidence) |
|---|---|---|---|---|
| R1 | `scripts/validate.py` | move + rewrite | `plugins/plugin-creator/scripts/validate.py` | Crashes on bad JSON (INV validate.py-1). Hand-rolled YAML (INV validate.py-3). Rejects stdio MCP (LOC-11). New version: shells out to `claude plugin validate --strict` per plugin and for `.claude/skills` (PLG-10, -11; SKL-49); `yaml.safe_load`; house rules only (length, reciprocity of Not-for, no mandated-read grep, CHANGELOG == version, cross-plugin names resolve to same-repo dependencies, no cross-repo `dependencies`, per V4). |
| R2 | `scripts/route.py` | retire | — | Re-indexes descriptions Claude already routes on (LOC-09). Writes on `--help` (INV route.py-2). Constrains description wording (LOC-08). |
| R3 | `scripts/bump.py` | move + rewrite | `plugins/plugin-creator/scripts/bump.py` | Dual-write goes against the docs (PLG-06, LOC-02). ASCII escapes and no trailing newline (LOC-45). Writes before validating (INV bump.py-4). New version: plugin.json only, plus the CHANGELOG entry, dry-run by default. |
| R4 | `ROUTING.md` | retire | descriptions with reciprocal Not-for | ~5,049 tokens per request, 29/29 cues verbatim, 0 Not-for clauses (INV route.py/ROUTING.md-1). Evals never see it (EVL-19). |
| R5 | `MEMORY.md` | split | `MEMORY.md` ≤ 6 KB of open threads and current wave, read on demand; `docs/history.md` for milestones; versions table deleted | 108 KB / ~27k tokens as a mandated read. About 30 of 51 milestones are content filings (LOC-25). The versions table duplicates plugin.json (R88 in the rubric). |
| R6 | `CLAUDE.md` (micky) | rewrite | ≤ 5 KB: layout, hard rules, `validate` command, delivery pointer | 69% of it is a plugin catalog that already omits gridgeist (INV CLAUDE.md-1, -2). It mandates MEMORY and ROUTING (LOC-09, LOC-25). |
| R7 | `.claude-plugin/marketplace.json` | rewrite | versionless entries, `$schema`, `renames` map, no hand-bumped top-level version | PLG-06, PLG-44; INV marketplace.json-1, -3. |
| R8 | `README.md` | rewrite | install = env var; correct `--strict` per-directory validation | INV README-1, -2, -3. |
| R9 | `vault/` | retire after the final drain (OD2) | `$LEARN_HUB_DIR/research-notes/` | 7 artifacts and 6 MOCs today. It is a staging buffer (section 2.3). |
| R10 | `.gitignore` (new entries) | rewrite | adds `.env`, `.firecrawl/`, `plugins/*/evals/results/` | INV firecrawl-3; EVL-26. |

### 3.5 learn-hub plugins (8), with their skills and commands

| # | Unit | Disposition | Target | Reason (evidence) |
|---|---|---|---|---|
| L1 | `plugins/intent-lock` (fork: intent-lock, misread-capture, second `misreads.md`) | retire | `micky alignment`. Ledger entries merged into `state/misreads.md`. | Same name and version as micky's, and both load together (V2). It splits the ledger (INV learn-hub intent-lock-1). Its hand-off target is not vendored (INV learn-hub intent-lock-4). |
| L2 | `plugins/pubmed-research-note` (fork) | retire | `evidence:pubmed-research-note`. The fork's research-notes sink becomes upstream's default whenever `$LEARN_HUB_DIR` resolves. | The fork differs only in the filing path (LOC-33). Its copied evals fail by construction (INV pubmed-fork-1). It has dangling references (INV pubmed-fork-3). |
| L3 | `plugins/comprehensive-review` (fork) + `/comprehensive-review` | retire | `evidence:comprehensive-review` | Makes a live-DB write the default (INV CR-fork-1). Contradicts itself about its deliverable (INV CR-fork-2). |
| L4 | `plugins/digest-report` + `/digest-report` | merge + rewrite | `plugins/learn-hub` skill `digest-report`. The command is folded (`argument-hint: "[report-path …]"`). | Unreachable by default (INV digest-report-2). The input contract conflicts with producers (INV digest-report-1). Stale sync-cost claim (-3). Voice-QC can't run as written (-5). PowerShell process check (-8). It becomes the owner of the inbox contract. |
| L5 | `plugins/source-to-vault` (skill `ingest-source`, `/ingest`) | retire | superseded by pdf-pipeline → ingest-article / atomize-book | Writes production rows with no `/vault` source (INV source-to-vault-1). Batch-ingests `Book/` without confirmation (-2). Collides on triggers (-3). Omits derived columns (-4). |
| L6 | `plugins/vault-atomizer` + `/atomize` | convert-to-project-skill | `.claude/skills/vault-atomizer` (user-only, `argument-hint`) | App-internal maintenance. Never loaded (LOC-41). Its sync runs in the foreground (INV vault-atomizer-3). Stale statistics (-2). |
| L7 | `plugins/vault-vectors` + `/vectors` | convert-to-project-skill | `.claude/skills/vault-vectors` (user-only) | As L6. Command and skill contradict each other (INV vault-vectors-1, -2). |
| L8 | `plugins/pk-plasma-animation` + `/pk-animation` + `.mcp.json` | convert-to-project-skill | `.claude/skills/pk-plasma-animation`. MCP removed; calls `evidence:pubmed-research-note` optional-with-stop. Filing delegated to `learn-hub:ingest-visual`. | Duplicate MCP (INV pk-7). Its brief's Sources format contradicts pubmed's (INV pk-2). It hand-builds the upsert (INV pk-1). Its sibling is not installed (INV pk-3). |
| L9 | `.claude-plugin/marketplace.json` (learn-hub-local) | retire | none; `plugins/` loads as a folder of plugins (V1) | Never registered (LOC-41). Validation passes per plugin directory without it. |
| L10 | `.claude/settings.json` hooks + `.claude/hooks/*.sh` | move | `plugins/learn-hub/hooks/` (root from `${CLAUDE_PLUGIN_ROOT}`) | Don't run in multi-repo sessions (PLG-47 corrected). Keeping them in both places would fire twice in single-repo sessions. |

### 3.6 learn-hub project skills (11)

| # | Unit | Disposition | Target | Reason (evidence) |
|---|---|---|---|---|
| F1 | `.claude/skills/atomize-book` | split | Body ≤5k tokens (checklist, standing rules, per-phase "read X before step N"); `references/` per phase; the 58 pipeline gotchas from CLAUDE.md go into the phase they concern; the Python tooling moves to repo `tools/source-pipeline/`, run by `npm test` | 1,256 lines / ~21k tokens (INV atomize-book-4). Contradicts itself on topic-id links (-1). Stale sync economics (-2). Missing `\$`, equation-PNG, stadium and `LIVE_GROUPS` rules (-3). ingest-article calls its scripts by path (INV project-skills obs "SCRIPT COUPLING"). |
| F2 | `.claude/skills/ingest-article` | rewrite | ≤1,024-char quoted description; `ARTICLE_INBOX_DIR` env var plus a gitignore entry; the inbox sweep asks before deleting; conditional references; fixed source-cover command | Windows path and repo-relative delete (INV ingest-article-1). Broken command (-2). ~18k tokens loaded every run (-7). Invalid YAML (SKL-51). |
| F3 | `.claude/skills/ingest-slides` | rewrite | `${CLAUDE_SKILL_DIR}/scripts/…`; figure and loss gates; sync tail delegated to `learn-hub:sync-vault` | Script paths are wrong (INV ingest-slides-1). pdf-pipeline doesn't route to it (-2). Tail contradicts ingest-article (-4). |
| F4 | `.claude/skills/ingest-infographic` | merge | `learn-hub:ingest-visual` (plugin) with `references/infographic.md` | A structural twin of F5, about 70% shared (INV ingest-infographic duplication). Dead empty-vault trigger (-1). Wrong sync claim (-2). Stale route (-4). |
| F5 | `.claude/skills/ingest-animation` | merge | `learn-hub:ingest-visual` with `references/animation.md`; runs `audit:visual` including layout | Doesn't check stage collapse or quirks mode (INV ingest-animation-2). Dead trigger (-1). |
| F6 | `.claude/skills/pdf-pipeline` | rewrite | The single broad PDF trigger: routes slides to ingest-slides; tail delegated to `learn-hub:sync-vault` | Routes slides to atomize-book (INV pdf-pipeline-1). Its ≤200 KB apply rule can never be met (-2). Wrong vault path (-3). Stale preflight (-5). |
| F7 | `.claude/skills/sync-vault` | move + rewrite | `learn-hub:sync-vault` (plugin): the sole owner of the sync, revalidate and verify tail plus the operational gotchas (background job, `EXIT=0` + Upserted line, fetch-first, TaskStop zombie); one `npm run sync:safe` wrapper script | 8 places restate the tail with 4 contradictory apply rules (INV project-skills obs "SHARED SYNC TAIL"). Recommends the nested layout (INV sync-vault-1). Its default path doesn't fit a 4,532-note vault (-2). digest-report and ingest-visual REQUIRE it, so it must be reachable wherever they are. |
| F8 | `.claude/skills/vault-coverage` | rewrite | user-only; `BOOK_ROOT` env var; atomize-book's final step adds `coverage-sources.json` entries | Windows path (INV vault-coverage-2). Source map covers 26 of 70 books (-1). |
| F9 | `.claude/skills/check-repetition` | rewrite (light) | user-only; Not-for naming detect-duplicates and atomize-book §7b; revalidate via sync-vault | INV check-repetition-1, -2. Otherwise accurate against the code. |
| F10 | `.claude/skills/verify` | rewrite + convert-to-script | bundled `scripts/mint-session.mjs` and `scripts/probe.mjs`; description gains triggers and a Not-for (browser pane / devtools) | The scripts it cites never existed (INV verify-1). The CLAUDE.md gotchas point here as the trusted method. |
| F11 | `.claude/skills/concept-animation` (learn-hub copy) | retire | Layout fixes merged into `visuals:concept-animation` (S9). Filing goes to `ingest-visual`. The builder pattern goes to `pk-plasma-animation` references. | A same-name collision with the micky plugin (INV learn-hub CA-7). Duplicates ingest-animation (-6). Stale builder path (-5). |

### 3.7 learn-hub CLAUDE.md, as it relates to skills

| # | Unit | Disposition | Target | Reason (evidence) |
|---|---|---|---|---|
| G1 | `learn-hub/CLAUDE.md` (3,126 lines, 268 KB, ~67k tokens) | split | Root ≤ 32 KB (~8k tokens). **Skill-owned material moves into skills:** the 58 import-pipeline gotcha headings go to atomize-book, ingest-*, sync-vault and digest-report references; "Vault note format" (lines 206-360) goes to `learn-hub:sync-vault/references/vault-format.md`, with a 10-line pointer left behind. **App gotchas and "Pages"** go to `.claude/rules/*.md` with `paths:` (OD9). Skill names are updated to the new homes. | SKL-30, MP-SKL-8 ("a section that grew into a procedure belongs in a skill"). The docs target is under 200 lines per CLAUDE.md, with path-scoped rules loaded on matching reads (V7). Gotchas drift in both directions with the skills (INV project-skills obs "GOTCHA DRIFT"). Evals never see CLAUDE.md (EVL-19), so skills that defer to it (digest-report SKILL.md:69-70) are untestable. |

---

## 4. Shared-content strategy

1. **Inside a repo, the family plugin is the unit of sharing.** Shared references live in `alignment/references`, `evidence/references` and `visuals/references`. Skills link to them one level deep with "Before step N, read X" (SKL-16, SKL-18). No symlinks, because in-place loads keep only intra-plugin symlinks (PLG-23), and no `../other-plugin` paths (PLG-22, COM-38).
2. **Across repos: four interfaces, one owner each, no copies.**

   | Interface | Owner | Consumer obligation | Drift check |
   |---|---|---|---|
   | Learn inbox (paths, `.meta.json` fields, collision `-2`) | learn-hub `digest-report/references/inbox-contract.md` | Producers restate only the two target paths and the cwd fallback, in ≤3 lines | Validator: every producer names `research-notes/` exactly |
   | Report format (`## Sources` grammar, no inline citations, depth contract) | micky `evidence/references/report-contract.md` | digest-report's input section cites it by name. pk-plasma's brief defers to it. | One fixture report, `evidence/evals/fixtures/report-v1.md`, generated by an evidence eval and consumed by a digest-report eval. `learn-hub scripts/check-contract-parity.mjs` compares the two copies when `$MICKY_TOOLS_DIR` is present. It warns, and never fails when the other checkout is absent. |
   | Visual layout and self-containment | learn-hub audits (`scripts/lib/*-responsive.mjs`, `src/lib/animation-layout.ts`) behind `npm run audit:visual` | `visuals` producers run it through `$LEARN_HUB_DIR`; the prose contract summarizes and points to it | Existing learn-hub unit tests |
   | Gate hand-back (`Assumed: … — say if wrong.`) | `alignment:intent-lock` | Callers print exactly that line and nothing else. The Reframed/Skipped drift ends (INV intent-lock-5). | Regex grader in each caller's eval |

3. **Dependencies.** Declare `dependencies` only for same-folder plugins, which always load together: `evidence → alignment`, `visuals → alignment, evidence`, `firecrawl → alignment`. Never declare a cross-repo dependency. The probe showed an unsatisfied dependency disables the plugin (V4), so in a micky-only session the producers would vanish. Cross-repo handoffs are written `OPTIONAL: learn-hub:digest-report — if not loaded, leave the report in research-notes/ and say "run /digest-report in a Learn session"` (COM-36, COM-37).
4. **Deterministic contracts become scripts** (SKL-31, COM-16):
   - `lit-watch/scripts/sweep.py`
   - `misread-capture/scripts/ledger-append.py`
   - `visuals/scripts/check-html.mjs`
   - `plugin-creator/scripts/{validate,bump}.py`
   - `verify/scripts/*.mjs`
   - `sync:safe`

---

## 5. Evals strategy

Three layers (EVL-41), run where the owner already works.

| Layer | What | Where / when |
|---|---|---|
| 1. Static | The house `validate.py` wraps `claude plugin validate --strict` per plugin directory and for `.claude/skills` (PLG-10, SKL-49), plus the house rules. | A git pre-commit hook in both repos (`.githooks`, with `core.hooksPath` set by each repo's plugin SessionStart hook in cloud). |
| 2. Deterministic | learn-hub `npm test`, extended to run the relocated Python suite (354 cases, EVL-41). New unit tests for every new script (`sweep.py` window, pagination and dedupe; `ledger-append.py`; `check-html.mjs`; `validate.py`; `bump.py`). | Pre-commit (fast subset) and before merge. |
| 3a. Behaviour (isolated) | `claude plugin eval` cases at `plugins/<p>/evals/<skill>/<case>/` (EVL-02, EVL-06). At least 3 per skill (SKL-43). Each case has one result grader and one process grader (EVL-10). Regex graders on long reports and HTML (EVL-11, EVL-13). PubMed and CT.gov answer from `evals/mocks/<server>/<tool>.md` (EVL-24). Gate skills get pressure scenarios, e.g. "I'm in a hurry, skip the questions" (COM-28). Negatives use `tool_used: Skill min 0 max 0 arm: both` (EVL-15). | Plugins in both repos. learn-hub project skills are not documented eval targets (EVL-46), so they are covered by layers 2 and 3b. |
| 3b. Trigger collisions (live listing) | skill-creator `run_eval` about 20 queries per family, 60/40 train/validation (SKL-14 corrected, EVL-38), run **in a real multi-repo cloud session** so the real competitors are loaded: the 22 synced skills plus project skills (EVL-39). Families: gates; evidence (+ deep-research, synced psych-paper-digest, daily-random-review); visuals (+ dataviz, ingest-visual); PDF front door (+ synced pdf, bullet-reconstruct); atomize (+ obsidian-knowledge-vault). | At description rewrite, and after any model change (EVL-48). |
| Acceptance | A blind A/B of the old SKILL.md snapshot against the rewrite for holistic skills (EVL-35, EVL-30). Rewrites are verified only in fresh subagents or sessions (SKL-44). | Per rewritten skill, before merge. |
| Telemetry | `/skill-doctor` and `/doctor` on the owner's real setup, 2–4 weeks after W5 (EVL-40), to decide user-only status and retirements (lit-watch, gridgeist). | W7. |

**Migration of the 118 empty `evals.json` cases.** Mine the prompts as case seeds. Only the skeleton converts mechanically; graders are hand-written (EVL-04 corrected). Delete the files; skill-creator format is no longer used for CI (EVL-01).
**Cost control.** A smoke tag per plugin uses free graders only, 1 run, `--ablation none`. Full two-arm runs happen at wave acceptance only (EVL-27). Budget per OD10.

---

## 6. Versioning and release

- **In-place loading everywhere means the "release" is a merge to the default branch.** Sessions load whatever commit they check out (PLG-09, LOC-39). No install or update ceremony remains.
- **Semver lives in plugin.json only.** Marketplace entries carry no version (PLG-06, LOC-02). Commit-SHA versioning is rejected because `--strict` fails a plugin.json without a version (MP-PLG-1). The top-level catalog version is deleted rather than hand-bumped (INV marketplace.json-3).
- **Bump only when behaviour changes.** Use `plugin-creator/scripts/bump.py`: plugin.json plus a CHANGELOG entry in one step, dry-run by default, UTF-8, trailing newline. The validator enforces top CHANGELOG entry == version. That fixes the skipped entries: pubmed 1.3/1.4, psych-paper-digest 0.1.1, clinical-infographic 0.2.1, vault-keeper 0.3/0.4, intent-lock 0.4.1.
- **Merges and renames are recorded append-only in `renames`** (PLG-44): intent-lock / decision-interview / plan-critique → alignment; pubmed-research-note / comprehensive-review / psych-paper-digest → evidence; the four renderers → visuals; vault-keeper removed. Run `claude plugin validate` on the merge-to-one mapping first (not probed).
- **`claude plugin tag`** (PLG-39, -40) is needed only if OD5 uploads anything to claude.ai. The tag then records exactly what was uploaded.
- **learn-hub:** one plugin, versioned the same way. Project skills stay unversioned (git history). learn-hub's plugin-polish-plan P1-2 closes (LOC-30).

---

## 7. Context-budget targets (numbers)

| Always-paid item | Now (measured) | Target | Lever |
|---|---|---|---|
| Listing entries from both repos (skills + commands, all loaded) | **55 entries, 33,856 chars** (V6) | **≤ 21 model-invocable entries, ≤ 10,000 chars**; ~7 user-only (name only) | Merges; commands folded; 3 forks and source-to-vault gone; `disable-model-invocation` on maintenance skills removes their descriptions (SKL-36); soft ≤ 500 chars, hard 1,024 (SKL-05, SKL-13); key use case in the first 150 chars (SKL-07) |
| claude.ai-synced listing | 22 entries, 15,385 chars (V6) | Unchanged by this plan; the owner may turn off skills unused in Code | Project `skillOverrides` isn't read in multi-repo sessions and user settings don't reach cloud (V7), so claude.ai is the only lever |
| Listing budget | 1% of context, 8,000-char fallback (V7). Demand today ≈ 49k chars | Repo share ≤ 10k chars. Measure with `/doctor` in W0 and W7 | SKL-08 open question on units, resolved by measurement |
| Always-on plugin cost (`claude plugin details`) | micky **6,579 tok**; learn-hub native 1,455 tok (+ forks ≈ 1.5k) (V5) | micky ≤ 3,000; learn-hub ≤ 800 | As above |
| micky CLAUDE.md | 13,954 B (~3.5k tok) | ≤ 5,000 B (~1.2k tok) | Catalog removed (R6) |
| micky MEMORY.md (mandated) | 108,178 B (~27k tok) | Not mandated; living section ≤ 6 KB | R5 |
| ROUTING.md (mandated per request) | 20,197 B (~5k tok) | 0 | R4 |
| learn-hub CLAUDE.md (loads on first read of a learn-hub file, V7) | 268,390 B (~67k tok) | ≤ 32 KB (~8k tok) | G1 |
| **Total paid before work starts** | **≈ 115k tok** | **≈ 15k tok** | |
| Per-invocation bodies | intent-lock 6.2k; atomize-book 21.3k; ingest-article ~18k incl. mandatory references; ml-concept-lab 10.8k full load; firecrawl 4.2k; pubmed 4.7k + 5.9k mandatory | Gates ≤ 2k; every body ≤ 5k (inside the compaction re-attach window, SKL-40); references conditional | SKL-15, SKL-18, SKL-21 |

---

## 8. Migration waves

Each wave is developed on a branch and tested from a branch session. Master sessions keep the old tools until the merge, which the in-place loading makes free.

| Wave | Scope | Entry criteria | Exit criteria |
|---|---|---|---|
| **W0: Probe and baseline** (no content changes) | Snapshot every SKILL.md as the A/B baseline. In a live multi-repo cloud session: `/doctor`, `/skill-doctor`, `/context`, `claude plugin details` totals. Set `CLAUDE_CODE_PLUGIN_DIRS` to **micky only** (the forks would double-load otherwise, V2). Probe plugin: SessionStart writes a marker and PreToolUse(Bash) logs, to confirm plugin hooks fire in multi-repo sessions. Probe a path-scoped rule inside learn-hub. On Windows, confirm the user environment variable loads plugins, and whether user-settings `env` can set it. | OD1–OD11 answered | Probe results in `docs/delivery.md`; baseline numbers recorded; unverified items (appendix) resolved or redesigned |
| **W1: Delivery and de-duplication** | Minimal sink patch to upstream pubmed and CR: research-notes when `$LEARN_HUB_DIR` resolves, otherwise current behaviour (L2/L3 delta, LOC-33). Delete the 3 forks and source-to-vault (L1–L3, L5). Create `learn-hub/plugins/learn-hub`: move digest-report, ingest-infographic, ingest-animation (still separate), sync-vault and the hooks into it (L4, L10, F7). Move vault-atomizer, vault-vectors and pk-plasma to `.claude/skills` (L6–L8). Delete learn-hub-local (L9). Environment variables and setup script (section 2.1). Windows: set the env vars and uninstall the marketplace copies. | W0 hooks probe passed | Fresh multi-repo cloud session: `claude plugin list` shows each plugin **once**; the `session-start: ready` line is printed; `.env.local` exists; `python3 -c 'import fitz'` works; `npm run sync:apply` dry path passes the gate; a local Windows session shows the same list |
| **W2: Pipeline repair (cross-repo contracts)** | Inbox contract; `report-contract.md`; digest-report consumes `## Sources`; `audit:visual` CLI; `ingest-visual` merge (F4, F5); producers hand off through the inbox; drain micky `vault/` (7 artifacts) into research-notes; digest-report's provenance check skips already-landed items; retire vault-keeper and empty-vault (P14, S16, S17, C4) per OD2 | W1 exit | End-to-end in one multi-repo session: a pubmed report reaches research-notes → digest-report → sync → the DB count matches the provenance count; an infographic and an animation go through ingest-visual → sync → `audit:visual` passes; parity check green |
| **W3: Context diet** | micky CLAUDE.md, MEMORY and ROUTING (R2, R4, R5, R6); learn-hub G1: pipeline gotchas into skill references (a mapping table: every heading → destination, none dropped), vault format into sync-vault, app material into path-scoped rules (OD9) | W2 exit, since skill homes are now fixed | The section 7 numbers are met; `grep` finds no mandated-read lines; the gotcha mapping table is complete |
| **W4: Tooling** | plugin-creator self-contained scripts (R1, R3; S14, S15, S18); validator covers both repos; pre-commit hooks; eval scaffold template; micky `.gitignore` | W1 exit | `validate.py` green on both repos; a failing fixture proves each house rule; pre-commit runs in a cloud session |
| **W5: micky consolidation and rewrites** | Order by callers: **alignment** (S4–S7, ledger to `state/`) → **evidence** (S1–S3, one `.mcp.json`, lit-watch rename) → **visuals** (S8–S11, absorbing F11) → firecrawl (S12) → gridgeist trim. Commands folded (C1–C12). `renames` entries. For each skill: write eval cases first, run the baseline against the snapshot, rewrite, then A/B. | W4 exit; OD4, OD7, OD8 answered | Every skill: ≥ 3 cases passing at the agreed threshold; no Δ regression vs baseline in the A/B; trigger suites pass in a live session; listing targets for micky met |
| **W6: learn-hub skill rewrites** | atomize-book split (F1) and tooling relocation; ingest-article, ingest-slides, pdf-pipeline, vault-coverage, check-repetition, verify (F2, F3, F6, F8–F10) | W5 evidence and visuals merged, since the contracts are stable; **a freeze window agreed with ongoing imports** (atomize-book is the most-churned skill, LOC-46) | `npm test` includes Python; the PDF-front-door trigger suite passes; one book chapter and one article are re-run end to end without regressions in the loss, depth or figure gates |
| **W7: Hardening and telemetry** | Full two-arm eval pass; `/skill-doctor` after 2–4 weeks of use; retire or user-only as the data says (lit-watch, gridgeist); re-measure the listing | W6 exit | The decision log is updated; the final numbers are recorded in MEMORY.md (living section) |

---

## 9. Owner decisions

These are limited to questions that turn on the owner's values or environment.

| # | Question | Options | Recommendation | Trade-off |
|---|---|---|---|---|
| OD1 | How should repo plugins reach cloud and local sessions? | (a) `CLAUDE_CODE_PLUGIN_DIRS` on both surfaces, loaded in place from the clones; (b) claude.ai-synced plugin uploads; (c) keep the local marketplace install, with nothing in cloud | **(a)** | (a) has zero copies and always matches the checkout, but requires both repos to be attached to the session. A learn-hub-only session has no micky tools. (b) works without the clone and in Cowork, but every change needs a re-upload, which recreates fork drift. (c) leaves cloud, the main surface, empty. |
| OD2 | Is micky `vault/` a place you read, or a staging buffer for the Learn hub? | (a) Staging: drain it once, retire vault-keeper and empty-vault, and let the Learn inbox replace it; (b) a destination: keep vault-keeper with an env-var root, marker file and index script, and retire only the drain | **(a)** | (a) removes a 2-skill plugin, a broken handshake and non-resolving Obsidian links; you lose an Obsidian-browsable staging area. (b) keeps a second knowledge store that has to stay in sync with the app. |
| OD3 | After a report is written, what happens by default? | (a) Archive to research-notes/; publish only on "digest"/"atomize"; (b) digest and sync to live Supabase by default | **(a)** | (a) keeps live-DB writes deliberate (Supabase is shared with board-prep-hub) and matches digest-report's own contract; it costs one extra word from you. (b) is one step shorter but writes to production on every review (INV CR-fork-1). |
| OD4 | Which literature surveillance do you actually read? | (a) Keep micky's watchlist sweep, renamed `lit-watch` (user-only /lit-watch); (b) retire it in favour of learn-hub feed highlights plus the claude.ai daily digest; (c) keep the name `psych-paper-digest` and only sharpen the Not-for clauses | **(a) now, then revisit with `/skill-doctor` data in W7** | (a) removes the collision at once and keeps targeted PubMed + registry sweeps. (b) is the leanest option but loses registry watch and domain targeting. (c) leaves two same-named skills competing for "what's new". |
| OD5 | Do you want any of these tools on claude.ai (phone or Cowork)? | (a) None for now; (b) a portable build of selected skills (e.g. pubmed-research-note), uploaded as claude.ai plugins under the same name (the in-place copy then suppresses the synced one in Code sessions, V7) | **(a)** | (b) gives phone access, but each upload is a copy that needs tagging, the 6-key frontmatter limit (SKL-04) and no `!` injection (SKL-35). (a) keeps one source. |
| OD6 | Should board-prep daily reviews ever use the PubMed comprehensive-review? | (a) Never: edit `daily-random-review` on claude.ai to "follow the structure below" and add a Not-for in comprehensive-review; (b) allow it as an optional evidence update | **(a)** | The two use opposite evidence bases (textbooks with zero citations vs PubMed with a Sources contract) and write to different stores (V8). Only you can edit a synced skill. |
| OD7 | Do you invoke maintenance tools by slash command or by natural language? | (a) Mixed: producers and gates stay model-invocable, maintenance skills become user-only (vault-atomizer, vault-vectors, vault-coverage, check-repetition, pk-plasma-animation, refine-plugin, lit-watch); (b) everything model-invocable; (c) slash-first with short alias stubs (/digest, /animate …) | **(a), plus optional aliases for the 2–3 names you type daily** | User-only saves listing budget and stops accidental runs (SKL-36), but "check coverage of X" then won't auto-route; you type /vault-coverage. Aliases cost nothing in the listing when `disable-model-invocation` is set. |
| OD8 | Where does compounding personal state live (misread ledger, lit-watch config and `last_swept`)? | (a) Git-tracked `micky-psych-tools/state/` (a private repo), committed at the end of the skill; (b) `${CLAUDE_PLUGIN_DATA}` per machine | **(a)** | Cloud VMs are ephemeral, so (b) silently resets the ledger in every cloud session. (a) puts personal priors in a git history, acceptable for a private repo, and needs a commit step. |
| OD9 | How deep should the learn-hub CLAUDE.md restructure go? | (a) Move only the skill-owned material (58 pipeline gotchas, vault format); (b) also move app gotchas and "Pages" into path-scoped `.claude/rules/` | **(b), staged: (a) in W3, (b) as a follow-up** | (a) meets the skill goal with little risk to your app docs but leaves about 40k tokens always loaded. (b) reaches about 8k tokens but reorganizes the file you maintain daily. |
| OD10 | How much eval spend? | (a) Smoke per merge plus full two-arm per wave; (b) smoke only; (c) monthly full pass | **(a)** | A full two-arm pass across ~60 cases is several hundred agent runs (EVL-27). Smoke-only misses Δ regressions. |
| OD11 | Two repos, or merge micky into learn-hub? | (a) Two repos with four named interfaces (section 4); (b) a monorepo | **(a)** | (b) removes cross-repo drift by construction, but couples the portable marketplace to a deployed app and its 67k-token CLAUDE.md. (a) keeps micky reusable and costs the parity check. |

---

## 10. Risks

1. **`CLAUDE_CODE_PLUGIN_DIRS` is new (v2.1.280, V7).** An older CLI in an image or on Windows loads nothing, silently.
   - *Mitigation:* the learn-hub SessionStart hook prints `claude --version` and the list of loaded plugins on its ready line. W1 exit checks it.
2. **Plugin hooks in multi-repo sessions are documented but not probed live** (appendix U1). If they don't fire, npm install, `.env.local` and the gates are still missing.
   - *Mitigation:* W0 probe. Fallback: move the static parts into cloud env vars (Puppeteer) and the setup script (tooling), and make `sync:safe` self-heal `.env.local` from the environment.
3. **Transition double-loads.** Same-named plugins in both folders both load (V2). Renamed plugins would load beside the old installed copies on Windows.
   - *Mitigation:* strict W0/W1 ordering (micky-only path until the forks are deleted), and uninstall the Windows marketplace copies in W1.
4. **An in-place load tracks the checked-out branch.** A broken branch breaks that session's tools.
   - *Mitigation:* pre-commit validation. Plugin changes go through PRs.
5. **Cross-repo `dependencies` would disable producers** (V4).
   - *Mitigation:* the validator forbids them. Cross-repo handoffs stay optional with a fallback.
6. **Git-held state requires a commit in ephemeral VMs** (OD8). A forgotten commit loses a ledger entry.
   - *Mitigation:* the append script prints `git status` and the skill ends with a commit prompt.
7. **Renames break muscle memory** (/digest, /animate, /infographic).
   - *Mitigation:* OD7 aliases. The `renames` map covers installs.
8. **atomize-book churn collides with W6** (LOC-46).
   - *Mitigation:* a freeze window. Relocate tooling in its own PR, with the 354 tests as the guard.
9. **The listing stays over budget from synced skills alone** (15,385 chars), outside repo control.
   - *Mitigation:* collisions are fixed first, so any remaining truncation hits the least-used skills (SKL-08). The owner may turn off unused claude.ai skills.
10. **The daily-random-review collision persists until the owner edits it on claude.ai** (OD6).
    - *Mitigation:* the comprehensive-review Not-for ships in W5 regardless.
11. **MCP tool naming.** Plugin servers and the account connectors dedupe by endpoint, so the live prefix varies (MP-PLG-2).
    - *Mitigation:* skills name tools by function and accept whichever instance is live. Mocks key on the plugin's server names (EVL-24).
12. **Environment variables are visible to anyone using the environment** (V7).
    - *Mitigation:* the new variables are paths only. Keys stay as existing env vars or API credentials.

---

## Appendix: verification log (beyond the phase-1 files)

- **V1.** Loaded both clones as folders of plugins: `CLAUDE_CONFIG_DIR=<scratch> CLAUDE_CODE_PLUGIN_DIRS=/home/user/micky-psych-tools/plugins:/home/user/learn-hub/plugins claude plugin list` (2.1.280). All 14 micky and 8 learn-hub plugins load as `<name>@inline` from the clone paths.
- **V2.** Same run: `intent-lock`, `pubmed-research-note` and `comprehensive-review` each appear **twice**, both "√ loaded". Same-named plugins from two folders are not de-duplicated.
- **V3.** A nonexistent path in the list is skipped with no error, and the rest load.
- **V4.** Probe plugin with `"dependencies":["probe-b"]`, loaded alone, reports "× disabled — Dependency "probe-b" is not installed". Loaded from the same folder as probe-b, both load.
- **V5.** `claude plugin details` always-on tokens.
  - micky: vault-keeper 773, plugin-creator 721, intent-lock 655, ml-concept-lab 468, concept-animation 442, plan-critique 442, comprehensive-review 440, pubmed 432, clinical-infographic 411, psych-paper-digest 391, decision-interview 388, code-explainer 368, firecrawl 368, gridgeist 280. Total 6,579.
  - learn-hub: pk-plasma 411, digest-report 383, vault-atomizer 278, vault-vectors 217, source-to-vault 166. Total 1,455.
- **V6.** Description characters, measured with a lenient frontmatter parse.
  - micky: skills 15,953 (17), commands 1,405 (12).
  - learn-hub: plugin skills 7,146 (9), plugin commands 626 (6), project skills 8,726 (11).
  - Total 33,856 over 55 entries.
  - claude.ai-synced (`~/.claude/skills/synced`): 15,385 over 22.
- **V7.** Docs in `wf2/docs/`:
  - env-vars.md and plugins.md: `CLAUDE_CODE_PLUGIN_DIRS` loads each path like `--plugin-dir`; `:` or `;` separators; absolute paths or `~`; project and local settings can't set it; v2.1.280.
  - settings-reference.md: "set those in your shell, user settings, or managed settings".
  - cloud-environments.md:
    - Carry-over table: hooks and `.mcp.json` load only in single-repo sessions; `.claude/skills` loads; repo-enabled plugins don't; user `~/.claude` doesn't.
    - Environment variables are copied at startup and readable by any command.
    - The setup script runs before Claude Code launches and is snapshot-cached, rebuilt about every 7 days.
  - plugins-reference.md "Synced plugins": another enabled same-named plugin wins, and the synced copy is reported as not loaded.
  - skills.md:
    - Budget at 1% of context; `skillOverrides` states; `disable-model-invocation` hides the description.
    - Synced skills are download-only and are changed on claude.ai.
  - env-vars.md: `SLASH_COMMAND_TOOL_CHAR_BUDGET` falls back to 8,000 characters.
  - memory.md:
    - Subdirectory CLAUDE.md loads on demand when Claude reads files there.
    - `paths:`-scoped `.claude/rules/`.
    - "Target under 200 lines per CLAUDE.md".
  - plugins.md: folder-of-plugins semantics; `--plugin-dir` hooks load and `/reload-plugins` reloads them.
- **V8.** Synced `daily-random-review/SKILL.md`:
  - lines 12-13: "chains into the comprehensive-review and obsidian-knowledge-vault skills internally";
  - line 128: "Synthesize following the comprehensive-review structure";
  - "ZERO citations anywhere";
  - notes saved to `Finish/Micky/`.
- **V9.** `learn-hub/.claude/hooks/session-start.sh`:
  - exits unless `CLAUDE_CODE_REMOTE`;
  - `cd "$CLAUDE_PROJECT_DIR"` (which is `/home/user` in multi-repo sessions);
  - then `npm install` and `.env.local` materialization;
  - `.claude/settings.json` holds only these hooks.
- **Unverified (resolve in W0):**
  - **U1.** Plugin SessionStart and PreToolUse hooks firing in a *live* multi-repo cloud session.
  - **U2.** Whether the setup script runs before or after the repo clone. The design assumes nothing repo-dependent runs in it.
  - **U3.** Whether user-settings `env` can set `CLAUDE_CODE_PLUGIN_DIRS` on Windows. A Windows user environment variable is used instead.
  - **U4.** Path-scoped rules in a nested repo during multi-repo sessions.
  - **U5.** The `renames` merge-to-one mapping.
  - **U6.** The exact claude.ai personal plugin upload flow (only matters if OD5 is (b)).
