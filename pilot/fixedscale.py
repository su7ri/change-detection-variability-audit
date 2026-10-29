"""
Fixed-scale z-score check (amendment of 2026-10-29 in ANALYSIS_PLAN.md).
Usage:  python fixedscale.py [--users 300] [--reps 20] [--boot 1000] [--out results] [--prefix fixedscale]
The window difference is divided by the baseline SD (days 0-27, in steps) instead of the moving 21-day SD.
Only this detector is run; scenarios `realistic` and `missing`; everything else as in pilot.py.
"""

from __future__ import annotations

import argparse
import os

import numpy as np

import detectors as dt
import pilot
import sim

dt.DETECTORS = {"zbase": (dt.fire_zbase, (0.0, 12.0))}
SCENARIOS = ("realistic", "missing")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--users", type=int, default=300)
    ap.add_argument("--reps", type=int, default=20)
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--out", default="results")
    ap.add_argument("--prefix", default="fixedscale")
    a = ap.parse_args()
    rows, infos = [], {}
    for name in SCENARIOS:
        gaps, _, info = pilot.run_scenario(sim.ALL_SCENARIOS[name], a.users, a.reps, a.boot)
        rows += gaps
        infos[name] = info
    for r in rows:
        r["verdict"] = pilot.verdict(r)
    pilot.write_csv(os.path.join(a.out, f"{a.prefix}_gaps.csv"), rows)
    ref = {}
    refpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "pilot_gaps.csv")
    if os.path.exists(refpath):
        import csv
        for r in csv.DictReader(open(refpath)):
            if r["detector"] == "zscore" and r["scenario"] in SCENARIOS:
                ref[(r["scenario"], r["convention"], float(r["effect"]), r["metric"])] = r
    cells = [("none", 0.0, "alarm_rate", "alarm rate"), ("standardised", 1.0, "rmd", "delay, 1 personal SD"),
             ("standardised", 1.0, "det14", "detected in 14 d, 1 personal SD"),
             ("absolute", 1000.0, "rmd", "delay, 1000 steps"), ("absolute", 1000.0, "det14", "detected in 14 d, 1000 steps")]
    out = ["# Fixed-scale z-score (z0) versus the moving-scale z-score",
           "", "Gap = high minus low variability tercile, 95% bootstrap interval, verdict by the pre-set rule "
           "(REAL / none / unclear). z0 divides the window difference by the baseline SD; z by the moving 21-day SD.", ""]
    for name in SCENARIOS:
        out += [f"## Scenario: {name}", "",
                f"Tuned constant z0: {infos[name]['params']['zbase']:.3f}; pooled alarm rate on the evaluation set "
                f"{infos[name]['pooled']['zbase']:.2f} (target {pilot.TARGET_RATE}).", "",
                "| Measure | z0 gap [95% CI] | z0 verdict | z gap [95% CI] (pilot_gaps.csv) | z verdict |", "|---|---|---|---|---|"]
        for conv, eff, met, lab in cells:
            r = next(x for x in rows if x["scenario"] == name and x["convention"] == conv and x["effect"] == eff and x["metric"] == met)
            z = ref.get((name, conv, eff, met))
            zt = (f"{float(z['gap_high_minus_low']):+.2f} [{float(z['gap_lo']):+.2f}, {float(z['gap_hi']):+.2f}]", z["verdict"]) if z else ("n/a", "")
            out.append(f"| {lab} | {r['gap_high_minus_low']:+.2f} [{r['gap_lo']:+.2f}, {r['gap_hi']:+.2f}] | {r['verdict']} | {zt[0]} | {zt[1]} |")
        out.append("")
    open(os.path.join(a.out, f"{a.prefix}_summary.md"), "w").write("\n".join(out))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
