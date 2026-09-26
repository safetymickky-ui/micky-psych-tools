# Examples — worked outputs of `clinical-infographic`

Reference renders that show the skill's grammar in practice. Open the `.html` in any browser
(it is fully self-contained — no network needed); the `.preview.png` is a static preview.

## `ppgl-perioperative-management.html` — a **dense reference infographic**

*Perioperative Management of Pheochromocytoma & Sympathetic Paraganglioma (PPGL)*, rendered
from the sourced report `vault/artifacts/ppgl-perioperative-management.md` (PubMed 15 · trials 4).

This is the **dense reference** end of the format range — a maximal clinical reference that
packs the whole protocol onto one screen-width sheet. On paper it prints on **3 A4 pages**
with its three columns intact (the content is about 2.1 A4 pages tall; measured 2026-09-26).
It is a screen / wall reference, not a one-page handout: for a brief that must fit one A4
page, dial *down* (fewer diagrams, a shorter drug list, a pocket card) and check the page count
in Step 2.5.

What it demonstrates from the [diagram grammar](../skills/clinical-infographic/references/design-system.md):

- **Signature journey curve** — a schematic arterial-BP trace across the perioperative course
  (titrated into the target band → surges above SBP 160 on manipulation → crash below MAP 60 at
  ligation → low recovery), with phase bands, threshold lines, and event markers. Labelled
  *illustrative — not measured data*; the only hard numbers on it are the sourced thresholds.
- **Mechanism strip** — the causal "why": tumour → catecholamines → α/β effects → block α first.
- **Decision-flow** — choosing the α-blocker (phenoxybenzamine vs doxazosin) with the indication
  and trade-off for each, and the PRESCRIPT RCT verdict beneath.
- **Escalation ladder** — numbered tiers (α → +β → +CCB/metyrosine) with the condition on each
  downward rung, a "never β before α" ban, and a volume-load foundation.
- **Paired-opposite split** — the intra-op surge ▲ vs crash ▼.
- **Stat tiles**, and the mandatory **critical-safety banner** ("medications / actions to avoid").
- **Fidelity + accessibility** — every figure traceable to the source; schematic labelled;
  SVG `role="img"`/`<title>`/`<desc>`; nothing conveyed by colour or an arrow glyph alone.

Every fact traces to the source report's `## Sources` block; the infographic never adds a
clinical claim of its own.
