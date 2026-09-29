# Report contract — what the two files must hold

Rules for every section:

- Every number carries a source tag: `[TV]`, `[Jitta]`, `[56-1]`, `[10-K]`, `[AR]`, or
  `[calc]` for a figure computed here from tagged inputs.
- A section the data leaves thin says so in one sentence. No section is dropped.
- Anything no document states is marked "my inference".
- No buy or sell instruction anywhere. The Verdict states where the price sits; the
  decision stays with the user.

## TradingView columns to pull for one company

Pull these with `mcp-tv-get-symbol-data` (or the batch tool), next to the annual history
from `mcp-tv-get-financial-history`:

`close`, `market_cap_basic`, `enterprise_value_current`, `net_debt_fq`, `total_debt_fy`,
`total_equity_fq`, `goodwill_fq`, `current_ratio_fq`, `total_debt_to_ebitda_fy`,
`effective_interest_rate_on_debt_fy`, `cash_f_operating_activities_ttm`,
`neg_capital_expenditures_ttm`, `free_cash_flow_fy`, `gross_margin_fy`,
`operating_margin_fy`, `net_margin_fy`, `return_on_invested_capital_ttm`,
`return_on_equity_ttm`, `share_buyback_ratio_fy`, `dividend_payout_ratio_ttm`,
`cash_dividend_coverage_ratio_ttm`, `price_earnings_ttm`, `enterprise_value_to_ebit_ttm`,
`earnings_yield`, `graham_numbers_fy`, `piotroski_f_score_fy`, `altman_z_score_fy`,
`sloan_ratio_fy`.

## Word report — sections in this order

1. **Verdict** — one line, then 2–3 bullets.
   - The line: the quality of the business in one phrase; value per share for bear, base
     and bull; the current price; the margin of safety against the 30% target.
   - The bullets: the 2–3 facts that move the value range most.
2. **Business** — what the company sells, to whom, and how it makes money. Segments with
   their share of revenue and profit. Unit economics where disclosed. How the business has
   changed over the 10 years.
3. **Industry** — structure (main players, concentration), growth drivers, cyclicality,
   regulation, and the bargaining power of suppliers and customers. A peer table of 3–6
   companies from TradingView: ROIC, operating margin, net debt/EBITDA, EV/EBIT, P/E,
   dividend yield.
4. **Moat** — each claimed moat source (switching costs, network effect, cost advantage,
   licences or other intangibles, efficient scale) with its evidence: ROIC above the cost
   of capital across a full cycle, gross-margin stability, market-share trend, statements
   in filings. Give the evidence against the moat as well.
5. **Management** — who runs the company and who owns it: major shareholders, insider
   stake, share pledges `[56-1]`. The 10-year capital-allocation record: reinvestment,
   acquisitions, buybacks, dilution, dividends. Related-party transactions. Executive pay
   against results. Guidance against delivery, from transcripts where they exist. The
   auditor's opinion and any change of auditor.
6. **10-year financials** — a table by year: revenue, gross margin, operating margin, net
   income, EPS, operating cash flow, capex, free cash flow, ROIC (ROE for banks and
   insurers), net debt/EBITDA, shares outstanding, dividend per share. Below it, the
   computed checks `[calc]`:
   - 10-year CAGR of revenue, EPS and free cash flow.
   - ROIC in its worst year, and the number of years above 12%.
   - Gross and operating margin range (highest minus lowest).
   - Free cash flow / net income each year; flag when it is below 0.8 in most years.
   - Sloan ratio; interest cover (EBIT / interest expense); goodwill / equity.
   - Share count change over 10 years (dilution or buybacks).
7. **Valuation** — owner earnings; the DCF for bear, base and bull with every assumption
   and its link to the 10-year record; discount rate and terminal growth with their
   sources; the sensitivity grid; the reverse DCF; the cross-checks (EV/EBIT, earnings
   yield against the 10-year government bond yield, Graham number, Jitta Line labelled as
   Jitta's model); the margin of safety.
8. **Risks** — business, industry, balance-sheet, governance and valuation risks. Each
   risk names the observation that would show it is happening.
9. **Sell triggers** — observable conditions that would break the thesis or make the price
   too high, each with the number to watch. Examples of the form: ROIC below a stated
   level for two years; net debt/EBITDA above a stated level; owners pledging more shares;
   price above the bull-case value.
10. **Sources** — every document and data source, with its date.
11. **Data gaps** — what could not be found, and which section it weakens.

## Banks and insurers — what changes

- ROIC → ROE. The free-cash-flow DCF → P/B against ROE (justified P/B = (ROE − g) / (r − g),
  where r is the cost of equity and g the long-run growth) plus a dividend discount model.
- Add from the 56-1 or 10-K: NPL ratio, coverage ratio, cost of credit, and CET1 or the
  capital adequacy ratio for banks; combined ratio and solvency ratio for insurers.

## Excel model — tabs

- **Summary** — value per share for bear, base and bull; price; margin of safety; the key
  assumptions.
- **Inputs** — every assumption in one place (growth by stage, margins, capex, discount
  rate, terminal growth, share count), each with its source or reason.
- **Financials** — the 10-year table with source tags.
- **DCF** — three scenarios, every cell a formula from Inputs.
- **Multiples** — EV/EBIT, P/E, P/B, earnings yield against the bond yield, and the peer
  table.
- **Sensitivity** — value per share for discount rate ±2 points against terminal growth
  ±1 point, as formulas.

## Charts

- At least: revenue, net income and free cash flow over 10 years; ROIC by year.
- Titles state the finding, not the variable.
- Long category names go on the y-axis (horizontal bars). No legend that only repeats the
  axis title.
- Embed PNG in the Word report; save PNG and an editable SVG beside the files.
