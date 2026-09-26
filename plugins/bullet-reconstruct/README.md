# bullet-reconstruct

Turns a dense source (a paper, a book chapter, a review, a transcript) into **tight,
scannable bullets**. It drops the packaging (reference list, citation numbers,
affiliations, boilerplate), **keeps figures and tables as image snips** cropped from the
file, and delivers **one self-contained HTML file** that opens offline, on a phone, and
prints cleanly.

It is a bounded-loss distillation, not a faithful reformat: loss is expected, but it is
capped under 10% of the source's substantive units, and the cap is measured.

## The gate: measured, not asserted

| Step | What stops a silent loss |
| --- | --- |
| Units frozen first | `units.json` is written from the source before any bullet exists, so the list is not shaped by what was kept. |
| Anchors | Each unit names the numbers and terms that must survive. `coverage_check.py --output` looks for them and downgrades any unit the notes do not support. |
| `distorted` status | A changed number, name or direction counts as a full loss and is always listed. |
| Number check | `--source` fails the run when a number in the notes does not occur in the source text. |
| Evidence tier | A dropped hedge, species, design or population makes the unit partial at most. |
| Fresh scorer | For sources over ~5,000 words, a subagent that did not write the notes does the scoring. |

## Figures and tables

`snip_figures.py` finds each captioned figure or table in a PDF, grows the caption into
the graphics beside it, and crops that region at 300 dpi. It works on **vector tables**
too (rules and text drawn on the page), where an embedded-image extractor finds nothing.
It skips logos and icons. Each snip goes under the bullet that discusses it; its facts
are also written as text, so they stay searchable.

## Use it

Just ask:

- "reconstruct this article", "reconstruct in bullets, keep the figures, as html"
- "bulletise this review, drop the references"
- "ทำเป็น bullet", "ย่อเป็นข้อ ๆ"

Output: `notes.html` (the deliverable), plus `notes.md` and `snips/` as the source for
the vault. The report line gives loss %, unit count and density, the number check, and
snips kept or skipped.

## What's inside

```
skills/bullet-reconstruct/
  SKILL.md                          # workflow + distillation contract
  references/verification.md        # units.json, anchors, statuses, subagent brief
  references/figures-and-html.md    # snip review, image syntax, HTML contract
  scripts/coverage_check.py         # the gate
  scripts/snip_figures.py           # figure/table crops from a PDF
  scripts/build_html.py             # notes.md -> one self-contained HTML
evals/bullet-reconstruct/           # trigger, near-miss and output cases
tests/test_scripts.py               # unit tests for the three scripts
```

Scripts need Python 3 with `pdfplumber`, `pillow` and `markdown`
(`python3 -m pip install pdfplumber pillow markdown`). Tests:
`python3 -m unittest discover -s plugins/bullet-reconstruct/tests`.

## Install

```
/plugin marketplace add safetymickky-ui/micky-psych-tools
/plugin install bullet-reconstruct@micky-psych-tools
```

This plugin replaces the claude.ai-uploaded skill of the same name. After installing
it, remove the uploaded copy, or two skills named `bullet-reconstruct` compete for the
same requests.
