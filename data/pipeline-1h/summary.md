# Pipeline run — 1h — 2026-11-14 03:08 UTC

## Scan

| instrument | tf | last_bar_utc | close | trend | regime | adx | rsi | atr | atr_pct | bb_width_pctile | squeeze | donchian_pos | breakout_20 | ema20_dist_atr | pattern | setups | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EURJPY | 1h | 2026-11-13 21:00 | 176.0 | down | trending | 44.400 | 27.000 | 0.205 | 0.116 | 100.0 | False | 0.070 | down | -2.460 | bearish_engulfing | donchian_breakout:short | 7.500 |
| UK100 | 1h | 2026-11-13 16:00 | 10,907.4 | up | weak_trend | 21.800 | 65.000 | 26.620 | 0.244 | 22.000 | False | 0.980 | up | 1.620 |  | ema_pullback:long | 5.000 |
| GER40 | 1h | 2026-11-13 16:00 | 26,756.0 | up | ranging | 14.900 | 55.200 | 89.930 | 0.336 | 12.000 | True | 0.440 |  | 0.300 | inside_bar |  | 3.500 |
| SPX500 | 1h | 2026-11-13 20:30 | 7,560.9 | down | ranging | 18.100 | 49.200 | 33.560 | 0.444 | 34.000 | False | 0.400 |  | -0.170 | bullish_engulfing |  | 2.000 |
| AUDUSD | 1h | 2026-11-13 22:00 | 0.677 | down | trending | 46.500 | 30.500 | 0.001 | 0.115 | 49.000 | False | 0.040 |  | -1.880 | inside_bar |  | 1.500 |
| EURGBP | 1h | 2026-11-13 22:00 | 0.834 | down | trending | 25.100 | 38.800 | 0.001 | 0.061 | 92.000 | False | 0.220 |  | -1.230 | inside_bar |  | 1.500 |
| GBPJPY | 1h | 2026-11-13 22:00 | 211.0 | down | trending | 33.300 | 36.100 | 0.250 | 0.118 | 90.000 | False | 0.190 |  | -1.400 | inside_bar |  | 1.500 |
| JPN225 | 1h | 2026-11-13 06:00 | 61,156.0 | mixed | ranging | 19.500 | 52.100 | 415.0 | 0.679 | 2.000 | True | 0.420 |  | 0.090 |  |  | 1.500 |
| EURUSD | 1h | 2026-11-13 22:00 | 1.103 | down | weak_trend | 24.900 | 33.200 | 0.001 | 0.087 | 51.000 | False | 0.090 |  | -1.710 | inside_bar |  | 1.000 |
| NAS100 | 1h | 2026-11-13 20:30 | 27,937.4 | down | ranging | 17.300 | 47.200 | 192.4 | 0.689 | 35.000 | False | 0.330 |  | -0.460 |  |  | 1.000 |
| US30 | 1h | 2026-11-13 20:30 | 52,342.0 | up | ranging | 16.000 | 51.600 | 174.9 | 0.334 | 18.000 | False | 0.440 |  | 0.100 |  |  | 1.000 |
| USDCAD | 1h | 2026-11-13 22:00 | 1.427 | up | ranging | 15.500 | 56.900 | 0.001 | 0.098 | 38.000 | False | 0.850 |  | 0.570 | inside_bar |  | 1.000 |
| USDJPY | 1h | 2026-11-13 21:00 | 159.7 | mixed | ranging | 18.200 | 42.900 | 0.179 | 0.112 | 17.000 | False | 0.260 |  | -0.810 | bearish_engulfing |  | 1.000 |
| GBPUSD | 1h | 2026-11-13 22:00 | 1.321 | down | trending | 25.500 | 37.200 | 0.001 | 0.088 | 22.000 | False | 0.070 |  | -1.250 |  |  | 0.500 |
| USDCHF | 1h | 2026-11-13 22:00 | 0.838 | up | weak_trend | 23.600 | 58.300 | 0.001 | 0.125 | 68.000 | False | 0.710 |  | 0.540 |  |  | 0.000 |

## Setups

| instrument | tf | strategy | direction | signal_bar_utc | fresh | bars_ago | ref_price | stop | target | stop_pips | atr | entry_type | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EURJPY | 1h | donchian_breakout | short | 2026-11-13 21:00 | True | 0 | 176.0 | 176.4 | n/a | 41.000 | 0.205 | market | close below 20-bar low, ADX>20 |
| UK100 | 1h | ema_pullback | long | 2026-11-13 16:00 | True | 0 | 10,907.4 | 10,850.9 | 11,020.5 | 56.500 | 26.620 | market | pullback to EMA20 in up-trend, bullish close |
| UK100 | 1h | donchian_breakout | long | 2026-11-13 15:00 | False | 1 | 10,907.4 | 10,852.4 | n/a | 55.000 | 27.510 | market | close above 20-bar high, ADX>20 |
| USDJPY | 1h | bb_mean_reversion | long | 2026-11-13 19:00 | False | 2 | 159.7 | 159.4 | 159.9 | 26.100 | 0.175 | market | re-entry above lower band, ADX<20 |

## Strategy history (same universe, same timeframe)

- **bb_mean_reversion**: 2985 trades, win 54%, expectancy -0.085R, max DD 259.6R — [report](backtest-bb_mean_reversion/report.md)
- **donchian_breakout**: 4697 trades, win 32%, expectancy -0.101R, max DD 499.0R — [report](backtest-donchian_breakout/report.md)
- **ema_pullback**: 4917 trades, win 35%, expectancy -0.099R, max DD 504.3R — [report](backtest-ema_pullback/report.md)

## Plans

```
EURJPY SHORT  (1h, as of 2026-11-13 21:00 UTC)  — donchian_breakout
  entry   175.986  (expected fill 175.976, market)
  stop    176.396  (42.0 pips, 2.05 ATR)
  targets 1R=175.557  2R=175.137  3R=174.718
  size    50,425 units of base currency = 0.5 lots  risking GBP 100.00
  costs   1.9 pips round trip = 4.5% of 1R
  context trend=down adx=44.4 rsi=27.0
  history 4697 trades, win 32%, expectancy -0.10R, max DD 499.0R  (t-stat -5.6)
          EURJPY alone: 398 trades, expectancy -0.11R
  ! This strategy has not been profitable after costs on this universe/timeframe. The setup is information, not a trade.
  ! RSI 27: entering with momentum already stretched.
  why     close below 20-bar low, ADX>20
```

```
UK100 LONG  (1h, as of 2026-11-13 16:00 UTC)  — ema_pullback
  entry   10907.41  (expected fill 10908.11, market)
  stop    10850.87  (57.2 pts, 2.15 ATR)
  targets 1R=10965.35  2R=11022.59  3R=11079.83  custom=11020.49  custom_R=1.96
  size    1.75 GBP per index point  risking GBP 100.00
  costs   1.4 pts round trip = 2.4% of 1R
  context trend=up adx=21.8 rsi=65.0
  history 4917 trades, win 35%, expectancy -0.10R, max DD 504.3R  (t-stat -5.3)
          UK100 alone: 187 trades, expectancy +0.01R
  ! This strategy has not been profitable after costs on this universe/timeframe. The setup is information, not a trade.
  why     pullback to EMA20 in up-trend, bullish close
```
