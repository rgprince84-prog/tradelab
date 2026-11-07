# Pipeline run — 4h — 2026-11-07 02:45 UTC

## Scan

| instrument | tf | last_bar_utc | close | trend | regime | adx | rsi | atr | atr_pct | bb_width_pctile | squeeze | donchian_pos | breakout_20 | ema20_dist_atr | pattern | setups | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AUDUSD | 4h | 2026-11-06 20:00 | 0.687 | down | trending | 38.600 | 20.200 | 0.002 | 0.331 | 100.0 | False | 0.060 |  | -3.130 | inside_bar |  | 2.500 |
| EURGBP | 4h | 2026-11-06 20:00 | 0.835 | down | ranging | 17.800 | 52.600 | 0.001 | 0.141 | 3.000 | True | 0.680 |  | 0.400 |  |  | 2.500 |
| JPN225 | 4h | 2026-11-06 04:00 | 57,411.0 | down | trending | 32.100 | 26.600 | 1,278.0 | 2.226 | 92.000 | False | 0.080 |  | -3.630 | inside_bar |  | 2.500 |
| GBPJPY | 4h | 2026-11-06 20:00 | 211.5 | mixed | trending | 29.200 | 42.300 | 0.606 | 0.287 | 84.000 | False | 0.140 |  | -0.980 | inside_bar |  | 1.500 |
| GBPUSD | 4h | 2026-11-06 20:00 | 1.336 | mixed | trending | 31.500 | 33.500 | 0.003 | 0.212 | 92.000 | False | 0.070 |  | -2.160 | inside_bar |  | 1.500 |
| NAS100 | 4h | 2026-11-06 20:00 | 26,977.3 | down | trending | 34.400 | 30.800 | 408.3 | 1.513 | 98.000 | False | 0.110 |  | -2.370 | inside_bar |  | 1.500 |
| USDCAD | 4h | 2026-11-06 20:00 | 1.413 | mixed | trending | 32.700 | 78.800 | 0.003 | 0.235 | 100.0 | False | 0.950 |  | 2.960 |  |  | 1.500 |
| USDCHF | 4h | 2026-11-06 20:00 | 0.820 | down | trending | 32.100 | 53.800 | 0.003 | 0.351 | 52.000 | False | 0.780 |  | 0.590 | bearish_engulfing |  | 1.500 |
| GER40 | 4h | 2026-11-06 16:00 | 25,794.8 | up | ranging | 19.500 | 46.500 | 216.1 | 0.838 | 96.000 | False | 0.160 |  | -0.900 | inside_bar |  | 1.000 |
| EURJPY | 4h | 2026-11-06 20:00 | 176.6 | down | trending | 25.900 | 43.200 | 0.478 | 0.271 | 83.000 | False | 0.190 |  | -0.840 |  |  | 0.500 |
| EURUSD | 4h | 2026-11-06 20:00 | 1.114 | down | weak_trend | 21.600 | 33.900 | 0.003 | 0.238 | 100.0 | False | 0.050 |  | -1.960 |  |  | 0.000 |
| SPX500 | 4h | 2026-11-06 20:00 | 7,374.9 | mixed | weak_trend | 23.100 | 33.500 | 68.830 | 0.933 | 100.0 | False | 0.060 |  | -2.360 |  |  | 0.000 |
| UK100 | 4h | 2026-11-06 16:00 | 10,670.3 | mixed | ranging | 18.200 | 46.200 | 77.150 | 0.723 | 69.000 | False | 0.340 |  | -0.730 |  |  | 0.000 |
| US30 | 4h | 2026-11-06 20:00 | 51,271.6 | mixed | ranging | 19.500 | 38.400 | 444.7 | 0.867 | 98.000 | False | 0.100 |  | -1.690 |  |  | 0.000 |
| USDJPY | 4h | 2026-11-06 20:00 | 158.4 | up | ranging | 13.900 | 55.700 | 0.470 | 0.297 | 67.000 | False | 0.770 |  | 0.640 |  |  | 0.000 |

## Setups

| instrument | tf | strategy | direction | signal_bar_utc | fresh | bars_ago | ref_price | stop | target | stop_pips | atr | entry_type | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| JPN225 | 4h | donchian_breakout | short | 2026-11-06 00:00 | False | 1 | 57,411.0 | 60,066.0 | n/a | 2,654.6 | 1,327.0 | market | close below 20-bar low, ADX>20 |
| UK100 | 4h | bb_mean_reversion | long | 2026-11-06 12:00 | False | 1 | 10,670.3 | 10,487.4 | 10,738.8 | 182.9 | 81.360 | market | re-entry above lower band, ADX<20 |
| USDCAD | 4h | donchian_breakout | long | 2026-11-06 12:00 | False | 2 | 1.413 | 1.406 | n/a | 66.700 | 0.003 | market | close above 20-bar high, ADX>20 |

## Strategy history (same universe, same timeframe)

- **bb_mean_reversion**: 829 trades, win 51%, expectancy -0.019R, max DD 58.9R — [report](backtest-bb_mean_reversion/report.md)
- **donchian_breakout**: 1240 trades, win 36%, expectancy -0.031R, max DD 112.3R — [report](backtest-donchian_breakout/report.md)

## Plans

_No fresh setups on the last closed bar._
