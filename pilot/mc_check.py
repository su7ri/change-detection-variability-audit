"""
Monte Carlo check of the bootstrap intervals (disclosure of 2026-10-29 in ANALYSIS_PLAN.md).
The reported runs used 1000 bootstrap resamples; the frozen plan said 2000. Every simulated analysis, and the LifeSnaps runs,
were re-run with 10000 resamples (same data, same seeds; results_mc/). This script compares the two sets of files and writes
results_mc/mc_check_summary.csv (one row per file) and results_mc/mc_check_changes.csv (every cell whose verdict changed).
Usage:  python mc_check.py
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OLD, NEW = os.path.join(HERE, "results"), os.path.join(HERE, "results_mc")
FILES = ["pilot_gaps", "tradeoff_gaps", "drift_gaps", "sensitivity_gaps", "sensitivity_tradeoff",
         "sensitivity_combos_gaps", "sensitivity_combos_tradeoff", "lifesnaps_gaps", "lifesnaps_log_gaps"]
VALUES = ["gap_high_minus_low", "gap_lo", "gap_hi", "maxmin", "maxmin_lo", "maxmin_hi", "verdict"]


def main():
    rows, changes = [], []
    for f in FILES:
        a = pd.read_csv(os.path.join(OLD, f + ".csv"), float_precision="round_trip")
        b = pd.read_csv(os.path.join(NEW, f + ".csv"), float_precision="round_trip")
        keys = [c for c in a.columns if c not in VALUES]
        m = a.merge(b, on=keys, suffixes=("_1000", "_10000"), validate="one_to_one")
        assert len(m) == len(a) == len(b), (f, len(a), len(b), len(m))
        shift = np.maximum((m.gap_lo_10000 - m.gap_lo_1000).abs(), (m.gap_hi_10000 - m.gap_hi_1000).abs())
        has = m.verdict_1000.notna()
        chg = has & (m.verdict_1000 != m.verdict_10000)
        rows.append(dict(file=f, cells=len(m), cells_with_verdict=int(has.sum()), verdict_changes=int(chg.sum()),
                         max_shift=float(shift.max()), median_shift=float(shift.median()),
                         max_point_diff=float((m.gap_high_minus_low_10000 - m.gap_high_minus_low_1000).abs().max())))
        for _, r in m[chg].iterrows():
            changes.append({**{k: r[k] for k in keys}, "verdict_1000": r.verdict_1000, "verdict_10000": r.verdict_10000,
                            "lo_1000": r.gap_lo_1000, "hi_1000": r.gap_hi_1000, "lo_10000": r.gap_lo_10000, "hi_10000": r.gap_hi_10000,
                            "gap": r.gap_high_minus_low_1000, "file": f})
    pd.DataFrame(rows).to_csv(os.path.join(NEW, "mc_check_summary.csv"), index=False)
    pd.DataFrame(changes, columns=sorted({k for c in changes for k in c}) or ["file"]).to_csv(os.path.join(NEW, "mc_check_changes.csv"), index=False)
    t = pd.DataFrame(rows)
    print(t.to_string(index=False))
    print("TOTAL cells", int(t.cells.sum()), "with verdict", int(t.cells_with_verdict.sum()), "verdict changes", int(t.verdict_changes.sum()),
          "max shift", round(float(t.max_shift.max()), 3))


if __name__ == "__main__":
    main()
