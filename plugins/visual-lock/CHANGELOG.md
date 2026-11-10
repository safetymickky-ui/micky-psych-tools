# Changelog

## 0.1.0 — 2026-11-10

- Initial release. A look interview before a visual build: eight slots (canvas, layout,
  density, emphasis, colour, type, graphics, motion), filled from the user's words, then a
  fixed look, then saved guidance, and asked only when still open. The owner chose on
  2026-11-10: choices are saved for reuse, and questions come in words first with rendered
  samples only when words cannot settle a choice.
- Picker questions in at most 2 rounds (1 when intent-lock ran for the same request). No
  recommendation on taste; an option is marked recommended only when a constraint favours it.
- Sample sheet (`assets/sample-sheet.html`): 2–4 variants with the build's real content,
  drawn at the true canvas width and scaled to fit, at most two slots varied.
- A measurable look spec, a check of the rendered result against it before delivery, and
  2–4 look lines with the delivery.
- Look Book page (`assets/look-book.html`): an artifact with a database holding
  `rules/<id>` and `builds/<id>`. Rules grouped by kind of output, colour swatches, retire /
  use again / delete, and a log of builds with their specs. Clinical Minimal palette, light
  and dark. A rule widens to every build when the same choice is made for two kinds of output.
- `/visual-lock` command; trigger and near-miss eval cases.
