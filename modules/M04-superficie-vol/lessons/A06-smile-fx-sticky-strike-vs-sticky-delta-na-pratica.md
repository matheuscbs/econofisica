<!-- imported from vault study notes; curated for open course -->
# M04.A06 — Smile FX: sticky strike vs sticky delta na prática

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M04
> **Aula:** M04.A06

↑ M04 · Resumo · Completo

**Módulo:** M04
**Pergunta do módulo:** Como ler, sanitizar e modelar a superfície de volatilidade?

## Conceito-núcleo
Dinâmica do smile FX: como a surface se move com o spot (sticky strike vs sticky delta).

## Aplicação em mercado / trading
Escolher regra de re-mark de IV após move do spot; impacto em P&L de estruturas FX.

## Entregável / lab
Experimento: reavaliar risk reversal sob sticky strike vs sticky delta após ±1% no spot.

## Fonte (mapeamento)
quantitative-trading-free-lesson/17 fx-smile-dynamics-from-delta-space-to-sticky-strike-vs-sticky-delta

## Guia de estudo aprofundado

> **info**
>

Este guia de estudo oferece uma síntese detalhada e estruturada sobre a mecânica de precificação e dinâmicas de superfície de volatilidade no mercado de câmbio (FX). O conteúdo aborda desde a convenção de deltas até as hipóteses de dinâmica da superfície (*sticky strike* versus *sticky delta*), fornecendo intuição de mercado, formulações matemáticas rigorosas, exercícios resolvidos e laboratório prático.

---

### Conceitos-Chave e Intuição de Mercado

#### 1. O Forward como Numeraire Base e o Modelo Garman-Kohlhagen
No mercado de FX, o preço *forward* não é um mero acessório, mas o ponto de partida fundamental. Ele representa o preço à vista (*spot*) carregado pelo diferencial de taxas de juros entre a moeda doméstica ($r_d$) e a moeda estrangeira ($r_f$). 
Toda a análise de *moneyness*, delta e interpolação de *smile* retorna ao *forward*. Na formulação de Garman-Kohlhagen, a moeda estrangeira atua exatamente como um rendimento contínuo de dividendos (*dividend yield*). O termo do *spot* é multiplicado por $e^{-r_f T}$ e o termo do *strike* por $e^{-r_d T}$. Confundir essa convenção equivale a aplicar um modelo de Black-Scholes de ações inapropriado ao mercado de FX, gerando precificação na moeda incorreta.

#### 2. Convenções de Delta Spot Delta vs. Forward Delta
As cotações de mercado em FX são estruturadas em termos de delta e não de *strikes* diretos. A interpretação de uma opção de "25-delta" depende estritamente da convenção adotada pelo mercado:
*   **Spot Delta ($\Delta^{\mathrm{call}}_{\mathrm{spot}}$):** Pondera o delta pelo fator de desconto da moeda estrangeira: $e^{-r_f T} N(d_1)$.
*   **Forward Delta ($\Delta^{\mathrm{call}}_{\mathrm{fwd}}$):** Considera diretamente a probabilidade acumulada na distribuição log-normal ajustada: $N(d_1)$.

Alterar a convenção de delta altera a condição sobre $d_1$, o que modifica o *strike* associado à cotação, mesmo que o valor nominal da volatilidade pareça idêntico no bilhete da operação (*ticket*).

#### 3. A Ponte Mercado-Modelo Transição de Delta para Strike
Enquanto o mercado opera e quota em espaço de delta (objeto de mercado), os modelos de precificação necessitam do *strike* $K$ (objeto do modelo). A conversão exige isolar $K$ na equação de $d_1$. Para opões de *put*, deve-se atentar que a cotação de mesa costuma referir-se ao valor absoluto do delta ($0.25$), enquanto o delta matemático da *put* é negativo.

#### 4. Linguagem do Desk Cotações de ATM, Risk Reversal (RR) e Butterfly (BF)
Uma mesa de negociação de FX não constrói o *smile* definindo múltiplos *strikes* arbitrários. O mercado quota três números principais para cada maturidade:
1.  **Volatilidade At-The-Money ($\sigma_{\mathrm{ATM}}$):** Define o nível central da superfície.
2.  **Risk Reversal 25-Delta ($RR25$):** Mede a assimetria ou *skew* da superfície ($\sigma_{25c} - \sigma_{25p}$).
3.  **Butterfly 25-Delta ($BF25$):** Mede a curvatura ou a atratividade das asas da superfície.

A partir desses três números, reconstroem-se os níveis de volatilidade das asas de call ($\sigma_{25c}$) e put ($\sigma_{25p}$).

#### 5. Espaço de Interpolação em Log-Moneyness
A interpolação dos pontos do *smile* para encontrar $\sigma(K)$ deve ser feita no espaço de *log-moneyness* $k = \ln(K/F)$. Como o *forward* move-se continuamente com o *carry* e com o *spot*, interpolar diretamente em *strikes* brutos faz com que a leitura relativa da superfície perca o sentido econômico. Ao construir a interpolação, o *forward* é absorvido pela função do *smile*, ancorando a superfície de volatilidade ao *forward* vigente.

#### 6. Dinâmicas de Superfície Sticky Strike vs. Sticky Delta
Quando o preço *spot* se move, a superfície de volatilidade se reconfigura. A forma como essa transição ocorre define o resultado financeiro (*PnL* de superfície):
*   **Sticky Strike:** Assume que a função de volatilidade $\sigma(K)$ permanece fixa em relação aos *strikes* nominais. Se o *spot* muda, a volatilidade associada a um *strike* contratado ($K_{\mathrm{track}}$) não se altera. O preço da opção varia exclusivamente pelo movimento do *spot*.
*   **Sticky Delta:** Assume que as cotações de mercado em delta ($\sigma_{\mathrm{ATM}}, RR25, BF25$) permanecem fixas. Com a mudança do *spot*, o *forward* muda ($F_0 \to F_1$), o que faz com que os *strikes* correspondentes aos deltas de 25c, 25p e ATM se desloquem. A superfície é reconstruída sobre os novos *strikes* e a opção contratada ($K_{\mathrm{track}}$) é precificada sob a nova curva reancorada.

---

### Fórmulas Fundamentais

#### Precificação e Forward
*   **Preço Forward FX:**
    $$F(0,T) = S_0 e^{(r_d - r_f)T}$$

#### Convenções de Delta (Call)
*   **Spot Delta:**
    $$\Delta^{\mathrm{call}}_{\mathrm{spot}} = e^{-r_f T} N(d_1)$$
*   **Forward Delta:**
    $$\Delta^{\mathrm{call}}_{\mathrm{fwd}} = N(d_1)$$

#### Transição de Forward Delta para Strike
Dado $N(d_1) = \Delta \implies d_1 = N^{-1}(\Delta)$, e sabendo que:
$$d_1 = \frac{\ln(F/K) + \frac{1}{2}\sigma^2 T}{\sigma\sqrt{T}}$$

Isolando o *strike* $K$:
$$K = F \exp\left(-\sigma\sqrt{T}d_1 + \frac{1}{2}\sigma^2 T\right)$$

#### Reconstrução das Asas (Wings)
*   **Volatilidade da Call 25-Delta:**
    $$\sigma_{25c} = \sigma_{\mathrm{ATM}} + BF25 + \frac{1}{2}RR25$$
*   **Volatilidade da Put 25-Delta:**
    $$\sigma_{25p} = \sigma_{\mathrm{ATM}} + BF25 - \frac{1}{2}RR25$$

#### Espaço de Moneyness e Paridade Call-Put
*   **Log-Moneyness:**
    $$k = \ln\left(\frac{K}{F}\right)$$
*   **Checagem de Paridade Call-Put:**
    $$C - P = S_0 e^{-r_f T} - K e^{-r_d T}$$

---

### Exemplo Numérico Resolvido Passo a Passo

#### Cenário de Mercado
Considere os seguintes dados para um par de moedas em $T = 1.0$ ano:
*   *Spot* inicial ($S_0$): $1.0000$
*   Taxa doméstica ($r_d$): $5.0\%$ ao ano ($0.05$)
*   Taxa estrangeira ($r_f$): $2.0\%$ ao ano ($0.02$)
*   Cotações de Mesa: $\sigma_{\mathrm{ATM}} = 10.0\%$, $RR25 = +1.0\%$, $BF25 = +0.5\%$

#### Passo 1 Cálculo do Preço Forward
$$F(0, 1.0) = 1.0000 \times e^{(0.05 - 0.02) \times 1.0} = 1.0000 \times e^{0.03} \approx 1.03045$$

#### Passo 2 Reconstrução da Volatilidade das Asas ($\sigma_{25c}$ e $\sigma_{25p}$)
*   **Call 25-Delta:**
    $$\sigma_{25c} = 0.100 + 0.005 + \frac{1}{2}(0.010) = 0.100 + 0.005 + 0.005 = 0.110 \text{ (ou } 11.0\% \text{)}$$
*   **Put 25-Delta:**
    $$\sigma_{25p} = 0.100 + 0.005 - \frac{1}{2}(0.010) = 0.100 + 0.005 - 0.005 = 0.095 \text{ (ou } 9.5\% \text{)}$$

#### Passo 3 Cálculo do Strike $K_{25c}$ usando Forward Delta
Para $\Delta = 0.25$, buscamos $d_1 = N^{-1}(0.25) \approx -0.6745$.
Aplicando a fórmula do *strike*:
$$K_{25c} = F \exp\left(-\sigma_{25c} \sqrt{T} d_1 + \frac{1}{2} \sigma_{25c}^2 T\right)$$
$$K_{25c} = 1.03045 \times \exp\left(-0.110 \times \sqrt{1.0} \times (-0.6745) + \frac{1}{2} (0.110)^2 \times 1.0\right)$$
$$K_{25c} = 1.03045 \times \exp\left(0.074195 + 0.00605\right)$$
$$K_{25c} = 1.03045 \times \exp(0.080245) \approx 1.03045 \times 1.08355 \approx 1.1165$$

O *strike* que corresponde exatamente à cotação de 25-delta call sob a convenção de *forward delta* é **$1.1165$**.

---

### Armadilhas Comuns

1.  **Confundir Convenções de Delta (Spot vs. Forward Delta):**
    Quotar uma opção assumindo *Forward Delta* quando a contraparte está operando sob *Spot Delta* altera o valor numérico de $d_1$ por meio do fator $e^{-r_f T}$. Isso resulta no cálculo de um *strike* incorreto e na precificação e *hedge* errôneos do bilhete.
2.  **Ignorar as Taxas de Juros na Formulação de Garman-Kohlhagen:**
    Tratar opões de câmbio como opções de ações sem dividendos faz com que os fatores de desconto $e^{-r_f T}$ no termo do *spot* e $e^{-r_d T}$ no termo do *strike* sejam esquecidos, conduzindo a erros de numeraire na moeda de liquidação.
3.  **Interpolação Direta no Espaço de Strike Bruto:**
    Ajustar a curva de volatilidade diretamente sobre $K$ sem utilizar o *log-moneyness* ($k = \ln(K/F)$) distorce a leitura dinâmica da superfície à medida que o *spot* e o *forward* oscilam no tempo.
4.  **Descuidar dos Sinais do Delta de Puts:**
    Tratar a cotação da put 25-delta com valor positivo $0.25$ nas equações matemáticas sem converter para a convenção correta de delta de put (que é negativo na formulação original) ocasiona inversão do *strike* e das asas.
5.  **Desalinhamento entre Modelo Interno e Mapeamento de Risco do Desk:**
    Utilizar um modelo interno de precificação baseado em *sticky strike* enquanto a carteira, os preços de mercado e a gestão de risco (*hedging*) são operados em baldes de *sticky delta*. Isso mascara a origem do PnL de superfície decorrente do movimento do *spot*.

---

### Laboratório Prático Sugerido em Python

Abaixo está o roteiro estruturado em passos conceituais para implementar a mecânica de superfície de volatilidade de FX em ambiente Python.

#### Passo 1 Construção do Forward e Garman-Kohlhagen
*   Implementar a função `fx_forward(S0, rd, rf, T)` retornando $S_0 e^{(r_d - r_f)T}$.
*   Implementar funções para precificação e delta sob Garman-Kohlhagen (`gk_call`, `gk_put`, `delta_spot_call`, `delta_fwd_call`).

#### Passo 2 Mapeamento de Delta Cotação para Strike Modelo
*   Implementar `strike_from_fwd_delta_call(S, rd, rf, T, sig, delta)` aplicando $d_1 = N^{-1}(\Delta)$ e retornando `F * exp(-sig * sqrt(T) * d1 + 0.5 * sig * sig * T)`.
*   Implementar `strike_from_fwd_delta_put` ajustando o sinal para o delta da *put*.

#### Passo 3 Reconstrução das Asas e Ancoragem do Smile
*   Calcular `sig_25c = sig_ATM + BF25 + 0.5 * RR25` e `sig_25p = sig_ATM + BF25 - 0.5 * RR25`.
*   Obter os *strikes* correspondentes: `K_25c`, `K_25p` e `K_ATM = F0`.
*   Criar a função `build_smile_interp(F, K_pts, sig_pts)` que constrói uma interpolação $\sigma(K)$ operando internamente no espaço de *log-moneyness* $k = \ln(K/F)$.

#### Passo 4 Simulação de Choque e Comparação Dinâmica (Sticky Strike vs. Sticky Delta)
*   Definir um choque de *spot* $S_0 \to S_1$, gerando um novo *forward* $F_1$.
*   **Sticky Strike:** Precificar uma opção rastreada em $K_{\mathrm{track}}$ com o novo *spot* $S_1$ mantendo a função `sigma_smile_0` original:
    ```python
    P_stickyK = price_with_smile(S1, F1, sigma_smile_0, K_track)
    ```
*   **Sticky Delta:** Recalcular os *strikes* de 25-delta call, 25-delta put e ATM para o novo *forward* $F_1$, reancorar o *smile* criando `sigma_smile_1` e precificar a mesma opção contratada ($K_{\mathrm{track}}$):
    ```python
    K1_25c = strike_from_fwd_delta_call(S1, rd, rf, T, sig_25c, 0.25)
    K1_25p = strike_from_fwd_delta_put(S1, rd, rf, T, sig_25p, 0.25)
    K1_ATM = F1
    sigma_smile_1 = build_smile_interp(
        F1,
        [K1_25p, K1_ATM, K1_25c],
        [sig_25p, sig_ATM, sig_25c],
    )
    P_stickyDelta = price_with_smile(S1, F1, sigma_smile_1, K_track)
    ```
*   **Diferencial de PnL:** Calcular a diferença `P_stickyDelta - P_stickyK` para quantificar o PnL de superfície resultante das dinâmicas do mercado.

#### Passo 5 Verificação de Paridade
*   Testar se os preços reconstruídos de call e put para um mesmo *strike* satisfazem rigorosamente a relação $C - P = S_0 e^{-r_f T} - K e^{-r_d T}$.

---

### Glossário

*   **Garman-Kohlhagen:** Adaptação do modelo de Black-Scholes para opções sobre moedas, considerando taxas de juros contínuas da moeda doméstica ($r_d$) e da moeda estrangeira ($r_f$).
*   **Forward Delta:** Convenção de delta em que $\Delta = N(d_1)$, expressando a probabilidade na distribuição log-normal sem o desconto da taxa estrangeira.
*   **Spot Delta:** Convenção de delta que inclui o fator de desconto da moeda estrangeira: $e^{-r_f T} N(d_1)$.
*   **Risk Reversal (RR25):** Medida de assimetria do *smile* de volatilidade expressa pela diferença de volatilidade entre a call de 25-delta e a put de 25-delta ($\sigma_{25c} - \sigma_{25p}$).
*   **Butterfly (BF25):** Medida de curvatura do *smile* de volatilidade, que reflete o nível médio das asas em relação à volatilidade ATM.
*   **Sticky Strike:** Hipótese de dinâmica de mercado na qual a volatilidade de um determinado *strike* nominal permanece constante quando o preço *spot* varia.
*   **Sticky Delta:** Hipótese de dinâmica na qual as volatilidades associadas a deltas fixos (ex: 25-delta) permanecem constantes, fazendo com que o *smile* deslize no espaço de *strike* junto com o movimento do *forward*.
*   **Log-Moneyness:** Variável dada por $k = \ln(K/F)$, utilizada para interpolar a superfície de volatilidade de maneira invariante ao deslocamento do *forward*.
*   **PnL de Superfície:** Parcela do resultado financeiro de uma carteira de opções decorrente da alteração da forma ou ancoragem da superfície de volatilidade após um movimento do *spot*.

---

### Questões de Fixação e Reflexão

#### Nível 1 Iniciante

**1. Qual é o papel do preço *forward* na construção da superfície de volatilidade em FX?**
> **Resposta:** O preço *forward* ($F = S_0 e^{(r_d-r_f)T}$) serve como numeraire central e ponto de ancoragem para a superfície. Ele reflete o *spot* corrigido pelo diferencial de juros, sendo a base necessária para calcular *moneyness*, converte cotações de delta em *strikes* e realizar a interpolação no espaço adequado.

**2. Como são calculadas as volatilidades das asas de 25-delta call e 25-delta put a partir das cotações de mesa?**
> **Resposta:** São calculadas combinando a volatilidade ATM, o Butterfly (BF25) e o Risk Reversal (RR25):
> $$\sigma_{25c} = \sigma_{\mathrm{ATM}} + BF25 + \frac{1}{2}RR25$$
> $$\sigma_{25p} = \sigma_{\mathrm{ATM}} + BF25 - \frac{1}{2}RR25$$

**3. O que acontece com o termo da moeda estrangeira na formulação de Garman-Kohlhagen em comparação com o modelo de Black-Scholes para ações?**
> **Resposta:** A taxa estrangeira ($r_f$) entra na equação de Garman-Kohlhagen com o mesmo papel do *dividend yield* contínuo em ações. O preço *spot* é descontado pelo fator $e^{-r_f T}$, enquanto o termo do *strike* é descontado pela taxa doméstica $e^{-r_d T}$.

---

#### Nível 2 Intermediário

**1. Qual é a diferença fundamental entre utilizar a convenção de *Spot Delta* e de *Forward Delta* no mapeamento de cotações?**
> **Resposta:** A convenção de *Forward Delta* define o delta como $N(d_1)$, enquanto o *Spot Delta* exige o fator de desconto estrangeiro $e^{-r_f T} N(d_1)$. Utilizar uma convenção no lugar da outra altera o valor necessário de $d_1$ para satisfazer a cotação de mercado, modificando diretamente o *strike* $K$ calculado e alterando a precificação e o *hedge* da estrutura.

**2. Por que a interpolação do *smile* de FX deve ser realizada em *log-moneyness* ($k = \ln(K/F)$) em vez do *strike* nominal ($K$)?**
> **Resposta:** Como o *forward* se desloca continuamente em função do tempo, do *spot* e do diferencial de juros, interpolar em *strikes* brutos perde a relação relativa de precificação. O *log-moneyness* garante que a superfície permaneça devidamente ancorada em termos relativos ao *forward* vigente.

**3. O que garante a checagem da paridade Call-Put na reconstrução do *smile*?**
> **Resposta:** A verificação da paridade ($C - P = S_0 e^{-r_f T} - K e^{-r_d T}$) confirma a consistência interna do modelo de precificação. Se a relação falhar, significa que o procedimento de interpolação ou conversão de *strikes* introduziu arbitragem ou inconsistências matemáticas na superfície reconstruída.

---

#### Nível 3 Avançado / Ensaio

**1. Explique passo a passo a diferença entre as dinâmicas de *Sticky Strike* e *Sticky Delta* quando ocorre uma oscilação no preço *spot*. Como essa diferença se materializa financeiramente no PnL de uma opção contratada?**
> **Resposta:** 
> Quando o *spot* oscila de $S_0$ para $S_1$, o preço *forward* altera-se de $F_0$ para $F_1$. 
> Na dinâmica **Sticky Strike**, assume-se que a curva de volatilidade $\sigma(K)$ construída no momento inicial permanece inalterada em relação aos *strikes* nominais. Ao reavaliar uma opção de *strike* $K_{\mathrm{track}}$, utiliza-se a volatilidade $\sigma_0(K_{\mathrm{track}})$ calculada no início. O PnL é gerado primariamente pela alteração do *spot* e da passagem do tempo.
> Na dinâmica **Sticky Delta**, assume-se que as cotações do mercado em delta ($\sigma_{\mathrm{ATM}}, RR25, BF25$) permanecem fixas. Com a mudança do *forward* para $F_1$, os *strikes* equivalentes aos deltas de 25-call, 25-put e ATM mudam para novos valores ($K1_{25c}, K1_{25p}, K1_{\mathrm{ATM}}$). Recontrói-se uma nova superfície de volatilidade $\sigma_1(K)$. A opção com *strike* original $K_{\mathrm{track}}$ é precificada com uma volatilidade diferente $\sigma_1(K_{\mathrm{track}})$.
> A diferença entre o preço calculado por *Sticky Delta* e o calculado por *Sticky Strike* representa o **PnL de Superfície**. Trata-se da fração do resultado financeiro decorrente puramente da regra de movimento da superfície de volatilidade, essencial para evitar descasamentos entre a gestão de risco da mesa (cotada em delta) e os modelos contábeis internos de precificação.

**2. Deduza matematicamente a fórmula do *strike* $K$ em função do *Forward Delta* de uma call ($\Delta$) e explique como a função $N^{-1}(\Delta)$ conecta a linguagem do mercado à precificação do modelo.**
> **Resposta:**
> A cotação de mercado do *Forward Delta* para uma call impõe que $\Delta = N(d_1)$.
> Aplicando a inversa da distribuição normal acumulada, obtemos:
> $$d_1 = N^{-1}(\Delta)$$
> Pela definição da variável $d_1$ no modelo de Garman-Kohlhagen expressa em termos do *forward* $F$:
> $$d_1 = \frac{\ln(F/K) + \frac{1}{2}\sigma^2 T}{\sigma\sqrt{T}}$$
> Multiplicando ambos os lados por $\sigma\sqrt{T}$:
> $$d_1 \sigma \sqrt{T} = \ln\left(\frac{F}{K}\right) + \frac{1}{2}\sigma^2 T$$
> Isolando o termo logarítmico:
> $$\ln\left(\frac{F}{K}\right) = -d_1 \sigma \sqrt{T} + \frac{1}{2}\sigma^2 T$$
> Aplicando a função exponencial em ambos os lados:
> $$\frac{F}{K} = \exp\left(-d_1 \sigma \sqrt{T} + \frac{1}{2}\sigma^2 T\right)$$
> Isolando o *strike* $K$:
> $$K = F \exp\left(-\sigma \sqrt{T} d_1 + \frac{1}{2}\sigma^2 T\right)$$
> Essa fórmula é a ponte direta entre o mercado e o modelo: ela pega uma cotação de delta ($\Delta$), que é uma condição sobre a probabilidade $d_1$, e a transforma no *strike* $K$ exato necessário para rodar as funções matemáticas de precificação.