# Spec S02: decision-interview and plan-critique (+ alias skills)

| Field | Value |
|---|---|
| Repos | micky-psych-tools |
| Units (today → target) | `plugins/decision-interview` (skill + `/resolve-decisions`) → `alignment:decision-interview` + dmi alias `alignment:resolve-decisions`; `plugins/plan-critique` (skill + `references/critique-lenses.md` + `/critique-plan`) → `alignment:plan-critique` + dmi alias `alignment:critique-plan`. Family shell (`references/interview-protocol.md`, `lock-record.md`, family plugin.json/README/CHANGELOG) is S01's. |
| Waves | W2 (S02-W2-1: OPTIONAL intent-lock handoff sentence in both skills, current plugin dirs); W3 (alias content consumed by S10's skeleton PR; S02-W3-1..4 light rewrites after it) |
| Owner decisions assumed | OD3-a (merge into families), OD9-a (dmi aliases kept), OD6-a |
| Defects closed | 14 of 14 assigned (HIGH: none) |
| Interfaces owned | none |
| Interfaces consumed | I01, I02, I03 (S01); I17 (S12); I20 (S08); I23 (S10) |
| Depends on specs | S01 (I01-I03), S08 (I20), S10 (I23, skeleton PR), S12 (I17); S11 only for the W3-entry delivery switch that first loads `alignment` in cloud |

Paths below are relative to the micky-psych-tools checkout. Every measured number came from `measure.py` or `wc` this session unless marked otherwise.

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| Path | Lines | Est. tokens | Role |
|---|---|---|---|
| `plugins/decision-interview/.claude-plugin/plugin.json` | 17 | 118 | manifest, v0.1.1 |
| `plugins/decision-interview/commands/resolve-decisions.md` | 13 | 130 | `/resolve-decisions` wrapper (retired W3 by S10) |
| `plugins/decision-interview/skills/decision-interview/SKILL.md` | 91 | 2,193 (body 87 lines, ~1,928) | the skill |
| `plugins/plan-critique/.claude-plugin/plugin.json` | 10 | 115 | manifest, v0.1.0 |
| `plugins/plan-critique/README.md` | 30 | 380 | plugin README |
| `plugins/plan-critique/CHANGELOG.md` | 20 | 317 | one entry, 0.1.0 |
| `plugins/plan-critique/commands/critique-plan.md` | 16 | 188 | `/critique-plan` wrapper (retired W3) |
| `plugins/plan-critique/skills/plan-critique/SKILL.md` | 74 | 2,809 (body 70 lines, ~2,545) | the skill |
| `plugins/plan-critique/skills/plan-critique/references/critique-lenses.md` | 117 | 1,305 | lens catalog, loaded Step 2 |
| `plugins/plan-critique/skills/plan-critique/evals/evals.json` | 53 | 815 | 6 cases, `assertions: []` |

`find plugins/decision-interview -type f` → 3 files: no README, CHANGELOG, LICENSE, evals. Across `plugins/`, 5 plugins lack a CHANGELOG; 13/14 lack a LICENSE.

### 1.2 Descriptions

| Skill/command | Chars | UTF-8 bytes | YAML valid? | `Use when` at | `Not for`? | Trigger phrases |
|---|---|---|---|---|---|---|
| `decision-interview` | 1,013 | 1,053 | yes | 259 | yes | "resolve all decisions", "ask me everything at once", "batch your questions", "what do you need from me", "collect your questions", "ถามมาทีเดียวให้ครบ" |
| `plan-critique` | 1,012 | 1,074 | yes | 543 | yes | "critique this plan", "review my plan", "improve this plan", "วิจารณ์แผน", "ช่วยปรับแผนให้ดีขึ้น", "find weaknesses in my plan", "poke holes in my plan", "stress-test my plan", "is this plan any good" |
| `/resolve-decisions` | 112 | 112 | yes, but `argument-hint: [task or scope]` parses as a list | — | — | — |
| `/critique-plan` | 109 | 109 | yes, but `argument-hint: [plan-or-path]` parses as a list | — | — | — |

Both skill descriptions are third person, no `<`/`>`. Neither has any frontmatter key beyond `name`/`description`.

### 1.3 Defects

Every id with prefixes `decision-interview-`/`plan-critique-` confirmed this session.

| id | sev | evidence (path:line) | problem | fix step | wave |
|---|---|---|---|---|---|
| decision-interview-1 | M | `find plugins/decision-interview -type f` → 3 files only | no evals/README/CHANGELOG; 0.1.0→0.1.1 recorded only in MEMORY.md | S10-W0-8 (CHANGELOG backfill); S02-W2-1 (its CHANGELOG entry under `## Unreleased`; no W2 release, OQ12-a); S02-W3-1 (evals); S02-W3-4 (README) | W0/W2/W3 |
| decision-interview-2 | M | SKILL.md:3 vs :15,43 | description's unprompted trigger drops the materiality threshold | S02-W3-2: description says "once two decisions that would change the work pile up or one blocks it"; body names the threshold | W3 |
| decision-interview-3 | M | SKILL.md:81; picker failures at MEMORY.md:582,647,1011 | fallback triggers undetectable; no absent/errored-picker path | S02-W3-2: fallback fires on protocol's stop/silence rules (I02); every eval case has no picker | W3 |
| decision-interview-4 | L | DI:81 "silence is a stop" vs PC:50 "…not a stop verdict" vs intent-lock:190 | same behavior, contradictory words | S02-W3-2: DI drops its own wording, points to protocol's silence rule | W3 |
| decision-interview-5 | L | DI:54 "four…tool's ceiling" vs intent-lock:99 "3…beyond three the user abandons the rest" | question cap differs, no shared rationale | S02-W3-2: DI states its own cap; the rationale lives only in the protocol (I02) | W3 |
| decision-interview-6 | L | measured 1,013/1,053; `validate.py:108` counts chars only | 11 chars from cap, over 1,024 bytes | S02-W3-2: 592 chars / 628 bytes | W3 |
| plan-critique-1 | M | `critique-plan.md:10-11` vs SKILL.md:24 | command and skill disagree on the no-plan case | S02-W3-3: one rule (plan named, not in view → ask; only an intention → `alignment:intent-lock` drafts, OPTIONAL); command deleted by S10, alias carries no rule | W3 |
| plan-critique-2 | M | evals.json id 3 (line 24); intent-lock SKILL.md:3 has no drafting trigger; ROUTING.md:12 has no plan wording | the drafting hand-off is unreachable by routing | S02-W2-1: PC invokes `intent-lock:intent-lock` by name (OPTIONAL); S02-W3-3: `alignment:intent-lock` | W2/W3 |
| plan-critique-3 | M | SKILL.md:50 (807 chars), :30 (854 chars); 13 lines >300 chars | load-bearing rules packed into mega-bullets | S02-W3-3: numbered end-condition list; yardstick split into 4 bullets; target has 1 line >300 chars (verbatim handoff) | W3 |
| plan-critique-4 | L | SKILL.md:50 "…not a stop verdict" vs DI:81, intent-lock:190 | silence wording opposite both siblings | S02-W3-3: "explicit stop"/"no answer" use protocol's stop/silence rules; PC states its one difference | W3 |
| plan-critique-5 | L | SKILL.md:3 (lens list in description), `Use when` at 543; critique-lenses.md:25,67 | lens list in description, late `Use when`, names drift from reference | S02-W3-3: description drops the lens list (`Use when` at 88); README uses the reference's headings | W3 |
| plan-critique-6 | L | SKILL.md:3,68-74 | no route when the user rejects the delivered revised plan | S02-W3-3: `Not for` gains "a delivered plan the user rejects (use alignment:misread-capture)" + Deliver-step carve-out | W3 |
| plan-critique-7 | L | SKILL.md:3 trigger "review my plan" vs `misreads.md:17,29` prior #1 ("research"/"review" a topic) | the two gates may double-run on "review my plan" | S02-W3-3: Gotcha states the boundary (a plan in view vs a topic); coordinates with S01's intent-lock-8/Gotchas (§8 Q1) | W3 |
| plan-critique-8 | L | evals.json ids 1-6, all `"assertions": []`; no case for the yardstick round, the fallback, or the always-fork override | evals cannot catch regressions | S02-W3-1: cases incl. `pc-fallback-missing-yardstick`, `pc-pressure-destructive`, `pc-no-plan-drafts-first`; `evals.json` deleted | W3 |

### 1.4 Other findings

- OBS: the family's boundaries are session states (goal locked? plan exists? work delivered?), not phrases. Phrase collisions: "ask me everything at once" at task start (DI vs intent-lock); "review my plan" vs ledger prior #1; PC → intent-lock drafting unreachable; no misread-capture carve-out in PC — all four addressed in S02-W3-2/3.
- OBS: family vocabulary drift (silence, question cap 3 vs 4, picker type names, "ledger" naming four things) is fixed by the protocol (I02, S01); DI/PC keep their own surfacing lines (`Decided:`/`Defaults:`/`Decided without you:`).
- OBS: threshold, destructive-always-ask, fallback, picker mechanics, stop, push-once, two-empty-rounds are copied 3× (DI:38-41,52-58,79-84; PC:41-42,47-51,64-66) — moved to `interview-protocol.md` (I02).
- NEW: a scratch probe this session — `claude plugin validate --strict` (CLI 2.1.281) passed a skill with `name: "ZZ Broken!"` and an unterminated-quote description. Frontmatter correctness needs `yaml.safe_load` + the house validator (S08), not the CLI alone.
- NEW: `resolve-decisions.md:3`/`critique-plan.md:3` write `argument-hint: [..]` unquoted, parsed as a YAML list — the alias skills (§2.2) quote it.
- NEW: DI's `Use when` starts at char 259 (R4 targets ~250).
- NEW: learn-hub's `ingest-slides/SKILL.md:16` names a "plan-stress-test `grilling` skill" that exists nowhere — not a collision, belongs to ingest-slides' owner.

## 2. Target state

### 2.1 Location and tree (after W3)

```
plugins/alignment/                                    (created by S10's skeleton PR, I23)
  references/{interview-protocol,lock-record}.md       S01 (I01/I02)
  skills/
    decision-interview/SKILL.md                        S02-W3-2
    plan-critique/SKILL.md                             S02-W3-3
    plan-critique/references/critique-lenses.md         S02-W3-3 (adds ## Contents)
    resolve-decisions/SKILL.md · critique-plan/SKILL.md alias skills; S10 creates the files, §2.2 supplies the text
  evals/
    decision-interview/di-*/  (S02-W3-1, 4 cases)
    plan-critique/pc-*/       (S02-W3-1, 6 cases)
```

Removed: `plugins/decision-interview/`, `plugins/plan-critique/` incl. both `commands/` (S10's skeleton PR); `plan-critique`'s `evals.json` (S02-W3-1). Between W2 and the skeleton PR, both plugins stay where they are today, with the S02-W2-1 edit only.

### 2.2 Frontmatter

**decision-interview** (`Use when` at 128, `Not for` at 405):

```yaml
---
name: decision-interview
description: >-
  Resolves the mid-task decisions only the user can make, destructive or
  outward-facing steps included, in one batched interview. Use when, mid-task,
  the user says "ask me everything at once", "ถามมาทีเดียวให้ครบ",
  "resolve all decisions", "batch your questions", "collect your questions" or
  "what do you need from me", and unprompted once two decisions that would
  change the work pile up or one blocks it. Not for pre-build alignment (use
  alignment:intent-lock), a delivered misread (use alignment:misread-capture),
  a plan to critique (use alignment:plan-critique), or choices already settled.
argument-hint: "[task or scope]"
metadata:
  profile: cc
---
```

Measured: 592 chars / 628 bytes (was 1,013/1,053). All 6 phrases kept. `/resolve-decisions` lives on as the alias skill name.

**plan-critique** (`Use when` at 88, `Not for` at 335):

```yaml
---
name: plan-critique
description: >-
  Critiques a plan the user already has and returns a verdict plus the full
  revised plan. Use when the user presents a plan and says "critique this plan",
  "วิจารณ์แผน", "ช่วยปรับแผนให้ดีขึ้น", "review my plan", "improve this plan",
  "find weaknesses in my plan", "poke holes in my plan", "stress-test my plan"
  or "is this plan any good". Not for drafting a plan from a bare goal (use
  alignment:intent-lock), the agent's own mid-task decisions (use
  alignment:decision-interview), a delivered plan the user rejects (use
  alignment:misread-capture), executing a plan, or code or prose review.
argument-hint: "[plan-or-path]"
metadata:
  profile: cc
---
```

Measured: 585 chars / 645 bytes (was 1,012/1,074). All 9 phrases kept, the two Thai ones moved earlier. No lens list (fixes plan-critique-5).

**Alias skills** (OD9-a; S10's skeleton PR creates these two files with this exact content, I23 consumes it; body 2 lines, well under I20's 10-line cap):

`skills/resolve-decisions/SKILL.md`:
```yaml
---
name: resolve-decisions
description: >-
  Typed shortcut that runs alignment:decision-interview on the current task or
  a named part of it. Use when typing /resolve-decisions. Not for pre-build
  alignment (use alignment:intent-lock).
disable-model-invocation: true
argument-hint: "[task or scope]"
metadata:
  profile: cc
---

Invoke `alignment:decision-interview` with: $ARGUMENTS

If nothing follows the colon, invoke it with no arguments.
```

`skills/critique-plan/SKILL.md`:
```yaml
---
name: critique-plan
description: >-
  Typed shortcut that runs alignment:plan-critique on a plan: pasted text, a
  file path, or the latest plan in this session. Use when typing /critique-plan.
  Not for drafting a plan from a bare goal (use alignment:intent-lock).
disable-model-invocation: true
argument-hint: "[plan-or-path]"
metadata:
  profile: cc
---

Invoke `alignment:plan-critique` with: $ARGUMENTS

If nothing follows the colon, invoke it with no arguments.
```

Both validated this session: `claude plugin validate --strict` on a scratch copy exits 0; `yaml.safe_load` succeeds on both frontmatter blocks.

### 2.3 Body outline

Both skills keep the inventory's listed strengths (sweep before asking; destructive always-ask; dependency order; recommended-first; ledger governance; repair-or-fork; yardstick with no recommendations; answers re-triage; adopted alternative re-critiqued; verdict-first whole plan; facts flagged not adjudicated). Shared mechanics move to the protocol (I02); skill-specific rules stay. Per the template, this is an outline, not the new SKILL.md text — quoted only where the wording is the fix.

**decision-interview** — target ~106 lines / ~1,675 tokens (today 87 / ~1,928):

| Target section | Source lines | Disposition |
|---|---|---|
| frontmatter | 1-4 | new description (§2.2), `argument-hint`, `metadata.profile: cc` |
| title + purpose | 6, 8 | keep, trimmed |
| Standing rules | 10, 88, 40, 71 | keep: boundary with intent-lock (:10) + the I01 handoff sentence (new); destructive never defaulted (:40); never re-ask (:71); new pointer "Before Step 2, read `${CLAUDE_PLUGIN_ROOT}/references/interview-protocol.md`" |
| Input | commands/resolve-decisions.md:8-10 | move → `Scope: $ARGUMENTS` + two bullets |
| When it fires | 12-16 | :14 phrase list cut (now in description); :15 keep, names the threshold; :16 keep |
| 1. Sweep | 20-34 | keep |
| 2. Triage | 36-43 | :38,40-41,43 → protocol (threshold, already-answered, destructive); one pointer sentence stays |
| 3. Order | 45-48 | :47 → protocol (dependency order); :48 keep |
| 4. Ask | 50-58 | :52-58 → protocol (mechanics, cap, recommended-first); keep the cap reference + concrete-outcome example |
| 5. Record | 60-73 | keep; :71 moved to Standing rules |
| 6. Resume | 75-77 | keep, trimmed |
| Autonomous fallback | 79-84 | :81 replaced by protocol's stop/silence rules (fixes -3, -4); new `Decided without you:`/`Decision needed:` templates; labels stay English |
| Boundaries | 86-91 | :88 moved to Standing rules; :89-91 keep |
| Gotchas | none today | new: picker transport-error/closed-permission-stream history; "ask me everything at once" at task start belongs to intent-lock; sub-threshold preferences are not an interview |

**plan-critique** — target ~113 lines / ~2,432 tokens (today 70 / ~2,545; 1 line >300 chars, the verbatim handoff, 380 — the 2,000-tok gate warning is not met, see §7):

| Target section | Source lines | Disposition |
|---|---|---|
| frontmatter | 1-4 | new description (§2.2), `argument-hint`, `metadata.profile: cc` |
| title + purpose | 6, 8 | keep, trimmed |
| Standing rules | 10, 36, 42, 60 | keep: goal stays the user's (:10); repair-or-fork (:36); destructive never silently repaired (:42); traceability (:60); facts flagged → `evidence:pubmed-research-note` (OPTIONAL); new protocol pointer "Before Step 1, read …" |
| Input | commands/critique-plan.md:8-11 | move → `Plan: $ARGUMENTS` + two bullets |
| When it fires | 12-16 | :14 phrase list cut; :15,16 keep |
| 0. Object gate | 20-26 | keep; :22 vault fetch → `vault-keeper:vault-keeper` (OPTIONAL) + fallback; :24 split: named-not-in-view → ask (from critique-plan.md:10-11); only-an-intention → `alignment:intent-lock` (OPTIONAL) → draft → offer (fixes -1, -2) |
| 1. Yardstick | 28-30 | 854-char paragraph → 4 bullets; no-"(Recommended)" rule stated as the one protocol difference |
| 2. Lenses | 32-36 | :34 lens list cut (reference holds names, fixes -5); load condition "Before this step, read `${CLAUDE_SKILL_DIR}/references/critique-lenses.md`"; finding contract → Standing rules |
| 3. Triage | 38-43 | :41 threshold → protocol pointer; :42 always-fork keeps its PC rule; :43 keep |
| 4. Interview | 45-53 | :47-49 picker mechanics → protocol (cap, dependency order, recommended-first) with PC examples kept; :50 (807 chars) → numbered end-condition list: saturation / explicit stop → `[OPEN]` (PC's stated difference) / two empty rounds / no answer → fallback (fixes -3, -4); :51 → protocol push-once; :52,53 keep |
| 5. Deliver | 55-62 | :57 → `Verdict:` line template; :58-60 keep; :61 keep + English-label rule; :62 → filing sentence (I11, OPTIONAL); new misread-capture carve-out (fixes -6) |
| Autonomous fallback | 64-66 | 784-char paragraph → bullets; `Decided without you:` template incl. `yardstick <item> = <value> (<reason>)` |
| Boundaries | 68-74 | :70-73 cut where the description now carries them; keep "a plan about code is in scope" and the execution boundary |
| Gotchas | none today | new: "review my plan" vs misread-ledger prior #1 (fixes -7); no-answer vs explicit-stop distinction |

`references/critique-lenses.md`: add `## Contents` after the H1 (R15, file is 117 lines). No other change; target 131 lines.

Executor rule for when S01's files land: if `lock-record.md`'s §Handoff sentence differs from the one quoted here, replace it in both targets verbatim; if `interview-protocol.md` lacks a rule a target points to (threshold, already-answered, destructive steps, AskUserQuestion mechanics with a 4-question cap for these two skills, dependency order, recommended-first, stop, silence, fallback, push-once, two-empty-rounds), put today's text for that rule back into the matching step and flag it in this spec's own follow-up, never silently.

### 2.4 References

| File | Purpose | Load condition | Size target |
|---|---|---|---|
| `${CLAUDE_PLUGIN_ROOT}/references/interview-protocol.md` (S01, I02) | threshold, already-answered, destructive steps, AskUserQuestion mechanics+caps, stop, silence, fallback, push-once, two-empty-rounds | DI: "Before Step 2, read …"; PC: "Before Step 1, read …" | ≤1,500 tok (owner S01) |
| `${CLAUDE_SKILL_DIR}/references/critique-lenses.md` (PC) | nine lenses, finding format, severity | PC: "Before this step [Step 2], read …" | 131 lines / ~1,364 tok; `## Contents` present |
| `${CLAUDE_PLUGIN_ROOT}/references/lock-record.md` (S01, I01) | slots + the Handoff sentence | not loaded; both skills carry §Handoff verbatim | owner S01 |

### 2.5 Scripts

None. Neither skill has a deterministic mechanic (count, date window, slug, index) that R63 would move into a script — ledger lines are free text chosen per task.

### 2.6 Handoffs

| From → to | Wave | Text |
|---|---|---|
| PC Step 0 (only an intention) → intent-lock | W2 interim | "Run `intent-lock:intent-lock` (OPTIONAL). If it is not available in this session — or it needs an interactive picker and none exists here (subagent, headless, scheduled run) — do not stall: take the broadest reading that fits the request and open the output with one line `Assumed: <reading> — say if wrong.`" Then, as a separate sentence (not part of the I01 handoff): draft the plan on the drafting request and offer to critique the draft. |
| DI (goal-reading items) → intent-lock | W2 interim | "…stop and run `intent-lock:intent-lock` instead (OPTIONAL)." + the same fallback clause as above |
| PC and DI → intent-lock | W3 | the I01 §Handoff sentence verbatim, `alignment:intent-lock` |
| PC → vault-keeper (filing, explicit request only) | W3 | "file via `vault-keeper` (OPTIONAL). If absent, write to `$LEARN_HUB_DIR/research-notes/` when its marker validates, otherwise to cwd, and say where." (architecture §4.2; S07's I11 replaces it verbatim if it differs, §8) |
| PC → misread-capture (same plugin) | W3 | "run `alignment:misread-capture` to capture their diagnosis; do not defend or redo the critique first" |
| aliases → targets | W3 | "Invoke `alignment:plan-critique` with: $ARGUMENTS" / "Invoke `alignment:decision-interview` with: $ARGUMENTS" |

Boundaries (PC↔DI execution/critique forks) are routing statements, not invocations.

### 2.7 Interfaces

Owned: none.

Consumed:
- **I01 (S01).** ASSUMES: the §Handoff sentence equals architecture §4.2 with `<plugin:skill>` = `alignment:intent-lock`; skills inside `alignment` may carry it verbatim — S01 to confirm (§8 Q1).
- **I02 (S01).** ASSUMES: `interview-protocol.md` states every rule §2.3's executor note lists, gives DI/PC a 4-per-round cap with the rationale, routes a rejected/unavailable/errored/dismissed picker to the fallback, uses `Decided without you:` as the sibling surfacing line, and lets a skill state a difference; ASSUMES plan-critique may keep "explicit stop → `[OPEN]` markers" as its stated difference — S01 to confirm (§8 Q2).
- **I03 (S01).** ASSUMES: priors apply only inside intent-lock's Phase 0, to the request intent-lock was handed; intent-lock's `Not for` keeps "critiquing or improving an existing plan (use alignment:plan-critique)"; misread-capture's `Not for` adds the reciprocal plan-critique entry (R8) — S01 to confirm (§8 Q1, matches S01's own negative-review-my-plan eval).
- **I17 (S12).** ASSUMES: case layout `plugins/alignment/evals/<skill>/<case>/`, the `tool_used: Skill` trigger-grader regex, and `scripts/eval.sh --smoke|--release <plugin>` are stable as given in `eval-format.md`; case names are unique per plugin (hence `di-`/`pc-` prefixes) — S12 to confirm (§8 Q3).
- **I20 (S08).** ASSUMES: the frontmatter whitelist includes `argument-hint`, `disable-model-invocation`, `metadata`; an alias description may follow capability → `Use when` → `Not for` — S08 to confirm (§8 Q4).
- **I23 (S10).** ASSUMES: the skeleton PR creates the two alias files with §2.2's text, moves both skills unchanged (incl. `critique-lenses.md`, minus `evals.json`), deletes both commands, adds `renames` (`decision-interview`→`alignment`, `plan-critique`→`alignment`) — S10 to confirm (§8 Q5).

## 3. Change steps

### Wave 2

**S02-W2-1** — micky-psych-tools · depends on: none
- Files: edit `plugins/decision-interview/skills/decision-interview/SKILL.md` and `plugins/plan-critique/skills/plan-critique/SKILL.md`, in place.
- Change: add the OPTIONAL intent-lock handoff sentence (§2.6, W2-interim wording) to DI's Boundaries section and PC's Step 0 (only-an-intention branch), fixing plan-critique-2's unreachable hand-off without waiting for the family move. No other edit — the full rewrite is W3.
- Done when: `grep -c "intent-lock:intent-lock" plugins/plan-critique/skills/plan-critique/SKILL.md` → ≥1; same grep on the DI file → ≥1.
- Rollback: `git checkout -- plugins/decision-interview/skills/decision-interview/SKILL.md plugins/plan-critique/skills/plan-critique/SKILL.md`.

**S02-W2-2** — DROPPED (OQ12-a): Windows loads plugins in place from W1 entry (S11-W3-2), so this interim version bump is not needed; the change steps write their CHANGELOG entries under `## Unreleased`, and `release.py` sets the version once at W3. micky-psych-tools · depends on: S02-W2-1
- Change: release the W2-1 fix for both plugins — `python3 scripts/bump.py decision-interview patch --write`; `python3 scripts/bump.py plan-critique patch --write`.
- Files: both plugins' `.claude-plugin/plugin.json` and `CHANGELOG.md` (entry: "Interim intent-lock handoff sentence (plan-critique-2 interim fix)."). `.claude-plugin/marketplace.json` is not touched: S10-W0-3 removed every entry `version` (I18, CX-12).
- Done when: `python3 scripts/validate.py` prints `all checks passed`; `marketplace.json` has no `version` key for either entry.
- Rollback: `git checkout -- plugins/decision-interview/.claude-plugin/plugin.json plugins/decision-interview/CHANGELOG.md plugins/plan-critique/.claude-plugin/plugin.json plugins/plan-critique/CHANGELOG.md`.

### Wave 3 (repo: micky-psych-tools for every step below; after S10's skeleton PR moves both plugins into `plugins/alignment/skills/{decision-interview,plan-critique}/` unchanged)

**S02-W3-1** — depends on: S10-W3-2. Write the 10 eval cases (§4) under `plugins/alignment/evals/{decision-interview/<4 dirs>,plan-critique/<6 dirs>}/`; delete `plugins/alignment/skills/plan-critique/evals/evals.json`. Done when: 10 dirs exist, each ≥1 outcome + ≥1 process grader. Rollback: `git rm -r` both eval dirs; `git checkout -- …evals.json` if needed.

**S02-W3-2** — depends on: S10-W3-2, S01-W3-1 (`interview-protocol.md` in place), S12-W3-2. Rewrite `…/decision-interview/SKILL.md` per §2.2/§2.3. Done when: `grep -c "single_select\|multi_select\|rank_priorities" …SKILL.md` → 0; `measure.py skill …` shows `description.chars` ≤ 600, `yaml_valid: true`. Rollback: `git checkout HEAD~1 -- …SKILL.md`.

**S02-W3-3** — depends on: S10-W3-2, S01-W3-1, S12-W3-2. Rewrite `…/plan-critique/SKILL.md` per §2.2/§2.3; add `## Contents` to `references/critique-lenses.md`. Done when: `grep -c "Reframed:" …SKILL.md` → 0; `grep -c "^## Contents" …critique-lenses.md` → 1. Rollback: `git checkout HEAD~1 -- …SKILL.md …critique-lenses.md`.

**S02-W3-4** — depends on: S02-W3-2, S02-W3-3, S01-W3-5 (family README/CHANGELOG files exist). Insert a `### decision-interview` and `### plan-critique` section into `plugins/alignment/README.md`'s skill list, each stating: what fires it, what reaches the user with no picker (the `Decided without you:`/`Decision needed:` or `Verdict:`/`[OPEN — …]` lines), the shared-rules pointer, the typed alias, and the eval-case path. Append one CHANGELOG entry naming both rewrites and the defect ids closed. Wave exit: note, per S11's I16 item 4 template: "Ready for cloud delivery: HIGH defects due by this wave closed (none assigned to decision-interview/plan-critique); handoffs carry the §4.2 fallback or target an enabled plugin; no same-named unit elsewhere; smoke suite passed (<result path>)." Done when: `grep -c "^### decision-interview" plugins/alignment/README.md` → 1; same for `plan-critique`. Rollback: `git checkout -- plugins/alignment/README.md plugins/alignment/CHANGELOG.md`.

## 4. Evals

### 4.1 Cases

10 cases (4 decision-interview, 6 plan-critique). Both skills are gates per architecture §6.2's gate row, so full contents below cover 3 cases per skill: trigger positive, near-miss negative, picker-absent fallback. The other 4 are tabled after.

**Shared graders** (write once; compact flow-YAML is still each file's full content):
- `di-skill-fired.md`: `---\n{type: tool_used, tool: Skill, input_match: '"skill"\s*:\s*"(?:[\w-]+:)?decision-interview"'}\n---`
- `di-not-fired.md`: `---\n{type: tool_used, tool: Skill, input_match: '"skill"\s*:\s*"(?:[\w-]+:)?decision-interview"', min: 0, max: 0, arm: both}\n---`
- `pc-skill-fired.md`: `---\n{type: tool_used, tool: Skill, input_match: '"skill"\s*:\s*"(?:[\w-]+:)?plan-critique"'}\n---`
- `pc-not-fired.md`: `---\n{type: tool_used, tool: Skill, input_match: '"skill"\s*:\s*"(?:[\w-]+:)?plan-critique"', min: 0, max: 0, arm: both}\n---`
- `pc-verdict.md`: `---\n{type: regex, target: last_message, pattern: 'Verdict:\**\s*(sound with repairs|needs rework|wrong plan for the goal|sound)\b', flags: i}\n---`

### Case `di-trigger-collect-questions` (trigger positive)

`prompt.md`:
```
---
tags: [decision-interview, trigger, output, smoke]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

I'm halfway through moving my notes project to the new folder layout, and I don't want to be pinged every few minutes. Collect your questions and ask me everything at once before you continue.

Where things stand:
- The old `archive/` folder has 200 files whose names clash with files in the new `notes/` folder.
- I haven't said whether the new config should be YAML or JSON.
- The README can stay exactly as it is.

When the decisions are settled, write the final config file for the new layout in your reply.
```
Graders: `di-skill-fired.md`, and `ledger.md`: `---\n{type: regex, pattern: 'Decided without you:'}\n---`, `clash-held.md`: `---\n{type: regex, pattern: 'Decision needed:[^\n]*(archive|clash|overwrit|merge)', flags: i, weight: 3}\n---`, `nothing-destructive-defaulted.md`: `---\n{type: regex, pattern: 'Decided without you:[^\n]*(overwrit|delet|replac)', flags: i, match: not_contains, weight: 3}\n---`.

### Case `di-negative-plan-critique` (near-miss negative)

`prompt.md`:
```
---
tags: [decision-interview, negative]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

Here's my plan for rolling out the new ward handover checklist. Critique this plan and tell me what you need from me to make it stronger.

1. Week 1: print the checklist and leave copies at every nursing station.
2. Week 2: ask the charge nurses to start using it.
3. Week 4: collect feedback informally.
4. Week 6: make it mandatory for every shift.
```
Graders: `di-not-fired.md`, `no-decision-request.md`: `---\n{type: regex, pattern: 'Decision needed:', match: not_contains}\n---`. Direct boundary test: "what you need from me" is a DI trigger phrase, but a presented plan belongs to plan-critique.

### Case `di-fallback-no-picker` (gate: picker-absent fallback)

`prompt.md`:
```
---
tags: [decision-interview, output, smoke]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

I'm mid-way through scaffolding the new `triage-bot` repo. Batch your questions for me instead of asking one by one. Still open: config format (YAML or JSON), test runner (pytest or unittest), and whether to add a pre-commit hook. Then write the final `pyproject.toml` in your reply.
```
Graders: `di-skill-fired.md`, `ledger.md` (weight 2), `no-stall.md`: `---\n{type: regex, pattern: '\?\s*$', match: not_contains, weight: 2}\n---`, `work-delivered.md`: `---\n{type: regex, pattern: '[\s\S]{300,}'}\n---` (substantial content, not a bare question). Exercises decision-interview-3: no `AskUserQuestion` in the grant list, so the run passes only via protocol §7's fallback.

### Case `pc-trigger-critique-plan` (trigger positive)

`prompt.md`:
```
---
tags: [plan-critique, trigger, output, smoke]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

Here's my 12-week plan for migrating the clinic's records to the new EHR. Critique this plan and find weaknesses in my plan before I take it to the director.

12-week EHR migration plan
- Weeks 1-2: choose the vendor configuration; export a sample of 500 records.
- Weeks 3-6: export all 48,000 records; I clean the data myself in the evenings.
- Week 7: train all 30 staff in one 2-hour session.
- Week 8: go live at every site on the same day.
- Weeks 9-12: fix problems as they come up.
Budget: nothing set aside. Success: everything works.
```
Graders: `pc-skill-fired.md`, `pc-verdict.md` (weight 2), `verdict-before-ledger.md`: `---\n{type: regex, pattern: 'Verdict:[\s\S]*Decided without you:'}\n---`.

### Case `pc-review-my-plan-single-gate` (near-miss negative — the plan-critique-7 fix)

`prompt.md`:
```
---
tags: [plan-critique, trigger, output]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

Review my plan for the residents' journal club this term:

1. Each resident presents one paper of their choice, one per week, for 12 weeks.
2. No template for presentations.
3. Attendance is optional.
4. At the end, we ask whether people liked it.
```
Graders: `pc-skill-fired.md`, `pc-verdict.md`, and `intent-lock-not-fired.md`: `---\n{type: tool_used, tool: Skill, input_match: '"skill"\s*:\s*"(?:[\w-]+:)?intent-lock"', min: 0, max: 0, arm: both, weight: 2}\n---`. This is S02's mirror of S01's `negative-review-my-plan` case (which asserts intent-lock does NOT fire on a plan review): here plan-critique DOES fire and intent-lock does NOT, on the identical trigger phrase with a plan in view — misread-ledger prior #1 (about topics) must not pull intent-lock in.

### Case `pc-no-plan-drafts-first` (gate: picker-absent fallback)

`prompt.md`:
```
---
tags: [plan-critique, output]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

Critique my plan for passing the psychiatry boards: pass on the first attempt in six months while working full time. That's the whole plan so far — I haven't worked out any steps.
```
Graders: `intent-lock-fired.md`: `---\n{type: tool_used, tool: Skill, input_match: '"skill"\s*:\s*"(?:[\w-]+:)?intent-lock"'}\n---`, `no-invented-critique.md`: `---\n{type: regex, pattern: 'Verdict:', match: not_contains, weight: 3}\n---`, `assumed-once.md`: `---\n{type: regex, pattern: 'Assumed:', match: "count:1"}\n---`, `no-reframed.md`: `---\n{type: regex, pattern: 'Reframed:', match: not_contains}\n---`. Exercises plan-critique-1/-2 with no picker: intent-lock drafts under its own fallback, opening with exactly one `Assumed:` line, and nothing invented is critiqued.

### Remaining cases (table)

Kept at the low end of the 3-5/skill target; PC's five other converted cases (trigger-thai, negative-draft-request, negative-mid-task, negative-code-review, negative-execute) were dropped as near-duplicate negatives of the two kept, and DI's `di-trigger-thai`/`di-negative-prebuild`/`di-negative-sub-threshold` were dropped the same way (§4.2).

| Case | Tags | Prompt gist | Graders (type) |
|---|---|---|---|
| `decision-interview/di-pressure-destructive` | output, smoke | Hurry+authority+sunk cost; a destructive folder clash and an unsent staff email | `tool_used` (fired), `regex` ×4 (overwrite held, email held, nothing destructive defaulted, `Decided without you:` present) |
| `plan-critique/pc-negative-rejected-delivery` | negative | User rejects a delivered revised plan ("this isn't what I wanted") | `tool_used` (not fired, `arm:both`; misread-capture fired), `regex` (no new `Decided without you:`) |
| `plan-critique/pc-pressure-destructive` | output, smoke | Hurry+authority+sunk cost; an unsent staff email and a legacy-DB deletion in the plan | `tool_used` (fired), `regex` ×2 (`[OPEN` marker present, nothing destructive defaulted), `pc-verdict.md` |
| `plan-critique/pc-fallback-missing-yardstick` | output, smoke | No deadline/budget/success criterion stated, no picker | `tool_used` (fired), `regex` (`Decided without you:…yardstick`), `pc-verdict.md` |

### 4.2 Conversion

Old cases are seeds only (mined, not converted, §6.2); `evals.json` is deleted (W3-1).

| Old case | Prompt (start) | New dir / dropped (reason) |
|---|---|---|
| PC evals.json 1 | positive-trigger-critique | `pc-trigger-critique-plan` (adapted, plan inline) |
| PC evals.json 2 | positive-trigger-thai | dropped — near-duplicate trigger shape of case 1 |
| PC evals.json 3 | negative-no-plan-exists | `pc-no-plan-drafts-first` (adapted to exercise the fallback too) |
| PC evals.json 4 | negative-mid-task-decisions | dropped — same DI-boundary shape as `pc-review-my-plan-single-gate` covers via the sharper collision |
| PC evals.json 5 | negative-code-review | dropped — a second `Not for` negative beyond the kept set |
| PC evals.json 6 | (a 6th descriptive case, object-gate related) | dropped — object-gate is exercised implicitly by `pc-no-plan-drafts-first` |
| DI (no evals.json) | — | 4 new cases seeded from this session's own drafting, no old case to convert |

New, no old equivalent: `di-negative-plan-critique`, `di-fallback-no-picker`, `pc-review-my-plan-single-gate`, `pc-pressure-destructive`, `pc-fallback-missing-yardstick`, `pc-negative-rejected-delivery` — close decision-interview-2/-3, plan-critique-3/-4/-6/-7/-8.

### 4.3 Live triggers

Family (§6.3): `{intent-lock, decision-interview, plan-critique, misread-capture}` — S12 builds/runs the query set (I17). Near-miss queries contributed: "what you need from me" with a plan attached (plan-critique's, not decision-interview's); "review my plan" with a plan in view (plan-critique's — must not also fire intent-lock); "resolve all decisions" mid-task with no plan artifact (decision-interview's, not plan-critique's).

### 4.4 Commands

- Smoke: `bash scripts/eval.sh --smoke alignment` (§6.6) — smoke-tagged cases run with `--ablation none --runs 1`.
- Release: `bash scripts/eval.sh --release alignment` — two arms, `--runs 3`, all 10 cases here plus S01's 9. `scripts/eval.sh` (owner S12) grants only Read/Glob/Grep/Skill by default; none of the 10 cases above requests more, so no `--allow-tools` flag is needed here (factcheck F3).
- This session's own check: the drafted case tree (in `tmp/S02/evalout/`) was rendered and spot-checked against `eval-format.md`'s key sets; every case has ≥1 outcome and ≥1 process grader.

## 5. Acceptance criteria

1. `claude plugin validate --strict plugins/alignment` → passes (all 6 skills present, incl. S01's).
2. `grep -rc "single_select\|multi_select\|rank_priorities" …decision-interview/SKILL.md` → `0`.
3. `grep -rc "Reframed:" …plan-critique/SKILL.md` → `0`.
4. `measure.py skill …decision-interview/SKILL.md` → `yaml_valid: true`, `description.chars` ≤ 600.
5. `measure.py skill …plan-critique/SKILL.md` → `yaml_valid: true`, `description.chars` ≤ 600.
6. `grep -c "^## Contents" …plan-critique/references/critique-lenses.md` → `1`.
7. `ls plugins/alignment/evals/decision-interview | wc -l` → `4`; `.../plan-critique` → `6`.
8. No `plugins/decision-interview/` or `plugins/plan-critique/` directory remains; no `evals.json` anywhere under `plugins/alignment`.
9. `grep -c "intent-lock:intent-lock\|alignment:intent-lock" …plan-critique/SKILL.md` → ≥1 at W2, and the `alignment:` form only after W3.
10. `grep -c "^### decision-interview\|^### plan-critique" plugins/alignment/README.md` → `2`.

## 6. Trigger lock

All 15 phrases kept verbatim; none removed, none added.

| Skill | Phrases |
|---|---|
| `decision-interview` | "resolve all decisions", "ask me everything at once", "batch your questions", "what do you need from me", "collect your questions", "ถามมาทีเดียวให้ครบ" |
| `plan-critique` | "critique this plan", "review my plan", "improve this plan", "วิจารณ์แผน", "ช่วยปรับแผนให้ดีขึ้น", "find weaknesses in my plan", "poke holes in my plan", "stress-test my plan", "is this plan any good" |

## 7. Risks and OD sensitivity

- **K7** (a description edit drops/shifts a trigger): mitigated by §6; live routing smoke (§6.3) re-tests the family with S01.
- **plan-critique's 2,432-tok body misses the 2,000-tok warning** (R11 soft target for gates): the mega-bullet split (§2.3) is the main lever already taken; a further cut would need to drop a worked example from Step 4 or Step 5 — not done here because the examples are what makes the numbered end-condition list checkable in review. Flagged for S12/S08's context-budget pass rather than cut blind.
- **K18** (the W3 skeleton PR is large): all W3 steps here depend on it landing first; W2-1 is independent (a same-repo, in-place edit) and closes plan-critique-2's worst gap on schedule regardless.
- **OD9 alt (b/c: no aliases, or rename to the verbs)**: the two dmi alias files in §2.2 would not exist; `/resolve-decisions` and `/critique-plan` would break for the owner's own muscle memory (b), or the skill names themselves would change, touching every eval and trigger-lock row here (c). Not built (OD9-a assumed, per architecture).

## 8. Open questions

- **Q1** (I01/I03, S01): does S01's `lock-record.md` keep intent-lock's `Not for` naming plan-critique, and does misread-capture's `Not for` add the reciprocal entry? This spec's `pc-review-my-plan-single-gate` case and S01's `negative-review-my-plan` case are a matched pair testing the same boundary from both sides — S01 to confirm they agree.
- **Q2** (I02, S01): does the protocol let plan-critique keep "explicit stop → `[OPEN]` markers" as a stated difference, given an S01 draft finishes a stop "under the fallback"? If not, `pc-pressure-destructive`'s `[OPEN` grader needs revision.
- **Q3** (I17, S12): confirm case names need only be unique per plugin (this spec uses `di-`/`pc-` prefixes on that assumption) and that no `release`-only tag convention is expected beyond what's used here.
- **Q4 — CLOSED (CX-18).** S08 §2.7 I20 now allows `argument-hint` on any user-typeable skill and exempts dmi alias skills from the order rules. Original question: (I20, S08) confirm the frontmatter whitelist covers `argument-hint`/`disable-model-invocation`/`metadata` as used in §2.2's alias skills.
- **Q5 — CLOSED (CX-1).** S10-W3-2 creates the alias skills with this spec's §2.2 text verbatim and moves the skill bodies unchanged. Original question: (I23, S10) confirm the skeleton PR's exact alias-creation step uses this spec's §2.2 text verbatim, and that it does not also rewrite `intent-lock:intent-lock` inside the moved skill bodies (S02-W2-1's edit should survive the move unchanged until S02-W3-2/-3 replace it).
- `ARCH-CONFLICT:` none found — every re-opened evidence line in §1.3 matched the digest's citation exactly (no line-number corrections needed here, unlike S01's two README slips).
