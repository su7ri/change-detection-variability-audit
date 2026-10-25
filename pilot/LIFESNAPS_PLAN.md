# Real-data consistency check on LifeSnaps (frozen plan)

Written on 25 Oct 2026, BEFORE any LifeSnaps data was opened. If something has to change after results are seen,
it is added as a dated amendment at the bottom, never edited in place.

## Purpose and limits
Check whether the pattern found in the simulator (ANALYSIS_PLAN.md, tradeoff experiment) shows up in real
daily step series. This is a consistency check, not a test: LifeSnaps has about 71 users, so about 20 to 24
per variability tercile and wide intervals. A real-data result cannot confirm or refute H2 or H3 on its own.
Alarms on real data include genuine, unlabelled changes, so they are called "alarm rate", not "false-alarm rate".

## Data
- LifeSnaps (Yfantidou et al., Scientific Data 2022), the openly licensed version only (Zenodo record 7229547,
  version 4 per my earlier check; Soroush verifies the licence and version on the record page before downloading;
  version 2 is restricted and is not used). File: the daily Fitbit table (daily_fitbit_sema_df_unprocessed.csv or
  the equivalent daily file of that version).
- Variable: daily step count, one row per user per day. The data files stay on Soroush's computer in
  data/lifesnaps/ and are never committed (data/ is in .gitignore); only code and aggregated results are committed.
- Before freezing, only the column names may be looked at, to find the user id, date and steps columns.
  Counts of users or days are looked at only after this plan is committed.

## Preparing each user's series
1. Order by date; use calendar days. Day 0 = the user's first day with a step count above 0.
2. A day with 0 steps (or no value) is treated as not observed (device not worn). Sensitivity run, reported
   separately: 0 steps kept as observed values.
3. Baseline = days 0-27. Evaluation segment = day 28 to the user's last day, at most 56 days (days 28-83).
4. A user is eligible if: at least 14 observed days in the baseline; an evaluation segment of at least 35 days;
   and at least 50% of the evaluation segment observed. No other exclusions.
5. If fewer than 45 users are eligible (15 per tercile), the check is reported as inconclusive and the rules above
   are NOT loosened.

## Variability groups
Terciles of the user's log-scale SD of observed baseline steps (days 0-27), equal-sized, never using the evaluation
segment. Reported by tercile: median daily steps, share of observed days, share of 0-step days, evaluation length,
and the Spearman correlation between log-SD and median steps. These are confounds to report; no causes are claimed.

## Detectors
The same detectors as the simulator, with the missing-day rules of the `missing` scenario (window detectors abstain
unless the last 7 days have at least 3 observations and the prior 21-day window at least half of its days; no alarm
on an unobserved day; EWMA and CUSUM skip missing days; baseline needs at least 14 observed days):
fixed threshold, personal z-score, EWMA, CUSUM, and the shrunk-scale window detector (SD type) with lambda in
{0, 0.5, 1}. Tuning constants: one per detector, set so that the pooled alarm rate on the un-injected evaluation
segments of all eligible users is 3.33 episodes per 100 calendar user-days (the same target, 7-day episode merging).
There is no separate calibration set because the sample is small; tuning uses only the pooled rate, never group
information, and this is stated in the paper.
The population scale for the shrunk detector is the median of the prior-window SD over all eligible users' evaluation
windows.

## Injected changes
Downward level shift, floored at 0, applied to the un-injected series from the onset to the end of the segment.
Conventions: standardised, 1 x the user's own baseline SD; absolute, 1000 steps. For each user, 20 onsets drawn
uniformly (fixed seed 11) from days 35 to (last evaluation day - 13), one shift per copy of the series, identical for
every detector. If a user's segment is too short for that range, the user is not used for the detection metrics
(and the count is reported). Missing days stay missing after injection.

## Metrics and gaps
Same as the simulator: alarm rate per 100 calendar user-days (un-injected), restricted mean delay censored at 14 days,
detection within 14 days; gap = high minus low tercile; user is the unit; stratified bootstrap over users, 1000
resamples, seed 7; margins 1.0 alarm per 100 user-days, 1.5 days, 0.10.

## What counts as "consistent with the simulator"
For each detector, metric and convention, the real-data gap is consistent if the gap found in the simulator's
`missing` scenario (results/pilot_gaps.csv, and tradeoff_gaps.csv for the shrunk detector) lies inside the real-data
95% interval. Report the share of cells that are consistent, the cells that are not, and the sign of every gap.
Intervals are expected to be wide; a wide interval that contains the simulated gap and also zero is reported as
"not informative", not as agreement. The paper states that the real-data check cannot decide H2.

## Amendments
Dated, appended after the fact, never edited in place.
- 2026-10-25, before any data were opened: Soroush pasted the Zenodo record page. Confirmed: Version 4
  (doi 10.5281/zenodo.7229547), "Open", licence CC BY 4.0, one file rais_anonymized.zip (615 MB). The daily table
  is csv_rais_anonymized/daily_fitbit_sema_df_unprocessed.csv inside it. Version 4 updates the CSV files after a
  bug fix in the export, so only version 4 is used. The record says 71 participants and "more than 4 months";
  the daily table's actual length per user is not known yet and is checked only after this plan is committed.
