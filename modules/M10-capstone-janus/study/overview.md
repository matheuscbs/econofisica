<!-- imported study note (overview.md) -->
# M10 — Capstone: sistema frágil/antifrágil com regimes (Janus)

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M10

> **info**
>
> Módulo 10 de 10 do curso Econofísica Khem Kapital. Pesquisa profunda montada em 2026-10-07 no NotebookLM com 24 fontes: o repositório `janus-anti-fragility-strategy` de Karim Khemiri (README, `mass.md`, `strat.md`, papers `mass neg.pdf` e `jpp papers.pdf`) e Deep Research (antifragilidade, regimes, Ashby, hedge convexo). Notebook `9625a739-548b-49c2-95eb-49083a981778`.

**Pergunta de mercado:** Como construir alocação frágil/antifrágil com consciência de regime?

**Resultado esperado:** Entregar um pipeline completo de resposta à variância → regime → alocação defasada → hedge, com métricas.

!400

## Documentos

| Nota | Tipo | O que tem |
|------|------|-----------|
| Resumo Executivo | Resumo | Visão geral do módulo, mecanismos e por que importa |
| Guia Completo | Relatório | Seções numeradas com teoria, fórmulas, tabelas, Python e glossário |
| Aulas (A01–A02) | Guia de estudo | Cada aula com conceito, lab, exemplo resolvido e questões em 3 níveis |

## Aulas
1. M10.A01 — Capstone — Lei assinada de resposta à variância (Janus)
2. M10.A02 — Capstone — Alocação defasada, hedge e variedade necessária

## Trilha de leitura
1. Resumo Executivo — o mapa do módulo.
2. Aulas na ordem, fazendo o lab e as questões de cada uma.
3. Guia Completo, nas seções-chave:
   - §1 Integração M01–M09
   - §2 Lei assinada
   - §3 Massa positiva e negativa
   - §5 Alocação defasada
   - §6 Hedge e convexidade
   - §8 Métricas e backtest
4. Conceitos abaixo, para fixar as definições.

## Conceitos
- Estratégia Janus — resposta assinada à variância → densidades → troca R+→R− defasada
- Classificador R+ e R− — as pernas frágil e antifrágil (do M09)
- Lei da Variedade Necessária — o controlador precisa de tantos modos quanto o mercado
- Volatility Targeting — dimensionamento por σ (do M08)
- Modelo GARCH — σ²_t como energia de variância (do M08)

## Mídia
!khem-m10-capstone-janus-podcast.m4a

- Vídeo explicativo: khem-m10-capstone-janus-video.mp4
- Apresentação: PDF · PPTX
- Infográfico: khem-m10-capstone-janus-stories.png

> **note**
>
> ```bash
> NB=9625a739-548b-49c2-95eb-49083a981778
> notebooklm artifact list -n $NB
> notebooklm download audio khem-m10-capstone-janus-podcast.m4a -n $NB
> notebooklm download video khem-m10-capstone-janus-video.mp4 -n $NB
> notebooklm download infographic khem-m10-capstone-janus-stories.png -n $NB
> notebooklm download slide-deck khem-m10-capstone-janus-apresentacao.pdf -n $NB
> notebooklm download slide-deck khem-m10-capstone-janus-apresentacao.pptx --format pptx -n $NB
> # gerar de novo: notebooklm generate audio|video|infographic|slide-deck -n $NB --language pt_BR
> ```

## Mapa conceitual
```
Capstone Janus: variância → regime → alocação → hedge
├── Medida: R_excess = α − β σ²_t
│   ├── β > 0 → arrasto frágil
│   └── β < 0 → "massa financeira negativa"
├── Sinais móveis + estresse causal → densidades ρ+ e ρ−
│   └── balanço H₂⁺ = ρ+ − ρ−
├── Regime confirmado (H₂⁺ < 0) → troca R+ (crescimento) → R− (pressão)
│   └── com 1 período de defasagem (sem look-ahead)
├── Pares: SPY/GLD · QQQ/GLD (AAPL/GLD = generalização)
└── Avaliação: custos · robustez · benchmark · Ashby (variedade de modos)
```

## Relacionadas
- M09 — Labs — módulo anterior; classificador R+/R−
- M01 — Fundamentos — início do curso
- Econofísica — a metáfora física por trás do Janus

## Fontes
1. Karim Khemiri — repositório `janus-anti-fragility-strategy` (GitHub `karimkhemkapital`)
2. (PDF) Mathematical Definition, Mapping, and Detection of (Anti)Fragility - ResearchGate — https://www.researchgate.net/publication/230609579_Mathematical_Definition_Mapping_and_Detection_of_AntiFragility
3. 9. Systems Thinking and 'Ashby's Law of Requisite Variety' – HES 2020-2026 — https://harmonious-entrepreneurship.org/9-systems-thinking-and-ashbys-law-of-requisite-variety/
4. Ashby's Law of Requisite Variety - Intelligent Organisations — https://intelligente-organisationen.de/ashbys-law-of-requisite-variety
5. Ashby's Law of Requisite Variety | Think Insights — https://thinkinsights.net/strategy/ashbys-law-requisite-variety
6. Computational Mechanics: Pattern and Prediction, Structure and Simplicity - Cosma Shalizi — https://bactra.org/research/cmppss.pdf
7. Derivatives and the Wealth of Societies 9780226392974 - DOKUMEN.PUB — https://dokumen.pub/derivatives-and-the-wealth-of-societies-9780226392974.html
8. Erik Kole - Erasmus Universiteit Rotterdam — https://personal.eur.nl/kole/CV2.pdf
9. Extreme Events in Finance: A Handbook of Extreme Value Theory and Its Applications 9781118650196, 9781118650202, 1118650190 - DOKUMEN.PUB — https://dokumen.pub/extreme-events-in-finance-a-handbook-of-extreme-value-theory-and-its-applications-9781118650196-9781118650202-1118650190.html
10. Fragility audit — Judgment Playbook - decidenda — https://www.decidenda.com/method/fragility-audit
11. Handbook of Ethics of Islamic Economics and Finance — https://api.pageplace.de/preview/DT0400.9783110593419_A40199663/preview-9783110593419_A40199663.pdf
12. Mathematical Definition, Mapping, and Detection of (Anti)Fragility - IDEAS/RePEc — https://ideas.repec.org/p/arx/papers/1208.1189.html
13. Mathematical Definition, Mapping, and Detection of (Anti)Fragility - IDEAS/RePEc — https://ideas.repec.org/p/mse/cesdoc/14093.html
14. On the Cognitive Surprise in Risk Management: An Analysis of the Value-at-Risk (VaR) Historical | Request PDF - ResearchGate — https://www.researchgate.net/publication/275891367_On_the_Cognitive_Surprise_in_Risk_Management_An_Analysis_of_the_Value-at-Risk_VaR_Historical
15. Planetary Antifragility: A new dimension in the definition of the Safe Operating Space for Humanity - ESD — https://esd.copernicus.org/preprints/esd-2021-26/esd-2021-26-manuscript-version5.pdf
16. Sustaining in Uncertain Time: Investigating Pension Fund Performance during Market Stress — https://www.researchgate.net/publication/389414750_Sustaining_in_Uncertain_Time_Investigating_Pension_Fund_Performance_during_Market_Stress
17. Table of Contents - Journals ISSS — https://journals.isss.org/index.php/proceedings62nd/article/download/3652/1164/12377
18. [1208.1189] Mathematical Definition, Mapping, and Detection of (Anti)Fragility - arXiv — https://arxiv.org/abs/1208.1189
19. ‪Raphael Douady‬ - ‪Google Scholar‬ — https://scholar.google.com/citations?user=2jTLF8kAAAAJ&hl=en