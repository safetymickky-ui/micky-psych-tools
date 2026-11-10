---
description: Interview me on how a visual build should look before it is built, or show and manage my saved look guidance
argument-hint: [what to build | show | forget <rule> | reset]
---

Run the `visual-lock` skill now.

- `$ARGUMENTS` names something to build (`/visual-lock a one-page summary of the lithium
  review`) → run the look interview for that build, then build it.
- `$ARGUMENTS` is empty and a visual build is under way or was just asked for → run the look
  interview for that build.
- `$ARGUMENTS` is empty and there is nothing to build → ask in one line what to build, and stop.
- `$ARGUMENTS` is `show` → find the Look Book page and open it.
- `$ARGUMENTS` is `forget <words>` → retire the saved rule that matches, and say which one.
- `$ARGUMENTS` is `reset` → ask one picker question to confirm, then retire every active rule.

The skill owns the whole procedure: load the saved guidance → draft the look spec → picker
questions in words → one sample sheet only when words cannot settle a choice → lock → build
→ check the render → save the choices to the Look Book. This command is only the manual trigger.
