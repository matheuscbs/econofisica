<!-- imported study note (overview.md) -->
# M04 — Superfície de vol e modelos de smile

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M04

> **info**
>
> Módulo 4 de 10 do curso Econofísica Khem Kapital. Pesquisa profunda montada em 2026-10-07 no NotebookLM com 34 fontes: as 6 lições originais de Karim Khemiri (superfície, construção sem arbitragem, Dupire, Heston, saltos, smile FX — com código) e Deep Research (SVI/SSVI, Breeden-Litzenberger, esquemas de Heston, convenções FX). Notebook `bb194c3b-2394-46dd-bb12-abf8deeee70a`.

**Pergunta de mercado:** Como ler, sanitizar e modelar a superfície de volatilidade?

**Resultado esperado:** Montar/sanitizar surface, escolher local vol vs Heston vs jumps e testar sticky strike vs sticky delta em FX.

!400

## Documentos

| Nota | Tipo | O que tem |
|------|------|-----------|
| Resumo Executivo | Resumo | Visão geral do módulo, mecanismos e por que importa |
| Guia Completo | Relatório | Seções numeradas com teoria, fórmulas, tabelas, Python e glossário |
| Aulas (A01–A06) | Guia de estudo | Cada aula com conceito, lab, exemplo resolvido e questões em 3 níveis |

## Aulas
1. M04.A01 — Superfície de volatilidade: expiry, tenor e convenções de mercado
2. M04.A02 — Construção livre de arbitragem da superfície
3. M04.A03 — De volatilidade implícita a volatilidade local
4. M04.A04 — Heston e Monte Carlo: origem do smile com vol estocástica
5. M04.A05 — Saltos (jump-diffusion): quando a continuidade do GBM falha
6. M04.A06 — Smile FX: sticky strike vs sticky delta na prática

## Trilha de leitura
1. Resumo Executivo — o mapa do módulo.
2. Aulas na ordem, fazendo o lab e as questões de cada uma.
3. Guia Completo, nas seções-chave:
   - §2 Arbitragem estática e densidade
   - §3 SVI e SSVI
   - §4 Dupire
   - §5 Heston
   - §6 Saltos
   - §7 Smile FX e dinâmica
   - §8 Como escolher o modelo
4. Conceitos abaixo, para fixar as definições.

## Conceitos
- Superfície de Volatilidade — smile, skew, variância total e arbitragem estática
- Volatilidade Local de Dupire — σ(S,t) que reproduz a superfície de hoje
- Modelo de Heston — vol estocástica; ρ gera skew, ξ gera curvatura
- Modelo de Merton com Saltos — caudas e smile curto
- Sticky Strike e Sticky Delta — como o smile anda com o spot; RR e BF em FX
- Modelo SABR — smile de taxas, visto no M03

## Mídia
!khem-m04-superficie-vol-podcast.m4a

- Vídeo explicativo: khem-m04-superficie-vol-video.mp4
- Apresentação: PDF · PPTX
- Infográfico: khem-m04-superficie-vol-stories.png

> **note**
>
> ```bash
> NB=bb194c3b-2394-46dd-bb12-abf8deeee70a
> notebooklm artifact list -n $NB
> notebooklm download audio khem-m04-superficie-vol-podcast.m4a -n $NB
> notebooklm download video khem-m04-superficie-vol-video.mp4 -n $NB
> notebooklm download infographic khem-m04-superficie-vol-stories.png -n $NB
> notebooklm download slide-deck khem-m04-superficie-vol-apresentacao.pdf -n $NB
> notebooklm download slide-deck khem-m04-superficie-vol-apresentacao.pptx --format pptx -n $NB
> # gerar de novo: notebooklm generate audio|video|infographic|slide-deck -n $NB --language pt_BR
> ```

## Mapa conceitual
```
Superfície de volatilidade σ_impl(K, T)
├── Ler: expiry, tenor, moneyness/delta, ATM
├── Construir sem arbitragem
│   ├── calendário ∂_T w ≥ 0 · borboleta q(K) ≥ 0
│   └── sanitizar → SVI / SSVI
├── Modelar a origem do smile
│   ├── vol local (Dupire): ajusta hoje, dinâmica ruim
│   ├── Heston: vol estocástica, Feller, MC (QE)
│   └── saltos (Merton, Kou): caudas, smile curto
└── Dinâmica do smile
    ├── sticky strike vs sticky delta → delta efetivo
    └── FX: ATM DNS, risk reversal, butterfly
```

## Relacionadas
- M03 — Curva de juros — módulo anterior; smile de taxas e SABR
- M05 — Econofísica e entropia — próximo módulo
- Modelagem Estocástica de Séries Temporais Financeiras — Heston, saltos e simulação
- Econofísica — caudas gordas e leis de potência por trás do smile

## Fontes
1. Karim Khemiri — lições 12 a 17 de `quantitative-trading-free-lesson` (volatility surface, arbitrage-free construction, implied to local vol, Heston/Monte Carlo, jump-diffusion, FX smile dynamics), com código
2. Arbitrage-free SVI volatility surfaces - Baruch MFE Program — https://mfe.baruch.cuny.edu/wp-content/uploads/2013/01/OsakaSVI2012.pdf
3. Arbitrage-free SVI volatility surfaces - Imperial College London — https://www.imperial.ac.uk/media/imperial-college/research-centres-and-groups/stochastic-analysis-group/preprints-2012/12-11.pdf
4. Essays on currency crash risk, carry trade returns, and sovereign bond yields - UvA-DARE (Digital Academic Repository) — https://pure.uva.nl/ws/files/187995983/Thesis.pdf
5. Foreign Exchange Derivatives — https://catalogimages.wiley.com/images/db/pdf/9781118471067.excerpt.pdf
6. Foreign Exchange, ADR's and Quanto-Securities — http://www.columbia.edu/~mh2078/ContinuousFE/FX_Quanto.pdf
7. Gatheral SSVI Volatility Surface Calculator - MetricGate — https://metricgate.com/docs/gatheral-ssvi-surface/
8. Implied volatility to local volatility via Dupire - Quantitative Finance Stack Exchange — https://quant.stackexchange.com/questions/74062/implied-volatility-to-local-volatility-via-dupire
9. Introduction to Merton Jump Diffusion Model. — https://www.maxmatsuda.com/Papers/Intro/Intro%20to%20MJD%20Matsuda.pdf
10. Jump diffusion models, Merton and Bates - LexiFi — https://www.lexifi.com/blog/quant/jump-diffusion-models-merton-and-bates/
11. Lecture 2: The SVI arbitrage-free volatility surface parameterization — https://www.imperial.ac.uk/media/imperial-college/research-centres-and-groups/cfm-imperial-institute-of-quantitative-finance/events/distinguished-lectures/Gatheral-2nd-Lecture.pdf
12. Obtaining arbitrage-free foreign exchange implied volatility by variational inference - Risk.net — https://www.risk.net/media/download/1088759/download
13. Option pricing in affine generalized Merton models — https://www.wias-berlin.de/people/bayerc/files/HolTAppl6.pdf
14. Options Pricing under Shared-jump Diffusion Model by Fourier Space Time-stepping Method - University of Waterloo — https://uwaterloo.ca/computational-mathematics/sites/default/files/uploads/documents/bangyao_xu.pdf
15. Research on American Option Pricing Under the Heston Jump Diffusion Model—Based on Fourier Space Time-Stepping Method - MDPI — https://www.mdpi.com/2227-7390/14/9/1412
16. Robust calibration and arbitrage-free interpolation of SSVI slices - arXiv — https://arxiv.org/pdf/1804.04924
17. Session 3: The SVI arbitrage-free volatility surface parameterization - Baruch MFE Program — https://mfe.baruch.cuny.edu/wp-content/uploads/2015/06/VW3.pdf
18. The role of higher moments in high-frequency data modelling - Qucosa - TU Dresden — https://tud.qucosa.de/api/qucosa%3A76719/attachment/ATT-0/
19. Volatility Surface API: How to Build, Visualize, and Trade the IV Surface with Code — https://flashalpha.com/articles/volatility-surface-api-how-to-build-visualize-trade-iv-surface
20. What Is SVI? Stochastic Vol Inspired Smile Parametrization | OAS - Options Analysis Suite — https://www.optionsanalysissuite.com/documentation/svi
21. What is a Jump-Diffusion Model? - Cube Exchange — https://www.cube.exchange/what-is/jump-diffusion-models
22. https://www.scribd.com/document/901734207/Gatheral-Jacquier-Arb-free — https://www.scribd.com/document/901734207/Gatheral-Jacquier-Arb-free