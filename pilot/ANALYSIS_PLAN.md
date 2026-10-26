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
- 2026-10-26, written BEFORE running the experiment below (drift hypothesis, prompted by the LifeSnaps result).
  Real series showed an alarm-rate gap for EWMA and CUSUM, also on log-steps, that the simulator did not produce.
  Untested guess: real series drift away from the 28-day baseline, and a drift of the same relative size is a larger
  multiple of a low-variability user's SD. The simulator is extended with such a drift and the guess is tested.
  - Drift: each simulated series gets a linear trend on the log scale, reaching T at the end of the series
    (day 83), T ~ Normal(0, d) drawn independently per user and replicate, independent of the user's variability.
    The trend is applied to the un-injected series, so baseline statistics see only the first days of it.
    d = 0.15 (`drift_small`), 0.25 (`drift`), 0.35 (`drift_large`); `drift_log` = d 0.25 with detectors on log(steps).
    These sizes are assumptions, not estimates from data. Same simulated users and noise as `realistic` (the drift
    is drawn after all other random numbers, so the earlier scenarios are unchanged). Everything else as in the pilot.
  - Hypothesis D: with drift, in `drift` and in `drift_log`, the alarm-rate gap (high minus low) of EWMA and of CUSUM
    is below -1.0 per 100 user-days with a 95% interval excluding 0, while the personal z-score window detector's
    gap stays inside the margin (|gap| < 1.0). Dose-response: the CUSUM alarm-rate gap is more negative in
    `drift_large` than in `drift` and in `drift` than in `drift_small`.
  - If D holds, drift is reported as a mechanism that can produce the real-data pattern (not as proof that it did).
    If it does not hold, the guess is reported as not supported by this model of drift.
  - Delay and detection gaps are also reported, with no separate decision rule.
- 2026-10-26, after running the drift scenarios (results/drift_summary.md, drift_gaps.csv, drift_groups.csv; 1000
  resamples; the earlier scenarios re-run and byte-identical). Hypothesis D is NOT supported.
  - Alarm-rate gap, high minus low, CUSUM / EWMA: `realistic` -0.99 / -0.47; `drift_small` -1.09 / -0.68;
    `drift` -1.21 / -0.92; `drift_large` -1.31 / -1.10; `drift_log` -0.52 / -0.53. The z-score window detector stays
    within the margin everywhere (-0.48 at most).
  - Against the pre-set rule: in `drift`, CUSUM passes (-1.21, interval excludes 0) but EWMA does not (-0.92, above the
    -1.0 margin); in `drift_log` neither passes (both inside the margin). The dose-response for CUSUM holds (more
    negative with more drift) but the steps are small.
  - So in this model drift widens the raw-scale CUSUM/EWMA alarm-rate gap a little, and does not reproduce the log-scale
    gap seen in LifeSnaps (real -3.15 / -2.34 against simulated -0.5). The drift guess is not supported as the
    explanation; the real-data gap stays unexplained. Other candidates (changes that are real and not injected,
    wear-time and routine effects tied to variability, small-sample noise with 17 users per tercile) are untested.
- 2026-10-26, written BEFORE running the experiment below (sensitivity analysis, prompted by a critical review
  of the two-page summary). Question: do the pilot's two main patterns survive when one assumption of the simulator
  is changed at a time? Base = `realistic` (300 users, 20 replicates, target 3.33, calibration seed 101,
  evaluation seed 202). Each variant changes ONE factor; everything else stays at the base value.
  - Variants (2 levels per factor, plus the base for reference):
    1. alarm-rate target: 1.5 and 6.0 episodes per 100 user-days;
    2. calibration seed: 303 and 404 (the evaluation data stay the same);
    3. evaluation seed: 505 and 606 (new simulated users and noise, same calibration set rule);
    4. number of users: 600 (replicates 20);
    5. autocorrelation: none (phi = 0) and strong (phi ~ U(0.3, 0.8));
    6. spread of variability across users: log-SD of sigma 0.20 (narrow) and 0.55 (wide);
    7. tails of the noise: Gaussian and Student-t with 3 degrees of freedom (base 4);
    8. level-variability correlation: correlation of log level with log sigma of -0.4 and +0.4 (base 0;
       LifeSnaps showed about -0.33 between variability and median steps);
    9. shape of the change: a ramp that grows linearly from 0 at onset to the full shift on day 14
       (delay is still counted from onset, censored at 14 days).
  - Detectors, metrics, margins, bootstrap (1000 resamples), and tuning rule are unchanged. The shrunk-scale
    detector uses the SD scale and lambda in {0, 0.25, 0.5, 0.75, 1}. Conventions: standardised 1 SD and
    absolute 1000 steps.
  - Robustness criteria, fixed now (all on point estimates and the pre-set verdicts):
    R1. Personal detectors (z-score, EWMA, CUSUM), standardised k = 1: no REAL gap in restricted mean delay or in
        detection within 14 days.
    R2. Crossing: alarm-rate gap at lambda 0 above +1.0 and at lambda 1 below +1.0; and absolute-convention delay gap
        at most -1.5 days at lambda 0 and at least +1.5 days at lambda 1.
    R3. A balanced lambda exists: some lambda in the grid whose alarm-rate gap is within +/-1.0 per 100 user-days and
        whose two delay gaps (standardised 1 SD and absolute 1000 steps) are both within +/-1.5 days.
  - A claim is called robust if its criterion holds in every variant, mostly robust if it holds in at least 80% of
    the variants, and sensitive otherwise. The paper states each claim at the strength found, and names the factor
    that breaks it.
  - Exploratory question, no decision rule: does any variant (especially level-variability correlation or the ramp)
    produce a CUSUM alarm-rate gap of about -2 or lower (the real data gave -3.3), on raw steps?
  - The results are reported whatever they show, including variants where R1 to R3 fail.
- 2026-10-26, results of the sensitivity analysis above (results/sensitivity_*.csv, sensitivity_summary.md; 17 variants,
  1000 resamples). Old outputs (8 scenarios, trade-off, drift) were re-run after the code change and are byte-identical.
  - R1 (personal detectors, no real delay or detection gap at 1 SD): holds in 16 of 16 variants, **robust**. All 102 cells
    (3 detectors x 2 metrics x 17 variants) have verdict "none". The largest point estimate is +0.76 days (CUSUM, wide
    variability spread), inside the 1.5-day margin.
  - R2 (the crossing): holds in 13 of 16 variants, **mostly robust**. Fails in `target_6.0` (absolute delay gap at lambda 0
    is -0.86 days; at lambda 1 +1.47, just under 1.5), `spread_narrow` (-1.33 / +1.04) and `ramp14` (lambda 1: +1.21).
    The signs of the four quantities (alarm gap at lambda 0 positive, delay gaps at lambda 0 negative and at lambda 1 positive
    in both conventions) are the same in all 17 variants except one near-zero value (standardised delay gap at lambda 1 in
    `phi_strong`, -0.06); only the size falls below the pre-set margins. The size grows with the spread of variability
    (alarm gap at lambda 0: +1.69 narrow, +3.33 base, +4.93 wide).
  - R3 (a balanced lambda exists): holds in 13 of 16 variants, **mostly robust**, but only just. In the base case lambda 0.75
    sits at 0.89 of the tightest margin. It fails in `evalseed_606` (absolute delay gap +1.505 against 1.5, a miss of 0.005
    days), `spread_wide` (alarm +1.25, absolute delay +1.91) and `corr_pos` (alarm +1.14, absolute delay +1.75). The best
    lambda on the grid is 0.75 in all 17 variants, and there all three gaps stay within 1.27 times the margins (descriptive,
    chosen after the run, not a pre-set criterion).
  - Exploratory question (CUSUM alarm-rate gap of about -2 or lower on raw steps): no variant gets there; the most negative
    is `spread_wide` (-1.52); base -0.99. The real LifeSnaps gap (-3.3) remains unexplained by anything in this simulator.
  - Two facts about the design of the variants that limit what they show: (1) the personal detectors are scale-free in the
    multiplicative model, so the level-variability correlation leaves their results identical to the base case (only the
    fixed threshold and the absolute convention change); the correlation variants therefore do not test the personal
    detectors; (2) the ramp does not change alarm rates (they are measured on series without a change), only delays.
  - Reading: the audit finding (personal detectors have no gap in delay or detection beyond the margins) is robust in
    this simulator. The trade-off has the same direction everywhere but its size depends on how spread out the users'
    variability is. A single balanced lambda is not a stable result: it sits near the margins and moves with the data.
    Seed-to-seed variation of point estimates is about 0.3 to 0.4 days for the delay gaps at lambda 1 (2.27, 1.96, 2.76
    for evaluation seeds 202, 505, 606).
- 2026-10-26, written BEFORE running the experiment below (combined-change check, prompted by the second critical review:
  the 16 sensitivity settings each changed one assumption). Question: do the three sensitivity claims (R1, R2, R3, defined
  in the sensitivity amendment above, unchanged) survive when several assumptions change together? Base = `realistic`.
  - Three combinations, chosen from the one-at-a-time results (not from any combined run):
    C1 `combo_weak`   the three conditions that made R2 fail, together: narrow variability spread (log-SD 0.20),
                      alarm-rate target 6.0 per 100 user-days, 14-day ramp change.
    C2 `combo_stress` the conditions that enlarged gaps or noise, together: wide spread (log-SD 0.55), level-variability
                      correlation +0.4, Student-t noise with 3 df, strong autocorrelation (phi ~ U(0.3, 0.8)).
    C3 `combo_reallike` features the real LifeSnaps data have, together: missing days more frequent for high-variability
                      users, 14-day prior window and baseline, level-variability correlation -0.4, 14-day ramp change.
  - Everything else, the criteria R1 to R3, the margins, the 1000 resamples and the seeds (101, 202) are unchanged.
  - Predictions, written before the run: R1 holds in all three; R2 fails in C1 (every one of its three parts weakened R2
    alone) and holds in C2 and C3; R3 fails in C2 (wide spread and positive correlation each failed it alone) and is
    uncertain in C1 and C3. Where the result differs from these predictions, the report says so.
  - With only three combinations, no 80% rule: each criterion is reported as held or failed per combination.
  - Descriptive only (no decision rule): whether any lambda has all three intervals inside the margins; the CUSUM
    alarm-rate gap on raw steps against the real-data value of about -3.3.
  - These three are examples of joint changes, not a search of the space. A claim that holds here is not shown to hold
    for all combinations.
- 2026-10-26, results of the combined-change check above (results/sensitivity_combos_*.csv/md; `python sensitivity.py --combos`).
  Existing sensitivity outputs were re-run after the code change; the two CSVs are byte-identical.
  - R1 holds in 3 of 3 (all 18 cells "none"; largest point estimate +0.54 days, CUSUM in C3). Predicted: yes.
  - R2 holds in 1 of 3 (C2 only). C1 `combo_weak` fails (absolute delay gap at lambda 0 is -1.07, margin 1.5): predicted.
    C3 `combo_reallike` fails (absolute delay gap at lambda 1 is +0.66, margin 1.5): **prediction missed**, I had expected it to
    hold. In C1 and C3 the crossing is small, not reversed: signs are as before, sizes are below the pre-set criterion.
  - R3 holds in C1 and C3 and fails in C2. Predicted for C2; "uncertain" for C1 and C3. In C1 and C3, lambda 0.75 and 1 have all
    three intervals inside the margins (descriptive), because the gaps are small to begin with.
  - C2 `combo_stress` (wide spread, correlation +0.4, t3 noise, strong autocorrelation): no lambda on the grid balances the
    three gaps. At lambda 0.75: alarm +1.31, standardised delay -1.63, absolute delay +1.52, all three with verdict REAL.
    The strongest case for the mitigation therefore requires that users' variability is not very spread out.
  - Exploratory: no combination reproduces the real CUSUM alarm-rate gap (-0.52, -0.84, -0.75 against -3.3).
  - Reading: the audit result (R1) holds in all 20 settings tried (the base case, 16 changed one at a time, and 3 combined).
    The crossing and the balanced lambda are real in the base case and under heterogeneous users, shrink to within the margins
    under weak-signal or real-data-like conditions, and fail to balance under the most heterogeneous condition.
