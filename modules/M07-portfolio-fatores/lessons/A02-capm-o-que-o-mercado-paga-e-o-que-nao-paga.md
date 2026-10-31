<!-- imported from vault study notes; curated for open course -->
# M07.A02 — CAPM: o que o mercado paga (e o que não paga)

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M07
> **Aula:** M07.A02

↑ M07 · Resumo · Completo

**Módulo:** M07
**Pergunta do módulo:** Como alocar além do μ ingênuo e do “alpha” ilusório?

## Conceito-núcleo
CAPM: prêmio só por beta de mercado; alpha residual sob hipóteses fortes.

## Aplicação em mercado / trading
Separar prêmio de mercado de “alpha”; alinhar expectativa de retorno ao beta cotado.

## Entregável / lab
Regressão R_i ~ R_m: beta, alpha, R²; interpretação trading (hedge ratio ingênuo).

## Fonte (mapeamento)
quantitative-trading-free-lesson/25 capm-what-the-market-pays-for-and-what-it-does-not | IG beta / risk premium

## Guia de estudo aprofundado

> **info**
>

### Visão Geral e Conceitos-Chave

O modelo de precificação de ativos financeiros (CAPM — *Capital Asset Pricing Model*) estende a teoria de carteiras de Markowitz para responder o que o mercado recompensa em equilíbrio. Enquanto Markowitz resolve um problema individual de otimização média-variância, o CAPM determina qual parcela do risco possui um preço no mercado e qual parcela não é remunerada.

#### De Markowitz ao CAPM

Na abordagem de Markowitz, um investidor analisa um vetor de retornos esperados $\mu$ e uma matriz de covariância $\Sigma$ para definir pesos $w$ que organizam a troca entre retorno e variância. Isso permite construir uma fronteira eficiente local, movendo, espalhando e comprimindo o risco. No entanto, Markowitz não informa qual parte do risco é remunerada em equilíbrio nem precifica ativos individuais no âmbito sistêmico.

#### O Ativo Livre de Risco e a Geometria da Fronteira

A inclusão de um ativo livre de risco com taxa $r_f$ altera a geometria do problema de investimento. Em vez de mover-se ao longo de uma fronteira curva, o investidor pode combinar qualquer carteira de risco $w$ com o ativo livre de risco, gerando uma reta no plano de retorno-risco.

Considerando um portfólio de risco $w$ tal que:
$$\mathbf{1}^{\top}w = 1$$

Se $y$ for a fração de capital alocada nesse portfólio de risco, o restante $(1-y)$ é alocado no ativo livre de risco. As propriedades do portfólio combinado são:

*   **Retorno:** $R_p = r_f + y(R_w - r_f)$
*   **Retorno Esperado:** $\mathbb{E}[R_p] = r_f + y(\mathbb{E}[R_w] - r_f)$
*   **Risco (Desvio Padrão):** $\sigma_p = |y|\sigma_w$

A inclinação dessa reta representa o excesso de retorno por unidade de risco, ou seja, o Índice de Sharpe do portfólio $w$:
$$S(w) = \frac{\mathbb{E}[R_w] - r_f}{\sigma_w}$$

#### Portfólio de Tangência e Teorema da Separação

A reta dominante é aquela que maximiza o Índice de Sharpe. A carteira de risco que atinge essa inclinação máxima é o **portfólio de tangência**. 

Em forma matricial, a direção do portfólio de tangência é dada por:
$$w_T \propto \Sigma^{-1}(\mu - r_f\mathbf{1})$$

Após a normalização para que a soma dos pesos seja igual a 1 ($\mathbf{1}^{\top}\widetilde{w}_T = 1$), obtém-se:
$$\widetilde{w}_T = \frac{\Sigma^{-1}(\mu - r_f\mathbf{1})}{\mathbf{1}^{\top}\Sigma^{-1}(\mu - r_f\mathbf{1})}$$

**Teorema da Separação:** Se todos os investidores observarem os mesmos parâmetros $(\mu, \Sigma)$ e a mesma taxa $r_f$, todos identificarão o mesmo portfólio de tangência. As diferenças individuais entre investidores não afetam a composição do núcleo de risco, apenas o dimensionamento (alocação $y$ entre o ativo livre de risco e a carteira arriscada, podendo envolver alavancagem).

#### Equilíbrio de Mercado e Capital Market Line

No equilíbrio, como todos os investidores mantêm a mesma carteira de ativos arriscados, a agregação de todas as posições arriscadas da economia coincide com o **portfólio de mercado** ($w_M$):
$$\widetilde{w}_T = w_M$$

A reta que parte de $r_f$ e passa pelo portfólio de mercado é a **Capital Market Line (CML)**:
$$\mathbb{E}[R_p] = r_f + \frac{\mathbb{E}[R_M] - r_f}{\sigma_M}\sigma_p$$

A CML estabelece que, para carteiras eficientes, o excesso de retorno esperado é proporcional à sua volatilidade total ($\sigma_p$), tendo o Índice de Sharpe do mercado como inclinação.

#### Decomposição do Risco e Security Market Line

Para precificar um ativo individual $i$, o risco total é decomposto em uma componente sistemática e uma componente residual:
$$R_i - r_f = \beta_i(R_M - r_f) + \epsilon_i$$

Onde o Beta ($\beta_i$) e a ortogonalidade do resíduo são definidos por:
$$\beta_i = \frac{\mathrm{Cov}(R_i,R_M)}{\mathrm{Var}(R_M)}$$
$$\mathrm{Cov}(\epsilon_i,R_M) = 0$$

*   **Risco Idiossincrático ($\epsilon_i$):** É o ruído próprio do ativo (problemas de governança, anúncios isolados, acidentes locais). Como esse risco pode ser eliminado via diversificação em uma carteira ampla, o mercado não o recompensa. Em equilíbrio, sua expectativa é nula:
$$\mathbb{E}[\epsilon_i] = 0$$

*   **Risco Sistemático ($\beta_i$):** É a parcela do risco vinculada ao movimento do mercado que não pode ser eliminada por diversificação. É a única parcela remunerada pelo mercado.

Aplicando a expectativa na decomposição do ativo, obtém-se a equação do **CAPM**:
$$\mathbb{E}[R_i] - r_f = \beta_i(\mathbb{E}[R_M] - r_f)$$

Ou na forma completa da **Security Market Line (SML)**:
$$\mathbb{E}[R_i] = r_f + \beta_i(\mathbb{E}[R_M] - r_f)$$

Exprimindo em função da covariância:
$$\mathbb{E}[R_i] - r_f = \frac{\mathrm{Cov}(R_i,R_M)}{\mathrm{Var}(R_M)}(\mathbb{E}[R_M] - r_f)$$

---

### Intuição de Mercado e Trading

*   **O que o mercado paga:** O mercado paga exclusivamente pela contribuição marginal do ativo para o risco do portfólio de mercado (medida pela covariância / beta).
*   **O que o mercado NÃO paga:** O mercado não recompensa a volatilidade total isolada ($\sigma_i$), dispersão bruta, *drawdowns*, curtose ou estrutura de saltos de um ativo individual, desde que estes sejam idiossincráticos e diversificáveis.
*   **Comportamento do Beta ($\beta$):**
    *   $\beta_i = 1$: O ativo possui a mesma exposição sistemática que o mercado e exige o mesmo prêmio de risco.
    *   $\beta_i > 1$: O ativo amplifica os movimentos de mercado, carregando maior risco sistemático e exigindo maior prêmio.
    *   $\beta_i < 1$: O ativo move-se menos que o mercado em média, exigindo menor prêmio de risco.
    *   $\beta_i < 0$: O ativo move-se na direção oposta ao mercado, atuando como proteção (*hedge*). Seu retorno esperado pode ser inferior à taxa livre de risco ($r_f$) devido ao serviço de hedge prestado.

---

### Exemplo Numérico Resolvido Passo a Passo

#### Cenário de Mercado

Considere os seguintes dados observados no mercado:
*   Taxa livre de risco ($r_f$): $4\%$ ao ano ($0{,}04$)
*   Retorno esperado do mercado ($\mathbb{E}[R_M]$): $10\%$ ao ano ($0{,}10$)
*   Variância do mercado ($\mathrm{Var}(R_M)$): $0{,}04$

Dados de dois ativos individuais ($A$ e $B$):
*   Ativo $A$: Covariância com o mercado $\mathrm{Cov}(R_A, R_M) = 0{,}06$; Volatilidade total $\sigma_A = 40\%$
*   Ativo $B$: Covariância com o mercado $\mathrm{Cov}(R_B, R_M) = -0{,}01$; Volatilidade total $\sigma_B = 15\%$

#### Passo 1 Calcular o Prêmio de Risco do Mercado

$$\text{Prêmio de Mercado} = \mathbb{E}[R_M] - r_f = 0{,}10 - 0{,}04 = 0{,}06 \text{ (ou } 6\%\text{)}$$

#### Passo 2 Calcular o Beta ($\beta$) de cada ativo

*   **Ativo A:**
$$\beta_A = \frac{\mathrm{Cov}(R_A, R_M)}{\mathrm{Var}(R_M)} = \frac{0{,}06}{0{,}04} = 1{,}5$$

*   **Ativo B:**
$$\beta_B = \frac{\mathrm{Cov}(R_B, R_M)}{\mathrm{Var}(R_M)} = \frac{-0{,}01}{0{,}04} = -0{,}25$$

#### Passo 3 Calcular o Retorno Esperado de Equilíbrio ($\mathbb{E} R_i $) pela SML

*   **Ativo A:**
$$\mathbb{E}[R_A] = r_f + \beta_A(\mathbb{E}[R_M] - r_f)$$
$$\mathbb{E}[R_A] = 0{,}04 + 1{,}5 \times (0{,}06) = 0{,}04 + 0{,}09 = 0{,}13 \text{ (ou } 13\%\text{)}$$

*   **Ativo B:**
$$\mathbb{E}[R_B] = r_f + \beta_B(\mathbb{E}[R_M] - r_f)$$
$$\mathbb{E}[R_B] = 0{,}04 + (-0{,}25) \times (0{,}06) = 0{,}04 - 0{,}015 = 0{,}025 \text{ (ou } 2{,}5\%\text{)}$$

#### Análise do Resultado
Apesar de o Ativo $A$ possuir uma volatilidade total de $40\%$, seu retorno justo de equilíbrio é $13\%$, determinado estritamente pelo seu $\beta_A = 1{,}5$. O Ativo $B$, por ter $\beta_B = -0{,}25$, oferece um retorno esperado ($2{,}5\%$) abaixo da taxa livre de risco ($4\%$), pois funciona como seguro/hedge contra quedas do mercado.

---

### Armadilhas Comuns

| Armadilha | Explicação Correta |
| :--- | :--- |
| **Confundir CML e SML** | A **CML** relaciona retorno esperado e volatilidade total ($\sigma_p$) apenas para **carteiras eficientes**. A **SML** relaciona retorno esperado e risco sistemático ($\beta_i$) para **qualquer ativo individual ou carteira**. |
| **Acreditar que maior volatilidade total gera maior retorno** | Se uma ação possui oscilação alta motivada por fatores puramente idiossincráticos (ruídos internos), o mercado não concede prêmio por essa oscilação, pois ela é eliminável via diversificação. |
| **Atribuir prêmio ao risco idiossincrático ($\epsilon_i$)** | Se $\mathbb{E}[\epsilon_i] \neq 0$, seria possível isolar um portfólio sem exposição ao mercado com excesso de retorno positivo, quebrando a lógica de equilíbrio do modelo. |

---

### Laboratório Prático Sugerido em Python

O laboratório prático a seguir descreve os passos para implementar e verificar empiricamente as propriedades do CAPM através de simulação ou dados históricos.

#### Passo 1 Definição dos Parâmetros e Geração de Séries
*   Definir a taxa livre de risco $r_f$ e gerar uma série temporal para os retornos do índice de mercado $R_M$.
*   Sintetizar o retorno de um ativo $R_i$ definindo um parâmetro do sistema $\beta_{\text{alvo}}$ e adicionando um termo de ruído aleatório normal $\epsilon_i$ descorrelacionado do mercado.

#### Passo 2 Excesso de Retorno e Estimação do Beta
*   Calcular o excesso de retorno do mercado $(R_M - r_f)$ e do ativo $(R_i - r_f)$.
*   Calcular a covariância entre $(R_i - r_f)$ e $(R_M - r_f)$ e a variância do excesso do mercado.
*   Determinar o beta estimado via fórmula: $\beta_i = \frac{\mathrm{Cov}(R_i, R_M)}{\mathrm{Var}(R_M)}$.

#### Passo 3 Decomposição do Risco e Validação dos Resíduos
*   Calcular os resíduos da regressão: $\epsilon_i = (R_i - r_f) - \beta_i(R_M - r_f)$.
*   Verificar programmaticamente que a média do resíduo $\mathbb{E}[\epsilon_i]$ aproxima-se de zero.
*   Verificar que a covariância entre o resíduo e o mercado $\mathrm{Cov}(\epsilon_i, R_M)$ é igual a zero.

#### Passo 4 Comparação com a Security Market Line
*   Calcular a média do retorno do ativo e comparar com o valor teórico predito pela equação do CAPM: $\mathbb{E}[R_i] = r_f + \beta_i(\mathbb{E}[R_M] - r_f)$.
*   Aumentar a variância do ruído idiossincrático $\epsilon_i$ e observar que, embora a volatilidade total $\sigma_i$ aumente, o retorno médio exigido de equilíbrio via CAPM permanece inalterado.

---

### Glossário

*   **Beta ($\beta_i$):** Medida da sensibilidade do retorno de um ativo em relação aos movimentos do portfólio de mercado. Representa a quantidade de risco sistemático de um ativo.
*   **Capital Market Line (CML):** Reta que representa a relação entre retorno esperado e volatilidade total ($\sigma_p$) para carteiras eficientes formadas pela combinação do ativo livre de risco e o portfólio de mercado.
*   **Índice de Sharpe ($S(w)$):** Razão entre o excesso de retorno esperado de um portfólio em relação à taxa livre de risco e seu desvio padrão (risco total).
*   **Portfólio de Mercado ($w_M$):** Carteira hipotética composta por todos os ativos com risco disponíveis na economia, ponderados por seus valores de mercado. No equilíbrio do CAPM, coincide com o portfólio de tangência.
*   **Portfólio de Tangência ($w_T$):** Carteira de ativos arriscados que maximiza o Índice de Sharpe na fronteira eficiente de Markowitz.
*   **Risco Idiossincrático ($\epsilon_i$):** Risco específico, pontual ou não sistemático de um ativo individual (ex.: falhas de gestão, anúncios pontuais). É completamente diversificável em uma carteira ampla.
*   **Risco Sistemático:** Risco macroeconômico agregador que afeta todo o sistema financeiro e não pode ser eliminado por diversificação.
*   **Security Market Line (SML):** Reta gráfica da equação do CAPM que relaciona o retorno esperado de qualquer ativo individual ou carteira com o seu nível de risco sistemático ($\beta$).
*   **Teorema da Separação:** Resultado formal indicando que a decisão de otimização da carteira de ativos arriscados é idêntica para todos os investidores, independentemente de suas preferências individuais de risco.

---

### Questões de Fixação e Avaliação

#### Nível 1 Resposta Curta

1. Qual é a limitação central da teoria de seleção de carteiras de Markowitz que o modelo CAPM resolve?
2. Em um cenário de equilíbrio do CAPM, qual é o valor esperado do resíduo específico $\mathbb{E}[\epsilon_i]$ de um ativo e por quê?
3. O que acontece com a geometria da fronteira eficiente quando um ativo livre de risco ($r_f$) é adicionado ao conjunto de investimentos?

#### Nível 2 Analíticas e Numéricas

4. Um ativo $X$ possui uma volatilidade total $\sigma_X = 50\%$, enquanto o mercado possui volatilidade $\sigma_M = 20\%$. Sabendo que a correlação entre o ativo $X$ e o mercado é $0{,}6$, a taxa livre de risco é $3\%$ e o retorno esperado do mercado é $9\%$:
   * a) Calcule o Beta ($\beta_X$) do ativo.
   * b) Determine o retorno esperado do ativo $X$ segundo o CAPM.
5. Explique resumidamente por que um ativo com Beta negativo ($\beta < 0$) pode apresentar um retorno esperado inferior à taxa livre de risco ($r_f$) sem violar o equilíbrio de mercado.

#### Nível 3 Dissertativas

6. Compare e contraste a *Capital Market Line* (CML) e a *Security Market Line* (SML). Explique qual medida de risco é utilizada em cada uma, a quais tipos de ativos/carteiras se aplicam e por que um ativo individual altamente volátil não se posiciona necessariamente acima da SML.
7. Discuta a relação entre o Teorema da Separação e a formação do Portfólio de Mercado em equilíbrio. Como as diferenças individuais de aversão ao risco entre investidores são acomodadas no modelo CAPM?

---

### Gabarito e Respostas Explicadas

#### Respostas do Nível 1

1. **Resposta:** O modelo de Markowitz é uma otimização individual (local) que não define quais riscos têm preço no equilíbrio de mercado nem precifica ativos individuais com base na sua contribuição para o risco sistêmico. O CAPM resolve essa lacuna ao introduzir o equilíbrio e a precificação do risco sistemático.
2. **Resposta:** O valor esperado é zero ($\mathbb{E}[\epsilon_i] = 0$). Sendo o risco idiossincrático totalmente eliminável por meio da diversificação, o mercado não oferece um prêmio médio para remunerar essa componente.
3. **Resposta:** A fronteira eficiente deixa de ser uma curva no plano retorno-risco e passa a ser representada por linhas retas que partem do ponto da taxa livre de risco $r_f$ no eixo vertical.

#### Respostas do Nível 2

4. **Resolução:**
   * a) Sabendo que $\mathrm{Cov}(R_X, R_M) = \rho_{X,M} \cdot \sigma_X \cdot \sigma_M = 0{,}6 \times 0{,}50 \times 0{,}20 = 0{,}06$.
      A variância do mercado é $\mathrm{Var}(R_M) = \sigma_M^2 = 0{,}20^2 = 0{,}04$.
      O Beta é:
      $$\beta_X = \frac{\mathrm{Cov}(R_X, R_M)}{\mathrm{Var}(R_M)} = \frac{0{,}06}{0{,}04} = 1{,}5$$
   * b) Aplicando a equação do CAPM:
      $$\mathbb{E}[R_X] = r_f + \beta_X(\mathbb{E}[R_M] - r_f) = 0{,}03 + 1{,}5 \times (0{,}09 - 0{,}03) = 0{,}03 + 1{,}5 \times (0{,}06) = 0{,}12 \text{ (ou } 12\%\text{)}$$

5. **Resposta:** Um ativo com $\beta < 0$ se move em direção oposta ao mercado, reduzindo o risco total de uma carteira diversificada. Ele atua como um instrumento de proteção (*hedge*). Devido a esse benefício de mitigação de risco sistêmico, os investidores aceitam receber um retorno esperado inferior à taxa livre de risco $r_f$.

#### Respostas do Nível 3

6. **Resposta:** A CML utiliza o risco total (desvio padrão $\sigma_p$) e é aplicável exclusivamente a carteiras eficientes. Sua inclinação é o Índice de Sharpe do mercado. A SML utiliza o risco sistemático (Beta $\beta_i$) e é aplicável a qualquer ativo individual ou carteira (eficiente ou não). Um ativo individual altamente volátil pode possuir grande parte dessa volatilidade concentrada em risco idiossincrático ($\epsilon_i$). Como a SML precifica apenas a exposição ao risco sistemático ($\beta_i$), essa alta volatilidade bruta não desloca o ativo para cima na SML; seu retorno de equilíbrio dependerá apenas da sua covariância com o mercado.

7. **Resposta:** O Teorema da Separação estabelece que a escolha da carteira de ativos com risco é isolada da aversão individual ao risco do investidor. Como todos observam os mesmos parâmetros $(\mu, \Sigma)$ e $r_f$, todos encontram o mesmo portfólio de tangência $w_T$. No equilíbrio, a agregação de todas as posições arriscadas força $w_T$ a ser igual ao portfólio de mercado $w_M$. As diferenças individuais de aversão ao risco são acomodadas exclusivamente pela alocação de capital $y$ entre o ativo livre de risco e o portfólio de mercado $w_M$ (investidores mais conservadores mantêm maior proporção em $r_f$, enquanto investidores mais arrojados utilizam alavancagem).