# Spec S14: learn-hub delivery plugin and retirements

| Field | Value |
|---|---|
| Repos | learn-hub (plus micky-psych-tools for the ledger merge target) |
| Units (today → target) | `plugins/learn-hub-session` (new, hooks-only); `.claude-plugin/marketplace.json` (learn-hub-local catalog, deleted); `plugins/intent-lock` (fork: ledger merged into micky then deleted); `plugins/pubmed-research-note` (fork, deleted); `plugins/comprehensive-review` (fork + `commands/comprehensive-review.md`, deleted); `plugins/source-to-vault` (deleted, W1) |
| Waves | W1 (retire `source-to-vault`: H17–H20), W2 (create `learn-hub-session`; merge + delete the intent-lock fork; delete the pubmed/CR forks; delete the `learn-hub-local` catalog) |
| Owner decisions assumed | OD1-a, OD2-a |
| Defects closed | 35 of 35 assigned (HIGH: H06, H14, H17, H18, H19, H20, H48, H49) |
| Interfaces owned | I15 |
| Interfaces consumed | I03 (owner S01), I13 (owner S13), I14 (owner S13), I16 (owner S11), I17 (owner S12) |
| Depends on specs | S01 (ledger grammar, consumed not required to land first), S03 (pubmed producer wiring), S04 (CR producer wiring), S07 (vault-keeper sink), S11 (Windows catalog uninstall, delivery schedule), S13 (session-start.sh root resolution) |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| path | lines | bytes | est. tokens | role |
|---|---|---|---|---|
| `.claude-plugin/marketplace.json` | 48 | 2,215 | 551 | learn-hub-local catalog, 8 entries, never registered (H14) |
| `plugins/source-to-vault/skills/ingest-source/SKILL.md` | 161 | 9,160 | 2,277 | the hazardous pipeline (H17–H20) |
| `plugins/source-to-vault/commands/ingest.md` | 17 | 770 | 190 | thin `/ingest` forward |
| `plugins/source-to-vault/.claude-plugin/plugin.json` | 6 | 229 | 57 | manifest, no `$schema`, no version bump path |
| `plugins/intent-lock/skills/intent-lock/SKILL.md` | 249 | 26,054 | 6,458 | fork, byte-identical to micky's (§1.4) |
| `plugins/intent-lock/skills/misread-capture/SKILL.md` | 69 | 5,006 | 1,225 | fork |
| `plugins/intent-lock/skills/intent-lock/references/misreads.md` | 47 | 2,446 | ~606 | the second ledger (H06) — confirmed byte-identical to micky's copy (§1.4) |
| `plugins/intent-lock/README.md` | 47 | 2,839 | 705 | claims "exactly one ledger file" (contradicted by its own existence) |
| `plugins/intent-lock/CHANGELOG.md` | 64 | 5,983 | 1,486 | identical to micky's, no fork note |
| `plugins/pubmed-research-note/skills/pubmed-research-note/SKILL.md` | 327 | 20,628 | 5,074 | fork, only delta is the filing path (H48 evidence) |
| `plugins/pubmed-research-note/.mcp.json` | 12 | 236 | 59 | 1 of 6 byte-identical MCP copies (B10) |
| `plugins/comprehensive-review/skills/comprehensive-review/SKILL.md` | 232 | 13,197 | 3,258 | fork, digest+live-sync default (H49) |
| `plugins/comprehensive-review/commands/comprehensive-review.md` | 15 | 665 | 163 | thin forward |
| `plugins/comprehensive-review/.mcp.json` | 12 | 236 | 59 | duplicate MCP declaration |
| `.claude/hooks/session-start.sh` | 92 | 4,759 | 1,182 | today's single-repo hook; S13 rewrites it in W1 (I14) |
| `.claude/settings.json` | 25 | — | — | registers `session-start.sh` for single-repo sessions only |

### 1.2 Descriptions (of the units being retired — for closure evidence, not rewrite)

| skill | yaml_valid | desc chars | `Use when` offset | `Not for` present | quoted triggers |
|---|---|---|---|---|---|
| `ingest-source` (source-to-vault) | true | 252 | -1 (none) | no | `/ingest`, "ingest this PDF/EPUB", "import notes from <file>", "turn this book into notes" |
| `intent-lock` (fork) | **false** | — | — | yes (prose) | same as micky's copy (byte-identical body, §1.4) |
| `misread-capture` (fork) | true | 789 | 398 | yes (prose) | "this isn't what I wanted", "you misunderstood", "that's not it", "I asked for X and got Y", "you wasted my time", "ไม่ใช่ที่ผมต้องการ", "เข้าใจผิด", "ไม่ใช่แบบนี้" |
| `pubmed-research-note` (fork) | true | 991 | 225 | yes | "research", "what does the literature say about", "search PubMed for", "is X true", "should I use X for Y", "หางานวิจัย", "ทบทวนหลักฐาน", "ค้น PubMed", "จริงหรือเปล่า", "just search", "atomize", "ทำโน้ต", "comprehensive review of X" |
| `comprehensive-review` (fork) | true | 1,011 | 376 | yes | "comprehensive review of X", "full review of X", "whole-disorder review", "academic review", "review the whole topic", "รีวิวทั้งโรค", "should I use X for Y" |

`ingest-source`'s description has no `Not for` clause at all (confirms source-to-vault-3: no negative scope against atomize-book/pdf-pipeline/ingest-article). `intent-lock` fork fails strict YAML — the same defect as micky's own copy (same bytes); not this spec's fix, since the whole file is deleted rather than repaired (owned by S01 for the surviving copy).

### 1.3 Defects — every assigned id, exactly once

| id | sev | H# | evidence (re-opened) | problem | fix step | wave |
|---|---|---|---|---|---|---|
| source-to-vault-1 | H | H17 | SKILL.md:8-10, :140-141 | writes `topics`/`notes` rows via `execute_sql` with no `/vault` `.md` — the "DB rows can outlive their vault source" trap, unrecoverable by `sync:apply` | S14-W1-1 (audit), S14-W1-2 (retire) | W1 |
| source-to-vault-2 | H | H18 | SKILL.md:27-28 "process every `.pdf`/`.epub` under `Book/`", :128-129 "create-only … apply immediately" | no-arg batch-ingest of the shared inbox with no confirmation on create-only paths | S14-W1-2 | W1 |
| source-to-vault-3 | H | H19 | SKILL.md:3, no `Not for` (§1.2) | routing collision with atomize-book/pdf-pipeline/ingest-article, no negative scope | S14-W1-2 | W1 |
| source-to-vault-4 | H | H20 | SKILL.md:116 column list omits `embedding`, `diagrams`, `images` | ingested notes invisible to `similar_notes()`/Explore, no mermaid bake, no figure bake, skip every gate | S14-W1-2 | W1 |
| source-to-vault-5 | M | — | SKILL.md:71-72, :117-119 | ignores `links.to_note` FK (migration 0020) and the chapter-reference rule; writes topic `prerequisites` as note-table rows | S14-W1-2 | W1 |
| source-to-vault-6 | M | — | SKILL.md:152-153 "no further steps" | never busts the `notes`-tag `unstable_cache`; content can serve stale up to 1h | S14-W1-2 | W1 |
| source-to-vault-7 | M | — | SKILL.md:43-46 "no page cap" | whole-book single-context read; no chapter slicing, loss/figure/depth/voice/order-band checks | S14-W1-2 | W1 |
| source-to-vault-8 | L | — | SKILL.md:153 "(Home, Topic, Note, Graph, Search)" | Graph page removed; `/search` 301s to `/books` | S14-W1-2 | W1 |
| source-to-vault-9 | L | — | SKILL.md:19 "see `supabase/migrations/0001_init.sql`" | stale schema pointer; migrations run 0001…0023 | S14-W1-2 | W1 |
| source-to-vault-10 | L | — | plugin.json:2 vs SKILL.md:2 vs `commands/ingest.md`; no README/CHANGELOG/keywords/evals | three names for one thing; no house files | S14-W1-2 | W1 |
| learn-hub-local-1 | H | H14 | `.claude/settings.json` has only `hooks`; no `.claude/settings.local.json`; no `extraKnownMarketplaces`/`enabledPlugins` grep hit | catalog never registered or enabled; always-loaded CLAUDE.md/skills nevertheless route work to it | S14-W2-5 | W2 |
| learn-hub-local-2 | M | — | marketplace.json lists `intent-lock`, `pubmed-research-note`, `comprehensive-review`; same names under `/home/user/micky-psych-tools/plugins` | name collisions with micky-psych-tools | S14-W2-5 (via S14-W2-2 and S14-W2-4 deleting the collision sources) | W2 |
| learn-hub-local-3 | M | — | `docs/plugin-polish-plan.md:140-149`; all five plugin.json `"version": "0.1.0"`, no bump script | versioning undecided; an installed copy never refreshes | S14-W2-5 | W2 |
| learn-hub-local-4 | L | — | `claude plugin validate .` → "No marketplace description provided" | fails `--strict` on the missing top-level description | S14-W2-5 | W2 |
| learn-hub-local-5 | L | — | `ls scripts/lib/plugin-manifest*` → none | the polish-plan P1-1 validator was never built | S14-W2-5 (moot: catalog deleted) | W2 |
| learn-hub-local-6 | L | — | `source-to-vault` catalog entry description vs plugin.json description differ | two sources of truth for catalog descriptions | S14-W2-5 | W2 |
| intent-lock (learn-hub clone)-1 | H | H06 | `plugins/intent-lock/README.md:44` "exactly one ledger file" vs the file existing at both repos | fork splits the single compounding ledger; priors in one repo are invisible in the other | S14-W2-2 | W2 |
| intent-lock (learn-hub clone)-2 | M | — | `.claude/settings.json` has only `hooks`; README.md:3-5 "mandatory Step 0" | the "mandatory Step 0" is not guaranteed here either; three incompatible gating models coexist | S14-W2-3 (retire; the gating-model question belongs to the surviving micky copy, S01/S02) | W2 |
| intent-lock (learn-hub clone)-3 | M | — | README.md:3 "unmodified"; pubmed fork SKILL.md:264-265 Reframed/Skipped | no sync/parity mechanism for the vendored copy; already carries interface drift | S14-W2-3 | W2 |
| intent-lock (learn-hub clone)-4 | L | — | intent-lock SKILL.md:228 "decision-interview skill"; marketplace.json lists no such plugin | Phase-3 hand-off points at a skill not vendored here | S14-W2-3 | W2 |
| pubmed-research-note (learn-hub fork)-1 | H | H48 | `evals.json:56`, `:128` name `vault-keeper`, absent here | 2 of the fork's evals fail by construction; a 3rd expects deference to psych-paper-digest, dropped from the description | S14-W2-4 | W2 |
| pubmed-research-note (learn-hub fork)-2 | M | — | fork SKILL.md:153-154, :158-159; README still advertises `report_dir` | output now written to two places with no stated relationship | S14-W2-4 | W2 |
| pubmed-research-note (learn-hub fork)-3 | M | — | fork SKILL.md:164-165 "step 4"; :272 "Atomic notes" heading that reads "Atomize — opt-in, word-gated" | dangling cross-references introduced by the fork's own edits | S14-W2-4 | W2 |
| pubmed-research-note (learn-hub fork)-4 | M | — | fork SKILL.md:26, :171-172 | stale upstream wording ("filed to the vault as an artifact") contradicts the fork's own rewiring | S14-W2-4 | W2 |
| pubmed-research-note (learn-hub fork)-5 | M | — | fork SKILL.md:164 "gated on atomize" vs CR fork SKILL.md:166-176 digest+sync default | the two sibling forks disagree on the digest gate | S14-W2-4 | W2 |
| pubmed-research-note (learn-hub fork)-6 | M | — | fork plugin.json:3 `"1.7.0"` == upstream; CHANGELOG identical | version/CHANGELOG not forked; two behaviourally different artifacts share one version string | S14-W2-4 | W2 |
| pubmed-research-note (learn-hub fork)-7 | L | — | fork SKILL.md Firecrawl bullet; marketplace.json has no `firecrawl` entry | references a plugin not present in this marketplace | S14-W2-4 | W2 |
| pubmed-research-note (learn-hub fork)-8 | L | — | `atomic-note-template.md:3-10` "ignore its frontmatter…" | ~1.3k disclaimed tokens loaded on every atomize | S14-W2-4 | W2 |
| pubmed-research-note (learn-hub fork)-9 | L | — | `diff -ru` identical for decision-brief.md, intent-lock-pairing.md, tool-catalog.md, report-craft.md | all upstream defects carry over unfixed | S14-W2-4 | W2 |
| comprehensive-review (learn-hub fork)-1 | H | H49 | fork SKILL.md:166-176 "Digest … then syncs to Supabase … Skip only on an explicit …" | digest+live-Supabase-sync is a default step; every run writes to the shared live DB unless refused | S14-W2-4 | W2 |
| comprehensive-review (learn-hub fork)-2 | M | — | fork SKILL.md:180-181 vs :205-206 | self-contradiction: "a draft, not a deliverable" vs "the file is the deliverable" | S14-W2-4 | W2 |
| comprehensive-review (learn-hub fork)-3 | M | — | `evals.json:8` "files it via vault-keeper" (byte-identical to upstream); fork SKILL.md:178 "no vault-keeper" | eval not forked; requires a plugin the fork's own text says is absent | S14-W2-4 | W2 |
| comprehensive-review (learn-hub fork)-4 | L | — | fork SKILL.md:199 "not chained" vs README.md:43 still names it | inconsistent psych-paper-digest handling after the rewire | S14-W2-4 | W2 |
| comprehensive-review (learn-hub fork)-5 | L | — | fork SKILL.md:229; README.md:10-11 | stale/garbled filing language after the rewire | S14-W2-4 | W2 |
| comprehensive-review (learn-hub fork)-6 | L | — | plugin.json `"0.3.0"` == upstream; CHANGELOG, `review-arc.md` identical; no firecrawl entry | version/CHANGELOG not forked; firecrawl dependency absent; upstream defects carry over | S14-W2-4 | W2 |

35 of 35 assigned defects close by deletion or (H06) by merge-then-deletion. None deferred.

### 1.4 Other findings

- OBS (ledger, H06 background): state forked across two repos; only git change 2026-07-11 though MEMORY.md logs later runs. **NEW, confirmed this session**: `diff` of the two `misreads.md` files is empty — both hold the identical 2 entries and 2 active priors, dated 2026-07-11. Merge target (I03, owner S01): `plugins/intent-lock/skills/intent-lock/references/misreads.md` in micky, unchanged until the W3 move to `state/misreads.md`.
- OBS (installation): nothing loads any of these plugins today — `.claude/settings.json` has only `hooks`; no `settings.local.json`; no install instructions in README.md/CLAUDE.md.
- OBS (source-to-vault architecture): designed 2026-06-24 as "Direct to Supabase — skip markdown-file layer"; its tech-stack notes still name the deprecated project `tyxnedapxscpmytanloz`. Bypasses embed, mermaid prebake, image bake, the duplication gate, the repetition gate, links-FK filtering and cache revalidation.
- OBS (PDF-reading premise): source-to-vault reads PDFs via Read-tool `pages`; pdf-pipeline says that needs poppler, "usually can't be installed here". Not this spec's problem (source-to-vault is retired, not repaired) — noted for S17/S18 awareness.
- OBS (forks): upstream frozen at the fork point (`git diff --stat f91b3b0 HEAD` empty per digest). **Confirmed this session**: the `.mcp.json` files here are 2 of the 6 byte-identical copies in B10 (md5 `1b35ee7c…`); both go with their forks in S14-W2-4, dropping live copies 6→4.
- **NEW**: `README.md` and `CLAUDE.md` (learn-hub, top-level) contain zero mentions of `source-to-vault`, `ingest-source`, `learn-hub-local`, the three forks, or `/ingest` (`grep -n`, no hits). No live-doc line needs editing. The only mentions live in historical planning docs — `docs/superpowers/plans/2026-06-24-source-to-vault-plugin.md` and `docs/plugin-polish-plan.md:4,16,31,33,39,42,79` (superseded by `docs/plugin-rewrite/`) — dated records, not runtime references; out of scope (§8).
- **NEW**: no learn-hub doc names `plugins/learn-hub-session` yet — wholly new unit; §2.3/§3 below are its only definition.

## 2. Target state

### 2.1 Location and tree (after W2)

```
learn-hub/
  .claude-plugin/                    DELETED (S14-W2-5)
  plugins/
    learn-hub-session/                NEW (S14-W2-1)
      .claude-plugin/plugin.json
      hooks/hooks.json
      hooks/run.sh
      README.md
      CHANGELOG.md
    # source-to-vault/                DELETED (S14-W1-2)
    # intent-lock/                    DELETED (S14-W2-3, after S14-W2-2 merges its ledger)
    # pubmed-research-note/           DELETED (S14-W2-4)
    # comprehensive-review/           DELETED (S14-W2-4)
    # vault-atomizer/, vault-vectors/, pk-plasma-animation/, digest-report/
    #   converted to `.claude/skills/*` by S20 (vault-atomizer, vault-vectors),
    #   S16 (pk-plasma-animation) and S15 (digest-report) — CX-59; not this spec's
    #   steps; `plugins/` holds only `learn-hub-session` once those land too, per S11-W2-4
  .claude/hooks/session-start.sh     rewritten by S13-W1-8 (I14); this spec execs it unchanged
```

micky-psych-tools (touched only for the ledger merge):
```
plugins/intent-lock/skills/intent-lock/references/misreads.md   confirmed unchanged by S14-W2-2
                                                                  (already byte-identical, §1.4)
```

### 2.2 Frontmatter

Not applicable to a hooks-only plugin — `learn-hub-session` has no `SKILL.md`. Its only "frontmatter-shaped" file is `.claude-plugin/plugin.json` (below).

### 2.3 Body outline

Not applicable — no skill body. `hooks/run.sh` is a script, defined under §2.5.

### 2.4 References

None. The plugin ships six files total: `plugin.json`, `hooks/hooks.json`, `hooks/run.sh`, `README.md`, `CHANGELOG.md`, `LICENSE` (CX-58: every plugin needs one per architecture §8's check, so it is no longer deferred to S08's validator — one line, MIT, same text S10-W0-8 backfills for the other plugins).

### 2.5 Scripts

| name | CLI | input | stdout/behavior | exit codes | tests |
|---|---|---|---|---|---|
| `hooks/run.sh` | invoked by Claude Code as the `SessionStart` hook, no args | env: `LEARN_HUB_DIR` (optional), `CLAUDE_PLUGIN_ROOT` (set by Claude Code) | root = `$LEARN_HUB_DIR` if set and a directory, else `${CLAUDE_PLUGIN_ROOT}/../..`; if `<root>/package.json` does not contain `"name": "learn-hub"` or `<root>/scripts/apply-sync.mjs` is missing, prints `learn-hub-session: marker mismatch at <root> — not a learn-hub checkout, skipping` to stderr and exits 0; otherwise exports `LEARN_HUB_DIR=<root>` and execs `<root>/.claude/hooks/session-start.sh` (I14, owner S13) | 0 on marker mismatch (no-op) or on `session-start.sh`'s own exit code (propagated by `exec`) | manual (§4.4) — no `claude plugin eval` case, since the plugin declares no skill (§4.1) |

`hooks/run.sh` full content:

```bash
#!/bin/bash
# SessionStart hook for the learn-hub-session plugin.
# Fires from any repo CLAUDE_CODE_PLUGIN_DIRS includes it in — in a multi-repo
# cloud session that is /home/user, where a repo's own .claude/hooks never load
# (architecture T5, P2). Exists only to reach session-start.sh from there.
set -u

ROOT="${LEARN_HUB_DIR:-}"
if [ -z "$ROOT" ] || [ ! -d "$ROOT" ]; then
  ROOT="$(cd -- "${CLAUDE_PLUGIN_ROOT}/../.." && pwd)"
fi

MARKER_OK=0
if [ -f "$ROOT/package.json" ] && [ -f "$ROOT/scripts/apply-sync.mjs" ]; then
  if grep -q '"name"[[:space:]]*:[[:space:]]*"learn-hub"' "$ROOT/package.json" 2>/dev/null; then
    MARKER_OK=1
  fi
fi

if [ "$MARKER_OK" != "1" ]; then
  echo "learn-hub-session: marker mismatch at $ROOT — not a learn-hub checkout, skipping" >&2
  exit 0
fi

export LEARN_HUB_DIR="$ROOT"
exec "$ROOT/.claude/hooks/session-start.sh"
```

Rubric note: `${CLAUDE_PLUGIN_ROOT}/../..` and the exec of an absolute repo path are normally forbidden (R44 self-contained, R47 no walk-ups). Architecture §3.7/line 640 names this file as the **declared exception** to both — a hooks-only plugin whose entire job is to reach the checkout it lives beside cannot avoid naming that checkout. `claude plugin validate --strict` still runs against it (§3, done-when); the exception is recorded, not a validator bypass.

### 2.6 Handoffs

None. `learn-hub-session` calls no other skill or plugin by name; it hands off once, to `.claude/hooks/session-start.sh` (I14, owner S13), which is not itself a Claude Code "skill" and carries no §4.2 OPTIONAL fallback sentence — the marker check above is its own fallback (no-op, not a stall).

### 2.7 Interfaces

#### I15 — `plugins/learn-hub-session` (owned)

- **Location**: `/home/user/learn-hub/plugins/learn-hub-session/.claude-plugin/plugin.json` with `name` = `learn-hub-session`.
- **plugin.json**:
  ```json
  {
    "$schema": "<ASSUMES — settled with S10's I24, §8>",
    "name": "learn-hub-session",
    "version": "1.0.0",
    "description": "SessionStart hook that fires learn-hub's session setup in multi-repo cloud sessions, where a repo's own .claude/hooks never load.",
    "author": { "name": "Thanawat Suharit (Micky)" },
    "keywords": ["hooks", "session-setup", "learn-hub"]
  }
  ```
- **hooks/hooks.json** (exec form, N8 — a single-string `command` with an embedded `${CLAUDE_PLUGIN_ROOT}` placeholder fails `--strict`'s unquoted-placeholder check; this is the exact form S11-W0-7's check b probe (`w0-hookprobe`) proved fires, and CX-58 confirms it as the one form to use everywhere, matching S08's own hook template):
  ```json
  {
    "hooks": {
      "SessionStart": [
        {
          "hooks": [
            {
              "type": "command",
              "command": "bash",
              "args": ["${CLAUDE_PLUGIN_ROOT}/hooks/run.sh"]
            }
          ]
        }
      ]
    }
  }
  ```
- **hooks/run.sh**: root and marker resolution, §2.5, full content above.
- **Versioning**: semver in `plugin.json` only (R83); no `commands/`, no skills, so no `renames` entry (nothing user-facing to migrate) and no `metadata.profile` (per-skill key, R54, none here).
- **Created**: W2, architecture §10 W2 work-item 1, before schedule point V5 (I16.2, owner S11) — S11-W2-4 depends on this plugin existing and merged.
- **Built only if** W0 checklist item **b** = yes (a probe plugin's hooks fire in a platform-started multi-repo session). If no, this step does not run; session setup falls back to the setup script + variables + preflight refusal text (§10 W0 fallback for check b).

#### Interfaces consumed

- **I03 (owner S01).** ASSUMES: entry grammar and cap (7, newest-first) exactly as read (confirmed identical, §1.4); pre-W3 merge target is `plugins/intent-lock/skills/intent-lock/references/misreads.md` in micky (S01's §2.7 names this spec as its W2 dependency) — S01 to confirm no drift before its W3-4 seeds `state/misreads.md`.
- **I13 (owner S13).** ASSUMES: `hooks/run.sh` need not itself call `sync:preflight` — session setup (I14) and sync preflight (invoked per-run by sync-vault) stay separate — S13 to confirm no session-start responsibility moved into the sync tail that this hook would need to trigger.
- **I14 (owner S13).** ASSUMES: from S13-W1-8, `session-start.sh` resolves root as (1) `LEARN_HUB_DIR` if set and the dir exists, (2) marker-checked `CLAUDE_PROJECT_DIR`, (3) its own script path — so exporting `LEARN_HUB_DIR` before `exec` is sufficient; its done-marker at `<root>/.claude/.session-start.done` stops the settings.json copy and this plugin's copy (§2.5, "both fire") from doing setup twice.
- **I16 (owner S11).** ASSUMES: schedule point **V5** (I16.2) adds the folder `/home/user/learn-hub/plugins` only after `ls` shows exactly `learn-hub-session` and `.claude-plugin/` is absent — after this spec's §3 W2 plus S15/S19/S20/S06's conversions (§7). Per I16.10, only S11 edits `CLAUDE_CODE_PLUGIN_DIRS`; this spec's exit line for S11: "Ready for cloud delivery: HIGH defects closed (H06, H14, H17–H20, H48, H49); no cross-plugin handoffs; no same-named unit remains; smoke = `claude plugin validate --strict plugins/learn-hub-session` (§4.4)."
- **I17 (owner S12).** ASSUMES: the case layout/tags/`tool_used: Skill` regex in `eval-format.md` are stable; this spec files no cases since `learn-hub-session` declares no skill — S12 to confirm its smoke runner accepts a zero-case plugin as a pass, since S11-W2-4 still reads an I16.3 "smoke" line for it.

## 3. Change steps

### Wave 1

**S14-W1-1 · OWNER · audit source-to-vault's live writes before deletion (read-only; critique F17, C2-21)**
- Repo: learn-hub · depends on: none.
- Action (owner, read-only against the live Supabase project): run `npm run vectors:check` (`node scripts/vector-report.mjs --no-verify`) and read report section "## 2. Vault ↔ database reconciliation", row "in DB, no vault file". This is the same reconciler CLAUDE.md's own "DB rows can outlive their /vault source" gotcha names, and the only mechanism that can tell whether source-to-vault (never confirmed loaded, H17 evidence) actually wrote anything.
- Files: none (report is a local artifact, not committed).
- Done when: the report prints an "in DB, no vault file" count.
  - If **0**: record it in the S14-W1-2 commit message ("source-to-vault audit: 0 orphan rows, `npm run vectors:check` <date>") and proceed — no further action.
  - If **>0**: the report's "Which of those orphans were REPLACED rather than merely un-filed" section (superseded-topic heuristic) narrows which orphans look like source-to-vault's own writes (topics/notes with no other producer's fingerprint — e.g. `sources[]` holding a bare filename, matching source-to-vault-4's column list, §1.3). The count covers every orphan, not only this plugin's (CLAUDE.md already records 13 from other causes), so the owner records the count and the ids that look like source-to-vault writes in the S14-W1-2 commit message. For each such row the owner chooses: **restore** it into `/vault` with `node scripts/restore-vault-from-db.mjs --verify <topic-id>` (writes files only; keeps the content re-syncable; the documented recovery path), or **leave** it. No row is deleted in W1: H17 closes when the skill is deleted, and a raw `execute_sql` delete is forbidden (sync-vault-4: `progress` cascades). A later deletion, if wanted, goes through app Hide → `npm run purge:hidden`, outside this wave.
- Rollback: not applicable (read-only; a restore only writes vault files, which a `git revert` removes).

**S14-W1-2 · learn-hub · delete `plugins/source-to-vault/`**
- Repo: learn-hub · depends on: S14-W1-1 (its finding recorded in this commit's message).
- Files: delete `plugins/source-to-vault/skills/ingest-source/SKILL.md`, `plugins/source-to-vault/commands/ingest.md`, `plugins/source-to-vault/.claude-plugin/plugin.json` (whole directory).
- Change: `git rm -r plugins/source-to-vault`. The `learn-hub-local` catalog's `source-to-vault` entry is left in place until S14-W2-5 deletes the whole catalog file (§1.4: nothing validates that file before W2, so a dangling `source` in it causes no active harm in the interim).
- Commands: `git rm -r plugins/source-to-vault`
- Done when: `test ! -d plugins/source-to-vault`; `npm run check:skills` still exits 0 (the catalog is not part of that check, §1.1).
- Rollback: `git checkout HEAD~1 -- plugins/source-to-vault`.

### Wave 2

**S14-W2-1 · learn-hub · create `plugins/learn-hub-session`**
- Repo: learn-hub · depends on: S13-W1-8 (`.claude/hooks/session-start.sh` rewritten with `LEARN_HUB_DIR`-first root resolution, done-marker, ready line — I14); S11-W0-7 (records W0 checklist item b; if b = no, skip this step, §2.7 I15; CX-34).
- Files: create `plugins/learn-hub-session/.claude-plugin/plugin.json`, `plugins/learn-hub-session/hooks/hooks.json`, `plugins/learn-hub-session/hooks/run.sh`, `plugins/learn-hub-session/README.md`, `plugins/learn-hub-session/CHANGELOG.md`, `plugins/learn-hub-session/LICENSE` (MIT, owner "Thanawat Suharit (Micky)", 2026 — the same text as S10-W0-8's backfill; critique P24).
- Change: contents exactly as §2.7 I15 (plugin.json, hooks.json, run.sh). README.md: one paragraph stating the plugin's sole job (fire `session-start.sh` in multi-repo cloud sessions) and the marker/fallback behavior; CHANGELOG.md: `## 1.0.0 — 2026-09-24` / `- Initial release: SessionStart hook for multi-repo cloud sessions (H14 successor infrastructure, architecture §2.3/§3.7).`
- Commands: `chmod +x plugins/learn-hub-session/hooks/run.sh`; `bash -n plugins/learn-hub-session/hooks/run.sh`; `claude plugin validate --strict plugins/learn-hub-session`
- Done when: `bash -n` exits 0; `claude plugin validate --strict plugins/learn-hub-session` exits 0 with no errors (a self-containment warning for `${CLAUDE_PLUGIN_ROOT}/../..` is the declared R44/R47 exception, §2.5 — record it, do not silence it by editing the manifest); a manual run of `hooks/run.sh` with `LEARN_HUB_DIR=/home/user/learn-hub` prints no marker-mismatch line and execs `session-start.sh`.
- Rollback: `git rm -r plugins/learn-hub-session`.

**S14-W2-2 · micky-psych-tools · confirm/merge the fork's ledger into micky's**
- Repo: micky-psych-tools · depends on: none.
- Files: `plugins/intent-lock/skills/intent-lock/references/misreads.md` (edit only if the diff is non-empty).
- Change: `diff` the fork's copy against micky's. If empty (confirmed this session, §1.4): no edit — already complete. If non-empty: append each entry unique to the fork's `## Entries` into micky's file, newest-first, no reordering existing entries (I03 grammar, owner S01); for each `Prior:` line unique to the fork's `## Active priors`, prepend it and drop the oldest past the cap of 7, recording the 3 oldest as retirement candidates rather than silently dropping them.
- Commands: `diff -u learn-hub/plugins/intent-lock/skills/intent-lock/references/misreads.md micky-psych-tools/plugins/intent-lock/skills/intent-lock/references/misreads.md`
- Done when: the two files are byte-identical (`diff` exits 0); entry count in micky's copy is the same or higher, never lower.
- Rollback: `git checkout -- plugins/intent-lock/skills/intent-lock/references/misreads.md` (micky-psych-tools).

**S14-W2-3 · learn-hub · delete `plugins/intent-lock/` fork**
- Repo: learn-hub · depends on: S14-W2-2 (merge confirmed/applied first — deleting before confirming would lose any entry unique to the fork).
- Files: delete `plugins/intent-lock/` (whole directory: both skills, `references/`, README.md, CHANGELOG.md, `.claude-plugin/plugin.json`).
- Change: `git rm -r plugins/intent-lock`.
- Commands: `git rm -r plugins/intent-lock`
- Done when: `test ! -d plugins/intent-lock`.
- Rollback: `git checkout HEAD~1 -- plugins/intent-lock`.

**S14-W2-4 · learn-hub · delete the pubmed and comprehensive-review forks**
- Repo: learn-hub · depends on: S07-W2-1 (sink routes to the inbox), S03-W2-1 (pubmed producer wiring), S04-W2-1 (CR producer wiring, OD5 publish-on-"digest"). These landing first makes the canonical skills (reached via the cloud folder join, I16) functionally equivalent to what the forks provided, before the forks disappear.
- Files: delete `plugins/pubmed-research-note/` and `plugins/comprehensive-review/` (whole directories, including both `.mcp.json` copies and `commands/comprehensive-review.md`).
- Change: `git rm -r plugins/pubmed-research-note plugins/comprehensive-review`.
- Commands: `git rm -r plugins/pubmed-research-note plugins/comprehensive-review`
- Done when: `test ! -d plugins/pubmed-research-note -a ! -d plugins/comprehensive-review`; `find plugins -name comprehensive-review.md` returns nothing.
- Rollback: `git checkout HEAD~1 -- plugins/pubmed-research-note plugins/comprehensive-review`.

**S14-W2-5 · learn-hub · delete the `learn-hub-local` catalog**
- Repo: learn-hub · depends on: S11-W2-1 (OWNER, Windows `claude plugin marketplace remove learn-hub-local`, only if W0-g found it — must land first per S11's own step note); S14-W1-2, S14-W2-3, S14-W2-4 (tidy: no commit should reference a dir a later commit removes, though nothing validates this file in the interim); S15-W2-3, S16-W2-6, S20-W2-1, S20-W2-2 (CX-34: the converted plugins — digest-report, pk-plasma-animation, vault-atomizer, vault-vectors — must be out of `learn-hub/plugins/` before the catalog that once listed some of them is deleted).
- Files: delete `.claude-plugin/marketplace.json` and the `.claude-plugin/` directory if now empty.
- Change: `git rm .claude-plugin/marketplace.json`; `rmdir .claude-plugin 2>/dev/null || true`.
- Commands: `git rm .claude-plugin/marketplace.json`
- Done when: `test ! -e .claude-plugin/marketplace.json`.
- Rollback: `git checkout HEAD~1 -- .claude-plugin/marketplace.json`.

Owner actions in this spec: **S14-W1-1** (the audit and any restore/delete decision). A hard dependency on another spec's owner action: **S11-W2-1** (Windows `claude plugin marketplace remove learn-hub-local`, only if found).

## 4. Evals

### 4.1 Cases

No `claude plugin eval` cases in this spec. Every unit is either **deleted** (source-to-vault, the catalog, the three forks — a deleted skill has no case to keep; its trigger phrases are recorded, not re-tested, in §6) or a **hooks-only plugin with no skill** (`learn-hub-session` — R71's "≥3 cases per skill" has no skill to apply to). This mirrors S11's own position for a spec that owns no skill (§2.7 I17 ASSUMES).

In place of eval cases, `learn-hub-session`'s three behaviors are checked deterministically (§4.4): marker-match (execs `session-start.sh`), marker-mismatch (exits 0 with a message), and `LEARN_HUB_DIR` precedence over the `${CLAUDE_PLUGIN_ROOT}/../..` fallback.

### 4.2 Conversion

| old evals.json case (file, name) | new case dir | dropped (reason) |
|---|---|---|
| `plugins/intent-lock/skills/intent-lock/evals/evals.json` (all cases) | — | dropped — plugin deleted (H06); the micky copy's evals are S01's, not a fork of these |
| `plugins/intent-lock/skills/misread-capture/evals/evals.json` (all cases) | — | dropped — plugin deleted; same reason |
| `plugins/pubmed-research-note/skills/pubmed-research-note/evals/evals.json` (17 cases, incl. the 2 that fail by construction, H48 evidence) | — | dropped — plugin deleted; the canonical skill's evals are S03's |
| `plugins/comprehensive-review/skills/comprehensive-review/evals/evals.json` (12 cases, incl. the vault-keeper one, H49 evidence) | — | dropped — plugin deleted; the canonical skill's evals are S04's |
| `plugins/source-to-vault/skills/ingest-source` — no `evals/` directory exists (§1.3, source-to-vault-10) | — | nothing to drop |

### 4.3 Live triggers

No live trigger family applies. `learn-hub-session` fires on `SessionStart`, never on a user request, so it carries no trigger phrase and is not a candidate for S12's family query sets. The 4 deleted skills' trigger phrases are retired, not reassigned — §6 records each disposition (all "removed"; surviving coverage sits with the canonical micky skills, owned by S01/S03/S04, and with pdf-pipeline/atomize-book/ingest-article for source-to-vault's ground, owned by S17/S18).

### 4.4 Commands

- Smoke (this spec's only unit with runnable content): `claude plugin validate --strict plugins/learn-hub-session` — exit 0.
- Marker-match: `cd /home/user/learn-hub && LEARN_HUB_DIR=/home/user/learn-hub CLAUDE_PLUGIN_ROOT=/home/user/learn-hub/plugins/learn-hub-session bash plugins/learn-hub-session/hooks/run.sh` — no "marker mismatch" line on stderr; the process ends with `session-start.sh`'s own exit code (0 locally, since `CLAUDE_CODE_REMOTE` is unset there and `session-start.sh` exits 0 immediately, §1.1).
- Marker-mismatch: same command with `LEARN_HUB_DIR=/tmp` (or any non-learn-hub dir) — prints `learn-hub-session: marker mismatch at /tmp — not a learn-hub checkout, skipping` on stderr, exits 0.
- `LEARN_HUB_DIR` precedence: unset `LEARN_HUB_DIR`, run from `CLAUDE_PLUGIN_ROOT=/home/user/learn-hub/plugins/learn-hub-session` — resolves the same root via the `../..` fallback and still execs `session-start.sh`.
- Release: none — `learn-hub-session` has no separate release step beyond the plugin.json version (§2.7); project skills elsewhere in learn-hub are unversioned (architecture §7).

## 5. Acceptance criteria

1. `test ! -d plugins/source-to-vault` (learn-hub) → true.
2. `test ! -d plugins/intent-lock -a ! -d plugins/pubmed-research-note -a ! -d plugins/comprehensive-review` (learn-hub) → all absent.
3. `test ! -e .claude-plugin/marketplace.json` (learn-hub) → absent.
4. `diff` of the fork's ledger vs micky's, before S14-W2-3 deletes the fork copy → exits 0.
5. `python3 -c "import json; json.load(open('plugins/learn-hub-session/.claude-plugin/plugin.json'))"` → no exception; `name` == `"learn-hub-session"`.
6. Same for `hooks/hooks.json` → contains `SessionStart`.
7. `claude plugin validate --strict plugins/learn-hub-session` → exit 0.
8. `grep -c '"command": "bash",' plugins/learn-hub-session/hooks/hooks.json` → `1` (exec form, N8).
9. `bash -n plugins/learn-hub-session/hooks/run.sh` → exit 0.
10. `grep -c 'LEARN_HUB_DIR\|CLAUDE_PLUGIN_ROOT' plugins/learn-hub-session/hooks/run.sh` → ≥ 2.
11. `grep -rc "source-to-vault\|ingest-source\|learn-hub-local" README.md CLAUDE.md` → `0` (already true today, §1.4 — guards against a future edit reintroducing a reference to a deleted unit).
12. All 35 rows of §1.3 show a fix step whose file above has landed.

## 6. Trigger lock

| phrase | source (skill, field) | kept / moved → \<skill\> / removed (reason) |
|---|---|---|
| `/ingest`, "ingest this PDF/EPUB", "import notes from <file>", "turn this book into notes" | `ingest-source` (source-to-vault), description | removed (H17–H20; no successor keeps this literal phrase — functional ground is covered by `pdf-pipeline` → `atomize-book`/`ingest-article`, owned by S17/S18, with their own descriptions) |
| "interview me", "ask me until you understand", "make sure you don't misunderstand", "lock the goal", "craft my prompt", "what do I actually want", "ถามจนกว่าจะเข้าใจ", "ล็อคเป้าหมาย" | `intent-lock` (fork), description | removed (H06; identical phrasing kept live in micky's `intent-lock`, owned by S01 — reached from a multi-repo learn-hub session via the plugin-dir folder join, I16, once enabled) |
| "this isn't what I wanted", "you misunderstood", "that's not it", "I asked for X and got Y", "you wasted my time", "ไม่ใช่ที่ผมต้องการ", "เข้าใจผิด", "ไม่ใช่แบบนี้" | `misread-capture` (fork), description | removed (H06; kept live in micky's `misread-capture`, owned by S01) |
| "research", "what does the literature say about", "search PubMed for", "is X true", "should I use X for Y", "หางานวิจัย", "ทบทวนหลักฐาน", "ค้น PubMed", "จริงหรือเปล่า", "just search", "atomize", "ทำโน้ต", "comprehensive review of X" | `pubmed-research-note` (fork), description | removed (H48; kept live in micky's `pubmed-research-note`, owned by S03) |
| "comprehensive review of X", "full review of X", "whole-disorder review", "academic review", "review the whole topic", "รีวิวทั้งโรค", "should I use X for Y" | `comprehensive-review` (fork), description | removed (H49; kept live in micky's `comprehensive-review`, owned by S04) |
| (none — hooks fire on `SessionStart`, never on a phrase) | `learn-hub-session`, hooks.json | n/a — not a trigger-lock entry |

## 7. Risks and OD sensitivity

- **Orphan DB rows from source-to-vault.** S14-W1-1 reads before deleting the *skill*, not any data it wrote — deleting the plugin directory cannot itself touch Supabase rows. The risk is only in *not* auditing: an unaudited orphan row stays permanently unreachable by any future vault walk (the "DB rows can outlive their /vault source" trap, CLAUDE.md). If the owner skips the audit, record that explicitly rather than silently proceeding.
- **Cross-repo coordination for `plugins/` becoming exactly `{learn-hub-session}`.** S11-W2-4's precondition needs this spec's five deletions **and** S15/S20/pk-plasma-animation's conversions all landed. This spec's steps are independent of those three; the ordering is S11's to sequence at its W2 step 6c (I16.2 V5).
- **OD1 sensitivity.** Under (a, assumed): once the folder join lands, a multi-repo session reaches micky's canonical skills directly. Under (b, claude.ai-synced): `learn-hub-session` "cannot ship that way" (§10 W0-b fallback) — S14-W2-1 does not run, replaced by the setup script + env vars + preflight refusal text; H06/H48/H49 closures (merge-then-delete) are unaffected. Under (c, none): same as (b) for this spec — the deletions still happen, only `learn-hub-session` is not built.
- **OD2 sensitivity.** Under (a, assumed): S11-W2-1's Windows uninstall is one-time cleanup before S14-W2-5. Under (b, local-directory marketplaces): learn-hub keeps a one-entry catalog for `learn-hub-session` — S14-W2-5 becomes "reduce to 1 entry" instead of "delete the file", and R33's `$schema`/description rules then apply to it. Not built this way here per OD2's recommendation.

## 8. Open questions

- **ASSUMES (I15, §2.7)**: the `plugin.json` `$schema` literal value — same unresolved item as S10's I24: run `claude plugin init` in a scratch dir and read the emitted value; settles both specs' manifests in one check, before S14-W2-1 and S10-W3-1.
- **ARCH-CONFLICT: none found.** Every cited architecture row (Appendix A H06/H14/H17-H20/H48/H49, §3.5 rows, §10 W1 item 8, W2 steps 1/5/6) matches what this session re-read in the source files.
- **Whether the smoke runner (I17, owner S12) accepts a zero-case plugin as a pass** — flagged in I17 ASSUMES; settle before S11-W2-4 reads `learn-hub-session`'s smoke result.
- **CLOSED (reconcile-2, critique P24).** LICENSE for a hooks-only plugin: S14-W2-1 now writes an MIT LICENSE, so the answer to R45 no longer matters.
- **Historical docs naming these retired units** (`docs/superpowers/plans/2026-06-24-source-to-vault-plugin.md`, `docs/plugin-polish-plan.md`) are out of scope (§1.4: not live references, not claimed by any spec). Archiving them, if wanted, is a small S21/follow-up item.
