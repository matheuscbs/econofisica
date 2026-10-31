# Lab 01 (M01) — GBM: parâmetros teóricos e convergência Monte Carlo

**Módulo:** M01 · Fundamentos  
**Aula:** [M01.A02](../../lessons/A02-preco-minimo-de-uma-opcao-o-que-o-mercado-nao-pode-deixar-de-pagar.md) — dinâmica mínima (GBM)  
**Nível:** introdutório  
**Tempo:** ~30–45 min

## Objetivo

Implementar o GBM de ponta a ponta: parâmetros do log-preço → momentos fechados de \(S_T\) → densidade log-normal → simulação de trajetórias → **teste de convergência** Monte Carlo.

## Pré-requisitos

- Python 3.10+, NumPy  
- Noção de esperança/variância e de \(S_T = S_0 e^{X_T}\)

## Modelo

$$
dS_t = \mu S_t\, dt + \sigma S_t\, dW_t
$$

O log-preço \(X_T = \ln S_T\) é gaussiano:

$$
m = \ln S_0 + \bigl(\mu - \tfrac12\sigma^2\bigr)T, \qquad
v = \sigma^2 T
$$

Momentos de \(S_T\) (log-normal):

$$
\mathbb{E}[S_T] = S_0 e^{\mu T}, \qquad
\mathrm{Var}(S_T) = S_0^2 e^{2\mu T}\bigl(e^{\sigma^2 T} - 1\bigr)
$$

Discretização Euler–Maruyama no log:

$$
\Delta X = \bigl(\mu - \tfrac12\sigma^2\bigr)dt + \sigma\sqrt{dt}\, Z, \quad Z\sim\mathcal{N}(0,1)
$$

$$
S_{t_k} = S_0 \exp\Bigl(\sum_{j=1}^{k}\Delta X_j\Bigr)
$$

## Passos do lab

| Passo | Função | O que faz |
|-------|--------|-----------|
| 1 | `gbm_ln_params` | \(m\), \(v\) do log-preço |
| 2 | `gbm_ST_moments` | média e variância teóricas de \(S_T\) |
| 3 | `lognormal_pdf` | densidade teórica (máscara \(s>0\)) |
| 4 | `simulate_gbm_paths` | \(N\) trajetórias, `nsteps` passos |
| 5 | convergência MC | \(N\in\{10^3,10^4,10^5\}\) vs teoria |

## Parâmetros padrão

| Símbolo | Valor | Nota |
|---------|-------|------|
| \(S_0\) | 100 | preço inicial |
| \(\mu\) | 0.08 | drift anual |
| \(\sigma\) | 0.02 | vol anual (baixa — túnel estreito) |
| \(T\) | 1.0 | horizonte 1 ano |
| `nsteps` | 252 | dias úteis |
| `seed` | 42 | reprodutibilidade |

> Com \(\sigma=0.02\) a dispersão é pequena (bom para ver convergência limpa). Experimente \(\sigma=0.20\) para um túnel mais “equity-like”.

## Como rodar

```bash
pip install -e ".[dev,manim]"
python modules/M01-fundamentos/labs/01-gbm-monte-carlo/run_lab.py --plot
# S_T via simulate_gbm_terminal (chunks); sim.npz para Manim
# SoT: econofisica.labs.M01_GBM
```

## O que observar

1. Erro absoluto da média e da variância **cai** com \(N\) (lei dos grandes números).  
2. Histograma de \(S_T\) se aproxima da `lognormal_pdf`.  
3. Trajetórias formam um “túnel”; \(\sigma\) controla a abertura.

## Desafios (opcional)

- Fixe \(N=10^5\) e varie `nsteps` ∈ {12, 52, 252}. O viés de discretização muda?  
- Troque \(\mu\) por \(r=0.05\) (mundo risco-neutro) e compare \(\mathbb{E}[S_T]\).  
- Estime IC 95% da média MC: \(\bar S_T \pm 1.96\cdot s/\sqrt{N}\).

## Manim

```bash
# na raiz do repo, com .venv ativo
manim -pql modules/M01-fundamentos/labs/01-gbm-monte-carlo/manim/scenes.py Lab01Full
```

Detalhes: [`manim/README.md`](manim/README.md) · interpretação: [`RESULTS.md`](RESULTS.md)

## Arquivos

- `run_lab.py` — execução + relatório de convergência  
- `RESULTS.md` — como ler a tabela MC  
- `manim/scenes.py` — 4 cenas animadas  
- Implementação: `src/econofisica/gbm.py`
