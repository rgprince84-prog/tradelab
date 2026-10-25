"""Technical indicators in plain pandas/numpy.

Every function here is *causal*: the value at bar t uses only bars <= t.
That property is what keeps the scanner, setup finder and backtester free
of look-ahead bias, so keep it when adding indicators.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


# ----------------------------------------------------------------------------
# Moving averages & oscillators
# ----------------------------------------------------------------------------
def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False, min_periods=n).mean()


def sma(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n, min_periods=n).mean()


def wilder(s: pd.Series, n: int) -> pd.Series:
    """Wilder's smoothing (used by RSI, ATR, ADX)."""
    return s.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()


def rsi(close: pd.Series, n: int = 14) -> pd.Series:
    delta = close.diff()
    up = delta.clip(lower=0.0)
    down = (-delta).clip(lower=0.0)
    avg_up = wilder(up, n)
    avg_down = wilder(down, n)
    rs = avg_up / avg_down.replace(0.0, np.nan)
    out = 100.0 - 100.0 / (1.0 + rs)
    out = out.where(avg_down != 0.0, 100.0)  # no losses in window -> 100
    out = out.where(~(avg_up.eq(0.0) & avg_down.eq(0.0)), 50.0)  # flat -> 50
    return out


def true_range(df: pd.DataFrame) -> pd.Series:
    prev_close = df["close"].shift(1)
    tr = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr


def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    return wilder(true_range(df), n)


def adx(df: pd.DataFrame, n: int = 14) -> pd.DataFrame:
    """Returns DataFrame with columns adx, di_plus, di_minus."""
    high, low = df["high"], df["low"]
    up_move = high.diff()
    down_move = -low.diff()
    plus_dm = pd.Series(np.where((up_move > down_move) & (up_move > 0), up_move, 0.0), index=df.index)
    minus_dm = pd.Series(np.where((down_move > up_move) & (down_move > 0), down_move, 0.0), index=df.index)
    tr_s = wilder(true_range(df), n)
    di_plus = 100.0 * wilder(plus_dm, n) / tr_s
    di_minus = 100.0 * wilder(minus_dm, n) / tr_s
    dx = 100.0 * (di_plus - di_minus).abs() / (di_plus + di_minus).replace(0.0, np.nan)
    out = pd.DataFrame({"adx": wilder(dx, n), "di_plus": di_plus, "di_minus": di_minus})
    return out


def bollinger(close: pd.Series, n: int = 20, k: float = 2.0) -> pd.DataFrame:
    mid = sma(close, n)
    sd = close.rolling(n, min_periods=n).std(ddof=0)
    upper = mid + k * sd
    lower = mid - k * sd
    width = (upper - lower) / mid
    return pd.DataFrame({"bb_mid": mid, "bb_upper": upper, "bb_lower": lower, "bb_width": width})


def donchian(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """Prior-n-bar channel (excludes the current bar) so a breakout can be
    tested as close > don_high_prev without self-reference."""
    hh = df["high"].rolling(n, min_periods=n).max()
    ll = df["low"].rolling(n, min_periods=n).min()
    return pd.DataFrame(
        {
            "don_high": hh,
            "don_low": ll,
            "don_high_prev": hh.shift(1),
            "don_low_prev": ll.shift(1),
        }
    )


def swing_low(df: pd.DataFrame, n: int = 10) -> pd.Series:
    return df["low"].rolling(n, min_periods=1).min()


def swing_high(df: pd.DataFrame, n: int = 10) -> pd.Series:
    return df["high"].rolling(n, min_periods=1).max()


def pct_rank(s: pd.Series, lookback: int = 120) -> pd.Series:
    """Percentile rank (0-1) of the current value within the trailing window."""
    return s.rolling(lookback, min_periods=max(20, lookback // 4)).rank(pct=True)


# ----------------------------------------------------------------------------
# Candle patterns (label for the *last* bar of a frame, or a Series)
# ----------------------------------------------------------------------------
def candle_patterns(df: pd.DataFrame) -> pd.Series:
    o, h, l, c = df["open"], df["high"], df["low"], df["close"]
    po, pc, ph, pl = o.shift(1), c.shift(1), h.shift(1), l.shift(1)
    body = (c - o).abs()
    rng = (h - l).replace(0.0, np.nan)
    upper_wick = h - np.maximum(o, c)
    lower_wick = np.minimum(o, c) - l

    bull_engulf = (pc < po) & (c > o) & (c >= po) & (o <= pc) & (body > (pc - po).abs())
    bear_engulf = (pc > po) & (c < o) & (c <= po) & (o >= pc) & (body > (pc - po).abs())
    hammer = (lower_wick >= 2.0 * body) & (upper_wick <= body) & ((c - l) / rng >= 0.66)
    shooting_star = (upper_wick >= 2.0 * body) & (lower_wick <= body) & ((h - c) / rng >= 0.66)
    inside = (h < ph) & (l > pl)

    label = pd.Series("", index=df.index, dtype=object)
    label = label.mask(inside, "inside_bar")
    label = label.mask(hammer, "hammer")
    label = label.mask(shooting_star, "shooting_star")
    label = label.mask(bull_engulf, "bullish_engulfing")
    label = label.mask(bear_engulf, "bearish_engulfing")
    return label


# ----------------------------------------------------------------------------
# Feature bundle used by the scanner
# ----------------------------------------------------------------------------
def features(df: pd.DataFrame) -> pd.DataFrame:
    """Standard indicator frame aligned to df.index."""
    out = pd.DataFrame(index=df.index)
    out["ema20"] = ema(df["close"], 20)
    out["ema50"] = ema(df["close"], 50)
    out["ema200"] = ema(df["close"], 200)
    out["rsi14"] = rsi(df["close"], 14)
    out["atr14"] = atr(df, 14)
    out = out.join(adx(df, 14))
    out = out.join(bollinger(df["close"], 20, 2.0))
    out = out.join(donchian(df, 20))
    out["bb_width_pct"] = pct_rank(out["bb_width"], 120)
    out["pattern"] = candle_patterns(df)
    return out
