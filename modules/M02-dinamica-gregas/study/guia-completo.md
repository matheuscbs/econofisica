<!-- imported study note (guia-completo.md) -->
# MÓDULO M02: GUIA COMPLETO DE ECONOFÍSICA - DINÂMICA, GREGAS E PATH DEPENDENCE

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M02

↑ M02 · Resumo · Completo

## Sumário Executivo

Este documento serve como um relatório de engenharia financeira e econofísica dedicado ao Módulo M02 do curso *Econofísica Khem Kapital*. O foco central deste módulo reside na modelagem, precificação e gestão de risco de derivativos complexos e dependentes de trajetória (*path-dependent*), bem como na infraestrutura computacional necessária para avaliar portfólios de alta dimensão de forma rigorosa e eficiente.

A precificação de derivativos modernos exige a superação das limitações das soluções analíticas fechadas de Black-Scholes. Enquanto opções vanila dependem apenas do estado do ativo no vencimento, produtos exóticos estruturados — tais como opções asiáticas, de barreira, *lookback*, *cliquet* e notas autopagáveis (*worst-of autocallables*) — demandam a simulação exata ou discretizada de trajetórias estocásticas. Este relatório analisa a dinâmica do Movimento Browniano Geométrico (GBM), comparando esquemas de discretização de Euler-Maruyama e Milstein com técnicas recentes de simulação exata baseadas em amostragem por aceitação-rejeição e encurtamento estocástico (*stochastic thinning*).

Além da precificação sob a medida neutra ao risco, o gerenciamento de portfólios requer o cálculo computacionalmente intensivo de sensibilidades de preços (as "Gregas"). Analisa-se o problema estrutural do método de diferenças finitas (*bumping*), que sofre com o dilema entre erro de truncamento e erro de cancelamento numérico em ponto flutuante, escalando a custo $O(n)$ ou $O(n^2)$ reavaliações de Monte Carlo. Como solução, apresentam-se os métodos de Derivada Caminho a Caminho (*Pathwise Sensitivity* / IPA), Razão de Verossimilhança (*Likelihood Ratio Method* - LRM), Cálculo de Malliavin e Diferenciação Algorítmica Adjunta (*Adjoint Algorithmic Differentiation* - AAD). AAD transforma o programa precificador em um grafo computacional e aplica a regra da cadeia em sentido reverso, permitindo obter o vetor gradiente completo a um custo constante pequeno $O(1)$, independentemente do número de entradas do mercado.

Por fim, abordam-se o impacto do monitoramento discreto em opções de barreira e a aplicação da correção de continuidade de Broadie-Glasserman-Kou (BGK), a resolução do problema de parada ótima para opções americanas (via Árvores Aleatórias, Malhas Estocásticas e Dualidade de Doob-Meyer), técnicas avançadas de redução de variância para *Value-at-Risk* (VaR) e a transição necessária para modelos de Volatilidade Local, Volatilidade Estocástica e Saltos quando o *payoff* exige dinâmicas além do GBM.

---

## Importantes Citações com Contexto

### 1. Sobre a Vantagem Custo-Dimensão do Método de Monte Carlo
> *"Compared to other numerical methods, Monte Carlo simulation has several advantages... its rate of convergence typically does not depend on the dimensionality of the problem. Therefore, it is often attractive to apply Monte Carlo simulation to problems with high dimensions."* — **Nan Chen e L. Jeff Hong (2007)**

*Contexto*: Chen e Hong destacam a propriedade fundamental que torna o método de Monte Carlo a ferramenta padrão para finanças quantitativas. Enquanto métodos baseados em Equações Diferenciais Parciais (PDE) ou redes em grade (*lattices*) sofrem com a "maldição da dimensionalidade" (onde a complexidade computacional cresce exponencialmente com o número de ativos $d \ge 3$), a taxa de convergência do erro padrão no Monte Carlo permanece estritamente $O(1/\sqrt{N})$, tornando-o escalável para cestas multiativos e modelos de taxa com muitos fatores.

### 2. Sobre o Ajuste de Continuidade para Barreira Discreta
> *"The correction shifts the barrier away from the underlying by a factor of $\exp(\beta \sigma \sqrt{\Delta t})$, where $\beta \approx 0.5826$, $\sigma$ is the underlying volatility, and $\Delta t$ is the time between monitoring instants. Compared with using the unadjusted continuous price, our formula reduces the error from $O(1/\sqrt{m})$ to $o(1/\sqrt{m})$, as the number of monitoring points $m$ increases."* — **Mark Broadie, Paul Glasserman e Steven Kou (1997)**

*Contexto*: Fórmulas analíticas fechadas para opções de barreira assumem monitoramento contínuo. Na prática do mercado *over-the-counter* (OTC), contudo, as barreiras são observadas discretamente (por exemplo, no fechamento diário). O uso da fórmula contínua pura gera erros de precificação expressivos. A correção de Broadie-Glasserman-Kou (BGK) prova teoricamente e experimentalmente que deslocar a barreira na direção oposta ao preço inicial captura exatamente o valor esperado do excesso (*overshoot*) da caminhada aleatória discreta sobre o nível limite.

### 3. Sobre a Regra do Grafo Computacional e AAD
> *"A pricing model returns one number. A risk manager needs hundreds: the sensitivity of that number to every spot, every point of every volatility surface, every tenor of every curve, every correlation... Adjoint algorithmic differentiation removes the constraint. It treats the pricer not as a formula to be re-derived but as a program—a graph of elementary operations—and applies the chain rule to that graph backwards... One backward sweep produces the entire gradient, and a theorem guarantees it costs no more than a small constant multiple of a single pricing, independent of how many inputs there are."* — **Martin Burke (2024)**

*Contexto*: Burke contextualiza a mudança de paradigma que a Diferenciação Algorítmica Adjunta (AAD) traz para as mesas de derivativos complexos. Para uma nota estruturada *worst-of autocallable* com 147 entradas de mercado, o cálculo de risco por diferenças finitas centrais exige 295 reavaliações do Monte Carlo. A AAD calcula o gradiente exato com precisão de máquina em uma única varredura reversa, exigindo cerca de $4.2\times$ o tempo de uma única precificação.

---

## Insights Acionáveis

1. **Eliminação do Erro de Discretização em Barreiras Discretas**: Na precificação de opções de barreira com monitoramento discreto (ex.: diário), não utilize a fórmula contínua padrão nem simule malhas extremamente finas. Aplique o deslocamento multiplicativo $H_{adj} = H e^{\pm \beta \sigma \sqrt{\Delta t}}$ na barreira nominal $H$, operando a precificação diretamente em fórmulas analíticas contínuas ou em simulações de passos largos. Isso reduz o erro de aproximação de $O(1/\sqrt{m})$ para $o(1/\sqrt{m})$.
2. **Substituição do Bumping por AAD na Gestão de Risco Intradia**: Para livros de exóticas com centenas de fatores de risco (superfícies de volatilidade, curvas de juros por *tenor*, correlações), substitua o método de diferenças finitas (*bumping*) por motores AAD de modo reverso (*reverse mode*). Isso converte um relatório de risco de processamento noturno de várias horas em um cálculo de poucos segundos, viabilizando o *hedging* dinâmico intradia.
3. **Mitigação de Descontinuidades em Simulação de Monte Carlo**: Para calcular Gregas caminho a caminho (*Pathwise*) em derivativos com *payoffs* descontínuos (como opções digitais, barreiras rígidas ou *autocallables*), aplique técnicas de suavização do *payoff* ou utilize o Método da Razão de Verossimilhança (LRM). A diferenciação direta caminho a caminho em funções degrau resulta em estimadores com viés nulo ou variância infinita devido à falha da condição de continuidade de Lipschitz.
4. **Aplicação do Teorema da Função Implícita na Calibração**: Para obter Gregas em relação aos instrumentos negociados no mercado (*Market Greeks*) e não apenas parâmetros internos do modelo (*Model Greeks*), diferencie através da etapa de calibração utilizando o Teorema da Função Implícita. Isso evita ter que recalibrar o modelo por diferenças finitas para cada choque de mercado.
5. **Redução de Variância Extremal para Cálculo de VaR**: Na estimação do *Value-at-Risk* (VaR) de cauda ($95\%$ ou $99\%$), aplique Amostragem por Importância (*Importance Sampling*) combinada com a aproximação Delta-Gamma e torção exponencial (*exponential twisting*). Isso altera a medida de probabilidade para transformar eventos raros de grande perda no centro do espaço amostral, reduzindo dramaticamente a variância do estimador de Monte Carlo.

---

## 1. GBM como Modelo de Trajetória e Simulação de Monte Carlo Disciplinada

### O Movimento Browniano Geométrico e Solução Exata
A dinâmica estocástica padrão para o preço de um ativo subjacente $S_t$ sob a medida neutra ao risco $\tilde{P}$ é modelada pela Equação Diferencial Estocástica (SDE) do Movimento Browniano Geométrico (GBM):

$$\frac{d S_t}{S_t} = r_t d t + \sigma (t, S_t) d \tilde{W}_t$$

Onde $r_t$ é a taxa livre de risco instantânea, $\sigma (t, S_t)$ é a volatilidade e $\tilde{W}_t$ é um Movimento Browniano padrão $k$-dimensional. No caso escalar unidimensional com parâmetros constantes ($r, \sigma$), a aplicação do Lema de Itô à função $f(t, S_t) = \ln S_t$ fornece a solução analítica exata sem erro de discretização temporal para qualquer instante $T$:

$$S_T = S_0 \exp \left( \left( r - \frac{1}{2} \sigma^2 \right) T + \sigma \sqrt{T} Z \right)$$

Onde $Z \sim \mathcal{N}(0, 1)$ é uma variável aleatória normal padrão.

### Discretização Temporal: Euler-Maruyama vs. Milstein
Quando a SDE possui coeficientes genéricos $d S_t = a(t, S_t) d t + b(t, S_t) d W_t$, a simulação computacional exige a divisão do intervalo de tempo $[0, T]$ em $N$ passos de tamanho $h = T/N$.

#### Esquema de Euler-Maruyama
A aproximação recursiva de Euler-Maruyama é dada por:

$$\hat{S}_{i+1} = \hat{S}_i + a(i h, \hat{S}_i) h + b(i h, \hat{S}_i) \sqrt{h} Z_{i+1}$$

Onde $Z_{i+1} \sim \mathcal{N}(0, 1)$ são i.i.d. O esquema de Euler possui ordem de convergência forte $\gamma = 1/2$, o que significa que $E[|\hat{S}_N - S_T|] \le C h^{1/2}$, e ordem de convergência fraca $\gamma = 1$, tal que $|E[f(\hat{S}_N)] - E[f(S_T)]| \le C h$.

#### Esquema de Milstein
Para obter maior precisão, aplica-se a expansão de Taylor de Itô aos coeficientes $a$ e $b$. Definindo os operadores funcionais:

$$L_0 := \frac{\partial}{\partial t} + a \frac{\partial}{\partial S} + \frac{1}{2} b^2 \frac{\partial^2}{\partial S^2}, \quad L_1 := b \frac{\partial}{\partial S}$$

O esquema de Milstein escalar (com convergência fraca de ordem 2 sob condições de suavidade) expande os integrais estocásticos múltiplos:

$$\hat{S}_{i+1} = \hat{S}_i + L_0 a \cdot \frac{1}{2} h^2 + L_1 a \cdot \Delta I_i + L_0 b \cdot (h \Delta W_i - \Delta I_i) + L_1 b \cdot \frac{1}{2} \left( (\Delta W_i)^2 - h \right)$$

Onde $\Delta W_i = W_{(i+1)h} - W_{ih}$ e $\Delta I_i = \int_{ih}^{(i+1)h} (W_t - W_{ih}) dt$. A implementação requer a amostragem conjunta das variáveis normais correlacionadas $(\Delta W_i, \Delta I_i)^T \sim \mathcal{N} \left( 0, \begin{pmatrix} h & \frac{1}{2}h^2 \\ \frac{1}{2}h^2 & \frac{1}{3}h^3 \end{pmatrix} \right)$.

### Simulação Exata de Difusões (Beskos et al.)
Para eliminar completamente o erro de discretização em SDEs não lineares, utilizam-se técnicas de amostragem por aceitação-rejeição (ARS).
1. **Transformação de Lamperti**: Aplica-se a mudança de variável $Y_t = F(t, S_t) = \int_0^{S_t} \frac{1}{b(t, u)} du$, reduzindo a volatilidade para a unidade: $d Y_t = \tilde{a}(t, Y_t) d t + d W_t$.
2. **Derivada de Radon-Nikodym e Girsanov**: A medida $Q$ induzida por $Y$ em relação à medida de um Movimento Browniano padrão $Z$ é dada por:

$$\frac{d Q}{d Z}(\omega) = \exp \{ A(\omega_T) \} \exp \left\{ - \int_0^T \phi(t, \omega_t) d t \right\}$$

Onde $A(u) = \int_0^u \tilde{a}(y) dy$ e $\phi(t, y) = \frac{1}{2} (\tilde{a}^2(t, y) + \partial \tilde{a}(t, y) / \partial y)$.
3. **Encurtamento Estocástico (*Stochastic Thinning*)**: Se $0 \le \phi(t, y) \le k$, simula-se um processo de Poisson homogêneo com intensidade $k$ no intervalo $[0, T]$, gerando pontos de tempo $0 \le \tau_1 < \dots < \tau_n \le T$. As posições $\omega_{\tau_i}$ são amostradas a partir de uma ponte browniana condicionada ao valor final $\omega_T$. Aceita-se a trajetória se variáveis uniformes $U_i$ satisfizerem $U_i \le \phi(\tau_i, \omega_{\tau_i})/k$ para todo $i$.

Para processos multidimensionais, a transformação exata existe se e somente se a condição de comutatividade das matrizes de volatilidade for satisfeita:

$$\sum_{j=1}^k \frac{\partial b_{im}}{\partial s_j} b_{jl} = \sum_{j=1}^k \frac{\partial b_{il}}{\partial s_j} b_{jm}, \quad \forall (i, m, l)$$

### Simulação Monte Carlo Disciplinada e Convergência
A estimativa do preço de um derivativo com *payoff* $\Phi(S)$ é a média de $N$ réplicas independentes:

$$\hat{V}_N = \frac{1}{N} \sum_{i=1}^N e^{-r T} \Phi(S^{(i)})$$

O Erro Padrão ($SE$) da estimativa é calculado por:

$$SE(\hat{V}_N) = \frac{s_N}{\sqrt{N}} = \sqrt{\frac{1}{N(N-1)} \sum_{i=1}^N \left( e^{-r T} \Phi(S^{(i)}) - \hat{V}_N \right)^2}$$

O Teorema do Limite Central garante que o intervalo de confiança de $95\%$ é dado por $\hat{V}_N \pm 1.96 \cdot SE(\hat{V}_N)$. A reprodutibilidade exige a gestão rigorosa de geradores de números pseudo-aleatórios e sementes (*seeds*).

---

## 2. Gregas de Primeira e Segunda Ordem sob Black-Scholes

As Gregas quantificam a exposição do valor de um derivativo $V$ a alterações nos parâmetros do mercado subjacente e do modelo.

### Gregas de Primeira Ordem

#### Delta ($\Delta$)
Sensibilidade de primeira ordem em relação ao preço do ativo subjacente: $\Delta = \frac{\partial V}{\partial S}$.
*   **Fórmula Call BS**: $N(d_1)$
*   **Fórmula Put BS**: $N(d_1) - 1 = -N(-d_1)$
*   *Intuição e Hedging*: Representa a quantidade de unidades do ativo subjacente que devem ser mantidas na carteira para criar uma posição instantaneamente imunizada contra pequenas variações de preço (cobertura delta-neutra).

#### Vega ($\mathcal{V}$)
Sensibilidade em relação à volatilidade do subjacente: $\mathcal{V} = \frac{\partial V}{\partial \sigma}$.
*   **Fórmula Call/Put BS**: $S_0 \sqrt{T} N'(d_1)$
*   *Intuição*: Mede o risco de exposição a mudanças na volatilidade implícita. É estritamente positiva para opções vanila compradas e atinge seu pico quando a opção está *at-the-money* (ATM).

#### Theta ($\Theta$)
Sensibilidade em relação à passagem do tempo (decaimento temporal): $\Theta = \frac{\partial V}{\partial t} = -\frac{\partial V}{\partial T}$.
*   **Fórmula Call BS**: $-\frac{S_0 N'(d_1) \sigma}{2 \sqrt{T}} - r K e^{-r T} N(d_2)$
*   **Fórmula Put BS**: $-\frac{S_0 N'(d_1) \sigma}{2 \sqrt{T}} + r K e^{-r T} N(-d_2)$
*   *Intuição*: Reflete a perda intrínseca diária de valor da opção à medida que a data de vencimento se aproxima.

#### Rho ($\rho$)
Sensibilidade em relação à taxa de juros livre de risco: $\rho = \frac{\partial V}{\partial r}$.
*   **Fórmula Call BS**: $K T e^{-r T} N(d_2)$
*   **Fórmula Put BS**: $-K T e^{-r T} N(-d_2)$
*   *Intuição*: Quantifica o impacto do custo de oportunidade e do financiamento do ativo no valor presente do preço de exercício.

Onde os parâmetros do modelo Black-Scholes são $d_1 = \frac{\ln(S_0/K) + (r + \frac{1}{2}\sigma^2)T}{\sigma \sqrt{T}}$ e $d_2 = d_1 - \sigma \sqrt{T}$.

### Gregas de Segunda Ordem

#### Gamma ($\Gamma$)
Sensibilidade de segunda ordem ao preço do subjacente (curvatura do Delta): $\Gamma = \frac{\partial^2 V}{\partial S^2} = \frac{\partial \Delta}{\partial S}$.
*   **Fórmula Call/Put BS**: $\frac{N'(d_1)}{S_0 \sigma \sqrt{T}}$
*   *Intuição*: Mede a velocidade com que o Delta se altera frente a variações no preço do ativo. Posições com Gamma elevado exigem rebalanceamento frequente da carteira de hedge.

#### Vanna
Sensibilidade cruzada do Delta em relação à volatilidade (ou do Vega em relação ao spot): $\text{Vanna} = \frac{\partial^2 V}{\partial S \partial \sigma} = \frac{\partial \Delta}{\partial \sigma} = \frac{\partial \mathcal{V}}{\partial S}$.
*   **Fórmula Call/Put BS**: $-N'(d_1) \frac{d_2}{\sigma} = -\frac{N'(d_1) d_2}{\sigma}$
*   *Intuição*: Quantifica como a inclinação do Delta muda quando a volatilidade oscila; essencial para gerenciar o risco de *skew* de volatilidade.

#### Volga / Vomma
Sensibilidade de segunda ordem em relação à volatilidade (curvatura do Vega): $\text{Volga} = \frac{\partial^2 V}{\partial \sigma^2} = \frac{\partial \mathcal{V}}{\partial \sigma}$.
*   **Fórmula Call/Put BS**: $S_0 \sqrt{T} N'(d_1) \frac{d_1 d_2}{\sigma} = \mathcal{V} \frac{d_1 d_2}{\sigma}$
*   *Intuição*: Indica a exposição do livro a grandes saltos de volatilidade implícita.

#### Charm (Delta Bleed)
Sensibilidade cruzada do Delta em relação ao tempo: $\text{Charm} = \frac{\partial^2 V}{\partial S \partial t} = -\frac{\partial \Delta}{\partial T}$.
*   **Fórmula Call BS**: $-N'(d_1) \left( \frac{2 r T - d_2 \sigma \sqrt{T}}{2 T \sigma \sqrt{T}} \right)$
*   *Intuição*: Descreve como o Delta da posição evolui do dia para a noite mantendo-se o preço do spot constante.

---

## 3. O Book de Opções Lido por Gregas, P&L Explain e Decomposição Gamma-Theta-Vega

### A Leitura Estrutural do Book de Opções
A gestão profissional de uma mesa de derivativos exige a agregação das exposições de risco de todos os contratos em termos de suas Gregas operacionais, decompostas geograficamente e por estruturas temporais (*tenors*). O risco de volatilidade não é uma métrica escalar simples, mas sim um vetor ou matriz de Vega bucketizado ao longo da grade de *strikes* e prazos da superfície de volatilidade implícita.

### P&L Explain por Expansão de Taylor
O resultado financeiro diário ($P\&L$) de uma carteira de derivativos entre $t$ e $t + \Delta t$ é explicado via expansão de Taylor até segunda ordem em relação aos fatores de risco observados no mercado ($\Delta S = S_{t+\Delta t} - S_t$, $\Delta \sigma = \sigma_{t+\Delta t} - \sigma_t$, $\Delta r = r_{t+\Delta t} - r_t$):

$$\Delta V \approx \Delta \cdot \Delta S + \frac{1}{2} \Gamma (\Delta S)^2 + \Theta \Delta t + \mathcal{V} \cdot \Delta \sigma + \frac{1}{2} \text{Volga} (\Delta \sigma)^2 + \text{Vanna} (\Delta S \Delta \sigma) + \rho \Delta r + \text{Termos de Ordem Superior}$$

### A Decomposição Gamma-Theta-Vega
Sob o modelo de Black-Scholes, a PDE de precificação estabelece uma relação rigorosa de substituição de risco entre decaimento temporal ($\Theta$) e curvatura de preço ($\Gamma$):

$$\Theta + r S \Delta + \frac{1}{2} \sigma^2 S^2 \Gamma = r V$$

Para uma carteira mantida delta-neutra ($\Delta = 0$) e considerando $r=0$ para simplicidade conceitual, obtém-se:

$$\Theta = -\frac{1}{2} \sigma^2 S^2 \Gamma$$

Esta equação explicita a barganha fundamental do *market maker* de opções:
*   **Comprador de Gamma ($\Gamma > 0$)**: Apresenta $\Theta < 0$. Paga um custo de carregamento diário (decaimento temporal) em troca de capturar lucros ajustando o hedge delta a cada oscilação do preço do subjacente.
*   **Vendedor de Gamma ($\Gamma < 0$)**: Apresenta $\Theta > 0$. Coleta renda diária pelo decaimento do valor das opções, mas incorre em perdas quadráticas em cenários de forte movimentação no ativo subjacente.
*   **Sensibilidade a Volatilidade ($\mathcal{V}$)**: Adiciona a dimensão de alteração na expectativa da amplitude dessas oscilações futuras.

---

## 4. Hedging de Gregas e Limites de Risco

### Estratégias de Neutralização Dinâmica

#### Hedge Delta-Neutro
Consiste em manter a posição imunizada contra oscilações infinitesimais no ativo subjacente. A quantidade de ativos subjacentes $N_S$ a vender para cobrir um livro de opções de valor $V$ é:

$$N_S = -\Delta_{livro} = -\sum_{i} w_i \Delta_i$$

Como $\Delta$ varia continuamente com o preço do subjacente e com o tempo, a carteira requer rebalanceamentos periódicos.

#### Hedge Delta-Gamma Neutro
Para reduzir a frequência e o custo de rebalanceamento do hedge delta, neutraliza-se a curvatura ($\Gamma$) utilizando um instrumento derivativo adicional $V_2$ negociado em mercado (como uma opção vanila com liquidez):

$$\omega_2 = -\frac{\Gamma_{livro}}{\Gamma_{V_2}}$$

Após neutralizar o Gamma com a quantidade $\omega_2$ de $V_2$, ajusta-se a posição no ativo subjacente para recalibrar o Delta global para zero:

$$\omega_S = -\left( \Delta_{livro} + \omega_2 \Delta_{V_2} \right)$$

#### Bucketing de Vega
A neutralização do risco de volatilidade exige a partição do Vega em blocos temporais e por *strikes* no mapa de volatilidade. A carteira é imunizada resolvendo o sistema linear de equações de risco:

$$\mathbf{\mathcal{V}}_{livro} + \sum_{j=1}^M \omega_j \mathbf{\mathcal{V}}_{inst_j} = \mathbf{0}$$

Onde $\mathbf{\mathcal{V}}$ representa os vetores de exposição por célula da grade de volatilidade.

### Limites operacionais de Risco
Os limites operacionais de uma mesa de operações estabelecem teto e piso para o acúmulo de exposures não cobertas:
1. **Limites de Delta Global e por Subjacente**: Máximo valor nocional equivalente exposto a movimentos de preço spot.
2. **Limites de Gamma Convexo**: Restrições ao deslocamento do Delta sob variações de $1\%$ ou $5\%$ no ativo subjacente.
3. **Limites de VaR e Stress Testing**: O *Value-at-Risk* impõe o valor máximo de perda esperada dentro de um horizonte temporal (ex.: 1 dia ou 10 dias) a um determinado nível de confiança (ex.: $99\%$).
4. **Stress Testing de Cenários**: Avaliação de matrizes de choque simultâneo de spot e volatilidade (ex.: Spot $\pm 20\%$ e Volatilidade $\pm 50\%$).

---

## 5. Opções Exóticas e Payoffs Complexos

Opções exóticas são instrumentos cujos *payoffs* diferem dos *calls* e *puts* europeus e americanos padrão, frequentemente dependendo de condições de trajetória ou de múltiplos ativos subjacentes.

```
                                  ┌─ Asiáticas ─── Média Aritmética / Geométrica
                                  │
                                  ├─ Barreiras ─── Knock-in / Knock-out (Up/Down)
                                  │
      ┌─ Dependência de Trajetória ┼─ Lookback ──── Preço Máximo / Mínimo Alcançado
      │                           │
      │                           ├─ Cliquet ───── Catraca (Rendimento Periódico)
Opções│                           │
Exóticas                          └─ Autocall ──── Notas Estruturadas Autopagáveis
      │
      └─ Independente de Trajetória ── Digitais ─── Payoff Descontínuo (Asset/Cash-or-Nothing)
```

### Opções Asiáticas
O *payoff* depende do valor médio do ativo subjacente ao longo da vida da opção.
*   **Média Geométrica (Monitoramento Contínuo)**: $A_T = \exp \left( \frac{1}{T} \int_0^T \ln S_t d t \right)$. Possui solução analítica fechada, pois a média de um GBM sob escala logarítmica permanece distribuída log-normalmente.
*   **Média Aritmética**: $A_T = \frac{1}{m} \sum_{i=1}^m S_{t_i}$. A soma de variáveis log-normais não possui distribuição log-normal fechada, exigindo métodos numéricos, Monte Carlo ou aproximações de momentos.
*   *Payoff de um Call de Strike Fixo*: $\max(A_T - K, 0)$.

### Opções de Barreira
Ativadas (*knock-in*) ou extintas (*knock-out*) quando o preço do subjacente atinge um limite predeterminado $H$.
*   **Down-and-Out Call ($S_0 > H, K > H$)**:
    *   *Payoff*: $(S_T - K)^+$ se $\tau_H > T$; $0$ se $\tau_H \le T$, onde $\tau_H = \inf\{t > 0 : S_t \le H\}$.

### Opções Lookback
O *payoff* depende dos valores extremos (mínimo $M_{min}$ ou máximo $M_{max}$) atingidos pelo ativo durante o contrato.
*   **Call de Floating Strike**: $\max(S_T - M_{min}, 0)$.
*   **Put de Floating Strike**: $\max(M_{max} - S_T, 0)$.

### Opções Digitais (Binárias)
Apresentam *payoffs* descontínuos com degrau no vencimento.
*   **Cash-or-Nothing Call**: Paga um valor fixo $Q$ se $S_T \ge K$ e $0$ se $S_T < K$.
*   **Asset-or-Nothing Call**: Paga o valor do próprio ativo $S_T$ se $S_T \ge K$ e $0$ se $S_T < K$.

### Opções Cliquet (Ratchet)
Compostas por uma série de opções de curto prazo com redefinição periódica de *strike* (*reset*). O rendimento total é a soma dos retornos limitados (*capped*) de cada subintervalo $t_{i-1}$ para $t_i$:

$$\text{Payoff} = \sum_{i=1}^N \max \left( \min \left( \frac{S_{t_i} - S_{t_{i-1}}}{S_{t_{i-1}}}, C \right), F \right)$$

Onde $C$ é o teto (*cap*) e $F$ é o piso (*floor*) local.

### Notas Autopagáveis (Worst-of Autocallables)
Produtos estruturados vinculados a uma cesta de $d$ ativos subjacentes $S^1, \dots, S^d$. Em datas de observação periódicas $t_1, \dots, t_K$:
1. **Redenção Antecipada**: Se o desempenho do pior ativo da cesta $W_t = \min_{1 \le j \le d} \left( \frac{S_t^j}{S_0^j} \right)$ for maior ou igual ao nível de *Autocall* (ex.: $100\%$), a nota é cancelada e paga o principal mais um cupom acumulado.
2. **Proteção de Capital / Baixa**: No vencimento $T$, se não houve retenção antecipada e $W_T$ estiver acima da barreira de proteção de capital (ex.: $60\%$), o investidor recebe o principal. Se $W_T < 60\%$, o investidor sofre a perda do pior ativo, recebendo a performance $W_T$.

---

## 6. Dependência de Trajetória, Monitoramento Discreto e Correção de Broadie-Glasserman-Kou

### A Incompatibilidade entre Monitoramento Discreto e Contínuo
As fórmulas analíticas clássicas de precificação de opções de barreira (Merton, Rubinstein & Reiner) assumem monitoramento contínuo do ativo subjacente ($\tau_H = \inf\{t > 0 : S_t = H\}$). Contudo, na prática do mercado financeiro, as barreiras de contratos realistas são verificadas apenas em instantes discretos de tempo $t_i = i \Delta t$, com $i = 0, 1, \dots, m$ (por exemplo, preços de fechamento diários, onde $\Delta t = T/m$).

Como a trajetória contínua pode cruzar a barreira entre as datas de amostragem e retornar sem ser detectada na observação discreta, o preço de uma opção de barreira com monitoramento discreto difere significativamente do valor contínuo.

```
Preço Ativo (S)
   │                       / Trajetória Contínua (Cruza Barreira)
   │      /\              /
Barreira H ───/──\───────────/──────
   │    /    \          /  <-- Ponto discreto não detecta cruzamento!
   │   /      \  x     /
   │  x        \      x
   └───────────────────────── Tempo (t)
     t_1       t_2   t_3  (Instantes de Monitoramento Discreto)
```

### O Teorema de Correção de Continuidade (Broadie-Glasserman-Kou)
Broadie, Glasserman e Kou (1997) demonstraram que a aplicação direta da fórmula de precificação contínua gera um erro de ordem $O(1/\sqrt{m})$. Para corrigir esse viés sem recorrer a simulações de malha fina computacionalmente proibitivas, provaram o seguinte resultado:

#### Teorema (BGK)
Seja $V_m(H)$ o preço de uma opção de barreira com monitoramento discreto em $m$ pontos de amostragem e barreira nominal $H$. Seja $V(H)$ a fórmula de precificação analítica contínua para a mesma opção. Então:

$$V_m(H) = V \left( H e^{\pm \beta \sigma \sqrt{T/m}} \right) + o \left( \frac{1}{\sqrt{m}} \right)$$

Onde:
*   O sinal $+$ aplica-se se $H > S_0$ (opções *up*)
*   O sinal $-$ aplica-se se $H < S_0$ (opções *down*)
*   $\sigma$ é a volatilidade do ativo subjacente
*   $\beta = -\frac{\zeta(1/2)}{\sqrt{2\pi}} \approx 0.5826$, onde $\zeta(\cdot)$ é a função Zeta de Riemann.

### Fundamentação Teórica da Constante $\beta$ e Excesso da Caminhada Aleatória
O resultado baseia-se na teoria de renovação e na probabilidade de travessia de nível para caminhadas aleatórias. Sob a transformação logarítmica $W_n = \sum_{i=1}^n Z_i$, a condição de cruzamento discreto exige determinar a distribuição do excesso de nível (*overshoot*) $R_m = \tilde{W}_{\tilde{\tau}} - b \sqrt{m}$ no primeiro momento $\tilde{\tau}$ em que o limite é ultrapassado.

Siegmund (1985) provou que a esperança assintótica do excesso de uma caminhada aleatória gaussiana converge rigorosamente para a constante:

$$E[R_m] \xrightarrow{m \to \infty} \beta = -\frac{\zeta(1/2)}{\sqrt{2\pi}} \approx 0.5826$$

A barreira deslocada $H_{adj} = H e^{\beta \sigma \sqrt{\Delta t}}$ compensa exatamente o valor esperado desse *overshoot* contínuo não observado entre os instantes discretos.

### Exemplo Numérico Concreto: Opção Down-and-Out Call
Considere uma opção *down-and-out call* com os seguintes parâmetros experimentais extraídos das fontes primárias:
*   Preço Inicial $S_0 = 100$
*   Preço de Exercício $K = 100$
*   Volatilidade $\sigma = 0.30$ ($30\%$ ao ano)
*   Taxa livre de risco $r = 0.10$ ($10\%$ ao ano)
*   Maturidade $T = 0.2$ anos (aproximadamente 50 dias úteis)
*   Número de pontos de monitoramento $m = 50$ ($\Delta t = 0.2/50 = 0.004$, amostragem diária)

Tabela comparativa dos preços obtidos para variadas barreiras $H$:

| Barreira ($H$) | Preço Contínuo $V(H)$ | Preço Corrigido BGK $V(H_{adj})$ | Valor Exato Discreto (Trinomial $m=50$) | Erro Relativo Contínuo vs. Exato | Erro Relativo BGK vs. Exato |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **85** | $6.308$ | $6.322$ | $6.322$ | $-0.22\%$ | $0.00\%$ |
| **90** | $5.977$ | $6.098$ | $6.098$ | $-1.98\%$ | $0.00\%$ |
| **93** | $5.277$ | $5.585$ | $5.584$ | $-5.50\%$ | $+0.01\%$ |
| **95** | $4.398$ | $4.907$ | $4.907$ | $-10.37\%$ | $0.00\%$ |
| **97** | $3.060$ | $3.836$ | $3.834$ | $-20.19\%$ | $+0.05\%$ |
| **98** | $2.189$ | $3.121$ | $3.126$ | $-29.98\%$ | $-0.16\%$ |
| **99** | $1.171$ | $2.271$ | $2.337$ | $-49.89\%$ | $-2.82\%$ |

Análise dos resultados: Quando a barreira está próxima do spot ($H=97$), a fórmula contínua ($3.060$) subavalia a opção discreta diária ($3.834$) em mais de $20\%$, pois superestima o risco de invalidação (*knock-out*). A correção BGK reduz esse erro para apenas $+0.05\%$, operando em tempo de execução irrisório ($>10.000$ avaliações/segundo).

### Variantes de Barreiras Parciais
1. **Aproximação de Barreira Parcial Corrigida**: Utiliza a fórmula analítica de Heynen e Kat (1994) para barreiras ativas no intervalo $[t_1, T]$, ajustando o início do monitoramento para $t_1 = \Delta t$ e aplicando a barreira deslocada $H_{adj}$.
2. **Aproximação Parcial Modificada de Heurística**: Ajusta o início da janela de monitoramento contínuo para $t_1 = 0.58 \Delta t$, oferecendo um ponto intermediário de convergência quando $H \to S_0$.

---

## 7. Precificação por Monte Carlo, Redução de Variância e Cálculo de Gregas

### Precificação de Exercício Antecipado (Opções Americanas)
A precificação de opções americanas via Monte Carlo exige resolver a equação de programação dinâmica recursiva em tempo reverso para determinar o valor de continuação $C_{i-1}(s) = E [ V_i(S_{t_i}) | S_{t_{i-1}} = s ]$:

$$V_K(s) = \Phi(s), \quad V_{i-1}(s) = \max \left( \Phi(s), C_{i-1}(s) \right)$$

#### Método da Árvore Aleatória (Broadie e Glasserman 1997)
Ramifica $m$ caminhos independentes a partir de cada nó. Produz dois estimadores assintoticamente não viesados: um estimador viesado para cima $\tilde{V}$ (que reutiliza os mesmos caminhos futuros para estimar o valor de continuação e decidir a parada) e um estimador viesado para baixo $\tilde{v}$ (que separa o conjunto de ramificações para decisão e estimativa). Cresce exponencialmente $O(m^K)$, limitando seu uso a baixas dimensões.

#### Método da Malha Estocástica (*Stochastic Mesh* - Broadie e Glasserman 2004)
Gera $m$ caminhos independentes para todo o horizonte e conecta todos os nós do tempo $t_i$ a todos os nós do tempo $t_{i+1}$ utilizando pesos de densidade condicional:

$$w_{j, k}^{t_i} = \frac{f_i(S_{t_{i+1}}^k ; S_{t_i}^j)}{g_{i+1}(S_{t_{i+1}}^k)}$$

Onde $f_i(\cdot; x)$ é a densidade condicional do estado e $g_{i+1}$ é a densidade marginal da malha. O método escala em $O(K m^2)$, permitindo precificar opções americanas de alta dimensão.

#### Abordagem de Dualidade (Rogers 2002, Haugh e Kogan 2004)
Baseia-se na Decomposição de Doob-Meyer de supermartingais ($V_i = M_i^* + D_i$, onde $M^*$ é um martingal e $D$ é um processo decrescente). Formula o preço do americano como um problema de minimização de limite superior (*upper bound*):

$$V_0(s) = \inf_{M \in \mathcal{M}} E \left[ \max_{0 \le i \le K} \left( \Phi(S_{t_i}) - M_{t_i} \right) \middle| S_0 = s \right]$$

Onde $\mathcal{M}$ é o espaço de martingais com $M_0 = 0$. O limite exato é atingido no martingal ótimo $M_{t_i}^* = \sum_{j=1}^i \{ V_j(S_{t_j}) - E[V_j(S_{t_j}) | S_{t_{j-1}}] \}$. Jamshidian (2003) expandiu a teoria para a forma de dualidade multiplicativa.

### Variáveis de Controle e Redução de Variância para VaR
Para calcular o risco de cauda $P(L > x)$ de uma carteira com perdas $L = -\Delta V$, utiliza-se a aproximação Delta-Gamma da perda $Q \approx L$:

$$Q = a + \mathbf{b}^T \mathbf{Z} + \mathbf{Z}^T \mathbf{\Lambda} \mathbf{Z} = a + \sum_{j=1}^m \left( b_j Z_j + \lambda_j Z_j^2 \right)$$

Aplica-se Amostragem por Importância (*Importance Sampling* - IS) via torção exponencial (*exponential twisting*) sob a geradora de cumulantes $\psi(\theta) = \ln E[e^{\theta Q}]$. A nova medida de probabilidade $P_{\theta^*}$ desloca a média e a variância dos fatores normais $\mathbf{Z}$:

$$\mu_j(\theta^*) = \frac{\theta^* b_j}{1 - 2 \lambda_j \theta^*}, \quad \sigma_j^2(\theta^*) = \frac{1}{1 - 2 \lambda_j \theta^*}$$

Onde $\theta^*$ satisfaz $E_{\theta^*}(Q) = x$, transformando a região de perda rara $x$ no centro da amostragem e reduzindo drasticamente a variância do estimador.

### Métodos Computacionais para Cálculo de Gregas

```
                            ┌─ Finite Differences (Bumping) ── O(n) reavaliações, erro de truncamento vs. cancelamento
                            │
                            ├─ Pathwise Sensitivity (IPA) ───── Diferencia a trajetória. Exige continuidade de Lipschitz
                            │
Métodos de Cálculo ─────────┼─ Likelihood Ratio (LRM) ───────── Diferencia a densidade p(s). Funciona para saltos, alta variância
de Gregas (Monte Carlo)     │
                            ├─ Cálculo de Malliavin ────────── Integração por partes no espaço de Wiener
                            │
                            └─ AAD (Modo Reverso) ───────────── Varredura reversa no grafo do programa. Custo O(1)
```

#### 1. Diferenças Finitas (*Bumping*)
Aproxima a derivada via choque de parâmetro:

$$\frac{\partial V}{\partial \theta} \approx \frac{V(\theta + h) - V(\theta - h)}{2 h}$$

*   **Problema Estrutural**: Conflito entre erro de truncamento $O(h^2)$ e erro de arredondamento/cancelamento numérico $\frac{\epsilon |V|}{2 h}$ em ponto flutuante ($10^{-16}$). Produz um comportamento em curva em "U". Para $n$ entradas, custa $2n$ execuções de Monte Carlo.

#### 2. Derivada Caminho a Caminho (*Pathwise / IPA*)
Comuta a derivada com a integral de expectativa:

$$\frac{d}{d \theta} E[\Phi(S(\theta))] = E \left[ \frac{d \Phi}{d S} \cdot \frac{d S(\theta)}{d \theta} \right]$$

*   Exige que a função de *payoff* $\Phi$ seja contínua de Lipschitz. Falha para opções digitais ou de barreira dura, onde $\frac{d \Phi}{d S} = 0$ em quase todos os pontos e indefinido na descontinuidade.

#### 3. Método da Razão de Verossimilhança (*Likelihood Ratio Method* - LRM)
Transfere o operador de diferenciação para a função de densidade de probabilidade $g(s; \theta)$:

$$\frac{d}{d \theta} E[\Phi(S)] = \int \Phi(s) \frac{\partial g(s; \theta)}{\partial \theta} d s = E \left[ \Phi(S) \frac{\partial \ln g(S; \theta)}{\partial \theta} \right]$$

*   Aplica-se a qualquer *payoff* descontínuo, mas apresenta variância mais elevada que o método *pathwise*. Chen e Glasserman (2007b) demonstraram que a aplicação da LRM sobre a densidade discreta de Euler converge sem necessidade do maquinário abstrato de Malliavin.

#### 4. Diferenciação Algorítmica Adjunta (AAD)
A AAD decompõe a execução da precificação em um Grafo Acíclico Dirigido (DAG) de operações elementares $v_i = \phi_i(v_{parents(i)})$.

*   **Algoritmo Reverso**: Para calcular a sensibilidade da saída $y$ em relação a todas as variáveis intermediárias e entradas $x_i$, define-se a variável adjunta $\bar{v}_i = \frac{\partial y}{\partial v_i}$.
*   A acumulação reversa satisfaz a recorrência:

$$\bar{v}_j = \sum_{i \in children(j)} \bar{v}_i \frac{\partial v_i}{\partial v_j}$$

*   **Teorema do Custo do Adjunto**: O custo de tempo para calcular o gradiente completo de uma função $f: \mathbb{R}^n \to \mathbb{R}$ via modo reverso satisfaz stritamente:

$$\text{Tempo}(\text{Gradiente}) \le C \cdot \text{Tempo}(\text{Avaliação Direta})$$

Onde $C \in$, totalmente independente do número de entradas $n$.

##### fita (*Tape*) e *Checkpointing*
A varredura reversa requer o armazenamento das derivadas parciais de cada nó intermediário na "fita" (*tape*). Em simulações de Monte Carlo longas, a memória da fita cresce em $O(N_{caminhos} \times N_{passos})$. Para mitigar isso, aplica-se a técnica de *checkpointing*, salvando apenas estados do gerador de aleatórios em blocos periódicos e reavaliando os trechos locais no momento da varredura reversa.

##### Gregas de Segunda Ordem por Forward-over-Reverse
A matriz Hessian completa (Gamma, Volga, Vanna) é calculada combinando uma passagem no modo direto (*forward*) sobre o motor adjunto reverso já compilado (*Forward-over-Reverse*).

##### Diferenciação do Processo de Calibração
A conversão de *Model Greeks* (derivadas em relação a parâmetros internos $\theta$, como volatilidade local $V(S,t)$) para *Market Greeks* (derivadas em relação aos preços das opções vanila líquidas $C_i$ negociadas na bolsa) é realizada sem refazer a calibração por *bumping*, aplicando o Teorema da Função Implícita no sistema de calibração $F(\theta, C) = 0$:

$$\frac{\partial \theta}{\partial C} = -\left( \frac{\partial F}{\partial \theta} \right)^{-1} \frac{\partial F}{\partial C}$$

---

## 8. Quando o Payoff Exige Modelo Além de Vanila

O modelo do Movimento Browniano Geométrico com volatilidade constante não captura fatos estilizados empíricos do mercado, tais como o *skew* e o *smile* de volatilidade implícita, nem a ocorrência de saltos descontínuos nos preços.

```
Modelos de Precificação ───┬─ Volatilidade Local (Dupire) ────── σ(t, S_t) determina a superfície dinâmica de vol
                           │
                           ├─ Volatilidade Estocástica (Heston) ─ dV_t = κ(θ - V_t)dt + ξ √V_t dW_t (Variância como SDE)
                           │
                           └─ Modelos de Saltos (Merton/Lévy) ── Retornos gaussianos + Saltos Poissonianos
```

### Limitações do GBM
1. **Incapacidade de reproduzir o Smile/Skew**: O GBM prevê uma distribuição log-normal estrita no vencimento. O mercado precifica opções fora-do-preço (*OTM*) com volatilidades implícitas superiores, indicando caudas mais pesadas.
2. **Incompatibilidade para Opções Dependentes de Trajetória**: Duas dinâmicas podem ser calibradas para reproduzir os mesmos preços de opções europeias vanila no vencimento, mas fornecer preços e Gregas drasticamente divergentes para opções de barreira ou *cliquets*, devido a diferenças na volatilidade futura esperada condicional (*forward volatility*).

### Volatilidade Local (Dupire 1996)
Assume que a volatilidade é uma função determinística do tempo e do preço spot instantâneo $\sigma(t, S_t)$.
*   A equação de Dupire extrai a volatilidade local exata a partir da superfície de preços de opções vanila $C(K, T)$:

$$\sigma_{local}^2(T, K) = \frac{\frac{\partial C}{\partial T} + r K \frac{\partial C}{\partial K}}{\frac{1}{2} K^2 \frac{\partial^2 C}{\partial K^2}}$$

*   *Limitação*: Faz a volatilidade implícita mover-se em sincronia estrita com o preço do ativo subjacente, o que nem sempre reflete a dinâmica de volatilidade estocástica real do mercado.

### Volatilidade Estocástica (Exemplo: Modelo de Heston 1993)
Trata a variância instantânea $v_t$ como um segundo processo estocástico correlacionado:

$$d S_t = r S_t d t + \sqrt{v_t} S_t d W_t^S$$

$$d v_t = \kappa (\theta - v_t) d t + \xi \sqrt{v_t} d W_t^v$$

$$d \langle W^S, W^v \rangle_t = \rho d t$$

*   Captura o dinamismo temporal do *skew* via correlação $\rho$ e o nível de *smile* através da volatilidade da volatilidade $\xi$.

### Modelos de Saltos e Processos de Lévy (Merton 1976)
Adicionam um processo de Poisson composto para capturar movimentações descontínuas extremas no mercado:

$$\frac{d S_t}{S_{t-}} = (r - \lambda k) d t + \sigma d W_t + (Y_t - 1) d N_t$$

Onde $N_t$ é um processo de Poisson com intensidade de salto $\lambda$, e $Y_t$ é a distribuição da magnitude do salto log-normal. É essencial para precificar derivativos de curto prazo expostos a risco de liquidez ou descontinuidade de mercado.

---

## 9. Implementação em Python e Checklist

### Código Python: Precificação de Opção de Barreira Discreta com Correção BGK e Gregas via Pathwise vs. Bumping

```python
import numpy as np
from scipy.stats import norm

def bs_call_price(S, K, r, sigma, T):
    """Preco de Call Europeia via Black-Scholes."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def bgk_adjusted_barrier(H, S0, sigma, T, m):
    """Calcula a barreira deslocada de Broadie-Glasserman-Kou (BGK)."""
    dt = T / m
    beta = 0.5826
    # Se H < S0 (Down option), aplica sinal negativo e^(-beta * sigma * sqrt(dt))
    # Se H > S0 (Up option), aplica sinal positivo e^(+beta * sigma * sqrt(dt))
    direction = -1.0 if H < S0 else 1.0
    return H * np.exp(direction * beta * sigma * np.sqrt(dt))

def monte_carlo_pathwise_delta(S0, K, r, sigma, T, N_paths):
    """
    Precificacao de Call Europeia via Monte Carlo Exact GBM
    e calculo do Delta via Pathwise Sensitivity (IPA).
    """
    np.random.seed(42)
    Z = np.random.standard_normal(N_paths)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    
    # Payoff
    payoff = np.maximum(ST - K, 0.0)
    price = np.exp(-r * T) * np.mean(payoff)
    
    # Pathwise Delta: d(Payoff)/dS0 = (ST/S0) * I(ST > K)
    payoff_grad = (ST / S0) * (ST > K)
    delta_pathwise = np.exp(-r * T) * np.mean(payoff_grad)
    
    # Standard Error do Preco
    se_price = np.exp(-r * T) * np.std(payoff) / np.sqrt(N_paths)
    
    return price, delta_pathwise, se_price

def monte_carlo_bumping_delta(S0, K, r, sigma, T, N_paths, h=1e-4):
    """Calculo do Delta via Bumping (Diferenca Finita Central)."""
    # Executa duas simulacoes independentes (ou com MCRN) deslocando S0
    np.random.seed(42)
    Z = np.random.standard_normal(N_paths)
    
    ST_up = (S0 + h) * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    payoff_up = np.maximum(ST_up - K, 0.0)
    price_up = np.exp(-r * T) * np.mean(payoff_up)
    
    ST_dn = (S0 - h) * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    payoff_dn = np.maximum(ST_dn - K, 0.0)
    price_dn = np.exp(-r * T) * np.mean(payoff_dn)
    
    delta_bumping = (price_up - price_dn) / (2.0 * h)
    return delta_bumping

if __name__ == "__main__":
    # Parametros do Teste Numérico de Barreira (Tabela Broadie-Glasserman-Kou)
    S0, K, r, sigma, T = 100.0, 100.0, 0.10, 0.30, 0.2
    H = 97.0
    m = 50  # 50 monitoramentos discretos
    
    # Barreira Corrigida por BGK
    H_adj = bgk_adjusted_barrier(H, S0, sigma, T, m)
    print(f"--- CORRECAO DE BARREIRA BGK ---")
    print(f"Barreira Nominal H: {H}")
    print(f"Barreira Ajustada BGK H_adj: {H_adj:.4f}")
    
    # Teste de Monte Carlo e Pathwise Delta vs Bumping
    N_sims = 1000000
    price_mc, delta_pw, se = monte_carlo_pathwise_delta(S0, K, r, sigma, T, N_sims)
    delta_bump = monte_carlo_bumping_delta(S0, K, r, sigma, T, N_sims, h=1e-3)
    
    # Comparacao Analitica BS
    price_bs = bs_call_price(S0, K, r, sigma, T)
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta_bs = norm.cdf(d1)
    
    print(f"\n--- COMPARATIVO DE PRECIFICAÇÃO E GREGAS ---")
    print(f"Preco Analitico BS: {price_bs:.5f}")
    print(f"Preco Monte Carlo:  {price_mc:.5f} (SE: {se:.5f})")
    print(f"Delta Analitico BS: {delta_bs:.5f}")
    print(f"Delta Pathwise (IPA): {delta_pw:.5f}")
    print(f"Delta Bumping Central: {delta_bump:.5f}")
```

### Checklist de Verificação e Validação para Engenharia Financeira

- [ ] **Sementes e Gerador Aleatório**: A semente do gerador de números aleatórios está fixada e documentada para permitir reprodução auditável?
- [ ] **Aproximação de Barreira Discreta**: Em opções com observação discreta de barreira, a correção de continuidade $H_{adj} = H e^{\pm \beta \sigma \sqrt{\Delta t}}$ foi aplicada antes de utilizar solvers contínuos?
- [ ] **Verificação de Suavidade para IPA**: O *payoff* do derivativo atende à condição de continuidade de Lipschitz? Se contiver descontinuidades (digitais/barreiras duras), utilizou-se LRM ou técnicas de suavização de *payoff*?
- [ ] **Escolha do Passo de Discretização $h$ no Bumping**: Caso utilize diferenças finitas, o tamanho do passo $h$ foi otimizado para evitar a dominância do erro de cancelamento numérico em precisão dupla ($10^{-16}$)?
- [ ] **Amostras Antitéticas / Variáveis de Controle**: Implementou-se técnicas de redução de variância para garantir convergência dentro da tolerância do Erro Padrão?
- [ ] **Gestão de Memória da Fita AAD**: Em motores AAD, adotou-se o uso de *checkpointing* nos ciclos de simulação de Monte Carlo para evitar o estouro da memória RAM?
- [ ] **Teste de Invariância por Rotação**: Em precificações multiativos (*worst-of*), a matriz de covariância utilizada na decomposição de Cholesky é estritamente definida positiva?

---

## 10. Tabela Comparativa e Glossário

### Tabela Comparativa de Métodos do Módulo M02

| Método / Algoritmo | Ordem de Convergência / Custo | Principais Vantagens | Principais Limitações / Desvantagens | Cenário de Uso Recomendado |
| :--- | :--- | :--- | :--- | :--- |
| **Euler-Maruyama** | Fraca: $O(h)$<br>Forte: $O(h^{0.5})$ | Simplicidade de implementação em SDEs não lineares. | Alto erro de discretização temporal em passos largos. | SDEs genéricas sem solução analítica fechada. |
| **Milstein** | Fraca: $O(h^2)$<br>Forte: $O(h)$ | Maior precisão e menor viés temporal que Euler. | Requer cálculo de derivadas parciais do coeficiente de volatilidade e simulação de integrais estocásticas duplas. | Difusões não lineares unidimensionais. |
| **Simulação Exata (Beskos)** | Erro temporal $0$ | Elimina completamente o erro de discretização temporal. | Computacionalmente intensivo; requer condição de comutatividade em dimensões elevadas. | Validação de benchmarks e SDEs unidimensionais complexas. |
| **Correção BGK** | Reduz erro de $O(m^{-0.5})$ para $o(m^{-0.5})$ | Extremamente rápida; ajusta fórmulas contínuas analíticas para monitoramento discreto. | Válida para barreiras simples; perde precisão no limite extremo $H \to S_0$. | Precificação de opções de barreira operadas no mercado OTC com leitura diária. |
| **Bumping (Diferenças Finitas)** | Custo: $O(n \cdot N_{paths})$ | Funciona como uma "caixa preta" sem necessidade de acessar o código interno. | Lentidão extrema; sofre com o erro de cancelamento em ponto flutuante; não escala para matrizes Hessianas. | Verificação pontual e validação cruzada de modelos pequenos. |
| **Pathwise Sensitivity (IPA)** | Custo: $O(N_{paths})$ | Baixa variância; cálculo das Gregas em uma única passagem direta do Monte Carlo. | Exige *payoffs* contínuos (condição de Lipschitz); falha em opções binárias/digitais. | Opções vanila, asiáticas e estruturas com *payoffs* suaves. |
| **Likelihood Ratio (LRM)** | Custo: $O(N_{paths})$ | Funciona para qualquer *payoff* descontínuo ou com degrau. | Apresenta variância mais elevada que o método *pathwise*. | Opções digitais, barreiras rígidas sem suavização e binárias. |
| **AAD Modo Reverso** | Custo: $O(1) \cdot N_{paths}$ | Calcula o gradiente em relação a centenas de entradas a um custo fixo pequeno ($3\times$ a $5\times$ o preço). | Exige rearquitetura do motor de precificação e gerenciamento intensivo de memória da fita. | Livros complexos de exóticas (*autocallables*), gestão de risco intradia e cálculo de matrizes de risco. |

### Glossário de Termos Técnicos

*   **Amostragem por Aceitação-Rejeição (Acceptance-Rejection Sampling - ARS)**: Técnica de simulação Monte Carlo que gera amostras de uma distribuição-alvo complexa aceitando ou rejeitando candidatas produzidas por uma distribuição proposição simples, com base na razão de suas densidades.
*   **Amostragem por Importância (Importance Sampling - IS)**: Técnica de redução de variância que altera a medida de probabilidade sob a qual as simulações são geradas, concentrando a amostragem em regiões do espaço amostral de maior interesse ou impacto (como as caudas de perda em VaR).
*   **Diferenciação Algorítmica Adjunta (AAD)**: Método computacional que aplica a regra da cadeia do cálculo de forma exata sobre o grafo de instruções de um programa de computador, permitindo calcular derivadas de ordens arbitrárias com precisão de máquina.
*   **Encurtamento Estocástico (Stochastic Thinning)**: Algoritmo utilizado em processos de Poisson não homogêneos que aceita eventos aleatórios gerados por um processo homogêneo dominante com probabilidade proporcional à razão das intensidades instantâneas.
*   **Excesso de Nível (Overshoot)**: A quantidade positiva pela qual um processo estocástico discretizado ou caminhada aleatória ultrapassa um limite ou barreira fixa no momento exato em que o cruzamento é detectado.
*   **Infinitesimal Perturbation Analysis (IPA)**: Denominação formal na literatura de simulação estocástica para o método de sensibilidade caminho a caminho (*pathwise*), que calcula derivadas diferenciando as trajetórias simuladas.
*   **Malha Estocástica (Stochastic Mesh)**: Algoritmo de Monte Carlo para precificação de opções americanas de alta dimensão que substitui o crescimento exponencial de árvores por uma rede densa onde todos os nós do tempo $t_i$ se conectam a todos os nós do tempo $t_{i+1}$ via pesos de densidade.
*   **Ponte Browniana (Brownian Bridge)**: Processo estocástico gaussiano cuja distribuição é condicionada aos valores do processo em ambos os extremos do intervalo de tempo (início e fim).
*   **Supermartingal**: Processo estocástico para o qual a expectativa condicional do valor futuro é menor ou igual ao valor atual presente. Na precificação de opções americanas, o valor da opção ao longo do tempo forma um supermartingal devido à opção de exercício antecipado.
*   **Torção Exponencial (Exponential Twisting)**: Família parametrizada de transformações de medida de probabilidade que desloca a média de uma distribuição adicionando um fator proporcional a $e^{\theta Q}$, utilizada na amostragem por importância para eventos de cauda.
*   **Value-at-Risk (VaR)**: Métrica estatística de gestão de risco que quantifica a perda máxima esperada de uma carteira de investimentos dentro de um horizonte temporal definido, a um nível de confiança estatística especificado.
*   **Volatilidade Local**: Modelo no qual a volatilidade do ativo subjacente é tratada como uma função determinística não constante dependente do nível do preço spot instantâneo e do tempo, $\sigma(t, S_t)$, desenhada para reproduzir exatamente a superfície de volatilidade implícita do mercado.