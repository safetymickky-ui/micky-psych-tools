---
name: vi-stock-screen-research
description: >-
  Screens stocks for value investing (VI) on TradingView and writes a full company review
  of the one stock the user picks — business, industry, moat, management, 10 years of
  financials, valuation with margin of safety, risks and sell triggers — as a multi-page
  Word report plus an Excel valuation model in the Clinical Minimal style. Thai SET and US
  stocks. Use when the user says "screen stocks", "VI screen", "value stock screen",
  "หาหุ้น VI", "สกรีนหุ้น", "deep research on this stock", "research this stock",
  "company review", "วิเคราะห์หุ้น", "value this company", or runs /vi-screen or
  /vi-research. Runs intent-lock FIRST in both modes — explicit opt-out only. Data order:
  TradingView, then Jitta in the user's Chrome when TradingView has fewer than 8 years,
  then the 56-1 One Report or 10-K for governance. NOT for: technical analysis, chart
  patterns or short-term trading; crypto, forex or options; a one-line price or ratio
  lookup; portfolio allocation or position sizing.
---

# VI stock screen and company review

Two modes. **Screen** finds quality companies at a fair price and stops at a ranked table;
the user picks one ticker. **Deep research** writes a full company review of that one
stock. Both run on TradingView data first. The deep-research deliverable is two Office
files in the Clinical Minimal style: a multi-page Word report and an Excel valuation
model. Chat gets a short close, not the report.

## Prime directive — a full company review, never just a valuation

The failure this skill exists to prevent is **silent narrowing**: a "deep research" that
quietly becomes a DCF with a few lines of business description. The report covers the
whole company — business, industry, moat, management, ten years of numbers, valuation,
risks, sell triggers — and each section is written at real depth. A section the data
leaves thin is written thin *and says so* in one sentence; it is never dropped silently.

Two more rules hold in every run:

- **Every number carries a source tag**: `[TV]` TradingView, `[Jitta]`, `[56-1]`,
  `[10-K]`, `[AR]` annual report, `[calc]` computed here from tagged inputs. A number with
  no source is not written.
- **The decision stays with the user.** The report shows where the price sits against the
  value range and the margin-of-safety target. It never tells the user to buy or sell.

## Step 0 — Run intent-lock first (both modes, before any data call)

Every screen and every deep research routes through `intent-lock` FIRST. The frame is
already fixed by this skill (screen = quality at a fair price; deep research = full
company review), so the interview does not reopen the frame. It locks what still varies:

- **Screen:** the market (SET or US); universe limits (sectors in or out, SET50 or SET100
  only, size); any threshold the user wants changed from
  [references/screen-criteria.md](references/screen-criteria.md).
- **Deep research:** the ticker and market; the user's own question about this stock
  (why it is on the table); which sections carry the most depth; explicit exclusions.

**The only bypass is an explicit opt-out** — "just run it" / "don't interview me" /
"ไม่ต้องถาม" — in the user's own words, never inferred. On opt-out, the screen uses the SET
market and the default thresholds, and deep research uses balanced depth across all
sections. A missing ticker or market is still asked for; that one question is not an
interview.

## Tools and failures

The TradingView MCP server ships in this plugin's `.mcp.json` (key `tradingview`). If the
user's own TradingView connector is also connected, use whichever responds; the tool base
names are the same (`mcp-tv-run-screener`, `mcp-tv-get-financial-history`, …).
TradingView MCP needs a paid Essential plan or higher. Its prices are delayed, which does
not matter for this work.

- **HTTP 429** means TradingView is rate-limiting. Wait about 60 seconds, retry once, then
  move to the next source. Never loop.
- Use `mcp-tv-get-symbol-data-batch` for several symbols in one call.
- **Plan, access or connection error:** say in one line which data is missing and
  continue with the next source. The screen cannot run without TradingView; say so and
  stop.

## Mode A — Screen (quality at a fair price)

1. After Step 0, confirm any column you are unsure of with `mcp-tv-get-screener-columns`
   (`search` parameter).
2. Run `mcp-tv-run-screener` with the filters, columns and market in
   [references/screen-criteria.md](references/screen-criteria.md). Banks, insurers and
   finance companies fail the ROIC, Altman Z and debt filters by design; they get the
   separate finance screen described there.
3. Rank the survivors as the reference says (ROIC rank + earnings-yield rank, lowest sum
   first). Show the top 10 as one table. Flag rows, never remove them, for the conditions
   under "Flags" in the reference. Say once that the thresholds are common value-investing
   conventions, not cut-offs proven by research.
4. **Stop at the table.** The user picks one ticker for deep research. Never start deep
   research on a name the user has not picked.
5. Offer once to save the list as a TradingView watchlist named `VI screen YYYY-MM-DD`.
   Create it with `mcp-watchlist-create-watchlist` only on a yes, because it changes the
   user's TradingView account.

## Mode B — Deep research (one company)

### B1. Gather the data, in this source order

1. **TradingView**
   - `mcp-tv-search-symbols` to resolve the symbol (`SET:XXXX`, `NASDAQ:XXXX`,
     `NYSE:XXXX`).
   - `mcp-tv-get-financial-history` with `period: "fy"` and `date_from` at least 11 years
     back, for the annual statements. Count the fiscal years returned.
   - `mcp-tv-get-financials` (`ttm` and `fy`) and `mcp-tv-get-symbol-data` for the
     balance-sheet, cash-flow and valuation columns listed in
     [references/report-contract.md](references/report-contract.md).
   - `mcp-tv-get-documents` and `mcp-tv-get-document-view` for annual reports and
     earnings-call transcripts (coverage is mostly US).
   - `mcp-tv-get-news` with `lang: "th"` for SET names and `en` for US names.
   - Peers: `mcp-tv-run-screener` on the same sector and industry (3–6 names) for the
     Industry section's peer table.
   - `mcp-tv-get-forecasts` only as a sanity check on growth assumptions, never as the
     valuation.
2. **Jitta**, when TradingView returns fewer than 8 fiscal years or fails.
   - Use the user's Chrome through Claude in Chrome; read the `chrome-browser` skill first
     if it is listed. Open jitta.com.
   - If Jitta is not signed in, ask the user to sign in. Never type a password.
   - Read the 10-year revenue, net profit, margins, ROE, debt and dividends, plus Jitta
     Score and Jitta Line. Tag Jitta Line as Jitta's own model output, never as a fact.
   - No browser tool available: ask the user to attach screenshots or the numbers.
3. **56-1 One Report (SET) or 10-K (US)**, always, for what the data feeds lack: major
   shareholders and share pledges, related-party transactions, board and management,
   executive pay, segments, the auditor's opinion. Fetch it from set.or.th, the company's
   investor-relations page or SEC EDGAR with WebFetch, or ask the user to attach it.

Save everything you pull to data files (JSON or CSV) as you go. Every figure in the report
is computed from these files in code, never estimated in prose.

### B2. Analyze

Work through the per-section checklist in
[references/report-contract.md](references/report-contract.md). In short: durability
(10-year growth, ROIC each year and in its worst year, margin range), cash quality (free
cash flow against net income, Sloan ratio), balance sheet (net debt/EBITDA, interest
cover, goodwill/equity), shareholder treatment (share count over 10 years, dividends,
capital raises), moat evidence, management's record, red flags. Mark anything that no
document states as "my inference".

### B3. Value

- **Owner earnings** ≈ operating cash flow − maintenance capex. When maintenance capex is
  not disclosed, use total capex and say so.
- **DCF in three scenarios** (bear / base / bull). State every assumption and tie it to
  the 10-year record. Terminal growth never exceeds the long-run nominal GDP growth of the
  company's main market; state the number and its source.
- **Discount rate:** state it and why. Show a sensitivity grid: discount rate ±2 points
  against terminal growth ±1 point.
- **Reverse DCF:** the growth rate the current price implies.
- **Cross-checks:** EV/EBIT; earnings yield against the market's current 10-year
  government bond yield (look it up, never from memory); Graham number; Jitta Line when
  available.
- **Margin of safety** = (base-case value − price) / base-case value. The default target
  is 30%. Report where the price sits against the bear/base/bull range and the target.
- **Banks and insurers:** value on P/B against ROE and on dividends, not on a free-cash-flow
  DCF (see the report contract).

### B4. Build the files with Clinical Minimal

Load the `clinical-minimal` skill before building. It decides how the files look; this
skill decides what they say. If `clinical-minimal` is not available, say so and ask
before building plain files.

- **Word report**, multi-page, sections in this order: Verdict · Business · Industry ·
  Moat · Management · 10-year financials · Valuation · Risks · Sell triggers, then
  Sources and Data gaps. What each section must hold is in
  [references/report-contract.md](references/report-contract.md).
- **Excel model**, tabs Summary · Inputs · Financials · DCF · Multiples · Sensitivity.
  The DCF and Sensitivity tabs run on live formulas from Inputs, so the user can change an
  assumption and watch the value move.
- **File names:** `<TICKER>-company-review-<YYYY-MM-DD>.docx` and
  `<TICKER>-valuation-model-<YYYY-MM-DD>.xlsx`, saved in the working folder or the
  folder the user names. Charts are also saved beside them as PNG and SVG.
- **Language:** English by default (a Clinical Minimal rule); Thai only when the user
  asks.
- Run the Clinical Minimal render check. It needs Microsoft Office on Windows; where it
  cannot run, say in one line that the files were built but not render-checked.

### B5. Close in chat

Chat gets the Verdict line, the two file paths, and the data gaps as one short list. Not
the report itself.

## Boundaries

- **Technical analysis**, chart patterns, indicators and short-term trading signals are
  out of scope.
- **Crypto, forex, options** and other derivatives are out of scope.
- **A one-line quote, price or ratio lookup** is answered directly, without this skill.
- **Portfolio allocation and position sizing** are out of scope.
- **Non-value screens** (momentum, technical ratings) are out of scope.
