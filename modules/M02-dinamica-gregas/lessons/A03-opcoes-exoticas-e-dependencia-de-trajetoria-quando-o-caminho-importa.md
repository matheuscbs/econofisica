<!-- imported from vault study notes; curated for open course -->
# M02.A03 — Opções exóticas e dependência de trajetória: quando o caminho importa

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M02
> **Aula:** M02.A03

↑ M02 · Resumo · Completo

**Módulo:** M02
**Pergunta do módulo:** Como a dinâmica do spot e as gregas mudam o P&L do livro?

## Conceito-núcleo
Path dependence: payoff depende da trajetória (barriers, Asians, lookbacks), não só de S_T.

## Aplicação em mercado / trading
Precificar/hedgear knock-ins, CPI barriers e estruturas path-dependent; ligar a histerese de mercado.

## Entregável / lab
Especificar 1 barreira (ex. knock-in) e listar riscos de hedge que vanila não captura.

## Fonte (mapeamento)
quantitative-trading-free-lesson/08 exotic options and path dependance | IG CPI knock-in + histerese

## Guia de estudo aprofundado

> **info**
>

Este guia de estudos apresenta uma análise aprofundada sobre opções exóticas e dependência de trajetória no âmbito do apreçamento por neutralidade ao risco e simulação de Monte Carlo. O material aborda as quatro principais famílias de produtos exóticos, suas formulações matemáticas, armadilhas numéricas, estratégias de mitigação e comportamento das sensibilidades (Gregas), além de fornecer exercícios práticos e um laboratório computacional.

---

### Fundamentos Teóricos e Estrutura Neutra ao Risco

A precificação de ativos derivativos sob o arcabouço contínuo tradicional adota uma medida neutra ao risco $\mathbb{Q}$, na qual a taxa livre de risco $r$ e a volatilidade $\sigma$ são assumidas constantes. O ativo subjacente $S_t$ segue um Movimento Browniano Geométrico (GBM):

$$dS_t = rS_t\,dt + \sigma S_t\,dW_t^\mathbb{Q}, \qquad S_0 > 0$$

Em que $W_t^\mathbb{Q}$ é um processo de Movimento Browniano padrão sob $\mathbb{Q}$.

#### A Transição das Opções Vanila para as Opções Exóticas

Nas opções vanila (como Calls e Puts europeias), o *payoff* depende exclusivamente do preço final do ativo no vencimento, $H(S_T)$. A trajetória percorrida pelo preço entre $t=0$ e $t=T$ é irrelevante para a determinação do valor do contrato no vencimento.

Para as **opções exóticas**, a regra do contrato é alterada: o *payoff* passa a ser uma função de toda a trajetória do ativo, denotada por $H(S_\cdot)$. O valor justo do derivativo no instante $t=0$ é a esperança descontada do *payoff* sob a medida $\mathbb{Q}$:

$$V_0 = e^{-rT} \mathbb{E}^\mathbb{Q}[H(S_\cdot)]$$

À medida que o contrato passa a ancorar-se no "caminho percorrido", a simulação de Monte Carlo torna-se o método numérico fundamental para simular trajetórias do ativo, aplicar o *payoff* ao longo de cada trajetória e calcular a média descontada sob $\mathbb{Q}$.

---

### As Quatro Famílias de Opções Exóticas e suas Armadilhas

A introdução da dependência de trajetória não invalida a teoria do apreçamento por esperança sob $\mathbb{Q}$, mas introduz quatro famílias de armadilhas mecânicas e numéricas na simulação.

#### Opções Digitais (Discontinuidade do Payoff)

As opções digitais possuem *payoffs* descontínuos, funcionando como interruptores do tipo "tudo ou nada".

*   **Cash-or-Nothing**: Paga uma quantia fixa $Q$ se $S_T > K$, e zero caso contrário:
    $$H = Q \, \mathbf{1}_{\{S_T > K\}}$$

*   **Asset-or-Nothing**: Paga o valor do próprio ativo $S_T$ se $S_T > K$, e zero caso contrário:
    $$H = S_T \, \mathbf{1}_{\{S_T > K\}}$$

##### A Armadilha Numérica
A função indicadora $\mathbf{1}_{\{S_T > K\}}$ cria uma descontinuidade abrupta perto do preço de exercício $K$. Trajetórias cujos preços finais diferem por um valor microscópico ao redor de $K$ geram *payoffs* completamente distintos ($0$ ou $Q$/$S_T$). Na simulação de Monte Carlo, isso causa alta variabilidade no estimador. 

Além disso, a estimação do Delta via diferenças finitas (*bump-and-revalue*):

$$\Delta \approx \frac{V(S_0 + h) - V(S_0 - h)}{2h}$$

torna-se instável. Um pequeno choque $h$ não altera o *payoff* suavemente, mas alterna aleatoriamente cenários entre os lados do limiar $K$, transformando a derivada estimada em ruído de amostragem.

##### Solução Suavização do Limiar
Substitui-se a parede vertical da função indicadora por uma transição suave e diferenciável, como uma função sigmoide aplicada a $x = S_T - K$:

$$g(x) = \frac{1}{1 + e^{-ax}}$$

Ao substituir $\mathbf{1}_{\{S_T > K\}}$ por $g(S_T - K)$, preserva-se o significado econômico do contrato, estabilizando os cálculos de sensibilidade.

---

#### Opções de Barreira (Eventos ao Longo da Trajetória)

O *payoff* de uma opção de barreira depende de o preço do ativo ter atingido ou não um determinado nível $B$ durante a vida do contrato.

*   **Down-and-Out Call** (com $B < S_0$): Mantém o *payoff* de uma Call vanila somente se o nível mínimo do ativo permanecer estritamente acima de $B$:
    $$H = (S_T - K)^+ \, \mathbf{1}_{\{\min_{0 \le t \le T} S_t > B\}}$$

*   **Down-and-In Call**: Ativa o *payoff* de uma Call vanila somente se o ativo tocar a barreira $B$ ao menos uma vez:
    $$H = (S_T - K)^+ \, \mathbf{1}_{\{\min_{0 \le t \le T} S_t \le B\}}$$

##### Identidade de Estruturação
Como os cenários são particionados entre "tocar" e "não tocar" na barreira, vale a identidade:

$$C_{\text{vanilla}} = C_{\text{down-in}} + C_{\text{down-out}}$$

##### A Armadilha Numérica Vício de Discretização
O contrato financeiro prevê o monitoramento contínuo da barreira. No entanto, na simulação de Monte Carlo, a trajetória é observada em uma grade discreta de tempo $(t_0, t_1, \dots, t_m)$. Se o preço cruza a barreira $B$ dentro do intervalo $(t_i, t_{i+1})$ e retorna ao nível original antes do próximo ponto da grade, a simulação discreta não registra o toque.

Consequências:
1. Subestimação sistemática da probabilidade de toque na barreira.
2. Vício de apreçamento (*bias*): no caso de uma opção *down-and-out*, subestimar os toques superavalia a opção, pois pressupõe que o contrato sobrevive mais do que deveria na realidade. O vício se agrava quando $B$ está próximo de $S_0$ ou quando o passo de tempo $\Delta t$ é grande.

##### Solução Ponte Browniana
Condiciona-se a trajetória aos dois pontos conhecidos da grade, $S_t$ e $S_{t+\Delta t}$. Para uma barreira inferior com $S_t > B$ e $S_{t+\Delta t} > B$, a probabilidade de ter havido um toque no intervalo é aproximada por:

$$p_{\text{hit}} \approx \exp\left( -\frac{2 \ln(S_t / B) \ln(S_{t+\Delta t} / B)}{\sigma^2 \Delta t} \right)$$

Em cada passo em que ambos os extremos estão acima de $B$, calcula-se $p_{\text{hit}}$ e sorteia-se $U \sim U(0,1)$. Se $U < p_{\text{hit}}$, declara-se que a barreira foi atingida no intervalo, eliminando o vício de discretização sem a necessidade de hiper-refinar a grade temporal.

---

#### Opções Asiáticas (Médias Temporais)

O *payoff* das opções asiáticas depende da média do preço do ativo observada em datas fixadas $(0 < t_1 < \dots < t_m = T)$.

*   **Média Aritmética**:
    $$A = \frac{1}{m} \sum_{i=1}^{m} S_{t_i}$$
    *   **Asian Call**: $H = (A - K)^+$
    *   **Asian Put**: $H = (K - A)^+$

*   **Média Geométrica**:
    $$G = \exp\left( \frac{1}{m} \sum_{i=1}^{m} \ln S_{t_i} \right)$$

##### Intuição de Mercado e Variável de Controle
A operação de média amortece os ruídos e oscilações do preço do ativo ao longo do tempo. Como resultado, a opção asiática "enxerga" uma volatilidade efetiva menor do que uma opção vanila correspondente, tornando seu preço, em condições equivalentes, inferior ao de uma vanila.

Como a média aritmética de variáveis log-normais não possui uma distribuição simples em forma fechada, Monte Carlo é a abordagem padronizada. No entanto, sob o GBM, a média geométrica $G$ segue uma distribuição log-normal, o que permite obter seu preço exato em forma fechada (similar ao modelo de Black-Scholes com parâmetros efetivos). 

Essa propriedade torna a opção asiática geométrica uma excelente **variável de controle** (*control variate*): simulam-se $A$ e $G$ nas mesmas trajetórias e utiliza-se o preço teórico conhecido de $G$ para calibrar a média de $A$, reduzindo substancialmente a variação das estimativas de Monte Carlo.

---

#### Opções Lookback (Valores Extremos)

Nas opções *lookback*, o *payoff* é guiado polos valores de máximo ou mínimo atingidos durante a vida do contrato.

*   **Lookback com Strike Fixo (Call sobre o Máximo)**:
    $$H = \left( \max_{0 \le t \le T} S_t - K \right)^+$$

*   **Lookback com Strike Flutuante (Call)**:
    $$H = S_T - \min_{0 \le t \le T} S_t$$

##### A Armadilha Numérica
A simulação em grade discreta avalia $\max_i S_{t_i}$ e $\min_i S_{t_i}$. Em tempo contínuo, os extremos reais são quase invariavelmente mais severos do que os observados na grade. A simulação ingênua gera um vício de discretização que subestima os preços máximos e superestima os preços mínimos. 

A correção exige o refinamento da frequência temporal ou o uso de técnicas de ponte browniana adaptadas para estimar os extremos intra-passo (frequentemente aplicadas sobre $\ln S$, onde o GBM possui propriedades gaussianas).

---

### Comparativo de Intuição de Mercado e Sensibilidades (Greeks)

A tabela abaixo sintetiza o comportamento econômico e a dinâmica das sensibilidades para cada família de exóticas:

| Família de Opção | Mecanismo do Payoff | Comportamento da Volatilidade / Preço | Desafios nas Sensibilidades (Greeks) |
| :--- | :--- | :--- | :--- |
| **Digitais** | Descontínuo (Switch) | Sensibilidade extrema perto do *strike* $K$. | *Bump-and-revalue* falha por ruído de amostragem. Exige suavização. |
| **Barreiras** | Evento de toque no nível $B$ | Preço varia drasticamente conforme a proximidade de $B$. | Sensibilidades instáveis perto da barreira; risco de *gap* inviabiliza *hedge* contínuo. |
| **Asiáticas** | Média temporal ($A$ ou $G$) | Volatilidade efetiva reduzida; opção mais barata que a vanila. | Grega mais suave devido ao amortecimento, mas altamente dependente do calendário de observação (*fixings*). |
| **Lookback** | Extremos ($\max$ ou $\min$) | Preço elevado pelo direito de acessar os extremos da trajetória. | Sensibilidades elevadas e irregulares quando novos recordes históricos são atingidos. |

---

### Exemplo Numérico Resolvido Passo a Passo

#### Problema
Considere uma opção de barreira *Down-and-Out Call* avaliada via simulação de Monte Carlo. Em um determinado passo de tempo da simulação, entre $t$ e $t + \Delta t$, o preço do ativo é observado em uma grade discreta.

Dados os seguintes parâmetros:
*   Preço no início do intervalo: $S_t = 95$
*   Preço no final do intervalo: $S_{t+\Delta t} = 93$
*   Nível da Barreira Inferior: $B = 90$
*   Volatilidade do ativo: $\sigma = 0{,}20$ (20% ao ano)
*   Passo de tempo: $\Delta t = 0{,}10$ anos

Ambos os preços observados na grade discreta estão estritamente acima da barreira ($95 > 90$ e $93 > 90$). Calcule a probabilidade $p_{\text{hit}}$ de o ativo ter atingido a barreira $B$ dentro do intervalo contínuo $(t, t+\Delta t)$ utilizando a correção de Ponte Browniana.

---

#### Resolução Passo a Passo

##### Passo 1 Aplicação da fórmula da Ponte Browniana
A probabilidade de toque intra-passo é dada por:

$$p_{\text{hit}} = \exp\left( -\frac{2 \ln(S_t / B) \ln(S_{t+\Delta t} / B)}{\sigma^2 \Delta t} \right)$$

##### Passo 2 Cálculo dos logaritmos das razões relativas à barreira

$$\frac{S_t}{B} = \frac{95}{90} \approx 1{,}055556 \implies \ln(S_t / B) = \ln(1{,}055556) \approx 0{,}054067$$

$$\frac{S_{t+\Delta t}}{B} = \frac{93}{90} \approx 1{,}033333 \implies \ln(S_{t+\Delta t} / B) = \ln(1{,}033333) \approx 0{,}032790$$

##### Passo 3 Cálculo do numerador do expoente

$$\text{Numerador} = -2 \times \ln(S_t / B) \times \ln(S_{t+\Delta t} / B)$$
$$\text{Numerador} = -2 \times 0{,}054067 \times 0{,}032790 \approx -0{,}0035457$$

##### Passo 4 Cálculo do denominador do expoente

$$\text{Denominador} = \sigma^2 \Delta t = (0{,}20)^2 \times 0{,}10 = 0{,}04 \times 0{,}10 = 0{,}004$$

##### Passo 5 Cálculo do valor do expoente

$$\text{Expoente} = \frac{-0{,}0035457}{0{,}004} = -0{,}886425$$

##### Passo 6 Cálculo final da probabilidade $p_{\text{hit}}$

$$p_{\text{hit}} = \exp(-0{,}886425) \approx 0{,}412128 \quad (41{,}21\%)$$

#### Conclusão do Exemplo
Apesar de os dois pontos discretos ($95$ e $93$) estarem acima do nível $B = 90$, a probabilidade de a trajetória contínua ter cruzado a barreira no intervalo é de **$41{,}21\%$**. Se a simulação ignorasse a ponte browniana, essa probabilidade seria considerada $0\%$, gerando um vício de subestimação do evento de desativação da opção (*knock-out*).

---

### Laboratório Prático em Python (Roteiro em Passos)

Abaixo descreve-se o roteiro para a construção de um algoritmo de apreçamento de opções exóticas via Monte Carlo em Python.

#### Passo 1 Geração de Trajetórias do GBM no Logaritmo
Implementar o esquema log-exato para garantir simulações exatas sem erro de Euler:

$$S_{t+\Delta t} = S_t \exp\left( \left( r - \frac{1}{2}\sigma^2 \right) \Delta t + \sigma \sqrt{\Delta t} \, Z \right), \qquad Z \sim \mathcal{N}(0,1)$$

*   Criar uma matriz de dimensão $(M \times m)$, onde $M$ é o número de trajetórias (ex: $M = 100.000$) e $m$ é a quantidade de subintervalos de tempo ($m = T / \Delta t$).

#### Passo 2 Implementação da Suavização para Opções Digitais
*   Para uma opção *Cash-or-Nothing*, calcular o preço terminal $S_T$ em cada trajetória.
*   Em vez de atribuir o *payoff* via `1 if S_T > K else 0`, aplicar a função sigmoide $g(S_T - K) = \frac{1}{1 + e^{-a(S_T - K)}}$, parametrizando $a$ para obter uma transição suave.
*   Calcular o Delta ajustando $S_0 \pm h$ e reavaliando a média do *payoff* suave.

#### Passo 3 Implementação da Ponte Browniana para Barreiras
*   Para opções de barreira (ex: *Down-and-Out Call*), iterar sobre cada passo de tempo $i$ de cada trajetória $j$.
*   Verificar se $S_{t_i} \le B$ ou $S_{t_{i+1}} \le B$. Se sim, marcar a trajetória como desativada (*hit*).
*   Se ambos os pontos estiverem acima da barreira ($S_{t_i} > B$ e $S_{t_{i+1}} > B$), calcular $p_{\text{hit}}$.
*   Sortear $U \sim U(0,1)$. Se $U < p_{\text{hit}}$, marcar a trajetória como desativada.
*   Retornar o *payoff* $(S_T - K)^+$ apenas para as trajetórias sobreviventes.

#### Passo 4 Implementação da Variável de Controle para Asiáticas
*   Para cada trajetória, calcular a média aritmética $A = \frac{1}{m} \sum_{i=1}^m S_{t_i}$ e a média geométrica $G = \exp\left(\frac{1}{m} \sum_{i=1}^m \ln S_{t_i}\right)$.
*   Obter o preço analítico da opção geométrica $V_G^{\text{analítico}}$.
*   Ajustar os *payoffs* da opção aritmética via regressão/covariância com a opção geométrica para reduzir a variância do estimador.

#### Passo 5 Estimador de Monte Carlo e Erro Padrão
*   Para qualquer payoff $H^{(j)}$ obtido na trajetória $j$, calcular o valor presente médio estimado:
    $$\widehat{V}_0 = e^{-rT} \frac{1}{M} \sum_{j=1}^{M} H^{(j)}$$
*   Calcular o Erro Padrão (*Standard Error*) da simulação para quantificar o ruído numérico:
    $$SE \approx \frac{\operatorname{Std}(e^{-rT}H)}{\sqrt{M}}$$

---

### Glossário de Termos Importantes

*   **Apreçamento Neutro ao Risco ($\mathbb{Q}$)**: Arcabouço teórico em que o preço de um derivativo é igual ao valor esperado descontado de seus *payoffs* futuros sob a medida de probabilidade $\mathbb{Q}$, na qual o retorno esperado de todos os ativos é a taxa livre de risco $r$.
*   **Dependência de Trajetória (*Path Dependence*)**: Propriedade de contratos cujo *payoff* no vencimento depende da evolução do preço do subjacente ao longo do tempo ($S_\cdot$), e não apenas do valor terminal no vencimento ($S_T$).
*   **Opção Digital (Binary Option)**: Opção com *payoff* descontínuo, que paga um valor fixo em dinheiro (*Cash-or-Nothing*) ou o próprio ativo (*Asset-or-Nothing*) caso uma condição de preço seja satisfeita.
*   **Opção de Barreira (Barrier Option)**: Opção cujo direito de exercício é ativado (*knock-in*) ou cancelado (*knock-out*) se o preço do ativo atingir um determinado nível $B$ durante sua vigência.
*   **Opção Asiática**: Opção cujo *payoff* é determinado pela média (aritmética ou geométrica) do preço do subjacente ao longo de datas de observação prefixadas.
*   **Opção Lookback**: Opção cujo *payoff* depende dos valores extremos (máximo ou mínimo) alcançados pelo ativo subjacente durante a vida do contrato.
*   **Ponte Browniana (*Brownian Bridge*)**: Tabela de probabilidade condicional utilizada para inferir o comportamento de um processo estocástico contínuo entre dois pontos discretos observados, usada para corrigir o vício de amostragem em opções de barreira e *lookback*.
*   **Vício de Discretização (*Discretization Bias*)**: Erro sistemático em simulações numéricas decorrente do monitoramento de processos contínuos em uma grade temporal discreta.
*   **Variável de Controle (*Control Variate*)**: Técnica de redução de variância em simulações de Monte Carlo que utiliza um ativo ou contrato correlacionado com preço analítico conhecido para calibrar a estimativa.
*   **Erro Padrão da Simulação (*Standard Error - SE*)**: Medida da incerteza estatística da estimativa de Monte Carlo, inversamente proporcional à raiz quadrada do número de simulações ($\sqrt{M}$).

---

### Questões de Prática e Autoavaliação

#### Nível 1 Conceitual e Curta Resposta

##### Questão 1
Qual é a diferença fundamental entre uma opção vanila e uma opção exótica no que tange à formação de seu *payoff*?

**Resposta:**
Nas opções vanila, o *payoff* depende exclusivamente do preço do ativo no momento do vencimento $S_T$. Nas opções exóticas, o *payoff* depende da trajetória percorrida pelo ativo ao longo da vida do contrato $S_\cdot$ (por exemplo, médias, extremos ou valores atingidos em relação a limiares).

---

##### Questão 2
Explique a identidade de estruturação $C_{\text{vanilla}} = C_{\text{down-in}} + C_{\text{down-out}}$ para opções com mesmo *strike* $K$, barreira $B$ e vencimento $T$.

**Resposta:**
A identidade decorre de uma partição exaustiva e mutuamente exclusiva dos cenários de trajetória do ativo sob a medida $\mathbb{Q}$. Para qualquer trajetória, ou o ativo toca a barreira $B$ pelo menos uma vez (ativando a opção *down-in* e desativando a *down-out*), ou nunca toca a barreira (mantendo a *down-out* ativa e a *down-in* inativa). A soma das duas resulta exatamente no *payoff* de uma Call vanila em todos os cenários.

---

##### Questão 3
Por que a opção asiática geralmente possui um preço inferior ao de uma opção vanila equivalente?

**Resposta:**
Porque a operação de média (seja aritmética ou geométrica) suaviza as oscilações e diminui a variabilidade do valor final considerado no *payoff*. Ao reduzir a volatilidade efetiva percebida pelo contrato, o valor esperado do *payoff* sob $\mathbb{Q}$ diminui em comparação ao de uma vanila exposta à volatilidade total de $S_T$.

---

#### Nível 2 Aplicação Intermediária

##### Questão 4
Uma simulação ingênua de Monte Carlo para uma opção *Down-and-Out Call* gera um preço estimado de R\$ 5,50. Se aplicarmos a correção por Ponte Browniana para toques intra-passo, o preço estimado da opção deve aumentar, diminuir ou permanecer igual? Justifique.

**Resposta:**
O preço estimado da opção deve **diminuir**. A simulação ingênua ignora os toques na barreira que ocorrem entre as datas da grade discreta, subestimando os eventos de desativação (*knock-out*). Ao aplicar a Ponte Browniana, mais trajetórias são identificadas como desativadas (atingiram a barreira), o que reduz a quantidade de trajetórias sobreviventes com *payoff* positivo e, consequentemente, reduz o valor justo estimado do contrato.

---

##### Questão 5
Descreva por que o cálculo do Delta ($\Delta$) por diferenças finitas centrais (*bump-and-revalue*) é instável para opções digitais e como a função sigmoide resolve esse problema.

**Resposta:**
Opções digitais possuem um *payoff* descontínuo decorrente do uso da função indicadora. Pequenos choques $h$ no preço inicial $S_0$ alteram aleatoriamente trajetórias marginais ao redor do *strike* $K$, fazendo com que o indicador alterne entre $0$ e $1$. Isso introduz alto ruído de amostragem na estimativa da derivada. A função sigmoide substitui o degrau vertical por uma curva suave e diferenciável, garantindo que pequenas mudanças em $S_0$ reflitam alterações graduais e continuas no valor esperado do *payoff*, estabilizando a estimativa do Delta.

---

##### Questão 6
Como a opção asiática geométrica pode ser utilizada para melhorar a eficiência da simulação de Monte Carlo de uma opção asiática aritmética?

**Resposta:**
A opção asiática geométrica sob o modelo GBM possui solução analítica em forma fechada. Como os valores das médias aritmética e geométrica calculados sob a mesma trajetória apresentam altíssima correlação, a opção geométrica pode ser utilizada como **variável de controle**. O erro de amostragem observado na simulação da opção geométrica (diferença entre sua média simulada e seu valor analítico) é utilizado para corrigir a estimativa da opção aritmética, reduzindo drasticamente a variância do estimador sem exigir aumento do número de trajetórias $M$.

---

#### Nível 3 Análise Crítica e Questões Discursivas

##### Questão 7
Considere a precificação de uma opção *Lookback* com *strike* flutuante ($H = S_T - \min_{0 \le t \le T} S_t$). Analise o impacto do erro de discretização temporal na estimativa do preço do contrato via Monte Carlo sem correções de ponte contínua, e explique o comportamento de suas sensibilidades perto de mínimos históricos.

**Resposta:**
A amostragem em grade discreta avalia o mínimo apenas nos pontos $t_i$. O mínimo contínuo verdadeiro no intervalo $[0, T]$ é sempre menor ou igual ao mínimo discreto ($\min_{\text{contínuo}} S_t \le \min_{\text{discreto}} S_{t_i}$). Portanto, a simulação ingênua superestima o mínimo real, resultando na subavaliação sistemática do *payoff* $S_T - \min S_t$. O preço estimado da *Lookback* fica viciado para baixo.

Em termos de sensibilidades, quando o preço do ativo atinge novos mínimos históricos, a variável de estado que define o "recorde" ($\min S_t$) é instantaneamente atualizada. Isso torna o *payoff* altamente sensível e irregular perto dessas marcas, criando variações não lineares intensas na precificação e exigindo ajustes frequentes de *hedge*.

---

##### Questão 8
Discuta a seguinte afirmação: "A simulação de Monte Carlo em exóticas não altera o arcabouço teórico da precificação neutra ao risco, mas transfere a complexidade do modelo matemático para a gestão do ruído e do vício numérico." Considere no seu argumento a taxa de convergência do Erro Padrão ($SE$) e as quatro famílias de exóticas estudadas.

**Resposta:**
A afirmação é correta. A teoria subjacente permanece idêntica à das opções vanila: o preço é a esperança descontada do *payoff* sob a medida neutra ao risco $\mathbb{Q}$, $V_0 = e^{-rT} \mathbb{E}^\mathbb{Q}[H(S_\cdot)]$, utilizando os mesmos parâmetros $r$, $\sigma$ e o processo $dW_t^\mathbb{Q}$. O arcabouço financeiro-teórico não muda.

A complexidade desloca-se para a engenharia numérica porque o formato de $H(S_\cdot)$ interage com a natureza do ruído de amostragem e da discretização:
1. Nas **digitais**, a descontinuidade do *payoff* explode a variância e desestabiliza o Erro Padrão ($SE \approx \operatorname{Std}(e^{-rT}H)/\sqrt{M}$), exigindo técnicas de suavização para estabilizar derivadas.
2. Nas **barreiras** e **lookbacks**, a amostragem discreta insere um vício sistemático (viés) ao perder eventos intra-passo, exigindo pontes brownianas.
3. Nas **asiáticas**, a dependência de múltiplos *fixings* exige ferramentas de redução de variância (como variáveis de controle) para acelerar a convergência lenta de ordem $\mathcal{O}(1/\sqrt{M})$.

Portanto, a precisão da precificação de exóticas via Monte Carlo depende de neutralizar o viés de discretização e controlar a variância do estimador estatístico.