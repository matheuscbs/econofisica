<!-- imported from vault study notes; curated for open course -->
# M03.A01 — Taxas forward sem arbitragem: construir a curva a partir do mercado

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M03
> **Aula:** M03.A01

↑ M03 · Resumo · Completo

**Módulo:** M03
**Pergunta do módulo:** Como montar curva de juros e precificar taxa sem arbitragem?

## Conceito-núcleo
Forwards implícitos por no-arbitrage entre depósitos/bonds; ausência de “opinião” na bootstrap.

## Aplicação em mercado / trading
Montar curva para precificar FRAs e marcar carry de taxa; detectar inconsistências entre tenors.

## Entregável / lab
Bootstrap simplificado: de cash/deposit a forwards 1x2, 2x3… e checagem de no-arb.

## Fonte (mapeamento)
quantitative-trading-free-lesson/09 forward rates by no arbitrage

## Guia de estudo aprofundado

> **info**
>

Este guia de estudos fornece uma síntese estruturada sobre a construção de taxas *forward* a partir da condição de não arbitragem, a transição entre o modelo de desconto constante e a curva de desconto de renda fixa, a precificação de *Forward Rate Agreements* (FRA) e a mecânica de liquidação no mercado financeiro.

---

### Visão Geral e Contextualização

Em modelos de apreçamento contínuo, como o modelo de Black-Scholes ou de Mouvement Browniano Geométrico (GBM), a estrutura de precificação é dividida em dois blocos:
1. A dinâmica estocástica do ativo subjacente sob a medida de risco-neutro $\mathbb{Q}$.
2. Uma regra de desconto temporal baseada em uma taxa livre de risco constante $r$.

Nesse contexto simplificado, o valor presente $V_0$ de um *payoff* futuro $H$ em $T$ é dado por:

$$V_0 = e^{-rT}\mathbb{E}^\mathbb{Q}[H]$$

No mercado de renda fixa e derivativos de taxas de juros, a lógica fundamental da avaliação do valor do dinheiro no tempo permanece idêntica, mas substitui-se o fator de desconto único $e^{-rT}$ por uma **função de desconto** $P(0,T)$. O objeto primário deixa de ser um único número ajustável $r$ e passa a ser uma tabela ou curva completa de fatores de desconto para cada maturidade $T$.

Se a taxa de juros for constante e igual a $r$, o fator $P(0,T)$ coincide exatamente com $e^{-rT}$. Quando as taxas não são constantes ou variam por maturidade, $P(0,T)$ representa diretamente o preço hoje ($t=0$) de 1 unidade monetária garantida a ser paga na data futura $T$.

---

### Conceitos-Chave Explicados em Profundidade

#### Fatores de Desconto $P(0,T)$
O fator de desconto $P(0,T)$ é o bloco construtivo elementar da renda fixa. Ele mapeia a maturidade $T$ no preço atual de um fluxo de caixa de 1 euro/real pago em $T$:

$$T \mapsto P(0,T)$$

Como todos os instrumentos de renda fixa são conjuntos de fluxos de caixa datados (certos ou condicionais a um *fixing*), a curva $P(0,T)$ é a base indispensável para precificar e replicar qualquer derivativo do setor.

#### Taxa Forward Simples
Uma vez estabelecida a curva de desconto $P(0,T)$, as taxas *forward* não podem ser definidas livremente ou por intuição; elas são estritamente impostas pela **ausência de arbitragem**.

Considerando duas datas $0 < T_1 < T_2$ e uma fração de ano $\Delta = T_2 - T_1$ (utilizando convenções como ACT/360 ou 30/360), a taxa *forward* simples $L(0;T_1,T_2)$ é a taxa fixada hoje para um empréstimo ou aplicação no período futuro $[T_1, T_2]$.

A condição de não arbitragem exige que investir 1 unidade monetária até $T_2$ diretamente resulte no mesmo montante final que investir 1 unidade até $T_1$ e reinvesti-la de $T_1$ a $T_2$ à taxa *forward*:

$$1 + L(0;T_1,T_2)\Delta = \frac{P(0,T_1)}{P(0,T_2)}$$

Isolando a taxa *forward* simples $L(0;T_1,T_2)$, obtém-se a fórmula fundamental:

$$L(0;T_1,T_2) = \frac{1}{\Delta} \left( \frac{P(0,T_1)}{P(0,T_2)} - 1 \right)$$

*Nota econômica:* Se a curva de desconto implicar $P(0,T_2) > P(0,T_1)$, a razão $\frac{P(0,T_1)}{P(0,T_2)}$ será menor que 1, resultando em uma taxa *forward* negativa. Isso reflete um retorno monetário negativo precificado pelo mercado para o período $[T_1, T_2]$.

#### Forward Rate Agreement (FRA)
O FRA é um contrato derivativo customizado (*over-the-counter* - OTC) firmado em $t=0$ sobre um valor nocional $N$, no qual as partes travam uma taxa fixa $K$ para vigorar durante o período futuro $[T_1, T_2]$. Na data de fixação $T_1$, observa-se a taxa flutuante de mercado $L(T_1;T_1,T_2)$, aplicável ao período.

O *payoff* no final do período ($T_2$), do ponto de vista de quem **recebe a taxa flutuante e paga a taxa fixa** (*receive float / pay fixed*), é dado por:

$$\text{Payoff}_{T_2} = N \Delta \left( L(T_1;T_1,T_2) - K \right)$$

#### Precificação do FRA Par e Off-Market
1. **FRA ao Par (Par FRA):** É o contrato cujo valor presente líquido $V_0$ é igual a zero no momento do início ($t=0$). Em um ambiente determinístico de curva única (*single-curve*), a taxa de exercício ao par $K^*$ coincide exatamente com a taxa *forward*:

$$K^* = L(0;T_1,T_2) = \frac{1}{\Delta} \left( \frac{P(0,T_1)}{P(0,T_2)} - 1 \right)$$

$$V_0(K^*) = 0$$

2. **FRA Fora do Mercado (Off-Market FRA):** Se o contrato for firmado com uma taxa fixa $K \neq L(0;T_1,T_2)$, o valor presente $V_0$ no início (padrão *receive float / pay fixed*) é calculado trazendo o *payoff* esperado a valor presente descontado até $T_2$:

$$V_0 = N P(0,T_2) \Delta \left( L(0;T_1,T_2) - K \right)$$

#### Identidade de Replicação e Sensibilidade (Rate Delta)
Utilizando a identidade fundamental da taxa *forward*:

$$P(0,T_2) \Delta L(0;T_1,T_2) = P(0,T_1) - P(0,T_2)$$

Podemos reescrever o valor presente $V_0$ do FRA como uma replicação pura por fatores de desconto:

$$V_0 = N \left[ (P(0,T_1) - P(0,T_2)) - P(0,T_2) \Delta K \right]$$

A sensibilidade do valor presente em relação à taxa fixa $K$ (conhecida como *rate delta*) é estritamente linear e constante:

$$\frac{\partial V_0}{\partial K} = -N P(0,T_2) \Delta$$

Se $K > L(0;T_1,T_2)$, o participante que paga taxa fixa está pagando acima do valor praticado pelo mercado *forward*, resultando em um $V_0 < 0$.

#### Liquidação Antecipada na Data de Fixação ($T_1$)
Embora o cálculo do juro se refira ao período $[T_1, T_2]$, a prática padrão de mercado realiza o ajuste financeiro antecipadamente em $T_1$ (no *settlement*). 

Para evitar a exposição ao risco de crédito até $T_2$, calcula-se o valor presente da diferença de juros na data $T_1$, utilizando a própria taxa flutuante realizada $L(T_1;T_1,T_2)$ como fator de desconto do mercado monetário simples:

$$\text{Settlement}_{T_1} = \frac{N \Delta \left( L(T_1;T_1,T_2) - K \right)}{1 + \Delta L(T_1;T_1,T_2)}$$

mecanicamente, essa operação equivale a descontar o *payoff* de $T_2$ para $T_1$ pelo fator simples $\frac{1}{1 + \Delta L}$.

---

### Intuição de Mercado e Trading

* **Proteção de Custos de Captação (Tomador / Payer FRA):** Um tomador de empréstimo (devedor) que precisará de recursos no período futuro $[T_1, T_2]$ teme a elevação das taxas de juros. Para se proteger, ele contrata a ponta que ganha com a alta da taxa flutuante: recebe taxa flutuante e paga taxa fixa (*payer FRA*). Se a taxa flutuante fixada em $T_1$ subir, o ganho no FRA compensa o maior custo de captação no mercado financeiro.
* **Aplicações de Recurso (Investidor / Receiver FRA):** Um investidor que aplicará capital no futuro teme a queda das taxas. Ele assume a ponta que recebe taxa fixa e paga flutuante (*receiver FRA*), travando o rendimento da sua aplicação.
* **Visão Estrutural das Curvas:** A conversão de fatores de desconto em taxas *forward* demonstra que os preços de mercado hoje já "amarram" todas as taxas futuras projetadas. Operar um FRA fora do par é assumir uma posição cujo valor oscilará linearmente conforme o deslocamento da taxa *forward* em relação à taxa fixa contratada $K$.

---

### Exemplo Numérico Resolvido Passo a Passo

Considerem-se os seguintes parâmetros de mercado e especificações do contrato:

* **Valor Nocional ($N$):** $10.000.000$
* **Datas:** $T_1 = 1{,}0$ ano, $T_2 = 1{,}5$ ano ($\Delta = 0{,}5$ ano)
* **Fatores de Desconto de Mercado:**
  * $P(0; 1{,}0) = 0{,}9750$
  * $P(0; 1{,}5) = 0{,}9600$

#### Passo 1 Calcular a Taxa Forward Simples $L(0; T_1, T_2)$
Aplica-se a fórmula de não arbitragem:

$$L(0; 1{,}0; 1{,}5) = \frac{1}{0{,}5} \left( \frac{0{,}9750}{0{,}9600} - 1 \right)$$

$$L(0; 1{,}0; 1{,}5) = 2 \times (1{,}015625 - 1) = 2 \times 0{,}015625 = 0{,}03125 \text{ (ou } 3{,}125\% \text{ ao ano)}$$

#### Passo 2 Determinar a Taxa ao Par e Valor Presente ao Par
A taxa de exercício ao par $K^*$ é igual à taxa *forward*:
$$K^* = 3{,}125\%$$

O valor presente para um FRA com $K = 3{,}125\%$ é:
$$V_0 = 10.000.000 \times 0{,}9600 \times 0{,}5 \times (0{,}03125 - 0{,}03125) = 0$$

#### Passo 3 Avaliar um FRA Off-Market ($K = L_0 + 100 \text{ bps}$)
Define-se uma taxa fixa fora do mercado: $K = 3{,}125\% + 1{,}00\% = 4{,}125\%$ ($0{,}04125$).

Calcula-se o valor presente em $t=0$ (*receive float / pay fixed*) via **Fórmula 1**:
$$V_0 = 10.000.000 \times 0{,}9600 \times 0{,}5 \times (0{,}03125 - 0{,}04125)$$
$$V_0 = 4.800.000 \times (-0{,}0100) = -48.000$$

#### Passo 4 Verificar a Identidade por Replicação (Fórmula 2)
Aplica-se a **Fórmula 2** baseada exclusivamente em fatores de desconto:
$$V_0 = 10.000.000 \times \left[ (0{,}9750 - 0{,}9600) - 0{,}9600 \times 0{,}5 \times 0{,}04125 \right]$$
$$V_0 = 10.000.000 \times \left[ 0{,}0150 - 0{,}0198 \right]$$
$$V_0 = 10.000.000 \times (-0{,}0048) = -48.000$$

As duas abordagens chegam exatamente ao mesmo valor.

#### Passo 5 Calcular a Liquidação Financeira Antecipada em $T_1$
Assume-se que, na data $T_1$, a taxa flutuante realizada (*fixing*) tenha sofrido um choque de $+50\text{ bps}$, atingindo $L(T_1; 1{,}0; 1{,}5) = 3{,}625\%$ ($0{,}03625$).

1. **Payoff teórico em $T_2$:**
$$\text{Payoff}_{T_2} = 10.000.000 \times 0{,}5 \times (0{,}03625 - 0{,}04125) = 5.000.000 \times (-0{,}0050) = -25.000$$

2. **Fator de desconto de $T_2$ para $T_1$:**
$$\text{Fator} = \frac{1}{1 + 0{,}5 \times 0{,}03625} = \frac{1}{1{,}018125} \approx 0{,}9821976$$

3. **Valor de liquidação em $T_1$ ($\text{Settlement}_{T_1}$):**
$$\text{Settlement}_{T_1} = -25.000 \times 0{,}9821976 = -24.554{,}94$$

---

### Armadilhas Comuns

1. **Confusão de Fatores de Desconto na Precificação do FRA:** Descontar o valor esperado do *payoff* do FRA utilizando $P(0, T_1)$ em vez de $P(0, T_2)$. O *payoff* teórico do contrato é gerado no final do período ($T_2$), portanto deve ser trazido a valor presente utilizando $P(0, T_2)$.
2. **Inversão de Sinais nos Contratos:** Esquecer a perspectiva da posição. Para quem **recebe flutuante e paga fixo**, se a taxa fixa $K$ for maior que a taxa *forward*, o contrato tem valor presente negativo ($V_0 < 0$).
3. **Desconsiderar a Fração de Ano ($\Delta$):** Omitir a convenção de contagem de dias ($\Delta = T_2 - T_1$) ao calcular tanto a taxa *forward* quanto o *payoff* do FRA, tratando taxas anuais como se fossem diretamente aplicáveis ao período.
4. **Erro na Liquidação em $T_1$:** Descontar a liquidação em $T_1$ usando a taxa *forward* de $t=0$ em vez de utilizar a taxa flutuante **realmente fixada em $T_1$** ($L(T_1; T_1, T_2)$).

---

### Laboratório Prático em Python

Abaixo descrevem-se os passos para estruturação de um script em Python focado na construção da curva, interpolação log-linear, precificação e verificação de identidades de arbitragem de um FRA.

#### Passos de Implementação

1. **Definição da Grade de Mercado:** Criar vetores NumPy para as maturidades $T\_grid = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]$ e para os fatores de desconto correspondentes $P\_grid = [0.9900, 0.9750, 0.9600, 0.9450, 0.9100, 0.8500]$.
2. **Construção da Função de Interpolação Log-Linear:** Implementar uma função `P0(T)` que realiza interpolação linear no logaritmo dos fatores de desconto ($\log P$), garantindo a preservação da estrutura exponencial dos descontos.
3. **Cálculo da Taxa Forward Simples:** Obter $P_1 = P(0, T_1)$ e $P_2 = P(0, T_2)$ via `P0(T)` e aplicar a fórmula $L_0 = \frac{1}{\Delta} \left(\frac{P_1}{P_2} - 1\right)$.
4. **Precificação ao Par e Off-Market:**
   * Calcular o $PV$ para $K = L_0$ e verificar se o resultado é zero.
   * Defasar a taxa em $+100\text{ bps}$ ($K = L_0 + 0,01$) e calcular o $PV$ através de $N \cdot P_2 \cdot \Delta \cdot (L_0 - K)$.
5. **Verificação Numérica das Identidades:**
   * Validar a igualdade $P_2 \cdot \Delta \cdot L_0 = P_1 - P_2$.
   * Calcular o $PV$ alternativo $N \cdot \left((P_1 - P_2) - P_2 \cdot \Delta \cdot K\right)$ e confirmar a diferença zero em relação à primeira fórmula.
6. **Simulação de Liquidação Antecipada em $T_1$:** Aplicar um choque na taxa de fixação realizada $L_{real}$, calcular a liquidação em $T_1$ usando a fórmula do mercado e comparar com o *payoff* de $T_2$ descontado por $(1 + \Delta \cdot L_{real})^{-1}$.

```python
import numpy as np

## 1. Grade de mercado
T_grid = np.array([0.5, 1.0, 1.5, 2.0, 3.0, 5.0])
P_grid = np.array([0.9900, 0.9750, 0.9600, 0.9450, 0.9100, 0.8500])

## 2. Interpolação log-linear de P(0,T)
def P0(T):
    T = float(T)
    if T <= T_grid:
        return float(P_grid)
    if T >= T_grid[-1]:
        return float(P_grid[-1])
    logP = np.log(P_grid)
    return float(np.exp(np.interp(T, T_grid, logP)))

## 3. Especificações do FRA
N = 10_000_000
T1, T2 = 1.0, 1.5
Delta = T2 - T1

P1, P2 = P0(T1), P0(T2)
L0 = (P1 / P2 - 1.0) / Delta

## 4. Avaliação de PV (Par e Off-Market)
K_par = L0
PV_par = N * P2 * Delta * (L0 - K_par)

K = L0 + 0.01
PV1 = N * P2 * Delta * (L0 - K)

## 5. Checagem de identidades de replicação
PV2 = N * ((P1 - P2) - P2 * Delta * K)
diff_pv = PV1 - PV2

## 6. Settlement em T1
shock = 0.005
L_real = L0 + shock
settle_T1 = N * Delta * (L_real - K) / (1.0 + Delta * L_real)
```

---

### Glossário

* **Fator de Desconto $P(0,T)$:** Preço em $t=0$ de um título que paga 1 unidade monetária determinística na data futura $T$.
* **Taxa Forward Simples ($L(0;T_1,T_2)$):** Taxa de juros praticada sob a convenção de juros simples para um período futuro $[T_1, T_2]$, contratada na data atual $t=0$ sem oportunidade de arbitragem.
* **Forward Rate Agreement (FRA):** Contrato derivativo de balcão (OTC) no qual duas partes travam uma taxa de juros fixa para ser aplicada sobre um valor nocional durante um período futuro.
* **Taxa de Exercício ao Par (Par Strike $K^*$):** A taxa fixa $K$ para a qual o valor presente líquido de um FRA no início do contrato é estritamente igual a zero.
* **Liquidação Antecipada (Settlement at $T_1$):** Mecanismo de mercado em que a liquidação financeira do FRA ocorre na data de fixação $T_1$, descontando-se o valor do *payoff* de $T_2$ pela taxa flutuante realizada no período.
* **Rate Delta ($\frac{\partial V_0}{\partial K}$):** Medida de sensibilidade do valor presente do FRA em relação a variações na taxa fixa contratada $K$.

---

### Questões de Prática e Avaliação

#### Nível 1 Respostas Curtas

1. Qual é a principal diferença conceitual entre o fator de desconto no modelo de Black-Scholes tradicional e no mercado de renda fixa?
2. Como se define a taxa de exercício ao par ($K^*$) de um FRA em um contexto determinístico de curva única?
3. Por que a liquidação financeira de muitos contratos FRA de mercado é realizada na data $T_1$ e não em $T_2$?

#### Nível 2 Questões Práticas / Numéricas

4. Dados os fatores de desconto $P(0; 0{,}5) = 0{,}9900$ e $P(0; 1{,}0) = 0{,}9750$, e considerando a fração de ano $\Delta = 0{,}5$, calcule a taxa *forward* simples $L(0; 0{,}5; 1{,}0)$.
5. Considere um FRA sobre um nocional de $R\$ 20.000.000$, para o período entre $T_1 = 1{,}0$ e $T_2 = 1{,}5$ ($\Delta = 0{,}5$). Sabendo que $P(0; 1{,}5) = 0{,}9600$, a taxa *forward* do mercado é $3{,}125\%$ ao ano e a taxa fixa acordada no contrato foi $K = 2{,}125\%$ ao ano, determine o valor presente líquido $V_0$ do contrato para a ponta que recebe a taxa flutuante e paga a taxa fixa.

#### Nível 3 Análise Profunda e Dissertativa

6. Demonstre matematicamente como a expressão do valor presente de um FRA fora do mercado $V_0 = N P(0,T_2)\Delta (L(0;T_1,T_2)-K)$ pode ser reescrita na forma de uma replicação por carteira contendo exclusivamente fatores de desconto. Explique o significado econômico de cada termo da equação resultante.
7. Explique o conceito de taxas *forward* negativas no contexto da relação entre $P(0,T_1)$ e $P(0,T_2)$. O que a ocorrência de uma taxa *forward* negativa reflete em termos de expectativas econômicas e preços de mercado?

---

### Gabarito e Respostas Comentadas

#### Resposta da Questão 1
No modelo de Black-Scholes tradicional, assume-se uma taxa livre de risco constante $r$, gerando um fator de desconto da forma $e^{-rT}$ dependente de um único parâmetro. No mercado de renda fixa, substitui-se o parâmetro constante por uma função completa de fatores de desconto $P(0,T)$, onde cada maturidade possui seu próprio preço de desconto determinado diretamente pelo mercado.

#### Resposta da Questão 2
A taxa ao par $K^*$ é a taxa fixa que torna o valor presente líquido do FRA igual a zero na data de celebração do contrato ($t=0$). No ambiente determinístico de curva única, $K^*$ é exatamente igual à taxa *forward* simples $L(0;T_1,T_2)$ derivada da curva de fatores de desconto de mercado.

#### Resposta da Questão 3
A liquidação em $T_1$ é adotada como convenção de mercado para antecipar o pagamento do ajuste financeiro para o início do período do empréstimo subjacente, reduzindo o risco de crédito de contraparte entre $T_1$ e $T_2$.

#### Resposta da Questão 4
Aplica-se a fórmula da taxa *forward* simples:
$$L(0; 0{,}5; 1{,}0) = \frac{1}{0{,}5} \left( \frac{P(0; 0{,}5)}{P(0; 1{,}0)} - 1 \right) = 2 \times \left( \frac{0{,}9900}{0{,}9750} - 1 \right)$$
$$L(0; 0{,}5; 1{,}0) = 2 \times (1{,}0153846 - 1) = 2 \times 0{,}0153846 = 0{,}030769 \text{ ou } 3{,}077\% \text{ ao ano.}$$

#### Resposta da Questão 5
Aplica-se a fórmula do valor presente $V_0$:
$$V_0 = N \cdot P(0; 1{,}5) \cdot \Delta \cdot (L_0 - K)$$
$$V_0 = 20.000.000 \times 0{,}9600 \times 0{,}5 \times (0{,}03125 - 0{,}02125)$$
$$V_0 = 9.600.000 \times 0{,}0100 = R\$ 96.000$$
Como a taxa fixa do contrato ($2{,}125\%$) está abaixo da taxa *forward* do mercado ($3{,}125\%$), a posição que paga a taxa fixa e recebe a taxa flutuante possui um valor presente positivo de $R\$ 96.000$.

#### Resposta da Questão 6
Partindo de $V_0 = N P(0,T_2)\Delta (L(0;T_1,T_2)-K)$, substitui-se a definição da taxa *forward*:
$$\Delta L(0;T_1,T_2) = \frac{P(0,T_1)}{P(0,T_2)} - 1 \implies P(0,T_2)\Delta L(0;T_1,T_2) = P(0,T_1) - P(0,T_2)$$
Multiplicando e distribuindo a equação do $V_0$:
$$V_0 = N \left[ P(0,T_2)\Delta L(0;T_1,T_2) - P(0,T_2)\Delta K \right]$$
$$V_0 = N \left[ (P(0,T_1) - P(0,T_2)) - P(0,T_2)\Delta K \right]$$

**Significado Econômico:**
* O termo $N(P(0,T_1) - P(0,T_2))$ representa a carteira de replicação exata do fluxo flutuante do FRA: equivale a comprar hoje um título de valor unitário com maturidade em $T_1$ e vender um título com maturidade em $T_2$.
* O termo $-N P(0,T_2)\Delta K$ representa o valor presente do compromisso fixo assumido de pagar a taxa $K$ sobre a fração $\Delta$ no momento $T_2$.

#### Resposta da Questão 7
Uma taxa *forward* simples $L(0;T_1,T_2)$ torna-se negativa quando a curva de desconto apresenta um fator de desconto para uma maturidade mais longa maior do que o fator de desconto para uma maturidade mais curta, ou seja, $P(0,T_2) > P(0,T_1)$. 

Do ponto de vista econômico, isso significa que 1 unidade monetária entregue na data mais distante $T_2$ vale mais hoje do que 1 unidade monetária entregue na data mais próxima $T_1$. Isso reflete uma precificação de mercado onde o rendimento do mercado monetário simples para o período futuro $[T_1, T_2]$ é estritamente negativo, impondo um custo para armazenar valor ou manter depósitos ao longo desse intervalo específico.