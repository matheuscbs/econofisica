<!-- imported study note (overview.md) -->
# M01 — Fundamentos: preço mínimo, delta, Itô e mundo risco-neutro

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M01

> **info**
>
> Módulo 1 de 10 do curso Econofísica Khem Kapital. Pesquisa profunda montada em 2026-10-07 no NotebookLM com 22 fontes: as 5 lições originais de Karim Khemiri (texto + código) e 16 fontes de Deep Research (papers de hedge discreto, custos de transação, teorema fundamental). Notebook `e08127a7-5d4e-4c45-897d-d0658834037c`.

**Pergunta de mercado:** Como precificar e fazer hedge de opções vanila sem “adivinhar” o drift?

**Resultado esperado:** Saber explicar por que o preço de uma vanila não depende do drift μ e montar um hedge Δ com consciência do termo de Itô.

!400

## Documentos

| Nota | Tipo | O que tem |
|------|------|-----------|
| Resumo Executivo | Resumo | Visão do módulo: GBM, Itô, delta hedge, EDP de BS e fricções reais |
| Guia Completo | Relatório | 9 seções numeradas: teoria, derivações, custos, erro de hedge, Python, glossário |
| Aulas A01–A05 (abaixo) | Guia de estudo | Cada aula com conceito, lab, exemplo resolvido e questões em 3 níveis |

## Aulas
1. M01.A01 — Mapa do curso: de precificação a alocação por regime
2. M01.A02 — Preço mínimo de uma opção — na lição original, "minimal price" é a *dinâmica mínima* (GBM) para raciocinar sobre convexidade; os limites de no-arbitrage estão no Guia Completo §3
3. M01.A03 — Delta neutro: transformar opinião direcional em risco controlado
4. M01.A04 — Lema de Itô: por que o hedge contínuo gera um termo extra de variância
5. M01.A05 — Mundo risco-neutro e Black–Scholes: precificar sem prever o drift

## Trilha de leitura
1. Resumo Executivo — 15 min para ter o mapa.
2. Aulas A01 → A05 na ordem, fazendo o lab e as questões de cada uma.
3. Guia Completo, nas seções-chave:
   - §2 Dinâmica GBM e log-normal
   - §4 Delta neutro, bandas e custos (Leland, Hodges-Neuberger)
   - §5 Itô e P&L gamma-theta
   - §6 EDP de BS, medida Q e fórmula fechada
   - §7 Erro de hedge: discreto e vol errada
   - §8 Python e checklist de mesa
4. Conceitos abaixo, para fixar as definições.

## Conceitos
- Movimento Browniano Geométrico — a dinâmica mínima de preço, log-normal
- Lema de Itô — regra da cadeia estocástica; origem do termo de variância/gamma
- Delta Hedging — neutralizar Δ, bandas de rebalanceamento e custos
- Modelo Black-Scholes — EDP, fórmula fechada, N(d1)/N(d2)
- Medida Risco-Neutra — por que μ some do preço; Girsanov e teorema fundamental
- Paridade Put-Call — relação model-free entre call e put

## Mídia
!khem-m01-fundamentos-podcast.m4a

- Vídeo explicativo: khem-m01-fundamentos-video.mp4
- Apresentação: PDF · PPTX
- Infográfico: khem-m01-fundamentos-stories.png

> **note**
>
> ```bash
> NB=e08127a7-5d4e-4c45-897d-d0658834037c
> notebooklm artifact list -n $NB
> notebooklm download audio khem-m01-fundamentos-podcast.m4a -n $NB
> notebooklm download video khem-m01-fundamentos-video.mp4 -n $NB
> notebooklm download infographic khem-m01-fundamentos-stories.png -n $NB
> notebooklm download slide-deck khem-m01-fundamentos-apresentacao.pdf -n $NB
> notebooklm download slide-deck khem-m01-fundamentos-apresentacao.pptx --format pptx -n $NB
> ```

## Mapa conceitual
```
Opção = transferência de risco (prêmio ↔ convexidade)
├── Dinâmica mínima: GBM  dS = μS dt + σS dW
│   └── ln S ~ Normal → preço log-normal, momentos fechados
├── Delta neutro: Δ_total = 0
│   ├── controlador por bandas (Hodges-Neuberger / Whalley-Wilmott)
│   └── custos → vol modificada de Leland
├── Lema de Itô: + ½ Γ σ² S² dt
│   └── P&L gamma-theta ∝ (σ²_real − σ²_impl)
└── Portfólio sem risco → EDP de Black-Scholes
    ├── μ desaparece → medida risco-neutra Q (Girsanov, FTAP)
    ├── fórmula fechada: S N(d1) − K e^{-rT} N(d2)
    └── realidade: erro discreto O(√Δt), vol errada, smile → M02/M04
```

## Relacionadas
- Econofísica — pesquisa anterior; a analogia difusão ↔ EDP de BS volta no M05
- Modelagem Estocástica de Séries Temporais Financeiras — GBM, Itô e simulação de trajetórias
- Programação Quantitativa — implementação em Python dos labs

## Fontes
1. Karim Khemiri — lições 01 a 05 de `quantitative-trading-free-lesson` (intro, the minimal price, neutral delta, Itô's lemma, risk-neutral world / Black-Scholes), com código
2. Continuous-Time Option Pricing, Risk-Neutral Arbitrage, and Practical Delta Hedging Frictions — relatório do Deep Research
3. Delta hedging with stochastic volatility in discrete time — WU Wien — https://www.wu.ac.at/fileadmin/wu/d/i/ifr/delta.pdf
4. Derivatives Hedging and Volatility Errors — University of Warwick — https://warwick.ac.uk/fac/soc/wbs/subjects/finance/research/wpaperseries/2003/03-122.pdf
5. Discrete-time delta hedging and the Black-Scholes model with transaction costs — https://ideas.repec.org/a/spr/mathme/v64y2006i2p227-236.html
6. Evaluating Hedging Errors: An Asymptotic Approach (Mykland) — https://galton.uchicago.edu/~mykland/paperlinks/hedgeerrors.pdf
7. Fundamental theorem of asset pricing — Wikipedia — https://en.wikipedia.org/wiki/Fundamental_theorem_of_asset_pricing
8. Introduction to Risk-Neutral Pricing Theory — Jérémie Smaga — https://blog.smaga.ch/introduction-to-risk-neutral-pricing-theory/
9. Martingale Pricing Theory — QuestDB — https://questdb.com/glossary/martingale-pricing-theory/
10. On Leland's Option Hedging Strategy with Transaction Costs — https://d-nb.info/1181860253/34
11. Optimal Delta-Hedging Under Transactions Costs — University of Warwick — https://warwick.ac.uk/fac/soc/wbs/subjects/finance/research/wpaperseries/1993/93-36.pdf
12. Risk-Neutral Pricing Explained — Quant Blueprint — https://www.quantblueprint.com/glossary/risk-neutral-pricing
13. Risk-Neutral Pricing: The Fundamental Theorem of Asset Pricing Made Concrete — Quantt — https://www.quantt.co.uk/resources/risk-neutral-pricing
14. Risk-Neutral Probability and Derivative Pricing — Risk Hub — https://riskhub.org/blogs/risk-neutral-probability-and-derivative-pricing-243
15. The Fundamental Theorem of Asset Pricing (Delbaen & Schachermayer) — https://www.mat.univie.ac.at/~schachermayer/preprnts/prpr0141a.pdf