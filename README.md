# tradelab — FX & index research pipeline

Four tools in one Python package, driven from the command line or by Claude Code:

| Tool | Command | What it does |
|---|---|---|
| 1. Chart Scanner | `scan` | One-line snapshot per instrument/timeframe: trend state, ADX regime, RSI, ATR%, Bollinger squeeze, 20-bar breakout, candle pattern, which strategies have a live signal. Ranked by a simple interest score. |
| 2. Setup Finder | `find` | Applies rule-based strategies to the last closed bars and lists every signal with direction, stop, target and reason. |
| 3. Entry & Exit Planner | `plan` | Turns instrument + direction into a sized plan: expected fill, stop, 1R/2R/3R targets, position size in your account currency, and the cost drag (spread + slippage) expressed in R. |
| 4. Time Machine | `backtest` | Bar-by-bar replay with realistic fills and costs. Win rate, expectancy, profit factor, drawdown, t-stat, Monte Carlo drawdown distribution, walk-forward parameter test. |
| All four | `pipeline` | scan → find → backtest the strategies that fired → plan each fresh setup with its historical stats attached. |

Markets: FX majors and crosses plus the main index CFDs (S&P 500, Nasdaq 100, Dow, FTSE 100, DAX, Nikkei 225). Data is free: Yahoo Finance (quick, ~2 years hourly) or Dukascopy (years of intraday, bid/ask, real volume).

> This is research tooling. It places no orders and makes no predictions. Backtests use free mid/bid data and are not advice.

## Quick start

```bash
pip install -r requirements.txt
python -m tradelab scan --tf 1h,4h            # what does the universe look like right now?
python -m tradelab find --tf 1h --lookback 3  # any rule-based setups on the last 3 closed bars?
python -m tradelab plan GBPUSD long --tf 4h   # size a trade from the current price
python -m tradelab backtest --strategy ema_pullback --tf 1d --start 2016-01-01 --mc --optimize
python -m tradelab pipeline --tf 1h           # everything, in one run; outputs land in ./out/<timestamp>-pipeline-1h/
```

Deeper intraday history (recommended for the backtester):

```bash
python -m tradelab --source dukascopy data refresh --tf 1h      # ~15 s for 8 years of hourly, cached locally
python -m tradelab --source dukascopy backtest --strategy session_orb --tf 1h --start 2018-01-01 --mc
```

Or set `data.source: dukascopy` in `config.yaml` to make it the default.

## Outputs

Every backtest writes a folder under `out/`:

- `report.md` — headline metrics, per-instrument / per-year / per-direction / per-exit-reason breakdowns, Monte Carlo, walk-forward
- `equity.png`, `r_distribution.png`
- `trades.csv` — every trade with signal time, fill, stop, target, exit reason, R and P&L
- `metrics.json` — the same numbers for machines

`pipeline` additionally writes `scan.csv`, `setups.csv`, `plans.json` and `summary.md`.

## How the backtester avoids cheating

These are the rules the engine enforces. Most "I automated my trading with AI" demos skip at least two of them.

1. **No look-ahead.** Every indicator is causal; a signal on bar *t* can only act from bar *t+1*. The still-forming bar is dropped before anything is computed.
2. **Realistic fills.** Market entries fill at the next bar's *open*, plus half the spread, plus slippage. Stop entries fill at the worse of the level and the open (gaps hurt you). Exits pay the same costs.
3. **Pessimistic same-bar resolution.** If a bar touches both the stop and the target, the loss is booked (`costs.same_bar_stop`).
4. **R is measured from the actual fill to the initial stop**, not from the planned entry.
5. **Costs are per instrument** and editable in `config.yaml`. Widen them to your broker's spreads; results move a lot.
6. **Sample-size honesty.** Reports flag fewer than 30 trades, print the t-stat of mean R, run Monte Carlo (shuffle + bootstrap) for the drawdown distribution and the probability the edge is negative, and `--optimize` fits parameters in-sample and tests out-of-sample so you can see the degradation.

What it does *not* model: overnight financing/swap, margin or leverage limits, correlation between simultaneous positions across instruments, broker-specific execution, or the fact that index CFDs and FX trade 24h with different liquidity by hour.

## Reading a report

- **Expectancy (R)** — average R per trade after costs. Positive is the whole game. 0.05R on 700 trades is not the same as 0.05R on 40.
- **t-stat** — mean R divided by its standard error. Below ~2 you cannot distinguish the result from zero.
- **Profit factor** — gross wins / gross losses. 1.0 is break-even.
- **Max drawdown (R)** — worst peak-to-trough in R. Compare with the Monte Carlo p95: that is what the same trades could have done in a different order.
- **P(edge < 0)** — bootstrap probability that the true expectancy is negative. Anything above ~10% says "not proven".
- **Walk-forward** — out-of-sample expectancy as a share of in-sample. Under 50% usually means the grid fitted noise.

## What the first runs showed (Oct 2026, default costs)

| Strategy | TF | Window | Trades | Expectancy | t-stat | Verdict |
|---|---|---|---|---|---|---|
| ema_pullback | 1h | 2024→ | 4,813 | −0.10R | −5.4 | consistently loses after spread |
| ema_pullback | 1d | 2016→ | 712 | +0.05R | +0.95 | indistinguishable from zero; P(edge<0) 16% |
| donchian_breakout | 1d | 2016→ | 813 | −0.07R | −1.6 | negative |
| bb_mean_reversion | 1d | 2016→ | 798 | −0.08R | −1.7 | negative |
| session_orb | 1h (Dukascopy) | 2018→ | 2,596 | −0.07R | −4.0 | negative; 1h is too coarse for ORB, retest on 15m/30m |

Textbook rules with default parameters do not have an edge on this universe once you pay the spread. That is the expected result and the reason to have a backtester: the value is in what you do next — tighter filters, better sessions, different instruments, lower costs — tested the same way.

## Configuration

`config.yaml` holds everything: account currency/equity/risk %, per-instrument spreads, slippage, sessions (local time, DST handled), the universe, and each strategy's parameters plus the grid used by `--optimize`. Override strategy params on the fly:

```bash
python -m tradelab backtest --strategy donchian_breakout --tf 4h --params '{"lookback": 55, "adx_min": 25}'
```

## Strategies included

- `ema_pullback` — EMA50/200 trend, pullback into EMA20 within 3 bars, reversal close; stop beyond the pullback low/high ± 0.5 ATR, 2R target, 48-bar time stop.
- `donchian_breakout` — first close beyond the 20-bar channel with ADX > 20 and the EMA50 on the right side; 2 ATR initial stop, 2 ATR trailing stop, no fixed target.
- `bb_mean_reversion` — ADX < 20 (ranging) and a close back inside the Bollinger band after closing outside; stop beyond the 2-bar extreme, target the middle band.
- `session_orb` — opening-range breakout of the instrument's home session (London for FX, home exchange for indices); stop at the other side of the range, 1.5R target, flat at session close, skips ranges wider than 1.5 ATR.

### Adding one

Write a function in `tradelab/setups.py` with the signature `fn(df, inst, params, cfg) -> DataFrame` that returns rows on signal bars with the columns documented at the top of that file, register it in `STRATEGIES` and `STRATEGY_TF`, add a params block to `config.yaml`. Use only information available at the signal bar.

## Data notes

- Yahoo intraday limits: 5m/15m/30m → last 60 days, 1h → ~2 years, daily → full history. The cache keeps extending as you re-run, so hourly history grows over time.
- Dukascopy: FX since 2003, index CFDs since ~2010s, bid side, UTC. First pull per instrument takes a few seconds per year of hourly data; afterwards it is incremental.
- Index data from Yahoo covers cash hours only; Dukascopy index CFDs trade extended hours, so session logic matters more there.
- `session_orb` on 1h bars uses the first *hour* as the range. For a 30-minute opening range on US indices use `--tf 30m` with Dukascopy.
- Cache lives in `.cache/` (CSV, or Parquet if `pyarrow` is installed). `python -m tradelab data clear` wipes it.

## Live dashboard (GitHub Actions → GitHub Pages)

The same pipeline runs unattended on GitHub Actions and publishes a dashboard page — scan,
setups, sized plans, strategy history and the weekly deep backtests, with the honest-numbers
rules above baked into the wording (fewer than 30 trades is an anecdote; t below 2 or
P(edge<0) above 10% is "not distinguishable from zero").

- **Page:** `https://<owner>.github.io/tradelab/` — a static page (`site/index.html`) that
  fetches `data.json` and renders it in the browser. No framework, no build step.
- **Schedule:** hourly at :12 UTC Monday–Friday on 1h and 4h; Sunday 20:12 UTC re-runs the
  deep backtests (1d since 2016 and 1h since 2024, all with Monte Carlo); Sunday 22:12 and
  23:12 as FX reopens. Every push to `main` also runs it. Run it on demand from
  *Actions → tradelab → Run workflow* (tick **backtests** to refresh the deep set).
- **Branches:**
  - `tradelab` — this code (the `.github/workflows/tradelab.yml` here is the reference copy);
  - `tradelab-data` — a single orphan commit holding the latest exported data
    (`data/data.json`, charts, CSVs, reports), force-pushed every run so it never grows;
  - inside a user-site repository (`owner.github.io`) the default branch additionally holds
    `.github/workflows/tradelab.yml` (GitHub only runs schedules from the default branch) and
    `tradelab/index.html`, whose `<meta name="tradelab-data">` points at the raw URL of the
    data branch. Nothing else there is touched, and the workflow never commits to it.
- **Market data cache:** `.cache/` is kept in the Actions cache (one save per day) so the
  hourly history keeps extending between runs, exactly as it does locally.

Local preview of the page with your own runs:

```
python -m tradelab dashboard --dest site/data      # newest run of each kind under out/ → site/data/
python -m http.server 8000 --directory site        # then open http://localhost:8000/
```

`dashboard` copies the newest `pipeline-<tf>` and `backtest-<strategy>-<tf>` folders, writes
`data.json` (NaN-free, browser-safe) and appends to `history.json`. It never modifies `out/`.

Running it in its own repository is the simplest setup: push this branch as `main` of any
repository whose name does not end in `.github.io`. The workflow then restores and publishes
the data branch exactly as above *and* deploys `site/` (page + data) to GitHub Pages itself, and
the page reads `./data/` because the `<meta name="tradelab-data">` tag is empty. One setting to
flip, once: *Settings → Pages → Build and deployment → Source: GitHub Actions* (the workflow's
own token is not allowed to do that for you; until it is set the `pages` job fails with that
message while the data branch is still published). (GitHub Pages on a private repository
needs a paid plan; on the free plan make the repository public.)

## Roadmap

- 15m/30m session strategies on Dukascopy with per-hour cost curves
- Regime filters (volatility percentile, day-of-week, news blackout) as composable pre-filters on any strategy
- Portfolio-level backtest: max concurrent risk, correlation-aware sizing
- Live/paper feed via a broker API (OANDA, IG, cTrader) for the scanner and planner; the research code stays unchanged
