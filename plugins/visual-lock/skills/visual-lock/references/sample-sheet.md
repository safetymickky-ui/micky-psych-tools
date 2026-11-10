# The sample sheet

A sample sheet is one page that shows 2 to 4 variants of the build side by side, so the user
can choose what words could not settle. Step 4 of the skill says when to make one.

## Rules

- **2 to 4 variants, labelled A, B, C, D.** The label is large and sits above each variant.
- **Real content.** Use the title, the first section and the first figure of this build.
  Never lorem ipsum, never invented numbers. Clinical content keeps its sourced wording.
- **The same content in every variant.** Only the look differs.
- **At most two slots vary.** Every settled slot is applied to every variant. When three
  slots are open, show the two that change the build most and give the third its default.
- **True size.** Draw each variant at the canvas size of the spec, then scale the whole
  frame down to fit. A phone variant is drawn 390 px wide. Never reflow a desktop layout
  into a narrow box: that shows a layout the user will not get.
- **One line under each label** names what differs, with its values: "A: one column,
  diagram first" / "B: two columns, diagram right".
- **A fragment is enough.** Show the first screen of the build. Do not build the whole
  page four times.
- **No polish.** The sheet is a throwaway. It needs to be accurate in the varied slots and
  plain everywhere else.

## Build it

Start from `assets/sample-sheet.html` next to this skill's SKILL.md. It holds the frame: a
grid of labelled panels that stacks to one column on a phone, and a `.stage` in each panel
that scales its content from the true canvas width.

1. Copy the file to the scratchpad or the working directory.
2. Set `--canvas-w` on each `.stage` to the canvas width of the spec, in pixels without a
   unit (`390`, `1280`).
3. Put each variant's markup inside its `.stage`. Prefix every class of a variant with its
   letter (`.a-title`, `.b-title`) so the variants' styles cannot touch each other.
4. Write the caption of each panel: the letter, then what differs.
5. Delete the panels you do not use.

## Show it

Use the first way this session offers:

1. Publish the file with the `Artifact` tool (a private page; `icon: "swatch"`; the title in
   the file is "Look Samples"). Publish the next build's sheet from the same file path in
   the same session so one page is reused.
2. Send the file to the user (`SendUserFile`, `display: "render"`).
3. Take a screenshot with a headless browser and show the image.

Then ask one picker question: "Which variant should the build follow?" Each option is a
letter plus what differs. The free-text answer may mix variants ("A with B's heading").

## After the choice

- The chosen variant's values go into the spec for the slots that varied.
- Each varied slot becomes a saved rule with `source: "sample"` (see `look-book.md`).
- Do not keep, file or link the sheet. It is not part of the delivery.
