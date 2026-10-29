"""
Cross-fitted tuning on LifeSnaps (amendment of 2026-10-29 in LIFESNAPS_PLAN.md).
Usage:  python crossfit.py [--boot 1000] [--out results] [--prefix lifesnaps_crossfit]
Users are split into two folds (seed 13, stratified by variability tercile). Each detector's constant is tuned to the
pooled alarm rate 3.33 on the series of the users in the OTHER fold and applied to the users of this fold; gaps are then
computed over all users exactly as in lifesnaps.py (same groups, onsets, injections, metrics, bootstrap).
Only the four detectors of the primary analysis are run. Data: see lifesnaps.py (LIFESNAPS_DATA).
"""

from __future__ import annotations

import argparse
import csv
import os

import numpy as np

import detectors as dt
import lifesnaps as ls
import pilot
import sim

FOLD_SEED = 13
CELLS = [("none", 0.0, "alarm_rate", "alarm rate"), ("standardised", 1.0, "rmd", "delay, 1 personal SD"),
         ("standardised", 1.0, "det14", "detected in 14 d, 1 personal SD"), ("absolute", 1000.0, "rmd", "delay, 1000 steps"),
         ("absolute", 1000.0, "det14", "detected in 14 d, 1000 steps")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--out", default="results")
    ap.add_argument("--prefix", default="lifesnaps_crossfit")
    a = ap.parse_args()

    users = ls.eligible(ls.load_series(False))
    n = len(users)
    X = np.stack([u["x"] for u in users])[:, None, :]
    eval_len = np.array([u["eval_len"] for u in users], dtype=float)
    lsd = np.array([np.nanstd(np.log(u["x"][: sim.BASE_DAYS][u["x"][: sim.BASE_DAYS] > 0]), ddof=1) for u in users])
    order = np.argsort(lsd, kind="stable")
    g = np.empty(n, dtype=int)
    for k, idx in enumerate(np.array_split(order, 3)):
        g[idx] = k
    sd0 = np.nanstd(X[..., : sim.BASE_DAYS], axis=-1, ddof=1)

    rng_f = np.random.default_rng(FOLD_SEED)
    fold = np.empty(n, dtype=int)
    for k in range(3):
        idx = rng_f.permutation(np.where(g == k)[0])
        fold[idx] = np.arange(len(idx)) % 2

    rng_o = np.random.default_rng(ls.ONSET_SEED)
    hi = np.array([u["last"] - 13 for u in users])
    onset = np.stack([rng_o.integers(35, h + 1, size=ls.N_ONSETS) for h in hi])
    Xr = np.repeat(X, ls.N_ONSETS, axis=1)
    delta = {conv: (np.repeat(eff * sd0, ls.N_ONSETS, axis=1) if conv == "standardised" else np.full(onset.shape, eff))
             for conv, eff in ls.EFFECTS}

    s_all = dt.StatsNaN(X, with_mad=False)
    params_all = {name: ls.bisect(fn, s_all, eval_len, *rng_) for name, (fn, rng_) in dt.DETECTORS.items()}
    params, vals = {}, {}
    for name in dt.DETECTORS:
        vals[(name, "alarm")] = np.zeros(n)
        for conv, _ in ls.EFFECTS:
            vals[(name, conv, "rmd")] = np.zeros(n)
            vals[(name, conv, "det14")] = np.zeros(n)
    pooled_fold = {}
    for f in (0, 1):
        tune, test = np.where(fold != f)[0], np.where(fold == f)[0]
        s_tune = dt.StatsNaN(X[tune], with_mad=False)
        s_test = dt.StatsNaN(X[test], with_mad=False)
        inj = {conv: dt.StatsNaN(sim.inject(Xr[test], onset[test], delta[conv][test])) for conv, _ in ls.EFFECTS}
        for name, (fn, rng_) in dt.DETECTORS.items():
            c = ls.bisect(fn, s_tune, eval_len[tune], *rng_)
            params[(f, name)] = c
            ev = dt.merge_events(fn(s_test, c))
            pooled_fold[(f, name)] = ev.sum() / eval_len[test].sum() * 100.0
            vals[(name, "alarm")][test] = ev.sum(-1)[:, 0] / eval_len[test] * 100.0
            for conv, _ in ls.EFFECTS:
                d = dt.delays(fn(inj[conv], c), onset[test], pilot.HORIZON)
                vals[(name, conv, "rmd")][test] = d.astype(float).mean(-1)
                vals[(name, conv, "det14")][test] = (d < pilot.HORIZON).astype(float).mean(-1)

    boot_rng = np.random.default_rng(pilot.BOOT_SEED)
    S = type("S", (), {"name": "lifesnaps_crossfit"})
    rows = []
    for name in dt.DETECTORS:
        rows.append(pilot._gap_row(S, name, "none", 0.0, "alarm_rate", vals[(name, "alarm")], g, a.boot, boot_rng))
        for conv, eff in ls.EFFECTS:
            for metric in ("rmd", "det14"):
                rows.append(pilot._gap_row(S, name, conv, eff, metric, vals[(name, conv, metric)], g, a.boot, boot_rng))
    for r in rows:
        r["verdict"] = pilot.verdict(r)
    pilot.write_csv(os.path.join(a.out, f"{a.prefix}_gaps.csv"), rows)

    ref = {}
    refpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "lifesnaps_gaps.csv")
    if os.path.exists(refpath):
        for r in csv.DictReader(open(refpath)):
            if r["zeros_observed"] in ("False", "false", "0") and r["detector"] in dt.DETECTORS:
                ref[(r["detector"], r["convention"], float(r["effect"]), r["metric"])] = r
    out = ["# LifeSnaps: cross-fitted tuning versus in-sample tuning", "",
           f"{n} eligible users, folds of {int((fold == 0).sum())} and {int((fold == 1).sum())} users (seed {FOLD_SEED}, stratified by tercile). "
           "Gap = high minus low tercile, 95% bootstrap interval (same seed and resamples as lifesnaps.py); verdict by the pre-set rule.", "",
           "| Detector | constant in-sample | constant fold 0 / fold 1 (tuned on the other fold) | pooled rate fold 0 / fold 1 |", "|---|---|---|---|"]
    for name in dt.DETECTORS:
        out.append(f"| {name} | {params_all[name]:.3f} | {params[(0, name)]:.3f} / {params[(1, name)]:.3f} | "
                   f"{pooled_fold[(0, name)]:.2f} / {pooled_fold[(1, name)]:.2f} |")
    out += ["", "| Detector | Measure | In-sample gap [95% CI] | verdict | Cross-fitted gap [95% CI] | verdict | same sign |", "|---|---|---|---|---|---|---|"]
    same_real, flips_other, n_real, n_other = True, 0, 0, 0
    for name in dt.DETECTORS:
        for conv, eff, met, lab in CELLS:
            r = next(x for x in rows if x["detector"] == name and x["convention"] == conv and x["effect"] == eff and x["metric"] == met)
            z = ref.get((name, conv, eff, met))
            if z is None:
                continue
            zg = float(z["gap_high_minus_low"])
            same = (zg > 0) == (r["gap_high_minus_low"] > 0)
            if z["verdict"] == "REAL":
                same_real &= same
                n_real += 1
            else:
                flips_other += int(not same)
                n_other += 1
            out.append(f"| {name} | {lab} | {zg:+.2f} [{float(z['gap_lo']):+.2f}, {float(z['gap_hi']):+.2f}] | {z['verdict']} | "
                       f"{r['gap_high_minus_low']:+.2f} [{r['gap_lo']:+.2f}, {r['gap_hi']:+.2f}] | {r['verdict']} | {'yes' if same else 'NO'} |")
    cu = next(x for x in rows if x["detector"] == "cusum" and x["metric"] == "alarm_rate")
    out += ["", f"Rule (a): every cell that was REAL in the primary run keeps its sign when cross-fitted: {'holds' if same_real else 'FAILS'} "
            f"({n_real} cells). Among the other {n_other} cells, {flips_other} change sign.",
            f"Rule (b): CUSUM alarm-rate gap cross-fitted below -1.0 with the interval excluding 0: "
            f"{'holds' if (cu['gap_high_minus_low'] < -1.0 and cu['gap_hi'] < 0) else 'FAILS'} "
            f"({cu['gap_high_minus_low']:+.2f} [{cu['gap_lo']:+.2f}, {cu['gap_hi']:+.2f}])."]
    open(os.path.join(a.out, f"{a.prefix}_summary.md"), "w").write("\n".join(out))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
