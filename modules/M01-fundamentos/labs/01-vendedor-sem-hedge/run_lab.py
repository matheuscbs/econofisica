#!/usr/bin/env python3
"""
Lab M01.01 — Vendedor de call sem hedge (wait-and-see).

Uso (raiz do repo):
  pip install -e .
  python modules/M01-fundamentos/labs/01-vendedor-sem-hedge/run_lab.py --plot
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from econofisica.bootstrap import ensure_src_on_path

ensure_src_on_path(Path(__file__).resolve())

from econofisica.artifacts import save_lab_npz  # noqa: E402
from econofisica.gbm import simulate_gbm_paths, simulate_gbm_terminal  # noqa: E402
from econofisica.labs import M01_VENDEDOR  # noqa: E402
from econofisica.options import call_payoff, naked_short_call_pnl  # noqa: E402

CFG = M01_VENDEDOR
_ROOT = Path(__file__).resolve().parents[4]


def print_section(title: str) -> None:
    print()
    print("=" * 64)
    print(title)
    print("=" * 64)


def simulate() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Trajetórias (plot), S_T, payoffs, pnl."""
    # Paths só para visual (N típico=1000); S_T via terminal API (mesma seed ⇒ alinhado).
    paths = simulate_gbm_paths(
        CFG.S0, CFG.mu, CFG.sigma, CFG.T, CFG.nsteps, CFG.N, seed=CFG.seed
    )
    ST = simulate_gbm_terminal(
        CFG.S0, CFG.mu, CFG.sigma, CFG.T, CFG.nsteps, CFG.N, seed=CFG.seed
    )
    # invariante SoT: terminal == última coluna
    if not np.allclose(ST, paths[:, -1]):
        raise RuntimeError("simulate_gbm_terminal divergiu de paths[:, -1]")
    payoffs = call_payoff(ST, CFG.K)
    pnl = naked_short_call_pnl(ST, CFG.K, CFG.premio)
    return paths, ST, payoffs, pnl


def report(ST: np.ndarray, payoffs: np.ndarray, pnl: np.ndarray) -> None:
    print_section("Passo 1 — Parâmetros (SoT: econofisica.labs.M01_VENDEDOR)")
    print(
        f"S0={CFG.S0}, K={CFG.K}, μ={CFG.mu}, σ={CFG.sigma}, T={CFG.T}, "
        f"nsteps={CFG.nsteps}, N={CFG.N}, prêmio={CFG.premio}, seed={CFG.seed}"
    )

    print_section("Passo 2–3 — S_T e payoff da call")
    print(f"E[S_T] amostral     = {ST.mean():.4f}")
    print(f"std(S_T) amostral   = {ST.std(ddof=1):.4f}")
    print(f"min / max S_T       = {ST.min():.2f} / {ST.max():.2f}")
    print(f"E[payoff] amostral  = {payoffs.mean():.4f}")
    print(f"P(ITM) = P(S_T>K)   = {(ST > CFG.K).mean():.3f}")

    print_section("Passo 4 — P&L do vendedor sem hedge")
    print("pnl = prêmio − max(S_T−K, 0)")
    print(f"E[pnl] amostral     = {pnl.mean():.4f}")
    print(f"std(pnl)            = {pnl.std(ddof=1):.4f}")
    print(f"pior perda (min)    = {pnl.min():.4f}")
    print(f"melhor resultado    = {pnl.max():.4f}")
    var05 = float(np.quantile(pnl, 0.05))
    cvar05 = float(pnl[pnl <= var05].mean()) if np.any(pnl <= var05) else var05
    print(f"VaR 5% (pnl)        = {var05:.4f}")
    print(f"CVaR 5% (pnl)       = {cvar05:.4f}")
    print(f"P(pnl < 0)          = {(pnl < 0).mean():.3f}")
    print()
    print(
        "Leitura: com prêmio ilustrativo "
        f"{CFG.premio} vs E[payoff] amostral ≈ {payoffs.mean():.1f}, "
        "o vendedor já perde na média — e a cauda (S_T ≫ K) piora o risco."
    )


def maybe_plot(
    paths: np.ndarray, ST: np.ndarray, pnl: np.ndarray, out_dir: Path
) -> None:
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    t = np.linspace(0.0, CFG.T, CFG.nsteps + 1)
    itm = ST > CFG.K
    n_show = min(CFG.n_paths_plot, paths.shape[0])

    fig, ax = plt.subplots(figsize=(9, 4.8))
    for i in range(n_show):
        color = "#e85d5d" if itm[i] else "#3d9cf0"
        ax.plot(t, paths[i], color=color, alpha=0.35, lw=0.9)
    ax.axhline(CFG.K, color="#f0a03d", ls="--", lw=1.5, label=f"K={CFG.K:.0f}")
    ax.plot([], [], color="#e85d5d", alpha=0.8, label="termina ITM (S_T>K)")
    ax.plot([], [], color="#3d9cf0", alpha=0.8, label="termina OTM/ATM")
    ax.set_xlabel("t")
    ax.set_ylabel("S_t")
    ax.set_title(f"GBM paths (N={CFG.N}, mostrando {n_show})")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(out_dir / "naked_seller_paths.png", dpi=140)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.hist(pnl, bins=40, color="#5b6b7a", edgecolor="white", alpha=0.9)
    ax.axvline(0.0, color="#e85d5d", ls="-", lw=1.8, label="pnl = 0")
    ax.axvline(
        CFG.premio, color="#3d9cf0", ls="--", lw=1.5, label=f"só prêmio (+{CFG.premio})"
    )
    ax.axvline(
        pnl.mean(), color="#f0a03d", ls=":", lw=1.8, label=f"média={pnl.mean():.2f}"
    )
    ax.set_xlabel("P&L do vendedor (prêmio − payoff)")
    ax.set_ylabel("frequência")
    ax.set_title("Distribuição do vendedor sem hedge — cauda de perdas")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "naked_seller_pnl_hist.png", dpi=140)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(ST, pnl, s=12, alpha=0.45, c=np.where(itm, "#e85d5d", "#3d9cf0"))
    ax.axhline(0.0, color="black", lw=0.8)
    ax.axvline(CFG.K, color="#f0a03d", ls="--", lw=1.2)
    ax.set_xlabel("S_T")
    ax.set_ylabel("pnl vendedor")
    ax.set_title("Payoff linear negativo acima de K")
    fig.tight_layout()
    fig.savefig(out_dir / "naked_seller_ST_vs_pnl.png", dpi=140)
    plt.close(fig)

    print_section("Figuras")
    print(f"Salvas em {out_dir}/")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lab M01.01 — vendedor de call sem hedge"
    )
    parser.add_argument("--plot", action="store_true")
    parser.add_argument(
        "--save-artifact",
        action="store_true",
        default=True,
        help="Salva sim.npz para Manim (default: on)",
    )
    parser.add_argument(
        "--no-save-artifact",
        action="store_false",
        dest="save_artifact",
    )
    args = parser.parse_args()

    print("Lab M01.01 — Vendedor sem hedge  |  @mosscardoso / econofisica")
    paths, ST, payoffs, pnl = simulate()
    report(ST, payoffs, pnl)

    out_dir = CFG.output_dir(_ROOT)
    if args.save_artifact:
        art = save_lab_npz(
            CFG.artifact_path(_ROOT),
            paths=paths,
            ST=ST,
            payoffs=payoffs,
            pnl=pnl,
            meta=np.array(
                [CFG.S0, CFG.K, CFG.mu, CFG.sigma, CFG.T, CFG.nsteps, CFG.premio, CFG.seed],
                dtype=float,
            ),
        )
        print_section("Artifact")
        print(f"Salvo {art}  (Manim: ECONOFISICA_ARTIFACT={art})")

    if args.plot:
        maybe_plot(paths, ST, pnl, out_dir)

    print()
    print("Done. Próximo: delta hedge dinâmico no mesmo GBM.")


if __name__ == "__main__":
    main()
