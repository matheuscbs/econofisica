<!-- imported from vault study notes; curated for open course -->
# M08.A01 — ARCH/GARCH: a variância não some — ela propaga

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M08
> **Aula:** M08.A01

↑ M08 · Resumo · Completo

**Módulo:** M08
**Pergunta do módulo:** Como a variância propaga e prepara regras de regime?

## Conceito-núcleo
Heterocedasticidade condicional: choques de vol persistem; GARCH modela a memória da variância.

## Aplicação em mercado / trading
Forecast de vol para sizing, hedge e limiares de regime; ponte conceitual para resposta assinada à variância (Janus).

## Entregável / lab
Ajustar GARCH(1,1) a retornos; plotar σ_t vs |r_t|; usar σ_t como input de regra de risco.

## Fonte (mapeamento)
quantitative-trading-free-lesson/28 arch-garch-variance-does-not-disappear-it-propagates | preâmbulo Janus IG

## Guia de estudo aprofundado

> **info**
>

Este guia fornece uma síntese estruturada e aprofundada sobre a modelagem de heterocedasticidade condicional por meio dos modelos ARCH e GARCH, com foco no papel da variância como um estado interno de tensão e no seu impacto direto no dimensionamento de risco e gestão de portfólios.

---

### Conceitos Fundamentais e Formulação Matemática

Na análise de séries temporais financeiras, observa-se frequentemente que o retorno $R_t$ apresenta baixa autocorrelação em nível, mas forte autocorrelação em seus valores absolutos ou ao quadrado:

$$Corr(R_t, R_{t-k}) \approx 0, \qquad Corr(R_t^2, R_{t-k}^2) > 0$$

Essa assimetria estatística reflete um fenômeno central dos mercados: a direção do preço (o sinal do retorno) é de difícil previsão, mas a intensidade ou dispersão do movimento deixa rastro. Períodos de choque e alta volatilidade tendem a ser seguidos por novos choques, enquanto fases de calmaria tendem a se prolongar. O mercado não guarda memória direcional prolongada, mas possui memória de dispersão (conhecida como *volatility clustering* ou agrupamento de volatilidade).

#### Estrutura Geral do Processo
Para capturar o ruído heterocedástico, a série de retornos é decomposta como:

$$R_t = \mu_t + \epsilon_t, \qquad \epsilon_t = \sigma_t z_t$$

Onde:
*   $\mu_t$ é a dinâmica do retorno médio (pode ser assumida constante ou estimada).
*   $\epsilon_t$ é o choque ou residual no instante $t$.
*   $z_t$ é uma variável aleatória i.i.d. com $E[z_t] = 0$ e $Var(z_t) = 1$.
*   $\sigma_t^2 = Var(\epsilon_t \mid \mathcal F_{t-1})$ é a **variância condicional**, dependente da informação disponível até o momento $t-1$ ($\mathcal F_{t-1}$).

#### O Modelo ARCH(q)
No modelo Autoregressivo com Heterocedasticidade Condicional de ordem $q$, a variância de hoje depende diretamente do quadrado dos $q$ choques passados:

$$\sigma_t^2 = \omega + \alpha_1\epsilon_{t-1}^2 + \alpha_2\epsilon_{t-2}^2 + \cdots + \alpha_q\epsilon_{t-q}^2$$

Com restrições de não-negatividade: $\omega > 0$ e $\alpha_i \ge 0$.
*   $\omega$: Nível base ou piso irredutível de variância.
*   $\alpha_i$: Coeficientes de transmissão que ditam o impacto de choques passados na variância atual.

*Limitação do ARCH:* Para capturar persistências de longo prazo, o ARCH exige um número elevado de defasagens ($q$), o que reduz a eficiência da estimação e aumenta a parametrização.

#### O Modelo GARCH(1,1)
O modelo GARCH (ARCH Generalizado) resolve a limitação de memória ao comprimir o histórico da variância condicional por meio de uma estrutura autorregressiva do próprio $\sigma^2$:

$$\sigma_t^2 = \omega + \alpha\epsilon_{t-1}^2 + \beta\sigma_{t-1}^2$$

Com as condições estruturais: $\omega > 0$, $\alpha \ge 0$, $\beta \ge 0$.

*   $\alpha$ (**Reatividade**): Mede a sensibilidade imediata do sistema a um choque recente ($\epsilon_{t-1}^2$).
*   $\beta$ (**Inércia / Persistência da Variância**): Mede a memória do estado de tensão anterior ($\sigma_{t-1}^2$).
*   $\alpha + \beta$ (**Persistência Total do Sistema**): Determina quão lentamente a tensão se dissipa.

#### Condição de Estacionariedade e Variância Incondicional
Para que o processo seja covariância-estacionário, exige-se estritamente que:

$$\alpha + \beta < 1$$

Sob essa condição, a **variância incondicional** (média de longo prazo) existe e é dada por:

$$E[\sigma_t^2] = \frac{\omega}{1 - \alpha - \beta}$$

A variância média de longo prazo não é apenas o piso $\omega$; ela é amplificada pelo fator de persistência do sistema $(1 - \alpha - \beta)^{-1}$.

#### Estimação por Máxima Verossimilhança (MLE)
A estimação dos parâmetros $\theta = (\omega, \alpha, \beta, \mu)$ é feita maximizando a log-verossimilhança condicional. Sob a hipótese de erros com distribuição Gaussiana padrão $z_t \sim \mathcal{N}(0, 1)$:

$$\ell(\theta) = -\frac{1}{2}\sum_{t=1}^{T}\left[\log(2\pi) + \log(\sigma_t^2) + \frac{\epsilon_t^2}{\sigma_t^2}\right]$$

Se a série apresentar caudas pesadas mesmo após a padronização, substitui-se a distribuição Gaussiana por uma distribuição $t$ de Student para evitar a subestimativa do risco extremo.

---

### Intuição de Mercado e Aplicação em Trading

A diferença entre ruído homocedástico e heterocedástico reside na transformação do clima do mercado:
1.  **Visão Homocedástica:** Os choques ocorrem dentro de uma dispersão fixa e invariável no tempo.
2.  **Visão GARCH:** Cada choque altera a própria estrutura da dispersão futura. Um choque violento no instante $t-1$ eleva $\sigma_t^2$. Por sua vez, esse $\sigma_t^2$ amplificado alimentará $\sigma_{t+1}^2$ por meio do termo $\beta \sigma_t^2$, propagando a volatilidade ao longo do tempo através de um decaimento suave.

#### Sigma Condicional como Input de Regime
O parâmetro $\sigma_t$ retornado pelo modelo não deve ser interpretado como uma previsão sobre a direção do ativo, mas sim como um **índice do estado de tensão local**.

*   **Dimensionamento de Posição e Alavancagem:** Quando o $\sigma_t$ condicional se eleva, o risco por unidade de capital aumenta instantaneamente, exigindo desalavancagem proporcional para manter a exposição ao risco constante.
*   **Value at Risk (VaR) Condicional:** Para um horizonte de 1 dia sob condicionalidade normal, o VaR é estimado dinamicamente por:

$$VaR_{\alpha, t+1} = -\left(\mu_{t+1} + q_\alpha \sigma_{t+1}\right)$$

Onde $q_\alpha$ é o quantil crítico da distribuição assumida para $z_t$. Em momentos pós-crise, o VaR condicional se ajusta imediatamente para cima, refletindo o novo regime de volatilidade, enquanto uma medida histórica incondicional demoraria dias ou semanas para responder.

---

### Exemplo Numérico Resolvido Passo a Passo

Considerando um ativo cujos parâmetros estimados para um modelo GARCH(1,1) são:
*   $\omega = 0{,}05$
*   $\alpha = 0{,}15$
*   $\beta = 0{,}80$
*   Média condicional assumiu-se $\mu = 0$, logo $R_t = \epsilon_t$.

#### Passo 1 Cálculo da Variância Incondicional
Verifica-se a condição de estacionariedade: $\alpha + \beta = 0{,}15 + 0{,}80 = 0{,}95 < 1$.

$$E[\sigma_t^2] = \frac{\omega}{1 - \alpha - \beta} = \frac{0{,}05}{1 - 0{,}15 - 0{,}80} = \frac{0{,}05}{0{,}05} = 1{,}00$$

A variância incondicional de longo prazo é igual a $1{,}00$ (volatilidade de longo prazo $\sigma = 1{,}00\%$).

#### Passo 2 Atualização da Variância Condicional no Instante $t$
Dado que no dia $t-1$:
*   A variância condicional era $\sigma_{t-1}^2 = 1{,}20$.
*   Ocorreu um choque forte de retorno $R_{t-1} = \epsilon_{t-1} = -2{,}00\%$ (logo, $\epsilon_{t-1}^2 = 4{,}00$).

Calcula-se a variância condicional para o dia $t$:

$$\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$
$$\sigma_t^2 = 0{,}05 + (0{,}15 \times 4{,}00) + (0{,}80 \times 1{,}20)$$
$$\sigma_t^2 = 0{,}05 + 0{,}60 + 0{,}96 = 1{,}61$$

A volatilidade condicional para o dia $t$ é:

$$\sigma_t = \sqrt{1{,}61} \approx 1{,}2688\%$$

#### Passo 3 Propagação para o Instante $t+1$ (Projeção)
Assumindo que no dia $t$ o choque foi nulo ($\epsilon_t = 0$):

$$\sigma_{t+1}^2 = \omega + \alpha (0)^2 + \beta \sigma_t^2$$
$$\sigma_{t+1}^2 = 0{,}05 + 0 + (0{,}80 \times 1{,}61) = 0{,}05 + 1{,}288 = 1{,}338$$
$$\sigma_{t+1} = \sqrt{1{,}338} \approx 1{,}1567\%$$

Note que, mesmo sem choque adicional ($\epsilon_t = 0$), a volatilidade condicional em $t+1$ ($1{,}1567\%$) permanece acima da média de longo prazo ($1{,}00\%$) devido à inércia do sistema ($\beta$).

#### Passo 4 Cálculo do VaR Condicional de 1 dia ($95\%$ de confiança)
Assumindo $z_t \sim \mathcal{N}(0, 1)$, o quantil $q_{0{,}05} \approx -1{,}645$.

$$VaR_{0.05, t} = -\left(0 + (-1{,}645 \times 1{,}2688)\right) \approx 2{,}087\%$$

---

### Armadilhas Comuns na Modelagem

1.  **Violação dos Parâmetros de Estacionariedade:** Estimar um modelo onde $\alpha + \beta \ge 1$ implica que o processo é não-estacionário (ou um modelo IGARCH). A variância incondicional deixa de existir e os choques causam impacto permanente na volatilidade futura.
2.  **Ignorar Autocorrelação nos Resíduos Padronizados:** Estimar o modelo e não testar a autocorrelação nos quadrados dos resíduos padronizados ($z_t^2 = \epsilon_t^2 / \sigma_t^2$). Se $z_t^2$ continuar exibindo autocorrelação significativa, a estrutura GARCH escolhida foi insuficiente para capturar toda a heterocedasticidade.
3.  **Assunção Falsa de Normalidade nas Caudas:** Utilizar a distribuição Gaussiana quando o ruído padronizado $z_t$ ainda apresenta curtose elevada. Isso gera uma falsa sensação de segurança, subestimando drasticamente o VaR e o risco de cauda. Nesses casos, deve-se adotar a distribuição $t$ de Student.
4.  **Confundir Volatilidade Condicional com Incondicional:** Utilizar a variância média de longo prazo para gerenciar riscos operacionais diários, ignorando que o regime local condicional pode estar muito acima da média histórica.

---

### Laboratório Prático em Python

Abaixo descreve-se o procedimento em passos para ajustar um modelo GARCH(1,1), validar seus resíduos e projetar a volatilidade.

#### Passo 1 Definição da Função de Ajuste
A função utiliza a biblioteca `arch` para estimar um modelo GARCH(1,1) com média constante e distribuição $t$ de Student para os resíduos.

```python
import numpy as np
import pandas as pd
from arch import arch_model

def fit_garch_11(returns: pd.Series, mean="Constant", dist="t"):
    # Limpeza e preparação dos dados de retorno
    r = pd.Series(returns).dropna().astype(float)
    
    # Especificação do modelo: p=1 (GARCH), q=1 (ARCH)
    am = arch_model(r, mean=mean, vol="GARCH", p=1, q=1, dist=dist)
    res = am.fit(disp="off")
    
    out = {
        "params": res.params,
        "cond_vol": res.conditional_volatility,
        "std_resid": res.std_resid,
        "loglik": res.loglikelihood,
    }
    return res, out
```

#### Passo 2 Função para Projeção da Volatilidade
Projeta-se a variância do próximo período com base no estado atual do modelo estimado.

```python
def forecast_next_vol(res, horizon=1):
    fc = res.forecast(horizon=horizon)
    var_next = fc.variance.iloc[-1, 0]
    return float(np.sqrt(var_next))
```

#### Passo 3 Validação dos Resíduos (Diagnóstico de Autocorrelação)
Para verificar se o modelo retirou com sucesso o agrupamento de volatilidade, compara-se a autocorrelação no lag 1 dos retornos ao quadrado antes e depois da padronização pelo $\sigma_t$ condicional.

```python
def acf_lag1(x):
    x = np.asarray(pd.Series(x).dropna(), float)
    if len(x) < 2:
        return np.nan
    x0 = x[:-1] - x[:-1].mean()
    x1 = x[1:] - x[1:].mean()
    den = np.sqrt((x0**2).sum() * (x1**2).sum())
    return float((x0 @ x1) / den) if den > 0 else np.nan
```

#### Roteiro de Execução do Laboratório
1.  **Carregar os dados:** Importar a série temporal de retornos $R_t$.
2.  **Calcular ACF Original:** Executar `acf_lag1(R_t**2)` nos retornos originais ao quadrado. Espera-se um valor positivo e estatisticamente relevante.
3.  **Ajustar o Modelo:** Executar `res, out = fit_garch_11(R_t)` para obter os parâmetros $\omega, \alpha, \beta$ e os resíduos padronizados $z_t$.
4.  **Calcular ACF dos Resíduos Padronizados:** Executar `acf_lag1(out["std_resid"]**2)`. O valor da autocorrelação deve ceder drasticamente próximo a zero, confirmando a eliminação da heterocedasticidade.
5.  **Prever Próximo Regime:** Executar `forecast_next_vol(res)` para extrair o input de volatilidade do próximo período.

---

### Glossário de Termos

*   **Heterocedasticidade Condicional:** Propriedade de uma série temporal na qual a variância do erro não é constante ao longo do tempo, dependendo do conjunto de informações passadas.
*   **Volatilidade Clustering (Agrupamento):** Fenômeno em que grandes variações de preços são seguidas por grandes variações, e pequenas variações são seguidas por pequenas variações, criando regimes alternados de alta e baixa tensão.
*   **Reatividade ($\alpha$):** Coeficiente do modelo GARCH que mede o grau de sensibilidade da volatilidade futura em relação ao choque (erro ao quadrado) imediatamente anterior.
*   **Inércia / Persistência ($\beta$):** Coeficiente que mede a taxa de retenção do estado de volatilidade condicional prévio na estrutura atual.
*   **Variância Incondicional:** A média de longo prazo da variância de um processo estocástico estacionário, calculada por $\omega / (1 - \alpha - \beta)$.
*   **Resíduos Padronizados ($z_t$):** A série de erros $\epsilon_t$ dividida pela volatilidade condicional do período $\sigma_t$. Se o modelo for bem especificado, $z_t$ deve comportar-se como ruído branco sem autocorrelação nos seus quadrados.
*   **Log-Verossimilhança (Log-Likelihood):** Função matemática otimizada durante a estimação estatística para encontrar os parâmetros que maximizam a probabilidade de geração dos dados observados.

---

### Questões de Fixação e Avaliação

#### Nível 1 Básico

**Questão 1**
O que significa afirmar que a série de retornos de um ativo possui autocorrelação nula em nível, mas autocorrelação positiva nos seus quadrados?
*   (A) O sinal do retorno de amanhã pode ser previsto com precisão a partir do retorno de hoje.
*   (B) O mercado é completamente previsível tanto em direção quanto em magnitude.
*   (C) A direção do preço é difícil de prever, mas a intensidade ou volatilidade do movimento futuro guarda dependência do passado.
*   (D) A variância do mercado é constante ao longo do tempo e independe de choques passados.

**Questão 2**
Qual é a condição necessária para que um modelo GARCH(1,1) seja covariância-estacionário e possua uma variância incondicional bem definida?
*   (A) $\alpha + \beta = 1$
*   (B) $\alpha + \beta < 1$
*   (C) $\omega = 0$
*   (D) $\alpha > \beta$

---

#### Nível 2 Intermediário

**Questão 3**
Dado um modelo GARCH(1,1) com os parâmetros $\omega = 0{,}02$, $\alpha = 0{,}10$ e $\beta = 0{,}85$.
1. Calcule a variância incondicional de longo prazo.
2. Sabendo que o choque no instante $t-1$ foi de $\epsilon_{t-1} = 3{,}0$ e que a variância condicional anterior era $\sigma_{t-1}^2 = 0{,}80$, determine a volatilidade condicional $\sigma_t$ para o instante $t$.

**Questão 4**
Apresente a interpretação econômica/financeira dos coeficientes $\alpha$ e $\beta$ em um modelo GARCH(1,1). O que ocorre com a dinâmica da volatilidade quando a soma $\alpha + \beta$ aproxima-se de $1$?

---

#### Nível 3 Avançado

**Questão 5**
Explique detalhadamente como o diagnóstico de resíduos padronizados é utilizado para validar a especificação de um modelo GARCH. Qual é a utilidade do teste de autocorrelação sobre $z_t^2$ e por que a mudança de uma distribuição Gaussiana para uma distribuição $t$ de Student pode ser necessária?

---

### Gabarito e Soluções Detalhadas

##### Solução - Questão 1
**Resposta Correta: (C)**
*Justificativa:* A ausência de autocorrelação nos retornos em nível indica eficiência fraca/dificuldade de prever a direção (sinal). A autocorrelação positiva nos quadrados indica agrupamento de volatilidade (*volatility clustering*), confirmando que a dispersão/intensidade se propaga ao longo do tempo.

##### Solução - Questão 2
**Resposta Correta: (B)**
*Justificativa:* A condição para estacionariedade em covariância do modelo GARCH(1,1) requer estritamente que a soma dos parâmetros de reatividade ($\alpha$) e inércia ($\beta$) seja estritamente menor que $1$ ($\alpha + \beta < 1$).

##### Solução - Questão 3
1.  **Variância Incondicional:**
    $$E[\sigma_t^2] = \frac{\omega}{1 - \alpha - \beta} = \frac{0{,}02}{1 - 0{,}10 - 0{,}85} = \frac{0{,}02}{0{,}05} = 0{,}40$$
2.  **Variância Condicional $\sigma_t^2$ e Volatilidade $\sigma_t$:**
    Com $\epsilon_{t-1}^2 = 3{,}0^2 = 9{,}0$:
    $$\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$
    $$\sigma_t^2 = 0{,}02 + (0{,}10 \times 9{,}0) + (0{,}85 \times 0{,}80) = 0{,}02 + 0{,}90 + 0{,}68 = 1{,}60$$
    $$\sigma_t = \sqrt{1{,}60} \approx 1{,}2649$$

##### Solução - Questão 4
*   $\alpha$ mede a **reatividade** a choques recentes ($\epsilon_{t-1}^2$). Quanto maior o $\alpha$, maior é o impacto imediato de um evento extremo na volatilidade do período seguinte.
*   $\beta$ mede a **inércia** ou memória do estado prévio de tensão ($\sigma_{t-1}^2$).
*   Quando $\alpha + \beta \to 1$, a persistência da volatilidade aproxima-se da unidade. O sistema leva um tempo extremamente longo para dissipar os choques e retornar à média incondicional, caracterizando regimes prolongados de tensão no mercado.

##### Solução - Questão 5
A validação de um modelo GARCH exige verificar se a estrutura condicional capturou toda a heterocedasticidade presente nos dados. Para isso, analisam-se os resíduos padronizados $z_t = \epsilon_t / \sigma_t$.
1.  **Autocorrelação de $z_t^2$:** Se o modelo estiver bem especificado, $z_t$ deve comportar-se como um ruído branco i.i.d. Portanto, a autocorrelação dos resíduos padronizados ao quadrado $Corr(z_t^2, z_{t-k}^2)$ deve ser estatisticamente igual a zero. Caso ainda exista autocorrelação significante, a estrutura do modelo foi insuficiente para absorver a memória de volatilidade.
2.  **Uso da Distribuição $t$ de Student:** Frequentemente, mesmo após remover o agrupamento de volatilidade por meio de $\sigma_t$, a distribuição empírica de $z_t$ apresenta caudas mais pesadas do que as previstas por uma distribuição Normal (curtose excessiva). Ao adotar a distribuição $t$ de Student na função de verossimilhança, o modelo aloca maior probabilidade a eventos extremos residuais, ajustando corretamente a quantificação de risco (como no cálculo do VaR) e evitando a subestimação da severidade de choques futuros.