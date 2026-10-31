# Lab 01 (M01) — Vendedor de call sem hedge (*wait-and-see*)

**Módulo:** M01 · Fundamentos  
**Aulas:** M01.A02 (preço mínimo) · M01.A03 (delta neutro)  
**Nível:** introdutório  
**Tempo:** ~25–40 min

## Objetivo

Simular \(S_t\) via GBM, calcular o payoff de uma **call europeia** no vencimento e mostrar a distribuição de P&L do **vendedor sem hedge** — a cauda de perdas quando \(S_T \gg K\).

Mensagem: cobrar um prêmio fixo e “esperar” não é estratégia. Sem replicação/hedge, a exposição é assimétrica e potencialmente ilimitada.

## Modelo

$$
S_{t+\Delta t} = S_t \exp\Bigl(\bigl(\mu-\tfrac12\sigma^2\bigr)\Delta t + \sigma\sqrt{\Delta t}\, Z_t\Bigr),\quad Z_t\sim\mathcal{N}(0,1)
$$

Payoff da call: \(\max(S_T-K,0)\).  
P&L do vendedor naked: \(\text{pnl} = \text{prêmio} - \max(S_T-K,0)\).

## Parâmetros padrão

| Símbolo | Valor | Nota |
|---------|------:|------|
| \(S_0\) | 100 | spot inicial |
| \(K\) | 100 | ATM |
| \(\mu\) | 0.05 | drift (mundo “real”, não Q) |
| \(\sigma\) | 0.20 | vol 20% |
| \(T\) | 1.0 | 1 ano |
| `nsteps` | 252 | passos |
| `N` | 1000 | trajetórias |
| `prêmio` | 7.0 | prêmio fixo ilustrativo (não é BSM) |
| `seed` | 42 | reprodutibilidade |

> O prêmio 7.0 é **didático**. No lab seguinte (BSM) você compara com o preço justo risco-neutro.

## Como rodar

```bash
# na raiz do repo
source .venv/bin/activate   # se já criou
pip install -r requirements.txt
PYTHONPATH=src python modules/M01-fundamentos/labs/01-vendedor-sem-hedge/run_lab.py --plot
```

Manim:

```bash
export PYTHONPATH=src
manim -pql modules/M01-fundamentos/labs/01-vendedor-sem-hedge/manim/scenes.py NakedSellerPnLScene
manim -pql modules/M01-fundamentos/labs/01-vendedor-sem-hedge/manim/scenes.py PathsByMoneynessScene
```

## O que observar

1. Muitas trajetórias: vendedor fica com \(+\text{prêmio}\) (call expira OTM).  
2. Poucas trajetórias: \(S_T\) sobe → payoff explode → **pnl fortemente negativo**.  
3. Média amostral do pnl pode ser positiva *nesta* amostra, mas o **risco de cauda** (VaR / worst loss) é o ponto pedagógico — não o lucro médio.

## Arquivos

- `run_lab.py` — simulação + histograma  
- `RESULTS.md` — leitura dos números  
- `manim/scenes.py` — animações  
- Código: `src/econofisica/gbm.py`, `src/econofisica/options.py`

## Próximo

Lab de **delta hedge dinâmico**: mesmo GBM, rebalancear Δ e comparar a distribuição residual com a naked short.
