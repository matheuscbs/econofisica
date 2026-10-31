<!-- imported study note (guia-completo.md) -->
# Guia Completo do Módulo M08: Variância que Propaga — ARCH/GARCH e Ponte aos Labs

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M08

↑ M08 · Resumo · Completo

## Sumário Executivo

Este documento apresenta um relatório de instrução técnica sobre a modelagem e previsão de volatilidade condicional no âmbito das séries temporais financeiras, cobrindo a teoria dos modelos da família ARCH/GARCH, suas variantes assimétricas e de mudança de regime, além das metodologias de avaliação econométrica de previsões. 

O objetivo central é detalhar como a volatilidade condicional não observada ($\sigma_t^2$) pode ser estimada, testada e utilizada em decisões financeiras quantitativas, como *volatility targeting*, gestão de risco e alocação de carteiras. O documento fundamenta-se nos arcabouços econométricos desenvolvidos por Engle (1982), Bollerslev (1986), Nelson (1991), Glosten, Jagannathan e Runkle (1993), Patton e Sheppard (2007, 2009), e Ardia et al. (2018).

### Principais Achados e Métricas-Chave

1. **Proxy de Volatilidade e Poder Estatístico:** O uso de proxies de volatilidade de alta frequência, como a volatilidade realizada amostrada a cada 30 minutos ($RV^{(13)}$) ou 5 minutos ($RV^{(78)}$), eleva substancialmente o poder dos testes estatísticos de otimização e comparação de modelos em amostras finitas em comparação com o retorno diário ao quadrado ($r_t^2$).
2. **Robustez das Funções de Perda:** Apenas funções de perda pertencentes à classe homogênea e robusta de Patton garantem que a ordenação de modelos concorrentes seja imune ao ruído da proxy de volatilidade utilizada. A função Quasi-Likelihood (**QLIKE**) destaca-se como a de maior poder estatístico nos testes de Diebold-Mariano-West (DMW).
3. **Ajuste à Heterocedasticidade com MZ-GLS:** A regressão de Mincer-Zarnowitz modificada por Mínimos Quadrados Generalizados (**MZ-GLS**) corrige a heterocedasticidade inerente aos resíduos das regressões de volatilidade, oferecendo propriedades superiores de tamanho e poder amostral.
4. **Captura de Assimetrias e Regimes:** A incorporação do efeito alavancagem via GJR-GARCH ou EGARCH, combinada com distribuições de caudas pesadas (Student-$t$, GED) e cadeias de Markov com mudanças de regime (MSGARCH), é essencial para capturar as descontinuidades e clusters de volatilidade observados em episódios de estresse de mercado.

---

## Análise Detalhada dos Temas e Seções do Módulo

### 1. Fatos Estilizados: Clustering de Volatilidade, Caudas Largas e Efeito Alavancagem

As séries temporais de retornos financeiros ($y_t$ ou $r_t$) apresentam propriedades estatísticas universais conhecidas como fatos estilizados, que invalidam a premissa de distribuição Normal com variância constante.

#### Ausência de Autocorrelação Linear e Estacionariedade na Média
Os retornos de ativos em frequências diárias ou intradia exibem média condicional nula e ausência de autocorrelação serial significativa:

$$\mathbb{E}[y_t] = 0 \quad \text{e} \quad \mathbb{E}[y_t y_{t-l}] = 0 \quad \forall \, l \neq 0$$

#### Agrupamento de Volatilidade (*Volatility Clustering*)
Embora os retornos em si não sejam autocorrelacionados, a magnitude dos retornos (medida por $|y_t|$ ou $y_t^2$) exibe forte autocorrelação serial positiva e persistente. Períodos de alta volatilidade são seguidos por períodos de alta volatilidade, e períodos de baixa volatilidade são seguidos por períodos de baixa volatilidade.

#### Caudas Pesadas e Leptocurtose
A distribuição incondicional dos retornos apresenta caudas consideravelmente mais pesadas que a distribuição Normal (*excess kurtosis*). Grandes oscilações de preço ocorrem com frequência substancialmente maior do que a prevista por um processo gaussiano.

#### Efeito Alavancagem (*Leverage Effect*)
Existe uma assimetria estrutural na resposta da volatilidade aos choques de preço. Retornos negativos significativos ($y_{t-1} < 0$) geram um impacto maior sobre a volatilidade futura do que retornos positivos ($y_{t-1} > 0$) de igual magnitude. Conforme documentado historicamente por Black (1976) e Christie (1982), quedas nos preços das ações elevam a alavancagem financeira da firma, aumentando o risco e, consequentemente, a volatilidade futura.

---

### 2. ARCH de Engle

Introduzido por Robert Engle em 1982 (trabalho reconhecido com o Prêmio Nobel de Economia em 2003), o modelo Autoregressive Conditional Heteroskedasticity (ARCH) foi a primeira formulação a parametrizar a variância condicional como uma função do passado dos resíduos ao quadrado.

#### Formulação Matemática do ARCH(1)
Seja $y_t$ o retorno de um ativo no instante $t$, condicional ao conjunto de informações $I_{t-1}$:

$$y_t = h_t^{1/2} \eta_t, \quad \eta_t \stackrel{\text{i.i.d.}}{\sim} D(0, 1)$$

Onde $h_t$ representa a variância condicional $\text{Var}(y_t | I_{t-1})$ e $D(0, 1)$ é uma distribuição contínua com média zero e variância unitária. O modelo ARCH(1) especifica a variância como:

$$h_t = \alpha_0 + \alpha_1 y_{t-1}^2$$

#### Restrições dos Parâmetros
* **Positividade:** Para garantir que $h_t > 0$ em todos os instantes $t$, exige-se:
  $$\alpha_0 > 0 \quad \text{e} \quad \alpha_1 \ge 0$$
* **Estacionariedade de Covariância:** A variância incondicional deve ser finita e constante ao longo do tempo. A condição necessária e suficiente é:
  $$\alpha_1 < 1$$

Nesse cenário, a variância incondicional $\bar{\sigma}^2 = \mathbb{E}[y_t^2]$ é dada por:

$$\bar{\sigma}^2 = \frac{\alpha_0}{1 - \alpha_1}$$

#### Mecânica de Propagação do Choque
Se o mercado sofre um choque exógeno no instante $t-1$ resultando em um retorno atípico $y_{t-1} = 3,0\%$, a variância para o período $t$ ($h_t$) reage diretamente ao quadrado dessa inovação ($y_{t-1}^2 = 9,0 \times 10^{-4}$). Se $\alpha_1$ for elevado, o choque persistirá por múltiplos períodos, gerando a dinâmica de *clustering*.

---

### 3. GARCH(1,1): Persistência, Variância Incondicional e Meia-Vida

Bollerslev (1986) generalizou o modelo ARCH ao incluir termos defasados da própria variância condicional, resultando no modelo Generalized ARCH (GARCH). A estrutura GARCH(1,1) oferece uma representação extremamente parcimoniosa para dinâmicas de volatilidade de alta ordem.

#### Formulação do Modelo GARCH(1,1)

$$h_t = \alpha_0 + \alpha_1 y_{t-1}^2 + \beta h_{t-1}$$

#### Restrições de Positividade e Estacionariedade
* **Positividade:**
  $$\alpha_0 > 0, \quad \alpha_1 > 0, \quad \beta \ge 0$$
* **Estacionariedade de Covariância:**
  $$k \equiv \alpha_1 + \beta < 1$$

Onde $k$ denota a **persistência total** do processo de variância.

#### Variância Incondicional
Se a condição de estacionariedade $k < 1$ for satisfeita, a variância incondicional de longo prazo $\bar{\sigma}^2$ é calculada por:

$$\bar{\sigma}^2 = \frac{\alpha_0}{1 - \alpha_1 - \beta}$$

#### Meia-Vida do Choque (*Half-Life*)
A meia-vida ($h_{HL}$) mensura o número de períodos necessários para que um desvio da variância condicional em relação à variância incondicional decline em 50%:

$$h_{HL} = \frac{\ln(0,5)}{\ln(\alpha_1 + \beta)}$$

#### Exemplo Numérico Concreto

Considere um modelo GARCH(1,1) estimado para retornos diários com os seguintes parâmetros:
$$\alpha_0 = 0,05, \quad \alpha_1 = 0,10, \quad \beta = 0,85$$

1. **Persistência ($k$):**
   $$k = 0,10 + 0,85 = 0,95$$
2. **Variância Incondicional ($\bar{\sigma}^2$):**
   $$\bar{\sigma}^2 = \frac{0,05}{1 - 0,95} = \frac{0,05}{0,05} = 1,00 \, (\%^2 \text{ ao dia})$$
   A volatilidade incondicional diária é $\bar{\sigma} = \sqrt{1,00} = 1,00\%$ (ou aproximadamente $15,87\%$ ao ano, considerando 252 dias úteis).
3. **Cálculo da Meia-Vida ($h_{HL}$):**
   $$h_{HL} = \frac{\ln(0,5)}{\ln(0,95)} = \frac{-0,693147}{-0,051293} \approx 13,51 \text{ dias}$$

Um choque de volatilidade leva aproximadamente 13,5 dias úteis para dissipar metade do seu impacto sobre a volatilidade condicional.

---

### 4. Estimação por Máxima Verossimilhança e Diagnósticos

#### Estimação por Máxima Verossimilhança (MLE)
Dada uma amostra de retornos $Y_T = \{y_1, y_2, \dots, y_T\}$ e o vetor de parâmetros $\Psi = (\alpha_0, \alpha_1, \beta, \xi)'$, a função de log-verossimilhança condicional é expressa por:

$$\ln L(\Psi | Y_T) = \sum_{t=1}^T \ln f(y_t | \Psi, I_{t-1})$$

Sob a hipótese de inovação Normal padrão ($\eta_t \sim \mathcal{N}(0,1)$):

$$\ln L(\Psi | Y_T) = -\frac{1}{2} \sum_{t=1}^T \left[ \ln(2\pi) + \ln(h_t) + \frac{y_t^2}{h_t} \right]$$

Se a distribuição verdadeira dos resíduos não for gaussiana, a estimação via verossimilhança gaussiana ainda fornece estimadores consistentes para os parâmetros de variância sob o arcabouço de **Quasi-Máxima Verossimilhança (QMLE)**, desde que os erros padrão sejam corrigidos pela matriz de covariância robusta de White.

#### Testes de Avaliação de Previsão: Mincer-Zarnowitz (MZ) e MZ-GLS
A avaliação da qualidade das previsões de volatilidade exige regressar a variância observada (ou sua proxy) sobre a variância prevista $h_t$.

##### Regressão Mincer-Zarnowitz Feita com Proxy de Volatilidade:
$$\hat{\sigma}_t^2 = \alpha + \beta h_t + e_t$$

A hipótese nula de otimidade do erro de previsão especifica:
$$H_0: \alpha = 0 \quad \cap \quad \beta = 1$$

Contudo, como os resíduos $e_t = \hat{\sigma}_t^2 - h_t = h_t(\eta_t^2 - 1)$ exibem forte heterocedasticidade sob a hipótese nula com $\text{Var}_{t-1}[e_t] = h_t^2 \text{Var}_{t-1}[\eta_t^2]$, os testes baseados em OLS padrão sofrem distorções severas de tamanho e perda de poder.

##### Modificação MZ-GLS Proposta por Patton e Sheppard:
Para corrigir a heterocedasticidade, divide-se a equação pelo previsor de volatilidade $h_t$:

$$\frac{\hat{\sigma}_t^2}{h_t} = \alpha \frac{1}{h_t} + \beta + \tilde{e}_t$$

Sob a hipótese nula ($H_0: \alpha = 0 \cap \beta = 1$), os resíduos $\tilde{e}_t$ tornam-se homocedásticos caso as inovações sejam condicionalmente homocúrticas.

#### Impacto das Proxies de Alta Frequência na Potência dos Testes
Simulações de Monte Carlo executadas por Patton e Sheppard demonstram o ganho de eficiência ao substituir o retorno diário ao quadrado ($RV^{(1)}$, $m=1$) por estimadores de volatilidade realizada construídos com dados intradia ($RV^{(13)}$, retornos de 30 minutos; e $RV^{(78)}$, retornos de 5 minutos):

| Tamanho Amostral ($T$) | Proxy Utilizada | Rejeição Nominal 5% (MZ1 White) | Rejeição Nominal 5% (MZ1-GLS) | Rejeição Nominal 5% (MZ2) |
| :--- | :--- | :--- | :--- | :--- |
| **$T = 100$** | $RV^{(1)}$ (Diário) | 0,23 | 0,11 | 0,07 |
| **$T = 100$** | $RV^{(13)}$ (30 min) | 0,09 | 0,07 | 0,06 |
| **$T = 100$** | $RV^{(78)}$ (5 min) | 0,07 | 0,06 | 0,05 |
| **$T = 1000$** | $RV^{(1)}$ (Diário) | 0,10 | 0,06 | 0,05 |
| **$T = 1000$** | $RV^{(13)}$ (30 min) | 0,06 | 0,05 | 0,05 |
| **$T = 1000$** | $RV^{(78)}$ (5 min) | 0,06 | 0,05 | 0,05 |

**Conclusão Crítica:** O teste MZ1-GLS possui um tamanho de amostra finita controlado mesmo para $T=100$. A utilização de dados intradia de 30 minutos ($RV^{(13)}$) com apenas $T=100$ observações atinge um poder estatístico equivalente ou superior ao uso de $T=1000$ observações diárias com retornos ao quadrado ($RV^{(1)}$).

---

### 5. Variantes Assimétricas GJR, EGARCH e Distribuições t

Para contornar as limitações do GARCH simétrico na captura do efeito alavancagem e das caudas pesadas, utilizam-se especificações assimétricas e distribuições flexíveis para as inovações.

#### GJR-GARCH
Desenvolvido por Glosten, Jagannathan e Runkle (1993), introduz um termo indicador para retornos negativos:

$$h_t = \alpha_0 + \left( \alpha_1 + \alpha_2 \mathbb{I}_{\{y_{t-1} < 0\}} \right) y_{t-1}^2 + \beta h_{t-1}$$

Onde $\mathbb{I}_{\{\cdot\}}$ é a função indicadora que assume valor 1 se $y_{t-1} < 0$ e 0 caso contrário. 
* **Positividade:** $\alpha_0 > 0$, $\alpha_1 > 0$, $\alpha_2 \ge 0$, $\beta \ge 0$.
* **Estacionariedade:** $\alpha_1 + \alpha_2 \mathbb{E}[\eta_t^2 \mathbb{I}_{\{\eta_t < 0\}}] + \beta < 1$. Para distribuições simétricas de $\eta_t$, isso reduz-se a $\alpha_1 + \frac{1}{2}\alpha_2 + \beta < 1$.

#### EGARCH
O modelo Exponential GARCH de Nelson (1991) parametriza o logaritmo da variância condicional:

$$\ln(h_t) = \alpha_0 + \alpha_1 \left( |\eta_{t-1}| - \mathbb{E}[|\eta_{t-1}|] \right) + \alpha_2 y_{t-1} + \beta \ln(h_{t-1})$$

A positividade de $h_t$ é garantida automaticamente para qualquer valor dos parâmetros devido à transformação exponencial $h_t = \exp(\ln(h_t))$. A condição de estacionariedade requer $|\beta| < 1$.

#### TGARCH
No Threshold GARCH de Zakoian (1994), o desvio padrão condicional é a variável dependente:

$$h_t^{1/2} = \alpha_0 + \left( \alpha_1 \mathbb{I}_{\{y_{t-1} \ge 0\}} - \alpha_2 \mathbb{I}_{\{y_{t-1} < 0\}} \right) y_{t-1} + \beta h_{t-1}^{1/2}$$

#### Distribuições de Inovações Não-Gaussianas
* **Student-$t$ Padronizada (`std`):**
  $$f_S(\eta; \nu) = \frac{\Gamma\left(\frac{\nu+1}{2}\right)}{\sqrt{(\nu-2)\pi} \, \Gamma\left(\frac{\nu}{2}\right)} \left( 1 + \frac{\eta^2}{\nu-2} \right)^{-\frac{\nu+1}{2}}, \quad \nu > 2$$
* **Generalized Error Distribution (`ged`):**
  $$f_{GED}(\eta; \nu) = \frac{\nu e^{-\frac{1}{2} |\eta/\lambda|^\nu}}{\lambda 2^{1 + 1/\nu} \Gamma(1/\nu)}, \quad \lambda \equiv \left( \frac{\Gamma(1/\nu)}{4^{1/\nu} \Gamma(3/\nu)} \right)^{1/2}$$
* **Versões com Assimetria (`snorm`, `sstd`, `sged`):** Implementadas via metodologia de Fernández e Steel (1998), adicionando um parâmetro de assimetria $\xi > 0$.

---

### 6. Previsão de Volatilidade e Term Structure

#### Previsão Multi-Passos à Frente no GARCH(1,1)
A previsão da variância condicional para $s$ passos à frente, condicionada às informações disponíveis no tempo $t$, é derivada iterativamente:

$$\mathbb{E}_t[h_{t+s}] = \bar{\sigma}^2 + (\alpha_1 + \beta)^{s-1} (h_{t+1} - \bar{\sigma}^2)$$

À medida que o horizonte de previsão $s \to \infty$, a previsão converge exponencialmente para a variância incondicional $\bar{\sigma}^2$ à taxa determinada pela persistência $k = \alpha_1 + \beta$.

#### Estrutura a Termo da Volatilidade (*Term Structure of Volatility*)
A volatilidade média anualizada prevista para um horizonte de $H$ dias é dada por:

$$\sigma_{t, H}^{\text{ann}} = \sqrt{252 \times \frac{1}{H} \sum_{s=1}^H \mathbb{E}_t[h_{t+s}]}$$

Se a volatilidade atual de curto prazo $h_{t+1}$ estiver acima da média de longo prazo $\bar{\sigma}^2$, a estrutura a termo apresentará inclinação negativa (*backwardation*). Se estiver abaixo, apresentará inclinação positiva (*contango*).

#### Funções de Perda Robustas e a Supremacia da QLIKE
Ao comparar modelos concorrentes através de testes de Diebold-Mariano-West (DMW), a utilização de uma proxy ruidosa $\hat{\sigma}_t^2$ pode alterar perversamente a ordenação dos modelos, a menos que a função de perda seja estatisticamente **robusta**.

##### Família Paramétrica de Perdas Robustas e Homogêneas de Patton (2006):

$$L(\hat{\sigma}_t^2, h_t; b) = \begin{cases} \frac{1}{(b+1)(b+2)} \left( \hat{\sigma}_t^{2(b+2)} - h_t^{b+2} \right) - \frac{1}{b+1} h_t^{b+1} (\hat{\sigma}_t^2 - h_t), & b \neq -1, -2 \\ \frac{\hat{\sigma}_t^2}{h_t} - \ln\left(\frac{\hat{\sigma}_t^2}{h_t}\right) - 1, & b = -2 \quad (\text{QLIKE}) \\ (\hat{\sigma}_t^2 - h_t)^2, & b = 0 \quad (\text{MSE}) \end{cases}$$

#### Tabela de Biés de Previsão sob Funções Não-Robustas
Abaixo, os resultados analíticos e de simulação compilados por Patton para o viés multiplicativo na previsão otimizada sob diferentes funções de perda e proxies de volatilidade:

| Função de Perda | Categoria | Proxy: $RV^{(1)}$ (Diário) | Proxy: $RV^{(13)}$ (30 min) | Proxy: $RV^{(78)}$ (5 min) | Proxy: Range Ajustado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MSE** ($b=0$) | Robusta | **1,00** | **1,00** | **1,00** | **1,00** |
| **QLIKE** ($b=-2$) | Robusta | **1,00** | **1,00** | **1,00** | **1,00** |
| **MSE-LOG** | **Não-Robusta**| 0,28 | 0,91 | 0,98 | 0,85 |
| **MSE-SD** | **Não-Robusta**| 0,56 | 0,96 | 0,99 | 0,92 |
| **MSE-prop** | **Não-Robusta**| 3,00 | 1,15 | 1,03 | 1,41 |
| **MAE** | **Não-Robusta**| 0,45 | 0,95 | 0,99 | 0,83 |

**Incapacidade das Funções Não-Robustas:** O uso de funções como MSE-LOG ou MSE-prop com retornos diários ao quadrado resulta em um viés severo (de 0,28 a 3,00), distorcendo totalmente os testes de avaliação. A função **QLIKE** destaca-se na literatura por apresentar o maior poder estatístico na detecção de modelos incorretos sem gerar viés, mesmo na presença de ruído na proxy.

---

### 7. Sigma Condicional como Input de Regime, Volatility Targeting e Ponte para a Lei Assinada do Janus

#### Volatility Targeting
O $h_t^{1/2}$ estimado serve como mecanismo direto para o controle dinâmico de risco de carteiras. A alocação no ativo arriscado ($w_t$) é ajustada inversamente à volatilidade condicional prevista para manter o risco total constante em um nível meta $\sigma_{\text{target}}$:

$$w_t = \min \left( w_{\max}, \, \frac{\sigma_{\text{target}}}{\sqrt{h_t}} \right)$$

Isso estabiliza a volatilidade do portfólio, reduz a exposição durante episódios de pânico no mercado e aumenta a alocação em momentos de calmaria.

#### Otimização de Portfólio e Estrutura de Engle-Colacito
Na otimização de carteiras de Mínima Variância Global (GMVP):

$$\min_{w_t} w_t' \Sigma_t w_t \quad \text{sujeito a} \quad w_t' \iota = 1 \implies w_t^* = \frac{\Sigma_t^{-1} \iota}{\iota' \Sigma_t^{-1} \iota}$$

Engle e Colacito (2006) provaram que a utilização da matriz de covariância condicional verdadeira $\Sigma_t$ produz a menor variância de portfólio *ex-post* para qualquer vetor de retornos esperados assumido não nulo, validando o uso do $h_t$ condicional como input decisivo de alocação.

#### Mudanças de Regime e Markov-Switching GARCH (MSGARCH)
Para evitar falhas na previsão decorrentes de alterações bruscas no nível incondicional da volatilidade, Ardia et al. (2018), fundamentando-se na formulação de Haas et al. (2004a), especificam modelos MSGARCH nos quais os parâmetros alternam segundo uma cadeia de Markov discreta não observada $s_t \in \{1, \dots, K\}$ com matriz de transição $P$:

$$y_t | (s_t = k, I_{t-1}) \sim D(0, h_{k,t}, \xi_k)$$

$$h_{k,t} = h(y_{t-1}, h_{k,t-1}, \theta_k)$$

Diferente do modelo original de Gray (1996), a abordagem de Haas et al. elimina o problema de dependência do caminho (*path-dependency problem*), permitindo que $K$ processos de volatilidade evoluam em paralelo.

#### Ponte para a Lei Assinada do Janus
A integração de modelos GARCH com a análise de saltos e variação realizada assinada (*realized semivariances*) — conforme detalhado por Patton e Sheppard (2011) — demonstra que a variância futura do mercado é predominantemente impulsionada pela variância de retornos passados negativos ($RV^-$) em vez de positivos ($RV^+$):

$$RV_t = RV_t^+ + RV_t^-$$

Choques negativos geram incrementos duradouros na volatilidade futura, enquanto saltos positivos possuem impacto substancialmente menor ou amortecedor.

---

## Citacões Importantes e Contextualização

### Citação 1: Mincer-Zarnowitz Modificado (MZ-GLS)
> *"Our suggested 'MZ-GLS' test has good size and much better power in finite samples than other MZ tests. The difference between MZ1 and MZ1-GLS was particularly striking when using the daily squared return as a proxy."*
> 
> — **Patton & Sheppard (2007/2008), p. 9-10**

* **Contexto e Aplicação:** As regressões padrão de Mincer-Zarnowitz sofrem de heterocedasticidade grave quando a proxy é o retorno ao quadrado diário, resultando em testes OLS com taxas de rejeição incorretas sob a hipótese nula. A ponderação GLS por $h_t$ padroniza os resíduos, restaurando a homocedasticidade e garantindo um teste estatístico preciso e de alto poder amostragem.

### Citação 2: Supremacia da Perda QLIKE
> *"Amongst the class of robust loss functions for volatility forecast evaluation, and the multivariate generalisation of these loss functions provided in this chapter, our simulations suggest that the 'QLIKE' loss function yields the greatest power."*
> 
> — **Patton & Sheppard (2007/2008), p. 2**

* **Contexto e Aplicação:** Ao avaliar modelos via testes Diebold-Mariano-West, a perda QLIKE não apenas pertence à classe de funções robustas que impedem distorções na ordenação de modelos decorrentes do ruído da proxy, como também atinge a maior capacidade estatística para rejeitar modelos incorretamente especificados.

### Citação 3: Otimização de Portfólio sem Ingerência da Média
> *"The EC framework establishes that the correct covariance will produce a smaller expected portfolio variance for any assumed non-zero vector of means. As a result, evidence of superiority based on ex-post measurements of portfolio variance can be attributed to the covariance forecast."*
> 
> — **Patton & Sheppard (2007/2008), p. 25**

* **Contexto e Aplicação:** A avaliação econômica baseada no arcabouço de Engle-Colacito isola a qualidade da previsão de volatilidade/covariância do erro de estimação do retorno esperado ($\mu$), permitindo comparar modelos diretamente pelo desempenho de variância das carteiras formadas.

---

## Insights Práticos Acionáveis

1. **Adoção do QLIKE como Métrica Padrão de Avaliação:** Em qualquer backtest de modelos de volatilidade, desconsidere métricas como MAE ou MSE-LOG para fins de seleção de modelos. Adote estritamente o QLIKE e o MSE tradicional para garantir ordenações robustas imunes ao ruído da proxy.
2. **Uso Obrigatório de Proxies Intradia em Testes:** Sempre que dados de alta frequência estiverem disponíveis, construa estimadores de volatilidade realizada (como $RV$ de 5 ou 30 minutos) para executar os testes MZ-GLS ou DMW. Isso reduz o tamanho da amostragem necessário para validação do modelo de $T=1000$ para apenas $T=100$ dias.
3. **Incorporação da Assimetria no Dimensionamento de Risco:** Modelos simétricos como o GARCH(1,1) subestimam o risco imediatamente após quedas bruscas de mercado. Utilize GJR-GARCH com inovações Student-$t$ ou modelos MSGARCH de 2 regimes em sistemas de *volatility targeting* para readequar as posições de forma ágil após choques negativos.

---

## Implementação em Python (`arch`) e Checklist Operacional

### Fluxo de Implementação em Python

Abaixo está o padrão de implementação para estimação, diagnóstico e previsão utilizando a biblioteca `arch` em Python:

```python
import numpy as np
import pandas as pd
from arch import arch_model

## 1. Carregamento e Preparação dos Dados (Retornos em Porcentagem)
## y_t representa a série de retornos diários de-meaned
returns = 100 * data['log_returns'].dropna()

## 2. Configuração e Estimação do Modelo GJR-GARCH(1,1) com Inovações Student-t
## p=1, o=1 (efeito alavancagem GJR), q=1, dist='studentst'
model = arch_model(
    returns, 
    mean='Zero', 
    vol='GARCH', 
    p=1, 
    o=1, 
    q=1, 
    dist='studentst'
)
res = model.fit(disp='off', update_freq=0)

## Exibição dos Parâmetros Estimados
print(res.summary())

## 3. Extração dos Sigmas Condicionais e Previsão
conditional_vol = res.conditional_volatility
forecasts = res.forecast(horizon=5)
forecast_var_5d = forecasts.variance.iloc[-1]

## 4. Cálculo da Variância Incondicional e Meia-Vida
pars = res.params
alpha0 = pars['omega']
alpha1 = pars['alpha[1]']
gamma1 = pars['gamma[1]'] # Parâmetro assimétrico do GJR
beta1 = pars['beta[1]']

## Persistência E[alpha + gamma/2 + beta] para Student-t/Normal simétrica
persistence = alpha1 + 0.5 * gamma1 + beta1
unc_variance = alpha0 / (1.0 - persistence)
half_life = np.log(0.5) / np.log(persistence)

print(f"Persistência (k): {persistence:.4f}")
print(f"Volatilidade Incondicional Diária: {np.sqrt(unc_variance):.4f}%")
print(f"Meia-vida do choque: {half_life:.2f} dias")
```

### Checklist Operacional de Laboratório

- [ ] **Limpeza de Dados:** Verificar se a série temporal de retornos foi desprovida de média condicional ($\mathbb{E}[y_t] = 0$) antes da estimação.
- [ ] **Escalonamento:** Multiplicar os retornos por 100 para evitar problemas de convergência numérica nos algoritmos de otimização de verossimilhança.
- [ ] **Validação de Positividade e Estacionariedade:** Confirmar se todos os parâmetros ($\alpha_0, \alpha_1, \beta, \gamma$) cumprem as restrições estritas de positividade e se a persistência $k < 1$.
- [ ] **Análise de Resíduos Padronizados:** Verificar se os resíduos padronizados $\hat{\eta}_t = y_t / \sqrt{h_t}$ não apresentam autocorrelação em seus quadrados (teste Ljung-Box em $\hat{\eta}_t^2$).
- [ ] **Adequação da Distribuição:** Avaliar se a curtose dos resíduos padronizados exige o uso de distribuições de caudas pesadas (Student-$t$ ou GED).
- [ ] **Avaliação via MZ-GLS:** Realizar a regressão MZ-GLS ponderada por $h_t$ e verificar se a hipótese conjunta $\alpha=0 \cap \beta=1$ não é rejeitada.
- [ ] **Aplicações de Risco:** Alimentar os algoritmos de *volatility targeting* e cálculo de Value-at-Risk (VaR) estritamente com as previsões $h_{t+1|t}$ fora da amostra.

---

## Tabela Comparativa de Modelos de Volatilidade

| Modelo | Equação do Processo de Volatilidade | Condição de Positividade | Condição de Estacionariedade | Principal Vantagem |
| :--- | :--- | :--- | :--- | :--- |
| **ARCH(1)** | $h_t = \alpha_0 + \alpha_1 y_{t-1}^2$ | $\alpha_0 > 0, \, \alpha_1 \ge 0$ | $\alpha_1 < 1$ | Simplicidade histórica e intuitiva. |
| **GARCH(1,1)** | $h_t = \alpha_0 + \alpha_1 y_{t-1}^2 + \beta h_{t-1}$ | $\alpha_0 > 0, \, \alpha_1 > 0, \, \beta \ge 0$ | $\alpha_1 + \beta < 1$ | Parcimônia na captura de *clustering* de volatilidade. |
| **GJR-GARCH(1,1)** | $h_t = \alpha_0 + (\alpha_1 + \alpha_2 \mathbb{I}_{\{y_{t-1} < 0\}}) y_{t-1}^2 + \beta h_{t-1}$ | $\alpha_0 > 0, \, \alpha_1 > 0, \, \alpha_2 \ge 0, \, \beta \ge 0$ | $\alpha_1 + \frac{\alpha_2}{2} + \beta < 1$ | Captura o efeito alavancagem de forma direta. |
| **EGARCH(1,1)** | $\ln(h_t) = \alpha_0 + \alpha_1 (\|\eta_{t-1}\| - \mathbb{E}[\|\eta_{t-1}\|]) + \alpha_2 y_{t-1} + \beta \ln(h_{t-1})$ | Garantida automaticamente por $\exp(\ln h_t)$ | $\|\beta\| < 1$ | Flexibilidade sem restrições de sinal nos parâmetros. |
| **TGARCH(1,1)** | $h_t^{1/2} = \alpha_0 + (\alpha_1 \mathbb{I}_{\{y_{t-1} \ge 0\}} - \alpha_2 \mathbb{I}_{\{y_{t-1} < 0\}}) y_{t-1} + \beta h_t^{1/2}$ | $\alpha_0 > 0, \, \alpha_1 > 0, \, \alpha_2 > 0, \, \beta \ge 0$ | Condição funcional sobre a amplitude das inovações | Modela diretamente o desvio padrão condicional. |
| **MSGARCH** | $h_{k,t} = h(y_{t-1}, h_{k,t-1}, \theta_k), \quad s_t \in \{1, \dots, K\}$ | Válida para cada regime $k$ individualmente | Matriz de transição $P$ ergódica + estacionariedade local | Adaptação rápida a mudanças estruturais de regime. |

---

## Glossário Técnico

* **Agrupamento de Volatilidade (*Volatility Clustering*):** Fenômeno empírico em que grandes variações nos preços de ativos são seguidas por grandes variações, e pequenas variações são seguidas por pequenas variações.
* **Caudas Pesadas (*Fat Tails* / Leptocurtose):** Propriedade de distribuições de probabilidade apresentarem probabilidade maior de ocorrência de valores extremos do que a distribuição Normal.
* **Efeito Alavancagem (*Leverage Effect*):** Tendência de choques negativos nos preços gerarem aumentos maiores na volatilidade futura do que choques positivos de igual magnitude.
* **Heterocedasticidade Condicional:** Propriedade de uma série temporal cuja variância não é constante ao longo do tempo, mas sim variante em função das informações passadas.
* **Meia-Vida (*Half-Life*):** Período de tempo necessário para que o impacto de um choque de volatilidade decline até a metade da sua magnitude inicial.
* **Mincer-Zarnowitz Modificado (MZ-GLS):** Teste de otimidade de previsão ajustado por Mínimos Quadrados Generalizados para eliminar a heterocedasticidade gerada pelo uso de proxies de volatilidade.
* **Modelo Markov-Switching GARCH (MSGARCH):** Extensão dos modelos GARCH que permite que os parâmetros alternem entre diferentes estados ou regimes governados por uma cadeia de Markov discreta e latente.
* **Persistência ($k$):** Soma dos coeficientes autorregressivos e de choque de um modelo de volatilidade ($\alpha_1 + \beta$), mensurando a velocidade com que a volatilidade retorna à sua média incondicional.
* **Proxy de Volatilidade:** Variável observável *ex-post* (como retornos ao quadrado ou volatilidade realizada intradia) utilizada para aproximar a volatilidade condicional latente e não observável.
* **Quasi-Likelihood (QLIKE):** Função de perda estatisticamente robusta e de elevado poder, utilizada para comparar modelos de previsão de volatilidade de forma imune a ruídos na proxy.
* **Volatilidade Realizada ($RV$):** Estimador não-paramétrico de volatilidade construído a partir do somatório de retornos intradia ao quadrado amostrados em frequências elevadas.
* **Volatility Targeting:** Estratégia de gestão de carteiras na qual a exposição aos ativos arriscados é ajustada inversamente à volatilidade condicional prevista para manter o risco global do portfólio pré-fixado.