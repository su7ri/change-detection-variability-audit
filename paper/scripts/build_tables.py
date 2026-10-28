"""Build LaTeX tables and the numbers.tex macro file from the CSVs in ../data.

Run:  python scripts/build_tables.py
Writes tables/*.tex and numbers.tex. Every figure in the text is a macro defined in numbers.tex.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from lib import *  # noqa: F401,F403

pilot = load("pilot_gaps")
groups = load("pilot_groups")
trade = load("tradeoff_gaps")
drift = load("drift_gaps")
sens_gaps = load("sensitivity_gaps")
sens_trade = load("sensitivity_tradeoff")
comb_gaps = load("sensitivity_combos_gaps")
comb_trade = load("sensitivity_combos_tradeoff")
ls_all = load("lifesnaps_gaps")
ls = ls_all[~ls_all.zeros_observed].reset_index(drop=True)          # primary run: 0-step days not observed
ls_zero = ls_all[ls_all.zeros_observed].reset_index(drop=True)   # sensitivity run: 0-step days kept
ls_log = load("lifesnaps_log_gaps")

macros: dict[str, str] = {}


def M(name: str, value) -> None:
    assert name.isalpha(), name
    macros[name] = str(value)


def write(path, text) -> None:
    (TABLES / path).write_text(text)


def bold_if(txt: str, flag: bool) -> str:
    return f"\\textbf{{{txt}}}" if flag else txt


# ------------------------------------------------------------------ macros: audit in the realistic scenario
CONV_KEYS = {  # key -> (convention, effect, metric)
    "Alarm": ("none", 0.0, "alarm_rate"),
    "RmdStd": ("standardised", 1.0, "rmd"),
    "DetStd": ("standardised", 1.0, "det14"),
    "RmdAbs": ("absolute", 1000.0, "rmd"),
    "DetAbs": ("absolute", 1000.0, "det14"),
}
DNAME = {"fixed": "Fixed", "zscore": "Zscore", "ewma": "Ewma", "cusum": "Cusum"}
for det in DETECTORS:
    for key, (conv, eff, met) in CONV_KEYS.items():
        r = cell(pilot, scenario="realistic", detector=det, convention=conv, effect=eff, metric=met)
        d = 2
        M(f"Real{DNAME[det]}{key}", tex(r.gap_high_minus_low, d))
        M(f"Real{DNAME[det]}{key}CI", ci_tex(r, d))

# lambda sweep (realistic)
for kind, kname in (("sd", "Sd"), ("mad", "Mad")):
    for lam in LAMBDAS:
        for key, (conv, eff, met) in CONV_KEYS.items():
            r = cell(trade, scenario="realistic", kind=kind, convention=conv, effect=eff, metric=met,
                     **{"lambda": lam})
            M(f"Lam{kname}{LAM_WORD[lam]}{key}", tex(r.gap_high_minus_low, 2))
            M(f"Lam{kname}{LAM_WORD[lam]}{key}CI", ci_tex(r, 2))

# ------------------------------------------------------------------ Table 1: audit in the realistic scenario
gv = groups[groups.scenario == "realistic"]


def gval(det, conv, eff, met, grp):
    return cell(gv, detector=det, convention=conv, effect=eff, metric=met, group=grp).value


panels = [
    ("A", "Alarm episodes per 100 user-days, series without a change", "none", 0.0, "alarm_rate", 2),
    ("B", "Restricted mean delay in days (censored at 14), change of 1 personal SD", "standardised", 1.0, "rmd", 2),
    ("C", "Proportion detected within 14 days, change of 1 personal SD", "standardised", 1.0, "det14", 2),
]
lines = [r"\begin{table}[t]", r"\centering", r"\small",
         r"\caption{Audit in the base simulation (``realistic'', 300 users $\times$ 20 replicates). Group means by "
         r"variability tercile, and the gap (high $-$ low) with its 95\% bootstrap interval. Verdicts follow the margins "
         r"fixed in advance: 1.0 alarm per 100 user-days, 1.5 days, 0.10 in proportion detected. ``Negligible'' means the "
         r"whole interval lies inside the margin; ``meaningful'' means the interval excludes zero and the gap exceeds the margin.}",
         r"\label{tab:audit}",
         r"\begin{tabular}{@{}lrrrlc@{}}", r"\toprule",
         r"Detector & Low & Mid & High & Gap [95\% CI] & Verdict \\"]
for tag, title, conv, eff, met, d in panels:
    lines += [r"\midrule", rf"\multicolumn{{6}}{{@{{}}l}}{{\emph{{{tag}. {title}}}}} \\"]
    for det in DETECTORS:
        r = cell(pilot, scenario="realistic", detector=det, convention=conv, effect=eff, metric=met)
        vals = [gval(det, conv, eff, met, g) for g in ("low", "mid", "high")]
        v = VERDICT_WORD[r.verdict]
        lines.append(f"{DET_LABEL[det]} & " + " & ".join(f"{x:.{d}f}" for x in vals) + f" & {ci_tex(r, d)} & {v} \\\\")
lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
write("audit.tex", "\n".join(lines) + "\n")

# ------------------------------------------------------------------ Table 2: all scenarios
lines = [r"\begin{table}[t]", r"\centering", r"\small",
         r"\caption{Alarm-rate gap (high $-$ low tercile, per 100 user-days) in eight simulated scenarios. Bold: the "
         r"interval excludes zero and the gap exceeds 1.0. Cells: for the three personal-baseline "
         r"detectors, the number of cells with a meaningful delay or detection gap among 24 (3 detectors $\times$ delay and "
         r"detection $\times$ four change sizes of 0.5 to 2 personal SD). Max delay gap: the largest delay gap (days) at 1 personal SD.}",
         r"\label{tab:scenarios}",
         r"\begin{tabular}{@{}p{5.2cm}rrrrrr@{}}", r"\toprule",
         r" & \multicolumn{4}{c}{Alarm-rate gap} & \multicolumn{2}{c}{Personal detectors} \\",
         r"\cmidrule(lr){2-5}\cmidrule(l){6-7}",
         r"Scenario & Fixed & z-score & EWMA & CUSUM & Cells & Max delay gap \\", r"\midrule"]
scen_stats = {}
for sc in SCEN_ORDER:
    cells = []
    for det in DETECTORS:
        r = cell(pilot, scenario=sc, detector=det, convention="none", metric="alarm_rate")
        cells.append(bold_if(tex(r.gap_high_minus_low), r.verdict == "REAL"))
    sub = pilot[(pilot.scenario == sc) & (pilot.detector.isin(PERSONAL)) & (pilot.convention == "standardised")
                & (pilot.metric.isin(["rmd", "det14"]))]
    assert len(sub) == 24, (sc, len(sub))
    n_real = int((sub.verdict == "REAL").sum())
    k1 = sub[(np.isclose(sub.effect, 1.0)) & (sub.metric == "rmd")]
    big = k1.loc[k1.gap_high_minus_low.abs().idxmax()]
    scen_stats[sc] = dict(n_real=n_real, big=float(big.gap_high_minus_low), big_det=big.detector)
    lines.append(f"{SCEN_LABEL[sc]} & " + " & ".join(cells) + f" & {n_real} & {tex(big.gap_high_minus_low)} \\\\")
lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
write("scenarios.tex", "\n".join(lines) + "\n")
M("ScenMaxPersonalRmd", tex(max(abs(v["big"]) for v in scen_stats.values()), 2, sign=False))
M("ScenMeaningfulTotal", sum(v["n_real"] for v in scen_stats.values()))

# ------------------------------------------------------------------ Table: lambda sweep (appendix), point estimates
lines = [r"\begin{table}[H]", r"\centering", r"\small",
         r"\caption{Mixing own and population scale (base simulation). Point estimates of the gap (high $-$ low tercile); "
         r"bold: meaningful by the pre-set rule. Intervals for every cell are in \texttt{tradeoff\_gaps.csv}. "
         r"$\lambda=0$ is a fixed threshold, $\lambda=1$ the personal z-score; each $\lambda$ is re-tuned to the same pooled alarm rate. "
         r"Delay in days; detection as a proportion.}",
         r"\label{tab:lambda}",
         r"\begin{tabular}{@{}lrrrrr@{}}", r"\toprule",
         r" & Alarm rate & \multicolumn{2}{c}{Delay} & \multicolumn{2}{c}{Detected in 14 days} \\",
         r"\cmidrule(lr){3-4}\cmidrule(l){5-6}",
         r"$\lambda$ & per 100 days & 1 SD & 1000 steps & 1 SD & 1000 steps \\"]
for kind, title in (("sd", "Scale: standard deviation"), ("mad", "Scale: robust (1.4826 $\\times$ MAD)")):
    lines += [r"\midrule", rf"\multicolumn{{6}}{{@{{}}l}}{{\emph{{{title}}}}} \\"]
    for lam in LAMBDAS:
        out = []
        for key in ("Alarm", "RmdStd", "RmdAbs", "DetStd", "DetAbs"):
            conv, eff, met = CONV_KEYS[key]
            r = cell(trade, scenario="realistic", kind=kind, convention=conv, effect=eff, metric=met, **{"lambda": lam})
            out.append(bold_if(tex(r.gap_high_minus_low, 2), r.verdict == "REAL"))
        lines.append(f"{lam:g} & " + " & ".join(out) + r" \\")
lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
write("lambda.tex", "\n".join(lines) + "\n")

# pre-set trade-off criterion (ANALYSIS_PLAN.md amendment 2026-10-25)
a0 = cell(trade, scenario="realistic", kind="sd", convention="absolute", metric="rmd", **{"lambda": 0.0}).gap_high_minus_low
a1 = cell(trade, scenario="realistic", kind="sd", convention="absolute", metric="rmd", **{"lambda": 1.0}).gap_high_minus_low
s0 = cell(trade, scenario="realistic", kind="sd", convention="standardised", metric="rmd", **{"lambda": 0.0}).gap_high_minus_low
s1 = cell(trade, scenario="realistic", kind="sd", convention="standardised", metric="rmd", **{"lambda": 1.0}).gap_high_minus_low
assert abs(a1) < abs(a0) and abs(s1) < abs(s0)   # both sizes shrink; the text below says so
M("CritAbsShrinks", tex(abs(a0) - abs(a1), 2, sign=False))
M("CritStdImproves", tex(abs(s0) - abs(s1), 2, sign=False))
assert not ((abs(a1) - abs(a0) > 1.5) and (abs(s0) - abs(s1) > 1.5))  # the pre-set criterion was not met

# ------------------------------------------------------------------ sensitivity + combinations
res = [criteria(sens_gaps, sens_trade, v) for v in sens_gaps.variant.unique()]
res_c = [criteria(comb_gaps, comb_trade, v) for v in comb_gaps.variant.unique() if v != "base"]
single = [r for r in res if r["variant"] != "base"]
n1 = len(single)
RNAME = {"r1": "Rone", "r2": "Rtwo", "r3": "Rthree"}
for key in ("r1", "r2", "r3"):
    n_ok = sum(r[key] for r in single)
    M(f"Sens{RNAME[key]}Ok", n_ok)
    M(f"Sens{RNAME[key]}Label", label(n_ok, n1))
M("SensN", n1)
M("SensRoneFails", ", ".join(r["variant"] for r in single if not r["r1"]) or "none")
M("SensMaxPersonal", tex(max(r["r1_max"] for r in res + res_c), 2, sign=False))
M("SensMostNegCusum", tex(min(r["cusum_alarm"] for r in res + res_c), 2))
for key, nm in (("r1", "Rone"), ("r2", "Rtwo"), ("r3", "Rthree")):
    M(f"Comb{nm}Ok", sum(r[key] for r in res_c))
M("CombN", len(res_c))
M("AllSettings", 1 + n1 + len(res_c))

allres = res + res_c
lines = [r"\begin{table}[H]", r"\centering", r"\scriptsize",
         r"\caption{Robustness of the simulation findings across 20 settings: the base case, 16 settings that change one "
         r"assumption, and 3 that change several together. R1: no meaningful delay or detection gap for the three "
         r"personal detectors at 1 personal SD. R2: the crossing (alarm gap above $+1.0$ at $\lambda=0$ and below $+1.0$ at "
         r"$\lambda=1$; absolute-change delay gap at most $-1.5$ days at $\lambda=0$ and at least $+1.5$ at $\lambda=1$). R3: some "
         r"$\lambda$ on the grid has the alarm gap within $\pm 1.0$ and both delay gaps within $\pm 1.5$ days "
         r"(the $\lambda$ values are listed). Gaps are high $-$ low tercile; alarm gaps per 100 user-days, "
         r"delay gaps in days for a 1000-step change. CUSUM: alarm-rate gap of the CUSUM detector.}",
         r"\label{tab:sens}",
         r"\begin{tabular}{@{}lcccrrrrr@{}}", r"\toprule",
         r" & & & & \multicolumn{2}{c}{Alarm gap} & \multicolumn{2}{c}{Delay gap, 1000 steps} & \\",
         r"\cmidrule(lr){5-6}\cmidrule(lr){7-8}",
         r"Setting & R1 & R2 & R3 ($\lambda$) & $\lambda=0$ & $\lambda=1$ & $\lambda=0$ & $\lambda=1$ & CUSUM \\", r"\midrule"]
for i, r in enumerate(allres):
    if r["variant"] == "combo_weak":
        lines.append(r"\midrule")
    yes = lambda b: "yes" if b else r"\textbf{no}"
    bal = ", ".join(f"{l:g}" for l in r["balanced"]) if r["balanced"] else r"\textbf{none}"
    lines.append(f"{VARIANT_LABEL[r['variant']]} & {yes(r['r1'])} & {yes(r['r2'])} & {bal} & {tex(r['a0'])} & {tex(r['a1'])} "
                 f"& {tex(r['d0'])} & {tex(r['d1'])} & {tex(r['cusum_alarm'])} \\\\")
lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
write("sensitivity.tex", "\n".join(lines) + "\n")
base = [r for r in res if r["variant"] == "base"][0]
M("BaseBalanced", ", ".join(f"{l:g}" for l in base["balanced"]))
for r in allres:
    nm = {"base": "Base", "combo_weak": "CombWeak", "combo_stress": "CombStress", "combo_reallike": "CombReal",
          "spread_wide": "SpreadWide", "spread_narrow": "SpreadNarrow", "corr_pos": "CorrPos", "ramp14": "Ramp",
          "target_6.0": "TargetSix", "evalseed_606": "EvalSeedB", "evalseed_505": "EvalSeedA"}.get(r["variant"])
    if nm:
        M(f"S{nm}AlarmZero", tex(r["a0"]))
        M(f"S{nm}AlarmOne", tex(r["a1"]))
        M(f"S{nm}DelayZero", tex(r["d0"]))
        M(f"S{nm}DelayOne", tex(r["d1"]))
        M(f"S{nm}Cusum", tex(r["cusum_alarm"]))

# C2 (stress) at lambda = 0.75: the closest the grid comes to balance
t2 = comb_trade[(comb_trade.variant == "combo_stress") & (comb_trade.kind == "sd")]
for key, (conv, eff, met) in (("Alarm", ("none", 0.0, "alarm_rate")), ("RmdStd", ("standardised", 1.0, "rmd")), ("RmdAbs", ("absolute", 1000.0, "rmd"))):
    r = cell(t2, convention=conv, effect=eff, metric=met, **{"lambda": 0.75})
    M(f"CombStressThreeQuarters{key}", tex(r.gap_high_minus_low, 2))
    M(f"CombStressThreeQuarters{key}Verdict", VERDICT_WORD[r.verdict])

# ------------------------------------------------------------------ LifeSnaps
fl = life_flags(ls, pilot, trade, "missing")
fl_log = life_flags(ls_log[ls_log.detector.isin(DETECTORS)], pilot, trade, "realistic_log")
M("LsConsistent", int(fl.consistent.sum()))
M("LsCells", len(fl))
M("LsInformative", int(fl.informative.sum()))
M("LsSameSign", int(fl.same_sign.sum()))
M("LsLogConsistent", int(fl_log.consistent.sum()))
M("LsLogCells", len(fl_log))
M("LsLogInformative", int(fl_log.informative.sum()))
fl_zero = life_flags(ls_zero, pilot, trade, "missing")
M("LsZeroConsistent", int(fl_zero.consistent.sum()))
M("LsZeroInformative", int(fl_zero.informative.sum()))
M("LsZeroCells", len(fl_zero))
M("LsZeroEligible", 53)   # typed from results/lifesnaps_summary.md (sensitivity run: 0-step days kept as observed)
rz = cell(fl_zero, detector="cusum", convention="none", metric="alarm_rate")
M("LsZeroCusumAlarmCI", ci_tex(rz))
M("LsEligible", LS_ELIGIBLE)
M("LsTotal", LS_TOTAL)
M("LsPopScale", f"{LS_POP_SCALE:,}".replace(",", r"\,"))
M("LsSpearman", tex(LS_SPEARMAN, 2))
for _, t in LS_TERCILES.iterrows():
    nm = t.tercile.capitalize()
    M(f"LsMedian{nm}", f"{int(t.median_steps):,}".replace(",", r"\,"))
    M(f"LsNoRow{nm}", f"{t.share_no_row:.3f}")
LSK = {"Alarm": ("none", 0.0, "alarm_rate"), "RmdStd": ("standardised", 1.0, "rmd"), "DetStd": ("standardised", 1.0, "det14"),
       "RmdAbs": ("absolute", 1000.0, "rmd"), "DetAbs": ("absolute", 1000.0, "det14")}
for det in DETECTORS:
    for key, (conv, eff, met) in LSK.items():
        r = cell(fl, detector=det, convention=conv, effect=eff, metric=met)
        M(f"Ls{DNAME[det]}{key}", tex(r.gap_high_minus_low))
        M(f"Ls{DNAME[det]}{key}CI", ci_tex(r))
        M(f"Ls{DNAME[det]}{key}Sim", tex(r.sim_gap))
        rl = cell(fl_log, detector=det, convention=conv, effect=eff, metric=met)
        M(f"LsLog{DNAME[det]}{key}", tex(rl.gap_high_minus_low))
        M(f"LsLog{DNAME[det]}{key}CI", ci_tex(rl))
        M(f"LsLog{DNAME[det]}{key}Sim", tex(rl.sim_gap))

lines = [r"\begin{table}[t]", r"\centering", r"\small",
         r"\caption{LifeSnaps consistency check, " + f"{LS_ELIGIBLE} eligible users" + r", 17 per variability tercile. "
         r"Real-data gap (high $-$ low) with 95\% interval, next to the gap found in the simulation with missing days. "
         r"Alarm rate in episodes per 100 user-days (these alarms may include real changes); delay in days for an injected change "
         r"of 1 personal SD or 1000 steps. Bold: meaningful by the pre-set rule. \emph{In}: the simulated gap lies inside the real-data interval.}",
         r"\label{tab:ls}",
         r"\begin{tabular}{@{}llrlrc@{}}", r"\toprule",
         r"Measure & Detector & Real gap [95\% CI] & & Simulated & In \\", r"\midrule"]
for title, conv, eff, met in (("Alarm rate", "none", 0.0, "alarm_rate"), ("Delay, 1 personal SD", "standardised", 1.0, "rmd"),
                              ("Delay, 1000 steps", "absolute", 1000.0, "rmd")):
    first = True
    for det in DETECTORS:
        r = cell(fl, detector=det, convention=conv, effect=eff, metric=met)
        lines.append(f"{title if first else ''} & {DET_LABEL[det]} & {bold_if(ci_tex(r), r.verdict == 'REAL')} & & "
                     f"{tex(r.sim_gap)} & {'yes' if r.consistent else 'no'} \\\\")
        first = False
    if met != "rmd" or conv != "absolute":
        lines.append(r"\addlinespace")
lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
write("lifesnaps.tex", "\n".join(lines) + "\n")

# full LifeSnaps table (appendix): 35 cells, primary run
lines = [r"{\footnotesize\setlength{\tabcolsep}{3.5pt}", r"\begin{longtable}{@{}lllrlrcc@{}}",
         r"\caption{All 35 cells of the LifeSnaps check (0-step days treated as not observed). Real-data gap (high $-$ low) with 95\% interval and pre-set verdict; "
         r"simulated gap in the matching ``missing'' scenario; \emph{In}: simulated gap inside the real interval; \emph{Inf}: interval does not contain both "
         r"the simulated gap and zero.}\label{tab:lsfull}\\",
         r"\toprule Detector & Change & Metric & Real gap [95\% CI] & Verdict & Simulated & In & Inf \\ \midrule \endfirsthead",
         r"\toprule Detector & Change & Metric & Real gap [95\% CI] & Verdict & Simulated & In & Inf \\ \midrule \endhead",
         r"\bottomrule \endlastfoot"]
MET = {"alarm_rate": "alarm rate", "rmd": "delay", "det14": "det. 14 d"}
CONVL = {"none": "none", "standardised": "1 SD", "absolute": "1000 steps"}
for _, r in fl.iterrows():
    dname = DET_LABEL.get(r.detector) or ("Shrunk $\\lambda=" + r.detector.replace("shrunk_lam", "") + "$")
    d = 2
    lines.append(f"{dname} & {CONVL[r.convention]} & {MET[r.metric]} & {ci_tex(r, d)} & {VERDICT_WORD[r.verdict]} & {tex(r.sim_gap, d)} & "
                 f"{'yes' if r.consistent else 'no'} & {'yes' if r.informative else 'no'} \\\\")
lines += [r"\end{longtable}", r"}"]
write("lifesnaps_full.tex", "\n".join(lines) + "\n")

# terciles table
lines = [r"\begin{table}[t]", r"\centering", r"\small",
         r"\caption{LifeSnaps users by variability tercile (log-scale SD of daily steps over the 28 baseline days).}",
         r"\label{tab:lsterc}",
         r"\begin{tabular}{@{}lrrrrr@{}}", r"\toprule",
         r"Tercile & Users & Median daily steps & Days without a record & Median log-SD & Mean evaluation days \\", r"\midrule"]
for _, t in LS_TERCILES.iterrows():
    lines.append(f"{t.tercile.capitalize()} & {int(t.users)} & {int(t.median_steps):,} & {t.share_no_row:.3f} & {t.median_log_sd:.2f} & {t.mean_eval_len:.1f} \\\\".replace(",", r"\,"))
lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
write("lifesnaps_terciles.tex", "\n".join(lines) + "\n")

# ------------------------------------------------------------------ drift (appendix)
lines = [r"\begin{table}[H]", r"\centering", r"\small",
         r"\caption{Slow drift away from the baseline (simulation; drift on the log scale reaching a normal draw with SD $d$ on day 83, independent of variability). "
         r"Alarm-rate gap (high $-$ low tercile, per 100 user-days). Bold: meaningful. The pre-set hypothesis (CUSUM and EWMA below $-1.0$ in both ``drift'' and ``drift\_log'' while the z-score stays inside the margin) was not supported.}",
         r"\label{tab:drift}",
         r"\begin{tabular}{@{}lcrrrr@{}}", r"\toprule",
         r"Scenario & $d$ & Fixed & z-score & EWMA & CUSUM \\", r"\midrule"]
for sc, dv, lab in (("drift_small", "0.15", "Small drift"), ("drift", "0.25", "Drift"), ("drift_large", "0.35", "Large drift"),
                    ("drift_log", "0.25", "Drift, detectors on log steps")):
    out = []
    for det in DETECTORS:
        r = cell(drift, scenario=sc, detector=det, convention="none", metric="alarm_rate")
        out.append(bold_if(tex(r.gap_high_minus_low), r.verdict == "REAL"))
    lines.append(f"{lab} & {dv} & " + " & ".join(out) + r" \\")
lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
write("drift.tex", "\n".join(lines) + "\n")
for sc, nm in (("drift", "Drift"), ("drift_large", "DriftLarge"), ("drift_log", "DriftLog")):
    for det in ("ewma", "cusum"):
        r = cell(drift, scenario=sc, detector=det, convention="none", metric="alarm_rate")
        M(f"{nm}{DNAME[det]}", tex(r.gap_high_minus_low))

# scenario macros used in the text
for sc, nm in (("ideal", "Ideal"), ("missing", "Missing"), ("symmetric", "Symmetric"), ("realistic_log", "RealLog")):
    for det in DETECTORS:
        r = cell(pilot, scenario=sc, detector=det, convention="none", metric="alarm_rate")
        M(f"Sc{nm}{DNAME[det]}Alarm", tex(r.gap_high_minus_low))
        M(f"Sc{nm}{DNAME[det]}AlarmCI", ci_tex(r))

# group means used in the text (realistic)
for det in DETECTORS:
    for grp in ("low", "high"):
        M(f"Grp{DNAME[det]}{grp.capitalize()}Alarm", f"{gval(det, 'none', 0.0, 'alarm_rate', grp):.2f}")

# ------------------------------------------------------------------ write numbers.tex
out = ["% Generated by scripts/build_tables.py from the CSV files in data/. Do not edit by hand."]
for k in sorted(macros):
    out.append(f"\\newcommand{{\\{k}}}{{{macros[k]}}}")
(ROOT / "numbers.tex").write_text("\n".join(out) + "\n")
print(f"{len(macros)} macros, tables written")
print("scenario stats:", {k: (v['n_real'], round(v['big'], 2)) for k, v in scen_stats.items()})
print("R1/R2/R3 single:", [sum(r[k] for r in single) for k in ('r1', 'r2', 'r3')], " combos:", [sum(r[k] for r in res_c) for k in ('r1', 'r2', 'r3')])
print("LifeSnaps:", int(fl.consistent.sum()), "/", len(fl), "informative", int(fl.informative.sum()), "same sign", int(fl.same_sign.sum()))
print("LifeSnaps log:", int(fl_log.consistent.sum()), "/", len(fl_log), "informative", int(fl_log.informative.sum()))
