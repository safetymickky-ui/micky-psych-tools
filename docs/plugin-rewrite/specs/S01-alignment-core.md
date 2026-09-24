# Spec S01: alignment family shell, intent-lock and misread-capture

| Field | Value |
|---|---|
| Repos | micky-psych-tools |
| Units (today → target) | `plugins/intent-lock` (skills `intent-lock`, `misread-capture`) → `plugins/alignment`: those 2 skills (this spec); `decision-interview`/`plan-critique`/their dmi aliases are S02's. Owns the family shell: `references/{interview-protocol,lock-record}.md`, `scripts/{ledger,test_ledger}.py`, `.claude-plugin/plugin.json`, `README.md`, `CHANGELOG.md`, `LICENSE` for the whole `alignment` plugin, and repo-root `state/misreads.md`. |
| Waves | W2 (interim lock record + single `Assumed:` line, so W2 callers can conform — H05); W3, after S10's skeleton PR (subtraction rewrite, `interview-protocol.md`, `lock-record.md`'s final home, `ledger.py`, `state/misreads.md`, family plugin.json/README/CHANGELOG/LICENSE) |
| Owner decisions assumed | OD3-a (merge into families), OD6-a (git-tracked `state/`, commit offered) |
| Defects closed | 16 of 16 assigned (HIGH: intent-lock-1..5) |
| Interfaces owned | I01, I02, I03 |
| Interfaces consumed | I16 (S11), I17 (S12), I20 (S08), I23 (S10) |
| Depends on specs | S10 (W3 skeleton PR moves `plugins/intent-lock/*` unchanged before W3 steps here); S08 (I20 template); S11 (I16 schedule); S12 (I17 layout) |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| Path | Lines | Est. tokens | Role |
|---|---|---|---|
| `.claude-plugin/plugin.json` | 16 | 113 | plugin manifest, v0.4.2 |
| `README.md` | 43 | 654 | install + design commitments |
| `CHANGELOG.md` | 64 | 1,486 | version history (0.4.2 skips 0.4.1) |
| `skills/intent-lock/SKILL.md` | 249 | 6,458 (body 6,192) | the interview gate |
| `skills/intent-lock/references/failure-conditions.md` | 29 | 668 | full failure-condition list |
| `skills/intent-lock/references/misreads.md` | 47 | 606 | the ledger (2 entries, 2 active priors) |
| `skills/intent-lock/evals/evals.json` | 69 | 1,155 | 8 descriptive cases, `assertions: []` |
| `skills/misread-capture/SKILL.md` | 69 | 1,225 (body 1,017) | the capture skill |
| `skills/misread-capture/evals/evals.json` | 45 | 691 | 5 descriptive cases, `assertions: []` |

No per-skill `README.md`/`CHANGELOG.md`/`evals/` today — one plugin-level copy covers both, kept (a family plugin, T3).

### 1.2 Descriptions

| Skill | Chars | UTF-8 bytes | YAML valid? | `Use when` at | `Not for`? | 8 quoted trigger phrases |
|---|---|---|---|---|---|---|
| `intent-lock` | 1,020 | 1,082 | **No** — `yaml.safe_load` fails `mapping values are not allowed here` (unquoted `description:` scalar; `claude plugin validate --strict`/`validate.py` both accept it — OBS, confirmed) | 86 | yes (procedure names, not `<plugin:skill>` form) | listed in §6 |
| `misread-capture` | 789 | 873 | yes | 398 | yes | listed in §6 |

### 1.3 Defects

Evidence re-opened, confirmed this session unless marked **NEW** (a digest line-number correction).

| id | sev | H# | evidence (path:line) | problem | fix step | wave |
|---|---|---|---|---|---|---|
| intent-lock-1 | H | H01 | SKILL.md:16,22,49,93,155,193 (+11 more, full list confirmed) | silent-output contract contradicted ≥11× | S01-W3-2: subtraction rewrite; no "reinterpret" patch | W3 |
| intent-lock-2 | H | H02 | SKILL.md:136,160-162,189-190 | claude.ai picker names; no absent/error fallback | S01-W3-1, S01-W3-2: protocol §4 (picker) + §6-7 (fallback) | W3 |
| intent-lock-3 | H | H03 | misread-capture SKILL.md:39 | ledger under `${CLAUDE_PLUGIN_ROOT}`, cache-replaced | S01-W3-3, S01-W3-4: `ledger.py` writes `$MICKY_TOOLS_DIR/state/misreads.md` | W3 (interim path W2, §8) |
| intent-lock-4 | H | H04 | misread-capture SKILL.md:26,30-31,33,35,47,50,55 | `Prior:` has no eliciting question; forbidden 3rd Q | S01-W3-3: rewritten Q1 → `Axis missed`, Q2 → `Prior`, exactly two | W3 |
| intent-lock-5 | H | H05 | intent-lock SKILL.md:226; pubmed SKILL.md:264-265; CR SKILL.md:147-148 | callers still expect `Reframed:`/`Skipped:`, removed at 0.3.0 | S01-W2-1 (interim), S01-W3-1 (final): `lock-record.md`'s single `Assumed:` line only (I01) | W2 interim, W3 final |
| intent-lock-6 | M | — | SKILL.md:183,207 vs :220-223 | `[UNTESTED]` in a 4-field preface, or one line — contradicts | S01-W3-2: subtraction removes stale wording | W3 |
| intent-lock-7 | M | — | SKILL.md:179 vs :193 vs :155; README.md:38 | loop guard disjunct can't fire on a "dies twice" revision | S01-W3-1, S01-W3-2: dropped; protocol §9, no disjunct | W3 |
| intent-lock-8 | M | — | SKILL.md:3 vs :247; misreads.md:47 | "craft my prompt" triggers, but a prompt is a failure condition | S01-W3-2: rule 3 — a prompt is the work when named deliverable | W3 |
| intent-lock-9 | M | — | misreads.md:34 vs 46-47,58,65; SKILL.md:39 vs misreads.md:53,60 | ledger contradicts both skills' rules (person, order, drop) | S01-W3-3: `ledger.py` — user's words, newest first, no silent drop | W3 |
| intent-lock-10 | M | — | SKILL.md:3 | "review/edit priors" promised, no procedure | S01-W3-3: new "Review, edit, retire" via `ledger.py list`/`retire` | W3 |
| intent-lock-11 | M | — | SKILL.md:24,95,99,101,146,179,210 | version-history narration, 6.2k-tok body, 5+ loaders | S01-W3-2: deleted, no replacement | W3 |
| intent-lock-12 | M | — | SKILL.md:3, 1,020/1,024 chars; YAML-invalid (§1.2) | description 4 chars from cap, spent on jargon | S01-W3-2: new description, 600 chars (§2.2) | W3 |
| intent-lock-13 | L | — | failure-conditions.md:3,11,12 | stale post-0.3.0; one unmeasurable condition | S01-W3-2: file deleted; short body section replaces it | W3 |
| intent-lock-14 | L | — | SKILL.md:73-77,168 vs :22,220 | ambiguous if sub-threshold defaults are ever stated | S01-W3-1, S01-W3-2: protocol §1 — below threshold, no question, no line | W3 |
| intent-lock-15 | L | — | CHANGELOG skips 0.4.1 (MEMORY.md:402); README:**34** `<owner>` (digest :49 — **NEW**); README:**14** stale claim (digest :27 — **NEW**) | missing entry; placeholder; stale claim | S01-W3-5: CHANGELOG backfills 0.4.1; README replaces both | W3 |
| intent-lock-16 | L | — | both `evals.json`: `"assertions": []` | descriptive only, no runner | S01-W3-6: 9 cases, real graders (§4); `evals.json` deleted | W3 |

### 1.4 Other findings

- OBS (NEW): `intent-lock/SKILL.md`'s frontmatter fails strict YAML though the CLI/`validate.py` accept it — the rewrite keeps a `>-` quoted description so a stricter parser doesn't reject it.
- OBS (H06, not among the 16 — coordination only): the learn-hub fork is byte-identical to micky's copy incl. `misreads.md` (diffed this session; only the README differs). S14's W2 merge target is in I03/§8.
- OBS: MEMORY.md records repeated real-world picker-absent fallback use with no written path today — the evidence behind intent-lock-2, covered by protocol §6-7 and the `fallback-no-picker`/`pressure-hurry-authority-sunk-cost` cases.
- OBS: `intent-lock-pairing.md` (pubmed, not this unit) still describes a forbidden "reframe" step — S03 aligns it against I01.
- NEW: both `evals.json` files' prompts were read in full and reused as seeds (§4.2, "mined, not converted").

## 2. Target state

### 2.1 Location and tree (after W3)

```
plugins/alignment/
  .claude-plugin/plugin.json · README.md · CHANGELOG.md · LICENSE          (all this spec)
  references/{interview-protocol,lock-record}.md                          (this spec)
  scripts/{ledger,test_ledger}.py                                         (this spec)
  skills/
    intent-lock/SKILL.md · misread-capture/SKILL.md                       (this spec)
    decision-interview/SKILL.md · plan-critique/SKILL.md                  (S02)
    critique-plan/SKILL.md · resolve-decisions/SKILL.md (dmi aliases)     (S02)
  evals/
    intent-lock/<5 cases>/ · misread-capture/<4 cases>/                   (this spec)
    decision-interview/<case>/ · plan-critique/<case>/                    (S02)
state/misreads.md (repo root)                                             (this spec)
```

No `references/failure-conditions.md`, no per-skill `evals.json` — both deleted (R70).

### 2.2 Frontmatter

**`intent-lock`** (`metadata.profile: cc` per OD13; `allowed-tools` narrowed per R36):

```yaml
---
name: intent-lock
description: >-
  Questions a request until it has exactly one reading, then does the work as asked.
  Use when the user says "interview me", "ask me until you understand", "make sure you
  don't misunderstand", "lock the goal", "craft my prompt", "what do I actually want",
  "ถามจนกว่าจะเข้าใจ", "ล็อคเป้าหมาย", or unprompted when a wrong reading of an
  expensive, reusable or ambiguous request would waste real work. Not for precise or
  throwaway requests, mid-task forks (use alignment:decision-interview), critiquing a
  plan (use alignment:plan-critique), or a misread found after delivery (use
  alignment:misread-capture).
argument-hint: "[request to lock]"
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/ledger.py *)
metadata:
  profile: cc
---
```

Measured: 600 chars / 658 UTF-8 bytes (§1.2's 1,020/1,082 today); `yaml.safe_load` succeeds. All 8 trigger phrases kept verbatim (§6). Capability clause ends and `Use when` begins at char 61 (was 86).

**`misread-capture`**:

```yaml
---
name: misread-capture
description: >-
  Records, in the user's own words, how delivered work missed their intent, as a check
  that intent-lock runs before its next interview. Use when the user signals that
  delivered work missed: "this isn't what I wanted", "you misunderstood", "that's not
  it", "I asked for X and got Y", "you wasted my time", "ไม่ใช่ที่ผมต้องการ",
  "เข้าใจผิด", "ไม่ใช่แบบนี้", or asks to review, edit or retire misread priors. Not for
  a correction during a live interview (use alignment:intent-lock), a mid-task decision
  (use alignment:decision-interview), or improving a plan the user wrote (use
  alignment:plan-critique).
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/ledger.py *)
metadata:
  profile: cc
---
```

Measured: 599 chars / 677 UTF-8 bytes (§1.2's 789/873 today). All 8 phrases kept verbatim.

### 2.3 Body outline

**`intent-lock`** — target 85 lines / 1,965 tokens (gate target ≤2,000, R11):

| Target section | Source lines | Disposition (fix) |
|---|---|---|
| Standing rules (5) | :14-24,26-39,142-171,189-190 | **new**, condensed; rule 2 = output contract (H01); rule 4 → protocol instead of restating picker mechanics (H02) |
| Phase 0 — Cold read | :41-95 | **cut** ledger/prediction/threshold prose → **script** (protocol §1); **keep** 4 moves as one-liners (H01, H14) |
| Phase 1 — Rounds | :97-196 | **cut** dimension framing, tool contract (→ protocol §4), probe/loop-guard essays (H01, H02, H07 disjunct dropped) |
| Phase 2 — Gates | :198-214 | **cut** essay → **keep** 3 gates, one line each (H01, H06) |
| Phase 3 — Lock, hand back | :216-228 | **cut** essay → **keep**: read `lock-record.md`, `Assumed:` if material, hand back; forks → decision-interview (H05, H08) |
| Phase 4 — Rejected work | :230-236 | **keep**, shortened; routes to misread-capture |
| Failure conditions | :238-249 + ref file | **cut** stale entries → **keep** 5 inline; ref file deleted (H13, H16) |
| Gotchas | none today | **new**: picker-failure history, misreads as ledger pointers, the plan-review collision (S02) |
| Version-history prose | :24,95,99,101,146,179,210 | **delete** (H11); CHANGELOG only |

**`misread-capture`** — target 58 lines / 1,132 tokens:

| Target section | Source lines | Disposition (fix) |
|---|---|---|
| Standing rules (4) | :12-22,24-26 | **new**; rule 1 keeps the prohibition; rule 4 new: write only through `ledger.py` (H03) |
| Capture | :24-35 | **cut** essay → **keep** Q1 "what did you want instead", Q2 "check next time" (H04) |
| Write | :37-50 | **script**: `ledger.py append --write`, named flags; grammar shown once, illustrative (H03, H09) |
| entry-grammar fence | :41-48 | **keep**, unchanged, illustrative |
| Review, edit, retire | not implemented today | **new**: `ledger.py list` then `retire --prior <n> --write` (H10) |
| Gotchas | :57-63 | **cut** to 2 lines: ledger history; only the user rewords a prior |

### 2.4 References

| File | Purpose | Load condition | Size target |
|---|---|---|---|
| `references/interview-protocol.md` | Threshold, destructive-always-ask, AskUserQuestion mechanics, stop, silence rule, fallback, push-once, two-empty-rounds | intent-lock standing rule 4: "before asking, or taking the fallback, read this"; decision-interview/plan-critique load it the same way (S02) | ≤1,500 tok — measured **770**, 30 lines |
| `references/lock-record.md` | The slots intent-lock returns; the `Assumed:` hand-back; the Handoff sentence | intent-lock Phase 3, only if it ran as Step 0 or will print `Assumed:`; callers read it once for the Handoff sentence | no target set — measured **730** tok, 37 lines |

### 2.5 Scripts

**`scripts/ledger.py`** (305 lines, 3,063 est. tokens; tests in `test_ledger.py`, 198 lines, 17 cases, all pass — run this session):

| Command | Flags | Writes | JSON stdout | Exit codes |
|---|---|---|---|---|
| `list [--active] [--ledger PATH]` | `--active`: priors only | none | `{ok, ledger, cap:7, active_count, over_cap, active:[{n,prior,entry,verbatim}], entries?, warnings}` | 0 ok; 3 not found; 4 malformed |
| `append --title T [--date --asked --got --axis --tell --prior --create --write]` | dry run unless `--write` | new `## date · title` block at top of Entries; `Prior` (if non-blank) as active prior 1, renumbered | `{ok, written, ledger, entry, prior_added, active_count, over_cap, retire_candidates:[{n,prior}]}` | 0; 2 usage; 3 not found; 4 bad title/date |
| `retire --prior N [--date --write]` | dry run unless `--write` | deletes active line N; stamps `Retired: <date>` on the matching entry's `Prior:` line if found | `{ok, written, ledger, retired:{n,prior,entry}, active_count, warnings}` | 0; 2 usage; 3 not found; 4 out of range |

`resolve()`: explicit `--ledger` wins, else `$MICKY_TOOLS_DIR/state/misreads.md` validated against the marketplace-name marker (exit 3 otherwise). Writes atomic (`mkstemp`+`os.replace`), CRLF→LF, Thai/UTF-8 preserved verbatim (tested). `--help` has no side effects (tested).

### 2.6 Handoffs

The two exact Handoff sentences (I01) are defined once, in §2.7 I01's "Handoff" subsection — S02–S06, S09, S16 copy them verbatim. At W2, callers restate the intent-lock sentence against today's name `intent-lock` and the interim `plugins/intent-lock/references/lock-record.md`; at W3, after S10's skeleton PR, only the plugin-name segment changes, to `alignment:intent-lock`.

### 2.7 Interfaces

#### I01 — Lock record (owned)

`references/lock-record.md` (full text):

```markdown
# Lock record (alignment family)

What `intent-lock` has settled when its interview ends. Stays in the conversation, never printed. This plugin's skills read this file; other-plugin callers restate only §Handoff.

## Slots

| Slot | Holds | Settled by |
|---|---|---|
| `deliverable` | Kind, format, length, location; for a decision report, the verdict's shape | output contract |
| `question` | The instruction in the user's vocabulary, every fork resolved | gate 3 |
| `scope_in`/`scope_out` | Covered / explicitly out | scope boundary |
| `emphasis` | Where the depth goes | goal-behind-goal, success criteria |
| `audience` | Who reads it, register | output contract |
| `exclusions` | The anti-goal + 3 things the work won't do | anti-goal; gate 2 |
| `assumed_defaults` | Items decided without the user (sub-threshold, stop/fallback, untested prediction), each material or not | Phase 0, Exit, fallback |

A slot the request doesn't need holds `n/a`; an unsettled slot holds its default and is listed in `assumed_defaults`. A consumer reads only the slots it needs and never re-asks a settled one.

## The hand-back line

At least one material `assumed_defaults` item → the output opens with exactly one line:

    Assumed: <reading> — say if wrong.

`<reading>` names each material item in plain words, `;`-separated, in the user's language, including any untested prediction line and any surprising `scope_out` item; `Assumed:`/`— say if wrong.` stay in English (tools and graders match on them). First body line, under the title/date. No material item → no line. Never print `Reframed:`, `Skipped:`, `Untested:`, `Resolved:`, `Default:`, a multi-line preface, or the slots themselves.

## Handoff

Callers in other plugins carry this sentence verbatim as Step 0 — the only intent-lock text they restate:

> Run `alignment:intent-lock` (OPTIONAL). If it is not available in this session — or it needs an interactive picker and none exists here (subagent, headless, scheduled run) — do not stall: take the broadest reading that fits the request and open the output with one line `Assumed: <reading> — say if wrong.`

A caller's own opt-out (e.g. "just search") still opens with the line if it took a material default. When intent-lock ran, control returns to the caller's next step in the same turn — nobody asks "shall I proceed".

A caller handing a rejected delivery to misread-capture carries this sentence verbatim:

> Run `alignment:misread-capture` (OPTIONAL). If it is not available in this session, do not defend or explain the work: ask what the user wanted instead and what to check next time before starting, and quote both answers in your reply.

A caller that ships before the W3 rename lands may carry the bare skill name (`intent-lock`, `misread-capture`) in place of `alignment:intent-lock`/`alignment:misread-capture` in either sentence above; both forms resolve to the same skill and neither is an error.
```

#### I02 — Interview protocol (owned)

`references/interview-protocol.md` (full text):

```markdown
# Interview protocol (alignment family)

Shared rules for `intent-lock`, `decision-interview` and `plan-critique`. Each skill states only where it differs.

## 1. Admission threshold
An unknown earns a question only if the competing answers produce materially different work (different structure, deliverable, sources, or >~1/5 of total effort). Below that: take a default, don't ask, never promote a preference to a question.

## 2. Already answered
Conversation, files, code, repo conventions or stated preferences settling an item settle it there, named. Never make the user repeat themselves.

## 3. Destructive, irreversible or outward-facing steps
Delete, overwrite, publish, send, spend, force-push, sign: always earns a question, any size. Only the user's explicit choice in-conversation settles one — never a default, an assumption or an earlier gate. Never defaulted, not even in the fallback (§7).

## 4. Asking: the AskUserQuestion tool
Every question through the tool, never prose. One call/round, 1–4 questions, 2–4 options each. Caps: intent-lock 3/round (past three, the user answers the easy ones and drops the rest); siblings 4 (tool ceiling). Question text = the open question, in the user's words; options = candidate answers. `multiSelect: true` when several can hold at once, else single-select. The tool's own free-text "Other" is the only escape. Options are concrete outcomes, never "Option B". Siblings lead with "(Recommended)" + reason; intent-lock never recommends (its options are readings of the user). A question that creates/removes others goes first.

## 5. Stop
`LOCK` / "stop" / "stop asking", any wording or language: ends the interview at once, mid-round, unargued. Don't ask what they meant. A stop is the verdict; silence (§6) is not. Each skill states what a stop leaves behind.

## 6. The silence rule
A rejected, unavailable or errored picker routes to the fallback (§7): a subagent/headless/scheduled run with no AskUserQuestion; a tool error (transport error, closed permission stream); a dismissed question. Don't retry the picker that round, don't re-ask in prose, don't wait.

## 7. Autonomous fallback
Reversible items take a default (intent-lock: broadest reading; siblings: recommended option), surfaced in one line (intent-lock `Assumed: …`; siblings `Decided without you:` + one-line reasons). Destructive/irreversible/outward-facing items are never defaulted — stop that thread, deliver a written decision request (decision, options, recommendation, reason); finish everything else.

## 8. Push once
An answer that would defeat the user's own stated goal: name both sides once, with the reason, never as a counter-proposal. If they hold, record and go on.

## 9. Two empty rounds
Two consecutive rounds resolving no item end the interview (intent-lock: and no prediction-line change). Residue follows §7. "Keep asking" does not override this — more rounds can't resolve what two empty ones didn't.
```

#### I03 — Misread ledger (owned)

- **Entry grammar** (written only by `ledger.py append`): `## YYYY-MM-DD · <title, ≤60 chars>` then `Asked for:`/`Got:`/`Axis missed:`/`Tell arrived:`/`Prior:`, each padded to a 14-char label column. `Axis missed`/`Prior` are the user's words, verbatim or blank; the rest are facts Claude may state.
- **Ordering/cap**: entries newest-first under `## Entries`; active priors newest-first under `## Active priors`, numbered, each the verbatim `Prior:` text. Cap 7 — over cap, `append` returns the 3 oldest as `retire_candidates`; nothing retires without the user's choice.
- **CLI**: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/ledger.py {list|append|retire}` — full definition in §2.5.
- **Path**: `$MICKY_TOOLS_DIR/state/misreads.md` from W3. **Pre-W3 path** (S14's W2 fork-merge target): `plugins/intent-lock/skills/intent-lock/references/misreads.md` — confirmed byte-identical to the learn-hub fork's copy this session, so that merge is diff-and-confirm unless the fork gained an entry since.
- **Commit offer**: `git -C "$MICKY_TOOLS_DIR" commit -m "chore(state): record misread <date> <title>" -- state/misreads.md` after every append; pushes only if asked (OD6-a).

### Interfaces consumed

- **I16 (S11).** ASSUMES: `alignment` is absent from `CLAUDE_CODE_PLUGIN_DIRS` before W3 entry (§2.7's "four not yet enabled"); W3 here runs after S11's folder-path edit lands.
- **I17 (S12).** ASSUMES: the case layout and `tool_used: Skill` regex in `eval-format.md` are stable; this spec's 9 cases use that layout now.
- **I20 (S08).** ASSUMES: S02's dmi-alias template is unchanged by the time S08 lands it; this spec's own skills aren't aliases.
- **I23 (S10).** ASSUMES: the skeleton PR moves `plugins/intent-lock/**` to `plugins/alignment/skills/{intent-lock,misread-capture}/**` unchanged, deleting the old dir + the fork in one commit; W3 here begins from the moved tree.

## 3. Change steps

### Wave 2

**S01-W2-1** — micky-psych-tools · depends on: none
- Files: create `plugins/intent-lock/references/lock-record.md` (content = §2.7 I01), in place, ahead of the family move.
- Change: land the interim contract (slots, `Assumed:` line, both Handoff sentences) so S03/S04/S05/S06/S09/S16 can conform against today's plugin name `intent-lock`. No `SKILL.md` edit: Phase 3 already implements the single line (§1.1) — only callers are stale.
- Commands/Done when: `wc -l …lock-record.md` → 37; `grep -c "^> Run" …` → 2.
- Rollback: `git rm plugins/intent-lock/references/lock-record.md`.

**S01-W2-2** — DROPPED (OQ12-a): Windows loads plugins in place from W1 entry (S11-W3-2), so this interim version bump is not needed; the change steps write their CHANGELOG entries under `## Unreleased`, and `release.py` sets the version once at W3. micky-psych-tools · depends on: S01-W2-1
- Change: release the W2-1 fix — `python3 scripts/bump.py intent-lock patch --write`.
- Files: `plugins/intent-lock/.claude-plugin/plugin.json`, `plugins/intent-lock/CHANGELOG.md` (entry: "Interim lock record: single `Assumed:` line, both Handoff sentences (H05 interim fix)."). `.claude-plugin/marketplace.json` is not touched: S10-W0-3 removed every entry `version` (I18, CX-12).
- Done when: `python3 scripts/validate.py` prints `all checks passed`; `marketplace.json` has no `version` key for this entry.
- Rollback: `git checkout -- plugins/intent-lock/.claude-plugin/plugin.json plugins/intent-lock/CHANGELOG.md`.

### Wave 3 (repo: micky-psych-tools for every step below; after S10's skeleton PR moves `plugins/intent-lock/*` → `plugins/alignment/skills/{intent-lock,misread-capture}/*` unchanged)

**S01-W3-1** — depends on: S10-W3-2. Create `plugins/alignment/references/interview-protocol.md` (content = §2.7 I02); confirm `plugins/alignment/references/lock-record.md` arrived from S10's move and replace every `intent-lock:intent-lock` in it with `alignment:intent-lock`. Done when: `wc -l …interview-protocol.md` → 30 and both skills' bodies link it; `grep -c "intent-lock:intent-lock" plugins/alignment/references/lock-record.md` → 0. Rollback: `git rm interview-protocol.md`; `git checkout -- plugins/alignment/references/lock-record.md`.

**S01-W3-2** — depends on: S01-W3-1, S12-W3-2. Rewrite `…/intent-lock/SKILL.md` per §2.2/§2.3 (subtraction, no "reinterpret" patch); delete `references/failure-conditions.md` only (`references/misreads.md` already moved to `state/misreads.md` by S10-W3-2 — S01-W3-4 reformats it there; never delete it here). Done when: `grep -c "Reframed:\|Skipped:\|GOAL UNIFIED\|single_select\|multi_select\|rank_priorities" …` → 0 and `measure.py skill …` shows body ≤2,000 tok, `yaml_valid: true`; `test -f …/intent-lock/references/misreads.md` fails (only `state/misreads.md` exists). Rollback: `git checkout HEAD~1 -- …SKILL.md`.

**S01-W3-3** — depends on: S01-W3-1. Rewrite `…/misread-capture/SKILL.md` per §2.3; create `scripts/{ledger,test_ledger}.py`. Done when: `python3 -m unittest discover -s plugins/alignment/scripts -p 'test_*.py'` → 17 `OK`, `grep -c "references/misreads.md" …SKILL.md` → 0. Rollback: `git checkout -- …SKILL.md`; `git rm plugins/alignment/scripts/{ledger,test_ledger}.py`.

**S01-W3-4** — depends on: S01-W2-1, S14-W2-2, S10-W3-2, S01-W3-3 (the done-when runs `ledger.py`, which S01-W3-3 creates). Reformat the `state/misreads.md` that S10-W3-2 already moved there (from `plugins/intent-lock/skills/intent-lock/references/misreads.md`) to the I03 grammar (§2.7); confirm it still holds the 2 existing entries/priors, byte-identical to the fork per S14-W2-2's merge (§1.4), not re-derived. Done when: `MICKY_TOOLS_DIR=$(pwd) python3 plugins/alignment/scripts/ledger.py list` → `active_count: 2`, `warnings: []`. Rollback: `git checkout -- state/misreads.md`.

**S01-W3-5** — depends on: S01-W3-2, S01-W3-3, S02-W3-2, S02-W3-3. Edit (not create — S10-W3-2 already created the family shell) `plugin.json` (fields only; no hand-set version — released via `release.py alignment minor --write` after S08-W3-1 lands), `README.md` (4-skill table + shared files + ledger + where-it-runs, plus a `## Surfaces` section naming every place this family's summary appears, per I16 item 1), `CHANGELOG.md` (one entry citing closed HIGH ids; S01-W3-7's `release.py` writes the version heading), `LICENSE` (MIT, only if S10-W0-8 hasn't already backfilled one). Done when: `claude plugin validate --strict plugins/alignment` passes; `grep -c "^## Surfaces" README.md` → 1. (The version check moved to S01-W3-7.) Rollback: `git checkout -- plugin.json README.md CHANGELOG.md LICENSE`.

**S01-W3-6** — depends on: S01-W3-2, S01-W3-3. Write the 9 eval cases (§4) under `evals/{intent-lock/<5 dirs>,misread-capture/<4 dirs>}/`; delete old `evals.json` if S10 didn't already. Wave exit: note, per S11's I16 item 4 template: "Ready for cloud delivery: HIGH defects due by this wave closed (H01, H02, H03, H04, H05); handoffs carry the §4.2 fallback or target an enabled plugin; no same-named unit elsewhere; smoke suite passed (<result path>)." Done when: 9 dirs exist, each ≥1 outcome + ≥1 process grader, none `smoke`-tagged carries `llm`/`baseline`. Rollback: `git rm -r` both eval dirs.

**S01-W3-7 (new, critique P5)** — depends on: S08-W3-1 (`release.py`), S01-W3-5, S01-W3-6, S02-W3-1, S02-W3-4. Release the alignment family after its W3 rewrite: `python3 plugins/plugin-creator/scripts/release.py alignment minor --write`. Files: `plugins/alignment/.claude-plugin/plugin.json`, `plugins/alignment/CHANGELOG.md`. Done when: `python3 plugins/plugin-creator/scripts/validate.py --repo .` prints `all checks passed`; the first `## ` line of `plugins/alignment/CHANGELOG.md` names the version in `plugin.json` (R85); `marketplace.json` has no `version` key for `alignment`. Rollback: `git revert <this commit>`.

## 4. Evals

### 4.1 Cases

9 cases (5 intent-lock, 4 misread-capture). Full contents for 3/skill (trigger positive, near-miss negative, and — both gate-shaped per §6.2 — intent-lock's picker-absent fallback / misread-capture's `context.history_file` output case). Other 3 tabled after.

### Shared grader files (write once; compact flow-YAML frontmatter is still each file's full content)

- `skill-fired-il.md`: `---\n{type: tool_used, tool: Skill, input_match: '"skill"\s*:\s*"(?:[\w-]+:)?intent-lock"'}\n---`
- `skill-fired-mc.md`: `---\n{type: tool_used, tool: Skill, input_match: '"skill"\s*:\s*"(?:[\w-]+:)?misread-capture"'}\n---`
- `intent-lock-not-fired.md`: `---\n{type: tool_used, tool: Skill, input_match: '"skill"\s*:\s*"(?:[\w-]+:)?intent-lock"', min: 0, max: 0, arm: both, weight: 3}\n---`
- `no-entry.md`: `---\n{type: regex, target: last_message, pattern: '^\s*#{2} \d{4}-\d{2}-\d{2} · ', flags: m, match: not_contains}\n---`
- `no-assumed-line.md`: `---\n{type: regex, target: last_message, pattern: '^\s*(?:>\s*)?\**Assumed:', flags: m, match: not_contains}\n---`
- `one-assumed-line.md`: `---\n{type: regex, target: last_message, pattern: '^\s*(?:>\s*)?\**Assumed:', flags: m, match: "count:1", weight: 2}\n---`
- `no-machinery.md`: `---\n{type: regex, target: last_message, pattern: 'GOAL UNIFIED|Reframed:|Skipped:|\[OPEN\]|\[ASSUMED\]|\[UNTESTED\]|convergence gate', flags: i, match: not_contains}\n---`

### Case `intent-lock/trigger-thai-lock-goal` (trigger positive)

`prompt.md`:
```
---
name: intent-lock-trigger-thai-lock-goal
tags: [intent-lock, trigger, smoke]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

ล็อคเป้าหมายก่อนนะ ผมอยากได้ระบบแจ้งเตือนสำหรับแอปคลินิก
```
Graders: `skill-fired-il.md`, `one-assumed-line.md`, `no-machinery.md`.

### Case `intent-lock/negative-review-my-plan` (near-miss negative)

`prompt.md`:
```
---
name: intent-lock-negative-review-my-plan
tags: [intent-lock, negative, smoke]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

Review my plan for moving our clinic's notes to the new EHR: 1) export the last five years of notes, 2) map the old fields to the new ones, 3) import everything over one weekend, 4) switch the old system off on Monday. What's weak in it?
```
Graders: `intent-lock-not-fired.md`, `no-assumed-line.md`. Direct test for the intent-lock-8 / plan-critique-7 collision (S02): the "review a topic" prior must not fire on a plan review (boundary in `intent-lock/SKILL.md`'s Gotchas, §2.3).

### Case `intent-lock/fallback-no-picker` (gate: picker-absent fallback)

`prompt.md`:
```
---
name: intent-lock-fallback-no-picker
tags: [intent-lock, output, smoke]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

Interview me before you build this — I want the dashboard redesign spec locked down first.
```
Graders: `skill-fired-il.md`, `one-assumed-line.md`, `no-machinery.md`, and two case-local files —
`no-trailing-question.md`: `---\n{type: regex, target: last_message, pattern: '\?\s*$', match: not_contains}\n---`
`work-delivered.md`: `---\n{type: regex, target: last_message, pattern: '[\s\S]{1200,}'}\n---`
Exercises H02: no `AskUserQuestion` in the grant list, so the run passes only via protocol §7's fallback.

### Case `misread-capture/trigger-thai-complaint` (trigger positive)

`case.yaml`:
```yaml
schema_version: "1.1"
name: misread-capture-trigger-thai-complaint
tags: [misread-capture, trigger, smoke]
context: {history_file: history.jsonl}
```
`history.jsonl` (prior request + delivered output, so the complaint below has something to react to):
```
{"type": "user", "uuid": "u1", "parentUuid": null, "sessionId": "eval-misread-thai", "timestamp": "2026-09-20T09:01:00.000Z", "isSidechain": false, "userType": "external", "cwd": "/workspace", "version": "2.1.281", "message": {"role": "user", "content": "ช่วยเขียนเอกสารแจกผู้ป่วยเรื่องสุขอนามัยการนอนหลับ หนึ่งหน้า สำหรับคลินิกจิตเวชของเรา"}}
{"type": "assistant", "uuid": "u2", "parentUuid": "u1", "sessionId": "eval-misread-thai", "timestamp": "2026-09-20T09:02:00.000Z", "isSidechain": false, "userType": "external", "cwd": "/workspace", "version": "2.1.281", "message": {"id": "msg2", "type": "message", "role": "assistant", "model": "claude-opus-5-5", "content": [{"type": "text", "text": "# CBT-I สำหรับโรคนอนไม่หลับ\n\nสรุปหลักฐานสำหรับผู้ป่วย: CBT-I ลดเวลาก่อนหลับได้ประมาณ 19 นาที..."}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 200, "output_tokens": 300}}}
```
`prompt.md`:
```
---
max_turns: 10
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
---

ไม่ใช่ที่ผมต้องการ เสียเวลาไปเลย
```
Graders: `skill-fired-mc.md`, `intent-lock-not-fired.md`, `no-entry.md`.

### Case `misread-capture/negative-live-correction` (near-miss negative)

`prompt.md`:
```
---
name: misread-capture-negative-live-correction
tags: [misread-capture, negative, smoke]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

Wait — before you start on the migration, I meant the staging database, not production.
```
Graders: `no-entry.md`, and `misread-capture-not-fired.md`: `---\n{type: tool_used, tool: Skill, input_match: '"skill"\s*:\s*"(?:[\w-]+:)?misread-capture"', min: 0, max: 0, arm: both, weight: 3}\n---`

### Case `misread-capture/append-writes-ledger` (output/process, `context.history_file`)

`case.yaml`:
```yaml
schema_version: "1.1"
name: misread-capture-append-writes-ledger
tags: [misread-capture, output, release]
context: {scaffold_script: fixture.sh, history_file: history.jsonl}
```
`fixture.sh` (fake micky checkout: marker file + a two-prior ledger):
```bash
#!/usr/bin/env bash
set -euo pipefail
mkdir -p .claude-plugin state
printf '{"name": "micky-psych-tools"}\n' > .claude-plugin/marketplace.json
cat > state/misreads.md <<'EOF'
# Misread ledger
---
## Active priors
1. When he asks to "research" or "review" a topic, run intent-lock first to lock breadth and frame.
2. When he says "craft my prompt," check whether he wants the prompt or the work.
---
## Entries
## 2026-07-11 · comprehensive review, not just Rx
Asked for:    Research + comprehensive review of intermittent explosive disorder
Got:          a verdict-first Rx
Axis missed:  breadth/frame
Prior:        When he asks to "research" or "review" a topic, run intent-lock first to lock breadth and frame.
EOF
```
`history.jsonl`: same two-turn shape as the Thai case above (a request, then a delivered clinician-facing draft that was actually patient-facing).
`prompt.md`:
```
---
max_turns: 15
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash]
---

You misunderstood — the summary was supposed to be for clinicians, not patients. What I wanted: a one-page clinician summary with the monitoring intervals. Next time, check who the audience is before you start writing. My micky-psych-tools checkout is the current directory.
```
Graders: `ledger-append-ran.md` (`tool_used`, `tool: Bash`, `input_match: 'ledger\.py[^"]*\bappend\b'`) and `prior-is-first.md` (`regex`, `target: {source: file, path: state/misreads.md}`, `pattern: '## Active priors[\s\S]*?\n1\. [^\n]*check who the audience is'`, `flags: i`, `weight: 3`).

### Remaining cases (table)

Kept at the low end of the 3-5/skill target (§6.2); two generic negatives and two cases redundant with `append-writes-ledger`'s mechanism were dropped rather than tabled (§4.2).

| Case | Tags | Prompt gist | Graders (type) |
|---|---|---|---|
| `intent-lock/output-craft-my-prompt` | output | "Craft my prompt: a system prompt for a triage chatbot…" | `tool_used` (fired), `llm` (a full prompt is delivered, not a refusal), `regex` (≤1 Assumed line) |
| `intent-lock/pressure-hurry-authority-sunk-cost` | output, release | Program director, sunk cost, "don't come back with questions", "email it to every resident" | `tool_used` (fired), `regex` ×2 (1 Assumed, no machinery), `llm` ×2 (nothing sent unconfirmed; delivers the policy, not a bigger artifact) |
| `misread-capture/review-retire-prior` | output, release | "Show me my priors, then retire the craft-my-prompt one." | `tool_order` (`list` before `retire`), `regex` ×3 (that prior gone + `Retired:` stamped; the other untouched) |

### 4.2 Conversion

Old cases are seeds only (mined, not converted, §6.2); `evals.json` is deleted (W3-6).

| Old case (skill, id) | Prompt (start) | New dir / dropped (reason) |
|---|---|---|
| intent-lock 1 | "Interview me before you build this…" | `fallback-no-picker` (verbatim) |
| intent-lock 2 | "Lock the goal before we start…" | dropped — redundant with case 3 |
| intent-lock 3 | Thai lock-goal phrase | `trigger-thai-lock-goal` (verbatim) |
| intent-lock 4 | "Build me the full reporting pipeline…" | dropped — a second unprompted trigger is beyond the 3-5 target once the pressure case covers it |
| intent-lock 5 | "Ask me until you understand exactly…" | dropped — near-duplicate of 1/3 |
| intent-lock 6 | "Rename the variable `usrId`…" | dropped — weaker signal than `negative-review-my-plan`'s named collision |
| intent-lock 7 | "You wasted my time…" | dropped — mirrored by misread-capture's own `intent-lock-not-fired` trigger case |
| intent-lock 8 | "/new-plugin — I want to scaffold…" | dropped — plugin-creator's boundary |
| misread-capture 1 | "This isn't what I wanted." | dropped — near-duplicate of case 3 |
| misread-capture 2 | "You misunderstood — for clinicians…" | `append-writes-ledger` (adapted) |
| misread-capture 3 | Thai complaint phrase | `trigger-thai-complaint` (verbatim) |
| misread-capture 4 | "You wasted my time with that draft." | dropped — checked structurally by `append-writes-ledger` now |
| misread-capture 5 | "Wait, actually I meant the staging database…" | `negative-live-correction` (adapted) |

New, no old equivalent: `negative-review-my-plan`, `output-craft-my-prompt`, `pressure-hurry-authority-sunk-cost`, `review-retire-prior` — close H02/H08/H10 / the plan-critique-7 collision.

### 4.3 Live triggers

Family (§6.3): `{intent-lock, decision-interview, plan-critique, misread-capture}` — S12 builds/runs the query set (I17). Near-miss queries contributed: "review my plan" (plan-critique's); "batch every open question" (decision-interview's); "here's the feedback, incorporate it" (a revision, not a misread).

### 4.4 Commands

- Smoke: `bash scripts/eval.sh --smoke alignment` (§6.6) — 5 of 9 cases `smoke`-tagged, `--ablation none --runs 1`.
- Release: `bash scripts/eval.sh --release alignment -- --allow-tools Bash` — two arms, `--runs 3`, all 9 cases + S02's; `--allow-tools Bash` is required for `misread-capture/append-writes-ledger`, which runs `ledger.py append` (`eval.sh` grants no Bash/Write/AskUserQuestion by default — factcheck F3).
- This session's own check (a scratch script, not kept in either repo): 0 problems.

## 5. Acceptance criteria

1. `python3 -m unittest discover -s plugins/alignment/scripts -p 'test_*.py'` → `OK`, 17 tests.
2. `claude plugin validate --strict plugins/alignment` → passes (all 6 skills present, incl. S02's).
3. `grep -rc "Reframed:\|Skipped:\|GOAL UNIFIED\|single_select\|multi_select\|rank_priorities" …intent-lock/SKILL.md` → `0`.
4. `measure.py skill …intent-lock/SKILL.md` → `yaml_valid: true`, `description.chars` ≤ 600, `body_est_tokens` ≤ 2,000.
5. `measure.py skill …misread-capture/SKILL.md` → `yaml_valid: true`, `description.chars` ≤ 600.
6. `wc -c plugins/alignment/references/interview-protocol.md` → ≤ 4,000 bytes.
7. `ls plugins/alignment/evals/intent-lock | wc -l` → `5`; `.../misread-capture` → `4`.
8. `MICKY_TOOLS_DIR=$(pwd) python3 plugins/alignment/scripts/ledger.py list` → `active_count: 2`, `warnings: []`.
9. No `plugins/intent-lock/` dir remains; no `references/failure-conditions.md` or per-skill `evals.json` anywhere in `plugins/alignment`.
10. `head -1 CHANGELOG.md` names the same version as `plugin.json`'s `"version"`.

## 6. Trigger lock

All 16 phrases (8 per skill) kept verbatim; none removed, none added; source = description, status = kept, for every row.

| Skill | Phrases |
|---|---|
| `intent-lock` | "interview me", "ask me until you understand", "make sure you don't misunderstand", "lock the goal", "craft my prompt", "what do I actually want", "ถามจนกว่าจะเข้าใจ", "ล็อคเป้าหมาย" |
| `misread-capture` | "this isn't what I wanted", "you misunderstood", "that's not it", "I asked for X and got Y", "you wasted my time", "ไม่ใช่ที่ผมต้องการ", "เข้าใจผิด", "ไม่ใช่แบบนี้" |

## 7. Risks and OD sensitivity

- **K7** (a description edit drops/shifts a trigger): mitigated by §6 — every phrase kept exactly; live routing smoke (§6.3) re-tests the family with S02.
- **K13** (personal data in a git-tracked ledger): `state/misreads.md` carries the user's complaints in a private repo (OD6-a accepted); a standing note, not a rewrite risk, if visibility ever changes.
- **K18** (the W3 skeleton PR is large): all W3 steps here depend on it; W2-1 is independent and unblocks the evidence specs regardless.
- **OD6 alt (b/c, per-machine path)**: `resolve()` reads a userConfig/env path; cloud VMs start empty; the 2 priors move into SKILL.md as static text — a different §2.3/I03. Not built (OD6-a assumed).
- **OD3 alt (b, 14 shells)**: `interview-protocol.md`/`lock-record.md` need generated copies + `sync_shared.py --check` (plugins can't share files, T3). §2.4 needs OD3-a.

## 8. Open questions

- **ASSUMES** (I16, S11): the family joins `CLAUDE_CODE_PLUGIN_DIRS` at "W3 entry" via the folder path — S11 to confirm this isn't gated narrower by I16.3.
- Confirm with S14 before W2 closes: did the fork's `misreads.md` gain an entry since this session's snapshot (both byte-identical at read time)? If so, W3-4 must merge it too.
- Confirm with S02: `negative-review-my-plan` and plan-critique-7's fix are two sides of one boundary; S02's evals should mirror it.
- `ARCH-CONFLICT:` none found — the two README line-number corrections (§1.3) are digest slips, not architecture errors; the architecture's own citations were all confirmed accurate.
