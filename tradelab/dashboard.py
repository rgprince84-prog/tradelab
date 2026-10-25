"""Dashboard export: publish the newest run of each kind under out/ as static data.

    python -m tradelab dashboard --dest site/data        # reads ./out (or --out DIR before the subcommand)

The page in site/index.html fetches <dest>/data.json and renders it in the browser, so
one export serves a local preview (``python -m http.server`` inside site/), a GitHub
Pages deploy of site/, or a data-only branch that a page hosted elsewhere reads.

What lands in dest/:
    data.json          tables, plans, metrics, Monte Carlo, report markdown, run log
    history.json       one line per run ever exported here (appended, capped)
    <kind>/...         the run's files: pipeline-1h/scan.csv, backtest-ema_pullback-1d/equity.png, ...
    <kind>/run.json    which out/ folder the copy came from

A *kind* is a run folder's name without its timestamp: ``pipeline-1h``,
``backtest-ema_pullback-1d``. Only the newest run of each kind is exported. Kinds with no
run in out/ keep their previous copy in dest, so hourly pipeline runs and weekly backtests
publish side by side. Nothing under out/ is modified or deleted (it is the audit trail).
"""
from __future__ import annotations

import json
import math
import os
import re
import shutil
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

import pandas as pd

from . import __version__
from .config import Config

RUN_RE = re.compile(r"^(\d{8})-(\d{6})-(pipeline-[0-9a-z]+|backtest-[a-z0-9_]+-[0-9a-z]+)$")
PIPELINE_SKIP_FILES = {"trades.csv"}   # 1-2 MB per strategy and churns hourly; the weekly backtest keeps its trades.csv
ASSET_FILES = ("equity.png", "r_distribution.png", "metrics.json", "report.md", "trades.csv")
HISTORY_CAP = 2000
HISTORY_IN_PAGE = 120


# ----------------------------------------------------------------------------- helpers
def _clean(obj: Any) -> Any:
    """JSON-safe copy: NaN/inf -> None, numpy scalars -> python, timestamps -> ISO strings."""
    if isinstance(obj, dict):
        return {str(k): _clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_clean(v) for v in obj]
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, float):
        return None if (math.isnan(obj) or math.isinf(obj)) else obj
    if isinstance(obj, (pd.Timestamp, datetime)):
        return obj.isoformat()
    if isinstance(obj, (str, int)) or obj is None:
        return obj
    if hasattr(obj, "item"):          # numpy scalar
        try:
            return _clean(obj.item())
        except Exception:
            return str(obj)
    return str(obj)


def _stamp_iso(day: str, hms: str) -> str:
    """Run folders are stamped in the machine's local time; publish them as UTC."""
    local = datetime.strptime(day + hms, "%Y%m%d%H%M%S").astimezone()   # naive -> local tz
    return local.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _complete(kind: str, path: str) -> bool:
    """A run folder counts only once its last file exists (summary.md / report.md); a run
    that crashed half-way must not replace a good earlier export."""
    marker = "summary.md" if kind.startswith("pipeline-") else "report.md"
    return os.path.isfile(os.path.join(path, marker))


def _read_json(path: str, default: Any) -> Any:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)          # Python accepts the NaN tokens json.dump writes
    except Exception:
        return default


def _read_text(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _read_records(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    try:
        df = pd.read_csv(path)
    except Exception:
        return []
    if df.empty:
        return []
    return json.loads(df.to_json(orient="records"))   # NaN -> null, numpy -> native


def latest_runs(out_dir: str) -> Dict[str, Dict[str, str]]:
    """kind -> {path, run_id, stamp} for the newest run folder of that kind."""
    runs: Dict[str, Dict[str, str]] = {}
    if not os.path.isdir(out_dir):
        return runs
    for name in sorted(os.listdir(out_dir)):           # ascending timestamp: the last one wins
        m = RUN_RE.match(name)
        path = os.path.join(out_dir, name)
        if m and os.path.isdir(path) and _complete(m.group(3), path):
            runs[m.group(3)] = {"path": path, "run_id": name, "stamp": _stamp_iso(m.group(1), m.group(2))}
    return runs


def _copy_run(src: str, dst: str, skip: Set[str]) -> List[str]:
    """Copy src into dst atomically: build next to it, then swap, so a failure half-way
    leaves the previous copy intact."""
    tmp = dst.rstrip("/\\") + ".tmp"
    if os.path.isdir(tmp):
        shutil.rmtree(tmp)
    copied: List[str] = []
    for root, _dirs, files in os.walk(src):
        for fn in sorted(files):
            if fn in skip:
                continue
            rel = os.path.relpath(os.path.join(root, fn), src).replace(os.sep, "/")
            target = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copy2(os.path.join(root, fn), target)
            copied.append(rel)
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    os.replace(tmp, dst)
    return copied


def _metrics_bundle(folder: str) -> Dict[str, Any]:
    mj = _read_json(os.path.join(folder, "metrics.json"), {}) or {}
    return {
        "metrics": mj.get("metrics", {}) or {},
        "monte_carlo": mj.get("monte_carlo", {}) or {},
        "params": mj.get("params", {}) or {},
    }


def _assets(kind: str, sub: Optional[str], copied: List[str]) -> Dict[str, str]:
    prefix = f"{sub}/" if sub else ""
    return {f: f"{kind}/{prefix}{f}" for f in ASSET_FILES if f"{prefix}{f}" in copied}


# ----------------------------------------------------------------------------- entries
def _pipeline_entry(kind: str, folder: str, run: Dict[str, Any], cfg: Config) -> Dict[str, Any]:
    copied = run.get("files", [])
    setups = _read_records(os.path.join(folder, "setups.csv"))
    entry: Dict[str, Any] = {
        "kind": kind,
        "tf": kind.split("-", 1)[1],
        "run_id": run["run_id"],
        "run_stamp": run.get("stamp"),
        "scan": _read_records(os.path.join(folder, "scan.csv")),
        "setups": setups,
        "plans": _read_json(os.path.join(folder, "plans.json"), []) or [],
        "summary_md": _read_text(os.path.join(folder, "summary.md")),
        "backtest_window": {"start": cfg.backtest.start, "end": cfg.backtest.end},
        "warnings": [str(w) for w in (_read_json(os.path.join(folder, "warnings.json"), []) or [])],
        "assets": {f: f"{kind}/{f}" for f in ("scan.csv", "setups.csv", "plans.json", "summary.md") if f in copied},
        "strategy_stats": {},
    }
    for d in sorted(os.listdir(folder)):
        sub = os.path.join(folder, d)
        if d.startswith("backtest-") and os.path.isdir(sub):
            bundle = _metrics_bundle(sub)
            bundle["report_md"] = _read_text(os.path.join(sub, "report.md"))
            bundle["assets"] = _assets(kind, d, copied)
            entry["strategy_stats"][d[len("backtest-"):]] = bundle
    return entry


def _backtest_entry(kind: str, folder: str, run: Dict[str, Any]) -> Dict[str, Any]:
    strategy, tf = kind[len("backtest-"):].rsplit("-", 1)
    bundle = _metrics_bundle(folder)
    return {
        "kind": kind,
        "strategy": strategy,
        "tf": tf,
        "run_id": run["run_id"],
        "run_stamp": run.get("stamp"),
        **bundle,
        "report_md": _read_text(os.path.join(folder, "report.md")),
        "assets": _assets(kind, None, run.get("files", [])),
    }


def _history_line(kind: str, entry: Dict[str, Any], exported_utc: str) -> Dict[str, Any]:
    line = {"run_id": entry["run_id"], "kind": kind, "run_stamp": entry.get("run_stamp"), "exported_utc": exported_utc}
    if kind.startswith("pipeline-"):
        setups = entry.get("setups", [])
        line.update(
            instruments=len(entry.get("scan", [])),
            setups=len(setups),
            fresh=sum(1 for s in setups if s.get("fresh") in (True, "True", 1)),
            strategies_fired=sorted({s.get("strategy") for s in setups if s.get("strategy")}),
        )
    else:
        m = entry.get("metrics", {})
        line.update(trades=m.get("trades"), expectancy_R=m.get("expectancy_R"), t_stat=m.get("t_stat"),
                    max_drawdown_R=m.get("max_drawdown_R"))
    return line


def _update_history(dest: str, lines: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    path = os.path.join(dest, "history.json")
    hist = _read_json(path, [])
    if not isinstance(hist, list):
        hist = []
    seen = {h.get("run_id") for h in hist if isinstance(h, dict)}
    for line in lines:
        if line["run_id"] not in seen:
            hist.append(line)
            seen.add(line["run_id"])
    hist.sort(key=lambda h: (str(h.get("run_stamp") or ""), str(h.get("run_id") or "")), reverse=True)
    hist = hist[:HISTORY_CAP]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(_clean(hist), f, indent=0, allow_nan=False)
    return hist


def _config_summary(cfg: Config) -> Dict[str, Any]:
    return {
        "account": asdict(cfg.account),
        "costs": asdict(cfg.costs),
        "data_source": cfg.data.source,
        "backtest": asdict(cfg.backtest),
        "universe": list(cfg.universe),
        "instruments": {
            k: {"type": v.type, "spread": v.spread, "pip": v.pip, "session": v.session, "digits": v.digits, "quote_ccy": v.quote_ccy}
            for k, v in cfg.instruments.items()
        },
        "strategies": {k: {kk: vv for kk, vv in (v or {}).items() if kk != "grid"} for k, v in cfg.strategies.items()},
    }


# ----------------------------------------------------------------------------- main
def export_dashboard(out_dir: str, dest: str, cfg: Config) -> Dict[str, Any]:
    """Copy the newest run of each kind from out_dir into dest and rebuild dest/data.json."""
    os.makedirs(dest, exist_ok=True)
    exported: List[str] = []
    for kind, run in sorted(latest_runs(out_dir).items()):
        skip = PIPELINE_SKIP_FILES if kind.startswith("pipeline-") else set()
        copied = _copy_run(run["path"], os.path.join(dest, kind), skip)
        with open(os.path.join(dest, kind, "run.json"), "w", encoding="utf-8") as f:
            json.dump({"run_id": run["run_id"], "kind": kind, "stamp": run["stamp"], "files": copied}, f, indent=1)
        exported.append(kind)

    exported_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    pipelines: Dict[str, Any] = {}
    backtests: Dict[str, Any] = {}
    lines: List[Dict[str, Any]] = []
    skipped: List[str] = []
    for kind in sorted(os.listdir(dest)):
        folder = os.path.join(dest, kind)
        run = _read_json(os.path.join(folder, "run.json"), None)
        if not os.path.isdir(folder) or not isinstance(run, dict) or not RUN_RE.match(str(run.get("run_id", ""))):
            continue
        try:
            if kind.startswith("pipeline-"):
                entry = _pipeline_entry(kind, folder, run, cfg)
                pipelines[entry["tf"]] = entry
            elif kind.startswith("backtest-"):
                entry = _backtest_entry(kind, folder, run)
                backtests[f"{entry['strategy']}-{entry['tf']}"] = entry
            else:
                continue
        except Exception as e:  # one damaged folder must not take the whole page down
            print(f"[dashboard] skipping {kind}: {type(e).__name__}: {e}")
            skipped.append(kind)
            continue
        lines.append(_history_line(kind, entry, exported_utc))

    history = _update_history(dest, lines)
    data = {
        "generated_utc": exported_utc,
        "tool": {"name": "tradelab", "version": __version__},
        "config": _config_summary(cfg),
        "pipelines": pipelines,
        "backtests": backtests,
        "history": history[:HISTORY_IN_PAGE],
        "history_total": len(history),
        "skipped": skipped,
    }
    path = os.path.join(dest, "data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(_clean(data), f, indent=1, allow_nan=False)
    return {"path": path, "exported": exported, "pipelines": sorted(pipelines), "backtests": sorted(backtests), "skipped": skipped}
