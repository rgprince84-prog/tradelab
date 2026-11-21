# Pipeline run — 4h — 2026-11-21 00:46 UTC

## Scan

| instrument | tf | last_bar_utc | close | trend | regime | adx | rsi | atr | atr_pct | bb_width_pctile | squeeze | donchian_pos | breakout_20 | ema20_dist_atr | pattern | setups | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| JPN225 | 4h | 2026-11-20 04:00 | 56,576.0 | down | weak_trend | 24.800 | 29.300 | 1,048.0 | 1.853 | 61.000 | False | 0.030 | down | -2.840 |  | donchian_breakout:short | 6.000 |
| EURUSD | 4h | 2026-11-20 20:00 | 1.097 | down | trending | 41.100 | 42.700 | 0.002 | 0.197 | 1.000 | True | 0.250 |  | -0.500 | hammer |  | 4.000 |
| NAS100 | 4h | 2026-11-20 20:00 | 25,065.4 | down | trending | 30.000 | 20.600 | 425.2 | 1.696 | 100.0 | False | 0.040 | down | -3.980 |  |  | 3.500 |
| SPX500 | 4h | 2026-11-20 20:00 | 6,918.4 | down | trending | 35.300 | 16.600 | 79.360 | 1.147 | 100.0 | False | 0.050 | down | -4.490 |  |  | 3.500 |
| US30 | 4h | 2026-11-20 20:00 | 48,184.7 | down | trending | 40.300 | 15.100 | 442.4 | 0.918 | 100.0 | False | 0.040 | down | -4.620 |  |  | 3.500 |
| USDCHF | 4h | 2026-11-20 20:00 | 0.840 | up | trending | 31.100 | 46.200 | 0.002 | 0.272 | 12.000 | True | 0.290 |  | -0.700 | bullish_engulfing |  | 3.000 |
| UK100 | 4h | 2026-11-20 16:00 | 10,360.9 | down | trending | 33.900 | 20.900 | 59.690 | 0.576 | 100.0 | False | 0.050 |  | -4.030 | inside_bar |  | 2.500 |
| AUDUSD | 4h | 2026-11-20 20:00 | 0.662 | down | trending | 61.700 | 24.800 | 0.002 | 0.328 | 88.000 | False | 0.050 |  | -3.030 |  |  | 1.500 |
| EURJPY | 4h | 2026-11-20 20:00 | 173.9 | down | trending | 38.200 | 31.900 | 0.468 | 0.269 | 70.000 | False | 0.070 |  | -2.020 | hammer |  | 1.500 |
| GBPJPY | 4h | 2026-11-20 20:00 | 207.5 | down | trending | 49.000 | 24.100 | 0.584 | 0.282 | 100.0 | False | 0.080 |  | -2.680 |  |  | 1.500 |
| GER40 | 4h | 2026-11-20 16:00 | 24,839.5 | mixed | trending | 30.700 | 18.600 | 197.9 | 0.797 | 100.0 | False | 0.010 |  | -4.860 |  |  | 1.500 |
| USDJPY | 4h | 2026-11-20 20:00 | 158.5 | mixed | weak_trend | 21.400 | 29.600 | 0.343 | 0.216 | 72.000 | False | 0.070 |  | -2.020 |  |  | 1.000 |
| EURGBP | 4h | 2026-11-20 20:00 | 0.838 | mixed | trending | 27.200 | 68.100 | 0.001 | 0.141 | 100.0 | False | 0.940 |  | 1.510 |  |  | 0.500 |
| GBPUSD | 4h | 2026-11-20 20:00 | 1.308 | down | trending | 52.100 | 30.600 | 0.002 | 0.185 | 71.000 | False | 0.040 |  | -2.020 |  |  | 0.500 |
| USDCAD | 4h | 2026-11-20 20:00 | 1.434 | up | trending | 26.900 | 59.800 | 0.003 | 0.194 | 17.000 | False | 0.790 |  | 0.700 |  |  | 0.500 |

## Setups

| instrument | tf | strategy | direction | signal_bar_utc | fresh | bars_ago | ref_price | stop | target | stop_pips | atr | entry_type | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| JPN225 | 4h | donchian_breakout | short | 2026-11-20 04:00 | True | 0 | 56,576.0 | 58,673.0 | n/a | 2,096.3 | 1,048.0 | market | close below 20-bar low, ADX>20 |
| EURJPY | 4h | donchian_breakout | short | 2026-11-20 16:00 | False | 1 | 173.9 | 174.9 | n/a | 98.100 | 0.490 | market | close below 20-bar low, ADX>20 |
| GBPJPY | 4h | donchian_breakout | short | 2026-11-20 16:00 | False | 1 | 207.5 | 208.7 | n/a | 121.6 | 0.608 | market | close below 20-bar low, ADX>20 |
| AUDUSD | 4h | donchian_breakout | short | 2026-11-20 12:00 | False | 2 | 0.662 | 0.666 | n/a | 43.400 | 0.002 | market | close below 20-bar low, ADX>20 |
| NAS100 | 4h | donchian_breakout | short | 2026-11-20 12:00 | False | 2 | 25,065.4 | 25,911.5 | n/a | 846.1 | 423.1 | market | close below 20-bar low, ADX>20 |
| SPX500 | 4h | donchian_breakout | short | 2026-11-20 12:00 | False | 2 | 6,918.4 | 7,070.2 | n/a | 151.7 | 75.860 | market | close below 20-bar low, ADX>20 |
| US30 | 4h | donchian_breakout | short | 2026-11-20 12:00 | False | 2 | 48,184.7 | 49,028.5 | n/a | 843.8 | 421.9 | market | close below 20-bar low, ADX>20 |

## Strategy history (same universe, same timeframe)

- **donchian_breakout**: 1258 trades, win 37%, expectancy -0.013R, max DD 112.4R — [report](backtest-donchian_breakout/report.md)

## Plans

```
JPN225 SHORT  (4h, as of 2026-11-20 04:00 UTC)  — donchian_breakout
  entry   56576.0  (expected fill 56571.0, market)
  stop    58673.0  (2101.8 pts, 2.01 ATR)
  targets 1R=54469.0  2R=52368.0  3R=50266.0
  size    9.94 JPY per index point  risking GBP 100.00
  costs   10.4 pts round trip = 0.5% of 1R
  context trend=down adx=24.8 rsi=29.3
  history 1258 trades, win 37%, expectancy -0.01R, max DD 112.4R  (t-stat -0.4)
          JPN225 alone: 43 trades, expectancy -0.04R
  ! This strategy has not been profitable after costs on this universe/timeframe. The setup is information, not a trade.
  ! RSI 29: entering with momentum already stretched.
  why     close below 20-bar low, ADX>20
```
