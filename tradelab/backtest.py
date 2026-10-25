"""Time Machine Simulator: replay signals bar by bar with honest fills.

Rules the engine enforces (these are what most reel demos skip):
  * a signal on bar t can only act from bar t+1 onward
  * market entries fill at the next bar's *open*, plus half-spread plus slippage
  * stop entries fill at max(level, open) for longs — gaps work against you
  * stop-loss and take-profit are tested against the bar's high/low; if both are
    touched in one bar the loss is booked (pessimistic), unless configured otherwise
  * exits pay half-spread plus slippage too
  * one position per instrument per strategy at a time; signals while in a trade are ignored
  * R is measured from the *actual* fill to the *initial* stop
"""
from __future__ import annotations

import itertools
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

from .config import Config, Instrument
from .data import DataHub, last_closed, session_frame
from .setups import STRATEGY_TF, generate_signals


@dataclass
class Trade:
    instrument: str
    strategy: str
    direction: int
    signal_time: pd.Timestamp
    entry_time: pd.Timestamp
    entry: float
    stop: float
    target: float
    exit_time: pd.Timestamp
    exit: float
    exit_reason: str
    bars_held: int
    risk: float          # initial risk per unit (price)
    r: float             # R-multiple after costs
    pnl: float           # account currency
    risk_amount: float   # account currency risked
    note: str


# ----------------------------------------------------------------------------
# Engine
# ----------------------------------------------------------------------------
def run_backtest(
    df: pd.DataFrame,
    signals: pd.DataFrame,
    inst: Instrument,
    cfg: Config,
    strategy: str = "",
    tf: str = "1h",
) -> List[Trade]:
    if df.empty or signals.empty:
        return []

    o = df["open"].to_numpy()
    h = df["high"].to_numpy()
    l = df["low"].to_numpy()
    c = df["close"].to_numpy()
    idx = df.index
    n = len(df)

    half_cost = (inst.spread / 2.0 + cfg.costs.slippage) * inst.pip
    pessimistic = cfg.costs.same_bar_stop == "pessimistic"
    equity = float(cfg.account.equity)
    risk_pct = float(cfg.account.risk_pct) / 100.0
    compounding = bool(cfg.account.compounding)
    commission = float(cfg.costs.commission)

    # session labels if any signal needs them
    sess_last = None
    sess_names = [s for s in signals["session"].dropna().unique()] if "session" in signals else []
    if sess_names:
        sess_last = session_frame(idx, cfg.sessions[str(sess_names[0]).upper()])["is_last"].to_numpy()

    # map signal time -> bar position
    pos_of = pd.Series(np.arange(n), index=idx)
    sig_pos = pos_of.reindex(signals.index).dropna().astype(int)
    sig_by_bar: Dict[int, list] = {}
    for (t, row), pidx in zip(signals.iterrows(), sig_pos.reindex(signals.index)):
        if pd.isna(pidx):
            continue
        sig_by_bar.setdefault(int(pidx), []).append(row)

    trades: List[Trade] = []
    position: Optional[dict] = None
    pending: Optional[dict] = None
    cur_equity = equity

    def _risk_amount() -> float:
        return (cur_equity if compounding else equity) * risk_pct

    def _close(pos: dict, i: int, price: float, reason: str) -> None:
        nonlocal cur_equity
        d = pos["dir"]
        fill = price - d * half_cost
        r = d * (fill - pos["entry"]) / pos["risk"]
        pnl = r * pos["risk_amount"] - commission
        cur_equity += pnl
        trades.append(
            Trade(
                instrument=inst.key, strategy=strategy, direction=d,
                signal_time=idx[pos["signal_bar"]], entry_time=idx[pos["entry_bar"]],
                entry=pos["entry"], stop=pos["stop0"], target=pos["target"] if pos["target"] is not None else float("nan"),
                exit_time=idx[i], exit=fill, exit_reason=reason, bars_held=i - pos["entry_bar"],
                risk=pos["risk"], r=r, pnl=pnl, risk_amount=pos["risk_amount"], note=pos["note"],
            )
        )

    def _open(sig: pd.Series, i: int, fill_mid: float, signal_bar: int) -> Optional[dict]:
        d = int(sig["direction"])
        fill = fill_mid + d * half_cost
        stop = sig["stop"]
        if pd.isna(stop):
            stop = fill - d * float(sig["stop_dist"])
        risk = d * (fill - stop)
        if not (risk > 0):
            return None  # gapped through the stop before entry; skip
        target = sig["target"]
        if pd.isna(target):
            target = fill + d * float(sig["rr"]) * risk if not pd.isna(sig["rr"]) else None
        else:
            target = float(target)
            if d * (target - fill) <= 0:  # target already passed; no edge left
                return None
        return {
            "dir": d, "entry": fill, "stop": float(stop), "stop0": float(stop), "target": target,
            "risk": float(risk), "risk_amount": _risk_amount(), "entry_bar": i, "signal_bar": signal_bar,
            "trail": None if pd.isna(sig["trail_atr"]) else float(sig["trail_atr"]) * float(sig["atr"]),
            "max_bars": None if pd.isna(sig["max_bars"]) else int(sig["max_bars"]),
            "flat_eod": bool(sig["flat_at_session_end"]), "note": str(sig["note"]),
        }

    def _check_exit(pos: dict, i: int, entry_bar_too: bool) -> bool:
        """Test SL/TP/time/session on bar i. Returns True if closed."""
        d = pos["dir"]
        stop, target = pos["stop"], pos["target"]
        hit_sl = (l[i] <= stop) if d == 1 else (h[i] >= stop)
        hit_tp = target is not None and ((h[i] >= target) if d == 1 else (l[i] <= target))
        if hit_sl and hit_tp and not pessimistic:
            hit_sl = False  # optimistic: assume target first
        if hit_sl:
            # gap through the stop fills at the open, otherwise at the stop
            px = o[i] if (d == 1 and o[i] < stop) or (d == -1 and o[i] > stop) else stop
            if entry_bar_too:
                px = stop  # entry happened at/after the open inside this bar
            moved = (d == 1 and stop > pos["stop0"]) or (d == -1 and stop < pos["stop0"])
            _close(pos, i, px, "trail_stop" if moved else "stop")
            return True
        if hit_tp:
            px = o[i] if (d == 1 and o[i] > target) or (d == -1 and o[i] < target) else target
            if entry_bar_too:
                px = target
            _close(pos, i, px, "target")
            return True
        if pos["flat_eod"] and sess_last is not None and sess_last[i]:
            _close(pos, i, c[i], "session_end")
            return True
        if pos["max_bars"] is not None and (i - pos["entry_bar"]) >= pos["max_bars"]:
            _close(pos, i, c[i], "time")
            return True
        if pos["trail"] is not None:  # ratchet the stop at bar close
            cand = c[i] - d * pos["trail"]
            if d == 1:
                pos["stop"] = max(pos["stop"], cand)
            else:
                pos["stop"] = min(pos["stop"], cand)
        return False

    for i in range(n):
        # 1) manage an open position with this bar
        if position is not None:
            if _check_exit(position, i, entry_bar_too=False):
                position = None
        # 2) try to fill a pending order on this bar
        if position is None and pending is not None:
            sig, sbar = pending["sig"], pending["signal_bar"]
            d = int(sig["direction"])
            filled_mid = None
            if sig["entry_type"] == "market":
                filled_mid = o[i]
                pending = None
            else:
                lvl = float(sig["entry_level"])
                if (d == 1 and h[i] >= lvl) or (d == -1 and l[i] <= lvl):
                    filled_mid = max(lvl, o[i]) if d == 1 else min(lvl, o[i])
                    pending = None
                elif i >= pending["expires"]:
                    pending = None
            if filled_mid is not None:
                position = _open(sig, i, filled_mid, sbar)
                if position is not None and _check_exit(position, i, entry_bar_too=True):
                    position = None
        # 3) new signals on this (closed) bar act from the next bar
        if position is None and pending is None and i in sig_by_bar and i + 1 < n:
            sig = sig_by_bar[i][0]  # first signal of the bar wins
            pending = {
                "sig": sig, "signal_bar": i,
                "expires": i + max(1, int(sig["valid_bars"] or 1)),
            }

    if position is not None:  # mark open position to the last close
        _close(position, n - 1, c[n - 1], "open_at_end")
    return trades


def trades_frame(trades: Iterable[Trade]) -> pd.DataFrame:
    rows = [asdict(t) for t in trades]
    if not rows:
        return pd.DataFrame(
            columns=[
                "instrument", "strategy", "direction", "signal_time", "entry_time", "entry", "stop", "target",
                "exit_time", "exit", "exit_reason", "bars_held", "risk", "r", "pnl", "risk_amount", "note",
            ]
        )
    df = pd.DataFrame(rows).sort_values("exit_time").reset_index(drop=True)
    return df


# ----------------------------------------------------------------------------
# Metrics
# ----------------------------------------------------------------------------
def _max_drawdown(series: np.ndarray) -> float:
    eq = np.concatenate([[0.0], np.cumsum(series)])
    peak = np.maximum.accumulate(eq)
    return float((peak - eq).max()) if len(eq) else 0.0


def _streak(signs: np.ndarray, target: int) -> int:
    best = cur = 0
    for s in signs:
        cur = cur + 1 if s == target else 0
        best = max(best, cur)
    return best


def compute_metrics(trades: pd.DataFrame, cfg: Config) -> Dict[str, Any]:
    equity = float(cfg.account.equity)
    out: Dict[str, Any] = {"trades": int(len(trades))}
    if trades.empty:
        return out
    r = trades["r"].to_numpy()
    pnl = trades["pnl"].to_numpy()
    wins = r[r > 0]
    losses = r[r <= 0]
    out.update(
        {
            "win_rate": float(len(wins) / len(r)),
            "expectancy_R": float(r.mean()),
            "median_R": float(np.median(r)),
            "avg_win_R": float(wins.mean()) if len(wins) else 0.0,
            "avg_loss_R": float(losses.mean()) if len(losses) else 0.0,
            "payoff_ratio": float(wins.mean() / abs(losses.mean())) if len(wins) and len(losses) and losses.mean() != 0 else float("nan"),
            "profit_factor": float(wins.sum() / abs(losses.sum())) if losses.sum() != 0 else float("inf"),
            "total_R": float(r.sum()),
            "total_pnl": float(pnl.sum()),
            "return_pct": float(pnl.sum() / equity * 100.0),
            "max_drawdown_R": _max_drawdown(r),
            "max_drawdown_pct": _max_drawdown(pnl) / equity * 100.0,
            "avg_bars_held": float(trades["bars_held"].mean()),
            "max_consec_losses": _streak(np.sign(r), -1),
            "max_consec_wins": _streak(np.sign(r), 1),
            "t_stat": float(r.mean() / (r.std(ddof=1) / math.sqrt(len(r)))) if len(r) > 1 and r.std(ddof=1) > 0 else float("nan"),
        }
    )
    # Sharpe from daily P&L (zero on days without exits)
    daily = trades.set_index("exit_time")["pnl"].groupby(pd.Grouper(freq="1D")).sum()
    daily = daily.reindex(pd.date_range(daily.index.min(), daily.index.max(), freq="B", tz="UTC")).fillna(0.0)
    rets = daily / equity
    out["sharpe_daily"] = float(rets.mean() / rets.std(ddof=1) * math.sqrt(252)) if rets.std(ddof=1) > 0 else float("nan")
    span_days = max((trades["exit_time"].max() - trades["entry_time"].min()).days, 1)
    out["trades_per_month"] = float(len(r) / (span_days / 30.44))
    out["first_trade"] = str(trades["entry_time"].min().date())
    out["last_trade"] = str(trades["exit_time"].max().date())
    return out


def breakdown(trades: pd.DataFrame, by: str) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame()
    t = trades.copy()
    if by == "year":
        t["year"] = t["exit_time"].dt.year
    elif by == "entry_hour_utc":
        t["entry_hour_utc"] = t["entry_time"].dt.hour
    elif by == "direction":
        t["direction"] = t["direction"].map({1: "long", -1: "short"})
    g = t.groupby(by)["r"]
    out = pd.DataFrame(
        {
            "trades": g.size(),
            "win_rate": g.apply(lambda s: (s > 0).mean()),
            "expectancy_R": g.mean(),
            "total_R": g.sum(),
            "max_dd_R": g.apply(lambda s: _max_drawdown(s.to_numpy())),
        }
    )
    return out.round(3)


# ----------------------------------------------------------------------------
# Monte Carlo
# ----------------------------------------------------------------------------
def monte_carlo(r: np.ndarray, runs: int = 1000, seed: int = 7) -> Dict[str, Any]:
    r = np.asarray(r, dtype=float)
    if len(r) < 5:
        return {}
    rng = np.random.default_rng(seed)
    dd_shuffle, dd_boot, fin_boot = [], [], []
    for _ in range(runs):
        s = rng.permutation(r)
        dd_shuffle.append(_max_drawdown(s))
        b = rng.choice(r, size=len(r), replace=True)
        dd_boot.append(_max_drawdown(b))
        fin_boot.append(b.sum())
    p = lambda a, q: float(np.percentile(a, q))
    return {
        "runs": runs,
        "shuffle_max_dd_R_p50": p(dd_shuffle, 50),
        "shuffle_max_dd_R_p95": p(dd_shuffle, 95),
        "bootstrap_max_dd_R_p50": p(dd_boot, 50),
        "bootstrap_max_dd_R_p95": p(dd_boot, 95),
        "bootstrap_total_R_p05": p(fin_boot, 5),
        "bootstrap_total_R_p50": p(fin_boot, 50),
        "bootstrap_total_R_p95": p(fin_boot, 95),
        "prob_total_R_negative": float(np.mean(np.asarray(fin_boot) < 0)),
    }


# ----------------------------------------------------------------------------
# Running strategies across instruments
# ----------------------------------------------------------------------------
def run_strategy(
    hub: DataHub,
    cfg: Config,
    strategy: str,
    instruments: List[str],
    tf: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    overrides: Optional[Dict[str, Any]] = None,
    source: Optional[str] = None,
    quiet: bool = False,
) -> pd.DataFrame:
    all_trades: List[Trade] = []
    for key in instruments:
        inst = cfg.instrument(key)
        if inst.type == "index" and tf == "1d" and strategy == "session_orb":
            continue
        try:
            df = hub.get(inst, tf, source=source)
        except Exception as e:
            if not quiet:
                print(f"[backtest] {key}: data error {e}")
            continue
        df = last_closed(df, tf)
        # signals need warm-up history before `start`; slice trades afterwards
        sig = generate_signals(df, inst, strategy, cfg, overrides)
        if sig.empty:  # too little history (or a feed outage) for this instrument: nothing to replay
            if not quiet:
                print(f"[backtest] {strategy:18} {key:7} {tf}: no signals ({len(df)} bars)")
            continue
        if start:
            sig = sig[sig.index >= pd.Timestamp(start, tz="UTC")]
        if end:
            sig = sig[sig.index <= pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1)]
        if sig.empty:
            continue
        # replay only from a bit before the first signal to keep it fast
        first = sig.index[0]
        df_run = df[df.index >= first - pd.Timedelta(days=1)]
        if end:
            df_run = df_run[df_run.index <= pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1)]
        all_trades.extend(run_backtest(df_run, sig, inst, cfg, strategy=strategy, tf=tf))
        if not quiet:
            print(f"[backtest] {strategy:18} {key:7} {tf}: {len(sig):4} signals")
    return trades_frame(all_trades)


def walk_forward(
    hub: DataHub,
    cfg: Config,
    strategy: str,
    instruments: List[str],
    tf: str,
    start: str,
    end: Optional[str],
    oos_fraction: float,
    grid: Dict[str, list],
    source: Optional[str] = None,
) -> Dict[str, Any]:
    """Grid-search params in-sample, test the winner (and defaults) out-of-sample.

    Score = expectancy_R * sqrt(trades): rewards edge but punishes tiny samples.
    """
    end_ts = pd.Timestamp(end, tz="UTC") if end else pd.Timestamp.now(tz="UTC").normalize()
    start_ts = pd.Timestamp(start, tz="UTC")
    split = start_ts + (end_ts - start_ts) * (1.0 - oos_fraction)
    is_end, oos_start = str(split.date()), str((split + pd.Timedelta(days=1)).date())
    keys = list(grid)
    rows = []
    for combo in itertools.product(*[grid[k] for k in keys]):
        params = dict(zip(keys, combo))
        t = run_strategy(hub, cfg, strategy, instruments, tf, start, is_end, params, source, quiet=True)
        m = compute_metrics(t, cfg)
        score = m.get("expectancy_R", float("nan")) * math.sqrt(max(m["trades"], 1)) if m["trades"] >= 10 else float("-inf")
        rows.append({**params, "is_trades": m["trades"], "is_expectancy_R": m.get("expectancy_R", float("nan")),
                     "is_total_R": m.get("total_R", float("nan")), "is_max_dd_R": m.get("max_drawdown_R", float("nan")), "score": score})
    table = pd.DataFrame(rows).sort_values("score", ascending=False).reset_index(drop=True)
    best = {k: table.iloc[0][k] for k in keys} if len(table) and np.isfinite(table.iloc[0]["score"]) else None
    result: Dict[str, Any] = {"is_period": [start, is_end], "oos_period": [oos_start, end or str(end_ts.date())], "grid": table}
    if best is not None:
        best = {k: (float(v) if isinstance(v, (np.floating, float)) else int(v) if isinstance(v, (np.integer,)) else v) for k, v in best.items()}
        t_oos = run_strategy(hub, cfg, strategy, instruments, tf, oos_start, end, best, source, quiet=True)
        result["best_params"] = best
        result["oos_best"] = compute_metrics(t_oos, cfg)
        result["oos_best_trades"] = t_oos
    t_def = run_strategy(hub, cfg, strategy, instruments, tf, oos_start, end, None, source, quiet=True)
    result["oos_default"] = compute_metrics(t_def, cfg)
    return result
