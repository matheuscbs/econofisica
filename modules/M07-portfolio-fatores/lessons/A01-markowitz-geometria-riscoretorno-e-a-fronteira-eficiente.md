<!-- imported from vault study notes; curated for open course -->
# M07.A01 — Markowitz: geometria risco–retorno e a fronteira eficiente

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M07
> **Aula:** M07.A01

↑ M07 · Resumo · Completo

**Módulo:** M07
**Pergunta do módulo:** Como alocar além do μ ingênuo e do “alpha” ilusório?

## Conceito-núcleo
Otimização média-variância como geometria; fronteira eficiente e papel da covariância.

## Aplicação em mercado / trading
Construir alocações base; ver fragilidade a erros de μ e à não-estacionariedade da cov.

## Entregável / lab
Fronteira 3–8 ativos; comparar equal-weight vs tangency sob μ estimado vs μ estressado.

## Fonte (mapeamento)
quantitative-trading-free-lesson/24 markowitz-closing-the-return-risk-problem-through-geometry

## Guia de estudo aprofundado

> **info**
>

### Visão Geral e Conceitos-Chave Explicados em Profundidade

#### O Fechamento Geométrico do Problema Risco-Retorno
A teoria de seleção de carteiras de Markowitz não deve ser entendida como uma verdade metafísica sobre o mercado de capitais ou uma teoria sagrada, mas sim como um fechamento geométrico do problema de alocação. Em vez de focar na compra individual de posições, o problema central é organizar um ponto dentro de um espaço multidimensional no qual todos os ativos se movimentam conjuntamente.

Para um universo de $N$ ativos arriscados, o mercado é sintetizado por dois objetos estatísticos fundamentais:
*   O vetor de retornos esperados: $\mu = E[R] \in \mathbb{R}^N$
*   A matriz de covariância: $\Sigma = Cov(R) \in \mathbb{R}^{N \times N}$

Enquanto $\mu$ representa a média de retorno esperada, $\Sigma$ estabelece a estrutura de comovimento, ou seja, a forma como os ativos vibram e oscilam juntos. A estrutura de covariância importa mais do que os nomes individuais dos ativos. O risco do portfólio não é apenas a soma do movimento de cada ativo, mas a forma como esses movimentos se combinam espacialmente.

#### A Definção Científica de Eficiência
Um portfólio $w$ é uma transformação que envia um vetor de pesos sujeitos à restrição orçamentária $\mathbf{1}^\top w = 1$ para o espaço risco-retorno $(\sigma_p, \mu_p)$, onde:
*   Retorno esperado: $\mu_p(w) = w^\top \mu$
*   Variância: $\sigma_p^2(w) = w^\top \Sigma w$
*   Risco (desvio padrão): $\sigma_p(w) = \sqrt{w^\top \Sigma w}$

Neste contexto, o termo "eficiente" não possui conotação moral ou ideológica; trata-se de uma propriedade de não-dominância geométrica. Um portfólio é considerado **eficiente** se não existir outro portfólio no espaço viável que ofereça:
1.  Um retorno estritamente maior para o mesmo nível de risco.
2.  Um risco estritamente menor para o mesmo nível de retorno.

#### Mecanismo de Diversificação e Geometria em N Ativos
A intuição básica da diversificação surge no caso com $N=2$ ativos, onde os pesos são $(w, 1-w)$. A variância do portfólio é calculada por:
$$\sigma_p^2(w) = w^2\sigma_1^2 + (1-w)^2\sigma_2^2 + 2w(1-w)\rho_{12}\sigma_1\sigma_2$$

Toda a capacidade de diversificação deriva de uma única condição geométrica: $\rho_{12} < 1$. Se a correlação entre os ativos não for perfeitamente alinhada ($\rho_{12} = 1$), torna-se possível construir combinações cujo risco total é inferior ao risco de qualquer um dos ativos mantidos individualmente. A diversificação é, portanto, um efeito geométrico de não-alinhamento.

Quando estendido para $N$ ativos, o problema central da fronteira eficiente consiste em resolver: para um retorno alvo $\bar{\mu}$, qual portfólio minimiza a variância total?

#### Separação em Dois Fundos e o Ativo Livre de Risco
A introdução do ativo livre de risco $r_f$ altera a natureza do problema ao separar a decisão de alocação em duas etapas independentes:
1.  **Escolha da mistura arriscada otimizada**: Identificação da carteira de tangência, que determina a direção arriscada de máxima inclinação no espaço risco-retorno.
2.  **Escolha da alavancagem**: Definição da proporção alocada entre o ativo livre de risco e a carteira de tangência.

Com a presença de $r_f$, a fronteira eficiente deixa de ser uma curva no plano $(\sigma, \mu)$ e passa a ser uma linha reta denominada *Capital Allocation Line* (CAL) ou Linha de Alocação de Capital.

#### O Impacto das Restrições e Canto de Politopos
Ao adicionar restrições reais de mercado, como a proibição de vendas a descoberto ($w_i \ge 0$) ou limites de concentração por ativo ($w_i \le w_{\max}$), o problema de minimização da variância transforma-se em um programa quadrático convexo sob desigualdades.

Sob essas restrições, a fronteira eficiente se dobra para dentro (*folds inward*). Alguns retornos alvos tornam-se impossíveis e as soluções ótimas deixam de ser combinações analíticas suaves, passando a se fixar nas bordas e vértices de um politopo (cantos das restrições).

---

### Formulação Matemática Detalhada

#### Minimização de Variância sem Restrições (Caso Puro Riscoso)
O problema de otimização para obter a fronteira de mínima variância com $N$ ativos arriscados é formulado como:
$$\min_w \; w^\top \Sigma w \quad \text{s.t.} \quad w^\top \mu = \bar{\mu}, \quad \mathbf{1}^\top w = 1$$

Escrevendo a função Lagrangeana:
$$L(w, \lambda_1, \lambda_2) = w^\top \Sigma w - \lambda_1(w^\top \mu - \bar{\mu}) - \lambda_2(\mathbf{1}^\top w - 1)$$

Tomando as condições de primeira ordem ($\nabla_w L = 0$):
$$2\Sigma w - \lambda_1\mu - \lambda_2\mathbf{1} = 0 \implies \Sigma w = \frac{\lambda_1}{2}\mu + \frac{\lambda_2}{2}\mathbf{1}$$

Isso demonstra que o vetor de pesos ótimo $w$ reside obrigatoriamente no espaço gerado por dois vetores fundamentais: $\Sigma^{-1}\mu$ e $\Sigma^{-1}\mathbf{1}$.

#### Escalares Geométricos e Solução Fechada
Para condensar a geometria do sistema, definem-se os quatro escalares fundamentais:
$$A = \mathbf{1}^\top\Sigma^{-1}\mathbf{1}$$
$$B = \mathbf{1}^\top\Sigma^{-1}\mu$$
$$C = \mu^\top\Sigma^{-1}\mu$$
$$D = AC - B^2$$

Desde que o vetor $\mu$ não seja colinear com o vetor de uns $\mathbf{1}$, garante-se que $D > 0$. A família de portfólios de mínima variância para qualquer retorno alvo $\bar{\mu}$ é expressa analiticamente por:
$$w(\bar{\mu}) = \Sigma^{-1} \left[ \frac{C-\bar{\mu}B}{D}\mathbf{1} + \frac{\bar{\mu}A-B}{D}\mu \right]$$

Ao plotar $(\sigma(\bar{\mu}), \bar{\mu})$, obtém-se uma curva do tipo hiperbólica. Contudo, apenas o ramo superior dessa curva pertence à fronteira eficiente, pois o ramo inferior é estritamente dominado.

#### Carteira de Tangência e a Razão de Sharpe
Definindo os retornos em excesso em relação ao ativo livre de risco como $\mu_{ex} = \mu - r_f\mathbf{1}$, com pesos do ativo arriscado $w_R$ e peso no ativo livre de risco $w_f = 1 - \mathbf{1}^\top w_R$, o retorno e risco do portfólio composto são:
$$E[R_p] = r_f + w_R^\top \mu_{ex}$$
$$\sigma_p = \sqrt{w_R^\top \Sigma w_R}$$

A inclinação da reta no plano risco-retorno é a Razão de Sharpe $S(w_R)$:
$$S(w_R) = \frac{w_R^\top \mu_{ex}}{\sqrt{w_R^\top \Sigma w_R}}$$

Dado que o Índice de Sharpe é invariante à escala, a direção ótima não-normalizada é calculada por:
$$w_T \propto \Sigma^{-1}\mu_{ex}$$

Para exibir a carteira de tangência normalizada com orçamento total alocado nos ativos arriscados ($\mathbf{1}^\top \tilde{w}_T = 1$):
$$\tilde{w}_T = \frac{\Sigma^{-1}\mu_{ex}}{\mathbf{1}^\top \Sigma^{-1}\mu_{ex}}$$

A Linha de Alocação de Capital (CAL) resultante é:
$$E[R_p] = r_f + S_T \sigma_p, \quad \text{onde} \quad S_T = \frac{\tilde{w}_T^\top\mu_{ex}}{\sqrt{\tilde{w}_T^\top\Sigma\tilde{w}_T}}$$

---

### Intuição de Mercado e Trading

*   **A Ilusão da Diversificação em Crises**: A diversificação não é uma fórmula mágica, mas um efeito dependente da não-sincronização ($\rho < 1$). Em momentos de estresse severo de mercado, travamento de liquidez e propagação de restrições, os ativos tendem a se sincronizar. Quando isso ocorre, as correlações sobem rapidamente em direção a 1 ($\rho \to 1$), e a margem de diversificação colapsa exatamente quando ela é mais necessária.
*   **Separação entre Direção de Risco e Alavancagem**: A carteira de tangência define a direção ótima de alocação arriscada (o vetor que maximiza o retorno em excesso por unidade de volatilidade). A decisão de quanto risco tomar é resolvida separadamente por meio do nível de alavancagem ou empréstimo ao ativo livre de risco $r_f$.
*   **A Invariância de Escala do Sharpe**: Tentar otimizar o Sharpe impondo arbitrariamente restrições rígidas no mesmo nível do medidor de escala quebra a lógica geométrica do problema. A abordagem correta em sistemas numéricos é fixar o retorno em excesso em um valor fixo (por exemplo, $w^\top \mu_{ex} = 1$), minimizar a variância resultante e, em seguida, renormalizar os pesos.

---

### Exemplo Numérico Resolvido Passo a Passo

Considere um universo com $N=2$ ativos arriscados e um ativo livre de risco com taxa $r_f = 0,02$ ($2\%$).

**Dados de Entrada:**
*   Vetor de retornos esperados: $\mu = \begin{bmatrix} 0,10 \\ 0,14 \end{bmatrix}$
*   Matriz de covariância: $\Sigma = \begin{bmatrix} 0,04 & 0,01 \\ 0,01 & 0,09 \end{bmatrix}$

**Objetivo:** Calcular a carteira de tangência $\tilde{w}_T$, seu retorno esperado $\mu_T$, sua volatilidade $\sigma_T$ e a Razão de Sharpe $S_T$.

#### Passo 1 Calcular o vetor de retornos em excesso $\mu_{ex}$
$$\mu_{ex} = \mu - r_f \mathbf{1} = \begin{bmatrix} 0,10 \\ 0,14 \end{bmatrix} - 0,02 \begin{bmatrix} 1 \\ 1 \end{bmatrix} = \begin{bmatrix} 0,08 \\ 0,12 \end{bmatrix}$$

#### Passo 2 Inverter a matriz de covariância $\Sigma$
Para uma matriz $2 \times 2$, a inversa é $A^{-1} = \frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$.

Determinante $\det(\Sigma) = (0,04)(0,09) - (0,01)(0,01) = 0,0036 - 0,0001 = 0,0035$.

$$\Sigma^{-1} = \frac{1}{0,0035} \begin{bmatrix} 0,09 & -0,01 \\ -0,01 & 0,04 \end{bmatrix} = \begin{bmatrix} \frac{180}{7} & -\frac{20}{7} \\[6pt] -\frac{20}{7} & \frac{80}{7} \end{bmatrix}$$

#### Passo 3 Obter a direção não-normalizada $w_{raw} = \Sigma {-1}\mu_{ex}$
$$w_{raw} = \begin{bmatrix} \frac{180}{7} & -\frac{20}{7} \\[6pt] -\frac{20}{7} & \frac{80}{7} \end{bmatrix} \begin{bmatrix} 0,08 \\[6pt] 0,12 \end{bmatrix} = \begin{bmatrix} \frac{180(0,08) - 20(0,12)}{7} \\[6pt] \frac{-20(0,08) + 80(0,12)}{7} \end{bmatrix} = \begin{bmatrix} \frac{14,4 - 2,4}{7} \\[6pt] \frac{-1,6 + 9,6}{7} \end{bmatrix} = \begin{bmatrix} \frac{12}{7} \\[6pt] \frac{8}{7} \end{bmatrix}$$

#### Passo 4 Normalizar os pesos para orçamento $\mathbf{1} \top \tilde{w}_T = 1$
Soma dos pesos não-normalizados:
$$\mathbf{1}^\top w_{raw} = \frac{12}{7} + \frac{8}{7} = \frac{20}{7}$$

Dividindo $w_{raw}$ pela soma:
$$\tilde{w}_T = \frac{\begin{bmatrix} 12/7 \\ 8/7 \end{bmatrix}}{\frac{20}{7}} = \begin{bmatrix} \frac{12}{20} \\[6pt] \frac{8}{20} \end{bmatrix} = \begin{bmatrix} 0,60 \\ 0,40 \end{bmatrix}$$

O portfólio de tangência aloca **60% no Ativo 1** e **40% no Ativo 2**.

#### Passo 5 Calcular o Retorno Esperado e Risco do Portfólio de Tangência
**Retorno Esperado ($\mu_T$):**
$$\mu_T = \tilde{w}_T^\top \mu = 0,60(0,10) + 0,40(0,14) = 0,06 + 0,056 = 0,116 \text{ (ou } 11,6\%)$$

**Variância do Portfólio ($\sigma_T^2$):**
$$\sigma_T^2 = \tilde{w}_T^\top \Sigma \tilde{w}_T = \begin{bmatrix} 0,60 & 0,40 \end{bmatrix} \begin{bmatrix} 0,04 & 0,01 \\ 0,01 & 0,09 \end{bmatrix} \begin{bmatrix} 0,60 \\ 0,40 \end{bmatrix}$$

Primeiro, multiplica-se $\Sigma \tilde{w}_T$:
$$\begin{bmatrix} 0,04(0,60) + 0,01(0,40) \\ 0,01(0,60) + 0,09(0,40) \end{bmatrix} = \begin{bmatrix} 0,024 + 0,004 \\ 0,006 + 0,036 \end{bmatrix} = \begin{bmatrix} 0,028 \\ 0,042 \end{bmatrix}$$

Em seguida, multiplica-se por $\tilde{w}_T^\top$:
$$\sigma_T^2 = 0,60(0,028) + 0,40(0,042) = 0,0168 + 0,0168 = 0,0336$$

**Desvio Padrão ($\sigma_T$):**
$$\sigma_T = \sqrt{0,0336} \approx 0,1833 \text{ (ou } 18,33\%)$$

#### Passo 6 Calcular a Razão de Sharpe da Carteira de Tangência ($S_T$)
$$S_T = \frac{\mu_T - r_f}{\sigma_T} = \frac{0,116 - 0,02}{0,1833} = \frac{0,096}{0,1833} \approx 0,5237$$

---

### Armadilhas Comuns e Verificações de Produção

1.  **Não Positividade da Matriz de Covariância**: Se a matriz $\Sigma$ não for simétrica e estritamente positiva definida (ou semidefinida), o otimizador estará atuando sobre uma ilusão numérica. Deve-se sempre verificar se os autovalores de $\Sigma$ são estritamente positivos.
2.  **Violação da Invariância de Escala do Sharpe**: Otimizar a Razão de Sharpe diretamente tentando impor simultaneamente a restrição $1^\top w = 1$ pode gerar instabilidades numéricas. A formulação robusta por Otimização Quadrática (QP) deve fixar a restrição do retorno em excesso em $w^\top \mu_{ex} = 1$ e renormalizar o vetor de pesos ao final.
3.  **Amplificação do Erro de Estimação (A Armadilha do Parâmetro)**: O otimizador de Markowitz atua como um "amplificador de erro". Ele busca ativamente as pequenas anomalias estatísticas presentes no vetor de retornos esperados $\mu$. Pequenas variações de estimativa em $\mu$ causam mudanças drásticas nos pesos ótimos. Em produção, reconstruir $\mu$ e $\Sigma$ em diferentes janelas móveis frequentemente revela que a volatilidade dos pesos decorre do otimizador amplificando erros de entrada, e não de mudanças reais no mercado.
4.  **Suposição Falsa de Estabilidade do Regime**: Tratar Markowitz como a estrutura total do mercado e não apenas como um bloco geométrico é perigoso. O modelo assume que o regime permanece estável e legível. Quando o mercado entra em estresse severo, a geometria efetiva se altera profundamente.

---

### Lab Prático Sugerido em Python

O laboratório prático deve ser estruturado nos seguintes passos sequenciais:

1.  **Cálculo e Anualização dos Parâmetros**:
    Partindo de uma matriz de retornos contínuos (log-retornos) de ativos, criar a função `estimate_mu_sigma` para extrair a média e a matriz de covariância anualizadas (considerando 252 dias úteis).
    ```python
    import numpy as np
    import pandas as pd

    def estimate_mu_sigma(returns: pd.DataFrame, ann: int = 252):
        mu = returns.mean().values * ann
        Sigma = returns.cov().values * ann
        return mu, Sigma

    def port_mu_sigma(w: np.ndarray, mu: np.ndarray, Sigma: np.ndarray):
        mu_p = float(w @ mu)
        sig_p = float(np.sqrt(w @ Sigma @ w))
        return mu_p, sig_p
    ```

2.  **Construção Numérica da Fronteira Eficiente**:
    Definir uma grade de retornos alvos (`mu_grid`) e resolver o problema de otimização quadrática convexa usando a biblioteca `cvxpy` com o solver `OSQP`, aplicando restrições de *long-only* ($w_i \ge 0$) e limite máximo por ativo ($w_i \le w_{\max}$).
    ```python
    import cvxpy as cp

    def efficient_frontier(mu, Sigma, mu_grid, long_only=False, w_max=None):
        n = len(mu)
        w = cp.Variable(n)
        risk = cp.quad_form(w, Sigma)

        cons_base = [cp.sum(w) == 1]
        if long_only:
            cons_base += [w >= 0]
        if w_max is not None:
            cons_base += [w <= w_max]

        sigs, mus, weights = [], [], []
        for mu_bar in mu_grid:
            cons = cons_base + [w @ mu == mu_bar]
            prob = cp.Problem(cp.Minimize(risk), cons)
            prob.solve(solver=cp.OSQP, verbose=False)

            if w.value is None:
                sigs.append(np.nan)
                mus.append(mu_bar)
                weights.append(None)
                continue

            wv = np.array(w.value).ravel()
            mu_p, sig_p = port_mu_sigma(wv, mu, Sigma)
            sigs.append(sig_p)
            mus.append(mu_p)
            weights.append(wv)

        return np.array(sigs), np.array(mus), weights
    ```

3.  **Cálculo da Carteira de Tangência Analítica (Forma Fechada)**:
    Implementar a solução não restrita para obter o vetor de tangência e renormalizá-lo para orçamento igual a 1.
    ```python
    def tangency_portfolio_closed_form(mu, Sigma, r_f):
        n = len(mu)
        mu_ex = mu - r_f * np.ones(n)
        w_raw = np.linalg.solve(Sigma, mu_ex)
        w = w_raw / np.sum(w_raw)
        mu_T, sig_T = port_mu_sigma(w, mu, Sigma)
        S_T = (mu_T - r_f) / sig_T
        return w, mu_T, sig_T, S_T
    ```

4.  **Cálculo da Carteira de Tangência Restrita via Otimização Quadrática (QP)**:
    Implementar a otimização definindo um único calibre rígido: retornos em excesso igual a 1 ($w^\top \mu_{ex} = 1$), e renormalizar os pesos resultantes para exibição.
    ```python
    def tangency_portfolio_qp(mu, Sigma, r_f, long_only=False, w_max=None):
        n = len(mu)
        mu_ex = mu - r_f * np.ones(n)

        w = cp.Variable(n)
        risk = cp.quad_form(w, Sigma)

        # Medidor único: retorno em excesso fixado em 1
        cons = [w @ mu_ex == 1]
        if long_only:
            cons += [w >= 0]
        if w_max is not None:
            cons += [w <= w_max]

        prob = cp.Problem(cp.Minimize(risk), cons)
        prob.solve(solver=cp.OSQP, verbose=False)
        if w.value is None:
            return None, np.nan, np.nan, np.nan

        w_raw = np.array(w.value).ravel()
        w_disp = w_raw / np.sum(w_raw)

        mu_T, sig_T = port_mu_sigma(w_disp, mu, Sigma)
        S_T = (mu_T - r_f) / sig_T
        return w_disp, mu_T, sig_T, S_T
    ```

5.  **Teste de Sensibilidade dos Parâmetros**:
    Executar o código em janelas móveis de dados históricos para verificar a estabilidade dos pesos e observar visualmente a amplificação do erro de estimação em $\mu$.

---

### Glossário de Termos Importantes

*   **Fronteira Eficiente**: Conjunto geométrico de portfólios não-dominados no plano risco-retorno que minimizam a variância para cada nível de retorno esperado alvo.
*   **Carteira de Tangência**: O portfólio de ativos arriscados que maximiza a Razão de Sharpe, localizado exatamente no ponto onde a Linha de Alocação de Capital (CAL) tangencia a fronteira eficiente arriscada.
*   **Linha de Alocação de Capital (CAL)**: Reta que representa todas as combinações possíveis entre o ativo livre de risco e a carteira de tangência no espaço desvio padrão-retorno esperado.
*   **Teorema da Separação em Dois Fundos**: Princípio geométrico que estabelece que qualquer alocação eficiente com um ativo livre de risco é composta por uma mistura do ativo livre de risco e da carteira de tangência única.
*   **Razão de Sharpe**: Medida de eficiência que calcula a inclinação da reta no espaço risco-retorno, dada pela razão entre o retorno em excesso do portfólio e seu desvio padrão.
*   **Invariância de Escala do Sharpe**: Propriedade matemática da Razão de Sharpe na qual a multiplicação do vetor de pesos não-normalizado por um escalar positivo altera o nível de risco e retorno, mas mantém a inclinação (eficiência) inalterada.
*   **Matriz de Covariância ($\Sigma$)**: Estrutura matemática que mapeia a variância individual dos ativos e a comovimentação conjunta entre todos os pares do universo de investimentos.
*   **Amplificação do Erro de Estimação**: Tendência inerente ao otimizador de Markowitz de atribuir pesos desproporcionalmente grandes a ativos cujos retornos esperados foram superestimados ou cujas variâncias foram subestimadas devido ao ruído dos dados de entrada.

---

### Questões Práticas e Exercícios

#### Nível 1 Fácil

**Questão 1:** O que significa a propriedade de "não-dominância" ao definir um portfólio eficiente na geometria de Markowitz?
*   **Resposta:** Significa que não existe nenhum outro portfólio no espaço viável que entregue um retorno estritamente maior para o mesmo nível de risco, ou um risco estritamente menor para o mesmo nível de retorno esperado.

**Questão 2:** Qual é a condição geométrica fundamental necessária no modelo de dois ativos para que ocorra o efeito de diversificação?
*   **Resposta:** A condição é que a correlação entre os dois ativos seja menor do que 1 ($\rho_{12} < 1$).

**Questão 3:** O que acontece geometricamente com a fronteira eficiente quando impomos a restrição de não-venda a descoberto (*long-only*, $w_i \ge 0$)?
*   **Resposta:** A fronteira eficiente se dobra para dentro (*folds inward*), tornando impossíveis certos níveis de retorno antes atingíveis, e as soluções ótimas passam a se fixar nas bordas e vértices do politopo definido pelas restrições.

---

#### Nível 2 Médio

**Questão 4:** Ao resolver numericamente o portfólio de tangência via otimização quadrática (QP), por que se utiliza a restrição $w^\top \mu_{ex} = 1$ em vez de tentar impor diretamente $1^\top w = 1$?
*   **Resposta:** Como a Razão de Sharpe é invariante à escala, fixar o calibre do retorno em excesso em $w^\top \mu_{ex} = 1$ converte o problema de maximização de uma razão não linear em um problema de minimização quadrática de risco tratável e convexo. O vetor de pesos $w_{raw}$ obtido é posteriormente renormalizado dividindo por $\mathbf{1}^\top w_{raw}$ para exibição de orçamento igual a 1.

**Questão 5:** No caso analítico sem restrições, as constantes geométricas são $A = \mathbf{1}^\top\Sigma^{-1}\mathbf{1}$, $B = \mathbf{1}^\top\Sigma^{-1}\mu$, $C = \mu^\top\Sigma^{-1}\mu$ e $D = AC - B^2$. O que ocorre matematicamente se o vetor de retornos esperados $\mu$ for totalmente colinear com o vetor de uns $\mathbf{1}$?
*   **Resposta:** Se $\mu$ for colinear com $\mathbf{1}$, todos os ativos possuem exatamente o mesmo retorno esperado. Nesse caso, obtém-se $B^2 = AC$, o que resulta em $D = AC - B^2 = 0$. Como $D$ está no denominador da equação dos pesos ótimos $w(\bar{\mu})$, a fórmula analítica falha devido à divisão por zero, refletindo a impossibilidade de construir uma fronteira com variação de retornos esperados.

**Questão 6:** Explique o papel do otimizador de Markowitz como um "amplificador de erros" em relação aos parâmetros de entrada ($\mu, \Sigma$).
*   **Resposta:** O otimizador busca matematicamente minimizar o risco para um dado retorno explorando todas as folgas numéricas fornecidas pelos dados. Ele atribui pesos elevados a ativos com altos retornos esperados estimativos ou baixas covariâncias estimativas. Quando há ruído de estimação em $\mu$, o otimizador foca nessas imperfeições pontuais, gerando oscilações drásticas nos pesos da carteira mesmo diante de pequenas alterações nos dados de entrada.

---

#### Nível 3 Difícil (Ensaio)

**Questão 7 (Ensaio):** Discuta a validade da Teoria da Fronteira Eficiente de Markowitz durante períodos de crise financeira extrema e travamento de liquidez. Em sua resposta, analise como a sincronização dos ativos afeta a matriz de covariância $\Sigma$ e qual o impacto disso sobre o conceito de diversificação.

*   **Guia de Resposta:** O ensaio deve enfatizar que a teoria de Markowitz assume um mundo onde a estrutura de covariância $\Sigma$ permanece explorável e relativamente estável. Durante regimes de estresse financeiro, ocorrem mecanismos de contágio e propagação de restrições de liquidez que sincronizam os ativos do mercado. Geometricamente, essa sincronização faz com que as correlações avancem em direção a 1 ($\rho \to 1$). À medida que o alinhamento entre os ativos se torna perfeito, o efeito de não-alinhamento que garante a diversificação colapsa. Consequentemente, a fronteira eficiente efetiva se dobra profundamente para dentro e a redução de risco via diversificação torna-se ineficaz. O candidato deve concluir que Markowitz é um bloco de cálculo indispensável para regimes estáveis, mas não descreve a totalidade do comportamento do sistema em momentos de transição de regime.

**Questão 8 (Ensaio):** Explique o Teorema da Separação em Dois Fundos sob a perspectiva geométrica do espaço risco-retorno. Como a introdução do ativo livre de risco $r_f$ altera a otimização de uma curva hiperbólica para uma solução linear tangente, e qual é a consequência prática disso para a tomada de decisão de investimento?

*   **Guia de Resposta:** O ensaio deve explicar que, na ausência de um ativo livre de risco, os investidores devem selecionar combinações exclusivamente no ramo superior hiperbólico da fronteira de ativos arriscados, onde a escolha do portfólio depende diretamente da aversão individual ao risco. Ao introduzir o ativo livre de risco $r_f$, o espaço de soluções expande-se para permitir combinações lineares entre $r_f$ e qualquer portfólio arriscado. A linha que maximiza o retorno por unidade de risco é aquela com a maior inclinação possível, correspondente à reta tangente à fronteira arriscada que parte de $(0, r_f)$ — a Linha de Alocação de Capital (CAL). O ponto de tangência estabelece uma única carteira de ativos arriscados ótima $\tilde{w}_T \propto \Sigma^{-1}\mu_{ex}$. A consequência prática é a separação das decisões: todos os investidores racionais escolhem rigorosamente a mesma proporção de ativos arriscados (a carteira de tangência) e atendem às suas preferências individuais de risco ajustando apenas a proporção alocada entre essa carteira e o ativo livre de risco (alavancagem).