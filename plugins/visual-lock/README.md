# visual-lock

Asks how a visual build should look before it is built, and remembers the answers.

Before Claude builds a page, an artifact, a slide deck, a figure or an infographic, it fills a
look spec with eight slots: canvas, layout, density, emphasis, colour, type, graphics and
motion. A slot is asked only when the request, a fixed design system and your saved guidance
all leave it open.

- **Words first.** Picker questions, at most 4 per round and at most 2 rounds. Each option
  says what you would see, with its value ("One column, 680 px wide, sections stacked").
- **Samples only when needed.** When words cannot settle a choice (two layouts, two
  palettes), Claude renders one sheet of 2–4 variants with the real content, at true size,
  and you pick a letter.
- **A measurable spec.** Every slot holds a value: pixels, counts, hex colours, font names.
- **A check on the render.** The finished build is rendered and compared with the spec
  before you see it.
- **Saved for reuse.** Each choice you made is saved to the **Look Book** page. The next
  build of the same kind does not ask it again. The same choice made for two kinds of output
  becomes a rule for every build. A correction after delivery is saved too.

## Use

```
/visual-lock a one-page summary of the lithium review
/visual-lock show
/visual-lock forget the dark theme rule
```

Or in chat: "interview me about the look", "ask me how it should look", "lock the look",
"show me options first", "remember this look", "ถามเรื่องหน้าตาก่อน", "ล็อคหน้าตา". It also
runs on its own before a visual build whose look is open.

The delivery carries 2–4 look lines: the look with its main values, what came from saved
guidance or was assumed, and the result of the render check.

## The Look Book page

A private artifact titled "Look Book" (template in `skills/visual-lock/assets/look-book.html`).

- **Saved guidance:** your rules, grouped by the kind of output they apply to. A rule that
  names colours shows them as swatches. "Stop using" retires a rule; a retired rule can be
  used again or deleted.
- **Builds:** each build that used a look interview, with the spec it was built to and the
  result of the check.

The skill writes to the page's database (`rules/<id>`, `builds/<id>`) through `ArtifactData`;
see `skills/visual-lock/references/look-book.md`. It finds the page by its title and creates
it from the template at the first save.

## What it does not ask

A look that something else already fixes is never asked: Office files follow
clinical-minimal, concept labs follow concept-lab, clinical one-pagers follow
clinical-infographic, and a project `DESIGN.md` governs its own tokens. Contrast, minimum
text size and touch-target size are floors, not questions.

## Install

```
/plugin marketplace add safetymickky-ui/micky-psych-tools
/plugin install visual-lock@micky-psych-tools
```

## Files

```
skills/visual-lock/SKILL.md                     the procedure
skills/visual-lock/references/slots.md          the eight slots, value forms and defaults
skills/visual-lock/references/sample-sheet.md   when and how to render sample variants
skills/visual-lock/references/look-book.md      find, create, read and write the Look Book
skills/visual-lock/assets/look-book.html        the Look Book page template
skills/visual-lock/assets/sample-sheet.html     the sample sheet frame
commands/visual-lock.md                         /visual-lock
evals/visual-lock/                              trigger and near-miss cases
```

## Boundaries

What the output should contain, what it is for and how deep it goes is intent-lock, which
runs first when both apply. A fork that appears mid-task is decision-interview. Writing a
design-system file is design-md-generator. Reviewing a finished design is a design review.
