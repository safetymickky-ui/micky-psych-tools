---
name: clinical-infographic
description: >-
  Renders a professional, print-ready medical summary infographic (a self-contained HTML file)
  for clinical reference from a SOURCED evidence report. Use when the user says "make an
  infographic", "medical summary infographic", "clinical reference infographic", "turn this
  review/report into an infographic", "one-page visual summary", "สรุปเป็นอินโฟกราฟิก", or runs
  /infographic. Deep-integrates with comprehensive-review and pubmed-research-note: it NEVER
  invents clinical facts — it renders a review or decision report in the vault or this session,
  and if none exists runs those plugins FIRST to generate sourced content, then lays it out as
  color-coded columns, stat tiles, and a mandatory contraindications / "medications to avoid"
  safety banner, filed to the vault as an asset via vault-keeper. NOT for: producing the
  underlying evidence (comprehensive-review / pubmed-research-note own that), non-clinical data
  charts (dataviz), or writing into vault/ directly (vault-keeper owns paths).
---

# Clinical Infographic — render the evidence, never author it

You turn an evidence report into a **single-page clinical reference** a clinician can pin to
a wall, laminate for a pocket, or print for the theatre. The deliverable is a **self-contained
HTML file** — color-coded columns, stat tiles, and a critical-safety banner — that opens
offline and prints clean.

This skill is a **rendering layer, not a research tool**. It has no search engines of its own
by design. Every fact on the infographic must already exist, sourced, in an underlying
`comprehensive-review` or `pubmed-research-note` report. The infographic is a *view* of that
report — never a new source of clinical truth.

## Prime directive — fidelity is the contract

The failure mode this skill exists to prevent is a **beautiful lie**: a crisp, confident panel
that says something the evidence never did — a dose without its ceiling, a target stripped of
its "unless contraindicated", a "medications to avoid" the layout quietly dropped for balance.
An infographic is read at speed, at the point of care, and trusted more than prose *because* it
is compact. That trust is the whole risk. So:

- **Nothing appears that is not traceable to the source report.** No new drugs, doses,
  numbers, or claims. If it is not in the report, it is not on the infographic.
- **Numbers keep their units and their qualifiers.** `<130/80 mmHg`, not `low`. `7–14 days`,
  not `early`. The "unless / avoid / only after" clause that makes a directive *safe* is part
  of the directive, never trimmed to fit a card.
- **Safety content is never sacrificed to design.** Contraindications, black-box warnings, and
  "do not use" items get the safety banner (see below); they are the last thing cut, never the
  first.
- **`[unverified]` never renders as fact.** A gap in the source stays a gap — omit it or mark
  it; do not launder it into a confident tile.

Read [references/source-contract.md](references/source-contract.md) before acquiring content
and [references/design-system.md](references/design-system.md) before laying anything out. The
worked retrospective in [references/lessons-learned.md](references/lessons-learned.md) explains
*why* the visual defaults below lean on diagrams and on rendering the result — read it once.

## Step 0 — Acquire SOURCED content (the deep integration)

The infographic needs a report to render. Resolve one in this order — **never skip to
authoring clinical facts yourself**:

1. **A report produced this session** — the user just ran `comprehensive-review` or
   `pubmed-research-note`, or pasted/pointed at one. Use it directly.
2. **An existing vault artifact** — query the **vault-keeper** skill for a matching review or
   decision report (its title, MOC, or topic). If one fits, that report is the single source
   of truth. Do not re-research it.
3. **No sourced content exists → generate it first, do not fabricate.** Pick the engine by what
   the user wants the infographic to *be*:
   - a **whole-topic / whole-disorder reference** (the usual case — phases, columns, the full
     picture) → run **comprehensive-review** first, then render its md.
   - a **single decision or protocol** ("first-line for X", "peri-op prep for Y") → run
     **pubmed-research-note** first, then render its verdict + working.

   Those plugins own their own intent-lock gate, searches, and citation discipline — let them.
   This skill never re-implements the interview and never issues a clinical claim of its own.

The only infographic-specific choices that vary — **page format** (wall poster / A4 handout /
pocket card), **column model** (clinical phases vs themes vs a decision's steps), and **length**
— default sensibly from the source's structure. Ask only when genuinely ambiguous; do not run a
full interview for a render.

## Step 1 — Read the source, extract the skeleton

From the source report, pull the renderable skeleton — nothing invented:

- **Title & scope** — the report's decision or disorder, its population/guideline basis.
- **The signature visual — name it first.** The one picture the report is *shaped* like: a
  physiologic **journey over time** (a BP / glucose / drug-level curve, a peri-op timeline), a
  **decision** (a branch), or a **mechanism** (a causal chain). Design this before the columns —
  it carries the gestalt they then detail. See the diagram grammar in `design-system.md`.
- **Columns** — 2–4 phases or themes the report is already organized around (e.g. Pre-op /
  Intra-op / Post-op; or Diagnosis / Treatment / Monitoring). If the report has no natural
  split, theme by the reader's workflow, not by prettiness.
- **Diagrams over prose cards** — sequential logic with conditions → an escalation ladder; a
  real choice → a decision-flow; two mirrored states → a paired split. Prefer these to text.
- **Cards** — the residue a diagram can't carry, each keeping its numbers and qualifiers.
- **Stat tiles** — the targets, doses, thresholds, and rates worth surfacing as figures.
- **Safety** — every contraindication / "avoid" / high-risk item, gathered for the banner.
- **Provenance** — the source's title, date, counts (`PubMed N · trials N`), and its
  `## Sources` mapping, carried into the footer so the infographic stays auditable.

## Step 2 — Lay it out (design system)

Fill [references/infographic-template.html](references/infographic-template.html) — a
self-contained, print-ready skeleton — following the grammar in
[references/design-system.md](references/design-system.md). The load-bearing rules:

- **Diagrams first.** The template ships commented, copy-ready scaffolds for a journey-curve,
  mechanism strip, decision-flow, escalation ladder, and surge/crash split. Fill the ones that
  fit the report's shape *before* writing prose cards; place the signature visual high on the
  page. Label every schematic *illustrative — not measured data* and put only sourced numbers
  on it (a target threshold, a labelled band) — never a value invented to make the picture read.
- **Self-contained, always.** One HTML file, inline `<style>`, inline SVG icons. **No external
  CSS, JS, fonts, images, or CDN** — it must open offline and print identically on any machine.
- **Color-coded columns** with a header chip (icon + phase/theme label), a tint, and stacked
  cards — the spine of the layout.
- **The critical-safety banner is mandatory** whenever the source carries contraindications or
  "avoid" content: a full-width, high-contrast band ("CRITICAL SAFETY — MEDICATIONS / ACTIONS
  TO AVOID") with prohibition iconography. Omit it *only* if the source truly has no such item.
- **Accessibility is not optional.** Color is never the only signal — every color pairs with a
  label or icon; contrast meets WCAG AA — **including white-on-accent headers and coloured cell
  markers** (verify white-on-accent ≥ 4.5, a "medium" green/blue often fails); headings are
  semantic; informative SVGs carry a label.
- **Light-locked — never a dark mode.** It renders on a white surface (paper + the Learn hub's
  white iframe). Keep `:root { color-scheme:light }` and ship **no** `@media
  (prefers-color-scheme:dark)` block — a partial one strands tinted rows and the safety body as
  invisible text under an OS dark theme. Wrap any wide table/heat-map in `.tscroll` so it scrolls
  inside its box, not the whole page (mobile).
- **A footer that keeps it honest** — the source title, the render date, and a collapsed
  Sources list (DOIs / NCT numbers), plus one line: *clinical reference aid, not a substitute
  for clinical judgment or local protocol.*

## Step 2.5 — Render & verify before filing

An infographic that was never rendered is a guess. Before it is filed:

1. **Rasterise it** — render the HTML to an image (a headless-browser screenshot) and *look*:
   nothing clipped or overlapping, columns balanced, the safety banner intact, every diagram
   and curve label legible, arrows pointing the way the flow reads.
2. **Check contrast and the dark-OS case.** Confirm white-on-accent headers and any coloured
   cell markers are legible (spot-check the ratios if unsure), and render once with the browser
   emulating a **dark** OS theme (`prefers-color-scheme: dark`) — the sheet must stay light and
   fully readable. If a row, the safety body, or an SVG label vanishes, a stray dark block
   survived: remove it. Also render narrow (~390 px) to confirm no table pushes the page sideways.
3. **Optionally OCR** the render — cheap insurance that a dense card or a curve annotation did
   not silently drop or overlap; the OCR text should contain the load-bearing numbers.
4. Fix layout in the HTML and re-render until it holds. The **PNG render is a first-class
   deliverable** alongside the HTML — offer it for sharing or embedding.

This is a *layout* check, never a content one — it changes how a fact sits on the page, never
the fact.

## Step 3 — Where output goes

1. **Write** the finished infographic as a single `.html` file (plus the PNG render from Step
   2.5) in the working directory.
2. **Surface it** — show the file to the user so they can open/print it (render or attach it);
   do not merely name a path.
3. **File it via vault-keeper.** An HTML infographic is a rendered **asset**: hand it to the
   **vault-keeper** skill to place in `vault/assets/` and wire into the **source report's
   MOC** under its `## Assets` section, linked from the source artifact when one exists (pass
   the asset — HTML plus PNG — a title like `<Topic> — Infographic`, and the suggested MOC
   topic; a short companion-note body is optional, only when it adds something the MOC line
   cannot carry). Vault-keeper owns every path, dedup, and MOC wiring — never resolve a vault
   path or write into `vault/` from this skill. Skip only on an explicit "don't vault this".

**No filesystem:** render/return the HTML inline and say explicitly that nothing was written
or filed. Never claim a save you did not perform, and never invent a vault path.

## Handoffs

- **comprehensive-review** — generates the whole-topic sourced content when none exists; the
  usual upstream for a reference infographic. Never duplicate its search here.
- **pubmed-research-note** — generates the sourced decision/protocol content when the
  infographic is about one call. It also owns any live verdict — the infographic shows the
  verdict, it never issues one.
- **vault-keeper** — every vault write (asset + MOC `## Assets` wiring; companion note
  optional), per Step 3.
- **intent-lock** — not re-run here; it gates the upstream content plugins when they generate.

## Close

Two lines in chat: what was rendered and from which source report, the file path, the vault
asset path returned by vault-keeper (or that the save was skipped), whether the safety banner
was included, and any `[unverified]` gap that was omitted rather than shown. The HTML file is
the deliverable — never restate its content inline as prose.

## Failure conditions

This skill has failed if:

- A clinical claim, drug, dose, or number appears on the infographic that is not traceable to
  the source report — or the skill authored clinical content instead of rendering sourced content.
- A number lost its units, or a safety-critical qualifier ("unless contraindicated", "only
  after alpha-blockade") was trimmed to fit a card.
- The source named contraindications / "avoid" items and the critical-safety banner was omitted.
- An `[unverified]` gap was rendered as a confident fact.
- The HTML referenced any external CSS, JS, font, image, or CDN — i.e. it is not self-contained
  and would not open or print offline.
- Color was the only signal for meaning, or contrast/heading semantics failed accessibility —
  including a white-on-accent header or coloured cell marker below 4.5:1.
- The document shipped a `@media (prefers-color-scheme:dark)` block (or was not light-locked), so
  it renders with stranded/invisible text under an OS dark theme.
- A wide table or heat-map was left unwrapped and scrolled the whole sheet sideways on mobile.
- A schematic/illustrative figure was drawn without an "illustrative — not measured data"
  label, to a fabricated axis, or carrying a number not in the source.
- The infographic was filed without ever being rendered and eyeballed for clipped text, broken
  layout, or a diagram/arrow that reads the wrong way.
- Content was rendered with no traceable source when comprehensive-review or
  pubmed-research-note should have generated it first.
- A vault path was resolved or a file written into `vault/` by this skill instead of vault-keeper,
  or a save/path was claimed that did not happen.
