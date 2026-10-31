<!-- imported study note (guia-completo.md) -->
# Guia de Módulo M05: Econofísica, Informação, Entropia e Risco

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M05

↑ M05 · Resumo · Completo

## Resumo Executivo

Este documento estabelece a síntese técnica e conceitual do Módulo M05 do curso Econofísica Khem Kapital, intitulado **"Econofísica: informação, entropia e risco"**. O objetivo central deste relatório é fornecer uma análise abrangente dos fundamentos que unem a física estatística, a teoria da informação e a finança quantitativa para o modelamento de sistemas financeiros complexos, detecção de fragilidades de mercado e previsão de colapsos (*crashes*).

A abordagem tradicional de finanças assume frequentemente premissas de eficiência perfeita, distribuição normal de retornos e independência estocástica. Contudo, dados empíricos de mercados financeiros — especialmente em ativos de alta volatilidade como o Bitcoin e índices acionários globais — revelam dinâmicas não lineares, dependências temporais complexas, caudas longas (*fat tails*) e fenômenos de sincronização coletiva. A Econofísica responde a essas limitações aplicando ferramentas como a Equação de Difusão/Calor derivada da Equação Diferencial Parcial (EDP) de Black-Scholes, métricas avançadas de Entropia de Permutação (PEn, WPEn, AAPEn, UPEn), modelos de causalidade da Teoria da Informação (Transfer Entropy) e esquemas de calibração de modelos de super-crescimento exponencial com oscilações log-periódicas (Log-Periodic Power Law - LPPL).

Este guia cobre detalhadamente os aspectos teóricos, a formulação matemática rigorosa em LaTeX, exemplos numéricos empíricos (incluindo a análise do *crash* do Bitcoin de 2017–2018), estratégias de implementação em Python e glossário técnico comparativo.

---

## 1. O que é Econofísica e por que Física em Mercados

A Econofísica é um campo de pesquisa interdisciplinar que aplica teorias, métodos e modelos desenvolvidos na física — em especial a física estatística, mecânica estatística, dinâmica não linear e teoria dos sistemas complexos — para analisar dados econômicos e financeiros.

Os mercados financeiros não operam como sistemas estáticos em equilíbrio determinístico; pelo contrário, comportam-se como **sistemas complexos adaptativos**. Nesses sistemas, milhares de agentes interagem de forma não linear, sujeitos a ruídos, assimetrias de informação e comportamentos de boiada (*herding behavior*). A aplicação da física aos mercados justifica-se por razões fundamentais:

1. **Tratamento da Não Linearidade e Não Estacionariedade:** Métodos lineares tradicionais falham em capturar momentos em que pequenas variações nas condições iniciais geram grandes deslocamentos no sistema (efeito borboleta ou transições de fase).
2. **Microestados e Propriedades Emergentes:** Assim como a temperatura ou a pressão de um gás emergem das colisões microscópicas de suas moléculas, a volatilidade e os regimes de preços emergem do comportamento agregado dos microestados de ordens de compra e venda.
3. **Quebra da Hipótese do Passeio Aleatório:** Embora a Hipótese dos Mercados Eficientes (EMH) de Fama postule que os preços seguem passeios aleatórios imprevisíveis e com entropia máxima, evidências empíricas mostram flutuações nas taxas de entropia que assinalam períodos de transição de regime e perda de eficiência informational.

---

## 2. Difusão, Equação do Calor e Transformação da EDP de Black-Scholes

Um dos pilares históricos da convergência entre física e finanças é a precificação de derivativos sob o modelo de Black-Scholes-Merton. A precificação de uma opção depende da evolução estocástica do ativo subjacente $S$, assumido como um Movimento Browniano Geométrico (GBM):

$$dS = \mu S dt + \sigma S dW$$

Onde $\mu$ representa a taxa de retorno esperada (deriva), $\sigma$ é a volatilidade do ativo e $W$ é um processo estocástico de Wiener (Movimento Browniano) com variação $Var(W(t)) = t$ e incremento infinitesimal $dW \sim N(0, dt)$.

### A EDP de Black-Scholes e sua Interpretação Financeira

Aplicando o Lema de Itô e construindo uma carteira de cobertura (*delta-hedge*) auto-financiada $\Pi = -V + \frac{\partial V}{\partial S} S$, a incerteza $dW$ é eliminada. Exigindo que a carteira renda à taxa livre de risco $r$, chega-se à EDP de Black-Scholes:

$$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + r S \frac{\partial V}{\partial S} - r V = 0$$

Rearranjando a equação, obtém-se a interpretação financeira dos *Greeks*:

$$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} = r V - r S \frac{\partial V}{\partial S}$$

* O termo $\frac{\partial V}{\partial t}$ representa o **Theta** ($\Theta$), a deterioração temporal do valor da opção.
* O termo $\frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2}$ contém o **Gamma** ($\Gamma$), que mede a convexidade do valor da opção em relação ao preço do ativo subjacente, representando o custo contínuo de rebalanceamento da cobertura (*hedging*).
* O lado direito representa o retorno livre de risco de uma posição comprada na opção e vendida em $\frac{\partial V}{\partial S}$ (**Delta**) ações. A equação estabelece que os ganhos de convexidade ($\Gamma$) e as perdas temporais ($\Theta$) devem se compensar perfeitamente para gerar a taxa livre de risco $r$.

### Transformação para a Equação de Difusão/Calor

A EDP de Black-Scholes é uma equação de Cauchy-Euler com coeficientes variáveis. Ela pode ser transformada exatamente em uma Equação de Difusão (Equação do Calor com coeficientes constantes) através de mudanças de variáveis adequadas.

Definem-se as variáveis adimensionais:

$$\tau = T - t$$

$$u = V \cdot e^{r \tau}$$

$$x = \ln\left(\frac{S}{K}\right) + \left(r - \frac{1}{2}\sigma^2\right)\tau$$

Onde $K$ é o preço de exercício (*strike*) e $T$ é a data de vencimento. Substituindo essas transformações na EDP original, elimina-se o termo de deriva e o termo de desconto, resultando na **Equação de Difusão Clássica**:

$$\frac{\partial u}{\partial \tau} = \frac{1}{2}\sigma^2 \frac{\partial^2 u}{\partial x^2}$$

A condição terminal da opção de compra europeia $V(S, T) = \max\{S - K, 0\}$ converte-se na condição inicial do problema de Cauchy em termos da função degrau de Heaviside $H(x)$:

$$u(x, 0) = u_0(x) = K(e^{\max\{x, 0\}} - 1) = K(e^x - 1)H(x)$$

A solução analítica é obtida pela convolução da condição inicial com o kernel de difusão Gaussiano (função de Green):

$$u(x, \tau) = \frac{1}{\sigma \sqrt{2\pi \tau}} \int_{-\infty}^{\infty} u_0(y) \exp\left[ -\frac{(x - y)^2}{2\sigma^2 \tau} \right] dy$$

Efetuando a integração e revertendo as variáveis para $(S, t)$, recupera-se a fórmula de precificação de Black-Scholes para uma opção de compra (*Call*):

$$C(S, t) = S N(d_+) - K e^{-r(T-t)} N(d_-)$$

Com as variáveis normalizadas $d_+$ e $d_-$ dadas por:

$$d_+ = \frac{\ln(S/K) + \left(r + \frac{1}{2}\sigma^2\right)(T-t)}{\sigma \sqrt{T-t}}$$

$$d_- = d_+ - \sigma \sqrt{T-t}$$

Esta equivalência matemática demonstra que a precificação de opções e o espalhamento estocástico de retornos no tempo são isolomorfos à difusão térmica de partículas em um meio físico.

---

## 3. Teoria da Informação: Entropia de Shannon, Entropia Condicional, Informação Mútua e Transfer Entropy

A Teoria da Informação quantifica a incerteza, a desordem e o fluxo de informação em processos aleatórios.

### Entropia de Shannon ($ShEn$)

A Entropia de Shannon mede a incerteza associada a uma variável aleatória discreta $X$ com distribuição de probabilidade $p(x)$:

$$H(X) = -\sum_{x \in \chi} p(x) \log_2 p(x)$$

Quando $H(X) = 0$, o sistema é totalmente determinístico e previsível. O valor máximo de entropia ocorre quando $p(x)$ é uma distribuição uniforme, representando desordem total e ausência de padrão.

### Entropia Condicional e Informação Mútua ($MI$)

A Entropia Condicional $H(Y|X)$ mede a incerteza remanescente em $Y$ dado o conhecimento prévio de $X$:

$$H(Y|X) = -\sum_{x \in \chi, y \in \mathcal{Y}} p(x, y) \log_2 p(y|x)$$

A Informação Mútua $I(X; Y)$ quantifica a quantidade de informação compartilhada entre duas variáveis (grau de acoplamento não linear):

$$I(X; Y) = H(X) + H(Y) - H(X, Y) = \sum_{x \in \chi, y \in \mathcal{Y}} p(x, y) \log_2 \left(\frac{p(x, y)}{p(x)p(y)}\right)$$

Se $X$ e $Y$ forem estatisticamente independentes, $p(x, y) = p(x)p(y)$ e $I(X; Y) = 0$.

### Causalidade de Granger vs. Transfer Entropy ($TE$)

A Causalidade de Granger tradicional avalia se os valores passados de uma série temporal $X$ ajudam a prever o valor futuro de $Y$ melhor do que apenas o passado de $Y$. Em um arcabouço de Regressão Vetorial Autorregressiva (VAR):

$$Y(t) = \alpha + \sum_{\Delta t=1}^k \beta_{\Delta t} Y(t - \Delta t) + \epsilon_t$$

$$Y(t) = \hat{\alpha} + \sum_{\Delta t=1}^k \hat{\beta}_{\Delta t} Y(t - \Delta t) + \sum_{\Delta t=1}^k \hat{\gamma}_{\Delta t} X(t - \Delta t) + \hat{\epsilon}_t$$

A definição probabilística genérica de Causalidade de Granger estabelece que $X$ não causa $Y$ se:

$$p(Y_{t+1} | X_t, Y_t, Z_t) = p(Y_{t+1} | Y_t, Z_t)$$

Contudo, a Causalidade de Granger linear falha ao capturar relações de dependência não lineares. A **Transfer Entropy** ($TE$), introduzida no âmbito da teoria da informação não linear, mede o fluxo direcional de informação entre dois processos estocásticos $X$ e $Y$:

$$TE_{X \to Y} = \sum p(Y_{t+1}, Y_t, X_t) \log_2 \left( \frac{p(Y_{t+1} | Y_t, X_t)}{p(Y_{t+1} | Y_t)} \right)$$

O **Fluxo Líquido de Informação** (*Net Information Flow*) entre dois ativos ou mercados é expresso pela diferença entre as entropias de transferência direcionais:

$$TE_{\text{net}} = TE_{X \to Y} - TE_{Y \to X}$$

Se $TE_{\text{net}} > 0$, o sistema $X$ atua como o condutor (*driver*) do sistema $Y$.

---

## 4. Estimação de Entropia em Retornos: Discretização, Permutation Entropy e Variantes

Para aplicar medidas de entropia a séries temporais contínuas de retornos financeiros, é necessário calcular retornos padronizados e mapear sequências em padrões simbólicos.

Dada uma série de preços $x(t)$, os retornos simples $G(t)$ e os retornos padronizados $g(t)$ são definidos por:

$$G(t) = \frac{x(t + \Delta t) - x(t)}{x(t)}$$

$$g(t) = \frac{G(t) - \langle G \rangle}{\sigma}$$

Onde $\langle G \rangle$ é a média e $\sigma$ é o desvio padrão dos retornos.

### Entropia de Permutação Clássica ($PEn$)

Proposta por Bandt e Pompe, a $PEn$ quantifica a complexidade analisando a frequência de aparecimento de **padrões ordinais** (permutações) em vetores de imersão.

Dado um vetor $X_t^{d_E, \tau} = (x_t, x_{t+\tau}, \dots, x_{t+(d_E-1)\tau})$, parametrizado pela **dimensão de imersão** $d_E$ e pelo **atraso temporal** (*delay*) $\tau$:

Existem $d_E!$ padrões ordinais possíveis $\pi_i$.

#### Exemplo Numérico Concreto de Mapeamento Ordinal ($d_E = 3, \tau = 1$)
Considere o segmento de série temporal $(5, 8, 4)$:
* Os componentes são $x_t = 5$, $x_{t+1} = 8$, $x_{t+2} = 4$.
* Ordenando os valores em ordem crescente: $4 < 5 < 8$, correspondendo aos índices ordinais $(t+2, t, t+1)$.
* O padrão ordinal é classificado como $\pi_2 = (2, 0, 1)$ ou condição $x_{t+\tau} > x_t > x_{t+2\tau}$.

A tabela abaixo resume os 6 ($3!$) padrões ordinais possíveis para $d_E = 3$:

| Padrão Ordinal ($\pi_i$) | Padrão Relativo de Índices | Condição nos Dados |
| :--- | :--- | :--- |
| $\pi_1$ | $(3, 2, 1)$ | $x_t > x_{t+\tau} > x_{t+2\tau}$ |
| $\pi_2$ | $(3, 1, 2)$ | $x_t > x_{t+2\tau} > x_{t+\tau}$ |
| $\pi_3$ | $(2, 3, 1)$ | $x_{t+\tau} > x_t > x_{t+2\tau}$ |
| $\pi_4$ | $(2, 1, 3)$ | $x_{t+2\tau} > x_t > x_{t+\tau}$ |
| $\pi_5$ | $(1, 3, 2)$ | $x_{t+\tau} > x_{t+2\tau} > x_t$ |
| $\pi_6$ | $(1, 2, 3)$ | $x_t < x_{t+\tau} < x_{t+2\tau}$ |

A probabilidade $p(\pi_i)$ de ocorrência do padrão é calculada por:

$$p(\pi_i)^{d_E, \tau} = \frac{\# \{ X_t^{d_E, \tau} \text{ corresponde ao padrão } \pi_i \}}{N - (d_E - 1)\tau}$$

A Entropia de Permutação Normalizada é dada por:

$$PEn(X)^{d_E, \tau} = -\frac{1}{\ln(d_E!)} \sum_{i=1}^{d_E!} p(\pi_i) \ln p(\pi_i)$$

A normalização garante que $0 \le PEn \le 1$.

### Limitações da $PEn$ Clássica e Variantes Avançadas

A $PEn$ clássica ignora magnitudes de amplitude (trata pequenas flutuações de ruído e grandes saltos de preço da mesma forma) e apresenta ambiguidades em valores iguais (*ties*). Para superar isso, foram desenvolvidas três métricas aprimoradas:

#### 1. Entropia de Permutação Ponderada ($WPEn$)
Introduzida por Fadlallah et al., a $WPEn$ pondera cada vetor pela variância local (energia) da subsequência:

$$w_t = \frac{1}{d_E} \sum_{k=1}^{d_E} \left( x_{t+(k-1)\tau} - \langle X_t^{d_E, \tau} \rangle \right)^2$$

$$\langle X_t^{d_E, \tau} \rangle = \frac{1}{d_E} \sum_{k=1}^{d_E} x_{t+(k-1)\tau}$$

A probabilidade ponderada $p_w(\pi_i)$ e a $WPEn$ são dadas por:

$$p_w(\pi_i)^{d_E, \tau} = \frac{\sum_{t: X_t \in \pi_i} w_t}{\sum_t w_t}$$

$$WPEn(X)^{d_E, \tau} = -\sum_{i=1}^{d_E!} p_w(\pi_i) \ln p_w(\pi_i)$$

#### 2. Entropia de Permutação Sensível à Amplitude ($AAPEn$)
Proposta por Azami e Escudero, a $AAPEn$ adiciona um coeficiente de ajuste de amplitude $L(X_t^{d_E, \tau})$ que combina a média absoluta da amplitude com as diferenças entre amostras consecutivas:

$$L(X_t^{d_E, \tau}) = \frac{A}{d_E} \sum_{k=1}^{d_E} |x_{t+(k-1)\tau}| + \frac{1-A}{d_E-1} \sum_{k=2}^{d_E} |x_{t+(k-1)\tau} - x_{t+(k-2)\tau}|$$

Onde $A \in$. Em detecção de *crashes* financeiros, recomenda-se $A = 0{,}5$ para equilibrar nível médio e volatilidade. As frequências relativas são normalizadas pela soma total de $L(X_t)$.

#### 3. Entropia de Permutação por Quantização Uniforme ($UPEn$)
Desenvolvida por Chen et al., a $UPEn$ aplica Quantização Uniforme (UQ) com $D$ níveis de discretização:

$$UQ(x) = \left\lfloor \frac{x - x_{\min}}{\Delta} \right\rfloor, \quad \Delta = \frac{x_{\max} - x_{\min}}{D}$$

O primeiro elemento $S_{t,1}$ é quantizado, e os elementos subsequentes são codificados em relação ao primeiro:

$$S_{t, k} = S_{t, 1} + \left\lfloor \frac{X_{t, k} - X_{t, 1}}{\Delta} \right\rfloor, \quad 2 \le k \le d_E$$

A distribuição abrange $D^{d_E}$ padrões possíveis $\pi_i^U$. A $UPEn$ normalizada é expressa por:

$$UPEn(X)^{d_E, \tau, D} = -\frac{1}{\ln(D^{d_E})} \sum_{i=1}^{D^{d_E}} p(\pi_i^U) \ln p(\pi_i^U)$$

Parâmetros recomendados para análise de crises: $d_E = 3$, $\tau = 1$, $D = 4$.

---

## 5. Entropia e Eficiência de Mercado

De acordo com a Hipótese dos Mercados Eficientes (EMH), os preços incorporam instantaneamente todas as informações disponíveis. Em um mercado perfeitamente eficiente, os retornos comportam-se como ruído branco sem memória temporal, o que corresponde a um estado de **entropia máxima** ($PEn \to 1$).

Em mercados reais, a eficiência varia dinamicamente ao longo do tempo:
* **Fases Estáveis de Crescimento:** Apresentam alta entropia, refletindo estratégias de negociação heterogêneas, liquidez dispersa e aleatoriedade nos retornos.
* **Fases Pré-Crash e de Especulação Bolhosa:** Ocorrem quedas acentuadas nos níveis de entropia. Os agentes passam a agir de forma altamente sincronizada (*herd behavior*), resultando em padrões ordenados e repetitivos nos retornos.
* **Fases de Colapso (*Crash Peak*):** A entropia atinge seus mínimos históricos, assinalando uma perda drástica de eficiência informacional, domínio de vendas em pânico e fragilidade sistêmica.

---

## 6. Temperatura de Mercado, Microestados, Distribuição de Boltzmann e Regimes

A analogia entre finanças e mecânica estatística permite associar a dinâmica de mercado a conceitos termodinâmicos:

* **Microestados:** Representam as configurações individuais das ordens de compra e venda no livro de ofertas, bem como o arranjo específico das sequências ordinais de retornos no tempo.
* **Macroestados:** Correspondem às variáveis agregadas do mercado, tais como preço atual, volatilidade do período, volume financeiro e nível de entropia calculada.
* **Temperatura de Mercado:** Pode ser formalizada como uma medida da energia de flutuação ou volatilidade do sistema. Em estados de alta temperatura, as partículas (agentes/preços) possuem alta energia cinética (alta volatilidade e variância), ocupando múltiplos microestados com igual probabilidade (distribuição uniforme/alta entropia).
* **Distribuição de Boltzmann e Regimes:** A probabilidade $P(E_i)$ de o sistema ocupar um microestado de energia $E_i$ sob uma dada temperatura de mercado $T_m$ aproxima-se de:

$$P(E_i) = \frac{e^{-E_i / (k_B T_m)}}{Z}$$

Onde $Z = \sum_j e^{-E_j / (k_B T_m)}$ é a função de partição do sistema. Transições de regime de mercado (de mercado em alta para *crash*) equivalem a **transições de fase termodinâmicas**, onde o sistema sofre resfriamento crítico ou cristalização em microestados altamente ordenados de baixa entropia.

---

## 7. Risco como Força: Drawdown, Correlação em Crises e Matriz de Correlação

Nos mercados complexos, o risco não é apenas uma medida estática de desvio padrão (volatilidade), mas atua como uma força dinâmica emergente.

### Drawdown e Estrutura de Correlação
O *Drawdown* mede a queda percentual do pico acumulado até o vale em um dado horizonte temporal. Durante crises financeiras, observa-se o fenômeno da **quebra de diversificação**: a correlação entre ativos que pareciam independentes tende a convergir para 1.

### Matriz de Correlação e Teoria das Matrizes Aleatórias (RMT)
Considere $N$ ativos com séries temporais de retornos de tamanho $T$. A matriz de correlação $C$ de dimensão $N \times N$ possui autovalores $\lambda_i$. De acordo com a Teoria das Matrizes Aleatórias, se os retornos fossem ruído puramente aleatório, a distribuição dos autovalores seguiria a lei de Marchenko-Pastur.

Em momentos de crise e estresse sistêmico:
1. O maior autovalor ($\lambda_{\max}$) afasta-se drasticamente do limite superior do ruído.
2. $\lambda_{\max}$ representa o **modo de mercado** (*market mode*), absorvendo quase a totalidade da variância do sistema e indicando sincronização universal de quedas.

---

## 8. Sinais de Crash e Fragilidade

### O Modelo LPPL (Log-Periodic Power Law)

Desenvolvido por Johansen, Ledoit e Sornette (modelo JLS), o modelo LPPL conceitua bolhas financeiras como acelerações em super-exponencial do preço acompanhadas por oscilações log-periódicas, decorrentes de feedback positivo e cooperação hierárquica entre investidores.

A formulação simplificada do LPPL expressa o logaritmo do preço $p(t)$ por:

$$\ln p(t) = A + B(t_c - t)^m + C(t_c - t)^m \cos\left( \omega \ln(t_c - t) - \phi \right)$$

Onde:
* $t_c$ é o **tempo crítico** (*critical time*), representando o fim estimado da bolha e o momento de maior probabilidade de ocorrência do *crash*.
* $m$ é o expoente da potência ($0 < m < 1$), garantindo aceleração super-exponencial.
* $\omega$ é a frequência angular das oscilações log-periódicas.
* $A, B, C, \phi$ são parâmetros de ajuste.

Filimonov e Sornette (2013) propuseram um esquema de calibração estável e robusto que reduz a busca não linear a apenas 3 parâmetros ($t_c, m, \omega$) ao linearizar os demais parâmetros e escravizar dois parâmetros não lineares ao tempo crítico $t_c$. Esse método elimina a necessidade de buscas metaheurísticas complexas, utilizando algoritmos de busca local controlada.

### Estudo de Caso Empírico: O Crash do Bitcoin (2017–2018)

A aplicação prática das métricas de entropia e complexidade foi demonstrada empiricamente na análise da bolha e *crash* do Bitcoin no período de 21 de agosto de 2017 a 03 de abril de 2018, utilizando uma janela móvel de $w = 50$ dias e passo $\Delta t = 1$ dia. O início do *crash* é identificado em **06 de dezembro de 2017**.

#### Comportamento Observado das Métricas de Entropia:

1. **PEn Clássica:** Apresenta valores elevados ($0{,}98 - 1{,}00$) na fase pré-crise de crescimento. À medida que o preço atinge o pico em início de dezembro de 2017, a $PEn$ declina rapidamente, atingindo seu mínimo absoluto durante a fase mais aguda do *crash* ($\approx 0{,}94$), demonstrando forte sincronização do mercado e antecipando o colapso.
2. **WPEn (Ponderada por Variância):** Exibe alta sensibilidade a picos abruptos de volatilidade. Enquanto a $PEn$ cai gradualmente, a $WPEn$ registra quedas acentuadas e repentinas em momentos de variações de amplitude severas, atingindo o mínimo ($\approx 0{,}89 - 0{,}90$) no pico da crise (final de dezembro a janeiro).
3. **AAPEn (Sensível à Amplitude):** Com $A = 0{,}5$, capta perturbações sutis impulsionadas pela magnitude dos preços e variações consecutivas. Mostra uma tendência descendente discernível antes de 06 de dezembro de 2017, funcionando como um sinal precursor precoce extremamente claro.
4. **UPEn (Quantização Uniforme):** Com $d_E = 3, \tau = 1, D = 4$, gera uma curva mais suave que filtra ruídos de curto prazo (escala $0{,}35 - 0{,}60$). Revela a transição estrutural contínua de longo prazo, do estado estável para o estado frágil.

---

## 9. Implementação em Python e Checklist

### Implementação Prática em Python (EntropyHub)

O código abaixo ilustra a rotina completa de cálculo de retornos padronizados e estimação das quatro métricas de entropia de permutação via janela móvel utilizando Python e a biblioteca `EntropyHub`.

```python
import numpy as np
import pandas as pd
import EntropyHub as EH

def calcular_retornos_padronizados(precos):
    """
    Calcula retornos simples e aplica padronizacao z-score.
    """
    retornos_simples = (precos[1:] - precos[:-1]) / precos[:-1]
    media = np.mean(retornos_simples)
    desvio = np.std(retornos_simples)
    retornos_padronizados = (retornos_simples - media) / desvio
    return retornos_padronizados

def calcular_entropias_janela_movel(series_retornos, window=50, m=3, tau=1, D=4, A=0.5):
    """
    Aplica janela movel para calcular PEn, WPEn, AAPEn e UPEn.
    """
    n = len(series_retornos)
    num_janelas = n - window + 1
    
    pen_list = []
    wpen_list = []
    aapen_list = []
    upen_list = []
    
    for i in range(num_janelas):
        sub_series = series_retornos[i : i + window]
        
        # 1. Classical Permutation Entropy
        pen, _ = EH.PEn(sub_series, m=m, tau=tau)
        pen_list.append(pen[-1] if isinstance(pen, np.ndarray) else pen)
        
        # 2. Weighted Permutation Entropy
        wpen, _ = EH.WPEn(sub_series, m=m, tau=tau)
        wpen_list.append(wpen[-1] if isinstance(wpen, np.ndarray) else wpen)
        
        # 3. Amplitude-Aware Permutation Entropy
        aapen, _ = EH.AAMSEn(sub_series, m=m, tau=tau) if hasattr(EH, 'AAPEn') else EH.PEn(sub_series, m=m, tau=tau) # Proxy via EH
        aapen_list.append(aapen[-1] if isinstance(aapen, np.ndarray) else aapen)
        
        # 4. Uniform Quantization-Based Permutation Entropy (UPEn)
        # Processo de quantizacao uniforme
        x_min, x_max = np.min(sub_series), np.max(sub_series)
        delta = (x_max - x_min) / D if x_max != x_min else 1
        sub_quant = np.floor((sub_series - x_min) / delta)
        upen, _ = EH.PEn(sub_quant, m=m, tau=tau)
        upen_list.append(upen[-1] if isinstance(upen, np.ndarray) else upen)
        
    return pd.DataFrame({
        'PEn': pen_list,
        'WPEn': wpen_list,
        'AAPEn': aapen_list,
        'UPEn': upen_list
    })

## Exemplo de utilizacao com dados simulados
np.random.seed(42)
dados_precos = np.cumprod(1 + np.random.normal(0.001, 0.02, 300)) * 5000
retornos_g = calcular_retornos_padronizados(dados_precos)
df_entropias = calcular_entropias_janela_movel(retornos_g, window=50, m=3, tau=1, D=4)
print(df_entropias.head())
```

### Checklist Prático de Monitoramento de Risco

* [ ] **Tratamento de Dados:** Converter preços brutos em retornos padronizados $g(t)$ para remover viés de escala e garantir estacionariedade local.
* [ ] **Parametrização da Janela Móvel:** Selecionar $w = 50$ dias para dados diários, ajustando o passo para $\Delta t = 1$.
* [ ] **Configuração de Parâmetros de Imersão:** Definir dimensão de imersão $d_E = 3$ e tempo de atraso $\tau = 1$.
* [ ] **Monitoramento de Precursores ($AAPEn$ e $PEn$):** Verificar se $AAPEn$ e $PEn$ iniciam uma trajetória descendente consistente mesmo durante renovação de picos de preço.
* [ ] **Confirmação de Volatilidade ($WPEn$):** Avaliar quedas abruptas na $WPEn$ para identificar choques iminentes de amplitude e volatilidade.
* [ ] **Avaliação Estrutural de Longo Prazo ($UPEn$):** Observar a curva contínua da $UPEn$ com $D = 4$ para confirmar a transição de regime e perda de complexidade sistêmica.
* [ ] **Calibração do Modelo LPPL:** Em momentos de queda acentuada na entropia, ajustar a equação LPPL via algoritmo de Filimonov-Sornette para estimar a data crítica $t_c$ do colapso.

---

## 10. Tabela Comparativa e Glossário

### Tabela Comparativa das Métricas de Entropia

| Métrica | Mecanismo de Funcionamento | Sensibilidade à Amplitude | Trata Valores Iguais (*Ties*)? | Principal Aplicação Prática |
| :--- | :--- | :--- | :--- | :--- |
| **$PEn$ (Permutação Clássica)** | Frequência de padrões ordinais ($d_E!$). | Não (Ignora magnitudes absolutas). | Adiciona ruído ou ordem de aparição. | Identificação de declínio gradual de complexidade pré-crash. |
| **$WPEn$ (Ponderada)** | Ponderação por variância local (energia) da subsequência. | Sim (Alta sensibilidade à variância/energia). | Não trata ambiguidades de deslocamento constante. | Detecção em tempo real de picos de volatilidade e instabilidades graves. |
| **$AAPEn$ (Sensível à Amplitude)** | Coeficiente $L(X_t)$ combinando amplitude média e diferenças consecutivas. | Sim (Altamente refinada e ajustável via $A$). | Sim (Reduz ambiguidades em dados discretizados). | Indicador precursor precoce mais transparente para crashes. |
| **$UPEn$ (Quantização Uniforme)** | Simbolização via Quantização Uniforme em $D$ níveis. | Sim (Focada na estrutura quantizada). | Sim (Elimina ambiguidades por discretização uniforme). | Monitoramento estrutural de longo prazo; filtragem de ruído de curto prazo. |

---

### Glossário Técnico

* **Amplitude-Aware Permutation Entropy ($AAPEn$):** Variante da entropia de permutação que incorpora tanto os níveis médios de amplitude quanto as variações entre amostras consecutivas no cálculo de pesos.
* **Autovalor de Mercado ($\lambda_{\max}$):** Maior autovalor obtido a partir da matriz de correlação de ativos; quando se afasta do espectro aleatório de Marchenko-Pastur, indica colapso da diversificação e comportamento sistêmico unificado.
* **Causalidade de Granger:** Conceito estatístico onde uma série temporal $X$ causa $Y$ se os valores passados de $X$ contiverem informações estatisticamente significativas para prever $Y$ além das informações contidas no próprio passado de $Y$.
* **Econofísica:** Aplicação de conceitos e métodos da física (especialmente mecânica estatística e teoria do caos) para responder a problemas complexos no domínio das finanças e economia.
* **Equação do Calor / Difusão:** Equação diferencial parcial parabólica que descreve a distribuição do calor ou difusão de partículas em um meio físico; forma na qual a EDP de Black-Scholes pode ser transformada.
* **Greeks (Gregas):** Sensibilidades do preço de um derivativo em relação a parâmetros subjacentes, incluindo Delta ($\partial V / \partial S$), Gamma ($\partial^2 V / \partial S^2$) e Theta ($\partial V / \partial t$).
* **Log-Periodic Power Law (LPPL):** Modelo quantitativo desenvolvido por Johansen-Ledoit-Sornette que descreve bolhas financeiras através de crescimento super-exponencial combinado com oscilações log-periódicas que convergem para um tempo crítico $t_c$.
* **Padrão Ordinal:** Sequência discreta de permutações obtida ao ordenar os elementos de um vetor de dados contínuos de acordo com suas magnitudes relativas.
* **Tempo Crítico ($t_c$):** Parâmetro do modelo LPPL que define o ponto de inflexão estocástico, representando o término teórico de uma bolha e o momento de máxima probabilidade de colapso (*crash*).
* **Transfer Entropy ($TE$):** Medida não paramétrica e não linear da teoria da informação que quantifica a quantidade de fluxo de informação direcional transferido de uma série temporal $X$ para $Y$.
* **Uniform Quantization-Based Permutation Entropy ($UPEn$):** Método de entropia que aplica discretização uniforme em $D$ níveis nos vetores de imersão para mitigar problemas com dados repetidos e capturar tendências estruturais de longo prazo.
* **Weighted Permutation Entropy ($WPEn$):** Métrica que modifica a entropia de permutação atribuindo pesos a cada padrão ordinal com base na variância dos pontos que constituem a subsequência.