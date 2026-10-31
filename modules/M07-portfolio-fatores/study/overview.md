<!-- imported study note (overview.md) -->
# M07 — Portfólio: da geometria Markowitz aos fatores

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M07

> **info**
>
> Módulo 7 de 10 do curso Econofísica Khem Kapital. Pesquisa profunda montada em 2026-10-07 no NotebookLM com 16 fontes: as 4 lições originais de Karim Khemiri (Markowitz com código, CAPM, Black-Litterman com código, APT) e pesquisa web em modo rápido (a cota de Deep Research estava esgotada). Notebook `9fba3184-035c-4b37-8809-abc057cf4a6c`.

**Pergunta de mercado:** Como alocar além do μ ingênuo e do “alpha” ilusório?

**Resultado esperado:** Construir fronteira, interpretar CAPM, aplicar BL com views e decompor “alpha” em fatores (APT).

!400

## Documentos

| Nota | Tipo | O que tem |
|------|------|-----------|
| Resumo Executivo | Resumo | Visão geral do módulo, mecanismos e por que importa |
| Guia Completo | Relatório | Seções numeradas com teoria, fórmulas, tabelas, Python e glossário |
| Aulas (A01–A04) | Guia de estudo | Cada aula com conceito, lab, exemplo resolvido e questões em 3 níveis |

## Aulas
1. M07.A01 — Markowitz: geometria risco–retorno e a fronteira eficiente
2. M07.A02 — CAPM: o que o mercado paga (e o que não paga)
3. M07.A03 — Black–Litterman: views explícitas no lugar de μ solto
4. M07.A04 — APT e multifatores: quando “alpha” era beta que faltava

## Trilha de leitura
1. Resumo Executivo — o mapa do módulo.
2. Aulas na ordem, fazendo o lab e as questões de cada uma.
3. Guia Completo, nas seções-chave:
   - §1 Geometria da fronteira
   - §3 Tangente e CML
   - §4 CAPM e evidência
   - §6 APT, Fama-French, momentum
   - §7 Alpha vs beta oculto
   - §8 Python e checklist
4. Conceitos abaixo, para fixar as definições.

## Conceitos
- Fronteira Eficiente de Markowitz — média-variância, tangente e erro de estimação
- CAPM — só o beta de mercado é pago
- Modelo Black-Litterman — equilíbrio + views com confiança
- APT e Modelos Multifatoriais — fatores, atribuição e alpha real

## Mídia
!khem-m07-portfolio-fatores-podcast.m4a

- Vídeo explicativo: khem-m07-portfolio-fatores-video.mp4
- Apresentação: PDF · PPTX
- Infográfico: khem-m07-portfolio-fatores-stories.png

> **note**
>
> ```bash
> NB=9fba3184-035c-4b37-8809-abc057cf4a6c
> notebooklm artifact list -n $NB
> notebooklm download audio khem-m07-portfolio-fatores-podcast.m4a -n $NB
> notebooklm download video khem-m07-portfolio-fatores-video.mp4 -n $NB
> notebooklm download infographic khem-m07-portfolio-fatores-stories.png -n $NB
> notebooklm download slide-deck khem-m07-portfolio-fatores-apresentacao.pdf -n $NB
> notebooklm download slide-deck khem-m07-portfolio-fatores-apresentacao.pptx --format pptx -n $NB
> # gerar de novo: notebooklm generate audio|video|infographic|slide-deck -n $NB --language pt_BR
> ```

## Mapa conceitual
```
Alocação: além do μ ingênuo
├── Markowitz: min wᵀΣw → fronteira eficiente
│   ├── + ativo livre → CML e portfólio tangente Σ⁻¹(μ − r_f)
│   └── problema: erro em μ → encolhimento, restrições
├── CAPM: E[R] − r_f = β (E[R_m] − r_f)
│   └── SML achatada na prática → betting against beta
├── Black-Litterman: Π = δΣw_mkt + views (P, Q, Ω, τ)
└── APT / multifatores: MKT, SMB, HML, RMW, CMA, UMD
    └── "alpha" = beta que faltava → atribuição de performance
```

## Relacionadas
- M06 — Histerese e caudas — módulo anterior
- M08 — GARCH — próximo módulo
- WACC, VPL e CAPM — o CAPM do lado do custo de capital
- Factor Investing — fatores como estratégia de investimento
- Inside the Black Box — construção de portfólio em sistemas quant

## Fontes
1. Karim Khemiri — lições 24 a 27 de `quantitative-trading-free-lesson` (Markowitz, CAPM, Black-Litterman, APT), com código
2. A STEP-BY-STEP GUIDE TO THE BLACK-LITTERMAN MODEL Incorporating user-specified confidence levels — https://people.duke.edu/~charvey/Teaching/BA453_2006/Idzorek_onBL.pdf
3. Black-Litterman Allocation — PyPortfolioOpt 1.5.4 documentation — https://pyportfolioopt.readthedocs.io/en/latest/BlackLitterman.html
4. Data Mining, Performance Chasing, and the Quest for Real Returns - FEG Investment Advisors — https://www.feg.com/hubfs/2017%20Forum/Presentations/FEG%202017%20Investment%20Forum%20-%20Rob%20Arnott%20-%20CME%20Smart%20Beta%20Research.pdf
5. Fama and French: The Five-Factor Model Revisited - CFA Institute Research and Policy Center — https://rpc.cfainstitute.org/blogs/enterprising-investor/2022/fama-and-french-the-five-factor-model-revisited
6. Five Concerns with the Five-Factor Model - Robeco.com — https://www.robeco.com/docm/docu-five-concerns-with-the-five-factor-model-2018.pdf
7. Mean-Variance Portfolio Optimization: Challenging the role of traditional covariance estimation - DiVA portal — https://www.diva-portal.org/smash/get/diva2:1060405/FULLTEXT01.pdf
8. Shrinkage Estimators for Mean and Covariance: Evidence on Portfolio Efficiency Across Market Dimensions - arXiv — https://arxiv.org/pdf/2601.20643
9. The Arbitrage Pricing Theory and Multifactor Models of Asset Returns* - Kellogg School of Management — https://www.kellogg.northwestern.edu/faculty/korajczy/ftp/wp139.pdf
10. The Lost Capital Asset Pricing Model - Julien Cujean — http://www.juliencujean.com/ACW2023.pdf
11. The amendment and empirical test of arbitrage pricing models - EconStor — https://www.econstor.eu/bitstream/10419/49031/1/665970145.pdf