<!-- imported study note (guia-completo.md) -->
# Guia Completo do Módulo M04: Superfície de Volatilidade e Modelos de Smile

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M04

↑ M04 · Resumo · Completo

## Sumário Executivo

Este documento apresenta uma análise detalhada e exaustiva sobre a construção, calibração e parametrização de superfícies de volatilidade sem arbitragem estática, tomando como base os avanços teóricos e práticos das formulações SVI (*Stochastic Volatility Inspired*) e SSVI (*Surface SVI*), desenvolvidas por Jim Gatheral e Antoine Jacquier, além das comparações com modelos estocásticos (Heston, SABR, SVI-SABR) e modelos de salto (Merton).

A modelagem adequada da superfície de volatilidade é um pilar crítico para a precificação de derivativos complexos e para a gestão de risco em instituições financeiras. O principal desafio enfrentado pelos praticantes é garantir que uma superfície ajustada aos preços discretos observados no mercado não admita oportunidades de arbitragem estática — especificamente a arbitragem de spread de calendário e a arbitragem de borboleta (*butterfly arbitrage*).

Através da parametrização SSVI e de algoritmos sistemáticos de otimização e sanitização de dados, demonstra-se como obter representações em forma fechada que garantem ausência de arbitragem estática em toda a superfície, mantendo perfeita aderência aos dados empíricos do mercado de opções (como observado no índice SPX e no mercado de câmbio).

---

## 1 Superfície de Volatilidade: Expiry, Tenor, Moneyness e Convenções

A superfície de volatilidade representa graficamente e matematicamente a estrutura a termo e o perfil de *moneyness* da volatilidade implícita obtida através do modelo de Black-Scholes.

### 1.1 Variáveis Fundamentais e Mapeamento

Para um dado processo de preço do ativo objeto $(S_t)_{t \ge 0}$ com filtração natural $(\mathcal{F}_t)_{t \ge 0}$, define-se o preço *forward* $F_t := \mathbb{E}[S_t | \mathcal{F}_0]$.

*   **Log-Strike / Log-Moneyness ($k$):** O moneyness é medido pelo logaritmo do strike em relação ao preço forward:
    $$k := \log\left(\frac{K}{F_t}\right)$$
    onde $K$ é o preço de exercício da opção.
*   **Tempo até a Expiração ($t$):** A maturidade da opção expressa em anos ou fração de ano.
*   **Volatilidade Implícita de Black-Scholes ($\sigma_{BS}(k, t)$):** A volatilidade constante que, inserida na fórmula clássica de Black-Scholes, iguala o preço teórico ao preço de mercado da opção.
*   **Variância Total Implícita ($w(k, t)$):** Produto da variância implícita pelo tempo até a expiração:
    $$w(k, t) := \sigma_{BS}^2(k, t) \cdot t$$
*   **Variância Implícita ($v(k, t)$):** Taxa de variância por unidade de tempo:
    $$v(k, t) := \sigma_{BS}^2(k, t) = \frac{w(k, t)}{t}$$

A superfície de volatilidade é a função bidimensional $(k, t) \mapsto w(k, t)$. Para uma maturidade fixa $t > 0$, a função unidimensional $k \mapsto w(k, t)$ é denominada **fatia** (*slice*).

### 1.2 Fórmula de Black-Scholes e Comportamento Assintótico

O preço de uma opção de compra (*European Call*) $C_{BS}(k, w(k,t))$ sobre $S$ com strike $F_t e^k$, expiração $t$ e variância total $w(k,t)$ é expresso por:
$$C_{BS}(k, w(k,t)) = S \left( N(d_+(k)) - e^k N(d_-(k)) \right)$$
com
$$d_\pm(k) := \frac{-k}{\sqrt{w(k,t)}} \pm \frac{\sqrt{w(k,t)}}{2}$$

De acordo com a **Fórmula de Momentos de Roger Lee**, para fatias extremas de moneyness ($|k| \to \infty$), a variância total implícita $w(k,t)$ apresenta comportamento linear em relação a $k$. A inclinação assintótica das asas é limitada superiormente por 2:
$$\limsup_{|k| \to \infty} \frac{w(k,t)}{|k|} \le 2$$

---

## 2 Arbitragem Estática: Calendário, Borboleta e Densidade Risco-Neutra de Breeden-Litzenberger

A ausência de arbitragem estática (Cox & Hobson, 2005) equivale à existência de uma medida de probabilidade risco-neutra martingale não negativa sob a qual o preço das opções europeias é dado pela expectativa descontada do seu *payoff*.

```
                      +------------------------------------------+
                      |       Superfície sem Arbitragem         |
                      |                 Estática                 |
                      +------------------------------------------+
                                           |
                   +-----------------------+-----------------------+
                   |                                               |
                   v                                               v
+------------------------------------+           +------------------------------------+
|  Arbitragem de Calendário          |           |  Arbitragem de Borboleta           |
|  d/dt [w(k, t)] >= 0               |           |  g(k) >= 0 e lim d+(k) = -infty    |
|  Opções mais longas valem mais     |           |  Densidade p(k) >= 0               |
+------------------------------------+           +------------------------------------+
```

### 2.1 Arbitragem de Spread de Calendário

A arbitragem de spread de calendário ocorre se o preço de uma opção com maturidade mais longa for menor do que o preço de uma opção idêntica de maturidade mais curta.

*   **Condição Necessária e Suficiente:** Assumindo dividendos proporcionais ao preço do ativo, a superfície de volatilidade $w$ é livre de arbitragem de calendário se e somente se a variância total for monótonamente não decrescente em relação ao tempo de expiração para qualquer moneyness $k$:
    $$\frac{\partial w(k, t)}{\partial t} \ge 0, \quad \forall k \in \mathbb{R}, \; t > 0$$

Em um gráfico de variância total $w(k,t)$ contra o moneyness $k$, a ausência de arbitragem de calendário implica que as curvas de fatias temporais distintas jamais se cruzam (*no crossed lines*).

### 2.2 Arbitragem de Borboleta e Relação de Breeden-Litzenberger

A ausência de arbitragem de borboleta (*butterfly arbitrage*) garante a convexidade dos preços das opções em relação ao strike e a existência de uma densidade de probabilidade risco-neutra não negativa $p(k) \ge 0$.

A densidade de probabilidade risco-neutra $p(k)$ é obtida pela segunda derivada do preço da opção Call em relação ao strike (Breeden & Litzenberger):
$$p(k) = \frac{\partial^2 C_{BS}}{\partial K^2} \Bigg|_{K = F_t e^k} = \frac{g(k)}{\sqrt{2\pi w(k)}} \exp\left( -\frac{d_-(k)^2}{2} \right)$$

onde a função $g(k)$ é definida formalmente como:
$$g(k) := \left( 1 - \frac{k w'(k)}{2 w(k)} \right)^2 - \frac{w'(k)^2}{4} \left( \frac{1}{w(k)} + \frac{1}{4} \right) + \frac{w''(k)}{2}$$

*   **Teorema da Ausência de Arbitragem de Borboleta:** Uma fatia de volatilidade é livre de arbitragem de borboleta se e somente se:
    1.  $g(k) \ge 0$ para todo $k \in \mathbb{R}$;
    2.  $\lim_{k \to +\infty} d_+(k) = -\infty$ (garantindo que a densidade integre exatamente 1).

---

## 3 Sanitização de Dados e Parametrizações SVI e SSVI

A calibração direta de dados brutos de mercado exige parametrizações flexíveis e analiticamente tratáveis.

### 3.1 Parametrização Raw SVI

Proposta por Jim Gatheral em 2004, a parametrização *Raw SVI* para a variância total implícita em uma fatia $t$ é dada por:
$$w(k; \chi_R) = a + b \left\{ \rho (k - m) + \sqrt{(k - m)^2 + \sigma^2} \right\}$$
onde $\chi_R = \{a, b, \rho, m, \sigma\}$ com $a \in \mathbb{R}$, $b \ge 0$, $|\rho| < 1$, $m \in \mathbb{R}$, $\sigma > 0$, e a condição $a + b \sigma \sqrt{1 - \rho^2} \ge 0$ (assegurando variância não negativa no mínimo).

| Parâmetro | Significado Geométrico no Smile |
| :--- | :--- |
| $a$ | Nível geral de variância (transladação vertical). |
| $b$ | Inclinação das asas de Put e Call (aperto/convexidade do smile). |
| $\rho$ | Rotação do smile (rotação anti-horária; reduz inclinação da asa esquerda e aumenta a da direita). |
| $m$ | Transladação horizontal da curva para a direita. |
| $\sigma$ | Curvatura na região *At-The-Money* (ATM) (reduz a curvatura pontual no ATM). |

### 3.2 Parametrização Natural SVI

A formulação *Natural SVI* reparametriza o espaço por $\chi_N = \{\Delta, \mu, \rho, \omega, \zeta\}$:
$$w(k; \chi_N) = \Delta + \frac{\omega}{2} \left\{ 1 + \zeta \rho (k - \mu) + \sqrt{(\zeta(k - \mu) + \rho)^2 + (1 - \rho^2)} \right\}$$

As conversões exatas entre Raw SVI e Natural SVI são dadas por:
$$(a, b, \rho, m, \sigma) = \left( \Delta + \frac{\omega}{2}(1 - \rho^2), \; \frac{\omega \zeta}{2}, \; \rho, \; \mu - \frac{\rho}{\zeta}, \; \frac{\sqrt{1 - \rho^2}}{\zeta} \right)$$
$$(\Delta, \mu, \rho, \omega, \zeta) = \left( a - \frac{\omega}{2}(1 - \rho^2), \; m + \frac{\rho \sigma}{\sqrt{1 - \rho^2}}, \; \rho, \; 2 b \sigma \sqrt{1 - \rho^2}, \; \frac{\sqrt{1 - \rho^2}}{\sigma} \right)$$

### 3.3 Parametrização SVI Jump-Wings (SVI-JW)

A parametrização *SVI-JW* reinterpreta os parâmetros em métricas intuitivas para operadoras de mesa (*traders*), focando na volatilidade implícita $v(k,t) = w(k,t)/t$:

$$\begin{aligned}
v_t &= \frac{1}{t} \left( a + b \left\{ -\rho m + \sqrt{m^2 + \sigma^2} \right\} \right) \quad \text{(Variância ATM)} \\
\psi_t &= \frac{1}{\sqrt{w_t}} \frac{b}{2} \left( -\frac{m}{\sqrt{m^2 + \sigma^2}} + \rho \right) = \frac{\partial \sigma_{BS}(k, t)}{\partial k} \Bigg|_{k=0} \quad \text{(Skew ATM)} \\
p_t &= \frac{1}{\sqrt{w_t}} b (1 - \rho) \quad \text{(Inclinação da Asa da Put / Asa Esquerda)} \\
c_t &= \frac{1}{\sqrt{w_t}} b (1 + \rho) \quad \text{(Inclinação da Asa da Call / Asa Direita)} \\
\tilde{v}_t &= \frac{1}{t} \left( a + b \sigma \sqrt{1 - \rho^2} \right) \quad \text{(Variância Mínima Implícita)}
\end{aligned}$$

### 3.4 Surface SVI (SSVI)

A extensão *Surface SVI* expressa a superfície inteira em termos do tempo de variância ATM $\theta_t := \sigma_{BS}^2(0, t) \cdot t$:
$$w(k, \theta_t) = \frac{\theta_t}{2} \left\{ 1 + \rho \phi(\theta_t) k + \sqrt{(\phi(\theta_t) k + \rho)^2 + (1 - \rho^2)} \right\}$$

onde $\phi: (0, \infty) \to (0, \infty)$ é uma função suave.

*   **Condições do Corolário 4.1 para Ausência Total de Arbitragem Estática:**
    1.  $\partial_t \theta_t \ge 0$ para todo $t > 0$ (Monotonicidade do tempo de variância ATM).
    2.  $0 \le \frac{\partial}{\partial \theta}(\theta \phi(\theta)) \le \frac{1}{\rho^2} \left( 1 + \sqrt{1 - \rho^2} \right) \phi(\theta)$ para todo $\theta > 0$ (Ausência de Arbitragem de Calendário).
    3.  $\theta \phi(\theta) (1 + |\rho|) < 4$ para todo $\theta > 0$ (Ausência de Arbitragem de Borboleta e Limite de Lee).
    4.  $\theta \phi(\theta)^2 (1 + |\rho|) \le 4$ para todo $\theta > 0$.

#### Famílias Notáveis de $\phi(\theta)$ no SSVI:
1.  **Heston-Like:** Consistent com a dinâmica assintótica do modelo de Heston:
    $$\phi(\theta) = \frac{1}{\lambda \theta} \left( 1 - \frac{1 - e^{-\lambda \theta}}{\lambda \theta} \right), \quad \text{com } \lambda \ge \frac{1 + |\rho|}{4}$$
2.  **Power-Law Modificada:** Totalmente livre de arbitragem estática em todos os prazos:
    $$\phi(\theta) = \frac{\eta}{\theta^\gamma (1 + \theta)^{1-\gamma}}, \quad \text{com } \gamma \in \left(0, \frac{1}{2}\right] \text{ e } \eta(1 + |\rho|) \le 2$$

### 3.5 Exemplo Numérico Concreto: Correção do Smile de Axel Vogt

Considerem-se os parâmetros de Raw SVI do famoso contraexemplo de Axel Vogt ($t = 1$):
$$\chi_R = \{a = -0.0410, \; b = 0.1331, \; m = 0.3586, \; \rho = 0.3060, \; \sigma = 0.4153\}$$

Ao avaliar a função $g(k)$, obtêm-se valores negativos na região $k \in [-1.5, 0.5]$, resultando em densidade risco-neutra negativa (arbitragem de borboleta).

Convertendo os parâmetros brutos para SVI-JW:
$$(v_t, \psi_t, p_t, c_t, \tilde{v}_t) = (0.01742625, \; -0.1752111, \; 0.6997381, \; 1.316798, \; 0.0116249)$$

#### Aplicação do Algoritmo de Eliminação de Arbitragem:
Mantendo-se fixos os parâmetros bem ajustados no mercado de ações ($v_t, \psi_t, p_t$), substitui-se a asa de Call $c_t$ e a variância mínima $\tilde{v}_t$ pelas condições limites de SSVI:
$$c'_t = p_t + 2\psi_t = 0.6997381 + 2(-0.1752111) = 0.3493158$$
$$\tilde{v}'_t = v_t \frac{4 p_t c'_t}{(p_t + c'_t)^2} = 0.01742625 \frac{4(0.6997381)(0.3493158)}{(0.6997381 + 0.3493158)^2} = 0.01548182$$

Através de uma otimização numérica que minimiza a soma dos erros quadráticos dos preços de opções sujeita a penalização de borboleta, obtém-se o ajuste ótimo sem arbitragem:
$$(c^*_t, \tilde{v}^*_t) = (0.8564763, \; 0.0116249)$$

O otimizador preserva a variância mínima original e reduz a asa de Call para eliminar a densidade negativa.

---

## 4 Volatilidade Local de Dupire, Calibração e Limitações Dinâmicas

A modelo de Volatilidade Local proposto por Bruno Dupire constrói um processo difusivo contínuo capaz de reproduzir exatamente a superfície de preços de opções observada:
$$dS_t = (r_t - q_t) S_t dt + \sigma_{loc}(S_t, t) S_t dW_t$$

### 4.1 A Fórmula de Dupire em Termos de Variância Total

A volatilidade local $\sigma_{loc}(K, T)$ é calculada diretamente da superfície de variância total $w(k, t)$:
$$\sigma_{loc}^2(k, t) = \frac{\frac{\partial w(k,t)}{\partial t}}{1 - \frac{k}{w(k,t)} \frac{\partial w(k,t)}{\partial k} + \frac{1}{4} \left( -\frac{1}{4} - \frac{1}{w(k,t)} + \frac{k^2}{w(k,t)^2} \right) \left( \frac{\partial w(k,t)}{\partial k} \right)^2 + \frac{1}{2} \frac{\partial^2 w(k,t)}{\partial k^2}}$$

### 4.2 Relação Crítica com a Ausência de Arbitragem Estática

Observa-se que o denominador da Equação de Dupire é exatamente igual à função $g(k)$ escalada pela variância, enquanto o numerador é a derivada temporal da variância total $\partial_t w(k,t)$.

*   Se houver arbitragem de calendário ($\partial_t w < 0$), o numerador torna-se negativo.
*   Se houver arbitragem de borboleta ($g(k) < 0$), o denominador torna-se negativo.

Em ambos os casos, a variância local $\sigma_{loc}^2(k, t)$ assume valores negativos, resultando em volatilidades locais números imaginários, o que inviabiliza a simulação Monte Carlo e a precificação de derivativos exóticos. Portanto, a parametrização via SSVI é uma ferramenta direta para garantir a bem-postura da equação de Dupire.

### 4.3 Limitações Dinâmicas do Modelo de Volatilidade Local

Apesar de calibrar perfeitamente os preços estáticos, a volatilidade local apresenta limitações dinâmicas graves:
1.  **Dinâmica de Smile Inversa:** O modelo prevê que o smile de volatilidade se desloca na direção oposta ao preço do ativo (*sticky strike* antinatural), subestimando a volatilidade de opções quando o ativo sofre grandes variações.
2.  **Achatamento do Skew Futuro:** O skew de volatilidade implícita reportado pelo modelo para datas futuras reduz-se rapidamente com o aumento do horizonte, divergindo dos padrões observados no mercado.

---

## 5 Modelo de Heston: Parâmetros, Condição de Feller, Origem do Smile e Simulação

O modelo de volatilidade estocástica de Heston (1993) assume que a variância instantânea $v_t$ segue um processo de Cox-Ingersoll-Ross (CIR).

### 5.1 Formulação Matemática do Modelo

$$\begin{aligned}
dS_t &= \mu S_t dt + \sqrt{v_t} S_t dW_t^S \\
dv_t &= \kappa (\theta - v_t) dt + \xi \sqrt{v_t} dW_t^v \\
d\langle W^S, W^v \rangle_t &= \rho dt
\end{aligned}$$

| Parâmetro | Definição | Impacto na Superfície |
| :--- | :--- | :--- |
| $\kappa > 0$ | Velocidade de reversão à média da variância. | Regula a inclinação da estrutura a termo do smile. |
| $\theta > 0$ | Variância média de longo prazo. | Determina o nível assintótico da variância implícita. |
| $\xi > 0$ | Volatilidade da volatilidade (*vol-of-vol*). | Controla a curvatura/kurtosis (asa) do smile. |
| $\rho \in [-1, 1]$ | Correlação entre os ruídos de preço e volatilidade. | Gera a assimetria (*skew*) do smile. |
| $v_0 > 0$ | Variância instantânea inicial. | Define o nível de volatilidade de curto prazo. |

### 5.2 Condição de Feller

Para garantir que o processo de variância $v_t$ permaneça estritamente positivo ($v_t > 0$) e não atinja a origem $0$, deve-se respeitar a **Condição de Feller**:
$$2 \kappa \theta > \xi^2$$

Quando a condição de Feller é violada ($2 \kappa \theta \le \xi^2$), a variância pode tocar a origem, exigindo esquemas numéricos avançados de simulação para evitar valores negativos ou instabilidade (como esquemas de absorção/reflexão ou o esquema *Quadratic-Exponential* - QE de Andersen).

### 5.3 Origem do Smile e Convergência Heston-SVI

Gatheral e Jacquier (2011) provaram matematicamente que, no limite de grande maturidade ($t \to \infty$), o smile de volatilidade implícita do modelo de Heston converge **exatamente** para a parametrização SVI.

No limite de curto prazo ($t \to 0$), a inclinação da volatilidade ATM para um processo de variância geral $dv_t = \alpha(v_t)dt + \eta \sqrt{v_t} \beta(v_t) dW_t$ é proporcional a $\beta(v)$. Para o modelo de Heston, como $\beta(v) = \sqrt{v}$, a volatilidade implícita apresenta skew ATM constante e bem-definido à medida que $t \to 0$.

---

## 6 Modelos de Saltos: Merton, Kou e Smile de Curto Prazo

Modelos de difusão pura (como Heston ou Black-Scholes) falham em capturar o elevado *skew* e a curvatura pronunciada de opções com maturidade muito curta ($t \to 0$), visto que os processos contínuos necessitam de tempo para acumular variância. Os modelos de saltos corrigem essa deficiência ao introduzir descontinuidades repentinas no preço.

```
Maturidade t -> 0
  |
  +---> Difusão Pura (Heston): phi_0 = lim theta*phi(theta) = 0 
  |     (Smile achata para curto prazo)
  |
  +---> Difusão com Saltos (Merton): phi_0 > 0 
        (Smile mantém formato em "V" pronunciado para curto prazo)
```

### 6.1 Modelo de Saltos de Merton (*Merton Jump Diffusion*)

No modelo de Merton (1976), o preço do ativo incorpora saltos Poissonianos com tamanhos distribuídos log-normalmente:
$$\frac{dS_t}{S_{t-}} = (r - q - \lambda k_J) dt + \sigma dW_t + (Y_t - 1) dN_t$$

onde $N_t$ é um processo de Poisson com intensidade $\lambda$, $Y_t$ é o tamanho do salto tal que $\log(Y_t) \sim \mathcal{N}(\mu_J, \sigma_J^2)$, e $k_J = \mathbb{E}[Y_t - 1] = e^{\mu_J + \frac{1}{2}\sigma_J^2} - 1$.

### 6.2 O Smile em "V" de Curto Prazo

Em modelos com saltos, a função de variância ATM no tempo zero atinge um limite positivo não nulo:
$$\varphi_0 := \lim_{\theta \to 0} \theta \phi(\theta) > 0$$

Em $t = 0$, a fatia de variância total assume o formato característico em "V":
$$w(k, \theta_0) = \frac{1}{2} \varphi_0 \left( \rho k + |k| \right)$$

Este formato em "V" permite capturar os preços de opções de curtíssimo prazo observados empiricamente no mercado, como evidenciado nos dados do SPX para $T = 0.0027$ anos (cerca de 1 dia de negociação).

---

## 7 Smile de FX: Convenções de Delta, ATM, Risk Reversal, Butterfly e Dinâmica de Smile

O mercado de câmbio (*Foreign Exchange* - FX) cotiza suas opções e superfícies de volatilidade segundo convenções operacionais distintas do mercado acionário.

### 7.1 Convenções de Cotação em Câmbio

As opções em FX são cotadas em termos de volatilidade implícita para deltas específicos de Call e Put (tipicamente $25\Delta$ e $10\Delta$), em vez de strikes absolutos em dinheiro.

*   **At-The-Money Delta Neutral (ATM DNS):** O strike $K_{ATM}$ é aquele onde o delta da Call iguala em magnitude o delta da Put (respeitando o prêmio pago).
*   **Risk Reversal ($RR_{25}$):** Mede o skew ou assimetria da cauda da superfície. Corresponde à diferença entre a volatilidade implícita da Call de $25\Delta$ e da Put de $25\Delta$:
    $$RR_{25} = \sigma(\text{Call}_{25\Delta}) - \sigma(\text{Put}_{25\Delta})$$
*   **Strangle / Butterfly ($BF_{25}$):** Mede a curvatura ou peso das caixas/caudas da distribuição (*kurtosis*):
    $$BF_{25} = \frac{\sigma(\text{Call}_{25\Delta}) + \sigma(\text{Put}_{25\Delta})}{2} - \sigma(\text{ATM})$$

 Nas convenções SVI-JW, estes conceitos mapeiam-se diretamente nas inclinações das asas esquerda e direita ($p_t$ e $c_t$):
$$p_t = \frac{1}{\sqrt{w_t}} b(1 - \rho), \quad c_t = \frac{1}{\sqrt{w_t}} b(1 + \rho)$$

### 7.2 Dinâmica de Smile: Sticky Strike vs Sticky Delta

1.  **Sticky Strike:** A volatilidade implícita para um dado strike fixo $K$ permanece constante quando o preço do ativo subjacente muda.
2.  **Sticky Delta:** A volatilidade implícita para um moneyness/delta fixo permanece constante quando o preço do ativo muda. O smile desloca-se horizontalmente junto com o preço do ativo.

### 7.3 Comparações: Modelo SABR vs SVI-SABR

O modelo SABR com $\beta = 1$ possui a fórmula clássica de volatilidade implícita aproximada:
$$\sigma_{BS}(k) = \alpha f\left(\frac{k}{\alpha}\right), \quad f(y) = \frac{-\nu y}{\log\left( \frac{\sqrt{\nu^2 y^2 + 2\rho \nu y + 1} - \nu y - \rho}{1 - \rho} \right)}$$

#### Problema da Arbitragem no SABR:
É amplamente conhecido que o modelo SABR tradicional sofre de arbitragem de borboleta severa nas caixas para strikes distantes do ATM, gerando densidades risco-neutras negativas ($p(k) < 0$).

#### A Solução SVI-SABR:
A formulação SVI-SABR corrige essa deficiência mantendo a forma simples do SVI:
$$\sigma_{BS}^2(k) = \frac{\alpha^2}{2} \left\{ 1 + \rho \frac{\nu}{\alpha} k + \sqrt{\left(\frac{\nu}{\alpha} k + \rho\right)^2 + (1 - \rho^2)} \right\}$$

A densidade do modelo SVI-SABR é garantidamente positiva para todas as strikes contanto que se respeitem as condições:
$$\alpha \nu t (1 + |\rho|) < 4 \quad \text{e} \quad \nu^2 t (1 + |\rho|) < 4$$

**Valores típicos empíricos para o SPX:** $\nu^2 t = 0.6$, $\alpha = 0.2$, $\rho = -0.7$, garantindo total ausência de arbitragem de borboleta.

---

## 8 Critérios de Escolha: Volatilidade Local vs Heston vs Saltos

A seleção da arquitetura de modelagem apropriada depende da aplicação final e das necessidades de gestão de risco.

| Critério / Modelo | Volatilidade Local (Dupire) | Parametrização SSVI / SVI | Volatilidade Estocástica (Heston) | Difusão com Saltos (Merton) |
| :--- | :--- | :--- | :--- | :--- |
| **Ajuste aos Preços VANILLA** | Perfeito (por construção). | Quase perfeito (excelente fit em SPX/FX). | Bom para prazos médios/longos; falha no curto prazo. | Excelente no curto prazo; razoável nos prazos longos. |
| **Garantia de Sem Arbitragem** | Exige sanitização prévia rigorosa da superfície. | Garantida analiticamente via condições de parâmetros. | Garantida por construção martingale. | Garantida por construção martingale. |
| **Comportamento das Caudas** | Determinado estaticamente pelos dados. | Linear no log-strike (Lee bound $\le 2$). | Determinado pelos parâmetros CIR. | Caudas pesadas geradas pelos saltos. |
| **Smile de Curto Prazo ($t \to 0$)** | Instável se os dados forem ruidosos. | Permite V-shape se $\phi_0 > 0$. | Achata demasiadamente ($\phi_0 = 0$). | Preserva V-shape e skew acentuado. |
| **Hedging de Exóticos** | Ruim para dinâmicas de longo prazo. | Usado como interpolação e extrepolador estável. | Bom para exóticos dependentes de variância. | Essencial para opções digitais e de barreira de curto prazo. |

---

## 9 Implementação e Checklist Prático de Calibração

O processo de ajuste de uma superfície de volatilidade a partir de cotações brutas de mercado deve seguir um protocolo rígido para precaver arbitragens e instabilidades numéricas.

```
+-------------------------------------------------------------------+
|               CHECKLIST DE CALIBRAÇÃO DE SUPERFÍCIE               |
+-------------------------------------------------------------------+
  [1] Capturar cotações Bid/Ask e extrair volatilidades Mid.
  [2] Converter volatilidades para preços de opções via Black-Scholes.
  [3] Executar ajuste inicial via Square-Root SVI (Initial Guess).
  [4] Otimizar fatia a fatia com penalidade de Crossedness.
  [5] Validar ausência de raízes reais do polinômio de Ferrari-Cardano.
  [6] Verificar g(k) >= 0 e limite d+(k) -> -infty para toda fatia.
  [7] Interpolar fatias preservando valor de chamada relativo.
  [8] Extrapolar para maturidades longas via SSVI funcional.
+-------------------------------------------------------------------+
```

### 9.1 Protocolo Numérico de Calibração Fatia por Fatia

1.  **Ajuste Inicial Square-Root SVI:** A partir das volatilidades implícitas mid $\sigma_{ij} = \sigma_{BS}(k_i, t_j)$, obtêm-se os preços mid das opções. Ajusta-se uma superfície *Square-Root SVI* inicial minimizando a soma dos erros quadráticos dos preços.
2.  **Quantificação de Cruzamento de Fatias (*Crossedness*):**
    Para duas fatias adjacentes $t_1 < t_2$ com parâmetros $\chi_1$ e $\chi_2$, calcula-se a interseção igualando $w(k, t_1) = w(k, t_2)$.
    Esta equação é transformada em um polinômio quártico de forma:
    $$\alpha_4 k^4 + \alpha_3 k^3 + \alpha_2 k^2 + \alpha_1 k + \alpha_0 = 0$$
    Cujas raízes $k_i \; (i=1,\dots,n; \; n \le 4)$ são encontradas analiticamente pelo método de Ferrari-Cardano.
    Se existirem raízes reais, definem-se os pontos médios:
    $$\tilde{k}_1 = k_1 - 1, \quad \tilde{k}_i = \frac{k_{i-1} + k_i}{2} \quad (2 \le i \le n), \quad \tilde{k}_{n+1} = k_n + 1$$
    O grau de cruzamento (*crossedness*) é:
    $$\text{Crossedness} = \max_i \left( \max\left[0, \; w(\tilde{k}_i, \chi_1) - w(\tilde{k}_i, \chi_2)\right] \right)$$
3.  **Otimização com Penalidade:** Minimiza-se a distância quadrática entre os preços teóricos SVI e os preços de mercado com uma penalidade severa aplicada à *crossedness*.

### 9.2 Interpolação e Extrapolação Sem Arbitragem

#### Algoritmo de Interpolação Livre de Arbitragem (Lemma 5.1):
Dadas duas fatias calibradas e livres de arbitragem $w(k, t_1)$ e $w(k, t_2)$ com $t_1 < t < t_2$, para qualquer interpolação monótona da variância total ATM $\theta_t$, calcula-se o preço interpolado da Call por:
$$\frac{C(F_t, K_t, t)}{K_t} = \alpha_t \frac{C(F_1, K_1, t_1)}{K_1} + (1 - \alpha_t) \frac{C(F_2, K_2, t_2)}{K_2}$$
com o fator de ponderação:
$$\alpha_t = \frac{\sqrt{\theta_{t_2}} - \sqrt{\theta_t}}{\sqrt{\theta_{t_2}} - \sqrt{\theta_{t_1}}} \in [0, 1]$$

A superfície de volatilidade interpolada é recuperada diretamente pela inversão da fórmula de Black-Scholes, garantindo $g(k) \ge 0$ e $\partial_t w \ge 0$.

#### Extrapolação Além da Última Fatia ($t > t_n$):
Recalibra-se a última fatia $t_n$ na forma SSVI. Fixa-se uma extensão monótona crescente de $\theta_t$ e extrapola-se por:
$$w(k, \theta_t) = w(k, \theta_{t_n}) + \theta_t - \theta_{t_n}$$
Pelo Teorema 4.3, como adiciona-se uma função dependente apenas do tempo $\alpha_t = \theta_t - \theta_{t_n} \ge 0$, a nova superfície estendida permanece estritamente livre de arbitragem estática.

---

## 10 Tabela Comparativa e Glossário Técnico

### 10.1 Tabela Comparativa das Parametrizações SVI

| Parametrização | Equação Governante | Vantagens Principais | Limitações |
| :--- | :--- | :--- | :--- |
| **Raw SVI** | $w(k) = a + b[\rho(k-m) + \sqrt{(k-m)^2+\sigma^2}]$ | Simplicidade analítica; parâmetros intuitivos no espaço $k$. | Dificuldade para impor limites globais de ausência de arbitragem de borboleta. |
| **Natural SVI** | $w(k) = \Delta + \frac{\omega}{2}[1 + \zeta\rho(k-\mu) + \sqrt{(\zeta(k-\mu)+\rho)^2 + (1-\rho^2)}]$ | Conexão teórica direta com o limite assintótico do modelo de Heston. | Parâmetros menos intuitivos para operadores de mercado. |
| **SVI-JW** | Expressa via $v_t, \psi_t, p_t, c_t, \tilde{v}_t$ na volatilidade implícita. | Parâmetros altamente estáveis no tempo; significado financeiro imediato (skew, wings). | Exige conversão para Raw/Natural para cálculo do $g(k)$. |
| **SSVI** | $w(k, \theta_t) = \frac{\theta_t}{2}[1 + \rho\phi(\theta_t)k + \sqrt{(\phi(\theta_t)k+\rho)^2+(1-\rho^2)}]$ | **Condições analíticas necessárias e suficientes** para eliminar arbitragem de calendário e borboleta na superfície inteira. | Menos flexibilidade para ajustar pequenas deformações locais pontuais. |
| **SVI-SABR** | $\sigma_{BS}^2(k) = \frac{\alpha^2}{2}[1 + \rho\frac{\nu}{\alpha}k + \sqrt{(\frac{\nu}{\alpha}k+\rho)^2+(1-\rho^2)}]$ | Elimina a densidade negativa do SABR mantendo alta qualidade de fit. | Restrito a fatias individuais. |

### 10.2 Glossário Técnico

*   **Arbitragem Estática:** Condição de mercado na qual existe uma combinação de posições em opções que gera lucro positivo sem risco no início ou no vencimento, violando a existência de uma medida martingale risco-neutra.
*   **Arbitragem de Spread de Calendário:** Violação da monotonicidade dos preços de opções em relação ao tempo de vencimento ($\partial_t w < 0$).
*   **Arbitragem de Borboleta (*Butterfly Arbitrage*):** Violação da convexidade dos preços de opções em relação ao strike, correspondendo a uma densidade de probabilidade risco-neutra negativa ($g(k) < 0$ ou $p(k) < 0$).
*   **Crossedness (Grau de Cruzamento):** Métrica quantitativa que mede o valor máximo pelo qual uma fatia de variância total invade ou cruza a fatia de outra maturidade em um gráfico $w(k)$.
*   **Densidade de Breeden-Litzenberger:** A densidade de probabilidade risco-neutra extraída da segunda derivada do preço da opção Call em relação ao preço de exercício $K$.
*   **Fórmula de Momentos de Lee:** Teorema que limita a inclinação assintótica da variância implícita em $w(k) \sim \beta |k|$ quando $|k| \to \infty$, demonstrando que $\beta \in$.
*   **Log-Moneyness ($k$):** Variável padronizada definida como $k = \log(K/F)$, que centraliza o at-the-money em $k=0$.
*   **Risk Reversal ($RR$):** Indicador de assimetria no mercado de câmbio dado pela diferença de volatilidade implícita entre uma Call OTM e uma Put OTM de mesmo delta.
*   **Slice (Fatia):** O corte unidimensional da superfície de volatilidade para uma maturidade específica $t$.
*   **Tempo de Variância ATM ($\theta_t$):** Produto da variância implícita at-the-money pelo tempo $t$, usado como a variável de tempo no SSVI.