#!/usr/bin/env python3
"""
Lab M02.01 — GBM: parâmetros teóricos + convergência Monte Carlo.

Uso:
  pip install -e .
  python modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo/run_lab.py --plot
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from econofisica.bootstrap import ensure_src_on_path

ensure_src_on_path(Path(__file__).resolve())

from econofisica.artifacts import save_lab_npz  # noqa: E402
from econofisica.gbm import (  # noqa: E402
    gbm_ST_moments,
    gbm_ln_params,
    lognormal_pdf,
    simulate_gbm_paths,
    simulate_gbm_terminal,
)
from econofisica.labs import M02_GBM  # noqa: E402

CFG = M02_GBM
_ROOT = Path(__file__).resolve().parents[4]


def print_section(title: str) -> None:
    print()
    print("=" * 64)
    print(title)
    print("=" * 64)


def run_theory() -> tuple[float, float, float, float]:
    print_section("Passos 1–2 — Parâmetros e momentos teóricos")
    m, v = gbm_ln_params(CFG.S0, CFG.mu, CFG.sigma, CFG.T)
    mean_th, var_th = gbm_ST_moments(CFG.S0, CFG.mu, CFG.sigma, CFG.T)
    print(
        f"S0={CFG.S0}, μ={CFG.mu}, σ={CFG.sigma}, T={CFG.T}  "
        f"(SoT: econofisica.labs.M02_GBM)"
    )
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


def run_convergence(
    mean_th: float, var_th: float
) -> tuple[list[dict], np.ndarray, np.ndarray]:
    print_section("Passos 4–5 — Simulação GBM + convergência Monte Carlo")
    rows: list[dict] = []

    # Só S_T em chunks — sem matriz (N_max × nsteps) na RAM
    ST_full = simulate_gbm_terminal(
        CFG.S0,
        CFG.mu,
        CFG.sigma,
        CFG.T,
        CFG.nsteps,
        CFG.N_max,
        seed=CFG.seed,
        chunk_size=CFG.chunk_size,
    )
    # Paths só para plot (subamostra; mesma seed ⇒ primeiras linhas alinhadas)
    paths_plot = simulate_gbm_paths(
        CFG.S0,
        CFG.mu,
        CFG.sigma,
        CFG.T,
        CFG.nsteps,
        min(CFG.n_paths_plot, CFG.N_max),
        seed=CFG.seed,
    )

    header = (
        f"{'N':>10}  {'mean_emp':>12}  {'err_mean':>12}  "
        f"{'var_emp':>12}  {'err_var':>12}"
    )
    print(header)
    print("-" * len(header))

    for N in CFG.sample_sizes:
        ST = ST_full[:N]
        mean_emp = float(np.mean(ST))
        var_emp = float(np.var(ST, ddof=1))
        err_mean = abs(mean_emp - mean_th)
        err_var = abs(var_emp - var_th)
        rows.append(
            {
                "N": N,
                "mean_emp": mean_emp,
                "var_emp": var_emp,
                "err_mean": err_mean,
                "err_var": err_var,
            }
        )
        print(
            f"{N:>10,d}  {mean_emp:>12.6f}  {err_mean:>12.6f}  "
            f"{var_emp:>12.6f}  {err_var:>12.6f}"
        )

    print()
    print(f"Referência teórica → E[S_T]={mean_th:.6f}  Var(S_T)={var_th:.6f}")
    print("Esperado: err_mean e err_var tendem a cair conforme N cresce.")
    return rows, paths_plot, ST_full


def maybe_plot(
    m: float,
    v: float,
    mean_th: float,
    rows: list[dict],
    ST_full: np.ndarray,
    paths_plot: np.ndarray,
    out_dir: Path,
) -> None:
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    ST = ST_full
    t = np.linspace(0.0, CFG.T, CFG.nsteps + 1)
    n_show = paths_plot.shape[0]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(t, paths_plot.T, color="steelblue", alpha=0.25, lw=0.8)
    ax.plot(
        t, paths_plot.mean(axis=0), color="darkorange", lw=2, label="média amostral"
    )
    ax.axhline(mean_th, color="crimson", ls="--", lw=1.5, label="E[S_T] teórico")
    ax.set_xlabel("t")
    ax.set_ylabel("S_t")
    ax.set_title(f"GBM paths (mostrando {n_show}; MC usa N={CFG.N_max:,} só em S_T)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "gbm_paths.png", dpi=140)
    plt.close(fig)

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


def main() -> None:
    parser = argparse.ArgumentParser(description="Lab M02.01 — GBM Monte Carlo")
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--save-artifact", action="store_true", default=True)
    parser.add_argument("--no-save-artifact", action="store_false", dest="save_artifact")
    args = parser.parse_args()

    print("Lab 01 — GBM + Monte Carlo  |  @mosscardoso / econofisica")
    m, v, mean_th, var_th = run_theory()
    run_pdf_check(m, v)
    rows, paths_plot, ST_full = run_convergence(mean_th, var_th)

    out_dir = CFG.output_dir(_ROOT)
    if args.save_artifact:
        err_mean = np.array([r["err_mean"] for r in rows])
        err_var = np.array([r["err_var"] for r in rows])
        Ns = np.array(CFG.sample_sizes, dtype=int)
        art = save_lab_npz(
            CFG.artifact_path(_ROOT),
            ST=ST_full,
            paths_plot=paths_plot,
            sample_sizes=Ns,
            err_mean=err_mean,
            err_var=err_var,
            mean_th=np.array([mean_th]),
            var_th=np.array([var_th]),
            m=np.array([m]),
            v=np.array([v]),
        )
        print_section("Artifact")
        print(f"Salvo {art}  (Manim: ECONOFISICA_ARTIFACT={art})")

    if args.plot:
        maybe_plot(m, v, mean_th, rows, ST_full, paths_plot, out_dir)

    print()
    print("Done. Próximo: variar σ e observar a abertura do túnel.")


if __name__ == "__main__":
    main()
