<!-- imported from vault study notes; curated for open course -->
# M04.A02 — Construção livre de arbitragem da superfície

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M04
> **Aula:** M04.A02

↑ M04 · Resumo · Completo

**Módulo:** M04
**Pergunta do módulo:** Como ler, sanitizar e modelar a superfície de volatilidade?

## Conceito-núcleo
Calendar/butterfly arb: restrições para a superfície ser consistente com preços de vanilas.

## Aplicação em mercado / trading
Sanitizar IV antes de marcar exóticas ou calibrar modelos; rejeitar quotes que violam no-arb.

## Entregável / lab
Checklist de arb (calendar, butterfly) + correção mínima ilustrativa numa surface suja.

## Fonte (mapeamento)
quantitative-trading-free-lesson/13 arbitrage-free construction

## Guia de estudo aprofundado

> **info**
>

Este guia de estudo apresenta uma síntese aprofundada dos princípios quantitativos e operacionais para a construção de superfícies de volatilidade implícita livres de arbitragem. O material aborda desde os procedimentos de preparação e sanitização de dados de mercado até os testes estruturais de arbitragem de calendário e *butterfly*, a derivação da densidade risco-neutra e os impactos na volatilidade local e na gestão de risco.

---

### Conceitos-Chave Explicados em Profundidade

#### 1. Etapa Zero Sanitização e Reconciliação dos Dados de Mercado
Antes de aplicar qualquer algoritmo de ajuste (*fitting*) ou interpolação na curva de volatilidade implícita, é indispensável realizar a limpeza prévia dos dados fornecidos pelo mercado. O ajuste de modelos não corrige contradições estruturais nos dados de entrada; ele apenas espalha e redistribui essas inconsistências pela curva. 

A prática de sanitização exige unificar todas as cotações sob o mesmo arcabouço formal:
*   Mesma maturidade ($T$);
*   Mesmo valor do ativo subjacente a termo (*forward* $F$);
*   Mesma estrutura de desconto ($DF(T)$);
*   Mesmas convenções operacionais.

No mercado real, as cotações de opções de venda (*puts*) costumam ser mais líquidas e limpas fora do preço (*Out-of-The-Money* - OTM) abaixo do preço de exercício *At-The-Money* (ATM), enquanto as opções de compra (*calls*) apresentam melhor qualidade e liquidez acima do ATM. Em vez de utilizar indiscriminadamente as cotações de tela (*bid/ask* polutados ou cruzados), reconstrói-se um conjunto único e coerente de preços de *calls* por meio da Paridade *Put-Call*. Dessa forma, obtém-se um único objeto de análise contínuo e unificado: a curva de preços de call $K \mapsto C(K,T)$.

#### 2. Monotonicidade e Arbitragem de Butterfly
Para uma maturidade fixa $T$, em uma grade discreta e ordenada de *strikes* $K_1 < K_2 < \cdots < K_n$, os preços de *calls* devem satisfazer duas condições fundamentais de ausência de arbitragem estática:

1.  **Monotonicidade no Strike:** O preço de uma opção de compra deve ser estritamente não crescente em relação ao aumento do *strike*. Aumentar o preço de exercício reduz o valor do direito de compra.
    $$C(K_{i+1}, T) \le C(K_i, T)$$

2.  **Convexidade Discreta:** A taxa de variação (inclinação ou *slope*) dos preços de *call* em relação ao *strike* deve ser não decrescente à medida que o *strike* aumenta. Definindo a inclinação discreta $s_i$ entre *strikes* consecutivos como:
    $$s_i = \frac{C(K_{i+1}, T) - C(K_i, T)}{K_{i+1} - K_i}$$
    
    A condição de convexidade discreta exige que:
    $$s_{i+1} \ge s_i$$

A violação desta inclinação não decrescente representa uma quebra da condição contínua $\frac{\partial^2 C}{\partial K^2} \ge 0$, originando uma oportunidade de **arbitragem de butterfly**. Se a convexidade falha, a estratégia de montar uma trava de borboleta (*butterfly spread*) resulta em um custo de montagem negativo ou em retorno garantido sem risco.

#### 3. Densidade Risco-Neutra (RND)
A relação matemática fundamental que conecta a geometria dos preços de *calls* à teoria de apreçamento de ativos estabelece que a segunda derivada parcial do preço da *call* em relação ao *strike* é proporcional à Densidade Risco-Neutra (RND) $f_T(K)$.

Sob a convenção usual de desconto pelo fator de desconto à vista (*spot-discounted*), a RND satisfaz:
$$\frac{\partial^2 C}{\partial K^2}(K,T) = DF(T) \cdot f_T(K)$$

Ao trabalhar na convenção *forward* (onde o fator de desconto é absorvido), a expressão assume a forma simplificada:
$$f_T(K) \propto \frac{\partial^2 C}{\partial K^2}(K,T)$$

**Consequência Matemática e Física:** Quando a convexidade dos preços torna-se negativa ($\frac{\partial^2 C}{\partial K^2} < 0$), o modelo produz uma densidade de probabilidade risco-neutra negativa em determinado trecho da distribuição. Uma probabilidade negativa inviabiliza a precificação coerente de qualquer derivativo e corrompe a diferenciação necessária para obter as gregas e a volatilidade local.

#### 4. Arbitragem de Calendário e Espaço de Variância Total
A arbitragem de calendário ocorre na dimensão temporal (maturidade $T$). Um contrato de opção com maturidade mais longa não pode valer menos do que um contrato com maturidade mais curta para o mesmo *strike* (ou mesma *log-moneyness* $k$), pois carrega maior valor temporal de incerteza:
$$C(K, T_2) \ge C(K, T_1) \quad \text{para } T_2 > T_1$$

Para facilitar o ajuste e a interpolação ao longo do tempo, utiliza-se a representação em **Variância Total** ($w$), definida como:
$$w(k, T) = \sigma_{\mathrm{impl}}^2 \cdot T$$

A condição prática para eliminação de arbitragem de calendário no espaço de variância total simplifica-se para:
$$w(k, T_2) \ge w(k, T_1) \quad \text{para todo } k \text{ e } T_2 > T_1$$

Trabalhar no espaço $(k, w)$ em vez de interpolar diretamente a volatilidade implícita superficial ($\sigma_{\mathrm{impl}}$) garante que o objeto interpolado carregue diretamente a incerteza acumulada ao longo do tempo, tornando a identificação e correção de arbitragens verticais mais simples e robustas.

#### 5. Implicações na Volatilidade Local de Dupire
A superfície de volatilidade implícita serve como camada intermediária para a calibração de modelos mais complexos, como o modelo de Volatilidade Local de Dupire. A fórmula da volatilidade local $\sigma_{\mathrm{loc}}^2(K,T)$, sob taxas de juros $r$ e rendimento de dividendos $q$, é dada por:

$$\sigma_{\mathrm{loc}}^2(K,T) = \frac{\partial_T C + (r-q)K\partial_K C + qC}{\frac{1}{2}K^2\partial_K^2 C}$$

Se a superfície de entrada contiver ruídos ou violações de convexidade ($\partial_K^2 C \le 0$ ou $\partial_K^2 C \approx 0$), o denominador da fórmula de Dupire entra em colapso ou torna-se negativo. Isso faz com que a volatilidade local resultante assuma valores imaginários ou infinitos, desintegrando o modelo.

---

### Intuição de Mercado e Visão da Mesa de Trading

*   **A Ilusão do Ajuste Estético (*Visual Smoothness*):** Uma superfície visualmente suave e sem imperfeições aparentes em um gráfico tridimensional ou *heatmap* pode estar estruturalmente corrompida. O ajuste matemático não resolve contradições nas cotações de entrada; ele apenas espalha os erros pela grade.
*   **Instabilidade do Hedging e Gregas Locais:** O principal risco para uma mesa de operações (*desk*) não é o nível geral da volatilidade implícita, mas a nervosidade local. Pequenos "caroços" (*bumps*) artificiais nos preços de *calls* criam oscilações nas derivadas de segunda ordem, fazendo com que o Gamma ($\Gamma = \frac{\partial^2 C}{\partial S^2}$) altere seu sinal abruptamente em intervalos de poucos *ticks*. Isso invalida completamente as estratégias de *delta hedging*.
*   **Perguntas de Validação Fundamental:** Antes de liberar uma superfície construída para precificação de exóticos e gestão de risco, a mesa deve responder de forma afirmativa às três validações rígidas:
    1. O preço da *call* diminui estritamente com o aumento do *strike*?
    2. O preço da *call* permanece estritamente convexo em relação ao *strike*?
    3. O preço da *call* (e a variância total) aumenta estritamente com o tempo de maturação?

---

### Exemplo Numérico Resolvido Passo a Passo

#### Cenário
Considere os dados de mercado de opções de compra (*calls*) para uma mesma maturidade $T$, após a unificação e sanitização das cotações via Paridade *Put-Call*. Deseja-se testar se os preços discretos apresentam arbitragem de *butterfly*.

*   *Strikes* ($K$): $$
*   Preços de Call ($C$): $[12.00, 8.50, 6.00, 2.50]$

---

#### Passo 1 Ordenação dos Dados
Verificar se a grade de *strikes* está estritamente crescente:
$$K_1 = 100, \quad K_2 = 105, \quad K_3 = 110, \quad K_4 = 115$$

Os preços associados estão corretamente pareados:
$$C_1 = 12.00, \quad C_2 = 8.50, \quad C_3 = 6.00, \quad C_4 = 2.50$$

---

#### Passo 2 Teste de Monotonicidade no Strike
Verificar se $C(K_{i+1}) - C(K_i) \le 0$ para todos os pontos:

*   $\Delta C_1 = C_2 - C_1 = 8.50 - 12.00 = -3.50 \le 0$
*   $\Delta C_2 = C_3 - C_2 = 6.00 - 8.50 = -2.50 \le 0$
*   $\Delta C_3 = C_4 - C_3 = 2.50 - 6.00 = -3.50 \le 0$

**Resultado:** O teste de monotonicidade foi **APROVADO**. Os preços de *call* decrescem monotonicamente com o aumento do *strike*.

---

#### Passo 3 Cálculo das Inclinações Discretas ($s_i$)
Calcular a inclinação do preço em cada intervalo de *strike*:

$$s_1 = \frac{C_2 - C_1}{K_2 - K_1} = \frac{8.50 - 12.00}{105 - 100} = \frac{-3.50}{5} = -0.70$$

$$s_2 = \frac{C_3 - C_2}{K_3 - K_2} = \frac{6.00 - 8.50}{110 - 105} = \frac{-2.50}{5} = -0.50$$

$$s_3 = \frac{C_4 - C_3}{K_4 - K_3} = \frac{2.50 - 6.00}{115 - 110} = \frac{-3.50}{5} = -0.70$$

---

#### Passo 4 Teste de Convexidade Discreta ($s_{i+1} \ge s_i$)
Verificar as diferenças entre as inclinações consecutivas ($\Delta s_i = s_{i+1} - s_i \ge 0$):

1.  **Primeiro intervalo de inclinação:**
    $$\Delta s_1 = s_2 - s_1 = -0.50 - (-0.70) = +0.20 \ge 0 \quad \text{(Aprovado)}$$

2.  **Segundo intervalo de inclinação:**
    $$\Delta s_2 = s_3 - s_2 = -0.70 - (-0.50) = -0.20 < 0 \quad \text{(FALHA)}$$

---

#### Conclusão do Exemplo
A condição $s_3 \ge s_2$ foi violada. A menor diferença entre inclinações foi de $-0.20$. Essa violação indica a presença de **arbitragem de butterfly** no trecho entre os *strikes* 105, 110 e 115. Matematicamente, a derivada segunda discreta tornou-se negativa, o que geraria uma densidade risco-neutra negativa nessa região e inviabilizaria a calibração de um modelo de volatilidade local.

---

### Armadilhas Comuns (Common Pitfalls)

| Armadilha | Descrição | Consequência no Trading / Modelagem |
| :--- | :--- | :--- |
| **Ajustar sem Sanitizar** | Tentar ajustar um modelo de *smile* diretamente sobre cotações puras de tela (*bid/ask* largos ou cruzados). | O ajuste espalha a contradição por toda a curva em vez de resolvê-la. |
| **Confiança Visual em Heatmaps** | Validar a superfície apenas por gráficos bonitos ou *heatmaps* contínuos. | Oculta nervosidades locais que fazem o Gamma trocar de sinal a cada 3 *ticks*. |
| **Interpolação em $\sigma_{\mathrm{impl}}$** | Interpolar a volatilidade implícita diretamente em vez de operar nos espaços de Preço $C$ ou Variância Total $w$. | Maior facilidade para introduzir arbitragem de calendário indesejada sem percepção direta. |
| **Ignorar o Denominador de Dupire** | Diferenciar uma superfície com pequenas violações de convexidade para gerar Volatilidade Local. | O denominador $\frac{1}{2}K^2\partial_K^2 C$ estourará ou ficará negativo, gerando volatilidades imaginárias. |

---

### Laboratório Prático Sugerido em Python

O laboratório a seguir descreve a implementação de rotinas de verificação estática de ausência de arbitragem em Python para validar a grade de preços discretos e a estrutura temporal.

#### Passo 1 Definição da Verificação Discreta por Maturidade
Implementar a função de verificação estática para testar a monotonicidade e a convexidade discreta para uma lista de *strikes* $K$ e preços de *calls* $C$.

```text
Algoritmo de Verificação Discreta de Monotonicidade e Convexidade:
1. Converter K e C em arrays numéricos do tipo float.
2. Ordenar a grade de strikes K de forma crescente e reordenar C com base nos mesmos índices.
3. Calcular a diferença entre preços consecutivos diff(C).
4. Verificar a monotonicidade: confirmar se todas as diferenças diff(C) <= tolerância (1e-10).
5. Calcular os slopes discretos: s = diff(C) / diff(K).
6. Verificar a convexidade: confirmar se a diferença entre slopes consecutivos diff(s) >= -tolerância (-1e-10).
7. Retornar um dicionário com:
   - mono_ok (Booleano)
   - convex_ok (Booleano)
   - min_slope (Float)
   - max_slope (Float)
   - min_slope_diff (Float)
```

#### Passo 2 Definição da Verificação Temporal de Calendário
Implementar o teste de arbitragem de calendário ao longo da grade temporal.

```text
Algoritmo de Verificação de Arbitragem de Calendário:
1. Para cada strike K pertencente a uma grade K_grid:
   a. Para cada maturidade T na grade T_grid, calcular o preço da call correspondente usando as funções de Forward e Discount Factor.
   b. Para cada par consecutivo de maturidades (T_i, T_{i+1}), verificar se Preço(T_{i+1}) >= Preço(T_i) - tolerância.
2. Armazenar a aprovação (Booleano) para cada strike K analisado.
3. Retornar a estrutura contendo os preços por maturidade e a flag de conformidade.
```

---

### Glossário de Termos Técnicos

*   **Arbitragem de Butterfly (Butterfly Arbitrage):** Condição de arbitragem estática que ocorre quando a regra de convexidade de preços de opções de compra ($\partial_K^2 C \ge 0$) é violada em relação ao *strike*, permitindo construir uma trava de borboleta com ganho certo e sem risco.
*   **Arbitragem de Calendário (Calendar Arbitrage):** Condição de arbitragem temporal que ocorre quando uma opção de maturação mais longa possui preço inferior a uma opção de maturação mais curta com o mesmo preço de exercício e mesmo ativo objeto ($\partial_T C < 0$).
*   **Densidade Risco-Neutra (Risk-Neutral Density - RND):** Distribuição de probabilidade do preço do ativo subjacente no vencimento, implicada pelos preços das opções no mercado. É proporcional à segunda derivada do preço da *call* em relação ao *strike*.
*   **Paridade Put-Call:** Relação financeira fundamental que conecta o preço de uma opção de compra (*call*) e de uma opção de venda (*put*) de mesmo *strike* e maturidade, garantindo a unificação do livro de cotações.
*   **Sanitização de Dados:** Processo inicial e fundamental de higienização dos dados do mercado (filtragem de cotações cruzadas, *bids/asks* disformes e conversão via paridade) antes do ajuste de qualquer modelo quantitativo.
*   **Variância Total ($w$):** Representação do risco acumulado até a maturação, definida por $w(k,T) = \sigma_{\mathrm{impl}}^2 \cdot T$. É a variável preferencial para interpolação temporal de superfícies de volatilidade.
*   **Volatilidade Local de Dupire:** Modelo de volatilidade determinística dependente do preço atual e do tempo, obtido a partir das derivadas parciais de primeira ordem no tempo e de primeira e segunda ordem no *strike* da superfície de preços de *calls*.

---

### Questões de Prática e Questões Dissertativas

#### Nível 1 Exercícios de Fixação e Curta Resposta

##### Questão 1
O que acontece quando a segunda derivada do preço de uma opção de compra em relação ao *strike* ($\frac{\partial^2 C}{\partial K^2}$) assume um valor negativo em uma região da superfície?
*   A) A volatilidade implícita atinge seu nível máximo.
*   B) A densidade de probabilidade risco-neutra torna-se negativa nessa região.
*   C) A arbitragem de calendário é ativada.
*   D) O preço da opção de venda equivalente torna-se zero.

**Resposta do Nível 1 - Questão 1:** **B**. Matematicamente, a Densidade Risco-Neutra é proporcional a $\frac{\partial^2 C}{\partial K^2}$. Se a derivada de segunda ordem for negativa, uma probabilidade negativa é gerada localmente, indicando arbitragem de *butterfly*.

---

##### Questão 2
Por que a interpolação contínua e o ajuste (*fitting*) direto em uma curva de cotações poluídas do mercado não corrigem os problemas de arbitragem?

**Resposta do Nível 1 - Questão 2:** Porque o algoritmo de ajuste não resolve ou elimina as contradições dos dados de entrada; ele apenas espalha as inconsistências e o ruído ao longo de toda a curva interpolada. A correção precisa ser feita na "Etapa Zero" por meio da sanitização de dados.

---

#### Nível 2 Problemas de Aplicação e Análise Numérica

##### Questão 3
Considere duas maturidades $T_1 = 0.5$ anos e $T_2 = 1.0$ ano. Para um mesmo *strike* $K = 100$, as volatilidades implícitas observadas são $\sigma_{\mathrm{impl}}(100, T_1) = 20\%$ e $\sigma_{\mathrm{impl}}(100, T_2) = 12\%$.
1. Calcule a variância total $w(k, T_1)$ e $w(k, T_2)$.
2. Verifique se há presença de arbitragem de calendário.

**Resposta do Nível 2 - Questão 3:**
1. Cálculo das variâncias totais:
   $$w(k, T_1) = \sigma_{\mathrm{impl}}^2(T_1) \cdot T_1 = (0.20)^2 \cdot 0.5 = 0.04 \cdot 0.5 = 0.020$$
   $$w(k, T_2) = \sigma_{\mathrm{impl}}^2(T_2) \cdot T_2 = (0.12)^2 \cdot 1.0 = 0.0144 \cdot 1.0 = 0.0144$$

2. Análise da condição de não-arbitragem:
   A condição exige que $w(k, T_2) \ge w(k, T_1)$. Como $0.0144 < 0.020$, a condição é **VIOLADA**. Existe **arbitragem de calendário**, pois a variância total acumulada decresceu com o tempo.

---

#### Nível 3 Questões Dissertativas Avançadas

##### Questão 4
Explique detalhadamente por que uma superfície de volatilidade implícita visualmente "suave" (*smooth*) pode causar o colapso do modelo de Volatilidade Local de Dupire e desorganizar a estratégia de *delta hedging* de um *desk* de exóticos. Em sua resposta, relacione os conceitos de inclinação discreta, denominador de Dupire e sensibilidades de segunda ordem (Gamma).

**Resposta do Nível 3 - Questão 4:**
Uma superfície de volatilidade implícita pode parecer esteticamente suave em um gráfico contínuo ou *heatmap*, mas ainda conter pequenas instabilidades ou oscilações locais nas derivadas. O modelo de Volatilidade Local de Dupire depende diretamente da fórmula:

$$\sigma_{\mathrm{loc}}^2(K,T) = \frac{\partial_T C + (r-q)K\partial_K C + qC}{\frac{1}{2}K^2\partial_K^2 C}$$

O denominador desta equação é dominado pela convexidade da *call* ($\partial_K^2 C$). Se a superfície ajustada possuir pequenos "caroços" ou alterações locais de inclinação ($s_{i+1} < s_i$), o termo $\partial_K^2 C$ se aproxima de zero ou torna-se negativo. 

Quando $\partial_K^2 C \to 0$, o denominador colapsa e a volatilidade local resultante diverge para o infinito. Quando $\partial_K^2 C < 0$, o termo sob a raiz quadrada torna-se negativo, gerando volatilidades locais imaginárias, o que invalida qualquer precificação por equações diferenciais parciais (PDE) ou Monte Carlo.

Sob a perspectiva da mesa de operações (*desk*), o cálculo de risco depende das gregas de ordem superior. O Gamma do portfólio ($\Gamma = \frac{\partial^2 C}{\partial S^2}$) está intimamente associado à curvatura no *strike*. Ondulações locais fazem com que o Gamma troque de sinal repetidamente entre posições compradas e vendidas ao longo de pequenos deslocamentos no preço do subjacente ($S$). Isso faz com que os rebalanceamentos de *delta hedging* exijam reajustes gigantescos e contraditórios a cada poucos *ticks*, destruindo a capacidade da mesa de gerenciar o risco do livro de derivativos.