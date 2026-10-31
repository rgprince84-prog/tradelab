# Pipeline run — 4h — 2026-10-31 00:43 UTC

## Scan

| instrument | tf | last_bar_utc | close | trend | regime | adx | rsi | atr | atr_pct | bb_width_pctile | squeeze | donchian_pos | breakout_20 | ema20_dist_atr | pattern | setups | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AUDUSD | 4h | 2026-10-30 20:00 | 0.704 | up | ranging | 14.000 | 50.700 | 0.002 | 0.218 | 15.000 | True | 0.350 |  | -0.020 | inside_bar |  | 3.500 |
| NAS100 | 4h | 2026-10-30 16:00 | 28,385.8 | mixed | trending | 32.500 | 31.100 | 356.1 | 1.255 | 68.000 | False | 0.160 | down | -2.800 | hammer |  | 3.500 |
| UK100 | 4h | 2026-10-30 16:00 | 10,736.1 | up | ranging | 15.300 | 54.100 | 47.890 | 0.446 | 6.000 | True | 0.710 |  | 0.430 | bullish_engulfing |  | 3.500 |
| JPN225 | 4h | 2026-10-30 04:00 | 63,082.0 | mixed | trending | 25.200 | 40.600 | 907.0 | 1.437 | 15.000 | True | 0.410 |  | -1.080 | inside_bar |  | 3.000 |
| SPX500 | 4h | 2026-10-30 16:00 | 7,580.9 | mixed | ranging | 16.500 | 34.600 | 52.480 | 0.692 | 57.000 | False | 0.220 | down | -2.110 | hammer |  | 3.000 |
| EURGBP | 4h | 2026-10-30 20:00 | 0.833 | down | trending | 30.400 | 29.200 | 0.001 | 0.138 | 68.000 | False | 0.180 |  | -1.900 | bearish_engulfing |  | 2.500 |
| EURUSD | 4h | 2026-10-30 20:00 | 1.117 | down | ranging | 18.400 | 47.400 | 0.002 | 0.210 | 51.000 | False | 0.500 |  | -0.190 | bearish_engulfing |  | 2.000 |
| US30 | 4h | 2026-10-30 16:00 | 51,774.2 | mixed | ranging | 19.400 | 39.200 | 326.7 | 0.631 | 39.000 | False | 0.150 | down | -1.410 |  |  | 2.000 |
| USDJPY | 4h | 2026-10-30 20:00 | 157.5 | down | ranging | 19.200 | 47.600 | 0.386 | 0.245 | 70.000 | False | 0.400 |  | -0.270 | inside_bar |  | 2.000 |
| EURJPY | 4h | 2026-10-30 20:00 | 175.8 | down | trending | 28.600 | 45.000 | 0.467 | 0.266 | 48.000 | False | 0.490 |  | -0.430 |  |  | 1.500 |
| GBPJPY | 4h | 2026-10-30 20:00 | 211.0 | up | ranging | 16.900 | 57.700 | 0.523 | 0.248 | 57.000 | False | 0.810 |  | 0.600 | inside_bar |  | 1.000 |
| GBPUSD | 4h | 2026-10-30 20:00 | 1.339 | up | weak_trend | 22.500 | 58.800 | 0.003 | 0.200 | 94.000 | False | 0.720 |  | 0.850 | inside_bar |  | 1.000 |
| GER40 | 4h | 2026-10-30 16:00 | 25,817.5 | up | ranging | 16.300 | 58.800 | 151.7 | 0.588 | 100.0 | False | 0.740 |  | 0.990 | hammer |  | 1.000 |
| USDCAD | 4h | 2026-10-30 20:00 | 1.397 | down | trending | 33.300 | 40.000 | 0.003 | 0.198 | 86.000 | False | 0.270 |  | -0.550 |  |  | 0.500 |
| USDCHF | 4h | 2026-10-30 20:00 | 0.825 | mixed | weak_trend | 23.700 | 47.400 | 0.002 | 0.280 | 89.000 | False | 0.470 |  | -0.170 |  |  | 0.000 |

## Setups

| instrument | tf | strategy | direction | signal_bar_utc | fresh | bars_ago | ref_price | stop | target | stop_pips | atr | entry_type | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GBPJPY | 4h | ema_pullback | long | 2026-10-30 16:00 | False | 1 | 211.0 | 210.0 | 213.0 | 99.800 | 0.539 | market | pullback to EMA20 in up-trend, bullish close |
| NAS100 | 4h | donchian_breakout | short | 2026-10-30 12:00 | False | 1 | 28,385.8 | 29,092.2 | n/a | 706.4 | 353.2 | market | close below 20-bar low, ADX>20 |
| EURUSD | 4h | ema_pullback | short | 2026-10-30 12:00 | False | 2 | 1.117 | 1.122 | 1.106 | 54.800 | 0.002 | market | pullback to EMA20 in down-trend, bearish close |
| GER40 | 4h | bb_mean_reversion | short | 2026-10-30 08:00 | False | 2 | 25,817.5 | 26,172.2 | 25,560.5 | 354.7 | 162.8 | market | re-entry below upper band, ADX<20 |
| USDJPY | 4h | bb_mean_reversion | long | 2026-10-30 12:00 | False | 2 | 157.5 | 156.8 | 157.8 | 76.500 | 0.407 | market | re-entry above lower band, ADX<20 |

## Strategy history (same universe, same timeframe)

- **bb_mean_reversion**: 824 trades, win 51%, expectancy -0.021R, max DD 58.9R — [report](backtest-bb_mean_reversion/report.md)
- **donchian_breakout**: 1228 trades, win 36%, expectancy -0.033R, max DD 113.2R — [report](backtest-donchian_breakout/report.md)
- **ema_pullback**: 1287 trades, win 38%, expectancy +0.006R, max DD 72.0R — [report](backtest-ema_pullback/report.md)

## Plans

_No fresh setups on the last closed bar._
