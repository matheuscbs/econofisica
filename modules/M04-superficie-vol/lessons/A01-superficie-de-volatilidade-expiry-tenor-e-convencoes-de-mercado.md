<!-- imported from vault study notes; curated for open course -->
# M04.A01 — Superfície de volatilidade: expiry, tenor e convenções de mercado

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M04
> **Aula:** M04.A01

↑ M04 · Resumo · Completo

**Módulo:** M04
**Pergunta do módulo:** Como ler, sanitizar e modelar a superfície de volatilidade?

## Conceito-núcleo
IV surface: eixos expiry×tenor/strike; convenções (delta space, sticky) mudam a leitura.

## Aplicação em mercado / trading
Ler smile/skew cotado; comparar tenors; evitar misturar convenções FX vs equity.

## Entregável / lab
Montar grade IV (expiry × delta/strike) a partir de um book fictício ou snapshot público.

## Fonte (mapeamento)
quantitative-trading-free-lesson/12 the-volatility-surface-expiry-tenor-and-market-conventions

## Guia de estudo aprofundado

> **info**
>

### Conceitos-Chave Explicados em Profundidade

#### A Natureza da Volatilidade em Taxas de Juros vs. Ações
No mercado de ações (*equities*), o ativo subjacente é simples: observa-se o preço do papel $S_t$ ou $S_T$ e calcula-se a "volatilidade da ação". No mercado de taxas de juros, a volatilidade não é um parâmetro único nem a volatilidade de uma "taxa spot" abstrata. Transaciona-se a volatilidade de instrumentos *forward*, como taxas *forward* para *caplets* ou taxas *swap forward* para *swaptions*.

Em vez de perguntar "qual é a volatilidade?", a formulação rigorosa exige responder a três perguntas fundamentais:
1. Volatilidade de qual objeto subjacente?
2. Em qual data de vencimento (*expiry*)?
3. Sobre qual curva subjacente e com qual extensão temporal (*tenor*)?

#### Horizonte de Risco Data de Fixing vs. Data de Pagamento
Para um *caplet* associado ao período $[T_{i-1}, T_i]$, a incerteza do instrumento não reside na data de pagamento $T_i$ (quando ocorre a liquidação financeira do fluxo de caixa), mas sim na data de *fixing* ou *reset* $T_{i-1}$. É nessa data que o cupom flutuante é descoberto e a taxa deixa de oscilar. Portanto, o horizonte de risco relevante $\tau_i$ em fórmulas de precificação como Black ou Bachelier é dado por:

$$\tau_i = T_{i-1}$$

Para uma *swaption* com data de vencimento $T_0$, o titular possui o direito de entrar ou não em um *swap* a partir dessa data. A incerteza do instrumento é o valor da taxa *swap forward* no momento do exercício $T_0$. A vida do *swap* subjacente ocorre após $T_0$, mas a opção é exercida estritamente em $T_0$. Logo, o horizonte de risco da *swaption* é $T_0$.

#### A Superfície Bidimensional Expiry e Tenor
Devido à variedade de objetos e prazos, a cotação de volatilidade em taxas de juros é organizada em uma superfície bidimensional composta por dois eixos concretos:
* **Eixo de Expiry (Vencimento):** O tempo até o *fixing* do *caplet* ou até o exercício da *swaption*.
* **Eixo de Tenor (Prazo Subjacente):** A duração do *swap* subjacente (para *swaptions*) ou a maturidade do *cap* (para *caps*).

A notação $1Y \times 5Y$ representa uma opção que vence em 1 ano sobre um *swap* com duração de 5 anos a partir do exercício (período total coberto no calendário de 6 anos). Essa estrutura difere do instrumento $10Y \times 1Y$ (opção de 10 anos sobre *swap* de 1 ano), pois o local e o impacto temporal da incerteza são completamente distintos.

```
       Superfície de Volatilidade de Swaptions
       
 Tenor (X) ^
           |  (1Y x 10Y) -> Opção curta, Swap longo
       10Y |  [ σ_1Y,10Y ] . . . . . . . . [ σ_10Y,10Y ]
        5Y |  [ σ_1Y,5Y  ] . . . . . . . . [ σ_10Y,5Y  ]
        2Y |  [ σ_1Y,2Y  ] . . . . . . . . [ σ_10Y,2Y  ]
        1Y |  [ σ_1Y,1Y  ] . . . . . . . . [ σ_10Y,1Y  ]  <-- (10Y x 1Y) Opção longa, Swap curto
           +---------------------------------------->
              1Y        2Y     3Y     5Y     10Y    Expiry (E)
```

#### Convenções de Volatilidade Black vs. Bachelier
A escolha do modelo subjacente altera a definição e a unidade da volatilidade cotada:

* **Convenção de Black (Lognormal):** Assume que a taxa *forward* $F$ ou a taxa *swap forward* $S$ segue um processo lognormal ($dF = \sigma F dW$). O modelo utiliza termos logarítmicos como $\ln(F/K)$ e força estruturalmente as taxas a se manterem positivas. A volatilidade de Black $\sigma_B$ é **adimensional** (porcentagem anual).
* **Convenção de Bachelier (Normal):** Assume que o subjacente segue um processo normal ($dF = \sigma_N dW$). O modelo admite taxas nulas ou negativas e utiliza termos diretos de diferença $(F-K)$ combinados com a densidade normal. A volatilidade normal $\sigma_N$ é expressa em **unidades de taxa** (tipicamente pontos-base por raiz quadrada de ano, ou $\text{bps}/\sqrt{\text{ano}}$).

#### Cotações de Mercado vs. Parâmetros de Modelo
As volatilidades observadas no mercado são cotações implícitas e não parâmetros isolados de um modelo estrutural:
* Uma cotação de volatilidade de um *cap* de 5 anos refere-se a uma *strip* completa de *caplets*. Para obter as volatilidades dos *caplets* individuais, é necessário realizar um processo de *bootstrapping* (desdobramento da *strip*).
* As *swaptions* cobrem simultaneamente múltiplas maturidades com estrutura correlacionada e convexa. Por essa razão, são os instrumentos primários para calibração de modelos de estrutura a termo, como Hull-White, Heath-Jarrow-Morton (HJM) e LIBOR Market Model (LMM).

---

### Formulação Matemática e Métricas em LaTeX

#### Anuidade e Taxa Swap Forward
Para um *swap* iniciado em $T_0$ e com vencimento em $T_n$, considerando datas de pagamento $T_1, T_2, \dots, T_n$ e frações de ano $\delta_k$, a anuidade $A(0)$ é definida por:

$$A(0) = \sum_{k=1}^n \delta_k P(0, T_k)$$

Onde $P(0, T)$ representa o fator de desconto para a maturidade $T$.

A taxa *swap forward* par $S(0)$ é dada por:

$$S(0) = \frac{P(0, T_0) - P(0, T_n)}{A(0)}$$

#### Precificação ATM sob a Convenção de Black
No ponto At-The-Money (ATM), onde o strike $K = S(0)$, a fórmula de precificação de uma *swaption* sob o modelo de Black simplifica-se. Definindo o desvio padrão acumulado $v = \sigma_B \sqrt{T_0}$:

$$d_1 = \frac{1}{2} v = \frac{1}{2} \sigma_B \sqrt{T_0}$$

$$d_2 = -\frac{1}{2} v = -\frac{1}{2} \sigma_B \sqrt{T_0}$$

O Valor Presente (PV) de uma *swaption* ATM com nocional $N$ é:

$$PV_{\text{Black}}^{\text{ATM}} = N \cdot A(0) \cdot S(0) \cdot \left[ N(d_1) - N(d_2) \right]$$

Onde $N(x)$ é a função de distribuição acumulada da normal padrão.

#### Precificação ATM sob a Convenção de Bachelier
Sob a convenção normal de Bachelier no ponto ATM ($K = S(0)$), a diferença $x = F - K = 0$. A fórmula em forma fechada para o PV é:

$$PV_{\text{Bachelier}}^{\text{ATM}} = N \cdot A(0) \cdot \sigma_N \cdot \sqrt{T_0} \cdot \varphi(0)$$

Onde $\varphi(0)$ é a densidade da distribuição normal padrão calculada em zero:

$$\varphi(0) = \frac{1}{\sqrt{2\pi}} \approx 0,398942$$

#### O Efeito Nível e Conversão por Price-Matching
O desvio padrão absoluto das variações de taxa varia entre os dois modelos:
* No modelo Lognormal (Black):
$$\operatorname{Std}(F) \approx \sigma_B \cdot F \cdot \sqrt{T}$$
* No modelo Normal (Bachelier):
$$\operatorname{Std}(F) \approx \sigma_N \cdot \sqrt{T}$$

Quando o nível da taxa $F$ ou $S(0)$ reduz-se, o desvio padrão absoluto no modelo de Black diminui mecanicamente.

Para converter uma cotação de volatilidade de Black em uma volatilidade normal equivalente ($\sigma_N^{\text{equiv}}$) no ponto ATM, igualam-se os preços das duas convenções (*price matching*):

$$PV_{\text{Black}}^{\text{ATM}} = PV_{\text{Bachelier}}^{\text{ATM}}$$

$$N \cdot A(0) \cdot S(0) \cdot \left[ N(d_1) - N(d_2) \right] = N \cdot A(0) \cdot \sigma_N^{\text{equiv}} \cdot \sqrt{T_0} \cdot \varphi(0)$$

Isolando $\sigma_N^{\text{equiv}}$:

$$\sigma_N^{\text{equiv}} = \frac{PV_{\text{Black}}^{\text{ATM}}}{N \cdot A(0) \cdot \sqrt{T_0} \cdot \varphi(0)}$$

---

### Intuição de Mercado e Trading

#### Leitura das Estruturas Assimétricas ($1Y \times 10Y$ vs. $10Y \times 1Y$)
* **$1Y \times 10Y$ (Opção Curta sobre Swap Longo):** O comprador possui apenas 1 ano de incerteza sobre o momento do exercício, mas assume o risco de um *swap* de 10 anos. Este contrato expõe o detentor à dinâmica de taxas de longo prazo com baixo custo temporal da opção.
* **$10Y \times 1Y$ (Opção Longa sobre Swap Curto):** O comprador carrega 10 anos de incerteza do tempo até o exercício, porém o objeto subjacente dura apenas 1 ano. A incerteza está concentrada nonde a taxa de curto prazo estará daqui a uma década.

#### Seleção de Convenção em Regimes de Taxas
* **Taxas Altas/Positivas:** A volatilidade de Black permanece funcional e fornece uma métrica percentual intuitiva.
* **Taxas Baixas ou Negativas:** A volatilidade de Black falha devido ao termo $\ln(F/K)$ e à compressão do desvio padrão absoluto ($\sigma_B F \sqrt{T}$). Nesses regimes, o mercado adota universalmente a volatilidade normal de Bachelier ($\text{bps}/\sqrt{\text{ano}}$), pois ela preserva a estabilidade das cotações sem quebrar as fórmulas matemáticas ao cruzar o zero.

#### Smile e Skew de Volatilidade
A volatilidade implícita não é constante ao longo dos strikes. As opções *Payer* (direito de pagar taxa fixa) e *Receiver* (direito de receber taxa fixa) habitam cauda distintas da distribuição:
* Se o mercado percebe maior risco ou demanda maior prêmio para altas abruptas nas taxas em relação a quedas acentuadas, a superfície apresentará uma assimetria (*skew*).
* Fenômenos como reversão à média das taxas de juros, barreiras operacionais do limite zero/negativo e correlações entre taxas *forward* de diferentes vértices geram padrões estruturados de *smile*, especialmente visíveis em expiries longas.

---

### Exemplo Numérico Resolvido Passo a Passo

#### Dados de Entrada
Considere a precificação de uma *swaption* ATM $1Y \times 1Y$ (vencimento $T_0 = 1,0$ ano, tenor $X = 1,0$ ano, vencimento final do *swap* $T_n = 2,0$ anos) com pagamentos semestrais ($\text{freq} = 2$, $\delta = 0,5$).

* Nocional: $N = 10.000.000$ USD
* Curva de fatores de desconto $P(0, T)$ dada pelos pontos:
  * $P(0; 1,0) = 0,9750$
  * $P(0; 2,0) = 0,9450$
* Interpolador log-linear para encontrar $P(0; 1,5)$:
  $$\ln P(0; 1,0) = \ln(0,9750) \approx -0,025318$$
  $$\ln P(0; 2,0) = \ln(0,9450) \approx -0,056570$$
  $$\ln P(0; 1,5) = 0,5 \cdot (-0,025318) + 0,5 \cdot (-0,056570) = -0,040944$$
  $$P(0; 1,5) = e^{-0,040944} \approx 0,959883$$
* Volatilidade de Black cotada na superfície: $\sigma_B(1Y, 1Y) = 0,35$ ($35,0\%$)

---

#### Passo 1 Cálculo da Anuidade $A(0)$
As datas de pagamento do *swap* são $T_1 = 1,5$ e $T_2 = 2,0$, ambas com fração de ano $\delta_k = 0,5$.

$$A(0) = \delta_1 P(0; 1,5) + \delta_2 P(0; 2,0)$$

$$A(0) = 0,5 \cdot 0,959883 + 0,5 \cdot 0,9450 = 0,4799415 + 0,472500 = 0,9524415$$

---

#### Passo 2 Cálculo da Taxa Swap Forward Par $S(0)$

$$S(0) = \frac{P(0; 1,0) - P(0; 2,0)}{A(0)} = \frac{0,9750 - 0,9450}{0,9524415} = \frac{0,0300}{0,9524415} \approx 0,031500 \quad (3,1500\%)$$

Como a opção é ATM, o strike $K = S(0) = 0,031500$.

---

#### Passo 3 Precificação sob o Modelo de Black ($PV_{\text{Black}}$)
Calculam-se os parâmetros $v$, $d_1$ e $d_2$:

$$v = \sigma_B \sqrt{T_0} = 0,35 \cdot \sqrt{1,0} = 0,35$$

$$d_1 = 0,5 \cdot v = 0,175$$

$$d_2 = -0,5 \cdot v = -0,175$$

Consultando a tabela da normal padrão $N(x)$:
* $N(0,175) \approx 0,569460$
* $N(-0,175) \approx 0,430540$
* $N(d_1) - N(d_2) = 0,569460 - 0,430540 = 0,138920$

Cálculo do PV de Black:

$$PV_{\text{Black}} = N \cdot A(0) \cdot S(0) \cdot [N(d_1) - N(d_2)]$$

$$PV_{\text{Black}} = 10.000.000 \cdot 0,9524415 \cdot 0,031500 \cdot 0,138920 \approx 41.714,24 \text{ USD}$$

---

#### Passo 4 Conversão para Volatilidade Normal Equivalente ($\sigma_N {\text{equiv}}$)
Utiliza-se a fórmula de *price matching* no ponto ATM:

$$\sigma_N^{\text{equiv}} = \frac{PV_{\text{Black}}}{N \cdot A(0) \cdot \sqrt{T_0} \cdot \varphi(0)}$$

Sabendo que $\varphi(0) = \frac{1}{\sqrt{2\pi}} \approx 0,398942$:

$$\text{Denominador} = 10.000.000 \cdot 0,9524415 \cdot \sqrt{1,0} \cdot 0,398942 \approx 3.799.691,48$$

$$\sigma_N^{\text{equiv}} = \frac{41.714,24}{3.799.691,48} \approx 0,010978$$

A volatilidade normal equivalente é de **0,010978** em unidades de taxa, o que corresponde a **109,78 bps/ano** ($\text{bps}/\sqrt{\text{ano}}$).

---

### Armadilhas Comuns

1. **Confundir Horizonte de Fixing com Data de Pagamento:** Considerar $T_i$ (data de pagamento do cupom) em vez de $T_{i-1}$ (data de *fixing*) como o parâmetro de tempo $\tau_i$ nas equações de precificação de *caplets*. O risco encerra-se no *fixing*.
2. **Tratar Cotações de Mercado como Parâmetros Isolados:** Inserir a cotação de volatilidade de um *cap* de 5 anos diretamente em uma fórmula de *caplet* sem realizar o *bootstrapping* da *strip*.
3. **Comparar Diretamente Volatilidade de Black e Bachelier:** Assumir que uma volatilidade de Black de $30\%$ e uma volatilidade Normal de $100\text{ bps}$ representam o mesmo número expressado em unidades diferentes sem ajustar pelo nível da taxa $S(0)$.
4. **Ignorar a Estrutura Curva Dupla em Ambientes Reais:** Projetar taxas *forward* utilizando a mesma curva usada para desconto de fluxos. Em mercados modernos, o desconto é realizado via OIS (ex: SOFR), enquanto a projeção do subjacente utiliza a curva do índice de referência.
5. **Acreditar na Reversibilidade de $1Y \times 10Y$ e $10Y \times 1Y$:** Assumir equivalência entre nós da superfície que somam a mesma maturidade final. Os perfis de gama, vega e incerteza temporal são totalmente distintos.

---

### Laboratório Prático em Python

Este laboratório descreve passo a passo a construção do script em Python para manipular a superfície de volatilidade, precificar *swaptions* ATM sob Black e Bachelier e converter as volatilidades via *price matching*.

#### Passo 1 Configuração das Grades e Entradas
Defina a grade de expiries $E \in \{1, 2, 3, 5, 10\}$, a grade de tenors $X \in \{1, 2, 5, 10\}$ e o nocional $N = 10.000.000$. Inicialize as matrizes bidimensionais de volatilidade de Black $\sigma_B(E, X)$ (adimensional) e de volatilidade Normal $\sigma_N(E, X)$ (em unidades de taxa).

#### Passo 2 Construção da Curva de Desconto com Interpolador Log-Linear
Defina os vetores de vértices da curva `T_grid` e fatores de desconto `P_grid`. Implemente a função `P0(T)` que realiza a interpolação log-linear:
$$\ln P(T) = \text{interpolação linear de } \ln(P_{\text{grid}}) \text{ em relação a } T_{\text{grid}}$$

#### Passo 3 Construção da Função de Objetos de Swap
Crie a função `build_swap_objects(expiry, tenor, freq=2)`. Ela deve:
1. Definir $T_0 = \text{expiry}$ e $T_n = \text{expiry} + \text{tenor}$.
2. Gerar as datas de pagamento $T_k$ com o passo $1/\text{freq}$.
3. Calcular a anuidade $A(0) = \sum \delta_k P(0, T_k)$.
4. Calcular a taxa *swap forward* par $S(0) = \frac{P(0, T_0) - P(0, T_n)}{A(0)}$.

#### Passo 4 Implementação das Funções de Precificação ATM
Crie as funções de precificação fechada para o ponto ATM:
* `black_atm_swaption(N, A0, S0, sigma, T0)`: calcula $v = \sigma \sqrt{T_0}$, $d_1 = 0,5v$, $d_2 = -0,5v$ e retorna $N \cdot A_0 \cdot S_0 \cdot (N(d_1) - N(d_2))$.
* `bach_atm_swaption(N, A0, sigmaN, T0)`: retorna $N \cdot A_0 \cdot \sigma_N \cdot \sqrt{T_0} \cdot \varphi(0)$.

#### Passo 5 Execução do Loop de Precificação e Conversão de Volatilidade
Percorra todos os nós $(E, X)$ da grade:
1. Obtenha $A_0$ e $S_0$ chamando `build_swap_objects`.
2. Precifique a *swaption* sob Black e Bachelier.
3. Armazene os valores em matrizes `PV_black` e `PV_norm`.
4. Calcule a volatilidade normal equivalente por *price matching*:
   $$\sigma_N^{\text{equiv}}[i, j] = \frac{PV_{\text{black}}[i, j]}{N \cdot A_0 \cdot \sqrt{E} \cdot \varphi(0)}$$

#### Passo 6 Diagnósticos da Estrutura a Termo e Tenor
Extraia cortes da matriz resultante para análise de mercado:
* **Estrutura a Termo:** Mantenha o tenor fixo (ex: $X = 10Y$) e imprima aevolução de $\sigma_B$ e $\sigma_N^{\text{equiv}}$ ao longo dos expiries $E$.
* **Estrutura de Tenor:** Mantenha o expiry fixo (ex: $E = 2Y$) e imprima a relação entre os tenors $X$, a volatilidade $\sigma_B$ e o nível da taxa $S(0)$.

```python
import numpy as np
from math import log, sqrt
from scipy.stats import norm

## ---------------------------------------------------------
## Passo 1 Entradas e Grades de Mercado
## ---------------------------------------------------------
Nn = 10_000_000
expiries = np.array(, dtype=float)
tenors   = np.array(, dtype=float)

sigma_B = np.array([
    [0.35, 0.33, 0.30, 0.28],
    [0.32, 0.30, 0.28, 0.26],
    [0.30, 0.28, 0.26, 0.24],
    [0.27, 0.25, 0.23, 0.21],
    [0.22, 0.20, 0.19, 0.18],
], dtype=float)

sigma_N = np.array([
    [0.015, 0.014, 0.013, 0.012],
    [0.014, 0.013, 0.012, 0.011],
    [0.013, 0.012, 0.011, 0.010],
    [0.012, 0.011, 0.010, 0.009],
    [0.010, 0.009, 0.0085, 0.008],
], dtype=float)

## ---------------------------------------------------------
## Passo 2 Curva de Desconto e Interpolação Log-Linear
## ---------------------------------------------------------
T_grid = np.array([0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0], dtype=float)
P_grid = np.array([1.0, 0.9900, 0.9750, 0.9450, 0.9100, 0.8500, 0.7200, 0.5200], dtype=float)

def P0(T):
    T = float(T)
    if T <= T_grid:
        return float(P_grid)
    if T >= T_grid[-1]:
        return float(P_grid[-1])
    return float(np.exp(np.interp(T, T_grid, np.log(P_grid))))

## ---------------------------------------------------------
## Passo 3 Construção dos Objetos do Swap (Anuidade e Swap Rate)
## ---------------------------------------------------------
def build_swap_objects(expiry, tenor, freq=2):
    T0 = float(expiry)
    Tn = float(expiry + tenor)
    step = 1.0 / freq
    pay_dates = np.arange(T0 + step, Tn + 1e-12, step)
    deltas = np.full_like(pay_dates, step, dtype=float)
    A0 = float(np.sum(deltas * np.array([P0(t) for t in pay_dates], dtype=float)))
    S0 = (P0(T0) - P0(Tn)) / A0
    return A0, S0, Tn

## ---------------------------------------------------------
## Passo 4 Funções de Precificação ATM
## ---------------------------------------------------------
def black_atm_swaption(N, A0, S0, sigma, T0):
    v = sigma * sqrt(T0)
    d1 = 0.5 * v
    d2 = -0.5 * v
    return N * A0 * (S0 * norm.cdf(d1) - S0 * norm.cdf(d2))

def bach_atm_swaption(N, A0, sigmaN, T0):
    return N * A0 * sigmaN * sqrt(T0) * norm.pdf(0.0)

## ---------------------------------------------------------
## Passo 5 Avaliação da Grade e Price Matching
## ---------------------------------------------------------
PV_black = np.zeros((len(expiries), len(tenors)))
PV_norm  = np.zeros((len(expiries), len(tenors)))
A_mat = np.zeros_like(PV_black)
S_mat = np.zeros_like(PV_black)

for i, E in enumerate(expiries):
    for j, X in enumerate(tenors):
        A0, S0, _ = build_swap_objects(E, X, freq=2)
        A_mat[i, j] = A0
        S_mat[i, j] = S0
        PV_black[i, j] = black_atm_swaption(Nn, A0, S0, sigma_B[i, j], E)
        PV_norm[i, j] = bach_atm_swaption(Nn, A0, sigma_N[i, j], E)

phi0 = norm.pdf(0.0)
sigmaN_equiv = np.zeros_like(PV_black)
for i, E in enumerate(expiries):
    for j in range(len(tenors)):
        sigmaN_equiv[i, j] = PV_black[i, j] / (Nn * A_mat[i, j] * sqrt(E) * phi0)

## ---------------------------------------------------------
## Passo 6 Impressão de Diagnósticos Curva/Tenor
## ---------------------------------------------------------
j10 = np.where(tenors == 10)
print("Estrutura a Termo (Tenor=10Y):")
print("Black Vol:", list(zip(expiries, sigma_B[:, j10])))
print("Eq Normal Vol:", list(zip(expiries, sigmaN_equiv[:, j10])))

i2 = np.where(expiries == 2)
print("\nEstrutura de Tenor (Expiry=2Y):")
print("Black Vol:", list(zip(tenors, sigma_B[i2, :])))
print("Swap Rate S0:", list(zip(tenors, S_mat[i2, :])))
```

---

### Glossário de Termos Importantes

* **Anuidade ($A(0)$):** A soma ponderada pelos fatores de desconto $P(0, T_k)$ das frações de ano $\delta_k$ das datas de pagamento do *swap*. Representa o valor presente de um ponto base ($1 \text{ bps}$) do *swap*.
* **Bachelier (Modelo Normal):** Modelo de precificação de opções que assume variações normais para o ativo subjacente ($dF = \sigma_N dW$). Permite taxas de juros nulas ou negativas e expressa volatilidade em unidades absolutas de taxa.
* **Black (Modelo Lognormal):** Modelo padrão histórico de precificação que assume distribuição lognormal para a taxa *forward* ($dF = \sigma F dW$). A volatilidade é dada em percentual adimensional.
* **Bootstrapping de Volatilidade:** Procedimento estrutural de extração de volatilidades de *caplets* individuais a partir das cotações de volatilidade de *caps* (que representam uma sequência ou *strip* de *caplets*).
* **Caplet:** Opção de compra (call) sobre uma taxa de juros referente a um único período de *fixing*.
* **Efeito Nível (Level Effect):** Fenômeno pelo qual a volatilidade absoluta de um modelo lognormal diminui proporcionalmente quando o nível da taxa $F$ reduz-se, exigindo ajustes ou transição para convenção normal.
* **Expiry (Data de Vencimento):** O tempo remanescente até a data de *fixing* de um *caplet* ou até a data de exercício de uma *swaption*.
* **Price Matching:** Método de conversão entre convenções de volatilidade (ex: Black para Bachelier) que consiste em encontrar o parâmetro de volatilidade que reproduz exatamente o mesmo valor presente (PV) para a opção.
* **Skew / Smile de Volatilidade:** Padrão não plano da volatilidade implícita ao longo dos strikes para uma mesma maturidade, refletindo assimetrias na probabilidade percebida de altas ou quedas das taxas.
* **Swaption:** Opção que concede ao titular o direito de entrar em um *interest rate swap* (pagando ou recebendo taxa fixa) a uma taxa de exercício predeterminada em uma data futura.
* **Tenor:** A duração ou prazo do instrumento subjacente (extensão temporal do *swap* no caso de *swaptions* ou maturidade do *cap* no caso de *caps*).

---

### Questões de Prática e Avaliação

#### Nível 1 Questões de Resposta Curta
1. Por que o horizonte de risco relevante de um *caplet* referente ao período $[T_{i-1}, T_i]$ é $T_{i-1}$ e não $T_i$?
2. Qual a principal diferença física/dimensional entre a cotação de volatilidade no modelo de Black e no modelo de Bachelier?
3. O que significam os dois números na notação de uma *swaption* $2Y \times 5Y$?
4. Como o modelo de Bachelier contorna a limitação matemática do modelo de Black em ambientes de taxas de juros negativas?

#### Nível 2 Questões Práticas e Numéricas
1. Considere uma *swaption* ATM com vencimento $T_0 = 4,0$ anos. A anuidade calculada da curva é $A(0) = 4,50$, o nocional é $N = 10.000.000$ USD e a volatilidade normal cotada é $\sigma_N = 0,0120$ ($120 \text{ bps}/\sqrt{\text{ano}}$). Calcule o valor presente ($PV_{\text{Bachelier}}^{\text{ATM}}$) do instrumento utilizando a fórmula de Bachelier.
2. Explique a diferença de alocação de risco entre um contrato $1Y \times 10Y$ e um contrato $10Y \times 1Y$. Qual dos dois carrega maior incerteza quanto à taxa do *swap* subjacente e qual possui maior incerteza quanto ao tempo de exercício?
3. Demonstre matematicamente por que o desvio padrão absoluto de uma taxa $F$ tende a zero sob o modelo de Black quando $F \to 0$, e por que isso não ocorre sob o modelo de Bachelier.

#### Nível 3 Prompts para Ensaios e Análise Crítica
1. **Análise de Calibração e Estrutura de Mercado:** "As cotações da superfície de volatilidade não representam parâmetros isolados de um modelo, mas sim cotações implícitas de instrumentos compostos." Discuta essa afirmação focando na diferença entre o *bootstrapping* de volatilidades de *caplets* a partir de *caps* e a calibração de modelos estruturais de taxa de juros (como Hull-White e LMM) a partir da superfície de *swaptions*.
2. **Impacto de Regimes de Taxas e Convenções:** Avalie a transição histórica dos mercados globais da convenção de Black para a convenção de Bachelier durante regimes de taxas de juros extremamente baixas ou negativas. Analise o impacto na leitura do *smile* de volatilidade, o efeito de nível (*level effect*) sobre a gestão de risco de carteiras de derivativos e a necessidade de separar as curvas de desconto e projeção (OIS vs. Índice).

---

### Gabarito e Respostas Comentadas

#### Respostas do Nível 1
1. **Resposta:** A incerteza da taxa flutuante é totalmente resolvida na data de *fixing* $T_{i-1}$ (quando o cupom é determinado). A data $T_i$ representa apenas o momento do pagamento do fluxo de caixa descontado, sem introduzir nova volatilidade à taxa.
2. **Resposta:** A volatilidade de Black é adimensional (uma taxa percentual anual $\sigma_B$), enquanto a volatilidade de Bachelier possui dimensão de unidade de taxa (expressa em pontos-base por raiz quadrada de ano, $\sigma_N$).
3. **Resposta:** $2Y$ (expiry) indica que a opção vence em 2 anos; $5Y$ (tenor) indica que o *swap* subjacente terá duração de 5 anos a partir da data de exercício.
4. **Resposta:** O modelo de Bachelier modela a variação absoluta da taxa através de um processo normal ($dF = \sigma_N dW$), o que permite que $F$ assuma valores menores ou iguais a zero sem gerar erros logarítmicos ($\ln(F/K)$ inexistente para valores negativos).

#### Respostas do Nível 2
1. **Resposta Numérica:**
   * $N = 10.000.000$
   * $A(0) = 4,50$
   * $\sigma_N = 0,0120$
   * $T_0 = 4,0 \implies \sqrt{T_0} = 2,0$
   * $\varphi(0) = \frac{1}{\sqrt{2\pi}} \approx 0,3989423$
   
   $$PV = N \cdot A(0) \cdot \sigma_N \cdot \sqrt{T_0} \cdot \varphi(0)$$
   $$PV = 10.000.000 \cdot 4,50 \cdot 0,0120 \cdot 2,0 \cdot 0,3989423 \approx 430.857,68 \text{ USD}$$

2. **Resposta:**
   * No contrato $1Y \times 10Y$, a incerteza do tempo de exercício é curta (1 ano), mas o objeto exposto é um *swap* longo de 10 anos (alta sensibilidade à curva de longo prazo/duração).
   * No contrato $10Y \times 1Y$, a incerteza sobre a data de exercício é longa (10 anos de espera até saber onde as taxas estarão), mas o objeto subjacente é um *swap* curto de 1 ano. 
   * A incerteza temporal do exercício é maior no $10Y \times 1Y$, enquanto a volatilidade do valor do *swap* subjacente após o exercício é maior no $1Y \times 10Y$.

3. **Resposta Matemática:**
   * No modelo de Black, a dinâmica é $dF = \sigma_B F dW$, de modo que a variância do processo é $\operatorname{Var}(dF) = \sigma_B^2 F^2 dt$, fornecendo um desvio padrão absoluto $\operatorname{Std}(F) \approx \sigma_B F \sqrt{T}$. Conforme $F \to 0$, $\operatorname{Std}(F) \to 0$.
   * No modelo de Bachelier, a dinâmica é $dF = \sigma_N dW$, de modo que a variância do processo é $\operatorname{Var}(dF) = \sigma_N^2 dt$, e o desvio padrão absoluto é $\operatorname{Std}(F) \approx \sigma_N \sqrt{T}$, sendo totalmente independente do nível de $F$.

#### Respostas do Nível 3
1. **Diretrizes para a Resposta do Ensaio:**
   * O candidato deve explicar que uma cotação de *cap* (ex: 5Y) envolve uma série temporal de múltiplos *caplets*. Como cada *caplet* possui seu próprio vencimento $T_{i-1}$, a cotação do *cap* é uma média ponderada implícita da volatilidade dessa sequência. O *bootstrapping* descola sequencialmente cada *caplet* $i$ isolando seu preço do acumulado dos *caplets* anteriores.
   * Em relação às *swaptions*, o candidato deve explicitar que elas cobrem áreas retangulares da superfície $(\text{expiry} \times \text{tenor})$. Como um *swap* de tenor longo atravessa múltiplos fatores de taxa *forward*, a volatilidade de uma *swaption* depende não apenas das volatilidades individuais das taxas *forward*, mas da correlação entre elas e do efeito de anuidade/convexidade. Assim, modelos de estrutura a termo (como Hull-White ou LMM) são calibrados minimizando a diferença entre os preços teóricos e os preços de mercado da grade de *swaptions*, ajustando parâmetros de volatilidade instantânea e correlação.

2. **Diretrizes para a Resposta do Ensaio:**
   * **Contexto e Transição:** Explicar que, com o advento de taxas de juros próximas de zero ou negativas, a convenção de Black tornou-se inviável devido à impossibilidade de calcular $\ln(F/K)$ para $F \le 0$ ou $K \le 0$ e ao colapso do desvio padrão absoluto.
   * **Efeito Nível:** Demonstrar como a volatilidade de Black explode artificialmente quando $F \to 0$ para compensar a precificação de um movimento absoluto real no mercado, enquanto a volatilidade de Bachelier ($\text{bps}/\sqrt{\text{ano}}$) permanece estável e interpretável.
   * **Estrutura de Curva:** Destacar que o modelo de precificação moderno exige desacoplar a curva de desconto (obtida via swaps OIS, refletindo o custo de colateral e livre de risco de crédito) da curva de projeção das taxas *forward* (índices como SOFR ou IBOR). A superfície de volatilidade deve ser construída e indexada rigorosamente respeitando esse arcabouço de curvas distintas.