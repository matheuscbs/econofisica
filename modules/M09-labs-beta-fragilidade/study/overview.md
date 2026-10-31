<!-- imported study note (overview.md) -->
# M09 — Labs de pesquisa: beta operacional e R+/R−

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M09

> **info**
>
> Módulo 9 de 10 do curso Econofísica Khem Kapital. Pesquisa profunda montada em 2026-10-07 no NotebookLM com 31 fontes: os repositórios de labs de Karim Khemiri (`Beta-and-trading-environement`: README, manifesto de dados, reprodutibilidade, paper e código; `Fragile-Antifragile-Regime-Classifier`: README e paper) e Deep Research (cointegração, antifragilidade de Taleb). Notebook `d343e9bf-295f-485a-b51f-e121ee2e47aa`.

**Pergunta de mercado:** Como transformar beta e fragilidade em regras operacionais?

**Resultado esperado:** Selecionar relações beta estacionárias no ambiente executável e rotular o universo em frágil vs antifrágil.

!400

## Documentos

| Nota | Tipo | O que tem |
|------|------|-----------|
| Resumo Executivo | Resumo | Visão geral do módulo, mecanismos e por que importa |
| Guia Completo | Relatório | Seções numeradas com teoria, fórmulas, tabelas, Python e glossário |
| Aulas (A01–A02) | Guia de estudo | Cada aula com conceito, lab, exemplo resolvido e questões em 3 níveis |

## Aulas
1. M09.A01 — Lab — Beta operacional selecionado pelo ambiente de trading
2. M09.A02 — Lab — Classificador determinístico frágil (R+) vs antifrágil (R−)

## Trilha de leitura
1. Resumo Executivo — o mapa do módulo.
2. Aulas na ordem, fazendo o lab e as questões de cada uma.
3. Guia Completo, nas seções-chave:
   - §1 Beta operacional vs beta de livro
   - §2 Spreads, estacionariedade e cointegração
   - §3 Gates, quadrantes e estados
   - §4 Custos, placebo e robustez
   - §6 Classificador R+/R−
   - §8 Como rodar os labs
4. Conceitos abaixo, para fixar as definições.

## Conceitos
- Beta Operacional — o beta que sobrevive a custos e regimes
- Cointegração — spread estacionário, Engle-Granger, OU
- Classificador R+ e R− — R+ frágil, R− antifrágil, pela resposta à variância

## Mídia
!khem-m09-labs-beta-fragilidade-podcast.m4a

- Vídeo explicativo: khem-m09-labs-beta-fragilidade-video.mp4
- Apresentação: PDF · PPTX
- Infográfico: khem-m09-labs-beta-fragilidade-stories.png

> **note**
>
> ```bash
> NB=d343e9bf-295f-485a-b51f-e121ee2e47aa
> notebooklm artifact list -n $NB
> notebooklm download audio khem-m09-labs-beta-fragilidade-podcast.m4a -n $NB
> notebooklm download video khem-m09-labs-beta-fragilidade-video.mp4 -n $NB
> notebooklm download infographic khem-m09-labs-beta-fragilidade-stories.png -n $NB
> notebooklm download slide-deck khem-m09-labs-beta-fragilidade-apresentacao.pdf -n $NB
> notebooklm download slide-deck khem-m09-labs-beta-fragilidade-apresentacao.pptx --format pptx -n $NB
> # gerar de novo: notebooklm generate audio|video|infographic|slide-deck -n $NB --language pt_BR
> ```

## Mapa conceitual
```
Labs: de beta e fragilidade a regras operacionais
├── Lab 1 — Beta operacional
│   ├── spread s = P_A − β P_B · ADF / cointegração · OU
│   ├── seleção pelo ambiente: quadrantes Q1–Q4, estados, gates
│   └── custos congelados · placebo · robustez · reprodutibilidade
└── Lab 2 — Classificador determinístico
    ├── E (desempenho ajustado) ~ β · V (variância realizada)
    ├── β̂ > 0 → R+ (frágil) · β̂ < 0 → R− (antifrágil)
    ├── confiança WEAK/MEDIUM/STRONG não muda a perna
    └── saída → alocação frágil/antifrágil do Janus (M10)
```

## Relacionadas
- M08 — GARCH — módulo anterior; variância como estressor
- M10 — Capstone Janus — próximo módulo
- Programação Quantitativa — pairs trading e cointegração
- Inside the Black Box — modelos de risco e arbitragem estatística

## Fontes
1. Karim Khemiri — repositórios `Beta-and-trading-environement` e `Fragile-Antifragile-Regime-Classifier` (GitHub `karimkhemkapital`)
2. (Anti) Fragility - Riskdata — https://www.riskdata.com/resource-centre-papers/anti-fragility/
3. (PDF) A New Heuristic Measure of Fragility and Tail Risks: Application to Stress Testing — https://www.researchgate.net/publication/314786821_A_New_Heuristic_Measure_of_Fragility_and_Tail_Risks_Application_to_Stress_Testing
4. (PDF) Mathematical Definition, Mapping, and Detection of (Anti)Fragility - ResearchGate — https://www.researchgate.net/publication/230609579_Mathematical_Definition_Mapping_and_Detection_of_AntiFragility
5. Adapting Pairs Trading to Gambling Markets: A Case Study of the U.S. Presidential Election — https://arxiv.org/html/2609.22639v1
6. Durham E-Theses - Exchange Rate Dynamics, Intervention and — https://www.mobt3ath.com/uplode/book/book-66173.pdf
7. Enhanced Pairs Trading applied to the commodities market — https://fenix.tecnico.ulisboa.pt/downloadFile/1126295043840647/Artigo-90125-Jose-Machado.pdf
8. Estimating Option Pricing Models Using a Characteristic Function Based Linear State Space Representation - EconStor — https://www.econstor.eu/bitstream/10419/273788/1/22075.pdf
9. Financial Data: Time-Series Modeling - Portfolio Optimization — Chapter 4 — https://portfoliooptimizationbook.com/slides/slides-data-time-series.pdf
10. From Cointegration to Out-of-Sample Failure: A Pairs-Trading Case Study on PEP-KO — https://www.researchgate.net/publication/415029139_From_Cointegration_to_Out-of-Sample_Failure_A_Pairs-Trading_Case_Study_on_PEP-KO
11. Mathematical Definition, Mapping, and Detection of (Anti)Fragility - IDEAS/RePEc — https://ideas.repec.org/p/mse/cesdoc/14093.html
12. Mathematical Definition, Mapping, and Detection of (Anti)Fragility - IDEAS/RePEc — https://ideas.repec.org/p/arx/papers/1208.1189.html
13. Mathematical definition, mapping, and detection of (anti)fragility - Taylor & Francis — https://www.tandfonline.com/doi/pdf/10.1080/14697688.2013.800219
14. Pairs Trading Based on Empirical Mode Decomposition (EMD) - Iranian Journal of Finance — https://www.ijfifsa.ir/article_180152.html
15. Recursive KalmanNet: Deep Learning-Augmented Kalman Filtering for State Estimation with Consistent Uncertainty Quantification - arXiv — https://arxiv.org/html/2506.11639v1
16. STATE-SPACE MODELS* — http://emn.dserwa.pl/art/ss.pdf
17. Statistical Arbitrage in Forex: A Study on Pairs Trading and Mean- Reverting Rates - POLITesi — https://www.politesi.polimi.it/bitstream/10589/236340/4/Article_Format_Thesis_LucaPiccinini.pdf
18. Statistical arbitrage pairs trading strategies: Review and outlook - EconStor — https://www.econstor.eu/bitstream/10419/116783/1/833997289.pdf
19. The Handbook of Risk — https://www.dmf.unisalento.it/~straf/allow_listing/fabio/fabio2.pdf
20. Time series of R4 (Boxes 2 and 8) and R3 (Box 6) 27 26 25 24 23 22 — https://www.researchgate.net/figure/Time-series-of-R4-Boxes-2-and-8-and-R3-Box-6-27-26-25-24-23-22-21-20_fig1_228645402
21. Trend Following Trading under a Regime Switching Model | SIAM Journal on Financial Mathematics — https://epubs.siam.org/doi/10.1137/090770552
22. WO2015149035A1 - Systems and methods for crowdsourcing of algorithmic forecasting - Google Patents — https://patents.google.com/patent/WO2015149035A1/en
23. [1208.1189] Mathematical Definition, Mapping, and Detection of (Anti)Fragility - arXiv — https://arxiv.org/abs/1208.1189
24. arXiv:1910.01438v2 [q-fin.PM] 7 Oct 2019 — https://arxiv.org/pdf/1910.01438