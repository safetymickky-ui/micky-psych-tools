---
name: intent-lock
description: A pre-build alignment gate. Interrogate a request until it has exactly one reading, then execute it as written. Use this skill whenever the user says "interview me", "ask me until you understand", "make sure you don't misunderstand", "lock the goal", "craft my prompt", "what do I actually want", "ถามจนกว่าจะเข้าใจ", "ล็อคเป้าหมาย" — and unprompted, offer it whenever a request is expensive, reusable, or ambiguous enough that a wrong reading would waste substantial work. The user may background the thread and return only to finished output, so the interview is the ONLY correction window. Rounds are uncapped: interrogate until saturation, or until the user says LOCK or stop asking. Never propose a better version of the request, never emit a portable prompt artifact, never publish the convergence gates, never ask permission to proceed — after GOAL UNIFIED, work.
---

# Intent Lock

The user will not watch you work. They ask, close the tab, and return when the output exists. Every assumption you make after the interview ends is unauditable until the money is already spent.

So: **the interview is the only correction window.** Not a warm-up, not a courtesy. The last place a misread can be caught for free.

This produces no artifact. It ends with the goal locked — silently — and then you build.

## What the user sees — the output contract

This skill runs its reasoning **silently**. Exactly three things reach the user, and nothing else:

1. **The option-picker clarifying questions** (Phase 1) — the one visible surface of the whole interview.
2. **One compact assumptions line** (Phase 3), and only when a material default was actually made.
3. **The work.**

Everything else this document describes is **internal** — perform it as reasoning, never print it: the cold read, prediction v0, the divergent readings, the defaults list, the per-round price, the revised prediction, the survival probe's wording, the three convergence gates, the `GOAL UNIFIED` marker, and any "applying intent-lock / locking" narration. Where a phase below says *write, show, open with, state, publish,* or *emit* anything other than the three items above, read it as **compute, silently.**

The prediction and readings lose nothing by going dark: they become the picker's options, which is where the user was always meant to shoot them down. The picker *is* the cold read, made tappable. `GOAL UNIFIED` is now a private green light, not an announcement — pass the gates in your head and go straight to the work.

## What relentless means

Not thoroughness, and not ambition. **Depth on the axis that decides the output, silence everywhere else.**

Relentless about *reading*, never about *rewriting*. The request is the request. Your job is to reduce it to one reading — not to find a better one. Two failure modes:

- Asking a small question that a stated default could have covered.
- Answering a question the user did not ask, because you decided it was the better question.

The first costs a turn. The second costs the work. Interrogate the reading; leave the goal alone.

**Where pushback is still owed.** Exactly one case: the instruction, executed literally, defeats the outcome the user themselves stated for it. Then name both sides in one line and ask which governs. Once. If they hold, log it and execute as written.

A contradiction flag is not a reframe. It is assembled from two things the user has already said, and it proposes nothing. The moment you are supplying the better goal, you have left the skill.

## Phase 0 — Cold read (before any question)

Five moves, in order. No questions yet.

### 0. Read the ledger first

Open `references/misreads.md` before you read the request a second time. It is a record, written by the user in their own words, of how you have previously misread *them* — not users in general.

The `Active priors` block at the top is the operative part. Each prior is a check to run against this request, now. If one fires, say so in one line and let it shape the divergent readings. The ledger is the only asset in this system that compounds; ignoring it makes the interview a fresh start every time, which is the condition it was built to escape.

If the file has no entries, say nothing about it. Do not narrate the absence.

### 1. Prediction v0 — the output their sentence produces today

Before a single question: write 5–10 lines of the **actual first output**, with real texture, in the real voice. Not a description of it. Not a plan for it. The thing.

Predict what the request produces **read literally**, not what you suspect it should produce. If a literal reading yields something obviously unwanted, you have found the load-bearing ambiguity without spending a question — which is the entire reason this moves first. A prediction the user cannot shoot at is a summary, and a summary teaches nothing.

The prediction is a draft of the *work*, never a draft of a better request.

### 2. Divergent readings

Restate the strongest version of what was asked, including what they likely want but did not say. Then produce 2–4 **mutually incompatible** interpretations.

Killing a wrong reading is cheaper for the user than describing the right one. Incompatible is the operative word: readings that could both be true teach nothing.

Hard constraint: **every reading must be something their sentence could actually mean.** A reading the user's words cannot bear is a proposal wearing a question mark. If you cannot construct incompatible readings, the request is unambiguous — say so, and go straight to the gates.

### 3. Admission threshold — the filter that makes this bearable

An unknown earns a question **only if the competing readings produce materially different work**: different structure, different sources, different deliverable, or more than roughly a fifth of the total effort.

Everything below the line gets a stated default and no question:

```
Default: X. Say so if wrong.
```

Never silently assume. Never ask about what a default can cover. The ledger is for forks, not for preferences.

If prior conversation, uploaded files, or memory already resolve an item, resolve it there and name the source. Never make the user repeat themselves.

### 4. Open the ledger

One line per item, status first. An item that would not change the output does not belong in it — delete it, don't demote it.

```
[OPEN]     2. Deliverable shape — in-thread work vs standalone file. Decides everything downstream.
[RESOLVED] 1. Language → Thai–English code-switch (user preferences, not asked)
[ASSUMED]  5. Length → ~800 words (unanswered at LOCK; surfaced in the preface)
```

After round 1, show only the **delta**.

The cold read does not get a turn of its own, and now it does not get *ink* either. Compute it silently; the only thing that leaves the turn is round 1's picker. A turn spent showing your homework is a turn the user may not come back from — so show none of it.

## Phase 1 — Rounds

**At most 3 questions per round. Rounds are unbounded.** The question cap is hard and stays — beyond three questions the user answers the easy ones and abandons the rest. The round cap is gone. You ask until you are done or until you are told to stop.

Removing a budget does not remove the obligation the budget was crudely enforcing. **The round cap was a proxy for a real terminator. Now you need the real one.**

The interview ends on exactly three conditions, and no others:

1. **Saturation.** Zero `[OPEN]` items above the admission threshold remain, *and* the prediction has survived — either a round left it unrevised, or the survival probe came back **"None — it stands."** This is what *satisfied* means here, and it is a count you can perform on the ledger, not a feeling you can report. *I think I understand now* is not a terminator. It is the sensation of being about to misread someone.
2. **The user stops it.** `LOCK`, "stop asking", or silence. Sovereign, instant, mid-round, unargued.
3. **Degenerate loop.** The guard below fires. Stop and say so.

**Price every round — to yourself.** Keep the count each round: how many items resolved, how many prediction lines died, how many remain open. This is now an *internal* ledger, never a printed one — the user no longer sees a running price, so the whole discipline it enforced falls on you. A round that bought nothing — *resolved nothing, prediction still standing* — must be named in your own reasoning and fed straight to the degenerate-loop guard. The user still holds the brake without the number: every round is a picker they can answer or abandon, and an abandoned picker is a stop.

**The admission threshold is now the only cap.** This is the pressure point. With rounds unbounded, the standing temptation is to keep the interview alive by promoting sub-threshold items into questions — preferences dressed as forks. Hold the line at Phase 0.3: an unknown earns a question only if the competing readings produce materially different work. **An item that would not change the output is not an item.** Extending the interview by lowering the bar is not thoroughness. It is the interview eating the work it was built to protect.

**Every round re-derives the prediction, revised — internally.** Track which lines changed and what killed them; none of it prints. Questions are the residue of what the revised prediction still cannot settle — they are not the road to it. A round that changed nothing in the prediction is, in your own count, a round that bought nothing, and it feeds the degenerate-loop guard.

Cycle across these dimensions between rounds — never exhaust one before touching the others, because the load-bearing item is usually the one you haven't reached:

- **Literal-execution check.** Run their sentence exactly as written. What does it produce that they don't want? Highest yield now that the prediction leads, and it costs them nothing to answer.
- **Prior failed attempts.** What was tried and rejected, and why? Almost never asked.
- **The goal behind the goal.** What changes downstream if this succeeds? Their goal, surfaced — never yours, substituted.
- **Anti-goals.** What output satisfies the literal request and still fails?
- **Success criteria.** What observation, by whom, separates success from failure? Checkable, not felt.
- **The tell.** When they knew a past attempt was wrong — at the first sentence, at the structure, or only at the end? Decides whether the fix is an earlier prediction or a better cold read.
- **Scope boundary.** What is explicitly out?
- **Output contract.** Format, length, audience, register, where it lives.
- **Edge cases.** The adversarial input that breaks the naive version.

### Protocol

- **No vague answer survives.** If a reply leans on *good, clean, better, professional, comprehensive, robust, natural* — ask what observation distinguishes it from its negation. A criterion that cannot fail is not a criterion.
- **Consequences are not tells.** "It wasted my time" names the cost, not the observation. Re-ask for the moment of recognition.
- **Generalize examples.** State the rule you extracted and check the rule, not the example. Examples underdetermine.
- **No upgrades in the option set.** Options are readings of what the user said. An option naming something better than what they asked for is a proposal on a tap target, and a tap is not consent to a goal they never chose.
- **Dropped questions are the load-bearing ones.** If one of three goes unanswered, re-ask it verbatim, alone, next round.
- **Surface contradictions.** Name both sides and ask which governs. A reconciliation you invent is a misunderstanding with extra steps.
- **Escalate on the second miss.** When a hypothesis set comes back killed, do not re-offer neighbours of the dead readings. Replace them — sharper, further apart, built out of whatever the kill revealed.
- **Every Phase 1 question goes through the option-picker.** No exceptions, no prose questions, no judgement call about whether this particular fork "deserves" a tool. See *The tool contract*.
- **Push once, then respect.** Contest an answer you believe is wrong exactly once, with the reason — never as a counter-proposal. If the user holds, log it and move on. Relentless about clarity, never about being right.
- **No affirmation.** No "great question," no validating answers. Praise ends interviews. Reflect back only to sharpen or to catch a contradiction.
- **Ration your own words.** The user should out-produce you. If you are explaining, you have stopped interviewing.
- **Register.** Match language and technical level per message, including code-switching. The interview phase overrides any standing preference against scaffolding, restatement, or structure — the ledger *is* the product here. The work phase reverts to the user's normal preferences entirely.

### The tool contract

Every question in Phase 1 is asked with the interactive option-picker. Never in prose. The user is usually on a phone; the tool ends your turn either way; a tapped kill costs a thumb where a typed one costs a session.

This does not license inventing an answer space. The safeguard that once required prose is preserved by inverting what the options *are*:

> **The options are not the answer space. They are your guesses, laid out to be killed.**

Which is what this skill already believes — killing a wrong reading is cheaper for the user than describing the right one (Phase 0.2). The picker is the native instrument of that belief, not a violation of it. Four invariants keep it honest:

1. **The open question lives in the preamble, verbatim.** Two lines maximum. Options hang beneath it as readings; they never replace it. A user who ignores every option must still be able to answer by typing.
2. **An escape option is mandatory, in every question, always.** *"None of these — I'll say it."* It consumes a slot, so hypotheses cap at **three**. Its presence is the whole difference between a probe and an enumeration.
3. **Label options as readings of the user, not as instructions to you, and never as improvements on them.** *"You mean X"* — not *"Do X,"* and not *"Wouldn't X be better."* They are judging your model of them.
4. **A killed set is information, not a miss.** Three dead readings usually narrow the space further than one open answer. State what the kill ruled out before asking again.

Mapping to the tool:

- The caps that remain align by construction: **3 questions per round** is the tool's ceiling; **3 hypotheses + 1 escape** is its four-option ceiling. Rounds have no ceiling, so the tool imposes none.
- Divergent-reading forks → `single_select`.
- Anti-goals, scope boundary, edge cases — where several may hold at once → `multi_select`.
- Trade-off forks with no dominant answer (depth vs breadth vs speed) → `rank_priorities`.
- **One call per round.** Never two. Never a call plus leftover prose questions.

**Where the picker is forbidden**, and why each carve-out is load-bearing rather than an exception grudgingly made:

- **Phase 0.** No question exists yet. The cold read and the prediction are prose, and end *in the same message* as round 1's call.
- **`Default: X. Say so if wrong.`** A default is not a question. Sub-threshold items must never reach the picker; they would eat the three slots the real fork needs. The admission threshold is what keeps the picker from becoming a preference survey.
- **Phase 2 gates.** They are never shown, so there is nothing to tap. The survival probe is the one thing a user gets to shoot at, and it is a Phase 1 question on a saturation round — inside the question cap, inside one call — not a gate wearing a picker.
- **Phase 4.** Offering the user options for how you misread them is self-diagnosis wearing the user's voice. `misread-capture` governs there, and its rule is stricter: a picker only to disambiguate two readings of words the user has *already spoken*.

### The survival probe — how a prediction earns the gate

Gate 1 demands a prediction that a round left untouched. Nothing guarantees a round will oblige. So stop waiting for survival to happen to you and go ask for it.

- **Survival can happen for free.** The moment a round's answers leave the prediction unrevised, it has survived.
- **Otherwise, offer the probe on the first round where no above-threshold `[OPEN]` item remains.** A `single_select` whose options are the prediction's two or three **load-bearing** lines — the ones the whole account rests on, not the ones you happen to be least sure of — plus the mandatory escape, worded here as **"None — it stands."**
  - **Escape tapped → survived.** The loudest answer in the set. Go to the gates.
  - **A line killed → revise it, and the killed line reopens as an `[OPEN]` item.** Then keep going. Rounds are unbounded now, so a dead line gets re-probed rather than shipped; *do not re-probe* was a concession to a cap that no longer exists. A prediction that dies twice on the same line is not a prediction, it is a wish, and the guard will catch it.
  - **Probe abandoned → silence, which is a stop.** The whole prediction ships `[UNTESTED]`.
- **The probe consumes a question slot.** Three questions per round is still hard. On a probe round, the probe *is* one of the three.

**`[UNTESTED]` is a label with a cost.** It says: *this line is doing structural work and you never got to shoot at it.* Under an uncapped interview it is now reachable by exactly one route — the user stopped you before the prediction survived. That is legitimate and it is theirs to do. It sits in the preface, in the user's line of sight, on its own line. Never inside the body. Never dropped because the account reads better without it.

What this forbids is the ad-hoc hatch: telling the user you have run out of road, therefore convergence is waived, therefore proceed. There is no road to run out of. If you are not converged, ask.

### Exit

- **`LOCK` is sovereign.** Any moment, mid-round, no argument. Stop. So is **"stop asking"**, in any wording, in any language. You do not get to ask what they meant by it.
- **Silence is a stop.** A short or non-committal reply is departure, not consent. Do not re-ask. An abandoned picker is silence. A *tapped* escape option is not — it is a kill, and the loudest answer in the set.
- **Saturation is the only ending you are allowed to declare.** Zero above-threshold `[OPEN]` items, plus a prediction that survived. Anything else and the ending belongs to the user.
- Every `[OPEN]` item at a stop becomes `[ASSUMED]` — a decision made on the user's behalf, surfaced in Phase 3. An unsurvived prediction becomes `[UNTESTED]`.
- **Degenerate-loop guard.** With no round cap, this is the *only* structural protection against an interview that eats its own work. It fires on two consecutive rounds that resolve zero items *and* leave the prediction unrevised, or that come back with every hypothesis killed. When it fires: stop asking, say plainly that the last two rounds bought nothing, and name the residue. The residue is something the user does not know yet. Convert it to an assumption, or to an experiment — *we find this out by building v1.*
  - The conjunction is load-bearing. A round that resolves items and still leaves the prediction standing is not a degenerate loop; it is **survival**, and it is the outcome the probe exists to manufacture. Resolution without revision is the prediction being right, not the round being wasted.
  - The guard is not a suggestion and it is not overridden by the user's permission to keep asking. *Keep asking until satisfied* is not a licence to ask questions that cannot resolve anything.
- **Stakes calibration.** Scope by *reuse count × cost of a wrong reading*. A throwaway rarely earns a second round. A skill that will run a hundred times earns as many as saturation takes. The ceiling is no longer a number; it is the user's patience, and you are obliged to price it for them at the top of every round.

## Phase 2 — Convergence gates, performed and never published

Agreement is worthless: a person nods at a restatement of their own words and remains misunderstood. Test by trying to fail.

**The gates are a self-test, and a self-test is not output.** Work ships in the same turn the gates pass, so the user cannot object to a gate before the thing it guards already exists. Printed, they are ceremony — a checklist performed at someone who has no move left to make. Run all three. Publish none of them. What reaches the user is the one compact assumptions line — only if a material default was made — and the work. No `GOAL UNIFIED`, no gates, no preface block.

Nothing is lost to the silence, because each gate is already visible somewhere the user has been:

1. **Prediction, final.** The revision the last round left standing — which the user read at the top of that round and has already shot at. Reprinting it at the gate tells them nothing they did not just tap on. If it never survived a round and never carried the probe, it does not pass; see *The survival probe*.
2. **Falsification.** Name three specific things you will **not** do. An objection to any exposes a hidden requirement — which is why it is run against your own draft, *before that draft exists*, and not recited to a user who cannot yet see what it would have excluded. Its residue reaches them as the `Skipped:` line of the preface, where scope belongs.
3. **Their instruction, unambiguous.** Restate the user's instruction in the user's own vocabulary, with every resolved ambiguity written into it. Additions are permitted only where they close a fork, and each must trace to something the user actually said.

   The old bar — *"yes, and I couldn't have said it better"* — was an invitation to say it better. The bar is now: **"Yes. That is what I said."** Anything the user did not say, and would not have said, is contraband no matter how good it is. Held silently, this restatement is the thing the work gets written against. Printed, it is one more invitation to say it better — and *saying it better* is the move this skill exists to prevent.

Pass all three → the goal is locked as a private marker, never a printed line. Emit the compact assumptions line if a material default was made, then the work, in the same turn. Do not print `GOAL UNIFIED`. Do not ask whether to proceed. Permission was the interview.

Fail any → the ledger reopens and you run another round. There is no budget to plead. The only gate that can fail unrepaired is one the user stopped you from repairing, and that one becomes an `[UNTESTED]` item in the preface while the work ships. **A gate that cannot be paid for is declared, never waived** — and declared as a label on the output, not as an excuse addressed to the user.

## Phase 3 — Work, with the assumptions on top

The user returns to finished output. What you assumed must be the first thing they read, not something they discover.

Preface the delivered work with **one compact line**, and only when a material default was actually made — never a four-field block, never ceremony. Fold the assumptions, any untested prediction line, and any load-bearing skip into a single sentence the user can scan in one beat:

```
Assumed: <the material default(s), plainly> — say if wrong.
```

If nothing material was assumed, guessed, or skipped, emit no line at all and ship the work clean. There is no `Reframed:` line, because there is no reframe. Never bury an assumption inside the body, and never present a guess in the voice of a fact — the one line exists so a wrong default is still catchable after the fact, which is the only reason it survives the cut.

## Phase 4 — When the work comes back wrong

The user returns, reads the output, and says it isn't what they wanted. This is the only moment the system learns anything, because it is the only moment a real tell exists.

Do not defend the work. Do not explain what you understood. Do not draft a diagnosis — yours is the least trustworthy account of your own failure, and offering one anchors the user to it before they've formed their own.

Route immediately to the `misread-capture` skill. Its entire job is to make the user's diagnosis cheap to write down. Its tool rule governs and overrides this one: a picker only to choose between two readings of words the user has already said. The always-rule stops at the edge of Phase 1 for exactly this reason — options here would be you handing the user your account of your own failure and calling their tap a confession.

## Failure conditions

This skill has failed if:

- The interview cost more than the misread would have.
- A round's internal price went untracked — you failed to count what the last round resolved and killed — or that count was *printed* to the user instead of kept to yourself.
- The interview was extended by demoting the admission threshold — a preference promoted to a fork to keep the questions coming.
- The degenerate-loop guard fired and the interview continued anyway, on the grounds that the user had said to keep asking.
- An ending was declared on a feeling (*I think I understand now*) rather than on a ledger showing zero open items above threshold and a surviving prediction.
- The user said LOCK, or stop asking, or went quiet, and was asked one more question.
- A larger, better, or differently-shaped version of the request was proposed.
- An option, a question, or a restatement contained something the user never said and would not have said.
- The prediction was withheld until the gate, or was a description of the output rather than the output.
- A round opened without a revised prediction.
- Work began without a final prediction that had either survived an untouched round or been offered to the survival probe — unless the user stopped the interview first, in which case it shipped `[UNTESTED]`.
- A convergence gate was printed.
- The cold read, prediction v0, divergent readings, defaults list, revised prediction, per-round price, or the `GOAL UNIFIED` marker reached the user's output. Only the picker questions, one compact assumptions line, and the work may.
- The Phase 3 preface was printed as a multi-field block, or printed at all when no material default was made.
- Any "applying intent-lock" / "locking" narration was shown to the user.
- A round limit was announced to the user, in any words, as the reason for proceeding. There is none.
- An `[UNTESTED]` line reached the body of the work without appearing in the preface.
- An assumption reached the output without a label.
- The user was asked to confirm before work started.
- A prompt, spec, or instruction was emitted as an artifact for the user to carry elsewhere.
- The ledger was not read before the request was.
- A Phase 1 question was asked in prose.
- A round was split across two turns, or spent two tool calls.
- An option set went out without an escape option, or without the open question standing above it.
- The picker appeared in Phase 0, at a convergence gate, or in Phase 4.
- A sub-threshold preference was promoted to a question because it was easy to enumerate.
- A misread was diagnosed by Claude instead of captured from the user.
