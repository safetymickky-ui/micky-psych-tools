# Changelog

## 0.2.2 — 2026-07-16
**Light-locked.** Removed the `@media (prefers-color-scheme:dark)` block from the template and
the ppgl example, and pinned `:root { color-scheme:light }`. Infographics are print-ready paper
rendered on a white surface in the Learn hub; a partial dark override stranded ink-on-tint rows
and hardcoded SVG colours as invisible text under an OS dark theme (and can't be overridden from
inside the app's sandboxed iframe). New **"Light-locked — no dark mode, ever"** rule in
design-system.md. This is the source-side fix for the light-lock normalisation that learn-hub's
`ingest-infographic` skill was having to apply on the way in.

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
