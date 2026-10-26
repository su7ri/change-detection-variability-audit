# LifeSnaps, exploratory log-scale run (post hoc; see the 2026-10-26 amendment)

## Exploratory: detectors on log(steps), 0-step days not observed

Eligible users 51 of 71 with any steps. Tuned constants: fixed=0.373, zscore=0.744, ewma=1.53, cusum=2.56, shrunk_lam0=0.683, shrunk_lam0.5=0.701, shrunk_lam1=0.744.
Pooled alarm rate (target 3.33): fixed=3.32, zscore=3.36, ewma=3.32, cusum=3.36, shrunk_lam0=3.36, shrunk_lam0.5=3.32, shrunk_lam1=3.32.
Population scale for the shrunk detector: 1 steps. Spearman(log-SD, median steps) = -0.33.

| tercile | users | median steps | share 0-step days | share days without a row | mean eval length | median log-SD |
|---|---|---|---|---|---|---|
| low | 17 | 8726 | 0.001 | 0.139 | 48.4 | 0.40 |
| mid | 17 | 6878 | 0.007 | 0.144 | 49.9 | 0.61 |
| high | 17 | 6292 | 0.015 | 0.175 | 52.2 | 0.93 |

| detector | convention | metric | real gap [95%] | verdict | simulator gap (missing) | consistent | informative | same sign |
|---|---|---|---|---|---|---|---|---|
| fixed | none 0 | alarm_rate | +2.93 [+1.46, +4.41] | REAL | +2.96 | yes | yes | yes |
| fixed | standardised 1 | rmd | -3.07 [-4.84, -1.34] | REAL | -2.64 | yes | yes | yes |
| fixed | standardised 1 | det14 | +0.10 [-0.01, +0.24] | unclear | +0.09 | yes | no | yes |
| fixed | absolute 1000 | rmd | -3.63 [-5.78, -1.44] | REAL | -1.61 | yes | yes | yes |
| fixed | absolute 1000 | det14 | +0.27 [+0.08, +0.44] | REAL | +0.11 | yes | yes | yes |
| zscore | none 0 | alarm_rate | -0.43 [-1.55, +0.78] | unclear | +0.13 | yes | no | NO |
| zscore | standardised 1 | rmd | -0.62 [-1.87, +0.69] | unclear | -0.80 | yes | no | yes |
| zscore | standardised 1 | det14 | -0.01 [-0.06, +0.04] | none | +0.01 | yes | no | NO |
| zscore | absolute 1000 | rmd | -0.03 [-1.93, +1.94] | unclear | +1.55 | yes | no | NO |
| zscore | absolute 1000 | det14 | -0.02 [-0.16, +0.14] | unclear | -0.11 | yes | no | yes |
| ewma | none 0 | alarm_rate | -2.34 [-3.90, -0.72] | REAL | -0.10 | NO | yes | yes |
| ewma | standardised 1 | rmd | -0.44 [-1.90, +0.81] | unclear | -0.61 | yes | no | yes |
| ewma | standardised 1 | det14 | +0.00 [-0.06, +0.08] | none | +0.00 | yes | no | NO |
| ewma | absolute 1000 | rmd | +1.20 [-1.00, +3.37] | unclear | +2.11 | yes | no | yes |
| ewma | absolute 1000 | det14 | -0.13 [-0.31, +0.04] | unclear | -0.13 | yes | no | yes |
| cusum | none 0 | alarm_rate | -3.15 [-4.70, -1.55] | REAL | -0.11 | NO | yes | yes |
| cusum | standardised 1 | rmd | -1.05 [-2.50, +0.36] | unclear | -0.60 | yes | no | yes |
| cusum | standardised 1 | det14 | +0.01 [-0.05, +0.09] | none | +0.00 | yes | no | yes |
| cusum | absolute 1000 | rmd | +1.33 [-0.76, +3.72] | unclear | +2.00 | yes | no | yes |
| cusum | absolute 1000 | det14 | -0.13 [-0.33, +0.06] | unclear | -0.12 | yes | no | yes |

Consistent cells: 18 of 20; informative cells (interval does not contain both the simulated gap and zero): 6 of 20.
