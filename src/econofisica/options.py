"""Payoffs e P&L de opções vanila (sem modelo de precificação)."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def call_payoff(ST: NDArray[np.floating] | float, K: float) -> NDArray[np.floating]:
    """Payoff de call europeia: max(S_T − K, 0)."""
    return np.maximum(np.asarray(ST, dtype=float) - K, 0.0)


def put_payoff(ST: NDArray[np.floating] | float, K: float) -> NDArray[np.floating]:
    """Payoff de put europeia: max(K − S_T, 0)."""
    return np.maximum(K - np.asarray(ST, dtype=float), 0.0)


def naked_short_call_pnl(
    ST: NDArray[np.floating] | float,
    K: float,
    premium: float,
) -> NDArray[np.floating]:
    """
    P&L do vendedor de call sem hedge (wait-and-see).

    No t=0 recebe `premium`; em T paga max(S_T − K, 0).
    pnl = premium − payoff
    """
    return float(premium) - call_payoff(ST, K)
