# clinical-infographic

Turns a **sourced** clinical evidence report into a **professional medical summary infographic
for clinical reference** — a single self-contained HTML file with color-coded phase/theme
columns, stat tiles, and a critical-safety banner, that opens offline and prints clean.

It is the **last mile** of the research pipeline, not a shortcut around it. This plugin ships
no search engines on purpose: it never invents a clinical fact. Every mark on the page traces
back to a `comprehensive-review` or `pubmed-research-note` report.

## Renderer, not researcher

| | comprehensive-review / pubmed-research-note | clinical-infographic |
|---|---|---|
| Owns | sourced content + citations | the visual layout of that content |
| Searches? | yes — that is its job | **never** |
| Adjudicates? | yes | **never** — it shows the verdict, it does not issue one |
| Output | an md report/review | a self-contained HTML infographic |

## The deep integration (Step 0)

The skill resolves a source before it renders anything, in order:

1. **This session's report** — one you just produced or pasted.
2. **An existing vault artifact** — found via `vault-keeper` query.
3. **None exists → generate it first, never fabricate:**
   - whole-topic reference → run **comprehensive-review**, then render its chapter;
   - one decision / protocol → run **pubmed-research-note**, then render its verdict + working.

Those plugins own their intent-lock gate, their searches, and their citation discipline. The
infographic only *lays out* what they sourced.

## The fidelity contract

An infographic is trusted precisely because it is compact — so the failure it must never make
is a confident panel the evidence never supported. The rules (full text in
`skills/clinical-infographic/references/source-contract.md`):

- **Nothing on the page that is not in the source report** — no new drugs, doses, or numbers.
- **Numbers keep units and qualifiers** — `<130/80 mmHg`, not `low`; "only after alpha-blockade"
  is never trimmed off.
- **Contraindications always reach the safety banner** — the last thing cut, never the first.
- **`[unverified]` never renders as fact.**

## The output

A single `.html` file — inline styles, inline SVG icons, **no external CSS/JS/fonts/images** —
so it opens on a locked-down machine and prints identically. Color-coded columns, figure tiles,
a mandatory `CRITICAL SAFETY — MEDICATIONS / ACTIONS TO AVOID` band when the source carries
contraindications, and a footer with provenance, a collapsed Sources list, and the standing
"not a substitute for clinical judgment" disclaimer. WCAG-AA contrast; color is never the only
signal. The design grammar lives in `skills/clinical-infographic/references/design-system.md`;
the fillable skeleton is `references/infographic-template.html`.

## Where it lands

The HTML is a rendered **asset**: `vault-keeper` files it into `vault/assets/` and wires it into
the **source report's MOC** under its `## Assets` section (a short companion note is optional),
so the infographic hangs off the same map as its evidence. This plugin never resolves a vault
path itself.

## Use it

```
/infographic perioperative management of pheochromocytoma
/infographic the review above
```

Or just ask: "make a clinical reference infographic of X", "turn this review into an
infographic", "one-page visual summary".

## Install

```
/plugin marketplace add <owner>/micky-psych-tools
/plugin install clinical-infographic@micky-psych-tools
```

Local development:

```
/plugin marketplace add .
/plugin install clinical-infographic@micky-psych-tools
```
