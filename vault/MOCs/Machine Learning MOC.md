---
title: Machine Learning MOC
created: 2026-07-28
type: moc
source: vault-keeper
tags: [machine-learning, computer-science, moc, explorables]
links: []
---

# Machine Learning MOC

Map of content for machine learning, AI, and computer science — the technical, non-clinical
side of the vault. Interactive explorables in which an algorithm runs live and the learner
drives it (`ml-concept-lab`), watch-only concept animations (`concept-animation`), and
line-by-line code explanations (`code-explainer`) land here, alongside any notes on the
mathematics underneath them.

Room here for: calculus and linear algebra for ML, optimization and training dynamics,
neural-network internals, transformers and LLM internals, classical ML, probability and
information theory, algorithms and data structures, and reinforcement learning.

Clinical evidence and drug-level material belong under their own MOCs — nothing here
adjudicates a clinical question.

## Assets

- `assets/differentiation-three-ways.html` — **Three ways to get a derivative: symbolic ·
  numerical · automatic.** Interactive explorable built from the DeepLearning.AI *Mathematics
  for Machine Learning* C2 W1 lab. Three real engines run live in the page over one shared
  expression DAG: a symbolic differentiator (sum/product/quotient/power/chain rules plus
  constant folding), forward and central finite differences, and forward-mode automatic
  differentiation with dual numbers. Kills the misconception that autodiff is a finite
  difference with a very small `h` — it uses no `h` at all. The error-vs-`h` view shows both
  difference schemes bottoming out near √ε and ∛ε and then getting *worse*, against a flat
  exact floor with no step size to choose; the cost bars show that composing the logistic map
  six times gives a printed derivative of 2,303 nodes over only 64 distinct sub-expressions,
  while the dual sweep stays at 60 operations. Five presets reach the failure regimes
  (cancellation at `h`=1e-15, truncation at `h`=0.5, the `|x|` kink where all three methods
  return different answers, and expression swell); five self-checks assert live invariants.
  Self-contained HTML, no external anything, seeded, keyboard-operable, reduced-motion path.
  Preview: `assets/differentiation-three-ways.preview.png`. Source skill: `ml-concept-lab`.

## Notes

_None yet._
