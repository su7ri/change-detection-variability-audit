# LifeSnaps: cross-fitted tuning versus in-sample tuning

51 eligible users, folds of 27 and 24 users (seed 13, stratified by tercile). Gap = high minus low tercile, 95% bootstrap interval (same seed and resamples as lifesnaps.py); verdict by the pre-set rule.

| Detector | constant in-sample | constant fold 0 / fold 1 (tuned on the other fold) | pooled rate fold 0 / fold 1 |
|---|---|---|---|
| fixed | 2368.095 | 2332.048 / 2460.524 | 3.52 / 2.86 |
| zscore | 0.587 | 0.664 / 0.549 | 2.62 / 3.76 |
| ewma | 1.305 | 1.300 / 1.434 | 3.44 / 3.03 |
| cusum | 1.615 | 1.584 / 1.794 | 3.67 / 2.78 |

| Detector | Measure | In-sample gap [95% CI] | verdict | Cross-fitted gap [95% CI] | verdict | same sign |
|---|---|---|---|---|---|---|
| fixed | alarm rate | +0.84 [-0.78, +2.62] | unclear | +0.70 [-0.77, +2.16] | unclear | yes |
| fixed | delay, 1 personal SD | -1.01 [-2.29, +0.28] | unclear | -1.00 [-2.29, +0.33] | unclear | yes |
| fixed | detected in 14 d, 1 personal SD | +0.05 [-0.04, +0.14] | unclear | +0.06 [-0.04, +0.14] | unclear | yes |
| fixed | delay, 1000 steps | -1.45 [-3.61, +0.59] | unclear | -1.37 [-3.52, +0.61] | unclear | yes |
| fixed | detected in 14 d, 1000 steps | +0.16 [-0.02, +0.34] | unclear | +0.14 [-0.05, +0.33] | unclear | yes |
| zscore | alarm rate | -0.54 [-1.96, +1.01] | unclear | +0.14 [-1.42, +1.73] | unclear | NO |
| zscore | delay, 1 personal SD | +0.39 [-0.81, +1.64] | unclear | +0.56 [-0.75, +1.89] | unclear | yes |
| zscore | detected in 14 d, 1 personal SD | -0.00 [-0.07, +0.06] | none | -0.01 [-0.07, +0.06] | none | yes |
| zscore | delay, 1000 steps | +1.46 [-0.63, +3.65] | unclear | +1.60 [-0.69, +4.10] | unclear | yes |
| zscore | detected in 14 d, 1000 steps | -0.17 [-0.35, +0.03] | unclear | -0.20 [-0.38, -0.00] | REAL | yes |
| ewma | alarm rate | -0.69 [-2.48, +1.13] | unclear | -0.90 [-2.74, +0.97] | unclear | yes |
| ewma | delay, 1 personal SD | +0.94 [-0.68, +2.64] | unclear | +1.06 [-0.55, +2.76] | unclear | yes |
| ewma | detected in 14 d, 1 personal SD | -0.05 [-0.13, +0.02] | unclear | -0.06 [-0.14, +0.00] | unclear | yes |
| ewma | delay, 1000 steps | +2.29 [-0.44, +4.77] | unclear | +2.11 [-0.58, +4.71] | unclear | yes |
| ewma | detected in 14 d, 1000 steps | -0.26 [-0.45, -0.04] | REAL | -0.24 [-0.44, +0.00] | unclear | yes |
| cusum | alarm rate | -3.33 [-4.86, -1.62] | REAL | -2.98 [-4.50, -1.19] | REAL | yes |
| cusum | delay, 1 personal SD | +1.50 [+0.21, +3.00] | REAL | +1.41 [+0.16, +2.88] | unclear | yes |
| cusum | detected in 14 d, 1 personal SD | -0.08 [-0.18, +0.00] | unclear | -0.08 [-0.17, +0.00] | unclear | yes |
| cusum | delay, 1000 steps | +3.29 [+0.85, +5.45] | REAL | +3.74 [+1.46, +5.80] | REAL | yes |
| cusum | detected in 14 d, 1000 steps | -0.30 [-0.45, -0.14] | REAL | -0.35 [-0.51, -0.20] | REAL | yes |

Rule (a): every cell that was REAL in the primary run keeps its sign when cross-fitted: holds (5 cells). Among the other 15 cells, 1 change sign.
Rule (b): CUSUM alarm-rate gap cross-fitted below -1.0 with the interval excluding 0: holds (-2.98 [-4.50, -1.19]).