"""SoT — Lab M01.02 vendedor de call sem hedge."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class M01VendedorConfig:
    S0: float = 100.0
    K: float = 100.0
    mu: float = 0.05
    sigma: float = 0.20
    T: float = 1.0
    nsteps: int = 252
    N: int = 1000
    premio: float = 7.0
    seed: int = 42
    output_rel: str = "outputs/lab-m01-vendedor-sem-hedge"
    artifact_name: str = "sim.npz"
    # paths só para visualização (resto usa terminal barato se N crescer)
    n_paths_plot: int = 120

    def output_dir(self, repo_root: Path) -> Path:
        return repo_root / self.output_rel

    def artifact_path(self, repo_root: Path) -> Path:
        return self.output_dir(repo_root) / self.artifact_name


M01_VENDEDOR = M01VendedorConfig()
