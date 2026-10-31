"""Golden tests — momentos fechados e alinhamento paths ↔ terminal."""

from __future__ import annotations

import numpy as np

from econofisica.gbm import (
    gbm_ST_moments,
    gbm_ln_params,
    lognormal_pdf,
    simulate_gbm_paths,
    simulate_gbm_terminal,
)


def test_gbm_ln_params_closed_form():
    m, v = gbm_ln_params(100.0, 0.08, 0.02, 1.0)
    assert abs(m - (np.log(100.0) + (0.08 - 0.5 * 0.02**2) * 1.0)) < 1e-12
    assert abs(v - 0.02**2) < 1e-12


def test_gbm_ST_moments_closed_form():
    mean, var = gbm_ST_moments(100.0, 0.08, 0.02, 1.0)
    mean_ref = 100.0 * np.exp(0.08)
    var_ref = 100.0**2 * np.exp(2 * 0.08) * (np.exp(0.02**2) - 1.0)
    assert abs(mean - mean_ref) < 1e-12
    assert abs(var - var_ref) < 1e-12


def test_lognormal_pdf_mask_and_peak():
    m, v = gbm_ln_params(100.0, 0.08, 0.02, 1.0)
    s = np.array([-1.0, 0.0, 108.0])
    pdf = lognormal_pdf(s, m, v)
    assert pdf[0] == 0.0 and pdf[1] == 0.0
    assert pdf[2] > 0.0


def test_terminal_matches_paths_last_column():
    S0, mu, sigma, T, nsteps, N, seed = 100.0, 0.05, 0.2, 1.0, 252, 500, 42
    paths = simulate_gbm_paths(S0, mu, sigma, T, nsteps, N, seed=seed)
    ST = simulate_gbm_terminal(
        S0, mu, sigma, T, nsteps, N, seed=seed, chunk_size=128
    )
    assert np.allclose(ST, paths[:, -1])


def test_terminal_chunk_invariant():
    kwargs = dict(S0=100.0, mu=0.08, sigma=0.02, T=1.0, nsteps=52, N=300, seed=7)
    a = simulate_gbm_terminal(**kwargs, chunk_size=300)
    b = simulate_gbm_terminal(**kwargs, chunk_size=50)
    assert np.allclose(a, b)
