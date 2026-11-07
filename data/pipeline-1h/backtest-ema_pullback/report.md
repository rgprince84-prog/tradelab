# ema_pullback 1h

**Parameters:** ema_fast=20, ema_mid=50, ema_slow=200, pullback_bars=3, rsi_max=70, sl_atr_buffer=0.5, rr=2.0, max_bars=48

**Costs modelled:** spread per instrument (config), slippage 0.2 pips/pts per side, commission 0.0 GBP/round trip, same-bar SL+TP → pessimistic.  
**Sizing:** 1.0% of GBP 10,000 per trade, fixed.

## Headline

| Metric | Value |
|---|---|
| Trades | 4,879 |
| Win rate | 34.9% |
| Expectancy (R) | -0.101 |
| Profit factor | 0.845 |
| Payoff ratio | 1.578 |
| Total R | -492.6 |
| Return % | -492.6 |
| Max drawdown (R) | 503.9 |
| Max drawdown % | 503.9 |
| Sharpe (daily) | -2.441 |
| t-stat of mean R | -5.420 |
| Avg bars held | 20.192 |
| Max consecutive losses | 27 |
| Trades / month | 143.4 |
| First trade | 2024-01-05 |
| Last trade | 2026-11-06 |

> Return below -100%: with fixed-size risk this strategy would have emptied the account. Read the R figures; the % is just arithmetic.

![equity](equity.png)

![R distribution](r_distribution.png)

## By instrument

| instrument | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| AUDUSD | 479 | 0.342 | -0.111 | -53.296 | 57.776 |
| EURGBP | 447 | 0.304 | -0.231 | -103.3 | 119.1 |
| EURJPY | 444 | 0.347 | -0.107 | -47.587 | 49.756 |
| EURUSD | 473 | 0.362 | -0.047 | -22.291 | 34.314 |
| GBPJPY | 450 | 0.336 | -0.118 | -52.948 | 65.462 |
| GBPUSD | 465 | 0.340 | -0.141 | -65.527 | 69.343 |
| GER40 | 164 | 0.348 | -0.071 | -11.596 | 21.563 |
| JPN225 | 111 | 0.432 | 0.180 | 19.990 | 8.131 |
| NAS100 | 123 | 0.382 | -0.041 | -5.084 | 12.900 |
| SPX500 | 132 | 0.386 | -0.018 | -2.350 | 14.393 |
| UK100 | 186 | 0.355 | -0.004 | -0.748 | 20.425 |
| US30 | 129 | 0.333 | -0.131 | -16.956 | 19.683 |
| USDCAD | 398 | 0.397 | -0.008 | -3.057 | 44.377 |
| USDCHF | 442 | 0.321 | -0.198 | -87.388 | 95.486 |
| USDJPY | 436 | 0.356 | -0.093 | -40.408 | 46.222 |

## By year

| year | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| 2024 | 1,675 | 0.355 | -0.091 | -151.7 | 191.3 |
| 2025 | 1,715 | 0.341 | -0.103 | -177.3 | 180.6 |
| 2026 | 1,489 | 0.351 | -0.110 | -163.6 | 200.2 |

## By direction

| direction | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| long | 2,823 | 0.365 | -0.067 | -189.8 | 199.1 |
| short | 2,056 | 0.326 | -0.147 | -302.8 | 329.2 |

## By exit reason

| exit_reason | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| open_at_end | 3 | 0.667 | 0.176 | 0.527 | 0.476 |
| stop | 2,945 | 0.000 | -1.050 | -3,091.9 | 3,091.9 |
| target | 1,148 | 1.000 | 1.987 | 2,281.4 | 0.000 |
| time | 783 | 0.704 | 0.405 | 317.3 | 2.335 |

## By entry hour (UTC)

| entry_hour_utc | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| 0 | 145 | 0.359 | -0.013 | -1.927 | 17.397 |
| 1 | 270 | 0.415 | 0.083 | 22.418 | 14.469 |
| 2 | 163 | 0.344 | -0.092 | -15.033 | 32.832 |
| 3 | 137 | 0.307 | -0.215 | -29.497 | 32.090 |
| 4 | 145 | 0.303 | -0.170 | -24.603 | 34.222 |
| 5 | 127 | 0.394 | 0.092 | 11.730 | 10.946 |
| 6 | 154 | 0.312 | -0.149 | -22.948 | 32.480 |
| 7 | 212 | 0.358 | -0.004 | -0.931 | 20.617 |
| 8 | 351 | 0.311 | -0.187 | -65.713 | 66.639 |
| 9 | 269 | 0.279 | -0.287 | -77.173 | 77.173 |
| 10 | 218 | 0.381 | -0.012 | -2.570 | 18.489 |
| 11 | 183 | 0.317 | -0.158 | -28.902 | 40.367 |
| 12 | 227 | 0.348 | -0.110 | -24.911 | 25.570 |
| 13 | 312 | 0.426 | 0.036 | 11.118 | 28.125 |
| 14 | 392 | 0.355 | -0.116 | -45.587 | 57.210 |
| 15 | 408 | 0.370 | -0.091 | -37.117 | 53.848 |
| 16 | 284 | 0.405 | -0.021 | -5.983 | 35.788 |
| 17 | 190 | 0.368 | -0.095 | -18.131 | 26.396 |
| 18 | 182 | 0.341 | -0.071 | -12.875 | 35.327 |
| 19 | 180 | 0.317 | -0.153 | -27.588 | 40.349 |
| 20 | 133 | 0.293 | -0.261 | -34.682 | 50.434 |
| 21 | 95 | 0.232 | -0.414 | -39.348 | 40.209 |
| 22 | 48 | 0.292 | -0.198 | -9.516 | 12.026 |
| 23 | 54 | 0.278 | -0.237 | -12.808 | 17.618 |

## Monte Carlo (1000 runs)

| | p50 | p95 |
|---|---|---|
| Max drawdown, shuffled order (R) | 505.2 | 530.5 |
| Max drawdown, bootstrap (R) | 504.4 | 651.0 |

Bootstrap total R: p5 -640.3, p50 -489.4, p95 -341.2. Probability the edge is actually negative: **100%**.

---

_Backtests use mid/bid prices from free feeds, one position per instrument, no overnight financing, no margin limits. They are research, not a forecast and not advice._