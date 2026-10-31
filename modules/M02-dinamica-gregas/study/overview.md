<!-- imported study note (overview.md) -->
# M02 — Dinâmica, gregas e path dependence

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M02

> **info**
>
> Módulo 2 de 10 do curso Econofísica Khem Kapital. Pesquisa profunda montada em 2026-10-07 no NotebookLM com 42 fontes: as 3 lições originais de Karim Khemiri (GBM com código, gregas, exóticas) e Deep Research (Monte Carlo, redução de variância, gregas por AAD, barreiras discretas). Notebook `e2a1c7d5-f7b5-4186-8a6a-de0093e8a9ff`.

**Pergunta de mercado:** Como a dinâmica do spot e as gregas mudam o P&L do livro?

**Resultado esperado:** Ler o book por gregas, simular GBM com disciplina e identificar quando o payoff path-dependent exige modelo além de vanila.

!400

## Documentos

| Nota | Tipo | O que tem |
|------|------|-----------|
| Resumo Executivo | Resumo | Visão geral do módulo, mecanismos e por que importa |
| Guia Completo | Relatório | Seções numeradas com teoria, fórmulas, tabelas, Python e glossário |
| Aulas (A01–A03) | Guia de estudo | Cada aula com conceito, lab, exemplo resolvido e questões em 3 níveis |

## Aulas
1. M02.A01 — Movimento browniano geométrico: o modelo padrão de trajetória de preço
2. M02.A02 — Gregas: o painel de risco do livro de opções
3. M02.A03 — Opções exóticas e dependência de trajetória: quando o caminho importa

## Trilha de leitura
1. Resumo Executivo — o mapa do módulo.
2. Aulas na ordem, fazendo o lab e as questões de cada uma.
3. Guia Completo, nas seções-chave:
   - §1 GBM e Monte Carlo disciplinado
   - §2 Gregas de 1ª e 2ª ordem
   - §3 P&L explain do book
   - §6 Path dependence e correção BGK
   - §7 MC, redução de variância e gregas
   - §8 Quando vanila não basta
4. Conceitos abaixo, para fixar as definições.

## Conceitos
- Movimento Browniano Geométrico — trajetória padrão; solução exata vs Euler
- Simulação de Monte Carlo — preço como média de payoffs; erro 1/√N e redução de variância
- Gregas das Opções — delta, gamma, vega, theta, rho e segunda ordem; P&L explain
- Opções Exóticas — asiáticas, barreira, lookback; o caminho importa
- Modelo Black-Scholes — fonte das gregas em forma fechada (do M01)

## Mídia
!khem-m02-dinamica-gregas-podcast.m4a

- Vídeo explicativo: khem-m02-dinamica-gregas-video.mp4
- Apresentação: PDF · PPTX
- Infográfico: khem-m02-dinamica-gregas-stories.png

> **note**
>
> ```bash
> NB=e2a1c7d5-f7b5-4186-8a6a-de0093e8a9ff
> notebooklm artifact list -n $NB
> notebooklm download audio khem-m02-dinamica-gregas-podcast.m4a -n $NB
> notebooklm download video khem-m02-dinamica-gregas-video.mp4 -n $NB
> notebooklm download infographic khem-m02-dinamica-gregas-stories.png -n $NB
> notebooklm download slide-deck khem-m02-dinamica-gregas-apresentacao.pdf -n $NB
> notebooklm download slide-deck khem-m02-dinamica-gregas-apresentacao.pptx --format pptx -n $NB
> # gerar de novo: notebooklm generate audio|video|infographic|slide-deck -n $NB --language pt_BR
> ```

## Mapa conceitual
```
Book de opções
├── Dinâmica: GBM  S_T = S_0 exp[(μ−½σ²)T + σW_T]
│   └── Monte Carlo disciplinado: semente, erro padrão, validação vs fechado
├── Painel de risco: gregas
│   ├── 1ª ordem: Δ, ν, Θ, ρ
│   ├── 2ª ordem: Γ, vanna, volga, charm
│   └── P&L explain: Δ dS + ½Γ dS² + ν dσ + Θ dt
└── Quando o caminho importa: exóticas
    ├── asiática (média) · barreira (toque) · lookback (máx/mín)
    ├── monitoramento discreto → correção BGK
    ├── MC + redução de variância + gregas pathwise/AAD
    └── exige modelo da dinâmica inteira → vol local, Heston, saltos (M04)
```

## Relacionadas
- M01 — Fundamentos — módulo anterior: Itô, delta hedge e BS
- M03 — Curva de juros — próximo módulo
- Modelagem Estocástica de Séries Temporais Financeiras — simulação de processos estocásticos

## Fontes
1. Karim Khemiri — lições 06 a 08 de `quantitative-trading-free-lesson` (geometric Brownian motion com código, the Greeks, exotic options and path dependence)
2. (PDF) Monte Carlo simulation in financial engineering - ResearchGate — https://www.researchgate.net/publication/4306230_Monte_Carlo_simulation_in_financial_engineering
3. A CONTINUITY CORRECTION FOR DISCRETE BARRIER OPTIONS Columbia Business School, New York Department of Statistics, University of — https://www.columbia.edu/~sk75/mfBGK.pdf
4. A Practical Introduction to Adjoint Algorithmic ... - Martin Burke — https://www.martin-burke.com/articles/adjoint-algorithmic-differentiation/adjoint-algorithmic-differentiation.pdf
5. AAD and least-square Monte Carlo: Fast Bermudan-style options and XVA Greeks — https://ideas.repec.org/a/ris/iosalg/0057.html
6. Accelerated Adjoint Algorithmic Differentiation with Applications in Finance - University of Cape Town — https://open.uct.ac.za/bitstreams/ba43872d-2d54-4700-8fa9-1dc8d93f19ed/download
7. Adjoint Algorithmic Differentiation Tool Support for Typical Numerical Patterns in Computational Finance — https://support.nag.com/doc/techrep/pdf/tr3_14.pdf
8. Adjoints and automatic (algorithmic) differentiation in computational finance - arXiv — https://arxiv.org/pdf/1107.1831
9. Calculation of Monte-Carlo Sensitivities for a portfolio of time coupled options and application to conventional power plants - DuEPublico — https://duepublico2.uni-due.de/servlets/MCRFileNodeServlet/duepublico_derivate_00039914/DissRaabe.pdf
10. Connecting Discrete and Continuous Path-Dependent Options - Columbia Business School — https://business.columbia.edu/sites/default/files-efs/pubfiles/1851/connecting.pdf
11. Discrete Barrier Approximations - Almost Sure — https://almostsuremath.com/2023/07/01/discrete-barrier-approximations/
12. Discrete Barrier and Lookback Options - Columbia University — http://www.columbia.edu/~sk75/HORM15008.pdf
13. Estimating the Greeks - Columbia University — http://www.columbia.edu/~mh2078/MonteCarlo/MCS_Greeks.pdf
14. Fast Correlation Greeks by Adjoint Algorithmic Differentiation | Request PDF - ResearchGate — https://www.researchgate.net/publication/46462759_Fast_Correlation_Greeks_by_Adjoint_Algorithmic_Differentiation
15. Fast Estimates of Greeks from American Options: A Case Study in Adjoint Algorithmic Differentiation - RWTH Aachen University — http://ftp.informatik.rwth-aachen.de/Publications/AIB/2018/2018-02.pdf
16. Fast Greeks by algorithmic differentiation - Luca Capriotti — http://luca-capriotti.net/pdfs/Finance/jcf_capriotti_press_web.pdf
17. Full article: A Crank-Nicolson finite difference approach on the numerical estimation of rebate barrier option prices - Taylor & Francis — https://www.tandfonline.com/doi/full/10.1080/23322039.2019.1598835
18. Generalized Control Variate Methods for Pricing Asian Options Chuan-Hsiang Han — http://mx.nthu.edu.tw/~chhan/gen_AAO.pdf
19. Geometric Asian Option (Kemna-Vorst) Calculator - MetricGate — https://metricgate.com/docs/geometric-asian-option-kemna-vorst/
20. Heston Model Calibration using Adjoint Algorithmic Differentiation - HPC-QuantLib — https://hpcquantlib.wordpress.com/2015/04/01/heston-model-calibration-using-adjoint-algorithmic-differentiation/
21. How to get greeks using Monte-Carlo for arbitrary option? — https://quant.stackexchange.com/questions/3329/how-to-get-greeks-using-monte-carlo-for-arbitrary-option
22. IEOR E4703: Monte-Carlo Simulation - Estimating the Greeks - Columbia University — http://www.columbia.edu/~mh2078/MonteCarlo/MCS_Greeks_MasterSlides.pdf
23. Malliavin Greeks without Malliavin calculus - CUHK — https://www1.se.cuhk.edu.hk/~nchenweb/Publications/malliavin.pdf
24. Monte Carlo pathwise Sensitivities for Barrier Options - Goethe University Frankfurt — https://www.math.uni-frankfurt.de/~harrach/publications/pathwise.pdf
25. Monte Carlo pricing of continuous barrier options with Heston — https://www.acenumerics.com/miscellaneous/monte-carlo-pricing-of-continuously-monitored-barrier-options-with-heston
26. Monte-Carlo Methods for Risk Management - Martin Haugh — https://martin-haugh.github.io/files/QRM/MC_RiskManage.pdf
27. On the data-driven COS method — https://diposit.ub.edu/server/api/core/bitstreams/3e16e0de-1cc5-4b06-9aa0-c95ba4e174c6/content
28. Pricing Derivatives with Barriers in a Stochastic Interest Rate Environment - Research@emlyon business school — https://research.em-lyon.com/view/pdfCoverPage?instCode=33EML_INST&filePid=136183060009453&download=true
29. Pricing Discrete Barrier Options with an Adaptive Mesh Model - NYU Stern — https://people.stern.nyu.edu/sfiglews/documents/DAMM4a.pdf
30. Quasi-Monte Carlo methods for calculating derivatives sensitivities on the GPU - Imperial College London — https://www.imperial.ac.uk/media/imperial-college/faculty-of-engineering/computing/public/distinguished-projects/2122-ug-projects/2122-individual-projects/Quasi-Monte-Carlo-methods-for-calculating-derivatives-sensitivities-on-the-GPU.pdf
31. Quasi-Monte Carlo methods for calculating derivatives sensitivities on the GPU - arXiv — https://arxiv.org/html/2209.11337v1
32. Short Communication: Monte Carlo Expected Wealth and Risk Measure Trade-Off Portfolio Optimization | SIAM Journal on Financial Mathematics — https://epubs.siam.org/doi/10.1137/23M1624439
33. Smoking Adjoints: fast evaluation of Greeks in Monte Carlo calculations - People — https://people.maths.ox.ac.uk/gilesm/files/NA-05-15.pdf
34. Variance Reduction for Asian Options - DiVA portal — https://www.diva-portal.org/smash/get/diva2:238857/FULLTEXT01
35. Variance Reduction for Monte Carlo Methods to Evaluate Option Prices under Multi-factor Stochastic Volatility Models - Jean-Pierre Fouque — https://fouque.faculty.pstat.ucsb.edu/PubliFM/VR_Asian.vncsu.pdf
36. Vibrato Monte Carlo sensitivities - Oxford University Research Archive — https://ora.ox.ac.uk/objects/uuid:dc53ad11-4bd8-480d-9106-7381804c40c2/files/me2fb6279f2ac035e45d1691ba7d9e539
37. Vibrato Monte Carlo sensitivities - People — https://people.maths.ox.ac.uk/gilesm/files/mcqmc08.pdf
38. quasi-monte carlo methods for calculating - arXiv — https://arxiv.org/pdf/2209.11337