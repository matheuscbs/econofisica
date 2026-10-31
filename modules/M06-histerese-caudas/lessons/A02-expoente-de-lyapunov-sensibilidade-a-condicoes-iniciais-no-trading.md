<!-- imported from vault study notes; curated for open course -->
# M06.A02 — Expoente de Lyapunov: sensibilidade a condições iniciais no trading

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M06
> **Aula:** M06.A02

↑ M06 · Resumo · Completo

**Módulo:** M06
**Pergunta do módulo:** Por que trajetória e caos importam no drawdown e na previsibilidade?

## Conceito-núcleo
Lyapunov: divergência exponencial entre trajetórias próximas; limite de previsibilidade.

## Aplicação em mercado / trading
Reduzir confiança em sinais de curto prazo quando o sistema está caótico; preferir regras de regime.

## Entregável / lab
Estimativa ilustrativa de divergência entre paths próximos (simulação ou série real).

## Fonte (mapeamento)
quantitative-trading-free-lesson/23 lyapuniov | IG Lyapunov

## Guia de estudo aprofundado

> **info**
>

### Visão Geral e Objetivos de Aprendizado

Este guia de estudo explora a estimativa do Expoente de Lyapunov aplicada às séries temporais do mercado financeiro, com base nas análises de Karim Khemiri (Khem Kapital). O objetivo principal não é prever a direção do mercado (se o preço vai subir ou cair), mas compreender a **mecanica de propagação de perturbações** e os **limites de previsibilidade** de um regime de mercado.

Ao final deste material, você será capaz de:
* Compreender como a reconstrução do espaço de estados captura a memória de curto prazo do sistema.
* Identificar visual e matematicamente o conceito de "gêmeo quase-idêntico" (vizinho mais próximo).
* Interpretar a taxa de divergência local usando a escala logarítmica.
* Classificar o regime de risco do mercado com base no sinal do Expoente de Lyapunov ($\lambda > 0$, $\lambda \approx 0$, $\lambda < 0$).
* Implementar a lógica do algoritmo em passos estruturados de código em Python.

---

### Conceitos-Chave Explicados em Profundidade

#### Reconstrução do Espaço de Estados

Um sistema financeiro não existe apenas em um ponto isolado no tempo $t$. Ele vive em um rastro (uma trajetória), onde o histórico recente estabelece as restrições para os estados futuros. Para sair de uma leitura plana de preços ou retornos, utiliza-se a reconstrução do espaço de estados por meio de dois parâmetros centrais:
* **Atraso temporal ($\tau$ ou `delay`)**: O intervalo de tempo entre as amostras passadas.
* **Dimensão de incorporação ($m$ ou `dimension`)**: O número de pontos do passado combinados para formar a configuração do sistema.

A fórmula que gera o vetor de estado $X_t$ no espaço reconstruído é dada por:

$$X_t = (x_t, x_{t+\tau}, x_{t+2\tau}, \ldots, x_{t+(m-1)\tau})$$

Cada vetor $X_t$ representa uma pequena configuração local com memória curta, capturando a tensão e a estrutura interna do mercado naquele momento específico. Para um sinal de tamanho $N$, o número total de estados reconstruídos válidos é $M = N - (m - 1)\tau$.

#### Identificação do Vizinho Mais Próximo

Após reconstruir os estados $X$, o algoritmo busca para cada estado $X_i$ outro momento no passado $X_j$ no qual o sistema esteve em uma configuração quase idêntica (um "gêmeo quase-idêntico"). 

Para evitar uma comparação artificial com o próprio ponto, a diagonal da matriz de distâncias euclidianas é preenchida com infinito ($\infty$), e o vizinho mais próximo é selecionado via menor distância:

$$\text{dists}_{i, j} = \lVert X_i - X_j \rVert$$

$$j = \arg\min_{j \neq i} (\text{dists}_{i, j})$$

#### Medida de Divergência Local e a Razão Logarítmica

A questão central do algoritmo é observar o que acontece com a pequena diferença entre esses dois estados quase iguais no passo de tempo seguinte. As distâncias no instante inicial ($d_0$) e no instante seguinte ($d_1$) são calculadas adicionando-se uma constante de regularização $\epsilon$ (`eps = 1e-6`) para estabilidade numérica:

$$d_0 = \lVert X_i - X_j \rVert + \epsilon$$

$$d_1 = \lVert X_{i+1} - X_{j+1} \rVert + \epsilon$$

A divergência local é calculada pela razão logarítmica:

$$\lambda_{\mathrm{local}} = \log\left(\frac{d_1}{d_0}\right)$$

**Por que utilizar o logaritmo?** 
A propagação de desvios em regimes instáveis segue uma lógica de contaminação e amplificação não linear. O uso do logaritmo traz essa taxa de amplificação exponencial para uma escala aditiva e linearizável, permitindo medir a lei subjacente de contaminação do sistema.

#### O Expoente Global de Lyapunov

O valor final do Expoente de Lyapunov operacional é obtido calculando-se a média de todas as divergências locais calculadas ao longo do rastro da série:

$$\lambda = \frac{1}{M-1} \sum_{i=0}^{M-2} \log\left(\frac{d_1}{d_0}\right)$$

---

### Intuição de Mercado e Trading

#### Propagação vs. Direção

O Expoente de Lyapunov não é um indicador de tendência (como médias móveis) nem um oscilador de preço (como RSI ou Estocástico). Ele não responde à pergunta "o mercado vai subir ou cair?". Ele responde à pergunta: **"Quando uma anomalia surge no mercado, o sistema a neutraliza ou a faz crescer?"**

#### Mapeamento dos Regimes de Risco

| Expoente ($\lambda$) | Comportamento do Sistema | Dinâmica de Mercado | Leitura de Risco de Mesa (Desk-Level) |
| :--- | :--- | :--- | :--- |
| **$\lambda > 0$** | **Amplificação** | Pequenas desviações e perturbações propagam-se rapidamente, gerando reações em cadeia. | Instabilidade estrutural. O mercado é capaz de fabricar grandes choques a partir de anomalias irrelevantes, sem necessidade de notícias exógenas. |
| **$\lambda \approx 0$** | **Limite / Borda** | O sistema não dissipa nem amplifica ativamente as diferenças. Mantém-se sem margem de segurança. | A superfície parece calma, mas a estabilidade é frágil. Qualquer pequeno impulso adicional pode quebrar o equilíbrio. |
| **$\lambda < 0$** | **Dissipação** | As lacunas se fecham; perturbações e divergências são absorvidas e neutralizadas. | O sistema atua como um amortecedor de choques (*shock absorber*), contendo as imperfeições locais. |

---

### Armadilhas Comuns

* **Tratar o indicador como sinal direcional:** Tentar abrir posições de compra ou venda baseando-se apenas no valor de $\lambda$. Ele mede instabilidade e propagação, não direção.
* **Acreditar que $\lambda < 0$ significa "ausência de risco":** Um regime dissipativo absorve anomalias internas, mas isso não garante proteção contra grandes choques exógenos repentinos.
* **Confundir a medida com o expoente teórico absoluto:** No trading, o algoritmo atua como um *proxy* operacional limpo e testável para dados finitos e ruidosos, e não como uma verdade matemática absoluta sobre o caos de sistemas contínuos infinitos.
* **Uso incorreto da escala das diferenças:** Avaliar diferenças simples de preço ($d_1 - d_0$) em vez do fator de taxa exponencial dado pela razão $\log(d_1 / d_0)$.

---

### Exemplo Numérico Resolvido Passo a Passo

Considere uma série temporal simplificada de preços de um ativo com $N = 5$ pontos:

$$\text{signal} = [1.0, 1.2, 1.5, 1.3, 1.8]$$

Parâmetros definidos:
* Atraso (`delay`): $\tau = 1$
* Dimensão (`dimension`): $m = 2$
* Épsilon (`eps`): $\epsilon = 0.0$ (para fins didáticos)

#### Passo 1 Reconstrução do Espaço de Estados
Número de estados $M = N - (m - 1)\tau = 5 - (2 - 1)(1) = 4$.

* $X_0 = (x_0, x_1) = (1.0, 1.2)$
* $X_1 = (x_1, x_2) = (1.2, 1.5)$
* $X_2 = (x_2, x_3) = (1.5, 1.3)$
* $X_3 = (x_3, x_4) = (1.3, 1.8)$

#### Passo 2 Matriz de Distâncias Euclidianas entre Estados

Cálculo das distâncias $d(X_i, X_j) = \sqrt{(x_{i,0}-x_{j,0})^2 + (x_{i,1}-x_{j,1})^2}$:

* $d(X_0, X_1) = \sqrt{(1.0-1.2)^2 + (1.2-1.5)^2} = \sqrt{0.04 + 0.09} = \sqrt{0.13} \approx 0.3606$
* $d(X_0, X_2) = \sqrt{(1.0-1.5)^2 + (1.2-1.3)^2} = \sqrt{0.25 + 0.01} = \sqrt{0.26} \approx 0.5099$
* $d(X_0, X_3) = \sqrt{(1.0-1.3)^2 + (1.2-1.8)^2} = \sqrt{0.09 + 0.36} = \sqrt{0.45} \approx 0.6708$
* $d(X_1, X_2) = \sqrt{(1.2-1.5)^2 + (1.5-1.3)^2} = \sqrt{0.09 + 0.04} = \sqrt{0.13} \approx 0.3606$
* $d(X_1, X_3) = \sqrt{(1.2-1.3)^2 + (1.5-1.8)^2} = \sqrt{0.01 + 0.09} = \sqrt{0.10} \approx 0.3162$
* $d(X_2, X_3) = \sqrt{(1.5-1.3)^2 + (1.3-1.8)^2} = \sqrt{0.04 + 0.25} = \sqrt{0.29} \approx 0.5385$

#### Passo 3 Identificação dos Vizinhos Mais Próximos
Desconsiderando a distância até si mesmo ($j \neq i$):
* Para $i = 0$: O ponto mais próximo é $j = 1$ ($d \approx 0.3606$).
* Para $i = 1$: O ponto mais próximo é $j = 3$ ($d \approx 0.3162$).
* Para $i = 2$: O ponto mais próximo é $j = 1$ ($d \approx 0.3606$).

#### Passo 4 Cálculo da Divergência Local $\log(d_1 / d_0)$

Iterando para $i$ de $0$ até $M-2 = 2$:

1. **Para $i = 0$ (vizinho $j = 1$):**
   * Distância inicial: $d_0 = \lVert X_0 - X_1 \rVert = 0.3606$
   * Distância no passo seguinte: $d_1 = \lVert X_1 - X_2 \rVert = 0.3606$
   * Divergência local: $\lambda_0 = \log(0.3606 / 0.3606) = \log(1.0) = 0.0$

2. **Para $i = 1$ (vizinho $j = 3$):**
   * Distância inicial: $d_0 = \lVert X_1 - X_3 \rVert = 0.3162$
   * Distância no passo seguinte: $d_1 = \lVert X_2 - X_4 \rVert$ (não existe estado $X_4$, o laço do código limita-se a $M-1$ pontos). 
   * *Nota do algoritmo*: O loop itera até $M-2$. Para $i=1$, os pontos seguintes são $X_{i+1} = X_2$ e $X_{j+1} = X_4$. Como $M=4$, os índices válidos de estado variam de 0 a 3.
   * Vamos calcular para $i=1$ com vizinho $j=2$:
     * $d_0 = \lVert X_1 - X_2 \rVert = 0.3606$
     * $d_1 = \lVert X_2 - X_3 \rVert = 0.5385$
     * Divergência local: $\lambda_1 = \log(0.5385 / 0.3606) = \log(1.4933) \approx 0.4010$

#### Passo 5 Média Global

$$\lambda = \frac{\lambda_0 + \lambda_1}{2} = \frac{0.0 + 0.4010}{2} = 0.2005$$

*Conclusão do Exemplo:* Como $\lambda = 0.2005 > 0$, o sinal demonstra um comportamento localmente amplificador.

---

### Lab Prático Sugerido em Python

Siga os passos abaixo para construir a função de estimativa do Expoente de Lyapunov com a biblioteca `numpy`:

#### Passo 1 Definir a assinatura da função e validação
Crie uma função `compute_lyapunov_exponent(signal, delay=1, dimension=3, eps=1e-6)`. Calcule o número total de estados válidos $M = N - (dimension - 1) \times delay$. Se $M \le 1$, retorne `np.nan`.

#### Passo 2 Reconstruir a matriz do espaço de estados
Utilize a técnica de compressão de listas em `numpy` para extrair amostras defasadas no tempo e transponha o resultado para obter a matriz de estados $X$ de dimensão $(M, dimension)$:
```python
X = np.array([signal[i:i + M] for i in range(0, dimension * delay, delay)]).T
```

#### Passo 3 Calcular a matriz de distâncias e identificar vizinhos
Calcule a norma euclidiana entre todos os pares de vetores de estado. Preencha a diagonal principal da matriz com `np.inf` para ignorar distâncias de um estado até ele mesmo, e identifique o índice do menor valor por linha com `np.argmin`:
```python
dists = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=-1)
np.fill_diagonal(dists, np.inf)
nearest = np.argmin(dists, axis=1)
```

#### Passo 4 Iterar sobre os estados e medir a divergência temporal
Para cada estado $i$ de $0$ até $M-2$, recupere o vizinho $j = nearest[i]$. Calcule as distâncias euclidianas $d_0 = \lVert X_i - X_j \rVert + eps$ e $d_1 = \lVert X_{i+1} - X_{j+1} \rVert + eps$. Calcule o valor logarítmico `log_div = np.log(d1 / d0)` e adicione à lista de divergências.

#### Passo 5 Retornar a média
Retorne o valor médio flutuante da lista de divergências locais usando `float(np.mean(diverge))`.

---

### Glossário

* **Atraso Temporal (`delay` / $\tau$):** Parâmetro de amostragem que define a distância fixa entre os pontos passados utilizados para construir a memória do estado.
* **Dimensão de Incorporação (`dimension` / $m$):** Número de variáveis/pontos temporais necessários para definir completamente o estado dinâmico do sistema em um espaço vetorial.
* **Divergência Local ($\lambda_{\mathrm{local}}$):** Taxa de variação logarítmica da distância entre dois estados inicialmente próximos após um passo temporal.
* **Espaço de Estados (State Space):** Representação geométrica abstrata onde cada ponto representa o estado completo de um sistema dinâmico em um instante.
* **Gêmeo Quase-Idêntico (Nearest Neighbor):** Estado reconstruído no passado que possui a menor distância euclidiana em relação ao estado atual analisado.
* **Regime Amplificador ($\lambda > 0$):** Condição de mercado caracterizada pela expansão de divergências e instabilidade estrutural, na qual pequenas perturbações geram reações em cadeia.
* **Regime Dissipativo ($\lambda < 0$):** Condição de mercado na qual as divergências se contraem e as perturbações são absorvidas pela estrutura interna do sistema.
* **Regularização ($\epsilon$ / `eps`):** Pequeno escalar adicionado aos cálculos de distância para evitar divisões por zero ou valores indefinidos no logaritmo.

---

### Questões de Fixação e Aplicação

#### Nível 1 Básico

1. O Expoente de Lyapunov é utilizado no trading para prever se o preço de um ativo vai subir ou cair? Justifique.
2. Qual a função do parâmetro `eps` no cálculo da divergência local?
3. O que indica um Expoente de Lyapunov com valor negativo ($\lambda < 0$)?

#### Nível 2 Intermediário

4. Explique por que a reconstituição do espaço de estados utiliza os parâmetros `delay` e `dimension` em vez de analisar um único preço $x_t$ isolado no tempo.
5. Qual a justificativa matemática para aplicar a função logarítmica na razão das distâncias $\log(d_1 / d_0)$ ao avaliar a propagação de perturbações?

#### Nível 3 Avançado

6. Considere que um algoritmo de quant trading detectou um Expoente de Lyapunov próximo de zero ($\lambda \approx 0$) durante um período de baixa volatilidade no mercado. Como a mesa de risco deve interpretar esse regime de mercado e quais são os perigos de se assumir alavancagem excessiva nessa condição?

---

### Gabarito e Respostas Explicadas

1. **Resposta:** Não. O Expoente de Lyapunov não mede direção nem tendência de preço. Ele mede a taxa de propagação de perturbações dentro do sistema, indicando se um regime de mercado tende a dissipar ou amplificar anomalias locais.
2. **Resposta:** O parâmetro `eps` ($\epsilon = 1e-6$) atua como uma constante de regularização numérica. Sua função é impedir erros matemáticos (como divisão por zero ou logaritmo de zero) caso dois estados sejam numericamente idênticos e resultem em $d_0 = 0$ ou $d_1 = 0$.
3. **Resposta:** Indica que o sistema está em um regime dissipativo. As perturbações e anomalias são absorvidas e neutralizadas ao longo do tempo, atuando como um amortecedor de choques.
4. **Resposta:** O mercado financeiro é um sistema dinâmico cujas opções futuras são condicionadas pelo rastro recente de suas ações. Um ponto isolado $x_t$ não possui memória. A combinação de pontos defasados com `delay` ($\tau$) e `dimension` ($m$) reconstrói a estrutura geométrica interna e a tensão do sistema no espaço de estados.
5. **Resposta:** Perturbações em sistemas instáveis propagam-se segundo uma lei de amplificação exponencial (lógica de contaminação/reação em cadeia). Aplicar o logaritmo traz essa taxa exponencial para uma escala linear, permitindo extrair uma taxa média de contaminação comparável.
6. **Resposta:** Um regime com $\lambda \approx 0$ representa um estado de borda ou limite. Embora a superfície do mercado pareça calma e a volatilidade atual seja baixa, a estabilidade não possui margem de segurança. O sistema não está dissipando perturbações. Assumir alta alavancagem nesse cenário é perigoso porque qualquer pequeno choque exógeno pode empurrar o sistema para um regime de amplificação ($\lambda > 0$), desencadeando rupturas e volatilidade extrema sem aviso prévio.