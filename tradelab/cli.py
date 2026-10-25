"""tradelab command line.

    python -m tradelab scan      [--tf 1h,4h] [--instruments EURUSD,GBPUSD]
    python -m tradelab find      [--tf 1h] [--strategies ema_pullback,session_orb] [--lookback 3]
    python -m tradelab plan      EURUSD long [--entry 1.0850] [--stop 1.0800] [--stop-method atr|structure]
    python -m tradelab backtest  --strategy ema_pullback [--tf 1h] [--start 2024-01-01] [--mc] [--optimize]
    python -m tradelab pipeline  [--tf 1h]      # scan -> find -> plan each setup -> backtest the strategies that fired
    python -m tradelab data      refresh|clear [--instruments ...] [--tf ...]
    python -m tradelab dashboard [--dest site/data]   # static data for the live dashboard page (reads ./out, or --out DIR before the subcommand)

Global: --config PATH  --source yfinance|dukascopy  --out DIR  --quiet
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from typing import List, Optional

import pandas as pd

from .backtest import compute_metrics, monte_carlo, run_strategy, walk_forward
from .config import Config, load_config
from .data import DataHub
from .planner import build_plan, format_plan
from .report import jsonable, md_table, write_backtest_report
from .scanner import find_setups, scan
from .setups import STRATEGIES, STRATEGY_TF

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 40)
pd.set_option("display.max_colwidth", 60)


def _split(s: Optional[str]) -> Optional[List[str]]:
    return [x.strip() for x in s.split(",") if x.strip()] if s else None


def _outdir(base: str, name: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(base, f"{stamp}-{name}")
    os.makedirs(path, exist_ok=True)
    return path


def _instruments(args, cfg: Config) -> List[str]:
    return [i.upper() for i in (_split(args.instruments) or cfg.universe)]


def _print(df: pd.DataFrame, title: str) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    print(df.to_string(index=False) if len(df) else "(nothing)")


# ------------------------------------------------------------------ commands
def cmd_scan(args, cfg: Config, hub: DataHub) -> int:
    tfs = _split(args.tf) or [cfg.data.default_tf]
    df = scan(hub, cfg, _instruments(args, cfg), tfs, source=args.source)
    _print(df, f"Chart scan — {', '.join(tfs)} — {datetime.utcnow():%Y-%m-%d %H:%M} UTC")
    if args.out:
        out = _outdir(args.out, "scan")
        df.to_csv(os.path.join(out, "scan.csv"), index=False)
        print(f"\nsaved {out}/scan.csv")
    return 0


def cmd_find(args, cfg: Config, hub: DataHub) -> int:
    tfs = _split(args.tf) or [cfg.data.default_tf]
    strategies = _split(args.strategies)
    df = find_setups(hub, cfg, _instruments(args, cfg), tfs, strategies, lookback=args.lookback, source=args.source)
    _print(df, f"Setups on the last {args.lookback} closed bars — {', '.join(tfs)}")
    if args.out:
        out = _outdir(args.out, "find")
        df.to_csv(os.path.join(out, "setups.csv"), index=False)
        print(f"\nsaved {out}/setups.csv")
    return 0


def cmd_plan(args, cfg: Config, hub: DataHub) -> int:
    plan = build_plan(
        hub, cfg, args.instrument, args.direction, tf=args.tf or cfg.data.default_tf,
        entry=args.entry, stop=args.stop, target=args.target, stop_method=args.stop_method,
        stop_atr=args.stop_atr, equity=args.equity, risk_pct=args.risk, source=args.source,
    )
    print(format_plan(plan))
    if args.json:
        print(json.dumps(jsonable(plan), indent=2, default=str))
    if args.out:
        out = _outdir(args.out, f"plan-{plan['instrument']}")
        with open(os.path.join(out, "plan.json"), "w") as f:
            json.dump(jsonable(plan), f, indent=2, default=str)
        print(f"\nsaved {out}/plan.json")
    return 0


def cmd_backtest(args, cfg: Config, hub: DataHub) -> int:
    strategies = _split(args.strategy) or list(STRATEGIES)
    tf = args.tf or cfg.data.default_tf
    start = args.start or cfg.backtest.start
    end = args.end or cfg.backtest.end
    instruments = _instruments(args, cfg)
    base_out = args.out or "out"
    overrides = json.loads(args.params) if args.params else None
    rc = 0
    for strat in strategies:
        if tf not in STRATEGY_TF[strat]:
            print(f"[backtest] {strat} is not designed for {tf} (use {', '.join(STRATEGY_TF[strat])}); skipping")
            continue
        print(f"\n=== {strat} on {tf}  {start} → {end or 'latest'}  ({len(instruments)} instruments)")
        trades = run_strategy(hub, cfg, strat, instruments, tf, start, end, overrides, args.source, quiet=args.quiet)
        m = compute_metrics(trades, cfg)
        mc = monte_carlo(trades["r"].to_numpy(), cfg.backtest.mc_runs) if (args.mc and len(trades)) else None
        wf = None
        if args.optimize:
            grid = cfg.strategies.get(strat, {}).get("grid")
            if not grid:
                print(f"[backtest] no grid defined for {strat} in config.yaml; skipping optimisation")
            else:
                print(f"[backtest] walk-forward over {grid} …")
                wf = walk_forward(hub, cfg, strat, instruments, tf, start, end, cfg.backtest.oos_fraction, grid, args.source)
        out = _outdir(base_out, f"backtest-{strat}-{tf}")
        params = cfg.strategy_params(strat, overrides)
        path = write_backtest_report(out, f"{strat} {tf}", trades, m, cfg, mc, wf, params)
        if m.get("trades"):
            print(
                f"trades {m['trades']}  win {m['win_rate']:.1%}  expectancy {m['expectancy_R']:+.3f}R  "
                f"PF {m['profit_factor']:.2f}  total {m['total_R']:+.1f}R ({m['return_pct']:+.1f}%)  "
                f"maxDD {m['max_drawdown_R']:.1f}R  t={m['t_stat']:.2f}"
            )
            if mc:
                print(f"MC: p95 drawdown {mc['bootstrap_max_dd_R_p95']:.1f}R, P(edge<0) {mc['prob_total_R_negative']:.0%}")
            if wf and wf.get("best_params"):
                ob, od = wf["oos_best"], wf["oos_default"]
                print(f"WF: best IS params {wf['best_params']} → OOS {ob.get('trades', 0)} trades, {ob.get('expectancy_R', float('nan')):+.3f}R;  defaults OOS {od.get('expectancy_R', float('nan')):+.3f}R")
        else:
            print("no trades")
        print(f"report: {path}")
    return rc


def cmd_pipeline(args, cfg: Config, hub: DataHub) -> int:
    """Scanner → Setup Finder → Planner for each fresh setup → Time Machine on the strategies that fired."""
    tf = args.tf or cfg.data.default_tf
    instruments = _instruments(args, cfg)
    out = _outdir(args.out or "out", f"pipeline-{tf}")
    start = args.start or cfg.backtest.start

    print(f"[1/4] scanning {len(instruments)} instruments on {tf} …")
    sc = scan(hub, cfg, instruments, [tf], source=args.source)
    sc.to_csv(os.path.join(out, "scan.csv"), index=False)
    _print(sc[["instrument", "trend", "regime", "adx", "rsi", "atr_pct", "squeeze", "breakout_20", "pattern", "setups", "score"]].head(15) if len(sc) else sc, "Scan (top 15)")

    print(f"\n[2/4] finding setups on the last {args.lookback} bars …")
    st = find_setups(hub, cfg, instruments, [tf], None, lookback=args.lookback, source=args.source)
    st.to_csv(os.path.join(out, "setups.csv"), index=False)
    _print(st[["instrument", "strategy", "direction", "signal_bar_utc", "fresh", "ref_price", "stop", "target", "stop_pips", "note"]] if len(st) else st, "Setups")

    print("\n[3/4] backtesting the strategies that fired …")
    fired = sorted(st["strategy"].unique()) if len(st) else []
    stats = {}
    for strat in fired:
        trades = run_strategy(hub, cfg, strat, instruments, tf, start, cfg.backtest.end, None, args.source, quiet=True)
        m = compute_metrics(trades, cfg)
        mc = monte_carlo(trades["r"].to_numpy(), cfg.backtest.mc_runs) if len(trades) else None
        write_backtest_report(os.path.join(out, f"backtest-{strat}"), f"{strat} {tf}", trades, m, cfg, mc, None, cfg.strategy_params(strat))
        stats[strat] = m
        by_inst = trades.groupby("instrument")["r"].agg(["size", "mean"]) if len(trades) else pd.DataFrame()
        stats[f"{strat}__by_instrument"] = by_inst
        print(f"  {strat:18} {m.get('trades', 0):4} trades  win {m.get('win_rate', float('nan')):.0%}  expectancy {m.get('expectancy_R', float('nan')):+.3f}R  maxDD {m.get('max_drawdown_R', float('nan')):.1f}R")

    print("\n[4/4] planning each fresh setup …")
    plans = []
    plan_failures = []
    fresh = st[st["fresh"]] if len(st) else st
    for _, s in fresh.iterrows():
        inst_stats = dict(stats.get(s["strategy"], {}))
        bi = stats.get(f"{s['strategy']}__by_instrument")
        if bi is not None and len(bi) and s["instrument"] in bi.index:
            inst_stats["this_instrument_trades"] = int(bi.loc[s["instrument"], "size"])
            inst_stats["this_instrument_expectancy_R"] = float(bi.loc[s["instrument"], "mean"])
        try:
            plan = build_plan(
                hub, cfg, s["instrument"], s["direction"], tf=tf, stop=float(s["stop"]),
                target=None if pd.isna(s["target"]) else float(s["target"]), source=args.source,
                stats=inst_stats, strategy=s["strategy"], note=s["note"],
            )
            plans.append(plan)
            print("\n" + format_plan(plan))
        except Exception as e:
            print(f"  plan failed for {s['instrument']} {s['strategy']}: {e}")
            plan_failures.append(f"{s['instrument']} {s['strategy']} {s['direction']}: {type(e).__name__}: {e}")
    with open(os.path.join(out, "plans.json"), "w") as f:
        json.dump(jsonable(plans), f, indent=2, default=str)

    # anything that degraded this run: feed failures, stale fallbacks, plans that could not be built
    warnings = [f"data: {p}" for p in hub.problems] + [f"plan: {p}" for p in plan_failures]
    if not len(sc):
        warnings.insert(0, "scan: no instrument returned enough data (feed down and cache empty?)")
    with open(os.path.join(out, "warnings.json"), "w") as f:
        json.dump(warnings, f, indent=2)
    if warnings:
        print("\nwarnings:")
        for w in warnings:
            print(f"  ! {w}")

    # summary markdown
    md = [f"# Pipeline run — {tf} — {datetime.utcnow():%Y-%m-%d %H:%M} UTC", "", "## Scan", "", md_table(sc, index=False), ""]
    md += ["## Setups", "", md_table(st, index=False) if len(st) else "_none on the last bars_", ""]
    md += ["## Strategy history (same universe, same timeframe)", ""]
    for strat in fired:
        m = stats[strat]
        md += [f"- **{strat}**: {m.get('trades', 0)} trades, win {m.get('win_rate', float('nan')):.0%}, expectancy {m.get('expectancy_R', float('nan')):+.3f}R, "
               f"max DD {m.get('max_drawdown_R', float('nan')):.1f}R — [report](backtest-{strat}/report.md)"]
    md += ["", "## Plans", ""]
    for p in plans:
        md += ["```", format_plan(p), "```", ""]
    if not plans:
        md += ["_Plans could not be built for the fresh setups (see warnings)._" if plan_failures
               else "_No fresh setups on the last closed bar._", ""]
    if warnings:
        md += ["## Warnings", ""] + [f"- {w}" for w in warnings] + [""]
    with open(os.path.join(out, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"\nsaved {out}/summary.md (+ scan.csv, setups.csv, plans.json, backtest-*/)")
    return 0


def cmd_data(args, cfg: Config, hub: DataHub) -> int:
    if args.action == "clear":
        shutil.rmtree(cfg.data.cache_dir, ignore_errors=True)
        print(f"cleared {cfg.data.cache_dir}")
        return 0
    tfs = _split(args.tf) or ["1h", "1d"]
    for key in _instruments(args, cfg):
        inst = cfg.instrument(key)
        for tf in tfs:
            df = hub.get(inst, tf, source=args.source, refresh=True)
            print(f"{key:7} {tf:3} {len(df):7} bars  {df.index[0] if len(df) else '-'} → {df.index[-1] if len(df) else '-'}")
    return 0



def cmd_dashboard(args, cfg: Config, hub: DataHub) -> int:
    """Export the newest run of each kind under out/ as static data for site/index.html."""
    from .dashboard import export_dashboard

    info = export_dashboard(args.out or "out", args.dest, cfg)
    print(f"dashboard data -> {info['path']}")
    print(f"  exported now : {', '.join(info['exported']) or 'nothing new under out/'}")
    print(f"  pipelines    : {', '.join(info['pipelines']) or '-'}")
    print(f"  backtests    : {', '.join(info['backtests']) or '-'}")
    return 0

# ---------------------------------------------------------------------- main
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="tradelab", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", default=None)
    p.add_argument("--source", default=None, choices=["yfinance", "dukascopy"])
    p.add_argument("--out", default=None, help="output directory (default: ./out for backtest/pipeline)")
    p.add_argument("--quiet", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan", help="Chart Scanner")
    s.add_argument("--tf", default=None, help="comma list, e.g. 1h,4h,1d")
    s.add_argument("--instruments", default=None)
    s.set_defaults(fn=cmd_scan)

    s = sub.add_parser("find", help="Setup Finder")
    s.add_argument("--tf", default=None)
    s.add_argument("--instruments", default=None)
    s.add_argument("--strategies", default=None, help=f"comma list from: {', '.join(STRATEGIES)}")
    s.add_argument("--lookback", type=int, default=3, help="closed bars to look back for signals")
    s.set_defaults(fn=cmd_find)

    s = sub.add_parser("plan", help="Entry & Exit Planner")
    s.add_argument("instrument")
    s.add_argument("direction", choices=["long", "short"])
    s.add_argument("--tf", default=None)
    s.add_argument("--entry", type=float, default=None, help="entry price (default: last close, market)")
    s.add_argument("--stop", type=float, default=None, help="stop price (default: computed)")
    s.add_argument("--target", type=float, default=None)
    s.add_argument("--stop-method", default="atr", choices=["atr", "structure"])
    s.add_argument("--stop-atr", type=float, default=1.5)
    s.add_argument("--equity", type=float, default=None)
    s.add_argument("--risk", type=float, default=None, help="risk %% per trade")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_plan)

    s = sub.add_parser("backtest", help="Time Machine Simulator")
    s.add_argument("--strategy", default=None, help=f"comma list from: {', '.join(STRATEGIES)} (default: all)")
    s.add_argument("--tf", default=None)
    s.add_argument("--instruments", default=None)
    s.add_argument("--start", default=None)
    s.add_argument("--end", default=None)
    s.add_argument("--params", default=None, help='JSON overrides, e.g. \'{"rr": 3}\'')
    s.add_argument("--mc", action="store_true", help="Monte Carlo drawdown distribution")
    s.add_argument("--optimize", action="store_true", help="walk-forward grid search using config grid")
    s.set_defaults(fn=cmd_backtest)

    s = sub.add_parser("pipeline", help="scan → find → plan → backtest, in one run")
    s.add_argument("--tf", default=None)
    s.add_argument("--instruments", default=None)
    s.add_argument("--start", default=None)
    s.add_argument("--lookback", type=int, default=3)
    s.set_defaults(fn=cmd_pipeline)

    s = sub.add_parser("data", help="refresh or clear the data cache")
    s.add_argument("action", choices=["refresh", "clear"])
    s.add_argument("--instruments", default=None)
    s.add_argument("--tf", default=None)
    s.set_defaults(fn=cmd_data)

    s = sub.add_parser("dashboard", help="export the newest out/ runs as static dashboard data (data.json + assets)")
    s.add_argument("--dest", default="site/data", help="destination folder (default: site/data)")
    s.set_defaults(fn=cmd_dashboard)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    cfg = load_config(args.config)
    hub = DataHub(cfg, source=args.source)
    try:
        return args.fn(args, cfg, hub)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
