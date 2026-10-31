<!-- imported study note (overview.md) -->
# M08 — Variância que propaga (ponte aos labs)

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M08

> **info**
>
> Módulo 8 de 10 do curso Econofísica Khem Kapital. Pesquisa profunda montada em 2026-10-07 no NotebookLM com 23 fontes: a lição original de Karim Khemiri (ARCH/GARCH, com código) e Deep Research (estimação, GJR/EGARCH, avaliação de previsão, volatility targeting). Notebook `745fbd16-6da1-4ddb-9713-81c9763d72ba`.

**Pergunta de mercado:** Como a variância propaga e prepara regras de regime?

**Resultado esperado:** Ajustar GARCH e usar σ_t condicional como input de regime — preparando a lei assinada do Janus.

!400

## Documentos

| Nota | Tipo | O que tem |
|------|------|-----------|
| Resumo Executivo | Resumo | Visão geral do módulo, mecanismos e por que importa |
| Guia Completo | Relatório | Seções numeradas com teoria, fórmulas, tabelas, Python e glossário |
| Aulas (A01) | Guia de estudo | Cada aula com conceito, lab, exemplo resolvido e questões em 3 níveis |

## Aulas
1. M08.A01 — ARCH/GARCH: a variância não some — ela propaga

## Trilha de leitura
1. Resumo Executivo — o mapa do módulo.
2. Aulas na ordem, fazendo o lab e as questões de cada uma.
3. Guia Completo, nas seções-chave:
   - §1 Fatos estilizados
   - §3 GARCH(1,1), persistência e meia-vida
   - §4 Máxima verossimilhança e diagnósticos
   - §5 GJR, EGARCH e t
   - §6 Previsão
   - §7 σ_t como regime e ponte ao Janus
4. Conceitos abaixo, para fixar as definições.

## Conceitos
- Modelo GARCH — variância condicional que propaga choques
- Volatility Targeting — exposição ∝ σ*/σ̂
- Caudas Gordas — fato estilizado que o GARCH com t ajuda a capturar

## Mídia
!khem-m08-garch-podcast.m4a

- Vídeo explicativo: khem-m08-garch-video.mp4
- Apresentação: PDF · PPTX
- Infográfico: khem-m08-garch-stories.png

> **note**
>
> ```bash
> NB=745fbd16-6da1-4ddb-9713-81c9763d72ba
> notebooklm artifact list -n $NB
> notebooklm download audio khem-m08-garch-podcast.m4a -n $NB
> notebooklm download video khem-m08-garch-video.mp4 -n $NB
> notebooklm download infographic khem-m08-garch-stories.png -n $NB
> notebooklm download slide-deck khem-m08-garch-apresentacao.pdf -n $NB
> notebooklm download slide-deck khem-m08-garch-apresentacao.pptx --format pptx -n $NB
> # gerar de novo: notebooklm generate audio|video|infographic|slide-deck -n $NB --language pt_BR
> ```

## Mapa conceitual
```
A variância não some: ela propaga
├── Fatos estilizados: clustering · caudas · alavancagem
├── ARCH(q) → GARCH(1,1): σ²_t = ω + α ε²_{t−1} + β σ²_{t−1}
│   ├── persistência α+β · variância incondicional · meia-vida
│   └── MLE (normal / t) · Ljung-Box nos resíduos²
├── Assimetria: GJR (γ·1[ε<0]) · EGARCH (ln σ²)
├── Previsão: reversão a σ̄² com taxa (α+β)^h · QLIKE, Mincer-Zarnowitz
└── σ_t condicional como input
    ├── volatility targeting
    └── regime → lei assinada de resposta à variância (Janus, M10)
```

## Relacionadas
- M07 — Portfólio e fatores — módulo anterior
- M09 — Labs — próximo módulo; a variância vira estressor do classificador R+/R−
- Modelagem Estocástica de Séries Temporais Financeiras — ARCH/GARCH na modelagem de séries

## Fontes
1. Karim Khemiri — lição 28 de `quantitative-trading-free-lesson` (ARCH/GARCH: variance does not disappear, it propagates), com código
2. (PDF) Evaluating Volatility and Correlation Forecasts - ResearchGate — https://www.researchgate.net/publication/24127105_Evaluating_Volatility_and_Correlation_Forecasts
3. (PDF) Markov-Switching GARCH Models in R: The MSGARCH Package - ResearchGate — https://www.researchgate.net/publication/325359792_Markov-Switching_GARCH_Models_in_R_The_MSGARCH_Package
4. A New Approach to Markov-Switching GARCH Models - EconPapers — https://econpapers.repec.org/RePEc:oup:jfinec:v:2:y:2004:i:4:p:493-530
5. Evaluating Volatility Forecasting Performance at Different Horizons - Erasmus University Thesis Repository — https://thesis.eur.nl/pub/38661/Li-X.-422186-.pdf
6. Evaluating exponential GARCH models - S-WoPEc — https://swopec.hhs.se/hastef/papers/hastef0564.pdf
7. Forecasting risk with Markov-switching GARCH models: A large-scale performance study - Pure — https://pure.au.dk/ws/files/137371173/Forecasting_risk_with_markov_switching_garch_models_VOR18.pdf
8. Interpreting QLIKE and MSE Loss function (Patton 2011) - Cross Validated - Stack Exchange — https://stats.stackexchange.com/questions/225877/interpreting-qlike-and-mse-loss-function-patton-2011
9. MSGARCH-package function - RDocumentation — https://www.rdocumentation.org/packages/MSGARCH/versions/0.17/topics/MSGARCH-package
10. Markov-Switching GARCH Models in R: The MSGARCH Package - Journal of Statistical Software — https://www.jstatsoft.org/article/view/v091i04/1321
11. Modelling Volatility with Markov-Switching GARCH Models - University of Liverpool Repository — https://livrepository.liverpool.ac.uk/3163032/1/201208298_Aug2022.pdf
12. Multi-Scale Markov-Switching GARCH:Volatility Regime Detection in EUR/USD - arXiv — https://arxiv.org/html/2606.06190v1
13. Persistence in Variance, Structural Change, and the GARCH Model - EconPapers — https://econpapers.repec.org/RePEc:bes:jnlbes:v:8:y:1990:i:2:p:225-34
14. Real-time GARCH: Modelling and forecasting the tail behaviour of asset returns* — https://www.finance.group.cam.ac.uk/system/files/documents/copy_of_Second_Revision_Manuscript_JFEC_2015_044_Smetanina_Ekaterina.pdf
15. Using Proxies to Improve Forecast Evaluation - arXiv — https://arxiv.org/pdf/2109.02432
16. VOLATILITY REGIMES OF SELECTED CENTRAL EUROPEAN STOCK RETURNS: A MARKOV SWITCHING GARCH APPROACH - VILNIUS TECH journals — https://journals.vilniustech.lt/index.php/JBEM/article/download/16648/11094
17. Volatility Forecast Comparison using Imperfect Volatility Proxies - National Bureau of Economic Research — https://users.nber.org/~confer/2006/si2006/efww/patton.pdf
18. Volatility Forecasting - gupea — https://gupea.ub.gu.se/bitstreams/7c20fc0f-c435-4e66-b204-663b4953c6a3/download
19. Volatility forecast comparison using imperfect volatility proxies - Duke Economics — https://public.econ.duke.edu/~ap172/Patton_vol_proxies_JoE_2011.pdf
20. Volatility forecast comparison using imperfect volatility proxies - EconPapers — https://econpapers.repec.org/RePEc:eee:econom:v:160:y:2011:i:1:p:246-256
21. Volatility forecast comparison using imperfect volatility proxies - IDEAS/RePEc — https://ideas.repec.org/a/eee/econom/v160y2011i1p246-256.html