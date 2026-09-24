# Spec S15: digest-report and the research-notes inbox contract

| Field | Value |
|---|---|
| Repos | learn-hub |
| Units (today → target) | `plugins/digest-report` (+ `/digest-report`) → `.claude/skills/digest-report` (model-invocable) with `references/inbox-contract.md`; `research-notes/` inbox layout (`visuals/`, `.intake-log.jsonl`); `scripts/check-contract.mjs` + `scripts/lib/report-parse.mjs` (pure parser, vitest tests) |
| Waves | W2 (first among the learn-hub-consumers steps, arch §10 W2 "learn-hub consumers" list item 1) |
| Owner decisions assumed | OD5-a (inbox only; publish on "digest"), OD9-a (no dmi; model-invocable, no alias — digest-report keeps its own name), OD10-a (n/a — digest-report stays model-invocable, not user-only) |
| Defects closed | 12 of 12 assigned (HIGH: H15, H16) |
| Interfaces owned | I09, I10, I25 |
| Interfaces consumed | I04 (owner S03), I12 (owner S07), I13 (owner S13), I17 (owner S12), I21 (owner S21), I22 (owner S21) |
| Depends on specs | S03 (I04 fixtures + report-contract text must exist for `check-contract.mjs` to have something to check against; not a hard code dependency — S15 degrades to "warning" per I25 when the fixtures are absent) |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| Path | Lines | Bytes | Est. tokens | Role |
|---|---|---|---|---|
| `plugins/digest-report/.claude-plugin/plugin.json` | 7 | 516 | 158 | plugin manifest (retired this wave) |
| `plugins/digest-report/README.md` | 47 | 2,361 | 444 | plugin README (retired; content moves to the project skill's own README) |
| `plugins/digest-report/commands/digest-report.md` | 25 | 1,076 | 269 | `/digest-report` command (retired; project skill needs no command — it is invoked by name) |
| `plugins/digest-report/skills/digest-report/SKILL.md` | 207 | 11,266 (body) | 2,816 (body) + 248 (desc) | the skill body being rewritten |
| `research-notes/*.md` (3 files) | — | 76,435 / 38,761 / 29,943 | — | real inbox contents today: 1 report/1-shaped (`trazodone-…`, has `## Sources`), 2 frontmatter-less legacy documents |
| `research-notes/.intake-log.jsonl` | — | — | — | does not exist yet (created this wave) |
| `research-notes/visuals/` | — | — | — | does not exist yet (created by S16, read by this skill's survey only incidentally) |

Measured (`measure.py skill plugins/digest-report/skills/digest-report/SKILL.md`): `description.chars: 991`, `body_lines: 203`, `body_est_tokens: 2816`. No `evals/` directory under `plugins/digest-report/` — nothing to convert (§4.2).

`research-notes/` is **not** in `.gitignore` (`grep -n research-notes .gitignore` → no match) — confirms architecture §5.4 "git-tracked (verified: not ignored)".

### 1.2 Descriptions

| Skill | Chars | UTF-8 bytes | YAML valid? | `Use when` offset | `Not for` present? | Quoted trigger phrases |
|---|---|---|---|---|---|---|
| digest-report (today) | 991 | 1,001 | yes | 374 | yes | "digest this report", "digest the pending reports", "digest this review into notes", "turn this report into notes", "create notes from this report", "atomize" (bare word, no quote marks around it in the text but functions as a trigger term) |

`atomize` as a bare gate word is the OBS-flagged P0-2 collision (§1.4); it must not survive the rewrite — the family's publish word is now "digest" (arch §2.8).

### 1.3 Defects

| id | sev | H# | evidence (re-opened) | problem | fix step | wave |
|---|---|---|---|---|---|---|
| digest-report-1 | H | H15 | SKILL.md:88-90, :115-116 ("keep inline citations…"; no `## Sources` mention); contrast pubmed SKILL.md:211-224 (no inline citations, `## Sources` topic→DOI) | input contract contradicts I04 (S03); per-claim provenance from a new-format report has nowhere to go | S15-W2-2 (tolerant reader, §2.3 step 1) | W2 |
| digest-report-2 | H | H16 | `docs/digest-report-plugin-plan.md:67` "Delete `.claude/skills/digest-report/`"; `ls .claude/skills/digest-report` → none; plugin not in `enabledPlugins` | not loaded by default; every named route (ingest-infographic, ingest-animation, pubmed, CR, CLAUDE.md) dead-ends | S15-W2-1, S15-W2-2, S15-W2-3 (convert to project skill) | W2 |
| digest-report-3 | M | — | SKILL.md:165-167 "~40 min"; `sync-cache.mjs`, `apply-sync.mjs:234` show incremental skip | stale sync-cost claim contradicts sync-vault's incremental cache | S15-W2-2 (delete; point at I13) | W2 |
| digest-report-4 | M | — | README.md:38-39 `voice:qc -- --files …`; `voice-qc.mjs:36-39` errors without `--base`/`--worktree` | README and skill disagree; README's form fails with a usage error | S15-W2-2, S15-W2-4 (one commit-then-`--base` form everywhere) | W2 |
| digest-report-5 | M | — | SKILL.md:140-141 "needs the files committed"; no commit step exists; `voice-qc.mjs:43-44` worktree mode omits untracked files | voice QC cannot run as written: `--base` needs a commit that never happens; `--worktree` checks nothing for new files | S15-W2-2 (explicit `git add`+`commit` before QC) | W2 |
| digest-report-6 | M | — | SKILL.md:130-132 "topic id = kebab basename"; real digest of `trazodone-novel-and-latest-evidence.md` lives at `vault/trazodone-2026-evidence/` (`ls vault \| grep -i trazo`) | the "deterministic slug" claim is fiction; idempotency rests on the step-2 DB provenance query | S15-W2-2 (drop the claim; state the real rule) | W2 |
| digest-report-7 | M | — | SKILL.md:22-24 "digest what has not landed" vs `commands/digest-report.md:11-20` "stop and let the user pick … do not start on your own initiative" | "digest the pending reports" defined two conflicting ways | S15-W2-2 (one meaning: bare form always surveys+stops) | W2 |
| digest-report-8 | M | — | SKILL.md:173-176 `Get-CimInstance …` (Windows-only) | PowerShell-only process check in a skill also run in the Linux cloud container | S15-W2-2 (delete; point at I13) | W2 |
| digest-report-9 | L | — | SKILL.md:72-75 topic fields omit `source:`; `CLAUDE.md:214` `source: book\|research\|review\|digest; omitted → derived` | a review digested without it derives to `research` | S15-W2-2 (add the `source:` rule, §2.3 step 3) | W2 |
| digest-report-10 | L | — | no `\$` rule though §4 invites KaTeX (SKILL.md:92); no fetch-first; no readiness check (`CLAUDE.md:2480-2488`) | missing authoring/safety rules that bite digests | S15-W2-2 (add all three) | W2 |
| digest-report-11 | L | — | SKILL.md:44-48 "the live DB" (no tool/project named); `CLAUDE.md` Supabase project `juvoohejxuuvwolmgoep` | provenance SQL names no tool or project ref | S15-W2-2 (name `mcp__Supabase__execute_sql`, project id, local fallback) | W2 |
| digest-report-12 | L | — | measured `desc_chars=991`; SKILL.md:3 "…(reader, graph, mastery, review)"; `CLAUDE.md` Phase 4 "a knowledge-graph view … removed" | description near the hard cap, names a stale surface ("graph") | S15-W2-2 (new description, §2.2) | W2 |

All 12 assigned defects appear above exactly once. No deferrals.

### 1.4 Other findings

- **OBS "atomize" collision (P0-2, still open).** digest-report's description sides with the wrong gate word ("on 'atomize'"); `atomize-book` triggers on "atomize this book"; `vault-atomizer` owns `/atomize`. Fixed by dropping "atomize" from the trigger vocabulary (§2.2) — the word is "digest" (OD5/§2.8).
- **OBS report-format drift** — covered as digest-report-1 (H15); the OBS also implicates pk-plasma-animation's Sources format, which is S16's defect, not double-counted here.
- **OBS empty-vault handoff drift** — empty-vault (S07) no longer calls digest-report directly; it transfers into the inbox via `drain_plan.py` (I12), and digest-report's survey picks up what lands there. No direct handshake code needed (§2.6).
- **NEW.** The three real `research-notes/` files are informative fixtures: `trazodone-novel-and-latest-evidence.md` has no frontmatter, an H1 title, an italic date line, inline `(PMID NNNNNNN)` citations, and a `## Sources` heading of natural-language paragraphs (not I04 grammar). `psychiatry-high-yield-2026-07-22-to-08-11.md` has no frontmatter, no `## Sources`, and a `Window: <dates>` line — a lit-watch-shaped digest. Both are legacy and must parse without error (§2.3, §4.1).
- **NEW.** `vault/trazodone-2026-evidence/` already exists — digest-report has been run once by hand, under an author-chosen slug, not the report basename — the ground truth behind digest-report-6.

## 2. Target state

### 2.1 Location and tree (after W2)

```
.claude/skills/digest-report/
  SKILL.md
  README.md
  references/
    inbox-contract.md          # I09 + I10, owned here
scripts/
  check-contract.mjs            # I25 CLI
  lib/
    report-parse.mjs            # pure tolerant parser (I25's engine; also used by SKILL.md step 1)
    report-parse.test.mjs
  check-contract.test.mjs
evals/
  digest-report/<case>/         # §4.1
research-notes/                 # unchanged path, now formally the inbox (I09)
  <slug>.md
  visuals/                      # created by S16; digest-report's survey ignores it
  .intake-log.jsonl             # created on first successful write (I10)
plugins/digest-report/          # DELETED (plugin.json, README.md, commands/, skills/)
```

### 2.2 Frontmatter

```yaml
---
name: digest-report
description: >-
  Distills a finished markdown research report — report/1 or a legacy inline-citation
  report — into Learn vault atomic notes (one topic + notes per report), then syncs via
  sync-vault. Use when the user says "digest this report", "digest the pending reports",
  "turn this report into notes", "create notes from this report", or a report skill hands
  off its output on "digest". A bare invocation surveys research-notes/ for un-landed
  reports and stops. Not for PDFs (pdf-pipeline/ingest-article), books (atomize-book),
  slide decks (ingest-slides), splitting an existing /vault note (vault-atomizer), or
  filing a finished HTML asset (ingest-visual) — input is a markdown report; output is
  notes, never articles.
---
```

Measured (`measure.py textfile`): 705 chars / 711 UTF-8 bytes / ~176 tokens. `use_when_at`: 182 (within R4's ~250). `not_for_at`: 448. No `I`/`you`/`your` outside quotes, no `<`/`>`. Above the 600-char soft target (SHOULD) but under the 1,024 hard cap — the 5-way `Not for` list (R8) does not compress further without dropping a named sibling.

Kept trigger phrases: "digest this report", "digest the pending reports", "turn this report into notes", "create notes from this report". Dropped: "digest this review into notes" (redundant, §6), "atomize" (P0-2 fix, §1.4).

### 2.3 Body outline

| # | Target section | Source lines → disposition | Target lines / tokens |
|---|---|---|---|
| 1 | Intro + distiller rule | 6-14 → keep, trim (2 lines) | ~4 / ~30 |
| 2 | Input | 16-33 → keep, rewrite: name I09 as the canonical inbox source; keep the micky-artifact case verbatim (still a valid input shape, unaffected by this wave) | ~14 / ~180 |
| 3 | Step 1 — Read and classify (tolerant reader, **new**) | 37-40 (rewritten) → new: run `node scripts/lib/report-parse.mjs <path> --json`; branch on `.contract` (`report/1` vs `legacy`); branch on `.sourcesForm` (`i04-grammar` vs `inline-mixed` vs `none`) | ~16 / ~220 |
| 4 | Step 2 — Already digested? (DB provenance) | 42-59 → keep logic, rewrite the SQL to name the tool (fix digest-report-11) | ~16 / ~200 |
| 5 | Step 3 — Shape (one topic per report) | 61-76 → keep; **add** `source:` field rule (fix digest-report-9); **drop** the false "kind" inference-free assumption — set `kind` from step 1's parsed `.kind` | ~18 / ~230 |
| 6 | Step 4 — Atomize into notes | 77-126 → keep the body-writing rules (money `\$` addition, fix -10); **rewrite** citation handling: report/1 → no inline citations, `sources:` = basename + the `## Sources` lines the note covers; legacy → inline citations preserved verbatim, `sources:` = basename only | ~46 / ~560 |
| 7 | Step 5 — Ids (rewritten, drops the false claim) | 128-136 → rewrite: note `id` stays deterministic (`<topic-slug>-<slugified title>`); topic `id` is **author-chosen** (concise, kebab-case), reused verbatim on re-digest per step 2's provenance hit — never re-derived from the basename (fix digest-report-6) | ~10 / ~130 |
| 8 | Step 6 — Commit, then voice QC | 138-158 → **new**: `git add vault/<topic-slug>/` + `git commit`, then `npm run voice:qc -- --base HEAD~1 --files vault/<topic-slug>/`; drop the `--worktree` alternative entirely (fix digest-report-4, -5) | ~14 / ~170 |
| 9 | Step 7 — Sync | 160-179 → **delete** the ~40-min claim and the PowerShell check (fix digest-report-3, -8); replace with: "Run the `sync-vault` skill (I13) exactly as it defines the apply path, the completion tell, and the stop-verification recipe — this skill restates none of it." | ~4 / ~50 |
| 10 | Step 8 — Verify, log, report | 181-194 → keep the provenance-scoped SQL (name the tool, fix digest-report-11); **add**: write one `.intake-log.jsonl` line (I10) only after the count matches; the log line, not a direct call, is what a later `/empty-vault` transfer or `ingest-visual` reads | ~20 / ~250 |
| 11 | Guardrails | 196-207 → keep, add "never write an intake-log line before verification succeeds" | ~8 / ~100 |
| — | **Total** | | ~170 lines / ~2,100 tokens (down from 203 / 2,816) |

### 2.4 References

| File | Purpose | Load condition | Size target |
|---|---|---|---|
| `references/inbox-contract.md` | I09 + I10 full definition | "Before step 1 (read/classify) and step 8 (log), read `references/inbox-contract.md`" | ≤2,000 tokens |

### 2.5 Scripts

| Name | CLI | Input | JSON stdout shape | Exit codes | Tests |
|---|---|---|---|---|---|
| `scripts/lib/report-parse.mjs` | library (imported below), plus a guarded CLI (`invokedDirectly` check): `node scripts/lib/report-parse.mjs <path> --json` prints the `ReportParse` object and exits 0, or exits 1 with the error when the parse throws (critique C2-22 — the skill's Step 1 calls this CLI); exposes `parseReport(text: string) -> ReportParse` | raw file text | n/a (library) | n/a | `report-parse.test.mjs`: report/1 fixture, legacy-with-Sources (mirrors `trazodone-…md`), legacy-no-Sources (mirrors `psychiatry-high-yield-…md`), garbage/empty (throws a named error) |
| `scripts/check-contract.mjs` | `node scripts/check-contract.mjs [--dir <path>] [--json]`; `--help` | default dir (CX-7): the first of `$MICKY_TOOLS_DIR/plugins/evidence/evals/fixtures` (post-W3 skeleton) or `$MICKY_TOOLS_DIR/plugins/pubmed-research-note/evals/fixtures` (pre-W3, S03's `report-{decision,topic,digest}.md`) that exists; `--dir` overrides either | `{"checked":[{"file":"…","contract":"report/1\|legacy","kind":"decision\|topic\|digest\|null","ok":true}],"warnings":["…"]}` | `0` = every file parsed (legacy = pass); `1` = a file threw inside `parseReport`; `$MICKY_TOOLS_DIR` unresolved and no `--dir` → warning only, `warnings` non-empty, still exit `0` (I25 "absent micky = warning") | `check-contract.test.mjs`: temp `--dir` of 3 fixtures, asserts exit 0 + fields; asserts the `$MICKY_TOOLS_DIR`-absent path warns and exits 0; asserts the pre-W3/post-W3 fallback order |

`ReportParse` shape (the CLI prints exactly this object): `{contract: "report/1"\|"legacy", title: string, created: string\|null, kind: "decision"\|"topic"\|"digest"\|null, sourcesForm: "i04-grammar"\|"inline-mixed"\|"none", sources: string[], assumedLine: string\|null, bodyStartLine: number}`. Classification rules (also §2.3 step 3):

- `contract`: `"report/1"` iff a YAML frontmatter block is present **and** its `contract` key equals `report/1`; otherwise `"legacy"` (frontmatter present with no `contract` key, or no frontmatter block at all — both observed in the real inbox).
- `title`: frontmatter `title` if `contract: report/1`; otherwise the first `# ` line; a file with neither throws.
- `created`: frontmatter `created` if present; otherwise a `\d{4}-\d{2}-\d{2}` matched out of the first italic (`*…*`) line under the title; otherwise `null` (the caller falls back to file mtime and flags `[unverified created date]`).
- `kind`: frontmatter `kind` if present; otherwise inferred — a `Window: <dates>` line or dated-range header → `"digest"`; a `## Sources` heading plus a lede reading as a verdict → `"decision"`; multiple `## <N>.` numbered sections with no verdict lede → `"topic"`; otherwise `null` (caller omits the topic's `source:` field, §2.3 step 3).
- `sourcesForm`/`sources`: if a `## Sources` heading's lines each match I04's grammar (`<topic phrase> — [doi:…]`, `NCT NNNNNNNN — …`, `<topic> — <URL> (accessed …)`, `Title, edition — OLID`) → `"i04-grammar"`, `sources` = those lines verbatim. If `## Sources` exists but its lines are natural-language paragraphs with inline `(Author Year)`/`PMID NNNNNNN`/DOI fragments (the `trazodone-…` shape) → `"inline-mixed"`, `sources` = the report basename only (one-element array; no line-level split is attempted). If no `## Sources` heading exists at all (the `psychiatry-high-yield-…` shape) → `"none"`, `sources` = the report basename only.
- `assumedLine`: the first body line if it matches `^> ?Assumed: .* — say if wrong\.$` (I04, S03) or `^> ?Assumed: `, else `null`.

### 2.6 Handoffs

- **To sync-vault (REQUIRED, always available — a project skill in the same repo, not a cross-plugin OPTIONAL handoff):** the one CX-17 sentence, verbatim, owned by S13 (I13): "Publish through the `sync-vault` skill (same repo, always present). Follow its steps as written; do not restate them here."
- **No I01/I11-style OPTIONAL-with-fallback handoff is carried here.** digest-report does not call `alignment:intent-lock` (its steps are a fixed deterministic pipeline, not an open-ended request needing scope-lock) and does not call `vault-keeper` (it writes directly into `/vault`, the same repo, not across repos).
- **Filing sentence not applicable.** digest-report is a *consumer* of the inbox (I09), never a filer into it.

### 2.7 Interfaces

#### Owned: I09 — Inbox contract `research-notes/`

**Paths.**
- `research-notes/<slug>.md` — reports (both `report/1` and legacy).
- `research-notes/visuals/<slug>.html` + `research-notes/visuals/<slug>.meta.json` — visual assets (written and read by S16's `ingest-visual`; this skill's survey step lists but never opens them).

**Slug rule** (shared by every producer that writes into the inbox): kebab-case, deterministic from the source title — lowercase; spaces and punctuation other than `-` become `-`; collapse repeats; strip leading/trailing `-`; truncate to 80 chars at a `-` boundary. A producer MAY choose a shorter, more evocative slug by hand (digest-report-6 shows this is real practice for a report's own **topic** id — that choice is independent of the inbox filename slug, which stays mechanical).

**Collision suffix.** If the mechanical slug already names a file in the target directory with **different content** (different sha256), append `-2`, then `-3`, … up to `-50`; beyond that the writer stops and asks (same cap S07's `sink.py file` applies, §5.3 of the architecture — this is one rule, stated once, that both scripts implement).

**`.meta.json` schema** (visual assets only; reports carry no sidecar — a report's own I04 frontmatter is its metadata):

| Field | Type | Notes |
|---|---|---|
| `kind` | `"infographic"\|"animation"\|"explorable"` | |
| `title` | string | |
| `description` | string | one line |
| `topic_hint` | string \| `null` | a guessed topic id; the consumer (`ingest-visual`, S16) still resolves the real topic itself |
| `source_report` | string \| `null` | basename of the report this asset illustrates, if any |
| `producer` | string | the `plugin:skill` name at write time (CX-10), e.g. `"visuals:clinical-infographic"`, `"pk-plasma-animation:pk-plasma-animation"` |
| `created` | `YYYY-MM-DD` | |
| `audit` | `{tool: string, verdict: "pass"\|"incomplete"}` | the producer's own pre-file `audit:visual` (I08, S16) run. `verdict` is never `"fail"` (CX-10) — a producer that fails its own audit does not file at all (§2.3's "never file an asset whose audit fails," architecture §5.5); `"incomplete"` covers a partial verdict (e.g. Chromium missing, `skipped` non-empty, I08) that still files with a caveat |

**Who writes what, when.** A producer (a micky `visuals:*` skill via the sink, or `pk-plasma-animation` directly) writes the `.html` + `.meta.json` pair. `digest-report` never writes into `research-notes/visuals/` and never reads `.meta.json` bodies — it only lists filenames during its survey (§2.3 step, "un-landed reports"), which is report-only; visuals are `ingest-visual`'s (S16) domain exclusively.

**Git.** `research-notes/` (including `visuals/` and `.intake-log.jsonl`) is git-tracked — verified not ignored (§1.1). Every writer offers a commit in learn-hub immediately after writing, because cloud VMs are ephemeral (architecture §5.4).

#### Owned: I10 — Intake log `research-notes/.intake-log.jsonl`

Append-only, one JSON object per line, UTF-8, LF-terminated:

```json
{"file":"research-notes/trazodone-novel-and-latest-evidence.md","sha256":"<64 hex>","consumer":"digest-report","action":"digested","rows":8,"commit":"<sha or null>","at":"2026-09-24T10:03:00Z"}
```

| Field | Values | Written by |
|---|---|---|
| `file` | path relative to the repo root | both |
| `sha256` | sha256 of the file's bytes **at the moment this line is written** | both |
| `consumer` | `"digest-report"` \| `"ingest-visual"` | both |
| `action` | `"digested"` (a report, by digest-report) \| `"filed"` (a visual, by ingest-visual, S16) \| `"refused"` (either consumer, when it cannot land the item) | both |
| `rows` | integer — notes written and verified (digest-report) or `1`/`0` (ingest-visual) | both |
| `commit` | the learn-hub commit sha that includes the landed `/vault` files, or `null` if the commit offer was declined/not yet made | both |
| `at` | ISO 8601 UTC timestamp | both |

**When digest-report writes a line.** Once per successful digest, in §2.3 step 8, only after the provenance-scoped verification count equals the notes written (`action: "digested"`). A `refused` line (`report-parse.mjs` threw), `rows: 0`, is also written, so a repeated identical-sha attempt shows as "previously refused" rather than being silently retried — but a `refused` line does **not** block a future retry.

**Re-digest / survey semantics** ("un-landed" — the one meaning, fixing digest-report-7). A report counts as **landed** iff the log holds a line with `action: "digested"` whose `sha256` equals the file's *current* sha256. A bare invocation lists every `research-notes/*.md` file that is **not** landed (including files with only a `refused` line, or no line at all) and **stops** — it never digests on its own initiative. "digest the pending reports" (an explicit instruction naming ALL of them, not the bare form) digests every un-landed report found by that same rule, in listed order. "digest `<path>`" digests exactly that one, regardless of landed state (an explicit re-digest is always honoured — step 2's DB provenance check, not the log, is what prevents a duplicate topic).

#### Owned: I25 — `scripts/check-contract.mjs`

Full definition in §2.5. Consumer: S08's `validate.py --cross-repo` (per interfaces.md) runs it as part of the cross-repo check set when both clones are present.

#### Consumed

| Interface | Owner | What this spec assumes |
|---|---|---|
| I04 | S03 | Report/1 frontmatter keys, `Assumed:` grammar, `## Sources` per-kind grammar used in `report-parse.mjs`'s `i04-grammar` branch, reproduced read-only. `check-contract.mjs` defaults to the first existing of `plugins/evidence/evals/fixtures/report-{decision,topic,digest}.md` (post-W3) or `plugins/pubmed-research-note/evals/fixtures/report-{decision,topic,digest}.md` (pre-W3, written at S03-W2-4) — CX-7. **Confirmed** two-way: S03's own §2.7 names this exact path back (not open, §8). |
| I12 | S07 | `drain_plan.py` writes directly into the two I09 paths and only reads `.intake-log.jsonl` (I10) to check "already landed" — never writes a line itself (S07 §2.7). Confirmed consistent. |
| I13 | S13 | The preflight → background `sync:apply` → `EXIT=0`+`Upserted …` → revalidate sequence and the portable stop-verification recipe that this skill used to restate (fix -3, -8) and now only points at, using S13's exact CX-17 handoff sentence (§2.6). **CLOSED (CX-17)**: no further restatement — the sentence is the whole handoff. |
| I17 | S12 | Layout `evals/digest-report/<case>/`; tags `smoke\|trigger\|negative\|output\|release`; trigger regex per §4.1. **ASSUMES** `eval-project-skill.sh` is S12's runner (architecture §6.5). |
| I21 | S21 | The gotchas this skill used to restate (`~40 min`, the PowerShell check) are deleted, not moved to a local `references/gotchas.md` — they belong to sync-vault's (S13) ownership. No new gotcha content here. |
| I22 | S21 | No new `npm run` script — `check-contract.mjs` runs directly (`node scripts/check-contract.mjs`). **ASSUMES** S21 needs no entry for it (§8). |

## 3. Change steps

### S15-W2-1 — Write the inbox contract reference

- **Repo · depends on**: learn-hub · none
- **Files**: create `.claude/skills/digest-report/references/inbox-contract.md`
- **Change**: write the full I09 + I10 text from §2.7 above (paths, slug rule, collision suffix, `.meta.json` schema, log line schema, who-writes-what-when, git-tracking note).
- **Commands**: none (content write only)
- **Done when**: `python3 measure.py file .claude/skills/digest-report/references/inbox-contract.md` reports ≤2,000 est. tokens; `python3 -c "import yaml"`-free manual read confirms no `{{` placeholders remain.
- **Rollback**: `git rm .claude/skills/digest-report/references/inbox-contract.md`.

### S15-W2-2 — Write the rewritten SKILL.md

- **Repo · depends on**: learn-hub · S15-W2-1, S15-W2-5 (the skill runs `report-parse.mjs --json`; critique C2-22)
- **Files**: create `.claude/skills/digest-report/SKILL.md`
- **Change**: assemble the body per §2.3's outline and the frontmatter from §2.2. Delete (not reinterpret) SKILL.md:165-167 (sync-cost claim) and SKILL.md:173-176 (PowerShell check) per R19 subtraction. Add the `source:` topic field rule, the `\$` money rule (cite `CLAUDE.md:2480-2488`), the git-commit-before-voice-QC step, the named Supabase tool + project id (`juvoohejxuuvwolmgoep`) in both SQL steps, and the fetch-first + `node scripts/ready.mjs --json` readiness check as Step 0 (matching the pattern other W1-fixed skills use, per architecture §2.6 "Nothing repo-dependent runs in the setup script … pipeline skills also run `node scripts/ready.mjs --json` as an explicit Step 0 command").
- **Commands**:
  ```
  python3 measure.py skill .claude/skills/digest-report/SKILL.md
  ```
- **Done when**: the command above reports `description.chars` ≤ 1,024, `body_est_tokens` ≤ 2,500 (target from §2.3's total), `yaml_valid: true`; a manual grep confirms zero occurrences of `Get-CimInstance` and `~40 min`.
- **Rollback**: `git rm .claude/skills/digest-report/SKILL.md`.

### S15-W2-3 — Retire the plugin form

- **Repo · depends on**: learn-hub · S15-W2-2 (the project skill must exist before the plugin form is removed, so no window exists with neither loaded)
- **Files**: delete `plugins/digest-report/.claude-plugin/plugin.json`, `plugins/digest-report/README.md`, `plugins/digest-report/commands/digest-report.md`, `plugins/digest-report/skills/digest-report/SKILL.md`; remove the now-empty `plugins/digest-report/` directory tree.
- **Change**: `git rm -r plugins/digest-report`.
- **Commands**:
  ```
  git rm -r plugins/digest-report
  ls plugins | grep -c digest-report   # expect 0
  ```
- **Done when**: `ls plugins/digest-report` fails (No such file or directory); `.claude/skills/digest-report/SKILL.md` still exists.
- **Rollback**: `git checkout HEAD~1 -- plugins/digest-report` (restores the deleted tree from the previous commit).

### S15-W2-4 — Write the project-skill README

- **Repo · depends on**: learn-hub · S15-W2-2
- **Files**: create `.claude/skills/digest-report/README.md`
- **Change**: port `plugins/digest-report/README.md`'s content (position-in-pipeline diagram, usage, guarantees), fixing the voice-QC invocation to the single `git commit` → `npm run voice:qc -- --base HEAD~1 --files vault/<topic-slug>/` form (fix digest-report-4) and the pipeline diagram's "reader, graph, mastery, review" to "reader, mastery, review" (drop "graph" — fix digest-report-12's stale-surface half; the description fix is §2.2).
- **Commands**: none
- **Done when**: `grep -c "voice:qc -- --files" .claude/skills/digest-report/README.md` → 0 (the broken form is gone); `grep -c "graph" .claude/skills/digest-report/README.md` → 0.
- **Rollback**: `git rm .claude/skills/digest-report/README.md`.

### S15-W2-5 — Write the pure parser and its tests

- **Repo · depends on**: learn-hub · none (parallel with W2-1/2)
- **Files**: create `scripts/lib/report-parse.mjs`, `scripts/lib/report-parse.test.mjs`
- **Change**: implement `parseReport(text)` exactly per §2.5's classification rules, and the guarded `--json <path>` CLI (§2.5). Fixture texts for the test file are drawn from (a) a synthetic report/1 example matching S03's `report-decision.md` shape, (b) an inline copy of `research-notes/trazodone-novel-and-latest-evidence.md`'s opening 40 lines (real legacy-with-Sources shape), (c) an inline copy of `research-notes/psychiatry-high-yield-2026-07-22-to-08-11.md`'s opening 20 lines (real legacy-no-Sources shape), (d) an empty string and a title-less garbage string (both must throw a named `Error`, never return a partial object).
- **Commands**:
  ```
  npx vitest run scripts/lib/report-parse.test.mjs
  ```
- **Done when**: the command above exits 0 with 4+ passing cases (one per fixture class above) plus a CLI case (`--json` on a fixture file prints the object; a missing file exits 1); `node scripts/lib/report-parse.mjs <a fixture> --json | python3 -m json.tool` exits 0.
- **Rollback**: `git rm scripts/lib/report-parse.mjs scripts/lib/report-parse.test.mjs`.

### S15-W2-6 — Write check-contract.mjs and its tests

- **Repo · depends on**: learn-hub · S15-W2-5
- **Files**: create `scripts/check-contract.mjs`, `scripts/check-contract.test.mjs`
- **Change**: implement the CLI exactly per §2.5 (default dir, `--dir`, `--json`, `--help`, the three exit codes, the `$MICKY_TOOLS_DIR`-absent warning path).
- **Commands**:
  ```
  node scripts/check-contract.mjs --help
  npx vitest run scripts/check-contract.test.mjs
  ```
- **Done when**: `--help` exits 0 with no side effects (no file writes — verified by `git status --short` reporting nothing new); the vitest run passes, including the mocked-absent-`$MICKY_TOOLS_DIR` case exiting 0 with a non-empty `warnings` array.
- **Rollback**: `git rm scripts/check-contract.mjs scripts/check-contract.test.mjs`.

### S15-W2-7 — Evals

- **Repo · depends on**: learn-hub · S15-W2-2, S15-W2-5
- **Files**: create `evals/digest-report/<case>/{prompt.md,graders/*.md,case.yaml,fixtures/…}` per §4.1
- **Change**: the three full cases from §4.1, plus the table-only cases listed there.
- **Commands**:
  ```
  bash scripts/eval-project-skill.sh digest-report --smoke
  ```
- **Done when**: the smoke run reports all cases at or above the `pre-rewrite` baseline (there is no `pre-rewrite` baseline for this skill — it was never loaded, §1.1 — so "above baseline" here means "every grader passes", the W0-recorded floor for a previously-unloaded skill).
- **Rollback**: `git rm -r evals/digest-report`.

### S15-W2-8 — Confirm the Supabase MCP project id in a live cloud session

Executor step, not OWNER (critique P15, C2-29): a read-only MCP query that a cloud session can run.

- **Repo · depends on**: learn-hub · S15-W2-2
- **Files**: learn-hub `docs/rewrite/baseline.md`, `## Owner records` (record the H15/H16 closure verification; the W2 tag step closes the rows in `h-coverage.md`; CX-27 — the delivery log is for environment/plugin-delivery rows only)
- **Change**: none to the skill; a manual read-only verification.
- **Commands**: in a multi-repo cloud session, run the provenance query from §2.3 step 2 via `mcp__Supabase__execute_sql` with `project_id: juvoohejxuuvwolmgoep` against a known-digested report basename.
- **Done when**: the query returns rows; the result is recorded against H15/H16 in `docs/rewrite/baseline.md` `## Owner records`.
- **Rollback**: n/a (read-only; revert the record line if needed).

## 4. Evals

### 4.1 Cases

**Case 1 — trigger positive + tolerant parse of a legacy report** (`evals/digest-report/digest-legacy-report/`)

`prompt.md`:
```markdown
---
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
tags: [trigger, output]
---

Digest this report into vault notes: research-notes/legacy-sample.md
```

`case.yaml`:
```yaml
schema_version: "1.1"
name: digest-legacy-report
tags: [trigger, output]
context:
  add_dirs: [fixtures]
```

`fixtures/legacy-sample.md` (no YAML frontmatter, inline citations, natural-language `## Sources` — mirrors the real `trazodone-…md` shape):
```markdown
# Trazodone — Evidence Review (sample)
*2026-08-07 · sources: PubMed (primary)*

## TL;DR

- Trazodone at 25-75 mg blocks 5-HT2A, alpha1 and H1 receptors (Smith et al., J Clin
  Psychiatry 2025, PMID 40000001).

## Sources

- Smith J, et al. Dose-dependent receptor occupancy of trazodone. J Clin Psychiatry.
  2025. PMID 40000001.
```

`graders/skill-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?digest-report"'
weight: 2
---
```

`graders/tolerant-parse.md`:
```markdown
---
type: llm
focus: last_message
criteria: >-
  PASS if the response digested the sample report into one or more vault notes and
  preserved PMID 40000001 (or the author name) somewhere in a note body or its
  sources, rather than refusing the file for lacking report/1 `## Sources` grammar.
  FAIL if the run refused the file, dropped the citation, or fabricated a DOI.
weight: 3
---
```

**Case 2 — near-miss negative from the sibling family** (`evals/digest-report/near-miss-atomize-book/`)

`prompt.md`:
```markdown
---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
tags: [negative]
---

I have an EPUB of a psychiatry textbook, "Foundations of Clinical Psychopharmacology".
Turn the whole book into vault notes, chapter by chapter.
```

`graders/not-digest-report.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?digest-report"'
min: 0
max: 0
arm: both
---
```

**Case 3 — process: bare invocation surveys and stops** (`evals/digest-report/bare-invocation-survey/`)

`prompt.md`:
```markdown
---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
tags: [process]
---

digest the pending reports
```

`case.yaml`:
```yaml
schema_version: "1.1"
name: bare-invocation-survey
tags: [process]
context:
  scaffold_script: fixture.sh
```

`fixture.sh` (runs via `context.scaffold_script`, before the agent starts):
```bash
#!/usr/bin/env bash
set -euo pipefail
mkdir -p research-notes
cat > research-notes/sample-unlanded.md << 'EOF'
# Sample Unlanded Report
*2026-09-01*

## Sources

- topic — [doi:10.1000/xyz123](https://doi.org/10.1000/xyz123)
EOF
: > research-notes/.intake-log.jsonl
```

`graders/no-write.md`:
```markdown
---
type: tool_used
tool: Write
min: 0
max: 0
arm: both
---
```

`graders/no-sync-bash.md`:
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

`graders/names-the-report.md`:
```markdown
---
type: regex
target: last_message
pattern: 'sample-unlanded'
---
```

**Further cases (table only, per template §4.1):**

| Name | Tags | Prompt gist | Graders |
|---|---|---|---|
| `digest-report-1-parses` | output | Digest a synthetic report/1 fixture (frontmatter, `contract: report/1`, clean `## Sources`) | `tool_used: Skill`; `regex` over the note asserting no `(Author Year)` survives |
| `digest-explicit-pending-all` | output, process | "digest all pending reports", two un-landed fixtures | `tool_used: Skill`; `regex` for both basenames; `tool_order` Write before `sync:apply` |
| `near-miss-vault-atomizer` | negative | "split this long note into two" (an existing `/vault` note) | `tool_used: Skill` digest-report, `min:0 max:0 arm:both` |
| `near-miss-ingest-visual` | negative | "file this infographic HTML into the hub" | `tool_used: Skill` digest-report, `min:0 max:0 arm:both` |
| `money-dollar-rule` | output | Digest a fixture with a literal price ("$20 co-pay") | `regex`: `pattern: '\\\$20'` landed in the note body |

### 4.2 Conversion

No `evals.json` or any eval directory exists anywhere under `plugins/digest-report/` today (`find … -iname '*eval*'` → empty, §1.1). Nothing to convert; all cases in §4.1 are new.

### 4.3 Live triggers

Family membership (architecture §6.3): `{atomize-book, digest-report, anthropic-skills:obsidian-knowledge-vault}`.

Near-miss queries for this family (4, per the template's 2-4):
1. "atomize this chapter into notes" (should trigger `atomize-book`, not digest-report — different input, a book chapter, not a finished report)
2. "make an Obsidian note from this paragraph" (should trigger the claude.ai synced skill, not digest-report)
3. "split this note in half" (should trigger `vault-atomizer`, not digest-report — an existing `/vault` note, not a `research-notes/` report)
4. "digest the report at research-notes/trazodone-novel-and-latest-evidence.md" (should trigger digest-report — the true positive, included so the family query set has at least one genuine hit)

### 4.4 Commands

| Command | What |
|---|---|
| `bash scripts/eval-project-skill.sh digest-report --smoke` | smoke run, free graders only (CX-46) |
| `bash scripts/eval-project-skill.sh digest-report --release` | two-arm release run, at the W3/W5 exits per OD14 (CX-46) |
| `npx vitest run scripts/lib/report-parse.test.mjs scripts/check-contract.test.mjs` | unit tests |
| `node scripts/check-contract.mjs --json` | manual cross-repo contract check |

## 5. Acceptance criteria

1. `.claude/skills/digest-report/SKILL.md` exists and `claude plugin validate --strict` (run against learn-hub's `.claude/skills`, per architecture §8) reports no error for it.
2. `plugins/digest-report/` does not exist: `ls plugins/digest-report` exits non-zero.
3. `python3 measure.py skill .claude/skills/digest-report/SKILL.md` reports `description.chars` ≤ 1,024 and `use_when_at` ≤ 250.
4. `grep -c "Get-CimInstance\|~40 min" .claude/skills/digest-report/SKILL.md` → 0.
5. `npx vitest run scripts/lib/report-parse.test.mjs` passes, including the legacy-with-Sources and legacy-no-Sources fixture cases.
6. `node scripts/check-contract.mjs --dir plugins/pubmed-research-note/evals/fixtures --json` (once S03-W2-4 has written its fixtures, pre-W3) or `--dir plugins/evidence/evals/fixtures --json` (post-W3) exits 0 and reports `contract: "report/1"` for all three; with no `--dir`, the default picks whichever of the two exists (CX-7).
7. `node scripts/check-contract.mjs --dir /nonexistent --json; echo $?` with `$MICKY_TOOLS_DIR` unset reports a non-empty `warnings` array and exits 0.
8. Running digest-report against `research-notes/trazodone-novel-and-latest-evidence.md` (or a fixture in its shape) does not throw and does not silently drop its two citation-bearing claims (eval case `digest-legacy-report`, §4.1).
9. A bare "digest the pending reports" with no reports landed in `.intake-log.jsonl` calls neither `Write` nor a `sync:apply`/`npm run sync` `Bash` command (eval case `bare-invocation-survey`, §4.1).
10. `.claude/skills/digest-report/references/inbox-contract.md` contains the `.meta.json` field table and the intake-log line schema verbatim as in §2.7.

## 6. Trigger lock

| Phrase | Source | Kept / moved / removed |
|---|---|---|
| "digest this report" | description | kept |
| "digest the pending reports" | description | kept |
| "digest this review into notes" | description (today) | removed (redundant with "turn this report into notes"; a distinct phrasing was not shown to add coverage) |
| "turn this report into notes" | description | kept |
| "create notes from this report" | description | kept |
| "atomize" (bare gate-word reference) | description (today, SKILL.md:3) | removed — P0-2 collision fix; the family's publish word is "digest" (OD5), never "atomize" |
| "ingest this infographic" / "ingest this animation" | N/A (never digest-report's) | not this skill's — see S16 |

## 7. Risks and OD sensitivity

- **Risk**: `sourcesForm: "inline-mixed"` preserves citations verbatim. A future producer format not covered by the three-way classification makes `report-parse.mjs` throw rather than mis-split sources (visible failure over a silent wrong one). Mitigation: `check-contract.mjs` against S03's fixtures on every cross-repo validate.
- **OD5 sensitivity.** Under OD5-b (sync by default), the explicit-word gate (§2.3 step 7, §4.1 case 2) would be removed and producers would call digest-report unattended. Under the assumed OD5-a nothing else here changes — I09/I10 are unaffected either way.
- **OD9 sensitivity.** digest-report keeps its own name, model-invocable, not dmi, under both options — it is not one of OD9's short-verb aliases. No change.

## 8. Open questions

- **CLOSED (CX-17)** (I13, S13): the sync-vault handoff (§2.6) is now S13's fixed verbatim sentence, not a generic paraphrase.
- **ASSUMES** (I17, S12): `eval-project-skill.sh`'s flags (`--tag`, `--ablation`, `--runs`, `--threshold`) are taken from the micky `eval.sh` table by analogy. Settled by S12's §2.5.
- **Open**: should this spec pre-create `research-notes/visuals/` empty? Decided **no** — S16 creates it on first write, same as `.intake-log.jsonl` here.
- **ARCH-CONFLICT**: none. I10's `action: digested|filed|refused` list is followed as given; an initial reading worried a `refused` line might count as "landed" for survey purposes — resolved by scoping "landed" to `action: "digested"` lines only, consistent with the architecture text.
