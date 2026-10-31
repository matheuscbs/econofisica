<!-- imported from vault study notes; curated for open course -->
# M01.A03 — Delta neutro: transformar opinião direcional em risco controlado

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M01
> **Aula:** M01.A03

↑ M01 · Resumo · Completo

**Módulo:** M01
**Pergunta do módulo:** Como precificar e fazer hedge de opções vanila sem “adivinhar” o drift?

## Conceito-núcleo
Delta (Δ) como sensibilidade ao spot; carteira Δ≈0 remove a primeira ordem da direção.

## Aplicação em mercado / trading
Montar hedges de opções/ações para isolar vol, skew ou carry sem “apostar o índice”.

## Entregável / lab
Simular trajetórias e rebalancear Δ=0; medir P&L residual vs frequência de hedge.

## Fonte (mapeamento)
quantitative-trading-free-lesson/03 neutral delta | IG Reel neutral delta Δ=0

## Guia de estudo aprofundado

> **info**
>

Este guia de estudos fornece uma síntese técnica e conceitual sobre a estratégia de neutralidade de delta no mercado de opções, detalhando os princípios de gestão de risco, formulação matemática do modelo Black-Scholes, rebalanceamento dinâmico adaptativo, custos de transação e implementação prática.

---

### Conceitos Fundamentais e Intuição de Mercado

#### A Natureza da Venda de Opções
A venda de uma opção representa a arrecadação imediata de um prêmio em troca da aceitação de um risco futuro potencial. Esse prêmio só é retido integralmente se o cenário que dispara o pagamento (*payoff*) não ocorrer ou se for neutralizado ao longo do tempo. O vendedor recebe caixa líquido no presente, mas assume uma exposição que cresce à medida que o mercado se movimenta. Sem uma intervenção ativa, a posição tende a derrapar e espiralar por construção.

#### A Deriva do Delta e a Gestão Dinâmica
O ativo subjacente varia continuamente. Conforme o preço à vista (*spot*) se altera, o delta da opção também se modifica. Se nenhuma calibragem for realizada, a exposição direcional deriva autonomamente:
* Se o delta total das opções for $\Delta_{\text{options}} = -0{,}25$, a posição exige $+0{,}25$ unidades do ativo subjacente para atingir a neutralidade.
* Conforme o *spot* se move, o delta da opção pode passar para $-0{,}18$ ou $-0{,}35$.
* O rebalanceamento dinâmico exige ajustar a quantidade do subjacente (comprando ou vendendo) para realinhar o hedge.

O objetivo do hedge em delta neutro não é capturar a alta ou a baixa do mercado, mas sim manter a exposição estritamente sob controle enquanto o tempo passa e o mercado oscila. Defender o prêmio exige controle do risco durante todo o percurso.

#### Trader Amador vs. Gestor Profissional
Vender uma opção sem manter a neutralidade de delta equivale a assumir uma posição direcional velada. Essa direção fica à mercê de variáveis instáveis e dinâmicas: volatilidade implícita, liquidez, fluxo de ordens e regimes de mercado. Nenhuma dessas variáveis mantém a exposição estável se não houver cobertura.
* **Operador não protegido:** Não possui uma estratégia; possui exposição à aleatoriedade.
* **Operador profissional:** Mantém a posição sob controle por meio de alinhamentos contínuos. A meta central não é a performance direcional, mas a capacidade de sustentação da posição.

Quando o equilíbrio é preservado, o prêmio arrecadado comporta-se como uma receita de seguro sem aposta direcional. Se o equilíbrio se rompe, a venda estruturada se degrada em uma tomada de risco descontrolada.

---

### Formulário Matemático

#### Condição de Neutralidade de Delta
A neutralidade busca manter o delta total da carteira próximo de zero:

$$\Delta_{\text{total}} = \Delta_{\text{options}} + \text{hedge\_units} \approx 0$$

O alvo da posição de hedge no ativo subjacente é definido por:

$$\text{Hedge target} = -\Delta_{\text{options}}$$

#### Modelo Black-Scholes e Gregas
Para uma opção com preço à vista $S$, strike $K$, tempo até o vencimento $T$, volatilidade $\sigma$, taxa livre de risco $r$ e taxa de dividendos $q$:

Os termos $d_1$ e $d_2$ são definidos por:
$$d_1 = \frac{\ln(S / K) + (r - q + \sigma^2 / 2) T}{\sigma \sqrt{T}}$$
$$d_2 = d_1 - \sigma \sqrt{T}$$

Fatores de desconto:
$$df_r = e^{-r T}, \quad df_q = e^{-q T}$$

##### Preços e Deltas
* **Call:**
  $$\text{Preço}_{\text{call}} = df_q \cdot S \cdot N(d_1) - df_r \cdot K \cdot N(d_2)$$
  $$\Delta_{\text{call}} = df_q \cdot N(d_1)$$

* **Put:**
  $$\text{Preço}_{\text{put}} = df_r \cdot K \cdot N(-d_2) - df_q \cdot S \cdot N(-d_1)$$
  $$\Delta_{\text{put}} = -df_q \cdot N(-d_1)$$

##### Gregas Complementares
* **Gamma ($\Gamma$):**
  $$\Gamma = \frac{df_q \cdot n(d_1)}{S \cdot \sigma \cdot \sqrt{T}}$$

* **Vega:**
  $$\text{Vega} = S \cdot df_q \cdot n(d_1) \cdot \sqrt{T}$$

* **Theta ($\Theta$):**
  $$\Theta_{\text{call}} = -\frac{S \cdot df_q \cdot n(d_1) \cdot \sigma}{2 \sqrt{T}} - r \cdot K \cdot df_r \cdot N(d_2) + q \cdot S \cdot df_q \cdot N(d_1)$$
  $$\Theta_{\text{put}} = -\frac{S \cdot df_q \cdot n(d_1) \cdot \sigma}{2 \sqrt{T}} + r \cdot K \cdot df_r \cdot N(-d_2) - q \cdot S \cdot df_q \cdot N(-d_1)$$

*Nota:* $N(\cdot)$ é a função de distribuição acumulada da normal padrão e $n(\cdot)$ é a densidade de probabilidade da normal padrão. No vencimento ($T \le 0$), os deltas assumem valores limites ($1{,}0$, $0{,}0$, $0{,}5$, $-1{,}0$, $-0{,}5$).

#### Gatilho de Rebalanceamento Adaptativo
Para evitar over-hedging motivado por ruído intradiário, o rebalanceamento só é acionado quando:

$$|\Delta_{\text{total}}| > \text{threshold}$$

O limiar adaptativo ($\text{adj}$) varia em função da magnitude do Gamma ($|\Gamma|$), do preço spot ($S$) e da variância dos retornos recentes ($\text{ret\_var}$):

$$\text{adj} = \frac{\text{base}}{1{,}0 + \text{gamma\_sensitivity} \cdot |\Gamma| \cdot S + \text{var\_sensitivity} \cdot \sqrt{\max(\text{ret\_var}, 10^{-12})}}$$

$$\text{threshold} = \min\left(\text{max\_threshold}, \max\left(\text{min\_threshold}, \text{adj}\right)\right)$$

#### Modelo de Custos de Transação
A quantidade negociada para atingir o alvo é limitada pelo tamanho máximo da ordem ($\text{max\_trade\_size}$):

$$\text{trade\_units} = \text{clip}\left(\text{target\_delta\_units} - \text{hedge\_units}, -\text{max\_trade\_size}, \text{max\_trade\_size}\right)$$

 O notional da operação e os custos associados são calculados por:

$$\text{notional} = |\text{trade\_units}| \cdot S$$
$$\text{fee\_cost} = |\text{trade\_units}| \cdot \text{fee\_per\_share}$$
$$\text{slip\_cost} = \text{notional} \cdot \left(\text{slippage\_bps} \cdot 10^{-4}\right)$$
$$\text{spread\_cost} = \text{notional} \cdot \left(\text{spread\_bps} \cdot 10^{-4}\right)$$
$$\text{trade\_cost} = \text{fee\_cost} + \text{slip\_cost} + \text{spread\_cost}$$

---

### Exemplo Numérico Resolvido Passo a Passo

#### Cenário de Mercado
Um gestor vendeu uma estrutura *Short Straddle* (venda de 1 Call e venda de 1 Put no mesmo strike $K=100$) com quantidade $\text{qty} = -1{,}0$.
* Preço spot inicial ($S_0$): $\$100{,}00$
* Taxas operacionais do modelo:
  * $\text{fee\_per\_share} = \$0{,}01$
  * $\text{slippage\_bps} = 5$ ($5 \times 10^{-4}$)
  * $\text{spread\_bps} = 10$ ($10 \times 10^{-4}$)
* Configuração do controlador de hedge:
  * $\text{delta\_threshold\_base} = 0{,}10$
  * $\text{gamma\_sensitivity} = 0{,}0$ (desativado para simplificação)
  * $\text{var\_sensitivity} = 0{,}0$ (desativado para simplificação)
  * $\text{min\_threshold} = 0{,}05$, $\text{max\_threshold} = 0{,}20$
  * $\text{max\_trade\_size} = 100{,}0$

---

#### Passo 1 Ajuste Inicial no Momento $T_0$
1. **Calcular o Delta das Opções:**
   No strike at-the-money ($S_0 = 100, K = 100$):
   * $\Delta_{\text{call}} = +0{,}50$
   * $\Delta_{\text{put}} = -0{,}50$
   * Delta total das opções vendido:
     $$\Delta_{\text{options}} = (-1{,}0 \cdot 0{,}50) + (-1{,}0 \cdot -0{,}50) = -0{,}50 + 0{,}50 = 0{,}00$$

2. **Determinar o Hedge Inicial:**
   $$\text{Hedge target} = -\Delta_{\text{options}} = 0{,}00$$
   Nenhuma unidade do subjacente precisa ser comprada ou soldada inicialmente ($\text{hedge\_units} = 0{,}00$).

---

#### Passo 2 Movimentação do Spot para $S_1 = \$105{,}00$
Com a elevação do ativo subjacente para $\$105{,}00$:
1. Os deltas individuais se alteram devido ao Gamma:
   * Novo $\Delta_{\text{call}} = +0{,}65$
   * Novo $\Delta_{\text{put}} = -0{,}35$

2. **Recalcular o Delta das Opções:**
   $$\Delta_{\text{options}} = (-1{,}0 \cdot 0{,}65) + (-1{,}0 \cdot -0{,}35) = -0{,}65 + 0{,}35 = -0{,}30$$

3. **Verificar o Delta Total Atual:**
   Como a carteira de hedge atual tem $\text{hedge\_units} = 0{,}0$:
   $$\Delta_{\text{total}} = \Delta_{\text{options}} + \text{hedge\_units} = -0{,}30 + 0{,}0 = -0{,}30$$

---

#### Passo 3 Avaliação do Gatilho de Rebalanceamento
1. **Calcular o Limiar Adaptativo:**
   Com sensibilidades nulas:
   $$\text{adj} = \frac{0{,}10}{1{,}0 + 0 + 0} = 0{,}10$$
   $$\text{threshold} = \min(0{,}20, \max(0{,}05, 0{,}10)) = 0{,}10$$

2. **Testar a Condição de Rebalanceamento:**
   $$|\Delta_{\text{total}}| = |-0{,}30| = 0{,}30$$
   Como $0{,}30 > 0{,}10$, o gatilho de rebalanceamento é **ativado**.

---

#### Passo 4 Execução do Rebalanceamento e Cálculo de Custos
1. **Calcular a Quantidade Negociada:**
   $$\text{target\_delta\_units} = -\Delta_{\text{options}} = -(-0{,}30) = +0{,}30$$
   $$\text{trade\_units} = \text{target\_delta\_units} - \text{hedge\_units} = 0{,}30 - 0{,}0 = +0{,}30 \text{ unidades}$$

2. **Cálculo Financeiro dos Custos:**
   * **Notional:**
     $$\text{notional} = 0{,}30 \cdot 105{,}00 = \$31{,}50$$
   * **Taxas de Corretagem ($\text{fee\_cost}$):**
     $$\text{fee\_cost} = 0{,}30 \cdot 0{,}01 = \$0{,}003$$
   * **Custo de Slippage ($\text{slip\_cost}$):**
     $$\text{slip\_cost} = 31{,}50 \cdot (5 \cdot 10^{-4}) = 31{,}50 \cdot 0{,}0005 = \$0{,}01575$$
   * **Custo de Spread ($\text{spread\_cost}$):**
     $$\text{spread\_cost} = 31{,}50 \cdot (10 \cdot 10^{-4}) = 31{,}50 \cdot 0{,}001 = \$0{,}03150$$
   * **Custo Total do Rebalanceamento ($\text{trade\_cost}$):**
     $$\text{trade\_cost} = 0{,}003 + 0{,}01575 + 0{,}03150 = \$0{,}05025$$

3. **Atualização da Posição:**
   * Novos $\text{hedge\_units} = +0{,}30$
   * Nova $\Delta_{\text{total}} = -0{,}30 + 0{,}30 = 0{,}00$

---

### Armadilhas Comuns na Prática

1. **Deriva da Exposição sem Ajuste (Unhedged Drift):**
   Acreditar que a venda de opções é uma estratégia estática de coleta de renda. Sem a execução do rebalanceamento dinâmico, o deslocamento do preço à vista transforma a posição vendida em uma aposta direcional descontrolada exposta a choques de mercado.

2. **Over-Hedging por Ruído de Mercado:**
   Rebalancear a posição a cada variação mínima do *spot* sem utilizar um filtro ou limiar adaptativo. Em cenários de alta volatilidade intradia, negociações excessivas geram um atrito operacional severo que devora a margem de lucro.

3. **Subestimação dos Custos de Transação:**
   Desconsiderar o impacto conjunto da taxa fixa por ação, *slippage* e *bid-ask spread*. Como demonstrado no cálculo numérico, a soma desses três componentes no modelo de custos corrói o P&L do hedge dinâmico.

4. **Ilusão de Receita Passiva:**
   Confundir a arrecadação imediata de prêmio com lucro líquido. O prêmio representa apenas um colateral financeiro inicial sob risco constante; a margem só se consolida se a exposição for continuamente mantida sob controle.

---

### Roteiro do Laboratório Prático em Python

Este roteiro descreve passo a passo como construir a simulação de um ambiente de *Delta Hedging* dinâmico para uma estrutura vendida em Python.

#### Passo 1 Implementar o Motor de Precificação e Gregas
* Criar a função `bs_price_greeks(S, K, T, sigma, r, q, is_call)`.
* Tratar a condição limite quando $T \le 0$, retornando o payoff intrínseco e os deltas associados ($1{,}0$, $0{,}0$, $0{,}5$, etc.).
* Para $T > 0$, calcular $d_1$, $d_2$, os fatores de desconto $df_r, df_q$ e as distribuições acumuladas e de densidade normal.
* Retornar um dicionário com os valores de `price`, `delta`, `gamma`, `vega`, `theta` e `rho`.

#### Passo 2 Estruturar a Posição Multi-Legs (Short Straddle)
* Definir uma classe de especificação de opção (`OptionSpec`) que receba tipo (*call/put*), *strike*, volatilidade implícita ($\text{iv}$), quantidade e tempo até o vencimento.
* Criar a classe `ShortStraddle` que instancie uma Call e uma Put vendidas com quantidade negativa ($-\text{abs}(qty)$).
* Implementar o método `greeks(S, T_years, params)` que invoque `bs_price_greeks` para cada perna e retorne a soma ponderada pelas quantidades das respectivas pernas.

#### Passo 3 Construir o Controlador de Hedge Adaptativo
* Criar a classe `DeltaHedger` inicializada com estruturas de configuração (`HedgeConfig`) e modelo de custos (`CostModel`).
* Implementar o método `adaptive_threshold(gamma, spot, ret_var)` para ajustar o limiar de rebalanceamento inversamente ao nível de Gamma e volatilidade recente dos retornos.
* Implementar o método `trade_to_target(target_delta_units, price)`:
  * Calcular a diferença entre o alvo e o hedge atual.
  * Aplicar o limite de tamanho da ordem via `np.clip`.
  * Calcular as três frações de custo: `fee_cost`, `slip_cost` e `spread_cost`.
  * Atualizar o estado do saldo de ativos subjacentes em carteira (`self.hedge_units`) e retornar o volume negociado e o custo incorrido.

#### Passo 4 Executar o Loop de Simulação
* No tempo inicial $T_0$, obter a grega delta total do *Short Straddle*.
* Executar a ordem de alinhamento inicial acionando `trade_to_target(-total_delta, S0)`.
* Iterar sobre a série temporal de preços simulated ou real:
  1. Recalcular o tempo residual $T_t$.
  2. Extrair as gregas atualizadas da estrutura.
  3. Verificar se o delta total violou o limiar adaptativo (`adaptive_threshold`).
  4. Se violado, rebalancear a posição e contabilizar os custos de transação no P&L acumulado da estratégia.

---

### Glossário de Termos Técnicos

| Termo | Definição Técnica |
| :--- | :--- |
| **Delta ($\Delta$)** | Taxa de variação do preço da opção em relação ao preço do ativo subjacente ($\frac{\partial V}{\partial S}$). |
| **Delta Neutro** | Estado de uma carteira em que o delta total é mantido próximo de zero ($\Delta_{\text{total}} \approx 0$), anulando a exposição direcional primária. |
| **Gamma ($\Gamma$)** | Taxa de variação do Delta em relação ao preço do ativo subjacente ($\frac{\partial^2 V}{\partial S^2}$). Mede a aceleração da exposição direcional. |
| **Vega** | Sensibilidade do preço da opção em relação a variações na volatilidade implícita do ativo subjacente. |
| **Theta ($\Theta$)** | Medida da degradação temporal do valor da opção à medida que o tempo avança em direção ao vencimento. |
| **Short Straddle** | Estrutura operacional que consiste na venda simultânea de uma Call e uma Put com o mesmo preço de exercício e data de vencimento. |
| **Limiar Adaptativo** | Algoritmo de decisão que ajusta dynamicamente a tolerância de desvio do delta antes de disparar ordens de rebalanceamento, evitando custos por ruídos. |
| **Slippage** | Diferença entre o preço esperado de uma execução e o preço real pelo qual a ordem foi preenchida no mercado. |
| **Bid-Ask Spread** | A diferença entre o preço mais alto que um comprador está disposto a pagar e o preço mais baixo que um vendedor aceita. |

---

### Exercícios e Questões de Fixação

#### Nível 1 - Resposta Curta

1. Qual é a meta fundamental de uma estratégia baseada em delta neutro ao longo do tempo?
2. O que acontece com a posição de um vendedor de opções se o ativo subjacente se movimentar e nenhum rebalanceamento for executado?
3. Qual é a regra matemática utilizada para definir o alvo da quantidade de ativos subjacentes na carteira de hedge?
4. Quais são os três componentes do custo de transação calculados na execução do rebalanceamento pelo modelo quantitativo?

---

#### Nível 2 - Aplicação Analítica e Numérica

1. Um gestor possui uma estrutura vendida cujo delta total atual das opções é $\Delta_{\text{options}} = +0{,}45$. O ativo subjacente está cotado a $S = \$50{,}00$.
   * a) Quantas unidades do subjacente devem ser mantidas para atingir a neutralidade?
   * b) Se o gestor já possui $+0{,}10$ unidades do subjacente em carteira, qual será a quantidade a ser negociada ($\text{trade\_units}$)?
   * c) Sabendo que a taxa por ação é $\$0{,}02$, o slippage é $10\text{ bps}$ e o spread é $20\text{ bps}$, calcule o custo total dessa transação.

2. Considere a fórmula do limiar adaptativo ($\text{adj}$). Se o valor do Gamma da posição ($|\Gamma|$) ou a variância dos retornos do mercado ($\text{ret\_var}$) aumentarem significativamente, o que acontecerá com a largura do limiar de rebalanceamento? Qual é a justificativa financeira dessa reação?

---

#### Nível 3 - Prompts de Ensaios Aprofundados

1. Explique a afirmação: *"Sem delta-neutral, vender uma opção equivale a tomar uma direção sem admiti-lo."* Analise o impacto dos regimes de volatilidade, liquidez e fluxo de mercado sobre uma posição unhedged versus uma posição dinamicamente protegida.

2. Avalie o dilema do rebalanceamento sob a ótica dos custos de transação e do risco de Gamma. Discuta como a escolha dos parâmetros do filtro adaptativo ($\text{base}$, $\text{gamma\_sensitivity}$, $\text{var\_sensitivity}$) afeta a sustentabilidade do P&L da carteira ao longo da vida de uma opção.

---

### Gabarito e Soluções das Questões

#### Respostas do Nível 1

1. **Resposta:** A meta fundamental não é capturar movimentos de alta ou baixa, mas manter a exposição direcional sob controle ($\Delta_{\text{total}} \approx 0$) enquanto o tempo passa, garantindo que o prêmio recebido seja defendido sem transformar a venda em uma aposta direcional descontrolada.
2. **Resposta:** O delta da opção muda conforme o *spot* se movimenta. Sem rebalanceamento, a exposição deriva e a posição se degrada em uma tomada de risco direcional exposta à aleatoriedade do mercado.
3. **Resposta:** A regra é $\text{Hedge target} = -\Delta_{\text{options}}$, o que garante que $\Delta_{\text{total}} = \Delta_{\text{options}} + \text{hedge\_units} = 0$.
4. **Resposta:** Taxa fixa por ação ($\text{fee\_cost}$), custo de deslizamento de preço ($\text{slip\_cost}$) e custo de spread compra/venda ($\text{spread\_cost}$).

---

#### Respostas do Nível 2

1. **Solução Numérica:**
   * **a)** O alvo do hedge é $\text{Hedge target} = -\Delta_{\text{options}} = -0{,}45$ unidades.
   * **b)** A quantidade a negociar é:
     $$\text{trade\_units} = \text{target} - \text{hedge\_units} = -0{,}45 - 0{,}10 = -0{,}55 \text{ unidades (venda de } 0{,}55 \text{ ações)}$$
   * **c)** Cálculo dos custos com $|\text{trade\_units}| = 0{,}55$ e $S = 50$:
     * Notional: $0{,}55 \cdot 50{,}00 = \$27{,}50$
     * $\text{fee\_cost} = 0{,}55 \cdot 0{,}02 = \$0{,}011$
     * $\text{slip\_cost} = 27{,}50 \cdot (10 \cdot 10^{-4}) = 27{,}50 \cdot 0{,}0010 = \$0{,}0275$
     * $\text{spread\_cost} = 27{,}50 \cdot (20 \cdot 10^{-4}) = 27{,}50 \cdot 0{,}0020 = \$0{,}0550$
     * $\text{trade\_cost} = 0{,}011 + 0{,}0275 + 0{,}0550 = \$0{,}0935$

2. **Solução Analítica:**
   De acordo com a fórmula:
   $$\text{adj} = \frac{\text{base}}{1{,}0 + \text{gamma\_sensitivity} \cdot |\Gamma| \cdot S + \text{var\_sensitivity} \cdot \sqrt{\dots}}$$
   Conforme $|\Gamma|$ ou a variância sobem, o denominador aumenta, o que reduz o valor de $\text{adj}$ e torna o limiar de rebalanceamento ($\text{threshold}$) mais estreito.
   *Justificativa financeira:* Um Gamma elevado significa que o Delta da opção varia rapidamente a cada movimento do spot. Uma variância alta indica movimentação acelerada do preço. Portanto, a posição exige ajustes mais frequentes (limiar menor) para evitar desvios grandes do Delta, priorizando o controle do risco em detrimento do custo de execução.

---

#### Orientação para Respostas do Nível 3

1. **Diretrizes para o Ensaio 1:**
   * O texto deve argumentar que vender uma opção sem hedge transfere a lucratividade da operação para a sorte direcional do preço à vista.
   * Deve-se abordar como mudanças no regime de volatilidade e liquidez afetam imprevisivelmente uma posição não protegida, transformando uma estrutura de arbitragem/coleta de prêmio em um risco sem controle de derrapagem.
   * Contrastar a atitude do amador (que apenas recebe o caixa e aguarda) com a do gestor institucional (que realinha a posição continuamente mantendo a estabilidade da carteira).

2. **Diretrizes para o Ensaio 2:**
   * O ensaio deve analisar o *trade-off* entre risco de rebalanceamento e custos de atrito.
   * Rebalancear frequentemente reduz o erro de rastreamento do Delta (risco de Gamma), mas gera uma acumulação contínua de custos de corretagem, slippage e spread que podem superar a margem do prêmio arrecadado.
   * Os parâmetros do controlador adaptativo equilibram essa relação: em momentos de calma ou baixo Gamma, abrem o limiar para economizar custos; em momentos de alto Gamma ou volatilidade, fecham o limiar para proteger a posição contra movimentações extremas.