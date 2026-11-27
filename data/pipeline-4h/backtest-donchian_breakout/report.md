# donchian_breakout 4h

**Parameters:** lookback=20, adx_min=20, sl_atr=2.0, trail_atr=2.0, rr=None, max_bars=200

**Costs modelled:** spread per instrument (config), slippage 0.2 pips/pts per side, commission 0.0 GBP/round trip, same-bar SL+TP → pessimistic.  
**Sizing:** 1.0% of GBP 10,000 per trade, fixed.

## Headline

| Metric | Value |
|---|---|
| Trades | 1,269 |
| Win rate | 36.1% |
| Expectancy (R) | -0.029 |
| Profit factor | 0.938 |
| Payoff ratio | 1.661 |
| Total R | -36.285 |
| Return % | -36.285 |
| Max drawdown (R) | 113.2 |
| Max drawdown % | 113.2 |
| Sharpe (daily) | -0.347 |
| t-stat of mean R | -0.843 |
| Avg bars held | 13.857 |
| Max consecutive losses | 15 |
| Trades / month | 36.476 |
| First trade | 2024-01-02 |
| Last trade | 2026-11-27 |

![equity](equity.png)

![R distribution](r_distribution.png)

## By instrument

| instrument | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| AUDUSD | 117 | 0.316 | -0.086 | -10.078 | 18.941 |
| EURGBP | 109 | 0.220 | -0.225 | -24.514 | 26.240 |
| EURJPY | 102 | 0.412 | 0.049 | 5.005 | 10.272 |
| EURUSD | 112 | 0.339 | -0.060 | -6.675 | 8.024 |
| GBPJPY | 107 | 0.374 | -0.046 | -4.954 | 19.514 |
| GBPUSD | 109 | 0.431 | 0.117 | 12.741 | 7.709 |
| GER40 | 51 | 0.412 | -0.005 | -0.246 | 13.536 |
| JPN225 | 44 | 0.386 | -0.064 | -2.799 | 12.009 |
| NAS100 | 54 | 0.296 | -0.155 | -8.352 | 11.665 |
| SPX500 | 48 | 0.312 | -0.192 | -9.224 | 14.743 |
| UK100 | 49 | 0.531 | 0.130 | 6.374 | 4.132 |
| US30 | 43 | 0.488 | 0.105 | 4.521 | 6.665 |
| USDCAD | 109 | 0.312 | -0.019 | -2.066 | 17.685 |
| USDCHF | 108 | 0.361 | -0.010 | -1.042 | 18.291 |
| USDJPY | 107 | 0.383 | 0.047 | 5.025 | 14.332 |

## By year

| year | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| 2024 | 414 | 0.394 | 0.129 | 53.423 | 27.457 |
| 2025 | 446 | 0.345 | -0.136 | -60.726 | 65.559 |
| 2026 | 409 | 0.345 | -0.071 | -28.983 | 58.531 |

## By direction

| direction | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| long | 651 | 0.392 | 0.014 | 9.245 | 30.691 |
| short | 618 | 0.328 | -0.074 | -45.531 | 92.991 |

## By exit reason

| exit_reason | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| open_at_end | 2 | 1.000 | 0.267 | 0.534 | 0.000 |
| stop | 252 | 0.000 | -1.024 | -258.1 | 258.1 |
| time | 1 | 1.000 | 3.392 | 3.392 | 0.000 |
| trail_stop | 1,014 | 0.449 | 0.215 | 217.9 | 14.640 |

## By entry hour (UTC)

| entry_hour_utc | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| 0 | 70 | 0.371 | 0.245 | 17.170 | 11.320 |
| 4 | 209 | 0.368 | -0.072 | -15.045 | 21.632 |
| 8 | 197 | 0.381 | 0.087 | 17.170 | 12.461 |
| 12 | 240 | 0.417 | 0.044 | 10.599 | 25.606 |
| 16 | 394 | 0.345 | -0.082 | -32.339 | 45.566 |
| 20 | 159 | 0.277 | -0.213 | -33.840 | 39.477 |

## Monte Carlo (1000 runs)

| | p50 | p95 |
|---|---|---|
| Max drawdown, shuffled order (R) | 63.5 | 90.0 |
| Max drawdown, bootstrap (R) | 67.0 | 119.5 |

Bootstrap total R: p5 -102.4, p50 -37.4, p95 +39.5. Probability the edge is actually negative: **79%**.

---

_Backtests use mid/bid prices from free feeds, one position per instrument, no overnight financing, no margin limits. They are research, not a forecast and not advice._