# Concept patterns — the form that fits each family

Each entry is a **menu**, not a build list. It names the **state**, candidate **views**,
candidate **controls with the question each asks**, the **invariants** for
`window.__lab.checks()`, and the **instructive regime** the controls must reach.

From each menu a walkthrough takes **one main view** and turns it into **5–14 steps**: the
first steps introduce the parts, the middle steps run the mechanism one piece at a time, the
last sums up. The menu's controls and instructive regimes become the **"what if" cases** on
the last step (0–4). Sliders are used only in a free-play lab (see the build contract).

A concept not listed here still follows the method:

> **What is the state? What one action changes it? What single picture makes that change visible?**
> Then: what would a learner *predict wrongly*, and which control proves them wrong?

Families 1–8 are machine learning and computer science. Families 9–11 are statistics,
pharmacology and clinical quantities, and computational psychiatry (all computed mode).
Family 12 holds the authored-mode patterns for concepts with no runnable model.

Three fields have a pack of their own under [fields/](fields/): endocrinology, general
psychiatry and computational psychiatry. Read the pack first for a concept in one of them; it
points back to the families here.

---

## 1. Optimization & training dynamics

*Gradient descent · SGD · momentum · Adam/RMSProp · learning-rate schedules · loss landscapes ·
conditioning & feature scaling · saddle points · convexity · early stopping · normalization*

- **State** — parameters θ, step *t*, loss L(θ), gradient ∇L, optimizer memory (velocity,
  second moments), the trajectory so far.
- **Views** — (a) **parameter space**: the real loss field as a heatmap/contours over two
  parameters, with the trajectory drawn on it; (b) **data space**: the current model against
  the data (fitted line, decision boundary); (c) **loss vs step**, log-scaled.
- **Controls** — learning rate *(does step size decide convergence or just speed?)* on a **log**
  slider reaching divergence · momentum *(what does inertia buy in a narrow ravine?)* ·
  initialization point, draggable *(does where you start decide where you end?)* · batch size
  *(what does the noise in SGD actually do?)* · feature scaling toggle *(why does standardizing
  inputs change everything?)* · noise σ · seed.
- **Invariants** — analytic ∇ vs central finite difference; loss non-increasing inside the
  stable step range; for least squares, the converged θ equals the normal-equation solution.
- **Instructive regimes** — lr above 2/λ_max → oscillation then overflow (report it, don't crash) ·
  lr ~1e-5 → visible stall · unscaled features → the classic zig-zag ravine · momentum 0.99 →
  overshoot and orbit.
- **The misconception to kill** — that "training failed" means the model is wrong. Usually the
  step size, the conditioning, or the initialization is wrong, and the same model converges.

## 2. Neural-network internals

*Perceptron · MLP · forward pass · backpropagation · activation functions · weight
initialization · vanishing/exploding gradients · dropout · batch norm · overfitting ·
capacity & the bias–variance trade-off*

- **State** — layer weights and biases, per-layer activations for the current input, per-layer
  gradients, epoch, train/validation loss history.
- **Views** — (a) **the network graph** (SVG): nodes and edges with edge thickness/colour bound
  to live weight magnitude and sign, node fill bound to activation; (b) **decision boundary**
  over a 2-D toy dataset, recomputed by the actual forward pass on a pixel grid; (c) **train vs
  validation loss** per epoch.
- **Controls** — depth and width *(does more capacity always fit better?)* · activation choice
  *(why did ReLU replace sigmoid?)* · initialization scale *(what breaks when every weight
  starts at 0, or at 10?)* · learning rate · dropout · dataset shape (blobs / moons / spiral /
  XOR) *(which shapes need depth?)* · noise level *(where does fitting become memorizing?)*
- **Invariants** — backprop gradients vs finite differences on every layer (the single most
  valuable check in this family); a linear model provably cannot separate XOR; softmax outputs
  sum to 1.
- **Instructive regimes** — deep sigmoid stack → per-layer gradient magnitudes visibly collapsing ·
  all-zero init → symmetric, never-differentiating units · high capacity + noisy small data →
  validation curve turning up while training loss keeps falling.
- **The misconception to kill** — that backprop is a mystery. It is the chain rule applied
  layer by layer, and the finite-difference check proves the arithmetic on screen.

## 3. Transformers & LLM internals

*Tokenization · embeddings · dot-product similarity · self-attention (QKᵀ/√d · softmax · V) ·
multi-head · masking · positional encoding · residual stream · temperature / top-k / top-p
sampling · context windows · KV cache*

- **State** — a short real sentence's tokens, the toy Q/K/V matrices (`d_k` ≈ 4–8), the attention
  weight matrix, the output vectors, and the sampling distribution over a small vocabulary.
- **Views** — (a) **attention heat matrix** (SVG, tokens on both axes, every cell the computed
  weight, hover for the raw score); (b) **the sentence** with arrow thickness from the selected
  query token to each key, so the matrix and the language line up; (c) **softmax bar chart** of
  the current row, redrawn as temperature changes.
- **Controls** — query token · temperature *(what is a "creative" model actually doing?)* on a
  range reaching both 0.01 and 5 · top-k / top-p *(what does truncating the tail remove?)* ·
  causal-mask toggle *(why can't a decoder look right?)* · head selector *(do heads specialize?)* ·
  positional-encoding on/off *(what does the model lose without order?)* · the `1/√d_k` scaling
  toggle *(why divide at all?)*
- **Invariants** — every attention row sums to 1; softmax is max-subtracted (feed it ±800 and it
  stays finite); the causal mask leaves a strictly lower-triangular matrix; scaling by `1/√d_k`
  measurably reduces the pre-softmax variance shown on screen.
- **Instructive regimes** — temperature → 0 collapses to argmax · temperature ≫ 1 approaches uniform ·
  scaling off → one cell saturates to ~1.0 and attention stops attending · mask off in a decoder
  → the token attends to its own future.
- **The misconception to kill** — that attention is magic. It is a similarity score, normalized,
  used as a weighted average — three steps you can watch happen on real numbers.
- **Scale caveat, mandatory here** — say on the page that this is a toy: real models use hundreds
  of dimensions, dozens of layers and heads, and learned rather than hand-set weights. The
  *arithmetic* is identical; the *capability* is not.

## 4. Classical machine learning

*k-means · kNN · decision trees · random forests · SVM & margins · the kernel trick · linear /
logistic regression · PCA · naive Bayes · regularization (L1 vs L2) · cross-validation ·
class imbalance · the confusion matrix*

- **State** — the generated dataset, the current model (centroids, split thresholds, support
  vectors, components, coefficients), iteration index, objective value.
- **Views** — (a) **data space**: points plus the model's partition — Voronoi cells, decision
  boundary, margin band, tree regions — computed by evaluating the real model on a pixel grid;
  (b) the **model's own structure**: the tree, the coefficient bars, the scree plot; (c) an
  **objective/metric trace** across iterations or across the regularization path.
- **Controls** — k, or depth, or C, or λ *(what does this knob trade away?)* · kernel choice ·
  distance metric · class balance · dataset shape and noise · seed *(does the answer depend on
  where you started?)* — for k-means, the seed control is the whole lesson.
- **Invariants** — k-means objective non-increasing at every half-step; PCA components
  orthonormal and reconstruction error equal to the discarded eigenvalue sum; logistic
  probabilities in (0,1); a reported accuracy recomputable from the shown confusion matrix.
- **Instructive regimes** — k-means with an unlucky seed → a permanently split cluster · k too small
  or too large · an unpruned tree → visibly shattered regions on noisy data · λ → 0 versus λ → ∞ ·
  99:1 imbalance → 99 % accuracy with zero recall, on screen, side by side.
- **The misconception to kill** — that these algorithms *find the truth*. They find the optimum of
  the objective you gave them, from the start you gave them.

## 5. Probability & information

*Bayes' rule · prior/likelihood/posterior · conditional probability & base rates · entropy ·
cross-entropy & KL divergence · maximum likelihood · the central limit theorem · sampling ·
confidence intervals · Monte Carlo · MCMC*

- **State** — the distribution parameters, drawn samples, running estimates, the posterior after
  *n* observations.
- **Views** — (a) **the distributions**, drawn from their real densities, prior and posterior
  overlaid; (b) **the samples accumulating** (a histogram filling, or a chain walking); (c) a
  **running-estimate trace** converging (or not) with its interval.
- **Controls** — prior strength *(when does the data overwhelm the prior?)* · base rate *(why is
  a 99 %-accurate test still usually wrong for a rare condition?)* · sample size on a log scale ·
  proposal width for MCMC *(what does a badly tuned proposal do?)* · number of repeated
  experiments · seed.
- **Invariants** — densities integrate to ≈1 on the drawn grid; the posterior equals the
  normalized prior × likelihood; the sample mean → the true mean within the stated tolerance;
  KL ≥ 0 with equality only at identity.
- **Instructive regimes** — base rate 0.1 % → the positive predictive value collapses · n = 5 →
  intervals that miss constantly · MCMC proposal far too wide (near-zero acceptance) or far too
  narrow (a chain that never explores).
- **The misconception to kill** — the base-rate fallacy, and the belief that "statistically
  significant" or "99 % accurate" means what it sounds like.

## 6. Algorithms & data structures

*Sorting (bubble/insertion/merge/quick/heap) · binary search · linked lists · stacks & queues ·
hash tables & collisions · trees, BSTs, balancing · heaps · graphs: BFS, DFS, Dijkstra, A\* ·
dynamic programming · recursion & memoization · greedy vs optimal*

- **State** — the array/graph/table itself, the algorithm's cursors (i, j, pivot, frontier,
  visited set), the call stack or DP table, and the operation counters.
- **Views** — (a) **the structure**: bars for an array, nodes and edges for a graph, cells for a
  DP table — with the *active* elements highlighted by role (comparing / swapping / frontier /
  settled / done); (b) **the bookkeeping**: the recursion stack, the priority queue's contents,
  or the DP table filling in; (c) **the counter panel**: comparisons, swaps, node expansions.
- **Controls** — algorithm selector *(same input, different cost — where does the difference come
  from?)* · input size · input pattern (random / sorted / reverse / few-unique / adversarial)
  *(does the input decide the cost?)* · speed · for graphs: heuristic weight *(when does A\* stop
  being optimal?)* · edge weights, including a negative one *(why does Dijkstra forbid this?)*
- **Invariants** — output non-decreasing **and** a permutation of the input (multiset equality —
  a sort that loses an element is the classic silent bug); every reachable node visited exactly
  once; no edge still relaxable at termination, and equality with brute force on a small
  instance; the DP table matching the naive recursion.
- **Instructive regimes** — already-sorted input into naive quicksort → quadratic, on the counter ·
  all-collide keys into the hash table → a linear chain · a negative edge into Dijkstra → a
  provably wrong answer, shown next to the correct one · an inadmissible A\* heuristic → a
  cheaper-looking but suboptimal path.
- **The misconception to kill** — that "sorted is sorted" and the choice of algorithm is taste.
  The counter, on adversarial input, is the argument.

## 7. Complexity & systems

*Big-O and growth rates · amortized analysis · recursion trees · P vs NP intuition · caches and
locality · memory layout · concurrency, races, deadlock, locks · scheduling · load balancing ·
consistency & consensus · compression · finite automata & parsing*

- **State** — measured operation counts at several *n*; or, for systems concepts, the simulated
  timeline: threads, resources held, queues, cache lines.
- **Views** — (a) **measured cost vs n**, the counted values plotted against the candidate curves
  (log-log, so a power law is a straight line whose slope is the exponent); (b) a **timeline/lane
  diagram** for concurrent or scheduled work — one lane per thread/core/server, blocks for
  operations, marks where a conflict occurs; (c) a **structure view** — the cache grid colouring
  hits and misses as the access pattern sweeps memory.
- **Controls** — n on a log slider · access pattern (sequential / strided / random) *(why is the
  same number of reads sometimes 10× slower?)* · thread count · lock on/off *(what exactly does a
  race lose?)* · scheduling policy · cache size and line size · arrival rate *(where does the
  queue explode?)*
- **Invariants** — the fitted slope on log-log axes matching the claimed exponent; total work
  conserved across threads; with locking, the shared counter equals the number of increments
  (and without it, visibly does not); simulated hits + misses equal total accesses.
- **Instructive regimes** — the unsynchronized counter losing updates, live · a deadlock reached by
  acquiring two locks in opposite order · utilization → 1 and the queue diverging · random access
  destroying cache locality.
- **The misconception to kill** — that operation count is runtime. Same asymptotics, different
  memory behaviour, order-of-magnitude difference — and a race condition that "works every time
  you run it" until the interleaving lands wrong.

## 8. Reinforcement learning

*Multi-armed bandits · exploration vs exploitation · ε-greedy / UCB / Thompson · Markov decision
processes · value iteration · policy iteration · Q-learning · discounting · reward shaping ·
credit assignment*

- **State** — the grid or bandit, the value/Q table, the policy, the agent's position, episode
  and step counters, cumulative reward and regret.
- **Views** — (a) **the world**: a grid with each cell's value as a heat fill and the greedy
  action as an arrow — value and policy in one picture; (b) **learning progress**: reward per
  episode, or cumulative regret for bandits; (c) **the Q-table** for the current state, as bars.
- **Controls** — ε *(what does an agent that never explores miss?)* · learning rate α · discount
  γ *(what does an agent that doesn't care about the future do?)* · reward structure, including a
  shaping term *(what does the agent do when you reward the wrong thing?)* · episode speed · seed.
- **Invariants** — the Bellman residual → 0; the greedy policy consistent with the value function;
  on a small MDP, learned values matching value iteration's fixed point.
- **Instructive regimes** — ε = 0 locking onto the first mildly good path forever · γ = 0 refusing all
  delayed reward · a shaped reward producing textbook reward hacking (looping on the bonus,
  never finishing) · α = 1 in a stochastic world, never settling.
- **The misconception to kill** — that the agent learns what you meant. It learns what you paid for.

---

## 9. Statistics & inference

*Sampling distributions · confidence intervals · p-values · power · regression to the mean ·
Bayes' rule · sensitivity/specificity/predictive values · ROC · multiple testing · mixed models*

- **State** — the population parameters, the sample (seeded), the statistic, the decision rule.
- **Views** — the sampling distribution building up draw by draw · a 2×2 natural-frequency grid
  (icons, not percentages) · an ROC curve with the moving threshold on two overlapping
  distributions.
- **Controls** — sample size *(what does n buy?)* · effect size *(how big must it be to be
  seen?)* · prevalence *(why does a good test fail in a rare disease?)* · threshold *(what do
  you trade when you move the cut-off?)* · number of tests.
- **Invariants** — empirical coverage of the interval tends to its nominal level; cells of the
  2×2 grid sum to N; PPV equals the Bayes' rule value; AUC from the curve equals the
  rank-statistic value.
- **Instructive regimes** — prevalence 1% → PPV collapses with 95% specificity · n = 10 →
  intervals that miss · 20 tests at α 0.05 → a "finding" from noise.
- **The misconception to kill** — that a p-value or a test's accuracy is the probability the
  conclusion is true.

## 10. Pharmacology & clinical quantities

*Receptor occupancy · dose–response (Emax, Hill) · half-life and accumulation · steady state ·
loading dose · drug interactions on clearance · therapeutic window · titration schedules*

**Clinical lane.** Every drug-specific number (EC50, half-life, occupancy threshold, dose) comes
from the sourced report and is listed in the lab spec with its place in that report. The model
form (one-compartment kinetics, the Hill equation) is established knowledge; the parameters are
not written from memory.

- **State** — dose, interval, time, concentration, effect or occupancy.
- **Views** — concentration over time with the therapeutic window as a band · an
  occupancy-versus-dose curve with the sourced thresholds marked.
- **Controls** — dose *(what does doubling the dose do to occupancy?)* · dosing interval
  *(what happens to the trough?)* · clearance or an inhibitor toggle *(what does an interaction
  do?)* · a missed dose.
- **Invariants** — concentration halves after one half-life; steady state is reached within
  about five half-lives and equals the closed-form value; effect stays inside 0–100% and is 50%
  at EC50.
- **Instructive regimes** — the flat top of a saturating curve (more dose, no more occupancy) ·
  accumulation with a long half-life · an inhibitor pushing a level out of the window.
- **The misconception to kill** — that effect scales in a straight line with dose.

## 11. Computational psychiatry

*Rescorla–Wagner and prediction error · temporal-difference learning · softmax choice and
inverse temperature · drift–diffusion · Bayesian belief updating and precision · model fitting
and parameter recovery*

- **State** — the agent's values or beliefs, the trial, the outcome, the prediction error.
- **Views** — value and prediction error across trials · choice probability against value
  difference · an evidence path drifting to a bound.
- **Controls** — learning rate α *(how fast should one outcome change a belief?)* · inverse
  temperature β *(is this exploring, or noise?)* · reward probability or a reversal *(what
  happens when the world changes?)* · drift rate and bound separation.
- **Invariants** — the Rescorla–Wagner value converges to the reward probability in a stable
  world; choice probabilities sum to 1; with zero drift the two bounds are hit equally often.
- **Instructive regimes** — α near 1 → the agent chases the last outcome · α near 0 → it never
  notices a reversal · low β → choices that look random with correct values.
- **The misconception to kill** — that a behaviour pattern identifies one parameter. Different
  parameters can produce the same choices.

---

## 12. Authored-mode patterns — concepts with no runnable model

Use these when nothing can be computed (defense mechanisms, a diagnostic pathway, a
classification, stages of a therapy). The content is written by hand in one `CONTENT` array,
each item with its source. The footer says the page is authored.

- **Reveal** — a set of cards or a labelled diagram; tapping one opens its explanation. The
  question each tap asks: *what is this, and how is it told apart from its neighbour?* Presets
  open the pairs people confuse.
- **Branch** — a pathway the user walks one decision at a time (yes/no, a finding present or
  absent). The view is the path so far and the next question. Presets are the instructive
  routes, including the one where the common shortcut goes wrong. Every branch ends at an outcome.
- **Sort / match** — items to place into groups or along an axis (immature → mature, first-line
  → last-line). The page answers each placement at once and says why. One correct place per item.
- **Compare** — two or three options with one switch that changes the case (age, comorbidity,
  severity) and shows what changes between them. The question: *what makes these differ here?*

Rules for all four: one pattern per lab; the control limits still hold (a set of cards is the
view, not a control); the status line says what the last action showed; nothing is scored,
timed, or graded unless the user asked for a quiz.

---

## Anti-patterns — things that look like explorables and aren't

- **The cosmetic slider** — it changes a colour, a zoom, or an animation speed, and asks no
  question about the concept. Speed and zoom are fine as *utilities*; they never count as the
  interaction.
- **The play button and nothing else** — that is a linear animation. Build it as watch mode,
  to the animation grammar, and do not call it interactive.
- **The dashboard** — every view and control from the family menu on one page. The page answers
  one question; take the one view and the few controls that carry it.
- **The authored curve** — a hand-drawn "dose–response" or "learning" curve presented as output.
  Compute it, or label it authored.
- **The rotatable surface you cannot descend** — a 3-D loss landscape you can spin but not run
  gradient descent on teaches "loss surfaces are bumpy" and nothing else.
- **The pretty-regime clamp** — sliders that cannot reach divergence, collapse, or the worst case.
  The lesson lives at the broken end.
- **The unlinked pair** — when a second view is used, two views that don't share state or
  don't update together.
- **Numbers that don't move** — an annotation frozen at its initial value while the model runs.
  Every number on screen is either live or explicitly labelled as fixed.
