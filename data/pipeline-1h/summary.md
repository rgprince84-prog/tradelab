# Pipeline run — 1h — 2026-11-27 23:24 UTC

## Scan

| instrument | tf | last_bar_utc | close | trend | regime | adx | rsi | atr | atr_pct | bb_width_pctile | squeeze | donchian_pos | breakout_20 | ema20_dist_atr | pattern | setups | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| USDCAD | 1h | 2026-11-27 22:00 | 1.425 | down | ranging | 10.400 | 52.300 | 0.001 | 0.103 | 1.000 | True | 0.620 |  | 0.130 | inside_bar |  | 3.500 |
| SPX500 | 1h | 2026-11-27 17:30 | 7,304.1 | mixed | ranging | 16.700 | 60.500 | 62.760 | 0.859 | 59.000 | False | 1.000 | up | 1.650 |  |  | 2.000 |
| EURGBP | 1h | 2026-11-27 22:00 | 0.835 | down | trending | 42.000 | 38.200 | 0.001 | 0.060 | 88.000 | False | 0.190 |  | -0.990 | inside_bar |  | 1.500 |
| USDCHF | 1h | 2026-11-27 22:00 | 0.836 | mixed | trending | 25.100 | 55.100 | 0.001 | 0.121 | 32.000 | False | 0.580 |  | 0.330 | inside_bar |  | 1.500 |
| EURJPY | 1h | 2026-11-27 22:00 | 174.5 | down | weak_trend | 24.600 | 41.500 | 0.137 | 0.078 | 51.000 | False | 0.190 |  | -0.880 | inside_bar |  | 1.000 |
| GBPJPY | 1h | 2026-11-27 22:00 | 209.0 | mixed | ranging | 15.800 | 50.800 | 0.186 | 0.089 | 18.000 | False | 0.280 |  | -0.060 | inside_bar |  | 1.000 |
| JPN225 | 1h | 2026-11-27 06:00 | 58,717.0 | mixed | ranging | 17.000 | 60.400 | 399.0 | 0.680 | 26.000 | False | 0.990 |  | 1.660 | inside_bar |  | 1.000 |
| US30 | 1h | 2026-11-27 17:30 | 50,807.4 | mixed | ranging | 19.300 | 65.000 | 345.7 | 0.680 | 43.000 | False | 0.990 |  | 1.960 | hammer |  | 1.000 |
| USDJPY | 1h | 2026-11-27 22:00 | 159.5 | up | ranging | 14.900 | 57.600 | 0.090 | 0.057 | 31.000 | False | 0.810 |  | 0.580 | inside_bar |  | 1.000 |
| EURUSD | 1h | 2026-11-27 22:00 | 1.094 | down | trending | 29.900 | 30.800 | 0.001 | 0.067 | 66.000 | False | 0.090 |  | -1.890 |  |  | 0.500 |
| GER40 | 1h | 2026-11-27 16:00 | 25,431.3 | mixed | trending | 26.800 | 59.400 | 98.210 | 0.386 | 62.000 | False | 0.950 |  | 1.420 |  |  | 0.500 |
| UK100 | 1h | 2026-11-27 16:00 | 10,701.8 | mixed | trending | 37.400 | 68.700 | 31.830 | 0.297 | 72.000 | False | 0.960 |  | 2.260 |  |  | 0.500 |
| AUDUSD | 1h | 2026-11-27 22:00 | 0.665 | mixed | weak_trend | 24.700 | 48.100 | 0.001 | 0.102 | 52.000 | False | 0.270 |  | -0.460 |  |  | 0.000 |
| GBPUSD | 1h | 2026-11-27 22:00 | 1.310 | down | weak_trend | 22.000 | 40.900 | 0.001 | 0.069 | 40.000 | False | 0.160 |  | -0.970 |  |  | 0.000 |
| NAS100 | 1h | 2026-11-27 17:30 | 26,757.2 | mixed | ranging | 18.200 | 59.400 | 324.2 | 1.212 | 63.000 | False | 0.940 |  | 1.700 |  |  | 0.000 |

## Setups

| instrument | tf | strategy | direction | signal_bar_utc | fresh | bars_ago | ref_price | stop | target | stop_pips | atr | entry_type | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EURGBP | 1h | donchian_breakout | short | 2026-11-27 21:00 | False | 1 | 0.835 | 0.836 | n/a | 10.100 | 0.001 | market | close below 20-bar low, ADX>20 |
| EURJPY | 1h | donchian_breakout | short | 2026-11-27 21:00 | False | 1 | 174.5 | 174.8 | n/a | 28.100 | 0.140 | market | close below 20-bar low, ADX>20 |
| UK100 | 1h | donchian_breakout | long | 2026-11-27 15:00 | False | 1 | 10,701.8 | 10,635.8 | n/a | 66.000 | 33.010 | market | close above 20-bar high, ADX>20 |
| US30 | 1h | bb_mean_reversion | short | 2026-11-27 16:30 | False | 1 | 50,807.4 | 51,010.2 | 49,976.1 | 202.8 | 360.0 | market | re-entry below upper band, ADX<20 |
| NAS100 | 1h | session_orb | long | 2026-11-27 15:30 | False | 2 | 26,757.2 | 26,167.3 | 27,642.0 | 589.8 | 347.1 | market | NEWYORK opening-range (1 bar) breakout up |

## Strategy history (same universe, same timeframe)

- **bb_mean_reversion**: 3023 trades, win 54%, expectancy -0.083R, max DD 259.6R — [report](backtest-bb_mean_reversion/report.md)
- **donchian_breakout**: 4761 trades, win 32%, expectancy -0.097R, max DD 493.0R — [report](backtest-donchian_breakout/report.md)
- **session_orb**: 7884 trades, win 43%, expectancy -0.074R, max DD 597.4R — [report](backtest-session_orb/report.md)

## Plans

_No fresh setups on the last closed bar._
