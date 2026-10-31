<!-- imported study note (overview.md) -->
# M06 — Histerese, caudas e previsibilidade

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M06

> **info**
>
> Módulo 6 de 10 do curso Econofísica Khem Kapital. Pesquisa profunda montada em 2026-10-07 no NotebookLM com 41 fontes: as 2 lições originais de Karim Khemiri (histerese e dependência de trajetória, Lyapunov — com código) e Deep Research (leis de potência, EVT, caos em séries financeiras). Notebook `2fd500bc-7536-4c0f-82aa-c928d7eb9ba5`.

**Pergunta de mercado:** Por que trajetória e caos importam no drawdown e na previsibilidade?

**Resultado esperado:** Tratar fat tails e sensibilidade a condições iniciais como limites operacionais de sinal e stop.

!400

## Documentos

| Nota | Tipo | O que tem |
|------|------|-----------|
| Resumo Executivo | Resumo | Visão geral do módulo, mecanismos e por que importa |
| Guia Completo | Relatório | Seções numeradas com teoria, fórmulas, tabelas, Python e glossário |
| Aulas (A01–A02) | Guia de estudo | Cada aula com conceito, lab, exemplo resolvido e questões em 3 níveis |

## Aulas
1. M06.A01 — Histerese e dependência de trajetória no risco de cauda
2. M06.A02 — Expoente de Lyapunov: sensibilidade a condições iniciais no trading

## Trilha de leitura
1. Resumo Executivo — o mapa do módulo.
2. Aulas na ordem, fazendo o lab e as questões de cada uma.
3. Guia Completo, nas seções-chave:
   - §1 Histerese
   - §2 Trajetória, memória e drawdown
   - §3 Caudas gordas e EVT
   - §4 Stops e dimensionamento
   - §6 Lyapunov e horizonte
   - §7 Limites operacionais
4. Conceitos abaixo, para fixar as definições.

## Conceitos
- Histerese em Mercados — o caminho importa; limiares duplos
- Caudas Gordas — lei de potência α≈3, Hill e EVT
- Expoente de Lyapunov — divergência de trajetórias e horizonte de previsão
- Drawdown — perda desde o pico (do M05)

## Mídia
!khem-m06-histerese-caudas-podcast.m4a

- Vídeo explicativo: khem-m06-histerese-caudas-video.mp4
- Apresentação: PDF · PPTX
- Infográfico: khem-m06-histerese-caudas-stories.png

> **note**
>
> ```bash
> NB=2fd500bc-7536-4c0f-82aa-c928d7eb9ba5
> notebooklm artifact list -n $NB
> notebooklm download audio khem-m06-histerese-caudas-podcast.m4a -n $NB
> notebooklm download video khem-m06-histerese-caudas-video.mp4 -n $NB
> notebooklm download infographic khem-m06-histerese-caudas-stories.png -n $NB
> notebooklm download slide-deck khem-m06-histerese-caudas-apresentacao.pdf -n $NB
> notebooklm download slide-deck khem-m06-histerese-caudas-apresentacao.pptx --format pptx -n $NB
> # gerar de novo: notebooklm generate audio|video|infographic|slide-deck -n $NB --language pt_BR
> ```

## Mapa conceitual
```
Por que trajetória e caos importam
├── Histerese: estado depende do caminho
│   ├── vol sobe rápido, cai devagar · liquidez assimétrica
│   └── sinal com dois limiares (evita whipsaw)
├── Caudas gordas: P(|r|>x) ~ x^(−α), α≈3
│   ├── Hill · GEV · POT/Pareto generalizada
│   └── stop e tamanho de posição pela cauda
└── Caos determinístico
    ├── atratores · Takens (m, τ)
    ├── Lyapunov λ > 0 → divergência e^(λt)
    └── horizonte T_p ≈ (1/λ) ln(Δ/δ0) → validade do sinal
```

## Relacionadas
- M05 — Econofísica e entropia — módulo anterior
- M07 — Portfólio e fatores — próximo módulo
- Econofísica — leis de potência e escala
- Modelagem Estocástica de Séries Temporais Financeiras — caudas e memória em séries

## Fontes
1. Karim Khemiri — lições 22 e 23 de `quantitative-trading-free-lesson` (hysteresis and path dependence, Lyapunov), com código
2. (PDF) Hawkes Processes in Finance - ResearchGate — https://www.researchgate.net/publication/272422571_Hawkes_Processes_in_Finance
3. (PDF) Worker Utility as Hysteresis: A Preisach Model of Transaction Acceptance in Gig Labour Markets - ResearchGate — https://www.researchgate.net/publication/414632552_Worker_Utility_as_Hysteresis_A_Preisach_Model_of_Transaction_Acceptance_in_Gig_Labour_Markets
4. 2014-09 - Analytical Solution for a Class of Network Dynamics with — https://utd-ir.tdl.org/bitstreams/76bb4e93-2a72-4a40-bd83-78792d154d86/download
5. A Model of Optimal Production Planning Based on the Hysteretic Demand Curve - MDPI — https://www.mdpi.com/2227-7390/10/18/3262
6. A Mutual Information Approach to Calculating Nonlinearity - arXiv — https://arxiv.org/html/1512.00750v1
7. A Simple Nonparametric Test for Independence - EconStor — https://www.econstor.eu/bitstream/10419/94293/1/1995-23.pdf
8. A novel approach to analyzing Philippine inflation dynamics through — https://www.malque.pub/ojs/index.php/msj/article/download/2672/1763/22435
9. An Introduction to Value at Risk Methodologies - QuantPedia — https://quantpedia.com/an-introduction-to-value-at-risk-methodologies/
10. BDS Test -- from Wolfram MathWorld — https://mathworld.wolfram.com/BDSTest.html
11. BDS test - Early Warning Signals Toolbox — https://www.early-warning-signals.org/?page_id=121
12. Chaos Analysis Framework: How to Safely Identify and Quantify Time-Series Dynamics — https://www.intechopen.com/chapters/83753
13. Chaos Detection in Economic Time Series: Metric versus Topological Tools - Scienpress.com — http://www.scienpress.com/Upload/AMAE/Vol%203_6_3.pdf
14. Conditional Drawdown at Risk (CDAR) - Breaking Down Finance — https://breakingdownfinance.com/finance-topics/alternative-investments/conditional-drawdown-at-risk-cdar/
15. Conditional Value-at-Risk (CVaR): Algorithms and Applications — https://www2.mathematik.hu-berlin.de/~romisch/SP01/Uryasev.pdf
16. Conditional Value-at-Risk for General Loss Distributions - Quant Beckman — https://www.quantbeckman.com/api/v1/file/b3f3f3bd-5dc5-4b18-8889-21cdda8c3f11.pdf
17. Conditional Value-at-Risk for General Loss Distributions - UW Math Department — https://sites.math.washington.edu/~rtr/papers/rtr187-CVaR2.pdf
18. Detecting Structural Changes in Time Series by Using the BDS Test Recursively: An Application to COVID-19 Effects on International Stock Markets - MDPI — https://www.mdpi.com/2227-7390/11/23/4843
19. EUI WORKING PAPERS IN ECONOMICS — https://cadmus.eui.eu/bitstreams/378d4539-baff-52a0-9036-83fc61268e05/download
20. Foundations of the Preisach Operator in Real Options Problems with Subscription Cost and Heterogeneous Population of Consumers — https://www.preprints.org/manuscript/202510.0157?utm_source=researchgate.net&utm_medium=article
21. Generalized relational tensors for chaotic time series - PMC - NIH — https://pmc.ncbi.nlm.nih.gov/articles/PMC10280504/
22. Identifying Nonlinearity in Financial Time Series - SBIA — https://sbia.org.br/wp-content/uploads/2016/03/5cbrn_022.pdf
23. Labour market reforms and employment hysteresis — https://real.mtak.hu/144302/1/article-p175.pdf
24. NoLiTiA: An Open-Source Toolbox for Non-linear Time Series Analysis - Frontiers — https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2022.876012/full
25. Nonlinear Dynamics and Chaos: Application to Financial Markets in Pakistan — https://file.pide.org.pk/pdfpdr/1994/1417-1429.pdf
26. PORTFOLIO OPTIMIZATION WITH DRAWDOWN CONSTRAINTS — https://www.cis.upenn.edu/~mkearns/finread/drawdown.pdf
27. Ph. D. Course in - IRIS UniCa — https://iris.unica.it/retrieve/e2f56ed8-43b2-3eaf-e053-3a05fe0a5d97/Pisano_phd.pdf.pdf
28. Play-Hysteresis in the Joint Dynamics of Employment and Investment - PMC — https://pmc.ncbi.nlm.nih.gov/articles/PMC8940986/
29. Power Laws in Economics and Finance - AMiner — https://www.aminer.cn/pub/5faa4f2b65ca82c27fa6a7df/power-laws-in-economics-and-finance
30. Proceedings from ACCSA Global International Conference – April 25, 2026 — https://accsaglobal.org/wp-content/uploads/2026/05/ACCSA-Global-Conference-Proceedings-Done.pdf
31. Publications and Working Papers - Collegio Carlo Alberto — https://www.carloalberto.org/research/publications/
32. Reduced-bias tail index estimators under a third order framework - CEAUL — http://ceaul.org/wp-content/uploads/2018/10/CGHRHillnew2-BIASNC2_08.pdf
33. Review of Play and Preisach Models for Hysteresis in Magnetic Materials - MDPI — https://www.mdpi.com/1996-1944/16/6/2422
34. The Domestic Debt Intolerance and Bad Equilibrium: An Empirical — https://dosya2.gsu.edu.tr/page/2023/1/24/wp-13-01-616.pdf
35. The New Method of Measuring the Effects of Noise Reduction in Chaotic Data — https://wneiz.umk.pl/_upload/1/Orzeszko_www.pdf
36. arXiv:1404.7493v5 [q-fin.PM] 21 Sep 2016 — https://arxiv.org/pdf/1404.7493
37. arXiv:2303.09635v4 [eess.SY] 11 Dec 2023 — https://arxiv.org/pdf/2303.09635