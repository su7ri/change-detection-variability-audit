# Analysis plan (pilot, simulator only)

Written on 25 Oct 2026, before the first pilot run. Everything here is fixed. If something has to change
after results are seen, it is added as a dated amendment at the bottom, never edited in place.

## Question
Do standard personal-baseline change detectors treat users with high and low day-to-day variability
equally? Variability groups are terciles of each user's log-scale SD over a 28-day baseline window.

## Data (simulated users)
- 300 users per run. Each user has an own level, own day-to-day variability (continuous, log-normal
  across users), own autocorrelation, own weekly pattern.
- Series are daily steps, strictly positive, floor at 0 after injection.
- Two scenarios: `ideal` (Gaussian noise, no autocorrelation, no weekly cycle) and `realistic`
  (heavy tails, autocorrelation, weekly cycle).
- 20 independent replicates per user. Each replicate has 84 days: days 0-27 baseline, days 28-83 evaluation.
- Not simulated in this pilot: missing days, non-wear, slow trends, several variables at once.

## Injected changes
- One downward level shift per replicate, onset uniform on days 35-49, lasting to the end of the series.
- The same noise is used for the un-injected and every injected version of a replicate, and for every detector.
- Two conventions, both always reported:
  - standardised: shift = k x the series' own baseline SD (days 0-27), k in {0.5, 1, 1.5, 2};
  - absolute: shift = A steps for everyone, A in {500, 1000, 1500, 2000}.
- Values are floored at 0. The fraction of injected series affected by the floor is reported.

## Detectors (all use only data available on the day)
Recent = mean of the last 7 days. Prior = the 21 days before them (days t-27 to t-7). delta = recent - prior mean.
1. Fixed threshold: alarm if delta <= -T steps, one T for everyone.
2. Personal z-score: alarm if delta / (prior SD) <= -c.
3. EWMA (lambda 0.2) on the standardised daily value against the day 0-27 baseline: alarm if
   S <= -L x sqrt(lambda / (2 - lambda)); state resets to 0 after an alarm.
4. One-sided CUSUM (k = 0.5) on the same standardised value: alarm if C >= h; resets to 0 after an alarm.
Evaluation starts on day 28.

## Fair comparison
Each detector has one tuning constant (T, c, L, h). It is set on a separate calibration set (different
seed) so that the pooled alarm rate over all un-injected series equals 3.33 alarm episodes per 100
user-days (about one per 30 days). Alarms within 7 days of an earlier alarm count as the same episode.
Tuning is done once per scenario and never on the evaluation set.

## Metrics
- Alarm rate: alarm episodes per 100 user-days on un-injected series (days 28-83).
- Detection delay: days from onset to the first alarm on or after onset. If no alarm in the first 14 days
  (onset to onset+13), the delay is censored at 14. Report restricted mean delay (RMD, days),
  detection within 7 days and within 14 days.
- Per-user values average over that user's 20 replicates. The user is the unit of analysis.
- Gap = high-variability tercile minus low-variability tercile, for each metric.
  Max-minus-min over the three terciles is also reported.
- Uncertainty: percentile bootstrap over users, resampled within terciles, 2000 resamples.

## What counts as a real gap (proposed margins, to confirm)
A gap is real only if its 95% interval excludes zero and the gap itself exceeds:
- alarm rate: 1.0 per 100 user-days (30% of the pooled target);
- restricted mean delay: 1.5 days;
- detection within 14 days: 0.10 (10 percentage points).
A detector "shows no meaningful gap" if the whole interval lies inside plus/minus the margin.

## Decision rule for the 8 Nov gate
- H1 (fixed threshold unequal) is expected; it is a sanity check, not a result.
- H2 holds if, for the realistic scenario and the standardised convention, at least one personal-baseline
  detector (z-score, EWMA or CUSUM) shows a real gap on at least one of the three metrics at k = 1.
- If no personal-baseline detector shows a real gap, even in the realistic scenario, the paper becomes
  "the gap is a convention choice" and its value is reassessed before real data are touched.

## Amendments
(none)
