# Quality pass — pubmed-research-note + clinical-infographic (high findings only)

Owner scope (2026-09-26): two plugins, high-severity findings only, one plan, one critique
pass, then implement. Evidence for every finding: [findings.md](findings.md). Everything
else found in the diagnostic waits in [deferred-findings.md](deferred-findings.md).

Standing owner decisions: bump per CLAUDE.md (`bump.py … minor --write`, MEMORY.md);
do not edit any skill `description`; keep the report's machine-read shape byte-compatible
(dated count line, `> Assumed/Reframed/Skipped` preface, `## Sources` line grammar — new
rigor goes in prose or inside a Sources topic phrase); the banner literal
`CRITICAL SAFETY — MEDICATIONS` stays. Rewrite-plan steps that are pure fixes to files this
pass edits are done now and recorded as "done ahead of wave".

## What the diagnostic measured (why these fixes)

- pubmed-research-note: 3 live reports, 131–133 claims each, 92–95% verified. Errors cluster
  in the verdict and adjudication (20.6% vs 4.0% elsewhere). An abstract hid a null result
  the full text had. The first label found was a 2009 label missing a 2025 warning. The
  skill's own model sentence has a wrong number (3.2 vs published 0.2). No grader catches a
  misquote or a missing verdict.
- clinical-infographic: 2 probes passed a 100% number trace but still altered 6 and 11
  claims (qualifiers, arm labels, "trial" → "RCT"). CSS turns `µg` into `ΜG`. The
  "single-sheet" example prints on 3 A4 pages. The safety banner is triggered by the word
  "avoid", so real harms are missed and "no benefit" items land under CRITICAL SAFETY. Every
  file grader uses a glob path the harness reads literally, so they always fail.

## Changes

### pubmed-research-note (1.7.0 → 1.8.0)

New file `skills/pubmed-research-note/references/evidence-checks.md` holds the method; the
SKILL.md body gets short pointers only (body stays near its current size; S03 caps it at
4,000 tok at W3).

| # | Finding | Change | Files |
|---|---|---|---|
| P1 | PR-07 | Replace the model sentence with the verified one: CAPS item B2 (0–8), between-group difference 0.2, 95% CI −0.3 to 0.8, n=304 RCT (PubMed record of the NEJM 2018 trial, checked this pass). Rule: any number in an example must be checkable. | SKILL.md, report-craft.md |
| P2 | PR-02 | **Provenance.** Every number comes from a record opened this run. Full text is required for each load-bearing study when PMC/open access has it; else the same sentence says `abstract only`. Other tags in the sentence: `registry results, unpublished`, `as reported in <the meta-analysis>`, `calculated`, `my inference:`. Mechanism prose is exempt from the "no number" tell. | evidence-checks.md §1; tool-catalog.md (full text line); SKILL.md drift tell |
| P3 | PR-09 | **Appraisal.** One-line risk-of-bias judgement per load-bearing study with the tool named by design (RoB 2 / ROBINS-I / AMSTAR 2 + overlap / MR instrument strength); for a load-bearing meta-analysis: heterogeneity (I², prediction interval), small-study check or "not assessable", subgroup credibility before a subgroup becomes a rule. Inline floor gains "risk of bias, replication". | evidence-checks.md §2; SKILL.md inline floor |
| P4 | PR-05 | **Counter-evidence search against the provisional verdict**, not always the null direction (positive terms when the verdict is null). Plus a recency sweep for newer reviews. The report names the strongest opposing study and one line on why it loses. | evidence-checks.md §3; tool-catalog.md; decision-brief.md |
| P5 | PR-03, PR-52 | **Dose and safety step** whenever the verdict names a dose or endorses an agent: open an official label this run; name country/regulator, label revision date, on/off-label. Route: Thai FDA (firecrawl search `site:fda.moph.go.th`), DailyMed/openFDA, EMA SmPC; say in the sentence which was not checked. Off-label doses tie to the trial arm that tested them. A marked safety block (contraindications, boxed warnings, key interactions, monitoring, pregnancy) — each item sourced, or "not assessed". Sources topic phrase carries `(<regulator> label, revised YYYY-MM)`. | evidence-checks.md §4; tool-catalog.md (firecrawl row, web Sources line); SKILL.md pointer |
| P6 | PR-08 | **Confidence by GRADE domains.** Scale becomes high / moderate / low / very low (GRADE; `moderate-low` retired — no consumer parses it). Rate the decision-driving outcome; "not higher because <domain>" names the downgrade; small certainty table when outcomes differ. Indirectness applies the same way to evidence for and against. New drift tell: confidence higher than the evidence allows. | evidence-checks.md §5; SKILL.md :53; report-craft.md; decision-brief.md indirectness line |
| P7 | PR-01 | **Claim check between Write and Show**: a ledger over the verdict, adjudication, headings, summary sentences and every number; re-open the source passage; fix or mark `[unverified]`; prefer an independent subagent. Close adds "claim check: N checked, N fixed". | evidence-checks.md §6; SKILL.md "Where output goes" + Close |
| P8 | PR-10 + CI-08 | Output case `output-sources-contract`: prompt names the file (`esketamine-trd.md`); every file grader uses that literal path; dated line graded on the file; citation regex also catches `[n]`, narrative "X et al. (2019)" and multi-source; new graders: marked verdict + confidence word, CT.gov search called, `abstract only` tag present (the case mocks no full-text tool), the load-bearing CIs carried (7.31/0.64; 0.29/0.84). | evals/pubmed-research-note/output-sources-contract/ |

### clinical-infographic (0.2.1 → 0.3.0)

| # | Finding | Change | Files |
|---|---|---|---|
| C1 | S06-W1-1 (H36/H37), CI-05 | Remove dark-mode block; `:root{color-scheme:light}`; `--c2:#3b8368`, `--c3:#aa6527`; every font-size ≥12px. Every breakpoint becomes `@media screen and (…)` (the `.mech` stacking rule goes inside it); `@page{size:A4;margin:10mm}`; `break-inside:avoid` on cards/tiles/banner, not whole columns. Re-measure the example's printed pages; README states the real count. | template, example, examples/README.md, design-system.md |
| C2 | CI-04 | Remove `text-transform` from `.stat .k` and `.opt .cond`. Rule: CSS never changes the case of text holding a number, unit or drug name; units go in the value line; write `mcg`, not `µg`. | template, example, design-system.md |
| C3 | CI-02, PR-52 | Banner defined by clinical class in source-contract.md: 🚫 source-stated contraindication/boxed warning; ⚠ warning/precaution; monitoring. Harvest from harms, special-population and "verdict inverts" sections and label warnings, not only "avoid" words. Futility ("no benefit") → a neutral "Not recommended — no benefit shown" panel; practice directives → a rule callout; never upgrade a judgement to a prohibition; each cell's "why" is the source's own reason. Literal header stays when ≥1 harm item. Source with no safety content → a visible coverage line, never silent omission. Handoff "brevity welcome" becomes a render brief (keep full depth; carry a safety block). | source-contract.md, SKILL.md (banner + Step 1), design-system.md |
| C4 | CI-01 | New **Step 2.6 fidelity check**, re-run after every layout fix: `scripts/verify-infographic.mjs` (static: every number/unit token in visible text is in the source; design labels such as RCT / meta-analysis / Cochrane not more frequent than in the source; template leaks `{{` / `-->`; `--render` when Playwright resolves: A4 PDF page count, text-case mutation, external requests). Then a claim ledger for qualifiers (population, arm, significance, design, "only/unless/not"), altered-strengthened or untraceable units block delivery. Close reports counts. node:test tests beside the script. | SKILL.md, source-contract.md, `skills/clinical-infographic/scripts/` |
| C5 | CI-08 | Output case `output-fidelity-and-safety`: prompt names `ppgl-infographic.html`; every file grader uses that literal path; new grader: the fidelity script was run. | evals/clinical-infographic/output-fidelity-and-safety/ |

### Rewrite-plan steps done ahead of wave

- S06-W1-1 (C1): all CSS edits land; its `auditInfographicResponsive` check is deferred (needs `$LEARN_HUB_DIR`, not present in the cloud session).
- S03-W3-2, part: P6 rewrites decision-brief.md's indirectness line, so its K13 wording ("a community OPD", not "a Klaeng OPD") lands in the same edit. The rest of S03-W3-2 (H45 slot split, intent-lock-pairing mirror) stays at W3.
- Recorded once per place: docs/rewrite/baseline.md `## Owner records`, one note under each wave in docs/plugin-rewrite/plan.md, one "Done ahead / Partly done <sha>" line in S03 and S06 (which also tells W2/W3 to keep: literal eval paths, the `evidence-checks.md` reference, `verify-infographic.mjs` as input to S06-W2-1's `check-html.mjs`, the grader tool prefix changing to `plugin_evidence_` at W3).

## Out of scope (named so nothing is silently dropped)

- comprehensive-review's review-arc.md safety floor (the producer half of PR-52 for whole-topic reports) — other plugin; in deferred-findings.md.
- Skill `description` wording — owner decision QD3, rewrite W3.
- Mock-backed fidelity cases with planted traps (new eval case dirs) — S03-W3-6 / S06 own the case list; recorded as a follow-up.
- Glob paths in sibling suites (comprehensive-review `output-report-contract/graders/no-inline-citation.md`, psych-paper-digest `tier-sections.md`, `no-pmid-in-digest.md`) — same defect as CI-08, other plugins.
- The template's other deferred defects (CI-19 aside, fixed here because C4 would fail on it).

Owner note: S12-W0-8's smoke baseline for these two plugins must run `--against pre-rewrite`, because this pass changes their skill text.

## Verification before push

1. `git config core.hooksPath .githooks`; `bash scripts/health.sh` (full) prints `health: OK`.
2. `node --test` on the new script's tests (run by hand — health.sh runs Python tests only; the script header says so). Tests cover: a faithful page passes (with `µg` in the source and `mcg` on the page, an ISO render date, ladder ordinals and axis ticks); a wrong number, a wrong unit, an added design label, a template leak and an ungapped `[unverified]` number each fail. Run it once on a real probe output.
3. Render the template and example with Playwright: print page count, no stacked columns in print, no `ΜG`/`MMHG` in PDF text, no dark block (`grep -c prefers-color-scheme:dark` = 0), no font-size <12px.
4. Every `target: {source: file}` grader path has no `*`/`?`/`[` (`file_exists` graders may keep globs); each changed regex is run against a hand-made good and bad output.
5. SKILL.md body token change for pubmed stays small (report before/after).
6. Bumps via `bump.py`, MEMORY.md updated; conventional commits, one logical change each; push to `claude/pubmed-clinical-infographic-quality-ei2th0`.

Owner action (cannot be done from the cloud session): tag `pre-rewrite` at `fd47fba` before this branch merges.

## Critique pass — repairs applied (one critic, 12 flaws)

1. Numeric trace would fail correct pages → the script skips ISO dates, elements marked `data-ordinal` (ladder numbers) or `data-axis` (chart ticks), and treats µg ≡ μg ≡ mcg, en dash ≡ hyphen, Unicode minus ≡ `-`; tests cover each.
2. The template's nested comment leaks `{{sourced values}}` and `-->` onto the page → fixed in C1 (deferred CI-19, one line).
3. The example's source report is not in the repo → tests use inline fixtures built from the eval's `review.md` facts; no example-vs-source run is claimed.
4. `--render` may not find Playwright; print half of CI-05 lived only in the script → the script also searches `NODE_PATH` and the global npm root and says clearly when it skips; SKILL.md Step 2.5 itself now requires an A4 print render + page count + no stacked columns.
5. "revised YYYY-MM" alone lets an old label pass → must be the newest version on the regulator's site (an older one is cited only as superseded); supplements get the safety-communication sweep; the Sources drift tell says a label's revision date is not a publication year.
6. Graders need literal tokens → SKILL.md and report-craft.md pin the words **Verdict** and **Confidence:**; confidence regex `Confidence\W{0,6}(?:very low|high|moderate|low)\b` (i); CI regexes tolerate rounding.
7. Glob check scoped to file targets; sibling glob graders listed out of scope.
8. More steps per run → the pubmed output case gets `max_turns: 80`, `timeout_seconds: 1800`.
9. Specs would reintroduce old paths/plans → one line each in S03 and S06 (see above).
10. C3 also edits the template's safety comments (:5, :217) and SKILL.md's failure condition, and adds scaffolds for the coverage line and the neutral "Not recommended — no benefit shown" panel.
11. The ledger's qualifier checklist includes upstream tags (`my inference:`, `abstract only`, `calculated`); a design label never in the source blocks, a label count above the source only warns.
12. Mechanism-prose exemption reaches every "no number" site; `as reported in` describes the review, never Author Year; the H45 deletion is cut; bookkeeping reduced to one line per place.
