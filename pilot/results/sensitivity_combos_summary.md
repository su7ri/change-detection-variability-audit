# Combined-change check (simulated users only)

Several assumptions of the `realistic` simulator are changed together; everything else is as in the base case.
Detectors are re-tuned to the variant's alarm-rate target on a separate calibration set. Gap = high minus low variability tercile.
Criteria were fixed before the run (ANALYSIS_PLAN.md, 2026-10-26): R1 no REAL delay or detection gap for the personal detectors (standardised, 1 SD); R2 the crossing (alarm gap at lambda 0 above +1.0 and at lambda 1 below +1.0; absolute-convention delay gap at most -1.5 days at lambda 0 and at least +1.5 days at lambda 1); R3 some lambda has all three gaps inside the margins (alarm +/-1.0, delay +/-1.5 days in both conventions).

## Criteria by variant

| variant | factor: level | R1 | R2 | R3 (balanced lambda) | alarm gap lambda 0 / 1 | abs. delay gap lambda 0 / 1 (days) | CUSUM alarm-rate gap |
|---|---|---|---|---|---|---|---|
| base | base: - | yes | yes | yes (0.75) | +3.33 / -0.21 | -2.86 / +2.27 | -0.99 |
| combo_weak | C1 weak signal: narrow spread + target 6.0 + 14-day ramp | yes | NO | yes (0.5, 0.75, 1) | +1.48 / -0.02 | -1.07 / +0.35 | -0.52 |
| combo_stress | C2 stress: wide spread + corr +0.4 + t3 + strong phi | yes | yes | NO | +5.07 / -0.21 | -5.29 / +3.23 | -0.84 |
| combo_reallike | C3 real-like: missing days + 14-day windows + corr -0.4 + 14-day ramp | yes | NO | yes (0.75, 1) | +2.10 / -0.16 | -2.39 / +0.66 | -0.75 |

## Verdict per claim (three combinations; no 80% rule)

- **R1 personal detectors show no real delay or detection gap (1 SD)**: holds in 3 of 3.
- **R2 the crossing of the two equality conventions**: holds in 1 of 3. Fails in: combo_weak, combo_reallike.
- **R3 a balanced lambda exists**: holds in 2 of 3. Fails in: combo_stress.

Lambda values whose three intervals all lie inside the margins (descriptive): base: none; combo_weak: 0.75, 1; combo_stress: none; combo_reallike: 0.75, 1.

## Exploratory: can a combination reproduce the real-data CUSUM alarm-rate gap (about -3.3)?

None reaches -2.0; the most negative is base (-0.99). The real-data gap stays unexplained.

## Personal detectors, standardised 1 SD: gap [95% interval] and verdict

| variant | zscore rmd | zscore det14 | ewma rmd | ewma det14 | cusum rmd | cusum det14 |
|---|---|---|---|---|---|---|
| base | +0.34 [+0.12, +0.55] none | -0.02 [-0.04, -0.01] none | +0.31 [+0.06, +0.53] none | -0.02 [-0.03, -0.01] none | +0.31 [+0.12, +0.51] none | -0.02 [-0.03, -0.01] none |
| combo_weak | -0.01 [-0.23, +0.21] none | +0.00 [-0.01, +0.01] none | +0.17 [-0.08, +0.41] none | -0.01 [-0.02, +0.01] none | +0.19 [-0.04, +0.42] none | -0.01 [-0.02, +0.01] none |
| combo_stress | +0.04 [-0.23, +0.28] none | -0.02 [-0.04, +0.00] none | +0.14 [-0.14, +0.43] none | -0.02 [-0.04, +0.01] none | +0.25 [-0.03, +0.53] none | -0.02 [-0.04, -0.00] none |
| combo_reallike | +0.04 [-0.25, +0.32] none | -0.01 [-0.04, +0.01] none | +0.51 [+0.25, +0.77] none | -0.05 [-0.07, -0.02] none | +0.54 [+0.27, +0.80] none | -0.02 [-0.04, -0.00] none |

## Alarm-rate gap by detector (per 100 user-days)

| variant | fixed | zscore | ewma | cusum |
|---|---|---|---|---|
| base | +3.33 [+2.81, +3.91] | -0.21 [-0.41, +0.00] | -0.47 [-0.65, -0.29] | -0.99 [-1.22, -0.79] |
| combo_weak | +1.48 [+1.02, +1.89] | -0.02 [-0.19, +0.14] | -0.13 [-0.32, +0.07] | -0.52 [-0.72, -0.32] |
| combo_stress | +5.07 [+4.57, +5.56] | -0.21 [-0.47, +0.06] | -0.51 [-0.71, -0.29] | -0.84 [-1.02, -0.64] |
| combo_reallike | +2.10 [+1.64, +2.58] | -0.16 [-0.34, +0.05] | -0.53 [-0.71, -0.33] | -0.75 [-0.97, -0.55] |

## Time

base: 11s, combo_weak: 11s, combo_stress: 12s, combo_reallike: 11s
