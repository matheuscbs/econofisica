"""Biblioteca compartilhada do curso Econofísica (@mosscardoso)."""

from .artifacts import load_lab_npz, resolve_artifact_path, save_lab_npz
from .gbm import (
    gbm_ST_moments,
    gbm_ln_params,
    lognormal_pdf,
    simulate_gbm_paths,
    simulate_gbm_terminal,
)
from .options import call_payoff, naked_short_call_pnl, put_payoff

__all__ = [
    "gbm_ln_params",
    "gbm_ST_moments",
    "lognormal_pdf",
    "simulate_gbm_paths",
    "simulate_gbm_terminal",
    "call_payoff",
    "put_payoff",
    "naked_short_call_pnl",
    "save_lab_npz",
    "load_lab_npz",
    "resolve_artifact_path",
]

__version__ = "0.1.1"
