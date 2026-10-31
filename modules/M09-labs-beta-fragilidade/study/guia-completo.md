<!-- imported study note (guia-completo.md) -->
# Guia Completo do Módulo M09: Beta Operacional, Cointegração e Classificador Frágil R− / Antifrágil R+

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M09

↑ M09 · Resumo · Completo

> **warning**
>
> No lab original de Karim Khemiri (`Fragile-Antifragile-Regime-Classifier`), **R+ = perna frágil** e **R− = perna antifrágil**. O relatório gerado pelo NotebookLM tinha invertido os rótulos; foram trocados nesta nota para seguir a fonte. A categoria "R0 (Robusto)" e a heurística $H$ de Taleb-Douady vêm das fontes da pesquisa web e não fazem parte do classificador original, que atribui só R+ ou R−.

## Executive Summary

Este documento estabelece o relatório consolidado do Módulo M09 da Khem Kapital, abordando a transição conceitual e prática do **beta de livro** (teórico/estático) para o **beta operacional** (dinâmico e sensível a não-linearidades). O módulo integra técnicas avançadas de arbitragem estatística (*pairs trading*) aplicadas a spreads de ativos e mercados de previsão com a teoria matemática rigorosa da **(anti)fragilidade** desenvolvida por Nassim Nicholas Taleb e Raphaël Douady.

A análise demonstra que os modelos tradicionais de gestão de risco e *stress testing* falham ao focar em estimativas pontuais de primeira ordem. Essas abordagens ignoram o erro de modelo, a estocasticidade dos parâmetros e as assimetrias côncavas nas caudas das distribuições. Por meio da introdução de uma heurística determinística livre de modelo e livre de probabilidade, quantifica-se a sensibilidade de segundo ordem (convexidade/concavidade em relação a estressores ou "vega de cauda"). Esta metodologia viabiliza a construção de um classificador operacional capaz de segregar ativos e estratégias em regimes **R− (Antifrágil)**, **R0 (Robusto)** e **R+ (Frágil)**, eliminando riscos ocultos de cauda antes da execução no mercado.

---

## 1 Por que Beta Operacional e não Beta de Livro

O **beta de livro** (proveniente do modelo CAPM e de regressões lineares clássicas de finanças) baseia-se na premissa de que a relação entre um ativo e um índice (ou entre dois ativos correlacionados) é linear, simétrica e estacionária ao longo do tempo. Assume-se que a variância dos resíduos é constante e que os riscos de mercado podem ser totalmente capturados pela covariância histórica dividida pela variância do mercado.

Entretanto, nos mercados reais, o beta teórico desmorona devido a três falhas fundamentais:
1. **Não-linearidade de Impacto de Mercado**: A liquidação ou montagem de posições sob estresse gera custos desproporcionais ao tamanho da ordem (*fire sales*). Um exemplo empírico notável ocorreu no banco Société Générale em janeiro de 2008, onde a necessidade de liquidar aproximadamente US$ 70 bilhões em futuros de índices de ações ao longo de apenas três dias (após a descoberta de posições não autorizadas) forçou o mercado a realizar perdas brutas extraordinárias de EUR 6,4 bilhões. Se essa mesma posição tivesse sido dividida em dez vendas gradativas de US$ 7 bilhões ao longo de semanas, o impacto sobre os preços e as perdas finais seriam drasticamente menores. O beta de livro trata dez ordens de US$ 7 bilhões como identicamente proporcionais a uma ordem de US$ 70 bilhões, ignorando a concavidade da função de dano.
2. **Instabilidade de Parâmetros e Erro de Modelo**: Parâmetros como volatilidade e correlação não são fixos, mas variáveis estocásticas com distribuições próprias. Projetar retornos ou riscos assumindo parâmetros constantes resulta no viés de convexidade (decorrente da Desigualdade de Jensen), subestimando perdas de cauda.
3. **Assimetria das Reações em Regimes Extremosa**: A resposta de um spread ou de uma carteira a choques de mercado não é simétrica. Em momentos de pânico, liquidez e correlações convergem para 1 na ponta vendedora, invalidando o beta estático calculado em períodos de tranquilidade.

O **beta operacional** substitui a premissa de linearidade estática pela medição dinâmica da sensibilidade do spread aos choques do ambiente de trading. Ele incorpora as fricções operacionais, a não-estacionariedade dos resíduos e a sensibilidade do sistema às variações do estressor de mercado.

---

## 2 Construção de Spreads Beta, Estacionariedade e Cointegração

A construção de estratégias de neutralidade de mercado via *pairs trading* estende-se de mercados tradicionais de ações e commodities até mercados de apostas e previsões políticas (como as eleições presidenciais americanas de 2020 e 2024).

### Inversão de Odds e Probabilidades Implícitas Combinadas
Em mercados de apostas peer-to-peer (P2P) ou exchanges de trading, as cotações decimais de dois candidatos majoritários (ex: Democrata e Republicano) são invertidas para obter as probabilidades implícitas de vitória.
Para odds decimais $O_A$ e $O_B$, as probabilidades implícitas $p_A$ e $p_B$ são:

$$p_A = \frac{1}{O_A}, \quad p_B = \frac{1}{O_B}$$

Em um mercado sem fricção e perfeitamente eficiente, a probabilidade combinada $S_t = p_A + p_B$ se somaria a $1,0$. Em mercados reais, $S_t$ oscila devido ao *over-round* ou à alocação provisória de probabilidade a terceiros candidatos.

### O Processo Ornstein-Uhlenbeck de Tendência com Ruído
Para modelar a dinamica de reversão à média do spread $S_t$, adota-se um processo estocástico de Ornstein-Uhlenbeck (OU) latente com nível de reversão variável no tempo e ruído branco aditivo nas observações:

$$dX_t = \theta (\mu(t) - X_t) dt + \sigma dW_t$$

$$Y_t = X_t + \epsilon_t, \quad \epsilon_t \sim \mathcal{N}(0, \sigma_\epsilon^2)$$

Onde:
* $X_t$ é o estado latente e contínuo da probabilidade combinada (ou spread beta).
* $\theta > 0$ representa a taxa de reversão à média.
* $\mu(t)$ é o nível de equilíbrio de longo prazo, ajustável ao longo do tempo para capturar tendências estruturais.
* $\sigma$ é a volatilidade do processo latente.
* $dW_t$ é o movimento Browniano padrão.
* $Y_t$ é o valor efetivamente observado do spread no tempo discreto $t$, corrompido pelo ruído de amostragem ou de microestrutura de mercado $\epsilon_t$.

### Estimação de Parâmetros e Testes de Estacionariedade
A estimação dos parâmetros $(\theta, \mu(t), \sigma, \sigma_\epsilon^2)$ a partir de dados amostrados regularmente ocorre via formulação de espaço-estado combinada com o **Filtro de Kalman**. Quando ocorrem cotações repetidas consecutivas, condensa-se a observação retida e preserva-se o intervalo de tempo transcorrido no operador de transição contínua, garantindo a cointegração e a avaliação consistente da estacionariedade dos resíduos do spread.

---

## 3 Seleção pelo Ambiente de Trading, Gates, Quadrantes e Estados

A execução operacional do modelo requer uma estrutura determinística de tomada de decisão para determinar *quando* operar e *qual* ponta assumir.

### Estrutura de Decisão Operacional
1. **Gate 1: Identificação do Sinal (Geração do *Trigger*)**:
   Utilizam-se limites de predição superiores obtidos via *bootstrap paramétrico* sobre o processo OU estimado. Quando a probabilidade combinada observada $Y_t$ excede o limite superior de predição em um passo adiante, é identificado um sinal de que o spread combinado está temporariamente inflacionado e tende a sofrer declínio (reversão à média).
2. **Gate 2: Seleção do Ativo/Candidato (Modelo Bradley-Terry)**:
   Uma vez disparado o sinal de que o spread combinado declinará, determina-se qual cotação individual está desalinhada utilizando um modelo do tipo Bradley-Terry antissimétrico sem intercepto. O modelo compara as forças relativas das odds dos dois candidatos e seleciona a cotação específica que apresenta o maior desvio em relação ao seu valor teórico ajustado.
3. **Mapeamento por Estados Operacionais**:
   * **Estado 0 (Neutro/Aguardando)**: O spread permanece dentro das bandas de predição do bootstrap paramétrico.
   * **Estado 1 (Sinal de Entrada / Venda do Spread)**: O spread rompe o limite superior de predição. Executa-se a venda da probabilidade sobressalente (ou posição *short* no ativo superavaliado do par) e a compra do ativo subavaliado.
   * **Estado 2 (Reversão / Fechamento de Posição)**: O spread retorna ao intervalo de confiança do processo OU ($\mu(t)$), realizando a convergência.

---

## 4 Custos, Placebo e Robustez

Para validar a sustentabilidade do beta operacional, é obrigatório isolar lucros teóricos ilusórios de retornos executáveis em ambiente real.

### Retornos Sintéticos sem Fricção vs. Lucro Executável Real
Em mercados de apostas e pares de commodities/ações, as métricas de desempenho puramente sintéticas ignoram o *bid-ask spread*, taxas de corretagem, impostos, custos de empréstimo (*borrowing fees*) e restrições de liquidez na ponta oposta (*lay/back*). 

Nos testes do modelo eleitoral de 2024, a aplicação da estratégia gerou:
* **Sinais gerados**: 130 sinais out-of-sample.
* **Cobertura empírica de um passo**: 95,1%.
* **Retorno médio sintético das odds**: 1,86%.
* **Índice de Sharpe por trade (não anualizado)**: 1,12.

*Nota de Alinhamento Factual*: Esses valores são **quantidades descritivas sintéticas e sem fricção**, e não lucros líquidos de arbitragem executáveis em uma exchange real.

### Testes Placebo e Validação Fora da Amostra (Out-of-Sample)
A robustez do pipeline é avaliada através de duas etapas:
1. **Treinamento e Validação Temporal**: Treina-se o modelo no conjunto de dados histórico (ex: Eleição de 2020) e avalia-se o desempenho estritamente fora da amostra no conjunto de teste (ex: Eleição de 2024).
2. **Testes Placebo**: Aplica-se o modelo a séries temporais onde a relação de cointegração é propositadamente destruída (por meio do embaralhamento temporal dos resíduos). Se a estratégia continuar gerando "sinais lucrativos" em dados placebo, a lógica de entrada é invalidadas por *overfitting*.

---

## 5 Fragilidade e Antifragilidade: Convexidade de Taleb

A definição matemática universal de fragilidade e antifragilidade, desenvolvida por Taleb & Douady (2012), dispensa preferências psicológicas subjetivas (teoria da utilidade) e aplica-se a qualquer objeto ou sistema que possua uma distribuição de probabilidade.

### Definição Matemática de Vega de Cauda
Seja $X$ uma variável aleatória com função de densidade de probabilidade $f_\lambda$ dependente de um parâmetro $\lambda$. Considera-se uma referência constante $\Omega$ e o desvio semi-absoluto à esquerda $s^-$:

$$s^-(\lambda) = \int_{-\infty}^{\Omega} (\Omega - x) f_\lambda(x) dx$$

Define-se a expectativa incondicional de queda abaixo do nível de estresse $K < \Omega$ como $\xi(K, s^-)$. A **sensibilidade vega de cauda à esquerda** $V$ (ou fragilidade intrínseca) é a derivada parcial de $\xi$ em relação ao desvio semi-absoluto $s^-$:

$$V(X, f_\lambda, K, s^-) = \frac{\partial \xi(K, s^-)}{\partial s^-}$$

Na versão por diferenças finitas para um desvio $\Delta s$:

$$V(X, f_\lambda, K, s^-, \Delta s) = \frac{\xi(K, s^- + \Delta s) - \xi(K, s^- - \Delta s)}{2 \Delta s}$$

### A Função de Dano e a Não-Linearidade
Um sistema é frágil quando sua função de dano $\Pi(z)$ em relação ao estressor $z$ é estritamente côncava. Para um fator multiplicativo $n > 1$:

$$\Pi(n z) < n \, \Pi(z)$$

Isso significa que o dano sofrido por um choque de grande magnitude é desproporcionalmente maior do que o efeito acumulado de $n$ pequenos choques de intensidade $z$. Como consequência direta da concavidade, a segunda derivada da resposta é negativa ($\Pi''(z) < 0$).

### Viés de Convexidade e a Desigualdade de Jensen
Quando um parâmetro ou estressor é tratado como constante determinística quando na verdade é estocástico, a Desigualdade de Jensen gera um viés sistemático nas estimativas do modelo. Se $g(x)$ é uma função côncava em relação ao estressor $x$, então:

$$\mathbb{E}[g(x)] < g(\mathbb{E}[x])$$

### Exemplo Numérico Concreto I: Déficit Orçamentário e Desemprego
Considere um governo que projeta a taxa de desemprego média nos próximos três anos em $9\%$, prevendo um déficit orçamentário $B$ de $200$ bilhões na moeda local. No entanto, o desemprego é uma variável estocástica que flutua em média $1\%$ (desvio médio $\Delta = 1\%$).

A relação entre o desemprego e o déficit é não-linear e côncava no domínio de saldo orçamentário:
* **Desemprego em 8%**: Déficit $B(8\%) = -75\text{ bilhões}$ (melhoria de $125\text{ bilhões}$).
* **Desemprego em 9% (Ponto Estimado)**: Déficit $B(9\%) = -200\text{ bilhões}$.
* **Desemprego em 10%**: Déficit $B(10\%) = -550\text{ bilhões}$ (piora de $350\text{ bilhões}$).

Cálculo do Viés de Convexidade ($\omega_A$):
Se integrarmos a incerteza do desemprego entre os dois cenários ($8\%$ e $10\%$):

$$\mathbb{E}[B] = \frac{B(8\%) + B(10\%)}{2} = \frac{-75 + (-550)}{2} = \frac{-625}{2} = -312,5\text{ bilhões}$$

O **viés de convexidade** resultante de ter ignorado a estocasticidade do desemprego é de:

$$\omega_A = -312,5 - (-200) = -112,5\text{ bilhões}$$

A estimativa pontual tradicional ($-200\text{ bilhões}$) subestima o déficit esperado real em $112,5\text{ bilhões}$ devido à concavidade oculta da resposta orçamentária ao desemprego.

### Exemplo Numérico Concreto II: Estrutura da Dívida Pública
Aplica-se a dinâmica da dívida pública sobre o PIB ($d_t$) em resposta a choques no crescimento econômico $g_t$:

$$d_t = \left(\frac{1 + r_t}{1 + g_t}\right) d_{t-1} - pb_t$$

Estudo empírico do FMI (Taleb et al., 2012) avaliou o impacto do estresse no crescimento de PIB para diversos países (designados de A a G) ao longo de 2012-2016:
* **País A**:
  * Choque Central de Crescimento ($2\%\text{ a menos que o cenário base}$): Aumento da Dívida/PIB em $+26,2\text{ ppts}$.
  * Choque de $+1\text{ MDev}$ ($+1,5\text{ ppts}$ de crescimento): Mudança na Dívida/PIB = $-13,5\text{ ppts}$.
  * Choque de $-1\text{ MDev}$ ($-1,5\text{ ppts}$ de crescimento): Mudança na Dívida/PIB = $+14,0\text{ ppts}$.

Cálculo da Heurística de Fragilidade $H$ para a Dívida do País A:

$$H(+/- 1\text{ MDev}) = \frac{14,0 + (-13,5)}{2} = \frac{0,5}{2} = +0,25 \approx +0,3\text{ ppts do PIB}$$

Como na análise de dívida pública um número positivo maior representa o cenário adverso (aumento da dívida), $H > 0$ indica que o resultado é **frágil**: os danos gerados por um choque de crescimento negativo adicional superam os benefícios obtidos por um choque positivo de igual magnitude. Para o caso de choque de $+/- 2\text{ MDev}$, $H$ sobe para $+1,1\text{ ppts}$ (e no País G atinge $+8,5\text{ ppts}$ do PIB), confirmando a expansão da fragilidade nas caudas distantes.

---

## 6 Classificador Determinístico R+ vs R-, Métricas e Pipeline

Para operacionalizar esses conceitos, define-se a **Heurística de Fragilidade $H$** como um escalar direto obtido por perturbação simétrica de primeira e segunda ordem ao redor da resposta de um teste de estresse central $\alpha$:

$$H = \frac{f(\alpha - \Delta) + f(\alpha + \Delta)}{2} - f(\alpha)$$

Onde $f(\alpha)$ representa a métrica de desempenho, capital de ativos, ou dívida decorrente do valor de estresse central $\alpha$, e $\Delta$ representa uma variação correspondente ao desvio absoluto médio do estressor.

### Classificação de Regimes Operacionais
A interpretação da Heurística $H$ depende da natureza do parâmetro de saída (se o resultado medido é um retorno/capitalização ou uma perda/dívida):

1. **Regime R− (Antifrágil)**:
   * Em Métricas de Retorno/Capitalização: $H > 0$ de forma significativa em relação ao capital. Aumentos de volatilidade produzem ganhos desproporcionalmente maiores do que as perdas associadas a choques contrários.
   * Em Métricas de Custo/Perda/Dívida: $H < 0$. O impacto desfavorável de choques negativos adicionais atenua-se nas caudas.
2. **Regime R0 (Robusto)**:
   * $H \approx 0$ em relação ao capital total. A resposta do sistema ao estressor é puramente linear. Aumentos na volatilidade não afetam a expectativa do resultado final.
3. **Regime R+ (Frágil)**:
   * Em Métricas de Retorno/Capitalização: $H < 0$ de forma expressiva. As perdas derivadas de um choque desfavorável adicional ($\alpha - \Delta$) são muito maiores do que os ganhos obtidos com um choque favorável ($\alpha + \Delta$).
   * Em Métricas de Custo/Perda/Dívida: $H > 0$. Pequenas piores na variável de estresse causam uma explosão desproporcional no passivo ou na dívida.

### Taxonomia Completa de Payoffs
A tabela abaixo sintetiza a taxonomia exaustiva dos payoffs $y = f(x)$ proposta por Taleb & Douady (2012):

| Categoria | Cauda Esquerda (Perda) | Cauda Direita (Ganho) | Payoff Não-Linear $y = f(x)$ | Sensibilidade Equivalente em Opções | Efeito da Cauda Gorda em $f(x)$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tipo 1: Frágil (Misto)** | Gorda (Barreira de Absorção) | Gorda | Misto côncavo à esquerda, convexo à direita | *Long vega* na alta, *short vega* na baixa | Aumenta a fragilidade na barreira |
| **Tipo 2: Frágil (Puro)** | Gorda | Fina | Côncavo puro | *Short vega* global | Aumenta drasticamente a fragilidade |
| **Tipo 3: Robusto** | Fina | Fina | Misto convexo à esquerda, côncavo à direita (Sigmóide/Digital) | *Short down vega*, *long up vega* | Sem efeito significativo |
| **Tipo 4: Antifrágil** | Fina | Gorda | Convexo puro | *Long vega* global | Aumenta a antifragilidade |

### Pipeline do Classificador Determinístico
1. **Passo 1 (Entrada de Dados)**: Obter o valor de saída base do sistema sob o estresse de referência $f(\alpha)$ (ex: Capitalização bancária Tier 1, valor do spread, ou razão dívida/PIB).
2. **Passo 2 (Perturbação Simétrica)**: Calcular o desvio médio $\Delta$ do parâmetro estressor. Executar duas simulações adicionais alterando o estressor para $(\alpha - \Delta)$ e $(\alpha + \Delta)$.
3. **Passo 3 (Cálculo do Escalar H)**: Aplicar $H = \frac{f(\alpha - \Delta) + f(\alpha + \Delta)}{2} - f(\alpha)$.
4. **Passo 4 (Classificação de Regime)**:
   * Se $H < -\text{threshold}$ (para métricas de capital): Rotular ativo/estratégia como **R+ (Frágil)** $\rightarrow$ **Bloqueio de Execução**.
   * Se $-\text{threshold} \le H \le \text{threshold}$: Rotular como **R0 (Robusto)** $\rightarrow$ **Liberação sem Alavancagem**.
   * Se $H > \text{threshold}$ (para métricas de capital): Rotular como **R− (Antifrágil)** $\rightarrow$ **Liberação para Execução Operacional**.

---

## 7 Resultados, Limitações e Reprodutibilidade dos Labs

### Análise do Estresse Bancário (Estudo de Caso FMI / 12 Bancos dos EUA)
O teste de estresse macroeconômico aplicado a 12 grandes bancos comerciais americanos (Taleb et al., 2012) projetou a trajetória do índice de capitalização Tier 1 sob um cenário de crescimento do PIB próximo de zero (desvio acumulado de $10\text{ ppts}$ do PIB durante 2012-2016). A heurística $H$ foi calculada para choques adicionais de $+/- 1$ e $+/- 2$ desvios médios (MDev) nos fatores determinantes: crescimento do PIB, crescimento do crédito, perdas de crédito e receitas pré-provisão.

#### Exemplo Numérico do Banco 1
* Capitalização Tier 1 base sob estresse: $1,639\%$.
* Sob choque de PIB $-1\text{ MDev}$ desfavorável ($-1,5\text{ ppts}$ de PIB): Tier 1 cai para $0,373\%$ (impacto de $-1,27\text{ ppts}$).
* Sob choque de PIB $+1\text{ MDev}$ favorável ($+1,5\text{ ppts}$ de PIB): Tier 1 sobe para $2,835\%$ (impacto de $+1,20\text{ ppts}$).

Cálculo de $H$:

$$H(+/- 1\text{ MDev}) = \frac{0,373 + 2,835}{2} - 1,639 = 1,604 - 1,639 = -0,035\text{ ppts}$$

Usando a variação direta da capitalização:

$$H = \frac{-1,27 + 1,20}{2} = -0,035\text{ ppts}$$

Para choques de $+/- 2\text{ MDev}$, $H$ expande-se para $-0,141\text{ ppts}$.

#### Descobertas Cruciais do Lab Bancário
* **Fragilidades Ocultas**: Bancos como o **Banco 3** e o **Banco 4** não foram classificados como os mais vulneráveis ao observar apenas o impacto do estresse pontual padrão (queda de capitalização no teste tradicional). No entanto, ao aplicar a heurística $H$, revelaram severas fragilidades côncavas ($H = -0,294$ e $H = -0,863$ para choques combinados). Eles seriam desproporcionalmente destruídos se o ambiente apresentasse uma volatilidade ligeiramente superior à testada no cenário padrão.
* **Inversão de Ranking**: A abordagem tradicional colocava o Banco 6 como altamente frágil, mas a heurística $H$ revelou comportamentos de desalavancagem e redução não-linear de Ativos Ponderados pelo Risco (RWA) via absorção de perdas, tornando a resposta marginal do Banco 6 menos frágil do que a do Banco 3.

### Limitações Teóricas e Práticas dos Labs
1. **Presença de Pseudo-Convexidades**: A heurística $H$ avalia variações discretas ao redor do ponto de estresse. Se a função de resposta apresentar inflexões locais severas (efeitos não-monotônicos), é necessário expandir a variação $\Delta$ para múltiplos pontos ($1\Delta, 2\Delta, 3\Delta$) a fim de evitar falsos diagnósticos de robustez.
2. **Dependência de Transmissão Não-Linear**: A detecção depende diretamente de os modelos satélite refletirem adequadamente as alças de realimentação (*feedback loops*) entre a deterioração dos ativos e os custos de captação das instituições.

---

## 8 Como Rodar os Labs em Python e Checklist

### Pipeline Conceitual em Python

```python
import numpy as np
import scipy.stats as stats

def calcular_heuristica_fragilidade(f_alpha, f_alpha_minus_delta, f_alpha_plus_delta):
    """
    Calcula a Heuristica H de Taleb & Douady.
    f_alpha: Resultado da metrica no estresse central
    f_alpha_minus_delta: Resultado com estressor reduzido por 1 Desvio Medio
    f_alpha_plus_delta: Resultado com estressor aumentado por 1 Desvio Medio
    """
    H = (f_alpha_minus_delta + f_alpha_plus_delta) / 2.0 - f_alpha
    return H

def classificar_regime(H, threshold=0.01, metrica_eh_capital=True):
    """
    Classifica o ativo/sistema nos regimes R+, R0 ou R-.
    Se a metrica for Capital/Retorno: H < 0 indica Frágil.
    Se a metrica for Perda/Dívida: H > 0 indica Frágil.
    """
    if metrica_eh_capital:
        if H < -threshold:
            return "R+ (FRÁGIL)"
        elif H > threshold:
            return "R− (ANTIFRÁGIL)"
        else:
            return "R0 (ROBUSTO)"
    else:
        if H > threshold:
            return "R+ (FRÁGIL)"
        elif H < -threshold:
            return "R− (ANTIFRÁGIL)"
        else:
            return "R0 (ROBUSTO)"

## --- Exemplo Numérico I: Banco 1 (Capitalização Tier 1) ---
f_base_banco1 = 1.639
f_minus_banco1 = 0.373  # PIB -1 MDev (desfavoravel)
f_plus_banco1 = 2.835   # PIB +1 MDev (favoravel)

H_banco1 = calcular_heuristica_fragilidade(f_base_banco1, f_minus_banco1, f_plus_banco1)
regime_banco1 = classificar_regime(H_banco1, threshold=0.005, metrica_eh_capital=True)

print(f"Banco 1 -> Escalar H: {H_banco1:.4f} | Regime: {regime_banco1}")

## --- Exemplo Numérico II: Déficit Orçamentário (Custo/Perda) ---
f_base_deficit = -200.0
f_minus_deficit = -550.0  # Desemprego 10% (desfavoravel)
f_plus_deficit = -75.0     # Desemprego 8% (favoravel)

H_deficit = calcular_heuristica_fragilidade(f_base_deficit, f_minus_deficit, f_plus_deficit)
regime_deficit = classificar_regime(H_deficit, threshold=1.0, metrica_eh_capital=False)

print(f"Déficit -> Escalar H: {H_deficit:.4f} | Viés de Convexidade: {H_deficit:.2f} bi | Regime: {regime_deficit}")
```

### Checklist Operacional Pré-Execução

* [ ] **Validação de Dados e Odds**: Verificar se as probabilidades implícitas $p_A, p_B$ foram corretamente invertidas a partir de cotações decimais e limpas de erros de amostragem.
* [ ] **Verificação de Cointegração e Estacionariedade**: Garantir que o spread latente do processo Ornstein-Uhlenbeck foi estimado via Filtro de Kalman em espaço-estado, mantendo os resíduos do spread estacionários.
* [ ] **Cálculo da Banda Paramétrica de Bootstrap**: Confirmar que as decisões de entrada (*gate* 1) utilizam os limites superiores do bootstrap paramétrico em um passo adiante.
* [ ] **Aplicação do Modelo Bradley-Terry**: Garantir que a seleção individual do ativo/candidato desalinhado (*gate* 2) está configurada sem intercepto e de forma antissimétrica.
* [ ] **Execução do Teste de Perturbação da Heurística $H$**: Aplicar os choques de $\pm 1 \Delta$ e $\pm 2 \Delta$ (desvio absoluto médio) sobre todas as variáveis de estresse.
* [ ] **Avaliação do Classificador R+ / R-**: Garantir que ativos ou estratégias que retornem $H$ côncavo no domínio de retorno ($R-$) sejam estritamente bloqueados pelo sistema de risco.
* [ ] **Verificação de Fricção e Custos**: Assegurar que as métricas de retorno esperadas superem o *bid-ask spread*, impostos e taxas de empréstimo da corretora/exchange.

---

## 9 Tabela Comparativa e Glossário

### Tabela Comparativa Multidimensional

| Dimensão | Beta de Livro (CAPM / Teórico) | Beta Operacional (Khem Kapital) |
| :--- | :--- | :--- |
| **Premissa de Estacionalidade** | Linear e estática no tempo | Dinâmica, não-linear e sensível a mudanças de regime |
| **Tratamento do Erro de Modelo** | Assumido como nulo; parâmetros tidos como exatos | Incorporado via perturbação e medição da sensibilidade de cauda |
| **Medição de Risco** | Variância / Desvio Padrão ($L_2$ norm) / VaR pontual | Desvio semi-absoluto ($L_1$ norm) e Vega de Cauda ($V$) |
| **Mecanismo de Seleção** | Correlação histórica e regressão OLS simples | Processo OU com Ruído + Bootstrap Paramétrico + Bradley-Terry |
| **Comportamento sob Estresse** | Falha devido ao viés de convexidade e perdas por impacto (*fire sales*) | Detecta e bloqueia ativamente estruturas côncavas ($R-$) via escalar $H$ |
| **Aplicação em Apostas / Eleições** | Inaplicável | Inversão de odds em probabilidades implícitas e spreads de par |

---

| Métrica / Conceito | Modelos Tradicionais (VaR / Stress Test Pontual) | Classificador de Fragilidade (Heurística H) |
| :--- | :--- | :--- |
| **Avaliação das Caudas** | Avalia apenas a estimativa pontual de um único cenário | Avalia a curvatura (convexidade/concavidade) ao redor do cenário |
| **Vulnerabilidade a Chutes** | Cega para erros de especificação na distribuição | Detecta viés de modelo sem requerer a distribuição exata |
| **Resultado de Saída** | Resposta binária de Aprovado / Reprovado (*pass/fail*) | Escalar contínuo $H$ e classificação de regime ($R+, R0, R-$) |
| **Custo Computacional** | Alto (requer re-simulação de centenas de cenários) | Mínimo (fast-and-frugal: requer apenas 3 pontos de cálculo) |

### Glossário Técnico

* **Antifragilidade**: Propriedade de um sistema que se beneficia da volatilidade, desordem, ruído ou estresse dentro de limites suportáveis. Matematicamente definida por uma resposta convexa ao estressor ($H > 0$ em métricas de ganho).
* **Beta de Livro**: Medida teórica e linear de sensibilidade de um ativo em relação ao mercado, calculada via regressão linear clássica, assumindo resíduos estacionários e ausência de impactos de liquidez.
* **Beta Operacional**: Medida dinâmica e não-linear da sensibilidade de um spread ou ativo ao estressor de mercado, ajustada por fricções de trading, erro de modelo e não-linearidades de execução.
* **Bootstrap Paramétrico**: Técnica de reamostragem estatística baseada nos parâmetros estimados de um modelo estocástico (como o processo OU), utilizada para gerar limites de predição fora da amostra.
* **Desigualdade de Jensen**: Teorema matemático que estabelece que o valor esperado de uma função convexa é maior ou igual à função do valor esperado, gerando o viés de convexidade quando variáveis estocásticas são tratadas como fixas.
* **Filtro de Kalman**: Algoritmo recursivo que estima o estado não observado de um sistema dinâmico linear a partir de uma série de medições ruidosas e discretas no tempo.
* **Fragilidade**: Propriedade de um sistema que sofre desproporcionalmente com o aumento da volatilidade ou do estresse. Matematicamente representada por uma função de dano côncava e vega de cauda negativo ($H < 0$ em métricas de capital).
* **Heurística H**: Escalar livre de modelo e livre de probabilidade, calculado via perturbação simétrica em um teste de estresse ($H = \frac{f(\alpha - \Delta) + f(\alpha + \Delta)}{2} - f(\alpha)$), utilizado para medir a convexidade e quantificar a fragilidade.
* **Modelo Bradley-Terry**: Modelo de probabilidade empírica utilizado para prever o resultado de comparações pareadas entre concorrentes, adaptado aqui sem intercepto para determinar qual cotação individual de odd está desalinhada.
* **Over-round**: Margem do organizador do mercado (ou bookmaker) representada pelo excesso da soma das probabilidades implícitas acima de $100\%$ ($1,0$).
* **Pairs Trading**: Estratégia de arbitragem estatística que explora a reversão à média do spread entre dois ativos ou contratos historicamente correlacionados.
* **Processo Ornstein-Uhlenbeck (OU)**: Processo estocástico em tempo contínuo que modela o comportamento de uma variável que tende a retornar a uma média de longo prazo com uma determinada taxa de atração.
* **Regime R− (Antifrágil)**: Regime operacional onde o ativo ou estratégia apresenta convexidade favorável à volatilidade do mercado.
* **Regime R+ (Frágil)**: Regime operacional marcado por concavidade no domínio de resultados, onde pequenos desvios negativos no ambiente provocam colapsos desproporcionais no capital.
* **Robustez**: Propriedade de um sistema que resiste ao estresse e à volatilidade sem apresentar ganhos ou perdas desproporcionais; resposta linear ao estressor ($H \approx 0$).
* **Vega de Cauda ($V$)**: Sensibilidade da expectativa incondicional de perda nas caudas da distribuição em relação ao desvio semi-absoluto à esquerda ($s^-$).