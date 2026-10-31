# Pipeline run — 1h — 2026-10-31 00:43 UTC

## Scan

| instrument | tf | last_bar_utc | close | trend | regime | adx | rsi | atr | atr_pct | bb_width_pctile | squeeze | donchian_pos | breakout_20 | ema20_dist_atr | pattern | setups | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| UK100 | 1h | 2026-10-30 16:00 | 10,736.1 | up | trending | 28.500 | 52.200 | 29.940 | 0.279 | 1.000 | True | 0.560 |  | 0.170 | bullish_engulfing |  | 4.000 |
| EURJPY | 1h | 2026-10-30 21:00 | 175.8 | down | trending | 25.400 | 48.100 | 0.296 | 0.169 | 94.000 | False | 0.530 |  | -0.130 | inside_bar |  | 2.500 |
| GER40 | 1h | 2026-10-30 16:00 | 25,817.5 | up | trending | 26.900 | 49.900 | 83.540 | 0.324 | 28.000 | False | 0.360 |  | -0.450 | hammer |  | 2.500 |
| GBPJPY | 1h | 2026-10-30 21:00 | 211.0 | up | ranging | 15.600 | 54.100 | 0.318 | 0.151 | 54.000 | False | 0.690 |  | 0.410 | inside_bar |  | 2.000 |
| AUDUSD | 1h | 2026-10-30 23:00 | 0.704 | mixed | ranging | 10.800 | 50.600 | 0.001 | 0.097 | 11.000 | True | 0.640 |  | 0.120 |  |  | 1.500 |
| EURGBP | 1h | 2026-10-30 21:00 | 0.833 | down | trending | 34.800 | 38.300 | 0.001 | 0.083 | 95.000 | False | 0.270 |  | -0.990 | inside_bar |  | 1.500 |
| NAS100 | 1h | 2026-10-30 19:30 | 28,385.8 | down | trending | 36.900 | 29.700 | 188.9 | 0.665 | 100.0 | False | 0.170 |  | -2.830 |  |  | 1.500 |
| EURUSD | 1h | 2026-10-30 21:00 | 1.117 | down | weak_trend | 21.000 | 46.500 | 0.001 | 0.122 | 90.000 | False | 0.380 |  | -0.510 | inside_bar |  | 1.000 |
| GBPUSD | 1h | 2026-10-30 21:00 | 1.339 | up | weak_trend | 22.300 | 50.500 | 0.001 | 0.098 | 62.000 | False | 0.250 |  | -0.290 |  |  | 1.000 |
| JPN225 | 1h | 2026-10-30 06:00 | 63,082.0 | down | weak_trend | 21.700 | 41.600 | 425.0 | 0.674 | 42.000 | False | 0.170 |  | -1.120 | inside_bar |  | 1.000 |
| USDCAD | 1h | 2026-10-30 23:00 | 1.397 | down | weak_trend | 21.000 | 52.600 | 0.001 | 0.099 | 16.000 | False | 0.840 |  | 0.450 |  |  | 1.000 |
| USDJPY | 1h | 2026-10-30 20:00 | 157.5 | down | weak_trend | 22.400 | 51.300 | 0.243 | 0.154 | 67.000 | False | 0.710 |  | 0.300 |  |  | 1.000 |
| SPX500 | 1h | 2026-10-30 19:30 | 7,580.9 | down | trending | 32.600 | 34.300 | 30.470 | 0.402 | 100.0 | False | 0.230 |  | -2.120 |  |  | 0.500 |
| US30 | 1h | 2026-10-30 19:30 | 51,774.2 | mixed | trending | 35.000 | 34.700 | 171.6 | 0.331 | 91.000 | False | 0.200 |  | -1.850 |  |  | 0.500 |
| USDCHF | 1h | 2026-10-30 23:00 | 0.825 | mixed | weak_trend | 22.500 | 55.600 | 0.001 | 0.155 | 81.000 | False | 0.880 |  | 0.870 |  |  | 0.000 |

## Setups

| instrument | tf | strategy | direction | signal_bar_utc | fresh | bars_ago | ref_price | stop | target | stop_pips | atr | entry_type | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EURJPY | 1h | ema_pullback | short | 2026-10-30 20:00 | False | 1 | 175.8 | 176.2 | 175.1 | 34.000 | 0.305 | market | pullback to EMA20 in down-trend, bearish close |
| EURUSD | 1h | ema_pullback | short | 2026-10-30 20:00 | False | 1 | 1.117 | 1.118 | 1.113 | 15.900 | 0.001 | market | pullback to EMA20 in down-trend, bearish close |
| GBPJPY | 1h | ema_pullback | long | 2026-10-30 19:00 | False | 2 | 211.0 | 210.5 | 212.0 | 50.100 | 0.335 | market | pullback to EMA20 in up-trend, bullish close |
| USDJPY | 1h | ema_pullback | short | 2026-10-30 18:00 | False | 2 | 157.5 | 157.8 | 157.0 | 24.800 | 0.250 | market | pullback to EMA20 in down-trend, bearish close |

## Strategy history (same universe, same timeframe)

- **ema_pullback**: 4842 trades, win 35%, expectancy -0.101R, max DD 500.0R — [report](backtest-ema_pullback/report.md)

## Plans

_No fresh setups on the last closed bar._
