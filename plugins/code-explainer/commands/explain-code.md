---
description: Explain given code as an interactive HTML page — VS Code-styled source on the left, cross-linked explanation on the right, step-through walkthrough and flow diagram
argument-hint: [pasted code, a file path, or a function/class name]
---

Run the `code-explainer` skill now.

- `$ARGUMENTS` is a file path → read that file in full and explain it.
- `$ARGUMENTS` names a function, class, or symbol → find it, confirm which one if the name
  is ambiguous, then explain that unit.
- `$ARGUMENTS` is pasted code → explain it as given.
- `$ARGUMENTS` empty → explain the code in the conversation above; if there is none, ask
  for it.

The skill owns the whole procedure — scope gate (intent-lock only when the ask has more
than one reading) → read the code in full → plan the annotated ranges and the
execution-order steps → build the self-contained HTML explainer (VS Code shell, linked
line↔explanation highlighting, debug-style step-through, cross-linked SVG flow diagram) →
render and verify → deliver to the working directory, vault only if asked. This command is
only the manual trigger.
