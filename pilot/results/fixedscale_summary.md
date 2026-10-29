# Fixed-scale z-score (z0) versus the moving-scale z-score

Gap = high minus low variability tercile, 95% bootstrap interval, verdict by the pre-set rule (REAL / none / unclear). z0 divides the window difference by the baseline SD; z by the moving 21-day SD.

## Scenario: realistic

Tuned constant z0: 0.623; pooled alarm rate on the evaluation set 3.38 (target 3.33).

| Measure | z0 gap [95% CI] | z0 verdict | z gap [95% CI] (pilot_gaps.csv) | z verdict |
|---|---|---|---|---|
| alarm rate | +0.13 [-0.04, +0.34] | none | -0.21 [-0.41, +0.00] | none |
| delay, 1 personal SD | +0.30 [+0.08, +0.53] | none | +0.34 [+0.12, +0.55] | none |
| detected in 14 d, 1 personal SD | -0.01 [-0.03, -0.00] | none | -0.02 [-0.04, -0.01] | none |
| delay, 1000 steps | +2.06 [+1.63, +2.53] | REAL | +2.27 [+1.83, +2.73] | REAL |
| detected in 14 d, 1000 steps | -0.17 [-0.21, -0.13] | REAL | -0.17 [-0.21, -0.14] | REAL |

## Scenario: missing

Tuned constant z0: 0.645; pooled alarm rate on the evaluation set 3.37 (target 3.33).

| Measure | z0 gap [95% CI] | z0 verdict | z gap [95% CI] (pilot_gaps.csv) | z verdict |
|---|---|---|---|---|
| alarm rate | +0.15 [-0.03, +0.31] | none | -0.18 [-0.34, +0.02] | none |
| delay, 1 personal SD | +0.44 [+0.23, +0.66] | none | +0.35 [+0.15, +0.56] | none |
| detected in 14 d, 1 personal SD | -0.03 [-0.04, -0.01] | none | -0.02 [-0.03, -0.01] | none |
| delay, 1000 steps | +2.00 [+1.55, +2.45] | REAL | +2.18 [+1.74, +2.62] | REAL |
| detected in 14 d, 1000 steps | -0.17 [-0.21, -0.13] | REAL | -0.16 [-0.20, -0.12] | REAL |
