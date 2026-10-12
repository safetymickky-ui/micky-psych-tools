# tutor

Teaches a new field one small chunk at a time, in the way Micky set out in an interview on
2026-10-12. Every lesson is saved to one phone-readable **Tutor tracker** page.

For any field below his Specialist level: coding (Python, R, SQL, software-engineering basics),
computational psychiatry, ML and neural networks, math and statistics notation, and anything
else he is still learning. His specialist fields (clinical psychiatry, psychopharmacology,
neuroscience, psychotherapy) are out of scope.

## A chunk

```
/tutor comp-psych
→ cp-2.4 TD learning
  [picker] cp-2.4 TD learning: RW learns only when the outcome arrives. How could a
  learner give value to a cue that comes 2 s before the reward?
    · 3 short predictions (the fitting one mixed in, none marked) · Just tell me · Other
→ (his pick or his own words) → what fits, what is missing → the answer first, in words he owns
→ dependency chain → anchor (Rescorla-Wagner) and where it breaks
→ every symbol named, a worked example computed in code, a table beside it
→ failure modes and term collisions → one resource line
→ 1. Deeper: why γ < 1 keeps values finite
  2. Next: cp-2.5 Q-learning
  3. Show it in code
  4. Visualize: drag γ and α and watch δ move to the cue (short interview in ml-concept-lab)
```

## The contract

| Rule | What it means |
| --- | --- |
| Answer first | The lesson opens with the idea itself; nothing is held back for him to discover. |
| Guess only before why/what-if ideas | One `AskUserQuestion` picker: three predictions, `Just tell me`, or his own words. Never scored. The pack's `guess` field decides; notation and procedures are explained first. Text prompt only when no picker exists. |
| No quizzes, checks or reviews | A chunk ends when he picks the next option. A quiz happens only if he asks in the moment. |
| Code that really ran | Every snippet runs in the session first; only real output is shown. |
| He writes code only on request | "give me an exercise" → a scaffold that fades over four levels. |
| Everything is saved | Each lesson goes to the tracker under its track and chunk. |

His standing preferences apply throughout: his language per message, short plain sentences,
bullets, no praise, each error named with its fix, no closing summary.

## The Tutor tracker

A private artifact titled "Tutor tracker" (template in `skills/tutor/assets/tracker.html`). It
shows a card per track (progress by milestone, next chunk), a chunk map per track, and each
saved lesson: the guess, the lesson text, the code with its real output, depth layers, the
errors named and their fixes, and sources. The page only reads. The skill writes through the
artifact database (`tracks/<id>`, `lessons/<track>__<chunk>`); see
`skills/tutor/references/tracker.md`. The skill finds the tracker by its title and creates it
from the template if it is missing.

## Domain packs

`skills/tutor/references/packs/`, each a spine of 43–45 chunks with an anchor, a guess, a seed
computed in Python, and checked resources per chunk:

- `comp-psych.md` (`cp`): RL → fitting → model comparison → DDM → Bayesian observers/HGF →
  clinical applications and limits → data-driven methods, tagged to the CPC Zurich programme.
- `python-r.md` (`py`): NumPy → pandas → Polars → scikit-learn → gradient-boosted trees →
  SciPy → Matplotlib/seaborn → R for models → software-engineering basics.
- `ml-dl.md` (`dl`): one neuron → MLP → losses → backprop → training practice → CNNs → RNNs →
  transformers and LLMs → VAEs, GNNs and clinical failure modes.
- `math-stats.md` (`ms`): reading notation → linear algebra → calculus → probability →
  estimation and the LR/Wald/score tests → optimization → MCMC and variational inference.

Any other field gets a custom syllabus at intake, checked against a real course or textbook.

## Use

- `/tutor` lists the tracks with their next chunks; `/tutor <track>` resumes one;
  `/tutor <new topic>` starts a track (intent-lock locks the goal, then a self-report
  "which of these do you already own?" picker).
- In chat: "teach me …", "explain … from scratch", "next chunk", "continue my track",
  "give me an exercise", "สอน …", "อยากเรียน …".

## Install

```
/plugin marketplace add safetymickky-ui/micky-psych-tools
/plugin install tutor@micky-psych-tools
```

## Files

```
skills/tutor/SKILL.md                    the contract and the procedure
skills/tutor/references/teaching-rules.md   one chunk, done well
skills/tutor/references/coding-mode.md      READ, worked code, exercises on request
skills/tutor/references/intake.md           new tracks
skills/tutor/references/tracker.md          find, read and write the tracker
skills/tutor/references/packs/*.md          four domain packs
skills/tutor/assets/tracker.html            the tracker page template
commands/tutor.md                           /tutor
evals/tutor/                                trigger and near-miss cases
```

## Boundaries

Live explorables (ml-concept-lab) and animations (concept-animation) are offered as numbered
options, never run unasked. A whole code file explained as a page goes to code-explainer. A
clinical evidence question goes to pubmed-research-note. Lessons are not filed to the vault;
the tracker page is their home.
