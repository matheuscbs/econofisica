<!-- imported from vault study notes; curated for open course -->
# M03.A02 — Swaps de juros: precificar o instrumento padrão de taxa

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M03
> **Aula:** M03.A02

↑ M03 · Resumo · Completo

**Módulo:** M03
**Pergunta do módulo:** Como montar curva de juros e precificar taxa sem arbitragem?

## Conceito-núcleo
IRS como troca fixed↔floating; valuation via curva de desconto e forward floating.

## Aplicação em mercado / trading
Marcar IRS, DV01 e sensibilidade a shifts de curva; base para hedge de duration.

## Entregável / lab
Precificar um swap plain vanilla com curva flat/bootstrap e reportar PV + DV01.

## Fonte (mapeamento)
quantitative-trading-free-lesson/10 pricing-interest-rate-swaps

## Guia de estudo aprofundado

> **info**
>

Este guia de estudos destina-se à consolidação dos conceitos de precificação de instrumentos padrão de taxa de juros, focando na dinâmica de *swaps* pré-fixados por flutuantes (*vanilla interest rate swaps*), mensuração de valor presente ($PV$), cálculo da taxa par ($K^*$), anuidade ($A$), sensibilidade ($PV01$) e a mecânica das pernas fixa e flutuante.

---

### Conceitos Fundamentais e Formulação Matemática

#### A Curva de Desconto e as Taxas Forward
Toda a estrutura de precificação de renda fixa decorre de uma tabela de fatores de desconto $P(0, T)$, que representa o preço hoje ($t=0$) de um fluxo de caixa unitário ($1.0$) a ser recebido no futuro ($T$). 

A partir da curva $P(0,T)$, a taxa *forward* simples $L(0; T_1, T_2)$ para o período $[T_1, T_2]$ é estritamente determinada pela condição de não arbitragem:

$$1 + L(0; T_1, T_2) \Delta = \frac{P(0, T_1)}{P(0, T_2)}$$

Isolando a taxa *forward* simples:

$$L(0; T_1, T_2) = \frac{1}{\Delta} \left( \frac{P(0, T_1)}{P(0, T_2)} - 1 \right)$$

onde $\Delta$ representa a fração de ano ou fator de acrual do período.

#### O Contrato FRA (Forward Rate Agreement)
O FRA é o bloco construtor básico de um *swap*. Um FRA fixa uma taxa de juros $K$ sobre o intervalo $[T_1, T_2]$. No momento de ajuste ($T_1$), observa-se a taxa flutuante $L(T_1; T_1, T_2)$. O pagamento ocorre no vencimento ($T_2$), com o seguinte *payoff*:

$$\text{Payoff}_{T_2} = N \Delta \left( L(T_1; T_1, T_2) - K \right)$$

Descontando esse fluxo para o instante inicial ($t=0$) pela mesma curva de desconto $P(0, T)$, o valor presente do FRA é:

$$V_0 = N P(0, T_2) \Delta \left( L(0; T_1, T_2) - K \right)$$

#### Estrutura e Cronograma do Swap
Um *swap* de taxa de juros estende o conceito do FRA para uma sequência de datas e fluxos de caixa definidos por um cronograma (*schedule*):

$$T_0 < T_1 < \dots < T_n$$

dividindo o tempo em intervalos $[T_{0}, T_1], [T_1, T_2], \dots, [T_{n-1}, T_n]$, onde cada período $i$ possui uma fração de ano $\Delta_i$.

#### Perna Fixa (Fixed Leg)
A perna fixa paga, em cada data $T_i$, um cupom fixo conhecido desde o início:

$$CF_{\text{fixed}}(T_i) = N K \Delta_i$$

O valor presente da perna fixa ($PV_{\text{fixed}}$) é a soma dos cupons fixos descontados:

$$PV_{\text{fixed}} = \sum_{i=1}^{n} P(0, T_i) N K \Delta_i = N K \sum_{i=1}^{n} \Delta_i P(0, T_i)$$

Define-se a **Anuidade** ($A$) como a soma ponderada dos fatores de desconto pelos fatores de acrual:

$$A = \sum_{i=1}^{n} \Delta_i P(0, T_i)$$

Portanto, a perna fixa pode ser expressa de forma simplificada como:

$$PV_{\text{fixed}} = N K A$$

#### Perna Flutuante (Floating Leg)
A perna flutuante paga, em cada data $T_i$, um valor atrelado à taxa flutuante observada no início do período (reset em $T_{i-1}$):

$$CF_{\text{float}}(T_i) = N \Delta_i L(T_{i-1}; T_{i-1}, T_i)$$

Um *swap* flutuante é conceitualmente um conjunto (*strip*) de FRAs sequenciais. Em um ambiente de curva única (*single-curve*), a precificação da perna flutuante beneficia-se de uma propriedade telescópica:

$$P(0, T_i) \Delta_i L(0; T_{i-1}, T_i) = P(0, T_{i-1}) - P(0, T_i)$$

Ao somar esses termos ao longo de todos os períodos $i = 1, \dots, n$, todos os termos intermediários se cancelam em cadeia:

$$\sum_{i=1}^{n} P(0, T_i) \Delta_i L(0; T_{i-1}, T_i) = P(0, T_0) - P(0, T_n)$$

Assim, o valor presente da perna flutuante resulta em:

$$PV_{\text{float}} = N \left( P(0, T_0) - P(0, T_n) \right)$$

No caso de um *swap* com início imediato (*spot-start*), onde $T_0 = 0$ e $P(0, 0) = 1$:

$$PV_{\text{float}} = N \left( 1 - P(0, T_n) \right)$$

#### Taxa Par (Par Swap Rate) e Valor do Swap
Para um *payer swap* (pagador da perna fixa e recebedor da perna flutuante), o valor presente líquido do instrumento é:

$$PV_{\text{swap}} = PV_{\text{float}} - PV_{\text{fixed}}$$

A taxa par ($K^*$) é definida como a taxa fixa $K$ que iguala o valor presente da perna fixa ao da perna flutuante, tornando o valor inicial do *swap* nulo ($PV_{\text{swap}} = 0$):

$$N \left( P(0, T_0) - P(0, T_n) \right) = N K^* A$$

$$K^* = \frac{P(0, T_0) - P(0, T_n)}{A} = \frac{P(0, T_0) - P(0, T_n)}{\sum_{i=1}^{n} \Delta_i P(0, T_i)}$$

Para um *swap* negociado fora das condições de mercado (*off-market*) com uma taxa $K$ arbitrária, o valor presente é expresso diretamente em relação à taxa par:

$$PV_{\text{swap}} = N \left( P(0, T_0) - P(0, T_n) \right) - N K A = N A (K^* - K)$$

* Se $K > K^*$: a taxa paga é superior à taxa par de mercado, gerando um $PV_{\text{swap}}$ negativo para o pagador da perna fixa.
* Se $K < K^*$: a taxa paga é inferior à taxa par de mercado, gerando um $PV_{\text{swap}}$ positivo para o pagador da perna fixa.

#### Métrica de Sensibilidade PV01
A sensibilidade do valor do *swap* em relação a mudanças na taxa fixa $K$ é dada pela derivada:

$$\frac{\partial PV_{\text{swap}}}{\partial K} = -N A$$

O **PV01** (ou valor presente de um ponto base) mede a variação no valor do *swap* para uma mudança de $1$ ponto base ($0,01\%$ ou $10^{-4}$) na taxa fixa $K$:

$$PV01 \approx N A \times 10^{-4}$$

#### Abordagem Single-Curve vs. Multi-Curve
* **Single-Curve**: A mesma curva $P(0,T)$ é utilizada tanto para projetar as taxas *forward* flutuantes quanto para descontar os fluxos de caixa a valor presente. Isso permite o cancelamento telescópico exato da perna flutuante.
* **Multi-Curve**: As taxas flutuantes são projetadas por uma curva específica (ex: IBOR), enquanto o desconto é realizado por uma curva livre de risco baseada em OIS (*Overnight Index Swaps*). Nesse contexto, o atalho do cancelamento telescópico $P(0, T_0) - P(0, T_n)$ não se aplica exatamente, sendo necessário projetar cada taxa *forward* e descontá-la individualmente.

---

### Intuição de Mercado e Trading

1. **A Máquina de Fluxos de Caixa**: Diferente do modelo de Movimento Browniano Geométrico (GBM) para ações, um instrumento de renda fixa não é um preço flutuando no espaço, mas sim uma máquina geradora de fluxos de caixa em datas predeterminadas. O papel da curva $P(0,T)$ é unicamente trazer esses fluxos futuros ao valor de hoje.
2. **Payer vs. Receiver Swap**:
   * **Payer Swap**: Paga taxa fixa e recebe taxa flutuante. É equivalente a estar vendida em taxa fixa (se as taxas subirem, o valor do contrato aumenta, pois $K^*$ sobe em relação ao $K$ contratado).
   * **Receiver Swap**: Recebe taxa fixa e paga taxa flutuante. É equivalente a estar comprada em taxa fixa (se as taxas caírem, o valor do contrato aumenta).
3. **Significado Físico da Anuidade ($A$)**: A anuidade representa a dimensão financeira da perna fixa por unidade de taxa. O $PV01$ é a materialização direta dessa dimensão: aumentar $K$ em $1$ ponto base desloca o $PV$ do *swap* em aproximadamente $N A \times 10^{-4}$.

---

### Exemplo Numérico Passo a Passo

Considere um *swap* com as seguintes características:
* Notional ($N$): $\$ 10.000.000$
* Início ($T_0$): $0,0$ anos
* Vencimento ($T_n$): $5,0$ anos
* Pagamentos: Semestrais ($\Delta_i = 0,5$ para $i=1, \dots, 10$)
* Grade da Curva de Desconto ($T_{\text{grid}}$ e $P_{\text{grid}}$):

| $T$ (Anos) | $P(0, T)$ |
| :--- | :--- |
| $0,0$ | $1,0000$ |
| $0,5$ | $0,9900$ |
| $1,0$ | $0,9750$ |
| $2,0$ | $0,9450$ |
| $3,0$ | $0,9100$ |
| $5,0$ | $0,8500$ |

O método de interpolação utilizado para pontos intermediários é a **interpolação log-linear** nos fatores de desconto:

$$\ln P(0, x) = \text{interpolação linear de } \ln P_{\text{grid}} \text{ em relação a } T_{\text{grid}}$$

#### Passo 1 Obtenção dos Fatores de Desconto $P(0, T_i)$
Aplicando a interpolação log-linear para as datas de pagamento semestrais:
* $P(0; 0,5) = 0,990000$
* $P(0; 1,0) = 0,975000$
* $P(0; 1,5) = \exp \left( 0,5 \times (\ln 0,9750 + \ln 0,9450) \right) \approx 0,959883$
* $P(0; 2,0) = 0,945000$
* $P(0; 2,5) = \exp \left( 0,5 \times (\ln 0,9450 + \ln 0,9100) \right) \approx 0,927335$
* $P(0; 3,0) = 0,910000$
* $P(0; 3,5) = \exp \left( \ln 0,9100 + 0,25 \times (\ln 0,8500 - \ln 0,9100) \right) \approx 0,894611$
* $P(0; 4,0) = \exp \left( \ln 0,9100 + 0,50 \times (\ln 0,8500 - \ln 0,9100) \right) \approx 0,879489$
* $P(0; 4,5) = \exp \left( \ln 0,9100 + 0,75 \times (\ln 0,8500 - \ln 0,9100) \right) \approx 0,864614$
* $P(0; 5,0) = 0,850000$

Soma dos fatores de desconto:

$$\sum_{i=1}^{10} P(0, T_i) \approx 9,195932$$

#### Passo 2 Cálculo da Anuidade ($A$)
Como $\Delta_i = 0,5$ para todos os períodos:

$$A = \sum_{i=1}^{10} \Delta_i P(0, T_i) = 0,5 \times 9,195932 = 4,597966$$

#### Passo 3 Cálculo da Taxa Par ($K *$)
Usando $P(0, T_0) = 1,0$ e $P(0, T_n) = 0,8500$:

$$K^* = \frac{P(0, T_0) - P(0, T_n)}{A} = \frac{1,0 - 0,8500}{4,597966} = \frac{0,1500}{4,597966} \approx 0,0326231 \quad (3,26231\% \text{ ao ano})$$

#### Passo 4 Precificação da Perna Flutuante ($PV_{\text{float}}$)
Em forma fechada (single-curve):

$$PV_{\text{float}} = N \left( P(0, T_0) - P(0, T_n) \right) = 10.000.000 \times (1,0 - 0,8500) = \$ 1.500.000,00$$

#### Passo 5 Precificação de um Swap Off-Market
Assuma uma taxa contratada $K = K^* + 0,005$ ($50$ bps acima da taxa par, ou seja, $K = 0,0376231$):

$$PV_{\text{fixed}} = N K A = 10.000.000 \times 0,0376231 \times 4,597966 \approx \$ 1.729.898,30$$

Para um *payer swap*:

$$PV_{\text{swap}} = PV_{\text{float}} - PV_{\text{fixed}} = 1.500.000,00 - 1.729.898,30 = -\$ 229.898,30$$

Alternativamente, via fórmula direta:

$$PV_{\text{swap}} = N A (K^* - K) = 10.000.000 \times 4,597966 \times (-0,005) = -\$ 229.898,30$$

#### Passo 6 Cálculo do PV01 e Teste de Choque de 1 bp
$$PV01 = N A \times 10^{-4} = 10.000.000 \times 4,597966 \times 10^{-4} = \$ 4.597,97$$

Se aumentarmos a taxa $K$ em $1$ bp ($K_{\text{up}} = K + 0,0001$):

$$PV_{\text{swap\_up}} = PV_{\text{float}} - N (K + 0,0001) A$$

$$PV_{\text{swap\_up}} - PV_{\text{swap}} = -N A \times 10^{-4} = -\$ 4.597,97$$

O choque numérico corrobora exatamente a magnitude teórica do $PV01$.

---

### Armadilhas Comuns

1. **Premissas Multi-Curve em Fórmulas Single-Curve**: Tratar $PV_{\text{float}} = N(P(0, T_0) - P(0, T_n))$ como uma verdade universal. Essa identidade falha em estruturas *multi-curve*, onde a projeção da taxa e o desconto utilizam curvas distintas.
2. **Inversão de Sinal entre Payer e Receiver**: Esquecer que o *payer swap* assume posição comprada na perna flutuante e vendida na perna fixa ($PV = PV_{\text{float}} - PV_{\text{fixed}}$). Se $K > K^*$, o valor do *payer swap* deve ser negativo.
3. **Erros na Fração de Ano ($\Delta_i$)**: Tratar a anuidade como simples soma dos fatores de desconto ($\sum P(0, T_i)$), esquecendo de multiplicar cada termo pela sua respectiva fração de ano $\Delta_i$.
4. **Confusão do Conceito de PV01**: Confundir um choque na taxa de cupom contratada $K$ (métrica estática de sensibilidade do contrato) com um choque paralelo na curva de juros inteira. O $PV01$ discutido aqui é a sensibilidade do $PV$ com relação a $K$.

---

### Laboratório Prático em Python

Abaixo descreve-se o roteiro para implementação do script de precificação de *swaps* em Python, reproduzindo a mecânica analítica.

#### Passo 1 Definir o Cronograma e o Notional
* Definir o início $T_0 = 0.0$ e os vencimentos semestrais até 5 anos via `np.arange(0.5, 5.0 + 0.5, 0.5)`.
* Criar o vetor de frações de ano $\Delta$ preenchido com $0.5$.
* Definir o valor do notional $N = 10.000.000$.

#### Passo 2 Construir a Curva de Desconto com Interpolação Log-Linear
* Definir os vetores `T_grid` e `P_grid`.
* Criar uma função `P0(x)` que extrai o logaritmo natural de `P_grid`, realiza interpolação linear via `np.interp` para a maturidade $x$, e retorna o valor exponencial do resultado ($\exp$).

#### Passo 3 Avaliar os Fatores de Desconto nas Datas do Swap
* Gerar o vetor `P_T` aplicando `P0` a cada data de pagamento do cronograma.
* Armazenar $P(0, T_0)$ em `P_T0` e $P(0, T_n)$ em `P_Tn`.

#### Passo 4 Calcular Anuidade e Taxa Par
* Calcular a anuidade $A = \text{sum}(\Delta \times P\_T)$.
* Obter a taxa par $K^* = (P\_T0 - P\_Tn) / A$.

#### Passo 5 Precificar Perna Fixa, Perna Flutuante e Valor Líquido
* Definir uma taxa *off-market* $K = K^* + 0,005$.
* Calcular $PV_{\text{float\_closed}} = N \times (P\_T0 - P\_Tn)$.
* Calcular $PV_{\text{fixed}} = N \times K \times A$.
* Obter $PV_{\text{swap}} = PV_{\text{float\_closed}} - PV_{\text{fixed}}$.

#### Passo 6 Reconstruir a Perna Flutuante via Strip de FRAs
* Construir o vetor de datas de início de período `T_prev` concatenando $[T_0]$ com as datas $T[:-1]$.
* Obter os fatores de desconto das datas anteriores `P_prev`.
* Calcular as taxas *forward* simples $L_i = ((P\_prev / P\_T) - 1.0) / \Delta$.
* Calcular o valor presente da perna flutuante via soma dos minicontratos FRA: $PV_{\text{float\_strip}} = \text{sum}(N \times P\_T \times \Delta \times L_i)$.
* Verificar se a diferença `PV_float_strip - PV_float_closed` é estritamente zero (dentro da precisão de ponto flutuante).

#### Passo 7 Validar o PV01 via Choque Numérico
* Calcular $PV01 = N \times A \times 1e-4$.
* Reprecificar o *swap* com taxa $K + 1e-4$ para obter $PV_{\text{swap\_up}}$.
* Verificar se $PV_{\text{swap\_up}} - PV_{\text{swap}}$ é equivalente a $-PV01$.

---

### Glossário

* **Anuidade ($A$)**: Soma dos fatores de desconto das datas de pagamento de um *swap*, ponderados pelas respectivas frações de ano. Representa o valor presente de um cupom fixo de $100\%$ ($1,0$).
* ** FRA (Forward Rate Agreement)**: Contrato a termo sobre taxa de juros no qual as partes travam uma taxa fixa para um período futuro específico.
* **Interpolação Log-Linear**: Técnica de interpolação onde assume-se variação linear sobre o logaritmo dos fatores de desconto ($\ln P(0, T)$), garantindo curvas de juros contínuas e sem arbitragem.
* **Multi-Curve**: Estrutura de apreçamento em que a curva usada para projetar as taxas flutuantes futuras difere da curva usada para descontar os fluxos de caixa a valor presente.
* **Payer Swap**: Posição em um *swap* na qual se paga a perna fixa e se recebe a perna flutuante.
* **PV01 (Present Value of a Basis Point)**: Variação monetária no valor presente de uma posição decorrente da alteração de $1$ ponto base ($0,01\%$) na taxa fixa de referência.
* **Receiver Swap**: Posição em um *swap* na qual se recebe a perna fixa e se paga a perna flutuante.
* **Single-Curve**: Estrutura de apreçamento que utiliza exatamente a mesma curva de fatores de desconto $P(0, T)$ tanto para a projeção das taxas flutuantes quanto para o desconto dos fluxos de caixa.
* **Taxa Par ($K^*$)**: A taxa de cupom fixo que iguala o valor presente da perna fixa ao valor presente da perna flutuante, resultando em um valor presente líquido de mercado igual a zero no início do contrato.

---

### Questões de Prática e Respostas

#### Nível 1 Introdução e Conceitos Básicos

##### Questão 1.1
Qual é a definição de taxa par ($K^*$) em um *swap* de taxa de juros pré-fixado por flutuante?
* (A) A taxa fixa que maximiza o lucro da instituição financeira na estruturação.
* (B) A taxa média histórica das taxas flutuantes do mercado nos últimos 12 meses.
* (C) A taxa fixa que iguala os valores presentes das pernas fixa e flutuante, tornando o valor presente líquido do *swap* igual a zero na origem.
* (D) A taxa que resulta da soma de todos os fatores de desconto da curva $P(0,T)$.

**Resposta:** (C). A taxa par é a taxa de cupom fixa que equilibra perfeitamente os valores presentes de ambas as pernas, zerando o valor inicial do instrumento ($PV_{\text{swap}} = 0$).

##### Questão 1.2
Em um *payer swap*, o participante do mercado assume qual estrutura de pagamentos?
* (A) Paga a taxa flutuante e recebe a taxa fixa.
* (B) Paga a taxa fixa e recebe a taxa flutuante.
* (C) Paga a taxa fixa e recebe o principal corrigido pela inflação.
* (D) Paga o $PV01$ e recebe a anuidade.

**Resposta:** (B). O "Payer" em um *swap* refere-se expressamente ao pagador da perna fixa e recebedor da perna flutuante.

---

#### Nível 2 Aplicação e Cálculos Intermediários

##### Questão 2.1
Considere um *swap* de 1 ano com pagamentos semestrais ($\Delta_1 = \Delta_2 = 0,5$). Os fatores de desconto da curva são $P(0; 0,5) = 0,9800$ e $P(0; 1,0) = 0,9500$. Qual é o valor da anuidade $A$ e da taxa par $K^*$ deste *swap*?

**Resposta:**
1. **Cálculo da Anuidade ($A$)**:
   $$A = \sum_{i=1}^{2} \Delta_i P(0, T_i) = 0,5 \times 0,9800 + 0,5 \times 0,9500 = 0,4900 + 0,4750 = 0,9650$$

2. **Cálculo da Taxa Par ($K^*$)**:
   Assumindo início imediato ($P(0, T_0) = 1,0$):
   $$K^* = \frac{P(0, T_0) - P(0, T_2)}{A} = \frac{1,0 - 0,9500}{0,9650} = \frac{0,0500}{0,9650} \approx 0,051813 \quad (5,1813\% \text{ a.a.})$$

##### Questão 2.2
Se um trader entra em uma posição *payer swap* com notional de $\$ 20.000.000$ e anuidade $A = 3,8$, qual é o $PV01$ dessa posição? Se a taxa fixa contratada $K$ estiver $10$ bps acima da taxa par $K^*$, qual é o valor presente líquido ($PV$) do *swap*?

**Resposta:**
1. **Cálculo do $PV01$**:
   $$PV01 = N \times A \times 10^{-4} = 20.000.000 \times 3,8 \times 10^{-4} = \$ 7.600,00$$

2. **Cálculo do $PV$**:
   Se $K = K^* + 0,0010$ (10 bps acima da taxa par), temos $(K^* - K) = -0,0010$:
   $$PV_{\text{swap}} = N \times A \times (K^* - K) = 20.000.000 \times 3,8 \times (-0,0010) = -\$ 76.000,00$$

---

#### Nível 3 Análise Avançada e Derivações

##### Questão 3.1
Demonstre matematicamente por que, em um ambiente de curva única (*single-curve*), o valor presente da perna flutuante de um *swap* de $n$ períodos simplifica-se para $PV_{\text{float}} = N(P(0, T_0) - P(0, T_n))$.

**Resposta:**
Em cada período $i \in [1, n]$, o fluxo de caixa da perna flutuante é $CF(T_i) = N \Delta_i L(0; T_{i-1}, T_i)$.
A taxa *forward* simples $L(0; T_{i-1}, T_i)$ é definida de forma a não permitir arbitragem por:

$$1 + \Delta_i L(0; T_{i-1}, T_i) = \frac{P(0, T_{i-1})}{P(0, T_i)}$$

Multiplicando ambos os lados por $P(0, T_i)$:

$$P(0, T_i) + P(0, T_i) \Delta_i L(0; T_{i-1}, T_i) = P(0, T_{i-1})$$

Isolando o termo descontado da perna flutuante:

$$P(0, T_i) \Delta_i L(0; T_{i-1}, T_i) = P(0, T_{i-1}) - P(0, T_i)$$

O valor presente total da perna flutuante é a soma descontada desses fluxos para $i=1$ até $n$:

$$PV_{\text{float}} = N \sum_{i=1}^{n} P(0, T_i) \Delta_i L(0; T_{i-1}, T_i) = N \sum_{i=1}^{n} \left( P(0, T_{i-1}) - P(0, T_i) \right)$$

Expandindo a soma:

$$PV_{\text{float}} = N \left[ (P(0, T_0) - P(0, T_1)) + (P(0, T_1) - P(0, T_2)) + \dots + (P(0, T_{n-1}) - P(0, T_n)) \right]$$

Trata-se de uma soma telescópica na qual todos os termos intermediários $P(0, T_1), P(0, T_2), \dots, P(0, T_{n-1})$ se cancelam mutuamente.
Restam apenas os termos limite, resultando em:

$$PV_{\text{float}} = N \left( P(0, T_0) - P(0, T_n) \right)$$

##### Questão 3.2
Por que a fórmula simplificada $PV_{\text{float}} = N(P(0, T_0) - P(0, T_n))$ deixa de ser válida em uma arquitetura de apreçamento *multi-curve*?

**Resposta:**
Em uma arquitetura *multi-curve*, existem duas curvas distintas:
1. A curva de **projeção** (ex: Libor/Euribor), usada para determinar as taxas *forward* $L(0; T_{i-1}, T_i) = \frac{1}{\Delta_i} \left( \frac{P_{\text{proj}}(0, T_{i-1})}{P_{\text{proj}}(0, T_i)} - 1 \right)$.
2. A curva de **desconto** (ex: OIS), usada para trazer os fluxos a valor presente utilizando $P_{\text{disc}}(0, T_i)$.

O termo a ser somado no valor presente torna-se:

$$PV_{\text{termo } i} = N \cdot P_{\text{disc}}(0, T_i) \cdot \Delta_i \cdot \frac{1}{\Delta_i} \left( \frac{P_{\text{proj}}(0, T_{i-1})}{P_{\text{proj}}(0, T_i)} - 1 \right) = N \cdot P_{\text{disc}}(0, T_i) \left( \frac{P_{\text{proj}}(0, T_{i-1})}{P_{\text{proj}}(0, T_i)} - 1 \right)$$

Como $P_{\text{disc}}(0, T_i) \neq P_{\text{proj}}(0, T_i)$, o fator $P_{\text{disc}}(0, T_i)$ não simplifica o denominador de projeção $P_{\text{proj}}(0, T_i)$. Consequentemente, o cancelamento telescópico em cadeia deixa de ocorrer, sendo exigida a projeção e o desconto individual de cada fluxo de caixa da perna flutuante.