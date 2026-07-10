# Changelog

## 0.3.0

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

## 0.2.0

Unreleased intermediate. The manifest carried this version from the plugin's first commit, but the changes it implies were never distinctly implemented or documented — the actual silent-run behavior landed in 0.3.0 above, which this entry's content has been folded into.

## 0.1.0

Initial: cold read with prediction v0, divergent readings, admission threshold, option-picker contract, three-round cap, convergence gates, assumption preface, `misread-capture` routing.
