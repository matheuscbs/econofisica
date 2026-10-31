#!/usr/bin/env python3
"""
Lab M01.01 — Vendedor de call sem hedge (wait-and-see).

Uso (raiz do repo):
  PYTHONPATH=src python modules/M01-fundamentos/labs/01-vendedor-sem-hedge/run_lab.py
  PYTHONPATH=src python .../run_lab.py --plot
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

_ROOT = Path(__file__).resolve().parents[4]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from econofisica.gbm import simulate_gbm_paths  # noqa: E402
from econofisica.options import call_payoff, naked_short_call_pnl  # noqa: E402

# --- Passo 1: parâmetros ---
S0 = 100.0
K = 100.0
MU = 0.05
SIGMA = 0.20
T = 1.0
NSTEPS = 252
NUM_SIMULACOES = 1000
PREMIO = 7.0
SEED = 42


def print_section(title: str) -> None:
    print()
    print("=" * 64)
    print(title)
    print("=" * 64)


def simulate() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Passos 2–4: trajetórias GBM, S_T, payoffs, pnl do vendedor.

    Retorna paths (N, nsteps+1), ST, payoffs, pnl_vendedor.
    """
    # Biblioteca: (num_paths, nsteps+1) — equivalente à matriz (N, num_sim) do enunciado
    # após transpor os incrementos; mesma dinâmica discreta do GBM.
    paths = simulate_gbm_paths(
        S0, MU, SIGMA, T, NSTEPS, NUM_SIMULACOES, seed=SEED
    )
    ST = paths[:, -1]
    payoffs = call_payoff(ST, K)
    pnl = naked_short_call_pnl(ST, K, PREMIO)
    return paths, ST, payoffs, pnl


def report(ST: np.ndarray, payoffs: np.ndarray, pnl: np.ndarray) -> None:
    print_section("Passo 1 — Parâmetros")
    print(
        f"S0={S0}, K={K}, μ={MU}, σ={SIGMA}, T={T}, "
        f"nsteps={NSTEPS}, N={NUM_SIMULACOES}, prêmio={PREMIO}"
    )

    print_section("Passo 2–3 — S_T e payoff da call")
    print(f"E[S_T] amostral     = {ST.mean():.4f}")
    print(f"std(S_T) amostral   = {ST.std(ddof=1):.4f}")
    print(f"min / max S_T       = {ST.min():.2f} / {ST.max():.2f}")
    print(f"E[payoff] amostral  = {payoffs.mean():.4f}")
    print(f"P(ITM) = P(S_T>K)   = {(ST > K).mean():.3f}")

    print_section("Passo 4 — P&L do vendedor sem hedge")
    print(f"pnl = prêmio − max(S_T−K, 0)")
    print(f"E[pnl] amostral     = {pnl.mean():.4f}")
    print(f"std(pnl)            = {pnl.std(ddof=1):.4f}")
    print(f"pior perda (min)    = {pnl.min():.4f}")
    print(f"melhor resultado    = {pnl.max():.4f}")
    # VaR empírico 5% (lado esquerdo = perdas do vendedor)
    var05 = float(np.quantile(pnl, 0.05))
    cvar05 = float(pnl[pnl <= var05].mean()) if np.any(pnl <= var05) else var05
    print(f"VaR 5% (pnl)        = {var05:.4f}")
    print(f"CVaR 5% (pnl)       = {cvar05:.4f}")
    frac_loss = float((pnl < 0).mean())
    print(f"P(pnl < 0)          = {frac_loss:.3f}")
    print()
    print(
        "Leitura: com prêmio ilustrativo 7 vs E[payoff] amostral ≈ "
        f"{payoffs.mean():.1f}, o vendedor já perde na média — "
        "e a cauda (S_T ≫ K) piora o risco. Precisa de hedge / preço justo."
    )


def maybe_plot(
    paths: np.ndarray, ST: np.ndarray, pnl: np.ndarray, out_dir: Path
) -> None:
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    t = np.linspace(0.0, T, NSTEPS + 1)
    itm = ST > K

    # Trajetórias coloridas por moneyness terminal
    fig, ax = plt.subplots(figsize=(9, 4.8))
    n_show = min(120, paths.shape[0])
    idx = np.arange(n_show)
    for i in idx:
        color = "#e85d5d" if itm[i] else "#3d9cf0"
        ax.plot(t, paths[i], color=color, alpha=0.35, lw=0.9)
    ax.axhline(K, color="#f0a03d", ls="--", lw=1.5, label=f"K={K:.0f}")
    ax.plot([], [], color="#e85d5d", alpha=0.8, label="termina ITM (S_T>K)")
    ax.plot([], [], color="#3d9cf0", alpha=0.8, label="termina OTM/ATM")
    ax.set_xlabel("t")
    ax.set_ylabel("S_t")
    ax.set_title(f"GBM paths (N={NUM_SIMULACOES}, mostrando {n_show})")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(out_dir / "naked_seller_paths.png", dpi=140)
    plt.close(fig)

    # Histograma do P&L do vendedor
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.hist(pnl, bins=40, color="#5b6b7a", edgecolor="white", alpha=0.9)
    ax.axvline(0.0, color="#e85d5d", ls="-", lw=1.8, label="pnl = 0")
    ax.axvline(PREMIO, color="#3d9cf0", ls="--", lw=1.5, label=f"só prêmio (+{PREMIO})")
    ax.axvline(pnl.mean(), color="#f0a03d", ls=":", lw=1.8, label=f"média={pnl.mean():.2f}")
    ax.set_xlabel("P&L do vendedor (prêmio − payoff)")
    ax.set_ylabel("frequência")
    ax.set_title("Distribuição do vendedor sem hedge — cauda de perdas")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "naked_seller_pnl_hist.png", dpi=140)
    plt.close(fig)

    # Scatter S_T vs pnl
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(ST, pnl, s=12, alpha=0.45, c=np.where(itm, "#e85d5d", "#3d9cf0"))
    ax.axhline(0.0, color="black", lw=0.8)
    ax.axvline(K, color="#f0a03d", ls="--", lw=1.2)
    ax.set_xlabel("S_T")
    ax.set_ylabel("pnl vendedor")
    ax.set_title("Payoff linear negativo acima de K")
    fig.tight_layout()
    fig.savefig(out_dir / "naked_seller_ST_vs_pnl.png", dpi=140)
    plt.close(fig)

    print_section("Figuras")
    print(f"Salvas em {out_dir}/")
    for name in (
        "naked_seller_paths.png",
        "naked_seller_pnl_hist.png",
        "naked_seller_ST_vs_pnl.png",
    ):
        print(f"  · {name}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lab M01.01 — vendedor de call sem hedge"
    )
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()

    print("Lab M01.01 — Vendedor sem hedge  |  @mosscardoso / econofisica")
    paths, ST, payoffs, pnl = simulate()
    report(ST, payoffs, pnl)

    if args.plot:
        maybe_plot(paths, ST, pnl, _ROOT / "outputs" / "lab-m01-vendedor-sem-hedge")

    print()
    print("Done. Próximo: delta hedge dinâmico no mesmo GBM.")


if __name__ == "__main__":
    main()
