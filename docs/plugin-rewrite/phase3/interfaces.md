# Interface registry for the phase-3 specs

Each interface has ONE owner spec. The owner defines it in full (fields, paths, CLI flags,
JSON shapes, exit codes). A consumer spec uses the architecture's definition, cites the
owner as `I<nn> (owner S<nn>)`, and never redefines it. When the architecture leaves a
detail open, the consumer writes `ASSUMES: <detail> — owner S<nn> to confirm` in its
§2.7 and §8. Section numbers point into `docs/plugin-rewrite/architecture.md`.

If the owner's spec file already exists in the specs folder when you work, read its §2.7
and conform to it. Never edit another spec's file.

| Id | Interface | Owner | Consumers | Architecture |
|---|---|---|---|---|
| I01 | Lock record: the slots intent-lock returns (deliverable, question, scope in/out, emphasis, audience, exclusions, assumed defaults); the single hand-back line `Assumed: <reading> — say if wrong.`; the §Handoff OPTIONAL-with-fallback sentence callers carry verbatim | S01 | S02, S03, S04, S05, S06, S09, S16 | §4.1, §4.2, §4.3 |
| I02 | Interview protocol: materiality threshold, destructive always-ask, AskUserQuestion mechanics (1–4 questions, 2–4 options, multiSelect, automatic Other), one silence rule, autonomous fallback when the picker is absent or errors, stop sovereignty, question caps (intent-lock 3, siblings 4) | S01 | S02 | §4.1 |
| I03 | Misread ledger: entry grammar, ordering (newest first), cap; `scripts/ledger.py append|list|retire` CLI; path `$MICKY_TOOLS_DIR/state/misreads.md` (W3); pre-W3 location for the W2 fork merge | S01 | S02 (plan-critique carve-out), S14 (W2 fork-ledger merge) | §2.2, §3.2, OD6 |
| I04 | Report contract `report/1`: frontmatter (`title`, `kind: decision|topic|digest`, `topic`, `source_skill`, `created`, `contract: report/1`), first-line `Assumed:`, no inline citations, `## Sources` grammar with ONE NCT form, depth contract, engine-failure policy, voice rule; `scripts/sources_lint.py` CLI; fixtures `plugins/evidence/evals/fixtures/report-*.md` | S03 | S04, S15 (tolerant reader), S16 (pk-plasma brief), S08 (cross-repo check) | §4.1, §5.4 |
| I05 | Engines: the runtime MCP resolution sentence; E-utilities `datetype=edat` + `retstart`; CT.gov v2 `AREA[…]RANGE`; firecrawl fetch-only contract; the single `plugins/evidence/.mcp.json` (server names `pubmed`, `clinical-trials`) | S03 | S04, S09, S16 | §4.4 |
| I06 | lit-watch state `state/lit-watch/{config.json,last_swept.json,digests/}`; `scripts/sweep.py` CLI | S04 | S10 (skeleton PR) | §4.5, OD6 |
| I07 | HTML artifact contract (full document: doctype, `lang`, `color-scheme`, painted `html,body`; self-contained; reduced-motion; sheets light-locked; strip rule; layout grammar `min-height:100dvh`, `.wrap>*{flex:0 0 auto}`, stage `max(220px,min(38dvh,280px))`, `flex-basis:0`); `references/render-verify.md`; `scripts/check-html.mjs` CLI (a static subset of ≤60 lines that delegates to `audit:visual` and returns `incomplete` without learn-hub; OQ13-a dropped the render port and the parity fixture) | S05 | S06, S16 | §4.1, §4.3, §5.4 |
| I08 | `npm run audit:visual -- <file> --json` in learn-hub: checks run per kind, JSON output schema, exit codes | S16 | S05, S06 | §4.3, §5.5 |
| I09 | Inbox contract `research-notes/`: `<slug>.md` reports; `visuals/<slug>.html` + `<slug>.meta.json` (`{kind, title, description, topic_hint, source_report, producer, created, audit: {tool, verdict}}`); slug rule; collision suffix `-2`; git-tracked; commit offer | S15 | S07 (sink), S03, S04, S05, S06 (producers via the sink), S16 (reads visuals) | §4.3, §5.4 |
| I10 | Intake log `research-notes/.intake-log.jsonl`: `{file, sha256, consumer, action: digested|filed|refused, rows, commit, at}`; written only after sync-vault verification | S15 | S07 (empty-vault reads), S16 (writes) | §5.6 |
| I11 | Sink: `scripts/sink.py` CLI; resolution order (explicit → `LEARN_HUB_DIR`/userConfig validated by marker → `MICKY_TOOLS_DIR` + `vault/.vault-id` → ask; headless: cwd + `Assumed:` line); the filing sentence callers carry | S07 | S03, S04, S05, S06 | §4.2, §5.3 |
| I12 | Transfer: `scripts/drain_plan.py` manifest (item → kind → receiver → destination); plan → validate → copy → sha verify → commit offer → delete verified only; held kinds. Deferred by OQ15-a: built at S07-W5-2 only if S07-W5-1 keeps the vault; W2 uses a one-time copy (S07-W2-8) | S07 | S15 | §5.6 |
| I13 | Sync tail: the sync-vault procedure (fetch + merge check → `npm run sync:preflight` → background `npm run sync:apply` with a log, no inner `&` → success = `EXIT=0` + `Upserted … note(s)` → revalidate → per-provenance verification; deletion via `purge:hidden` / `merge_note_history`); `scripts/lib/sync-preflight.mjs`; `scripts/ready.mjs --json` CLI | S13 | S14, S15, S16, S17, S18, S19, S20 | §3.6, §5.5, §5.7 |
| I14 | Session setup: `.claude/hooks/session-start.sh` root resolution (`LEARN_HUB_DIR` → marker-checked `CLAUDE_PROJECT_DIR` → own path), done-marker, ready line (prints `claude --version` + loaded plugins) | S13 | S14 | §3.7 |
| I15 | `plugins/learn-hub-session` (hooks.json, `hooks/run.sh` root + marker, versioning) | S14 | S11 | §2.3, §3.7 |
| I16 | Delivery: `CLAUDE_CODE_PLUGIN_DIRS` schedule, `docs/rewrite/delivery-log.md` format, env var table, cloud setup script contents, W0 checklist a–h procedures, Windows route | S11 | every spec's cloud-enable step | §2.5–§2.7, §10 W0 |
| I17 | Eval program: case layout `plugins/<p>/evals/<skill>/<case>/`; tags `smoke|trigger|negative|output|release`; the trigger grader regex form; `scripts/eval.sh` CLI (micky); `scripts/eval-project-skill.sh` CLI (learn-hub); `docs/rewrite/{ratchet.json,triggers.lock.json,baseline.md,h-coverage.md}` formats and generators; live trigger families + query sets; routing smoke set | S12 | all | §6, §8 ratchet |
| I18 | W0 tooling in place (micky): `scripts/validate.py` fixes, `scripts/bump.py` rewrite, `scripts/route.py` fix, `scripts/health.sh`, `.githooks/pre-commit` | S10 | S08 (moves them in W3), S12 | §3.4, §10 W0 |
| I19 | Final validator + release (W3): `plugins/plugin-creator/scripts/validate.py` modes (`--repo`, `--cross-repo`, `--versions`, `--fix-seams`) and the §8 check list; `release.py` CLI | S08 | S10 (health.sh after W3), S12, S21 (skill-lint subset) | §7, §8 |
| I20 | Skill house shape: frontmatter key whitelist; description = capability + `Use when …` + `Not for … (use plugin:skill)`, ≤1,024 hard, ≤600 soft; `metadata.profile: cc`; standing rules first; `## Gotchas`; alias skill template (dmi, ≤10-line body `Invoke <plugin:skill> with: $ARGUMENTS`, `argument-hint`) | S08 (templates) | every skill spec | §3 conventions, §3.3, §8 |
| I21 | learn-hub gotcha destinations: `docs/rewrite/gotcha-map.md` (heading → destination), per-skill `references/gotchas.md`, `docs/vault-format.md`, `.claude/rules/*.md`, `docs/gotchas-archive.md` | S21 | S13, S16, S17, S18, S19, S20 | §3.7, §10 W4 |
| I22 | learn-hub npm scripts: `sync:preflight` (S13), `audit:visual` (S16), `test:py` + `check:skills` (S21), `book:*` aliases (S19); one package.json edit list | S21 | all learn-hub specs | §2.3 |
| I23 | W3 skeleton PR in micky: move plugins unchanged into `alignment`, `evidence` (+ `lit-watch` rename, `state/lit-watch/`), `visuals`; one `.mcp.json`; `renames`; commands deleted → dmi alias skills + `argument-hint`; misread ledger → `state/misreads.md` | S10 | S01–S07 (their W3 content steps come after it) | §10 W3 step 2 |
| I24 | `.claude-plugin/marketplace.json` shape: W0 strip entry versions; W3 `$schema`, top-level `description`, entries `{name, source, category, keywords}`, `renames` | S10 | S08 | §2.2, §3.4, §7 |
| I25 | `learn-hub/scripts/check-contract.mjs`: runs digest-report's pure parser over `$MICKY_TOOLS_DIR/plugins/evidence/evals/fixtures/*.md`; absent micky = warning | S15 | S08 (`validate.py --cross-repo`) | §4.3 |
| I26 | `scripts/classify_pdf.py` (learn-hub, pdf-pipeline): signals → suggested route JSON | S18 | S17 | §3.6 |
| I27 | Env vars `ARTICLE_INBOX_DIR` (ingest-article) and `BOOK_ROOT` (vault-coverage): defaults and absent-behaviour | S11 (table) | S17, S20 | §2.6 |

## Step id convention

`S<nn>-W<wave>-<k>` (for example `S07-W1-2`). One step = one commit in one repo. A step
that depends on another spec's step names it (`depends on S13-W1-1`).
