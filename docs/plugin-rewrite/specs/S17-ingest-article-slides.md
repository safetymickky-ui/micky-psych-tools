# Spec S17: ingest-article and ingest-slides

| Field | Value |
|---|---|
| Repos | learn-hub |
| Units (today → target) | `.claude/skills/ingest-article/{SKILL.md,references/figures-and-loss.md}`; `.claude/skills/ingest-slides/{SKILL.md,scripts/extract_pdf.py}`; learn-hub `.gitignore` (+1 line) — all edits. Both skills keep name/dir/separation (R9: no shared steps). |
| Waves | W1 (H25–H28 + the rest of INV ingest-article/ingest-slides + descriptions/YAML + `ready.mjs` preflight); W4 (ingest-article conditional references; description pass + live-trigger query contribution) |
| Owner decisions assumed | none of OD1–OD14 changes this spec's content (OD9-a: no alias skill — neither unit had a `/` command) |
| Defects closed | 17 of 17 assigned (HIGH: H25, H26, H27, H28) |
| Interfaces owned | none |
| Interfaces consumed | I13 (owner S13), I17 (owner S12), I20 (owner S08), I21 (owner S21, not yet written), I22 (owner S21, not yet written), I26 (owner S18, this job), I27 (owner S11) |
| Depends on specs | S13 (I13: `ready.mjs`/`sync-preflight.mjs` must exist before S17-W1-6/-11); S11 (I27: `ARTICLE_INBOX_DIR` resolution, `.gitignore` line — confirmed identical); S18 (I26 `classify_pdf.py` shape, W4 only; the reciprocal pdf-pipeline routing fix should land the same wave as S17-W1-2/-8) |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| Path | Lines | Est. tokens | Role |
|---|---|---|---|
| `.claude/skills/ingest-article/SKILL.md` | 379 | 6,656 (body) | procedure |
| `.claude/skills/ingest-article/references/article-frontmatter.md` | 147 | 1,805 | schema (unchanged) |
| `.claude/skills/ingest-article/references/figures-and-loss.md` | 503 | 8,070 | figure/loss contract (one fix, §1.3) |
| `.claude/skills/ingest-article/context/example.md` | 149 | 2,103 | worked example (unchanged) |
| `.claude/skills/ingest-slides/SKILL.md` | 141 | 2,035 (body) | procedure |
| `.claude/skills/ingest-slides/references/lecture-adaptations.md` | 72 | 1,216 | schema mapping (unchanged) |
| `.claude/skills/ingest-slides/scripts/extract_pdf.py` | 128 | 1,114 | text-anchor extractor (one line fixed, §1.3) |
| `.claude/skills/ingest-slides/scripts/render_slides.py` | 78 | 636 | slide renderer (docstring fixed, §1.3) |
| `.gitignore` | 63 | — | gains one line (§1.3, H25) |

Neither skill ships a `commands/` directory; both are invoked as `/ingest-article` / `/ingest-slides` already (OBS "COMMANDS").

### 1.2 Descriptions

| Skill | Chars (today) | UTF-8 bytes | YAML valid? | `Use when` offset | `Not for` present? | Quoted triggers (today) |
|---|---|---|---|---|---|---|
| ingest-article | 1,137 | 1,139 | **No** — `mapping values are not allowed here`, col 445 (the plain scalar's `assumed: every` reads as a mapping key) | 563 | yes (books, vault notes/topics — not ingest-slides) | "explain more", "explore next", "ingest this article", "/ingest-article", "add this paper to the hub", "reconstruct + add this study", "bullet-reconstruct this" |
| ingest-slides | 1,150 | 1,152 | yes (already folded `>-`) | 612 | yes (article PDFs, books, vault notes/topics, `grilling`) | "extract the high-yield content", "digest these slides", "get this lecture into the hub", "add these decks to Articles", "ingest these slides", "review this deck slide by slide" |

`ingest-article`'s two "quoted" hits at offsets for "explain more"/"explore next" are false positives of the measurer (they are section names inside the capability clause, not triggers) — not counted as triggers below.

### 1.3 Defects

| id | sev | H# | evidence (re-opened) | problem | fix step (fix) | wave |
|---|---|---|---|---|---|---|
| ingest-article-1 | H | H25 | `SKILL.md:3,49,51,348`; `.gitignore` lacks a `Raw Article PDF` line (grep empty) | Hardcoded Windows path; bare invocation ingests-and-deletes with no confirmation; untracked-but-not-ignored | S17-W1-1, S17-W1-3 (resolve via `$ARTICLE_INBOX_DIR`, I27; bare/folder-phrase invocation **lists + asks** (interactive) or **lists + stops** (headless); add `/Raw Article PDF/` to `.gitignore`) | W1 |
| ingest-article-2 | H | H26 | `figures-and-loss.md:455-458`; `measure-source-cover.mjs:73-74` filters `^ch.*\.txt$/i` (dump is `source.txt`); `:83` `walk()`→`readdirSync` throws `ENOTDIR` on a file | §5b's command cannot run: wrong pattern AND a file-vs-directory crash | S17-W1-7 (**drop §5b for articles**, "or dropped" branch, §8 — shared with `vault-coverage` (S20), owned by neither spec; one line naming the lexical floor as the whole measurement) | W1 |
| ingest-article-3 | M | — | `figures-and-loss.md` §5a code block omits `--strip-references`/`--explain-numbers` vs the prose 10 lines below calling both REQUIRED; a stale manual "split on `\nReferences\n`" recipe follows | Reference's own example contradicts its own prose; keeps a workaround the flags now do automatically | S17-W1-7 (add the two flags to the code block, matches `SKILL.md` step 6a; replace the manual-split paragraph with one line noting the flags supersede it) | W1 |
| ingest-article-4 | M | — | `SKILL.md:313-316` "skip the `npm run sync` dry run… re-embeds the WHOLE vault — ~40 minutes" | Stale: `apply-sync.mjs` is incremental (CLAUDE.md gotcha); re-derives sync mechanics I13 now owns | S17-W1-6 (delete the paragraph; step 7 becomes the CX-17 sync-vault sentence, R59) | W1 |
| ingest-article-5 | M | — | `SKILL.md:174-197` inline `node --input-type=module -e "…"` mermaid check vs `scripts/check-mermaid.mjs` (58 lines, read: same renderer + determinism audit the snippet lacks) | Reinvents, worse, a repo script; contradicts atomize-book's own pointer to it | S17-W1-5 (replace with one command: `node scripts/check-mermaid.mjs vault/articles`) | W1 |
| ingest-article-6 | M | — | `SKILL.md:337-341` "slimming the prebaked-SVG `diagrams` blob to `{}`" | Bypasses `bakeOrPreserve` ("never write `{}`", CLAUDE.md gotcha); wipes a baked SVG on re-ingest | S17-W1-6 (delete the "no `.env.local`" fallback; I13's `sync:preflight` now refuses cleanly instead) | W1 |
| ingest-article-7 | M | — | `SKILL.md:28`; measured 6,656+1,805+8,070+2,103 = 18,634 tok mandatory (§9: ≤9k W1, ≤6k W4) | ~18.7k tok every run regardless of the paper's needs | S17-W4-1 (W1's prose cuts alone don't reach ≤9k; the token cut is conditional loading, **W4**) | **W4** |
| ingest-article-8 | M | — | `SKILL.md:80` `atomize-book/scripts/extract-figures.py`; `:112-115` inline `import fitz`; confirmed `ModuleNotFoundError` here | Cross-skill path coupling (accepted, T2); PyMuPDF absence has no actionable preflight | S17-W1-3 (keep the coupling; `node scripts/ready.mjs` Step 0, I13, names the fix before figure work starts) | W1 |
| ingest-article-9 | L | — | `SKILL.md:144` "4 seed files"; `ls vault/articles/*.md \| wc -l` → 36 | Stale dated count (R18) | S17-W1-4 (drop the number: "the existing articles in `/vault/articles/`") | W1 |
| ingest-article-10 | L | H25-adj. | desc 1,137 chars, YAML invalid (§1.2); "bullet-reconstruct this" matches a synced skill | Over cap, breaks strict YAML, collides (§2.8) | S17-W1-2 (rewrite to §2.2's folded description, 910 chars; drop the trigger, architecture line 219) | W1 |
| ingest-slides-1 | H | H27 | `SKILL.md:62,71` `python scripts/extract_pdf.py`/`render_slides.py`; from repo root resolves to `learn-hub/scripts/`, which has neither file | The two commands fail from the skill's own working directory | S17-W1-9 (`${CLAUDE_SKILL_DIR}/scripts/extract_pdf.py` / `.../render_slides.py`, R49) | W1 |
| ingest-slides-2 | H | H28 | pdf-pipeline `SKILL.md:98`, `routing.md:42,60` route decks to `atomize-book` (mini), never mention `ingest-slides` (S18's defect; reciprocal half) | Two skills give opposite answers for a deck; this skill's own boundary is correct but unreachable | S17-W1-8 (no change inside ingest-slides — Not-for already correct; the actual fix lives in pdf-pipeline, S18-W1, H32; S17-W1-8 lands the same wave for consistent reading) | W1 (coordination) |
| ingest-slides-3 | M | — | `render_slides.py:15` "already available"; confirmed `ModuleNotFoundError` here | False claim, no actionable fix text | S17-W1-9, S17-W1-10 (docstring points at `ready.mjs`; add `## 0. Preflight` step) | W1 |
| ingest-slides-4 | M | — | `SKILL.md:114` "1. `npm run sync`" vs ingest-article's own (pre-fix) "skip the dry run" — already disagreed | Contradicts the sibling it claims to copy; both wrong against I13 | S17-W1-11 (step 7 becomes the same CX-17 sync-vault sentence as ingest-article's) | W1 |
| ingest-slides-5 | M | — | `SKILL.md:22-24` "reuses … wholesale" — no figure manifest, `check-figures`, or `measure-loss` anywhere (grep empty) | A slide's chart/table/diagram can drop silently with no gate | S17-W1-11 (add lexical floor, `measure-loss.py`, + a lightweight figure manifest + `check-figures.py` for visual slides, §2.3, new steps 3b/6b) | W1 |
| ingest-slides-6 | L | — | `extract_pdf.py:85` help `_grill_text` vs `:95` actual `_slide_text`; desc names a `grilling` skill absent from both repos | Stale rename remnants | S17-W1-10 (fix help string to `_slide_text`; drop the `grilling` clause) | W1 |
| ingest-slides-7 | L | H27-adj. | desc 1,150 chars (soft cap 600) | Over soft target | S17-W1-8 (rewrite to §2.2's 948-char description) | W1 |

Count: 17 of 17 assigned. No deferrals.

### 1.4 Other findings (inventory OBS lines touching these units; NEW = found this session)

- **SCRIPT COUPLING** (OBS): ingest-article calls `atomize-book`'s scripts by relative path; both skills read pdf-pipeline's `preflight-and-apply.md`. Project-skill-to-project-skill, same repo (T2) — R44 does not apply; architecture keeps atomize-book's scripts in place, so this spec does not move them.
- **STALE COUNTS / GOTCHA DRIFT** (OBS): ingest-article `:313-316`'s "~2,700 notes"/full-re-embed claim is the same text fixed under ingest-article-4 — one edit closes both OBS lines.
- **NEW**: `check-mermaid.mjs` walks directories via `readdir`, exactly like `measure-source-cover.mjs` — a single `.md` file would crash it the same way. The ingest-article-5 fix therefore points it at `vault/articles` (a directory, 36 files, cheap), not at one slug.
- **NEW**: `check-figures.py`'s label grammar (`figure_lib.py`, `normalize_label`) always emits `"Figure N"`, no "Slide N" vocabulary. The ingest-slides-5 fix reuses that exact label text (the slide's page number stands in for N), so the unmodified script works with no change to `figure_lib.py`.

## 2. Target state

### 2.1 Location and tree (after W1; W4 adds nothing new here, only reference files)

```
.claude/skills/ingest-article/
  SKILL.md                              rewritten (§2.3)
  references/
    article-frontmatter.md              unchanged
    figures-and-loss.md                 one code block + one paragraph fixed (§1.3)
    pipeline-steps.md                   NEW, W4 only (§2.3/§2.4)
  context/example.md                    unchanged
.claude/skills/ingest-slides/
  SKILL.md                              rewritten (§2.3)
  references/lecture-adaptations.md     unchanged
  scripts/
    extract_pdf.py                      one help-text line fixed
    render_slides.py                    one docstring line fixed
.gitignore                              +1 line: `/Raw Article PDF/`
```

### 2.2 Frontmatter

**ingest-article** (folded scalar closes the YAML defect; parses under `yaml.safe_load`):

```yaml
---
name: ingest-article
description: >-
  Turns a journal-article PDF (or a DOI/PMID) into a fully enriched Learn-hub vault article: an
  at-a-glance overview, key-findings tables, typed charts, prebaked mechanism diagrams, an
  explain-more primer and glossary, theme labels, and PubMed explore-next pointers, with every
  figure gated for coverage and the text distillation scored against the source. Use when the
  user drops an article PDF and says "ingest this article", "/ingest-article", "add this paper
  to the hub", "reconstruct this study", or points at a paper and asks to get it into the
  Articles tab; also runs the watched-folder inbox on "digest the folder", "process the PDFs",
  "ingest the inbox", or a bare invocation, surveying it and asking before ingesting or
  deleting anything. Not for lecture or conference slide decks (use ingest-slides), books or
  textbooks (use atomize-book), or vault notes and topics already in /vault (use sync-vault).
---
```

Measured: 910 chars / 910 bytes (`measure.py textfile`); `Use when` at char 355; `Not for` at 747; no `I/you/your`; no `<>`. Kept triggers: "ingest this article", "/ingest-article", "add this paper to the hub", "reconstruct this study" (was "reconstruct + add this study" — reworded, still matches the same user phrasing), "digest the folder", "process the PDFs", "ingest the inbox". Dropped: "bullet-reconstruct this" (§1.3, ingest-article-10).

**ingest-slides**:

```yaml
---
name: ingest-slides
description: >-
  End-to-end lecture-slide pipeline for the Learn hub: turns a slide-deck PDF (or a folder of
  them) into an enriched vault article in the /articles tab — a high-yield bullet distillation
  plus overview, theme labels, and, where the slides carry real data, key-findings tables and
  typed charts. It reads every slide by rendering the page and reading it visually
  (OCR-by-vision), capturing image-only slides, diagrams, and mixed Thai/English text a text
  extractor misses. Use when the user points at lecture slides, a conference or PsychiTalk
  handout, a teaching deck, or a PPT/ folder and says "extract the high-yield content", "digest
  these slides", "get this lecture into the hub", "add these decks to Articles", "ingest these
  slides", "review this deck slide by slide". This is the slide sibling of ingest-article. Not
  for journal-article PDFs (use ingest-article), books (use atomize-book), or vault
  notes/topics already in /vault (use sync-vault).
---
```

Measured: 948 chars / 950 bytes; `Use when` at 467; `Not for` at 814. Kept triggers: all six unchanged. Dropped: the `grilling` Not-for clause (§1.3, ingest-slides-6 — names nothing).

## 2.3 Body outline

**ingest-article** (target ≈310 lines / ≈5,600 tok after W1 — down from 379/6,656; conditional refs land in W4):

| Source lines | Keep / cut / move | Target section |
|---|---|---|
| Source lines | Disposition |
|---|---|
| 1–46 (deliverable) | keep, trim seed-file count (ingest-article-9) |
| 47–53 (watched-folder inbox) | **rewrite** → `$ARTICLE_INBOX_DIR` (I27) + survey-ask/survey-stop; new `## 0. Preflight` above it |
| 55–139 (steps 1, 1b) | keep |
| 141–200 (step 2) | keep voice rules; **replace** inline mermaid snippet (174–197) with one `check-mermaid.mjs` line (-5) |
| 202–303 (steps 3–6) | keep |
| 305–343 (step 7) | **replace wholesale** with the I13 one-liner (-4, -6) — ≈6 lines, was 39 |
| 345–356 (step 8) | keep; scope delete to "path inside the resolved inbox" (I27) |
| 358–378 (guardrails) | keep verbatim |

**ingest-slides** (target ≈150 lines / ≈2,300 tok — was 141/2,035; the figure-gate step adds ≈25 lines):

| Source lines | Disposition |
|---|---|
| 1–50 (deliverable) | keep |
| 52–66 (steps 1–2) | keep; fix script paths (`${CLAUDE_SKILL_DIR}`); new `## 0. Preflight` above |
| 68–80 (step 3) | keep; add the "flag a slide visual" sentence |
| — | **new `## 3b.`** figure manifest for visual slides (~20 lines, -5) |
| 82–111 (steps 4–6) | keep |
| — | **new `## 6b.`** measure loss + gate figures (~15 lines, -5) |
| 113–124 (step 7) | **replace** with the I13 one-liner (≈4 lines, was 12) |
| 126–141 (step 8, guardrails) | keep |

## 2.4 References

| File | Purpose | Load condition | Size |
|---|---|---|---|
| `article-frontmatter.md` | frontmatter schema | W1 unconditional; **W4**: before step 3 | 1,805 tok |
| `figures-and-loss.md` | figure/loss contract | W1 unconditional; **W4**: before step 1b | 8,070 tok (two fixes only) |
| `context/example.md` | worked example | W1 unconditional; **W4**: before step 3, if chart-worthy | 2,103 tok |
| `references/pipeline-steps.md` | **W4 only**, steps 1b/2–6 moved out of `SKILL.md` | conditional, per step | new, ≈4,000 tok |
| `ingest-slides/lecture-adaptations.md` | lecture field-mapping | unconditional | 1,216 tok |

## 2.5 Scripts

No new scripts this spec owns. Two existing files get one-line text fixes (`extract_pdf.py` help string, `render_slides.py` docstring). `check-mermaid.mjs`, `check-figures.py`/`measure-loss.py` are invoked as documented upstream (atomize-book, unowned here) — no new flags.

## 2.6 Handoffs

Neither skill hands off elsewhere in the OPTIONAL sense (§4.2) — both are terminus skills; their only downstream dependency is the sync tail, reached by **naming `sync-vault`** with S13's exact CX-17 sentence, verbatim, and nothing restated:

> Publish through the `sync-vault` skill (same repo, always present). Follow its steps as written; do not restate them here.

`pdf-pipeline` (S18) hands off TO these two skills; that fallback sentence is S18's to carry, not restated here (R57/R59).

## 2.7 Interfaces

**Owned:** none.

**Consumed:**

- **I13 (owner S13).** ASSUMES `node scripts/ready.mjs` and `npm run sync:preflight` exist by S17-W1 (S13 is first in the W1 list). Both skills' `## 0. Preflight` step is `node scripts/ready.mjs` — its five checks cover ingest-article-8/ingest-slides-3. Sync tail reached by name (§2.6), never restated.
- **I17 (owner S12).** ASSUMES `learn-hub/evals/<skill>/<case>/` run through `scripts/eval-project-skill.sh <skill>` (S12-W0-4). §4.1 follows that layout. Whether S12-W0-5's "content from S17-W0" line means THIS spec's W1 cases or a separate pre-fix baseline S12 captures itself is open (§8) — either reading is satisfied by shipping ≥3 cases/skill at W1.
- **I20 (owner S08).** ASSUMES the frontmatter whitelist/description grammar apply unchanged to project skills (T2). Neither skill needs an alias — no `/` command beyond its own name.
- **I21 (owner S21, not yet written).** ASSUMES `gotcha-map.md` will name any sync/figure gotchas to move into a per-skill `references/gotchas.md` — none moved here (that's S21's own W4 step, not this spec's conditional-reference item).
- **I22 (owner S21, not yet written).** ASSUMES the package.json edit list adds no new script for these units — both call existing `npm run sync:preflight`/`sync:apply`/`revalidate`, `check-mermaid.mjs`, `check-figures.py`/`measure-loss.py`.
- **I26 (owner S18, this job).** ASSUMES `classify_pdf.py` (W4) prints `{"route": "article"|"book"|"report"|"slides", ...}` (S18 §2.5 authoritative). Neither skill calls it directly — `pdf-pipeline` does. No text change needed here.
- **I27 (owner S11).** ASSUMES the resolution order, absent-behaviour text and `.gitignore` line in §1.3/§2.3 match S11's I27 exactly (confirmed against `S11-delivery-environment.md` §2.7 this session — a citation, not a restatement, R59).

## 3. Change steps

### Wave 0

**S17-W0-1 (new, CX-4)**
- Repo: learn-hub · depends on: S12-W0-4
- Files: create 3 `evals/ingest-article/*` case directories, tagged `smoke`, ahead of S17-W1-12's fuller set. Each takes the name of an ingest-article §4.1 case (`trigger-positive`, `near-miss-ingest-slides`, `inbox-survey-and-ask`), so S17-W1-12 extends them instead of adding new ones (critique P7).
- Change: seed 3 `smoke`-tagged cases against TODAY's ingest-article SKILL.md, I17 layout, current script paths (architecture §10 W0 item 3) — the pre-rewrite baseline S12's smoke suite needs.
- Commands: `find evals/ingest-article -name prompt.md | xargs grep -l 'tags:.*smoke' | wc -l`
- Done when: the count is ≥3.
- Rollback: delete `evals/ingest-article/`.

### Wave 1

**S17-W1-1**
- Repo: learn-hub · depends on: S13-W1-8 (CX-39 — same-file `.gitignore` edit order)
- Files: edit `.gitignore`
- Change: append `/Raw Article PDF/` under a new comment `# ingest-article drop folder (ARTICLE_INBOX_DIR default) — I27`.
- Commands: `git check-ignore -v "Raw Article PDF/x.pdf"` (create the dir first if absent: `mkdir -p "Raw Article PDF"`)
- Done when: `git check-ignore -v "Raw Article PDF/x.pdf"` prints a match against `.gitignore`.
- Rollback: remove the two added lines.

**S17-W1-2**
- Repo: learn-hub · depends on: none
- Files: edit `.claude/skills/ingest-article/SKILL.md` (frontmatter only)
- Change: replace the frontmatter block (lines 1–4) with the §2.2 folded-scalar description.
- Commands: `python3 $MICKY_TOOLS_DIR/docs/plugin-rewrite/phase3/measure.py skill .claude/skills/ingest-article/SKILL.md`
- Done when: the command reports `"yaml_valid": true` and `"chars": 910`.
- Rollback: restore the original frontmatter block.

**S17-W1-3**
- Repo: learn-hub · depends on: S17-W1-1, S13-W1-2 (CX-34 — `ready.mjs` must exist)
- Files: edit `.claude/skills/ingest-article/SKILL.md` (body)
- Change: replace the "## Watched-folder inbox" section (source lines 47–53) with:
  ```markdown
  ## 0. Preflight

  `node scripts/ready.mjs` — five checks (node_modules, `.env.local`/env vars, Chromium,
  PyMuPDF, poppler). Fix whatever it names before continuing; do not work around a failed
  check.

  ## Watched-folder inbox

  Resolve the drop folder: `$ARTICLE_INBOX_DIR` when set and absolute, else
  `<learn-hub root>/Raw Article PDF` (root = `$LEARN_HUB_DIR` when its marker validates,
  else this checkout's top — the full contract is the architecture's `ARTICLE_INBOX_DIR`
  environment variable). On a bare invocation, or "digest the folder" / "process the PDFs" /
  "ingest the inbox": list every `*.pdf` in the resolved folder.
  - Folder does not exist → say so, stop.
  - Folder has no PDFs → say so, stop.
  - PDFs found → **show the list and ask before running anything** (interactive session); in
    a subagent, headless, or scheduled run with no picker available, **list them and stop** —
    never ingest-and-delete without an explicit confirmation. Each file stays source-of-truth
    only until its article is verified in the DB — see step 8 for the delete, scoped to a
    resolved path inside the resolved folder.
  ```
- Commands: `grep -n "C:\\\\Users\\\\User" .claude/skills/ingest-article/SKILL.md`
- Done when: the grep above prints nothing, and the new section contains the string `$ARTICLE_INBOX_DIR`.
- Rollback: restore the original "Watched-folder inbox" section and remove "## 0. Preflight".

**S17-W1-4**
- Repo: learn-hub · depends on: none
- Files: edit `.claude/skills/ingest-article/SKILL.md` (line 144)
- Change: replace `"See the 4 seed files in \`/vault/articles/\` (e.g. \`alho-2026-peer-effects.md\`)"` with `"See the existing articles in \`/vault/articles/\` (e.g. \`alho-2026-peer-effects.md\`)"`.
- Commands: `grep -n "4 seed files" .claude/skills/ingest-article/SKILL.md`
- Done when: the grep above prints nothing.
- Rollback: restore the literal count.

**S17-W1-5**
- Repo: learn-hub · depends on: none
- Files: edit `.claude/skills/ingest-article/SKILL.md` (source lines 174–197)
- Change: replace the inline `node --input-type=module -e "…"` mermaid-check block (and its two preceding sentences about the validator MCP) with:
  ```markdown
  **Validate mermaid with the repo's own renderer** (the same one the sync uses — an invalid
  fence silently falls back to the client island and looks identical to a diagram you never
  drew): `node scripts/check-mermaid.mjs vault/articles` — checks every article's fences
  (cheap at 36 articles) and prints the same determinism audit atomize-book's own pointer to
  this script relies on.
  ```
- Commands: `grep -n "mermaid-render.mjs\|createRenderer" .claude/skills/ingest-article/SKILL.md`
- Done when: the grep above prints nothing, and `grep -n "check-mermaid.mjs" .claude/skills/ingest-article/SKILL.md` prints one line.
- Rollback: restore the inline snippet.

**S17-W1-6**
- Repo: learn-hub · depends on: S17-W1-5 (same section of the file), S13-W1-6 (CX-34 — sync-vault must exist to be pointed at)
- Files: edit `.claude/skills/ingest-article/SKILL.md` (source lines 305–343, "## 7. Sync + verify")
- Change: replace the whole section with (CX-17 — the sync-vault sentence, verbatim, no restated procedure; only this skill's own post-sync verification of its own artifact stays, since that is not sync-vault's procedure):
  ```markdown
  ## 7. Sync + verify

  Publish through the `sync-vault` skill (same repo, always present). Follow its steps as
  written; do not restate them here.

  After it completes, confirm this article's row (`overview`/`charts`/`key_findings`/`related`
  populated, curate defaults `inbox`/false/false/`{}`). If you deduped in step 1, delete the
  old stub's DB row now via `merge-notes.mjs` (`sync:apply` only upserts files still in the
  vault; it never removes an orphaned row).
  ```
- Commands: `grep -n "diagrams.*{}\|~40 minutes\|Skip the .npm run sync" .claude/skills/ingest-article/SKILL.md`
- Done when: the grep above prints nothing.
- Rollback: restore source lines 305–343 verbatim.

**S17-W1-7**
- Repo: learn-hub · depends on: none
- Files: edit `.claude/skills/ingest-article/references/figures-and-loss.md` (§5a code block, §5a prose paragraph, §5b)
- Change: (a) add `--strip-references --explain-numbers 40` to the §5a code block (matches `SKILL.md` step 6a); (b) replace the "split on `\nReferences\n`" paragraph with: "`--strip-references`/`--explain-numbers N` now do this automatically — read the single printed number. The calibration table below (2026-08-04) predates both flags and is kept as a historical record, not current guidance."; (c) replace "### 5b. Semantic floor"'s body with: "Semantic worklist scoring does not apply to a single paper — `measure-source-cover.mjs` expects `ch*.txt` chapter files and a notes *directory* (atomize-book's shape; a file passed to `--notes` throws `ENOTDIR`). The lexical floor in §5a, all three required flags, is the whole measurement for an article."
- Commands: `grep -n "keep-frontmatter --figures\|book:source-cover" .claude/skills/ingest-article/references/figures-and-loss.md`
- Done when: both greps above print nothing.
- Rollback: restore the three edited passages verbatim.

**S17-W1-8**
- Repo: learn-hub · depends on: none
- Files: edit `.claude/skills/ingest-slides/SKILL.md` (frontmatter)
- Change: replace the description with the §2.2 948-char version (same `>-` folded style, already used today — only the body text and the `grilling` clause change).
- Commands: `python3 $MICKY_TOOLS_DIR/docs/plugin-rewrite/phase3/measure.py skill .claude/skills/ingest-slides/SKILL.md`
- Done when: the command reports `"chars": 948` and `"yaml_valid": true`.
- Rollback: restore the original description text.

**S17-W1-9**
- Repo: learn-hub · depends on: S13-W1-2 (CX-34 — `ready.mjs` must exist)
- Files: edit `.claude/skills/ingest-slides/SKILL.md` (source lines 60–71)
- Change: replace `python scripts/extract_pdf.py` with `python "${CLAUDE_SKILL_DIR}/scripts/extract_pdf.py"`, and `python scripts/render_slides.py` with `python "${CLAUDE_SKILL_DIR}/scripts/render_slides.py"`. Add above step 1: `## 0. Preflight` — `node scripts/ready.mjs` (same text as S17-W1-3's preflight block, one line).
- Commands: `grep -n '^python scripts/' .claude/skills/ingest-slides/SKILL.md`
- Done when: the grep above prints nothing, and `grep -c 'CLAUDE_SKILL_DIR' .claude/skills/ingest-slides/SKILL.md` → 2.
- Rollback: restore the two bare `python scripts/…` lines and remove the preflight section.

**S17-W1-10**
- Repo: learn-hub · depends on: none
- Files: edit `.claude/skills/ingest-slides/scripts/extract_pdf.py` (line 85), `render_slides.py` (line 15)
- Change: `extract_pdf.py:85` help string `default: <folder>/_grill_text` → `default: <folder>/_slide_text`; `render_slides.py:15` docstring `"already available in this repo."` → `"— run this skill's Step 0 (\`node scripts/ready.mjs\`) first if \`import fitz\` fails."`.
- Commands: `grep -n "_grill_text\|already available in this repo" .claude/skills/ingest-slides/scripts/*.py`
- Done when: the grep above prints nothing.
- Rollback: restore both original lines.

**S17-W1-11**
- Repo: learn-hub · depends on: S13-W1-6 (CX-34 — sync-vault must exist to be pointed at)
- Files: edit `.claude/skills/ingest-slides/SKILL.md` (source lines 68–113, steps 3–6, and 113–124, step 7)
- Change: (1) step 3 gains one sentence: "Flag a slide **visual** if it carries a diagram, chart, table, or data image — note its number." (2) New `### 3b.`: one `figures.json` entry per flagged slide, the schema `check-figures.py` reads: `{"label": "Figure <n>", "disposition": "prose"|"chart"|"mermaid", "note": "<slug>"}` (`skip`+`reason` if not testable); the body opens that slide's passage with `Figure <n>`, same convention `ingest-article` uses. (3) New `### 6b.`, after step 6: `python .claude/skills/atomize-book/scripts/measure-loss.py --chapters "<scratch>/_slide_text" --pattern '<deck-stem>.txt' --notes "vault/articles/<slug>.md" --top 150 --keep-frontmatter --json "…/loss.json"` then `python .claude/skills/atomize-book/scripts/check-figures.py --figures "…/figures.json" --notes "vault/articles/<slug>.md"` — fix flags before syncing. (4) Step 7 → the same CX-17 sync-vault sentence as S17-W1-6, verbatim, plus this skill's own post-sync row check.
- Commands: `grep -c "check-figures.py\|measure-loss.py" .claude/skills/ingest-slides/SKILL.md` → 2
- Done when: the grep count above → 2, and `grep -n "npm run sync$" .claude/skills/ingest-slides/SKILL.md` prints nothing (the bare dry-run step is gone).
- Rollback: revert all four sub-changes; restore original steps 3–7.

**S17-W1-12**
- Repo: learn-hub · depends on: S17-W1-2, S17-W1-8, S17-W0-1 (extends its seeds, CX-4)
- Files: create `evals/ingest-article/{trigger-positive,near-miss-ingest-slides,inbox-survey-and-ask}/`, `evals/ingest-slides/{trigger-positive,near-miss-ingest-article,figure-gate-process}/` (§4.1, full contents there)
- Change: the six case directories, each `prompt.md` + `graders/*.md` as given in §4.1.
- Commands: `find evals/ingest-article evals/ingest-slides -name prompt.md | wc -l` → 6
- Done when: the command above → 6 (the 3 W0 seeds are 3 of the 6 named dirs).
- Rollback: delete the two new `evals/` subtrees.

### Wave 4

**S17-W4-0 (new, critique P14, F14) — OWNER, Windows: pre-W4 article baseline**
- Repo: learn-hub (Windows, where `Raw Article PDF/` and the owner's article PDFs live) · depends on: W2 exit; runs before S17-W4-1
- Files: create `docs/rewrite/w4-article-baseline/<article-id>.json`
- Change: the owner picks one already-ingested article whose source PDF is still at hand. Run the gates ingest-article runs against the existing vault article: `extract-figures.py` + `check-figures.py`, and `measure-loss.py --keep-frontmatter` (the article gates, `figures-and-loss.md`). Save each gate's JSON and its pass/fail verdict.
- Done when: the JSON file names the article id, the PDF's sha256, and a verdict per gate.
- Rollback: `git revert <this commit>`.

**S17-W4-1**
- Repo: learn-hub · depends on: S17-W1-2, S21-W4a-2 (CX-34), S17-W4-0
- Files: create `.claude/skills/ingest-article/references/pipeline-steps.md`; edit `SKILL.md`
- Change: move steps 1b, 2–6 verbatim into `pipeline-steps.md` behind `## Step N` headings; `SKILL.md` keeps 0/1/7/8/Guardrails plus one pointer per moved step ("Before step N, read `references/pipeline-steps.md#step-N`"). `article-frontmatter.md`/`example.md`/`figures-and-loss.md` each gain a "Before step N" load condition (§2.4).
- Commands: `python3 $MICKY_TOOLS_DIR/docs/plugin-rewrite/phase3/measure.py file .claude/skills/ingest-article/SKILL.md`
- Done when: body ≤6,000 tok, and every pointer target resolves (`grep -c '^## Step' references/pipeline-steps.md` matches the pointer count in `SKILL.md`).
- Rollback: revert; delete `pipeline-steps.md`.

**S17-W4-2**
- Repo: learn-hub · depends on: S17-W4-1
- Files: none (measurement; `docs/rewrite/baseline.md`, format owned by S12)
- Change: re-run `measure.py skill` on both files, confirm §9 targets, record under the W4 column.
- Commands: `python3 $MICKY_TOOLS_DIR/docs/plugin-rewrite/phase3/measure.py skill .claude/skills/ingest-article/SKILL.md .claude/skills/ingest-slides/SKILL.md`
- Done when: ingest-article body ≤6,000 tok; ingest-slides body ≤3,000 tok (this spec's own target, §2.3 — not a stated §9 row).
- Rollback: not applicable (measurement only).

**S17-W4-3**
- Repo: learn-hub · depends on: S17-W1-12, S12-W0-4 (CX-34, I17 layout wrapper)
- Files: `evals/ingest-article/`, `evals/ingest-slides/` — 2 more cases each, per §4.1's "further cases" table
- Change: add the four case directories.
- Commands: `find evals/ingest-article evals/ingest-slides -name prompt.md | wc -l` → 10
- Done when: the command above → 10.
- Rollback: delete the four new case dirs.

**S17-W4-5 (new, critique P14, F14) — OWNER, Windows: one article re-run end to end**
- Repo: learn-hub (Windows) · depends on: S17-W4-0, S17-W4-1, S17-W4-2, S17-W4-3
- Files: `docs/rewrite/w4-article-baseline/<article-id>.json` (adds the re-run verdicts)
- Change: re-run the same PDF through the W4 ingest-article skill end to end, up to but not including sync (plan §0 rule 10), following the new `references/` pointers; run the same gates as S17-W4-0. Compare verdicts per gate (pass/fail), not scores: fresh LLM drafting varies between runs. Do not commit the re-drafted article.
- Done when: no gate's verdict went from pass to fail (architecture §10 W4 exit, "one article re-run end to end").
- Rollback: not applicable (verification); a regression goes back to S17-W4-1.

**S17-W4-4 (contributes to S12's live family set)**
- Repo: learn-hub · depends on: S17-W1-2, S17-W1-8, S18-W4-1 (routing.md final text; CX-38 — not all of "S18-W4", which would cycle against S18-W4-5's own dependency on this step)
- Files: none — §4.3 content handoff to S12
- Change: hand the §4.3 query list to S12 for the PDF-front-door family's live trigger set.
- Commands: none
- Done when: S12's family file contains every §4.3 query here.
- Rollback: not applicable.

## 4. Evals

### 4.1 Cases

`evals/ingest-article/trigger-positive/prompt.md`:
```markdown
---
allowed_tools: [Read, Glob, Grep, Skill]
tags: [ingest-article, trigger, smoke]
---
I have a new RCT PDF I want in the Learn hub — can you ingest this article? It's at ./paper.pdf.
```
`.../graders/fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?ingest-article"'
weight: 3
---
```

`evals/ingest-article/near-miss-ingest-slides/prompt.md`:
```markdown
---
allowed_tools: [Read, Glob, Grep, Skill]
tags: [ingest-article, negative, trigger]
---
Can you digest these lecture slides from journal club and get them into Articles? They're a
PPT/ folder of PDFs.
```
`.../graders/not-ingest-article.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?ingest-article"'
min: 0
max: 0
arm: both
weight: 3
---
```

`evals/ingest-article/inbox-survey-and-ask/case.yaml` (process case):
```yaml
schema_version: "1.1"
name: inbox-survey-and-ask
tags: [ingest-article, process, output, smoke]
context: { scaffold_script: fixture.sh }
execution:
  max_turns: 8
  allowed_tools: [Read, Glob, Grep, Skill, Bash(ls *), Bash(find *)]
  prompt: "Digest the drop folder."
```
`fixture.sh`: `mkdir -p "Raw Article PDF"; : > "Raw Article PDF/smith-2024.pdf"; : > "Raw Article PDF/jones-2025.pdf"`.
`.../graders/lists-before-writes.md`:
```markdown
---
type: tool_order
before: { tool: Glob }
after: { tool: Write }
weight: 2
---
```
`.../graders/no-delete.md`:
```markdown
---
type: regex
target: trace
pattern: 'rm\s+["'']?Raw Article PDF'
match: not_contains
weight: 3
---
```
(No `AskUserQuestion` granted, so the run exercises the headless "list and stop" branch by construction — §2.3, S17-W1-3. No `env` block: the skill reads `ARTICLE_INBOX_DIR`, which the eval allowlist would strip anyway, and its default relative path `Raw Article PDF/` is what the scaffold creates. The case is smoke-tagged because the W1 exit gate "bare ingest-article asks" runs it — critique F3.)

`evals/ingest-slides/trigger-positive/prompt.md`:
```markdown
---
allowed_tools: [Read, Glob, Grep, Skill]
tags: [ingest-slides, trigger, smoke]
---
I have a folder of PsychiTalk lecture PDFs I want to get into the hub — can you ingest these
slides? They're in PPT/.
```
`.../graders/fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?ingest-slides"'
weight: 3
---
```

`evals/ingest-slides/near-miss-ingest-article/prompt.md`:
```markdown
---
allowed_tools: [Read, Glob, Grep, Skill]
tags: [ingest-slides, negative, trigger]
---
Here's a journal article PDF — please add it to the Articles tab.
```
`.../graders/not-ingest-slides.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?ingest-slides"'
min: 0
max: 0
arm: both
weight: 3
---
```

`evals/ingest-slides/figure-gate-process/prompt.md` (process case):
```markdown
---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
tags: [ingest-slides, process]
---
Write a short note describing how you would gate a slide deck's diagrams before syncing it, for
the deck "adhd-brain-science.pdf". Name the exact commands you would run, in order.
```
`.../graders/names-check-figures.md`:
```markdown
---
type: regex
pattern: check-figures\.py
weight: 2
---
```
`.../graders/order.md`:
```markdown
---
type: regex
pattern: measure-loss\.py[\s\S]*check-figures\.py
weight: 1
---
```

**Further cases (W4, §4.1 table — name / tags / prompt gist / graders):**

| Skill | Case | Tags | Prompt gist | Graders |
|---|---|---|---|---|
| ingest-article | `dedup-existing-stub` | output | "Ingest this paper — it may already exist as a stub, check first" | `regex` over `trace` for `vault/articles`, `tool_used: Grep` |
| ingest-article | `preflight-refusal` | process, release | fixture with `PUPPETEER_EXECUTABLE_PATH` unset; "ingest this PDF" | `regex` on last_message for "ready.mjs" or "fix"; `tool_order` ready before Write |
| ingest-slides | `dedup-existing-speaker` | output | "Ingest this deck — the speaker may already have a deck in the vault" | `regex` over `trace` for `vault/articles`, `tool_used: Grep` |
| ingest-slides | `thai-english-mixed` | output, release | fixture deck with Thai filename; "get this lecture into the hub" | `llm` PASS-if title cleaned per lecture-adaptations.md table |

### 4.2 Conversion

No prior `evals.json` exists for either skill (confirmed: `find .claude/skills/ingest-article .claude/skills/ingest-slides -iname 'evals*'` → empty; the four plugin-copy `evals.json` files found in the repo belong to unrelated plugins). Nothing to convert.

### 4.3 Live triggers

Family (architecture §6.3): `{pdf-pipeline, ingest-article, ingest-slides, atomize-book, anthropic-skills:pdf, anthropic-skills:bullet-reconstruct}` — the "PDF front door" family, owned by S12 for assembly; this spec contributes the near-miss set for its two units.

| Query | Expected skill | Why it is a near-miss |
|---|---|---|
| "Bulletise this paper for me, keep it tight" | ingest-article | wording overlaps `anthropic-skills:bullet-reconstruct`'s own trigger vocabulary |
| "Turn this journal PDF into something I can read on the Articles page" | ingest-article | no literal "ingest" word |
| "Here's a stack of conference handout PDFs, get the high points into the hub" | ingest-slides | "handout" not "slides"; tests the PPT/-folder path without naming it |
| "Read through this deck slide by slide and pull out anything testable" | ingest-slides | matches the locked "review this deck slide by slide" phrase exactly — should win outright |

### 4.4 Commands

- Smoke: `scripts/eval-project-skill.sh ingest-article --smoke -- --allow-tools "Bash(ls *),Bash(find *)"`; `scripts/eval-project-skill.sh ingest-slides --smoke` (I17, owner S12; CX-46; the Bash grant is what `inbox-survey-and-ask` needs, and the wrapper passes `--scaffold`).
- Release (W4 exit): `scripts/eval-project-skill.sh ingest-article --release`; same for `ingest-slides` (CX-46).

## 5. Acceptance criteria

1. `git check-ignore -v "Raw Article PDF/x.pdf"` matches (S17-W1-1).
2. `python3 $MICKY_TOOLS_DIR/docs/plugin-rewrite/phase3/measure.py skill .claude/skills/ingest-article/SKILL.md` reports `yaml_valid: true`, `chars: 910`.
3. `python3 $MICKY_TOOLS_DIR/docs/plugin-rewrite/phase3/measure.py skill .claude/skills/ingest-slides/SKILL.md` reports `chars: 948`.
4. `grep -n 'C:\\Users\\User' .claude/skills/ingest-article/SKILL.md` prints nothing.
5. `grep -n '^python scripts/' .claude/skills/ingest-slides/SKILL.md` prints nothing (S17-W1-9).
6. `grep -c 'check-figures.py\|measure-loss.py' .claude/skills/ingest-slides/SKILL.md` → 2 (S17-W1-11).
7. `grep -n 'diagrams.*{}\|Skip the .npm run sync\|~40 minutes' .claude/skills/ingest-article/SKILL.md` prints nothing (S17-W1-6).
8. `grep -n 'keep-frontmatter --figures' .claude/skills/ingest-article/references/figures-and-loss.md` prints nothing (S17-W1-7).
9. `grep -n '_grill_text\|already available in this repo' .claude/skills/ingest-slides/scripts/*.py` prints nothing (S17-W1-10).
10. `find evals/ingest-article evals/ingest-slides -name prompt.md | wc -l` → 6 after W1, 10 after W4.
11. `python3 $MICKY_TOOLS_DIR/docs/plugin-rewrite/phase3/measure.py skill .claude/skills/ingest-article/SKILL.md` body est. tokens ≤6,000 after W4 (S17-W4-1/2).
12. `claude plugin validate --strict` (or `check:skills` once S21 lands) reports no new frontmatter-key violations on either skill.

## 6. Trigger lock

| Phrase | Source | Disposition |
|---|---|---|
| "ingest this article" | ingest-article desc | kept |
| "/ingest-article" | ingest-article desc | kept |
| "add this paper to the hub" | ingest-article desc | kept |
| "reconstruct + add this study" | ingest-article desc | moved → reworded "reconstruct this study" (same user intent, shorter) |
| "bullet-reconstruct this" | ingest-article desc | removed (collision with `anthropic-skills:bullet-reconstruct`, R7; architecture line 219) |
| "digest the folder" / "process the PDFs" / "ingest the inbox" | ingest-article desc | kept |
| "extract the high-yield content" | ingest-slides desc | kept |
| "digest these slides" | ingest-slides desc | kept |
| "get this lecture into the hub" | ingest-slides desc | kept |
| "add these decks to Articles" | ingest-slides desc | kept |
| "ingest these slides" | ingest-slides desc | kept |
| "review this deck slide by slide" | ingest-slides desc | kept |

## 7. Risks and OD sensitivity

- **K-risk**: the survey-and-ask rewrite (S17-W1-3) changes the owner's habit of a silent bare invocation. Mitigated: it only adds a confirmation, never silently deletes — R22 + I27's absent-behaviour text, no OD branch.
- **ingest-slides-5's new gate** adds a manifest + two script runs per deck (10+ extra tool calls for a 10-deck folder). Mitigation: both scripts are fast/lexical, and the manifest is only as large as the deck's visual-slide count (typically single digits).
- **OD9**: assumed (a) — no alias skill needed, neither unit had a bare `/` command distinct from its name.
- **OD11**: this spec's W4 work moves content into the skill's OWN `references/`, not `.claude/rules/` — identical under either OD11 branch.

## 8. Open questions

1. **ASSUMES** (I17): whether S12-W0-5's "content from … S17-W0" line means this spec's W1 cases (§4.1) or a separate pre-fix baseline S12 captures itself. Either reading is satisfied by shipping ≥3 cases/skill at W1. Check: does `baseline.md`'s ingest-article/ingest-slides row predate or postdate S17-W1's merge?
2. **ASSUMES**: dropping §5b (ingest-article-2) rather than fixing `measure-source-cover.mjs` is this spec's reading of the "fixed … or dropped" branch — the script is shared with `vault-coverage` (S20), owned by neither spec. Restorable with a one-line change if a future spec fixes the script; nothing else here depends on the choice.
3. **ARCH-CONFLICT: none found.** Every fix traces to architecture §3.6's rows or an explicitly assigned defect.
4. Coordination: confirm at wave-merge time that pdf-pipeline's rewritten routing (S18) names `ingest-slides` before/with S17-W1-8 shipping, so the family reads consistently.
