---
description: Run a value-investing stock screen on TradingView (SET or US) and return a ranked top-10 table
argument-hint: [SET | US, optional limits]
---

Run the `vi-stock-screen-research` skill now, in **screen** mode.

- `$ARGUMENTS` names the market or limits (e.g. `/vi-screen SET`, `/vi-screen US no
  banks`) → seed the Step 0 interview with it.
- `$ARGUMENTS` empty → the interview asks for the market.

The skill owns the whole procedure — intent-lock gate → TradingView screen → ranked top 10
→ stop for the user's pick. This command is only the manual trigger for it.
