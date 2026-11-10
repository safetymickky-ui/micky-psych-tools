# The eight slots of a look spec

A look spec has eight slots. Each slot holds a value that can be measured or pointed at.
A word such as "clean", "modern", "minimal" or "compact" is not a value: it is the
question that still has to be asked.

Ask a slot only when two fitting answers would make the user see a different build.
Otherwise give it the default below and carry it as an assumption.

## 1. Canvas

Where the build is seen, and at what size.

- **Value form:** the target and its size. "Phone first, 390 × 700, no scrolling."
  "Desktop page, 1280 wide, scrolls." "A4 portrait, prints on one sheet." "Slide, 16:9."
  State whether a second size must also work.
- **Default:** a page that works at 390 px and at 1280 px and scrolls.
- **Ask when:** the request does not say where it will be read, and the answer changes the
  layout (one screen with no scrolling versus a long page; print versus screen).
- **Option examples:** "One phone screen, 390 × 700, nothing scrolls" / "A long page that
  scrolls, phone and desktop" / "One A4 sheet for print".

## 2. Layout

How the regions are arranged, and the reading order.

- **Value form:** the named regions, their arrangement and their widths. "One column,
  680 px, sections stacked: summary, diagram, detail." "Two columns from 900 px: source left
  60 %, notes right 40 %; stacked below 900 px." "Grid of cards, 3 across at 1280 px, 1
  across at 390 px."
- **Default:** one column of at most 720 px, sections stacked in reading order.
- **Ask when:** the content can be arranged in more than one way that fits the canvas.
- **Wireframe in the preview:** when the picker shows previews, draw each option with box
  characters, at most 12 lines:

  ```
  ┌──────────────┐
  │ Summary      │
  ├──────┬───────┤
  │ Fig  │ Notes │
  └──────┴───────┘
  ```

## 3. Density

How much sits on one screen, and how much air is around it.

- **Value form:** body text size, line height, the gap between sections, and how many items
  the first screen holds. "16 px body, 1.55 line height, 32 px between sections, about 5
  items on the first screen."
- **Default:** 16 px body text, 1.5 to 1.6 line height, 24 to 32 px between sections.
- **Ask when:** the content can be shown as a few large items or as many small ones.
- **Floors that are never asked:** body text is at least 14 px on a screen and 9 pt in
  print; a label inside a figure is at least 12 px; a touch target is at least 44 px.

## 4. Emphasis

What the eye lands on first, second and third.

- **Value form:** the ordered list of what stands out, and by which means. "First the
  verdict line (28 px, bold), then the diagram, then the section headings (19 px)."
- **Default:** the title, then the first figure or the first heading.
- **Ask when:** the build holds two things that could each lead (a number or a diagram; a
  verdict or a method).

## 5. Colour

The ground, the ink, the accent, and the theme.

- **Value form:** hex values by role, and the themes. "White ground #FFFFFF, ink #1B232B,
  one accent #0E7C86; light and dark." A meaning colour (good, warning, critical) is listed
  apart from the accent.
- **Default:** the project's existing palette when one exists; otherwise a white or
  near-white ground, a near-black ink and one accent, in light and dark.
- **Ask when:** no palette governs and the subject allows more than one direction (light
  or dark first; one accent or a set of category colours).
- **Words rarely settle colour.** When the user cannot choose from the descriptions, this
  slot goes to the sample sheet.
- **Never asked:** body text contrast is at least 4.5 : 1 against its ground.

## 6. Type

The typefaces, and the size scale.

- **Value form:** the face for each role and the scale. "Headings Atkinson Hyperlegible
  700, body the same at 400, numbers and code JetBrains Mono; sizes 13 / 16 / 19 / 23 / 28."
- **Default:** the project's existing faces when they exist; otherwise one sans-serif
  family for headings and body, and a monospace face for code and aligned numbers.
- **Thai:** every stack that may show Thai text names a face that holds Thai glyphs.
- **Ask when:** the look depends on the voice of the type (serif or sans headings; a
  display face or none).

## 7. Graphics

What is drawn, and in which style.

- **Value form:** the kind and count of visuals and the drawing style. "One inline SVG flow
  diagram, 1.5 px lines, no icons, no photos." "Three stat tiles and one bar chart."
- **Default:** only the visuals the content needs; line drawings in the ink and accent
  colours; no decorative icons and no stock images.
- **Ask when:** the content could be shown as a diagram, a chart, a picture or text only.

## 8. Motion

What moves, when, and what the viewer controls.

- **Value form:** what animates, the trigger and the duration; or "none". "Step changes
  animate over 300 ms on Next; nothing plays on its own; respects reduced motion."
- **Default:** none.
- **Ask when:** the build shows a process or a change over time, where static frames and
  motion would both fit.

## Kinds of output (the scope of a rule)

Name the kind of output with one of these words. A saved rule matches a build of the same
kind, or every build when its scope is `any`.

- `page`: an explainer, a report or an article page.
- `dashboard`: a page of numbers that is scanned, not read.
- `app`: a tool with controls that the user operates.
- `slides`: a slide deck.
- `figure`: one chart, diagram or image.
- `infographic`: a one-sheet visual summary.
- `document`: a document meant for print or PDF.
- `any`: every kind.

## A filled spec

```
canvas:    phone first, 390 × 700, also 1280 wide; scrolls
layout:    one column, 680 px max; summary, diagram, detail
density:   16 px body, 1.55 line height, 32 px between sections
emphasis:  verdict line (28 px bold), then the diagram, then headings (19 px)
colour:    ground #FFFFFF, ink #1B232B, accent #0E7C86; light and dark
type:      Atkinson Hyperlegible for headings and body; JetBrains Mono for numbers
graphics:  one inline SVG diagram, 1.5 px lines; no icons, no photos
motion:    none
```
