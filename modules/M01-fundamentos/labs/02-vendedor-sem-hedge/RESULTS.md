# Lab M01.01 — Leitura dos resultados

Parâmetros: \(S_0=K=100\), \(\mu=0.05\), \(\sigma=0.20\), \(T=1\), 252 passos, \(N=1000\), prêmio \(=7\), `seed=42`.

## Números desta seed

| Métrica | Valor |
|---------|------:|
| \(\mathbb{E}[S_T]\) amostral | ≈ 105.1 |
| \(\mathbb{E}[\text{payoff}]\) | ≈ **11.0** |
| \(P(S_T>K)\) | ≈ 55.5% |
| \(\mathbb{E}[\text{pnl}]\) vendedor | ≈ **−4.0** |
| melhor pnl | +7.0 (call OTM) |
| pior pnl | ≈ **−82** (\(S_T\approx 189\)) |
| VaR 5% | ≈ −37 |
| CVaR 5% | ≈ −51 |
| \(P(\text{pnl}<0)\) | ≈ 42% |

## O que isso ensina

1. **Prêmio 7 é barato** frente ao payoff médio ~11 sob este \(\mu,\sigma\) — o vendedor *naked* já tem esperança negativa nesta medida “real”.  
2. Mesmo se você subir o prêmio até empatar a média, a **forma** do P&L continua ruim: lucro limitado em +prêmio, perdas lineares quando \(S_T\to\infty\).  
3. Por isso o mercado não “espera”: precifica sob **Q** (BSM) e **hedgeia** (delta). Wait-and-see não é replicação.

## Figuras

`outputs/lab-m01-vendedor-sem-hedge/`

- `naked_seller_paths.png` — ITM (vermelho) vs OTM (azul)  
- `naked_seller_pnl_hist.png` — pico em +7 e cauda à esquerda  
- `naked_seller_ST_vs_pnl.png` — knick em \(K\): plano depois queda  

## Experimento rápido

Troque `PREMIO = 12.0` em `run_lab.py`: a média do pnl sobe, mas VaR/CVaR e a cauda continuam o argumento contra wait-and-see.
