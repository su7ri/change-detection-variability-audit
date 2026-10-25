"""
Four detectors from ANALYSIS_PLAN.md, vectorised over (users, replicates).

All detectors see, on day t, only data up to day t. Evaluation days are 28..N_DAYS-1, so every output
has length EVAL_DAYS along the last axis (index j <-> day 28 + j).
"""

from __future__ import annotations

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view as swv

import sim

REFRACTORY = 7
EWMA_LAMBDA = 0.2
CUSUM_K = 0.5


class Stats:
    """Statistics shared by the detectors, computed once per set of series."""

    def __init__(self, x: np.ndarray):
        days = np.arange(sim.BASE_DAYS, x.shape[-1])
        recent = swv(x, 7, axis=-1).mean(-1)               # index j: days j..j+6
        prior_w = swv(x, 21, axis=-1)                      # index j: days j..j+20
        prior_mean = prior_w.mean(-1)
        prior_sd = prior_w.std(-1, ddof=1)
        self.delta = recent[..., days - 6] - prior_mean[..., days - 27]    # recent 7 vs prior 21 (t-27..t-7)
        self.prior_sd = np.maximum(prior_sd[..., days - 27], 1e-9)
        m0 = x[..., : sim.BASE_DAYS].mean(-1, keepdims=True)
        s0 = np.maximum(x[..., : sim.BASE_DAYS].std(-1, ddof=1, keepdims=True), 1e-9)
        self.u = (x[..., sim.BASE_DAYS:] - m0) / s0          # standardised against days 0-27


def fire_fixed(s: Stats, T: float) -> np.ndarray:
    return s.delta <= -T


def fire_zscore(s: Stats, c: float) -> np.ndarray:
    return s.delta / s.prior_sd <= -c


def fire_ewma(s: Stats, L: float, lam: float = EWMA_LAMBDA) -> np.ndarray:
    thr = -L * np.sqrt(lam / (2.0 - lam))
    u = s.u
    state = np.zeros(u.shape[:-1])
    out = np.zeros(u.shape, dtype=bool)
    for j in range(u.shape[-1]):
        state = lam * u[..., j] + (1.0 - lam) * state
        f = state <= thr
        out[..., j] = f
        state = np.where(f, 0.0, state)
    return out


def fire_cusum(s: Stats, h: float, k: float = CUSUM_K) -> np.ndarray:
    u = s.u
    c = np.zeros(u.shape[:-1])
    out = np.zeros(u.shape, dtype=bool)
    for j in range(u.shape[-1]):
        c = np.maximum(0.0, c - u[..., j] - k)
        f = c >= h
        out[..., j] = f
        c = np.where(f, 0.0, c)
    return out


# name -> (fire function, search range for the tuning constant)
DETECTORS = {
    "fixed": (fire_fixed, (0.0, 30000.0)),
    "zscore": (fire_zscore, (0.0, 12.0)),
    "ewma": (fire_ewma, (0.0, 12.0)),
    "cusum": (fire_cusum, (0.0, 30.0)),
}


def merge_events(fires: np.ndarray, refractory: int = REFRACTORY) -> np.ndarray:
    """Alarms within `refractory` days of an earlier alarm belong to the same episode; mark episode starts."""
    ev = np.zeros_like(fires)
    since = np.full(fires.shape[:-1], refractory, dtype=int)
    for j in range(fires.shape[-1]):
        e = fires[..., j] & (since >= refractory)
        ev[..., j] = e
        since = np.where(e, 1, since + 1)
    return ev


def alarm_rate(fires: np.ndarray) -> float:
    """Pooled alarm episodes per 100 user-days."""
    return merge_events(fires).sum() / (fires.shape[0] * fires.shape[1] * fires.shape[2]) * 100.0


def calibrate(name: str, s_cal: Stats, target: float, iters: int = 40) -> float:
    """Find the tuning constant whose pooled alarm rate on the calibration set equals `target`
    (the rate falls as the constant grows)."""
    fn, (lo, hi) = DETECTORS[name]
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if alarm_rate(fn(s_cal, mid)) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def delays(fires: np.ndarray, onset: np.ndarray, horizon: int = 14) -> np.ndarray:
    """Days from onset to the first alarm on or after onset; `horizon` if none within the horizon
    (censored). fires: (n, reps, EVAL_DAYS); onset: (n, reps) as day index."""
    j = np.arange(fires.shape[-1])[None, None, :]
    start = (onset - sim.BASE_DAYS)[..., None]
    window = (j >= start) & (j < start + horizon)
    hit = fires & window
    any_hit = hit.any(-1)
    first = hit.argmax(-1) - (onset - sim.BASE_DAYS)
    return np.where(any_hit, first, horizon)
