---
title: Deep Transcranial Magnetic Stimulation (Deep TMS) — Comprehensive Review
created: 2026-07-16
type: artifact
source: comprehensive-review
tags: [neuromodulation, deep-tms, tms, h-coil, depression, ocd, smoking-cessation, psychiatry]
links: [Neuromodulation MOC]
---

# Deep Transcranial Magnetic Stimulation (Deep TMS) — Comprehensive Review
*2026-07-16 · PubMed 42 · trials 17 · sections 10*

> Assumed (the intent-lock picker was interrupted before it could be answered, so these are defaults — say if any is wrong): a **whole-modality** review of Deep TMS as a treatment technology, with **delivery protocols and efficacy carrying the depth**; **all indications** — the four FDA-cleared uses (major depression, OCD, smoking cessation, anxious depression) plus the investigational pipeline; **clinician self-study** register.
> Arc note: the object is a treatment *technology*, not a disorder, so the canonical disorder arc is adapted to a device/modality arc (device class · reach · mechanism · treatment course · patient selection · comparators · protocols & efficacy by indication · special populations · durability · controversies). No section is dropped.
> Thin sections (written thin, and said so): §2 Reach & utilization (little formal adoption data exists) and §8 Special populations (few dedicated trials).
> One boundary: this is the evidence *landscape*, not a patient-level verdict. "Should I use Deep TMS for this patient?" is a decision — route it to pubmed-research-note.

## Definition & device class

Deep transcranial magnetic stimulation (Deep TMS, dTMS) is a form of repetitive TMS (rTMS) that uses **Hesed ("H") coils** instead of the conventional figure-8 coil. A time-varying magnetic pulse induces an electric field in cortical tissue; where the figure-8 coil produces a focal, rapidly-decaying field, the H-coil's winding geometry produces a **broader and deeper** field, reaching structures a focal coil cannot without unsafe surface intensities. "Deep" therefore refers to **field penetration**, not to direct stimulation of deep grey-matter nuclei — a distinction that matters mechanistically (§3).

The technology was developed in the early 2000s and commercialised by a single manufacturer (Brainsway); the H-coil is its defining component. The coil is not one device but a **family**, each shaped for a different target:

- **H1** — bilateral prefrontal, left-weighted → **major depression**
- **H7** — medial prefrontal cortex + dorsal anterior cingulate → **OCD**
- **H4 / H-ADD** — bilateral prefrontal + insula → **addiction / smoking cessation**
- others in research use — H2, an insula-targeting variant used with a temporal montage, and a dorsomedial variant trialled in autism.

Its regulatory identity is the clearest way to place it: the H-coil is the basis of **four US FDA clearances in sequence** — major depressive disorder (2013), obsessive–compulsive disorder (2018), smoking cessation (2020, the first device ever cleared for that indication), and anxious depression (2021, a label expansion). Reviews confirm that of the small number of rTMS coils cleared for OCD, the H7 is one.

In the neuromodulation taxonomy, dTMS sits with rTMS as **non-invasive** (unlike deep brain stimulation or vagus-nerve stimulation), **non-convulsive** and **anaesthesia-free** (unlike electroconvulsive therapy), and **outpatient**. Its selling proposition relative to standard rTMS is reach; its cost, as the physics section shows, is focality.

## Reach, regulatory footprint & evidence base

*(A thin section: adoption and utilisation are poorly quantified in the peer-reviewed literature; what can be said is said, and no more.)*

The formal footprint is the four cleared indications above, anchored by three registration-grade multicentre trials (§7). At the level of the **treatment class**, professional guidance is now firmly supportive: the CANMAT neurostimulation guideline recommends rTMS as a **first-line** option for major depression after failure of at least one antidepressant, with ECT reserved to second-line and tDCS/VNS to third — a positioning that lends dTMS its clinical standing even though the guideline speaks to rTMS broadly rather than the H-coil specifically.

The research footprint is substantial but concentrated. A systematic review of **sham-controlled dTMS trials identified 28 studies**, with the efficacy signal concentrated in OCD, substance-use disorders, and depressive episodes (major and bipolar), and heterogeneous or weak signals elsewhere. An umbrella review spanning **102 meta-analyses** of TMS placed depression among the better-supported indications (see §7). The ClinicalTrials.gov registry holds on the order of **59 ongoing and 83 completed** dTMS/H-coil/Brainsway records (raw counts, some non-dTMS noise), of which roughly **41 are manufacturer-sponsored** — a footprint dominated by a single commercial developer, which is itself relevant to how the evidence should be read (§10).

What is genuinely thin is **real-world adoption data**: how many devices are installed, how many courses are delivered, adherence and dropout in routine practice, and payer coverage are not systematically reported in the literature. This gap is named, not filled.

## Etiology & pathophysiology — mechanism & neurobiology

The mechanistic story has two layers: the **physics** of the induced field, and the **neurobiology** it sets in motion.

**The field.** Phantom-mapping studies established the H-coil's signature: at 120% of the hand motor threshold, the H1 coil induces a supra-threshold field to a depth of roughly **4–5 cm**, against roughly **1.5 cm** for a figure-8 coil — a review synthesis puts H-coil penetration at up to ~6 cm. Computational realistic-head-model work confirms that H-coils penetrate significantly deeper than figure-8 coils, though **less deeply than a double-cone coil**, and — crucially — that depth is bought at the cost of **focality**: the deeper the supra-threshold volume, the wider it is. There is no free lunch; a coil that reaches farther also stimulates a larger, less selective volume.

**What is actually stimulated.** A consensus position paper on the biophysics of TMS locates the primary target not in deep nuclei but in **axonal terminals and bends at the gyral crown and juxtacortical white matter**, where the induced field is strongest — which is superficial. The clinical implication reframes "deep": the H-coil most plausibly works by engaging a **broader expanse of cortex and its network connections**, with effects then propagating **trans-synaptically** to limbic and subcortical targets, rather than by directly depolarising structures centimetres below the surface. Connectivity data support this network reading — more effective dorsolateral-prefrontal targets in depression are those **functionally connected to the subgenual cingulate**, motivating connectivity-guided targeting.

**Downstream neurobiology.** High-frequency stimulation (the 18–20 Hz used for depression and OCD) is broadly **excitatory**, raising cortical excitability, whereas 1 Hz is inhibitory (used in the hallucination work of §7). Proposed durable mechanisms include LTP-like **synaptic plasticity** and normalisation of pathological network connectivity; one convergent line across brain-stimulation modalities is **attenuation of neuroinflammation** and pro-inflammatory signalling as a substrate of mood improvement. These remain mechanistic hypotheses, better evidenced at the level of "the network changed" than "this molecule did it."

## Clinical features & course — the treatment course

A course of dTMS is a defined procedure, not a titrated drug. It opens with **motor-threshold determination** — the operator finds the minimum intensity evoking a hand-muscle response and sets treatment intensity relative to it, typically **110–120% of motor threshold**.

The **session** is coil- and indication-specific but shares a train structure. The depression protocol delivers **18 Hz** in **55 trains** of 2 s on / 20 s off — about **1,980 pulses** in roughly **20 minutes** over the prefrontal cortex. The OCD protocol delivers **20 Hz** (~2,000 pulses) but is **preceded by individualised symptom provocation** to bring the target circuit "online" before stimulation. The smoking protocol is likewise **preceded by cue-induced craving**, stimulating prefrontal cortex and insula.

The **acute course** is intensive and front-loaded. Depression: **20 daily sessions over 4 weeks**, then a biweekly taper continuing to roughly week 16. OCD: **daily over about 6 weeks** (~29 sessions). Smoking: **15 daily sessions across 3 weeks, then 3 weekly** sessions. Response is gradual rather than immediate, typically consolidating over the **4–6 week** acute phase — a tempo that shapes patient counselling and the choice of maintenance (§9).

## Diagnosis & assessment — patient selection

Because dTMS is procedural, "diagnosis" here is **candidate selection and screening**.

**Who is a candidate.** In depression, the treated population is functionally **treatment-resistant** — the guideline threshold that makes rTMS first-line is failure of **at least one adequate antidepressant trial**, and the registration cohorts were more resistant than that. In OCD, candidacy follows inadequate response to SSRIs and CBT. In smoking, it is adults seeking cessation, generally after other aids.

**Screening and contraindications.** The dominant safety concern is **seizure** (§ below), so screening targets seizure-threshold-lowering factors — personal/family epilepsy history, relevant medications, sleep deprivation, alcohol withdrawal. Ferromagnetic or active implanted hardware near the coil (aneurysm clips, cochlear implants, some neurostimulators/pacemakers) is a **contraindication**. The IFCN safety guidelines that govern rTMS screening and dosing apply.

**Measurement.** Outcomes are tracked on validated scales — the **HDRS/HAM-D or MADRS** for depression, the **Y-BOCS** for OCD, and biochemically-verified continuous-abstinence/quit rates for smoking — the same instruments that define response and remission in the trials below.

## Differential & comorbidity — comparators, and where dTMS sits

The clinically live "differential" is **which neuromodulation option**, and above all **dTMS versus standard figure-8 rTMS**.

**Versus figure-8 rTMS.** This is the field's unsettled question and it does not resolve cleanly in dTMS's favour. Coil-modelling and a single head-to-head clinical comparison suggest the H1 coil's broader, deeper field confers a **clinical and effect-size advantage** in depression. But the largest **network meta-analysis (81 studies, 4,233 patients)** reached the opposite class-level conclusion: **"accelerated, synchronised, and deep rTMS were not more effective than sham,"** while conventional high-frequency rTMS clearly was (OR 3.07, 95% CI 2.24–4.21). A second network meta-analysis (**113 trials, 6,750 patients**) ranked bilateral rTMS (OR 4.92) and high-frequency left rTMS (OR 3.17) above sham with deep rTMS among the strategies but not atop them. The honest reading: **deep TMS is effective, but it has not demonstrated superiority over standard rTMS** in pooled comparisons, and head-to-head RCTs remain scarce.

**Versus iTBS.** Intermittent theta-burst compresses a session to a few minutes; a manufacturer non-inferiority trial tested iTBS against standard high-frequency H1 stimulation in depression (§10).

**Versus ECT.** ECT remains **more efficacious for severe, psychotic, or emergency depression** and sits second-line where rTMS is first; dTMS trades that ceiling for no anaesthesia, no seizure induction, no cognitive burden, and outpatient delivery.

**Combination with pharmacotherapy.** The signal that **only dTMS combined with an antidepressant** reached significance for response and remission in one meta-analysis argues for positioning dTMS as an **augmentation** of ongoing medication rather than a standalone.

## Treatment — protocols & efficacy by indication

This is the core of the review. Each indication is given its coil, its protocol, and its evidence.

### Major depressive disorder (H1 coil)

**Protocol.** 18 Hz at 120% motor threshold, 55 trains (2 s on / 20 s off), ~1,980 pulses per session over prefrontal cortex; 20 daily sessions across 4 weeks, then a biweekly continuation to ~week 16.

**Pivotal evidence.** The multicentre double-blind RCT behind the 2013 clearance (**n=212**) showed HDRS-21 improvement of **6.39 points with dTMS vs 3.28 with sham** (p=0.008; effect size 0.76), **response 38.4% vs 21.4%** (p=0.013), and **remission 32.6% vs 14.6%** (p=0.005) at week 5 — a real but moderate separation from sham, achieved in a treatment-resistant population.

**Pooled evidence.** A meta-analysis of 5 RCTs (**n=507** treatment-resistant) found **response 45.3% vs 24.2%** (RR 1.87, 95% CI 1.21–2.91) and **remission 38.3% vs 14.4%** (RR 2.37), depression SMD −0.65. Open-label pooling runs higher (Cohen's d 2.04; response ~60%, remission ~29%) — the expected inflation of uncontrolled data. One meta-analysis found the significant response/remission advantage held **only for dTMS added to an antidepressant**, and a GRADE appraisal, reading the controlled evidence strictly, judged support **"insufficient"** and noted the sham difference was not statistically significant in its analysis. The tension between the positive pooled RCTs and the sceptical network/GRADE readings is the depression story in one line: **efficacious, moderate, and not clearly better than cheaper focal rTMS.**

### Obsessive–compulsive disorder (H7 coil)

**Protocol.** 20 Hz over medial prefrontal cortex + dorsal anterior cingulate, each session **preceded by individualised symptom provocation**; daily over ~6 weeks (~29 sessions).

**Pivotal evidence.** The multicentre (11-site) sham-controlled RCT behind the 2018 clearance (**n=99**) showed a **Y-BOCS reduction of 6.0 vs 3.3 points**, **response (≥30% Y-BOCS reduction) 38.1% vs 11.1%** at end of treatment, rising to **45.2% vs 17.8% at one-month** follow-up. Secondary analysis found dTMS retained efficacy **even in patients who had failed multiple medications and CBT** — the refractory group where it is actually needed. A single-centre retrospective series (n=29) reported that all responded (≥35% Y-BOCS reduction) with QEEG beta-power reduction tracking improvement. OCD is, on the sham-controlled evidence, the indication where dTMS looks **strongest**.

### Smoking cessation and other addictions (H4 coil)

**Protocol.** Bilateral lateral prefrontal cortex + insula, each session **preceded by cue-induced craving**; 15 daily sessions across 3 weeks, then 3 weekly.

**Pivotal evidence.** The multicentre RCT behind the 2020 clearance — the **first FDA clearance for smoking cessation by any device** (**n=262**, ITT 234) — showed a **4-week continuous quit rate through week 18 of 19.4% vs 8.7%** (p=0.017), and **28.0% vs 11.7% among completers** (p=0.007). The preceding pilot (n=115) had found high-frequency stimulation with smoking cues gave ~44% abstinence at end of treatment and ~33% at 6 months. The umbrella review graded the **substance-use** signal for deep/dorsolateral-prefrontal HF-TMS at **SMD 1.16 (GRADE moderate)** — the *largest* effect size across its indications. Addiction beyond nicotine is now the busiest frontier (§10): an insula-targeting H-coil variant combined with varenicline reported **82.4% vs 30.7%** 7-day point-prevalence abstinence at week 12 in a small RCT (n=42) — a different coil, but a signal that circuit-plus-drug combinations may outperform either alone.

### Anxious depression (H1 coil)

The 2021 clearance is a **label expansion, not a new trial**: there is **no dedicated anxious-depression pivotal** in the literature; the clearance rests on **reduction of comorbid anxiety within the depression programme**. Supporting numbers are indirect but consistent — anxiety Hedges' g −1.282 alongside the depression effect in one meta-analysis, anxiety improvement (g up to 1.72) in an open-label augmentation series, and a generalised-anxiety TMS SMD of 0.68 in the umbrella review. Read it as "depression treatment that also moves comorbid anxiety," not as an independent anxiety indication.

### Investigational indications

- **PTSD — negative.** This is the cautionary tale. After a positive pilot (n=30, benefit on intrusive symptoms), the pivotal multisite RCT (**n=125**) of H7 mPFC stimulation with brief exposure was **negative in the wrong direction**: sham numerically **outperformed** active dTMS (CAPS-5 improvement 16.32 with dTMS vs 20.52 with sham, p=0.027). A large registration-scale trial (n=203) was **terminated**. dTMS is **not** established for PTSD, and the provocation-plus-stimulation paradigm that works in OCD did not transfer.
- **Bipolar depression — promising but unsettled.** An H1 RCT (n=50) showed active > sham at week 4 (difference 4.88, 95% CI 0.43–9.32, p=0.03) but **not at follow-up**; response 48% vs 24% (OR 2.92, p=0.08) missed significance; importantly **no treatment-emergent mania**, and cognition was unaffected. A manufacturer bipolar trial (n=120) sits in **unknown registry status**.
- **Schizophrenia — weak.** An open-label series (n=8) reported a 31.7% drop in auditory-hallucination scores with 1 Hz temporoparietal stimulation, but the controlled follow-up (n=18) found **no significant active-vs-sham difference**.
- **Autism.** A sham-controlled RCT (n=28) of dorsomedial-prefrontal deep rTMS reported reduced social-relating symptoms and social anxiety — an early, single positive signal.
- Exploratory work (Alzheimer's + cognitive training, adult ADHD, spinocerebellar ataxia) exists mostly as small or unreported trials (§10).

## Special populations

*(Thin: dedicated trials are few; the honest content is mostly "under-studied.")*

- **Late-life depression.** A treatment-resistant late-life cohort (n=58) tested H1 dTMS vs sham — the population where efficacy and tolerability most need dedicated data, and where the evidence remains sparse.
- **Adolescents.** An open-label pilot in adolescent treatment-resistant depression (**n=15**, H1, 1,980 pulses/session, 80–120% MT) had **6/15 responders** and, notably, **one convulsive syncope** — a reminder that the seizure-safety margin deserves extra caution in developing brains. Dedicated adolescent trials are only now recruiting (§10).
- **Pregnancy.** dTMS delivers **no systemic drug and no fetal pharmacological exposure**, which makes it conceptually attractive in pregnancy — but there is **no dedicated dTMS pregnancy trial**, so this rationale is theoretical for the H-coil specifically `[unverified]`.
- **Cognitive safety across populations.** Reassuringly consistent: dTMS is **cognitively safe but not pro-cognitive** — a bipolar cognitive-safety analysis found improvement across domains regardless of active or sham, and a systematic review of cognition found most studies show no significant change.

## Prognosis — durability & maintenance

Acute response is not the whole story; **relapse after a successful course is the rule without a plan for it**, as with rTMS generally.

The maintenance evidence, though small, points one way. A controlled maintenance study (n=24) found HDRS scores **stayed stable with maintenance dTMS but rose significantly without it at both 6 and 12 months** — maintenance matters. A Phase IV real-world registry of **accelerated** dTMS (n=111) reported **80.2% response and 50.5% remission** in the first month, with durability of **86.7% at 60 days** (n=30) and **92.9% at 180 days** (n=14) — but the durability denominators are tiny and the authors are from the manufacturer, so these figures are best read as **encouraging and in need of independent replication** rather than as settled durability rates. Predictors of sustained response (connectivity, symptom profile) are an active question, not an answered one.

## Controversies & future directions

**Is "deeper" actually better?** The central controversy. The rationale for the H-coil is depth and breadth of field; the pooled network evidence says deep rTMS is **not superior to standard high-frequency rTMS**, which is cheaper and more focal. The biophysics suggests any advantage comes from **broader cortical/network engagement**, not direct deep-structure stimulation — which, if true, undercuts the naming more than the method. What would settle it — **adequately powered head-to-head dTMS-vs-rTMS RCTs** — barely exists; a comparative trial is only now active.

**Blinding.** The H-coil produces a **strong scalp sensation**; if sham does not reproduce it, unblinding inflates the apparent effect. Sham-integrity is a standing threat to the depression effect sizes above.

**Accelerated and theta-burst delivery.** Multiple sessions per day (the accelerated registry) and **iTBS on the H-coil** (a manufacturer non-inferiority trial vs standard H1) aim to compress a 4–6 week course into days — the most likely near-term change to how dTMS is delivered. (Note that the widely-cited high-remission accelerated SAINT/SNT protocol used a *figure-8* coil, not the H-coil — a common conflation.)

**Personalisation.** Connectivity-guided targeting and candidate biomarkers (functional connectivity to subgenual cingulate; QEEG signatures) point toward individualised rather than one-target-fits-all stimulation.

**The pipeline** (registry harvest). The centre of gravity has shifted to **addiction**: a manufacturer alcohol-use-disorder registration-scale trial (n=186, readout 2027), a separate academic AUD trial (n=100, 2030), methamphetamine (n=30, 2026) and cocaine-plus-contingency-management (n=100, 2029) trials, alongside bipolar depression (n=100, 2025), accelerated OCD (n=50, 2027), adolescent depression (n=100, 2025), and youth-mood response-prediction (n=180, 2027) studies.

**A reporting-transparency flag.** The three flagship trials were journal-published, but **none of the large completed manufacturer trials has results posted on ClinicalTrials.gov**, and several completed or unknown-status trials — bipolar depression (n=120), a mood-disorder cohort (n=228), ADHD, autism, Alzheimer's — have **neither registry results nor prominent publications**. Combined with a heavily single-sponsor evidence base, this selective-visibility pattern is a reason to weight the independent and negative data (the network meta-analyses, the GRADE appraisal, the failed PTSD trial) more heavily than headline open-label figures.

## Sources

- Deep TMS pivotal trial in major depression (multicentre RCT, n=212) — [doi:10.1002/wps.20199](https://doi.org/10.1002/wps.20199)
- Deep TMS pivotal trial in OCD (multicentre RCT, n=99) — [doi:10.1176/appi.ajp.2019.18101180](https://doi.org/10.1176/appi.ajp.2019.18101180)
- Deep TMS pivotal trial in smoking cessation (multicentre RCT, n=262) — [doi:10.1002/wps.20905](https://doi.org/10.1002/wps.20905)
- Smoking-cessation dTMS pilot with cue provocation (RCT, n=115) — [doi:10.1016/j.biopsych.2014.05.020](https://doi.org/10.1016/j.biopsych.2014.05.020)
- Meta-analysis of dTMS in treatment-resistant depression, response/remission (5 RCTs, n=507) — [doi:10.1016/j.ajp.2024.104032](https://doi.org/10.1016/j.ajp.2024.104032)
- Meta-analysis of dTMS in depression, open-label effect size (9 studies) — [doi:10.1016/j.jad.2015.08.033](https://doi.org/10.1016/j.jad.2015.08.033)
- Meta-analysis of dTMS depression/anxiety and the combination effect (15 studies) — [doi:10.1016/j.pnpbp.2019.109850](https://doi.org/10.1016/j.pnpbp.2019.109850)
- Network meta-analysis finding deep rTMS not superior to sham (81 studies, 4,233 patients) — [doi:10.1001/jamapsychiatry.2016.3644](https://doi.org/10.1001/jamapsychiatry.2016.3644)
- Network meta-analysis of rTMS strategies in depression (113 trials, 6,750 patients) — [doi:10.1136/bmj.l1079](https://doi.org/10.1136/bmj.l1079)
- Umbrella review of TMS across psychiatric disorders (102 meta-analyses) — [doi:10.1016/j.neubiorev.2022.104743](https://doi.org/10.1016/j.neubiorev.2022.104743)
- Systematic review of sham-controlled dTMS trials by indication (28 trials) — [doi:10.1016/j.jpsychires.2024.05.011](https://doi.org/10.1016/j.jpsychires.2024.05.011)
- GRADE appraisal judging dTMS depression evidence insufficient — [doi:10.3109/08039488.2016.1166263](https://doi.org/10.3109/08039488.2016.1166263)
- Open-label dTMS augmentation in severe treatment-resistant depression (n=17) — [doi:10.3109/15622975.2014.925141](https://doi.org/10.3109/15622975.2014.925141)
- H-coil electric-field mapping — depth vs focality (phantom) — [doi:10.1097/WNP.0b013e31802fa393](https://doi.org/10.1097/WNP.0b013e31802fa393)
- Computational realistic-head-model comparison of deep coils — [doi:10.1371/journal.pone.0178422](https://doi.org/10.1371/journal.pone.0178422)
- Coil-design review, H1 vs figure-8 in major depression — [doi:10.1016/j.euroneuro.2019.06.009](https://doi.org/10.1016/j.euroneuro.2019.06.009)
- Consensus on the physical target of TMS (axonal terminals, network spread) — [doi:10.1016/j.clinph.2022.04.022](https://doi.org/10.1016/j.clinph.2022.04.022)
- Connectivity-guided dorsolateral-prefrontal targeting for depression — [doi:10.1016/j.biopsych.2020.05.033](https://doi.org/10.1016/j.biopsych.2020.05.033)
- Neuroinflammation as a shared brain-stimulation mechanism — [doi:10.1038/s41398-022-02297-y](https://doi.org/10.1038/s41398-022-02297-y)
- Review of H-coil applications and field depth (~6 cm) — [doi:10.1016/j.eurpsy.2012.02.006](https://doi.org/10.1016/j.eurpsy.2012.02.006)
- Synthesis of IFCN TMS safety guidelines (seizure risk, screening, dosing) — [doi:10.12786/bn.2021.14.e6](https://doi.org/10.12786/bn.2021.14.e6)
- Phase IV real-world registry of accelerated dTMS in depression (n=111) — [doi:10.1016/j.psychres.2023.115482](https://doi.org/10.1016/j.psychres.2023.115482)
- Negative pivotal dTMS RCT in PTSD (n=125) — [doi:10.1016/j.biopsych.2021.04.019](https://doi.org/10.1016/j.biopsych.2021.04.019)
- dTMS pilot in PTSD, intrusive symptoms (n=30) — [doi:10.1016/j.brs.2012.07.008](https://doi.org/10.1016/j.brs.2012.07.008)
- Systematic review of neuromodulation for PTSD — [doi:10.1007/s13311-020-00871-0](https://doi.org/10.1007/s13311-020-00871-0)
- dTMS RCT in bipolar depression (n=50) — [doi:10.1038/npp.2017.26](https://doi.org/10.1038/npp.2017.26)
- Cognitive-safety analysis of dTMS in bipolar depression — [doi:10.1016/j.jad.2018.04.022](https://doi.org/10.1016/j.jad.2018.04.022)
- Maintenance dTMS durability at 6 and 12 months (n=24) — [doi:10.3389/fneur.2015.00016](https://doi.org/10.3389/fneur.2015.00016)
- Open-label dTMS for auditory hallucinations in schizophrenia (n=8) — [doi:10.1186/1744-859X-10-3](https://doi.org/10.1186/1744-859X-10-3)
- Sham-controlled dTMS RCT for auditory hallucinations, null result (n=18) — [doi:10.1186/1744-859X-11-13](https://doi.org/10.1186/1744-859X-11-13)
- H1-coil methods and repositioning across indications — [doi:10.3791/55100](https://doi.org/10.3791/55100)
- Deep rTMS RCT in autism, social-relating symptoms (n=28) — [doi:10.1016/j.brs.2013.10.004](https://doi.org/10.1016/j.brs.2013.10.004)
- Retrospective dTMS in OCD with QEEG correlates (n=29) — [doi:10.1177/15500594221095385](https://doi.org/10.1177/15500594221095385)
- Review of the H7 coil evidence across indications — [doi:10.1080/17434440.2021.2013803](https://doi.org/10.1080/17434440.2021.2013803)
- Narrative review of TMS coils cleared for OCD — [doi:10.1016/j.psc.2022.10.003](https://doi.org/10.1016/j.psc.2022.10.003)
- Secondary analysis — dTMS in OCD after medication and CBT failure — [doi:10.1016/j.psychres.2020.113179](https://doi.org/10.1016/j.psychres.2020.113179)
- Insula H-coil variant plus varenicline for smoking (RCT, n=42) — [doi:10.1016/j.brs.2023.10.002](https://doi.org/10.1016/j.brs.2023.10.002)
- Adolescent treatment-resistant depression dTMS open-label pilot, safety (n=15) — [doi:10.1016/j.jad.2024.03.061](https://doi.org/10.1016/j.jad.2024.03.061)
- CANMAT neurostimulation guideline — rTMS first-line for major depression — [doi:10.1177/0706743716660033](https://doi.org/10.1177/0706743716660033)
- WFSBP guideline positioning of rTMS in OCD and PTSD — [doi:10.1080/15622975.2022.2086296](https://doi.org/10.1080/15622975.2022.2086296)
- Review of dTMS applications beyond depression (H-coil catalogue) — [doi:10.1080/17434440.2016.1233812](https://doi.org/10.1080/17434440.2016.1233812)
- Systematic review of cognitive effects of dTMS across disorders — [doi:10.1016/j.neulet.2021.135906](https://doi.org/10.1016/j.neulet.2021.135906)

**Registry — ClinicalTrials.gov:**

- NCT00927173 — Deep TMS pivotal in major depression (H1), completed, n=233, registry results not posted; basis of 2013 FDA clearance
- NCT02229903 — Deep TMS pivotal in OCD (H7), completed, n=100, registry results not posted; basis of 2018 FDA clearance
- NCT02126124 — Deep TMS pivotal in smoking cessation (H4), phase 3, completed, n=224, registry results not posted; basis of 2020 FDA clearance
- NCT04679753 — iTBS vs high-frequency H1 in depression, non-inferiority, phase 4, completed, n=177
- NCT01860157 — Deep TMS in treatment-resistant late-life depression, completed, n=58
- NCT03718013 — accelerated vs standard Deep TMS in depression, completed, n=118
- NCT02479906 — Deep TMS in PTSD, terminated, n=203
- NCT01566591 — Deep TMS in bipolar depression, unknown status, n=120
- NCT02917499 — Deep TMS in mood disorders, completed, n=228, registry results not posted (reporting-gap flag)
- NCT07216872 — Deep TMS in alcohol use disorder, recruiting, n=186, readout 2027-11
- NCT06949423 — Deep TMS in alcohol use disorder, recruiting, n=100, readout 2030-06
- NCT06578429 — Deep TMS in methamphetamine use disorder, recruiting, n=30, readout 2026-12
- NCT07490600 — Deep TMS + contingency management in cocaine use disorder, recruiting, n=100, readout 2029-06
- NCT07116785 — accelerated Deep TMS in OCD, recruiting, n=50, readout 2027-06
- NCT06524505 — Deep TMS in bipolar depression, recruiting, n=100, readout 2025-09
- NCT06728280 — Deep TMS in adolescent depression (H1 vs H7), n=100, readout 2025-12
- NCT07188506 — Deep TMS response predictors in youth mood/suicidality, n=180, readout 2027-12

## Rendered references & spin-offs

- **Infographic** — `assets/deep-tms-protocol-reference-infographic.html` (+ `.preview.png`): a print-ready protocol & efficacy reference card rendered from this review, filed under the [[Neuromodulation MOC]].
- **Decision spin-off** — [[deep-tms-vs-standard-rtms-depression]]: a verdict-first decision report adjudicating Deep TMS vs standard figure-8 rTMS for treatment-resistant depression (the central tension of §6 and §10, resolved into an action).
