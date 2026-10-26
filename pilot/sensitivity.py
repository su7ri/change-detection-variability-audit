"""
Sensitivity analysis (see the dated amendment in ANALYSIS_PLAN.md, written before this was run).
One factor of the `realistic` simulator is changed at a time; the audit (four detectors) and the lambda sweep
(SD scale) are re-run for each variant. Usage:  python sensitivity.py [--users 300] [--reps 20] [--boot 1000]
Writes results/sensitivity_gaps.csv, results/sensitivity_tradeoff.csv, results/sensitivity_summary.md
"""

from __future__ import annotations

import argparse
import dataclasses
import os
import time

import pilot
import sim
import tradeoff

BASE = sim.REALISTIC
ZSC = ("zscore", "ewma", "cusum")


def _v(name, factor, level, scen_changes=None, **run_kw):
    scen = dataclasses.replace(BASE, name=name, seed_key="realistic", **(scen_changes or {}))
    return dict(name=name, factor=factor, level=level, scen=scen, run=run_kw)


VARIANTS = [
    _v("base", "base", "-"),
    _v("target_1.5", "alarm-rate target", "1.5 per 100", target=1.5),
    _v("target_6.0", "alarm-rate target", "6.0 per 100", target=6.0),
    _v("calseed_303", "calibration seed", "303", cal_seed=303),
    _v("calseed_404", "calibration seed", "404", cal_seed=404),
    _v("evalseed_505", "evaluation seed", "505", eval_seed=505),
    _v("evalseed_606", "evaluation seed", "606", eval_seed=606),
    _v("users_600", "number of users", "600", n_users=600),
    _v("phi_none", "autocorrelation", "none (phi = 0)", dict(phi_range=(0.0, 0.0))),
    _v("phi_strong", "autocorrelation", "strong (U(0.3, 0.8))", dict(phi_range=(0.3, 0.8))),
    _v("spread_narrow", "variability spread", "log-SD 0.20", dict(sigma_sd=0.20)),
    _v("spread_wide", "variability spread", "log-SD 0.55", dict(sigma_sd=0.55)),
    _v("tails_gauss", "noise tails", "Gaussian", dict(heavy_tails=False)),
    _v("tails_t3", "noise tails", "Student-t, 3 df", dict(t_df=3)),
    _v("corr_neg", "level-variability correlation", "-0.4", dict(level_corr=-0.4)),
    _v("corr_pos", "level-variability correlation", "+0.4", dict(level_corr=0.4)),
    _v("ramp14", "shape of the change", "14-day ramp", dict(ramp_days=14)),
]


def run_variant(v, n_users, reps, n_boot):
    kw = dict(v["run"])
    nu = kw.pop("n_users", n_users)
    t0 = time.time()
    gaps, _, info = pilot.run_scenario(v["scen"], nu, reps, n_boot, **kw)
    for r in gaps:
        r["verdict"] = pilot.verdict(r)
    trows, tinfo = tradeoff.run(v["scen"], nu, reps, n_boot, kinds=("sd",), **kw)
    for rows in (gaps, trows):
        for r in rows:
            r["variant"], r["factor"], r["level"] = v["name"], v["factor"], v["level"]
    return gaps, trows, dict(pooled=info["pooled"], tuned_tradeoff=tinfo["tuned"], seconds=time.time() - t0)


def _g(rows, **cond):
    r = [r for r in rows if all(r[k] == val for k, val in cond.items())]
    assert len(r) == 1, (cond, len(r))
    return r[0]


def criteria(gaps, trows) -> dict:
    """R1-R3 for one variant, as fixed in the plan."""
    m = pilot.MARGIN
    r1_cells = {}
    for det in ZSC:
        for metric in ("rmd", "det14"):
            r1_cells[(det, metric)] = _g(gaps, detector=det, convention="standardised", effect=1.0, metric=metric)
    r1 = all(c["verdict"] != "REAL" for c in r1_cells.values())

    def tg(lam, conv, metric):
        return _g(trows, **{"lambda": lam, "convention": conv, "metric": metric})["gap_high_minus_low"]

    a0, a1 = tg(0.0, "none", "alarm_rate"), tg(1.0, "none", "alarm_rate")
    d0, d1 = tg(0.0, "absolute", "rmd"), tg(1.0, "absolute", "rmd")
    r2 = (a0 > m["alarm_rate"]) and (a1 < m["alarm_rate"]) and (d0 <= -m["rmd"]) and (d1 >= m["rmd"])
    balanced = []
    for lam in tradeoff.LAMBDAS:
        ok = (abs(tg(lam, "none", "alarm_rate")) <= m["alarm_rate"]
              and abs(tg(lam, "standardised", "rmd")) <= m["rmd"]
              and abs(tg(lam, "absolute", "rmd")) <= m["rmd"])
        if ok:
            balanced.append(lam)
    cusum_ar = _g(gaps, detector="cusum", convention="none", metric="alarm_rate")["gap_high_minus_low"]
    return dict(R1=r1, R2=r2, R3=bool(balanced), balanced=balanced, a0=a0, a1=a1, d0=d0, d1=d1, cusum_alarm_gap=cusum_ar,
                r1_cells=r1_cells)


def label(n_ok: int, n: int) -> str:
    if n_ok == n:
        return "robust"
    if n_ok / n >= 0.8:
        return "mostly robust"
    return "sensitive"


def summary_md(results, infos) -> str:
    names = [v["name"] for v in VARIANTS]
    crit = {n: criteria(*results[n]) for n in names}
    out = ["# Sensitivity analysis (simulated users only)", "",
           "One factor of the `realistic` simulator is changed at a time; everything else is as in the base case.",
           "Detectors are re-tuned to the variant's alarm-rate target on a separate calibration set. Gap = high minus low variability tercile.",
           "Criteria were fixed before the run (ANALYSIS_PLAN.md, 2026-10-26): R1 no REAL delay or detection gap for the personal detectors "
           "(standardised, 1 SD); R2 the crossing (alarm gap at lambda 0 above +1.0 and at lambda 1 below +1.0; absolute-convention delay gap "
           "at most -1.5 days at lambda 0 and at least +1.5 days at lambda 1); R3 some lambda has all three gaps inside the margins "
           "(alarm +/-1.0, delay +/-1.5 days in both conventions).", "",
           "## Criteria by variant", "",
           "| variant | factor: level | R1 | R2 | R3 (balanced lambda) | alarm gap lambda 0 / 1 | abs. delay gap lambda 0 / 1 (days) | CUSUM alarm-rate gap |",
           "|---|---|---|---|---|---|---|---|"]
    for v in VARIANTS:
        c = crit[v["name"]]
        out.append(f"| {v['name']} | {v['factor']}: {v['level']} | {'yes' if c['R1'] else 'NO'} | {'yes' if c['R2'] else 'NO'} | "
                   f"{'yes (' + ', '.join(f'{b:g}' for b in c['balanced']) + ')' if c['R3'] else 'NO'} | "
                   f"{c['a0']:+.2f} / {c['a1']:+.2f} | {c['d0']:+.2f} / {c['d1']:+.2f} | {c['cusum_alarm_gap']:+.2f} |")
    var = [n for n in names if n != "base"]
    out += ["", "## Verdict per claim (16 changed variants; base case shown above for reference)", ""]
    for key, text in (("R1", "R1 personal detectors show no real delay or detection gap (1 SD)"),
                      ("R2", "R2 the crossing of the two equality conventions"),
                      ("R3", "R3 a balanced lambda exists")):
        ok = [n for n in var if crit[n][key]]
        bad = [n for n in var if not crit[n][key]]
        out.append(f"- **{text}**: holds in {len(ok)} of {len(var)} variants, **{label(len(ok), len(var))}**."
                   + (f" Fails in: {', '.join(bad)}." if bad else ""))
    q4 = [(n, crit[n]["cusum_alarm_gap"]) for n in names if crit[n]["cusum_alarm_gap"] <= -2.0]
    out += ["", "## Exploratory: can a variant reproduce the real-data CUSUM alarm-rate gap (about -3.3)?", "",
            ("Variants with CUSUM alarm-rate gap at or below -2.0: " + ", ".join(f"{n} ({g:+.2f})" for n, g in q4) + ".") if q4
            else "No variant reaches -2.0; the most negative is " +
                 min(((n, crit[n]['cusum_alarm_gap']) for n in names), key=lambda t: t[1])[0] + " (" +
                 f"{min(crit[n]['cusum_alarm_gap'] for n in names):+.2f}). The real-data gap stays unexplained.", "",
            "## Personal detectors, standardised 1 SD: gap [95% interval] and verdict", ""]
    out += ["| variant | " + " | ".join(f"{d} {m}" for d in ZSC for m in ("rmd", "det14")) + " |",
            "|---|" + "---|" * 6]
    for n in names:
        cells = []
        for det in ZSC:
            for metric in ("rmd", "det14"):
                r = crit[n]["r1_cells"][(det, metric)]
                cells.append(f"{r['gap_high_minus_low']:+.2f} [{r['gap_lo']:+.2f}, {r['gap_hi']:+.2f}] {r['verdict']}")
        out.append(f"| {n} | " + " | ".join(cells) + " |")
    out += ["", "## Alarm-rate gap by detector (per 100 user-days)", "",
            "| variant | fixed | zscore | ewma | cusum |", "|---|---|---|---|---|"]
    for n in names:
        cells = []
        for det in ("fixed", "zscore", "ewma", "cusum"):
            r = _g(results[n][0], detector=det, convention="none", metric="alarm_rate")
            cells.append(f"{r['gap_high_minus_low']:+.2f} [{r['gap_lo']:+.2f}, {r['gap_hi']:+.2f}]")
        out.append(f"| {n} | " + " | ".join(cells) + " |")
    out += ["", "## Time", "", ", ".join(f"{n}: {infos[n]['seconds']:.0f}s" for n in names), ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--users", type=int, default=300)
    ap.add_argument("--reps", type=int, default=20)
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--out", default="results")
    ap.add_argument("--only", default="", help="comma-separated variant names (default: all)")
    a = ap.parse_args()
    chosen = [v for v in VARIANTS if not a.only or v["name"] in a.only.split(",")]
    results, infos = {}, {}
    for v in chosen:
        gaps, trows, info = run_variant(v, a.users, a.reps, a.boot)
        results[v["name"]], infos[v["name"]] = (gaps, trows), info
        print(f"{v['name']}: {info['seconds']:.0f}s pooled {info['pooled']}", flush=True)
    if a.only:
        return
    pilot.write_csv(os.path.join(a.out, "sensitivity_gaps.csv"), [r for n in results for r in results[n][0]])
    pilot.write_csv(os.path.join(a.out, "sensitivity_tradeoff.csv"), [r for n in results for r in results[n][1]])
    with open(os.path.join(a.out, "sensitivity_summary.md"), "w") as f:
        f.write(summary_md(results, infos))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
