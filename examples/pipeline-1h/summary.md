# Pipeline run — 1h — 2026-10-23 23:04 UTC

## Scan

| instrument | tf | last_bar_utc | close | trend | regime | adx | rsi | atr | atr_pct | bb_width_pctile | squeeze | donchian_pos | breakout_20 | ema20_dist_atr | pattern | setups | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| USDJPY | 1h | 2026-10-23 20:00 | 156.8 | down | trending | 26.400 | 47.300 | 0.235 | 0.150 | 46.000 | False | 0.630 |  | -0.150 |  | ema_pullback:short | 4.500 |
| EURGBP | 1h | 2026-10-23 21:00 | 0.838 | down | ranging | 18.600 | 55.500 | 0.001 | 0.065 | 9.000 | True | 0.900 |  | 0.710 | inside_bar |  | 2.500 |
| GBPJPY | 1h | 2026-10-23 21:00 | 209.8 | down | trending | 28.800 | 45.300 | 0.304 | 0.145 | 62.000 | False | 0.480 |  | -0.230 | inside_bar |  | 2.500 |
| EURUSD | 1h | 2026-10-23 21:00 | 1.120 | down | ranging | 13.600 | 47.600 | 0.001 | 0.080 | 27.000 | False | 0.500 |  | -0.050 | inside_bar |  | 2.000 |
| USDCAD | 1h | 2026-10-23 21:00 | 1.400 | down | ranging | 16.000 | 48.500 | 0.002 | 0.112 | 60.000 | False | 0.700 |  | 0.020 | inside_bar |  | 2.000 |
| EURJPY | 1h | 2026-10-23 21:00 | 175.7 | down | trending | 32.600 | 47.700 | 0.255 | 0.145 | 70.000 | False | 0.560 |  | 0.100 |  |  | 1.500 |
| AUDUSD | 1h | 2026-10-23 21:00 | 0.704 | up | ranging | 19.500 | 61.000 | 0.001 | 0.084 | 82.000 | False | 0.910 |  | 1.270 | inside_bar |  | 1.000 |
| GBPUSD | 1h | 2026-10-23 21:00 | 1.337 | mixed | ranging | 15.800 | 45.400 | 0.001 | 0.075 | 18.000 | False | 0.350 |  | -0.410 | inside_bar |  | 1.000 |
| UK100 | 1h | 2026-10-23 15:00 | 10,670.6 | mixed | weak_trend | 20.300 | 42.300 | 27.890 | 0.261 | 17.000 | False | 0.290 |  | -0.800 | bullish_engulfing |  | 1.000 |
| JPN225 | 1h | 2026-10-23 06:00 | 62,727.0 | down | trending | 37.300 | 38.200 | 451.0 | 0.719 | 80.000 | False | 0.340 |  | -1.110 |  |  | 0.500 |
| NAS100 | 1h | 2026-10-23 19:30 | 28,956.1 | down | trending | 35.800 | 34.000 | 138.4 | 0.478 | 99.000 | False | 0.110 |  | -1.670 |  |  | 0.500 |
| SPX500 | 1h | 2026-10-23 19:30 | 7,623.0 | down | trending | 27.400 | 37.100 | 25.490 | 0.334 | 100.0 | False | 0.070 |  | -1.620 |  |  | 0.500 |
| US30 | 1h | 2026-10-23 19:30 | 52,209.2 | mixed | trending | 35.800 | 42.800 | 189.5 | 0.363 | 75.000 | False | 0.180 |  | -1.280 |  |  | 0.500 |
| GER40 | 1h | 2026-10-23 15:00 | 25,151.7 | down | weak_trend | 23.300 | 39.800 | 92.670 | 0.368 | 68.000 | False | 0.210 |  | -1.240 |  |  | 0.000 |
| USDCHF | 1h | 2026-10-23 21:00 | 0.824 | mixed | ranging | 15.000 | 54.400 | 0.001 | 0.130 | 83.000 | False | 0.690 |  | 0.340 |  |  | 0.000 |

## Setups

| instrument | tf | strategy | direction | signal_bar_utc | fresh | bars_ago | ref_price | stop | target | stop_pips | atr | entry_type | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| USDJPY | 1h | ema_pullback | short | 2026-10-23 20:00 | True | 0 | 156.8 | 157.0 | 156.4 | 22.500 | 0.235 | market | pullback to EMA20 in down-trend, bearish close |

## Strategy history (same universe, same timeframe)

- **ema_pullback**: 4813 trades, win 35%, expectancy -0.102R, max DD 506.2R — [report](backtest-ema_pullback/report.md)

## Plans

```
USDJPY SHORT  (1h, as of 2026-10-23 20:00 UTC)  — ema_pullback
  entry   156.814  (expected fill 156.807, market)
  stop    157.039  (23.2 pips, 0.99 ATR)
  targets 1R=156.575  2R=156.343  3R=156.111  custom=156.365  custom_R=1.91
  size    90,514.0 units of base currency = 0.91 lots  risking GBP 100.00
  costs   1.4 pips round trip = 6.0% of 1R
  context trend=down adx=26.4 rsi=47.3
  history 4813 trades, win 35%, expectancy -0.10R, max DD 506.2R
  why     pullback to EMA20 in down-trend, bearish close
```
