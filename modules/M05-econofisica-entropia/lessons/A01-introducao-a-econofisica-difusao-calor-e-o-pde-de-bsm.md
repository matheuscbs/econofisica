<!-- imported from vault study notes; curated for open course -->
# M05.A01 — Introdução à econofísica: difusão, calor e o PDE de BSM

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M05
> **Aula:** M05.A01

↑ M05 · Resumo · Completo

**Módulo:** M05
**Pergunta do módulo:** O que a econofísica muda na leitura de incerteza e risco?

## Conceito-núcleo
Analogia difusão/calor ↔ PDE BSM; mercados como sistemas com leis efetivas mensuráveis.

## Aplicação em mercado / trading
Trocar narrativa “previsão de preço” por leis empíricas (entropia, resposta à variância, regimes).

## Entregável / lab
Mapa mental: qual analogia física vira qual métrica de trading (entropy, collapse, tail density).

## Fonte (mapeamento)
quantitative-trading-free-lesson/18 introduction to econophysics | IG intro econofísica + difusão BSM

## Guia de estudo aprofundado

> **info**
>

Este guia de estudo estabelece uma abordagem rigorosa sobre a aplicação de conceitos da física estatística e termodinâmica no entendimento dos mercados financeiros. O foco central é a diferenciação entre volatilidade e risco, o mecanismo de difusão de estresse e restrições, e o papel da entropia informacional na degradação da legibilidade do mercado.

---

### Conceitos-Chave e Intuição de Mercado

#### Diferença Fundamental Volatilidade vs. Risco

A confusão entre volatilidade e risco leva à leitura incorreta do mercado por meio de instrumentos inadequados. A divisão real nos mercados não é entre "o mercado se move" e "o mercado não se move", mas sim entre **movimento** e **ruptura**.

*   **Volatilidade ($\sigma$):** Mede o ritmo, a amplitude dos choques e a dispersão dos retornos ao redor da média. É o equivalente à **temperatura** na física (nível médio de agitação microbiana/particular). Descreve o ruído e a agitação observada, não a solidez ou a probabilidade de falha do sistema.
    $$\sigma^2 = E[(X-E[X])^2]$$
*   **Risco:** É a probabilidade condicional de ocorrência de um evento de **ruptura** (um evento não linear, como liquidação forçada, incapacidade de saída, gapping, cascatas, alargamento de spread, explosão de impacto de mercado, quebra de drawdown e falha de margem).
    $$\mathrm{risco} = P(\mathrm{ruptura} \mid \mathrm{restrições})$$

Um mercado pode ser altamente volátil e apresentar baixo risco (se for líquido, pouco alavancado, bem colateralizado e transparente). Por outro lado, um mercado pode parecer calmo (baixa volatilidade realizada) e ser extremamente perigoso/arisco por estar estruturalmente frágil, alavancado e com alta entropia.

#### Mecanismo de Difusão e a Equação do Calor

Na física, a difusão da energia em uma barra de metal aquecida em um ponto é expressa por:

$$\frac{\partial E}{\partial t} = D\nabla^2 E$$

Onde $E$ representa a energia e $D$ o coeficiente de difusão. 

*   **Intuição de Mercado:** O metal não se rompe simplesmente porque as partículas estão agitadas (temperatura/volatilidade alta). Ele se rompe porque a difusão de energia gera **gradientes** ($\nabla E$), que por sua vez geram tensões e restrições mecânicas internas (uma zona quente quer expandir, a zona fria adjacente não acompanha).
*   **Difusão Financeira:** Nos mercados, o que se difunde não é apenas o preço ou a temperatura, mas o **estresse financeiro** e as **restrições**. Um participante vende porque é forçado; a venda move o preço; o movimento degrada o colateral de outro participante; este recebe uma chamada de margem e vende por sua vez; a liquidez recua, o impacto aumenta e a fragilidade avança passo a passo pela rede.

#### Entropia Informacional e Legibilidade do Mercado

A entropia mede a dispersão de estados do sistema e a perda de legibilidade da sua configuração. A formulação informacional básica é dada por:

$$H = -\sum_i p_i \log p_i$$

Cada preço ou *tick* é uma atualização do estado do sistema. 
*   **Baixa Entropia:** A informação circula de forma limpa. O mercado é legível, permitindo estimativas e hipóteses consistentes.
*   **Alta Entropia:** A leitura do mercado torna-se borrada. Os participantes perdem a capacidade de saber qual preço é real, onde está a liquidez ou quem está prestes a desalavancar. 
*   **A Armadilha:** A entropia pode subir enquanto a volatilidade realizada permanece baixa. Quando a legibilidade degrada, os participantes abandonam o "modo cálculo" e entram no "modo defensivo", momento em que a estrutura se tenciona e o risco se torna ativo.

#### Formulação Geral do Risco Sistêmico

Unindo a mecânica das restrições e a qualidade da informação, o risco é formalizado como:

$$\mathrm{risco} = P(\mathrm{ruptura} \mid \mathrm{estrutura},\ \mathrm{restrições},\ \mathrm{entropia})$$

As restrições do sistema incluem: liquidez, alavancagem, financiamento (*funding*), colateral, concentração, chamadas de margem, profundidade do livro de ofertas (*order book*), dependências entre ativos, travamento de correlações e velocidade do dinheiro.

---

### Exemplo Numérico Resolvido Passo a Passo

#### Problema

Considere um sistema simplificado de mercado composto por 3 estados possíveis de liquidez ($S_1, S_2, S_3$) com distribuições de probabilidade sob duas condições distintas de mercado (Cenário A e Cenário B). Cada estado possui um impacto financeiro associado $X$ (retorno percentual do ativo).

*   **Valores do impacto ($X$):** $S_1 = -2\%$, $S_2 = 0\%$, $S_3 = +2\%$.
*   **Cenário A (Mercado Transparente / Baixa Entropia):**
    *   $p(S_1) = 0,10$
    *   $p(S_2) = 0,80$
    *   $p(S_3) = 0,10$
*   **Cenário B (Mercado Ilíquido e Indeterminado / Alta Entropia):**
    *   $p(S_1) = 0,333$
    *   $p(S_2) = 0,333$
    *   $p(S_3) = 0,334$

Calcule, para cada cenário:
1. O valor esperado $E[X]$.
2. A volatilidade (variância $\sigma^2$ e desvio-padrão $\sigma$).
3. A entropia informacional $H$ (utilizando o logaritmo natural $\ln$).
4. Analise o nível de legibilidade do sistema em cada cenário.

---

#### Solução Passo a Passo

##### Passo 1 Cálculo para o Cenário A

1. **Valor Esperado $E[X_A]$:**
   $$E[X_A] = (0,10 \times -2) + (0,80 \times 0) + (0,10 \times 2) = -0,2 + 0 + 0,2 = 0\%$$

2. **Variância $\sigma_A^2$ e Desvio-Padrão $\sigma_A$:**
   $$\sigma_A^2 = 0,10 \times (-2 - 0)^2 + 0,80 \times (0 - 0)^2 + 0,10 \times (2 - 0)^2$$
   $$\sigma_A^2 = 0,10 \times 4 + 0 + 0,10 \times 4 = 0,4 + 0,4 = 0,80$$
   $$\sigma_A = \sqrt{0,80} \approx 0,894\%$$

3. **Entropia Informacional $H_A$:**
   $$H_A = - [p(S_1)\ln p(S_1) + p(S_2)\ln p(S_2) + p(S_3)\ln p(S_3)]$$
   $$H_A = - [0,10 \times \ln(0,10) + 0,80 \times \ln(0,80) + 0,10 \times \ln(0,10)]$$
   $$\ln(0,10) \approx -2,3026 \quad \text{e} \quad \ln(0,80) \approx -0,2231$$
   $$H_A = - [0,10 \times (-2,3026) + 0,80 \times (-0,2231) + 0,10 \times (-2,3026)]$$
   $$H_A = - [-0,23026 - 0,17848 - 0,23026] = - [-0,6390] = 0,6390 \text{ nats}$$

---

##### Passo 2 Cálculo para o Cenário B

1. **Valor Esperado $E[X_B]$:**
   $$E[X_B] = (0,333 \times -2) + (0,333 \times 0) + (0,334 \times 2) = -0,666 + 0 + 0,668 = +0,002\% \approx 0\%$$

2. **Variância $\sigma_B^2$ e Desvio-Padrão $\sigma_B$:**
   $$\sigma_B^2 = 0,333 \times (-2)^2 + 0,333 \times (0)^2 + 0,334 \times (2)^2$$
   $$\sigma_B^2 = 0,333 \times 4 + 0 + 0,334 \times 4 = 1,332 + 1,336 = 2,668$$
   $$\sigma_B = \sqrt{2,668} \approx 1,633\%$$

3. **Entropia Informacional $H_B$:**
   $$H_B = - [0,333 \times \ln(0,333) + 0,333 \times \ln(0,333) + 0,334 \times \ln(0,334)]$$
   $$\ln(0,333) \approx -1,0996 \quad \text{e} \quad \ln(0,334) \approx -1,0966$$
   $$H_B = - [0,333 \times (-1,0996) + 0,333 \times (-1,0996) + 0,334 \times (-1,0966)]$$
   $$H_B = - [-0,3662 - 0,3662 - 0,3663] = 1,0987 \text{ nats}$$

---

##### Passo 3 Comparação e Análise

| Métrica | Cenário A | Cenário B | Interpretação |
| :--- | :--- | :--- | :--- |
| **Média $E[X]$** | $0,00\%$ | $0,00\%$ | Retorno esperado idêntico |
| **Volatilidade ($\sigma$)** | $0,894\%$ | $1,633\%$ | Cenário B apresenta variabilidade quase duas vezes maior |
| **Entropia ($H$)** | $0,6390$ | $1,0987$ | A entropia no Cenário B está próxima do seu máximo teórico ($\ln(3) \approx 1,0986$) |

**Conclusão da Análise:** No Cenário B, a incerteza quanto ao estado do sistema é máxima ($H_B \approx \ln(3)$). A legibilidade do mercado foi severamente degradada, o que significa que os agentes incapazes de prever o estado da liquidez assumem postura defensiva, aumentando drasticamente a probabilidade de ruptura $P(\mathrm{ruptura})$ frente a qualquer choque marginal de restrição.

---

### Armadilhas Comuns

*   **Proxy Automático de Risco:** Tratar a volatilidade como a medida direta e única de risco. A volatilidade mede apenas a amplitude das oscilações em torno da média (ruído), enquanto o risco trata da sustentabilidade do sistema sob restrições estressadas.
*   **Ilusão de Calmaria:** Assumir que mercados com baixa volatilidade realizada são intrinsecamente seguros. Um mercado calmo na superfície pode estar em estado de alta entropia informacional e com restrições tencionadas (alta alavancagem, pouca profundidade de livro e colaterais frágeis), tornando-o vulnerável a rupturas não lineares violentas.
*   **Foco Exclusivo em Sensibilidade Local:** Limitar a análise de risco a perguntas locais do tipo "quanto perco se o mercado mover $X\%$?". A análise real exige identificar a probabilidade de ruptura sistêmica gerada pelo efeito cascata das restrições financeiras.
*   **Erros na Modelagem de Difusão:** Considerar que a difusão no mercado transporta apenas variação de preços. Na prática, o que difunde ao longo da rede de participantes é o estresse financeiro e a degradação de restrições (margens, colateral e liquidez).

---

### Laboratório Prático em Python

Este laboratório propõe a simulação da difusão de estresse financeiro em uma rede de agentes acoplados por restrições de colateral e chamadas de margem.

#### Passos de Implementação

1.  **Instalação e Configuração do Ambiente:**
    *   Importe as bibliotecas necessárias: `numpy` para cálculos matriciais e `matplotlib.pyplot` para geração de gráficos.

2.  **Inicialização da Estrutura da Rede:**
    *   Crie um vetor com $N = 100$ participantes (agentes).
    *   Defina os níveis iniciais de colateral de cada agente, alavancagem e limites de margem.
    *   Configure a matriz de adjacência ou acoplamento, representando as conexões contratuais entre os agentes.

3.  **Injeção do Choque Inicial (Fonte de Gradiente):**
    *   Aplique um choque de preço/estresse localizado no agente $k=0$ (equivalente ao aquecimento pontual na barra de metal).

4.  **Loop da Equação de Difusão de Estresse:**
    *   Simule iterativamente a propagação do estresse $E_i(t)$ no tempo $t$ usando uma versão discretizada da equação de difusão:
        $$E_i(t+1) = E_i(t) + D \cdot \left[ E_{i+1}(t) - 2E_i(t) + E_{i-1}(t) \right]$$
    *   Em cada iteração, verifique se o nível de estresse $E_i(t)$ ultrapassa o limite de restrição de margem do agente $i$.

5.  **Simulação do Efeito Cascata (Ruptura):**
    *   Se o estresse ultrapassar o limite de margem, force a liquidação da posição do agente.
    *   A liquidação forçada adiciona um pico pontual de estresse nos agentes vizinhos, alterando a taxa local de difusão $D$ e reduzindo a liquidez do livro.

6.  **Cálculo das Métricas de Módulo (Volatilidade vs. Entropia):**
    *   A cada passo $t$, calcule o desvio-padrão dos níveis de estresse ($\sigma$) e a entropia informacional ($H$) da distribuição do estresse entre os agentes.

7.  **Visualização dos Resultados:**
    *   Gere um gráfico contendo:
        *   Perfil espacial do estresse ao longo dos agentes no tempo.
        *   Evolução temporal da volatilidade observada vs. ocorrência de eventos de liquidação/ruptura sistêmica.

---

### Glossário

*   **Difusão:** Processo físico pelo qual uma grandeza (como energia, calor ou estresse) se propaga através de uma estrutura através de interações locais contínuas.
*   **Entropia Informacional ($H$):** Medida probabilística da incerteza ou falta de legibilidade do estado de um sistema. Quanto maior a entropia, menor a transparência das condições reais do mercado.
*   **Gradiente de Energia ($\nabla E$):** Diferença espacial na distribuição de energia dentro de uma estrutura. Na econofísica, gradientes de estresse geram forças e restrições internas que causam rupturas.
*   **Legibilidade do Mercado:** Capacidade dos participantes de interpretar corretamente a qualidade da informação, preços reais, localização de liquidez e solvência dos pares no sistema.
*   **Restrições Financeiras:** Limitações estruturais que condicionam o comportamento dos agentes, como regras de margem, alavancagem máxima disponível, profundidade do livro de ordens, dependência de colateral e velocidade do dinheiro.
*   **Risco:** Probabilidade condicional de o sistema sofrer uma ruptura dada a sua estrutura, restrições e nível de entropia informacional.
*   **Ruptura:** Evento sistêmico não linear provocado pela incapacidade da estrutura absorver tensões internas (ex.: cascatas de chamadas de margem, liquidações forçadas, iliquidez repentina e congelamento de spreads).
*   **Volatilidade ($\sigma$):** Medida de dispersão estatística das flutuações de uma variável em torno da sua média. Indica o nível de agitação ou ruído, mas não a integridade estrutural do sistema.

---

### Questões e Exercícios

#### Nível 1 Resposta Curta e Conceitual

1. **Por que a volatilidade não deve ser utilizada como medida direta de risco sistêmico?**
   * **Resposta:** Porque a volatilidade mede apenas a amplitude das flutuações locais (ruído ou temperatura do sistema), enquanto o risco reflete a probabilidade condicional de uma ruptura sistêmica dependente de restrições estruturais (alavancagem, liquidez, colateral).

2. **Na analogia com a física do calor, qual elemento é o responsável direto por quebrar a estrutura de um metal?**
   * **Resposta:** Não é a temperatura em si (energia média/volatilidade), mas sim o gradiente de energia ($\nabla E$), que cria tensões e restrições mecânicas internas entre zonas quentes e frias.

3. **O que ocorre quando os participantes do mercado mudam do "modo cálculo" para o "modo defensivo"?**
   * **Resposta:** Essa transição ocorre quando a entropia informacional se eleva e o mercado perde a legibilidade. Os agentes deixam de calcular precificações finas e passam a proteger posições, acionando restrições estruturais e fechando a liquidez.

---

#### Nível 2 Aplicação Médio-Avançada

4. **Explique a afirmação: "Um mercado pode parecer calmo na superfície e já estar extremamente perigoso em sua estrutura".**
   * **Resposta:** Um mercado pode apresentar baixa volatilidade realizada observada (pouca movimentação de preços) e ao mesmo tempo acumular alta alavancagem, degradação de colaterais, opacidade de posições e alta entropia informacional. Quando o sistema perde legibilidade e possui restrições severas, qualquer choque marginal pode desencadear uma ruptura não linear instantânea.

5. **Como o processo de difusão se manifesta em uma crise de liquidação forçada encadeada?**
   * **Resposta:** O que se difunde no sistema é a restrição financeira (estresse). A venda forçada de um participante devido a uma chamada de margem derruba o preço, o que deprecia o colateral de outros agentes acoplados. Esses agentes enfrentam novas chamadas de margem e vendem em seguida, ampliando o spread e consumindo a profundidade do livro de ofertas em um processo difusivo de propagação de fragilidade.

---

#### Nível 3 Prompts para Redação e Análise Aprofundada

6. **Avalie o papel da Entropia Informacional na transição de um regime de mercado normal para um evento de estresse sistêmico.**
   * **Resposta Guiada:** O texto deve explorar como cada *tick* funciona como uma mensagem de atualização do estado do sistema. Quando a entropia $H = -\sum p_i \log p_i$ aumenta, a incerteza sobre quem está solvente, onde há liquidez real ou qual preço é justo cresce. A falta de transparência impede que os modelos tradicionais operem adequadamente. Com a perda da legibilidade, a resposta dos agentes torna-se não linear, acionando restrições operacionais simultâneas (desalavancagem e vendas a qualquer preço), transformando o estresse informacional em ruptura estrutural física do mercado.

7. **Compare a formulação tradicional do risco baseada na variância $\sigma^2$ com a formulação econofísica dada por $\mathrm{risco} = P(\mathrm{ruptura} \mid \mathrm{estrutura}, \mathrm{restrições}, \mathrm{entropia})$.**
   * **Resposta Guiada:** A resposta deve contrastar a visão estatística clássica (que trata o risco como dispersão simétrica e contínua dos retornos) com a abordagem econofísica. A formulação econofísica demonstra que o risco é uma probabilidade condicional de eventos discretos e não lineares (ruptura). Deve-se destacar o papel dos determinantes condicionantes: a **estrutura** (rede de agentes e dependências), as **restrições** (regras de margem, alavancagem, profundidade de ordem e financiamento) e a **entropia** (nível de degradação da informação circulante). A conclusão deve demonstrar por que sistemas de baixa volatilidade podem falhar miseravelmente sob a ótica clássica quando as restrições e a entropia não são contabilizadas.