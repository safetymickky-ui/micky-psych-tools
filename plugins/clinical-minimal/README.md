# clinical-minimal

Personal design system for every Office file Claude makes: white page, one clinical-teal accent,
Leelawadee UI for Thai and English, structure from hairline rules and space. No personal branding on files.

## Components

- **skill `clinical-minimal`**: fires on any request for a document, deck or spreadsheet, or when another
  plugin is about to produce one (it decides how the file looks; the other decides what it says).
- `cm.py`: build helpers for python-docx, python-pptx and openpyxl (styles, tables, charts, KPI tiles,
  forest plots, timelines, range bars, diagrams, pictures, fade transitions and click builds).
- `slidecheck.py` + `slideprobe.ps1`: per-slide verification. PowerPoint lays the deck out; automatic checks
  (overflow, split words, wrapping titles, collisions, blurry/stretched pictures, missing credits, empty
  slides) plus a recorded full-size visual review of every slide.
- `imgpick.py`: picture selection. Brief → Google Images candidates → filter (stock, avoid terms, resolution,
  duplicates) → score (relevance, trust, resolution, crop, sharpness, fill) → contact sheet as placed →
  visual judgement → choose, with credits recorded.
- `render.ps1`: Word/Excel → PDF for visual QA.

## Requirements

Windows with Microsoft Office; `pip install python-docx python-pptx openpyxl pillow numpy`.
