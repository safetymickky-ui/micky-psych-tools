# Screen criteria — quality at a fair price

These are the defaults. The user may change any of them in the Step 0 interview. They are
common value-investing conventions, not cut-offs proven by research; the screen output
says so once.

Column names were checked against `mcp-tv-get-screener-columns` in September 2026.
Confirm any column you are unsure of with its `search` parameter before a run.

## Market

- `market`: `thailand` for SET (symbols `SET:XXXX`) or `america` for US (`NASDAQ:` /
  `NYSE:`).
- `symbol_types: ["stock"]`.

## Filters — main screen

| Group | Column | Rule |
| --- | --- | --- |
| Quality | `return_on_invested_capital_ttm` | ≥ 12 |
| Quality | `piotroski_f_score_fy` | ≥ 6 |
| Quality | `free_cash_flow_margin_fy` | > 0 |
| Safety | `altman_z_score_fy` | ≥ 3 |
| Safety | `debt_to_equity_fq` | ≤ 1 |
| Liquidity | `AvgValue.Traded_10d` | SET ≥ 10,000,000 THB; US ≥ 5,000,000 USD |
| Size | `market_cap_basic` | SET ≥ 5,000,000,000 THB; US ≥ 1,000,000,000 USD |

The liquidity floor keeps names where a position can be built and sold. The size floor
is set per market, because the same number in local currency means a very different
company size in THB and in USD.

## Filters — finance screen (banks, insurers, finance companies)

ROIC, Altman Z and debt-to-equity do not apply to lenders and insurers, so they fail the
main screen by design. Run this screen separately when the user wants them:

| Column | Rule |
| --- | --- |
| `sector` | Finance |
| `return_on_equity_ttm` | ≥ 12 |
| `price_book_fq` | ≤ 1.5 |
| Liquidity and size | as in the main screen |

Rank by ROE and earnings yield the same way as below. Flag in the table that asset quality
(NPL ratio, coverage ratio) and capital ratios must come from the 56-1 One Report or
10-K.

## Columns to return

`description`, `sector`, `close`, `market_cap_basic`, `return_on_invested_capital_ttm`,
`piotroski_f_score_fy`, `altman_z_score_fy`, `debt_to_equity_fq`, `earnings_yield`,
`enterprise_value_to_ebit_ttm`, `price_free_cash_flow_ttm`, `price_book_fq`,
`dividends_yield`, `graham_numbers_fy`, `sloan_ratio_fy`, `continuous_dividend_growth`.

## Ranking

1. Rank the survivors by `earnings_yield`, highest first (high = cheap).
2. Rank them by `return_on_invested_capital_ttm`, highest first (high = good).
3. Add the two ranks. Sort by the sum, lowest first. Show the top 10.

## Flags — mark the row, never remove it

- `sloan_ratio_fy` > 0.10: earnings lean on accruals rather than cash.
- `close` above `graham_numbers_fy`: priced above the Graham number.
