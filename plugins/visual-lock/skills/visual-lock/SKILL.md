---
name: visual-lock
description: >-
  Locks how a visual build should look before it is built, and saves each choice as guidance
  for later builds. Use when the user says "interview me about the look", "ask me how it
  should look", "lock the look", "show me options first", "remember this look",
  "ถามเรื่องหน้าตาก่อน", "ล็อคหน้าตา", or runs /visual-lock, and unprompted before building a
  page, artifact, slide deck, figure or infographic whose look the request and the saved
  guidance leave open. Asks picker questions on canvas, layout, density, emphasis, colour,
  type, graphics and motion in at most 2 rounds, and renders one sheet of 2-4 sample variants
  only when words cannot settle a choice. Writes a measurable look spec, checks the render
  against it, and saves the choices to the Look Book artifact so the next build asks less.
  Not for what the output should contain (intent-lock), mid-task forks (decision-interview),
  writing a design-system file (design-md-generator), or a look a plugin already fixes
  (clinical-minimal, concept-lab).
---

# Visual lock

This skill prevents two failures:

1. **The look is guessed.** The build is finished, the user says "this is not what I
   pictured", and the build is done again.
2. **The same thing is asked or corrected twice.** A choice the user made last week is asked
   again, or a correction the user gave last week is needed again.

So the look is asked before the build, written as values that can be measured, checked on the
rendered result, and saved for the next build.

## What the user sees

Only these four things:

1. Picker questions, in at most 2 rounds.
2. At most one sample sheet, and only when words cannot settle a choice.
3. The look lines, with the delivery (2 to 4 lines).
4. The work.

Do everything else silently. Do not narrate the steps, announce the skill or print the spec.

## Step 1. Load the saved guidance

Read the active rules from the Look Book before drafting anything.
[references/look-book.md](references/look-book.md) says where the Look Book is and how to
read it. This is one query. When the Look Book cannot be reached, continue with no saved
rules and say so in the look lines.

## Step 2. Draft the look spec

The spec has eight slots: **canvas, layout, density, emphasis, colour, type, graphics,
motion**. [references/slots.md](references/slots.md) defines each slot, the form of its
value and its default.

Fill each slot from the first source that settles it, in this order:

1. **The user's words in this request**, including a reference the user gave (an image, a
   file, a URL, "like the last one"). Open and look at a reference before asking about it.
2. **A fixed look that governs this build.** A plugin's own design contract (concept-lab,
   clinical-infographic, clinical-minimal for Office files), a project `DESIGN.md`
   (design-md-apply), or the existing page when this is an edit. A fixed look is never asked
   about and never overridden by a saved rule.
3. **A saved rule whose scope matches this kind of output.** The slot is filled and not
   asked. A rule with scope `any` matches every build; a rule with a specific scope wins
   over it.
4. Otherwise the slot is **open**.

Then test the open slots. Imagine two finished builds that both satisfy the request and
every filled slot, and that look different enough that the user would send one of them
back. A slot where they differ stays open. A slot where the difference would not matter to
the user takes its default and becomes an assumption. When no slot stays open, skip Steps 3
and 4.

## Step 3. Ask in words first

Ask the open slots in this order: canvas, layout, density, emphasis, then colour, type,
graphics, motion. An earlier slot changes the options of a later one.

- Use the picker tool (`AskUserQuestion`, loaded with ToolSearch when deferred). Ask at most
  4 questions in a round, in one call. **The limit is 2 rounds.** When intent-lock ran for
  the same request, the limit is 1 round.
- Write each option as what the user would see, with its value: "One column, 680 px wide,
  sections stacked" is an option. "Minimal" is not.
- For a layout question, put a small text wireframe in the option's preview when the picker
  shows previews.
- Offer 2 to 4 options. Every option fits the request and every filled slot.
- Never recommend on taste. State the trade-off of each option in its description. Mark an
  option "(Recommended)" only when a constraint favours it (the amount of content, the
  canvas, legibility or contrast), and name that constraint in the description.
- Make each question stand alone. The user may see only the picker.
- Match the user's language. Use short plain sentences.
- Stop at once when the user says LOCK, "stop asking", "พอ" or anything with that meaning.
- After the last round, every slot that is still open takes its default and becomes an
  assumption.

Never ask permission to start, never ask the user to confirm the spec, and never ask about
content, purpose or depth: those belong to intent-lock.

**When nobody can answer** (an unattended run, or an opt-out such as "just build it",
"ไม่ต้องถาม"): ask nothing. Use the saved rules and the defaults, and state the unconfirmed
slots as assumptions.

## Step 4. Show one sample sheet, only when needed

Render samples only when one of these holds after the questions:

- A slot is still open and its options differ in space, proportion, colour or type in a way
  one sentence cannot carry (two layouts, two palettes, two type pairings).
- The user answered "not sure", "show me", "ขอดูก่อน", or picked free text that has two
  visual readings.
- Two answers conflict when put on the same canvas.

Never render samples for a slot that words settled. One sheet per build; a second one only
when the user asks for it.

Build the sheet as [references/sample-sheet.md](references/sample-sheet.md) says: 2 to 4
variants labelled A to D, the real content of this build, the same content in every
variant, every settled slot applied, and at most two slots varied. Show it, then ask one
picker question: which variant. A free-text answer may mix them ("A with B's heading").

The sheet is a throwaway. It is not the deliverable, and it gets no polish beyond what the
choice needs.

## Step 5. Lock

Write the spec when the questions end, and start the build in the same turn.

- Every slot holds a value that can be measured or pointed at: pixels, counts, hex colours,
  font names, named regions. [references/slots.md](references/slots.md) gives the form.
- For a build with more than a few steps, save the spec to `visual-lock.md` in the working
  folder and reread it before the check in Step 7.
- Give the spec, word for word, to every subagent that builds part of the output.

## Step 6. Build to the spec

- Treat every answer the user gave as a requirement.
- When the build raises a visual choice the spec does not settle, take the option closest to
  the spec and add it to the assumptions. Use decision-interview only when the choice
  changes the build materially.
- Do not add visual elements the spec does not hold: no extra hero, tiles, icons or motion.

## Step 7. Check the render before delivery

Render the finished build and compare it with the spec, slot by slot, before the user sees it.

1. Render at the canvas size: a headless browser screenshot for a page, the slide images for
   a deck, the exported image for a figure.
2. Measure what can be measured: content width, column count, font sizes, the colours in
   use, how many items the first screen holds, overflow and scrolling.
3. Look at the screenshot for what cannot be measured: where the eye lands first (emphasis)
   and whether the density reads as the spec says.
4. Fix every mismatch, then render and check that part again.

When this session cannot render the build, say in the look lines that the result was not
checked on a render. Never report a match without doing the comparison.

## Step 8. Save

Do this before the final reply, in one write.
[references/look-book.md](references/look-book.md) has the fields and the rules.

- Save one `builds` entry: what was built, the spec, which rules filled slots, what was
  asked, and the check result.
- Save or update one rule for each slot **the user chose** (a picker answer, a sample pick,
  free text, or words in the request). Scope it to this kind of output.
- Never save an assumption, a default or a value that came from a fixed look as a rule.
- A choice the user states as standing ("always", "from now on", "ทุกครั้ง") gets scope `any`.

## After delivery

When the user corrects the look ("too cramped", "the heading is too small", "แน่นไป"):

1. Fix it. Do not defend the build.
2. Save the correction as a rule in the user's words, with the measured value that fixed it.
   When a saved rule caused the problem, change that rule instead of adding a second one.

## The look lines

Put 2 to 4 lines in the chat reply that delivers the work, in the user's language:

1. The look in one or two sentences, with its main values.
2. Which slots came from saved guidance and which are assumptions, with "say if wrong".
   Leave this line out when there are none.
3. The check result: the render matches the spec, or which mismatches were fixed, or that no
   render was possible.

Write them as plain sentences. Do not start a line with a label such as "Look:", "Assumed:"
or "Check:". Example:

> The page is one 680 px column on a white ground with a teal accent, 16 px body text, and
> the diagram first.
> The canvas and the type come from your saved guidance. I assumed no motion. Say if wrong.
> I rendered it at 390 px and 1280 px and fixed one mismatch: the diagram labels were 11 px,
> below the 13 px floor.

## Managing the saved guidance

- "Show my look book", "what look did I save", `/visual-lock show`: open the Look Book page.
- "Forget X", "stop using X": retire the matching rule and say which rule in one line.
- "Reset my look": ask one picker question to confirm, then retire every active rule. Never
  delete a rule; the user deletes on the page.

## This skill has failed if

- A question was asked whose answers would not change what the user sees.
- A slot that a saved rule, a fixed look or the user's own words settled was asked again.
- A third round was asked, or a question came after the user said stop.
- A sample sheet was rendered for a choice that words had settled, or its variants differed
  in more than two slots.
- The spec holds a word such as "clean", "modern" or "compact" where a value belongs.
- The look lines report a match and no render was compared.
- An assumption or a default was saved as the user's rule.
- The user's correction was fixed and not saved.

## Not for

- **What the output should contain, what it is for, or how deep it goes.** That is
  intent-lock. When both apply, intent-lock runs first; its answers count as the user's
  words here.
- **A fork that appears mid-task and is not about the look.** That is decision-interview.
- **Writing or extracting a design-system file.** That is design-md-generator. A project
  `DESIGN.md` is a fixed look here.
- **A look that a plugin already fixes.** Office files follow clinical-minimal, concept labs
  follow concept-lab's locked shape, and clinical one-pagers follow clinical-infographic's
  design system. This skill asks only what those leave open.
- **Reviewing a finished design.** That is a design review, not an interview.
- **Text-only output.** A chat answer, a markdown note or code has no look to lock.
