<!-- imported from vault study notes; curated for open course -->
# M07.A04 — APT e multifatores: quando “alpha” era beta que faltava

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M07
> **Aula:** M07.A04

↑ M07 · Resumo · Completo

**Módulo:** M07
**Pergunta do módulo:** Como alocar além do μ ingênuo e do “alpha” ilusório?

## Conceito-núcleo
APT/fatores: retornos explicados por múltiplos riscos; smart beta; “no alpha without beta”.

## Aplicação em mercado / trading
Atribuir P&L a fatores; evitar vender como alpha o que é exposição a valor/momentum/etc.

## Entregável / lab
Decomposição simples: regressão multifatorial e relatório de exposições do book.

## Fonte (mapeamento)
quantitative-trading-free-lesson/27 apt-and-multi-factor-models-when-“alpha”-was-just-a-missing-factor | IG smart beta / no alpha without beta

## Guia de estudo aprofundado

> **info**
>

Este guia de estudo oferece uma análise aprofundada da Teoria de Precificação por Arbitragem (APT - *Arbitrage Pricing Theory*) e dos modelos multifatoriais, abordando a transição conceitual do CAPM unifatorial para estruturas de múltiplos fatores, a reinterpretação do conceito de *alpha*, as formulações matemáticas rigorosas, intuições de mercado, exemplos práticos e questões de autoavaliação.

---

### Visão Geral e Conceitos-Chave

#### A Limitação do CAPM e a Origem do APT
O Modelo de Precificação de Ativos Financeiros (CAPM) estabeleceu que o mercado não paga pelo risco abstrato ou pela volatilidade bruta de um ativo, mas sim pelo risco sistêmico — a fração do risco que não pode ser eliminada via diversificação. No entanto, na prática empírica, os resíduos do CAPM frequentemente não desaparecem de forma limpa. Resta uma deriva consistente, um prêmio não explicado denominado *alpha* ($\alpha$).

Diante da persistência desse resíduo, surgem duas interpretações possíveis:
1. **Hipótese de Ineficiência:** O mercado está precificado incorretamente, é irracional e oferece retornos gratuitos.
2. **Hipótese de Má Especificação:** O modelo é excessivamente simplista e omitiu forças comuns do sistema.

O APT surge adotando a segunda hipótese: o sistema financeiro possui múltiplos motores e fontes de restrição comuns. O *alpha* observado em modelos de fator único geralmente não é um ganho anômalo ou habilidade pura, mas a manifestação de um fator sistêmico ausente no modelo.

#### Estrutura do Modelo de Decomposição
Em vez de depender de uma única direção central (o portfólio de mercado), o APT decompõe o retorno de um ativo em uma combinação de exposições a múltiplos fatores transversais, acrescida de um resíduo idiossincrásico.

A equação de decomposição do retorno do ativo $i$ é expressa por:

$$R_i = \alpha_i + \beta_{i1}F_1 + \beta_{i2}F_2 + \cdots + \beta_{iK}F_K + \epsilon_i$$

Onde:
* **$R_i$**: Retorno do ativo $i$.
* **$\alpha_i$**: Intercepto (resíduo condicional ao modelo).
* **$F_k$**: Fatores comuns representativos de forças sistêmicas (ex.: crescimento, inflação, *spread* de crédito, inclinação da curva, *momentum*, valor, liquidez, *carry*).
* **$\beta_{ik}$**: Cargas ou sensibilidades (*loadings*) do ativo $i$ em relação ao fator $k$, representando a geometria de exposição do ativo à restrição compartilhada.
* **$\epsilon_i$**: Ruído local ou acidente idiossincrásico do ativo $i$.

#### Condições Mecânicas Mínimas do Resíduo
Para que o modelo seja bem especificado e a estrutura seja válida, o termo de erro $\epsilon_i$ deve respeitar duas restrições fundamentais:

$$E[\epsilon_i] = 0$$

$$Cov(\epsilon_i, F_k) = 0 \quad \text{para todo } k$$

Se a covariância entre o resíduo e qualquer fator for diferente de zero, o resíduo contém uma força comum omitida, configurando um erro de especificação do modelo.

#### Da Decomposição à Equação de Precificação
Se o risco sistêmico for devidamente coberto pelos $K$ fatores e se o resíduo $\epsilon_i$ for suficientemente diversificável em uma carteira ampla, a ausência de arbitragem exige que o retorno esperado seja uma função linear das exposições aos fatores.

Caso contrário, seria possível construir portfólios que neutralizam os fatores comuns, diversificam o risco idiossincrásico e ainda assim mantêm um ganho positivo líquido — o que caracterizaria uma oportunidade de arbitragem, e não um "estilo" de investimento.

A equação de precificação do retorno esperado é dada por:

$$E[R_i] = r_f + \beta_{i1}\lambda_1 + \beta_{i2}\lambda_2 + \cdots + \beta_{iK}\lambda_K$$

Em formato de retorno em excesso ($R_{i,ex} = R_i - r_f$):

$$E[R_{i,ex}] = \sum_{k=1}^{K} \beta_{ik}\lambda_k$$

Onde $\lambda_k$ representa o prêmio de risco associado ao fator $k$.

---

### Equações Fundamentais

A tabela abaixo resume as formulações matemáticas centrais da Teoria de Precificação por Arbitragem.

| Conceito | Formulação Matemática | Descrição / Significado |
| :--- | :--- | :--- |
| **Decomposição do Retorno** | $R_i = \alpha_i + \sum_{k=1}^{K} \beta_{ik}F_k + \epsilon_i$ | Separa o retorno individual entre componentes sistêmicos ($\beta_{ik}F_k$) e idiossincrásicos ($\epsilon_i$). |
| **Restrições dos Erros** | $E[\epsilon_i] = 0 \quad \text{e} \quad Cov(\epsilon_i, F_k) = 0$ | Garante que o resíduo seja estritamente ruído não correlacionado aos fatores. |
| **Retorno Esperado (Absoluto)**| $E[R_i] = r_f + \sum_{k=1}^{K} \beta_{ik}\lambda_k$ | O retorno esperado é a taxa livre de risco somada ao produto das cargas pelos preços dos riscos. |
| **Retorno Esperado em Excesso**| $E[R_{i,ex}] = \sum_{k=1}^{K} \beta_{ik}\lambda_k$ | O excesso de retorno esperado é totalmente explicado pela combinação linear de vetores de risco e seus prêmios ($\lambda_k$). |
| **Exposição do Portfólio** | $\beta_{p,k} = \sum_{i=1}^{N} w_i\beta_{ik}$ | A sensibilidade da carteira ao fator $k$ é a média ponderada dos $\beta$s dos ativos integrantes. |
| **Excesso de Retorno do Portfólio**| $E[R_{p,ex}] = \sum_{k=1}^{K} \beta_{p,k}\lambda_k$ | A remuneração esperada do portfólio depende diretamente da sua assinatura final de exposição aos fatores. |

---

### Intuição de Mercado e Trading

#### A Natureza Sistemática dos Fatores
No mercado financeiro, um fator não é uma mera variável estatística ou uma lista de preferências passageiras. Um fator é a expressão matemática de uma restrição compartilhada no sistema financeiro. 

Quando ocorrem choques macroeconômicos ou estruturais — como a compressão da duração (*duration*), o alargamento de *spreads* de crédito, choques de liquidez ou desaceleração da atividade —, os ativos não reagem de forma isolada. Eles se movimentam em blocos de acordo com suas conexões com esses motores comuns.

```
                  [ Choque Sistêmico / Restrição Comum ]
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
[ Transmissão: Fator 1 ]  [ Transmissão: Fator 2 ]  [ Transmissão: Fator K ]
         │                          │                          │
         ├──────────────────────────┼──────────────────────────┤
         ▼                          ▼                          ▼
[ Ativo A (Beta A,1) ]     [ Ativo B (Beta B,2) ]     [ Ativo C (Beta C,K) ]
```

#### O Conceito Relativo de Alpha
O termo *alpha* não possui existência absoluta; ele é sempre condicional à estrutura do modelo adotado:
* Em um modelo CAPM unifatorial, uma carteira exposta aos fatores de valor ou liquidez pode apresentar um $\alpha$ expressivo.
* Ao expandir o espaço de fatores para incluir esses vetores (incorporando modelos como Fama-French, Carhart, ou estruturas de *quality*, *low vol*, *carry* e *liquidity*), o $\alpha$ anterior se dissolve, transformando-se em exposição explicada ($\beta$).

#### Insuficiência da Volatilidade Bruta
Duas carteiras ou ativos podem apresentar exatamente a mesma variância/volatilidade total, mas possuírem mecânicas de risco completamente distintas. Se os vetores de exposição ($\beta_{p}$) forem direcionados a fatores diferentes (por exemplo, uma exposta ao fator de crescimento e outra ao fator de liquidez), elas responderão a choques de mercado distintos e serão remuneradas por prêmios de risco diferentes.

---

### Exemplo Numérico Resolvido Passo a Passo

#### Cenário Proposto
Considere um mercado em que a taxa livre de risco ($r_f$) é de $3,0\%$ ao ano. A dinâmica de precificação é governada por dois fatores sistêmicos principais ($K = 2$):
1. **Fator 1 (Crescimento Econômico):** Prêmio de risco ($\lambda_1$) = $5,0\%$
2. **Fator 2 (Liquidez de Mercado):** Prêmio de risco ($\lambda_2$) = $2,0\%$

Dois ativos ($A$ e $B$) possuem as seguintes exposições ($\beta$):
* **Ativo A:** $\beta_{A,1} = 1,2$ e $\beta_{A,2} = 0,5$
* **Ativo B:** $\beta_{B,1} = 0,4$ e $\beta_{B,2} = 1,5$

Um gestor monta um **Portfólio P** alocando $60\%$ no Ativo A e $40\%$ no Ativo B ($w_A = 0,60$; $w_B = 0,40$).

---

#### Passo 1 Calcular o excesso de retorno esperado dos ativos individuais
Utilizando a fórmula do excesso de retorno esperado $E[R_{i,ex}] = \beta_{i1}\lambda_1 + \beta_{i2}\lambda_2$:

* **Para o Ativo A:**
  $$E[R_{A,ex}] = (1,2 \times 5,0\%) + (0,5 \times 2,0\%)$$
  $$E[R_{A,ex}] = 6,0\% + 1,0\% = 7,0\%$$

* **Para o Ativo B:**
  $$E[R_{B,ex}] = (0,4 \times 5,0\%) + (1,5 \times 2,0\%)$$
  $$E[R_{B,ex}] = 2,0\% + 3,0\% = 5,0\%$$

---

#### Passo 2 Calcular o retorno esperado total dos ativos individuais
Aplicando $E[R_i] = r_f + E[R_{i,ex}]$:

* **Para o Ativo A:**
  $$E[R_A] = 3,0\% + 7,0\% = 10,0\%$$

* **Para o Ativo B:**
  $$E[R_B] = 3,0\% + 5,0\% = 8,0\%$$

---

#### Passo 3 Calcular as exposições do Portfólio P aos fatores ($\beta_{p,k}$)
Utilizando a fórmula $\beta_{p,k} = w_A \beta_{A,k} + w_B \beta_{B,k}$:

* **Exposição do Portfólio ao Fator 1 ($\beta_{p,1}$):**
  $$\beta_{p,1} = (0,60 \times 1,2) + (0,40 \times 0,4)$$
  $$\beta_{p,1} = 0,72 + 0,16 = 0,88$$

* **Exposição do Portfólio ao Fator 2 ($\beta_{p,2}$):**
  $$\beta_{p,2} = (0,60 \times 0,5) + (0,40 \times 1,5)$$
  $$\beta_{p,2} = 0,30 + 0,60 = 0,90$$

---

#### Passo 4 Calcular o excesso de retorno e o retorno total esperado do Portfólio P
* **Excesso de retorno do Portfólio ($E[R_{p,ex}]$):**
  $$E[R_{p,ex}] = \beta_{p,1}\lambda_1 + \beta_{p,2}\lambda_2$$
  $$E[R_{p,ex}] = (0,88 \times 5,0\%) + (0,90 \times 2,0\%)$$
  $$E[R_{p,ex}] = 4,4\% + 1,8\% = 6,2\%$$

* **Verificação via Média Ponderada dos Excessos Individuais:**
  $$E[R_{p,ex}] = (0,60 \times 7,0\%) + (0,40 \times 5,0\%) = 4,2\% + 2,0\% = 6,2\%$$

* **Retorno Total Esperado do Portfólio ($E[R_p]$):**
  $$E[R_p] = r_f + E[R_{p,ex}] = 3,0\% + 6,2\% = 9,2\%$$

---

### Armadilhas Comuns

1. **Confundir Alpha com Habilidade do Gestor:** Assumir que um intercepto positivo em uma regressão unifatorial seja prova de ineficiência de mercado ou genialidade do gestor, quando na verdade pode ser apenas o efeito de um fator omitido.
2. **Decoração Estatística (*Factor Zoo*):** Incluir variáveis arbitrárias ou "da moda" sem fundamentação econômica/estrutural. Um fator válido deve representar uma restrição compartilhada que transmite choques através de múltiplos ativos.
3. **Avaliar Riscos Apenas pela Variância Bruta:** Supor que ativos com volatilidades idênticas possuem o mesmo perfil de risco, ignorando que a composição de suas sensibilidades ($\beta_k$) pode expô-los a choques completamente distintos.
4. **Negligenciar as Restrições do Resíduo:** Tratar o termo $\epsilon_i$ como um ruído qualquer, ignorando a verificação de $Cov(\epsilon_i, F_k) = 0$. Se o erro for correlacionado com alguma variável do sistema, a especificação do modelo está incorreta.

---

### Laboratório Prático em Python (Roteiro Guiado)

Abaixo está estruturado o procedimento para implementação e teste de um modelo multifatorial APT em ambiente Python:

#### Passo 1 Coleta e Pré-processamento de Dados
* Importar bibliotecas analíticas (`pandas`, `numpy`, `statsmodels`).
* Obter séries históricas temporais de retornos de um conjunto de ativos ($R_i$), da taxa livre de risco ($r_f$) e de fatores de risco macroeconômicos/estilo ($F_1, F_2, \ldots, F_K$).
* Calcular as séries de excesso de retorno: $R_{i,ex} = R_i - r_f$.

#### Passo 2 Estimação das Cargas de Fator ($\beta$) via Regressão Múltipla
* Para cada ativo $i$, ajustar uma regressão linear múltipla por Mínimos Quadrados Ordinários (OLS):
  $$R_{i,ex,t} = \alpha_i + \beta_{i1} F_{1,t} + \beta_{i2} F_{2,t} + \dots + \beta_{iK} F_{K,t} + \epsilon_{i,t}$$
* Extrair os coeficientes $\beta_{ik}$ e o intercepto $\alpha_i$.

#### Passo 3 Verificação Diagnóstica dos Resíduos
* Verificar se a média dos resíduos $E[\epsilon_i]$ aproxima-se de zero.
* Calcular a matriz de correlação/covariância entre os resíduos obtidos ($\epsilon_i$) e os fatores de risco ($F_k$) para confirmar a premissa $Cov(\epsilon_i, F_k) \approx 0$.

#### Passo 4 Estimação dos Prêmios de Risco do Fator ($\lambda_k$)
* Realizar uma regressão em corte transversal (*cross-sectional regression*) utilizando os retornos médios dos ativos contra as cargas de fator ($\beta_{ik}$) estimadas no Passo 2:
  $$\bar{R}_{i,ex} = \beta_{i1}\lambda_1 + \beta_{i2}\lambda_2 + \dots + \beta_{iK}\lambda_K + \eta_i$$
* Obter os valores dos prêmios de risco $\lambda_k$.

#### Passo 5 Análise da Redução do Alpha
* Comparar o $\alpha$ obtido em um modelo de fator único (ex.: CAPM) contra o $\alpha$ remanescente após a inclusão da estrutura multifatorial.
* Avaliar a redução estatística do intercepto ao expandir a base de fatores.

---

### Glossário de Termos Importantes

* **APT (Arbitrage Pricing Theory):** Teoria de precificação de ativos baseada na lei do preço único e na ausência de arbitragem, que estabelece que o retorno esperado de um ativo é uma função linear de sua exposição a vários fatores de risco sistêmico.
* **CAPM (Capital Asset Pricing Model):** Modelo de precificação de ativos de fator único que utiliza apenas o portfólio de mercado para explicar o retorno esperado dos ativos.
* **Alpha ($\alpha$):** Retorno excedente de um ativo em relação ao previsto por um modelo de precificação. No APT, o alpha é visto como um resíduo condicional à especificação do modelo.
* **Beta ($\beta$):** Medida de sensibilidade ou carga de exposição da taxa de retorno de um ativo em relação às variações de um fator de risco comum.
* **Prêmio de Risco do Fator ($\lambda_k$):** Retorno em excesso esperado exigido pelo mercado por unidade de exposição ao fator $k$.
* **Risco Idiossincrásico ($\epsilon_i$):** Risco específico de uma empresa ou ativo individual que pode ser completamente eliminado através da diversificação em uma carteira ampla.
* **Risco Sistêmico:** Risco associado a forças macroeconômicas ou de mercado comuns que afetam múltiplos ativos simultaneamente e não pode ser diversificado.
* **Geometria de Exposição:** Assinatura multifatorial formada pelo conjunto de coeficientes $\beta_i = (\beta_{i1}, \ldots, \beta_{iK})$ de um ativo ou carteira.

---

### Questões de Prática e Autoavaliação

#### Nível 1 Resposta Curta (Conceitual)

##### Questão 1
Qual é a principal diferença conceitual entre o CAPM e o APT no que diz respeito às fontes de risco sistêmico?

**Resposta:**
O CAPM assume que existe apenas uma única fonte de risco sistêmico representada pelo portfólio de mercado. O APT assume que o sistema financeiro é movido por múltiplas forças ou restrições comuns (fatores multifatoriais), sendo o CAPM um caso particular do APT.

---

##### Questão 2
O que significa a condição de que a covariância entre o resíduo e os fatores deve ser nula ($Cov(\epsilon_i, F_k) = 0$)?

**Resposta:**
Significa que o termo de erro não contém qualquer informação ou força comum omitida pelo modelo. Se a covariância fosse diferente de zero, o resíduo estaria mascarando um fator sistêmico mal especificado.

---

##### Questão 3
Como o APT interpreta a existência de um *alpha* positivo persistente em um modelo CAPM unifatorial?

**Resposta:**
O APT interpreta esse *alpha* não como uma prova direta de ineficiência de mercado ou arbitragem, mas sim como um sintoma de um modelo mal especificado que omitiu fatores comuns de risco.

---

#### Nível 2 Média Complexidade (Cálculo e Análise)

##### Questão 4
Considere um ativo $Z$ em um modelo APT de dois fatores com $r_f = 4\%$. O Fator 1 possui prêmio de risco $\lambda_1 = 6\%$ e o Fator 2 possui prêmio de risco $\lambda_2 = 3\%$. Se o ativo $Z$ possui $\beta_{Z,1} = 0,8$ e $\beta_{Z,2} = 1,2$, qual é o retorno esperado total $E[R_Z]$ deste ativo?

**Resposta:**
1. Cálculo do excesso de retorno esperado:
   $$E[R_{Z,ex}] = \beta_{Z,1}\lambda_1 + \beta_{Z,2}\lambda_2$$
   $$E[R_{Z,ex}] = (0,8 \times 6\%) + (1,2 \times 3\%) = 4,8\% + 3,6\% = 8,4\%$$
2. Cálculo do retorno esperado total:
   $$E[R_Z] = r_f + E[R_{Z,ex}] = 4\% + 8,4\% = 12,4\%$$

---

##### Questão 5
Um gestor possui uma carteira montada com dois ativos, $X$ e $Y$, com pesos de $50\%$ cada. As cargas de fator são: $\beta_{X,1} = 1,5$, $\beta_{Y,1} = 0,5$. Sabendo que o prêmio do fator 1 é $\lambda_1 = 4\%$ e a taxa livre de risco é $2\%$, determine a carga do fator 1 para a carteira e sua contribuição para o retorno em excesso.

**Resposta:**
1. Carga do fator 1 na carteira ($\beta_{p,1}$):
   $$\beta_{p,1} = (0,50 \times 1,5) + (0,50 \times 0,5) = 0,75 + 0,25 = 1,0$$
2. Contribuição do fator 1 para o excesso de retorno:
   $$E[R_{p,ex1}] = \beta_{p,1} \times \lambda_1 = 1,0 \times 4\% = 4,0\%$$

---

#### Nível 3 Questões Dissertativas e De Aprofundamento

##### Questão 6
Explique a frase "Alpha é sempre um resíduo condicional a uma estrutura de modelo" no contexto da evolução dos modelos de precificação de ativos e do APT.

**Resposta:**
A frase destaca que a medição do desempenho "anormal" ($\alpha$) não ocorre em um vácuo absoluto, mas é dependente dos fatores de risco explicitamente considerados no modelo de referência. No CAPM unifatorial, qualquer retorno excedente não explicado pelo mercado geral é categorizado como $\alpha$. No entanto, quando o espaço de fatores é expandido via APT (incluindo dimensões como valor, *momentum*, liquidez, qualidade ou *carry*), os ganhos que antes eram atribuídos ao $\alpha$ passam a ser mapeados como remuneração por exposições a esses novos fatores ($\beta$). Assim, o que parecia ser uma anomalia de precificação ou habilidade do gestor revela-se como exposição sistêmica a forças de risco compartilhadas no mercado.

---

##### Questão 7
Por que a presença de resíduos não diversificáveis e correlacionados entre ativos violaria a condição de ausência de arbitragem no APT?

**Resposta:**
O APT baseia-se no princípio de que o retorno em excesso esperado deve compensar apenas o risco sistêmico que não pode ser diversificado. Se os resíduos ($\epsilon_i$) contiverem componentes correlacionados entre si ou não diversificáveis, um investidor não conseguiria construir uma carteira de arbitrage que zerasse o risco idiossincrásico total mantendo retorno positivo. Caso existissem retornos não explicados pelos fatores em carteiras totalmente diversificadas, surgiria uma oportunidade de arbitragem perfeita (ganho sem risco e sem custo). Para evitar a existência de tais oportunidades em equilíbrio, o retorno esperado deve ser rigorosamente uma função linear das exposições aos fatores sistêmicos comuns que não podem ser eliminados pela diversificação.