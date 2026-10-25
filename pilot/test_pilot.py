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
