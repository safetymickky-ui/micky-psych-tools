# Changelog

## 1.0.0 — 2026-11-10

A rewrite. Both skills were written again from an interview with the owner (2026-11-10).

- **Round 1 has fixed targets.** It settles what kind of output, what it is for, and how
  deep and wide, in that order. Each option must describe a concrete output.
- **Rounds are capped at 3.** The uncapped interview, the saturation rule, the survival
  probe and the degenerate-loop guard are gone.
- **The lock is written down.** For long work it is saved to `intent-lock.md` and reread
  before each stage.
- **Check before delivery.** The finished work is compared with the lock line by line, and
  drift is fixed before the user sees the output.
- **Lock lines on top of the output.** 3 to 5 plain sentences: the locked goal, the
  assumptions, the check result. This replaces the silent run and the one-line preface.
- **The ledger moved to an artifact page with a database** ("Misread Ledger"). The plugin
  file lost every new entry at the end of a cloud session. The three existing entries were
  moved over, including the September 2026 entry that the old file never kept.
  `references/misreads.md` is replaced by `references/ledger.md` (where the ledger is and
  how to use it) and `references/checks-snapshot.md` (a fallback copy).
- **Claude writes ledger entries.** Drifts, interview errors and the user's corrections are
  logged without being asked, and each becomes a check. The July rule that only the user
  writes the diagnosis is dropped.
- **misread-capture asks at most one question** and logs automatically. It separates a
  misread from an ordinary follow-up edit.
- **A rule for runs where nobody can answer.** Scheduled runs and explicit opt-outs ask
  nothing and state every default.
- **Removed:** the tool names `single_select`, `multi_select` and `rank_priorities` (not in
  the current picker), and `references/failure-conditions.md` (a short list now sits in
  each SKILL.md).
- **Unchanged for callers:** the skill names, every locked trigger phrase, the explicit
  opt-out, `[ASSUMED]` items, the boundaries with decision-interview and plan-critique, and
  the rules against proposing a better request, asking permission, or emitting a prompt artifact.

## 0.4.3 — 2026-10-19

- **Frontmatter parses again.** The `intent-lock` skill description is now a YAML folded
  block scalar (`description: >-`); unquoted, its `: ` sequences broke the YAML parse and
  the skill loaded with empty metadata. Wording unchanged (1020 chars).

## 0.4.2 — 2026-08-06

- **Reciprocal boundary with plan-critique.** The skill description's Not-for clause now
  carves out critiquing or improving an existing plan (plan-critique), alongside the
  existing decision-interview and misread-capture carve-outs. Phrasing tightened to fit
  the 1024-char cap ("Use when…" canonical form; no meaning change).

## 0.4.1

no contemporaneous entry; see `git log` around this version.

## 0.4.0 — 2026-07-10

- **Fixed the misread ledger.** `misread-capture` addressed the ledger as a bare
  `references/misreads.md`, which resolved to a non-existent file inside its own skill
  directory — so appended priors never reached the one file `intent-lock` reads at Phase 0,
  and the compounding-priors loop silently did nothing. Both skills now name the single
  canonical ledger (`skills/intent-lock/references/misreads.md`, via `${CLAUDE_PLUGIN_ROOT}`
  from `misread-capture`). The retirement rule in the ledger header now defers to
  `misread-capture`'s procedure (present the oldest three, user picks) instead of a divergent
  "retire past 7" shorthand.
- **Leaner skill body.** The exhaustive failure-conditions list moved to
  `references/failure-conditions.md`; the six load-bearing invariants stay inline with a pointer.
- **Sharper triggering.** Both skill descriptions made third-person and given explicit
  `Not for` clauses (throwaway/precise requests and post-delivery misread-capture for
  `intent-lock`; mid-interview corrections for `misread-capture`). Added `evals.json` for both
  skills covering positive triggers and cross-skill negatives.
- **Docs.** Fixed the marketplace slug (`mickky-plugins` → `micky-psych-tools`) and the
  README's contradictory "prints `GOAL UNIFIED`" claim; corrected the changelog so 0.3.0
  documents the real silent-run change; fixed the author spelling.

## 0.3.0

**The run went silent.** `GOAL UNIFIED` became a private gate, never printed — the goal locks internally and the work follows in the same turn. Everything the interview computes now stays internal: the cold read, prediction v0, divergent readings, defaults list, per-round price, revised prediction, survival-probe wording, and the three convergence gates are performed as reasoning and never reach the user. Exactly two things surface — the option-picker clarifying questions, and the work.

- The four-field assumption preface (`Assumed:` / `Untested:` / `Resolved:` / `Skipped:`) collapsed to at most one conditional line: `Assumed: … — say if wrong.`, emitted only when a material default was actually made. Nothing material assumed, guessed, or skipped → no line, ship clean.
- The per-round price is still counted, but only to yourself — it feeds the degenerate-loop guard instead of being printed. The user holds the brake through the picker itself: an abandoned picker is a stop.
- Added a governing output-contract section, and new failure conditions forbidding any internal machinery — the `GOAL UNIFIED` marker, a multi-field or unwarranted preface, or "applying intent-lock" narration — from reaching the user.

## 0.2.0

**Removed the round cap.** Rounds are now unbounded. The interview ends on saturation (zero open items above the admission threshold plus a surviving prediction), on `LOCK` / "stop asking" / silence, or on the degenerate-loop guard.

- Saturation is defined as a count performed on the ledger, not a feeling. *I think I understand now* is explicitly not a terminator.
- Every round must open with its price: items resolved, prediction lines killed, items still open. A round that bought nothing must say so.
- The admission threshold is now the only cap, and the standing temptation is to lower it. Extending an interview by promoting sub-threshold preferences into forks is a named failure condition.
- The degenerate-loop guard becomes the sole structural protection against runaway interviews, and is explicitly not overridable by the user's instruction to keep asking.
- 3 questions per round is retained. That cap serves attention, not budget.

**Convergence gates are performed and never published.** Work ships in the same turn the gates pass, so the user has no move left when they read them. Printed, they were ceremony — and the printed restatement was a standing invitation to *say it better*, the one move the skill exists to prevent. All three still run. None reach the user. `GOAL UNIFIED.`, the preface, and the work do.

**Added the survival probe.** Gate 1 demands a prediction a round left untouched; nothing guaranteed a round would oblige, and under the old cap the last round's answers necessarily revised the prediction they arrived too late to test — making gate 1 unpassable on any full-length run, waivable only by announcing the cap to the user. Now:

- Survival happens for free when a round leaves the prediction unrevised.
- Otherwise, on the first round with no above-threshold open items, one question slot goes to a `single_select` over the prediction's load-bearing lines, escape worded **"None — it stands."**
- Escape tapped → survived. A line killed → revise, reopen it, keep going. Probe abandoned → the prediction ships `[UNTESTED]`.

**Added `[UNTESTED]`** to the Phase 3 preface, above `Resolved:`. Reachable by exactly one route: the user stopped the interview before the prediction survived.

**Fixed a collision in the degenerate-loop guard.** It read *zero items resolved OR prediction unrevised*, which made survival and degeneracy the same event. Now a conjunction, with the reason stated inline.

**Six new failure conditions**, including *a convergence gate was printed*, *a round opened without its price*, *the interview was extended by demoting the admission threshold*, *the guard fired and the interview continued anyway*, and *an ending was declared on a feeling*.

## 0.1.0

Initial: cold read with prediction v0, divergent readings, admission threshold, option-picker contract, three-round cap, convergence gates, assumption preface, `misread-capture` routing.
