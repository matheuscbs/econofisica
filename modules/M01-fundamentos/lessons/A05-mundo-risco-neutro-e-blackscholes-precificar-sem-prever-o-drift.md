<!-- imported from vault study notes; curated for open course -->
# M01.A05 — Mundo risco-neutro e Black–Scholes: precificar sem prever o drift

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M01
> **Aula:** M01.A05

↑ M01 · Resumo · Completo

**Módulo:** M01
**Pergunta do módulo:** Como precificar e fazer hedge de opções vanila sem “adivinhar” o drift?

## Conceito-núcleo
Medida risco-neutra: o preço é esperança descontada sob Q; BSM como PDE de replicação.

## Aplicação em mercado / trading
Separar “previsão de retorno” de “preço justo de opção”; usar BSM como linguagem de cotação (IV).

## Entregável / lab
Implementar BSM call/put + IV invertida a partir de um snapshot de mercado.

## Fonte (mapeamento)
quantitative-trading-free-lesson/05 the-risk-neutral-world-black–scholes-pricing | IG BSM/difusão

## Guia de estudo aprofundado

> **info**
>

Este guia de estudo oferece uma síntese abrangente e rigorosa sobre a precificação de opções no mundo risco-neutro e a derivação da fórmula de Black-Scholes, com base no material técnico de Karim Khemiri (Khem Kapital).

---

### Visão Geral e Objetivos de Aprendizagem

Ao estudar este material, você será capaz de:
* Compreender o conceito de medida risco-neutra $Q$ e a razão do descarte da taxa de retorno real ($\mu$) na precificação.
* Utilizar o Lema de Itô para transformar o Movimento Browniano Geométrico (GBM) na dinâmica do log-preço.
* Interpretar os componentes da fórmula fechada de Black-Scholes para uma call europeia ($d_1$, $d_2$, $N(d_1)$ e $N(d_2)$).
* Implementar a precificação de opções tanto analiticamente quanto via Simulação Monte Carlo, calculando a convergência e o erro padrão.

---

### Conceitos-Chave Explicados em Profundidade

#### O Payoff da Call Europeia
Para uma call europeia com preço de exercício (strike) $K$ e data de vencimento $T$, o valor do pagamento final (payoff) no vencimento $S_T$ é dado por:

$$(S_T - K)^+ = \max(S_T - K, 0)$$

A precificação consiste em determinar o valor justo presente (em $t=0$) desse fluxo de caixa futuro incerto.

#### A Medida Risco-Neutra $Q$ e a Ausência de Arbitragem
A estrutura de Black-Scholes estabelece que o preço de um payoff futuro é a sua expectativa descontada. No entanto, essa expectativa não é calculada sob a medida do mundo real (onde o ativo possui um drift $\mu$), mas sob uma medida de probabilidade especial: a **medida risco-neutra**, denotada por $Q$.

* **Por que a medida $Q$ é necessária?** Precisamos de uma medida na qual os preços descontados se comportem de forma "limpa" (como martingalas), garantindo que a precificação seja plenamente compatível com o princípio de ausência de arbitragem.
* **Ajuste de Drift:** A incerteza e o ruído do mercado, representados pela volatilidade $\sigma$, permanecem inalterados. No entanto, o drift real $\mu$ — que é inobservável e inútil para a precificação — é substituído pela taxa livre de risco $r$.
* **Escolha da Unidade de Medida:** Definir que "o drift se torna $r$" equivale a escolher a conta de caixa (*cash account*) como a unidade de medida do sistema. Com isso, os preços descontados passam a ser martingalas sob a medida $Q$ associada.

#### Dinâmica do Ativo sob a Medida $Q$
Sob a medida risco-neutra $Q$, a dinâmica do preço do ativo subjacente segue o seguinte GBM:

$$dS_t = r S_t \, dt + \sigma S_t \, dW_t, \qquad S_0 > 0$$

A regra central de precificação determina que o preço da call no tempo zero ($C_0$) é:

$$C_0 = e^{-rT} \mathbb{E}^Q \left[ (S_T - K)^+ \right]$$

O modelo de Black-Scholes é a combinação desse pacote: **GBM sob $Q$ + Expectativa Descontada + Payoff Europeu**.

---

### Intuição de Mercado e Trading

#### Precificação sem Opinião Direcional
Uma das conclusões mais profundas da precificação risco-neutra é que o preço de uma opção não depende das crenças do investidor sobre a tendência do mercado ($\mu$). 

* Se um trader acredita que a ação vai subir fortemente ($\mu = 50\%$) e outro acredita que vai cair ($\mu = -20\%$), **ambos devem concordar sobre o mesmo preço da opção**.
* O preço de uma opção não é uma previsão direcional; é o custo de uma **escrita de replicação** (*replication writing*), composta por uma posição no ativo subjacente menos um montante de caixa descontado.

#### O Papel das Variáveis na Fórmula
* **Taxa Livre de Risco ($r$):** Atua descontando o valor presente do strike por meio do termo $K e^{-rT}$. Além disso, entra nos termos $d_1$ e $d_2$, afetando a probabilidade risco-neutra de a opção terminar no dinheiro.
* **Volatilidade ($\sigma$):** Controla o grau de dispersão da distribuição de $S_T$. Como o payoff de uma call é uma função convexa ($\max(S_T - K, 0)$), um aumento na dispersão eleva o valor esperado do payoff, tornando a call mais valiosa.

---

### Derivação Matemática Passo a Passo

#### Transformação para o Log-Preço via Lema de Itô
Para simplificar o GBM multiplicativo em uma relação linear, define-se a variável $X_t$:

$$X_t = \ln(S_t)$$

Considerando a função $f(S) = \ln(S)$, calcula-se as suas derivadas de primeira e segunda ordem:

$$f'(S) = \frac{1}{S}, \qquad f''(S) = -\frac{1}{S^2}$$

Pelo Lema de Itô, a regra de expansão estocástica é:

$$dX_t = f'(S_t) dS_t + \frac{1}{2} f''(S_t) (dS_t)^2$$

Substituindo $dS_t = r S_t dt + \sigma S_t dW_t$ e aplicando a identidade fundamental do cálculo estocástico $(dW_t)^2 = dt$:

$$(dS_t)^2 = (\sigma S_t dW_t)^2 = \sigma^2 S_t^2 dt$$

Substituindo os termos na expansão de Itô:

$$dX_t = \frac{1}{S_t} \left( r S_t dt + \sigma S_t dW_t \right) + \frac{1}{2} \left( -\frac{1}{S_t^2} \right) \left( \sigma^2 S_t^2 dt \right)$$

$$dX_t = \left( r - \frac{1}{2}\sigma^2 \right) dt + \sigma dW_t$$

Assim, os parâmetros de drift ($\tilde{\mu}$) e difusão ($\tilde{\sigma}$) do log-preço sob $Q$ são:

$$\tilde{\mu} = r - \frac{1}{2}\sigma^2, \qquad \tilde{\sigma} = \sigma$$

#### Distribuição Terminal de $S_T$
Integrando a equação no intervalo $t \in [0, T]$:

$$X_T = X_0 + \left( r - \frac{1}{2}\sigma^2 \right) T + \sigma W_T$$

onde $X_0 = \ln(S_0)$. Sabendo que $W_T \sim \mathcal{N}(0, T)$, conclui-se que:

$$\ln(S_T) \sim \mathcal{N} \left( \ln(S_0) + \left( r - \frac{1}{2}\sigma^2 \right) T, \ \sigma^2 T \right)$$

Isso demonstra rigorosamente que $S_T$ segue uma distribuição **log-normal** sob a medida $Q$.

#### A Fórmula Fechada de Black-Scholes
Avaliando a expectativa descontada $C_0 = e^{-rT} \mathbb{E}^Q [(S_T - K)^+]$ sob a distribuição log-normal, obtém-se a solução analítica fechada:

$$C_0 = S_0 N(d_1) - K e^{-rT} N(d_2)$$

Onde $N(\cdot)$ representa a função de distribuição acumulada (CDF) da normal padrão, e:

$$d_1 = \frac{\ln(S_0 / K) + \left( r + \frac{1}{2}\sigma^2 \right) T}{\sigma \sqrt{T}}$$

$$d_2 = d_1 - \sigma \sqrt{T}$$

#### Interpretação Direta dos Termos
* $N(d_2) = \mathbb{P}^Q(S_T > K)$: Probabilidade sob a medida risco-neutra $Q$ de a opção terminar no dinheiro (*in the money*).
* $N(d_1) = \Delta_{\text{call}}$: O Delta da call em Black-Scholes, representando a sensibilidade do preço da opção em relação ao preço do ativo subjacente.

---

### Exemplo Numérico Resolvido Passo a Passo

#### Cenário
Considere uma opção de compra europeia com os seguintes parâmetros:
* Preço inicial do ativo ($S_0$): $\$100,00$
* Preço de exercício ($K$): $\$100,00$
* Taxa livre de risco ($r$): $5\%$ ao ano ($0,05$)
* Volatilidade ($\sigma$): $20\%$ ao ano ($0,20$)
* Tempo até o vencimento ($T$): $1,0$ ano

#### Passo 1 Calcular $\ln(S_0 / K)$
$$\ln(100 / 100) = \ln(1) = 0$$

#### Passo 2 Calcular $d_1$
$$d_1 = \frac{0 + \left( 0,05 + \frac{1}{2} (0,20)^2 \right) \times 1,0}{0,20 \times \sqrt{1,0}}$$

$$d_1 = \frac{0,05 + 0,02}{0,20} = \frac{0,07}{0,20} = 0,35$$

#### Passo 3 Calcular $d_2$
$$d_2 = d_1 - \sigma \sqrt{T} = 0,35 - 0,20 \times 1,0 = 0,15$$

#### Passo 4 Consultar a CDF da Normal Padrão $N(\cdot)$
* $N(d_1) = N(0,35) \approx 0,6368$ (Delta da call)
* $N(d_2) = N(0,15) \approx 0,5596$ (Probabilidade risco-neutra de término *in the money*)

#### Passo 5 Calcular o Valor Presente do Strike
$$K e^{-rT} = 100 \times e^{-0,05 \times 1,0} \approx 100 \times 0,95123 = 95,123$$

#### Passo 6 Aplicar a Fórmula de Black-Scholes
$$C_0 = S_0 N(d_1) - K e^{-rT} N(d_2)$$

$$C_0 = (100 \times 0,6368) - (95,123 \times 0,5596)$$

$$C_0 = 63,68 - 53,231 = 10,449 \approx \$10,45$$

---

### Armadilhas Comuns e Erros de Interpretação

1. **Incluir o Drift Real ($\mu$) na Precificação:**
   * *Erro:* Tentar ajustar o preço da opção porque o mercado está em tendência de alta ($\mu > r$).
   * *Correção:* O preço de arbitragem depende apenas do custo de replicação do risco ($\sigma$) e do custo de financiamento ($r$). O parâmetro $\mu$ é irrelevante.

2. **Confundir $N(d_2)$ com a Probabilidade do Mundo Real:**
   * *Erro:* Afirmar que $N(d_2)$ é a probabilidade real do mercado de a ação fechar acima de $K$.
   * *Correção:* $N(d_2)$ é estritamente a probabilidade sob a medida hipotética risco-neutra $Q$.

3. **Esquecer o Ajuste de Convexidade na Simulação do Log-Preço:**
   * *Erro:* Usar $r$ diretamente no drift do log-preço ao simular a lei terminal.
   * *Correção:* Devido ao Lema de Itô, o drift do log-preço é $\left(r - \frac{1}{2}\sigma^2\right)$, e não apenas $r$.

---

### Laboratório Prático em Python

Este roteiro descreve a implementação computacional para comparar a fórmula analítica de Black-Scholes com a precificação via Simulação Monte Carlo sob a medida $Q$.

#### Roteiro de Implementação

1. **Definição de Parâmetros de Entrada:**
   * Configurar as variáveis do problema: $S_0$, $K$, $r$, $\sigma$, $T$ e o número de simulações $N$ (ex: $N = 1.000.000$).

2. **Cálculo Analítico (Black-Scholes):**
   * Importar `scipy.stats.norm`.
   * Computar $d_1 = \frac{\ln(S_0 / K) + (r + 0.5 \sigma^2) T}{\sigma \sqrt{T}}$ e $d_2 = d_1 - \sigma \sqrt{T}$.
   * Calcular o preço analítico $C_0 = S_0 N(d_1) - K e^{-rT} N(d_2)$.

3. **Simulação Monte Carlo da Lei Terminal sob $Q$:**
   * Gerar um vetor de $N$ variáveis aleatórias normais padrão $Z \sim \mathcal{N}(0, 1)$.
   * Amostrar o valor terminal do ativo diretamente pela fórmula exata:
     $$S_T = S_0 \exp\left( \left( r - \frac{1}{2}\sigma^2 \right) T + \sigma \sqrt{T} Z \right)$$

4. **Cálculo do Estimador e Erro Padrão:**
   * Calcular o vetor de payoffs no vencimento: $\text{payoff} = \max(S_T - K, 0)$.
   * Descontar os payoffs para o valor presente: $V_{MC} = e^{-rT} \times \text{payoff}$.
   * Calcular a média amostral para obter o estimador Monte Carlo:
     $$\widehat{C}_{MC} = \frac{1}{N} \sum_{i=1}^N V_{MC}^{(i)}$$
   * Calcular o erro padrão ($SE$) da estimativa:
     $$SE = \frac{\operatorname{Std}(V_{MC})}{\sqrt{N}}$$

5. **Validação:**
   * Verificar se o intervalo $[\widehat{C}_{MC} - 1,96 \times SE, \ \widehat{C}_{MC} + 1,96 \times SE]$ contém o preço exato de Black-Scholes, observando a convergência na ordem de $1/\sqrt{N}$.

---

### Glossário de Termos

* **Medida Risco-Neutra ($Q$):** Medida de probabilidade sob a qual o preço descontado de qualquer ativo negociado é um martingala, equivalente à ausência de oportunidades de arbitragem.
* **Martingala:** Processo estocástico cujo valor esperado futuro, dado todo o histórico até o presente, é igual ao seu valor atual.
* **Conta de Caixa (*Cash Account*):** Ativo livre de risco que cresce à taxa $r$, utilizado como numeraire (unidade de medida) para tornar os preços descontados martingalas sob $Q$.
* **Delta da Call ($\Delta_{\text{call}}$):** Primeira derivada do preço da call em relação ao preço do subjacente ($N(d_1)$), indicando a quantidade do ativo necessária para replicar a opção.
* **Ajuste de Convexidade ($-\frac{1}{2}\sigma^2$):** Termo decorrente do Lema de Itô que reduz o drift do log-preço para compensar a não-linearidade da função exponencial.
* **Erro Padrão ($SE$):** Medida da incerteza estatística da estimativa de Monte Carlo, calculada como o desvio padrão dos payoffs descontados dividido pela raiz quadrada do número de simulações ($N$).

---

### Exercícios e Questões de Fixação

#### Nível 1 Básico (Resposta Curta)

**Questão 1.1:**
Na fórmula de Black-Scholes, por que a taxa de retorno esperada do mercado ($\mu$) não é utilizada no cálculo do preço da opção?
* **Resposta:** Porque a precificação de opções é baseada no princípio da ausência de arbitragem e na replicação de carteiras. A precificação é realizada sob a medida risco-neutra $Q$, na qual todo o risco direcional é coberto e o drift do ativo é substituído pela taxa livre de risco $r$.

**Questão 1.2:**
Qual é o papel da volatilidade ($\sigma$) no preço de uma opção de compra europeia?
* **Resposta:** A volatilidade controla a dispersão dos preços do subjacente no vencimento ($S_T$). Como a função de payoff da call é convexa, uma maior dispersão aumenta a expectativa do payoff sob $Q$, elevando o valor da opção.

---

#### Nível 2 Intermediário (Aplicação e Análise)

**Questão 2.1:**
Explique o significado financeiro e probabilístico dos termos $N(d_1)$ e $N(d_2)$ na fórmula de Black-Scholes.
* **Resposta:**
  * $N(d_2)$ é a probabilidade sob a medida risco-neutra $Q$ de a opção terminar no dinheiro, ou seja, $\mathbb{P}^Q(S_T > K)$.
  * $N(d_1)$ representa o Delta da call ($\Delta_{\text{call}}$), que determina a quantidade do ativo subjacente $S_0$ necessária para construir uma carteira de replicação coberta.

**Questão 2.2:**
Por que a simulação de Monte Carlo para a precificação de opções sob $Q$ utiliza o drift $\left(r - \frac{1}{2}\sigma^2\right)$ na equação do log-preço em vez de apenas $r$?
* **Resposta:** O termo $-\frac{1}{2}\sigma^2$ é o ajuste de convexidade resultante da aplicação do Lema de Itô à função não-linear $X_t = \ln(S_t)$. Ele garante que a expectativa do preço em nível $\mathbb{E}^Q[S_T]$ cresça exatamente à taxa livre de risco $r$, mantendo a propriedade de martingala do preço descontado.

---

#### Nível 3 Avançado (Dissertativo)

**Questão 3.1:**
Demonstre como a aplicação do Lema de Itô na transformação $X_t = \ln(S_t)$ permite passar da SDE do GBM sob $Q$ para a distribuição explícita do preço terminal $S_T$. Em seguida, descreva como esse resultado possibilita a precificação via Monte Carlo com amostragem direta (sem necessidade de discretização de passos intermediários de tempo).

* **Resposta:**
  A SDE do ativo subjacente sob a medida risco-neutra $Q$ é dada por $dS_t = r S_t dt + \sigma S_t dW_t$. Aplicando a função $f(S) = \ln(S)$ e expandindo pelo Lema de Itô:
  $$dX_t = f'(S_t) dS_t + \frac{1}{2} f''(S_t) (dS_t)^2$$
  Sabendo que $f'(S) = 1/S$, $f''(S) = -1/S^2$ e $(dS_t)^2 = \sigma^2 S_t^2 dt$, a substituição resulta em:
  $$dX_t = \left( r - \frac{1}{2}\sigma^2 \right) dt + \sigma dW_t$$
  Como os coeficientes desta SDE para $X_t$ são constantes, a integração direta entre $0$ e $T$ fornece:
  $$X_T = \ln(S_0) + \left( r - \frac{1}{2}\sigma^2 \right) T + \sigma W_T$$
  Como $W_T \sim \mathcal{N}(0, T)$, podemos reescrever $W_T = \sqrt{T} Z$, onde $Z \sim \mathcal{N}(0, 1)$. Aplicando a função exponencial em ambos os lados, obtemos a lei terminal exata de $S_T$:
  $$S_T = S_0 \exp\left( \left( r - \frac{1}{2}\sigma^2 \right) T + \sigma \sqrt{T} Z \right)$$
  Essa solução analítica exata permite gerar simulações de Monte Carlo amostrando $S_T$ diretamente em um único passo de tempo $T$, utilizando variáveis normais padrão $Z$. Isso elimina qualquer erro de discretização temporal e permite estimar o preço descontado $C_0 = e^{-rT} \frac{1}{N} \sum \max(S_T^{(i)} - K, 0)$ com um erro padrão convergindo a uma taxa de $\mathcal{O}(1/\sqrt{N})$.