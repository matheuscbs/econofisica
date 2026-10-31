<!-- imported from vault study notes; curated for open course -->
# M04.A03 — De volatilidade implícita a volatilidade local

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M04
> **Aula:** M04.A03

↑ M04 · Resumo · Completo

**Módulo:** M04
**Pergunta do módulo:** Como ler, sanitizar e modelar a superfície de volatilidade?

## Conceito-núcleo
Local vol σ_loc(S,t) via Dupire: extrair dinâmica spot-dependente da surface de vanilas.

## Aplicação em mercado / trading
Usar local vol para path-dependent quando se quer casar vanilas; saber limites (dinâmica do smile).

## Entregável / lab
Esboço Dupire: de C(K,T) para σ_loc e simular 1 path-dependent sob local vol.

## Fonte (mapeamento)
quantitative-trading-free-lesson/14 from-implied-to-local-volatility

## Guia de estudo aprofundado

> **info**
>

### Conceitos-Chave

#### Superfície de Volatilidade Implícita vs. Volatilidade Local
No modelo tradicional de Black-Scholes, assume-se que a volatilidade é um número constante. Contudo, o mercado precifica opções utilizando uma função bidimensional de strike e maturidade, conhecida como superfície de volatilidade implícita, $\sigma_{\mathrm{impl}}(K,T)$. Essa superfície fornece a volatilidade que equaliza o preço teórico de Black-Scholes ao preço de mercado para cada par $(K,T)$.

O modelo de volatilidade local surge como uma resposta direta a essa incoerência. Mantendo a estrutura de difusão por movimento browniano sob a medida neutra ao risco $Q$, substitui-se a volatilidade constante por uma função determinística que depende do nível do ativo subjacente $S$ e do tempo $t$: $\sigma_{\mathrm{loc}}(S,t)$. A dinâmica do ativo sob esse modelo é descrita pela equação diferencial estocástica:

$$dS_t = (r-q)S_t\,dt + \sigma_{\mathrm{loc}}(S_t,t)S_t\,dW_t^Q, \quad S_0 > 0$$

onde $r$ representa a taxa livre de risco e $q$ o dividend yield contínuo (ambos mantidos constantes). O papel de $\sigma_{\mathrm{loc}}$ é absorver e carregar o "smile" (sorriso) de volatilidade observado no mercado.

#### Postulado Central da Volatilidade Local
O postulado fundamental do modelo estabelece que, para todo strike $K$ e maturidade $T$, o preço de uma opção de compra (Call) europeia gerado pelo modelo de volatilidade local deve coincidir exatamente com o preço de mercado:

$$C_{\mathrm{mkt}}(K,T) = C_{\mathrm{loc}}(K,T) \quad \text{para todo } (K,T)$$

Esse postulado possui duas implicações críticas:
1. **Calibração Perfeita de Vanillas:** O modelo é capaz de reproduzir perfeitamente todas as marginais do preço do ativo $S_T$ para diferentes maturidades $T$.
2. **Limitação para Opções Exóticas:** A correspondência com os preços de mercado não garante a precificação correta de opções exóticas dependentes do caminho (path-dependent). Enquanto as opções vanillas dependem apenas da distribuição marginal no vencimento $S_T$, as opções exóticas dependem da dinâmica conjunta do caminho de $S_t$. A volatilidade local é calibrada para ajustar marginais, sem inferir com precisão a verdadeira dinâmica estocástica oculta do ativo.

#### Densidade Neutra ao Risco e Convexidade
A segunda derivada do preço da Call em relação ao strike representa a densidade neutra ao risco $f_T(K)$ do ativo subjacente no instante $T$:

$$f_T(K) = \frac{\partial^2 C}{\partial K^2}$$

Para garantir a ausência de arbitragem, a densidade deve ser estritamente não negativa ($f_T(K) \ge 0$), o que exige que a curva do preço do Call em função do strike seja estritamente convexa ($\frac{\partial^2 C}{\partial K^2} > 0$).

#### Equação Forward e Fórmula de Dupire
A ligação matemática entre os preços das opções vanillas $C(K,T)$ e a volatilidade local $\sigma_{\mathrm{loc}}(K,T)$ no espaço $(K,T)$ é dada pela Equação Forward de Dupire:

$$\frac{\partial C}{\partial T} = \frac{1}{2}\sigma_{\mathrm{loc}}(K,T)^2 K^2 \frac{\partial^2 C}{\partial K^2} - (r-q)K\frac{\partial C}{\partial K} - qC$$

com a condição inicial dada pelo payoff na maturidade zero: $C(K,0) = (S_0-K)^+$.

Isolando o termo da volatilidade local ao quadrado, obtém-se a **Fórmula de Dupire**:

$$\sigma_{\mathrm{loc}}(K,T)^2 = \frac{\frac{\partial C}{\partial T} + (r-q)K\frac{\partial C}{\partial K} + qC}{\frac{1}{2}K^2\frac{\partial^2 C}{\partial K^2}}$$

Nesta formulação forward, $\sigma_{\mathrm{loc}}(K,T)$ deve ser interpretada como a volatilidade local $\sigma_{\mathrm{loc}}(S,t)$ avaliada no ponto em que $S=K$ e $t=T$.

#### Estabilização via Moneyness e Variância Total
Para melhorar a estabilidade numérica da superfície, em vez de trabalhar diretamente no espaço $(K,T)$, é comum transformar as variáveis para log-moneyness $k$ e variância total $w(k,T)$:

$$k = \ln\left(\frac{K}{F(T)}\right)$$

$$w(k,T) = \sigma_{\mathrm{impl}}(k,T)^2 T$$

onde $F(T)$ é o preço forward do ativo. A função $w(k,T)$ tende a apresentar maior regularidade em relação a $T$, auxiliando na mitigação de anomalias de calendário, embora a extração final de Dupire passe obrigatoriamente pelas derivadas dos preços $C$.

---

### Intuição de Mercado e Trading

No ambiente de trading e estruturação de derivativos, a volatilidade local atua como uma ferramenta de calibração que reflete a volatilidade instantânea esperada para um determinado nível de preço e tempo.

1. **Ajuste Marginal vs. Dinâmica do Smile:** O modelo ajusta perfeitamente os preços de vanillas negociadas em bolsa porque "força" a distribuição marginal $S_T$ a bater com o mercado. Contudo, ele assume que a volatilidade é puramente determinística em função do spot ($S$). Na prática, quando o spot se move, o smile de volatilidade real do mercado pode se mover de forma diferente do previsto pelo modelo de volatilidade local (o chamado *smile dynamics*).
2. **Sensibilidade do Numerador e Denominador:** 
   - O numerador da Fórmula de Dupire combina o decaimento temporal do preço ($\frac{\partial C}{\partial T}$) e os efeitos de *drift* de financiamento/dividendos.
   - O denominador reflete a probabilidade neutra ao risco de o ativo terminar próximo àquele strike ($\frac{\partial^2 C}{\partial K^2}$). Se a probabilidade for muito baixa ou a curva de preços perder a convexidade devido a ruídos, o denominador aproxima-se de zero ou torna-se negativo, provocando picos irreais ou valores matematicamente indefinidos na volatilidade local.

---

### Exemplo Numérico Resolvido

Considere os seguintes parâmetros de um ativo e de uma opção europeia de compra em um determinado ponto da grade $(K,T)$:

- Spot e Strike: $S_0 = 100,0$, $K = 100,0$
- Maturidade: $T = 1,0$ ano
- Taxa livre de risco contínua: $r = 0,02$ ($2\%$ ao ano)
- Dividend yield contínuo: $q = 0,00$ ($0\%$)
- Preço de mercado da Call observado no ponto: $C(100, 1,0) = 10,00$
- Derivada parcial do preço em relação à maturidade: $\frac{\partial C}{\partial T} = 1,50$
- Derivada parcial de $1^a$ ordem em relação ao strike: $\frac{\partial C}{\partial K} = -0,45$
- Derivada parcial de $2^a$ ordem em relação ao strike (densidade): $\frac{\partial^2 C}{\partial K^2} = 0,015$

**Objetivo:** Calcular o valor da volatilidade local $\sigma_{\mathrm{loc}}(100, 1,0)$ utilizando a Fórmula de Dupire.

#### Passo 1 Cálculo do Numerador
O numerador $N$ da Fórmula de Dupire é dado por:
$$N = \frac{\partial C}{\partial T} + (r-q)K\frac{\partial C}{\partial K} + qC$$

Substituindo os valores fornecidos:
$$N = 1,50 + (0,02 - 0,00) \times 100,0 \times (-0,45) + 0,00 \times 10,00$$
$$N = 1,50 + (0,02 \times 100,0 \times -0,45) + 0$$
$$N = 1,50 + (2,0 \times -0,45)$$
$$N = 1,50 - 0,90 = 0,60$$

#### Passo 2 Cálculo do Denominador
O denominador $D$ da Fórmula de Dupire é dado por:
$$D = \frac{1}{2} K^2 \frac{\partial^2 C}{\partial K^2}$$

Substituindo os valores fornecidos:
$$D = 0,5 \times (100,0)^2 \times 0,015$$
$$D = 0,5 \times 10000,0 \times 0,015$$
$$D = 5000,0 \times 0,015 = 75,0$$

#### Passo 3 Cálculo da Volatilidade Local ao Quadrado
$$\sigma_{\mathrm{loc}}(100, 1,0)^2 = \frac{N}{D} = \frac{0,60}{75,0} = 0,008$$

#### Passo 4 Extração da Volatilidade Local
$$\sigma_{\mathrm{loc}}(100, 1,0) = \sqrt{0,008} \approx 0,0894427$$

Convertendo para porcentagem:
$$\sigma_{\mathrm{loc}}(100, 1,0) \approx 8,94\%$$

---

### Armadilhas Comuns

1. **Amplificação de Ruído por Diferenciação Numérica:** A extração da volatilidade local exige calcular primeiras e segundas derivadas parciais dos preços em relação a $K$ e $T$. Cotações de mercado discretas e ruidosas causam instabilidades numéricas extremas se aplicadas diretamente via diferenças finitas sem um alisamento adequado da superfície implícita.
2. **Violações de Convexidade e Arbitragem de Borboleta (Fly Spread):** Se a superfície implícita interpolada gerar preços onde $\frac{\partial^2 C}{\partial K^2} \le 0$, haverá arbitragem de densidade negativa. Na Fórmula de Dupire, isso torna o denominador nulo ou negativo, resultando em volatilidades locais que explodem para o infinito ou tornam-se números complexos/imaginários ($\sigma_{\mathrm{loc}}^2 < 0$).
3. **Erros de Arbitragem de Calendário:** Se os preços das Calls não forem estritamente crescentes em relação ao tempo de maturidade ($\frac{\partial C}{\partial T} < 0$), o numerador da Fórmula de Dupire pode tornar-se negativo, inviabilizando o cálculo do modelo.
4. **Falsa Confiança em Opções Exóticas:** Assumir que, por repricar com precisão $100\%$ todas as opções vanillas do mercado, a volatilidade local precificará corretamente opções exóticas como barreiras ou asiáticas. O modelo acerta as marginais unidimensionais, mas ignora a verdadeira dinâmica estocástica do risco de volatilidade ao longo do tempo.

---

### Lab Prático em Python

Abaixo descreve-se o pipeline em Python para construir a superfície de volatilidade local através da Fórmula de Dupire e validar a repreciação de uma Call via Simulação de Monte Carlo.

#### Passo 1 Funções Utilitárias e Precificação Black-Scholes
Implementam-se as funções da distribuição normal (`n_cdf` e `n_pdf`) e o modelo Black-Scholes para opção de compra (`bs_call`), capaz de lidar com prazos nulos e limites determinísticos de volatilidade.

```python
import numpy as np
from math import log, sqrt, exp, erf

def n_cdf(x):
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))

def n_pdf(x):
    return (1.0 / sqrt(2.0 * np.pi)) * np.exp(-0.5 * x * x)

def bs_call(S0, K, r, q, T, sigma):
    if T <= 0:
        return max(S0 - K, 0.0)
    if sigma <= 0:
        F = S0 * exp((r - q) * T)
        return exp(-r * T) * max(F - K, 0.0)
    F = S0 * exp((r - q) * T)
    vol_sqrtT = sigma * sqrt(T)
    d1 = (log(F / K) + 0.5 * sigma * sigma * T) / vol_sqrtT
    d2 = d1 - vol_sqrtT
    return exp(-r * T) * (F * n_cdf(d1) - K * n_cdf(d2))
```

#### Passo 2 Geração da Superfície Sintética de Volatilidade Implícita
Cria-se uma função simulada de volatilidade implícita contendo estrutura a termo, *skew* e curvatura em função do log-moneyness $k = \ln(K/S_0)$.

```python
def sigma_impl_mock(S0, K, T):
    k = log(K / S0)
    base = 0.20 + 0.02 * (T / 5.0)
    skew = -0.15 * k
    curv = 0.25 * (k * k)
    return max(0.01, base + skew + curv)

S0 = 100.0
r, q = 0.02, 0.00
T_grid = np.array([0.25, 0.5, 1.0, 2.0, 3.0, 5.0])
K_grid = np.arange(60.0, 140.0 + 1e-9, 2.0)
nT, nK = len(T_grid), len(K_grid)

C = np.zeros((nT, nK))
for j, T in enumerate(T_grid):
    for i, K in enumerate(K_grid):
        sig = sigma_impl_mock(S0, K, T)
        C[j, i] = bs_call(S0, K, r, q, T, sig)
```

#### Passo 3 Diferenciação Numérica por Diferenças Finitas
Calculam-se as derivadas parciais do preço $C$ em relação a $T$ ($C\_T$) e em relação a $K$ (primeira derivada $C\_K$ e segunda derivada $C\_KK$).

```python
## Diferenças finitas em T
C_T = np.zeros_like(C)
for i in range(nK):
    C_T[0, i] = (C[1, i] - C[0, i]) / (T_grid - T_grid)
    C_T[-1, i] = (C[-1, i] - C[-2, i]) / (T_grid[-1] - T_grid[-2])
    for j in range(1, nT - 1):
        dt = T_grid[j + 1] - T_grid[j - 1]
        C_T[j, i] = (C[j + 1, i] - C[j - 1, i]) / dt

## Diferenças finitas em K
C_K = np.zeros_like(C)
C_KK = np.zeros_like(C)
dK = K_grid - K_grid
for j in range(nT):
    C_K[j, 0] = (C[j, 1] - C[j, 0]) / dK
    C_K[j, -1] = (C[j, -1] - C[j, -2]) / dK
    C_KK[j, 0] = (C[j, 2] - 2 * C[j, 1] + C[j, 0]) / (dK ** 2)
    C_KK[j, -1] = (C[j, -1] - 2 * C[j, -2] + C[j, -3]) / (dK ** 2)
    for i in range(1, nK - 1):
        C_K[j, i] = (C[j, i + 1] - C[j, i - 1]) / (2 * dK)
        C_KK[j, i] = (C[j, i + 1] - 2 * C[j, i] + C[j, i - 1]) / (dK ** 2)
```

#### Passo 4 Aplicação da Fórmula de Dupire e Salvaguardas Numéricas
Aplica-se a fórmula de Dupire na grade discretizada. Utiliza-se um parâmetro $\epsilon = 10^{-12}$ para proteger o denominador contra divisões por zero ou valores negativos decorrentes de ruídos.

```python
sigma_loc2 = np.zeros_like(C)
eps = 1e-12
for j, T in enumerate(T_grid):
    for i, K in enumerate(K_grid):
        denom = 0.5 * K * K * max(C_KK[j, i], eps)
        num = C_T[j, i] + (r - q) * K * C_K[j, i] + q * C[j, i]
        sigma_loc2[j, i] = num / denom

sigma_loc2 = np.maximum(sigma_loc2, 0.0)
sigma_loc = np.sqrt(sigma_loc2)
print("min sigma_loc =", sigma_loc.min(), "max sigma_loc =", sigma_loc.max())
```

#### Passo 5 Interpolação Bilinear da Volatilidade Local
Para permitir a simulação contínua do preço em Monte Carlo, cria-se uma função de interpolação bilinear que tranca (*clamp*) os valores nas fronteiras da grade.

```python
def sigma_loc_ST(S, t):
    t, S = float(t), float(S)
    if t <= T_grid:
        j0, j1 = 0, 1
    elif t >= T_grid[-1]:
        j0, j1 = nT - 2, nT - 1
    else:
        j1 = np.searchsorted(T_grid, t)
        j0 = j1 - 1

    if S <= K_grid:
        i0, i1 = 0, 1
    elif S >= K_grid[-1]:
        i0, i1 = nK - 2, nK - 1
    else:
        i1 = np.searchsorted(K_grid, S)
        i0 = i1 - 1

    t0, t1 = T_grid[j0], T_grid[j1]
    k0, k1 = K_grid[i0], K_grid[i1]

    wt = 0.0 if t1 == t0 else (t - t0) / (t1 - t0)
    wk = 0.0 if k1 == k0 else (S - k0) / (k1 - k0)

    s00, s01 = sigma_loc[j0, i0], sigma_loc[j0, i1]
    s10, s11 = sigma_loc[j1, i0], sigma_loc[j1, i1]
    return (1 - wt) * ((1 - wk) * s00 + wk * s01) + wt * ((1 - wk) * s10 + wk * s11)
```

#### Passo 6 Precificação via Monte Carlo Discretizado por Log-Euler
Simula-se a trajetória de preços sob a volatilidade local utilizando a forma log-Euler:

$$S_{t+\Delta t} = S_t \exp\left(\left(r - q - \frac{1}{2}\sigma_{\mathrm{loc}}(S_t,t)^2\right)\Delta t + \sigma_{\mathrm{loc}}(S_t,t)\sqrt{\Delta t}\,Z\right), \quad Z \sim \mathcal{N}(0,1)$$

```python
def mc_localvol_european_call(K, T, n_paths=20000, n_steps=200):
    dt = T / n_steps
    disc = exp(-r * T)
    S = np.full(n_paths, S0, dtype=float)
    for step in range(n_steps):
        t = step * dt
        sig = np.array([sigma_loc_ST(s, t) for s in S])
        Z = np.random.randn(n_paths)
        S *= np.exp((r - q - 0.5 * sig * sig) * dt + sig * np.sqrt(dt) * Z)
    payoff = np.maximum(S - K, 0.0)
    return disc * payoff.mean()

K_test, T_test = 100.0, 1.0
pv_mc = mc_localvol_european_call(K_test, T_test, n_paths=20000, n_steps=200)
pv_bs = bs_call(S0, K_test, r, q, T_test, sigma_impl_mock(S0, K_test, T_test))
print("PV MC localvol =", pv_mc, "PV BS de impl =", pv_bs, "diff =", pv_mc - pv_bs)
```

---

### Glossário

- **Volatilidade Implícita ($\sigma_{\mathrm{impl}}$):** O valor do parâmetro de volatilidade que, quando inserido na fórmula clássica de Black-Scholes, iguala o preço teórico da opção ao seu preço observado no mercado.
- **Volatilidade Local ($\sigma_{\mathrm{loc}}(S,t)$):** Uma função determinística do nível do ativo $S$ e do tempo $t$ que define a volatilidade instantânea do modelo de difusão de modo a replicar exatamente a superfície de preços de opções vanillas.
- **Fórmula de Dupire:** Equação matemática que extrai de forma exata a volatilidade local $\sigma_{\mathrm{loc}}(K,T)$ a partir das derivadas parciais de primeira ordem em tempo e primeira/segunda ordens em strike dos preços de opções vanillas.
- **Densidade Neutra ao Risco ($f_T(K)$):** A função de densidade de probabilidade do preço do ativo subjacente no instante $T$ sob a medida neutra ao risco $Q$, dada pela segunda derivada do preço da Call em relação ao strike.
- **Log-Moneyness ($k$):** Medida estandardizada de distância do strike em relação ao preço forward, expressa por $k = \ln(K/F(T))$.
- **Variância Total ($w(k,T)$):** O produto da volatilidade implícita ao quadrado pelo tempo até a maturidade, $w(k,T) = \sigma_{\mathrm{impl}}(k,T)^2 T$.
- **Discretização Log-Euler:** Esquema de simulação estocástica em tempo discreto aplicado ao logaritmo do preço do ativo para garantir a não negatividade dos preços e manter a estabilidade numérica.

---

### Questões e Exercícios de Prática

#### Nível Básico (Resposta Curta)

**Questão 1:** Qual a principal diferença entre a premissa de volatilidade do modelo de Black-Scholes e a do modelo de Volatilidade Local?  
*Resposta:* O modelo de Black-Scholes assume que a volatilidade é uma constante escalar ao longo de todo o tempo e níveis de preço. O modelo de Volatilidade Local assume que a volatilidade é uma função determinística que varia dinamicamente de acordo com o nível atual do ativo e do tempo, $\sigma_{\mathrm{loc}}(S,t)$.

**Questão 2:** Qual a relação matemática entre a densidade de probabilidade neutra ao risco do ativo no vencimento e o preço das opções vanillas?  
*Resposta:* A densidade de probabilidade neutra ao risco $f_T(K)$ é exatamente igual à segunda derivada parcial do preço da opção Call europeia em relação ao strike: $f_T(K) = \frac{\partial^2 C}{\partial K^2}$.

---

#### Nível Intermediário (Cálculo e Análise Técnica)

**Questão 3:** Uma opção com strike $K = 50$, taxa livre de risco $r = 0,01$, dividend yield $q = 0,01$ e preço $C = 4,00$ apresenta as seguintes derivadas parciais:
- $\frac{\partial C}{\partial T} = 0,80$
- $\frac{\partial C}{\partial K} = -0,30$
- $\frac{\partial^2 C}{\partial K^2} = 0,02$

Calcule o valor exato da volatilidade local $\sigma_{\mathrm{loc}}(50, T)$.

*Resposta:*
1. Numerador:
   $$N = \frac{\partial C}{\partial T} + (r-q)K\frac{\partial C}{\partial K} + qC$$
   $$N = 0,80 + (0,01 - 0,01) \times 50 \times (-0,30) + 0,01 \times 4,00$$
   $$N = 0,80 + 0 + 0,04 = 0,84$$

2. Denominador:
   $$D = \frac{1}{2} K^2 \frac{\partial^2 C}{\partial K^2}$$
   $$D = 0,5 \times 50^2 \times 0,02 = 0,5 \times 2500 \times 0,02 = 25,0$$

3. Volatilidade Local ao quadrado:
   $$\sigma_{\mathrm{loc}}^2 = \frac{0,84}{25,0} = 0,0336$$

4. Volatilidade Local:
   $$\sigma_{\mathrm{loc}} = \sqrt{0,0336} \approx 0,1833 \text{ ou } 18,33\%$$

**Questão 4:** Por que a diferenciação numérica aplicada a uma grade de cotações discretas de mercado pode inviabilizar a calibração do modelo de Dupire se não houver um tratamento prévio dos dados?  
*Resposta:* A diferenciação numérica amplifica significativamente o ruído presente nos dados discretos do mercado. Erros pequenos nas cotações podem levar a estimativas instáveis de $\frac{\partial^2 C}{\partial K^2}$. Se essa segunda derivada se tornar nula ou negativa (violação da convexidade), a Fórmula de Dupire resulta em divisões por zero ou em volatilidades quadráticas negativas ($\sigma_{\mathrm{loc}}^2 < 0$), tornando o cálculo inviável sem suavização e remoção prévia de arbitragem da superfície.

---

#### Nível Avançado (Questões Discursivas)

**Questão 5:** Avalie criticamente a seguinte afirmação: "Como o modelo de volatilidade local de Dupire reprica com precisão de $100\%$ todas as opções vanillas europeias negociadas no mercado, ele é o modelo perfeito e isento de riscos para precificar e fazer hedge de opções exóticas dependentes do caminho, como opções barreira."  
*Resposta:* A afirmação é **falsa**. O postulado de Dupire garante que a volatilidade local ajusta com precisão perfeita as distribuições marginais unidimensionais do ativo $S_T$ para diferentes maturidades $T$, o que garante a repreciação exata de opções vanillas. Contudo, opções exóticas dependentes do caminho (como opções barreira ou asiáticas) dependem da distribuição conjunta dos preços ao longo do tempo (a dinâmica estocástica contínua do caminho do ativo). O modelo de volatilidade local assume uma volatilidade puramente determinística em relação a $S$ e $t$, forçando a volatilidade a ceder quando o spot se move de uma maneira irrealista em relação à dinâmica real observada no mercado (o comportamento do *smile* sob dinâmicas de spot). Portanto, o modelo não "adivinha" a verdadeira dinâmica estocástica oculta, podendo gerar preços e parâmetros de hedge (como o Delta e o Vega) distorcidos para produtos exóticos.

**Questão 6:** Explique a utilidade teórica e prática da transformação da superfície de volatilidade para o espaço de log-moneyness $k$ e variância total $w(k,T)$ no processo de calibração do modelo de volatilidade local.  
*Resposta:* Trabalhar diretamente na superfície de preços no espaço $(K,T)$ é altamente susceptível a instabilidades devido ao decaimento do valor das opções e variações de escala entre strikes distantes do dinheiro. A transformação para o log-moneyness $k = \ln(K/F(T))$ remove o efeito de *drift* do ativo ao normalizar o strike pelo preço forward. A conversão da volatilidade implícita para a variância total $w(k,T) = \sigma_{\mathrm{impl}}(k,T)^2 T$ gera uma função mais suave e monotonicamente crescente em relação ao tempo $T$. Essa representação suavizada facilita a interpolação e parametrização da superfície, garantindo a ausência de arbitragens de calendário e de borboleta de forma mais simples e estável antes do cálculo final das derivadas de preços exigidas por Dupire.