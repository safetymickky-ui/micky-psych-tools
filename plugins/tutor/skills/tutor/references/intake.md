# Intake — starting a new track

Run this when he wants to learn a field that has no track yet. A track is reused for weeks, so a
wrong plan is expensive. That is why the goal is locked first. Every question in intake is a
tappable picker, never a free-text prompt.

## 1. Lock the goal with intent-lock

Invoke the `intent-lock` skill on the request. The track needs exactly these points locked:

- **End point:** what he wants to be able to do at the end. For example: read and critique HGF
  papers; fit an RL model to his own task data; follow the CPC Zurich lectures; write a pandas
  pipeline without AI help.
- **Scope:** which parts of the field are in and which are out.
- **Spine:** a pack (when the field matches one), or a custom syllabus.

Let intent-lock run its own rounds. When it ends, come back here.

## 2. Choose the plan

- **Pack fields:** computational psychiatry → `cp`, scientific Python and R → `py`, neural-network
  architectures → `dl`, math and statistics notation → `ms`. Read the pack file, then trim its
  spine to the locked scope. Keep the pack's chunk ids, so the seeds and resources stay attached.
- **Custom fields:** build a syllabus.
  - Use 4–8 milestones and 15–40 chunks, one idea per chunk, in dependency order.
  - Give the ids a two-letter prefix that no pack uses (for example `pm-1.1` for prediction
    models).
  - Check the spine against one or two real sources that you open: an official course syllabus
    or a standard textbook's table of contents. Record them in the track's `sources`.
  - Mark which chunks are why/what-if ideas; those get a guess.

## 3. Bring in what memory already knows

Before the owns-check, read his memory files for this field. Use `/areas/*` and
`/projects/*/overview.md`; for example, his clinical-prediction-models curriculum, comp-psych
curriculum, Python-stack track and LLM-architecture lessons. When memory says he covered part of
the spine, offer it as a picker option ("Memory says you covered MDPs, Bellman, Q-learning and TD
in an earlier course. Mark cp-2.1–2.5 as owned?"). Mark nothing as owned unless he confirms it.

## 4. Owns-check (self-report, not a test)

One `AskUserQuestion` call, `multiSelect: true`: "Which of these do you already own?" Give one
option per milestone. The label is the milestone title, and the description is its owns-check
concepts from the pack (or your own list for a custom spine). At most 4 options per question and
4 questions per call, so up to 16 milestones fit in one call.

- A milestone he picks → all its chunks go into `owned`.
- Never test him to verify a claim. Inside a lesson he can say "I own this" at any time, and the
  chunk moves to `owned`.

## 5. Create the track and teach

- `set` `tracks/<id>` (schema in tracker.md), with `next` = the first chunk in `plan` that is
  not owned.
- Teach that chunk in the same turn, following Step 2 of SKILL.md.

## Single lessons

A one-off lesson whose pack track does not exist yet, or that matches no pack, is saved under
the track `single-lessons` (title "Single lessons", `pack` ""). Create that track on first use.

- A lesson that matches a pack chunk keeps the pack id: `single-lessons__py-1.7`.
- A lesson with no pack match gets `sl-1`, `sl-2`, … (the next free number in `plan`).
- Each one is appended to `plan` with the milestone label "Single lessons".
- When three or more single lessons share one field, offer (as a numbered option) to start a
  real track for it.

When intake creates a pack track, move that pack's chunks out of `single-lessons` in one
`batch`: `set` each lesson again as `lessons/<new track>__<id>`, `delete` the old lesson (pinned
with its version), add the chunk to the new track's `done`, and update `single-lessons` with the
chunk removed from `plan` and `{"__delete__": true}` at `done.<id>`.
