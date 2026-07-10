# Improve All Plugins Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix every confirmed defect across the 4 plugins (pubmed-research-note, intent-lock, plugin-creator, vault-keeper) and the shared tooling (validate.py, route.py, repo docs), sourced from a 4-agent audit run on 2026-07-10.

**Architecture:** Three waves. Wave 1 fixes shared tooling (validator, router) so later verification is trustworthy. Wave 2 fixes the two cross-plugin architecture breaks: the vault contract (pubmed bypasses vault-keeper with an incompatible layout) and the intent-lock misread-ledger path collision. Wave 3 is per-plugin polish (bloat trims, descriptions, READMEs/CHANGELOGs, evals) and a final release bump.

**Tech Stack:** Markdown (SKILL.md, commands, references), Python 3 (scripts/), JSON manifests. No test framework — verification is `python scripts/validate.py`, `python scripts/route.py`, and targeted `grep`.

**Repo root:** `C:\Users\User\Desktop\My skill\micky-psych-tools` — all paths below are relative to it. All work stops before commit approval per repo convention only where noted; otherwise commit per task (conventional commits).

---

## Wave 1 — Shared tooling

### Task 1: validate.py — fix misleading PASS message, per-skill evals, command/agent checks

**Files:**
- Modify: `scripts/validate.py:110` (message), `:112-115` (evals loop), insert new block after `:110`

- [ ] **Step 1: Fix the min-length message** (currently prints "(too short to trigger reliably)" even on PASS)

Replace line 110:
```python
                check(n >= 200, f"skills/{skill}: description {n} chars (min 200 for reliable triggering)")
```

- [ ] **Step 2: Replace the evals lookup** — current code (`:112-115`) assumes the skill dir equals the plugin name, so secondary skills (refine-plugin, misread-capture) can never have evals validated. Replace lines 112–115 with a per-skill loop folded into the existing `skills_dir` walk (add inside the `for skill in sorted(...)` loop, after the description checks):

```python
                ev = os.path.join(skills_dir, skill, "evals", "evals.json")
                if os.path.isfile(ev):
                    json.load(open(ev, encoding="utf-8"))
                    print(f"  PASS  skills/{skill}/evals/evals.json is valid JSON")
```

Delete the old block at former lines 112–115 entirely.

- [ ] **Step 3: Add command/agent frontmatter checks** (authoring-rules claims validate.py enforces agent description length — make that true). Insert after the skills block, before the evals-era blank line:

```python
        for comp in ("commands", "agents"):
            cdir = os.path.join(pdir, comp)
            if os.path.isdir(cdir):
                for fname in sorted(os.listdir(cdir)):
                    if not fname.endswith(".md"):
                        continue
                    fm = frontmatter(os.path.join(cdir, fname)) or {}
                    check(bool(fm.get("description")),
                          f"{comp}/{fname}: frontmatter description present")
                    if comp == "agents":
                        n = len(fm.get("description", ""))
                        check(200 <= n <= 1024,
                              f"agents/{fname}: description {n} chars in 200-1024")
```

- [ ] **Step 4: Verify**

Run: `python scripts/validate.py`
Expected: `all checks passed`; no line contains "too short" next to PASS; three `commands/<name>.md: frontmatter description present` lines under plugin-creator.

- [ ] **Step 5: Commit**

```bash
git add scripts/validate.py
git commit -m "fix(scripts): correct validator min-length message, per-skill evals, command/agent checks"
```

### Task 2: route.py + /route — route on "Use when" clauses, kill the broken staleness heuristic

**Files:**
- Modify: `scripts/route.py` (~`:51` and `:113` — cue selection)
- Modify: `plugins/plugin-creator/commands/route.md:23-24`
- Modify: `.claude-plugin/marketplace.json` (plugin-creator description — add /route)

- [ ] **Step 1: Add a `use_when()` extractor to route.py** near `first_sentence` (~line 51):

```python
def use_when(desc):
    """Cue for the routing table: the 'Use when...' clause if present, else first sentence."""
    m = re.search(r"[Uu]se (?:this skill |it )?when(ever)?\b(.*?)(?:\.|$)", desc)
    if m:
        return ("when" + (m.group(1) or "") + m.group(2)).strip() + "."
    return first_sentence(desc)
```

Then replace every `first_sentence(desc)` call used for the Quick-index cue column (audit found it at the cue build, ~`:113`, and inside `components`, ~`:51` region) with `use_when(desc)`. Read the surrounding code before editing — line numbers may have drifted.

- [ ] **Step 2: Verify regeneration quality**

Run: `python scripts/route.py && grep -n "pre-build alignment gate" ROUTING.md`
Expected: no match — intent-lock's row now shows its "Use when" trigger clause, not "A pre-build alignment gate."

- [ ] **Step 3: Fix the /route staleness heuristic.** In `plugins/plugin-creator/commands/route.md:23-24`, delete the "if ROUTING.md ... looks stale versus marketplace.json" condition and replace with:

```markdown
Before consulting the table, always run `python scripts/route.py` first — it is
idempotent and cheap, and it is the only way to pick up edited skill descriptions
(which change ROUTING.md without touching marketplace.json).
```

- [ ] **Step 4: Add /route to the catalog description.** In `.claude-plugin/marketplace.json`, plugin-creator entry, extend the description's final clause:

```
...bumps and validates; /route regenerates ROUTING.md and routes a request to the owning skill or command.
```

- [ ] **Step 5: Verify + commit**

Run: `python scripts/validate.py` → `all checks passed`.
```bash
git add scripts/route.py plugins/plugin-creator/commands/route.md .claude-plugin/marketplace.json ROUTING.md
git commit -m "fix(plugin-creator): route on Use-when clauses; always regenerate before routing"
```

---

## Wave 2 — Cross-plugin architecture

### Task 3: Canonical vault contract (vault-keeper side)

Decision (locked): **one canonical layout owned by vault-keeper; pubmed-research-note delegates saving/indexing and keeps only its note-content schema.** This makes the "single place any skill's output is saved" claim true instead of downgrading it.

**Files:**
- Create: `plugins/vault-keeper/skills/vault-keeper/references/vault-layout.md`
- Modify: `plugins/vault-keeper/skills/vault-keeper/SKILL.md`
- Create: `plugins/vault-keeper/README.md`, `plugins/vault-keeper/CHANGELOG.md`
- Create: `plugins/vault-keeper/skills/vault-keeper/evals/evals.json`

- [ ] **Step 1: Write the shared layout reference** `references/vault-layout.md` — the single file both plugins cite:

```markdown
# Canonical vault layout (single source of truth)

Vault root: the `vault/` directory beside `.claude-plugin/marketplace.json` at the
marketplace repo root. NEVER a `vault/` relative to the current working directory.

Resolve it: walk up from cwd to the directory containing `.claude-plugin/marketplace.json`,
then append `vault/`. From inside a plugin, `${CLAUDE_PLUGIN_ROOT}/../../vault` is equivalent.
Use the resolved ABSOLUTE path in every Glob/Grep/Read/Write.

Tree (fixed — no free-form top-level folders):
  vault/index.md          # master index — every MOC listed
  vault/MOCs/<Topic> MOC.md
  vault/notes/<Concept — Qualifier>.md
  vault/artifacts/<kebab-slug>.md
  vault/assets/

Naming: MOC files are `<Topic> MOC.md` (not `MOC — <Topic>`). Notes use
`Concept — Qualifier` title case. Artifacts kebab-case.

Collision rule: if the derived filename exists and is NOT the same topic being
extended, disambiguate with ` -2`, ` -3`… — never overwrite.

MOC membership: every note reachable from exactly one MOC. Multi-topic notes declare
`primary-moc:` in frontmatter; that MOC wins, other MOCs may link but index checks
only the primary. Index regeneration is a pure rebuild, alphabetical by title;
orphans are REPORTED, never moved.

"Populated" (skip init): `vault/index.md` exists. `.gitkeep`-only dirs do not count
as content.
```

- [ ] **Step 2: Rewire vault-keeper SKILL.md.** Edits, in place:
  1. Add a **Step 0 — Locate the vault** section at the top of the workflow, quoting the resolve rule above and stating every subsequent path op uses the absolute path.
  2. Replace the inline tree (~`:29-35`) and naming/collision/index rules with pointers to `references/vault-layout.md` (keep one-line summaries).
  3. Frontmatter description: change opening noun phrase to action-first — `"Files, indexes, links, and retrieves any skill's output in the shared vault at the marketplace repo root (vault/)..."` (keep existing triggers/Not-for).
  4. `created:` date rule (~`:47`, `:86`): add "obtain today's date from the environment context (`currentDate`) or ask; if neither, omit the field rather than guess."
  5. init guard (~`:60-62`): replace "missing or empty" with the "Populated" definition from the layout reference.

- [ ] **Step 3: Sync manifests.** Align `plugin.json` and marketplace.json entry: same description wording, same keyword list (add `moc` to marketplace entry).

- [ ] **Step 4: Add README.md** (the integration contract other plugin authors call — init/save/index/query, the layout reference path, the handoff rule: "producer skills output content + target type (note/artifact/MOC); vault-keeper owns paths, dedup, index wiring") **and CHANGELOG.md** seeded:

```markdown
# Changelog — vault-keeper
## 0.2.0 — 2026-07-10
- Step 0 vault resolution (absolute path from marketplace root; fixes wrong-cwd writes)
- Canonical layout extracted to references/vault-layout.md; collision + index determinism rules
- Integration contract README; pubmed-research-note now delegates vault writes here
## 0.1.0
- Initial: single skill, init/save/index/query
```

- [ ] **Step 5: Add evals** `skills/vault-keeper/evals/evals.json` — 6 cases: (1) save routes note vs artifact correctly and wires a MOC; (2) query-before-save prevents duplicate; (3) init skipped when index.md exists; (4) refuses to author missing content, hands back; (5) save from non-root cwd still targets repo-root vault; (6) slug collision disambiguates instead of overwriting. Follow the shape of `plugins/pubmed-research-note/skills/pubmed-research-note/evals/evals.json` (id, prompt, expected_behavior fields).

- [ ] **Step 6: Verify + commit**

Run: `python scripts/validate.py` → `all checks passed` (evals line appears for vault-keeper).
```bash
git add plugins/vault-keeper .claude-plugin/marketplace.json
git commit -m "feat(vault-keeper): vault resolution step, canonical layout reference, contract docs, evals"
```

### Task 4: pubmed-research-note — Claude Code paths + vault handoff

**Files:**
- Modify: `plugins/pubmed-research-note/skills/pubmed-research-note/SKILL.md` (`:96-104`, `:195-202`)
- Modify: `plugins/pubmed-research-note/skills/pubmed-research-note/references/atomic-note-template.md` (`:16-19`, `:98-107`)

- [ ] **Step 1: Replace sandbox-only runtime modes** (`SKILL.md:96-104`). New text:

```markdown
## Where output goes
1. **Claude Code (default):** write the report into the working directory
   (or `report_dir` from `.pubmed-research-note.json` if present).
2. **Vault mode (only on request):** hand the finished note content to the
   vault-keeper skill — it owns paths, dedup, MOC wiring, and the index. Pass:
   note title (`Concept — Qualifier`), body, and suggested MOC topic. Never
   write into `vault/` directly from this skill.
3. **No filesystem:** render inline and say explicitly that nothing was written.
```

Delete every mention of `/mnt/user-data/outputs` and `present_files` (also at `:202`); if a claude.ai-sandbox branch is worth keeping, mark it "sandbox only — not Claude Code" in one line.

- [ ] **Step 2: Gut the duplicated vault logic in atomic-note-template.md.** Remove the `vault_dir`/`<Folder>`/dedup-grep mechanics (`:16-19`, `:98-107`); keep the note CONTENT schema (frontmatter fields, section order, wikilink style) and add one line: "Placement, filenames, dedup, and MOC wiring are owned by vault-keeper — see `plugins/vault-keeper/skills/vault-keeper/references/vault-layout.md`."

- [ ] **Step 3: Verify no orphaned references**

Run: `grep -rn "mnt/user-data\|present_files\|vault_dir" plugins/pubmed-research-note/`
Expected: no matches (or only the single flagged "sandbox only" line).

- [ ] **Step 4: Commit**

```bash
git add plugins/pubmed-research-note
git commit -m "fix(pubmed-research-note): drop sandbox-only paths; delegate vault writes to vault-keeper"
```

### Task 5: intent-lock — repair the misread-ledger loop

**Files:**
- Modify: `plugins/intent-lock/skills/misread-capture/SKILL.md:40,58` (+ any other `references/misreads.md` mention)
- Modify: `plugins/intent-lock/skills/intent-lock/references/misreads.md:5-6` (header ownership rules)
- Modify: `plugins/intent-lock/README.md` ("The ledger" section)

- [ ] **Step 1: Point misread-capture at the real ledger.** In `misread-capture/SKILL.md`, replace every `references/misreads.md` with the explicit cross-skill path:

```
${CLAUDE_PLUGIN_ROOT}/skills/intent-lock/references/misreads.md
```

Add one sentence: "This is the SAME file intent-lock reads at Phase 0 — there is exactly one ledger; never create a `references/` dir under misread-capture."

- [ ] **Step 2: Align the ledger header.** In `misreads.md:5-6`, mirror the skill's exact line-ownership: Claude appends `Asked for` / `Got` / `when`; `Axis missed` and `Prior` are verbatim-user. Add: "Active-priors line must be copied verbatim from the entry's `Prior:` at append time; retire past 7."

- [ ] **Step 3: Update README ledger section** to name the single canonical path and that misread-capture appends / intent-lock reads.

- [ ] **Step 4: Verify**

Run: `grep -rn "misreads.md" plugins/intent-lock/`
Expected: every hit resolves to `skills/intent-lock/references/misreads.md`; `plugins/intent-lock/skills/misread-capture/references/` does not exist.

- [ ] **Step 5: Commit**

```bash
git add plugins/intent-lock
git commit -m "fix(intent-lock): single canonical misread ledger path across both skills"
```

---

## Wave 3 — Per-plugin polish

### Task 6: intent-lock — docs truth + version history

**Files:**
- Modify: `plugins/intent-lock/README.md:7,34-35,42`
- Modify: `plugins/intent-lock/CHANGELOG.md`
- Modify: `plugins/intent-lock/.claude-plugin/plugin.json:6`

- [ ] **Step 1:** README:34-35,42 — replace `mickky-plugins` → `micky-psych-tools` (both the `marketplace add` slug and `intent-lock@...`).
- [ ] **Step 2:** README:7 — replace `Ends with \`GOAL UNIFIED.\` and the work, in the same turn` with `Ends silently with the work in the same turn — GOAL UNIFIED is a private gate, never printed` (matches SKILL.md:24,202,252).
- [ ] **Step 3:** CHANGELOG — add a `## 0.3.0` section describing what actually shipped between 0.2.0 and 0.3.0 (read `git log --oneline -- plugins/intent-lock` to reconstruct; the silent-gates refactor commit `ce8461c` is the likely content — if 0.2.0's entry already describes it, retitle that entry 0.3.0 and write an honest thinner 0.2.0).
- [ ] **Step 4:** plugin.json:6 — `"Thanawat Suharit (Mickky)"` → `"Thanawat Suharit (Micky)"`.
- [ ] **Step 5:** Commit: `git add plugins/intent-lock && git commit -m "docs(intent-lock): fix marketplace slug, silent-gate claim, 0.3.0 changelog, author spelling"`

### Task 7: intent-lock — trim SKILL bloat, sharpen triggers, add evals

**Files:**
- Modify: `plugins/intent-lock/skills/intent-lock/SKILL.md` (266 lines — target ≤ ~170)
- Create: `plugins/intent-lock/skills/intent-lock/references/failure-conditions.md`
- Modify: `plugins/intent-lock/skills/misread-capture/SKILL.md:3`
- Create: `evals/evals.json` under both skills

- [ ] **Step 1:** Move the exhaustive failure-conditions list (`:236-266`) to `references/failure-conditions.md`; keep the 5 highest-stakes ones inline (never print GOAL UNIFIED; never propose a better version; never emit a portable prompt; never ask permission after unify; work in same turn) + a pointer.
- [ ] **Step 2:** Collapse repeated silent-gate exposition (stated at `:16-24`, `:95`, Phase 2, failure list) to ONE canonical statement in the header; elsewhere reference it ("gates are silent — see header").
- [ ] **Step 3:** Frontmatter: change opening to third person (`Interrogates a request until it has exactly one reading, then executes it as written.`) and append a Not-for clause: `Not for quick throwaway requests, already-precise specs, or capturing a past misread after delivery (that is misread-capture).`
- [ ] **Step 4:** misread-capture frontmatter: append `Not for mid-interview corrections (intent-lock handles those live) and never drafts the diagnosis itself — the two capture questions are answered verbatim by the user.`
- [ ] **Step 5:** Evals: intent-lock — 5 positive triggers (incl. Thai) + 3 negatives that must NOT fire (a precise one-liner request; "you wasted my time" post-delivery → misread-capture; a /new-plugin request). misread-capture — its verbatim triggers + negative: mid-interview tell.
- [ ] **Step 6:** Verify: `python scripts/validate.py` → all pass, evals lines appear for both skills. Commit: `refactor(intent-lock): dedup silent-gate prose, extract failure list, Not-for clauses, evals`

### Task 8: pubmed-research-note — reference hygiene + docs + evals

**Files:**
- Modify: `skills/pubmed-research-note/SKILL.md:3-6,59-94`
- Modify: `references/tool-catalog.md:4,9-10,86`
- Modify: `.claude-plugin/plugin.json` + marketplace entry
- Modify: `skills/pubmed-research-note/evals/evals.json`
- Create: `plugins/pubmed-research-note/README.md`, `CHANGELOG.md`

- [ ] **Step 1:** Collapse the "Pairing with intent-lock" body section (`:59-94`) to ~4 lines: division of labour, the 3 chain conditions, pointer to `references/intent-lock-pairing.md`. Delete duplicated detail from the body (the reference already holds it).
- [ ] **Step 2:** tool-catalog.md: (a) `:86` — state Open Library is web-fallback only, no MCP server wired in `.mcp.json`; delete the `mcp__open-library__` preferred-path claim; (b) `:9-10` — split prefix guidance: bundled servers use the stable `mcp__plugin_pubmed-research-note_pubmed__*` / `mcp__plugin_pubmed-research-note_clinical-trials__*` prefixes (no ToolSearch hunt needed); only external managed connectors have session-varying hash prefixes.
- [ ] **Step 3:** Frontmatter description: `Answer` → `Answers` (third person); trim ~100 chars from the trigger list (drop the weakest 2–3 near-duplicate triggers) to regain headroom under 1024; soften `The sole entry point for literature research` (`:6`) → `The entry point for decision-driven biomedical literature research` (consistent with the psych-paper-digest / deep-research carve-outs).
- [ ] **Step 4:** Marketplace entry: append the chaining clause from plugin.json (`Chains to the intent-lock plugin when the request carries no decision.`) so catalog matches manifest.
- [ ] **Step 5:** evals.json: renumber ids contiguously 1–15; add eval 16: no-filesystem branch → renders inline and states nothing was written; add eval 17: vault mode → hands off to vault-keeper instead of writing paths itself.
- [ ] **Step 6:** Add README.md (purpose, 4 decision frames, MCP setup incl. the two bundled servers, `.pubmed-research-note.json` schema: `{ "report_dir": "<path>" }`) and CHANGELOG.md reconstructing 0.1.0 → 1.1.1 → 1.2.0 from `git log --oneline -- plugins/pubmed-research-note`.
- [ ] **Step 7:** Verify: `python scripts/validate.py` all pass; `grep -c "Use when\|use when" plugins/pubmed-research-note/skills/pubmed-research-note/SKILL.md` ≥ 1. Commit: `docs(pubmed-research-note): fix tool-catalog claims, dedup pairing section, third-person description, README/CHANGELOG, eval coverage`

### Task 9: plugin-creator — truth-align rules/checklist, templates, dedup

**Files:**
- Modify: `skills/plugin-creator/references/authoring-rules.md:1,28-34`
- Modify: `skills/refine-plugin/references/audit-checklist.md`
- Modify: `skills/plugin-creator/SKILL.md:39,84-104`
- Modify: `skills/refine-plugin/SKILL.md:44,70-90`
- Modify: `skills/plugin-creator/references/templates/SKILL.md:3`
- Create: `skills/plugin-creator/references/templates/evals.json`
- Create: `plugins/plugin-creator/README.md`, `CHANGELOG.md`

- [ ] **Step 1:** authoring-rules.md — after Task 1 made validate.py actually check agent descriptions, keep the `[BLOCKER] mechanical` tier for agent length but re-verify the "Distilled from scripts/validate.py" claim holds for every rule listed; move any rule validate.py still doesn't check into an explicitly-labeled quality tier.
- [ ] **Step 2:** audit-checklist.md — add checks: commands have `description` + `argument-hint` and reference `$ARGUMENTS` where they take input; every declared command/skill appears in the catalog description; ROUTING.md regenerated after any frontmatter edit; README + CHANGELOG exist per plugin.
- [ ] **Step 3:** plugin-creator SKILL.md:39 — replace the hardcoded `(currently research, productivity)` with "offer the distinct `category` values read from marketplace.json at runtime."
- [ ] **Step 4:** Dedup the router-refresh + stop-before-commit prose duplicated across `plugin-creator/SKILL.md:84-104` and `refine-plugin/SKILL.md:70-90`: in each, one line — `Regenerate the router: python scripts/route.py (never hand-edit ROUTING.md). Stage changes and stop before commit for user approval.` Delete the duplicated rationale paragraphs.
- [ ] **Step 5:** templates/SKILL.md:3 — move the authoring recipe OUT of the `description:` value into a comment block above the frontmatter; leave the value as a short `{{one-line action-first description with Use-when and Not-for clauses, 200-1024 chars}}` placeholder. Add `templates/evals.json` (2-case skeleton: one positive trigger, one negative).
- [ ] **Step 6:** Add plugin README.md (three commands + two skills, what each does) and CHANGELOG.md (0.1.0 scaffold-only → 0.2.0 refine+route → 0.3.0 this task).
- [ ] **Step 7:** Verify: `python scripts/validate.py` all pass. Commit: `refactor(plugin-creator): truth-align rules with validator, checklist gaps, template fixes, dedup router prose`

### Task 10: Repo docs — CLAUDE.md + README refresh

**Files:**
- Modify: `CLAUDE.md` (Layout, Workflow, Plugins sections)
- Modify: `README.md:54-64`

- [ ] **Step 1:** CLAUDE.md Layout — add `scripts/route.py`, `ROUTING.md (generated)`, and `vault/ (shared knowledge vault — owned by vault-keeper)` lines.
- [ ] **Step 2:** CLAUDE.md Workflow — insert step between validate and bump: `Regenerate the router: python scripts/route.py (any frontmatter description change alters ROUTING.md).`
- [ ] **Step 3:** CLAUDE.md Plugins — update plugin-creator blurb (2 skills, 3 commands incl. /route); add vault-keeper entry (one line: shared vault manager — init/save/index/query; other plugins delegate vault writes to it).
- [ ] **Step 4:** README.md Plugins section — list all four plugins with one-liners; de-hardcode install/bump examples or show one generic `<plugin>` example.
- [ ] **Step 5:** Commit: `docs: refresh CLAUDE.md and README for router, vault, and all four plugins`

### Task 11: Release — bump everything, regenerate, final validate

**Files:**
- Modify (via script): every `plugin.json` + `marketplace.json` version pair; `ROUTING.md`

- [ ] **Step 1:** Bump (behavioral changes → minor):

```bash
python scripts/bump.py pubmed-research-note minor   # 1.1.1 -> 1.2.0
python scripts/bump.py intent-lock minor            # 0.3.0 -> 0.4.0
python scripts/bump.py plugin-creator minor         # 0.2.0 -> 0.3.0
python scripts/bump.py vault-keeper minor           # 0.1.0 -> 0.2.0
```

- [ ] **Step 2:** Bump marketplace `version` in `.claude-plugin/marketplace.json` to `1.3.0` (bump.py does not touch it).
- [ ] **Step 3:** Ensure every CHANGELOG top entry matches the new version numbers (Tasks 3, 6, 8, 9 wrote them — fix any that predicted a different number).
- [ ] **Step 4:** `python scripts/route.py && python scripts/validate.py`
Expected: `all checks passed`; ROUTING.md rows show Use-when cues for all skills.
- [ ] **Step 5:** Final commit:

```bash
git add -A
git commit -m "chore: release pubmed 1.2.0, intent-lock 0.4.0, plugin-creator 0.3.0, vault-keeper 0.2.0"
```

---

## Deliberately dropped (audited, judged not worth doing)

- Splitting vault-keeper into 4 skills — audit confirmed single-skill is correct (shared layout rules, query runs inside save).
- Optional `/vault-index` slash command — YAGNI until index runs prove annoying to trigger.
- Eval id 8 archaeology in pubmed evals — renumbering (Task 8) supersedes it.

## Execution order constraint

Task 1 → Task 2 → Task 3 → Task 4 (depends on 3's layout reference) → Tasks 5–10 in any order → Task 11 last.
