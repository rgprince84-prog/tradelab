"""Reports: charts + markdown + machine-readable outputs for a backtest run."""
from __future__ import annotations

import json
import math
import os
from typing import Any, Dict, Optional

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from .backtest import breakdown  # noqa: E402
from .config import Config  # noqa: E402


def _fmt(v: Any, col: str = "") -> str:
    if isinstance(v, (bool, np.bool_)):
        return str(bool(v))
    if isinstance(v, (int, np.integer)):
        return str(int(v)) if col in ("year", "entry_hour_utc") else f"{int(v):,}"
    if isinstance(v, (float, np.floating)):
        v = float(v)
        if math.isnan(v):
            return "n/a"
        if math.isinf(v):
            return "-inf" if v < 0 else "inf"
        if v.is_integer() and col in ("year", "entry_hour_utc", "trades", "is_trades"):
            return str(int(v))
        return f"{v:,.3f}" if abs(v) < 100 else f"{v:,.1f}"
    if isinstance(v, pd.Timestamp):
        return v.strftime("%Y-%m-%d %H:%M")
    return str(v)


def jsonable(obj: Any) -> Any:
    """Copy of obj that strict JSON parsers (browsers) accept: NaN/inf -> null, numpy -> python."""
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonable(v) for v in obj]
    if isinstance(obj, (bool, np.bool_)):
        return bool(obj)
    if isinstance(obj, (float, np.floating)):
        v = float(obj)
        return None if (math.isnan(v) or math.isinf(v)) else v
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    if isinstance(obj, pd.DataFrame):
        return jsonable(obj.reset_index().to_dict(orient="records"))
    return obj


def md_table(df: pd.DataFrame, index: bool = True) -> str:
    if df is None or len(df) == 0:
        return "_none_"
    d = df.reset_index() if index else df
    cols = [str(c) for c in d.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for i in range(len(d)):
        cells = [_fmt(d[c].iloc[i], str(c)) for c in d.columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def plot_equity(trades: pd.DataFrame, cfg: Config, path: str, title: str) -> None:
    if trades.empty:
        return
    t = trades.sort_values("exit_time")
    eq = cfg.account.equity + t["pnl"].cumsum()
    eq_r = t["r"].cumsum()
    peak = eq.cummax()
    dd = (eq - peak) / cfg.account.equity * 100.0

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]})
    ax1.plot(t["exit_time"], eq, color="#1f5fbf", lw=1.6)
    ax1.axhline(cfg.account.equity, color="grey", lw=0.8, ls="--")
    ax1.set_title(title, fontsize=13, fontweight="bold")
    ax1.set_ylabel(f"Equity ({cfg.account.currency})")
    ax1b = ax1.twinx()
    ax1b.plot(t["exit_time"], eq_r, color="#1f5fbf", alpha=0.0)
    ax1b.set_ylabel("Cumulative R")
    ax2.fill_between(t["exit_time"], dd, 0, color="#c0392b", alpha=0.35)
    ax2.set_ylabel("Drawdown %")
    ax2.set_xlabel("Exit time")
    for ax in (ax1, ax2):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.autofmt_xdate()
    plt.tight_layout()
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def plot_r_distribution(trades: pd.DataFrame, path: str, title: str) -> None:
    if trades.empty:
        return
    r = trades["r"].to_numpy()
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    bins = np.linspace(min(-3, r.min()), max(3, r.max()), 40)
    ax.hist(r[r > 0], bins=bins, color="#2e8b57", alpha=0.8, label="wins")
    ax.hist(r[r <= 0], bins=bins, color="#c0392b", alpha=0.8, label="losses")
    ax.axvline(r.mean(), color="black", lw=1.2, ls="--", label=f"mean {r.mean():+.2f}R")
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xlabel("R multiple (after costs)")
    ax.set_ylabel("Trades")
    ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def _metrics_block(m: Dict[str, Any]) -> str:
    if not m or m.get("trades", 0) == 0:
        return "_no trades_"
    keys = [
        ("trades", "Trades"), ("win_rate", "Win rate"), ("expectancy_R", "Expectancy (R)"), ("profit_factor", "Profit factor"),
        ("payoff_ratio", "Payoff ratio"), ("total_R", "Total R"), ("return_pct", "Return %"), ("max_drawdown_R", "Max drawdown (R)"),
        ("max_drawdown_pct", "Max drawdown %"), ("sharpe_daily", "Sharpe (daily)"), ("t_stat", "t-stat of mean R"),
        ("avg_bars_held", "Avg bars held"), ("max_consec_losses", "Max consecutive losses"), ("trades_per_month", "Trades / month"),
        ("first_trade", "First trade"), ("last_trade", "Last trade"),
    ]
    lines = ["| Metric | Value |", "|---|---|"]
    for k, label in keys:
        if k in m:
            v = m[k]
            if k == "win_rate":
                v = f"{v:.1%}"
            lines.append(f"| {label} | {_fmt(v) if not isinstance(v, str) else v} |")
    return "\n".join(lines)


def write_backtest_report(
    outdir: str,
    title: str,
    trades: pd.DataFrame,
    metrics: Dict[str, Any],
    cfg: Config,
    mc: Optional[Dict[str, Any]] = None,
    wf: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    notes: Optional[str] = None,
) -> str:
    os.makedirs(outdir, exist_ok=True)
    trades.to_csv(os.path.join(outdir, "trades.csv"), index=False)
    with open(os.path.join(outdir, "metrics.json"), "w") as f:
        json.dump(jsonable({"metrics": metrics, "monte_carlo": mc or {}, "params": params or {}}), f, indent=2, default=str)
    if not trades.empty:
        plot_equity(trades, cfg, os.path.join(outdir, "equity.png"), f"{title}: equity & drawdown")
        plot_r_distribution(trades, os.path.join(outdir, "r_distribution.png"), f"{title}: R distribution")

    md = [f"# {title}", ""]
    if params:
        md += ["**Parameters:** " + ", ".join(f"{k}={v}" for k, v in params.items()), ""]
    md += [
        f"**Costs modelled:** spread per instrument (config), slippage {cfg.costs.slippage} pips/pts per side, "
        f"commission {cfg.costs.commission} {cfg.account.currency}/round trip, same-bar SL+TP → {cfg.costs.same_bar_stop}.  ",
        f"**Sizing:** {cfg.account.risk_pct}% of {cfg.account.currency} {cfg.account.equity:,.0f} per trade"
        + (", compounding" if cfg.account.compounding else ", fixed") + ".",
        "",
        "## Headline", "", _metrics_block(metrics), "",
    ]
    if metrics.get("return_pct", 0) <= -100:
        md += ["> Return below -100%: with fixed-size risk this strategy would have emptied the account. Read the R figures; the % is just arithmetic.", ""]
    if metrics.get("trades", 0) and metrics["trades"] < cfg.backtest.min_trades_for_stats:
        md += [f"> Only {metrics['trades']} trades — below the {cfg.backtest.min_trades_for_stats} needed to say anything; treat every number above as noise.", ""]
    if not trades.empty:
        md += ["![equity](equity.png)", "", "![R distribution](r_distribution.png)", ""]
        md += ["## By instrument", "", md_table(breakdown(trades, "instrument")), ""]
        md += ["## By year", "", md_table(breakdown(trades, "year")), ""]
        md += ["## By direction", "", md_table(breakdown(trades, "direction")), ""]
        md += ["## By exit reason", "", md_table(breakdown(trades, "exit_reason")), ""]
        if trades["bars_held"].median() < 48:
            md += ["## By entry hour (UTC)", "", md_table(breakdown(trades, "entry_hour_utc")), ""]
    if mc:
        md += [
            "## Monte Carlo (" + str(mc["runs"]) + " runs)", "",
            "| | p50 | p95 |", "|---|---|---|",
            f"| Max drawdown, shuffled order (R) | {mc['shuffle_max_dd_R_p50']:.1f} | {mc['shuffle_max_dd_R_p95']:.1f} |",
            f"| Max drawdown, bootstrap (R) | {mc['bootstrap_max_dd_R_p50']:.1f} | {mc['bootstrap_max_dd_R_p95']:.1f} |",
            "",
            f"Bootstrap total R: p5 {mc['bootstrap_total_R_p05']:+.1f}, p50 {mc['bootstrap_total_R_p50']:+.1f}, p95 {mc['bootstrap_total_R_p95']:+.1f}. "
            f"Probability the edge is actually negative: **{mc['prob_total_R_negative']:.0%}**.",
            "",
        ]
    if wf:
        md += ["## Walk-forward", "", f"In-sample {wf['is_period'][0]} → {wf['is_period'][1]}, out-of-sample {wf['oos_period'][0]} → {wf['oos_period'][1]}.", ""]
        md += ["### Parameter grid (in-sample)", "", md_table(wf["grid"].head(15), index=False), ""]
        if wf.get("best_params"):
            md += [f"**Best in-sample params:** {wf['best_params']}", "", "### Out-of-sample with best params", "", _metrics_block(wf["oos_best"]), ""]
        md += ["### Out-of-sample with default params", "", _metrics_block(wf["oos_default"]), ""]
        if wf.get("best_params") and wf["oos_best"].get("trades", 0) and wf["grid"].iloc[0]["is_expectancy_R"] > 0:
            degr = wf["oos_best"].get("expectancy_R", 0) / wf["grid"].iloc[0]["is_expectancy_R"]
            md += [f"Out-of-sample expectancy is {degr:.0%} of in-sample. Under ~50% usually means the grid fitted noise.", ""]
    if notes:
        md += ["## Notes", "", notes, ""]
    md += [
        "---", "",
        "_Backtests use mid/bid prices from free feeds, one position per instrument, no overnight financing, no margin limits. "
        "They are research, not a forecast and not advice._",
    ]
    path = os.path.join(outdir, "report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    return path
