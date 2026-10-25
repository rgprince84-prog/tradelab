"""Entry & Exit Planner: turn an idea (instrument + direction) into a sized plan.

Outputs entry, stop, targets at 1R/2R/3R, position size for the configured
account/risk, and the cost drag (spread + slippage) expressed in R — the number
that tells you whether a stop is too tight to trade at retail spreads.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from .config import Config, Instrument
from .data import DataHub, last_closed
from .indicators import adx, atr, ema, rsi, swing_high, swing_low


def _round(x: float, d: int) -> float:
    return float(round(x, d))


def build_plan(
    hub: DataHub,
    cfg: Config,
    inst_key: str,
    direction: str,
    tf: str = "1h",
    entry: Optional[float] = None,
    stop: Optional[float] = None,
    target: Optional[float] = None,
    stop_method: str = "atr",
    stop_atr: float = 1.5,
    structure_bars: int = 10,
    rr_targets: List[float] = (1.0, 2.0, 3.0),
    equity: Optional[float] = None,
    risk_pct: Optional[float] = None,
    source: Optional[str] = None,
    stats: Optional[Dict[str, Any]] = None,
    strategy: Optional[str] = None,
    note: str = "",
) -> Dict[str, Any]:
    inst: Instrument = cfg.instrument(inst_key)
    d = 1 if direction.lower().startswith("l") or direction == "1" else -1
    df = last_closed(hub.get(inst, tf, source=source), tf)
    if len(df) < 50:
        raise RuntimeError(f"Not enough data for {inst_key} {tf}")
    last = df.iloc[-1]
    a = float(atr(df, 14).iloc[-1])
    e20, e50, e200 = (float(ema(df["close"], n).iloc[-1]) for n in (20, 50, 200))
    adx_v = float(adx(df, 14)["adx"].iloc[-1])
    rsi_v = float(rsi(df["close"], 14).iloc[-1])

    stop_given = stop is not None
    entry_px = float(entry) if entry is not None else float(last["close"])
    half_cost = (inst.spread / 2.0 + cfg.costs.slippage) * inst.pip
    fill = entry_px + d * half_cost  # what you'd actually pay

    if stop is None:
        if stop_method == "structure":
            lo, hi = float(swing_low(df, structure_bars).iloc[-1]), float(swing_high(df, structure_bars).iloc[-1])
            stop = lo - 0.25 * a if d == 1 else hi + 0.25 * a
        else:
            stop = fill - d * stop_atr * a
    stop = float(stop)
    risk = d * (fill - stop)
    if risk <= 0:
        raise ValueError("Stop is on the wrong side of the entry")

    equity = float(equity if equity is not None else cfg.account.equity)
    risk_pct = float(risk_pct if risk_pct is not None else cfg.account.risk_pct)
    risk_amount = equity * risk_pct / 100.0
    # convert account-currency risk into the instrument's quote currency
    rate_q2a = hub.fx_rate(inst.quote_ccy, cfg.account.currency) if inst.quote_ccy != cfg.account.currency else 1.0
    risk_quote = risk_amount / rate_q2a
    units = risk_quote / risk          # 1 unit moves 1 quote-ccy per 1.0 price change
    lots = units / inst.lot_size if inst.type == "fx" else units
    unit_dp = 0 if inst.type == "fx" else 2

    targets = {f"{r:g}R": _round(fill + d * r * risk, inst.digits) for r in rr_targets}
    if target is not None:
        targets["custom"] = _round(float(target), inst.digits)
        targets["custom_R"] = _round(d * (float(target) - fill) / risk, 2)

    round_trip_cost = 2 * half_cost
    cost_in_R = round_trip_cost / risk
    warnings: List[str] = []
    if cost_in_R > 0.15:
        warnings.append(f"Costs are {cost_in_R:.0%} of 1R — stop is tight relative to spread; widen the stop or trade a lower-spread instrument.")
    if risk < 0.5 * a:
        warnings.append(f"Stop is only {risk / a:.2f} ATR away — likely to be hit by noise on {tf}.")
    if risk > 4.0 * a:
        warnings.append(f"Stop is {risk / a:.1f} ATR away — position will be small and targets far; check the thesis justifies it.")
    if d == 1 and e50 < e200:
        warnings.append("Long against the EMA50/200 trend on this timeframe.")
    if d == -1 and e50 > e200:
        warnings.append("Short against the EMA50/200 trend on this timeframe.")
    if (d == 1 and rsi_v > 70) or (d == -1 and rsi_v < 30):
        warnings.append(f"RSI {rsi_v:.0f}: entering with momentum already stretched.")

    plan: Dict[str, Any] = {
        "instrument": inst.key,
        "strategy": strategy,
        "direction": "long" if d == 1 else "short",
        "timeframe": tf,
        "as_of_utc": df.index[-1].strftime("%Y-%m-%d %H:%M"),
        "last_close": _round(float(last["close"]), inst.digits),
        "entry": {"price": _round(entry_px, inst.digits), "expected_fill": _round(fill, inst.digits),
                   "type": "market" if entry is None else "limit/stop at level"},
        "stop": {"price": _round(stop, inst.digits), "distance": _round(risk, inst.digits),
                  "distance_pips": _round(inst.to_pips(risk), 1), "unit": inst.unit, "distance_atr": _round(risk / a, 2),
                  "method": "given" if stop_given else stop_method},
        "targets": targets,
        "position": {
            "units": int(round(units)) if inst.type == "fx" else _round(units, unit_dp),
            "lots": _round(lots, 2) if inst.type == "fx" else None,
            "unit_label": "units of base currency" if inst.type == "fx" else f"{inst.quote_ccy} per index point",
            "risk_amount": _round(risk_amount, 2), "account_ccy": cfg.account.currency,
            "risk_quote_ccy": _round(risk_quote, 2), "quote_ccy": inst.quote_ccy,
            "quote_to_account_rate": _round(rate_q2a, 6),
            "notional_quote": _round(units * fill, 0) if inst.type == "fx" else _round(units * fill, 0),
        },
        "costs": {
            "spread_pips": inst.spread, "slippage_pips_per_side": cfg.costs.slippage,
            "round_trip_pips": _round(inst.to_pips(round_trip_cost), 2),
            "cost_in_R": _round(cost_in_R, 3),
            "breakeven_move_pips": _round(inst.to_pips(round_trip_cost), 2),
        },
        "context": {"trend": "up" if e50 > e200 else "down", "ema20": _round(e20, inst.digits), "ema50": _round(e50, inst.digits),
                     "ema200": _round(e200, inst.digits), "adx": _round(adx_v, 1), "rsi": _round(rsi_v, 1), "atr": _round(a, inst.digits)},
        "warnings": warnings,
        "note": note,
    }
    if stats:
        plan["strategy_stats"] = stats
    return plan


def format_plan(plan: Dict[str, Any]) -> str:
    p = plan
    lines = [
        f"{p['instrument']} {p['direction'].upper()}  ({p['timeframe']}, as of {p['as_of_utc']} UTC)"
        + (f"  — {p['strategy']}" if p.get("strategy") else ""),
        f"  entry   {p['entry']['price']}  (expected fill {p['entry']['expected_fill']}, {p['entry']['type']})",
        f"  stop    {p['stop']['price']}  ({p['stop']['distance_pips']} {p['stop']['unit']}, {p['stop']['distance_atr']} ATR)",
        "  targets " + "  ".join(f"{k}={v}" for k, v in p["targets"].items()),
        f"  size    {p['position']['units']:,} {p['position']['unit_label']}"
        + (f" = {p['position']['lots']} lots" if p["position"]["lots"] is not None else "")
        + f"  risking {p['position']['account_ccy']} {p['position']['risk_amount']:,.2f}",
        f"  costs   {p['costs']['round_trip_pips']} {p['stop']['unit']} round trip = {p['costs']['cost_in_R']:.1%} of 1R",
        f"  context trend={p['context']['trend']} adx={p['context']['adx']} rsi={p['context']['rsi']}",
    ]
    if p.get("strategy_stats"):
        s = p["strategy_stats"]
        lines.append(
            f"  history {s.get('trades', 0)} trades, win {s.get('win_rate', float('nan')):.0%}, "
            f"expectancy {s.get('expectancy_R', float('nan')):+.2f}R, max DD {s.get('max_drawdown_R', float('nan')):.1f}R"
            + (f"  (t-stat {s['t_stat']:.1f})" if s.get("t_stat") is not None and s.get("t_stat") == s.get("t_stat") else "")
        )
        if "this_instrument_trades" in s:
            lines.append(
                f"          {p['instrument']} alone: {s['this_instrument_trades']} trades, "
                f"expectancy {s['this_instrument_expectancy_R']:+.2f}R"
            )
        if s.get("expectancy_R", 0) <= 0:
            lines.append("  ! This strategy has not been profitable after costs on this universe/timeframe. The setup is information, not a trade.")
    for w in p["warnings"]:
        lines.append(f"  ! {w}")
    if p.get("note"):
        lines.append(f"  why     {p['note']}")
    return "\n".join(lines)
