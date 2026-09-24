#!/usr/bin/env bash
# Synthetic source report for the render. Every fact is taken from the plugin's own sourced
# example (examples/ppgl-perioperative-management.html); the [unverified] tag on the
# hypotension rate is the fixture's planted gap.
set -euo pipefail
cat > review.md <<'EOF'
# Perioperative management of pheochromocytoma and paraganglioma (PPGL): how should an adult be prepared for elective resection?
*2026-07-11 · PubMed 15 · trials 4 · books 0*

**Verdict: alpha-blockade first for every functional PPGL, titrated over about 7–14 days to a seated BP <130/80 mmHg and HR 60–70 bpm, with sodium and fluid loading; a beta-blocker only after alpha-blockade.** Confidence: moderate-high — the preparation schedule rests on guideline consensus and one RCT comparing agents, not on trials against no preparation.

## Absolute contraindications

1. **Never start a beta-blocker before alpha-blockade.** Unopposed alpha-stimulation precipitates a hypertensive crisis.
2. **Never give metoclopramide or another dopamine-receptor antagonist to a patient with a functional PPGL.** Dopamine antagonists precipitate a catecholamine crisis.

## Pre-operative preparation (about 7–14 days)

- Alpha-blockade for all functional PPGL, started 2–3 weeks before surgery and titrated to BP: phenoxybenzamine 10 mg twice daily, titrated towards 1 mg/kg/day, or doxazosin 2 mg/day, titrated to at most 32 mg/day. Target: seated BP <130/80 mmHg, HR 60–70 bpm, standing BP no lower than 80/45 mmHg.
- The PRESCRIPT RCT (n=134) found either agent acceptable: time outside the BP target 11.1% with phenoxybenzamine vs 12.2% with doxazosin (P=.75); 30-day cardiovascular complications 8.8% vs 6.9%.
- Beta-blocker only after at least 3–4 days of alpha-blockade, and only if HR >100 bpm: propranolol 20 mg three times daily, or atenolol 25 mg/day titrated to 50 mg/day.
- Volume loading throughout: sodium 5000 mg/day plus fluids 2.5 L/day.

## Intra-operative

- Surge on tumour manipulation (SBP >160 mmHg): phentolamine 5 mg IV bolus, repeated as needed, or nicardipine 5 mg/h titrated to at most 15 mg/h.
- Crash after venous ligation (MAP <60 mmHg): IV isotonic fluid first, then norepinephrine, or vasopressin 0.03–0.04 units/min for catecholamine-resistant vasoplegia.

## Post-operative (24–48 h)

- Rebound hypoglycaemia, typically within the first 4 hours: check glucose every 6 h for at least 24 h; IV 5% dextrose until oral intake.
- Prolonged post-operative hypotension occurs in roughly 10% of patients [unverified].

## Sources

- Endocrine Society guideline, blockade for all functional PPGL — [doi:10.1210/jc.2014-1498](https://doi.org/10.1210/jc.2014-1498)
- PRESCRIPT RCT, phenoxybenzamine vs doxazosin (n=134) — [doi:10.1210/clinem/dgz188](https://doi.org/10.1210/clinem/dgz188)
- Postoperative management, hypotension and hypoglycaemia — [doi:10.3390/cancers11070936](https://doi.org/10.3390/cancers11070936)
- Drugs precipitating catecholamine crisis — [doi:10.1089/jpm.2022.0402](https://doi.org/10.1089/jpm.2022.0402)
- NCT01379898 — PRESCRIPT, completed, n=134
EOF
