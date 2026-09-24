# Spec S04: comprehensive-review and lit-watch (was psych-paper-digest)

| Field | Value |
|---|---|
| Repos | micky-psych-tools |
| Units (today → target) | `plugins/comprehensive-review` → `plugins/evidence/skills/comprehensive-review` (bare name unchanged, `argument-hint`). `plugins/psych-paper-digest` → `plugins/evidence/skills/lit-watch` + dmi alias `evidence:digest`. `scripts/sweep.py` (new, +tests). `state/lit-watch/{config.json,last_swept.json,digests/}` (new, replaces cwd state). |
| Waves | W0 (smoke seeds, CX-4); W1 (PPD search fixes H46/H47, today's layout); W2 (CR: OPTIONAL fallbacks, sink filing, interim report-contract copy aligned to S03's W2 text); W3 (lit-watch rename, `sweep.py`, `state/lit-watch/`, CR remaining fixes, interim copy deleted) |
| Owner decisions assumed | OD3-a, OD5-a, OD6-a (state in git-tracked `state/`), OD7-a (rename to `lit-watch`, `/digest` kept), OD8-a (owner edits synced skill; CR gains a Not-for), OD9-a, OD13-a |
| Defects closed | 25 of 25 (comprehensive-review 12, psych-paper-digest 13; HIGH: H46, H47) |
| Interfaces owned | I06 |
| Interfaces consumed | I01 (S01), I04 (S03), I05 (S03), I09 (S15), I11 (S07), I17 (S12), I20 (S08), I23 (S10) |
| Depends on specs | S01 (I01), S03 (I04/I05 — aligns CR's interim copy, deletes it at W3), S07 (I11), S08 (I20, validator), S10 (I18 W0 backfill, I23 move), S11 (I16), S12 (I17), S15 (I09) |

## 1. Current state (measured 2026-09-24)

Read in full: every file under `plugins/comprehensive-review/` and `plugins/psych-paper-digest/`; the synced `psych-paper-digest`/`daily-random-review` skills; live `mcp__Clinical_Trials__search_trials` schema (shared grounding with S03's I05).

### 1.1 Files

Paths relative to each plugin's own root.

| Path | Lines | Bytes | Est. tok | Role |
|---|---|---|---|---|
| CR `.claude-plugin/plugin.json` | 16 | 672 | 168 | version 0.3.0 |
| CR `.mcp.json` | 12 | 236 | 59 | byte-identical to S03's copy |
| CR `CHANGELOG.md` | 29 | ~1,400 | 350 | no history before 0.3.0 (defect-12) |
| CR `README.md` | 55 | 2,743 | 686 | |
| CR `commands/comprehensive-review.md` | 14 | 628 | 157 | wrapper, `argument-hint: "[disorder or topic]"` |
| CR `skills/comprehensive-review/SKILL.md` | 205 | 11,197 | 2,799 (body) | the skill |
| CR `.../references/review-arc.md` | 61 | 5,427 | 1,344 | coverage map, registry recipe (defect-8) |
| CR `skills/comprehensive-review/evals/evals.json` | 45 | 3,595 | — | 5 cases, `assertions: []` |
| PPD `.claude-plugin/plugin.json` | 16 | 639 | 160 | version 0.1.1 |
| PPD `.mcp.json` | 12 | 236 | 59 | byte-identical |
| PPD `CHANGELOG.md` | ~12 | ~700 | 175 | missing 0.1.1 entry (defect-9) |
| PPD `README.md` | 89 | 4,003 | 1,001 | stale cron claim (defect-8) |
| PPD `commands/digest.md` | 15 | 728 | 182 | |
| PPD `skills/psych-paper-digest/SKILL.md` | 162 | 8,127 | 2,032 (body) | the skill |
| PPD `.../references/sweep-recipes.md` | 93 | 4,541 | 1,124 | `pdat` default, no pagination (H46/H47) |
| PPD `.../references/config-schema.md` | 58 | 2,821 | 696 | schema, init flow, sanity rules |
| PPD `.../references/triage-rubric.md` | 57 | 3,021 | 748 | Act/Read/Suppressed criteria — healthy, no defect |
| PPD `skills/psych-paper-digest/evals/evals.json` | 101 | 7,084 | — | 12 cases, `assertions: []` |

CR mandatory refs = `review-arc.md` only (1,344 tok); body 2,799 tok — under the family's W3 targets. PPD mandatory refs = `sweep-recipes.md`+`triage-rubric.md` (not marked "read before" — defect-11) = 1,872 tok; body 2,032 tok.

### 1.2 Descriptions

CR: 1,020 chars (99.6% of cap), 255 tok, YAML valid, `use_when_at` **376** — an R4 violation (NEW, not previously numbered). `not_for_at` 824. Quoted: "comprehensive review of X", "full review of X", "whole-disorder review", "academic review", "review the whole topic", "รีวิวทั้งโรค", "should I use X for Y" (echoed for Not-for).

PPD: 939 chars, 235 tok, `use_when_at` 238 (within band), `not_for_at` 709. Quoted: "paper digest", "today's digest", "what's new in the literature", "anything new this week", "อัปเดตงานวิจัย", "มีเปเปอร์ใหม่ไหม", "add X to my watchlist", "show my watchlist".

### 1.3 Defects

| id | sev | evidence (re-opened) | problem | fix step | wave |
|---|---|---|---|---|---|
| comprehensive-review-1 | M | SKILL.md:132-133 no-number rule vs :35-36 thin-domain guidance | Conflicts with thin-domain instruction | S04-W3-2 | W3 |
| comprehensive-review-2 | M | SKILL.md:103-124 (Step 2), no engine-failure rule; contrast PPD :74-76 | No PubMed/CT.gov-down policy | S04-W2-2 (I04) | W2 |
| comprehensive-review-3 | M | SKILL.md:108 "source floors" vs :57 "capped by relevance, never by count" | Wording contradicts the no-ceiling rule | S04-W3-2 | W3 |
| comprehensive-review-4 | M | SKILL.md:64 "ALWAYS...FIRST"; :169-173 vault-keeper default, no absent-plugin path | No fallback when intent-lock/vault-keeper absent | S04-W2-1 | W2 |
| comprehensive-review-5 | L | SKILL.md:128 "Inherited from the house rules" — no such file | Cites a nonexistent file | S04-W2-2 | W2 |
| comprehensive-review-6 | L | SKILL.md:168,196 — no name/path rule | Output location/name unspecified | S04-W2-2 (I04 slug) | W2 |
| comprehensive-review-7 | L | SKILL.md:67-68 locks "length"; :160 forbids cutting content | Locked field with no mechanism | S04-W3-2 | W3 |
| comprehensive-review-8 | L | review-arc.md:23 "completed-no-results"; live `status` enum has no such value | Non-existent CT.gov status filter | S04-W3-2 (I05) | W3 |
| comprehensive-review-9 | L | description 1,020 chars incl. a non-sibling clause in `Not for` | Non-routing clause inside `Not for` | S04-W3-3 | W3 |
| comprehensive-review-10 | L | SKILL.md:99; review-arc.md:51-53 "past reviews...old budget" | Version-history narration | S04-W3-2 | W3 |
| comprehensive-review-11 | L | evals.json 5 entries, all `assertions: []`; no Thai/no-filesystem/opt-out cases | Prose-only evals, thin coverage | S04-W3-5 | W3 |
| comprehensive-review-12 | L | CHANGELOG.md:24 "0.2.0 and earlier...Pre-changelog releases" | No history before 0.3.0 | none — the note already discloses the gap; no earlier data to backfill | — |

| id | sev | H# | evidence (re-opened) | problem | fix step | wave |
|---|---|---|---|---|---|---|
| psych-paper-digest-1 | H | H46 | sweep-recipes.md:39-40 no `datetype` (default `pdat`) | Windows on pub date, misses late-indexed records | S04-W1-1 | W1 |
| psych-paper-digest-2 | H | H47 | sweep-recipes.md:39-40 `max_results:50`, no `retstart`; :92-93 "No silent drops" | Silent truncation beyond 50 | S04-W1-1 | W1 |
| psych-paper-digest-3 | M | — | sweep-recipes.md:65-68 "cannot date-filter directly"; live schema has `advanced_query`; "has-results" not a status | Misstates the CT.gov MCP tool | S04-W1-1 | W1 |
| psych-paper-digest-4 | M | — | config-schema.md:55-56 "3 consecutive sweeps"; schema (:7-20) has no history field | Rule needs state the schema doesn't keep | S04-W3-1 (I06 `zero_kept_streak`) | W3 |
| psych-paper-digest-5 | M | — | sweep-recipes.md:80-82 dedups vs the newest digest only | Breaks after a scoped run | S04-W3-1 (`sweep.py` overlap dedup) | W3 |
| psych-paper-digest-6 | M | — | synced `anthropic-skills:psych-paper-digest` shares name+triggers | Name collision | S04-W3-3 (rename) | W3 |
| psych-paper-digest-7 | M | — | config-schema.md:42-43 walk-up to `marketplace.json` | Fails silently outside the marketplace repo | S04-W3-1 (I06, `$MICKY_TOOLS_DIR`) | W3 |
| psych-paper-digest-8 | L | — | README.md:48 "no built-in cron" | Stale — Routines/cron exist | S04-W1-2 | W1 |
| psych-paper-digest-9 | L | — | plugin.json `"0.1.1"`; CHANGELOG has only `## 0.1.0` | Missing 0.1.1 entry | S10-W0-8 | W0 |
| psych-paper-digest-10 | L | — | SKILL.md:94 collision suffix; :81 "take the newest" (mtime vs lexical undefined) | Ambiguous filename/ordering rules | S04-W3-1 (`sweep.py`) | W3 |
| psych-paper-digest-11 | L | — | SKILL.md:80-81 points at triage-rubric.md, not "read before" | Rubric not a stated load condition | S04-W3-4 | W3 |
| psych-paper-digest-12 | L | — | SKILL.md:50-58,72-73,92-97; failure list :170-171,176 — all in prose | Deterministic mechanics not scripted | S04-W3-1 (`sweep.py`) | W3 |
| psych-paper-digest-13 | L | — | evals.json ids 6,7,9 need live literature/engine states | Ungradeable, prose-only | S04-W3-6 | W3 |

### 1.4 Other findings

- Step-0 dependency unguaranteed (no `dependencies` mechanism) — same T4/§4.2 fix as S03, at S04-W2-1.
- MCP duplication — CR's/PPD's `.mcp.json` both byte-identical to S03's; W3 moves all three to one `plugins/evidence/.mcp.json` (S03 owns the file; this spec's W3-1 deletes CR's and PPD's copies).
- digest-report/empty-vault cross-repo drift is S15/S07 territory, not acted on here beyond citing I04/I05/I09/I11.
- **NEW**: live `mcp__Clinical_Trials__search_trials` schema (shared grounding with S03) confirms comprehensive-review-8 exactly: no `completed-no-results` value, `advanced_query` supports `AREA[Field]RANGE[min,max]`.
- **NEW**: `daily-random-review`'s synced SKILL.md never actually invokes `comprehensive-review` (only description text and prose at :13/:128, no Skill call) — its "chains into...internally" claim is inaccurate. OD8's fix removes a false handoff impression, not a working one.

## 2. Target state

### 2.1 Location and tree (after W3)

```
plugins/evidence/
  skills/
    comprehensive-review/{SKILL.md, references/review-arc.md, evals/}
    lit-watch/{SKILL.md, references/{sweep-recipes,config-schema,triage-rubric}.md, evals/}
    digest/{SKILL.md}                 # dmi alias → lit-watch, ≤10-line body
  scripts/sweep.py test_sweep.py   # + sources_lint.py etc. from S03
  references/report-contract.md engines.md   # S03's I04/I05; CR + lit-watch both link them
state/lit-watch/
  config.json          # domains[]: name,label,query,trials_term,floor,zero_kept_streak
  last_swept.json       # {"<domain>": "<YYYY-MM-DD>"}, sweep.py-owned only
  digests/digest-YYYY-MM-DD.md   # moved from cwd; git-tracked
```
`sweep-recipes.md` is trimmed to CT.gov/PubMed recipe specifics; MCP-resolution text moves to S03's `engines.md`, per the family pattern.

### 2.2 Frontmatter

`comprehensive-review` (unchanged name):
```yaml
---
name: comprehensive-review
description: >-
  Writes a textbook-chapter academic review of a whole psychiatric disorder or topic from
  primary literature — every coverage domain present or consciously excluded, structure
  designed per topic, never silently narrowed to a treatment essay. Use when asked for
  "comprehensive review of X", "full review of X", "whole-disorder review", "review the
  whole topic", or "รีวิวทั้งโรค". Not for: one clinical decision (use
  evidence:pubmed-research-note), watchlist surveillance (use evidence:lit-watch).
argument-hint: "[disorder or topic]"
metadata:
  profile: cc
---
```
Measured (`measure.py text`): 519 chars, 130 tok, `use_when_at` 189 (fixes the R4 violation), `not_for_at` 400. Dropped: "Runs intent-lock FIRST...", "Searches PubMed and ClinicalTrials.gov itself", "chat gets a short summary" (R3 process/output prose), "writing into vault/ directly (vault-keeper owns paths)" (not a sibling — moved to body).

`lit-watch` (renamed from `psych-paper-digest`):
```yaml
---
name: lit-watch
description: >-
  Sweeps every domain on the user's watchlist for literature published since the last
  sweep and delivers a triaged, read-once digest — practice-changing first, then
  worth-reading, plus registry readouts; noise suppressed with counts. Use when the user
  says "paper digest", "today's digest", "what's new in the literature", "anything new
  this week", "อัปเดตงานวิจัย", "มีเปเปอร์ใหม่ไหม", or asks to manage the watchlist. Not
  for: one named topic or clinical decision (use evidence:pubmed-research-note); a daily
  8-12 paper cross-subspecialty digest with no watchlist (use
  anthropic-skills:psych-paper-digest).
metadata:
  profile: cc
---
```
Measured: 588 chars, 147 tok, `use_when_at` 173, `not_for_at` 396. Dropped: "Initializes its config on first run", "Triage only, never adjudication..." (R3 process prose, moved to body Standing rules). New Not-for clause names the synced skill by id (fixes SKL-55/psych-paper-digest-6 reciprocally — the synced skill's own Not-for is owner-edited, OD7-a, not this spec's job).

`digest` (new dmi alias skill, `plugins/evidence/skills/digest/SKILL.md`):
```yaml
---
name: digest
description: Alias for evidence:lit-watch.
disable-model-invocation: true
argument-hint: "[domain]"
---
Invoke `evidence:lit-watch` with: $ARGUMENTS
```
5-line body per I20's alias template (OD9-a).

### 2.3 Body outline

Actions: keep | cut (reason) | move → file | script → name | new.

**CR SKILL.md, W2** (target ≤230 lines):

| # | Section | Source | Action |
|---|---|---|---|
| 1 | Title, boundary statement | :18-27 | keep |
| 2 | Prime directive, depth contract | :29-60 | keep |
| 3 | `## Step 0` | :62-77 | insert §2.6's OPTIONAL-fallback sentence as the unavailable branch; drop "locks...length" (defect-7, no I01 field); keep audience/emphasis/exclusions |
| 4 | `## Step 1` (coverage map) | :79-101 | keep |
| 5 | `## Step 2` (search) | :103-124 | append I04's engine-failure policy by pointer (defect-2); NCT/citation aligned to the interim copy below |
| 6 | `## The citation contract` | :126-139 | ":128 house rules" → "Per the report contract"; body becomes the **interim copy** of S03's W2 report-contract text (deleted W3) |
| 7 | `## The review` template | :141-157 | frontmatter block replaces the dated-line + Assumed/Skipped pair (I04, `kind: topic`) |
| 8 | `## Where output goes` | :164-177 | File step → §2.6 sink sentence |
| 9 | `## Handoffs` | :179-190 | add Not-for `anthropic-skills:daily-random-review` (OD8-a) |
| 10 | `## Close`/`## Failure conditions` | :192-222 | keep; drop the "length" failure item |

**CR, W3**: :126-139's interim copy → a pointer at `../../references/report-contract.md`; :108 "source floors" → "evidence types" (defect-3); :132-133's no-number rule scoped past thin domains (defect-1); :99, review-arc.md:51-53 narration cut (defect-10); Not-for trimmed (defect-9, §2.2). `review-arc.md:23` registry recipe → `status: [COMPLETED]` + `get_trial_details` (defect-8, mirrors S03's I05).

**PPD, W1** (today's layout): H46 — add `datetype: "edat"` to `search_articles` calls. H47 — `retstart`-paginated loop, per-domain cap (default 200), header reports `screened N (capped: yes/no)`. CT.gov (defect-3) — `search_trials` recipe → `advanced_query: 'AREA[ResultsFirstPostDate]RANGE[<from>,<to>]'`, drops "cannot date-filter" and `has-results`. README.md:48 (defect-8) struck.

**Timezone note** (task-directed "UTC+7 stated"): Step 1's `date_to = today` is ambiguous when the session clock is UTC. Add: "`today` = the calendar date in Thailand local time (UTC+7), computed explicitly rather than read off the raw system date." Without it, a run between 17:00–23:59 UTC windows one day short.

**PPD → lit-watch, W3**: rename throughout; config/state moves from cwd `.psych-paper-digest.json` to `$MICKY_TOOLS_DIR/state/lit-watch/{config.json,last_swept.json}` (I06, R47, defect-7); render/mark-swept logic → `sweep.py` (defects 4,5,10,12); "Before Step 3, read `triage-rubric.md`" added (defect-11); Not-for the synced skill added (defect-6); vault filing stays explicit-request-only.

### 2.4 References

| File | Purpose | Load condition | Size target |
|---|---|---|---|
| `comprehensive-review/references/review-arc.md` | Coverage map, per-domain recipes | "Read before outlining (Step 1)" | ≤70 lines / ≤1,400 tok |
| `lit-watch/references/sweep-recipes.md` | Engine recipes (MCP-resolution text moved to `engines.md`) | "Read before the first sweep call" | ≤75 lines / ≤950 tok |
| `lit-watch/references/config-schema.md` | State schema (points to I06), init flow, sanity rules | "Read before Step 0" | ≤65 lines / ≤800 tok |
| `lit-watch/references/triage-rubric.md` | Act/Read/Suppressed criteria | "Before Step 3, read..." (new — had none) | unchanged, 57 lines |
| `../../references/report-contract.md` (S03, family) | I04 | CR: "before writing `## Sources`" | shared read |
| `../../references/engines.md` (S03, family) | I05 | both: "before the first tool call" | shared read |

### 2.5 Scripts

**`scripts/sweep.py`** (family script, `plugins/evidence/scripts/`):

| Field | Value |
|---|---|
| CLI | `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/sweep.py <plan\|write\|dedup\|zero-streak> ...` |
| `plan --domain <name>\|--all` | Read-only. Computes each domain's window from `last_swept.json` (14-day inaugural if null; 90-day cap with `capped: true` if stale) and Thailand-local `today` (UTC+7). JSON: `{"domains":[{"name","date_from","date_to","inaugural","capped"}]}`. |
| `dedup --domain <name> --date-from <d> --date-to <d>` | Read-only. Globs `state/lit-watch/digests/digest-*.md`, keeps files whose own header window **overlaps** `[date_from,date_to]` for that domain, unions their DOI/PMID/NCT ids (regex-extracted). JSON: `{"seen_ids":[...]}`. Fixes defect-5. |
| `write --domain <name> --date <YYYY-MM-DD> --content <path>` | Writes `digests/digest-<date>.md` (date-based name, mtime+lexical agree; collision → `-2`,`-3` — defect-10), THEN advances `last_swept.json[domain]` — never before the write succeeds. `--dry-run` skips both. Fixes defect-4/10/12. |
| `zero-streak --domain <name> --increment\|--reset` | Reads/writes `zero_kept_streak` in `config.json` (defect-4 — makes "3 consecutive sweeps" checkable: `--increment` on a 0-kept sweep, `--reset` otherwise; nudge fires at streak ≥3). |
| Exit codes | 0 clean; 1 bad args/no state dir; 2 `$MICKY_TOOLS_DIR` unresolved (R47) |
| Tests | inaugural/normal/capped windows; dedup overlap (adjacent/disjoint/identical); write-then-advance ordering (a forced write failure leaves `last_swept.json` untouched); collision suffix; zero-streak increment/reset |

Non-interactive; `--help` exits 0; dry-run default for `write`; UTF-8, trailing newline; no network calls (state/file mechanics only — the search calls stay in the skill, R63).

### 2.6 Handoffs

CR Step 0 / File step — identical §4.2 pattern as S03 (§2.6 there); plugin segment per wave (CX-16): `intent-lock:intent-lock` at W2 (S04-W2-1, before S10's skeleton PR exists), `alignment:intent-lock` from W3 (S04-W3-3):
> Run `intent-lock:intent-lock` (OPTIONAL). If it is not available in this session — or it needs an interactive picker and none exists here (subagent, headless, scheduled run) — do not stall: take the broadest reading that fits the request and open the review with one line `Assumed: <reading> — say if wrong.`
> File via `vault-keeper` (OPTIONAL). If absent, write to `$LEARN_HUB_DIR/research-notes/` when its marker validates, otherwise to cwd, and say where.

lit-watch's vault-keeper handoff stays **explicit-request-only** ("vault this digest"), same OPTIONAL sentence when it fires. lit-watch does **not** chain `intent-lock` (unchanged — init's own interview is the only elicitation it owns).

**K6 — the W2 exit's unattended `daily-random-review` pass.** That synced skill never calls `Skill(comprehensive-review)` (§1.4 NEW) — it only copies CR's old structure in prose, so the run completes regardless of CR's fallback wiring. §2.6's fallback buys forward safety: if a future OD8 edit does invoke CR by name unattended, Step 0 takes the broadest reading and proceeds rather than stalling, exactly as pubmed-research-note's does.

### 2.7 Interfaces

**I06 — lit-watch state (owned in full).**

`state/lit-watch/config.json`:
```json
{
  "domains": [
    {"name": "child-adhd", "label": "Child & adolescent ADHD",
     "query": "<PubMed field-tagged query, no dates>", "trials_term": "<plain text>",
     "floor": "high", "zero_kept_streak": 0}
  ]
}
```
`name`/`label`/`query`/`trials_term`/`floor` are user-editable (unchanged from today's config, minus `digest_dir`/`last_swept`, moved out); `zero_kept_streak` is written only by `sweep.py zero-streak` (defect-4).

`last_swept.json`: `{"<domain>": "<YYYY-MM-DD>"}` — key absent = never swept; written only by `sweep.py write`, only after the digest write succeeds.

`digests/digest-YYYY-MM-DD.md`: today's body grammar plus I04 frontmatter (`kind: digest`, `contract: report/1`). Collision → `-2`, `-3`.

Root resolution: `$MICKY_TOOLS_DIR`, marker-validated (R47); unresolved → `sweep.py` exits 2, skill stops and asks (no cwd fallback — a lost `last_swept.json` silently re-sweeps or skips windows, so it must not degrade quietly). Git-tracked (OD6-a); `sweep.py write` prints a commit-offer line, mirroring S03's report-filing offer. CLI: §2.5.

**Consumed, all ASSUMES unless noted (§8 tracks the load-bearing ones):**

| Interface | Owner | What this spec assumes |
|---|---|---|
| I01 | S01 | CR's Step 0 reads `audience`/`emphasis`/`exclusions` from the lock record, same pattern as pubmed-research-note (S03 §2.7). |
| I04 | S03 | Report frontmatter (`kind: topic`/`digest`), one NCT form, depth contract, engine-failure policy, slug rule — as S03 §2.7 defines. |
| I05 | S03 | Runtime MCP resolution + `datetype`/`retstart`/`advanced_query` — as S03 §2.7 defines, used for W1's H46/H47 and defect-3/-8. |
| I09 | S15 | CR reports and lit-watch digests land in `research-notes/` with no `.meta.json` sidecar — same assumption as S03. |
| I11 | S07 | Filing sentence: "report, `sink.py --kind report`" (CX-8) — the sink accepts `kind: topic`/`digest` artifacts and returns a landing path. |
| I17 | S12 | Layout `plugins/evidence/evals/{comprehensive-review,lit-watch}/<case>/`; same tags/regex form as S03. |
| I20 | S08 | House shape (§2.2/§2.3); the `digest` alias's 5-line body matches S08's alias template — S08 to confirm. |
| I23 | S10 | The W3 skeleton-PR step moves+renames both plugins into `plugins/evidence/skills/{comprehensive-review,lit-watch}/` before this spec's W3 steps run. |

## 3. Change steps

Path shorthand: `C` = `plugins/comprehensive-review` (W2 location); `Q` = `plugins/psych-paper-digest` (W1 location); `P` = `plugins/evidence`; `S1`/`S2` = `$P/skills/comprehensive-review` / `$P/skills/lit-watch` (W3 locations, after S10's move).

### Wave W0

**S04-W0-1** · depends on: S12-W0-3
- Files: create `$Q/evals/psych-paper-digest/<case>/{prompt.md,graders/*.md}` (3 cases: trigger positive, near-miss negative, one output case, mined against today's skill; I17 layout; every `prompt.md` carries `smoke` in `tags`; each case directory takes the name of one of §4.1's cases, so the later eval step extends these directories instead of adding new ones (critique P2, P7) — the lit-watch §4.1 set, which S04-W3-6 moves to `$P/evals/lit-watch/`).
- Change: seed the pre-rewrite smoke baseline for psych-paper-digest.
- Commands / done when: S12-W0-5's check for this unit — `find . -path '*/evals/psych-paper-digest/*' -name prompt.md | xargs grep -l 'tags:.*smoke' | wc -l` ≥ 3.
- Rollback: `git rm -r $Q/evals/psych-paper-digest`.

**S04-W0-2** · depends on: S12-W0-3
- Files: create `$C/evals/comprehensive-review/<case>/{prompt.md,graders/*.md}` (3 cases; plugin-root `evals/`, not inside the skill directory; I17 layout; every `prompt.md` carries `smoke` in `tags`; each case directory takes the name of one of §4.1's cases, so the later eval step extends these directories instead of adding new ones (critique P2, P7)).
- Change: seed the pre-rewrite smoke baseline for comprehensive-review.
- Commands / done when: S12-W0-5's check for this unit — `find . -path '*/evals/comprehensive-review/*' -name prompt.md | xargs grep -l 'tags:.*smoke' | wc -l` ≥ 3.
- Rollback: `git rm -r $C/evals/comprehensive-review`.

### Wave W1 (repo: micky-psych-tools; plugin stays at `$Q/`)

**S04-W1-1** · depends on: none
- Files: edit `$Q/skills/psych-paper-digest/references/sweep-recipes.md`, `$Q/skills/psych-paper-digest/SKILL.md`.
- Change: H46 — add `datetype: "edat"` to every `search_articles` call description. H47 — add `retstart` pagination with a per-domain cap, header reports `screened N (capped: yes/no)`. Defect-3 — CT.gov recipe → `advanced_query: 'AREA[...]RANGE[...]'`, drop `has-results`. Add the UTC+7 `today` note (§2.3). CX-6 — replace the hardcoded MCP prefix text at `SKILL.md:64-65` and `sweep-recipes.md:8-9` with S03's I05 runtime-resolution sentence, verbatim (§2.7 there): "Use the PubMed / ClinicalTrials tool present in this session: `mcp__PubMed__*` / `mcp__Clinical_Trials__*` (connector) or `mcp__plugin_*_pubmed__*` / `mcp__plugin_*_clinical-trials__*` (plugin). If neither is listed, run ToolSearch for 'pubmed' once. If still none, use E-utilities / CT.gov API v2 via WebFetch."
- Commands / done when: `grep -c "datetype" $Q/skills/psych-paper-digest/references/sweep-recipes.md` ≥ 1; `grep -c "retstart" $Q/skills/psych-paper-digest/references/sweep-recipes.md` ≥ 1; `grep -c "has-results\|cannot date-filter" $Q/skills/psych-paper-digest/references/sweep-recipes.md` = 0; `grep -c "mcp__plugin_" $Q/skills/psych-paper-digest/SKILL.md $Q/skills/psych-paper-digest/references/sweep-recipes.md` = 0.
- Rollback: `git checkout -- $Q/skills/psych-paper-digest/references/sweep-recipes.md $Q/skills/psych-paper-digest/SKILL.md`.

**S04-W1-2** · depends on: none
- Files: edit `$Q/README.md`.
- Change: strike the "no built-in cron" claim (defect-8, R18).
- Commands / done when: `grep -c "no built-in cron" $Q/README.md` = 0.
- Rollback: `git checkout -- $Q/README.md`.

**S04-W1-3** · depends on: S04-W1-1, S04-W1-2
- Change: release the W1 fixes — `python3 scripts/bump.py psych-paper-digest patch --write`.
- Files: `$Q/.claude-plugin/plugin.json`, `$Q/CHANGELOG.md` (entry: "H46/H47 fixes: `datetype`, pagination, runtime MCP resolution."). `.claude-plugin/marketplace.json` is not touched: S10-W0-3 removed every entry `version` (I18, CX-12).
- Done when: `python3 scripts/validate.py` prints `all checks passed`; `marketplace.json` has no `version` key for this entry.
- Rollback: `git checkout -- $Q/.claude-plugin/plugin.json $Q/CHANGELOG.md`.

W1 exit: `claude plugin validate --strict $Q` exits 0; H46/H47 closed (psych-paper-digest-1, -2); defects -3, -8 closed.

### Wave W2 (repo: micky-psych-tools; CR stays at `$C/`)

**S04-W2-1** · depends on: S15-W2-2 (the tolerant reader must exist before this step writes against it — consumers before producers, CX-35)
- Files: edit `$C/skills/comprehensive-review/SKILL.md`.
- Change: §2.3 row 3 (Step 0 fallback sentence, drop "length"); row 8 (File step → sink sentence); row 9 (Not-for `anthropic-skills:daily-random-review`, OD8-a). CX-6 — replace the hardcoded MCP prefix text at `SKILL.md:103-107` with S03's I05 runtime-resolution sentence, verbatim (§2.7 there, quoted in S04-W1-1 above).
- Commands / done when: `grep -c "OPTIONAL" $C/skills/comprehensive-review/SKILL.md` ≥ 2; `grep -c "locks.*length\|length.*locks" $C/skills/comprehensive-review/SKILL.md` = 0; `grep -c "mcp__plugin_" $C/skills/comprehensive-review/SKILL.md` = 0.
- Rollback: `git checkout -- $C/skills/comprehensive-review/SKILL.md`.

**S04-W2-2** · depends on: S04-W2-1, S03-W2-4 (`report-contract.md`/I04 fixtures must exist before this step aligns CR's interim copy to them — CX-7)
- Files: edit `$C/skills/comprehensive-review/SKILL.md`.
- Change: §2.3 row 6 — `## The citation contract` becomes the interim copy of S03's W2 report-contract text (one NCT form, engine-failure policy, depth contract by pointer within this file since the family file doesn't exist yet); "Inherited from the house rules" (defect-5) removed; row 7's frontmatter/`contract: report/1` block (defect-6's slug rule follows I04).
- Commands / done when: `grep -c "house rules" $C/skills/comprehensive-review/SKILL.md` = 0; `grep -c "contract: report/1" $C/skills/comprehensive-review/SKILL.md` = 1.
- Rollback: `git checkout -- $C/skills/comprehensive-review/SKILL.md`.

**S04-W2-3** · depends on: S04-W2-1, S04-W2-2
- Change: release the W2 fixes — `python3 scripts/bump.py comprehensive-review minor --write`.
- Files: `$C/.claude-plugin/plugin.json`, `$C/CHANGELOG.md` (entry: "OPTIONAL fallbacks, sink filing, interim report-contract copy, runtime MCP resolution."). `.claude-plugin/marketplace.json` is not touched: S10-W0-3 removed every entry `version` (I18, CX-12).
- Done when: `python3 scripts/validate.py` prints `all checks passed`; `marketplace.json` has no `version` key for this entry.
- Rollback: `git checkout -- $C/.claude-plugin/plugin.json $C/CHANGELOG.md`.

**S04-W2-5 (new, critique P12)** [OWNER] · depends on: S04-W2-1 (CR carries its Not-for) · runs before S04-W2-4
- Files: none in either repo (the skill is claude.ai-synced; only the owner can edit it, SKL-55).
- Change: OD8-a — the owner edits the synced `anthropic-skills:daily-random-review` so that its "chains into the comprehensive-review … skills internally" wording becomes "follow the structure below" (architecture §4.2 row, V8).
- Done when: the owner confirms the edit is saved; the date and the new sentence are recorded in micky `docs/rewrite/baseline.md` under `## Owner records`.
- Rollback: the owner restores the previous sentence.

**S04-W2-4** [OWNER] · depends on: S11-W2-2 (the plugin must be cloud-enabled before an unattended run can be observed), S04-W2-5
- Files: none (verification step).
- Change: OWNER runs `anthropic-skills:daily-random-review` once unattended and confirms it completes without stalling (K6, §2.6) — the check the W2-exit note (below) promises but no scripted step performs.
- Commands: none scriptable.
- Done when: OWNER confirms the run completed and records the result in micky `docs/rewrite/baseline.md` under `## Owner records` (the delivery log accepts only variable rows, I16.4).
- Rollback: n/a.

W2 exit: `claude plugin validate --strict $C` exits 0; defects -2,-4,-5,-6 closed; K6's unattended-run note (§2.6) holds, verified by S04-W2-4. CR is a W2-exit cloud-delivery candidate per §2.7's V3 row — §8 repeats S03's "check the closed-defect set, not just the plugin list" caution.

### Wave W3 (depends on S10-W3-2 — the skeleton-PR step moving `$C`→`$S1` and `$Q`→`$S2`, I23)

**S04-W3-1** · depends on: S10-W3-2
- Files: create `$P/scripts/sweep.py` + `test_sweep.py` (CX-42 — `-p 'test_*.py'` matches this name, not `sweep.py.test.py`), `state/lit-watch/{config.json,last_swept.json}` (seeded from `.psych-paper-digest.json`, `digest_dir` dropped), `state/lit-watch/digests/` (existing files `git mv`-ed in); edit `$S2/references/{sweep-recipes,config-schema}.md` to point at I06.
- Change: implement §2.5's CLI; migrate config per §2.7 (adds `zero_kept_streak: 0`); fixes defects 4, 5, 7, 10, 12.
- Commands / done when: `python3 -m unittest discover -s $P/scripts -p 'test_*.py'` all-green; `python3 $P/scripts/sweep.py plan --all` prints valid JSON with every configured domain.
- Rollback: `git mv state/lit-watch/digests/*.md . && git rm -r $P/scripts/sweep.py $P/scripts/test_sweep.py state/lit-watch`.

**S04-W3-2** · depends on: S10-W3-2, S01-W3-2
- Files: edit `$S1/SKILL.md`, `$S1/references/review-arc.md`.
- Change: §2.3's "CR, W3" row — interim citation-contract copy → pointer at `../../references/report-contract.md`; "source floors"→"evidence types"; no-number rule scoped past thin domains; CT.gov recipe → `status: [COMPLETED]` + `get_trial_details`; narration cut.
- Commands / done when: `grep -c "house rules\|source floors\|completed-no-results" $S1/SKILL.md $S1/references/review-arc.md` = 0.
- Rollback: `git checkout -- $S1/SKILL.md $S1/references/review-arc.md`.

**S04-W3-3** · depends on: S10-W3-2, S12-W3-2
- Files: edit `$S1/SKILL.md` frontmatter, `$S2/SKILL.md` (rename throughout); verify `$P/skills/digest/SKILL.md` matches §2.2's text (S10-W3-2 already creates the family's alias skills — CX-1; this step does not create the file, only checks it); edit `docs/rewrite/triggers.lock.json`.
- Change: CR description → §2.2's text (defect-9, R4). lit-watch: `name:` + description → §2.2's text, self-references renamed, Not-for the synced skill (defect-6). Re-key the trigger-lock rows for the renamed skill: `python3 scripts/rewrite_gate.py triggers remove --skill psych-paper-digest --reason "renamed to lit-watch (OD7-a)" --write` then `python3 scripts/rewrite_gate.py triggers extract --skill lit-watch --write` (S12 §2.5 CLI; CX-54 — a `triggers.lock.json` row keyed `skill: psych-paper-digest` fails VAL-06 once the skill is renamed).
- Commands / done when: `measure.py skill $S1/SKILL.md` → `use_when_at` ≤ 260; `grep -v "anthropic-skills" $S2/SKILL.md | grep -c "psych-paper-digest"` = 0; `diff <(cat $P/skills/digest/SKILL.md) <(§2.2's text)` empty; `grep -c '"skill": "psych-paper-digest"' docs/rewrite/triggers.lock.json` = 0.
- Rollback: `git checkout -- $S1/SKILL.md $S2/ docs/rewrite/triggers.lock.json`.

**S04-W3-4** · depends on: S10-W3-2
- Files: edit `$S2/SKILL.md`.
- Change: add "Before Step 3, read `references/triage-rubric.md`" (defect-11).
- Commands / done when: `grep -c "triage-rubric.md" $S2/SKILL.md` ≥ 2.
- Rollback: `git checkout -- $S2/SKILL.md`.

**S04-W3-5** · depends on: S04-W3-3
- Files: delete `$S1/evals/evals.json`; create `$P/evals/comprehensive-review/<case>/{prompt.md,graders/*.md}` per §4.1.
- Change: mine the 5 old prompts as seeds; add the Thai-trigger case (defect-11); land at 3-5 cases.
- Commands / done when: `test ! -f $S1/evals/evals.json`; `find $P/evals/comprehensive-review -mindepth 1 -maxdepth 1 -type d | wc -l` between 3 and 5.
- Rollback: `git checkout -- $S1/evals/evals.json && git rm -r $P/evals/comprehensive-review`.

**S04-W3-6** · depends on: S04-W3-3, S04-W3-1
- Files: first `git mv $P/evals/psych-paper-digest $P/evals/lit-watch` (the S04-W0-1 seeds; update their trigger graders' skill name to `lit-watch`); delete `$S2/evals/evals.json`; create the remaining `$P/evals/lit-watch/<case>/{prompt.md,graders/*.md}` per §4.1.
- Change: mine the 12 old prompts as seeds (drop ids 6,7,9 — defect-13, ungradeable); mocks assert `datetype: edat` and `retstart` presence (H46/H47 regression guard).
- Commands / done when: `test ! -f $S2/evals/evals.json`; `find $P/evals/lit-watch -mindepth 1 -maxdepth 1 -type d | wc -l` between 3 and 5.
- Rollback: `git checkout -- $S2/evals/evals.json && git rm -r $P/evals/lit-watch`.

W3 exit: all 6 steps done; both descriptions pass R3-R5; `sweep.py` tests green; both eval dirs populated, no `evals.json`; every remaining defect closed. No OWNER-marked steps. Per S11's I16 item 4 template: "Ready for cloud delivery: HIGH defects due by this wave closed (H46, H47, closed at W1); handoffs carry the §4.2 fallback or target an enabled plugin; no same-named unit elsewhere; smoke suite passed (<result path>)."

### Wave W5

**S04-W5-1 (new, critique P13)** [OWNER] · depends on: W3 exit + 2–4 weeks of use (architecture §10 W5)
- Files: `plugins/evidence/skills/lit-watch/SKILL.md` (only if flipped), `plugins/evidence/CHANGELOG.md`.
- Change: OD10 usage decision for lit-watch — run `/skill-doctor` and `/doctor`; if lit-watch fired rarely or never, add `disable-model-invocation: true` (user-only; `/digest` still works through the alias); else leave it model-invocable.
- Done when: the decision and its evidence (fire count from `/skill-doctor`) are in `plugins/evidence/CHANGELOG.md`; after a flip, `python3 plugins/plugin-creator/scripts/validate.py --repo .` prints `all checks passed`.
- Rollback: revert the flip.

## 4. Evals

### 4.1 Cases

3 full cases per skill (trigger positive, near-miss negative, output/process). Paths under `plugins/evidence/evals/<skill>/`.

**CR Case 1 — `comprehensive-review/trigger-whole-disorder/`** (trigger positive):

`prompt.md`:
```markdown
---
tags: [comprehensive-review, trigger, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Write]
max_turns: 20
---

Write me a comprehensive review of intermittent explosive disorder.
```

`graders/skill-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?comprehensive-review"'
arm: both
---
```

`graders/coverage-preserved.md`:
```markdown
---
type: llm
criteria: >-
  PASS if the output covers multiple coverage domains (definition, epidemiology,
  etiology, clinical features, diagnosis, comorbidity, treatment, special populations,
  prognosis, controversies) — either present or explicitly named as excluded — and does
  NOT collapse into a treatment-only essay. FAIL if treatment absorbs the whole review
  with no other domain addressed.
focus: last_message
---
```

**CR Case 2 — `negative-single-decision/`** (near-miss negative, pubmed-research-note's territory):

`prompt.md`:
```markdown
---
tags: [comprehensive-review, negative]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 10
---

Should I use prazosin for PTSD nightmares in my patient this afternoon?
```

`graders/not-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?comprehensive-review"'
min: 0
max: 0
arm: both
---
```

**CR Case 3 — `output-report-contract/`** (output/process — I04 compliance):

`prompt.md`:
```markdown
---
tags: [comprehensive-review, output, release]
allowed_tools: [Read, Glob, Grep, Skill, Write]
max_turns: 20
---

Comprehensive review of treatment-resistant schizophrenia — write it to a file.
```

`graders/frontmatter-and-sources.md`:
```markdown
---
type: regex
target: { source: file, path: "*.md" }
pattern: 'contract:\s*report/1'
weight: 2
---
```

`graders/no-house-rules-reference.md`:
```markdown
---
type: regex
target: { source: file, path: "*.md" }
pattern: 'house rules'
match: not_contains
---
```

`graders/wrote-via-write-tool.md`:
```markdown
---
type: tool_used
tool: Write
min: 1
---
```

Further CR case: `thai-trigger` (trigger, tags `[comprehensive-review,trigger]`) — prompt "รีวิวทั้งโรค PTSD ให้หน่อย"; graders: `tool_used Skill` positive, `llm` PASS on coverage as Case 1.

**lit-watch Case 1 — `lit-watch/trigger-full-sweep/`** (trigger positive):

`prompt.md`:
```markdown
---
tags: [lit-watch, trigger, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Write]
max_turns: 20
---

Give me today's paper digest.
```

`graders/skill-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?lit-watch"'
arm: both
---
```

`graders/digest-shape.md`:
```markdown
---
type: regex
target: { source: file, path: "digest-*.md" }
pattern: '## Act[\s\S]*## Read[\s\S]*## Suppressed'
---
```

**lit-watch Case 2 — `negative-single-topic/`** (near-miss negative, pubmed-research-note's territory):

`prompt.md`:
```markdown
---
tags: [lit-watch, negative]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 10
---

What does the literature say about ketamine for treatment-resistant depression?
```

`graders/not-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?lit-watch"'
min: 0
max: 0
arm: both
---
```

**lit-watch Case 3 — `output-datetype-and-pagination/`** (output/process — H46/H47 regression guard):

`prompt.md`:
```markdown
---
tags: [lit-watch, output, release]
allowed_tools: [Read, Glob, Grep, Skill, Write]
max_turns: 20
---

Sweep my watchlist.
```
(This case supplies its own case-scoped `mocks/pubmed/search_articles.md` — S03's I05 design — with `expect: {datetype: /^edat$/}` and >50 matching records for one domain, forcing both the `datetype` check and pagination.)

`graders/datetype-edat.md`:
```markdown
---
type: tool_used
tool: mcp__PubMed__search_articles
input_match: '"datetype"\s*:\s*"edat"'
min: 1
---
```

`graders/retstart-paginated.md`:
```markdown
---
type: tool_used
tool: mcp__PubMed__search_articles
input_match: '"retstart"\s*:\s*(?!0\b)\d+'
min: 1
---
```

### 4.2 Conversion

**comprehensive-review** (5 old → 3-5 new):

| Old case (id, name) | New case dir | Dropped (reason) |
|---|---|---|
| 1 `positive-trigger` | `trigger-whole-disorder` (seed) | — |
| 2 `negative-trigger` | `negative-single-decision` (seed) | — |
| 3 `negative-trigger-surveillance` | — | redundant with lit-watch's own near-miss; owned by S12's live set |
| 4 `adaptive-structure-coverage-held` | folded into Case 1's `llm` rubric | redundant coverage |
| 5 `depth-over-compression` | folded into Case 3 | I04's depth contract graded there |

**lit-watch / psych-paper-digest** (12 old → 3-5 new):

| Old case (id, name) | New case dir | Dropped (reason) |
|---|---|---|
| 1 `positive-trigger-full-sweep` | `trigger-full-sweep` (seed) | — |
| 2, 3 negative-trigger variants | `negative-single-topic` (seed) | same near-miss shape |
| 4 `first-run-init`, 11 `scoped-domain-run` | — | good W4/S12 candidates; not required for 3-5 |
| 5 `catch-up-window-capped` | — | covered by `sweep.py`'s own unit tests, not a behavioural eval |
| 6, 7, 9 live-state-dependent cases | — | ungradeable deterministically (defect-13); a mock-error variant is a W4/S12 candidate |
| 8 `registry-readout-section` | folded into `output-datetype-and-pagination`'s mock | CT.gov coverage added there instead |
| 10 `vault-gate-delegation` | — | same OPTIONAL-fallback pattern as S03's `sink-fallback-no-vault-keeper`; not required twice per family |
| 12 `thai-trigger-and-watchlist-management` | — | S12's live Thai-trigger set already covers the family |

### 4.3 Live triggers

Family (arch §6.3), same set S03 names: `{pubmed-research-note, comprehensive-review, lit-watch, anthropic-skills:psych-paper-digest, anthropic-skills:deep-research, anthropic-skills:daily-random-review}`. Near-miss queries (feeding S12's set):
- "Sweep my watchlist for anything new" → `evidence:lit-watch`, not `comprehensive-review`
- "Give me today's psychiatry paper digest across all subspecialties" → `anthropic-skills:psych-paper-digest` (no watchlist), not `evidence:lit-watch`
- "Pick a random topic and review it for my board vault" → `anthropic-skills:daily-random-review`, not `evidence:comprehensive-review`
- "Full academic review of generalized anxiety disorder" → should-trigger here

### 4.4 Commands

Smoke/release: `bash scripts/eval.sh --smoke evidence` / `--release evidence` (S10's wrapper, same as S03 §4.4 — one suite covers the whole `evidence` plugin including this spec's two skills). Neither runs from this spec (hard constraint).

## 5. Acceptance criteria

`P` = `plugins/evidence`; `C1`/`C2` = `$P/skills/{comprehensive-review,lit-watch}`; `Q` = `plugins/psych-paper-digest`.

1. `claude plugin validate --strict $P` (post-W3) exits 0.
2. `grep -c "datetype" $Q/skills/psych-paper-digest/references/sweep-recipes.md` ≥ 1 (post-W1, pre-move).
3. `grep -c "house rules" $C1/SKILL.md` = 0; `grep -c "contract: report/1" $C1/SKILL.md` = 1.
4. `measure.py skill $C1/SKILL.md` → description `chars` ≤ 1,024, `use_when_at` ≤ 260.
5. `measure.py skill $C2/SKILL.md` → `name: lit-watch`; description `chars` ≤ 1,024.
6. `python3 -m unittest discover -s $P/scripts -p 'test_*.py'` all-green.
7. `test -f state/lit-watch/config.json`; `test -f state/lit-watch/last_swept.json`; `grep -c "zero_kept_streak" state/lit-watch/config.json` ≥ 1.
8. `find $P/evals/comprehensive-review -mindepth 1 -maxdepth 1 -type d | wc -l` between 3-5; same for `$P/evals/lit-watch`; neither old `evals.json` remains.
9. `test -f $P/skills/digest/SKILL.md`; `grep -c "disable-model-invocation: true" $P/skills/digest/SKILL.md` = 1.
10. `grep -c "completed-no-results\|has-results" $C1/references/review-arc.md $Q/skills/psych-paper-digest/references/sweep-recipes.md` = 0.

## 6. Trigger lock

| Phrase | Source | Kept / moved / removed |
|---|---|---|
| "comprehensive review of X" / "full review of X" / "whole-disorder review" / "review the whole topic" / "รีวิวทั้งโรค" | CR description | kept |
| "should I use X for Y" | CR description (echoed for Not-for) | kept, unchanged role |
| "paper digest" / "today's digest" / "what's new in the literature" / "anything new this week" / "อัปเดตงานวิจัย" / "มีเปเปอร์ใหม่ไหม" | PPD→lit-watch description | kept |
| "add X to my watchlist" / "show my watchlist" | lit-watch description | kept |
| "just write it" / "don't interview me" / "ไม่ต้องถาม" | CR body (opt-out) | kept, body — moved out of description scope per R3 (same pattern as S03) |
| "ALWAYS runs intent-lock FIRST...", "Searches PubMed and ClinicalTrials.gov itself", "chat gets a short summary" | CR description | **removed** (R3 process/output prose) |
| "Initializes its...config on first run", "Triage only, never adjudication" | PPD description | **removed** (R3 process prose), sense kept in body Standing rules |
| `psych-paper-digest` as a bare skill name | plugin/skill name | **renamed** to `lit-watch` (OD7-a); `/digest` typed invocation kept via the new alias skill (OD9-a) |

## 7. Risks and OD sensitivity

- **OD3-b (keep 14 shells)**: `sweep.py`/`state/lit-watch/` unaffected; `report-contract.md`/`engines.md` become `shared/`-synced copies per skill's own dir, as S03 §7.
- **OD6-b/c (per-machine, not git-tracked)**: I06's root moves off `$MICKY_TOOLS_DIR`; cloud sessions start `last_swept.json` fresh each time, so H47's 90-day cap fires more often — document, not a defect.
- **OD7-b/c (rename the synced skill, or keep both names)**: under (c), W3-3's rename step is skipped in favour of sharpening both Not-for clauses.
- **OD8-b (CR gains a board-prep mode)**: a second output shape (textbook-sourced, no Sources block, no inbox filing) with its own eval — a W4/S12 follow-up, out of this spec's scope.
- **OD5-b (digest + sync by default)**: CR's File-step handoff becomes `REQUIRED-with-stop`; lit-watch's already-opt-in digest filing is unaffected.

## 8. Open questions

- **ASSUMES-1**: I01's `audience`/`emphasis`/`exclusions` are read by CR the same way pubmed-research-note reads `deliverable`/`exclusions` (S03 §2.7). Check: read S01's I01 once written.
- **ASSUMES-2**: S07's I11 sink accepts `kind: topic`/`digest` like `kind: decision`. Check: read S07's spec once written.
- **ASSUMES-3**: S08's alias template (I20) produces the same 5-line body used across families' aliases. Check: read S08's spec; a mismatch needs a one-line reformat, not a redesign.
- **Scheduling note, S11**: CR's W2-exit closes defects -2,-4,-5,-6, leaving -1,-3,-7..-11 open until W3 — its I16.2 readiness sentence should not overclaim, same caution as S03.
- **ARCH-CONFLICT**: none. The `daily-random-review` "never calls CR" finding (§1.4 NEW) supports OD8-a's fix rather than conflicting with it.
