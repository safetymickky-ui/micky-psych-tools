# Spec S16: ingest-visual (merge), the audit:visual CLI, and pk-plasma-animation

| Field | Value |
|---|---|
| Repos | learn-hub |
| Units (today → target) | `ingest-infographic`+`ingest-animation` → `.claude/skills/ingest-visual` (kinds `infographic`,`animation`,`explorable`); `npm run audit:visual` (new CLI over existing pure audits); `plugins/pk-plasma-animation` (+`/pk-animation`,`.mcp.json`) → `.claude/skills/pk-plasma-animation` (dmi) + alias `/pk-animation` |
| Waves | W1 (YAML fixes on the two skills as they stand today, H30, `/visualization` route fix); W2 (`ingest-visual` merge with refuse-and-return, H29/H31; `audit:visual` CLI; pk-plasma-animation conversion) |
| Owner decisions assumed | OD5-a (n/a directly — no report publishing here), OD9-a (pk-plasma-animation keeps a short alias, `/pk-animation`), OD10-a (pk-plasma-animation user-only/dmi; `ingest-visual` stays model-invocable, not in OD10's user-only list) |
| Defects closed | 19 of 19 assigned (HIGH: H29, H31; ingest-infographic-2 = H30) |
| Interfaces owned | I08 |
| Interfaces consumed | I01 (owner S01), I04 (owner S03), I05 (owner S03), I07 (owner S05), I09 (owner S15), I10 (owner S15), I13 (owner S13), I17 (owner S12), I21 (owner S21), I22 (owner S21) |
| Depends on specs | S05 (I07: the document/layout contract `audit:visual` implements — read §2.7 I07-H/G/E first); S15 (I09/I10: the inbox `visuals/` layout and intake log) |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| Path | Lines | Bytes | Est. tokens | Role |
|---|---|---|---|---|
| `.claude/skills/ingest-infographic/SKILL.md` | 152 | — | — | rewritten into `ingest-visual`'s infographic kind |
| `.claude/skills/ingest-animation/SKILL.md` | 139 | — | — | rewritten into `ingest-visual`'s animation/explorable kinds |
| `plugins/pk-plasma-animation/.claude-plugin/plugin.json` | 18 | — | — | retired this wave |
| `plugins/pk-plasma-animation/.mcp.json` | 12 | — | — | deleted (R41 duplicate endpoint; runtime resolution per I05) |
| `plugins/pk-plasma-animation/commands/pk-animation.md` | 22 | — | — | retired; becomes a project command (§2.1) |
| `plugins/pk-plasma-animation/skills/pk-plasma-animation/SKILL.md` | 133 | — | — | the skill body being rewritten |
| `.../references/{drug-config,parameter-fitting,pubmed-research-plan}.md` | 94/—/109 | — | — | kept, lazily loaded (fix -4) |
| `scripts/lib/animation-responsive.mjs` | 183 | — | — | exports `auditAnimationSelfContained`, `auditAnimationLayout` |
| `scripts/lib/infographic-responsive.mjs` | 166 | — | — | exports `auditInfographicResponsive` |
| `src/lib/animation-layout.ts`, `infographic-html.ts` | 107/26 | — | — | app-side RUNTIME guards, not audits (§1.4) |
| `scripts/animations/pk-plasma/*.mjs` (18 files) | — | — | — | shared engine; stays in place (T2/§4.6) |
| `scripts/animations/mph-plasma/*.mjs` (7 files) | — | — | — | reference build; unaffected |

Measured (`measure.py skill`): ingest-infographic `description.chars=933`; ingest-animation `description.chars=963`. No `evals/` directory under any of the three units — nothing to convert (§4.2).

### 1.2 Descriptions

| Skill | Chars | UTF-8 bytes | YAML valid? | `Use when` offset | `Not for`? | Quoted trigger phrases |
|---|---|---|---|---|---|---|
| ingest-infographic (today) | 933 | — | **no** — ScannerError at col 296 (INV -6) | ~330 | yes | "ingest this infographic", "add this infographic to the hub", "file this infographic HTML" |
| ingest-animation (today) | 963 | — | **no** — ScannerError at col 320 (INV -4) | ~340 | yes | "ingest this animation", "add this animation to the hub", "file this animation HTML" |
| pk-plasma-animation (today) | — (plugin desc, not a skill desc) | — | n/a | n/a | n/a | — |

Both YAML errors share a shape: an unquoted `description` containing a bare colon (`` `type: infographic` sidecar ``) breaks `yaml.safe_load` at that point — R2.

### 1.3 Defects

| id | sev | H# | evidence (re-opened) | problem | fix step | wave |
|---|---|---|---|---|---|---|
| ingest-infographic-1 | H | H29 | SKILL.md:3, :137-138 "waits for" | dead producer/caller contract — empty-vault (S07) never hands assets over directly | S16-W2-3, S16-W2-4 (rewrite to I09/I10, then delete the old skill; CX-60 — closure, not S16-W2-2 alone) | W2 |
| ingest-infographic-2 | H | H30 | SKILL.md:116-118 "equivalent to a full `npm run sync`"; ingest-article SKILL.md:306 "does NOT publish" | wrong claim: `npm run sync` writes no rows at all | S16-W1-1 (delete; point at I13) | W1 |
| ingest-infographic-3 | M | — | SKILL.md:17-18 "the only edits allowed" vs :79 "Two mechanical normalisations" | internal contradiction on the edit count | S16-W1-1 (one count, "two") | W1 |
| ingest-infographic-4 | M | — | SKILL.md:11, :133 "`/infographic`"; `CLAUDE.md` "301-redirects" to `/visualization` | stale app route | S16-W1-1 (rewrite both mentions) | W1 |
| ingest-infographic-5 | M | — | SKILL.md:45 "Run digest-report … FIRST"; absent from a default session | missing-topic fallback names a skill not guaranteed loaded | S16-W1-1 (OPTIONAL-with-fallback, §2.6) | W1 |
| ingest-infographic-6 | L | — | YAML ScannerError col 296 | invalid strict YAML | S16-W1-1 (quote/fold) | W1 |
| ingest-animation-1 | H | H31 | SKILL.md:3, :123-125 "waits for" | same dead contract as ingest-infographic-1 | S16-W2-3, S16-W2-4 (rewrite to I09/I10, then delete the old skill; CX-60) | W2 |
| ingest-animation-2 | M | — | SKILL.md:88-98 checks only self-contained+reduced-motion then "Make no other change"; `CLAUDE.md` calls stage-collapse and quirks-mode universal defects | the sanity check misses both; "no other change" conflicts with "fix at source when touched" | S16-W2-2, S16-W2-3 (`audit:visual` runs both, refuse-and-return) | W2 |
| ingest-animation-3 | M | — | SKILL.md:54-55 "run digest-report" | same availability issue as -5 above | S16-W1-2 (OPTIONAL-with-fallback) | W1 |
| ingest-animation-4 | L | — | YAML ScannerError col 320 | invalid strict YAML | S16-W1-2 (quote/fold) | W1 |
| pk-plasma-animation-1 | M | — | SKILL.md:112-114 "prefer a targeted upsert … mirrors `apply-sync.mjs`'s animation path"; no script exists | asks Claude to hand-build an upsert, bypassing the audits unless reimplemented | S16-W2-4 (files via `ingest-visual` instead) | W2 |
| pk-plasma-animation-2 | M | — | `pubmed-research-plan.md:91` `` `<title> (<year>) — <DOI>` ``; I04 (S03) forbids titles/years | the brief contradicts the skill it is handed to; the reference report followed the brief, not the contract | S16-W2-4 (rewrite Sources to I04's grammar) | W2 |
| pk-plasma-animation-3 | M | — | SKILL.md:51-54 "Run pubmed-research-note", no fallback | hard-depends on a sibling not guaranteed installed | S16-W2-4 (OPTIONAL-with-stop, R58) | W2 |
| pk-plasma-animation-4 | L | — | SKILL.md:15-22 "Read, before anything else" + 3 refs, unconditionally | eager loading on every invocation, even rebuild | S16-W2-4 (conditional loads, §2.4) | W2 |
| pk-plasma-animation-5 | L | — | `pubmed-research-plan.md:36-38` "the web engine" — undefined | undefined term | S16-W2-4 (name firecrawl/WebFetch, I05) | W2 |
| pk-plasma-animation-6 | L | — | SKILL.md:117 "open `/animation/<id>`" — no mechanism named | app check names no auth/verify mechanism | S16-W2-4 (name `verify`, OPTIONAL) | W2 |
| pk-plasma-animation-7 | L | — | SKILL.md:88-90 names `report-fidelity.test.mjs`; real file is `pk-engine.test.mjs` | wrong filename | S16-W2-4 (correct it) | W2 |
| pk-plasma-animation-8 | L | — | `.mcp.json:3-10` identical to 2 siblings; session has PubMed/CT connectors already | duplicate MCP declarations (P4, R41) | S16-W2-1 (delete) | W2 |
| pk-plasma-animation-9 | L | — | `plugin.json:6,8` name+license drift from digest-report's | author metadata drift | S16-W2-6 (moot — plugin retires here) | W2 |

All 19 defects appear once. No deferrals.

### 1.4 Other findings

- **OBS "executable truth is in another repo."** The three pure audits plus the app's `enforceAnimationLayout`/`neutralizeInfographicColorScheme` guards already exist; no plugin ships a `scripts/` dir. `audit:visual` wraps the three audits rather than reimplementing them. **NEW**: the two app-side files are runtime DEFENSE-IN-DEPTH guards (they rewrite stored HTML), not audits with codes — `audit:visual` never calls them; its doctype/color-scheme static checks are new code (§2.5).
- **OBS filing pipeline incoherence.** Resolved structurally by S07 (empty-vault → `drain_plan.py`, I12) and this spec (`ingest-visual` reads I09, no direct empty-vault call). Nothing further needed beyond removing the dead-handshake text.
- **OBS description budget.** ingest-infographic (933) and ingest-animation (963) sit near the 1,024 cap; the merged `ingest-visual` targets 985 — not a concatenation of both.
- **NEW.** `.claude/commands/` does not exist in learn-hub today. No established alias mechanism for a project skill's short slash form exists; this spec creates one file for `/pk-animation` (§2.1, §8 — a design choice, not prior art).
- **NEW.** `scripts/animations/{pk-plasma,mph-plasma}/` already sit outside any plugin directory, so converting pk-plasma-animation from a plugin (where calling them would violate R44) to a project skill (T2) resolves the tension without moving a file.

## 2. Target state

### 2.1 Location and tree (after W2)

```
.claude/skills/ingest-visual/
  SKILL.md
  references/kind-normalisation.md   # light-lock + mobile-strip CSS, infographic-only
.claude/skills/pk-plasma-animation/
  SKILL.md                           # dmi: true
  references/{drug-config,parameter-fitting,pubmed-research-plan}.md
.claude/skills/pk-animation/
  SKILL.md                           # dmi alias skill (CX-24; I20's alias template, not a commands/ file)
scripts/
  audit-visual.mjs                   # CLI (I08)
  lib/audit-visual.mjs               # pure: static checks + aggregation
  lib/audit-visual.test.mjs
  audit-visual-render.mjs            # puppeteer render/drive (impure)
scripts/animations/{pk-plasma,mph-plasma}/   # UNCHANGED (T2, §4.6)
.claude/skills/ingest-infographic/   # DELETED
.claude/skills/ingest-animation/     # DELETED
plugins/pk-plasma-animation/         # DELETED
```

### 2.2 Frontmatter

**`ingest-visual`:**
```yaml
---
name: ingest-visual
description: >-
  Files a finished, self-contained HTML visual asset — infographic, animation, or
  explorable — into the Learn hub's infographics or animations table: audits it,
  refusing and returning any failure to the author rather than silently fixing it. Use
  when the user says "ingest this infographic", "ingest this animation", "add this
  infographic to the hub", "add this animation to the hub", "file this HTML asset", or
  research-notes/visuals/ holds an un-filed item. Reads research-notes/visuals/ (a
  .meta.json-described item) or a direct call from pk-plasma-animation; writes the type:
  infographic|animation sidecar plus the sibling HTML into the target topic directory,
  then syncs via sync-vault. Not for markdown reports (digest-report), PDFs
  (pdf-pipeline/ingest-article), books (atomize-book), slide decks (ingest-slides), or
  code-explainer output (no vault receiver) — input is a finished self-contained HTML
  document; output is an infographics or animations row, never notes or articles.
---
```
Measured: 985 chars / 991 UTF-8 bytes / ~246 tokens. `use_when_at`: 240 (within R4's ~250). `not_for_at`: 690.

**`pk-plasma-animation`:**
```yaml
---
name: pk-plasma-animation
description: >-
  Builds a "one molecule, N curves" plasma-level-by-delivery-technology animation for a
  drug with several release technologies, then files it into the Learn hub. Use when the
  user says "/pk-animation methylphenidate", "animate atomoxetine's plasma curves",
  "plasma level by formulation for lisdexamfetamine", "make the drug version of the
  methylphenidate animation", or asks to rebuild an existing drug directory under
  scripts/animations/. Runs a PubMed-sourced pharmacokinetic research report (via
  pubmed-research-note, OPTIONAL, stops if absent), fits a one-compartment model with one
  input function per technology, drives the shared scene-by-scene simulator template,
  verifies it headless at the app's real frame sizes, then files it via ingest-visual.
  Not for a concept animation without a PK simulator (concept-animation), infographics
  (clinical-infographic), or notes (digest-report) — the deliverable is a filed
  animations row built on measured pharmacokinetics, not a markdown report.
disable-model-invocation: true
argument-hint: "<drug or drug-dir> [--report research-notes/<slug>.md]"
---
```
Measured: 990 chars / 992 UTF-8 bytes / ~248 tokens. `use_when_at`: 160. No `<`/`>` in the description (`argument-hint` is a separate key, exempt). Per OD10-a, `dmi: true` removes it from the listing; `argument-hint` keeps it self-documenting when typed directly.

### 2.3 Body outline

**`ingest-visual`** (merges ingest-infographic 152 lines + ingest-animation 139 lines; target ≤220 lines / ≤2,800 tokens — under the sum of the two originals, since the shared steps 1/4/5 stop being duplicated):

| # | Section | Source → disposition |
|---|---|---|
| 1 | Intro + filer rule | both intros → merge, one paragraph; state the `infographics`/`animations` table split once |
| 2 | Kind — pick the right table | ingest-animation:19-29 "Animation vs infographic" → keep verbatim, the kind-router both skills need |
| 3 | Input | both §Input → merge; add explorable (ml-concept-lab output, same `type: animation` shape, per I07-A) |
| 4 | Step 1 — Resolve the topic | both step-1 → merge verbatim (identical logic in both originals) |
| 5 | Step 2 — Run `audit:visual`; refuse-and-return (CX-41 — audit BEFORE filing, not after: architecture §5.5 forbids ever filing an asset whose audit fails, and a refused asset left in `/vault` publishes on the next unrelated sync) | **new**, replaces ingest-infographic's light-lock/strip prose (moved to `references/kind-normalisation.md`, infographic-only) and ingest-animation's self-contained/reduced-motion prose (now inside `audit:visual`'s static checks). On `verdict: "fail"` the skill writes the `refused` I10 line, returns every `issues[].message`+`fix` to the author, and STOPS — nothing is written into `/vault`, and the HTML is never edited (fixes ingest-animation-2: mechanical normalisation stays for infographics only, everything else is refuse-and-return) |
| 6 | Step 3 — File the sidecar + HTML (only once step 2 passed) | both step-2 → merge; one shared sidecar table, `type:` column switches |
| 7 | Step 4 — Sync | both step-4 → merge; delete the "targeted upsert = `npm run sync`" claim (fix -2/H30); point at `sync-vault` (I13) only |
| 8 | Step 5 — Verify, log, report | both step-5 → merge the SQL; **replace** the dead empty-vault sentence with: write one `.intake-log.jsonl` line (I10) after verification succeeds |
| 9 | Guardrails | both → merge, dedupe |

**`pk-plasma-animation`** (133 lines today; target ≤150 lines / ≤2,600 tokens — a project skill, not a sub-step other skills invoke, so no R11 ≤2,000-token gate cap):

| # | Section | Source lines → disposition |
|---|---|---|
| 1 | Intro + prime directive | 6-30 → keep verbatim |
| 2 | Reference loading | 15-22 → **rewrite** conditional: "Before Step 1 read `pubmed-research-plan.md`; before Step 2 `parameter-fitting.md`; before Step 3 `drug-config.md`" (fix -4) |
| 3 | Step 0 — Lock the question | 32-47 → keep; name `intent-lock`'s (bare name, CX-16) OPTIONAL-with-fallback handoff (I01, §2.6) |
| 4 | Step 1 — Research report | 49-58 → **rewrite**: `pubmed-research-note` OPTIONAL-with-stop (fix -3) — "if absent, stop; a PK brief needs sourced numbers it cannot supply itself." Fix "web engine" (fix -5) to name firecrawl/WebFetch, I05. |
| 5 | Step 2 — Fit the model | 60-73 → keep verbatim |
| 6 | Step 3 — Drug directory | 75-90 → keep; fix test filename to `pk-engine.test.mjs` (fix -7) |
| 7 | Step 4 — Build | 92-97 → keep verbatim |
| 8 | Step 5 — Verify | 99-106 → keep verbatim |
| 9 | Step 6 — File, sync, verify, revalidate | 108-117 → **rewrite**: replace the hand-built targeted upsert (fix -1) with "File via `ingest-visual` — it audits, writes the sidecar, delegates to `sync-vault`. Never upsert `animations` directly." Name `verify` OPTIONAL for the app check (fix -6). |
| 10 | Report back | 119-123 → keep |
| 11 | Guardrails | 125-133 → keep, add "Sources lines follow I04's grammar, never title/year" |

### 2.4 References

| File | Purpose | Load condition | Size target |
|---|---|---|---|
| `ingest-visual/references/kind-normalisation.md` | light-lock + mobile-strip CSS, infographic-only, ported from ingest-infographic §3 | "Before step 3, if `kind: infographic`" | ≤800 tok |
| `pk-plasma-animation/references/pubmed-research-plan.md` | PK research brief | "Before Step 1" | ≤1,500 tok (Sources section trimmed, I04) |
| `pk-plasma-animation/references/parameter-fitting.md` | fit-engine types/tolerances | "Before Step 2" | unchanged |
| `pk-plasma-animation/references/drug-config.md` | drug directory field reference | "Before Step 3" | unchanged |

### 2.5 Scripts

**Owned: `audit:visual` (I08).**

| Name | CLI | Input | JSON stdout shape | Exit codes | Tests |
|---|---|---|---|---|---|
| `scripts/audit-visual.mjs` | `npm run audit:visual -- <file> [--kind infographic\|animation\|explorable] [--static-only] [--shots <dir>] [--json]`; `--help` | path to a self-contained HTML document | `{"file":"…","kind":"infographic\|animation\|explorable","verdict":"pass\|fail","issues":[{"code":"…","tier":"static\|render\|drive","message":"…","fix":"…"}],"frames":[{"viewport":"360x780","frame":"344x608","stageOk":true,"clipped":[],"overflowPx":0}],"skipped":["render","drive"]}` (`frames`/`skipped` only when relevant) | `0` pass (`issues` empty); `1` fail (≥1 issue); `2` usage error (bad path, `--kind` omitted and ambiguous) | `audit-visual.test.mjs` (static tier, pure); the render tier is exercised by S16-W2-8's real-Chromium run — not vitest (OQ13-a dropped S05's parity fixture) |

**`--kind` inference** (omitted, per I07-E hooks): `.stage`+`#play`/`#step`/`#stepCount` → `explorable`; `.stage-wrap`+`#playBtn`/`#nextBtn`/`#restartBtn`/`#indicator` → `animation`; neither, `:root{color-scheme:light}` → `infographic`. Ambiguous → exit `2`.

**Degrade rule.** If Chromium is unresolvable (same check `ready.mjs`, I13, performs), only the static tier runs, a stderr warning fires, `"skipped":["render","drive"]`, and the exit code reflects the static verdict only — never a false overall pass. `--static-only` requests this (a sandboxed eval run with no browser grant).

**`--shots <dir>`** (OQ13-a): writes one PNG per rendered frame (and, for an animation, per scene hold) into `<dir>`. `check-html.mjs` passes it through, since it no longer renders itself.

**Rule ids — I07-H (owner S05), reproduced verbatim, not redefined:**

> Static (all unless noted): `no-doctype`, `no-lang`, `no-color-scheme`, `no-painted-ground`, `external-reference`, `no-reduced-motion` (anim/explorable — code-explainer's own copy of this rule is checked by its own port, S06's `check-html.mjs`, never through this CLI's `--kind`, CX-10). Infographic-only static: `color-scheme-not-light`, `prefers-color-scheme-dark`, `strip-cramps`. Anim/explorable-only static: `children-can-shrink`, `stage-can-collapse`. Render: `no-wrap`/`no-stage`/`no-controls` (3 codes), `stage-collapsed`, `child-clipped`/`children-overlap` (2 codes), `controls-below-fold`, `horizontal-overflow`, `page-error`. Drive: `drive-hooks-missing`; animation `scene-walk-stuck`/`restart-not-scene-1` (2 codes); explorable `step-counter-off`, `self-check-failing`, `non-finite-on-screen`. 26 codes total (F2: 6 + 3 + 2 + 9 + 6 — the paragraph's own list sums to 26, not 21); each `fix` names the concrete repair.

**Implementation mapping:**

| Code(s) | Backed by |
|---|---|
| `external-reference`, `no-reduced-motion` | `auditAnimationSelfContained` — anim/explorable only through this CLI; code-explainer never passes `--kind code-explainer` here (CX-10) — its own copy of the same rule runs through `check-html.mjs`'s code-explainer static check (OQ13-a) |
| `children-can-shrink`, `stage-can-collapse` | `auditAnimationLayout` — anim/explorable only |
| `strip-cramps` | `auditInfographicResponsive` — infographic only |
| `no-doctype`, `no-lang`, `no-color-scheme`, `no-painted-ground`, `color-scheme-not-light`, `prefers-color-scheme-dark` | **new** static regex checks (no existing pure module covers these); the last two are infographic-only |
| Render tier | **new** — puppeteer at the 5 I07-G viewports, `.wrap`/`.stage`/`.deck` box per kind, I07-G's frame formula and limit table unaltered |
| Drive tier | **new** — puppeteer clicks `#playBtn`/`#nextBtn`/`#restartBtn` (animation) or `#play`/`#step`/`#reset`+reads `#stepCount`/`[data-check][data-pass]` (explorable), per I07-E |

**Pure vs impure split** (R63/R68): `scripts/lib/audit-visual.mjs` holds the static tier — pure, string-in/JSON-out. `scripts/audit-visual-render.mjs` holds puppeteer render+drive — impure, exercised by S16-W2-8's real-Chromium run (§4.4), not vitest.

**pk-plasma-animation's own scripts (unchanged):** `scripts/animations/pk-plasma/{build,fit,new-drug,verify}.mjs`; its step 6 calls `ingest-visual` instead of a nonexistent targeted-upsert script (§2.3).

### 2.6 Handoffs

- **`ingest-visual`'s missing-topic fallback** (replaces -5/-3's unconditional "run digest-report"): "Run `digest-report` (OPTIONAL). If not available, stop and tell the user the target topic must be created first — never invent a topic or attach to an unrelated one."
- **`pk-plasma-animation`'s research handoff** (OPTIONAL-with-STOP, not a broadest-reading fallback — R58's "names how to enable the dependency" branch, since a PK brief cannot proceed without sourced numbers): "Run `pubmed-research-note` (OPTIONAL) with this plugin's research plan as the brief. If not available, stop: a PK animation needs measured pharmacokinetic anchors, and fabricating them is never acceptable — enable `evidence:pubmed-research-note` or supply `--report`."
- **`pk-plasma-animation`'s filing handoff**: "File via `ingest-visual` (REQUIRED — same repo, always available). Never write an `animations` row directly."
- **`pk-plasma-animation`'s intent-lock handoff** (I01, S01, copied verbatim with the bare skill name — CX-16: a learn-hub skill has no W3 rename step, so `intent-lock` resolves before and after S01's own W3 rename, PLG-17; `alignment:intent-lock` would not): "Run `intent-lock` (OPTIONAL). If not available — or its picker is absent — do not stall: take the broadest reading and open with `Assumed: <reading> — say if wrong.`"

### 2.7 Interfaces

#### Owned: I08 — `npm run audit:visual`

Full definition in §2.5: CLI shape, `--kind` inference, degrade rule, JSON schema, exit codes, the 21 rule ids (verbatim from I07-H), the implementation mapping, and the pure/impure script split. Consumers: S05's `visuals:concept-animation`/`ml-concept-lab`/`clinical-infographic` call it through `$LEARN_HUB_DIR` before filing (S05 §2.7 I07-K); S05's `check-html.mjs` runs a static subset and delegates the rest here; without learn-hub it returns `incomplete` (OQ13-a).

#### Consumed

| Interface | Owner | What this spec assumes |
|---|---|---|
| I01 | S01 | The OPTIONAL-with-fallback sentence (§2.6) and `Assumed:` grammar, carried verbatim into pk-plasma-animation's Step 0. |
| I04 | S03 | The `## Sources` grammar `pubmed-research-plan.md` must match exactly — no title/year form (fix -2). Confirmed against S03's own I04 text, not redefined here. |
| I05 | S03 | The runtime MCP resolution sentence, in place of the deleted `.mcp.json` and the "web engine" reference (fix -5, -8). |
| I07 | S05 | The full HTML artifact contract (I07-A…J) is S05's; `audit:visual` (I08) implements it without altering any value. **Confirmed**: S05's own §2.7 already assumes this exact CLI/JSON/exit-code shape (not open, §8). |
| I09 | S15 | Paths + `.meta.json` fields + slug/collision rule. `ingest-visual` is the sole reader/writer of this half of the inbox. |
| I10 | S15 | `ingest-visual` writes `action: "filed"` (success, `rows: 1`) after verification, or `action: "refused"` (`audit:visual` failed, `rows: 0`) immediately, no sync attempted. |
| I13 | S13 | `ingest-visual`'s step 4 carries S13's exact CX-17 handoff sentence instead of restating the procedure: "Publish through the `sync-vault` skill (same repo, always present). Follow its steps as written; do not restate them here." |
| I17 | S12 | Case layout, tags, trigger regex — same as S15's I17 row. |
| I21 | S21 | Animation/infographic gotchas stay owned by their skills' `references/`, not duplicated here beyond §2.3 step 6's one-line pointer. |
| I22 | S21 | Adds `"audit:visual": "node scripts/audit-visual.mjs"` to `package.json`, at S16-W2-2 itself (CX-25) — confirmed as the step id in S21's I22 registry, not deferred to S21's own pass. |

## 3. Change steps

### S16-W1-1 — Fix ingest-infographic in place (YAML, H30, route, contradiction)

- **Repo · depends on**: learn-hub · none
- **Files**: edit `.claude/skills/ingest-infographic/SKILL.md`
- **Change**: quote/fold the description (fix -6); delete SKILL.md:116-118's "targeted upsert = `npm run sync`" claim, point at `sync-vault` (fix -2/H30); rewrite `/infographic` → `/visualization` (fix -4); reconcile "only edit" vs "two normalisations" to "two" (fix -3).
- **Commands**: `python3 measure.py skill .claude/skills/ingest-infographic/SKILL.md`
- **Done when**: `yaml_valid: true`; `grep -c "equivalent to a full" .claude/skills/ingest-infographic/SKILL.md` → 0; `grep -c "/infographic\`" .claude/skills/ingest-infographic/SKILL.md` → 0 (only `/visualization` remains).
- **Rollback**: `git checkout HEAD~1 -- .claude/skills/ingest-infographic/SKILL.md`.

### S16-W1-2 — Fix ingest-animation in place (YAML)

- **Repo · depends on**: learn-hub · none
- **Files**: edit `.claude/skills/ingest-animation/SKILL.md`
- **Change**: quote/fold the description to fix the YAML ScannerError (fix -4).
- **Commands**: `python3 measure.py skill .claude/skills/ingest-animation/SKILL.md`
- **Done when**: `yaml_valid: true`.
- **Rollback**: `git checkout HEAD~1 -- .claude/skills/ingest-animation/SKILL.md`.

### S16-W2-1 — Write the pure static-audit module and its tests

- **Repo · depends on**: learn-hub · none (parallel with W2-2/3)
- **Files**: create `scripts/lib/audit-visual.mjs`, `scripts/lib/audit-visual.test.mjs`
- **Change**: import the three existing audits, normalise each into `{code, tier: "static", message, fix}`; add the six new static checks per §2.5's mapping table. Test fixtures are **inline HTML strings in this test file** (CX-31 — not a read of S05's fixture file, which `npm test` here must never depend on the micky checkout to reach): one clean shape, and the two I07-J bad shapes (`bad-animation`: doctype-less, no `color-scheme`/painted ground, `.wrap{height:100dvh}` with no `min-height` floor; `bad-infographic`: `prefers-color-scheme:dark` block present) reproduced as literal strings matching I07-J's own description.
- **Commands**: `npx vitest run scripts/lib/audit-visual.test.mjs`
- **Done when**: passes against the inline fixtures' static codes only (clean → `[]`; `bad-animation` → the 6 named codes; `bad-infographic` → the 3 named codes, I07-J). No cross-tool parity check exists (OQ13-a).
- **Rollback**: `git rm scripts/lib/audit-visual.mjs scripts/lib/audit-visual.test.mjs`.

### S16-W2-2 — Write the CLI and the render/drive pass

- **Repo · depends on**: learn-hub · S16-W2-1, S19-W1-4 (CX-39 — same-file `package.json` edit order)
- **Files**: create `scripts/audit-visual.mjs`, `scripts/audit-visual-render.mjs`; edit `package.json` (CX-25); edit `README.md` (one script-table row for `audit:visual`; critique F12)
- **Change**: implement the CLI per §2.5 (`--kind`, `--static-only`, `--shots`, `--json`, `--help`, degrade rule, exit codes); the render/drive pass drives puppeteer at the 5 I07-G viewports and the I07-E DOM hooks. Add `"audit:visual": "node scripts/audit-visual.mjs"` to `package.json` (I22, CX-25) — this is the entry S05's `check-html.mjs` delegates through via `npm run -s audit:visual`.
- **Commands**:
  ```
  node scripts/audit-visual.mjs --help
  node scripts/audit-visual.mjs vault/tms-principles/tms-electromagnetic-induction.html --json
  npm run -s audit:visual -- --help
  ```
  (CX-31: `vault/tms-principles/…` — the generated, committed vault file — not `.claude/skills/concept-animation/examples/…`, which S05-W2-8 deletes later in the same wave.)
- **Done when**: `--help` exits 0 with no file writes; the example-file run exits 0 or 1 with a well-formed JSON object on stdout (no exception); `npm run -s audit:visual -- --help` exits 0.
- **Rollback**: `git rm scripts/audit-visual.mjs scripts/audit-visual-render.mjs`.

### S16-W2-3 — Write the merged ingest-visual SKILL.md

- **Repo · depends on**: learn-hub · S16-W2-2 (the skill's step 3 names `audit:visual`, which must exist first for its own smoke eval to run against a real binary)
- **Files**: create `.claude/skills/ingest-visual/SKILL.md`, `.claude/skills/ingest-visual/references/kind-normalisation.md`
- **Change**: assemble per §2.2/§2.3/§2.4/§2.6.
- **Commands**: `python3 measure.py skill .claude/skills/ingest-visual/SKILL.md`
- **Done when**: `description.chars` ≤ 1,024; `use_when_at` ≤ 250; `body_est_tokens` ≤ 2,800; a manual grep confirms no "empty-vault … waits for" sentence survives.
- **Rollback**: `git rm -r .claude/skills/ingest-visual`.

### S16-W2-4 — Delete ingest-infographic and ingest-animation

- **Repo · depends on**: learn-hub · S16-W2-3
- **Files** / **Change**: `git rm -r .claude/skills/ingest-infographic .claude/skills/ingest-animation`
- **Commands**: `ls .claude/skills | grep -E 'ingest-infographic|ingest-animation'` (expect empty)
- **Done when**: the command above prints nothing; `.claude/skills/ingest-visual/SKILL.md` still exists.
- **Rollback**: `git checkout HEAD~1 -- .claude/skills/ingest-infographic .claude/skills/ingest-animation`.

### S16-W2-5 — Write the rewritten pk-plasma-animation project skill

- **Repo · depends on**: learn-hub · S16-W2-3 (its filing step names `ingest-visual`)
- **Files**: create `.claude/skills/pk-plasma-animation/SKILL.md` + ported `references/{drug-config,parameter-fitting,pubmed-research-plan}.md` (Sources line rewritten per fix -2); create `.claude/skills/pk-animation/SKILL.md` (CX-24 — a dmi alias skill from I20's alias template, not a `.claude/commands/` file: `disable-model-invocation: true`, body `Invoke pk-plasma-animation with: $ARGUMENTS`)
- **Change**: assemble per §2.2/§2.3/§2.4/§2.6.
- **Commands**: `python3 measure.py skill .claude/skills/pk-plasma-animation/SKILL.md`
- **Done when**: `disable_model_invocation: true`; `description.chars` ≤ 1,024; `grep -c "★ · <title>" .claude/skills/pk-plasma-animation/references/pubmed-research-plan.md` → 0 (old Sources form gone); `.claude/skills/pk-animation/SKILL.md` exists with `disable-model-invocation: true` and no `.claude/commands/` directory is created.
- **Rollback**: `git rm -r .claude/skills/pk-plasma-animation .claude/skills/pk-animation`.

### S16-W2-6 — Retire the pk-plasma-animation plugin

- **Repo · depends on**: learn-hub · S16-W2-5
- **Files** / **Change**: `git rm -r plugins/pk-plasma-animation`
- **Commands**: `ls plugins | grep -c pk-plasma-animation` (expect 0)
- **Done when**: `ls plugins/pk-plasma-animation` fails; `.claude/skills/pk-plasma-animation/SKILL.md` exists.
- **Rollback**: `git checkout HEAD~1 -- plugins/pk-plasma-animation`.

### S16-W2-7 — Evals

- **Repo · depends on**: learn-hub · S16-W2-3, S16-W2-5
- **Files** / **Change**: create `evals/ingest-visual/<case>/…`, `evals/pk-plasma-animation/<case>/…` — the cases from §4.1 (full + table-only)
- **Commands**: `bash scripts/eval-project-skill.sh ingest-visual --smoke` (and the same for `pk-plasma-animation`; CX-46)
- **Done when**: every grader passes (no `pre-rewrite` baseline exists for either — never loaded, §1.1).
- **Rollback**: `git rm -r evals/ingest-visual evals/pk-plasma-animation`.

### S16-W2-8 — Confirm audit:visual against a real Chromium in a cloud session

Executor step, not OWNER (critique P15, C2-29): a cloud session has Chromium.

- **Repo · depends on**: learn-hub · S16-W2-2
- **Files** / **Change**: record the run against H29/H31 in learn-hub `docs/rewrite/baseline.md` `## Owner records` (the W2 tag step closes the rows in `h-coverage.md`; CX-27 — not `docs/rewrite/delivery-log.md`, which is for environment/plugin-delivery rows only); no skill change, a verification run.
- **Commands**: with `PUPPETEER_EXECUTABLE_PATH` set (I16), `npm run audit:visual -- vault/tms-principles/tms-electromagnetic-induction.html --json` (CX-31)
- **Done when**: `frames` is populated (render tier ran, not skipped).
- **Rollback**: n/a (read-only).

## 4. Evals

### 4.1 Cases

**Case 1 — ingest-visual trigger positive + refuse-and-return** (`evals/ingest-visual/refuse-bad-animation/`)

`prompt.md`:
```markdown
---
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill, Bash]
tags: [trigger, output]
env:
  EVAL_SKIP_RENDER: "1"
---

File this animation into the hub: fixtures/bad-animation.html
```

`case.yaml`:
```yaml
schema_version: "1.1"
name: refuse-bad-animation
tags: [trigger, output]
context:
  add_dirs: [fixtures]
```

`fixtures/bad-animation.html` (the I07-J `bad-animation` shape: doctype-less, `.wrap{height:100dvh}`, no color-scheme/painted ground):
```html
<div class="wrap"><style>
.wrap{height:100dvh;display:flex;flex-direction:column}
.stage-wrap{flex:1 1 auto;min-height:0}
</style>
<div class="stage-wrap"><svg class="stage"></svg></div>
<div class="controls"><button id="playBtn">Play</button><button id="nextBtn">Next</button>
<button id="restartBtn">Restart</button><span id="indicator">1 / 3</span></div></div>
```

`graders/skill-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?ingest-visual"'
weight: 2
---
```

`graders/refused-not-filed.md`:
```markdown
---
type: llm
focus: last_message
criteria: >-
  PASS if the response reports the animation was REFUSED and names at least one
  concrete issue (missing doctype, color-scheme, or the stage-collapse defect), without
  claiming it was filed or synced. FAIL if it claims success or silently "fixes" the HTML.
weight: 3
---
```

`graders/no-sync.md`:
```markdown
---
type: tool_used
tool: Bash
input_match: 'sync:apply|npm run sync'
min: 0
max: 0
arm: both
---
```

**Case 2 — near-miss negative from the sibling family** (`evals/ingest-visual/near-miss-digest-report/`)

`prompt.md`:
```markdown
---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
tags: [negative]
---

Digest this report into vault notes: research-notes/some-review.md
```

`graders/not-ingest-visual.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?ingest-visual"'
min: 0
max: 0
arm: both
---
```

**Case 3 — process: audit runs before any sidecar write** (`evals/ingest-visual/audit-before-write/`)

`prompt.md`:
```markdown
---
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write]
tags: [process]
---

Ingest this infographic into the hub: fixtures/good-infographic.html, topic
existing-topic-id
```

`case.yaml`:
```yaml
schema_version: "1.1"
name: audit-before-write
tags: [process]
context:
  scaffold_script: fixture.sh
  add_dirs: [fixtures]
```

`fixture.sh` (creates the target topic the infographic attaches to):
```bash
#!/usr/bin/env bash
set -euo pipefail
mkdir -p vault/existing-topic-id
cat > vault/existing-topic-id/_topic.md << 'EOF'
id: existing-topic-id
type: topic
title: Existing Topic
domain: Psychiatry
description: A pre-existing topic for the fixture.
icon: "🧠"
color: "#16a34a"
order: 1
status: active
created: 2026-09-01
updated: 2026-09-01
EOF
```

`graders/audit-before-write.md`:
```markdown
---
type: tool_order
before: { tool: Bash, input_match: 'audit-visual|audit:visual' }
after: Write
---
```

**Further cases (table only):**

| Name | Skill | Tags | Prompt gist | Graders |
|---|---|---|---|---|
| `ingest-good-infographic` | ingest-visual | output | File a clean infographic fixture (passes `audit:visual`) | `tool_used: Skill`; `regex` on the sidecar for `type: infographic` |
| `explorable-routes-to-animations` | ingest-visual | output | File an ml-concept-lab explorable fixture | `regex` on the sidecar for `type: animation` (I07-A) |
| `pk-animate-trigger` | pk-plasma-animation | trigger | "/pk-animation atomoxetine" | `tool_used: Skill` `input_match: '"skill"\s*:\s*"(?:[\w-]+:)?pk-plasma-animation"'` |
| `pk-animate-no-pubmed-stop` | pk-plasma-animation | negative, process | Same prompt, `pubmed-research-note` absent | `llm`: PASS if the run stops, names the missing dependency, invents nothing |
| `pk-animate-near-miss-concept-animation` | pk-plasma-animation | negative | "animate the concept of neuroplasticity" (no PK simulator) | `tool_used: Skill` pk-plasma-animation, `min:0 max:0 arm:both` |

### 4.2 Conversion

No `evals.json` or eval directory exists under any of the three units today (§1.1). Nothing to convert.

### 4.3 Live triggers

Family (architecture §6.3): `{clinical-infographic, concept-animation, ml-concept-lab, code-explainer, dataviz}` — `ingest-visual`/`pk-plasma-animation` are FILERS for this family's output, not members, so they get their own near-miss set:

1. "digest this report into notes" → `digest-report`, not `ingest-visual`
2. "animate the concept of dopamine reward prediction error" → `concept-animation`, not `pk-plasma-animation`
3. "make an infographic for this report" → `clinical-infographic` (which PRODUCES the asset), not `ingest-visual`
4. "/pk-animation methylphenidate" → true positive, `pk-plasma-animation`

### 4.4 Commands

| Command | What |
|---|---|
| `bash scripts/eval-project-skill.sh ingest-visual --smoke` | smoke run (CX-46) |
| `bash scripts/eval-project-skill.sh pk-plasma-animation --smoke` | smoke run (CX-46) |
| `npx vitest run scripts/lib/audit-visual.test.mjs` | static-tier unit tests |
| `node scripts/audit-visual.mjs <file> --json` | manual single-file audit |
| `npm run audit:visual -- vault/tms-principles/tms-electromagnetic-induction.html --json` with `PUPPETEER_EXECUTABLE_PATH` set (S16-W2-8) | render tier against a real Chromium (OQ13-a: no parity smoke) |

## 5. Acceptance criteria

1. `.claude/skills/ingest-visual/SKILL.md` and `.claude/skills/pk-plasma-animation/SKILL.md` both exist and `claude plugin validate --strict` (on `.claude/skills`) reports no error for either.
2. `.claude/skills/ingest-infographic`, `.claude/skills/ingest-animation`, `plugins/pk-plasma-animation` do not exist.
3. `node scripts/audit-visual.mjs --help` exits 0 with no file writes.
4. `npx vitest run scripts/lib/audit-visual.test.mjs` passes, against the inline `clean`/`bad-animation`/`bad-infographic` fixtures defined in the test file itself (§3, S16-W2-1, CX-31 — not a read of S05's fixture file).
5. Running `audit:visual` against a `bad-animation`-shaped fixture returns exactly the 6 codes I07-J names; against a `bad-infographic`-shaped fixture, exactly the 3 codes.
6. `ingest-visual`'s eval case `refuse-bad-animation` shows no `sync:apply`/`npm run sync` Bash call when the fixture fails audit (§4.1).
7. `grep -c "empty-vault.*waits for" .claude/skills/ingest-visual/SKILL.md` → 0.
8. `grep -c "★ · <title>" .claude/skills/pk-plasma-animation/references/pubmed-research-plan.md` → 0; the file's Sources line matches I04's grammar instead.
9. `.mcp.json` does not exist under `.claude/skills/pk-plasma-animation/` or anywhere pk-plasma-animation's directory used to be.
10. `pk-plasma-animation`'s frontmatter carries `disable-model-invocation: true`.
11. `.claude/skills/pk-animation/SKILL.md` exists, has `disable-model-invocation: true`, and `.claude/commands/` is not created by this spec (CX-24).

## 6. Trigger lock

| Phrase | Source | Kept / moved / removed |
|---|---|---|
| "ingest this infographic" | ingest-infographic desc | kept → `ingest-visual` |
| "add this infographic to the hub" | ingest-infographic desc | kept → `ingest-visual` |
| "ingest this animation" | ingest-animation desc | kept → `ingest-visual` |
| "add this animation to the hub" | ingest-animation desc | kept → `ingest-visual` |
| "file this infographic HTML" / "file this animation HTML" | both | merged into "file this HTML asset" (§2.2) — a per-kind phrasing was not shown to add coverage |
| "/pk-animation \<drug\>" | pk-plasma-animation command (today) | kept, concrete drug names substituted per R3; the slash form now fires the `pk-animation` dmi alias skill, not a `commands/` file (CX-24, §2.1) |
| "animate \<drug\>'s plasma curves" / "plasma level by formulation for \<drug\>" / "make the \<drug\> version of the methylphenidate animation" | pk-plasma-animation desc (today) | kept, concrete examples substituted |

## 7. Risks and OD sensitivity

- **Risk**: `audit:visual`'s render/drive tiers need a headless Chromium the eval sandbox may not grant. Mitigation: `--static-only` (§2.5) keeps the static tier usable with only read-only tools; render/drive verification stays a real-app step (OWNER action, §3).
- **Risk**: reusing the three existing audits directly means a future export-shape change silently changes `audit:visual`'s output. Mitigation: `audit-visual.test.mjs` pins the normalised `{code, tier, message, fix}` shape, so a drift fails the test, not silently.
- **OD9 sensitivity.** Under OD9-b, `.claude/commands/pk-animation.md` is deleted and the skill is invoked as `/pk-plasma-animation` directly; nothing else changes. Under OD9-c the skill directory itself would be renamed — out of scope for the assumed OD9-a.
- **OD10 sensitivity.** Under OD10-b, `pk-plasma-animation` drops `dmi` and joins a live trigger family (likely with `concept-animation`) — its description already partially provides the R8 Not-for tightening that would need.

## 8. Open questions

- **CLOSED (CX-24).** `/pk-animation` is a dmi alias skill (`.claude/skills/pk-animation/SKILL.md`, I20's template), matching how S20 gives `vault-vectors` its `/vectors` alias — not a `.claude/commands/` file, which has no established prior art in learn-hub (§1.4) and is not how any other short-verb alias in this rewrite is built.
- **ASSUMES** (I13, S13): the Chromium-resolution check `audit-visual.mjs`'s degrade rule reuses is S13's `ready.mjs`; if the real function differs in name/shape, the degrade detection should call it directly rather than reimplementing the probe. Settled by S13's §2.5.
- **CLOSED (CX-25).** `package.json`'s `audit:visual` line is added by S16-W2-2 itself (not deferred to S21); S21's I22 registry names S16-W2-2 as the step id, confirmed.
- **ARCH-CONFLICT**: none. I07-H's code list is reproduced verbatim from S05's spec, since S05 owns I07; the code count is corrected to 26 (F2, §2.5) rather than re-derived independently.
- **NOTE (CX-55).** pk-plasma-animation is not loaded today, so no W1 step is needed for it — all 9 of its defects close in the W2 rewrite (§1.3). An earlier third W1 placeholder step (no files, no commit) is dropped; a step with nothing to commit is not a step (one step = one commit).
