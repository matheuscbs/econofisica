<!-- imported study note (guia-completo.md) -->
# Guia Completo do Módulo M01: Fundamentos de Precificação de Opções e Dinâmica de Hedge

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M01

↑ M01 · Resumo · Completo

---

## Sumário Executivo

Este documento estabelece a fundamentação teórica, matemática e operacional para a precificação de derivativos financeiros e a gestão de risco através do hedge dinâmico em tempo contínuo e discreto. A teoria moderna de apreçamento de ativos baseia-se na replicação perfeita e na ausência de oportunidades de arbitragem, modelando os preços dos ativos subjacentes como equações diferenciais estocásticas (EDEs) impulsionadas pelo movimento Browniano.

No entanto, a implementação prática do hedge delta em mercados reais enfrenta importantes fricções de mercado:
* A necessidade de rebalanceamento em intervalos discretos de tempo ($\Delta t > 0$), gerando um erro estocástico de discretização assintoticamente proporcional a $O(\sqrt{\Delta t})$.
* A presença de custos de transação proporcionais, que fazem com que o custo total de rebalanceamento contínuo divirja para o infinito.
* A incerteza e má especificação de parâmetros, em particular o erro de previsão da volatilidade futura e a presença de dinâmicas estocásticas de volatilidade do tipo GARCH(1,1).

Através da integração do Lema de Itô, do Teorema de Girsanov, do Teorema Fundamental do Apreço de Ativos e de expansões de erro de replicação (Boyle-Emanuel, Leland, Mykland e Hayashi), este guia detalha a transição do modelo ideal de Black-Scholes para estratégias operacionais ajustadas às imperfeições do mercado.

---

## 1. Opção como Transferência de Risco e Convexidade

Um contrato de derivativo financeiro $V(t, S_t)$ representa um direito cujo valor no vencimento $T$ depende da trajetória ou do estado terminal do preço do ativo subjacente $S_t$. Sob a perspectiva de engenharia financeira, as opções operam essencialmente como instrumentos de transferência de risco entre agentes econômicos.

A característica fundamental que diferencia uma opção de um contrato a termo ou contrato futuro é a **convexidade** da sua função de *payoff* em relação ao preço do ativo subjacente:
* Para uma opção de compra (*European call*), o *payoff* terminal é dado por $C(S_T, T) = \max(S_T - K, 0)$, onde $K$ é o preço de exercício (*strike*).
* Para uma opção de venda (*European put*), o *payoff* terminal é $P(S_T, T) = \max(K - S_T, 0)$.

A não-linearidade do *payoff* exige que a função de valor $V(t, S_t) \in C^{1,2}([0, T] \times \mathbb{R}^+)$ seja continuamente diferenciável uma vez em relação ao tempo $t$ e duas vezes em relação ao preço do ativo $S_t$. A convexidade do derivativo é quantificada pela sua segunda derivada espacial, o **Gamma** ($\Gamma = \frac{\partial^2 V}{\partial S^2}$). 

A convexidade positiva ($\Gamma > 0$) implica que a taxa de variação do valor do derivativo em relação ao ativo subjacente (o **Delta**, $\Delta = \frac{\partial V}{\partial S}$) aumenta à medida que o preço do ativo sobe e diminui à medida que o preço cai. Esse comportamento cria uma assimetria no perfil de retorno: o comprador do derivativo adquire proteção contra variações desfavoráveis do ativo subjacente, enquanto mantém participação em variações favoráveis. A transferência dessa exposição assimétrica exige o pagamento de um prêmio, o qual reflete o custo de replicação estocástica da convexidade ao longo da vida da opção.

---

## 2. Dinâmica GBM Mínima, Log-Preço, Distribuição Log-Normal e Momentos

Para modelar o comportamento contínuo dos preços dos ativos em ambientes estocásticos não-determinísticos, assume-se um espaço de probabilidade filtrado $(\Omega, \mathcal{F}, (\mathcal{F}_t)_{t \ge 0}, P)$ que satisfaz as condições habituais, onde $P$ representa a medida de probabilidade física (real).

A dinâmica padrão do preço do ativo subjacente $S_t$ é descrita por um Movimento Browniano Geométrico (GBM):

$$dS_t = \mu S_t dt + \sigma S_t dW_t^P$$

onde:
* $\mu \in \mathbb{R}$ é a taxa de retorno esperada instantânea (*drift*).
* $\sigma > 0$ é o coeficiente de volatilidade constante.
* $W_t^P$ é um movimento Browniano padrão sob a medida física $P$.

A conta do mercado monetário (*money market account*) $B_t$ evolui deterministicamente sob uma taxa de juros livre de risco constante $r \ge 0$:

$$dB_t = r B_t dt \implies B_t = B_0 e^{rt}$$

### Dinâmica do Log-Preço e Distribuição Log-Normal

Para derivar a distribuição exata do preço do ativo $S_T$ em qualquer instante futuro $T > t$, define-se a função do log-preço $x_t = f(S_t) = \ln S_t$. Aplicando o Lema de Itô a $f(S_t)$:

$$\frac{df}{dS} = \frac{1}{S_t}, \quad \frac{d^2f}{dS^2} = -\frac{1}{S_t^2}$$

$$d(\ln S_t) = \frac{1}{S_t} dS_t + \frac{1}{2} \left(-\frac{1}{S_t^2}\right) (dS_t)^2$$

Como $(dS_t)^2 = \sigma^2 S_t^2 dt$, a EDE do log-preço torna-se:

$$d(\ln S_t) = \left( \mu - \frac{1}{2} \sigma^2 \right) dt + \sigma dW_t^P$$

Integrando a equação de $t$ a $T$:

$$\ln S_T = \ln S_t + \left( \mu - \frac{1}{2} \sigma^2 \right) (T - t) + \sigma (W_T^P - W_t^P)$$

Dado que $(W_T^P - W_t^P) \sim \mathcal{N}(0, T - t)$, o log-preço no vencimento é normalmente distribuído:

$$\ln\left(\frac{S_T}{S_t}\right) \sim \mathcal{N}\left( \left( \mu - \frac{1}{2} \sigma^2 \right) (T - t), \sigma^2 (T - t) \right)$$

Consequentemente, o preço do ativo $S_T$ possui uma **distribuição log-normal** sob a medida física $P$.

### Momentos da Distribuição

Utilizando a função geradora de momentos da distribuição normal, os momentos do preço do ativo sob $P$ são expressos por:

$$\mathbb{E}^P [S_T \mid \mathcal{F}_t] = S_t e^{\mu (T - t)}$$

$$\operatorname{Var}^P [S_T \mid \mathcal{F}_t] = S_t^2 e^{2\mu (T - t)} \left( e^{\sigma^2 (T - t)} - 1 \right)$$

---

## 3. Limites de No-Arbitrage e Put-Call Parity

Antes de impor premissas distributivas específicas, os preços dos derivativos devem respeitar limites universais independentes de modelo, ditados exclusivamente pelos princípios de dominância de portfólio e não-arbitragem estática.

### Limites Livres de Modelo (*Model-Free Bounds*)

Para um ativo subjacente com preço não-negativo $S_t$, os preços de uma Call Europeia $C_t$ e de uma Put Europeia $P_t$, ambas com preço de exercício $K$ e vencimento $T$, estão sujeitos aos seguintes limites:

$$\max\left(0, S_t - K e^{-r(T-t)}\right) \le C_t \le S_t$$

$$\max\left(0, K e^{-r(T-t)} - S_t\right) \le P_t \le K e^{-r(T-t)}$$

#### Prova da Fronteira Inferior da Call via Dominância de Portfólio
Considere o Portfólio A, composto por uma opção de compra $C_t$ e $K e^{-r(T-t)}$ aplicados em títulos de cupom zero com valor de face $K$ no vencimento $T$. Considere o Portfólio B, composto por uma ação $S_t$.

No vencimento $T$:
* **Portfólio A:** $\max(S_T - K, 0) + K = \max(S_T, K)$
* **Portfólio B:** $S_T$

Como $\max(S_T, K) \ge S_T$ em todos os estados da natureza no instante $T$, o Portfólio A domina o Portfólio B. Para evitar arbitragem no instante $t$, o custo inicial do Portfólio A deve ser maior ou igual ao custo do Portfólio B:

$$C_t + K e^{-r(T-t)} \ge S_t \implies C_t \ge S_t - K e^{-r(T-t)}$$

Dado que uma opção possui responsabilidade limitada ($C_t \ge 0$), obtém-se o limite inferior $\max\left(0, S_t - K e^{-r(T-t)}\right)$.

### Paridade Call-Put (*Put-Call Parity*)

A Paridade Call-Put estabelece uma relação de equivalência estática entre uma Call e uma Put europeias com mesmo *strike* $K$ e vencimento $T$.

Considere a construção de dois portfólios no instante $t$:
* **Portfólio 1:** 1 Call Europeia ($C_t$) + Título livre de risco pagando $K$ em $T$ (valor presente $K e^{-r(T-t)}$).
* **Portfólio 2:** 1 Put Europeia ($P_t$) + 1 Ação subjacente ($S_t$).

Evaluating os *payoffs* terminais no instante $T$:

| Condição de Estado Terminal | *Payoff* do Portfólio 1 ($\text{Call} + \text{Título}$) | *Payoff* do Portfólio 2 ($\text{Put} + \text{Ação}$) |
| :--- | :--- | :--- |
| **Estado 1:** $S_T > K$ | $(S_T - K) + K = S_T$ | $0 + S_T = S_T$ |
| **Estado 2:** $S_T \le K$ | $0 + K = K$ | $(K - S_T) + S_T = K$ |

Como os *payoffs* de ambos os portfólios são idênticos a $\max(S_T, K)$ em todos os estados no vencimento, a ausência de arbitragem exige custos iniciais idênticos no instante $t$:

$$C_t + K e^{-r(T-t)} = P_t + S_t \implies C_t - P_t = S_t - K e^{-r(T-t)}$$

#### Ajustes para Dividendos e Opções Americanas
1. **Rendimento de Dividendos Contínuos ($q$):** Se o ativo pagar dividendos a uma taxa contínua $q \ge 0$, a retenção da ação exige desconto na posição acionária:

$$C_t - P_t = S_t e^{-q(T-t)} - K e^{-r(T-t)}$$

2. **Opções Americanas ($C_t^A, P_t^A$):** Para ações sem dividendos, o exercício antecipado de uma Call Americana é estritamente sub-ótimo, de modo que $C_t^A = C_t$. Para Puts Americanas, o exercício antecipado pode ser ótimo quando a opção está profundamente "no dinheiro" (*deep in the money*), transformando a igualdade em uma banda de desigualdade:

$$S_t - K \le C_t^A - P_t^A \le S_t - K e^{-r(T-t)}$$

---

## 4. Delta Neutro, Controlador de Rebalanceamento, Bandas e Custos de Transação

A replicação teórica perfeita do modelo de Black-Scholes assume negociação contínua sem custos. Contudo, a presença de custos de transação proporcionais ao valor negociado $k |\Delta \theta_t| S_t$ (onde $k > 0$ é a taxa de custo e $\Delta \theta_t$ é a variação na quantidade de ações) faria com que o custo acumulado de um rebalanceamento contínuo divergisse para o infinito.

### Modelo de Volatilidade Modificada de Leland (1985)

Leland propôs ajustar a volatilidade utilizada no apreçamento e no cálculo do delta para absorver os custos de transação esperados dentro do prêmio da opção. Para um intervalo de rebalanceamento discreto fixo $\Delta t$, a volatilidade aumentada $\hat{\sigma}$ é definida por:

$$\hat{\sigma}^2 = \sigma^2 \left( 1 + \sqrt{\frac{2}{\pi}} \frac{k}{\sigma \sqrt{\Delta t}} \right)$$

Para posições compradas em convexidade (opções com Gamma positivo, $C_{SS} > 0$), a volatilidade ajustada é superior à volatilidade do ativo ($\hat{\sigma} > \sigma$), o que eleva o preço de compra da opção para cobrir os custos operacionais do hedge. A EDP de Black-Scholes ajustada sob o modelo de Leland assume a forma:

$$\frac{\partial \hat{C}}{\partial t} + r S \frac{\partial \hat{C}}{\partial S} + \frac{1}{2} \hat{\sigma}^2 S^2 \frac{\partial^2 \hat{C}}{\partial S^2} - r \hat{C} = 0$$

#### Inconsistência Assintótica de Leland (Kabanov e Safarian, 1997)
Kabanov e Safarian demonstraram rigorosamente que a estratégia de Leland falha em convergir para o *payoff* da opção quando o intervalo de rebalanceamento tende a zero ($\Delta t \to 0$). À medida que a frequência de negociação aumenta, os custos de transação crescem a uma taxa superior à acumulação do prêmio de volatilidade aumentada $\hat{\sigma}$, fazendo com que o erro de replicação não convirja para zero.

### Controlador por Bandas de Não-Transação (Hodges-Neuberger)

Para suprimir a frequência excessiva de rebalanceamento, os modelos de controle ótimo baseados em utilidade (como o modelo de Hodges-Neuberger sob utilidade CARA, $U(w) = -e^{-\lambda w}$) estabelecem bandas de não-transação $(\Delta_t^{lower}, \Delta_t^{upper})$ ao redor do Delta teórico.

```
       Ação / Delta
         ^
         |      /  Banda Superior: \Delta_t^{upper}
         |     /   ---------------------------------
         |    /    Delta Teórico: \Delta_t = \partial V / \partial S
         |   /     ---------------------------------
         |  /      Banda Inferior: \Delta_t^{lower}
         | /
         +--------------------------------------------> Tempo (t)
```

O operador executa ordens de rebalanceamento apenas quando a variação do preço do ativo força o Delta a ultrapassar as fronteiras da banda de controle:
1. Se $\Delta_t > \Delta_t^{upper}$, vende-se o excedente para retornar o hedge à borda superior.
2. Se $\Delta_t < \Delta_t^{lower}$, compra-se o necessário para retornar o hedge à borda inferior.
3. Dentro da banda $[\Delta_t^{lower}, \Delta_t^{upper}]$, nenhuma operação é realizada, reduzindo radicalmente o atrito de custos enquanto delimita o risco de Gamma.

---

## 5. Lema de Itô, Termo de Variância, Gamma e Convexidade, P&L Gamma-Theta

A variação quadrática do movimento Browniano ($\langle W, W \rangle_t = t$ ou informalmente $(dW_t)^2 = dt$) exige a expansão em série de Taylor de segunda ordem para avaliar funções estocásticas.

### Expansão via Lema de Itô

Seja $V(t, S_t)$ uma função de classe $C^{1,2}$. O diferencial estocástico $dV(t, S_t)$ sob a medida física $P$ é expresso por:

$$dV(t, S_t) = \frac{\partial V}{\partial t} dt + \frac{\partial V}{\partial S} dS_t + \frac{1}{2} \frac{\partial^2 V}{\partial S^2} (dS_t)^2$$

Substituindo $dS_t = \mu S_t dt + \sigma S_t dW_t^P$ e retendo os termos de ordem até $dt$:

$$(dS_t)^2 = (\mu S_t dt + \sigma S_t dW_t^P)^2 = \sigma^2 S_t^2 dt + O(dt^{3/2})$$

$$dV(t, S_t) = \left( \frac{\partial V}{\partial t} + \mu S_t \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S_t^2 \frac{\partial^2 V}{\partial S^2} \right) dt + \sigma S_t \frac{\partial V}{\partial S} dW_t^P$$

### Dinâmica do P&L Gamma-Theta

Considere um portfólio delta-hedged composto por uma posição vendida na opção $V(t, S_t)$ e uma posição comprada em $\Delta_t = \frac{\partial V}{\partial S}$ ações subjacentes. A variação determinística do resultado do portfólio no intervalo $dt$ é ditada pelo compromisso entre o decaimento temporal (**Theta**, $\Theta = \frac{\partial V}{\partial t}$) e o ganho de convexidade (**Gamma**, $\Gamma = \frac{\partial^2 V}{\partial S^2}$).

Substituindo a EDP de Black-Scholes ($\Theta + r S \Delta + \frac{1}{2} \sigma^2 S^2 \Gamma - r V = 0$), obtém-se a relação fundamental de P&L instantâneo:

$$\Theta dt + \frac{1}{2} \sigma^2 S^2 \Gamma dt = r (V - \Delta S) dt$$

Assumindo taxa de juros nula ($r = 0$) para isolar o P&L de mercado:

$$\Theta = -\frac{1}{2} \sigma^2 S^2 \Gamma$$

Esta equação demonstra que a perda diária decorrente do decaimento temporal ($\Theta < 0$) equilibra exatamente o ganho esperado proveniente da variabilidade do preço do ativo ponderada pelo Gamma ($\Gamma > 0$). Se a volatilidade realizada do mercado suplantar a volatilidade precificada na opção, o retorno gerado pelas variações do ativo superará a perda de Theta, gerando P&L positivo para a carteira delta-neutra comprada em convexidade.

---

## 6. Portfólio Sem Risco, PDE de Black-Scholes, Medida Risco-Neutro, Teorema Fundamental e Fórmula Fechada

### Derivação do Portfólio Replicante e da EDP de Black-Scholes

Considere a construção de um portfólio auto-financiado $\Pi_t$ composto por uma posição vendida em um derivativo europeu $V(t, S_t)$ e uma posição comprada em $\Delta_t$ unidades do ativo subjacente $S_t$:

$$\Pi_t = -V(t, S_t) + \Delta_t S_t$$

A variação do valor do portfólio sobre um incremento infinitesimal $dt$ é dada por:

$$d\Pi_t = -dV(t, S_t) + \Delta_t dS_t$$

Substituindo a expansão de Itô de $dV(t, S_t)$:

$$d\Pi_t = -\left( \frac{\partial V}{\partial t} + \mu S_t \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S_t^2 \frac{\partial^2 V}{\partial S^2} \right) dt - \sigma S_t \frac{\partial V}{\partial S} dW_t^P + \Delta_t \left( \mu S_t dt + \sigma S_t dW_t^P \right)$$

Agrupando os termos determinísticos ($dt$) e estocásticos ($dW_t^P$):

$$d\Pi_t = \left( -\frac{\partial V}{\partial t} - \frac{1}{2} \sigma^2 S_t^2 \frac{\partial^2 V}{\partial S^2} + \left( \Delta_t - \frac{\partial V}{\partial S} \right) \mu S_t \right) dt + \left( \Delta_t - \frac{\partial V}{\partial S} \right) \sigma S_t dW_t^P$$

Para anular o risco estocástico impulsionado por $dW_t^P$, escolhe-se continuamente a razão de hedge:

$$\Delta_t = \frac{\partial V(t, S_t)}{\partial S}$$

Com $\Delta_t = \frac{\partial V}{\partial S}$, o termo estocástico extingue-se identicamente, tornando o portfólio localmente determinístico sobre $dt$. Pela lei do preço único e ausência de arbitragem, o retorno de um portfólio sem risco deve ser igual à taxa de juros livre de risco $r$:

$$d\Pi_t = r \Pi_t dt = r \left( -V + \frac{\partial V}{\partial S} S_t \right) dt$$

Igualando a variação determinística do portfólio ao retorno livre de risco:

$$-\frac{\partial V}{\partial t} - \frac{1}{2} \sigma^2 S_t^2 \frac{\partial^2 V}{\partial S^2} = r \left( -V + S_t \frac{\partial V}{\partial S} \right)$$

Reorganizando os termos, obtém-se a **Equação Diferencial Parcial de Black-Scholes**:

$$\frac{\partial V}{\partial t} + r S \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} - r V = 0$$

O parâmetro de retorno esperado do ativo subjacente sob a medida física ($\mu$) é completamente cancelado na etapa de neutralização do delta. Consequentemente, o valor justo do derivativo não depende das preferências de risco dos investidores ou da taxa de retorno esperada do ativo.

### Os Teoremas Fundamentais do Apreço de Ativos e Medidas Risco-Neutras

1. **Primeiro Teorema Fundamental do Apreço de Ativos:** Um modelo de mercado financeiro é livre de arbitragem se e somente se existe pelo menos uma medida de probabilidade $Q$ equivalente à medida física $P$ ($Q \sim P$) sob a qual todos os preços dos ativos descontados pela taxa livre de risco são martingales. As medidas $Q$ e $P$ são equivalentes se concordam sobre todos os eventos de probabilidade zero ($P(E) = 0 \iff Q(E) = 0$).

2. **Segundo Teorema Fundamental do Apreço de Ativos:** Um mercado livre de arbitragem é completo (isto é, qualquer claim contingente pode ser perfeitamente replicado por uma estratégia auto-financiada) se e somente se a medida martingale equivalente $Q$ for única.

#### Mudança de Medida via Teorema de Girsanov
A transição da medida física $P$ para a medida risco-neutra $Q$ altera o *drift* do ativo de $\mu$ para $r$. Define-se o processo do preço do risco do mercado por $\gamma_t = \frac{\mu - r}{\sigma}$. A densidade de Radon-Nikodym $Z_t = \frac{dQ}{dP}\Big|_{\mathcal{F}_t}$ é expressa como uma exponencial estocástica:

$$Z_t = \exp\left( -\int_0^t \gamma_u dW_u^P - \frac{1}{2} \int_0^t \gamma_u^2 du \right)$$

Pelo Teorema de Girsanov, o processo $W_t^Q$, definido por $dW_t^Q = dW_t^P + \left( \frac{\mu - r}{\sigma} \right) dt$, é um movimento Browniano padrão sob $Q$. A dinâmica do ativo subjacente sob $Q$ reduz-se a:

$$dS_t = r S_t dt + \sigma S_t dW_t^Q$$

Aplicando o Lema de Itô ao preço descontado $\tilde{S}_t = e^{-rt} S_t$:

$$d\tilde{S}_t = -r e^{-rt} S_t dt + e^{-rt} dS_t = \sigma \tilde{S}_t dW_t^Q$$

Como $d\tilde{S}_t$ possui *drift* nulo sob $Q$, o preço descontado é um $Q$-martingale. Pelo Teorema da Representação de Martingales e pela dualidade de Feynman-Kac, o valor de qualquer claim contingente $X = h(S_T)$ equivale à expectativa condicional de seu *payoff* terminal descontado avaliada sob $Q$:

$$V(t, S_t) = e^{-r(T-t)} \mathbb{E}^Q \left[ h(S_T) \mid \mathcal{F}_t \right]$$

### Fórmula Fechada para Call Europeia e Gregas

A solução analítica da EDP de Black-Scholes para uma opção de compra europeia com *strike* $K$ e vencimento $T$ é dada por:

$$C(S_t, t) = S_t N(d_1) - K e^{-r(T-t)} N(d_2)$$

onde $N(\cdot)$ representa a função de distribuição acumulada da normal padrão $\mathcal{N}(0,1)$, e os termos $d_1$ e $d_2$ são expressos por:

$$d_1 = \frac{\ln(S_t / K) + \left( r + \frac{1}{2} \sigma^2 \right)(T - t)}{\sigma \sqrt{T - t}}$$

$$d_2 = d_1 - \sigma \sqrt{T - t} = \frac{\ln(S_t / K) + \left( r - \frac{1}{2} \sigma^2 \right)(T - t)}{\sigma \sqrt{T - t}}$$

As sensibilidades de primeira e segunda ordem (**Gregas**) derivadas desta solução são:

* **Delta ($\Delta_C$):** $\frac{\partial C}{\partial S} = N(d_1)$
* **Gamma ($\Gamma_C$):** $\frac{\partial^2 C}{\partial S^2} = \frac{n(d_1)}{S \sigma \sqrt{T - t}}$
* **Theta ($\Theta_C$):** $\frac{\partial C}{\partial t} = -\frac{S n(d_1) \sigma}{2 \sqrt{T - t}} - r K e^{-r(T-t)} N(d_2)$
* **Vega ($\mathcal{V}_C$):** $\frac{\partial C}{\partial \sigma} = S \sqrt{T - t} \, n(d_1)$

onde $n(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2 / 2}$ denota a função densidade de probabilidade da normal padrão.

---

## 7. Erro de Hedge Discreto e com Vol Errada (Vol Implícita vs Realizada)

### Erro de Rebalanceamento Discreto (Framework Boyle-Emanuel e Hayashi-Mykland)

Quando o hedge delta é executado em intervalos de tempo discretos $\Delta t = T/N$, mantendo-se a posição fixada em $\Delta_{t_{i-1}}$ ao longo de cada subintervalo $[t_{i-1}, t_i]$, surge um erro de discretização não-hedgado.

Considerando taxa livre de risco nula ($r=0$), o incremento local do resultado de hedge $H(t_i)$ é expresso por:

$$H(t_i) = -\Delta C(t_i) + \left( \frac{\partial C(t_{i-1})}{\partial S} \right) \Delta S(t_i)$$

Expandindo $\Delta C(t_i)$ por Taylor de segunda ordem no espaço e primeira ordem no tempo, e aplicando a EDP de Black-Scholes ($\frac{\partial C}{\partial t} = -\frac{1}{2} \sigma^2 S^2 C_{SS}$):

$$H(t_i) = \frac{1}{2} C_{SS}(t_{i-1}) \sigma^2 S_{t_{i-1}}^2 \Delta t \left( 1 - u(t_i)^2 \right)$$

onde $u(t_i) \sim \mathcal{N}(0,1)$. Como $u(t_i)^2 \sim \chi_1^2$, temos $\mathbb{E}[u(t_i)^2] = 1$ e $\operatorname{Var}[u(t_i)^2] = 2$. Consequentemente, as propriedades estatísticas do erro local são:

$$\mathbb{E}[H(t_i)] = 0$$

$$\operatorname{Var}[H(t_i)] = \frac{1}{2} \left( C_{SS}(t_{i-1}) \sigma^2 S_{t_{i-1}}^2 \Delta t \right)^2$$

O erro terminal acumulado $HE(T) = \sum_{i=1}^N H(t_i)$ possui variância assintótica proporcional ao tamanho do passo $\Delta t$:

$$\operatorname{Var}[HE(T)] \xrightarrow{\Delta t \to 0} \frac{1}{2} \Delta t \int_0^T \left( C_{SS}(t, S_t) \sigma^2 S_t^2 \right)^2 dt$$

Pelo Teorema do Limite Central Funcional (Hayashi e Mykland, 2005), o erro de hedge padronizado converge fracamente para um martingale Gaussiano impulsionado por um movimento Browniano independente $W_t^*$:

$$\frac{HE(T)}{\sqrt{\Delta t}} \xrightarrow{d} \frac{1}{\sqrt{2}} \int_0^T C_{SS}(t, S_t) \sigma^2 S_t^2 dW_t^*$$

Isto estabelece formalmente que a escala de convergência do erro de discretização é de ordem $O(\sqrt{\Delta t})$.

### Erro por Má Especificação da Volatilidade (Delvar e Eta)

Se um operador executa o hedge utilizando uma volatilidade previstilizada $\sigma_F$ enquanto a volatilidade realizada do mercado evolui a $\sigma_R \neq \sigma_F$, o erro local $H(t_i)$ divide-se em um componente de viés de volatilidade $\delta(t_{i-1})$ e um ruído de discretização de Gamma $\gamma(t_{i-1})$:

$$H(t_i) = \delta(t_{i-1}) u(t_i) + \gamma(t_{i-1}) (1 - u(t_i)^2)$$

onde:

$$\delta(t_{i-1}) = \left( C_S^F(t_{i-1}) - C_S^R(t_{i-1}) \right) \sigma_R S_{t_{i-1}} \sqrt{\Delta t} \approx (\sigma_F - \sigma_R) \left( \frac{\partial C_S}{\partial \sigma} \right) \sigma_R S_{t_{i-1}} \sqrt{\Delta t}$$

$$\gamma(t_{i-1}) = \frac{1}{2} C_{SS}^F(t_{i-1}) \sigma_R^2 S_{t_{i-1}}^2 \Delta t$$

A derivada cruzada **Delvar** ($\frac{\partial^2 C}{\partial S \partial \sigma}$) governa a sensibilidade da razão de hedge à volatilidade:

$$\text{Delvar} = \frac{\partial C_S}{\partial \sigma} = -C_{SS} d_2 S \sqrt{T - t} = -\frac{n(d_1) d_2}{\sigma}$$

Para quantificar o impacto agregativo do erro de previsão de volatilidade sobre o desvio padrão do erro de hedge terminal, Anagnou-Basioudis e Hodges introduziram a grega não-linear **Eta ($\eta$)**:

$$\eta = \frac{\partial \operatorname{SD}(HE(T))}{\partial \sigma} = \sqrt{ \sum_{i=1}^N \left( \frac{\partial C_S(t_{i-1})}{\partial \sigma} \right)^2 \sigma_R^2 S_{t_{i-1}}^2 \Delta t }$$

Valores empíricos de $\eta$ comparativos obtidos na literatura para opções com $S_0 = 50, K = 50, T = 1, \sigma = 20\%$ e $N = 200$ rebalanceamentos:
* **Call Vanilla:** $\eta = 7,5073$ (Padronizado $\eta / \text{SD}(C_T) = 1,14$)
* **Call Média Geométrica (Asiática):** $\eta = 4,3834$ (Padronizado $\eta / \text{SD}(C_T) = 1,22$)
* **Call Up-and-Out com Barreira Exponencial:** $\eta = 23,683$

### Hedging Não-Paramétrico Baseado em Dados (*Data-Driven Strategy*)

Em ambientes sem especificação paramétrica, Hayashi e Mykland propuseram a estimação do hedge delta via regressão baseada na variação quadrática e covariação amostral observada:

$$\tilde{\theta}_{t_i}^n = \frac{\langle S, C \rangle_{t_i} - \langle S, C \rangle_{t_{i-1}}}{\langle S, S \rangle_{t_i} - \langle S, S \rangle_{t_{i-1}}}$$

O erro relativo resultante $L_2^n$ e o erro discreto do modelo verdadeiro $L_1^n$ convergem conjuntamente para processos Brownianos independentes $W^{*1}$ e $W^{*2}$:

$$\left(\sqrt{n} L_1^n, \sqrt{n} L_2^n\right) \xrightarrow{d} \left( \sqrt{\frac{T}{2}} \int_0^\cdot \|\bar{\theta}_u^{[1]}\| f_u dW_u^{*1}, \, \sqrt{\frac{T}{3}} \int_0^\cdot \|\bar{\theta}_u^{[1]}\| f_u dW_u^{*2} \right)$$

### Dinâmicas de Volatilidade Estocástica GARCH(1,1)

Sob a economia GARCH(1,1) de Duan (1995), o processo de retorno conticional é regido por:

$$\ln\left(\frac{S_t}{S_{t-1}}\right) = r + \lambda \sqrt{h_t} - 0,5 h_t + \epsilon_t, \quad \epsilon_t \mid \Phi_{t-1} \sim \mathcal{N}(0, h_t)$$

$$h_t = a_0 + a_1 \epsilon_{t-1}^2 + b_1 h_{t-1}$$

Sob a Medida de Avaliação Local Risco-Neutra (LRNV), a variância condicional ajustada torna-se:

$$h_t^* = a_0 + a_1 \left( \epsilon_{t-1}^* - \lambda \sqrt{h_{t-1}^*} \right)^2 + b_1 h_{t-1}^*$$

Estudos de simulação (Geyer e Schwaiger) indicam que quando o parâmetro de aversão ao risco $\lambda > 0$ (ex: $\lambda = 0,4$), ocorrem fortes divergências entre os preços teóricos GARCH e os custos médios de hedge de estratégias discretas, especialmente para opções fora do dinheiro (*out-of-the-money*).

---

## 8. Implementação em Python e Checklist Prático

### Módulo de Precificação, Gregas e Análise de Erros de Hedge

```python
import numpy as np
from scipy.stats import norm

class BlackScholesEngine:
    def __init__(self, S: float, K: float, T: float, r: float, sigma: float):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def d1_d2(self):
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return d1, d2

    def call_price(self) -> float:
        d1, d2 = self.d1_d2()
        return self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)

    def greeks(self) -> dict:
        d1, d2 = self.d1_d2()
        pdf_d1 = norm.pdf(d1)
        
        delta = norm.cdf(d1)
        gamma = pdf_d1 / (self.S * self.sigma * np.sqrt(self.T))
        theta = (- (self.S * pdf_d1 * self.sigma) / (2 * np.sqrt(self.T)) 
                 - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2))
        vega = self.S * np.sqrt(self.T) * pdf_d1
        delvar = - (pdf_d1 * d2) / self.sigma
        
        return {
            "Delta": delta,
            "Gamma": gamma,
            "Theta": theta,
            "Vega": vega,
            "Delvar": delvar
        }

    def leland_adjusted_vol(self, k: float, dt: float) -> float:
        """Calcula a volatilidade aumentada de Leland considerando custos de transacao k."""
        adjusted_var = (self.sigma ** 2) * (1.0 + np.sqrt(2.0 / np.pi) * (k / (self.sigma * np.sqrt(dt))))
        return np.sqrt(adjusted_var)

    @staticmethod
    def discrete_hedge_error_variance(gamma: float, sigma: float, S: float, dt: float, T: float) -> float:
        """Calcula a variancia assintotica do erro de hedge discreto (Boyle-Emanuel / Mykland)."""
        return 0.5 * dt * T * ((gamma * (sigma ** 2) * (S ** 2)) ** 2)

    @staticmethod
    def calculate_eta(delvar_array: np.ndarray, sigma_R: float, S_array: np.ndarray, dt: float) -> float:
        """Calcula a grega Eta para erros de previsao de volatilidade."""
        sum_terms = np.sum((delvar_array ** 2) * (sigma_R ** 2) * (S_array ** 2) * dt)
        return np.sqrt(sum_terms)

## Exemplo de Execucao Numerica
if __name__ == "__main__":
    bs = BlackScholesEngine(S=50.0, K=50.0, T=1.0, r=0.0, sigma=0.20)
    print(f"Preco da Call: {bs.call_price():.4f}")
    greeks = bs.greeks()
    for k, v in greeks.items():
        print(f"{k}: {v:.6f}")
        
    dt = 1.0 / 200.0  # 200 rebalanceamentos por ano
    leland_vol = bs.leland_adjusted_vol(k=0.01, dt=dt)
    print(f"Volatilidade Ajustada de Leland (k=1%): {leland_vol:.6f}")
    
    var_he = bs.discrete_hedge_error_variance(gamma=greeks["Gamma"], sigma=0.20, S=50.0, dt=dt, T=1.0)
    print(f"Variancia do Erro de Hedge Discreto: {var_he:.6f}")
```

### Checklist Prático para a Mesa de Operações

1. **Validação do Regime de Volatilidade:**
   * Comparar a volatilidade implícita do mercado ($\sigma_F$) com a volatilidade realizada do ativo ($\sigma_R$).
   * Calcular a exposição de Delvar ($\frac{\partial C_S}{\partial \sigma}$) e quantificar o índice Eta ($\eta$) do portfólio.
2. **Dimensionamento da Frequência de Rebalanceamento ($\Delta t$):**
   * Avaliar o *trade-off* entre o erro de discretização $O(\sqrt{\Delta t})$ e os custos de transação $k |\Delta \theta| S$.
   * Se os custos de transação forem significativos, migrar de rebalanceamento fixo por tempo para **bandas de não-transação por utilidade** ($\Delta_t^{lower}, \Delta_t^{upper}$).
3. **Gestão do Risco de Convexidade (Gamma-Theta):**
   * Monitorar o balanço diário entre decaimento temporal ($\Theta$) e ganho de volatilidade ($\frac{1}{2} \sigma^2 S^2 \Gamma$).
   * Estruturar hedges secundários com opções para neutralizar Vega e Gamma em posições onde o ativo subjacente exibe dinâmicas GARCH/estocásticas.

---

## 9. Tabela Comparativa dos Conceitos e Glossário

### Comparação dos Paradigmas de Precificação de Opções

| Paradigma de Precificação | Completação do Mercado | Dinâmica de Volatilidade Subjacente | Métrica de Governança / EDP | Desempenho do Hedge Dinâmico |
| :--- | :--- | :--- | :--- | :--- |
| **Black-Scholes Padrão** | Completo | Constante ($\sigma$) | $\frac{\partial V}{\partial t} + rS\frac{\partial V}{\partial S} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} - rV = 0$ | Replicação contínua perfeita; erro discreto escala em $O(\sqrt{\Delta t})$. |
| **Modelo de Custos de Leland** | Incompleto | Constante Ajustada ($\hat{\sigma}$) | $\hat{\sigma}^2 = \sigma^2 \left( 1 + \sqrt{\frac{2}{\pi}}\frac{k}{\sigma\sqrt{\Delta t}}\right)$ | Compensa custos via prêmio; falha em convergir para o *payoff* quando $\Delta t \to 0$. |
| **Controle Ótimo por Utilidade** | Incompleto | Constante ou Estocástica | $\max E[U(W_T)]$ via EDP de Hamilton-Jacobi-Bellman | Hedge executado dentro de bandas de controle ótimo; domina o modelo de Leland. |
| **GARCH / Risco-Neutro Local (LRNV)** | Incompleto | Condicional Variante no Tempo ($h_t$) | $C_t = e^{-r(T-t)} \mathbb{E}^Q [\max(S_T^* - K, 0)]$ via Monte Carlo | Exige rastreamento de trajetórias de variância condicional; deixa exposição a Vega. |

### Mapeamento Quantitativo de Fricções de Hedge e Sensitividades

| Fonte de Fricção | Impacto Quantitativo no Erro | Fórmula Matemática / Métrica | Principal Grega Afetada | Mecanismo de Mitigação |
| :--- | :--- | :--- | :--- | :--- |
| **Rebalanceamento Discreto** | Variância no P&L terminal | $\operatorname{Var}[HE(T)] \approx \frac{1}{2}\Delta t \int_0^T (C_{SS} \sigma^2 S^2)^2 dt$ | Gamma ($\Gamma = C_{SS}$) | Aumentar frequência $N$; executar hedge Gamma-neutro. |
| **Fricções de Transação** | *Drag* no portfólio; custo infinito se $\Delta t \to 0$ | $\text{Custo} = k \left \| \Delta \theta_t \right \| S_t$ | Delta ($\Delta$) / Frequência | Adotar bandas de não-transação de Hodges-Neuberger. |
| **Erro de Previsão de Volatilidade** | Viés direcional sistemático | $\delta(t_{i-1}) \approx (\sigma_F - \sigma_R) \left( \frac{\partial C_S}{\partial \sigma} \right) \sigma_R S \sqrt{\Delta t}$ | Delvar ($\frac{\partial C_S}{\partial \sigma} = -C_{SS} d_2 S \sqrt{T-t}$) | Recalibrar superfície continuamente; hedge Vega-neutro. |
| **Dinâmicas de Volatilidade / Caudas Longas** | Desalinhamento da razão de hedge | $h_t = a_0 + a_1 \epsilon_{t-1}^2 + b_1 h_{t-1}$ | Vega ($\mathcal{V}$) / Vol-Gamma | Utilizar aproximações de Monte Carlo GARCH ou volatilidade estocástica. |

### Glossário de Termos Técnicos

* **Movimento Browniano Geométrico (GBM):** Processo estocástico contínuo em que o logaritmo da variável segue um passeio aleatório com *drift*, garantindo preços estritamente positivos.
* **Lema de Itô:** Teorema fundamental do cálculo estocástico que fornece a expansão em série de Taylor de segunda ordem para funções de processos de difusão.
* **Medida Risco-Neutra ($Q$):** Medida de probabilidade equivalente à medida real sob a qual o preço descontado de todos os ativos é um martingale, eliminando a dependência do *drift* físico $\mu$.
* **Teorema de Girsanov:** Resultado matemático que define a mudança de medida de probabilidade e a alteração do termo de *drift* de um processo estocástico sem alterar seu termo de difusão.
* **Delta ($\Delta$):** Primeira derivada parcial do preço da opção em relação ao preço do ativo subjacente ($\frac{\partial V}{\partial S}$).
* **Gamma ($\Gamma$):** Segunda derivada parcial do preço da opção em relação ao preço do ativo subjacente ($\frac{\partial^2 V}{\partial S^2}$), medindo a convexidade do preço.
* **Theta ($\Theta$):** Derivada parcial do preço da opção em relação ao tempo ($\frac{\partial V}{\partial t}$), representando a taxa de decaimento temporal.
* **Vega ($\mathcal{V}$):** Sensibilidade do preço da opção em relação a alterações na volatilidade do ativo subjacente ($\frac{\partial V}{\partial \sigma}$).
* **Delvar (Ddeltadvol):** Derivada cruzada de segunda ordem que mede a variação do Delta em relação a mudanças na volatilidade ($\frac{\partial^2 V}{\partial S \partial \sigma}$).
* **Eta ($\eta$):** Grega não-linear que quantifica a sensibilidade do desvio padrão do erro de hedge terminal em relação a erros de previsão de volatilidade.
* **Princípio de Avaliação Local Risco-Neutra (LRNV):** Estrutura desenvolvida por Duan para precificação de opções quando o ativo subjacente segue um processo heteroscedástico GARCH.

---

## Citações Importantes com Contexto

> *"Substituting the drift and diffusion terms from the Geometric Brownian Motion equation into the quadratic term $(dS_t)^2$ reveals that $(\mu S_t dt + \sigma S_t dW_t^P)^2 = \sigma^2 S_t^2 dt + O(dt^{3/2})$. Consequently, the explicit stochastic expansion of $dV(t, S_t)$ under the physical measure $P$ is expressed as: $dV(t, S_t) = \left( \frac{\partial V}{\partial t} + \mu S_t \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S_t^2 \frac{\partial^2 V}{\partial S^2} \right) dt + \sigma S_t \frac{\partial V}{\partial S} dW_t^P$."*

**Contexto:** Esta passagem estabelece a base teórica do Lema de Itô aplicada ao preço das opções. Ela demonstra como a variação quadrática não-nula do movimento Browniano introduz o termo de convexidade de segunda ordem ($\frac{1}{2} \sigma^2 S_t^2 \frac{\partial^2 V}{\partial S^2}$) na variação determinística do valor da opção.

> *"Crucially, the drift parameter of the physical asset $\mu$ cancels out completely during the delta-matching step. Consequently, the fair value of a derivative is entirely independent of investor risk preferences and expected market returns."*

**Contexto:** Este trecho destaca o conceito central do modelo de Black-Scholes: a neutralização do risco direcional via hedge delta contínuo elimina a taxa de retorno esperada do ativo subjacente ($\mu$), permitindo a precificação risco-neutra.

> *"Kabanov and Safarian (1997) rigorously re-evaluated Leland’s model and proved that as $\Delta t \to 0$, Leland’s modified delta strategy fails to converge to the target option payoff. Because frequent rebalancing accelerates transaction costs faster than the augmented volatility premium accumulates, total hedging error diverges unless rebalancing schedules are linked dynamically to cost parameters."*

**Contexto:** Revela a limitação teórica do modelo de volatilidade aumentada de Leland para custos de transação, justificando a adoção de estratégias de controle ótimo baseadas em bandas de não-transação.

> *"As demonstrated by Mykland and peers, as $\Delta t \to 0$ (or $N \to \infty$), the normalized terminal hedging error process $\frac{HE(T)}{\sqrt{\Delta t}}$ converges weakly to a continuous Gaussian martingale driven by an independent Brownian motion $W_t^*$. This limiting distribution confirms that discrete delta hedging error scales at the asymptotic order of $O(\sqrt{\Delta t})$."*

**Contexto:** Define a estrutura assintótica do erro de discretização no hedge delta, demonstrando que a incompletude gerada pela negociação em tempo discreto introduz uma nova fonte irredutível de variação estocástica no portfólio.

---

## Insights Acionáveis

1. **Ajuste Frequencial vs. Fricção de Custos:** A escala de erro de discretização de ordem $O(\sqrt{\Delta t})$ exige alta frequência de rebalanceamento; no entanto, em presença de custos de transação $k$, o rebalanceamento em tempo discreto fixo deve ser substituído por **bandas de não-transação por utilidade (Hodges-Neuberger)** para evitar a divergência dos custos operacionais.
2. **Hedge de Segunda Ordem (Gamma e Vega):** A neutralização do Delta não elimina os riscos associados ao descasamento de volatilidade ($\sigma_F \neq \sigma_R$). Posições em opções complexas (ex: opções de barreira, que exibem elevado $\eta = 23,683$) exigem a execução combinada de hedges Gamma-neutros e Vega-neutros com opções secundárias.
3. **Ajuste para Dinâmicas GARCH:** Quando a volatilidade exibe heteroscedasticidade condicional e os investidores são aversos ao risco ($\lambda > 0$), deltas calculados via fórmula padrão de Black-Scholes geram desalinhamentos estruturais. Nestes regimes, deve-se aplicar a aproximação de delta baseada em simulação Monte Carlo sob a medida LRNV de Duan.