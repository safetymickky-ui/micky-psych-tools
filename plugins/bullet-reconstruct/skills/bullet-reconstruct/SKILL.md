---
name: bullet-reconstruct
description: >-
  Distils a dense source (paper, article, book chapter, review, transcript) into
  scannable bullets with measured, bounded loss under 10%, keeps its figures and tables
  as image snips cropped from the file, and delivers one self-contained .html. Use when
  the user says "reconstruct this article", "reconstruct in bullets", "bulletise",
  "condense", "distil", "strip to essentials", "keep the figures", "as html",
  "ทำเป็น bullet", "ย่อเป็นข้อ ๆ", or wants the substance without footnotes, citation
  numbers or boilerplate. Not for a lossless reformat to PDF (reformat-md-pdf), clinical
  case data (psych-case-reconstruct), adding a paper to the Learn hub (ingest-article),
  or new content from textbooks (comprehensive-review).
---

# bullet-reconstruct

Return a dense source's substance as bullets: packaging discarded, at least 90% of the
substantive units kept, figures and tables kept as images, delivered as one HTML file.
The 90% is **measured, not asserted**: units are frozen from the source before any bullet
is written, each unit carries anchors that a script must find in the output, and every
number in the notes must exist in the source.

`$SKILL_DIR` below is the directory this skill loaded from (in Claude Code:
`${CLAUDE_PLUGIN_ROOT}/skills/bullet-reconstruct`). The scripts need Python 3 with
pdfplumber, Pillow and markdown (`python3 -m pip install pdfplumber pillow markdown`).

## Workflow

1. **Ingest the whole source** end to end before writing anything. If it is a file,
   also save its plain text as `source.txt` (PDF: `pdftotext -layout` or pdfplumber);
   the number check reads it.
2. **Freeze the units first.** Walk the source top to bottom and write `units.json`:
   one unit per claim, number, named entity or relationship, each with `anchors` (the
   exact numbers and names that must survive). Do it before the bullets exist, so the
   list is not shaped by what was kept. Rules and schema:
   [references/verification.md](references/verification.md).
3. **Snip figures and tables** (PDF sources):
   `python3 "$SKILL_DIR/scripts/snip_figures.py" source.pdf --out snips`
   Open every snip. Delete false positives; a skipped caption means a text-only table,
   so fold it in as a markdown table. Other formats and the review checklist:
   [references/figures-and-html.md](references/figures-and-html.md).
4. **Write the bullets** in `notes.md` under the contract below. Put each snip under
   the bullet that discusses it, alone on its line:
   `![Table 1: short description](snips/table-1.png "Table 1 · p. 2 · Author Year")`
   Also fold the figure's unique facts into text bullets: an image is not searchable
   and does not count for the gate.
5. **Score, then run the gate.** Score each unit `present`, `partial`, `missing` or
   `distorted` against `notes.md`. For a source over ~5,000 words, a subagent that did
   not write the notes does the scoring (brief in verification.md). Then run:
   `python3 "$SKILL_DIR/scripts/coverage_check.py" units.json --output notes.md --source source.txt`
   FAIL means loss of 10% or more, a unit downgraded by the anchor check, or a number
   that is not in the source. Fix the notes, re-score, re-run. Only PASS clears delivery.
6. **Build the HTML:**
   `python3 "$SKILL_DIR/scripts/build_html.py" notes.md --out notes.html`
   It embeds every image, so the one file works offline and on a phone. Look at the
   result once: render it at phone width if a headless browser is available; otherwise
   check the script's image count against the snips.
7. **Deliver.** Save in the working directory and send `notes.html` with the session's
   file tool (SendUserFile, present_files, or whatever the session provides). Keep
   `notes.md` and `snips/` as the source for the vault. Report in one line: loss %,
   unit count and density, number check, snips kept and skipped, discarded classes.

## Distillation contract

**Keep. Each lost item counts against the 10%:**
- Every distinct claim, mechanism, relationship and definition.
- Every named entity (people, models, regions, receptors, genes, drugs, instruments,
  datasets) and every quantity (n, %, CI, dose, year, direction, threshold).
- **The evidence tier of each claim**: its hedge ("appears to", "emerging evidence",
  "may"), its species, its design and its population. Losing any of them changes the
  claim, so that unit scores `partial` at most.
- The argumentative spine: the order in which ideas depend on each other.
- Content unique to figures and tables: as a snip AND as text.
- **Appraisal facts that sit in packaging:**
    - When the body states a finding without its species, design or population and the
      cited reference's title gives it, carry it into the bullet, marked `(ref. title)`.
    - When the source argues for a named drug or intervention, keep the authors'
      disclosures as one line (companies named).

**Discard. This is packaging, not loss:** the reference list; in-text citation markers
(keep the claim); affiliations, correspondence, received/accepted dates, DOI and running
heads (keep one source line at the top); funding, acknowledgements, author contributions,
licence text; figure-legend prose that only repeats the body; decorative images (logos,
icons, badges); filler with no information. A footnote that carries a real argument is
not packaging. Borderline means keep.

**Compress, don't transcribe:** paraphrase each unit in fewer words, merge repeated
statements, keep technical terms exact, and compress the prose around them.

**Hold the boundary:** add nothing the source does not say; never change a number, a
name or a direction of effect. If the source looks wrong or miscited, tell the user
separately, not in the bullets.

## Bullet conventions

- Start `notes.md` with `# Title` and an italic source line
  (`*Author. Journal Year;Vol:Pages — design*`); build_html.py turns them into the header.
- One source section → one `##` heading, in source order; sub-themes → `###`.
- Nest with 4 spaces; a unit that qualifies another is its child.
- Lead each bullet with its key term in **bold**, then the compressed claim.
- Tables only for truly tabular units. Keep Unicode (→ ↑ ↓ ≈ ≥ ≤, Greek letters) and
  keep Thai–English code-switching exactly as the source writes it.

## Not for

- A lossless reorganisation that keeps everything (reformat-md-pdf).
- Clinical case data (psych-case-reconstruct).
- Getting a paper into the Learn hub (ingest-article).
- Generating content from textbooks or background knowledge (comprehensive-review).
- A PDF deliverable. The HTML prints cleanly from a browser. OPTIONAL: if
  document-to-pdf or reformat-md-pdf is installed, hand it `notes.md`; if neither is,
  print the HTML to PDF.

## Files

- [references/verification.md](references/verification.md): units.json schema, unit
  and anchor rules, scoring statuses, the subagent brief, reading the gate output.
- [references/figures-and-html.md](references/figures-and-html.md): snip review,
  non-PDF sources, image syntax and captions, the HTML contract.
- [scripts/coverage_check.py](scripts/coverage_check.py): the gate (anchors, statuses,
  number check, unit density).
- [scripts/snip_figures.py](scripts/snip_figures.py): captioned figure and table crops
  from a PDF, vector tables included.
- [scripts/build_html.py](scripts/build_html.py): `notes.md` → one self-contained HTML.
