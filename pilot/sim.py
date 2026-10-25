"""
Simulator for the variability audit pilot (see ANALYSIS_PLAN.md).

Daily steps for simulated users, each with its own level, day-to-day variability, autocorrelation and
weekly pattern. Everything here is an assumption chosen for the pilot, not an estimate from real people.

Per user i, per replicate r, day t:
    y[t] = log(mu_i) + weekly[t] + eps[t]
    eps  = AR(1) with coefficient phi_i, stationary SD sigma_i (log scale)
    x[t] = exp(y[t])           (steps, strictly positive)
`ideal` scenario: Gaussian innovations, phi = 0, no weekly cycle.
`realistic` scenario: Student-t(4) innovations, phi_i ~ U(0, 0.5), weekly cycle with amplitude ~ U(0, 0.2).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

BASE_DAYS = 28
EVAL_DAYS = 56
N_DAYS = BASE_DAYS + EVAL_DAYS          # 84
ONSET_RANGE = (35, 49)                  # inclusive, day index
BURN_IN = 20
T_DF = 4                                # Student-t degrees of freedom (heavy tails)


ADDITIVE_SIGMA_CAP = 0.45     # additive scenario: cap on the relative noise SD, to limit truncation at zero
ADDITIVE_FLOOR = 0.05         # additive scenario: values never fall below 5% of the user's level


@dataclass(frozen=True)
class Scenario:
    name: str
    heavy_tails: bool
    weekly: bool
    autocorr: bool
    additive: bool = False      # noise added on the raw scale (symmetric) instead of the log scale (skewed)
    log_detect: bool = False    # detectors run on log(steps) instead of steps
    seed_key: str = ""          # scenarios with the same seed_key get identical simulated data


IDEAL = Scenario("ideal", heavy_tails=False, weekly=False, autocorr=False)
REALISTIC = Scenario("realistic", heavy_tails=True, weekly=True, autocorr=True)
# Diagnostics for the skewness confound (variability and skewness both grow with sigma in the log-normal model):
REALISTIC_LOG = Scenario("realistic_log", True, True, True, log_detect=True, seed_key="realistic")
SYMMETRIC = Scenario("symmetric", True, True, True, additive=True)
SCENARIOS = {s.name: s for s in (IDEAL, REALISTIC, REALISTIC_LOG, SYMMETRIC)}


def make_users(n: int, rng: np.random.Generator) -> dict:
    """Between-user heterogeneity. sigma is the SD of daily log-steps: continuous across users."""
    return dict(
        mu=np.exp(rng.normal(np.log(7000.0), 0.35, n)),
        sigma=np.clip(np.exp(rng.normal(np.log(0.30), 0.35, n)), 0.10, 0.90),
        phi=rng.uniform(0.0, 0.5, n),
        amp=rng.uniform(0.0, 0.2, n),
        phase=rng.uniform(0.0, 7.0, n),
    )


def simulate_series(users: dict, reps: int, scen: Scenario, rng: np.random.Generator) -> np.ndarray:
    """Un-injected series, shape (n_users, reps, N_DAYS), in steps."""
    n = len(users["mu"])
    total = N_DAYS + BURN_IN
    shape = (n, reps, total)
    if scen.heavy_tails:
        z = rng.standard_t(T_DF, size=shape) / np.sqrt(T_DF / (T_DF - 2.0))
    else:
        z = rng.standard_normal(shape)
    phi = (users["phi"] if scen.autocorr else np.zeros(n))[:, None]
    sigma = users["sigma"][:, None]
    innov = np.sqrt(1.0 - phi ** 2)
    eps = np.empty(shape)
    eps[..., 0] = sigma * z[..., 0]
    for t in range(1, total):
        eps[..., t] = phi * eps[..., t - 1] + innov * sigma * z[..., t]
    eps = eps[..., BURN_IN:]

    weekly = 0.0
    if scen.weekly:
        dow = np.arange(N_DAYS)[None, None, :] + rng.integers(0, 7, size=(n, reps, 1))
        weekly = users["amp"][:, None, None] * np.cos(2.0 * np.pi * (dow - users["phase"][:, None, None]) / 7.0)
    if scen.additive:
        scale = (np.minimum(users["sigma"], ADDITIVE_SIGMA_CAP) / users["sigma"])[:, None, None]
        rel = 1.0 + eps * scale + weekly
        return users["mu"][:, None, None] * np.maximum(rel, ADDITIVE_FLOOR)
    return np.exp(np.log(users["mu"])[:, None, None] + eps + weekly)


def draw_onsets(n: int, reps: int, rng: np.random.Generator) -> np.ndarray:
    return rng.integers(ONSET_RANGE[0], ONSET_RANGE[1] + 1, size=(n, reps))


def baseline_sd(x: np.ndarray) -> np.ndarray:
    """Each series' own SD over the baseline window (days 0-27)."""
    return x[..., :BASE_DAYS].std(axis=-1, ddof=1)


def inject(x: np.ndarray, onset: np.ndarray, delta: np.ndarray) -> np.ndarray:
    """Subtract `delta` steps from `onset` to the end, floored at 0. delta, onset: (n, reps)."""
    t = np.arange(x.shape[-1])[None, None, :]
    after = t >= onset[..., None]
    return np.where(after, np.maximum(0.0, x - delta[..., None]), x)


def floor_fraction(x: np.ndarray, onset: np.ndarray, delta: np.ndarray) -> np.ndarray:
    """Per series: share of post-onset days where the shift hit the floor at 0."""
    t = np.arange(x.shape[-1])[None, None, :]
    after = t >= onset[..., None]
    hit = after & (x - delta[..., None] < 0.0)
    return hit.sum(-1) / after.sum(-1)


def variability_terciles(x: np.ndarray) -> np.ndarray:
    """Group per user (0 low, 1 mid, 2 high) from log-scale SD over the baseline window of replicate 0.
    Estimated from data, as it would be on real users (so groups are noisy)."""
    lsd = np.log(x[:, 0, :BASE_DAYS]).std(axis=-1, ddof=1)
    q1, q2 = np.quantile(lsd, [1.0 / 3.0, 2.0 / 3.0])
    return np.where(lsd <= q1, 0, np.where(lsd <= q2, 1, 2))
