# Trade-off experiment (simulated users only)

Scale = lambda x own + (1 - lambda) x population; lambda 0 = fixed threshold in steps, lambda 1 = personal z-score.
Every lambda is re-tuned to 3.33 alarm episodes per 100 user-days. Gap = high minus low variability tercile.
Verdict as in the pilot: REAL / none / unclear (margins: alarm rate 1.0, RMD 1.5 days, detection 14 days 0.10).

## Scenario: realistic

Population scale constants: sd=2103, mad=1711.

### Scale type: sd

| lambda | alarm-rate gap | RMD gap, standardised k=1 | RMD gap, absolute 1000 | det14 gap, standardised | det14 gap, absolute |
|---|---|---|---|---|---|
| 0 | +3.33 [+2.81, +3.91] REAL | -3.37 [-4.03, -2.74] REAL | -2.86 [-3.41, -2.31] REAL | +0.22 [+0.17, +0.27] REAL | +0.22 [+0.17, +0.27] REAL |
| 0.25 | +2.70 [+2.25, +3.13] REAL | -2.39 [-2.93, -1.89] REAL | -1.44 [-1.80, -1.08] unclear | +0.12 [+0.09, +0.16] REAL | +0.09 [+0.06, +0.12] unclear |
| 0.5 | +1.73 [+1.40, +2.08] REAL | -1.44 [-1.82, -1.07] unclear | +0.06 [-0.24, +0.37] none | +0.06 [+0.04, +0.09] none | -0.02 [-0.04, +0.00] none |
| 0.75 | +0.79 [+0.53, +1.05] unclear | -0.49 [-0.73, -0.26] none | +1.33 [+0.97, +1.67] unclear | +0.01 [-0.01, +0.02] none | -0.11 [-0.14, -0.08] REAL |
| 1 | -0.21 [-0.42, -0.00] none | +0.34 [+0.13, +0.53] none | +2.27 [+1.79, +2.73] REAL | -0.02 [-0.04, -0.01] none | -0.17 [-0.21, -0.14] REAL |

### Scale type: mad

| lambda | alarm-rate gap | RMD gap, standardised k=1 | RMD gap, absolute 1000 | det14 gap, standardised | det14 gap, absolute |
|---|---|---|---|---|---|
| 0 | +3.33 [+2.78, +3.89] REAL | -3.37 [-4.01, -2.73] REAL | -2.86 [-3.43, -2.32] REAL | +0.22 [+0.17, +0.27] REAL | +0.22 [+0.17, +0.27] REAL |
| 0.25 | +2.89 [+2.42, +3.31] REAL | -2.57 [-3.13, -2.01] REAL | -1.72 [-2.14, -1.34] REAL | +0.14 [+0.11, +0.19] REAL | +0.11 [+0.08, +0.14] REAL |
| 0.5 | +2.28 [+1.92, +2.65] REAL | -1.79 [-2.19, -1.38] REAL | -0.69 [-1.02, -0.35] none | +0.09 [+0.06, +0.12] unclear | +0.02 [-0.00, +0.05] none |
| 0.75 | +1.55 [+1.28, +1.84] REAL | -1.10 [-1.39, -0.82] none | +0.31 [-0.02, +0.64] none | +0.04 [+0.03, +0.06] none | -0.04 [-0.07, -0.02] none |
| 1 | +0.72 [+0.53, +0.92] none | -0.36 [-0.60, -0.13] none | +1.18 [+0.75, +1.64] unclear | +0.01 [-0.00, +0.03] none | -0.09 [-0.13, -0.06] unclear |

## Scenario: short7

Population scale constants: sd=1795, mad=1455.

### Scale type: sd

| lambda | alarm-rate gap | RMD gap, standardised k=1 | RMD gap, absolute 1000 | det14 gap, standardised | det14 gap, absolute |
|---|---|---|---|---|---|
| 0 | +3.02 [+2.52, +3.51] REAL | -3.90 [-4.62, -3.15] REAL | -3.56 [-4.13, -2.96] REAL | +0.29 [+0.23, +0.35] REAL | +0.32 [+0.27, +0.38] REAL |
| 0.25 | +2.42 [+2.03, +2.81] REAL | -2.99 [-3.62, -2.38] REAL | -2.41 [-2.88, -1.96] REAL | +0.21 [+0.16, +0.26] REAL | +0.22 [+0.18, +0.26] REAL |
| 0.5 | +1.64 [+1.34, +1.98] REAL | -1.92 [-2.33, -1.49] REAL | -0.86 [-1.22, -0.51] none | +0.13 [+0.09, +0.16] REAL | +0.08 [+0.05, +0.11] unclear |
| 0.75 | +0.70 [+0.46, +0.95] none | -0.75 [-1.10, -0.45] none | +0.87 [+0.47, +1.25] none | +0.05 [+0.02, +0.07] none | -0.07 [-0.11, -0.04] unclear |
| 1 | -0.23 [-0.46, -0.02] none | +0.23 [-0.03, +0.51] none | +2.11 [+1.62, +2.59] REAL | -0.02 [-0.04, -0.00] none | -0.18 [-0.22, -0.14] REAL |

### Scale type: mad

| lambda | alarm-rate gap | RMD gap, standardised k=1 | RMD gap, absolute 1000 | det14 gap, standardised | det14 gap, absolute |
|---|---|---|---|---|---|
| 0 | +3.02 [+2.52, +3.50] REAL | -3.90 [-4.58, -3.15] REAL | -3.56 [-4.20, -3.01] REAL | +0.29 [+0.23, +0.35] REAL | +0.32 [+0.27, +0.38] REAL |
| 0.25 | +2.46 [+2.04, +2.83] REAL | -3.11 [-3.74, -2.51] REAL | -2.53 [-3.01, -2.12] REAL | +0.23 [+0.18, +0.28] REAL | +0.23 [+0.19, +0.27] REAL |
| 0.5 | +1.90 [+1.58, +2.22] REAL | -2.32 [-2.80, -1.86] REAL | -1.37 [-1.74, -0.99] unclear | +0.16 [+0.13, +0.20] REAL | +0.13 [+0.10, +0.16] REAL |
| 0.75 | +1.19 [+0.96, +1.41] REAL | -1.43 [-1.78, -1.08] unclear | -0.16 [-0.51, +0.19] none | +0.10 [+0.07, +0.13] unclear | +0.02 [-0.01, +0.05] none |
| 1 | +0.31 [+0.14, +0.48] none | -0.43 [-0.72, -0.14] none | +0.92 [+0.50, +1.38] none | +0.03 [+0.00, +0.05] none | -0.07 [-0.11, -0.04] unclear |

## Scenario: missing

Population scale constants: sd=2050, mad=1668.

### Scale type: sd

| lambda | alarm-rate gap | RMD gap, standardised k=1 | RMD gap, absolute 1000 | det14 gap, standardised | det14 gap, absolute |
|---|---|---|---|---|---|
| 0 | +3.13 [+2.63, +3.66] REAL | -3.22 [-3.90, -2.67] REAL | -2.67 [-3.24, -2.16] REAL | +0.22 [+0.17, +0.28] REAL | +0.21 [+0.17, +0.26] REAL |
| 0.25 | +2.57 [+2.14, +2.98] REAL | -2.27 [-2.81, -1.74] REAL | -1.34 [-1.69, -0.99] unclear | +0.14 [+0.10, +0.18] REAL | +0.08 [+0.05, +0.11] unclear |
| 0.5 | +1.68 [+1.38, +2.01] REAL | -1.29 [-1.66, -0.91] unclear | +0.10 [-0.18, +0.39] none | +0.07 [+0.04, +0.09] none | -0.02 [-0.05, +0.00] none |
| 0.75 | +0.78 [+0.55, +1.04] unclear | -0.43 [-0.67, -0.18] none | +1.27 [+0.90, +1.63] unclear | +0.02 [+0.00, +0.03] none | -0.10 [-0.13, -0.07] REAL |
| 1 | -0.18 [-0.36, +0.01] none | +0.35 [+0.13, +0.56] none | +2.18 [+1.72, +2.62] REAL | -0.02 [-0.03, -0.01] none | -0.16 [-0.20, -0.13] REAL |

### Scale type: mad

| lambda | alarm-rate gap | RMD gap, standardised k=1 | RMD gap, absolute 1000 | det14 gap, standardised | det14 gap, absolute |
|---|---|---|---|---|---|
| 0 | +3.13 [+2.58, +3.65] REAL | -3.22 [-3.92, -2.61] REAL | -2.67 [-3.17, -2.16] REAL | +0.22 [+0.17, +0.27] REAL | +0.21 [+0.17, +0.25] REAL |
| 0.25 | +2.72 [+2.30, +3.13] REAL | -2.36 [-2.91, -1.84] REAL | -1.56 [-1.93, -1.19] REAL | +0.15 [+0.11, +0.19] REAL | +0.10 [+0.07, +0.13] REAL |
| 0.5 | +2.20 [+1.84, +2.54] REAL | -1.63 [-2.03, -1.26] REAL | -0.49 [-0.80, -0.17] none | +0.09 [+0.06, +0.12] unclear | +0.02 [-0.01, +0.05] none |
| 0.75 | +1.57 [+1.31, +1.83] REAL | -0.89 [-1.20, -0.61] none | +0.35 [-0.03, +0.69] none | +0.04 [+0.02, +0.06] none | -0.04 [-0.07, -0.01] none |
| 1 | +0.68 [+0.50, +0.87] none | -0.18 [-0.41, +0.03] none | +1.20 [+0.76, +1.64] unclear | +0.00 [-0.01, +0.02] none | -0.09 [-0.13, -0.06] unclear |

## Pre-set criterion (realistic, sd, RMD)

Absolute-convention gap grows from lambda 0 to 1 by -0.59 days (needs > 1.5); standardised-convention gap shrinks by +3.04 days (needs > 1.5). Trade-off confirmed: **False**.
