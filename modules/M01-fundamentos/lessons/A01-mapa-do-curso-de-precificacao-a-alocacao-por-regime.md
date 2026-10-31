<!-- imported from vault study notes; curated for open course -->
# M01.A01 — Mapa do curso: de precificação a alocação por regime

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M01
> **Aula:** M01.A01

↑ M01 · Resumo · Completo

**Módulo:** M01
**Pergunta do módulo:** Como precificar e fazer hedge de opções vanila sem “adivinhar” o drift?

## Conceito-núcleo
Visão do pipeline FE → econofísica → labs de beta/regime/Janus; o que cada bloco muda na decisão de trading.

## Aplicação em mercado / trading
Definir objetivo de estudo (trader, quant ou risco) e priorizar módulos conforme a pergunta de mercado.

## Entregável / lab
Checklist pessoal: pergunta de mercado + path sugerido + repos a clonar.

## Fonte (mapeamento)
quantitative-trading-free-lesson/01 intro | IG pinned free-lesson

## Guia de estudo aprofundado

> **info**
>

Este guia de estudo foi elaborado com base nas pesquisas de Karim Khemiri (sociedade de P&D em finanças Khem Kapital) para fornecer uma compreensão rigorosa e estruturada sobre a natureza dos ativos financeiros, a mecânica das opções, o papel do *hedge* e a necessidade de modelagem estocástica do preço dos ativos.

---

### Conceitos-Chave

#### Categorização dos Ativos de Mercado
Em qualquer mercado financeiro, existem apenas duas categorias de itens que podem ser comprados ou vendidos:
1. **Reivindicações de Propriedade (*Property Claims / Equity / Ownership*)**: Títulos que representam a posse de um bem ou de uma empresa.
2. **Compromissos Contratuais (*Contractual Commitments*)**: Instrumentos financeiros baseados em acordos e obrigações futuras, tais como títulos de dívida (*bonds*), contratos futuros (*futures*), operações de recompra (*repos*), *swaps* e opções (*options*).

#### Definição e Função Estrutural de uma Opção
Uma opção é um compromisso contratual que concede ao comprador o direito (mas não a obrigação) de adquirir um ativo ou uma reivindicação de propriedade em uma data determinada e a um preço fixado com antecedência.

*   **Comprador da Opção**: Paga um valor chamado **prêmio** (*premium*) para transferir um risco ao qual está exposto (como uma alta acentuada ou uma queda expressiva nos preços do ativo) para a contraparte.
*   **Vendedor da Opção**: Recebe o prêmio no presente, mas concorda em carregar o risco de *payoff* (pagamento futuro) no vencimento.

#### O Mito da Alavancagem vs. Transferência Estruturada de Risco
Definir opções puramente como uma "ferramenta de alavancagem" é uma visão errônea. Embora as opções possam oferecer exposição não linear com um aporte de caixa inicial limitado, a verdadeira essência do produto é a **transferência estruturada de um risco condicional**. 

#### A Necessidade Impositiva do Hedge
O vendedor de uma opção recebe o prêmio no momento da transação, mas assume a responsabilidade do *payoff* futuro. Como é impossível prever onde o preço do ativo estará no vencimento, o vendedor não pode se dar ao luxo de "esperar para ver" (*wait and see*), sob pena de enfrentar perdas massivas em cenários de mercado desfavoráveis. 

Portanto, um vendedor sério de opções deve construir um **hedge** (uma estrutura de proteção) que reduza progressivamente o seu risco à medida que o mercado se movimenta, em vez de realizar apostas na direção do preço.

#### Modelagem Dinâmica com Movimento Browniano Geométrico
Para construir essa proteção dinâmica, é indispensável utilizar um modelo mínimo do movimento dos preços que traduza a premissa "o mercado se move aleatoriamente" em uma estrutura matemática computável. Utiliza-se o **Movimento Browniano Geométrico** (*Geometric Brownian Motion*) para descrever a evolução temporal do preço do ativo $(S_t)$ e derivar a sua distribuição de probabilidade (lei estocástica). É essa distribuição que permite quantificar e operacionalizar os conceitos de preço, prêmio e *hedge*.

---

### Intuição de Mercado e Trading

No contexto prático de negociação, a transação de uma opção não é uma simples aposta de alta ou queda, mas uma negociação sobre a incerteza e a assimetria:

*   **A Posição do Comprador**: O comprador identifica um risco no seu portfólio (por exemplo, a desvalorização de uma ação que ele possui ou a alta do preço de um insumo que precisa comprar) e utiliza o mercado de opções para estipular um teto para suas perdas ou fixar um preço futuro. O prêmio pago é o custo exato dessa transferência de risco.
*   **A Posição do Vendedor**: O vendedor atua de forma análoga a uma seguradora. Ele não deve atuar como um investidor direcional que torce para que o mercado vá a seu favor. Como o resultado futuro de $(S_t)$ é incerto, a gestão do vendedor exige reajustes contínuos da posição de proteção (*hedge*). O lucro do vendedor provém da gestão eficiente do prêmio recebido em relação aos custos de manutenção dessa cobertura contra variações aleatórias do mercado.

---

### Formulação Matemática e Exemplo Numérico Resolvido

#### Formulação Matemática

1. **Dinâmica do Preço do Ativo**:
   O preço do ativo subjacente em um instante $t$, denotado por $S_t$, é modelado por um Movimento Browniano Geométrico:
   $$dS_t = \mu S_t dt + \sigma S_t dW_t$$
   Onde $S_t$ representa o preço do ativo, $\mu$ é a taxa de deriva (*drift*), $\sigma$ é a volatilidade e $dW_t$ é o incremento de um processo de Wiener (Movimento Browniano).

2. **Payoff Condicional no Vencimento $T$**:
   Para um contrato de opção com preço de exercício fixado em $K$ e vencimento na data $T$:
   $$\text{Payoff do Comprador} = \max(S_T - K, 0)$$
   $$\text{Resultado do Vendedor no Vencimento} = \text{Prêmio Recebido} - \max(S_T - K, 0)$$

---

#### Exemplo Numérico Passo a Passo

Consideremos um cenário simplificado de mercado para ilustrar o risco do vendedor e a necessidade de precificação do prêmio:

##### Dados do Problema
*   Preço atual do ativo no tempo $t=0$: $S_0 = \$100$
*   Preço de exercício fixado no contrato: $K = \$100$
*   Prêmio negociado e pago pelo comprador ao vendedor hoje: $P_0 = \$5$
*   Cenário de Mercado A no vencimento $T$: $S_T = \$125$
*   Cenário de Mercado B no vencimento $T$: $S_T = \$85$

##### Passo 1 Avaliação do Fluxo de Caixa no Tempo $t=0$
*   Comprador desbensa: $-\$5$ (paga o prêmio).
*   Vendedor arrecada: $+\$5$ (pockets the premium).

##### Passo 2 Avaliação do Cenário A no Vencimento ($S_T = \$125$)
*   **Decisão do Comprador**: Como $S_T (\$125) > K (\$100)$, o comprador exerce o direito de adquirir o ativo por $\$100$.
*   **Payoff do Contrato**:
    $$\text{Payoff} = \max(125 - 100, 0) = \$25$$
*   **Resultado do Comprador**:
    $$\text{Lucro Líquido} = \text{Payoff} - P_0 = \$25 - \$5 = \$20$$
*   **Resultado do Vendedor Sem Hedge**:
    $$\text{Resultado Líquido} = P_0 - \text{Payoff} = \$5 - \$25 = -\$20$$
    *Conclusão no Cenário A*: O vendedor sofreu uma perda significativa por não ter realizado o *hedge* das variações de $S_t$.

##### Passo 3 Avaliação do Cenário B no Vencimento ($S_T = \$85$)
*   **Decisão do Comprador**: Como $S_T (\$85) < K (\$100)$, o comprador não exerce o contrato.
*   **Payoff do Contrato**:
    $$\text{Payoff} = \max(85 - 100, 0) = \$0$$
*   **Resultado do Comprador**: Perda limitada ao prêmio pago ($-\$5$).
*   **Resultado do Vendedor**: Retém o prêmio integral ($+\$5$).

##### Passo 4 Conclusão da Necessidade de Hedge
Se o vendedor adotar a postura "esperar para ver" (*wait and see*), o Cenário A demonstra que a perda pode superar em muitas vezes o prêmio recebido ($-\$20$ vs $+\$5$). Para evitar esse risco caótico, o vendedor utiliza a lei de distribuição derivada do Movimento Browniano Geométrico para manter uma posição de proteção contínua durante a vida do contrato.

---

### Armadilhas Comuns

*   **Confundir a Natureza do Instrumento**: Tratar opções puramente como instrumentos de alavancagem financeira, negligenciando que a sua fundação é a transferência estruturada de risco condicional.
*   **Postura "Wait and See" (Esperar para Ver)**: Acreditar que o vendedor de uma opção pode simplesmente receber o prêmio e aguardar passivamente a expiração do contrato sem realizar a gestão de risco.
*   **Confusão entre Aposta Direcional e Proteção (Hedge)**: Tentar proteger uma posição vendida em opções fazendo apostas sobre a direção do mercado, em vez de reequilibrar dinamicamente a carteira com base nas variações aleatórias de $S_t$.
*   **Ausência de Modelo Probabilístico**: Tentar precificar ou cobrir opções sem definir uma dinâmica estocástica (como o Movimento Browniano Geométrico) para derivar a distribuição probabilística do preço do ativo.

---

### Laboratório Prático em Python

Abaixo está a descrição em passos para implementar uma simulação em Python que demonstra a evolução do preço de um ativo $(S_t)$ via Movimento Browniano Geométrico e calcula a exposição de payoff sem proteção.

#### Passo 1 Configuração do Ambiente e Parâmetros
*   Importar as bibliotecas `numpy` (para geração de números aleatórios e operações matriciais) e `matplotlib.pyplot` (para visualização gráfica).
*   Definir os parâmetros da simulação:
    *   Preço inicial do ativo: `S0 = 100.0`
    *   Preço de exercício: `K = 100.0`
    *   Taxa de deriva de longo prazo: `mu = 0.05`
    *   Volatilidade anualizada: `sigma = 0.20`
    *   Tempo até a expiração em anos: `T = 1.0`
    *   Número de passos de tempo: `N = 252`
    *   Número de simulações de trajetórias: `num_simulacoes = 1000`

#### Passo 2 Construção da Dinâmica do Movimento Browniano Geométrico
*   Calcular o intervalo de tempo: `dt = T / N`.
*   Gerar uma matriz de números aleatórios com distribuição normal padrão de dimensão `(N, num_simulacoes)`.
*   Calcular as trajetórias de preço utilizando a solução discreta da equação do Movimento Browniano Geométrico:
    $$S_{t+\Delta t} = S_t \cdot \exp\left(\left(\mu - \frac{\sigma^2}{2}\right)\Delta t + \sigma \sqrt{\Delta t} \, Z_t\right)$$
    onde $Z_t \sim \mathcal{N}(0,1)$.

#### Passo 3 Cálculo do Payoff da Opção no Vencimento
*   Extrair os preços finais do ativo no tempo $T$ (`S_T = trajetorias[-1, :]`).
*   Calcular o vetor de payoffs da opção de compra no vencimento para todas as simulações: `payoffs = np.maximum(S_T - K, 0)`.

#### Passo 4 Análise da Distribuição do Vendedor sem Hedge
*   Definir um prêmio simulado fixo recebido no tempo $t=0$ (exemplo: `prêmio = 7.0`).
*   Calcular o resultado financeiro líquido do vendedor para cada trajetória simulated: `resultados_vendedor = premio - payoffs`.
*   Plotar o histograma dos resultados do vendedor para evidenciar a cauda de perdas potenciais em cenários onde $S_T \gg K$, demonstrando por que a postura *wait and see* é inviável sem a implementação de um *hedge*.

---

### Glossário

| Termo | Definição |
| :--- | :--- |
| **Reivindicação de Propriedade (*Property Claim*)** | Ativo financeiro que representa a posse ou participação direta sobre um patrimônio ou empresa (ex.: ações/equity). |
| **Compromisso Contratual (*Contractual Commitment*)** | Instrumento financeiro estruturado por meio de um contrato que define obrigações e direitos futuros entre as partes (ex.: títulos, futuros, repos, swaps e opções). |
| **Opção (*Option*)** | Contrato financeiro que confere ao comprador o direito de adquirir um ativo ou propriedade em uma data futura por um preço pré-determinado. |
| **Prêmio (*Premium*)** | Valor monetário pago pelo comprador ao vendedor para transferir a exposição a um risco condicional. |
| **Hedge (Proteção)** | Estratégia contínua de gerenciamento de risco estruturada para neutralizar ou reduzir a exposição às variações imprevisíveis de preço do ativo subjacente. |
| **Movimento Browniano Geométrico** | Modelo estocástico contínuo utilizado para descrever a evolução temporal aleatória do preço de um ativo $S_t$, permitindo derivar sua distribuição de probabilidade. |
| **Risco Condicional** | Risco financeiro cuja concretização e magnitude dependem da ocorrência de determinados cenários de preço do ativo no futuro. |
| **Estratégia *Wait and See*** | Prática de vender uma opção e aguardar passivamente a expiração do contrato sem construir uma estrutura de hedge; altamente arriscada devido às perdas potenciais ilimitadas. |

---

### Questões e Exercícios

#### Nível 1 Questões de Fixação (Resposta Curta)

**Questão 1:** Quais são as duas únicas categorias de itens que podem ser negociadas em um mercado financeiro segundo Karim Khemiri?
> **Resposta:** Reivindicações de propriedade (*property claims / equity*) e compromissos contratuais (*contractual commitments*, tais como títulos, futuros, repos, swaps e opções).

**Questão 2:** Qual é o objetivo principal do comprador ao pagar o prêmio de uma opção?
> **Resposta:** Transferir para o vendedor um risco ao qual está exposto, como uma alta ou uma queda indesejada nos preços do ativo subjacente.

**Questão 3:** Por que é incorreto afirmar que as opções são puramente "ferramentas de alavancagem"?
> **Resposta:** Porque, embora forneçam exposição não linear com aporte inicial limitado de caixa, a essência do produto é a transferência estruturada de um risco condicional entre o comprador e o vendedor.

---

#### Nível 2 Questões de Aplicação e Análise

**Questão 4:** O que impede um vendedor sério de opções de adotar a estratégia de "esperar para ver" (*wait and see*) após receber o prêmio?
> **Resposta:** Como ninguém pode prever onde o preço do ativo estará no vencimento, a ausência de um *hedge* expõe o vendedor ao risco de pagar valores extremamente elevados (*payoffs* massivos) em cenários de mercado desfavoráveis, superando de longe o prêmio recebido no início.

**Questão 5:** De que maneira o Movimento Browniano Geométrico auxilia o vendedor de opções no gerenciamento de suas posições?
> **Resposta:** O Movimento Browniano Geométrico oferece um modelo dinâmico mínimo para o preço do ativo $(S_t)$, traduzindo a movimentação aleatória do mercado em uma distribuição de probabilidade computável. É com base nessa lei que o vendedor consegue precificar o prêmio e construir uma estratégia de *hedge* adequada.

---

#### Nível 3 Questão Dissertativa para Aprofundamento

**Questão 6:** Explique a relação existente entre o pagamento do prêmio, a assimetria de risco entre comprador e vendedor, e a necessidade de modelagem estocástica do preço do ativo $(S_t)$ via Movimento Browniano Geométrico.

> **Resposta:** 
> A relação entre as partes de um contrato de opção é estruturada sobre uma assimetria financeira e temporal. No momento inicial ($t=0$), o comprador realiza o pagamento de um prêmio fixo ao vendedor. Em troca desse valor, o comprador transfere o seu risco condicional de preço, garantindo o direito de efetuar uma transação futura por um preço pré-fixado. 
>
> Por outro lado, o vendedor embolsa o prêmio no presente, mas assume integralmente o risco de arcar com o *payoff* do contrato na data de vencimento. Como a trajetória do ativo subjacente até a expiração é incerta, o vendedor fica exposto a perdas potencialmente severas se o mercado se mover em uma direção desfavorável. Para evitar uma postura passiva e perigosa de "esperar para ver", o vendedor precisa mitigar esse risco de forma contínua através da construção de um *hedge*.
>
> Para construir essa proteção sem realizar apostas direcionais, é necessário calcular como o risco evolui em função das variações do preço do ativo. É exatamente nesse ponto que se insere o Movimento Browniano Geométrico. Ao modelar $S_t$ como um processo estocástico, obtém-se a lei de distribuição de probabilidade do preço do ativo. Essa base matemática provê os fundamentos necessários para precificar o contrato de forma justa e operacionalizar o *hedge* dinâmico, transformando a aleatoriedade do mercado em uma estrutura quantificável e gerenciável.