# Pipeline run — 4h — 2026-11-14 03:08 UTC

## Scan

| instrument | tf | last_bar_utc | close | trend | regime | adx | rsi | atr | atr_pct | bb_width_pctile | squeeze | donchian_pos | breakout_20 | ema20_dist_atr | pattern | setups | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AUDUSD | 4h | 2026-11-13 20:00 | 0.677 | down | trending | 49.100 | 21.000 | 0.002 | 0.258 | 82.000 | False | 0.020 | down | -2.930 |  | donchian_breakout:short | 6.500 |
| EURJPY | 4h | 2026-11-13 20:00 | 176.0 | down | trending | 26.400 | 31.200 | 0.412 | 0.234 | 59.000 | False | 0.060 | down | -1.880 |  | ema_pullback:short | 5.500 |
| JPN225 | 4h | 2026-11-13 04:00 | 61,156.0 | down | weak_trend | 23.300 | 47.300 | 1,076.0 | 1.759 | 78.000 | False | 0.560 |  | -0.060 | bearish_engulfing | ema_pullback:short | 5.000 |
| EURUSD | 4h | 2026-11-13 20:00 | 1.103 | down | trending | 34.500 | 25.900 | 0.002 | 0.200 | 91.000 | False | 0.030 |  | -2.640 | hammer |  | 2.500 |
| GBPUSD | 4h | 2026-11-13 20:00 | 1.321 | down | trending | 47.300 | 23.900 | 0.002 | 0.181 | 82.000 | False | 0.020 |  | -2.510 | shooting_star |  | 2.500 |
| USDCAD | 4h | 2026-11-13 20:00 | 1.427 | up | trending | 44.700 | 70.700 | 0.003 | 0.194 | 42.000 | False | 0.730 |  | 1.310 |  |  | 1.500 |
| USDCHF | 4h | 2026-11-13 20:00 | 0.838 | up | trending | 44.500 | 71.600 | 0.002 | 0.274 | 88.000 | False | 0.900 |  | 2.280 |  |  | 1.500 |
| USDJPY | 4h | 2026-11-13 20:00 | 159.7 | up | trending | 26.500 | 60.800 | 0.357 | 0.224 | 70.000 | False | 0.670 |  | 0.520 | inside_bar |  | 1.500 |
| EURGBP | 4h | 2026-11-13 20:00 | 0.834 | down | ranging | 17.400 | 41.600 | 0.001 | 0.125 | 48.000 | False | 0.160 |  | -0.890 | hammer |  | 1.000 |
| GER40 | 4h | 2026-11-13 16:00 | 26,756.0 | up | weak_trend | 25.000 | 62.700 | 175.1 | 0.654 | 100.0 | False | 0.820 |  | 1.450 | inside_bar |  | 1.000 |
| NAS100 | 4h | 2026-11-13 20:00 | 27,937.4 | down | ranging | 18.700 | 46.900 | 358.1 | 1.282 | 69.000 | False | 0.670 |  | -0.280 |  |  | 1.000 |
| US30 | 4h | 2026-11-13 20:00 | 52,342.0 | up | ranging | 9.700 | 51.800 | 336.8 | 0.643 | 64.000 | False | 0.770 |  | 0.210 |  |  | 1.000 |
| GBPJPY | 4h | 2026-11-13 20:00 | 211.0 | mixed | trending | 36.400 | 35.600 | 0.504 | 0.239 | 28.000 | False | 0.130 |  | -1.310 |  |  | 0.500 |
| SPX500 | 4h | 2026-11-13 20:00 | 7,560.9 | mixed | ranging | 13.200 | 49.100 | 60.700 | 0.803 | 84.000 | False | 0.700 |  | -0.040 |  |  | 0.000 |
| UK100 | 4h | 2026-11-13 16:00 | 10,907.4 | up | weak_trend | 21.700 | 62.400 | 56.890 | 0.522 | 76.000 | False | 0.960 |  | 1.560 |  |  | 0.000 |

## Setups

| instrument | tf | strategy | direction | signal_bar_utc | fresh | bars_ago | ref_price | stop | target | stop_pips | atr | entry_type | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AUDUSD | 4h | donchian_breakout | short | 2026-11-13 20:00 | True | 0 | 0.677 | 0.681 | n/a | 34.900 | 0.002 | market | close below 20-bar low, ADX>20 |
| EURJPY | 4h | ema_pullback | short | 2026-11-13 20:00 | True | 0 | 176.0 | 177.1 | 173.7 | 113.4 | 0.412 | market | pullback to EMA20 in down-trend, bearish close |
| JPN225 | 4h | ema_pullback | short | 2026-11-13 04:00 | True | 0 | 61,156.0 | 62,440.0 | 58,587.0 | 1,284.4 | 1,076.0 | market | pullback to EMA20 in down-trend, bearish close |
| EURGBP | 4h | bb_mean_reversion | long | 2026-11-13 16:00 | False | 1 | 0.834 | 0.833 | 0.836 | 8.200 | 0.001 | market | re-entry above lower band, ADX<20 |
| EURJPY | 4h | ema_pullback | short | 2026-11-13 16:00 | False | 1 | 176.0 | 177.2 | 173.5 | 123.0 | 0.423 | market | pullback to EMA20 in down-trend, bearish close |
| EURJPY | 4h | donchian_breakout | short | 2026-11-13 16:00 | False | 1 | 176.0 | 176.8 | n/a | 84.700 | 0.423 | market | close below 20-bar low, ADX>20 |
| GBPUSD | 4h | donchian_breakout | short | 2026-11-13 16:00 | False | 1 | 1.321 | 1.326 | n/a | 50.100 | 0.003 | market | close below 20-bar low, ADX>20 |
| USDCHF | 4h | donchian_breakout | long | 2026-11-13 16:00 | False | 1 | 0.838 | 0.833 | n/a | 47.200 | 0.002 | market | close above 20-bar high, ADX>20 |
| AUDUSD | 4h | donchian_breakout | short | 2026-11-13 12:00 | False | 2 | 0.677 | 0.681 | n/a | 37.900 | 0.002 | market | close below 20-bar low, ADX>20 |
| EURGBP | 4h | ema_pullback | short | 2026-11-13 12:00 | False | 2 | 0.834 | 0.837 | 0.829 | 25.500 | 0.001 | market | pullback to EMA20 in down-trend, bearish close |
| EURJPY | 4h | ema_pullback | short | 2026-11-13 12:00 | False | 2 | 176.0 | 177.3 | 173.3 | 135.0 | 0.420 | market | pullback to EMA20 in down-trend, bearish close |
| EURUSD | 4h | donchian_breakout | short | 2026-11-13 12:00 | False | 2 | 1.103 | 1.108 | n/a | 48.000 | 0.002 | market | close below 20-bar low, ADX>20 |
| JPN225 | 4h | ema_pullback | short | 2026-11-12 04:00 | False | 2 | 61,156.0 | 62,357.0 | 58,754.0 | 1,200.9 | 1,137.0 | market | pullback to EMA20 in down-trend, bearish close |
| NAS100 | 4h | ema_pullback | short | 2026-11-13 12:00 | False | 2 | 27,937.4 | 28,670.8 | 26,470.5 | 733.4 | 383.2 | market | pullback to EMA20 in down-trend, bearish close |

## Strategy history (same universe, same timeframe)

- **bb_mean_reversion**: 834 trades, win 51%, expectancy -0.019R, max DD 59.2R — [report](backtest-bb_mean_reversion/report.md)
- **donchian_breakout**: 1246 trades, win 36%, expectancy -0.026R, max DD 113.4R — [report](backtest-donchian_breakout/report.md)
- **ema_pullback**: 1309 trades, win 38%, expectancy +0.011R, max DD 72.9R — [report](backtest-ema_pullback/report.md)

## Plans

```
AUDUSD SHORT  (4h, as of 2026-11-13 20:00 UTC)  — donchian_breakout
  entry   0.67742  (expected fill 0.67735, market)
  stop    0.6809  (35.5 pips, 2.04 ATR)
  targets 1R=0.67379  2R=0.67024  3R=0.66668
  size    37,219 units of base currency = 0.37 lots  risking GBP 100.00
  costs   1.4 pips round trip = 3.9% of 1R
  context trend=down adx=49.1 rsi=21.0
  history 1246 trades, win 36%, expectancy -0.03R, max DD 113.4R  (t-stat -0.8)
          AUDUSD alone: 115 trades, expectancy -0.09R
  ! This strategy has not been profitable after costs on this universe/timeframe. The setup is information, not a trade.
  ! RSI 21: entering with momentum already stretched.
  why     close below 20-bar low, ADX>20
```

```
EURJPY SHORT  (4h, as of 2026-11-13 20:00 UTC)  — ema_pullback
  entry   175.986  (expected fill 175.976, market)
  stop    177.12  (114.4 pips, 2.77 ATR)
  targets 1R=174.833  2R=173.689  3R=172.546  custom=173.718  custom_R=1.98
  size    18,499 units of base currency = 0.18 lots  risking GBP 100.00
  costs   1.9 pips round trip = 1.7% of 1R
  context trend=down adx=26.4 rsi=31.2
  history 1309 trades, win 38%, expectancy +0.01R, max DD 72.9R  (t-stat 0.3)
          EURJPY alone: 127 trades, expectancy -0.06R
  why     pullback to EMA20 in down-trend, bearish close
```

```
JPN225 SHORT  (4h, as of 2026-11-13 04:00 UTC)  — ema_pullback
  entry   61156.0  (expected fill 61151.0, market)
  stop    62440.0  (1289.1 pts, 1.2 ATR)
  targets 1R=59862.0  2R=58573.0  3R=57284.0  custom=58587.0  custom_R=1.99
  size    16.41 JPY per index point  risking GBP 100.00
  costs   10.4 pts round trip = 0.8% of 1R
  context trend=down adx=23.3 rsi=47.3
  history 1309 trades, win 38%, expectancy +0.01R, max DD 72.9R  (t-stat 0.3)
          JPN225 alone: 37 trades, expectancy +0.34R
  why     pullback to EMA20 in down-trend, bearish close
```
