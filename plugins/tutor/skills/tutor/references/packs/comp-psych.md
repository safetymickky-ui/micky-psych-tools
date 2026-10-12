# Computational psychiatry pack

Scope: theory-driven models (RL, fitting, DDM, Bayesian observers), their clinical use and limits, then data-driven prediction.
CPC tags are lecture and tutorial titles from the official CPC Zurich page, which still showed the 2026 program (7–12 Sep 2026) on 2026-10-12; recheck when the 2027 program appears.
His level here: developing. He owns RW/RPE, intro MDP/TD/Q-learning, logistic regression, MLE (in progress), CV and leakage, mixed models, entropy/KL: move fast there, but still define every symbol.
Build from scratch: the likelihood of a choice sequence, the recovery and model-comparison workflow, the DDM, Kalman/HGF, active inference (overview only). Code: Python numpy/scipy for single-subject fits; hBayesDM, HSSM or pyhgf for hierarchical fits.

## Spine

### M1 — Foundations: what a computational model is · CPC: Introduction to Computational Modeling; Building a Model: A Step-by-step guide

Owns-check: generative model, latent variable, Marr's three levels, theory- vs data-driven, simulation

- **cp-1.1 What a computational model is** — needs — · anchor: logistic regression p = 1/(1+e^(−Xβ)) · guess: — · seed: same formula, but the input is a latent value made by a learning rule, not a measured column: −1 + 0.5·4 = 1 → p = 1/(1+e^(−1)) = 0.731 · code: no · res: Primer ch 2; CPC (Introduction to Computational Modeling)
- **cp-1.2 Marr's three levels** — needs cp-1.1 · anchor: a drug described at clinical-effect (what), mechanism (how) and receptor (where) levels · guess: — · seed: one goal (track reward), two algorithms: V = 0, r = 1 → V′ = 0 + α(1 − 0) = 0.1 with α = 0.1, but 0.5 with α = 0.5 · code: no · res: Primer ch 1
- **cp-1.3 Theory-driven vs data-driven** — needs cp-1.1 · anchor: his clinical-prediction-model curriculum (data-driven) vs PK/PD models (theory-driven) · guess: "200 patients and 300 features: which approach overfits first, and why?" · seed: 100 events / 300 predictors → EPV = 0.33 (classic rule ≥ 10); an RW fit compresses 200 choices into 2 parameters · code: no · res: Primer ch 2; CPC (Machine Learning Basics)
- **cp-1.4 Simulate before you fit** — needs cp-1.1 · anchor: sketching the expected dose–response curve before a trial · guess: "Why simulate fake patients from your model before you collect real data?" · seed: agent with p(A) = 0.7 over 100 trials → expected 70 A choices, SD = √(100·0.7·0.3) = 4.58 · code: yes · res: Ten rules ("Simulate, simulate, simulate!")

### M2 — Reinforcement-learning models · CPC: Reinforcement Learning; Models of Action Selection: MDPs; tutorial C (hBayesDM)

Owns-check: Rescorla-Wagner, prediction error, learning rate, TD error, Q-learning, softmax

- **cp-2.1 Rescorla-Wagner: notation** — needs cp-1.1 · anchor: RW and dopamine RPE (owned) · guess: — · seed: V = 0.5, r = 1, α = 0.2 → δ = r − V = 0.5 → V′ = V + αδ = 0.6 (′ = next trial) · code: no · res: RL book §14.2.2
- **cp-2.2 Learning rate = memory length** — needs cp-2.1 · anchor: drug half-life (first-order elimination) · guess: "A patient has α near 1. Good or bad in a stable world? In a changing one?" · seed: weight on the outcome k trials back = α(1−α)^k: α = 0.5 → 0.5, 0.25, 0.125; memory half-life = ln 0.5 / ln(1−α): α = 0.1 → 6.58 trials, α = 0.5 → 1.0 trial · code: yes · res: RL book §2.5
- **cp-2.3 Softmax choice rule** — needs cp-2.1 · anchor: logistic regression: with 2 options p(A) = 1/(1+e^(−β(Q_A − Q_B))), β = slope · guess: "If β falls to 0, what does choice look like, and what could a clinician mistake it for?" · seed: Q_A = 0.6, Q_B = 0.4 → p(A) = 0.731 (β = 5), 0.5 (β = 0), 0.982 (β = 20) · code: yes · res: RL book §2.8
- **cp-2.4 TD learning** — needs cp-2.1 · anchor: RW plus Bellman's equation (owned) · guess: "RW learns only when the outcome arrives. How could a learner give value to a cue that comes 2 s before the reward?" · seed: V(s) = 0.5, r = 1, γ = 0.9, V(s′) = 0.4 → δ = 1 + 0.9·0.4 − 0.5 = 0.86; α = 0.1 → V(s) = 0.586 · code: no · res: RL book §6.1, §15.6
- **cp-2.5 Q-learning** — needs cp-2.4 · anchor: MDP, Bellman, Q-learning (owned, intro level) · guess: — · seed: Q(s,a) = 0.2, r = 0, γ = 0.9, max Q(s′,·) = 0.8, α = 0.5 → δ = 0.52, Q = 0.46; bandit form (γ = 0): Q_A = 0.5, r = 0, α = 0.3 → 0.35, unchosen Q_B unchanged · code: yes · res: RL book §6.5; NMA W3D4
- **cp-2.6 Add-ons: reward sensitivity ρ, α+/α−, perseveration** — needs cp-2.3 · anchor: dose–response: ρ sets the ceiling (like Emax), α sets the speed · guess: "Low ρ and low α both slow the rise of V. What in the curve tells them apart?" · seed: update V += α(ρr − V), 5 rewards (r = 1) from V = 0: ρ = 1, α = 0.3 → 0.832; ρ = 0.5, α = 0.3 → 0.416; ρ = 1, α = 0.15 → 0.556 · code: yes · res: anhedonia meta-analysis; hBayesDM (prl_rp)
- **cp-2.7 Model-free vs model-based values** — needs cp-2.5 · anchor: habit vs goal-directed action, outcome devaluation; expected value Σp·x · guess: "If the reward is devalued, which system changes choice at once, with no new experience?" · seed: P(common) = 0.7, second-stage values X = 0.8, Y = 0.2 → Q_MB(A) = 0.7·0.8 + 0.3·0.2 = 0.62, Q_MB(B) = 0.38 · code: no · res: RL book §8.1, §14.6
- **cp-2.8 Two-step task and the weight w** — needs cp-2.7, cp-2.3 · anchor: logistic regression with an interaction: stay ~ reward × transition · guess: — · seed: Q_net = w·Q_MB + (1−w)·Q_MF; Q_MB(A) = 0.62, Q_MF(A) = 0.30, w = 0.4 → 0.248 + 0.180 = 0.428 · code: yes · res: two-step paper; hBayesDM (ts_par4)

### M3 — Fitting one learner: likelihood and MLE · CPC: Fitting a Model: Maximum Likelihood

Owns-check: likelihood, log-likelihood, MLE, optimizer, logit link, standard error

- **cp-3.1 Likelihood of a choice sequence** — needs cp-2.3 · anchor: Bernoulli likelihood of logistic regression (MLE, in progress) · guess: "Why sum log-probabilities instead of multiplying probabilities over 200 trials?" · seed: the model gave p = 0.731, 0.5, 0.9 to the 3 choices made → LL = −0.313 − 0.693 − 0.105 = −1.112, NLL = 1.112; 0.7^200 = 1.05e−31 (underflow risk) · code: yes · res: Ten rules ("Fit the parameters"); NMA W1D2
- **cp-3.2 MLE with scipy.optimize.minimize** — needs cp-3.1 · anchor: glm() also finds β by maximizing the likelihood · guess: — · seed: 7 of 10 choices = A, constant-p model: NLL(0.5) = 6.931, NLL(0.7) = 6.109; minimize (L-BFGS-B) → p̂ = 0.700 · code: yes · res: scipy minimize; NMA W1D2
- **cp-3.3 Transforms, bounds and restarts** — needs cp-3.2 · anchor: logit link in logistic regression · guess: — · seed: fit on an unbounded scale, then map back: α = 1/(1+e^(−x)): x = 0 → 0.5, x = −2 → 0.119; β = e^y: y = 1.609 → 5.00; run 10–20 random starts, keep the lowest NLL · code: yes · res: scipy minimize
- **cp-3.4 Parameter recovery** — needs cp-3.2, cp-1.4 · anchor: lab-assay spike recovery: add a known amount, measure it back · guess: "If a patient's β = 0, can you recover their α?" · seed: β = 0 → every choice has p = 0.5 → NLL = 100·ln 2 = 69.31 for α = 0.1 and α = 0.9 alike: flat likelihood, α not identifiable · code: yes · res: Ten rules ("Check that you can recover your parameters"); Primer ch 2
- **cp-3.5 Uncertainty from curvature** — needs cp-3.2 · anchor: the SE column of glm() output · guess: "A sharp NLL valley or a flat one: which estimate do you trust?" · seed: p̂ = 0.7, n = 10 → curvature d²NLL/dp² = n/(p(1−p)) = 47.62 → SE = 1/√47.62 = 0.145, same as √(0.7·0.3/10) · code: yes · res: NMA W1D2; scipy minimize

### M4 — Comparing models and fitting groups · CPC: Selecting a Model: BMS; Fitting a Model: VB & MCMC

Owns-check: AIC, BIC, k-fold CV, confusion matrix, partial pooling, fixed vs random effects

- **cp-4.1 AIC and BIC** — needs cp-3.2 · anchor: AIC/BIC in regression; a price for complexity · guess: "AIC and BIC disagree. Which one favors the simpler model as trials grow, and why?" · seed: AIC = 2k + 2NLL, BIC = k·ln n + 2NLL, n = 200: M1 (k = 2, NLL = 120) → 244 / 250.6; M2 (k = 3, NLL = 118) → 242 / 251.9 → AIC picks M2, BIC picks M1 · code: no · res: Ten rules ("Can you arbitrate between different models?"); Primer ch 2
- **cp-4.2 Cross-validation for learning models** — needs cp-4.1 · anchor: k-fold CV and leakage (owned) · guess: "Why is random trial-wise k-fold unsafe for a learning model?" · seed: held-out NLL per trial 0.58 vs 0.61 → geometric-mean p of the choices made = e^(−0.58) = 0.560 vs e^(−0.61) = 0.543 · code: yes · res: NMA W1D2
- **cp-4.3 Model recovery: the confusion matrix** — needs cp-4.1, cp-3.4 · anchor: sensitivity vs PPV of a diagnostic test · guess: "Model A wins in your patients. If data simulated from B often fit A best, how much do you trust the win?" · seed: 100 sims per model: A→A 85, A→B 15, B→A 30, B→B 70 → p(fit A | true A) = 0.85; p(true A | fit A) = 85/115 = 0.74 · code: yes · res: Ten rules ("Can you arbitrate between different models?")
- **cp-4.4 Hierarchical Bayesian fitting** — needs cp-3.2 · anchor: lme4/brms random effects and BLUP shrinkage · guess: "A patient with only 40 trials gets an extreme α. What should the group data do to it?" · seed: own α̂ = 0.9 (SE 0.2), group mean 0.4 (SD 0.1) → precision-weighted (0.9/0.04 + 0.4/0.01)/(1/0.04 + 1/0.01) = 62.5/125 = 0.50 · code: yes · res: hBayesDM; reliability paper
- **cp-4.5 Group-level model selection** — needs cp-4.1, cp-4.4 · anchor: fixed vs random effects in mixed models · guess: "One subject strongly favors M2; two weakly favor M1. Which model wins the group?" · seed: per-subject ΔBIC (M2 − M1) = −20, +3, +4 → sum −13 (fixed effects: M2), yet 2 of 3 prefer M1; random-effects BMS estimates how common each model is · code: no · res: CPC (Selecting a Model: BMS)
- **cp-4.6 Validate the winning model** — needs cp-4.3 · anchor: calibration plot (predicted vs observed) · guess: "Your model wins on BIC. Can it still be wrong in a way that matters?" · seed: simulate from the fitted parameters: p(stay | reward) = 0.75 simulated vs 0.62 observed → a 0.13 gap that BIC did not show · code: yes · res: Ten rules ("Validate (at least) the winning model")

### M5 — Sequential sampling: the drift-diffusion model · CPC: Models of Action Selection: DDM; tutorial D

Owns-check: drift rate, boundary separation, non-decision time, starting point, speed–accuracy trade-off

- **cp-5.1 The DDM and its parameters** — needs cp-1.1 · anchor: Bayesian log-odds updating: evidence piles up to a threshold · guess: — · seed: start at a/2, drift v = 1, boundary a = 2, noise s = 1 → P(correct) = 1/(1+e^(−va/s²)) = 0.881 · code: yes · res: HSSM; NMA W3D3 (SPRT)
- **cp-5.2 Mean RT and the speed–accuracy trade-off** — needs cp-5.1 · anchor: dose–response: accuracy is a sigmoid in v·a · guess: "You tell a patient 'be careful'. Which parameter should change, and which should not?" · seed: mean DT = (a/(2v))·tanh(va/(2s²)), v = 1, s = 1, t0 = 0.3 s: a = 1 → P = 0.731, RT = 0.231 + 0.3 = 0.531 s; a = 2 → P = 0.881, RT = 0.762 + 0.3 = 1.062 s · code: yes · res: HSSM
- **cp-5.3 Why fit RT and accuracy together** — needs cp-5.2, cp-3.4 · anchor: identifiability (cp-3.4): one summary cannot pin two parameters · guess: "Two patients both score 88% correct. Same processing ability?" · seed: (v = 1, a = 2) and (v = 2, a = 1) both give P = 0.881, but mean DT = 0.762 vs 0.190 s · code: yes · res: HSSM
- **cp-5.4 Fitting DDMs** — needs cp-5.3, cp-3.2 · anchor: the trial likelihood of cp-3.1, now for a (choice, RT) pair · guess: — · seed: EZ closed form (s = 0.1): accuracy 0.802, mean RT 0.723 s, RT variance 0.112 s² → v = 0.10, a = 0.14, Ter = 0.30 s (EZ assumes an unbiased start and no between-trial variability) · code: yes · res: HSSM; hBayesDM (choiceRT_ddm)
- **cp-5.5 RL-DDM: learning sets the drift** — needs cp-5.1, cp-2.3 · anchor: softmax β ↔ drift scale m · guess: "When the two options have almost equal value, what happens to RT?" · seed: v = m·(Q_A − Q_B) = 4·0.25 = 1 → mean DT = 0.762 s (a = 2, s = 1); Q_A = Q_B → v = 0 → DT = (a/2)²/s² = 1.0 s · code: yes · res: hBayesDM (pstRT_rlddm1); HSSM

### M6 — Bayesian observer models · CPC: Bayesian Models of Perception; Models of Perception: Predictive Coding; From Perception to Action: HGF; Models of Action Selection: Active Inference; tutorials A (HGF), B (Active Inference)

Owns-check: prior and posterior, precision, Bayesian updating, Kalman filter, volatility, KL divergence

- **cp-6.1 Precision-weighted updating** — needs cp-2.1 · anchor: Bayesian updating (owned) + RW: the learning rate becomes a precision ratio · guess: "If the sensory signal gets noisier, should the learning rate go up or down?" · seed: prior μ = 0, σ² = 1; observation x = 2: σx² = 1 → weight 1/(1+1) = 0.5 → μ′ = 1.0; σx² = 4 → weight 0.25/1.25 = 0.2 → μ′ = 0.4 · code: no · res: NMA W3D2
- **cp-6.2 Kalman filter: RW with a computed learning rate** — needs cp-6.1, cp-2.2 · anchor: α as memory length (cp-2.2) · guess: "In a world that keeps changing, should the learning rate shrink to 0 as in a fixed world?" · seed: posterior var 0.5, noise var 1: no drift → gain 0.5/1.5 = 0.333; drift var 0.5 → prior var 1.0 → gain 1.0/2.0 = 0.5 · code: yes · res: NMA W3D3; hBayesDM (bandit4arm2_kalman_filter)
- **cp-6.3 HGF: the binary 3-level model** — needs cp-6.2, cp-2.3 · anchor: RW δ, logistic sigmoid s(·), Bayesian updating · guess: "If a patient believes the world is very volatile, how big are the updates after each surprise?" · seed: μ2 = 0 → μ̂1 = s(0) = 0.5; outcome u = 1 → δ1 = 0.5; σ̂2 = σ2 + e^(κμ3+ω2) = 1 → π2 = 1 + 0.5·0.5 = 1.25 → μ2′ = 0.5/1.25 = 0.40 → p = s(0.4) = 0.599; σ̂2 = 2 (higher ω2) → μ2′ = 0.667, p = 0.661 · code: yes · res: pyhgf ("Zurich CPC I"); TAPAS (hgf-toolbox)
- **cp-6.4 Predictive coding** — needs cp-6.1 · anchor: RW δ passed up a hierarchy; precision as gain · guess: "If sensory precision is set too high, could random noise feel meaningful?" · seed: prediction error 1, weight π_x/(π_x + π_prior): π_x = 4, π_prior = 1 → update 0.8; π_x = 1, π_prior = 4 → update 0.2 · code: no · res: CPC (Models of Perception: Predictive Coding); pyhgf
- **cp-6.5 Active inference (overview only)** — needs cp-6.4 · anchor: KL divergence and entropy (owned) · guess: — · seed: "risk" = KL(predicted ‖ preferred outcomes): q = (0.8, 0.2), p = (0.95, 0.05) → 0.8·ln(0.8/0.95) + 0.2·ln(0.2/0.05) = 0.140 nats · code: no · res: CPC (Models of Action Selection: Active Inference, tutorial B)
- **cp-6.6 Observing the observer: perceptual + response model** — needs cp-6.3, cp-3.1 · anchor: the softmax layer of cp-2.3, now placed on top of beliefs · guess: "Two patients hold the same beliefs but choose differently. Which part of the model differs?" · seed: unit-square sigmoid p(y = 1) = μ̂1^ζ/(μ̂1^ζ + (1−μ̂1)^ζ) with μ̂1 = 0.599: ζ = 1 → 0.599; ζ = 2 → 0.690 · code: yes · res: TAPAS (hgf-toolbox); pyhgf ("Using custom response models")

### M7 — Clinical applications and limits · CPC: Depression & Affective Disorders; Schizophrenia; Day 5 psychosis talks

Owns-check: anhedonia, reward sensitivity, aberrant salience, jumping to conclusions, habit vs goal-directed, test–retest reliability

- **cp-7.1 Anhedonia: reward sensitivity vs learning rate** — needs cp-2.6 · anchor: consummatory pleasure vs learning from reward (the Primer ch 7 split); Emax vs rate from cp-2.6 · guess: "Is anhedonia slow learning, or rewards counting less? How would the curves differ?" · seed: after 20 rewards: ρ = 0.5, α = 0.3 → V = 0.500 (stuck at the ceiling ρ); ρ = 1, α = 0.05 → V = 0.642 (still rising toward 1) · code: yes · res: anhedonia meta-analysis; Primer ch 7
- **cp-7.2 Psychosis: aberrant salience and belief updating** — needs cp-6.3, cp-6.4 · anchor: Bayesian log-odds updating (owned) · guess: "A patient decides after one bead. Is that irrational if the jars are 85:15?" · seed: each bead adds ln(0.85/0.15) = 1.735 log-odds; P(jar) = 0.85 after 1 bead, 0.970 after 2 same-color beads · code: no · res: Primer ch 6; CPC (Schizophrenia)
- **cp-7.3 Compulsivity and model-based control** — needs cp-2.8 · anchor: habit theory of OCD; symptom dimensions from factor analysis · guess: — · seed: after a rewarded rare transition (Q_MF: A = 0.6, B = 0.4; second-stage values X = 0.2, Y = 0.8 → Q_MB: A = 0.38, B = 0.62; β = 5): w = 0.8 → p(stay) = 0.319; w = 0.2 → 0.636 · code: yes · res: compulsivity paper; two-step paper
- **cp-7.4 Reliability of parameters** — needs cp-4.4 · anchor: ICC from lme4; PHQ-9 test–retest · guess: "If α has test–retest reliability 0.4, how high can its correlation with a symptom score go?" · seed: true r = 0.5, reliability 0.4 (α) and 0.8 (PHQ-9) → observed r = 0.5·√(0.4·0.8) = 0.283 · code: no · res: reliability paper
- **cp-7.5 The cost of unreliability: sample size** — needs cp-7.4 · anchor: power calculation · guess: "With an unreliable α, how many patients do you need to detect the same true effect?" · seed: 80% power, two-sided 0.05: n = ((1.960 + 0.842)/atanh r)² + 3: r = 0.5 → 29.0 → 30; r = 0.283 → 95.8 → 96 · code: yes · res: reliability paper

### M8 — Data-driven computational psychiatry · CPC: Machine Learning Basics; Machine Learning Advanced; tutorial F (PCNtoolkit)

Owns-check: clinical prediction model, calibration, decision curve, nested CV, normative model, deviation z-score

- **cp-8.1 Prediction models in psychiatry** — needs cp-1.3 · anchor: his clinical-prediction-model curriculum (AUC, calibration, decision curves) · guess: "Your model moves to a new hospital. What usually breaks first: AUC or calibration?" · seed: net benefit at threshold 0.2, TP = 20, FP = 30, n = 100 → 0.20 − 0.30·(0.2/0.8) = 0.125 · code: no · res: CPC (Machine Learning Basics)
- **cp-8.2 Nested CV, leakage and site effects** — needs cp-8.1, cp-4.2 · anchor: data leakage (owned) · guess: "You pick the 20 best features using all patients, then run CV. Is the CV AUC honest?" · seed: 5 outer folds × (5 inner folds × 10 λ values + 1 refit) = 255 fits; scaling, feature selection and site correction go inside each training fold · code: yes · res: CPC (Machine Learning Advanced)
- **cp-8.3 Model parameters as features (generative embedding)** — needs cp-8.1, cp-4.4 · anchor: using a lab value as a predictor instead of the raw signal · guess: "Why might 3 fitted parameters predict outcome better than 200 raw choices?" · seed: 100 events: 200 raw trial features → EPV 0.5; 3 parameters → EPV 33.3 · code: no · res: TAPAS (genbed)
- **cp-8.4 Normative modeling** — needs cp-8.1 · anchor: pediatric growth charts and centiles · guess: "Two patients share a diagnosis but deviate in different brain regions. What does a case–control mean difference hide?" · seed: cortical thickness 2.30 mm, predicted 2.60 mm for age/sex/site, predictive SD 0.12 → z = (2.30 − 2.60)/0.12 = −2.5 → about the 0.6th centile · code: yes · res: PCNtoolkit; CPC (tutorial F)

## Anchors

- Softmax with 2 options → logistic regression on Q_A − Q_B with slope β; breaks: Q is latent and the model rebuilds it after every trial, so the "predictor" is never measured.
- Likelihood of a choice sequence → Bernoulli likelihood of logistic regression; breaks: p on each trial depends on the person's own past choices and outcomes, so the model must run in trial order.
- Learning rate α → drug half-life: old outcomes fade by (1−α) per trial; breaks: a new "dose" (outcome) arrives every trial, and in Kalman/HGF the rate itself changes.
- Reward sensitivity ρ vs learning rate α → Emax vs rate constant; breaks: ρ and β trade off (see errors), so a low ρ can hide inside β.
- Hierarchical fitting → lme4/brms random effects (BLUP shrinkage); breaks: parameters act through a non-linear learning rule, priors sit on transformed scales (logit α, log β), and shrinkage can distort individual differences.
- Model-recovery confusion matrix → sensitivity and PPV of a diagnostic test; breaks: the "prevalence" of each model is set by you in the simulation, not by nature.
- AIC/BIC → penalized fit (the ridge/LASSO idea); breaks: they count parameters instead of shrinking them, and they say nothing about absolute fit (cp-4.6).
- Two-step stay analysis → logistic regression with an interaction (stay ~ reward × transition); breaks: the full hybrid model uses every trial's history, not only the last trial.
- DDM evidence accumulation → Bayesian log-odds updating; breaks: Bayesian updating has no stopping rule; in the DDM the boundary a is a free caution setting, and the noise is moment-to-moment within one trial.
- Kalman gain and HGF update size → RW α; breaks: the gain is computed from variances (uncertainty, volatility), not fitted as a fixed constant.
- HGF ω2 → a person-level trait, like a random-effect value; breaks: it lives on a log-variance scale (σ̂2 = σ2 + e^(κμ3+ω2)); check its recovery (cp-3.4) before you read it as a trait.
- Parameter reliability → PHQ-9 test–retest; breaks: much of the error comes from the task and the fitting method (trial count, estimation), not only from the person.
- Normative-model z-score → pediatric growth-chart centile; breaks: it needs a representative reference sample, site correction and good tail modeling (non-Gaussian likelihoods).
- Predictive-coding precision → gain or signal-to-noise; breaks: it is a neural process theory, usually not fitted per patient the way RW is.
- Model-based vs model-free → goal-directed vs habit; breaks: w is one task's index, not a direct measure of habits in daily life.

## Common errors and term collisions

- Prime ′ read as a derivative → it means "next trial": V′ = V + αδ.
- Softmax β read as a regression coefficient → it is an inverse temperature (higher = more deterministic); it acts as a slope on Q_A − Q_B but is not the coefficient vector in Xβ; temperature τ = 1/β runs the other way.
- α and ε reused → learning rate α is not significance level α or Cronbach's α; ε is the learning rate in Primer ch 7 but the exploration probability in ε-greedy (RL book ch 2).
- "Pooling" → partial pooling = shrinkage toward the group mean; CNN pooling = down-sampling a feature map.
- "Model-based" taken as one idea → 3 meanings: model-based RL (planning with a transition model), "model-based analysis" (fitting any computational model), model-based fMRI regressors.
- "Volatility" and "precision" read in their finance/ML sense → HGF volatility = how fast the hidden tendency drifts (not market volatility or mood lability); precision = 1/variance (not PPV).
- Superscripts and hats read as math → MB, MF and level numbers (μ2) are labels, but ζ in x^ζ is a real exponent; HGF μ̂ = prediction before the outcome, while stats θ̂ = an estimate.
- "High α = learns better" → high α forgets fast; the best α depends on how fast the world changes.
- "Lower in-sample NLL = better model" → extra parameters always lower it; compare with AIC/BIC, held-out data or BMS, then validate the winner.
- "A group difference in a parameter = a mechanism" → first check parameter and model recovery and validate the model; a missing term (e.g., perseveration) can appear as a false α difference.
- "Fit ρ and β together in a plain bandit" → with V₀ = 0, only ρ·β is identifiable: (ρ = 1, β = 5) and (ρ = 0.5, β = 10) give the same NLL; fix one or change the design.
- "Anhedonia = slow learning" → a meta-analysis (6 datasets, 392 sessions, probabilistic reward task) found MDD/anhedonia lowered reward sensitivity more than learning rate; low-dose pramipexole showed the opposite pattern.
- "Hierarchical fitting always fixes reliability" → still debated: one 4-sample study found model-based planning reliability ranged from 0 to above 0.9 by analysis choice, with hierarchical, robust estimation helping most; another analysis warns that priors can skew reliability toward high-precision people and that true session-to-session change also lowers it.
- DDM values compared across papers or packages → conventions differ (s = 0.1 or s = 1) and v and a scale with s, so compare within one convention; coarse Euler simulation also inflates RT (v = 1, a = 2, s = 1: dt = 0.01 s → mean DT ≈ 0.83 vs exact 0.76 s).
- Random trial-wise k-fold on learning data → it leaks the learning history; hold out whole blocks, sessions or subjects.

## Resources

- [Computational Psychiatry Course (CPC) Zurich](https://www.translationalneuromodeling.org/cpcourse/) — official course page (TNU, University of Zurich & ETH Zurich) · free · the target course: 2026 lecture program, tutorials A–L, link to the precourse reading list · chunks: cp-1.1, cp-1.3, cp-4.5, cp-6.4, cp-6.5, cp-7.2, cp-8.1, cp-8.2, cp-8.4
- [Reinforcement Learning: An Introduction, 2nd ed.](http://incompleteideas.net/book/the-book-2nd.html) — "RL book": textbook site with full PDF (MIT Press 2018) · free · RL equations: §2.5 constant α, §2.8 soft-max, §6.1 TD, §6.5 Q-learning, §8.1 planning, §14.2.2 Rescorla–Wagner, §14.6 habit vs goal-directed, §15.6 TD error and dopamine · chunks: cp-2.1, cp-2.2, cp-2.3, cp-2.4, cp-2.5, cp-2.7
- [Ten simple rules for the computational modeling of behavioral data](https://pmc.ncbi.nlm.nih.gov/articles/PMC6879303) — "Ten rules": paper (eLife 2019, CC BY, code on GitHub) · free · the workflow simulate → fit → recover → compare → validate · chunks: cp-1.4, cp-3.1, cp-3.4, cp-4.1, cp-4.3, cp-4.6
- [Computational Psychiatry: A Primer (submitted manuscript)](https://homepages.inf.ed.ac.uk/pseries/CPPrimer/CPprimer-submitted.pdf) — "Primer": textbook draft hosted by the editor; published by MIT Press in 2020 · free (print edition paid) · ch 1 Marr's levels, ch 2 methods (fitting, recovery, BIC, HGF, DDM), ch 6 psychosis, ch 7 depression · chunks: cp-1.1, cp-1.2, cp-1.3, cp-3.4, cp-4.1, cp-7.1, cp-7.2
- [Neuromatch Academy: Computational Neuroscience](https://compneuro.neuromatch.io/tutorials/intro.html) — "NMA": interactive Python course book · free · W1D2 Model Fitting (MLE, bootstrap, cross-validation), W3D2 Bayesian Decisions, W3D3 Hidden Dynamics (SPRT, Kalman filter), W3D4 Reinforcement Learning · chunks: cp-2.5, cp-3.1, cp-3.2, cp-3.5, cp-4.2, cp-5.1, cp-6.1, cp-6.2
- [scipy.optimize.minimize](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html) — API docs · free · bounded MLE fits (L-BFGS-B) in Python · chunks: cp-3.2, cp-3.3, cp-3.5
- [hBayesDM](https://ccs-lab.github.io/hBayesDM/) — R and Python package (Stan) · free · ready hierarchical models: bandit2arm_delta, prl_rp, ts_par4/6/7 (two-step), choiceRT_ddm, pstRT_rlddm1, bandit4arm2_kalman_filter; used in CPC tutorial C · chunks: cp-2.6, cp-2.8, cp-4.4, cp-5.4, cp-5.5, cp-6.2
- [HSSM](https://lnccbrown.github.io/HSSM/) — Python package (PyMC/Bambi) · free · hierarchical DDM and RL-SSM fits with trial-level regressions · chunks: cp-5.1, cp-5.2, cp-5.3, cp-5.4, cp-5.5
- [TAPAS software suite](https://github.com/ComputationalPsychiatry/) — GitHub organization that now hosts TAPAS (the old TAPAS repo is archived and points here) · free · MATLAB hgf-toolbox, pyhgf, genbed (generative embedding) · chunks: cp-6.3, cp-6.6, cp-8.3
- [pyhgf: Learn](https://computationalpsychiatry.github.io/pyhgf/learn.html) — Python docs and notebooks · free · binary and continuous HGF, custom response models, parameter recovery, "Zurich CPC I/II" exercises · chunks: cp-6.3, cp-6.4, cp-6.6
- [Model-based influences on humans' choices and striatal prediction errors](https://pmc.ncbi.nlm.nih.gov/articles/PMC3077926) — "two-step paper": the original two-step task (Neuron 2011) · free · task design (70/30 transitions, slowly drifting rewards) and the hybrid weight w · chunks: cp-2.8, cp-7.3
- [Characterizing a psychiatric symptom dimension related to deficits in goal-directed control](https://doi.org/10.7554/eLife.11305) — "compulsivity paper" (eLife 2016) · free · in two general-population samples, low model-based control tracked a compulsive behavior and intrusive thought dimension most strongly, and specifically vs other symptom dimensions · chunks: cp-7.3
- [Mapping anhedonia onto reinforcement learning: a behavioural meta-analysis](https://doi.org/10.1186/2045-5380-3-12) — "anhedonia meta-analysis" (Biol Mood Anxiety Disord 2013) · free · reward sensitivity vs learning rate across 6 datasets · chunks: cp-2.6, cp-7.1
- [Does the reliability of computational models truly improve with hierarchical modeling?](https://link.springer.com/article/10.3758/s13423-024-02490-8) — "reliability paper" (Psychon Bull Rev 2024) · free · how to assess parameter reliability; limits of hierarchical priors · chunks: cp-4.4, cp-7.4, cp-7.5
- [PCNtoolkit: Background](https://pcntoolkit.readthedocs.io/en/stable/pages/background.html) — Python docs · free · normative models (BLR, HBR with Normal/SHASH/Beta likelihoods, GPR); used in CPC tutorial F · chunks: cp-8.4

Checked: 2026-10-12 — every URL opened; every seed computed in Python.
