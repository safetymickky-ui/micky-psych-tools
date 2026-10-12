---
description: Start or resume a tutor track, or list your tracks with their next chunk
argument-hint: [track name, or a new topic to learn]
---

Run the `tutor` skill now.

- `$ARGUMENTS` is empty → read the Tutor tracker and list the active tracks as numbered options
  (title · next chunk id and title). He answers with a number to resume one. With no tracks
  yet, ask what he wants to learn in one picker (computational psychiatry, Python and R, neural
  networks, math and statistics notation, plus his own answer), then start intake.
- `$ARGUMENTS` names an existing track (its id or its title) → resume it at its `next` chunk.
- `$ARGUMENTS` is a new topic → intake for a new track (intent-lock first), then the first chunk.

The skill owns the whole procedure: route → load tracker and pack → teach one chunk (one-line
guess only before why/what-if ideas, answer first, computed worked example, code that really
ran) → numbered next options → save the lesson to the tracker. No quizzes. This command is only
the manual trigger.
