# bb_mean_reversion 1h

**Parameters:** period=20, std=2.0, adx_max=20, sl_atr_buffer=0.5, max_bars=30

**Costs modelled:** spread per instrument (config), slippage 0.2 pips/pts per side, commission 0.0 GBP/round trip, same-bar SL+TP → pessimistic.  
**Sizing:** 1.0% of GBP 10,000 per trade, fixed.

## Headline

| Metric | Value |
|---|---|
| Trades | 3,000 |
| Win rate | 53.6% |
| Expectancy (R) | -0.084 |
| Profit factor | 0.829 |
| Payoff ratio | 0.719 |
| Total R | -253.2 |
| Return % | -253.2 |
| Max drawdown (R) | 259.6 |
| Max drawdown % | 259.6 |
| Sharpe (daily) | -2.211 |
| t-stat of mean R | -4.236 |
| Avg bars held | 4.273 |
| Max consecutive losses | 15 |
| Trades / month | 86.971 |
| First trade | 2024-01-05 |
| Last trade | 2026-11-20 |

> Return below -100%: with fixed-size risk this strategy would have emptied the account. Read the R figures; the % is just arithmetic.

![equity](equity.png)

![R distribution](r_distribution.png)

## By instrument

| instrument | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| AUDUSD | 300 | 0.503 | -0.147 | -44.044 | 48.165 |
| EURGBP | 287 | 0.624 | 0.019 | 5.445 | 13.749 |
| EURJPY | 282 | 0.546 | -0.032 | -9.133 | 25.934 |
| EURUSD | 286 | 0.483 | -0.149 | -42.546 | 47.130 |
| GBPJPY | 313 | 0.569 | -0.046 | -14.434 | 30.566 |
| GBPUSD | 279 | 0.520 | -0.047 | -12.979 | 35.851 |
| GER40 | 91 | 0.385 | -0.310 | -28.213 | 31.943 |
| JPN225 | 37 | 0.351 | -0.313 | -11.579 | 13.061 |
| NAS100 | 51 | 0.451 | -0.334 | -17.055 | 20.180 |
| SPX500 | 48 | 0.458 | -0.295 | -14.147 | 16.928 |
| UK100 | 82 | 0.512 | -0.004 | -0.316 | 13.986 |
| US30 | 74 | 0.419 | -0.165 | -12.210 | 18.922 |
| USDCAD | 275 | 0.611 | -0.039 | -10.779 | 21.404 |
| USDCHF | 326 | 0.583 | -0.065 | -21.052 | 28.316 |
| USDJPY | 269 | 0.513 | -0.075 | -20.137 | 25.747 |

## By year

| year | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| 2024 | 1,027 | 0.547 | -0.095 | -97.075 | 101.7 |
| 2025 | 1,065 | 0.529 | -0.087 | -92.349 | 114.5 |
| 2026 | 908 | 0.531 | -0.070 | -63.754 | 80.795 |

## By direction

| direction | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| long | 1,340 | 0.551 | -0.072 | -97.100 | 105.8 |
| short | 1,660 | 0.523 | -0.094 | -156.1 | 182.4 |

## By exit reason

| exit_reason | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| open_at_end | 1 | 0.000 | -0.034 | -0.034 | 0.034 |
| stop | 1,358 | 0.000 | -1.090 | -1,480.7 | 1,480.7 |
| target | 1,626 | 0.982 | 0.753 | 1,224.4 | 0.068 |
| time | 15 | 0.667 | 0.212 | 3.180 | 0.688 |

## By entry hour (UTC)

| entry_hour_utc | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| 0 | 26 | 0.654 | -0.006 | -0.160 | 3.145 |
| 1 | 33 | 0.606 | -0.010 | -0.325 | 4.522 |
| 2 | 75 | 0.560 | -0.044 | -3.333 | 13.645 |
| 3 | 109 | 0.495 | -0.119 | -13.023 | 21.039 |
| 4 | 84 | 0.452 | -0.171 | -14.342 | 18.214 |
| 5 | 59 | 0.356 | -0.292 | -17.243 | 23.798 |
| 6 | 72 | 0.472 | -0.049 | -3.495 | 14.407 |
| 7 | 92 | 0.511 | -0.182 | -16.750 | 20.636 |
| 8 | 107 | 0.598 | -0.084 | -8.963 | 20.394 |
| 9 | 173 | 0.618 | -0.041 | -7.155 | 13.029 |
| 10 | 206 | 0.544 | -0.107 | -21.973 | 29.818 |
| 11 | 213 | 0.521 | -0.131 | -27.998 | 38.312 |
| 12 | 188 | 0.521 | -0.029 | -5.438 | 24.035 |
| 13 | 159 | 0.541 | -0.130 | -20.609 | 25.988 |
| 14 | 203 | 0.581 | -0.112 | -22.770 | 32.379 |
| 15 | 230 | 0.583 | -0.054 | -12.307 | 16.433 |
| 16 | 226 | 0.544 | -0.138 | -31.296 | 38.904 |
| 17 | 234 | 0.538 | -0.049 | -11.480 | 25.631 |
| 18 | 159 | 0.491 | -0.180 | -28.644 | 41.162 |
| 19 | 119 | 0.496 | -0.058 | -6.913 | 12.757 |
| 20 | 81 | 0.605 | 0.179 | 14.474 | 6.528 |
| 21 | 78 | 0.449 | 0.028 | 2.184 | 11.615 |
| 22 | 48 | 0.396 | 0.073 | 3.490 | 9.836 |
| 23 | 26 | 0.577 | 0.034 | 0.889 | 4.979 |

## Monte Carlo (1000 runs)

| | p50 | p95 |
|---|---|---|
| Max drawdown, shuffled order (R) | 264.2 | 285.5 |
| Max drawdown, bootstrap (R) | 264.3 | 367.0 |

Bootstrap total R: p5 -357.9, p50 -251.4, p95 -154.2. Probability the edge is actually negative: **100%**.

---

_Backtests use mid/bid prices from free feeds, one position per instrument, no overnight financing, no margin limits. They are research, not a forecast and not advice._