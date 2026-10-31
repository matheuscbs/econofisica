<!-- imported study note (overview.md) -->
# M05 — Econofísica: informação, entropia e risco

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M05

> **info**
>
> Módulo 5 de 10 do curso Econofísica Khem Kapital. Pesquisa profunda montada em 2026-10-07 no NotebookLM com 33 fontes: as 4 lições originais de Karim Khemiri (introdução à econofísica, teoria da informação, entropia, risco) e Deep Research (entropia de permutação, transfer entropy, temperatura de mercado, correlação em crises). Notebook `99ac1375-3f57-48c0-8b57-e8a79b777cf8`.

**Pergunta de mercado:** O que a econofísica muda na leitura de incerteza e risco?

**Resultado esperado:** Calcular entropia/collapse/tail density e usar risco agregado (correlação no crash) na decisão de sizing.

!400

## Documentos

| Nota | Tipo | O que tem |
|------|------|-----------|
| Resumo Executivo | Resumo | Visão geral do módulo, mecanismos e por que importa |
| Guia Completo | Relatório | Seções numeradas com teoria, fórmulas, tabelas, Python e glossário |
| Aulas (A01–A04) | Guia de estudo | Cada aula com conceito, lab, exemplo resolvido e questões em 3 níveis |

## Aulas
1. M05.A01 — Introdução à econofísica: difusão, calor e o PDE de BSM
2. M05.A02 — Teoria da informação e entropia: medir incerteza de retornos
3. M05.A03 — Entropia e “temperatura” de mercado: do microestado ao regime
4. M05.A04 — Risco como força: drawdown, correlação e o crash

## Trilha de leitura
1. Resumo Executivo — o mapa do módulo.
2. Aulas na ordem, fazendo o lab e as questões de cada uma.
3. Guia Completo, nas seções-chave:
   - §2 Difusão, calor e a EDP de BS
   - §3 Shannon, informação mútua, transfer entropy
   - §4 Estimação: permutation entropy
   - §6 Temperatura de mercado e regimes
   - §7 Risco como força: drawdown e correlação
   - §8 Sinais de crash
4. Conceitos abaixo, para fixar as definições.

## Conceitos
- Entropia de Shannon — incerteza dos retornos; informação mútua
- Entropia de Permutação — complexidade ordinal, robusta a ruído
- Transfer Entropy — fluxo direcional de informação
- Temperatura de Mercado — volatilidade como temperatura; Boltzmann e regimes
- Drawdown — perda desde o pico; risco de trajetória
- Modelo Black-Scholes — a EDP vira equação do calor

## Mídia
!khem-m05-entropia-risco-podcast.m4a

- Vídeo explicativo: khem-m05-entropia-risco-video.mp4
- Apresentação: PDF · PPTX
- Infográfico: khem-m05-entropia-risco-stories.png

> **note**
>
> ```bash
> NB=99ac1375-3f57-48c0-8b57-e8a79b777cf8
> notebooklm artifact list -n $NB
> notebooklm download audio khem-m05-entropia-risco-podcast.m4a -n $NB
> notebooklm download video khem-m05-entropia-risco-video.mp4 -n $NB
> notebooklm download infographic khem-m05-entropia-risco-stories.png -n $NB
> notebooklm download slide-deck khem-m05-entropia-risco-apresentacao.pdf -n $NB
> notebooklm download slide-deck khem-m05-entropia-risco-apresentacao.pptx --format pptx -n $NB
> # gerar de novo: notebooklm generate audio|video|infographic|slide-deck -n $NB --language pt_BR
> ```

## Mapa conceitual
```
Econofísica: mercado como sistema físico
├── Difusão: EDP de BS → equação do calor (troca de variáveis)
├── Informação
│   ├── Shannon H(X) · condicional · informação mútua
│   ├── estimação: bins, permutation entropy, sample entropy
│   └── transfer entropy: quem lidera quem
├── Termodinâmica de mercado
│   ├── microestados → Boltzmann P ∝ e^(−E/T_m)
│   └── temperatura (vol) e entropia → rótulo de regime
└── Risco como força
    ├── drawdown e duração · correlação ↑ em crises
    └── sinais de crash e fragilidade → M06 (caudas) e M09 (R+/R−)
```

## Relacionadas
- M04 — Superfície de vol — módulo anterior
- M06 — Histerese e caudas — próximo módulo
- Econofísica — pesquisa anterior do vault sobre o mesmo campo, com foco mais amplo
- Séries de Fourier — Regimes de Mercado — outra ferramenta de detecção de regimes

## Fontes
1. Karim Khemiri — lições 18 a 21 de `quantitative-trading-free-lesson` (introduction to econophysics, information theory and entropy, entropy, risk)
2. A Stable and Robust Calibration Scheme of the Log-Periodic Power Law Model - arXiv — https://arxiv.org/abs/1108.0099
3. Black Scholes Derivation from Heat Equation - YouTube — https://www.youtube.com/watch?v=pSDHWT6kbaI
4. Black–Scholes equation - Wikipedia — https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_equation
5. Capturing Bitcoin Market Dynamics: Assessing Advanced Permutation Entropy Metrics as Early-Warning Indicators - CEUR-WS — https://ceur-ws.org/Vol-3988/paper8.pdf
6. Chapter 5 How to Measure Statistical Causality: A Transfer Entropy Approach with Financial Applications | The Open Quant Live Book - Bookdown — https://bookdown.org/souzatharsis/open-quant-live-book/how-to-measure-statistical-causality-a-transfer-entropy-approach-with-financial-applications.html
7. Characterizing Complexity Changes in Chinese Stock Markets by Permutation Entropy — https://www.mdpi.com/1099-4300/19/10/514
8. Diffusion equation and drift-diffusion equation - YouTube — https://www.youtube.com/watch?v=wbi1nQS9bbw
9. Econophysics and the Landauer Principle: A Redefinition of Economic Temperature - PMC — https://pmc.ncbi.nlm.nih.gov/articles/PMC13115127/
10. Effective Transfer Entropy Approach to Information Flow Among EPU, Investor Sentiment and Stock Market - Frontiers — https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2020.00206/full
11. Entropy as a Tool for the Analysis of Stock Market Efficiency During Periods of Crisis - PMC — https://pmc.ncbi.nlm.nih.gov/articles/PMC11675851/
12. Evaluation and Prediction of Stock Market Crash Risk in Mexico Using Log-Periodic Power-Law Modeling - MDPI — https://www.mdpi.com/2227-9091/14/1/3
13. FOKKER-PLANCK- AND LANGEVIN EQUATION - Heidelberg University — https://www.thphys.uni-heidelberg.de/~wolschin/statsem21_6s.pdf
14. Financial Information Theory - arXiv — https://arxiv.org/html/2511.16339v1
15. Fokker–Planck equation - Wikipedia — https://en.wikipedia.org/wiki/Fokker%E2%80%93Planck_equation
16. Fractional Transfer Entropy Networks: Short- and Long-Memory Perspectives on Global Stock Market Interactions - MDPI — https://www.mdpi.com/2504-3110/9/2/69
17. How to predict crashes in financial markets with the Log-Periodic Power Law Examensarbete 2009:7 — https://www2.math.su.se/matstat/reports/serieb/2009/rep7/report.pdf
18. LPPLS for Bubbles in Speculative Markets - QuantConnect — https://www.quantconnect.com/research/20262/lppls-for-bubbles-in-speculative-markets/
19. LPPLS: Log Periodic Power Law Singularity Model for Financial Bubbles - GitHub — https://github.com/sabato96/lppls
20. Langevin Equation and Fokker-Planck Equation — https://www.thphys.uni-heidelberg.de/~wolschin/statsem20_7s.pdf
21. Langevin and Fokker-Planck equation - Heidelberg University — https://www.thphys.uni-heidelberg.de/~wolschin/statsem23_6.pdf
22. Log Periodic Power Law model for the detection of financial bubbles - POLITesi — https://www.politesi.polimi.it/retrieve/c280fa02-ead6-4885-8602-3f6c24dfb6d1/Bonanomi%20-%20Log%20Periodic%20Power%20Law%20model%20for%20the%20detection%20of%20financial%20bubbles.pdf
23. Multiscale Permutation Entropy and Forbidden Patterns for Stock Market Volatility Analysis — https://www.preprints.org/manuscript/202511.1980
24. Phase Transitions in Financial Markets: An Ising Model Approach to Simulating Market Crashes | Sciety — https://sciety.org/articles/activity/10.31219/osf.io/e28mq_v1
25. Physics in Finance? Entropy and Market Efficiency - YouTube — https://www.youtube.com/watch?v=pXhiuqZQB80
26. Prediction accuracy and sloppiness of log-periodic functions — https://sonar.ch/documents/302953/files/cha_pas.pdf
27. Solution of Fokker-Planck equation for a broad class of drift and diffusion coefficients - arXiv — https://arxiv.org/abs/1107.0959
28. Transforming Black Scholes Into the Heat Equation - YouTube — https://www.youtube.com/watch?v=M_eStIqDPHU
29. What's the intuition behind the transformation of Black-Scholes into Heat equation? — https://quant.stackexchange.com/questions/30982/whats-the-intuition-behind-the-transformation-of-black-scholes-into-heat-equati