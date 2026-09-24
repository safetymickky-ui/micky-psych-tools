# Spec S11: Delivery and environment

| Field | Value |
|---|---|
| Repos | micky-psych-tools (`docs/rewrite/`, `scripts/`, `README.md`, `MEMORY.md`), learn-hub (`docs/cloud-env-setup.md`). OWNER actions on the Claude Code cloud environment and on the owner's Windows machine. |
| Units (today → target) | Cloud environment configuration: app variables only, no setup script, `CLAUDE_CODE_PLUGIN_DIRS` unset → adds `LEARN_HUB_DIR`, `MICKY_TOOLS_DIR`, `PUPPETEER_EXECUTABLE_PATH`, `PUPPETEER_SKIP_DOWNLOAD`, the scheduled `CLAUDE_CODE_PLUGIN_DIRS` and a VM-tooling setup script. `CLAUDE_CODE_PLUGIN_DIRS` schedule: none → seven exact values (§2.7 I16.2). `docs/rewrite/delivery-log.md`: absent → new (micky). Cloud setup script: absent → `docs/rewrite/cloud-setup.sh` + the environment field. `ARTICLE_INBOX_DIR`, `BOOK_ROOT`: undefined contract → I27. W0 checklist a–h: unanswered → procedures + recorded answers. Windows route: user-scope marketplace install → user env var from W3 entry (OD2-a). New checker `scripts/delivery_log.py` (+ tests). |
| Waves | W0 (canary + checklist), W1 exit, W2 exit, W3 entry, W5 |
| Owner decisions assumed | OD1-a, OD2-a, OD4-a, OD6-a, OD11-b, OD12-a, OD13-a |
| Defects closed | 0 of 0 assigned (HIGH: none). This spec serves the environment half of H25, H14 and K15 (see §1.4). |
| Interfaces owned | I16, I27 |
| Interfaces consumed | I14 (owner S13), I15 (owner S14), I17 (owner S12) |
| Depends on specs | S10 (W0 `scripts/health.sh`, `bump.py`), S12 (smoke suites, `h-coverage.md`, `baseline.md`), S13 (session-start ready line), S14 (`learn-hub-session`, fork and catalog deletions), S07 (vault-keeper), S03 and S04 (evidence writers), S05 and S06 (renderers), S08 (plugin-creator, W3 validator), S09 (firecrawl), S17 (`ARTICLE_INBOX_DIR`), S20 (`BOOK_ROOT`), S21 (learn-hub `CLAUDE.md` W1 line) |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| path | lines | bytes | est. tokens | role |
|---|---|---|---|---|
| micky `docs/rewrite/delivery-log.md` | — | — | — | absent (created W0) |
| micky `docs/rewrite/cloud-setup.sh` | — | — | — | absent (created W0) |
| micky `scripts/delivery_log.py`, `scripts/test_delivery_log.py` | — | — | — | absent (created W0) |
| micky `scripts/health.sh` | — | — | — | absent today; created by S10 in W0 (I18); this spec adds 2 lines |
| micky `README.md` | 110 | 6,571 | 1,632 | install docs: `/plugin marketplace add` (README.md:10, :20), update by bump (:36-48) |
| micky `MEMORY.md` | 1,153 | 108,178 | 26,717 | delivery fact at MEMORY.md:11 "Installed to Claude Code as marketplace `micky-psych-tools` (user scope)."; Windows toolchain at :1139-1144 |
| micky `CLAUDE.md` | 200 | 13,954 | 3,462 | no delivery pointer today |
| learn-hub `docs/cloud-env-setup.md` | 169 | 8,435 | 2,084 | the cloud environment contract: six app variables (:18-25), where to set them (:100-117), verify (:139-147) |
| learn-hub `.claude/settings.json` | 31 | 652 | 163 | SessionStart (:3-12) + two PreToolUse(Bash) gates (:13-29); read only in single-repo sessions |
| learn-hub `.claude/hooks/session-start.sh` | 92 | 4,759 | 1,182 | remote-only (:8-10); root from `CLAUDE_PROJECT_DIR` or own path (:21-30); writes `PUPPETEER_*` to `CLAUDE_ENV_FILE` (:46-60); `npm install` (:62); ready line (:92) |
| learn-hub `scripts/lib/session-start-hook.test.mjs` | 154 | 7,022 | 1,752 | asserts the `PUPPETEER_*` lines (:119, :133-134) |
| learn-hub `.gitignore` | 73 | 1,341 | 335 | `/Book/` (:48), `raw book/` (:67); no `Raw Article PDF` entry |
| learn-hub `.claude/skills/ingest-article/SKILL.md` | 378 | 28,048 | 6,952 | Windows inbox path in the description (:3) and body (:49); `Glob Raw Article PDF/*.pdf` (:51); `rm "Raw Article PDF/<file>.pdf"` (:348) |
| learn-hub `.claude/skills/vault-coverage/SKILL.md` | 126 | 7,556 | 1,878 | `BOOK_ROOT` precondition (:21-22); `BOOK_ROOT="C:/Users/User/Desktop/Learn"` (:40) |
| learn-hub `scripts/scrape/coverage-baseline.mjs` | 220 | 10,760 | 2,677 | `const BOOK_ROOT = process.env.BOOK_ROOT \|\| REPO;` (:41); same default in `measure-coverage.mjs:38`, `eval-coverage.mjs:46` |
| learn-hub `scripts/lib/coverage-source-io.mjs` | 93 | 4,076 | 1,019 | `source dir missing: <dir>` per book (:58) |

Environment state in this cloud session (probe 2026-09-24; values of secrets not printed):

| item | state |
|---|---|
| `claude --version` | 2.1.281 (`/opt/node22/bin/claude` → `/opt/claude-code/bin/claude`, the binary that runs the session) |
| `HOME`, `PWD`, `CLAUDE_PROJECT_DIR`, `CLAUDE_CODE_REMOTE` | `/root`, `/home/user`, unset, `true` |
| `CLAUDE_CODE_PLUGIN_DIRS`, `LEARN_HUB_DIR`, `MICKY_TOOLS_DIR`, `PUPPETEER_EXECUTABLE_PATH`, `PUPPETEER_SKIP_DOWNLOAD`, `ARTICLE_INBOX_DIR`, `BOOK_ROOT` | all unset |
| `FIRECRAWL_API_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `NEXT_PUBLIC_SUPABASE_URL` | set (the environment already carries app variables and the Firecrawl key) |
| PDF tooling | `import fitz`, `import pypdf`, `import pdfplumber` fail; `pdftoppm`, `pdftotext`, `pdfinfo` absent |
| `firecrawl` CLI | absent; npm `firecrawl-cli` latest 1.24.4 (2026-09-22), bin `firecrawl`, `engines.node >=22.0.0`; node here v22.22.2 |
| Chromium | `/opt/pw-browsers/chromium` → `chromium-1194/chrome-linux/chrome` |
| python | `python3` and `python` = 3.11.15 (`/usr/bin/python3.11`); its pip 24.0 has no `EXTERNALLY-MANAGED` marker (`/usr/lib/python3.12/EXTERNALLY-MANAGED` exists for 3.12 only) |
| apt | package lists present; `poppler-utils` candidate `24.02.0-1ubuntu9.8` |
| network | HEAD probes reach `*.supabase.co` (401), `api.firecrawl.dev` (200), `eutils.ncbi.nlm.nih.gov` (405), `clinicaltrials.gov` (200), `archive.ubuntu.com` (200), `pypi.org` (200) |
| user settings | no `/root/.claude/settings.json`; the session runs with `--settings /root/.claude/launcher-settings.json` (keys `$schema`, `autoMode`, `hooks`, `permissions`) |
| claude.ai-synced skills | 22 dirs under `~/.claude/skills/synced/<id>/` (includes `psych-paper-digest`, `pdf`, `bullet-reconstruct`, `obsidian-knowledge-vault`) |

### 1.2 Descriptions

No skill or command belongs to this spec's units.

### 1.3 Defects

| id | sev | H# | evidence | problem | fix step | wave |
|---|---|---|---|---|---|---|
| — | — | — | — | No inventory defect has a prefix assigned to this spec. | — | — |

### 1.4 Other findings

Inventory OBS lines that touch these units (re-opened in `docs/plugin-rewrite/evidence/defects-digest.txt`):

- :137 learn-hub plugins "INSTALLATION: nothing loads these plugins" → the §2.7 schedule loads them.
- :149 and :214 "PDF TOOLING IS ABSENT in the cloud environment" → confirmed today (§1.1); the setup script installs it.
- :213 "WINDOWS vs CLOUD PATHS" (ingest-article `C:\Users\User\Desktop\Learn\Raw Article PDF`, vault-coverage `BOOK_ROOT="C:/Users/User/Desktop/Learn"`) → I27.
- :301 "Chromium exists only at /opt/pw-browsers" → `PUPPETEER_EXECUTABLE_PATH` set on the environment.
- :50 and :60 probes in a scratch `CLAUDE_CONFIG_DIR` → the same method is used for this spec's probes.

Defects owned by other specs whose environment half this spec provides:

| defect (defect-index.txt line) | owner spec | what S11 provides |
|---|---|---|
| ingest-article-1 (:166, H25) | S17 | I27 `ARTICLE_INBOX_DIR` default and absent behaviour |
| vault-coverage-2 (:207) | S20 | I27 `BOOK_ROOT` default and absent behaviour |
| atomize-book-11 (:162), ingest-slides-3 (:178), ingest-article-8 (:173), pdf-pipeline-5 (:197) | learn-hub pipeline specs | setup script installs PyMuPDF, pypdf, pdfplumber, poppler-utils |
| firecrawl-3 (:66) | the firecrawl spec | `FIRECRAWL_API_KEY` stays an environment value; rule DL10 rejects keys in the log |
| learn-hub-local-1 (:101, H14) | the catalog-retirement spec (W2) | Windows removal step S11-W2-1 |
| vault-keeper-12 (:60) | S07 | `LEARN_HUB_DIR` on both environments |
| README.md (root)-3 (:94) | S10 (W0) | README install section rewritten at W3 (S11-W3-3) |

New facts (probes run for this spec on 2026-09-24, CLI 2.1.281, scratch `CLAUDE_CONFIG_DIR` under `wf3/tmp/S11/`; no repo was changed, `git status --short` stayed empty in micky):

- **N1 (NEW).** A relative entry in `CLAUDE_CODE_PLUGIN_DIRS` is skipped with **no error line**: `claude plugin list --json` printed `[]` and the text form printed "No plugins installed." A `~` entry and a missing absolute path each print `inline[N]: × Path not found: …` and appear in JSON with `"errors"` and `"errorDetails": [{"type": "path-not-found", …}]`. Exit code 0 in all cases.
- **N2 (NEW).** The same path listed twice loads once. The same plugin name from two paths loads twice: the final value `/home/user/micky-psych-tools/plugins:/home/user/learn-hub/plugins` against today's trees lists 22 entries, with `intent-lock@inline`, `pubmed-research-note@inline` and `comprehensive-review@inline` each twice (V2 reconfirmed).
- **N3 (NEW).** `claude plugin list --json` entries carry `id`, `version`, `scope`, `enabled`, `installPath`, and `errors`/`errorDetails` on failure. It ran in 0.41 s.
- **N4 (NEW).** `"defaultEnabled": false` in plugin.json makes an env-var-loaded plugin `"enabled": false` (text: `× disabled`). `claude plugin enable firecrawl@inline` then wrote `"enabledPlugins": {"firecrawl@inline": true}` into the user `settings.json`. See ARCH-CONFLICT 1 in §8.
- **N5 (NEW).** An install from a **local-directory** marketplace is a versioned copy under `<config>/plugins/cache/<marketplace>/<plugin>/<version>`. An edit without a version bump did not reach it through `claude plugin marketplace update` + `claude plugin update` ("already at the latest version (0.0.1)"); after a bump it did ("updated from 0.0.1 to 0.0.2 … Restart to apply"). A refresh at session start was not tested (it needs a session start). See ARCH-CONFLICT 2.
- **N6 (NEW).** An installed `gridgeist@micky-psych-tools` and an env-var `gridgeist@inline` are both listed as enabled.
- **N7 (NEW, W0-c pre-answer).** A many-to-one `renames` map (10 old names → `alignment`, `evidence`, `visuals`) on a scratch copy of the real catalog passed `claude plugin validate --strict` (exit 0). A cycle control failed (exit 1, "chain does not resolve (cycle)").
- **N8 (NEW).** A hooks plugin in shell form (`"command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/mark.sh"`) fails `--strict` (unquoted placeholder warning). Exec form (`"command": "bash", "args": ["${CLAUDE_PLUGIN_ROOT}/hooks/mark.sh"]`) passes. A manifest with a `userConfig` option that has a `default` passes and loads enabled.
- **N9 (NEW).** This multi-repo session (cwd `/home/user`) lists all 11 learn-hub project skills from `.claude/skills/` — the skills half of W0-e is observed.
- **N10 (NEW).** The micky Windows checkout is recorded at `C:\Users\User\Desktop\My skill\micky-psych-tools` (micky `docs/superpowers/plans/2026-07-10-improve-all-plugins.md:11`), a path with a space. The learn-hub main checkout is `C:/Users/User/Desktop/Learn` (learn-hub `docs/handoff-vault-embeddings.md:42`). W0-g confirms both.
- **N11 (NEW).** learn-hub `docs/cloud-env-setup.md:144` recommends `npm run sync` (the full dry emitter) as a verification step. Outside this spec; recorded for S13 (§8 Q9).
- **N12 (NEW).** The cloud-environment documentation (read through the environment docs tool, 2026-09-24) places every setting in one dialog: the cloud environment menu in the session title bar → Edit → "Update cloud environment", with **Environment variables** (`.env` format, `KEY=value` per line, readable by anyone using the environment), **API credentials** (Pro/Max only), **Setup script**, and **Network access** (None, Trusted, Full, Custom + Allowed domains). A setup script runs as root before Claude Code starts, must exit 0 or the session fails to start, should finish within about five minutes, is cached as a filesystem snapshot, and re-runs only when the script or the allowed hosts change or after about seven days. Editing variables affects only sessions started afterwards.

## 2. Target state

### 2.1 Location and tree (after W5)

```
micky-psych-tools/
  docs/rewrite/delivery-log.md      new (W0); rows appended at every schedule point
  docs/rewrite/cloud-setup.sh       new (W0); SETUP_VERSION 1 → 2 at W0 exit; +1 per later change
  scripts/delivery_log.py           new (W0); stdlib only
  scripts/test_delivery_log.py      new (W0); unittest
  scripts/health.sh                 S10's file; +2 lines (W0)
  README.md                         "## Install per environment" replaces the install and update sections (W3)
  MEMORY.md                         delivery fact at line 11 rewritten (W0 after check g; W3)
learn-hub/
  docs/cloud-env-setup.md           new section "### C. Delivery and VM tooling" (W0)
Cloud environment (owner)           variables per I16.1; setup script = docs/rewrite/cloud-setup.sh
Windows (owner)                     user variables MICKY_TOOLS_DIR, LEARN_HUB_DIR, BOOK_ROOT (W0); CLAUDE_CODE_PLUGIN_DIRS (W3); no marketplace installs (W3)
```

### 2.2 Frontmatter

Not applicable: no skill in this spec.

### 2.3 Body outline

Not applicable: no skill body. The two document layouts this spec owns are defined in §2.7: the delivery log (I16.4) and the setup script (I16.6).

### 2.4 References (documents created)

| file | purpose | read when | size target |
|---|---|---|---|
| micky `docs/rewrite/delivery-log.md` | the single record of every delivery change, with previous values for rollback; the W0 checklist answers | before any edit of an environment variable, setup script, or Windows install | grows by rows; each row one line |
| micky `docs/rewrite/cloud-setup.sh` | the canonical setup-script text pasted into the cloud environment | before editing the Setup script field | ≤ 80 lines |
| learn-hub `docs/cloud-env-setup.md` §3C | tells learn-hub readers which delivery variables exist and where their values live | when configuring the cloud environment | ≤ 30 new lines |

### 2.5 Scripts

| name | CLI | input | JSON stdout | exit codes | tests |
|---|---|---|---|---|---|
| `scripts/delivery_log.py` (micky, Python 3 stdlib only) | `check [--log PATH] [--setup PATH] [--strict] [--json]`; `current --env ID [--var NAME] [--log PATH]`; `live [--from FILE\|-] [--env ID] [--expect auto\|a,b,c] [--project-roots A,B] [--strict] [--log PATH]`; `--help` with no side effects. Default `--log` = `<repo of the script>/docs/rewrite/delivery-log.md`; default `--setup` = `<repo of the script>/docs/rewrite/cloud-setup.sh`. `live` without `--from` runs `claude plugin list --json` itself, finding the executable with `shutil.which("claude")` (so `claude.cmd` resolves on Windows). | the log and setup files; `claude plugin list --json` output; env `CLAUDE_CODE_PLUGIN_DIRS`, `LEARN_HUB_DIR`, `MICKY_TOOLS_DIR`; `~/.claude/skills/synced/` | `check`: `{"ok": bool, "rows": int, "errors": [{"rule": "DLn", "row": int\|null, "message": str}], "warnings": [same], "checklist": {"a": "pending\|yes\|no", …}, "current": {"<env>": {"<variable>": "<value>"}}}`. `live`: `{"ok": bool, "entries": int, "loaded": [names], "expected": [names]\|null, "duplicates": [names], "disabled": [ids], "errors": [{"rule": "Ln", "message": str}], "warnings": [same]}`. `current`: the plain value on one line (not JSON). | `check`: 0 no errors (warnings allowed unless `--strict`), 1 rule errors, 2 usage error or unreadable log. `live`: 0 ok, 1 rule errors, 2 usage error, 3 `claude` not found or its output is not a JSON array. `current`: 0 printed, 1 no row for that environment and variable, 2 usage error. | `scripts/test_delivery_log.py` (unittest; fixtures inline or in `tempfile` dirs; no network, no wall clock), cases below |

Rules the script enforces (messages must name the fix, R66):

| rule | subcommand | check |
|---|---|---|
| DL1 | check | sections `## Environments`, `## W0 mechanism checklist`, `## Log` each present exactly once |
| DL2 | check | the Log header equals `\| # \| date \| environment \| variable \| previous \| new \| reason \| evidence \| rollback \|`; every row has 9 cells |
| DL3 | check | `#` runs 1, 2, 3 … with no gap; `date` is `YYYY-MM-DD` and never decreases |
| DL4 | check | environment matches `^(cloud\|windows):[A-Za-z0-9._-]+$` and is listed in `## Environments`; an id containing `<` in that table is a warning ("placeholder not filled") |
| DL5 | check | variable is one of `CLAUDE_CODE_PLUGIN_DIRS`, `LEARN_HUB_DIR`, `MICKY_TOOLS_DIR`, `PUPPETEER_EXECUTABLE_PATH`, `PUPPETEER_SKIP_DOWNLOAD`, `ARTICLE_INBOX_DIR`, `BOOK_ROOT`, `FIRECRAWL_API_KEY`, `setup-script`, `network-access`, `marketplace:<name>`, `installs:<marketplace>`, `enabled:<plugin>@<source>` |
| DL6 | check | `previous` and `new` are each one code span; the value grammar per variable is I16.4 |
| DL7 | check | `previous` equals the `new` of the last earlier row with the same environment and variable (the first row of a pair may hold any value, including `(unrecorded)`) |
| DL8 | check | `CLAUDE_CODE_PLUGIN_DIRS` values: cloud splits on `:`, every segment starts with `/`, no `;`, no backslash; Windows splits on `;`, every segment matches `^[A-Za-z]:\\`, no `:` after the drive; both: no empty segment, no surrounding spaces, no leading `~` (message: "~ resolves to /root in cloud (probe P1)"), no relative segment (message: "Claude Code skips a relative path with no error line (N1)"), no `..` segment, no trailing separator, no segment listed twice |
| DL9 | check | `LEARN_HUB_DIR`, `MICKY_TOOLS_DIR`, `BOOK_ROOT`, `ARTICLE_INBOX_DIR`, `PUPPETEER_EXECUTABLE_PATH`: `(unset)` or one absolute path of the environment's kind |
| DL10 | check | `FIRECRAWL_API_KEY` values are only `(set)` or `(unset)`; no cell matches `fc-[A-Za-z0-9]{8,}`, `sk-[A-Za-z0-9]{8,}`, `eyJ[A-Za-z0-9_-]{10,}` or `service_role` |
| DL11 | check | reason starts with `W0` … `W5`, `probe`, `fix`, or `rollback of #N` |
| DL12 | check | evidence is not empty; `pending` is a warning (an error with `--strict`) |
| DL13 | check | rollback is not empty |
| DL14 | check | checklist rows a–h each present once; answer ∈ {`pending`, `yes`, `no`}; `no` needs "fallback taken"; `yes`/`no` need evidence; `pending` is a warning (an error with `--strict`) |
| DL15 | check | for the latest `CLAUDE_CODE_PLUGIN_DIRS` value of each environment whose kind matches this OS: when every segment exists here, expand it (a segment holding `.claude-plugin/plugin.json` = that plugin's `name`; otherwise each child dir holding one) and fail on any name reached twice; when a segment is absent, a warning "not expanded here" |
| DL16 | check | the setup file exists; `bash -n` on it exits 0 (warning when `bash` is not on PATH) |
| DL17 | check | the setup file has exactly one `SETUP_VERSION=<integer>` line, equal to `<n>` in the latest `setup-script` row (`setup_version=<n>`) of every cloud environment that has one |
| DL18 | check | the setup file contains neither `/home/user/learn-hub` nor `/home/user/micky-psych-tools`, no DL10 secret pattern, and its last non-empty line is `exit 0` |
| DL19 | check `--strict` | once no checklist row is `pending`: no latest cloud value contains `/opt/w0-probe` and the setup file does not contain `w0-probe` |
| L1 | live | no entry has `errors` (path-not-found or any other) |
| L2 | live | each plugin name (the `id` before `@`) appears once; the message lists every `installPath` |
| L3 | live | with `--env`: `$CLAUDE_CODE_PLUGIN_DIRS` equals that environment's latest logged value (warning; error with `--strict`) |
| L4 | live | every `@inline` entry's `installPath` lies under a segment of `$CLAUDE_CODE_PLUGIN_DIRS` (split on `os.pathsep`, compared after `os.path.normcase(os.path.normpath())`) |
| L5 | live | with `--expect`: the enabled, error-free names equal the expected set; a plugin that is present but disabled is reported as "present but disabled (defaultEnabled:false or a user setting)". `auto` = the DL15 expansion of `$CLAUDE_CODE_PLUGIN_DIRS` |
| L6 | live | no `skills/<name>/` of a loaded plugin shares `<name>` with a project skill `<root>/.claude/skills/<name>/`; roots = `--project-roots` or `$LEARN_HUB_DIR,$MICKY_TOOLS_DIR` |
| L7 | live | warning when a loaded plugin skill shares its name with `~/.claude/skills/synced/*/<name>/` |

Test cases in `scripts/test_delivery_log.py` (each a `unittest.TestCase` method; run with `PYTHONDONTWRITEBYTECODE=1`):

1. `test_template_passes_with_pending_warnings`: the exact W0 template (I16.4) → exit 0, 8 DL14 warnings; with `--strict` → 8 DL14 errors.
2. `test_tilde_segment_rejected` → DL8, message contains `/root`.
3. `test_relative_segment_rejected` → DL8, message contains `no error line`.
4. `test_cloud_value_with_semicolon_rejected` → DL8.
5. `test_windows_value_separators`: `C:\a\plugins:C:\b\plugins` → DL8; `C:\Users\User\Desktop\My skill\micky-psych-tools\plugins;C:\Users\User\Desktop\Learn\plugins` → no error.
6. `test_duplicate_segment_rejected` → DL8.
7. `test_chain_break_rejected` → DL7.
8. `test_secret_values_rejected`: `fc-abcdef1234567890` and `service_role` → DL10.
9. `test_unknown_environment_and_variable` → DL4, DL5.
10. `test_reason_evidence_rollback_required` → DL11, DL12, DL13.
11. `test_checklist_no_needs_fallback` → DL14.
12. `test_static_listed_once`: two temp roots each holding a plugin named `dup` → DL15.
13. `test_setup_version_must_match_log` → DL17; `test_setup_repo_paths_rejected` → DL18; `test_setup_last_line_exit_0` → DL18.
14. `test_probe_remnants_fail_strict` → DL19.
15. `test_live_duplicates`: a fixture with two `intent-lock@inline` entries (the N2 shape) → L2.
16. `test_live_path_not_found`: a fixture entry with `"errors": ["Path not found: /root/x (commands)"]` → L1.
17. `test_live_expect_reports_disabled`: `firecrawl@inline` with `"enabled": false` and `--expect firecrawl` → L5 "present but disabled".
18. `test_live_project_skill_collision`: temp project root with `.claude/skills/concept-animation/` and a loaded plugin skill of that name → L6.
19. `test_current_prints_latest_value` and `test_help_has_no_side_effects` (run `--help` in a temp cwd; exit 0; the directory stays empty).

### 2.6 Handoffs (exact sentences other units carry)

1. Every plugin README, from that plugin's W3 rewrite (R52), carries this section verbatim:

   > ## Surfaces
   > - Claude Code cloud sessions: loaded in place through `CLAUDE_CODE_PLUGIN_DIRS` on the cloud environment. Current value and history: micky-psych-tools `docs/rewrite/delivery-log.md`.
   > - Windows: loaded in place through the user environment variable `CLAUDE_CODE_PLUGIN_DIRS`.
   > - claude.ai, Cowork and routines on sessions without the clones: not delivered.

2. micky `CLAUDE.md` after its W3 rewrite (owner of that rewrite: S10, step S10-W3-8; CX-34/CX-49) carries one delivery line: "Delivery: plugins load in place through `CLAUDE_CODE_PLUGIN_DIRS` (cloud environment variable and Windows user variable). Current values, history and rollback: `docs/rewrite/delivery-log.md`."
3. learn-hub `CLAUDE.md`, in the "Claude Code cloud environment" paragraph, when S21-W1-4 edits it (CX-34/CX-49), gains: "Delivery and VM-tooling variables and the setup script: `docs/cloud-env-setup.md` §3C; current values in micky-psych-tools `docs/rewrite/delivery-log.md`."
4. A plugin spec never edits `CLAUDE_CODE_PLUGIN_DIRS`. At the wave where its plugin is scheduled (I16.2), its exit section states, for that plugin: "Ready for cloud delivery: HIGH defects due by this wave closed (<ids>); handoffs carry the §4.2 fallback or target an enabled plugin; no same-named unit elsewhere; smoke suite passed (<result path>)." S11's step for that schedule point makes the one edit.

### 2.7 Interfaces

#### I16 — Delivery (owned)

**I16.1 Variables.** Validation markers are the architecture's (§2.6): learn-hub = `package.json` `"name": "learn-hub"` + `scripts/apply-sync.mjs`; micky = `.claude-plugin/marketplace.json` `"name": "micky-psych-tools"`; vault = `vault/.vault-id`.

| variable | cloud environment | Windows (user variable) | set at | read by |
|---|---|---|---|---|
| `CLAUDE_CODE_PLUGIN_DIRS` | schedule I16.2 | from W3 entry: `C:\Users\User\Desktop\My skill\micky-psych-tools\plugins;C:\Users\User\Desktop\Learn\plugins` (paths confirmed by W0-g) | W0 (cloud), W3 entry (Windows) | Claude Code ≥ 2.1.280 |
| `LEARN_HUB_DIR` | `/home/user/learn-hub` | `C:\Users\User\Desktop\Learn` | W0 | vault-keeper `sink.py`, empty-vault, visuals audit call, learn-hub hooks (I14, I15) |
| `MICKY_TOOLS_DIR` | `/home/user/micky-psych-tools` | `C:\Users\User\Desktop\My skill\micky-psych-tools` | W0 | alignment `ledger.py`, lit-watch, vault-keeper, plugin-creator guard |
| `PUPPETEER_EXECUTABLE_PATH` | `/opt/pw-browsers/chromium` | unset | W0 | mermaid prebake, thumbs, `audit:visual` |
| `PUPPETEER_SKIP_DOWNLOAD` | `1` | unset | W0 | `npm install` of puppeteer |
| `ARTICLE_INBOX_DIR` | unset | unset | never (I27 default applies) | ingest-article |
| `BOOK_ROOT` | unset | `C:\Users\User\Desktop\Learn` | W0 (Windows only) | vault-coverage and its scripts |
| `FIRECRAWL_API_KEY` | existing value, unchanged | existing, unchanged | — | firecrawl CLI, learn-hub `scripts/scrape/fetch-pages.mjs:18`; never written to a file (DL10) |

Existing app variables (`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `REVALIDATE_SECRET`, `APP_URL`, optional `SHARE_TOKEN_SECRET`) stay as learn-hub `docs/cloud-env-setup.md` §1 defines them; this spec does not log or change them. Network access stays at its current setting (N12 probes reach every needed host). If it is ever set to Trusted or Custom, the allowed domains must include `*.supabase.co`, `api.firecrawl.dev`, `eutils.ncbi.nlm.nih.gov`, `clinicaltrials.gov` and the `APP_URL` host, with "Also include default list of common package managers" checked; log the change as variable `network-access`.

**I16.2 `CLAUDE_CODE_PLUGIN_DIRS` schedule.** Exact values; paste them as one line after `CLAUDE_CODE_PLUGIN_DIRS=` in the Environment variables box.

| point | value | condition before the edit | expected plugins (live `--expect`) |
|---|---|---|---|
| before W0 | unset | observed 2026-09-24 | — |
| V0 · W0 probe window | `/home/user/micky-psych-tools/plugins/gridgeist:/opt/w0-probe/hookprobe` | setup script version 1 saved | gridgeist, w0-hookprobe |
| V1 · W0 exit | `/home/user/micky-psych-tools/plugins/gridgeist` | checklist b answered | gridgeist |
| V2 · W1 exit | `/home/user/micky-psych-tools/plugins/gridgeist:/home/user/micky-psych-tools/plugins/vault-keeper:/home/user/micky-psych-tools/plugins/firecrawl:/home/user/micky-psych-tools/plugins/plugin-creator` | checklist a = yes; I16.3 for vault-keeper, firecrawl, plugin-creator | gridgeist, vault-keeper, firecrawl, plugin-creator |
| V3 · W2 step 6a | V2 + `:/home/user/micky-psych-tools/plugins/pubmed-research-note:/home/user/micky-psych-tools/plugins/comprehensive-review:/home/user/micky-psych-tools/plugins/clinical-infographic:/home/user/micky-psych-tools/plugins/ml-concept-lab:/home/user/micky-psych-tools/plugins/code-explainer` | I16.3 for the five | V2 + the five |
| V4 · W2 step 6b | V3 + `:/home/user/micky-psych-tools/plugins/concept-animation` | micky concept-animation W2 rewrite merged; learn-hub branch deleting `.claude/skills/concept-animation` pushed | V3 + concept-animation |
| V5 · W2 step 6c (W2 exit value) | V4 + `:/home/user/learn-hub/plugins` | `ls /home/user/learn-hub/plugins` prints only `learn-hub-session`; `/home/user/learn-hub/.claude-plugin/` absent; checklist b = yes | V4 + learn-hub-session |
| V6 · W3 entry (final) | `/home/user/micky-psych-tools/plugins:/home/user/learn-hub/plugins` | W2 exit gates passed | `auto` (15 before the W3 skeleton PR: 14 micky + learn-hub-session; 8 after it) |
| W5 | V6 unchanged | — | `auto` |

Measured lengths: V0 70, V1 46, V2 195, V3 473, V4 528, V5 557, V6 65 characters; all pass DL8 (prototype, 2026-09-24). V4 loaded exactly its 10 plugins with no errors against today's tree.

If checklist b = no: skip V5; V6 becomes `/home/user/micky-psych-tools/plugins`, and the Windows value becomes `C:\Users\User\Desktop\My skill\micky-psych-tools\plugins`. If checklist a = no: stop at V1, do not make any later cloud edit, and re-ask OD1 before W1 exit (architecture §10 W0 exit).

**I16.3 Enablement conditions (architecture §2.7), made checkable.** Before a schedule point adds a plugin, all four hold:

1. HIGH defects: at a wave **exit**, every Appendix A defect of the plugin assigned to that wave or an earlier one is `closed` in `docs/rewrite/h-coverage.md` (for a split row such as H10 "W1/W2", the part assigned to that wave); at **W3 entry**, those assigned to W2 or earlier. Command: `grep -E '^\| (H08\|H09) ' docs/rewrite/h-coverage.md` shows `closed` on each line (ids per plugin from architecture Appendix A). See §8 ARCH-CONFLICT 4.
2. Handoffs: `grep -rn '(OPTIONAL)' plugins/<p>/skills` shows the §4.2 fallback sentence at every cross-plugin handoff, or the plugin has none, or the target is already in the value.
3. No same-named unit elsewhere: after the edit, `live` passes L2 and L6 (and DL15 passes before the edit).
4. Smoke: `bash scripts/eval.sh --smoke <p>` (I17, owner S12) passed for the plugin; its result path goes into the evidence cell.

**I16.4 `docs/rewrite/delivery-log.md` format.** The file is created with exactly this text (the W0 template):

```markdown
# Delivery log

One row per change to how plugins and VM tooling reach an environment, newest last.
To roll back row N: set the same variable in the same environment to row N's `previous`
value, then append a row whose reason is `rollback of #N`.

Format owner: spec S11 (interface I16). Check: `python3 scripts/delivery_log.py check`
(scripts/health.sh runs it). Setup script text: `docs/rewrite/cloud-setup.sh`.

## Environments

| id | configured at | network access |
|---|---|---|
| `cloud:<id>` | claude.ai/code, cloud environment menu in the session title bar, environment `<name>`, Edit | `<level>` |
| `windows:<host>` | user environment variables on `<host>` (`$env:COMPUTERNAME`), set with PowerShell | n/a |

## W0 mechanism checklist

| check | question | answer | evidence | date | fallback taken |
|---|---|---|---|---|---|
| a | Does a new platform-started multi-repo session load `gridgeist@inline`? | pending | | | |
| b | Do a probe plugin's SessionStart and PreToolUse(Bash) hooks fire in that session? | pending | | | |
| c | Does a many-to-one `renames` map validate on a scratch copy of the real catalog? | pending | | | |
| d | Is `claude plugin eval` enabled on the account, with an http MCP mock answering? | pending | | | |
| e | Do learn-hub `.claude/skills` load, and does a `.claude/rules` file with `paths:` load, in a multi-repo session? | pending | | | |
| f | Does `/doctor` report the listing cost, without overflow, in a multi-repo session? | pending | | | |
| g | Windows: CLI at least 2.1.280, micky source type, learn-hub-local state, and does the variable load a canary? | pending | | | |
| h | Does the setup script run before the repos are cloned? | pending | | | |

## Log

| # | date | environment | variable | previous | new | reason | evidence | rollback |
|---|---|---|---|---|---|---|---|---|
```

Value grammar (DL6), one code span per cell:

| variable | allowed values |
|---|---|
| `CLAUDE_CODE_PLUGIN_DIRS` | `(unset)`, `(unrecorded)` (first row only), or a path list (DL8) |
| path variables (DL9) | `(unset)`, `(unrecorded)`, or one absolute path |
| `PUPPETEER_SKIP_DOWNLOAD` | `(unset)` or `1` |
| `FIRECRAWL_API_KEY` | `(set)` or `(unset)` |
| `setup-script` | `(none)`, `(unrecorded)`, or `setup_version=<n>` |
| `network-access` | `none`, `trusted`, `full`, `custom` |
| `marketplace:<name>` | `(absent)`, `directory:<path>`, `github:<owner>/<repo>`, `git:<url>` |
| `installs:<marketplace>` | `(none)` or comma-separated plugin names |
| `enabled:<plugin>@<source>` | `(unset)`, `true`, `false` |

Evidence cell: the session URL printed by `echo "https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID/#cse_/session_}"` plus the command and its key output, or for Windows "PowerShell <date>: <command> → <result>".

**I16.5 Checker.** `scripts/delivery_log.py`, defined in §2.5. `scripts/health.sh` runs `check` (fast, pure parsing) and the unit tests on every commit through `.githooks/pre-commit`.

**I16.6 Setup script.** `docs/rewrite/cloud-setup.sh` version 1 is exactly:

```bash
#!/bin/bash
# Cloud environment setup script for sessions that clone micky-psych-tools and learn-hub.
# Canonical copy: micky-psych-tools/docs/rewrite/cloud-setup.sh (spec S11, interface I16).
# Paste this whole file into the environment's "Setup script" field, then add a
# delivery-log row (variable setup-script) with the SETUP_VERSION below.
#
# Rules for this file:
# - VM tooling only. It may run before the repos are cloned, so nothing here reads
#   or writes /home/user/<repo>.
# - Every step is non-fatal: a non-zero exit stops the session from starting.
# - Output goes to /var/log/cloud-setup.log (kept in the environment cache).
SETUP_VERSION=1
LOG=/var/log/cloud-setup.log
exec >>"$LOG" 2>&1
echo "== cloud-setup start $(date -u +%Y-%m-%dT%H:%M:%SZ) setup_version=$SETUP_VERSION user=$(id -un)"
echo "-- /home/user at setup time (W0 check h: are the repos cloned yet?)"
ls -la /home/user || true
echo "-- tools: python3=$(command -v python3 || echo none) npm=$(command -v npm || echo none)"

# 1. PDF libraries for the python3 that learn-hub's scripts call.
python3 -m pip install --quiet --no-input pymupdf pypdf pdfplumber \
  || python3 -m pip install --quiet --no-input --break-system-packages pymupdf pypdf pdfplumber \
  || echo "WARN step 1 failed: pip install pymupdf pypdf pdfplumber"

# 2. poppler-utils: pdftoppm, pdftotext, pdfinfo.
apt-get install -y -qq poppler-utils \
  || { apt-get update -qq && apt-get install -y -qq poppler-utils; } \
  || echo "WARN step 2 failed: apt-get install -y poppler-utils"

# 3. Firecrawl CLI, pinned (OD12-a). Change the pin only together with a delivery-log row.
NPM="$(command -v npm || true)"
if [ -z "$NPM" ] && [ -x /opt/node22/bin/npm ]; then NPM=/opt/node22/bin/npm; fi
if [ -n "$NPM" ]; then
  "$NPM" install -g --no-audit --no-fund firecrawl-cli@1.24.4 \
    || echo "WARN step 3 failed: npm install -g firecrawl-cli@1.24.4"
else
  echo "WARN step 3 skipped: npm not found"
fi

# 4. Sandbox backend for eval runs that grant Bash: without bubblewrap and socat,
#    claude plugin eval refuses each Bash-granted run (eval-format.md:195; critique C2-02).
apt-get install -y -qq bubblewrap socat \
  || { apt-get update -qq && apt-get install -y -qq bubblewrap socat; } \
  || echo "WARN step 4 failed: apt-get install -y bubblewrap socat"

# --- W0 probe block (checks b and U7). Delete this block at W0 exit (set SETUP_VERSION=2). ---
P=/opt/w0-probe/hookprobe
mkdir -p "$P/.claude-plugin" "$P/hooks"
cat >"$P/.claude-plugin/plugin.json" <<'EOF'
{"name":"w0-hookprobe","version":"0.0.1","description":"W0 probe: records whether plugin SessionStart and PreToolUse(Bash) hooks fire and whether a userConfig default reaches the hook.","author":{"name":"W0 probe"},"keywords":["probe"],"userConfig":{"probe_dir":{"type":"directory","title":"Probe directory","description":"W0 check U7: is a userConfig default visible to an env-var-loaded plugin?","default":"/tmp"}}}
EOF
cat >"$P/hooks/hooks.json" <<'EOF'
{"hooks":{"SessionStart":[{"hooks":[{"type":"command","command":"bash","args":["${CLAUDE_PLUGIN_ROOT}/hooks/mark.sh"],"timeout":10}]}],"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"bash","args":["${CLAUDE_PLUGIN_ROOT}/hooks/pre.sh"],"timeout":10}]}]}}
EOF
cat >"$P/hooks/mark.sh" <<'EOF'
#!/bin/bash
echo "SessionStart $(date -u +%FT%TZ) root=${CLAUDE_PLUGIN_ROOT:-unset} project=${CLAUDE_PROJECT_DIR:-unset} pwd=$PWD env_file=${CLAUDE_ENV_FILE:-unset} remote=${CLAUDE_CODE_REMOTE:-unset} option_probe_dir=${CLAUDE_PLUGIN_OPTION_PROBE_DIR:-unset}" >>/tmp/w0-hookprobe.log
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then echo "export W0_PROBE_ENV=1" >>"$CLAUDE_ENV_FILE"; fi
exit 0
EOF
cat >"$P/hooks/pre.sh" <<'EOF'
#!/bin/bash
echo "PreToolUse $(date -u +%FT%TZ)" >>/tmp/w0-hookprobe.log
exit 0
EOF
# --- end of W0 probe block ---

echo "-- versions"
python3 -c "import importlib.metadata as m; print({p: m.version(p) for p in ('pymupdf', 'pypdf', 'pdfplumber')})" || true
pdftoppm -v 2>&1 | head -n 1 || true
command -v bwrap socat || true
"$(dirname "${NPM:-/opt/node22/bin/npm}")/firecrawl" --version || true
echo "== cloud-setup end $(date -u +%Y-%m-%dT%H:%M:%SZ) setup_version=$SETUP_VERSION"
exit 0
```

Version 2 (W0 exit) = version 1 with `SETUP_VERSION=2` and every line from `# --- W0 probe block` through `# --- end of W0 probe block ---` deleted. Checked on 2026-09-24: version 1 passes `bash -n`; its probe block, run with `P` redirected into a scratch dir, produced a plugin that passes `claude plugin validate --strict`. Why each command has this form: `python3` is the interpreter the repo scripts call (§1.1), its pip is not PEP 668 locked, and the `--break-system-packages` retry covers an image where it is; package lists exist, so `apt-get update` runs only when the install fails; npm's global prefix is `/opt/node22`, which is on the session PATH. Nothing in it touches a clone, so it is correct whether it runs before or after the clone (U2).

**I16.7 W0 mechanism checklist procedures.** Record each answer in the checklist table (answer, evidence, date, fallback taken) and commit the log. Sessions below are started by the owner from claude.ai/code in the cloud environment, with both repositories unless stated.

| # | procedure (exact) | evidence to capture | pass ("yes") | fallback on "no" |
|---|---|---|---|---|
| a | 1. In a new multi-repo session: `echo "$CLAUDE_CODE_PLUGIN_DIRS"; claude plugin list --json \| python3 -c 'import json,sys; d=json.load(sys.stdin); print(sorted(e["id"] for e in d)); print([e["id"] for e in d if e.get("errors")])'`. 2. Ask the session: "List every skill you can invoke right now whose name contains gridgeist, exactly as named in your skill list." 3. (a2) In a new session with **only learn-hub**: `pwd; ls -d /home/user/*; claude plugin list --json`. | session URLs; the printed id lists; the skill name quoted; a2 `pwd` and the `path-not-found` entry | step 1 prints `['gridgeist@inline', 'w0-hookprobe@inline']` and `[]`; step 2 names `gridgeist:gridgeist` (or `gridgeist`). a2 is recorded, not pass/fail: `pwd` should be `/home/user/learn-hub`, and the gridgeist path shows `path-not-found` with exit 0 | stop all later cloud edits; re-ask OD1 before W1 exit; under OD1-b see §7 |
| b | In the session of (a): `cat /tmp/w0-hookprobe.log; echo "W0_PROBE_ENV=${W0_PROBE_ENV:-unset}"`. The owner also notes whether a "Probe directory" prompt appeared at session start (U7). | the log lines (they record `project=`, `pwd=`, `env_file=`, `option_probe_dir=`); the `W0_PROBE_ENV` value; the prompt observation | the log holds at least one `SessionStart` line and at least one `PreToolUse` line. Record separately: `W0_PROBE_ENV=1` means a plugin hook's `CLAUDE_ENV_FILE` export persists; `option_probe_dir=/tmp` means a `userConfig` default reaches an env-var-loaded plugin (U7) | no hooks plugin: S14 does not build `learn-hub-session`; session duties come from the setup script, the environment variables and the preflight refusal text (S13); skip V5 (I16.2) |
| c | Executor, any machine, in a scratch dir `$S`: `mkdir -p $S/.claude-plugin && cp .claude-plugin/marketplace.json $S/.claude-plugin/`; edit the copy so `plugins` holds the 4 kept entries plus `alignment`, `evidence`, `visuals` (source `./plugins/<name>`), with `renames` mapping intent-lock, decision-interview, plan-critique → alignment; pubmed-research-note, comprehensive-review, psych-paper-digest → evidence; clinical-infographic, concept-animation, ml-concept-lab, code-explainer → visuals; create `$S/plugins/<name>/.claude-plugin/plugin.json` for each of the 7 entries (`name`, `version`, `description`, `author`); run `CLAUDE_CONFIG_DIR=$S/cfg claude plugin validate --strict $S`. Control: set `renames.alignment` to `intent-lock` and re-run. | both exit codes and the error text of the control | exit 0, and the control exits 1 with "chain does not resolve (cycle)". Pre-answered yes on 2026-09-24 (N7); W0 re-runs it on the W0-day catalog | omit `renames` in S10's W3 skeleton; record the old → new mapping in README |
| d | Executor in a scratch dir `$E` (outside both repos): create `$E/.claude-plugin/plugin.json` `{"name":"w0-evalprobe","version":"0.0.1","description":"W0-d probe: checks that claude plugin eval runs and an http MCP mock answers.","author":{"name":"W0 probe"},"keywords":["probe"]}`; `$E/.mcp.json` `{"mcpServers":{"probe":{"type":"http","url":"https://example.invalid/mcp"}}}`; `$E/evals/mocks/probe/ping.md` with body `pong-7Q2`; `$E/evals/ping-case/prompt.md` with frontmatter `max_turns: 5`, `tags: [smoke]`, `runs: 1` and body "Call the ping tool of the probe MCP server once and reply with exactly what it returned."; graders `called-ping.md` (`type: tool_used`, `tool: mcp__plugin_w0-evalprobe_probe__ping`, `min: 1`) and `echoed.md` (`type: regex`, `pattern: pong-7Q2`, `target: last_message`). Run `claude plugin validate --strict $E`, then `claude plugin eval $E --ablation none --runs 1 --max-cost-usd 0.50 --no-publish --trust-plugin --json $E/w0d.json`. Then the sandbox-and-scaffold canary (critique C2-01, C2-02): add `$E/evals/bash-scaffold-case/` with `case.yaml` `context: {scaffold_script: s.sh}`, `s.sh` = `echo seeded > sentinel.txt`, prompt "Run `echo ok > done.txt`, then reply done.", graders `file_exists` on `sentinel.txt` and on `done.txt`; run `claude plugin eval $E --case bash-scaffold-case --scaffold --allow-tools "Bash(echo *)" --ablation none --runs 1 --max-cost-usd 0.50 --no-publish --trust-plugin --json $E/w0d2.json`. | exit codes; the pass/fail of both graders from `$E/w0d.json`; both canary graders from `$E/w0d2.json`; any "not enabled" or "no sandbox backend" message | validate exits 0 (pre-checked 2026-09-24), the eval exits 0 and both graders pass; the canary passes both `file_exists` graders (a refused run means setup step 4 did not install bubblewrap/socat; a missing `sentinel.txt` means the scaffold did not run) | skill-creator runner for behavioural cases (S12); static and unit layers unchanged |
| e | 1. Push a learn-hub branch `w0/rules-probe` whose only change adds `.claude/rules/w0-probe.md` (content in step S11-W0-6). 2. Start a multi-repo session with learn-hub on that branch. 3. Ask: "Without opening any file: is a rule that mentions a W0-e verification word in your context? Answer none, or quote the word exactly." 4. Then: "Read the first 5 lines of /home/user/learn-hub/src/lib/toc.ts. Is a rule that mentions a W0-e verification word in your context now? Answer none, or quote the word exactly." 5. Ask: "Can you invoke skills named sync-vault, atomize-book and ingest-article? Answer yes or no for each." | session URL; the three answers verbatim | question 4 quotes `TANGERINE-4F2C` and question 5 is yes for all three. Record question 3 too: a quote there means the rule loads without a path match | app gotchas go to `docs/gotchas/*.md` with a pointer index in CLAUDE.md (S21) |
| f | In the session of (a), type `/doctor`; copy the lines about the skill listing (cost, budget, overflow) into S12's `docs/rewrite/baseline.md`. On Windows, `/skill-doctor` is recorded later (W5). | the copied lines; the baseline.md section | `/doctor` runs and shows the listing cost with no overflow | record only: an overflow or an unavailable `/doctor` sets the W3/W4 description budget (S12) |
| g | Owner, PowerShell on Windows: I16.8 step G1 | the outputs listed in G1 | version ≥ 2.1.280 and the canary loads | stay on the marketplace install (OD2-b); see §7 and ARCH-CONFLICT 2 |
| h | In the session of (a): `head -n 20 /var/log/cloud-setup.log` | the `/home/user` listing written by the setup script | record only: "yes" when `learn-hub` and `micky-psych-tools` are absent from that listing (the script ran before the clone), "no" when present | none needed: the script is correct either way (I16.6) |

**I16.8 Windows route (OD2-a).** Run in PowerShell. `$M` and `$L` are the checkouts confirmed in G1.

G1 — W0 check g (read-only apart from one process-scope variable):

```powershell
claude --version
claude plugin marketplace list --json
claude plugin list --json
$M = 'C:\Users\User\Desktop\My skill\micky-psych-tools'
$L = 'C:\Users\User\Desktop\Learn'
Select-String -Path "$M\.claude-plugin\marketplace.json" -Pattern '"name": "micky-psych-tools"' -SimpleMatch
Select-String -Path "$L\package.json" -Pattern '"name": "learn-hub"' -SimpleMatch
Test-Path "$L\scripts\apply-sync.mjs"
# Stale-copy check: does each installed micky copy match the checkout?
foreach ($p in (claude plugin list --json | ConvertFrom-Json | Where-Object { $_.id -like '*@micky-psych-tools' })) {
  $name = $p.id.Split('@')[0]
  Get-ChildItem -Path (Join-Path $p.installPath 'skills') -Recurse -Filter SKILL.md | ForEach-Object {
    $rel = $_.FullName.Substring($p.installPath.Length)
    $src = Join-Path "$M\plugins\$name" $rel
    $same = (Test-Path $src) -and ((Get-FileHash $_.FullName).Hash -eq (Get-FileHash $src).Hash)
    '{0}{1} same={2}' -f $name, $rel, $same
  }
}
# Toolchain facts for the learn-hub npm scripts and hooks (critique F9):
python3 --version; python --version; py -3 --version; bash --version
npm config get script-shell
# Canary in this window only (process scope; nothing persists):
$env:CLAUDE_CODE_PLUGIN_DIRS = "$M\plugins\gridgeist;C:\w0-no-such-dir\plugins"
claude plugin list --json
Remove-Item Env:\CLAUDE_CODE_PLUGIN_DIRS
```

Evidence: the version; each marketplace's `name`, `source` and `path`/`repo`; whether `learn-hub-local` appears in either list; every installed `id` and `installPath`; the `same=` lines; the canary JSON. Pass: version ≥ 2.1.280, and the canary JSON has `gridgeist@inline` with `installPath` = `$M\plugins\gridgeist` and an `inline[1]` entry whose `errorDetails.type` is `path-not-found` for `C:\w0-no-such-dir\plugins` (this proves the `;` split with a real path that contains a space). If `$M` or `$L` fail their marker check, find the right paths with `git -C <candidate> remote -v` and use those everywhere below.

G2 — W0, after G1 passes (persistent user variables; no plugin-loading change):

```powershell
[Environment]::SetEnvironmentVariable('MICKY_TOOLS_DIR', $M, 'User')
[Environment]::SetEnvironmentVariable('LEARN_HUB_DIR', $L, 'User')
[Environment]::SetEnvironmentVariable('BOOK_ROOT', $L, 'User')
# open a NEW PowerShell window, then:
$env:MICKY_TOOLS_DIR; $env:LEARN_HUB_DIR; $env:BOOK_ROOT
```

G3 — W1 exit and W2 exit, until W3 (installs are cache copies, N5, so only released versions arrive):

```powershell
claude plugin marketplace update micky-psych-tools
foreach ($p in (claude plugin list --json | ConvertFrom-Json | Where-Object { $_.id -like '*@micky-psych-tools' })) { claude plugin update $p.id --scope $p.scope }
# restart Claude Code, then:
claude plugin list --json | ConvertFrom-Json | Select-Object id, version
```

Pass: each listed version equals the `version` in `$M\plugins\<name>\.claude-plugin\plugin.json` on `origin/master` (for a GitHub source, after the wave merge is pushed).

G4 — W2, only if G1 found `learn-hub-local`, before the catalog-deletion commit:

```powershell
foreach ($p in (claude plugin list --json | ConvertFrom-Json | Where-Object { $_.id -like '*@learn-hub-local' })) { claude plugin uninstall $p.id --scope $p.scope }
claude plugin marketplace remove learn-hub-local
claude plugin marketplace list --json
```

G5 — W3 entry, the switch (set the variable first, verify, then uninstall; ARCH-CONFLICT 3):

```powershell
claude plugin list --json | Out-File -Encoding utf8 "$env:USERPROFILE\w3-plugin-list-before.json"
claude plugin marketplace list --json | Out-File -Encoding utf8 "$env:USERPROFILE\w3-marketplace-list-before.json"
[Environment]::SetEnvironmentVariable('CLAUDE_CODE_PLUGIN_DIRS', "$M\plugins;$L\plugins", 'User')
# open a NEW PowerShell window ($M and $L again), then check that the @inline copies load:
claude plugin list --json
foreach ($p in (claude plugin list --json | ConvertFrom-Json | Where-Object { $_.id -like '*@micky-psych-tools' })) { claude plugin uninstall $p.id --scope $p.scope }
claude plugin marketplace remove micky-psych-tools
cd $M
python scripts\delivery_log.py live --env windows:$env:COMPUTERNAME --expect auto --project-roots "$L,$M"
```

Pass: `"ok": true`; no `@micky-psych-tools` id remains. Keep `$M` and `$L` on `master` from now on and do rewrite work in a separate worktree (`git worktree add ..\micky-psych-tools-wip <branch>`), because whatever is checked out there is live in every Windows session (K9).

G6 — rollback of the switch, before the W3 skeleton merges (after it, set the variable back instead; the old plugin names no longer exist on master):

```powershell
[Environment]::SetEnvironmentVariable('CLAUDE_CODE_PLUGIN_DIRS', $null, 'User')
claude plugin marketplace add '<source recorded in G1: the directory path or owner/repo>'
foreach ($n in '<names from the W3 installs row>'.Split(',')) { claude plugin install "$n@micky-psych-tools" --scope user }
```

**I16.9 Rollback.** Cloud: open the environment (menu in the session title bar → Edit), set the variable to the row's `previous` value (delete the line for `(unset)`), Save changes, start a new session, run `live` with the previous expected set, append a row `rollback of #N`. Setup script: paste `git show <commit>:docs/rewrite/cloud-setup.sh` of the previous version. Windows: `[Environment]::SetEnvironmentVariable('<NAME>', '<previous>', 'User')` (`$null` for `(unset)`), new window, `live`. A wave rollback (architecture §7) = `git revert` of the wave merge + this procedure for the rows the wave added.

**I16.10 Consumer obligations.** Only S11 steps edit environment variables, the setup script or Windows installs, and every such edit adds a log row in the same step. A spec whose plugin joins the value writes the §2.6 item 4 readiness sentence at its wave exit. A spec that needs a new variable or a new VM tool asks S11 (a new I16.1 row or setup-script version); it never edits the environment itself.

#### I27 — `ARTICLE_INBOX_DIR` and `BOOK_ROOT` (owned)

**`ARTICLE_INBOX_DIR`** (consumer: ingest-article, S17)
- Meaning: the drop folder whose PDFs ingest-article surveys on a bare invocation.
- Resolution, in order: (1) `$ARTICLE_INBOX_DIR` when set and absolute (a relative value is ignored with the warning "ARTICLE_INBOX_DIR must be absolute; using the default"); (2) `<learn-hub root>/Raw Article PDF`, where `<learn-hub root>` = `$LEARN_HUB_DIR` when its marker validates, else the top of the checkout that holds the skill (`git -C "${CLAUDE_SKILL_DIR}" rev-parse --show-toplevel`).
- Values: cloud unset; Windows unset (the default is `C:\Users\User\Desktop\Learn\Raw Article PDF`, the owner's existing folder).
- The default folder is gitignored: learn-hub `.gitignore` gains the line `/Raw Article PDF/` (S17's W1 step; absent today, §1.1).
- Absent behaviour: when the resolved folder does not exist, print `inbox <path> does not exist — nothing to ingest` and stop without creating it; when it holds no `*.pdf`, print `inbox <path> is empty` and stop. With PDFs present, a bare invocation lists them and asks before ingesting or deleting (H25, S17); a headless run lists them and stops.
- Deletion scope: only a PDF whose resolved absolute path is inside the resolved folder, and only after its row is verified (S17).

**`BOOK_ROOT`** (consumer: vault-coverage, S20)
- Meaning: the directory that holds `Book/` and `raw book/` (gitignored source text, `.gitignore:48`, `:67`).
- Default when unset: the root of the learn-hub checkout that runs the scripts, as today (`coverage-baseline.mjs:41`, `measure-coverage.mjs:38`, `eval-coverage.mjs:46`: `process.env.BOOK_ROOT || REPO`). No script change.
- Values: cloud unset (the source text never reaches a cloud VM); Windows `C:\Users\User\Desktop\Learn` (set at W0, G2), so a worktree run finds the main checkout's `Book\`.
- Absent behaviour (vault-coverage precondition, S20): let `<root>` = `$BOOK_ROOT` or the checkout root; when neither `<root>/Book` nor `<root>/raw book` is a directory, report exactly one finding line `Book/ absent — cannot run here (BOOK_ROOT=<value, or "unset → <root>">)` and stop before any coverage script runs; write no report file. When at least one exists, run as today; a book whose `dir` is missing keeps its per-book `source dir missing` row (`coverage-source-io.mjs:58`).
- The skill text carries no Windows path: vault-coverage SKILL.md:40 changes to a command without `BOOK_ROOT="C:/…"` (S20).

#### Consumed interfaces

- **I14 (owner S13).** ASSUMES: from W1, `.claude/hooks/session-start.sh` resolves its root from `LEARN_HUB_DIR` first (set here at W0), keeps writing the `PUPPETEER_*` exports to `CLAUDE_ENV_FILE` (harmless duplicates of I16.1), and its ready line prints `claude --version` and the `claude plugin list` ids, so a duplicate or a `path-not-found` is visible at every session start — S13 to confirm.
- **I15 (owner S14).** ASSUMES: the plugin directory is `/home/user/learn-hub/plugins/learn-hub-session` with `.claude-plugin/plugin.json` `name` = `learn-hub-session`; its hooks use exec form (N8); it is created in W2 before step V5; it is built only if checklist b = yes — S14 to confirm.
- **I17 (owner S12).** ASSUMES: `bash scripts/eval.sh --smoke <plugin>` exits 0 on pass and writes a JSON result whose path goes into the evidence cell; `docs/rewrite/h-coverage.md` has one row per H id starting `| H<nn> |` with the word `closed` when done; `docs/rewrite/baseline.md` has a section for `/doctor` output — S12 to confirm.
- **I18 (owner S10), not listed in the registry for this spec but touched.** ASSUMES: `scripts/health.sh` exists before S11-W0-3 and accepts two more lines in its fast path — S10 to confirm.

## 3. Change steps

Notation: `<id>` = the cloud environment id chosen in S11-W0-5 (for example `main`); `<host>` = `$env:COMPUTERNAME`; V0–V6 = I16.2 values; "new session" = a session the owner starts from claude.ai/code in the cloud environment, with both repos, on the default branches unless stated. Log rows use the I16.4 grammar; `<URL>` = the session URL command in I16.4.

### W0

**S11-W0-1 · micky · add the delivery-log checker**
- Depends on: none.
- Files: create `scripts/delivery_log.py`, `scripts/test_delivery_log.py`.
- Change: implement §2.5 exactly (CLI, rules DL1–DL19 and L1–L7, JSON, exit codes, 19 test cases). Stdlib only. UTF-8 output with a trailing newline. No writes anywhere.
- Commands: `python3 scripts/delivery_log.py --help` ; `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_delivery_log.py' -v`
- Done when: the unittest run ends with `OK` and runs ≥ 19 tests; `--help` exits 0 and `git status --short` shows only the two new files.
- Rollback: `git revert <this commit>`.

**S11-W0-2 · micky · add the delivery log and the setup script**
- Depends on: S11-W0-1.
- Files: create `docs/rewrite/delivery-log.md` (I16.4 template, verbatim) and `docs/rewrite/cloud-setup.sh` (I16.6 version 1, verbatim).
- Commands: `bash -n docs/rewrite/cloud-setup.sh` ; `python3 scripts/delivery_log.py check`
- Done when: `bash -n` exits 0; `check` exits 0 with exactly 8 DL14 warnings and 2 DL4 placeholder warnings.
- Rollback: `git revert <this commit>`.

**S11-W0-3 · micky · run the checker in health.sh**
- Depends on: S11-W0-2, S10-W0-9.
- Files: edit `scripts/health.sh`.
- Change: add to the fast path, next to the other script tests:
  `python3 scripts/delivery_log.py check >/dev/null || fail "delivery log: run python3 scripts/delivery_log.py check"` and
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_delivery_log.py' -q || fail "delivery_log tests"`
  (use S10's own failure helper if it is not named `fail`).
- Commands: `bash scripts/health.sh --fast`
- Done when: health prints its success line; `grep -c 'delivery_log.py check' scripts/health.sh` prints `1`.
- Rollback: `git revert <this commit>`.

**S11-W0-4 · learn-hub · document the delivery variables**
- Depends on: none.
- Files: edit `docs/cloud-env-setup.md`.
- Change: (1) in §3A, after the bullet "`SHARE_TOKEN_SECRET`  ← optional here …" (line 112), add the bullet "- the delivery and VM-tooling variables in §3C below". (2) Insert before `### B. Vercel (the live deployment)` (line 119):

  ```markdown
  ### C. Delivery and VM tooling

  These live on the same cloud environment. Every change to them is recorded in
  micky-psych-tools `docs/rewrite/delivery-log.md`, which holds the current
  `CLAUDE_CODE_PLUGIN_DIRS` value. Do not copy that value here.

  | Variable | Value on the cloud environment | Why |
  |---|---|---|
  | `LEARN_HUB_DIR` | `/home/user/learn-hub` | root for hooks and skills; multi-repo sessions start in `/home/user` |
  | `MICKY_TOOLS_DIR` | `/home/user/micky-psych-tools` | root for micky plugins that write to that repo |
  | `PUPPETEER_EXECUTABLE_PATH` | `/opt/pw-browsers/chromium` | mermaid prebake, thumbs and `audit:visual`, even when no SessionStart hook runs |
  | `PUPPETEER_SKIP_DOWNLOAD` | `1` | `npm install` skips the Chrome download |
  | `CLAUDE_CODE_PLUGIN_DIRS` | see the delivery log | which plugin directories load |
  | `ARTICLE_INBOX_DIR`, `BOOK_ROOT` | not set | ingest-article uses `Raw Article PDF/`; vault-coverage reports that `Book/` is absent |

  The environment's **Setup script** field holds micky-psych-tools
  `docs/rewrite/cloud-setup.sh`: PyMuPDF, pypdf, pdfplumber, poppler-utils and a pinned
  firecrawl-cli. It installs VM tooling only. Repo steps (`npm install`, `.env.local`)
  stay in `.claude/hooks/session-start.sh`.
  ```
- Commands: `grep -n '^### C. Delivery and VM tooling' docs/cloud-env-setup.md` ; `npm test -- --run scripts/lib/session-start-hook.test.mjs`
- Done when: the grep prints one line; the test passes (the hook is unchanged).
- Rollback: `git revert <this commit>`.

**S11-W0-5 · OWNER (+ micky log commit) · configure the cloud environment**
- Depends on: S11-W0-2 pushed to the W0 branch (the owner copies the setup script text from it).
- Actions (owner, claude.ai/code): open any session in the environment → the cloud environment menu in the session title bar → the environment → Edit.
  1. Note the environment name and the Network access level. Choose an id (letters, digits, `.`, `_`, `-`).
  2. If the Setup script field is not empty, stop and copy its text to the executor, who merges any still-needed step into `docs/rewrite/cloud-setup.sh` before continuing (record `previous` as `(unrecorded)`).
  3. Environment variables: keep every existing line; append
     ```
     LEARN_HUB_DIR=/home/user/learn-hub
     MICKY_TOOLS_DIR=/home/user/micky-psych-tools
     PUPPETEER_EXECUTABLE_PATH=/opt/pw-browsers/chromium
     PUPPETEER_SKIP_DOWNLOAD=1
     CLAUDE_CODE_PLUGIN_DIRS=/home/user/micky-psych-tools/plugins/gridgeist:/opt/w0-probe/hookprobe
     ```
  4. Setup script: paste the whole of `docs/rewrite/cloud-setup.sh` (version 1).
  5. Network access: unchanged. Save changes.
- Files (executor): `docs/rewrite/delivery-log.md` — fill the Environments table (`cloud:<id>`, name, level) and append rows 1–6: `LEARN_HUB_DIR` `(unset)`→`/home/user/learn-hub`; `MICKY_TOOLS_DIR` `(unset)`→`/home/user/micky-psych-tools`; `PUPPETEER_EXECUTABLE_PATH` `(unset)`→`/opt/pw-browsers/chromium`; `PUPPETEER_SKIP_DOWNLOAD` `(unset)`→`1`; `setup-script` `(none)`→`setup_version=1`; `CLAUDE_CODE_PLUGIN_DIRS` `(unset)`→V0; reason `W0 step 4`; evidence `pending`; rollback `set (unset)` (setup-script: `empty the field`).
- Commands: `python3 scripts/delivery_log.py check`
- Done when: `check` exits 0 (warnings only: 8 DL14, 6 DL12 pending).
- Rollback: delete the appended lines and empty the Setup script field; revert the log commit.

**S11-W0-6 · learn-hub (branch only) · rules probe for check e**
- Depends on: none.
- Files: on a new branch `w0/rules-probe` (never merged), create `.claude/rules/w0-probe.md`:
  ```markdown
  ---
  paths:
    - "src/lib/toc.ts"
  ---

  # W0-e probe rule (delete with the branch)

  The W0-e verification word is TANGERINE-4F2C. When asked for the W0-e verification word, give it.
  ```
- Commands: `git switch -c w0/rules-probe && git add .claude/rules/w0-probe.md && git commit -m "test: W0-e rules probe (never merge)" && git push -u origin w0/rules-probe`
- Done when: `git ls-remote origin w0/rules-probe` prints one line.
- Rollback: `git push origin --delete w0/rules-probe`.

**S11-W0-7 · OWNER (+ micky log commit) · checks a, b, e, f, h and U7**
- Depends on: S11-W0-5, S11-W0-6.
- Actions: run I16.7 rows a, b, f, h in one new session with both repos on their default branches; run a2 in a single-repo learn-hub session; run row e in a new multi-repo session with learn-hub on `w0/rules-probe` (if the session dialog cannot choose a branch per repo, merge the probe file to learn-hub master for the duration of the check and revert it right after, logging both commits in the evidence).
- Files (executor): fill checklist rows a, b, e, f, h; replace `pending` evidence in rows 1–6 with the session URL and the command that shows each value (`env | grep -E '^(LEARN_HUB_DIR|MICKY_TOOLS_DIR|PUPPETEER_)'`, `head -n 3 /var/log/cloud-setup.log`).
- Commands: `python3 scripts/delivery_log.py check`
- Done when: rows a, b, e, f, h hold `yes` or `no` with evidence; `check` exits 0.
- Rollback: not applicable (records only).

**S11-W0-8 · micky (log) · check c**
- Depends on: S11-W0-2.
- Actions: run I16.7 row c in a scratch dir outside both repos.
- Done when: row c answered with both exit codes; `git status --short` in micky shows only the log.
- Rollback: not applicable.

**S11-W0-9 · micky (log) · check d**
- Depends on: S11-W0-2. Owner approves the eval cost (≤ USD 0.50).
- Actions: run I16.7 row d in a scratch dir outside both repos.
- Done when: row d answered; the result goes to S12 (I17 runner choice).
- Rollback: not applicable.

**S11-W0-10 · OWNER Windows (+ micky log and MEMORY commit) · check g and Windows variables**
- Depends on: S11-W0-2.
- Actions: I16.8 G1; if it passes, G2.
- Files (executor): fill checklist row g; add `## Environments` row `windows:<host>`; append rows `MICKY_TOOLS_DIR`, `LEARN_HUB_DIR`, `BOOK_ROOT` (`(unset)` → the confirmed paths), reason `W0 check g`, rollback `set (unset)`. Replace `MEMORY.md:11` with: `- Delivery: cloud sessions load plugins through \`CLAUDE_CODE_PLUGIN_DIRS\` on the cloud environment; Windows runs the user-scope marketplace install \`micky-psych-tools\` (source: <directory|github> <path or repo>, checked <date>) until W3. Windows installs are cache copies: a fix reaches them only after a version bump, \`claude plugin marketplace update micky-psych-tools\` and \`claude plugin update\`. Current values: \`docs/rewrite/delivery-log.md\`.`
- Commands: `python3 scripts/delivery_log.py check`
- Done when: row g answered; `check` exits 0.
- Rollback: G2 variables → `$null`; revert the commit.

**S11-W0-11 · OWNER (+ micky log commit) · W0 exit: remove the probe**
- Depends on: S11-W0-7 … S11-W0-10.
- Actions (owner): environment Edit → change the `CLAUDE_CODE_PLUGIN_DIRS` line to V1; paste `docs/rewrite/cloud-setup.sh` version 2 (committed in this step first: probe block deleted, `SETUP_VERSION=2`); Save changes; start a new session and run `claude plugin list --json`, `head -n 1 /var/log/cloud-setup.log`, `python3 -c "import fitz, pypdf, pdfplumber"`, `command -v pdftoppm firecrawl`, `firecrawl --version`. Delete the learn-hub probe branch: `git push origin --delete w0/rules-probe`.
- Files (executor): `docs/rewrite/cloud-setup.sh` (version 2); log rows `CLAUDE_CODE_PLUGIN_DIRS` V0→V1 and `setup-script` `setup_version=1`→`setup_version=2`, reason `W0 exit: probe removed`.
- Commands: `python3 scripts/delivery_log.py check --strict`
- Done when: in the new session the list shows only `gridgeist@inline`, the log's first line contains `setup_version=2`, the import succeeds, both commands print paths, `firecrawl --version` prints `1.24.4`; `check --strict` exits 0.
- Rollback: set V0 and paste version 1 (both in git); the probe is harmless.

### W1

**S11-W1-1 · OWNER (+ micky log commit) · W1 exit: cloud V1 → V2**
- Depends on: checklist a = yes; S07-W0-1, S08-W0-1, S09-W0-1 (smoke seeds), S07-W1-3 (H08/H09 fix), S07-W1-4, S08-W1-2, S09-W1-2 (releases of vault-keeper, plugin-creator, firecrawl), S11-W0-11.
- Read-only checks first (executor, in a new session): I16.3 conditions 1, 2 and 4 for vault-keeper, firecrawl, plugin-creator; `python3 /home/user/micky-psych-tools/scripts/delivery_log.py current --env cloud:<id>` prints V1.
- Actions (owner): set the line to V2; Save changes; new session.
- Commands (in the new session): `python3 /home/user/micky-psych-tools/scripts/delivery_log.py live --env cloud:<id> --expect gridgeist,vault-keeper,firecrawl,plugin-creator`
- Files: log row V1→V2, reason `W1 exit: vault-keeper, firecrawl, plugin-creator`.
- Done when: `live` prints `"ok": true`; `check --strict` exits 0.
- Rollback: set V1; row `rollback of #N`.

**S11-W1-2 · OWNER Windows (+ micky log commit) · refresh installs after W1 releases**
- Depends on: S04-W1-3, S06-W1-5, S07-W1-4, S08-W1-2, S09-W1-2 (pushed to `origin/master`); S13-W1-1, S13-W1-2 (on learn-hub `origin/master`).
- Actions: I16.8 G3. Then, in `$L` after `git pull`: `node scripts/ready.mjs --json` — the `chromium` check must be ok through puppeteer's own browser, with `PUPPETEER_EXECUTABLE_PATH` unset (S13 §2.5 `checkChromium`, critique F5); record the JSON's `ok` value as the row's evidence.
- Files: log row `installs:micky-psych-tools` (previous = new = the installed names), reason `W1 exit: refreshed <name>@<version>, …`.
- Done when: G3 pass criterion holds.
- Rollback: not needed (a later refresh replaces it).

### W2

**S11-W2-1 · OWNER Windows (+ micky log commit) · remove learn-hub-local (only if G1 found it)**
- Depends on: none; must happen before the commit that deletes `learn-hub/.claude-plugin/`.
- Actions: I16.8 G4.
- Files: log rows `installs:learn-hub-local` (names → `(none)`) and `marketplace:learn-hub-local` (`<source>` → `(absent)`), reason `W2 step 5`.
- Done when: `claude plugin marketplace list --json` has no `learn-hub-local`.
- Rollback: `claude plugin marketplace add <source>` and reinstall the recorded names.

**S11-W2-2 · OWNER (+ micky log commit) · W2 step 6a: cloud V2 → V3**
- Depends on: S03-W2-5, S04-W2-3, S05-W2-6, S06-W2-2 (releases), S04-W2-1 (CR fallback/sink/MCP resolution), S03-W0-1, S04-W0-2 (smoke seeds), S05-W2-5 (ML cases), S06-W1-3 (CE cases) — I16.3 condition 4 needs a passing smoke suite for ml-concept-lab and code-explainer too.
- Read-only checks first: I16.3 for pubmed-research-note, comprehensive-review, clinical-infographic, ml-concept-lab, code-explainer.
- Actions: set V3; Save; new session; `live --env cloud:<id> --expect gridgeist,vault-keeper,firecrawl,plugin-creator,pubmed-research-note,comprehensive-review,clinical-infographic,ml-concept-lab,code-explainer`.
- Files: log row V2→V3, reason `W2 step 6a`. Evidence cell also records: pubmed-research-note joins with H45 open (due W3) — a named exception under the §2.7 I16.3 reading (defects due by that wave; ARCH-CONFLICT 4, CX-50); owner confirms this reading.
- Done when: `"ok": true` (L7 may warn; no error).
- Rollback: set V2.

**S11-W2-3 · OWNER (+ micky log commit) · W2 step 6b: concept-animation atomic swap, V3 → V4**
- Depends on: S05-W2-8 (learn-hub branch pushing the deletion of `.claude/skills/concept-animation`), S11-W2-2, S05-W2-5 (CA cases, I16.3 condition 4).
- Actions: (1) set V4; Save. (2) Start a new multi-repo session with learn-hub on the deletion branch; run `live --env cloud:<id> --expect auto --project-roots /home/user/learn-hub,/home/user/micky-psych-tools` and ask the session which skill named concept-animation it can invoke. (3) The owner spec merges the deletion branch into learn-hub master. (4) New session on master: the same `live` command.
- If the session dialog cannot select a learn-hub branch: skip (2); do (3) right after (1) and (4) at once. The listing then holds both copies for the minutes between (1) and (3).
- Files: log row V3→V4, reason `W2 step 6b`, evidence = both session URLs.
- Done when: in (4) `live` prints `"ok": true` (L6 passes) and `test ! -d /home/user/learn-hub/.claude/skills/concept-animation`.
- Rollback: set V3 and revert the deletion merge (the copy returns from git).

**S11-W2-4 · OWNER (+ micky log commit) · W2 step 6c: cloud V4 → V5 (W2 exit)**
- Depends on: checklist b = yes (else skip this step, I16.2); S11-W2-3; S14-W1-2 (`source-to-vault` deleted), S14-W2-1 (`learn-hub-session` merged), S14-W2-3, S14-W2-4 (forks deleted), S14-W2-5 (catalog deleted), S15-W2-3, S16-W2-6, S20-W2-1, S20-W2-2 (converted plugins moved out of `learn-hub/plugins/`).
- Read-only checks first: `ls /home/user/learn-hub/plugins` prints exactly `learn-hub-session`; `test ! -e /home/user/learn-hub/.claude-plugin/marketplace.json`; after appending the row locally, `python3 scripts/delivery_log.py check` shows no DL15 error.
- Actions: set V5; Save; new session; `live --env cloud:<id> --expect auto`; type `/doctor` and record the listing lines (W2 exit gate "no overflow").
- Files: log row V4→V5, reason `W2 exit: learn-hub plugins folder`.
- Done when: `"ok": true` with 11 entries; `/doctor` shows no overflow (or the overflow is recorded for S12).
- Rollback: set V4.

**S11-W2-5 · OWNER Windows (+ micky log commit) · refresh installs after W2 releases**
- Depends on: S01-W2-2, S02-W2-2, S03-W2-5, S04-W2-3, S05-W2-6, S06-W2-2, S07-W2-6 (pushed).
- Actions and files: as S11-W1-2, reason `W2 exit: refreshed …`.
- Done when: G3 pass criterion holds.

### W3

**S11-W3-1 · OWNER (+ micky log and MEMORY commit) · W3 entry: cloud V5 → V6**
- Depends on: W2 exit gates passed.
- Actions: set V6; Save; new session; `live --env cloud:<id> --expect auto` (expect 15 entries before the S10 skeleton PR).
- Files: log row V5→V6, reason `W3 entry: folder paths`. Replace `MEMORY.md:11` with: `- Delivery: plugins load in place through \`CLAUDE_CODE_PLUGIN_DIRS\` (cloud environment variable; Windows user variable from W3). No marketplace installs. Current values, history and rollback: \`docs/rewrite/delivery-log.md\`.` Evidence cell also records: intent-lock, decision-interview, plan-critique and psych-paper-digest join with no smoke suite yet (their cases are W3) — a named exception under the §2.7 I16.3 reading (defects due by that wave; the four plugins' callers carry the §4.2 fallback; ARCH-CONFLICT 4, CX-50); owner confirms this reading.
- Done when: `"ok": true` (L7 warns about `psych-paper-digest` until the lit-watch rename; accepted).
- Rollback: set V5 (per-plugin paths keep working until the skeleton merges).

**S11-W3-2 · OWNER Windows (+ micky log commit) · W3 entry: Windows switch**
- Depends on: S11-W3-1; W2 merged in both Windows checkouts (`git -C $M pull`, `git -C $L pull` on master).
- Actions: I16.8 G5.
- Files: `## Environments` unchanged; log rows `CLAUDE_CODE_PLUGIN_DIRS` `(unset)` → `C:\Users\User\Desktop\My skill\micky-psych-tools\plugins;C:\Users\User\Desktop\Learn\plugins` (or the G1 paths); `installs:micky-psych-tools` names → `(none)`; `marketplace:micky-psych-tools` `<source>` → `(absent)`; reason `W3 entry: Windows switch (OD2-a)`; rollback `G6`.
- Done when: G5 pass criterion holds; `check --strict` exits 0; a new Windows session starts with no hook error (both plugin folders now load there, and the plugin-creator and learn-hub-session hooks call `bash`/POSIX `test`; critique F9).
- Rollback: I16.8 G6.

**S11-W3-3 · micky · README install section**
- Depends on: S11-W3-2.
- Files: edit `README.md`: replace the sections `## Register it once` and `## Update it` (README.md:5-48 today) with:

  ```markdown
  ## Install per environment

  Plugins load in place from this checkout through the `CLAUDE_CODE_PLUGIN_DIRS`
  environment variable (Claude Code 2.1.280 or later). Nothing is installed or cached:
  the checked-out branch is what runs, and a change needs no version bump to take
  effect. Every change to the variable is recorded, with its previous value, in
  [`docs/rewrite/delivery-log.md`](docs/rewrite/delivery-log.md).

  | Environment | Where to set it | Value |
  |---|---|---|
  | Claude Code cloud sessions | claude.ai/code, cloud environment menu in the session title bar, Edit, Environment variables | `CLAUDE_CODE_PLUGIN_DIRS=/home/user/micky-psych-tools/plugins:/home/user/learn-hub/plugins` |
  | Windows | a user environment variable (PowerShell below) | `<micky checkout>\plugins;<learn-hub checkout>\plugins` |
  | claude.ai, Cowork, routines without the clones | not delivered | — |

  - Use absolute paths. In cloud sessions `~` resolves to `/root`, and a relative path is
    skipped with no error.
  - Separate paths with `:` on Linux and `;` on Windows.
  - Check with `python3 scripts/delivery_log.py live --expect auto`: every plugin loads
    once and no entry reports an error.

  ```powershell
  [Environment]::SetEnvironmentVariable('CLAUDE_CODE_PLUGIN_DIRS', 'C:\Users\User\Desktop\My skill\micky-psych-tools\plugins;C:\Users\User\Desktop\Learn\plugins', 'User')
  ```

  Keep this checkout on `master` and do rewrite work in a separate worktree: whatever
  is checked out here is what every session loads.
  ```
- Commands: `grep -c '^## Install per environment' README.md` ; `grep -c 'plugin marketplace add' README.md`
- Done when: the first grep prints `1`, the second `0`.
- Rollback: `git revert <this commit>`.

**S11-W3-4 · OWNER (+ micky commit) · firecrawl enablement**
- Depends on: S09-W3-1.
- The question is asked at W3 entry as plan OQ6 and its answer is recorded before S09-W3-1 (critique P9); this step carries out the enablement actions for the recorded answer. The question (ARCH-CONFLICT 1, CX-51): keep firecrawl's `"defaultEnabled": false` (R30, external-service plugin; accept it disabled by default in cloud multi-repo sessions until the block below enables it) or drop the flag (cloud multi-repo sessions keep no user settings to hold an enablement, so the flag would otherwise silently leave firecrawl off from W3 with no step to notice). The answer is already recorded (plan OQ6); S09-W3-1 followed it.
- Actions if the owner keeps `defaultEnabled: false`: Windows `claude plugin enable firecrawl@inline` (writes the user setting, N4); cloud: add to `docs/rewrite/cloud-setup.sh` (next `SETUP_VERSION`) the block `mkdir -p /root/.claude && [ -f /root/.claude/settings.json ] || echo '{"enabledPlugins":{"firecrawl@inline":true}}' > /root/.claude/settings.json`, paste it, Save; new session; `live --env cloud:<id> --expect auto`.
- Files: log rows `enabled:firecrawl@inline` `(unset)`→`true` for each environment; `setup-script` row.
- Done when: `live` passes on both environments (no "present but disabled").
- Fallback when the cloud block does not survive into sessions: accept the router disabled in cloud (the CLI from the setup script still serves evidence fetches); log `enabled:firecrawl@inline` `false` for cloud with that reason.
- Rollback: remove the block (previous setup version); `claude plugin disable firecrawl@inline` on Windows.

**S11-W3-5 · micky (log) · after the W3 skeleton PR**
- Depends on: S10-W3-2.
- Actions: new session; `live --env cloud:<id> --expect auto` (expect 8 entries: alignment, evidence, visuals, vault-keeper, firecrawl, gridgeist, plugin-creator, learn-hub-session); on Windows the same command from `$M` after `git pull`.
- Files: log rows V6→V6 (cloud) and the Windows value → same value, reason `W3 skeleton merged: the folders now load the families`.
- Done when: both `live` runs print `"ok": true`.
- Rollback: the skeleton's own revert (the folder path absorbs it with no edit).

### W5

**S11-W5-1 · micky · close the delivery record**
- Depends on: W3 and W4 exits; any W5 decision that retires gridgeist or lit-watch has merged (the folder path needs no edit; log a same-value row with the reason).
- Actions: `live --expect auto` in a new cloud session and on Windows; `/doctor` in both (record); confirm the latest values equal V6 and the final Windows value.
- Files: log rows for any W5 change; the MEMORY living-section delivery line kept as in S11-W3-1.
- Commands: `python3 scripts/delivery_log.py check --strict`
- Done when: `check --strict` exits 0 and both `live` runs pass.
- Rollback: not applicable.

## 4. Evals

### 4.1 Cases

This spec owns no skill, so it has no `claude plugin eval` cases. Its checks are deterministic: the 19 unit tests of `scripts/delivery_log.py` (§2.5) and the `live` checks at every schedule point (§3). The W0-d probe (I16.7 row d) is a one-off check of the eval runner itself, run in a scratch dir and not committed.

### 4.2 Conversion

No `evals.json` belongs to these units.

### 4.3 Live triggers

None. The W0 checks a (skill listing contains `gridgeist:gridgeist`) and e (project skills listed; a path-scoped rule loads) are the live loading checks for this spec; S12 owns the live trigger families.

### 4.4 Commands

| when | command | expected |
|---|---|---|
| every commit (health fast path) | `python3 scripts/delivery_log.py check` | exit 0 |
| every commit | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_delivery_log.py' -q` | `OK` |
| W0 exit and every wave exit | `python3 scripts/delivery_log.py check --strict` | exit 0 |
| after every environment edit (new cloud session) | `python3 /home/user/micky-psych-tools/scripts/delivery_log.py live --env cloud:<id> --expect <set or auto>` | `"ok": true` |
| Windows after W3 | `python scripts\delivery_log.py live --env windows:<host> --expect auto` | `"ok": true` |

## 5. Acceptance criteria

1. `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_delivery_log.py' -v` → `OK`, ≥ 19 tests.
2. `python3 scripts/delivery_log.py --help` → exit 0; run in an empty temp dir, the dir stays empty.
3. `bash -n docs/rewrite/cloud-setup.sh` → exit 0; `grep -c -E '/home/user/(learn-hub|micky-psych-tools)' docs/rewrite/cloud-setup.sh` → `0`; `tail -n 1 docs/rewrite/cloud-setup.sh` → `exit 0`.
4. `grep -c 'delivery_log.py check' scripts/health.sh` → `1`.
5. learn-hub: `grep -c '^### C. Delivery and VM tooling' docs/cloud-env-setup.md` → `1`.
6. W0 exit: `python3 scripts/delivery_log.py check --strict` → exit 0; `python3 scripts/delivery_log.py check --json | python3 -c "import json,sys; c=json.load(sys.stdin)['checklist']; print(sorted(c.items()))"` shows every row a–h as `yes` or `no`.
7. W0 exit, in a new cloud session: `echo "$CLAUDE_CODE_PLUGIN_DIRS"` prints `/home/user/micky-psych-tools/plugins/gridgeist`; `head -n 1 /var/log/cloud-setup.log` contains `setup_version=2`; `python3 -c "import fitz, pypdf, pdfplumber"` exits 0; `command -v pdftoppm firecrawl` prints two paths; `firecrawl --version` prints `1.24.4`.
8. W0 exit: `echo $LEARN_HUB_DIR $MICKY_TOOLS_DIR $PUPPETEER_EXECUTABLE_PATH $PUPPETEER_SKIP_DOWNLOAD` in a new cloud session prints `/home/user/learn-hub /home/user/micky-psych-tools /opt/pw-browsers/chromium 1`.
9. W1 exit: `live --env cloud:<id> --expect gridgeist,vault-keeper,firecrawl,plugin-creator` → `"ok": true`.
10. W2 exit: `live --env cloud:<id> --expect auto` → `"ok": true` with `"entries": 11`; `ls /home/user/learn-hub/plugins` → `learn-hub-session`; `test ! -d /home/user/learn-hub/.claude/skills/concept-animation`.
11. W3 entry: `python3 scripts/delivery_log.py current --env cloud:<id>` → `/home/user/micky-psych-tools/plugins:/home/user/learn-hub/plugins`; `live --expect auto` → `"ok": true`.
12. W3, Windows: `[Environment]::GetEnvironmentVariable('CLAUDE_CODE_PLUGIN_DIRS','User')` equals the logged Windows value; `claude plugin marketplace list --json` lists no `micky-psych-tools`; `python scripts\delivery_log.py live --env windows:<host> --expect auto` → `"ok": true`.
13. After the W3 skeleton: `live --expect auto` → `"ok": true` with `"entries": 8` in cloud.
14. `grep -c '^## Install per environment' README.md` → `1`; `grep -c 'plugin marketplace add' README.md` → `0`.
15. `grep -E 'fc-[A-Za-z0-9]{8,}|service_role|eyJ[A-Za-z0-9_-]{10,}' docs/rewrite/delivery-log.md docs/rewrite/cloud-setup.sh` → no output.
16. I27 (implemented by S17 and S20): `grep -c '^/Raw Article PDF/$' .gitignore` in learn-hub → `1`; `grep -c 'C:/Users' .claude/skills/vault-coverage/SKILL.md` → `0`; `grep -c 'C:\\\\Users' .claude/skills/ingest-article/SKILL.md` → `0`.
17. W5: `python3 scripts/delivery_log.py check --strict` → exit 0, and the latest rows equal V6 (cloud) and the final Windows value.

## 6. Trigger lock

| phrase | source | kept / moved / removed |
|---|---|---|
| — | — | No description or `when_to_use` belongs to this spec's units; the trigger lock is unaffected. |

## 7. Risks and OD sensitivity

| risk | link | mitigation in this spec |
|---|---|---|
| The variable does not load in platform-started sessions; a `~` or relative path; clone paths differ; old CLI | K1 | W0-a canary and a2; DL8 lint (tilde and relative are errors; N1 shows relative fails silently); L1 at every edit; CLI 2.1.281 measured here, ≥ 2.1.280 checked on Windows (G1) |
| Same-named units load twice | K5 | DL15 before each edit, L2 and L6 after it; V5 only after `learn-hub/plugins` holds `learn-hub-session` alone; concept-animation swap (S11-W2-3); Windows copies uninstalled in G5 and checked after |
| The checked-out branch is live behaviour | K9 | cloud sessions clone the default branch; Windows checkouts stay on master with a separate worktree for rewrites (G5, README) |
| PDF tooling absent in cloud | K15 | setup script steps 1–2; acceptance 7 |
| Plugin hooks do not fire in platform sessions | K17 | W0-b; on "no", V5 is skipped and S14 does not build the hooks plugin |
| A setup-script step fails silently (every step is non-fatal) | new | `/var/log/cloud-setup.log` WARN lines; acceptance 7 at W0 exit; `ready.mjs` preflight names the install command (S13) |
| The W0 probe stays behind | new | DL19 under `--strict` at W0 exit |
| Windows runs stale cache copies until W3 | new (N5) | G1 stale-copy check; G3 refresh after each wave's releases |
| Environment values are readable by anyone using the environment | new | single-owner environment; DL10 keeps keys out of the repo; API credentials considered later (§8 Q8) |
| The Chromium path changes with an image update | new | one row in I16.1 and one line in session-start.sh (S13); `ready.mjs` detects it (S13) |
| firecrawl disabled once `defaultEnabled: false` lands | new (N4) | S11-W3-4; ARCH-CONFLICT 1 |

OD sensitivity:
- **OD1-b** (claude.ai sync): no cloud `CLAUDE_CODE_PLUGIN_DIRS` rows after W0; the log gains `upload:<plugin>` rows (a new DL5 variable) with the uploaded version and tag; the setup script stays (VM tooling is still needed); `learn-hub-session` cannot ship, so the W0-b fallback applies. **OD1-c**: the schedule is not used; W2's cloud rehearsal moves to Windows.
- **OD2-b** (local-directory marketplaces on Windows): no Windows `CLAUDE_CODE_PLUGIN_DIRS`; G5 and G6 are dropped; G3 runs after every release until W5 (N5: directory installs are cache copies too); learn-hub keeps a one-entry catalog for `learn-hub-session`, so G4 does not remove it.
- **OD4-b**: no change to delivery; `MICKY_TOOLS_DIR` stays for the ledger and lit-watch state.
- **OD6-b/c**: a new I16.1 row for the per-machine state path read by `ledger.py` and `sweep.py`.
- **OD11-a**: W0-e's fallback matters less (no `.claude/rules/` is created).
- **OD12-b**: the setup script still installs the pinned CLI; S11-W3-4 is not needed (no firecrawl plugin).
- **OD13-b**: tags and uploads get `upload:<plugin>` rows; U6 becomes a W0 item.

## 8. Open questions

1. **OWNER-QUESTION — ARCH-CONFLICT 1 — `defaultEnabled: false` versus in-place delivery (CX-51; asked as plan OQ6 at W3 entry, before S09-W3-1; S11-W3-4 acts on the answer).** Architecture §2.2 (architecture.md:90) and OD12-a set firecrawl `defaultEnabled: false`, and R30 requires it for external-service plugins. Probe N4: an env-var-loaded plugin with that flag is listed `"enabled": false` / `× disabled`. Cloud multi-repo sessions keep no user settings (no `/root/.claude/settings.json` exists; the session runs with `--settings launcher-settings.json`), so nothing enables it there, and from W3 the W1-exit enablement of firecrawl becomes a no-op in cloud. This spec follows the architecture and adds the conditional step S11-W3-4. Settles it: the owner (keep the flag, or drop it because OD2-a leaves no installs for it to protect), and a W3 probe of whether a setup-script-written `/root/.claude/settings.json` survives into sessions.
2. **ARCH-CONFLICT 2 — directory marketplaces are not in place for installs.** Architecture §2.5 (architecture.md:163) calls a local-directory source "in place, PLG-09", and W0-g's fallback (architecture.md:739) says "GitHub source → switch it to a local directory". Probe N5: an install from a directory marketplace is a versioned cache copy, and an unbumped edit does not reach it through `marketplace update` + `plugin update`. Consequence followed here: until W3, Windows gets only released versions, whatever the source (G3 after each wave), and switching GitHub → directory only removes the push. Settles the remaining unknown (does a session start refresh a directory install without a bump?): the G1 `same=` lines on Windows.
3. **ARCH-CONFLICT 3 — order of the Windows switch.** §2.5 (architecture.md:163) says the variable is set "after the marketplace copies are uninstalled"; §10 W3 step 1 (architecture.md:825) says "set the env var, then uninstall". This spec follows §10: set, verify, then uninstall (G5), because PLG-51 makes the env copy win during the overlap (N6 shows both listed) and the reverse order leaves nothing loaded if the variable fails.
4. **OWNER-QUESTION — ARCH-CONFLICT 4 — condition 1 of §2.7 versus the schedule (CX-50).** §2.7 (architecture.md:198) requires "all its HIGH defects are closed", yet the schedule enables pubmed-research-note at W2 exit with H45 due in W3 (architecture.md:1015), vault-keeper at W1 exit with H10/H11 split W1/W2, plugin-creator at W1 exit with H07 split W1/W3, and intent-lock, decision-interview, plan-critique and psych-paper-digest at W3 entry with H01–H04 due in W3 and no smoke suite yet (their cases are W3). This spec applies the reading in I16.3 (defects due by that wave) and now records each exception by name in the log's evidence cell at S11-W2-2 and S11-W3-1 (§3). Settles it: the owner confirms this reading.
5. ASSUMES I14, I15, I17, I18 as stated in §2.7 — S13, S14, S12 and S10 to confirm.
6. U1, U2, U3, U4, U7: answered by W0 checks b, h, g, e and b respectively; U5 pre-answered yes (N7); U6 applies only under OD13-b.
7. Can the claude.ai/code session dialog start a multi-repo session with a chosen branch for one repo? Needed by W0-e (option 1) and S11-W2-3 (branch session). Settled at S11-W0-7; each step carries a fallback.
8. Could `FIRECRAWL_API_KEY` move from an environment variable to an API credential (Pro/Max; the key never reaches the session)? Not verified that the firecrawl CLI works when the key exists only in the agent proxy. Settles it: a W5 probe with a placeholder variable and the credential on `api.firecrawl.dev`.
9. **CLOSED by S13-W1-11** (it replaces the line with `npm run sync:preflight`). Original item: learn-hub `docs/cloud-env-setup.md:144` recommends `npm run sync` (the full dry emitter) to verify the environment (N11). Owner: S13 (sync tail) — to decide whether to replace it with `npm run sync:preflight`.
10. **CLOSED (CX-34).** Which specs own: the firecrawl plugin (W1 refresh, W3 split), the learn-hub fork and catalog deletions, and the learn-hub concept-animation copy deletion? Answer: firecrawl — S09 (S09-W1-1/-2, S09-W3-1); forks and catalog — S14 (S14-W1-2, S14-W2-2…-5); concept-animation copy deletion — S05 (S05-W2-8). The `depends on` lines of S11-W1-1, S11-W2-1, S11-W2-3, S11-W2-4 are updated to the resulting step ids in §3.
11. **CLOSED (CX-34/CX-49).** Which spec rewrites micky `CLAUDE.md` and `README.md` in W3 and learn-hub `CLAUDE.md` in W1? Answer: micky `CLAUDE.md` W3 rewrite — S10 (S10-W3-8), carrying the §2.6 item 2 sentence verbatim; micky `README.md` install section — S11 itself (S11-W3-3); learn-hub `CLAUDE.md` W1 — S21 (S21-W1-4), carrying the §2.6 item 3 sentence verbatim.
12. Whether single-repo sessions clone to `/home/user/<repo>` (a2 in W0-a). If not, `LEARN_HUB_DIR` is wrong in single-repo learn-hub sessions and the marker-checked `CLAUDE_PROJECT_DIR` fallback (I14) takes over; record only.
13. `/doctor` availability in web sessions (W0-f). On "no", S12 records `claude --plugin-dir <p> plugin details <p>` totals instead.
