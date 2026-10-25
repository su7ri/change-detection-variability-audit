"""Main figure: gaps (high minus low variability tercile) against lambda. Reads results/tradeoff_gaps.csv."""
import csv
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

scen = sys.argv[1] if len(sys.argv) > 1 else "realistic"
rows = [r for r in csv.DictReader(open("results/tradeoff_gaps.csv")) if r["scenario"] == scen]
panels = [("none", "alarm_rate", "Alarm rate gap\n(episodes per 100 user-days)", 1.0),
          ("standardised", "rmd", "Delay gap, change = 1 personal SD\n(days)", 1.5),
          ("absolute", "rmd", "Delay gap, change = 1000 steps\n(days)", 1.5)]
fig, axes = plt.subplots(1, 3, figsize=(11, 3.4), sharex=True)
style = {"sd": ("#1f4e79", "o", "SD scale"), "mad": ("#c0504d", "s", "MAD scale (robust)")}
for ax, (conv, metric, title, margin) in zip(axes, panels):
    ax.axhspan(-margin, margin, color="0.9", zorder=0)
    ax.axhline(0, color="0.4", lw=0.8)
    for kind, (col, mk, lab) in style.items():
        rs = sorted([r for r in rows if r["kind"] == kind and r["convention"] == conv and r["metric"] == metric],
                    key=lambda r: float(r["lambda"]))
        x = [float(r["lambda"]) for r in rs]
        y = [float(r["gap_high_minus_low"]) for r in rs]
        lo = [float(r["gap_lo"]) for r in rs]
        hi = [float(r["gap_hi"]) for r in rs]
        ax.errorbar(x, y, yerr=[[a - b for a, b in zip(y, lo)], [b - a for a, b in zip(y, hi)]], color=col, marker=mk,
                    ms=4, lw=1.4, capsize=2, label=lab)
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("lambda (0 = fixed threshold, 1 = personal scale)", fontsize=8)
    ax.tick_params(labelsize=8)
axes[0].legend(fontsize=8, frameon=False)
fig.suptitle(f"High minus low variability tercile, simulated users ({scen}); grey band = margin", fontsize=9)
fig.tight_layout()
fig.savefig(f"results/tradeoff_{scen}.png", dpi=200)
