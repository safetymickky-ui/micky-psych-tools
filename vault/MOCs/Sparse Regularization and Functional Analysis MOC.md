---
title: Sparse Regularization and Functional Analysis
created: 2026-07-30
type: moc
source: manual
tags: [sparse-regularization, functional-analysis, measure-theory, trend-filtering, moc]
links: ["Sparse Regularization: from L1 Corners to Dirac Measures"]
---

# Sparse Regularization and Functional Analysis

Topic map for the mathematics behind $\ell_1$-type regularization, from the finite-dimensional
lasso through to representer theorems over spaces of measures. The through-line of everything
filed here is one question:

> Why does an $\ell_1$ penalty produce exact zeros — and what does that fact become when the
> unknown is a function instead of a vector?

The short answer, and the spine of the artifact below: the $\ell_1$ ball has corners, and
minimizers land on corners. Move to functions and the corners become **Dirac measures**, which is
why the continuum theory needs distributions (to differentiate a step), measures (because a spike
has no density), and duality (because $\mathcal{M}(\Omega) = C_0(\Omega)^*$ is what buys the
compactness that makes a minimizer exist at all). Trend filtering is that continuum theorem,
discretized.

## Artifacts

- [[Sparse Regularization: from L1 Corners to Dirac Measures]] — a newcomer's comprehensive
  review in six parts (~33,400 words, 71 sections): $\ell_1$ vs ridge geometry → discrete
  difference operators, fused lasso and trend filtering → weak derivatives and Schwartz
  distributions → measures, BV, and why $L^1$ is not closed under concentration → Riesz
  representation, weak-\* convergence, Banach–Alaoglu, Krein–Milman → representer theorems for
  $\mathcal{M}$-norm regularization, splines as universal solutions, and the RKHS contrast.
  Assumes calculus and linear algebra only; builds measure theory and functional analysis from
  nothing. Every worked example is numerically verified.

## Notes

_None yet._ Candidates for atomization, each already a self-contained section of the artifact:
the corner-to-zero argument (§I.2–I.3), the order-$k$ trend filtering convention (§II.6), why
$\mathrm{D}H=\delta_0$ (§III.7), singular $\neq$ atomic (§IV.2), the $\mathcal{M}$-vs-$L^1$
concentration failure (§IV.8), $\mathrm{ext}\,B_{\mathcal M}=\{\pm\delta_x\}$ (§V.8), and the
extreme-point atom-count argument (§VI.4).

## Assets

_None yet._
