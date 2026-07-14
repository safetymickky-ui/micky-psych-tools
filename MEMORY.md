# MEMORY — micky-psych-tools living state

Fast-moving state for this marketplace. `CLAUDE.md` holds the stable conventions;
this file holds what changes. Update it whenever you release, add a plugin, or close
a milestone.

## Identity

- Personal Claude Code plugin marketplace. Owner: Thanawat Suharit (Micky).
- Remote: `origin` → https://github.com/safetymickky-ui/micky-psych-tools (**private**), branch `master`.
- Installed to Claude Code as marketplace `micky-psych-tools` (user scope).
- GitHub account `safetymickky-ui` (gh authed, `repo` scope).

## Current versions — 2026-07-13

| item                  | version |
| --------------------- | ------- |
| marketplace catalog   | 1.10.0  |
| pubmed-research-note   | 1.6.0   |
| intent-lock           | 0.4.0   |
| plugin-creator        | 0.3.0   |
| vault-keeper          | 0.4.0   |
| psych-paper-digest    | 0.1.0   |
| comprehensive-review  | 0.2.0   |
| clinical-infographic  | 0.2.1   |
| firecrawl             | 0.2.0   |

A version MUST be identical in `plugins/<name>/.claude-plugin/plugin.json` and its
`.claude-plugin/marketplace.json` entry — if they drift, Claude Code silently offers no
update. Never hand-edit versions; bump with `python3 scripts/bump.py <plugin> patch|minor|major`.

## Plugins at a glance

- **pubmed-research-note** — clinical decision from primary literature; verdict-first,
  quantified, trial-registry-checked evidence reports whose shape follows the decision, not the
  topic. Default output pipeline: write md → show inline → file to vault as an artifact via
  vault-keeper; atomic notes on "atomize" only. ALWAYS runs intent-lock first as a mandatory
  Step 0 gate (explicit opt-out only — "just search"). **No fixed frames, no fixed template**
  (removed in 1.5.0): the interview builds a bespoke *decision brief* (decision · verdict's
  shape · what settles it · what's counted · mandatory checks · anti-goal), and the report
  takes whatever shape the decision demands, guided by principles not rules. Delegates vault
  writes to vault-keeper.
- **intent-lock** — pre-build alignment gate; interrogate a request to one reading, then build.
  Ships `intent-lock` (the interview) + `misread-capture` (the compounding misread ledger).
- **plugin-creator** — meta-plugin: `/new-plugin` scaffolds, `/refine-plugin` audits/refines,
  `/route` regenerates `ROUTING.md` and routes a request to the owning skill/command. Create and
  refine keep the router in sync automatically.
- **vault-keeper** — shared knowledge-vault manager for repo-root `vault/`; five jobs: init, save,
  index, query, empty. The single place every skill's output lands. The `empty-vault` skill
  (+ `/empty-vault [topic]`) drains the vault into the Learn hub: hands each artifact to
  learn-hub's `digest-report` skill (which authors atomic Learn notes + syncs to Supabase),
  then deletes only after verified sync + git-committed state + explicit confirmation.
- **psych-paper-digest** — watchlist literature surveillance; sweeps PubMed + ClinicalTrials.gov
  since `last_swept`, triages Act / Read / Suppressed, never adjudicates (Act items hand off to
  pubmed-research-note). Skill + `/digest [domain]`; state in `.psych-paper-digest.json`.
- **comprehensive-review** — whole-disorder academic reviews, textbook-chapter breadth across a
  ten-section arc (definition → controversies), never collapsed into Rx-only. Intent-lock is the
  mandatory Step 0 gate; own PubMed + CT.gov pipeline; deliverable is an md file filed to the
  vault via vault-keeper (chat gets the Close, not the chapter). Skill + `/comprehensive-review
  [topic]`. Decisions still route to pubmed-research-note.
- **clinical-infographic** — the pipeline's last mile: renders a SOURCED report into a
  professional, print-ready medical summary infographic for clinical reference — one
  self-contained HTML file (inline styles + inline SVG, no external CSS/JS/fonts/images) with
  color-coded phase/theme columns, stat tiles, and a mandatory "medications to avoid" safety
  banner. **Visual-first (v0.2.0):** a diagram grammar — a *signature visual* (journey/timeline
  curve, mechanism strip, decision-flow, escalation ladder, paired-opposite split) designed
  before the columns, with template scaffolds; schematics must be labelled illustrative + carry
  only sourced numbers; a render-&-verify step (rasterise + OCR) before filing; PNG a named
  deliverable; a worked **dense reference** example under `examples/`. **Rendering layer, not a
  research tool** — ships no search engines and never
  fabricates a clinical fact: it resolves a source in order (this session's report → an existing
  vault artifact via vault-keeper → generate one with comprehensive-review / pubmed-research-note)
  and enforces a fidelity contract (nothing untraceable, numbers keep units + qualifiers,
  contraindications always reach the safety banner, `[unverified]` never rendered as fact). Files
  the HTML as an **asset** via vault-keeper, wired into the source report's MOC. Skill +
  `/infographic [topic-or-source]`.
- **firecrawl** — Firecrawl onboarding + routing for general-web data (search / scrape /
  interact / crawl / map via the Firecrawl CLI or API). Skill body is the vendor's official
  AI-onboarding guide kept verbatim: one install command, three vendor skill segments
  (CLI / build / workflow), six usage paths A–F. **Deep-integrated (0.2.0):** the
  marketplace's general-web evidence engine — pubmed-research-note (fifth engine in its
  catalog) and comprehensive-review call it for documents outside PubMed/CT.gov (regulator
  labels, guideline full texts, gray literature; clean markdown + URL + access date,
  fetch-only, blog ban stands); Path C deliverables gate through intent-lock and vault via
  vault-keeper on explicit request; clinical-infographic and psych-paper-digest explicitly
  not chained. Boundary: biomedical literature stays with the PubMed-facing plugins;
  `FIRECRAWL_API_KEY` lives in the environment, never the repo. One skill + 8 evals,
  no commands.

## Recent milestones

- **2026-07-14** — Filed the **Tier 2 R2R/publication candidates** (#6, #7) of the addiction-service
  accreditation research program (same branch), taking the **Addiction Psychiatry MOC to 7 artifacts** via
  pubmed-research-note → vault-keeper. **#6 Contingency management for stimulant UD — build-and-design:**
  verdict *build it* — CM is the **only** treatment reliably tied to stimulant abstinence (Bentzley meta 157
  studies: OR 2.13; Bolívar d≈0.70; De Crescenzo NMA: CM+CRA the only psychosocial intervention beating TAU,
  OR 2.84 end / 7.60 at 12 wk / 3.08 follow-up; Cochrane RR 1.89); design spec from the dismantling
  literature — objective single target (abstinence r=0.32 > attendance r=0.15, Lussier), **adequate magnitude**
  + immediacy (both dose-response moderators), **escalation with reset**, 2–3×/wk, **≥12 wk** (Ginley: longer
  active tx the durability moderator), **prize-based fishbowl** for low cost (Petry/Walker, counsellor-
  delivered), plan for **decay**; ethics guardrail (gambling-history → fixed vouchers). 9 PubMed. **#7 Retention
  interventions — what works + how to defend 30.9→79.8%:** honest finding that the stand-alone retention-
  intervention base is **thin/mixed**; best levers = **attendance-CM** (dropout RR 0.82; CM+CRA OR 3.63),
  **case management/assertive outreach** (Miler review-of-reviews), **structural supports** (phones/flexible
  scheduling — Stewart); **MI NOT reliable for retention** (Smedslund Cochrane: no better than TAU) and generic
  added counselling didn't help (Wyse); **no single retention definition** (fixed-timepoint 3/6/12-mo [OAT
  standard, Degenhardt] vs 45-day-gap [Mintz] vs planned-discharge completion [Daly 58.1%]) — recommend one,
  held constant; the **30.9→79.8% jump** is real but pre/post ⇒ **association not causation** — name RTM,
  **definition drift**, case-mix, secular trend; strengthen with constant definition + case-mix adjustment +
  **ITS/comparison arm** to make it publishable. 11 PubMed. Both are prime R2R candidates and interlock with #5→#6.
  Tiers 1–2 (#1–#7) complete; Tier 3 (#8–#16: Matrix, short-stay, suicide/violence pathways, harm reduction,
  emerging local substances, KPIs) remains. `validate.py` clean.
- **2026-07-14** — Closed **Tier 1** of the addiction-service accreditation research program (same branch),
  filing reports **#3** and **#5** to the **Addiction Psychiatry MOC** (now 5 artifacts) via pubmed-research-note
  → vault-keeper. **#3 AUD relapse-prevention pharmacotherapy (limited adherence support):** naltrexone first
  (once-daily/XR fits low supervision; JAMA 2023 meta 118 trials — NNT to prevent return to any drinking:
  **acamprosate 11, naltrexone 18**; naltrexone NNT 11 for heavy drinking), acamprosate co-first-line (abstinent/
  **hepatic** — renally cleared), **disulfiram ONLY supervised** (Skinner meta: effect appears only in open-label
  trials g 0.70, vanishes when blinded — the anti-goal is the unsupervised default), second-line topiramate/
  gabapentin/**baclofen** (niche = advanced liver disease); Bahji NMA (156 trials) for the comparative RRs. 7
  PubMed + 4 CT.gov (mature field — only mechanistic/formulation trials ongoing). **#5 Methamphetamine use
  disorder pharmacotherapy (usable-now vs wait):** **nothing approved**; **ADAPT-2** combo (XR-naltrexone + ER
  bupropion) the best off-label try-now (Trivedi NEJM n=403, response 13.6% vs 2.5%, **effect 11.1 pp**, NNT ~9,
  reduced-use not abstinence), **mirtazapine** reasonable adjunct (Colfax RR 0.57 / Coffin RR 0.67–0.73; meta RR
  0.81 small — best where insomnia/depression/high-risk behaviour coexist), bupropion marginal (RR 0.90), agonists
  (dexamfetamine/methylphenidate) most-consistent signal but **watch** (regulatory/diversion); **CM is the
  backbone** (Cochrane RR 1.89 continuous abstinence) → hands to report #6. Live frontier = **GLP-1 agonists**
  (semaglutide Phase 2, 2027–2030) + **ketamine** (NIDA CTN-0132, 2026) + extended ADAPT-2 delivery. 8 PubMed + 5
  CT.gov. Tier 1 (#1–#5) complete; Tier 2 (#6 CM, #7 retention — the R2R/publication candidates) and Tier 3 next.
  `validate.py` clean.
- **2026-07-14** — Completed the **pre-meeting trio** of the addiction-service accreditation research program
  (same branch), filing reports **#2** and **#4** to the **Addiction Psychiatry MOC** (now 3 artifacts) via
  the pubmed-research-note → vault-keeper flow. **#2 Methamphetamine-associated psychosis — consult protocol:**
  olanzapine/quetiapine first-line (Chiang Mai NMA, 6 RCTs/395; aripiprazole significantly inferior; Thanyarak
  quetiapine≈haloperidol RCT n=80), lower doses/brisk response, **time-limited not indefinite**; transition to
  schizophrenia **≈22%** (Murrie meta 50 studies/40,783), most within 2–5 y (Alderson), so surveillance is the
  core, not the drug; **LAI reserved on borrowed schizophrenia evidence — no MAP-specific LAI trial exists** and
  none ongoing (honest gap); antipsychotics treat psychosis not use (Kishi null), and the ~76% violence rate ties
  it to the SMI-V layer (report #11). 14 PubMed + 3 CT.gov. **#4 Smoking cessation for a counselling-only public
  clinic:** adding pharmacotherapy ≈**doubles** abstinence (~11%→~20%+); **cytisine first-line for a public system**
  (≈varenicline efficacy, cheaper, fewer AEs — RAUORA Māori RCT 12.1% vs 7.9%; Ofori meta RR 1.13 NS vs varenicline),
  varenicline + combination NRT co-first-line, bupropion reserved; **EAGLES (n=8,144) cleared the neuropsychiatric
  fear** → comorbidity is not a barrier (directly relevant to a psych clinic). Anchored on the Cochrane component
  NMA (319 RCTs/157,179). 8 PubMed; field mature so no CT.gov sweep load-bearing (stated). Sequence 1→2→4 as
  advised; #3, #5, and Tiers 2–3 remain. `validate.py` clean.
- **2026-07-14** — Filed **Alcohol Withdrawal on a District-Hospital Ward — Protocol Choice and Thiamine
  Dosing** to the vault via the pubmed-research-note → vault-keeper flow (branch
  `claude/addiction-protocols-research-sng1gs`). First report of the **addiction-service accreditation
  research program** (a 16-item decision-locked plan; this is Tier-1 #1, "the single most defensible gap").
  Decision was handed over pre-locked, so intent-lock was bypassed (valid opt-out) and the brief named at
  the top. Verdict adjudicates a real trap: symptom-triggered CIWA-Ar dosing is the specialist-unit
  "textbook best" (Holleck meta: duration −60.4 h, BZD −10.5 mg lorazepam-eq) but the same meta rates its
  **general-hospital applicability low** — it presupposes reliable hourly CIWA-Ar scoring a district ward
  lacks. So the recommendation is a **risk-stratified, benzodiazepine-anchored** protocol: PAWSS ≥4 gate
  (validation n=403: sens 93.1%, spec 99.5%; JAMA RCE LR+ 174) → front-loaded long-acting diazepam
  (pharmacokinetic self-taper, monitoring only during the loading window) → **phenobarbital as reserve, not
  first-line** (retrospective series positive but the two ED meta-analyses null: ICU RR 0.92; intubation RR
  0.70 NS — believe the nulls) → **parenteral thiamine before glucose** (100–250 mg/d prophylaxis; 500 mg IV
  TID for suspected Wernicke), the high dose justified by harm-asymmetry not by the one dosing RCT (Dingwall:
  no high-dose benefit, but underpowered). Publication-bias sweep: 14 ongoing AWS trials, **none** re-litigate
  regimen choice or thiamine dosing (all adjuncts/novel — prazosin, CBD, ketones, neurostim), so "wait" is not
  a reason to defer standardisation; Rosenson's phenobarbital RCT (NCT01184417) is published, no hidden
  negative. 21 PubMed + 4 CT.gov trials; confidence moderate-high on the skeleton, moderate on the specific
  regimen (no RCT in a low-resource ward). New **Addiction Psychiatry MOC** (umbrella for the whole program —
  reports #2–#16 to follow) wired into `index.md`; first vault content since the empty-vault drain.
  `validate.py` clean.
- **2026-07-13** — **firecrawl deep-integration wave** (same branch; released firecrawl
  0.2.0, pubmed-research-note 1.6.0, comprehensive-review 0.2.0; catalog → 1.10.0). Wired
  the new plugin into the pipeline in both directions. **Inbound:** firecrawl is now the
  general-web document engine — pubmed-research-note's tool catalog grew from four engines
  to five (regulator labels FDA/EMA/MHRA, guideline full texts NICE/APA/WFSBP, gray
  literature; `firecrawl search` / `firecrawl scrape`, WebFetch fallback, never blocks a
  run) and comprehensive-review gained the same engine in Step 2 + Handoffs; both keep the
  contract *widens where documents come from, never the evidence bar* — fetch-only,
  adjudication stays with the caller, the blog ban stands, scraped sources cite exact URL +
  access date (`<topic> — <URL> (accessed YYYY-MM-DD)` in `## Sources`). **Outbound:**
  firecrawl's Path C deliverables now gate through intent-lock (explicit opt-out only) and
  file to the vault via vault-keeper on explicit request (opt-in like psych-paper-digest);
  clinical-infographic (sourced clinical reports only) and psych-paper-digest (fixed sweep
  engines) explicitly not chained. Firecrawl's description rewritten action-first with the
  handoffs; first 8 evals shipped. A four-way adversarial audit followed (contracts /
  conventions / consistency / regressions — no blockers): the web-document citation format
  was propagated into pubmed's citation-discipline + report-craft (it had only reached the
  engine catalog), "publication year" disambiguated from the access date in both research
  plugins' failure tells, firecrawl's vault bullet gained the HTML/binary→`asset` carve-out,
  and two pre-existing README drifts were fixed (pubmed's stale opt-in vault framing →
  write→show→file default; vault-keeper's "four jobs" → five with the empty row).
  `validate.py` clean; ROUTING.md regenerated.
- **2026-07-13** — Added **firecrawl 0.1.0** (eighth plugin; catalog → 1.9.0, branch
  `claude/firecrawl-docs-5qlw5z`), packaging Firecrawl's official AI-onboarding guide as a
  marketplace skill. Body kept verbatim (install command, CLI/build/workflow skill segments,
  usage paths A–F: live tools, app integration, deliverables, auth, REST-only, keyless
  fallback); two local adaptations only — the frontmatter description gained this
  marketplace's Use-when / Not-for clauses (biomedical literature carved out to the
  PubMed-facing plugins), and the vendor doc's session-specific API-key block was replaced by
  a credentials-hygiene rule (keys live in the environment, never the repo; a key that
  appears in chat is exposed — rotate it). Note: the onboarding doc that seeded this plugin
  arrived carrying a live `fc-…` key; it was NOT committed anywhere and should be rotated.
  `validate.py` clean; ROUTING.md regenerated (8 plugins, 18 components).
- **2026-07-13** — **First empty-vault run — drained the whole vault into the Learn hub** (same
  branch). Ran the new skill end to end: 9 artifacts → 9 Learn topics / **97 atomic notes / 301
  links**, each report handed to learn-hub's `digest-report` skill, distilled, and synced to the
  shared Supabase project `juvoohejxuuvwolmgoep`. Sync integrity was proven, not assumed —
  every note body was **md5-verified byte-exact** (local `md5(content.trim())` vs Postgres
  `md5(body_md)`, 97/97 match) before any deletion. Then the double gate: files were already
  git-committed, and with that satisfied the 9 artifacts, the 2 PPGL infographic assets
  (html+png), and all 7 MOCs were deleted and `index.md` rebuilt to the empty scaffold
  (`.gitkeep` tree kept). Everything remains recoverable from git history. New panic-disorder
  reports (3) grouped under a shared `book: "Panic Disorder"`; the other 6 are standalone topics
  by domain (Psychiatry / Pharmacology / Endocrinology / Neurology). Toolchain notes for next
  time: learn-hub had no `.env.local`/service-role key, so the sync went through the Supabase MCP
  `execute_sql` (per-topic SQL under the ~200 KB ceiling) rather than `npm run sync:apply`; the
  deployed-app cache revalidate was skipped (no `APP_URL`/`REVALIDATE_SECRET` locally) so content
  surfaces within the 1 h safety revalidate.
- **2026-07-13** — **vault-keeper 0.4.0 — the empty-vault skill** (catalog → 1.8.0, branch
  `claude/micky-vault-emptying-skill-2z107h`). New fifth job: **empty** — drain the vault into the
  Learn hub. The skill is a mover/eraser, never an author: it resolves both roots (psych vault per
  Step 0; the learn-hub checkout found or asked for, never guessed), inventories a manifest
  (artifacts / notes / assets / MOCs), hands each artifact to **learn-hub's new `digest-report`
  skill** (created in the learn-hub repo, same branch: distills a report into one Learn topic +
  6–12 atomic notes with deterministic ids + `sources[]` provenance, syncs via sync-vault, verifies
  a provenance-scoped Supabase count — that verification is the deletion handshake), then deletes
  **only** verified files behind a double gate (git-committed + explicit user confirmation), prunes
  MOCs, and rebuilds `index.md` (whole-vault empty → empty scaffold). Supports topic scoping via
  `/empty-vault [topic]`. Ships SKILL.md + command + 6 evals; ROUTING.md regenerated
  (7 plugins, 17 components); `validate.py` clean.
- **2026-07-13** — Filed **Choosing an Antidepressant by Mechanism — a Phenotype-to-Drug Selection Guide** to the
  vault via the pubmed-research-note → vault-keeper flow (branch `claude/antidepressant-pharmacology-research-yoma58`).
  Intent-lock gate ran first: a 3-question picker locked the shape from a topic-shaped 8-item list (serotonin receptor
  map → SSRI transporter comparison → dose–occupancy/adaptation → activation/akathisia/blunting → PK-vs-PD → α₂δ
  pharmacology → misuse/withdrawal → clinical selection). User chose **selection instrument** (item 8's phenotype→drug
  framework is the verdict; items 1–7 are the mechanistic argument beneath it — not an atlas, not 8 notes), **full
  antidepressant spectrum + α₂δ ligands**, **clinician self-study** register. Active prior #1 fired (don't collapse a
  broad "research" list) — here the risk was the opposite, an item-by-item receptor encyclopedia, so the picker forced
  the culminating decision to lead. The spine adjudicates a real tension: efficacy is a class near-tie (Cipriani 21-drug
  NMA, OR 1.37–2.13 vs placebo, head-to-head diffs only 1.15–1.55) and PET shows why (SERT ~80% occupancy at the min
  effective dose; high dose → ~85% but only more dropout), so **selection belongs to mechanism/tolerability/PK matched
  to phenotype, not efficacy ranking**. Cashes out to: receptor fingerprint → side-effect forecast; half-life → the
  discontinuation you choose at the start (Henssler 2024: ~15% attributable, ~1 in 6–7, severe 2.8%; short-t½
  paroxetine/venlafaxine worst; hyperbolic taper per Horowitz); emotional blunting ~46% and partly residual depression
  (Goodwin); α₂δ ligands as the non-monoamine anxiety option (Slee GAD NMA pregabalin −2.79 HAM-A; Taylor α₂δ-1
  mechanism) capped hard by dependence (Evoy: 1.6% general vs 3–68% opioid-user misuse). **17 PubMed + 3 CT.gov trials**
  (hyperbolic-vs-linear taper NCT07393919 2027; deprescribing NCT07398053; pharmacogenomic-guided NCT06729541 2026).
  New **Antidepressant Pharmacology MOC** (seventh MOC) — first drug-side, cross-disorder pharmacology MOC — wired into
  `index.md` and cross-linked to Depression — Treatment. Confidence moderate-high on the spine, moderate on the specific
  phenotype mappings. `validate.py` clean.
- **2026-07-13** — Filed **Tension-Type Headache and Migraine — Comprehensive Review** to the vault via
  the comprehensive-review → vault-keeper flow (branch `claude/tension-migraine-review-ep6xs5`). Intent-lock
  gate ran first (active prior #1 fired on "review"): a 3-question picker locked **one combined review** (both
  disorders through a single ten-section arc, compared section by section — not two separate reviews),
  **balanced emphasis** (equal depth, no section favored), and **clinician self-study** register. First
  **neurology** topic in the vault and first **combined two-disorder** review; new **Primary Headache Disorders
  MOC** (sixth MOC) wired into `index.md`. The chapter's spine is the prevalence/disability inversion + the
  research-attention asymmetry: TTH is far more prevalent (GBD 2016: **1.89 billion** vs migraine's 1.04 billion)
  but migraine owns the disability (**45.1M vs 7.2M YLDs**; #1 disabler in women 15–49) and the entire
  therapeutic revolution — the 137-RCT acute NMA (triptans still first-line; gepants/ditans for cardiovascular
  risk), best-in-class CGRP-antibody prevention (74-trial NMA), onabotulinumtoxinA for chronic migraine, and a
  novel post-CGRP target (anti-PACAP **Lu AG09222**, n=874) — while TTH has only amitriptyline and "little
  progress since the early 2000s," a gap the registry confirms (migraine pipeline = drugs, TTH pipeline =
  physiotherapy). MOH treated as the shared secondary complication; stroke comorbidity OR 2.04; CHAMP pediatric
  futility (52/55/61%). **30 PubMed sources + 5 CT.gov trials**, all 10 arc sections present. `validate.py` clean.
- **2026-07-12** — **Interconnect + conflict-resolution wave** (7-plugin review; released pubmed
  1.5.1, vault-keeper 0.3.0, clinical-infographic 0.2.1; catalog → 1.7.0). Fixed the asymmetric
  "review X" routing: pubmed-research-note's NOT-for now carves out whole-disorder reviews to
  comprehensive-review (the IED-collapse gap, closed at the description layer). Unified the
  asset handoff contract: vault-keeper gained an `asset` target type (binary → `assets/`, wired
  into the topic MOC's `## Assets` section; companion note optional) and clinical-infographic
  now hands over exactly that payload. Codified the canonical MOC section vocabulary
  (`## Artifacts / ## Assets / ## Notes`) in vault-layout.md and normalized the Panic Disorder
  MOC to it. Also: artifact titles clarified as human titles (kebab filename is vault-keeper's),
  clinical-infographic got its first evals, the stray root-level adjunctive-treatment duplicate
  was removed, README refreshed to 7 plugins, CLAUDE.md notes digest vault saves are opt-in.
  Left by design: triple MCP wiring (self-contained plugins), stale `frame:` frontmatter in old
  artifacts (historical records), no validate.py cross-ref linter (false-positive risk).
- **2026-07-12** — First run of **comprehensive-review** end-to-end: filed **CBT for Panic Disorder —
  Comprehensive Review** (same branch), the third artifact under the **Panic Disorder MOC** (now split
  into Decision reports + Reviews). Ledger prior #1 fired on "review" — intent-lock round confirmed the
  user wanted the **comprehensive academic review**, not another decision report (emphasis: components &
  mechanism + who-responds/relapse). Adapted the disorder-arc to a treatment-modality arc (model →
  components → efficacy → formats → mechanism → predictors → durability → limitations → controversies).
  Key numbers: Pompoli component NMA (interoceptive exposure + face-to-face = active ingredients;
  relaxation/VR *lower* efficacy; best-vs-worst remission OR 7.69), efficacy g 0.5–1.0 (JAMA 2025 unified
  meta, 375 trials), predictors (agoraphobic avoidance most consistent, Cluster C; 5-HTTLPR null), and the
  honest weak point — CBT panic gains hold to ~12 months but are **not significant beyond 12 months**
  (van Dis). 23 PubMed + 5 CT.gov trials. `validate.py` clean.
- **2026-07-12** — Filed a second panic report, **Panic disorder — novel & emerging treatments (try-now vs
  watch)**, to the vault (same branch), extending the **Panic Disorder MOC** to two artifacts. Follow-up
  to the pharmacology report; intent-lock picker hit a transport error so proceeded on a declared broad
  reading (all modalities; actionable-first then horizon). Verdict: **watch, don't prescribe** — for panic
  *specifically*, nothing novel is prescribable now except better-delivered CBT (digital/VR: VRET g≈0.90,
  guided iCBT ≈ face-to-face). The novelty gradient is **inverted from the hype**: psychedelics
  (psilocybin g −1.49; MM120/LSD −5 to −6 HAM-A points) + ketamine are aimed at GAD/depression/PTSD, not
  panic; rTMS **null in panic** (SMD 1.19, P=.054) though positive in GAD; D-cycloserine near-null (Cochrane
  RR 1.10) and cannabidiol negative in refractory panic. CT.gov: ~35 active panic trials, almost all
  psychotherapy-delivery — no ongoing panic-specific psychedelic/ketamine trial. 12 PubMed + 6 CT.gov
  trials. `validate.py` clean.
- **2026-07-12** — Filed **Panic disorder — pharmacological management** decision report to the vault
  via the pubmed-research-note → vault-keeper flow (branch `claude/panic-disorder-pharmacology-mw7hqv`).
  Intent-lock gate ran first (active prior #1 fired): a 2-question round locked the *whole
  pharmacological algorithm* for an uncomplicated adult outpatient (not first-line-only, not a
  whole-disorder review). The verdict adjudicates a real tension — the Cochrane 2023 NMA (70 RCTs)
  ranks benzodiazepines/TCAs above SSRIs on *acute* response and dropout, but the BMJ 2022 NMA
  (87 RCTs, 12,800) remission-vs-adverse-event cluster puts **SSRIs (sertraline/escitalopram)** as
  the best tradeoff; report believes the tradeoff over the raw ranking (BDZ evidence low-quality,
  "acceptability" = acute-trial dropout that misses dependence/mortality). Rests on 15 PubMed sources
  + 1 CT.gov trial: benzo-as-bridge-only, continue 6–12 months then **slow taper + psychological
  support** (Batelaan 2017: relapse OR 3.11, 36.4% vs 16.4%; Lancet Psychiatry 2026 deprescribing NMA:
  taper-alone no better than abrupt), switch-not-augment on failure (augmentation meta RR 1.08 NS).
  Field is mature/quiet — only ongoing trial is NCT05737511 (hydroxyzine vs escitalopram, n≈80, 2026).
  New **Panic Disorder MOC** (fifth MOC) wired into `index.md`. `validate.py` clean.
- **2026-07-11** — **clinical-infographic 0.2.0 — visual-first upgrade** (same PPGL branch),
  driven by feedback that the first render was text-heavy. Design system gains a **diagram
  grammar** (name a *signature visual* before the columns; journey/timeline curve, mechanism
  strip, decision-flow, escalation ladder, paired-opposite split) with commented scaffolds in
  the template; a **schematic-fidelity rule** (illustrative figures must be labelled, sourced-
  numbers-only, no fake axis) in the source contract; a **render-&-verify** Step 2.5 (rasterise
  + eyeball + optional OCR before filing; PNG is a named deliverable); and an `examples/` dir
  holding a worked **dense reference infographic** (the PPGL one). Rationale kept in
  `references/lessons-learned.md`. The PPGL infographic itself gained a mechanism strip, a
  haemodynamic-journey curve, a which-α-blocker decision-flow, and an escalation ladder (rung
  arrows corrected to point down-flow). Bumped via `scripts/bump.py`; validate + route clean.
- **2026-07-11** — First real run of the **research → infographic** pipeline end-to-end (branch
  `claude/ppgl-perioperative-infographic-2ghpcr`): filed a sourced **Perioperative Management of
  PPGL** decision report to the vault and rendered it into a **clinical-infographic** asset — the
  exact PPGL perioperative reference that motivated building the plugin. Report (`pubmed-research-note`
  style, opt-out/autonomous, phase-structured Pre-op → Intra-op → Post-op) rests on 15 PubMed sources
  + 4 CT.gov trials: Endocrine Society guideline (all functional PPGL blocked pre-op), the **PRESCRIPT
  RCT** settling phenoxybenzamine vs doxazosin to "either" (time outside BP target 11.1% vs 12.2%,
  P=.75), selective-vs-nonselective series, PHEO-RISK complications, and the contraindicated-drugs
  literature; forward-looking flag = **NCT05702944** (live RCT testing whether normotensive tumours can
  skip α-blockade, readout 2027). Fidelity contract held: sodium-nitroprusside, "Roizen criteria", and
  glucagon-as-crisis-trigger were deliberately **excluded** as untraceable to the retrieved sources.
  Deliverables: `vault/artifacts/ppgl-perioperative-management.md`,
  `vault/assets/ppgl-perioperative-management-infographic.html` (self-contained, print-ready, AA), new
  `Pheochromocytoma & Paraganglioma MOC` (fourth MOC) wired into `index.md`. `validate.py` clean.
- **2026-07-11** — Added **clinical-infographic 0.1.0** (seventh plugin; catalog → 1.6.0), built
  via the plugin-creator flow. It is the visual **last mile** of the research pipeline: renders a
  SOURCED comprehensive-review / pubmed-research-note report into a professional medical summary
  infographic for clinical reference — one **self-contained** HTML file (inline styles + inline
  SVG icons, zero external CSS/JS/fonts/images; opens offline, prints identically) with
  color-coded phase/theme columns, stat tiles, and a mandatory `CRITICAL SAFETY — MEDICATIONS /
  ACTIONS TO AVOID` banner modelled on the reference standard. Deliberately **ships no search
  engines** — the guardrail against a confident-but-fabricated panel: it resolves a source in
  order (this session → vault artifact via vault-keeper → generate with the two research plugins,
  never author facts itself) and enforces a fidelity contract (nothing untraceable to the source,
  numbers keep units + qualifiers, contraindications always reach the safety banner, `[unverified]`
  never rendered as fact). Files the HTML as an **asset** via vault-keeper, wired into the source
  report's MOC. Ships the `clinical-infographic` skill, `/infographic [topic-or-source]`, and three
  references (source-contract, design-system, fillable infographic-template.html). `route.py`
  regenerated (7 plugins, 15 components); validate clean. Prompted by a request for a PPGL
  perioperative-management reference infographic (NotebookLM-style) — the plugin generalises that
  into a repeatable, source-locked renderer.
- **2026-07-11** — Filed **Adjustment Disorder** comprehensive review to the vault via the
  comprehensive-review → vault-keeper flow (branch `claude/adjustment-disorder-vault-1xg0lo`).
  Intent-lock gate ran first (misread prior #1 fired): locked clinician self-study register +
  treatment/management emphasis, full ten-section arc preserved. Deliverable centres on the DSM-5-TR
  (residual) vs ICD-11 (stress-response syndrome) reconceptualisation and the thin treatment base
  (etifoxine, plant extracts, digital self-help; psychotherapy first-line; foregrounded suicide
  risk). 30 PubMed sources + 3 registry trials (psilocybin, work-CBT, US-military ADNM). New
  `Adjustment Disorder MOC` wired into `index.md` (third MOC alongside Depression, IED). One
  `[unverified]` gap flagged: no dedicated AjD-specific suicide-mortality register study located.
- **2026-07-11** — pubmed-research-note **1.5.0**: **deleted the four fixed frames and the
  fixed report template**, the skill's two most rigid structures. Rx / Service / Truth /
  Teaching are replaced by a bespoke **decision brief** built fresh per request from a shared
  six-slot anatomy (decision · verdict's shape · what settles it · what's counted · mandatory
  checks · anti-goal) — `references/decision-frames.md` → new `references/decision-brief.md`.
  The five-heading report skeleton is replaced by report-craft *principles*
  (`references/report-craft.md`): answer first, headings from the decision not the topic,
  numbers everywhere, adjudicate don't list, as long as the decision needs. The old hard
  "Failure conditions" + forbidden-headings ban became motivated *tells of drift* toward the
  encyclopedia — guidance, not enforcement (Micky's explicit call: delete the frames entirely,
  loosen invariants to principles). De-framed `intent-lock-pairing.md` (four what-the-user-wants
  slots, not "the frame") and `tool-catalog.md` (engine mandates tied to the decision at stake,
  not named frames); rewrote all 16 evals to test brief-building + verdict-first + decision-shaped
  headings + adjudication. `route.py` regenerated; validate clean.
- **2026-07-11** — Added **comprehensive-review 0.1.0** (sixth plugin; catalog → 1.5.0), built via
  the plugin-creator flow with an intent-lock interview up front. Closes the gap the IED misread
  exposed: "comprehensive review" is now a first-class deliverable, not a frame pubmed-research-note
  must be talked into. Locked in the interview: whole-disorder textbook-chapter reviews, own
  PubMed + CT.gov pipeline (pubmed-research-note stays the decision tool), output is an md file
  kept in the vault via vault-keeper. Skill + `/comprehensive-review [topic]`; ROUTING.md
  regenerated (6 plugins, 13 components).
- **2026-07-11** — pubmed-research-note **1.4.0**: intent-lock is now a **mandatory Step 0 gate**
  before any search (was conditional — only fired on bare topics, frame-ties, or expensive runs).
  The frame now *falls out of the interview* instead of being inferred; the only bypass is an
  explicit opt-out ("just search" / "don't interview me"), which must be the user's own words —
  an opt-out may never be inferred from an ordinary "research this and file it." Prompted by an
  IED report that silently collapsed a "comprehensive review" request into an Rx-only decision.
  Rewrote Step 0, the intent-lock pairing section + trigger table (`references/intent-lock-pairing.md`),
  and the failure conditions; logged the misread to the intent-lock ledger as a new active prior.
  `route.py` regenerated. Then re-ran the IED vault artifact *through* the new gate: intent-lock
  locked an academic, whole-disorder frame, so the Rx-only artifact was replaced by a comprehensive
  academic review (`intermittent-explosive-disorder-review`) and its MOC promoted to a whole-disorder
  `Intermittent Explosive Disorder MOC`.
- **2026-07-10** — pubmed-research-note **1.3.0**: output is now a three-step default
  pipeline — write the md report, render it inline in the chat, then file it to the vault as
  an artifact via vault-keeper (was working-directory only, vault opt-in). Atomic-note
  distillation stays word-gated on "atomize"; failure conditions, Close, manifest + SKILL
  descriptions and ROUTING.md updated to match. First real report — the difficult-to-treat-
  depression Rx note — filed to the vault under a new `Depression — Treatment MOC`.
- **2026-07-10** — Added **psych-paper-digest 0.1.0** (fifth plugin; catalog → 1.4.0), built
  via the plugin-creator flow from a profile-based brainstorm. Fills the temporal gap next to
  pubmed-research-note: pull-based decision research vs scheduled watchlist surveillance —
  the carve-out named in pubmed's description since 1.2.0 now resolves to a real plugin.
- **2026-07-10** — Full four-plugin audit produced an 11-task improvement plan
  (`docs/superpowers/plans/2026-07-10-improve-all-plugins.md`), EXECUTED same day (branch
  `improve-all-plugins`, 22 commits). Fixed: intent-lock misread-ledger path collision,
  pubmed sandbox-only paths + vault-logic duplication (now delegates to vault-keeper via a
  producer→vault-keeper handoff), `route.py` routing on first sentence not Use-when, validator
  gaps. Released pubmed 1.2.0, intent-lock 0.4.0, plugin-creator 0.3.0, vault-keeper 0.2.0,
  catalog 1.3.0. `validate.py` now also checks per-skill evals + command/agent frontmatter
  descriptions. Merged to `master` (`57e470e`).

## Machine toolchain — audited 2026-07-12

All plugin/skill dependencies on this machine are satisfied; don't re-audit or suggest installing these.

- **CLIs:** python 3.14, node 24, npm, pnpm, git, gh, pandoc, mermaid-cli (`mmdc`), rg, curl, jq 1.8.2, rtk, firebase-tools, vercel, firecrawl-cli, poppler 26.02.0 (`pdftoppm`, `pdftotext`, `pdfinfo`, …).
- **Poppler location:** `C:\Users\User\Desktop\My skill\tools\poppler-26.02.0\Library\bin`, on user PATH.
- **Python packages:** yfinance, pandas, numpy, matplotlib 3.11, openpyxl, python-docx, python-pptx, pypdf, PyMuPDF, Pillow, weasyprint, reportlab, svglib, pdfplumber, curl_cffi, requests, bs4, lxml, httpx, yaml.
- **Deliberately skipped** (install only when a use case appears): LibreOffice, ffmpeg, ImageMagick, playwright, cairosvg, edge-tts, uv, feedparser.

## Open threads

- Local branch `improve-all-plugins` still present — delete once its merge into `master` is confirmed.

## Health check

- `python3 scripts/validate.py` → must print `all checks passed`.
- `python3 scripts/route.py` → regenerates `ROUTING.md` (never hand-edit the router).
