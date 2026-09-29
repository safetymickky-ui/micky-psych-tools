# Changelog

## 0.1.0 — 2026-09-29

- **First release.** One skill, `vi-stock-screen-research`, with two modes, plus
  `/vi-screen` and `/vi-research`.
- **Screen — quality at a fair price** on TradingView: ROIC ≥ 12%, Piotroski F-score ≥ 6,
  Altman Z ≥ 3, debt/equity ≤ 1, positive free-cash-flow margin, and liquidity and size
  floors set per market. Top 10 ranked by ROIC rank + earnings-yield rank; the user picks
  one ticker. A separate finance screen covers banks and insurers.
- **Deep research — a full company review**: Verdict · Business · Industry · Moat ·
  Management · 10-year financials · Valuation · Risks · Sell triggers, as a multi-page Word
  report plus an Excel valuation model (Summary · Inputs · Financials · DCF · Multiples ·
  Sensitivity), both built through clinical-minimal.
- **Data order**: TradingView → Jitta in the user's Chrome when TradingView returns fewer
  than 8 fiscal years → 56-1 One Report or 10-K for governance. Every number is
  source-tagged.
- **intent-lock runs first in both modes** (explicit opt-out only).
- **TradingView MCP** bundled in `.mcp.json`.
