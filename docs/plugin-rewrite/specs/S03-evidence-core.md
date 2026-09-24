# Spec S03: evidence family shell and pubmed-research-note

| Field | Value |
|---|---|
| Repos | micky-psych-tools (`/home/user/micky-psych-tools`) |
| Units (today → target) | `plugins/pubmed-research-note` → interim rewrite in place (**W2**), then `plugins/evidence/skills/pubmed-research-note` (**W3**, after S10's move). New family files at `plugins/evidence/` root, **W3**: `.mcp.json`, `references/{report-contract,engines}.md`, `scripts/sources_lint.py`(+tests), `evals/mocks/{pubmed,clinical-trials}/*.md`, `evals/fixtures/report-*.md`. |
| Waves | W0 (smoke seeds, CX-4); W2 (preface → single `Assumed:` line, OPTIONAL fallbacks, runtime MCP resolution, sink filing, gate word "digest", `contract: report/1`); W3 (family files, 6-slot brief fix, dedupe, size targets, mocks, fixtures, eval conversion, description pass) |
| Owner decisions assumed | OD3-a (family merge in W3), OD5-a (publish/digest only on the explicit word), OD13-a (no claude.ai upload) |
| Defects closed | 14 of 14 assigned (HIGH: H44, H45) |
| Interfaces owned | I04, I05 |
| Interfaces consumed | I01 (owner S01), I09 (owner S15), I11 (owner S07), I17 (owner S12), I20 (owner S08), I23 (owner S10) |
| Depends on specs | S01 (I01), S04 (sibling `evidence` skills share this plugin), S07 (I11), S08 (I20, validator), S10 (I18 W0 tooling, I23 move), S11 (I16), S12 (I17), S15 (I09, I25) |

## 1. Current state (measured 2026-09-24)

Read in full: every file under `plugins/pubmed-research-note/`; CR's and psych-paper-digest's `.mcp.json` (both `diff`-identical to this plugin's — confirms P4's "6 byte-identical copies"); `learn-hub/plugins/digest-report/skills/digest-report/SKILL.md`; the 3 real reports in `learn-hub/research-notes/`; live schemas `mcp__PubMed__search_articles` and `mcp__Clinical_Trials__search_trials` (to ground I05 in actual args, not prose).

### 1.1 Files

Paths relative to `plugins/pubmed-research-note/`.

| Path | Lines | Bytes | Est. tokens | Role |
|---|---|---|---|---|
| `.claude-plugin/plugin.json` | 16 | 687 | 172 | manifest, version 1.7.0 |
| `.mcp.json` | 12 | 236 | 59 | `pubmed` + `clinical-trials` HTTP servers |
| `CHANGELOG.md` | 98 | 7,080 | 1,770 | jumps 1.5.0 → 1.2.0 (defect-7) |
| `README.md` | 107 | 5,484 | 1,371 | install + config docs |
| `skills/pubmed-research-note/SKILL.md` | 320 | 20,185 | 4,692 (body) | the skill |
| `.../references/decision-brief.md` | 120 | 7,410 | 1,838 | 6-slot anatomy, "first four/last three" contradiction (H45) |
| `.../references/intent-lock-pairing.md` | 96 | 5,400 | 1,342 | stale vs intent-lock 0.4.2 (H44) |
| `.../references/report-craft.md` | 140 | 8,316 | 2,056 | shape + depth guide |
| `.../references/tool-catalog.md` | 157 | 8,137 | 2,013 | hardcoded MCP prefixes (defect-5), 2nd NCT form (defect-8) |
| `.../references/atomic-note-template.md` | 121 | 5,171 | 1,278 | contradicts Sources rule + vault-keeper's target-type slot (defect-3) |
| `skills/pubmed-research-note/evals/evals.json` | 141 | 14,598 | — | 17 cases, `assertions: []` (defect-13) |

Mandatory refs (decision-brief + report-craft + tool-catalog) = 1,838+2,056+2,013 = **5,907 tok**, matching architecture's "5.9k" exactly; body 4,692 tok matches "4.7k". `intent-lock-pairing.md` is pointed to but not marked "read before"; `atomic-note-template.md` is conditional.

### 1.2 Descriptions

`measure.py skill`: 1,007 chars (98.3% of the 1,024 cap), 252 tok, YAML valid. `Use when` at char 225 (within R4's ~250-char band, not broken); `Not for` at 788. Quoted triggers (incl. Thai): "research", "what does the literature say about", "search PubMed for", "is X true", "should I use X for Y", "หางานวิจัย", "ทบทวนหลักฐาน", "ค้น PubMed", "จริงหรือเปล่า", plus the gate words "just search", "atomize", "ทำโน้ต" and "comprehensive review of X". No first/second person. **R3 violation (NEW):** the description carries process/output-mechanics clauses R3 forbids — "ALWAYS runs intent-lock FIRST...", "Default: write...show...file...atomize...", "Engines: PubMed, ClinicalTrials.gov, Open Library, Wikipedia, Firecrawl" — ~340 of the 1,007 chars.

### 1.3 Defects

| id | sev | H# | evidence (re-opened) | problem | fix step | wave |
|---|---|---|---|---|---|---|
| pubmed-research-note-1 | H | H44 | SKILL.md:256-269 `Reframed:`/`Skipped:` preface vs intent-lock SKILL.md:202,226 "no preface block"/"no Reframed line" | Stale vs installed gate | S03-W2-1 | W2 |
| pubmed-research-note-2 | H | H45 | decision-brief.md:11-12 "first four ... last three" over 6 headings; intent-lock-pairing.md:49-57 lists 4 items | Slot arithmetic self-contradicts (4+3≠6) | S03-W3-2 | W3 |
| pubmed-research-note-3 | M | — | atomic-note-template.md:23 pushes PMIDs into Sources vs SKILL.md:219-221 "No...PMID"; :37 `type:` vs vault-keeper's legal types | Atomic-note path contradicts both contracts | S03-W2-1 | W2 |
| pubmed-research-note-4 | M | — | evals.json id 6 "NOT restated inline" vs SKILL.md:155-158 mandatory inline render | Eval contradicts default Show/File | S03-W2-1; converted S03-W3-6 | W2 |
| pubmed-research-note-5 | M | — | tool-catalog.md:25-28 stable prefix + "No ToolSearch step"; connector already exposes `mcp__PubMed__*` | Hardcoded prefix ignores a live connector | S03-W2-2 | W2 |
| pubmed-research-note-6 | M | — | SKILL.md:82 "ALWAYS...FIRST"; :150-151 "Run all three every time" | No path when intent-lock/vault-keeper absent | S03-W2-1 | W2 |
| pubmed-research-note-7 | M | — | CHANGELOG.md jumps 1.5.0(L42)→1.2.0(L67); :40 cites "1.3.0 behavior" | Missing 1.3.0/1.4.0 entries | S10-W0-8 | W0 |
| pubmed-research-note-8 | L | H45-adj | SKILL.md:221-222 vs tool-catalog.md:100, two NCT grammars | Two NCT forms in one skill | S03-W2-2 | W2 |
| pubmed-research-note-9 | L | — | SKILL.md:32,61,293 version-history narration | Time-relative text in operational instructions | S03-W2-1 | W2 |
| pubmed-research-note-10 | L | — | SKILL.md:153-154 no filename rule; README's config schema undocumented in-skill | No slug/naming convention | S03-W3-1 (I04) | W3 |
| pubmed-research-note-11 | L | — | SKILL.md:170-172 names `notes/` vs :172 "never invent a vault path" | Names a path while forbidding it | S03-W2-1 | W2 |
| pubmed-research-note-12 | L | — | "explicit opt-out" ×4; depth contract SKILL.md:59-78=report-craft.md:12-70; "Signs...drifted" SKILL.md:291-320=report-craft.md:118-140 | Repetition inflates the body | S03-W3-2, -3 | W3 |
| pubmed-research-note-13 | L | — | evals.json: 17 entries, all `assertions: []`; id 11 needs live literature | Prose-only, ungradeable | S03-W3-6 | W3 |
| pubmed-research-note-14 | L | — | no `commands/`; siblings had `/comprehensive-review`, `/digest` | No slash-command parity | S03-W3-4 (`argument-hint`, §7) | W3 |

Every defect with the `pubmed-research-note` prefix appears exactly once above (14 of 14).

### 1.4 Other findings

- Step-0 dependency unguaranteed session-wide (no `dependencies` mechanism) — resolved generically by T4/§4.2, applied at S03-W2-1.
- "atomize" collision (vault-atomizer / atomize-book / this skill's old gate word) — resolved by retiring the word here (S03-W2-1), not renaming it to something that still collides.
- Report-format drift vs digest-report's inline-citation expectation — digest-report (S15, I09) is a **tolerant reader**; I04 is the *forward* contract, not a retrofit of the 3 real `research-notes/` reports (numbered author-year Sources with PMIDs, no frontmatter). Noted for S15.
- MCP duplication (3 micky copies) — resolved at W3's move to one `plugins/evidence/.mcp.json`; W2 does not touch `.mcp.json`.
- **NEW**: `comprehensive-review`'s `Use when` sits at char 376 (R4 violation) — S04's territory, noted only because it shares this plugin's eventual listing budget (§9).
- **NEW**: live tool schemas ground I05 precisely (`datetype` default `pdat`, enum `pdat\|edat\|mdat`; `retstart` pagination; CT.gov `status` enum has no `completed-no-results`/`has-results`; `advanced_query` date-filters via `AREA[Field]RANGE[min,max]`) — §2.7.

## 2. Target state

### 2.1 Location and tree (after W3)

```
plugins/evidence/
  .claude-plugin/plugin.json
  .mcp.json                    # pubmed, clinical-trials (I05)
  references/report-contract.md engines.md   # I04, I05
  skills/
    pubmed-research-note/{SKILL.md, references/{decision-brief,intent-lock-pairing,report-craft,tool-catalog}.md, evals/}
    comprehensive-review/ lit-watch/          # S04
  scripts/sources_lint.py test_sources_lint.py
  evals/mocks/{pubmed,clinical-trials}/*.md
       fixtures/report-{decision,topic,digest}.md
  README.md · CHANGELOG.md · LICENSE
```
Top-level eval cases live at `evals/pubmed-research-note/<case>/`. `tool-catalog.md` is trimmed to engine-specific recipes; MCP-resolution text moves to `engines.md`.

`atomic-note-template.md` does not exist in the target tree (retired, S03-W2-1).

### 2.2 Frontmatter (W3 final; also the W2 interim, minus `argument-hint` and `metadata.profile` which land W3 per the architecture's description-pass wave)

```yaml
---
name: pubmed-research-note
description: >-
  Answers a clinical question from primary literature with a quantified, adjudicated
  evidence report — an explicit, marked verdict with full per-study depth, in whatever
  shape serves the question. Use when asked to "research", "what does the literature say
  about", "search PubMed for", "is X true", "should I use X for Y", or whether a drug or
  intervention is worth using, building a service on, or teaching. Thai: "หางานวิจัย",
  "ทบทวนหลักฐาน", "ค้น PubMed", "จริงหรือเปล่า". Not for: a whole-disorder review (use
  evidence:comprehensive-review), a multi-domain watchlist sweep (use evidence:lit-watch),
  non-biomedical research (use deep-research), MCQ/CRQ/essay generation or grading.
argument-hint: "[clinical question]"
metadata:
  profile: cc
---
```

Measured (`measure.py text`): 655 chars, 164 tok, `use_when_at` 187 (within R4's ~250 band), `not_for_at` 493, no first/second person, no angle brackets. Kept: the 9 quoted phrases above. **Dropped** (§6): "ALWAYS runs intent-lock FIRST...", "Default: write...atomize/ทำโน้ต", "Engines: ...Firecrawl" — all R3-forbidden process prose. "comprehensive review of X" drops too (it was the Not-for target's own phrase); the real trigger stays in `evidence:comprehensive-review`'s description (S04 to confirm).

### 2.3 Body outline

Actions: keep | cut (reason) | move → file | script → name | new. Line numbers are today's (§1.1).

**SKILL.md, W2** (target ≤210 lines / ≤4,300 tokens interim — the ≤4,000-token W3 floor in §9 is reached only after W3's dedupe):

| # | Target section | Source | Action |
|---|---|---|---|
| 1 | Title + two owed things | :18-30 | keep |
| 2 | `## Standing rules` | :38-78 | keep :38-58; keep :59-78 too at W2 (report-craft.md's copy untouched this wave; full cut to a pointer is W3) |
| 3 | `## Step 0` | :80-98 | rewrite: drop the "ALWAYS...opt-out" repeat (kept once); insert §2.6's OPTIONAL-fallback sentence as the *unavailable* branch |
| 4 | `## The decision brief` | :100-122 | keep (anatomy pointer; slot-count text is H45, W3) |
| 5 | `## Pairing with intent-lock` | :124-146 | cut to 3 lines pointing at `intent-lock-pairing.md` (:126-142 duplicates it verbatim, defect-12) |
| 6 | `## Where output goes` | :148-172 | File step → §2.6 sink sentence (I11); cut the "not atomize" paragraph and "never invent a vault path" line (name the retired path) |
| 7 | `## Source engines` | :174-204 | keep the 5 roles; "Prefer the MCP server..." → "Before the first call, read `references/tool-catalog.md`" |
| 8 | `## The citation discipline` | :206-228 | keep at W2 (pointer at W3); fix the NCT line |
| 9 | `## The report` (preface) | :230-269 | rewrite: frontmatter (`title`, `kind: decision`, `topic`, `source_skill`, `created`, `contract: report/1`) replaces the dated-line + Assumed/Reframed/Skipped block; single conditional `Assumed:` line (H44) |
| 10 | `## Atomize` | :271-282 | **cut entirely** (defects 3, 4, 11) |
| 11 | `## Close` | :284-289 | drop "atomize"; add "or the sink fallback taken" |
| 12 | `## Signs...drifted` | :291-320 | keep at W2; cut the `[ASSUMED]`/Reframed and atomize items |

`atomic-note-template.md`'s link is removed (file deleted, S03-W2-1).

**tool-catalog.md, W2**: intro+prefix table (:1-20) → I05's sentence, once; §1 PubMed (:23-61) → cut :25-28, add `datetype` note; §2 CT.gov (:65-101) → cut :71-73, NCT line → canonical form; §3-5 (:104-158) → unchanged.

**intent-lock-pairing.md, W2**: keep :1-41; **cut** "Reframes and the decision" (:84-90) — 0.4.2 never reframes; rewrite "Where the assumptions live" (:73-82) to the single conditional line; "What intent-lock must have fixed" (:43-59) held for W3; keep :92-96.

**decision-brief.md, W3** (H45, design note below): items 1/2/6 rewritten as fixed by the lock record; items 3/4/5 rewritten as skill-derived; the ":11-12 first four/last three" sentence deleted.

**report-craft.md, W3**: depth-contract text becomes the single copy (SKILL.md's :59-78 duplicate cut here); "Signs you've drifted" stays the single copy (SKILL.md's :291-320 cut to a pointer here).

**Design note — retiring "Atomize"** (resolves defects 3, 4, 11 + the §2.8 collision): §5.2's producer table lists one output for this skill — `report .md`, kind `decision`, no atomic-notes row — with publish trigger `"digest <report>"` (OD5-a), which is digest-report's own existing trigger. So the word-gated atomic-note production (today's "atomize", `atomic-note-template.md`) is **retired, not renamed**: this skill ends at write → show → file; notes come later, via a separate call to `digest-report`. Design resolution, not an architecture conflict — §8.

### 2.4 References

Paths relative to `plugins/evidence/skills/pubmed-research-note/` except the last two (family root).

| File | Purpose | Load condition | Size target |
|---|---|---|---|
| `references/decision-brief.md` | 6-slot anatomy | "Read before your first search" | ≤110 lines / ≤1,700 tok |
| `references/intent-lock-pairing.md` | Trigger rule, slot mapping, never-re-ask list | "Full contract: read before Step 0's first run" (new — it had none) | ≤85 lines / ≤1,200 tok |
| `references/report-craft.md` | Shape + depth contract, worked shapes | "Read before you write" | ≤130 lines / ≤1,900 tok |
| `references/tool-catalog.md` | Per-engine search recipes | "Read before the first tool call" | ≤130 lines / ≤1,700 tok |
| `../../references/report-contract.md` (family) | I04 in full | "Before writing `## Sources`, read..." (also linked from `evidence:comprehensive-review`/`lit-watch`) | ≤120 lines / ≤1,600 tok |
| `../../references/engines.md` (family) | I05 in full | "Before the first tool call, read..." | ≤90 lines / ≤1,300 tok |

Mandatory-at-search set after W3 sums to ~8,200 tok, above today's 5,900, unless `report-contract.md`/`engines.md` are counted **once per family session** (CR and lit-watch cite the same two files, §4.1's "family is the unit of sharing"). Architecture's §9 target (body ≤4k, mandatory ≤3k) is a per-skill **body** budget; the family files are shared reads.

### 2.5 Scripts

**`scripts/sources_lint.py`** (family script, `plugins/evidence/scripts/`):

| Field | Value |
|---|---|
| CLI | `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/sources_lint.py <file.md> [--json] [--help]` |
| Input | one report `.md` file path (frontmatter + body) |
| Checks | frontmatter present, `contract: report/1`, `kind` ∈ {decision,topic,digest}; body has zero inline-citation matches (`\(\w+\s+\d{4}\)`, `PMID\s*\d+`, `\[\d+\]`, outside fences); `## Sources` non-empty and every line matches one of the four I04 grammars; no bare URL lacking a topic phrase |
| JSON stdout | `{"ok": bool, "file": str, "violations": [{"line": int, "rule": str, "text": str}]}` |
| Exit codes | 0 clean; 1 violations (also on stderr); 2 no file/frontmatter |
| Tests | `test_sources_lint.py` (CX-42 — `-p 'test_*.py'` matches this name): one case per violation rule + one clean-fixture pass against `evals/fixtures/report-decision.md` |

Non-interactive, read-only (a linter, never a fixer — R65/R67); `--help` exits 0; UTF-8, trailing newline.

### 2.6 Handoffs

Step 0, verbatim per `alignment/references/lock-record.md` §Handoff (owner S01), plugin segment per wave (CX-16): `intent-lock:intent-lock` at W2 (S03-W2-1, before S10's skeleton PR exists), `alignment:intent-lock` from W3 (S03-W3-4):

> Run `intent-lock:intent-lock` (OPTIONAL). If it is not available in this session — or it needs an interactive picker and none exists here (subagent, headless, scheduled run) — do not stall: take the broadest reading that fits the request and open the report with one line `Assumed: <reading> — say if wrong.`

File step, same pattern (§4.2), owner S07's I11 report form:

> File via `vault-keeper` (OPTIONAL). If absent, write to `$LEARN_HUB_DIR/research-notes/` when its marker validates, otherwise to cwd, and say where.

### 2.7 Interfaces

**I04 — Report contract `report/1` (owned in full).**

Frontmatter (top of every report this family writes):
```yaml
---
title: <sentence-case human title>
kind: decision | topic | digest
topic: <kebab-case slug for grouping; may equal the report's own slug>
source_skill: evidence:pubmed-research-note | evidence:comprehensive-review | evidence:lit-watch
created: <YYYY-MM-DD>
contract: report/1
---
```
`kind` by producer: `decision` (pubmed-research-note), `topic` (comprehensive-review), `digest` (lit-watch) — §5.2.

Body opens with the single `Assumed: <reading> — say if wrong.` line, **only** when a material default was taken (mirrors intent-lock 0.4.2's Phase 3 rule, `.../intent-lock/SKILL.md:226`; no `Reframed:` line, :202,226). No inline citations anywhere in prose (`(Author Year)`, `PMID NNNNNNN`, `[3]`).

`## Sources`, one line per source, one grammar per kind:
- Journal: `<topic phrase> — [doi:10.xxxx/yyyy](https://doi.org/10.xxxx/yyyy)`. No authors, journal, year, volume, pages, PMID.
- Registry (**canonical NCT form**, replacing the two variants — defect-8): `NCT NNNNNNNN — <topic>, <status>, n=<N>, readout <YYYY-MM|completed|unknown>`.
- Textbook: `Title, edition — OLID`. Web (firecrawl): `<topic> — <URL> (accessed YYYY-MM-DD)`, DOI preferred if one exists. Unsourced: `[unverified]` in place.

Depth contract (stated once, every producer points here): load-bearing studies as full paragraphs (design, population, n, comparator, endpoint, effect size + CI, key harms); supporting studies grouped; sources capped by relevance never count; compression is the named failure.

Engine-failure policy: PubMed unreachable (MCP + E-utilities both) = **fatal**. ClinicalTrials.gov unreachable = **degrade**, name the gap. Open Library / Wikipedia / firecrawl unreachable = optional, omit and say so if load-bearing.

Voice rule: state findings directly, no "the search found" / "according to PubMed" narration (matches digest-report's own rule — LOC-28 P0-1).

Slug: kebab-case, deterministic from `title`. Collision at the write destination → `-2`, `-3`, ….

`sources_lint.py` CLI: §2.5. Fixtures (written here): `plugins/evidence/evals/fixtures/report-{decision,topic,digest}.md`, one short valid example per `kind`. **ASSUMES**: S15's `check-contract.mjs` (I25) reads these by this exact path/name — S15 to confirm (§8).

**I05 — Engines (owned in full).**

Runtime MCP resolution (replaces every hardcoded `mcp__plugin_<p>_pubmed__` prefix and "No ToolSearch step" line, T4/R41):
> Use the PubMed / ClinicalTrials tool present in this session: `mcp__PubMed__*` / `mcp__Clinical_Trials__*` (connector) or `mcp__plugin_*_pubmed__*` / `mcp__plugin_*_clinical-trials__*` (plugin). If neither is listed, run ToolSearch for "pubmed" once. If still none, use E-utilities / CT.gov API v2 via WebFetch.

PubMed / E-utilities (confirmed against the live schema):
- Args incl. `max_results` (default 20), `retstart` (offset), **`datetype`** (default `pdat`; enum `pdat|edat|mdat`). Pass `datetype: "edat"` for every windowed/recency call — the default `pdat` silently misses records whose entry postdates their nominal pub date.
- Page with `retstart` until a page returns fewer rows than `max_results` or a cap is hit; report screened-vs-kept, never one uncounted call.
- Web fallback: `esearch.fcgi?db=pubmed&term=<query>&datetype=edat&mindate=<from>&maxdate=<to>&retmode=json`, then `efetch.fcgi?...&rettype=abstract`. Unreachable both paths = fatal (I04).

ClinicalTrials.gov v2 (confirmed against the live schema):
- `status` enum (14 values, e.g. `RECRUITING, COMPLETED, TERMINATED, WITHDRAWN, UNKNOWN` — full list in the live tool schema) has **no** `completed-no-results`/`has-results` value; "completed, nothing posted" = `status: COMPLETED` + a per-trial `get_trial_details` results-posted check.
- Date-filters directly via `advanced_query`: `AREA[<Field>]RANGE[<from>,<to>]`, e.g. `AREA[ResultsFirstPostDate]RANGE[2026-07-01,2026-08-01]` — replaces any recipe claiming it cannot date-filter.
- Web fallback: `.../api/v2/studies?query.term=<term>&filter.advanced=AREA[<Field>]RANGE[<from>,<to>]`. Unreachable = degrade (I04).

Firecrawl: `firecrawl search "<query>"` / `firecrawl scrape <url>` (WebFetch fallback, never blocks); fetches, never adjudicates; scope guard unchanged (authoritative primary document only).

`.mcp.json`, `plugins/evidence/.mcp.json`, server names `pubmed` and `clinical-trials`:
```json
{"mcpServers":{"pubmed":{"type":"http","url":"https://pubmed.mcp.claude.com/mcp"},"clinical-trials":{"type":"http","url":"https://hcls.mcp.claude.com/clinical_trials/mcp"}}}
```
(byte-identical to today's 3 micky copies, confirmed by `diff`.)

Mocks (suite-wide, written here): `evals/mocks/pubmed/{search_articles,get_article_metadata}.md`, `evals/mocks/clinical-trials/{search_trials,get_trial_details}.md`. The suite-wide `search_articles` mock carries **no** `expect:` on `datetype` (this skill's searches are not always windowed); a case testing `datetype: edat` (H46, S04/lit-watch) supplies a **case-scoped** override with `expect: {datetype: /^edat$/}`, per eval-format.md's case-level override rule. S04 to use this pattern, not a suite-wide guard.

**Consumed, all ASSUMES unless noted (owner to confirm; §8 tracks the load-bearing ones):**

| Interface | Owner | What this spec assumes |
|---|---|---|
| I01 | S01 | `deliverable` supplies brief slot 2 ("verdict's shape"); `exclusions`+`assumed defaults` supply slot 6 ("anti-goal"); `scope in/out` governs search breadth, not a numbered slot. Used in H45 (S03-W3-2). |
| I09 | S15 | Filing a report writes `research-notes/<slug>.md` with **no** `.meta.json` sidecar (that shape is I09's visual-asset case; a report carries its own I04 frontmatter). |
| I11 | S07 | Filing sentence: "report, `sink.py --kind report`" — the sink accepts a `kind: decision` report artifact (`title`, `body`) and returns the landing path for Close (CX-8). |
| I17 | S12 | Layout `plugins/evidence/evals/pubmed-research-note/<case>/`; tags `smoke\|trigger\|negative\|output\|release`; trigger-grader regex as in §4.1. |
| I20 | S08 | House shape applied in §2.2/§2.3 (order, `metadata.profile: cc`, standing rules first, `## Gotchas`, no version narration). |
| I23 | S10 | The W3 skeleton-PR step moves `plugins/pubmed-research-note/` → `plugins/evidence/skills/pubmed-research-note/` byte-for-byte and creates the empty `plugins/evidence/` shell before this spec's W3 steps populate it. |

## 3. Change steps

Path shorthand used below: `Q` = `plugins/pubmed-research-note` (W2 location); `P` = `plugins/evidence` and `S` = `$P/skills/pubmed-research-note` (W3 location, after S10's move).

### Wave W0

**S03-W0-1** · depends on: S12-W0-3
- Files: create `$Q/evals/pubmed-research-note/<case>/{prompt.md,graders/*.md}` (3 cases: trigger positive, near-miss negative, one output case, mined against today's skill — see architecture §10 W0 item 3; I17 layout; every `prompt.md` carries `smoke` in `tags`; each case directory takes the name of one of §4.1's cases, so the later eval step extends these directories instead of adding new ones (critique P2, P7)).
- Change: seed the pre-rewrite smoke baseline so later gates (I16.3, S12's W0-5 checklist) have something to compare against before this spec's own W2/W3 rewrites land.
- Commands / done when: S12-W0-5's check for this unit — `find . -path '*/evals/pubmed-research-note/*' -name prompt.md | xargs grep -l 'tags:.*smoke' | wc -l` ≥ 3.
- Rollback: `git rm -r $Q/evals/pubmed-research-note`.

### Wave W2 (repo: micky-psych-tools; plugin stays at `$Q/`)

**S03-W2-1** · depends on: S15-W2-2 (the tolerant reader must exist before this step writes against it — consumers before producers, CX-35)

- Files: edit `Q/skills/pubmed-research-note/SKILL.md`; delete `.../references/atomic-note-template.md`.
- Change: §2.3 rows 2-12 (Step-0 fallback sentence; File-step sink sentence; frontmatter + single conditional `Assumed:` preface with `contract: report/1`; cut `## Atomize` + its link; cut version-narration at L32/61/293; trim "Pairing with intent-lock" to 3 lines).
- Commands / done when: `claude plugin validate --strict $Q` exits 0; `grep -ic "Reframed:\|atomize" $Q/skills/pubmed-research-note/SKILL.md $Q/skills/pubmed-research-note/references/*.md` = 0; `test ! -f $Q/skills/pubmed-research-note/references/atomic-note-template.md`.
- Rollback: `git checkout -- $Q/skills/pubmed-research-note/SKILL.md $Q/skills/pubmed-research-note/references/atomic-note-template.md`.

**S03-W2-2** · depends on: S03-W2-1
- Files: edit `Q/skills/pubmed-research-note/references/tool-catalog.md`.
- Change: replace :1-20 intro and the two "stable prefix / No ToolSearch step" passages (:25-28, :71-73) with I05's resolution sentence (§2.7), quoted once; rewrite the :100 NCT line to the one canonical form; add the `datetype: edat` note to the PubMed recipe.
- Commands / done when: `grep -c "No ToolSearch\|mcp__plugin_pubmed-research-note" $Q/skills/pubmed-research-note/references/tool-catalog.md` = 0; the SKILL.md and tool-catalog.md NCT-line strings are byte-identical (`diff` of the two `grep -o 'NCT NNNNNNNN[^)]*'` outputs empty).
- Rollback: `git checkout -- $Q/skills/pubmed-research-note/references/tool-catalog.md`.

**S03-W2-3** · depends on: S03-W2-1
- Files: edit `Q/skills/pubmed-research-note/references/intent-lock-pairing.md`.
- Change: delete "Reframes and the decision" (:84-90); rewrite "Where the assumptions live" (:73-82) to the single conditional `Assumed:` line.
- Commands / done when: `grep -c "Reframed" $Q/skills/pubmed-research-note/references/intent-lock-pairing.md` = 0.
- Rollback: `git checkout -- $Q/skills/pubmed-research-note/references/intent-lock-pairing.md`.

**S03-W2-4** · depends on: S03-W2-1
- Files: create `plugins/pubmed-research-note/references/report-contract.md` (I04 text, §2.7); create `plugins/pubmed-research-note/evals/fixtures/report-{decision,topic,digest}.md` (one short valid example per `kind`).
- Change: land the I04 report contract and its 3 fixtures at today's (W2) plugin path, so S04-W2-2 and S15's `--cross-repo` gate have a report-contract file and fixtures to read before the family shell exists (CX-7).
- Commands / done when: `grep -c "contract: report/1" $Q/references/report-contract.md` = 1; `ls $Q/evals/fixtures | wc -l` = 3.
- Rollback: `git rm $Q/references/report-contract.md && git rm -r $Q/evals/fixtures`.

**S03-W2-5** · depends on: S03-W2-1, S03-W2-2, S03-W2-3, S03-W2-4
- Change: release the W2 fixes — `python3 scripts/bump.py pubmed-research-note minor --write` (CX-13).
- Files: `$Q/.claude-plugin/plugin.json`, `$Q/CHANGELOG.md` (entry: "H44 closed: single Assumed: line, OPTIONAL fallbacks, runtime MCP resolution, sink filing, report/1 contract."). `.claude-plugin/marketplace.json` is not touched: S10-W0-3 removed every entry `version` (I18, CX-12).
- Done when: `python3 scripts/validate.py` prints `all checks passed`; `marketplace.json` has no `version` key for this entry.
- Rollback: `git checkout -- $Q/.claude-plugin/plugin.json $Q/CHANGELOG.md`.

W2 exit: `claude plugin validate --strict $Q` exits 0; a hand-written fixture report passes a manual read against §2.7 (`sources_lint.py` itself is W3). **Note for S11**: H45 stays open until W3, so this plugin's I16.2 V3 readiness sentence should read "H44 closed; H45 tracked for W3" — §8.

### Wave W3 (depends on S10-W3-2 — the skeleton-PR step moving `$Q` → `$S`, I23)

**S03-W3-1** · depends on: S10-W3-2, S01-W3-2
- Files: edit (not create — S03-W2-4 already created `report-contract.md`/fixtures at the W2 path, and S10-W3-2 already moved `.mcp.json` to `$P/.mcp.json`) `$P/references/report-contract.md` (moved from `Q/references/`, now at its W3 path — no content change needed); create `$P/references/engines.md`; edit the moved SKILL.md and tool-catalog.md to point at the two family files instead of carrying the text inline.
- Change: write I05's text into `engines.md` (I04's `report-contract.md` already exists from S03-W2-4 and moved unchanged). Drop the `.mcp.json` create-and-diff step entirely — S10-W3-2 already moved it and deleted CR's/PPD's duplicate copies (CX-14).
- Commands / done when: `grep -c "contract: report/1" $P/references/report-contract.md` = 1; `find plugins -name .mcp.json | wc -l` = 1.
- Rollback: `git rm $P/references/engines.md && git checkout -- $S/ $P/references/report-contract.md`.

**S03-W3-2** · depends on: S03-W3-1, S01-W3-2
- Files: edit `$S/references/decision-brief.md`, `$S/references/intent-lock-pairing.md`.
- Change (H45): decision-brief.md items 1/2/6 ("the question"/"verdict's shape"/"anti-goal") rewritten as **fixed by the lock record** (I01's `question`/`deliverable`/`exclusions`+`assumed defaults`); items 3/4/5 rewritten as **derived by the skill** from 1/2/6 plus `scope in/out` (a governing constraint, not a 7th slot); delete the ":11-12 first four/last three" sentence. Mirror the split into intent-lock-pairing.md:49-57. K13: replace "a Klaeng OPD" (decision-brief.md:93) with "a community OPD" — no personal context in distributable text (critique P27).
- Commands / done when: `grep -c "first four" $S/references/decision-brief.md` = 0; the file's numbered slot headings count to 6; `grep -c Klaeng $S/references/decision-brief.md` = 0.
- Rollback: `git checkout -- $S/references/decision-brief.md $S/references/intent-lock-pairing.md`.

**S03-W3-3** · depends on: S03-W3-1
- Files: edit `$S/SKILL.md`, `$S/references/report-craft.md`.
- Change (defect-12, remainder): cut SKILL.md's Standing-rules depth-contract duplicate (today's :59-78) and its "Signs the report has drifted" (:291-320) each to a 2-line pointer at report-craft.md.
- Commands / done when: `measure.py skill $S/SKILL.md` reports `body_est_tokens` ≤ 4,000 and still lists `report-craft.md` under `linked_files`.
- Rollback: `git checkout -- $S/SKILL.md $S/references/report-craft.md`.

**S03-W3-4** · depends on: S03-W3-1, S12-W3-2
- Files: edit `$S/SKILL.md` frontmatter.
- Change: description → §2.2's text; add `argument-hint: "[clinical question]"`; add `metadata: {profile: cc}`; cross-check reciprocal `Not for` against `evidence:comprehensive-review`/`evidence:lit-watch` (S04 carries the reverse phrase).
- Commands / done when: `measure.py skill $S/SKILL.md` reports description `chars` ≤ 1024, `use_when_at` ≤ 260, `yaml_valid: true`.
- Rollback: `git checkout -- $S/SKILL.md`.

**S03-W3-5** · depends on: S03-W3-1
- Files: create `$P/scripts/sources_lint.py` + `test_sources_lint.py` (CX-42 — `-p 'test_*.py'` matches this name, not `sources_lint.test.py`); `$P/evals/mocks/pubmed/{search_articles,get_article_metadata}.md`, `$P/evals/mocks/clinical-trials/{search_trials,get_trial_details}.md`. The 3 `report-{decision,topic,digest}.md` fixtures already exist at `$P/evals/fixtures/` (created S03-W2-4, moved unchanged by S10-W3-2) — do not recreate them here.
- Change: implement §2.5's CLI; write 4 mock files per I05 with fixed PMIDs (reused from the real trazodone report, e.g. `41645529`, `42446992`) and NCT ids (e.g. `NCT05209035`).
- Commands / done when: `python3 -m unittest discover -s $P/scripts -p 'test_*.py'` all-green; `sources_lint.py <fixture> --json` prints `"ok": true` exit 0 for all 3 existing fixtures.
- Rollback: `git rm -r $P/scripts/sources_lint.py $P/scripts/test_sources_lint.py $P/evals/mocks`.

**S03-W3-6** · depends on: S03-W3-1, S03-W3-5
- Files: delete `$S/evals/evals.json`; create `$P/evals/pubmed-research-note/<case>/{prompt.md,graders/*.md}` per §4.1.
- Change: mine the 17 old prompts as seeds; hand-write graders; land at 5 cases (§4.1). Drop "Klaeng" from any mined prompt (K13).
- Commands / done when: `test ! -f $S/evals/evals.json`; `find $P/evals/pubmed-research-note -mindepth 1 -maxdepth 1 -type d | wc -l` = 5; `grep -rc Klaeng $P/evals | grep -v ':0$'` prints nothing. (`claude plugin eval` itself is run later, not by this spec — hard constraint.)
- Rollback: `git checkout -- $S/evals/evals.json && git rm -r $P/evals/pubmed-research-note`.

**S03-W3-7** · depends on: S03-W3-6, S04-W3-6
- Files: merge `$P/README-pubmed-research-note.md`/`README-comprehensive-review.md`/`README-lit-watch.md` (S10-W3-2's per-member suffix) and the equivalent `CHANGELOG-<p>.md` files into single `$P/README.md`/`$P/CHANGELOG.md`; create `$P/LICENSE` (MIT) if S10-W0-8 hasn't already backfilled one for every member; delete the per-member files.
- Change: `README.md` states the three skills, the shared `.mcp.json`/`report-contract.md`/`engines.md`, and a `## Surfaces` section naming every place this family's summary appears (I16 item 1). `CHANGELOG.md` merges the three histories, newest first.
- Commands / done when: `find $P -maxdepth 1 -name 'README-*.md' -o -name 'CHANGELOG-*.md' | wc -l` = 0; `grep -c "^## Surfaces" $P/README.md` = 1.
- Rollback: `git checkout -- $P/README.md $P/CHANGELOG.md $P/LICENSE`.

**S03-W3-8 (new, critique P5)** · depends on: S08-W3-1 (`release.py`), S03-W3-7, S03-W3-2, S03-W3-3, S03-W3-4, S04-W3-2, S04-W3-4, S04-W3-5
- Change: release the evidence family after its W3 rewrite — `python3 plugins/plugin-creator/scripts/release.py evidence minor --write`.
- Files: `$P/.claude-plugin/plugin.json`, `$P/CHANGELOG.md`.
- Done when: `python3 plugins/plugin-creator/scripts/validate.py --repo .` prints `all checks passed`; the first `## ` line of `$P/CHANGELOG.md` names the `plugin.json` version; `marketplace.json` has no `version` key for `evidence`.
- Rollback: `git revert <this commit>`.

W3 exit: all 7 steps done; body ≤4,000 tok; description ≤1,024 chars, `Use when` ≤260; `sources_lint.py` tests green; 5 eval dirs, no `evals.json`; one family README/CHANGELOG/LICENSE, no per-member copies; H44+H45 closed. No OWNER-marked steps in this spec. Per S11's I16 item 4 template: "Ready for cloud delivery: HIGH defects due by this wave closed (H44, H45); handoffs carry the §4.2 fallback or target an enabled plugin; no same-named unit elsewhere; smoke suite passed (<result path>)."

## 4. Evals

### 4.1 Cases

5 cases for `pubmed-research-note` (≥3 required; R71/EVL-04 target 3-5). Full content for the first 3 (trigger positive, near-miss negative, output/process); the remaining 2 in the table below. All paths are under `plugins/evidence/evals/pubmed-research-note/`.

**Case 1 — `trigger-decision-question/`** (trigger positive):

`prompt.md`:
```markdown
---
tags: [pubmed-research-note, trigger, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Write]
max_turns: 20
---

Should I use prazosin for PTSD nightmares in my patient this afternoon? What does the
literature actually say.
```

`graders/skill-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?pubmed-research-note"'
arm: both
---
```

`graders/verdict-marked.md`:
```markdown
---
type: llm
criteria: >-
  PASS if the final message or a file it wrote contains an explicit, marked verdict
  (bolded line or its own heading) about prazosin for PTSD nightmares with a stated
  confidence level. FAIL if unmarked, or if it asks a clarifying question instead of
  answering (no interactive picker in this run — the skill must take the broadest
  reading and proceed, per its OPTIONAL-fallback rule).
focus: last_message
---
```

**Case 2 — `negative-whole-disorder/`** (near-miss negative, drawn from `evidence:comprehensive-review`'s territory):

`prompt.md`:
```markdown
---
tags: [pubmed-research-note, negative]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 10
---

Write me a comprehensive review of intermittent explosive disorder — I want the whole
picture, not one decision.
```

`graders/not-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?pubmed-research-note"'
min: 0
max: 0
arm: both
---
```

**Case 3 — `output-sources-contract/`** (output/process — I04 compliance):

`prompt.md`:
```markdown
---
tags: [pubmed-research-note, output, release]
allowed_tools: [Read, Glob, Grep, Skill, Write]
max_turns: 20
---

Research esketamine for treatment-resistant depression and write the report — I want to
see the file, not just chat.
```

`graders/frontmatter-contract.md`:
```markdown
---
type: regex
target: { source: file, path: "*.md" }
pattern: 'contract:\s*report/1'
weight: 2
---
```

`graders/no-inline-citation.md`:
```markdown
---
type: regex
target: { source: file, path: "*.md" }
pattern: '\([A-Z][a-z]+ (19|20)\d{2}\)|PMID\s*\d+'
match: not_contains
weight: 3
---
```

`graders/wrote-via-write-tool.md` (process grader):
```markdown
---
type: tool_used
tool: Write
min: 1
---
```

Further cases:

| Name | Tags | Prompt gist | Graders |
|---|---|---|---|
| `negative-daily-sweep` | pubmed-research-note, negative | "Give me today's psychiatry paper digest across all subspecialties." | `tool_used Skill min:0 max:0 arm:both` (near-miss vs `evidence:lit-watch`) |
| `sink-fallback-no-vault-keeper` | pubmed-research-note, process, release | "Research vortioxetine for anhedonia and save it." (isolated run — no `vault-keeper` plugin loaded) | `regex` on the last message for the sink-fallback path taken (`$LEARN_HUB_DIR` or cwd, stated); `llm` PASS if the skill did not stall waiting for vault-keeper and did not fabricate a save path |

### 4.2 Conversion

| Old case (id, name) | New case dir | Dropped (reason) |
|---|---|---|
| 1 `treatment-decision-answer-and-depth` | `trigger-decision-question` (seed) | — |
| 2, 5, 12 shape/teaching/adjudicate variants | folded into Case 1/3 rubrics | redundant coverage; R71 targets 3-5, not 17 |
| 3 `service-decision-and-registry` | — | redundant with Case 3's depth coverage |
| 4 `thai-trigger-contested-claim` | — | owned by S12's live-trigger set (§4.3), not required per-skill |
| 6, 7 `atomize-gate-*` | — | the atomize gate no longer exists (§2.3 design note); defect-4 moot |
| 8 `negative-trigger-daily-digest` | `negative-daily-sweep` | renamed |
| 9 `negative-trigger-nonbiomedical` | — | redundant with `negative-whole-disorder`; owned by S12's live set |
| 10 `citation-contract-refusal` | folded into `no-inline-citation` grader | dropped as a separate case |
| 11 `adversarial-null-search` | — | depends on live literature state, ungradeable deterministically (defect-13) |
| 13, 14 intent-lock-chain cases | — | isolated eval runs never load `alignment:intent-lock`; covered instead by `sink-fallback-no-vault-keeper`'s fallback pattern |
| 15 `no-filesystem-renders-inline` | — | good W4/S12 candidate, not required for the 3-5 minimum |
| 16 `vault-artifact-without-atomize` | `sink-fallback-no-vault-keeper` (seed) | renamed, rewritten for the sink |
| 17 `depth-over-compression` | folded into Case 3 | I04's depth contract graded there |

### 4.3 Live triggers

Family (arch §6.3): `{pubmed-research-note, comprehensive-review, lit-watch, anthropic-skills:psych-paper-digest, anthropic-skills:deep-research, anthropic-skills:daily-random-review}`. Near-miss queries (feeding S12's set):
- "What's new in psychiatry this week across all my areas?" → `evidence:lit-watch`
- "Give me a full academic review of bipolar II disorder" → `evidence:comprehensive-review`
- "Research the history of Thai civil-service physician pay reform" → `deep-research` (non-biomedical)
- "Is there good evidence for omega-3 in depression?" → should-trigger here

### 4.4 Commands

Smoke: `bash scripts/eval.sh --smoke evidence -- --allow-tools Write` (S12's wrapper passes args after `--` through to `claude plugin eval plugins/evidence --tag smoke --ablation none --runs 1 --allow-tools Write`; `--allow-tools Write` is required because `output-sources-contract` writes the report file — factcheck F3). Release: `bash scripts/eval.sh --release evidence -- --allow-tools Write` (two arms, `--runs 3 --threshold 0.8`). Neither runs from this spec (hard constraint) — documented for the executor session after S10's wrapper exists.

## 5. Acceptance criteria

`P` = `plugins/evidence`; `S` = `$P/skills/pubmed-research-note`.

1. `claude plugin validate --strict $P` (post-W3) exits 0.
2. `grep -rc "Reframed\|GOAL UNIFIED" $S/` = 0 across all files.
3. `grep -rc "No ToolSearch\|mcp__plugin_pubmed-research-note" $S/references/tool-catalog.md` = 0.
4. `test ! -f $S/references/atomic-note-template.md` succeeds.
5. `python3 -c "import yaml; d=yaml.safe_load(open('$S/SKILL.md').read().split('---')[1])"` parses; `d['description']` ≤1,024 chars.
6. `measure.py skill $S/SKILL.md` reports `body_est_tokens` ≤ 4,000.
7. `sources_lint.py $P/evals/fixtures/report-{decision,topic,digest}.md --json` exits 0, `"ok": true` for all 3.
8. `find $P/evals/pubmed-research-note -mindepth 1 -maxdepth 1 -type d | wc -l` = 5; `test ! -f $S/evals/evals.json`.
9. `diff <(grep -o 'NCT NNNNNNNN[^)]*' $S/SKILL.md | head -1) <(grep -o 'NCT NNNNNNNN[^)]*' $P/references/report-contract.md | head -1)` empty (one NCT form, family-wide).
10. `grep -ic "atomize\|ทำโน้ต" $S/SKILL.md` = 0.

## 6. Trigger lock

| Phrase | Source | Kept / moved / removed |
|---|---|---|
| "research" | description | kept |
| "what does the literature say about" | description | kept |
| "search PubMed for" | description | kept |
| "is X true" | description | kept |
| "should I use X for Y" | description | kept |
| "หางานวิจัย" | description | kept |
| "ทบทวนหลักฐาน" | description | kept |
| "ค้น PubMed" | description | kept |
| "จริงหรือเปล่า" | description | kept |
| "just search" | body (opt-out, Step 0) | kept, moved to body — R3 bars process phrasing from the description |
| "don't interview me" | body (opt-out) | kept, body |
| "ไม่ต้องถาม" | body (opt-out) | kept, body |
| "atomize" | description + body | **removed** (§2.3 design note; closes the §2.8 collision) |
| "ทำโน้ต" | description + body | **removed**, same reason |
| "comprehensive review of X" | description (echoed) | removed; the real trigger lives in `evidence:comprehensive-review`'s own description (S04 to confirm) |

## 7. Risks and OD sensitivity

- **K-risk**: retiring the atomize path (§2.3) is this spec's one interpretive call beyond a literal defect fix; if S15's digest-report contract (unwritten) expects structured note-shaped data directly, §2.3 row 10 needs revisiting. Mitigated by §8.
- **OD3-b (keep 14 shells)**: `report-contract.md`/`engines.md` become `shared/` canonical files synced by `sync_shared.py --check` into this skill's own `references/`, not family-root files; `.mcp.json` stays a 3rd standing copy. W2's 3 steps are unaffected either way.
- **OD5-b (digest + sync by default)**: the File-step handoff (§2.6) becomes `REQUIRED-with-stop`, not `OPTIONAL`, and "digest <report>" fires automatically; §2.3's atomize retirement still holds, but Close would report the Supabase provenance count, not just the sink path.
- No OD9/OD10 sensitivity: this skill gets no alias skill either way.

## 8. Open questions

- **ASSUMES-1**: I01's `deliverable`/`exclusions`/`assumed defaults` map onto decision-brief slots 2/6 (§2.7, used in S03-W3-2). Check: read S01's I01 once written; a field-name mismatch needs a one-line edit, not a redesign.
- **ASSUMES-2**: S15's I09/I25 accept the 3 fixtures (S03-W3-5) by their stated filenames, with no `.meta.json` sidecar for a plain report. Check: read S15's spec once written.
- **ASSUMES-3**: S07's I11 sink accepts a `kind: decision` report shaped as in §2.7. Check: read S07's spec once written.
- **ARCH-CONFLICT**: none found. Retiring the atomize path is a reading of §5.2 + OD5, not a conflict — a design **resolution**, flagged per the writing rules rather than asserted silently.
- **Scheduling note, S11**: H45 stays open until W3 (§3) — I16.2 V3's readiness line should read "H44 closed; H45 tracked for W3", not "both closed". S11 to confirm.
