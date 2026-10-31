# M01 — Fundamentos de precificação

**Pergunta:** Como precificar e fazer hedge de opções vanila sem adivinhar o drift?

## Lições → Labs

| Aula | Tema | Lab |
|------|------|-----|
| [A01](lessons/A01-mapa-do-curso-de-precificacao-a-alocacao-por-regime.md) | Mapa do curso | — |
| [A02](lessons/A02-preco-minimo-de-uma-opcao-o-que-o-mercado-nao-pode-deixar-de-pagar.md) | Dinâmica mínima (GBM) + momentos | **[01 — GBM Monte Carlo](labs/01-gbm-monte-carlo)** |
| [A03](lessons/A03-delta-neutro-transformar-opiniao-direcional-em-risco-controlado.md) | Delta neutro / wait-and-see | **[02 — Vendedor sem hedge](labs/02-vendedor-sem-hedge)** |
| [A04](lessons/A04-lema-de-ito-por-que-o-hedge-continuo-gera-um-termo-extra-de-variancia.md) | Lema de Itô | próximo |
| [A05](lessons/A05-mundo-risco-neutro-e-blackscholes-precificar-sem-prever-o-drift.md) | Mundo risco-neutro e BSM | planejado |

## Ordem sugerida

1. Ler A02 → rodar **Lab 01** (teoria GBM + convergência MC)  
2. Ler A03 → rodar **Lab 02** (por que vender naked quebra)  
3. A04–A05 → próximos labs (Itô / BSM + IV / delta hedge)

## Estudo

- [Overview](study/overview.md) · [Resumo](study/resumo.md) · [Guia completo](study/guia-completo.md)

## Pré-requisitos

Esperança/variância, Python + NumPy. Setup: `pip install -e ".[dev,manim]"`.
