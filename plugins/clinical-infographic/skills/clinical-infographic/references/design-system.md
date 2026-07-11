# The design system — the visual grammar of a clinical reference

How a sourced report becomes a page a clinician trusts at a glance. Read this before laying
anything out; fill [infographic-template.html](infographic-template.html) rather than starting
from a blank file.

## The anatomy

A clinical reference infographic has a fixed grammar. Not every part is always present, but
their order and role are:

1. **Masthead** — the topic/decision as a bold title, one subtitle line naming scope,
   population, or guideline basis.
2. **Columns (2–4)** — the spine. Each is a **clinical phase** (Pre-op / Intra-op / Post-op),
   a **theme** (Diagnosis / Treatment / Monitoring), or a **decision's steps**. Each column has
   a colored header chip (icon + label + optional time/scope badge), a background tint, and a
   stack of cards.
3. **Cards** — the directives. Three kinds:
   - **Directive card** — a bold heading + a concise instruction that keeps its numbers and
     qualifiers.
   - **Rule callout** — a highlighted card (left accent bar + ⚠) for a load-bearing rule
     ("Alpha before beta", "Start 7–14 days pre-op").
   - **Stat-tile row** — targets / doses / thresholds rendered as compact figure tiles.
4. **Critical-safety banner** — a full-width, high-contrast band below the columns for
   contraindications and "medications / actions to avoid". **Mandatory when the source has such
   content.** This is the signature element that separates a *clinical reference* from a poster.
5. **Footer** — provenance (source title, render date, counts), a collapsed Sources list, and
   the standing disclaimer line.

## Columns — the color model

Use **2–4** columns; more than four stops being scannable. Each column gets one accent family,
applied to its header chip and (as a tint) its body. A documented, print-safe, AA-contrast
starting palette (swap per topic, keep the contrast):

| Slot | Accent | Tint | Typical role |
|---|---|---|---|
| c1 | deep blue `#3b6ea8` | `#eef3f9` | first phase / diagnosis |
| c2 | green `#3f8a6e` | `#edf5f1` | middle phase / treatment |
| c3 | amber-brown `#c9772e` | `#fbf1e7` | late phase / monitoring |
| safety | crimson `#a4304a` | `#f7e9ed` | the do-not band |

Colour is **decoration, never the message**: every column is also named in its header, every
rule also carries ⚠, every prohibition also carries 🚫 or a ban icon. A reader in greyscale (a
photocopy, colour-blindness) must lose nothing.

## Stat tiles — numbers as figures

Promote the source's key figures into tiles: a big value with its unit, a small label under it.
`<130/80 mmHg` / "seated BP". `60–70` / "HR bpm". `7–14 d` / "pre-op". Tiles are for figures
that are **already in the report** — never a figure you inferred to fill a row.

## The critical-safety banner

Model it on the reference standard: a full-width band, crimson header reading **CRITICAL
SAFETY — MEDICATIONS / ACTIONS TO AVOID**, prohibition iconography, and 1–4 cells each naming
a contraindication group and *why*. Drug names stay verbatim. This band is the last thing cut
from a crowded page, never the first — if space is tight, shrink a column, not the safety.

Include it whenever the source names any contraindication, black-box warning, or "do not use /
avoid" item. Omit it only when the source genuinely has none — and say so in the Close.

## Self-contained HTML — non-negotiable

A clinical reference must open on a locked-down hospital machine and print identically. So:

- **One file.** Inline `<style>`; no external `.css`.
- **No network.** No CDN, no web fonts, no remote images, no external JS. Use a **system font
  stack** and **inline SVG** icons (a `<symbol>` sprite at the bottom of the file, referenced
  with `<use href="#...">`). Emoji (⚠ 🚫 💊) are an acceptable self-contained fallback.
- **Works offline, forever.** Nothing on the page may depend on a request succeeding.

## Print & page

- Target **A4 / Letter**. Set `print-color-adjust: exact` so tints and the safety band survive
  printing. Use `break-inside: avoid` on columns, cards, and the safety band so nothing splits
  across a page. Set a sensible `@page { margin }`.
- **Formats:** *wall poster* (larger type, one page), *A4 handout* (default), *pocket card*
  (denser, two-up). Default to A4 handout unless the user asked otherwise.

## Accessibility

- **Contrast:** body text and every colored chip meet **WCAG AA** (4.5:1 text, 3:1 large).
- **Not by colour alone:** pair every colour with a label or icon (see the color model).
- **Semantics:** real headings (`h1`/`h3`), `lang` set, columns as `<article>`/`<section>` with
  `aria-label`; decorative SVGs `aria-hidden`, informative ones labelled.
- **Legible minimums:** no clinical text below ~12px at print size.

## Fidelity rules restated (they live here too)

- Numbers keep units and qualifiers; ranges stay ranges.
- Nothing on the page that is not in the source report.
- Contraindications always reach the safety banner.
- `[unverified]` is never rendered as a fact.

The full rationale is in [source-contract.md](source-contract.md).
