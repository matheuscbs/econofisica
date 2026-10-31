<!-- imported from vault study notes; curated for open course -->
# M01.A04 — Lema de Itô: por que o hedge contínuo gera um termo extra de variância

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M01
> **Aula:** M01.A04

↑ M01 · Resumo · Completo

**Módulo:** M01
**Pergunta do módulo:** Como precificar e fazer hedge de opções vanila sem “adivinhar” o drift?

## Conceito-núcleo
Itô: dF = … + (1/2)F_SS σ²S² dt — o segundo termo muda o P&L do hedge dinâmico.

## Aplicação em mercado / trading
Entender theta vs gamma no livro de opções; não tratar o P&L de hedge como “só delta”.

## Entregável / lab
Derivação guiada + notebook: expansão de Itô em GBM e impacto no P&L de um call hedged.

## Fonte (mapeamento)
quantitative-trading-free-lesson/04 ito's lemma | IG pinned + Reel difusão/Itô

## Guia de estudo aprofundado

> **info**
>

Este guia de estudos aborda a transformação estocástica do preço de um ativo sob o Movimento Castanho Geométrico (GBM), demonstrando a aplicação do Lema de Itô para a função de log-preço $X_t = \ln(S_t)$. O material traz os fundamentos matemáticos, a intuição econômica de mercado, procedimentos computacionais em Python e exercícios práticos em três níveis de complexidade.

---

### Visão Geral e Objetivos de Aprendizado

* Compreender a limitação da análise matemática clássica quando aplicada a variáveis financeiras estocásticas.
* Dominar a regra de tradução do Lema de Itô e a propriedade geométrica fundamental do ruído: $(dW_t)^2 = dt$.
* Derivar rigorosamente o drift corrigido do log-preço $\tilde{\mu} = \mu - \frac{1}{2}\sigma^2$.
* Entender o impacto da curvatura (convexidade/concavidade) das funções no comportamento determinístico do ruído.
* Desenvolver um pipeline de verificação empírica via simulação de Monte Carlo em Python.

---

### Conceitos-Chave Explicados em Profundidade

#### A Dinâmica do Movimento Castanho Geométrico

O mercado financeiro fornece apenas o preço atual do ativo. Para projetar cenários futuros e distribuições de probabilidade de $S_T$, é necessário definir uma dinâmica estocástica. O Movimento Castanho Geométrico (GBM) é o modelo de referência, definido pela Equação Diferencial Estocástica (SDE):

$$dS_t = \mu S_t \, dt + \sigma S_t \, dW_t, \qquad S_0 > 0$$

onde:
* $\mu$ representa o drift (taxa de retorno esperada instantânea do preço).
* $\sigma$ representa a volatilidade do ativo.
* $dW_t$ é o incremento de um processo de Wiener (Movimento Castanho).

Embora o GBM seja uma dinâmica considerada "pobre" por possuir poucos parâmetros, ele é suficiente para gerar uma lei de probabilidade utilizável para os preços.

#### Cálculo Clássico vs. Cálculo Estocástico

Ao transformar uma variável que possui ruído — por exemplo, aplicando o logaritmo, calculando retornos ou analisando o *payoff* de uma opção —, não se pode utilizar a análise matemática clássica. Em variáveis com ruído estocástico, a expansão de Taylor não pode ser truncada na primeira ordem, pois o ruído possui uma geometria própria no tempo contínuo:

$$(dW_t)^2 = dt$$

Se a transformação for tratada pela análise clássica (ignorando os termos de segunda ordem), a taxa de variação esperada (drift) será calculada incorretamente. Consequentemente, a distribuição de probabilidade projetada e a precificação derivada estarão erradas.

#### O Lema de Itô como Regra de Tradução

O Lema de Itô é a regra de tradução que estabelece como uma função $f(S_t)$ se move quando $S_t$ é submetido a um ruído estocástico. Para uma função derivável $f(S)$, a variação $df(S_t)$ é dada por:

$$df(S_t) = f'(S_t) dS_t + \frac{1}{2} f''(S_t) (dS_t)^2$$

A presença do termo de segunda ordem $\frac{1}{2} f''(S_t) (dS_t)^2$ é a diferença crucial em relação ao cálculo tradicional.

#### Derivação do Drift do Log-Preço $X_t = \ln(S_t)$

Para analisar o log-preço, define-se a função $f(S) = \ln(S)$.

1. **Cálculo das Derivadas Primária e Secundária:**
   $$f'(S) = \frac{1}{S}$$
   $$f''(S) = -\frac{1}{S^2}$$

2. **Cálculo de $(dS_t)^2$:**
   Substituindo a dinâmica do GBM:
   $$(dS_t)^2 = (\mu S_t \, dt + \sigma S_t \, dW_t)^2$$
   Ao expandir o quadrado, os termos em $dt^2$ e $dt \, dW_t$ são infinitesimais de ordem superior e colapsam para zero. O único termo sobrevivente vem de $(dW_t)^2 = dt$:
   $$(dS_t)^2 = \sigma^2 S_t^2 (dW_t)^2 = \sigma^2 S_t^2 \, dt$$

3. **Injeção no Lema de Itô:**
   $$dX_t = \frac{1}{S_t} \left( \mu S_t \, dt + \sigma S_t \, dW_t \right) + \frac{1}{2} \left( -\frac{1}{S_t^2} \right) \left( \sigma^2 S_t^2 \, dt \right)$$

4. **Simplificação Térmica e Resultado:**
   $$dX_t = \mu \, dt + \sigma \, dW_t - \frac{1}{2} \sigma^2 \, dt$$
   $$dX_t = \left( \mu - \frac{1}{2} \sigma^2 \right) dt + \sigma \, dW_t$$

O log-preço $X_t$ não mantém o drift original $\mu$. Ele sofre uma correção exata de $-\frac{1}{2}\sigma^2$, resultando no drift corrigido $\tilde{\mu}$:

$$\tilde{\mu} = \mu - \frac{1}{2}\sigma^2$$

#### Solução da SDE e Propriedades Estatísticas

Como a SDE de $dX_t$ possui drift e difusão constantes, a integração direta sobre o intervalo $[0, t]$ fornece:

$$X_t = X_0 + \left( \mu - \frac{1}{2}\sigma^2 \right) t + \sigma W_t$$

com $X_0 = \ln(S_0)$. Dado que $W_t \sim \mathcal{N}(0, t)$, a variável $X_t$ segue uma distribuição Normal com os seguintes momentos teóricos:

$$\mathbb{E}[X_t] = \ln(S_0) + \left( \mu - \frac{1}{2}\sigma^2 \right) t$$
$$\operatorname{Var}(X_t) = \sigma^2 t$$

---

### Intuição de Mercado e Trading

* **Multiplicação vs. Adição:** O preço $S_t$ move-se por acoplamento multiplicativo. A transformação logarítmica converte essas variações multiplicativas em um processo aditivo no log-preço.
* **O Custo da Volatilidade:** A transformação logarítmica é uma função côncava ($f''(S) < 0$). O ruído e a volatilidade criam um termo de média determinístico na dinâmica transformadora. Devido à concavidade do logaritmo, o ruído reduz a taxa de crescimento média contínua do log-preço em relação à taxa de crescimento simples do ativo.
* **Mecanismo da Correção:** O termo $-\frac{1}{2}\sigma^2$ não é uma suposição heurística ou intuitiva; é o resultado inevitável da geometria do cálculo estocástico dada por $(dW_t)^2 = dt$.

---

### Exemplo Numérico Resolvido Passo a Passo

#### Cenário de Aplicação
Considere um ativo com as seguintes características:
* Preço inicial: $S_0 = 100$
* Drift do preço ($S_t$): $\mu = 0{,}10$ (10% ao ano)
* Volatilidade: $\sigma = 0{,}20$ (20% ao ano)
* Horizon temporal: $T = 1{,}0$ ano

#### Passo 1 Calcular o Log-Preço Inicial $X_0$
$$X_0 = \ln(S_0) = \ln(100) \approx 4{,}605170$$

#### Passo 2 Calcular o Drift Corrigido do Log-Preço ($\tilde{\mu}$)
$$\tilde{\mu} = \mu - \frac{1}{2}\sigma^2$$
$$\tilde{\mu} = 0{,}10 - 0{,}5 \times (0{,}20)^2$$
$$\tilde{\mu} = 0{,}10 - 0{,}5 \times 0{,}04 = 0{,}10 - 0{,}02 = 0{,}08 \text{ (8\% ao ano)}$$

#### Passo 3 Calcular o Valor Esperado Teórico $\mathbb{E} X_T $
$$m(T) = \mathbb{E}[X_T] = \ln(S_0) + \tilde{\mu} T$$
$$m(T) = 4{,}605170 + 0{,}08 \times 1{,}0 = 4{,}685170$$

#### Passo 4 Calcular a Variância Teórica $\operatorname{Var}(X_T)$
$$v(T) = \operatorname{Var}(X_T) = \sigma^2 T$$
$$v(T) = (0{,}20)^2 \times 1{,}0 = 0{,}04$$

---

### Armadilhas Comuns

1. **Ignorar o termo de segunda ordem:** Aplicar a regra da cadeia da análise clássica para obter $d(\ln S_t) = \frac{1}{S_t} dS_t = \mu \, dt + \sigma \, dW_t$. Isso omite o termo de correção de variância $-\frac{1}{2}\sigma^2$.
2. **Confundir a média de $S_T$ com a média de $\ln(S_T)$:** A taxa de retorno simples esperada do preço é $\mu$, mas a taxa esperada do crescimento do log-preço é $\mu - \frac{1}{2}\sigma^2$.
3. **Errar a potência do incremento estocástico:** Tratar $(dW_t)^2$ como se fosse um valor infinitesimal negligenciável de ordem $dt^2$, esquecendo que $(dW_t)^2 = dt$.

---

### Laboratório Prático em Python

Este procedimento descreve a implementação para simular a dinâmica do GBM, transformar os preços finais em escala logarítmica e verificar numericamente se o drift e a variância amostrais correspondem às equações teóricas de Itô.

#### Passos de Implementação

1. **Definição de Parâmetros e Grade Temporal:**
   Defina os parâmetros do modelo ($\mu$, $\sigma$, $T$, $S_0$, $nsteps$).
   Calcule o tamanho do passo temporal e a taxa teórica do log-preço:
   ```python
   dt = T / nsteps
   mu_tilde = mu - 0.5 * sigma**2
   print(f"mu_tilde (drift of ln S) = {mu_tilde:.6f}")
   ```

2. **Extração e Métricas Teóricas do Log-Preço Final:**
   Após realizar a simulação Monte Carlo para obter os preços finais `ST = S[:, -1]`, calcule a transformação logarítmica e suas estatísticas amostrais:
   ```python
   XT = np.log(ST)
   mean_X_emp = XT.mean()
   var_X_emp = XT.var(ddof=1)

   mean_X_th = mT
   var_X_th = vT
   ```

3. **Estimativa do Drift Empírico por Incrementos:**
   Aplique a transformação logarítmica em toda a matriz de trajetórias $S$ para medir os incrementos passo a passo e estimar o drift simulado ($\hat{\tilde{\mu}}$):
   ```python
   X = np.log(S)
   dX = X[:, 1:] - X[:, :-1]
   mu_tilde_hat = dX.mean() / dt
   ```

4. **Validação dos Resultados e Impressão de Erros:**
   Compare as métricas empíricas extraídas da simulação com os valores teóricos esperados:
   ```python
   print(
       f"E[X_T]   = {mean_X_emp:.6f}    (error = {mean_X_emp - mean_X_th:+.6e})"
   )
   print(
       f"Var[X_T] = {var_X_emp:.6f}    (error = {var_X_emp - var_X_th:+.6e})"
   )
   print(
       f"mu_tilde_hat = {mu_tilde_hat:.6f}    (error ="
       f" {mu_tilde_hat - mu_tilde:+.6e})"
   )
   ```

Conforme o número de simulações $N$ e passos $nsteps$ aumentam, as médias empíricas e a estimativa `mu_tilde_hat` convergem de forma precisa para $\mu - \frac{1}{2}\sigma^2$.

---

### Glossário de Termos Importantes

* **Movimento Castanho Geométrico (GBM):** Processo estocástico em tempo contínuo $dS_t = \mu S_t dt + \sigma S_t dW_t$ onde os retornos logarítmicos são normalmente distribuídos.
* **Lema de Itô:** Teorema fundamental do cálculo estocástico que fornece a expansão para diferenciação de funções de processos estocásticos.
* **Drift Corrigido ($\tilde{\mu}$):** Taxa de variação média esperada do log-preço de um ativo sob GBM, equivalente a $\mu - \frac{1}{2}\sigma^2$.
* **Geometria do Ruído Estocástico:** Propriedade do processo de Wiener que determina que a variação quadrática acumulada dos incrementos é determinística, ou seja, $(dW_t)^2 = dt$.
* **Efeito de Curvatura:** Ajuste determinístico em $dt$ no drift resultante da segunda derivada $f''(S)$ de uma função aplicada a um processo estocástico.

---

### Questões e Exercícios

#### Nível 1 Resposta Curta (Short-Answer Quiz)

**Questão 1:** Por que a relação $(dW_t)^2 = dt$ é fundamental no cálculo estocástico e diferente do cálculo diferencial clássico?
> **Resposta:** No cálculo clássico, os incrementos quadráticos $(dt)^2$ são negligenciáveis. No cálculo estocástico, a variação do ruído $dW_t$ é da ordem de $\sqrt{dt}$, tornando o seu quadrado $(dW_t)^2$ exatamente igual a $dt$. Isso introduz termos determinísticos de segunda ordem que afetam diretamente a média do sistema.

**Questão 2:** Qual é a expressão formal do drift corrigido da variável $X_t = \ln(S_t)$ quando $S_t$ segue um Movimento Castanho Geométrico?
> **Resposta:** O drift corrigido é $\tilde{\mu} = \mu - \frac{1}{2}\sigma^2$.

**Questão 3:** Como a concavidade da função $f(S) = \ln(S)$ afeta o drift resultante do log-preço?
> **Resposta:** Como a derivada segunda da função logarítmica é negativa ($f''(S) = -1/S^2$), a função é côncava. O termo de ajuste de Itô $\frac{1}{2} f''(S) (dS)^2$ torna-se negativo, subtraindo $\frac{1}{2}\sigma^2$ do drift original.

---

#### Nível 2 Questões Práticas e Intermediárias

**Questão 1:** A partir da SDE $dS_t = \mu S_t dt + \sigma S_t dW_t$, demonstre passo a passo por que a expressão $(dS_t)^2$ se reduz a $\sigma^2 S_t^2 dt$.
> **Resposta:**
> Ao elevar a dinâmica ao quadrado:
> $$(dS_t)^2 = (\mu S_t dt + \sigma S_t dW_t)^2$$
> $$(dS_t)^2 = \mu^2 S_t^2 (dt)^2 + 2 \mu \sigma S_t^2 (dt)(dW_t) + \sigma^2 S_t^2 (dW_t)^2$$
> Aplicando as regras de multiplicação de Itô: $(dt)^2 = 0$, $(dt)(dW_t) = 0$, e $(dW_t)^2 = dt$.
> O primeiro e o segundo termos zeram, restando apenas:
> $$(dS_t)^2 = \sigma^2 S_t^2 dt$$

**Questão 2:** Um ativo possui tendência esperada $\mu = 12\%$ ao ano e volatilidade $\sigma = 30\%$ ao ano. Sabendo que o preço inicial é $S_0 = 50$:
1. Calcule o drift do log-preço $\tilde{\mu}$.
2. Determine o valor esperado do log-preço $\mathbb{E}[X_T]$ para $T = 2$ anos.
3. Determine a variância teórica do log-preço em $T = 2$ anos.

> **Resposta:**
> 1. $\tilde{\mu} = \mu - \frac{1}{2}\sigma^2 = 0{,}12 - 0{,}5 \times (0{,}30)^2 = 0{,}12 - 0{,}5 \times 0{,}09 = 0{,}12 - 0{,}045 = 0{,}075$ (7,5% ao ano).
> 2. $X_0 = \ln(50) \approx 3{,}912023$.
>    $$\mathbb{E}[X_2] = \ln(50) + \tilde{\mu} \times 2 = 3{,}912023 + 0{,}075 \times 2 = 3{,}912023 + 0{,}15 = 4{,}062023$$
> 3. $\operatorname{Var}(X_2) = \sigma^2 T = (0{,}30)^2 \times 2 = 0{,}09 \times 2 = 0{,}18$.

---

#### Nível 3 Questões Discursivas para Aprofundamento

**Questão 1:** Explique por que a aplicação ingênua do cálculo diferencial clássico à transformação de preços de ativos acarreta erros na modelagem de cenários e precificação. Na sua resposta, relacione a geometria do ruído estocástico e a curvatura da função de transformação com a necessidade do Lema de Itô.

> **Resposta:**
> A análise clássica assume que as funções são suaves e que variações quadráticas infinitesimais podem ser ignoradas, usando a aproximação $df(S) \approx f'(S)dS$. No entanto, os preços de ativos financeiros no tempo contínuo contêm componentes estocásticos ruidosos representados pelo Movimento Castanho. 
> A geometria desse ruído implica que o incremento de Wiener $dW_t$ possui magnitude de ordem $\sqrt{dt}$, o que faz com que sua variação quadrática acumulada não desapareça no limite contínuo, convergindo para $(dW_t)^2 = dt$.
> Ao transformar a escala dos preços por meio de uma função não linear $f(S)$, como o logaritmo, a curvatura da função (medida por sua segunda derivada $f''(S)$) interage diretamente com esse ruído persistente. Se a função for côncava (como o logaritmo), a oscilação do ruído gera um deslocamento descendente determinístico na média da nova variável. Ignorar a segunda ordem da expansão de Itô omite esse ajuste determinístico em $dt$, resultando em uma estimativa incorreta do drift ($\mu$ em vez de $\mu - \frac{1}{2}\sigma^2$). Isso corrompe toda a distribuição de probabilidade projetada do ativo e invalida modelos de precificação de derivativos baseados nessa dinâmica.

**Questão 2:** Descreva como a estrutura do laboratório prático em Python valida empiricamente a teoria do Lema de Itô. Explique o papel dos incrementos logarítmicos `dX`, a razão de sua divisão por `dt` e o comportamento esperado do erro amostral conforme $N$ (número de simulações) e $nsteps$ crescem.

> **Resposta:**
> O laboratório prático em Python funciona como um ambiente de validação monte carlo para a teoria estocástica. Ao gerar trajetórias de preços $S_t$ via discretização do GBM e calcular o log-preço $X = \ln(S)$, o código extrai os incrementos discretos $dX = X[:, 1:] - X[:, :-1]$.
> Como $dX_t = \tilde{\mu} dt + \sigma dW_t$, a média esperada desses incrementos é $\mathbb{E}[dX_t] = \tilde{\mu} dt$. Ao dividir a média amostral dos incrementos `dX.mean()` por `dt`, isola-se a estimativa do drift empírico `mu_tilde_hat`.
> A teoria prevê que `mu_tilde_hat` deve ser idêntico a $\mu - \frac{1}{2}\sigma^2$, e não a $\mu$. Conforme o número de caminhos $N$ aumenta, o erro amostral decrece devido à Lei dos Grandes Números. Paralelamente, o aumento do número de passos $nsteps$ reduz os erros de discretização temporal. A verificação do erro `mean_X_emp - mean_X_th` e `mu_tilde_hat - mu_tilde` aproximando-se de zero confirma visual e numericamente a existência do termo de correção derivado pelo Lema de Itô.