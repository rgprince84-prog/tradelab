"""Market data: fetch, cache, resample, label sessions.

Two free sources:
  * yfinance  — quick, ~2 years of hourly, full daily history. Mid-ish prices.
  * dukascopy — years of intraday (bid side), real tick volume, since ~2003 for FX.

All frames returned here are UTC-indexed with columns open/high/low/close/volume.
"""
from __future__ import annotations

import os
import warnings
from datetime import datetime, timedelta, timezone
from typing import Optional

import numpy as np
import pandas as pd

from .config import Config, Instrument, Session

warnings.filterwarnings("ignore", category=FutureWarning)
import logging
logging.getLogger("DUKASCRIPT").setLevel(logging.WARNING)

OHLCV = ["open", "high", "low", "close", "volume"]

# which base interval to fetch for each timeframe (4h is built from 1h)
BASE_TF = {"5m": "5m", "15m": "15m", "30m": "30m", "1h": "1h", "4h": "1h", "1d": "1d"}
TF_MINUTES = {"5m": 5, "15m": 15, "30m": 30, "1h": 60, "4h": 240, "1d": 1440}
# Yahoo's history limits per interval
YF_MAX_PERIOD = {"5m": "60d", "15m": "60d", "30m": "60d", "1h": "730d", "1d": "max"}

try:  # optional
    import pyarrow  # noqa: F401
    _PARQUET = True
except Exception:  # pragma: no cover
    _PARQUET = False


def _now_utc() -> pd.Timestamp:
    return pd.Timestamp.now(tz="UTC")


def normalise(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten yfinance's MultiIndex columns, lowercase, UTC index, clean rows."""
    if df is None or len(df) == 0:
        # keep the empty frame time-indexed so resample/last_closed/comparisons stay valid
        return pd.DataFrame(columns=OHLCV, index=pd.DatetimeIndex([], tz="UTC", name="time"))
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = df.columns.get_level_values(0)
    df = df.rename(columns={c: str(c).lower().replace(" ", "_") for c in df.columns})
    if "volume" not in df.columns:
        df["volume"] = 0.0
    df = df[[c for c in OHLCV if c in df.columns]].copy()
    idx = pd.DatetimeIndex(df.index)
    idx = idx.tz_localize("UTC") if idx.tz is None else idx.tz_convert("UTC")
    df.index = idx
    df.index.name = "time"
    df = df[~df.index.duplicated(keep="last")].sort_index()
    df = df.dropna(subset=["open", "high", "low", "close"])
    df = df[(df["high"] >= df["low"]) & (df["close"] > 0)]
    df["volume"] = df["volume"].fillna(0.0)
    return df.astype(float)


def resample(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    agg = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    out = df.resample(rule, label="left", closed="left", origin="start_day").agg(agg)
    return out.dropna(subset=["open", "high", "low", "close"])


def session_frame(index: pd.DatetimeIndex, sess: Session) -> pd.DataFrame:
    """Label each bar with its session membership.

    Columns: in_session (bool), sess_id (local date string or ''), pos (0-based
    position inside the session, -1 outside), is_last (bool, last bar of session).
    """
    local = index.tz_convert(sess.tz)
    mins = local.hour * 60 + local.minute
    in_sess = (mins >= sess.open_min) & (mins < sess.close_min)
    sess_id = pd.Series(np.where(in_sess, local.strftime("%Y-%m-%d"), ""), index=index)
    out = pd.DataFrame({"in_session": in_sess, "sess_id": sess_id}, index=index)
    pos = out[out["in_session"]].groupby("sess_id").cumcount()
    size = out[out["in_session"]].groupby("sess_id")["sess_id"].transform("size")
    out["pos"] = pos.reindex(index).fillna(-1).astype(int)
    out["remaining"] = (size - 1 - pos).reindex(index).fillna(-1).astype(int)  # bars left after this one
    out["is_last"] = (pos == (size - 1)).reindex(index).fillna(False).astype(bool)
    return out


class DataHub:
    """Fetch-and-cache front door for all market data."""

    def __init__(self, cfg: Config, source: Optional[str] = None):
        self.cfg = cfg
        self.source = (source or cfg.data.source).lower()
        self.cache_dir = cfg.data.cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        self._mem: dict = {}
        self._fx: dict = {}
        # Human-readable notes about degraded data this process has seen (fetch failures,
        # stale fallbacks). The pipeline writes them next to its outputs.
        self.problems: list = []

    # ------------------------------------------------------------------ public
    def get(
        self,
        inst: Instrument,
        tf: str = "1h",
        start: Optional[str] = None,
        end: Optional[str] = None,
        source: Optional[str] = None,
        refresh: bool = False,
    ) -> pd.DataFrame:
        if tf not in BASE_TF:
            raise ValueError(f"Unsupported timeframe {tf}. Use one of {list(BASE_TF)}")
        src = (source or self.source).lower()
        base = BASE_TF[tf]
        key = (src, inst.key, base)
        if key in self._mem and not refresh:
            df = self._mem[key]
        else:
            df = self._load(inst, base, src, refresh)
            self._mem[key] = df
        if tf == "4h":
            df = resample(df, "4h")
        if start:
            df = df[df.index >= pd.Timestamp(start, tz="UTC")]
        if end:
            df = df[df.index <= pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1)]
        return df

    def fx_rate(self, from_ccy: str, to_ccy: str) -> float:
        """Spot conversion from one currency to another (latest daily close).

        Prefers a configured instrument for the pair, which goes through the normal cache
        (so a rate-limited feed does not stop the planner), then falls back to a direct
        Yahoo download. Memoised for the life of the process.
        """
        if from_ccy == to_ccy:
            return 1.0
        key = (from_ccy, to_ccy)
        if key in self._fx:
            return self._fx[key]
        for inst in self.cfg.instruments.values():
            if inst.type != "fx":
                continue
            pair = (inst.base_ccy, inst.quote_ccy)
            if pair not in ((from_ccy, to_ccy), (to_ccy, from_ccy)):
                continue
            try:
                df = self.get(inst, "1d")
            except Exception:
                continue
            if len(df):
                px = float(df["close"].iloc[-1])
                rate = px if inst.base_ccy == from_ccy else 1.0 / px
                self._fx[key] = rate
                return rate
        import yfinance as yf

        for sym, invert in ((f"{from_ccy}{to_ccy}=X", False), (f"{to_ccy}{from_ccy}=X", True)):
            try:
                df = yf.download(sym, period="5d", interval="1d", progress=False, auto_adjust=False, threads=False)
                df = normalise(df)
                if len(df):
                    px = float(df["close"].iloc[-1])
                    rate = 1.0 / px if invert else px
                    self._fx[key] = rate
                    return rate
            except Exception:
                continue
        raise RuntimeError(f"Could not fetch conversion rate {from_ccy}->{to_ccy}")

    # ----------------------------------------------------------------- caching
    def _cache_path(self, src: str, inst: Instrument, base: str) -> str:
        ext = "parquet" if _PARQUET else "csv"
        return os.path.join(self.cache_dir, f"{src}_{inst.key}_{base}.{ext}")

    def _read_cache(self, path: str) -> Optional[pd.DataFrame]:
        if not os.path.exists(path):
            return None
        try:
            if path.endswith(".parquet"):
                df = pd.read_parquet(path)
            else:
                df = pd.read_csv(path, index_col=0)
                df.index = pd.to_datetime(df.index, utc=True)
            return normalise(df)
        except Exception:
            return None

    def _write_cache(self, path: str, df: pd.DataFrame) -> None:
        try:
            if path.endswith(".parquet"):
                df.to_parquet(path)
            else:
                df.to_csv(path)
        except Exception as e:  # cache is best-effort
            print(f"[data] cache write failed for {path}: {e}")

    def _is_stale(self, df: pd.DataFrame, base: str) -> bool:
        if df is None or df.empty:
            return True
        age = _now_utc() - df.index[-1]
        # The cache holds closed bars only (see _load), so re-fetch as soon as the next bar
        # should have closed, plus a little grace for the feed to publish it. A wider window
        # would make an hourly run scan one bar behind. Over a weekend this is one cheap
        # re-download; better than scanning Friday's data on Monday.
        tolerance = pd.Timedelta(minutes=TF_MINUTES[base] + max(10, TF_MINUTES[base] // 4))
        if base == "1d":
            tolerance = pd.Timedelta(hours=30)
        return age > tolerance

    def _load(self, inst: Instrument, base: str, src: str, refresh: bool) -> pd.DataFrame:
        path = self._cache_path(src, inst, base)
        cached = self._read_cache(path)
        if cached is not None and not refresh and not self._is_stale(cached, base):
            return cached
        failure = None
        try:
            if src == "dukascopy":
                since = None
                if cached is not None and len(cached):
                    since = cached.index[-1] - pd.Timedelta(minutes=3 * TF_MINUTES[base])
                fresh = self._fetch_dk(inst, base, since)
            else:
                fresh = self._fetch_yf(inst, base)
        except Exception as e:
            failure = f"fetch failed ({type(e).__name__}: {str(e)[:160]})"
            fresh = pd.DataFrame(columns=OHLCV)
        if failure is None and not len(fresh):
            failure = "feed returned no rows"
        if failure:
            have = (f"using cached bars to {cached.index[-1]:%Y-%m-%d %H:%M} UTC"
                    if cached is not None and len(cached) else "no cached bars")
            msg = f"{inst.key} {base} via {src}: {failure}; {have}"
            print(f"[data] {msg}")
            self.problems.append(msg)
        if cached is not None and len(cached):
            df = pd.concat([cached, fresh]) if len(fresh) else cached
            df = normalise(df)
        else:
            df = normalise(fresh)
        if len(df):
            # Persist closed bars only: a still-forming bar written now would be read back
            # as a complete bar by a later run that does not re-fetch.
            self._write_cache(path, last_closed(df, base))
        return df

    # ---------------------------------------------------------------- yfinance
    def _fetch_yf(self, inst: Instrument, base: str) -> pd.DataFrame:
        import yfinance as yf

        df = yf.download(
            inst.yf,
            period=YF_MAX_PERIOD[base],
            interval=base,
            progress=False,
            auto_adjust=False,
            threads=False,
        )
        df = normalise(df)
        if base == "1d":
            # Yahoo stamps daily bars at local midnight with no tz; keep as UTC dates.
            df.index = df.index.normalize()
        return df

    # --------------------------------------------------------------- dukascopy
    def _fetch_dk(self, inst: Instrument, base: str, since: Optional[pd.Timestamp]) -> pd.DataFrame:
        if not inst.dk:
            raise RuntimeError(f"{inst.key} has no Dukascopy code in config")
        import dukascopy_python as dk

        interval = {
            "5m": dk.INTERVAL_MIN_5,
            "15m": dk.INTERVAL_MIN_15,
            "30m": dk.INTERVAL_MIN_30,
            "1h": dk.INTERVAL_HOUR_1,
            "1d": dk.INTERVAL_DAY_1,
        }[base]
        start = (since or pd.Timestamp(self.cfg.data.dk_start, tz="UTC")).to_pydatetime()
        end = datetime.now(timezone.utc)
        rows_per_day = 1440 / TF_MINUTES[base]
        chunk_days = max(1, int(20_000 / rows_per_day))
        frames = []
        s = start
        while s < end:
            e = min(s + timedelta(days=chunk_days), end)
            try:
                part = dk.fetch(inst.dk, interval, dk.OFFER_SIDE_BID, s, e, max_retries=4)
                if part is not None and len(part):
                    frames.append(part)
            except Exception as ex:
                print(f"[data] dukascopy chunk {s.date()}..{e.date()} failed: {ex}")
            s = e
        if not frames:
            return pd.DataFrame(columns=OHLCV)
        df = pd.concat(frames)
        df.index = pd.DatetimeIndex(df.index)
        return normalise(df)


def last_closed(df: pd.DataFrame, tf: str) -> pd.DataFrame:
    """Drop a still-forming final bar so signals only use completed bars."""
    if df.empty:
        return df
    bar = pd.Timedelta(minutes=TF_MINUTES[tf])
    if _now_utc() - df.index[-1] < bar:
        return df.iloc[:-1]
    return df
