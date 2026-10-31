<!-- imported from vault study notes; curated for open course -->
# M06.A01 — Histerese e dependência de trajetória no risco de cauda

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M06
> **Aula:** M06.A01

↑ M06 · Resumo · Completo

**Módulo:** M06
**Pergunta do módulo:** Por que trajetória e caos importam no drawdown e na previsibilidade?

## Conceito-núcleo
Histerese: o estado atual depende do caminho; fat tails vs gaussiana; memória de stress.

## Aplicação em mercado / trading
Não tratar volatilidade realizada como simétrica no tempo; ajustar stops/sizing após trajetórias extremas.

## Entregável / lab
Comparar densidades gaussiana vs fat-tailed; calculate_tail_density em janela móvel.

## Fonte (mapeamento)
quantitative-trading-free-lesson/22 hysteresis-and-path-dependence | IG hysteresis / fat tails

## Guia de estudo aprofundado

> **info**
>

Este guia destina-se ao estudo aprofundado dos mecanismos de risco dinâmico, histerese e memória em séries temporais financeiras, abordando como métricas de entropia, persistência e divergência revelam rupturas estruturais ocultas no mercado.

---

### Conceitos-Chave Explicados em Profundidade

#### Risco Dinâmico e Histerese
As métricas tradicionais de risco observam o mercado de forma estática, medindo a amplitude do movimento (como a volatilidade). No entanto, o risco opera como uma dinâmica de fluxo que se deforma, atinge bloqueios e satura. A **histerese** e a **dependência de trajetória** estabelecem que um sistema financeiro pode retornar à normalidade na superfície (preços estáveis), mas continuar marcado e restrito em sua estrutura subjacente. O caminho percorrido pelo mercado altera o próprio estado do regime.

#### Entropia de Shannon (Legibilidade do Sinal)
A Entropia de Shannon não mede o quanto o mercado se move, mas sim se a mensagem do mercado continua estruturada ou se tornou tão desorganizada a ponto de perder a legibilidade.
* **Sinal Estruturado (Próximo de 0):** Poucos estados dominam o comportamento dos retornos; o sinal retém significado legível.
* **Sinal Desorganizado (Próximo de 1):** Os estados tornam-se uniformes, ocorrendo um colapso na legibilidade da informação.

#### Expoente de Hurst (Memória e Traço do Sistema)
O Expoente de Hurst ($H$) avalia a existência de uma memória ativa deixada por choques passados.
* **$H \approx 0.5$:** Memória longa fraca ou inexistente (passeio aleatório).
* **$H > 0.5$:** Persistência. O passado continua pesando sobre o presente; o sistema guarda o traço do choque e o risco torna-se condicional ao caminho percorrido.

#### Expoente de Lyapunov (Velocidade de Propagação da Memória)
O Expoente de Lyapunov ($\lambda$) mede quão rápido uma pequena perturbação se propaga e se amplia no espaço de estados.
* **$\lambda > 0$:** Divergência rápida de estados próximos. A perturbação se propaga e se amplifica.
* **$\lambda \approx 0$:** Neutralidade do sistema.
* **$\lambda < 0$:** Contração e dissipação da perturbação.

#### Classificação Integrada dos Regimes de Risco
A combinação desses três indicadores permite diagnosticar o estado de regime do mercado antes que a mudança de preço se torne visível:

| Estado de Risco | Entropia ($H_{\text{ent}}$) | Hurst ($H$) | Lyapunov ($\lambda$) | Descrição Estrutural |
| :--- | :--- | :--- | :--- | :--- |
| `latent` | Normal | Normal | $\le 0$ | Nada se alterou criticamente na estrutura; os limites de risco não foram cruzados. |
| `propagating_instability` | Qualquer | Qualquer | $> 0$ | O canal de propagação está ativo; perturbações transmitem-se rapidamente. |
| `chaotic_memory` | $> 0.9$ | $> 0.5$ | $\le 0$ | O passado pesa sobre o presente, mas dentro de um ambiente informativo caótico e ilegível. |
| `structural_time_bomb` | $> 0.9$ | $> 0.5$ | $> 0$ | Memória persistente, alta entropia e rápida propagação. Condições de ruptura iminente instaladas. |

---

### Formulação Matemática

#### Entropia de Shannon Normalizada
A entropia da distribuição de probabilidade dos retornos $p_i$ dividida em compartimentos (*bins*) é dada por:

$$H = -\sum_{i} p_i \log_2(p_i)$$

Para normalizar o resultado no intervalo $$, divide-se pela entropia máxima possível $H_{\max}$:

$$H_{\max} = \log_2(N_{\text{bins}})$$

$$H_{\text{norm}} = \frac{H}{H_{\max}}$$

#### Expoente de Hurst via R/S (Rango Reescalado)
Para subintervalos de tamanho $w$, calcula-se a amplitude acumulada desviada $R$ e o desvio padrão $S$. A relação de escala obedece a:

$$\mathbb{E}\left[\frac{R(w)}{S(w)}\right] \propto w^H$$

Aplicando o logaritmo em ambos os lados, o expoente $H$ é obtido como a inclinação da regressão linear:

$$\ln\left(\frac{R}{S}\right) = H \cdot \ln(w) + C$$

#### Expoente de Lyapunov e Espaço de Estados
A taxa de divergência exponencial entre dois estados inicialmente próximos $X_0$ e $X_0 + \delta X_0$ é expressa por:

$$|\delta X_t| \approx |\delta X_0| e^{\lambda t}$$

Isolando a taxa de propagação $\lambda$:

$$\lambda \approx \frac{1}{t} \ln \left( \frac{|\delta X_t|}{|\delta X_0|} \right)$$

No espaço de estados reconstruído $X$, a inclinação da média temporal dos logaritmos das distâncias $\ln(d(t))$ fornece o proxy numérico de $\lambda$.

---

### Intuição de Mercado e Trading

Na prática de trading e gestão de risco, a maioria dos modelos falha por avaliar o risco apenas quando a variação dos preços acontece. A abordagem por histerese demonstra que:

1. **A superfície mente:** O preço pode estar consolidado e com baixa volatilidade aparente, mas se o regime for classificado como `structural_time_bomb`, o sistema perdeu a capacidade de dissipar perturbações.
2. **A memória altera a reação:** Em regimes com $H > 0.5$, o mercado reage a um choque não como um evento isolado, mas acumulando o histórico recente. 
3. **Canais de contágio e velocidade:** Um Lyapunov positivo ($\lambda > 0$) avisa ao gestor que qualquer fluxo imbalanceado pontual não será absorvido pela liquidez, mas amplificado ao longo do espaço de estados.

---

### Exemplo Numérico Resolvido Passo a Passo

#### Problema 1 Cálculo da Entropia de Shannon Normalizada
Considere uma série temporal curta de 8 retornos categorizados em $N_{\text{bins}} = 4$ intervalos. A contagem de frequências resultou em:
* Bin 1: 4 observações
* Bin 2: 2 observações
* Bin 3: 2 observações
* Bin 4: 0 observações

**Passo 1: Calcular as probabilidades $p_i$ para cada bin.**
* Total de observações = $4 + 2 + 2 + 0 = 8$
* $p_1 = \frac{4}{8} = 0.5$
* $p_2 = \frac{2}{8} = 0.25$
* $p_3 = \frac{2}{8} = 0.25$
* $p_4 = \frac{0}{8} = 0.0$ (desconsiderado no cálculo da entropia pois $p_4 > 0$ é falso)

**Passo 2: Calcular a Entropia de Shannon bruta ($H$).**
$$H = - \left( p_1 \log_2(p_1) + p_2 \log_2(p_2) + p_3 \log_2(p_3) \right)$$
* $p_1 \log_2(p_1) = 0.5 \cdot \log_2(0.5) = 0.5 \cdot (-1) = -0.5$
* $p_2 \log_2(p_2) = 0.25 \cdot \log_2(0.25) = 0.25 \cdot (-2) = -0.5$
* $p_3 \log_2(p_3) = 0.25 \cdot \log_2(0.25) = 0.25 \cdot (-2) = -0.5$

$$H = - (-0.5 - 0.5 - 0.5) = 1.5 \text{ bits}$$

**Passo 3: Calcular a Entropia Máxima ($H_{\max}$).**
$$H_{\max} = \log_2(N_{\text{bins}}) = \log_2(4) = 2.0 \text{ bits}$$

**Passo 4: Calcular a Entropia Normalizada ($H_{\text{norm}}$).**
$$H_{\text{norm}} = \frac{H}{H_{\max}} = \frac{1.5}{2.0} = 0.75$$

---

#### Problema 2 Estimativa do Taxa de Divergência de Lyapunov
Dois pontos no espaço de estados possuem uma distância inicial $|\delta X_0| = 0.02$. Após $t = 5$ passos temporais, a distância entre suas trajetórias expandiu para $|\delta X_5| = 0.14778$.

**Passo 1: Aplicar a equação de divergência.**
$$|\delta X_5| = |\delta X_0| e^{\lambda \cdot 5}$$
$$0.14778 = 0.02 \cdot e^{5\lambda}$$

**Passo 2: Isolar o termo exponencial.**
$$\frac{0.14778}{0.02} = 7.389$$
$$e^{5\lambda} = 7.389$$

**Passo 3: Aplicar o logaritmo natural em ambos os lados e resolver para $\lambda$.**
$$5\lambda = \ln(7.389) \approx 2.0$$
$$\lambda = \frac{2.0}{5} = 0.4$$

**Conclusão:** Como $\lambda = 0.4 > 0$, o sistema apresenta taxa de divergência positiva, caracterizando propagação de instabilidade.

---

### Armadilhas Comuns

1. **Confundir Volatilidade com Desorganização:** A volatilidade mede a dispersão/amplitude dos preços, enquanto a Entropia mede a perda de estrutura informativa. Um mercado pode ser altamente volátil, porém perfeitamente estruturado e previsível.
2. **Inclusão de Vizinhos Temporais Triviais no Cálculo de Lyapunov:** Ao reconstruir o espaço de estados, buscar o ponto mais próximo sem definir uma separação temporal mínima (`min_separation`) faz com que o algoritmo selecione o ponto imediatamente anterior ou posterior na série. Isso mascara a divergência real e gera estimativas falsas de $\lambda$.
3. **Leitura Isolada dos Indicadores:** Analisar o Expoente de Hurst isoladamente pode sugerir que a memória é benigna. No entanto, se combinada com alta entropia ($>0.9$) e Lyapunov positivo, trata-se de uma "bomba relógio estrutural".
4. **Tratar o Risco como Medida de Nível:** Achar que o risco baixou simplesmente porque o drawdown estagnou. A histerese indica que o sistema permanece fragilizado pelo caminho percorrido.

---

### Laboratório Prático em Python

Siga os passos abaixo para implementar o sistema de detecção de regime de risco dinâmico:

#### Passo 1 Importação de Bibliotecas e Preparação
Utilize a biblioteca `numpy` para operações vetoriais e tratamento de séries de retornos. Caso a série apresente desvio padrão zero, adicione um ruído infinitesimal para evitar divisão por zero.

#### Passo 2 Implementação da Entropia de Shannon
1. Crie um histograma dos retornos com `bins=30`.
2. Converta as contagens em probabilidades $p$.
3. Filtre valores $p > 0$.
4. Calcule $H = -\sum p \log_2(p)$ e normalize dividindo por $\log_2(\text{quantidade de bins})$.

#### Passo 3 Implementação do Expoente de Hurst via R/S
1. Centralize a série subtraindo a média.
2. Defina tamanhos de janela logarítmicos entre uma janela mínima (ex: 16) e $N/2$.
3. Para cada tamanho de janela, divida a série em segmentos, calcule a média acumulada desviada, obtenha o intervalo $R$ (máximo - mínimo) e a desvio padrão $S$.
4. Ajuste uma regressão linear (`np.polyfit`) entre $\ln(\text{janelas})$ e $\ln(R/S)$ para extrair o coeficiente angular $H$.

#### Passo 4 Reconstrução de Espaço de Estados e Lyapunov
1. Construa a matriz do espaço de estados $X$ combinando a série defasada com dimensão de embutimento `emb_dim=3` e atraso `lag=1`.
2. Para cada estado $i$, encontre o vizinho mais próximo $j$ usando a norma euclidiana, garantindo uma separação temporal $|i - j| > \text{min\_separation}$.
3. Acompanhe a variação da distância euclidiana entre as trajetórias dos pares $(i+k, j+k)$ ao longo de um horizonte $k$.
4. Calcule a inclinação da média do logaritmo das distâncias ao longo do tempo usando regressão linear.

#### Passo 5 Classificação de Regime de Risco
Defina uma função agregadora que receba os retornos e execute as regras condicionais:
* Se $H_{\text{hurst}} > 0.5$, $H_{\text{ent}} > 0.9$ e $\lambda > 0 \implies$ `"structural_time_bomb"`
* Senão, se $H_{\text{hurst}} > 0.5$ e $H_{\text{ent}} > 0.9 \implies$ `"chaotic_memory"`
* Senão, se $\lambda > 0 \implies$ `"propagating_instability"`
* Caso contrário $\implies$ `"latent"`

---

### Glossário

* **Dependência de Trajetória (Path Dependence):** Propriedade de sistemas dinâmicos onde o estado atual depende de toda a sequência de estados anteriores, e não apenas da posição no instante atual.
* **Entropia de Shannon:** Medida da incerteza ou desordem na distribuição de frequências do sinal de um sistema.
* **Expoente de Hurst:** Indicador quantitativo de dependência de longo prazo e autocorrelação em séries temporais.
* **Expoente de Lyapunov:** Medida da taxa média de divergência ou convergência exponencial de trajetórias vizinhas no espaço de estados.
* **Histerese:** Fenômeno em que a resposta de um sistema a um estímulo depende do histórico do sistema, mantendo traços de perturbações passadas mesmo após a remoção do estímulo.
* **Reconstrução do Espaço de Estados:** Técnica que transforma uma série temporal unidimensional em uma trajetória vetorial multidimensional utilizando atrasos temporais.
* **Structural Time Bomb:** Estado crítico de risco caracterizado simultaneamente por persistência de memória, colapso na legibilidade da informação e propagação rápida de perturbações.

---

### Questões e Exercícios Práticos

#### Nível 1 Básico (Respostas Curtas)

**Questão 1:** Qual é a diferença fundamental entre o que a Entropia de Shannon mede e o que a volatilidade tradicional mede em uma série financeira?  
*Resposta:* A volatilidade mede a amplitude ou variação do movimento dos preços. A Entropia de Shannon mede o grau de desorganização e perda de estrutura do sinal, ou seja, se o movimento do mercado ainda possui legibilidade e significado estruturado.

**Questão 2:** O que indica um Expoente de Hurst ($H$) maior que 0.5 em uma série de retornos de mercado?  
*Resposta:* Indica persistência ou memória de longo prazo no sistema. Significa que os choques passados deixam um traço ativo e o comportamento futuro retém dependência do caminho percorrido.

---

#### Nível 2 Intermediário (Aplicação e Análise)

**Questão 3:** Um modelo de análise de risco detectou que o Expoente de Lyapunov ($\lambda$) de um ativo tornou-se positivo ($\lambda > 0$), mas a volatilidade do preço permanece extremamente baixa. Como o gestor de risco deve interpretar esse cenário?  
*Resposta:* O gestor deve interpretar como um estado de instabilidade propagativa (`propagating_instability`). Embora a superfície do preço pareça calma, o canal de propagação de memória está ativo. Qualquer pequena perturbação externa ou choque pontual não será dissipado, mas amplificado rapidamente através do espaço de estados do sistema.

**Questão 4:** Ao calcular o Expoente de Lyapunov, por que é crítico aplicar o parâmetro de separação temporal mínima (`min_separation`) na busca de vizinhos no espaço de estados?  
*Resposta:* O parâmetro `min_separation` impede que o algoritmo escolha como vizinho mais próximo um ponto imediatamente adjacente no tempo ($i \pm 1$). Sem essa restrição, a proximidade temporal natural da série cria uma ilusão de continuidade estática, mascarando a divergência real das trajetórias e invalidando a estimativa do expoente.

---

#### Nível 3 Avançado (Dissertativo)

**Questão 5:** Explique como a convergência dos três indicadores (Entropia de Shannon, Expoente de Hurst e Expoente de Lyapunov) gera a condição classificada como `structural_time_bomb`. Qual é a dinâmica de mercado associada a esse estado e por que as métricas tradicionais de risco falham em detectá-la?

*Resposta:*  
A condição de `structural_time_bomb` ocorre quando o mercado apresenta simultaneamente:
1. **$H_{\text{hurst}} > 0.5$ (Memória Persistente):** O sistema não esquece choques passados; cada evento acumula tensão e altera o estado do regime.
2. **$H_{\text{ent}} > 0.9$ (Caos Informativo):** O sinal torna-se completamente desorganizado e ilegível, eliminando a eficiência na formação de preços.
3. **$\lambda > 0$ (Amplificação Exponencial):** O sistema perde a capacidade de dissipar perturbações, passando a propagar e ampliar divergências no espaço de estados.

A dinâmica de mercado associada a esse estado é a de uma ruptura iminente em tempo real. O mercado acumula restrições internas e dependência de trajetória, mas a superfície do preço ainda não imprimiu o movimento catastrófico final. 

As métricas tradicionais de risco (como VaR e Volatilidade Histórica) falham totalmente porque analisam apenas a amplitude estática recente ou assumem uma distribuição cujos choques são independentes e dissipativos. Elas observam o nível atual, e não o traço histórico acumulado (histerese), sendo incapazes de notar que as leis operacionais da estrutura já mudaram por baixo da superfície.