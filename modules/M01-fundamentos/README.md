# M01 — Fundamentos de precificação

**Pergunta:** Como precificar e fazer hedge de opções vanila sem adivinhar o drift?

## Lições

| Aula | Tema |
|------|------|
| [A01](lessons/A01-mapa-do-curso-de-precificacao-a-alocacao-por-regime.md) | Mapa do curso |
| [A02](lessons/A02-preco-minimo-de-uma-opcao-o-que-o-mercado-nao-pode-deixar-de-pagar.md) | Preço mínimo (no-arbitrage) |
| [A03](lessons/A03-delta-neutro-transformar-opiniao-direcional-em-risco-controlado.md) | Delta neutro |
| [A04](lessons/A04-lema-de-ito-por-que-o-hedge-continuo-gera-um-termo-extra-de-variancia.md) | Lema de Itô |
| [A05](lessons/A05-mundo-risco-neutro-e-blackscholes-precificar-sem-prever-o-drift.md) | Mundo risco-neutro e BSM |

## Labs

| Lab | Status |
|-----|--------|
| [01 — Vendedor sem hedge](labs/01-vendedor-sem-hedge) | **ativo** — cauda de perdas *wait-and-see* |
| 02 — Delta hedge dinâmico | próximo |
| 03 — BSM + IV | planejado |

## Estudo

- [Overview](study/overview.md) · [Resumo](study/resumo.md) · [Guia completo](study/guia-completo.md)

## Pré-requisitos

Esperança/variância, Python + NumPy. GBM detalhado também em [M02 Lab 01](../M02-dinamica-gregas/labs/01-gbm-monte-carlo).

## Ordem sugerida

1. Ler A02–A03  
2. Rodar **Lab 01** (este módulo)  
3. [M02 Lab 01](../M02-dinamica-gregas/labs/01-gbm-monte-carlo) se quiser aprofundar o motor GBM  
4. Voltar para A04–A05 + próximo lab de hedge  
