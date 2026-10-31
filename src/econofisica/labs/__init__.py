"""Configurações canônicas (SoT) por lab — importadas por run_lab e Manim."""

from .m01_vendedor_sem_hedge import M01_VENDEDOR, M01VendedorConfig
from .m02_gbm_monte_carlo import M02_GBM, M02GbmConfig

__all__ = [
    "M01VendedorConfig",
    "M01_VENDEDOR",
    "M02GbmConfig",
    "M02_GBM",
]
