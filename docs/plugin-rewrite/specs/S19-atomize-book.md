# Spec S19: atomize-book (W1 content fixes, W4 verbatim split)

| Field | Value |
|---|---|
| Repos | learn-hub |
| Units (today → target) | `.claude/skills/atomize-book/SKILL.md` (rewrite in place); `references/note-format.md`, `references/drafting-agent.md` (edit); `references/{extract,figures,measure,qc,traps,gotchas}.md` (new, W4); `scripts/` (unchanged — 354 Python unittests stay in place) |
| Waves | W1 (H21, H22, H23 + atomize-book-5..11, -13, -14), W4 (H24 verbatim split; atomize-book-12 resolves as a side effect) |
| Owner decisions assumed | OD11-b (staged CLAUDE.md restructure reaching app gotchas — feeds W4's `gotcha-map.md`, consumed here) |
| Defects closed | 14 of 14 assigned (HIGH: H21, H22, H23 in W1; H24 in W4) |
| Interfaces owned | none |
| Interfaces consumed | I13 (owner S13), I17 (owner S12), I20 (owner S08), I21 (owner S21), I22 (owner S21) |
| Depends on specs | S13 (sync-vault must exist before §9 can point at it); S21 (gotcha-map.md, `book:*`/`test:py` package.json entries); S08 (house-shape templates, informative); S16 (`ingest-visual` must exist before S19-W2-1 names it, CX-29) |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| Path | Lines | Bytes | Est. tokens | Role |
|---|---|---|---|---|
| `SKILL.md` | 1,274 total (1,256 body per `measure.py skill`; frontmatter 18 lines) | 87,050 | 21,607 whole / 21,320 body | the skill |
| `references/note-format.md` | 265 | — | — | note/topic frontmatter + body contract |
| `references/drafting-agent.md` | 172 | — | — | drafting-agent prompt template + auditor/expander variants |
| `scripts/*.py` (13) + `test_*.py` (4) | — | — | — | extract/slice/measure/QC tooling; 354 `unittest` cases, all green (re-run this session: `Ran 354 tests ... OK`) |

`learn-hub/scripts/check-mermaid.mjs` exists today (renders every fence with the sync's own renderer, then runs `auditMermaidDeterminism`) but no skill references it — SKILL.md and `drafting-agent.md` mandate the mermaid validator MCP instead (H7). No `npm run book:check-mermaid` alias exists yet.

### 1.2 Description

Measured with `measure.py skill`: 1,075 chars; `use_when_at: 432` (exceeds R4's ~250 target); `not_for_at: 922`; `has_angle_brackets: true` (`<book>`/`<topic>` placeholders violate R3); 10 quoted trigger phrases incl. `"import <book> into the vault"` and `"re-sync the vault"`. `Not for:` names only 3 siblings (hand-written note, board-prep, PubMed/research notes) — not `vault-atomizer`, `ingest-slides`, `ingest-article`, `sync-vault` (LOC-31, the open "atomize" collision, architecture §2.8).

### 1.3 Defects

Every defect with prefix `atomize-book` (14), re-opened against the file read this session.

| id | sev | H# | evidence (path:line, re-opened) | problem | fix | wave |
|---|---|---|---|---|---|---|
| atomize-book-1 | H | H21 | SKILL.md:295-296 ("not a 404") vs :1027-1029 ("renders as `/note/<topic-id>`, which 404s") vs :1063-1067 (tells agents to repoint at "that topic's own order-1 note") | Three passages give three different answers for `[[topic-id]]`. CLAUDE.md:2567-2599 settles it: a chapter reference in body prose is legal, routes to `/topic/<id>`, no edge, never repointed. | S19-W1-1 | W1 |
| atomize-book-2 | H | H22 | SKILL.md:1116-1117 ("each re-embed the WHOLE vault … ~40 minutes") and :1265-1267 (restated) | `sync:apply` is incremental via a content-hash cache (confirmed live in `apply-sync.mjs`). The whole-vault claim is stale and drives agents to kill a run that would finish in minutes. | S19-W1-2 | W1 |
| atomize-book-3 | H | H23 | 0 grep hits this session for `\$`, `EQ:`, `stadium`, `LIVE_GROUPS`, `book-category` under `atomize-book/{SKILL.md,references/*.md}` | Four documented silent-failure classes have no drafting rule: `\$` money escaping (CLAUDE.md:2480-2489), equation-as-PNG EPUB re-extraction (:2490-2523), the mermaid stadium-node ban (:2408-2426), the `LIVE_GROUPS`/`coverage-sources.json` shelf checklist (:1298-1341). | S19-W1-3 | W1 |
| atomize-book-4 | H | H24 | Measured: body 1,256 lines / ~21.3k tok | ~60% is reference-grade (figures §5.0-5c ~416 lines, measurement §6/7/7b ~243, traps ~105), loaded every trigger. | S19-W4-2, S19-W4-3, S19-W4-4, S19-W4-5, S19-W4-6, S19-W4-7 | W4 |
| atomize-book-5 | M | — | SKILL.md:1051 `find vault -name '*.md' ... > /tmp/allids.txt` | Resolves ids from every `.md`, incl. `vault/articles/*` and sidecars — the article-id false-pass `qc-gate.py`'s `is_linkable`/`LINKABLE_TYPES=("note","topic")` (`manifest_lib.py:559-571`, confirmed) was fixed for. Duplicates a script and gets it wrong. | S19-W1-4 | W1 |
| atomize-book-6 | M | — | SKILL.md:80 one-level glob vs :90-91 (names that exact glob as the failure two paragraphs later) | Step-0 prefix check uses the glob its own next paragraph documents as broken. | S19-W1-4 | W1 |
| atomize-book-7 | M | — | SKILL.md:443-444 + `drafting-agent.md:172` mandate the mermaid validator MCP; `ingest-article/SKILL.md:174-180` forbids it (confirmed) | Direct sibling contradiction. `scripts/check-mermaid.mjs` (confirmed present, unreferenced) already wraps the renderer the sync uses. | S19-W1-4 | W1 |
| atomize-book-8 | M | — | `note-format.md:263-265` "wikilink the existing note (e.g. `aim-neurodegenerative`…)" | `aim-neurodegenerative` is a **topic** id (`type: topic`, confirmed), held up as an "existing note" example — the exact H21 error, in the reference agents read for the correct pattern. | S19-W1-1 | W1 |
| atomize-book-9 | M | — | SKILL.md:27 "~9 topics, ~20 notes" vs :267-277 (≥1200 words/note) | 20×1200=24,000 words minimum; contradicts the depth contract two sections later and its own `planned_notes × 1200` arithmetic check. | S19-W1-5 | W1 |
| atomize-book-10 | M | — | SKILL.md:406-407, :301-302, :327, :129-134 | Deterministic checks written as prose/ad-hoc shell (R63); some duplicate `check-manifest.py`, others have no script home. | S19-W1-6 (partial) | W1 |
| atomize-book-11 | M | — | SKILL.md:129-131 `import fitz`; confirmed `python3 -c 'import fitz'` → `ModuleNotFoundError` | PDF route not executable here; no preflight before an agent is deep into extraction. | S19-W1-7 | W1 |
| atomize-book-12 | L | — | Headings at :340 (5.0), :424 (5.1), :493 (5.2), :571 (5d), :614 (5a), :681 (5b), :738 (5c), confirmed | Out-of-document-order numbering, hard to cross-reference. | resolves via S19-W4-3b (fresh sequential order; renumbered after the verbatim move S19-W4-3) | W4 |
| atomize-book-13 | L | — | SKILL.md:3-17 (1,075 chars); :15 `"re-sync the vault"` | Over the 1,024-char cap; carries sync-vault's own trigger. | S19-W1-8 | W1 |
| atomize-book-14 | L | — | SKILL.md:1142-1143 "2,835 files vs 2,746 notes"; :1117 "2,566 notes"; measured today: 4,532 `type: note`, 851 `_topic.md` | Time-sensitive counts stated as fact, already stale by ~2,000. | S19-W1-8 | W1 |

**Defects assigned: 14. Fixed: 14 (atomize-book-10 partially deferred — ratchet entry, §8).**

### 1.4 Other findings (NEW)

- **NEW — R3 `<>` violation** and **NEW — R4 `Use when` position (432 > ~250)**: not inventory ids, but on the exact text atomize-book-13 already rewrites; fixed in the same step (S19-W1-8).
- OBS: the "atomize" collision (LOC-31, architecture §2.8) is open against `obsidian-knowledge-vault`, `vault-atomizer`, pubmed's "atomize" gate word. This spec adds `vault-atomizer` and the book-pipeline siblings to atomize-book's own `Not for` (S19-W1-8); the reciprocal side belongs to whichever spec owns those units — flagged in §8.
- OBS: `ingest-article` calls three of these scripts by path (`extract-figures.py`, `check-figures.py`, `measure-loss.py`). Neither W1 nor W4 moves or renames scripts ("Python stays in place"), so that coupling is unaffected.
- OBS: `check-order-band.py` (free `order`-band collisions) is already wired into SKILL.md steps 0 and 8 (lines 82-109, 1076-1090) — not a missing rule; H23's four rules are the ones with zero coverage.

## 2. Target state

### 2.1 Location and tree (after W4)

```
.claude/skills/atomize-book/
  SKILL.md                  rewritten body, ≤500 lines / ≤5,000 tokens
  references/
    note-format.md          edited (bridge example fixed; \$ rule added)
    drafting-agent.md       edited (mermaid-validator line fixed; \$/stadium restated)
    extract.md              NEW — verbatim §1+§2 + the equation-as-PNG rule
    figures.md              NEW — verbatim §5.0-5c + the stadium-node ban
    measure.md               NEW — verbatim §6, §7, §7b
    qc.md                    NEW — verbatim §8 (id-resolution already fixed in W1)
    traps.md                  NEW — verbatim "Hard-won traps" + relocated evidence paragraphs
    gotchas.md                NEW (W4, after S21's gotcha-map.md) — see §2.4
  scripts/                    unchanged (13 .py + 4 test_*.py)
```

### 2.2 Frontmatter (target, after S19-W1-8)

```yaml
---
name: atomize-book
description: >-
  Extracts a book (EPUB/PDF/HTML) into Learn-hub vault notes end to end: extract, slice
  into chapters, fan out drafting agents, recreate figures, measure information loss,
  expand gaps, dedupe, QC, then hand off to sync-vault. Use when the user drops a book
  file and says "extract the book", "atomize this book", "turn this book into vault
  notes", "add this book to the Learn hub", "make notes from this textbook", or points
  at an epub/pdf in Book/raw book. Also for follow-ups: "check coverage of this book",
  "the notes missed this topic, expand them", "add diagrams to the notes". Not for: a
  hand-written note or a re-sync with no new content (use sync-vault), board-prep Micky
  notes, PubMed/research-cited notes (use pubmed-research-note), a lecture deck (use
  ingest-slides), a journal article (use ingest-article), or a note distilled from
  content already in the hub (use vault-atomizer).
metadata:
  profile: cc
---
```

Measured this session (`measure.py skill` against the exact text above): 889 chars, `use_when_at: 224`, `not_for_at: 580`, `has_angle_brackets: false`, `has_first_or_second_person: false`, `yaml_valid: true`.

Kept trigger phrases (8, quoted): `"extract the book"`, `"atomize this book"`, `"turn this book into vault notes"`, `"add this book to the Learn hub"`, `"make notes from this textbook"`, `"check coverage of this book"`, `"the notes missed this topic, expand them"`, `"add diagrams to the notes"`. Full mapping in §6.

### 2.3 Body outline

W1 edits content in place first (line numbers below are today's); W4 then moves whole sections into reference files. The W4 executor locates each section **by heading**, confirmed with `grep -n '^## \|^### '` against the post-W1 file — the numeric ranges below are for planning; W1 shifts them by a small, bounded amount (§3 estimates ~+20 net lines).

| Source (heading) | Today's lines | W1 change | W4 target | Post-W4 body lines |
|---|---|---|---|---|
| Frontmatter+title+intro | 1-32 | rewrite description (W1-8) | keep | ~30 |
| Reporting contract | 34-70 | keep verbatim | keep (standing rule) | 37 |
| `## 0. Orient` | 72-110 | fix glob (W1-4), add ready.mjs preflight (W1-7), trim evidence 93-96 → move | keep condensed; evidence → `traps.md` | ~34 |
| `## 1. Extract` | 111-142 | add equation-as-PNG rule (W1-3) | **move → `extract.md`**; keep heading + pointer + 2 commands | ~10 |
| `## 2. Slice` | 144-161 | none | **move → `extract.md`** (append); heading + 1-line pointer | ~3 |
| `## 3. Plan` + `3b` | 163-278 | fix bridge rule (W1-1), fix scale opener (W1-5), trim evidence 226-234 → move | keep core rules inline (standing procedure); evidence → `traps.md` | ~105 |
| `## 4. Draft` | 280-336 | fix bridge-list text (W1-1), fix mermaid-validator line (W1-4) | keep (fan-out flow); trim 2 evidence asides → `traps.md` | ~45 |
| `## 5. Figures` (5.0-5c/5d/5a/5b) | 338-753 | add stadium-node ban (W1-3) | **move → `figures.md`**, renumbered in file order (closes atomize-book-12); keep heading+pointer+disposition table (431-438, kept inline) | ~25 |
| `## 6. Measure` | 755-922 | none | **move → `measure.md`**; heading+pointer+3 commands | ~20 |
| `## 7. Expand` | 924-948 | none | **move → `measure.md`** (append) | ~3 |
| `## 7b. Dedupe` | 950-999 | none | **move → `measure.md`** (append) | ~3 |
| `## 8. QC gate` | 1001-1105 | fix id-resolution in `<details>` (W1-4) | **move → `qc.md`**; heading+`qc-gate.py` command+1-line summary | ~12 |
| `## 9. Sync` | 1106-1155 | **rewritten**, not moved (W1-2) — collapses to the sync-vault handoff | stays inline, short (§2.6) | ~11 |
| `## 10. Upkeep` | 1156-1169 | add `LIVE_GROUPS`/`coverage-sources.json` item (W1-3) | keep | ~18 |
| `## Gotchas` (was "Hard-won traps") | 1170-1274 | rename heading (R23), content unchanged | **move body → `traps.md`**; keep 4-6 top one-liners + pointer | ~20 |
| — | — | — | **new**: `references/gotchas.md` from S21's `gotcha-map.md` (§2.4) | n/a |

Post-W4 projected body: 30+37+34+10+3+105+45+25+20+3+3+12+11+18+20 ≈ **376 lines**, under 500/5,000-tok with margin. Re-measure with `measure.py skill` at S19-W4-7 rather than trusting this estimate.

### 2.4 References

| File | Purpose | Load condition | Size target |
|---|---|---|---|
| `note-format.md` (edited) | note/topic contract | unconditional, step 0 | unchanged ~270 |
| `drafting-agent.md` (edited) | drafting prompt template | unconditional, step 4 | unchanged ~175 |
| `extract.md` (new) | extraction + slicing + equation-as-PNG check | "Before step 1, read `references/extract.md`" | ~60 |
| `figures.md` (new) | full figure pipeline + stadium-node ban | "Before step 5, read `references/figures.md`" | ~420 (needs `## Contents`, R15 — comparable to `ingest-article`'s 503-line `figures-and-loss.md`) |
| `measure.md` (new) | loss/depth measurement, expand, dedupe | "Before step 6, read `references/measure.md`" | ~245 |
| `qc.md` (new) | QC gate, fixed id-resolution, bulk-import dup screen (moved from old §9) | "Before step 8, read `references/qc.md`" | ~130 |
| `traps.md` (new) | former traps body + relocated evidence paragraphs | "Read before step 3/5/9, per the heading" | ~120 |
| `gotchas.md` (new, W4) | atomize-book's slice of the CLAUDE.md gotcha corpus per S21's map | "Read before drafting/figures/sync, per heading" | sized by S21's map; candidates in S19-W4-8 |

### 2.5 Scripts

Unchanged — no script added or removed. `scripts/check-mermaid.mjs` (already present under `learn-hub/scripts/`, not `.claude/skills/atomize-book/scripts/`) gets a new **caller**: SKILL.md and `drafting-agent.md` invoke it in place of the mermaid validator MCP (S19-W1-4). CLI confirmed: `node scripts/check-mermaid.mjs <vault-dir> [...]`, prints per-fence FAIL/WARN, exits 1 on any render failure. No `--help` today; not assigned to this spec (outside `.claude/skills/atomize-book`), flagged in §8. The 354-test suite is unchanged; wiring `npm run test:py` is I22 (owner S21).

### 2.6 Handoffs

Step 9's rewritten text (S19-W1-2) carries S13's exact CX-17 handoff sentence, verbatim, with no restated fallback (CX-17 explicitly names this spec as dropping one):

> Publish through the `sync-vault` skill (same repo, always present). Follow its steps as written; do not restate them here.

### 2.7 Interfaces

**Owned:** none.

**Consumed:**

- **I13 (owner S13).** Full sync-tail procedure + `scripts/ready.mjs` (`checkPyMuPDF` runs `python3 -c "import fitz"`; `checkChromium` checks `PUPPETEER_EXECUTABLE_PATH`). This spec's step-0 preflight (W1-7) and step-9 rewrite (W1-2) assume both exist — confirmed against S13's own §2.7, read this session.
- **I17 (owner S12, not yet written).** ASSUMES: `scripts/eval-project-skill.sh atomize-book` builds a throwaway plugin wrapping the skill + `evals/atomize-book/` and runs `claude plugin eval` on it (architecture §6.5, confirmed). Case layout follows eval-format.md's shape unchanged.
- **I20 (owner S08).** ASSUMES: the frontmatter whitelist S08 defines (confirmed against its §2.7). atomize-book uses only `name`, `description`, `metadata.profile: cc`.
- **I21 (owner S21, not yet written).** ASSUMES: `docs/rewrite/gotcha-map.md` names exactly which CLAUDE.md headings move here. §3 S19-W4-8 lists 22 candidates by direct grep evidence this session; the W4 executor reconciles against S21's actual map before moving text (§8), same pattern S13 used for its own 6 candidates.
- **I22 (owner S21, not yet written).** ASSUMES: the single package.json edit list includes `"book:check-mermaid": "node scripts/check-mermaid.mjs"` and `"test:py"`. S19-W1-4 adds the `book:check-mermaid` line directly (matching S13's precedent for `sync:preflight`); a no-op if S21's pass finds it present (§8).

## 3. Change steps

### Wave W1

**S19-W1-1 — One topic-id chapter-reference rule (H21, atomize-book-1, -8)**
- Repo: learn-hub · depends on: none
- Files: `SKILL.md`, `references/note-format.md`
- Change: SKILL.md:288-304 (step-4 bridge-list text) — replace the paragraph from "…what it costs in general is the EDGE…" through the trailing "substitute a real note inside it" instruction with one rule: *a `[[topic-id]]` in body prose is a legitimate chapter reference — routes to `/topic/<id>`, writes no edge, never repointed at a note; a bridge-list entry meant to cross-link a specific concept must be built from a real NOTE id from the start (usually that topic's order-1 note) — if the list wrongly carries a topic id for a note-level concept, fix the LIST, never the agent's usage of it.* Keep the `find vault -name '_topic.md' ...` snippet, drop its "repoint" framing. SKILL.md:1027-1029 — delete "it renders as `/note/<topic-id>`, which 404s" (factually wrong — `remarkWikilink` routes to `/topic/<id>`), replace with: *a topic id used as a note-wikilink target is not itself an error — the plain dangling check can't see it, since it IS a real vault id — but it writes no `links` edge, so `qc-gate.py`'s extra check reports it for review, not as broken.* SKILL.md:1063-1067 — replace "repoint to that topic's own order-1 note … instead of stripping the link" with "confirm it is a whole-chapter reference (leave it) or a mis-built bridge (fix the list)." `note-format.md:263-265` — replace `aim-neurodegenerative` (a topic id) with a real note id from the same book (confirm via `grep -l "^topic: aim-neurodegenerative" vault/aim-neurodegenerative/*.md | head -1` — do not guess a slug).
- Commands: `grep -c "topic's own order-1 note" .claude/skills/atomize-book/SKILL.md` (expect 0); confirm the substituted id has `type: note`.
- Done when: the three passages state one rule; the note-format.md example resolves to a `type: note` file.
- Rollback: `git checkout -- .claude/skills/atomize-book/SKILL.md .claude/skills/atomize-book/references/note-format.md`.

**S19-W1-2 — Fix stale sync economics (H22, atomize-book-2)**
- Repo: learn-hub · depends on: S13-W1-6 (CX-34 — sync-vault must exist so the handoff names a real skill)
- Files: `SKILL.md`
- Change: replace `## 9.` (1106-1155) wholesale with the §2.6 handoff (CX-17's sync-vault sentence, verbatim — no restated incremental-cache mechanics; that belongs to sync-vault's own doc, owned by S13). Delete the now-false restatement at :1265-1274, keeping only what is still true (env vars don't persist across Bash calls — set `PUPPETEER_EXECUTABLE_PATH` in the same command as `sync:apply`).
- Commands: `grep -n "re-embed the WHOLE vault\|re-embed from scratch" .claude/skills/atomize-book/SKILL.md` (expect 0).
- Done when: grep above returns 0; new §9 ≤15 lines.
- Rollback: `git checkout -- .claude/skills/atomize-book/SKILL.md`.

**S19-W1-3 — Add the four missing drafting rules (H23, atomize-book-3)**
- Repo: learn-hub · depends on: none
- Files: `SKILL.md`, `references/note-format.md`, `references/drafting-agent.md`
- Change (four additions, condensed from CLAUDE.md's narrative to a drafting-spec rule):
  1. **`\$` money rule** → `note-format.md` after line 181: *literal money must be `\$20`, not `$20` — two unescaped `$` in one paragraph parse as inline math and swallow the text between (CLAUDE.md:2480-2489).* Restate one line in `drafting-agent.md` after line 126.
  2. **Equation-as-PNG** → SKILL.md after line 142 (moves into `extract.md` at W4): *an EPUB can render every equation as a PNG with no MathML — check `grep -c '<img' <extract>/OEBPS/xhtml/chapterN.xhtml` against `grep -c '<math'`; if images dominate, re-extract with a placeholder naming the image (`[[EQ: pgNN-1.png]]`) so agents Read and transcribe to KaTeX rather than reconstruct from prose — reconstruction measured ~80% wrong-equation rate on one import (CLAUDE.md:2490-2523).*
  3. **Stadium-node ban** → SKILL.md §5.1 after line 452: *never author `([...])` — renders non-deterministically (five renders of one diagram produced five distinct SVGs); use `(...)` instead (CLAUDE.md:2408-2426).* Restate in `drafting-agent.md` after line 172.
  4. **`LIVE_GROUPS`/`coverage-sources.json`** → `## 10.` after line 1162: *confirm the book lands on the correct `/books` shelf — add its `(title, domain)` to `book-category.test.ts`'s `LIVE_GROUPS` fixture and to `scripts/scrape/coverage-sources.json`; a book can import perfectly and render on the wrong shelf with every gate green (CLAUDE.md:1298-1341).*
- Commands: `grep -c '\\\\\$' references/note-format.md` ≥1; `grep -c 'stadium' SKILL.md` ≥1; `grep -c 'LIVE_GROUPS' SKILL.md` ≥1; `grep -c 'EQ:' SKILL.md` ≥1.
- Done when: all four greps ≥1.
- Rollback: `git checkout -- .claude/skills/atomize-book/`.

**S19-W1-4 — Fix id-resolution, the glob, and the mermaid-validator contradiction (atomize-book-5, -6, -7)**
- Repo: learn-hub · depends on: S13-W1-5 (CX-34/CX-39 — same-file `package.json` edit order: S13-W1-5 adds `sync:preflight` first)
- Files: `SKILL.md`, `references/drafting-agent.md`, `package.json`, learn-hub `README.md` (one script-table row for `book:check-mermaid`; critique F12)
- Change: SKILL.md:80 — `grep -rh "^id:" vault/*/_topic.md | sort` → `find vault -name '_topic.md' -exec grep -h "^id:" {} + | sort`. SKILL.md:1051 — filter the id-set by type: `find vault -name '*.md' ! -path 'vault/articles/*' ! -name '*.infographic.md' ! -name '*.animation.md' -exec grep -h "^id:" {} + | sed 's/^id: *//' | sort -u > /tmp/allids.txt` (matches `manifest_lib.is_linkable`'s exclusions, confirmed). SKILL.md:443-444 — "mermaid validator MCP" → `node scripts/check-mermaid.mjs <vault-dir>` (same renderer as `sync:apply`; the MCP returns 70-115 KB inline SVG+PNG/diagram and is not that renderer). `drafting-agent.md:172` — same substitution. `package.json` — add `"book:check-mermaid": "node scripts/check-mermaid.mjs"` after `book:upload-figures` (I22 ASSUMES).
- Commands: `grep -c "mermaid validator MCP" SKILL.md references/drafting-agent.md` (expect 0); `grep -c "vault/\*/_topic.md" SKILL.md` (expect 0); `node -e "require('./package.json').scripts['book:check-mermaid']"` exits 0.
- Done when: both greps 0; node check does not throw.
- Rollback: `git checkout -- .claude/skills/atomize-book/ learn-hub/package.json`.

**S19-W1-5 — Fix scale-guidance contradiction (atomize-book-9)**
- Repo: learn-hub · depends on: none
- Files: `SKILL.md`
- Change: line 27 — "a 16-chapter book → ~9 topics, ~20 notes, ~20 subagents" → "a 16-chapter book runs ~9 topics and, per the depth floor in step 3, well over 20 notes once note count is planned from the chapter's own concept density and word count — see the `planned_notes × 1200` check, not a fixed target."
- Commands: `grep -n "~20 notes" SKILL.md` (expect 0).
- Done when: grep 0.
- Rollback: `git checkout -- .claude/skills/atomize-book/SKILL.md`.

**S19-W1-6 — Script where a script exists, defer the rest (atomize-book-10, partial)**
- Repo: learn-hub · depends on: none
- Files: `SKILL.md`
- Change: SKILL.md:301-302 (post-draft topic-id resolution) — replace the inline `find`/`sed` snippet with a pointer to `check-manifest.py --notes` (already performs this exact resolution as part of its tick-off). Leave :406-407 (Calibre sanity grep), :327 (heading dump), :129-134 (PDF TOC dump) as prose — no script exists; new tooling is out of scope for a content-fix wave (ratchet, §8).
- Commands: `grep -c "check-manifest.py --notes" SKILL.md` (expect ≥2, up from 1).
- Done when: grep shows the increment.
- Rollback: `git checkout -- .claude/skills/atomize-book/SKILL.md`.

**S19-W1-7 — Wire the PyMuPDF/Chromium/poppler preflight (atomize-book-11)**
- Repo: learn-hub · depends on: S13-W1-2 (CX-34 — `scripts/ready.mjs` must exist)
- Files: `SKILL.md`
- Change: `## 0.` after line 78 — add: *Run `node scripts/ready.mjs --json` first (I13, owner S13). A failing `pymupdf` check names `pip install pymupdf`; a failing `chromium` check means mermaid/figure baking silently falls back at sync time. Stop and fix the named gap before extracting a PDF.*
- Commands: `grep -c "scripts/ready.mjs" SKILL.md` (expect ≥1).
- Done when: grep ≥1.
- Rollback: `git checkout -- .claude/skills/atomize-book/SKILL.md`.

**S19-W1-8 — Description rewrite + stale counts (atomize-book-13, -14, R3/R4 NEW)**
- Repo: learn-hub · depends on: none
- Files: `SKILL.md`
- Change: replace frontmatter `description:` (lines 3-17) with §2.2's target text verbatim. Replace :1142-1143 "2,835 files vs 2,746 notes today" with "a large vault" (no number as current fact, R18); confirm no orphan "2,566 notes" copy survives S19-W1-2.
- Commands: `python3 <measure.py> skill SKILL.md` → `description.chars <= 1024`, `has_angle_brackets: false`, `use_when_at <= 260`; `grep -n "2,566\|2,835\|2,746" SKILL.md` (expect 0).
- Done when: both checks pass.
- Rollback: `git checkout -- .claude/skills/atomize-book/SKILL.md`.

### Wave W2

**S19-W2-1 (new, CX-29) — Visuals handover text (S05's H-11)**
- Repo: learn-hub · depends on: S16-W2-3 (`ingest-visual` must exist to be named)
- Files: `SKILL.md`
- Change: replace `SKILL.md:588-590` (visuals go through the inbox and `ingest-visual`) with S05's H-11 fix text, verbatim: a visual (infographic, animation, or explorable) arising from an atomized chapter is never written directly into `/vault` — it is filed through the `research-notes/visuals/` inbox (I09, owner S15) and the `ingest-visual` skill (owner S16), the same as any other producer's visual asset. This lands outside the W4 freeze window (§3, S19-W4-1), since it is a normal content fix, not part of the verbatim split.
- Commands: `grep -n "ingest-visual" SKILL.md`
- Done when: the grep shows the new text at the old line range; no direct-write instruction for visuals survives nearby.
- Rollback: `git checkout -- .claude/skills/atomize-book/SKILL.md`.

### Wave W4

Move proof for S19-W4-2…6 (critique C2-08): S19-W4-1 saves the pre-split `SKILL.md` to the scratch dir once; each move step proves every moved part with `diff <(sed -n '<a>,<b>p' <saved SKILL.md>) <(sed -n '<c>,<d>p' references/<file>.md)` — the output must be empty. A move commit never rewords or renumbers.

**S19-W4-0 (new, critique F14) — OWNER, Windows: pre-split chapter baseline**
- Repo: learn-hub (Windows, `BOOK_ROOT` set: `Book/` and `raw book/` exist only there) · depends on: W2 exit; runs before S19-W4-1
- Files: create `docs/rewrite/w4-chapter-baseline/<chapter-id>.json`
- Change: pick one imported chapter whose source is under `BOOK_ROOT`; run `measure-loss.py`, `measure-depth.py` and `check-figures.py` on its existing notes, through today's (pre-split) SKILL.md commands. Save each gate's JSON and pass/fail verdict.
- Done when: the JSON names the chapter, the source file's sha256 and a verdict per gate.
- Rollback: `git revert <this commit>`.

**S19-W4-1 (OWNER) — Freeze window.** The owner pauses new atomize-book imports from the start of S19-W4-2 until S19-W4-9 passes (K12: an import landing mid-split would edit a file this wave restructures; critique C2-27 — S19-W4-2…6, -8, -7 and -9 run back to back in one session, so the pause is short). No command — a stated pause, recorded in the learn-hub `CHANGELOG.md` (CX-27 — not `docs/rewrite/delivery-log.md`, which is for environment/plugin-delivery rows only); the executor also saves the pre-split `SKILL.md` for the move proofs above.

**S19-W4-2 — `references/extract.md`**
- Repo: learn-hub · depends on: S19-W1-1..8, S19-W4-1 (the freeze and the saved copy)
- Files: create `references/extract.md`; edit `SKILL.md`
- Change: move `## 1.` and `## 2.` (post-W1, located by heading) verbatim into the new file, plus the equation-as-PNG rule from W1-3.2. SKILL.md keeps: heading + "Before this step, read `references/extract.md`" + the two bash commands.
- Commands: the move-proof `diff` above, once per moved part — each prints nothing.
- Done when: `references/extract.md` exists with the full moved text; SKILL.md's step 1/2 ≤10 lines combined.
- Rollback: `git checkout -- .claude/skills/atomize-book/`.

**S19-W4-3 — `references/figures.md`**
- Repo: learn-hub · depends on: S19-W4-2
- Files: create `references/figures.md`; edit `SKILL.md`
- Change: move `## 5.` and its subsections (5.0/5.1/5.2/5d/5a/5b/5c) verbatim, in their current order and numbering (S19-W4-3b renumbers them in a separate commit, so this move stays provable by `diff`; critique C2-08). SKILL.md keeps heading + pointer + the disposition table (today's :431-438) inline.
- Commands: the move-proof `diff` above; `wc -l references/figures.md`.
- Done when: every move-proof `diff` prints nothing; SKILL.md's §5 ≤25 lines.
- Rollback: `git checkout -- .claude/skills/atomize-book/`.

**S19-W4-3b (new, critique C2-08) — renumber `references/figures.md`**
- Repo: learn-hub · depends on: S19-W4-3
- Files: edit `references/figures.md`
- Change: renumber the subsections in file order (5.1 manifest, 5.2 disposition, 5.3 svg redraw, 5.4 hand the agent the picture, 5.5 baking, 5.6 budgets/rights, 5.7 chapter visualizations) — closes atomize-book-12. Add `## Contents` (R15, ≥400 lines). Headings and cross-references only; no body text changes.
- Commands: `git diff --stat` (one file); `git diff -U0 -- .claude/skills/atomize-book/references/figures.md`; `grep -c '^## Contents' references/figures.md` (expect 1).
- Done when: the diff changes only heading lines, `§5.N` cross-references and the new Contents block; the Contents grep is 1.
- Rollback: `git revert <this commit>`.
- Rollback: `git checkout -- .claude/skills/atomize-book/`.

**S19-W4-4 — `references/measure.md`**
- Repo: learn-hub · depends on: S19-W4-3
- Files: create `references/measure.md`; edit `SKILL.md`
- Change: move `## 6.`, `## 7.`, `## 7b.` verbatim. SKILL.md keeps heading + pointer + the four bash commands (`measure-loss.py`, `book:source-cover`, `measure-depth.py`, `measure-redundancy.py`).
- Commands: `grep -c '^## 6\.\|^## 7\.\|^## 7b\.' SKILL.md` (expect 3, each ≤7 lines).
- Done when: grep matches, sections short.
- Rollback: `git checkout -- .claude/skills/atomize-book/`.

**S19-W4-5 — `references/qc.md`**
- Repo: learn-hub · depends on: S19-W4-4
- Files: create `references/qc.md`; edit `SKILL.md`
- Change: move `## 8.` (post-W1-4 fix) verbatim, plus the bulk-import duplicate-screening block deleted from old §9 in W1-2 (lines 1126-1151 today — preserved here, not discarded). SKILL.md keeps heading + `qc-gate.py` command + "Fix anything flagged before syncing. Full checklist: `references/qc.md`."
- Commands: `grep -c "similarity:detect" references/qc.md` (expect ≥1 — confirms the block moved, not lost).
- Done when: grep passes; SKILL.md's §8 ≤12 lines.
- Rollback: `git checkout -- .claude/skills/atomize-book/`.

**S19-W4-6 — `references/traps.md`**
- Repo: learn-hub · depends on: S19-W4-5
- Files: create `references/traps.md`; edit `SKILL.md`
- Change: move the former traps body (renamed `## Gotchas` at W1, content unchanged) verbatim, plus the four evidence paragraphs relocated from §0/§3b/§4. SKILL.md keeps `## Gotchas` with 4-6 one-liners + "Full list: `references/traps.md`, read before step 3/5/9."
- Commands: `grep -c '^## Gotchas' SKILL.md` (expect 1, R23).
- Done when: grep passes; section ≤20 lines.
- Rollback: `git checkout -- .claude/skills/atomize-book/`.

**S19-W4-7 — Final SKILL.md pass**
- Repo: learn-hub · depends on: S19-W4-2..6
- Files: `SKILL.md`
- Change: confirm every `references/*.md` link resolves (R13), every pointer is "Before step N, read X" not a bare "see references/" (R14), `## Gotchas` present (R23), no version narration (R18).
- Commands: `python3 <measure.py> skill SKILL.md` → `body_lines <= 500`, `body_est_tokens <= 5000`.
- Done when: both hold; if over, cut further from §3/§4 (the largest inline sections) first.
- Rollback: `git checkout -- .claude/skills/atomize-book/SKILL.md`.

**S19-W4-8 — `references/gotchas.md`**
- Repo: learn-hub · depends on: S21-W4a-2 (CX-28/CX-34)
- Files: create `references/gotchas.md`; edit `CLAUDE.md`
- Change: move, verbatim, the CLAUDE.md headings `gotcha-map.md` assigns to atomize-book, **and delete those headings from CLAUDE.md in this same commit** (CX-28 — move and delete together, not in two separate steps; the map wins over the candidate list below if they disagree, and S21-W4a-2 must have landed first so S21-W4a-3's archive already has the pre-move text). Candidates by direct grep evidence this session (reconcile against S21's actual map): `/books` "Other" shelf gap detector (1298), `measure-loss.py` endnote-marker false alarm (1374), high-compression-figure question-not-verdict (1403), figure LABELS text-cutting (1620), figure baking two-routes-one-fallback (1636), mermaid stadium node (2408), `\$` money rule (2480), EPUB equation-as-PNG (2490), `extract-figures.py` letter-numbered labels (2524), caption-in-HEADING (2534), `#` in code fence not a heading (2551), EPUB OPF single-quoted (2558), `[[topic-id]]` chapter reference (2567), ARTICLE id not a wikilink target (2599), vault not two levels deep (2697), `similarity:detect` stale index (2711), split chapter owned by neither agent (2732), z-lib duplicated page runs (2745), figures unmeasured until 2026-08-04 (2803), figure PARTS never figure-sized (2817), gate false-positive worse than silence (2865), worklist inherits blind spots (2882), free order band only as of last fetch (2906).
- Commands: `node scripts/move-blocks.mjs --map docs/rewrite/gotcha-map.md --dest atomize-book --write`, then `node scripts/move-blocks.mjs --check` (S21-W4a-4; critique C2-08); `grep -c '^## ' references/gotchas.md` (sanity, non-empty); `grep -c '<moved heading text>' CLAUDE.md` (expect 0 per heading).
- Done when: `move-blocks --check` exits 0; every candidate heading appears in exactly one of `gotchas.md`/`traps.md` (check against S21's map for the split), confirmed by an exactly-once grep against both together; none of the moved headings remain in CLAUDE.md.
- Rollback: `git checkout -- .claude/skills/atomize-book/ CLAUDE.md`.

**S19-W4-9 — Exit test: one chapter re-run — OWNER, Windows (critique F14)**
- Repo: learn-hub (Windows, `BOOK_ROOT` set) · depends on: S19-W4-7, S19-W4-0
- Files: none created outside scratchpad
- Change: verification only.
- Commands: (1) `python3 -m unittest discover -s .claude/skills/atomize-book/scripts -p 'test_*.py'` → `Ran 354 tests ... OK`. (2) Re-run S19-W4-0's measurements on the same chapter through the new `references/` pointers. (3) Run one fresh drafting pass of that chapter through the restructured skill (extract → draft → figures → measure-loss → measure-depth → QC), without syncing and without committing the drafts. (4) Compare gate verdicts (pass/fail per gate), not scores, against `docs/rewrite/w4-chapter-baseline/<chapter-id>.json`: fresh drafting varies between runs.
- Done when: no gate verdict went from pass to fail in (2) or (4); all 354 tests remain green. The freeze (S19-W4-1) ends here.
- Rollback: revert the W4 merge — content is recoverable from `references/*.md` regardless, since W4 never rewords, only relocates.

**S19-W4-10 (new, critique P6) — atomize-book eval cases**
- Repo: learn-hub · depends on: S12-W0-4, S19-W4-7
- Files: create `evals/atomize-book/<case>/{prompt.md,graders/*.md}` — the three full cases of §4.1 and the three tabled ones.
- Change: add `smoke` to the tags of the three full cases (`trigger-positive-epub`, `near-miss-single-paper-note`, `sync-tail-decision`): S12-W4-1 runs `--smoke` and needs ≥3 passing smoke cases (architecture §10 W4 item 9).
- Commands: `find evals/atomize-book -name prompt.md | xargs grep -l 'tags:.*smoke' | wc -l`; `scripts/eval-project-skill.sh atomize-book --smoke`.
- Done when: the count is 3; 6 case directories exist; the smoke run passes.
- Rollback: `git rm -r evals/atomize-book`.

## 4. Evals

### 4.1 Cases

Layout: `learn-hub/evals/atomize-book/<case>/{prompt.md, graders/*.md}`, run via `scripts/eval-project-skill.sh atomize-book` (I17, owner S12). Per architecture §6.5, a Supabase-dependent skill gets evals for **decision steps only** — none of the three cases below executes the pipeline.

**Case 1 — trigger positive** (`trigger-positive-epub/`)

`prompt.md`:
```markdown
---
tags: [atomize-book, trigger]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 6
---

I have "Cognitive Behavioral Therapy for Adolescents.epub" sitting in the Book/ folder.
Can you atomize this book into the Learn vault?
```

`graders/skill-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?atomize-book"'
weight: 2
---
```

`graders/response-engages.md`:
```markdown
---
type: llm
criteria: |
  PASS if the final response indicates the assistant is beginning or has begun the
  atomize-book pipeline for the named EPUB (mentions extracting text, slicing chapters,
  a topic map, or the book's own title).
  FAIL if the response does not engage with atomizing the named book, or names a
  different skill as the one handling it.
---
```

**Case 2 — near-miss negative** (`near-miss-single-paper-note/`)

`prompt.md`:
```markdown
---
tags: [atomize-book, negative]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 6
---

I found a great new RCT on PubMed about ketamine for treatment-resistant depression.
Can you make me a vault note summarizing it?
```

`graders/no-atomize-book.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?atomize-book"'
min: 0
max: 0
arm: both
weight: 2
---
```

`graders/response-not-book-pipeline.md`:
```markdown
---
type: llm
criteria: |
  PASS if the final response does not describe a whole-book extraction pipeline (no
  extracting chapters, slicing, or a topic map), and instead addresses a single vault
  note or summary from the named paper.
  FAIL if the response describes extracting a book, slicing chapters, or a topic map.
---
```

**Case 3 — output/process** (`sync-tail-decision/`)

`prompt.md`:
```markdown
---
tags: [atomize-book, output]
allowed_tools: [Read, Skill, Bash(npm run sync:preflight)]
max_turns: 6
---

I'm partway through the atomize-book pipeline for a new import — notes are drafted,
QC'd, and clean. Walk me through getting them into Supabase.
```

`graders/never-runs-full-sync.md`:
```markdown
---
type: tool_used
tool: Bash
input_match: 'npm run sync(?!:)'
min: 0
max: 0
arm: both
weight: 3
---
```

`graders/mentions-sync-apply.md`:
```markdown
---
type: regex
target: last_message
pattern: 'sync:apply|sync-vault'
---
```

**Further cases** (table only):

| Name | Tags | Prompt gist | Graders |
|---|---|---|---|
| `bridge-list-topic-id` | `atomize-book, output` | Scaffolded fixture: a bridge-id list has a topic id meant for a specific concept; ask what the assistant does with it | `llm` PASS if it substitutes the topic's order-1 note or flags the list for correction, FAIL if it wikilinks the topic id as a note bridge |
| `figure-disposition-photo` | `atomize-book, output` | Figure record described as a stained histology plate; ask which disposition applies | `regex` on `last_message` for `bake`; `not_contains` for `mermaid\|redraw` |
| `near-miss-vault-atomizer` | `atomize-book, negative` | "Take this one long note already in the vault and split it into three shorter notes." | `tool_used: Skill`, `atomize-book`, `min:0 max:0 arm:both` |

### 4.2 Conversion

No `evals.json` exists for atomize-book today (`.claude/skills/atomize-book/` has no `evals/` directory). All three cases above are new, not mined.

### 4.3 Live triggers

Family membership (architecture §6.3): `{pdf-pipeline, ingest-article, ingest-slides, atomize-book, anthropic-skills:pdf, anthropic-skills:bullet-reconstruct}` and `{atomize-book, digest-report, anthropic-skills:obsidian-knowledge-vault}`.

Near-miss queries (feed S12's family sets): (1) "Can you bullet-reconstruct this dense chapter I'm pasting in?" → `bullet-reconstruct`, not atomize-book (pasted excerpt, not a whole book file). (2) "I have a lecture deck PDF, can you get the high-yield content into the hub?" → `ingest-slides`. (3) "Turn this chapter into atomic Obsidian notes for my board-prep vault." → `obsidian-knowledge-vault` or refused (different format). (4) "Extract this book and make notes from it — it's a PDF in Book/." → atomize-book (positive control).

### 4.4 Commands

- Smoke: `bash scripts/eval-project-skill.sh atomize-book -- --tag trigger --tag negative --ablation none --runs 1`
- Release: `bash scripts/eval-project-skill.sh atomize-book -- --tag output --runs 1 --threshold 0.8` (OQ11-a)

## 5. Acceptance criteria

1. `grep -c "repoint to that topic's own order-1 note" SKILL.md` → 0 (H21).
2. `grep -c "renders as \`/note/<topic-id>\`, which 404s" SKILL.md` → 0.
3. `grep -c "re-embed the WHOLE vault\|re-embed from scratch" SKILL.md` → 0 (H22).
4. `grep -c '\\\\\$' references/note-format.md` ≥1; `grep -c 'stadium' SKILL.md` (post-W4: `figures.md`) ≥1; `grep -c 'EQ:' SKILL.md` (post-W4: `extract.md`) ≥1; `grep -c 'LIVE_GROUPS' SKILL.md` ≥1 (H23).
5. `measure.py skill SKILL.md` → `description.chars <= 1024`, `has_angle_brackets: false` (atomize-book-13 + R3 NEW).
6. `grep -c "vault/\*/_topic.md" SKILL.md` → 0 (atomize-book-6).
7. `grep -c "mermaid validator MCP" SKILL.md references/drafting-agent.md` → 0 (atomize-book-7).
8. The id `note-format.md` now names for the bridge example resolves to a `type: note` file (atomize-book-8).
9. (W4) `measure.py skill SKILL.md` → `body_lines <= 500`, `body_est_tokens <= 5000` (H24).
10. (W4) `python3 -m unittest discover -s .claude/skills/atomize-book/scripts -p 'test_*.py'` → `Ran 354 tests ... OK`, unchanged.
11. (W4) every S19-W4-8 candidate heading appears in exactly one of `gotchas.md`/`traps.md`.
12. (W4) the one-chapter re-run (S19-W4-9) shows no regression in loss/depth/figure-coverage.

## 6. Trigger lock

| Phrase | Source | Kept / moved / removed |
|---|---|---|
| "extract the book" | description | kept |
| "atomize this book" | description | kept |
| "turn this book into vault notes" | description | kept |
| "import `<book>` into the vault" | description | removed (redundant with "atomize this book"; carried the R3-forbidden placeholder) |
| "add this book to the Learn hub" | description | kept |
| "make notes from this textbook" | description | kept |
| "check coverage of `<book>`" | description | kept, reworded → "check coverage of this book" |
| "the notes missed `<topic>`, expand them" | description | kept, reworded → "the notes missed this topic, expand them" |
| "add diagrams to the `<book>` notes" | description | kept, reworded → "add diagrams to the notes" |
| "re-sync the vault" | description | removed → sync-vault (H23; owned by S13) |

## 7. Risks and OD sensitivity

- **K11** (redistribution knowledge loss): mitigated by W4's verbatim-only moves and the exactly-once grep (acceptance criterion 11).
- **K12** (churn collides with W4): mitigated by the freeze window (W4-1, OWNER) and per-file commits — a partial revert loses only the last file.
- **K16** (scope creep): W1 steps are content fixes only; W4 moves text without rewording (diff-based done-when checks). atomize-book-10's deferred half (§8) is the one deliberate stop-short.
- **OD11 sensitivity**: the `gotchas.md` step (W4-8) depends on OD11-b producing `gotcha-map.md`. Under OD11-a (skill-owned material only), the same mechanism still applies to atomize-book's own pipeline gotchas — the candidate list is unaffected either way, since all 22 candidates are pipeline procedure, not app behavior.

## 8. Open questions

- **ASSUMES (I17, owner S12):** `eval-project-skill.sh` takes a skill name as its first argument (architecture §6.5). Settled when S12's spec exists — read its §2.5 before running §4.4.
- **ASSUMES (I21, owner S21):** the 22-heading list (W4-8) is provisional. Settled when `gotcha-map.md` exists; W4-8's grep is the reconciliation point.
- **ASSUMES (I22, owner S21):** the `book:check-mermaid`/`test:py` lines added in W1-4 are a safety against S21 not existing yet (S13's precedent); no conflict if S21 finds them present.
- **DEFER (atomize-book-10, partial):** the Calibre figure-markup check, the heading dump, and the PDF TOC dump stay prose — no script exists; writing one is new tooling, out of scope for a content-fix wave. Ratchet: `atomize-book-10-partial — 3 checks with no script home; deferred; reason: scope (K16)`.
- **Not verified here:** whether `check-mermaid.mjs`'s exit-1-on-failure is safe inside a future `Bash`-grader case that runs it — none of §4.1's cases execute it.
