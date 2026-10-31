<!-- imported from vault study notes; curated for open course -->
# M05.A04 — Risco como força: drawdown, correlação e o crash

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M05
> **Aula:** M05.A04

↑ M05 · Resumo · Completo

**Módulo:** M05
**Pergunta do módulo:** O que a econofísica muda na leitura de incerteza e risco?

## Conceito-núcleo
Analogia f=m·a aplicada a stress: aceleração de perdas, massa (exposição) e correlação no crash.

## Aplicação em mercado / trading
Dimensionar risco agregado; ver como correlação sobe em COVID-like events e invalida diversificação ingênua.

## Entregável / lab
Replay de crash: retornos vs benchmark, correlação rolling e drawdown conjunto.

## Fonte (mapeamento)
quantitative-trading-free-lesson/21 risk | IG f=m·a / drawdown COVID

## Guia de estudo aprofundado

> **info**
>

Este guia de estudos foi estruturado para fornecer uma compreensão rigorosa e avançada sobre a natureza do risco financeiro, transições de regime de mercado, colapso de correlações e a dinâmica mecânica dos *crashes*. O conteúdo baseia-se na premissa de que o risco real não é a mera flutuação de preços, mas a mudança estrutural nas leis de propagação do sistema.

---

### Visão Geral e Conceitos-Chave Explicados em Profundidade

#### O Conceito Fundamental Risco como Mudança na Lei de Propagação
O risco verdadeiro em mercados financeiros não se confunde com a volatilidade ordinária ou com a flutuação diária de preços. O risco real se manifesta no exato instante em que a lei de propagação do sistema se altera: quando aquilo que até então era dissipado pela estrutura passa a ser transmitido e amplificado.

*   **Regime Dissipativo:** Mecanismos locais de mercado operam amortecendo os choques. Um fluxo vendedor agressivo é absorvido pela profundidade do livro de ordens, pela capacidade de balanço dos formadores de mercado (*market makers*) e pela diversificação de estratégias.
*   **Regime Propagativo:** A mecânica local deixa de amortecer e passa a ampliar o choque. Nesse ponto, as ferramentas tradicionais de gestão não sofrem apenas uma "degradação suave"; seu status funcional é alterado. O *hedge* deixa de atuar como proteção e pode distorcer os preços; a diversificação perde a eficácia; a execução transiciona para um ambiente ilíquido e hostil.

#### Ruptura de Regime vs. Flutuação de Preço
Quase todos os erros graves em gestão de risco surgem da incapacidade de diferenciar a medição de uma flutuação da medição de uma ruptura de regime.
*   **Flutuação:** Representa um movimento dentro da mesma lei estatística/estocástica. Métrica como Variância, Value at Risk (VaR) e testes de estresse isolados descrevem amplitudes possíveis *dentro* de um regime dado.
*   **Ruptura:** É a passagem do sistema para outra lei de governança. O erro fatal do gestor não é errar a direção do mercado, mas sim continuar raciocinando sob a premissa de uma lei que deixou de existir.

#### Perda de Dimensionalidade e o Mercado de Fator Único
Em um regime estável e dissipativo, o mercado exibe alta dimensionalidade. Os ativos respondem a múltiplos fatores locais, fundamentos individuais e prêmios de risco distintos. 

Quando o sistema entra em estresse extremo e atinge o ponto de ruptura:
1. A profundidade da liquidez recua bruscamente e a liquidez deixa de ser contínua.
2. As correlações deixam de ser locais e tornam-se estruturais.
3. Fluxos forçados (exiquibilidade mecânica) passam a dominar completamente os fluxos discricionários.
4. Os ativos deixam de responder aos seus fundamentos e passam a ser governados por uma **única restrição dominante** (como necessidade imediata de caixa, desalavancagem compulsória, chamadas de margem ou defesa de colateral).

Nesse estágio, o mercado perde dimensionalidade: ele deixa de reagir de forma granular e passa a executar uma necessidade mecânica uniforme.

#### A Sequência Estrutural do Risco O Preço como Sinal Tardio
O preço é a última variável a reagir. Antes que o preço confirme a crise, a estrutura do sistema já apresenta sinais claros de degradação:
*   Compressão severa de liquidez.
*   Encolhimento e aperto dos balanços das contrapartes.
*   Aumento agudo das interdependências entre ativos.
*   Deformação na velocidade de circulação dos fluxos.
*   Perda de redundância entre contrapartes.

Ler o risco corretamente exige monitorar os mecanismos de absorção (profundidade, capacidade de balanço, viabilidade do *hedge* sem autodistorção e custos de financiamento) antes que a variação abrupta de preço ocorra.

#### A Lógica Regime-First e a Ilusão do Backtest
A regra de ouro da gestão estrutural de risco é: **Identificar o regime $\to$ Adaptar a exposição**.
A prioridade do operador não deve ser a convicção direcional ou a criação de cenários estáticos, mas sim verificar se a exposição atual é compatível com o regime vigente no sistema.

*   **A Ilusão do Backtest:** O desempenho passado não garante estabilidade futura ($Past\ Performance \neq Future\ Stability$). Um *backtest* demonstra apenas como uma estratégia se comportou em um ambiente histórico onde o limiar crítico de ruptura ainda não havia sido cruzado. Tratar métricas condicionais a um regime estável como verdades incondicionais é a raiz dos acidentes financeiros graves.

---

### Formulação Matemática e Formalização

#### 1. Sistema Dinâmico de Absorção vs. Propagação
Podemos modelar o impacto de um choque externo de fluxo $F(t)$ na variação do estado do sistema $x(t)$ (representando retornos ou pressões de liquidez) através de uma equação diferencial linearizada:

$$\frac{dx(t)}{dt} = -\gamma x(t) + F(t)$$

Onde:
*   $\gamma > 0$ representa a **taxa de dissipação/amortecimento** do sistema.
*   Se $\gamma > 0$, o sistema absorve o choque e retorna ao equilíbrio (Regime Dissipativo).
*   Na ocorrência de uma ruptura de regime, a taxa de amortecimento torna-se negativa ($\gamma < 0$), transformada por feedback de desalavancagem e chamadas de margem:

$$\frac{dx(t)}{dt} = |\gamma| x(t) + F(t)$$

Neste estado propagativo, o termo $|\gamma| x(t)$ atua como amplificador, fazendo com que o choque se propague exponencialmente no tempo.

#### 2. Matriz de Covariância e Perda de Dimensionalidade
Seja $\mathbf{\Sigma}$ a matriz de covariância $N \times N$ dos retornos dos ativos no regime estável $R_0$. Ela possui uma decomposição em autovalores e autovetores:

$$\mathbf{\Sigma} = \sum_{i=1}^{N} \lambda_i \mathbf{v}_i \mathbf{v}_i^T$$

Onde os autovalores $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_N$ estão distribuídos de forma relativamente homogênea (alta dimensionalidade).

Sob o regime restrito/propagativo $R_1$, devido à presença de uma restrição dominante comum (fator único $f(t)$ de liquidação forçada), a matriz de correlação $\mathbf{R}$ converge para a matriz unitária $\mathbf{J}_{N \times N}$ (onde $R_{ij} \to 1, \forall i,j$). 

A decomposição espectral no regime $R_1$ resulta em:

$$\lambda_1 \approx \sum_{i=1}^{N} \sigma_i^2 \approx N \cdot \bar{\sigma}^2 \quad \text{e} \quad \lambda_2, \dots, \lambda_N \approx 0$$

A razão de variância explicada pelo primeiro componente principal ($PC_1$) aproxima-se de $100\%$:

$$\text{Variância Explicada por } PC_1 = \frac{\lambda_1}{\sum_{k=1}^{N} \lambda_k} \to 1$$

Isso formaliza matematicamente a **perda de dimensionalidade** do mercado durante um crash.

---

### Intuição de Mercado e Aplicação em Trading

Para um operador ou gestor de portfólio, a transição de um regime dissipativo para um regime propagativo exige uma mudança imediata de postura operacional.

| Dimensão de Análise | Regime Dissipativo (Mercado Estável) | Regime Propagativo (Mercado sob Restrição) |
| :--- | :--- | :--- |
| **Comportamento do Fluxo** | Múltiplas opiniões e visões fundamentais. Fluxos discricionários em equilíbrio. | Fluxo mecânico forçado de venda (chamadas de margem, stop-loss estrutural). |
| **Correlação entre Ativos** | Baixa a moderada. Ativos respondem a choques idiossincráticos. | Altíssima ($1,0$). Ativos descorrelacionados caem simultaneamente. |
| **Execução e Liquidez** | Livro profundo, custos baixos, execução contínua. | Abismo de liquidez (*liquidity hole*), slippage extremo, execução descontínua. |
| **Eficácia do Hedge** | Proteções locais funcionam perfeitamente. | O *hedge* se autodistorce; vender o ativo de proteção gera impacto adverso severo. |
| **Foco do Trader** | Conviction, valuation, direção do ativo, Alpha local. | Compatibilidade da exposição, acesso a caixa, funding, estabilidade da margem. |

---

### Exemplo Numérico Resolvido Passo a Passo

#### Cenário
Considere um portfólio composto por dois ativos ($A$ e $B$) alocados em pesos iguais ($w_A = 0{,}5$, $w_B = 0{,}5$). O gestor utiliza métricas históricas calculadas em um **Regime Normal (Dissipativo)** e deseja avaliar o risco real quando o mercado transiciona para um **Regime de Estresse (Propagativo/Fator Único)**.

##### Parâmetros do Regime 1 (Dissipativo - Normalidade)
*   Volatilidade do Ativo A ($\sigma_A$): $15\%$ ao ano
*   Volatilidade do Ativo B ($\sigma_B$): $20\%$ ao ano
*   Correlação entre A e B ($\rho_{AB}$): $0{,}10$

##### Parâmetros do Regime 2 (Propagativo - Crash/Liquidação Forçada)
*   Devido à alta velocidade de propagação e desalavancagem, as volatilidades sobem: $\sigma_A^* = 35\%$, $\sigma_B^* = 45\%$
*   Devido à necessidade dominante de caixa, a correlação colapsa para um fator único: $\rho_{AB}^* = 0{,}95$

---

#### Passo 1 Calcular a Volatilidade do Portfólio no Regime 1 ($\sigma_{p,1}$)

A fórmula da volatilidade do portfólio de dois ativos é:

$$\sigma_p = \sqrt{w_A^2 \sigma_A^2 + w_B^2 \sigma_B^2 + 2 w_A w_B \sigma_A \sigma_B \rho_{AB}}$$

Substituindo os valores do Regime 1:

$$\sigma_{p,1} = \sqrt{(0{,}5)^2 (0{,}15)^2 + (0{,}5)^2 (0{,}20)^2 + 2 (0{,}5) (0{,}5) (0{,}15) (0{,}20) (0{,}10)}$$

$$\sigma_{p,1} = \sqrt{0{,}25 (0{,}0225) + 0{,}25 (0{,}0400) + 0{,}50 (0{,}0030)}$$

$$\sigma_{p,1} = \sqrt{0{,}005625 + 0{,}010000 + 0{,}001500} = \sqrt{0{,}017125} \approx 0{,}13086 \text{ ou } 13{,}09\%$$

---

#### Passo 2 Calcular a Volatilidade do Portfólio no Regime 2 ($\sigma_{p,2}$)

Substituindo os valores de crise do Regime 2:

$$\sigma_{p,2} = \sqrt{(0{,}5)^2 (0{,}35)^2 + (0{,}5)^2 (0{,}45)^2 + 2 (0{,}5) (0{,}5) (0{,}35) (0{,}45) (0{,}95)}$$

$$\sigma_{p,2} = \sqrt{0{,}25 (0{,}1225) + 0{,}25 (0{,}2025) + 0{,}50 (0{,}149625)}$$

$$\sigma_{p,2} = \sqrt{0{,}030625 + 0{,}050625 + 0{,}0748125} = \sqrt{0{,}1560625} \approx 0{,}39505 \text{ ou } 39{,}51\%$$

---

#### Passo 3 Análise do Erro de Redução de Risco (Ilusão da Diversificação)

Se o gestor assumir que as métricas do Regime 1 são incondicionais e perpétuas, ele estimará que o risco da carteira é de apenas $13{,}09\%$.

A variação do risco real sob a mudança de regime é calculada como:

$$\text{Aumento Real do Risco} = \frac{\sigma_{p,2} - \sigma_{p,1}}{\sigma_{p,1}} = \frac{39{,}51\% - 13{,}09\%}{13{,}09\%} \approx 201{,}83\%$$

**Conclusão do Exemplo:** O risco do portfólio triplicou ($+201{,}83\%$). O benefício da diversificação esperado pelo operador desapareceu virtualmente porque a correlação saltou de $0{,}10$ para $0{,}95$, impulsionada pela restrição única de liquidez que governou ambos os ativos simultaneamente.

---

### Armadilhas Comuns

1.  **Confundir Flutuação de Preço com Ruptura de Estrutura:**
    *   *Falha:* Acreditar que uma queda de $5\%$ no preço de um ativo significa apenas um movimento de cauda estatística dentro da normalidade, ignorando que o livro de ordens se esvaziou e os custos de financiamento dobraram.
2.  **Tratar Métricas Condicionais como Incondicionais:**
    *   *Falha:* Utilizar matrizes de correlação de longo prazo, índices Sharpe ou métricas de VaR calculadas em períodos calmos para calibrar o tamanho da posição durante momentos de estresse mecânico.
3.  **Acreditar na Diversificação Nominal Durante Crashes:**
    *   *Falha:* Manter um portfólio com dezenas de ativos sob a falsa premissa de diversificação, ignorando que, sob restrição dominante de margem, todos os ativos serão vendidos em massa, apresentando correlação próxima de $1{,}0$.
4.  **Focar Exclusivamente na Direção do Preço (Conviction/Scenario):**
    *   *Falha:* Priorizar teses macroeconômicas ou fundamentais ("o ativo está barato") enquanto a mecânica de execução e liquidez do mercado está destruindo o balanço da contraparte.
5.  **Afiliações Cegas a Backtests Históricos:**
    *   *Falha:* Assumir que, porque uma estratégia não quebrou nos últimos 10 anos de dados históricos, ela é imune ao risco de ruína. O *backtest* não projeta o limiar em que o sistema altera sua lei de propagação.

---

### Laboratório Prático Sugerido em Python

Este laboratório descreve passo a passo como construir um algoritmo em Python capaz de detectar a mudança de regime de mercado por meio do monitoramento da **perda de dimensionalidade** da matriz de correlação e da variação do primeiro componente principal ($PC_1$).

#### Roteiro de Implementação em Passos

1.  **Obtenção e Preparação dos Dados:**
    *   Carregar séries temporais de preços diários para um universo diversificado de ativos (ex: $10$ a $20$ ativos cobrindo ações, títulos, commodities e moedas).
    *   Calcular os retornos logarítmicos diários: $r_t = \ln(P_t / P_{t-1})$.

2.  **Construção da Janela Móvel de Correlação (*Rolling Correlation*):**
    *   Definir uma janela temporal curta (ex: $21$ dias úteis) para capturar dinâmicas de curto prazo sem diluir o estresse recente.
    *   Para cada ponto no tempo $t$, calcular a matriz de correlação $R_t$ do universo de ativos.

3.  **Decomposição Espectral e Cálculo de Componentes Principais (PCA):**
    *   Em cada janela $t$, aplicar a Análise de Componentes Principais (PCA) na matriz $R_t$.
    *   Extrair os autovalores $\lambda_1, \lambda_2, \dots, \lambda_N$.
    *   Calcular a taxa de variância explicada pelo primeiro autovalor:
        $$\text{Razão } PC_1(t) = \frac{\lambda_1(t)}{\sum_{i=1}^{N} \lambda_i(t)}$$

4.  **Mapeamento e Indicador de Mudança de Regime:**
    *   Estabelecer um limiar crítico (ex: quando $\text{Razão } PC_1 > 65\%$).
    *   Monitorar a taxa de variação ($\Delta$) do $PC_1$. Acelerações abruptas na concentração da variância sinalizam o colapso do regime dissipativo e a emergência do mercado de fator único.

5.  **Simulação do Gatilho de Adaptação de Exposição:**
    *   Criar uma regra simples: Se $\text{Razão } PC_1$ ultrapassar o limiar crítico, o algoritmo deve gerar um sinal automático de redução de alavancagem/exposição bruta, independentemente do sinal direcional dos modelos de tendência ou valor.

---

### Glossário

*   **Capacidade de Balanço (*Balance-Sheet Capacity*):** A disposição e capacidade financeira dos intermediários (como *prime brokers* e *market makers*) para absorver riscos e manter posições do outro lado do mercado.
*   **Desalavancagem Compulsória (*Forced Deleveraging*):** Processo em que participantes do mercado são obrigados a vender ativos a qualquer preço para cumprir chamadas de margem ou requisitos de liquidez.
*   **Lei de Propagação:** O conjunto de regras dinâmicas e estruturais que governa como o impacto de uma ordem ou choque externo se espalha pelo sistema financeiro.
*   **Mercado de Fator Único (*One-Factor Market*):** Condição extrema de estresse em que todas as características individuais dos ativos são suplantadas por uma única restrição dominante (ex: busca desenfreada por caixa).
*   **Perda de Dimensionalidade:** Fenômeno estatístico no qual o número de vetores independentes que explicam a variação do mercado cai drasticamente, fazendo com que ativos variados passem a se mover em uníssono.
*   **Regime Dissipativo:** Estado do mercado em que choques de oferta e demanda são amortecidos e absorvidos pelos mecanismos locais de liquidez.
*   **Regime Propagativo:** Estado do mercado em que choques são amplificados pelos mecanismos da própria estrutura, gerando reações em cadeia e *crashes*.
*   **Ruptura de Regime (*Regime Rupture*):** A transição desfeita e descontínua entre duas leis dinâmicas distintas de funcionamento do mercado.
*   **Velocidade de Circulação:** A rapidez com que o fluxo de ordens e obrigações de liquidação se desloca entre as contrapartes do sistema.

---

### Questões de Fixação e Prática

#### Nível 1 Resposta Curta (Conceitual)

##### Questão 1.1
Qual é a diferença fundamental entre uma flutuação de preço e uma ruptura de regime?

*   **Resposta:** Uma flutuação de preço é um movimento que ocorre dentro das regras estatísticas de um regime mantido (uma variação dentro da mesma lei). Uma ruptura de regime é a transição do sistema para uma nova lei dinâmica, onde os mecanismos que antes dissipavam os choques passam a amplificá-los.

##### Questão 1.2
O que faz com que um mercado diversificado se transforme em um "mercado de fator único" durante um crash?

*   **Resposta:** Durante um crash sob estresse extremo, os ativos deixam de responder aos seus fundamentos individuais porque todos os participantes passam a ser governados por uma única restrição mecânica dominante (como necessidade imediata de caixa ou chamadas de margem), forçando vendas simultâneas e indiscriminadas.

##### Questão 1.3
Por que a variação observada no preço é considerada um indicador tardio de risco?

*   **Resposta:** Porque a deterioração do risco ocorre primeiramente na estrutura subjacente (compressão de liquidez, aperto do balanço das contrapartes e perda de redundância). O preço apenas torna visível a mudança que já ocorreu na arquitetura do sistema.

---

#### Nível 2 Aplicação e Análise

##### Questão 2.1
Explique por que um *backtest* tradicional não consegue prever o momento em que um sistema financeiro mudará de regime.

*   **Resposta:** O *backtest* avalia o desempenho histórico de uma estratégia dentro de um conjunto de dados onde as regras do regime passado estavam operando. Ele não possui capacidade intrínseca de identificar os limiares críticos estruturais (*tipping points*) nos quais a lei do sistema muda. O *backtest* enxerga a história apenas no trecho em que o limite ainda não foi cruzado.

##### Questão 2.2
Um gestor possui um portfólio neutro em mercado com ordens de *hedge* posicionadas para mitigar riscos de queda. Durante uma crise de liquidez, ele percebe que o próprio *hedge* está exacerbando as perdas da carteira. Com base nos conceitos do texto, o que está acontecendo?

*   **Resposta:** O mercado transicionou de um regime dissipativo para um regime propagativo. Nesse novo estado, a execução do *hedge* deixou de absorver impacto e passou a gerar autodistorção nos preços, transformando a proteção em um vetor adicional de amplificação do choque devido à falta de profundidade do livro e iliquidez generalizada.

---

#### Nível 3 Dissertativas para Aprofundamento

##### Questão 3.1
Sintetize a lógica "*Regime-First*" e contraste-a com a abordagem tradicional de gestão de riscos focada em previsão direcional e cenários. Por que a prioridade do gestor deve ser a compatibilidade da exposição com o regime vigente?

*   **Guia de Resposta / Critérios de Avaliação:**
    *   **Análise Conceitual:** O candidato deve destacar que a gestão tradicional foca em acertar a direção do preço (alta/baixa) ou criar cenários baseados em probabilidades passadas. A lógica *Regime-First* coloca a identificação do estado do sistema em primeiro lugar (`identificar o regime -> adaptar a exposição`).
    *   **Mecânica Estrutural:** Explicar que em um regime dissipativo é viável carregar posições mais finas, alavancadas ou com convexidade curta, pois o sistema absorve ruídos. Em um regime propagativo, qualquer exposição que amplifique a restrição dominante causará ruína, independentemente da convicção do operador no fundamento do ativo.
    *   **Conclusão:** A compatibilidade da exposição com a lei vigente do sistema garante a sobrevivência operacional, superando previsões subjetivas de preço.

##### Questão 3.2
Discuta como a compressão dos balanços dos intermediários financeiros e o aumento da velocidade de circulação dos fluxos afetam a transição do estado de amortecimento local para a amplificação de choques no mercado.

*   **Guia de Resposta / Critérios de Avaliação:**
    *   **Papel dos Balanços:** O candidato deve expor que os formadores de mercado precisam de espaço de balanço livre para absorver fluxos pontuais de venda. Quando o balanço é contraído (por regulamentação, perda de capital ou risco), esses agentes recuam a liquidez.
    *   **Velocidade de Circulação:** Explicar que a aceleração na velocidade com que exigências de liquidez (margem/garantias) são cobradas faz com que os choques viagem mais rápido do que a capacidade natural do mercado de encontrar compradores discricionários.
    *   **Resultado:** A combinação de balanços contraídos e circulação acelerada destrói a dissipação local e aciona a propagação em cadeia do choque financeiro.