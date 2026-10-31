<!-- imported study note (guia-completo.md) -->
# Relatório Técnico Executivo: Módulo M03 — Curva de Juros e Produtos de Taxa: Forwards Sem Arbitragem, Swaps e Opções de Taxa

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M03

↑ M03 · Resumo · Completo

---

## Executive Summary

Este documento constitui a síntese técnica do Módulo M03 do curso de Econofísica da Khem Kapital. O objetivo principal deste relatório é apresentar uma análise rigorosa e exaustiva da matemática financeira subjacente à construção de curvas de juros, apreçamento de derivativos de taxa de juro e modelagem de volatilidade estocástica e áspera (*rough volatility*).

A análise abrange desde as definições fundamentais de fatores de desconto e taxas zero/forward até os métodos avançados de interpolação não linear — com ênfase no método **Monotone Convex** de Hagan e West. O relatório examina a transição histórica para o paradigma **multi-curva** pós-crise de 2007-2008, detalhando a mecânica do *bootstrap* de instrumentos de mercado (depósitos, FRAs e swaps) e a avaliação do risco de taxa por meio da sensibilidade local e *key rate durations*.

Na esfera da precificação de opções de taxa de juros e derivativos estruturados (caps, floors, swaptions), explora-se a transição da precificação lognormal clássica de Black-76 para o modelo normal de Bachelier (essencial em ambientes de taxas de juros negativas ou próximas de zero). Por fim, apresenta-se a extensão do modelo SABR clássico para o **Rough SABR** (Fukasawa e Gatheral), derivando a equação diferencial ordinária (ODE) para o *smile* de volatilidade normalizado sob rugosidade estocástica (parâmetro de Hurst $H \in (0, 1/2]$) e demonstrando como essa estrutura parametriza e prepara a superfície de volatilidade para o Módulo M04.

---

## 1. Fatores de Desconto, Taxas Zero, Forward e Composição

O alicerce da matemática de renda fixa baseia-se na avaliação do valor do dinheiro no tempo por meio do **fator de desconto** $P(0, t)$, definido como o valor presente no instante $t=0$ de uma unidade monetária ($1,00$) a ser recebida na data futura $t$. A função de desconto $t \mapsto P(0, t)$ é estritamente decrescente em ambientes de taxas de juros nominais positivas, refletindo a propriedade $P(0, 0) = 1$ e $\lim_{t \to \infty} P(0, t) = 0$.

### 1.1 Convenções de Composição e Relações Matemáticas

A relação entre o fator de desconto $P(0, t)$ e a taxa spot (ou taxa zero) $r(t)$ depende da convenção de composição temporal adotada:

*   **Composição Simples (*Simple Rate*):** Utilizada em mercados de curto prazo e depósitos do mercado monetário. O montante acumulado $B_N$ para um capital $B_0$ aplicado por $t$ anos é dado por:
    $$B_N = B_0 \cdot (1 + r_{\text{simple}} \cdot t)$$
    O fator de desconto equivalente é:
    $$P(0, t) = \frac{1}{1 + r_{\text{simple}} \cdot t}$$

*   **Composição Anual (*Annually Compounded Rate*):**
    $$P(0, t) = \frac{1}{(1 + r_1(t))^t} \implies r_1(t) = P(0, t)^{-1/t} - 1$$

*   **Composição Periódica (*Sub-annual Compounding*):** Para $f$ pagamentos por ano (ex.: $f=2$ para semestral, $f=4$ para trimestral):
    $$(1 + r_{\text{annual}})^t = \left( 1 + \frac{r_f(t)}{f} \right)^{f \cdot t}$$

*   **Composição Contínua (*Continuously Compounded Rate - NACC*):** É a convenção padrão na modelagem analítica e em econofísica:
    $$P(0, t) = \exp(-r(t) \cdot t) \implies r(t) = -\frac{1}{t} \ln P(0, t)$$
    O fator de capitalização $C(0, t)$ é o inverso exato do fator de desconto:
    $$C(0, t) = \frac{1}{P(0, t)} = \exp(r(t) \cdot t)$$

### 1.2 Taxas Forward Discretas e Instantâneas

A taxa *forward* representa a taxa de juros acertada no instante presente para um empréstimo ou investimento que ocorrerá entre duas datas futuras $t_1$ e $t_2$ ($0 \le t_1 < t_2$). Pela ausência de arbitragem, o fator de desconto *forward* $P(0; t_1, t_2)$ deve satisfazer a relação de consistência temporal:
$$P(0, t_1) \cdot P(t_1, t_2) = P(0, t_2) \implies P(t_1, t_2) = \frac{P(0, t_2)}{P(0, t_1)}$$

Sob composição contínua, a taxa *forward* discreta $f(t_1, t_2)$ expressa-se como:
$$P(t_1, t_2) = \exp\left( -f(t_1, t_2) \cdot (t_2 - t_1) \right)$$
$$f(t_1, t_2) = \frac{-\ln P(0, t_2) - (-\ln P(0, t_1))}{t_2 - t_1} = \frac{r(t_2) \cdot t_2 - r(t_1) \cdot t_1}{t_2 - t_1}$$

Tomando o limite quando $t_2 \to t_1 = t$, obtém-se a **taxa forward instantânea** $f(t)$:
$$f(t) = -\frac{d}{dt} \ln P(0, t) = \frac{d}{dt} \left( r(t) \cdot t \right) = r(t) + r'(t) \cdot t$$

A integração da taxa *forward* instantânea permite recuperar a taxa zero $r(t)$ e a função de desconto $P(0, t)$:
$$r(t) \cdot t = \int_0^t f(s) \, ds \implies P(0, t) = \exp\left( -\int_0^t f(s) \, ds \right)$$

Existe uma paridade exata entre a taxa *forward* discreta no intervalo $[t_{i-1}, t_i]$ e a média da taxa *forward* instantânea sobre esse mesmo intervalo:
$$\frac{r_i \cdot t_i - r_{i-1} \cdot t_{i-1}}{t_i - t_{i-1}} = \frac{1}{t_i - t_{i-1}} \int_{t_{i-1}}^{t_i} f(s) \, ds$$

---

## 2. Forwards por No-Arbitrage e Forward Rate Agreements (FRA)

### 2.1 Relação de Não Arbitragem e Precificação Forward

A precificação de qualquer instrumento *forward* baseia-se na replicação por arbitragem ("carregar e financiar" ou *cash-and-carry*). Se um agente deseja fixar hoje a taxa de retorno para o período $[t_1, t_2]$, ele pode simultaneamente comprar um título com vencimento em $t_2$ e vender (emitir) um título com vencimento em $t_1$. O fluxo de caixa líquido no instante inicial $t=0$ é zero se as proporções forem ajustadas corretamente, garantindo que a taxa resultante seja rigorosamente $f(t_1, t_2)$.

### 2.2 Estrutura e Mecânica do FRA (*Forward Rate Agreement*)

Um *Forward Rate Agreement* (FRA) é um contrato derivativo do mercado de balcão (*OTC*) no qual duas partes concordam com uma taxa de juros fixa ($R_{\text{FRA}}$) a ser aplicada sobre um valor notocional $N$ durante um período futuro definido entre a data de liquidação $t_1$ e a data de vencimento $t_2$ ($\tau = t_2 - t_1$).

*   **Comprador do FRA (Tomador/Borrower):** Paga a taxa fixa $R_{\text{FRA}}$ e recebe a taxa flutuante de referência $L$ (ex.: EURIBOR ou LIBOR) observada na data de fixação em $t_1$. Protege-se contra a alta das taxas de juros.
*   **Vendedor do FRA (Doador/Lender):** Recebe a taxa fixa $R_{\text{FRA}}$ e paga a taxa flutuante de referência $L$. Protege-se contra a queda das taxas de juros.

Como a liquidação financeira do FRA ocorre na data de início do período ($t_1$), o valor do ajuste deve ser descontado da data $t_2$ para a data $t_1$ pela taxa flutuante realizada $L$:
$$\text{Payoff}_{\text{Comprador}} = N \cdot \frac{(L - R_{\text{FRA}}) \cdot \tau}{1 + L \cdot \tau}$$

### 2.3 Exemplo Numérico Concreto de Cálculo com FRA

Considere os dados de mercado do EURIBOR para um depósito de 1 mês ($32$ dias) e um contrato FRA $1 \times 4$ ($123$ dias de prazo total, cobrindo o período do dia $32$ ao dia $123$, ou seja, um período de $91$ dias):

*   Taxa do depósito de 1M: $r_{\text{1M}} = -0,404\%$
*   Fator de capitalização do depósito de 1M em convenção Actual/365:
    $$C(1\text{M}) = 1 + (-0,00404) \cdot \frac{32}{365} = 0,999646$$
*   Taxa do FRA $1 \times 4$ cotada no mercado: $R_{\text{FRA } 1 \times 4} = -0,270\%$
*   Período do FRA: $\tau_{\text{FRA}} = \frac{91}{365}$ anos.

O fator de capitalização acumulado até o vencimento do FRA ($123$ dias) é dado por:
$$C(\text{FRA } 1 \times 4) = C(1\text{M}) \cdot \left( 1 + (-0,00270) \cdot \frac{91}{365} \right) = 0,999646 \cdot 0,999327 = 0,998973$$

A taxa zero continuamente composta equivalente ($NACC$) para o nó de $123$ dias é:
$$Z(\text{FRA } 1 \times 4) = 100 \cdot \ln(0,998973) \cdot \frac{365}{123} = -0,304948\%$$

---

## 3. Bootstrap da Curva (Depósitos, FRAs/Futuros e Swaps) e Interpolação

### 3.1 O Processo de Bootstrap

O *bootstrapping* é um procedimento iterativo de resolução no qual a curva de juros zero-cupom é construída de forma sequencial, do vértice mais curto ao mais longo, garantindo que cada instrumento financeiro utilizado como *input* seja precificado exatamente ao seu valor de mercado.

```
+-------------------------------------------------------------------+
|                        SELEÇÃO DE INPUTS                          |
|  Depósitos (Curto Prazo) -> FRAs/Futuros (Médio) -> Swaps (Longo) |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                     MONTAGEM DA CURVA ZERO                        |
|  Cálculo Direto dos Fatores de Desconto $P(0, t_i)$ no Curto Prazo |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                 MÉTODO ITERATIVO DE INTERPOLAÇÃO                  |
|  Aplica Interpolação -> Estima Fatores Intermediários ->         |
|  Ajusta Nó $r_n$ via Equação do Instrumento                       |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                     CONVERGÊNCIA DO BOOTSTRAP                     |
|  Itera até que todos os instrumentos de input reprecifiquem a zero|
+-------------------------------------------------------------------+
```

#### Algoritmo do Bootstrap para Títulos/Bônus
Para um conjunto de $n$ títulos com preços de mercado $A_k$, cupons $c_k$ e datas de fluxo de caixa $t_i$, a condição de reprecificação exata exige:
$$[A] \cdot P(0, t_{\text{settle}}) = \sum_{i=0}^n s_i P(0, t_i)$$
onde $s_0 = e \cdot \frac{c}{2}$, $s_i = \frac{c}{2}$ para $1 \le i < n$ e $s_n = 1 + \frac{c}{2}$. Isolando a taxa zero contínua $r_n$ no nó $t_n$:
$$r_n = \frac{1}{t_n} \left[ \ln s_n - \ln \left( [A] \cdot e^{-r_{\text{settle}} \cdot t_{\text{settle}}} - \sum_{i=0}^{n-1} s_i \cdot e^{-r_i \cdot t_i} \right) \right]$$

#### Algoritmo do Bootstrap para Swaps
Para uma taxa de swap fixa cotada $R_n$ com fluxos nas datas $t_1, t_2, \dots, t_n$ e frações de ano $\alpha_i$:
$$R_n = \frac{1 - P(0, t_n)}{\sum_{i=1}^n \alpha_i P(0, t_i)} \implies P(0, t_n) = \frac{1 - R_n \sum_{i=1}^{n-1} \alpha_i P(0, t_i)}{1 + R_n \cdot \alpha_n}$$
Em forma de taxa zero contínua iterativa:
$$r_n = -\frac{1}{t_n} \ln \left[ \frac{1 - R_n \sum_{j=1}^{n-1} \alpha_j P(t, t_j)}{1 + R_n \cdot \alpha_n} \right]$$

### 3.2 Avaliação Crítica dos Métodos Tradicionais de Interpolação

A escolha do método de interpolação entre os nós $t_i$ é indissociável do processo de *bootstrap*. O uso de métodos inadequados gera anomalias financeiras graves:

1.  **Linear nas Taxas Zero $r(t)$:**
    $$r(t) = \frac{t - t_{i-1}}{t_i - t_{i-1}} r_i + \frac{t_i - t}{t_i - t_{i-1}} r_{i-1}$$
    A taxa *forward* instantânea resultante é dada por:
    $$f(t) = \frac{2t - t_{i-1}}{t_i - t_{i-1}} r_i + \frac{t_i - 2t}{t_i - t_{i-1}} r_{i-1}$$
    *Patologias:* A função $r(t) \cdot t$ não é diferenciável nos nós $t_i$. As taxas *forward* apresentam descontinuidades (saltos) nos nós e podem tornar-se negativas mesmo quando as taxas spot são estritamente positivas.
2.  **Linear nos Logaritmos das Taxas / Fatores de Desconto:** Previne taxas negativas, mas mantém os saltos indesejados nas taxas *forward*.
3.  **Raw Interpolation (Linear no Log dos Fatores de Desconto):** Resulta em taxas *forward* instantâneas constantes em cada intervalo $[t_{i-1}, t_i]$:
    $$f(t) = \frac{r_i t_i - r_{i-1} t_{i-1}}{t_i - t_{i-1}}$$
    *Patologias:* Gera uma curva *forward* em escada (*piecewise constant*), com descontinuidades acentuadas em cada nó de mercado.
4.  **Piecewise Linear Forward:** Força a continuidade da taxa *forward* conectando os nós por retas.
    *Patologias:* Gera oscilações extremas e não naturais (*effetto zig-zag*). Exemplo de Hagan e West: para taxas zero flat de $5\%$ de $1$ a $5$ anos e $6\%$ de $6$ a $10$ anos, o *forward* linear necessita atingir $17\%$ no ano $6$ e $-5\%$ no ano $7$ para preservar as médias dos intervalos, destruindo a localidade da curva.
5.  **Cubic Splines (Natural, Financeira, Bessel/Hermite):** Garantem suavidade e continuidade de segunda derivada ($C^2$).
    *Patologias:* Ausência total de localidade. A perturbação no preço de um único instrumento afeta os coeficientes da *spline* ao longo de toda a curva, estendendo o risco para vértices muito distantes da maturidade do título perturbado. Além disso, *splines* cúbicas frequentemente geram taxas *forward* negativas e oscilações espúrias.

### 3.3 O Método Monotone Convex (Hagan e West)

O método **Monotone Convex** foi especificamente desenvolvido para superar todas as patologias dos métodos tradicionais. Ele opera sobre as taxas *forward* discretas $f_i^d = \frac{r_i t_i - r_{i-1} t_{i-1}}{t_i - t_{i-1}}$ e constrói uma função de taxa *forward* instantânea $f(t)$ contínua, estritamente positiva e monótona em cada intervalo.

Para o intervalo local parametrizado por $x = \frac{t - t_{i-1}}{t_i - t_{i-1}} \in$, define-se a função desvio $g(x) = f(t) - f_i^d$. A função $g(x)$ é ajustada por parábolas quadráticas por partes:
$$g(x) = g(0)(1 - 4x + 3x^2) + g(1)(-2x + 3x^2)$$
onde $g(0) = f_{i-1} - f_i^d$ e $g(1) = f_i - f_i^d$, satisfazendo rigorosamente a restrição de preservação de área $\int_0^1 g(x) \, dx = 0$.

O plano de coeficientes $(g(0), g(1))$ é dividido em quatro regiões/grupos comportamentais:

```
                  g(1)
                   ^
                   |    Grupo (ii)
       Grupo (iv)  |   / (Ajuste eta)
                   |  /
                   | /  Grupo (i)
                   |/  (Monótono Direto)
  -----------------+------------------> g(0)
                  /|
                 / |    Grupo (iii)
    Grupo (ii)  /  |   (Ajuste eta)
               /   |
              /    |    Grupo (iv)
                   |
```

*   **Grupo (i) [Monótono]:** Se $g(0)$ e $g(1)$ possuem sinais opostos e $g'(x)$ mantém o mesmo sinal em $$ (condição $-\frac{1}{2} g(0) \le g(1) \le -2 g(0)$), a função $g(x)$ é intrinsecamente monótona e nenhuma modificação é necessária.
*   **Grupo (ii) [Ajuste por Extremo Interno à Esquerda]:** A função $g(x)$ é redefinida como $g(x) = g(0)$ para $0 \le x \le \eta$, e $g(x) = g(0) + (g(1) - g(0))\left(\frac{x - \eta}{1 - \eta}\right)^2$ para $\eta < x \le 1$, com $\eta = \frac{g(1) + 2g(0)}{g(1) - g(0)}$.
*   **Grupo (iii) [Ajuste por Extremo Interno à Direita]:** A função $g(x)$ torna-se constante à direita: $g(x) = g(1) + (g(0) - g(1))\left(\frac{\eta - x}{\eta}\right)^2$ para $0 \le x < \eta$, e $g(x) = g(1)$ para $\eta \le x \le 1$, com $\eta = \frac{3g(1)}{g(1) - g(0)}$.
*   **Grupo (iv) [Ajuste de Mínimo Parabólico Positivo]:** Para evitar violação de positividade quando $g(0)$ e $g(1)$ têm o mesmo sinal, aplica-se uma parábola composta com mínimo em $A = -\frac{g(0)g(1)}{g(0)+g(1)}$ na posição $\eta = \frac{g(1)}{g(0)+g(1)}$.

Garante-se a positividade estrita de $f(t)$ aplicando o *collar* $0 \le f_i \le 2 \min(f_i^d, f_{i+1}^d)$ sobre os nós das taxas *forward* instantâneas.

---

## 4. Estrutura Multi-Curva Pós-2008, OIS vs. IBOR/SOFR e Contexto Operacional

### 4.1 A Ruptura do Paradigma de Curva Única (*Single-Curve*)

Até a crise financeira global de 2007-2008, o mercado financeiro operava sob a premissa de que as taxas interbancárias (como LIBOR e EURIBOR) eram isentas de risco de crédito de contraparte e de liquidez. Consequentemente, uma única curva de juros era utilizada tanto para **projetar** os fluxos de caixa flutuantes quanto para **descontar** esses fluxos a valor presente.

Com a eclosão da crise, os *spreads* de crédito interbancário e de liquidez explodiram. Títulos e *swaps* vinculados a diferentes prazos de fixação (tenores como $1\text{M}, 3\text{M}, 6\text{M}, 12\text{M}$) passaram a negociar a níveis significativamente distintos, violando as relações clássicas de não arbitragem.

```
PARADIGMA PRÉ-2008 (Single-Curve)
  [ Curva Única LIBOR/EURIBOR ] ---> Projeta Fluxos E Desconta Fluxos

PARADIGMA PÓS-2008 (Multi-Curve)
  [ Curva OIS / SOFR / CDI ]    ---> Desconto Isento de Risco de Crédito (CSA Colateralizado)
  [ Curva Projeção 1M ]        ---> Projeção de Taxas Forward Tenor 1M
  [ Curva Projeção 3M ]        ---> Projeção de Taxas Forward Tenor 3M
  [ Curva Projeção 6M ]        ---> Projeção de Taxas Forward Tenor 6M
```

### 4.2 Desconto por OIS (*Overnight Index Swap*) e Reformas de Taxas Livres de Risco (RFRs)

Em acordos com colateralização diária (*Credit Support Annex - CSA*), a remuneração do colateral em dinheiro ocorre à taxa overnight do banco central. Por essa razão, a **curva OIS** (baseada em taxas como ESTR na Zona do Euro, SOFR nos EUA, SONIA no Reino Unido) tornou-se o padrão universal para **desconto de fluxos colateralizados**.

*   **Ajuste Quanto Interno (*Quanto / Basis Adjustment*):** A mudança do numeraire associado à curva de projeção para o numeraire da curva de desconto OIS introduz uma correção técnica análoga a um ajuste quanto, dependente da volatilidade do *basis* e da correlação inter-curvas.

### 4.3 O Contexto Operacional Brasileiro: A Curva DI x Pré (B3)

No Brasil, o mercado financeiro opera nativamente sob a estrutura de precificação por **dias úteis** (convenção `Business/252`) e composição composta diária baseada na taxa **CDI (Certificado de Depósito Interfinanceiro)** acumulada.

O fator de desconto da curva DI x Pré para um vencimento de $DU$ dias úteis é expresso por:
$$P(0, DU) = \left( 1 + R_{\text{DI}}(DU) \right)^{-\frac{DU}{252}}$$
onde $R_{\text{DI}}(DU)$ é a taxa anualizada composta equivalente B3.

Devido à liquidez extrema do contrato de DI Futuro na B3, a curva DI atua simultaneamente como curva de desconto de colateral e como curva primária de projeção de taxa de juros no mercado doméstico.

---

## 5. Swaps de Taxa de Juros: Pernas Fixa e Flutuante, Taxa Par, PV e MTM

### 5.1 Estrutura do *Interest Rate Swap* (IRS) Vanilla

Um *Interest Rate Swap* (IRS) é um contrato em que duas partes trocam fluxos de caixa futuros baseados em um valor notocional $N$. Na perna fixa, uma taxa de juros contratual $R_{\text{fixa}}$ é paga periodicamente; na perna flutuante, pagamentos baseados na taxa de referência observada do mercado (ex.: EURIBOR 3M) são efetuados.

### 5.2 Matemática da Taxa Par do Swap ($R_{\text{par}}$)

Considerando a estrutura multi-curva, denote por $P_d(0, t_i)$ os fatores de desconto da curva de desconto (OIS) e por $F(0; t_{i-1}, t_i)$ as taxas *forward* projetadas da curva do tenor flutuante correspondente.

O Valor Presente Líquido (PV) da Perna Flutuante é:
$$\text{PV}_{\text{flutuante}} = N \sum_{i=1}^n \alpha_i^{\text{flut}} \cdot F(0; t_{i-1}^{\text{flut}}, t_i^{\text{flut}}) \cdot P_d(0, t_i^{\text{flut}})$$

Em uma estrutura mono-curva purificada, por cancelamento telescópico, o valor da perna flutuante simplifica para $N \cdot [P_d(0, t_0) - P_d(0, t_n)]$.

O Valor Presente Líquido (PV) da Perna Fixa é:
$$\text{PV}_{\text{fixa}} = N \cdot R_{\text{fixa}} \sum_{j=1}^m \alpha_j^{\text{fixa}} \cdot P_d(0, t_j^{\text{fixa}})$$

A **Taxa Swap Par** ($R_{\text{par}}$) é a taxa fixa $R_{\text{fixa}}$ que iguala o valor presente de ambas as pernas no início do contrato ($\text{PV}_{\text{swap}} = 0$):
$$R_{\text{par}} = \frac{P_d(0, t_0) - P_d(0, t_n)}{\sum_{j=1}^m \alpha_j^{\text{fixa}} P_d(0, t_j^{\text{fixa}})}$$
O denominador $A(0) = \sum_{j=1}^m \alpha_j^{\text{fixa}} P_d(0, t_j^{\text{fixa}})$ é denominado **Anuidade do Swap** (*Swap Annuity* ou *PV01 Notional*).

### 5.3 Mark-to-Market (MTM) de um Swap em Carteira

À medida que o tempo passa e as taxas de juros flutuam no mercado, a taxa par de um novo swap de mesmo vencimento residual altera-se para $R_{\text{par}}^{\text{novo}}$. O valor de mercado no instante $t$ ($\text{MTM}_t$) de um swap pré-existente no qual o agente paga taxa fixa $R_{\text{contratada}}$ é dado diretamente por:
$$\text{MTM}_t = N \cdot (R_{\text{par}}^{\text{novo}} - R_{\text{contratada}}) \cdot \sum_{j=1}^m \alpha_j \cdot P_d(t, t_j)$$

---

## 6. Gestão de Risco de Taxa: DV01/PV01, Duração, Convexidade, Key Rate Durations e Localidade

### 6.1 DV01 e PV01

O **DV01** (*Dollar Value of a Basis Point*) ou **PV01** (*Present Value of a Basis Point*) mede a variação absoluta no valor presente de uma posição financeira decorrente de um deslocamento paralelo de $1$ ponto base ($0,01\%$ ou $0,0001$) na curva de juros:
$$\text{DV01} = -\frac{\Delta \text{PV}}{\Delta y} = -\frac{\text{PV}(y + 0,0001) - \text{PV}(y - 0,0001)}{2}$$

### 6.2 Duração de Macaulay, Duração Modificada e Convexidade

Para um título que paga fluxos $C_i$ nas datas $t_i$ com *yield to maturity* $y$:

*   **Duração de Macaulay ($D_{\text{Mac}}$):** Média ponderada do tempo dos fluxos de caixa:
    $$D_{\text{Mac}} = \frac{\sum_{i=1}^n t_i \cdot \frac{C_i}{(1+y)^{t_i}}}{P}$$
*   **Duração Modificada ($D_{\text{Mod}}$):** Sensibilidade percentual de preço a mudanças no yield:
    $$D_{\text{Mod}} = \frac{D_{\text{Mac}}}{1 + y} = -\frac{1}{P} \frac{dP}{dy}$$
*   **Convexidade ($C$):** Medida de segunda ordem da curvatura da relação preço-taxa:
    $$C = \frac{1}{P} \frac{d^2 P}{dy^2} = \frac{1}{P \cdot (1+y)^2} \sum_{i=1}^n \frac{C_i \cdot t_i \cdot (t_i + 1)}{(1+y)^{t_i}}$$
*   **Aproximação de Preço por Série de Taylor:**
    $$\frac{\Delta P}{P} \approx -D_{\text{Mod}} \cdot \Delta y + \frac{1}{2} C \cdot (\Delta y)^2$$

### 6.3 Key Rate Durations e o Conceito de Localidade da Interpolação

A gestão moderna de risco de curva não utiliza apenas choques paralelos, mas decomposições por **vértices de risco** (*time buckets*) por meio das *Key Rate Durations*. Aplica-se um choque ("blip") de $1$ ponto base em um nó específico da curva $t_i$, mantendo os demais nós fixos, e calcula-se o impacto no portfólio.

A eficácia do *hedge* por *Key Rate Durations* depende criticamente do **índice de localidade** ($l, u$) do método de interpolação utilizado no *bootstrap*:

| Método de Interpolação | Índice de Localidade à Esquerda ($l$) | Índice de Localidade à Direita ($u$) | Impacto Financeiro do Choque em $t_i$ |
| :--- | :--- | :--- | :--- |
| **Linear nas Taxas $r(t)$** | $l = 1$ | $u = 1$ | **Estritamente Local:** O choque afeta apenas o intervalo vizinho imediato $[t_{i-1}, t_{i+1}]$. |
| **Natural Cubic Spline** | $l = i - 1$ | $u = n - i$ | **Não Local:** O choque espalha contaminação de risco por **todos** os nós da curva ($1$ a $n$). |
| **Monotone Convex** | $l = 2$ | $u = 2$ | **Local Controlado:** O choque afeta estritamente no máximo $2$ nós à esquerda e $2$ à direita. |

#### Demonstração Empírica do Impacto da Localidade (Dados de Hagan e West - Tabela 2)
Considere uma curva com as seguintes taxas nominais de input:

$$\begin{array}{c|c|c|c|c|c|c}
\hline
t_i \text{ (anos)} & 0,1 & 1 & 4 & 9 & 20 & 30 \\
\hline
r_i (\%) & 8,1\% & 7,0\% & 5,0\% & 7,0\% & 4,0\% & 3,0\% \\
\hline
\end{array}$$

Ao aplicar um choque pontual no nó de $4$ anos, alterando sua taxa de $4,4\%$ para $5,4\%$:
*   Sob **Natural Cubic Spline**, os preços teóricos de títulos com vencimento em $20$ e $30$ anos flutuam artificialmente, gerando necessidades falsas de rebalanceamento de carteira (*hedging espúrio*).
*   Sob **Monotone Convex**, a alteração afeta apenas a região próxima de $4$ anos (intervalo $$ anos), deixando as taxas para vencimentos curtos ($< 1$ ano) e longos ($> 9$ anos) inalteradas.

---

## 7. Opções sobre Taxas: Caps, Floors, Caplets, Swaptions e Paridade Cap-Floor

### 7.1 Caplets, Floorlets e Estruturas Cap/Floor

Uma opção sobre taxa de juros protege o detentor contra variações adversas nas taxas futuras:

*   **Caplet:** Um call europeu sobre a taxa *forward* $L(t_1, t_2)$ com taxa de exercício (strike) $K$. O payoff pago em $t_2$ é:
    $$\text{Payoff}_{\text{Caplet}} = N \cdot \alpha \cdot \max(L(t_1, t_2) - K, 0)$$
*   **Floorlet:** Um put europeu sobre a taxa *forward* $L(t_1, t_2)$ com strike $K$. O payoff pago em $t_2$ é:
    $$\text{Payoff}_{\text{Floorlet}} = N \cdot \alpha \cdot \max(K - L(t_1, t_2), 0)$$
*   **Interest Rate Cap / Floor:** Uma carteira (soma) de *caplets* ou *floorlets* sequenciais cobrindo uma série de datas de fixação futuras.

### 7.2 Paridade Cap-Floor

Pela relação fundamental de arbitragem, para cada caplet e floorlet vinculados ao mesmo período $[t_1, t_2]$ e mesmo strike $K$:
$$\text{Caplet}(K) - \text{Floorlet}(K) = N \cdot \alpha \cdot P_d(0, t_2) \cdot (F(0; t_1, t_2) - K)$$

A soma sobre todos os períodos da estrutura resulta na **Paridade Cap-Floor-Swap**:
$$\text{Cap}(K) - \text{Floor}(K) = \text{Swap Payer}(K)$$

### 7.3 Swaptions (Opções sobre Swaps)

Uma *Swaption* concede ao seu titular o direito (sem obrigação) de entrar em um *Interest Rate Swap* na data de expiração da opção $T_{\text{exp}}$ a uma taxa fixa prefixada $K$.

*   **Payer Swaption:** Direito de **pagar taxa fixa** $K$ e receber taxa flutuante. Equivale a um call sobre a taxa par do swap $R_{\text{par}}$.
*   **Receiver Swaption:** Direito de **receber taxa fixa** $K$ e pagar taxa flutuante. Equivale a um put sobre a taxa par do swap $R_{\text{par}}$.

O payoff de uma Payer Swaption no vencimento $T_{\text{exp}}$ é expresso por:
$$\text{Payoff}_{\text{Payer Swaption}} = A(T_{\text{exp}}) \cdot \max(R_{\text{par}}(T_{\text{exp}}) - K, 0)$$
onde $A(T_{\text{exp}}) = \sum_{j=1}^m \alpha_j P_d(T_{\text{exp}}, t_j)$ é a anuidade do swap subjacente.

---

## 8. Modelagem de Volatilidade: Black-76 vs. Bachelier, Taxas Negativas, Smile e Modelo SABR / Rough SABR

### 8.1 Modelo de Black-76 (Volatilidade Lognormal)

O modelo clássico de Black-76 assume que a taxa *forward* ou a taxa par do swap $S$ segue um movimento browniano geométrico lognormal sob a medida de probabilidade equivalente apropriada (medida forward ou medida anuidade):
$$dS_t = \sigma_{\text{BS}} \cdot S_t \, dZ_t$$

A fórmula de apreçamento de um call europeu (ou caplet/payer swaption) com tempo de expiração $\tau = T - t$ é:
$$P^{\text{BS}}(S, K, \tau, \sigma_{\text{BS}}) = S \cdot \Phi(d_+) - K \cdot \Phi(d_-)$$
$$d_\pm = \frac{\ln(S/K) \pm \frac{1}{2} \sigma_{\text{BS}}^2 \tau}{\sigma_{\text{BS}} \sqrt{\tau}}$$
onde $\Phi(\cdot)$ é a função de distribuição acumulada da normal padrão.

*Patologia Crítica:* Se a taxa $S \le 0$ ou se o strike $K \le 0$, a fórmula de Black-76 colapsa devido ao termo $\ln(S/K)$, inviabilizando sua aplicação em mercados de taxas de juros negativas (como o EURIBOR e os títulos escandinavos exibiram empiricamente).

### 8.2 Modelo de Bachelier (Volatilidade Normal)

O modelo de Bachelier (1900) assume uma dinâmica normal em que as variações da taxa são independentes do seu nível absoluto:
$$dS_t = \sigma_B \, dZ_t$$

A fórmula de apreçamento para o call de Bachelier $P^B(S, K, \tau, \sigma_B)$ é dada por:
$$P^B(S, K, \tau, \sigma_B) = \sigma_B \sqrt{\tau} \cdot \phi\left( \frac{S - K}{\sigma_B \sqrt{\tau}} \right) + (S - K) \cdot \Phi\left( \frac{S - K}{\sigma_B \sqrt{\tau}} \right)$$
onde $\phi(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2/2}$ é a densidade da normal padrão.

A volatilidade de Bachelier $\sigma_B$ é expressa em pontos base por ano (ex.: $\sigma_B = 0,0050 = 50\text{ bps/ano}$). O modelo funciona perfeitamente para taxas zero ou negativas. A relação assintótica de Berestycki para converter a volatilidade Black-Scholes em Bachelier é:
$$\sigma_{\text{BS}} \approx \sigma_B \cdot \frac{\ln(K/S)}{K - S}$$

### 8.3 Condição de Drift para Dinâmicas de Implied Volatility Sem Arbitragem (Abordagem de Balland)

Para derivar aproximações assintóticas de volatilidade implícita livres de arbitragem, Balland (2006) estabeleceu que o processo de volatilidade implícita $\Sigma_t$ deve cumprir condições de *drift* sob a medida de martingal $Q$.

Para o caso lognormal de Black-Scholes com log-moneyness $k = \ln(K/S)$, denotando por $D \, dt$ a parte de *drift* de $d\Sigma$:
$$\frac{d}{dt} \langle \ln S \rangle + 2 k \frac{d}{dt} \langle \ln S, \ln \Sigma \rangle + k^2 \frac{d}{dt} \langle \ln \Sigma \rangle = \Sigma^2 - 2 \Sigma \tau D - \Sigma^2 \tau \frac{d}{dt} \langle \ln S, \ln \Sigma \rangle + \frac{\Sigma^4 \tau^2}{4} \frac{d}{dt} \langle \ln \Sigma \rangle$$

Para o caso normal de Bachelier com moneyness $k = K - S$:
$$\frac{d}{dt} \langle S \rangle + 2 k \frac{d}{dt} \langle S, \ln \Sigma \rangle + k^2 \frac{d}{dt} \langle \ln \Sigma \rangle = \Sigma^2 - 2 \Sigma \tau D$$

### 8.4 Modelo SABR Clássico (Hagan et al., 2002)

O modelo estocástico de volatilidade SABR (*Stochastic Alpha-Beta-Rho*) é formalizado pelo sistema de equações diferenciais estocásticas:
$$dS_t = \alpha_t S_t^\beta \, dZ_t, \quad S_0 = S$$
$$d\alpha_t = \eta \alpha_t \, dW_t, \quad \alpha_0 = \alpha$$
$$d\langle Z, W \rangle_t = \rho \, dt$$
onde $\alpha$ é o nível de volatilidade instantânea, $\beta \in$ é a elasticidade do ativo ($\beta=1$ lognormal, $\beta=0$ normal), $\eta > 0$ é a volatilidade da volatilidade (*vol-of-vol*) e $\rho \in (-1, 1)$ é a correlação entre o ativo e a volatilidade.

No caso lognormal ($\beta=1$), a solução da ODE de Balland para o *smile* normalizado $f(y) = \frac{y}{g(y)}$ com $y = \frac{\eta}{\alpha} \ln(K/S)$ resulta na celebrada fórmula SABR de Hagan:
$$g(y) = \frac{-2 \ln \left( \frac{\sqrt{1 + \rho y + y^2/4} - \rho - y/2}{1 - \rho} \right)}{1 - \rho}$$

### 8.5 O Modelo Rough SABR (Fukasawa e Gatheral, 2021/2022)

Embora extremamente popular, o modelo SABR clássico é incapaz de reproduzir a estrutura a termo da inclinação do *smile* (*at-the-money skew*) observada empiricamente no mercado, que obedece a uma lei de potência $T^{H - 1/2}$ com parâmetro de Hurst $H \approx 0,05 - 0,15$. Para ajustar diferentes maturidades, operadores eram forçados a usar parâmetros SABR calibrados fatia por fatia (*slice-by-slice*).

O modelo **Rough SABR** introduzido por Fukasawa e Gatheral unifica o modelo SABR e o modelo Rough Bergomi. A dinâmica sob a medida de martingal $Q$ é expressa por:
$$d S_t = \alpha_t \beta(S_t) \, dZ_t$$
$$d \xi_t(s) = \xi_t(s) \kappa(s - t) \, dW_t, \quad t < s$$
onde $\alpha_t = \sqrt{\xi_t(t)}$, $\kappa(t) = \eta \sqrt{2H} \, t^{H - 1/2}$ é o núcleo fracionário singular, $(Z, W)$ é um movimento browniano bidimensional com $d\langle Z, W \rangle_t = \rho \, dt$, $\eta > 0$, e $H \in (0, 1/2]$ é o parâmetro de Hurst.

A curva de variância *forward* $\xi_t(s) = E^Q[\alpha_s^2 / \beta(S_s)^2 \mid \mathcal{F}_t]$ possui a solução explícita:
$$\xi_t(s) = \xi_0(s) \exp\left( \eta \sqrt{2H} \int_0^t (s - u)^{H - 1/2} \, dW_u - \frac{1}{2} \eta^2 (s^{2H} - (s - t)^{2H}) \right)$$

#### A Equação Diferencial Ordinária (ODE) do Rough SABR
Aplicando o princípio da aproximação assintoticamente livre de arbitragem para maturidades curtas $\tau = T - t \to 0$, Fukasawa e Gatheral provam que o *smile* de volatilidade normalizado $f(y)$ satisfaz rigorosamente a seguinte ODE não linear:

$$\left( 1 - \frac{y f'(y)}{f(y)} \right)^2 \left[ 1 + \frac{2\rho y}{2H+1} + \left( \frac{y}{2H+1} \right)^2 \right] = f(y)^2 \left( 1 - \frac{(1-2H) y f'(y)}{f(y)} \right)$$
com condição inicial $f(0) = 1$.

Recastando a ODE em termos de $G(y) = g(y)^2 = \left(\frac{y}{f(y)}\right)^2$, obtém-se:
$$\frac{1}{4} G'(y)^2 \left[ \frac{y^2}{(2H+1)^2} + \frac{2\rho y}{2H+1} + 1 \right] = \frac{1-2H}{2} y G'(y) + 2H G(y), \quad G(0) = 0$$

#### Soluções Limite Exatas
1.  **Caso Clássico ($H = 1/2$):** Recupera exatamente a fórmula SABR de Hagan:
    $$G_{1/2}(y) = 4 \left[ \frac{\ln\left( \frac{\sqrt{1 + \rho y + y^2/4} - \rho - y/2}{1 - \rho} \right)}{1 - \rho} \right]^2$$
2.  **Caso Ultra-Áspero ($H = 0$):**
    $$G_0(y) = \ln(1 + 2\rho y + y^2) + \frac{2\rho}{\sqrt{1-\rho^2}} \left[ \arctan\left( \frac{\rho}{\sqrt{1-\rho^2}} \right) - \arctan\left( \frac{y + \rho}{\sqrt{1-\rho^2}} \right) \right]$$

#### Expansão de Séries e Aproximação Analítica de Fechamento (*A Rough SABR Formula*)
Substituindo $f(x) = 1 + a x + \frac{b}{2} x^2 + \dots$ na ODE, os coeficientes de expansão obtidos são:
$$a = \frac{\rho}{2(H + 1/2)(H + 3/2)}$$
$$b = \frac{(2H+3)^2 - 12(2H+1)\rho^2}{2(H+1)(2H+1)^2(2H+3)^2}$$
O coeficiente $a$ concorda perfeitamente com a fórmula de *skew* assintótico de El Euch, Fukasawa, Gatheral e Rosenbaum (2019).

A interpolação analítica de fechamento para $G_A(y)$ que une os extremos $G_0$ e $G_{1/2}$ garantindo o *skew* ATM correto para qualquer $H \in (0, 1/2]$ é:

$$G_A(y) = (2H+1)^2 \left[ \frac{3(1-2H)}{2H+3} G_0\left( \frac{y}{2H+1} \right) + \frac{2H}{2H+3} G_{1/2}\left( \frac{2y}{2H+1} \right) \right]$$

A **Fórmula Rough SABR** para a volatilidade implícita $Black-Scholes$ $\Sigma(k, \tau)$ para um log-strike $k = \ln(K/S)$ e tempo de expiração $\tau$ é dada por:

$$\Sigma(k, \tau) = \Sigma(0, \tau) \frac{|y(k, \tau)|}{\sqrt{G_A(y(k_\beta, \tau))}}$$

onde:
$$y(x, \tau) = \frac{\kappa(\tau) \cdot x}{U(\tau)}, \quad k_\beta = \int_S^K \frac{ds}{\beta(s)}, \quad U_t(\tau) = \sqrt{\frac{1}{\tau} \int_t^{t+\tau} \xi_t(s) \, ds}$$

---

## 9. Integração da Volatilidade e Preparação da Superfície do Módulo M04

### 9.1 Colapso de Escalamento Universal das Fatias de Volatilidade

A grande inovação do modelo Rough SABR reside na sua capacidade de reescalonar o log-moneyness $k$ pelo fator $\kappa(\tau) / U(\tau)$. No modelo SABR clássico, curvas de volatilidade normalizadas $\Sigma(k, \tau) / \Sigma(0, \tau)$ para diferentes maturidades $\tau$ espalham-se em trajetórias distintas. Sob o Rough SABR, quando plottadas contra a variável reescalonada $y(k, \tau)$, as fatias de volatilidade de diferentes maturidades (ex.: de $3$ semanas a $9$ meses) desabam e alinham-se rigorosamente sobre uma **única curva universal** dada por $f_A(y) = \frac{|y|}{\sqrt{G_A(y)}}$.

```
SMILES CLÁSSICOS (Múltiplas Curvas Espalhadas)
  Implied Vol
     ^
     |    /--- Tau = 1M
     |   /---- Tau = 6M
     |  /----- Tau = 1Y
     +-------------------> Log-Strike (k)

SMILES ROUGH SABR (Colapso na Curva Universal)
  Implied Vol Normalizada
     ^
     |         /-- Todos os Vencimentos (3W a 9M)
     |    .---*---.  Colapsados na Função f_A(y)
     |   /         \
     +-------------------> Variável Reescalonada y(k, tau)
```

### 9.2 Calibração Empírica no Mercado Cambial (FX EURUSD)

Fukasawa e Gatheral demonstraram o ajuste da fórmula Rough SABR com dados reais do mercado de opções de câmbio EURUSD ( Bloomberg):

*   **Parâmetros Calibrados Globalmente:** $H = 0,1525$, $\eta = 26,66$, $\rho = 0,0339$.
*   **Comportamento Observado:** As cotações de $5$ pontos de volatilidade por maturidade (25-Delta Put, 10-Delta Put, ATM, 10-Delta Call, 25-Delta Call) para vencimentos entre $3$ semanas e $9$ meses colapsaram perfeitamente sobre a curva teórica $f_A(y)$.

### 9.3 Condição de Validade da Expansão

A aproximação analítica do Rough SABR funciona como uma expansão de prazo curto (*short-dated expansion*). Testes numéricos intensivos via simulação de Monte Carlo pelo esquema híbrido (Bennedsen, Lunde, Pakkanen) confirmaram que a fórmula retém altíssima precisão desde que o parâmetro de expansão adimensional satisfaça:
$$\eta \cdot \tau^H < 1$$

Essa parametrização universal estabelece a fundação exata para a construção e parametrização global da superfície de volatilidade sem arbitragem (*implied volatility surface*) que será aprofundada no **Módulo M04**.

---

## 10. Implementação em Python e Checklist Operacional

### 10.1 Implementação Completa em Python

```python
import numpy as np
from scipy.optimize import newton

def g0_function(y, rho):
    """
    Solucao exata da funcao g(y) para H = 0 no modelo Rough SABR.
    """
    if abs(y) < 1e-7:
        return 1.0
    
    arg_arctan1 = rho / np.sqrt(1.0 - rho**2)
    arg_arctan2 = (y + rho) / np.sqrt(1.0 - rho**2)
    
    term1 = np.log(1.0 + 2.0 * rho * y + y**2)
    term2 = (2.0 * rho / np.sqrt(1.0 - rho**2)) * (np.arctan(arg_arctan1) - np.arctan(arg_arctan2))
    
    val = term1 + term2
    val = np.maximum(val, 0.0) # Garantia de estabilidade numerica
    
    g_val = (y / np.abs(y)) * np.sqrt(val)
    return g_val

def g12_function(y, rho):
    """
    Solucao exata da funcao g(y) para H = 1/2 (SABR Classico Lognormal).
    """
    if abs(y) < 1e-7:
        return 1.0
    
    numerator = np.sqrt(1.0 + rho * y + (y**2) / 4.0) - rho - y / 2.0
    denominator = 1.0 - rho
    
    g_val = -2.0 * np.log(numerator / denominator) / (1.0 - rho)
    return g_val

def rough_sabr_G_A(y, H, rho):
    """
    Aproximacao de fechamento G_A(y) do Rough SABR (Fukasawa & Gatheral).
    Interpolacao entre G_0 e G_1/2 garantindo o skew ATM correto.
    """
    if abs(y) < 1e-7:
        return 0.0
    
    term_H = 2.0 * H + 1.0
    y_g0 = y / term_H
    y_g12 = 2.0 * y / term_H
    
    G0_val = (g0_function(y_g0, rho))**2
    G12_val = (g12_function(y_g12, rho))**2
    
    weight0 = 3.0 * (1.0 - 2.0 * H) / (2.0 * H + 3.0)
    weight12 = 2.0 * H / (2.0 * H + 3.0)
    
    G_A = (term_H**2) * (weight0 * G0_val + weight12 * G12_val)
    return G_A

def rough_sabr_implied_vol(K, S, tau, xi0, H, eta, rho, beta=1.0):
    """
    Calcula a volatilidade implicita Black-Scholes pelo Modelo Rough SABR.
    """
    k = np.log(K / S)
    
    # Integracao da funcao beta(s) para x
    if beta == 1.0:
        k_beta = k
    elif beta == 0.5:
        k_beta = 2.0 * (np.sqrt(K) - np.sqrt(S))
    else:
        k_beta = (K**(1.0 - beta) - S**(1.0 - beta)) / (1.0 - beta)
        
    kappa_tau = eta * np.sqrt(2.0 * H) * (tau**(H - 0.5))
    U_tau = np.sqrt(xi0) # Assumindo curva de variancia forward flat xi0
    
    y_val = kappa_tau * k / U_tau
    y_kbeta = kappa_tau * k_beta / U_tau
    
    if abs(k) < 1e-6:
        # Volatilidade At-The-Money (ATM)
        sigma_ATM = U_tau
        return sigma_ATM
    
    G_A_val = rough_sabr_G_A(y_kbeta, H, rho)
    f_A_val = np.abs(y_val) / np.sqrt(G_A_val)
    
    sigma_BS = U_tau * f_A_val
    return sigma_BS

## Exemplo de Teste de Execucao Numérica
if __name__ == "__main__":
    S0 = 100.0
    K_test = 105.0
    tau_test = 0.25 # 3 meses
    xi0_test = 0.04 # Volatilidade ATM de 20% (sqrt(0.04) = 0.20)
    H_test = 0.05   # Parametro de Hurst altamente aspero
    eta_test = 1.0  # Vol-of-vol
    rho_test = -0.6 # Correlacao negativa
    
    vol_impl = rough_sabr_implied_vol(K_test, S0, tau_test, xi0_test, H_test, eta_test, rho_test)
    print(f"Volatilidade Implicita Rough SABR para K={K_test}: {vol_impl*100:.4f}%")
```

### 10.2 Checklist Operacional de Construção e Calibração

```
[ ] PASSO 1: SANEAMENTO E FILTRAGEM DOS DADOS DE ENTRADA
    - Coletar cotações de mercado para Depósitos, FRAs, Futuros e Swaps.
    - Descartar instrumentos ilíquidos ou com spreads de compra/venda excessivos.
    - Verificar convenções de contagem de dias (Ex: Actual/360, Actual/365, Business/252).

[ ] PASSO 2: MONTAGEM DA ESTRUTURA MULTI-CURVA
    - Construir a curva OIS/SOFR/CDI primária para uso estrito no DESCONTO COLATERALIZADO.
    - Construir curvas independentes de PROJEÇÃO FORWARD para cada tenor (1M, 3M, 6M).

[ ] PASSO 3: SELEÇÃO E EXECUÇÃO DO BOOTSTRAP DE INTERPOLAÇÃO
    - Selecionar o método MONOTONE CONVEX para garantir positividade e continuidade do forward.
    - Aplicar o algoritmo iterativo de reprecificação até convergência dos preços a zero.
    - Validar os índices de localidade (l=2, u=2) garantindo a integridade do risco local.

[ ] PASSO 4: AVALIAÇÃO E GESTÃO DE RISCO DE CURVA
    - Calcular a matriz de Key Rate Durations nos vértices operacionais.
    - Aplicar choques de +1 bps por nó para verificar ausência de contaminação não local.

[ ] PASSO 5: CALIBRAÇÃO DA MODELAGEM DE VOLATILIDADE
    - Determinar a convenção de precificação: Black-76 para taxas estritamente positivas;
      Bachelier Normal para ambientes com taxas próximas de zero ou negativas.
    - Extrair parâmetros do Rough SABR (H, eta, rho, xi0) ajustando a curva universal f_A(y).
    - Checar a condição de validade da expansão adimensional: eta * tau^H < 1.
```

---

## 11. Tabelas Comparativas e Glossário Técnico de Termos

### 11.1 Tabela Comparativa de Métodos de Interpolação de Curvas de Juros

| Método de Interpolação | Continuidade do Forward $f(t)$ | Positividade do Forward Garantida? | Preservação da Localidade de Risco | Risco de Oscilações Espúrias | Aplicação Recomendada em Produção |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Linear nas Taxas $r(t)$** | Descontínuo (Saltos nos nós) | Não (Pode gerar $f(t) < 0$) | Alta ($l=1, u=1$) | Baixo | Não recomendada em mesas quantitativas. |
| **Raw (Linear no Log de DF)** | Constante por Partes | Sim (se $r_i > 0$) | Alta ($l=1, u=1$) | Nulo (Escada) | Apenas para testes iniciais de validação. |
| **Piecewise Linear Forward** | Contínuo ($C^0$) | Não (Gera oscilações extremas) | Muito Baixa | Severo (*Zig-zag*) | Totalmente desaconsehada. |
| **Natural Cubic Spline** | Suave ($C^2$) | Não | Nula ($l=i-1, u=n-i$) | Alto (Nas extremidades) | Inadequada para gestão de risco local. |
| **Monotone Convex** | Contínuo e Monótono | **Sim** (Com restrição de collar) | **Alta** ($l=2, u=2$) | **Nulo** | **Padrão Ouro de Mercado (Hagan & West)**. |

### 11.2 Tabela Comparativa de Modelos de Volatilidade e Precificação de Opções

| Modelo de Volatilidade | Dinâmica Subjacente | Suporta Taxas Negativas? | Estrutura a Termo do ATM Skew | Mecanismo de Parametrização do Smile | Complexidade Computacional |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Black-76** | Lognormal ($dS = \sigma S dZ$) | **Não** (Singularidade em $S \le 0$) | Ausente (Ajuste individual por fatia) | Nulo (Volatilidade Flat por vencimento) | Análise Direta (Analítico Instantâneo) |
| **Bachelier** | Normal ($dS = \sigma_B dZ$) | **Sim** (Natural) | Ausente | Nulo (Ajuste Flat Normal) | Análise Direta (Analítico Instantâneo) |
| **SABR Clássico** | Difusão Estocástica ($dS = \alpha S^\beta dZ$) | Parcial (Apenas sob modelos deslocados) | Incapaz ($T^{-1/2}$ incorreto) | Excelente no Smile local; falha globalmente | Fórmula de Hagan (Analítico Rápido) |
| **Rough SABR** | Ruído Fracionário ($H \in (0, 1/2]$) | **Sim** (Ajuste Normal / Beta flexível) | **Exata** (Lei de potência $T^{H - 1/2}$) | **Colapsa todas as fatias em curva única** | Fórmula $f_A(y)$ ou Resolução de ODE |

### 11.3 Glossário Técnico de Termos

*   **Anuidade do Swap (*Swap Annuity / PV01 Notional*):** O valor presente de um ponto base pago ao longo de todas as datas de fluxo da perna fixa de um swap, expresso por $A(0) = \sum_{j=1}^m \alpha_j P_d(0, t_j)$.
*   **Bootstrapping:** Método numérico sequencial para determinar a curva de taxas de juros zero-cupom a partir de instrumentos cotados de mercado.
*   **Caplet / Floorlet:** Opções europeias individuais sobre uma taxa de juros *forward* cobrindo um único período de fixação.
*   **Colateralização (CSA):** Acordo contratual de margem de garantia em dinheiro reduzindo o risco de crédito de contraparte; determina a taxa OIS como taxa de desconto.
*   **Duração Modificada:** Medida de sensibilidade percentual de preço de um título em relação a mudanças paralelas na sua taxa de retorno (*yield*).
*   **DV01 / PV01:** Mudança absoluta no valor monetário de um portfólio para uma alteração de $1$ ponto base ($0,01\%$) nas taxas de juros.
*   **Fator de Desconto $P(0, t)$:** Preço presente de um título cupom zero que paga $1,00$ na data futura $t$.
*   **Forward Rate Agreement (FRA):** Contrato no qual duas partes fixam a taxa de juros a ser aplicada sobre um montante nocional durante um período futuro.
*   **Key Rate Duration:** Sensibilidade do valor de um portfólio a um choque isolado de taxa de juros localizado em um nó específico da curva.
*   **Monotone Convex Method:** Método avançado de interpolação desenvolvido por Hagan e West que garante taxas *forward* contínuas, positivas e preserva a localidade do risco.
*   **Overnight Index Swap (OIS):** Swap de taxa de juros cuja perna flutuante é vinculada a uma taxa diária overnight repactuada (ex.: ESTR, SOFR, CDI).
*   **Paridade Cap-Floor:** Relação teórica de não arbitragem segundo a qual a diferença entre um Cap e um Floor de mesmo strike equivale a um Swap Payer.
*   **Parâmetro de Hurst ($H$):** Parâmetro que mede a rugosidade de um processo estocástico. Para $H < 1/2$, as trajetórias da volatilidade são mais ásperas (*rough*) que o movimento browniano padrão.
*   **Rough SABR:** Extensão do modelo estocástico SABR desenvolvida por Fukasawa e Gatheral que incorpora um núcleo fracionário singular, capturando a rugosidade da volatilidade.
*   **Swaption:** Opção que confere ao titular o direito de entrar em um contrato de *Interest Rate Swap* em uma data futura a uma taxa fixa pré-especificada.
*   **Taxa Forward Instantânea $f(t)$:** Taxa de juros aplicável a um investimento realizado no instante futuro $t$ por um período infinitesimal $dt$.
*   **Taxa Swap Par:** A taxa fixa de um swap que iguala o valor presente da perna fixa ao valor presente da perna flutuante no início do contrato.

---

## Citações Importantes com Contexto

### 1. Sobre a Fraqueza do Modelo SABR Clássico e a Motivação para o Rough SABR
> *"SABR implied volatility surfaces are, however, not really consistent with market data. In particular, the SABR implied volatility surface and its approximation by the SABR formula cannot reproduce the power-law type term structure of at-the-money (ATM) skew typically observed in markets. As a result, practitioners are forced to use different SABR parameters for different maturities."*
>
> — **Masaaki Fukasawa e Jim Gatheral (2022)**, em *A Rough SABR Formula*, Frontiers of Mathematical Finance.
>
> **Contexto:** Esta citação destaca a limitação central do modelo SABR clássico de Hagan (2002). Em dados reais de mercado, a inclinação do *smile* ATM decrece segundo uma lei de potência em relação à maturidade. Como o SABR clássico não possui esse decaimento estrutural, os operadores eram obrigados a recalibrar o modelo independentemente para cada vencimento. O Rough SABR resolve essa patologia unificando a superfície sob um único conjunto global de parâmetros.

### 2. Sobre o Propósito e a Superioridade do Método Monotone Convex
> *"In Hagan and West we introduced two new interpolation methods — the monotone convex method and the minimal method... highlight why this method has a very high pedigree in terms of the construction quality criteria that one should be interested in... ensures positive and continuous forward curves and preserves locality."*
>
> — **Patrick S. Hagan e Graeme West (2008)**, em *Methods for Constructing a Yield Curve*, Wilmott Magazine.
>
> **Contexto:** Hagan e West explicam por que os métodos tradicionais de interpolação (como *splines* cúbicas e interpolação linear) falham em aplicações práticas de mesa de operações. O método Monotone Convex foi explicitamente construído para resolver os problemas de taxas *forward* negativas, saltos descontínuos e contaminação de risco não local (*hedging espúrio*).

### 3. Sobre a Descontinuidade e Patologia da Interpolação Linear nas Taxas
> *"The function $r(t)t$ is clearly not differentiable at $t_i$ so that the function $f$ is undefined there which changes the slope frequently, therefore it is not suitable for yield curves... the forward has a jump at $t_i$ since the left and right limits are not equal."*
>
> — **Abdulhamid Iebesh (2020)**, em *Interpolation of Yield Curves*, Mälardalen University.
>
> **Contexto:** Análise matemática demonstrando por que a interpolação linear direta sobre as taxas zero nominais $r(t)$ é inaceitável para finanças quantitativas. A falta de diferenciação do produto $r(t)t$ gera saltos instantâneos e não físicos na curva de taxas *forward*, distorcendo o apreçamento de derivados de taxa.

---

## Insights Acionáveis

1.  **Eliminação Imediata de Splines Cúbicas no Bootstrap da Curva:**
    Mapeamentos de risco realizados sob *Natural Cubic Splines* propagam choques pontuais por toda a extensão da curva de juros. Recomenda-se a substituição imediata dos algoritmos de interpolação legados pelo **Monotone Convex Method**, que assegura localidade rigorosa ($l=2, u=2$), protegendo as estratégias de *immunization* e *hedging* por Key Rate Durations contra rebalanceamentos falsos.
2.  **Migração Obrigatória para Arquitetura Multi-Curva com Desconto OIS:**
    Sistemas de precificação de swaps e derivativos de taxa que ainda utilizam a mesma curva para projeção e desconto devem ser urgentemente atualizados. A curva de desconto deve ser purificada via **OIS / SOFR / CDI (B3)** para refletir o custo do colateral em acordos CSA, isolando as curvas de projeção de tenores ($1\text{M}, 3\text{M}, 6\text{M}$).
3.  **Adoção do Modelo de Bachelier em Ambientes de Juros Baixos/Negativos:**
    Para opções de taxas de juros (caps, floors e swaptions) negociadas em mercados de taxas de juros próximas de zero ou negativas, a parametrização lognormal de Black-76 deve ser abandonada em favor do **Modelo Normal de Bachelier**. Isso previne travamentos numéricos e elimina a necessidade de deslocamentos arbitrários (*shifted Black*).
4.  **Parametrização Global da Superfície de Volatilidade via Rough SABR:**
    Em vez de recalibrar modelos estocásticos fatia por fatia para cada maturidade, a equipe quantitativa deve adotar o **Rough SABR**. Utilizando a variável reescalonada $y(k, \tau) = \frac{\kappa(\tau) k}{U(\tau)}$, o modelo colapsa os *smiles* de todas as maturidades sobre uma única curva analítica universal $f_A(y)$, reduzindo dramaticamente o tempo computacional de calibração e preparando a superfície de volatilidade do Módulo M04 de forma consistente e livre de arbitragem.