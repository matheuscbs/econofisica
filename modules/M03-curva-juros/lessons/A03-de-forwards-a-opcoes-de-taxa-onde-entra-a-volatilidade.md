<!-- imported from vault study notes; curated for open course -->
# M03.A03 — De forwards a opções de taxa: onde entra a volatilidade

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M03
> **Aula:** M03.A03

↑ M03 · Resumo · Completo

**Módulo:** M03
**Pergunta do módulo:** Como montar curva de juros e precificar taxa sem arbitragem?

## Conceito-núcleo
Caplets/floorlets/swaptions: integrar vol aos produtos de taxa além do forward determinístico.

## Aplicação em mercado / trading
Passar de “só curva” para risco de vol em livros de taxa; escolher modelo de cotação (Black etc.).

## Entregável / lab
Mapa de produtos: FRA → caplet → cap/swaption e qual vol cada um “vê”.

## Fonte (mapeamento)
quantitative-trading-free-lesson/11 from-forwards-to-options-integrating-volatility-into-interest-rate-products

## Guia de estudo aprofundado

> **info**
>

### Conceitos-Chave Explicados em Profundidade

#### Da Curva Linear para Estruturas Opcionais
Na precificação de ativos de taxa de juros, o ponto de partida é a curva de desconto $P(0,T)$, que representa uma tabela de preços no presente ($t=0$). A partir dessa curva, a condição de não arbitragem impõe deterministicamente as taxas *forward* para cada período $[T_{i-1}, T_i]$. 

Para um determinado período $i$, delimitado pelas datas $T_{i-1}$ (data de fixação ou *reset*) e $T_i$ (data de pagamento), com fator de acrual $\Delta_i$, a taxa *forward* simples $F_i$ (ou Libor *forward*) é dada por:

$F_i = L(0; T_{i-1}, T_i) = \frac{1}{\Delta_i} \left( \frac{P(0, T_{i-1})}{P(0, T_i)} - 1 \right)$

Essa relação obedece à identidade local utilizada como verificação numérica:

$P(0, T_i) \Delta_i F_i = P(0, T_{i-1}) - P(0, T_i)$

A transição dos produtos lineares (como FRAs e Swaps) para produtos opcionais não altera a mecânica subjacente do fluxo de caixa; ela substitui a parcela linear por um operador não linear do tipo $\max(\cdot, 0)$. O fluxo contínuo de cupom flutuante mantém os mesmos calendários, acruais e datas, mas o valor do cupom passa a ser protegido por uma opção.

#### Caplets, Floorlets, Caps e Floors
Um **caplet** é uma opção sobre a taxa flutuante de um único período $i$, fixada em $T_{i-1}$ e paga em $T_i$. O seu *payoff* no momento do pagamento $T_i$ é:

$\text{Payoff}_{T_i}^{\text{caplet}} = N \Delta_i \max\left(L(T_{i-1}; T_{i-1}, T_i) - K, 0\right)$

Um **floorlet** é a estrutura espelhada, com *payoff* pago em $T_i$:

$\text{Payoff}_{T_i}^{\text{floorlet}} = N \Delta_i \max\left(K - L(T_{i-1}; T_{i-1}, T_i), 0\right)$

Um **Cap** com maturidade $T_n$ é a soma de *caplets* ao longo de todos os períodos do cronograma. Da mesma forma, um **Floor** é a soma de *floorlets*:

$\text{Cap} = \sum_{i=1}^{n} \text{Caplet}_i, \qquad \text{Floor} = \sum_{i=1}^{n} \text{Floorlet}_i$

Como os fluxos de caixa ocorrem em datas distintas, o Valor Presente ($V_0$) no tempo $t=0$ é obtido pela soma direta dos valores presentes de cada componente individual:

$V_0(\text{Cap}) = \sum_{i=1}^{n} V_0(\text{Caplet}_i), \qquad V_0(\text{Floor}) = \sum_{i=1}^{n} V_0(\text{Floorlet}_i)$

#### O Modelo de Black-76
Para precificar a não linearidade do *payoff*, é necessário modelar a distribuição de probabilidade da taxa de fixação no *reset*. No modelo de Black-76, assume-se que a taxa *forward* $F_i$ segue uma distribuição lognormal sob a medida de amarra apropriada.

Definindo $\tau_i = T_{i-1}$ como o tempo até a fixação e $\sigma_i$ como a volatilidade implícita de Black do *caplet*, a fórmula de precificação em $t=0$ para o *caplet* é:

$V_0(\text{caplet}_i) = N P(0, T_i) \Delta_i \left[ F_i \mathcal{N}(d_1) - K \mathcal{N}(d_2) \right]$

onde:

$d_1 = \frac{\ln(F_i / K) + \frac{1}{2} \sigma_i^2 \tau_i}{\sigma_i \sqrt{\tau_i}}, \qquad d_2 = d_1 - \sigma_i \sqrt{\tau_i}$

E para o *floorlet*:

$V_0(\text{floorlet}_i) = N P(0, T_i) \Delta_i \left[ K \mathcal{N}(-d_2) - F_i \mathcal{N}(-d_1) \right]$

A **paridade caplet-floorlet** garante que a diferença entre um *caplet* e um *floorlet* de mesmo *strike* resulte na posição em um contrato *forward* linear (tipo FRA):

$\text{Caplet}_i - \text{Floorlet}_i = N P(0, T_i) \Delta_i (F_i - K)$

#### O Modelo de Bachelier
Quando as taxas de juros assumem valores muito baixos ou negativos, o modelo lognormal de Black-76 torna-se inadequado devido à presença do termo logarítmico $\ln(F_i / K)$. O modelo de Bachelier assume que a taxa *forward* segue uma distribuição normal, com volatilidade $\sigma_N$ expressa em unidades de taxa (pontos-base).

Definindo a variável padronizada:

$x = \frac{F_i - K}{\sigma_N \sqrt{\tau_i}}$

O valor presente do *caplet* sob Bachelier é:

$V_0(\text{caplet}_i) = N P(0, T_i) \Delta_i \left[ (F_i - K) \mathcal{N}(x) + \sigma_N \sqrt{\tau_i} \varphi(x) \right]$

E do *floorlet*:

$V_0(\text{floorlet}_i) = N P(0, T_i) \Delta_i \left[ (K - F_i) \mathcal{N}(-x) + \sigma_N \sqrt{\tau_i} \varphi(x) \right]$

Nessas equações, $(F_i - K)$ representa o valor intrínseco, enquanto o termo contendo a densidade normal $\varphi(x)$ representa o valor no tempo da opção.

#### Swaptions
Uma **swaption** é uma opção para entrar em um *swap* de taxa de juros (fixo por flutuante) em uma data futura (data de expiração $T_0$). Diferente do *cap*, a *swaption* não se decompõe em uma simples soma de *caplets*, pois incide sobre a taxa *swap* como um todo, dependendo da estrutura de correlação entre as diversas taxas *forward*.

Para precificação, o *swap* subjacente iniciado em $T_0$ e encerrado em $T_n$ é comprimido em dois indicadores em $t=0$:
1. A **Anuidade** $A(0)$, que é a soma dos fatores de desconto ponderados pelos acruais das datas de pagamento do *swap*:

$A(0) = \sum_{i=1}^{n} \Delta_i P(0, T_i)$

2. A **Taxa Swap Forward** $S(0)$:

$S(0) = \frac{P(0, T_0) - P(0, T_n)}{A(0)}$

Sob o modelo de Black, uma **Payer Swaption** (direito de pagar taxa fixa $K$ e receber flutuante) é precificada como:

$V_0(\text{payer swaption}) = N A(0) \left[ S(0) \mathcal{N}(d_1) - K \mathcal{N}(d_2) \right]$

onde:

$d_1 = \frac{\ln(S(0) / K) + \frac{1}{2} \sigma^2 T_0}{\sigma \sqrt{T_0}}, \qquad d_2 = d_1 - \sigma \sqrt{T_0}$

A **Receiver Swaption** (direito de receber taxa fixa $K$ e pagar flutuante) é dada por:

$V_0(\text{receiver swaption}) = N A(0) \left[ K \mathcal{N}(-d_2) - S(0) \mathcal{N}(-d_1) \right]$

A **paridade das swaptions** reflete o valor de um *swap forward* linear:

$\text{Payer} - \text{Receiver} = N A(0) (S(0) - K)$

---

### Intuição de Mercado e Trading

#### Gestão de Risco Tomadores vs. Aplicadores
* **Tomadores de Empréstimo (Borrowers):** Estão expostos ao risco de alta nas taxas de juros flutuantes nas datas de *reset*. Para fixar um teto ao custo de financiamento sem abdicar de eventuais quedas nas taxas, assumem posições compradas (*long*) em *caplets* ou *caps*.
* **Aplicadores/Investidores (Lenders):** Estão expostos à queda das taxas de juros. Para garantir um rendimento mínimo em suas aplicações flutuantes, compram *floorlets* ou *floors*.

#### Caps vs. Swaptions
Embora ambos protejam contra variações nas taxas de juros, o *cap* é uma carteira de opções independentes sobre taxas *forward* individuais (cada *caplet* exerce individualmente se a taxa daquele período superar $K$). Já a *swaption* é uma opção única exercida na expiração $T_0$ sobre a taxa média ponderada (*forward swap rate*) de todo o período contratual. Por isso, a *swaption* depende da correlação entre as taxas *forward*, não podendo ser obtida pela simples soma de *caplets*.

#### A Escolha entre Black-76 e Bachelier
O modelo Black-76 trabalha em termos percentuais relativos da taxa (volatilidade lognormal). Quando as taxas de juros caem para níveis muito próximos de zero ou entram em território negativo, os retornos relativos explodem e a matemática do logaritmo natural falha. O modelo de Bachelier contorna essa limitação ao expressar a volatilidade em termos absolutos (pontos-base), permitindo a simulação contínua e sem interrupções de taxas nulas ou negativas.

---

### Exemplo Numérico Resolvido Passo a Passo

Considere um *caplet* com os seguintes parâmetros obtidos do mercado no tempo $t=0$:
* Notional ($N$): $\$ 10.000.000$
* Período de acrual ($\Delta_1$): $0,5$ anos
* Data de fixação ($\tau_1 = T_0$): $0,5$ anos
* Data de pagamento ($T_1$): $1,0$ ano
* Preços de desconto da curva: $P(0, 0,5) = 0,9900$ e $P(0, 1,0) = 0,9750$
* Taxa de exercício ($K$): $3,0\%$ ao ano ($0,03$)
* Volatilidade de Black ($\sigma_1$): $20\%$ ao ano ($0,20$)

#### Passo 1 Calcular a Taxa Forward $F_1$
Aplicando a fórmula da taxa *forward* simples:

$F_1 = \frac{1}{\Delta_1} \left( \frac{P(0, T_0)}{P(0, T_1)} - 1 \right) = \frac{1}{0,5} \left( \frac{0,9900}{0,9750} - 1 \right) = 2 \times (1,0153846 - 1) = 0,0307692 \quad (3,07692\%)$

*Verificação de Consistência Local:*
$P(0, 1,0) \Delta_1 F_1 = 0,9750 \times 0,5 \times 0,0307692 = 0,0150$
$P(0, 0,5) - P(0, 1,0) = 0,9900 - 0,9750 = 0,0150$ (Identidade confirmada).

#### Passo 2 Calcular os Parâmetros $d_1$ e $d_2$ do Black-76
* Volatilidade acumulada até a fixação: $\text{vol} = \sigma_1 \sqrt{\tau_1} = 0,20 \times \sqrt{0,5} = 0,20 \times 0,7071068 = 0,1414214$
* Logaritmo da razão entre a taxa *forward* e o *strike*: $\ln(F_1 / K) = \ln(0,0307692 / 0,03) = \ln(1,02564) = 0,0253178$
* Termo do desvio: $\frac{1}{2} \sigma_1^2 \tau_1 = 0,5 \times (0,20)^2 \times 0,5 = 0,0100$

Cálculo de $d_1$:
$d_1 = \frac{0,0253178 + 0,0100}{0,1414214} = \frac{0,0353178}{0,1414214} \approx 0,24973$

Cálculo de $d_2$:
$d_2 = d_1 - \sigma_1 \sqrt{\tau_1} = 0,24973 - 0,14142 = 0,10831$

#### Passo 3 Avaliar as Probabilidades Acumuladas $\mathcal{N}(d_1)$ e $\mathcal{N}(d_2)$
Consultando a distribuição normal padrão:
$\mathcal{N}(0,24973) \approx 0,59860$
$\mathcal{N}(0,10831) \approx 0,54311$

#### Passo 4 Calcular o Valor Presente do Caplet ($V_0$)
$V_0(\text{caplet}_1) = N \times P(0, T_1) \times \Delta_1 \times \left[ F_1 \mathcal{N}(d_1) - K \mathcal{N}(d_2) \right]$

Substituindo os valores:
$N \times P(0, T_1) \times \Delta_1 = 10.000.000 \times 0,9750 \times 0,5 = 4.875.000$
$\text{Termo entre colchetes} = (0,0307692 \times 0,59860) - (0,03 \times 0,54311) = 0,0184184 - 0,0162933 = 0,0021251$

$V_0(\text{caplet}_1) = 4.875.000 \times 0,0021251 \approx \$ 10.364,86$

#### Passo 5 Verificação por Paridade Caplet-Floorlet
O valor do contrato *forward* equivalente (lado direito da paridade) é:
$\text{Paridade}_{\text{RHS}} = N \times P(0, T_1) \times \Delta_1 \times (F_1 - K) = 4.875.000 \times (0,0307692 - 0,03) = 4.875.000 \times 0,0007692 = \$ 3.750,00$

Logo, o valor do *floorlet* correspondente no mesmo *strike* é:
$V_0(\text{floorlet}_1) = V_0(\text{caplet}_1) - 3.750,00 = 10.364,86 - 3.750,00 = \$ 6.614,86$

---

### Armadilhas Comuns

1. **Incoerência nos Fatores de Desconto versus Volatilidade:**
   Ao precificar um *caplet*, a volatilidade atua sobre o tempo até a **data de fixação** ($\tau_i = T_{i-1}$), pois a incerteza cessa no *reset*. No entanto, o fator de desconto $P(0, T_i)$ deve ser calculado até a **data de pagamento** ($T_i$). Descontar o fluxo para a data de fixação $T_{i-1}$ gera um erro sistemático de precificação.

2. **Decomposição Incorreta de Swaptions:**
   Tentar avaliar uma *swaption* somando o valor de vários *caplets*. A *swaption* exerce sobre uma única taxa *swap* e em uma única data de expiração $T_0$, dependendo da estrutura de covariância/correlação entre todos os *forwards* do período, enquanto os *caplets* são opções independentes exercidas período a período.

3. **Aplicação do Modelo Black-76 com Taxas Negativas:**
   Utilizar a fórmula de Black-76 em cenários onde a taxa *forward* $F_i$ ou o *strike* $K$ são menores ou iguais a zero. O cálculo do parâmetro $d_1$ requer o logaritmo natural de $(F_i / K)$, gerando falha de execução matemática. Em tais contextos, deve-se transicionar para o modelo de Bachelier.

4. **Incompatibilidade na Unidade da Volatilidade:**
   Misturar a volatilidade de Black ($\sigma$, expressa em porcentagem relativa, ex: $20\% = 0,20$) com a volatilidade de Bachelier ($\sigma_N$, expressa em unidades de taxa/pontos-base, ex: $1\% = 0,01$).

---

### Lab Prático Sugerido em Python

O laboratório prático deve seguir a sequência estrutural de implementação descrita abaixo.

#### Passo 1 Construção do Cronograma e Curva de Desconto
Defina o vetor de datas de pagamento $T$ de $0,5$ a $5,0$ anos com passos de $0,5$ ($\Delta = 0,5$) e o notional $N = 10.000.000$. Configure uma grade de pontos discretos de mercado:
* $T_{\text{grid}} =$
* $P_{\text{grid}} =$

Crie uma função de interpolação log-linear sobre os preços de desconto para obter $P(0, T)$ e monte os vetores de desconto para a data de pagamento $P$ e data anterior $P_{\text{prev}}$.

```python
import numpy as np
from math import log, sqrt
from scipy.stats import norm

## 1. Schedule
T = np.arange(0.5, 5.0 + 0.5, 0.5)
Delta = np.full_like(T, 0.5, dtype=float)
Nn = 10_000_000

## 2. Curva de desconto com interpolação log-linear
T_grid = np.array([0.0, 0.5, 1.0, 2.0, 3.0, 5.0], dtype=float)
P_grid = np.array([1.0, 0.9900, 0.9750, 0.9450, 0.9100, 0.8500], dtype=float)

def P0(x):
    x = float(x)
    if x <= T_grid: return float(P_grid)
    if x >= T_grid[-1]: return float(P_grid[-1])
    return float(np.exp(np.interp(x, T_grid, np.log(P_grid))))

P = np.array([P0(ti) for ti in T], dtype=float)
P_prev = np.array([P0(0.0)] + [P0(ti) for ti in T[:-1]], dtype=float)
```

#### Passo 2 Extração das Taxas Forward
Calcule as taxas *forward* para cada período $F_i = \frac{1}{\Delta_i} \left( \frac{P(0, T_{i-1})}{P(0, T_i)} - 1 \right)$ e defina o tempo de fixação $\tau_{\text{fix}} = T - \Delta$.

```python
F = (P_prev / P - 1.0) / Delta
tau_fix = T - Delta
```

#### Passo 3 Funções Precificadoras (Black e Bachelier)
Implemente as funções `black_caplet`, `black_floorlet`, `bach_caplet` e `bach_floorlet`. Inclua o tratamento para $\tau \le 0$ retornando o *payoff* intrínseco descontado.

```python
def black_caplet(N, P_pay, delta, Fwd, K, sigma, tau):
    if tau <= 0: return N * P_pay * delta * max(Fwd - K, 0.0)
    vol = sigma * sqrt(tau)
    d1 = (log(Fwd / K) + 0.5 * vol * vol) / vol
    d2 = d1 - vol
    return N * P_pay * delta * (Fwd * norm.cdf(d1) - K * norm.cdf(d2))

def black_floorlet(N, P_pay, delta, Fwd, K, sigma, tau):
    if tau <= 0: return N * P_pay * delta * max(K - Fwd, 0.0)
    vol = sigma * sqrt(tau)
    d1 = (log(Fwd / K) + 0.5 * vol * vol) / vol
    d2 = d1 - vol
    return N * P_pay * delta * (K * norm.cdf(-d2) - Fwd * norm.cdf(-d1))

def bach_caplet(N, P_pay, delta, Fwd, K, sigmaN, tau):
    if tau <= 0: return N * P_pay * delta * max(Fwd - K, 0.0)
    s = sigmaN * sqrt(tau)
    x = (Fwd - K) / s
    return N * P_pay * delta * ((Fwd - K) * norm.cdf(x) + s * norm.pdf(x))

def bach_floorlet(N, P_pay, delta, Fwd, K, sigmaN, tau):
    if tau <= 0: return N * P_pay * delta * max(K - Fwd, 0.0)
    s = sigmaN * sqrt(tau)
    x = (Fwd - K) / s
    return N * P_pay * delta * ((K - Fwd) * norm.cdf(-x) + s * norm.pdf(-x))
```

#### Passo 4 Precificação de Caps/Floors e Checagem de Paridade
Itere sobre a grade de prazos para somar os valores dos *caplets* e *floorlets* ($K_{\text{cap}} = 0,03$, $\sigma_{\text{black}} = 0,20$, $\sigma_N = 0,01$). Calcule o valor do fluxo linear e valide a paridade $\text{Cap} - \text{Floor} = \text{Paridade}_{\text{RHS}}$.

```python
K_cap = 0.03
sigma_black = 0.20
sigmaN = 0.01

cap_black = sum(black_caplet(Nn, P[i], Delta[i], F[i], K_cap, sigma_black, tau_fix[i]) for i in range(len(T)))
floor_black = sum(black_floorlet(Nn, P[i], Delta[i], F[i], K_cap, sigma_black, tau_fix[i]) for i in range(len(T)))
cap_norm = sum(bach_caplet(Nn, P[i], Delta[i], F[i], K_cap, sigmaN, tau_fix[i]) for i in range(len(T)))

parity_rhs = np.sum(Nn * P * Delta * (F - K_cap))
print("Diferença da Paridade Cap-Floor =", (cap_black - floor_black) - parity_rhs)
```

#### Passo 5 Compressão de Swaptions e Verificação
Para uma *swaption* com expiração em $1,0$ ano sobre um *swap* até $5,0$ anos:
1. Filtre as datas $T > \text{expiry}$.
2. Calcule a Anuidade $A(0) = \sum \Delta_i P(0, T_i)$.
3. Calcule a Taxa Swap Forward $S(0) = \frac{P(0, \text{expiry}) - P(0, T_n)}{A(0)}$.
4. Precifique Payer e Receiver Swaptions ATM ($K = S(0)$) com volatilidade $\sigma_{\text{swpt}} = 0,20$.
5. Confirme a paridade de *swaption*: $\text{Payer} - \text{Receiver} = N A(0) (S(0) - K)$.

```python
expiry = 1.0
Tn = 5.0
sigma_swpt = 0.20

mask = T > expiry
T_pay = T[mask]
Delta_pay = Delta[mask]

A0 = np.sum(Delta_pay * np.array([P0(ti) for ti in T_pay]))
S0 = (P0(expiry) - P0(Tn)) / A0

K_swpt = S0
vol = sigma_swpt * sqrt(expiry)
d1 = (log(S0 / K_swpt) + 0.5 * vol * vol) / vol
d2 = d1 - vol

pv_payer = Nn * A0 * (S0 * norm.cdf(d1) - K_swpt * norm.cdf(d2))
pv_receiver = Nn * A0 * (K_swpt * norm.cdf(-d2) - S0 * norm.cdf(-d1))

print("Diferença Paridade Swaption =", (pv_payer - pv_receiver) - Nn * A0 * (S0 - K_swpt))
```

---

### Glossário

* **Anuidade ($A(0)$):** Soma dos fatores de desconto ponderados pelos fatores de acrual dos fluxos de pagamento de um *swap*, representando o valor presente de $1$ ponto-base pago na perna fixa.
* **Bachelier (Modelo Normal):** Modelo de precificação de opções que assume distribuição normal para as taxas *forward*, utilizando volatilidades absolutas e permitindo a modelagem de taxas de juros nulas ou negativas.
* **Black-76 (Modelo Lognormal):** Modelo padrão de mercado para precificação de opções sobre *forwards*, que assume distribuição lognormal para a taxa subjacente.
* **Cap:** Contrato financeiro composto por uma sequência de *caplets*, que garante um teto para a taxa de juros flutuante ao longo de múltiplos períodos.
* **Caplet:** Opção de compra (Call) sobre a taxa de juros de um único período, que paga a diferença positiva entre a taxa de fixação e a taxa de exercício.
* **Data de Fixação / Reset ($T_{i-1}$):** Momento no qual a taxa de juros flutuante do período $[T_{i-1}, T_i]$ é observada e definida no mercado.
* **Floor:** Contrato financeiro composto por uma sequência de *floorlets*, que estabelece um piso mínimo para a taxa de juros flutuante ao longo de múltiplos períodos.
* **Floorlet:** Opção de venda (Put) sobre a taxa de juros de um único período, que paga a diferença positiva entre a taxa de exercício e a taxa de fixação.
* **Payer Swaption:** Opção que concede ao seu titular o direito de entrar em um *swap* na posição de pagador da taxa fixa e recebedor da taxa flutuante.
* **Receiver Swaption:** Opção que concede ao seu titular o direito de entrar em um *swap* na posição de recebedor da taxa fixa e pagador da taxa flutuante.
* **Taxa Swap Forward ($S(0)$):** A taxa fixa que zera o valor presente líquido de um *swap* de taxa de juros com início em uma data futura $T_0$ e término em $T_n$.

---

### Questões e Prática

#### Nível Fácil

1. **Qual é o *payoff* de um *caplet* no momento do seu pagamento $T_i$?**
   * **Resposta:** O *payoff* é dado por $N \Delta_i \max(L(T_{i-1}; T_{i-1}, T_i) - K, 0)$, onde $N$ é o notional, $\Delta_i$ é o fator de acrual, $L(T_{i-1}; T_{i-1}, T_i)$ é a taxa flutuante fixada em $T_{i-1}$ e $K$ é a taxa de exercício.

2. **Como se obtém o Valor Presente ($V_0$) de um *Cap* de maturidade $T_n$ a partir de seus componentes?**
   * **Resposta:** Somando os valores presentes de cada *caplet* individual que compõe o cronograma do contrato: $V_0(\text{Cap}) = \sum_{i=1}^{n} V_0(\text{Caplet}_i)$.

3. **Qual é a relação matemática que define a paridade *caplet-floorlet* para um período $i$?**
   * **Resposta:** $\text{Caplet}_i - \text{Floorlet}_i = N P(0, T_i) \Delta_i (F_i - K)$.

#### Nível Intermediário

4. **Por que o tempo para cálculo da volatilidade ($\tau_i$) utiliza a data $T_{i-1}$ enquanto o fator de desconto utiliza a data $T_i$?**
   * **Resposta:** Porque a incerteza referente ao valor da taxa flutuante é resolvida na data de fixação/reset ($T_{i-1}$), definindo a volatilidade aplicável até esse ponto. O pagamento do fluxo financeiro correspondente, no entanto, ocorre apenas no final do período de acrual, na data $T_i$, exigindo que o desconto financeiro cubra todo o intervalo até $T_i$.

5. **A partir dos preços de desconto $P(0, 1,0) = 0,9750$ e $P(0, 5,0) = 0,8500$, com anuidade $A(0) = 3,50$, calcule a Taxa Swap Forward $S(0)$ para um *swap* de $1,0$ a $5,0$ anos.**
   * **Resposta:** Aplicando a fórmula $S(0) = \frac{P(0, T_0) - P(0, T_n)}{A(0)}$ com $T_0 = 1,0$ e $T_n = 5,0$:
     $S(0) = \frac{0,9750 - 0,8500}{3,50} = \frac{0,1250}{3,50} \approx 0,035714 \quad (3,5714\%)$

6. **Explique a principal limitação do modelo Black-76 ao precificar opções de taxa de juros em ambientes de taxas negativas e como o modelo de Bachelier resolve essa questão.**
   * **Resposta:** O modelo Black-76 assume distribuição lognormal para a taxa *forward*, necessitando calcular $\ln(F_i / K)$. Se $F_i \le 0$ ou $K \le 0$, o logaritmo fica indefinido. O modelo de Bachelier substitui a distribuição lognormal pela distribuição normal, medindo a variação em termos absolutos de taxa ($\sigma_N$), o que elimina o logaritmo e permite precificar taxas negativas sem falhas matemáticas.

#### Nível Avançado

7. **Demonstre por que uma *Swaption* não pode ser precificada simplesmente através da soma dos valores dos *caplets* correspondentes às datas do *swap* subjacente.**
   * **Resposta:** Um *cap* é uma carteira de opções independentes, onde cada *caplet* possui o direito de exercício individualizado em cada data de *reset* $T_{i-1}$ sobre a taxa *forward* específica $F_i$. A *swaption*, por outro lado, é exercida em um único momento (na expiração $T_0$) sobre a taxa *swap forward* $S(0)$, que representa uma média ponderada de todas as taxas *forward* futuras. O valor da *swaption* depende da estrutura de correlação entre as diversas taxas *forward* da curva. Como o operador $\max$ da soma de taxas não é igual à soma dos operadores $\max$ individuais ($\max(\sum X_i - K, 0) \neq \sum \max(X_i - K_i, 0)$), a precificação por simples soma de *caplets* descarta a correlação e incorre em erro estrutural.

8. **Considere um *caplet* precificado pelo modelo de Bachelier com $F_i = K$. Mostre como a fórmula do valor presente do *caplet* se simplifica nesse cenário de opção *At-The-Money* (ATM).**
   * **Resposta:** No modelo de Bachelier:
     $V_0(\text{caplet}_i) = N P(0, T_i) \Delta_i \left[ (F_i - K) \mathcal{N}(x) + \sigma_N \sqrt{\tau_i} \varphi(x) \right]$
     Quando a opção está ATM ($F_i = K$), a variável padronizada torna-se:
     $x = \frac{F_i - K}{\sigma_N \sqrt{\tau_i}} = \frac{0}{\sigma_N \sqrt{\tau_i}} = 0$
     Sabendo que para a distribuição normal padrão $\mathcal{N}(0) = 0,5$ e a densidade de probabilidade é $\varphi(0) = \frac{1}{\sqrt{2\pi}}$, o termo intrínseco se anula:
     $(F_i - K) \mathcal{N}(0) = 0 \times 0,5 = 0$
     Restando apenas o valor no tempo:
     $V_0(\text{caplet}_i) = N P(0, T_i) \Delta_i \left( \sigma_N \sqrt{\tau_i} \varphi(0) \right) = N P(0, T_i) \Delta_i \frac{\sigma_N \sqrt{\tau_i}}{\sqrt{2\pi}}$