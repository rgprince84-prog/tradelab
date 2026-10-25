"""Chart Scanner: one-line snapshot per instrument x timeframe, ranked by interest.

The scanner *describes* — trend state, regime, volatility, compression,
breakouts, candle pattern, and which strategies currently have a signal.
It does not predict. The score only ranks what deserves a look first.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from .config import Config
from .data import DataHub, last_closed
from .indicators import features
from .setups import STRATEGIES, STRATEGY_TF, generate_signals


def _trend(close: float, e20: float, e50: float, e200: float) -> str:
    if close > e50 > e200:
        return "up"
    if close < e50 < e200:
        return "down"
    return "mixed"


def _regime(adx: float) -> str:
    if np.isnan(adx):
        return "n/a"
    if adx >= 25:
        return "trending"
    if adx >= 20:
        return "weak_trend"
    return "ranging"


def snapshot(df: pd.DataFrame, inst_key: str, tf: str, cfg: Config, inst, lookback_signals: int = 1) -> Optional[Dict[str, Any]]:
    if len(df) < 250:
        return None
    f = features(df)
    row, last = f.iloc[-1], df.iloc[-1]
    close = float(last["close"])
    atr = float(row["atr14"])
    if not atr or np.isnan(atr):
        return None
    trend = _trend(close, row["ema20"], row["ema50"], row["ema200"])
    regime = _regime(float(row["adx"]))
    don_rng = row["don_high"] - row["don_low"]
    don_pos = float((close - row["don_low"]) / don_rng) if don_rng > 0 else np.nan
    breakout = "up" if close > row["don_high_prev"] else "down" if close < row["don_low_prev"] else ""
    squeeze = bool(row["bb_width_pct"] <= 0.15) if not np.isnan(row["bb_width_pct"]) else False
    ema20_dist = float((close - row["ema20"]) / atr)
    rsi = float(row["rsi14"])

    # active setups on the last closed bar(s)
    active: List[str] = []
    for name in STRATEGIES:
        if tf not in STRATEGY_TF[name]:
            continue
        try:
            sig = generate_signals(df, inst, name, cfg)
        except Exception:
            continue
        recent = sig[sig.index >= df.index[-lookback_signals]]
        for t, s in recent.iterrows():
            active.append(f"{name}:{'long' if s['direction'] == 1 else 'short'}")

    score = 0.0
    score += min(3.0 * len(active), 6.0)
    score += 2.0 if breakout else 0.0
    score += 1.5 if squeeze else 0.0
    score += 1.0 if row["pattern"] else 0.0
    score += 1.0 if (trend != "mixed" and abs(ema20_dist) < 0.5) else 0.0  # sitting on the 20 EMA in a trend
    score += 1.0 if (rsi >= 70 or rsi <= 30) else 0.0
    score += 0.5 if regime == "trending" else 0.0

    return {
        "instrument": inst_key,
        "tf": tf,
        "last_bar_utc": df.index[-1].strftime("%Y-%m-%d %H:%M"),
        "close": round(close, inst.digits),
        "trend": trend,
        "regime": regime,
        "adx": round(float(row["adx"]), 1),
        "rsi": round(rsi, 1),
        "atr": round(atr, inst.digits),
        "atr_pct": round(atr / close * 100.0, 3),
        "bb_width_pctile": round(float(row["bb_width_pct"]) * 100.0, 0) if not np.isnan(row["bb_width_pct"]) else np.nan,
        "squeeze": squeeze,
        "donchian_pos": round(don_pos, 2) if not np.isnan(don_pos) else np.nan,
        "breakout_20": breakout,
        "ema20_dist_atr": round(ema20_dist, 2),
        "pattern": row["pattern"],
        "setups": ", ".join(active),
        "score": round(score, 1),
    }


def scan(
    hub: DataHub,
    cfg: Config,
    instruments: List[str],
    tfs: List[str],
    source: Optional[str] = None,
    lookback_signals: int = 1,
) -> pd.DataFrame:
    rows = []
    for key in instruments:
        inst = cfg.instrument(key)
        for tf in tfs:
            try:
                df = last_closed(hub.get(inst, tf, source=source), tf)
                snap = snapshot(df, key, tf, cfg, inst, lookback_signals)
                if snap:
                    rows.append(snap)
            except Exception as e:
                print(f"[scan] {key} {tf}: {e}")
    out = pd.DataFrame(rows)
    if len(out):
        out = out.sort_values(["score", "instrument"], ascending=[False, True]).reset_index(drop=True)
    return out


def find_setups(
    hub: DataHub,
    cfg: Config,
    instruments: List[str],
    tfs: List[str],
    strategies: Optional[List[str]] = None,
    lookback: int = 3,
    source: Optional[str] = None,
) -> pd.DataFrame:
    """Setup Finder: signals on the last `lookback` closed bars, newest first."""
    strategies = strategies or list(STRATEGIES)
    rows = []
    for key in instruments:
        inst = cfg.instrument(key)
        for tf in tfs:
            try:
                df = last_closed(hub.get(inst, tf, source=source), tf)
            except Exception as e:
                print(f"[find] {key} {tf}: {e}")
                continue
            if len(df) < 250:
                continue
            last_bar = df.index[-1]
            for name in strategies:
                if tf not in STRATEGY_TF[name]:
                    continue
                sig = generate_signals(df, inst, name, cfg)
                recent = sig[sig.index >= df.index[-lookback]]
                for t, s in recent.iterrows():
                    ref = float(df["close"].iloc[-1])
                    stop = s["stop"] if not pd.isna(s["stop"]) else ref - s["direction"] * s["stop_dist"]
                    target = s["target"]
                    if pd.isna(target) and not pd.isna(s["rr"]):
                        target = ref + s["direction"] * s["rr"] * abs(ref - stop)
                    rows.append(
                        {
                            "instrument": key, "tf": tf, "strategy": name,
                            "direction": "long" if s["direction"] == 1 else "short",
                            "signal_bar_utc": t.strftime("%Y-%m-%d %H:%M"),
                            "fresh": bool(t == last_bar),
                            "bars_ago": int((df.index > t).sum()),
                            "ref_price": round(ref, inst.digits),
                            "stop": round(float(stop), inst.digits),
                            "target": round(float(target), inst.digits) if target is not None and not pd.isna(target) else np.nan,
                            "stop_pips": round(inst.to_pips(abs(ref - float(stop))), 1),
                            "atr": round(float(s["atr"]), inst.digits),
                            "entry_type": s["entry_type"],
                            "note": s["note"],
                        }
                    )
    out = pd.DataFrame(rows)
    if len(out):
        out = out.sort_values(["fresh", "bars_ago", "instrument"], ascending=[False, True, True]).reset_index(drop=True)
    return out
