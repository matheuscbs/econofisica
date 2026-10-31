<!-- imported study note (resumo.md) -->
# Documento de Briefing: Superfície de Volatilidade e Modelos de Smile (Módulo M04)

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M04

↑ M04 · Resumo · Completo

## Resumo Executivo

O Módulo M04 do curso de Econofísica Khem Kapital aborda a modelagem matemática e financeira da superfície de volatilidade implícita e dos modelos de *smile*, com foco central nas parametrizações **SVI** (*Stochastic Volatility Inspired*) desenvolvidas por Jim Gatheral e nas suas extensões livres de arbitragem, como a **SSVI** (*Surface SVI*). 

Historicamente desenvolvida no Merrill Lynch em 1999 e divulgada publicamente em 2004, a parametrização SVI tornou-se um padrão de indústria na finança quantitativa devido a duas propriedades essenciais:
1. **Comportamento Assintótico Correto:** Para um tempo fixo até o vencimento $t$, a variância implícita de Black-Scholes $\sigma^2_{BS}(k, t)$ é linear no log-strike $k$ quando $|k| \to \infty$, o que é rigorosamente consistente com a fórmula dos momentos de Roger Lee.
2. **Ajuste Prático e Consistência com Modelos Estocásticos:** É notavelmente eficiente para ajustar preços de opções cotadas no mercado, além de representar o limite de grande maturidade do modelo de volatilidade estocástica de Heston.

Apesar de sua popularidade, ajustes ingênuos do modelo SVI podem introduzir arbitragem estática — especificamente arbitragem de *calendar spread* (quando as linhas de variância total se cruzam no tempo) e arbitragem de borboleta (*butterfly arbitrage*, onde a densidade de probabilidade implícita associada se torna negativa). Durante anos, a busca por parametrizações simples em forma fechada que garantissem a ausência total de arbitragem foi considerada inviável na literatura quantitativa.

Este briefing sintetiza as definições matemáticas formais, as parametrizações equivalentes do SVI (Raw, Natural, SVI-JW e SSVI), as condições necessárias e suficientes para eliminar arbitragens estáticas, os algoritmos práticos de calibração e interpolação/extrapolação, bem como as aplicações operacionais em *trading* de derivativos e a integração do módulo com o ecossistema mais amplo de modelos financeiros.

---

## Análise Detalhada dos Temas Principais

### Definição da Superfície de Volatilidade e Inexistência de Arbitragem Estática

Dado um processo para o preço do ativo subjacente $(S_t)_{t \ge 0}$ com filtração natural $(\mathcal{F}_t)_{t \ge 0}$, o processo do preço a termo (*forward*) é definido por $F_t := \mathbb{E}(S_t \mid \mathcal{F}_0)$. Para qualquer log-moneyness $k \in \mathbb{R}$ e vencimento $t > 0$, o preço de uma opção de compra (*European Call*) com strike $K = F_t e^k$ sob o modelo de Black-Scholes é denotado por $C_{BS}(k, \sigma^2 t)$.

Definimentos fundamentais da superfície de volatilidade:
* **Variância Implícita Total:** $w(k, t) = \sigma^2_{BS}(k, t) t$.
* **Variância Implícita:** $v(k, t) = \sigma^2_{BS}(k, t) = \frac{w(k, t)}{t}$.
* **Superfície de Volatilidade:** O mapeamento bidimensional $(k, t) \mapsto w(k, t)$.
* **Fatia (*Slice*):** A função unidimensional $k \mapsto w(k, t)$ para um vencimento fixo $t > 0$.

De acordo com a caracterização modelo-independente de Cox e Hobson, uma superfície de volatilidade está isenta de **arbitragem estática** se e somente se satisfizer duas condições indispensáveis:
1. **Ausência de Arbitragem de Calendar Spread:** Para dividendos proporcionais ao preço do ativo, a variância total deve ser não decrescente no tempo para um moneyness fixo, ou seja:
$$\partial_t w(k, t) \ge 0, \quad \forall k \in \mathbb{R}, \, t > 0$$
Visualmente, no gráfico de variância implícita total $w(k,t)$ versus $k$, não pode haver cruzamento entre fatias de tempos diferentes.
2. **Ausência de Arbitragem de Borboleta (*Butterfly Arbitrage*):** Cada fatia individual deve gerar uma densidade de probabilidade $p(k)$ estritamente não negativa. 

Diferenciando explicitamente a fórmula de Black-Scholes em relação ao strike, a densidade de probabilidade implícita $p(k)$ é expressa como:
$$p(k) = \frac{g(k)}{\sqrt{2\pi w(k)}} \exp\left( -\frac{d_-(k)^2}{2} \right)$$
Onde a função altamente não linear $g(k)$ é definida por:
$$g(k) := \left( 1 - \frac{k w'(k)}{2 w(k)} \right)^2 - \frac{w'(k)^2}{4} \left( \frac{1}{w(k)} + \frac{1}{4} \right) + \frac{w''(k)}{2}$$
Uma fatia de volatilidade está livre de arbitragem de borboleta se e somente se $g(k) \ge 0$ para todo $k \in \mathbb{R}$ e a condição assintótica de contorno $\lim_{k \to +\infty} d_+(k) = -\infty$ for satisfeita, garantindo que a densidade integre exatamente um.

---

### Formulações do Modelo SVI

O modelo SVI possui três formulações matemáticas equivalentes, cada uma adaptada para uma finalidade específica (matemática, teórica ou operacional).

#### 1. Parametrização Raw SVI
Para um conjunto de parâmetros $\chi_R = \{a, b, \rho, m, \sigma\}$, a variância total implícita é dada por:
$$w(k; \chi_R) = a + b \left\{ \rho (k - m) + \sqrt{(k - m)^2 + \sigma^2} \right\}$$
Sujeito às condições $a \in \mathbb{R}$, $b \ge 0$, $|\rho| < 1$, $m \in \mathbb{R}$, $\sigma > 0$, e $a + b \sigma \sqrt{1 - \rho^2} \ge 0$ (que assegura que o mínimo da função $w(\cdot, \chi_R)$ seja não negativo).

Impacto das alterações dos parâmetros na forma do *smile*:
* **$a$:** Translada o nível geral de variância verticalmente.
* **$b$:** Aumenta as inclinações das asas de *put* e *call*, estreitando o *smile*.
* **$\rho$:** Rotaciona o *smile* no sentido anti-horário; diminui a inclinação da asa esquerda e aumenta a da asa direita.
* **$m$:** Translada o *smile* horizontalmente para a direita.
* **$\sigma$:** Reduz a curvatura no dinheiro (*At-The-Money* - ATM).

#### 2. Parametrização Natural SVI
Com o conjunto $\chi_N = \{\Delta, \mu, \rho, \omega, \zeta\}$, a variância total é expressa por:
$$w(k; \chi_N) = \Delta + \frac{\omega}{2} \left\{ 1 + \zeta \rho (k - \mu) + \sqrt{(\zeta(k - \mu) + \rho)^2 + (1 - \rho^2)} \right\}$$
Esta forma é uma generalização natural do limite de maturidade infinita do modelo de Heston. As transformações bijetoras entre os parâmetros *Raw* e *Natural* são explicitadas na tabela a seguir:

| Parâmetro Raw | Correspondência a partir do Natural | Parâmetro Natural | Correspondência a partir do Raw |
| :--- | :--- | :--- | :--- |
| **$a$** | $\Delta + \frac{\omega}{2}(1 - \rho^2)$ | **$\Delta$** | $a - \frac{\omega}{2}(1 - \rho^2)$ |
| **$b$** | $\frac{\omega \zeta}{2}$ | **$\mu$** | $m + \frac{\rho \sigma}{\sqrt{1 - \rho^2}}$ |
| **$\rho$** | $\rho$ | **$\rho$** | $\rho$ |
| **$m$** | $\mu - \frac{\rho}{\zeta}$ | **$\omega$** | $2 b \sigma \sqrt{1 - \rho^2}$ |
| **$\sigma$** | $\frac{\sqrt{1 - \rho^2}}{\zeta}$ | **$\zeta$** | $\frac{\sqrt{1 - \rho^2}}{\sigma}$ |

#### 3. Parametrização SVI Jump-Wings (SVI-JW)
Inspirada por propostas operacionais de Tim Klassen no Goldman Sachs, a parametrização SVI-JW expressa a variância implícita $v$ (em vez da variância total $w$) através de parâmetros intuitivos para operadores de mercado: $\chi_J = \{v_t, \psi_t, p_t, c_t, \tilde{v}_t\}$.

Relações diretas a partir dos parâmetros *Raw* (com $w_t = v_t t$):
* **Variância ATM ($v_t$):** $v_t = \frac{1}{t} \left[ a + b \left( -\rho m + \sqrt{m^2 + \sigma^2} \right) \right]$
* **Skew ATM ($\psi_t$):** $\psi_t = \frac{\partial \sigma_{BS}(k,t)}{\partial k} \Big|_{k=0} = \frac{1}{2 \sqrt{w_t}} b \left( -\frac{m}{\sqrt{m^2 + \sigma^2}} + \rho \right)$
* **Inclinação da Asa de Put ($p_t$):** $p_t = \frac{1}{\sqrt{w_t}} b (1 - \rho)$
* **Inclinação da Asa de Call ($c_t$):** $c_t = \frac{1}{\sqrt{w_t}} b (1 + \rho)$
* **Variância Implícita Mínima ($\tilde{v}_t$):** $\tilde{v}_t = \frac{1}{t} \left( a + b \sigma \sqrt{1 - \rho^2} \right)$

A escolha do *skew* de volatilidade $\psi_t$ reflete a observação empírica de que a volatilidade se distribui de forma aproximadamente lognormal. Quando os *smiles* escalam proporcionalmente a $1/\sqrt{w_t}$, os parâmetros SVI-JW permanecem constantes ao longo dos vencimentos, permitindo extrapolações estáveis para prazos longos.

---

### Modelo Surface SVI (SSVI) e Condições Teóricas de Ausência de Arbitragem

Para garantir analiticamente a ausência de arbitragem estática em toda a superfície, introduz-se o modelo **SSVI**, que parametriza a variância total em função do tempo de variância ATM, $\theta_t := \sigma^2_{BS}(0, t) t$:

$$w(k, \theta_t) = \frac{\theta_t}{2} \left\{ 1 + \rho \phi(\theta_t) k + \sqrt{(\phi(\theta_t) k + \rho)^2 + (1 - \rho^2)} \right\}$$

onde $\phi: (0, \infty) \to (0, \infty)$ é uma função suave. O *skew* de volatilidade ATM sob SSVI é dado por $\partial_k \sigma_{BS}(k,t)|_{k=0} = \frac{\rho \sqrt{\theta_t} \phi(\theta_t)}{2 \sqrt{t}}$.

#### Teorema de Ausência de Arbitragem de Calendar Spread em SSVI
A superfície SSVI está isenta de arbitragem de *calendar spread* se e somente se:
1. $\partial_t \theta_t \ge 0, \quad \forall t \ge 0$
2. $0 \le \partial_\theta (\theta \phi(\theta)) \le \frac{1}{\rho^2} \left( 1 + \sqrt{1 - \rho^2} \right) \phi(\theta), \quad \forall \theta > 0$ *(para $\rho = 0$, o limite superior é infinito).*

Na prática, isso significa que o *skew* em termos de variância total deve ser monotonicamente crescente no tempo de negociação, enquanto o *skew* em termos de volatilidade implícita deve ser monotonicamente decrescente.

#### Teorema de Ausência de Arbitragem de Borboleta em SSVI
A superfície SSVI está isenta de arbitragem de borboleta se as seguintes condições forem satisfeitas para todo $\theta > 0$:
1. $\theta \phi(\theta) (1 + |\rho|) < 4$ *(condição estrita para satisfazer os limites assintóticos de Lee e garantir integração da densidade a um).*
2. $\theta \phi(\theta)^2 (1 + |\rho|) \le 4$.

Traduzido para os parâmetros SVI-JW, uma fatia estará livre de arbitragem de borboleta se:
$$\sqrt{v_t t} \max(p_t, c_t) < 4 \quad \text{e} \quad (p_t + c_t) \max(p_t, c_t) \le 8$$

#### Exemplos Notáveis de Superfícies SSVI

1. **Superfície Tipo Heston:**
   $$\phi(\theta) = \frac{1}{\lambda \theta} \left( 1 - \frac{1 - e^{-\lambda \theta}}{\lambda \theta} \right)$$
   Livre de arbitragem estática se $\lambda \ge \frac{1 + |\rho|}{4}$. É perfeitamente consistente com o *skew* de variância do modelo de volatilidade estocástica de Heston.

2. **Superfície Lei de Potência (*Power-Law*):**
   $$\phi(\theta) = \frac{\eta}{\theta^\gamma (1 + \theta)^{1-\gamma}}$$
   Completamente livre de arbitragem estática desde que $\gamma \in (0, 1/2]$ e $\eta (1 + |\rho|) \le 2$. Esta forma captura com precisão empírica a estrutura a termo do *skew* observada no mercado de ações.

3. **Extensão via Função Temporal ($\alpha_t$):**
   Se $w(k, t)$ é livre de arbitragem estática e $\alpha: \mathbb{R}_+ \to \mathbb{R}_+$ é uma função não negativa e crescente no tempo, a superfície estendida $w_\alpha(k, \theta_t) := w(k, \theta_t) + \alpha_t$ também é garantida como livre de arbitragem estática.

---

### Correção Prática de Arbitragem e Comparação SVI vs. SABR

#### O Caso do "Smile de Axel Vogt"
Axel Vogt expôs no fórum Wilmott.com um conjunto de parâmetros *Raw SVI* que gera uma violação severa de arbitragem de borboleta (densidade negativa):
$$\{a, b, m, \rho, \sigma\} = \{-0.0410, \, 0.1331, \, 0.3586, \, 0.3060, \, 0.4153\} \quad \text{com } t = 1$$
Convertendo para parâmetros SVI-JW, obtém-se:
$$\{v_t, \psi_t, p_t, c_t, \tilde{v}_t\} = \{0.01742625, \, -0.1752111, \, 0.6997381, \, 1.316798, \, 0.0116249\}$$

Para eliminar a arbitragem mantendo fixos os parâmetros de mercado mais observáveis ($v_t, \psi_t, p_t$), as regras teóricas de SSVI determinam a substituição da asa de *call* e da variância mínima pelos valores limite que garantem arbitragem zero:
$$c'_t = p_t + 2\psi_t = 0.3493158 \quad \text{e} \quad \tilde{v}'_t = v_t \frac{4 p_t c'_t}{(p_t + c'_t)^2} = 0.01548182$$

Via otimização numérica (minimizando a soma dos quadrados das diferenças de preços de opções com uma penalidade para densidades negativas), encontra-se a solução "ótima" que minimiza a distorção no mercado e elimina a arbitragem:
$$c^*_t = 0.8564763 \quad \text{e} \quad \tilde{v}^*_t = 0.0116249$$
O otimizador reduz a asa de *call* mantendo a variância mínima inalterada, restaurando a positividade da função $g(k)$.

#### SVI-SABR versus SABR Padrão
O modelo clássico SABR (com $\beta = 1$) produz a volatilidade implícita:
$$\sigma^{SABR}_{BS}(k) = \alpha f\left(\frac{k}{\alpha}\right), \quad f(y) = -\frac{\nu y}{\log\left( \frac{\sqrt{\nu^2 y^2 + 2\rho\nu y + 1} - \nu y - \rho}{1-\rho} \right)}$$
É amplamente sabido que o modelo SABR sofre de arbitragem de borboleta significativa em *strikes* extremos (a densidade implícita torna-se visivelmente negativa nas asas distantes).

Em contrapartida, a fórmula **SVI-SABR**:
$$\sigma^2_{BS}(k) = \frac{\alpha^2}{2} \left\{ 1 + \rho \frac{\nu}{\alpha} k + \sqrt{\left( \frac{\nu}{\alpha} k + \rho \right)^2 + (1 - \rho^2)} \right\}$$
tem densidade **garantida estritamente positiva** desde que satisfeitas as condições $\alpha \nu t (1 + |\rho|) < 4$ e $\nu^2 t (1 + |\rho|) < 4$. Para dados do índice SPX, onde valores típicos são $\nu^2 t = 0.6$, $\alpha = 0.2$ e $\rho = -0.7$, a condição é totalmente cumprida, tornando o SVI-SABR um substituto perfeito para o SABR em motores de precificação de derivativos.

---

### Algoritmo de Calibração, Interpolação e Extrapolação

Para calibrar uma superfície completa a dados de mercado sem violar regras de arbitragem:

#### 1. Quantificação de Cruzamento (*Crossedness*)
Para duas fatias SVI com parâmetros $\chi_1$ e $\chi_2$ ($t_2 > t_1$), determinam-se os pontos de interseção $k_i$ ($n \le 4$). Ordenando os pontos e definindo pontos médios $\tilde{k}_i$, o valor do cruzamento $c_i$ é:
$$c_i = \max\left[ 0, \, w(\tilde{k}_i, \chi_1) - w(\tilde{k}_i, \chi_2) \right]$$
A **cruzabilidade (*crossedness*)** das duas fatias é definida como $\max(c_i)$. Se $n=0$, a cruzabilidade é nula.

#### 2. Receita de Calibração
1. A partir das volatividades implícitas de mercado $\sigma_{ij} = \sigma_{BS}(k_i, t_j)$, calcular os preços médios das opções via Black-Scholes.
2. Ajustar uma superfície SVI raiz-quadrada (*square-root SVI*) como estimativa inicial.
3. Ajustar fatia por fatia minimizando a soma dos erros quadráticos dos preços, impondo uma penalidade severa para qualquer cruzamento com a fatia anterior ou posterior (medido pela *crossedness*).

#### 3. Interpolação Sem Arbitragem Estática
Dadas duas fatias calibradas e livres de arbitragem $w(k, t_1)$ e $w(k, t_2)$ com $w(k, t_2) \ge w(k, t_1)$, interpola-se a razão de preço da opção $C_t / K_t$ para qualquer $t \in (t1, t2)$:
$$\frac{C_t}{K_t} = \alpha_t \frac{C_1}{K_1} + (1 - \alpha_t) \frac{C_2}{K_2}, \quad \text{com } \alpha_t = \frac{\sqrt{\theta_{t2}} - \sqrt{\theta_t}}{\sqrt{\theta_{t2}} - \sqrt{\theta_{t1}}} \in [0, 1]$$
Como a combinação linear preserva a convexidade ($\partial^2_{KK} C_t \ge 0$) e a monotonicidade temporal ($\partial_t (C_t / K_t) \ge 0$), a fatia interpolada é analiticamente garantida como livre de arbitragem estática.

#### 4. Extrapolação
* **Para $t < t_1$:** Interpola-se entre $t_0 = 0$ (onde a opção de compra vale apenas seu valor intrínseco) e a primeira fatia $t_1$.
* **Para $t > t_n$:** Re-calibra-se a última fatia cotada na forma SSVI, fixa-se uma extensão monotonicamente crescente para $\theta_t$ (asymptoticamente linear no tempo) e extrapola-se por $w(k, \theta_t) = w(k, \theta_{tn}) + \theta_t - \theta_{tn}$, o que mantém a ausência de arbitragem de borboleta de acordo com o Teorema 4.3.

---

## Citações Importantes e Contexto Detalhado

### 1. Limite Assintótico de Heston e o Modelo SVI
> *"As shown in Gatheral and Jacquier (2011), the SVI parameterization is not arbitrary in the sense that the large-maturity limit of the Heston implied volatility smile is exactly SVI."*

* **Contexto:** Esta afirmação é fundamental para demonstrar que o modelo SVI não é apenas uma construção empírica ou ad-hoc de ajuste de curvas (*curve fitting*). Existe uma conexão matemática rigorosa entre modelos teóricos contínuos baseados em equações diferenciais estocásticas (como o modelo de volatilidade estocástica de Heston) e a fórmula funcional de SVI. Quando o tempo até o vencimento tende ao infinito ($t \to \infty$), a volatilidade implícita gerada por Heston converge exatamente para a parametrização SVI, fundamentando teoricamente o uso do SVI no mercado.

### 2. A Inexistência Histórica de Parametrizações Fechadas Livres de Arbitragem
> *"Prior work has not successfully attempted to eliminate static arbitrage and indeed, efforts to find simple closed-form arbitrage-free parameterizations of the implied volatility surface are still widely considered to be futile."*

* **Contexto:** O texto ressalta o avanço proporcionado pelas pesquisas de Gatheral e Jacquier (2012). Até a publicação dos resultados sobre a classe **SSVI**, a comunidade quantitativa considerava impossível encontrar uma equação matemática fechada, simples e tratável para a superfície de volatilidade que garantisse simultaneamente ausência de arbitragem de *calendar spread* e ausência de arbitragem de borboleta sem recorrer a métodos numéricos pesados e de otimização restrita por grade.

### 3. Definição Formal de Inexistência de Arbitragem Estática
> *"A volatility surface is free of static arbitrage if and only if the following conditions are satisfied: (i) it is free of calendar spread arbitrage; (ii) each time slice is free of butterfly arbitrage."*

* **Contexto:** Esta definição formal estabelece os pilares necessários para a consistência dos modelos de precificação no mercado de derivativos. A ausência de arbitragem de *calendar spread* assegura que o valor do tempo das opções seja estritamente positivo (opções de maior maturidade devem ser mais valiosas). A ausência de arbitragem de borboleta garante que a distribuição de probabilidade neutra ao risco $p(k)$ associada aos preços de mercado não assuma valores negativos, respeitando os axiomas fundamentais da teoria de probabilidades de Kolmogorov e do teorema fundamental da precificação de ativos.

### 4. Falha do Modelo SABR em Asas Extremas vs. Solução SVI-SABR
> *"It is well known that the SABR volatility smile is susceptible to butterfly arbitrage... On the other hand, the SVI-SABR density is guaranteed positive so long as $a \nu t (1 + |\rho|) < 4$ and $\nu^2 t (1 + |\rho|) < 4$."*

* **Contexto:** O modelo SABR é largamente empregado em mesas de operaçôes de taxas de juros e moedas (*FX*). No entanto, o modelo falha drasticamente ao precificar opções muito fora do dinheiro (*deep OTM*), gerando preços que permitem montar operações de borboleta com ganho livre de risco (densidade de probabilidade negativa). O SVI-SABR corrige essa falha estrutural ao substituir a aproximação de volatilidade por uma função do tipo SVI, garantindo densidades estritamente positivas em todas as fatias sob limites analíticos simples.

---

## Aplicações em Trading e Conexão com Outros Módulos

### Aplicações Práticas em Mesa de Operações (*Trading*)

1. **Gestão de Risco e Cálculo de Gregas:**
   A interpolação e extrapolação livres de arbitragem fornecidas pelo SSVI garantem que derivadas parciais do preço das opções em relação ao *spot* (Delta $\Delta$, Gamma $\Gamma$), ao tempo (Theta $\Theta$) e à volatilidade (Vega $\mathcal{V}$, Volga, Vanna) permaneçam bem-comportadas e sem contornos espúrios ou descontinuidades, o que é crucial para estratégias de *delta-hedging* e *vega-hedging* dinâmicos.

2. **Precificação de Derivativos Exóticos e de Volatilidade:**
   Derivativos cujos *payoffs* dependem de múltiplos *strikes* ou da volatilidade percebida (como *volatility swaps*, *variance swaps*, opções barreira e opções *cliquet*) exigem uma superfície de volatilidade contínua e sem arbitragem estática. A presença de uma densidade implícita negativa geraria distorções severas no valor presente desses exóticos.

3. **Substituição de Motores de Precificação SABR por SVI-SABR:**
   Mesas de derivativos em mercados de câmbio (*FX*) e renda fixa podem substituir o SABR tradicional pelo SVI-SABR em suas ferramentas de precificação. Isso elimina erros de marcação a mercado em opções *deep OTM* sem perder a intuição dos parâmetros originais de volatilidade inicial, correlação e volatilidade da volatilidade.

4. **Interpolação e Extrapolação de Vencimentos Não Cotados:**
   Através da parametrização SVI-JW e do modelo SSVI, mesclar ativos com alta liquidez em certas datas de vencimento e preencher lacunas em datas sem cotação líquida torna-se um processo transparente e matematicamente robusto.

---

### Conexão com o Ecossistema do Curso Econofísica Khem Kapital

O Módulo M04 atua como a ponte de integração teórica e prática entre os diversos módulos do curso:

* **Conexão com Fundamentos de Precificação de Opções (Módulos Iniciais):**
  Aprofunda a teoria clássica de Black-Scholes, expandindo a suposição irrealista de volatilidade constante para uma superfície dinâmica tridimensional dependente do *strike* e da maturidade.

* **Conexão com Modelos de Volatilidade Estocástica e Salto (Módulos Intermediários):**
  O módulo demonstra analiticamente como parametrizações da superfície de volatilidade conectam-se aos modelos de tempo contínuo. A verificação de que o limite de maturidade longa do modelo de **Heston** resulta exatamente no SVI e que a forma *Power-Law* do SSVI captura a natureza em "V" de **modelos de salto** (como Merton e Kou) unifica a modelagem empírica à modelagem estrutural de processos estocásticos.

* **Conexão com Microestrutura e Gestão de Riscos (Módulos Avançados):**
  A calibração do modelo SVI a dados reais do índice SPX demonstra como tratar *spreads* de compra e venda (*bid-ask spreads*), filtrar cotações ruidosas em vencimentos ultracurtos (como opções de vencimento overnight/1 dia) e evitar a propagação do risco de dados incorretos para a gestão de portfólios e limites de risco do fundo.

---

## Insights Acionáveis para Modelagem e Otimização

1. **Protocolo de Calibração em Duas Etapas:**
   Ao ajustar superfícies de volatilidade no mercado de ações (como opções SPX), utilize sempre o ajuste *square-root SVI* como estimativa inicial (*initial guess*). Em seguida, execute a otimização fatia por fatia impondo a função de penalidade de *crossedness* para zerar as violações de *calendar spread*.

2. **Ajuste Focado nas Asas de Call para Correção de Arbitragem:**
   Quando uma fatia cotada apresentar arbitragem de borboleta (como no exemplo de Axel Vogt), mantenha fixos os parâmetros SVI-JW de volatilidade ATM ($v_t$), *skew* ATM ($\psi_t$) e asa de *put* ($p_t$), ajustando preferencialmente a asa de *call* ($c_t$) e a variância mínima ($\tilde{v}_t$). As asas de *call* possuem menor liquidez em mercados de ações e absorvem os ajustes sem distorcer os preços das *puts* no dinheiro e fora do dinheiro.

3. **Adição do Termo Temporal $\alpha_t$ para Ajustar a Curvatura:**
   Para aumentar a flexibilidade no ajuste de superfícies SSVI sem introduzir arbitragem, adicione um termo determinístico e crescente no tempo $\alpha_t$. Isso concede liberdade adicional para ajustar um terceiro parâmetro em cada *smile* sem violar as restrições teóricas de ausência de arbitragem.

4. **Uso das Limitações Assintóticas de Roger Lee na Filtragem de Dados:**
   Descarte ou ajuste automaticamente durante a limpeza de dados qualquer cotação de mercado cuja inclinação assintótica de variância total no log-strike exceda o valor de 2 ($\theta \phi(\theta)(1+|\rho|) \ge 4$), prevenindo falhas de convergência nos algoritmos de otimização quantitativa.