"""Golden tests — payoffs e P&L naked short."""

from __future__ import annotations

import numpy as np

from econofisica.options import call_payoff, naked_short_call_pnl, put_payoff


def test_call_payoff_nonnegative_and_otm():
    ST = np.array([80.0, 100.0, 120.0])
    pay = call_payoff(ST, 100.0)
    assert np.all(pay >= 0)
    assert pay[0] == 0.0 and pay[1] == 0.0 and pay[2] == 20.0


def test_put_payoff():
    ST = np.array([80.0, 100.0, 120.0])
    pay = put_payoff(ST, 100.0)
    assert pay[0] == 20.0 and pay[1] == 0.0 and pay[2] == 0.0


def test_naked_short_call_pnl_identity():
    ST = np.array([90.0, 110.0])
    premio = 7.0
    pnl = naked_short_call_pnl(ST, 100.0, premio)
    assert np.allclose(pnl, premio - call_payoff(ST, 100.0))
    assert pnl[0] == premio
    assert pnl[1] == premio - 10.0
