# HIGH-defect coverage (H01-H49)

Appendix A of `docs/plugin-rewrite/architecture.md` as a checklist (spec S12, I17).
Canonical copy: micky-psych-tools; learn-hub holds a byte-for-byte copy. Rows split
across two waves are H<nn>a (first wave) and H<nn>b (second wave). Close rows only
in the wave's tag step: `python3 scripts/rewrite_gate.py h-coverage close --id <H> --wave <Wn> --write`.

- [ ] H01 intent-lock-1 — silent contract contradicted in 11 places — closed: no — wave: W3
- [ ] H02 intent-lock-2 — picker contract not executable in CC; no fallback — closed: no — wave: W3
- [ ] H03 intent-lock-3 — ledger in the plugin tree cannot compound — closed: no — wave: W3
- [ ] H04 intent-lock-4 — `Prior:` has no eliciting question — closed: no — wave: W3
- [ ] H05 intent-lock-5 — callers expect Reframed/Skipped — closed: no — wave: W2
- [ ] H06 intent-lock (learn-hub clone)-1 — fork splits the ledger — closed: no — wave: W2
- [ ] H07a plugin-creator-1 — repo-bound, no precondition — closed: no — wave: W1
- [ ] H07b plugin-creator-1 — repo-bound, no precondition — closed: no — wave: W3
- [ ] H08 vault-keeper-1 — `${CLAUDE_PLUGIN_ROOT}/../../vault` wrong in cache — closed: no — wave: W1
- [ ] H09 vault-keeper-2 — walk-up matches learn-hub — closed: no — wave: W1
- [ ] H10a vault-keeper-3 — stale learn-hub marker in empty-vault — closed: no — wave: W1
- [ ] H10b vault-keeper-3 — stale learn-hub marker in empty-vault — closed: no — wave: W2
- [ ] H11a vault-keeper-4 — empty-vault deletes assets that have receivers — closed: no — wave: W1
- [ ] H11b vault-keeper-4 — empty-vault deletes assets that have receivers — closed: no — wave: W2
- [ ] H12 firecrawl-1 — stale "verbatim" vendor guide — closed: no — wave: W1
- [ ] H13 validate.py-1 — tracebacks; uncounted PASS — closed: no — wave: W0
- [ ] H14 learn-hub-local-1 — catalog never registered — closed: no — wave: W2
- [ ] H15 digest-report-1 — input contract vs `## Sources` producers — closed: no — wave: W2
- [ ] H16 digest-report-2 — not loaded anywhere — closed: no — wave: W2
- [ ] H17 source-to-vault-1 — prod rows without vault files — closed: no — wave: W1
- [ ] H18 source-to-vault-2 — no-arg batch ingest of `Book/` — closed: no — wave: W1
- [ ] H19 source-to-vault-3 — routing collision, no negative scope — closed: no — wave: W1
- [ ] H20 source-to-vault-4 — omits embedding/diagrams/images — closed: no — wave: W1
- [ ] H21 atomize-book-1 — `[[topic-id]]` contradiction — closed: no — wave: W1
- [ ] H22 atomize-book-2 — stale sync economics — closed: no — wave: W1
- [ ] H23 atomize-book-3 — 4 drafting rules missing — closed: no — wave: W1
- [ ] H24 atomize-book-4 — ~21.3k-token body — closed: no — wave: W4
- [ ] H25 ingest-article-1 — Windows inbox; bare invocation deletes; not ignored — closed: no — wave: W1
- [ ] H26 ingest-article-2 — source-cover command cannot run — closed: no — wave: W1
- [ ] H27 ingest-slides-1 — wrong script paths — closed: no — wave: W1
- [ ] H28 ingest-slides-2 — routing conflict with pdf-pipeline — closed: no — wave: W1
- [ ] H29 ingest-infographic-1 — dead empty-vault contract — closed: no — wave: W2
- [ ] H30 ingest-infographic-2 — "targeted upsert == npm run sync" — closed: no — wave: W1
- [ ] H31 ingest-animation-1 — dead empty-vault contract — closed: no — wave: W2
- [ ] H32 pdf-pipeline-1 — slides → atomize-book — closed: no — wave: W1
- [ ] H33 pdf-pipeline-2 — impossible apply rule — closed: no — wave: W1
- [ ] H34 sync-vault-1 — recommends nested layout — closed: no — wave: W1
- [ ] H35 sync-vault-2 — default `npm run sync` path; no traps — closed: no — wave: W1
- [ ] H36 clinical-infographic-1 — dark block in template + example — closed: no — wave: W1
- [ ] H37 clinical-infographic-2 — `.mech` cramps on phones — closed: no — wave: W1
- [ ] H38 concept-animation-1 — stage-collapse layout rule — closed: no — wave: W2
- [ ] H39 concept-animation-2 — single-viewport fit check — closed: no — wave: W2
- [ ] H40 ml-concept-lab-1 — stage-collapse layout rule — closed: no — wave: W2
- [ ] H41 ml-concept-lab-2 — verify recipe fails (ESM playwright) — closed: no — wave: W2
- [ ] H42 code-explainer-1 — template never existed — closed: no — wave: W1
- [ ] H43 concept-animation (learn-hub copy)-1 — invalid strict YAML — closed: no — wave: W1
- [ ] H44 pubmed-research-note-1 — Reframed preface stale — closed: no — wave: W2
- [ ] H45 pubmed-research-note-2 — decision-brief slot arithmetic (4 + 3 over 6 headings) — closed: no — wave: W3
- [ ] H46 psych-paper-digest-1 — pdat vs edat — closed: no — wave: W1
- [ ] H47 psych-paper-digest-2 — silent truncation at 50 — closed: no — wave: W1
- [ ] H48 pubmed-research-note (learn-hub fork)-1 — evals fail by construction — closed: no — wave: W2
- [ ] H49 comprehensive-review (learn-hub fork)-1 — default digest + live sync — closed: no — wave: W2
