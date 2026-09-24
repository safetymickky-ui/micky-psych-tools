# Spec S18: pdf-pipeline (+ classify_pdf.py) and verify (+ bundled scripts)

| Field | Value |
|---|---|
| Repos | learn-hub |
| Units (today → target) | `.claude/skills/pdf-pipeline/{SKILL.md,references/{routing,preflight-and-apply,surface-checklist}.md}` (edit) + `scripts/classify_pdf.py`, `scripts/test_classify_pdf.py` (new, W4); `.claude/skills/verify/SKILL.md` (edit) + `scripts/{mint-session,probe}.mjs`, `scripts/{mint-session,probe}.test.mjs` (new, W4). Both skills keep name/dir. |
| Waves | W1 (H32, H33, pdf-pipeline-3..7, Not-for `anthropic-skills:pdf`, `ready.mjs` preflight); W4 (`classify_pdf.py`; verify's bundled scripts; description pass + trigger evals for the PDF front door) |
| Owner decisions assumed | none of OD1–OD14 changes this spec's content |
| Defects closed | 10 of 10 assigned (HIGH: H32, H33) |
| Interfaces owned | I26 |
| Interfaces consumed | I13 (owner S13), I17 (owner S12), I20 (owner S08), I21 (owner S21, not yet written), I22 (owner S21, not yet written) |
| Depends on specs | S13 (I13: `ready.mjs`/`sync-preflight.mjs` must exist before S18-W1-3); S17 (ingest-slides must exist and accept decks — it does today, unblocked by its own W1); S11 (I16 env vars `PUPPETEER_EXECUTABLE_PATH` etc. for verify's scripts, W4) |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| Path | Lines | Est. tokens | Role |
|---|---|---|---|
| `.claude/skills/pdf-pipeline/SKILL.md` | 207 | 2,686 (body) | orchestrator |
| `.claude/skills/pdf-pipeline/references/routing.md` | 86 | — | classification guide (edited) |
| `.claude/skills/pdf-pipeline/references/preflight-and-apply.md` | 90 | — | no-`.env.local` recipe (edited) |
| `.claude/skills/pdf-pipeline/references/surface-checklist.md` | 82 | — | surfacing checklist (edited) |
| `.claude/skills/verify/SKILL.md` | 64 | 774 (body) | procedure |

Neither ships a `commands/` directory (OBS "COMMANDS"); both invoked as `/pdf-pipeline` / `/verify`.

### 1.2 Descriptions

| Skill | Chars | UTF-8 bytes | YAML valid? | `Use when` offset | `Not for` present? | Quoted triggers (today) |
|---|---|---|---|---|---|---|
| pdf-pipeline | 934 | 940 | yes | 354 | yes (`/vault` content only — no sibling name) | "process this", "add this to the hub", "get this into the app", "ingest this PDF", "here's a PDF", "put this in Learn", "turn this PDF into notes", "I uploaded a PDF" |
| verify | 236 | 238 | yes | none (-1) | none (-1) | none |

### 1.3 Defects

| id | sev | H# | evidence (re-opened) | problem | fix step (fix) | wave |
|---|---|---|---|---|---|---|
| pdf-pipeline-1 | H | H32 | `SKILL.md:37` `└── report/extract► atomize-book (mini)`; `SKILL.md:60-61,101` "report/extract" step; `routing.md:14,40-42,60-61` route slide decks to `atomize-book` (mini), never mention `ingest-slides` | Two skills give opposite answers for a slide deck (S17's ingest-slides-2) | S18-W1-1, S18-W1-2 (add a fourth destination **Slides → `ingest-slides`** to `routing.md`'s table, §2.3; move the "slide deck exported to PDF" line out of Report/extract's signals; drop the "A slide deck → usually report/extract" edge case; `SKILL.md`'s diagram/table/step-3 text gain a `slides` branch) | W1 |
| pdf-pipeline-2 | H | H33 | `SKILL.md:138-141` "≲ ~200 KB → apply via Supabase MCP `execute_sql`"; `:150` "you don't need the whole 5.8 MB dump"; `surface-checklist.md:13` same rule; `atomize-book`/`ingest-article` (S17) say never run the `npm run sync` dry run | The rule can never be met (the dump is 5.8 MB, the threshold 200 KB) and contradicts the sub-skills it delegates to | S18-W1-4, S18-W1-5, S18-W1-6 (replace step 4 wholesale with the CX-17 sync-vault sentence; delete the size-check line from `surface-checklist.md`; replace `preflight-and-apply.md`'s manual SQL-splitting recipe with a pointer to I13's clean refusal) | W1 |
| pdf-pipeline-3 | M | — | `SKILL.md:36` `/atomize-book → /vault/<book>/<chapter>/*.md`; `routing.md:13` same | atomize-book's real layout is flat `vault/<topic-id>/_topic.md` (CLAUDE.md note-format) — the nested path is what the vault gotchas call the trap | S18-W1-1, S18-W1-2 (both files: `/vault/<book>/<chapter>/*.md` → `/vault/<topic-id>/*.md`) | W1 |
| pdf-pipeline-4 | M | — | `SKILL.md:178-179` "the **graph** (new book/chapter hubs + edges)"; `surface-checklist.md:59` "card wall" | The graph view was removed (CLAUDE.md Phase 4); `/books` is a shelved library (ShelfHeader disclosure), not a "card wall" | S18-W1-6 (delete the graph bullet; replace "card wall" with "category shelf, nested book → part → chapter, expanding to peek notes", matches CLAUDE.md §1b) | W1 |
| pdf-pipeline-5 | M | — | `SKILL.md:59` "A remote/web session starts with **no `node_modules`, no `.env.local`**" | Stale: the SessionStart hook (I14, owned by S13) now provisions both automatically | S18-W1-3 (replace "## 0. Preflight" with `node scripts/ready.mjs`, I13 — same preflight step S17 gives ingest-article/ingest-slides) | W1 |
| pdf-pipeline-6 | M | — | `surface-checklist.md:43` "(`flowchart`/`mindmap` only …) and re-run `npm run sync`" | Restricts mermaid types atomize-book allows (sequenceDiagram/stateDiagram-v2/…); `npm run sync` never writes the DB | S18-W1-6 (point at `node scripts/check-mermaid.mjs`, full type set, the real prebake renderer, and the I13 sync tail, not a bare dry run) | W1 |
| pdf-pipeline-7 | L | — | `routing.md:82` `grep -rh "^id:" vault/*/_topic.md` — one-level glob | Misses nested books (the vault is not two levels deep for every book) | S18-W1-7 (`find vault -name '_topic.md' -exec grep -h '^id:' {} +`) | W1 |
| pdf-pipeline-8 | L | — | `routing.md:20-45` prose signal checklist; `SKILL.md:94-98` classify table | Routing is judgment-only; a deterministic pre-classifier could narrow most cases and leave only the edge cases to judgement | S18-W4-1 (`scripts/classify_pdf.py`, I26, §2.5: DOI/ISBN/abstract/TOC/page-count/low-text-ratio signals → a suggested route JSON; step 2 runs it first, then confirms against the first pages) | **W4** |
| verify-1 | M | — | `SKILL.md:41-43` "Full working scripts from the last run: see the session scratchpad pattern below" — no `scripts/` dir in the skill (confirmed: `find .claude/skills/verify -type f` → SKILL.md only) | Deterministic mint-session/cookie/puppeteer code re-implemented from prose every run instead of bundled and reused | S18-W4-2, S18-W4-3 (bundle `scripts/mint-session.mjs` + `scripts/probe.mjs`, §2.5 — the prose recipe made executable) | **W4** |
| verify-2 | L | — | desc 236 chars, no `Use when`/`Not for` (§1.2); body hardcodes `/home/user/learn-hub/node_modules`, `/opt/pw-browsers/chromium` | No triggers to route on; cloud-only absolute paths break on a differently-rooted checkout | S18-W4-2, S18-W4-3 (rewrite description, §2.2, 734 chars, with triggers + Not-for; scripts resolve ROOT by walking to the learn-hub marker and Chromium from `$PUPPETEER_EXECUTABLE_PATH`, I13's `checkChromium`, never a literal path) | **W4** |

Count: 10 of 10 assigned. No deferrals.

### 1.4 Other findings (OBS lines touching these units; NEW = found this session)

- **ROUTING OVERLAP** (OBS): pdf-pipeline is the declared PDF front door and gave a different answer than ingest-slides for the same input — closed by pdf-pipeline-1/S17's ingest-slides-2 together; land the same wave.
- **PDF TOOLING ABSENT** (OBS): `import fitz`/`pypdf`/`pdfplumber` all raise `ModuleNotFoundError`, `pdftoppm`/`pdftotext` not on PATH — matches pdf-pipeline-5's fix (`ready.mjs`'s `pymupdf`/`poppler` checks) and is also `classify_pdf.py`'s own W4 precondition.
- **SHARED SYNC TAIL** (OBS): pdf-pipeline restated the apply rule in 3 places (`SKILL.md`, `preflight-and-apply.md`, `surface-checklist.md`) — all three are fixed under pdf-pipeline-2 in one wave, closing the "8 restatements, 4 contradictory rules" finding for this unit's share of it.
- **NEW**: no script in either repo already mints a Supabase magic-link session or drives puppeteer with it (grep for `generateLink`/`magiclink`/`verifyOtp` across `scripts/` → empty) — confirms `mint-session.mjs`/`probe.mjs` are genuinely new, not a duplicate of existing tooling.
- **NEW**: `apply-sync.mjs`'s `loadEnv()` (reads `.env.local` relative to the script's own resolved root, never `process.env`) is the pattern `verify-mint.mjs` reuses, generalised into a marker walk-up (CX-26) rather than a fixed relative-parent count — `apply-sync.mjs` sits at repo-root `scripts/`, but the verify CLI wrapper sits three levels deeper at `.claude/skills/verify/scripts/`, so the fixed-depth form would resolve to the wrong directory here. Keeps the "never hardcode `/home/user`" rule (validator check, §8 of the architecture) satisfied for free either way.

## 2. Target state

### 2.1 Location and tree (after W4)

```
.claude/skills/pdf-pipeline/
  SKILL.md                              rewritten (§2.3)
  references/{routing,preflight-and-apply,surface-checklist}.md   edited (§1.3)
  scripts/classify_pdf.py               NEW, W4 (§2.5, I26)
  scripts/test_classify_pdf.py          NEW, W4 (unittest)
.claude/skills/verify/
  SKILL.md                              rewritten (§2.3)
  scripts/mint-session.mjs              NEW, W4 — thin CLI wrapper (§2.5, CX-26)
  scripts/probe.mjs                     NEW, W4 — thin CLI wrapper (§2.5, CX-26)
scripts/lib/
  verify-mint.mjs                       NEW, W4 — pure logic (CX-26: `vitest.config.ts` only
  verify-mint.test.mjs                    collects `src/**` and repo-root `scripts/**/*.test.mjs`,
  verify-probe.mjs                        never `.claude/skills/*/scripts/*.test.mjs` — a test
  verify-probe.test.mjs                   left inside the skill dir would never run under `npm test`)
```

### 2.2 Frontmatter

**pdf-pipeline**:

```yaml
---
name: pdf-pipeline
description: >-
  The front door for a user-uploaded PDF: classifies what it is (a journal article, a book or
  textbook, a slide/lecture deck, or a long report or extract), routes it to the right
  authoring skill, then owns the shared sync, revalidate and verify tail so the content
  actually appears in the Learn app. Use whenever the user uploads or points at a .pdf and
  says "process this", "add this to the hub", "get this into the app", "ingest this PDF",
  "here's a PDF", "put this in Learn", "turn this PDF into notes", "I uploaded a PDF", or
  drops a file without naming a pipeline. Delegates the authoring to ingest-article,
  ingest-slides, or atomize-book and never duplicates their steps. Not for content already in
  /vault (use sync-vault), and not for general PDF editing, merging or OCR with no Learn-hub
  destination (use anthropic-skills:pdf).
---
```

Measured: 833 chars; `Use when` at 298; `Not for` at 676. Kept triggers: all eight unchanged. New Not-for target: `anthropic-skills:pdf` (architecture: "a Not-for naming `anthropic-skills:pdf`").

**verify**:

```yaml
---
name: verify
description: >-
  Drives the real Learn-hub app end to end in this repo's cloud environment: builds it, starts
  it, mints a real owner session with no password (a service-role magic link turned into a
  session cookie), then screenshots and probes pages with puppeteer to confirm a change
  actually renders and works for a logged-in user. Use when no human can log in to check a UI
  or auth-gated change, or the user says "verify this in the real app", "check this actually
  renders", "screenshot this logged in", "confirm this shows up for the owner". Not for a
  quick unauthenticated look at a page (use the built-in browser or Claude in Chrome) or for
  reading page state through an isolated-world script (see Gotchas) instead of driving it with
  real input.
---
```

Measured: 734 chars; `Use when` at 317; `Not for` at 529. New triggers: all four (none existed before, verify-2). New Not-for: the built-in browser pane / Claude in Chrome (for unauthenticated checks) and a self-reference to the isolated-world gotcha (not a sibling skill, but the same slot names the mistake this skill exists to avoid — see §7 for the reading).

## 2.3 Body outline

**pdf-pipeline** (target ≈180 lines, was 207 — the size-rule paragraphs shrink to one line each):

| Source lines | Disposition |
|---|---|
| 1–29 (diagram) | keep; step `[2]` gains a `slides` branch (pdf-pipeline-1); step-2's arrow target `/vault/<book>/<chapter>/*.md` → `/vault/<topic-id>/*.md` (-3) |
| 30–56 (§0 Preflight) | **replace wholesale** with `node scripts/ready.mjs` (I13) — ≈2 lines, was 9 (-5) |
| 57–86 (§1 Land the file) | keep verbatim |
| 88–110 (§2 Classify) | table gains a **Slides** row; **W4**: add "run `classify_pdf.py` first" line |
| 111–133 (§3 Hand off) | keep article/book bullets; add a **slides** bullet naming `ingest-slides`; keep report/extract, now scoped to non-slide long extracts only |
| 134–156 (§4 Sync) | **replace wholesale** with the CX-17 sync-vault sentence, verbatim (-2) |
| 157–169 (§5 Revalidate) | keep verbatim (unchanged rule, matches I13) |
| 170–185 (§6 Verify) | drop the "graph" bullet (-4); "card wall" → "shelved library" wording |
| 186–207 (§7 Document, Guardrails) | keep verbatim |

**verify** (target ≈75 lines, was 60 — the two new script pointers add ~15):

| Source lines | Disposition |
|---|---|
| 1–4 (frontmatter) | rewrite (§2.2) |
| 6–24 (Build + serve) | keep verbatim (no defect) |
| 26–37 (Mint an owner session) | **replace** the prose recipe with: "run `node scripts/mint-session.mjs --email <owner email> --out session.json`" — the script IS the recipe now (verify-1) |
| 38–43 (Drive + capture) | **replace** with: "run `node scripts/probe.mjs <path> --cookies session.json --screenshot out.png`" |
| — | **new `## Gotchas`**: the browser-pane-does-not-composite and chrome-devtools-isolated-world traps (from CLAUDE.md, quoted; §7), plus the existing inline "Gotchas that actually bit" bullets folded in under R23's house shape |

## 2.4 References

| File | Purpose | Load condition | Size |
|---|---|---|---|
| `routing.md` | classification signals + edge cases | "when the call isn't obvious" (unchanged) | unchanged length, table + 2 bullets edited |
| `preflight-and-apply.md` | no-`.env.local` recipe | unconditional today (unchanged load condition) | the SQL-splitting recipe replaced by a 2-line I13 pointer |
| `surface-checklist.md` | per-route surfacing checks | unconditional (unchanged) | 2 lines fixed, rest unchanged |

## 2.5 Scripts

**`scripts/classify_pdf.py`** (new, W4 — **I26 owned here**)
CLI: `python3 .claude/skills/pdf-pipeline/scripts/classify_pdf.py <pdf-path> [--pages N] [--json]`. `--pages N` caps how many leading pages are scanned for signals (default 15). `--help` prints usage, no side effects.
Input: one PDF file path (positional, required).
Behavior: opens with PyMuPDF, reads `doc.get_toc()` and `doc.page_count`, extracts text of the first `--pages` pages. Regex-scans for a DOI (`10\.\d{4,9}/\S+`), an ISBN-10/13, an "Abstract" heading, a "References"/"Bibliography" heading; computes average words/sampled-page and the fraction of sampled pages under 40 chars of text (the same `LOW_TEXT_CHARS` convention `ingest-slides/scripts/extract_pdf.py` already uses). The DECISION is a pure function, `decide_route(signals: dict) -> (route, confidence, reasons)`, called by the I/O wrapper:
1. `isbn` present, or `toc_entries >= 3` and `page_count >= 40` → `"book"`.
2. `doi` and `has_abstract` and `has_references` → `"article"`.
3. `low_text_page_ratio >= 0.5` and `page_count >= 5` → `"slides"`.
4. else → `"report"`.
Confidence: 0.6 base + 0.1 per corroborating signal beyond the deciding one, capped 0.95.
JSON stdout:
```json
{"path": "<abs>", "route": "article", "confidence": 0.9,
 "signals": {"doi": "10.1001/...", "isbn": null, "has_abstract": true, "has_references": true,
             "toc_entries": 0, "page_count": 12, "pages_sampled": 12,
             "avg_words_per_sampled_page": 410, "low_text_page_ratio": 0.0},
 "reasons": ["doi+abstract+references -> article"]}
```
Exit codes: `0` classified (any route, including the `"report"` fallback); `1` file not found / not a PDF / PyMuPDF missing (prints the fix, `pip install pymupdf`); `2` PDF open/parse failure.
Tests (`scripts/test_classify_pdf.py`, `unittest`, run by `npm run test:py`): `decide_route` exercised directly with constructed signal dicts — an article-shaped dict, a book-shaped dict (ISBN), a book-shaped dict (TOC+pages, no ISBN), a slides-shaped dict, an ambiguous/ all-false dict → `"report"`. No PDF fixtures, no PyMuPDF import needed for these cases (pure function). One `unittest.mock`-based test drives the CLI wrapper end-to-end against a `fitz`-shaped stub to confirm the JSON shape and exit codes.

**`scripts/lib/verify-mint.mjs`** (new, W4 — repo-root, pure logic, CX-26) + **`.claude/skills/verify/scripts/mint-session.mjs`** (new, W4 — thin CLI wrapper, imports from the lib)
CLI (on the wrapper): `node scripts/mint-session.mjs --email <owner-email> [--out <file>] [--json]`. `--email` required — never hardcoded, so no real address sits in a committed script.
Root resolution (CX-26 — not `dirname(dirname(fileURLToPath(import.meta.url)))`, which resolves to the wrong directory now that the wrapper lives three levels deeper, under `.claude/skills/verify/scripts/`, than `apply-sync.mjs`'s repo-root `scripts/`): walk up from the wrapper's own path to the nearest ancestor carrying the learn-hub marker (`package.json` `"name": "learn-hub"` + `scripts/apply-sync.mjs`, same marker I14/I27 use), then load `.env.local` from there.
Input: `.env.local` via the walked-up `loadEnv()` above (no `process.env`, no hardcoded root, no fixed relative-parent count).
Behavior (in `verify-mint.mjs`, pure where possible): admin client (`SUPABASE_SERVICE_ROLE_KEY`) `auth.admin.generateLink({type:"magiclink", email})`; anon client `auth.verifyOtp({type:"magiclink", token_hash: linkData.properties.hashed_token})` → a session; cookie name `sb-<project-ref>-auth-token` (project-ref = the first label of `NEXT_PUBLIC_SUPABASE_URL`'s hostname); value `"base64-" + base64url(JSON.stringify(session))`, chunked at 3,180 chars into `.0`/`.1`/… suffixes via the pure, exported `chunkCookieValue(name, value, limit=3180)` — this and the root-walk function are what `verify-mint.test.mjs` covers; the wrapper holds only argv parsing and the two Supabase client calls.
JSON stdout (or `--out <file>`):
```json
{"project_ref": "abc123", "email": "owner@example.com",
 "cookies": [{"name": "sb-abc123-auth-token", "value": "...", "domain": "localhost", "path": "/"}]}
```
Exit codes: `0` success; `1` missing env vars or no learn-hub marker found (names which); `2` `generateLink`/`verifyOtp` failed (prints the Supabase error).
Tests (`scripts/lib/verify-mint.test.mjs`, vitest, repo-root — collected by `vitest.config.ts`, CX-26): `chunkCookieValue` — a value under 3,180 chars returns one `{name, value}` pair; a value over it returns `name.0`/`name.1`/… each ≤3,180 chars whose concatenation round-trips to the input. The root-walk function, against a fixture directory tree with and without the marker. No network in tests.

**`scripts/lib/verify-probe.mjs`** (new, W4 — repo-root, pure logic, CX-26) + **`.claude/skills/verify/scripts/probe.mjs`** (new, W4 — thin CLI wrapper)
CLI (on the wrapper): `node scripts/probe.mjs <path> [--base http://localhost:3100] [--cookies <file>] [--screenshot <out.png>] [--viewport 1280x1000|390x844] [--json]`.
Input: `<path>` a route (e.g. `/articles`); `--cookies <file>` the JSON `mint-session.mjs` wrote (falls back to stdin if piped, `--cookies -`).
Behavior (puppeteer-driving in the wrapper; `parseViewport` pure in `verify-probe.mjs`): launches puppeteer with `executablePath: process.env.PUPPETEER_EXECUTABLE_PATH` (refuses with `readiness.mjs`'s `checkChromium` message if unset/missing — I13, never a literal `/opt/…` path), `args: ["--no-sandbox"]`; sets the cookies for domain `localhost`; navigates to `<base><path>`; screenshots to `--screenshot` when given, at the parsed `--viewport` (default `1280x1000`, `deviceScaleFactor` 2 for the `390x844` form per the existing "Screenshot at 1280×1000 and 390×844" rule); collects `console` "error"-level events.
JSON stdout: `{"url": "...", "status": 200, "title": "...", "screenshot": "out.png"|null, "console_errors": 0}`.
Exit codes: `0` navigation completed (the caller reads `status`/`console_errors` to judge success); `1` launch or navigation error (timeout, connection refused, Chromium missing).
Tests (`scripts/lib/verify-probe.test.mjs`, vitest, repo-root — CX-26): the pure `parseViewport("1280x1000")` → `{width:1280,height:1000,deviceScaleFactor:1}`; `"390x844"` → same with `deviceScaleFactor:2` (the documented convention); a malformed spec throws with a named error. The puppeteer-driving path stays in the wrapper, integration-only, uncovered by unit tests (CLAUDE.md Testing: "anything needing a live DOM/browser" is out of scope).

## 2.6 Handoffs

pdf-pipeline hands off to three skills, each carrying the §4.2 fallback sentence verbatim:

> Run `ingest-article` / `ingest-slides` / `atomize-book` (OPTIONAL). If it is not available in this session, take the broadest reading that fits and open the output with `Assumed: <reading> — say if wrong.`

verify makes no handoff — it is a terminus diagnostic skill, invoked directly.

## 2.7 Interfaces

**Owned:**

- **I26 — `scripts/classify_pdf.py`.** Full CLI, input, JSON shape, exit codes and test plan in §2.5. Consumer: S17 (ingest-article) ASSUMES the `route` enum is exactly `"article"|"book"|"slides"|"report"` — confirmed the value `"slides"` maps 1:1 to the new routing-table destination (§2.3), so S17's own ASSUMES (its §2.7) needs no correction.

**Consumed:**

- **I13 (owner S13).** ASSUMES `node scripts/ready.mjs` and `npm run sync:preflight` exist by S18-W1 (S13 is first in the W1 list, pdf-pipeline is third). pdf-pipeline's `## 0. Preflight` is `node scripts/ready.mjs`; step 4 (sync) carries S13's exact CX-17 handoff sentence, not restated. `probe.mjs` (W4) imports `checkChromium` directly from `scripts/lib/readiness.mjs` rather than re-testing for the Chromium path itself.
- **I17 (owner S12).** ASSUMES `learn-hub/evals/pdf-pipeline/<case>/` and `evals/verify/<case>/`, run through `scripts/eval-project-skill.sh <skill>` (S12-W0-4). §4.1 follows that layout.
- **I20 (owner S08).** ASSUMES the frontmatter whitelist/description grammar apply unchanged to project skills (T2). Neither skill needs an alias.
- **I21 (owner S21, not yet written).** ASSUMES `gotcha-map.md` will confirm whether the browser-pane/chrome-devtools-isolated-world gotchas belong solely in verify's own `## Gotchas` (this spec's reading, §2.3) or also in a shared `.claude/rules/*.md` — either way this spec's W4 addition is correct content, just possibly duplicated once S21 lands; flagged in §8.
- **I22 (owner S21, not yet written).** ASSUMES the package.json edit list adds `test:py` (already named in the architecture, owned by S21) which will pick up `test_classify_pdf.py` automatically (unittest discovery over `.claude/skills/*/scripts/test_*.py`, matching atomize-book's existing convention) — no new script name needed from this spec.

## 3. Change steps

### Wave 0

**S18-W0-1 (new, CX-4)**
- Repo: learn-hub · depends on: S12-W0-4
- Files: create 3 `evals/pdf-pipeline/*` case directories, tagged `smoke`, ahead of S18-W1-9's fuller set. They take the names of the three §4.1 cases S18-W1-9 lists (`trigger-positive`, `near-miss-book`, `slides-routing`), so S18-W1-9 extends them instead of adding new ones (critique P7).
- Change: seed 3 `smoke`-tagged cases against TODAY's pdf-pipeline SKILL.md, I17 layout, current script paths (architecture §10 W0 item 3) — the pre-rewrite baseline S12's smoke suite needs.
- Commands: `find evals/pdf-pipeline -name prompt.md | xargs grep -l 'tags:.*smoke' | wc -l`
- Done when: the count is ≥3.
- Rollback: delete `evals/pdf-pipeline/`.

### Wave 1

**S18-W1-1**
- Repo: learn-hub · depends on: none
- Files: edit `.claude/skills/pdf-pipeline/references/routing.md`
- Change: add a row to the destinations table (line 10-14): `| **Slides** | one enriched card in the **Articles** hub | `ingest-slides` | `/vault/articles/<slug>.md` |`; change the Book row's Vault path `/vault/<book>/<chapter>/*.md` → `/vault/<topic-id>/*.md` (pdf-pipeline-3); delete "a **slide deck** exported to PDF" from the Report/extract signals (line 42); delete the "A slide deck → usually report/extract…" edge case (lines 60-61) and replace it with "**A slide/lecture deck** → **slides**. Route to `ingest-slides`; it reads every slide visually, which preserves the deck's own structure instead of reconstructing an essay."; add one line under "After routing": "**`ingest-slides`**: the deck PDF or folder of decks; it self-reads every slide."
- Commands: `grep -n "slide deck.*report/extract\|report/extract.*slide deck" .claude/skills/pdf-pipeline/references/routing.md`; `grep -c "ingest-slides" .claude/skills/pdf-pipeline/references/routing.md`
- Done when: the first grep prints nothing; the second → ≥3.
- Rollback: restore the table, signal list and edge case verbatim.

**S18-W1-2**
- Repo: learn-hub · depends on: S17-W1-8 (ingest-slides' description lands the same wave, §7)
- Files: edit `.claude/skills/pdf-pipeline/SKILL.md`
- Change: diagram (lines 30-37): add `├── slides ──────►  /ingest-slides  → /vault/articles/<slug>.md` between the article and book branches; book branch's target `/vault/<book>/<chapter>/*.md` → `/vault/<topic-id>/*.md`; step 2's table (lines 94-98) gains a Slides row mirroring routing.md's; step 3 (lines 111-133) gains a bullet: "**slides** → run **`/ingest-slides`**. It renders and vision-reads every slide, then writes `/vault/articles/<slug>.md` with the same schema `ingest-article` uses."
- Commands: `grep -c "ingest-slides" .claude/skills/pdf-pipeline/SKILL.md`
- Done when: the command → ≥3.
- Rollback: revert the diagram, table and step-3 addition.

**S18-W1-3**
- Repo: learn-hub · depends on: S13-W1-2 (CX-34 — `ready.mjs` must exist)
- Files: edit `.claude/skills/pdf-pipeline/SKILL.md` (lines 57-65, "## 0. Preflight")
- Change: replace the whole section with:
  ```markdown
  ## 0. Preflight

  `node scripts/ready.mjs` — five checks (node_modules, `.env.local`/env vars, Chromium,
  PyMuPDF, poppler). Fix whatever it names; do not work around a failed check.
  ```
- Commands: `grep -n "no .node_modules., no .\.env\.local\|often no PDF renderer" .claude/skills/pdf-pipeline/SKILL.md`
- Done when: the grep above prints nothing, and `grep -c "ready.mjs" .claude/skills/pdf-pipeline/SKILL.md` → 1.
- Rollback: restore the original preflight prose.

**S18-W1-4**
- Repo: learn-hub · depends on: S13-W1-6 (CX-34/CX-17 — sync-vault must exist to be pointed at)
- Files: edit `.claude/skills/pdf-pipeline/SKILL.md` (lines 134-156, "## 4. Sync to Supabase")
- Change: replace the whole section with (CX-17 — the sync-vault sentence, verbatim, no restated procedure):
  ```markdown
  ## 4. Sync to Supabase

  Publish through the `sync-vault` skill (same repo, always present). Follow its steps as
  written; do not restate them here. Target project is the shared ref `juvoohejxuuvwolmgoep`
  — never the deprecated `tyxnedapxscpmytanloz`.
  ```
- Commands: `grep -n "200 KB\|200KB\|5.8 MB" .claude/skills/pdf-pipeline/SKILL.md`
- Done when: the grep above prints nothing.
- Rollback: restore lines 134-156 verbatim.

**S18-W1-5**
- Repo: learn-hub · depends on: S13-W1-6 (CX-34)
- Files: edit `.claude/skills/pdf-pipeline/references/preflight-and-apply.md` (the whole "Applying the sync when there IS no `.env.local`" section, lines 41-83)
- Change: replace the section body with: "`sync:preflight` (I13) refuses cleanly when `.env.local`/the service-role key is missing and names the fix (`bash .claude/hooks/session-start.sh`). There is no manual SQL-splitting path any more — fix the named gap, then run the normal tail." Keep the "Revalidation without secrets" section (lines 85-90) unchanged (still accurate — `npm run revalidate` genuinely no-ops without `APP_URL`/`REVALIDATE_SECRET`, and that stays true under I13).
- Commands: `grep -n "dollar-quoting\|split on semicolons\|Slim the .diagrams." .claude/skills/pdf-pipeline/references/preflight-and-apply.md`
- Done when: the grep above prints nothing.
- Rollback: restore the section verbatim.

**S18-W1-6**
- Repo: learn-hub · depends on: S13-W1-6 (CX-34)
- Files: edit `.claude/skills/pdf-pipeline/references/surface-checklist.md`
- Change: (a) lines 11-15 code block: delete the `# apply per size (MCP execute_sql if ≲200KB, else npm run sync:apply)` comment line, replace `npm run sync` with the I13 tail's `npm run sync:preflight && npm run sync:apply` (backgrounded per I13; shown foreground here only as the checklist's own smoke command); (b) line 43: replace with "A blank diagram means the fence failed to prebake — validate with `node scripts/check-mermaid.mjs vault/...` (the full type set atomize-book supports, not just `flowchart`/`mindmap`), fix what it flags, then re-run the sync tail (I13) — `npm run sync` alone never writes the DB."; (c) line 59: `**book wall**` phrasing → "the import appears under its category shelf, nested book → part (domain) → chapter (topic); the chapter row expands to peek notes inline"; (d) lines 178-179 equivalent in `SKILL.md` step 6 (line 179): delete "the **graph** (new book/chapter hubs + edges)," entirely.
- Commands: `grep -n "200KB\|card wall\|the .graph." .claude/skills/pdf-pipeline/references/surface-checklist.md .claude/skills/pdf-pipeline/SKILL.md`
- Done when: the grep above prints nothing.
- Rollback: restore all four edits verbatim.

**S18-W1-7**
- Repo: learn-hub · depends on: none
- Files: edit `.claude/skills/pdf-pipeline/references/routing.md` (line 82)
- Change: `grep -rh "^id:" vault/*/_topic.md` → `find vault -name '_topic.md' -exec grep -h '^id:' {} +`.
- Commands: `grep -n 'vault/\*/_topic.md' .claude/skills/pdf-pipeline/references/routing.md`
- Done when: the grep above prints nothing.
- Rollback: restore the one-level glob.

**S18-W1-8**
- Repo: learn-hub · depends on: none
- Files: edit `.claude/skills/pdf-pipeline/SKILL.md` (frontmatter)
- Change: replace the description with §2.2's 833-char version.
- Commands: `python3 $MICKY_TOOLS_DIR/docs/plugin-rewrite/phase3/measure.py skill .claude/skills/pdf-pipeline/SKILL.md`
- Done when: the command reports `"yaml_valid": true` and `"chars": 833`.
- Rollback: restore the original description.

**S18-W1-9**
- Repo: learn-hub · depends on: S18-W1-1 through S18-W1-8, S18-W0-1 (extends its seeds, CX-4)
- Files: extend `evals/pdf-pipeline/{trigger-positive,near-miss-book,slides-routing}/` (the S18-W0-1 seeds)
- Change: three case directories, full contents in §4.1.
- Commands: `find evals/pdf-pipeline -name prompt.md | wc -l`
- Done when: the command → 3.
- Rollback: `git revert <this commit>` (the W0 seeds stay).

### Wave 4

**S18-W4-1**
- Repo: learn-hub · depends on: S18-W1-1/-2 (routing text `classify_pdf.py` must agree with)
- Files: create `.claude/skills/pdf-pipeline/scripts/classify_pdf.py`, `scripts/test_classify_pdf.py`; edit `SKILL.md` step 2
- Change: implement `decide_route` + the I/O wrapper per §2.5; step 2 gains: "Run `python3 ${CLAUDE_SKILL_DIR}/scripts/classify_pdf.py <pdf>` first — read its suggested `route` and `confidence`, then confirm against the first few pages before committing (it narrows most cases; ambiguous or low-confidence ones still need your judgement)."
- Commands: `python3 -m unittest .claude/skills/pdf-pipeline/scripts/test_classify_pdf.py`; `python3 .claude/skills/pdf-pipeline/scripts/classify_pdf.py --help`
- Done when: the unittest run is green (≥5 cases across the four routes + ambiguous); `--help` exits 0 with no side effects.
- Rollback: delete both new files; revert the step-2 addition.

**S18-W4-2**
- Repo: learn-hub · depends on: S21-W4a-2 (it creates `verify/references/gotchas.md` with these two gotchas, verbatim; critique P29)
- Files: edit `.claude/skills/verify/SKILL.md`
- Change: replace the frontmatter with §2.2's 734-char description; replace "Mint an owner session" (source lines 26-37) with a pointer to `node scripts/mint-session.mjs --email <owner email> --out session.json`; replace "Drive + capture" (lines 38-43) with a pointer to `node scripts/probe.mjs <path> --cookies session.json --screenshot out.png`; add `## Gotchas` (new) with one pointer line — "Before driving the app, read `references/gotchas.md` (the in-app browser pane does not composite; chrome-devtools `evaluate_script` runs in an isolated world)." — instead of restating the two gotchas S21-W4a-2 already moved there, so they exist once (critique P29).
- Commands: `grep -n "/home/user/learn-hub\|/opt/pw-browsers" .claude/skills/verify/SKILL.md`
- Done when: the grep above prints nothing (the only remaining path text is inside the two new scripts, which resolve it at runtime, not in prose).
- Rollback: revert all four sub-changes.

**S18-W4-3**
- Repo: learn-hub · depends on: S18-W4-2
- Files: create `scripts/lib/verify-mint.mjs`, `scripts/lib/verify-mint.test.mjs`, `scripts/lib/verify-probe.mjs`, `scripts/lib/verify-probe.test.mjs` (repo-root, pure logic + tests); `.claude/skills/verify/scripts/mint-session.mjs`, `scripts/probe.mjs` (thin CLI wrappers, importing from the lib files above) — CX-26
- Change: implement the pure logic + tests in `scripts/lib/`, and the thin CLI wrappers (argv parsing, the Supabase/puppeteer calls) in the skill's own `scripts/`, per §2.5. The wrapper resolves the repo root by walking up to the learn-hub marker (§2.5), not a fixed relative-parent count.
- Commands: `node --check .claude/skills/verify/scripts/mint-session.mjs`; `node --check .claude/skills/verify/scripts/probe.mjs`; `npx vitest run scripts/lib/verify-mint.test.mjs scripts/lib/verify-probe.test.mjs`
- Done when: both `--check`s exit 0; the vitest run is green (chunking round-trip cases + viewport-parsing cases + root-walk cases) — and runs under a plain `npm test` from the repo root with no extra flags, confirming `vitest.config.ts` actually collects it (CX-26).
- Rollback: delete all six files; the SKILL.md pointers from S18-W4-2 become dangling — revert that step too if rolling this one back alone.

**S18-W4-4**
- Repo: learn-hub · depends on: S18-W1-9, S12-W0-4 (CX-34, I17 layout wrapper)
- Files: create `evals/verify/{scripts-exist,triggers-not-browser-pane,mint-and-probe-order}/`; add 1 more case to `evals/pdf-pipeline/` (per §4.1's further-cases table)
- Change: the case directories, full/gist contents in §4.1.
- Commands: `find evals/pdf-pipeline evals/verify -name prompt.md | wc -l`
- Done when: the command → 7 (4 pdf-pipeline + 3 verify).
- Rollback: delete the new case dirs.

**S18-W4-5 (contributes to S12's live family set)**
- Repo: learn-hub · depends on: S18-W1-8, S17-W4-4 (shared family)
- Files: none — §4.3 content handoff to S12
- Change: hand the §4.3 query list to S12 for the PDF-front-door family's live trigger set (same family as S17).
- Commands: none
- Done when: S12's family file contains every §4.3 query here.
- Rollback: not applicable.

## 4. Evals

### 4.1 Cases

`evals/pdf-pipeline/trigger-positive/prompt.md`:
```markdown
---
allowed_tools: [Read, Glob, Grep, Skill]
tags: [pdf-pipeline, trigger, smoke]
---
I uploaded a PDF — can you get it into the Learn hub? It's at ./upload.pdf.
```
`.../graders/fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?pdf-pipeline"'
weight: 3
---
```

`evals/pdf-pipeline/near-miss-book/prompt.md`:
```markdown
---
allowed_tools: [Read, Glob, Grep, Skill]
tags: [pdf-pipeline, negative, trigger]
---
Here's a textbook PDF with 14 chapters — atomize it into the vault.
```
`.../graders/not-pdf-pipeline.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?pdf-pipeline"'
min: 0
max: 0
arm: both
weight: 2
---
```
(A direct "atomize it" request names its own skill; this checks pdf-pipeline does not also fire redundantly — `arm: both` since a plugin with no pdf-pipeline loaded should show the same behavior.)

`evals/pdf-pipeline/slides-routing/prompt.md` (process case, output case):
```markdown
---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
tags: [pdf-pipeline, process, output]
---
This PDF is a 40-slide PsychiTalk lecture deck exported from PowerPoint. Which pipeline should
handle it, and why? Don't ingest anything — just tell me the route and the skill name.
```
`.../graders/names-ingest-slides.md`:
```markdown
---
type: regex
pattern: ingest-slides
weight: 3
---
```
`.../graders/not-atomize-book.md`:
```markdown
---
type: regex
target: last_message
pattern: atomize-book
match: not_contains
weight: 2
---
```

`evals/verify/scripts-exist/prompt.md` (output case):
```markdown
---
allowed_tools: [Read, Glob, Grep]
tags: [verify, output]
---
List the scripts the verify skill bundles for minting a session and probing a page, with their
paths.
```
`.../graders/names-both.md`:
```markdown
---
type: regex
pattern: mint-session\.mjs[\s\S]*probe\.mjs
weight: 3
---
```

`evals/verify/triggers-not-browser-pane/prompt.md` (negative case):
```markdown
---
allowed_tools: [Read, Glob, Grep, Skill]
tags: [verify, negative, trigger]
---
Can you just glance at the homepage and tell me if it looks okay? No login needed.
```
`.../graders/not-verify.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?verify"'
min: 0
max: 0
arm: both
weight: 3
---
```

`evals/verify/mint-and-probe-order/prompt.md` (process case):
```markdown
---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
tags: [verify, process]
---
Explain, step by step and in order, how you would confirm a new article page renders for the
logged-in owner. Name the exact commands.
```
`.../graders/order.md`:
```markdown
---
type: regex
pattern: mint-session\.mjs[\s\S]*probe\.mjs
weight: 2
---
```

**Further cases (W4, name / tags / prompt gist / graders):**

| Skill | Case | Tags | Prompt gist | Graders |
|---|---|---|---|---|
| pdf-pipeline | `classify-then-confirm` | process, release | fixture PDF with a DOI+abstract; "get this into the hub" | `tool_order`: `classify_pdf.py` (via `Bash`) before `Skill` (ingest-article); `regex` for "confidence" in trace |

### 4.2 Conversion

No prior `evals.json` exists for either skill (`find .claude/skills/pdf-pipeline .claude/skills/verify -iname 'evals*'` → empty). Nothing to convert.

### 4.3 Live triggers

Family (architecture §6.3): `{pdf-pipeline, ingest-article, ingest-slides, atomize-book, anthropic-skills:pdf, anthropic-skills:bullet-reconstruct}` — same PDF-front-door family as S17; this spec contributes pdf-pipeline's near-miss set.

| Query | Expected skill | Why it is a near-miss |
|---|---|---|
| "This PDF has both a DOI and a table of contents with 6 chapters, what do I do with it?" | pdf-pipeline (routes, likely asks) | genuinely ambiguous — tests the "ask a one-line question" branch, not silent misroute |
| "Just save this PDF somewhere, I'll deal with it later" | none (no Learn-hub destination) | tests the Not-for boundary against `anthropic-skills:pdf` |

### 4.4 Commands

- Smoke: `scripts/eval-project-skill.sh pdf-pipeline --smoke`; `scripts/eval-project-skill.sh verify --smoke` (I17, owner S12; CX-46).
- Release (W4 exit): `scripts/eval-project-skill.sh pdf-pipeline --release`; same for `verify` (CX-46).

## 5. Acceptance criteria

1. `grep -n "slide deck.*report/extract" .claude/skills/pdf-pipeline/references/routing.md` prints nothing (S18-W1-1).
2. `grep -c "ingest-slides" .claude/skills/pdf-pipeline/SKILL.md` → ≥3 (S18-W1-2).
3. `grep -n "no .node_modules., no .\.env\.local" .claude/skills/pdf-pipeline/SKILL.md` prints nothing (S18-W1-3).
4. `grep -n "200 KB\|200KB\|5.8 MB" .claude/skills/pdf-pipeline/SKILL.md .claude/skills/pdf-pipeline/references/*.md` prints nothing (S18-W1-4/5/6).
5. `grep -n "the .graph.\|card wall" .claude/skills/pdf-pipeline/SKILL.md .claude/skills/pdf-pipeline/references/surface-checklist.md` prints nothing (S18-W1-6).
6. `grep -n 'vault/\*/_topic.md' .claude/skills/pdf-pipeline/references/routing.md` prints nothing (S18-W1-7).
7. `python3 $MICKY_TOOLS_DIR/docs/plugin-rewrite/phase3/measure.py skill .claude/skills/pdf-pipeline/SKILL.md` reports `chars: 833`.
8. `python3 -m unittest .claude/skills/pdf-pipeline/scripts/test_classify_pdf.py` exits 0 (S18-W4-1).
9. `grep -n "/home/user/learn-hub\|/opt/pw-browsers" .claude/skills/verify/SKILL.md` prints nothing (S18-W4-2).
10. `npx vitest run scripts/lib/verify-mint.test.mjs scripts/lib/verify-probe.test.mjs` exits 0, and plain `npm test` (no extra args) collects both (S18-W4-3, CX-26).
11. `find evals/pdf-pipeline evals/verify -name prompt.md | wc -l` → 3 after W1, 7 after W4.
12. `claude plugin validate --strict` (or `check:skills` once S21 lands) reports no new frontmatter-key violations.

## 6. Trigger lock

| Phrase | Source | Disposition |
|---|---|---|
| "process this" / "add this to the hub" / "get this into the app" / "ingest this PDF" / "here's a PDF" / "put this in Learn" / "turn this PDF into notes" / "I uploaded a PDF" | pdf-pipeline desc | kept |
| "verify this in the real app" / "check this actually renders" / "screenshot this logged in" / "confirm this shows up for the owner" | verify desc | new (verify-2 had none) |

## 7. Risks and OD sensitivity

- **K-risk**: `classify_pdf.py`'s deterministic rules are a suggestion, not a gate — a wrong `route` value read uncritically would misroute silently. Mitigated: step 2's text explicitly says "confirm against the first few pages before committing," and the eval `classify-then-confirm` (§4.1 table) checks the tool runs BEFORE the routing `Skill` call, never instead of judgement.
- verify's new `## Gotchas` restates two CLAUDE.md items rather than linking them — deliberate, since verify is not named in I21's (S21, not yet written) explicit gotcha-map, and the content is short enough that duplication costs less than a broken cross-repo pointer if S21's map lands differently. Flagged in §8.
- No OD (OD1–OD14) changes this spec's fixes; none of the ten defects touches a decision point in §11 of the architecture.

## 8. Open questions

1. **ASSUMES** (I21, S21 not yet written): whether the browser-pane/chrome-devtools gotchas belong ONLY in verify's own `references`/body (this spec's choice) or also in a shared `.claude/rules/*.md` once S21's gotcha-map lands. No action needed now; if S21 adds a shared rule file, verify's own copy can be trimmed to a pointer without changing its behavior.
2. **ASSUMES** (I17, S12): `docs/rewrite/baseline.md`'s pdf-pipeline/verify rows are captured by S12 independently of this spec's W1 content, mirroring the same open question S17 raised for its own units — see S17 §8 item 1 for the shared reasoning.
3. **ARCH-CONFLICT: none found.** Every fix in §1.3 traces to architecture §3.6's pdf-pipeline/verify rows or an explicitly assigned defect (H32, H33, and the rest of pdf-pipeline-3..8/verify-1..2 named in Appendix A / §3.6).
4. Coordination: S18-W1-1/-2 (routes decks to `ingest-slides`) and S17-W1-8 (ingest-slides' own description/Not-for pass) should land in the same wave-1 merge, per S17 §1.3's ingest-slides-2 row.
