"""SoT — Lab M02.01 GBM + convergência Monte Carlo."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class M02GbmConfig:
    S0: float = 100.0
    mu: float = 0.08
    sigma: float = 0.02
    T: float = 1.0
    nsteps: int = 252
    sample_sizes: tuple[int, ...] = (1_000, 10_000, 100_000)
    seed: int = 42
    # σ maior só para cena de túnel visual
    sigma_wide: float = 0.20
    output_rel: str = "outputs/lab01-gbm"
    artifact_name: str = "sim.npz"
    n_paths_plot: int = 80
    chunk_size: int = 10_000

    def output_dir(self, repo_root: Path) -> Path:
        return repo_root / self.output_rel

    def artifact_path(self, repo_root: Path) -> Path:
        return self.output_dir(repo_root) / self.artifact_name

    @property
    def N_max(self) -> int:
        return max(self.sample_sizes)


M02_GBM = M02GbmConfig()
