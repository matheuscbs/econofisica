<!-- imported study note (resumo.md) -->
# Documento de Briefing: Módulo M06 – Histerese, Caudas e Previsibilidade

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** M06

↑ M06 · Resumo · Completo

Este documento de briefing fornece uma síntese exaustiva e estruturada do Módulo M06 do curso de Econofísica Khem Kapital. A análise aborda formalismos matemáticos, dinâmicas de microestrutura de mercado, dependência temporal de longa memória, testes estatísticos de independência e modelos computacionais de histerese.

---

## Resumo Executivo

O Módulo M06 dedica-se ao estudo de sistemas econômico-financeiros fora do equilíbrio, focando na transição entre dinâmicas microscópicas e propriedades macroscópicas emergentes. O núcleo conceitual do módulo articula-se em três eixos centrais:

1. **Caudas e Autoexcitação**: Processos de ponto estocásticos autorregressivos (processos de Hawkes) que capturam o agrupamento de volatilidade (*volatility clustering*), a memória longa no fluxo de ordens e a reflexividade endógena dos mercados financeiros.
2. **Histerese e Dependência do Trajeto**: Fenômenos em que o estado atual de um sistema depende do seu histórico funcional, exemplificados pela modelagem da utilidade e aceitação de transações via modelos de Preisach.
3. **Previsibilidade e Testes de Independência**: A detecção de dependências não lineares e quebras estruturais em séries temporais de alta frequência utilizando o teste não paramétrico BDS em regimes recursivos.

A premissa fundamental do módulo é que os mercados modernos não são guiados prioritariamente por um fluxo contínuo de informações exógenas, mas sim por mecanismos internos de retroalimentação (endogenia). Sob certas condições críticas, as interações entre agentes geram cascatas de eventos descritas por distribuições de cauda pesada (leis de potência), exigindo métodos estatísticos e econométricos não paramétricos para estimar parâmetros de impacto, execução ótima e estabilidade de mercado.

---

## Análise Detalhada dos Temas Principais

### Processos de Hawkes, Autoexcitação e Caudas Pesadas

Os processos de Hawkes constituem uma classe de processos de ponto multivariados autorregressivos caracterizados por um vetor de intensidade estocástica $\lambda_t = \{\lambda_i(t)\}_{i=1}^D$. A probabilidade condicional de ocorrência de um evento no intervalo imediato $[t, t+\Delta t)$ é dada por:

$$\lambda_i(t) = \mu_i + \sum_{j=1}^D \int_0^t \phi_{ij}(t - t') dN_j(t')$$

Onde $\mu_i$ representa a taxa de intensidade exógena (eventos decorrentes de informações externas ao sistema) e $\Phi(t) = \{\phi_{ij}(t)\}_{i,j=1}^D$ é a matriz de núcleos de interação (*kernels*), que satisfaz as condições de causalidade, positividade e integrabilidade $L^1$.

```
[Fluxo Exógeno μ_i] ───────┐
                           ▼
[Eventos Passados dN_j] ──► ( Convolução com Kernel Φ_ij(t-t') ) ──► [Intensidade Estocástica λ_i(t)]
```

#### Condição de Estacionariedade e Representação em Ramificação
A estabilidade e estacionariedade assintótica dos incrementos do processo de Hawkes são governadas pelo raio espectral da matriz $\|\Phi\| = \{\|\phi_{ij}\|\}_{i,j=1}^D$, onde $\|\phi_{ij}\| = \int_0^\infty \phi_{ij}(t) dt$.
* **Regime Subcrítico** ($\|\Phi\| < 1$): O processo possui incrementos estacionários. A taxa média de eventos é finita e expressa por $\Lambda = (I - \hat{\Phi}(0))^{-1} \mu$. Na representação de agrupamento (*cluster representation* ou árvore de Galton-Watson), cada evento exógeno ("imigrante") gera em média $\|\Phi\|$ descendentes diretos.
* **Regime Crítico ou Quasestacionário** ($\|\Phi\| = 1$): A probabilidade de extinção das cascatas permanece unitária, mas o tamanho médio das ramificações diverge.
* **Regime Supercrítico** ($\|\Phi\| > 1$): A taxa média de eventos cresce exponencialmente com o tempo, gerando cascatas fora de controle.

#### Núcleos Exponenciais versus Leis de Potência
A escolha da funcionalidade do núcleo $\Phi(t)$ é crítica para a representação do sistema:
* **Núcleo Exponencial**: $\phi(t) = \alpha \beta e^{-\beta t}$. Possui a propriedade de Markov, permitindo que o par $(N_t, \lambda_t)$ seja representado na forma diferencial $d\lambda_t = -\beta \lambda_t dt + \alpha \beta dN_t$.
* **Núcleo em Lei de Potência**: $\Phi(t) = \frac{\alpha \beta}{(1 + \beta t)^{1 + \gamma}}$. É indispensável para capturar a memória longa observada empiricamente em dados financeiros de alta frequência. O expoente de cauda $\gamma \in (0, 0,5)$ induz autocorrelações algébricas no fluxo de ordens $c(t) \sim t^{-\gamma-1}$ ou $c(t) \sim t^{2\gamma-1}$, gerando comportamento de dependência de longo alcance e expoentes de Hurst aparentes $H = 1/2 + \gamma$.

---

### Medição da Endogenia e Reflexividade de Mercado

A aplicação de processos de Hawkes para quantificar a fração de flutuações endógenas nos preços originou o conceito de **reflexividade de mercado**. O parâmetro $\|\Phi\|$, interpretado como a taxa de ramificação (*branching ratio*), define a proporção de eventos disparados por retroalimentação interna:

$$\text{Grau de Reflexividade} = \frac{\text{Taxa Endógena}}{\text{Taxa Total}} = \|\Phi\|$$

#### O Debate sobre a Criticalidade dos Mercados
* **Filimonov e Sornette**: Utilizando parametrizações exponenciais no contrato futuro E-mini S&P 500 (1998–2010), argumentaram que a reflexividade havia crescido dramaticamente de $70\%$ para mais de $90\%$, associando esse aumento à expansão do trading algorítmico e de alta frequência (HFT).
* **Hardiman, Bercot e Bouchaud**: Demonstraram que ajustes paramétricos baseados em núcleos exponenciais introduzem severos viéses quando aplicados a dados com decaimento lento. Ao utilizarem métodos não paramétricos e parametrizações de lei de potência, provaram que a reflexividade dos mercados financeiros manteve-se **estável e criticamente próxima da instabilidade** ($\|\Phi\| \approx 1$) ao longo de décadas.
* **Estimador Livre de Modelo**: Hardiman e Bouchaud propuseram uma aproximação não paramétrica simples baseada na relação estatística de segundo ordem no domínio da frequência para $z=0$:

$$\|\Phi\| \approx 1 - \left( \frac{V[N_T]}{E[N_T]} \right)^{1/2}$$

Para um processo de Poisson puro (sem dependência), a variância é igual à média ($V[N_T] = E[N_T]$), resultando em $\|\Phi\| = 0$. À medida que o reagrupamento de eventos aumenta a variância em relação à média, $\|\Phi\|$ aproxima-se de $1$.

---

### Histerese e Modelagem de Utilidade do Trabalhador

O conceito de histerese descreve sistemas cujos estados internos exibem memória não volátil e irreversibilidade local em relação às forças externas. No contexto dos mercados de trabalho sob demanda (*gig economy*), a utilidade e a disposição do trabalhador em aceitar uma transação/corrida são modeladas via o **Modelo de Preisach**.

#### Desafios Computacionais e Inconsistência de Modelos
Ao prever a probabilidade de aceitação $P(\text{accept})$ sob efeitos de histerese, a arquitetura preditiva utilizada desempenha um papel determinante na estabilidade matemática:

```
[Entradas de Mercado e Histórico]
               │
               ├─────────────────────────────────────────┐
               ▼                                         ▼
   [Arquitetura XGBoost v1]                   [Rede Neural Dual v2]
(Regressores Independentes)                 (Saída Vetorial Unificada)
               │                                         │
               ▼                                         ▼
• Inconsistência Estrutural (desvio ≈ 1,02)   • Mantém Consistência Estrutural
• Razões r₀/r₁ Explodem                        • Estimativa Estável de P(accept)
• Curvas de Aceitação Degeneradas
```

* **Regressores XGBoost Independentes (v1)**: Produzem lacunas estruturalmente inconsistentes (desvio padrão $std \approx 1,02$). Como as redes preditivas não compartilham informações sobre suas estimativas mútuas, as feições de razão $r_0 / r_1$ explodem numericamente, levando o classificador subsequente a gerar curvas de probabilidade $P(\text{accept})$ degeneradas.
* **Rede Neural Dual de Saída Múltipla (v2)**: Modela simultaneamente os limiares de alternância da histerese, preservando a coerência estrutural dos dados e garantindo previsões funcionais estáveis.

---

### Previsibilidade, Testes Não Paramétricos e Quebras Estruturais

Para avaliar se uma série temporal financeira possui dinâmica i.i.d. (independente e identicamente distribuída) ou se apresenta dependências estocásticas não lineares e histerese, utiliza-se o **Teste BDS** (desenvolvido por Brock, Dechert e Scheinkman).

#### Teste BDS Recursivo para Quebras Estruturais
O teste BDS baseia-se na integral de correlação $C_m(\epsilon)$, medindo a frequência com que pares de pontos de uma série temporal em uma dimensão de imersão $m$ permanecem a uma distância inferior a $\epsilon$.
* **Aplicação Recursiva**: O teste BDS é aplicado de maneira contínua/recursiva sobre janelas móveis das séries temporais de retornos ou resíduos de modelos de filtragem.
* **Detecção de Eventos Críticos**: Permite identificar a emergência de não linearidades e quebras estruturais associadas a choque sistêmicos exógenos, como os impactos da pandemia de COVID-19 sobre os mercados acionários internacionais, sinalizando a perda temporária de eficiência do mercado e o aumento da imprevisibilidade.

---

### Microestrutura, Impacto de Mercado e Livro de Ofertas

A modelagem de alta frequência utiliza o formalismo de Hawkes para resolver os problemas de precificação, impacto de mercado de meta-ordens e dinâmica do livro de ofertas (*limit order book* - LOB).

#### Modelos de Preço e Ruído de Microestrutura
Bacry, Delattre, Hoffmann e Muzy introduziram o modelo de preço bivariado:

$$P_t = P_0 + N_1(t) - N_2(t)$$

Onde $N_1(t)$ e $N_2(t)$ representam os processos de contagem de saltos discretos de alta para cima e para baixo, respectivamente. O modelo assume uma estrutura puramente revertente à média ($\phi_{11} = \phi_{22} = 0$ e $\phi_{12} = \phi_{21} = \alpha \beta e^{-\beta t}$), sendo capaz de reproduzir analiticamente o gráfico de assinatura (*signature plot*) da variação quadrática $C(\tau)$ e o **Efeito Epps** (desaparecimento da correlação cruzada entre ativos em escalas de tempo infinitesimais).

```
Variação Quadrática C(τ)
  ▲
  │   *  Empírico
1.04│  /   --- Ajuste do Modelo
1.03│ /
1.02│/
    └────────────────────────► Escala de Tempo τ (segundos)
```

#### Impacto de Mercado e o Modelo HIM (Hawkes Impact Model)
O impacto de mercado de uma meta-ordem executada com taxa $r(t)$ no intervalo $[0, T]$ é decomposto pelo modelo HIM Impulsivo:

$$\lambda_1(t) = \mu + \phi^{(s)} * dN_2(t) + f(r(t)) \cdot \delta(t)$$

$$\lambda_2(t) = \mu + \phi^{(s)} * dN_1(t) + C \frac{\phi^{(s)}(t)}{\|\phi^{(s)}\|} f(r(t))$$

O parâmetro estocástico $C \in$ governa a resposta comportamental do mercado:
* $C = 0$: Ausência de reação contrária (herding puro), gerando impacto permanente elevado.
* $C = 1$: Reação contrária de mesma magnitude que a reação de rebanho, garantindo que o impacto convirja a zero no longo prazo (sem impacto permanente).
* $C \in (0,1)$: Decaimento de impacto seguindo uma lei de potência $t^{-(\gamma+1)}$, consistente com dados empíricos de corretoras.

#### Dinâmica do Livro de Ofertas (Nível-I e Completo)
* **Modelo Nível-I de 8 Dimensões (Bacry, Jaisson e Muzy)**: Classifica ordens de mercado ($T$), ordens limite ($L$) e cancelamentos ($C$) nas pontas de compra (*bid*) e venda (*ask*), além das mudanças no preço médio ($P$). O estudo revelou que os blocos de ordens normais são estritamente autorregulados (matriz diagonal de $K_n$), enquanto as mudanças de preço médio são governadas por interações antidiagonais (inibição e reversão imediata).
* **Execução Ótima (Hewlett; Alfonsi & Blanc)**: A inclusão do fluxo de Hawkes na otimização de liquidação impede estratégias de manipulação de preços quando a taxa de autoexcitação do processo compensa exatamente a resiliência/amortecimento natural do livro de ofertas.

---

## Citações Importantes e Análise de Contexto

### "On CME MDP3 the arrival process is strongly self-exciting: packets arrive in Hawkes-clustered bursts."
* **Origem**: Maciejewski (2026), *Packets, Transactions and Queues*.
* **Análise de Contexto**: O estudo demonstra que o agrupamento de pacotes nos feeds de dados de alta frequência (CME) não é um artefato da infraestrutura de rede, mas sim um reflexo direto da natureza autoexcitada do mecanismo de correspondência da bolsa. Os pacotes chegam em rajadas com grau de reflexividade próximo do nível crítico, exigindo que os sistemas HFT operem com threads dedicadas que processem cada mensagem dentro do período do publicador ($\approx 7,5\,\mu\text{s}$) para evitar filas na camada de recepção.

### "Accounting for this feature on their estimation of $\\Phi\$, Hardiman et al. found that the reflexivity of the E-mini S&P future hasn't been increasing during the last decade, but has remained constant at a value very close to the critical one $\\Phi\ = 1$."
* **Origem**: Bacry, Mastromatteo e Muzy (2015), revisando Hardiman, Bercot e Bouchaud (2013).
* **Análise de Contexto**: Esta citação refuta a hipótese simplista de que o crescimento do trading algorítmico aumentou a instabilidade estrutural dos mercados. Ela estabelece a invariância escalar do grau de reflexividade, demonstrando que os mercados operam em um estado "quase-crítico" autoorganizado, onde pequenas perturbações exógenas podem desencadear cascatas endógenas de grande escala (*flash crashes*).

### "Diagnostic comparison between XGBoost regressors (v1) and the dual-output NN (v2): XGBoost regressors produce structurally inconsistent gaps (std ≈ 1.02)... causing ratio features $r_0/r_1$ to explode."
* **Origem**: Estudo de Histerese em Gig Labour Markets (2026).
* **Análise de Contexto**: Evidencia a limitação dos algoritmos tradicionais baseadas em árvores de decisão para aprender dinâmicas que possuem estados ocultos e histerese. Quando dois modelos independentes tentam prever estados acoplados, a falta de restrição conjunta faz com que a relação espacial/temporal divirja, exigindo redes neurais de saída dupla para manter a consistência física/econômica do sistema.

---

## Insights Acionáveis e Conexão Integradora

### Conexão aos Outros Módulos do Curso

```
┌────────────────────────────────────────────────────────────────────────┐
│                      MÓDULO M06: ECONOFÍSICA                           │
│              Histerese, Caudas e Previsibilidade                       │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │                                │
                    ▼                                ▼
┌──────────────────────────────────────┐ ┌───────────────────────────────┐
│       Conexão a Módulos de           │ │    Conexão a Módulos de       │
│       Microestrutura e Risco         │ │   Execução e Algoritmos       │
├──────────────────────────────────────┤ ├───────────────────────────────┤
│ • Alimenta estresse de volatilidade  │ │ • Calibração de impacto HIM   │
│   via caudas pesadas de Hawkes.      │ │   para mineração de custos.    │
│ • Detecta instabilidade sistêmica    │ │ • Modelagem de histerese em   │
│   com teste não paramétrico BDS.     │ │   sistemas de decisão/trabalho│
└──────────────────────────────────────┘ └───────────────────────────────┘
```

1. **Conexão com Microestrutura e Risco Sistêmico**: A transição do modelo de agrupamento de volatilidade convencional para processos de Hawkes multivariados fornece o arcabouço para calibrar o risco de contágio entre ativos, conforme demonstrado por Aït-Sahalia no modelo *Mutually Exciting Jump-Diffusion*.
2. **Conexão com Algoritmos de Execução Ótima**: O parâmetro de resiliência $C$ do modelo HIM conecta-se diretamente aos modelos de impacto de mercado. Ignorar a natureza de lei de potência do núcleo de autoexcitação resulta em subestimar custos de liquidação de meta-ordens em até $40\%$.
3. **Conexão com Modelos Demanda/Oferta Não Lineares**: A integração dos testes BDS recursivos permite que estratégias quantitativas identifiquem em tempo real quando o mercado abandona o regime de passeio aleatório e entra em regimes de histerese endógena, ajustando o tamanho das posições (*position sizing*) para evitar eventos de cauda.

---

## Tabela Comparativa dos Modelos e Métodos Estudados

| Modelo / Método | Fundamentação Teórica | Aplicação / Achado Empírico Principal | Particularidade Matemática / Algorítmica |
| :--- | :--- | :--- | :--- |
| **Hawkes Paramétrico Exponencial** | Processo de Ponto Markoviano ($d\lambda_t = -\beta\lambda_t dt + \alpha\beta dN_t$) | Estimativa rápida de volatilidade e execução em alta frequência (Hewlett, Alfonsi). | Complexidade de verossimilhança $O(MD)$; superestima a taxa de decaimento no longo prazo. |
| **Hawkes Não Paramétrico (Wiener-Hopf)** | Inversão do sistema espectral $g(t) = \chi(t) + \chi(t) * g(t)$ | Captura precisa de núcleos em lei de potência $\Phi(t) \sim t^{-(1+\gamma)}$ em livros de oferta (Bacry & Muzy). | Admite valores de núcleos negativos (inibição); livre de viéses de parametrização. |
| **Estimador de Reflexividade Livre de Modelo** | Relação de correlação temporal para escala zero $z=0$ | Demonstração de que a reflexividade dos mercados é estável e crítica ($\|\Phi\| \approx 1$) (Hardiman & Bouchaud). | Baseado na razão variância/média: $\|\Phi\| \approx 1 - (V[N_T]/E[N_T])^{1/2}$. |
| **Modelo de Preisach (Histerese)** | Operadores de histerese elementares em sistemas com memória | Modelagem de utilidade e aceitação de transações na *Gig Economy*. | Requer Redes Neurais Doutoradas (Dual-Output) para evitar explosão das razões $r_0/r_1$. |
| **Teste BDS Recursivo** | Integral de correlação em espaço de fase $C_m(\epsilon)$ | Detecção não paramétrica de quebras estruturais e dependências não lineares (ex: choque COVID-19). | Avalia independência i.i.d. em resíduos sem preassumir distribuições específicas. |
| **Modelo HIM Impulsivo** | Preço acoplado ao fluxo de ordens com resposta delta de Dirac | Reprodução do decaimento de impacto de meta-ordens $t^{-(\gamma+1)}$ (Bacry et al.). | Parâmetro $C \in$ pondera a reação do mercado entre comportamento de rebanho e contrário. |