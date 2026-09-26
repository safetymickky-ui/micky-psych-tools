# Figures, tables and the HTML output

## Snipping from a PDF

```
python3 "$SKILL_DIR/scripts/snip_figures.py" source.pdf --out snips [--dpi 300] [--gap 24] [--pages 2-5]
```

- It finds caption labels (Figure, Fig., Table, Box, Scheme, Chart, Exhibit + a number)
  that start a line in their column, grows each caption into the graphics beside it
  (rules, boxes, curves, raster images), renders the region and trims the margin.
- It works on vector tables. A PDF whose tables are drawn with rules and text holds zero
  embedded images, so an image extractor such as `pdfimages` finds nothing there.
- It also saves large raster images with no caption (`image-p3-1.png`). It skips icons
  and logos: anything smaller than `--min-pt` (72 pt), or of one size on two or more pages.
- It writes `snips/manifest.json`: file, kind, label, page, caption text, crop box.

## Review every snip before using it

Open each PNG. Then:
- **False positive** (a body line starting "Table 1 shows…" grew into a nearby graphic):
  delete the file.
- **Cut off** (part of the figure is missing): re-run with a larger `--gap`, for
  example 36.
- **Two figures merged** (neighbours closer than `--gap`): re-run with a smaller `--gap`,
  for example 12, or `--pages` for just that page.
- **Skipped caption** ("no graphic next to the caption"): a text-only table. Rebuild it
  as a markdown table in the notes; it counts as text units.
- **Decorative image kept** (a large logo or cover): delete it.

## Other source formats

- `.docx`: images are in the zip under `word/media/`; `.pptx`: under `ppt/media/`
  (python `zipfile`). Match each image to its caption from the document text.
- An image or screenshot given as the source: use it as it is.
- Pasted text or a web article with no files: no snips. Say so in the report line.

## Placing a snip in notes.md

Put it alone on its own line, right under the bullet that discusses it, with a blank
line before and after:

```
![Table 2: how orexin antagonism may improve glucose control](snips/table-2.png "Table 2 · p. 3 · McIntyre & Wong 2026 · CC BY 4.0")
```

- Alt text: the label and what the figure shows (read aloud by screen readers).
- Title (the quoted part): the caption build_html.py prints under the image. Use
  `Label · page · Author Year`; add the licence when the source states one (CC BY needs
  attribution). Without an open licence, keep the notes for personal study.
- The snip does not replace text: also write the figure's unique facts as bullets.

## The HTML contract (what build_html.py guarantees)

```
python3 "$SKILL_DIR/scripts/build_html.py" notes.md --out notes.html [--title T] [--source-html H] [--footer-html H]
```

- One self-contained file: every local image is embedded as base64; no CDN, no web
  fonts, no scripts. A missing, remote or unsupported image fails the build (exit 1).
- Header: the `# ` title and the italic source line after it. A footer names what was
  discarded. Pass `--footer-html` to state the exact classes.
- An image alone on its line becomes a `<figure>` with its title as the caption.
- No `loading="lazy"`: a lazy data-URI image stays blank in print, in previews and in
  full-page captures.
- Light and dark mode follow the device; print CSS keeps figures unbroken; the font
  stack covers Thai.

Look at the page once before delivery. With a headless browser (playwright), render
it at 390 px wide: no horizontal scroll, every figure visible. Without one, check that
the script's image count equals the number of snips placed in the notes.
