<!-- imported from vault study notes; curated for open course -->
# M05.A02 — Teoria da informação e entropia: medir incerteza de retornos

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M05
> **Aula:** M05.A02

↑ M05 · Resumo · Completo

**Módulo:** M05
**Pergunta do módulo:** O que a econofísica muda na leitura de incerteza e risco?

## Conceito-núcleo
Entropia de Shannon em retornos binned: quanto a distribuição “surpreende”; informação vs ruído.

## Aplicação em mercado / trading
Monitorar regimes de incerteza; filtrar sinais quando entropia sobe (mercado menos previsível).

## Entregável / lab
Implementar calculate_entropy em janela móvel de retornos de 1 ativo líquido.

## Fonte (mapeamento)
quantitative-trading-free-lesson/19 information-theory-and-entropy | IG information theory

## Guia de estudo aprofundado

> **info**
>

Este guia de estudo aborda a aplicação da Teoria da Informação e da Entropia de Shannon no contexto dos mercados financeiros e do gerenciamento de risco, com base nos conceitos desenvolvidos por Karim Khemiri (Khem Kapital).

---

### Visão Geral e Introdução

No estudo dos mercados financeiros, é necessário distinguir movimento de risco e informação:
* **Volatilidade:** Mede a magnitude do movimento dos preços.
* **Risco:** Representa a probabilidade de ruptura, condicionada pela estrutura, pelas restrições e pelo estado informacional do sistema.
* **Mercado como fonte de informação:** Cada cotação é uma mensagem. Cada tick, variação de spread, desequilíbrio de volume ou retorno de preço é uma atualização parcial do estado do sistema. 

Quando o mercado é visto como uma fonte emissora contínua de informação, a entropia deixa de ser um conceito abstrato ou decorativo e passa a atuar como uma medida direta da **legibilidade do mercado**.

---

### Conceitos Chave

#### Surpresa e Entropia de Shannon

A informação transmitida por um evento depende de quão inesperado ele é. A **surpresa** $I(i)$ associada a um estado $i$ é expressa por:

$$I(i) = -\log(p_i)$$

* Se um evento é raro (pequena probabilidade $p_i$), sua surpresa é grande.
* Se um evento é frequente (alta probabilidade $p_i$), sua surpresa é pequena.

A **Entropia de Shannon** ($H$) de uma fonte mede a surpresa média associada aos estados possíveis emitidos por essa fonte:

$$H = -\sum_i p_i \log p_i$$

A entropia não mede "desordem" de forma vaga, mas sim a incerteza média do sistema:
* Se um estado domina o sistema, a incerteza cai e $H$ diminui.
* Se todos os estados se tornam aproximadamente equiprováveis, a incerteza sobe e $H$ aumenta.

#### Distribuição Uniforme e Colapso da Previsibilidade

Uma distribuição uniforme maximiza a entropia. Isso ocorre porque ela destrói qualquer predominância entre os estados. Quando nenhum estado é mais provável que outro, nenhum serve como guia. A previsibilidade colapsa não por falta de dados, mas pela ausência de uma estrutura dominante nos dados. As mensagens continuam sendo emitidas, mas saturam a leitura em vez de organizá-la.

#### Dinâmica da Entropia ($dH/dt$)

O nível absoluto de $H$ é importante, mas sua variação temporal é ainda mais crítica para o risco:

$$\frac{dH}{dt} > 0$$

Quando $\frac{dH}{dt} > 0$, a incerteza informacional está aumentando. Isso indica que:
1. A estrutura implícita do mercado está se degradando.
2. As regularidades e correlações úteis estão se esvaindo.
3. As mensagens emitidas pelo sistema assemelham-se cada vez mais a ruído e menos a um código legível.
4. O suporte informacional dos modelos estatísticos perde estabilidade operacional, pois a própria "geometria" do sistema se deforma durante o processo de medição.

#### A Tríade do Risco Informacional

A entropia sozinha não constitui um modelo completo de risco. Para transitar da detecção para a modelagem, a entropia deve ser combinada a duas outras dimensões:

| Dimensão | Papel no Sistema Informacional | Descrição |
| :--- | :--- | :--- |
| **Entropia** | Legibilidade | Mede a incerteza e a presença de estrutura no instante atual. |
| **Persistência** | Memória do Regime | Mede a capacidade do sistema de reter seu estado e manter coerência temporal. |
| **Circulação** | Transmissão do Sinal | Mede a fluidez com que a informação trafega sem sofrer distorções, atrasos, fragmentações ou amplificações patológicas. |

Sob essa ótica, o **risco** é redefinido como a probabilidade de o sistema perder estrutura, memória e capacidade de transmissão suficientes para que uma perturbação local se transforme em uma ruptura generalizada.

---

### Intuição de Mercado e Trading

#### O Fenômeno da Calmaria Perigosa

A situação mais perigosa para um trader ou gestor de risco ocorre quando o mercado apresenta **baixa volatilidade realizada**, mas **alta entropia**.

```
[ Volatilidade Realizada Baixa ] + [ Entropia Elevada (Alta Incerteza) ]
                 │
                 ▼
    [ Falsa Impressão de Calmaria ]
                 │
                 ▼
[ Choque Local Não Dispersado -> Propagação Direta -> Ruptura ]
```

* **Superfície:** As variações de preço são pequenas. Um analista focado apenas na volatilidade conclui que "nada está acontecendo".
* **Estrutura Subjacente:** As mensagens do mercado estão incoerentes, saturadas ou sem hierarquia clara. Os preços se movem pouco, mas deixam de informar adequadamente.
* **Mecanismo de Ruptura:** Em um sistema legível (baixa entropia), um pequeno choque é absorvido pelas estruturas existentes. Em um sistema saturado informacionalmente, o mesmo choque pequeno pode propagar-se sem dissipação, gerando uma transição rápida de regime.

#### Escolha do Alfabeto ($i$)

A entropia não existe no vácuo; ela depende da definição de um espaço de estados ou "alfabeto". Exemplos de alfabetos no trading incluem:
* Direção do tick: $i \in \{+, -, 0\}$ (alta, baixa, neutro).
* Classes discretizadas de retornos de preço.
* Configurações microestruturais (combinações de estados de spread e volume).
* Padrões locais em uma janela de tempo (entropia de permutação).

---

### Exemplo Numérico Resolvido Passo a Passo

Considere um mercado onde a direção dos ticks é observada a partir de um alfabeto de 3 estados: $i \in \{+, -, 0\}$. A fórmula da entropia utilizada será baseada no logaritmo de base 2, expressa em bits:

$$H = -\sum_i p_i \log_2(p_i)$$

#### Passo 1 Avaliar o Caso A (Mercado Estruturado / Baixa Entropia)

Suponha as seguintes probabilidades observadas em uma janela de tempo:
* $p_+ = 0{,}70$ (tendência clara de alta)
* $p_- = 0{,}20$
* $p_0 = 0{,}10$

Calcular a surpresa $I(i) = -\log_2(p_i)$ para cada estado:
* $I(+) = -\log_2(0{,}70) \approx -(-0{,}5146) = 0{,}5146 \text{ bits}$
* $I(-) = -\log_2(0{,}20) \approx -(-2{,}3219) = 2{,}3219 \text{ bits}$
* $I(0) = -\log_2(0{,}10) \approx -(-3{,}3219) = 3{,}3219 \text{ bits}$

Calcular a entropia $H_A$:
$$H_A = - [ (0{,}70 \times -0{,}5146) + (0{,}20 \times -2{,}3219) + (0{,}10 \times -3{,}3219) ]$$
$$H_A = - [ -0{,}3602 - 0{,}4644 - 0{,}3322 ] = 1{,}1568 \text{ bits}$$

#### Passo 2 Avaliar o Caso B (Mercado Saturado / Distribuição Uniforme)

Suponha agora que o mercado perdeu a estrutura e os estados se tornaram equiprováveis:
* $p_+ = 1/3 \approx 0{,}3333$
* $p_- = 1/3 \approx 0{,}3333$
* $p_0 = 1/3 \approx 0{,}3333$

Calcular a entropia $H_B$:
$$H_B = -\sum_{i=1}^3 \left(\frac{1}{3}\right) \log_2\left(\frac{1}{3}\right) = \log_2(3) \approx 1{,}5850 \text{ bits}$$

#### Passo 3 Interpretação dos Resultados

* $H_A = 1{,}1568 \text{ bits}$ (O estado $+$ domina o sistema. A legibilidade é alta e a incerteza é baixa).
* $H_B = 1{,}5850 \text{ bits}$ (A entropia atinge seu valor máximo para 3 estados. A legibilidade colapsou).
* A variação $\Delta H = H_B - H_A = +0{,}4282 \text{ bits}$ indica uma dinâmica $\frac{dH}{dt} > 0$, sinalizando degradação da estrutura informacional do mercado.

---

### Armadilhas Comuns

* **Equiparar Baixa Volatilidade a Baixo Risco:** Assumir que variações pequenas de preço garantem um ambiente seguro. A perda de legibilidade pode ocorrer em momentos de aparente calmaria.
* **Desconsiderar o Alfabeto:** Tentar calcular ou interpretar a entropia sem definir rigorosamente o espaço de estados $i$ (ex.: ticks, retornos discretizados ou microestrutura).
* **Tratar Entropia como "Desordem Abstrata":** Ignorar a definição formal da entropia como a surpresa média associada à capacidade de leitura dos estados do sistema.
* **Avaliar Apenas o Nível Estático de $H$:** Focar apenas no valor pontual da entropia e negligenciar sua derivada temporal $\frac{dH}{dt}$. O crescimento da entropia sinaliza a deformação do suporte informacional.
* **Utilizar a Entropia de Forma Isolada:** Tentar construir modelos completos de risco sem considerar as outras duas pontas da tríade informacional: a persistência (memória) e a circulação (transmissão de sinal).

---

### Lab Prático Sugerido em Python

Abaixo estão os passos detalhados para implementar um indicador de legibilidade informacional e monitorar a dinâmica da entropia $\frac{dH}{dt}$ em dados financeiros.

#### Passo 1 Coleta e Discretização dos Dados
1. Obtenha uma série temporal de alta frequência de retornos de preço ou direção de ticks.
2. Defina um alfabeto de estados discretos. Por exemplo, mapeie os retornos $r_t$ em três classes:
   * Estado $+1$ se $r_t > \epsilon$
   * Estado $-1$ se $r_t < -\epsilon$
   * Estado $0$ se $|r_t| \le \epsilon$ (onde $\epsilon$ é um limite fixo para ruído microestrutural).

#### Passo 2 Construção da Janela Móvel (Rolling Window)
1. Estabeleça uma janela móvel temporal de tamanho $W$ (ex.: 100 observações).
2. Para cada posição da janela, calcule a frequência relativa de ocorrência de cada estado $i \in \{-1, 0, 1\}$ para estimar a distribuição $p_i$.

#### Passo 3 Cálculo da Entropia de Shannon
1. Aplique a fórmula $H = -\sum_{i} p_i \log_2(p_i)$ para cada janela.
2. Garanta a convenção de que $0 \cdot \log_2(0) = 0$ para cobrir estados com probabilidade zero na janela.

#### Passo 4 Estimação da Derivada Temporal
1. Calcule a variação da entropia entre janelas consecutivas: $\Delta H_t = H_t - H_{t-1}$.
2. Suavize a série temporal de $\Delta H_t$ para estimar a tendência de $\frac{dH}{dt}$.

#### Passo 5 Detecção do Sinal de Alerta
1. Compute em paralelo a volatilidade realizada histórica (ex.: desvio padrão dos retornos na mesma janela $W$).
2. Crie uma regra de sinalização para identificar regimes onde:
   * A volatilidade realizada está abaixo de seu percentil 30 (calmaria aparente).
   * A entropia $H_t$ está acima de seu percentil 70 e $\frac{dH}{dt} > 0$.
3. Registre esses momentos como zonas de instabilidade informacional e risco de transição rápida.

---

### Glossário de Termos

* **Alfabeto (Espaço de Estados):** Conjunto finito de estados discretos $i$ (como direções de ticks, faixas de retorno ou estados de order book) utilizados para categorizar as mensagens do mercado.
* **Circulação da Informação:** Propriedade do sistema que descreve como as mensagens trafegam através do mercado, avaliando se sofrem atrasos, distorções ou amplificações.
* **Entropia de Shannon ($H$):** Medida da incerteza média ou da surpresa média gerada pelos estados emitidos por uma fonte informacional.
* **Legibilidade:** Capacidade do mercado de fornecer dados com estrutura clara, permitindo discernir sinais relevantes do ruído de fundo.
* **Persistência (Memória de Mercado):** Capacidade de um sistema financeiro de reter seu estado e manter sua coerência temporal ao longo do tempo.
* **Risco Informacional:** Probabilidade de o sistema perder estrutura, memória e fluidez de transmissão a ponto de uma perturbação local provocar uma ruptura.
* **Surpresa ($I(i)$):** Quantidade de informação gerada pela ocorrência de um determinado estado, calculada como o logaritmo negativo de sua probabilidade ($-\log p_i$).
* **Tríade do Risco:** Estrutura conceitual composta por Entropia (legibilidade), Persistência (memória) e Circulação (transmissão de sinal).

---

### Questões de Fixação e Prática

#### Nível 1 Resposta Curta

**Questão 1:** O que a Entropia de Shannon mede quando aplicada às cotações do mercado financeiro?
* **Resposta:** Mede a incerteza média (ou surpresa média) dos estados emitidos pelo mercado, funcionando como um indicador de legibilidade do sistema.

**Questão 2:** Qual a relação entre a probabilidade de um evento ($p_i$) e a sua surpresa associada ($I(i)$)?
* **Resposta:** A relação é inversamente proporcional. Quanto menor a probabilidade do evento (evento raro), maior será a sua surpresa ($I(i) = -\log p_i$).

**Questão 3:** Por que uma distribuição uniforme de probabilidades entre os estados maximiza a entropia do mercado?
* **Resposta:** Porque elimina qualquer predominância entre os estados. Sem uma estrutura ou hierarquia dominante, nenhum estado serve como guia, levando ao colapso da previsibilidade.

---

#### Nível 2 Analítica e Intermediária

**Questão 4:** Explique por que um cenário de baixa volatilidade realizada combinado com alta entropia representa uma condição de mercado perigosa.
* **Resposta:** Porque cria a falsa ilusão de estabilidade. Superficialmente, os preços variam pouco, mas a estrutura informacional subjacente está saturada e sem legibilidade. Em um sistema legível, choques são absorvidos; em um sistema saturado informacionalmente, pequenas perturbações não se dissipam e podem se propagar, levando a transições ou rupturas abruptas.

**Questão 5:** Qual é o significado prático de observar $\frac{dH}{dt} > 0$ durante a estimativa de modelos estatísticos no mercado?
* **Resposta:** Significa que a incerteza informacional está aumentando e a estrutura implícita do mercado está se degradando. A geometria do sistema está se alterando durante a medição, fazendo com que as probabilidades condicionais estimadas percam a estabilidade operacional.

---

#### Nível 3 Análise Profunda e Dissertativa

**Questão 6:** Por que a entropia, considerada de forma isolada, é insuficiente para construir um modelo completo de risco? Descreva a Tríade do Risco e como suas componentes se complementam.
* **Resposta Esperada:** 
  A entropia mede a legibilidade e a incerteza do sistema em um determinado momento, mas não fornece a visão completa do comportamento dinâmico do risco. Para modelar o risco adequadamente, a entropia precisa ser integrada a duas outras dimensões:
  1. **Persistência (Memória do Regime):** Avalia se a perda ou ganho de legibilidade é temporário ou se tende a durar no tempo, medindo a capacidade do sistema de reter seu estado.
  2. **Circulação da Informação:** Avalia como os sinais se propagam pelo mercado, detectando se as mensagens chegam sem distorções ou se são filtradas, atrasadas ou amplificadas de forma patológica.
  
  Somente ao combinar a **Entropia** (legibilidade), a **Persistência** (memória) e a **Circulação** (transmissão), é possível avaliar se uma perturbação local será absorvida pelo sistema ou se resultará em uma ruptura informacional e estrutural do mercado.