# Pipeline run — 1h — 2026-11-21 00:46 UTC

## Scan

| instrument | tf | last_bar_utc | close | trend | regime | adx | rsi | atr | atr_pct | bb_width_pctile | squeeze | donchian_pos | breakout_20 | ema20_dist_atr | pattern | setups | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NAS100 | 1h | 2026-11-20 20:30 | 25,065.4 | down | trending | 38.500 | 14.700 | 290.6 | 1.160 | 100.0 | False | 0.050 | down | -3.880 |  |  | 3.500 |
| SPX500 | 1h | 2026-11-20 20:30 | 6,918.4 | down | trending | 48.900 | 9.300 | 55.580 | 0.803 | 100.0 | False | 0.070 | down | -4.140 |  |  | 3.500 |
| US30 | 1h | 2026-11-20 20:30 | 48,184.7 | down | trending | 67.100 | 12.600 | 315.6 | 0.655 | 93.000 | False | 0.080 | down | -3.730 |  |  | 3.500 |
| AUDUSD | 1h | 2026-11-20 22:00 | 0.662 | down | trending | 37.700 | 29.500 | 0.001 | 0.160 | 95.000 | False | 0.090 |  | -2.610 | inside_bar |  | 2.500 |
| GBPJPY | 1h | 2026-11-20 22:00 | 207.5 | down | trending | 46.700 | 30.800 | 0.313 | 0.151 | 88.000 | False | 0.160 |  | -1.860 | inside_bar |  | 1.500 |
| GER40 | 1h | 2026-11-20 16:00 | 24,839.5 | down | trending | 61.900 | 23.100 | 127.9 | 0.515 | 100.0 | False | 0.020 |  | -3.790 |  |  | 1.500 |
| JPN225 | 1h | 2026-11-20 06:00 | 56,576.0 | down | trending | 29.300 | 28.000 | 520.0 | 0.918 | 83.000 | False | 0.040 |  | -2.820 |  |  | 1.500 |
| UK100 | 1h | 2026-11-20 16:00 | 10,360.9 | down | trending | 63.400 | 29.500 | 39.180 | 0.378 | 52.000 | False | 0.110 |  | -2.550 |  |  | 1.500 |
| USDCHF | 1h | 2026-11-20 22:00 | 0.840 | mixed | trending | 36.900 | 41.200 | 0.001 | 0.155 | 92.000 | False | 0.350 |  | -0.790 | inside_bar |  | 1.500 |
| EURGBP | 1h | 2026-11-20 22:00 | 0.838 | up | weak_trend | 21.600 | 58.100 | 0.001 | 0.078 | 47.000 | False | 0.880 |  | 0.670 | inside_bar |  | 1.000 |
| EURUSD | 1h | 2026-11-20 22:00 | 1.097 | down | ranging | 13.500 | 48.200 | 0.001 | 0.096 | 40.000 | False | 0.320 |  | -0.200 |  |  | 1.000 |
| GBPUSD | 1h | 2026-11-20 22:00 | 1.308 | down | weak_trend | 21.400 | 37.400 | 0.001 | 0.090 | 40.000 | False | 0.110 |  | -1.450 | inside_bar |  | 1.000 |
| USDCAD | 1h | 2026-11-20 22:00 | 1.434 | up | ranging | 16.300 | 56.400 | 0.002 | 0.115 | 48.000 | False | 0.720 |  | 0.600 | inside_bar |  | 1.000 |
| EURJPY | 1h | 2026-11-20 22:00 | 173.9 | down | trending | 35.600 | 32.600 | 0.231 | 0.133 | 72.000 | False | 0.140 |  | -1.770 |  |  | 0.500 |
| USDJPY | 1h | 2026-11-20 21:00 | 158.5 | down | trending | 41.400 | 31.600 | 0.216 | 0.137 | 87.000 | False | 0.110 |  | -1.690 |  |  | 0.500 |

## Setups

| instrument | tf | strategy | direction | signal_bar_utc | fresh | bars_ago | ref_price | stop | target | stop_pips | atr | entry_type | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| USDCAD | 1h | bb_mean_reversion | short | 2026-11-20 21:00 | False | 1 | 1.434 | 1.437 | 1.433 | 26.200 | 0.002 | market | re-entry below upper band, ADX<20 |
| EURGBP | 1h | ema_pullback | long | 2026-11-20 20:00 | False | 2 | 0.838 | 0.837 | 0.840 | 9.700 | 0.001 | market | pullback to EMA20 in up-trend, bullish close |
| JPN225 | 1h | donchian_breakout | short | 2026-11-20 04:00 | False | 2 | 56,576.0 | 57,714.0 | n/a | 1,137.7 | 569.0 | market | close below 20-bar low, ADX>20 |
| NAS100 | 1h | donchian_breakout | short | 2026-11-20 18:30 | False | 2 | 25,065.4 | 25,653.0 | n/a | 587.6 | 293.8 | market | close below 20-bar low, ADX>20 |
| SPX500 | 1h | donchian_breakout | short | 2026-11-20 18:30 | False | 2 | 6,918.4 | 7,028.3 | n/a | 109.9 | 54.950 | market | close below 20-bar low, ADX>20 |
| USDCAD | 1h | ema_pullback | long | 2026-11-20 20:00 | False | 2 | 1.434 | 1.432 | 1.439 | 23.800 | 0.002 | market | pullback to EMA20 in up-trend, bullish close |
| USDJPY | 1h | donchian_breakout | short | 2026-11-20 19:00 | False | 2 | 158.5 | 159.0 | n/a | 45.200 | 0.226 | market | close below 20-bar low, ADX>20 |

## Strategy history (same universe, same timeframe)

- **bb_mean_reversion**: 3000 trades, win 54%, expectancy -0.084R, max DD 259.6R — [report](backtest-bb_mean_reversion/report.md)
- **donchian_breakout**: 4734 trades, win 32%, expectancy -0.094R, max DD 498.0R — [report](backtest-donchian_breakout/report.md)
- **ema_pullback**: 4945 trades, win 35%, expectancy -0.094R, max DD 505.2R — [report](backtest-ema_pullback/report.md)

## Plans

_No fresh setups on the last closed bar._
