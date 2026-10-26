"""
Trade-off experiment (see the 2026-10-25 amendment in ANALYSIS_PLAN.md). Usage:  python tradeoff.py [--boot 1000]
Window detector with scale = lambda * own + (1 - lambda) * population, lambda in {0, .25, .5, .75, 1}.
Writes results/tradeoff_gaps.csv and results/tradeoff_summary.md
"""

from __future__ import annotations

import argparse
import os
import zlib

import numpy as np

import detectors as dt
import pilot
import sim

LAMBDAS = (0.0, 0.25, 0.5, 0.75, 1.0)
KINDS = ("sd", "mad")
SCENARIO_NAMES = ("realistic", "short7", "missing")
CONVENTIONS = (("standardised", 1.0), ("absolute", 1000.0))


def run(scen: sim.Scenario, n_users: int, reps: int, n_boot: int, target: float = pilot.TARGET_RATE,
        cal_seed: int = pilot.CAL_SEED, eval_seed: int = pilot.EVAL_SEED, kinds: tuple = KINDS):
    key = zlib.crc32((scen.seed_key or scen.name).encode()) % 1000
    rng_c = np.random.default_rng([cal_seed, key])
    users_c = sim.make_users(n_users, rng_c, **scen.user_kwargs())
    x_c = sim.simulate_series(users_c, max(reps // 2, 5), scen, rng_c)
    if scen.missing:
        x_c = sim.apply_missing(x_c, users_c, rng_c)
    s_c = dt.StatsNaN(x_c, scen.prior_len, scen.base_len, with_mad=True)
    pop = {"sd": float(np.nanmedian(s_c.prior_sd[s_c.can_decide])),
           "mad": float(np.nanmedian(s_c.prior_mad[s_c.can_decide]))}

    rng_e = np.random.default_rng([eval_seed, key])
    users = sim.make_users(n_users, rng_e, **scen.user_kwargs())
    x0 = sim.simulate_series(users, reps, scen, rng_e)
    onset = sim.draw_onsets(n_users, reps, rng_e)
    if scen.missing:
        x0 = sim.apply_missing(x0, users, rng_e)
    g = sim.variability_terciles(x0)
    sd0 = sim.baseline_sd(x0)
    boot_rng = np.random.default_rng(pilot.BOOT_SEED)
    s0 = dt.StatsNaN(x0, scen.prior_len, scen.base_len, with_mad=True)
    inj = {}
    for conv, eff in CONVENTIONS:
        delta = eff * sd0 if conv == "standardised" else np.full(sd0.shape, eff)
        inj[conv] = dt.StatsNaN(sim.inject(x0, onset, delta, scen.ramp_days), scen.prior_len, scen.base_len, with_mad=True)

    rows, info = [], {"pop": pop, "tuned": {}, "pooled": {}}
    for kind in kinds:
        for lam in LAMBDAS:
            fn = lambda s, c, lam=lam, kind=kind: dt.fire_shrunk(s, c, lam, pop[kind], kind)
            c = dt.calibrate_fn(fn, s_c, target)
            info["tuned"][(kind, lam)] = c
            ev = dt.merge_events(fn(s0, c))
            info["pooled"][(kind, lam)] = ev.sum() / ev.size * 100.0
            ar_u = pilot.user_means(ev.sum(-1) / sim.EVAL_DAYS * 100.0)
            rows.append(_row(scen, kind, lam, "none", 0.0, "alarm_rate", ar_u, g, n_boot, boot_rng))
            for conv, eff in CONVENTIONS:
                d = dt.delays(fn(inj[conv], c), onset, pilot.HORIZON)
                for metric, v in (("rmd", pilot.user_means(d.astype(float))),
                                  ("det14", pilot.user_means((d < pilot.HORIZON).astype(float)))):
                    rows.append(_row(scen, kind, lam, conv, eff, metric, v, g, n_boot, boot_rng))
    for r in rows:
        r["verdict"] = pilot.verdict(r)
    return rows, info


def _row(scen, kind, lam, conv, eff, metric, v, g, n_boot, rng):
    r = pilot._gap_row(scen, f"{kind}_lam{lam:g}", conv, eff, metric, v, g, n_boot, rng)
    r["kind"], r["lambda"] = kind, lam
    return r


def criterion(rows, scen_name: str = "realistic", kind: str = "sd") -> dict:
    """Pre-set 'trade-off confirmed' test on RMD (see the amendment)."""
    def gap(conv, lam):
        r = [r for r in rows if r["scenario"] == scen_name and r["kind"] == kind and r["lambda"] == lam
             and r["convention"] == conv and r["metric"] == "rmd"][0]
        return r["gap_high_minus_low"]
    a = abs(gap("absolute", 1.0)) - abs(gap("absolute", 0.0))
    s = abs(gap("standardised", 0.0)) - abs(gap("standardised", 1.0))
    m = pilot.MARGIN["rmd"]
    return dict(abs_worsens=a, std_improves=s, confirmed=bool(a > m and s > m))


def summary_md(rows, infos) -> str:
    out = ["# Trade-off experiment (simulated users only)", "",
           "Scale = lambda x own + (1 - lambda) x population; lambda 0 = fixed threshold in steps, lambda 1 = personal z-score.",
           "Every lambda is re-tuned to 3.33 alarm episodes per 100 user-days. Gap = high minus low variability tercile.",
           "Verdict as in the pilot: REAL / none / unclear (margins: alarm rate 1.0, RMD 1.5 days, detection 14 days 0.10).", ""]
    for scen, info in infos.items():
        out += [f"## Scenario: {scen}", "",
                "Population scale constants: " + ", ".join(f"{k}={v:.0f}" for k, v in info["pop"].items()) + ".", ""]
        for kind in KINDS:
            out += [f"### Scale type: {kind}", "",
                    "| lambda | alarm-rate gap | RMD gap, standardised k=1 | RMD gap, absolute 1000 | det14 gap, standardised | det14 gap, absolute |",
                    "|---|---|---|---|---|---|"]
            for lam in LAMBDAS:
                cells = []
                for conv, metric in (("none", "alarm_rate"), ("standardised", "rmd"), ("absolute", "rmd"),
                                     ("standardised", "det14"), ("absolute", "det14")):
                    r = [r for r in rows if r["scenario"] == scen and r["kind"] == kind and r["lambda"] == lam
                         and r["convention"] == conv and r["metric"] == metric][0]
                    cells.append(f"{r['gap_high_minus_low']:+.2f} [{r['gap_lo']:+.2f}, {r['gap_hi']:+.2f}] {r['verdict']}")
                out.append(f"| {lam:g} | " + " | ".join(cells) + " |")
            out.append("")
    c = criterion(rows)
    out += ["## Pre-set criterion (realistic, sd, RMD)", "",
            f"Absolute-convention gap grows from lambda 0 to 1 by {c['abs_worsens']:+.2f} days (needs > 1.5); "
            f"standardised-convention gap shrinks by {c['std_improves']:+.2f} days (needs > 1.5). "
            f"Trade-off confirmed: **{c['confirmed']}**.", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--users", type=int, default=300)
    ap.add_argument("--reps", type=int, default=20)
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--out", default="results")
    a = ap.parse_args()
    rows, infos = [], {}
    for name in SCENARIO_NAMES:
        r, info = run(sim.SCENARIOS[name], a.users, a.reps, a.boot)
        rows += r
        infos[name] = info
        print(name, "done; pooled alarm rates", {k: round(v, 2) for k, v in info["pooled"].items()})
    pilot.write_csv(os.path.join(a.out, "tradeoff_gaps.csv"), rows)
    with open(os.path.join(a.out, "tradeoff_summary.md"), "w") as f:
        f.write(summary_md(rows, infos))
    print("criterion:", criterion(rows))


if __name__ == "__main__":
    main()
