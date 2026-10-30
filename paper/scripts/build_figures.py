"""Build the figures (vector PDF) from the CSV files in ../data.

Run:  python scripts/build_figures.py
Colours: validated categorical pair (blue, orange); marker shape and fill carry the same information,
so the figures stay readable in greyscale. Margin bands are the margins of the analysis plan.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from lib import *  # noqa: F401,F403

BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#6b6a66"
INK, INK2, BAND, GRID = "#0b0b0b", "#52514e", "#ecebe8", "#d9d8d3"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 7.5, "axes.titlesize": 8, "axes.labelsize": 7.5,
    "xtick.labelsize": 7, "ytick.labelsize": 7.5, "legend.fontsize": 7,
    "axes.edgecolor": INK2, "axes.linewidth": 0.6, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK2, "ytick.color": INK2, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 2.5, "ytick.major.size": 2.5,
    "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42, "ps.fonttype": 42,
    "figure.dpi": 150, "savefig.dpi": 300, "axes.unicode_minus": True,
})

pilot = load("pilot_gaps")
trade = load("tradeoff_gaps")
sens_gaps = load("sensitivity_gaps")
sens_trade = load("sensitivity_tradeoff")
comb_gaps = load("sensitivity_combos_gaps")
comb_trade = load("sensitivity_combos_tradeoff")
ls_all = load("lifesnaps_gaps")
ls = ls_all[~ls_all.zeros_observed].reset_index(drop=True)
ls_log = load("lifesnaps_log_gaps")

VERDICT_STYLE = {  # verdict -> (colour, marker, filled)
    "REAL": (ORANGE, "s", True),
    "none": (BLUE, "o", True),
    "unclear": (GREY, "D", False),
}


def band(ax, m, orient="v"):
    if orient == "v":
        ax.axvspan(-m, m, color=BAND, zorder=0, lw=0)
        ax.axvline(0, color=INK2, lw=0.5, zorder=1)
    else:
        ax.axhspan(-m, m, color=BAND, zorder=0, lw=0)
        ax.axhline(0, color=INK2, lw=0.5, zorder=1)


def clean_x(ax):
    ax.grid(axis="x", color=GRID, lw=0.4, zorder=0)
    ax.set_axisbelow(True)


def save(fig, name):
    fig.savefig(FIGS / f"{name}.pdf", bbox_inches="tight", pad_inches=0.03)
    fig.savefig(FIGS / f"{name}.png", bbox_inches="tight", pad_inches=0.03, dpi=200)
    plt.close(fig)


# ============================================================ Figure 1: schematic with two simulated users
def fig_example():
    pilot_dir = ROOT.parent / "pilot"
    if not pilot_dir.exists():
        pilot_dir = Path("/home/claude/pilot")
    sys.path.insert(0, str(pilot_dir))
    import sim  # noqa: E402

    rng = np.random.default_rng(7)
    users = dict(mu=np.array([7000.0, 7000.0]), sigma=np.array([0.12, 0.45]), phi=np.array([0.25, 0.25]),
                 amp=np.array([0.08, 0.08]), phase=np.array([2.0, 2.0]))
    x = sim.simulate_series(users, 1, sim.REALISTIC, rng)
    onset, delta = np.array([[42], [42]]), np.array([[1000.0], [1000.0]])
    xi = sim.inject(x, onset, delta)
    sd0 = sim.baseline_sd(x)[:, 0]
    mean0 = x[:, 0, :28].mean(-1)
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.0), sharey=True)
    titles = ["Steady user", "Variable user"]
    info = []
    for i, ax in enumerate(axes):
        t = np.arange(84)
        ax.axvspan(0, 27.5, color=BAND, lw=0, zorder=0)
        ax.fill_between(t, mean0[i] - sd0[i], mean0[i] + sd0[i], where=t <= 27, color=BLUE, alpha=0.18, lw=0, zorder=1)
        ax.axhline(mean0[i], xmax=28 / 84, color=BLUE, lw=0.8, zorder=2)
        ax.plot(t, xi[i, 0] / 1000, lw=0)  # keep autoscale simple
        ax.plot(t, xi[i, 0], color=INK, lw=0.7, zorder=3)
        ax.axvline(42, color=ORANGE, lw=1.0, ls=(0, (4, 2)), zorder=2)
        ax.set_xlim(0, 83)
        ax.set_title(f"{titles[i]}: baseline SD {sd0[i]:,.0f} steps\na drop of 1000 steps is {1000 / sd0[i]:.1f} personal SD", loc="left")
        ax.set_xlabel("Day")
        ax.text(14, 0.97, "baseline", transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=6.5, color=INK2)
        ax.text(42.8, 0.97, "change", transform=ax.get_xaxis_transform(), ha="left", va="top", fontsize=6.5, color=ORANGE)
        info.append((float(sd0[i]), float(1000 / sd0[i])))
    axes[0].set_ylabel("Daily steps")
    axes[0].set_ylim(0, None)
    fig.tight_layout(w_pad=1.0)
    save(fig, "fig_example")
    return info


# ============================================================ Figure 2: audit forest plot (realistic scenario)
def fig_audit():
    panels = [("(a) Alarm rate, per 100 days", "none", 0.0, "alarm_rate", "episodes"),
              ("(b) Delay in days, 1 SD change", "standardised", 1.0, "rmd", "days"),
              ("(c) Detected in 14 days, 1 SD", "standardised", 1.0, "det14", "proportion")]
    fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.0), sharey=True)
    ypos = {d: i for i, d in enumerate(reversed(DETECTORS))}
    for ax, (title, conv, eff, met, unit) in zip(axes, panels):
        band(ax, MARGIN[met])
        for det in DETECTORS:
            r = cell(pilot, scenario="realistic", detector=det, convention=conv, effect=eff, metric=met)
            col, mk, filled = VERDICT_STYLE[r.verdict]
            y = ypos[det]
            ax.plot([r.gap_lo, r.gap_hi], [y, y], color=col, lw=1.2, solid_capstyle="butt", zorder=3)
            ax.plot(r.gap_high_minus_low, y, marker=mk, ms=5, mfc=col if filled else "white", mec=col, mew=1.1, zorder=4, ls="")
        ax.set_title(title, loc="left")
        ax.set_xlabel("gap, high minus low")
        clean_x(ax)
        ax.set_ylim(-0.6, len(DETECTORS) - 0.4)
    axes[0].set_yticks([ypos[d] for d in DETECTORS])
    axes[0].set_yticklabels([DET_LABEL[d] for d in DETECTORS])
    for ax in axes[1:]:
        ax.tick_params(axis="y", length=0)
    handles = [Line2D([], [], marker="s", color=ORANGE, mfc=ORANGE, ls="", ms=5, label="meaningful"),
               Line2D([], [], marker="o", color=BLUE, mfc=BLUE, ls="", ms=5, label="negligible (interval inside margin)"),
               Line2D([], [], marker="D", color=GREY, mfc="white", ls="", ms=5, label="inconclusive"),
               matplotlib.patches.Patch(facecolor=BAND, label="margin")]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.12))
    fig.tight_layout(w_pad=0.8)
    save(fig, "fig_audit")


# ============================================================ Figure 3: lambda sweep
def fig_lambda():
    panels = [("(a) Alarm rate, per 100 days", "alarm_rate", [("none", 0.0, BLUE, "o", True, "no change")], "episodes per 100 user-days"),
              ("(b) Delay in days", "rmd", [("standardised", 1.0, BLUE, "o", True, "1 personal SD"),
                                    ("absolute", 1000.0, ORANGE, "s", False, "1000 steps")], "days"),
              ("(c) Detected in 14 days", "det14", [("standardised", 1.0, BLUE, "o", True, "1 personal SD"),
                                                       ("absolute", 1000.0, ORANGE, "s", False, "1000 steps")], "proportion")]
    fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.2))
    for ax, (title, met, series, unit) in zip(axes, panels):
        band(ax, MARGIN[met], orient="h")
        for k, (conv, eff, col, mk, filled, lab) in enumerate(series):
            dx = (k - (len(series) - 1) / 2) * 0.03
            gaps, lo, hi = [], [], []
            for lam in LAMBDAS:
                r = cell(trade, scenario="realistic", kind="sd", convention=conv, effect=eff, metric=met, **{"lambda": lam})
                gaps.append(r.gap_high_minus_low); lo.append(r.gap_lo); hi.append(r.gap_hi)
            x = np.array(LAMBDAS) + dx
            gaps, lo, hi = map(np.array, (gaps, lo, hi))
            ax.errorbar(x, gaps, yerr=[gaps - lo, hi - gaps], color=col, lw=1.0, elinewidth=0.9, capsize=0,
                        marker=mk, ms=4.5, mfc=col if filled else "white", mec=col, mew=1.1, zorder=3)
        ax.set_title(title, loc="left")
        ax.set_ylabel("gap, high minus low" if ax is axes[0] else "")
        ax.set_xticks(LAMBDAS)
        ax.set_xticklabels(["0", "", "0.5", "", "1"])
        ax.grid(axis="y", color=GRID, lw=0.4, zorder=0)
        ax.set_axisbelow(True)
        ax.set_xlim(-0.08, 1.08)
    axes[1].set_xlabel("weight on own variability, $\\lambda$   (0 = fixed threshold, 1 = personal z-score)")
    axes[0].set_xlabel("")
    axes[2].set_xlabel("")
    handles = [Line2D([], [], marker="o", color=BLUE, mfc=BLUE, ms=4.5, label="change of 1 personal SD"),
               Line2D([], [], marker="s", color=ORANGE, mfc="white", ms=4.5, label="change of 1000 steps"),
               matplotlib.patches.Patch(facecolor=BAND, label="margin")]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.17))
    fig.tight_layout(w_pad=0.8)
    save(fig, "fig_lambda")


# ============================================================ Figure 4: sensitivity (20 settings)
def fig_sensitivity():
    items = [("base", sens_gaps, sens_trade)] + [(v, sens_gaps, sens_trade) for v in sens_gaps.variant.unique() if v != "base"] + \
            [(v, comb_gaps, comb_trade) for v in comb_gaps.variant.unique() if v != "base"]
    n = len(items)
    ypos = {v: n - 1 - i for i, (v, _, _) in enumerate(items)}
    fig, axes = plt.subplots(1, 3, figsize=(6.5, 4.6), sharey=True)
    # (a) alarm gap at lambda 0 and 1
    for ax, title, unit in zip(axes, ("(a) Alarm rate, per 100 days", "(b) Delay, 1000 steps (days)", "(c) Delay, 1 SD change (days)"),
                               ("", "", "")):
        ax.set_title(title, loc="left", fontsize=7.5)
        ax.set_xlabel("gap, high minus low")
        clean_x(ax)
    band(axes[0], 1.0); band(axes[1], 1.5); band(axes[2], 1.5)
    for v, g, t in items:
        tt = t[(t.variant == v) & (t.kind == "sd")]
        y = ypos[v]
        a0 = cell(tt, convention="none", metric="alarm_rate", **{"lambda": 0.0})
        a1 = cell(tt, convention="none", metric="alarm_rate", **{"lambda": 1.0})
        d0 = cell(tt, convention="absolute", metric="rmd", **{"lambda": 0.0})
        d1 = cell(tt, convention="absolute", metric="rmd", **{"lambda": 1.0})
        for ax, (r0, r1) in ((axes[0], (a0, a1)), (axes[1], (d0, d1))):
            ax.plot(r0.gap_high_minus_low, y + 0.17, marker="o", ms=4, mfc=BLUE, mec=BLUE, ls="")
            ax.plot(r1.gap_high_minus_low, y - 0.17, marker="s", ms=4, mfc="white", mec=ORANGE, mew=1.1, ls="")
        gg = g[g.variant == v]
        for k, (det, mk) in enumerate((("zscore", "o"), ("ewma", "^"), ("cusum", "D"))):
            r = cell(gg, detector=det, convention="standardised", effect=1.0, metric="rmd")
            yy = y + (1 - k) * 0.24
            axes[2].plot([r.gap_lo, r.gap_hi], [yy, yy], color=INK2, lw=0.6, zorder=3)
            axes[2].plot(r.gap_high_minus_low, yy, marker=mk, ms=3.2, mfc=INK2, mec=INK2, ls="", zorder=4)
    axes[0].set_yticks([ypos[v] for v, _, _ in items])
    axes[0].set_yticklabels([VARIANT_LABEL_PLAIN[v] for v, _, _ in items])
    for ax in axes:
        ax.set_ylim(-0.7, n - 0.3)
        ax.axhline(2.5, color=GRID, lw=0.6)         # divider: one-at-a-time settings above, combinations below
        ax.axhline(n - 1.5, color=GRID, lw=0.6)     # divider: base case above
    for ax in axes[1:]:
        ax.tick_params(axis="y", length=0)
    handles = [Line2D([], [], marker="o", color=BLUE, mfc=BLUE, ls="", ms=4, label="$\\lambda=0$ (fixed threshold)"),
               Line2D([], [], marker="s", color=ORANGE, mfc="white", ls="", ms=4, label="$\\lambda=1$ (personal z-score)"),
               Line2D([], [], marker="o", color=INK2, mfc=INK2, ls="", ms=3.2, label="z-score"),
               Line2D([], [], marker="^", color=INK2, mfc=INK2, ls="", ms=3.2, label="EWMA"),
               Line2D([], [], marker="D", color=INK2, mfc=INK2, ls="", ms=3.2, label="CUSUM"),
               matplotlib.patches.Patch(facecolor=BAND, label="margin")]
    fig.legend(handles=handles, loc="lower center", ncol=6, frameon=False, bbox_to_anchor=(0.5, -0.045), columnspacing=1.2, handletextpad=0.3)
    fig.tight_layout(w_pad=0.6)
    save(fig, "fig_sensitivity")


# ============================================================ Figure 5: LifeSnaps vs simulation
def fig_lifesnaps():
    fl = life_flags(ls, pilot, trade, "missing")
    fl_log = life_flags(ls_log[ls_log.detector.isin(DETECTORS)], pilot, trade, "realistic_log")
    panels = [("(a) Alarm rate, per 100 days", "none", 0.0, "alarm_rate", "episodes"),
              ("(b) Delay in days, 1 SD change", "standardised", 1.0, "rmd", "days"),
              ("(c) Delay in days, 1000 steps", "absolute", 1000.0, "rmd", "days")]
    fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.6), sharey=True)
    ypos = {d: i for i, d in enumerate(reversed(DETECTORS))}
    for ax, (title, conv, eff, met, unit) in zip(axes, panels):
        band(ax, MARGIN[met])
        for det in DETECTORS:
            y = ypos[det]
            r = cell(fl, detector=det, convention=conv, effect=eff, metric=met)
            ax.plot([r.gap_lo, r.gap_hi], [y + 0.18, y + 0.18], color=BLUE, lw=1.2, solid_capstyle="butt", zorder=3)
            ax.plot(r.gap_high_minus_low, y + 0.18, marker="o", ms=4.5, mfc=BLUE, mec=BLUE, ls="", zorder=4)
            ax.plot(r.sim_gap, y + 0.18, marker="D", ms=4.5, mfc=ORANGE, mec="white", mew=0.6, ls="", zorder=5)
            rl = cell(fl_log, detector=det, convention=conv, effect=eff, metric=met)
            ax.plot([rl.gap_lo, rl.gap_hi], [y - 0.18, y - 0.18], color=GREY, lw=1.0, solid_capstyle="butt", zorder=3)
            ax.plot(rl.gap_high_minus_low, y - 0.18, marker="o", ms=4.0, mfc="white", mec=GREY, mew=1.1, ls="", zorder=4)
        ax.set_title(title, loc="left")
        ax.set_xlabel("gap, high minus low")
        clean_x(ax)
        ax.set_ylim(-0.6, len(DETECTORS) - 0.4)
    axes[0].set_yticks([ypos[d] for d in DETECTORS])
    axes[0].set_yticklabels([DET_LABEL[d] for d in DETECTORS])
    for ax in axes[1:]:
        ax.tick_params(axis="y", length=0)
    handles = [Line2D([], [], marker="o", color=BLUE, mfc=BLUE, ms=4.5, label="real users, raw steps (95% interval)"),
               Line2D([], [], marker="D", color=ORANGE, mfc=ORANGE, ls="", ms=4.5, label="simulation (missing days)"),
               Line2D([], [], marker="o", color=GREY, mfc="white", ms=4.0, label="real users, detectors on log steps (exploratory)"),
               matplotlib.patches.Patch(facecolor=BAND, label="margin")]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.17), columnspacing=1.5)
    fig.tight_layout(w_pad=0.8)
    save(fig, "fig_lifesnaps")


if __name__ == "__main__":
    info = fig_example()
    print("example users (baseline SD, 1000 steps in SD):", info)
    fig_audit()
    fig_lambda()
    fig_sensitivity()
    fig_lifesnaps()
    print("figures written")
