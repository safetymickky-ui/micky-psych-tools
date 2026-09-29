# vi-stock-screen-research

Value-investing (VI) stock work for Thai SET and US stocks, in two modes:

- **Screen** — finds quality companies at a fair price on TradingView and stops at a ranked
  top-10 table. You pick one ticker.
- **Deep research** — writes a full company review of that one stock: a multi-page Word
  report and an Excel valuation model, both in the Clinical Minimal style. Chat gets the
  Verdict line, the file paths and the data gaps, not the report.

## Components

- **`vi-stock-screen-research` skill** — the whole procedure for both modes: intent-lock
  gate → data (TradingView → Jitta → 56-1 / 10-K) → analysis → valuation → files.
- **`/vi-screen [SET | US, limits]`** — manual trigger for the screen.
- **`/vi-research [ticker]`** — manual trigger for deep research.

## The contracts

- **A full company review, never just a valuation.** Sections: Verdict · Business ·
  Industry · Moat · Management · 10-year financials · Valuation · Risks · Sell triggers,
  then Sources and Data gaps. A thin section says it is thin; none is dropped.
- **Every number is source-tagged**: `[TV]`, `[Jitta]`, `[56-1]`, `[10-K]`, `[AR]`,
  `[calc]`.
- **The decision stays with you.** The report shows where the price sits against the
  bear/base/bull value range and the 30% margin-of-safety target; it never says buy or
  sell.
- **intent-lock runs first in both modes.** Opt out only in your own words ("just run it",
  "ไม่ต้องถาม").

Full rules: `skills/vi-stock-screen-research/references/screen-criteria.md` and
`skills/vi-stock-screen-research/references/report-contract.md`.

## Data sources, in order

| Order | Source | Used for |
| --- | --- | --- |
| 1 | TradingView MCP | Screen, 10-year statements, ratios, peers, documents, news |
| 2 | Jitta, read in your Chrome | 10-year history when TradingView returns fewer than 8 years |
| 3 | 56-1 One Report (SET) / 10-K (US) | Shareholders and pledges, related parties, management, auditor |

## Requirements

- A TradingView plan at Essential or higher (MCP access is part of paid plans; the server
  is in public beta).
- Claude in Chrome, for the Jitta step. Without it, attach Jitta screenshots or numbers.
- The **clinical-minimal** plugin, which decides how the Word and Excel files look. Its
  render check needs Windows with Microsoft Office; elsewhere the files are built but not
  render-checked.

## MCP setup

This plugin bundles one MCP server in its own `.mcp.json`. Sign in with your TradingView
account the first time it connects (`/mcp` in Claude Code).

| Server key | Backing | Stable tool prefix |
|---|---|---|
| `tradingview` | `https://mcp.tradingview.com/mcp` | `mcp__plugin_vi-stock-screen-research_tradingview__<tool>` |

If your own TradingView connector is also connected, the skill uses whichever responds.

## Boundaries

- Technical analysis, chart patterns and short-term trading — out of scope.
- Crypto, forex, options — out of scope.
- A one-line price or ratio lookup — answered directly, without this skill.
- Portfolio allocation and position sizing — out of scope.

## Install

```
/plugin marketplace add safetymickky-ui/micky-psych-tools
/plugin install vi-stock-screen-research@micky-psych-tools
```
