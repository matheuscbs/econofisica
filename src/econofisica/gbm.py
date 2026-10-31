"""
Geometric Brownian Motion — parâmetros teóricos, densidade e simulação.

Sob o SDE
    dS = μ S dt + σ S dW,
o log-preço X_T = ln S_T é gaussiano e S_T é log-normal.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def gbm_ln_params(
    S0: float, mu: float, sigma: float, T: float
) -> tuple[float, float]:
    """
    Média m e variância v do log-preço X_T = ln S_T.

    m = ln(S0) + (μ − ½ σ²) T
    v = σ² T
    """
    m = np.log(S0) + (mu - 0.5 * sigma**2) * T
    v = sigma**2 * T
    return float(m), float(v)


def gbm_ST_moments(
    S0: float, mu: float, sigma: float, T: float
) -> tuple[float, float]:
    """
    Momentos fechados de S_T (log-normal).

    E[S_T] = S0 · exp(μ T)
    Var(S_T) = S0² · exp(2 μ T) · (exp(σ² T) − 1)
    """
    mean = S0 * np.exp(mu * T)
    var = (S0**2) * np.exp(2.0 * mu * T) * (np.exp(sigma**2 * T) - 1.0)
    return float(mean), float(var)


def lognormal_pdf(
    s: NDArray[np.floating] | float, m: float, v: float
) -> NDArray[np.floating]:
    """
    Densidade log-normal de S com parâmetros (m, v) do log.

    pdf(s) = 1 / (s √(2π v)) · exp( −(ln s − m)² / (2v) ),  s > 0
    """
    s_arr = np.asarray(s, dtype=float)
    pdf = np.zeros_like(s_arr, dtype=float)
    mask = s_arr > 0.0
    if not np.any(mask):
        return pdf

    s_pos = s_arr[mask]
    pdf[mask] = (1.0 / (s_pos * np.sqrt(2.0 * np.pi * v))) * np.exp(
        -((np.log(s_pos) - m) ** 2) / (2.0 * v)
    )
    return pdf


def simulate_gbm_paths(
    S0: float,
    mu: float,
    sigma: float,
    T: float,
    nsteps: int,
    N: int,
    seed: int = 42,
) -> NDArray[np.floating]:
    """
    Simula N trajetórias discretas do GBM com nsteps passos.

    ΔX = (μ − ½ σ²) dt + σ √dt · Z,  Z ~ N(0,1)
    S_{t_k} = S0 · exp(∑_{j=1}^k ΔX_j)

    Retorna matriz (N, nsteps + 1) com S0 na coluna 0.
    """
    if nsteps < 1:
        raise ValueError("nsteps must be >= 1")
    if N < 1:
        raise ValueError("N must be >= 1")
    if T <= 0:
        raise ValueError("T must be > 0")

    rng = np.random.default_rng(seed)
    dt = T / nsteps
    Z = rng.standard_normal(size=(N, nsteps))
    dX = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
    X = np.cumsum(dX, axis=1)
    S = S0 * np.exp(X)
    S0_col = np.full((N, 1), S0, dtype=float)
    return np.hstack([S0_col, S])
