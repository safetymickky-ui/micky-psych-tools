# Spec S21: learn-hub CLAUDE.md diet, gotcha map, skill-lint and npm scripts

| Field | Value |
|---|---|
| Repos | learn-hub |
| Units (today → target) | `CLAUDE.md` (3,126 lines / 268,390 B) → ≤32 KB (OD11-b); new `docs/vault-format.md`; new `docs/gotchas-archive.md`; new `docs/rewrite/gotcha-map.md`; new `.claude/rules/*.md` (13 files); new `scripts/lib/skill-lint.mjs` + `src/lib/__tests__`-style vitest test; `package.json` scripts `test:py`, `check:skills` (+ the I22 registry) |
| Waves | W0 (skill-lint.mjs + tests; `test:py`; `check:skills`; then, right after W0 check e = yes, stage b (app gotchas + Pages → `.claude/rules`) inside a CLAUDE.md freeze — OQ9-a, OQ14-a), W1 (4 factual corrections), W4 stage a (pipeline gotchas + vault format out; size guard) |
| Owner decisions assumed | OD11-b (staged, a then b); owner answers OQ9-a, OQ14-a (all confirmed 2026-09-24) |
| Defects closed | 0 of 0 assigned (this spec has no inventory defect ids; it serves other specs — see digest) |
| Interfaces owned | I21, I22 |
| Interfaces consumed | I13 (owner S13), I16 (owner S11), I17 (owner S12), I19 (owner S08, not yet written) |
| Depends on specs | none for W0/W1 (this spec's own steps are self-contained); W4 stage-a steps are inputs INTO S13/S19/S16's own W4 gotcha-move steps (they depend on this spec's `gotcha-map.md`, not the reverse) |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| Path | Lines | Bytes | Est. tokens | Role |
|---|---|---|---|---|
| `learn-hub/CLAUDE.md` | 3,126 | 268,390 | 66,600 (measure.py) | always-loaded project instructions |
| `learn-hub/package.json` | — | — | — | scripts registry (I22) |
| `learn-hub/vitest.config.ts` | 24 | — | — | test include globs: `src/**/*.test.ts`, `src/**/*.test.tsx`, `scripts/**/*.test.mjs` |
| `.claude/skills/*/SKILL.md` (11 dirs) | — | — | — | skill-lint's target population |
| `.claude/rules/` | — | — | — | does not exist yet (`ls` fails) |
| `docs/vault-format.md` | — | — | — | does not exist yet |
| `docs/gotchas-archive.md` | — | — | — | does not exist yet |
| `docs/rewrite/gotcha-map.md` | — | — | — | does not exist yet (`docs/rewrite/` created by S10/S11 safety-net work, W0) |

CLAUDE.md top-level `## ` headings (`grep -n "^## " CLAUDE.md`), 14 total:
Live infrastructure (7), Core idea (40), Tech stack (54), Access model (71), Storage strategy
(101), Data model (108), Vault note format (206), Pages (360), Dashboard/tracking (799), Build
phases (806), **Gotchas (817)**, Testing (2997), Conventions (3084), Documentation upkeep (3107).

Section byte sizes (python, UTF-8, this session):

| Section | Lines | Bytes | Disposition (this spec) |
|---|---|---|---|
| Live infra | 7–39 | 2,478 | stays |
| Core idea | 40–53 | 695 | stays |
| Tech stack | 54–70 | 1,061 | stays |
| Access model | 71–100 | 2,291 | stays |
| Storage strategy | 101–107 | 398 | stays |
| Data model (Supabase) | 108–205 | 8,546 | stays (schema reference, not a gotcha, not "Pages") |
| **Vault note format** | 206–359 | 8,650 | **moves W4a → `docs/vault-format.md`** |
| **Pages** | 360–798 | 39,282 | **moves W4b → `.claude/rules/*.md`, by page (§2.3)** |
| Dashboard/tracking | 799–805 | 280 | stays |
| Build phases | 806–816 | 525 | stays |
| **Gotchas** | 817–2,996 | 194,666 | **moves W4a/b, 136 headings, full map §2.4/§8-file** |
| Testing | 2,997–3,083 | 6,313 | stays |
| Conventions | 3,084–3,106 | 1,650 | stays |
| Documentation upkeep | 3,107–3,126 | 1,233 | stays |

Sum of "stays" bytes: 25,470 B. Removed: 8,650 + 39,282 + 194,666 = 242,598 B. Remainder after
removal: 25,792 B. Budget for pointer text added back (short "moved to X" notes replacing Vault
note format, Pages and Gotchas) must stay ≤ 32,768 − 25,792 = **6,976 B** to hit OD11-b's ≤32 KB.

Gotcha heading count, verified this session:
`grep -n "^- \*\*" CLAUDE.md | awk -F: '$1>817 && $1<2997'` → **136** (matches architecture's
figure). Full list with line numbers extracted to
`/tmp/.../wf3/tmp/S21/gotchas-all.txt` (scratch; not part of the deliverable).

### 1.2 Descriptions

Not applicable — this spec owns no `SKILL.md`. `scripts/lib/skill-lint.mjs` is a script, not a
skill; it has no frontmatter of its own.

### 1.3 Defects

| id | sev | H# | evidence | problem | fix step | wave |
|---|---|---|---|---|---|---|
| — | — | — | — | none assigned (digest: `Count: 0`) | — | — |

Self-check: 0 of 0 assigned defect ids appear in this table — satisfied vacuously.

### 1.4 Other findings

- OBS (digest): "learn-hub/CLAUDE.md is 3,126 lines / 268,390 chars (~67k tokens). Its Gotchas
  section alone runs lines 817–2997, with 136 top-level gotchas, and 58 of those headings are
  pipeline/import topics." Re-measured this session: **136 confirmed exactly**; this spec's own
  classification (§2.4) assigns 66 headings to 8 skill/reference `gotchas.md` files (pipeline)
  and 70 to 13 `.claude/rules/*.md` files (app), which is close to but not identical to the OBS's
  58/78 estimate — recorded as a discrepancy, not corrected against it (§8).
- OBS (digest): "GOTCHA DRIFT BETWEEN CLAUDE.md AND THE SKILLS... atomize-book SKILL.md:1116-1117
  and 1265-1267 and ingest-article SKILL.md:314-316 still say [sync] re-embeds the whole vault
  from scratch." Not this spec's fix (owned by S19/ingest-article's spec) — noted because the W1
  CLAUDE.md correction "sync-vault as owner of the tail" (§3, S21-W1-4) is the CLAUDE.md-side
  half of the same drift.
- **NEW** (`figure_lib.py:966`): `VALID_DISPOSITIONS = ("mermaid", "redraw", "prose", "bake",
  "chart", "skip")` — six values. CLAUDE.md:2807-2808 states "(`mermaid|prose|bake|skip`)" — four,
  omitting `redraw` (used at CLAUDE.md:1574) and `chart` (used at :2850). This is the W1 "figure
  disposition list" correction the architecture names (§3.7 row); see §3, S21-W1-1.
- **NEW**: `package.json` (read this session) has no `test:py`, `check:skills`, `sync:preflight`,
  `audit:visual`, or `book:check-mermaid` entries yet — confirms all five are net-new (I22, §2.7).
  It does already have `book:source-cover`, `book:file-figures`, `book:upload-figures`,
  `similarity:detect`, `similarity:merge`, `changelog:check`, `revalidate`, `vectors:*`,
  `repetition:*`, `tags:*` — none of these are touched by this spec.
- **NEW**: no SKILL.md in `.claude/skills/*` uses `disable-model-invocation`, `metadata`,
  `allowed-tools`, or `argument-hint` today (`grep -rn` over all 11, this session) — confirms the
  frontmatter-key checks in skill-lint (§2.5) are validating against a currently-empty set on
  this repo; they will start mattering once other specs (S13, S19, S16, S20…) add those keys.
- **Already claimed by other written specs** (not duplicated here): S13 claims 6–7 headings for
  `sync-vault/references/gotchas.md` and already staged `sync:preflight` (S13-W1-5, a no-op
  placeholder pending this spec). S19 claims 23 headings for `atomize-book/references/gotchas.md`
  and staged `book:check-mermaid` (S19-W1-4, same pattern). S16 stages `audit:visual`
  (S16-W2-2) and states its animation/infographic gotchas "stay owned by their skills'
  `references/`, not duplicated here" — expecting this spec to create those files. S15 states
  digest-report's old gotcha restatements are **deleted, not moved** (no gotchas.md). S20
  deliberately does **not** create a `references/gotchas.md` for vault-atomizer, vault-vectors,
  vault-coverage or check-repetition, leaving that to "S21's later pass."

## 2. Target state

### 2.1 Location and tree (after W4 exit)

```
learn-hub/
  CLAUDE.md                          ≤32 KB (OD11-b)
  docs/
    vault-format.md                  NEW — moved verbatim from CLAUDE.md:206-359
    gotchas-archive.md               NEW — verbatim copy of every one of the 136 headings' text,
                                      as they read today, kept for history (never loaded)
    rewrite/
      gotcha-map.md                  NEW — the exit artefact: 136 rows, heading → destination
  .claude/
    rules/
      reader-focus-band.md           NEW, paths: (§2.4)
      reader-ui.md                   NEW
      diagrams-rendering.md          NEW
      visualizations.md              NEW
      books-library.md               NEW
      data-layer.md                  NEW
      platform-infra.md              NEW
      swipe-gestures.md              NEW
      ui-components.md               NEW
      explore-search.md              NEW
      color-similarity.md            NEW
      dev-workflow.md                NEW
      articles-feed.md               NEW
    skills/
      verify/references/gotchas.md          NEW (created by this spec, fallback — §8)
      check-repetition/references/gotchas.md NEW (created by this spec — S20 declined, §1.4)
      vault-coverage/references/gotchas.md   NEW (created by this spec — S20 declined, §1.4)
      ingest-article/references/gotchas.md   NEW (created by this spec — no other spec claims it)
      ingest-visual/references/gotchas.md    NEW (created by this spec — S16 expects, doesn't create)
      pk-plasma-animation/references/gotchas.md NEW (created by this spec, same reason)
      atomize-book/references/gotchas.md     created by S19-W4-8, NOT by this spec — this spec
                                              only supplies the map row this file is built from
      sync-vault/references/gotchas.md       created by S13-W4-1, NOT by this spec — same
  scripts/lib/
    skill-lint.mjs                   NEW (+ vitest test alongside it, `skill-lint.test.mjs`)
  package.json                       edited: `test:py`, `check:skills` added (I22)
```

### 2.2 Frontmatter

Not applicable — no `SKILL.md` owned by this spec.

### 2.3 Body outline

Not a skill body. The two moved sections restructure as follows.

**Vault note format (CLAUDE.md:206-359, 154 lines) → `docs/vault-format.md`**, verbatim, with a
one-line header `# Vault note format` prepended (the section had no H1 of its own since it was a
`##` inside CLAUDE.md) and a footer line: `Referenced by: sync-vault, atomize-book,
ingest-article, ingest-slides, ingest-visual, pk-plasma-animation.` CLAUDE.md keeps a 2-line
pointer at the old location:
`## Vault note format` / `Moved to docs/vault-format.md — read it before authoring any note,
topic, article, infographic or animation frontmatter.`

**Pages (CLAUDE.md:360-798, 439 lines) → split by page across `.claude/rules/*.md`.** Prose, not
flat headings like Gotchas, so the split follows its own numbered sub-headings
(`grep -n "^[0-9]\+[a-z]*\. \*\*"`) plus three unnumbered `**bold**`-led paragraphs at the end:

| Page (source lines) | Destination file |
|---|---|
| 1. Home (362-372) | `rules/books-library.md` |
| 1b. Books (373-451) | `rules/books-library.md` |
| 2. Stats (452-453) | `rules/data-layer.md` |
| 3. Topic view (454-460) | `rules/reader-ui.md` |
| 3b. Infographic viewer (461-464) | `rules/visualizations.md` |
| 4. Note/Lesson view (465-574) | `rules/reader-focus-band.md` (dominated by FocusBand/TOC/pill prose) |
| 5. Tag view (575-579) | `rules/books-library.md` |
| 6. Articles hub (580-613) | `rules/articles-feed.md` |
| 7. Visualizations (614-691) | `rules/visualizations.md` |
| 8. Hidden (692-700) | `rules/data-layer.md` |
| 9. Explore (701-741) | `rules/explore-search.md` |
| Desktop workspace shell (742-772) | `rules/ui-components.md` |
| Primary navigation (773-785) | `rules/ui-components.md` |
| ⌘K command palette (786-798) | `rules/explore-search.md` |

Each destination file gets a `## Pages: <name>` subsection holding that block **verbatim**.
CLAUDE.md keeps one `## Pages` section reduced to a 14-line index: page name, one clause, and
`→ .claude/rules/<file>.md`.

**Gotchas (CLAUDE.md:817-2996, 136 headings) → the map in §2.4.** CLAUDE.md keeps
`## Gotchas` reduced to: one sentence ("Hard-won traps, moved to owning files — read
`docs/rewrite/gotcha-map.md` for the index; Claude Code loads the file for the code you have
open via `.claude/rules/*.md` `paths:`, and the pipeline skills load their own
`references/gotchas.md` at the step that needs it") plus the same 13+8 file list as a bullet
list (no descriptions — the map has those).

### 2.4 References — the full gotcha map (136 of 136, none dropped)

Grouping key: **AB**=`atomize-book/references/gotchas.md` (built by S19-W4-8) · **SV**=
`sync-vault/references/gotchas.md` (built by S13-W4-1) · **IV**=`ingest-visual/references/
gotchas.md` (built here) · **PK**=`pk-plasma-animation/references/gotchas.md` (built here) ·
**IA**=`ingest-article/references/gotchas.md` (built here) · **VC**=`vault-coverage/references/
gotchas.md` (built here) · **CR**=`check-repetition/references/gotchas.md` (built here) ·
**VR**=`verify/references/gotchas.md` (built here) · **rules/\<file\>**=`.claude/rules/<file>.md`
(built here). This table IS the content written to `docs/rewrite/gotcha-map.md` (§3,
S21-W4a-1/W4b-1); line numbers are today's (before any text moves).

**Pipeline destinations (66 headings):**

| Dest | Line numbers (heading count) |
|---|---|
| AB (26) | 1298, 1374, 1403, 1414, 1592, 1620, 1636, 2408, 2472, 2480, 2490, 2524, 2534, 2551, 2558, 2567, 2599, 2697, 2711, 2732, 2745, 2803, 2817, 2865, 2882, 2906 |
| SV (20) | 869, 1165, 1178, 1344, 1654, 1669, 1685, 1705, 1722, 1743, 1769, 1781, 2243, 2263, 2268, 2425, 2450, 2615, 2630, 2950 |
| IV (6) | 1868, 1878, 1915, 1969, 2342, 2357 |
| PK (4) | 1930, 1937, 1944, 1950 |
| IA (2) | 2253, 2842 |
| VC (2) | 2680, 2897 |
| CR (4) | 2637, 2754, 2765, 2790 |
| VR (2) | 843, 856 |

**App/rules destinations (70 headings), with each rule file's `paths:` glob:**

| Rule file | `paths:` (frontmatter of the rule file) | Line numbers (count) |
|---|---|---|
| `reader-focus-band.md` | `src/components/focus-band.tsx`, `src/lib/focus-band.ts`, `src/lib/sentence-ranges.ts`, `src/lib/fab-position.ts`, `src/lib/focus-tap.ts`, `src/lib/reader-prefs*.ts`, `src/app/note/**` | 933, 959, 973, 999, 1011, 1030, 1042, 1053, 1067 (9) |
| `reader-ui.md` | `src/app/note/**`, `src/components/markdown.tsx`, `src/components/note-toc.tsx`, `src/app/globals.css`, `src/lib/toc.ts`, `src/lib/reading-progress.ts`, `src/lib/note-nav.ts`, `src/lib/related-notes.ts`, `src/components/related-notes.tsx`, `src/lib/note-image.ts` | 891, 1076, 1099, 1227, 1237, 1250, 1549, 1573, 2128, 2203, 2210, 2279, 2286, 2774 (14) |
| `diagrams-rendering.md` | `src/components/mermaid.tsx`, `src/components/diagram-figure.tsx`, `src/lib/markdown/**`, `scripts/lib/mermaid-render.mjs` | 1108, 1124, 1196, 1219 (4) |
| `visualizations.md` | `src/components/infographic/**`, `src/components/animation/**`, `src/app/infographic/**`, `src/app/animation/**`, `src/app/visualization/**`, `src/lib/infographic-*.ts`, `src/lib/animation-layout.ts`, `src/lib/visualization.ts` | 1265, 1833, 1982, 2066, 2293, 2320, 2331 (7) |
| `books-library.md` | `src/app/books/**`, `src/lib/book-category.ts`, `src/lib/topic-grouping.ts`, `src/lib/shelf-collapse.ts`, `src/lib/shelf-geometry.ts`, `src/lib/tag-groups.ts`, `src/app/tag/**` | 819, 1281, 1512, 1854, 2051 (5) |
| `data-layer.md` | `src/lib/db.ts`, `src/lib/db/**`, `supabase/migrations/**`, `src/lib/hidden.ts` | 1446, 1452, 1469, 1478, 1487, 2225, 2378, 2663, 2688 (9) |
| `platform-infra.md` | `src/proxy.ts`, `src/lib/request-context.ts`, `src/app/manifest.ts`, `public/sw.js`, `vercel.json`, `src/app/error.tsx`, `src/app/global-error.tsx`, `scripts/generate-icons.mjs` | 1432, 1438, 1797, 1812, 1823, 1827, 2101 (7) |
| `swipe-gestures.md` | `src/components/swipe-pager.tsx`, `src/components/note-swipe-pager.tsx`, `src/components/swipe-back.tsx`, `src/lib/swipe-math.ts`, `src/lib/swipe-dom.ts`, `src/lib/nav.ts` | 1997, 2134, 2156, 2175, 2190 (5) |
| `ui-components.md` | `src/components/ui/**`, `src/components/use-optimistic-action.ts`, `src/lib/radio-group.ts`, `src/components/workspace/**`, `src/components/bottom-nav.tsx`, `src/components/header-nav.tsx`, `src/lib/nav.ts`, `src/lib/workspace-tree.ts`, `src/lib/workspace-rail.ts` | 1526, 2014, 2230 (3) |
| `explore-search.md` | `src/app/explore/**`, `src/lib/explore*.ts`, `src/components/command-palette*.tsx`, `src/lib/fuzzy-search.ts`, `src/lib/palette-*.ts` | 1536, 2079 (2) |
| `color-similarity.md` | `src/lib/color.ts` | 2023, 2042 (2) |
| `dev-workflow.md` | `package.json`, `CHANGELOG.md`, `.githooks/**` | 1545, 2937, 2972 (3) |
| `articles-feed.md` | `src/app/article/**`, `src/app/articles/**`, `src/lib/article-*.ts`, `src/lib/feed-*.ts`, `src/components/article/**`, `src/components/feed-*.tsx` | (Pages-section content only, §2.3; no Gotcha heading assigned — none of the 136 headings is articles/feed-specific) (0) |

`data-layer.md` includes 2378 (`getInfographics`/`getAnimations` metadata-only caches — a `db.ts`
query concern, not a component-rendering one). Count check: rules total =
9+14+4+7+5+9+7+5+3+2+2+3+0 = **70**. Grand total 66 + 70 = **136**, matching §1.1's `wc -l` on
the extracted list; every line number above appears in that list exactly once (S21-W4a-1's "Done
when" names the exact re-check command).

### 2.5 Scripts

**`scripts/lib/skill-lint.mjs`** — vitest-invocable pure module + thin CLI wrapper.

- CLI: `node scripts/lib/skill-lint.mjs [--dir <path>] [--json]`. Default `--dir .claude/skills`.
- `--help`: prints usage, exits 0, no side effects.
- Input: reads every `<dir>/*/SKILL.md`.
- Checks (the section-8 subset that applies to a bare `.claude/skills` frontmatter):
  1. YAML frontmatter parses strict (js-yaml) — fail.
  2. Frontmatter key whitelist per I20 (owner S08); an unknown key fails. Not restated here
     (ASSUMES, §2.7).
  3. `name` == the skill's directory name — fail.
  4. `description` ≤1,024 chars hard (fail), ≤600 chars warn.
  5. No Windows paths (`C:\`, backslash separators, bare `/home/user` outside the declared
     exception) — fail.
  6. Every `references/`/`scripts/`/`assets/`/`examples/` file the body links resolves on disk —
     fail if missing.
  7. dmi **alias-skill** shape (I20/OD9), scoped to alias skills only (CX-52 — not every dmi
     skill: `vault-atomizer`/`vault-vectors`/`vault-coverage`/`check-repetition`/
     `pk-plasma-animation` are dmi but are full skills, not thin aliases, and must not warn here):
     a skill whose body is a single `Invoke <target> with: $ARGUMENTS` line gets
     `disable-model-invocation: true` + body ≤10 lines — warn if either half is missing.
  8. No leftover `{{` outside `templates/` — fail.
  9. **Trigger lock and ratchet (I17, owner S12)**: imports `scripts/lib/rewrite-gate.mjs`'s
     exported functions (CX-19 — not a re-parse of `triggers.lock.json`/`ratchet.json`, so the two
     implementations cannot drift) to check whether a locked phrase is missing from the current
     description (fail) or a check is ratcheted to warn for its listed paths. When S12's library
     is absent (before S12-W0-2 lands), this check is skipped, not failed (§8).
- Output: JSON on stdout (`{"ok": bool, "checked": n, "failures": [...], "warnings": [...]}`),
  human summary on stderr. Exit 0 = all fail-level checks pass (warnings do not fail); exit 1 =
  at least one fail-level check failed; exit 2 = a checked directory does not exist or no
  SKILL.md found under `--dir`.
- Tests: `scripts/lib/skill-lint.test.mjs` (vitest; picked up by the existing
  `scripts/**/*.test.mjs` glob, `vitest.config.ts:16` — no config change needed). Cases: valid
  skill passes; invalid YAML fails; `name`/dir mismatch fails; description at 1,025/601–1,024/≤600
  chars (fail/warn/clean); a Windows path fails; a dangling `references/` link fails; a dmi skill
  with an 11-line body warns; a stray `{{PLACEHOLDER}}` fails; a locked trigger phrase missing
  from the description fails when `triggers.lock.json` exists, is skipped when absent.

Other new scripts (critique F9, C2-05, C2-08, C2-20): `scripts/test-py.mjs` and `scripts/check-skills.mjs` (the two npm entries above, each with a vitest test of its pure part: interpreter choice, dir walk, `Ran 0 tests` detection); `.githooks/pre-commit` (S21-W0-3); `scripts/lib/move-blocks.mjs` + `scripts/move-blocks.mjs` (S21-W4a-4).

### 2.6 Handoffs

Not applicable — this spec owns no skill that hands off to another.

### 2.7 Interfaces

**I21 (owned here).** learn-hub gotcha destinations.

- `docs/rewrite/gotcha-map.md`: the §2.4 table, verbatim, plus a header "136 of 136 headings
  mapped; 0 dropped" and the generation date.
- Per-skill `references/gotchas.md`: one `##` per moved heading, original CLAUDE.md text copied
  **verbatim**, each preceded by `<!-- moved from learn-hub/CLAUDE.md:<line>, <date> -->`.
- `docs/vault-format.md`: §2.3.
- `.claude/rules/*.md`: YAML frontmatter `paths: [...]` (§2.4's table) then the moved Gotcha
  headings (verbatim) under `## Gotchas` and the moved Pages content (verbatim, §2.3) under
  `## Pages`.
- `docs/gotchas-archive.md`: all 136 headings' text, verbatim, in original line order, noted
  "superseded by the files docs/rewrite/gotcha-map.md names — never loaded by any skill/rule."

**I22 (owned here).** The single registry of every `package.json` `scripts` entry added or
changed by any spec in this rewrite, so no two specs' edits collide.

| Script | Command | Added by | Status as of this spec |
|---|---|---|---|
| `sync:preflight` | `node scripts/lib/sync-preflight.mjs` | S13 (S13-W1-5) | already staged by S13; this spec's own W0/W1 steps treat it as present and do not re-add it |
| `audit:visual` | `node scripts/audit-visual.mjs` | S16 (S16-W2-2) | already staged by S16; not re-added here |
| `book:check-mermaid` | `node scripts/check-mermaid.mjs` | S19 (S19-W1-4) | already staged by S19; not re-added here |
| `test:py` | `node scripts/test-py.mjs` — walks every `.claude/skills/*/scripts` dir that holds `test_*.py` and runs `<python> -m unittest discover -s <dir> -p 'test_*.py'` in each, where `<python>` is the first of `python3`, `python`, `py -3` that runs; exits 1 on a failing suite or on a dir that reports `Ran 0 tests` (CX-26 — every skill's own `scripts/` dir, incl. `pdf-pipeline/scripts/test_classify_pdf.py`, S18-W4-1; a node script, not a bash `for` loop, because npm runs scripts with cmd.exe on Windows — critique F9) | **this spec** (W0) | new |
| `check:skills` | `node scripts/check-skills.mjs` — runs `node scripts/lib/skill-lint.mjs --dir .claude/skills`, then `claude plugin validate --strict .claude` (the `.claude/skills` form exits 1, "No manifest found in directory" — measured, critique C2-05), then `claude plugin validate --strict plugins/learn-hub-session` when that dir exists; exits non-zero on the first failure. `claude plugin validate` does not check frontmatter YAML or the 1,024-char cap; skill-lint does (critique F22) | **this spec** (W0) | new |

Any spec adding a sixth entry updates this table in its own file's §2.7 (never edits this one —
"never edit another spec's file"); at assembly time (workflow step 5) the owner reconciles all
`package.json` edits against this row set for collisions. No collision found among the specs read
this session (S11, S12, S13, S15, S16, S19, S20).

**I13 (consumed, owner S13).** ASSUMES: S13's sync-vault rewrite defines the `sync:preflight` →
`sync:apply` (background, logged) → revalidate → verify tail; this spec's W1 CLAUDE.md correction
(S21-W1-4) states only that "`sync-vault` is the sole owner of this procedure" and does not
restate the procedure's steps — settled by reading S13's shipped SKILL.md once it exists; if S13's
final command names differ from `sync:preflight`/`sync:apply`, this spec's one sentence still
holds (it names no command).

**I16 (consumed, owner S11).** ASSUMES: none of this spec's file moves interact with
`CLAUDE_CODE_PLUGIN_DIRS` or the delivery log — `.claude/rules/*.md` load by path match inside an
existing session (W0 check e, owned by S11), not by plugin delivery. If W0 check (e) reports "no"
(rules don't load in multi-repo sessions), this spec's W4b work still creates the files (they are
useful in single-repo learn-hub sessions and as documentation) but the OD11 fallback
(`docs/gotchas/*.md` + a CLAUDE.md pointer index) replaces `.claude/rules/*.md` as the actual
runtime destination — see §7, §8.

**I17 (consumed, owner S12).** CLOSED for the schema-drift risk (CX-19): `skill-lint.mjs` imports
`scripts/lib/rewrite-gate.mjs`'s exported functions directly rather than re-parsing
`triggers.lock.json`/`ratchet.json` itself, so a schema change in S12's files cannot silently
desync from what this spec's check 9 expects. ASSUMES the case-tag vocabulary
(`smoke|trigger|negative|output|release`) is irrelevant to skill-lint (it lints frontmatter and
files, not eval cases) — no case tags are read or written by this spec's script.

**I19 (consumed, owner S08, spec not yet written).** ASSUMES: `plugin-creator/scripts/validate.py
--repo ../learn-hub` will eventually run a superset of what `check:skills` runs today, and that
`check:skills` stays as the fast, no-micky-checkout-required path (architecture §8: "learn-hub
runs its own small vitest skill-lint... so `npm test` never depends on the micky checkout").
Settled by reading S08 once it exists; no conflict expected since I19's owner is explicitly told
(architecture §8) that this subset exists independently.

## 3. Change steps

### Wave W0

**S21-W0-1** — Write `scripts/lib/skill-lint.mjs` and `scripts/lib/skill-lint.test.mjs`.
- Repo: learn-hub · depends on: none
- Files: create `scripts/lib/skill-lint.mjs`, `scripts/lib/skill-lint.test.mjs`
- Change: implement per §2.5. The frontmatter key whitelist (check 2) is read from I20; until S08
  exists, hardcode the currently-known baseline (`name`, `description` — the only two keys any
  learn-hub skill uses today, §1.4). Check 9 imports `scripts/lib/rewrite-gate.mjs`'s exported
  functions (CX-19); until S12-W0-2 creates that file, check 9 is skipped, not failed (§8 tracks
  wiring the real import once S12 lands).
- Commands: `npx vitest run scripts/lib/skill-lint.test.mjs`
- Done when: the test file passes; `node scripts/lib/skill-lint.mjs --dir .claude/skills --json`
  exits 1 and its `failures` list exactly today's known violations — YAML parse failures in
  concept-animation, ingest-animation, ingest-article, ingest-infographic, and descriptions over
  1,024 chars (atomize-book 1,075, ingest-slides 1,150, and ingest-article if its YAML parses) —
  measured by critique C2-06; §1.4's grep missed them. S21-W0-2 seeds them into the ratchet.
- Rollback: `git rm scripts/lib/skill-lint.mjs scripts/lib/skill-lint.test.mjs`.

**S21-W0-2** — Add `test:py` and `check:skills` to `package.json`; seed the learn-hub ratchet.
- Repo: learn-hub · depends on: S21-W0-1, S12-W0-2 (`rewrite-gate.mjs` must exist to seed the ratchet)
- Files: edit `package.json`; create `scripts/test-py.mjs`, `scripts/check-skills.mjs` and their vitest tests; edit `docs/rewrite/ratchet.json`; edit `README.md` (two script-table rows, learn-hub Documentation upkeep)
- Change: seed the ratchet with today's skill-lint failures — `node scripts/lib/skill-lint.mjs --dir .claude/skills --json > /tmp/skill-lint.json`, then `node scripts/rewrite-gate.mjs ratchet seed --check <id> --from /tmp/skill-lint.json --write` per failing check id (critique C2-06; S17-W1-2, S17-W1-8, S19-W1-8, S05-W1-1, S16-W1-1 and S16-W1-2 close these entries). Add the two lines from §2.7's I22 table under the existing `"scripts"` block, after
  `"test:watch"` — `test:py` is the per-skill-dir walk (CX-26), not a single fixed path. Read
  `package.json` immediately before editing (per the workflow's read-before-write rule) in case
  S13/S16/S19's steps have already landed `sync:preflight` / `audit:visual` / `book:check-mermaid`
  — if so, leave those three untouched and only add the two new ones.
- Commands: `npm run test:py` directly against every `.claude/skills/*/scripts/test_*.py` file
  found today (currently only atomize-book's 4; `pdf-pipeline/scripts/test_classify_pdf.py`
  lands later, S18-W4-1, and the same walk picks it up with no further edit here). `npm run
  check:skills`.
- Done when: `npm run test:py` runs every skill's own unittest suite and reports its pass/fail
  count (not asserted green here — that is each skill's own spec's concern, e.g. S19 for
  atomize-book); `npm run check:skills` exits 0 after the seed (skill-lint reports the seeded violations as warnings;
  `claude plugin validate --strict .claude` exits 0), and `node scripts/rewrite-gate.mjs ratchet
  verify` exits 0.
- Rollback: revert the `package.json` diff.

**S21-W0-3 (new, critique F8, C2-20)** — learn-hub `.githooks/pre-commit`.
- Repo: learn-hub · depends on: S21-W0-2, S12-W0-2
- Files: create `.githooks/pre-commit` (a two-line shell wrapper: `#!/usr/bin/env sh` and `exec node scripts/pre-commit.mjs`) and `scripts/pre-commit.mjs` + a vitest test of its file filter.
- Change: when a staged path is under `.claude/skills/` or is `CLAUDE.md`, run `node scripts/lib/skill-lint.mjs`, `node scripts/rewrite-gate.mjs ratchet verify` and `node scripts/rewrite-gate.mjs triggers verify`; block the commit on a failure. Other commits pass untouched. `.claude/hooks/session-start.sh` already sets `core.hooksPath .githooks` (the `post-merge` hook lives there), so every session gets it; architecture §8 requires a pre-commit in both repos.
- Commands: `node scripts/pre-commit.mjs` on a clean tree; a scratch commit that removes a locked trigger phrase from a skill description (then `git reset`).
- Done when: the clean run exits 0; the scratch commit is blocked; `npx vitest run scripts/pre-commit.test.mjs` passes.
- Rollback: `git revert <this commit>`.

**S21-W0-4 (new, OQ9-a)** — Start the CLAUDE.md freeze for stage b.
- Repo: learn-hub · depends on: S11-W0-7 (W0 check e = yes; OQ14-a runs stage b right after it), S21-W0-3
- Files: create `docs/gotchas-inbox.md`; edit `CLAUDE.md` (one line right under the `## Gotchas (hard-won)` heading and one right under `## Pages`, both outside every gotcha block)
- Change: `docs/gotchas-inbox.md` gets a `# Gotchas inbox` header and one sentence: "Frozen window S21-W0-4 … S21-W0-5 (OQ9-a): add a new learn-hub gotcha here as a `- **…**` bullet; it moves to its destination when the window ends." Each CLAUDE.md line reads: "Frozen for the plugin rewrite (OQ9-a, from <date>): do not edit this section; add a new gotcha to `docs/gotchas-inbox.md`."
- Commands: `grep -c 'Frozen for the plugin rewrite' CLAUDE.md`; `test -f docs/gotchas-inbox.md`
- Done when: the grep prints 2; the file exists; the commit is merged to learn-hub master before S21-W4a-1 starts, because other sessions read master (OQ7-a).
- Rollback: `git revert <this commit>`.

**S21-W0-5 (new, OQ9-a)** — End the freeze.
- Repo: learn-hub · depends on: S21-W4b-1
- Files: delete `docs/gotchas-inbox.md`; edit `CLAUDE.md` and each `.claude/rules/*.md` file an inbox entry goes to
- Change: move each entry of `docs/gotchas-inbox.md`, verbatim: an app-area entry to the `.claude/rules/*.md` file that §2.4's area rules name; a pipeline-area entry under `## Gotchas` in CLAUDE.md, where S21-W4a-3 maps it as a `new` row in W4. Delete the inbox file and every freeze line S21-W0-4 added that S21-W4b-1 did not already remove.
- Commands: `grep -c 'Frozen for the plugin rewrite' CLAUDE.md`; `test ! -e docs/gotchas-inbox.md`; `node scripts/move-blocks.mjs --check`
- Done when: the grep prints 0; the inbox file is gone; `--check` exits 0.
- Rollback: `git revert <this commit>`.

### Wave W1 — CLAUDE.md factual corrections

**S21-W1-1** — Fix the figure disposition list.
- Repo: learn-hub · depends on: none
- Files: edit `CLAUDE.md`
- Change: at CLAUDE.md:2807-2808, replace
  `` (`mermaid|prose|bake|skip`) `` with `` (`mermaid|redraw|prose|bake|chart|skip` — chart is
  article-only, see below) ``. Evidence: `figure_lib.py:966`
  `VALID_DISPOSITIONS = ("mermaid", "redraw", "prose", "bake", "chart", "skip")` (§1.4).
- Commands: `grep -n "mermaid|redraw|prose|bake|chart|skip" CLAUDE.md`
- Done when: the grep above returns the edited line; `grep -c "mermaid|prose|bake|skip\"" CLAUDE.md`
  returns 0 (old string gone).
- Rollback: revert the one-line diff.

**S21-W1-4** — State sync-vault's tail ownership explicitly; carry S11's delivery-line sentence (CX-49 item 3).
- Repo: learn-hub · depends on: none
- Files: edit `CLAUDE.md`
- Change: (1) in the "Core idea" section, after the flow diagram (CLAUDE.md:43-51), add one
  sentence: `The sync-vault skill is the sole owner of the sync → revalidate → verify → purge
  tail; no other skill restates its procedure — see its own SKILL.md.` This is the CLAUDE.md-side
  half of closing the "8 restatements today, 4 contradictory apply rules" ownership gap
  (architecture §2.4 ownership-map row); the restating skills themselves (digest-report,
  ingest-article, vault-atomizer, …) are fixed by their own specs (S13, S15, S19, S20), not here.
  (2) In the "Claude Code cloud environment" paragraph (Live infrastructure section), add S11's
  §2.6 item 3 sentence verbatim (CX-49): `Delivery and VM-tooling variables and the setup script:
  docs/cloud-env-setup.md §3C; current values in micky-psych-tools docs/rewrite/delivery-log.md.`
- Commands: `grep -n "sole owner of the sync" CLAUDE.md`; `grep -n "docs/cloud-env-setup.md §3C" CLAUDE.md`
- Done when: both greps above return 1 line each.
- Rollback: revert the one-line diff.

### Wave W4, stage a — pipeline gotchas + vault format out (S21-W4a-1 and S21-W4a-4 run before W1 with stage b — OQ14-a; ids kept)

**S21-W4a-1** — Write `docs/rewrite/gotcha-map.md`.
- Repo: learn-hub · depends on: S21-W0-1, S21-W0-4 (the freeze is on master). Runs right after W0 check e = yes, before W1 (OQ14-a).
- Files: create `docs/rewrite/gotcha-map.md`
- Change: write the table from §2.4, keyed by heading text (the bold first sentence of each
  `- **…**` gotcha bullet) with the line number as a second column, plus the header line stated
  there and the base commit sha (the frozen `CLAUDE.md`). Build it from the live `CLAUDE.md` at the start of the frozen window (S21-W0-4; OQ9-a, OQ14-a), not from
  the 2026-09-24 line numbers: other sessions add gotchas every week. A heading added since
  2026-09-24 gets a destination by §2.4's area rules and is marked `new` (critique C2-09).
- Commands: `wc -l docs/rewrite/gotcha-map.md`; `grep -c '^- \*\*' CLAUDE.md` inside `## Gotchas`.
- Done when: every gotcha heading in the frozen `CLAUDE.md` appears exactly once in the map
  (136 plus the `new` rows), and every row's heading text still occurs exactly once in `CLAUDE.md`.
- Rollback: `git rm docs/rewrite/gotcha-map.md`.

**S21-W4a-4 (new, critique C2-08)** — Write the block mover.
- Repo: learn-hub · depends on: S21-W4a-1 (runs before W1, OQ14-a)
- Files: create `scripts/lib/move-blocks.mjs` (pure planner), `scripts/lib/move-blocks.test.mjs`, `scripts/move-blocks.mjs` (CLI).
- Change: a block is a gotcha heading line (`- **…`) through the line before the next heading or `## ` section. `--map <file> [--dest <key>] --write` cuts every block the map assigns to `<key>` (all keys when omitted) from `CLAUDE.md` and appends it, verbatim, under `## <heading text>` plus the `<!-- CLAUDE.md:<line> -->` provenance comment, to the destination file I21 names. `--archive <out>` writes every mapped block in original order without cutting. `--check` compares the sha256 of the sorted blocks of each row's base `CLAUDE.md` (`git show <base sha>:CLAUDE.md`; the map's base sha unless the row names its own — S21-W4a-3 gives the rows still in CLAUDE.md the W4-entry sha, OQ14-a) with the blocks found across `CLAUDE.md` and every destination: exit 0 only when each block occurs exactly once, byte-identical. `--check-archive` does the same for the archive. Dry run by default.
- Commands: `npx vitest run scripts/lib/move-blocks.test.mjs`; `node scripts/move-blocks.mjs --map docs/rewrite/gotcha-map.md` (dry run).
- Done when: the tests pass, including a case where one changed character inside a moved block makes `--check` exit 1 and a case with two base shas; the dry run lists every map row with its block's line range.
- Rollback: `git revert <this commit>`.

**S21-W4a-3** — Write `docs/gotchas-archive.md` (archive before any stage-a deletion — CX-28; OQ14-a moved stage b's deletions before W1);
fix the pk-plasma-animation location line (the edit noted in §8).
- Repo: learn-hub · depends on: S21-W4a-4 (the mover writes the archive, critique C2-08), S21-W4a-1 (the map — this step no longer depends on S21-W4a-2;
  CX-28 moves the archive ahead of the first deletion, closing the transient-unrecoverable window
  §7 used to describe: archiving right after the map, before ANY text moves, captures all 136
  headings in one shot — including AB's 26 and SV's 20, which S19-W4-8/S13-W4-1 delete only later
  — so there is no longer a reason to archive after a partial deletion); S16-W2-6 (CX-34 —
  pk-plasma-animation must already be at `.claude/skills/pk-plasma-animation` for the line fix)
- Files: create `docs/gotchas-archive.md`; edit `CLAUDE.md:355` and `docs/rewrite/gotcha-map.md` (base shas, `new` rows)
- Change: `docs/gotchas-archive.md` per §2.7 (I21) — every mapped heading, verbatim, written by
  `node scripts/move-blocks.mjs --map docs/rewrite/gotcha-map.md --archive docs/gotchas-archive.md`
  from each row's base commit, before S21-W4a-2's or any other stage-a deletion. First (OQ14-a): give
  every row still in CLAUDE.md the W4-entry sha as its base (a pipeline block may have changed since
  S21-W4a-1, e.g. at S21-W1-1) and add a `new` row for any pipeline heading added since; the rows
  S21-W4b-1 moved before W1 keep the map's base sha, so the archive still holds their frozen text (a
  script copy, not a hand copy, so the archive cannot carry a hand-made error; critique C2-08). CLAUDE.md's
  pk-plasma line: replace
  `` the `pk-plasma-animation` plugin (`plugins/pk-plasma-animation/`, `/pk-animation <drug>`) ``
  with `` the `pk-plasma-animation` skill (`.claude/skills/pk-plasma-animation`, `/pk-animation
  <drug>`) ``.
- Commands: `ls .claude/skills/pk-plasma-animation/SKILL.md` (precondition check); `grep -n
  "pk-plasma-animation.*plugin" CLAUDE.md` (should be empty after the edit); `grep -c '^## ' docs/gotchas-archive.md` → the map's row count; `node scripts/move-blocks.mjs --check-archive` exits 0.
- Done when: both greps above match expectations, and the archive holds exactly one block per map row, byte-identical to its row's base commit.
- Rollback: revert the diffs; the archive file is additive and safe to leave.

**S21-W4a-2** — Move `Vault note format` to `docs/vault-format.md`; move the pipeline-destined
66 gotcha headings out of CLAUDE.md into their owning skills' `references/gotchas.md` (creating
the 6 this spec owns: IV, PK, IA, VC, CR, VR; **not** touching AB/SV's files, which S19-W4-8 and
S13-W4-1 create independently, each reading this step's `gotcha-map.md`).
- Repo: learn-hub · depends on: S21-W4a-3 (CX-28 — the archive must land first, so a delete here
  can never outrun the backstop that recovers it)
- Files: create `docs/vault-format.md`; create `.claude/skills/{verify,check-repetition,
  vault-coverage,ingest-article,ingest-visual,pk-plasma-animation}/references/gotchas.md`; edit
  `CLAUDE.md` (delete the moved text, insert the two pointers per §2.3)
- Change: verbatim moves per §2.3 (vault format) and §2.4/I21 (gotcha text, one `##` per heading
  with the HTML-comment provenance line), made by `node scripts/move-blocks.mjs --map
  docs/rewrite/gotcha-map.md --dest <IV|PK|IA|VC|CR|VR> --write` (S21-W4a-4), never by hand
  (critique C2-08). Precondition: `ls .claude/skills/ingest-visual/SKILL.md`
  and `.claude/skills/pk-plasma-animation/SKILL.md` exist (both land at S16's W2 exit, which
  precedes W4 in the standard wave order).
- Commands: `grep -c "^- \*\*" CLAUDE.md` before and after — drops by 20 (IV+PK+IA+VC+CR+VR only;
  AB's 26 and SV's 20 stay in CLAUDE.md until S19-W4-8 / S13-W4-1 delete them, each after reading
  this step's map).
- Done when: `node scripts/move-blocks.mjs --check` exits 0; `ls .claude/skills/verify/references/gotchas.md` (and the other 5) succeed; each
  contains exactly its assigned heading count from the map (§2.4 today: 2, 4, 2, 2, 6, 4); `docs/vault-format.md`
  exists and CLAUDE.md:206 now reads the 2-line pointer.
- Rollback: `git revert` the commit; the moved text is recoverable from `docs/gotchas-archive.md`
  (S21-W4a-3, already written before this step ran) regardless.

**S21-W4a-5 (new, OQ14-a)** — Size guard after stage a.
- Repo: learn-hub · depends on: S21-W4a-2, S13-W4-1, S19-W4-8 (every pipeline row has moved)
- Files: edit `scripts/lib/skill-lint.mjs`, `scripts/lib/skill-lint.test.mjs`, `CLAUDE.md` (the `## Documentation upkeep` line)
- Change: add skill-lint check 10: `CLAUDE.md` over 32,768 bytes fails (with a vitest case), so the target cannot erode. Set the upkeep line to its final text: "New trap → add it to the file `docs/rewrite/gotcha-map.md` names for its area; CLAUDE.md keeps pointers only." Both moved here from S21-W4b-1: stage b runs before W1, when CLAUDE.md still holds the 66 pipeline gotchas and the vault format (OQ14-a).
- Commands: `python3 $MICKY_TOOLS_DIR/docs/plugin-rewrite/phase3/measure.py file CLAUDE.md`; `npm run check:skills`; `node scripts/move-blocks.mjs --check`
- Done when: `wc -c CLAUDE.md` ≤ 32,768; `grep -c '^- \*\*' CLAUDE.md` inside `## Gotchas` → 0; `npm run check:skills` passes with check 10; `--check` exits 0 (the W4 exit gate's own check, §4.4, §5).
- Rollback: `git revert <this commit>`.

### Wave W4, stage b — app gotchas + Pages → `.claude/rules/*.md` (runs right after W0 check e = yes, before W1 — OQ14-a; id kept)

**S21-W4b-1** — Create the 13 `.claude/rules/*.md` files and move the 70 app gotcha headings plus
the Pages content into them; reduce CLAUDE.md's `## Gotchas` and `## Pages` sections to indexes.
- Repo: learn-hub · depends on: S21-W4a-1, S21-W4a-4, S21-W0-4. OQ14-a: runs right after W0 check
  e = yes, before W1, inside the OQ9-a freeze. The 66 pipeline headings stay under `## Gotchas`
  until stage a moves them in W4 (S21-W4a-2, S13-W4-1, S19-W4-8). If check e = no, this step waits
  for W4, runs after those three steps and targets `docs/gotchas/` (§7).
- Files: create the 13 files listed in §2.1/§2.4; edit `CLAUDE.md`
- Change: for each rule file, write the `paths:` frontmatter (§2.4's table) then the assigned
  Gotcha headings (verbatim, `## Gotchas` subsection) and the assigned Pages content (verbatim,
  §2.3's table, `## Pages` subsection where applicable — only `books-library.md`, `data-layer.md`,
  `reader-ui.md`, `visualizations.md`, `reader-focus-band.md`, `explore-search.md`,
  `ui-components.md` receive a Pages subsection; `diagrams-rendering.md`, `platform-infra.md`,
  `swipe-gestures.md`, `color-similarity.md`, `dev-workflow.md`, `articles-feed.md` receive Pages
  content only where §2.3's table names them — `articles-feed.md` gets Pages content (item 6) but
  no Gotcha headings, per §2.4's note). CLAUDE.md's `## Gotchas` becomes the short pointer text
  from §2.3; `## Pages` becomes the 14-row index from §2.3; the `## Gotchas` pointer text sits above the 66
  pipeline blocks until W4. Gotcha blocks move with
  `node scripts/move-blocks.mjs --map docs/rewrite/gotcha-map.md --dest rules --write` (critique C2-08).
  Same commit (critique C2-09): replace the "New trap discovered → add it to Gotchas" line in
  `## Documentation upkeep` with "New trap → add it to the file `docs/rewrite/gotcha-map.md` names
  for its area; until the W4 moves, a pipeline-area trap goes under `## Gotchas` here." S21-W4a-5
  sets the final wording and adds skill-lint check 10: after this step CLAUDE.md is still about
  135 KB (measured 2026-09-24: 268,390 bytes, of which about 39 KB is Pages and 94 KB app
  gotchas), so the 32,768-byte check waits for stage a (OQ14-a).
- Commands: `node scripts/move-blocks.mjs --check`; `ls .claude/rules/*.md | wc -l`
- Done when: `grep -c "^- \*\*" CLAUDE.md` inside `## Gotchas` → the pipeline rows only (66, plus
  any `new` pipeline row), which stage a moves in W4; `ls .claude/rules/*.md | wc -l` → 13;
  `node scripts/move-blocks.mjs --check` exits 0: every mapped block from the frozen `CLAUDE.md`
  exists exactly once across CLAUDE.md and the destinations, byte-identical (replaces the
  first-8-words grep, which a changed number or a dropped sentence inside a block would pass;
  critique C2-08); `npm run check:skills` passes.
- Rollback: `git revert`; the map commit (S21-W4a-1) holds every moved block's text, and
  `docs/gotchas-archive.md` (S21-W4a-3, W4) archives it from there (OQ14-a).

**Owner action (OWNER)** — none required for this spec's own steps; all four waves are executable
without a human decision beyond the already-assumed OD11-b.

## 4. Evals

### 4.1 Cases

Not applicable in the `claude plugin eval` sense — this spec owns no `SKILL.md`. The equivalent
verification is `scripts/lib/skill-lint.test.mjs` (vitest unit tests, listed in full in §2.5) and
the exactly-once grep in S21-W4b-1's "Done when." No `evals/<skill>/<case>/` directory is created
by this spec.

### 4.2 Conversion

Not applicable — no `evals.json` case in the mined 118 names a unit this spec owns (this spec's
units did not exist as skills/commands before this rewrite).

### 4.3 Live triggers

Not applicable — `scripts/lib/skill-lint.mjs` and `check:skills` are not model-invoked; nothing
here has a description Claude routes to. No family membership, no near-miss queries.

### 4.4 Commands

- Smoke: `npx vitest run scripts/lib/skill-lint.test.mjs` (W0); `npm run check:skills` (every
  wave exit, per the standard exit gates in architecture §10); `npm run test:py` (every wave
  exit).
- Release: `python3 $MICKY_TOOLS_DIR/docs/plugin-rewrite/phase3/measure.py file CLAUDE.md` ≤ 32,768 bytes (W4 exit, S21-W4a-5); the exactly-once
  grep script named in S21-W4a-5's "Done when" (W4 exit, and again at the overall migration's W5
  exit per architecture §10 W4's "A grep shows every mapped heading exists exactly once in its
  destination").

## 5. Acceptance criteria

1. `grep -n "^## " CLAUDE.md | wc -l` reports 14 at every wave (no section header is deleted,
   only bodies shrink/move) until W4b, after which `## Vault note format`, `## Pages` and
   `## Gotchas` are pointer-only.
2. `wc -c CLAUDE.md` ≤ 32,768 after S21-W4a-5 (OD11-b; OQ14-a).
3. `wc -l docs/rewrite/gotcha-map.md` — table row count (excluding header rows) sums to 136
   across the two grouped tables in §2.4 (66 + 70).
4. `ls docs/vault-format.md docs/gotchas-archive.md` both succeed after W4a.
5. `ls .claude/rules/*.md | wc -l` = 13 after W4b.
6. `ls .claude/skills/{verify,check-repetition,vault-coverage,ingest-article,ingest-visual,
   pk-plasma-animation}/references/gotchas.md | wc -l` = 6 after W4a.
7. `npm run test:py` and `npm run check:skills` both exit with a code that is 0 or a documented
   non-zero from one of the discovered skills' own suites (this spec does not assert any
   individual skill's tests are green — that is each skill's own spec's concern, e.g. S19 for
   atomize-book, S18 for pdf-pipeline's `classify_pdf.py`).
8. `npx vitest run scripts/lib/skill-lint.test.mjs` exits 0 after S21-W0-1.
9. `grep -c "mermaid|prose|bake|skip\"" CLAUDE.md` = 0 after S21-W1-1 (old disposition string
   gone).
10. `grep -n "sole owner of the sync" CLAUDE.md` returns exactly 1 line after S21-W1-4; `grep -n
    "docs/cloud-env-setup.md §3C" CLAUDE.md` returns exactly 1 line after S21-W1-4 (CX-49).
11. Every one of the 136 line numbers in §2.4's two tables is distinct and their union has 136
    members (self-check performed during drafting; re-verifiable with the sort/uniq command in
    S21-W4a-1's "Done when").

## 6. Trigger lock

Not applicable — this spec's units carry no descriptions Claude routes to.

## 7. Risks and OD sensitivity

- **K11** (knowledge loss on redistribution) is this spec's primary risk. Mitigation: verbatim
  moves only (no paraphrase in §2.3/§2.4), `gotcha-map.md` covering all 136,
  `gotchas-archive.md` as a backstop. `gotchas-archive.md` is now written at S21-W4a-3, ordered
  BEFORE S21-W4a-2's first deletion (CX-28) — archiving all 136 headings in one shot, before any
  spec (this one or S13/S19) has deleted anything, closes the transient-unrecoverable window a
  git-history-only backstop used to leave open. S21-W4a-2, S13-W4-1 and S19-W4-8 all run only
  after the archive exists. Under OQ14-a, stage b's deletions (S21-W4b-1) run before W1, before the
  archive exists; their backstop is `move-blocks --check` in the same step plus the map commit in
  git, and S21-W4a-3 later archives those rows from the map's base sha.
- **OD11 sensitivity.** Under OD11-a (architecture's non-recommended option), stage b
  (S21-W4b-1) does not run: CLAUDE.md stops after stage a at a larger size (architecture's own
  estimate: "the §9 total becomes ≈48k" tokens, i.e. `.claude/rules/` is never created and the 70
  app headings + Pages content stay in CLAUDE.md). This spec assumes OD11-b per the workflow's
  instruction to assume every OD's recommended option; if the owner later picks OD11-a, only
  S21-W4b-1 is skipped — S21-W4a-1/2/3 and the W0/W1 steps are unaffected (they do not depend on
  which OD11 branch is chosen).
- **W0 check (e) sensitivity (owned by S11, I16).** If "no" — `.claude/rules/*.md` do not load in
  a multi-repo session — the fallback per architecture §10 W0 is `docs/gotchas/*.md` with a
  pointer index in CLAUDE.md, instead of `.claude/rules/*.md`. This spec's W4b-1 step would then
  create `docs/gotchas/*.md` (same content, same `paths:` metadata kept as a documentation
  comment even though it does nothing) instead of `.claude/rules/*.md`. Not built two ways here —
  §8 names this as the one open item this spec cannot close without S11's checklist result. Under
  OQ14-a, stage b runs before W1 only when check e = yes; on "no", it waits for W4, after stage a.

## 8. Open questions

- `ASSUMES: W0 check (e) (S11/I16) reports "yes" — .claude/rules/*.md load by path match in a
  multi-repo session. If "no", S21-W4b-1's target directory changes to docs/gotchas/ (§7);
  settled by reading S11's W0 checklist result before running S21-W4b-1.`
- **CLOSED (OQ9-a, OQ14-a, 2026-09-24).** Stage b runs right after W0 check e = yes, before W1,
  inside a freeze of CLAUDE.md `## Gotchas` and `## Pages` (S21-W0-4 … S21-W0-5); stage a stays in
  W4, and S21-W4a-5 adds the size guard.
- `ASSUMES: S08's plugin-creator validate.py (I19, not yet written) does not duplicate
  check:skills's checks in a conflicting way — settled by reading S08 once it exists.`
- **CLOSED (CX-19).** Check 9 imports `scripts/lib/rewrite-gate.mjs` (S12) directly rather than
  parsing `triggers.lock.json`/`ratchet.json` itself, so there is no schema to independently track;
  both files also carry a `"schema": 1` field (S12 §2.3) for any future format change. Until
  S12-W0-2 lands that file, check 9 is a no-op (S21-W0-1).
- `ASSUMES: the OBS "58 pipeline / 78 app" estimate (digest §1.4) is approximate, not a target
  this spec's 66/70 classification must match — settled only if a reviewer re-derives the split
  and disputes a specific heading's assignment (§2.4), not the totals.`
- `ARCH-CONFLICT: none found.` The Pages-by-page split (§2.3) fills a gap the architecture leaves
  open (it says only "app gotchas + Pages → .claude/rules/*.md", not which page goes where) —
  filled in here as the map owner (I21), per architecture rule T3 (§2.1).
- Assembler note: S21-W4a-2 requires `.claude/skills/ingest-visual` and `pk-plasma-animation` to
  exist (S16's W2). Standard wave order (W0→W1→W2→W4) already guarantees this; flagged so the
  combined execution plan does not schedule W4a before S16's W2 exit.
- **NOTE (CX-55).** Two W1 items are verification-only, with no file to commit, so they are not
  change steps (a step with nothing to commit is not a step; "one step = one commit"): (1)
  `book:file-figures` text — this session's reading of CLAUDE.md:1568-1571 against `package.json`'s
  `book:file-figures: node scripts/file-figures.mjs` and `book:upload-figures: node
  scripts/upload-figures.mjs` found no discrepancy; the prose already correctly names
  `book:file-figures` as current and `book:upload-figures` as legacy-only (§1.4) — nothing to
  fix. (2) The pk-plasma-animation location line (CLAUDE.md:355, "the `pk-plasma-animation` plugin
  (`plugins/pk-plasma-animation/`, `/pk-animation <drug>`)") is factually correct as of W0/W1
  (verified: `ls learn-hub/plugins/pk-plasma-animation` exists) and becomes stale only after
  S16-W2-6 retires that plugin directory — editing it now would describe a path that does not
  exist yet. The actual edit is S21-W4a-3, after S16's W2 exit.
