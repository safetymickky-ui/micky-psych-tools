# Changelog

## 0.1.0 — 2026-09-26

First release in micky-psych-tools. Moved in from the claude.ai-uploaded skill
(`anthropic-skills:bullet-reconstruct`) and revised after a refine-plugin audit:

- **Measured gate.** Units are frozen from the source before the bullets are written and
  carry `anchors`; `coverage_check.py --output` downgrades any unit the notes do not
  support. New `distorted` status (full loss). `--source` fails a number that is not in
  the source. Unit density is reported. Long sources are scored by a fresh subagent.
- **Evidence tier.** A dropped hedge, species, design or population scores `partial` at
  most. Reference titles may supply a missing tier, marked `(ref. title)`; author
  disclosures are kept as one line when the source argues for a named drug.
- **Figure and table snips.** New `snip_figures.py`: captioned regions cropped at 300 dpi,
  vector tables included, logos and icons skipped.
- **HTML output.** New `build_html.py`: one self-contained file (base64 images, light/dark,
  print CSS, Thai-capable fonts, no lazy loading). The `.md` stays as the vault source.
- **Delivery.** No hard-coded paths or tool names; the file is sent with whatever
  file tool the session has.
- **Description.** Third person, "Use when" before char 250, new triggers ("reconstruct
  this article", "keep the figures", "as html"). The Not-for no longer names
  crq-essay-review, which does not exist, and now names ingest-article.
