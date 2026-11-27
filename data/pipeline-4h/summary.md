# Pipeline run — 4h — 2026-11-27 23:24 UTC

## Scan

| instrument | tf | last_bar_utc | close | trend | regime | adx | rsi | atr | atr_pct | bb_width_pctile | squeeze | donchian_pos | breakout_20 | ema20_dist_atr | pattern | setups | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GBPUSD | 4h | 2026-11-27 16:00 | 1.310 | down | ranging | 14.000 | 47.400 | 0.002 | 0.188 | 8.000 | True | 0.570 |  | -0.310 |  | ema_pullback:short | 5.500 |
| US30 | 4h | 2026-11-27 16:00 | 50,807.4 | mixed | trending | 26.000 | 56.200 | 522.9 | 1.029 | 86.000 | False | 0.990 | up | 1.270 |  | donchian_breakout:long | 5.500 |
| EURGBP | 4h | 2026-11-27 16:00 | 0.835 | down | ranging | 19.000 | 37.100 | 0.001 | 0.126 | 66.000 | False | 0.090 |  | -1.310 | inside_bar | bb_mean_reversion:long | 4.000 |
| USDCHF | 4h | 2026-11-27 16:00 | 0.836 | up | weak_trend | 22.900 | 52.100 | 0.002 | 0.275 | 15.000 | True | 0.730 |  | 0.430 | inside_bar |  | 3.500 |
| EURJPY | 4h | 2026-11-27 16:00 | 174.5 | down | ranging | 10.800 | 47.500 | 0.386 | 0.221 | 2.000 | True | 0.550 |  | -0.270 |  |  | 2.500 |
| USDJPY | 4h | 2026-11-27 16:00 | 159.6 | up | ranging | 11.600 | 62.200 | 0.261 | 0.164 | 5.000 | True | 0.970 |  | 1.000 | inside_bar |  | 2.500 |
| EURUSD | 4h | 2026-11-27 16:00 | 1.094 | down | ranging | 15.500 | 40.600 | 0.002 | 0.182 | 9.000 | True | 0.060 |  | -1.220 |  |  | 1.500 |
| AUDUSD | 4h | 2026-11-27 16:00 | 0.665 | down | weak_trend | 22.700 | 52.000 | 0.002 | 0.320 | 61.000 | False | 0.730 |  | 0.400 |  |  | 1.000 |
| GBPJPY | 4h | 2026-11-27 16:00 | 209.0 | down | ranging | 14.100 | 53.800 | 0.501 | 0.240 | 17.000 | False | 0.730 |  | 0.440 |  |  | 1.000 |
| JPN225 | 4h | 2026-11-27 04:00 | 58,717.0 | down | ranging | 19.800 | 47.600 | 1,044.0 | 1.779 | 53.000 | False | 0.420 |  | 0.020 |  |  | 1.000 |
| UK100 | 4h | 2026-11-27 16:00 | 10,701.8 | mixed | trending | 26.800 | 62.100 | 59.670 | 0.558 | 78.000 | False | 0.970 |  | 2.040 |  |  | 0.500 |
| USDCAD | 4h | 2026-11-27 16:00 | 1.425 | mixed | trending | 28.000 | 44.600 | 0.003 | 0.193 | 56.000 | False | 0.420 |  | -0.270 |  |  | 0.500 |
| GER40 | 4h | 2026-11-27 16:00 | 25,431.3 | down | weak_trend | 21.300 | 50.300 | 189.5 | 0.745 | 56.000 | False | 0.660 |  | 0.540 |  |  | 0.000 |
| NAS100 | 4h | 2026-11-27 16:00 | 26,757.2 | down | ranging | 19.600 | 51.700 | 525.5 | 1.964 | 83.000 | False | 0.650 |  | 0.630 |  |  | 0.000 |
| SPX500 | 4h | 2026-11-27 16:00 | 7,304.1 | down | weak_trend | 21.900 | 52.600 | 98.140 | 1.344 | 87.000 | False | 0.790 |  | 0.770 |  |  | 0.000 |

## Setups

| instrument | tf | strategy | direction | signal_bar_utc | fresh | bars_ago | ref_price | stop | target | stop_pips | atr | entry_type | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EURGBP | 4h | bb_mean_reversion | long | 2026-11-27 16:00 | True | 0 | 0.835 | 0.834 | 0.837 | 9.800 | 0.001 | market | re-entry above lower band, ADX<20 |
| GBPUSD | 4h | ema_pullback | short | 2026-11-27 16:00 | True | 0 | 1.310 | 1.315 | 1.300 | 50.500 | 0.002 | market | pullback to EMA20 in down-trend, bearish close |
| US30 | 4h | donchian_breakout | long | 2026-11-27 16:00 | True | 0 | 50,807.4 | 49,761.5 | n/a | 1,045.8 | 522.9 | market | close above 20-bar high, ADX>20 |
| EURJPY | 4h | ema_pullback | short | 2026-11-27 12:00 | False | 1 | 174.5 | 175.2 | 173.1 | 69.100 | 0.403 | market | pullback to EMA20 in down-trend, bearish close |
| EURUSD | 4h | ema_pullback | short | 2026-11-27 12:00 | False | 1 | 1.094 | 1.100 | 1.082 | 59.700 | 0.002 | market | pullback to EMA20 in down-trend, bearish close |
| EURGBP | 4h | ema_pullback | short | 2026-11-27 08:00 | False | 2 | 0.835 | 0.838 | 0.829 | 28.000 | 0.001 | market | pullback to EMA20 in down-trend, bearish close |
| UK100 | 4h | donchian_breakout | long | 2026-11-27 08:00 | False | 2 | 10,701.8 | 10,573.1 | n/a | 128.7 | 64.330 | market | close above 20-bar high, ADX>20 |

## Strategy history (same universe, same timeframe)

- **bb_mean_reversion**: 838 trades, win 51%, expectancy -0.020R, max DD 59.2R — [report](backtest-bb_mean_reversion/report.md)
- **donchian_breakout**: 1269 trades, win 36%, expectancy -0.029R, max DD 113.2R — [report](backtest-donchian_breakout/report.md)
- **ema_pullback**: 1329 trades, win 38%, expectancy +0.006R, max DD 73.9R — [report](backtest-ema_pullback/report.md)

## Plans

```
EURGBP LONG  (4h, as of 2026-11-27 16:00 UTC)  — bb_mean_reversion
  entry   0.83496  (expected fill 0.83504, market)
  stop    0.83398  (10.6 pips, 1.0 ATR)
  targets 1R=0.8361  2R=0.83716  3R=0.83822  custom=0.83654  custom_R=1.42
  size    94,341 units of base currency = 0.94 lots  risking GBP 100.00
  costs   1.6 pips round trip = 15.1% of 1R
  context trend=down adx=19.0 rsi=37.1
  history 838 trades, win 51%, expectancy -0.02R, max DD 59.2R  (t-stat -0.5)
          EURGBP alone: 72 trades, expectancy -0.16R
  ! This strategy has not been profitable after costs on this universe/timeframe. The setup is information, not a trade.
  ! Costs are 15% of 1R — stop is tight relative to spread; widen the stop or trade a lower-spread instrument.
  ! Long against the EMA50/200 trend on this timeframe.
  why     re-entry above lower band, ADX<20
```

```
GBPUSD SHORT  (4h, as of 2026-11-27 16:00 UTC)  — ema_pullback
  entry   1.30969  (expected fill 1.30961, market)
  stop    1.31474  (51.3 pips, 2.09 ATR)
  targets 1R=1.30448  2R=1.29935  3R=1.29422  custom=1.29959  custom_R=1.95
  size    25,529 units of base currency = 0.26 lots  risking GBP 100.00
  costs   1.6 pips round trip = 3.1% of 1R
  context trend=down adx=14.0 rsi=47.4
  history 1329 trades, win 38%, expectancy +0.01R, max DD 73.9R  (t-stat 0.2)
          GBPUSD alone: 117 trades, expectancy -0.04R
  why     pullback to EMA20 in down-trend, bearish close
```

```
US30 LONG  (4h, as of 2026-11-27 16:00 UTC)  — donchian_breakout
  entry   50807.39  (expected fill 50808.84, market)
  stop    49761.54  (1047.3 pts, 2.0 ATR)
  targets 1R=51856.14  2R=52903.44  3R=53950.74
  size    0.13 USD per index point  risking GBP 100.00
  costs   2.9 pts round trip = 0.3% of 1R
  context trend=down adx=26.0 rsi=56.2
  history 1269 trades, win 36%, expectancy -0.03R, max DD 113.2R  (t-stat -0.8)
          US30 alone: 43 trades, expectancy +0.11R
  ! This strategy has not been profitable after costs on this universe/timeframe. The setup is information, not a trade.
  ! Long against the EMA50/200 trend on this timeframe.
  why     close above 20-bar high, ADX>20
```
