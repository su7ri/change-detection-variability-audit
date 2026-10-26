# Sensitivity analysis (simulated users only)

One factor of the `realistic` simulator is changed at a time; everything else is as in the base case.
Detectors are re-tuned to the variant's alarm-rate target on a separate calibration set. Gap = high minus low variability tercile.
Criteria were fixed before the run (ANALYSIS_PLAN.md, 2026-10-26): R1 no REAL delay or detection gap for the personal detectors (standardised, 1 SD); R2 the crossing (alarm gap at lambda 0 above +1.0 and at lambda 1 below +1.0; absolute-convention delay gap at most -1.5 days at lambda 0 and at least +1.5 days at lambda 1); R3 some lambda has all three gaps inside the margins (alarm +/-1.0, delay +/-1.5 days in both conventions).

## Criteria by variant

| variant | factor: level | R1 | R2 | R3 (balanced lambda) | alarm gap lambda 0 / 1 | abs. delay gap lambda 0 / 1 (days) | CUSUM alarm-rate gap |
|---|---|---|---|---|---|---|---|
| base | base: - | yes | yes | yes (0.75) | +3.33 / -0.21 | -2.86 / +2.27 | -0.99 |
| target_1.5 | alarm-rate target: 1.5 per 100 | yes | yes | yes (0.75) | +2.37 / -0.29 | -3.50 / +2.73 | -0.59 |
| target_6.0 | alarm-rate target: 6.0 per 100 | yes | NO | yes (0.75, 1) | +3.03 / +0.07 | -0.86 / +1.47 | -1.07 |
| calseed_303 | calibration seed: 303 | yes | yes | yes (0.75) | +3.36 / -0.22 | -2.81 / +2.24 | -0.96 |
| calseed_404 | calibration seed: 404 | yes | yes | yes (0.75) | +3.30 / -0.22 | -3.02 / +2.24 | -0.95 |
| evalseed_505 | evaluation seed: 505 | yes | yes | yes (0.75) | +3.02 / -0.28 | -3.02 / +1.96 | -0.73 |
| evalseed_606 | evaluation seed: 606 | yes | yes | NO | +3.60 / -0.38 | -3.14 / +2.76 | -1.12 |
| users_600 | number of users: 600 | yes | yes | yes (0.75) | +3.20 / -0.19 | -2.98 / +2.07 | -0.88 |
| phi_none | autocorrelation: none (phi = 0) | yes | yes | yes (0.75) | +3.58 / -0.13 | -2.71 / +2.43 | -1.11 |
| phi_strong | autocorrelation: strong (U(0.3, 0.8)) | yes | yes | yes (0.75) | +2.75 / -0.31 | -2.74 / +1.75 | -0.67 |
| spread_narrow | variability spread: log-SD 0.20 | yes | NO | yes (0.5, 0.75, 1) | +1.69 / -0.14 | -1.33 / +1.04 | -0.51 |
| spread_wide | variability spread: log-SD 0.55 | yes | yes | NO | +4.93 / -0.25 | -4.56 / +3.35 | -1.52 |
| tails_gauss | noise tails: Gaussian | yes | yes | yes (0.75) | +3.22 / -0.23 | -2.84 / +2.06 | -0.92 |
| tails_t3 | noise tails: Student-t, 3 df | yes | yes | yes (0.75) | +3.05 / -0.13 | -2.68 / +1.84 | -0.79 |
| corr_neg | level-variability correlation: -0.4 | yes | yes | yes (0.75) | +2.41 / -0.21 | -1.95 / +1.54 | -0.99 |
| corr_pos | level-variability correlation: +0.4 | yes | yes | NO | +4.24 / -0.21 | -3.75 / +2.94 | -0.99 |
| ramp14 | shape of the change: 14-day ramp | yes | NO | yes (0.75, 1) | +3.33 / -0.21 | -3.70 / +1.21 | -0.99 |

## Verdict per claim (16 changed variants; base case shown above for reference)

- **R1 personal detectors show no real delay or detection gap (1 SD)**: holds in 16 of 16 variants, **robust**.
- **R2 the crossing of the two equality conventions**: holds in 13 of 16 variants, **mostly robust**. Fails in: target_6.0, spread_narrow, ramp14.
- **R3 a balanced lambda exists**: holds in 13 of 16 variants, **mostly robust**. Fails in: evalseed_606, spread_wide, corr_pos.

## Exploratory: can a variant reproduce the real-data CUSUM alarm-rate gap (about -3.3)?

No variant reaches -2.0; the most negative is spread_wide (-1.52). The real-data gap stays unexplained.

## Personal detectors, standardised 1 SD: gap [95% interval] and verdict

| variant | zscore rmd | zscore det14 | ewma rmd | ewma det14 | cusum rmd | cusum det14 |
|---|---|---|---|---|---|---|
| base | +0.34 [+0.12, +0.55] none | -0.02 [-0.04, -0.01] none | +0.31 [+0.06, +0.53] none | -0.02 [-0.03, -0.01] none | +0.31 [+0.12, +0.51] none | -0.02 [-0.03, -0.01] none |
| target_1.5 | +0.34 [+0.07, +0.61] none | -0.03 [-0.05, -0.00] none | +0.46 [+0.19, +0.72] none | -0.03 [-0.05, -0.01] none | +0.41 [+0.19, +0.67] none | -0.02 [-0.03, -0.00] none |
| target_6.0 | +0.10 [-0.08, +0.26] none | -0.00 [-0.01, +0.00] none | +0.20 [+0.01, +0.38] none | -0.01 [-0.02, -0.00] none | +0.09 [-0.05, +0.25] none | -0.01 [-0.02, -0.00] none |
| calseed_303 | +0.36 [+0.15, +0.58] none | -0.02 [-0.04, -0.01] none | +0.34 [+0.09, +0.56] none | -0.02 [-0.04, -0.01] none | +0.30 [+0.11, +0.49] none | -0.02 [-0.02, -0.01] none |
| calseed_404 | +0.36 [+0.15, +0.58] none | -0.02 [-0.04, -0.01] none | +0.34 [+0.09, +0.55] none | -0.02 [-0.04, -0.01] none | +0.30 [+0.11, +0.49] none | -0.02 [-0.02, -0.01] none |
| evalseed_505 | +0.03 [-0.20, +0.26] none | -0.01 [-0.03, +0.00] none | +0.11 [-0.13, +0.35] none | -0.01 [-0.02, +0.01] none | +0.21 [-0.01, +0.42] none | -0.01 [-0.02, -0.00] none |
| evalseed_606 | +0.32 [+0.09, +0.57] none | -0.02 [-0.03, -0.00] none | +0.34 [+0.12, +0.58] none | -0.02 [-0.04, -0.01] none | +0.26 [+0.06, +0.46] none | -0.02 [-0.03, -0.01] none |
| users_600 | +0.14 [-0.02, +0.31] none | -0.01 [-0.02, -0.00] none | +0.12 [-0.06, +0.30] none | -0.01 [-0.02, -0.00] none | +0.26 [+0.11, +0.43] none | -0.01 [-0.02, -0.01] none |
| phi_none | +0.33 [+0.15, +0.51] none | -0.02 [-0.02, -0.01] none | +0.34 [+0.15, +0.52] none | -0.02 [-0.03, -0.01] none | +0.28 [+0.12, +0.46] none | -0.01 [-0.02, -0.01] none |
| phi_strong | -0.06 [-0.30, +0.22] none | +0.01 [-0.01, +0.03] none | +0.06 [-0.22, +0.33] none | -0.01 [-0.03, +0.01] none | +0.03 [-0.21, +0.30] none | -0.01 [-0.02, +0.01] none |
| spread_narrow | +0.05 [-0.14, +0.25] none | -0.01 [-0.02, +0.01] none | +0.09 [-0.13, +0.30] none | -0.01 [-0.02, +0.00] none | +0.17 [-0.01, +0.34] none | -0.01 [-0.02, -0.00] none |
| spread_wide | +0.64 [+0.42, +0.87] none | -0.04 [-0.06, -0.03] none | +0.66 [+0.41, +0.91] none | -0.04 [-0.05, -0.03] none | +0.76 [+0.53, +1.01] none | -0.04 [-0.05, -0.03] none |
| tails_gauss | +0.13 [-0.10, +0.37] none | -0.00 [-0.02, +0.01] none | -0.05 [-0.25, +0.17] none | +0.00 [-0.01, +0.01] none | -0.04 [-0.22, +0.14] none | +0.00 [-0.01, +0.01] none |
| tails_t3 | +0.03 [-0.18, +0.24] none | -0.01 [-0.02, +0.01] none | +0.05 [-0.18, +0.29] none | -0.01 [-0.03, -0.00] none | +0.21 [+0.01, +0.43] none | -0.02 [-0.03, -0.01] none |
| corr_neg | +0.34 [+0.12, +0.55] none | -0.02 [-0.04, -0.01] none | +0.31 [+0.06, +0.53] none | -0.02 [-0.03, -0.01] none | +0.31 [+0.12, +0.51] none | -0.02 [-0.03, -0.01] none |
| corr_pos | +0.34 [+0.12, +0.55] none | -0.02 [-0.04, -0.01] none | +0.31 [+0.06, +0.53] none | -0.02 [-0.03, -0.01] none | +0.31 [+0.12, +0.51] none | -0.02 [-0.03, -0.01] none |
| ramp14 | +0.18 [-0.10, +0.49] none | -0.01 [-0.04, +0.01] none | +0.32 [+0.05, +0.58] none | -0.02 [-0.05, -0.00] none | +0.58 [+0.34, +0.82] none | -0.02 [-0.03, +0.00] none |

## Alarm-rate gap by detector (per 100 user-days)

| variant | fixed | zscore | ewma | cusum |
|---|---|---|---|---|
| base | +3.33 [+2.81, +3.91] | -0.21 [-0.41, +0.00] | -0.47 [-0.65, -0.29] | -0.99 [-1.22, -0.79] |
| target_1.5 | +2.37 [+1.95, +2.85] | -0.29 [-0.46, -0.12] | -0.46 [-0.61, -0.31] | -0.59 [-0.76, -0.42] |
| target_6.0 | +3.03 [+2.52, +3.51] | +0.07 [-0.09, +0.23] | -0.26 [-0.45, -0.08] | -1.07 [-1.29, -0.85] |
| calseed_303 | +3.36 [+2.83, +3.93] | -0.22 [-0.43, -0.01] | -0.48 [-0.67, -0.29] | -0.96 [-1.18, -0.75] |
| calseed_404 | +3.30 [+2.79, +3.87] | -0.22 [-0.42, -0.01] | -0.47 [-0.66, -0.29] | -0.95 [-1.17, -0.75] |
| evalseed_505 | +3.02 [+2.46, +3.59] | -0.28 [-0.49, -0.09] | -0.46 [-0.66, -0.26] | -0.73 [-0.94, -0.54] |
| evalseed_606 | +3.60 [+3.01, +4.15] | -0.38 [-0.61, -0.14] | -0.61 [-0.81, -0.42] | -1.12 [-1.33, -0.93] |
| users_600 | +3.20 [+2.82, +3.59] | -0.19 [-0.35, -0.04] | -0.38 [-0.51, -0.23] | -0.88 [-1.04, -0.73] |
| phi_none | +3.58 [+3.01, +4.09] | -0.13 [-0.25, -0.01] | -0.52 [-0.67, -0.37] | -1.11 [-1.30, -0.92] |
| phi_strong | +2.75 [+2.26, +3.26] | -0.31 [-0.56, -0.06] | -0.43 [-0.62, -0.22] | -0.67 [-0.88, -0.46] |
| spread_narrow | +1.69 [+1.18, +2.20] | -0.14 [-0.35, +0.06] | -0.26 [-0.44, -0.08] | -0.51 [-0.69, -0.33] |
| spread_wide | +4.93 [+4.35, +5.47] | -0.25 [-0.47, -0.03] | -0.73 [-0.94, -0.53] | -1.52 [-1.76, -1.29] |
| tails_gauss | +3.22 [+2.73, +3.70] | -0.23 [-0.43, -0.02] | -0.37 [-0.55, -0.16] | -0.92 [-1.15, -0.70] |
| tails_t3 | +3.05 [+2.51, +3.56] | -0.13 [-0.31, +0.08] | -0.37 [-0.57, -0.17] | -0.79 [-0.98, -0.58] |
| corr_neg | +2.41 [+1.91, +2.92] | -0.21 [-0.41, +0.00] | -0.47 [-0.65, -0.29] | -0.99 [-1.22, -0.79] |
| corr_pos | +4.24 [+3.73, +4.78] | -0.21 [-0.41, +0.00] | -0.47 [-0.65, -0.29] | -0.99 [-1.22, -0.79] |
| ramp14 | +3.33 [+2.81, +3.91] | -0.21 [-0.41, +0.00] | -0.47 [-0.65, -0.29] | -0.99 [-1.22, -0.79] |

## Time

base: 11s, target_1.5: 11s, target_6.0: 10s, calseed_303: 11s, calseed_404: 11s, evalseed_505: 11s, evalseed_606: 11s, users_600: 18s, phi_none: 12s, phi_strong: 12s, spread_narrow: 11s, spread_wide: 11s, tails_gauss: 10s, tails_t3: 11s, corr_neg: 11s, corr_pos: 11s, ramp14: 11s
