# CLAUDE.md — driving tradelab

## Goal

Run and extend this FX/index research pipeline for Rajat, and report what the data actually says. "Done" for an analysis request is a short written verdict backed by numbers from `out/`, never a number you did not generate in this session.

## Context

Rajat trades FX majors and index CFDs on a UK (GBP) retail account and uses this repo to decide which setups deserve attention and which rules have no edge after costs. The expensive failure mode is false confidence: a backtest with a flattering parameter set, a tiny sample, or costs left at zero. A result that says "no edge" is a good result here.

## How the pieces fit

```
python -m tradelab scan      --tf 1h,4h                      # Chart Scanner: snapshot + ranking
python -m tradelab find      --tf 1h --lookback 3            # Setup Finder: live rule-based signals
python -m tradelab plan      EURUSD long --tf 4h [--stop ..] # Entry & Exit Planner: sized plan, cost in R
python -m tradelab backtest  --strategy X --tf 1d --start 2016-01-01 --mc --optimize
python -m tradelab pipeline  --tf 1h                         # all four; writes out/<ts>-pipeline-1h/summary.md
python -m tradelab --source dukascopy data refresh --tf 1h   # deep intraday history (8+ years), cached
```

Strategy rules and costs live in `config.yaml`; strategy code in `tradelab/setups.py`; the engine in `tradelab/backtest.py` (read its docstring before changing fills or exits). Each backtest writes `report.md`, `trades.csv`, `metrics.json`, `equity.png` into `out/`.

## Standards for any result you report

- State the window, timeframe, instrument set, trade count, expectancy in R, t-stat and max drawdown in R. Those six numbers travel together; a win rate on its own is not a result.
- Fewer than 30 trades is an anecdote. Say so and do not draw a conclusion from it.
- t-stat below 2 (or Monte Carlo P(edge<0) above 10%) means "not distinguishable from zero". Use those words.
- If you tuned parameters, report the out-of-sample figure, not the in-sample one, and name the parameters you tried. Prefer `--optimize` (walk-forward) over hand-tuning.
- When the result is negative, say it is negative. Do not soften it into "mixed" or "shows promise".
- Costs: never lower spreads or slippage below the config defaults to improve a result. Raising them to stress-test is fine and worth doing.

Worked example of a verdict line:

> `donchian_breakout` 1d, 2016→2026, 15 instruments: 813 trades, −0.07R expectancy, t = −1.6, max DD 87R, P(edge<0) 94%. Negative after costs. Shorts on JPY crosses were the only positive bucket (41 trades, +0.21R) — too few to act on.

## Boundaries

- Research only. Never connect a broker, place, modify or cancel an order, or write code that does, even if asked in passing — stop and confirm first.
- Do not change the engine's fill rules, same-bar resolution, or R definition to make a strategy look better. Changes to `backtest.py` need a one-line reason in the commit message explaining what became *more* realistic.
- Do not delete or rewrite files under `out/`; they are the audit trail.
- Keep every new indicator and strategy causal (bar *t* uses bars ≤ *t*). If a signal needs the bar's own close, the trade acts on *t+1*.
- New strategies go in `setups.py` with a `config.yaml` block and a line in `README.md`. Register the timeframes they are designed for.

## Working style

Lead with the verdict, then the supporting numbers, then what you would test next. Keep terse notes between tool calls; the final message should re-ground someone who did not watch the run. If a request is ambiguous about window, timeframe or instruments, use the config defaults (2024→ on 1h, or 2016→ on 1d) and say which you used rather than asking.
