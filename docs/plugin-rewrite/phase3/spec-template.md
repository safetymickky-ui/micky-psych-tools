# Spec template (phase 3) — every spec uses exactly these sections

Write for an executor: a later Claude Code session (or the owner) that will make the
changes step by step, with this spec open and the repos checked out. It has not read the
research. Every instruction must be concrete enough to execute without guessing.

## Size and effort limits (hard)

- One spec file is at most 40 KB. Prefer tables and short bullets over prose.
- Section 4.1: give FULL file contents for exactly three cases per skill (trigger
  positive, near-miss negative, one output or process case; for a gate the third case
  is the picker-absent fallback). List further cases in a table (name, tags, prompt
  gist, graders by type) without full contents.
- Section 2.3: an outline table, not the new SKILL.md text. Quote new text only where
  the exact wording is the fix (a description, a contract sentence, a handoff line).
- Do not write helper scripts to generate, simulate or test eval files or skills.
  Write the spec directly. Aim for about 30 tool calls in total; batch reads.

## Writing rules

- English. Short sentences. Active voice. Common words. Literal phrasing, no idioms.
- Bullets at most two levels deep. Use a table for any matrix.
- No praise, grades or taste words ("elegant", "solid", "clean"). Describe; do not rate.
- Every claim about today's files carries `path:line` evidence that you opened in this
  session. Measured numbers come from `python3 docs/plugin-rewrite/phase3/measure.py` or `wc`.
- Mark uncertainty inside the sentence ("the inventory reports", "not verified here").
  Never invent a fact. An unknown goes to §8 with the check that settles it.
- Owner decisions: assume the architecture's recommended option (§11). State the
  alternative's effect only in §7.
- Do not re-argue the architecture. If you find a real conflict with it, or an error in
  it, record it in §8 as `ARCH-CONFLICT:` with evidence, and follow the architecture
  unless it is factually wrong.
- Scope: only the units assigned to this spec. Interfaces owned by other specs are
  referenced (`I09 (owner S15)`), never redefined.

## Sections

```
# Spec Sxx: <title>

| Field | Value |
|---|---|
| Repos | … |
| Units (today → target) | … |
| Waves | … |
| Owner decisions assumed | ODn-a, … |
| Defects closed | <n> of <n> assigned (HIGH: H…) |
| Interfaces owned | I… |
| Interfaces consumed | I… (owner S…) |
| Depends on specs | S… |

## 1. Current state (measured 2026-09-24)
### 1.1 Files            table: path | lines | bytes | est. tokens | role
### 1.2 Descriptions     per skill/command: chars, UTF-8 bytes, YAML valid?, `Use when` offset,
                         `Not for` present?, every quoted trigger phrase (incl. Thai, slash forms)
### 1.3 Defects          table: id | sev | H# | evidence (path:line, re-opened) | problem | fix step | wave
                         EVERY defect with the assigned prefixes appears exactly once.
                         A deferral names its ratchet entry and the reason.
### 1.4 Other findings   inventory OBS lines that touch these units; new facts (mark NEW)

## 2. Target state
### 2.1 Location and tree (after the last wave that touches the units)
### 2.2 Frontmatter      exact YAML per skill (valid under yaml.safe_load); the full description
                         text; its measured chars; list of kept trigger phrases
### 2.3 Body outline     per skill: target section list in order; for each: source lines →
                         keep | cut (reason) | move → <file> | script → <name> | new;
                         target body lines and est. tokens
### 2.4 References       file | purpose | load condition ("Before step N, read …") | size target
### 2.5 Scripts          name | CLI (args, flags, --help) | input | JSON stdout shape | exit codes |
                         tests (file, cases)
### 2.6 Handoffs         exact sentences (OPTIONAL + fallback per I01; filing per I11)
### 2.7 Interfaces       owned: full definition. consumed: what you assume, `ASSUMES:` lines.

## 3. Change steps
Per wave, ordered. Step id `Sxx-W<n>-<k>`. One step = one commit in one repo.
For each step:
- Repo · depends on (step ids, other specs included)
- Files (create / edit / delete / move)
- Change (precise; quote the old text to delete or replace when it is short)
- Commands (exact; read-only checks first, then writes)
- Done when (checkable: command + expected output)
- Rollback (one line)
Also list owner actions (things only the owner can do) as separate steps marked OWNER.

## 4. Evals
### 4.1 Cases            ≥3 per skill: trigger positive, near-miss negative, output or process.
                         Gates add a pressure case and a picker-absent fallback case.
                         Give FULL file contents in fenced blocks headed by their path:
                         prompt.md (only keys from eval-format.md), graders/*.md, case.yaml,
                         mocks. Trigger grader form:
                         input_match: '"skill"\s*:\s*"(?:[\w-]+:)?<skill>"'
                         Negative: tool_used Skill, min: 0, max: 0, arm: both.
                         Safety graders carry the dominant weight.
### 4.2 Conversion       table: old evals.json case (file, name) → new case dir | dropped (reason)
### 4.3 Live triggers    family membership (§6.3 of the architecture) + 2–4 near-miss queries
                         for this unit (they feed S12's family query sets)
### 4.4 Commands         smoke and release commands for these units

## 5. Acceptance criteria
Numbered. Each one checkable with a command or a grep, with the expected result.

## 6. Trigger lock
Table: phrase | source (skill, field) | kept / moved → <skill> / removed (reason)

## 7. Risks and OD sensitivity
Unit-specific risks (link K#). For each relevant OD: what changes under the other option.

## 8. Open questions
Unknowns, `ASSUMES:` items, `ARCH-CONFLICT:` items; for each, the check that settles it
(W0 checklist item, probe command, or owner question).
```
