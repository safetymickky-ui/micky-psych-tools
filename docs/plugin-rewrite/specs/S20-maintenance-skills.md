# Spec S20: learn-hub user-only maintenance skills

| Field | Value |
|---|---|
| Repos | learn-hub |
| Units (today → target) | `plugins/vault-atomizer` (+ `/atomize`) → `.claude/skills/vault-atomizer` (dmi); `plugins/vault-vectors` (+ `/vectors`) → `.claude/skills/vault-vectors` (dmi) + `.claude/skills/vectors` (dmi alias); `.claude/skills/vault-coverage` → same path, fixed + dmi; `.claude/skills/check-repetition` → same path, fixed + dmi |
| Waves | W1 (vault-coverage: `BOOK_ROOT`, source map, stale text — it already loads today), W2 (vault-atomizer/vault-vectors converted to project skills; check-repetition rewrite; all four flip to user-only, OD10) |
| Owner decisions assumed | OD9-a (dmi aliases kept — the `/vectors` alias), OD10-a (mixed: these four user-only) |
| Defects closed | 19 of 19 assigned (no HIGH ids — none of this spec's defects reached Appendix A) |
| Interfaces owned | none |
| Interfaces consumed | I13 (owner S13), I17 (owner S12), I20 (owner S08), I21 (owner S21), I22 (owner S21), I27 (owner S11) |
| Depends on specs | S19 (atomize-book's own checklist item for `coverage-sources.json`, referenced not redefined), S11 (I27 `BOOK_ROOT` contract), S13 (I13 sync-tail wording) |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| path | lines | bytes | est. tokens | role |
|---|---|---|---|---|
| `plugins/vault-atomizer/skills/vault-atomizer/SKILL.md` | 211 | 11,386 | 2,828 | split-note pipeline, never loaded (plugin, no catalog registration) |
| `plugins/vault-atomizer/commands/atomize.md` | 20 | 1,143 | 282 | thin `/atomize` forward — dropped (OD9, collides with atomize-book) |
| `plugins/vault-atomizer/.claude-plugin/plugin.json` | 7 | 383 | 95 | plugin manifest, deleted with the plugin form |
| `plugins/vault-vectors/skills/vault-vectors/SKILL.md` | 153 | 8,109 | 2,013 | embed + report pipeline, never loaded |
| `plugins/vault-vectors/commands/vectors.md` | 19 | 1,097 | 270 | thin `/vectors` forward — becomes a dmi alias skill instead |
| `plugins/vault-vectors/.claude-plugin/plugin.json` | 6 | 217 | 54 | plugin manifest, deleted with the plugin form |
| `.claude/skills/vault-coverage/SKILL.md` | 126 | 7,556 | 1,878 | already a project skill, already loads today |
| `.claude/skills/check-repetition/SKILL.md` | 101 | 6,071 | 1,505 | already a project skill, already loads today |
| `scripts/split-note.mjs` | 241 | 11,051 | 2,751 | vault-atomizer's engine (untouched by this spec) |
| `scripts/vector-report.mjs` | 886 | 39,232 | 9,779 | vault-vectors' engine (untouched except the doc-path finding below) |
| `scripts/check-repetition.mjs` | 321 | 11,985 | 2,991 | check-repetition's engine (untouched) |
| `scripts/lib/coverage-map.mjs` | 291 | 13,378 | 3,333 | source-map lookup; line 264 is the "not in the source map" string vault-coverage-1 evidences |
| `scripts/scrape/coverage-sources.json` | — | — | — | the source map itself: 26 entries today (§1.4) |

### 1.2 Descriptions

| skill | yaml_valid | desc chars | `Use when`/`Use for` at | `Not for` at | quoted triggers |
|---|---|---|---|---|---|
| `vault-atomizer` | true | 643 | -1 ("Use for", not "Use when") | 419 | `/atomize`, "this note is too long", "split this note", "atomize the vault", "which notes should be split", "break this chapter into atomic notes" |
| `vault-vectors` | true | 484 | -1 ("Use for") | 327 | `/vectors`, "embed the new notes", "create vectors for new notes", "backfill embeddings", "are any notes missing a vector", "vector report", "check similar-notes coverage" |
| `vault-coverage` | true | 659 | 102 | 476 | "measure coverage", "coverage report", "did we lose anything from <book>", "/vault-coverage", "what did the notes miss", "run the coverage baseline", "check <book> for gaps" |
| `check-repetition` | true | 387 | 210 | -1 (none) | `/check-repetition`, "check repetition", "find repeated content in the vault", "is this import repetitive" |

`check-repetition` has no `Not for` clause (confirms check-repetition-1). `vault-atomizer`/`vault-vectors` say "Use for" where R3 specifies "Use when" — a wording defect neither the digest nor architecture names by id; noted as **NEW** in §1.4 and folded into the rewrite since both descriptions are being replaced anyway.

### 1.3 Defects — every assigned id, exactly once

| id | sev | evidence (re-opened) | problem | fix step | wave |
|---|---|---|---|---|---|
| vault-atomizer-1 | M | `node scripts/split-note.mjs --list --limit 3` → "1681 split candidate(s) of 4532 notes (≥1500 words, ≥3 sections)"; SKILL.md:99-103 cites atomize-book's ≥1,200-word depth floor | the ≥1,500-word survey criterion overlaps the depth floor: a flagged note split into 2 children can each land under 1,200 (THIN) | S20-W2-1 | W2 |
| vault-atomizer-2 | M | SKILL.md:9-10 "291 of 2,979 notes… worst 7,893 words"; measured now 1,681 of 4,532, worst 10,943 (`actinf-continuous-time-dynamical-systems`) | stale time-sensitive stats in the opening argument | S20-W2-1 | W2 |
| vault-atomizer-3 | M | SKILL.md:157 `npm run sync:apply && npm run revalidate && npm run vectors:missing` | foreground `&&` chain contradicts the repo rule (background job + log) and the sibling skills | S20-W2-1 | W2 |
| vault-atomizer-4 | L | SKILL.md:169-171 "`vectors:missing` is not optional: children reach the DB with `embedding is null`"; `apply-sync.mjs:366-393` embeds every changed note it writes | false premise — `sync:apply` already embeds changed notes; `vectors:missing` covers only DB rows with no vault file | S20-W2-1 | W2 |
| vault-atomizer-5 | L | SKILL.md:105 "`summary` is load-bearing — it is the graph hover text" | stale UI reference; the graph view was removed | S20-W2-1 | W2 |
| vault-atomizer-6 | L | SKILL.md:197-199 "the hub still holds the original text in its children" | garbled — the hub does not hold the children's text; a split moves each section to exactly one owner | S20-W2-1 | W2 |
| vault-atomizer-7 | L | SKILL.md:196 "Do one, sync, look at it in the app, then decide." | unactionable in a cloud session with no browser — no mechanism named | S20-W2-1 | W2 |
| vault-atomizer-8 | L | `find plugins/vault-atomizer -type f` → plugin.json, commands/atomize.md, SKILL.md only | no README, CHANGELOG or evals | S20-W2-1 | W2 |
| vault-vectors-1 | M | commands/vectors.md:10 "Sync anything new, embed only the notes that have no vector" vs SKILL.md:56-57 "syncing is outside this skill's remit" | the command's default path claims to sync; the skill says syncing must be asked for first | S20-W2-2 | W2 |
| vault-vectors-2 | L | commands/vectors.md:15 `--no-report`; SKILL.md never mentions it; `vectors:check` always writes the report | the command defines a flag the skill never handles | S20-W2-2 | W2 |
| vault-vectors-3 | L | SKILL.md:50 "Writes `docs/note-vector-report.md`"; tracked; **`vector-report.mjs:64-73` shows `--no-verify` writes the UNVERIFIED path `scripts/.out/vector-report-unverified.md` (gitignored) instead**, reserving the tracked doc for a VERIFIED run | SKILL.md misdescribes which file the fast path writes — the script already avoids dirtying the tree; the doc is wrong, not the design | S20-W2-2 | W2 |
| vault-vectors-4 | L | SKILL.md:82 "~2,400 notes… ~15 minutes"; :137 "2,400 notes x 384 floats"; :152 "0 created, all 2,434 already present"; :142 "~350 notes" | stale corpus sizes and timings | S20-W2-2 | W2 |
| vault-vectors-5 | L | commands/vectors.md:11 "Normally under a minute." vs SKILL.md:73 "First run downloads the ~130 MB model; expect a slow start" | the command's timing promise conflicts with the skill's own first-run caveat | S20-W2-2 | W2 |
| vault-vectors-6 | L | SKILL.md:42 "If you are behind, merge `origin/master` before going further." | an unguarded git write instruction on the user's own branch | S20-W2-2 | W2 |
| vault-coverage-1 | M | `coverage-sources.json` → 26 entries; 70 distinct `book:` values in vault; SKILL.md:31-33 | 44 of 70 books report "not in the source map"; no import skill is told to add entries | S20-W1-1 | W1 |
| vault-coverage-2 | M | SKILL.md:40 `BOOK_ROOT="C:/Users/User/Desktop/Learn" node …`; `ls Book "raw book"` → absent here | hardcoded Windows path in the primary command; cannot run in the cloud environment (I27) | S20-W1-1 | W1 |
| vault-coverage-3 | L | SKILL.md:69 "Last run: **all four passed**"; findings dated 2026-07-28 at 2,290 notes | time-sensitive "last run" status presented as current | S20-W1-1 | W1 |
| check-repetition-1 | L | description has no `Not for`; atomize-book SKILL.md:956-980 uses `measure-redundancy.py` + `detect-duplicates.mjs` and never mentions `repetition:check` | missing negative scope against sibling redundancy tools (`npm run similarity:detect`, atomize-book §7b) — routing left to chance | S20-W2-4 | W2 |
| check-repetition-2 | L | SKILL.md:88 `POST /api/revalidate` with `{ secret, tag: "notes" }` vs `npm run revalidate` used by sync-vault/atomize-book/ingest-article | inconsistent revalidation mechanism | S20-W2-4 | W2 |

19 of 19 assigned defects close. None deferred.

### 1.4 Other findings

- OBS: the "atomize" collision (polish-plan P0-2) is still open. Closed by this spec dropping `/atomize` (OD9) and by vault-atomizer's target description stating its input is a note **already in `/vault`**, distinct from atomize-book's book-file input.
- OBS: description budget — `vault-coverage` 659 chars, `check-repetition` 387, both under cap; the two already-loaded skills' always-on total (1,046 chars, ~260 tokens) leaves the listing entirely once dmi lands (OD10 saving).
- OBS: vault-atomizer's own restatement of the mermaid-wipe gotcha (SKILL.md:160-167) is accurate but is exactly the restated-copy pattern I13 (owner S13) flags; not a defect id here, folded into the rewrite as "point at sync-vault, do not restate."
- **NEW**: `scripts/lib/coverage-map.mjs:264` is the exact source of the "not in the source map" string — a single source of truth, so fixing the map data (not code) closes vault-coverage-1.
- **NEW**: the 44 missing books with a derived note-id prefix each (§2.5, computed this session from `vault/*/_topic.md`). `dir`/`pattern`/`kind`/`scope` cannot be derived here — no `Book/`/`raw book/` in this checkout (I27's cloud-unset case) — so the backfill is an OWNER step (S20-W1-1b), scaffolded but not completed here.

## 2. Target state

### 2.1 Location and tree (after W2)

```
learn-hub/
  .claude/skills/
    vault-atomizer/SKILL.md      NEW (moved + rewritten from plugins/vault-atomizer), dmi
    vault-vectors/SKILL.md       NEW (moved + rewritten from plugins/vault-vectors), dmi
    vectors/SKILL.md             NEW — dmi alias, ≤10-line body (OD9-a)
    vault-coverage/SKILL.md      rewritten in place, dmi (W2; BOOK_ROOT/map/stale-text fixed W1)
    check-repetition/SKILL.md    rewritten in place, dmi
  plugins/
    # vault-atomizer/            DELETED (S20-W2-1)
    # vault-vectors/              DELETED (S20-W2-2)
  scripts/scrape/coverage-sources.json   26 → up to 70 entries (owner backfill, §3)
```

### 2.2 Frontmatter

All five share one shape (`metadata: {profile: cc}`, `disable-model-invocation: true`):

| skill | description | argument-hint |
|---|---|---|
| `vault-atomizer` | §2.3 body outline; capability + Use when + Not for, ~700 chars | `<note-id> [--list] [--manifest]` |
| `vault-vectors` | ~520 chars, §2.3 | `[--audit] [--check]` |
| `vectors` | "Alias for vault-vectors. Use when the user types \"/vectors\"." | `[--audit] [--check]` |
| `vault-coverage` | unchanged capability/Use-when text; adds Not for `detect-duplicates.mjs` | — |
| `check-repetition` | adds Not for `similarity:detect` / atomize-book §7b, §2.3 | — |

Kept trigger phrases: all of §1.2's quoted lists carry over unchanged in substance (only "Use for" → "Use when", R3). `/atomize` is the one phrase dropped (OD9, §6).

### 2.3 Body outline

**vault-atomizer** (source `plugins/vault-atomizer/skills/vault-atomizer/SKILL.md`, 211 lines → target ~190 lines):

| source lines | keep / cut (reason) / move / new |
|---|---|
| 1-4 frontmatter | rewrite — "Use for"→"Use when" (R3); ~700 chars |
| 6-16 intro | rewrite stats: "1,681 of 4,532 notes are ≥1,500 words with ≥3 sections; worst is 10,943 words / 7 sections (`actinf-continuous-time-dynamical-systems`)" (closes -2) |
| 18-38 "two rules" | keep verbatim (no defect) |
| 40-47 step 1 fetch | keep |
| 52-65 step 2 survey | `--min-words` default 1500→**2400** (2× atomize-book's 1,200-word depth floor, so a flagged note splits into ≥2 children each still clearing it); state the new count "1,011 of 4,532 (22%), depth-floor overlap removed" (closes -1, P1-6); stays overridable |
| 67-107 steps 3-4 | keep verbatim |
| 105 `summary` line | cut "graph hover text and" — keep "the hub's listing line" (closes -5) |
| 108-152 steps 5-6b | keep verbatim |
| 154-171 step 7 sync | replace the `&&` chain with the CX-17 sync-vault sentence, verbatim, no restated fallback: "Publish through the `sync-vault` skill (same repo, always present). Follow its steps as written; do not restate them here." (closes -3); cut the `vectors:missing` "not optional" claim → "`sync:apply` already embeds every changed note including children; `vectors:missing` only covers a DB row with no vault file" (closes -4) |
| 173-181 step 8 | keep verbatim |
| 183-199 rules | rewrite last bullet: "…the hub still holds the original text in its children" → "…delete only the children if a split is wrong; nothing that carried history was touched, since the parent id survived as the hub" (closes -6) |
| 196 "look at it in the app" | "Do one, sync, then run `verify` (OPTIONAL) to screenshot the note; if unavailable, confirm via the step-8 SQL query before the next note." (closes -7) |
| 201-212 | keep verbatim |
| — | new `## Gotchas` heading (R23) around the relocated sync-tail pointer + id-collision caveat |

Target body: ~185 lines, ~2,600 tokens.

**vault-vectors** (source `plugins/vault-vectors/skills/vault-vectors/SKILL.md`, 153 lines → target ~140 lines):

| source lines | keep / cut / move / new |
|---|---|
| 1-4 frontmatter | rewrite, "Use for"→"Use when" |
| 6-27 intro + table | keep verbatim |
| 31-42 step 1 fetch | "If you are behind, merge `origin/master`…" → "If behind, report the commits and stop; merging is the user's call" (closes -6) |
| 44-59 step 2 reconcile | correct the file-path claim: `vectors:check` (`--no-verify`) writes `scripts/.out/vector-report-unverified.md` (gitignored) + `vector-report.json`; the **tracked** `docs/note-vector-report.md` is written only by a VERIFIED run (step 4) — the script deliberately keeps the fast path from overwriting the audited file (`vector-report.mjs:64-73`) (closes -3) |
| 61-73 step 3 | keep verbatim |
| 75-90 step 4 audit | heading → "Only when asked for an audit — catch the stale ones"; note `--audit` is the slash-command's argument forwarded here, not a `vector-report.mjs` flag; timing line → "at whatever the corpus size is this run — treat ~2,400/~15 min as an old data point" (closes -4) |
| 92-103 step 5 | keep verbatim |
| 105-117 step 6 report | branch on which path ran: fast-only → unverified file, label it so; only after step 4 does the tracked doc hold this run's numbers (closes -3, second half) |
| 119-153 | keep verbatim |
| — | new line under step 2: the old `--no-report` flag is retired (closes -2) — the fast path always produces its correctly-named file |

Target body: ~145 lines, ~2,050 tokens.

**`.claude/skills/vectors/SKILL.md`** (new, ≤10 lines, dmi alias template per I20):
```markdown
---
name: vectors
description: Alias for vault-vectors — embed new notes, report vector health. Use when the user types "/vectors".
disable-model-invocation: true
argument-hint: "[--audit] [--check]"
metadata:
  profile: cc
---

Invoke the `vault-vectors` skill with: $ARGUMENTS
```

**vault-coverage** (source `.claude/skills/vault-coverage/SKILL.md`, 126 lines, rewritten in place — no move):

| source lines | keep / cut / move / new |
|---|---|
| 1-4 frontmatter | W1: unchanged (still model-invocable). W2: add `disable-model-invocation: true`; add `Not for` clause naming `detect-duplicates.mjs`/`similarity:detect` (already present at :10 for redundancy — extend it to name the script, not just the doc) |
| 19-22 precondition 1 | **W1 rewrite**: replace "From a worktree, set `BOOK_ROOT` to the main checkout path" with I27's contract (owner S11): "`BOOK_ROOT` unset → the checkout root that runs the script (unchanged default). If neither `<root>/Book` nor `<root>/raw book` is a directory, print exactly `Book/ absent — cannot run here (BOOK_ROOT=<value, or "unset → <root>">)` and stop before any coverage script runs — write no report file." (closes -2's cloud-cannot-run half) |
| 31-33 precondition 3 | **W1 rewrite**: keep the "not in the source map" sentence, add: "44 of today's 70 books have no entry (§2.5 table) — add one per book you work on; `atomize-book`'s own W2 checklist item now reminds the importing agent to add its book's entry at import time (S19; referenced, not redefined here)." (closes -1's routing half) |
| 40 command | **W1 rewrite**: cut `BOOK_ROOT="C:/Users/User/Desktop/Learn"` — the command becomes `node scripts/scrape/coverage-baseline.mjs` (BOOK_ROOT is an environment variable set once per machine, I27, not restated per-command; Windows sets it at W0 per S11's G2) (closes -2's Windows-hardcode half) |
| 69 "Last run" | **W1 rewrite**: cut the status line entirely — replace with "Re-run `eval-coverage.mjs` before trusting any number; its own report carries its date, and this file should not restate one that goes stale." (closes -3) |
| everything else | keep verbatim (no defect) |

Target body: ~124 lines (net -2 after the "Last run" cut, +additions elsewhere roughly offset).

**check-repetition** (source `.claude/skills/check-repetition/SKILL.md`, 101 lines, rewritten in place):

| source lines | keep / cut / move / new |
|---|---|
| 1-4 frontmatter | add `Not for` clause (below); W2: add `disable-model-invocation: true` |
| 88 revalidate line | rewrite: `POST /api/revalidate` with `{ secret, tag: "notes" }` → `npm run revalidate` (matches sync-vault/atomize-book/ingest-article, I13) (closes -2) |
| everything else | keep verbatim (no defect) |

`Not for` clause (new text, closes -1): `Not for a fresh import's own pre-sync redundancy pass (atomize-book §7b: measure-redundancy.py within one book's new notes, then \`npm run similarity:detect\` against the whole vault before syncing) — those screen an import before it lands; this audits repetition already synced into \`/vault\`.`

Target body: 101 lines, unchanged length (one line rewritten, one clause added to frontmatter).

### 2.4 References

None added. All four skills stay single-file (bodies land at ~1,900–2,800 tokens each, under the 5,000-tok cap with no need for conditional references, R11/R13).

### 2.5 Scripts

No new scripts. The 44-book backfill scaffold below (`prefix — title`, this session's vault walk, not a script deliverable) gives the owner `book`+`prefix`; `dir`/`pattern`/`kind`/`scope` are not determinable here — `Book/`/`raw book/` are gitignored and absent from this checkout (§1.4) — so the owner fills those four per row from the Windows checkout, shaped like the 26 existing entries (§1.1: `{book, prefix, dir, pattern, kind, scope}`).

`actinf` — Active Inference: The Free Energy Principle in Mind, Brain, and Behavior; `ambit` — Adaptive Mentalization-Based Integrative Treatment; `ampn` — Adaptive Mentalization-Based Integrative Treatment (AMBIT) for People with Multiple Needs; `adult` — Adult ADHD; `bd2` — Bipolar II Disorder: A State-of-the-Art Review; `bllm` — Build a Large Language Model (From Scratch); `cbtad` — CBT for Anxiety Disorders: A Practitioner Book; `chdis` — Character Disturbance: The Phenomenon of Our Age; `cbtga` — Cognitive Behavior Therapy with Gifted Adults; `coa` — Coming of Age: How Adolescence Shapes Us; `cptsd` — Complex PTSD: From Surviving to Thriving; `cpkp` — Computational Psychiatry — Key Papers; `dlp` — Deep Learning with Python; `eb` — Emotional Blackmail; `eom` — Empire of Madness; `gtb` — Game Theory and Behavior; `homl` — Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow; `isc` — In Sheep's Clothing; `pop` — Influence: The Psychology of Persuasion; `imlp` — Introduction to Machine Learning with Python; `mhp` — Mental Health Prediction using Machine Learning and Deep Learning Technology; `mbt` — Mentalization-Based Treatment; `nvc` — Nonverbal Communication; `exercise`/`weight` — Obesity and Cognition (two prefixes, §8); `pmdd` — Premenstrual Dysphoric Disorder; `pqt` — PubMed Evidence Digest; `pda` — Python for Data Analysis: Data Wrangling with pandas, NumPy, and Jupyter; `rsak` — Raising Securely Attached Kids; `raa` — Rethinking Adult ADHD: Helping Clients Turn Intentions Into Actions; `sparse` — Sparse Regularization: from L1 Corners to Dirac Measures; `srk` — Statistical Rethinking; `dps` — TMS Guidelines — Transcranial Magnetic Stimulation in Psychiatry (Danish Psychiatric Society, 2025); `wrmh` — Textbook of Women's Reproductive Mental Health; `lop` — The 48 Laws of Power; `epph` — The Evidence-based Parenting Practitioner's Handbook; `teog` — The Experience of God: Being, Consciousness, Bliss; `lhn` — The Laws of Human Nature; `tsnm` — These Strange New Minds; `tllt` — Transforming the Living Legacy of Trauma; `travn` — Traumatic Narcissism: Relational Systems of Subjugation; `ipsrt` — Treating Bipolar Disorder: A Clinician's Guide to Interpersonal and Social Rhythm Therapy; `udl` — Understanding Deep Learning; `npg` — WFSBP/CANMAT Nutraceuticals & Phytoceuticals Guidelines; `yrm` — Your Rainforest Mind: A Guide to the Well-Being of Gifted Adults and Youth.

### 2.6 Handoffs

- vault-atomizer step 7 (sync): S13's exact CX-17 handoff sentence, verbatim, no restated fallback (§2.3 above).
- vault-atomizer step 7b (verify in app): `verify` (OPTIONAL) — §2.3 fallback sentence above.
- vault-coverage: a real gap's fix is `atomize-book` (OPTIONAL) — already stated at SKILL.md:126, unchanged, no rewrite needed.
- check-repetition: `sync:apply`/`npm run revalidate` are npm scripts, not skills — no OPTIONAL handoff sentence applies (I13 is a script/procedure interface, not a skill name); the `Not for` line (§2.3) is the only cross-skill reference this spec adds.

### 2.7 Interfaces

This spec owns no interface. All four skills are read/write to the vault or to Supabase's `notes`/`links`/`embedding` columns directly — nothing here is a contract another spec's skill consumes by name.

#### Interfaces consumed

- **I13 (owner S13).** CLOSED (CX-17): vault-atomizer's step 7 carries S13's exact handoff sentence, verbatim — "Publish through the `sync-vault` skill (same repo, always present). Follow its steps as written; do not restate them here." — no restatement of the preflight/apply/revalidate procedure at all, closing what would otherwise have been a 9th restatement of I13's own "8 restatements" complaint.
- **I17 (owner S12).** CLOSED (CX-53): S12's I17 rule for dmi skills is explicit — the positive case uses an explicit `/<name>` prompt (the slash form still invokes the skill), negatives stay natural-language near-misses. This spec's §4.1 cases follow it.
- **I20 (owner S08).** ASSUMES: the frontmatter whitelist covers `disable-model-invocation`/`argument-hint`/`metadata.profile` for a project skill the same as a plugin skill (both are `SKILL.md` files Claude Code loads identically) — S08 to confirm.
- **I21 (owner S21).** ASSUMES: vault-atomizer's/vault-vectors' own already-correct CLAUDE.md restatements (mermaid-wipe, vault-not-two-levels-deep) stay in place — neither is a defect id here, so this spec does not move them into a shared `references/gotchas.md`; S21's later pass may still do so.
- **I22 (owner S21).** ASSUMES: none of the six npm scripts this spec relies on (`vectors:check`, `vectors:fix`, `vectors:missing`, `repetition:check`, `revalidate`, `sync:preflight`/`sync:apply`) is renamed by S21's script-list edit — read as-is this session.
- **I27 (owner S11).** ASSUMES: `BOOK_ROOT` resolution exactly as S11's §2.7 states — unset → checkout root, "Book/ absent — cannot run here (BOOK_ROOT=<value>)" finding, no report file written; Windows sets it once at W0 (G2), never per-command — quoted here, not redefined.

## 3. Change steps

### Wave 1

**S20-W1-1 · learn-hub · fix vault-coverage: `BOOK_ROOT`, source map, stale text**
- Repo: learn-hub · depends on: none (I27's contract is already fixed text, owner S11, quoted not built here).
- Files: edit `.claude/skills/vault-coverage/SKILL.md`.
- Change: §2.3 vault-coverage rows — precondition 1 (I27 contract), precondition 3 (name the 44-missing-books count + point at atomize-book's own checklist item, S19), the step-1 command (drop the inline `BOOK_ROOT=`), the "Last run" status line (cut).
- Commands: `grep -c 'C:/Users' .claude/skills/vault-coverage/SKILL.md`
- Done when: returns `0`; `grep -c 'Book/ absent' .claude/skills/vault-coverage/SKILL.md` → ≥1; `grep -c 'Last run' .claude/skills/vault-coverage/SKILL.md` → `0`.
- Rollback: `git checkout -- .claude/skills/vault-coverage/SKILL.md`.

**S20-W1-1b · OWNER (Windows, BOOK_ROOT available) · backfill `coverage-sources.json`**
- Repo: learn-hub · depends on: S20-W1-1 (the SKILL.md text this step's result makes true).
- Action: for each of the 44 books in §2.5's table, inspect `%BOOK_ROOT%\Book\` or `%BOOK_ROOT%\raw book\` for that book's extracted text directory, and add one entry `{book, prefix, dir, pattern, kind, scope}` to `scripts/scrape/coverage-sources.json`, following the shape of the 26 existing entries (§1.1). `prefix` is already given (§2.5); `dir`/`pattern`/`kind`/`scope` are read off the actual files on disk.
- Files: `scripts/scrape/coverage-sources.json`.
- Done when: `node -e "console.log(require('./scripts/scrape/coverage-sources.json').sources.length)"` → `70` (or fewer if some books are deliberately left unmapped, each with a one-line reason in the commit message).
- Rollback: `git checkout -- scripts/scrape/coverage-sources.json`.

### Wave 2

**S20-W2-1 · learn-hub · vault-atomizer → project skill, dmi**
- Repo: learn-hub · depends on: none.
- Files: create `.claude/skills/vault-atomizer/SKILL.md` (content per §2.2/§2.3); delete `plugins/vault-atomizer/` (whole directory: SKILL.md, `commands/atomize.md`, `.claude-plugin/plugin.json`).
- Change: as tabled in §2.3. `/atomize` is dropped, not carried over (OD9 — collides with atomize-book's own trigger).
- Commands: `git mv plugins/vault-atomizer/skills/vault-atomizer/SKILL.md .claude/skills/vault-atomizer/SKILL.md`; `git rm -r plugins/vault-atomizer`
- Done when: `test -f .claude/skills/vault-atomizer/SKILL.md -a ! -d plugins/vault-atomizer`; `grep -c 'disable-model-invocation: true' .claude/skills/vault-atomizer/SKILL.md` → `1`; `grep -c '2400\|2,400' .claude/skills/vault-atomizer/SKILL.md` → ≥1 (closes -1); `grep -c '&&' .claude/skills/vault-atomizer/SKILL.md` → `0` (closes -3, no foreground chain left).
- Rollback: `git mv .claude/skills/vault-atomizer/SKILL.md plugins/vault-atomizer/skills/vault-atomizer/SKILL.md`; `git checkout HEAD~1 -- plugins/vault-atomizer`.

**S20-W2-2 · learn-hub · vault-vectors → project skill, dmi, + `/vectors` alias**
- Repo: learn-hub · depends on: none.
- Files: create `.claude/skills/vault-vectors/SKILL.md` (§2.2/§2.3); create `.claude/skills/vectors/SKILL.md` (§2.3, the ≤10-line alias); delete `plugins/vault-vectors/`.
- Change: as tabled in §2.3.
- Commands: `git mv plugins/vault-vectors/skills/vault-vectors/SKILL.md .claude/skills/vault-vectors/SKILL.md`; `git rm -r plugins/vault-vectors`
- Done when: `test -f .claude/skills/vault-vectors/SKILL.md -a -f .claude/skills/vectors/SKILL.md -a ! -d plugins/vault-vectors`; `grep -c 'vector-report-unverified' .claude/skills/vault-vectors/SKILL.md` → ≥1 (closes -3); `grep -c '\-\-no-report' .claude/skills/vault-vectors/SKILL.md` → `0` (closes -2); `wc -l .claude/skills/vectors/SKILL.md` → ≤10 body lines (excl. frontmatter).
- Rollback: `git mv .claude/skills/vault-vectors/SKILL.md plugins/vault-vectors/skills/vault-vectors/SKILL.md`; `git rm .claude/skills/vectors/SKILL.md`; `git checkout HEAD~1 -- plugins/vault-vectors`.

**S20-W2-3 · learn-hub · vault-coverage flips to dmi**
- Repo: learn-hub · depends on: S20-W1-1 (content fixes land first, so the dmi flip is the only remaining change here).
- Files: edit `.claude/skills/vault-coverage/SKILL.md`.
- Change: add `disable-model-invocation: true` to frontmatter; extend the existing `Not for` clause (already names `detect-duplicates.mjs` for redundancy, §1.2) with nothing further — it already covers the boundary this wave cares about.
- Commands: `grep -c 'disable-model-invocation: true' .claude/skills/vault-coverage/SKILL.md`
- Done when: returns `1`.
- Rollback: `git checkout -- .claude/skills/vault-coverage/SKILL.md`.

**S20-W2-4 · learn-hub · check-repetition rewrite + dmi**
- Repo: learn-hub · depends on: none.
- Files: edit `.claude/skills/check-repetition/SKILL.md`.
- Change: add the `Not for` clause (§2.3); replace the raw `POST /api/revalidate` call with `npm run revalidate`; add `disable-model-invocation: true`.
- Commands: `grep -c 'Not for' .claude/skills/check-repetition/SKILL.md`; `grep -c 'npm run revalidate' .claude/skills/check-repetition/SKILL.md`; `grep -c 'POST /api/revalidate' .claude/skills/check-repetition/SKILL.md`
- Done when: first two return ≥1; third returns `0`; `grep -c 'disable-model-invocation: true' .claude/skills/check-repetition/SKILL.md` → `1`.
- Rollback: `git checkout -- .claude/skills/check-repetition/SKILL.md`.

**S20-W2-5 (new, critique P6) · learn-hub · eval cases for the four skills**
- Repo: learn-hub · depends on: S12-W0-4, S20-W2-1, S20-W2-2, S20-W2-3, S20-W2-4.
- Files: create `evals/{vault-atomizer,vault-vectors,vault-coverage,check-repetition}/<case>/{prompt.md,graders/*.md}` — the 12 cases of §4.1 (3 per skill; the `explicit-invocation` case of each is smoke-tagged). The `/vectors` alias has no cases of its own (§4.1 defines none); `vault-vectors`' cases cover its target.
- Commands: `find evals/vault-atomizer evals/vault-vectors evals/vault-coverage evals/check-repetition -name prompt.md | wc -l` → 12; `scripts/eval-project-skill.sh <skill> --smoke` for each of the four.
- Done when: 12 case directories exist; each skill's smoke run passes (S12-W4-1 needs ≥3 cases and a passing smoke run for vault-coverage and check-repetition).
- Rollback: `git rm -r` the four `evals/` directories.

## 4. Evals

### 4.1 Cases

All four skills are `disable-model-invocation: true` (OD10-a). Per R35, dmi "also blocks Skill-tool delegation" — so a `tool_used: Skill` trigger-positive grader, the platform's own recommended pattern (§6.2), cannot fire for these skills by the ordinary route (Claude choosing to call the Skill tool from a natural-language request). This spec's cases substitute an **explicit-invocation** trigger case, per S12's I17 rule for dmi skills (CX-53): the positive case is an explicit `/<name>` prompt (the slash-command form still invokes the skill), and the negative cases stay natural-language near-misses, asserting the skill does NOT fire on prose alone.

3 cases per skill (12 total), one full set shown for `vault-atomizer` (trigger via explicit name, near-miss negative, output); the other three skills' cases are tabled.

**Shared graders:**
- `va-skill-fired.md`: `---\n{type: tool_used, tool: Skill, input_match: '"skill"\s*:\s*"(?:[\w-]+:)?vault-atomizer"'}\n---`
- `va-not-fired.md`: `---\n{type: tool_used, tool: Skill, input_match: '"skill"\s*:\s*"(?:[\w-]+:)?vault-atomizer"', min: 0, max: 0, arm: both}\n---`

**`vault-atomizer/explicit-invocation` (trigger positive — explicit name, per §4.1's note):**

`prompt.md`:
```
---
name: vault-atomizer-explicit-invocation
tags: [vault-atomizer, trigger, smoke]
max_turns: 10
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
---

/vault-atomizer mbt-overview — list its sections first, don't write anything yet.
```
Graders: `va-skill-fired.md`.

**`vault-atomizer/negative-book-import` (near-miss negative — atomize-book's territory, not this skill's):**

`prompt.md`:
```
---
name: vault-atomizer-negative-book-import
tags: [vault-atomizer, negative]
max_turns: 10
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
---

Atomize this new book into vault notes — I've dropped the PDF in Book/.
```
Graders: `va-not-fired.md`.

**`vault-atomizer/output-plan-rejects-unassigned-section` (output/process):**

`prompt.md`:
```
---
name: vault-atomizer-output-plan-rejects-unassigned-section
tags: [vault-atomizer, output]
max_turns: 15
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, Bash(node scripts/split-note.mjs*)]
---

Run the vault-atomizer skill: validate a split plan for note mbt-overview that leaves section 3 unassigned to any hub or child, and tell me what happens.
```
`graders/mentions-rejection.md`: `---\n{type: regex, target: last_message, pattern: 'unassigned|rejected|section 3', flags: i}\n---`
`graders/no-apply-before-validate.md`: `---\n{type: tool_order, before: {tool: Bash, input_match: '--plan.*\.json(?!.*--apply)'}, after: {tool: Bash, input_match: '--apply'}}\n---`

Other 9 cases (tabled):

| skill | case name | tags | prompt gist | graders |
|---|---|---|---|---|
| vault-vectors | explicit-invocation | trigger, smoke | "/vault-vectors — fast path only" (CX-53: `/<name>` positive case) | `tool_used: Skill` |
| vault-vectors | negative-authoring | negative | "Write new notes about X" (atomize-book territory) | `tool_used: Skill` min0 max0 both |
| vault-vectors | output-labels-unverified | output | "Run vault-vectors without --audit and summarize" | regex `unverified\|not verified\|presence` |
| vault-coverage | explicit-invocation | trigger, smoke | "/vault-coverage Mentalization-Based Treatment" (CX-53) | `tool_used: Skill` |
| vault-coverage | negative-redundancy | negative | "Are there duplicate notes in the vault?" (detect-duplicates territory) | `tool_used: Skill` min0 max0 both |
| vault-coverage | output-book-root-absent | output | "Run vault-coverage" with no `Book/` in the env | regex `Book/ absent` |
| check-repetition | explicit-invocation | trigger, smoke | "/check-repetition mbt-" (CX-53) | `tool_used: Skill` |
| check-repetition | negative-presync-screen | negative | "Screen this new import for duplicates before syncing" (similarity:detect/atomize-book §7b) | `tool_used: Skill` min0 max0 both |
| check-repetition | output-revalidate-call | output | "Run check-repetition, apply one approved fix, finish" | regex `trace`: `npm run revalidate` |

### 4.2 Conversion

No `evals.json` exists for any of these four skills today (`find plugins/vault-atomizer plugins/vault-vectors .claude/skills/vault-coverage .claude/skills/check-repetition -iname evals.json` → none). All 12 cases in §4.1 are new, seeded from this spec's own drafting.

### 4.3 Live triggers

None of these four join a live trigger family (§6.3 of the architecture) — OD10-a makes them user-only precisely so "check coverage of X" and similar phrasings do **not** auto-route (the owner types `/vault-coverage` instead). Near-miss queries worth recording for the family they border, for S12's negative sets:
- "atomize the vault"/"split this note" (vault-atomizer) vs "atomize this book" (atomize-book, S19) — must not cross-fire.
- "check similar-notes coverage" (vault-vectors) vs "check coverage of X" (vault-coverage) — two different meanings of "coverage" in one vault; the explicit-invocation-only design sidesteps this rather than resolving it lexically.
- "check repetition" (check-repetition) vs "screen for duplicates before syncing" (`similarity:detect`, no skill wrapper) — check-repetition's `Not for` line is the resolution.

### 4.4 Commands

- Smoke: `bash scripts/eval-project-skill.sh vault-atomizer`; same for `vault-vectors`, `vault-coverage`, `check-repetition`, `vectors` (I17, owner S12's throwaway-plugin wrapper, §6.5 architecture).
- `claude plugin validate --strict` does not apply directly to `.claude/skills/*` as a plugin root; use learn-hub's own `check:skills` (I22, owner S21) once it exists — not built by this spec.
- Release: none — project skills are unversioned (git history is the version, architecture §7); no `release.py` step applies.

## 5. Acceptance criteria

1. `test ! -d plugins/vault-atomizer -a ! -d plugins/vault-vectors` → both absent.
2. `test -f .claude/skills/vault-atomizer/SKILL.md -a -f .claude/skills/vault-vectors/SKILL.md -a -f .claude/skills/vectors/SKILL.md` → all present.
3. `grep -l 'disable-model-invocation: true' .claude/skills/{vault-atomizer,vault-vectors,vectors,vault-coverage,check-repetition}/SKILL.md | wc -l` → `5`.
4. `grep -c 'C:/Users\|C:\\\\Users' .claude/skills/vault-coverage/SKILL.md` → `0`.
5. `node -e "console.log(require('./scripts/scrape/coverage-sources.json').sources.length)"` → `26` immediately after S20-W1-1 (text-only fix; the JSON is untouched until the owner's S20-W1-1b), then `70` (or a documented lower number) after S20-W1-1b.
6. `grep -c 'Not for' .claude/skills/check-repetition/SKILL.md` → ≥1.
7. `grep -c 'POST /api/revalidate' .claude/skills/check-repetition/SKILL.md` → `0`.
8. `grep -c '1500\|1,500' .claude/skills/vault-atomizer/SKILL.md` → `0` (old threshold no longer stated as current); `grep -c '2400\|2,400' .claude/skills/vault-atomizer/SKILL.md` → ≥1.
9. `grep -c 'vector-report-unverified.md' .claude/skills/vault-vectors/SKILL.md` → ≥1.
10. All 19 rows of §1.3 show a fix step whose file above has landed.

## 6. Trigger lock

| phrase | source (skill, field) | kept / moved / removed (reason) |
|---|---|---|
| `/atomize` | vault-atomizer, description | removed (OD9 — collides with atomize-book's own name/trigger) |
| "this note is too long", "split this note", "atomize the vault", "which notes should be split", "break this chapter into atomic notes" | vault-atomizer, description | kept — `vault-atomizer` remains the skill's typeable name; not in any listing (dmi) |
| `/vectors`, "embed the new notes", "create vectors for new notes", "backfill embeddings", "are any notes missing a vector", "vector report", "check similar-notes coverage" | vault-vectors, description | kept — `/vectors` becomes the dedicated dmi alias skill (§2.3); the rest stay on `vault-vectors`'s own description |
| "measure coverage", "coverage report", "did we lose anything from <book>", `/vault-coverage`, "what did the notes miss", "run the coverage baseline", "check <book> for gaps" | vault-coverage, description | kept, unchanged text |
| `/check-repetition`, "check repetition", "find repeated content in the vault", "is this import repetitive" | check-repetition, description | kept, unchanged text |

## 7. Risks and OD sensitivity

- **The dmi-eval tension (§4.1) is the main risk.** If explicit-name invocation cannot fire the Skill tool under dmi, none of §4.1's trigger-positive cases pass as written, and R71's "≥3 cases including one should-trigger" is unmeetable without a rubric exception — this follows directly from R35 ("also blocks Skill-tool delegation") read against R71. Flagged in §8; if the grader must change, only the trigger case needs replacing (a `regex` grader over the skill's distinctive first-output line), not the negative/output cases.
- **OD9 sensitivity.** (a, assumed): `/vectors` is a dedicated alias skill, `/atomize` is not (collision). (b, capability names only): no `.claude/skills/vectors/`, the owner types `vault-vectors` in full. (c, rename to verbs): both skills renamed, touching every §5/§6 row — not built this way here.
- **OD10 sensitivity.** (a, assumed): all four leave the always-loaded listing (§1.4's ~260-token saving on the two already loaded). (b, everything model-invocable): dmi absent everywhere, §4.1's tension disappears, and the listing grows ~2,173 chars (~540 tokens) — small alone, but SKL-08's overflow risk is cumulative across every unit.

## 8. Open questions

- **CLOSED (CX-53).** Whether a dmi skill's Skill tool still fires when the prompt explicitly names it via `/<name>` (§4.1, §7) is now S12's stated I17 rule, not an open question here. Still unverified by a live run (no `claude plugin eval` run this session — out of scope, hard constraint); that live confirmation happens at S12-W4-1's project-skill smoke pass.
- **ASSUMES (I27, owner S11):** "Book/ absent — cannot run here (BOOK_ROOT=<value, or "unset → <root>">)" is quoted verbatim from S11's own §2.7 — S11 to confirm no wording drift before S20-W1-1 lands.
- **ARCH-CONFLICT: none found.** Every cited architecture row (§3.5, §3.6, §6.5, §10 W1 item 7/W2 step 1, OD9, OD10) matches what this session re-read in the source files.
- **The `Obesity and Cognition` two-prefix book** (§2.5): whether the schema takes an array `prefix` or needs two entries — settle during the W1-1b backfill.
- **S19's atomize-book checklist wording** (referenced at S20-W1-1's precondition-3 text): assumed compatible; if S19 phrases it differently, only that one cross-reference sentence needs a word change.
