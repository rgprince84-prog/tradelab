# donchian_breakout 1h

**Parameters:** lookback=20, adx_min=20, sl_atr=2.0, trail_atr=2.0, rr=None, max_bars=200

**Costs modelled:** spread per instrument (config), slippage 0.2 pips/pts per side, commission 0.0 GBP/round trip, same-bar SL+TP → pessimistic.  
**Sizing:** 1.0% of GBP 10,000 per trade, fixed.

## Headline

| Metric | Value |
|---|---|
| Trades | 4,734 |
| Win rate | 32.5% |
| Expectancy (R) | -0.094 |
| Profit factor | 0.818 |
| Payoff ratio | 1.699 |
| Total R | -443.3 |
| Return % | -443.3 |
| Max drawdown (R) | 498.0 |
| Max drawdown % | 498.0 |
| Sharpe (daily) | -2.117 |
| t-stat of mean R | -5.155 |
| Avg bars held | 13.699 |
| Max consecutive losses | 29 |
| Trades / month | 136.8 |
| First trade | 2024-01-02 |
| Last trade | 2026-11-20 |

> Return below -100%: with fixed-size risk this strategy would have emptied the account. Read the R figures; the % is just arithmetic.

![equity](equity.png)

![R distribution](r_distribution.png)

## By instrument

| instrument | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| AUDUSD | 439 | 0.298 | -0.140 | -61.243 | 82.545 |
| EURGBP | 396 | 0.283 | -0.301 | -119.0 | 119.5 |
| EURJPY | 402 | 0.333 | -0.103 | -41.526 | 46.504 |
| EURUSD | 451 | 0.335 | -0.103 | -46.305 | 54.076 |
| GBPJPY | 413 | 0.334 | -0.099 | -40.920 | 45.624 |
| GBPUSD | 470 | 0.321 | -0.086 | -40.327 | 46.522 |
| GER40 | 179 | 0.363 | 0.029 | 5.258 | 23.217 |
| JPN225 | 159 | 0.352 | 0.167 | 26.490 | 8.026 |
| NAS100 | 154 | 0.344 | 0.042 | 6.490 | 15.009 |
| SPX500 | 156 | 0.340 | -0.184 | -28.640 | 33.834 |
| UK100 | 181 | 0.320 | 0.050 | 9.020 | 19.944 |
| US30 | 152 | 0.342 | -0.029 | -4.433 | 26.790 |
| USDCAD | 331 | 0.338 | -0.086 | -28.510 | 38.895 |
| USDCHF | 415 | 0.306 | -0.163 | -67.725 | 72.741 |
| USDJPY | 436 | 0.333 | -0.027 | -11.907 | 23.612 |

## By year

| year | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| 2024 | 1,556 | 0.319 | -0.087 | -135.0 | 138.3 |
| 2025 | 1,697 | 0.329 | -0.121 | -205.5 | 215.9 |
| 2026 | 1,481 | 0.326 | -0.069 | -102.8 | 188.1 |

## By direction

| direction | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| long | 2,419 | 0.335 | -0.070 | -168.4 | 182.6 |
| short | 2,315 | 0.314 | -0.119 | -274.9 | 322.4 |

## By exit reason

| exit_reason | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| open_at_end | 10 | 0.800 | 1.360 | 13.598 | 0.137 |
| stop | 1,168 | 0.000 | -1.045 | -1,220.3 | 1,220.3 |
| time | 5 | 1.000 | 3.124 | 15.622 | 0.000 |
| trail_stop | 3,551 | 0.429 | 0.211 | 747.8 | 23.413 |

## By entry hour (UTC)

| entry_hour_utc | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| 0 | 109 | 0.339 | -0.112 | -12.209 | 17.426 |
| 1 | 262 | 0.397 | 0.076 | 20.033 | 15.126 |
| 2 | 128 | 0.352 | 0.067 | 8.572 | 14.856 |
| 3 | 99 | 0.253 | -0.104 | -10.321 | 19.232 |
| 4 | 105 | 0.343 | -0.059 | -6.152 | 21.864 |
| 5 | 104 | 0.202 | -0.450 | -46.835 | 49.512 |
| 6 | 110 | 0.345 | 0.026 | 2.811 | 12.930 |
| 7 | 159 | 0.340 | -0.084 | -13.296 | 25.355 |
| 8 | 317 | 0.341 | -0.030 | -9.524 | 34.915 |
| 9 | 267 | 0.337 | -0.066 | -17.750 | 42.144 |
| 10 | 213 | 0.300 | -0.193 | -41.007 | 44.131 |
| 11 | 186 | 0.323 | -0.150 | -27.965 | 39.948 |
| 12 | 209 | 0.254 | -0.236 | -49.330 | 64.261 |
| 13 | 404 | 0.309 | -0.141 | -56.826 | 70.462 |
| 14 | 503 | 0.330 | -0.036 | -18.339 | 49.609 |
| 15 | 472 | 0.362 | -0.071 | -33.346 | 52.791 |
| 16 | 269 | 0.342 | -0.065 | -17.612 | 27.199 |
| 17 | 197 | 0.360 | 0.078 | 15.363 | 24.601 |
| 18 | 161 | 0.267 | -0.163 | -26.239 | 40.358 |
| 19 | 213 | 0.244 | -0.302 | -64.330 | 65.440 |
| 20 | 102 | 0.353 | -0.042 | -4.317 | 12.636 |
| 21 | 69 | 0.304 | -0.291 | -20.110 | 20.110 |
| 22 | 41 | 0.341 | -0.156 | -6.385 | 10.454 |
| 23 | 35 | 0.343 | -0.234 | -8.181 | 9.032 |

## Monte Carlo (1000 runs)

| | p50 | p95 |
|---|---|---|
| Max drawdown, shuffled order (R) | 457.2 | 482.7 |
| Max drawdown, bootstrap (R) | 464.2 | 591.4 |

Bootstrap total R: p5 -580.0, p50 -448.6, p95 -302.0. Probability the edge is actually negative: **100%**.

---

_Backtests use mid/bid prices from free feeds, one position per instrument, no overnight financing, no margin limits. They are research, not a forecast and not advice._