<!-- imported from vault study notes; curated for open course -->
# M10.A01 — Capstone — Lei assinada de resposta à variância (Janus)

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M10
> **Aula:** M10.A01

↑ M10 · Resumo · Completo

**Módulo:** M10
**Pergunta do módulo:** Como construir alocação frágil/antifrágil com consciência de regime?

## Conceito-núcleo
R_excess,t = α − β·σ²_t + ε; β>0 frágil; β<0 canal antifrágil (“massa financeira negativa”); densidades e regimes.

## Aplicação em mercado / trading
Estimar β por ativo/par; classificar frágil vs antifrágil; alimentar alocação defasada.

## Entregável / lab
Estimar a lei em SPY, QQQ, GLD (e pares SPY/GLD, QQQ/GLD); documentar sinais de β e regimes.

## Fonte (mapeamento)
janus-anti-fragility-strategy (mass.md, strat.md, bigravity model.py) | IG effective laws + Janus

## Guia de estudo aprofundado

> **info**
>

### Visão Geral e Objetivos de Aprendizagem

Este guia de estudo apresenta uma síntese rigorosa da estratégia determinística de econofísica Janus, fundamentada no operador de densidade de resposta assinada à variância e na teoria de bigravidade / métricas conjugadas. O objetivo é fornecer uma compreensão profunda da transição entre modelos cosmológicos bimetric e sua aplicação em engenharia financeira de arbitragem estatística e gestão antifrágil de portfólio.

Ao finalizar este material, você será capaz de:
* Compreender a transição teórica entre a bigravidade cosmológica de métricas conjugadas e a econofísica operacional de mercado.
* Derivar e interpretar a lei de resposta assinada à variância e diferenciar estados de massa financeira positiva (frágil) e negativa (antifrágil).
* Formular matematicamente os campos de densidade restritos ($\rho_+$ e $\rho_-$) e o operador de balanço de densidade ($\Delta\rho$).
* Implementar a lógica causal de troca de regime com defasagem temporal de execução e avaliar os critérios de saída baseados na aceleração do fator de escala.
* Avaliar a estrutura de precificação de opções e o modelo Black-Scholes / GBM modificado pela resposta assinada.
* Construir um pipeline prático em Python para backtest determinístico livre de viés de antecipação (*look-ahead bias*).

---

### Conceitos-Chave Explicados em Profundidade

#### Fundamentação Teórica de Bigravidade e Modelos Bimétricos

A origem conceitual do modelo Janus reside na física teórica e na cosmologia bimétrica desenvolvida por Jean-Pierre Petit. A relatividade geral tradicional baseia-se nas equações de Einstein $S = \chi T - g\Lambda$, onde se assumia historicamente que a constante cosmológica $\Lambda$ era nula e a aceleração da expansão do universo era impossível sem recorrer à "energia escura".

A abordagem bimétrica estende a dinâmica do ponto material ao utilizar o Grupo de Poincaré completo. O grupo de Lorentz possui quatro componentes conectadas: as componentes ortócronas (subgrupo $L_n$), que preservam a direção do tempo, e as componentes antícronas ($L_o$), que invertem a coordenada temporal. A ação coadjunta do grupo de Poincaré sobre seu espaço de momentos dá-se por:

$$P' = \lambda L_o P$$

$$M' = L_o M L_o^t + (C P^t L_o^t - L_o P C^t)$$

Quando $\lambda = -1$, a transformação antícrona converte movimentos ortócronos com energia e massa positivas em movimentos antícronos com energia e massa negativas. A introdução de uma dimensão adicional de Kaluza ($\zeta$) estende o grupo para oito componentes conectadas, introduzindo a simetria CPT (Inversão de Carga, Paridade Espacial e Inversão Temporal), onde a ação do elemento $(\lambda = -1, \nu = -1)$ reverte carga, espaço e tempo:

$$q' = \lambda \nu q$$

A matéria de massa negativa emite fótons de energia negativa. Por essa razão, observadores ou instrumentos compostos por matéria positiva não conseguem interagir nem registrar imagens ópticas dessa segunda espécie de matéria via ondas eletromagnéticas.

Para modelar a interação gravitacional, assume-se que o universo é uma variedade quadridimensional $M^4$ equipada com duas métricas conjugadas, $g^+$ e $g^-$. Partículas de massa positiva movem-se ao longo de geodésicas da métrica $g^+$, enquanto partículas de massa negativa movem-se ao longo de geodésicas de $g^-$. O sistema de equações de campo acopladas de Einstein assume a forma:

$$S^+(g^+) = \chi (T^+ - T^-)$$

$$S^-(g^-) = \chi (T^- - T^+)$$

Com a condição de acoplamento geométrico $S^+(g^+) = -S^-(g^-)$. Na aproximação newtoniana (fraca curvatura e baixas velocidades), a densidade do tensor de energia-momento reduz-se a $T_{00} \cong \rho c^2$, resultando em duas equações de Poisson acopladas para os potenciais gravitacionais $\Psi^+$ e $\Psi^-$:

$$\nabla^2 \Psi^+ = 4 \pi G (\rho^+ - \rho^-)$$

$$\nabla^2 \Psi^- = -4 \pi G (\rho^- - \rho^+)$$

Isso estabelece a relação fundamental $\Psi^- = -\Psi^+$, gerando a seguinte lei de interação:
* Massas do mesmo sinal atraem-se mutuamente via lei de Newton convencional.
* Massas de sinais opostos repelem-se mutuamente via "lei anti-Newtoniana".

Em um modelo cosmológico com métricas de Robertson-Walker com fatores de escala $R^+(\tau)$ e $R^-(\tau)$, a conservação de massa implica $\rho^+ (R^+)^3 = \text{constante}$ e $\rho^- (R^-)^3 = \text{constante}$. O sistema dinâmico resultante produz uma solução instável: se $R^+ > R^-$, então $\ddot{R}^+ > 0$ e $\ddot{R}^- < 0$. Isso explica a reaceleração da expansão observada no universo visível sem a necessidade de entidades exóticas.

#### Mecanismo Operacional da Lei de Resposta Assinada à Variância

Na transposição para a econofísica operacional, os conceitos físicos são convertidos em operadores matemáticos estritos aplicados a séries temporais financeiras. Não se trata de uma analogia metafórica, mas de uma equivalência formal de equações:

| Conceito Físico / Bimétrico | Operador Econofísico de Mercado |
| :--- | :--- |
| Massa Financeira Negativa | Resposta assinada negativa à variância ($\beta < 0$) |
| Energia | Variância realizada dos retornos logarítmicos ($\sigma_t^2$) |
| Campo de Densidade | Intensidade de resposta ajustada ao estresse causualmente |
| Superfície de Transição | Zero do balanço de densidade ($\Delta\rho(t) = 0$) |
| Reaceleração do Fator de Escala | Condição de retorno ao crescimento ($a_+(t) > 0$) |
| Paridade de Estado | Resíduo de conservação Put-Call dentro da tolerância |

A quantidade primitiva do modelo é o coeficiente $\beta$ na lei de resposta à variância, estimada pela relação entre o retorno anual em excesso e a variância realizada:

$$R_{\text{excess}, t} = \alpha - \beta \sigma_t^2 + \varepsilon_t$$

Onde a variância realizada (energia de variância $E_t$) é definida pela janela móvel de 252 dias úteis dos retornos logarítmicos $r_t = \Delta \log P_t$:

$$E_t = \sigma_t^2 = 252 \times \text{Var}(r_{t-251}, \dots, r_t)$$

O sinal do coeficiente $\beta$ determina o estado operacional do ativo:
* Estado de Resposta Positiva / Frágil ($\beta > 0$): $\frac{\partial R_{\text{excess}}}{\partial \sigma^2} < 0$. A volatilidade atua como um desvio / atrito (*variance drag*), reduzindo o retorno do ativo. É a dinâmica característica de índices de ações e ativos de crescimento convencionais (ex: SPY, QQQ).
* Estado de Resposta Negativa / Massa Financeira Negativa ($\beta < 0$): $\frac{\partial R_{\text{excess}}}{\partial \sigma^2} > 0$. A variância entra com sinal invertido na equação; episódios de alta volatilidade expandem o retorno em excesso do ativo. É o canal de antifragilidade observado em carreadores de pressão e refúgios (ex: GLD).

Uma descoberta empírica fundamental demonstrada nos dados é que o ticker do ativo não é um rótulo estático de estado:

$$\text{Ticker Identity} \neq \text{Response State}$$

A ação AAPL durante e após o período da COVID-19 ilustra essa dinâmica. No período pré-COVID (2015–2019), AAPL apresentou comportamento predominantemente frágil ($\beta > 0$). Durante o choque de 2020 e a reprecificação subsequente, a estimativa móvel de $\beta(t)$ para AAPL migrou para a região negativa ($\beta < 0$ em mais de 73% dos dias no período de reprecificação pós-COVID). Isso prova que um mesmo instrumento de capital próprio (*equity*) pode alterar seu estado de resposta sob diferentes regimes macroeconômicos.

#### Construção de Campos de Densidade Restritos

Para transformar os sinais de resposta em decisões determinísticas de alocação, constroem-se dois campos de densidade restritos para um par de ativos formado pelo ativo de crescimento ($R_+$) e o ativo de pressão ($R_-$).

Primeiro, isolam-se os componentes de resposta positiva e negativa:

$$M_+(t) = \max(\beta_+(t), 0)$$

$$M_-(t) = \max(-\beta_-(t), 0)$$

Em seguida, calcula-se o estresse de variância causal $S_i(t)$ usando a variância móvel de curto prazo $v_i(t)$ (janela de 62 dias) em relação à sua mediana histórica de 252 dias defasada em 1 período $b_i(t)$:

$$v_i(t) = 252 \times \text{Var}(\Delta \log P_i)_{t-62:t}$$

$$b_i(t) = \text{Median}_{252}(v_i)(t-1)$$

$$S_i(t) = \max\left(\frac{v_i(t)}{b_i(t)} - 1, 0\right)$$

Com esses elementos, formulam-se as densidades restritas do par:

$$\rho_+(t) = \frac{M_+(t)}{1 + S_+(t)}$$

$$\rho_-(t) = \frac{M_-(t) S_+(t)}{1 + S_-(t)}$$

As densidades satisfazem restrições operacionais estritas:
1. Densidade de Crescimento ($\rho_+$): proporcional ao coeficiente frágil $M_+(t)$, mas amortecida pelo estresse interno $S_+(t)$.
2. Densidade de Pressão ($\rho_-$): ativada unicamente quando o ativo de crescimento está sob estresse ($S_+(t) > 0$) E o ativo de pressão está em estado efetivo de massa negativa ($M_-(t) > 0$). Se o ativo de pressão perder sua característica antifrágil ($\beta_-(t) > 0 \implies M_-(t) = 0$), a densidade de pressão colapsa para zero ($\rho_-(t) = 0$), impedindo alocações falsas em momentos de estresse generalizado.

#### Transição de Regime, Balanço de Densidade e Execução Causal

O operador de balanço de densidade é a diferença escalar entre as duas densidades:

$$\Delta\rho(t) = \rho_+(t) - \rho_-(t)$$

O estado de transição é definido pela mudança de sinal de $\Delta\rho(t)$:
* Domínio de Crescimento: $\Delta\rho(t) > 0$
* Domínio de Pressão: $\Delta\rho(t) < 0$

Para garantir a causalidade estrita no filtro adaptado à filtração observada ($\mathcal{G}_t \in \mathcal{F}_t$), a alocação de capital é executada com exatamente um período de defasagem (*lag*):

$$\Delta\rho(t) < 0 \implies w_-(t+1) = 1, \quad w_+(t+1) = 0$$

A janela de confirmação do sinal $\tau(t)$ varia dinamicamente de acordo com a magnitude do desequilíbrio de densidade:

$$\tau(t) = \text{round}\left(\text{clip}\left(\frac{1}{\sqrt{|\Delta\rho(t)|}}, \tau_{\min}, \tau_{\max}\right)\right)$$

Desequilíbrios elevados ($\Delta\rho \ll 0$) produzem janelas de confirmação mais curtas (resposta rápida), enquanto desequilíbrios marginais exigem mais períodos de confirmação para evitar ruído de alta frequência.

#### Fatores de Escala e Condição de Saída

Os ativos são normalizados em fatores de escala $R_i(t) = P_i(t) / P_i(0)$. Suas derivadas temporais causais ($\dot{R}_i$ e $\ddot{R}_i$) são estimadas via filtros polinomiais de Savitzky-Golay ajustados em janelas passadas. A aceleração normalizada é dada por:

$$a_i(t) = \frac{\ddot{R}_i(t)}{R_i(t)}$$

A condição de saída do ativo de pressão e retorno ao ativo de crescimento é regida pelo campo de aceleração e balanço de densidade:

$$a_+(t) = \frac{\ddot{R}_+(t)}{R_+(t)} + \frac{1}{2}(\rho_+(t) - \rho_-(t)) > 0$$

Quando a aceleração própria do ativo de crescimento reverte para campo positivo sob o balanço de densidade vigente, a alocação retorna causavelmente a $R_+$.

A proxy de inércia financeira $I_t$ quantifica o atrito de variância em relação à resposta do ativo:

$$I_t = \frac{\sigma_t^2}{\beta}$$

Se $\beta > 0$, $I_t > 0$ representa um atrito que consome o retorno do ativo. Se $\beta < 0$, $I_t < 0$ reflete a inversão do atrito em força de expansão.

#### Estrutura de Opções e Kernel de Black-Scholes com Resposta Assinada

A camada de opções opera como uma auditoria de conservação estática, independente da dinâmica de troca de spot histórico. A identidade composta do patrimônio líquido baseia-se na paridade Put-Call:

$$S = B + C - P \quad \text{onde} \quad B = K e^{-rT}$$

 O resíduo de paridade do mercado é medido por:

$$\varepsilon_{\text{parity}} = (C - P) - (S - K e^{-rT})$$

O estado é considerado conservado se $|\varepsilon_{\text{parity}}| \le \tau_{\text{market}}$, onde $\tau_{\text{market}}$ é a tolerância calculada a partir dos *spreads* de compra e venda (*bid-ask*).

Na precificação de opções e modelagem estocástica, a difusão do ativo sob a lei de resposta assinada modifica a deriva do Movimento Browniano Geométrico (GBM):

$$\frac{d S_t}{S_t} = (\mu - \beta \sigma^2) dt + \sigma dW_t$$

Na forma logarítmica:

$$d \log S_t = \left(\mu - \beta \sigma^2 - \frac{1}{2}\sigma^2\right) dt + \sigma dW_t$$

Para o modelo Black-Scholes, o kernel de resposta assinada introduz um termo de transporte/carrego efetivo $\kappa_\beta$ na propagação do valor do dinheiro no tempo (*moneyness*), mantendo a taxa de desconto do título de renda fixa livre de risco ($K e^{-rT}$) inalterada:

$$\kappa_\beta = r - \beta \sigma^2$$

As variáveis $d_1$ e $d_2$ modificadas para o cálculo da opção assumem a forma:

$$d_1^\beta = \frac{\log(S/K) + \left(\kappa_\beta + \frac{1}{2}\sigma^2\right)T}{\sigma \sqrt{T}}$$

$$d_2^\beta = d_1^\beta - \sigma \sqrt{T}$$

As equações para as opções de compra ($C_\beta$) e venda ($P_\beta$) tornam-se:

$$C_\beta = S \Phi(d_1^\beta) - K e^{-rT} \Phi(d_2^\beta)$$

$$P_\beta = K e^{-rT} \Phi(-d_2^\beta) - S \Phi(-d_1^\beta)$$

Quando $\beta > 0$, o fator $\kappa_\beta$ reduz o carrego efetivo devido ao drag de variância. Quando $\beta < 0$, $\kappa_\beta$ aumenta o carrego efetivo, refletindo o ganho estrutural da massa negativa sob volatilidade.

---

### Intuição de Mercado e Trading

#### Drag de Volatilidade versus Antifragilidade

Na maioria dos ativos de risco (como ações e índices), a volatilidade é um inimigo silencioso do composto de retornos. Matematicamente, para um ativo com retorno médio $\mu$ e variância $\sigma^2$, o retorno composto aproximado é $\mu - \frac{1}{2}\sigma^2$. Quando estimamos a lei empírica de resposta assinada e encontramos $\beta > 0$, observamos um fenômeno ainda mais severo: a volatilidade destrói o retorno em excesso do ativo. Em momentos de pânico no mercado, esses ativos sofrem quedas acentuadas e expansão da variância.

Por outro lado, ativos de refúgio e proteção estrutural funcionam como detentores de massa financeira negativa ($\beta < 0$). Nesses instrumentos, a variância não é um fator de erosão, mas o próprio combustível do retorno. Quando o mercado amplo entra em estresse, esses ativos não apenas absorvem o choque, mas expandem suas cotações devido à reprecificação positiva gerada pela volatilidade.

#### Dinâmica de Estado e a Falsabilidade do Ticker Específico

Uma armadilha comum em modelos quantitativos clássicos é fixar regras estáticas baseadas em nomes de ativos (exemplo: "comprar ouro quando o índice cai"). O modelo Janus trata o mercado como um sistema dinâmico de campos acoplados, onde nenhum ticker possui um rótulo imutável.

Se as condições macroeconômicas mudarem e um ativo de proteção (como GLD) passar a responder de forma frágil à volatilidade ($\beta > 0$), a equação de densidade anula automaticamente sua densidade de pressão ($\rho_- = 0$). O modelo recusa-se a comprar a proteção porque ela perdeu sua propriedade de massa negativa. Da mesma forma, se um ativo de ações como AAPL passar a demonstrar propriedades antifrágeis em determinados regimes, o modelo reconhece a mudança de estado via cálculo rolante de $\beta(t)$.

---

### Exemplo Numérico Resolvido Passo a Passo

Considere um par de ativos formado pelo ativo de crescimento $R_+$ (SPY) e o ativo de pressão $R_-$ (GLD) no dia $t$. Abaixo, acompanhamos o cálculo passo a passo para determinar a alocação causavelmente executada no dia $t+1$.

#### Dados de Entrada Registrados no Dia $t$
* Coeficiente de resposta móvel de crescimento: $\beta_+(t) = 1,20$
* Coeficiente de resposta móvel de pressão: $\beta_-(t) = -2,50$
* Variância móvel de curto prazo do crescimento (62 dias): $v_+(t) = 0,085$
* Mediana histórica da variância do crescimento (252 dias defasada): $b_+(t) = 0,050$
* Variância móvel de curto prazo da pressão (62 dias): $v_-(t) = 0,040$
* Mediana histórica da variância da pressão (252 dias defasada): $b_-(t) = 0,035$

---

#### Passo 1 Isolar os Componentes de Resposta ($M_+$ e $M_-$)

$$M_+(t) = \max(\beta_+(t), 0) = \max(1,20, 0) = 1,20$$

$$M_-(t) = \max(-\beta_-(t), 0) = \max(-(-2,50), 0) = 2,50$$

---

#### Passo 2 Calcular os Níveis de Estresse Causal ($S_+$ e $S_-$)

$$S_+(t) = \max\left(\frac{v_+(t)}{b_+(t)} - 1, 0\right) = \max\left(\frac{0,085}{0,050} - 1, 0\right) = \max(1,70 - 1, 0) = 0,70$$

$$S_-(t) = \max\left(\frac{v_-(t)}{b_-(t)} - 1, 0\right) = \max\left(\frac{0,040}{0,035} - 1, 0\right) = \max(1,1428 - 1, 0) = 0,1428$$

---

#### Passo 3 Calcular as Densidades Restritas ($\rho_+$ e $\rho_-$)

Densidade da perna de crescimento:

$$\rho_+(t) = \frac{M_+(t)}{1 + S_+(t)} = \frac{1,20}{1 + 0,70} = \frac{1,20}{1,70} \approx 0,7059$$

Densidade da perna de pressão:

$$\rho_-(t) = \frac{M_-(t) S_+(t)}{1 + S_-(t)} = \frac{2,50 \times 0,70}{1 + 0,1428} = \frac{1,75}{1,1428} \approx 1,5313$$

---

#### Passo 4 Calcular o Balanço de Densidade ($\Delta\rho$) e Determinar o Regime

$$\Delta\rho(t) = \rho_+(t) - \rho_-(t) = 0,7059 - 1,5313 = -0,8254$$

Como $\Delta\rho(t) < 0$, o campo de densidade de pressão domina o sistema.

---

#### Passo 5 Determinar a Janela de Confirmação Dinâmica ($\tau$)

Assuma limites de parâmetro $\tau_{\min} = 1$ e $\tau_{\max} = 5$:

$$\tau(t) = \text{round}\left(\text{clip}\left(\frac{1}{\sqrt{|-0,8254|}}, 1, 5\right)\right) = \text{round}\left(\text{clip}\left(\frac{1}{0,9085}, 1, 5\right)\right) = \text{round}(1,1007) = 1$$

A transição é confirmada em 1 período.

---

#### Passo 6 Definir a Alocação Executada para o Dia $t+1$

Com a confirmação do desequilíbrio negativo no fechamento do dia $t$, a alocação causavelmente executada no início do próximo período comercial $t+1$ é:

$$w_+(t+1) = 0,0 \quad (0\%\text{ em SPY})$$

$$w_-(t+1) = 1,0 \quad (100\%\text{ em GLD})$$

---

### Armadilhas Comuns e Erros Metodológicos

* Viés de Antecipação no Sinal de Troca (*Look-Ahead Bias*): Utilizar o sinal calculado no fechamento do dia $t$ para obter o retorno do próprio dia $t$. A alocação gerada pelas informações disponíveis na filtração $\mathcal{F}_t$ só pode afetar a carteira do período $t$ para $t+1$.
* Estresse Causal com Baseline Contaminada: Calcular a mediana de referência da variância $b_i(t)$ incluindo os dados do próprio dia $t$. O correto é utilizar estritamente dados defasados $t-1$ ($\text{Median}_{252}(v_i)(t-1)$) para evitar contaminação de dados presentes na normalização.
* Suposição Estática de Ativos de Refúgio: Presumir que um ativo (como GLD) manterá permanentemente a propriedade de massa negativa ($\beta < 0$). Se o estresse no mercado for por liquidez irrestrita e o ativo de refúgio passar a ser vendido para cobrir margem ($\beta > 0$), o modelo deve zerar a densidade de pressão imediatamente via exclusão de resposta positiva.
* Confusão entre a Camada de Opções e a Camada Spot: Misturar os testes de conservação da paridade Put-Call com o sinal móvel de troca de densidade. O modelo de opções testa a consistência de precificação estática e não arbitragem do mercado em um *snapshot*, enquanto o sinal de spot rege a rotação temporal de capital.

---

### Laboratório Prático Sugerido em Python

Abaixo está o roteiro estruturado em passos para implementar o pipeline determinístico do modelo Janus em Python.

#### Passo 1 Carregamento de Dados e Cálculo dos Retornos Logarítmicos
```python
import numpy as np
import pandas as pd

## Carregar dados históricos de fechamento para SPY (crescimento) e GLD (pressão)
data = pd.DataFrame(...) # Colunas: 'SPY', 'GLD'

## Calcular retornos logarítmicos causais
log_returns = np.log(data / data.shift(1))
```

#### Passo 2 Estimar a Energia de Variância Móvel e Beta Móvel
```python
## Variância realizada anualizada de 252 dias (Energia)
var_252 = log_returns.rolling(window=252).var() * 252

## Retorno acumulado em excesso de 252 dias
excess_return = np.log(data / data.shift(252)) - 0.02 # Assumindo rf = 2%

## Estimativa de beta móvel (simplificada via covariância/variância móvel)
cov_ret_var = excess_return['SPY'].rolling(252).cov(var_252['SPY'])
var_var = var_252['SPY'].rolling(252).var()
beta_plus = - (cov_ret_var / var_var) # Inversão de sinal conforme equação de regressão
```

#### Passo 3 Construção dos Níveis de Estresse Causais
```python
## Variância de curto prazo (62 dias)
v_plus = log_returns['SPY'].rolling(window=62).var() * 252
v_minus = log_returns['GLD'].rolling(window=62).var() * 252

## Base de referência causal (mediana de 252 dias defasada em 1 dia)
b_plus = v_plus.shift(1).rolling(window=252).median()
b_minus = v_minus.shift(1).rolling(window=252).median()

## Estresse relativo
S_plus = (v_plus / b_plus - 1).clip(lower=0)
S_minus = (v_minus / b_minus - 1).clip(lower=0)
```

#### Passo 4 Cálculo das Densidades e Balanço de Regime
```python
M_plus = beta_plus.clip(lower=0)
## Assumindo beta_minus estimado para GLD
M_minus = (-beta_minus).clip(lower=0)

rho_plus = M_plus / (1 + S_plus)
rho_minus = (M_minus * S_plus) / (1 + S_minus)

delta_rho = rho_plus - rho_minus
```

#### Passo 5 Geração de Posição Defasada e Retorno da Estratégia
```python
## Sinal de regime (1 para pressão quando delta_rho < 0, caso contrário 0 para crescimento)
regime_raw = np.where(delta_rho < 0, 1.0, 0.0)

## Execução causal defasagem de 1 período
pos_minus = pd.Series(regime_raw, index=data.index).shift(1)
pos_plus = 1.0 - pos_minus

## Retorno diário simples da estratégia
simple_ret = data.pct_change()
strat_return = pos_plus * simple_ret['SPY'] + pos_minus * simple_ret['GLD']
strat_equity = (1 + strat_return).cumprod()
```

---

### Glossário de Termos

* Antifragilidade Financial: Propriedade de um ativo ou estratégia de se beneficiar e expandir retornos diante de episódios de elevada variância/disrupção do mercado ($\beta < 0$).
* Balanço de Densidade ($\Delta\rho$ / $H_2^+$): Diferença escalar entre a densidade de crescimento e a densidade de pressão. Valores negativos indicam dominância do regime de proteção.
* Bigravidade: Modelo teórico cosmológico baseado em duas métricas conjugadas ($g^+, g^-$) que descreve interações gravitacionais atrativas entre massas do mesmo sinal e repulsivas entre massas de sinais opostos.
* Drag de Variância (*Variance Drag*): Erosão dos retornos compostos gerada pela volatilidade em ativos com resposta positiva à variância ($\beta > 0$).
* Fator de Escala ($R_i(t)$): Preço normalizado de um ativo em relação ao seu valor inicial no tempo zero ($P_i(t)/P_i(0)$).
* Grupo de Poincaré Completo: Extensão de grupo contendo componentes ortócronas e antícronas, cuja ação no espaço de momentos permite estados de energia e massa negativas.
* Massa Financeira Negativa: Classificação operacional atribuída a um ativo cujo coeficiente de resposta assinada à variância é negativo ($\beta < 0$).
* Métricas Conjugadas: Par de tensores métricos acoplados ($g^+, g^-$) em uma variedade quadridimensional que determinam as geodésicas de partículas de massa positiva e negativa, respectivamente.
* Paridade Put-Call Composta: Relação de conservação em opções onde uma ação sintética é replicada por um título de renda fixa, uma opção de compra e uma opção de venda ($S = B + C - P$).
* Resposta Assinada à Variância: A inclinação $\beta$ na regressão do retorno em excesso do ativo contra sua variância realizada.

---

### Questões Práticas e Exercícios de Fixação

#### Nível 1 Questões de Resposta Curta (Conceitual)

1. Qual é a condição matemática formal para que um ativo seja classificado como possuidor de massa financeira negativa?
2. Como o estresse interno do ativo de pressão ($S_-$) afeta a densidade de pressão ($\rho_-$)?
3. Por que instrumentos ópticos baseados em matéria de massa positiva não conseguem detectar partículas de massa negativa no modelo de bigravidade?
4. Por que a alocação da carteira no modelo Janus exige obrigatoriamente um período de defasagem (*lag*) após a confirmação do sinal de regime?
5. O que ocorre com a densidade de pressão $\rho_-$ se o ativo de refúgio passar a apresentar resposta positiva à variância ($\beta_- > 0$)?

---

#### Respostas do Nível 1

1. A condição formal é $\beta < 0$ no operador de resposta assinada $R_{\text{excess}, t} = \alpha - \beta \sigma_t^2 + \varepsilon_t$, indicando que a derivada parcial do retorno em excesso em relação à variância é positiva ($\frac{\partial R_{\text{excess}}}{\partial \sigma^2} > 0$).
2. O estresse interno $S_-$ entra no denominador da equação de densidade de pressão ($\rho_- = \frac{M_- S_+}{1 + S_-}$). Portanto, um aumento no estresse do próprio ativo de pressão atua amortecendo e regularizando sua densidade para evitar instabilidade.
3. Partículas de massa negativa emitem fótons de energia negativa, os quais não interagem eletromagneticamente com detectores ou observadores formados por matéria de massa e energia positivas.
4. Para evitar o viés de antecipação (*look-ahead bias*) e garantir a causalidade estrita no filtro adaptado ($\mathcal{G}_t \in \mathcal{F}_t$), garantindo que os sinais calculados no fechamento de $t$ só afetem retornos negociáveis de $t$ para $t+1$.
5. Se $\beta_- > 0$, o componente $M_- = \max(-\beta_-, 0)$ torna-se zero. Isso zera imediatamente a densidade de pressão ($\rho_- = 0$), impedindo a migração de capital para um ativo de refúgio degradado.

---

#### Nível 2 Questões de Aplicação e Análise Numérica

1. Um analista observa os seguintes dados no fechamento de um determinado dia $t$:
   * $\beta_+(t) = 0,80$, $\beta_-(t) = -1,50$
   * $v_+(t) = 0,060$, $b_+(t) = 0,030$
   * $v_-(t) = 0,020$, $b_-(t) = 0,020$
   Calculate os valores de $S_+$, $S_-$, $\rho_+$, $\rho_-$ e determine o balanço de densidade $\Delta\rho(t)$. Qual será a decisão de alocação para o dia $t+1$?

2. Considere uma opção de compra em um ativo de massa negativa onde $\beta = -0,50$. Se a taxa livre de risco for $r = 4\%$ e a volatilidade do ativo for $\sigma = 30\%$, calcule o termo de carrego efetivo $\kappa_\beta$ utilizado no modelo Black-Scholes de resposta assinada e compare-o com o carrego tradicional.

---

#### Respostas do Nível 2

1. **Cálculo Passo a Passo:**
   * **Componentes de Resposta:** $M_+ = \max(0,80, 0) = 0,80$; $M_- = \max(-(-1,50), 0) = 1,50$.
   * **Níveis de Estresse:**
     $$S_+ = \max\left(\frac{0,060}{0,030} - 1, 0\right) = \max(2,0 - 1, 0) = 1,00$$
     $$S_- = \max\left(\frac{0,020}{0,020} - 1, 0\right) = \max(1,0 - 1, 0) = 0,00$$
   * **Densidades:**
     $$\rho_+ = \frac{0,80}{1 + 1,00} = \frac{0,80}{2,00} = 0,40$$
     $$\rho_- = \frac{1,50 \times 1,00}{1 + 0,00} = 1,50$$
   * **Balanço de Densidade:**
     $$\Delta\rho(t) = \rho_+ - \rho_- = 0,40 - 1,50 = -1,10$$
   * **Decisão para $t+1$:** Como $\Delta\rho(t) < 0$, o regime de pressão domina. A alocação em $t+1$ será $100\%$ no ativo de pressão $R_-$ e $0\%$ no ativo de crescimento $R_+$.

2. **Cálculo de $\kappa_\beta$:**
   * A variância é $\sigma^2 = (0,30)^2 = 0,09$.
   * O carrego efetivo é $\kappa_\beta = r - \beta \sigma^2 = 0,04 - (-0,50 \times 0,09) = 0,04 + 0,045 = 0,085$ ou $8,5\%$.
   * No modelo tradicional, o carrego de propagação é a própria taxa de juros $r = 4\%$. Sob a lei de resposta assinada com $\beta < 0$, a resposta antifrágil aumenta o carrego efetivo de propagação de $4,0\%$ para $8,5\%$, elevando o valor teórico da opção de compra devido ao ganho esperado sob variância.

---

#### Nível 3 Questões Dissertativas para Aprofundamento

1. Explique detalhadamente como o conceito de métricas conjugadas no modelo de bigravidade cosmológica de Jean-Pierre Petit e as equações de Poisson acopladas ($\nabla^2 \Psi^+ = 4\pi G(\rho^+ - \rho^-)$ e $\nabla^2 \Psi^- = -4\pi G(\rho^- - \rho^+)$) fundamentam a construção dos campos de densidade e do operador de balanço ($\Delta\rho$) no modelo determinístico Janus de negociação financeira.

2. Discuta o caso de estudo de reprecificação do papel da Apple (AAPL) durante o choque e o pós-choque da COVID-19. Por que a constatação de que o coeficiente móvel $\beta(t)$ migrou de terreno positivo para terreno predominantemente negativo refuta o paradigma de classificação estática de ativos e valida a econofísica operacional baseada em estados de resposta dinâmica?

---

#### Respostas do Nível 3

1. **Resposta Detalhada:**
   Na bigravidade bimétrica de Jean-Pierre Petit, o espaço-tempo é representado por duas métricas conjugadas ($g^+, g^-$) acopladas pelas equações de campo de Einstein, gerando dois potenciais gravitacionais opostos na aproximação newtoniana ($\Psi^- = -\Psi^+$). Essa relação demonstra que a matéria ordinária ($\rho^+$) e a matéria de massa negativa ($\rho^-$) exercem influências repulsivas entre si. A aceleração da expansão do universo acessível surge não de uma força misteriosa externa, mas do desequilíbrio e acoplamento relacional entre essas duas densidades.

   Na transposição para o modelo financeiro Janus, o par de ativos (Crescimento $R_+$ e Pressão $R_-$) assume o papel das duas populações cósmicas. Em vez de avaliar os ativos isoladamente por seus preços, constroem-se dois campos de densidade restritos ($\rho_+$ e $\rho_-$) baseados no estresse do mercado e na natureza de resposta à variância ($\beta$). O operador de balanço de densidade $\Delta\rho(t) = \rho_+(t) - \rho_-(t)$ atua como o equivalente do desequilíbrio das fontes de campo. A transição de regime ($\Delta\rho(t) < 0$) representa a repulsão/saída do capital da perna frágil de crescimento em direção à perna de pressão antifrágil. A dinâmica do portfólio torna-se, portanto, um sistema determinístico orientado pelo gradiente de densidade do par acoplado.

2. **Resposta Detalhada:**
   A abordagem tradicional de alocação quantitativa e gestão de risco baseia-se na premissa de que os ativos possuem rótulos fixos de classe: ações são ativos de risco/crescimento, títulos públicos e ouro são ativos de proteção/refúgio. O experimento com AAPL durante o período da COVID-19 desafia frontalmente essa visão estática.

   No período pré-COVID (2015–2019), AAPL comportava-se como um ativo de crescimento tradicional frágil, exibindo coeficiente $\beta > 0$ em relação à variância. Contudo, durante o choque de volatilidade e o subseqüente período de reprecificação macroeconômica, a regressão móvel revelou que a resposta de AAPL tornou-se negativa ($\beta < 0$ em mais de 73% dos dias no período de reprecificação pós-COVID). Isso significou que a volatilidade do mercado passou a expandir os retornos em excesso de AAPL, conferindo-lhe uma dinâmica temporária de massa financeira negativa e antifragilidade.

   Esse resultado demonstra numericamente a proposição fundamental do modelo: $\text{Ticker Identity} \neq \text{Response State}$. Ativos são condutos dinâmicos de resposta a choques. A econofísica operacional substitui o julgamento subjetivo do nome do ativo pela medição contínua e causualmente defasada do sinal de regime de resposta. Isso garante que o capital seja direcionado ao ativo que efetivamente apresenta comportamento de proteção no momento presente, evitando as falhas das correlações históricas estáticas durante crises estruturais de mercado.