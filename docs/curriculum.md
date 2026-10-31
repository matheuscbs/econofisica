# Curriculum — Econofísica (@mosscardoso)

Grade em **10 módulos / ~32 lições**. Cada lição tem: conceito-núcleo · aplicação de mercado · entregável prático.

## M01 — Fundamentos de precificação

**Pergunta:** Como precificar e fazer hedge de vanilas sem “adivinhar” o drift?

| Aula | Título | Entregável |
|------|--------|------------|
| M01.A01 | Mapa do curso | Checklist pessoal + trilha |
| M01.A02 | Preço mínimo de uma opção | Tabela call/put vs limites |
| M01.A03 | Delta neutro | Simulação de rebalance Δ≈0 |
| M01.A04 | Lema de Itô | Expansão em GBM + P&L hedged |
| M01.A05 | Mundo risco-neutro e BSM | BSM call/put + IV invertida |

## M02 — Dinâmica, gregas e path dependence

**Pergunta:** Como a dinâmica do spot e as gregas mudam o P&L do livro?

| Aula | Título | Entregável |
|------|--------|------------|
| **M02.A01** | **GBM — trajetória padrão** | **Lab 01: Monte Carlo + convergência** |
| M02.A02 | Gregas | Painel Δ, Γ, Θ, ν, ρ |
| M02.A03 | Exóticas e path dependence | Spec de 1 barreira + riscos de hedge |

## M03 — Curva de juros

**Pergunta:** Como montar curva e precificar taxa sem arbitragem?

| Aula | Título | Entregável |
|------|--------|------------|
| M03.A01 | Forwards por no-arb | Bootstrap simplificado |
| M03.A02 | Swaps de juros | PV + DV01 |
| M03.A03 | Opções de taxa | Mapa FRA → caplet → swaption |

## M04 — Superfície de vol

**Pergunta:** Como ler, sanitizar e modelar o smile?

| Aula | Título | Entregável |
|------|--------|------------|
| M04.A01 | Convenções da surface | Grade IV |
| M04.A02 | Construção livre de arb | Checklist calendar/butterfly |
| M04.A03 | Imposta → local vol | Esboço Dupire |
| M04.A04 | Heston + MC | Smile gerado vs BSM flat |
| M04.A05 | Jump-diffusion | Densidades GBM vs jump |
| M04.A06 | Smile FX sticky | Strike vs delta após ±1% spot |

## M05 — Econofísica: informação, entropia e risco

**Pergunta:** O que a econofísica muda na leitura de incerteza?

| Aula | Título | Entregável |
|------|--------|------------|
| M05.A01 | Difusão, calor e PDE BSM | Mapa analogia → métrica |
| M05.A02 | Entropia de Shannon | Entropia rolling |
| M05.A03 | Temperatura de mercado | Entropia + drawdown |
| M05.A04 | Risco como força | Replay de crash |

## M06 — Histerese, caudas e previsibilidade

**Pergunta:** Por que trajetória e caos importam no drawdown?

| Aula | Título | Entregável |
|------|--------|------------|
| M06.A01 | Histerese e caudas | Gaussiana vs fat tails |
| M06.A02 | Expoente de Lyapunov | Divergência de paths próximos |

## M07 — Portfólio e fatores

**Pergunta:** Como alocar além do μ ingênuo?

| Aula | Título | Entregável |
|------|--------|------------|
| M07.A01 | Markowitz | Fronteira + stress de μ |
| M07.A02 | CAPM | Regressão beta/alpha |
| M07.A03 | Black–Litterman | Views + pesos |
| M07.A04 | APT / multifatores | Decomposição de exposições |

## M08 — Variância que propaga

**Pergunta:** Como a variância prepara regras de regime?

| Aula | Título | Entregável |
|------|--------|------------|
| M08.A01 | ARCH/GARCH | σ_t vs \|r_t\| |

## M09 — Labs: beta e fragilidade

**Pergunta:** Como transformar beta e fragilidade em regras?

| Aula | Título | Entregável |
|------|--------|------------|
| M09.A01 | Beta operacional | Pares + regimes + custos |
| M09.A02 | Classificador R+/R− | Labels frágil vs antifrágil |

## M10 — Capstone Janus

**Pergunta:** Como alocar frágil/antifrágil com consciência de regime?

| Aula | Título | Entregável |
|------|--------|------------|
| M10.A01 | Lei assinada de resposta à variância | β por ativo/par |
| M10.A02 | Alocação defasada + hedge | Backtest regime-aware |
