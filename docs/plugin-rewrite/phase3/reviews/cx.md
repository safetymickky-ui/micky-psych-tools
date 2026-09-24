# Cross-spec consistency check (phase 3, specs S01–S21)

Date: 2026-09-24. Inputs: `specs/S01…S21`, `interfaces.md`, `architecture.md` (§2–§12, Appendix A), `phaseB/coverage.md`, `phaseB/summaries.json`. Read-only; no repo was changed.

**Rules applied.**
- Check A: for each interface I01–I27, the owner spec's §2.7 is the definition. A consumer that differs is a mismatch. The owner wins unless it contradicts the architecture; then the architecture wins.
- Check B: every `depends on` must name a real step id; no cycles; waves follow architecture §10; `CLAUDE_CODE_PLUGIN_DIRS` additions follow their fixes; HIGH defects close in their Appendix A wave; same-file edits in one wave are ordered.
- Owner decisions: every OD takes the architecture's recommended option.
- A step marked "new" below does not exist in any spec today. The finding that creates it is named.

**Result in one line.** 62 findings: 6 high, 37 medium, 19 low. HIGH defects all land in their Appendix A wave on paper, but H08/H09 do not really close in W1 (CX-5). The W3 skeleton PR (S10) loses content that other specs created (CX-1, CX-2, CX-3). The W0 smoke seeds that every later gate needs do not exist (CX-4).

---

## 1. Findings

Severity: **high** = the plan breaks or harms data if executed as written; **medium** = a real contradiction, gap or order error that an executor would hit; **low** = wording, naming or bookkeeping.

| Id | Sev | Specs | Problem | Exact fix per spec |
|---|---|---|---|---|
| CX-1 | high | S10, S02, S04, S05, S06 | I23 alias skills. Architecture §10 W3 step 2 and `interfaces.md` I23 put "commands deleted → dmi alias skills + `argument-hint`" inside the skeleton PR. S10 §2.7 I23 item (3) says the aliases are added later by S02/S04/S05/S06. S02 and S05 have no alias step (they ASSUME S10 creates them); S04-W3-3 creates `digest`; S06-W3-4 creates two "if S10 has not". After S10-W3-2 deletes the commands, `/critique-plan`, `/resolve-decisions`, `/animate` and `/visualize` exist nowhere. The owner contradicts the architecture. | **S10** §2.7 I23 item (3) and S10-W3-2: in the same commit, create the 7 family alias skills (`alignment/skills/{critique-plan,resolve-decisions}`, `evidence/skills/digest`, `visuals/skills/{infographic,animate,visualize,explain-code}`), text copied verbatim from S02 §2.2, S04 §2.2, S05 §2.2, S06 §2.2. **S04** S04-W3-3: replace "create `$P/skills/digest/SKILL.md`" with "verify it matches §2.2". **S06** S06-W3-4: verify only. **S02, S05**: no change. |
| CX-2 | high | S10, S01, S05, S06 | The skeleton move deletes plugin-root content. S10-W3-2 moves only `skills/<skill>`, `.mcp.json`, README/CHANGELOG, `examples/` and `misreads.md`, then runs `git rm -r plugins/<p>`. Files created at plugin root in W0–W2 are not moved and are deleted: `plugins/intent-lock/references/lock-record.md` (S01-W2-1, the I01 contract), `plugins/{concept-animation,ml-concept-lab,clinical-infographic}/scripts/check-html.mjs` + tests + `fixtures/` (S05-W2-1/-2), plugin-level `evals/<skill>/` dirs (S05-W2-5, S06-W1-3, the CX-4 seeds), `LICENSE` (S10-W0-8). No S01 step gives `lock-record.md` its W3 home. S05-W3-1 `git mv`s `CA/scripts/*` after `CA/` is gone. | **S10** S10-W3-2: add "for each member plugin, move every plugin-root dir except `skills/`, `.claude-plugin/`, `commands/` to the family root at the same relative path (`references/`, `scripts/` keeping one copy of byte-identical files, `evals/<skill>/`, one family `LICENSE`); run `git rm -r plugins/<p>` only when `find plugins/<p> -type f` lists nothing but `.claude-plugin/plugin.json`". **S01** S01-W3-1: add "confirm `plugins/alignment/references/lock-record.md` arrived; replace `intent-lock:intent-lock` with `alignment:intent-lock` in it". **S05** S05-W3-1: replace the `git mv` with "verify exactly one `V/scripts/check-html.mjs`; delete nothing". |
| CX-3 | high | S10, S01, S03, S04, S05, S06 | Family manifests have no owner. S10-W3-2 creates `plugins/{alignment,evidence,visuals}/skills/` but no `.claude-plugin/plugin.json`, and deletes the members' manifests. S10-W3-1's own done-when (`claude plugin validate --strict` on the catalog) and VAL-11 need them. S05-W3-4 edits a visuals `plugin.json` it assumes S10 made. S01-W3-5 creates alignment's with a hand-set `1.1.0` (the repo forbids hand-set versions). No step consolidates evidence or visuals `README-<p>.md`/`CHANGELOG-<p>.md`, although S10 says S03+S04 and S05 own it; S06-W3-1 edits a `V/CHANGELOG.md` nothing creates. | **S10** S10-W3-2: create the three family `plugin.json` (`$schema`, name, `version: 1.0.0` — major, renames per §7 — description, author, keywords). **S01** S01-W3-5: edit, not create; no hand version (release via `release.py alignment minor --write` after S08-W3-1). **S03**: new S03-W3-7 "evidence README/CHANGELOG/LICENSE: merge `README-<p>.md`/`CHANGELOG-<p>.md`, delete the per-member files" (depends S03-W3-6, S04-W3-6). **S05**: new S05-W3-5 same for visuals (depends S05-W3-4). **S06** S06-W3-1: depends S05-W3-5. |
| CX-4 | high | S12, S03, S04, S06, S07, S08, S09, S13, S17, S18, S11 | No W0 smoke seeds, and no smoke suite at enablement. Architecture §10 W0 item 3 seeds 3 smoke cases per W1 unit at W0 ("evaluation first"; the `pre-rewrite` baseline). S12-W0-5 counts on "S13-W0, S17-W0, S18-W0, S07-W1, S04-W1, S06-W1": none exist. S13-W1-9, S17-W1-12, S18-W1-9, S06-W1-3 write cases in W1 after the rewrite; S07-W2-5 in W2; S04 in W3. I16.3 condition 4 needs a passing smoke suite before V2 (vault-keeper, firecrawl, plugin-creator — S07 W2, S09 W3, S08 W3) and V3 (pubmed, CR — both W3). | Add W0 steps, each "3 `smoke` cases against today's skill, I17 layout, current plugin path", depends S12-W0-3 (micky) or S12-W0-4 (learn-hub): **S07** S07-W0-1 (vault-keeper + empty-vault, mined from `evals.json`); **S04** S04-W0-1 (psych-paper-digest), S04-W0-2 (CR); **S03** S03-W0-1 (pubmed); **S06** S06-W0-1 (clinical-infographic); **S08** S08-W0-1; **S09** S09-W0-1; **S13** S13-W0-1; **S17** S17-W0-1; **S18** S18-W0-1. **S12** S12-W0-5: depends on those ids. Later eval steps extend these dirs. **S11** S11-W1-1 and S11-W2-2: depend on the seeds of the plugins they add. |
| CX-5 | high | S07, S11 | H08/H09 do not close in W1. S07 §1.3 closes them at S07-W1-1, which only adds `sink.py` and `.vault-id`. The evidence lines (vault-keeper `SKILL.md:28-29`, `vault-layout.md:6-7`) change only in S07-W2-1 (SKILL.md), and `vault-layout.md` in no step. V2 (S11-W1-1) enables vault-keeper with the walk-up still live; the W1 exit test "vault-keeper from a learn-hub cwd → marker mismatch → asks" fails. | **S07**: new S07-W1-3 (depends S07-W1-1): SKILL.md Step 0 calls `sink.py resolve`; `vault-layout.md:6-7` names `sink.py`; done-when `grep -c "\.\./\.\./vault" <both files>` = 0 and no walk-up text. Remove the Step 0 part from S07-W2-1. §1.3 rows H08/H09: fix step S07-W1-1 + S07-W1-3. **S11** S11-W1-1: depends S07-W1-3. |
| CX-6 | high | S04, S11 | CR and psych-paper-digest keep hard-coded MCP prefixes when they join the cloud. I05 (S03) and architecture W2 item 2 / K4 need runtime resolution before research writers load. CR `SKILL.md:106-107` names `mcp__plugin_comprehensive-review_pubmed__<tool>`; S04 §2.3 W2 row 5 keeps it. psych-paper-digest `SKILL.md:64-65` and `sweep-recipes.md:8-9` hard-code theirs until W3. V3 loads pubmed + CR (endpoint dedup); V6 adds psych-paper-digest. | **S04** S04-W2-1: replace CR `SKILL.md:103-107` prefix text with the I05 resolution sentence (verbatim, S03 §2.7). S04-W1-1: same for psych-paper-digest `SKILL.md:64-65` and `sweep-recipes.md:8-9`. Done-when `grep -c "mcp__plugin_" <files>` = 0. **S11** S11-W2-2: depends S04-W2-1. |
| CX-7 | medium | S03, S04, S15 | I04 has no W2 text. Architecture W2 item 2 puts "the report contract in pubmed-research-note references" in W2. S04-W2-2 aligns CR's copy "to S03's W2 report-contract text"; S16 (W2) defers pk-plasma's brief to it. S03's W2 steps create no contract file and no fixtures (both W3). S15's `check-contract.mjs` has nothing to check at the W2 `--cross-repo` gate. | **S03**: new S03-W2-4 (depends S03-W2-1): create `plugins/pubmed-research-note/references/report-contract.md` (I04 text) and `plugins/pubmed-research-note/evals/fixtures/report-{decision,topic,digest}.md`; S03-W3-1 edits instead of creates (CX-2 moves them). **S04** S04-W2-2: depends S03-W2-4. **S15** §2.5: default dirs = `plugins/evidence/evals/fixtures` then `plugins/pubmed-research-note/evals/fixtures` (first that exists). |
| CX-8 | medium | S07, S05, S06, S03, S04 | I11 filing sentence. Architecture §4.2 fixes: "file via `vault-keeper` (OPTIONAL). If absent, write to `$LEARN_HUB_DIR/research-notes/` when its marker validates, otherwise to cwd, and say where." S07 §2.6 (owner) defines a different, self-referential sentence ("Run `vault-keeper:vault-keeper` … file via `vault-keeper` when present; if absent …"). S02/S03/S04/S09 use the architecture text; S05 H-7 and S06 H-CI2 use a visual variant. S03/S04 §2.7 ASSUME `kind: decision/topic` on the sink; S07's CLI takes `--kind report\|visual`. The owner contradicts the architecture. | **S07** §2.6/§2.7 I11: define two sentences — report = architecture §4.2 verbatim; visual = same with `research-notes/visuals/` and "passing `<slug>.html` and `<slug>.meta.json`". **S05** H-7, **S06** H-CI2: adopt S07's visual sentence verbatim; keep "Filing never publishes …" as a separate sentence. **S03, S04** §2.7 I11 row: "report, `sink.py --kind report`". |
| CX-9 | medium | S07, S15, S16 | Asset kind stored twice; the transfer drops `.meta.json`. I09 (S15) puts `kind` in `<slug>.meta.json`. S07 adds an `assets/<slug>.kind` sidecar, and its I12 manifest lists only the `.html` as `inbox_path`. An asset saved in the micky vault reaches `research-notes/visuals/` without the `.meta.json` that ingest-visual (S16) reads. | **S07** §2.3 save row and S07-W2-1: `save` stores `<slug>.meta.json` next to `<slug>.html`; drop the `.kind` sidecar. §2.7 I12 and S07-W2-4: kind comes from `.meta.json`; an asset item copies both files; missing `.meta.json` → `held`. Tests updated. |
| CX-10 | medium | S05, S15, S16 | Audit verdicts. I08 (S16) returns `pass\|fail`, with `skipped:["render","drive"]` and exit 0 when Chromium is missing. S05's `check-html.mjs` delegates and reports only `verdict`, so an unrendered file can be filed as `pass`. S05/S06 write `audit.verdict: pass\|incomplete`; I09 (S15) allows only `pass\|fail`. S05 delegates `--kind code-explainer`, which I08 rejects (exit 2). I09's `producer` example is `visuals:…` while W2 producers write bare names. | **S05** §2.5: when delegating, non-empty `skipped` → `verdict: incomplete`, exit 3; never delegate `code-explainer` (own port). **S15** §2.7 I09: `audit.verdict` = `"pass"\|"incomplete"` (a producer never files `fail`); `producer` = the `plugin:skill` name at write time. **S16** §2.5: drop "code-explainer" from the mapping rows or mark it own-port only. |
| CX-11 | medium | S08, S10, S11, S05, S06, S09 | Validator path breaks at S08-W3-1. It deletes repo-root `scripts/validate.py` and `bump.py`. No step updates `scripts/health.sh` (S10 ASSUMES S08 does it; S08 §2.7 says health.sh calls `validate.py --repo .` but has no step) or the lines S11-W0-3 adds. Later W3 commands still call `python3 scripts/validate.py` (S05-W3-4, S05 §5.1, S06 §5.1, S09-W3-4). | **S08** S08-W3-1: also edit `scripts/health.sh`: `python3 plugins/plugin-creator/scripts/validate.py --repo .` (+ `--cross-repo "$LEARN_HUB_DIR"` when set), `python3 -m unittest discover -s plugins -p 'test_*.py'`, `node --test 'plugins/*/scripts/*.test.mjs'`; keep S11's two lines. **S05, S06, S09**: W3 commands and acceptance use `$VALIDATE --repo .`. |
| CX-12 | medium | S05, S08, S09 | Release commands contradict I18. After S10-W0-2/-3 (W0), `bump.py` is dry-run by default and marketplace entries carry no version. S05-W2-6, S08-W1-2 and S09-W1-2 run `bump.py <p> <level>` without `--write` and expect `marketplace.json` versions. | **S05** S05-W2-6, **S08** S08-W1-2, **S09** S09-W1-2: `python3 scripts/bump.py <p> <level> --write`; files = `plugin.json` + `CHANGELOG.md`; done-when adds "marketplace.json has no `version`". Delete S08 §8 Q3 and S09 §8 Q4 ("today's tool"). |
| CX-13 | medium | S01, S02, S03, S04, S06, S07, S11 | Missing releases. Architecture W1 item 8 releases the touched plugins; S11-W1-2/S11-W2-5 refresh Windows (marketplace cache copies until W3) after them. Only S08-W1-2, S09-W1-2 and S05-W2-6 release. | New release steps (`bump.py <p> <level> --write`): **S04** S04-W1-3 (psych-paper-digest patch), S04-W2-3 (CR minor); **S06** S06-W1-5 (CI, CE patch), S06-W2-2 (CI minor); **S07** S07-W1-4 (minor), S07-W2-6 (minor); **S03** S03-W2-5 (minor); **S01** S01-W2-2 (intent-lock patch); **S02** S02-W2-2 (DI, PC patch). **S11** S11-W1-2, S11-W2-5: depend on them. |
| CX-14 | medium | S01, S03, S10 | Defined twice. S10-W3-2 moves `misreads.md` → `state/misreads.md` and pubmed's `.mcp.json` → `plugins/evidence/.mcp.json`. S01-W3-4 "creates" `state/misreads.md`; S01-W3-2 deletes `references/misreads.md` (already moved). S03-W3-1 "copies" `.mcp.json` and diffs it against `plugins/comprehensive-review/.mcp.json`, which S10-W3-2 has deleted. | **S01** S01-W3-4: "reformat the moved `state/misreads.md` to the I03 grammar; verify with `ledger.py list`"; S01-W3-2: drop the `misreads.md` delete. **S03** S03-W3-1: drop the `.mcp.json` create and diff; done-when `find plugins -name .mcp.json \| wc -l` = 1. |
| CX-15 | medium | S08, S10 | Router deletion defined twice. S08-W3-7 deletes `scripts/route.py`, `ROUTING.md` and all plugin-creator commands; S10-W3-9 deletes the same after the CLAUDE.md rewrite. S08-W3-7 would run first and leave CLAUDE.md naming deleted files. | **S08** S08-W3-7: delete only `plugins/plugin-creator/commands/` and route mentions inside plugin-creator. **S10** S10-W3-9: sole deleter of `ROUTING.md`/`route.py`; depends S08-W3-7, S10-W3-8. |
| CX-16 | medium | S03, S04, S16, S09, S01, S02 | I01 name at W2 and paraphrases. S01 §2.6: W2 callers use today's plugin name, W3 switches to `alignment:intent-lock`. S03 §2.6 and S04 §2.6 (applied in S03-W2-1, S04-W2-1) and S16 §2.6 (W2) write `alignment:intent-lock`, which resolves only after S10-W3-2; on Windows Step 0 always falls back until W3. S16's sentence is a paraphrase marked "verbatim". S02's W2 text extends the sentence. S09-W3-1 writes the W3 name with no dependency on the skeleton. | **S03, S04**: W2 text `intent-lock:intent-lock`; S03-W3-4 / S04-W3-3 switch to `alignment:intent-lock`. **S16** §2.6: copy S01's I01 sentence verbatim with the bare names `intent-lock` and `pubmed-research-note` (a learn-hub skill with no W3 step; bare names resolve before and after the rename, PLG-17). **S01** §2.7 I01: allow the bare skill name for callers that outlive the W3 rename. **S02**: keep the I01 sentence verbatim and put "draft the plan, then offer to critique" in a separate sentence. **S09** S09-W3-1: depends S10-W3-2. |
| CX-17 | medium | S13, S15, S16, S17, S18, S19, S20 | I13 handoff has seven forms. S13 §2.6 says callers carry "Run sync-vault (OPTIONAL) … take the broadest reading …" (a broadest-reading fallback makes no sense for a publish step). S15/S16 say REQUIRED; S17/S18 "Run the sync-vault tail (I13)"; S19 §2.6 and S20 §2.3 carry fallbacks that restate the tail, which architecture §2.4 forbids ("link to it and never restate it"). | **S13** §2.6: one sentence — "Publish through the `sync-vault` skill (same repo, always present). Follow its steps as written; do not restate them here." **S15, S16, S17, S18, S19, S20**: carry it verbatim; S19 §2.6 and S20 §2.3/§2.6 drop the restated fallback. |
| CX-18 | medium | S08 | I20 contradicts the architecture and itself. The whitelist allows `argument-hint` on alias skills only; architecture §3.3 moves argument handling to the target skill, and S01–S07 put it on non-alias skills. The alias template writes unquoted `{{…}}` placeholders and `argument-hint: [{{ARG_HINT}}]` (a YAML list) — the defect class S08-W3-5 fixes. The template description has no `Use when`/`Not for`, which VAL-04 fails. | **S08** §2.7 I20: `argument-hint` allowed on any user-typeable skill; template quotes every placeholder (`name: "{{ALIAS_NAME}}"`, `argument-hint: "[{{ARG_HINT}}]"`). §2.5 VAL-04: skills with `disable-model-invocation: true` and an `Invoke …` body are exempt from the order/`Use when` rules (description ≤150 chars instead). |
| CX-19 | medium | S12, S10, S08, S21 | Ratchet and trigger-lock schema and parsers. Owner S12: `{generated_at, repo, entries:[{check_id,path,message}]}` and `{phrases:[{phrase,kind,skill,field}], removed:[]}`. S10-W0-1/-1b read and write `{"yaml-parse":[paths]}`; S08 ASSUMES keys `"<check-id>:<path>"` and a per-skill lock; S21 ASSUMES a `schema` field. Four parsers exist (S10 validate.py W0, S12 `rewrite_gate`, S08 VAL-06/ratchet, S21 skill-lint check 9). | **S10** S10-W0-1: read S12's `entries[]` (check id `yaml-parse`); S10-W0-1b becomes `python3 scripts/rewrite_gate.py ratchet seed --check yaml-parse --write`, depends S12-W0-1. **S12**: expose `rewrite_gate.py` and `lib/rewrite-gate.mjs` functions as a library; add `"schema": 1` to both files. **S08** §2.5 VAL-06 + ratchet: import S12's functions; §8 Q1 closed. **S21** §2.5 check 9: import `scripts/lib/rewrite-gate.mjs`. |
| CX-20 | medium | S08 | I25 invocation. S08 ASSUMES `node $LEARN_HUB_DIR/scripts/check-contract.mjs $MICKY_TOOLS_DIR`; S15's CLI has no positional argument (`[--dir <path>] [--json]`). | **S08** §2.5 VAL-14 and §2.7 I25 row: `node "$LEARN_HUB_DIR/scripts/check-contract.mjs" --dir "$MICKY_TOOLS_DIR/plugins/evidence/evals/fixtures" --json`; fail on exit 1. |
| CX-21 | medium | S08, S12 | Committed lists have no owner. VAL-03/05/10 need `synced-names.md`, `sibling-pairs.md`, `dmi-skills.md`, `fork-denylist.md`, `gate-skills.md`; S08 says S12 owns them; S12 neither defines nor creates them. | **S08**: owns them; S08-W3-1 creates `plugins/plugin-creator/references/lists/*.md` from architecture §2.8 (synced names), §6.3 families (sibling pairs), OD9/OD10 (dmi), §8 (fork denylist, gate skills). **S12**: no change. |
| CX-22 | medium | S08 | The plugin-creator SessionStart hook never fires in cloud. S08 §2.6 tests `"$CLAUDE_CODE_REMOTE" = "1"`; the cloud sets `true` (this VM; learn-hub `session-start.sh:8` tests `!= "true"`). | **S08** §2.6 hooks.json: `test "$CLAUDE_CODE_REMOTE" = "true"`. |
| CX-23 | medium | S07, S10 | Eval layout deviates from I17 (`plugins/<p>/evals/<skill>/<case>/`). S07-W2-5 and S07 §5 item 11 use `plugins/vault-keeper/skills/<skill>/evals/<case>/`; S12-W0-5's find pattern misses it. S10-W0-5 draws `skills/<skill>/evals/<case>/` in the CLAUDE.md layout. | **S07** S07-W2-5, S07-W0-1, §2.1, §5.11: `pvk/evals/{vault-keeper,empty-vault}/<case>/`. **S10** S10-W0-5: diagram line `evals/<skill>/<case>/`. |
| CX-24 | medium | S16 | `/pk-animation` is a command file. S16-W2-5 creates `.claude/commands/pk-animation.md`; OD9-a and §3.5 make it a dmi alias skill (S20 does this for `/vectors`). | **S16** S16-W2-5: create `.claude/skills/pk-animation/SKILL.md` from I20's alias template (`disable-model-invocation: true`, body `Invoke pk-plasma-animation with: $ARGUMENTS`); no `.claude/commands/`. |
| CX-25 | medium | S16, S21 | `audit:visual` npm script has no step. S21's I22 registry says S16-W2-2 adds it; S16-W2-2 creates only `scripts/audit-visual.mjs`. S05's `check-html.mjs` delegates through `npm run -s audit:visual`. | **S16** S16-W2-2: add `"audit:visual": "node scripts/audit-visual.mjs"` to `package.json`; done-when `npm run -s audit:visual -- --help` exits 0. **S21** I22 row: step id S16-W2-2 confirmed. |
| CX-26 | medium | S21, S18 | Tests S18 adds never run. S21's `test:py` discovers only `.claude/skills/atomize-book/scripts`; S18's `test_classify_pdf.py` is in `.claude/skills/pdf-pipeline/scripts/`. `vitest.config.ts` includes only `src/**` and `scripts/**/*.test.mjs`, so S18-W4-3's `.claude/skills/verify/scripts/*.test.mjs` never run. S18's `mint-session.mjs` `loadEnv()` pattern resolves `.claude/skills/verify/.env.local` from that folder. | **S21** §2.7 I22 + S21-W0-2: `test:py` = `for d in .claude/skills/*/scripts; do python3 -m unittest discover -s "$d" -p 'test_*.py' \|\| exit 1; done`. **S18** S18-W4-3: pure modules and tests at `scripts/lib/verify-{mint,probe}.mjs` + `.test.mjs` (CLI wrappers stay in the skill); resolve the repo root by walking to the learn-hub marker. |
| CX-27 | medium | S15, S16, S19, S09 | The delivery log is misused. S15's and S16's OWNER steps and S19-W4-1 append notes to learn-hub `docs/rewrite/delivery-log.md`; S09-W5-1 may too. I16.4 keeps the log in micky, and its grammar (DL rules) accepts only variable rows, so `delivery_log.py check` fails on a note. | **S15, S16**: record the verification against H15/H16 and H29/H31 in learn-hub `docs/rewrite/h-coverage.md`. **S19** S19-W4-1: record the freeze in the learn-hub CHANGELOG. **S09** S09-W5-1: gridgeist CHANGELOG only. |
| CX-28 | medium | S13, S19, S21 | I21 gotcha moves: nobody deletes some text, and S21-W4b-1 lacks deps. S13-W4-1 says S21 deletes moved headings from CLAUDE.md; S21-W4a-2 says the 26 atomize-book and 20 sync-vault headings stay until S19-W4-8/S13-W4-1 delete them. S21-W4b-1 assumes they are gone but depends only on S21-W4a-2. Candidate counts differ (S13 lists 6–7 vs 20; S19 lists 23 vs 26). The archive (S21-W4a-3) is written after the deletions. | **S13** S13-W4-1 and **S19** S19-W4-8: move AND delete, in one commit, exactly the headings `gotcha-map.md` assigns; the map wins over their candidate lists; both depend on S21-W4a-2. **S21**: order S21-W4a-1 → S21-W4a-3 (archive first) → S21-W4a-2 → {S13-W4-1, S19-W4-8} → S21-W4b-1 (depends S13-W4-1, S19-W4-8). |
| CX-29 | medium | S05, S19 | H-11 has no step. S05 §2.6 H-11 rewrites atomize-book `SKILL.md:588-590` (visuals go through the inbox and ingest-visual) and says S05-W2-7 applies it; S05-W2-7 is an owner check; S19 has no step on those lines. | **S19**: new S19-W2-1 (learn-hub; depends S16-W2-3): replace `SKILL.md:588-590` with S05's H-11 text (outside the W4 freeze). **S05** §2.6: "applied by S19-W2-1". |
| CX-30 | medium | S05, S11 | The atomic-swap check is defined twice: S05-W2-7 (owner confirms micky CA loads in a learn-hub branch session) and S11-W2-3 actions (1)–(4). | **S05**: delete S05-W2-7; S05-W2-8 = push the learn-hub deletion branch (depends S05-W2-6, S16-W2-5); merge happens in S11-W2-3. **S11** S11-W2-3: depends S05-W2-8. |
| CX-31 | medium | S16, S05 | S16-W2-1's done-when tests against "S05's 6-row parity fixture", created by S05-W2-1 later in W2 (architecture W2: learn-hub consumers before micky renderers); a cross-repo test read also breaks "npm test never depends on the micky checkout" (§8). S16-W2-2 and S16's OWNER step use `.claude/skills/concept-animation/examples/…`, which S05-W2-8 deletes later in W2. | **S16** S16-W2-1: vitest cases with inline HTML strings of the two I07-J bad shapes; no S05 file. S16-W2-2 and OWNER step: use `vault/tms-principles/tms-electromagnetic-induction.html`. **S05**: parity comparison stays at S05-W2-5 / W2 exit and S08 VAL-14. |
| CX-32 | medium | S10, S05, S06 | Examples location. S10-W3-2 moves `examples/` into each skill dir. Architecture §3.2 (ML "example via `${CLAUDE_PLUGIN_ROOT}/examples/`") and S05 (fix ml-concept-lab-5; §5.5 greps `plugins/visuals/examples/*.html`) expect plugin root. The owner contradicts the architecture. | **S10** S10-W3-2: move members' `examples/*` to `plugins/visuals/examples/`. **S06** S06-W3-1: rename CI `examples/README.md` → `ppgl-perioperative-management.md` (S05-W2-4 already renames ML's README) and fix its link. |
| CX-33 | medium | S05, S06 | The code-explainer `--source` flag has no implementer. S05 §2.7 I07-K says S06 adds it in W3; S06 §2.7 and S06-W3-3 say S05-W3-1 adds it. | **S06**: S06-W3-3 implements `--kind code-explainer --source <file>` in `V/scripts/check-html.mjs` + tests (depends S05-W3-1); §2.7 ASSUMES row removed. **S05** I07-K unchanged. |
| CX-34 | medium | all | Informal depends-on. Replace each with a step id (section 2 uses these): S01-W3-1…6 "S10's skeleton-PR commit" → S10-W3-2; S01-W3-4 "S14's W2 fork-merge" → S14-W2-2; S01-W3-5 "S02's W3 files" → S02-W3-2, S02-W3-3; S02-W3-1…3, S03-W3-1, S04-W3-1…4, S05-W3-1, S06-W3-1 → S10-W3-2; S05-W2-7 "S11's schedule" → deleted (CX-30); S07-W2-1/-4 "S15" → S15-W2-1; S07-W2-5 "S12" → S12-W0-3; S07-W3-1 "S08" → S10-W3-2; S08-W3-1 "S10's W0" → S10-W0-1, S10-W0-2, S10-W0-3; S08-W3-7 → S10-W0-4; S09-W3-1 "S08's I19/I20" → S08-W3-1; S10-W3-1 → S11-W3-1; S10-W3-8 "S01–S08" → S01-W3-6, S02-W3-4, S03-W3-7, S04-W3-6, S05-W3-5, S06-W3-4, S07-W3-1, S08-W3-9, S09-W3-4; S11-W0-3 → S10-W0-9; S11-W1-1 → S07-W1-4, S08-W1-2, S09-W1-2 + seeds; S11-W1-2 → W1 releases; S11-W2-2 → S03-W2-5, S04-W2-3, S05-W2-6, S06-W2-2; S11-W2-3 → S05-W2-8; S11-W2-4 → S14-W1-2, S14-W2-1, S14-W2-3, S14-W2-4, S14-W2-5, S15-W2-3, S16-W2-6, S20-W2-1, S20-W2-2; S11-W3-4 → S09-W3-1; S11-W3-5 → S10-W3-2; S12-W0-1 "S10-W0" → S10-W0-1; S12-W0-6 → S11-W0-9; S12-W3-1 → the eval steps; S12-W3-4 → S11-W3-5; S12-W4-1 → S13-W1-9, S17-W4-3, S18-W4-4, S19-W4-9; S13-W1-10 → S11-W0-11; S13-W4-1 → S21-W4a-2; S14-W2-1 → S11-W0-7; S14-W2-5 → + S15-W2-3, S16-W2-6, S20-W2-1, S20-W2-2; S17-W1-3/-9 → S13-W1-2; S17-W1-6/-11 → S13-W1-6; S17-W4-1 → S21-W4a-2; S17-W4-3, S18-W4-4 → S12-W0-4; S18-W1-3 → S13-W1-2; S18-W1-4…-6 → S13-W1-6; S19-W1-2 → S13-W1-6; S19-W1-7 → S13-W1-2; S19-W4-8 → S21-W4a-2; S21-W4a-3 "S16's W2 exit" → S16-W2-6. Also closes S11 §8 Q10/Q11 (owners: firecrawl S09; forks/catalog S14; CA copy S05-W2-8; micky CLAUDE.md W3 S10-W3-8; README install S11-W3-3; learn-hub CLAUDE.md W1 S21). | Edit each named step's `depends on` line as listed. |
| CX-35 | medium | S03, S04, S05, S06, S07 | W2 "consumers before producers" is not encoded. S03-W2-1 and S04-W2-1 (report/1 + filing) do not depend on the tolerant reader (S15-W2-2); S05-W2-3/-4 and S06-W2-1 (visual filing with `.meta.json`) do not depend on ingest-visual (S16-W2-3). | **S03** S03-W2-1, **S04** S04-W2-1: + S15-W2-2. **S05** S05-W2-3, S05-W2-4, **S06** S06-W2-1: + S16-W2-3. **S07** S07-W2-1: + S15-W2-1. |
| CX-36 | medium | S03, S04, S05, S06, S07, S08, S09 | W3 order: skeleton first, alignment before evidence and visuals. S08-W3-1 (moves validate.py; would break S10-W3-2's own done-when), S09-W3-1/-2 and S07-W3-1 do not depend on S10-W3-2. Evidence and visuals steps that consume the lock record or write `alignment:` names do not depend on the alignment rewrite. | **S08** S08-W3-1, **S09** S09-W3-1/-2, **S07** S07-W3-1: + S10-W3-2. **S03** S03-W3-1, S03-W3-2; **S04** S04-W3-2; **S05** S05-W3-1; **S06** S06-W3-2: + S01-W3-2. |
| CX-37 | medium | S12, S01–S09, S17, S18 | Live trigger runs are not ordered. S12-W3-2 (BEFORE) depends only on S12-W0-6; the W3 description steps (S01-W3-2, S02-W3-2/-3, S03-W3-4, S04-W3-3, S05-W3-2, S06-W3-2, S08-W3-2/-3, S09-W3-1) do not depend on it. Architecture W4 item 8 runs live trigger evals for the PDF and atomize families; S12 has no W4 live-trigger step (S17-W4-4/S18-W4-5 only hand over queries). | **S12** S12-W3-2: depends S10-W3-2; each listed description step: + S12-W3-2; S12-W3-3 depends on all of them. **S12**: new S12-W4-2 (BEFORE, depends S12-W0-6) and S12-W4-3 (AFTER, depends S17-W4-4, S18-W4-5) for those two families; note that the W1 description edits (S17-W1-2/-8, S18-W1-8, S19-W1-8) are guarded only by the trigger lock. |
| CX-38 | medium | S17, S18 | Cycle. S17-W4-4 depends on "S18-W4" (all S18 W4 steps); S18-W4-5 depends on S17-W4-4. | **S17** S17-W4-4: depends S18-W4-1 (routing text), not "S18-W4". |
| CX-39 | medium | S13, S16, S17, S19, S21, S10, S11, S08 | Same file, same or adjacent wave, no order. learn-hub `package.json`: S21-W0-2 (W0), S13-W1-5 and S19-W1-4 (W1), S16-W2-2 (W2). learn-hub `.gitignore` (W1): S13-W1-8, S17-W1-1. micky `MEMORY.md` (W3): S11-W3-1, S10-W3-10. micky `scripts/health.sh`: S10-W0-9, S11-W0-3, S08-W3-1. micky `marketplace.json`: S10-W0-3, S10-W3-1 (no other writer after CX-12). learn-hub `CLAUDE.md`: S21 only. `.claude/settings.json`: S13-W1-7 only. | **S13** S13-W1-5: + S21-W0-2. **S19** S19-W1-4: + S13-W1-5. **S16** S16-W2-2: + S19-W1-4. **S17** S17-W1-1: + S13-W1-8. **S10** S10-W3-10: + S11-W3-1 (keep S11's delivery line at `MEMORY.md:11`). **S08** S08-W3-1: + S11-W0-3. |
| CX-40 | medium | S12, S11 | No step creates the `pre-rewrite` tag (W0 entry; §6.4 baseline worktree) or the `wave-N` tags (§7 rollback). No step writes `docs/rewrite/baseline.md` at W0, though S12 owns its format. | **S12**: new S12-W0-0 (OWNER, both repos, first W0 step): `git tag pre-rewrite && git push origin pre-rewrite`; new S12-W0-7 (both repos, depends S12-W0-1/-2): `baseline measure … --write`; new S12-W<n>-T at each wave exit: tag `wave-<n>` in each touched repo. |
| CX-41 | medium | S16 | ingest-visual files before it audits. S16 §2.3 rows 5–6: Step 2 writes the sidecar + HTML into the topic dir; Step 3 runs `audit:visual` and refuses. Architecture §5.5: never file an asset whose audit fails; a refused asset left in `/vault` publishes on the next unrelated sync. | **S16** §2.3: Step 2 = audit (fail → write the `refused` I10 line, return findings, stop); Step 3 = file sidecar + HTML. |
| CX-42 | medium | S03, S04 | Test files the health check never runs. `sources_lint.test.py` and `sweep.py.test.py` do not match `-p 'test_*.py'` (architecture §6.6, S10 health.sh, S08 VAL-15); `python3 -m unittest <dotted file>` fails. | **S03** §2.5, S03-W3-5: `test_sources_lint.py`. **S04** §2.1, §2.5, S04-W3-1: `test_sweep.py`. Commands: `python3 -m unittest discover -s plugins/evidence/scripts -p 'test_*.py'`. |
| CX-43 | medium | S07, S04, S11 | W2 exit checks have no owner: the rehearsal (fixture report in the micky vault → `/empty-vault` transfer → inbox → "digest" → sync → provenance count), "a multi-repo report lands in `research-notes/` and is not digested without 'digest'", and one unattended `daily-random-review` run. | **S07**: new S07-W2-7 (OWNER; depends S07-W2-4, S15-W2-2, S14-W2-4, S11-W2-4): run the rehearsal and the no-digest check. **S04**: new S04-W2-4 (OWNER; depends S11-W2-2): the unattended run. |
| CX-44 | low | S05, S16 | I07-H and S16 §2.5 say "21 codes total"; the listed ids count 26 (6 + 3 + 2 + 9 + 6). S05-W2-1 says 26. | **S05** §2.7 I07-H, **S16** §2.5: "26 codes total". |
| CX-45 | low | S05, S07, S08, S09 | README/CHANGELOG/LICENSE created twice. S10-W0-8 backfills LICENSE (firecrawl, plugin-creator, CA, ML, …), gridgeist README/CHANGELOG, CA/ML/DI/CE CHANGELOG. S05-W2-6, S08-W3-1, S09-W3-1, S09-W3-2 "create" the same files. S07-W1-1 assumes license `UNLICENSED` (owner question) while S10 writes MIT. | **S05** S05-W2-6, **S08** S08-W3-1, **S09** S09-W3-1/-2: edit, not create; + S10-W0-8. **S07** S07-W1-1: `"license": "MIT"`; + S10-W0-8; drop the license OWNER question. |
| CX-46 | low | S01, S02, S03, S12, S13, S15, S16 | Runner call shapes. S01/S02 call `eval.sh --smoke plugins/alignment` (S12 takes a dir name → `plugins/plugins/alignment`). S03 appends `--allow-tools Write`, which `eval.sh` does not pass on. `eval-project-skill.sh <skill> [-- <args>]`: consumers pass args without `--` and without pinned models or budget. | **S01, S02** §4.4: `eval.sh --smoke alignment`. **S12** §2.5/§2.7: `eval.sh` passes args after `--`; `eval-project-skill.sh` gains `--smoke`/`--release` with the same pinned models and `--max-cost-usd`, passing other args with or without `--`. **S03** §4.4: `-- --allow-tools Write`. **S13, S15, S16**: use `--smoke`/`--release`. |
| CX-47 | low | S01, S02 | S01-W3-5 depends on "S02's W3 files" while S02-W3-4 depends on S01-W3-5. | **S01** S01-W3-5: depends S02-W3-2, S02-W3-3 (not S02-W3-4). |
| CX-48 | low | S13 | S13-W1-7 removes the PreToolUse gates with no dependency on S13-W1-4 (gates inside `apply-sync.mjs`); a commit window has no gates. | **S13** S13-W1-7: + S13-W1-4. |
| CX-49 | low | S10, S21, S01, S03, S05, S08, S09, S11 | S11 §2.6 sentences are not carried: item 1 (README "## Surfaces"), item 2 (micky CLAUDE.md delivery line), item 3 (learn-hub CLAUDE.md delivery line), item 4 (wave-exit "Ready for cloud delivery" line; only S14 has it). | **S10** S10-W3-8: item 2 verbatim. **S21** S21-W1-4: item 3 verbatim. **S01** S01-W3-5, **S03** S03-W3-7, **S05** S05-W3-5, **S08** S08-W3-4 (own README), **S09** S09-W3-1: item 1. Every plugin spec's wave-exit line: item 4. |
| CX-50 | low | S11 | I16.3 exceptions are silent. At V3, pubmed joins with H45 open (W3); at V6 (W3 entry), intent-lock, decision-interview, plan-critique and psych-paper-digest load with no smoke suite (their cases are W3). Architecture §2.7 condition 1 says "all HIGH defects closed"; its own schedule contradicts that (S11 ARCH-CONFLICT 4). | **S11** S11-W2-2 and S11-W3-1: record these as named exceptions in the log's evidence cell (reading: defects due by that wave; the four plugins' callers carry fallbacks, architecture §2.7 W3 row). Owner confirms the reading. |
| CX-51 | low | S09, S11 | `defaultEnabled: false` (S09-W3-1, OD12-a) disables firecrawl in cloud from W3, because multi-repo sessions keep no user settings (S11 ARCH-CONFLICT 1). S11-W3-4 is conditional on an owner answer that no step asks for. | **S11**: make S11-W3-4 ask the owner explicitly (keep the flag + setup-script enable block, or drop the flag). **S09** S09-W3-1: follows the answer. |
| CX-52 | low | S21 | skill-lint check 7 warns on every dmi skill whose body is over 10 lines, so every user-only skill (vault-atomizer, vault-vectors, vault-coverage, check-repetition, pk-plasma-animation) warns. | **S21** §2.5 check 7: apply only to skills whose body is an `Invoke …` alias line. |
| CX-53 | low | S12, S20 | No eval pattern for dmi skills. S20 §8 asks whether a dmi skill's Skill tool fires; S12-W4-1 runs trigger-tagged smoke on dmi skills (vault-coverage, check-repetition). | **S12** §2.7 I17: dmi skills use an explicit `/<name>` prompt as the positive case and natural-language near-misses as negatives. **S20**: follow it. |
| CX-54 | low | S04 | The lit-watch rename breaks the trigger lock: `triggers.lock.json` rows keyed `skill: psych-paper-digest` fail VAL-06 after S04-W3-3. | **S04** S04-W3-3: re-key the rows with `rewrite_gate.py triggers remove/extract`, reason "renamed OD7-a". |
| CX-55 | low | S16, S21 | Placeholder steps with no commit break "one step = one commit": S16-W1-3, S21-W1-2, S21-W1-3. | **S16, S21**: move them to §8 notes; drop the ids. |
| CX-56 | low | S06 | S06-W1-1's done-when runs `node --input-type=module -e "…require('fs')…"`; `require` is undefined in ESM, so the check cannot pass. | **S06** S06-W1-1: use `import('fs')` or `--input-type=commonjs` with a dynamic `import()` of the audit module. |
| CX-57 | low | S08 | S08-W1-1's guard walks cwd up 3 parents. Architecture §3.2 W1 guard is "`MICKY_TOOLS_DIR` → marker; else stop" (R47, no walk-up). | **S08** S08-W1-1: drop the walk-up; `MICKY_TOOLS_DIR` + marker, else stop. |
| CX-58 | low | S14, S08 | I15 details. `hooks.json` uses `"command":"bash","args":[…]`; S08's hook uses a single command string. `learn-hub-session` ships no LICENSE (architecture §8 check). Author "Thanawat Suharit" vs "Thanawat Suharit (Micky)" elsewhere. | **S14** §2.7 I15: pick the form W0 check b's probe proved (S11-W0-7), same as S08's template; add LICENSE; author "Thanawat Suharit (Micky)". |
| CX-59 | low | S14 | §2.1 tree comment names wrong specs: conversions are S15 (digest-report), S16 (pk-plasma), S20 (vault-atomizer, vault-vectors), not "S15/S19/S20/S06". | **S14** §2.1: fix the ids. |
| CX-60 | low | S15, S16 | Fix-step ids in §1.3 point at the wrong step: H16 at S15-W2-1 (closes at S15-W2-2/-3); H29/H31 at S16-W2-2 (closes at S16-W2-3/-4). `h-coverage.md` closure evidence would cite the wrong commit. | **S15** §1.3 H16 row, **S16** §1.3 H29/H31 rows: correct the step ids. |
| CX-61 | low | S11, S13 | S11 §8 Q9: learn-hub `docs/cloud-env-setup.md:144` still recommends `npm run sync`; S13 (owner of the tail) has no step. | **S13**: add to S13-W1-6 (or a new S13-W1-11) the one-line edit to `npm run sync:preflight`. |
| CX-62 | low | S10 | `mkdir state/lit-watch` in S10-W3-2 is a no-op in git (empty dirs are not tracked). | **S10** S10-W3-2: drop it; S04-W3-1 creates the files. |

---

## 2. Merged step order per wave

Conventions: dependencies include the fixes above. "new" marks a step a finding adds. OWNER = only the owner can do it. Architecture §10 order is kept: W0 safety net first; W1 learn-hub starts with S13; W2 learn-hub consumers → micky producers → renderers → vault-keeper → forks → cloud; W3 delivery switch → S10 skeleton → alignment → evidence → visuals → standalone → diet → exit; W4 freeze window for atomize-book.

### W0 — ground truth and safety net

| # | Step | Spec | Repo | Title | Depends on | OWNER |
|---|---|---|---|---|---|---|
| 1 | S12-W0-0 (new, CX-40) | S12 | both | Tag `pre-rewrite` | — | yes |
| 2 | S10-W0-3 | S10 | micky | Strip marketplace versions | — | no |
| 3 | S10-W0-1 | S10 | micky | validate.py: guarded loads, counted checks, CRLF YAML, stdio | — | no |
| 4 | S10-W0-2 | S10 | micky | bump.py rewrite (plugin.json only, `--write`) | S10-W0-1, S10-W0-3 | no |
| 5 | S10-W0-4 | S10 | micky | route.py argparse, no versions | — | no |
| 6 | S10-W0-7 | S10 | micky | `.gitignore` | — | no |
| 7 | S10-W0-8 | S10 | micky | README/CHANGELOG/LICENSE backfill | — | no |
| 8 | S10-W0-9 | S10 | micky | `scripts/health.sh` | S10-W0-1 | no |
| 9 | S10-W0-10 | S10 | micky | `.githooks/pre-commit` | S10-W0-9 | no |
| 10 | S10-W0-11 | S10 | micky | Enable hooksPath once per clone | S10-W0-10 | yes |
| 11 | S10-W0-5 | S10 | micky | CLAUDE.md version rule, mandate demotion, layout | S10-W0-1…4 | no |
| 12 | S10-W0-6 | S10 | micky | README fixes | S10-W0-1, S10-W0-7 | no |
| 13 | S12-W0-1 | S12 | micky | rewrite_gate.py, ratchet, triggers.lock, h-coverage | S10-W0-1, S10-W0-9 | no |
| 14 | S10-W0-1b | S10 | micky | Ratchet seed `yaml-parse` via rewrite_gate (CX-19) | S12-W0-1 | no |
| 15 | S12-W0-3 | S12 | micky | `scripts/eval.sh` | S12-W0-1 | no |
| 16 | S11-W0-1 | S11 | micky | delivery_log.py + tests | — | no |
| 17 | S11-W0-2 | S11 | micky | delivery-log.md + cloud-setup.sh v1 | S11-W0-1 | no |
| 18 | S11-W0-3 | S11 | micky | health.sh runs the log checker | S11-W0-2, S10-W0-9 | no |
| 19 | S21-W0-1 | S21 | learn-hub | skill-lint.mjs + tests | — | no |
| 20 | S21-W0-2 | S21 | learn-hub | package.json `test:py` (all skills, CX-26), `check:skills` | S21-W0-1 | no |
| 21 | S12-W0-2 | S12 | learn-hub | rewrite-gate.mjs, ratchet, triggers.lock, h-coverage | — | no |
| 22 | S12-W0-4 | S12 | learn-hub | `scripts/eval-project-skill.sh` | S12-W0-2 | no |
| 23 | S12-W0-7 (new, CX-40) | S12 | both | `baseline.md` W0 section | S12-W0-1, S12-W0-2 | no |
| 24 | S11-W0-4 | S11 | learn-hub | cloud-env-setup.md §3C | — | no |
| 25 | S11-W0-6 | S11 | learn-hub | Rules probe branch (never merged) | — | no |
| 26 | S11-W0-5 | S11 | env + micky | Configure cloud env, V0 | S11-W0-2 | yes |
| 27 | S11-W0-7 | S11 | env + micky | Checks a, b, e, f, h | S11-W0-5, S11-W0-6 | yes |
| 28 | S11-W0-8 | S11 | micky | Check c (renames) | S11-W0-2 | no |
| 29 | S11-W0-9 | S11 | micky | Check d (eval enabled; cost approval) | S11-W0-2 | yes |
| 30 | S12-W0-6 | S12 | micky | Record eval availability | S11-W0-9 | yes |
| 31 | S11-W0-10 | S11 | Windows + micky | Check g, Windows variables | S11-W0-2 | yes |
| 32 | S07-W0-1 (new, CX-4) | S07 | micky | Smoke seeds vault-keeper, empty-vault | S12-W0-3 | no |
| 33 | S04-W0-1 (new, CX-4) | S04 | micky | Smoke seeds psych-paper-digest | S12-W0-3 | no |
| 34 | S04-W0-2 (new, CX-4) | S04 | micky | Smoke seeds comprehensive-review | S12-W0-3 | no |
| 35 | S03-W0-1 (new, CX-4) | S03 | micky | Smoke seeds pubmed-research-note | S12-W0-3 | no |
| 36 | S06-W0-1 (new, CX-4) | S06 | micky | Smoke seeds clinical-infographic | S12-W0-3 | no |
| 37 | S08-W0-1 (new, CX-4) | S08 | micky | Smoke seeds plugin-creator | S12-W0-3 | no |
| 38 | S09-W0-1 (new, CX-4) | S09 | micky | Smoke seeds firecrawl | S12-W0-3 | no |
| 39 | S13-W0-1 (new, CX-4) | S13 | learn-hub | Smoke seeds sync-vault | S12-W0-4 | no |
| 40 | S17-W0-1 (new, CX-4) | S17 | learn-hub | Smoke seeds ingest-article | S12-W0-4 | no |
| 41 | S18-W0-1 (new, CX-4) | S18 | learn-hub | Smoke seeds pdf-pipeline | S12-W0-4 | no |
| 42 | S12-W0-5 | S12 | both | Seed checklist (≥3 per unit) | rows 32–41 | no |
| 43 | S11-W0-11 | S11 | env + micky | W0 exit: remove probe, V0→V1, setup v2 | S11-W0-7…10 | yes |
| 44 | S12-W0-T (new, CX-40) | S12 | both | Tag `wave-0` | all above | yes |

### W1 — stop active harm (learn-hub first)

| # | Step | Spec | Repo | Title | Depends on | OWNER |
|---|---|---|---|---|---|---|
| 1 | S13-W1-1 | S13 | learn-hub | readiness.mjs + tests | — | no |
| 2 | S13-W1-2 | S13 | learn-hub | ready.mjs | S13-W1-1 | no |
| 3 | S13-W1-3 | S13 | learn-hub | sync-preflight.mjs + tests | S13-W1-1 | no |
| 4 | S13-W1-4 | S13 | learn-hub | apply-sync runs the preflight | S13-W1-3 | no |
| 5 | S13-W1-5 | S13 | learn-hub | package.json `sync:preflight` | S13-W1-3, S21-W0-2 | no |
| 6 | S13-W1-6 | S13 | learn-hub | sync-vault SKILL.md rewrite (+ CX-17 sentence, CX-61) | S13-W1-2, S13-W1-3, S13-W1-5 | no |
| 7 | S13-W1-7 | S13 | learn-hub | settings.json PreToolUse removed; gate scripts deleted | S13-W1-4 | no |
| 8 | S13-W1-8 | S13 | learn-hub | session-start.sh root, done-marker, ready line; .gitignore | — | no |
| 9 | S13-W1-9 | S13 | learn-hub | sync-vault evals (extend seeds) | S13-W1-6, S13-W0-1 | no |
| 10 | S17-W1-1 | S17 | learn-hub | .gitignore `Raw Article PDF/` | S13-W1-8 | no |
| 11 | S17-W1-2 | S17 | learn-hub | ingest-article frontmatter | — | no |
| 12 | S17-W1-3 | S17 | learn-hub | Preflight + inbox survey-and-ask | S17-W1-1, S13-W1-2 | no |
| 13 | S17-W1-4 | S17 | learn-hub | Seed-count text | — | no |
| 14 | S17-W1-5 | S17 | learn-hub | check-mermaid.mjs | — | no |
| 15 | S17-W1-6 | S17 | learn-hub | Sync section → sync-vault | S17-W1-5, S13-W1-6 | no |
| 16 | S17-W1-7 | S17 | learn-hub | figures-and-loss.md flags | — | no |
| 17 | S17-W1-8 | S17 | learn-hub | ingest-slides description | — | no |
| 18 | S17-W1-9 | S17 | learn-hub | ingest-slides script paths + preflight | S13-W1-2 | no |
| 19 | S17-W1-10 | S17 | learn-hub | extract_pdf/render_slides text | — | no |
| 20 | S17-W1-11 | S17 | learn-hub | Slides figure/loss gates + sync | S13-W1-6 | no |
| 21 | S17-W1-12 | S17 | learn-hub | ingest-article/-slides evals | S17-W1-2, S17-W1-8, S17-W0-1 | no |
| 22 | S18-W1-1 | S18 | learn-hub | routing.md: decks → ingest-slides | — | no |
| 23 | S18-W1-2 | S18 | learn-hub | pdf-pipeline slides branch | S17-W1-8 | no |
| 24 | S18-W1-3 | S18 | learn-hub | Preflight = ready.mjs | S13-W1-2 | no |
| 25 | S18-W1-4 | S18 | learn-hub | Sync section → sync-vault | S13-W1-6 | no |
| 26 | S18-W1-5 | S18 | learn-hub | preflight-and-apply.md | S13-W1-6 | no |
| 27 | S18-W1-6 | S18 | learn-hub | surface-checklist.md | S13-W1-6 | no |
| 28 | S18-W1-7 | S18 | learn-hub | routing.md find-based glob | — | no |
| 29 | S18-W1-8 | S18 | learn-hub | pdf-pipeline description | — | no |
| 30 | S18-W1-9 | S18 | learn-hub | pdf-pipeline evals | S18-W1-1…8, S18-W0-1 | no |
| 31 | S19-W1-1 | S19 | learn-hub | One topic-id rule (H21) | — | no |
| 32 | S19-W1-2 | S19 | learn-hub | Sync economics (H22) | S13-W1-6 | no |
| 33 | S19-W1-3 | S19 | learn-hub | Four drafting rules (H23) | — | no |
| 34 | S19-W1-4 | S19 | learn-hub | Id resolution, glob, check-mermaid; package.json | S13-W1-5 | no |
| 35 | S19-W1-5 | S19 | learn-hub | Scale guidance | — | no |
| 36 | S19-W1-6 | S19 | learn-hub | check-manifest pointer | — | no |
| 37 | S19-W1-7 | S19 | learn-hub | ready.mjs preflight | S13-W1-2 | no |
| 38 | S19-W1-8 | S19 | learn-hub | Description + stale counts | — | no |
| 39 | S16-W1-1 | S16 | learn-hub | ingest-infographic YAML, H30, route | S13-W1-6 | no |
| 40 | S16-W1-2 | S16 | learn-hub | ingest-animation YAML | — | no |
| 41 | S05-W1-1 | S05 | learn-hub | learn-hub CA copy YAML (H43) | — | no |
| 42 | S20-W1-1 | S20 | learn-hub | vault-coverage `BOOK_ROOT`, map, stale text | — | no |
| 43 | S20-W1-1b | S20 | learn-hub | Backfill coverage-sources.json | S20-W1-1 | yes |
| 44 | S14-W1-1 | S14 | learn-hub | Audit source-to-vault writes | — | yes |
| 45 | S14-W1-2 | S14 | learn-hub | Delete source-to-vault (H17–H20) | S14-W1-1 | no |
| 46 | S21-W1-1 | S21 | learn-hub | CLAUDE.md figure dispositions | — | no |
| 47 | S21-W1-4 | S21 | learn-hub | CLAUDE.md sync-vault owner sentence (+ CX-49 item 3) | S13-W1-6 | no |
| 48 | S13-W1-10 | S13 | learn-hub | Live sync of a trivial edit; diagrams count | S13-W1-1…9, S11-W0-11 | yes |
| 49 | S07-W1-1 | S07 | micky | sink.py + .vault-id; manifest (MIT) | S10-W0-8 | no |
| 50 | S07-W1-2 | S07 | micky | empty-vault stopgap | S07-W1-1 | no |
| 51 | S07-W1-3 (new, CX-5) | S07 | micky | vault-keeper Step 0 + vault-layout.md use sink.py (H08, H09) | S07-W1-1 | no |
| 52 | S07-W1-4 (new, CX-13) | S07 | micky | Release vault-keeper | S07-W1-2, S07-W1-3, S10-W0-2 | no |
| 53 | S08-W1-1 | S08 | micky | plugin-creator guard, no walk-up (H07) | — | no |
| 54 | S08-W1-2 | S08 | micky | Release plugin-creator (`--write`) | S08-W1-1, S10-W0-2 | no |
| 55 | S04-W1-1 | S04 | micky | PPD edat, retstart, CT.gov RANGE, UTC+7, MCP resolution (H46, H47) | — | no |
| 56 | S04-W1-2 | S04 | micky | PPD README cron claim | — | no |
| 57 | S04-W1-3 (new, CX-13) | S04 | micky | Release psych-paper-digest | S04-W1-1, S04-W1-2, S10-W0-2 | no |
| 58 | S06-W1-1 | S06 | micky | CI light-lock, strip, contrast, 12px (H36, H37) | — | no |
| 59 | S06-W1-2 | S06 | micky | CE dead pointers (H42) | — | no |
| 60 | S06-W1-3 | S06 | micky | CI/CE evals (extend seeds) | S06-W0-1 | no |
| 61 | S06-W1-4 | S06 | micky | Validate | S06-W1-1, S06-W1-2 | no |
| 62 | S06-W1-5 (new, CX-13) | S06 | micky | Release CI, CE | S06-W1-4, S10-W0-2 | no |
| 63 | S09-W1-1 | S09 | micky | firecrawl refresh (H12) | — | no |
| 64 | S09-W1-2 | S09 | micky | Release firecrawl (`--write`) | S09-W1-1, S10-W0-2 | no |
| 65 | S11-W1-1 | S11 | env + micky | V1→V2: vault-keeper, firecrawl, plugin-creator | S07-W1-4, S08-W1-2, S09-W1-2, S07-W0-1, S08-W0-1, S09-W0-1, S11-W0-11 | yes |
| 66 | S11-W1-2 | S11 | Windows + micky | Refresh installs | S04-W1-3, S06-W1-5, S07-W1-4, S08-W1-2, S09-W1-2 | yes |
| 67 | S12-W1-T (new, CX-40) | S12 | both | Tag `wave-1` | all above | yes |

### W2 — reconnect the pipeline (consumers → producers)

| # | Step | Spec | Repo | Title | Depends on | OWNER |
|---|---|---|---|---|---|---|
| 1 | S15-W2-1 | S15 | learn-hub | inbox-contract.md (I09, I10) | — | no |
| 2 | S15-W2-5 | S15 | learn-hub | report-parse.mjs + tests | — | no |
| 3 | S15-W2-2 | S15 | learn-hub | digest-report project skill (H15, H16) | S15-W2-1, S13-W1-6 | no |
| 4 | S15-W2-3 | S15 | learn-hub | Retire the digest-report plugin | S15-W2-2 | no |
| 5 | S15-W2-4 | S15 | learn-hub | Project-skill README | S15-W2-2 | no |
| 6 | S15-W2-6 | S15 | learn-hub | check-contract.mjs + tests (two default dirs, CX-7) | S15-W2-5 | no |
| 7 | S15-W2-7 | S15 | learn-hub | digest-report evals | S15-W2-2, S15-W2-5 | no |
| 8 | S15-W2-OWNER | S15 | learn-hub | Confirm Supabase project id (record in h-coverage) | S15-W2-2 | yes |
| 9 | S16-W2-1 | S16 | learn-hub | Static audit module + tests (inline fixtures, CX-31) | — | no |
| 10 | S16-W2-2 | S16 | learn-hub | audit:visual CLI + npm script (CX-25) | S16-W2-1, S19-W1-4 | no |
| 11 | S16-W2-3 | S16 | learn-hub | ingest-visual skill (audit before filing, CX-41) | S16-W2-2, S15-W2-1 | no |
| 12 | S16-W2-4 | S16 | learn-hub | Delete ingest-infographic, ingest-animation (H29, H31) | S16-W2-3 | no |
| 13 | S16-W2-5 | S16 | learn-hub | pk-plasma-animation skill + `pk-animation` alias skill | S16-W2-3 | no |
| 14 | S16-W2-6 | S16 | learn-hub | Retire the pk-plasma plugin | S16-W2-5 | no |
| 15 | S16-W2-7 | S16 | learn-hub | ingest-visual, pk-plasma evals | S16-W2-3, S16-W2-5 | no |
| 16 | S16-W2-OWNER | S16 | learn-hub | audit:visual with real Chromium (record in h-coverage) | S16-W2-2 | yes |
| 17 | S19-W2-1 (new, CX-29) | S19 | learn-hub | atomize-book:588-590 visuals handover | S16-W2-3 | no |
| 18 | S20-W2-1 | S20 | learn-hub | vault-atomizer → project skill, dmi | S13-W1-6 | no |
| 19 | S20-W2-2 | S20 | learn-hub | vault-vectors → project skill + `/vectors` alias | — | no |
| 20 | S20-W2-3 | S20 | learn-hub | vault-coverage dmi | S20-W1-1 | no |
| 21 | S20-W2-4 | S20 | learn-hub | check-repetition Not-for, dmi | — | no |
| 22 | S14-W2-1 | S14 | learn-hub | plugins/learn-hub-session (I15) | S13-W1-8, S11-W0-7 | no |
| 23 | S01-W2-1 | S01 | micky | Interim lock-record.md (I01) | — | no |
| 24 | S01-W2-2 (new, CX-13) | S01 | micky | Release intent-lock | S01-W2-1 | no |
| 25 | S02-W2-1 | S02 | micky | DI/PC OPTIONAL intent-lock handoff | S01-W2-1 | no |
| 26 | S02-W2-2 (new, CX-13) | S02 | micky | Release DI, PC | S02-W2-1 | no |
| 27 | S03-W2-1 | S03 | micky | pubmed: Assumed line, fallback, sink, report/1 (H44) | S01-W2-1, S15-W2-2 | no |
| 28 | S03-W2-2 | S03 | micky | tool-catalog runtime MCP resolution | S03-W2-1 | no |
| 29 | S03-W2-3 | S03 | micky | intent-lock-pairing: no Reframed | S03-W2-1 | no |
| 30 | S03-W2-4 (new, CX-7) | S03 | micky | Interim report-contract.md + fixtures | S03-W2-1 | no |
| 31 | S03-W2-5 (new, CX-13) | S03 | micky | Release pubmed | S03-W2-1…4 | no |
| 32 | S04-W2-1 | S04 | micky | CR fallback, sink, Not-for, MCP resolution (CX-6) | S01-W2-1, S15-W2-2, S03-W2-4 | no |
| 33 | S04-W2-2 | S04 | micky | CR interim contract copy | S04-W2-1, S03-W2-4 | no |
| 34 | S04-W2-3 (new, CX-13) | S04 | micky | Release CR | S04-W2-2 | no |
| 35 | S05-W2-1 | S05 | micky | check-html.mjs + tests + parity fixture | — | no |
| 36 | S05-W2-2 | S05 | micky | Copy check-html into ML, CI | S05-W2-1 | no |
| 37 | S05-W2-3 | S05 | micky | CA grammar port, 5-frame verify, filing (H38, H39) | S05-W2-1, S16-W2-3 | no |
| 38 | S05-W2-4 | S05 | micky | ML port, verify, gradient check (H40, H41) | S05-W2-2, S16-W2-3 | no |
| 39 | S05-W2-5 | S05 | micky | CA/ML evals | S05-W2-3, S05-W2-4 | no |
| 40 | S05-W2-6 | S05 | micky | CA/ML README/CHANGELOG edit + release (`--write`) | S05-W2-3, S05-W2-4, S10-W0-8 | no |
| 41 | S06-W2-1 | S06 | micky | CI render/verify + filing | S05-W2-2, S16-W2-3 | no |
| 42 | S06-W2-2 (new, CX-13) | S06 | micky | Release CI | S06-W2-1 | no |
| 43 | S07-W2-1 | S07 | micky | Sink routes to inbox; `.meta.json` stored (CX-9) | S07-W1-3, S15-W2-1 | no |
| 44 | S07-W2-2 | S07 | micky | Job count, README, layout pointer | — | no |
| 45 | S07-W2-3 | S07 | micky | vault_index.py | S07-W2-1 | no |
| 46 | S07-W2-4 | S07 | micky | drain_plan.py; empty-vault transfer (H10, H11) | S07-W2-1, S07-W2-3, S15-W2-1 | no |
| 47 | S07-W2-5 | S07 | micky | Evals in I17 layout (CX-23) | S07-W2-1, S07-W2-4, S07-W0-1 | no |
| 48 | S07-W2-6 (new, CX-13) | S07 | micky | Release vault-keeper | S07-W2-1…5 | no |
| 49 | S14-W2-2 | S14 | micky | Confirm/merge fork ledger (H06) | — | no |
| 50 | S14-W2-3 | S14 | learn-hub | Delete intent-lock fork | S14-W2-2 | no |
| 51 | S14-W2-4 | S14 | learn-hub | Delete pubmed and CR forks (H48, H49) | S07-W2-1, S03-W2-1, S04-W2-1 | no |
| 52 | S11-W2-1 | S11 | Windows + micky | Remove learn-hub-local (if found) | — | yes |
| 53 | S14-W2-5 | S14 | learn-hub | Delete learn-hub-local catalog (H14) | S11-W2-1, S14-W1-2, S14-W2-3, S14-W2-4, S15-W2-3, S16-W2-6, S20-W2-1, S20-W2-2 | no |
| 54 | S11-W2-2 | S11 | env + micky | V2→V3: pubmed, CR, CI, ML, CE | S03-W2-5, S04-W2-3, S05-W2-6, S06-W2-2, S03-W0-1, S04-W0-2 | yes |
| 55 | S05-W2-8 | S05 | learn-hub | Push branch deleting the learn-hub CA copy | S05-W2-6, S16-W2-5 | no |
| 56 | S11-W2-3 | S11 | env + both | V3→V4: atomic swap; merge the branch | S05-W2-8, S11-W2-2 | yes |
| 57 | S11-W2-4 | S11 | env + micky | V4→V5: learn-hub/plugins folder | S11-W2-3, S14-W2-1, S14-W2-5 | yes |
| 58 | S07-W2-7 (new, CX-43) | S07 | both | Rehearsal + no-digest-without-word check | S07-W2-4, S15-W2-2, S14-W2-4, S11-W2-4 | yes |
| 59 | S04-W2-4 (new, CX-43) | S04 | cloud | One unattended daily-random-review run | S11-W2-2 | yes |
| 60 | S11-W2-5 | S11 | Windows + micky | Refresh installs | S01-W2-2, S02-W2-2, S03-W2-5, S04-W2-3, S05-W2-6, S06-W2-2, S07-W2-6 | yes |
| 61 | S12-W2-T (new, CX-40) | S12 | both | Tag `wave-2` | all above | yes |

### W3 — micky consolidation (skeleton first, alignment before evidence and visuals)

| # | Step | Spec | Repo | Title | Depends on | OWNER |
|---|---|---|---|---|---|---|
| 1 | S11-W3-1 | S11 | env + micky | V5→V6 folder paths; MEMORY:11 | W2 exit | yes |
| 2 | S11-W3-2 | S11 | Windows + micky | Windows switch (OD2-a) | S11-W3-1 | yes |
| 3 | S10-W3-1 | S10 | micky | marketplace.json W3 shape + renames (same commit as row 4) | S10-W0-3, S11-W3-1 | no |
| 4 | S10-W3-2 | S10 | micky | Skeleton: moves, plugin-root dirs, family manifests, aliases, examples (CX-1, 2, 3, 32) | S10-W3-1 | no |
| 5 | S11-W3-5 | S11 | micky | Log: families load | S10-W3-2 | no |
| 6 | S11-W3-3 | S11 | micky | README install section | S11-W3-2 | no |
| 7 | S12-W3-2 | S12 | cloud | Live triggers BEFORE | S10-W3-2, S12-W0-6 | no |
| 8 | S01-W3-1 | S01 | micky | interview-protocol.md; lock-record names | S10-W3-2 | no |
| 9 | S01-W3-2 | S01 | micky | intent-lock by subtraction (H01, H02) | S01-W3-1, S12-W3-2 | no |
| 10 | S01-W3-3 | S01 | micky | misread-capture + ledger.py (H04) | S01-W3-1, S12-W3-2 | no |
| 11 | S01-W3-4 | S01 | micky | Reformat moved state/misreads.md (H03) | S01-W3-3, S14-W2-2 | no |
| 12 | S02-W3-1 | S02 | micky | DI/PC evals | S10-W3-2 | no |
| 13 | S02-W3-2 | S02 | micky | decision-interview rewrite | S01-W3-1, S12-W3-2 | no |
| 14 | S02-W3-3 | S02 | micky | plan-critique rewrite | S01-W3-1, S12-W3-2 | no |
| 15 | S01-W3-5 | S01 | micky | alignment plugin.json edit, README, CHANGELOG | S01-W3-2, S01-W3-3, S02-W3-2, S02-W3-3 | no |
| 16 | S02-W3-4 | S02 | micky | README sections DI/PC | S02-W3-2, S02-W3-3, S01-W3-5 | no |
| 17 | S01-W3-6 | S01 | micky | intent-lock/misread-capture evals | S01-W3-2, S01-W3-3 | no |
| 18 | S03-W3-1 | S03 | micky | report-contract.md, engines.md (edit moved files) | S10-W3-2, S01-W3-2 | no |
| 19 | S03-W3-2 | S03 | micky | Decision-brief 6 slots (H45) | S03-W3-1, S01-W3-2 | no |
| 20 | S03-W3-3 | S03 | micky | Dedupe depth contract | S03-W3-1 | no |
| 21 | S03-W3-4 | S03 | micky | pubmed description | S03-W3-1, S12-W3-2 | no |
| 22 | S03-W3-5 | S03 | micky | sources_lint.py (`test_sources_lint.py`), mocks, fixtures | S03-W3-1 | no |
| 23 | S03-W3-6 | S03 | micky | pubmed evals | S03-W3-1, S03-W3-5 | no |
| 24 | S04-W3-1 | S04 | micky | sweep.py (`test_sweep.py`), state/lit-watch | S10-W3-2 | no |
| 25 | S04-W3-2 | S04 | micky | CR remaining fixes | S10-W3-2, S03-W3-1, S01-W3-2 | no |
| 26 | S04-W3-3 | S04 | micky | CR + lit-watch descriptions, rename, lock re-key | S10-W3-2, S12-W3-2 | no |
| 27 | S04-W3-4 | S04 | micky | triage-rubric pointer | S10-W3-2 | no |
| 28 | S04-W3-5 | S04 | micky | CR evals | S04-W3-3 | no |
| 29 | S04-W3-6 | S04 | micky | lit-watch evals | S04-W3-1, S04-W3-3 | no |
| 30 | S03-W3-7 (new, CX-3) | S03 | micky | evidence README/CHANGELOG/LICENSE | S03-W3-6, S04-W3-6 | no |
| 31 | S05-W3-1 | S05 | micky | html-artifact-contract.md, render-verify.md; verify one check-html | S10-W3-2, S01-W3-2 | no |
| 32 | S05-W3-2 | S05 | micky | CA/ML descriptions + handoffs | S05-W3-1, S12-W3-2 | no |
| 33 | S05-W3-3 | S05 | micky | ML size trim | S05-W3-1 | no |
| 34 | S05-W3-4 | S05 | micky | visuals plugin.json edit | S05-W3-1 | no |
| 35 | S05-W3-5 (new, CX-3) | S05 | micky | visuals README/CHANGELOG/LICENSE | S05-W3-4 | no |
| 36 | S06-W3-1 | S06 | micky | lessons-learned → CHANGELOG; example README rename | S05-W3-5 | no |
| 37 | S06-W3-2 | S06 | micky | CI/CE descriptions + handoffs | S06-W3-1, S12-W3-2, S01-W3-2 | no |
| 38 | S06-W3-3 | S06 | micky | CE fidelity; implement `--source` (CX-33) | S06-W3-2, S05-W3-1 | no |
| 39 | S06-W3-4 | S06 | micky | Verify alias skills | S10-W3-2 | no |
| 40 | S08-W3-1 | S08 | micky | Self-contained validate/release; health.sh; lists (CX-11, CX-21) | S10-W3-2, S08-W1-2, S10-W0-2, S11-W0-3 | no |
| 41 | S08-W3-2 | S08 | micky | plugin-creator SKILL.md | S08-W3-1, S12-W3-2 | no |
| 42 | S08-W3-3 | S08 | micky | refine-plugin + new-plugin alias | S08-W3-1, S12-W3-2 | no |
| 43 | S08-W3-4 | S08 | micky | Scaffold writes README/CHANGELOG/LICENSE/evals | S08-W3-2 | no |
| 44 | S08-W3-5 | S08 | micky | Templates (quoted placeholders) | S08-W3-1 | no |
| 45 | S08-W3-6 | S08 | micky | MCP wiring in scaffold | S08-W3-5 | no |
| 46 | S08-W3-7 | S08 | micky | Delete plugin-creator commands only | S08-W3-2, S08-W3-3 | no |
| 47 | S08-W3-8 | S08 | micky | plugin-creator evals | S08-W3-2, S08-W3-3, S08-W0-1 | no |
| 48 | S08-W3-9 | S08 | micky | Release plugin-creator | S08-W3-1…8 | no |
| 49 | S09-W3-1 | S09 | micky | firecrawl router split | S09-W1-2, S08-W3-1, S10-W3-2, S12-W3-2 | no |
| 50 | S09-W3-2 | S09 | micky | gridgeist metadata (edit W0 files) | S10-W3-2, S10-W0-8 | no |
| 51 | S09-W3-3 | S09 | micky | firecrawl, gridgeist evals | S09-W3-1, S09-W3-2, S09-W0-1 | no |
| 52 | S09-W3-4 | S09 | micky | Release firecrawl, gridgeist | S09-W3-1…3, S08-W3-1 | no |
| 53 | S11-W3-4 | S11 | env + micky | firecrawl enablement (owner answer, CX-51) | S09-W3-1 | yes |
| 54 | S07-W3-1 | S07 | micky | Delete empty-vault command | S07-W1-2, S10-W3-2 | no |
| 55 | S01-W3-7 (new, CX-3) | S01 | micky | Release alignment (`release.py`) | S01-W3-6, S02-W3-4, S08-W3-1 | no |
| 56 | S03-W3-8 (new, CX-3) | S03 | micky | Release evidence | S03-W3-7, S08-W3-1 | no |
| 57 | S05-W3-6 (new, CX-3) | S05 | micky | Release visuals | S05-W3-5, S06-W3-4, S08-W3-1 | no |
| 58 | S12-W3-3 | S12 | cloud | Live triggers AFTER | rows 9, 10, 13, 14, 21, 26, 32, 37, 41, 42, 49 | no |
| 59 | S10-W3-8 | S10 | micky | CLAUDE.md ≤5 KB (+ S11 item 2) | S01-W3-6, S02-W3-4, S03-W3-7, S04-W3-6, S05-W3-5, S06-W3-4, S07-W3-1, S08-W3-9, S09-W3-4 | no |
| 60 | S10-W3-9 | S10 | micky | Delete ROUTING.md, route.py | S10-W3-8, S08-W3-7 | no |
| 61 | S10-W3-10 | S10 | micky | MEMORY split | S10-W3-8, S11-W3-1 | no |
| 62 | S10-W3-11 | S10 | micky | Archive the superseded plan | — | no |
| 63 | S12-W3-1 | S12 | micky | No evals.json remains | S01-W3-6, S02-W3-1, S03-W3-6, S04-W3-5, S04-W3-6, S05-W2-5, S06-W1-3, S07-W2-5, S08-W3-8, S09-W3-3 | no |
| 64 | S12-W3-4 | S12 | both | Routing smoke (≥17/20, 0 destructive) | S12-W3-3, S11-W3-5 | no |
| 65 | S12-W3-5 | S12 | micky | Release eval run per family | S12-W3-1…4 | no |
| 66 | S12-W3-T (new, CX-40) | S12 | both | Tag `wave-3` | all above | yes |

### W4 — learn-hub consolidation (freeze window for atomize-book)

| # | Step | Spec | Repo | Title | Depends on | OWNER |
|---|---|---|---|---|---|---|
| 1 | S19-W4-1 | S19 | learn-hub | Freeze atomize-book imports (record in CHANGELOG) | W2 exit | yes |
| 2 | S12-W4-2 (new, CX-37) | S12 | cloud | Live triggers BEFORE (PDF, atomize families) | S12-W0-6 | no |
| 3 | S21-W4a-1 | S21 | learn-hub | gotcha-map.md (136 of 136) | — | no |
| 4 | S21-W4a-3 | S21 | learn-hub | gotchas-archive.md first; pk-plasma line | S21-W4a-1, S16-W2-6 | no |
| 5 | S21-W4a-2 | S21 | learn-hub | vault-format.md; 6 skills' gotchas | S21-W4a-3 | no |
| 6 | S13-W4-1 | S13 | learn-hub | sync-vault gotchas: move + delete | S21-W4a-2 | no |
| 7 | S19-W4-8 | S19 | learn-hub | atomize-book gotchas: move + delete | S21-W4a-2, S19-W4-1 | no |
| 8 | S21-W4b-1 | S21 | learn-hub | App gotchas + Pages → .claude/rules | S21-W4a-2, S13-W4-1, S19-W4-8 | no |
| 9 | S19-W4-2 | S19 | learn-hub | references/extract.md | S19-W4-1, S19-W1-1…8 | no |
| 10 | S19-W4-3 | S19 | learn-hub | references/figures.md | S19-W4-2 | no |
| 11 | S19-W4-4 | S19 | learn-hub | references/measure.md | S19-W4-3 | no |
| 12 | S19-W4-5 | S19 | learn-hub | references/qc.md | S19-W4-4 | no |
| 13 | S19-W4-6 | S19 | learn-hub | references/traps.md | S19-W4-5 | no |
| 14 | S19-W4-7 | S19 | learn-hub | Final SKILL.md pass (H24) | S19-W4-2…6 | no |
| 15 | S19-W4-9 | S19 | learn-hub | Exit: one chapter re-run, 354 tests | S19-W4-7, S19-W4-8 | no |
| 16 | S17-W4-1 | S17 | learn-hub | ingest-article conditional references | S17-W1-2, S21-W4a-2 | no |
| 17 | S17-W4-2 | S17 | learn-hub | Measure | S17-W4-1 | no |
| 18 | S17-W4-3 | S17 | learn-hub | 4 more cases | S17-W1-12, S12-W0-4 | no |
| 19 | S18-W4-2 | S18 | learn-hub | verify SKILL.md | — | no |
| 20 | S18-W4-3 | S18 | learn-hub | verify scripts (lib + tests under scripts/lib, CX-26) | S18-W4-2 | no |
| 21 | S18-W4-1 | S18 | learn-hub | classify_pdf.py (I26) | S18-W1-1, S18-W1-2 | no |
| 22 | S18-W4-4 | S18 | learn-hub | verify + pdf-pipeline cases | S18-W1-9, S12-W0-4 | no |
| 23 | S17-W4-4 | S17 | learn-hub | Hand queries to S12 | S17-W1-2, S17-W1-8, S18-W4-1 | no |
| 24 | S18-W4-5 | S18 | learn-hub | Hand queries to S12 | S18-W1-8, S17-W4-4 | no |
| 25 | S12-W4-3 (new, CX-37) | S12 | cloud | Live triggers AFTER | S17-W4-4, S18-W4-5 | no |
| 26 | S12-W4-1 | S12 | learn-hub | Project-skill smoke | S13-W1-9, S17-W4-3, S18-W4-4, S19-W4-9 | no |
| 27 | S12-W4-T (new, CX-40) | S12 | learn-hub | Tag `wave-4`; end the freeze | all above | yes |

### W5 — hardening and deferred decisions

| # | Step | Spec | Repo | Title | Depends on | OWNER |
|---|---|---|---|---|---|---|
| 1 | S12-W5-1 | S12 | both | Full release pass | W3 exit, W4 exit | no |
| 2 | S12-W5-2 | S12 | both | Routing smoke with everything loaded | S12-W5-1 | no |
| 3 | S09-W5-1 | S09 | micky | gridgeist usage decision (CHANGELOG) | 2–4 weeks after W3 | yes |
| 4 | S10-W5-1 | S10 | micky | MEMORY final numbers | W3 exit, W4 exit | no |
| 5 | S11-W5-1 | S11 | micky | Close the delivery record | W3 exit, W4 exit, S09-W5-1 | no |

---

## 3. Checks that passed

- Every HIGH defect H01–H49 has a fix step in its Appendix A wave (`coverage.md`); the two exceptions in substance are H08/H09 (CX-5) and the wrong step ids in CX-60.
- I27 (`ARTICLE_INBOX_DIR`, `BOOK_ROOT`) agrees across S11, S17, S20, including the `.gitignore` line.
- I14 (session-start root, done-marker, ready line) agrees between S13 and S14.
- I02 (interview protocol) agrees between S01 and S02, including the 4-question cap and `Decided without you:`.
- I06 (lit-watch state) has one definition (S04); S10 only creates the folder (CX-62).
- I26 has one owner (S18); S17 does not call it.
- The `CLAUDE_CODE_PLUGIN_DIRS` schedule (S11 I16.2) matches architecture §2.7 point by point; with the depends added in section 2, each addition follows the fixes and smoke suites it needs, apart from the recorded exceptions in CX-50.
