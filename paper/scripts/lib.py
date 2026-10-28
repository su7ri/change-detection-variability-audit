"""Shared helpers: data loading, number formatting, verdict words, criteria R1-R3.

Everything that ends up in the paper is computed from the CSV files in ../data (copies of the files
in pilot/results of the repository). No number is typed by hand except where a comment says so.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
# Inside the repository the result files are read straight from pilot/results (paper/data is not used: the repository's
# .gitignore excludes folders called data/). A local paper/data folder, if present, takes precedence.
DATA = ROOT / "data" if (ROOT / "data").exists() else ROOT.parent / "pilot" / "results"
TABLES = ROOT / "tables"
FIGS = ROOT / "figures"

MARGIN = {"alarm_rate": 1.0, "rmd": 1.5, "det14": 0.10}
VERDICT_WORD = {"REAL": "meaningful", "none": "negligible", "unclear": "inconclusive"}
DETECTORS = ["fixed", "zscore", "ewma", "cusum"]
DET_LABEL = {"fixed": "Fixed threshold", "zscore": "Personal z-score", "ewma": "EWMA", "cusum": "CUSUM"}
PERSONAL = ["zscore", "ewma", "cusum"]
LAMBDAS = [0.0, 0.25, 0.5, 0.75, 1.0]
LAM_WORD = {0.0: "Zero", 0.25: "Quarter", 0.5: "Half", 0.75: "ThreeQuarters", 1.0: "One"}

SCEN_ORDER = ["ideal", "realistic", "realistic_log", "symmetric", "missing", "short14", "short7", "missing_short14"]
SCEN_LABEL = {
    "ideal": "Ideal (Gaussian, no autocorrelation, no weekly cycle)",
    "realistic": "Realistic (base case)",
    "realistic_log": "Realistic, detectors on log steps",
    "symmetric": "Symmetric noise on the raw scale",
    "missing": "Missing days (more for variable users)",
    "short14": "14-day windows",
    "short7": "7-day windows",
    "missing_short14": "Missing days and 14-day windows",
}

VARIANT_LABEL = {
    "base": "Base case",
    "target_1.5": "Alarm target 1.5 per 100",
    "target_6.0": "Alarm target 6.0 per 100",
    "calseed_303": "Calibration seed 303",
    "calseed_404": "Calibration seed 404",
    "evalseed_505": "Evaluation seed 505",
    "evalseed_606": "Evaluation seed 606",
    "users_600": "600 users",
    "phi_none": "No autocorrelation",
    "phi_strong": "Strong autocorrelation",
    "spread_narrow": "Narrow spread (log-SD 0.20)",
    "spread_wide": "Wide spread (log-SD 0.55)",
    "tails_gauss": "Gaussian noise",
    "tails_t3": "Student-t noise, 3 df",
    "corr_neg": "Level-variability corr. $-0.4$",
    "corr_pos": "Level-variability corr. $+0.4$",
    "ramp14": "14-day ramp change",
    "combo_weak": "C1 weak signal",
    "combo_stress": "C2 stress",
    "combo_reallike": "C3 real-data-like",
}
VARIANT_LABEL_PLAIN = {k: v.replace("$-$", "−").replace("$+$", "+") for k, v in VARIANT_LABEL.items()}
VARIANT_LABEL_PLAIN["corr_neg"] = "Level–variability corr. −0.4"
VARIANT_LABEL_PLAIN["corr_pos"] = "Level–variability corr. +0.4"


# LifeSnaps tercile descriptives. Typed from results/lifesnaps_summary.md (the file has no CSV twin);
# check_numbers.py compares them with the strings quoted there.
LS_TERCILES = pd.DataFrame(
    [("low", 17, 8726, 0.139, 0.40, 48.4), ("mid", 17, 6878, 0.144, 0.61, 49.9), ("high", 17, 6292, 0.175, 0.93, 52.2)],
    columns=["tercile", "users", "median_steps", "share_no_row", "median_log_sd", "mean_eval_len"],
)
LS_ELIGIBLE, LS_TOTAL = 51, 71
LS_POP_SCALE = 3638
LS_SPEARMAN = -0.33


def load(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA / f"{name}.csv", float_precision="round_trip")   # exact doubles, so that rounding ties match the repo summaries


def cell(df: pd.DataFrame, **kw) -> pd.Series:
    q = df
    for k, v in kw.items():
        q = q[np.isclose(q[k].astype(float), v)] if isinstance(v, float) else q[q[k] == v]
    assert len(q) == 1, (kw, len(q))
    return q.iloc[0]


def plain(x: float, d: int = 2) -> str:
    """Signed number as plain text; values that round to zero print as 0.00 (no sign)."""
    s = f"{x:+.{d}f}"
    if float(s) == 0.0:
        s = f"{0.0:.{d}f}"
    return s


def tex(x: float, d: int = 2, sign: bool = True) -> str:
    s = plain(x, d) if sign else f"{x:.{d}f}"
    return s.replace("-", "$-$")


def ci_plain(r, d: int = 2) -> str:
    return f"{plain(r.gap_high_minus_low, d)} [{plain(r.gap_lo, d)}, {plain(r.gap_hi, d)}]"


def ci_tex(r, d: int = 2) -> str:
    return f"{tex(r.gap_high_minus_low, d)} [{tex(r.gap_lo, d)}, {tex(r.gap_hi, d)}]"


def verdict_of(gap: float, lo: float, hi: float, metric: str) -> str:
    """Same rule as pilot.verdict (re-implemented so that the CSV verdicts can be cross-checked)."""
    m = MARGIN[metric]
    if (lo > 0 or hi < 0) and abs(gap) > m:
        return "REAL"
    if lo > -m and hi < m:
        return "none"
    return "unclear"


# ---------------------------------------------------------------- criteria R1-R3 (ANALYSIS_PLAN.md, 2026-10-26)
def criteria(gaps: pd.DataFrame, trade: pd.DataFrame, variant: str) -> dict:
    g = gaps[gaps.variant == variant]
    r1 = True
    r1_max = 0.0
    for det in PERSONAL:
        for m in ("rmd", "det14"):
            r = cell(g, detector=det, convention="standardised", effect=1.0, metric=m)
            if r.verdict == "REAL":
                r1 = False
            if m == "rmd":
                r1_max = max(r1_max, abs(r.gap_high_minus_low))
    t = trade[(trade.variant == variant) & (trade.kind == "sd")]

    def gap(lam, conv, metric):
        return cell(t, **{"lambda": float(lam), "convention": conv, "metric": metric}).gap_high_minus_low

    a0, a1 = gap(0.0, "none", "alarm_rate"), gap(1.0, "none", "alarm_rate")
    d0, d1 = gap(0.0, "absolute", "rmd"), gap(1.0, "absolute", "rmd")
    r2 = (a0 > 1.0) and (a1 < 1.0) and (d0 <= -1.5) and (d1 >= 1.5)
    balanced = [lam for lam in LAMBDAS
                if abs(gap(lam, "none", "alarm_rate")) <= 1.0
                and abs(gap(lam, "standardised", "rmd")) <= 1.5
                and abs(gap(lam, "absolute", "rmd")) <= 1.5]
    cus = cell(g, detector="cusum", convention="none", metric="alarm_rate").gap_high_minus_low
    return dict(variant=variant, r1=r1, r1_max=r1_max, r2=r2, r3=len(balanced) > 0, balanced=balanced,
                a0=a0, a1=a1, d0=d0, d1=d1, cusum_alarm=cus)


def label(n_ok: int, n: int) -> str:
    if n_ok == n:
        return "robust"
    if n_ok / n >= 0.8:
        return "mostly robust"
    return "sensitive"


# ---------------------------------------------------------------- LifeSnaps comparison flags
def life_flags(real: pd.DataFrame, pilot: pd.DataFrame, trade: pd.DataFrame, sim_scen: str = "missing") -> pd.DataFrame:
    """For each real-data cell: simulated gap (same scenario family), consistent / informative / same sign."""
    rows = []
    for _, r in real.iterrows():
        det = r.detector
        if det.startswith("shrunk_lam"):
            lam = float(det.replace("shrunk_lam", ""))
            src = trade[(trade.scenario == sim_scen) & (trade.kind == "sd")]
            s = cell(src, **{"lambda": lam, "convention": r.convention, "metric": r.metric,
                             "effect": float(r.effect)}) if r.convention != "none" else \
                cell(src, **{"lambda": lam, "convention": "none", "metric": r.metric})
        else:
            if r.convention == "none":
                s = cell(pilot[pilot.scenario == sim_scen], detector=det, convention="none", metric=r.metric)
            else:
                s = cell(pilot[pilot.scenario == sim_scen], detector=det, convention=r.convention,
                         effect=float(r.effect), metric=r.metric)
        sg = float(s.gap_high_minus_low)
        inside = r.gap_lo <= sg <= r.gap_hi
        zero_in = r.gap_lo <= 0 <= r.gap_hi
        rows.append(dict(r, sim_gap=sg, consistent=bool(inside), informative=not (inside and zero_in),
                         same_sign=bool(np.sign(r.gap_high_minus_low) == np.sign(sg))))
    return pd.DataFrame(rows)
