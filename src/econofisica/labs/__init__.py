"""Configurações canônicas (SoT) por lab — importadas por run_lab e Manim."""

from .m01_gbm_monte_carlo import M01_GBM, M01GbmConfig
from .m01_vendedor_sem_hedge import M01_VENDEDOR, M01VendedorConfig

__all__ = [
    "M01GbmConfig",
    "M01_GBM",
    "M01VendedorConfig",
    "M01_VENDEDOR",
]
