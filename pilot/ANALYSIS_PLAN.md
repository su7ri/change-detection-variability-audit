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
Dated, appended after the fact, never edited in place.

- 2026-10-25, after the first pilot run: the margins above were confirmed by Soroush as proposed.
- 2026-10-25, after the first pilot run (exploratory, post hoc): two diagnostic scenarios were added because
  the CUSUM alarm-rate gap in `realistic` could be a side effect of the log-normal model, where variability
  and skewness grow together.
  - `realistic_log`: the same simulated data as `realistic`; detectors run on log(steps).
  - `symmetric`: noise added on the raw scale, relative SD capped at 0.45, values floored at 5% of the user's level.
  The `ideal` and `realistic` results are unchanged (checked: identical output). The decision rule is
  unchanged and still applies to `realistic`; the diagnostics only help explain it.
- 2026-10-25, written BEFORE running the experiments below. The first pilot found no gap for personal-baseline
  detectors in the standardised convention. Four more scenarios test where a gap could still appear. All use
  the same simulated data as `realistic` (same seed_key), the same detectors, the same metrics, margins and
  decision rule, and each detector is re-tuned to 3.33 alarm episodes per 100 user-days in its own scenario.
  - `missing`: each day is missing with probability 0.05 + 0.30 x (sigma - 0.10) / 0.80, so high-variability
    users miss more days (5% to 35%). This direction is an assumption, not an estimate from data.
    Statistics use observed days only. A window detector abstains unless the last 7 days have at least 3
    observations and the prior window has at least half of its days. No detector alarms on a day without an
    observation. EWMA and CUSUM skip the update on missing days. Alarm rate is still per calendar user-day.
    The baseline for EWMA and CUSUM needs at least half of its days observed, otherwise the series abstains.
  - `short14`: prior window 14 days, EWMA/CUSUM baseline = days 0-13. `short7`: both 7 days. Evaluation days,
    variability terciles (28-day log SD) and injections are unchanged.
  - `missing_short14`: both changes together.
  - Also reported for the missing scenarios (descriptive, no margin): share of evaluation days observed and
    share on which the window detectors can decide (abstention coverage), by tercile.
  - Not run in this round: variance-increase and gradual (ramp) changes. The four detectors are level detectors;
    a variance change would need new detectors that are not in this plan.
  - Decision rule: H2 is supported if, in any of these four scenarios, a personal-baseline detector shows a
    REAL gap at k = 1 (standardised) on alarm rate, restricted mean delay or detection within 14 days.
- 2026-10-25, after running the four scenarios above (results in results/pilot_summary.md, 1000 bootstrap
  resamples, the same as the earlier committed runs; the old four scenarios are byte-identical to before).
  - In no new scenario does a personal-baseline detector show a REAL gap in restricted mean delay or in detection
    within 14 days, at k = 1 or at any other standardised effect size.
  - One cell crosses the alarm-rate margin by the letter of the rule: CUSUM in `missing`, gap -1.02 [-1.21, -0.82]
    per 100 user-days (margin 1.0). It is the same skewness effect as in `realistic` (-0.99), `ideal` (-1.16);
    it disappears when detectors run on log(steps) (-0.11) and in `symmetric` (-0.03), and it points the other way
    from harm (high-variability users get fewer false alarms). Missing days add nothing to it.
    Reported as a knife-edge cell of a known artefact, not as support for H2.
  - Missing days do reduce coverage for high-variability users (observed days 0.90 / 0.87 / 0.83 by tercile;
    window detectors can decide on 0.90 / 0.87 / 0.82 of days). That is a coverage gap, not a detection gap.
- 2026-10-25, written BEFORE running the experiment below (trade-off between the two equality conventions;
  this is the planned mitigation, run as a separate experiment).
  - Detector family, one window detector with a shrunk scale: alarm if delta / s <= -c, where
    s = lambda x s_own + (1 - lambda) x s_pop. delta, the 7-vs-prior-window difference, and the abstention rules
    are the same as for the z-score detector. s_own is the scale of the user's own prior window; s_pop is one
    constant for everyone: the median of that same scale over all windows of the calibration set (different seed).
    lambda = 0 is a fixed threshold in steps (up to rescaling); lambda = 1 is the personal z-score.
  - lambda in {0, 0.25, 0.5, 0.75, 1}. Two scale types: `sd` (standard deviation) and `mad` (1.4826 x median
    absolute deviation), the robust variant. Nothing else is tuned. For each lambda, c is re-tuned on the
    calibration set to 3.33 alarm episodes per 100 user-days, as for the other detectors.
  - Scenarios (same simulated data as `realistic`): `realistic`, `short7`, `missing`.
  - Metrics, same definitions and margins as before. Two conventions: standardised k = 1 and absolute 1000 steps.
    Reported per lambda: alarm-rate gap (un-injected), and RMD and detection within 14 days gaps (high minus low
    tercile) under each convention, with the bootstrap intervals (1000 resamples) and verdicts.
  - Question: is there a trade-off, i.e. no lambda that makes both conventions equal?
  - Pre-set criterion for "trade-off confirmed" in `realistic`, `sd` type, on RMD:
    (|absolute gap at lambda = 1| - |absolute gap at lambda = 0|) > 1.5 days AND
    (|standardised gap at lambda = 0| - |standardised gap at lambda = 1|) > 1.5 days.
    If only one holds, or neither, it is reported as "no trade-off in this range". If it holds, the lambda
    values at which the absolute gap and the standardised gap are each within the margin are reported
    (possibly none).
  - The result is reported whatever it shows. Part of a trade-off is expected from the algebra (a fixed shift in
    steps is a different multiple of different users' SDs); the contribution is its size and shape, and how the
    robust scale and the missing/short-baseline scenarios change it.
- 2026-10-25, after running the trade-off experiment (results/tradeoff_summary.md, 1000 resamples).
  - Pre-set criterion NOT met in `realistic` (sd type): the absolute-convention RMD gap does not grow in
    magnitude from lambda 0 to 1 (|-2.86| at 0, |+2.27| at 1; change -0.59 days, needed > +1.5); it changes sign.
    The standardised-convention gap does shrink (3.37 -> 0.34, change +3.04). Reported as "no trade-off in the
    sense of the criterion".
  - What the data show instead: a crossing. At lambda 0 high-variability users are detected faster but get more
    alarms; at lambda 1 they are detected later (absolute convention). Delay gaps are within or near the margin
    around lambda 0.5 to 0.75 (sd, realistic: standardised -1.44 / -0.49, absolute +0.06 / +1.33; mad at 0.75:
    -1.10 / +0.31). The alarm-rate gap falls from +3.3 to -0.2 (sd) with lambda, so it needs lambda near 0.75 or
    higher. Same pattern in `short7` and `missing`. The robust (mad) scale narrows the delay gap but leaves a larger
    alarm-rate gap at the same lambda (realistic, lambda 1: +0.72 vs -0.21).
  - Caveat: this is the same simulator and the same assumptions; the lambda that balances the gaps is specific to
    this variability distribution and not a recommendation for real data.
