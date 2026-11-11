# Field pack — computational psychiatry

Read this before choosing the view for any computational-psychiatry concept. **Family 11** in
[concept-patterns.md](../concept-patterns.md) holds the core menu (state, views, controls,
invariants). This pack adds what that entry does not: which task and which clinical question
each model belongs to, the confusions that matter, and where the field's claims must come
from. The build contract and every rule of the skill still apply.

## Field rules

- **Default reader:** a psychiatrist learning the methods. Clinical ideas may appear
  unexplained; every symbol is defined the first time it appears, and each formula is shown
  with numbers under it. Offer this as the default level at the intent-lock gate.
- **General lane:** the mechanics of a model. The page computes them, so they need no source.
- **Sourced:** any statement that links a parameter to a disorder, a symptom or a patient
  group, and any number taken from a paper. It carries the paper, and the word *proposed*
  where the field has not settled. A model that fits behaviour is not a mechanism; never draw
  it as one.
- **Simulation is seeded**, and simulated data are called simulated on the page.
- **Colour roles:** one colour for what the agent believes or values, one for what the world
  delivers, one for the prediction error between them. A fitted estimate and the true
  generating value never share a colour.

## Families

### C1. Learning from outcomes

*Rescorla–Wagner · learning rate as length of memory · separate rates for gains and losses ·
reward sensitivity · temporal-difference learning · Q-learning*

- **Task** — a probabilistic reward task, a two-armed bandit, reversal learning.
- **Clinical question** — is a blunted response to reward a problem of learning or of how
  much a reward is worth?
- **What-if cases beyond family 11** — a low learning rate against a low reward sensitivity:
  both slow the rise of value, and only the level it settles at tells them apart.
- **The confusion to remove** — that a slow learner and an indifferent one look different
  early on.

### C2. Choosing

*Softmax and inverse temperature · lapses · stickiness · exploring on purpose against
exploring by noise*

- **Task** — bandits.
- **View** — choice probability against the difference in value, the curve steepening with
  inverse temperature.
- **What-if cases** — inverse temperature near zero (choices look random although the values
  are right) · values scaled up and inverse temperature scaled down by the same factor (the
  choices do not change).
- **Invariants** — choice probabilities sum to 1; only the product of value scale and inverse
  temperature moves the curve.
- **The confusion to remove** — that noisy choices mean poor learning.

### C3. Planning

*Habitual (model-free) against goal-directed (model-based) control · the two-step task · the
weight between them*

- **Task** — the two-step task: a first choice, a common or rare transition, a reward.
- **View** — probability of repeating the first choice, split by rewarded or not and by
  common or rare transition: four bars.
- **What-if cases** — weight fully habitual (only reward matters) · fully goal-directed
  (reward and transition interact) · a mixture.
- **Invariants** — a purely habitual agent shows no reward-by-transition interaction.
- **Clinical question** — compulsivity. The link is sourced and *proposed*.
- **The confusion to remove** — that one choice shows which system made it. Only the pattern
  over many trials does.

### C4. Deciding from noisy evidence

*Drift–diffusion: drift rate, bound separation, starting point, non-decision time · the
trade of speed for accuracy*

- **Task** — two-choice decisions with response times.
- **Views** — evidence paths running to two bounds · the response-time distributions they
  produce, for correct and error responses.
- **What-if cases** — wider bounds (slower and more accurate) · lower drift (slower and less
  accurate) · a shifted starting point (fast errors toward the favoured side).
- **Invariants** — with zero drift and a central start, both bounds are hit equally often;
  mean decision time rises with bound separation.
- **The confusion to remove** — that slow responses mean poor evidence. Caution and poor
  evidence both slow a response; accuracy tells them apart.

### C5. Believing under uncertainty

*Bayes' rule with precision weighting · the Kalman gain as a learning rate that moves ·
volatility · priors that are too strong or too weak · active inference (overview)*

- **Views** — prior, evidence and posterior as three curves on one axis · a learning rate
  that rises and falls across trials.
- **What-if cases** — a prior that is too precise (evidence is ignored) · evidence trusted
  too much (every noisy sample is believed) · a world that turns volatile (the learning rate
  climbs).
- **Invariants** — the posterior mean is the precision-weighted average of prior and
  evidence; posterior precision is the sum of the two.
- **Clinical question** — accounts of psychosis and of anxiety. Sourced and *proposed*.
- **Active inference** is watch mode and an overview: say what the page leaves out.

### C6. From a model to a patient

*Likelihood of a sequence of choices · maximum likelihood · parameter recovery · model
recovery · hierarchical fitting and shrinkage · model comparison · posterior predictive
checks · test–retest reliability*

- **Views** — the likelihood surface over two parameters, with the ridge where they trade
  off · recovered against true values · individual estimates drawn toward the group.
- **What-if cases** — inverse temperature at zero (the surface is flat along the learning
  rate: it cannot be recovered) · few trials (a wide, shallow surface) · data from one model
  fitted best by another.
- **Invariants** — the maximum of the plotted surface is the reported estimate; simulated
  data recover the generating values within the stated tolerance, or the page says they do
  not.
- **The confusion to remove** — that a fitted parameter is a trait of the person. It is a
  property of person, task and model together.

### C7. Predicting from data

*Overfitting · leakage in cross-validation · calibration against discrimination · base rates
in a clinical predictor*

Use **family 4** (classical machine learning) and **family 9** (statistics and inference)
for the form. This field adds the clinical frame: what the prediction would change for the
patient, and what the base rate does to a positive result (see P3 in
[general-psychiatry.md](general-psychiatry.md)).

## Picking the family

| The concept is about | Family | Mode |
|---|---|---|
| How a value is learned from outcomes | C1 with family 11 | computed |
| How a value becomes a choice | C2 with family 11 | computed |
| Habit against planning | C3 | computed |
| Speed, accuracy and evidence | C4 with family 11 | computed |
| Beliefs, precision and volatility | C5 | computed; active inference as watch |
| Fitting, recovering, comparing models | C6 | computed |
| A prediction model on clinical data | C7 with families 4 and 9 | computed |
