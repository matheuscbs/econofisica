<!-- imported from vault study notes; curated for open course -->
# M09.A01 — Lab — Beta operacional selecionado pelo ambiente de trading

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M09
> **Aula:** M09.A01

↑ M09 · Resumo · Completo

**Módulo:** M09
**Pergunta do módulo:** Como transformar beta e fragilidade em regras operacionais?

## Conceito-núcleo
Beta como relação estacionária entre tickers escolhida pelo ambiente executável (não só slope CAPM); cointegração, ADF/KPSS, regimes Q1–Q4, custos e risco de transição; entropia do ambiente.

## Aplicação em mercado / trading
Selecionar pares/spreads com beta estável no regime atual; reduzir drawdown via smart spread; incluir custos e transição Q.

## Entregável / lab
Rodar notebook do repo: data/ → testes de estacionariedade → regimes Q1–Q4 → métricas com custos; relatório de pares elegíveis.

## Fonte (mapeamento)
Beta-and-trading-environement (beta.pdf, beta.ipynb, data/, results/) | IG pinned beta + stable beta

## Guia de estudo aprofundado

> **info**
>

### Visão Geral e Objetivos de Aprendizagem

Este guia destina-se ao estudo aprofundado do conceito de **Beta Operacional**, conforme desenvolvido na pesquisa de Karim Khemiri (Khem Kapital). Diferente da abordagem tradicional baseada em uma única inclinação do CAPM ou em narrativas macroeconômicas discricionárias, o beta operacional é tratado como um *manifold* de relações finitas e estacionárias entre ativos (*tickers*), selecionado e delimitado pelas restrições de um ambiente de negociação real.

Ao concluir este guia, você deverá ser capaz de:
* Compreender a definição formal e empírica de Beta Operacional sob restrições do ambiente de trading.
* Diferenciar o diagnóstico estrutural contemporâneo (mesma data, $t+0$) da implantação executável causal ($t+1$).
* Formular e avaliar modelos de spreads estacionários através de testes de raiz unitária (ADF) e estacionariedade (KPSS) aplicados ao resíduo de nível centralizado.
* Interpretar a geometria de escores $Q1$–$Q4$, métricas de entropia, lacuna de escore (*score gap*) e modelos de risco de transição (*purged and embargoed*).
* Aplicar operadores formais de custos de execução, incluindo comissões, *spread* compra/venda, *slippage*, taxa de aluguel (*borrow*) e custo de financiamento (*funding*), considerando a contagem dupla de giro (*turnover* de saída mais entrada).
* Implementar um fluxo de trabalho em Python para reconstrução, auditagem, filtragem por histerese e simulação de livros *entry-frozen*.

---

### Conceitos-Chave Explicados em Profundidade

#### Beta Operacional como Manifold de Relação Estacionária
O Beta Operacional não é uma mera inclinação teórica ou uma história sobre a psicologia do mercado. É a estrutura estável de relações entre *tickers* que permanece legível, mensurável e executável após o ambiente impor suas restrições operacionais: universo admissível, acesso à corretora, margem de garantia, disponibilidade de aluguel de ações (*borrow*), taxas de financiamento, liquidez, *spread* de compra e venda (*bid-ask*), *slippage*, escala de capital, horários de negociação e requisitos regulatórios/legais.

O Beta Operacional é composto por oito elementos fundamentais:
1. Universo de *tickers* executáveis selecionado pelas restrições do ambiente.
2. Cestas opostas de compra (*buy*) e venda (*sell*) com pesos proporcionais à volatilidade inversa no ponto no tempo (*point-in-time*).
3. Coordenadas de *hedge* aplicadas a séries de retorno e nível.
4. Resíduo de deformação de nível centralizado causalmente.
5. Suporte de estados $Q1$–$Q4$ e geometria de escores associada.
6. Campos de auditoria de carga (*loading*), covariância, correlação e cointegração de cada ativo.
7. Diagnósticos de persistência de regime, risco de transição e entropia de informação.
8. Testes causais de implantação com custos explícitos de execução, aluguel, financiamento e rotatividade (*turnover*).

#### Seleção por Restrição do Ambiente (Admissibilidade de Probabilidade)
Inspirando-se na física de sistemas abertos (onde registros estáveis são selecionados pela acoplagem com o ambiente, e não escolhidos livremente pelo observador), o arcabouço estabelece que uma probabilidade atribuída a um regime de mercado só é operacionalmente admissível se o estado puder ser observado, mantido, financiado e falsificado dentro do ambiente $E_t$.

O ambiente executável $E_t$ no instante $t$ é formalmente definido como:
$$E_t = (U_t, A_t, M_t, L_t, F_{cost,t}, R_t)$$

Onde:
* $U_t$: Universo de *tickers* disponíveis.
* $A_t$: Instrumentos admissíveis.
* $M_t$: Regras de margem e alavancagem.
* $L_t$: Restrições de liquidez e venda a descoberto.
* $F_{cost,t}$: Cronograma de custos de execução e financiamento.
* $R_t$: Suporte de estados disponível.

Se uma relação de ativos for lucrativa no papel, mas não puder ser mantida sob os limites de margem, liquidez e aluguel de $E_t$, ela não pertence ao *manifold* do beta operacional.

#### Geometria de Escores Q1–Q4 e Papel Empírico dos Estados
A expansão da visão histórica de dois estados ($Q1/Q2$) para o pacote completo $Q1$–$Q4$ fornece suporte estatístico total e permite identificar o papel estrutural de cada quadrante no arquivo de dados:

| Estado | Frequência | Persistência (5 dias) | Taxa de Transição | Função Empírica no Arquivo |
| :--- | :--- | :--- | :--- | :--- |
| **Q1** | $39,16\%$ | $92,94\%$ | $12,97\%$ | Deformação positiva de cauda longa; vetor secundário de retorno. |
| **Q2** | $53,64\%$ | $94,98\%$ | $11,69\%$ | Vetor estático dominante do arquivo; maior estabilidade e retorno. |
| **Q3** | $3,71\%$ | $76,53\%$ | $52,04\%$ | Estado fraco de baixa volatilidade; funciona como detector de fronteira. |
| **Q4** | $3,49\%$ | $77,17\%$ | $37,50\%$ | Estado estritamente negativo; atua como indicador de estresse e transição. |

Os estados $Q3$ e $Q4$ não precisam gerar alpha individualmente para ter valor: sua função principal é reduzir a incerteza e sinalizar quando o sistema está perdendo invariância ou se aproximando de uma zona de transição de risco.

#### Desagregação Temporal Diagnóstico Estrutural vs. Livro Causal Executável
Existe uma diferença crítica entre medir a legibilidade de um estado no mesmo dia ($t+0$) e executar uma estratégia de negociação causal no dia seguinte ($t+1$):
* **Detector Estrutural Contemporâneo ($t+0$):** Apresenta um Índice de Sharpe bruto de $1,505$ nos dias ativos do pacote $Q1$–$Q4$. Ele mede quanta informação sobre o estado está contida na geometria de escores na mesma data.
* **Livro Causal com Congelamento na Entrada (*Entry-Frozen*, $t+1$):** Ao deslocar o sinal para o tempo causal, aplicar filtro de histerese ($h=0,05$) e deduzir custos sob estresse, o Sharpe cai para $0,537$ (com alpha anualizado líquido sob estresse de $5,59\%$).

A diferença entre $1,505$ e $0,892$ (bruto causal) é o **orçamento de conversão estrutural para causal**. A diferença entre $0,892$ e $0,537$ é o **orçamento de custos de execução do ambiente**.

---

### Intuição de Mercado e Trading

1. **Beta não é uma narrativa macroeconômica:** Um rótulo de estado ($Q1$–$Q4$) é uma coordenada estatística do *spread*, não uma história sobre inflação ou decisões de bancos centrais. Tentar ajustar a negociação a uma narrativa em vez da relação estrutural dos *tickers* expõe o operador ao risco de tomar decisões com base em variáveis não executáveis.
2. **O custo do *Over-Rotation* (Giro Excessivo):** No mercado real, mudar de posição constantemente gera custos devastadores. Trocar uma unidade da carteira A por uma unidade da carteira B exige encerrar A e abrir B. Isso representa **duas unidades de notional negociado** (saída + entrada). Sem um mecanismo de retenção (histerese) ou confirmação por consenso, os ganhos operacionais marginais são absorvidos por *bid-ask*, *slippage* e corretagem.
3. **Compressão de Volatilidade no Nível vs. Retorno Diário:** A coordenada de *hedge* baseada em retornos diários reduz pouco a variância do retorno diário (redução de $1,41\%$ a $5,82\%$). O verdadeiro efeito estabilizador do beta operacional ocorre no **acúmulo do nível**: a centralização causal da série de nível reduz a volatilidade do nível acumulado em **$79,19\%$** no arquivo completo (e reduz a variância do nível em **$95,67\%$**). É essa desaceleração do *drift* que permite identificar e operar desvios estacionários.
4. **Dimensionamento de Posição Baseado em Consenso (*Consensus-Risk*):** Quando múltiplos modelos (por exemplo, uma grade de $25$ regras com diferentes janelas e margens) discordam sobre qual é o estado líder, o estado da relação está difuso. Em vez de forçar uma alocação total, a intuição de mercado correta é reduzir proporcionalmente o tamanho da posição (*notional*), economizando capital e custos antes que a incerteza se converta em perdas.

---

### Fórmulas Fundamentais

#### 1. Retornos Logarítmicos e Baskets Opostos
Para preços ajustados $P_{i,t}$, os retornos logarítmicos e os retornos dos cestos ponderados pela volatilidade inversa ponto a ponto são:

$$r_{i,t} = \log\left(\frac{P_{i,t}}{P_{i,t-1}}\right)$$

$$R^+_t = \sum_{i \in U^+} w^+_{i,t} r_{i,t}, \quad R^-_t = \sum_{j \in U^-} w^-_{j,t} r_{j,t}$$

#### 2. Coordenada de Hedge ($\beta$) e Spread Diário de Excesso
A inclinação de *hedge* causal baseada em dados observados até $t-1$ e o *spread* diário resultante:

$$\beta_t = \frac{\text{Cov}_{\le t-1}(R^+, R^-)}{\text{Var}_{\le t-1}(R^-)}$$

$$a_t = R^+_t - \beta_t R^-_t$$

#### 3. Nível Acumulado e Resíduo de Deformação Centrado Causalmente
Acumulação dos níveis $L^+_t$ e $L^-_t$, *spread* bruto de nível com alinhamento $k_t$, e o resíduo estacionário $S_t$ obtido por uma janela causal de centralização $W_c$ (padrão de $126$ dias):

$$L^+_t = \sum_{\tau \le t} R^+_\tau, \quad L^-_t = \sum_{\tau \le t} R^-_\tau$$

$$S^{\text{raw}}_t = L^+_t - k_t L^-_t$$

$$S_t = S^{\text{raw}}_t - \frac{1}{W_c} \sum_{h=1}^{W_c} S^{\text{raw}}_{t-h}$$

#### 4. Operador de Custo Completo de Execução e Financiamento
O retorno líquido $a^{\text{net}}_t$ considera comissões/slippage $c_i$, taxa de aluguel anual $b_i$ sobre posições vendidas e taxa de financiamento anual $f_i$ sobre exposição bruta:

$$a^{\text{net}}_t = a_t - \sum_i c_i |p_{i,t} - p_{i,t-1}| - \frac{1}{252} \sum_i b_i \max(-p_{i,t}, 0) - \frac{1}{252} \sum_i f_i |p_{i,t}|$$

Note que a rotatividade negociada no dia é $T_t = \sum_i |p_{i,t} - p_{i,t-1}|$, cobrando integralmente cada transação (sem fator $1/2$).

#### 5. Concentração de Herfindahl (HHI) e Entropia de Posição
Métricas para avaliar a estrutura microestrutural da carteira a partir dos pesos de posição relativos $q_{i,t} = \frac{|p_{i,t}|}{\sum_j |p_{j,t}|}$:

$$\text{HHI}_t = \sum_i q_{i,t}^2$$

$$H_t = -\sum_i q_{i,t} \log(q_{i,t})$$

#### 6. Geometria de Escores Densidade Softmax e Lacuna Top-Two
Dado o vetor de escores padronizados $z_{q,t}$ para cada estado $q \in \{Q1, Q2, Q3, Q4\}$ e uma escala de dispersão $\tau_t$:

$$\hat{\rho}_{q,t} = \frac{\exp(z_{q,t}/\tau_t)}{\sum_{r} \exp(z_{r,t}/\tau_t)}$$

$$G_t = z_{(1),t} - z_{(2),t}$$

Onde $z_{(1),t}$ e $z_{(2),t}$ representam, respectivamente, o maior e o segundo maior escore do dia.

#### 7. Multiplicador de Risco de Consenso
Para uma grade de $25$ modelos $\Theta = \{63, 84, 126, 168, 252\} \times \{0; 0,25; 0,50; 0,75; 1,00\}$, a taxa de acordo $c_t$ e a posição ajustada com parâmetro $\eta \ge 0$:

$$\pi_{q,t} = \frac{1}{25} \sum_{\theta \in \Theta} 1\{\ell^\theta_t = q\}$$

$$c_t = |\pi_{Q1,t} - \pi_{Q2,t}| \in$$

$$p^{(\eta)}_t = c_t^\eta \left( \pi_{Q1,t} p_{Q1,t} + \pi_{Q2,t} p_{Q2,t} \right)$$

---

### Exemplo Numérico Resolvido Passo a Passo

Considere uma operação simplificada em um ambiente de ações dos EUA sob o cenário de custos base.

#### Dados de Entrada
* Retorno do Basket Compra ($R^+_t$): $+1,20\%$ ($0,0120$)
* Retorno do Basket Venda ($R^-_t$): $+0,80\%$ ($0,0080$)
* Coordenada de *hedge* calculada até $t-1$ ($\beta_t$): $1,10$
* Alinhamento de nível ($k_t$): $1,00$
* Nível acumulado $L^+_t = 0,1500$, $L^-_t = 0,1200$
* Média móvel de $126$ dias do $S^{\text{raw}}$ até $t-1$: $0,0250$
* Posição no dia $t-1$: Posição neutra ($p_{t-1} = 0$)
* Posição assumida no dia $t$: Compra de $1,0$ unidade no basket $R^+$ e venda de $1,10$ unidades no basket $R^-$ ($p_t = 1,0$). Notional negociado $T_t = 2,10$ unidades (mudança total de posição).
* Cronograma de custos base (EUA Equity):
  * Custos de execução $c_i$: $7,5 \text{ bps}$ ($0,00075$) por transação.
  * Custo anual de aluguel (*borrow*) $b_i$: $75 \text{ bps}$ ($0,0075$) sobre exposição vendida ($1,10$).
  * Custo anual de financiamento (*funding*) $f_i$: $50 \text{ bps}$ ($0,0050$) sobre exposição bruta ($2,10$).

---

#### Passo 1 Cálculo do Spread Diário Bruto de Excesso ($a_t$)
$$a_t = R^+_t - \beta_t R^-_t$$
$$a_t = 0,0120 - (1,10 \times 0,0080) = 0,0120 - 0,0088 = +0,0032 \text{ ou } 0,32\% \text{ (32 bps)}$$

---

#### Passo 2 Cálculo do Nível Bruto e Resíduo Estacionário Centrado ($S_t$)
$$S^{\text{raw}}_t = L^+_t - k_t L^-_t = 0,1500 - (1,00 \times 0,1200) = 0,0300$$
$$S_t = S^{\text{raw}}_t - \text{Média}_{126}(S^{\text{raw}}) = 0,0300 - 0,0250 = +0,0050 \text{ ou } 0,50\%$$

---

#### Passo 3 Dedução dos Custos de Execução e Rotatividade
Como a posição mudou de $0$ para $2,10$ de notional total:
$$\text{Custo de Execução} = c \times T_t = 0,00075 \times 2,10 = 0,001575 \text{ ou } 15,75 \text{ bps}$$

---

#### Passo 4 Dedução dos Custos Diários de Aluguel (*Borrow*) e Financiamento (*Funding*)
$$\text{Custo Diário de Borrow} = \frac{0,0075 \times 1,10}{252} = \frac{0,00825}{252} \approx 0,0000327 \text{ ou } 0,327 \text{ bps}$$

$$\text{Custo Diário de Funding} = \frac{0,0050 \times 2,10}{252} = \frac{0,0105}{252} \approx 0,0000417 \text{ ou } 0,417 \text{ bps}$$

$$\text{Custo Diário de Posse} = 0,0000327 + 0,0000417 = 0,0000744 \text{ ou } 0,744 \text{ bps}$$

---

#### Passo 5 Resultado Líquido Final ($a {\text{net}}_t$)
$$a^{\text{net}}_t = a_t - \text{Custo Execução} - \text{Custo Posse}$$
$$a^{\text{net}}_t = 0,0032 - 0,001575 - 0,0000744 = 0,0015506 \text{ ou } +0,1551\% \text{ (15,51 bps)}$$

O ganho bruto de $32 \text{ bps}$ foi reduzido para $15,51 \text{ bps}$ devido aos custos operacionais do ambiente, demonstrando empiricamente o impacto da atrito executável no alpha.

---

### Armadilhas Comuns (Pitfalls)

1. **Confundir Diagnóstico Contemporâneo com Desempenho Executável:** 
   * *Erro:* Publicar ou projetar retornos baseando-se no Sharpe contemporâneo de $1,505$ ($t+0$).
   * *Correção:* O resultado contemporâneo mede apenas a legibilidade do estado. O desempenho negociável real é o do modelo causal ($t+1$) com congelamento na entrada e custos completos ($0,537$ sob estresse).
2. **Atribuir Narrativas Macroeconômicas a Rótulos Estatísticos:**
   * *Erro:* Tratar o estado $Q1$ como "Crescimento/Inflação" ou $Q4$ como "Recessão".
   * *Correção:* Os rótulos $Q1$–$Q4$ representam coordenadas estatísticas do *spread*. Mudar os nomes para termos macroeconômicos introduz hipóteses não testadas que contaminam a auditoria quantitativa.
3. **Subestimar o Custo de Giro (Negligenciar a Dupla Contagem de Rotatividade):**
   * *Erro:* Assumir que a rotação entre carteiras custa apenas uma taxa de transação.
   * *Correção:* Rotacionar uma carteira exige fechar a posição antiga (exit) e abrir a nova (entry). O custo do *turnover* deve ser contabilizado como $T_t = \sum |p_{i,t} - p_{i,t-1}|$ sem a divisão por 2.
4. **Rejeitar o Pacote Q1–Q4 por Causa do Retorno Isolado do Q2:**
   * *Erro:* Concluir que o pacote $Q1$–$Q4$ é inútil porque o estado $Q2$ estático apresenta um alto índice de Sharpe sozinho.
   * *Correção:* A função do pacote $Q1$–$Q4$ não é substituir o $Q2$ em retorno simples, mas fornecer sinais de transição, medição de entropia, controle de risco e proteção em momentos de estresse de mercado.
5. **Vazamento de Dados em Modelos de Transição de Regime (Data Leakage):**
   * *Erro:* Utilizar modelos de aprendizado de máquina (*Machine Learning*) validados por *K-Fold cross-validation* tradicional.
   * *Correção:* A dependência serial das séries financeiras distorce o desempenho. É indispensável utilizar **validação purgada e embargada** (*purged and embargoed*), que separa os conjuntos de treino e teste por um intervalo temporal (embargo de 5 dias) para evitar vazamento de informação.

---

### Laboratório Prático Sugerido em Python

Este laboratório descreve em passos lógicos como construir um pipeline de auditoria do Beta Operacional utilizando dados sanitizados.

#### Passo 1 Carregamento de Dados e Verificação de Integridade
* Carregar o arquivo `data/beta_spread_pack_daily_sanitized.csv`.
* Validar as dimensões do arquivo: exatamente $4.165$ linhas e $203$ colunas.
* Verificar o intervalo de datas: de `2010-07-05` a `2026-06-29`.

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller, kpss

## 1. Leitura do arquivo sanitizado
df = pd.read_csv("data/beta_spread_pack_daily_sanitized.csv")
assert len(df) == 4165, "Contagem de linhas incorreta!"
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)
print("Dados carregados com sucesso. Período:", df['date'].min(), "a", df['date'].max())
```

#### Passo 2 Construção da Centralização Causal e Testes de Estacionariedade
* Calcular a série de nível bruto e aplicar a média móvel causal de $126$ dias.
* Executar os testes ADF e KPSS no resíduo $S_t$.

```python
## 2. Centralização causal de nível (janela Wc = 126)
Wc = 126
df['raw_level'] = df['level_plus'] - df['level_minus']
df['causal_center'] = df['raw_level'].shift(1).rolling(window=Wc).mean()
df['S_t'] = df['raw_level'] - df['causal_center']

## Filtrar valores válidos
valid_series = df['S_t'].dropna()

## Teste ADF (Nula possui raiz unitária)
adf_pvalue = adfuller(valid_series)

## Teste KPSS (Nula é estacionário)
kpss_pvalue = kpss(valid_series, regression='c', nlags='auto')

print(f"ADF p-value: {adf_pvalue:.6f} (Passa se < 0.05)")
print(f"KPSS p-value: {kpss_pvalue:.6f} (Passa se > 0.05)")
```

#### Passo 3 Determinação do Líder com Histerese e Sinais Causais
* Implementar o filtro de histerese $h=0,05$ entre os escores dos quadrantes para evitar alterações frequentes de posição (*churning*).

```python
## 3. Regra de Líder com Histerese h = 0.05
h = 0.05
leader = []
current_state = 'Q2' # Estado inicial padrão

for i in range(len(df)):
    z_q1 = df.loc[i, 'score_Q1']
    z_q2 = df.loc[i, 'score_Q2']
    
    if z_q1 - z_q2 > h:
        current_state = 'Q1'
    elif z_q2 - z_q1 > h:
        current_state = 'Q2'
    
    leader.append(current_state)

df['leader_causal'] = pd.Series(leader).shift(1) # Deslocamento causal t+1
```

#### Passo 4 Módulo de Contabilidade do Livro Entry-Frozen e Dedução de Custos
* Simular a manutenção de posição congelada e aplicar custos no momento da troca de estado.

```python
## 4. Simulação de livro entry-frozen com custos sob estresse
stress_execution_bps = 0.0025 # 25 bps por transação
annual_borrow_bps = 0.0300    # 300 bps ao ano
annual_funding_bps = 0.0150   # 150 bps ao ano

df['position'] = np.where(df['leader_causal'] == 'Q1', 1.0, 0.0)
df['turnover'] = df['position'].diff().abs().fillna(0.0)

## Calculo de retornos
df['gross_ret'] = df['position'] * df['spread_ret']
df['execution_cost'] = df['turnover'] * stress_execution_bps
df['holding_cost'] = df['position'] * ((annual_borrow_bps + annual_funding_bps) / 252.0)
df['net_ret_stress'] = df['gross_ret'] - df['execution_cost'] - df['holding_cost']

## Métricas Finais
sharpe_gross = np.sqrt(252) * df['gross_ret'].mean() / df['gross_ret'].std()
sharpe_stress = np.sqrt(252) * df['net_ret_stress'].mean() / df['net_ret_stress'].std()

print(f"Sharpe Bruto Causal: {sharpe_gross:.3f}")
print(f"Sharpe Líquido sob Estresse: {sharpe_stress:.3f}")
```

---

### Glossário de Termos Essenciais

* **ADF (Augmented Dickey-Fuller Test):** Teste estatístico de raiz unitária. A hipótese nula é que a série possui raiz unitária (não é estacionária). Para que o resíduo do *spread* seja válido, o valor-$p$ deve ser inferior a $0,05$.
* **Beta Operacional:** *Manifold* de relações estacionárias entre ativos, mantido e falsificado dentro das restrições operacionais impostas por um ambiente de negociação real.
* **Causalidade (Causal Alignment):** Princípio de estruturação de dados em que qualquer decisão ou estatística utilizada no instante $t$ é estritamente calculada a partir de informações disponíveis até $t-1$.
* **Coordenada de Hedge ($\beta$):** Razão entre a covariância dos cestos compra/venda e a variância do cesto de venda, calculada de forma móvel até $t-1$, para anular a exposição direcional primária.
* **Double-Counted Turnover:** Métrica de contabilização de rotatividade que reconhece que fechar uma posição e abrir outra incorre em custos operacionais nas duas pontas (saída + entrada), expressa como $T_t = \sum |p_{i,t} - p_{i,t-1}|$.
* **Entry-Frozen Book:** Modelo de execução em que a posição da carteira é fixada na entrada e mantida constante até que um novo sinal de transição seja acionado, evitando rebalanceamentos diários desnecessários.
* **Histerese ($h$):** Margem ou barreira de estabilidade exigida para alterar a classificação de um estado. Uma nova ordem só é executada se a diferença de escore entre o novo estado e o atual superar a margem $h$.
* **KPSS (Kwiatkowski-Phillips-Schmidt-Shin Test):** Teste estatístico de estacionariedade. A hipótese nula é que a série é estacionária. Um valor-$p$ superior a $0,05$ indica que não há evidência para rejeitar a estacionariedade da série.
* **Purged and Embargoed ML:** Metodologia de validação de modelos de aprendizado de máquina em séries temporais que remove amostras de treino sobrepostas (*purging*) e aplica um intervalo de tempo (*embargo*) após os testes para evitar contaminação de dados.
* **Score Gap ($G_t$):** Diferença absoluta entre o escore padronizado do estado líder e o escore do segundo colocado. Uma lacuna ampla indica elevada confiança e persistência do regime.

---

### Questões de Fixação e Treinamento

#### Nível 1 Questões de Resposta Curta (Conceituais)

**Questão 1.1**
O que distingue fundamentalmente a definição de Beta Operacional de uma simples inclinação de regressão do CAPM?
* **Resposta:** O Beta Operacional não é apenas um coeficiente de projeção ou uma narrativa teórica; é um *manifold* completo de relações finitas e estacionárias entre ativos que permanece legível, estável e executável após passar pelas restrições do ambiente de negociação (como margem, aluguel, liquidez, custos e fricções de execução).

**Questão 1.2**
Por que o teste de estacionariedade deve ser aplicado ao resíduo do nível acumulado e não apenas aos retornos diários do *spread*?
* **Resposta:** Retornos diários são quase sempre estacionários por construção. No entanto, se o nível acumulado apresentar desvio contínuo (*drift*), o *spread* acumulado perderá estabilidade econômica no longo prazo, inviabilizando a operação de reversão à média.

**Questão 1.3**
Qual é a diferença de cálculo na rotatividade de carteira (*turnover*) entre um rebalanceamento simples e a rotação completa entre duas carteiras?
* **Resposta:** A rotação completa exige encerrar a posição antiga e abrir a nova. O modelo de custos contabiliza ambas as operações como rotatividade negociada ($T_t = \sum |p_{i,t} - p_{i,t-1}|$), resultando em duas unidades de *notional* negociado (saída mais entrada), sem a divisão por 2.

**Questão 1.4**
O que indica uma alta lacuna de escore (*score gap*) entre o primeiro e o segundo estado no pacote $Q1$–$Q4$?
* **Resposta:** Uma lacuna de escore elevada indica que o estado líder está claramente separado dos concorrentes, o que se traduz em maior persistência temporal do regime (chegando a $100\%$ de persistência para lacunas $> 0,10$) e menor risco de transição imediata.

---

#### Nível 2 Questões Práticas e Análise de Dados

**Questão 2.1**
Analise a tabela de dados abaixo, extraída de um teste de centralização de nível para o *spread* $Q1$:

| Janela de Centralização ($W_c$) | ADF ($p$-valor) | KPSS ($p$-valor) | Redução de Volatilidade do Nível |
| :--- | :--- | :--- | :--- |
| **42 dias** | $7,90 \times 10^{-17}$ | $0,100$ | $86,69\%$ |
| **126 dias** | $9,27 \times 10^{-08}$ | $0,100$ | $79,23\%$ |
| **252 dias** | $3,98 \times 10^{-05}$ | $0,010$ | $73,84\%$ |

Com base nesses dados, responda:
a) Qual das janelas **falha** no critério de estacionariedade conjunto (ADF $< 0,05$ e KPSS $> 0,05$)?
b) Por que a janela de $126$ dias é selecionada como padrão no estudo, apesar de a janela de $42$ dias apresentar maior redução de volatilidade?

* **Resposta:**
  a) A janela de **$252$ dias** falha no teste KPSS, pois o $p$-valor de $0,010$ é menor que o limite de $0,05$, rejeitando a hipótese nula de estacionariedade.
  b) A janela de $126$ dias atinge o equilíbrio ideal entre reduzir substancialmente a volatilidade do nível ($79,23\%$), passar com folga nos dois testes de estacionariedade e evitar o rebalanceamento excessivo decorrente de janelas muito curtas (como a de $42$ dias), reduzindo o custo total de transação.

**Questão 2.2**
Um analista observa os seguintes resultados de desempenho para uma estratégia baseada no pacote $Q1$–$Q4$:
* Detector Estrutural Contemporâneo ($t+0$): Sharpe $= 1,505$.
* Livro Causal sem Histerese ($t+1$, $h=0,00$): Sharpe Bruto $= 0,898$; Sharpe Líquido sob Estresse $= -0,145$; Trocas de Estado $= 381$.
* Livro Causal com Histerese ($t+1$, $h=0,05$): Sharpe Bruto $= 0,892$; Sharpe Líquido sob Estresse $= 0,537$; Trocas de Estado $= 21$.

Explique qual mecanismo econômico fez o Sharpe líquido sob estresse mudar de **negativo ($-0,145$)** para **positivo ($0,537$)**, mesmo com o Sharpe bruto permanecendo praticamente idêntico ($0,898$ vs $0,892$).

* **Resposta:** O fator determinante foi a introdução da margem de histerese ($h=0,05$). Sem histerese ($h=0,00$), o modelo realizou $381$ trocas de estado, gerando rotação excessiva (*churning*) e consumindo o alpha bruto em taxas de execução, *bid-ask*, aluguel e financiamento. Com $h=0,05$, o número de trocas caiu de $381$ para apenas $21$. Ao filtrar ruídos e evitar trocas desnecessárias, a histerese preservou o resultado do livro após a aplicação dos custos operacionais do ambiente.

---

#### Nível 3 Questões Dissertativas para Aprofundamento

**Questão 3.1**
Desenvolva o conceito de "Admissibilidade de Probabilidade sob Seleção do Ambiente" em contraste com a probabilidade laplaciana enumerativa tradicional. Em sua resposta, aborde:
1. Como o ambiente de negociação atua como um filtro ativo sobre o universo de relações de ativos.
2. Por que a atribuição de probabilidade a uma narrativa macroeconômica não auditada é considerada operacionalmente inválida.
3. As quatro condições exigidas para aceitar uma probabilidade de regime no arcabouço do Beta Operacional.

* **Resposta Guiada / Estrutura da Resposta:**
  1. *Filtro do Ambiente:* A abordagem laplaciana tradicional enumera alternativas no papel assumindo simetria ou ignorância parcial. Em mercados financeiros reais, as escolhas não são livres; o ambiente de negociação $E_t$ atua como um filtro rigoroso. Restrições de margem, liquidez, disponibilidade de aluguel e custos eliminam diversas relações teóricas que não conseguem sobreviver no mundo real.
  2. *Invalidade de Narrativas Não Auditadas:* Atribuir probabilidades a histórias discricionárias (como "cenário de inflação") sem vincular o sinal a uma série de dados auditada é operacionalmente inválido. Se o estado não possuir uma definição matemática clara, uma regra de execução explícita e um teste de falsificação dentro da conta de negociação, a probabilidade calculada é apenas uma preferência subjetiva.
  3. *Quatro Condições de Admissibilidade:* Para que uma probabilidade de regime seja aceita, é necessário definir com precisão:
     - O ambiente executável explícito ($E_t$).
     - O *spread* estacionário subjacente (testado via ADF/KPSS).
     - O registro do regime (baseado na geometria de escores e métricas de entropia).
     - O teste de execução causal deduzido de custos operacionais.

**Questão 3.2**
Avalie criticamente o papel do Benchmark $Q2$ estático em relação ao pacote completo $Q1$–$Q4$. Se o estado $Q2$ estático apresenta desempenho consistente de maneira isolada, qual é a justificativa técnica para manter a complexidade do pacote $Q1$–$Q4$?

* **Resposta Guiada / Estrutura da Resposta:**
  1. *Desempenho Isolado do Q2:* O estado $Q2$ é o vetor estático dominante no arquivo empírico, apresentando um Índice de Sharpe elevado e servindo como um benchmark de baixa complexidade muito forte.
  2. *Limitações do Q2 Estático:* Uma alocação estática no $Q2$ não oferece mecanismos de sinalização quando o ambiente sofre alterações estruturais, entra em zonas de transição ou caminha para situações de estresse. O modelo estático é incapaz de medir a volatilidade do ambiente ou ajustar o risco antes de quedas expressivas (*drawdowns*).
  3. *Justificativa Técnica do Pacote Q1–Q4:* A inclusão do pacote $Q1$–$Q4$ não se justifica apenas pela busca por um Sharpe bruto maior do que o do $Q2$, mas sim pelas funções adicionais oferecidas pelo sistema:
     - **Mapeamento de Regimes e Entropia:** A combinação do estado líder com a lacuna de escores reduz a incerteza (*entropia*) do estado futuro em $78,03\%$.
     - **Diagnóstico de Transição e Risco:** Estados como $Q3$ e $Q4$ funcionam como alertas de borda. Quando a lacuna de escore diminui, o sistema sinaliza aumento no risco de transição.
     - **Mapeamento de Covariância entre Tickers:** Permite entender como a estrutura interna dos ativos muda ao longo do tempo.
     - **Mecanismo de Proteção e Dimensionamento:** Integrado com a camada de *Consensus-Risk* e portões de risco (*risk gates*), o pacote permite reduzir a exposição da carteira durante momentos de incerteza, otimizando o rebaixamento máximo (*drawdown*) e melhorando a segurança geral do sistema.