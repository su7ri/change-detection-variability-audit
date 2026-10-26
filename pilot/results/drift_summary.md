# Pilot results (simulated users only)

Target pooled alarm rate 3.33 episodes per 100 user-days. Gap = high minus low variability tercile.
Margins: alarm rate 1.0, RMD 1.5 days, detection within 14 days 0.1.
Verdict: REAL = interval excludes 0 and gap beyond margin; none = interval inside the margin; unclear otherwise.

## Scenario: drift_small

Users per tercile (low, mid, high): [100, 100, 100]. Tuned constants: fixed=1.45e+03, zscore=0.591, ewma=1.4, cusum=1.65.
Pooled alarm rate on the evaluation set (target 3.33): fixed=3.47, zscore=3.31, ewma=3.20, cusum=3.22.
Share of post-onset days at the 0 floor, by tercile (low, mid, high), standardised 2 SD: 0.053, 0.162, 0.408; absolute 2000: 0.012, 0.007, 0.015.

### Alarm episodes per 100 user-days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| none | 0 | fixed | 1.92 | 3.29 | 5.20 | +3.29 | [+2.72, +3.85] | REAL |
| none | 0 | zscore | 3.43 | 3.35 | 3.16 | -0.26 | [-0.46, -0.07] | none |
| none | 0 | ewma | 3.52 | 3.25 | 2.84 | -0.68 | [-0.90, -0.46] | none |
| none | 0 | cusum | 3.72 | 3.30 | 2.63 | -1.09 | [-1.33, -0.86] | REAL |

### Restricted mean delay (days, censored at 14)

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 9.44 | 6.92 | 5.05 | -4.38 | [-5.11, -3.67] | REAL |
| standardised | 0.5 | zscore | 6.20 | 6.29 | 6.23 | +0.03 | [-0.26, +0.33] | none |
| standardised | 0.5 | ewma | 6.37 | 6.19 | 6.31 | -0.06 | [-0.36, +0.24] | none |
| standardised | 0.5 | cusum | 5.96 | 5.86 | 6.13 | +0.16 | [-0.15, +0.49] | none |
| standardised | 1 | fixed | 6.68 | 4.56 | 3.24 | -3.43 | [-4.01, -2.80] | REAL |
| standardised | 1 | zscore | 3.85 | 3.85 | 3.93 | +0.08 | [-0.13, +0.30] | none |
| standardised | 1 | ewma | 3.69 | 3.40 | 3.52 | -0.16 | [-0.39, +0.05] | none |
| standardised | 1 | cusum | 2.94 | 2.77 | 2.83 | -0.10 | [-0.31, +0.11] | none |
| standardised | 1.5 | fixed | 4.75 | 3.16 | 2.33 | -2.42 | [-2.93, -1.93] | REAL |
| standardised | 1.5 | zscore | 2.59 | 2.65 | 2.84 | +0.25 | [+0.07, +0.41] | none |
| standardised | 1.5 | ewma | 2.18 | 2.07 | 2.33 | +0.16 | [-0.03, +0.33] | none |
| standardised | 1.5 | cusum | 1.53 | 1.49 | 1.67 | +0.14 | [-0.01, +0.29] | none |
| standardised | 2 | fixed | 3.45 | 2.33 | 1.82 | -1.63 | [-2.07, -1.24] | REAL |
| standardised | 2 | zscore | 1.88 | 1.96 | 2.28 | +0.40 | [+0.25, +0.55] | none |
| standardised | 2 | ewma | 1.38 | 1.38 | 1.77 | +0.39 | [+0.25, +0.56] | none |
| standardised | 2 | cusum | 0.84 | 0.86 | 1.19 | +0.35 | [+0.21, +0.51] | none |
| absolute | 500 | fixed | 10.63 | 8.70 | 6.97 | -3.66 | [-4.29, -3.07] | REAL |
| absolute | 500 | zscore | 7.40 | 8.18 | 8.93 | +1.54 | [+1.10, +1.97] | REAL |
| absolute | 500 | ewma | 7.76 | 8.55 | 9.45 | +1.69 | [+1.27, +2.12] | REAL |
| absolute | 500 | cusum | 7.39 | 8.52 | 9.61 | +2.22 | [+1.76, +2.66] | REAL |
| absolute | 1000 | fixed | 8.76 | 7.12 | 5.82 | -2.94 | [-3.41, -2.41] | REAL |
| absolute | 1000 | zscore | 5.44 | 6.66 | 7.70 | +2.25 | [+1.78, +2.72] | REAL |
| absolute | 1000 | ewma | 5.61 | 6.66 | 7.98 | +2.37 | [+1.85, +2.87] | REAL |
| absolute | 1000 | cusum | 5.23 | 6.51 | 8.03 | +2.80 | [+2.24, +3.31] | REAL |
| absolute | 1500 | fixed | 6.46 | 5.62 | 4.82 | -1.64 | [-1.97, -1.29] | REAL |
| absolute | 1500 | zscore | 4.12 | 5.31 | 6.63 | +2.51 | [+2.03, +2.98] | REAL |
| absolute | 1500 | ewma | 4.09 | 5.20 | 6.63 | +2.54 | [+2.01, +3.08] | REAL |
| absolute | 1500 | cusum | 3.66 | 4.82 | 6.64 | +2.98 | [+2.42, +3.56] | REAL |
| absolute | 2000 | fixed | 4.65 | 4.35 | 4.01 | -0.64 | [-0.88, -0.40] | none |
| absolute | 2000 | zscore | 3.26 | 4.29 | 5.63 | +2.36 | [+1.90, +2.79] | REAL |
| absolute | 2000 | ewma | 3.02 | 4.02 | 5.58 | +2.55 | [+2.06, +3.03] | REAL |
| absolute | 2000 | cusum | 2.58 | 3.64 | 5.50 | +2.91 | [+2.36, +3.46] | REAL |

### Detection within 14 days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 0.50 | 0.72 | 0.86 | +0.36 | [+0.30, +0.43] | REAL |
| standardised | 0.5 | zscore | 0.80 | 0.79 | 0.81 | +0.02 | [-0.01, +0.04] | none |
| standardised | 0.5 | ewma | 0.77 | 0.80 | 0.80 | +0.02 | [-0.01, +0.05] | none |
| standardised | 0.5 | cusum | 0.81 | 0.83 | 0.82 | +0.01 | [-0.01, +0.03] | none |
| standardised | 1 | fixed | 0.75 | 0.89 | 0.96 | +0.21 | [+0.16, +0.26] | REAL |
| standardised | 1 | zscore | 0.95 | 0.95 | 0.94 | -0.01 | [-0.02, +0.01] | none |
| standardised | 1 | ewma | 0.94 | 0.95 | 0.95 | +0.01 | [-0.01, +0.03] | none |
| standardised | 1 | cusum | 0.97 | 0.97 | 0.97 | +0.01 | [-0.00, +0.02] | none |
| standardised | 1.5 | fixed | 0.88 | 0.96 | 0.99 | +0.11 | [+0.07, +0.15] | REAL |
| standardised | 1.5 | zscore | 0.98 | 0.98 | 0.98 | -0.01 | [-0.02, -0.00] | none |
| standardised | 1.5 | ewma | 0.99 | 0.99 | 0.98 | -0.01 | [-0.02, +0.00] | none |
| standardised | 1.5 | cusum | 0.99 | 0.99 | 0.98 | -0.01 | [-0.02, -0.00] | none |
| standardised | 2 | fixed | 0.95 | 0.98 | 1.00 | +0.05 | [+0.03, +0.08] | none |
| standardised | 2 | zscore | 0.99 | 0.99 | 0.98 | -0.01 | [-0.02, -0.00] | none |
| standardised | 2 | ewma | 1.00 | 1.00 | 0.98 | -0.01 | [-0.02, -0.00] | none |
| standardised | 2 | cusum | 1.00 | 1.00 | 0.99 | -0.01 | [-0.02, -0.01] | none |
| absolute | 500 | fixed | 0.38 | 0.57 | 0.71 | +0.34 | [+0.28, +0.40] | REAL |
| absolute | 500 | zscore | 0.69 | 0.63 | 0.57 | -0.13 | [-0.16, -0.09] | REAL |
| absolute | 500 | ewma | 0.65 | 0.60 | 0.52 | -0.13 | [-0.17, -0.10] | REAL |
| absolute | 500 | cusum | 0.68 | 0.60 | 0.49 | -0.19 | [-0.22, -0.15] | REAL |
| absolute | 1000 | fixed | 0.59 | 0.72 | 0.82 | +0.23 | [+0.18, +0.28] | REAL |
| absolute | 1000 | zscore | 0.85 | 0.77 | 0.70 | -0.16 | [-0.19, -0.12] | REAL |
| absolute | 1000 | ewma | 0.82 | 0.76 | 0.66 | -0.17 | [-0.20, -0.13] | REAL |
| absolute | 1000 | cusum | 0.83 | 0.76 | 0.64 | -0.19 | [-0.23, -0.15] | REAL |
| absolute | 1500 | fixed | 0.81 | 0.85 | 0.90 | +0.09 | [+0.06, +0.11] | unclear |
| absolute | 1500 | zscore | 0.92 | 0.87 | 0.78 | -0.14 | [-0.17, -0.11] | REAL |
| absolute | 1500 | ewma | 0.91 | 0.86 | 0.76 | -0.15 | [-0.18, -0.11] | REAL |
| absolute | 1500 | cusum | 0.91 | 0.86 | 0.74 | -0.17 | [-0.21, -0.13] | REAL |
| absolute | 2000 | fixed | 0.94 | 0.94 | 0.95 | +0.00 | [-0.01, +0.02] | none |
| absolute | 2000 | zscore | 0.95 | 0.92 | 0.84 | -0.11 | [-0.14, -0.08] | REAL |
| absolute | 2000 | ewma | 0.95 | 0.93 | 0.84 | -0.11 | [-0.14, -0.08] | REAL |
| absolute | 2000 | cusum | 0.95 | 0.92 | 0.82 | -0.14 | [-0.17, -0.11] | REAL |

## Scenario: drift

Users per tercile (low, mid, high): [100, 100, 100]. Tuned constants: fixed=1.45e+03, zscore=0.598, ewma=1.51, cusum=1.8.
Pooled alarm rate on the evaluation set (target 3.33): fixed=3.47, zscore=3.33, ewma=3.21, cusum=3.24.
Share of post-onset days at the 0 floor, by tercile (low, mid, high), standardised 2 SD: 0.058, 0.168, 0.416; absolute 2000: 0.013, 0.008, 0.018.

### Alarm episodes per 100 user-days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| none | 0 | fixed | 1.90 | 3.30 | 5.20 | +3.30 | [+2.75, +3.82] | REAL |
| none | 0 | zscore | 3.49 | 3.38 | 3.13 | -0.36 | [-0.57, -0.17] | none |
| none | 0 | ewma | 3.65 | 3.27 | 2.72 | -0.92 | [-1.17, -0.67] | unclear |
| none | 0 | cusum | 3.80 | 3.32 | 2.59 | -1.21 | [-1.45, -0.96] | REAL |

### Restricted mean delay (days, censored at 14)

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 9.48 | 7.00 | 5.02 | -4.46 | [-5.16, -3.69] | REAL |
| standardised | 0.5 | zscore | 6.39 | 6.40 | 6.33 | -0.07 | [-0.36, +0.25] | none |
| standardised | 0.5 | ewma | 6.99 | 6.78 | 6.86 | -0.13 | [-0.48, +0.17] | none |
| standardised | 0.5 | cusum | 6.46 | 6.37 | 6.59 | +0.14 | [-0.19, +0.46] | none |
| standardised | 1 | fixed | 6.73 | 4.60 | 3.20 | -3.53 | [-4.11, -2.89] | REAL |
| standardised | 1 | zscore | 4.05 | 4.00 | 4.05 | -0.01 | [-0.24, +0.22] | none |
| standardised | 1 | ewma | 4.34 | 3.95 | 3.98 | -0.36 | [-0.61, -0.10] | none |
| standardised | 1 | cusum | 3.50 | 3.14 | 3.22 | -0.28 | [-0.53, -0.05] | none |
| standardised | 1.5 | fixed | 4.75 | 3.21 | 2.32 | -2.43 | [-2.96, -1.96] | REAL |
| standardised | 1.5 | zscore | 2.68 | 2.71 | 2.91 | +0.23 | [+0.04, +0.41] | none |
| standardised | 1.5 | ewma | 2.70 | 2.42 | 2.60 | -0.10 | [-0.29, +0.12] | none |
| standardised | 1.5 | cusum | 1.88 | 1.76 | 1.87 | -0.01 | [-0.18, +0.17] | none |
| standardised | 2 | fixed | 3.46 | 2.36 | 1.83 | -1.63 | [-2.07, -1.24] | REAL |
| standardised | 2 | zscore | 1.96 | 2.02 | 2.33 | +0.37 | [+0.21, +0.52] | none |
| standardised | 2 | ewma | 1.73 | 1.61 | 1.95 | +0.22 | [+0.04, +0.40] | none |
| standardised | 2 | cusum | 1.05 | 1.02 | 1.37 | +0.31 | [+0.17, +0.48] | none |
| absolute | 500 | fixed | 10.63 | 8.66 | 6.94 | -3.68 | [-4.30, -3.04] | REAL |
| absolute | 500 | zscore | 7.50 | 8.21 | 9.00 | +1.50 | [+1.08, +1.91] | unclear |
| absolute | 500 | ewma | 8.26 | 9.00 | 9.90 | +1.64 | [+1.24, +2.04] | REAL |
| absolute | 500 | cusum | 7.75 | 8.78 | 9.89 | +2.14 | [+1.68, +2.58] | REAL |
| absolute | 1000 | fixed | 8.79 | 7.16 | 5.76 | -3.03 | [-3.52, -2.53] | REAL |
| absolute | 1000 | zscore | 5.69 | 6.72 | 7.80 | +2.11 | [+1.63, +2.55] | REAL |
| absolute | 1000 | ewma | 6.32 | 7.20 | 8.53 | +2.21 | [+1.76, +2.69] | REAL |
| absolute | 1000 | cusum | 5.77 | 6.89 | 8.33 | +2.56 | [+2.05, +3.08] | REAL |
| absolute | 1500 | fixed | 6.58 | 5.63 | 4.80 | -1.77 | [-2.13, -1.39] | REAL |
| absolute | 1500 | zscore | 4.33 | 5.45 | 6.73 | +2.39 | [+1.92, +2.87] | REAL |
| absolute | 1500 | ewma | 4.86 | 5.88 | 7.22 | +2.36 | [+1.81, +2.92] | REAL |
| absolute | 1500 | cusum | 4.18 | 5.33 | 7.03 | +2.85 | [+2.32, +3.43] | REAL |
| absolute | 2000 | fixed | 4.76 | 4.42 | 4.05 | -0.71 | [-0.96, -0.47] | none |
| absolute | 2000 | zscore | 3.42 | 4.43 | 5.79 | +2.37 | [+1.88, +2.80] | REAL |
| absolute | 2000 | ewma | 3.69 | 4.62 | 6.12 | +2.43 | [+1.92, +2.97] | REAL |
| absolute | 2000 | cusum | 3.07 | 4.14 | 5.92 | +2.85 | [+2.31, +3.41] | REAL |

### Detection within 14 days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 0.49 | 0.71 | 0.86 | +0.37 | [+0.31, +0.43] | REAL |
| standardised | 0.5 | zscore | 0.78 | 0.78 | 0.80 | +0.03 | [+0.00, +0.05] | none |
| standardised | 0.5 | ewma | 0.70 | 0.74 | 0.75 | +0.05 | [+0.02, +0.08] | none |
| standardised | 0.5 | cusum | 0.76 | 0.78 | 0.78 | +0.03 | [-0.00, +0.05] | none |
| standardised | 1 | fixed | 0.74 | 0.89 | 0.96 | +0.22 | [+0.17, +0.27] | REAL |
| standardised | 1 | zscore | 0.93 | 0.93 | 0.93 | +0.01 | [-0.01, +0.02] | none |
| standardised | 1 | ewma | 0.88 | 0.92 | 0.92 | +0.04 | [+0.02, +0.06] | none |
| standardised | 1 | cusum | 0.93 | 0.95 | 0.96 | +0.03 | [+0.01, +0.04] | none |
| standardised | 1.5 | fixed | 0.88 | 0.96 | 0.99 | +0.11 | [+0.07, +0.15] | REAL |
| standardised | 1.5 | zscore | 0.98 | 0.98 | 0.97 | -0.01 | [-0.02, +0.00] | none |
| standardised | 1.5 | ewma | 0.96 | 0.97 | 0.97 | +0.01 | [-0.01, +0.02] | none |
| standardised | 1.5 | cusum | 0.98 | 0.98 | 0.98 | +0.00 | [-0.01, +0.01] | none |
| standardised | 2 | fixed | 0.95 | 0.98 | 1.00 | +0.05 | [+0.03, +0.08] | none |
| standardised | 2 | zscore | 0.99 | 0.99 | 0.98 | -0.01 | [-0.02, -0.00] | none |
| standardised | 2 | ewma | 0.99 | 0.99 | 0.98 | -0.01 | [-0.01, +0.00] | none |
| standardised | 2 | cusum | 1.00 | 1.00 | 0.98 | -0.01 | [-0.02, -0.01] | none |
| absolute | 500 | fixed | 0.38 | 0.57 | 0.72 | +0.34 | [+0.28, +0.39] | REAL |
| absolute | 500 | zscore | 0.67 | 0.62 | 0.55 | -0.12 | [-0.16, -0.08] | REAL |
| absolute | 500 | ewma | 0.59 | 0.55 | 0.47 | -0.12 | [-0.16, -0.08] | REAL |
| absolute | 500 | cusum | 0.63 | 0.56 | 0.46 | -0.17 | [-0.20, -0.13] | REAL |
| absolute | 1000 | fixed | 0.58 | 0.72 | 0.82 | +0.24 | [+0.20, +0.29] | REAL |
| absolute | 1000 | zscore | 0.82 | 0.76 | 0.68 | -0.14 | [-0.18, -0.11] | REAL |
| absolute | 1000 | ewma | 0.74 | 0.70 | 0.60 | -0.14 | [-0.18, -0.10] | REAL |
| absolute | 1000 | cusum | 0.78 | 0.71 | 0.60 | -0.17 | [-0.21, -0.13] | REAL |
| absolute | 1500 | fixed | 0.79 | 0.85 | 0.90 | +0.11 | [+0.08, +0.13] | REAL |
| absolute | 1500 | zscore | 0.90 | 0.85 | 0.77 | -0.13 | [-0.17, -0.10] | REAL |
| absolute | 1500 | ewma | 0.84 | 0.80 | 0.71 | -0.13 | [-0.17, -0.09] | REAL |
| absolute | 1500 | cusum | 0.87 | 0.82 | 0.71 | -0.16 | [-0.20, -0.13] | REAL |
| absolute | 2000 | fixed | 0.93 | 0.93 | 0.94 | +0.02 | [+0.00, +0.03] | none |
| absolute | 2000 | zscore | 0.94 | 0.91 | 0.83 | -0.11 | [-0.14, -0.08] | REAL |
| absolute | 2000 | ewma | 0.91 | 0.88 | 0.79 | -0.12 | [-0.15, -0.08] | REAL |
| absolute | 2000 | cusum | 0.92 | 0.89 | 0.78 | -0.14 | [-0.17, -0.11] | REAL |

## Scenario: drift_large

Users per tercile (low, mid, high): [100, 100, 100]. Tuned constants: fixed=1.44e+03, zscore=0.614, ewma=1.64, cusum=1.99.
Pooled alarm rate on the evaluation set (target 3.33): fixed=3.47, zscore=3.29, ewma=3.22, cusum=3.22.
Share of post-onset days at the 0 floor, by tercile (low, mid, high), standardised 2 SD: 0.064, 0.183, 0.421; absolute 2000: 0.015, 0.012, 0.022.

### Alarm episodes per 100 user-days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| none | 0 | fixed | 1.95 | 3.30 | 5.16 | +3.22 | [+2.67, +3.75] | REAL |
| none | 0 | zscore | 3.52 | 3.32 | 3.04 | -0.48 | [-0.68, -0.27] | none |
| none | 0 | ewma | 3.75 | 3.26 | 2.65 | -1.10 | [-1.38, -0.82] | REAL |
| none | 0 | cusum | 3.86 | 3.25 | 2.55 | -1.31 | [-1.58, -1.03] | REAL |

### Restricted mean delay (days, censored at 14)

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 9.36 | 7.06 | 5.05 | -4.31 | [-5.04, -3.60] | REAL |
| standardised | 0.5 | zscore | 6.57 | 6.53 | 6.54 | -0.03 | [-0.33, +0.29] | none |
| standardised | 0.5 | ewma | 7.45 | 7.25 | 7.37 | -0.08 | [-0.44, +0.23] | none |
| standardised | 0.5 | cusum | 6.97 | 6.98 | 7.15 | +0.18 | [-0.15, +0.49] | none |
| standardised | 1 | fixed | 6.69 | 4.67 | 3.25 | -3.43 | [-4.03, -2.77] | REAL |
| standardised | 1 | zscore | 4.30 | 4.25 | 4.23 | -0.07 | [-0.33, +0.16] | none |
| standardised | 1 | ewma | 5.01 | 4.60 | 4.51 | -0.50 | [-0.79, -0.20] | none |
| standardised | 1 | cusum | 4.21 | 3.83 | 3.78 | -0.43 | [-0.72, -0.16] | none |
| standardised | 1.5 | fixed | 4.69 | 3.29 | 2.34 | -2.36 | [-2.94, -1.87] | REAL |
| standardised | 1.5 | zscore | 2.88 | 2.90 | 3.02 | +0.14 | [-0.04, +0.32] | none |
| standardised | 1.5 | ewma | 3.28 | 2.92 | 2.94 | -0.34 | [-0.57, -0.11] | none |
| standardised | 1.5 | cusum | 2.39 | 2.08 | 2.16 | -0.23 | [-0.43, -0.02] | none |
| standardised | 2 | fixed | 3.48 | 2.41 | 1.85 | -1.62 | [-2.06, -1.23] | REAL |
| standardised | 2 | zscore | 2.08 | 2.15 | 2.42 | +0.34 | [+0.19, +0.50] | none |
| standardised | 2 | ewma | 2.18 | 1.98 | 2.20 | +0.02 | [-0.18, +0.22] | none |
| standardised | 2 | cusum | 1.38 | 1.29 | 1.56 | +0.18 | [+0.03, +0.36] | none |
| absolute | 500 | fixed | 10.47 | 8.69 | 6.99 | -3.48 | [-4.07, -2.87] | REAL |
| absolute | 500 | zscore | 7.71 | 8.40 | 9.12 | +1.41 | [+1.01, +1.80] | unclear |
| absolute | 500 | ewma | 8.47 | 9.20 | 10.18 | +1.71 | [+1.30, +2.11] | REAL |
| absolute | 500 | cusum | 8.14 | 9.11 | 10.18 | +2.04 | [+1.63, +2.46] | REAL |
| absolute | 1000 | fixed | 8.66 | 7.23 | 5.83 | -2.83 | [-3.29, -2.32] | REAL |
| absolute | 1000 | zscore | 5.99 | 6.87 | 8.00 | +2.01 | [+1.51, +2.46] | REAL |
| absolute | 1000 | ewma | 6.81 | 7.66 | 9.00 | +2.19 | [+1.70, +2.67] | REAL |
| absolute | 1000 | cusum | 6.34 | 7.39 | 8.72 | +2.38 | [+1.88, +2.88] | REAL |
| absolute | 1500 | fixed | 6.57 | 5.71 | 4.87 | -1.70 | [-2.03, -1.34] | REAL |
| absolute | 1500 | zscore | 4.69 | 5.61 | 6.90 | +2.21 | [+1.76, +2.68] | REAL |
| absolute | 1500 | ewma | 5.48 | 6.41 | 7.71 | +2.23 | [+1.67, +2.77] | REAL |
| absolute | 1500 | cusum | 4.81 | 5.92 | 7.48 | +2.67 | [+2.16, +3.21] | REAL |
| absolute | 2000 | fixed | 4.89 | 4.50 | 4.08 | -0.81 | [-1.08, -0.55] | none |
| absolute | 2000 | zscore | 3.72 | 4.63 | 5.99 | +2.27 | [+1.78, +2.74] | REAL |
| absolute | 2000 | ewma | 4.44 | 5.35 | 6.60 | +2.16 | [+1.63, +2.73] | REAL |
| absolute | 2000 | cusum | 3.69 | 4.73 | 6.34 | +2.65 | [+2.09, +3.24] | REAL |

### Detection within 14 days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 0.50 | 0.70 | 0.86 | +0.36 | [+0.30, +0.42] | REAL |
| standardised | 0.5 | zscore | 0.75 | 0.76 | 0.78 | +0.02 | [-0.00, +0.05] | none |
| standardised | 0.5 | ewma | 0.64 | 0.69 | 0.70 | +0.06 | [+0.03, +0.09] | none |
| standardised | 0.5 | cusum | 0.69 | 0.71 | 0.73 | +0.03 | [+0.00, +0.06] | none |
| standardised | 1 | fixed | 0.74 | 0.88 | 0.96 | +0.22 | [+0.17, +0.27] | REAL |
| standardised | 1 | zscore | 0.90 | 0.91 | 0.92 | +0.02 | [+0.00, +0.04] | none |
| standardised | 1 | ewma | 0.82 | 0.86 | 0.89 | +0.06 | [+0.04, +0.09] | none |
| standardised | 1 | cusum | 0.87 | 0.91 | 0.93 | +0.06 | [+0.04, +0.08] | none |
| standardised | 1.5 | fixed | 0.88 | 0.95 | 0.99 | +0.11 | [+0.07, +0.15] | REAL |
| standardised | 1.5 | zscore | 0.96 | 0.96 | 0.97 | +0.00 | [-0.01, +0.01] | none |
| standardised | 1.5 | ewma | 0.92 | 0.95 | 0.95 | +0.04 | [+0.02, +0.06] | none |
| standardised | 1.5 | cusum | 0.95 | 0.98 | 0.98 | +0.02 | [+0.01, +0.04] | none |
| standardised | 2 | fixed | 0.95 | 0.98 | 1.00 | +0.05 | [+0.03, +0.08] | none |
| standardised | 2 | zscore | 0.99 | 0.98 | 0.98 | -0.01 | [-0.02, -0.00] | none |
| standardised | 2 | ewma | 0.97 | 0.98 | 0.97 | +0.01 | [-0.00, +0.02] | none |
| standardised | 2 | cusum | 0.99 | 0.99 | 0.98 | -0.00 | [-0.01, +0.01] | none |
| absolute | 500 | fixed | 0.39 | 0.56 | 0.71 | +0.32 | [+0.26, +0.38] | REAL |
| absolute | 500 | zscore | 0.65 | 0.60 | 0.53 | -0.11 | [-0.15, -0.07] | REAL |
| absolute | 500 | ewma | 0.55 | 0.51 | 0.42 | -0.12 | [-0.16, -0.09] | REAL |
| absolute | 500 | cusum | 0.58 | 0.52 | 0.42 | -0.16 | [-0.19, -0.12] | REAL |
| absolute | 1000 | fixed | 0.59 | 0.71 | 0.82 | +0.23 | [+0.18, +0.27] | REAL |
| absolute | 1000 | zscore | 0.79 | 0.74 | 0.65 | -0.14 | [-0.18, -0.10] | REAL |
| absolute | 1000 | ewma | 0.68 | 0.64 | 0.55 | -0.13 | [-0.17, -0.10] | REAL |
| absolute | 1000 | cusum | 0.72 | 0.66 | 0.56 | -0.16 | [-0.20, -0.12] | REAL |
| absolute | 1500 | fixed | 0.79 | 0.83 | 0.89 | +0.11 | [+0.08, +0.13] | REAL |
| absolute | 1500 | zscore | 0.87 | 0.83 | 0.75 | -0.13 | [-0.16, -0.10] | REAL |
| absolute | 1500 | ewma | 0.78 | 0.74 | 0.66 | -0.13 | [-0.17, -0.09] | REAL |
| absolute | 1500 | cusum | 0.81 | 0.77 | 0.67 | -0.15 | [-0.18, -0.11] | REAL |
| absolute | 2000 | fixed | 0.91 | 0.92 | 0.94 | +0.03 | [+0.01, +0.05] | none |
| absolute | 2000 | zscore | 0.92 | 0.89 | 0.81 | -0.12 | [-0.15, -0.09] | REAL |
| absolute | 2000 | ewma | 0.84 | 0.81 | 0.75 | -0.09 | [-0.13, -0.06] | unclear |
| absolute | 2000 | cusum | 0.88 | 0.84 | 0.75 | -0.13 | [-0.17, -0.09] | REAL |

## Scenario: drift_log

Users per tercile (low, mid, high): [100, 100, 100]. Tuned constants: fixed=0.186, zscore=0.661, ewma=1.74, cusum=2.41.
Pooled alarm rate on the evaluation set (target 3.33): fixed=3.50, zscore=3.38, ewma=3.23, cusum=3.25.
Share of post-onset days at the 0 floor, by tercile (low, mid, high), standardised 2 SD: 0.058, 0.168, 0.416; absolute 2000: 0.013, 0.008, 0.018.

### Alarm episodes per 100 user-days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| none | 0 | fixed | 2.13 | 3.46 | 4.92 | +2.78 | [+2.49, +3.09] | REAL |
| none | 0 | zscore | 3.34 | 3.40 | 3.40 | +0.06 | [-0.16, +0.24] | none |
| none | 0 | ewma | 3.49 | 3.25 | 2.96 | -0.53 | [-0.76, -0.31] | none |
| none | 0 | cusum | 3.50 | 3.26 | 2.98 | -0.52 | [-0.75, -0.28] | none |

### Restricted mean delay (days, censored at 14)

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 8.18 | 5.98 | 4.24 | -3.94 | [-4.44, -3.47] | REAL |
| standardised | 0.5 | zscore | 6.32 | 5.99 | 5.34 | -0.97 | [-1.29, -0.65] | none |
| standardised | 0.5 | ewma | 6.98 | 6.51 | 5.78 | -1.20 | [-1.55, -0.88] | unclear |
| standardised | 0.5 | cusum | 6.74 | 6.18 | 5.42 | -1.32 | [-1.67, -0.99] | unclear |
| standardised | 1 | fixed | 5.12 | 3.45 | 2.24 | -2.88 | [-3.25, -2.52] | REAL |
| standardised | 1 | zscore | 3.89 | 3.42 | 2.72 | -1.17 | [-1.42, -0.90] | none |
| standardised | 1 | ewma | 4.26 | 3.52 | 2.85 | -1.41 | [-1.67, -1.14] | unclear |
| standardised | 1 | cusum | 3.79 | 3.05 | 2.40 | -1.39 | [-1.64, -1.13] | unclear |
| standardised | 1.5 | fixed | 3.24 | 2.04 | 1.24 | -1.99 | [-2.25, -1.74] | REAL |
| standardised | 1.5 | zscore | 2.40 | 2.03 | 1.48 | -0.92 | [-1.09, -0.75] | none |
| standardised | 1.5 | ewma | 2.44 | 1.90 | 1.35 | -1.09 | [-1.28, -0.91] | none |
| standardised | 1.5 | cusum | 1.96 | 1.54 | 1.07 | -0.88 | [-1.05, -0.72] | none |
| standardised | 2 | fixed | 2.11 | 1.26 | 0.76 | -1.35 | [-1.54, -1.17] | unclear |
| standardised | 2 | zscore | 1.52 | 1.23 | 0.86 | -0.66 | [-0.77, -0.55] | none |
| standardised | 2 | ewma | 1.43 | 1.10 | 0.75 | -0.68 | [-0.82, -0.56] | none |
| standardised | 2 | cusum | 1.04 | 0.79 | 0.56 | -0.47 | [-0.58, -0.37] | none |
| absolute | 500 | fixed | 9.41 | 7.96 | 6.73 | -2.68 | [-3.12, -2.23] | REAL |
| absolute | 500 | zscore | 7.55 | 8.10 | 8.54 | +0.98 | [+0.57, +1.40] | none |
| absolute | 500 | ewma | 8.25 | 8.78 | 9.40 | +1.15 | [+0.75, +1.56] | unclear |
| absolute | 500 | cusum | 8.10 | 8.69 | 9.23 | +1.12 | [+0.70, +1.54] | unclear |
| absolute | 1000 | fixed | 7.23 | 6.25 | 5.47 | -1.77 | [-2.26, -1.23] | REAL |
| absolute | 1000 | zscore | 5.57 | 6.39 | 7.06 | +1.50 | [+1.01, +1.92] | unclear |
| absolute | 1000 | ewma | 6.28 | 6.98 | 7.78 | +1.50 | [+1.02, +2.00] | unclear |
| absolute | 1000 | cusum | 6.02 | 6.75 | 7.54 | +1.52 | [+1.00, +2.02] | REAL |
| absolute | 1500 | fixed | 5.38 | 4.88 | 4.44 | -0.94 | [-1.42, -0.43] | none |
| absolute | 1500 | zscore | 4.15 | 5.03 | 5.84 | +1.69 | [+1.21, +2.15] | REAL |
| absolute | 1500 | ewma | 4.67 | 5.45 | 6.22 | +1.55 | [+1.02, +2.09] | REAL |
| absolute | 1500 | cusum | 4.31 | 5.14 | 5.96 | +1.65 | [+1.11, +2.20] | REAL |
| absolute | 2000 | fixed | 3.98 | 3.77 | 3.53 | -0.45 | [-0.90, +0.00] | none |
| absolute | 2000 | zscore | 3.18 | 3.94 | 4.70 | +1.52 | [+1.03, +1.96] | REAL |
| absolute | 2000 | ewma | 3.47 | 4.18 | 4.96 | +1.49 | [+0.99, +2.00] | unclear |
| absolute | 2000 | cusum | 3.17 | 3.74 | 4.70 | +1.53 | [+1.01, +2.06] | REAL |

### Detection within 14 days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 0.63 | 0.80 | 0.91 | +0.28 | [+0.25, +0.32] | REAL |
| standardised | 0.5 | zscore | 0.78 | 0.80 | 0.85 | +0.07 | [+0.05, +0.10] | none |
| standardised | 0.5 | ewma | 0.70 | 0.75 | 0.80 | +0.10 | [+0.07, +0.12] | REAL |
| standardised | 0.5 | cusum | 0.73 | 0.78 | 0.83 | +0.10 | [+0.07, +0.13] | REAL |
| standardised | 1 | fixed | 0.86 | 0.94 | 0.98 | +0.11 | [+0.09, +0.14] | REAL |
| standardised | 1 | zscore | 0.93 | 0.94 | 0.97 | +0.04 | [+0.03, +0.05] | none |
| standardised | 1 | ewma | 0.88 | 0.92 | 0.95 | +0.07 | [+0.05, +0.09] | none |
| standardised | 1 | cusum | 0.91 | 0.95 | 0.97 | +0.06 | [+0.04, +0.08] | none |
| standardised | 1.5 | fixed | 0.96 | 0.99 | 1.00 | +0.04 | [+0.03, +0.05] | none |
| standardised | 1.5 | zscore | 0.98 | 0.99 | 0.99 | +0.01 | [+0.00, +0.02] | none |
| standardised | 1.5 | ewma | 0.96 | 0.98 | 0.99 | +0.03 | [+0.02, +0.04] | none |
| standardised | 1.5 | cusum | 0.98 | 0.99 | 1.00 | +0.02 | [+0.01, +0.03] | none |
| standardised | 2 | fixed | 0.99 | 1.00 | 1.00 | +0.01 | [+0.00, +0.01] | none |
| standardised | 2 | zscore | 1.00 | 1.00 | 1.00 | +0.00 | [+0.00, +0.00] | none |
| standardised | 2 | ewma | 0.99 | 0.99 | 1.00 | +0.01 | [+0.00, +0.02] | none |
| standardised | 2 | cusum | 0.99 | 1.00 | 1.00 | +0.01 | [+0.00, +0.01] | none |
| absolute | 500 | fixed | 0.51 | 0.64 | 0.75 | +0.24 | [+0.19, +0.28] | REAL |
| absolute | 500 | zscore | 0.67 | 0.63 | 0.59 | -0.08 | [-0.11, -0.04] | unclear |
| absolute | 500 | ewma | 0.58 | 0.56 | 0.52 | -0.06 | [-0.10, -0.03] | none |
| absolute | 500 | cusum | 0.61 | 0.57 | 0.53 | -0.08 | [-0.11, -0.04] | unclear |
| absolute | 1000 | fixed | 0.71 | 0.79 | 0.85 | +0.13 | [+0.10, +0.17] | REAL |
| absolute | 1000 | zscore | 0.83 | 0.78 | 0.73 | -0.10 | [-0.13, -0.06] | REAL |
| absolute | 1000 | ewma | 0.75 | 0.71 | 0.66 | -0.08 | [-0.12, -0.04] | unclear |
| absolute | 1000 | cusum | 0.76 | 0.73 | 0.68 | -0.08 | [-0.12, -0.04] | unclear |
| absolute | 1500 | fixed | 0.85 | 0.88 | 0.91 | +0.06 | [+0.03, +0.09] | none |
| absolute | 1500 | zscore | 0.91 | 0.87 | 0.83 | -0.08 | [-0.11, -0.05] | unclear |
| absolute | 1500 | ewma | 0.85 | 0.82 | 0.78 | -0.07 | [-0.10, -0.04] | unclear |
| absolute | 1500 | cusum | 0.87 | 0.84 | 0.79 | -0.08 | [-0.11, -0.04] | unclear |
| absolute | 2000 | fixed | 0.92 | 0.93 | 0.95 | +0.03 | [+0.00, +0.05] | none |
| absolute | 2000 | zscore | 0.95 | 0.92 | 0.89 | -0.05 | [-0.08, -0.03] | none |
| absolute | 2000 | ewma | 0.91 | 0.89 | 0.86 | -0.05 | [-0.08, -0.03] | none |
| absolute | 2000 | cusum | 0.92 | 0.91 | 0.87 | -0.05 | [-0.08, -0.02] | none |
