"""Configuration: instruments, sessions, account, costs, strategy params.

Everything comes from config.yaml so strategy rules and cost assumptions are
visible and editable without touching code.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class Instrument:
    key: str
    type: str                 # 'fx' | 'index'
    yf: str                   # Yahoo Finance symbol
    dk: Optional[str]         # Dukascopy instrument code (None if unavailable)
    pip: float                # price value of one pip (fx) or one index point
    spread: float             # typical retail spread, in pips / points
    base_ccy: str
    quote_ccy: str
    session: str              # default session for intraday logic (ORB, session flat)
    digits: int = 5
    lot_size: int = 100_000   # units per standard lot (fx); 1 for index CFDs

    def to_pips(self, price_distance: float) -> float:
        return price_distance / self.pip

    @property
    def unit(self) -> str:
        """Name of the price unit: pips for FX, pts for indices."""
        return "pips" if self.type == "fx" else "pts"

    def fmt(self, price: float) -> str:
        return f"{price:.{self.digits}f}"


@dataclass
class Session:
    name: str
    tz: str
    open: str   # "HH:MM" local
    close: str  # "HH:MM" local

    def _mins(self, hhmm: str) -> int:
        h, m = hhmm.split(":")
        return int(h) * 60 + int(m)

    @property
    def open_min(self) -> int:
        return self._mins(self.open)

    @property
    def close_min(self) -> int:
        return self._mins(self.close)


@dataclass
class Account:
    currency: str = "GBP"
    equity: float = 10_000.0
    risk_pct: float = 1.0
    compounding: bool = False


@dataclass
class Costs:
    slippage: float = 0.2        # per side, in pips / points
    commission: float = 0.0      # account currency per round trip
    same_bar_stop: str = "pessimistic"  # if SL and TP both hit in one bar, assume SL


@dataclass
class DataCfg:
    source: str = "yfinance"      # 'yfinance' | 'dukascopy'
    cache_dir: str = ".cache"
    default_tf: str = "1h"
    dk_start: str = "2018-01-01"  # earliest history to pull from Dukascopy


@dataclass
class BacktestCfg:
    start: Optional[str] = "2024-01-01"
    end: Optional[str] = None
    mc_runs: int = 1000
    oos_fraction: float = 0.3
    min_trades_for_stats: int = 30


@dataclass
class Config:
    account: Account
    costs: Costs
    data: DataCfg
    backtest: BacktestCfg
    sessions: Dict[str, Session]
    instruments: Dict[str, Instrument]
    universe: List[str]
    strategies: Dict[str, Dict[str, Any]]
    raw: Dict[str, Any] = field(default_factory=dict)

    def instrument(self, key: str) -> Instrument:
        k = key.upper()
        if k not in self.instruments:
            raise KeyError(f"Unknown instrument '{key}'. Known: {', '.join(sorted(self.instruments))}")
        return self.instruments[k]

    def session_for(self, inst: Instrument, override: Optional[str] = None) -> Session:
        name = (override or inst.session).upper()
        if name == "AUTO":
            name = inst.session.upper()
        return self.sessions[name]

    def strategy_params(self, name: str, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        p = dict(self.strategies.get(name, {}))
        p.pop("grid", None)
        if overrides:
            p.update({k: v for k, v in overrides.items() if v is not None})
        return p


def _find_config(path: Optional[str]) -> str:
    if path:
        return path
    for cand in ("config.yaml", os.path.join(os.path.dirname(__file__), "..", "config.yaml")):
        if os.path.exists(cand):
            return cand
    raise FileNotFoundError("config.yaml not found; pass --config")


def load_config(path: Optional[str] = None) -> Config:
    path = _find_config(path)
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    account = Account(**raw.get("account", {}))
    costs = Costs(**raw.get("costs", {}))
    data = DataCfg(**raw.get("data", {}))
    backtest = BacktestCfg(**raw.get("backtest", {}))
    sessions = {k.upper(): Session(name=k.upper(), **v) for k, v in raw["sessions"].items()}
    instruments: Dict[str, Instrument] = {}
    for k, v in raw["instruments"].items():
        v = dict(v)
        v.setdefault("digits", 5 if v.get("type") == "fx" else 2)
        v.setdefault("lot_size", 100_000 if v.get("type") == "fx" else 1)
        instruments[k.upper()] = Instrument(key=k.upper(), **v)
    universe = [u.upper() for u in raw.get("universe", list(instruments))]
    return Config(
        account=account,
        costs=costs,
        data=data,
        backtest=backtest,
        sessions=sessions,
        instruments=instruments,
        universe=universe,
        strategies=raw.get("strategies", {}),
        raw=raw,
    )
