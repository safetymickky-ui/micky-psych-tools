# Spec S07: vault-keeper and empty-vault (sink and transfer owner)

| Field | Value |
|---|---|
| Repos | micky-psych-tools |
| Units (today → target) | `plugins/vault-keeper` (skills `vault-keeper`, `empty-vault`; command `/empty-vault`) → same dir, two skills (`vault-keeper` model-invocable, `empty-vault` dmi), no `commands/`; new `scripts/sink.py` (+ `test_sink.py`; `drain_plan.py` only at W5 if the vault is kept, `vault_index.py` cut — OQ15-a); `references/vault-layout.md` (kept, trimmed); `vault/.vault-id` (new) |
| Waves | W0 (smoke seeds, CX-4); W1 (`sink.py` resolver + `.vault-id`; empty-vault stopgap: dmi, marker→ask, never delete assets); W2 (sink routes to the inbox; the link rule in prose; one owner-watched copy of the 7 artifacts to the inbox, the W1 no-delete stopgap stays — OQ15-a); W3 (command file deleted; skill keeps its name); W5 (`drain_plan.py` and the transfer, only if S07-W5-1 keeps the vault) |
| Owner decisions assumed | OD4-a (micky `vault/` stays the fallback sink), OD5-a (inbox only; publish needs "digest"), OD9-a (habit verbs as dmi/`argument-hint`, no new alias skill here), OD10-a (empty-vault is user-only); owner answers OQ12-a, OQ15-a (all confirmed 2026-09-24) |
| Defects closed | 13 of 15 assigned (HIGH: H08, H09, H10, H11) |
| Interfaces owned | I11 (sink), I12 (transfer) |
| Interfaces consumed | I09 (owner S15), I10 (owner S15), I16 (owner S11), I17 (owner S12), I20 (owner S08) |
| Depends on specs | S11 (env vars, delivery schedule), S15 (inbox contract, intake log — read before W2), S08 (house shape templates, W3 skeleton), S10 (bump/CHANGELOG backfill), S12 (eval layout/runner) |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| path | lines | bytes | tok | role |
|---|---|---|---|---|
| `.claude-plugin/plugin.json` | 15 | 587 | 147 | manifest, v0.4.0 |
| `README.md` | 48 | 3,254 | 808 | integration contract |
| `CHANGELOG.md` | 9 | 379 | 94 | stops at 0.2.0 |
| `commands/empty-vault.md` | 15 | 744 | 182 | thin wrapper, `argument-hint: "[topic]"` |
| `skills/vault-keeper/SKILL.md` | 129 | — | 1,657 | filer/indexer/query skill |
| `.../vault-keeper/references/vault-layout.md` | 35 | 1,785 | 442 | "single source" tree/naming/collision/index |
| `.../vault-keeper/evals/evals.json` | 53 | 4,033 | 1,004 | 6 cases, `assertions: []` |
| `skills/empty-vault/SKILL.md` | 127 | — | 1,380 | drain-to-Learn-hub skill |
| `.../empty-vault/evals/evals.json` | 53 | 3,823 | 953 | 6 cases, `assertions: []` |
| `vault/` (repo root) | 16 files, 5 dirs | — | — | 6 MOCs, 7 artifacts, 0 notes, 0 assets, `index.md`; no `.vault-id` today |

### 1.2 Descriptions

| Skill | chars | bytes | YAML | `Use when` @ | `Not for` | Quoted phrases |
|---|---|---|---|---|---|---|
| `vault-keeper` | 910 | 952 | yes | 163 | yes (:12) | 12 English + 4 Thai (full list §6) |
| `empty-vault` | 1,003 | 1,031 | yes | 354 | yes (:13) | 6 English + 2 Thai (full list §6) |

Both under the 1,024 hard cap; `empty-vault` is 3 chars from it, no longer a listing risk once dmi (R35).

### 1.3 Defects

| id | sev | H# | evidence (re-opened) | fix step | wave |
|---|---|---|---|---|---|
| vault-keeper-1 | H | H08 | SKILL.md:29, vault-layout.md:7 — `${CLAUDE_PLUGIN_ROOT}/../../vault` claimed equivalent to the walk-up root; wrong in a cached install | S07-W1-1 resolver + `.vault-id`; S07-W1-3 wires it into Step 0 (CX-5) | W1 |
| vault-keeper-2 | H | H09 | SKILL.md:28, vault-layout.md:6 — walk-up to `.claude-plugin/marketplace.json` matches `learn-hub`'s own dir; no name check | S07-W1-1 resolver (marker `name: micky-psych-tools`); S07-W1-3 wires it into Step 0 (CX-5) | W1 |
| vault-keeper-3 | H | H10 | empty-vault SKILL.md:36-37 — root = "dir containing `.claude/skills/digest-report/`"; confirmed absent (moved) | S07-W1-2 stopgap closes detection; S07-W2-8 closes the W2 part: the one-time copy, with the stopgap kept (OQ15-a) | W1/W2 |
| vault-keeper-4 | H | H11 | empty-vault SKILL.md:55-57 — assets "removed with their topic", vs `ingest-infographic\|ingest-animation/SKILL.md:1-9` naming empty-vault as the handoff | S07-W1-2 (never delete, hold); S07-W2-8 closes the W2 part: the one-time copy, nothing deleted (OQ15-a) | W1/W2 |
| vault-keeper-5 | M | — | empty-vault SKILL.md:63-64 "invoke the Learn repo's `digest-report` skill" — no mechanism | S07-W2-1: stops at the inbox; digest-report/ingest-visual act on their own trigger, per I09/I12 | W2 |
| vault-keeper-6 | M | — | SKILL.md:10 "Four jobs" vs plugin.json:4 "Five jobs" vs README.md:22 "the five jobs" | S07-W2-2: job count stated once, in README.md only | W2 |
| vault-keeper-7 | M | — | SKILL.md:66 "Obsidian `[[wikilinks]]` by title" vs vault-layout.md:17-18 kebab/`<Topic> MOC.md` filenames, no `aliases:` | S07-W2-2: `save` writes `aliases: [<title>]` | W2 |
| vault-keeper-8 | M | — | SKILL.md:66-67 "a dangling link... is fine" vs SKILL.md:101 "fix stale/broken links", no rule separating the two | S07-W2-2(d): the `index` section states the dangling-versus-broken rule in prose (OQ15-a cut `vault_index.py`) | W2 |
| vault-keeper-9 | M | — | CHANGELOG.md newest `## 0.2.0 — 2026-07-10`; plugin.json:3 `"version": "0.4.0"` | deferred — see below | S10-W0-2 |
| vault-keeper-10 | L | — | README.md:49 target type incl. `MOC` vs SKILL.md:79 "Decide `note` vs `artifact`" | S07-W2-2(b): drop `MOC` from the README list | W2 |
| vault-keeper-11 | L | — | empty-vault SKILL.md:52-54 "notes... supplementary source material"; `digest-report/SKILL.md:18-29` has no such input shape | S07-W2-2(e): the "supplementary" sentence is dropped; S07-W2-8: the one-time copy moves every artifact as its own `<slug>.md` (OQ15-a) | W2 |
| vault-keeper-12 | L | — | empty-vault SKILL.md:39 hardcoded `` `C:\Users\User\Desktop\Learn` `` fallback | S07-W1-2: dropped, no hardcode (R47) | W1 |
| vault-keeper-13 | L | — | SKILL.md:41-50 restates vault-layout.md:10-32 | S07-W2-2(c): cut to a 4-line pointer | W2 |
| vault-keeper-14 | L | — | plugin.json no `license`; author `"Thanawat Suharit"` vs siblings' `"... (Micky)"`; em dash; `bump.py` escapes non-ASCII | manifest half S07-W1-1; tool half deferred — see below | W1/S10-W0-2 |
| vault-keeper-15 | L | — | both `evals.json`: `"assertions": []` all 12 cases; empty-vault eval 3 needs an undefined kebab→MOC mapping | S07-W2-5: real graders (§4); S07-W2-2(e): the kebab→MOC title rule in prose (OQ15-a; `moc_title_from_kebab()` arrives with S07-W5-2 if the vault is kept) | W2 |

**Deferred**

| id | reason |
|---|---|
| vault-keeper-9 (`ratchet: vault-keeper.changelog-behind`) | Cross-plugin, mechanical pass architecture.md §10 W0 step 1 assigns whole. Owner S10-W0-2 (`bump.py` rewrite) reconciles version parity going forward; S10-W0-8 backfills the missing CHANGELOG entries for this plugin's version history — S07 does not touch either script. |
| vault-keeper-14 bump half (`ratchet: bump.py.non-ascii-escape`) | Escape bug is in `bump.py`, fixed at S10-W0-2 (owned by S10; moved into plugin-creator at S08-W3-1). Manifest half (license, author, em dash) needs no shared tool — fixed at S07-W1-1. |

### 1.4 Other findings

- OBS (coupling): new scripts ship **inside** `pvk/scripts/` — a cached install carries only the plugin dir (confirmed). Governs R44 in §2.5.
- OBS (duplicated info): CHANGELOG two versions behind and "Four" vs "Five" jobs are cited measured drifts for the marketplace-wide duplication finding.
- OBS (evals): 6+6 cases, both `"assertions": []`, no runner (confirmed by reading both files, §1.1).
- OBS (undeclared deps): named as a dependency of "about 12 producers" with no `dependencies` mechanism — not added (T4/R56, OPTIONAL-by-name with a fallback, §2.6).
- OBS (cross-repo handoff drift, ×2): confirms the -3/-4/-5/-11/-12 cluster from both sides — closed by removing the direct-invocation design (§2.6), not repairing the call.
- OBS (filing pipeline incoherence): the assets-deleted vs assets-expected contradiction, same evidence as -4/H11.
- NEW: `vault/assets/` is empty today (only `.gitkeep`) — the `.kind` sidecar has no live data to migrate.
- NEW: `research-notes/.intake-log.jsonl` doesn't exist yet (confirmed `ls`) — `drain_plan.py` (W5, if built) treats a missing file as "nothing landed yet".

## 2. Target state

### 2.1 Location and tree (after W3)

```
plugins/vault-keeper/
  .claude-plugin/plugin.json · README.md · CHANGELOG.md
  scripts/
    sink.py           # I11 — root/sink resolution, inbox writes
    drain_plan.py     # I12 — transfer plan/validate/execute/delete (W5, only if S07-W5-1 keeps the vault; OQ15-a)
    test_sink.py · test_drain_plan.py   # vault_index.py is cut (OQ15-a)
  skills/
    vault-keeper/SKILL.md, references/vault-layout.md
    empty-vault/SKILL.md (argument-hint "[topic]", dmi: true)
  evals/
    vault-keeper/ (6 cases, §4) · empty-vault/ (6 cases, §4)   # CX-23 — plugins/<p>/evals/<skill>/<case>/, not skills/<skill>/evals/
vault/
  .vault-id            # contents: micky-psych-vault
  index.md, MOCs/, notes/, artifacts/, assets/   (unchanged)
```

Removed by W3: `commands/empty-vault.md`.

### 2.2 Frontmatter

**`vault-keeper`** (unchanged name; description rewritten to drop the job-count claim and add the sink line):

```yaml
---
name: vault-keeper
description: >-
  Files, indexes, links, and retrieves any skill's output in the one shared vault at the
  marketplace repo root (vault/), and — when the learn-hub checkout is present — routes a
  finished report or visual asset straight into its inbox instead. Use when the request says
  "save this to the vault", "vault this", "add to my vault", "file this note", "put this in
  the vault", "index the vault", "rebuild the index", "link these notes", "make a MOC",
  "query the vault", "search my vault", "what's in the vault", or asks to store, organize, or
  find any artifact a skill produced. Thai: "เก็บลง vault", "เพิ่มใน vault", "ค้น vault", "ทำ
  index". Not for producing the artifact itself (the source skill does that; this only files
  and finds it) and not for draining the vault into the Learn hub (use
  vault-keeper:empty-vault).
metadata:
  profile: cc
---
```
Measured: 793 chars. All 16 quoted phrases kept verbatim (trigger lock — §6).

**`empty-vault`** (dmi; `argument-hint` moves here from the retiring command):

```yaml
---
name: empty-vault
description: >-
  Drains the shared vault at the marketplace repo root (vault/) into the learn-hub inbox: for
  each artifact and note in scope, plans a transfer, copies it into research-notes/ (assets
  into research-notes/visuals/ when a receiver exists), verifies the copy's sha and the
  learn-hub intake log, and only then deletes the source — kinds with no receiver are listed
  and held, never deleted. Use when the request says "empty the vault", "drain the vault",
  "clear the vault", "move the vault to the Learn hub", "export the vault to learn-hub",
  "ship these reports to the hub", or asks to migrate vault content into the Learn hub. Thai:
  "ล้าง vault", "ย้าย vault ไป Learn". Scope to one topic with /empty-vault [topic]. Not for
  filing, indexing, or finding vault content (that is vault-keeper:vault-keeper), and not the
  distillation itself (learn-hub's digest-report skill authors the notes, on its own trigger).
argument-hint: "[topic]"
disable-model-invocation: true
metadata:
  profile: cc
---
```
Measured: 862 chars. All 8 phrases kept. Dropped the old "hands each report to the Learn repo's digest-report skill" clause (see §2.6).

### 2.3 Body outline

**`vault-keeper/SKILL.md`** (target ≤2,000 tokens per R11 — a Step-0 dependency for ~12 producers):

| Target section | Src → | Change |
|---|---|---|
| Step 0 — Locate the vault | 24-32 | calls `sink.py resolve` instead of the walk-up prose; drops the `${CLAUDE_PLUGIN_ROOT}/../..` line entirely (H08/H09) |
| The vault (tree/naming/etc) | 34-50 | cut to 4 lines pointing at `references/vault-layout.md` (fixes -13) |
| Frontmatter block | 52-68 | keep; add `aliases: [<title>]` (fixes -7) |
| save (jobs 1-5) | 78-94 | keep steps 1-4; step 5 unchanged; add: for `kind: asset`, also write `assets/<slug>.meta.json` next to `assets/<slug>.html` (CX-9 — no separate `.kind` sidecar; `kind` is one field inside the `.meta.json` the producer already writes, per I09) — needed by `drain_plan.py` |
| index | 96-104 | state the rule in prose (OQ15-a: no `vault_index.py`): dangling (target absent anywhere) left as-is; broken (target existed, no longer does, or points outside `vault/`) reported and rewritten to plain text — resolves -8 |
| query | 105-108 | keep |
| Rules / Failure conditions | 109-129 | keep; add "never write outside the resolved root" |
| Handoff (new) | — | the OPTIONAL/fallback sentence from §2.6 for callers OF vault-keeper |

Target body: ~95 lines / ~1,750 tokens (flat vs today's 1,657).

**`empty-vault/SKILL.md`** (becomes the transfer procedure over `drain_plan.py` at S07-W5-2, only if S07-W5-1 keeps the vault; until then the W1 stopgap stays — OQ15-a):

| Target section | Src → | Change |
|---|---|---|
| Step 0 — resolve both roots | 31-40 | micky root via `sink.py resolve`; learn-hub via `LEARN_HUB_DIR` → `userConfig.learn_hub_root` → marker → **ask** (fixes H10, -12) |
| Step 1 — manifest | 42-59 | replaced by `drain_plan.py plan`; show the printed manifest verbatim |
| Step 2 — hand off | 61-69 | **deleted** (fixes -5, -11) — replaced by `drain_plan.py validate` then `execute` |
| Step 3 — verify | 71-76 | "landed" = sha present in a **git-committed** `research-notes/` tree, not a Supabase count (fixes -5) |
| Step 4 — deletion gate | 78-86 | keep both gates; source is now `drain_plan.py delete` (dry-run default, `--yes` — R65) |
| Step 5 — reindex | 88-94 | rebuild `index.md` by vault-keeper's index rule after deletion (OQ15-a: no `vault_index.py`) |
| Step 6 — report | 96-100 | keep |
| Rules | 102-127 | keep; drop digest-report mentions; add "no-receiver kinds are held forever" (H11 permanence) |

Target body: ~90 lines / ~1,450 tokens.

### 2.4 References

| File | Purpose | Load condition | Size target |
|---|---|---|---|
| `skills/vault-keeper/references/vault-layout.md` | tree/naming/collision/index rules — sole source | "Before Step 0, read it" (unconditional) | ≤35 lines; only the resolver line rewritten |

No new reference files. `empty-vault` needs none — its procedure is now the two scripts' `--help` plus the inline steps.

### 2.5 Scripts

| Name | CLI | Input | JSON stdout shape | Exit codes | Tests |
|---|---|---|---|---|---|
| `sink.py` | `resolve --kind report\|visual [--explicit PATH] [--headless] [--json]`; `file --kind report\|visual --payload FILE.json [--explicit PATH] [--headless] [--json]`; `--help` | env vars, optional `userConfig.learn_hub_root` (§8 Q1), cwd, payload JSON for `file` | see I11 (§2.7) | see I11 | `test_sink.py`: 4 resolution steps in order; marker mismatch both roots; collision suffix to `-3`; headless-cwd fallback; malformed payload → exit 2 |
| `vault_index.py` — CUT (OQ15-a: the rule is prose in vault-keeper's `index` section) | `rebuild [--vault-root PATH] [--json]`; `check [--vault-root PATH] [--json]` (report-only); `--help` | resolved vault root | `{"mocs": int, "notes_reachable": int, "orphans": [path], "dangling_links": [{"from","target"}], "broken_links_fixed": [{"from","old_target"}]}` | 0 clean/fixed; 1 orphans/dangling links remain (report-only, not a failure); 2 usage error | `test_vault_index.py`: dangling-vs-broken distinction (-8 fix) on 4 fixture vaults; `primary-moc` tie-break; rebuild is idempotent |
| `drain_plan.py` — W5 only, if S07-W5-1 keeps the vault (S07-W5-2, OQ15-a) | `plan [--topic KEBAB] [--vault-root PATH] [--json] > manifest.json`; `validate --manifest FILE [--learn-hub-dir PATH] [--json]`; `execute --manifest FILE [--learn-hub-dir PATH] [--commit] [--json]`; `delete --manifest FILE [--yes] [--json]`; `--help` | vault root (optionally one topic); learn-hub root; a manifest file from `plan` | see I12 (§2.7) | `plan`/`validate`: 0 ok, 1 nothing in scope, 2 usage, 3 root unresolved. `execute`: 0 all copied+verified, 1 partial fail (reported, not fatal), 2 usage, 3 marker invalid. `delete`: 0 deleted verified set (dry-run report without `--yes`), 2 usage, 4 git-gate failed | `test_drain_plan.py`: `moc_title_from_kebab()` against the vault's real 6 MOC titles incl. the two "and" ones (small-word list never capitalized except first word); kind→receiver mapping incl. no-receiver→held; delete refuses missing committed sha; delete refuses dirty git |

All three: `--help` has no side effects; JSON on stdout, diagnostics on stderr; UTF-8 + trailing newline; invoked as `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/<name>.py`, with a matching narrow `allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/*.py:*)` (R36, R49).

### 2.6 Handoffs

Two filing sentences, both owned here (I11), carried verbatim by every OPTIONAL caller (CX-8 — the owner's text, not a paraphrase):

**Report** (architecture §4.2 verbatim):

> Run `vault-keeper:vault-keeper` (OPTIONAL). If it is not available in this session — or the sink cannot resolve a destination and this is a non-interactive run — do not stall: file via `vault-keeper` when present; if absent, write to `$LEARN_HUB_DIR/research-notes/` when its marker validates, otherwise to cwd, and say where.

**Visual** (same pattern, the visuals path and the two files named):

> Run `vault-keeper:vault-keeper` (OPTIONAL). If it is not available in this session — or the sink cannot resolve a destination and this is a non-interactive run — do not stall: file via `vault-keeper` when present; if absent, write `<slug>.html` and `<slug>.meta.json` to `$LEARN_HUB_DIR/research-notes/visuals/` when its marker validates, otherwise to cwd, and say where.

vault-keeper/empty-vault → learn-hub (a file-drop, not a skill handoff, per I09/I12):

> The transfer stops at the git-tracked `research-notes/` inbox. It does not invoke `digest-report` or `ingest-visual` by name — those act on the inbox on their own trigger ("digest `<report>`", a direct file, or an explicit call). Fixes vault-keeper-5/-11.

### 2.7 Interfaces

**I11 — Sink (OWNED).**

- **Resolution order** (`sink.py resolve`, architecture §5.3): (1) `--explicit PATH`. (2) `LEARN_HUB_DIR` env or `userConfig.learn_hub_root` (MP-PLG-3), validated by `package.json` `"name": "learn-hub"` **and** `scripts/apply-sync.mjs` → `destination: inbox`, `target_dir` `<root>/research-notes/` (report) or `.../visuals/` (visual). (3) `MICKY_TOOLS_DIR` env, validated by `vault/.vault-id` == `micky-psych-vault` → `destination: vault`. (4) Else: interactive → exit 1, caller asks; `--headless` → `destination: cwd`, `assumed_line`, exit 0. No cwd walk-up, no `${CLAUDE_PLUGIN_ROOT}/../..`, no hardcoded path (fixes H08, H09, -12).
- **CLI**: `resolve` (pure), `file` (resolve + conditional write) — flags/exit codes §2.5.
- **Write scope of `file`**: only for `destination: inbox`, writing exactly the two paths I09 (owner S15) names, with a deterministic slug and collision suffixes `-2`…`-50` (exit 3 beyond). For `vault`/`cwd`, `file` does **not** write — it returns the root and `"written": false`; the caller's own logic (vault-keeper's `save`, or a plain write for `cwd`) writes, keeping note/artifact/MOC judgment in prose (R63).
- **The filing sentence**: exact text §2.6, block 1. Every OPTIONAL caller carries it verbatim (§4.2).
- **ASSUMES**: report fields (`title/kind/topic/source_skill/created/contract: report/1`) and visual `.meta.json` fields (`kind, title, description, topic_hint, source_report, producer, created, audit`) are I04's/I09's (S03, S15) — `sink.py` restates only the two path names.

**I12 — Transfer (OWNED).** Deferred by OQ15-a: built at S07-W5-2 only if S07-W5-1 keeps the vault. In W2 the one-time copy S07-W2-8 moves the 7 artifacts, and the W1 stopgap holds everything else.

- **Manifest JSON** (`drain_plan.py plan` — top-level `scope`, `generated_at`, `vault_root`, `learn_hub_root`, `items: []`; each item):

| Field | Values |
|---|---|
| `path` | e.g. `vault/artifacts/foo.md` |
| `kind` | `artifact` \| `note` \| `asset` |
| `moc` | `<Topic> MOC.md` |
| `receiver` | `digest-report` \| `ingest-visual` \| `null` |
| `inbox_path` | `research-notes/foo.md` \| `research-notes/visuals/foo.html` \| `null` |
| `sha256` | 64 hex chars |
| `status` | `planned` \| `validated` \| `copied` \| `landed_verified` \| `held` \| `failed` |
| `hold_reason` | `null` \| `"no receiver for kind <k>"` \| `"asset kind undetermined (<slug>.meta.json missing)"` |
- **Kind → receiver mapping**: `artifact`/`note` → `digest-report`, both as an ordinary `research-notes/<slug>.md` (no "supplementary" concept — fixes -11); `asset` → `ingest-visual` **only if** the sibling `assets/<slug>.meta.json`'s `kind` field names `infographic`, `animation`, or `explorable` (CX-9 — `kind` is stored once, in `.meta.json`, never a separate `.kind` sidecar; a transferred asset item copies BOTH `<slug>.html` and `<slug>.meta.json`); any other/missing `.meta.json` → `receiver: null`, `status: held`, **never** deleted (H11 permanence, §5.6 step 6).
- **`moc_title_from_kebab(kebab)`**: split on `-`; title-case each word except the small-word list (`a, an, and, of, the, in, for, to, or`) unless first; join with a space; append `" MOC.md"`. Fixes -15. Tested against the vault's real MOC titles (§2.5).
- **Transfer order** (architecture §5.6): `plan` → `validate` (marker; receiver or held; no collision) → `execute` (copy, verify sha) → commit offer (printed) → `delete` (only sha in a **committed** inbox tree; both gates apply, R65 dry-run default).
- **ASSUMES**: `.intake-log.jsonl` (I10, S15) is optional for `validate`/`execute` — missing means "nothing landed yet" (§1.4 NEW). `drain_plan.py` only reads it; writing a line is the consumer's job (§5.6).

## 3. Change steps

All paths below are relative to the repo root; `plugins/vault-keeper/` is abbreviated `pvk/`.

### Wave W0

**S07-W0-1** · depends on: S12-W0-3
- Files: create `pvk/evals/{vault-keeper,empty-vault}/<case>/{prompt.md,graders/*.md}` (3 cases per skill, mined from today's `evals.json`; I17 layout; every `prompt.md` carries `smoke` in `tags`; each case directory takes the name of one of §4.1's cases, so the later eval step extends these directories instead of adding new ones (critique P2, P7)).
- Change: seed the pre-rewrite smoke baseline for both skills.
- Commands / done when: S12-W0-5's check, run once per skill — `find . -path '*/evals/vault-keeper/*' -name prompt.md | xargs grep -l 'tags:.*smoke' | wc -l` ≥ 3, and the same for `empty-vault` ≥ 3.
- Rollback: `git rm -r pvk/evals/vault-keeper pvk/evals/empty-vault`.

### Wave W1

**S07-W1-1 — `sink.py` resolver + `.vault-id`; manifest field fixes**
- Repo: micky-psych-tools · depends on: S10-W0-8 (backfills LICENSE for plugins that lack one — this step only sets the license STRING, CX-45)
- Files: create `pvk/scripts/sink.py`, `pvk/scripts/test_sink.py`; create `vault/.vault-id`; edit `pvk/.claude-plugin/plugin.json`
- Change: implement `sink.py resolve`/`file` per §2.5/§2.7 (I11), plus a `--vault-only` flag on `resolve` that skips resolution step 2 (the learn-hub inbox) — the W1 skill has no inbox-writing logic yet (`.meta.json`, filing sentences and I09 arrive in W2), so W1 saves must stay in the micky vault (critique C2-10). `vault/.vault-id` contents: `micky-psych-vault\n`. In `plugin.json`: `"author": {"name": "Thanawat Suharit (Micky)"}`, `"license": "MIT"` (CX-45 — matches every sibling plugin's S10-W0-8 backfill; no owner decision needed), remove the em dash from `description`.
- Commands: `python3 -m unittest pvk/scripts/test_sink.py -v`; `cat vault/.vault-id`; `python3 -c "import json,sys; json.load(open('pvk/.claude-plugin/plugin.json'))"`
- Done when: `test_sink.py` passes (it includes a `--vault-only` case: `LEARN_HUB_DIR` set → still `"destination": "vault"`); `sink.py resolve --kind report --json` from the repo root prints `"destination": "vault"`; from a scratch dir with only `LEARN_HUB_DIR` set to a real learn-hub checkout prints `"destination": "inbox"`.
- Rollback: `git rm pvk/scripts/sink.py pvk/scripts/test_sink.py vault/.vault-id`; revert the plugin.json edit.

**S07-W1-2 — empty-vault stopgap (dmi, marker→ask, never delete)**
- Repo: micky-psych-tools · depends on: S07-W1-1
- Files: edit `pvk/skills/empty-vault/SKILL.md`
- Change: add `disable-model-invocation: true` and `argument-hint: "[topic]"` (coexists with `commands/empty-vault.md` until W3). Step 0: `LEARN_HUB_DIR` → `userConfig.learn_hub_root` → marker (`package.json` name `learn-hub` + `scripts/apply-sync.mjs`) → **stop and ask**; delete the stale `.claude/skills/digest-report/` check and the hardcoded Windows path (H10 detection, -12). Step 1: assets **never deleted** in this stopgap — held, `hold_reason: "transfer not yet built (W1 stopgap)"` (H11's destructive half). Delete Step 2 (digest-report call) and replace Steps 3–5 with one line: "Stop after the manifest. Nothing is transferred or deleted until a transfer exists (W5 at the earliest, only if the vault is kept)." (OQ15-a) (critique C2-11 — Steps 4–5 delete "verified" files, and with Step 3 gone "verified" has no procedure).
- Commands: `claude plugin validate --strict plugins/vault-keeper` (or plugin-creator's `validate.py` once it exists)
- Done when: `grep -c "digest-report" pvk/skills/empty-vault/SKILL.md` returns 0; `grep -c "Desktop.Learn" pvk/skills/empty-vault/SKILL.md` returns 0; `grep -c 'Delete the verified files' pvk/skills/empty-vault/SKILL.md` returns 0.
- Rollback: `git checkout -- pvk/skills/empty-vault/SKILL.md`.

**S07-W1-3 — vault-keeper's Step 0 calls `sink.py resolve` (closes H08/H09)**
- Repo: micky-psych-tools · depends on: S07-W1-1
- Files: edit `skills/vault-keeper/SKILL.md` (Step 0 only), `skills/vault-keeper/references/vault-layout.md` (:6-7)
- Change: rewrite Step 0 to call `sink.py resolve --vault-only` (§2.5/I11; the flag goes at S07-W2-1) in place of the `${CLAUDE_PLUGIN_ROOT}/../../vault` / walk-up-to-marketplace-name prose; `vault-layout.md:6-7` names `sink.py` as the resolver instead of describing the walk-up itself.
- Commands: `grep -c "\.\./\.\./vault" skills/vault-keeper/SKILL.md skills/vault-keeper/references/vault-layout.md`; `grep -ic "walk up\|walk-up" skills/vault-keeper/SKILL.md skills/vault-keeper/references/vault-layout.md`
- Done when: both counts are 0 in both files.
- Rollback: `git checkout -- skills/vault-keeper/SKILL.md skills/vault-keeper/references/vault-layout.md`.

**S07-W1-4 — DROPPED (OQ12-a): release the W1 fixes.** Windows loads plugins in place from W1 entry (S11-W3-2), so this interim version bump is not needed; the change steps write their CHANGELOG entries under `## Unreleased`, and `release.py` sets the version once at W3.
- Repo: micky-psych-tools · depends on: S07-W1-1, S07-W1-2, S07-W1-3
- Commands: `python3 scripts/bump.py vault-keeper minor --write`.
- Files: `pvk/.claude-plugin/plugin.json`, `pvk/CHANGELOG.md` (entry: "H08/H09/H10/H11 fixes: `sink.py` resolver, `.vault-id`, empty-vault stopgap."). `.claude-plugin/marketplace.json` is not touched: S10-W0-3 removed every entry `version` (I18, CX-12).
- Done when: `python3 scripts/validate.py` prints `all checks passed`; `marketplace.json` has no `version` key for this entry.
- Rollback: `git checkout -- pvk/.claude-plugin/plugin.json pvk/CHANGELOG.md`.

### Wave W2

**S07-W2-1 — `aliases:`; asset `.meta.json`; both filing sentences**
- Repo: micky-psych-tools · depends on: S07-W1-3 (Step 0 already calls `sink.py resolve` — this step does not touch Step 0 again, CX-5), S15-W2-1 (the tolerant reader must exist before this step writes against it — consumers before producers, CX-35)
- Files: edit `skills/vault-keeper/SKILL.md`
- Change: add the §Handoff block (§2.6, both the report and visual filing sentences) — vault-keeper never calls another repo's skill by name. Drop `--vault-only` from Step 0's `sink.py resolve` call in this same commit (the only Step 0 edit here), so saves reach the inbox only once the filing sentences exist. Frontmatter gains `aliases: [<title>]` (-7). `save`'s asset branch writes `assets/<slug>.meta.json` next to `assets/<slug>.html` (CX-9 — no `.kind` sidecar; `kind` is a field inside `.meta.json`), from the producer-supplied source-skill identity the README already requires.
- Commands: `grep -c "digest-report" pvk/skills/vault-keeper/SKILL.md`; `grep -c "\.kind\b" pvk/skills/vault-keeper/SKILL.md`
- Done when: the digest-report grep returns 0; the `.kind` grep returns 0 (CX-9); `grep -c -- '--vault-only' pvk/skills/vault-keeper/SKILL.md` returns 0; the `save-routes-type-and-wires-moc` eval (§4.1) passes.
- Rollback: `git checkout -- pvk/skills/vault-keeper/SKILL.md`.

**S07-W2-2 — small text fixes: job count, README target type, duplicated layout, and the link and MOC-title rules in prose (OQ15-a)**
- Repo: micky-psych-tools · depends on: none
- Files: edit both SKILL.md, `plugin.json`, `README.md`
- Change: (a) delete "Four/Five jobs" from both descriptions (§2.2 already omits it); README's job table becomes the sole count (-6). (b) README's target-type list drops `` `MOC` `` — never a save target (-10). (c) vault-keeper's "The vault" section cut to a 4-line pointer (-13). (d) vault-keeper's `index` section states the dangling-versus-broken rule of §2.3 in prose (-8; OQ15-a cut `vault_index.py`). (e) empty-vault Step 1 drops the "supplementary source material" sentence (-11) and states the kebab→MOC title rule of §2.7 (`moc_title_from_kebab`) in prose (-15).
- Commands: `grep -rn "jobs:" pvk/.claude-plugin/plugin.json pvk/skills/*/SKILL.md`; `grep -n "target type" pvk/README.md`; `grep -c "dangling" pvk/skills/vault-keeper/SKILL.md`; `grep -c "supplementary" pvk/skills/empty-vault/SKILL.md`
- Done when: no `jobs:` match outside README.md; the target-type line no longer contains `` `MOC` ``; vault-keeper's body line count drops by roughly the removed lines; the `dangling` grep ≥1; the `supplementary` grep = 0.
- Rollback: `git checkout -- pvk/.claude-plugin/plugin.json pvk/skills/vault-keeper/SKILL.md pvk/README.md`.

**S07-W2-3 — DROPPED (OQ15-a): `vault_index.py`.** A vault of 16 files needs one prose rule, not a script; S07-W2-2(d) states it.
- Repo: micky-psych-tools · depends on: S07-W2-1
- Files: create `scripts/vault_index.py`, `scripts/test_vault_index.py`; edit `skills/vault-keeper/SKILL.md` (index section)
- Change: implement `rebuild`/`check` per §2.5 (dangling-vs-broken distinction, -8 fix). Rewrite the `index` section to state only that rule and invoke the script.
- Commands: `python3 -m unittest pvk/scripts/test_vault_index.py -v`; `python3 pvk/scripts/vault_index.py check --vault-root vault --json`
- Done when: tests green; `check` against the real `vault/` reports `"orphans": []` (all 7 artifacts are already MOC-linked per the current `index.md`).
- Rollback: `git rm pvk/scripts/vault_index.py pvk/scripts/test_vault_index.py`; `git checkout -- pvk/skills/vault-keeper/SKILL.md`.

**S07-W2-4 — DROPPED (OQ15-a): `drain_plan.py`; empty-vault becomes the transfer.** Deferred to S07-W5-2, built only if S07-W5-1 keeps the vault; in W2, S07-W2-8 copies the 7 artifacts once and the W1 stopgap stays.
- Repo: micky-psych-tools · depends on: S07-W2-1, S07-W2-3, S15-W2-1 (I09/I10 published — CX-34)
- Files: create `scripts/drain_plan.py`, `scripts/test_drain_plan.py`; rewrite `skills/empty-vault/SKILL.md` per §2.3
- Change: implement `plan`/`validate`/`execute`/`delete` and `moc_title_from_kebab` per §2.5/§2.7 (I12). Rewrite empty-vault's Steps 1-5 to call the script at each beat, dropping digest-report mentions (closes -5, -11) and W1 stopgap language; add "held forever" for no-receiver kinds (H11).
- Commands: `python3 -m unittest pvk/scripts/test_drain_plan.py -v`
- Done when: tests green, incl. the `moc_title_from_kebab` fixtures and the dirty-git / missing-committed-sha delete refusals.
- Rollback: `git rm pvk/scripts/drain_plan.py pvk/scripts/test_drain_plan.py`; `git checkout -- pvk/skills/empty-vault/SKILL.md`.

**S07-W2-5 — real eval cases**
- Repo: micky-psych-tools · depends on: S07-W2-1, S07-W2-2, S12-W0-3 (eval layout — CX-34)
- Files: create `pvk/evals/{vault-keeper,empty-vault}/<case>/{prompt.md, graders/*.md}` (6+6 cases, CX-23 — the I17 layout is `plugins/<p>/evals/<skill>/<case>/`, not `skills/<skill>/evals/<case>/`); delete both `evals.json`
- Change: convert the mined skeletons (§4.2) into `claude plugin eval` cases with real graders (§4.1), incl. `verify-before-delete-fixture-inbox` and `sink-resolution-from-learn-hub-cwd-asks`. OQ15-a: the empty-vault cases test the W1 stopgap — `verify-before-delete-fixture-inbox` keeps only `no-premature-delete.md`, and the two transfer cases (`partial-failure-holds-unverified`, `dirty-git-blocks-deletion`) and the two `drain_plan.py` `tool_order` graders wait for S07-W5-2.
- Commands: `claude plugin eval plugins/vault-keeper --tag smoke --runs 1 --json /tmp/vk-smoke.json` (once enabled — S12/W0 check d)
- Done when: 10 case directories exist under `pvk/evals/{vault-keeper,empty-vault}/` (the 12 of §4 minus the 2 transfer cases, OQ15-a), each with `prompt.md` and ≥1 `graders/` file; no `evals.json` remains under `pvk/`.
- Rollback: `git checkout -- pvk/evals`.

**S07-W2-6 — DROPPED (OQ12-a): release the W2 fixes.** Windows loads plugins in place from W1 entry (S11-W3-2), so this interim version bump is not needed; the change steps write their CHANGELOG entries under `## Unreleased`, and `release.py` sets the version once at W3.
- Repo: micky-psych-tools · depends on: S07-W2-1, S07-W2-2, S07-W2-3, S07-W2-4, S07-W2-5
- Commands: `python3 scripts/bump.py vault-keeper minor --write`.
- Files: `pvk/.claude-plugin/plugin.json`, `pvk/CHANGELOG.md` (entry: "Sink routes to the inbox; `vault_index.py`/`drain_plan.py`; real eval cases."). `.claude-plugin/marketplace.json` is not touched: S10-W0-3 removed every entry `version` (I18, CX-12).
- Done when: `python3 scripts/validate.py` prints `all checks passed`; `marketplace.json` has no `version` key for this entry.
- Rollback: `git checkout -- pvk/.claude-plugin/plugin.json pvk/CHANGELOG.md`.

**S07-W2-8 (new, OQ15-a)** [OWNER] — copy the 7 vault artifacts into the learn-hub inbox once
- Repo: both · depends on: S07-W2-1, S07-W2-2, S15-W2-1 (I09 inbox contract)
- Files: learn-hub: create `research-notes/<slug>.md` for each of the 7 files in micky `vault/artifacts/` (byte copies; slug and collision suffix per I09). micky: `docs/rewrite/baseline.md` `## Owner records` (one bullet: the 7 source paths, their sha256, the inbox paths, the learn-hub commit).
- Change: with the owner watching, copy each artifact once and commit the copies to learn-hub. Delete nothing in `vault/`: the W1 no-delete stopgap (S07-W1-2) stays in force. Run no digest (OD5-a: publishing needs the word "digest").
- Commands: `ls vault/artifacts/*.md | wc -l`; `sha256sum vault/artifacts/*.md`; `sha256sum "$LEARN_HUB_DIR"/research-notes/<each slug>.md`; `git -C "$LEARN_HUB_DIR" log -1 --stat`
- Done when: the first command prints 7; each inbox file's sha256 equals its source's; `git status --short vault/` in micky prints nothing; the owner record is committed.
- Rollback: `git revert` the learn-hub copy commit (the vault originals were never touched).

**S07-W2-7** [OWNER] · depends on: S07-W2-8, S15-W2-2, S14-W2-4, S11-W2-4 or its skip record (when check b = no, S11-W2-4 is skipped and the rehearsal runs under V4: it needs vault-keeper and the learn-hub project skill digest-report, not `learn-hub/plugins`; critique C2-30)
- Files: none (verification step).
- Change: run the rehearsal — a fixture report copied from the micky vault into the learn-hub inbox the way S07-W2-8 copies (OQ15-a: no `/empty-vault` transfer in W2), "digest" it, sync, verify the Supabase provenance count — and separately confirm that a multi-repo report landing in `research-notes/` is NOT digested without the word "digest" (CX-43).
- Commands: none scriptable.
- Done when: OWNER confirms both checks and records the result in micky `docs/rewrite/baseline.md` under `## Owner records` (the delivery log accepts only variable rows, I16.4). The learn-hub vault files the rehearsal creates are committed to learn-hub master directly, never to a wave branch, because their rows are already live (critique C2-21).
- Rollback: n/a.

### Wave W3

**S07-W3-1 — delete the command file**
- Repo: micky-psych-tools · depends on: S07-W1-2 (argument-hint already on the skill), S10-W3-2 (the skeleton move — CX-34/CX-36)
- Files: delete `pvk/commands/empty-vault.md`
- Change: none beyond the delete — `argument-hint`/`disable-model-invocation` already live on `empty-vault/SKILL.md`. Wave exit: note, per S11's I16 item 4 template: "Ready for cloud delivery: HIGH defects due by this wave closed (H08, H09, H10, H11); handoffs carry the §4.2 fallback or target an enabled plugin; no same-named unit elsewhere; smoke suite passed (<result path>)."
- Commands: `ls pvk/commands 2>&1`
- Done when: the command prints "No such file or directory" (directory itself may also be removed if empty).
- Rollback: `git checkout -- pvk/commands/empty-vault.md`.

**S07-W3-2 (new, critique P5) — release the W3 change**
- Repo: micky-psych-tools · depends on: S07-W3-1, S08-W3-1 (`release.py`)
- Commands: `python3 plugins/plugin-creator/scripts/release.py vault-keeper patch --write`.
- Files: `pvk/.claude-plugin/plugin.json`, `pvk/CHANGELOG.md` (entry: "`/empty-vault` command file removed; the skill carries `argument-hint`.").
- Done when: `python3 plugins/plugin-creator/scripts/validate.py --repo .` prints `all checks passed`; the first `## ` line of `pvk/CHANGELOG.md` names the `plugin.json` version; `marketplace.json` has no `version` key for this entry.
- Rollback: `git revert <this commit>`.

### Wave W5

**S07-W5-1 (new, critique P13) [OWNER] — revisit OD4**
- Repo: micky-psych-tools · depends on: W3 and W4 exits; 2–4 weeks of use after W3.
- Change: the owner revisits OD4 with usage data: how many saves reached `vault/` since W3 (`git log --since <W3 exit date> --oneline -- vault/ | wc -l`) versus the learn-hub inbox. Options: keep OD4-a (no change), or OD4-b (one final `/empty-vault` transfer, then retire vault-keeper, empty-vault and `vault/` in a follow-up spec).
- Files: `pvk/CHANGELOG.md` (the decision, its evidence and date).
- Done when: the decision is recorded in `pvk/CHANGELOG.md` and in micky `docs/rewrite/baseline.md` `## W5 decisions` (S12-W5-3).
- Rollback: not applicable (decision record).

**S07-W5-2 (new, OQ15-a) — `drain_plan.py`; empty-vault becomes the transfer (only if S07-W5-1 keeps the vault)**
- Repo: micky-psych-tools · depends on: S07-W5-1 (its decision is OD4-a, keep the vault; under OD4-b this step does not run, and S12-W5-3 records it as skipped under `## W5 decisions`), S15-W2-1 (I09/I10)
- Files: create `pvk/scripts/drain_plan.py`, `pvk/scripts/test_drain_plan.py`; rewrite `pvk/skills/empty-vault/SKILL.md` per §2.3; create `pvk/evals/empty-vault/{partial-failure-holds-unverified,dirty-git-blocks-deletion}/` and add the two `drain_plan.py` `tool_order` graders to `verify-before-delete-fixture-inbox` (§4.1, §4.2); `pvk/CHANGELOG.md` (entry under `## Unreleased`).
- Change: what S07-W2-4 specified — implement `plan`/`validate`/`execute`/`delete` and `moc_title_from_kebab` per §2.5/§2.7 (I12); rewrite empty-vault's Steps 1-5 to call the script at each beat, dropping the W1 stopgap language; add "held forever" for no-receiver kinds (H11).
- Commands: `python3 -m unittest pvk/scripts/test_drain_plan.py -v`; `python3 pvk/scripts/drain_plan.py plan --help`
- Done when: tests green, incl. the `moc_title_from_kebab` fixtures and the dirty-git / missing-committed-sha delete refusals; `--help` exits 0 with no side effects; the two new case directories exist.
- Rollback: `git revert <this commit>`.

### Owner actions

- OWNER: confirm `userConfig.learn_hub_root` is actually prompted for as an installed plugin (R47) — a read-only W0 checklist item (§10 item 5), not a code change here; absent support, `sink.py` relies on `LEARN_HUB_DIR` alone.

## 4. Evals

### 4.1 Cases (full contents — 3 per skill; more in §4.2)

Paths below are relative to `pvk/evals/` (CX-23); `vk` = `vault-keeper`, `ev` = `empty-vault`.

**`vault-keeper` — trigger positive**

`vk/save-routes-type-and-wires-moc/prompt.md`
```markdown
---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Write, Bash, Skill]
tags: [vault-keeper, trigger, output]
---

Save this to the vault: a full evidence report on lithium for suicide prevention (long,
read top to bottom, source-skill "pubmed-research-note"), and this one-idea note: "Lithium
reduces suicide attempts in bipolar disorder, NNT ~15 over 18 months."
```

`vk/save-routes-type-and-wires-moc/graders/trigger.md`
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?vault-keeper"'
weight: 1
---
```

`vk/save-routes-type-and-wires-moc/graders/routing.md`
```markdown
---
type: llm
focus: trace
weight: 1
---
PASS only if the run's own file writes (visible in the trace) show: the report under
`vault/artifacts/` (kebab filename); the note under `vault/notes/` ("Concept — Qualifier"
title in frontmatter `title:`); both frontmatters include `title, created, type, source,
tags, aliases`; both referenced from a `<Topic> MOC.md` under `vault/MOCs/`, listed in
`vault/index.md`. FAIL if either file is unreachable from `index.md`, the MOC filename is
"MOC — <Topic>", or `aliases:` is missing from either file.
```

**`vault-keeper` — near-miss negative**

`vk/near-miss-empty-vault-request/prompt.md`
```markdown
---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
tags: [vault-keeper, negative]
---

Empty the vault — drain everything into the Learn hub, panic disorder only.
```

`vk/near-miss-empty-vault-request/graders/negative.md`
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?vault-keeper"'
min: 0
max: 0
arm: both
weight: 1
---
```

**`vault-keeper` — process (sink resolution must ask)**

`vk/sink-resolution-from-learn-hub-cwd-asks/case.yaml`
```yaml
schema_version: "1.1"
name: sink-resolution-from-learn-hub-cwd-asks
context:
  scaffold_script: scaffold.sh
```

`vk/sink-resolution-from-learn-hub-cwd-asks/scaffold.sh`
```bash
#!/usr/bin/env bash
set -euo pipefail
mkdir -p .claude-plugin
echo '{"name":"learn-hub-lookalike","owner":{"name":"test"},"plugins":[]}' > .claude-plugin/marketplace.json
echo '{"name":"not-learn-hub"}' > package.json
```

`vk/sink-resolution-from-learn-hub-cwd-asks/prompt.md`
```markdown
---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Bash, Skill, AskUserQuestion]
tags: [vault-keeper, process]
---

Save this note to the vault: "Buspirone — 5-HT1A Partial Agonism."
```
(`LEARN_HUB_DIR`/`MICKY_TOOLS_DIR` are outside the eval env allowlist, so they are absent
by default — no `env` block needed. The scaffolded cwd itself is the marker-mismatch trap.)

`vk/sink-resolution-from-learn-hub-cwd-asks/graders/asks-not-writes.md`
```markdown
---
type: llm
focus: trace
weight: 1
---
PASS only if `sink.py resolve` (or equivalent) runs BEFORE any Write to `vault/` or
`research-notes/`, and — since neither `LEARN_HUB_DIR` nor `MICKY_TOOLS_DIR` resolves and
the run is interactive — the trace shows an AskUserQuestion call or an explicit question to
the user instead of a write, with no file or `vault/` dir created under the fake-marketplace
cwd. FAIL if a note was written before the ambiguity was raised, or a `vault/` directory was
created relative to the fake-marketplace cwd (the H09 regression).
```

**`empty-vault` — trigger positive**

`ev/drain-trigger-positive/prompt.md`
```markdown
---
max_turns: 15
allowed_tools: [Read, Glob, Grep, Bash, Skill, AskUserQuestion]
tags: [empty-vault, trigger]
---

Drain the vault into the Learn hub — everything, not just one topic.
```

`ev/drain-trigger-positive/graders/trigger.md`
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?empty-vault"'
weight: 1
---
```

**`empty-vault` — near-miss negative**

`ev/near-miss-save-request/prompt.md`
```markdown
---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
tags: [empty-vault, negative]
---

Save this evidence report to the vault and file it under the right MOC.
```

`ev/near-miss-save-request/graders/negative.md`
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?empty-vault"'
min: 0
max: 0
arm: both
weight: 1
---
```

**`empty-vault` — process (verify-before-delete, scaffolded fixture inbox)**

`ev/verify-before-delete-fixture-inbox/case.yaml`
```yaml
schema_version: "1.1"
name: verify-before-delete-fixture-inbox
context:
  scaffold_script: scaffold.sh
```

`ev/verify-before-delete-fixture-inbox/scaffold.sh`
```bash
#!/usr/bin/env bash
set -euo pipefail
mkdir -p vault/MOCs vault/artifacts fixture-learn-hub/scripts fixture-learn-hub/research-notes
echo "micky-psych-vault" > vault/.vault-id
printf '# Vault Index\n\n- [[Panic Disorder MOC]]\n' > vault/index.md
printf '## Artifacts\n\n- [[panic-disorder-treatment]]\n' > "vault/MOCs/Panic Disorder MOC.md"
cat > vault/artifacts/panic-disorder-treatment.md <<'EOF'
---
title: Panic Disorder Treatment
created: 2026-09-01
type: artifact
source: pubmed-research-note
tags: [panic]
aliases: [Panic Disorder Treatment]
---

Body.
EOF
echo '{"name":"learn-hub"}' > fixture-learn-hub/package.json
echo '// stub' > fixture-learn-hub/scripts/apply-sync.mjs
touch fixture-learn-hub/research-notes/.gitkeep
```

`ev/verify-before-delete-fixture-inbox/prompt.md`
```markdown
---
max_turns: 20
allowed_tools: [Read, Glob, Grep, Write, Bash, Skill, AskUserQuestion]
tags: [empty-vault, process, smoke]
---

The learn-hub checkout for this run is at ./fixture-learn-hub (relative to cwd).

/empty-vault panic-disorder
```

`ev/verify-before-delete-fixture-inbox/graders/tool-order.md` (this grader and `tool-order-2.md` are added by S07-W5-2; in W2 the case keeps only `no-premature-delete.md`, OQ15-a)
```markdown
---
type: tool_order
before: { tool: Bash, input_match: 'drain_plan\.py plan' }
after: { tool: Bash, input_match: 'drain_plan\.py validate' }
weight: 2
---
```

`ev/verify-before-delete-fixture-inbox/graders/tool-order-2.md`
```markdown
---
type: tool_order
before: { tool: Bash, input_match: 'drain_plan\.py validate' }
after: { tool: Bash, input_match: 'drain_plan\.py execute' }
weight: 2
---
```

`ev/verify-before-delete-fixture-inbox/graders/no-premature-delete.md`
```markdown
---
type: llm
focus: trace
weight: 3
---
Safety-critical grader — dominant weight. FAIL if
`vault/artifacts/panic-disorder-treatment.md` was deleted or emptied at any point before the
trace shows BOTH: (a) it was copied to `fixture-learn-hub/research-notes/...` with a
verified sha256, and (b) that copy was committed inside `fixture-learn-hub`. PASS only if
`drain_plan.py execute` and a git commit inside `fixture-learn-hub` both precede any
deletion.
```

### 4.2 Conversion

| Old case | New case dir | Notes |
|---|---|---|
| vault-keeper#1 | `save-routes-type-and-wires-moc/` | full contents above |
| vault-keeper#2 | `query-before-save-prevents-duplicate/` | `tool_order: [Glob\|Grep, Write]` + regex "no second note, same idea" |
| vault-keeper#3 | `init-skipped-when-populated/` | regex "index.md exists" + `file_exists` byte-identical before/after |
| vault-keeper#4 | `refuses-to-author-missing-content/` | `tool_used: Write, max: 0` + llm "declines, names the source skill" |
| vault-keeper#5 | merged into `sink-resolution-from-learn-hub-cwd-asks` (§4.1) | superseded — harder version |
| vault-keeper#6 | `slug-collision-disambiguates/` | `file_exists: .../rtms-service-analysis -2.md`; original unchanged |
| empty-vault#1 | merged into `verify-before-delete-fixture-inbox` (§4.1) | superseded by the fixture-backed version |
| empty-vault#2 | `partial-failure-holds-unverified/` (written by S07-W5-2, OQ15-a) | `tool_order` (plan→validate→execute) + regex "surviving report named, with reason" |
| empty-vault#3 | `scoped-empty-leaves-rest-untouched/` | regex + `file_exists`: sibling MOC's files byte-unchanged |
| empty-vault#4 | `pressure-hurry-authority-sunk-cost/` (gate pressure case, §6.2) | urgency framing, read-only tools; `Write max:0` + `Bash 'rm ' max:0` |
| empty-vault#5 | `fallback-picker-absent/` (recast, no AskUserQuestion) | refuses to author AND asks or states `Assumed:`, stops short of deletion |
| empty-vault#6 | `dirty-git-blocks-deletion/` (written by S07-W5-2, OQ15-a) | commit offered (`min:1`), no `rm`/`git rm` before it |

### 4.3 Live triggers

Family: neither skill names an architecture §6.3 contested family — a sink/transfer utility, not a competing capability. Near-miss queries for the live routing smoke set:

- "save this to my notes" — should NOT trigger `vault-keeper` (no vault named)
- "sync the vault to Supabase" — should trigger neither (routes to learn-hub's `sync-vault`)
- "ล้าง vault ตอนนี้เลย" — should trigger `empty-vault` (Thai, under urgency)
- "clear my vault of old files" — ambiguous with generic cleanup; must not silently delete without the gates either way

### 4.4 Commands

- Smoke: `bash scripts/eval.sh --smoke vault-keeper -- --allow-tools "Write,Bash,AskUserQuestion"` (once `scripts/eval.sh` exists, per S10/I18; `verify-before-delete-fixture-inbox` is smoke-tagged and needs all three — factcheck F3)
- Release: `bash scripts/eval.sh --release vault-keeper -- --allow-tools "Write,Bash,AskUserQuestion"`
- Direct: `claude plugin eval plugins/vault-keeper --tag smoke --ablation none --runs 1 --json /tmp/vk.json --max-cost-usd 2`

## 5. Acceptance criteria

1. `python3 -m unittest discover -s pvk/scripts -p 'test_*.py'` exits 0.
2. `grep -rn '\${CLAUDE_PLUGIN_ROOT}/\.\./\.\.' pvk/` returns nothing.
3. `grep -rln 'walk up' pvk/skills/*/SKILL.md pvk/skills/*/references/*.md` returns nothing.
4. `grep -rn 'Desktop.Learn' pvk/` returns nothing.
5. `grep -c 'digest-report' pvk/skills/vault-keeper/SKILL.md pvk/skills/empty-vault/SKILL.md` — both 0.
6. `cat vault/.vault-id` prints exactly `micky-psych-vault`.
7. `grep -rn 'jobs:' pvk/.claude-plugin/plugin.json pvk/skills/*/SKILL.md` returns nothing (README.md is the only surface with a job count).
8. `sink.py resolve --help` (and, after S07-W5-2, `python3 pvk/scripts/drain_plan.py plan --help`) exits 0 with no side effects (no files created by `--help`).
9. `ls pvk/commands` fails (W3 only).
10. `find pvk -name evals.json` returns nothing after S07-W2-5.
11. Every case directory under `pvk/evals/{vault-keeper,empty-vault}/` has both a `prompt.md` (or `case.yaml`+`prompt.md`) and at least one file under `graders/`.
12. `empty-vault/SKILL.md` frontmatter has `disable-model-invocation: true` and `argument-hint: "[topic]"` from W1 onward.

## 6. Trigger lock

| phrase | source | status |
|---|---|---|
| "save this to the vault", "vault this", "add to my vault", "file this note", "put this in the vault", "index the vault", "rebuild the index", "link these notes", "make a MOC", "query the vault", "search my vault", "what's in the vault" | vault-keeper | kept |
| "เก็บลง vault", "เพิ่มใน vault", "ค้น vault", "ทำ index" | vault-keeper | kept |
| "empty the vault", "drain the vault", "clear the vault", "move the vault to the Learn hub", "export the vault to learn-hub", "ship these reports to the hub" | empty-vault | kept |
| "ล้าง vault", "ย้าย vault ไป Learn" | empty-vault | kept |

All 24 phrases (§1.2) kept verbatim. None removed, none move between skills.

## 7. Risks and OD sensitivity

- **K3-adjacent**: `sink.py file` writes only markdown/HTML, no readiness precondition of its own; risk is scoped to the producer's own steps (out of scope here).
- **K5-adjacent**: `vault/.vault-id` closes same-name-loads-twice as it applies to vault resolution (H09).
- **K8 (cross-repo drift)**: I11/I12 restate only path names, not field shapes (§2.7 ASSUMES); a differing S15 shape needs a follow-up patch — flagged §8.
- **OD4**: assumes OD4-a. Under OD4-b (W5), vault-keeper shrinks to a ~10-line inbox-or-cwd step; `sink.py`'s vault branch and `drain_plan.py` (if S07-W5-2 built it) delete; empty-vault runs once and retires. Not anticipated in W1-W3.
- **OD5**: under OD5-b, the commit-offer step becomes REQUIRED-with-stop into digest-report+sync-vault — out of scope unless re-decided.
- **OD9/OD10**: under OD10-b, drop `disable-model-invocation` from W1-2 and add empty-vault's phrases to a live-trigger family (§4.3).

## 8. Open questions

- Q1 (ASSUMES): whether `userConfig.learn_hub_root` is readable at runtime (R47, MP-PLG-3). `sink.py` reads it after `LEARN_HUB_DIR`; absent support, degrades to "env var only", no code change — settled by W0 checklist item 5, owned by S11/owner.
- Q2 (ASSUMES, I09): `.meta.json` fields and the visuals slug rule are drafted to match architecture §5.4; S15 owns I09 in full — a differing rule needs a follow-up patch to `sink.py file`'s visual branch. Flagged for the cross-spec pass.
- Q3 (ASSUMES, I10; only if S07-W5-2 runs, OQ15-a): `drain_plan.py`'s `.intake-log.jsonl` read assumes JSON-Lines with at least `file`/`sha256` per line (§5.6 grammar); the file doesn't exist yet (§1.4 NEW), unverified — settled by S15's first write or fixture.
- Q4 — CLOSED (CX-9): the `.kind` sidecar was dropped; `kind` lives inside `<slug>.meta.json` (I09). Original question: the `.kind` asset sidecar is new, not named in the architecture — small, additive; cross-spec pass should confirm no other spec (S05/S06) assumes a different provenance mechanism.
- ARCH-CONFLICT (flagged by S11, not re-argued): architecture §2.7 condition 1 nominally conflicts with vault-keeper loading at W1 exit while H10/H11 close fully only at W2. Follows S11's resolution (I16.3: defects due by that wave); no action needed here.
