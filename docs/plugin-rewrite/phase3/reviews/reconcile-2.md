# Reconciliation log — specs S11–S21

Scope: S11 (delivery-environment), S12 (eval-program), S13 (sync-tail), S14
(learn-hub-retirements), S15 (digest-report-inbox), S16 (ingest-visual-pk-plasma), S17
(ingest-article-slides), S18 (pdf-pipeline-verify), S19 (atomize-book), S20
(maintenance-skills), S21 (learn-hub-claude-md-infra).

Inputs applied: `phaseB/cx.md` (findings CX-1..CX-62), `phaseB/factcheck.md` (F1-F3 and
per-spec items). Every finding below names at least one of S11–S21 in its "Specs" column
and was applied here. Mechanical fixes (full step ids in §1.3 and depends-on lines; size
check) were also applied to all eleven specs, listed once at the end.

Format: finding id → spec → what changed.

## CX-4 — no W0 smoke seeds

- S11: S11-W1-1 and S11-W2-2 depends-on rewritten to name the new W0 smoke-seed steps
  (S07-W0-1/S08-W0-1/S09-W0-1 and S03-W0-1/S04-W0-2) plus the release steps they gate.
- S12: §2.6 rewritten from a 7-unit table to the full 10-unit smoke-seed table (adds
  pubmed-research-note, plugin-creator, firecrawl); S12-W0-5 depends-on lists all 10 new
  step ids; acceptance criterion 11 updated to "10 skills."
- S13: new step S13-W0-1 (3 smoke cases, depends S12-W0-4); S13-W1-9 now depends on it too.
- S17: new step S17-W0-1 (3 smoke cases, depends S12-W0-4); S17-W1-12 now depends on it too.
- S18: new step S18-W0-1 (3 smoke cases, depends S12-W0-4); S18-W1-9 now depends on it too.

## CX-5 — H08/H09 do not really close in W1

- S11: S11-W1-1 depends-on adds S07-W1-3 explicitly (alongside the release steps that
  already transitively depend on it).

## CX-6 — CR/psych-paper-digest keep hard-coded MCP prefixes

- S11: S11-W2-2 depends-on adds S04-W2-1.

## CX-7 — I04 report-contract has no W2 text

- S15: `check-contract.mjs` default-dir logic changed from a single fixed path to "first of
  `plugins/evidence/evals/fixtures` (post-W3) or `plugins/pubmed-research-note/evals/fixtures`
  (pre-W3, written by S03-W2-4) that exists"; §2.5 table, I04 consumed-interface row, S15-W2-6
  description, and acceptance criterion 6 all updated to match.

## CX-9 — asset kind stored twice (S07's fix; checked, no S15/S16 edit needed)

- S15/S16: confirmed neither text mentions a `.kind` sidecar; no change required.

## CX-10 — audit verdicts; code-explainer own-port

- S15: `.meta.json` `audit.verdict` changed from `"pass"|"fail"` to `"pass"|"incomplete"`
  (a producer never files `"fail"`); `producer` field clarified as the `plugin:skill` name
  at write time.
- S16: I08's rule-id paragraph and the implementation-mapping table's first row both marked
  `no-reduced-motion`/`external-reference` as "anim/explorable only through this CLI —
  code-explainer's own copy of the rule runs through S06's own port, never `--kind
  code-explainer`."

## CX-13 — missing releases

- S11: S11-W1-2 and S11-W2-5 depends-on rewritten to the exact new release-step ids
  (S04-W1-3, S06-W1-5, S07-W1-4, S08-W1-2, S09-W1-2; S01-W2-2, S02-W2-2, S03-W2-5, S04-W2-3,
  S05-W2-6, S06-W2-2, S07-W2-6).

## CX-16 — I01 bare vs. `alignment:` name

- S16: pk-plasma-animation's intent-lock handoff sentence changed from `alignment:intent-lock`
  to the bare `intent-lock` (a learn-hub skill has no W3 rename step, so the bare name
  resolves both before and after S01's rename); the §2.3 body-outline row for Step 0 updated
  the same way.

## CX-17 — I13 handoff has seven forms

- S13 (owner of I13): §2.6 rewritten to the one sentence — "Publish through the `sync-vault`
  skill (same repo, always present). Follow its steps as written; do not restate them here."
  — carried into the I13 interface definition and the §8 open-question closure.
- S15, S16, S17, S18, S19, S20: every "Run sync-vault..."/"Run the sync-vault tail (I13)"
  restatement replaced with the same sentence verbatim, and every place that previously
  restated the preflight→apply→revalidate procedure had that restatement deleted (only each
  skill's own post-sync verification of its own artifact, which is not sync-vault's
  procedure, was kept). S19 and S20's versions additionally drop the restated OPTIONAL
  fallback the finding calls out by name.

## CX-19 — ratchet/trigger-lock schema and parsers

- S12: `ratchet.json` and `triggers.lock.json` both gain a `"schema": 1` field; §2.5 adds a
  paragraph stating both scripts are also importable libraries (not CLI-only), specifically so
  S08 and S21 can import instead of re-implementing; §8 item 1 closed.
- S21: skill-lint's check 9 rewritten to import `scripts/lib/rewrite-gate.mjs`'s exported
  functions rather than re-parsing the JSON files itself; I17 consumed-interface row and the
  matching §8 item closed to reflect this.

## CX-24 — `/pk-animation` must be a dmi alias skill, not a command file

- S16: replaced `.claude/commands/pk-animation.md` with `.claude/skills/pk-animation/SKILL.md`
  (I20's alias template) throughout — §2.1 tree, S16-W2-5's files/change/done-when/rollback,
  acceptance criterion 11, the trigger-lock table, and §8's open question (closed).

## CX-25 — `audit:visual` npm script has no step

- S16: S16-W2-2 now also edits `package.json` (adds the `audit:visual` line); §2.7 I22 row and
  §8 updated to record S16-W2-2 as the step, closed.

## CX-26 — verify's tests never run; wrong root-resolution depth

- S18: split `mint-session.mjs`/`probe.mjs` into thin CLI wrappers (stay under
  `.claude/skills/verify/scripts/`) plus pure logic + tests at repo-root `scripts/lib/
  verify-mint.mjs`/`verify-probe.mjs` (+ `.test.mjs`), which `vitest.config.ts` actually
  collects. Root resolution changed from a fixed relative-parent count (wrong depth for the
  wrapper's new location) to a walk-up to the learn-hub marker. §2.1, §2.5, S18-W4-3, and
  acceptance criterion 10 all updated.
- S21: `test:py` changed from a single fixed `atomize-book` path to a per-skill-dir walk
  (`for d in .claude/skills/*/scripts; do python3 -m unittest discover -s "$d" ...`), so it
  also reaches `pdf-pipeline/scripts/test_classify_pdf.py` (S18-W4-1); I22 table, S21-W0-2, and
  acceptance criterion 7 updated.

## CX-27 — delivery log misused for verification evidence

- S15: the OWNER Supabase-project-id verification step now records against H15/H16 in
  `docs/rewrite/h-coverage.md`, not `docs/rewrite/delivery-log.md`.
- S16: the OWNER Chromium-verification step now records against H29/H31 in
  `docs/rewrite/h-coverage.md`.
- S19: S19-W4-1's freeze-window record moved from `docs/rewrite/delivery-log.md` to the
  learn-hub `CHANGELOG.md`.

## CX-28 — I21 gotcha moves: archive-after-delete ordering; S21-W4b-1 missing deps

- S13: S13-W4-1 now moves AND deletes its assigned headings from CLAUDE.md in the same
  commit; depends-on set to S21-W4a-2.
- S19: S19-W4-8 does the same (move + delete in one commit); depends-on set to S21-W4a-2.
- S21: reordered W4 stage a so the archive (S21-W4a-3) runs immediately after the map
  (S21-W4a-1), BEFORE the first deletion (S21-W4a-2) — this also removes the "transient
  unrecoverable window" the spec's own §7 used to describe, since archiving before any
  deletion captures all 136 headings (including AB's/SV's) in one shot. S21-W4b-1's
  depends-on now explicitly names S13-W4-1 and S19-W4-8, not only S21-W4a-2.

## CX-29 — H-11 (atomize-book visuals handover) has no step

- S19: new step S19-W2-1 (depends S16-W2-3) rewrites `SKILL.md:588-590` to route visuals
  through the `research-notes/visuals/` inbox and `ingest-visual`, outside the W4 freeze.

## CX-31 — S16-W2-1's test depends on a cross-repo fixture; stale example path

- S16: S16-W2-1's test fixtures changed from a read of S05's parity-fixture file to inline
  HTML strings in the test file itself. S16-W2-2's and the OWNER step's example file changed
  from `.claude/skills/concept-animation/examples/…` (deleted later in the same wave by
  S05-W2-8) to the committed `vault/tms-principles/tms-electromagnetic-induction.html`.
  Acceptance criteria 4 and 5 updated to match.

## CX-34 — informal depends-on

- S11: S11-W0-3, W1-1, W1-2, W2-2, W2-3, W2-4, W2-5, W3-4, W3-5 all rewritten to full step
  ids; §8 items 10/11 closed with the resolved owners.
- S13: S13-W1-10 depends-on changed to S11-W0-11.
- S14: S14-W2-1 depends-on changed to S11-W0-7; S14-W2-5 depends-on gains S15-W2-3, S16-W2-6,
  S20-W2-1, S20-W2-2.
- S16: (via CX-38/CX-39, see below) — no separate CX-34 edit beyond what those cover.
- S17: S17-W1-3/-9 → +S13-W1-2; S17-W1-6/-11 → +S13-W1-6; S17-W4-1 → S21-W4a-2; S17-W4-3 →
  +S12-W0-4.
- S18: S18-W1-3 → S13-W1-2; S18-W1-4…-6 → +S13-W1-6; S18-W4-4 → +S12-W0-4.
- S19: S19-W1-2 → S13-W1-6; S19-W1-7 → S13-W1-2; S19-W4-8 → S21-W4a-2 (see CX-28).
- S21: S21-W4a-3 depends-on changed from "S16's W2 exit" to S16-W2-6.

## CX-37 — live trigger runs not ordered

- S12: S12-W3-2 depends-on gains S10-W3-2; S12-W3-3 depends-on rewritten to list every
  family's description-pass step; S12-W3-4 depends-on corrected to S11-W3-5; two new steps
  S12-W4-2 (BEFORE) and S12-W4-3 (AFTER) added for the PDF and atomize-book families' live
  triggers at W4.
- S17: S17-W4-4 depends-on gains S18-W4-1 (see CX-38, same edit).

## CX-38 — S17/S18 live-trigger cycle

- S17: S17-W4-4 depends-on narrowed from "S18-W4" (all of S18's W4 steps, which would cycle
  against S18-W4-5's own dependency on this step) to S18-W4-1 specifically.

## CX-39 — same-file, same/adjacent-wave, no order

- S13: S13-W1-5 depends-on gains S21-W0-2.
- S16: S16-W2-2 depends-on gains S19-W1-4 (package.json edit chain).
- S17: S17-W1-1 depends-on gains S13-W1-8 (.gitignore edit chain).
- S19: S19-W1-4 depends-on gains S13-W1-5 (package.json edit chain).

## CX-40 — no pre-rewrite/wave-N tags; no baseline.md W0 section

- S12: seven new steps added — S12-W0-0 (tag `pre-rewrite`, first W0 step), S12-W0-7
  (`baseline.md` W0 section), and one tag step per wave exit (S12-W0-T, S12-W1-T, S12-W2-T,
  S12-W3-T, S12-W4-T); acceptance criteria 12/13 added.

## CX-41 — ingest-visual files before it audits

- S16: §2.3's body-outline table reordered so Step 2 is the `audit:visual` refuse-and-return
  check and Step 3 is the file write (was the reverse); the refuse branch now explicitly
  writes the `refused` I10 line and writes nothing into `/vault`.

## CX-43 — W2 exit checks have no owner (S07/S04 new steps referencing S11/S15)

- S11: no direct edit needed — S07-W2-7 and S04-W2-4 (owned by S07/S04) depend on
  S11-W2-4/S11-W2-2 and S15-W2-2, which already existed under those ids.

## CX-46 — runner call shapes; `--allow-tools` gap (F3)

- S12: `eval.sh` and `eval-project-skill.sh` CLIs gain an args-passthrough after `--`
  (resolving F3 for the specs this task covers); `eval-project-skill.sh` also gains explicit
  `--smoke`/`--release` flags with the same pinned models as `eval.sh`; §8 gains an
  OWNER-QUESTION recording this as the chosen resolution of F3.
- S13, S15, S16, S17, S18: every `--tag smoke --ablation none --runs 1` / `--tag release
  --runs 3 --threshold 0.8` call rewritten to the new `--smoke`/`--release` flags.

## CX-49 — S11 §2.6 sentences not carried

- S11: §2.6 items 2 and 3 updated to name their real owners (S10-W3-8; S21-W1-4) instead of
  open questions; §8 items 10/11 closed.
- S21: S21-W1-4 now also adds S11's exact item-3 sentence ("Delivery and VM-tooling
  variables...") to learn-hub CLAUDE.md, verbatim; acceptance criterion 10 extended to check
  it.

## CX-50 — I16.3 exceptions are silent

- S11: S11-W2-2 and S11-W3-1 now record the pubmed-research-note (H45-open) and the four
  W3-entry plugins (no smoke suite yet) as named exceptions in the log's evidence cell; §8
  item 4 (ARCH-CONFLICT 4) marked OWNER-QUESTION and updated to reference this.

## CX-51 — firecrawl `defaultEnabled: false` owner question never asked

- S11: S11-W3-4 rewritten to ask the owner explicitly (keep or drop the flag) as its own
  first action, not only in §8; §8 item 1 marked OWNER-QUESTION explicitly.

## CX-52 — skill-lint check 7 over-warns on every user-only dmi skill

- S21: check 7 scoped to alias skills only (a single `Invoke ... with: $ARGUMENTS` body line),
  not every dmi skill — so `vault-atomizer`/`vault-vectors`/`vault-coverage`/
  `check-repetition`/`pk-plasma-animation` no longer trip it.

## CX-53 — no eval pattern for dmi skills

- S12: I17 gains a rule — a dmi skill's positive case is an explicit `/<name>` prompt; negatives
  stay natural-language near-misses.
- S20: all four `explicit-invocation` case prompts (vault-atomizer, vault-vectors,
  vault-coverage, check-repetition) rewritten to the `/<name>` slash form; the §4.1 intro
  paragraph and the two open-question/interface entries updated to point at S12's rule instead
  of treating it as unresolved.

## CX-55 — placeholder steps with no commit

- S16: S16-W1-3 (no files, no commit) removed; its content folded into a §8 note.
- S21: S21-W1-2 and S21-W1-3 (both no-file verification-only) removed; their content folded
  into a §8 note; S21-W4a-3's reference to "deferred from S21-W1-3" updated to point at the §8
  note instead.

## CX-58 — I15 details (hooks form, LICENSE, author)

- S14: `learn-hub-session`'s file list extended to six files including `LICENSE`; author
  changed from "Thanawat Suharit" to "Thanawat Suharit (Micky)"; the hooks.json exec-form
  citation now names S11-W0-7's probe as the confirming evidence.

## CX-59 — S14 §2.1 tree comment names wrong specs

- S14: comment corrected — conversions are S20 (vault-atomizer, vault-vectors), S16
  (pk-plasma-animation), S15 (digest-report), not "S15/S19/S20/S06."

## CX-60 — wrong fix-step ids for H16/H29/H31

- S15: digest-report-2 (H16) row already names S15-W2-1/-2/-3 (the closure steps), confirmed
  correct — no further edit needed once the mechanical fix (below) expanded the shorthand.
- S16: ingest-infographic-1 (H29) and ingest-animation-1 (H31) rows corrected from
  "S16-W2-2" alone to "S16-W2-3, S16-W2-4" (the steps that actually close them).

## CX-61 — `docs/cloud-env-setup.md:144` still says `npm run sync`

- S13: new step S13-W1-11 replaces the `npm run sync` recommendation with `npm run
  sync:preflight`.

## F2 (factcheck.md) — "21 codes total" vs. a list that sums to 26

- S16: I08's rule-id paragraph and the "26 codes total" arithmetic reproduced explicitly;
  the implementation-mapping table's per-tier counts annotated.

## Factcheck.md size/line/byte corrections

- S13: `.claude/settings.json` row corrected from 24 to 31 lines.
- S14: fork `misreads.md` row corrected from "45 | ~1,850 | ~460" to "47 | 2,446 | ~606".
- S15: `plugin.json` row corrected from 632 to 516 bytes; `README.md` row corrected from
  1,777 to 2,361 bytes.
- S16: "21 codes total" corrected to "26 codes total" (same fix as F2 above).
- S18: `verify/SKILL.md` row corrected from 60 to 64 lines.

## Mechanical fixes (applied to all eleven specs)

- §1.3 defect tables: every "fix"/"fix step" cell now names full step ids (`Sxx-W<n>-<k>`).
  S17 and S18 had a template deviation (a prose "fix" column with no step ids at all,
  paired with a separate "wave" column) — both rewritten to a "fix step (fix)" column
  carrying the real step id plus the original prose in parentheses. S14, S16, S19 had a few
  shorthand ranges (`S16-W2-2/3`, `S14-W2-2/-4`, `S19-W4-2..7`) expanded to full comma-separated
  id lists.
- §3 depends-on lines: every informal reference ("S13-W1" instead of "S13-W1-6", "the S10 W0
  step that creates scripts/health.sh", "S21's gotcha-map.md step", "S12-W0 (I17 layout)",
  etc.) replaced with the exact step id. Applied across all eleven specs; see the CX-34/
  CX-39 entries above for the ones driven by a named finding, plus a handful of others found
  during the pass itself (e.g. S11-W3-1's Windows-switch dependency was already a full id and
  needed no change).
- Size: all eleven specs are at or slightly over 40 KB after these edits (S11 the largest at
  ~87 KB, unchanged in scale from before — its size is the W0 probe/checklist/rollback
  procedure text, which is required content). None were trimmed, since every addition was a
  finding-driven fix and removing it would drop required content, per the task's own allowance.

## Findings named in cx.md/factcheck.md that touch S11–S21 only as context, not as an edit

These were checked against my specs and needed no change, confirmed during the pass:

- CX-9 (S15, S16 — checked, no `.kind` sidecar language present).
- CX-43 (S11 — S07/S04 add new steps that depend on existing S11/S15 step ids; no S11 edit
  required).
- CX-35, CX-36 (name S07 among others but the fix cells for those rows belong to S03/S04/
  S05/S06/S07/S08/S09, outside this job's scope).
