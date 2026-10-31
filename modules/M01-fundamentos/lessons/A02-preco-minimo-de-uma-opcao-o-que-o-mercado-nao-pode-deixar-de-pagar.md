<!-- imported from vault study notes; curated for open course -->
# M01.A02 — Preço mínimo de uma opção: o que o mercado não pode deixar de pagar

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M01
> **Aula:** M01.A02

↑ M01 · Resumo · Completo

**Módulo:** M01
**Pergunta do módulo:** Como precificar e fazer hedge de opções vanila sem “adivinhar” o drift?

> **warning**
>
> Na lição original do Karim, "the minimal price" é a **dinâmica mínima** do preço (GBM) — o mínimo de parâmetros para obter uma distribuição. Os limites de no-arbitrage e a paridade put-call previstos na grade estão em Guia Completo §3 e em Paridade Put-Call.

## Conceito-núcleo
Limites de no-arbitrage e o “preço mínimo” como piso de replicação, não opinião subjetiva.

## Aplicação em mercado / trading
Evitar vender opções abaixo do custo de hedge; checar se prêmios observados violam limites básicos.

## Entregável / lab
Tabela call/put: preços de mercado vs limites (intrinsic, put-call parity) em 1 ticker líquido.

## Fonte (mapeamento)
quantitative-trading-free-lesson/02 the minimal price | IG Reels opções

## Guia de estudo aprofundado

> **info**
>

Este guia de estudo fornece uma análise detalhada dos fundamentos da dinâmica do Movimento Browniano Geométrico (GBM), a modelagem do log-preço, a dedução via Lema de Itô, os momentos teóricos da distribuição log-normal e a implementação de simulações Monte Carlo.

---

### Visão Geral e Objetivos de Aprendizado

Ao estudar este módulo, você deverá ser capaz de:
* Compreender a filosofia de trading de opções como gestão de convexidade e transferência de risco, em oposição a apostas direcionais.
* Derivar a equação diferencial estocástica do log-preço a partir do Movimento Browniano Geométrico utilizando o Lema de Itô.
* Calcular os parâmetros da distribuição do log-preço $m(t)$ e $v(t)$, bem como a média e a variação teórica do preço do ativo subjacente $S_t$.
* Implementar um ambiente de simulação em Python para gerar trajetórias discretas e validar a convergência do método de Monte Carlo frente à teoria.

---

### Conceitos-Chave e Fundamentação Teórica

#### Filosofia de Trading de Opções e Convexidade
O trading de opções não deve ser encarado como uma aposta direcional no mercado. O mercado nunca fornece a informação exata sobre o comportamento do preço no futuro; a única informação verdadeiramente confiável disponível é o preço atual. 

Nesse contexto, uma opção é uma transferência de risco onde se paga um prêmio para mover uma convexidade. O papel do operador de opções é gerenciar essa convexidade e manter o prêmio intacto, independentemente de o mercado subir ou descer. Para transitar entre cenários dentro dessa convexidade, é necessário definir uma dinâmica estocástica para o preço do ativo $S_t$.

#### O Modelo do Movimento Browniano Geométrico (GBM)
Escolhe-se o Movimento Browniano Geométrico como dinâmica base por ser um modelo simples que utiliza o mínimo de parâmetros necessários para gerar uma distribuição utilizável. A equação diferencial estocástica (SDE) do GBM é dada por:

$$dS_t = \mu S_t\,dt + \sigma S_t\,dW_t, \qquad S_0 > 0$$

A variação infinitesimal do preço $dS_t$ é composta por duas partes:
1. **Tendência Determinística (Drift):** $\mu S_t\,dt$, proporcional ao preço atual e ao tempo, ponderada pela taxa de deriva $\mu$.
2. **Choque Aleatório (Ruído):** $\sigma S_t\,dW_t$, uma perturbação proporcional ao preço com intensidade de volatilidade $\sigma$, conduzida pelo processo de Wiener $dW_t$.
3. **Condição Inicial:** $S_0 > 0$, garantindo que o preço seja estritamente positivo, permitindo a aplicação de transformações logarítmicas.

#### Derivação da Dinâmica do Log-Preço via Lema de Itô
Como o preço varia em porcentagens multiplicativas, a transformação logarítmica transforma multiplicações em somas. Define-se a variável do log-preço por:

$$X_t = \ln(S_t)$$

Para determinar a dinâmica de $X_t$, aplica-se o Lema de Itô à função $f(S) = \ln(S)$. Calculam-se as derivadas de primeira e segunda ordem:

$$f'(S) = \frac{1}{S}, \qquad f''(S) = -\frac{1}{S^2}$$

Pelo Lema de Itô, a expansão estocástica de $X_t = f(S_t)$ é:

$$dX_t = f'(S_t) dS_t + \frac{1}{2} f''(S_t) (dS_t)^2$$

Onde $f'(S_t) dS_t$ representa o termo de transporte e $\frac{1}{2} f''(S_t) (dS_t)^2$ representa o termo de correção devido à curvatura (convexidade) da função logarítmica.

Substituindo $dS_t$:

$$(dS_t)^2 = (\mu S_t\,dt + \sigma S_t\,dW_t)^2 = \sigma^2 S_t^2 (dW_t)^2 = \sigma^2 S_t^2\,dt$$

Notando que $(dW_t)^2 = dt$ e que termos de ordem superior como $dt^2$ e $dt\,dW_t$ são desprezíveis na ordem infinitesimal.

Substituindo $f'(S_t)$, $f''(S_t)$, $dS_t$ e $(dS_t)^2$ na equação do Lema de Itô:

$$dX_t = \frac{1}{S_t} (\mu S_t\,dt + \sigma S_t\,dW_t) + \frac{1}{2} \left(-\frac{1}{S_t^2}\right) (\sigma^2 S_t^2\,dt)$$

$$dX_t = \mu\,dt + \sigma\,dW_t - \frac{1}{2}\sigma^2\,dt$$

$$dX_t = \left(\mu - \frac{1}{2}\sigma^2\right)dt + \sigma\,dW_t$$

Essa equação mostra que o log-preço avança com uma tendência constante $a = \mu - \frac{1}{2}\sigma^2$ e flutua com um ruído de intensidade $b = \sigma$.

#### Solução Analítica do Preço e Distribuição
Integrando a equação de $dX_t$ no intervalo $[0, t]$:

$$X_t = X_0 + \left(\mu - \frac{1}{2}\sigma^2\right)t + \sigma W_t$$

Onde $X_0 = \ln(S_0)$ e $W_t \sim \mathcal{N}(0, t)$.

Como $X_t$ é uma combinação linear de uma constante e de uma variável com distribuição Normal, $X_t$ também segue uma distribuição Normal:

$$\ln(S_t) = X_t \sim \mathcal{N}(m(t), v(t))$$

Os parâmetros de média $m(t)$ e variância $v(t)$ da variável Normal $X_t$ são:

$$m(t) = \ln(S_0) + \left(\mu - \frac{1}{2}\sigma^2\right)t$$

$$v(t) = \sigma^2 t$$

Retornando à variável original de preço através da função exponencial $S_t = \exp(X_t)$:

$$S_t = S_0 \exp\left(\left(\mu - \frac{1}{2}\sigma^2\right)t + \sigma W_t\right)$$

Sendo $X_t$ normalmente distribuído, o preço $S_t$ segue uma distribuição Log-Normal.

#### Momentos Teóricos do Preço
Apesar de o log-preço ter uma tendência corrigida pela metade da variância $\left(\mu - \frac{1}{2}\sigma^2\right)$, o valor esperado do preço $S_t$ cresce à taxa contínua $\mu$:

$$\mathbb{E}[S_t] = S_0 e^{\mu t}$$

A dispersão do preço, medida pela sua variância teórica, expanda-se exponencialmente com o tempo e acelera com o aumento da volatilidade $\sigma^2$:

$$\operatorname{Var}(S_t) = S_0^2 e^{2\mu t} \left(e^{\sigma^2 t} - 1\right)$$

#### Função de Densidade de Probabilidade (PDF) Log-Normal
A densidade teórica de probabilidade do preço $S_T$ para $s > 0$ é dada por:

$$f_{S_T}(s) = \frac{1}{s \sqrt{2\pi v}} \exp\left(-\frac{(\ln s - m)^2}{2v}\right)$$

Para $s \le 0$, a densidade é nula, refletindo a não-negatividade do preço no modelo GBM.

---

### Intuição de Mercado e Trading

* **Ajuste de Convexidade ($-\frac{1}{2}\sigma^2$):** A razão pela qual a tendência do log-preço é $\mu - \frac{1}{2}\sigma^2$ e não simplesmente $\mu$ decorre da curvatura da função logarítmica. Em ambientes de alta volatilidade ($\sigma$), a mediana do preço fica abaixo do valor esperado da média.
* **Gerenciamento de Prêmio vs. Aposta Direcional:** Como o trader não domina a direção do mercado, ele estrutura suas posições para explorar a distribuição implícita $S_T$. O valuation de opções baseia-se na dinâmica de propagação dessa distribuição ao longo do tempo $T$.

---

### Exemplo Numérico Resolvido Passo a Passo

Considere um ativo com as seguintes características de mercado:
* Preço inicial: $S_0 = 100,0$
* Taxa de deriva (drift): $\mu = 0,08$ ($8\%$ ao ano)
* Volatilidade: $\sigma = 0,02$ ($2\%$ ao ano)
* Horizonte temporal: $T = 1,0$ ano

#### Passo 1 Calcular os parâmetros $m(T)$ e $v(T)$ do log-preço

$$m(T) = \ln(S_0) + \left(\mu - \frac{1}{2}\sigma^2\right)T$$

1. $\ln(S_0) = \ln(100,0) \approx 4,605170$$
2. $\sigma^2 = (0,02)^2 = 0,0004$$
3. $\frac{1}{2}\sigma^2 = 0,0002$$
4. $\mu - \frac{1}{2}\sigma^2 = 0,08 - 0,0002 = 0,0798$$
5. $m(1,0) = 4,605170 + 0,0798 \times 1,0 = 4,684970$$

$$v(T) = \sigma^2 T = 0,0004 \times 1,0 = 0,0004$$

#### Passo 2 Calcular a Média Teórica do Preço $\mathbb{E} S_T $

$$\mathbb{E}[S_T] = S_0 e^{\mu T} = 100,0 \times e^{0,08 \times 1,0} = 100,0 \times e^{0,08}$$

Sabendo que $e^{0,08} \approx 1,083287$:

$$\mathbb{E}[S_T] \approx 100,0 \times 1,083287 = 108,3287$$

#### Passo 3 Calcular a Variância Teórica do Preço $\operatorname{Var}(S_T)$

$$\operatorname{Var}(S_T) = S_0^2 e^{2\mu T} \left(e^{\sigma^2 T} - 1\right)$$

1. $S_0^2 = 100,0^2 = 10\,000,0$$
2. $e^{2\mu T} = e^{2 \times 0,08 \times 1,0} = e^{0,16} \approx 1,173511$$
3. $e^{\sigma^2 T} - 1 = e^{0,0004} - 1 \approx 1,00040008 - 1 = 0,00040008$$
4. $\operatorname{Var}(S_T) = 10\,000,0 \times 1,173511 \times 0,00040008 \approx 4,6949$$

---

### Armadilhas Comuns

* **Esquecer o Termo de Correção de Itô:** O erro mais comum ao integrar a SDE do GBM é supor que $dX_t = \mu\,dt + \sigma\,dW_t$. O termo $-\frac{1}{2}\sigma^2$ surge estritamente da derivada de segunda ordem $f''(S) = -1/S^2$ e da propriedade de que $(dW_t)^2 = dt$.
* **Confundir Média do Log-Preço com o Log da Média do Preço:** Note que $\mathbb{E}[\ln(S_T)] = m(T) = \ln(S_0) + (\mu - \frac{1}{2}\sigma^2)T$, ao passo que $\ln(\mathbb{E}[S_T]) = \ln(S_0) + \mu T$.
* **Avaliação da Densidade para Preços Nulos ou Negativos:** A função de densidade da log-normal $f_{S_T}(s)$ só é definida para $s > 0$. Na implementação computacional, é indispensável utilizar uma máscara booleana ($s > 0$) para evitar erros de divisão por zero ou logaritmo de números não positivos.
* **Amostragem Indireta vs. Direta:** Na simulação estocástica do GBM, não se deve simular variações diretamente sobre $S$ adicionando ruídos aditivos simples. O correto é acumular os incrementos no domínio do log-preço ($\Delta X$) e depois aplicar a função exponencial.

---

### Lab Prático em Python

Este laboratório descreve a criação de um script estruturado para calcular os parâmetros teóricos do GBM e realizar simulações de Monte Carlo validando a convergência estatística.

#### Passo 1 Definição dos Parâmetros Teóricos do Log-Preço
Crie uma função `gbm_ln_params(S0, mu, sigma, T)` que recebe os parâmetros do mercado e retorna a média $m$ e a variância $v$ do log-preço:
* Cálculo: $m = \ln(S_0) + (\mu - 0,5 \cdot \sigma^2) \cdot T$
* Cálculo: $v = \sigma^2 \cdot T$

#### Passo 2 Cálculo dos Momentos Fechados da Log-Normal
Crie uma função `gbm_ST_moments(S0, mu, sigma, T)` que calcula o valor esperado e a variância exata do preço $S_T$:
* Média teórica: $mean = S_0 \cdot \exp(\mu \cdot T)$
* Variância teórica: $var = S_0^2 \cdot \exp(2 \mu T) \cdot (\exp(\sigma^2 T) - 1,0)$

#### Passo 3 Implementação da Densidade de Probabilidade Log-Normal
Crie uma função `lognormal_pdf(s, m, v)` para mapear a curva teórica do preço:
* Crie uma máscara para identificar elementos onde $s > 0$.
* Para os pontos válidos, aplique a fórmula:
  $$pdf[mask] = \frac{1}{s \sqrt{2\pi v}} \exp\left(-\frac{(\ln(s) - m)^2}{2v}\right)$$

#### Passo 4 Simulação de Trajetórias Discretas do GBM
Crie a função `simulate_gbm_paths(S0, mu, sigma, T, nsteps, N, seed=42)`:
1. Calcule o intervalo discreto de tempo $dt = T / nsteps$.
2. Gere uma matriz $Z$ de dimensão $(N, nsteps)$ com números aleatórios da distribuição Normal Padrão $\mathcal{N}(0,1)$.
3. Calcule a matriz de incrementos discretos do log-preço:
   $$\Delta X = \left(\mu - 0,5 \cdot \sigma^2\right) dt + \sigma \sqrt{dt} \cdot Z$$
4. Realize a soma acumulada dos incrementos ao longo do tempo (eixo dos passos temporais) utilizando `np.cumsum`.
5. Reconstrua a matriz de preços $S$:
   $$S_{t_k} = S_0 \cdot \exp\left(\sum_{j=1}^{k} \Delta X_j\right)$$

#### Passo 5 Execução do Teste de Convergência de Monte Carlo
Defina os parâmetros globais ($S_0 = 100,0$, $\mu = 0,08$, $\sigma = 0,02$, $T = 1,0$, $nsteps = 252$).
Execute a simulação para diferentes tamanhos de amostra $N \in [1\,000, 10\,000, 100\,000]$:
1. Extraia o vetor de preços finais $S_T$ (última coluna da matriz de simulação).
2. Calcule a média empírica do vetor $S_T$.
3. Calcule a variância empírica da amostra utilizando $ddof=1$.
4. Compare os valores empíricos obtidos com a média e variância teóricas calculadas no Passo 2, observando a redução do erro à medida que $N$ aumenta.

---

### Glossário de Termos Importantes

* **Convexiade (Convexity):** Propriedade não linear do valor de um derivativo em relação ao preço do ativo subjacente. No contexto de opções, representa a alteração do perfil de risco que exige gerenciamento e conservação do prêmio pago.
* **Movimento Browniano Geométrico (GBM):** Processo estocástico em tempo contínuo no qual o logaritmo da variável aleatória segue um Movimento Browniano com deriva. É o modelo padrão para dinâmica de preços de ativos.
* **Lema de Itô:** Teorema do cálculo estocástico utilizado para encontrar a diferencial de uma função dependente de um ou mais processos estocásticos.
* **Processo de Wiener ($W_t$):** Processo estocástico em tempo contínuo com incrementos independentes e normalmente distribuídos, tais que $W_t - W_s \sim \mathcal{N}(0, t-s)$.
* **Taxa de Deriva (Drift - $\mu$):** Taxa de retorno médio anualizado esperada do ativo subjacente de forma determinística.
* **Ajuste de Volatilidade ($-\frac{1}{2}\sigma^2$):** Redução aplicada à taxa de deriva no domínio do log-preço, decorrente da segunda derivada da transformação logarítmica via Lema de Itô.
* **Distribuição Log-Normal:** Distribuição de probabilidade contínua de uma variável aleatória cujo logaritmo é normalmente distribuído.

---

### Exercícios e Questões de Fixação

#### Nível 1 Básico / Resposta Curta

**Questão 1**
Qual é a principal premissa defendida em relação à finalidade do trading de opções?
*Resposta:* O trading de opções não é uma aposta direcional, mas sim uma transferência de risco paga por meio de um prêmio para gerenciar a convexidade do perfil de pagamento, mantendo o prêmio intacto independente do sentido do mercado.

**Questão 2**
Por que a condição $S_0 > 0$ é indispensável no modelo do Movimento Browniano Geométrico?
*Resposta:* A condição $S_0 > 0$ garante que o preço do ativo permaneça estritamente positivo em qualquer instante $t$, permitindo a aplicação da transformação logarítmica $X_t = \ln(S_t)$ sem indefinições matemáticas.

**Questão 3**
Quais são a média $m(t)$ e a variância $v(t)$ da variável log-preço $\ln(S_t)$ no modelo GBM?
*Resposta:* A média é $m(t) = \ln(S_0) + \left(\mu - \frac{1}{2}\sigma^2\right)t$ e a variância é $v(t) = \sigma^2 t$.

---

#### Nível 2 Intermediário / Análise e Aplicação

**Questão 4**
Utilizando o Lema de Itô para $f(S) = \ln(S)$, mostre explicitamente a origem do termo $-\frac{1}{2}\sigma^2\,dt$ na dinâmica de $dX_t$.
*Resposta:*
Ao expandir $dX_t = f'(S_t)dS_t + \frac{1}{2}f''(S_t)(dS_t)^2$:
1. As derivadas são $f'(S) = \frac{1}{S}$ e $f''(S) = -\frac{1}{S^2}$.
2. A variação ao quadrado é $(dS_t)^2 = (\mu S_t dt + \sigma S_t dW_t)^2 = \sigma^2 S_t^2 dt$ (pois $(dW_t)^2 = dt$).
3. O segundo termo da expansão fica:
   $$\frac{1}{2} f''(S_t) (dS_t)^2 = \frac{1}{2} \left(-\frac{1}{S_t^2}\right) \left(\sigma^2 S_t^2 dt\right) = -\frac{1}{2}\sigma^2\,dt$$
Esse termo de curvatura ajusta a deriva determinística do log-preço.

**Questão 5**
Considere um ativo com $S_0 = 50$, $\mu = 0,10$, $\sigma = 0,30$ e $T = 0,5$ anos. Calcule o valor esperado teórico do preço $\mathbb{E}[S_T]$ e o parâmetro de média do log-preço $m(T)$.
*Resposta:*
1. **Média teórica do preço $\mathbb{E}[S_T]$:**
   $$\mathbb{E}[S_T] = S_0 e^{\mu T} = 50 \times e^{0,10 \times 0,5} = 50 \times e^{0,05} \approx 50 \times 1,051271 = 52,5635$$
2. **Parâmetro $m(T)$ do log-preço:**
   $$m(T) = \ln(50) + \left(0,10 - \frac{1}{2}(0,30)^2\right) \times 0,5$$
   $$\ln(50) \approx 3,912023$$
   $$0,10 - 0,5 \times 0,09 = 0,10 - 0,045 = 0,055$$
   $$m(0,5) = 3,912023 + (0,055 \times 0,5) = 3,912023 + 0,0275 = 3,939523$$

---

#### Nível 3 Avançado / Questões Dissertativas

**Questão 6**
Explique detalhadamente por que a simulação de trajetórias do GBM em códigos de programação deve ser feita acumulando os incrementos do log-preço em vez de aplicar diretamente aproximações lineares ao preço $S_t$.
*Resposta:*
A aproximação linear direta $S_{t+\Delta t} = S_t + \mu S_t \Delta t + \sigma S_t \sqrt{\Delta t} Z$ é uma discretização de Euler-Maruyama sobre o preço que introduz erros de discretização e permite que, sob volatilidades elevadas ou passos de tempo grandes, o preço $S_t$ assuma valores negativos, violando a premissa fundamental $S_t > 0$.

Ao utilizar a estrutura do log-preço:
$$\Delta X = \left(\mu - \frac{1}{2}\sigma^2\right)\Delta t + \sigma \sqrt{\Delta t} Z$$
$$X_t = X_0 + \sum \Delta X$$
$$S_t = \exp(X_t)$$

A propriedade de não-negatividade de $S_t$ é preservada para qualquer valor de $Z \in \mathbb{R}$, pois a função exponencial de números reais é estritamente positiva. Além disso, a simulação no domínio logarítmico reflete exatamente a solução analítica exata da SDE em tempo contínuo, garantindo convergência perfeita dos momentos estatísticos quando a amostragem de Monte Carlo $N$ tende ao infinito.