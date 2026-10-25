# LifeSnaps consistency check (real users; plan frozen in LIFESNAPS_PLAN.md)

Alarm rate, not false-alarm rate: alarms may include real changes. About 20 users per tercile, so intervals are wide.

## Primary: 0-step days treated as not observed

Eligible users 51 of 71 with any steps. Tuned constants: fixed=2.37e+03, zscore=0.587, ewma=1.31, cusum=1.62, shrunk_lam0=0.651, shrunk_lam0.5=0.62, shrunk_lam1=0.587.
Pooled alarm rate (target 3.33): fixed=3.32, zscore=3.32, ewma=3.36, cusum=3.36, shrunk_lam0=3.36, shrunk_lam0.5=3.32, shrunk_lam1=3.32.
Population scale for the shrunk detector: 3638 steps. Spearman(log-SD, median steps) = -0.33.

| tercile | users | median steps | share 0-step days | share days without a row | mean eval length | median log-SD |
|---|---|---|---|---|---|---|
| low | 17 | 8726 | 0.001 | 0.139 | 48.4 | 0.40 |
| mid | 17 | 6878 | 0.007 | 0.144 | 49.9 | 0.61 |
| high | 17 | 6292 | 0.015 | 0.175 | 52.2 | 0.93 |

| detector | convention | metric | real gap [95%] | verdict | simulator gap (missing) | consistent | informative | same sign |
|---|---|---|---|---|---|---|---|---|
| fixed | none 0 | alarm_rate | +0.84 [-0.78, +2.62] | unclear | +3.13 | NO | yes | yes |
| fixed | standardised 1 | rmd | -1.01 [-2.29, +0.28] | unclear | -3.22 | NO | yes | yes |
| fixed | standardised 1 | det14 | +0.05 [-0.04, +0.14] | unclear | +0.22 | NO | yes | yes |
| fixed | absolute 1000 | rmd | -1.45 [-3.61, +0.59] | unclear | -2.67 | yes | no | yes |
| fixed | absolute 1000 | det14 | +0.16 [-0.02, +0.34] | unclear | +0.21 | yes | no | yes |
| zscore | none 0 | alarm_rate | -0.54 [-1.96, +1.01] | unclear | -0.18 | yes | no | yes |
| zscore | standardised 1 | rmd | +0.39 [-0.81, +1.64] | unclear | +0.35 | yes | no | yes |
| zscore | standardised 1 | det14 | -0.00 [-0.07, +0.06] | none | -0.02 | yes | no | yes |
| zscore | absolute 1000 | rmd | +1.46 [-0.63, +3.65] | unclear | +2.18 | yes | no | yes |
| zscore | absolute 1000 | det14 | -0.17 [-0.35, +0.03] | unclear | -0.16 | yes | no | yes |
| ewma | none 0 | alarm_rate | -0.69 [-2.48, +1.13] | unclear | -0.63 | yes | no | yes |
| ewma | standardised 1 | rmd | +0.94 [-0.68, +2.64] | unclear | +0.58 | yes | no | yes |
| ewma | standardised 1 | det14 | -0.05 [-0.13, +0.02] | unclear | -0.03 | yes | no | yes |
| ewma | absolute 1000 | rmd | +2.29 [-0.44, +4.77] | unclear | +2.89 | yes | no | yes |
| ewma | absolute 1000 | det14 | -0.26 [-0.45, -0.04] | REAL | -0.20 | yes | yes | yes |
| cusum | none 0 | alarm_rate | -3.33 [-4.86, -1.62] | REAL | -1.02 | NO | yes | yes |
| cusum | standardised 1 | rmd | +1.50 [+0.21, +3.00] | REAL | +0.64 | yes | yes | yes |
| cusum | standardised 1 | det14 | -0.08 [-0.18, +0.00] | unclear | -0.02 | yes | no | yes |
| cusum | absolute 1000 | rmd | +3.29 [+0.85, +5.45] | REAL | +3.27 | yes | yes | yes |
| cusum | absolute 1000 | det14 | -0.30 [-0.45, -0.14] | REAL | -0.23 | yes | yes | yes |
| shrunk_lam0 | none 0 | alarm_rate | +0.84 [-0.83, +2.62] | unclear | +3.13 | NO | yes | yes |
| shrunk_lam0 | standardised 1 | rmd | -1.01 [-2.22, +0.31] | unclear | -3.22 | NO | yes | yes |
| shrunk_lam0 | standardised 1 | det14 | +0.05 [-0.04, +0.14] | unclear | +0.22 | NO | yes | yes |
| shrunk_lam0 | absolute 1000 | rmd | -1.45 [-3.47, +0.74] | unclear | -2.67 | yes | no | yes |
| shrunk_lam0 | absolute 1000 | det14 | +0.16 [-0.03, +0.35] | unclear | +0.21 | yes | no | yes |
| shrunk_lam0.5 | none 0 | alarm_rate | +0.50 [-0.96, +2.01] | unclear | +1.68 | yes | no | yes |
| shrunk_lam0.5 | standardised 1 | rmd | -0.21 [-1.57, +1.10] | unclear | -1.29 | yes | no | yes |
| shrunk_lam0.5 | standardised 1 | det14 | +0.01 [-0.06, +0.08] | none | +0.07 | yes | no | yes |
| shrunk_lam0.5 | absolute 1000 | rmd | +0.09 [-2.01, +2.27] | unclear | +0.10 | yes | no | yes |
| shrunk_lam0.5 | absolute 1000 | det14 | +0.01 [-0.18, +0.20] | unclear | -0.02 | yes | no | NO |
| shrunk_lam1 | none 0 | alarm_rate | -0.54 [-1.99, +0.89] | unclear | -0.18 | yes | no | yes |
| shrunk_lam1 | standardised 1 | rmd | +0.39 [-0.91, +1.71] | unclear | +0.35 | yes | no | yes |
| shrunk_lam1 | standardised 1 | det14 | -0.00 [-0.07, +0.06] | none | -0.02 | yes | no | yes |
| shrunk_lam1 | absolute 1000 | rmd | +1.46 [-0.67, +3.63] | unclear | +2.18 | yes | no | yes |
| shrunk_lam1 | absolute 1000 | det14 | -0.17 [-0.34, +0.01] | unclear | -0.16 | yes | no | yes |

Consistent cells: 28 of 35; informative cells (interval does not contain both the simulated gap and zero): 11 of 35.

## Sensitivity: 0-step days kept as observed

Eligible users 53 of 71 with any steps. Tuned constants: fixed=2.42e+03, zscore=0.632, ewma=1.48, cusum=1.78, shrunk_lam0=0.659, shrunk_lam0.5=0.625, shrunk_lam1=0.632.
Pooled alarm rate (target 3.33): fixed=3.31, zscore=3.31, ewma=3.31, cusum=3.31, shrunk_lam0=3.35, shrunk_lam0.5=3.35, shrunk_lam1=3.31.
Population scale for the shrunk detector: 3678 steps. Spearman(log-SD, median steps) = -0.38.

| tercile | users | median steps | share 0-step days | share days without a row | mean eval length | median log-SD |
|---|---|---|---|---|---|---|
| low | 18 | 8905 | 0.001 | 0.131 | 48.8 | 0.41 |
| mid | 18 | 6783 | 0.012 | 0.153 | 49.4 | 0.64 |
| high | 17 | 6266 | 0.023 | 0.190 | 52.4 | 0.95 |

| detector | convention | metric | real gap [95%] | verdict | simulator gap (missing) | consistent | informative | same sign |
|---|---|---|---|---|---|---|---|---|
| fixed | none 0 | alarm_rate | +0.86 [-0.71, +2.25] | unclear | +3.13 | NO | yes | yes |
| fixed | standardised 1 | rmd | -1.26 [-2.89, +0.29] | unclear | -3.22 | NO | yes | yes |
| fixed | standardised 1 | det14 | +0.07 [-0.03, +0.19] | unclear | +0.22 | NO | yes | yes |
| fixed | absolute 1000 | rmd | -1.77 [-3.82, +0.43] | unclear | -2.67 | yes | no | yes |
| fixed | absolute 1000 | det14 | +0.22 [+0.02, +0.40] | REAL | +0.21 | yes | yes | yes |
| zscore | none 0 | alarm_rate | -0.21 [-1.69, +1.25] | unclear | -0.18 | yes | no | yes |
| zscore | standardised 1 | rmd | +0.70 [-0.93, +2.26] | unclear | +0.35 | yes | no | yes |
| zscore | standardised 1 | det14 | -0.04 [-0.13, +0.06] | unclear | -0.02 | yes | no | yes |
| zscore | absolute 1000 | rmd | +1.72 [-0.49, +4.01] | unclear | +2.18 | yes | no | yes |
| zscore | absolute 1000 | det14 | -0.16 [-0.36, +0.04] | unclear | -0.16 | yes | no | yes |
| ewma | none 0 | alarm_rate | -1.15 [-2.73, +0.69] | unclear | -0.63 | yes | no | yes |
| ewma | standardised 1 | rmd | +1.30 [-0.57, +3.35] | unclear | +0.58 | yes | no | yes |
| ewma | standardised 1 | det14 | -0.06 [-0.17, +0.03] | unclear | -0.03 | yes | no | yes |
| ewma | absolute 1000 | rmd | +1.62 [-0.89, +4.16] | unclear | +2.89 | yes | no | yes |
| ewma | absolute 1000 | det14 | -0.15 [-0.36, +0.08] | unclear | -0.20 | yes | no | yes |
| cusum | none 0 | alarm_rate | -3.13 [-4.61, -1.53] | REAL | -1.02 | NO | yes | yes |
| cusum | standardised 1 | rmd | +1.65 [+0.13, +3.21] | REAL | +0.64 | yes | yes | yes |
| cusum | standardised 1 | det14 | -0.05 [-0.16, +0.03] | unclear | -0.02 | yes | no | yes |
| cusum | absolute 1000 | rmd | +3.45 [+1.16, +5.47] | REAL | +3.27 | yes | yes | yes |
| cusum | absolute 1000 | det14 | -0.34 [-0.52, -0.15] | REAL | -0.23 | yes | yes | yes |
| shrunk_lam0 | none 0 | alarm_rate | +0.97 [-0.56, +2.56] | unclear | +3.13 | NO | yes | yes |
| shrunk_lam0 | standardised 1 | rmd | -1.26 [-2.93, +0.25] | unclear | -3.22 | NO | yes | yes |
| shrunk_lam0 | standardised 1 | det14 | +0.07 [-0.04, +0.18] | unclear | +0.22 | NO | yes | yes |
| shrunk_lam0 | absolute 1000 | rmd | -1.77 [-4.14, +0.41] | unclear | -2.67 | yes | no | yes |
| shrunk_lam0 | absolute 1000 | det14 | +0.22 [+0.03, +0.42] | REAL | +0.21 | yes | yes | yes |
| shrunk_lam0.5 | none 0 | alarm_rate | +0.47 [-0.86, +2.00] | unclear | +1.68 | yes | no | yes |
| shrunk_lam0.5 | standardised 1 | rmd | -0.37 [-1.78, +1.03] | unclear | -1.29 | yes | no | yes |
| shrunk_lam0.5 | standardised 1 | det14 | +0.02 [-0.07, +0.11] | unclear | +0.07 | yes | no | yes |
| shrunk_lam0.5 | absolute 1000 | rmd | -0.17 [-2.21, +1.98] | unclear | +0.10 | yes | no | NO |
| shrunk_lam0.5 | absolute 1000 | det14 | +0.05 [-0.13, +0.25] | unclear | -0.02 | yes | no | NO |
| shrunk_lam1 | none 0 | alarm_rate | -0.21 [-1.59, +1.17] | unclear | -0.18 | yes | no | yes |
| shrunk_lam1 | standardised 1 | rmd | +0.70 [-0.80, +2.20] | unclear | +0.35 | yes | no | yes |
| shrunk_lam1 | standardised 1 | det14 | -0.04 [-0.14, +0.06] | unclear | -0.02 | yes | no | yes |
| shrunk_lam1 | absolute 1000 | rmd | +1.72 [-0.39, +3.96] | unclear | +2.18 | yes | no | yes |
| shrunk_lam1 | absolute 1000 | det14 | -0.16 [-0.35, +0.05] | unclear | -0.16 | yes | no | yes |

Consistent cells: 28 of 35; informative cells (interval does not contain both the simulated gap and zero): 12 of 35.
