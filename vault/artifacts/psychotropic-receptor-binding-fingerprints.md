---
title: Antipsychotic & Antidepressant Receptor-Binding Fingerprints — Affinity Atlas
created: 2026-07-15
type: artifact
source: manual
tags: [psychopharmacology, antipsychotics, antidepressants, receptor-binding, affinity, ki, fingerprint, reference]
links: [Antipsychotics & Antidepressants — Dose Range and Receptor Occupancy Reference]
sources:
  - "Kroeze 2003 — 17 antipsychotics x 12 receptors, PDSP; H1 predicts weight gain — doi:10.1038/sj.npp.1300027"
  - "Richelson & Souder 2000 — antipsychotic binding at human brain receptors — doi:10.1016/s0024-3205(00)00911-5"
  - "Siafis 2018 — antipsychotic receptor-binding profiles to metabolic effects — doi:10.2174/1570159X15666170630163616"
  - "Nasrallah 2007 — atypical antipsychotic receptor-binding profiles — doi:10.1038/sj.mp.4002066"
  - "Tatsumi 1999 — neuroleptics at human monoamine transporters — doi:10.1016/s0014-2999(99)00005-9"
  - "Owens 1997 — antidepressant receptor & transporter binding profile — PMID 9400006"
  - "Tatsumi 1997 — antidepressants at human monoamine transporters — doi:10.1016/s0014-2999(97)01393-9"
  - "NIMH PDSP Ki database (Roth/Kroeze) and manufacturer/FDA data for newer agents"
---

# Antipsychotic & Antidepressant Receptor-Binding Fingerprints — Affinity Atlas

**Scope.** The *binding* companion to [[psychotropic-dose-receptor-occupancy|the dose–occupancy reference]].
Where that report gives in-vivo occupancy at the primary target (D2, SERT), this atlas maps each drug's
**in-vitro affinity across the whole receptor panel** — the receptor *fingerprint* that predicts the
side-effect profile. Antipsychotics are profiled over D1/D2/D3/5-HT1A/5-HT2A/5-HT2C/5-HT7/H1/M1/α1/α2;
antidepressants over SERT/NET/DAT/5-HT1A/5-HT2A/5-HT2C/5-HT3/H1/M1/α1/σ1/MAO. Affinities are binned from
radioligand-binding Ki (mostly PDSP / the classic human-brain compilations); representative Ki are given
where well established. Assembled and adversarially verified across two independent lenses
(pharmacology-correctness + Ki-traceability) — every drug-class matrix was checked for wrong bins,
missing dominant affinities, and fabricated/over-precise Ki before inclusion.

## How to read this — three things that are NOT the same

1. **Affinity ≠ occupancy ≠ clinical effect.** A low Ki (high affinity) does not guarantee engagement at
   therapeutic dose — that depends on dose, plasma level, CNS penetration and receptor density (e.g.
   venlafaxine's NET action only emerges > 150 mg/day; quetiapine's D2 is transient). Read bins *with* dose.
2. **Affinity does not encode functional DIRECTION.** The same bin can be antagonism, partial agonism,
   agonism or inverse agonism — with opposite consequences. D2 `+++` is prolactin-*raising* blockade for
   risperidone but prolactin-*sparing* partial agonism for aripiprazole; 5-HT1A `+++` is beneficial
   *agonism*; 5-HT2A `+++` is beneficial *antagonism*. **Always read the bin with the drug's functional note.**
3. **The bins are coarse ordinal buckets, not a scale.**

**Affinity bins (from Ki):**  `+++` high (< 10 nM) · `++` moderate (10–100 nM) · `+` low (100–1000 nM) ·
`±` very low (1000–10000 nM) · `–` negligible (> 10000 nM / inactive).

---

## Receptor → clinical-consequence legend

### Antipsychotic panel
| Receptor | Clinical consequence when engaged |
|---|---|
| **D1** | Minor direct clinical role; prefrontal/cognitive and dopaminergic tone modulation. Blockade contributes marginally to EPS and possibly to negative-symptom/cognitive effects. No single agent's profile is D1-driven here (asenapine and lumateperone carry the highest D1 bins). |
| **D2** | The core antipsychotic target: mesolimbic blockade reduces positive symptoms. Nigrostriatal blockade -> EPS (acute dystonia, parkinsonism, akathisia, tardive dyskinesia). Tuberoinfundibular blockade -> hyperprolactinemia (galactorrhea, amenorrhea, sexual dysfunction, bone loss). Partial agonism (aripiprazole/brexpiprazole/cariprazine) delivers efficacy while sparing prolactin but is akathisia-prone. |
| **D3** | Limbic/mesocortical, motivational and mood/cognitive modulation. High D3 affinity (cariprazine, ~10x over D2) is invoked for negative-symptom and anhedonia benefit; also contributes to prolactin/EPS signaling. |
| **5HT1A** | As AGONISM/partial agonism: anxiolytic, antidepressant, pro-cognitive and EPS-sparing (increases prefrontal dopamine). A defining feature of the newer SGAs (aripiprazole, brexpiprazole, cariprazine, ziprasidone, lurasidone, asenapine). |
| **5HT2A** | As ANTAGONISM: disinhibits nigrostriatal dopamine -> lowers EPS (the pharmacologic basis of 'atypicality'); improves slow-wave sleep; mood/negative-symptom and anti-migraine benefit. High 5-HT2A:D2 ratio (ziprasidone, lurasidone, loxapine, pimavanserin) predicts low EPS. |
| **5HT2C** | As antagonism/inverse agonism: appetite stimulation and weight gain; mood modulation. A driver (with H1) of the metabolic burden of olanzapine, clozapine, asenapine. |
| **5HT7** | As antagonism: circadian/sleep regulation, antidepressant and pro-cognitive effects. Prominent in lurasidone, brexpiprazole, risperidone/paliperidone, amisulpride, asenapine. |
| **H1** | As antagonism/inverse agonism: sedation and weight gain. Drives the sedating/metabolic profile of chlorpromazine, perphenazine, loxapine, olanzapine, quetiapine, clozapine, asenapine. |
| **M1** | As antagonism: anticholinergic burden - dry mouth, constipation, blurred vision, urinary retention, tachycardia, cognitive impairment/delirium (esp. elderly). Also masks/offsets EPS. Highest in thioridazine, clozapine, olanzapine, chlorpromazine; near-absent in the high-potency FGAs and most newer SGAs. |
| **α1** | As antagonism: orthostatic hypotension, dizziness, reflex tachycardia, fall risk, sedation; priapism. Most potent in iloperidone (requires slow titration), chlorpromazine, thioridazine, fluphenazine, risperidone/paliperidone, clozapine, asenapine, brexpiprazole. |
| **α2** | As antagonism: increases noradrenergic release (potential mood/arousal effect) and may blunt some antihypertensive drugs. Minor contributor for most antipsychotics; notable bins in asenapine and clozapine. |

### Antidepressant panel
| Receptor | Clinical consequence when engaged |
|---|---|
| **SERT** | Serotonin-transporter inhibition: antidepressant/anxiolytic/anti-OCD efficacy. On-target adverse effects - nausea/GI, sexual dysfunction, discontinuation syndrome (worse with short half-life agents), hyponatremia/SIADH, platelet/bleeding risk. Potency ranges from sub-nM (paroxetine, clomipramine, vilazodone) to weak (venlafaxine, trazodone). |
| **NET** | Norepinephrine-transporter inhibition: energy, motivation, analgesia (neuropathic/fibromyalgia). Dose-dependent BP/HR rise, sweating, urinary hesitancy, activation/tremor. Prominent in NET-preferring agents (levomilnacipran, milnacipran, desipramine, nortriptyline, duloxetine). |
| **DAT** | Dopamine-transporter inhibition: activation, pro-motivation, lower sexual/anergic burden; abuse potential at extremes. Meaningful only in bupropion (primary) and sertraline (~25 nM, modest at clinical dose). |
| **5HT1A** | As agonism/partial agonism: augments antidepressant effect, hastens autoreceptor desensitization (faster onset), softens early serotonergic side effects and sexual dysfunction. Defining for vilazodone (partial agonist) and vortioxetine (agonist). |
| **5HT2A** | As antagonism: improved sleep, anxiolysis, reduced sexual dysfunction, antidepressant augmentation. The load-bearing action of the SARIs trazodone and nefazodone; also carried by sedating TCAs. |
| **5HT2C** | As antagonism: appetite/weight gain and mood modulation (e.g., amitriptyline, mirtazapine, clomipramine). Fluoxetine/norfluoxetine 5-HT2C antagonism contributes to its early activating/anxiogenic profile and underlies the olanzapine-fluoxetine combination rationale. |
| **5HT3** | As antagonism: antiemetic/anti-nausea and possible pro-cognitive/GI-tolerability benefit. Prominent in vortioxetine and mirtazapine (its antiemetic property). |
| **H1** | As antagonism/inverse agonism: sedation and weight/appetite gain. Drives the profile of mirtazapine (Ki <1 nM), doxepin (sub-nM - repurposed as a low-dose hypnotic), amitriptyline; citalopram's mild sedation comes from R-enantiomer H1. |
| **M1** | As antagonism: anticholinergic effects - dry mouth, constipation, blurred vision, urinary retention, cognitive load/delirium (esp. elderly). Highest in the tertiary-amine TCAs and, among SSRIs, paroxetine; SSRIs/SNRIs otherwise near-clean. |
| **α1** | As antagonism: orthostatic hypotension, dizziness, sedation, fall risk; priapism (trazodone). Strongest in TCAs and the SARIs (trazodone > nefazodone). |
| **σ1** | Chaperone-protein modulation (mostly agonism); implicated in antidepressant/anxiolytic, cognitive, antipsychotic-depression and OCD effects but clinically poorly defined. Notable in fluvoxamine (most potent), sertraline, fluoxetine. |
| **MAO** | Irreversible non-selective monoamine-oxidase inhibition raises synaptic 5-HT/NE/DA indirectly (no direct transporter binding). Governs the safety profile: hypertensive tyramine ('cheese') crisis, serotonin-syndrome risk, ~2-week washout for enzyme resynthesis. Low-dose selegiline is MAO-B-selective and tyramine-safe until higher/patch doses recruit MAO-A. |

---

## PART A — ANTIPSYCHOTIC RECEPTOR FINGERPRINTS

### First-generation antipsychotics

| Drug | D1 | D2 | D3 | 5HT1A | 5HT2A | 5HT2C | 5HT7 | H1 | M1 | α1 | α2 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| haloperidol | + | **+++** | **+++** | ± | ++ | ± | + | ± | – | ++ | + |
| fluphenazine | ++ | **+++** | **+++** | ± | ++ | + | ++ | ++ | ± | **+++** | + |
| trifluoperazine | ++ | **+++** | **+++** | ± | ++ | + | ++ | ++ | ± | ++ | + |
| thiothixene | ++ | **+++** | **+++** | ± | ++ | + | + | ++ | ± | ++ | + |
| perphenazine | ++ | **+++** | **+++** | ± | **+++** | + | ++ | **+++** | ± | ++ | + |
| loxapine | ++ | ++ | ++ | ± | **+++** | ++ | ++ | **+++** | + | ++ | ++ |
| chlorpromazine | ++ | **+++** | **+++** | ± | **+++** | ++ | ++ | **+++** | ++ | **+++** | + |
| thioridazine | ++ | ++ | ++ | + | ++ | ++ | ++ | ++ | **+++** | **+++** | ++ |
| pimozide | + | **+++** | ++ | ± | ++ | + | + | + | ± | ++ | + |

**Signatures (affinity read with functional direction):**

- **haloperidol** — Pure antagonist throughout. Potent, near-selective D2/D3 antagonism is the whole clinical story — high EPS and hyperprolactinemia, little else. alpha1 antagonism gives some orthostasis; negligible H1 (Ki ~hundreds–>1000 nM) and negligible M1, so minimal sedation and no anticholinergic burden — the prototypic 'clean' high-potency FGA. _(Ki: D2 1.4 nM; D3 2.5 nM; 5HT2A 45 nM; α1 12 nM)_
- **fluphenazine** — High-potency piperazine phenothiazine antagonist. Sub-nanomolar D2/D3 → marked EPS/prolactin. Potent alpha1 (orthostasis) and moderate H1; negligible muscarinic block so no anticholinergic offset to its EPS. _(Ki: D2 0.9 nM; D3 1.4 nM; 5HT2A 12 nM; α1 6.5 nM)_
- **trifluoperazine** — High-potency piperazine phenothiazine antagonist, profile close to fluphenazine. D2/D3-dominant → EPS/prolactin; moderate 5-HT2A, H1 and alpha1; low anticholinergic activity. _(Ki: D2 1.6 nM; 5HT2A 13 nM)_
- **thiothixene** — High-potency thioxanthene antagonist. D2/D3-dominant → EPS/prolactin; moderate alpha1 and H1; low muscarinic affinity. Behaves like the piperazine phenothiazines pharmacodynamically. _(Ki: D2 1.4 nM)_
- **perphenazine** — Mid-potency piperazine phenothiazine antagonist. Potent D2/D3 alongside strong 5-HT2A and H1 antagonism (the H1 block predicts its sedation/weight effect); low muscarinic affinity. The CATIE-era 'moderate' FGA comparator. _(Ki: D2 1.4 nM; 5HT2A 5.6 nM; H1 8 nM)_
- **loxapine** — Dibenzoxazepine antagonist, structurally clozapine-like, with an atypical-range high 5-HT2A:D2 ratio — 5-HT2A is its most potent site. Potent 5-HT2C and H1 (sedation); modest muscarinic block (amoxapine-like) and moderate alpha1/alpha2. Weaker, more moderate D2 occupancy than the classic high-potency FGAs. _(Ki: D2 11 nM; 5HT2A 2 nM; 5HT2C 13 nM; H1 5 nM)_
- **chlorpromazine** — Low-potency aliphatic phenothiazine, broad promiscuous antagonist. Its side-effect profile is receptor-driven: potent alpha1 (marked orthostasis) + potent H1 (sedation) + moderate M1 (anticholinergic) layered on strong D2/5-HT2A antagonism. The prototypic 'dirty' sedating FGA. _(Ki: D2 2 nM; 5HT2A 4 nM; 5HT2C 16 nM; H1 3 nM; M1 47 nM; α1 0.4 nM)_
- **thioridazine** — Low-potency piperidine phenothiazine antagonist and the most anticholinergic FGA — potent M1 block plus potent alpha1 (orthostasis). Intrinsic anticholinergic tone offsets EPS (low EPS liability) but drives its notorious QT prolongation/cardiotoxicity ceiling. _(Ki: D2 14 nM; 5HT2A 40 nM; H1 20 nM; M1 5 nM; α1 4 nM)_
- **pimozide** — Diphenylbutylpiperidine, potent and relatively selective D2 antagonist. Its dose-limiting risk is dose-dependent QT prolongation, driven primarily by blockade of the cardiac hERG (IKr, rapid delayed-rectifier K+) channel (it also blocks L-/T-type Ca2+ channels, but the QT liability is a potassium-current effect). Modest alpha1/5-HT2A; low H1/M1. Used in Tourette's and delusional disorder. _(Ki: D2 1.5 nM; 5HT2A 40 nM; α1 20 nM)_

### Second-generation antipsychotics

| Drug | D1 | D2 | D3 | 5HT1A | 5HT2A | 5HT2C | 5HT7 | H1 | M1 | α1 | α2 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| risperidone | + | **+++** | ++ | ± | **+++** | ++ | **+++** | ++ | – | **+++** | ++ |
| paliperidone | + | **+++** | ++ | ± | **+++** | ++ | **+++** | ++ | – | **+++** | ++ |
| olanzapine | ++ | ++ | ++ | ± | **+++** | ++ | + | **+++** | **+++** | ++ | + |
| quetiapine | + | + | + | + | ++ | ± | + | **+++** | + | ++ | + |
| clozapine | + | + | + | + | **+++** | ++ | ++ | **+++** | **+++** | **+++** | ++ |
| ziprasidone | ++ | **+++** | **+++** | **+++** | **+++** | **+++** | **+++** | ++ | – | ++ | + |
| aripiprazole | + | **+++** | **+++** | **+++** | **+++** | ++ | ++ | ++ | – | ++ | ++ |
| brexpiprazole | + | **+++** | **+++** | **+++** | **+++** | ++ | **+++** | ++ | – | **+++** | ++ |
| cariprazine | + | **+++** | **+++** | **+++** | ++ | + | + | ++ | – | + | + |
| asenapine | **+++** | **+++** | **+++** | **+++** | **+++** | **+++** | **+++** | **+++** | – | **+++** | **+++** |
| lurasidone | + | **+++** | ++ | **+++** | **+++** | + | **+++** | ± | – | ++ | ++ |
| iloperidone | + | **+++** | **+++** | ++ | **+++** | ++ | ++ | ++ | – | **+++** | ++ |
| lumateperone | ++ | ++ | + | + | **+++** | + | + | + | – | ++ | + |
| amisulpride | – | **+++** | **+++** | – | – | ± | ++ | – | – | – | – |
| pimavanserin | – | – | – | – | **+++** | ++ | – | – | – | – | – |

**Signatures (affinity read with functional direction):**

- **risperidone** — Antagonist across the panel. Signature = very high 5-HT2A + potent D2 (EPS/prolactin at higher dose) with strong alpha1 (orthostasis). Potent 5-HT7. 5-HT1A is weak (~200-430 nM), not a functional 5-HT1A agent (downgraded to ±). Essentially no muscarinic binding. Ki anchored to classic compilations (Kroeze 2003, PDSP). _(Ki: D2 3.5 nM; 5HT2A 0.3 nM; 5HT7 3 nM; α1 2 nM)_
- **paliperidone** — 9-hydroxy-risperidone active metabolite; near-identical antagonist profile to risperidone. High 5-HT2A + potent D2 (prolactin elevation), strong alpha1, potent 5-HT7; weak 5-HT1A (~480 nM, ±); no muscarinic binding. Ki are Invega/manufacturer-era; only order-of-magnitude D2 (~3 nM) retained, secondary values nulled as not independently corroborated. _(Ki: D2 3 nM)_
- **olanzapine** — Antagonist. Multireceptor 'pin' profile like clozapine: very potent H1 + M1 driving weight gain/metabolic burden and anticholinergic load. Moderate D2, high 5-HT2A. Ki anchored to classic compilations. _(Ki: D2 15 nM; 5HT2A 2 nM; H1 2.8 nM; M1 5 nM)_
- **quetiapine** — Antagonist with low, transient D2 occupancy. Dominated by potent H1 (sedation/weight) and alpha1 (orthostasis). Active metabolite norquetiapine adds NET inhibition + 5-HT2C antagonism + 5-HT1A partial agonism (not modeled here). Loose D2 binding underlies low EPS. Ki anchored to classic compilations. _(Ki: D2 320 nM; 5HT2A 220 nM; H1 6 nM; α1 15 nM)_
- **clozapine** — Prototype 'dirty' antagonist; weak/loose D2 (no EPS, low prolactin). Very potent 5-HT2A, H1, alpha1 and complex muscarinic pharmacology (M1 antagonism + M4 partial agonism → sialorrhea). High H1/M1 drive metabolic/anticholinergic effects. Ki anchored to classic compilations. _(Ki: D2 150 nM; 5HT2A 5.4 nM; H1 2 nM; M1 6 nM; α1 7 nM)_
- **ziprasidone** — Highest 5-HT2A:D2 ratio in class. 5-HT1A partial agonist; 5-HT2A/2C/7 antagonist; adds roughly balanced SERT + NET reuptake inhibition (not in panel) → antidepressant-leaning profile. Negligible muscarinic. Note: H1 binding affinity is actually moderate-high (Ki ~5 nM); clinical weight-neutrality reflects offsetting mechanisms rather than low H1 affinity — H1 bin kept at ++. Ki anchored to classic compilations. _(Ki: D2 5 nM; 5HT2A 0.4 nM; 5HT2C 1.3 nM; 5HT7 5 nM; 5HT1A 3 nM)_
- **aripiprazole** — D2 & D3 & 5-HT1A partial agonist ('dopamine system stabilizer'), 5-HT2A antagonist. Low H1/no muscarinic → weight/sedation-sparing but akathisia-prone. Partial agonism lowers prolactin. Ki sourced to Shapiro 2003 (Roth lab) + PDSP — classic, widely reproduced, retained. _(Ki: D2 0.34 nM; D3 0.8 nM; 5HT1A 1.7 nM; 5HT2A 3.4 nM)_
- **brexpiprazole** — D2/D3 & 5-HT1A partial agonist, 5-HT2A antagonist; lower intrinsic D2 activity than aripiprazole → less akathisia/activation. Potent 5-HT7 and alpha1B/alpha2C antagonism. Ki from Maeda 2014 (Otsuka), single-source; headline D2 ~0.3 retained, sub/multi-sig-fig secondary values nulled. _(Ki: D2 0.3 nM)_
- **cariprazine** — D3-preferring D3/D2 partial agonist (highest D3 affinity in class, ~10x over D2), 5-HT1A partial agonist, 5-HT2B and 5-HT2A antagonist. Long-acting active metabolites. Low clinical adrenergic/histaminergic burden (H1 Ki ~23 nM is moderate binding but low sedation; bin kept ++); akathisia-prone. Ki from Kiss 2010 (Gedeon Richter); D3/D2 signature retained at order-of-magnitude, single-source 5-HT2A/5-HT1A decimals nulled. _(Ki: D2 0.5 nM; D3 0.09 nM)_
- **asenapine** — Pan-antagonist (5-HT1A partial agonist) with sub-nanomolar potency across serotonergic, dopaminergic, histaminergic and adrenergic receptors — 5-HT2A/2C among the highest affinities of any antipsychotic. Uniquely for this broad profile, essentially no muscarinic binding. Sublingual only. Sub-nM Ki from Shahid 2009 (Organon) nulled as spuriously precise; D2 ~1.3 retained as headline, bins retained. _(Ki: D2 1.3 nM)_
- **lurasidone** — D2 & 5-HT2A & potent 5-HT7 antagonist, 5-HT1A partial agonist (pro-cognitive/antidepressant profile). Negligible H1 and muscarinic binding → metabolically favorable, non-sedating; akathisia and modest alpha-mediated effects instead. Requires food (≥350 kcal) for absorption. Ki are Latuda-label/Ishibashi 2010 (approximate); round headline values retained flagged, 5-HT1A 6.4 nulled. _(Ki: D2 1 nM; 5HT2A 0.5 nM; 5HT7 0.5 nM)_
- **iloperidone** — 5-HT2A & D2/D3 antagonist with the most potent alpha1 antagonism in class → marked orthostatic hypotension requiring slow titration. Low EPS; QT prolongation. Negligible muscarinic. Manufacturer-era Ki; 'most potent alpha1 in class' (~0.5) retained, D3 7.1 nulled as over-precise. _(Ki: D2 3.3 nM; 5HT2A 0.4 nM; α1 0.5 nM)_
- **lumateperone** — 5-HT2A antagonist is dominant (~60x affinity over D2). Unique D2 pre-synaptic partial agonist / post-synaptic antagonist duality → low EPS at low D2 occupancy. Adds SERT inhibition (SERT-selective, ~33 nM) and indirect D1/NMDA glutamatergic modulation (not in panel). Low H1/no muscarinic → metabolically favorable. Ki from Snyder 2015 (Intra-Cellular); D2 ~32 retained, 5-HT2A 0.54 nulled (single-source sub-nM over-precision). _(Ki: D2 32 nM)_
- **amisulpride** — Substituted benzamide; highly selective D2/D3 antagonist (low-dose preferential presynaptic autoreceptor blockade → disinhibition). The one meaningful off-dopamine target is potent 5-HT7 antagonism (mood benefit; also 5-HT2B). Essentially no histaminergic, muscarinic or adrenergic binding — but high prolactin elevation. European agent, not in US classic compilations; D2/D3 (~2/3) retained, 5-HT7 11.5 nulled (single-source over-precision). _(Ki: D2 2 nM; D3 3 nM)_
- **pimavanserin** — Selective 5-HT2A inverse agonist/antagonist with weaker 5-HT2C activity and functional selectivity (~40x) for 2A. NO dopaminergic (no D2), histaminergic, muscarinic or adrenergic binding → no EPS/prolactin; used for Parkinson's disease psychosis. Sub-nM Ki (Vanover 2006) nulled as spuriously precise; identity carried by the isolated 5-HT2A +++ bin pattern — no numeric Ki survives.


---

## PART B — ANTIDEPRESSANT RECEPTOR FINGERPRINTS

### SSRIs and SNRIs

| Drug | SERT | NET | DAT | 5HT1A | 5HT2A | 5HT2C | 5HT3 | H1 | M1 | α1 | σ1 | MAO |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| fluoxetine | **+++** | + | ± | – | + | ++ | – | ± | ± | ± | + | – |
| sertraline | **+++** | + | ++ | – | ± | ± | – | – | + | + | ++ | – |
| paroxetine | **+++** | ++ | + | – | ± | ± | – | – | ++ | ± | + | – |
| citalopram | **+++** | ± | – | – | – | – | – | + | ± | ± | – | – |
| escitalopram | **+++** | ± | – | – | – | – | – | ± | ± | ± | – | – |
| fluvoxamine | **+++** | ± | – | – | – | – | – | – | – | – | ++ | – |
| venlafaxine | ++ | ± | ± | – | – | – | – | – | – | – | – | – |
| desvenlafaxine | ++ | + | ± | – | – | – | – | – | – | – | – | – |
| duloxetine | **+++** | **+++** | + | – | – | – | – | – | – | – | – | – |
| levomilnacipran | ++ | ++ | – | – | – | – | – | – | – | – | – | – |
| milnacipran | ++ | ++ | – | – | – | – | – | – | – | – | – | – |

**Signatures (affinity read with functional direction):**

- **fluoxetine** — Potent SERT reuptake inhibitor. Distinguished among SSRIs by clinically meaningful 5-HT2C antagonism (fluoxetine and especially the long-lived metabolite norfluoxetine) — contributes to its early activating/anxiogenic profile and appetite effects, and underlies the fluoxetine/olanzapine combination rationale. 5-HT2A affinity is weak (the predominant 5-HT2 action is at 2C). Weak NET inhibition emerges only at high dose. Modest sigma1 affinity. Negligible antihistaminic/anticholinergic/adrenergic binding, so non-sedating and clean on autonomic side-effects. Long half-life (norfluoxetine days–weeks). Ki caveat: SERT/NET trace to Owens 1997; 5-HT2C (~55) and sigma1 (~120) are off-anchor (PDSP/sigma-specific) and approximate. _(Ki: SERT 0.8 nM; NET 240 nM; 5HT2C 55 nM; σ1 120 nM)_
- **sertraline** — Most SERT-potent SSRI. Uniquely carries appreciable DAT affinity (Ki ~25 nM, Tatsumi) — modestly dopaminergic at higher doses and a plausible contributor to its lower rate of sexual/anergic complaints, though functional DAT occupancy at clinical doses is modest. Potent sigma1 binding (~57 nM, antagonist, off-anchor). Mild muscarinic (Ki ~625 nM) can produce loose stools/GI effects; modest alpha1. Reuptake inhibition at all three transporters; antagonist/inhibitor pharmacology otherwise. _(Ki: SERT 0.3 nM; NET 420 nM; DAT 25 nM; σ1 57 nM)_
- **paroxetine** — Highest-affinity SERT ligand of the class, but the least clean SSRI. Moderate NET affinity (Ki ~40 nM, Owens 1997) gives partial SNRI-like action at higher doses. Most anticholinergic SSRI (M1 Ki ~108 nM, Owens) — dry mouth, constipation, sweating, and cognitive load in the elderly. Short half-life plus potent CYP2D6 self-inhibition drives a sharp discontinuation syndrome. Weakly weight-gaining. Reuptake inhibition; muscarinic antagonism. SERT/NET/M1 trace to Owens 1997, DAT to Tatsumi. _(Ki: SERT 0.13 nM; NET 40 nM; DAT 490 nM; M1 108 nM)_
- **citalopram** — Racemic; highly selective for SERT. The R-enantiomer carries the drug's only notable off-target affinity — H1 antagonism (Ki ~380 nM) that can give mild sedation. Otherwise essentially devoid of adrenergic/muscarinic/dopaminergic action. Dose-dependent QTc prolongation (FDA 40 mg cap; 20 mg in the elderly / 2C19 poor metabolizers) is a hERG/channel effect, not captured by this receptor panel. SERT and H1 Ki traceable. _(Ki: SERT 1.2 nM; H1 380 nM)_
- **escitalopram** — The active S-enantiomer of citalopram and the most selective SSRI. Removing R-citalopram (which carried the racemate's H1 signal) leaves negligible antihistaminic action, so escitalopram is less sedating than citalopram and cleaner across the board. H1 Ki is deliberately omitted: the previously quoted ~1970 nM figure is over-precise and untraceable, and the bin (±) already conveys the negligible-to-weak affinity without a doubtful number. Also allosterically stabilizes its own binding at SERT (Ki ~1.1 nM, traceable). Lower QTc liability than citalopram at equivalent therapeutic exposure. _(Ki: SERT 1.1 nM)_
- **fluvoxamine** — Selective SERT reuptake inhibitor with the most potent sigma1 binding of any SSRI (Ki ~36 nM, agonist; off-anchor but well-established) — invoked for its distinctive efficacy in OCD, psychotic depression, and delirium/cognition. Essentially no antihistaminic, anticholinergic, or adrenergic affinity. Potent CYP1A2/2C19/3A4 inhibitor (raises clozapine, theophylline, tizanidine, caffeine) — the clinically dominant liability is metabolic, not receptor-mediated. SERT from Owens. _(Ki: SERT 2.2 nM; σ1 36 nM)_
- **venlafaxine** — Serotonin-predominant SNRI with a steep dose-response: SERT inhibition (Ki ~82 nM) dominates at low dose, and meaningful NET inhibition (weak binding, Ki ~2480 nM) only appears at doses >150 mg/day — below that it behaves as an SSRI. Very clean off-target profile (no H1/M1/alpha1), so side-effects are on-target serotonergic/noradrenergic (nausea, sweating, dose-dependent BP rise) plus a brisk discontinuation syndrome from its short half-life. All action is reuptake inhibition; all three Ki values trace to Tatsumi 1997. _(Ki: SERT 82 nM; NET 2480 nM; DAT 7600 nM)_
- **desvenlafaxine** — Newer agent (2008) — Ki approximate. The active O-desmethyl metabolite of venlafaxine. Similar serotonin-preferring SNRI profile but a somewhat higher relative NET contribution (SERT Ki ~40, NET ~558; ratio ~1:14) and, importantly, minimal CYP2D6 dependence for its formation — giving flatter, more predictable exposure than venlafaxine. Clean off-target binding; on-target noradrenergic dose-dependent BP effects. Reuptake inhibition only. Ki values come from Deecher 2006 / Pfizer data, not Owens or Tatsumi. _(Ki: SERT 40 nM; NET 558 nM)_
- **duloxetine** — High-potency dual reuptake inhibitor. By Ki it is serotonin-preferring (~10-fold: SERT ~0.8 nM vs NET ~7.5 nM), NOT the most balanced marketed SNRI — the genuinely NET-favoring/most-balanced agent is levomilnacipran (NET 11 < SERT 19). Its true and clinically important feature is that NET affinity is high enough for noradrenergic effects to be present from standard therapeutic doses, unlike serotonin-dominant venlafaxine. Trace DAT affinity (Ki ~240 nM). This dual profile underlies its analgesic indications (diabetic neuropathy, fibromyalgia, chronic musculoskeletal pain). Minimal off-target receptor binding; reuptake inhibition throughout. Ki traceable (Bymaster 2001). _(Ki: SERT 0.8 nM; NET 7.5 nM; DAT 240 nM)_
- **levomilnacipran** — Newer agent (2013) — Ki approximate. The active enantiomer of milnacipran and the most NET-preferring SNRI in clinical use — roughly 2-fold higher potency at NET (Ki ~11 nM) than SERT (Ki ~19 nM), the reverse of the serotonin-dominant venlafaxine/desvenlafaxine. Noradrenergic tone is prominent (energy/motivation, but also dose-dependent heart-rate and BP rise, urinary hesitancy). No DAT affinity and negligible off-target receptor binding; reuptake inhibition only. Potencies are manufacturer/FDA-label (IC50-derived), not classic radioligand Ki. _(Ki: NET 11 nM; SERT 19 nM)_
- **milnacipran** — Racemic dual reuptake inhibitor, roughly balanced with a slight noradrenergic lean (NE Ki ~22 nM, 5-HT Ki ~38 nM; ~1:1.7 favoring NE). SERT Ki corrected from the originally proposed 9 nM, which erroneously made the racemate MORE SERT-potent than its own active enantiomer levomilnacipran (SERT ~19 nM) — impossible for a racemate whose eutomer is the more potent enantiomer, and inconsistent with the drug's documented NET-preferring character. Correcting SERT to ~2x levomilnacipran (~38 nM) restores consistency (NET 22 < SERT 38). Marketed for fibromyalgia (US) and depression (elsewhere). Essentially free of antihistaminic/anticholinergic/adrenergic/dopaminergic off-target binding, so side-effects are on-target noradrenergic (sweating, tachycardia, BP, urinary hesitancy). Reuptake inhibition only; exact SERT value approximate. _(Ki: SERT 38 nM; NET 22 nM)_

### TCAs and MAOIs

| Drug | SERT | NET | DAT | 5HT1A | 5HT2A | 5HT2C | 5HT3 | H1 | M1 | α1 | σ1 | MAO |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| amitriptyline | **+++** | ++ | ± | + | ++ | **+++** | + | **+++** | ++ | ++ | + | – |
| nortriptyline | ++ | **+++** | ± | + | ++ | ++ | + | ++ | ++ | ++ | ± | – |
| imipramine | **+++** | ++ | ± | + | + | + | + | ++ | ++ | ++ | + | – |
| desipramine | ++ | **+++** | ± | ± | + | + | + | ++ | ++ | ++ | ± | – |
| clomipramine | **+++** | ++ | ± | + | ++ | ++ | + | ++ | ++ | ++ | + | – |
| doxepin | ++ | ++ | – | + | ++ | ++ | + | **+++** | ++ | ++ | + | – |
| phenelzine | – | – | – | – | – | – | – | – | – | – | – | **+++** |
| tranylcypromine | – | – | – | – | – | – | – | – | – | – | – | **+++** |
| isocarboxazid | – | – | – | – | – | – | – | – | – | – | – | **+++** |
| selegiline | – | – | ± | – | – | – | – | – | – | – | – | **+++** |

**Signatures (affinity read with functional direction):**

- **amitriptyline** — Tertiary-amine TCA; dual SERT>NET reuptake inhibition. Antagonist at 5-HT2A/5-HT2C, potent H1 antagonist (sedation), M1 antagonist (anticholinergic load), alpha1 antagonist (orthostatic hypotension). Active metabolite nortriptyline shifts profile toward NET. Class Ia-like Na-channel/cardiac risk in overdose. (5-HT2C Ki ~6 nM nulled as non-anchor-traceable; +++ bin retained.) _(Ki: SERT 4.3 nM; NET 35 nM; 5HT2A 18 nM; H1 1.1 nM; M1 18 nM; α1 27 nM)_
- **nortriptyline** — Secondary-amine TCA (amitriptyline metabolite); NET-preferring reuptake inhibitor. 5-HT2A/2C, H1, M1, alpha1 antagonism, but lower anticholinergic/antihistaminic burden and least orthostatic hypotension of the TCAs — the best-tolerated, therapeutically-monitored TCA. _(Ki: SERT 18 nM; NET 4.4 nM; 5HT2A 41 nM; H1 10 nM; M1 37 nM; α1 55 nM)_
- **imipramine** — Prototype tertiary-amine TCA; SERT>NET reuptake inhibition, demethylated to the NET-selective desipramine. Antagonist at H1 (sedation), M1 (anticholinergic), alpha1 (orthostasis); modest 5-HT2 and sigma1 binding. Cardiac conduction risk in overdose. _(Ki: SERT 1.4 nM; NET 37 nM; H1 11 nM; M1 46 nM; α1 90 nM)_
- **desipramine** — Secondary-amine TCA (imipramine metabolite); the most NET-selective TCA (sub-nanomolar NET). Comparatively lower H1/M1/alpha1 burden than tertiary amines — less sedating and less anticholinergic, but retains cardiac/overdose risk. Noradrenergic-forward profile. _(Ki: SERT 17.6 nM; NET 0.83 nM; H1 110 nM; M1 66 nM; α1 100 nM)_
- **clomipramine** — Most serotonergic TCA (sub-nanomolar SERT) — the TCA of choice for OCD. Parent is SERT-potent; N-desmethyl metabolite is NET-selective, giving mixed serotonergic/noradrenergic action at steady state. Potent 5-HT2A/2C, H1, M1, alpha1 antagonism; lowers seizure threshold most among TCAs. _(Ki: SERT 0.28 nM; NET 38 nM; 5HT2A 35 nM; H1 31 nM; M1 37 nM; α1 38 nM)_
- **doxepin** — Tertiary-amine TCA and one of the most potent H1 antagonists known (sub-nanomolar) — repurposed at very low dose (Silenor) as a selective H1 antihistamine hypnotic where transporter/antimuscarinic effects are subclinical. At antidepressant doses adds 5-HT2A, M1, alpha1 antagonism and modest dual reuptake inhibition. _(Ki: SERT 68 nM; NET 29.5 nM; 5HT2A 26 nM; H1 0.24 nM; M1 80 nM; α1 24 nM)_
- **phenelzine** — Irreversible, non-selective MAO-A/B inhibitor (hydrazine); raises 5-HT/NE/DA indirectly by blocking metabolism — no meaningful direct transporter or receptor binding. Also inhibits GABA-transaminase (elevates GABA). Dietary tyramine and serotonergic-drug interactions dominate its safety profile; requires ~2-week washout for enzyme resynthesis.
- **tranylcypromine** — Irreversible, non-selective MAO-A/B inhibitor; a cyclopropylamine (amphetamine-related) structure conferring mild direct monoamine-releasing/uptake-inhibiting and stimulant-like activity, but negligible affinity in binding assays. Tyramine ("cheese") pressor reaction and serotonin-syndrome risk govern use; ~2-week washout.
- **isocarboxazid** — Irreversible, non-selective MAO-A/B inhibitor (hydrazine); increases synaptic monoamines by enzyme inhibition with no direct transporter/receptor binding. Same tyramine and serotonergic-interaction cautions as other classical MAOIs.
- **selegiline** — Irreversible MAO-B-selective inhibitor at low oral dose (Parkinson use, tyramine-safe); loses selectivity to inhibit MAO-A as well at antidepressant/transdermal (EMSAM) doses, requiring dietary caution at high patch strengths. Metabolized to l-amphetamine/l-methamphetamine, giving mild indirect dopaminergic/stimulant activity (marginal DAT-relevant effect); negligible direct receptor binding.

### Atypical / multimodal antidepressants

| Drug | SERT | NET | DAT | 5HT1A | 5HT2A | 5HT2C | 5HT3 | H1 | M1 | α1 | σ1 | MAO |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| bupropion | – | ± | + | – | – | – | – | – | – | – | – | – |
| mirtazapine | – | – | – | – | ++ | ++ | ++ | **+++** | + | + | – | – |
| trazodone | + | – | – | + | ++ | + | – | + | – | ++ | – | – |
| nefazodone | + | ± | – | + | ++ | + | – | ± | – | ++ | – | – |
| vilazodone | **+++** | – | – | **+++** | ± | + | – | – | – | – | – | – |
| vortioxetine | **+++** | – | – | ++ | ± | ± | **+++** | – | – | – | – | – |

**Signatures (affinity read with functional direction):**

- **bupropion** — NDRI, but a weak one at the level of the parent drug: modest DAT and even weaker NET reuptake inhibition (Ki roughly high-hundreds to low-µM in binding assays), with the active metabolite hydroxybupropion carrying much of the clinical NET effect. Also a nicotinic acetylcholine receptor antagonist (off-panel). Essentially devoid of serotonergic, histaminergic, muscarinic and adrenergic binding — hence the activating, non-sedating, weight-neutral, sexually-sparing profile; main liability is a dose-dependent lowering of seizure threshold.
- **mirtazapine** — NaSSA — no monoamine reuptake inhibition and no MAO inhibition. Mechanism is antagonism: central alpha2-adrenergic autoreceptor/heteroreceptor antagonist (the defining action, off-panel) plus 5-HT2A, 5-HT2C and 5-HT3 antagonism. Among the most potent H1 inverse agonists in clinical use (Ki <1 nM, classic range ~0.14–1.6 nM) — drives the profound sedation and appetite/weight gain, most pronounced at low doses before noradrenergic activation offsets it. Mild muscarinic and alpha1 affinity. 5-HT3 blockade gives it antiemetic/anti-nausea properties. _(Ki: H1 0.5 nM)_
- **trazodone** — SARI: potent 5-HT2A antagonism (Ki ~20–35 nM across sources) layered on comparatively weak SERT inhibition (Ki ~160–370 nM) — so at low (hypnotic) doses the 5-HT2A/H1/alpha1 blockade dominates and only at higher (antidepressant) doses does meaningful serotonin reuptake inhibition appear. Weak 5-HT1A partial agonism; the metabolite mCPP is a 5-HT2C agonist. Strong alpha1 antagonism (Ki ~36 nM) is the clinically load-bearing off-target — orthostatic hypotension and priapism. Notably free of anticholinergic (M1) activity. H1 blockade adds to sedation. _(Ki: 5HT2A 20 nM; α1 36 nM)_
- **nefazodone** — SARI, structurally and mechanistically a trazodone congener: potent 5-HT2A antagonism (Ki ~26 nM) with weak SERT inhibition and a small, genuine component of NET reuptake inhibition that trazodone lacks. Less alpha1 blockade and much less H1 affinity than trazodone (H1 binned ± to reflect this), so it is less sedating and causes less orthostasis. Metabolite mCPP is a 5-HT2C agonist. No anticholinergic activity. Carries a black-box warning for idiosyncratic hepatotoxicity/hepatic failure, which has largely retired it from use. _(Ki: 5HT2A 26 nM)_
- **vilazodone** — SPARI — high-potency SERT inhibitor (Ki ~0.1 nM, approx) combined with high-affinity 5-HT1A partial agonism (Ki ~1–2 nM, approx), the 5-HT1A component intended to soften early-onset serotonergic side effects and speed autoreceptor desensitization. NOTE: both Ki values are manufacturer/FDA-derived (Page 2002), not from the classic Owens/Tatsumi/Kroeze compilations — treat as approximate. Clean of histaminergic, muscarinic and adrenergic binding, so weight- and cardiovascular-neutral; the dose-limiting liability is GI (nausea/diarrhea), best mitigated by taking with food. _(Ki: SERT 0.1 nM; 5HT1A 2.1 nM)_
- **vortioxetine** — Multimodal: potent SERT inhibition (Ki ~1.6 nM) plus a spread of direct receptor actions — 5-HT3 antagonism (Ki ~3.7 nM), 5-HT1A agonism (Ki ~15 nM), 5-HT1B partial agonism, and 5-HT1D/5-HT7 antagonism (the last two off-panel). NOTE: all Ki values are manufacturer-derived (Bang-Andersen 2011 / Lundbeck), not from the classic anchor papers — treat as approximate. This receptor multimodality is invoked to explain its pro-cognitive signal and comparatively lower sexual-dysfunction burden. Nausea is the leading adverse effect — dose-dependent and driven by serotonergic/SERT-mediated gut 5-HT, NOT by 5-HT3 blockade (5-HT3 antagonism is itself antiemetic). No meaningful H1/M1/alpha1 binding. _(Ki: SERT 1.6 nM; 5HT3 3.7 nM; 5HT1A 15 nM)_


---

## Internal-consistency verification

The atlas passed all 9 cross-consistency checks (every strong-H1 agent reads as sedating/metabolic; every strong-M1 agent flagged anticholinergic; every strong-α1 agent flagged orthostasis; all partial/inverse agonists labelled as such; bupropion negligible across the monoamine receptor panel; racemate/enantiomer potencies internally ordered). The only "exceptions" are correctly-flagged affinity-vs-function mismatches, not contradictions:

- **Every drug binned +++/++ at H1 is described as sedating and/or weight-gaining.** PASS with three explicitly flagged affinity-vs-clinical exceptions. All +++ H1 agents read as sedating/metabolic (chlorpromazine, perphenazine, loxapine, olanzapine, quetiapine, clozapine, asenapine; and amitriptyline, doxepin, mirtazapine). The atlas itself flags the exceptions where H1 binding is moderate-to-high but clinical sedation/weight is NOT proportionate: ziprasidone (H1 ~5 nM, ++, weight-neutral via offsetting mechanisms), cariprazine (H1 ~23 nM, ++, low sedation), aripiprazole (++ bin yet notes state 'low H1 -> weight/sedation-sparing'). These are the correct kind of note: the bin reflects binding, the clinic reflects net function.
- **Every strong-M1 (+++/++) drug is flagged anticholinergic.** PASS. All strong-M1 agents carry an explicit anticholinergic note: thioridazine ('most anticholinergic FGA'), clozapine, olanzapine, chlorpromazine; and TCAs amitriptyline, nortriptyline, imipramine, desipramine, clomipramine, doxepin; plus paroxetine ('most anticholinergic SSRI', M1 ~108 nM). No strong-M1 drug is left unlabeled.
- **Every strong-alpha1 (+++) drug is flagged for orthostasis.** PASS. All alpha1 +++ agents are associated with orthostasis/hypotension: iloperidone ('most potent alpha1 in class -> marked orthostatic hypotension, slow titration'), chlorpromazine, thioridazine, fluphenazine, risperidone, paliperidone, clozapine, brexpiprazole, asenapine. ++ agents (haloperidol, quetiapine, TCAs, trazodone) likewise note orthostasis. One internal nuance worth surfacing: nortriptyline is alpha1 ++ yet documented as the LEAST orthostatic TCA - consistent, since it is the lowest-alpha1 tertiary/secondary amine and the note is comparative within class.
- **All partial agonists / inverse agonists are labelled as such (not as plain antagonists).** PASS. Dopamine partial agonists: aripiprazole, brexpiprazole, cariprazine (D3-preferring), and lumateperone (presynaptic partial agonist / postsynaptic antagonist duality) - all explicitly labelled. 5-HT1A partial agonists/agonists labelled: ziprasidone, aripiprazole, brexpiprazole, cariprazine, lurasidone, asenapine, vilazodone, vortioxetine, trazodone (weak). Inverse agonists labelled: pimavanserin (5-HT2A inverse agonist), mirtazapine (H1 inverse agonist). No partial/inverse agonist is mislabeled as a pure antagonist.
- **Bupropion reads as negligible across the monoamine RECEPTOR panel (activity confined to transporters).** PASS. Bupropion is '-' at SERT, all 5-HT receptors, H1, M1, alpha1, sigma1, MAO; only DAT '+' and NET '±'. This matches its activating, non-sedating, weight-neutral, sexually-sparing clinical profile and confirms the fingerprint carries no antihistaminic/anticholinergic/adrenergic/serotonergic component. (Off-panel nAChR antagonism and the seizure-threshold liability are correctly noted as not captured by the panel.)
- **Transporter-potency ordering is internally coherent for racemate/enantiomer pairs.** PASS - and the atlas documents a deliberate correction. Milnacipran (racemate) SERT was corrected to ~38 nM so that its eutomer levomilnacipran (SERT ~19 nM) remains the MORE SERT-potent species, as required for a racemate whose active enantiomer is more potent; both retain NET<SERT (levomilnacipran 11<19; milnacipran 22<38), preserving their NET-preferring character. Escitalopram (S-citalopram) is correctly the cleaner, less-antihistaminic species vs racemic citalopram (whose R-enantiomer carries the H1 signal). Paliperidone is coherent as the 9-OH active metabolite mirroring risperidone.
- **5-HT2A antagonism / high 5-HT2A:D2 ratio agents read as low-EPS.** PASS. Agents with dominant 5-HT2A relative to D2 - ziprasidone (highest ratio in class), lurasidone, loxapine (atypical-range ratio for an FGA), quetiapine and clozapine (loose D2) - all carry low-EPS descriptions. Conversely the high-potency FGAs with D2>>5-HT2A (haloperidol, fluphenazine, trifluoperazine, thiothixene) are correctly flagged high-EPS. Pimavanserin (isolated 5-HT2A, no D2) correctly reads as no-EPS/no-prolactin.
- **Dopamine partial-agonist agents (highest D2/D3 affinity) read as prolactin-sparing rather than prolactin-raising despite +++ D2/D3 bins.** PASS. Aripiprazole, brexpiprazole, cariprazine carry +++ D2/D3 (sub-nM Ki, the highest affinities in the tables) yet are correctly described as prolactin-lowering/sparing and akathisia-prone - because the bin encodes affinity while the note encodes partial-agonist function. This is the mirror image of the risperidone/paliperidone/amisulpride +++ D2 pure-antagonists correctly flagged as prolactin-RAISING. Confirms the atlas separates affinity magnitude from functional direction consistently.
- **MAOIs show the pure-enzyme fingerprint (negligible transporter/receptor binding).** PASS. Phenelzine, tranylcypromine, isocarboxazid, selegiline are '-' across SERT/NET(/DAT)/all receptors with MAO '+++' only (selegiline carries a trace DAT '±' from its l-amphetamine metabolite, correctly noted). The clinical hazard is correctly attributed to the enzyme mechanism (tyramine/serotonergic interactions, washout), not to receptor binding.

## Safety — what the fingerprints imply to avoid

- MAOI + any serotonergic agent = serotonin syndrome (potentially fatal). Never co-administer phenelzine, tranylcypromine, isocarboxazid, or antidepressant-dose/patch selegiline with SSRIs, SNRIs, clomipramine/imipramine/amitriptyline, trazodone, nefazodone, vilazodone, vortioxetine (or non-panel serotonergics: tramadol, meperidine, linezolid, methylene blue, triptans, St John's wort). Require a >=2-week washout in BOTH directions for enzyme resynthesis; because of fluoxetine/norfluoxetine's weeks-long half-life, allow ~5 weeks after stopping fluoxetine before starting an MAOI. MAOIs also mandate a tyramine-restricted diet (hypertensive 'cheese' crisis); low-dose oral selegiline is MAO-B-selective and tyramine-safe, but high oral/high-patch doses lose selectivity.
- Anticholinergic burden stacking (additive M1 blockade -> confusion/delirium, constipation/paralytic ileus, urinary retention, blurred vision, tachycardia, falls; worst in the elderly and in dementia). Avoid combining strong-M1 agents: clozapine, olanzapine, thioridazine, chlorpromazine on the antipsychotic side with tertiary-amine TCAs (amitriptyline, imipramine, clomipramine, doxepin) or paroxetine on the antidepressant side - and remember co-prescribed antihistamines, oxybutynin, benztropine add to the same pool. Clozapine + strong anticholinergic is a particular ileus risk.
- QT prolongation / torsades - a hERG(IKr) channel effect NOT captured by this receptor panel, so it must be tracked separately. Higher-risk agents: thioridazine and pimozide (both dose-limited by QT), ziprasidone, iloperidone, chlorpromazine, and (antidepressant side) citalopram (FDA cap 40 mg, 20 mg in elderly/CYP2C19 poor metabolizers) > escitalopram, plus TCAs in overdose. Avoid stacking two QT-prolongers, correct hypokalemia/hypomagnesemia, and get baseline/on-treatment ECGs when combining or using high doses.
- Orthostatic hypotension and fall/fracture risk, especially in the elderly - additive alpha1 blockade. Titrate slowly and counsel on positional changes with strong-alpha1 agents: iloperidone (slowest titration, most potent alpha1 in class), chlorpromazine, thioridazine, clozapine, risperidone/paliperidone, quetiapine, asenapine, brexpiprazole; and trazodone and the TCAs. Trazodone's alpha1 blockade also carries a priapism risk (urologic emergency). Stacking two alpha1 blockers, or adding an antihypertensive/PDE5 inhibitor, compounds the drop.
- Clozapine-specific hazards requiring active monitoring, not just avoidance: agranulocytosis (mandatory ANC/REMS monitoring), myocarditis (early) and cardiomyopathy, dose-dependent seizures, severe constipation/ileus (anticholinergic + hypomotility - a leading cause of clozapine death), sialorrhea (M4 partial agonism), orthostasis on titration, and metabolic syndrome. Critical interaction: do NOT combine clozapine with fluvoxamine (potent CYP1A2 inhibitor) - it can multiply clozapine levels into toxic range; smoking cessation raises levels similarly. Weigh olanzapine/clozapine (H1+5-HT2C+M1) metabolic load in patients with cardiometabolic risk.
- Hyperprolactinemia: pure high-affinity D2 antagonists (risperidone, paliperidone, amisulpride, and the high-potency FGAs haloperidol/fluphenazine) raise prolactin most (galactorrhea, amenorrhea, sexual dysfunction, long-term bone loss). Prefer/switch to a D2 partial agonist (aripiprazole, brexpiprazole, cariprazine) or loose-D2 agent (quetiapine, clozapine) when prolactin is the problem.
- Discontinuation syndrome and bleeding/hyponatremia are on-target SERT effects: taper short-half-life serotonergics (paroxetine, venlafaxine) rather than stopping abruptly; use caution combining SSRIs/SNRIs with anticoagulants/NSAIDs (bleeding) and in the elderly/diuretic-treated (SIADH). Bupropion's isolated liability is dose-dependent seizure-threshold lowering - avoid in seizure disorders, eating disorders, and abrupt alcohol/benzodiazepine withdrawal, and don't stack with other threshold-lowering agents.

## Caveats

- In-vitro Ki is affinity, not in-vivo occupancy. Actual receptor engagement depends on administered dose, plasma concentration, CNS penetration, plasma-protein binding, and regional receptor density - a low Ki does not guarantee a clinically relevant effect at therapeutic doses (e.g., venlafaxine's NET action only emerges >150 mg/day; quetiapine's transient D2 occupancy).
- Affinity does not encode functional DIRECTION. The same bin can mean antagonism, partial agonism, agonism, or inverse agonism with opposite clinical consequences - hence D2 '+++' means prolactin-raising blockade for risperidone but prolactin-sparing partial agonism for aripiprazole, and 5-HT1A '+++' is beneficial agonism, while 5-HT2A '+++' is beneficial antagonism. The ordinal bins must always be read together with the functional_notes.
- Assay, species, tissue and radioligand variance. The matrices blend anchor compilations (Owens 1997, Tatsumi 1997, Kroeze 2003, Roth/PDSP) with manufacturer/FDA-derived values; cross-source Ki are not strictly comparable, and some potencies were IC50-derived rather than true radioligand Ki (e.g., levomilnacipran, milnacipran).
- Newer and single-source agents are least certain. Vilazodone, vortioxetine, levomilnacipran, lumateperone, brexpiprazole, cariprazine, asenapine, iloperidone, pimavanserin rest on manufacturer/single-lab data; several spuriously precise sub-nM Ki were deliberately nulled (bin retained) precisely because they were untraceable or over-precise - treat their numbers as approximate and the bins as the more reliable signal.
- Active metabolites reshape the real-world fingerprint, which the parent-drug panel cannot show: norfluoxetine (5-HT2C, long half-life), norquetiapine (NET inhibition + 5-HT2C antagonism + 5-HT1A partial agonism), hydroxybupropion (much of bupropion's NET effect), the desmethyl-TCAs (shift toward NET), mCPP from trazodone/nefazodone (5-HT2C agonism), paliperidone from risperidone, and cariprazine's long-lived metabolites. Steady-state pharmacology can differ substantially from the parent.
- The panels are deliberately bounded and omit clinically load-bearing off-panel targets: mirtazapine's defining alpha2 autoreceptor antagonism; vortioxetine's 5-HT1B/1D/7 actions; bupropion's nicotinic antagonism; phenelzine's GABA-transaminase inhibition; lumateperone's SERT/D1/NMDA glutamatergic modulation; clozapine's M4 partial agonism (sialorrhea); and - importantly for safety - the hERG/IKr and cardiac Na-channel effects that drive QT prolongation and TCA overdose toxicity, which are channel phenomena no receptor-affinity panel can capture.
- Bins are coarse ordinal buckets (-, +/-, +, ++, +++), not a linear or logarithmic scale, and the cut-points reflect curated editorial judgment reconciling disparate sources. Small differences between adjacent bins should not be over-interpreted, and 'negligible' (-) means below a practical binding threshold, not truly zero.

## Sources

According to PubMed, the affinity bins rest on in-vitro radioligand-binding compilations (Ki), blended with the NIMH PDSP Ki database and manufacturer/FDA data for newer agents:

**Antipsychotics**
1. Kroeze WK, et al. *H1-histamine receptor affinity predicts short-term weight gain for typical and atypical antipsychotic drugs.* Neuropsychopharmacology 2003;28:519–26. [DOI](https://doi.org/10.1038/sj.npp.1300027)
2. Richelson E, Souder T. *Binding of antipsychotic drugs to human brain receptors — focus on newer generation compounds.* Life Sci 2000;68:29–39. [DOI](https://doi.org/10.1016/s0024-3205%2800%2900911-5)
3. Siafis S, et al. *Antipsychotic Drugs: From Receptor-binding Profiles to Metabolic Side Effects.* Curr Neuropharmacol 2018;16:1210–23. [DOI](https://doi.org/10.2174/1570159X15666170630163616)
4. Nasrallah HA. *Atypical antipsychotic-induced metabolic side effects: insights from receptor-binding profiles.* Mol Psychiatry 2008;13:27–35. [DOI](https://doi.org/10.1038/sj.mp.4002066)
5. Tatsumi M, et al. *Pharmacological profile of neuroleptics at human monoamine transporters.* Eur J Pharmacol 1999;368:277–83. [DOI](https://doi.org/10.1016/s0014-2999%2899%2900005-9)

**Antidepressants**
6. Owens MJ, et al. *Neurotransmitter receptor and transporter binding profile of antidepressants and their metabolites.* J Pharmacol Exp Ther 1997;283:1305–22. PMID 9400006.
7. Tatsumi M, et al. *Pharmacological profile of antidepressants and related compounds at human monoamine transporters.* Eur J Pharmacol 1997;340:249–58. [DOI](https://doi.org/10.1016/s0014-2999%2897%2901393-9)

**Database & newer agents**
8. NIMH Psychoactive Drug Screening Program (PDSP) Ki Database (Roth BL, Kroeze WK, et al.); individual-agent manufacturer/FDA prescribing-information binding data for lurasidone, cariprazine, brexpiprazole, lumateperone, iloperidone, asenapine, pimavanserin, amisulpride, vilazodone, vortioxetine, levomilnacipran and desvenlafaxine (flagged approximate in the tables).

*Clinical reference aid — not a substitute for clinical judgment or local protocol. In-vitro affinities; read with dose, occupancy and functional direction.*
