<!-- imported from vault study notes; curated for open course -->
# M09.A02 — Lab — Classificador determinístico frágil (R+) vs antifrágil (R−)

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M09
> **Aula:** M09.A02

↑ M09 · Resumo · Completo

**Módulo:** M09
**Pergunta do módulo:** Como transformar beta e fragilidade em regras operacionais?

## Conceito-núcleo
Todo ativo elegível cai em exatamente uma perna: R+ frágil ou R− antifrágil; classificação OHLC; camada de opções separada.

## Aplicação em mercado / trading
Rotular universo para alocação/hedge: longs relativos em R−, shorts/hedges em R+ conforme regra do pipeline.

## Entregável / lab
Executar yahoo_fragility_pipeline.py (ou equivalente do repo); exportar labels R+/R− + notas da camada de opções.

## Fonte (mapeamento)
Fragile-Antifragile-Regime-Classifier (pipeline + PDF metodologia) | IG fragile/antifragile

## Guia de estudo aprofundado

> **info**
>

Este guia de estudos apresenta a sintetização completa dos conceitos, formulações matemáticas, intuição operacional e resultados empíricos da arquitetura do classificador dinâmico de resposta a variância MASS (*Methodology for Antifragile System Selection*).

---

### Visão Geral e Fundamentos Conceituais

#### A Fragilidade como Resposta Dinâmica
Na estrutura do classificador MASS, a fragilidade e a antifragilidade não são tratadas como propriedades estáticas de um ativo, tampouco são definidas pelo nível absoluto da volatilidade realizada. Um ativo com baixa volatilidade realizada não é automaticamente antifrágil, assim como um ativo altamente volátil não é necessariamente frágil. 

A fragilidade é definida rigorosamente como a **resposta** (ou sensibilidade) do desempenho acumulado de um ativo frente a alterações no seu nível de estresse local, onde o estresse é mensurado pela variância realizada amostral.

#### Arquitetura de Duas Pernas Mutuamente Exclusivas e Exaustivas
O classificador opera de forma determinística atribuindo cada ativo elegível $i$ em uma data de sinal $t$ a exatamente **uma de duas pernas de resposta**:
*   **Perna Frágil ($R+$):** Acontece quando o coeficiente de resposta $\hat{\beta}_{i,t} > 0$. Nesse regime, o aumento da variância realizada acarreta uma degradação (arrasto) no desempenho ajustado do ativo.
*   **Perna Antifrágil ($R-$):** Acontece quando o coeficiente de resposta $\hat{\beta}_{i,t} < 0$. Nesse regime, o aumento da variância realizada está associado a um ganho ou recuperação no desempenho ajustado do ativo.

As duas pernas satisfazem a relação de união disjunta para o universo válido $U_t$:
$$U_t = R_t^+ \dot{\cup} R_t^-, \quad R_t^+ \cap R_t^- = \emptyset$$

Não existe uma terceira classe ou "regime neutro". Se uma estimativa é finita e não nula, o sinal do coeficiente atribui o ativo de forma exaustiva a $R+$ ou $R-$.

#### Separação entre Classificação de Perna e Camada de Evidência
A arquitetura do sistema separa estritamente o problema da **classificação de perna** do problema da **confiança estatística**:
1.  **Atribuição da Perna ($R+/R-$):** Depende exclusivamente do sinal algébrico do coeficiente estimado $\hat{\beta}_{252}$.
2.  **Grau de Confiança (WEAK, MEDIUM, STRONG):** Avalia a estabilidade e a robustez desse sinal sob seis testes de estresse estatísticos. Um grau de confiança fraco (*WEAK*) não remove o ativo da perna $R-$ ou $R+$, nem o move para uma categoria neutra.
3.  **Filtro Exploratório de Curvatura (`taleb_validated`):** Campo reservado para identificar ativos em $R-$ que também satisfazem condições locais de curvatura quadrática e assimetria de cauda. É um filtro de pesquisa e não uma condição para definir a perna $R-$.

#### Isolamento da Camada de Opções
As cadeias de opções negociadas em mercado são mantidas completamente separadas do classificador $R+/R-$:
*   A classificação do ativo subjacente depende exclusivamente dos dados diários de preços (OHLC).
*   A ausência de cadeias de opções em mercado altera o status de dados para `option_status = MISSING`, mas **não cancela nem altera** a atribuição de perna $R+/R-$.
*   Modelos de precificação sintética de opções podem ser rodados em uma camada paralela, mas valores sintéticos nunca substituem ou sobrescrevem dados observados de mercado (como *bid*, *ask*, volume, *open interest* ou volatilidade implícita de mercado).

---

### Formulário Matemático e Modelo Estatístico

#### Variáveis Amostrais do Classificador OHLC
Para cada ativo $i$ na data observada $t$, com preço de fechamento ajustado $P_{i,t} > 0$:

1.  **Retorno Logarítmico Diário:**
    $$r_{i,t} = \ln P_{i,t} - \ln P_{i,t-1}$$

2.  **Variância Realizada Amostral Anualizada (Janela de 252 dias):**
    $$V_{i,t}^{(252)} = 252 \times \hat{\text{Var}}(r_{i,t-251}, \dots, r_{i,t})$$

3.  **Desempenho Logarítmico Anual em Excesso:**
    $$E_{i,t}^{(252)} = \ln P_{i,t} - \ln P_{i,t-252} - r_f$$
    onde a taxa livre de risco é fixada operacionalmente em $r_f = 0{,}02$ ($2\%$ ao ano).

#### Relação de Resposta de Variância Sinalizada MASS
A regressão é estimada sobre as $252$ observações mais recentes disponíveis no vetor de tempo $W_{i,t}$:
$$E_{i,s}^{(252)} = \alpha_{i,t} - \beta_{i,t} V_{i,s}^{(252)} + \varepsilon_{i,s}, \quad s \in W_{i,t}$$

Dada a convenção do modelo em escrever a inclinação com o sinal negativo ($-\beta$), a derivada condicional do desempenho esperado em relação à variância é:
$$\frac{\partial \hat{E}_{i,t}}{\partial V} = -\hat{\beta}_{i,t}$$

#### Estimador OLS em Forma Fechada
Escrevendo $X_s = V_{i,s}^{(252)}$ e $Y_s = E_{i,s}^{(252)}$, a inclinação Mínimos Quadrados Ordinários (OLS) convencional $b$ e o coeficiente de resposta $\hat{\beta}$ são dados por:
$$\hat{b}_{i,t} = \frac{\hat{\text{Cov}}_W(X, Y)}{\hat{\text{Var}}_W(X)}$$

$$\hat{\beta}_{i,t} = -\hat{b}_{i,t} = -\frac{\hat{\text{Cov}}_W\left(V^{(252)}, E^{(252)}\right)}{\hat{\text{Var}}_W\left(V^{(252)}\right)}$$

O intercepto $\hat{\alpha}$ e o coeficiente de determinação $R^2$ são computados como:
$$\hat{\alpha}_{i,t} = \bar{E}_{i,t} + \hat{\beta}_{i,t} \bar{V}_{i,t}$$

$$R_{i,t}^2 = \left[\text{Corr}_W\left(V^{(252)}, E^{(252)}\right)\right]^2$$

#### Modelos para Precificação Sintética de Opções
Quando cadeias de mercado não estão disponíveis, a precificação teórica de opções na camada secundária segue o modelo adequado para cada instrumento:

| Instrumento | Modelo Base | Formulação Matemática Principal |
| :--- | :--- | :--- |
| **Ação / ETF Europeu** | Black-Scholes-Merton (BSM) | $d_1 = \frac{\ln(S/K) + (r - q + \sigma^2/2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}$<br>$C = S e^{-qT} N(d_1) - K e^{-rT} N(d_2)$<br>$P = K e^{-rT} N(-d_2) - S e^{-qT} N(-d_1)$ |
| **FX (Câmbio)** | Garman-Kohlhagen | $d_1 = \frac{\ln(S/K) + (r_d - r_f + \sigma^2/2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}$<br>$C = S e^{-r_f T} N(d_1) - K e^{-r_d T} N(d_2)$<br>$P = K e^{-r_d T} N(-d_2) - S e^{-r_f T} N(-d_1)$ |
| **Opção sobre Futuro de Índice** | Black-76 | $d_1 = \frac{\ln(F/K) + \sigma^2 T / 2}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}$<br>$C = e^{-rT}\left[F N(d_1) - K N(d_2)\right]$<br>$P = e^{-rT}\left[K N(-d_2) - F N(-d_1)\right]$ |
| **Ação / ETF / Índice Americano** | Árvore Binomial / Diferenças Finitas | Suporta dividendos discretos e exercício antecipado. |

##### Banda de Sensibilidade Teórica
A incerteza do modelo de precificação sintética é capturada gerando uma banda de precificação a partir de três cenários de volatilidade estimada ($\sigma_{\text{estimada}}$):
$$\sigma_{\text{low}} = 0{,}75 \times \sigma_{\text{estimada}}, \quad \sigma_{\text{central}} = \sigma_{\text{estimada}}, \quad \sigma_{\text{high}} = 1{,}25 \times \sigma_{\text{estimada}}$$

*Nota de operação:* Esta banda expressa estritamente incerteza de modelo, **não** devendo ser confundida com um *spread bid-ask* de mercado.

---

### Intuição de Mercado e Trading

#### Interpretação Econômica dos Regimes

```
Variância Realizada (V) Sobe ---> Coeficiente beta > 0 (R+) ---> Desempenho Ajustado (E) Cai [Arrasto por Volatilidade]
Variância Realizada (V) Sobe ---> Coeficiente beta < 0 (R-) ---> Desempenho Ajustado (E) Sobe [Ganho com a Desordem]
```

*   **Perna $R+$ (Frágil):** Representa ativos cujo desempenho sofre degradação quando o estresse ou a incerteza do mercado aumenta. É o comportamento típico de ativos de crescimento ou com forte viés de carregamento positivo que sofrem com o *volatility drag* (arrasto de volatilidade).
*   **Perna $R-$ (Antifrágil):** Representa ativos que performam melhor ou recuperam seu valor em períodos de alta volatilidade realizada. Esse comportamento pode ser derivado de dinâmicas de repique (*rebound*), efeitos de alavancagem inversa, realimentação de volatilidade ou readequação de prêmios de risco.

#### Aplicação Operacional na Construção de Pares
O classificador de ativos é o módulo de entrada (*upstream*) para o sistema de pares MASS. 
*   A construção de pares exige desenhar um par de ativos combinando **obrigatoriamente** um elemento da perna frágil $R_t^+$ e um elemento da perna antifrágil $R_t^-$:
    $$\mathcal{P}_t \subseteq R_t^+ \times R_t^-$$
*   O classificador garante que o par seja formado por dois ativos em estados de resposta opostos no instante $t$.
*   A atração do par, ativação sob estresse, dominância de densidade e alocação de capital são executadas posteriormente pelo operador de pares MASS, não sendo incorporadas no classificador de ativos.

#### Alinhamento Temporal e Ausência de *Look-Ahead Bias*
Para evitar vazamento de informação (*look-ahead bias*):
*   O sinal de classificação $L_{i,t} = g(\mathcal{F}_{i,t})$ é gerado com as informações disponíveis até o fechamento da sessão $t$.
*   O sinal torna-se efetivo na próxima sessão observada ($t+1$), registrada no campo `signal_effective_date`.
*   Para a última linha observada de um ativo (data terminal), o campo `signal_effective_date` permanece **vazio**, pois a sessão seguinte ainda não ocorreu ou não foi baixada.

---

### Exemplo Numérico Resolvido Passo a Passo

A seguir, um cálculo simplificado da regressão OLS para determinar a inclinação $b$, o coeficiente de resposta $\hat{\beta}$ e a atribuição final de perna para um ativo hipotético com $m = 3$ observações na janela $W$.

#### Dados de Entrada
Assuma que temos os seguintes dados calculados para $V^{(252)}$ ($X$) e $E^{(252)}$ ($Y$):

| Observação ($s$) | Variância Realizada $X_s = V_{i,s}^{(252)}$ | Desempenho Excesso $Y_s = E_{i,s}^{(252)}$ |
| :---: | :---: | :---: |
| 1 | $0{,}04$ | $0{,}15$ |
| 2 | $0{,}09$ | $0{,}10$ |
| 3 | $0{,}16$ | $0{,}05$ |

#### Passo 1 Cálculo das Médias Amostrais
$$\bar{X} = \frac{0{,}04 + 0{,}09 + 0{,}16}{3} = \frac{0{,}29}{3} \approx 0{,}09667$$

$$\bar{E} = \frac{0{,}15 + 0{,}10 + 0{,}05}{3} = \frac{0{,}30}{3} = 0{,}10000$$

#### Passo 2 Cálculo dos Desvios e Produtos Crus
Calculando os desvios em relação às médias:

*   **Para $s = 1$:**
    *   $X_1 - \bar{X} = 0{,}04 - 0{,}09667 = -0{,}05667$
    *   $Y_1 - \bar{Y} = 0{,}15 - 0{,}10000 = +0{,}05000$
    *   $(X_1 - \bar{X})(Y_1 - \bar{Y}) = -0{,}0028335$
    *   $(X_1 - \bar{X})^2 = 0{,}0032115$

*   **Para $s = 2$:**
    *   $X_2 - \bar{X} = 0{,}09 - 0{,}09667 = -0{,}00667$
    *   $Y_2 - \bar{Y} = 0{,}10 - 0{,}10000 = 0{,}00000$
    *   $(X_2 - \bar{X})(Y_2 - \bar{Y}) = 0{,}0000000$
    *   $(X_2 - \bar{X})^2 = 0{,}0000445$

*   **Para $s = 3$:**
    *   $X_3 - \bar{X} = 0{,}16 - 0{,}09667 = +0{,}06333$
    *   $Y_3 - \bar{Y} = 0{,}05 - 0{,}10000 = -0{,}05000$
    *   $(X_3 - \bar{X})(Y_3 - \bar{Y}) = -0{,}0031665$
    *   $(X_3 - \bar{X})^2 = 0{,}0040107$

#### Passo 3 Covariância e Variância Amostrais
Somando os termos (dividindo por $m - 1 = 2$):

$$\hat{\text{Cov}}(X, Y) = \frac{-0{,}0028335 + 0 + (-0{,}0031665)}{2} = \frac{-0{,}0060000}{2} = -0{,}00300$$

$$\hat{\text{Var}}(X) = \frac{0{,}0032115 + 0{,}0000445 + 0{,}0040107}{2} = \frac{0{,}0072667}{2} \approx 0{,}0036333$$

#### Passo 4 Inclinação OLS e Conversão para $\hat{\beta}$
$$\hat{b} = \frac{\hat{\text{Cov}}(X, Y)}{\hat{\text{Var}}(X)} = \frac{-0{,}00300}{0{,}0036333} \approx -0{,}82568$$

Como a relação MASS define $\hat{\beta} = -\hat{b}$:
$$\hat{\beta} = -(-0{,}82568) = +0{,}82568$$

#### Passo 5 Atribuição de Perna
Como $\hat{\beta} = +0{,}82568 > 0$, o ativo é classificado deterministicamente na **Perna Frágil ($R+$)**.

---

### Armadilhas Comuns e Erros de Interpretação

| Armadilha | Descrição Errada | Correção Baseada nas Fontes |
| :--- | :--- | :--- |
| **1. Confundir Nível de Volatilidade com Fragilidade** | Achar que um ativo com alta volatilidade é frágil ($R+$) e um com baixa volatilidade é antifrágil ($R-$). | A fragilidade é a **sensibilidade (inclinação $\beta$)** do retorno em relação às mudanças na volatilidade, e não o nível do desvio padrão do ativo. |
| **2. Criar um "Regime Neutro"** | Tratar ativos com baixa significância estatística como "neutros" ou "não classificados". | O sistema é um classificador exaustivo de 2 pernas. Qualquer resultado finito e não nulo é estritamente $R+$ ou $R-$. A incerteza reflete no grau de confiança, nunca na remoção da perna. |
| **3. Injeção de Opções Sintéticas nos Dados de Mercado** | Preencher campos de *bid*, *ask* ou volatilidade implícita ausentes com saídas de modelos teóricos (ex: BSM). | Preços sintéticos só podem ser salvos em campos explícitos de modelo (`model_price`, `is_synthetic=1`). É proibido alterar os campos de dados observados de mercado. |
| **4. Incongruência de Sinal entre Inclinação e Coeficiente** | Assumir que se a inclinação OLS convencional $\hat{b}$ for negativa, o ativo é $R-$. | A relação MASS é $E = \alpha - \beta V$. Portanto, $\hat{\beta} = -\hat{b}$. Uma inclinação OLS negativa ($\hat{b} < 0$) implica em $\hat{\beta} > 0$ ($R+$). |
| **5. Viés de Sobrevivência na Avaliação Histórica** | Interpretar a largura e o histórico como prova do comportamento de todo o mercado no passado. | O painel de 419 ativos é fixado no terminal de corte (sobreviventes por 10 anos). As análises históricas refletem a projeção para trás desses sobreviventes. |
| **6. Confundir Acurácia de Software com Robustez do Sinal** | Acreditar que ter $0$ incompatibilidades de código significa que todos os sinais são estatisticamente estáveis no futuro. | A acurácia de software indica que o algoritmo calculou a regra matemática sem erros. A robustez estatística mede a estabilidade do sinal sob testes de estresse (apenas 120 de 419 ativos passaram em todos os testes). |

---

### Resultados Empíricos e Diagnósticos de Robustez

#### Painel da Execução de Referência
Os resultados empíricos estão ancorados na execução congelada sob o identificador `20260711T051344.464872Z`:
*   **Universo elegível (10 anos de histórico):** 419 tickers.
*   **Corte terminal (10 de julho de 2026):**
    *   **Perna $R+$ (Frágil):** 267 tickers ($63{,}72\%$). Mediana de $\hat{\beta}_{252} = 5{,}119$; Mediana do $R^2 = 0{,}295$.
    *   **Perna $R-$ (Antifrágil):** 152 tickers ($36{,}28\%$). Mediana de $\hat{\beta}_{252} = -4{,}405$; Mediana do $R^2 = 0{,}178$.
*   **Auditabilidade do código:** Zero discrepâncias entre o sinal do coeficiente e a perna atribuída em 3.439.101 linhas diárias classificadas.

#### As Seis Verificações de Diagnóstico de Confiança
Para avaliar a estabilidade do sinal medido, o pipeline aplica 6 testes adicionais:

1.  **HAC + FDR:** Covariância Newey-West com 63 lags e correção de taxa de falsa descoberta (FDR) de Benjamini-Hochberg a $5\%$. O intervalo de confiança HAC para $\beta$ não pode conter o zero.
2.  **Bootstrap em Bloco Circular:** 500 reamostragens com blocos circulares de 21 sessões. No mínimo $95\%$ dos coeficientes reamostrados devem manter o sinal original.
3.  **Consenso de Horizontes:** Coeficientes estimados sobre 126, 252 e 504 linhas de regressão devem apresentar o mesmo sinal.
4.  **Estabilidade por Deleção de Bloco:** Remoção sistemática de cada bloco não sobreposto de 21 sessões precisa preservar o sinal.
5.  **Estabilidade por Winsorização:** Winsorização de variância e desempenho a $1\%$ e $99\%$ deve preservar o sinal do coeficiente.
6.  **Persistência Recente de Sinal:** Pelo menos $80\%$ das últimas 126 estimativas móveis diárias devem ter o mesmo sinal atual.

##### Distribuição das Notas de Confiança
*   **STRONG (Forte):** Passa em todas as 6 verificações (120 tickers).
*   **MEDIUM (Média):** Passa em 4 ou 5 verificações (148 tickers).
*   **WEAK (Fraca):** Passa em 0 a 3 verificações (151 tickers).

##### Taxas de Aprovação por Diagnóstico
A tabela a seguir apresenta as taxas de aprovação observadas na execução de referência para cada um dos testes de diagnóstico:

| Diagnóstico de Confiança | Aprovação Total (419) | Aprovação $R+$ (267) | Aprovação $R-$ (152) |
| :--- | :---: | :---: | :---: |
| **HAC + FDR (63 lags)** | $55{,}8\%$ (234) | $61{,}4\%$ (164) | $46{,}1\%$ (70) |
| **Bootstrap em Bloco (21 sessões)** | $53{,}9\%$ (226) | $59{,}9\%$ (160) | $43{,}4\%$ (66) |
| **Consenso 126 / 252 / 504** | $57{,}5\%$ (241) | $66{,}3\%$ (177) | $42{,}1\%$ (64) |
| **Deleção de Blocos (21 sessões)** | $81{,}9\%$ (343) | $82{,}8\%$ (221) | $80{,}3\%$ (122) |
| **Winsorização (1% / 99%)** | $100{,}0\%$ (419) | $100{,}0\%$ (267) | $100{,}0\%$ (152) |
| **Persistência Recente de Sinal** | $57{,}8\%$ (242) | $56{,}6\%$ (151) | $59{,}9\%$ (91) |

*Observação:* Os ativos em $R-$ apresentam, em média, menor estabilidade sob consensos de horizonte e testes de bootstrap em comparação aos ativos em $R+$.

#### Dinâmica do Painel Balanceado (2018–2026)
*   **Período:** 3 de julho de 2018 a 10 de julho de 2026 (2.015 datas de sinal).
*   **Largura Média de $R+$:** $67{,}67\%$ dos ativos ativos permanecem em $R+$.
    *   **Máximo de $R+$:** $91{,}65\%$ em 8 de abril de 2020 (pico de estresse de mercado no COVID-19).
    *   **Mínimo de $R+$:** $14{,}80\%$ em 9 de março de 2022.
*   **Transições de Perna:** Foram registradas 16.913 mudanças de estado no total (8.449 transições de $R+ \to R-$ e 8.464 de $R- \to R+$).
*   **Duração dos Episódios:** A duração mediana de permanência ininterrupta em um regime é de **206 sessões para $R+$** e **111 sessões para $R-$**.

---

### Projeto Prático Sugerido no Lab (Python)

Abaixo descreve-se a sequência lógica recomendada para implementar e auditar o pipeline determinístico em Python.

#### Passo 1 Descompactação do Banco de Dados SQLite
Como arquivos grandes são gerenciados de forma comprimida no repositório, o laboratório inicia descompactando o banco SQLite localmente:

```python
import gzip
import shutil

## Restaura o banco de dados localmente ignorado pelo controle de versão
with gzip.open('yahoo_fragility.sqlite.gz', 'rb') as f_in:
    with open('yahoo_fragility.sqlite', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
```

#### Passo 2 Cálculo das Séries Temporais Móveis
Para cada ticker com pelo menos 10 anos de histórico elegível:
1.  Carregue a série temporizada de preços ajustados $P_t$.
2.  Calcule o retorno logarítmico diário: $r_t = \log(P_t) - \log(P_{t-1})$.
3.  Calcule a variância realizada amostral dos últimos 252 dias e anualize: $V_t^{(252)} = 252 \times \text{Var}(r_{t-251:t})$.
4.  Calcule o desempenho acumulado de 252 dias em excesso à taxa livre de risco: $E_t^{(252)} = \log(P_t) - \log(P_{t-252}) - 0{,}02$.

#### Passo 3 Estimação da Regressão Móvel e Atribuição de Perna
Para cada janela de 252 dias válidos:
1.  Estime a inclinação $b$ via OLS da regressão de $E^{(252)}$ contra $V^{(252)}$.
2.  Inverta o sinal para obter o coeficiente de resposta MASS: $\hat{\beta} = -b$.
3.  Aplique a regra determinística de atribuição:
    *   Se $\hat{\beta} > 0 \implies \text{leg} = \text{"R+"}$ (`FRAGILE`).
    *   Se $\hat{\beta} < 0 \implies \text{leg} = \text{"R-"}$ (`ANTIFRAGILE`).

#### Passo 4 Rotina de Auditoria de Software
Verifique a consistência entre o cálculo em forma fechada e a gravação de exportação:
1.  Recalcule a inclinação em forma fechada usando a fórmula de covariância/variância direta.
2.  Confirme se `abs(beta_reconstruido - beta_armazenado) < 1e-8`.
3.  Valide se não existe nenhum registro com divergência entre o sinal de $\hat{\beta}$ e a perna gravada.

---

### Glossário de Termos Importantes

*   **Antifragilidade (Perna $R-$):** Regime de resposta operacional em que o desempenho acumulado ajustado do ativo apresenta relação positiva com o aumento da variância realizada ($\hat{\beta} < 0$).
*   **Arrasto de Volatilidade (*Volatility Drag*):** Degradação do retorno composto de um ativo provocada pela variação ou dispersão dos retornos ao longo do tempo.
*   **Cadeia de Opções (*Option Chain*):** Conjunto de contratos de opções disponíveis no mercado para diferentes preços de exercício e datas de vencimento de um mesmo ativo subjacente.
*   **Consenso de Horizontes:** Diagnóstico de estabilidade que exige que os coeficientes estimados em janelas de 126, 252 e 504 dias compartilhem o mesmo sinal algébrico.
*   **Data de Sinal (*Signal Date*):** A data da sessão de mercado em que os dados de fechamento são observados para calcular os coeficientes e definir a perna.
*   **Data Efetiva do Sinal (*Signal Effective Date*):** A sessão de mercado imediatamente posterior à data do sinal, quando o estado de classificação passa a vigorar operacionalmente.
*   **Desempenho em Excesso Logarítmico ($E^{(252)}$):** Variação do preço logarítmico acumulada em 252 dias úteis descontada da taxa livre de risco anual fixada ($2\%$).
*   **Estatística HAC (Newey-West):** Correção de heterocedasticidade e autocorrelação nos erros da regressão, utilizada para construir intervalos de confiança e p-valores estatisticamente válidos sob dados sobrepostos.
*   **Fragilidade (Perna $R+$):** Regime de resposta operacional em que o desempenho acumulado ajustado do ativo apresenta relação negativa com o aumento da variância realizada ($\hat{\beta} > 0$).
*   **Largura da Perna Frágil (*$R+$ Breadth*):** Proporção de ativos no universo elegível classificados na perna $R+$ em uma determinada data de sinal.
*   **Mapeamento de Transição:** Registro diário de trocas de estado de um ativo entre as pernas $R+$ e $R-$.
*   **Opção Sintética:** Valor teórico de uma opção gerado por modelos analíticos ou numéricos (ex: Black-Scholes-Merton) quando dados reais de mercado não estão disponíveis.
*   **Taxa de Falsa Descoberta (FDR - Benjamini-Hochberg):** Procedimento estatístico de ajuste de p-valores em testes múltiplos para controlar a proporção de falsos positivos na seção cruzada de ativos.
*   **Variância Realizada Anualizada ($V^{(252)}$):** Estimativa da variância calculada sobre os últimos 252 retornos logarítmicos diários e multiplicada por 252.
*   **Winsorização:** Técnica estatística de limitação de valores discrepantes (*outliers*), substituindo valores extremos além de percentis pré-determinados (ex: $1\%$ e $99\%$).

---

### Questões de Fixação e Prática

#### Nível 1 Resposta Curta

##### Questão 1
Qual é a relação matemática direta entre a inclinação OLS convencional ($\hat{b}$) de uma regressão de desempenho contra variância e o coeficiente de resposta MASS ($\hat{\beta}$)?
*   **Resposta:** A relação é dada por $\hat{\beta} = -\hat{b}$. A inversão do sinal ocorre porque a equação do modelo MASS é especificada como $E = \alpha - \beta V + \varepsilon$. Assim, uma inclinação OLS negativa ($\hat{b} < 0$) resulta em um coeficiente de resposta positivo ($\hat{\beta} > 0$), classificando o ativo na perna frágil $R+$.

##### Questão 2
O que acontece com a classificação $R+/R-$ baseada em dados OHLC se a cadeia de opções de mercado para determinado ativo estiver ausente?
*   **Resposta:** A classificação $R+/R-$ permanece inalterada. O modelo separa estritamente a camada de preços OHLC da camada de opções. A falta da cadeia de opções altera o status para `option_status = MISSING`, mas mantém a classificação derivada dos preços do ativo subjacente.

##### Questão 3
Por que a data efetiva do sinal (`signal_effective_date`) fica vazia na linha referente à data terminal de um ativo?
*   **Resposta:** Porque o sinal é gerado no fechamento da sessão $t$ e só se torna efetivo na sessão subsequente ($t+1$). Na data terminal da base baixada, a sessão $t+1$ ainda não ocorreu ou não foi baixada, portanto a data efetiva permanece indisponível até o próximo *download*.

---

#### Nível 2 Questões Analíticas e de Aplicação

##### Questão 1
Um analista afirma que um ativo com nota de confiança *WEAK* na perna $R-$ deve ser reclassificado para uma categoria "neutra" e descartado da pipeline. Avalie essa afirmação com base nos princípios do classificador MASS.
*   **Resposta:** A afirmação do analista está incorreta sob a arquitetura MASS. O classificador é determinístico, exaustivo e composto por exatamente duas pernas ($R+$ e $R-$). Não existe regime neutro. A nota de confiança (*WEAK*, *MEDIUM*, *STRONG*) é uma camada de evidência anexada que quantifica a estabilidade estatística do sinal medido sob testes de estresse, mas não possui autoridade para alterar a perna atribuída ou remover o ativo da elegibilidade de formação de pares (`pair_eligible`).

##### Questão 2
Explique a limitação da estimativa HAC com 251 lags quando aplicada a uma amostra de 252 observações de regressão.
*   **Resposta:** Especificar 251 lags Newey-West em uma amostra de nominalmente 252 linhas coloca o estimador no limite matemático da amostra disponível. Nessa situação extrema, quase não restam produtos de lag efetivos para estimar a estrutura de autocovariância com precisão. Isso pode fazer com que a matriz de covariância subestime a verdadeira incerteza da amostragem, gerando um número artificialmente elevado de rejeições de hipótese nula. Trata-se de um teste de estresse de fronteira e não de um estimador inferencial ótimo.

##### Questão 3
Considere uma precificação sintética de opções para um ETF negociado nos EUA com dividendos discretos. Qual modelo de precificação deve ser utilizado e como a incerteza do modelo deve ser armazenada?
*   **Resposta:** Deve-se utilizar uma Árvore Binomial ou um modelo de Diferenças Finitas, que comportam o exercício antecipado típico de opções de estilo americano e dividendos discretos (diferente do modelo BSM fechado europeu). A incerteza deve ser registrada salvando a precificação em campos de modelo dedicados (`is_synthetic = 1`, `pricing_model = AMERICAN_TREE`), juntamente com a banda de sensibilidade computada sobre cenários de volatilidade ($\sigma_{\text{low}}, \sigma_{\text{central}}, \sigma_{\text{high}}$). Os campos de mercado (`market_bid`, `market_ask`, etc.) devem permanecer como `NULL`.

---

#### Nível 3 Prompts para Ensaios Acadêmicos e Aprofundamento

##### Prompt 1 Resposta Local vs. Antifragilidade Estrutural
> **Diretrizes para desenvolvimento do ensaio:**
> Compare o conceito de fragilidade como resposta local reduzida ($\hat{\beta} > 0$ ou $\hat{\beta} < 0$) utilizado pelo classificador determinístico com a definição matemática de antifragilidade estrutural proposta por Taleb e Douady. Em sua argumentação, aborde os seguintes pontos:
> 1. A diferença entre medir uma inclinação linear local versus avaliar a curvatura de segunda ordem (convexidade/propriedades de Jensen) em relação a perturbações de distribuição.
> 2. O papel do filtro exploratório `taleb_validated` e por que ele é tratado como uma ferramenta de geração de hipóteses e não como um critério de classificação de perna.
> 3. Como dinâmicas de mercado (como efeitos de alavancagem, realimentação de volatilidade e mudanças em prêmios de risco) podem gerar uma perna $R-$ sem necessariamente comprovar uma convexidade estrutural global do ativo.

##### Prompt 2 O Impacto da Sobreposição Amostral e Variáveis de Longa Memória na Inferência
> **Diretrizes para desenvolvimento do ensaio:**
> Analise os desafios econométricos associados ao uso de variáveis anuais sobrepostas ($V^{(252)}$ e $E^{(252)}$) calculadas diariamente em janelas móveis de 252 dias. Desenvolva sua resposta cobrindo:
> 1. Como a dependência temporal intrínseca afeta o tamanho amostral efetivo e distorce as estatísticas t convencionais do estimador OLS.
> 2. O desempenho comparativo dos testes de robustez utilizados no estudo (HAC Newey-West com 63 lags versus Bootstrap em Bloco Circular de 21 sessões e testes de deleção de bloco).
> 3. As consequências observadas no artigo ao estender os blocos de bootstrap para 63 e 126 sessões, e quais alternativas econométricas poderiam ser propostas em um programa de falsificação rigoroso (ex: observações não sobrepostas, assintótica de largura de banda fixa ou amostragem intradiária).