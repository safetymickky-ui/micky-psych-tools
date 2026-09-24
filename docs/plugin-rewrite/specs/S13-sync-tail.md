# Spec S13: learn-hub sync tail — sync-vault, sync preflight, ready.mjs, hooks

| Field | Value |
|---|---|
| Repos | learn-hub |
| Units (today → target) | `.claude/skills/sync-vault/SKILL.md` (rewrite); `scripts/lib/readiness.mjs` (new); `scripts/ready.mjs` (new); `scripts/lib/sync-preflight.mjs` (new); `apply-sync.mjs` (wire preflight in); `package.json` `sync:preflight` entry; `.claude/hooks/pre-sync-gate.sh`, `pre-sync-repetition-gate.sh` (deleted); `.claude/settings.json` (PreToolUse hooks removed); `.claude/hooks/session-start.sh` (root resolution + done-marker + ready line); `scripts/lib/session-start-hook.test.mjs` (extended) |
| Waves | W1 (first of all learn-hub work); W4 (operational gotchas move verbatim) |
| Owner decisions assumed | OD5-a (publish only on explicit word — sync-vault never runs itself), OD11 (not reached by this spec: vault-format doc is S21's, referenced not created here) |
| Defects closed | 5 of 5 assigned (HIGH: H34, H35) |
| Interfaces owned | I13, I14 |
| Interfaces consumed | I16 (owner S11), I17 (owner S12), I21 (owner S21), I22 (owner S21) |
| Depends on specs | S21 (I22, for the `package.json` edit landing and W0 `test:py`/`check:skills`; I21 gotcha map at W4), S12 (I17 wrapper and W0 smoke-seed layout), S11 (W0 cloud confirmation before the W1-10 rehearsal) |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| Path | Lines | Role |
|---|---|---|
| `.claude/skills/sync-vault/SKILL.md` | 159 (8,033 B body, 2,008 est. tok) | the skill |
| `.claude/hooks/session-start.sh` | 92 | SessionStart hook, remote-only |
| `.claude/hooks/pre-sync-gate.sh` | 21 | PreToolUse gate, duplication |
| `.claude/hooks/pre-sync-repetition-gate.sh` | 13 | PreToolUse gate, repetition |
| `.claude/settings.json` | 31 | hooks registration |
| `scripts/apply-sync.mjs` | 683 | the real apply path (PostgREST) |
| `scripts/sync-vault.mjs` | 470 | dry SQL emitter (diagnostic only, §1.4) |
| `scripts/gate-duplicates.mjs` | 506 | duplication gate CLI (I/O + `gate-plan.mjs`) |
| `scripts/gate-repetition.mjs` | 165 | repetition gate CLI (I/O + `repetition.mjs`) |
| `scripts/lib/gate-plan.mjs` | 215 | pure: `buildFindings`, `formatGateReport`, `hookOutput`, `isSyncCommand` |
| `scripts/lib/repetition.mjs` | 433 | pure: shingle/sentence analysis, `formatRepetitionReport` |
| `scripts/lib/session-start-hook.test.mjs` | 154 | existing hook tests (real-bash fixture pattern) |

`measure.py skill` on the current file: `description.chars=252`, `use_when_at=-1`, `not_for_at=-1` (no `Use when` / `Not for` at all), `body_lines=155`, `body_est_tokens=2008`, `linked_files=["scripts/.out/sync-cache.json","scripts/.out/sync.sql","scripts/sync-vault.mjs"]`.

### 1.2 Descriptions

| Skill | chars | UTF-8 bytes | YAML valid | `Use when` offset | `Not for` present | Quoted triggers kept |
|---|---|---|---|---|---|---|
| sync-vault (today) | 252 | 252 | yes | none (−1) | no | "sync the vault", "/sync-vault", "push notes to the hub", "update the database from the vault" |
| sync-vault (target) | 590 (`measure.py textfile`) | 592 | yes | 220 | yes, at 413 | same four, unchanged |

### 1.3 Defects

| id | sev | H# | evidence (path:line, re-opened) | problem | fix step | wave |
|---|---|---|---|---|---|---|
| sync-vault-1 | H | H34 | `SKILL.md:126-132` "…groups a book's chapters under one folder … `vault/<book-slug>/<chapter-topic-id>/_topic.md`" (re-read this session, still present) | Recommends the nested layout CLAUDE.md documents as the trap that broke five tools; atomize-book actually writes flat. | S13-W1-6 | W1 |
| sync-vault-2 | H | H35 | `SKILL.md:32-34` "`sync.sql` ≲ ~200 KB → MCP path"; `:65-88` steps 1–4 (SQL → read → MCP `execute_sql` → whole-table count) | The default path only applies below ~200 KB, never true for the real vault (4,532 notes, §1.4); step 1 forces a full re-render/re-embed unwarned; none of the operational traps present. | S13-W1-6, S13-W1-1, S13-W1-2, S13-W1-3, S13-W1-4, S13-W1-5 | W1 |
| sync-vault-3 | M | — | `SKILL.md:81-88` "Confirm the counts match…"; CLAUDE.md "13 live `notes` rows with no `/vault` file" | Whole-table count verification can never match once any row outlives its file — the check never passes, or gets ignored. | S13-W1-6 | W1 |
| sync-vault-4 | M | — | `SKILL.md:157-158` "delete the row explicitly via `execute_sql`" | Ignores `purge:hidden` and the `progress`/`activity` cascade; a direct row delete destroys mastery history unless `merge_note_history` runs first. | S13-W1-6 | W1 |
| sync-vault-5 | L | — | `SKILL.md:18` "Tables: `topics`, `notes`, `links`"; `:113` "re-embeds ~2,400 notes" | Stale inventory: 6 types actually written (adds `articles`, `infographics`, `animations`); note count stale (measured 4,532, §1.4). | S13-W1-6 | W1 |

All 5 assigned defects (the `sync-vault-*` prefix in `evidence/defect-index.txt`) appear above exactly once. No deferrals.

### 1.4 Other findings

- Measured (`grep -rl '^type: note' vault --include=*.md | wc -l` etc.): 4,532 `type: note`, 851 `_topic.md`, 36 `type: article`, 36 `type: infographic`, 26 `type: animation`. Confirms the OBS figures; target body avoids hardcoding any count (§2.3).
- OBS: the sync/revalidate/verify tail is restated in 8 places today (7 pipeline skills + sync-vault itself), 4 contradictory apply rules — confirmed by grep this session. This spec fixes sync-vault's own copy only; the other 7 are fixed by their own specs delegating to sync-vault by name (architecture §2.4).
- NEW: `gate-duplicates.mjs`/`gate-repetition.mjs` already factor decision logic into `lib/gate-plan.mjs`/`lib/repetition.mjs` (pure, unit-tested). Neither CLI exports its own `run()`, so `sync-preflight.mjs` spawns them as subprocesses (`--json`, no `--hook`, so they always run) rather than re-implementing their Supabase/embedding I/O — this is what keeps `sync-preflight.mjs` itself "pure" (§2.5).
- NEW: `apply-sync.mjs` already implements "bake preserve" (`bakeOrPreserve`, `:93` `--purge-hidden`). sync-vault-4's fix is documentation-only.
- NEW: `package.json` already has `purge:hidden` and `similarity:merge`. Only `sync:preflight` is new (owned by S21, I22).
- NEW: no `evals/` directory exists anywhere in learn-hub; sync-vault has zero eval cases and no `references/`/`scripts/` subdirectory yet.

## 2. Target state

### 2.1 Location and tree (after W4, the last wave that touches these units)

```
.claude/hooks/
  session-start.sh                 # fixed root resolution + done-marker + ready line
.claude/settings.json              # SessionStart only — PreToolUse gates removed
.claude/skills/sync-vault/
  SKILL.md                         # ≤500 lines / ≤5,000 tok; house shape
  references/gotchas.md            # W4: 6 sync gotchas moved verbatim from CLAUDE.md
evals/sync-vault/
  sync-trigger-positive/{prompt.md, graders/skill-fired.md}
  sync-near-miss-coverage/{prompt.md, graders/no-skill.md}
  sync-preflight-before-apply/{case.yaml, prompt.md, fixture.sh, graders/*.md}
scripts/
  ready.mjs                        # new: readiness report CLI
  apply-sync.mjs                   # edited: calls runPreflight() first
  lib/
    readiness.mjs                  # new: pure readiness checks (shared by ready.mjs and sync-preflight.mjs)
    readiness.test.mjs             # new
    sync-preflight.mjs             # new: planPreflight + runPreflight + CLI
    sync-preflight.test.mjs        # new
```

Deleted: `.claude/hooks/pre-sync-gate.sh`, `.claude/hooks/pre-sync-repetition-gate.sh`.

Not touched by this spec (owned elsewhere, referenced only): `docs/vault-format.md` (S21, I21) — until it exists, SKILL.md points at `CLAUDE.md` "Vault note format" as it does today; the W4 step switches the pointer once S21 lands it (§8).

### 2.2 Frontmatter

```yaml
---
name: sync-vault
description: Pushes authored /vault markdown into the Learn app's Supabase database through a readiness check, a background apply job, and a verify-and-revalidate tail — sole owner of the sync tail every pipeline skill delegates to. Use when vault content was just written or edited and needs to go live, or when the user says "sync the vault", "/sync-vault", "push notes to the hub", or "update the database from the vault". Not for authoring vault content (use atomize-book, ingest-article, ingest-slides, or digest-report) or measuring coverage or redundancy (use vault-coverage or check-repetition).
metadata:
  profile: cc
---
```

Valid under `yaml.safe_load` (two top-level keys, one nested `metadata.profile`). Measured (`measure.py textfile`): 590 chars, 592 UTF-8 bytes, `use_when_at=220` (within the ~250-char rule, R4), `not_for_at=413`, no `I/you/your`, no `<`/`>`. Kept trigger phrases, unchanged from today: `"sync the vault"`, `"/sync-vault"`, `"push notes to the hub"`, `"update the database from the vault"`. No new phrase added (no Thai form exists in the source; not invented, per the writing rules).

### 2.3 Body outline (target, W1; the W4 column shows what further moves)

| # | Section | Source (today) | W1 disposition | W4 disposition |
|---|---|---|---|---|
| 1 | Standing rules (R12): sole owner of the tail; delegate by name | new | new, ~10 lines | keep |
| 2 | Project (Supabase ref, shared project note) | `:12-17`, kept | keep, trim | keep |
| 3 | ~~Which apply path~~ (≲200KB/MCP branch) | `:25-45` | **cut** — never taken on this vault (sync-vault-2); `sync:apply` is the only path | — |
| 4 | Steps: 0 readiness, 1 fetch+merge, 2 `sync:preflight`, 3 `sync:apply` (background+log), 4 verify (per-provenance), 5 revalidate, 6 similarity snapshot (optional, unchanged) | `:47-115` | **rewrite**, ~55 lines (§3) | trim once gotchas move out |
| 5 | Optional diagnostic: `npm run sync` — never applied, catches YAML/mermaid errors early | `:65-72` (folded in) | new, ~8 lines, cites the dry-run-economics gotcha by name | citation moves into `references/gotchas.md` |
| 6 | Vault layout (flat) | `:117-135` | **rewrite** to flat (sync-vault-1); ~12 lines | keep |
| 7 | Note format contract | `:137-143` | keep, points at CLAUDE.md (docs/vault-format.md not built yet) | repoint to `docs/vault-format.md` |
| 8 | Other content types | `:145-153` | keep, fix table to 6 types (sync-vault-5) | keep |
| 9 | Removing content (purge:hidden/merge_note_history) | `:155-159` | **rewrite** (sync-vault-4); ~10 lines | keep |
| 10 | `## Gotchas` | absent | new, ~6 lines, pointer to `references/gotchas.md` | filled with the 6 moved gotchas |

Target W1 body: ≈170 lines total, ≈2,000 tokens — net smaller than today's 155 lines despite the new readiness/verification detail, because the "Which apply path" branch (21 lines, 200KB arithmetic) is deleted outright. Well under R11's 500-line/5,000-token cap; this is a sub-step skill other skills invoke by name, so the ≤2,000-token *(house)* gate/filer target is also met.

### 2.4 References

| File | Purpose | Load condition | Size target |
|---|---|---|---|
| `references/gotchas.md` | 6 operational sync gotchas moved verbatim from CLAUDE.md (TaskStop zombie, background exit-code trap, fetch-first, bake preserve, SessionStart hook, sync cache) | "Before running step 3 (`sync:apply` in the background), read `references/gotchas.md`." (W4 only — absent in W1, see §3 W4 step) | ≤6 KB (six short gotchas, unchanged text) |

No other reference file. R14 is met trivially (one file, one conditional pointer) once W4 lands; in W1 there is no `references/` directory yet (the SKILL.md body carries the (few) needed facts inline).

### 2.5 Scripts

#### `scripts/lib/readiness.mjs` (new)

| Export | Signature | Behaviour |
|---|---|---|
| `checkNodeModules` | `(root: string) => Check` | `ok` iff `<root>/node_modules` exists (`existsSync`) |
| `checkEnvCreds` | `(root: string, env: object) => Check` | `ok` iff `<root>/.env.local` exists **or** `env.NEXT_PUBLIC_SUPABASE_URL` and `env.SUPABASE_SERVICE_ROLE_KEY` are both set |
| `checkChromium` | `(env: object, resolveBundled = () => puppeteer.executablePath()) => Check` | if `env.PUPPETEER_EXECUTABLE_PATH` is set, `ok` iff that path exists (puppeteer honours a set variable, so a wrong one is a failure, not a fallback); if it is unset, `ok` iff `resolveBundled()` returns a path that exists — puppeteer's own downloaded browser, which is what Windows uses (architecture §2.6 leaves the variable unset there; critique F5). `resolveBundled` is injected in tests |
| `checkPyMuPDF` | `(exec = execFile) => Promise<Check>` | tries `python3`, then `python`, then `py -3` (first that runs), with `-c "import fitz"`; `ok` iff exit 0; `detail` names the interpreter used (Windows often has no `python3`, critique F9) |
| `checkPoppler` | `(exec = execFile) => Promise<Check>` | runs `pdftoppm -v`; `ok` iff exit 0 (poppler prints its version to stderr on `-v` and still exits 0) |
| `runReadinessChecks` | `(opts) => Promise<Check[]>` | runs all five, in the order above |

`Check` shape: `{ id: string, label: string, ok: boolean, detail: string, fix: string \| null }`. `fix` is `null` when `ok`. Every check takes its inputs as parameters (root path, env object, an injectable `exec`) — no implicit `process.env`/`process.cwd()` reads — so `readiness.test.mjs` calls each directly with fixture values; the two `python3`/`pdftoppm` checks take a fake `exec` in tests and the real `node:child_process.execFile` at the CLI boundary.

Fix text per check (used verbatim in both `ready.mjs`'s human output and `sync-preflight.mjs`'s refusal message):

| id | fix text when `!ok` |
|---|---|
| `node_modules` | `run bash .claude/hooks/session-start.sh (or npm install locally)` |
| `env` | `run bash .claude/hooks/session-start.sh to materialize .env.local, or set NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY` |
| `chromium` | `run bash .claude/hooks/session-start.sh (sets PUPPETEER_EXECUTABLE_PATH), or export it yourself if the image changed; locally, unset a wrong PUPPETEER_EXECUTABLE_PATH or run npx puppeteer browsers install chrome` |
| `pymupdf` | `pip install pymupdf` |
| `poppler` | `apt-get install -y poppler-utils` |

#### `scripts/ready.mjs` (new) — **I13**

CLI: `node scripts/ready.mjs [--json]`. No side effects; read-only. Calls `runReadinessChecks({ root: REPO_ROOT, env: process.env })` from `lib/readiness.mjs`.

JSON stdout shape:
```json
{
  "ok": true,
  "generated_at": "2026-09-24T00:00:00.000Z",
  "checks": [
    {"id": "node_modules", "label": "node_modules installed", "ok": true, "detail": "…", "fix": null}
  ]
}
```
`ok` at the top level is `checks.every(c => c.ok)`. Without `--json`: one line per check, `OK  <label>` or `FAIL <label> — <fix>`, plus a final `ready: yes|no` line.

Exit codes: `0` every check passed; `1` at least one check failed. `--help` prints usage and exits 0 with no other output.

#### `scripts/lib/sync-preflight.mjs` (new) — **I13**

Exports:
- `planPreflight({ readiness, staleness, dupText, repText })` — **pure**, no I/O. `readiness` = the 3-check subset (`node_modules`, `env`, `chromium`); `staleness` = `{ checked, behind, warning }`; `dupText`/`repText` = already-gathered gate strings (`""` = nothing to say). Returns `{ ready, exitCode: 0|2, report }`. `ready=false` iff any readiness check failed; the report then names ONLY those failures + fix text + `bash .claude/hooks/session-start.sh` (architecture §5.7: "On failure it exits 2 and names `bash .claude/hooks/session-start.sh`"), omitting staleness/gate text. When `ready=true`, the report concatenates the staleness warning (if any) then both gate texts (if any); empty when there is nothing to say.
- `runPreflight({ root = REPO_ROOT } = {})` — **I/O wrapper**, `async`. Gathers the 3 readiness checks; staleness via `execFile("git", ["rev-list","--count","HEAD..origin/master"], {cwd:root})` parsed by pure `parseAheadCount` (`null` on any git failure — no origin, detached HEAD — so staleness degrades silently); the two gate texts via `execFile(process.execPath, [join(root, "scripts/gate-duplicates.mjs"), "--json"], {cwd: root})` / the same for `gate-repetition.mjs` (no `--hook`, so they always run; absolute path and `cwd: root`, so they run from any cwd, including `/home/user` — critique F11), each parsed as `gate-plan.mjs`'s own `hookOutput` shape and `additionalContext` extracted. A crash still never fails the preflight, but it is no longer silent: the gate text becomes `gate unavailable: <name> (<error message>)`. Calls `planPreflight` with the gathered inputs.
- `parseAheadCount(stdout)` — pure: trims/`parseInt`s a `git rev-list --count` line; `null` on anything non-numeric.

CLI (bottom of file, `invokedDirectly` guard as `purge-hidden.mjs` already uses): runs `runPreflight()`, prints `report` (or JSON under `--json`), sets `process.exitCode`. Never `process.exit()` directly (the Node-24/Windows libuv trap applies here too).

`npm run sync:preflight` → `node scripts/lib/sync-preflight.mjs` (package.json entry, §3 step; coordinate with S21/I22).

Tests (`scripts/lib/sync-preflight.test.mjs`, vitest): `planPreflight` — all-ready no-warnings → `{ready:true, exitCode:0, report:""}`; one readiness check failing → `ready:false, exitCode:2`, report names only that check + fix + the session-start command, and omits a supplied staleness warning; ready + staleness behind + both gate texts non-empty → report contains all three, in order; ready + everything empty → `report:""`. `parseAheadCount` — `"0\n"` → `0`; `"12\n"` → `12`; `""`/garbage → `null`. A gate-crash input (`dupText = "gate unavailable: gate-duplicates (…)"`) appears in the report and leaves `ready:true` (critique F11).

#### `scripts/apply-sync.mjs` (edited)

At the top of `main()`, after `loadEnv()`/before the Supabase client is created: call `runPreflight()` and pass the result to the pure `gateOnPreflight(result, {preflightOnly}) → {proceed, exitCode, stderr}` (in `lib/sync-preflight.mjs`); if `!proceed`, print `stderr`, set `process.exitCode = exitCode` and return (no Supabase client, no hidden-marks logic, no vault parse). `--preflight-only` makes `proceed` false in every case: the script exits with the preflight's own code (0 or 2) before any Supabase client exists, so a refusal test can never write to the shared database (critique C2-04, F6). If `ready` and `report` is non-empty, `console.warn(report)` and continue as today. `main()` takes an injectable client factory so a vitest case can assert that the preflight runs before the factory is ever called. This is a deliberate behaviour change: a missing Chromium used to only warn (`apply-sync.mjs:278`) and the run still completed; now it is a hard refusal before any work starts, per architecture §5.7 ("On failure it exits 2"), closing sync-vault-2/H35's "no traps" complaint before the background job spends its wall-clock budget. The existing `bakeOrPreserve` fallback still protects the DB on any LATER, mid-run failure — this refusal only covers the environment never having been ready to begin with.

### 2.6 Handoffs

sync-vault is a terminus, not a caller — it makes no OPTIONAL cross-skill handoff itself. It is the target of every other pipeline skill's handoff. Per architecture §2.4 ("link to it and never restate it") and CX-17 — replacing the seven different forms other specs had each written independently — every caller in learn-hub carries exactly this sentence (I13, one sentence, no restated fallback, since sync-vault is same-repo and always present, unlike a cross-plugin OPTIONAL handoff): `Publish through the sync-vault skill (same repo, always present). Follow its steps as written; do not restate them here.` sync-vault's own body states the reciprocal rule as a standing rule (§2.3 row 1): it never re-describes another skill's authoring steps, and it is never itself the thing that decides WHETHER to publish (OD5-a: only on an explicit "digest"/"publish"/"sync" word from the caller or the user).

### 2.7 Interfaces

**Owned:**

- **I13 — Sync tail.** Caller handoff sentence (CX-17, verbatim, §2.6): `Publish through the sync-vault skill (same repo, always present). Follow its steps as written; do not restate them here.` The full procedure, in order:
  1. `git fetch` then a merge check (`git log --oneline HEAD..origin/master`, or `git status`) — run by hand or by the calling skill, **not** by `sync-preflight.mjs` (no network calls inside the preflight; §2.5).
  2. `npm run sync:preflight` — foreground, ≈10 s. Exit 0 = proceed (read warnings); exit 2 = stop, fix the named gap, re-run.
  3. `npm run sync:apply` — a **background job with a log file and no inner `&`** (`Bash`'s own `run_in_background: true`; see the "background exit-code trap"/"TaskStop zombie" gotchas, W4). Never `npm run sync` → MCP `execute_sql` — that branch is deleted (sync-vault-2).
  4. Success = the log contains `EXIT=0` **and** an `Upserted N note(s) (…)` line (unchanged text `apply-sync.mjs` already prints).
  5. **Per-provenance verification**: confirm the ids THIS run touched (the log's own ids, or `select id, updated from notes where updated >= '<run start>' order by updated desc`), never a whole-table `count(*)` vs. vault-file-walk comparison (sync-vault-3 — DB rows can outlive their file).
  6. `npm run revalidate` (unchanged).
  7. Deletion, when wanted: staged app-hidden content → `npm run purge:hidden -- --yes` or `sync:apply --purge-hidden`; merging notes → `node scripts/merge-notes.mjs`, which runs `merge_note_history` **before** removing the losing row. Never delete a `notes`/`topics` row directly via SQL (sync-vault-4).
  - `scripts/lib/sync-preflight.mjs` and `scripts/ready.mjs`: full contracts in §2.5.
- **I14 — Session setup.** `.claude/hooks/session-start.sh` root resolution: (1) `LEARN_HUB_DIR`, if set and the dir exists; (2) `CLAUDE_PROJECT_DIR`, only if it passes the learn-hub marker (`package.json` `"name": "learn-hub"` + `scripts/apply-sync.mjs`, architecture §2.6); (3) the script's own path, today's fallback, unchanged. A **done-marker** at `<root>/.claude/.session-start.done` (gitignored) holds the session key (`$CLAUDE_ENV_FILE`, or the hook's stdin `session_id` when that variable is unset): absent → the full sequence (hooksPath, Chromium exports, `npm install`, `.env.local`) runs once, then the marker is written with the key; present with the SAME key (§3.7: "settings.json SessionStart **and** the plugin hook both fire" once `CLAUDE_CODE_PLUGIN_DIRS` includes `/home/user/learn-hub/plugins`) → skip to the ready line, exit 0; present with a DIFFERENT key (a resumed session or a reused container) → re-run the per-session parts (the `CLAUDE_ENV_FILE` export of `PUPPETEER_EXECUTABLE_PATH`, the `.env.local` refresh) and skip only `npm install` (critique F10). The **ready line** (every invocation) is `session-start: ready — project dir <dir> — claude <version, or "unknown"> — plugins: <claude plugin list, or "unavailable">`, so a duplicate load or a `path-not-found` plugin is visible every session start — matches S11's own ASSUMES for I14.

**Consumed:**

- **I16 (owner S11).** ASSUMES: the cloud environment sets `PUPPETEER_EXECUTABLE_PATH=/opt/pw-browsers/chromium` and `PUPPETEER_SKIP_DOWNLOAD=1` directly on the environment (not only via the hook's `CLAUDE_ENV_FILE` export), per architecture §2.6's variable table — so `readiness.mjs`'s `checkChromium` sees a populated `process.env.PUPPETEER_EXECUTABLE_PATH` independent of whether `session-start.sh` has run yet in THIS process. Confirmed consistent with S11 §2.7 line 212 ("Validation markers are the architecture's") and its I16.1 table — not re-defined here.
- **I17 (owner S12).** ASSUMES: `scripts/eval-project-skill.sh sync-vault` builds the throwaway plugin and runs `claude plugin eval` against `evals/sync-vault/`, per architecture §6.5; sync-vault's cases follow the same `prompt.md`/`graders/*.md` shape as every plugin skill (eval-format.md), since the eval CLI does not distinguish a project skill's cases from a plugin's once wrapped.
- **I21 (owner S21).** ASSUMES: `docs/rewrite/gotcha-map.md` will name exactly which CLAUDE.md headings move to `.claude/skills/sync-vault/references/gotchas.md` — the W4 step in §3 below names the 6 candidates this spec identifies by direct evidence (TaskStop zombie, background exit-code trap, fetch-first, bake preserve, SessionStart hook, sync cache) and instructs the W4 executor to reconcile against S21's map before moving text, rather than assuming this list is final (§8).
- **I22 (owner S21).** ASSUMES: the single package.json edit list (owned by S21) includes `"sync:preflight": "node scripts/lib/sync-preflight.mjs"`. This spec's own W1 step adds that one line directly (§3, S13-W1-5) rather than waiting on S21, because sync-vault is first in W1 and nothing else needs this entry yet; if S21's own pass finds the line already present it is a no-op, not a conflict (§8).

## 3. Change steps

### Wave 0

**S13-W0-1 (new, CX-4)**
- Repo: learn-hub · depends on: S12-W0-4
- Files: create 3 `evals/sync-vault/*` case directories, ahead of S13-W1-9's fuller set. Each takes the name of a §4.1 case (`sync-trigger-positive`, `sync-near-miss-coverage`, `sync-preflight-before-apply`), so S13-W1-9 extends them instead of adding new ones (critique P7); each is tagged `smoke`.
- Change: seed 3 `smoke`-tagged cases against TODAY's sync-vault SKILL.md, I17 layout, current script paths (architecture §10 W0 item 3) — this is the pre-rewrite baseline S12's smoke suite needs before I16.3 condition 4 can pass at V2/V3.
- Commands: `find evals/sync-vault -name prompt.md | xargs grep -l 'tags:.*smoke' | wc -l`
- Done when: the count is ≥3.
- Rollback: delete `evals/sync-vault/`.

### Wave 1

**S13-W1-1**
- Repo: learn-hub · depends on: none
- Files: create `scripts/lib/readiness.mjs`, `scripts/lib/readiness.test.mjs`
- Change: add the five pure/injectable checks and `runReadinessChecks` exactly as specified in §2.5 (table of exports, `Check` shape, fix text table).
- Commands: `node --check scripts/lib/readiness.mjs`; `npx vitest run scripts/lib/readiness.test.mjs`
- Done when: `npx vitest run scripts/lib/readiness.test.mjs` exits 0 with the 5-export cases (node_modules present/absent, env via file/via vars/neither, chromium set-and-exists/set-missing/unset-with-bundled-browser/unset-without, pymupdf ok/fail via a fake `exec` (and the `python` fallback when `python3` is absent), poppler ok/fail via a fake `exec`) all green.
- Rollback: delete both files.

**S13-W1-2**
- Repo: learn-hub · depends on: S13-W1-1
- Files: create `scripts/ready.mjs`
- Change: CLI wrapper per §2.5 (`--json`, `--help`, exit 0/1, human + JSON output).
- Commands: `node scripts/ready.mjs --help`; `node scripts/ready.mjs --json | python3 -m json.tool >/dev/null`
- Done when: `node scripts/ready.mjs --help` exits 0 and prints usage with no side effects; `node scripts/ready.mjs --json` prints valid JSON matching the §2.5 shape (`checks` has exactly 5 entries with the 5 documented ids).
- Rollback: delete the file.

**S13-W1-3**
- Repo: learn-hub · depends on: S13-W1-1
- Files: create `scripts/lib/sync-preflight.mjs`, `scripts/lib/sync-preflight.test.mjs`
- Change: `planPreflight`, `runPreflight`, `parseAheadCount`, and the CLI guard, per §2.5.
- Commands: `node --check scripts/lib/sync-preflight.mjs`; `npx vitest run scripts/lib/sync-preflight.test.mjs`
- Done when: the four `planPreflight` cases, the gate-crash case and the `parseAheadCount` cases listed in §2.5 all pass, plus `gateOnPreflight` cases (not ready → exit 2; ready → proceed; `--preflight-only` → no proceed, exit 0 or 2).
- Rollback: delete both files.

**S13-W1-4**
- Repo: learn-hub · depends on: S13-W1-3
- Files: edit `scripts/apply-sync.mjs`
- Change: import `runPreflight` and `gateOnPreflight` from `./lib/sync-preflight.mjs`; insert the preflight call at the start of `main()` (§2.5), before `const url = env.NEXT_PUBLIC_SUPABASE_URL;` (`apply-sync.mjs:78`); add `--preflight-only` and the injectable client factory (§2.5). Add `scripts/apply-sync.test.mjs`: with a fake preflight that is not ready, `main()` never calls the client factory.
- Commands: `node --check scripts/apply-sync.mjs`; `npx vitest run scripts/apply-sync.test.mjs`; `PUPPETEER_EXECUTABLE_PATH=/nonexistent node scripts/apply-sync.mjs --preflight-only; echo "EXIT=$?"`. Never run it without `--preflight-only` outside an OWNER step: `.env.local` holds live credentials (critique C2-04, F6).
- Done when: the vitest case passes; the command above prints `EXIT=2` and the readiness report naming `chromium` + the session-start fix text, with no `Upserted` line anywhere.
- Rollback: revert the edit (import + 4-line preflight block).

**S13-W1-5**
- Repo: learn-hub · depends on: S13-W1-3, S21-W0-2 (CX-39: same-file `package.json` edit order)
- Files: edit `package.json`; edit `README.md` (one script-table row for `sync:preflight`; learn-hub Documentation upkeep, critique F12)
- Change: add `"sync:preflight": "node scripts/lib/sync-preflight.mjs",` alongside `"sync:apply"` (`package.json:17`). Coordinate with S21 (I22 owner) — no-op if already present.
- Commands: `node -e "const p=require('./package.json'); if(p.scripts['sync:preflight']!=='node scripts/lib/sync-preflight.mjs') process.exit(1)"`
- Done when: the command exits 0.
- Rollback: remove the one line.

**S13-W1-6**
- Repo: learn-hub · depends on: S13-W1-2, S13-W1-3, S13-W1-5
- Files: rewrite `.claude/skills/sync-vault/SKILL.md`
- Change: apply §2.2 + §2.3 in full — delete the "Which apply path" branch and steps 1–4 (`SKILL.md:25-45`, `:65-88`); replace with the I13 procedure (§2.7); rewrite "Vault layout" to the flat form; fix "Other content types" to list all 6 types; replace the deletion paragraph (`:157-159`) with purge:hidden/merge_note_history guidance; add `## Gotchas` with the (empty-until-W4) pointer. No `references/` yet.
- Commands: `python3 $MICKY_TOOLS_DIR/docs/plugin-rewrite/phase3/measure.py skill .claude/skills/sync-vault/SKILL.md`; `claude plugin validate --strict .claude` (the `.claude/skills` form exits 1, "No manifest found" — critique C2-05)
- Done when: `measure.py` reports `yaml_valid: true`, `description.chars`≤1024, `use_when_at` present and ≤~250, `not_for_at` present, `body_lines`≤500; validator reports no error for sync-vault.
- Rollback: `git checkout -- .claude/skills/sync-vault/SKILL.md`.

**S13-W1-7**
- Repo: learn-hub · depends on: S13-W1-4 (CX-48: the gates' logic must already run inside `sync-preflight.mjs`/`apply-sync.mjs` before the PreToolUse gates that enforced it are removed, or a commit window has no gates at all)
- Files: edit `.claude/settings.json`; delete `.claude/hooks/pre-sync-gate.sh`, `pre-sync-repetition-gate.sh`; edit `README.md`, `CLAUDE.md`
- Change: remove the `"PreToolUse"` array, leaving only `"SessionStart"`; delete both gate hook scripts (their logic now runs inside `sync-preflight.mjs`, §2.5; the underlying CLIs are unchanged and still work standalone via `similarity:gate`/`repetition:gate`). Same commit (learn-hub CLAUDE.md, Documentation upkeep; critique F12): replace `README.md:159-163` ("The gate also fires automatically before a sync via a `PreToolUse` hook … which is why `sync-vault` SKILL.md runs it as step 0.") with one sentence saying both gates run inside `npm run sync:preflight`, which `apply-sync.mjs` calls first, warn-only; in `CLAUDE.md` change "runs from a `PreToolUse(Bash)` hook" (:2616) to say the gate ran from such a hook until this change and now runs inside `sync-preflight.mjs` (keep the exit-0 law text), and drop "`PreToolUse`" from "warn-only `PreToolUse` gate" (:2649). W4 then moves the corrected text verbatim.
- Commands: `python3 -m json.tool .claude/settings.json >/dev/null`
- Done when: settings.json parses and has no `PreToolUse` key; `test ! -e .claude/hooks/pre-sync-gate.sh && test ! -e .claude/hooks/pre-sync-repetition-gate.sh`; `grep -c PreToolUse README.md` = 0; `grep -n PreToolUse CLAUDE.md` shows only past-tense lines.
- Rollback: `git revert <this commit>`.

**S13-W1-8**
- Repo: learn-hub · depends on: none
- Files: edit `.claude/hooks/session-start.sh`; edit `scripts/lib/session-start-hook.test.mjs`; edit `.gitignore`
- Change: implement the I14 root-resolution, done-marker and ready line (§2.7). Replace the unconditional `PROJECT_DIR="${CLAUDE_PROJECT_DIR:-}"` block (`:21-29`) with the 3-step resolution, keeping the existing exit-1 guard; wrap the hooksPath/Chromium/`npm install`/`.env.local` block in a marker check (`$PROJECT_DIR/.claude/.session-start.done`, holding the session key — absent → run all, then write the key; same key → print a skip line, no re-run; different key → re-run the `CLAUDE_ENV_FILE` export and `.env.local`, skip `npm install`; §2.7 I14); replace the final ready-line echo (`:92`) with the version from §2.7 (`|| echo unknown` / `|| echo unavailable` guards). Add the marker path to `.gitignore`. Extend the test fixture with a `bin/claude` stub (fixed `--version` + `plugin list` output) and 4 new cases: LEARN_HUB_DIR wins over CLAUDE_PROJECT_DIR; a marker-failing CLAUDE_PROJECT_DIR falls through to the script-relative path; a second invocation with the same key skips npm install/.env.local and still prints the ready line; an invocation with a new `CLAUDE_ENV_FILE` writes the `PUPPETEER_EXECUTABLE_PATH` export into it and skips only npm install (critique F10); the ready line carries the stubbed claude output.
- Commands: `bash -n .claude/hooks/session-start.sh`; `npx vitest run scripts/lib/session-start-hook.test.mjs`
- Done when: the test file is green, 5 new cases + all 7 existing ones.
- Rollback: `git checkout -- .claude/hooks/session-start.sh scripts/lib/session-start-hook.test.mjs .gitignore`.

**S13-W1-9**
- Repo: learn-hub · depends on: S13-W1-6, S13-W0-1
- Files: extend the `evals/sync-vault/*` case directories seeded at S13-W0-1 to the full set (§4.1)
- Change: the full case set in full, §4.1.
- Commands: `bash scripts/eval-project-skill.sh sync-vault --smoke --json /tmp/s13-smoke.json` (CX-46; deferred until S12's wrapper exists — not written by hand here)
- Done when: every case directory §4.1 names exists (the 3 W0 seeds among them) with valid frontmatter, and every grader has a `type` key from eval-format.md.
- Rollback: `git revert <this commit>` (the W0 seeds stay).

**S13-W1-10** — OWNER
- Repo: learn-hub · depends on: S13-W1-1..9, S11-W0-11 (CX-34)
- Action: in a real multi-repo cloud session, make a trivial edit to one vault note's body, run the full I13 procedure by hand, confirm the log ends `EXIT=0` + `Upserted … note(s) (… with a fresh vector)`, and run `select count(*) from notes where diagrams <> '{}'::jsonb` before/after to confirm no drop (architecture §10 W1 exit). Commit the edited vault note to learn-hub master directly (never to a wave branch: its row is now live; critique C2-21). Record both counts and the log tail in learn-hub `docs/rewrite/baseline.md` under `## Owner records` (S12 §2.3); the W1 tag step closes H34/H35 in `h-coverage.md`.
- Done when: the owner confirms no drop and pastes the `EXIT=0`/`Upserted` line.
- Rollback: n/a (verification only).

**S13-W1-11 (new, CX-61)**
- Repo: learn-hub · depends on: S13-W1-5
- Files: edit `docs/cloud-env-setup.md`.
- Change: replace the `npm run sync` verification recommendation at line 144 with `npm run sync:preflight` (the full dry emitter never applies and is the wrong tool for a readiness check; §2.5 owns `sync:preflight`).
- Commands: `grep -n 'npm run sync' docs/cloud-env-setup.md`
- Done when: the grep shows only `npm run sync:preflight` (and `npm run sync:apply` if present elsewhere), never a bare `npm run sync`.
- Rollback: `git checkout -- docs/cloud-env-setup.md`.

### Wave 4

**S13-W4-1**
- Repo: learn-hub · depends on: S13-W1-6, S21-W4a-2 (CX-28)
- Files: create `.claude/skills/sync-vault/references/gotchas.md`; edit SKILL.md (repoint the note-format reference to `docs/vault-format.md`); edit `CLAUDE.md`
- Change: read S21-W4a-2's `gotcha-map.md` for the confirmed heading list (the map wins over the candidate list below if they disagree). Move each heading's text **verbatim** from CLAUDE.md into `references/gotchas.md`, **and delete the moved headings from CLAUDE.md in this same commit** (CX-28 — moving and deleting are one commit, not two; the map's assignment is what decides which headings this step deletes, and S21-W4a-2 must land first, since S21-W4a-3 archives the pre-move text before this step touches it). Candidate list, by direct evidence read this session (`CLAUDE.md` line ranges): background exit-code trap (`1685-1704`), TaskStop zombie (`1705-1721`), sync cache (`1743-1768`), bake preserve (`2425-2449`), SessionStart hook (`2450-2471`), fetch-first (`2950-2971`). Also candidate: "DB rows can outlive their /vault source" (`1722-1742`, direct evidence for sync-vault-3).
- Commands: `node scripts/move-blocks.mjs --map docs/rewrite/gotcha-map.md --dest sync-vault --write`, then `node scripts/move-blocks.mjs --check` (S21-W4a-4); `grep -c '<moved heading text>' CLAUDE.md`
- Done when: `move-blocks --check` exits 0 (every moved block is byte-identical to the W4-entry copy); the file contains exactly the headings S21's map assigns here, each with a `path:line` provenance comment; the moved headings no longer appear in CLAUDE.md. No size cap: the six candidate ranges alone measure 12,025 bytes verbatim, and a `references/` file loads only on demand (critique P10).
- Rollback: `git checkout -- .claude/skills/sync-vault/references/gotchas.md .claude/skills/sync-vault/SKILL.md CLAUDE.md`.

## 4. Evals

### 4.1 Cases

**`evals/sync-vault/sync-trigger-positive/prompt.md`**
```markdown
---
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
tags: [trigger, smoke]
---

I just finished editing a note in /vault after fixing a typo. Push the change to the Learn app's database.
```

**`evals/sync-vault/sync-trigger-positive/graders/skill-fired.md`**
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?sync-vault"'
---
```

**`evals/sync-vault/sync-near-miss-coverage/prompt.md`**
```markdown
---
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
tags: [negative]
---

Check whether the notes I wrote for the CBT chapter repeat each other too much before I move on.
```

**`evals/sync-vault/sync-near-miss-coverage/graders/no-skill.md`**
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?sync-vault"'
min: 0
max: 0
arm: both
---
```

**`evals/sync-vault/sync-preflight-before-apply/case.yaml`**
```yaml
schema_version: "1.1"
name: sync-preflight-before-apply
tags: [process, smoke]
context:
  scaffold_script: fixture.sh
```

**`evals/sync-vault/sync-preflight-before-apply/prompt.md`**
```markdown
---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Bash, Skill]
---

Sync the vault changes to the database. It's a big vault, so run the apply step as a background job with a log file, not in the foreground.
```

**`evals/sync-vault/sync-preflight-before-apply/fixture.sh`**
```bash
#!/bin/bash
set -e
cat > package.json <<'JSON'
{
  "name": "learn-hub",
  "scripts": {
    "sync:preflight": "node -e \"console.log('Vault duplication gate — 1 new/changed note(s) screened against 0 existing; nothing above the floor.')\"",
    "sync:apply": "node -e \"console.log('Rendered 0 unique diagram(s) from 0 fence(s).'); console.log('Upserted 1 topic(s).'); console.log('Upserted 1 note(s) (1 with a fresh vector).'); console.log('Done.');\""
  }
}
JSON
mkdir -p vault/psy-test node_modules
cat > vault/psy-test/_topic.md <<'MD'
---
id: psy-test
type: topic
title: Test Topic
domain: Test
order: 9999
status: active
created: 2026-09-24
updated: 2026-09-24
---
MD
cat > vault/psy-test/psy-test-note.md <<'MD'
---
id: psy-test-note
type: note
topic: psy-test
title: Test Note
summary: A fixture note for the sync-vault eval.
order: 1
created: 2026-09-24
updated: 2026-09-24
---
Fixture body text.
MD
touch .env.local
```

**`evals/sync-vault/sync-preflight-before-apply/graders/order.md`**
```markdown
---
type: tool_order
before:
  tool: Bash
  input_match: 'sync:preflight'
after:
  tool: Bash
  input_match: 'sync:apply'
---
```

**`evals/sync-vault/sync-preflight-before-apply/graders/process.md`**
```markdown
---
type: llm
weight: 2
criteria: |
  PASS if the response runs the apply step as a background job with a log file (not a
  bare `&` inside one shell call) and reports success from the log's `EXIT=0` and
  `Upserted … note(s)` line.
  FAIL if it claims success without checking those, or runs `npm run sync` followed by
  an MCP `execute_sql` step.
---
```

Further cases (table only, per the size limit — no full contents):

| Name | Tags | Prompt gist | Graders |
|---|---|---|---|
| sync-near-miss-authoring | negative | "Add this PDF to the Learn hub" → pdf-pipeline/atomize-book, not sync-vault | `tool_used Skill`, `min:0 max:0 arm:both` |
| sync-flat-layout-output | output | ask what layout a new book's vault files should use | `regex` on `last_message`: flat `vault/<topic-slug>/_topic.md` present, nested `vault/<book>/<chapter>/` absent |

### 4.2 Conversion

No prior `evals.json` entries exist for sync-vault (learn-hub project skills ship no evals today, §1.4). Nothing to convert; all 3+2 cases above are new.

### 4.3 Live triggers

sync-vault is not a member of any of the 5 contested families in architecture §6.3 — a pipeline terminus other skills call by name, not competing for the same phrasing. `ASSUMES: only the isolated (per-skill) cases in §4.1 plus this near-miss set are needed, not a dedicated live-trigger family — S12 (I17 owner) to confirm at W3/W4 trigger-lock time.`

Near-miss queries (2–4, for S12's family query sets):
1. "Did we lose anything from the trauma book when we atomized it?" → should route to `vault-coverage`, not sync-vault.
2. "Check these notes for repeated content before I sync." → should route to `check-repetition` first; sync-vault only if the user then says "now push it."
3. "Add this book to the Learn hub." → should route to `pdf-pipeline`/`atomize-book` (which call sync-vault internally at their own end), not sync-vault directly.
4. "Ingest this article PDF." → should route to `ingest-article`, not sync-vault.

### 4.4 Commands

- Smoke: `bash scripts/eval-project-skill.sh sync-vault --smoke -- --allow-tools Bash --json /tmp/sync-vault-smoke.json` (S12's wrapper, §6.5 of the architecture; CX-46). `sync-preflight-before-apply` is smoke-tagged so the W1 exit gate "sync-vault picks preflight" runs it; it needs the Bash grant and the scaffold (the wrapper passes `--scaffold`, critique F3).
- Release: `bash scripts/eval-project-skill.sh sync-vault --release --json /tmp/sync-vault-release.json` (two-arm, at the W3/W5 exits per §10; CX-46).
- Project-side: `npx vitest run scripts/lib/readiness.test.mjs scripts/lib/sync-preflight.test.mjs scripts/lib/session-start-hook.test.mjs`.

## 5. Acceptance criteria

1. `measure.py skill .claude/skills/sync-vault/SKILL.md` → `yaml_valid: true`, `description.chars`≤1024, `use_when_at` present and ≤~250, `not_for_at` present, `body_lines`≤500.
2. `grep -c "vault/<book-slug>/<chapter-topic-id>" SKILL.md` → `0`.
3. `grep -c "≲ ~200 KB\|execute_sql" SKILL.md` → `0`.
4. `grep -c "purge:hidden\|merge_note_history" SKILL.md` → ≥1 each.
5. `python3 -m json.tool .claude/settings.json | grep -c PreToolUse` → `0`.
6. `test ! -e .claude/hooks/pre-sync-gate.sh -a ! -e .claude/hooks/pre-sync-repetition-gate.sh` → exit 0.
7. `npx vitest run scripts/lib/readiness.test.mjs scripts/lib/sync-preflight.test.mjs scripts/lib/session-start-hook.test.mjs` → exit 0.
8. `node scripts/ready.mjs --json | python3 -c "import json,sys;d=json.load(sys.stdin);assert len(d['checks'])==5"` → exits 0.
9. `PUPPETEER_EXECUTABLE_PATH=/nonexistent node scripts/apply-sync.mjs --preflight-only; test $? -eq 2` → true; `npx vitest run scripts/apply-sync.test.mjs` → exit 0.
10. W1-exit rehearsal (S13-W1-10, OWNER) recorded with a non-dropping diagrams count.

## 6. Trigger lock

| Phrase | Source | Kept / moved / removed |
|---|---|---|
| "sync the vault" | sync-vault description | kept |
| "/sync-vault" | sync-vault description | kept |
| "push notes to the hub" | sync-vault description | kept |
| "update the database from the vault" | sync-vault description | kept |

No phrase removed or moved; no Thai form exists in the source to carry forward.

## 7. Risks and OD sensitivity

- **The readiness refusal is a behaviour change.** Today a missing Chromium only warns; now it is a hard `exitCode 2` refusal in both `sync:preflight` and `sync:apply` itself. A legitimate text-only sync in a Chromium-less environment now blocks. Mitigated: the refusal names the exact fix, and the cloud environment (I16, S11) is expected to always have Chromium resolvable — this only bites a genuinely broken environment, which is the point (H35). Under OD1-b (claude.ai sync), this refusal is unaffected — a learn-hub-local concern, independent of micky delivery.
- **The `sync:preflight` package.json entry is a shared-file edit (I22, S21).** Mitigated by the step's own no-op-if-present check.
- **The gotchas-verbatim move (W4) depends on S21's map, not yet written.** This spec's candidate list is evidence-based, not authoritative; §8 tracks it.
- **OD5 sensitivity.** Under OD5-b, sync-vault is unaffected — it never decides to run itself; only callers' handoff wording changes (their specs).
- **OD11 sensitivity.** Architecture recommends (b) staged. If W0 check (e) fails, the fallback is `docs/gotchas/*.md` instead of `.claude/rules/*.md` — irrelevant to sync-vault's own `references/gotchas.md`, a skill-owned file either way.

## 8. Open questions

- `ASSUMES: S21's gotcha-map.md assigns the 6 candidate headings (§3 S13-W4-1), possibly plus "DB rows can outlive their /vault source" (CLAUDE.md:1722-1742), to sync-vault's references/gotchas.md — settled by reading that file once written, before S13-W4-1.`
- `ASSUMES: S21's I22 edit list either has not yet added "sync:preflight" by S13-W1-5, or added the identical line — settled by that step's read-before-write check.`
- `ASSUMES: sync-vault needs no dedicated §6.3 live-trigger family — settled by S12 at W3/W4 trigger-lock time; the §4.3 near-miss queries seed that family's set if S12 disagrees.`
- Not verified read-only: whether plain `claude plugin list` (no flags) prints one stable line per plugin, or needs `--json`+parsing to avoid multi-line log noise. `ASSUMES` plain output is fine for a diagnostic line; if too verbose, pipe through `tr '\n' ';'` (already specified) — settled by running it once during S13-W1-10.
- `ARCH-CONFLICT: none found.` The one judgment call beyond a literal quote — `apply-sync.mjs` hard-refusing on missing Chromium, not just warning — is directly supported by architecture §5.7 ("On failure it exits 2"); documented as a behaviour change in §7, not a conflict.
