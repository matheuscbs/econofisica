<!-- imported from vault study notes; curated for open course -->
# M04.A04 — Heston e Monte Carlo: origem do smile com vol estocástica

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M04
> **Aula:** M04.A04

↑ M04 · Resumo · Completo

**Módulo:** M04
**Pergunta do módulo:** Como ler, sanitizar e modelar a superfície de volatilidade?

## Conceito-núcleo
Heston: vol média-reversível; MC como motor de precificação; smile como efeito da vol estocástica.

## Aplicação em mercado / trading
Calibrar/interpretar smile sem forçar local vol; stress de parâmetros (κ, θ, ξ, ρ) no book.

## Entregável / lab
Simulação MC Heston: paths de S e v; smile gerado vs vanila BSM flat.

## Fonte (mapeamento)
quantitative-trading-free-lesson/15 the-heston-model-monte-carlo-mechanics-and-the-origin-of-the-smile

## Guia de estudo aprofundado

> **info**
>

Este guia de estudo foi concebido para fornecer uma análise detalhada da origem do *smile* de volatilidade por meio de modelos de volatilidade estocástica, focando na mecânica de discretização do Modelo de Heston via simulação de Monte Carlo, na gramática de seus parâmetros e na comparação com modelos de volatilidade local.

---

### Visão Geral e Conceitos-Chave

#### A Origem do Volatility Smile via Volatilidade Estocástica
No modelo tradicional de Black-Scholes, a volatilidade é assumida como constante. No entanto, no mercado real, as opções negociadas para diferentes preços de exercício (*strikes*) e vencimentos apresentam volatilidades implicitas distintas, gerando uma estrutura conhecida como *smile* ou *skew* de volatilidade.

No Modelo de Heston, o *smile* de volatilidade não é introduzido por meio de interpolação ou ajuste arbitrário, mas emerge mecanicamente do fato de que a volatilidade possui sua própria fonte de ruído e evolui no tempo como um fator de estado. A volatilidade instantânea muda ao longo do caminho de simulação do ativo subjacente (*spot*). Se a variância se eleva após um choque, os movimentos subsequentes do *spot* tornam-se mecanicamente mais acentuados. O *smile* nasce da dinâmica estocástica conjunta entre o preço do ativo e sua volatilidade.

#### A Mecânica Numérica do Modelo de Heston no Monte Carlo
A simulação de Monte Carlo sob o modelo de Heston exige a discretização rigorosa do sistema de Equações Diferenciais Estocásticas (SDEs). A discretização deve preservar as propriedades estruturais do modelo contínuo:

1. **Correlação de Processos Brownianos**: O modelo possui dois movimentos brownianos correlacionados:
   $dW_t^S dW_t^v = \rho\,dt$
   Na simulação discreta, sorteiam-se duas variáveis normais padronizadas independentes, $Z_1$ e $Z_2 \sim N(0,1)$, e constroem-se os incrementos correlacionados via decomposição estrutural:
   $dW_S = \sqrt{\Delta t} \cdot Z_1$
   $dW_v = \sqrt{\Delta t} \cdot (\rho Z_1 + \sqrt{1.0 - \rho^2} Z_2)$

2. **Garantia de Positividade e Truncamento Total (*Full Truncation*)**: No mundo contínuo, o processo de Cox-Ingersoll-Ross (CIR) que governa a variância possui uma estrutura de positividade. Porém, em máquinas de precisão finita usando esquemas numéricos como o de Euler, choques discretos podem tornar a variância $v$ negativa. Como $\sqrt{v}$ não é definida para $v < 0$, o algoritmo falha abruptamente. A solução numérica de segurança é a aplicação da variância efetiva $v_{\mathrm{eff}} = \max(v, 0.0)$ tanto no drift quanto no termo de difusão, seguida de um ajuste ao final do passo $v = \max(v, 0.0)$.

3. **Atualização do Spot (Log-Euler)**: O preço do ativo subjacente é atualizado utilizando a estrutura log-normal discreta:
   $S_{t+\Delta t} = S_t \cdot \exp\left( (r - q - 0.5 \cdot v_{\mathrm{eff}}) \Delta t + \sqrt{v_{\mathrm{eff}}} \, dW_S \right)$

4. **Inversão de Black-Scholes como Termômetro**: A função de precificação de Black-Scholes não é utilizada para redefinir o preço do modelo de Heston. O Monte Carlo gera o preço descontado da opção. Em seguida, utiliza-se a inversão estável da fórmula de Black-Scholes (por exemplo, via método da bisseção) para reexpressar o preço obtido em termos de volatilidade implícita. O modelo de Black-Scholes atua estritamente como um "termômetro" para traduzir preços em superfícies de volatilidade.

#### Gramática dos Parâmetros do Modelo de Heston
Cada parâmetro do modelo de Heston controla um aspecto geométrico específico da superfície de volatilidade:

| Parâmetro | Descrição Matemática / Mecânica | Efeito na Superfície de Volatilidade |
| :--- | :--- | :--- |
| $v_0$ | Variância instantânea inicial ($v_t$ em $t=0$). | Eleva ou reduz o nível de volatilidade implícita do curto prazo (curto vencimento). Para prazos extremamente curtos, a volatilidade implícita no dinheiro (ATM) aproxima-se de $\sqrt{v_0}$. |
| $\theta$ | Média de longo prazo da variância (*long-term mean*). | Altera o nível base da superfície nos prazos mais longos (*long-end*), atuando como a âncora para onde a variância converge. |
| $\kappa$ | Velocidade de reversão à média (*mean reversion speed*). | Define a rapidez com que a volatilidade esquece o valor inicial $v_0$ e retorna a $\theta$. Não cria *smile* por si só, mas acelera a transição temporal da superfície. |
| $\xi$ | Volatilidade da variância (*vol-of-vol*). | Injeta aleatoriedade diretamente no processo de variância. Aumenta a convexidade da distribuição terminal, aprofundando o *smile* (eleva as asas em relação ao centro). |
| $\rho$ | Correlação entre os incrementos brownianos do ativo e da variância. | Governa a assimetria (*skew*). Quando $\rho < 0$, choques negativos no preço coincidem com aumentos na variância, encarecendo opções de venda (puts) e ajustando a inclinação típica de renda variável (*equity skew*). |

#### Heston vs. Volatilidade Local
A diferença entre o Modelo de Heston e os Modelos de Volatilidade Local é conceitual e filosófica:

* **Volatilidade Local**: A superfície de volatilidade observada no mercado é a **entrada** (*input*). O modelo reconstrói uma difusão determinística para reproduzir perfeitamente os preços de *vanillas* em $t=0$. Contudo, a dinâmica futura da volatilidade é altamente restrita e artificial.
* **Modelo de Heston**: A difusão paramétrica de dois fatores (ativo e variância) é a **entrada** (*input*). A superfície de volatilidade resultante é a **saída** (*output*). Embora o modelo perca a capacidade de se ajustar perfeitamente ponto a ponto a todas as opções do mercado, ele ganha uma dinâmica estocástica coerente com conteúdo econômico real (reversão à média, efeito alavancagem e *vol-of-vol*).

---

### Intuição de Mercado e Trading

#### O Efeito Alavancagem e a Leitura de Skew
No mercado de ações (*equities*), é comum observar que quedas no preço de um ativo são acompanhadas por picos de volatilidade. Esse fenômeno é capturado diretamente no modelo de Heston pela correlação negativa ($\rho < 0$).
Quando $\rho < 0$:
* Uma queda no *spot* ($dW_S < 0$) injeta simultaneamente um impulso positivo na variância ($dW_v > 0$).
* O aumento da variância faz com que a cauda esquerda da distribuição fique mais pesada.
* Mercadologicamente, as opções *Out-of-the-Money* (OTM) de venda (puts / *strikes* baixos) tornam-se mais caras do que as opções de compra (calls / *strikes* altos), gerando a inclinação ascendente à esquerda no gráfico de volatilidade versus *strike*.

#### Convexidade e Volatilidade da Volatilidade (*Vol-of-Vol*)
O parâmetro $\xi$ funciona como o motor gerador de caudas gordas e convexidade. Se a variância for constante ou tiver $\xi = 0$, a distribuição do log-retorno terminal é normal e o *smile* colapsa em uma linha reta horizontal. Conforme $\xi$ aumenta, a volatilidade sofre variações bruscas, espalhando a distribuição dos preços terminais do *spot*. Isso amplia o valor das opções que estão muito fora do dinheiro nas duas pontas (*wings*), aprofundando o formato em "U" do *smile*.

---

### Formulacao Matematica Essencial

#### Sistema de Equações Diferenciais Estocásticas (SDEs)
No modelo contínuo de Heston, a dinâmica do preço do ativo $S_t$ e da sua variância instantânea $v_t$ sob a medida de risco neutro é expressa por:

$dS_t = (r - q) S_t dt + \sqrt{v_t} S_t dW_t^S$

$dv_t = \kappa (\theta - v_t) dt + \xi \sqrt{v_t} dW_t^v$

Com correlação instantânea dada por:

$dW_t^S dW_t^v = \rho\,dt$

Onde $r$ é a taxa livre de risco e $q$ é a taxa de dividendos.

#### Média Esperada da Variância
A expectativa condicional da variância no tempo $t$, dado o seu valor inicial $v_0$, possui solução analítica exata:

$E[v_t \mid v_0] = \theta + (v_0 - \theta)e^{-\kappa t}$

Esta relação é utilizada como teste de integridade (*sanity check*) do esquema numérico da simulação.

#### Condição de Feller
Para garantir que a variância $v_t$ permaneça estritamente maior que zero ($v_t > 0$) no regime contínuo, os parâmetros do modelo devem satisfazer a Condição de Feller:

$2\kappa\theta \ge \xi^2$

Se a condição de Feller for violada ($2\kappa\theta < \xi^2$), o processo de variância pode tocar a origem $0$. Na simulação discreta em computador, mesmo que a condição seja satisfeita analiticamente, o ruído discretizado pode forçar $v < 0$, tornando indispensável o uso de salvaguardas numéricas como $v_{\mathrm{eff}} = \max(v, 0.0)$.

---

### Exemplo Numérico Resolvido Passo a Passo

Considere um único passo de tempo no modelo de Heston com os seguintes parâmetros de mercado e de simulação:

* **Parâmetros do Ativo e Mercado**: $S_0 = 100$, $r = 0{,}05$, $q = 0{,}02$
* **Parâmetros de Heston**: $v_0 = 0{,}04$, $\kappa = 2{,}0$, $\theta = 0{,}04$, $\xi = 0{,}3$, $\rho = -0{,}7$
* **Passo de Tempo**: $\Delta t = \frac{1}{252} \approx 0{,}00396825$ (1 dia útil)
* **Variáveis Normais Sorteadas**: $Z_1 = -0{,}50$, $Z_2 = 0{,}80$

Objetivo: Calcular o valor do *spot* $S_1$ e da variância $v_1$ após um passo de tempo.

#### Passo 1 Calcular os Incrementos Brownianos Correlacionados
Primeiro, calcula-se $\sqrt{\Delta t}$:
$\sqrt{\Delta t} = \sqrt{0{,}00396825} \approx 0{,}062994$

Incremento para o *spot* ($dW_S$):
$dW_S = \sqrt{\Delta t} \cdot Z_1 = 0{,}062994 \cdot (-0{,}50) = -0{,}031497$

Incremento para a variância ($dW_v$):
$dW_v = \sqrt{\Delta t} \cdot \left( \rho Z_1 + \sqrt{1.0 - \rho^2} Z_2 \right)$
$\sqrt{1.0 - (-0{,}7)^2} = \sqrt{1.0 - 0{,}49} = \sqrt{0{,}51} \approx 0{,}714143$
$\rho Z_1 + \sqrt{1 - \rho^2} Z_2 = (-0{,}70) \cdot (-0{,}50) + 0{,}714143 \cdot 0{,}80 = 0{,}35 + 0{,}571314 = 0{,}921314$
$dW_v = 0{,}062994 \cdot 0{,}921314 \approx 0{,}058037$

#### Passo 2 Variância Efetiva e Atualização da Variância ($v_1$)
Determinar a variância efetiva inicial $v_{\mathrm{eff}} = \max(v_0, 0.0) = \max(0{,}04, 0.0) = 0{,}04$.

Calcular a nova variância $v_1$:
$v_1 = v_0 + \kappa(\theta - v_{\mathrm{eff}})\Delta t + \xi \sqrt{v_{\mathrm{eff}}} dW_v$
$v_1 = 0{,}04 + 2{,}0 \cdot (0{,}04 - 0{,}04) \cdot 0{,}00396825 + 0{,}3 \cdot \sqrt{0{,}04} \cdot 0{,}058037$
$v_1 = 0{,}04 + 0{,}0 + 0{,}3 \cdot 0{,}20 \cdot 0{,}058037$
$v_1 = 0{,}04 + 0{,}0034822 = 0{,}0434822$

Aplicar a trava de segurança final:
$v_1 = \max(0{,}0434822, 0.0) = 0{,}0434822$

#### Passo 3 Atualização do Preço do Ativo ($S_1$)
Aplicar o esquema Log-Euler utilizando a variância efetiva $v_{\mathrm{eff}} = 0{,}04$:

$S_1 = S_0 \cdot \exp\left( (r - q - 0{,}5 \cdot v_{\mathrm{eff}})\Delta t + \sqrt{v_{\mathrm{eff}}} dW_S \right)$

Termo de *drift* ajustado:
$(r - q - 0{,}5 \cdot v_{\mathrm{eff}})\Delta t = (0{,}05 - 0{,}02 - 0{,}5 \cdot 0{,}04) \cdot 0{,}00396825$
$= (0{,}03 - 0{,}02) \cdot 0{,}00396825 = 0{,}01 \cdot 0{,}00396825 = 0{,}0000396825$

Termo estocástico:
$\sqrt{v_{\mathrm{eff}}} dW_S = \sqrt{0{,}04} \cdot (-0{,}031497) = 0{,}20 \cdot (-0{,}031497) = -0{,}0062994$

Soma dos termos no expoente:
$0{,}0000396825 - 0{,}0062994 = -0{,}00625972$

Cálculo final do preço:
$S_1 = 100 \cdot \exp(-0{,}00625972) \approx 100 \cdot 0{,}9937598 = 99{,}37598$

---

### Armadilhas Comuns na Simulação e Calibração

1. **Confundir Ruído de Monte Carlo com Efeito Paramétrico**:
   O preço gerado via Monte Carlo é um estimador ruidoso com erro padrão associado:
   $SE = \frac{\sigma_{\text{payoff}}}{\sqrt{N_{\text{paths}}}}$
   Se você alterar um parâmetro do modelo sem fixar a semente aleatória (*random seed*), a variação observada na superfície de volatilidade pode ser fruto do ruído amostral da simulação e não do impacto real do parâmetro.

2. **Truncamento Naive de Variância**:
   Permitir que $v$ assuma valores negativos ou tentar extrair a raiz quadrada de números negativos resulta na interrupção (*crash*) do pipeline numérico. É indispensável aplicar o truncamento completo (`v_eff = np.maximum(v, 0.0)`).

3. **Tentativa de Calibração via Monte Carlo em Produção**:
   Utilizar simulação de Monte Carlo para calibrar o modelo de Heston contra uma superfície inteira de opções de mercado é computacionalmente inviável, pois exigiria rodar dezenas de milhares de trajetórias para cada *strike* e maturidade a cada iteração do otimizador. Em produção, a calibração é feita via integração numérica da **Função Característica** do modelo de Heston. O Monte Carlo é utilizado para compreensão conceitual, testes de validação (*sanity checks*) e precificação de exóticos dependentes de trajetória.

4. **Interpretação Incorreta da Violação de Feller**:
   A violação da condição de Feller ($2\kappa\theta < \xi^2$) não significa que o modelo seja inválido ou "proibido". Significa apenas que a variância tocará o valor zero com frequência. O algoritmo deve estar numericamente preparado para lidar com zero sem colapsar.

---

### Laboratório Prático Sugerido em Python (Passo a Passo)

Para fixação prática da mecânica do modelo, descreve-se a estrutura detalhada de um experimento de simulação em Python:

#### Passo 1 Função de Inversão de Volatilidade Implicita (Termômetro BS)
* Implementar uma função que calcula o preço da Call de Black-Scholes.
* Implementar um algoritmo de **bisseção** (`implied_vol_call`) que recebe o preço de uma opção gerado pelo Monte Carlo, o *strike* $K$, a maturidade $T$, a taxa $r$ e o dividendo $q$, retornando a volatilidade implícita que iguala o preço de Black-Scholes ao preço do Monte Carlo. O foco deve ser na estabilidade numérica, já que a precificação de Black-Scholes é monotonicamente crescente em relação à volatilidade.

#### Passo 2 O Motor de Simulação de Monte Carlo (`heston_mc_call`)
* Definir a grade temporal com $N_{\text{steps}} = T \cdot 252$ e incremento $\Delta t = T / N_{\text{steps}}$.
* Gerar matrizes de variáveis normais independentes $Z_1, Z_2$ de dimensão $(N_{\text{paths}}, N_{\text{steps}})$.
* Construir $dW_S$ e $dW_v$ aplicando a correlação $\rho$.
* Iterar no tempo atualizando a variância com truncamento total:
  1. `v_eff = np.maximum(v, 0.0)`
  2. `v = v + kappa * (theta - v_eff) * dt + xi * np.sqrt(v_eff) * dW_v`
  3. `v = np.maximum(v, 0.0)`
  4. `S = S * np.exp((r - q - 0.5 * v_eff) * dt + np.sqrt(v_eff) * dW_S)`
* Vetorizar o cálculo do *payoff* terminal $\max(S_T - K, 0)$, calcular o preço descontado $e^{-rT} \text{payoff}$ e extrair a média e o erro padrão $SE = \text{std} / \sqrt{N_{\text{paths}}}$.

#### Passo 3 Testes de Sanidade Numérica
* **Teste da Média da Variância**: Comparar a média amostral de $v_t$ ao longo de todas as trajetórias no tempo $t$ com a fórmula teórica $\theta + (v_0-\theta)e^{-\kappa t}$.
* **Colapso do Smile**: Configurar $\xi = 0{,}0001$. Verificar se o *smile* de volatilidade colapsa em uma linha reta horizontal.
* **Achatamento do Skew**: Alterar $\rho$ de $-0{,}8$ para $-0{,}1$ e observar o achatamento da inclinação do *skew*.

#### Passo 4 Experimento Controlado de Parâmetros
* Fixar uma semente aleatória (`np.random.seed(42)`).
* Definir uma grade de *strikes* (`K_list`).
* Alterar um parâmetro de cada vez ($v_0$, $\theta$, $\kappa$, $\xi$, $\rho$) mantendo os demais constantes e plotar a curva de volatilidade implícita vs. *strike* para visualizar o efeito individual de cada elemento da "gramática" de Heston.

---

### Glossário de Termos Importantes

* **Condição de Feller**: Relação paramétrica $2\kappa\theta \ge \xi^2$ que garante analiticamente que a variância estocástica no modelo contínuo permaneça estritamente positiva.
* **Efeito Alavancagem (*Leverage Effect*)**: Tendência observada no mercado onde retornos negativos do ativo estão correlacionados com aumentos na volatilidade. No modelo de Heston, é representado pelo parâmetro de correlação negativa $\rho < 0$.
* **Função Característica**: Transformada de Fourier da densidade de probabilidade do modelo de Heston, utilizada para precificar opções europeias de forma semi-analítica via integração unidimensional, permitindo calibração rápida.
* **Inversão por Bisseção**: Método numérico estável para encontrar a volatilidade implícita de Black-Scholes igualando o preço do modelo ao preço de mercado/simulação.
* **Smile de Volatilidade (*Volatility Smile*)**: Padrão formato em "U" ou inclinado observável ao plotar a volatilidade implícita em função do preço de exercício (*strike*) para um determinado vencimento.
* **Truncamento Total (*Full Truncation*)**: Técnica de salvaguarda numérica para simulação de processos CIR onde a parte positiva da variância $\max(v, 0.0)$ é utilizada no cálculo do *drift* e da difusão, evitando colapsos computacionais por números negativos.
* **Volatilidade da Volatilidade (*Vol-of-Vol* / $\xi$)**: Parâmetro que mede o nível de aleatoriedade e dispersão na evolução da própria variância instantânea.

---

### Questões de Fixação e Aprofundamento

#### Nível 1 Resposta Curta

1. **Qual é a principal função do modelo de Black-Scholes no contexto de um laboratório de simulação do Modelo de Heston?**
   *Resposta*: O modelo de Black-Scholes é utilizado unicamente como um "termômetro". Ele converte os preços de opções gerados pelo modelo de Heston em volatilidades implícitas, permitindo visualizar o *smile* na linguagem padrão de mercado.

2. **Como se constroem dois incrementos brownianos correlacionados $dW_S$ e $dW_v$ a partir de duas variáveis aleatórias normais independentes $Z_1$ e $Z_2$?**
   *Resposta*: Através da decomposição: $dW_S = \sqrt{\Delta t} \cdot Z_1$ e $dW_v = \sqrt{\Delta t} \cdot (\rho Z_1 + \sqrt{1 - \rho^2} Z_2)$.

3. **O que acontece com o *smile* de volatilidade se o parâmetro de volatilidade da variância ($\xi$) for reduzido a zero?**
   *Resposta*: O *smile* colapsa e a volatilidade implícita torna-se plana (constante em relação aos *strikes*), pois a variância passa a ter uma evolução determinística.

4. **Por que a variância instantânea inicial $v_0$ afeta principalmente as opções de curto prazo?**
   *Resposta*: Porque $v_0$ representa o ponto de partida do processo de variância em $t=0$. À medida que o tempo passa, a reversão à média puxa a variância em direção a $\theta$, fazendo com que o impacto de $v_0$ diminua em prazos mais longos.

---

#### Nível 2 Questões Intermediárias e de Análise

1. **Explique porque a calibração do modelo de Heston contra opções de mercado não deve ser executada utilizando simulações de Monte Carlo em ambiente de produção.**
   *Resposta*: A calibração envolve um algoritmo de otimização que avalia milhares de combinações de parâmetros. Executar dezenas de milhares de trajetórias de Monte Carlo para cada *strike* e maturidade em cada iteração do otimizador seria extremamente lento e inviável computacionalmente. Em produção, utiliza-se a função característica de Heston para precificação semi-analítica ultrarrápida.

2. **Considere dois testes de simulação onde o parâmetro $\rho$ muda de $-0{,}8$ para $-0{,}1$. Descreva a alteração esperada na curva de volatilidade implícita.**
   *Resposta*: A inclinação (*skew*) da curva de volatilidade se achatará significativamente. Com $\rho = -0{,}8$, as opções de *strikes* baixos (OTM puts) possuem volatilidade implícita muito superior às de *strikes* altos. Com $\rho = -0{,}1$, essa assimetria é quase eliminada, aproximando o gráfico de um *smile* simétrico.

3. **Qual é o papel da fórmula do valor esperado da variância $E[v_t \mid v_0] = \theta + (v_0-\theta)e^{-\kappa t}$ na validação do código de simulação?**
   *Resposta*: Ela serve como um teste de integridade (*sanity check*). Se a média empírica da variância simulada em variadas trajetórias não coincidir aproximadamente com esse resultado analítico, o erro não é do modelo de Heston, mas sim uma falha de discretização ou implementação no código do usuário.

---

#### Nível 3 Prompts de Dissertação / Análise Crítica

1. **Compare e contraste a filosofia de modelagem entre os modelos de Volatilidade Local e o Modelo de Volatilidade Estocástica de Heston. Quais são as vantagens e limitações de cada abordagem em relação ao ajuste de superfície e dinâmica do mercado?**
   *Resposta*: A diferença fundamental reside na direção do fluxo da informação. No modelo de Volatilidade Local, a superfície de volatilidade observada no mercado é a entrada (*input*), e o modelo constrói uma difusão determinística para reproduzir exatamente todos os preços de opções vanillas do mercado em $t=0$. A vantagem é o ajuste perfeito à superfície de preços atuais; a limitação é que a dinâmica futura da volatilidade é rígida e não possui componentes estocásticos independentes. No modelo de Heston, a dinâmica de difusão de dois fatores estocásticos (ativo e variância) é a entrada (*input*), e a superfície é a saída (*output*). A limitação é a impossibilidade de calibrar perfeitamente ponto a ponto cada opção do mercado devido ao número limitado de parâmetros. A vantagem é que o modelo gera uma dinâmica temporal da volatilidade rica e com significado econômico (efeito alavancagem, *vol-of-vol* e reversão à média), sendo superior para precificar produtos exóticos cuja rentabilidade depende do caminho percorrido pela volatilidade.

2. **Analise os impactos da discretização numérica no modelo de Heston quando a Condição de Feller ($2\kappa\theta \ge \xi^2$) é violada. Por que o truncamento simples pode falhar em máquinas digitais e como a técnica de truncamento total (*Full Truncation*) resolve o problema?**
   *Resposta*: Quando a condição de Feller é violada, o processo contínuo de variância CIR pode tocar o valor zero. Na implementação discreta em computador, choques aleatórios negativos podem projetar o valor da variância $v$ para a região negativa. Tentar calcular a atualização do ativo ou da própria variância usando $v < 0$ gera erro de raiz quadrada de número negativo, interrompendo a simulação. Se tentarmos usar um truncamento simples (como tomar o valor absoluto ou zerar apenas ao final), o *drift* pode ser calculado de forma incorreta no passo seguinte, distorcendo a dinâmica. A técnica de truncamento total (*Full Truncation*) resolve esse problema aplicando a variância efetiva $v_{\mathrm{eff}} = \max(v, 0.0)$ em todas as instâncias da equação (tanto no termo de *drift* $\kappa(\theta - v_{\mathrm{eff}})dt$ quanto no termo de difusão $\xi \sqrt{v_{\mathrm{eff}}} dW_v$). Isso garante estabilidade numérico-computacional mantendo o comportamento correto da dinâmica mesmo em regimes onde a variância toca a origem com frequência.