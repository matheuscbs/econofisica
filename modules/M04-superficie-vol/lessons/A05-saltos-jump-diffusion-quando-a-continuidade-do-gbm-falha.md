<!-- imported from vault study notes; curated for open course -->
# M04.A05 — Saltos (jump-diffusion): quando a continuidade do GBM falha

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M04
> **Aula:** M04.A05

↑ M04 · Resumo · Completo

**Módulo:** M04
**Pergunta do módulo:** Como ler, sanitizar e modelar a superfície de volatilidade?

## Conceito-núcleo
Merton/jump-diffusion: descontinuidades; caudas e skew além de difusão pura.

## Aplicação em mercado / trading
Precificar risco de gap/crash; hedgear o que delta contínuo não cobre em saltos.

## Entregável / lab
Comparar densidades GBM vs jump-diffusion; impacto no preço OTM e no hedge residual.

## Fonte (mapeamento)
quantitative-trading-free-lesson/16 jump-diffusion-models

## Guia de estudo aprofundado

> **info**
>

Este guia de estudo aborda a transição dos modelos de difusão contínua (como o Movimento Browniano Geométrico) para os modelos de salto e difusão (*jump-diffusion*), focando nas formulações de Merton e Kou, na compensação de deriva sob a medida de risco-neutro, no comportamento do *smile* de volatilidade de curto prazo e na implementação numérica estável.

---

### Conceitos-Chave e Fundamentação Teórica

#### Limitações do Movimento Browniano Geométrico (GBM)
O GBM assume trajetórias contínuas para o preço dos ativos. Em prazos muito curtos (curto *maturity*), a incerteza gerada por uma difusão pura acumula-se de forma contínua e proporcional a $\sqrt{\Delta t}$. Consequentemente, difusões puras encontram severas dificuldades para gerar convexidade instantânea e volatilidades implícitas elevadas para opções fora-do-preço (*OTM - Out of the Money*) de curto prazo sem adotar parâmetros não físicos ou artificiais.

#### A Mecânica dos Modelos Jump-Diffusion
Os modelos de *jump-diffusion* combinam uma difusão contínua de Black-Scholes com um processo de Poisson composto para capturar choques discretos e abruptos no preço do ativo subjacente:
* **Eventos Pontuais:** Ocorrem com uma taxa de intensidade $\lambda$. A probabilidade de ocorrência de um salto em um horizonte curto $T$ é de primeira ordem $\lambda T$.
* **Impacto Imediato:** Um único salto é capaz de mover o ativo subjacente de maneira descontínua, alterando instantaneamente a precificação e a demanda por opções OTM, elevando o preço das asas (*wings*) do *smile*.

#### Compensação de Deriva sob a Medida de Risco-Neutro ($\mathbb{Q}$)
Para que o processo de preço descontado seja um martingal sob a medida de risco-neutro $\mathbb{Q}$, o parâmetro de deriva (*drift*) da parte contínua precisa ser explicitamente corrigido. A inclusão de saltos introduz uma expectativa de variação percentual média representada por $\kappa_J = \mathbb{E}[e^Y - 1]$, onde $Y = \ln J$ é o tamanho do salto no espaço logarítmico.
* **Deriva Compensada:** A fórmula do *drift* discreto torna-se:
  $$\text{drift} = \left(r - q - \lambda \kappa_J - \frac{1}{2}\sigma^2\right) \Delta t$$
* **Importância:** Se o termo de compensação $-\lambda \kappa_J$ for omitido, o processo perde sua neutralidade ao risco. Como consequência, o valor esperado do preço no vencimento violará a condição de não arbitragem:
  $$\mathbb{E}_\mathbb{Q}[S_T] = S_0 e^{(r-q)T}$$

#### Comparação entre os Modelos Merton vs. Kou
A especificação da lei de probabilidade do tamanho do salto $Y = \ln J$ define as propriedades do *smile* e da assimetria (*skew*):

| Característica | Modelo de Merton | Modelo de Kou |
| :--- | :--- | :--- |
| **Distribuição do Salto Log ($Y$)** | Normal: $Y \sim \mathcal{N}(\mu_J, \delta^2)$ | Exponencial Dupla (assimétrica) |
| **Mecanismo de Salto** | Média $\mu_J$ e desvio-padrão $\delta$. | Probabilidade $p$ de salto positivo (parâmetro $\eta_1$) e $1-p$ de salto negativo (parâmetro $\eta_2$). |
| **Compensador ($\kappa_J$)** | $e^{\mu_J + \frac{1}{2}\sigma_J^2} - 1$ | $p \frac{\eta_1}{\eta_1-1} + (1-p) \frac{\eta_2}{\eta_2+1} - 1$ |
| **Formato do Smile** | Curvatura pronunciada nas asas (*wings*), gerando um *smile* simétrico (a menos que $\mu_J$ seja fortemente deslocado). | Assimetria direta e ajustável. Permite controlar o *skew* de baixa separadamente da asa de alta. |
| **Cauda Esquerda** | Controlada pelo deslocamento de $\mu_J$. | Fortemente expressa reduzindo $\eta_2$ (deixa a cauda esquerda mais pesada). |

#### Ausência de Memória vs. Volatilidade Estocástica (Heston)
Nos modelos de *jump-diffusion*, os saltos introduzem massa imediata nas caudas das distribuições, mas **não criam memória**. Ocorrido um salto no instante $t$, a dinâmica do processo não mantém uma persistência do choque para os instantes posteriores (ausência de *volatility clustering*). Isso contrasta com modelos como o de Heston, em que a variância é uma variável de estado estocástica com reversão à média, gerando contaminação e persistência ao longo do tempo.

---

### Formulário Matemático e Dinâmica Numérica

#### Atualização Contínua e Discreta no Espaço Logarítmico
A evolução temporal do log-preço $\ln S_t$ é estritamente aditiva, o que garante estabilidade numérica superior ao evitar multiplicações diretas de sequências de saltos no preço *spot*:

$$\ln S_{t+\Delta t} = \ln S_t + \left(r - q - \lambda \kappa_J - \frac{1}{2}\sigma^2\right)\Delta t + \sigma\sqrt{\Delta t}\,Z + \sum_{k=1}^{N} Y_k$$

Onde:
* $Z \sim \mathcal{N}(0, 1)$ é uma variável normal padrão.
* $N \sim \text{Poisson}(\lambda \Delta t)$ é o número de saltos gerados no intervalo $\Delta t$.
* $Y_k$ é a amplitude do $k$-ésimo salto em escala logarítmica.

#### Compensadores de Salto ($\kappa_J$)
* **Merton:**
  $$\kappa_J = \mathbb{E}[e^Y - 1] = e^{\mu_J + \frac{1}{2}\sigma_J^2} - 1$$
* **Kou:**
  $$\mathbb{E}[e^Y] = p\frac{\eta_1}{\eta_1-1} + (1-p)\frac{\eta_2}{\eta_2+1}$$
  $$\kappa_J = \mathbb{E}[e^Y] - 1$$

#### Extração da Volatilidade Implícita por Bissecção
Para converter os preços gerados pelo modelo de *jump-diffusion* na linguagem tradicional de superfície de volatilidade ($\sigma_{\text{impl}}(K,T)$), aplica-se a inversão da fórmula de Black-Scholes via método da bissecção:
1. A função de preço de uma opção de compra de Black-Scholes $C_{BS}(\sigma)$ é estritamente crescente em relação à volatilidade $\sigma$.
2. O método busca um intervalo estável para determinar o valor de $\sigma$ tal que $C_{BS}(\sigma) - C_{\text{modelo}} = 0$.

---

### Intuição de Mercado e Trading

#### Comportamento do Smile de Curto Prazo
Em vencimentos extremamente curtos ($T \to 0$), a componente de difusão de uma ação ou índice tem pouca variância acumulada ($\sigma \sqrt{T}$ é reduzido). Sem saltos, as opções OTM seriam cotadas a preços irrisórios. 

Com a introdução de saltos, a probabilidade de um choque pontual $\lambda T$ garante valor substancial para opções OTM, elevando a volatilidade implícita nas pontas do *strike*.

#### Sensibilidade dos Parâmetros e Impacto na Superfície

* **Aumento de $\lambda$ (Frequência de Saltos):** Aumenta a frequência de riscos descontínuos; eleva ambas as asas (*wings*) da superfície de volatilidade simultaneamente.
* **Aumento de $\delta$ ou $\sigma_J$ em Merton (Dispersão do Salto):** Amplia a variabilidade dos tamanhos dos saltos, tornando os eventos extremos mais caros e elevando ainda mais o preço das opções muito fora-do-preço.
* **Redução de $\mu_J$ em Merton (Média de Salto Negativa):** Desloca a massa dos saltos para baixo, acentuando a inclinação negativa do *skew* (puts OTM ficam mais caras que calls OTM).
* **Redução de $\eta_2$ em Kou (Parâmetro da Cauda de Baixa):** Torna a cauda esquerda do log-preço mais pesada, encarecendo diretamente as puts OTM e gerando um *skew* de baixa mais íngreme.
* **Redução de $p$ em Kou (Probabilidade de Saltos de Baixa):** Torna os saltos negativos mais frequentes do que os positivos, aumentando a inclinação negativa do *skew*.

---

### Exemplo Numérico Resolvido Passo a Passo

#### Cenário de Aplicação
Considere os seguintes parâmetros para um modelo de Merton Jump-Diffusion em um horizonte de tempo de $\Delta t = 1,0$ ano:
* Preço inicial do ativo ($S_0$): $100,00
* Taxa livre de risco ($r$): $5\%$ ao ano ($0,05$)
* Taxa de dividendos ($q$): $2\%$ ao ano ($0,02$)
* Volatilidade contínua ($\sigma$): $20\%$ ao ano ($0,20$)
* Intensidade de saltos ($\lambda$): $1,0$ salto por ano
* Média do log-salto ($\mu_J$): $-0,05$
* Desvio-padrão do log-salto ($\sigma_J$): $0,10$

#### Passo 1 Calcular o Compensador de Salto de Merton ($\kappa_J$)
Aplicando a fórmula:
$$\kappa_J = e^{\mu_J + \frac{1}{2}\sigma_J^2} - 1$$

Calculando o expoente:
$$\mu_J + \frac{1}{2}\sigma_J^2 = -0,05 + \frac{1}{2}(0,10)^2 = -0,05 + 0,005 = -0,045$$

Calculando o valor do compensador:
$$e^{-0,045} \approx 0,955997$$
$$\kappa_J = 0,955997 - 1 = -0,044003$$

#### Passo 2 Calcular a Deriva Compensada ($\text{drift}$)
A deriva sob a medida de risco-neutro é dada por:
$$\text{drift} = \left(r - q - \lambda \kappa_J - \frac{1}{2}\sigma^2\right)\Delta t$$

Substituindo os valores numéricos:
$$r - q = 0,05 - 0,02 = 0,03$$
$$-\lambda \kappa_J = -1,0 \times (-0,044003) = +0,044003$$
$$-\frac{1}{2}\sigma^2 = -0,5 \times (0,20)^2 = -0,02$$

Somando os componentes para $\Delta t = 1,0$:
$$\text{drift} = (0,03 + 0,044003 - 0,02) \times 1,0 = 0,054003$$

#### Passo 3 Verificação da Propriedade Martingal para o Valor Esperado Teórico
A condição de martingal sob $\mathbb{Q}$ exige que o preço esperado no vencimento atenda a:
$$\mathbb{E}_\mathbb{Q}[S_T] = S_0 e^{(r-q)T} = 100 \times e^{(0,05 - 0,02) \times 1,0} = 100 \times e^{0,03} \approx 103,0455$$

Se a compensação $-\lambda \kappa_J$ fosse erroneamente omitida da deriva, o valor do termo de deriva contínua seria apenas $0,03 - 0,02 = 0,01$. Ao adicionar a expectativa não compensada dos saltos, a média da simulação iria desviar-se do alvo risco-neutro $103,0455$, gerando precificações incorretas e oportunidades fictícias de arbitragem.

---

### Armadilhas Comuns de Modelagem

1. **Omissão da Deriva Compensada ($-\lambda \kappa_J$):**
   * *Erro:* Esquecer de subtrair o termo $\lambda \kappa_J$ na equação da deriva.
   * *Consequência:* O processo simulado perde a propriedade de martingal sob a medida $\mathbb{Q}$. A média dos preços simulados $\mathbb{E}[S_T]$ divergirá de $S_0 e^{(r-q)T}$, invalidando a precificação de qualquer derivativo.

2. **Simulação Direta no Nível do Preço em Vez do Espaço Logarítmico:**
   * *Erro:* Multiplicar iterativamente os preços $S_t$ por fatores de salto $(1 + J_k)$ em cada passo.
   * *Consequência:* Instabilidade numérica e acúmulo de erros de arredondamento. A abordagem correta e estável evolui o processo somando os termos no espaço logarítmico ($\ln S_t$).

3. **Confundir Dinâmica de Salto com Volatilidade Estocástica / Memória:**
   * *Erro:* Esperar que um modelo de *jump-diffusion* puro simule agrupamentos de volatilidade (*volatility clustering*).
   * *Consequência:* Os saltos geram caudas pesadas instantâneas, mas são eventos independentes e pontuais sem persistência contínua na variância do ativo.

4. **Calibração Inadequada para Vencimentos Longos versus Curtos:**
   * *Erro:* Utilizar modelos de salto na esperança de capturar a dinâmica de superfícies de volatilidade de longo prazo sem ajustar a parte de variância estocástica.
   * *Consequência:* Os saltos dominam o comportamento da superfície no curto prazo ($T \to 0$), mas seu efeito no *smile* dilui-se à medida que $T$ cresce devido ao Teorema do Limite Central.

---

### Laboratório Prático Sugerido em Python

O laboratório prático tem como objetivo implementar o simulador Monte Carlo terminal para modelos de *jump-diffusion* mantendo a arquitetura genérica e modular.

#### Roteiro de Implementação em Passos

* **Passo 1: Implementar o Inversor de Volatilidade Implícita de Black-Scholes**
  * Criar uma função de preço de opção de compra de Black-Scholes `bs_call(S, K, r, q, T, sigma)`.
  * Criar a função `implied_vol_call(price, S, K, r, q, T)` utilizando o algoritmo de bissecção para encontrar a volatilidade implícita de forma estável.

* **Passo 2: Implementar os Calculadores de Compensação ($\kappa_J$)**
  * Criar a função `merton_kappa(mu_J, sigma_J)` que retorna $e^{\mu_J + 0.5 \sigma_J^2} - 1$.
  * Criar a função `kou_kappa(p, eta1, eta2)` que retorna $p \frac{\eta_1}{\eta_1 - 1} + (1-p) \frac{\eta_2}{\eta_2 + 1} - 1$.

* **Passo 3: Construir os Amostradores do Salto Acumulado (`sample_jump_logsum`)**
  * Para Merton (`sample_merton_lnJ_sum`):
    1. Sortear $N \sim \text{Poisson}(\lambda \Delta t)$.
    2. Se $N > 0$, somar $N$ variáveis aleatórias extraídas de $\mathcal{N}(\mu_J, \delta^2)$. Caso contrário, retornar $0$.
  * Para Kou (`sample_kou_Y`):
    1. Sortear $N \sim \text{Poisson}(\lambda \Delta t)$.
    2. Para cada salto, decidir com probabilidade $p$ se é de alta ou baixa.
    3. Sortear a magnitude a partir de uma distribuição exponencial com parâmetro $\eta_1$ (alta) ou $\eta_2$ (baixa).

* **Passo 4: Desenvolver o Motor Monte Carlo Terminal (`jd_mc_terminal`)**
  * Calcular a deriva compensada: `drift = (r - q - lam * kappa_J - 0.5 * sigma**2) * dt`.
  * Atualizar o vetor de trajetórias no espaço logarítmico: `logS = logS + drift + sigma * sqrt(dt) * Z + lnJ_sum`.
  * Obter os preços finais fazendo $S_T = \exp(\text{logS})$.

* **Passo 5: Executar o Teste do Martingal (Martingale Check)**
  * Simular $N_{\text{sim}} = 100.000$ trajetórias para um prazo $T = 1.0$.
  * Calcular a média dos preços simulados $\bar{S}_T = \frac{1}{N_{\text{sim}}} \sum S_T$.
  * Comparar com a meta teórica $S_0 e^{(r-q)T}$.
  * Validar que a diferença entre a média simulada e a meta seja estatisticamente desprezível.

* **Passo 6: Mapeamento do Smile de Volatilidade**
  * Precificar opções de compra para uma grade de *strikes* $K$.
  * Passar os preços obtidos pelo inversor `implied_vol_call` para extrair e plotar a curva de volatilidade implícita $\sigma_{\text{impl}}(K)$.

---

### Glossário

* **Amostrador de Salto (*Sampler*):** Módulo estocástico responsável por sortear a quantidade de saltos de um processo de Poisson e calcular a soma dos seus impactos no espaço logarítmico.
* **Compensador de Deriva ($\lambda \kappa_J$):** Termo subtraído do parâmetro de deriva da difusão para neutralizar a expectativa do impacto dos saltos e manter a propriedade de martingal sob $\mathbb{Q}$.
* **Inversão por Bissecção:** Algoritmo numérico robusto que encontra a volatilidade implícita de Black-Scholes igualando o preço do modelo ao preço analítico de BS.
* **Modelo de Kou:** Modelo de *jump-diffusion* em que o log-tamanho do salto segue uma distribuição exponencial dupla, permitindo controle direto e assimétrico das caudas.
* **Modelo de Merton:** Modelo de *jump-diffusion* pioneiro em que o log-tamanho do salto segue uma distribuição normal, gerando *smiles* simétricos com asas elevadas.
* **Smile de Curto Prazo (*Front-End Smile*):** Formato acentuado e flectido da volatilidade implícita observada em opções com vencimentos muito curtos, gerado pela presença de choques discretos.
* **Volatility Clustering (Agrupamento de Volatilidade):** Fenômeno em que dias de alta volatilidade são seguidos por alta volatilidade. É uma propriedade presente no modelo de Heston, mas **ausente** em modelos puros de *jump-diffusion*.

---

### Questões de Prática e Avaliação

#### Nível 1 Questões Curtas (Conceituais e Diretas)

**Questão 1:** Qual é a função exata do termo $-\lambda \kappa_J$ na equação de deriva do modelo de *jump-diffusion*?  
**Resposta:** O termo compensa o valor esperado das variações percentuais geradas pelos saltos descontínuos sob a medida de risco-neutro $\mathbb{Q}$, garantindo que a expectativa do preço no vencimento seja $\mathbb{E}_\mathbb{Q}[S_T] = S_0 e^{(r-q)T}$ e preservando a propriedade de martingal.

**Questão 2:** Por que é recomendável atualizar as trajetórias de simulação do modelo de *jump-diffusion* no espaço logarítmico ($\ln S_t$) em vez do espaço original do preço ($S_t$)?  
**Resposta:** Porque no espaço logarítmico a difusão e os saltos tornam-se estritamente aditivos. Isso evita multiplicações sucessivas no nível do preço, resultando em maior estabilidade numérica e prevenindo erros de arredondamento.

**Questão 3:** Como o modelo de Kou gera assimetria (*skew*) de baixa na superfície de volatilidade de forma mais direta do que o modelo de Merton?  
**Resposta:** O modelo de Kou utiliza uma distribuição exponencial dupla para o tamanho dos saltos, permitindo ajustar parâmetros independentes para saltos de alta e de baixa. Ao reduzir o parâmetro $\eta_2$ ou diminuir a probabilidade $p$, a cauda esquerda (saltos negativos) torna-se mais pesada de forma direta.

---

#### Nível 2 Questões Intermediárias (Análise e Aplicação)

**Questão 4:** Um analista roda uma simulação Monte Carlo para o modelo de Merton Jump-Diffusion e obtém uma média para os preços terminais $E[S_T]$ significativamente maior do que o valor teórico de não arbitragem $S_0 e^{(r-q)T}$. Qual é a causa numérica primária desse problema e como corrigi-la?  
**Resposta:** A causa primária é a omissão ou o cálculo incorreto da deriva compensada ($-\lambda \kappa_J$). O analista provavelmente utilizou a deriva padrão do Black-Scholes sem deduzir o termo de compensação dos saltos. A correção exige recalcular $\kappa_J = e^{\mu_J + \frac{1}{2}\sigma_J^2} - 1$ e atualizar a deriva discreta para $\left(r - q - \lambda \kappa_J - \frac{1}{2}\sigma^2\right)\Delta t$.

**Questão 5:** Explique por que difusões puras contínuas (como o Movimento Browniano Geométrico) falham em reproduzir a precificação de opções OTM em vencimentos muito curtos ($T \to 0$), enquanto os modelos de *jump-diffusion* são bem-sucedidos.  
**Resposta:** Em difusões puras, a incerteza acumula-se de forma contínua proporcional a $\sqrt{T}$. Quando $T \to 0$, a variância acumulada tende a zero, fazendo com que a probabilidade de atingir *strikes* OTM caia drasticamente. Já o modelo de *jump-diffusion* possui uma probabilidade de salto de primeira ordem igual a $\lambda T$. Mesmo com $T$ muito pequeno, um único salto descontínuo pode mover o ativo imediatamente para a região OTM, conferindo valor real e elevando a volatilidade implícita nessas pontas.

---

#### Nível 3 Questões Discursivas e de Análise Profunda

**Questão 6:** Compare a dinâmica estrutural de um modelo de volatilidade estocástica (como Heston) com a de um modelo de *jump-diffusion* (como Merton) no que tange ao comportamento das asas da superfície de volatilidade e à presença de memória nos choques de mercado.  
**Resposta:** 
* **Superfície de Volatilidade:** Ambos os modelos conseguem gerar curvatura nas asas (*wings*) do *smile*. No entanto, o modelo de *jump-diffusion* domina o comportamento do curto prazo (*front-end*), pois um salto produz convexidade instantânea em vencimentos curtos. O modelo de Heston precisa de tempo para a volatilidade evoluir estocasticamente, sendo mais eficaz em prazos intermediários e longos.
* **Memória e Agrupamento de Volatilidade:** No modelo de Heston, a variância é uma variável de estado contínua com reversão à média. Um choque de volatilidade no instante $t$ contamina e eleva a volatilidade dos períodos subsequentes, gerando *volatility clustering*. No modelo de *jump-diffusion*, os saltos são eventos pontuais e independentes governados por um processo de Poisson. Um salto altera o nível do ativo no momento em que ocorre, mas não deixa "memória" ou persistência na variância futura do processo.

**Questão 7:** Descreva como os parâmetros $\lambda$, $\delta$ e $\mu_J$ do modelo de Merton atuam como "testes de mecanismo" na alteração do formato da superfície de volatilidade implícita.  
**Resposta:** 
* **Intensidade ($\lambda$):** Atua no aumento da frequência do risco descontínuo. Elevar $\lambda$ adiciona massa global às caudas da distribuição terminal, fazendo com que as volatilidades implícitas de ambas as asas (*put OTM* e *call OTM*) subam simultaneamente.
* **Dispersão ($\delta$ ou $\sigma_J$):** Determina a variabilidade do tamanho dos saltos. O aumento de $\delta$ espalha os resultados dos saltos para valores mais extremos, encarecendo opções muito fora-do-preço e aumentando a curvatura (*wings*) da superfície.
* **Média do Log-Salto ($\mu_J$):** Controla a direção média do choque. Tornar $\mu_J$ mais negativo desloca a distribuição de saltos para baixo. Isso aumenta a assimetria negativa da distribuição terminal, tornando as puts OTM proporcionalmente mais caras que as calls OTM e gerando um *skew* de volatilidade com inclinação negativa.