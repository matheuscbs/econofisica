<!-- imported from vault study notes; curated for open course -->
# M02.A01 — Movimento browniano geométrico: o modelo padrão de trajetória de preço

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M02
> **Aula:** M02.A01

↑ M02 · Resumo · Completo

**Módulo:** M02
**Pergunta do módulo:** Como a dinâmica do spot e as gregas mudam o P&L do livro?

## Conceito-núcleo
GBM: dS = μS dt + σS dW; log-preço gaussiano; papel de μ vs σ no trading vs na precificação.

## Aplicação em mercado / trading
Simular cenários de spot para stress de livro, sizing e checks de hedge; não confundir μ histórico com preço de opção.

## Entregável / lab
Gerar n paths GBM; comparar média/variância empírica vs teórica; plot de envelope.

## Fonte (mapeamento)
quantitative-trading-free-lesson/06 geometric brownian motion | IG Reels GBM/brownian

## Guia de estudo aprofundado

> **info**
>

Este guia de estudo oferece uma análise abrangente e estruturada sobre o Movimento Browniano Geométrico (GBM), a simulação de trajetórias de preços por Monte Carlo, a construção de limites estatísticos (túneis) e a implementação de sensores estatísticos para detecção de quebras de regime no mercado financeiro.

---

### Conceitos-Chave

#### Passeio Aleatório e Espaço Estatístico
O mercado move-se de forma aleatória, mas não desordenada. Um processo estocástico permite descrever a família de trajetórias possíveis dentro de um enquadramento estatístico delimitado. O preço de um ativo não pode ser previsto com exatidão para o dia seguinte, mas é possível delimitar a zona estatisticamente permitida para a sua evolução.

#### Passeio Aleatório Discreto vs. Gaussiano
* **Passeio Aleatório Discreto:** Modela variações com saltos fixos de amplitude constante (por exemplo, $+\text{passo}$ ou $-\text{passo}$ com probabilidades de $50\%$). Embora desenhe um "túnel" de trajetórias, é um modelo muito rígido para a realidade dos mercados.
* **Passeio Aleatório Gaussiano:** Substitui os saltos fixos por choques contínuos extraídos de uma distribuição Normal centrada $\mathcal{N}(0, \sigma^2)$. A escala desses choques é controlada diretamente pelo parâmetro de volatilidade $\sigma$.

#### O Conceito de Túnel no Movimento Browniano Geométrico (GBM)
O Movimento Browniano Geométrico modela o logaritmo dos preços adicionando um termo de tendência (*drift*) e um termo de difusão (ruído gaussiano). A volatilidade $\sigma$ funciona literalmente como o controle de "abertura do túnel":
* **Volatilidade alta ($\sigma$ elevado):** O túnel de dispersão estatística abre-se rapidamente.
* **Volatilidade baixa ($\sigma$ reduzido):** O túnel permanece estreito e contido.

O ajuste de tendência para os retornos logarítmicos inclui a correção de convexidade $-\frac{1}{2}\sigma^2$, garantindo a consistência teórica do processo estatístico.

#### Quebras de Regime e Limitações do Modelo Constante
Assumir uma volatilidade constante $\sigma_{model}$ é uma aproximação útil, porém limitada. Os mercados reais mudam de regime: sofrem compressões, agrupamentos de volatilidade (*clustering*), saltos discretos (*jumps*), assimetrias e caudas pesadas. Quando o caminho do preço sai do túnel teórico, isso não deve ser interpretado imediatamente como um sinal direcional de compra ou venda, mas sim como um **sinal de quebra de regime** (o modelo estático deixou de descrever o mundo real).

#### Sensores e Termômetros de Monitoramento
Para evitar a cegueira diante de mudanças no mercado, utilizam-se três sensores estatísticos:
1. **Volatilidade Realizada Rolante (RV):** Mede a variabilidade local em uma janela móvel de tempo. A razão $\frac{RV}{\sigma_{model}}$ indica se o túnel do modelo está excessivamente apertado para a volatilidade atual do mercado.
2. **Divergência de Kullback-Leibler (KL) Rolante:** Mede a alteração na forma da distribuição de retornos entre duas janelas consecutivas, capturando mudanças em caudas, assimetrias e valores discrepantes (*outliers*).
3. **CUSUM de Variância:** Algoritmo de soma acumulada que detecta transições, compressões ou aglomerações de variância em relação a uma linha de base.

---

### Fórmulas Matemáticas

#### Modelo de Retorno Logarítmico do GBM
Para um passo de tempo $\Delta t$ e um choque normal padronizado $Z \sim \mathcal{N}(0, 1)$:

$$\text{lnret}_t = \left( \mu - \frac{1}{2}\sigma_{true}^2 \right) \Delta t + \sigma_{true} \sqrt{\Delta t} Z_t + \text{saltos}$$

#### Reconstrução da Trajetória de Preços
$$S_t = S_0 \exp\left( \sum_{k=1}^{t} \text{lnret}_k \right)$$

#### Limites Teóricos do Túnel de Preço
Para um determinado número de desvios $z$ (por exemplo, $z = 2,58$):

$$\text{Média}_{log}(t) = \ln(S_0) + \left( \mu - \frac{1}{2}\sigma_{model}^2 \right) t$$

$$\text{Desvio Padrão}_{log}(t) = \sigma_{model} \sqrt{t}$$

$$\text{Limite Inferior}(t) = \exp\left( \text{Média}_{log}(t) - z \cdot \text{Desvio Padrão}_{log}(t) \right)$$

$$\text{Limite Superior}(t) = \exp\left( \text{Média}_{log}(t) + z \cdot \text{Desvio Padrão}_{log}(t) \right)$$

#### Volatilidade Realizada Rolante (RV)
Para uma janela de tamanho $W$ e retornos logarítmicos $w$:

$$RV = \sqrt{\frac{\text{Var}(w, \text{ddof}=1)}{\Delta t}}$$

#### Divergência de Kullback-Leibler (KL) Discreta
Com regularização $\epsilon$ para evitar divisão por zero:

$$P_a(i) = \frac{\text{contagem}_a(i) + \epsilon}{\sum (\text{contagem}_a + \epsilon)}, \quad P_b(i) = \frac{\text{contagem}_b(i) + \epsilon}{\sum (\text{contagem}_b + \epsilon)}$$

$$KL(P_a \parallel P_b) = \sum_{i} P_a(i) \ln \left( \frac{P_a(i)}{P_b(i)} \right)$$

#### Algoritmo CUSUM de Variância
Dado $x_i = r_i^2 - \text{baseline}$:

$$g_{pos, i} = \max(0, g_{pos, i-1} + x_i)$$

$$g_{neg, i} = \min(0, g_{neg, i-1} + x_i)$$

Alarme acionado se $g_{pos, i} > h$ ou $|g_{neg, i}| > h$, reiniciando os acumuladores para zero.

---

### Intuição de Mercado e Trading

* **Volatilidade como Dimensão Espacial:** A volatilidade não mede a direção da tendência (se o mercado vai subir ou cair), mas sim a velocidade de expansão das fronteiras estatísticas do preço.
* **Ruptura de Túnel $\neq$ Sinal Direcional:** A saída de um preço de um túnel GBM calibrado não significa que o ativo está "caro" ou "barato". Significa que as premissas de volatilidade estática falharam e que o mercado entrou em um novo regime de risco.
* **Gauges e Gregas de Opções:** As Gregas de opções de compra ou venda são instrumentos conectados diretamente à mecânica do túnel:
  * **Delta ($\Delta$):** Mede a reação do preço da opção conforme o ativo subjacente se desloca no interior do túnel.
  * **Gamma ($\Gamma$):** Mede a aceleração do Delta diante dos deslocamentos no túnel.
  * **Theta ($\Theta$):** Representa o custo ou ganho da passagem do tempo $t$ enquanto o preço evolui dentro do enquadramento.
  * **Vega ($\nu$):** Sensibilidade direta da opção à variação da largura do túnel (alteração na volatilidade $\sigma$).

---

### Exemplo Numérico Resolvido Passo a Passo

#### Cenário de Parâmetros
* Preço Inicial ($S_0$): $100,00$
* Tendência Anualizada ($\mu$): $0,00$
* Volatilidade do Modelo ($\sigma_{model}$): $0,20$ ($20\%$ ao ano)
* Tempo Total ($T$): $1,0$ ano ($252$ dias úteis)
* Passo de Tempo ($\Delta t$): $\frac{1}{252} \approx 0,00396825$
* Fator de Confiança ($z$): $2,58$

---

#### Passo 1 Cálculo do Drift Corrigido e Desvio por Passo
1. **Termo de Drift Corrigido:**

$$\text{drift} = \left( \mu - \frac{1}{2}\sigma_{model}^2 \right) \Delta t = \left( 0,00 - 0,5 \times 0,20^2 \right) \times \frac{1}{252} = -0,02 \times 0,00396825 = -0,000079365$$

2. **Termo de Difusão Base:**

$$\text{diff}_{base} = \sigma_{model} \sqrt{\Delta t} = 0,20 \times \sqrt{0,00396825} = 0,20 \times 0,0629941 = 0,0125988$$

---

#### Passo 2 Simulação do Primeiro Passo ($t = 1$)
Assuma que o sorteio gaussiano resultou em $Z_1 = 1,0$.

1. **Retorno Logarítmico no Passo 1:**

$$\text{lnret}_1 = \text{drift} + \text{diff}_{base} \times Z_1 = -0,000079365 + 0,0125988 \times 1,0 = 0,012519435$$

2. **Preço Simulado $S_1$:**

$$S_1 = S_0 \times \exp(\text{lnret}_1) = 100,00 \times \exp(0,012519435) = 100,00 \times 1,012598 = 101,26$$

---

#### Passo 3 Cálculo das Fronteiras do Túnel em $t = 1$
1. **Média Logarítmica em $t = 1$:**

$$\text{Média}_{log}(1) = \ln(100,00) + (-0,000079365) = 4,6051702 - 0,000079365 = 4,6050908$$

2. **Desvio Padrão Logarítmico em $t = 1$:**

$$\text{DesvPadrão}_{log}(1) = \sigma_{model} \sqrt{1 \times \Delta t} = 0,0125988$$

3. **Limites do Túnel em Nível de Preço ($z = 2,58$):**
   * **Limite Inferior:**

$$\text{Lower}_1 = \exp\left( 4,6050908 - 2,58 \times 0,0125988 \right) = \exp(4,6050908 - 0,0325049) = \exp(4,5725859) \approx 96,79$$

   * **Limite Superior:**

$$\text{Upper}_1 = \exp\left( 4,6050908 + 2,58 \times 0,0125988 \right) = \exp(4,6050908 + 0,0325049) = \exp(4,6375957) \approx 103,29$$

* **Resultado:** No dia 1, para um preço de $101,26$, a trajetória permanece com segurança dentro do túnel delimitado entre $96,79$ e $103,29$.

---

### Armadilhas Comuns

* **Acreditar na Estabilidade da Volatilidade:** Tratar $\sigma$ como uma constante permanente e não como uma variável propensa a saltos e mudanças de regime leva a subestimar gravemente o risco de cauda.
* **Interpretar Saída de Túnel como Sinal Direcional de Trading:** Tratar o rompimento das bandas do túnel como um indicador automático de compra/venda, quando na realidade reflete uma quebra no modelo de ruído subjacente.
* **Ignorar Ajustes de Convexidade no Drift:** Omitir o termo $-\frac{1}{2}\sigma^2$ ao simular retornos logarítmicos introduz viés na média dos preços gerados pela simulação de Monte Carlo.
* **Confiar Apenas na Variância para Monitorar Riscos:** Utilizar unicamente a volatilidade realizada e desconsiderar a alteração da forma da distribuição (capturada pela divergência KL) impede a identificação de mudanças estruturais nas caudas do mercado.

---

### Lab Prático Sugerido em Python

O laboratório prático consiste na implementação de um ambiente modular de simulação de GBM e monitoramento de regime dividido nas quatro etapas descritas a seguir.

#### Passo 1 Construção da Classe de Túnel GBM (`GBMTunnel`)
* Crie uma classe contendo os atributos $S_0$, $\mu$, $\sigma_{model}$ e $\Delta t$.
* Desenvolva o método `simulate_path(n_steps, sigma_true, jumps, seed)` para gerar trajetórias permitindo:
  * Mudança dinâmica na volatilidade real (`sigma_true`).
  * Introdução de saltos pontuais (`jumps`) mapeados em dicionário `{passo: valor_salto}`.
* Desenvolva o método `tunnel_bounds(n_steps, z)` que calcula os limites inferior e superior do túnel para todos os passos $t$.

#### Passo 2 Implementação do Termômetro de Volatilidade Realizada Rolante
* Escreva uma função `realized_vol(log_returns, window, dt)` que calcula a variação amostral (`ddof=1`) dos retornos logarítmicos em uma janela móvel e normaliza o valor dividindo por $\Delta t$.
* Calcule a razão $\frac{RV}{\sigma_{model}}$ e plote em relação ao nível $1,0$.

#### Passo 3 Implementação da Divergência KL Rolante
* Crie a função auxiliar `_kl_from_counts` aplicando a fórmula com constante de suavização $\epsilon = 10^{-12}$.
* Crie a função `rolling_kl(x, window, step, bins)` para dividir a série temporal de retornos em duas janelas adjacentes de tamanho `window`, criar histogramas comparativos e calcular a divergência temporal.

#### Passo 4 Implementação do Detector CUSUM de Variância
* Projete a função `cusum_variance(r2, baseline, h)` que acumula os desvios dos retornos ao quadrado ($r^2$) frente a uma linha de base (`baseline`).
* Defina o limite de alarme $h = 8 \times \text{baseline}$ para registrar disparos de alertas de mudança de volatilidade.

---

### Glossário

* **CUSUM de Variância:** Algoritmo estatístico de soma acumulada projetado para detectar desvios persistentes e mudanças de regime na variância de uma série temporal em relação a um patamar de referência.
* **Divergência de Kullback-Leibler (KL):** Medida de quão diferente uma distribuição de probabilidade é em relação a outra distribuição de referência.
* **Drift ($\mu$):** Taxa de retorno esperada ou tendência determinística média de valorização/desvalorização do preço de um ativo no tempo.
* **Gregas de Opções:** Medidas de sensibilidade do preço de um derivativo em relação a parâmetros subjacentes (Delta para preço, Gamma para variação do Delta, Theta para tempo, Vega para volatilidade).
* **Movimento Browniano Geométrico (GBM):** Processo estocástico em tempo contínuo no qual o logaritmo da variável aleatória segue um Movimento Browniano padrão com *drift*.
* **Quebra de Regime (*Regime Break*):** Mudança estrutural abrupta nas propriedades estatísticas subjacentes do mercado (como um aumento repentino de volatilidade ou presença de saltos).
* **Volatilidade Realizada (RV):** Desvio padrão amostral dos retornos efetivamente observados em uma janela móvel histórica, anualizado pelo fator $\Delta t$.

---

### Questões Práticas

#### Nível 1 Básico

##### Questão 1
Qual é o papel do parâmetro de volatilidade ($\sigma$) na definição do túnel do Movimento Browniano Geométrico?

###### Resposta
A volatilidade $\sigma$ atua como o parâmetro de escala dos choques gaussianos, definindo visualmente a velocidade de abertura do túnel de incerteza do preço ao longo do tempo.

---

##### Questão 2
O que indica o rompimento das bandas de um túnel GBM por uma trajetória real de preço?

###### Resposta
Indica um sinal de quebra de regime do mercado (alteração na volatilidade real ou ocorrência de um salto), sinalizando que o modelo de parâmetro constante deixou de ser válido.

---

##### Questão 3
Por que subtraímos $\frac{1}{2}\sigma^2$ da taxa de tendência $\mu$ no cálculo do retorno logarítmico do GBM?

###### Resposta
A subtração de $\frac{1}{2}\sigma^2$ é uma correção de convexidade (derivada do Lema de Itô) necessária para garantir que a média da distribuição do nível de preços $S_t$ corresponda à taxa de crescimento $\mu$.

---

#### Nível 2 Intermediário

##### Questão 1
Explique a mecânica do detector CUSUM de variância e descreva como ele identifica compressões ou expansões de volatilidade.

###### Resposta
O CUSUM de variância subtrai um nível de variância base (`baseline`) dos retornos ao quadrado ($r^2_i$). Ele mantém dois acumuladores: $g_{pos}$ para somar desvios positivos (expansões de volatilidade) e $g_{neg}$ para desvios negativos (compressões). Quando a soma acumulada de desvios ultrapassa um limite limiar pré-definido $h$, o algoritmo sinaliza um alarme de transição e reinicia os acumuladores para zero.

---

##### Questão 2
Um ativo com $S_0 = 100$, $\mu = 0,0$, $\sigma = 0,30$ é simulado em um passo de tempo $\Delta t = 0,01$. Se o choque gaussiano sorteado for $Z = -2,0$, qual será o retorno logarítmico e o preço resultante $S_1$?

###### Resposta
1. Cálculo do termo de *drift*:

$$\text{drift} = \left(0,0 - 0,5 \times 0,30^2\right) \times 0,01 = -0,045 \times 0,01 = -0,00045$$

2. Cálculo do termo de difusão:

$$\text{diff} = 0,30 \times \sqrt{0,01} \times (-2,0) = 0,30 \times 0,1 \times (-2,0) = -0,06$$

3. Retorno logarítmico:

$$\text{lnret}_1 = -0,00045 - 0,06 = -0,06045$$

4. Preço $S_1$:

$$S_1 = 100 \times \exp(-0,06045) \approx 100 \times 0,94134 = 94,13$$

---

#### Nível 3 Avançado

##### Questão 1
Analise a relação funcional entre o túnel de incerteza do GBM e as Gregas de uma opção. Como uma alteração abrupta na estrutura de choque do mercado afeta simultaneamente o sensor de Divergência KL e a grega Vega de um portfólio?

###### Resposta
As Gregas operam como medidores de sensibilidade diretamente acoplados ao túnel de probabilidades desenhado pelo GBM. A grega Vega mede a sensibilidade do preço de uma opção em relação à largura desse túnel ($\sigma$). 

Quando o mercado sofre uma mudança abrupta de regime — como o surgimento de caudas pesadas ou um salto discreto —, a distribuição empírica de retornos sofre mutação. A Divergência KL rolante detecta esse fenômeno ao comparar a janela recente com a anterior, apresentando uma elevação pronunciada na sua métrica ao identificar que a estrutura do ruído mudou. 

Simultaneamente, como a volatilidade implícita do mercado tende a se expandir para precificar a nova incerteza e a abertura mais rápida do túnel, o risco associado ao Vega do portfólio sofre um impacto direto, exigindo a recalibragem da largura do túnel ($\sigma_{model}$) para restabelecer a precisão do hedge de opções.