"""
Pilot run (see ANALYSIS_PLAN.md). Usage:  python pilot.py [--users 300] [--reps 20] [--boot 2000]
Writes results/pilot_gaps.csv, results/pilot_groups.csv, results/pilot_summary.md
"""

from __future__ import annotations

import argparse
import csv
import os
import time
import zlib

import numpy as np

import detectors as dt
import sim

CAL_SEED = 101
EVAL_SEED = 202
TARGET_RATE = 3.33            # alarm episodes per 100 user-days, pooled
HORIZON = 14
SD_EFFECTS = (0.5, 1.0, 1.5, 2.0)
ABS_EFFECTS = (500.0, 1000.0, 1500.0, 2000.0)
BOOT_SEED = 7
MARGIN = {"alarm_rate": 1.0, "rmd": 1.5, "det14": 0.10}
GROUPS = ("low", "mid", "high")


def user_means(per_series: np.ndarray) -> np.ndarray:
    """(n, reps) -> (n,) average over a user's replicates."""
    return per_series.mean(-1)


def group_means(v: np.ndarray, g: np.ndarray) -> np.ndarray:
    return np.array([v[g == k].mean() for k in range(3)])


def boot_gaps(v: np.ndarray, g: np.ndarray, n_boot: int, rng: np.random.Generator):
    """Stratified (within tercile) bootstrap over users. Returns (point_gap, lo, hi, point_maxmin, lo, hi)."""
    idx = [np.where(g == k)[0] for k in range(3)]
    point = group_means(v, g)
    gap = point[2] - point[0]
    mm = point.max() - point.min()
    reps_gap, reps_mm = np.empty(n_boot), np.empty(n_boot)
    for b in range(n_boot):
        gm = np.array([v[rng.choice(ix, size=len(ix), replace=True)].mean() for ix in idx])
        reps_gap[b] = gm[2] - gm[0]
        reps_mm[b] = gm.max() - gm.min()
    return (gap, *np.percentile(reps_gap, [2.5, 97.5]), mm, *np.percentile(reps_mm, [2.5, 97.5]))


def run_scenario(scen: sim.Scenario, n_users: int, reps: int, n_boot: int):
    t0 = time.time()
    key = zlib.crc32((scen.seed_key or scen.name).encode()) % 1000      # same data for scenarios sharing a seed_key
    prep = (lambda a: np.log(np.maximum(a, 1.0))) if scen.log_detect else (lambda a: a)
    # 1. calibration set (different seed): one tuning constant per detector
    rng_c = np.random.default_rng([CAL_SEED, key])
    users_c = sim.make_users(n_users, rng_c)
    x_c = sim.simulate_series(users_c, max(reps // 2, 5), scen, rng_c)
    s_c = dt.Stats(prep(x_c))
    params = {name: dt.calibrate(name, s_c, TARGET_RATE) for name in dt.DETECTORS}

    # 2. evaluation set
    rng_e = np.random.default_rng([EVAL_SEED, key])
    users = sim.make_users(n_users, rng_e)
    x0 = sim.simulate_series(users, reps, scen, rng_e)
    onset = sim.draw_onsets(n_users, reps, rng_e)
    g = sim.variability_terciles(x0)
    sd0 = sim.baseline_sd(x0)
    s0 = dt.Stats(prep(x0))
    boot_rng = np.random.default_rng(BOOT_SEED)

    gap_rows, group_rows, diag = [], [], {}
    pooled_check = {}
    fires0 = {name: fn(s0, params[name]) for name, (fn, _) in dt.DETECTORS.items()}
    for name in dt.DETECTORS:
        ev = dt.merge_events(fires0[name])
        pooled_check[name] = ev.sum() / ev.size * 100.0
        ar_u = user_means(ev.sum(-1) / sim.EVAL_DAYS * 100.0)
        for k, gname in enumerate(GROUPS):
            group_rows.append(dict(scenario=scen.name, detector=name, convention="none", effect=0.0,
                                   group=gname, metric="alarm_rate", value=ar_u[g == k].mean()))
        gap_rows.append(_gap_row(scen, name, "none", 0.0, "alarm_rate", ar_u, g, n_boot, boot_rng))

    for conv, effects in (("standardised", SD_EFFECTS), ("absolute", ABS_EFFECTS)):
        for eff in effects:
            delta = eff * sd0 if conv == "standardised" else np.full(sd0.shape, eff)
            xi = sim.inject(x0, onset, delta)
            diag[(conv, eff)] = group_means(user_means(sim.floor_fraction(x0, onset, delta)), g)
            si = dt.Stats(prep(xi))
            for name, (fn, _) in dt.DETECTORS.items():
                d = dt.delays(fn(si, params[name]), onset, HORIZON)
                rmd_u = user_means(d.astype(float))
                d7_u = user_means((d < 7).astype(float))
                d14_u = user_means((d < HORIZON).astype(float))
                for metric, v in (("rmd", rmd_u), ("det7", d7_u), ("det14", d14_u)):
                    for k, gname in enumerate(GROUPS):
                        group_rows.append(dict(scenario=scen.name, detector=name, convention=conv, effect=eff,
                                               group=gname, metric=metric, value=v[g == k].mean()))
                    gap_rows.append(_gap_row(scen, name, conv, eff, metric, v, g, n_boot, boot_rng))
    info = dict(params=params, pooled=pooled_check, counts=[int((g == k).sum()) for k in range(3)],
                floor=diag, seconds=time.time() - t0)
    return gap_rows, group_rows, info


def _gap_row(scen, name, conv, eff, metric, v, g, n_boot, rng):
    gap, lo, hi, mm, mlo, mhi = boot_gaps(v, g, n_boot, rng)
    return dict(scenario=scen.name, detector=name, convention=conv, effect=eff, metric=metric,
                gap_high_minus_low=gap, gap_lo=lo, gap_hi=hi, maxmin=mm, maxmin_lo=mlo, maxmin_hi=mhi)


def verdict(row) -> str:
    """Real gap = interval excludes 0 and |gap| beyond margin; null = whole interval inside the margin."""
    m = MARGIN.get(row["metric"])
    if m is None:
        return ""
    lo, hi, gap = row["gap_lo"], row["gap_hi"], row["gap_high_minus_low"]
    if (lo > 0 or hi < 0) and abs(gap) > m:
        return "REAL"
    if lo > -m and hi < m:
        return "none"
    return "unclear"


def write_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def summary_md(all_gaps, all_groups, infos) -> str:
    out = ["# Pilot results (simulated users only)", "",
           f"Target pooled alarm rate {TARGET_RATE} episodes per 100 user-days. Gap = high minus low variability tercile.",
           f"Margins: alarm rate {MARGIN['alarm_rate']}, RMD {MARGIN['rmd']} days, detection within 14 days {MARGIN['det14']}.",
           "Verdict: REAL = interval excludes 0 and gap beyond margin; none = interval inside the margin; unclear otherwise.", ""]
    for scen, info in infos.items():
        out += [f"## Scenario: {scen}", "",
                f"Users per tercile (low, mid, high): {info['counts']}. Tuned constants: "
                + ", ".join(f"{k}={v:.3g}" for k, v in info["params"].items()) + ".",
                "Pooled alarm rate on the evaluation set (target 3.33): "
                + ", ".join(f"{k}={v:.2f}" for k, v in info["pooled"].items()) + ".",
                f"Share of post-onset days at the 0 floor, by tercile (low, mid, high), standardised 2 SD: "
                + ", ".join(f"{v:.3f}" for v in info["floor"][("standardised", 2.0)])
                + "; absolute 2000: " + ", ".join(f"{v:.3f}" for v in info["floor"][("absolute", 2000.0)]) + ".", ""]
        for metric, label in (("alarm_rate", "Alarm episodes per 100 user-days"),
                              ("rmd", "Restricted mean delay (days, censored at 14)"),
                              ("det14", "Detection within 14 days")):
            out += [f"### {label}", "",
                    "| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |",
                    "|---|---|---|---|---|---|---|---|---|"]
            gaps = [r for r in all_gaps if r["scenario"] == scen and r["metric"] == metric]
            for r in gaps:
                gv = {x["group"]: x["value"] for x in all_groups
                      if x["scenario"] == scen and x["detector"] == r["detector"] and x["convention"] == r["convention"]
                      and x["effect"] == r["effect"] and x["metric"] == metric}
                out.append(f"| {r['convention']} | {r['effect']:g} | {r['detector']} | {gv['low']:.2f} | {gv['mid']:.2f} | "
                           f"{gv['high']:.2f} | {r['gap_high_minus_low']:+.2f} | [{r['gap_lo']:+.2f}, {r['gap_hi']:+.2f}] | "
                           f"{verdict(r)} |")
            out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--users", type=int, default=300)
    ap.add_argument("--reps", type=int, default=20)
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--out", default="results")
    a = ap.parse_args()
    all_gaps, all_groups, infos = [], [], {}
    for name, scen in sim.SCENARIOS.items():
        gaps, groups, info = run_scenario(scen, a.users, a.reps, a.boot)
        all_gaps += gaps
        all_groups += groups
        infos[name] = info
        print(f"{name}: done in {info['seconds']:.0f}s; params {info['params']}")
    for r in all_gaps:
        r["verdict"] = verdict(r)
    write_csv(os.path.join(a.out, "pilot_gaps.csv"), all_gaps)
    write_csv(os.path.join(a.out, "pilot_groups.csv"), all_groups)
    with open(os.path.join(a.out, "pilot_summary.md"), "w") as f:
        f.write(summary_md(all_gaps, all_groups, infos))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
