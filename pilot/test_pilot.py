import numpy as np
import detectors as dt
import sim
import pilot


def _series(scen=sim.REALISTIC, n=60, reps=6, seed=1):
    rng = np.random.default_rng(seed)
    users = sim.make_users(n, rng)
    return users, sim.simulate_series(users, reps, scen, rng), rng


def test_shapes_and_positive():
    _, x, _ = _series()
    assert x.shape == (60, 6, sim.N_DAYS)
    assert (x > 0).all()


def test_deterministic():
    _, a, _ = _series(seed=5)
    _, b, _ = _series(seed=5)
    assert np.array_equal(a, b)


def test_ideal_log_sd_matches_sigma():
    rng = np.random.default_rng(3)
    users = sim.make_users(40, rng)
    x = sim.simulate_series(users, 60, sim.IDEAL, rng)
    est = np.log(x).std(axis=(-1, -2))
    assert np.corrcoef(est, users["sigma"])[0, 1] > 0.97
    assert abs(np.median(est / users["sigma"]) - 1) < 0.05


def test_inject_only_after_onset_and_floor():
    _, x, rng = _series()
    onset = sim.draw_onsets(60, 6, rng)
    delta = np.full((60, 6), 1000.0)
    xi = sim.inject(x, onset, delta)
    t = np.arange(sim.N_DAYS)[None, None, :]
    before = t < onset[..., None]
    assert np.array_equal(xi[before], x[before])
    after = ~before
    assert np.allclose(xi[after], np.maximum(0, x[after] - 1000.0))
    assert (xi >= 0).all()


def test_terciles_balanced():
    _, x, _ = _series(n=90)
    g = sim.variability_terciles(x)
    assert [int((g == k).sum()) for k in range(3)] == [30, 30, 30]


def test_calibration_hits_target():
    rng = np.random.default_rng(11)
    users = sim.make_users(200, rng)
    x = sim.simulate_series(users, 8, sim.REALISTIC, rng)
    s = dt.Stats(x)
    for name in dt.DETECTORS:
        p = dt.calibrate(name, s, 3.33)
        rate = dt.alarm_rate(dt.DETECTORS[name][0](s, p))
        assert abs(rate - 3.33) < 0.15, (name, rate)


def test_detectors_catch_a_big_shift_fast():
    users, x, rng = _series(scen=sim.IDEAL, n=100, reps=4)
    s = dt.Stats(x)
    onset = np.full((100, 4), 40)
    xi = sim.inject(x, onset, 3.0 * sim.baseline_sd(x))
    si = dt.Stats(xi)
    for name, (fn, _) in dt.DETECTORS.items():
        p = dt.calibrate(name, s, 3.33)
        d = dt.delays(fn(si, p), onset)
        assert (d < 14).mean() > 0.8, name


def test_no_alarms_before_evaluation_and_no_peeking():
    # changing data AFTER day t must not change any detector output at day t
    _, x, _ = _series(n=30, reps=3)
    x2 = x.copy()
    x2[..., 60:] *= 0.1
    for name, (fn, (lo, hi)) in dt.DETECTORS.items():
        p = 0.5 * (lo + hi) * 0.05
        a, b = fn(dt.Stats(x), p), fn(dt.Stats(x2), p)
        cut = 60 - sim.BASE_DAYS
        assert np.array_equal(a[..., :cut], b[..., :cut]), name


def test_merge_events_refractory():
    f = np.zeros((1, 1, 20), dtype=bool)
    f[..., [2, 3, 8, 9, 10]] = True
    ev = dt.merge_events(f)
    assert list(np.where(ev[0, 0])[0]) == [2, 9]


def test_delays_censoring():
    f = np.zeros((1, 3, sim.EVAL_DAYS), dtype=bool)
    onset = np.array([[40, 40, 40]])
    f[0, 0, 40 - 28 + 3] = True       # delay 3
    f[0, 1, 40 - 28 + 20] = True      # beyond horizon -> censored at 14
    # series 2: alarm before onset only -> censored
    f[0, 2, 5] = True
    d = dt.delays(f, onset)
    assert list(d[0]) == [3, 14, 14]


def test_verdict_rules():
    r = dict(metric="alarm_rate", gap_high_minus_low=2.0, gap_lo=1.5, gap_hi=2.5)
    assert pilot.verdict(r) == "REAL"
    r = dict(metric="alarm_rate", gap_high_minus_low=0.1, gap_lo=-0.3, gap_hi=0.5)
    assert pilot.verdict(r) == "none"
    r = dict(metric="alarm_rate", gap_high_minus_low=0.5, gap_lo=-0.8, gap_hi=1.8)
    assert pilot.verdict(r) == "unclear"


def test_additive_positive_and_symmetric():
    rng = np.random.default_rng(21)
    users = sim.make_users(60, rng)
    x = sim.simulate_series(users, 6, sim.SYMMETRIC, rng)
    assert (x > 0).all()
    z = (x - x.mean(-1, keepdims=True)) / x.std(-1, keepdims=True)
    skew = (z ** 3).mean()
    rng = np.random.default_rng(21)
    users = sim.make_users(60, rng)
    xl = sim.simulate_series(users, 6, sim.REALISTIC, rng)
    zl = (xl - xl.mean(-1, keepdims=True)) / xl.std(-1, keepdims=True)
    assert abs(skew) < 0.5 * abs((zl ** 3).mean())     # additive noise is much less skewed than log-normal


def test_scenarios_sharing_seed_key_share_data():
    assert sim.SCENARIOS["realistic_log"].seed_key == "realistic"
    assert sim.SCENARIOS["realistic_log"].log_detect and not sim.SCENARIOS["realistic"].log_detect


def test_statsnan_equals_stats_without_missing():
    _, x, _ = _series()
    a, b = dt.Stats(x), dt.StatsNaN(x)
    assert np.allclose(a.delta, b.delta) and np.allclose(a.prior_sd, b.prior_sd) and np.allclose(a.u, b.u)
    for name, (fn, _) in dt.DETECTORS.items():
        c = {"fixed": 800.0, "zscore": 1.0, "ewma": 1.5, "cusum": 3.0}[name]
        assert np.array_equal(fn(a, c), fn(b, c))


def test_missing_probability_rises_with_sigma_and_no_alarm_on_missing_days():
    users, x, rng = _series(n=200, reps=4)
    xm = sim.apply_missing(x, users, rng)
    miss = np.isnan(xm).mean((1, 2))
    order = np.argsort(users["sigma"])
    assert miss[order[-60:]].mean() > miss[order[:60]].mean() + 0.05
    s = dt.StatsNaN(xm)
    for name, (fn, _) in dt.DETECTORS.items():
        c = {"fixed": 300.0, "zscore": 0.3, "ewma": 0.5, "cusum": 0.5}[name]
        f = fn(s, c)
        assert not (f & np.isnan(xm[..., sim.BASE_DAYS:])).any()
        assert f.any()


def test_window_detector_abstains_with_too_few_observations():
    x = np.full((1, 1, sim.N_DAYS), 5000.0)
    x[..., 60:] = 1000.0
    x[..., 54:60] = np.nan                    # day 60 + : recent window has <3 observations at some days
    s = dt.StatsNaN(x)
    j = 61 - sim.BASE_DAYS                   # day 61: recent days 55..61 -> only 61 and nothing else observed? (55-59 NaN)
    assert np.isnan(s.delta[0, 0, j])
    assert not dt.fire_fixed(s, 1.0)[0, 0, j]


def test_no_look_ahead_with_missing():
    users, x, rng = _series(n=20, reps=3)
    xm = sim.apply_missing(x, users, rng)
    x2 = xm.copy()
    x2[..., 70:] = 100.0
    s1, s2 = dt.StatsNaN(xm), dt.StatsNaN(x2)
    j = 70 - sim.BASE_DAYS
    assert np.allclose(s1.delta[..., :j], s2.delta[..., :j], equal_nan=True)
    assert np.allclose(s1.u[..., :j], s2.u[..., :j], equal_nan=True)


def test_short_windows_use_right_days():
    x = np.zeros((1, 1, sim.N_DAYS))
    x[..., 40:] = -1.0                        # step at day 40
    x += np.arange(sim.N_DAYS) * 0.0
    s = dt.StatsNaN(x, prior_len=7, base_len=7)
    t = 47                                    # recent 41..47 (all -1), prior 34..40 (6 zeros, one -1)
    assert np.isclose(s.delta[0, 0, t - sim.BASE_DAYS], -1.0 + 1.0 / 7.0)


def test_shrunk_lambda_endpoints():
    _, x, _ = _series()
    s = dt.StatsNaN(x, with_mad=True)
    pop = float(np.median(s.prior_sd))
    assert np.array_equal(dt.fire_shrunk(s, 0.5, 1.0, pop), dt.fire_zscore(s, 0.5))
    assert np.array_equal(dt.fire_shrunk(s, 0.5, 0.0, pop), s.delta / pop <= -0.5)
    assert (s.prior_mad > 0).all()


def test_calibrate_fn_hits_target():
    _, x, _ = _series(n=100, reps=6)
    s = dt.StatsNaN(x, with_mad=True)
    pop = float(np.median(s.prior_sd))
    c = dt.calibrate_fn(lambda st, k: dt.fire_shrunk(st, k, 0.5, pop), s, 3.33)
    assert abs(dt.alarm_rate(dt.fire_shrunk(s, c, 0.5, pop)) - 3.33) < 0.15
