<!-- imported from vault study notes; curated for open course -->
# M02.A02 — Gregas: o painel de risco do livro de opções

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M02
> **Aula:** M02.A02

↑ M02 · Resumo · Completo

**Módulo:** M02
**Pergunta do módulo:** Como a dinâmica do spot e as gregas mudam o P&L do livro?

## Conceito-núcleo
Δ, Γ, Θ, ν, ρ como derivadas do preço; sensibilidade operacional do book.

## Aplicação em mercado / trading
Definir limites de gregas, decidir rebalance e escolher strikes por perfil de risco (não só por “premio alto”).

## Entregável / lab
Painel: gregas vs spot/tempo/vol para 1 estrutura (ex.: straddle ou risk reversal).

## Fonte (mapeamento)
quantitative-trading-free-lesson/07 the greeks | IG Reel greeks

## Guia de estudo aprofundado

> **info**
>

### Visão Geral e Modelo de Referência

O modelo de precificação de opções de Black-Scholes estabelece um arcabouço estruturado para precificar uma opção de compra (*call*) europeia sobre um ativo subjacente $S_t$. O ativo segue um Movimento Browniano Geométrico (GBM) sob a medida neutra ao risco $\mathbb{Q}$, com taxa livre de risco constante $r$ e volatilidade constante $\sigma$.

No tempo $t = 0$, a fórmula do preço de uma *call* europeia com preço de exercício $K$ e maturidade $T$ é dada por:

$$C_0 = S_0 N(d_1) - K e^{-rT} N(d_2)$$

Onde os parâmetros $d_1$ e $d_2$ são definidos como:

$$d_1 = \frac{\ln(S_0/K) + \left(r + \frac{1}{2}\sigma^2\right)T}{\sigma\sqrt{T}}$$

$$d_2 = d_1 - \sigma\sqrt{T}$$

Neste contexto, $N(\cdot)$ representa a função de distribuição acumulada (CDF) da normal padrão, enquanto $\varphi(\cdot)$ representa sua função de densidade de probabilidade (PDF).

No ecossistema de derivativos, as **Gregas** funcionam como medidores de sensibilidade do preço da opção em relação a alterações nos parâmetros do mercado. Elas operam como sensores do painel de risco de um livro de opções, indicando a taxa de variação do valor do ativo à medida que os parâmetros de entrada mudam.

---

### Conceitos-Chave e Intuição das Gregas

#### Delta

O Delta ($\Delta$) representa a sensibilidade do preço da opção em relação às variações no preço do ativo subjacente ($S_0$). Matematicamente, é a primeira derivada parcial do preço da opção em relação a $S_0$:

$$\Delta = \frac{\partial C_0}{\partial S_0} = N(d_1)$$

##### Intuição de Mercado
Para uma *call*, à medida que o preço *spot* aumenta, o *payoff* no vencimento aproxima-se do comportamento do próprio ativo subjacente. 
* Opções muito dentro do preço (*deep ITM*): o Delta aproxima-se de $1$.
* Opções muito fora do preço (*deep OTM*): o Delta aproxima-se de $0$.
* Entre esses extremos, o Delta evolui como uma probabilidade neutra ao risco suavizada através de $d_1$.

#### Gamma

O Gamma ($\Gamma$) mede a curvatura da opção, ou seja, a velocidade de variação do próprio Delta em relação às mudanças no preço do ativo subjacente:

$$\Gamma = \frac{\partial^2 C_0}{\partial S_0^2} = \frac{\partial \Delta}{\partial S_0} = \frac{\varphi(d_1)}{S_0 \sigma \sqrt{T}}$$

##### Intuição de Mercado
O Gamma é estritamente positivo para uma *call* comprada (*long call*), refletindo uma convexidade positiva. Ele atinge seu valor máximo na região do preço de exercício onde a opção está no preço (*at-the-money* - ATM), ponto em que o Delta sofre as alterações mais rápidas. Para opções *deep ITM* ou *deep OTM*, a curva do Delta torna-se plana e o Gamma cai para valores próximos de zero.

#### Vega

O Vega mede a sensibilidade do preço da opção em relação à volatilidade do ativo subjacente ($\sigma$):

$$\text{Vega} = \frac{\partial C_0}{\partial \sigma} = S_0 \varphi(d_1) \sqrt{T}$$

##### Intuição de Mercado
A volatilidade funciona como o regulador do "túnel de cenários possíveis". Como a *call* possui um *payoff* convexo, o alargamento desse túnel decorrente de uma volatilidade mais alta aumenta o valor esperado da opção. O Vega atinge sua magnitude máxima em opções ATM, onde o impacto da convexidade sobre a precificação é mais pronunciado.

#### Theta

O Theta ($\Theta$) representa a sensibilidade do preço da opção em relação ao tempo até o vencimento ($T$):

$$\Theta = \frac{\partial C_0}{\partial T} = -\frac{S_0 \varphi(d_1) \sigma}{2\sqrt{T}} - r K e^{-rT} N(d_2)$$

##### Intuição de Mercado
A equação do Theta é dividida em dois componentes estruturais:
1. **Decaimento temporal puro:** representado pelo primeiro termo, tipicamente negativo para uma posição comprada em *call*.
2. **Efeito do desconto do strike e taxa de juros:** representado pelo segundo termo, atrelado à taxa de desconto do preço de exercício.

Na prática de negociação, manter uma posição comprada em *call* (*long call*) acarreta um Theta predominantemente negativo. Caso as variáveis de mercado permaneçam inalteradas, a passagem do tempo corrói o valor da opção.

#### Rho

O Rho ($\rho$) mede a sensibilidade do preço da opção em relação à taxa de juros livre de risco ($r$):

$$\rho = \frac{\partial C_0}{\partial r} = K T e^{-rT} N(d_2)$$

##### Intuição de Mercado
Com o aumento da taxa de juros $r$, o valor presente do preço de exercício descontado ($K e^{-rT}$) diminui. Consequentemente, o custo relativo do exercício futuro reduz-se, elevando o valor intrínseco da *call*. Por essa razão, o Rho de uma *call* é positivo.

---

### Verificação Numérica por Diferenças Finitas

Para garantir a precisão matemática do painel de risco e validar as derivadas analíticas, utiliza-se a aproximação numérica por diferenças finitas.

| Grega | Método de Diferenças Finitas | Fórmula de Aproximação |
| :--- | :--- | :--- |
| **Delta** ($\Delta_{FD}$) | Centralizada | $\Delta_{FD} \approx \frac{C(S_0+h) - C(S_0-h)}{2h}$ |
| **Gamma** ($\Gamma_{FD}$) | Segunda derivada centralizada | $\Gamma_{FD} \approx \frac{C(S_0+h) - 2C(S_0) + C(S_0-h)}{h^2}$ |
| **Vega** ($\text{Vega}_{FD}$) | Centralizada em $\sigma$ | $\text{Vega}_{FD} \approx \frac{C(\sigma+h) - C(\sigma-h)}{2h}$ |
| **Theta** ($\Theta_{FD}$) | Regressiva (*backward*) | $\Theta_{FD} \approx \frac{C(T-h) - C(T)}{-h}, \quad T-h > 0$ |
| **Rho** ($\rho_{FD}$) | Centralizada em $r$ | $\rho_{FD} \approx \frac{C(r+h) - C(r-h)}{2h}$ |

---

### Exemplo Numérico Resolvido Passo a Passo

Considerem-se os seguintes parâmetros de teste de mercado:
* $S_0 = 100$
* $K = 100$
* $r = 0{,}03$ (3% ao ano)
* $\sigma = 0{,}20$ (20% ao ano)
* $T = 1$ ano

#### Passo 1 Cálculo de $d_1$ e $d_2$

$$d_1 = \frac{\ln(100/100) + \left(0{,}03 + \frac{1}{2}(0{,}20)^2\right)(1)}{0{,}20 \sqrt{1}} = \frac{0 + (0{,}03 + 0{,}02)}{0{,}20} = \frac{0{,}05}{0{,}20} = 0{,}25$$

$$d_2 = 0{,}25 - 0{,}20 \sqrt{1} = 0{,}05$$

#### Passo 2 Cálculo das Probabilidades Acumuladas e Densidade

Com $d_1 = 0{,}25$ e $d_2 = 0{,}05$:
* $\varphi(d_1) = \varphi(0{,}25) = \frac{1}{\sqrt{2\pi}} e^{-\frac{0{,}25^2}{2}} \approx 0{,}3867$
* $N(d_1) = N(0{,}25) \approx 0{,}5987$
* $N(d_2) = N(0{,}05) \approx 0{,}5199$

#### Passo 3 Precificação da Call ($C_0$)

$$C_0 = 100 \times 0{,}5987 - 100 \times e^{-0{,}03 \times 1} \times 0{,}5199$$
$$C_0 = 59{,}87 - 100 \times 0{,}970446 \times 0{,}5199 = 59{,}87 - 50{,}45 = 9{,}42$$

#### Passo 4 Cálculo Analítico das Gregas

1. **Delta ($\Delta$):**
   $$\Delta = N(d_1) = 0{,}5987$$

2. **Gamma ($\Gamma$):**
   $$\Gamma = \frac{\varphi(d_1)}{S_0 \sigma \sqrt{T}} = \frac{0{,}3867}{100 \times 0{,}20 \times 1} = \frac{0{,}3867}{20} = 0{,}019335$$

3. **Vega:**
   $$\text{Vega} = S_0 \varphi(d_1) \sqrt{T} = 100 \times 0{,}3867 \times 1 = 38{,}67$$

4. **Theta ($\Theta$):**
   $$\Theta = -\frac{100 \times 0{,}3867 \times 0{,}20}{2 \sqrt{1}} - 0{,}03 \times 100 \times e^{-0{,}03} \times 0{,}5199$$
   $$\Theta = -\frac{7{,}734}{2} - 0{,}03 \times 97{,}0446 \times 0{,}5199 = -3{,}867 - 1{,}5136 = -5{,}3806$$

5. **Rho ($\rho$):**
   $$\rho = 100 \times 1 \times e^{-0{,}03} \times 0{,}5199 = 100 \times 0{,}970446 \times 0{,}5199 = 50{,}453$$

---

### Armadilhas Comuns no Redirecionamento e Hedging

#### Escolha Inadequada do Incremento $h$
Ao calcular derivadas parciais via diferenças finitas para validar ou executar um *hedge*, a calibração do passo $h$ apresenta duas armadilhas numéricas:
* **$h$ muito grande:** introduz erro substancial de discretização. A aproximação deixa de refletir a derivada no ponto exato e passa a medir uma inclinação média sobre um intervalo extenso.
* **$h$ muito pequeno:** expõe o cálculo a erros numéricos de arredondamento e cancelamento catastrófico na representação de ponto flutuante do computador.

#### Riscos Implicados no Hedge Incorreto
As gregas não são abstrações conceituais; constituem a base para a neutralização de riscos de um livro de derivativos. Se as equações analíticas forem implementadas com erros ou validadas incorretamente via diferenças finitas devido ao parâmetro $h$ desajustado, a estratégia de *hedge* falhará. Isso fará com que o gestor assuma exposições indesejadas e riscos não mapeados de mercado.

---

### Lab Prático Sugerido em Python

Para consolidar o aprendizado, sugere-se a implementação de um laboratório em Python estruturado nas seguintes etapas:

1. **Estruturação da Precificação:**
   * Implementar uma função `black_scholes_call(S, K, r, sigma, T)` utilizando a biblioteca `scipy.stats` para obter as funções $N(\cdot)$ (`norm.cdf`) e $\varphi(\cdot)$ (`norm.pdf`).

2. **Implementação Analítica das Gregas:**
   * Criar funções dedicadas para calcular analiticamente os valores de $\Delta$, $\Gamma$, $\text{Vega}$, $\Theta$ e $\rho$ para os parâmetros do ponto de teste ($S_0=100, K=100, r=0{,}03, \sigma=0{,}20, T=1$).

3. **Implementação por Diferenças Finitas:**
   * Escrever rotinas numéricas para calcular $\Delta_{FD}$, $\Gamma_{FD}$, $\text{Vega}_{FD}$, $\Theta_{FD}$ e $\rho_{FD}$ utilizando as fórmulas de diferenças centradas e regressivas descritas na teoria.

4. **Análise do Comportamento do Passos de Discretização ($h$):**
   * Avaliar a precisão da aproximação variando $h$ em uma escala logarítmica (ex: de $h = 10^{-1}$ até $h = 10^{-6}$).
   * Comparar os erros absolutos e relativos gerados pela aproximação numérica em relação ao valor analítico exato para identificar a faixa ideal de $h$.

---

### Glossário

* **At-the-Money (ATM):** Situação em que o preço do ativo subjacente ($S_0$) é igual ou muito próximo ao preço de exercício ($K$) da opção.
* **Curvatura:** Taxa de variação de segunda ordem de uma função, representada no mercado de opções pelo Gamma.
* **Delta ($\Delta$):** Primeira derivada do preço da opção em relação ao preço do ativo subjacente; mede a sensibilidade de primeira ordem ao preço *spot*.
* **Diferenças Finitas:** Método numérico empregado para aproximar derivadas de funções contínuas por meio de incrementos discretos ($h$).
* **Gamma ($\Gamma$):** Segunda derivada do preço da opção em relação ao ativo subjacente; mede a variação do Delta e a convexidade da opção.
* **In-the-Money (ITM):** Condição em que a opção possui valor intrínseco. Para uma *call*, ocorre quando $S_0 > K$.
* **Out-of-the-Money (OTM):** Condição em que a opção não possui valor intrínseco. Para uma *call*, ocorre quando $S_0 < K$.
* **Rho ($\rho$):** Derivada do preço da opção em relação à taxa de juros livre de risco $r$.
* **Theta ($\Theta$):** Derivada do preço da opção em relação ao tempo até o vencimento $T$; mede a taxa de sensibilidade ou decaimento temporal.
* **Vega:** Derivada do preço da opção em relação à volatilidade do ativo subjacente $\sigma$.

---

### Questões de Fixação e Ensaios

#### Nível 1 Exercícios Rápidos de Fixação

##### Questão 1
Qual é a interpretação do Delta ($\Delta$) de uma *call* europeia e quais são seus limites quando a opção está profundamente dentro do preço (*deep ITM*) e profundamente fora do preço (*deep OTM*)?

**Resposta:**
O Delta mede a sensibilidade de primeira ordem do preço da opção em relação às variações no preço do ativo subjacente ($S_0$). Quando a *call* está *deep ITM*, seu preço varia quase na proporção de $1:1$ com o ativo, de modo que o Delta tende a $1$. Quando está *deep OTM*, a probabilidade de exercício torna-se marginal, fazendo com que o Delta tenda a $0$.

##### Questão 2
Por que o Gamma ($\Gamma$) atinge seu valor máximo quando a opção está no preço (*at-the-money* - ATM)?

**Resposta:**
O Gamma mede a velocidade com que o Delta muda em relação a $S_0$. Na região ATM, a probabilidade de a opção terminar no preço ou fora do preço é altamente sensível a pequenas variações de $S_0$. Por ser a área de maior incerteza e inclinação da curva do Delta, a variação do Delta é mais rápida, maximizando o Gamma.

---

#### Nível 2 Aplicação Numérica e Análise

##### Questão 3
Considere uma *call* europeia sob os parâmetros $S_0=100, K=100, r=0{,}03, \sigma=0{,}20, T=1$. Utilizando a aproximação por diferença finita centrada para o Delta com um passo $h = 1$, expresse a fórmula a ser calculada e explique a importância da escolha do valor de $h$.

**Resposta:**
A fórmula da diferença finita centrada para o Delta é dada por:

$$\Delta_{FD} \approx \frac{C(S_0+h) - C(S_0-h)}{2h} = \frac{C(101) - C(99)}{2}$$

A escolha de $h$ é crítica: se $h$ for excessivamente grande (como um valor ordinal elevado), o resultado conterá um erro substancial de discretização, falhando em capturar a derivada pontual. Por outro lado, se $h$ for extremamente pequeno (ex: próximo do limite de precisão da máquina), erros de arredondamento e cancelamento numérico distorcerão a aproximação.

##### Questão 4
Analise o impacto no Vega de uma *call* quando a volatilidade $\sigma$ do ativo subjacente aumenta. Por que uma volatilidade maior eleva o valor do contrato?

**Resposta:**
O Vega é dado por $\text{Vega} = S_0 \varphi(d_1) \sqrt{T}$, um valor estritamente positivo. O aumento da volatilidade expande a largura do túnel de cenários futuros possíveis para o preço do ativo subjacente. Como o *payoff* de uma opção de compra é convexo (limitado inferiormente a zero), a expansão da dispersão dos resultados aumenta o valor esperado do *payoff* no vencimento sob a medida neutra ao risco $\mathbb{Q}$, elevando o preço da *call*.

---

#### Nível 3 Ensaio e Reflexão Avançada

##### Questão 5
Explicite os dois componentes da fórmula do Theta ($\Theta$) para uma *call* europeia segundo o modelo de Black-Scholes. Discuta as implicações de um modelo de risco que negligencie a precisão da estimativa do Theta na gestão de um livro de derivativos neutralizado em Delta.

**Resposta:**
A expressão analítica do Theta é composta por dois termos distintos:

$$\Theta = -\frac{S_0 \varphi(d_1) \sigma}{2\sqrt{T}} - r K e^{-rT} N(d_2)$$

O primeiro termo ($-\frac{S_0 \varphi(d_1) \sigma}{2\sqrt{T}}$) captura o decaimento temporal puro do valor da opção decorrente do encurtamento do horizonte de maturidade. Este termo é estritamente negativo para posições compradas. O segundo termo ($- r K e^{-rT} N(d_2)$) reflete o efeito do custo do dinheiro e do desconto do valor presente do strike.

Em um livro de opções mantido com *hedge* de Delta (Delta-neutro), o gestor elimina a exposição primária ao movimento direcional do preço do ativo subjacente. Contudo, o tempo continua a fluir. Se o painel de risco utilizar equações incorretas ou aproximações numéricas imprecisas para o Theta, a mesa de operações subestimará a perda diária decorrente da atrição temporal (*time decay*). Esse desalinhamento leva a uma leitura distorcida do Lucro e Perda (P&L) acumulado do livro, expondo a carteira a riscos residuais e desalinhamentos de cobertura não mapeados.