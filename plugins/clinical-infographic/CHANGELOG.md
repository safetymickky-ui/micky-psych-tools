# Changelog

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
