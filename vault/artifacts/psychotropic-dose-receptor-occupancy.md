---
title: Antipsychotics & Antidepressants — Dose Range and Receptor Occupancy Reference
created: 2026-07-15
type: artifact
source: manual
tags: [psychopharmacology, antipsychotics, antidepressants, receptor-occupancy, pet, dose-range, reference]
links: [Antipsychotic & Antidepressant Receptor-Binding Fingerprints — Affinity Atlas]
sources:
  - "Kapur 2000 — D2 occupancy thresholds (65/72/78%) — doi:10.1176/appi.ajp.157.4.514"
  - "Seeman 2002 — fast-off-D2, atypicality, clozapine/quetiapine transient occupancy — PMID 11873706"
  - "Tauscher 2002 — olanzapine/risperidone brain vs plasma D2 kinetics — doi:10.1038/sj.mp.4001009"
  - "Yokoi/Grunder 2002 — aripiprazole partial agonist 40-95%, no EPS >90% — doi:10.1016/S0893-133X(02)00304-4"
  - "Wong 2013 — lurasidone D2 dose-occupancy — doi:10.1007/s00213-013-3103-z"
  - "Seneca 2011 — cariprazine D3/D2-preferring partial agonist — doi:10.1007/s00213-011-2343-z"
  - "Meyer 2004 — five SSRIs ~80% SERT at minimum therapeutic dose — doi:10.1176/appi.ajp.161.5.826"
  - "Sorensen 2021 — antidepressant dose-SERT occupancy hyperbolic, ~80% plateau — doi:10.1038/s41380-021-01285-w"
  - "Hart 2024 — SNRI NET occupancy above SERT threshold; bupropion low DAT; MAOI unestablished — doi:10.1097/FTD.0000000000001142"
  - "Lundberg 2007 — escitalopram vs citalopram SERT occupancy — doi:10.1017/S1461145706007486"
  - "Kim 2017 — escitalopram regional dose-occupancy — doi:10.1007/s40262-016-0444-x"
  - "Stenkrona 2013 — vortioxetine SERT 2-97% dose-dependent — doi:10.1016/j.euroneuro.2013.01.002"
  - "Learned-Coughlin 2003 — bupropion DAT ~26% — doi:10.1016/s0006-3223(02)01834-6"
---

# Antipsychotics & Antidepressants — Dose Range and Receptor Occupancy

**Scope.** A cross-drug reference: for every commonly used antipsychotic and antidepressant, the usual adult oral dose range and the *primary-target receptor occupancy* it produces — **striatal dopamine D2** for antipsychotics, **serotonin transporter (SERT)** for antidepressants — plus the secondary receptors that drive tolerability. Occupancy is the number that turns a dose into a mechanism, and it explains two clinical facts a mg-value alone cannot: why pushing the dose higher usually adds side-effects rather than efficacy, and why two drugs at the "same" dose behave differently.

> **Read the occupancy, not just the milligrams.** Both drug classes share one lesson from PET imaging: the target is ~65–80% occupied across most of the *usual* dose range, and the dose–occupancy curve is **hyperbolic** (steep at low dose, flat once the target is saturated). Dose escalation past the plateau buys side-effects, not receptor blockade.

> **Companion:** [[psychotropic-receptor-binding-fingerprints|Receptor-Binding Fingerprints — Affinity Atlas]] maps the *in-vitro affinity* of each drug across the whole receptor panel (the fingerprint behind the side-effect profile). This report is the *in-vivo occupancy* at the primary target; read the two together.

---

## The two occupancy frameworks (read first)

### Antipsychotics — the 65–80% striatal D2 window
Every antipsychotic that works by D2 antagonism shares one target range (Kapur 2000, first-episode haloperidol PET; confirmed across typical and atypical agents by Seeman 2002):

| Striatal D2 occupancy | Consequence |
|---|---|
| **< ~65%** | usually sub-therapeutic |
| **~65%** | antipsychotic-response threshold |
| **~72%** | hyperprolactinaemia threshold |
| **~78–80%** | extrapyramidal side-effect (EPS) threshold |

So the **therapeutic window is ≈65–80% D2**. Three groups sit *outside* the plain-antagonist model:

- **Fast-off / transiently-bound agents — clozapine, quetiapine.** They achieve antipsychotic effect while striatal D2 occupancy is *low and transient*: peaks briefly after each dose, then dissociates within hours so that 24-h occupancy has "mostly disappeared" (Seeman 2002). Steady-state trough D2 is often < 60% (clozapine) or < 30% (quetiapine) — which is exactly why they cause little EPS or prolactin rise.
- **Partial agonists — aripiprazole, brexpiprazole, cariprazine.** They can occupy *> 90%* of D2 receptors and still not cause EPS, because at the occupied receptor they retain intrinsic dopaminergic activity rather than fully blocking it (Yokoi/Gründer 2002). Occupancy alone therefore does not predict EPS for this group.
- **Mesolimbic-preferential / non-D2 agents — lumateperone (low striatal D2), pimavanserin (no D2 at all — a pure 5-HT2A inverse agonist).**

5-HT2A blockade — long invoked to explain "atypicality" — is near-saturated at low doses of most SGAs, but the D2 response (65%) and EPS (80%) thresholds hold *regardless* of 5-HT2A occupancy (Seeman 2002). The window is a D2 phenomenon; 5-HT2A and fast-off kinetics widen the *therapeutic index*, not the thresholds.

### Antidepressants — the ~80% SERT threshold
For serotonergic antidepressants the analogous target is the serotonin transporter. Across five SSRIs, **~80% striatal SERT occupancy is reached at the minimum therapeutic dose** (mean 76–85%; Meyer 2004), and a systematic review of 10 antidepressants confirms a **hyperbolic** dose–occupancy curve that plateaus at ≈80% at the usual minimum recommended dose (Sørensen 2021). Clinical corollaries:

- The **starting dose already saturates SERT** — this is why SSRI dose-escalation gives a flat efficacy curve but more adverse effects, and why abrupt discontinuation (loss of ~80% blockade) produces withdrawal.
- **SNRIs** occupy SERT like SSRIs at low dose; their **noradrenaline-transporter (NET)** engagement is added at higher doses and is "sufficiently occupied, well above the SERT threshold" at recommended doses (Hart 2024). Their dual action is therefore *dose-dependent*.
- **Bupropion** is the mechanistic outlier — dopamine-transporter (DAT) occupancy is only ~26% at therapeutic doses (Learned-Coughlin 2003); NET occupancy is likewise modest.
- **MAOIs** act by enzyme (MAO-A/B) inhibition, not transporter occupancy; a concentration–occupancy relationship is not established (Hart 2024).
- **Mirtazapine, trazodone, nefazodone** are not primarily reuptake inhibitors — they work through receptor antagonism (α2, 5-HT2A/2C, 5-HT3, H1), so "SERT occupancy" does not describe them.

---

## PART A — ANTIPSYCHOTICS (dose + striatal D2 occupancy)

Doses are usual adult oral ranges for schizophrenia (formulation- and country-dependent). D2 occupancy is striatal, from PET; values marked "~" are representative of the [11C]raclopride/[18F]fallypride literature synthesised in reviews (Seeman 2002; Tauscher 2002) rather than a single measurement. Directly-measured anchors are cited inline.

### First-generation (typical) antipsychotics
Class behaviour: pure, tight-binding D2 antagonists — D2 occupancy rises with dose and **crosses 80% (EPS) readily**. High-potency agents reach the window at low mg; low-potency agents need hundreds of mg and carry heavy H1/M1/α1 loads.

| Drug | Usual dose (mg/day) | Striatal D2 occupancy | Notes / secondary receptors |
|---|---|---|---|
| Haloperidol | 2–20 (first-episode 2–4) | ~53–67% at 2 mg; **70–90%** at ≥5 mg; response > 65%, EPS > 78% (Kapur 2000) | high-potency; benchmark D2 antagonist; QT with IV use |
| Fluphenazine | 5–20 | ~70–90% at therapeutic doses | high-potency; LAI available |
| Trifluoperazine | 15–40 | ~70–90% | high-potency |
| Thiothixene | 15–60 | ~70–90% | high-potency |
| Perphenazine | 12–64 | ~70–85% | mid-potency (CATIE comparator) |
| Loxapine | 30–100 (inhaled 10 mg for agitation) | dose-dependent, ~70–85% | mid-potency; some 5-HT2A |
| Molindone | 50–225 | dose-dependent | weight-neutral |
| Chlorpromazine | 300–800 (up to 1000) | dose-dependent, ~70–90% at therapeutic doses | low-potency; **100 mg = 1 chlorpromazine-equivalent**; strong H1/M1/α1 (sedation, anticholinergic, orthostasis) |
| Thioridazine | 200–800 | dose-dependent | low-potency; **restricted — marked QT prolongation** |
| Pimozide | 1–10 | high at therapeutic doses | Tourette/delusional disorder; **QT**, CYP3A4 |
| Amisulpride¹ | 400–800 (up to 1200); 50–300 low-dose | dose-dependent; limbic-selective D2/D3 | ¹not FDA-approved (EU/other); low-dose blocks presynaptic autoreceptors for negative symptoms; prolactin |

### Second-generation (atypical) antipsychotics
| Drug | Usual dose (mg/day) | Striatal D2 occupancy | Notes / secondary receptors |
|---|---|---|---|
| Risperidone | 2–8 (usual 2–6) | ~66% at 2 mg → ~72–79% at 4–6 mg → **> 80% above 6–8 mg** | near-saturating 5-HT2A; **strong prolactin elevator**; EPS dose-dependent |
| Paliperidone | 3–12 (usual 6) | ≈ risperidone (6 mg ≈ risperidone 4–6 mg) | active metabolite of risperidone; prolactin; renally cleared |
| Olanzapine | 10–20 (to 30–40 off-label) | ~55–70% at 10 mg → ~70–80% at 20 mg (Tauscher 2002) | high H1/M1 → **weight/metabolic**; broad receptor block |
| Ziprasidone | 40–160 (BID **with food ≥ 500 kcal**) | ~45% at 40 mg → ~60–80% at 120–160 mg | high 5-HT2A; **QT**; food-dependent absorption |
| Asenapine | 10–20 (5–10 mg **sublingual** BID) | ~70–80% at 10–20 mg | must be sublingual (oral bioavailability < 2%); broad receptor block |
| Iloperidone | 12–24 (BID, slow titration) | ~60–80% | strong **α1 → orthostasis**; QT |
| **Lurasidone** | 40–160 (**with food ≥ 350 kcal**) | 40 mg→63–67%; 60 mg→77–84%; 80 mg→73–79% (Wong 2013) | 5-HT7 antagonist, 5-HT1A partial agonist; low metabolic; **akathisia** dose-dependent |
| **Quetiapine** | 300–800 (bipolar-depression add-on 150–300) | **transient** — brief peak ~40–60% post-dose, falls to < 30% at trough (fast-off; Seeman 2002) | very high H1 (sedation), α1; minimal EPS/prolactin; XR smooths the peak |
| **Clozapine** | 300–450 (up to 900; titrate) | **low steady-state ~40–60%** (< 60%); fast-off | treatment-resistant only; high 5-HT2A/M1-M4/H1/α1; **agranulocytosis, myocarditis, seizures, ileus** — REMS/ANC monitoring |
| **Aripiprazole** | 10–30 | **partial agonist** — 40–95% dose-dependent (~87% at 10 mg, > 90% at 30 mg), **no EPS even > 90%** (Yokoi/Gründer 2002) | akathisia/activation; **lowers** prolactin; long half-life |
| **Brexpiprazole** | 2–4 (1–4) | partial agonist, high occupancy (~80% at 4 mg), lower intrinsic activity | **less akathisia** than aripiprazole |
| **Cariprazine** | 1.5–6 | **D3-preferring** D2/D3 partial agonist; dose-dependent to > 90% (Seneca 2011) | very long-acting active metabolite (weeks); akathisia |
| Lumateperone | 42 (fixed dose) | **low striatal D2 (~40%)** — mesolimbic-preferential | high 5-HT2A; low EPS/metabolic |
| Pimavanserin | 34 (fixed dose) | **none — no D2 activity** | selective **5-HT2A inverse agonist**; Parkinson's-disease psychosis; the "antipsychotic without D2" |

*Long-acting injectables* (risperidone, paliperidone, aripiprazole, olanzapine, fluphenazine/haloperidol decanoate) target the **same ≈65–80% D2 window** at steady state; dosing is per-injection-interval and occupancy is smoother than oral peaks — the receptor target does not change, only the kinetics.

---

## PART B — ANTIDEPRESSANTS (dose + SERT / NET / DAT occupancy)

Doses are usual adult oral ranges for major depression. Transporter occupancy is from PET where available; SSRI/SNRI SERT values rest on Meyer 2004, Sørensen 2021 and Hart 2024. TCA and MAOI occupancy are poorly PET-characterised and are inferred from in-vitro potency and plasma levels (flagged below).

### SSRIs — ~80% SERT at the minimum therapeutic dose
The defining fact: the **starting dose already delivers ~80% SERT occupancy** (Meyer 2004); higher doses sit on the flat top of the hyperbola (Sørensen 2021).

| Drug | Usual dose (mg/day) | SERT occupancy | Notes / secondary actions |
|---|---|---|---|
| Fluoxetine | 20–80 | ~80% at 20 mg | long t½ (norfluoxetine 1–2 wk) → self-tapering, **least withdrawal**; activating; CYP2D6/3A4 inhibitor |
| Sertraline | 50–200 | ~80% at 50 mg | modest **DAT** occupancy at higher doses (unique, small); GI effects |
| Paroxetine | 20–50 (CR 25–62.5) | ~80% at 20 mg | most anticholinergic SSRI; short t½ → **worst discontinuation**; weight gain; CYP2D6 inhibitor |
| Citalopram | 20–40 (**max 40; 20** if > 60 y, CYP2C19-poor, or hepatic) | ~80% at 20 mg | **QT dose-cap (FDA)** |
| Escitalopram | 10–20 | ~80% at 10–20 mg (single-dose/regional studies show some regions need > 20 mg — Lundberg 2007, Kim 2017) | S-enantiomer of citalopram; cleanest SSRI profile |
| Fluvoxamine | 100–300 | ~80% at ~50–100 mg | **sigma-1** agonist; strong CYP1A2/2C19 inhibitor; mainly OCD |

### SNRIs — SERT at low dose, NET added higher up
| Drug | Usual dose (mg/day) | SERT / NET occupancy | Notes |
|---|---|---|---|
| Venlafaxine | 75–225 (to 375) | SERT ~80% at 75 mg; **NET meaningful > 150 mg** | short t½ → notable discontinuation; dose-dependent ↑BP |
| Desvenlafaxine | 50 (50–100) | as venlafaxine (its active metabolite) | flat dose-response above 50 mg |
| Duloxetine | 40–120 (usual 60) | SERT + **NET occupied above SERT threshold** at recommended doses (Hart 2024) | also neuropathic pain, fibromyalgia; hepatic caution |
| Levomilnacipran | 40–120 | **NET-preferring** (NET > SERT) | most noradrenergic SNRI |
| Milnacipran | 100–200 | balanced SERT/NET | US: **fibromyalgia** indication |

### Atypical / multimodal antidepressants
| Drug | Usual dose (mg/day) | Occupancy / mechanism | Notes |
|---|---|---|---|
| Bupropion (NDRI) | 150–450 (SR/XL) | **DAT ~26%** (Learned-Coughlin 2003) + modest NET; **no SERT** | no sexual dysfunction/weight gain; **dose-dependent seizure risk** (avoid in eating disorders, seizure) |
| Vortioxetine | 5–20 | SERT dose-dependent — ~50% at 5 mg, ~80%+ needs 20 mg (Stenkrona 2013) + 5-HT1A agonist, 5-HT3/7/1D antagonist | "multimodal"; pro-cognitive claims; nausea |
| Vilazodone | 20–40 (**with food**) | SERT + **5-HT1A partial agonist** (SERT occupancy less PET-characterised) | food ↑ absorption markedly |
| Mirtazapine (NaSSA) | 15–45 | **no transporter occupancy** — α2 antagonist + 5-HT2A/2C, 5-HT3, potent **H1** | sedation/appetite strongest at *low* dose; useful for insomnia, cachexia |
| Trazodone (SARI) | 150–400 (to 600); 25–100 hypnotic | 5-HT2A antagonist; **SERT only at higher antidepressant doses**; α1, H1 | mostly used as a hypnotic; priapism risk |
| Nefazodone | 300–600 | 5-HT2A antagonist + weak SERT | **hepatotoxicity (boxed warning)** — largely withdrawn |

### Tricyclic antidepressants (TCAs) — SERT and/or NET, plus antihistamine/anticholinergic/α1
Transporter occupancy is not well PET-characterised; the SERT-vs-NET *balance* below is from in-vitro potency, and dosing is guided by **plasma-level therapeutic drug monitoring** and a narrow therapeutic index.

| Drug | Usual dose (mg/day) | Transporter preference | Notes |
|---|---|---|---|
| Clomipramine | 100–250 | **most serotonergic** TCA (SERT) | OCD; seizure risk |
| Amitriptyline | 75–150 (to 300 inpatient) | balanced SERT/NET | potent H1/M1/α1 → sedation, anticholinergic, orthostasis; migraine/pain |
| Imipramine | 75–300 | SERT + NET | prototype TCA; enuresis |
| Nortriptyline | 50–150 | **NET-preferring** | therapeutic window **50–150 ng/mL**; best-tolerated TCA |
| Desipramine | 100–300 | **NET-selective** | most activating/least anticholinergic |
| Doxepin | 75–300 (**3–6 mg for insomnia**) | SERT + NET | at 3–6 mg is a pure H1 antihistamine (hypnotic) |

*All TCAs: narrow therapeutic index, **lethal in overdose** (cardiac Na-channel blockade); avoid in conduction disease / recent MI.*

### MAOIs — enzyme inhibition, not transporter occupancy
| Drug | Usual dose | Mechanism | Notes |
|---|---|---|---|
| Tranylcypromine | 30–60 mg/day | irreversible MAO-A/B | concentration–MAO-A occupancy not established (Hart 2024) |
| Phenelzine | 45–90 mg/day | irreversible MAO-A/B | requires **tyramine-restricted diet** |
| Isocarboxazid | 20–60 mg/day | irreversible MAO-A/B | |
| Selegiline (transdermal) | 6–12 mg/24 h | MAO-B (oral) / MAO-A+B (patch) | **6 mg patch avoids dietary restriction** (spares gut MAO-A); oral selegiline is Parkinson's MAO-B |

*All MAOIs: **serotonin-syndrome and hypertensive-crisis** risk — see safety section; washout required when switching.*

---

## CRITICAL SAFETY — doses and combinations to avoid

- **Do not chase D2 > 80%.** Pushing an antipsychotic above the 65–80% window adds EPS, akathisia and hyperprolactinaemia — **not** antipsychotic efficacy (Kapur 2000). "More milligrams" is not "more antipsychotic." (Partial agonists and clozapine/quetiapine are read differently — see the frameworks.)
- **MAOI + any serotonergic drug → serotonin syndrome.** Never combine MAOIs with SSRIs, SNRIs, TCAs (esp. clomipramine), tramadol, linezolid, triptans, or St John's wort. Observe washout: ≥ 14 days off/on an MAOI; **5 weeks after fluoxetine**. MAOI + dietary **tyramine → hypertensive crisis**.
- **QT-prolonging agents and dose caps.** Citalopram max **40 mg** (20 mg if elderly / CYP2C19-poor / hepatic); watch ziprasidone, iloperidone, thioridazine, pimozide, IV haloperidol. Avoid stacking QT-prolongers; check ECG, K⁺, Mg²⁺.
- **Clozapine** — agranulocytosis, myocarditis, seizures, constipation/ileus: mandatory ANC monitoring (REMS); reserved for treatment resistance.
- **TCAs are lethal in overdose** (cardiac Na-channel blockade); dispense cautiously in at-risk patients and avoid in conduction disease.
- **Serotonin syndrome** can arise from any serotonergic combination, not only MAOIs (e.g. SSRI/SNRI + tramadol/triptan/linezolid).

---

## Method, scope & caveats

- **Dose ranges** are usual approved adult oral ranges (schizophrenia for antipsychotics, major depression for antidepressants) from standard prescribing references; they vary by indication, age, formulation, hepatic/renal function, pharmacogenetics and country. Several agents (amisulpride, sulpiride, some formulations) are not FDA-approved. This is a reference aid, **not a dosing protocol** — verify locally before prescribing.
- **Occupancy** is *primary-target* occupancy: striatal D2 for antipsychotics, SERT for serotonergic antidepressants. PET values depend on radioligand, brain region, and timing relative to dose; many derive from small or single-dose healthy-volunteer studies. Figures with "~" are representative of the synthesised literature, not one measurement; directly-measured values are cited inline (haloperidol, aripiprazole, lurasidone, cariprazine; the SSRIs, escitalopram, vortioxetine, bupropion).
- **Not covered** as occupancy: mirtazapine/trazodone/nefazodone (receptor antagonists, not reuptake blockers), MAOIs (enzyme inhibition), and TCAs (poorly PET-characterised — potency balance shown instead).

## Sources

According to PubMed, the receptor-occupancy figures rest on the following PET and systematic-review studies (dose ranges are from standard prescribing references):

**Antipsychotic D2 occupancy**
1. Kapur S, et al. *Relationship between dopamine D2 occupancy, clinical response, and side effects: a double-blind PET study of first-episode schizophrenia.* Am J Psychiatry 2000;157:514–20. [DOI](https://doi.org/10.1176/appi.ajp.157.4.514)
2. Seeman P. *Atypical antipsychotics: mechanism of action.* Can J Psychiatry 2002;47:27–38. PMID 11873706.
3. Tauscher J, et al. *Significant dissociation of brain and plasma kinetics with antipsychotics.* Mol Psychiatry 2002;7:317–21. [DOI](https://doi.org/10.1038/sj.mp.4001009)
4. Yokoi F, Gründer G, et al. *Dopamine D2 and D3 receptor occupancy in normal humans treated with aripiprazole (OPC 14597): a PET study with [11C]raclopride.* Neuropsychopharmacology 2002;27:248–59. [DOI](https://doi.org/10.1016/S0893-133X%2802%2900304-4)
5. Wong DF, et al. *Determination of dopamine D2 receptor occupancy by lurasidone using PET in healthy male subjects.* Psychopharmacology 2013;229:245–52. [DOI](https://doi.org/10.1007/s00213-013-3103-z)
6. Seneca N, et al. *Occupancy of dopamine D2 and D3 and serotonin 5-HT1A receptors by cariprazine (RGH-188) in monkey brain measured using PET.* Psychopharmacology 2011;218:579–87. [DOI](https://doi.org/10.1007/s00213-011-2343-z)
7. Wadenberg ML, Kapur S, et al. *Dopamine D2 receptor occupancy is a common mechanism underlying animal models of antipsychotics and their clinical effects.* Neuropsychopharmacology 2001;25:633–41. [DOI](https://doi.org/10.1016/S0893-133X%2801%2900261-5)

**Antidepressant SERT / NET / DAT occupancy**
8. Meyer JH, et al. *Serotonin transporter occupancy of five SSRIs at different doses: an [11C]DASB PET study.* Am J Psychiatry 2004;161:826–35. [DOI](https://doi.org/10.1176/appi.ajp.161.5.826)
9. Sørensen A, Ruhé HG, Munkholm K. *The relationship between dose and serotonin transporter occupancy of antidepressants — a systematic review.* Mol Psychiatry 2022;27:192–201. [DOI](https://doi.org/10.1038/s41380-021-01285-w)
10. Hart XM, Gründer G, et al. *Update Lessons from PET Imaging Part II: a systematic critical review on therapeutic plasma concentrations of antidepressants.* Ther Drug Monit 2024;46:155–69. [DOI](https://doi.org/10.1097/FTD.0000000000001142)
11. Lundberg J, Farde L, et al. *PET measurement of serotonin transporter occupancy: a comparison of escitalopram and citalopram.* Int J Neuropsychopharmacol 2007;10:777–85. [DOI](https://doi.org/10.1017/S1461145706007486)
12. Kim E, Howes OD, et al. *Regional differences in serotonin transporter occupancy by escitalopram: an [11C]DASB PK-PD study.* Clin Pharmacokinet 2017;56:371–81. [DOI](https://doi.org/10.1007/s40262-016-0444-x)
13. Stenkrona P, Halldin C, Lundberg J. *5-HTT and 5-HT1A receptor occupancy of vortioxetine (Lu AA21004): a PET study in control subjects.* Eur Neuropsychopharmacol 2013;23:1190–8. [DOI](https://doi.org/10.1016/j.euroneuro.2013.01.002)
14. Learned-Coughlin SM, et al. *In vivo activity of bupropion at the human dopamine transporter as measured by PET.* Biol Psychiatry 2003;54:800–5. [DOI](https://doi.org/10.1016/s0006-3223%2802%2901834-6)

*Clinical reference aid — not a substitute for clinical judgment or local protocol. Dose ranges from standard prescribing references; occupancy from the cited PET literature.*
