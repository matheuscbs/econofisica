<!-- imported study note (overview.md) -->
# M03 — Curva de juros e produtos de taxa

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M03

> **info**
>
> Módulo 3 de 10 do curso Econofísica Khem Kapital. Pesquisa profunda montada em 2026-10-07 no NotebookLM com 30 fontes: as 3 lições originais de Karim Khemiri (forwards/FRA, swaps, opções de taxa — todas com código) e Deep Research (bootstrap, multi-curva, Black-76/Bachelier, SABR). Notebook `6f7d0a5e-b29a-4ff6-8d2e-f175d357e103`.

**Pergunta de mercado:** Como montar curva de juros e precificar taxa sem arbitragem?

**Resultado esperado:** Bootstrap de forwards, PV/DV01 de swap e mapa de onde a vol entra em caps/swaptions.

!400

## Documentos

| Nota | Tipo | O que tem |
|------|------|-----------|
| Resumo Executivo | Resumo | Visão geral do módulo, mecanismos e por que importa |
| Guia Completo | Relatório | Seções numeradas com teoria, fórmulas, tabelas, Python e glossário |
| Aulas (A01–A03) | Guia de estudo | Cada aula com conceito, lab, exemplo resolvido e questões em 3 níveis |

## Aulas
1. M03.A01 — Taxas forward sem arbitragem: construir a curva a partir do mercado
2. M03.A02 — Swaps de juros: precificar o instrumento padrão de taxa
3. M03.A03 — De forwards a opções de taxa: onde entra a volatilidade

## Trilha de leitura
1. Resumo Executivo — o mapa do módulo.
2. Aulas na ordem, fazendo o lab e as questões de cada uma.
3. Guia Completo, nas seções-chave:
   - §1 Fatores de desconto e forwards
   - §3 Bootstrap e interpolação
   - §4 Multi-curva, OIS, SOFR
   - §5 Swaps: taxa par, PV, MTM
   - §6 DV01, duração e KRD
   - §8 Black-76, Bachelier e SABR
4. Conceitos abaixo, para fixar as definições.

## Conceitos
- Curva de Juros — fatores de desconto, forwards, bootstrap e multi-curva
- Swap de Taxa de Juros — perna fixa × flutuante, taxa par e MTM
- DV01 — risco de taxa por ponto-base; hedge e key rates
- Modelo de Black-76 — caplets, swaptions; Bachelier para taxas negativas
- Modelo SABR — smile de taxas com vol estocástica

## Mídia
!khem-m03-curva-juros-podcast.m4a

- Vídeo explicativo: khem-m03-curva-juros-video.mp4
- Apresentação: PDF · PPTX
- Infográfico: khem-m03-curva-juros-stories.png

> **note**
>
> ```bash
> NB=6f7d0a5e-b29a-4ff6-8d2e-f175d357e103
> notebooklm artifact list -n $NB
> notebooklm download audio khem-m03-curva-juros-podcast.m4a -n $NB
> notebooklm download video khem-m03-curva-juros-video.mp4 -n $NB
> notebooklm download infographic khem-m03-curva-juros-stories.png -n $NB
> notebooklm download slide-deck khem-m03-curva-juros-apresentacao.pdf -n $NB
> notebooklm download slide-deck khem-m03-curva-juros-apresentacao.pptx --format pptx -n $NB
> # gerar de novo: notebooklm generate audio|video|infographic|slide-deck -n $NB --language pt_BR
> ```

## Mapa conceitual
```
Curva de juros (sem arbitragem)
├── P(0,T) fatores de desconto ↔ taxas zero ↔ forwards F(T1,T2)
│   └── FRA: trava hoje a taxa futura
├── Bootstrap: depósitos → FRAs/futuros → swaps  (+ interpolação)
│   └── multi-curva: desconto OIS/CDI ≠ projeção do índice
├── Swaps: PV_fixa vs PV_flut → taxa par = PV_flut / anuidade
│   └── risco: DV01, duração, convexidade, key rates
└── Onde entra a vol: caps/floors (caplets) e swaptions
    ├── Black-76 (lognormal) vs Bachelier (normal, taxas negativas)
    └── smile → SABR → superfície de vol (M04)
```

## Relacionadas
- M02 — Dinâmica e gregas — módulo anterior
- M04 — Superfície de vol — próximo módulo; o smile de taxas vira superfície
- PIB, Inflação e Yield Curve — a curva vista pela macro; aqui, pela engenharia de preço
- Ações e Bonds — duração e convexidade de bonds ↔ DV01 de swaps

## Fontes
1. Karim Khemiri — lições 09 a 11 de `quantitative-trading-free-lesson` (forward rates by no arbitrage, pricing interest rate swaps, from forwards to options), com código
2. (PDF) A rough SABR formula - ResearchGate — https://www.researchgate.net/publication/354444187_A_rough_SABR_formula
3. (PDF) Interpolation of Yield curves - ResearchGate — https://www.researchgate.net/publication/342437744_Interpolation_of_Yield_curves
4. (PDF) Methods for constructing a yield curve - ResearchGate — https://www.researchgate.net/publication/228463045_Methods_for_constructing_a_yield_curve
5. A rough SABR formula arXiv:2105.05359v1 [q-fin.MF] 11 May 2021 — https://arxiv.org/pdf/2105.05359
6. Alma Mater Studiorum Università di Bologna Archivio istituzionale della ricerca — https://cris.unibo.it/retrieve/handle/11585/601673/e1dcb338-8ae1-7715-e053-1705fe0a6cc9/MathematicalFinance27-2017.pdf
7. Approximate Arbitrage-Free Option Pricing under the SABR Model — https://www1.se.cuhk.edu.hk/~nchenweb/working_paper/SSRN-id2854797.pdf
8. Interest Rate Caps and Floors: Payoff Mechanics, Pricing, and Hedging — https://ryanoconnellfinance.com/interest-rate-caps-floors/
9. Interest Rate Modelling and Derivative Pricing — https://www.applied-financial-mathematics.de/sites/default/files/Teaching/InterestRateMdellingWS19/IRModellingLecture_Part_03.pdf
10. Interpolation Methods for Curve Construction - Deriscope — https://www.deriscope.com/docs/Hagan_West_curves_AMF.pdf
11. LIBOR Market Model calibration for Credit Valuation Adjustment of a portfolio of swaptions - Erasmus University Thesis Repository — https://thesis.eur.nl/pub/65835/Thesis_Daniel_Allick_Final.pdf
12. Learning the Exact SABR Model - arXiv — https://arxiv.org/html/2510.10343v2
13. MANAGING SMILE RISK 1. Introduction. European options are often priced and hedged using Black's model, or, equivalently, the B - Next Finance — https://www.next-finance.net/IMG/pdf/pdf_SABR.pdf
14. MASTER THESIS IN MATHEMATICS / APPLIED MATHEMATICS Hedging Interest Rate Derivatives (Evidence from Swaptions) in a Negative Int - DiVA portal — https://www.diva-portal.org/smash/get/diva2:1068004/FULLTEXT01.pdf
15. Methods for Constructing a Yield Curve - dxFeed — https://downloads.dxfeed.com/specifications/dxLibOptions/HaganWest.pdf
16. Pricing and Hedging Fixed Income Derivatives under Negative Interest Rates: An SABR approach Elizabet Tsvetanova Atanasova — https://www.uv.es/bfc/TFM2017/3%20Elizabet%20Atanasova%201.pdf
17. SABR volatility model - Wikipedia — https://en.wikipedia.org/wiki/SABR_volatility_model
18. Stable Interpolation for the Yield Curve - Anthony Lloyd — http://anthonylloyd.github.io/public/finance/Stable%20Interpolation%20for%20the%20Yield%20Curve%20-%20Fabien%20Le%20Floc'h.pdf
19. Work with Negative Interest Rates Using Functions - MATLAB & Simulink - MathWorks — https://www.mathworks.com/help/fininst/work-with-negative-interest-rates-using-functions.html
20. Work with Negative Interest Rates Using Objects - MATLAB & Simulink - MathWorks — https://la.mathworks.com/help/fininst/work-with-negative-interest-rates-using-objects.html
21. arXiv:0708.0998v3 [q-fin.CP] 18 Mar 2008 — https://arxiv.org/pdf/0708.0998
22. https://archive.org/download/arxiv-0906.0658/0906.0658.pdf — https://archive.org/download/arxiv-0906.0658/0906.0658.pdf
23. https://lutpub.lut.fi/bitstream/10024/38026/1/Pro.Gradu.pihlaja.pdf — https://lutpub.lut.fi/bitstream/10024/38026/1/Pro.Gradu.pihlaja.pdf
24. interpolating yield curve data in a manner that ensures positive and continuous forward curves - South African Journal of Economic and Management Sciences — https://sajems.org/index.php/sajems/article/download/388/269