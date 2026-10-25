# Pilot results (simulated users only)

Target pooled alarm rate 3.33 episodes per 100 user-days. Gap = high minus low variability tercile.
Margins: alarm rate 1.0, RMD 1.5 days, detection within 14 days 0.1.
Verdict: REAL = interval excludes 0 and gap beyond margin; none = interval inside the margin; unclear otherwise.

## Scenario: ideal

Users per tercile (low, mid, high): [100, 100, 100]. Tuned constants: fixed=1.26e+03, zscore=0.547, ewma=1.21, cusum=1.37.
Pooled alarm rate on the evaluation set (target 3.33): fixed=3.35, zscore=3.26, ewma=3.24, cusum=3.26.
Share of post-onset days at the 0 floor, by tercile (low, mid, high), standardised 2 SD: 0.010, 0.122, 0.421; absolute 2000: 0.003, 0.004, 0.021.

### Alarm episodes per 100 user-days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| none | 0 | fixed | 1.62 | 3.17 | 5.26 | +3.64 | [+3.09, +4.14] | REAL |
| none | 0 | zscore | 3.36 | 3.30 | 3.12 | -0.23 | [-0.34, -0.13] | none |
| none | 0 | ewma | 3.40 | 3.31 | 3.00 | -0.40 | [-0.57, -0.25] | none |
| none | 0 | cusum | 3.80 | 3.34 | 2.63 | -1.16 | [-1.35, -1.00] | REAL |

### Restricted mean delay (days, censored at 14)

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 9.36 | 6.77 | 4.63 | -4.73 | [-5.47, -4.01] | REAL |
| standardised | 0.5 | zscore | 5.79 | 5.67 | 5.93 | +0.14 | [-0.15, +0.40] | none |
| standardised | 0.5 | ewma | 5.40 | 5.22 | 5.32 | -0.08 | [-0.35, +0.17] | none |
| standardised | 0.5 | cusum | 4.71 | 4.58 | 4.76 | +0.05 | [-0.22, +0.29] | none |
| standardised | 1 | fixed | 6.54 | 4.18 | 2.82 | -3.72 | [-4.44, -3.02] | REAL |
| standardised | 1 | zscore | 3.25 | 3.17 | 3.31 | +0.06 | [-0.12, +0.21] | none |
| standardised | 1 | ewma | 2.65 | 2.50 | 2.57 | -0.08 | [-0.24, +0.07] | none |
| standardised | 1 | cusum | 1.86 | 1.80 | 1.91 | +0.05 | [-0.08, +0.17] | none |
| standardised | 1.5 | fixed | 4.31 | 2.67 | 1.91 | -2.40 | [-2.91, -1.85] | REAL |
| standardised | 1.5 | zscore | 2.14 | 2.09 | 2.29 | +0.16 | [+0.03, +0.29] | none |
| standardised | 1.5 | ewma | 1.48 | 1.45 | 1.53 | +0.05 | [-0.05, +0.15] | none |
| standardised | 1.5 | cusum | 0.89 | 0.85 | 0.97 | +0.08 | [-0.00, +0.16] | none |
| standardised | 2 | fixed | 3.14 | 1.92 | 1.47 | -1.67 | [-2.14, -1.25] | REAL |
| standardised | 2 | zscore | 1.59 | 1.56 | 1.80 | +0.21 | [+0.10, +0.31] | none |
| standardised | 2 | ewma | 0.94 | 0.93 | 1.08 | +0.14 | [+0.06, +0.22] | none |
| standardised | 2 | cusum | 0.46 | 0.46 | 0.57 | +0.10 | [+0.03, +0.18] | none |
| absolute | 500 | fixed | 10.60 | 8.50 | 6.62 | -3.98 | [-4.67, -3.31] | REAL |
| absolute | 500 | zscore | 6.95 | 7.64 | 8.94 | +1.98 | [+1.57, +2.38] | REAL |
| absolute | 500 | ewma | 6.65 | 7.60 | 8.77 | +2.12 | [+1.65, +2.57] | REAL |
| absolute | 500 | cusum | 6.09 | 7.21 | 9.10 | +3.01 | [+2.56, +3.48] | REAL |
| absolute | 1000 | fixed | 8.20 | 6.63 | 5.38 | -2.81 | [-3.32, -2.25] | REAL |
| absolute | 1000 | zscore | 4.73 | 5.83 | 7.37 | +2.64 | [+2.14, +3.10] | REAL |
| absolute | 1000 | ewma | 4.14 | 5.37 | 7.03 | +2.89 | [+2.43, +3.41] | REAL |
| absolute | 1000 | cusum | 3.56 | 4.93 | 6.94 | +3.38 | [+2.83, +3.92] | REAL |
| absolute | 1500 | fixed | 5.39 | 4.85 | 4.25 | -1.14 | [-1.41, -0.85] | none |
| absolute | 1500 | zscore | 3.39 | 4.45 | 6.08 | +2.69 | [+2.24, +3.15] | REAL |
| absolute | 1500 | ewma | 2.76 | 3.83 | 5.49 | +2.74 | [+2.24, +3.22] | REAL |
| absolute | 1500 | cusum | 2.14 | 3.30 | 5.13 | +2.99 | [+2.50, +3.49] | REAL |
| absolute | 2000 | fixed | 3.89 | 3.64 | 3.43 | -0.46 | [-0.65, -0.25] | none |
| absolute | 2000 | zscore | 2.55 | 3.46 | 5.05 | +2.51 | [+2.08, +2.95] | REAL |
| absolute | 2000 | ewma | 1.92 | 2.85 | 4.37 | +2.44 | [+1.96, +2.91] | REAL |
| absolute | 2000 | cusum | 1.34 | 2.28 | 3.91 | +2.57 | [+2.13, +3.00] | REAL |

### Detection within 14 days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 0.53 | 0.75 | 0.89 | +0.36 | [+0.29, +0.43] | REAL |
| standardised | 0.5 | zscore | 0.88 | 0.88 | 0.86 | -0.02 | [-0.04, +0.00] | none |
| standardised | 0.5 | ewma | 0.88 | 0.89 | 0.88 | +0.00 | [-0.02, +0.02] | none |
| standardised | 0.5 | cusum | 0.92 | 0.92 | 0.91 | -0.01 | [-0.02, +0.01] | none |
| standardised | 1 | fixed | 0.77 | 0.92 | 0.98 | +0.20 | [+0.15, +0.26] | REAL |
| standardised | 1 | zscore | 0.99 | 0.99 | 0.98 | -0.00 | [-0.01, +0.01] | none |
| standardised | 1 | ewma | 0.99 | 0.99 | 0.99 | -0.01 | [-0.01, -0.00] | none |
| standardised | 1 | cusum | 1.00 | 1.00 | 1.00 | -0.00 | [-0.00, +0.00] | none |
| standardised | 1.5 | fixed | 0.92 | 0.98 | 0.99 | +0.08 | [+0.04, +0.12] | unclear |
| standardised | 1.5 | zscore | 1.00 | 1.00 | 1.00 | -0.00 | [-0.01, +0.00] | none |
| standardised | 1.5 | ewma | 1.00 | 1.00 | 1.00 | -0.00 | [-0.00, +0.00] | none |
| standardised | 1.5 | cusum | 1.00 | 1.00 | 1.00 | +0.00 | [+0.00, +0.00] | none |
| standardised | 2 | fixed | 0.96 | 1.00 | 1.00 | +0.04 | [+0.01, +0.06] | none |
| standardised | 2 | zscore | 1.00 | 1.00 | 1.00 | +0.00 | [-0.00, +0.00] | none |
| standardised | 2 | ewma | 1.00 | 1.00 | 1.00 | -0.00 | [-0.00, +0.00] | none |
| standardised | 2 | cusum | 1.00 | 1.00 | 1.00 | +0.00 | [+0.00, +0.00] | none |
| absolute | 500 | fixed | 0.41 | 0.60 | 0.75 | +0.33 | [+0.27, +0.40] | REAL |
| absolute | 500 | zscore | 0.78 | 0.70 | 0.58 | -0.20 | [-0.23, -0.16] | REAL |
| absolute | 500 | ewma | 0.78 | 0.71 | 0.60 | -0.18 | [-0.22, -0.14] | REAL |
| absolute | 500 | cusum | 0.81 | 0.71 | 0.56 | -0.26 | [-0.29, -0.21] | REAL |
| absolute | 1000 | fixed | 0.68 | 0.79 | 0.86 | +0.18 | [+0.13, +0.22] | REAL |
| absolute | 1000 | zscore | 0.92 | 0.85 | 0.74 | -0.18 | [-0.22, -0.15] | REAL |
| absolute | 1000 | ewma | 0.93 | 0.86 | 0.75 | -0.18 | [-0.21, -0.14] | REAL |
| absolute | 1000 | cusum | 0.94 | 0.87 | 0.75 | -0.19 | [-0.23, -0.16] | REAL |
| absolute | 1500 | fixed | 0.93 | 0.94 | 0.94 | +0.01 | [-0.00, +0.03] | none |
| absolute | 1500 | zscore | 0.97 | 0.94 | 0.84 | -0.13 | [-0.15, -0.10] | REAL |
| absolute | 1500 | ewma | 0.98 | 0.95 | 0.86 | -0.12 | [-0.14, -0.09] | REAL |
| absolute | 1500 | cusum | 0.98 | 0.95 | 0.86 | -0.12 | [-0.15, -0.10] | REAL |
| absolute | 2000 | fixed | 0.98 | 0.99 | 0.97 | -0.01 | [-0.02, -0.00] | none |
| absolute | 2000 | zscore | 0.99 | 0.97 | 0.90 | -0.09 | [-0.11, -0.07] | unclear |
| absolute | 2000 | ewma | 0.99 | 0.97 | 0.91 | -0.08 | [-0.10, -0.06] | unclear |
| absolute | 2000 | cusum | 1.00 | 0.98 | 0.92 | -0.08 | [-0.10, -0.06] | unclear |

## Scenario: realistic

Users per tercile (low, mid, high): [100, 100, 100]. Tuned constants: fixed=1.45e+03, zscore=0.584, ewma=1.29, cusum=1.53.
Pooled alarm rate on the evaluation set (target 3.33): fixed=3.46, zscore=3.33, ewma=3.26, cusum=3.23.
Share of post-onset days at the 0 floor, by tercile (low, mid, high), standardised 2 SD: 0.049, 0.158, 0.402; absolute 2000: 0.011, 0.006, 0.015.

### Alarm episodes per 100 user-days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| none | 0 | fixed | 1.87 | 3.32 | 5.20 | +3.33 | [+2.81, +3.91] | REAL |
| none | 0 | zscore | 3.42 | 3.35 | 3.22 | -0.21 | [-0.41, +0.00] | none |
| none | 0 | ewma | 3.45 | 3.35 | 2.98 | -0.47 | [-0.65, -0.29] | none |
| none | 0 | cusum | 3.68 | 3.33 | 2.68 | -0.99 | [-1.22, -0.79] | unclear |

### Restricted mean delay (days, censored at 14)

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 9.42 | 6.96 | 5.12 | -4.30 | [-5.04, -3.57] | REAL |
| standardised | 0.5 | zscore | 6.08 | 6.14 | 6.21 | +0.13 | [-0.17, +0.41] | none |
| standardised | 0.5 | ewma | 5.76 | 5.64 | 5.96 | +0.21 | [-0.07, +0.49] | none |
| standardised | 0.5 | cusum | 5.42 | 5.35 | 5.81 | +0.39 | [+0.08, +0.70] | none |
| standardised | 1 | fixed | 6.69 | 4.54 | 3.31 | -3.37 | [-3.96, -2.70] | REAL |
| standardised | 1 | zscore | 3.60 | 3.65 | 3.94 | +0.34 | [+0.12, +0.55] | none |
| standardised | 1 | ewma | 2.98 | 3.03 | 3.29 | +0.31 | [+0.06, +0.53] | none |
| standardised | 1 | cusum | 2.40 | 2.44 | 2.71 | +0.31 | [+0.12, +0.51] | none |
| standardised | 1.5 | fixed | 4.70 | 3.09 | 2.28 | -2.42 | [-2.99, -1.91] | REAL |
| standardised | 1.5 | zscore | 2.43 | 2.54 | 2.81 | +0.38 | [+0.22, +0.54] | none |
| standardised | 1.5 | ewma | 1.75 | 1.78 | 2.12 | +0.37 | [+0.20, +0.54] | none |
| standardised | 1.5 | cusum | 1.24 | 1.26 | 1.54 | +0.30 | [+0.16, +0.45] | none |
| standardised | 2 | fixed | 3.37 | 2.27 | 1.79 | -1.58 | [-2.02, -1.20] | REAL |
| standardised | 2 | zscore | 1.75 | 1.88 | 2.25 | +0.50 | [+0.36, +0.64] | none |
| standardised | 2 | ewma | 1.16 | 1.21 | 1.54 | +0.38 | [+0.24, +0.53] | none |
| standardised | 2 | cusum | 0.69 | 0.70 | 1.06 | +0.37 | [+0.24, +0.52] | none |
| absolute | 500 | fixed | 10.57 | 8.78 | 6.85 | -3.72 | [-4.39, -3.06] | REAL |
| absolute | 500 | zscore | 7.30 | 8.06 | 8.78 | +1.48 | [+1.08, +1.88] | unclear |
| absolute | 500 | ewma | 7.07 | 8.07 | 9.18 | +2.12 | [+1.70, +2.54] | REAL |
| absolute | 500 | cusum | 6.96 | 8.00 | 9.38 | +2.43 | [+2.00, +2.89] | REAL |
| absolute | 1000 | fixed | 8.72 | 7.20 | 5.86 | -2.86 | [-3.39, -2.33] | REAL |
| absolute | 1000 | zscore | 5.32 | 6.43 | 7.59 | +2.27 | [+1.83, +2.73] | REAL |
| absolute | 1000 | ewma | 4.80 | 6.14 | 7.64 | +2.84 | [+2.33, +3.30] | REAL |
| absolute | 1000 | cusum | 4.58 | 6.03 | 7.79 | +3.20 | [+2.63, +3.70] | REAL |
| absolute | 1500 | fixed | 6.39 | 5.62 | 4.90 | -1.49 | [-1.86, -1.13] | unclear |
| absolute | 1500 | zscore | 3.95 | 5.13 | 6.54 | +2.59 | [+2.12, +3.07] | REAL |
| absolute | 1500 | ewma | 3.37 | 4.58 | 6.24 | +2.87 | [+2.41, +3.39] | REAL |
| absolute | 1500 | cusum | 3.10 | 4.36 | 6.31 | +3.21 | [+2.67, +3.77] | REAL |
| absolute | 2000 | fixed | 4.57 | 4.30 | 4.00 | -0.58 | [-0.79, -0.36] | none |
| absolute | 2000 | zscore | 3.06 | 4.14 | 5.61 | +2.55 | [+2.11, +2.94] | REAL |
| absolute | 2000 | ewma | 2.48 | 3.46 | 5.11 | +2.62 | [+2.14, +3.08] | REAL |
| absolute | 2000 | cusum | 2.15 | 3.27 | 5.09 | +2.94 | [+2.38, +3.48] | REAL |

### Detection within 14 days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 0.49 | 0.71 | 0.85 | +0.35 | [+0.29, +0.42] | REAL |
| standardised | 0.5 | zscore | 0.82 | 0.80 | 0.80 | -0.01 | [-0.04, +0.01] | none |
| standardised | 0.5 | ewma | 0.84 | 0.85 | 0.83 | -0.01 | [-0.04, +0.01] | none |
| standardised | 0.5 | cusum | 0.87 | 0.88 | 0.84 | -0.02 | [-0.04, +0.00] | none |
| standardised | 1 | fixed | 0.74 | 0.89 | 0.95 | +0.22 | [+0.16, +0.27] | REAL |
| standardised | 1 | zscore | 0.96 | 0.96 | 0.94 | -0.02 | [-0.04, -0.01] | none |
| standardised | 1 | ewma | 0.97 | 0.97 | 0.95 | -0.02 | [-0.03, -0.01] | none |
| standardised | 1 | cusum | 0.99 | 0.99 | 0.97 | -0.02 | [-0.03, -0.01] | none |
| standardised | 1.5 | fixed | 0.88 | 0.96 | 0.99 | +0.11 | [+0.07, +0.15] | REAL |
| standardised | 1.5 | zscore | 0.99 | 0.99 | 0.98 | -0.01 | [-0.02, -0.01] | none |
| standardised | 1.5 | ewma | 1.00 | 0.99 | 0.98 | -0.01 | [-0.02, -0.01] | none |
| standardised | 1.5 | cusum | 1.00 | 0.99 | 0.99 | -0.01 | [-0.02, -0.01] | none |
| standardised | 2 | fixed | 0.95 | 0.99 | 1.00 | +0.04 | [+0.02, +0.07] | none |
| standardised | 2 | zscore | 1.00 | 0.99 | 0.99 | -0.01 | [-0.02, -0.01] | none |
| standardised | 2 | ewma | 1.00 | 1.00 | 0.99 | -0.01 | [-0.01, -0.00] | none |
| standardised | 2 | cusum | 1.00 | 1.00 | 0.99 | -0.01 | [-0.02, -0.01] | none |
| absolute | 500 | fixed | 0.38 | 0.55 | 0.72 | +0.34 | [+0.28, +0.39] | REAL |
| absolute | 500 | zscore | 0.71 | 0.63 | 0.58 | -0.13 | [-0.17, -0.10] | REAL |
| absolute | 500 | ewma | 0.74 | 0.65 | 0.56 | -0.19 | [-0.22, -0.15] | REAL |
| absolute | 500 | cusum | 0.73 | 0.64 | 0.53 | -0.21 | [-0.25, -0.17] | REAL |
| absolute | 1000 | fixed | 0.59 | 0.71 | 0.81 | +0.22 | [+0.17, +0.26] | REAL |
| absolute | 1000 | zscore | 0.87 | 0.78 | 0.69 | -0.17 | [-0.21, -0.14] | REAL |
| absolute | 1000 | ewma | 0.89 | 0.81 | 0.70 | -0.19 | [-0.22, -0.15] | REAL |
| absolute | 1000 | cusum | 0.88 | 0.80 | 0.66 | -0.22 | [-0.26, -0.19] | REAL |
| absolute | 1500 | fixed | 0.82 | 0.85 | 0.89 | +0.07 | [+0.05, +0.10] | none |
| absolute | 1500 | zscore | 0.94 | 0.87 | 0.77 | -0.16 | [-0.19, -0.13] | REAL |
| absolute | 1500 | ewma | 0.95 | 0.91 | 0.81 | -0.14 | [-0.17, -0.11] | REAL |
| absolute | 1500 | cusum | 0.94 | 0.90 | 0.77 | -0.18 | [-0.21, -0.14] | REAL |
| absolute | 2000 | fixed | 0.95 | 0.95 | 0.95 | -0.00 | [-0.01, +0.01] | none |
| absolute | 2000 | zscore | 0.97 | 0.93 | 0.85 | -0.12 | [-0.14, -0.09] | REAL |
| absolute | 2000 | ewma | 0.98 | 0.96 | 0.87 | -0.11 | [-0.14, -0.08] | REAL |
| absolute | 2000 | cusum | 0.97 | 0.94 | 0.84 | -0.13 | [-0.15, -0.10] | REAL |

## Scenario: realistic_log

Users per tercile (low, mid, high): [100, 100, 100]. Tuned constants: fixed=0.18, zscore=0.643, ewma=1.45, cusum=2.01.
Pooled alarm rate on the evaluation set (target 3.33): fixed=3.52, zscore=3.37, ewma=3.25, cusum=3.26.
Share of post-onset days at the 0 floor, by tercile (low, mid, high), standardised 2 SD: 0.049, 0.158, 0.402; absolute 2000: 0.011, 0.006, 0.015.

### Alarm episodes per 100 user-days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| none | 0 | fixed | 2.06 | 3.47 | 5.02 | +2.96 | [+2.67, +3.24] | REAL |
| none | 0 | zscore | 3.32 | 3.35 | 3.45 | +0.13 | [-0.05, +0.32] | none |
| none | 0 | ewma | 3.27 | 3.29 | 3.17 | -0.10 | [-0.27, +0.07] | none |
| none | 0 | cusum | 3.30 | 3.29 | 3.19 | -0.11 | [-0.30, +0.08] | none |

### Restricted mean delay (days, censored at 14)

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 7.99 | 5.80 | 4.10 | -3.90 | [-4.45, -3.39] | REAL |
| standardised | 0.5 | zscore | 6.10 | 5.75 | 5.17 | -0.93 | [-1.26, -0.61] | none |
| standardised | 0.5 | ewma | 5.83 | 5.50 | 5.10 | -0.73 | [-1.06, -0.40] | none |
| standardised | 0.5 | cusum | 5.79 | 5.27 | 4.85 | -0.94 | [-1.30, -0.59] | none |
| standardised | 1 | fixed | 4.80 | 3.18 | 2.16 | -2.64 | [-3.03, -2.26] | REAL |
| standardised | 1 | zscore | 3.43 | 3.17 | 2.63 | -0.80 | [-1.01, -0.60] | none |
| standardised | 1 | ewma | 2.94 | 2.68 | 2.32 | -0.61 | [-0.84, -0.40] | none |
| standardised | 1 | cusum | 2.62 | 2.39 | 2.02 | -0.60 | [-0.81, -0.39] | none |
| standardised | 1.5 | fixed | 2.87 | 1.89 | 1.18 | -1.68 | [-1.95, -1.44] | REAL |
| standardised | 1.5 | zscore | 2.08 | 1.85 | 1.42 | -0.66 | [-0.80, -0.50] | none |
| standardised | 1.5 | ewma | 1.57 | 1.38 | 1.16 | -0.41 | [-0.55, -0.27] | none |
| standardised | 1.5 | cusum | 1.28 | 1.09 | 0.92 | -0.36 | [-0.47, -0.23] | none |
| standardised | 2 | fixed | 1.91 | 1.17 | 0.69 | -1.22 | [-1.41, -1.03] | none |
| standardised | 2 | zscore | 1.35 | 1.15 | 0.80 | -0.56 | [-0.66, -0.45] | none |
| standardised | 2 | ewma | 0.93 | 0.77 | 0.60 | -0.32 | [-0.42, -0.24] | none |
| standardised | 2 | cusum | 0.68 | 0.55 | 0.44 | -0.25 | [-0.31, -0.18] | none |
| absolute | 500 | fixed | 9.23 | 7.86 | 6.55 | -2.68 | [-3.21, -2.14] | REAL |
| absolute | 500 | zscore | 7.38 | 7.92 | 8.25 | +0.87 | [+0.49, +1.27] | none |
| absolute | 500 | ewma | 7.24 | 8.04 | 8.69 | +1.45 | [+1.06, +1.86] | unclear |
| absolute | 500 | cusum | 7.28 | 7.95 | 8.69 | +1.41 | [+0.97, +1.84] | unclear |
| absolute | 1000 | fixed | 6.84 | 6.11 | 5.23 | -1.61 | [-2.09, -1.12] | REAL |
| absolute | 1000 | zscore | 5.25 | 6.15 | 6.80 | +1.55 | [+1.13, +1.99] | REAL |
| absolute | 1000 | ewma | 4.82 | 5.92 | 6.93 | +2.11 | [+1.55, +2.59] | REAL |
| absolute | 1000 | cusum | 4.86 | 5.86 | 6.86 | +2.00 | [+1.46, +2.48] | REAL |
| absolute | 1500 | fixed | 4.82 | 4.57 | 4.19 | -0.63 | [-1.12, -0.18] | none |
| absolute | 1500 | zscore | 3.70 | 4.67 | 5.53 | +1.83 | [+1.38, +2.28] | REAL |
| absolute | 1500 | ewma | 3.30 | 4.34 | 5.37 | +2.07 | [+1.58, +2.60] | REAL |
| absolute | 1500 | cusum | 3.14 | 4.14 | 5.27 | +2.13 | [+1.65, +2.61] | REAL |
| absolute | 2000 | fixed | 3.55 | 3.50 | 3.34 | -0.21 | [-0.62, +0.25] | none |
| absolute | 2000 | zscore | 2.79 | 3.65 | 4.48 | +1.69 | [+1.25, +2.09] | REAL |
| absolute | 2000 | ewma | 2.30 | 3.11 | 4.18 | +1.88 | [+1.45, +2.30] | REAL |
| absolute | 2000 | cusum | 2.16 | 2.99 | 3.96 | +1.80 | [+1.30, +2.30] | REAL |

### Detection within 14 days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 0.66 | 0.82 | 0.92 | +0.27 | [+0.23, +0.31] | REAL |
| standardised | 0.5 | zscore | 0.81 | 0.83 | 0.86 | +0.05 | [+0.03, +0.07] | none |
| standardised | 0.5 | ewma | 0.83 | 0.85 | 0.87 | +0.04 | [+0.01, +0.06] | none |
| standardised | 0.5 | cusum | 0.83 | 0.86 | 0.87 | +0.04 | [+0.02, +0.07] | none |
| standardised | 1 | fixed | 0.90 | 0.97 | 0.99 | +0.09 | [+0.07, +0.11] | unclear |
| standardised | 1 | zscore | 0.97 | 0.96 | 0.98 | +0.01 | [+0.00, +0.02] | none |
| standardised | 1 | ewma | 0.97 | 0.98 | 0.98 | +0.00 | [-0.01, +0.01] | none |
| standardised | 1 | cusum | 0.98 | 0.98 | 0.98 | +0.00 | [-0.01, +0.01] | none |
| standardised | 1.5 | fixed | 0.98 | 1.00 | 1.00 | +0.02 | [+0.01, +0.03] | none |
| standardised | 1.5 | zscore | 1.00 | 1.00 | 1.00 | +0.00 | [-0.00, +0.01] | none |
| standardised | 1.5 | ewma | 1.00 | 1.00 | 1.00 | -0.00 | [-0.00, +0.00] | none |
| standardised | 1.5 | cusum | 1.00 | 1.00 | 1.00 | -0.00 | [-0.00, +0.00] | none |
| standardised | 2 | fixed | 1.00 | 1.00 | 1.00 | +0.00 | [+0.00, +0.01] | none |
| standardised | 2 | zscore | 1.00 | 1.00 | 1.00 | -0.00 | [-0.00, +0.00] | none |
| standardised | 2 | ewma | 1.00 | 1.00 | 1.00 | -0.00 | [-0.00, +0.00] | none |
| standardised | 2 | cusum | 1.00 | 1.00 | 1.00 | -0.00 | [-0.00, +0.00] | none |
| absolute | 500 | fixed | 0.54 | 0.66 | 0.76 | +0.22 | [+0.18, +0.26] | REAL |
| absolute | 500 | zscore | 0.70 | 0.65 | 0.63 | -0.08 | [-0.11, -0.04] | unclear |
| absolute | 500 | ewma | 0.72 | 0.65 | 0.60 | -0.13 | [-0.16, -0.09] | REAL |
| absolute | 500 | cusum | 0.71 | 0.65 | 0.60 | -0.11 | [-0.15, -0.08] | REAL |
| absolute | 1000 | fixed | 0.76 | 0.81 | 0.87 | +0.11 | [+0.07, +0.15] | REAL |
| absolute | 1000 | zscore | 0.87 | 0.80 | 0.76 | -0.11 | [-0.15, -0.08] | REAL |
| absolute | 1000 | ewma | 0.89 | 0.82 | 0.76 | -0.13 | [-0.17, -0.10] | REAL |
| absolute | 1000 | cusum | 0.87 | 0.80 | 0.75 | -0.12 | [-0.16, -0.09] | REAL |
| absolute | 1500 | fixed | 0.90 | 0.91 | 0.93 | +0.03 | [-0.00, +0.06] | none |
| absolute | 1500 | zscore | 0.94 | 0.90 | 0.85 | -0.09 | [-0.12, -0.07] | unclear |
| absolute | 1500 | ewma | 0.95 | 0.92 | 0.85 | -0.10 | [-0.13, -0.07] | unclear |
| absolute | 1500 | cusum | 0.95 | 0.91 | 0.86 | -0.09 | [-0.11, -0.06] | unclear |
| absolute | 2000 | fixed | 0.95 | 0.96 | 0.96 | +0.01 | [-0.01, +0.03] | none |
| absolute | 2000 | zscore | 0.97 | 0.95 | 0.91 | -0.05 | [-0.08, -0.03] | none |
| absolute | 2000 | ewma | 0.98 | 0.96 | 0.92 | -0.06 | [-0.08, -0.04] | none |
| absolute | 2000 | cusum | 0.97 | 0.96 | 0.92 | -0.05 | [-0.07, -0.03] | none |

## Scenario: symmetric

Users per tercile (low, mid, high): [100, 100, 100]. Tuned constants: fixed=1.31e+03, zscore=0.651, ewma=1.46, cusum=2.03.
Pooled alarm rate on the evaluation set (target 3.33): fixed=3.31, zscore=3.27, ewma=3.29, cusum=3.29.
Share of post-onset days at the 0 floor, by tercile (low, mid, high), standardised 2 SD: 0.039, 0.135, 0.212; absolute 2000: 0.014, 0.024, 0.039.

### Alarm episodes per 100 user-days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| none | 0 | fixed | 2.08 | 3.70 | 4.14 | +2.06 | [+1.57, +2.52] | REAL |
| none | 0 | zscore | 3.13 | 3.29 | 3.40 | +0.27 | [+0.08, +0.46] | none |
| none | 0 | ewma | 3.33 | 3.22 | 3.33 | -0.00 | [-0.19, +0.18] | none |
| none | 0 | cusum | 3.35 | 3.21 | 3.32 | -0.03 | [-0.21, +0.16] | none |

### Restricted mean delay (days, censored at 14)

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 8.93 | 6.79 | 6.17 | -2.76 | [-3.51, -2.00] | REAL |
| standardised | 0.5 | zscore | 6.83 | 6.86 | 6.70 | -0.12 | [-0.46, +0.18] | none |
| standardised | 0.5 | ewma | 6.45 | 6.69 | 6.56 | +0.11 | [-0.19, +0.42] | none |
| standardised | 0.5 | cusum | 6.95 | 6.98 | 6.87 | -0.08 | [-0.40, +0.22] | none |
| standardised | 1 | fixed | 6.22 | 4.28 | 3.97 | -2.25 | [-2.99, -1.47] | REAL |
| standardised | 1 | zscore | 4.03 | 4.24 | 4.14 | +0.11 | [-0.12, +0.32] | none |
| standardised | 1 | ewma | 3.48 | 3.67 | 3.59 | +0.11 | [-0.09, +0.33] | none |
| standardised | 1 | cusum | 3.49 | 3.63 | 3.64 | +0.15 | [-0.09, +0.39] | none |
| standardised | 1.5 | fixed | 4.19 | 2.86 | 2.70 | -1.49 | [-2.08, -0.94] | unclear |
| standardised | 1.5 | zscore | 2.67 | 2.80 | 2.73 | +0.05 | [-0.11, +0.21] | none |
| standardised | 1.5 | ewma | 1.92 | 2.15 | 2.07 | +0.15 | [+0.02, +0.28] | none |
| standardised | 1.5 | cusum | 1.79 | 1.92 | 1.92 | +0.13 | [-0.02, +0.26] | none |
| standardised | 2 | fixed | 3.06 | 2.06 | 2.01 | -1.05 | [-1.54, -0.62] | unclear |
| standardised | 2 | zscore | 1.91 | 2.04 | 2.02 | +0.10 | [-0.02, +0.22] | none |
| standardised | 2 | ewma | 1.22 | 1.34 | 1.32 | +0.10 | [+0.02, +0.20] | none |
| standardised | 2 | cusum | 0.99 | 1.07 | 1.06 | +0.08 | [+0.01, +0.15] | none |
| absolute | 500 | fixed | 10.09 | 8.29 | 7.69 | -2.40 | [-3.05, -1.80] | REAL |
| absolute | 500 | zscore | 7.88 | 8.54 | 8.35 | +0.47 | [+0.06, +0.88] | none |
| absolute | 500 | ewma | 7.86 | 8.76 | 8.71 | +0.86 | [+0.49, +1.22] | none |
| absolute | 500 | cusum | 8.20 | 8.87 | 8.81 | +0.61 | [+0.22, +1.04] | none |
| absolute | 1000 | fixed | 8.10 | 6.86 | 6.45 | -1.65 | [-2.18, -1.09] | REAL |
| absolute | 1000 | zscore | 5.78 | 7.09 | 7.06 | +1.28 | [+0.85, +1.74] | unclear |
| absolute | 1000 | ewma | 5.46 | 6.88 | 7.05 | +1.59 | [+1.13, +2.07] | REAL |
| absolute | 1000 | cusum | 5.76 | 7.24 | 7.28 | +1.52 | [+1.05, +2.03] | REAL |
| absolute | 1500 | fixed | 5.82 | 5.39 | 5.08 | -0.74 | [-1.06, -0.41] | none |
| absolute | 1500 | zscore | 4.27 | 5.75 | 5.80 | +1.53 | [+1.10, +1.96] | REAL |
| absolute | 1500 | ewma | 3.74 | 5.36 | 5.55 | +1.81 | [+1.38, +2.27] | REAL |
| absolute | 1500 | cusum | 3.91 | 5.59 | 5.82 | +1.92 | [+1.41, +2.39] | REAL |
| absolute | 2000 | fixed | 4.12 | 4.19 | 4.01 | -0.11 | [-0.32, +0.12] | none |
| absolute | 2000 | zscore | 3.25 | 4.67 | 4.86 | +1.61 | [+1.22, +2.01] | REAL |
| absolute | 2000 | ewma | 2.66 | 4.15 | 4.44 | +1.78 | [+1.36, +2.20] | REAL |
| absolute | 2000 | cusum | 2.72 | 4.29 | 4.60 | +1.87 | [+1.44, +2.32] | REAL |

### Detection within 14 days

| convention | effect | detector | low | mid | high | gap (high-low) | 95% interval | verdict |
|---|---|---|---|---|---|---|---|---|
| standardised | 0.5 | fixed | 0.55 | 0.74 | 0.78 | +0.24 | [+0.16, +0.31] | REAL |
| standardised | 0.5 | zscore | 0.76 | 0.77 | 0.78 | +0.02 | [-0.01, +0.04] | none |
| standardised | 0.5 | ewma | 0.80 | 0.79 | 0.80 | -0.00 | [-0.03, +0.02] | none |
| standardised | 0.5 | cusum | 0.76 | 0.76 | 0.77 | +0.00 | [-0.02, +0.03] | none |
| standardised | 1 | fixed | 0.79 | 0.93 | 0.92 | +0.13 | [+0.08, +0.19] | REAL |
| standardised | 1 | zscore | 0.95 | 0.94 | 0.95 | -0.00 | [-0.02, +0.01] | none |
| standardised | 1 | ewma | 0.97 | 0.96 | 0.96 | -0.01 | [-0.02, -0.00] | none |
| standardised | 1 | cusum | 0.97 | 0.96 | 0.96 | -0.01 | [-0.02, +0.00] | none |
| standardised | 1.5 | fixed | 0.91 | 0.98 | 0.98 | +0.06 | [+0.03, +0.10] | unclear |
| standardised | 1.5 | zscore | 0.99 | 0.99 | 0.99 | +0.00 | [-0.01, +0.01] | none |
| standardised | 1.5 | ewma | 1.00 | 0.99 | 0.99 | -0.00 | [-0.01, -0.00] | none |
| standardised | 1.5 | cusum | 1.00 | 1.00 | 1.00 | -0.00 | [-0.00, +0.00] | none |
| standardised | 2 | fixed | 0.96 | 1.00 | 0.99 | +0.03 | [+0.00, +0.06] | none |
| standardised | 2 | zscore | 1.00 | 1.00 | 1.00 | +0.00 | [-0.00, +0.00] | none |
| standardised | 2 | ewma | 1.00 | 1.00 | 1.00 | +0.00 | [+0.00, +0.00] | none |
| standardised | 2 | cusum | 1.00 | 1.00 | 1.00 | +0.00 | [+0.00, +0.00] | none |
| absolute | 500 | fixed | 0.44 | 0.61 | 0.66 | +0.22 | [+0.16, +0.28] | REAL |
| absolute | 500 | zscore | 0.66 | 0.61 | 0.62 | -0.04 | [-0.08, -0.01] | none |
| absolute | 500 | ewma | 0.69 | 0.60 | 0.60 | -0.09 | [-0.12, -0.06] | unclear |
| absolute | 500 | cusum | 0.65 | 0.59 | 0.59 | -0.06 | [-0.10, -0.03] | none |
| absolute | 1000 | fixed | 0.65 | 0.76 | 0.77 | +0.12 | [+0.07, +0.16] | REAL |
| absolute | 1000 | zscore | 0.84 | 0.74 | 0.74 | -0.10 | [-0.14, -0.07] | REAL |
| absolute | 1000 | ewma | 0.86 | 0.76 | 0.74 | -0.12 | [-0.15, -0.08] | REAL |
| absolute | 1000 | cusum | 0.83 | 0.73 | 0.71 | -0.12 | [-0.16, -0.08] | REAL |
| absolute | 1500 | fixed | 0.86 | 0.88 | 0.89 | +0.02 | [+0.00, +0.05] | none |
| absolute | 1500 | zscore | 0.92 | 0.84 | 0.83 | -0.09 | [-0.13, -0.07] | unclear |
| absolute | 1500 | ewma | 0.94 | 0.87 | 0.85 | -0.09 | [-0.12, -0.06] | unclear |
| absolute | 1500 | cusum | 0.92 | 0.83 | 0.81 | -0.11 | [-0.14, -0.08] | REAL |
| absolute | 2000 | fixed | 0.96 | 0.95 | 0.95 | -0.01 | [-0.03, +0.00] | none |
| absolute | 2000 | zscore | 0.96 | 0.91 | 0.89 | -0.07 | [-0.10, -0.05] | none |
| absolute | 2000 | ewma | 0.97 | 0.93 | 0.92 | -0.06 | [-0.08, -0.04] | none |
| absolute | 2000 | cusum | 0.96 | 0.91 | 0.89 | -0.07 | [-0.09, -0.04] | none |
