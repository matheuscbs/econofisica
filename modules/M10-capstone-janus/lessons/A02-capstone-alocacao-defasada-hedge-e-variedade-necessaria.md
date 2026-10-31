<!-- imported from vault study notes; curated for open course -->
# M10.A02 — Capstone — Alocação defasada, hedge e variedade necessária

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M10
> **Aula:** M10.A02

↑ M10 · Resumo · Completo

**Módulo:** M10
**Pergunta do módulo:** Como construir alocação frágil/antifrágil com consciência de regime?

## Conceito-núcleo
Pipeline: price → return → variance energy → signed response → densities → regime → alocação defasada → hedge; Ashby/requisite variety no switch de regime.

## Aplicação em mercado / trading
Operar sistema regime-aware: quando mudar pesos, como hedgear a perna frágil, métricas de robustez.

## Entregável / lab
Backtest completo do sistema Janus com relatório (Sharpe, drawdown, turnover, estabilidade de regime).

## Fonte (mapeamento)
janus-anti-fragility-strategy | IG Janus part 1 backtest + part 2 requisite variety

## Guia de estudo aprofundado

> **info**
>

Este guia de estudo foi projetado para fornecer uma compreensão exaustiva, rigorosa e prática da estratégia econofísica determinística Janus. O documento cobre desde o embasamento físico-matemático de bigravidade e massas financeiras negativas até a implementação do pipeline completo de dados de mercado, cálculo de densidades vinculadas, transição de regime e execução de alocação causal defasada.

---

### Visão Geral e Arquitetura do Pipeline

A estratégia Janus é um operador econofísico determinístico estruturado em torno de um operador de densidade de resposta à variância com sinal. A premissa central é tratar pares de ativos como campos acoplados de resposta positiva e negativa à desordem de mercado (variância realizada).

O pipeline de execução segue uma cadeia de prova estritamente adaptada à filtração informacional do mercado ($\mathcal{F}_t$), garantindo que nenhuma informação futura seja utilizada na tomada de decisão:

$$\text{Preço} \longrightarrow \text{Retorno} \longrightarrow \text{Energia de Variância} \longrightarrow \text{Resposta com Sinal} \longrightarrow \text{Densidades Restritas} \longrightarrow \text{Balanço de Densidade} \longrightarrow \text{Regime Confirmado} \longrightarrow \text{Alocação Defasada} \longrightarrow \text{Hedge Realizado}$$

#### Etapas Fundamentais do Pipeline

1. **Camada de Estado de Preço**: Coleta e transformação de preços de fechamento ($P_t$) em log-preços e retornos simples/logarítmicos.
2. **Energia de Variância**: Mensuração da desordem do sistema por meio da variância anualizada móvel dos retornos logarítmicos.
3. **Lei de Resposta à Variância com Sinal**: Estimação do parâmetro $\beta$, que classifica se o ativo sofre com arrasto de variância ($\beta > 0$) ou exibe resposta antifragil/massa financeira negativa ($\beta < 0$).
4. **Camada de Escala e Curvatura**: Normalização dos fatores de escala $R_i(t)$ e derivação causal de velocidade $\dot{R}_i(t)$ e aceleração $\ddot{R}_i(t)$ usando filtros de Savitzky-Golay com janelas voltadas para o passado.
5. **Densidades Restritas de Resposta**: Construção de campos de densidade para a perna de crescimento ($\rho_+$) e perna de pressão ($\rho_-$), combinando o sinal de resposta e o estresse causal de variância.
6. **Balanço de Densidade e Transição**: Avaliação do operador de diferença de densidade $\Delta \rho(t) = \rho_+(t) - \rho_-(t)$ para determinar a dominância relacional.
7. **Controle Causal e Alocação Defasada**: Chaveamento da alocação com defasagem de um período ($w_-(t+1) = 1$ quando $\Delta \rho(t) < 0$), respeitando rigorosamente o princípio de causalidade temporal.
8. **Auditoria de Conservação de Opções**: Verificação independente da paridade put-call e precificação do kernel de Black-Scholes adaptado à resposta com sinal.

---

### Conceitos-Chave e Fundamentação Teórica

#### Massa Financeira Negativa e Antifragilidade
No modelo Janus, a "massa financeira negativa" é a tradução operacional para um estado onde a resposta à variância realizada é invertida. Em ativos tradicionais de crescimento (massa positiva, fragilidade), a variância atua como um arrasto (drag) que reduz os retornos em excesso. Em ativos portadores de pressão/refúgio (massa negativa), surtos de variância e desordem geram um impulso positivo no retorno.

#### Analogia com Bigravidade e Relatividade Bimétrica
O modelo inspira-se na teoria cosmológica bimétrica de Jean-Pierre Petit e Gilles d'Agostini, na qual o Universo é descrito por duas métricas conjugadas ($g_+$ e $g_-$) associadas a partículas de massa positiva e negativa:
- As equações de campo de Einstein acopladas são dadas por:
  $$S_+(g_+) = \chi (T_+ - T_-)$$
  $$S_-(g_-) = \chi (T_- - T_+)$$
  com $S_+(g_+) = -S_-(g_-)$.
- Na aproximação newtoniana, isso resulta em duas equações de Poisson acopladas:
  $$\nabla^2 \Psi_+ = -4\pi G (\rho_+ - \rho_-)$$
  $$\nabla^2 \Psi_- = -4\pi G (\rho_- - \rho_+)$$
  onde os potenciais gravitacionais satisfazem $\Psi_- = -\Psi_+$.
- **Regra de Interação**: Partículas de massa positiva se atraem mútua e newtonianamente; partículas de massa negativa se atraem mutuamente; partículas de massas com sinais opostos se repelem através de uma "lei anti-newtoniana". Na finança, a perna de crescimento e a perna de pressão atuam como esses dois fluidos acoplados.

#### Identidade de Ticker vs. Estado de Resposta
Uma descoberta central observada no ativo AAPL durante e após a crise da COVID-19 é que o rótulo de um ticker não define seu estado de resposta permanentemente. A resposta à variância $\beta(t)$ é uma variável de regime dinâmica. Antes da COVID, a AAPL apresentava $\beta$ predominantemente positivo (comportamento de crescimento frágil). Durante a reprecificação pós-COVID, a AAPL transitou temporariamente para um estado de resposta negativa ($\beta < 0$). Isso demonstra operacionalmente que:

$$\text{Identidade do Ticker} \neq \text{Estado de Resposta}$$

---

### Formulação Matemática do Operador

#### 1. Lei Primária de Resposta à Variância
A relação entre retorno em excesso anualizado ($R_{excess,t}$) e a variância realizada ($\sigma^2_t$) é expressa por:

$$R_{excess,t} = \alpha - \beta \sigma^2_t + \epsilon_t$$

Onde:
- $R_{excess,t} = \log\left(\frac{P_t}{P_{t-252}}\right) - r_f$
- $\sigma^2_t = E_t = 252 \cdot \text{Var}(\Delta \log P_{t-251}, \dots, \Delta \log P_t)$ (Energia de Variância)
- $\beta > 0 \implies \frac{\partial R_{excess}}{\partial \sigma^2} < 0$ (Estado frágil / arrasto de variância)
- $\beta < 0 \implies \frac{\partial R_{excess}}{\partial \sigma^2} > 0$ (Estado antifrágil / massa negativa)

#### 2. Estresse Causal de Variância
Para evitar a contaminação por dados futuros, o nível de estresse de variância $S_i(t)$ para o ativo $i$ é calculado em relação a uma linha de base mediana defasada:

$$v_i(t) = 252 \cdot \text{Var}(\Delta \log P_i)_{t-62:t}$$
$$b_i(t) = \text{Median}_{252}(v_i)(t-1)$$
$$S_i(t) = \max\left( \frac{v_i(t)}{b_i(t)} - 1, 0 \right)$$

#### 3. Campos de Densidade Restrita
Definem-se os componentes operacionais de resposta positiva e negativa:
$$M_+(t) = \max(\beta_+(t), 0)$$
$$M_-(t) = \max(-\beta_-(t), 0)$$

A **densidade da perna de crescimento** ($\rho_+$) é atenuada pelo seu próprio estresse:
$$\rho_+(t) = \frac{M_+(t)}{1 + S_+(t)}$$

A **densidade da perna de pressão** ($\rho_-$) requer a presença simultânea de estado de massa negativa no ativo de pressão e estresse na perna de crescimento:
$$\rho_-(t) = \frac{M_-(t) S_+(t)}{1 + S_-(t)}$$

*Proposição de Exclusão Simultânea*: Se a perna de pressão temporariamente perder sua característica de massa negativa ($\beta_-(t) > 0$), então $M_-(t) = 0$, resultando em $\rho_-(t) = 0$, impedindo qualquer entrada indevida no regime de hedge.

#### 4. Balanço de Densidade e Janela de Confirmação
O operador de balanço de densidade é dado por:
$$\Delta \rho(t) = B_\rho(t) = \rho_+(t) - \rho_-(t)$$

A janela de tempo adaptativa para confirmação da transição ($\tau(t)$) ajusta o atraso exigido com base na magnitude do desequilíbrio:
$$\tau(t) = \text{round}\left( \text{clip}\left( \frac{1}{\sqrt{|\Delta \rho(t)|}}, \tau_{min}, \tau_{max} \right) \right)$$

#### 5. Condição de Alocação Causal e Saída
- **Ativação de Hedge**: Se $\Delta \rho(t) < 0$, ativa-se a perna de pressão no período seguinte:
  $$w_-(t+1) = 1$$
- **Saída para Crescimento (Return-to-Growth Exit)**: A alocação retorna à perna de crescimento quando o campo de curvatura/aceleração $a_+(t)$ torna-se positivo:
  $$a_+(t) = \frac{\ddot{R}_+(t)}{R_+(t)} + \frac{1}{2}(\rho_+(t) - \rho_-(t)) > 0$$

#### 6. Camada de Opções e Kernel de Black-Scholes Modificado
A equidade composta satisfaz a identidade de replicação $S = B + C - P$, com $B = K e^{-rT}$. A paridade put-call possui o resíduo de conservação:
$$\epsilon_{parity} = (C - P) - (S - K e^{-rT})$$
Um estado é conservado se $|\epsilon_{parity}| \le \tau_{market}$.

No Movimento Browniano Geométrico com resposta com sinal:
$$d \log S_t = \left( \mu - \beta \sigma^2 - \frac{1}{2}\sigma^2 \right) dt + \sigma dW_t$$

O Kernel de Black-Scholes ajustado utiliza o frete/carrego efetivo $\kappa_\beta = r - \beta \sigma^2$ na propagação de *moneyness* ($d_1^\beta$), enquanto a taxa livre de risco $r$ é mantida estritamente no desconto do título de renda fixa ($K e^{-rT}$):
$$d_1^\beta = \frac{\log(S/K) + (\kappa_\beta + \frac{1}{2}\sigma^2)T}{\sigma \sqrt{T}}$$
$$d_2^\beta = d_1^\beta - \sigma \sqrt{T}$$
$$C_\beta = S \Phi(d_1^\beta) - K e^{-rT} \Phi(d_2^\beta)$$
$$P_\beta = K e^{-rT} \Phi(-d_2^\beta) - S \Phi(-d_1^\beta)$$

---

### Intuição de Mercado e Trading

| Elemento | Papel no Mercado / Intuição de Trading |
| :--- | :--- |
| **Perna de Crescimento ($R_+$)** | Carreador principal de retorno (ex: SPY, QQQ). Em ambientes calmos, gera valor, mas sofre degradação e drag drástico quando a variância salta ($\beta > 0$). |
| **Perna de Pressão ($R_-$)** | Carreador de refúgio/proteção (ex: GLD). Funciona como uma mola comprimida: sob estresse de mercado, absorve a desordem e expande o retorno ($\beta < 0$). |
| **Proxy de Inércia ($I_t = \frac{\sigma^2}{\beta}$)** | Mede a escala de resistência do ativo em relação ao arrasto de variância. Quando $\beta < 0$, a inércia fica negativa, sinalizando impulso a favor do choque. |
| **Ativação Defasada ($w_-(t+1)$)** | Garante a "variedade necessária" (Lei de Ashby) para controlar o sistema sem cair na armadilha de *look-ahead bias*. O sinal é fechado em $t$ com a informação $\mathcal{F}_t$, e a ordem só executa na abertura/fechamento de $t+1$. |

---

### Exemplo Numérico Resolvido Passo a Passo

Considere a avaliação de um par **SPY (Perna $+$)** e **GLD (Perna $-$)** no fechamento do dia $t$.

#### Dados Observados no Fechamento do Dia $t$
- **SPY ($R_+$)**:
  - $\beta_+(t) = 1,152$
  - Variância de 62 dias $v_+(t) = 0,04$
  - Linha de base mediana $b_+(t) = 0,02$
- **GLD ($R_-$)**:
  - $\beta_-(t) = -8,524$
  - Variância de 62 dias $v_-(t) = 0,03$
  - Linha de base mediana $b_-(t) = 0,03$

---

#### Passo 1 Calcular o Estresse Causal de Variância ($S_+$ e $S_-$)
Para o SPY ($R_+$):
$$S_+(t) = \max\left( \frac{0,04}{0,02} - 1, 0 \right) = \max(2,0 - 1, 0) = 1,0$$

Para o GLD ($R_-$):
$$S_-(t) = \max\left( \frac{0,03}{0,03} - 1, 0 \right) = \max(1,0 - 1, 0) = 0,0$$

---

#### Passo 2 Calcular as Respostas Operacionais ($M_+$ e $M_-$)
$$M_+(t) = \max(1,152, 0) = 1,152$$
$$M_-(t) = \max(-(-8,524), 0) = 8,524$$

---

#### Passo 3 Calcular as Densidades Restritas ($\rho_+$ e $\rho_-$)
Densidade de Crescimento ($\rho_+$):
$$\rho_+(t) = \frac{M_+(t)}{1 + S_+(t)} = \frac{1,152}{1 + 1,0} = \frac{1,152}{2,0} = 0,576$$

Densidade de Pressão ($\rho_-$):
$$\rho_-(t) = \frac{M_-(t) \cdot S_+(t)}{1 + S_-(t)} = \frac{8,524 \cdot 1,0}{1 + 0,0} = 8,524$$

---

#### Passo 4 Calcular o Balanço de Densidade ($\Delta \rho$)
$$\Delta \rho(t) = \rho_+(t) - \rho_-(t) = 0,576 - 8,524 = -7,948$$

---

#### Passo 5 Determinar o Regime e a Janela de Confirmação ($\tau$)
Como $\Delta \rho(t) = -7,948 < 0$, a densidade de pressão domina o sistema.
Assumindo limites de janela $\tau_{min} = 1$ e $\tau_{max} = 5$:

$$\tau(t) = \text{round}\left( \text{clip}\left( \frac{1}{\sqrt{|-7,948|}}, 1, 5 \right) \right) = \text{round}\left( \text{clip}\left( \frac{1}{2,819}, 1, 5 \right) \right) = \text{round}(0,354) \longrightarrow \text{limitado a } 1 \text{ período}$$

---

#### Passo 6 Decisão Executiva Causal de Alocação
Devido ao sinal confirmado de dominância da densidade de pressão em $t$ ($\Delta \rho(t) < 0$), o algoritmo emite a instrução de chaveamento com defasagem de 1 período:

$$w_-(t+1) = 1 \quad \text{e} \quad w_+(t+1) = 0$$

Em $t+1$, 100% do capital da estratégia estará alocado em **GLD** para capturar o hedge de variância.

---

### Armadilhas Comuns na Implementação

1. **Uso de Variância Centrada ou Não-Causal**: Calcular $v_i(t)$ usando janelas centralizadas que incluem dados de $t+1, \dots, t+k$.
   - *Correção*: Utilizar exclusivamente janelas com corte à esquerda ($t-62 : t$) para variância e medians defasadas em $t-1$.
2. **Atribuição Estática de Rótulo ao Ticker**: Classificar permanentemente um ativo como "proteção" sem verificar dinamicamente se $\beta_-(t) < 0$. Se o GLD passar a ter $\beta > 0$ em determinado regime, o modelo falha se for forçado a operar estaticamente.
   - *Correção*: Implementar a Proposição de Exclusão Simultânea ($M_-(t) = 0$ se $\beta_-(t) > 0$).
3. **Erros de Desconto no Kernel de Black-Scholes Modificado**: Subduzir a taxa livre de risco $r$ pelo termo $\kappa_\beta$ no fator de desconto temporal do título de renda fixa $K e^{-rT}$.
   - *Correção*: O termo $\kappa_\beta = r - \beta \sigma^2$ entra **apenas** no cálculo de $d_1^\beta$ e $d_2^\beta$ para propagação da probabilidade de *moneyness*, preservando $r$ puro no valor presente do *strike*.
4. **Execução Simultânea no Mesmo Fechamento (Look-Ahead Bias)**: Aplicar a alocação $w(t)$ aos retornos do período de $t-1$ para $t$.
   - *Correção*: O sinal gerado em $t$ com informação $\mathcal{F}_t$ afeta estritamente o retorno do período $t \to t+1$.

---

### Laboratório Prático Sugerido em Python

Abaixo descreve-se a estrutura lógica passo a passo para implementar o pipeline determinístico Janus em Python sem o uso de bibliotecas de aprendizado de máquina.

#### Passo 1 Construção da Janela Móvel Causal e Estimação de $\beta$
- Escreva uma função para calcular a variância realizada anualizada $\sigma^2_t$ em uma janela deslizante de 252 dias.
- Regrida os retornos anuais em excesso $R_{excess,t}$ contra $\sigma^2_t$ para extrair a inclinação $b$, obtendo $\beta = -b$ e $\alpha = a$.

#### Passo 2 Cálculo dos Indicadores de Estresse de Variância
- Calcule a variância de 62 dias $v_i(t)$ para cada ativo.
- Calcule a mediana móvel de 252 dias defasada $b_i(t) = \text{Median}_{252}(v_i)_{t-1}$.
- Derive a métrica $S_i(t) = \max\left(\frac{v_i(t)}{b_i(t)} - 1, 0\right)$.

#### Passo 3 Implementação do Operador de Densidade e Balanço
- Para a perna de crescimento (SPY), calcule $M_+(t) = \max(\beta_+(t), 0)$ e $\rho_+(t) = \frac{M_+(t)}{1 + S_+(t)}$.
- Para a perna de pressão (GLD), calcule $M_-(t) = \max(-\beta_-(t), 0)$ e $\rho_-(t) = \frac{M_-(t) S_+(t)}{1 + S_-(t)}$.
- Derive a série de balanço de densidade $\Delta \rho(t) = \rho_+(t) - \rho_-(t)$.

#### Passo 4 Geração do Sinal Defasado e Backtest Causal
- Crie a coluna de posição defasada `posição_minus = (delta_rho < 0).shift(1).fillna(0)`.
- Crie a coluna `posição_plus = 1 - posição_minus`.
- Calcule o retorno diário da estratégia:
  $$\text{retorno\_estrategia}_t = w_+(t) \cdot \text{retorno}_+(t) + w_-(t) \cdot \text{retorno}_-(t)$$
- Audite os resultados verificando os retornos acumulados e métricas de risco (Sharpe, Calmar, Drawdown Máximo).

---

### Glossário de Termos Importantes

| Termo | Definição Operacional e Contexto no Modelo |
| :--- | :--- |
| **Massa Financeira Negativa** | Estado de um ativo em que o coeficiente de resposta à variância $\beta$ é negativo ($\beta < 0$), significando que o aumento da desordem do mercado amplia os retornos do ativo. |
| **Energia de Variância ($E_t$)** | Métrica de desordem do sistema, calculada como a variância anualizada dos retornos logarítmicos em uma janela histórica de 252 dias. |
| **Arrasto de Variância (Variance Drag)** | Fenômeno verificado em ativos com $\beta > 0$, onde surtos de volatilidade/variância penalizam de forma sistemática o retorno em excesso do ativo. |
| **Densidade Restrita ($\rho$)** | Métrica de intensidade de resposta que combina o sinal de resposta ao risco, a magnitude do coeficiente e o nível de estresse causal de variância regularizado. |
| **Superfície de Transição** | A condição em que o balanço de densidades cruza o nível zero ($\Delta \rho(t) = 0$), marcando a fronteira entre o regime de crescimento e o regime de hedge. |
| **Fator de Escala ($R_i(t)$)** | Preço normalizado do ativo em relação ao seu valor inicial $P_i(t)/P_i(0)$, permitindo a análise de aceleração e curvatura do crescimento. |
| **Variedade Necessária** | Princípio da cibernética (Lei de Ashby) aplicado à finança: o mecanismo de hedge do controlador deve possuir variedade de estados internos para compensar as perturbações do mercado. |
| **Resíduo de Conservação da Opção** | Desvio observado da paridade put-call em relação à tolerância da cotação de mercado ($|\epsilon_{parity}| > \tau_{market}$). |

---

### Questões de Prática e Autoavaliação

#### Nível Básico (Respostas Curtas)

1. **Pergunta**: O que significa um valor positivo de $\beta$ na lei primária de resposta $R_{excess,t} = \alpha - \beta \sigma^2_t + \epsilon_t$?
2. **Pergunta**: Como a energia de variância $E_t$ é calculada no pipeline Janus?
3. **Pergunta**: O que acontece com a densidade da perna de pressão ($\rho_-$) se a perna de refúgio temporariamente apresentar $\beta_- > 0$?
4. **Pergunta**: Por que a alocação do portfólio $w_-(t+1)$ deve ser defasada em um período em relação ao balanço de densidade calculado em $t$?

---

#### Nível Intermediário (Aplicação e Análise)

5. **Pergunta**: Considere um ativo com variância realizada de 62 dias de $0,06$ e uma linha de base mediana defasada de $0,03$. Qual é o nível de estresse de variância $S(t)$? Se a resposta positiva $M_+$ for $1,2$, qual será a densidade de crescimento $\rho_+$?
6. **Pergunta**: Explique o significado da transição comportamental observada na AAPL no período pós-COVID em relação ao conceito "Identidade do Ticker $\neq$ Estado de Resposta".
7. **Pergunta**: No modelo de opções com resposta com sinal, como o parâmetro $\beta$ altera a deriva efetiva / carrego $\kappa_\beta$ e o parâmetro $d_1^\beta$ de Black-Scholes?

---

#### Nível Avançado e Ensaios Dissertativos (Aprofundamento)

8. **Prompt de Ensaio 1**: Disserte sobre a correspondência matemática e conceitual entre os modelos cosmológicos de bigravidade (equações de Poisson acopladas para massas positivas e negativas de Petit e d'Agostini) e o operador de densidades acopladas Janus ($\rho_+$ e $\rho_-$). Como a repulsão entre massas opostas se reflete na mecânica de migração de capital durante regimes de estresse?
9. **Prompt de Ensaio 2**: Avalie criticamente a importância do princípio da filtragem adaptada à informação $\mathcal{F}_t$ e da variabilidade de tempo de confirmação $\tau(t)$ na eliminação de vãos de otimização (overfitting) e viés de antecipação (look-ahead bias) em estratégias de trading quantitativo determinístico.

---

#### Gabarito e Respostas Detalhadas

##### 1. Resposta (Nível Básico)
Um $\beta > 0$ indica que o ativo sofre de arrasto de variância (fragilidade). O aumento da variância realizada $\sigma^2_t$ reduz de forma determinística o retorno anual em excesso do ativo ($\frac{\partial R_{excess}}{\partial \sigma^2} < 0$).

##### 2. Resposta (Nível Básico)
A energia de variância $E_t$ é a variância anualizada dos retornos logarítmicos diários do ativo, calculada em uma janela móvel retroativa de 252 dias: $E_t = \sigma^2_t = 252 \cdot \text{Var}(\Delta \log P_{t-251}, \dots, \Delta \log P_t)$.

##### 3. Resposta (Nível Básico)
Se $\beta_- > 0$, o componente de massa negativa $M_-(t) = \max(-\beta_-(t), 0)$ torna-se zero. Consequentemente, a densidade de pressão $\rho_-(t)$ desaba para exatamente $0$, impedindo que o algoritmo aloque capital na perna de pressão quando ela não estiver atuando como um refúgio de massa negativa.

##### 4. Resposta (Nível Básico)
A defasagem de um período é necessária para garantir a causalidade temporal e aderência à filtração $\mathcal{F}_t$. O sinal do regime $G_t$ é gerado com base nos preços de fechamento em $t$. Portanto, a primeira oportunidade tradável afetada por esse sinal ocorre no período seguinte ($t \to t+1$).

##### 5. Resposta (Nível Intermediário)
- **Cálculo do Estresse $S(t)$**:
  $$S(t) = \max\left( \frac{0,06}{0,03} - 1, 0 \right) = \max(2 - 1, 0) = 1,0$$
- **Cálculo da Densidade de Crescimento $\rho_+$**:
  $$\rho_+ = \frac{M_+}{1 + S_+} = \frac{1,2}{1 + 1,0} = \frac{1,2}{2,0} = 0,6$$

##### 6. Resposta (Nível Intermediário)
Historicamente e conceitualmente, a AAPL é tratada como uma ação de tecnologia/crescimento (massa positiva, $\beta > 0$). No entanto, durante o período de reprecificação pós-shock da COVID-19, o coeficiente móvel $\beta(t)$ da AAPL tornou-se negativo em $73,5\%$ dos dias analisados. Isso provou empiricamente que o comportamento de resposta à desordem não é um rótulo fixo ancorado no nome da empresa (ticker), mas sim um estado dinâmico de regime que deve ser medido continuamente pelo operador.

##### 7. Resposta (Nível Intermediário)
O parâmetro $\beta$ introduz um termo de correção de arrasto na taxa de carrego efetiva $\kappa_\beta = r - \beta \sigma^2$. 
- Se $\beta > 0$ (frágil), $\kappa_\beta < r$, reduzindo o carrego e o valor do parâmetro $d_1^\beta$, refletindo a atenuante do arrasto de volatilidade no valor da opção de compra.
- Se $\beta < 0$ (antifrágil), $\kappa_\beta > r$, elevando o carrego e aumentando $d_1^\beta$. Importante ressaltar que a taxa livre de risco pura $r$ continua sendo usada no fator de desconto do título $K e^{-rT}$.

##### 8. Resposta (Nível Avançado - Ensaio Guia)
O candidato deve articular que, na cosmológica de Petit e d'Agostini, duas métricas $g_+$ e $g_-$ geram potenciais tais que $\Psi_- = -\Psi_+$, induzindo repulsão entre massas de sinais opostos. No pipeline Janus, as densidades $\rho_+$ e $\rho_-$ desempenham o papel dos fluidos acoplados. A perna de crescimento $\rho_+$ atrai capital em estados de baixa energia de variância, mas repulsa a exposição quando $S_+$ cresce. O termo $S_+$ atua na densidade de pressão $\rho_- = \frac{M_- S_+}{1 + S_-}$ exatamente como uma força de acoplamento cruzado: o estresse na massa positiva ativa a densidade da massa negativa. Essa assimetria força a rotação do capital da perna frágil para a perna antifrágil, espelhando a dinâmica repulsiva entre fluidos gravitacionais opostos.

##### 9. Resposta (Nível Avançado - Ensaio Guia)
O candidato deve discutir que a construção determinística de estratégias quantitativas frequentemente sofre de overfitting devido ao ajuste retrospectivo de hiperparâmetros ou ao uso inadvertido de dados do futuro (*look-ahead bias*). O modelo Janus combate essas patologias através de três mecanismos matemáticos rigorosos:
1. **Adaptação estrita à filtração $\mathcal{F}_t$**: Todos os componentes (mediana defasada em $t-1$, filtro de Savitzky-Golay com suporte estritamente à esquerda e execução defasada $w(t+1)$) garantem que nenhum dado de $t+1$ seja usado na decisão em $t$.
2. **Ausência de parâmetros treinados por Machine Learning**: As regras do operador derivam diretamente de condições de contorno físico-matemáticas (Proposição 1), tornando o modelo imune à degradação por sobreajuste de sinal.
3. **Janela adaptativa $\tau(t)$**: A modulação do tempo de confirmação impede o excesso de negociação (*whipsaws*) em zonas de baixo desequilíbrio e acelera o chaveamento quando o balanço de densidade é esmagador, mantendo a estabilidade operacional através do princípio da Variedade Necessária.