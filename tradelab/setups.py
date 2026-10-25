"""Setup Finder: rule-based strategies that emit signals on *closed* bars.

A signal row describes what to do on the bars *after* the signal bar:

    direction        +1 long / -1 short
    entry_type       'market' (fill at next bar's open) | 'stop' (pending order)
    entry_level      price for stop orders (NaN for market)
    valid_bars       how long a stop order stays working
    stop             absolute initial stop price   (or NaN -> use stop_dist)
    stop_dist        stop distance from the fill   (used when stop is NaN)
    target           absolute take-profit price    (or NaN -> use rr)
    rr               take-profit as a multiple of initial risk (NaN -> no target)
    trail_atr        trailing stop in ATR multiples (NaN -> none)
    atr              ATR at the signal bar
    max_bars         time stop (NaN -> none)
    flat_at_session_end  close at the last bar of the session
    session          session name used for the above
    note             human-readable reason

Adding a strategy = write a function with this signature and register it in
STRATEGIES. Use only information available at the signal bar.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, Optional

import numpy as np
import pandas as pd

from . import indicators as ind
from .config import Config, Instrument
from .data import session_frame

SIGNAL_COLUMNS = [
    "direction", "entry_type", "entry_level", "valid_bars", "stop", "stop_dist",
    "target", "rr", "trail_atr", "atr", "max_bars", "flat_at_session_end", "session", "note",
]


def _empty() -> pd.DataFrame:
    # time-indexed even when empty, so callers can filter by timestamp without a TypeError
    return pd.DataFrame(columns=SIGNAL_COLUMNS, index=pd.DatetimeIndex([], tz="UTC", name="time"))


def _frame(index: pd.DatetimeIndex, **cols) -> pd.DataFrame:
    base = {
        "direction": 0, "entry_type": "market", "entry_level": np.nan, "valid_bars": 0,
        "stop": np.nan, "stop_dist": np.nan, "target": np.nan, "rr": np.nan, "trail_atr": np.nan,
        "atr": np.nan, "max_bars": np.nan, "flat_at_session_end": False, "session": None, "note": "",
    }
    base.update(cols)
    out = pd.DataFrame(base, index=index)
    return out[SIGNAL_COLUMNS]


# ----------------------------------------------------------------------------
# 1. EMA pullback (trend continuation)
# ----------------------------------------------------------------------------
def ema_pullback(df: pd.DataFrame, inst: Instrument, p: Dict[str, Any], cfg: Config) -> pd.DataFrame:
    c, o, h, l = df["close"], df["open"], df["high"], df["low"]
    ema_f = ind.ema(c, int(p.get("ema_fast", 20)))
    ema_m = ind.ema(c, int(p.get("ema_mid", 50)))
    ema_s = ind.ema(c, int(p.get("ema_slow", 200)))
    rsi = ind.rsi(c, 14)
    atr = ind.atr(df, 14)
    n = int(p.get("pullback_bars", 3))
    rsi_max = float(p.get("rsi_max", 70))
    buf = float(p.get("sl_atr_buffer", 0.5))

    uptrend = (ema_m > ema_s) & (c > ema_m)
    downtrend = (ema_m < ema_s) & (c < ema_m)
    touched_down = l.rolling(n, min_periods=1).min() <= ema_f      # pulled back into EMA20
    touched_up = h.rolling(n, min_periods=1).max() >= ema_f
    bull_rev = (c > ema_f) & (c > h.shift(1)) & (c > o)             # closes back above, takes prior high
    bear_rev = (c < ema_f) & (c < l.shift(1)) & (c < o)

    long_sig = uptrend & touched_down & bull_rev & (rsi < rsi_max)
    short_sig = downtrend & touched_up & bear_rev & (rsi > 100 - rsi_max)

    swing_lo = l.rolling(n, min_periods=1).min()
    swing_hi = h.rolling(n, min_periods=1).max()

    longs = _frame(
        df.index[long_sig],
        direction=1, stop=(swing_lo - buf * atr)[long_sig].values, rr=p.get("rr"),
        atr=atr[long_sig].values, max_bars=p.get("max_bars"),
        note="pullback to EMA%d in up-trend, bullish close" % int(p.get("ema_fast", 20)),
    )
    shorts = _frame(
        df.index[short_sig],
        direction=-1, stop=(swing_hi + buf * atr)[short_sig].values, rr=p.get("rr"),
        atr=atr[short_sig].values, max_bars=p.get("max_bars"),
        note="pullback to EMA%d in down-trend, bearish close" % int(p.get("ema_fast", 20)),
    )
    return pd.concat([longs, shorts]).sort_index()


# ----------------------------------------------------------------------------
# 2. Donchian breakout (trend following, ATR trailing stop)
# ----------------------------------------------------------------------------
def donchian_breakout(df: pd.DataFrame, inst: Instrument, p: Dict[str, Any], cfg: Config) -> pd.DataFrame:
    c = df["close"]
    n = int(p.get("lookback", 20))
    don = ind.donchian(df, n)
    adx = ind.adx(df, 14)["adx"]
    ema50 = ind.ema(c, 50)
    atr = ind.atr(df, 14)
    adx_min = float(p.get("adx_min", 20))
    sl_atr = float(p.get("sl_atr", 2.0))

    long_sig = (c > don["don_high_prev"]) & (adx > adx_min) & (c > ema50)
    short_sig = (c < don["don_low_prev"]) & (adx > adx_min) & (c < ema50)
    # only the first bar of a breakout (previous close was inside the channel)
    long_sig &= ~(c.shift(1) > don["don_high_prev"].shift(1))
    short_sig &= ~(c.shift(1) < don["don_low_prev"].shift(1))

    rr = p.get("rr")
    rr = np.nan if rr in (None, "null") else float(rr)
    longs = _frame(
        df.index[long_sig], direction=1, stop_dist=(sl_atr * atr)[long_sig].values, rr=rr,
        trail_atr=p.get("trail_atr", np.nan), atr=atr[long_sig].values, max_bars=p.get("max_bars"),
        note=f"close above {n}-bar high, ADX>{adx_min:g}",
    )
    shorts = _frame(
        df.index[short_sig], direction=-1, stop_dist=(sl_atr * atr)[short_sig].values, rr=rr,
        trail_atr=p.get("trail_atr", np.nan), atr=atr[short_sig].values, max_bars=p.get("max_bars"),
        note=f"close below {n}-bar low, ADX>{adx_min:g}",
    )
    return pd.concat([longs, shorts]).sort_index()


# ----------------------------------------------------------------------------
# 3. Bollinger mean reversion (ranging regime only)
# ----------------------------------------------------------------------------
def bb_mean_reversion(df: pd.DataFrame, inst: Instrument, p: Dict[str, Any], cfg: Config) -> pd.DataFrame:
    c, l, h = df["close"], df["low"], df["high"]
    bb = ind.bollinger(c, int(p.get("period", 20)), float(p.get("std", 2.0)))
    adx = ind.adx(df, 14)["adx"]
    atr = ind.atr(df, 14)
    adx_max = float(p.get("adx_max", 20))
    buf = float(p.get("sl_atr_buffer", 0.5))

    ranging = adx < adx_max
    long_sig = ranging & (c.shift(1) < bb["bb_lower"].shift(1)) & (c > bb["bb_lower"]) & (c < bb["bb_mid"])
    short_sig = ranging & (c.shift(1) > bb["bb_upper"].shift(1)) & (c < bb["bb_upper"]) & (c > bb["bb_mid"])

    lo2 = pd.concat([l, l.shift(1)], axis=1).min(axis=1)
    hi2 = pd.concat([h, h.shift(1)], axis=1).max(axis=1)
    longs = _frame(
        df.index[long_sig], direction=1, stop=(lo2 - buf * atr)[long_sig].values,
        target=bb["bb_mid"][long_sig].values, atr=atr[long_sig].values, max_bars=p.get("max_bars"),
        note=f"re-entry above lower band, ADX<{adx_max:g}",
    )
    shorts = _frame(
        df.index[short_sig], direction=-1, stop=(hi2 + buf * atr)[short_sig].values,
        target=bb["bb_mid"][short_sig].values, atr=atr[short_sig].values, max_bars=p.get("max_bars"),
        note=f"re-entry below upper band, ADX<{adx_max:g}",
    )
    return pd.concat([longs, shorts]).sort_index()


# ----------------------------------------------------------------------------
# 4. Session opening-range breakout
# ----------------------------------------------------------------------------
def session_orb(df: pd.DataFrame, inst: Instrument, p: Dict[str, Any], cfg: Config) -> pd.DataFrame:
    sess = cfg.session_for(inst, p.get("session"))
    sf = session_frame(df.index, sess)
    rb = int(p.get("range_bars", 1))
    max_range_atr = float(p.get("max_range_atr", 1.5))
    atr = ind.atr(df, 14)

    in_s = sf["in_session"].values
    sid = sf["sess_id"].values
    pos = sf["pos"].values
    remaining = sf["remaining"].values
    min_left = int(p.get("min_bars_left", 2))  # don't enter with fewer bars than this left in the session
    rng_hi = pd.Series(np.where(pos < rb, df["high"].values, np.nan), index=df.index)
    rng_lo = pd.Series(np.where(pos < rb, df["low"].values, np.nan), index=df.index)
    # opening range per session, forward-filled through the session
    tmp = pd.DataFrame({"sid": sid, "hi": rng_hi, "lo": rng_lo}, index=df.index)
    tmp = tmp[in_s]
    rh = tmp.groupby("sid")["hi"].transform("max")
    rl = tmp.groupby("sid")["lo"].transform("min")
    range_high = rh.reindex(df.index)
    range_low = rl.reindex(df.index)
    range_size = range_high - range_low

    c = df["close"]
    after_range = in_s & (pos >= rb) & (remaining >= min_left)
    ok_size = (range_size <= max_range_atr * atr) & (range_size > 0)
    long_raw = after_range & (c > range_high) & ok_size
    short_raw = after_range & (c < range_low) & ok_size

    # first breakout bar per session and direction only
    def first_per_session(mask: pd.Series) -> pd.Series:
        s = pd.Series(np.asarray(mask, dtype=bool), index=df.index)
        grp = pd.Series(sid, index=df.index)
        running = s.astype(int).groupby(grp).cumsum()
        return s & (running == 1)

    long_sig = first_per_session(long_raw)
    short_sig = first_per_session(short_raw)

    rr = p.get("rr")
    rr = np.nan if rr in (None, "null") else float(rr)
    flat = bool(p.get("flat_at_session_end", True))
    longs = _frame(
        df.index[long_sig], direction=1, stop=range_low[long_sig].values, rr=rr, atr=atr[long_sig].values,
        flat_at_session_end=flat, session=sess.name,
        note=f"{sess.name} opening-range ({rb} bar) breakout up",
    )
    shorts = _frame(
        df.index[short_sig], direction=-1, stop=range_high[short_sig].values, rr=rr, atr=atr[short_sig].values,
        flat_at_session_end=flat, session=sess.name,
        note=f"{sess.name} opening-range ({rb} bar) breakout down",
    )
    return pd.concat([longs, shorts]).sort_index()


STRATEGIES: Dict[str, Callable[[pd.DataFrame, Instrument, Dict[str, Any], Config], pd.DataFrame]] = {
    "ema_pullback": ema_pullback,
    "donchian_breakout": donchian_breakout,
    "bb_mean_reversion": bb_mean_reversion,
    "session_orb": session_orb,
}

# which timeframes each strategy is meant for
STRATEGY_TF = {
    "ema_pullback": ["1h", "4h", "1d"],
    "donchian_breakout": ["1h", "4h", "1d"],
    "bb_mean_reversion": ["1h", "4h", "1d"],
    "session_orb": ["5m", "15m", "30m", "1h"],
}


def generate_signals(
    df: pd.DataFrame, inst: Instrument, strategy: str, cfg: Config, overrides: Optional[Dict[str, Any]] = None
) -> pd.DataFrame:
    if strategy not in STRATEGIES:
        raise KeyError(f"Unknown strategy '{strategy}'. Known: {', '.join(STRATEGIES)}")
    if len(df) < 250:
        return _empty()
    params = cfg.strategy_params(strategy, overrides)
    sig = STRATEGIES[strategy](df, inst, params, cfg)
    sig = sig.dropna(subset=["atr"])
    sig = sig[sig["direction"] != 0]
    sig.index.name = "time"
    return sig
