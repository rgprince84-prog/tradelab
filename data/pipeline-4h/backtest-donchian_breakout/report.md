# donchian_breakout 4h

**Parameters:** lookback=20, adx_min=20, sl_atr=2.0, trail_atr=2.0, rr=None, max_bars=200

**Costs modelled:** spread per instrument (config), slippage 0.2 pips/pts per side, commission 0.0 GBP/round trip, same-bar SL+TP → pessimistic.  
**Sizing:** 1.0% of GBP 10,000 per trade, fixed.

## Headline

| Metric | Value |
|---|---|
| Trades | 1,240 |
| Win rate | 36.1% |
| Expectancy (R) | -0.031 |
| Profit factor | 0.933 |
| Payoff ratio | 1.650 |
| Total R | -38.181 |
| Return % | -38.181 |
| Max drawdown (R) | 112.3 |
| Max drawdown % | 112.3 |
| Sharpe (daily) | -0.381 |
| t-stat of mean R | -0.902 |
| Avg bars held | 13.875 |
| Max consecutive losses | 15 |
| Trades / month | 36.329 |
| First trade | 2024-01-02 |
| Last trade | 2026-11-06 |

![equity](equity.png)

![R distribution](r_distribution.png)

## By instrument

| instrument | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| AUDUSD | 114 | 0.316 | -0.100 | -11.421 | 18.945 |
| EURGBP | 108 | 0.213 | -0.228 | -24.657 | 26.235 |
| EURJPY | 99 | 0.414 | 0.058 | 5.758 | 10.272 |
| EURUSD | 110 | 0.336 | -0.064 | -7.022 | 8.024 |
| GBPJPY | 104 | 0.365 | -0.044 | -4.543 | 19.517 |
| GBPUSD | 107 | 0.439 | 0.109 | 11.627 | 7.712 |
| GER40 | 48 | 0.417 | 0.003 | 0.144 | 12.386 |
| JPN225 | 43 | 0.419 | -0.019 | -0.797 | 10.053 |
| NAS100 | 52 | 0.327 | -0.104 | -5.408 | 11.665 |
| SPX500 | 47 | 0.319 | -0.190 | -8.935 | 14.743 |
| UK100 | 46 | 0.522 | 0.125 | 5.752 | 4.132 |
| US30 | 42 | 0.476 | 0.081 | 3.394 | 6.665 |
| USDCAD | 107 | 0.308 | -0.039 | -4.174 | 17.685 |
| USDCHF | 106 | 0.358 | -0.028 | -2.925 | 18.316 |
| USDJPY | 107 | 0.383 | 0.047 | 5.025 | 14.332 |

## By year

| year | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| 2024 | 414 | 0.394 | 0.129 | 53.423 | 27.928 |
| 2025 | 446 | 0.345 | -0.136 | -60.726 | 65.559 |
| 2026 | 380 | 0.345 | -0.081 | -30.879 | 57.640 |

## By direction

| direction | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| long | 645 | 0.391 | 0.011 | 7.219 | 30.691 |
| short | 595 | 0.329 | -0.076 | -45.400 | 92.084 |

## By exit reason

| exit_reason | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| open_at_end | 5 | 1.000 | 0.932 | 4.661 | 0.000 |
| stop | 244 | 0.000 | -1.024 | -249.9 | 249.9 |
| time | 1 | 1.000 | 3.392 | 3.392 | 0.000 |
| trail_stop | 990 | 0.446 | 0.206 | 203.7 | 14.640 |

## By entry hour (UTC)

| entry_hour_utc | trades | win_rate | expectancy_R | total_R | max_dd_R |
|---|---|---|---|---|---|
| 0 | 66 | 0.364 | 0.176 | 11.627 | 11.320 |
| 4 | 208 | 0.370 | -0.074 | -15.408 | 20.637 |
| 8 | 195 | 0.379 | 0.092 | 17.986 | 12.461 |
| 12 | 234 | 0.419 | 0.054 | 12.708 | 25.606 |
| 16 | 383 | 0.347 | -0.086 | -32.916 | 44.640 |
| 20 | 154 | 0.273 | -0.209 | -32.179 | 39.435 |

## Monte Carlo (1000 runs)

| | p50 | p95 |
|---|---|---|
| Max drawdown, shuffled order (R) | 64.5 | 87.9 |
| Max drawdown, bootstrap (R) | 69.0 | 124.1 |

Bootstrap total R: p5 -108.8, p50 -38.6, p95 +28.0. Probability the edge is actually negative: **82%**.

---

_Backtests use mid/bid prices from free feeds, one position per instrument, no overnight financing, no margin limits. They are research, not a forecast and not advice._