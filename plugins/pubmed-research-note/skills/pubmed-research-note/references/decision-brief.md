# Crafting the Decision Brief

Read before your first tool call. This replaces the old four fixed frames. There is no menu
to sort the request into anymore — you **build** the decision from scratch every time, using
the same anatomy every good decision shares.

The brief is not a template to fill for its own sake. It is the answer to one question:
*what is this person about to do differently, and what would a good answer to that look like?*
Everything the search does and everything the report becomes is built against it.

The interview (or, on an explicit opt-out, you) fixes the first four slots — they are about
*what the user wants*. You derive the last three from them — they are about *how to answer*.

---

## 1. The question — what will be done, or understood, differently

One sentence. Not the topic, the **question**: the concrete thing that changes depending on
the answer. "Prazosin for this patient's PTSD nightmares this afternoon" is a decision.
"Prazosin in PTSD" is a bare topic, and a bare topic has no answer until it is turned into a
question. Usually the question is a decision. A pure understanding question is also
legitimate — "understand the ketamine evidence well enough to brief the department" — and
then this slot holds the understanding sought *and the use it will be put to*, which is what
keeps the search targeted.

If you cannot write the question as a sentence — a decision with a verb the user will act
on, or an understanding with a named use — the request is still a bare topic. That is not
yours to resolve by guessing — it is exactly what intent-lock is there to settle. Go back to
Step 0.

## 2. The verdict's shape — what a good answer physically looks like

Before searching, name the *form* the answer will take, because it decides what evidence is
worth gathering. This is bespoke to the decision, not chosen from a list. Some forms it has
taken:

- a **dose or range**, a sequence (give / don't / give only if X fails first), and an explicit
  statement of what **not** to promise the patient;
- a **build / don't / build-under-conditions**, with throughput and staff-time stated in the
  units the service actually uses;
- a **true / false / unsettled**, plus *why the disagreement exists* — and, if unsettled, the
  specific experiment that would settle it;
- a **sentence you can say out loud** to trainees, written verbatim, plus the conditions under
  which it expires;
- a **probability against a threshold** for act-or-wait decisions.

These are illustrations of forms the verdict has taken, not a set to pick from. The point is
to decide the *shape* early: a verdict with no shape produces a search with no target.

## 3. What settles it — match the evidence to the decision

Different decisions are settled by different evidence. Name the load-bearing kind before you
start, or you will collect abstracts that answer a neighbouring question:

- A **treatment choice** leans on head-to-head trials over placebo trials, effect size on the
  endpoint the patient cares about rather than a surrogate, NNT beside NNH, and the
  discontinuation rate in the treatment arm as the real-world proxy for tolerability.
- A **service or protocol** leans on pragmatic effectiveness over explanatory efficacy,
  remission and durability over response at week 6, and sessions / staff-time / cost per
  responder over effect size in the abstract. A therapy with `d = 0.6` over 30 sessions can be
  a worse *service* than one with `d = 0.4` over six.
- A **contested claim** is settled by the strongest study for and the strongest study against,
  adjudicated head-to-head — replication status, effect-size drift across the series (an effect
  that shrinks with each larger trial is a dying effect, and saying so is the finding),
  preregistration, funding source where it plausibly bears. Never by counting papers: twelve
  small positive trials and one large rigorous negative trial is not 12–1.
- A **teaching claim** is settled by the gap between the canonical textbook and the current
  evidence — name both, and say which the trainee should hold and which they should merely
  recognise on an exam.

## 4. What must be counted — the numbers the verdict can't stand without

List, before searching, the two to five numbers the verdict is hollow without: the effect size
with CI, the NNT and NNH, the dose range and titration interval, the absolute event rates for
the harms that would stop you, the remission rate and durability, the sessions per course.
These are what you hunt for — not "evidence about the topic" in general.

## 5. Mandatory checks — what would embarrass the verdict if skipped

- **The publication-bias sweep** (ClinicalTrials.gov) whenever an action or a claim's live
  status is at stake. A completed-unpublished negative trial is the single most common reason a
  confident verdict is wrong; a large ongoing trial reading out inside the decision's horizon
  can be the whole answer — *wait*.
- **The textbook edition** (Open Library) when the decision is what to teach. A textbook claim
  without a named edition is not a textbook claim; editions disagree.
- **The deliberately adversarial query** on every run — search the negative or null literature
  explicitly, or the known large trial by name. A verdict built only from the positive
  literature is publication bias, restated.

## 6. The anti-goal — the report that satisfies the words and still fails

Name the specific failure this decision invites, so the report can dodge it by design. The
most common: efficacy in a specialist RCT population generalising silently to a Klaeng OPD
patient with three comorbidities and no monitoring; the survey that catalogues the topic and
never answers the question; the balanced catalogue that lists both sides of a disagreement
and adjudicates neither; the answer hollowed by compression — a verdict whose load-bearing
trials arrive as clauses instead of studies.

---

## When the request carries two readings

Do not straddle. A brief built for two questions serves neither — the report answers both
halfway and neither fully, which is the unanswered survey by another route. Pick the reading
whose **wrong answer costs more**, build the brief for that one, and declare the choice in a
single line under the title (which reading you took, and the one it beat). If the two readings genuinely
tie on cost, or the request names a topic with no decision at all, that is not yours to resolve
by guessing — hand it back to intent-lock, which exists precisely to settle it.

## How the brief drives everything downstream

- **The search** hunts the evidence named in slots 3–5, runs the mandatory checks, and
  gathers **every source that genuinely bears on the question — capped by relevance, never
  by count.** A load-bearing study is never dropped to keep the report lean; an abstract
  that neither changes nor deepens the answer is never kept to look thorough.
- **The report** answers slot 1 in the form named in slot 2 — explicitly marked, wherever
  the chosen shape places it. The brief *informs* the report's shape; it no longer dictates
  it — structure is chosen for the question and the reader, topic-shaped sections included,
  and load-bearing studies get the full per-study treatment. See
  [report-craft.md](report-craft.md) for choosing the shape and the depth contract.
