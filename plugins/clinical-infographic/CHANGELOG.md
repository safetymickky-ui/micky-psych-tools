# Changelog

## 0.3.0 — 2026-09-26

Quality pass on measured defects (two probes passed a 100% number trace yet altered 6 and 11
claims; `µg` could render as `ΜG`; the example printed as one stacked column on 3 pages; the
banner keyed on the word "avoid"). Details: `docs/quality-pass/`.

- **Step 2.6 fidelity check** — `scripts/verify-infographic.mjs` (numbers, units, design
  labels, template residue, `[unverified]` gaps; with `--render`: unit case, print stacking,
  A4 page count, network) plus a claim ledger for qualifiers; blocks filing on an altered or
  untraceable claim.
- **Safety band by clinical class** — 🚫 contraindication / boxed warning, ⚠ warning /
  interaction / serious harm, ⏱ monitoring, each with the source's verb and reason; "no
  benefit shown" goes to a neutral panel; a coverage line is always shown; the generate
  handoff sends a render brief instead of "brevity welcome".
- **Print** — breakpoints scoped to `@media screen`, `@page { size:A4 }`, break-inside on
  cards not columns; Step 2.5 renders the A4 PDF and counts pages. The example keeps its
  three columns on paper (3 A4 pages; its README no longer says single-sheet).
- **Units keep their case** — no `text-transform` on labels that hold numbers, units or drug
  names; write `mcg`.
- **Rewrite step S06-W1-1 done ahead of wave** — light-lock (dark block removed,
  `color-scheme:light`), AA column accents (`#3b8368`, `#aa6527`), 12px floor, mobile
  mechanism strip. Template comment leak fixed.
- **Evals** — the output case writes `ppgl-infographic.html` and grades it at a literal path
  (the glob paths failed every run); new grader: the fidelity script ran.

## 0.2.1

no contemporaneous entry; see `git log` around this version.

## 0.2.0 — 2026-07-11

**Visual-first.** After the first real run rendered a text-heavy first pass, the defaults now
lean on diagrams. New **diagram grammar** in the design system — a *signature visual* named
before the columns, plus a journey/timeline curve, mechanism strip, decision-flow, escalation
ladder, and paired-opposite split — with matching commented, copy-ready scaffolds in the
template so a diagram is reached for before a prose card.

**Schematic fidelity.** New rule (in the source contract and design system): any illustrative
figure must be labelled *illustrative — not measured data*, carry only sourced numbers, and
never use a fabricated axis. Diagram accessibility spelled out (SVG `role="img"`/`<title>`/
`<desc>`, logical DOM order, never arrow-glyph-only).

**Render & verify.** New Step 2.5 — rasterise the HTML, eyeball the layout (and optionally OCR
it) before filing; the PNG render is now a named deliverable.

**Examples.** Added `examples/` with a worked **dense reference infographic** (PPGL perioperative
management) — HTML + preview — demonstrating every diagram type.

Rationale captured in `references/lessons-learned.md`.

## 0.1.0 — 2026-07-11

Initial release. Renders a **sourced** clinical evidence report into a professional medical
summary infographic for clinical reference — a single self-contained HTML file (inline styles
+ inline SVG icons, no external CSS/JS/fonts/images) with color-coded phase/theme columns, stat
tiles, a mandatory `CRITICAL SAFETY — MEDICATIONS / ACTIONS TO AVOID` banner when the source
carries contraindications, and a provenance/Sources/disclaimer footer. WCAG-AA contrast; color
is never the only signal; prints identically offline.

A **rendering layer, not a research tool** — ships no search engines by design. Deep-integrates
with `comprehensive-review` and `pubmed-research-note`: it resolves a source in order (this
session's report → an existing vault artifact via `vault-keeper` → generate one with those
plugins) and **never fabricates a clinical fact**. Fidelity contract enforced: nothing on the
page that is not traceable to the source, numbers keep units and qualifiers, contraindications
always reach the safety banner, `[unverified]` never renders as fact. Files the HTML as an
**asset** via `vault-keeper`, wired into the source report's MOC. Ships the `clinical-infographic`
skill, the `/infographic [topic-or-source]` command, and three references (source contract,
design system, fillable HTML template).
