"""
Real-data consistency check on LifeSnaps, exactly as frozen in LIFESNAPS_PLAN.md.
Usage:  python lifesnaps.py --counts            (eligibility counts only, no detector output)
        python lifesnaps.py [--boot 1000]       (full run; writes results/lifesnaps_*.csv/md)
Data: data/lifesnaps/daily_fitbit_sema_df_unprocessed.csv (not committed).
"""

from __future__ import annotations

import argparse
import csv
import os

import numpy as np
import pandas as pd

import detectors as dt
import pilot
import sim

DATA = os.environ.get("LIFESNAPS_DATA", os.path.join("..", "data", "lifesnaps", "daily_fitbit_sema_df_unprocessed.csv"))
N_ONSETS, ONSET_SEED = 20, 11
MIN_BASE_OBS, MIN_EVAL_LEN, MIN_EVAL_SHARE, MIN_USERS = 14, 35, 0.5, 45
LAMS = (0.0, 0.5, 1.0)
EFFECTS = (("standardised", 1.0), ("absolute", 1000.0))


def load_series(zeros_observed: bool):
    """Per user: array of length N_DAYS (NaN = not observed or beyond the end), plus bookkeeping."""
    df = pd.read_csv(DATA, usecols=["id", "date", "steps"])
    df["date"] = pd.to_datetime(df["date"])
    out = []
    for uid, d in df.groupby("id"):
        d = d.sort_values("date").drop_duplicates("date")
        s = d.set_index("date")["steps"].astype(float)
        pos = s[s > 0]
        if pos.empty:
            continue
        first, last = pos.index[0], s.index[-1]
        full = s.reindex(pd.date_range(first, last, freq="D"))
        span = len(full)
        zero_days = int((full == 0).sum())
        none_days = int(full.isna().sum())
        vals = full.to_numpy().copy()
        if not zeros_observed:
            vals[vals == 0] = np.nan
        x = np.full(sim.N_DAYS, np.nan)
        n = min(span, sim.N_DAYS)
        x[:n] = vals[:n]
        out.append(dict(id=uid, x=x, span=span, last=n - 1, zero_share=zero_days / span, none_share=none_days / span,
                        median_steps=float(np.nanmedian(vals[:n])) if np.isfinite(vals[:n]).any() else np.nan))
    return out


def eligible(users):
    keep = []
    for u in users:
        base_obs = int(np.isfinite(u["x"][: sim.BASE_DAYS]).sum())
        eval_len = u["last"] - sim.BASE_DAYS + 1
        if base_obs < MIN_BASE_OBS or eval_len < MIN_EVAL_LEN:
            continue
        if np.isfinite(u["x"][sim.BASE_DAYS: u["last"] + 1]).mean() < MIN_EVAL_SHARE:
            continue
        u["eval_len"] = eval_len
        keep.append(u)
    return keep


def rate_pooled(fires, eval_len):
    ev = dt.merge_events(fires)
    return ev.sum() / eval_len.sum() * 100.0


def bisect(fn, s, eval_len, lo, hi, iters=40):
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if rate_pooled(fn(s, mid), eval_len) > pilot.TARGET_RATE:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def run(zeros_observed: bool, n_boot: int, log: bool = False):
    users = eligible(load_series(zeros_observed))
    n = len(users)
    if n < MIN_USERS:
        return None, dict(n=n, inconclusive=True)
    X = np.stack([u["x"] for u in users])[:, None, :]                 # (n, 1, 84)
    eval_len = np.array([u["eval_len"] for u in users], dtype=float)
    lsd = np.array([np.nanstd(np.log(u["x"][: sim.BASE_DAYS][u["x"][: sim.BASE_DAYS] > 0]), ddof=1) for u in users])
    order = np.argsort(lsd, kind="stable")
    g = np.empty(n, dtype=int)
    for k, idx in enumerate(np.array_split(order, 3)):
        g[idx] = k
    sd0 = np.nanstd(X[..., : sim.BASE_DAYS], axis=-1, ddof=1)         # (n, 1)

    prep = (lambda a: np.log(np.maximum(a, 1.0))) if log else (lambda a: a)
    s0 = dt.StatsNaN(prep(X), with_mad=False)
    pop = float(np.nanmedian(s0.prior_sd[s0.can_decide]))
    detectors = {name: (fn, rng_) for name, (fn, rng_) in dt.DETECTORS.items()}
    for lam in LAMS:
        detectors[f"shrunk_lam{lam:g}"] = ((lambda s, c, lam=lam: dt.fire_shrunk(s, c, lam, pop, "sd")), (0.0, 40.0))
    params = {name: bisect(fn, s0, eval_len, *rng_) for name, (fn, rng_) in detectors.items()}

    rng_o = np.random.default_rng(ONSET_SEED)
    hi = np.array([u["last"] - 13 for u in users])
    onset = np.stack([rng_o.integers(35, h + 1, size=N_ONSETS) for h in hi])    # (n, 20)
    Xr = np.repeat(X, N_ONSETS, axis=1)
    inj = {}
    for conv, eff in EFFECTS:
        delta = np.repeat(eff * sd0, N_ONSETS, axis=1) if conv == "standardised" else np.full(onset.shape, eff)
        inj[conv] = dt.StatsNaN(prep(sim.inject(Xr, onset, delta)))
    boot_rng = np.random.default_rng(pilot.BOOT_SEED)

    rows, pooled = [], {}
    for name, (fn, _) in detectors.items():
        c = params[name]
        f0 = fn(s0, c)
        ev = dt.merge_events(f0)
        pooled[name] = ev.sum() / eval_len.sum() * 100.0
        ar_u = ev.sum(-1)[:, 0] / eval_len * 100.0
        rows.append(pilot._gap_row(type("S", (), {"name": "lifesnaps"}), name, "none", 0.0, "alarm_rate", ar_u, g, n_boot, boot_rng))
        for conv, eff in EFFECTS:
            d = dt.delays(fn(inj[conv], c), onset, pilot.HORIZON)
            for metric, v in (("rmd", d.astype(float).mean(-1)), ("det14", (d < pilot.HORIZON).astype(float).mean(-1))):
                rows.append(pilot._gap_row(type("S", (), {"name": "lifesnaps"}), name, conv, eff, metric, v, g, n_boot, boot_rng))
    for r in rows:
        r["verdict"] = pilot.verdict(r)

    med = np.array([u["median_steps"] for u in users])
    ranks = lambda a: np.argsort(np.argsort(a)).astype(float)
    spearman = float(np.corrcoef(ranks(lsd), ranks(med))[0, 1])
    conf = [dict(group=pilot.GROUPS[k], users=int((g == k).sum()),
                 median_steps=float(np.median(med[g == k])),
                 zero_share=float(np.mean([u["zero_share"] for u, gg in zip(users, g) if gg == k])),
                 missing_row_share=float(np.mean([u["none_share"] for u, gg in zip(users, g) if gg == k])),
                 eval_len=float(np.mean(eval_len[g == k])),
                 median_log_sd=float(np.median(lsd[g == k]))) for k in range(3)]
    info = dict(n=n, params=params, pooled=pooled, pop=pop, conf=conf, spearman=spearman, inconclusive=False,
                total_users=len(load_series(zeros_observed)))
    return rows, info


def consistency(rows, log: bool = False):
    """Compare each real-data gap with the simulator's gap (missing scenario). Returns list of dict."""
    sim_rows = [r for r in csv.DictReader(open("results/pilot_gaps.csv"))
                if r["scenario"] == ("realistic_log" if log else "missing")]
    tr_rows = [] if log else [r for r in csv.DictReader(open("results/tradeoff_gaps.csv"))
                              if r["scenario"] == "missing" and r["kind"] == "sd"]
    out = []
    for r in rows:
        det = r["detector"]
        if det.startswith("shrunk_lam"):
            lam = float(det.replace("shrunk_lam", ""))
            cand = [t for t in tr_rows if float(t["lambda"]) == lam]
        else:
            cand = [t for t in sim_rows if t["detector"] == det]
        cand = [t for t in cand if t["convention"] == r["convention"] and float(t["effect"]) == r["effect"]
                and t["metric"] == r["metric"]]
        if not cand:
            continue
        sg = float(cand[0]["gap_high_minus_low"])
        inside = r["gap_lo"] <= sg <= r["gap_hi"]
        zero_inside = r["gap_lo"] <= 0 <= r["gap_hi"]
        out.append(dict(detector=det, convention=r["convention"], effect=r["effect"], metric=r["metric"],
                        real_gap=r["gap_high_minus_low"], lo=r["gap_lo"], hi=r["gap_hi"], sim_gap=sg,
                        consistent=inside, informative=not (inside and zero_inside),
                        same_sign=(np.sign(r["gap_high_minus_low"]) == np.sign(sg))))
    return out


def summary_md(label, rows, info, log: bool = False) -> str:
    if info["inconclusive"]:
        return f"## {label}\n\nOnly {info['n']} eligible users (need {MIN_USERS}). Inconclusive; rules not loosened.\n"
    out = [f"## {label}", "",
           f"Eligible users {info['n']} of {info['total_users']} with any steps. Tuned constants: "
           + ", ".join(f"{k}={v:.3g}" for k, v in info["params"].items()) + ".",
           "Pooled alarm rate (target 3.33): " + ", ".join(f"{k}={v:.2f}" for k, v in info["pooled"].items()) + ".",
           f"Population scale for the shrunk detector: {info['pop']:.0f} steps. Spearman(log-SD, median steps) = {info['spearman']:+.2f}.", "",
           "| tercile | users | median steps | share 0-step days | share days without a row | mean eval length | median log-SD |",
           "|---|---|---|---|---|---|---|"]
    for c in info["conf"]:
        out.append(f"| {c['group']} | {c['users']} | {c['median_steps']:.0f} | {c['zero_share']:.3f} | "
                   f"{c['missing_row_share']:.3f} | {c['eval_len']:.1f} | {c['median_log_sd']:.2f} |")
    out += ["", "| detector | convention | metric | real gap [95%] | verdict | simulator gap (missing) | consistent | informative | same sign |",
            "|---|---|---|---|---|---|---|---|---|"]
    cons = {(c["detector"], c["convention"], c["metric"]): c for c in consistency(rows, log)}
    n_cons = n_inf = n_tot = 0
    for r in rows:
        c = cons.get((r["detector"], r["convention"], r["metric"]))
        if c is None:
            continue
        n_tot += 1
        n_cons += int(c["consistent"])
        n_inf += int(c["informative"])
        out.append(f"| {r['detector']} | {r['convention']} {r['effect']:g} | {r['metric']} | {r['gap_high_minus_low']:+.2f} "
                   f"[{r['gap_lo']:+.2f}, {r['gap_hi']:+.2f}] | {r['verdict']} | {c['sim_gap']:+.2f} | "
                   f"{'yes' if c['consistent'] else 'NO'} | {'yes' if c['informative'] else 'no'} | "
                   f"{'yes' if c['same_sign'] else 'NO'} |")
    out += ["", f"Consistent cells: {n_cons} of {n_tot}; informative cells (interval does not contain both the simulated gap "
            f"and zero): {n_inf} of {n_tot}.", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counts", action="store_true")
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--log", action="store_true", help="exploratory: detectors run on log(steps), primary run only")
    a = ap.parse_args()
    if a.log:
        rows, info = run(False, a.boot, log=True)
        md = ["# LifeSnaps, exploratory log-scale run (post hoc; see the 2026-10-26 amendment)", "",
              summary_md("Exploratory: detectors on log(steps), 0-step days not observed", rows, info, log=True)]
        pilot.write_csv("results/lifesnaps_log_gaps.csv", rows)
        open("results/lifesnaps_log_summary.md", "w").write("\n".join(md))
        print("log run -> eligible", info["n"])
        return
    if a.counts:
        for z in (False, True):
            us = load_series(z)
            el = eligible(us)
            print(f"zeros_observed={z}: users with any steps {len(us)}, eligible {len(el)}; "
                  f"evaluation length min/median/max {min([u['eval_len'] for u in el], default=0)}/"
                  f"{np.median([u['eval_len'] for u in el]) if el else 0}/{max([u['eval_len'] for u in el], default=0)}; "
                  f"span days median {np.median([u['span'] for u in us]):.0f}")
        return
    md = ["# LifeSnaps consistency check (real users; plan frozen in LIFESNAPS_PLAN.md)", "",
          "Alarm rate, not false-alarm rate: alarms may include real changes. About 20 users per tercile, so intervals are wide.", ""]
    allrows = []
    for z, label in ((False, "Primary: 0-step days treated as not observed"), (True, "Sensitivity: 0-step days kept as observed")):
        rows, info = run(z, a.boot)
        md.append(summary_md(label, rows, info))
        for r in rows or []:
            allrows.append(dict(r, zeros_observed=z))
        print(label, "-> eligible", info["n"])
    os.makedirs("results", exist_ok=True)
    if allrows:
        pilot.write_csv("results/lifesnaps_gaps.csv", allrows)
    with open("results/lifesnaps_summary.md", "w") as f:
        f.write("\n".join(md))


if __name__ == "__main__":
    main()
