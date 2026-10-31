<!-- imported study note (guia-completo.md) -->
# Briefing Executivo: Módulo M06 - Econofísica Khem Kapital (Histerese, Caudas e Previsibilidade)

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M06

↑ M06 · Resumo · Completo

---

## Sumário Executivo

Este documento constitui o relatório técnico e analítico integral do Módulo M06 do curso **Econofísica Khem Kapital**, dedicado ao estudo de histerese, dependência de trajetória, caudas gordas, leis de potência, risco de cauda e limites operacionais de previsibilidade em mercados de alta frequência (*High-Frequency Finance*).

A partir de uma abordagem rigorosa baseada em processos pontuais estocásticos auto-excitados (*Hawkes Processes*), econometria de microestrutura e física estatística, este briefing sintetiza os fundamentos teóricos, formulações matemáticas em LaTeX, métodos de estimação não-paramétrica (como a inversão de Wiener-Hopf), dinâmica de livros de ofertas (*Order Books*), modelos de impacto de mercado e ferramentas computacionais.

Os principais achados e conceitos estruturantes abordados incluem:
*   **Endogenia e Reflexividade**: A atividade dos mercados financeiros modernos é predominantemente endógena (frequentemente operando próxima ao limiar crítico de instabilidade $\|\Phi\| \approx 1$), na qual o fluxo de ordens passado induz surtos auto-organizados de liquidez e volatilidade.
*   **Memória de Lei de Potência**: Os núcleos de interação de Hawkes exibem decaimento em lei de potência $\Phi(t) \sim t^{-(1+\gamma)}$ com expoente tailal $\gamma \in (0, 0,5)$, gerando dependência de longo alcance e Hurst aparente $H = 1/2 + \gamma$.
*   **Microestrutura e Impacto de Mercado**: O impacto das ordens de mercado é transiente e decai segundo $t^{-(\gamma+1)}$, enquanto o efeito epps e o *signature plot* do preço médio (*mid-price*) são explicados por dinâmicas cruzadas de reversão à média e autofluxo de execução.
*   **Limites Operacionais**: A previsibilidade determinística é severamente delimitada pela taxa de amplificação endógena, exigindo dimensionamento dinâmico de posição e gestão de stops baseada no risco de cauda e na reflexividade instantânea.

---

## 1. Histerese: Definição Física e Análogo em Mercados

### Definição Física
Na física dos materiais e sistemas complexos, a **histerese** é caracterizada pela dependência do estado de um sistema não apenas em relação às suas condições e estímulos atuais, mas em relação a todo o seu histórico de trajetórias passadas. Em sistemas ferromagnéticos ou no modelo clássico de Preisach, a resposta a um campo externo apresenta memória não-linear e retardo estrutural, de modo que o caminho de reversão não coincide com o caminho de excitação.

### Análogo em Mercados Financeiros
Nos mercados financeiros de alta frequência, o analógico direto da histerese manifesta-se na dependência de trajetória (*path-dependency*) do fluxo de ordens e na resposta assimétrica do livro de ofertas (*Limit Order Book* - LOB). Um choque exógeno de informação ou uma grande ordem de venda (*meta-order*) altera o estado interno de liquidez e a intensidade condicional de novos eventos, criando um ciclo de retroalimentação em que o sistema não retorna imediatamente ao seu estado de equilíbrio original após a remoção do estímulo.

Dentro do arcabouço de processos pontuais contínuos, essa memória estrutural e excitação retroalimentada são formalizadas pelos **Processos de Hawkes**. Um processo counting $D$-variado $N_t = \{N_t^i\}_{i=1}^D$ possui vetor de intensidade condicional $\lambda_t = \{\lambda_t^i\}_{i=1}^D$ definido como a densidade de probabilidade condicional de ocorrência de um evento no futuro imediato dada a filtração $\mathcal{F}_t$:

$$\lambda_t^i = \lim_{\Delta \to 0} \frac{1}{\Delta} \mathbb{E}\left[ N_{t+\Delta}^i - N_t^i \mid \mathcal{F}_t \right]$$

A histerese e a memória do mercado são expressas pela estrutura linear de auto-excitação e excitação cruzada:

$$\lambda_t^i = \mu_i + \sum_{j=1}^D \int_0^t \varphi_{ij}(t - s) \, dN_s^j = \mu_i + \sum_{m=1}^M \varphi_{i, k_m}(t - t_m)$$

Em que:
*   $\mu_i \ge 0$ é a intensidade exógena de base (linha de base imprevisível ou choque externo).
*   $\Phi(t) = \{\varphi_{ij}(t)\}_{i,j=1}^D$ é a matriz de núcleos de resposta (*kernels*), componente a componente positiva e causal ($\varphi_{ij}(t) = 0$ para $t < 0$).
*   $t_m$ representa o instante de ocorrência do $m$-ésimo evento do tipo $k_m \in \{1, \dots, D\}$.

---

## 2. Dependência de Trajetória, Memória e Drawdown

### Núcleos Exponenciais versus Lei de Potência

A natureza do decaimento da memória no mercado depende da especificação matemática do núcleo $\Phi(t)$:

1.  **Núcleo Exponencial (Memória Curta / Markoviana)**:
    $$\varphi(t) = \alpha \beta e^{-\beta t} \mathbf{1}_{\{t \in \mathbb{R}_+\}}$$
    O parâmetro $\alpha$ representa a força total de interação (norma $L_1$), e $\beta$ controla a taxa de relaxamento. Sob o núcleo exponencial, o par $(N_t, \lambda_t)$ forma um processo Markoviano governado pela equação diferencial estocástica:
    $$d\lambda_t = -\beta \lambda_t \, dt + \alpha \beta \, dN_t$$
    A função de autocorrelação decai exponencialmente conforme $c(t) \propto e^{-(1-\alpha)\beta |t|}$.

2.  **Núcleo em Lei de Potência (Memória Longa / Não-Markoviana)**:
    $$\Phi(t) = \frac{\alpha \beta}{(1 + \beta t)^{1+\gamma}} \mathbf{1}_{\{t \in \mathbb{R}_+\}}$$
    O parâmetro $\gamma > 0$ determina o expoente da cauda do núcleo. Para $\gamma < 1$, o decaimento da autocorrelação do fluxo de eventos obedece a um comportamento assintótico de memória longa:
    $$c(t) \sim (\beta t)^{-\gamma - 1}$$
    Na região intermediária e sob regimes quase-críticos, o processo desenvolve uma escala intermediária com Hurst aparente $H = 1/2 + \gamma$, explicando empiricamente o agrupamento de volatilidade (*volatility clustering*).

### Dinâmica de Drawdown e Processos Marcados
O risco de *drawdown* prolongado é amplificado pela memória auto-excitada. Para modelar eventos extremos e grandes quedas de preço (*exceedances*), utiliza-se o **Processo de Hawkes Marcado**, no qual cada evento carrega uma variável aleatória $\xi_m$ (marca) correspondente ao volume negociado, tamanho do salto de preço ou magnitude da perda:

$$\lambda_t^i = \mu_i + \sum_{m=1}^M \varphi_{i, k_m}(t - t_m) \chi_{i, k_m}(\xi_m)$$

Modelos aplicados a quedas profundas (como os desenvolvidos por Chavez-Demoulin & McGill e Embrechts et al.) demonstram que as marcas $\xi$ seguem distribuições de cauda pesada (ex.: Pareto ou Gamma). A ocorrência de um grande *drawdown* eleva instantaneamente o patamar de intensidade $\lambda_t$, gerando reações em cascata de liquidação contagiada.

### Exemplo Numérico Concreto: Comparação de Intensidades

Considere um mercado com intensidade exógena $\mu = 0,20$ eventos/segundo.

*   **Cenário A (Exponencial)**: $\alpha = 0,80$, $\beta = 1,0 \, \text{s}^{-1}$.
    *   Sendo $\|\Phi\| = \alpha = 0,80 < 1$, o sistema é estável.
    *   A intensidade média de equilíbrio é:
        $$\Lambda = \frac{\mu}{1 - \alpha} = \frac{0,20}{1 - 0,80} = 1,00 \text{ evento/s}$$
    *   Fraçao endógena de eventos: $80\%$; Fração exógena: $20\%$.

*   **Cenário B (Lei de Potência)**: $\alpha = 0,20$, $\beta = 1,0 \, \text{s}^{-1}$, $\gamma = 0,25$.
    *   A norma do núcleo é $\|\Phi\| = \int_0^\infty \frac{\alpha \beta}{(1+\beta t)^{1+\gamma}} \, dt = \frac{\alpha}{\gamma} = \frac{0,20}{0,25} = 0,80 < 1$.
    *   A intensidade média resulta em:
        $$\Lambda = \mu \left( \frac{\gamma}{\gamma - \alpha} \right) = 0,20 \times \left( \frac{0,25}{0,25 - 0,20} \right) = 1,00 \text{ evento/s}$$
    *   Apesar de possuírem a mesma taxa média $\Lambda = 1,00$, o Cenário B exibe aglomerações (*clusters*) de eventos e *drawdowns* incomparavelmente mais persistentes devido ao decaimento lento em lei de potência.

---

## 3. Caudas Gordas, Leis de Potência, Expoente de Cauda e Teoria de Valores Extremos

### Leis de Potência e Critério de Estabilidade
A estabilidade assintótica de um processo de Hawkes é governada pelo raio espectral da matriz $\|\Phi\| = \{\|\varphi_{ij}\|\}_{i,j=1}^D$, em que $\|\varphi_{ij}\| = \int_0^\infty |\varphi_{ij}(t)| \, dt$.

*   **Regime Subcrítico ($\|\Phi\| < 1$)**: O processo possui incrementos assintoticamente estacionários com taxa média finita $\Lambda = (I - \hat{\Phi}(0))^{-1} \mu$.
*   **Regime Supercrítico ($\|\Phi\| > 1$)**: A atividade cresce exponencialmente, gerando instabilidade e explosão de eventos.
*   **Regime Crítico / Quase-Estacionário ($\|\Phi\| = 1$)**: 
    *   Segundo o Teorema de Brémaud e Massoulié, para núcleos de curto alcance em dimensão $D=1$, o processo é degenerado ($\Lambda = 0$ ou $\infty$).
    *   No entanto, para núcleos de lei de potência com expoente $\Phi(t) \sim t^{-(1+\gamma)}$, se $\gamma \in (0, 0,5)$, existe um regime crítico não-degenerado com intensidade média finita, gerando distribuições de tamanho de aglomeração (*cluster size*) com caudas gordas e divergência das flutuações de variância.

### Representação em Árvores de Galton-Watson
Pela propriedade de ramificação (*clustering representation*), qualquer processo de Hawkes pode ser decomposto como uma floresta de árvores de Galton-Watson:
1.  Eventos "imigrantes" (geração 0) chegam segundo um processo de Poisson homogêneo com taxa $\mu_i$.
2.  Cada evento da geração $n-1$ gera filhos de primeira geração (geração $n$) com taxa dependente do tempo $\varphi_{ij}(t - t_m)$.
3.  O número médio de descendentes diretos por evento é dado pela norma $\|\Phi\|$. 

Quando $\|\Phi\| \to 1$, o número total de descendentes por árvore segue uma distribuição de probabilidade de cauda pesada (lei de potência), característica da Teoria de Valores Extremos (*Extreme Value Theory* - EVT).

---

## 4. Risco de Cauda e Implicações para Stops e Dimensionamento

### Medição da Reflexividade e Endogenia do Mercado
A reflexividade do mercado mede a proporção do fluxo de ordens e das variações de preço que decorre do próprio funcionamento interno do sistema (vendas forçadas, *stop losses*, algoritmos executores), em oposição a notícias exógenas.

A taxa de reflexividade do sistema é definida pela norma espectral do núcleo de Hawkes:

$$R = \|\Phi\|$$

Por meio da relação entre o espectro de variância e média das contagens em uma janela $T$ suficientemente grande ($N_T$), Hardiman e Bouchaud derivaram o estimador não-paramétrico livre de modelo para a reflexividade $D=1$:

$$\|\Phi\| \approx 1 - \sqrt{\frac{\mathbb{E}[N_T]}{\mathbb{V}[N_T]}}$$

Em um processo de Poisson estritamente exógeno, a variância é igual à média ($\mathbb{V}[N_T] = \mathbb{E}[N_T]$), resultando em $\|\Phi\| = 0$. À medida que o agrupamento e a auto-excitação aumentam, a razão variância-média $\mathbb{V}[N_T] / \mathbb{E}[N_T]$ explode, levando $\|\Phi\| \to 1$.

```
   POISSON (Exógeno)                     HAWKES CRÍTICO (Endógeno)
   ||Φ|| = 0                             ||Φ|| ≈ 1
   V[N_T] / E[N_T] = 1                   V[N_T] / E[N_T] >> 1
   
   Eventos aleatórios independentes      Cascata de eventos agrupados
   |  |   |   |  |   |  |                |||||||||    |||||       ||||||||
---|--|---|---|--|---|--|---> t      ----|||||||||----|||||-------||||||||---> t
```

### Exemplo Numérico Concreto: Estimativa de Reflexividade

Suponha a observação da contagem de ordens de mercado em janelas de $T = 60$ segundos ao longo de um dia de negociação:
*   Média amostral de contagem: $\mathbb{E}[N_T] = 100$ ordens.
*   Variância amostral calculada: $\mathbb{V}[N_T] = 2.500$.

Calculando a razão variância-média:
$$\frac{\mathbb{V}[N_T]}{\mathbb{E}[N_T]} = \frac{2.500}{100} = 25$$

Aplicando a fórmula de reflexividade:
$$\|\Phi\| \approx 1 - \sqrt{\frac{1}{25}} = 1 - \frac{1}{5} = 0,80 \quad (80\% \text{ de endogenia})$$

Se durante um evento de estresse do mercado a variância subir para $\mathbb{V}[N_T] = 10.000$:
$$\frac{\mathbb{V}[N_T]}{\mathbb{E}[N_T]} = \frac{10.000}{100} = 100 \implies \|\Phi\| \approx 1 - \sqrt{\frac{1}{100}} = 1 - 0,10 = 0,90 \quad (90\% \text{ de endogenia})$$

### Implicações para Stops e Dimensionamento de Posição
1.  **Ineficácia de Stops Fixos**: Sob regimes de alta reflexividade ($\|\Phi\| \ge 0,90$), as flutuações de preços ocorrem em surtos autocatalíticos. Stops posicionados em distâncias fixas de volatilidade clássica (ex.: $2\sigma$ Gaussiano) são atingidos com frequência ordens de magnitude superior ao previsto teoricamente.
2.  **Ajuste Dinâmico de Dimensionamento (Position Sizing)**: O tamanho da posição $S_t$ deve ser inversamente proporcional à reflexividade e à intensidade estocástica instantânea $\lambda_t$:
    $$S_t = S_0 \times \left(1 - \|\Phi\|_t\right) \times \frac{\bar{\lambda}}{\lambda_t}$$
    Quando a intensidade instantânea $\lambda_t$ dobra em relação à média $\bar{\lambda}$, o risco de cauda exige que o tamanho da posição seja reduzido pela metade.

---

## 5. Caos Determinístico, Atratores e Sensibilidade a Condições Iniciais

### Modelos Não-Lineares e Inibição
A generalização não-linear de processos de Hawkes permite introduzir mecanismos de **inibição** (núcleos com valores negativos $\varphi_{ij}(t) < 0$), simulando saturação de liquidez ou esgotamento de participantes:

$$\lambda_t^i = h\left( \mu_i + \sum_{j=1}^D \int_0^t \varphi_{ij}(t - s) \, dN_s^j \right)$$

Em que $h(x)$ é uma função de ligação não-linear, como $h(x) = \max(0, x)$ ou $h(x) = e^x$. O comportamento desse sistema pode exibir atratores complexos em espaço de fase e sensibilidade extrema ao estado inicial do livro de ofertas.

### Estrutura Restrita por Spread (*Spread-Gated Models*)
No modelo de preços de oferta e demanda (*Bid-Ask*) acoplados (como o proposto por Zheng et al. e Lee & Lee), a distância em ticks entre Ask e Bid (spread $S_t$) atua como uma barreira não-linear:
*   Quando $S_t = 1$ tick, as intensidades de saltos que reduziriam o spread abaixo de 1 são estritamente zeradas ($\lambda^{\text{down}} = 0$).
*   Essa dinâmica desacopla os regimes de volatilidade dependendo do estado do atrator do spread, gerando não-lineariedades estruturais e quebras de dependência linear.

---

## 6. Expoente de Lyapunov: Definição, Estimação e Horizonte de Previsibilidade

### Limite de Previsibilidade via Representação Martingal
A dinâmica de predição do vetor de intensidade estocástica é obtida pela representação de martingal de Hawkes. De acordo com o teorema de compensação, o processo $Y_t = N_t - \int_0^t \lambda_s \, ds$ é um martingal. 

Substituindo na equação de intensidade e utilizando o núcleo resolvete inverso $\Psi(t) = \sum_{n=1}^\infty \Phi^{*n}(t)$ cuja transformada de Laplace é $\hat{\Psi}(z) = (I - \hat{\Phi}(z))^{-1} - I$, a intensidade futura condicional à filtração do passado $\mathcal{F}_s$ (para $t > s$) é explicitamente prevista por:

$$\mathbb{E}\left[ \lambda_t \mid \mathcal{F}_s \right] = \mu + \int_0^t \Psi(t - u) \mu \, du + \int_0^s \Psi(t - u) \, dY_u$$

À medida que o horizonte de previsão $\Delta = t - s$ aumenta, a contribuição dos termos do passado $dY_u$ decai à taxa determinada pelos polos de $\hat{\Psi}(z)$.

```
   PREDIÇÃO DA INTENSIDADE E[λ_t | F_s]
   
   ^ λ_t
   |       Informação Conhecida (s)  |   Horizonte de Previsibilidade (t > s)
   |       /                         |   
   |      /                          |....... Convergência para
   |  /\ /                           | ~ ~ ~  a média Λ
   | /  V                            |
---|---------------------------------+----------------------------------> t
   0                                 s (instante atual)
```

### Divergência e Horizonte Operacional
O expoente de Lyapunov efetivo de um processo auto-excitatório relaciona-se com o maior valor próprio da matriz de interação $\|\Phi\|$. 
*   Para $\|\Phi\| < 1$, as perturbações no fluxo de informação decaem com tempo característico de relaxamento $\tau_R \approx \frac{1}{\beta(1 - \|\Phi\|)}$.
*   Quando $\|\Phi\| \to 1$, o tempo de relaxamento diverge ($\tau_R \to \infty$), significando que flutuações microscópicas propagam-se por longas escalas de tempo, destruindo a previsibilidade determinística e tornando o sistema dominado por ruído estocástico de ramificação (*branching noise*).

### Estimação Não-Paramétrica de Wiener-Hopf
Para evitar vieses de parametrização arbitrária na estimativa dos núcleos de interação, utiliza-se a inversão não-paramétrica do sistema de **Wiener-Hopf** (desenvolvida por Bacry e Muzy). 

Definindo a matriz de intensidade condicional observável $g_{ij}(t) = \frac{\mathbb{E}[dN_t^i \mid dN_0^j = 1]}{dt} - \Lambda_i$ para $t > 0$, o núcleo do Hawkes $\chi(t) = \Phi(t)$ é a única solução do sistema integral:

$$g(t) = \chi(t) + \chi(t) * g(t), \quad \forall t > 0$$

Discretizando esse sistema por técnicas de quadratura Gaussiana, obtém-se a matriz de núcleos $\Phi(t)$ diretamente dos dados observáveis, permitindo identificar interações inibitórias (negativas) ou de lei de potência sem pressupostos parametrizados.

---

## 7. Limites Operacionais de Sinal e Stop

### Ruído de Microestrutura e o *Signature Plot*
Ao analisar variações de preços no nível do tick, o sinal do preço é distorcido pelo ruído de microestrutura (*microstructure noise*). O modelo de preço $P_t$ proposto por Bacry et al. representa o *mid-price* como a diferença de dois processos de contagem bidimensionais auto e cruzadamente excitados:

$$P_t = P_0 + N_t^1 - N_t^2$$

Em que $N_t^1$ representa saltos para cima e $N_t^2$ saltos para baixo. A matriz de núcleo em cenário puramente reversivo é dada por:

$$\Phi(t) = \begin{pmatrix} 0 & \varphi^{(c)}(t) \\ \varphi^{(c)}(t) & 0 \end{pmatrix}$$

O gráfico de assinatura (*signature plot*), que mede a variação quadrática média $C(\tau) = \frac{1}{T} \sum_{i=0}^{T/\tau - 1} (P_{(i+1)\tau} - P_{i\tau})^2$ em função da escala de tempo $\tau$, exibe uma explosão característica quando $\tau \to 0$:

```
   SIGNATURE PLOT C(τ) - COMPORTAMENTO MICROESTRUTURAL
   
   ^ C(τ)
   | 
   | *
   |  * 
   |   *
   |    * * * * * * * * * * * * * * *  (Nível Difusivo de Longo Prazo)
   |
   +------------------------------------> τ (Escala de Tempo)
   0 (Tick Level)
```

Essa reversão à média de curtíssimo prazo no *tick level* implica que sinais operacionais baseados em impulso (*momentum*) executados em sub-segundos falharão sistematicamente devido ao *bid-ask bounce* e à fricção da liquidez.

### Interações do Livro de Ofertas Nível-I
No modelo 8-dimensional de Nível-I (Bacry, Jaisson e Muzy), eventos são classificados em:
*   Ordens de Mercado (Buy/Sell Trades: $T^a, T^b$)
*   Ordens Limite (Buy/Sell Limits: $L^a, L^b$)
*   Cancelamentos (Buy/Sell Cancels: $C^a, C^b$)
*   Mudanças no Mid-Price (Price Up/Down: $P^a, P^b$)

A análise empírica revela que:
1.  A matriz de núcleos das ordens que não alteram o preço ($T, L, C$) é eminentemente **diagonal** (auto-excitação massiva por fracionamento de ordens/meta-orders).
2.  O bloco de variação de preço ($P^a, P^b$) é **anti-diagonal**: um movimento de alta em $P^a$ excita fortemente um movimento subsequente de baixa $P^b$, confirmando a dominância da reversão à média na microestrutura.

---

## 8. Implementação em Python e Checklist

### Código Python: Simulação e Estimação de Processo de Hawkes

```python
import numpy as np
import matplotlib.pyplot as plt

def simulate_hawkes_exponential(mu, alpha, beta, max_time):
    """
    Simula um processo de Hawkes 1D com nucleo exponencial via Algoritmo de Thinning de Ogata.
    
    Parametros:
        mu (float): Intensidade exogena de base.
        alpha (float): Forca de auto-excitacao (norma L1).
        beta (float): Taxa de decaimento do nucleo.
        max_time (float): Tempo total de simulacao.
        
    Retorna:
        timestamps (np.ndarray): Instantes de ocorrencia dos eventos.
        intensities (np.ndarray): Perfil de intensidade nos instantes dos eventos.
    """
    timestamps = []
    intensities = []
    t = 0.0
    lambda_t = mu
    
    while t < max_time:
        # Ponto de guarda superior para a intensidade
        if len(timestamps) == 0:
            lambda_upper = mu
        else:
            # Calcular a intensidade exata no tempo atual t
            dt_past = t - np.array(timestamps)
            lambda_upper = mu + np.sum(alpha * beta * np.exp(-beta * dt_past))
            
        # Gerar candidato a tempo de salto via distribuicao exponencial
        u1 = np.random.uniform(0, 1)
        delta_t = -np.log(u1) / lambda_upper
        t += delta_t
        
        if t >= max_time:
            break
            
        # Calcular intensidade exata no tempo candidato t
        dt_past = t - np.array(timestamps)
        lambda_actual = mu + np.sum(alpha * beta * np.exp(-beta * dt_past))
        
        # Teste de aceitacao/rejeicao (Thinning)
        u2 = np.random.uniform(0, 1)
        if u2 <= (lambda_actual / lambda_upper):
            timestamps.append(t)
            intensities.append(lambda_actual)
            
    return np.array(timestamps), np.array(intensities)

def estimate_reflexivity(timestamps, window_size, total_time):
    """
    Estima o grau de reflexividade ||Phi|| atraves da razao Variancia-Media das contagens.
    
    Parametros:
        timestamps (np.ndarray): Instantes dos eventos.
        window_size (float): Tamanho da janela de contagem (T).
        total_time (float): Tempo total observado.
        
    Retorna:
        reflexivity (float): Estimativa da reflexividade ||Phi||.
        mean_counts (float): Media das contagens.
        var_counts (float): Variancia das contagens.
    """
    num_windows = int(total_time / window_size)
    counts = []
    
    for i in range(num_windows):
        t_start = i * window_size
        t_end = (i + 1) * window_size
        cnt = np.sum((timestamps >= t_start) & (timestamps < t_end))
        counts.append(cnt)
        
    counts = np.array(counts)
    mean_cnt = np.mean(counts)
    var_cnt = np.var(counts)
    
    if var_cnt == 0 or mean_cnt == 0:
        return 0.0, mean_cnt, var_cnt
        
    ratio = var_cnt / mean_cnt
    if ratio < 1.0:
        reflexivity = 0.0 # Aproximacao exogena pura
    else:
        reflexivity = 1.0 - np.sqrt(1.0 / ratio)
        
    return reflexivity, mean_cnt, var_cnt

## --- Execucao e Validacao Numerica ---
if __name__ == "__main__":
    np.random.seed(42)
    mu_param = 0.2
    alpha_param = 0.8  # Branching ratio ||Phi|| = 0.8
    beta_param = 1.0
    T_sim = 5000.0     # Tempo de simulacao
    
    events, lambda_vals = simulate_hawkes_exponential(mu_param, alpha_param, beta_param, T_sim)
    
    phi_est, mean_c, var_c = estimate_reflexivity(events, window_size=50.0, total_time=T_sim)
    
    print(f"Total de eventos gerados: {len(events)}")
    print(f"Taxa Media Teorica (Lambda): {mu_param / (1 - alpha_param):.4f} ev/s")
    print(f"Taxa Media Empirica: {len(events) / T_sim:.4f} ev/s")
    print(f"Reflexividade Teorica ||Phi||: {alpha_param:.4f}")
    print(f"Reflexividade Estimada ||Phi||: {phi_est:.4f}")
    print(f"Razao Variancia/Media (V[N]/E[N]): {var_c / mean_c:.4f}")
```

### Checklist Operacional para Algoritmos de Econofísica

*   [ ] **Validação de Estacionariedade**: Verificar se a norma do núcleo estimado cumpre rigorosamente $\|\Phi\| < 1$. Se $\|\Phi\| \ge 0,98$, ativar protocolo de risco para ambiente quase-crítico.
*   [ ] **Tratamento de Filtração Temporal**: Garantir resolução de timestamp sub-milissegundo ($10^{-6}$s) para evitar simultaneidade artificial de eventos que distorçam o cálculo de auto-excitação.
*   [ ] **Deteção de Inibição**: Monitorar se a matriz de núcleos apresenta componentes negativos. Se sim, utilizar a inversão não-paramétrica de Wiener-Hopf em substituição aos algoritmos EM (Expectation-Maximization) padrão.
*   [ ] **Ajuste de Position Sizing**: Escalar o tamanho do lote de execução proporcionalmente ao fator $(1 - \|\Phi\|_t)$.
*   [ ] **Filtro de Ruído de Microestrutura**: Não executar estratégias de *trend-following* em janelas de tempo inferiores ao ponto de inflexão do *signature plot* $C(\tau)$.
*   [ ] **Proteção contra Flash Crash**: Monitorar a razão variância/média $\mathbb{V}[N_T] / \mathbb{E}[N_T]$. Se a razão ultrapassar 50 em janelas móveis de 1 minuto, suspender o fornecimento de liquidez passiva.

---

## 9. Tabela Comparativa e Glossário

### Tabela Comparativa de Modelos de Processos Pontuais em Finanças

| Modelo / Abordagem | Dimensão ($D$) | Especif. do Núcleo $\Phi(t)$ | Método de Estimação | Aplicação Principal no Mercado |
| :--- | :--- | :--- | :--- | :--- |
| **Bowsher (2007)** | $2$ | Soma de Exponenciais | Máxima Verossimilhança (MLE) | Dinâmica conjunta de negociações e mudanças de preço no NYSE. |
| **Bacry, Dayri & Muzy (2012)** | $1 - 2$ | Não-Paramétrico / Espectral | Fatoração Espectral / Hilbert | Estimação livre de modelo do decaimento de memória e estabilidade. |
| **Filimonov & Sornette (2012)** | $1$ | Exponencial | Máxima Verossimilhança (MLE) | Medição da reflexividade do mercado e detecção de *flash crashes*. |
| **Hardiman, Bercot & Bouchaud (2013)** | $1$ | Lei de Potência / Soma Exp. | Razão Variância/Média & NP | Demonstração de estabilidade crítica constante ($\|\Phi\| \approx 1$) do S&P 500. |
| **Bacry, Delattre, Hoffmann & Muzy (2013)**| $2 - 4$ | Exponencial / Geral | MLE / GMM | Modelagem do ruído de microestrutura, *signature plot* e Efeito Epps. |
| **Bacry & Muzy (2014) - HIM** | $2$ | Lei de Potência | Analítico / Inversão | Modelo Hawkes de Impacto de Mercado (HIM) e decaimento $t^{-(\gamma+1)}$. |
| **Large (2007)** | $10$ | Exponencial | Máxima Verossimilhança (MLE) | Medição da resiliência do livro de ofertas (LSE Barclays). |
| **Bacry, Jaisson & Muzy (2015)** | $8$ | Lei de Potência / Geral | Inversão de Wiener-Hopf | Modelagem completa de Nível-I (trades, limites, cancelamentos e preços). |
| **Aït-Sahalia, Cacho-Diaz & Laeven (2014)** | Multi-Ativo | Exponencial + Difusão | Método dos Momentos (GMM) | Contágio financeiro e propagação de saltos entre índices globais. |

---

### Glossário Técnico de Econofísica e Microestrutura

*   **Auto-excitação (*Self-excitation*)**: Propriedade de um processo pontual na qual a ocorrência de um evento aumenta temporariamente a probabilidade condicional de ocorrência de novos eventos futuros no mesmo componente.
*   **Excitação Cruzada (*Cross-excitation*)**: Fenômeno em que a ocorrência de um evento em uma determinada variável (ex.: Ordem de Venda) aumenta a intensidade condicional de outra variável distinta (ex.: Cancelamento na Compra).
*   **Razão de Ramificação (*Branching Ratio*)**: Valor correspondente à norma $L_1$ ou maior valor próprio da matriz de núcleos $\|\Phi\|$. Define o número médio de eventos filhos gerados diretamente por um evento pai.
*   **Reflexividade**: Medida percentual da atividade do mercado que é gerada por retroalimentação endógena interna, quantificada por $\|\Phi\|$.
*   **Sistema de Wiener-Hopf**: Equação integral que conecta a matriz de correlação cruzada observável de um processo ao seu núcleo de interações diretas, permitindo estimação não-paramétrica sem viés.
*   **Efeito Epps**: Fenômeno empírico em que a correlação amostral calculada entre os retornos de dois ativos financeiros tende a zero à medida que a janela de amostragem temporal encolhe em direção ao nível de ticks contínuos.
*   **Gráfico de Assinatura (*Signature Plot*)**: Representação da variação quadrática (volatilidade realizada) em função da escala de agregação temporal $\tau$, utilizada para diagnosticar ruído de microestrutura e reversão à média.
*   **Algoritmo de Thinning (Ogata)**: Método de simulação estocástica exata para processos pontuais não-homogêneos que aceita ou rejeita saltos candidatos com base na razão entre a intensidade instantânea real e um limite superior local.
*   **Compensador de Martingal**: Processo acumulado de intensidade $\int_0^t \lambda_s \, ds$ que, subtraído do processo de contagem $N_t$, transforma o processo resultante em um martingal de média nula.