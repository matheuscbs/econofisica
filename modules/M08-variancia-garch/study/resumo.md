<!-- imported study note (resumo.md) -->
# Briefing Executivo: Módulo M08 - Variância que Propaga: ARCH/GARCH, Ponte aos Labs

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M08

↑ M08 · Resumo · Completo

## Resumo Executivo

O Módulo M08 do curso Econofísica Khem Kapital aborda a modelagem, estimação e avaliação da variância condicional e da matriz de covariância temporalmente variantes em séries temporais financeiras. Em finanças quantitativas e econofísica, a volatilidade é uma dimensão latente — ou seja, não observável diretamente nem mesmo *ex post*. Essa característica impõe desafios metodológicos rigorosos tanto no ajuste de modelos autoregressivos quanto na validação de suas previsões.

Este briefing sintetiza a fundamentação teórica e econométrica referente aos modelos da família ARCH/GARCH e suas extensões com comutação de regimes de Markov (MSGARCH), além de estruturar as práticas de avaliação estatística e econômica de previsões de volatilidade univariadas e multivariadas. O módulo atua como uma ponte crítica entre os fundamentos teóricos de séries temporais e os laboratórios práticos de aplicação em trading algorítmico, otimização de portfólios e gestão de risco extremo.

---

## Definições e Mecanismos Estruturais

### A Natureza Latente da Volatilidade

A variância condicional $\sigma_t^2 \equiv \text{Var}(r_t | \mathcal{F}_{t-1})$ de um retorno financeiro $r_t$ (assumindo média condicional nula $E[r_t | \mathcal{F}_{t-1}] = 0$) é uma variável estocástica não observável. Para testar ou estimar modelos de volatilidade, faz-se necessário o uso de uma "proxy de volatilidade" observável e não viesada, tais como o retorno diário ao quadrado $r_t^2$, a volatilidade realizada obtida via amostras intradia $RV^{(m)}_t$, ou a amplitude operacional baseada nas máximas e mínimas diárias ($RG_t$).

A utilização dessas proxies imperfeitas introduz ruído de medição, o que exige testes estatísticos e funções de perda estruturalmente robustos à presença desse ruído, sob pena de gerar classificações distorcidas de modelos e conclusões espúrias.

### Modelos de Volatilidade Univariada

A estrutura scedástica condicional determina como os choques do passado $y_{t-1}$ e a volatilidade latente antecedente $h_{t-1}$ propagam a variância futura. As principais formulações univariadas incluem:

*   **sARCH (ARCH Simples):** Proposto por Engle (1982), modela a variância em função dos choques passados:
    $$h_t = \alpha_0 + \alpha_1 y_{t-1}^2$$
    Requer $\alpha_0 > 0$, $\alpha_1 \ge 0$ para positividade, e $\alpha_1 < 1$ para estacionariedade.
*   **sGARCH (GARCH Padrão):** Proposto por Bollerslev (1986), adiciona um componente autoregressivo da variância:
    $$h_t = \alpha_0 + \alpha_1 y_{t-1}^2 + \beta h_{t-1}$$
    Garante positividade com $\alpha_0 > 0, \alpha_1 > 0, \beta \ge 0$ e estacionariedade em variância quando $\alpha_1 + \beta < 1$.
*   **eGARCH (GARCH Exponencial):** Desenvolvido por Nelson (1991) para capturar o efeito de alavancagem (*leverage effect*), onde quedas no preço provocam maior volatilidade do que altas de mesma magnitude:
    $$\ln(h_t) = \alpha_0 + \alpha_1 (|\eta_{t-1}| - E[|\eta_{t-1}|]) + \alpha_2 y_{t-1} + \beta \ln(h_{t-1})$$
    A transformação logarítmica garante a positividade intrínseca de $h_t$ sem necessidade de restrições de sinal nos parâmetros.
*   **gjrGARCH (GJR-GARCH):** Formulado por Glosten, Jagannathan e Runkle (1993), introduz uma variável indicadora $I_{\{y_{t-1} < 0\}}$ para diferenciar choques negativos:
    $$h_t = \alpha_0 + (\alpha_1 + \alpha_2 I_{\{y_{t-1} < 0\}}) y_{t-1}^2 + \beta h_{t-1}$$
*   **tGARCH (GARCH Umbral):** Zakoian (1994) modela diretamente o desvio padrão condicional $h_t^{1/2}$ em vez da variância, aplicando restrições lineares sobre os retornos positivos e negativos.

### Dinâmica de Mudança de Regime: MSGARCH e Mistura de GARCH

Modelos GARCH padrão frequentemente falham na presença de quebras estruturais ou mudanças no nível incondicional da volatilidade, resultando em uma persistência de volatilidade artificialmente elevada (próxima da unidade). A classe de modelos GARCH com comutação de regimes de Markov (MSGARCH) resolve esse problema permitindo que os parâmetros variem ao longo do tempo segundo um processo Markoviano discreto latente $s_t \in \{1, \dots, K\}$.

Seguindo a formulação de Haas, Mittnik e Paolella (2004a), evitam-se os problemas de "dependência de trajetória" (*path-dependency problem*) identificados em modelos anteriores (como os de Gray ou Dueker). Nela, $K$ processos GARCH paralelos e independentes progridem simultaneamente:

$$y_t | (s_t = k, \mathcal{F}_{t-1}) \sim D(0, h_{k,t}, \xi_k)$$

Onde a dinâmica do estado $s_t$ é regida por uma matriz de transição de primeira ordem $P$:

$$P = \begin{bmatrix} p_{1,1} & \dots & p_{1,K} \\ \vdots & \ddots & \vdots \\ p_{K,1} & \dots & p_{K,K} \end{bmatrix}$$

Onde $p_{i,j} = P[s_t = j | s_t-1 = i]$. A distribuição dos inovações padronizadas $\eta_{k,t}$ pode assumir formatos com caudas pesadas ou assimetrias, como as distribuições Normal, Student-$t$, GED e suas variações com assimetria de Fernández-Steel (snorm, sstd, sged).

A estimação dos parâmetros pode ser realizada por Máxima Verossimilhança (ML) ou métodos Bayesianos via MCMC (utilizando amostradores de caminhada aleatória adaptativa de Metropolis, como o algoritmo de Vihola).

---

## Avaliação e Comparação de Previsões de Volatilidade

Como a volatilidade latente não é observada, a avaliação de modelos requer o uso de proxies e métodos econométricos que previnam distorções assintóticas e perdas de poder estatístico.

### Regressões de Mincer-Zarnowitz e a Inovação MZ-GLS

O teste de otimização de previsão via regressão de Mincer-Zarnowitz (MZ) viável regride a proxy de volatilidade observada $\hat{\sigma}_t^2$ contra a volatilidade prevista pelo modelo $h_t$:

$$\hat{\sigma}_t^2 = \alpha + \beta h_t + e_t$$

A hipótese nula de otimidade estabelece $H_0: \alpha = 0 \cap \beta = 1$. No entanto, os resíduos $e_t$ dessa regressão apresentam heterocedasticidade severa sob a hipótese nula ($V_{t-1}[e_t] = \sigma_t^4 V_{t-1}[\eta_t]$).

Para resolver a perda de eficiência, o método **MZ-GLS** padroniza a regressão dividindo os termos pela previsão $h_t$:

$$\frac{\hat{\sigma}_t^2}{h_t} = \alpha \frac{1}{h_t} + \beta + \tilde{e}_t$$

Estudos de simulação comprovam que o teste MZ-GLS exibe propriedades dimensionais superiores em pequenas amostras e um ganho de poder estatístico expressivo quando comparado ao teste MZ com erros-padrão robustos de White.

### O Perigo das Transformações Não Lineares

Muitos pesquisadores tentam suavizar o impacto de retornos extremos aplicando regressões sobre transformações das proxies, tais como $|r_t|$ ou $\log(r_t^2)$. A análise econométrica demonstra que essas transformações introduzem distorções assintóticas severas quando os retornos exibem curtose excessiva (como na distribuição Student-$t$). Nestes casos, o parâmetro populacional de regressão desvia-se do valor verdadeiro, levando à rejeição sistemática de previsões perfeitas ($h_t = \sigma_t^2$) à medida que o tamanho da amostra cresce.

### Funções de Perda Robustas e a Supremacia do QLIKE

Ao comparar dois ou mais modelos concorrentes por meio do teste de Diebold-Mariano-West (DMW), a escolha da função de perda é crítica. Patton (2006) define uma função de perda $L(\hat{\sigma}_t^2, h_t)$ como "robusta" se a ordenação esperada de dois modelos concorrentes for idêntica, independentemente de ser avaliada contra a volatilidade verdadeira $\sigma_t^2$ ou contra uma proxy não viesada $\hat{\sigma}_t^2$.

A classe paramétrica homogênea e robusta de funções de perda univariadas de Patton é indexada pelo parâmetro de forma $b$:

$$L(\hat{\sigma}_t^2, h_t; b) = \begin{cases} \frac{1}{(b+1)(b+2)} \left(\hat{\sigma}_t^{2(b+2)} - h_t^{b+2}\right) - \frac{1}{b+1} h_t^{b+1} (\hat{\sigma}_t^2 - h_t), & b \neq -1, -2 \\ h_t - \hat{\sigma}_t^2 + \hat{\sigma}_t^2 \log \frac{\hat{\sigma}_t^2}{h_t}, & b = -1 \\ \frac{\hat{\sigma}_t^2}{h_t} - \log \frac{\hat{\sigma}_t^2}{h_t} - 1, & b = -2 \quad (\text{QLIKE}) \end{cases}$$

O erro médio quadrático (MSE, $b=0$) pertence a essa classe, mas simulações de Monte Carlo demonstram que a função de quase-verossimilhança **QLIKE ($b=-2$)** possui o maior poder estatístico na rejeição de modelos incorretos. Funções não robustas (como MAE, MSE-LOG ou MSE-SD) geram vieses severos na variância ideal, distorcendo os rankings de modelos mesmo quando utilizadas proxies de alta precisão.

### O Impacto do Uso de Dados de Alta Frequência

A precisão da proxy de volatilidade impacta diretamente o poder dos testes econométricos. A utilização de variâncias realizadas baseadas em dados intradia (como retornos de 30 minutos ou 5 minutos) reduz dramaticamente o ruído de medição. Estatisticamente:
*   Utilizar apenas $T=100$ observações com proxy de volatilidade realizada $RV^{(13)}$ (retornos de 30 minutos) oferece um poder estatístico equivalente a utilizar $T=1000$ observações diárias com retornos ao quadrado $RV^{(1)}$.
*   A amostragem em intervalos de 30 minutos é empiricamente ideal por capturar ganhos substanciais de precisão sem ser contaminada pelo ruído de microestrutura de mercado ou por negociantes não síncronos.

---

## Aplicações em Trading e Gestão de Risco

A modelagem precisa de variâncias e covariâncias condicionais traduz-se em estratégias operacionais e métricas de risco quantitativo nos laboratórios do curso.

### Otimização de Portfólios de Variância Mínima

Na alocação de ativos baseada em média-variância, a busca pelo Portfólio de Mínima Variância Global (GMVP) requer a inversão da matriz de covariância condicional $\Sigma_t$. O problema minimiza $w_t' \Sigma_t w_t$ sujeito a $w_t' \iota = 1$.

Conforme o arcabouço de Engle e Colacito, a matriz de covariância condicional verdadeira sempre produzirá a menor variância de portfólio *ex post* para qualquer vetor de retornos esperados não nulos assumido. Assim, a comparação do desempenho prático de dois modelos de covariância pode ser realizada diretamente comparando a volatilidade realizada dos portfólios resultantes.

### Minimização do Erro de Rastreamento (Tracking Error)

Para operações de *index tracking* ou arbitragem estatística (*long/short*), a matriz de covariância condicional fracionada determina os pesos ideais $w_t = \Sigma_{22,t}^{-1} \Sigma_{12,t}$. A qualidade das previsões da covariância condicional determina a minimização do erro quadrático médio de rastreamento do portfólio sintético em relação ao ativo-alvo.

### Gestão de Risco Caudal: VaR e Expected Shortfall

Modelos GARCH e MSGARCH alimentam diretamente os cálculos de Valor em Risco ($VaR_\alpha$) e Espectro de Perda Esperada ($ES_\alpha$). Em estruturas MSGARCH, o $VaR$ e o $ES$ são derivados da densidade preditiva completa, permitindo ajustar instantaneamente as perdas potenciais em cauda caso o mercado transite de um regime de baixa volatilidade para um regime de crise estocástica.

---

## Por que Importa e Conexão aos Módulos do Curso

A volatilidade é a engrenagem central do risco financeiro e da precificação de ativos. Compreender a propagação da variância e a metodologia correta de avaliação de modelos previne erros comuns na indústria, como a escolha de estratégias baseada em métricas distorcidas por ruído de proxy ou a incapacidade de reagir a choques de regime.

### Conexão Intermodular

```
+--------------------------------------------------------------------------+
|                       MÓDULOS ANTERIORES (M01 - M07)                     |
|        Estrutura de Mercado, Processos Estocásticos e Séries Temporais    |
+--------------------------------------------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
|                       MÓDULO M08 (ESTE MÓDULO)                            |
|       Variância que Propaga: ARCH/GARCH e MSGARCH ao Módulo Multivariado |
| - Agrupamento e Persistência de Volatilidade (GARCH, eGARCH, GJR)         |
| - Comutação de Regimes Markovianos (MSGARCH)                             |
| - Avaliação Robusta de Previsões (MZ-GLS, QLIKE, Proxies Intradia)       |
+--------------------------------------------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
|                         LABS E MÓDULOS SEGUINTES                         |
| - Lab de Trading Algorítmico: Volatility Timing e Dimensionamento        |
| - Lab de Risco Caudal: Backtesting de VaR e Expected Shortfall           |
| - Lab de Alocação: Otimização Dinâmica de Portfólios via DCC-GARCH       |
+--------------------------------------------------------------------------+
```

1.  **Fundação Econométrica (Módulos M01–M07):** O M08 utiliza as noções de processos estacionários, modelos ARMA e teoria de martingales para modelar a estrutura do segundo momento condicional.
2.  **Laboratórios de Trading Algorítmico:** As previsões de volatilidade do M08 são inseridas nos algoritmos de execução para dimensionamento de posições (*position sizing*) por volatilidade-alvo (*volatility targeting*).
3.  **Laboratórios de Risco e Alocação:** A avaliação robusta (QLIKE) garante que os modelos multivariados alimentando os motores de otimização de portfólios e matrizes de risco não estejam sofrendo de *overfitting* ou distorções causadas por proxies ruidosas.

---

## Citações Importantes com Contexto

### 1. Robustez das Funções de Perda a Proxies Imperfeitas

> *"The use of a conditionally unbiased, but imperfect, volatility proxy can lead to undesirable outcomes in standard methods for comparing conditional variance forecasts... A loss function is 'robust' if the ranking of any two volatility forecasts by expected loss is the same whether the ranking is done using the true conditional variance or some conditionally unbiased volatility proxy."*
> — **Andrew J. Patton (2006)**

*Contexto:* Patton demonstra que usar funções de perda inadequadas (como o MAE ou erro percentual) em testes de Diebold-Mariano pode fazer com que um modelo imperfeito ou com viés severo seja classificado como "melhor" do que um modelo perfeito, simplesmente porque a avaliação utilizou retornos ao quadrado em vez da volatilidade oculta real.

### 2. A Superioridade do Teste MZ-GLS

> *"Our suggested 'MZ-GLS' test has good size and much better power in finite samples than other MZ tests. The difference between MZ1 and MZ1-GLS was particularly striking when using the daily squared return as a proxy."*
> — **Andrew J. Patton e Kevin Sheppard (2007)**

*Contexto:* Os autores explicam que a regressão Mincer-Zarnowitz tradicional padece de heterocedasticidade grave nos resíduos. Ao aplicar MQG (GLS) dividindo os dados pela volatilidade prevista, o teste ganha estabilidade dimensional (tamanho) e capacidade de identificar modelos incorretos (poder) mesmo em amostras pequenas ($T=100$).

### 3. Eliminação do Problema de Dependência de Trajetória em MSGARCH

> *"The MSGARCH model of Haas et al. (2004a) has the advantage that the estimation does not face the 'path-dependency problem'... In their model, the authors define K separate GARCH-type processes, one for each regime of the unobserved Markov chain, which leads to volatility forecasts that can quickly adapt to variations in the unconditional volatility level."*
> — **David Ardia et al. (2019)**

*Contexto:* A citação destaca a resolução técnica do pacote `MSGARCH` em R. Modelos de mudança de regime anteriores exigiam avaliar $K^T$ trajetórias possíveis (intratável computacionalmente). A abordagem de Haas et al. permite estimar modelos com comutação de parâmetros de forma eficiente por Máxima Verossimilhança ou MCMC, adaptando-se instantaneamente a choques de volatilidade incondicional.

---

## Tabela Comparativa de Métodos e Métricas

A tabela a seguir resume as principais propriedades dos modelos e métodos de avaliação discutidos no Módulo M08:

| Categoria | Método / Modelo | Mecanismo Central | Principais Vantagens | Limitações / Cuidados |
| :--- | :--- | :--- | :--- | :--- |
| **Modelo Univariado** | **sGARCH** | Dependência autoregressiva da variância ($h_t$) e choques ($y_{t-1}^2$). | Simplicidade, facilidade de conversão e convergência. | Não captura assimetrias (efeito alavancagem); hiper-persistência sob quebra de regime. |
| **Modelo Assimétrico** | **eGARCH / GJR** | Termo assimétrico para impactos diferenciados de choques negativos. | Captura o efeito alavancagem realista de ativos de renda variável. | Maior rigor de parâmetros; eGARCH exige cálculo numérico de esperanças. |
| **Modelo de Regime** | **MSGARCH** | $K$ processos GARCH paralelos regidos por matriz de transição de Markov $P$. | Adaptação rápida a mudanças no nível incondicional; sem *path-dependency*. | Requer bibliotecas eficientes em C++; identificação de estados exige ordenação por variância. |
| **Avaliação MZ** | **MZ-GLS** | Regressão de Mincer-Zarnowitz ponderada por $1/h_t$. | Excelente tamanho e poder estatístico em pequenas amostras. | Exige atenção à heterocedasticidade em dados de alta frequência intradiários. |
| **Função de Perda** | **QLIKE ($b=-2$)** | Perda logarítmica proporcional $\frac{\hat{\sigma}^2}{h} - \log\frac{\hat{\sigma}^2}{h} - 1$. | Matematicamente robusta a ruído de proxy; maior poder estatístico no teste DMW. | Requer valores estritamente positivos da proxy e das previsões. |
| **Proxy de Volatilidade** | **Intraday RV ($m=13$)** | Soma dos retornos ao quadrado amostrados em intervalos de 30 min. | Reduz ruído de amostragem em até 10x em comparação aos dados diários. | Exige dados de alta frequência (*tick/bar data*) limpos de ruído microestrutural. |

---

## Insights Acionáveis e Diretrizes de Implementação

1.  **Priorize QLIKE em Seleção de Modelos:** Em pipelines de pesquisa quantitativa, utilize estritamente a função de perda **QLIKE** para comparar modelos de volatilidade via testes Diebold-Mariano-West. Descarte métricas como MAE ou RMSE sobre os retornos, pois elas geram escolhas enviesadas.
2.  **Adote Proxies Intradia quando Disponíveis:** Ao validar modelos de volatilidade diários, não utilize $r_t^2$ como ground truth se houver dados de alta frequência. A utilização da volatilidade realizada em barras de 30 minutos ($RV^{(13)}$) garante ganhos drásticos de poder estatístico sem introduzir o ruído de microestrutura inerente às barras de 1 ou 5 minutos.
3.  **Monitore a Persistência ($\alpha_1 + \beta$):** Se um modelo GARCH tradicional apresentar uma soma de parâmetros $\alpha_1 + \beta > 0.99$, investigue a ocorrência de quebras estruturais na série. Migre a especificação para um modelo **MSGARCH** com 2 regimes para isolar mudanças no nível incondicional da volatilidade.
4.  **Alique MZ-GLS nos Testes de Otimidade:** Substitua a regressão Mincer-Zarnowitz convencional OLS pela formulação padronizada **MZ-GLS**. Teste a hipótese conjunta $\alpha=0 \cap \beta=1$ garantindo a remoção da heterocedasticidade intrínseca dos resíduos.
5.  **Integração com Gestão de Risco:** Utilize as densidades preditivas completas geradas por estimadores Bayesianos em MSGARCH para alimentar diretamente o cálculo de $VaR$ e $Expected\ Shortfall$, capturando a assimetria e caudas pesadas características de períodos de estresse de mercado.