#!/usr/bin/env python3
"""
Lab 01 — GBM: parâmetros teóricos + convergência Monte Carlo.

Uso (raiz do repo):
  PYTHONPATH=src python modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo/run_lab.py
  PYTHONPATH=src python .../run_lab.py --plot
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

# Permite rodar sem instalar o pacote se PYTHONPATH=src não estiver setado.
_ROOT = Path(__file__).resolve().parents[4]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from econofisica.gbm import (  # noqa: E402
    gbm_ST_moments,
    gbm_ln_params,
    lognormal_pdf,
    simulate_gbm_paths,
)

# --- Parâmetros globais do lab ---
S0 = 100.0
MU = 0.08
SIGMA = 0.02
T = 1.0
NSTEPS = 252
SAMPLE_SIZES = (1_000, 10_000, 100_000)
SEED = 42


def print_section(title: str) -> None:
    print()
    print("=" * 64)
    print(title)
    print("=" * 64)


def run_theory() -> tuple[float, float, float, float]:
    print_section("Passos 1–2 — Parâmetros e momentos teóricos")
    m, v = gbm_ln_params(S0, MU, SIGMA, T)
    mean_th, var_th = gbm_ST_moments(S0, MU, SIGMA, T)

    print(f"S0={S0}, μ={MU}, σ={SIGMA}, T={T}")
    print(f"log-preço:  m = {m:.8f}")
    print(f"            v = {v:.8f}  (std = {np.sqrt(v):.8f})")
    print(f"S_T:        E[S_T]   = {mean_th:.8f}")
    print(f"            Var(S_T) = {var_th:.8f}")
    return m, v, mean_th, var_th


def run_pdf_check(m: float, v: float) -> None:
    print_section("Passo 3 — Densidade log-normal (amostra de pontos)")
    s_grid = np.array([80.0, 100.0, 108.0, 120.0, -1.0])
    pdf = lognormal_pdf(s_grid, m, v)
    for s, p in zip(s_grid, pdf):
        print(f"  pdf({s:7.1f}) = {p:.8e}")


def run_convergence(mean_th: float, var_th: float) -> list[dict]:
    print_section("Passos 4–5 — Simulação GBM + convergência Monte Carlo")
    rows: list[dict] = []

    # Uma simulação com N máximo; subamostras aninhadas deixam a LLN mais legível.
    N_max = max(SAMPLE_SIZES)
    paths_full = simulate_gbm_paths(
        S0, MU, SIGMA, T, NSTEPS, N_max, seed=SEED
    )
    ST_full = paths_full[:, -1]

    header = (
        f"{'N':>10}  {'mean_emp':>12}  {'err_mean':>12}  "
        f"{'var_emp':>12}  {'err_var':>12}"
    )
    print(header)
    print("-" * len(header))

    for N in SAMPLE_SIZES:
        ST = ST_full[:N]
        mean_emp = float(np.mean(ST))
        var_emp = float(np.var(ST, ddof=1))
        err_mean = abs(mean_emp - mean_th)
        err_var = abs(var_emp - var_th)
        row = {
            "N": N,
            "mean_emp": mean_emp,
            "var_emp": var_emp,
            "err_mean": err_mean,
            "err_var": err_var,
            "paths": paths_full[:N],
        }
        rows.append(row)
        print(
            f"{N:>10,d}  {mean_emp:>12.6f}  {err_mean:>12.6f}  "
            f"{var_emp:>12.6f}  {err_var:>12.6f}"
        )

    print()
    print(f"Referência teórica → E[S_T]={mean_th:.6f}  Var(S_T)={var_th:.6f}")
    print("Esperado: err_mean e err_var tendem a cair conforme N cresce.")
    return rows


def maybe_plot(
    m: float, v: float, mean_th: float, rows: list[dict], out_dir: Path
) -> None:
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    best = rows[-1]
    paths = best["paths"]
    ST = paths[:, -1]

    # Trajetórias (subamostra)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    t = np.linspace(0.0, T, NSTEPS + 1)
    n_show = min(80, paths.shape[0])
    ax.plot(t, paths[:n_show].T, color="steelblue", alpha=0.25, lw=0.8)
    ax.plot(t, paths[:n_show].mean(axis=0), color="darkorange", lw=2, label="média amostral")
    ax.axhline(mean_th, color="crimson", ls="--", lw=1.5, label="E[S_T] teórico")
    ax.set_xlabel("t")
    ax.set_ylabel("S_t")
    ax.set_title(f"GBM paths (mostrando {n_show} de N={best['N']:,})")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "gbm_paths.png", dpi=140)
    plt.close(fig)

    # Histograma S_T vs pdf teórica
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(ST, bins=60, density=True, alpha=0.55, color="steelblue", label="histograma S_T")
    s_grid = np.linspace(max(ST.min() * 0.98, 1e-6), ST.max() * 1.02, 400)
    ax.plot(s_grid, lognormal_pdf(s_grid, m, v), color="crimson", lw=2, label="pdf teórica")
    ax.set_xlabel("S_T")
    ax.set_ylabel("densidade")
    ax.set_title("Distribuição terminal vs log-normal teórica")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "gbm_ST_density.png", dpi=140)
    plt.close(fig)

    # Erro vs N
    fig, ax = plt.subplots(figsize=(7, 4))
    Ns = [r["N"] for r in rows]
    ax.loglog(Ns, [r["err_mean"] for r in rows], "o-", label="|mean − E[S_T]|")
    ax.loglog(Ns, [r["err_var"] for r in rows], "s-", label="|var − Var(S_T)|")
    ax.set_xlabel("N")
    ax.set_ylabel("erro absoluto")
    ax.set_title("Convergência Monte Carlo")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_dir / "gbm_mc_convergence.png", dpi=140)
    plt.close(fig)

    print_section("Figuras")
    print(f"Salvas em {out_dir}/")
    for name in ("gbm_paths.png", "gbm_ST_density.png", "gbm_mc_convergence.png"):
        print(f"  · {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Lab 01 — GBM Monte Carlo")
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Gera figuras em outputs/lab01-gbm/",
    )
    args = parser.parse_args()

    print("Lab 01 — GBM + Monte Carlo  |  @mosscardoso / econofisica")
    m, v, mean_th, var_th = run_theory()
    run_pdf_check(m, v)
    rows = run_convergence(mean_th, var_th)

    if args.plot:
        maybe_plot(m, v, mean_th, rows, _ROOT / "outputs" / "lab01-gbm")

    print()
    print("Done. Próximo: variar σ e observar a abertura do túnel.")


if __name__ == "__main__":
    main()
