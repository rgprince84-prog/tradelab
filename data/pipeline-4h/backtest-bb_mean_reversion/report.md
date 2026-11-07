# bb_mean_reversion 4h

**Parameters:** period=20, std=2.0, adx_max=20, sl_atr_buffer=0.5, max_bars=30

**Costs modelled:** spread per instrument (config), slippage 0.2 pips/pts per side, commission 0.0 GBP/round trip, same-bar SL+TP → pessimistic.  
**Sizing:** 1.0% of GBP 10,000 per trade, fixed.

## Headline

| Metric | Value |
|---|---|
| Trades | 829 |
| Win rate | 51.3% |
| Expectancy (R) | -0.019 |
| Profit factor | 0.963 |
| Payoff ratio | 0.916 |
| Total R | -15.411 |
| Return % | -15.411 |
| Max drawdown (R) | 58.941 |
| Max drawdown % | 58.941 |
| Sharpe (daily) | -0.127 |
| t-stat of mean R | -0.468 |
| Avg bars held | 4.086 |
| Max consecutive losses | 11 |
| Trades / month | 24.334 |
| First trade | 2024-01-04 |
| Last trade | 2026-11-06 |

![equity](equity.png)

![R distribution](r_distribution.png)

## By instrument

| instrument | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| AUDUSD | 66 | 0.545 | 0.075 | 4.950 | 7.613 |
| EURGBP | 68 | 0.471 | -0.166 | -11.277 | 15.849 |
| EURJPY | 80 | 0.388 | -0.341 | -27.296 | 29.860 |
| EURUSD | 61 | 0.475 | -0.050 | -3.033 | 12.397 |
| GBPJPY | 92 | 0.576 | 0.097 | 8.917 | 7.045 |
| GBPUSD | 73 | 0.521 | 0.093 | 6.808 | 8.658 |
| GER40 | 43 | 0.535 | 0.038 | 1.644 | 7.105 |
| JPN225 | 27 | 0.444 | -0.292 | -7.872 | 9.688 |
| NAS100 | 18 | 0.556 | -0.004 | -0.079 | 5.109 |
| SPX500 | 26 | 0.577 | 0.256 | 6.664 | 7.520 |
| UK100 | 49 | 0.531 | 0.046 | 2.251 | 6.781 |
| US30 | 33 | 0.545 | 0.072 | 2.376 | 7.058 |
| USDCAD | 55 | 0.564 | -0.007 | -0.369 | 6.086 |
| USDCHF | 76 | 0.566 | 0.125 | 9.477 | 6.788 |
| USDJPY | 62 | 0.452 | -0.138 | -8.572 | 14.412 |

## By year

| year | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| 2024 | 268 | 0.515 | 0.018 | 4.916 | 20.206 |
| 2025 | 307 | 0.479 | -0.118 | -36.111 | 46.416 |
| 2026 | 254 | 0.551 | 0.062 | 15.784 | 13.370 |

## By direction

| direction | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| long | 358 | 0.587 | 0.050 | 17.980 | 19.223 |
| short | 471 | 0.456 | -0.071 | -33.391 | 53.871 |

## By exit reason

| exit_reason | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| open_at_end | 1 | 1.000 | 0.055 | 0.055 | 0.000 |
| stop | 399 | 0.000 | -1.052 | -419.6 | 419.6 |
| target | 422 | 0.995 | 0.953 | 402.2 | 0.027 |
| time | 7 | 0.571 | 0.277 | 1.940 | 0.717 |

## By entry hour (UTC)

| entry_hour_utc | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| 0 | 145 | 0.400 | -0.093 | -13.552 | 28.308 |
| 4 | 136 | 0.507 | -0.039 | -5.280 | 17.538 |
| 8 | 112 | 0.616 | 0.216 | 24.170 | 7.141 |
| 12 | 138 | 0.471 | -0.125 | -17.187 | 30.435 |
| 16 | 149 | 0.537 | -0.105 | -15.665 | 22.818 |
| 20 | 149 | 0.564 | 0.081 | 12.103 | 17.010 |

## Monte Carlo (1000 runs)

| | p50 | p95 |
|---|---|---|
| Max drawdown, shuffled order (R) | 42.0 | 61.9 |
| Max drawdown, bootstrap (R) | 43.6 | 85.7 |

Bootstrap total R: p5 -70.1, p50 -16.2, p95 +42.4. Probability the edge is actually negative: **67%**.

---

_Backtests use mid/bid prices from free feeds, one position per instrument, no overnight financing, no margin limits. They are research, not a forecast and not advice._