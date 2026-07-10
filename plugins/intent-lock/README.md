# intent-lock

A pre-build alignment gate. Interrogate a request until it has exactly one reading, then execute it as written.

Two skills:

- **`intent-lock`** — the interview. Cold read, a prediction of the actual output written before any question, mutually incompatible readings offered to be killed, then rounds of option-picker questions until saturation. Ends with `GOAL UNIFIED.` and the work, in the same turn.
- **`misread-capture`** — the ledger. When work comes back wrong, the user's diagnosis is written down in the user's own words. `skills/intent-lock/references/misreads.md` is the only asset here that compounds.

## Design commitments

- **The interview is the only correction window.** The user may background the thread and return to finished output.
- **Relentless about reading, never about rewriting.** The request is the request. No better version is ever proposed.
- **The prediction leads.** Every round opens with the actual first output, revised, with what killed the dead lines.
- **Options are guesses laid out to be killed**, never an enumeration of the answer space. Every question carries an escape.
- **Gates are performed, never published.** Convergence is a self-test, not a ceremony.
- **Rounds are uncapped.** The interview ends on saturation, on `LOCK` / "stop asking" / silence, or on the degenerate-loop guard.

## Ending conditions

- **Saturation** — zero open items above the admission threshold, and a prediction that survived a round or a probe.
- **Stop** — `LOCK`, "stop asking", or silence. Sovereign, instant, unargued.
- **Degenerate loop** — two consecutive rounds resolved nothing and left the prediction unrevised.

Anything unresolved at a stop ships labelled: `[ASSUMED]` for open items, `[UNTESTED]` for a prediction that was never shot at.

## The ledger

There is exactly one ledger file, at `skills/intent-lock/references/misreads.md`. Both skills share it: `misread-capture` appends to it — addressing it via `${CLAUDE_PLUGIN_ROOT}/skills/intent-lock/references/misreads.md` since the file lives in intent-lock's directory — and `intent-lock` reads it at Phase 0, before the request is read a second time. It holds `## Active priors` — checks to run against the *next* request, written by the user, in the user's words. Entries are appended by `misread-capture`, never drafted by Claude.

## Install

```
/plugin marketplace add <owner>/mickky-plugins
/plugin install intent-lock@mickky-plugins
```

Local development:

```
/plugin marketplace add .
/plugin install intent-lock@mickky-plugins
```
