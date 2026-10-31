<!-- course map -->
# Econofísica Aplicada a Mercados & Trading — Resumo

> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)
> **Módulo:** CURSO

> **Marca pública:** [@mosscardoso](https://instagram.com/mosscardoso) · repo [matheuscbs/econofisica](https://github.com/matheuscbs/econofisica)  
> Pesquisa privada de apoio a partir de fonte histórica: Karim Khemiri / Khem Kapital (`@mosscardoso (curso) / fonte histórica @khemkapital`). Uso educacional / não comercial. Não republicar conteúdo proprietário dos repos de terceiros.

## O que é
Grade de estudo (32 lições em 10 módulos) que liga engenharia financeira → econofísica → labs de beta, fragilidade e alocação Janus. Cada aula tem conceito, aplicação de mercado, lab e fonte mapeada.

## Promessa
Sair capaz de (1) precificar/hedgear com BSM, gregas, vol surface e taxa; (2) ler risco com entropia, histerese, Lyapunov e GARCH; (3) operar labs de beta estacionário, R+/R− e Janus por regime.

## Fontes-mestras
| Repo | Papel |
|------|-------|
| `quantitative-trading-free-lesson` | Trilha 01–28 |
| `Beta-and-trading-environement` | Lab beta |
| `Fragile-Antifragile-Regime-Classifier` | Lab R+/R− |
| `janus-anti-fragility-strategy` | Capstone Janus |

## Mapa rápido

### M01 — Fundamentos: preço mínimo, delta, Itô e mundo risco-neutro

**Pergunta:** Como precificar e fazer hedge de opções vanila sem “adivinhar” o drift?

- M01.A01 — Mapa do curso: de precificação a alocação por regime
- M01.A02 — Preço mínimo de uma opção: o que o mercado não pode deixar de pagar
- M01.A03 — Delta neutro: transformar opinião direcional em risco controlado
- M01.A04 — Lema de Itô: por que o hedge contínuo gera um termo extra de variância
- M01.A05 — Mundo risco-neutro e Black–Scholes: precificar sem prever o drift

### M02 — Dinâmica, gregas e path dependence

**Pergunta:** Como a dinâmica do spot e as gregas mudam o P&L do livro?

- M02.A01 — Movimento browniano geométrico: o modelo padrão de trajetória de preço
- M02.A02 — Gregas: o painel de risco do livro de opções
- M02.A03 — Opções exóticas e dependência de trajetória: quando o caminho importa

### M03 — Curva de juros e produtos de taxa

**Pergunta:** Como montar curva de juros e precificar taxa sem arbitragem?

- M03.A01 — Taxas forward sem arbitragem: construir a curva a partir do mercado
- M03.A02 — Swaps de juros: precificar o instrumento padrão de taxa
- M03.A03 — De forwards a opções de taxa: onde entra a volatilidade

### M04 — Superfície de vol e modelos de smile

**Pergunta:** Como ler, sanitizar e modelar a superfície de volatilidade?

- M04.A01 — Superfície de volatilidade: expiry, tenor e convenções de mercado
- M04.A02 — Construção livre de arbitragem da superfície
- M04.A03 — De volatilidade implícita a volatilidade local
- M04.A04 — Heston e Monte Carlo: origem do smile com vol estocástica
- M04.A05 — Saltos (jump-diffusion): quando a continuidade do GBM falha
- M04.A06 — Smile FX: sticky strike vs sticky delta na prática

### M05 — Econofísica: informação, entropia e risco

**Pergunta:** O que a econofísica muda na leitura de incerteza e risco?

- M05.A01 — Introdução à econofísica: difusão, calor e o PDE de BSM
- M05.A02 — Teoria da informação e entropia: medir incerteza de retornos
- M05.A03 — Entropia e “temperatura” de mercado: do microestado ao regime
- M05.A04 — Risco como força: drawdown, correlação e o crash

### M06 — Histerese, caudas e previsibilidade

**Pergunta:** Por que trajetória e caos importam no drawdown e na previsibilidade?

- M06.A01 — Histerese e dependência de trajetória no risco de cauda
- M06.A02 — Expoente de Lyapunov: sensibilidade a condições iniciais no trading

### M07 — Portfólio: da geometria Markowitz aos fatores

**Pergunta:** Como alocar além do μ ingênuo e do “alpha” ilusório?

- M07.A01 — Markowitz: geometria risco–retorno e a fronteira eficiente
- M07.A02 — CAPM: o que o mercado paga (e o que não paga)
- M07.A03 — Black–Litterman: views explícitas no lugar de μ solto
- M07.A04 — APT e multifatores: quando “alpha” era beta que faltava

### M08 — Variância que propaga (ponte aos labs)

**Pergunta:** Como a variância propaga e prepara regras de regime?

- M08.A01 — ARCH/GARCH: a variância não some — ela propaga

### M09 — Labs de pesquisa: beta operacional e R+/R−

**Pergunta:** Como transformar beta e fragilidade em regras operacionais?

- M09.A01 — Lab — Beta operacional selecionado pelo ambiente de trading
- M09.A02 — Lab — Classificador determinístico frágil (R+) vs antifrágil (R−)

### M10 — Capstone: sistema frágil/antifrágil com regimes (Janus)

**Pergunta:** Como construir alocação frágil/antifrágil com consciência de regime?

- M10.A01 — Capstone — Lei assinada de resposta à variância (Janus)
- M10.A02 — Capstone — Alocação defasada, hedge e variedade necessária

## Trilhas
| Perfil | Ordem |
|--------|-------|
| Trader | M01 → M02 → M05 → M06 → M08 → M09 → M10 |
| Quant | M01→M04 → M08 → M09 → M10 (M05–M07 paralelo) |
| Risco | M05 → M06 → M07 → M08 → M09 → M10 |

## Pasta
- `00-resumo.md` — este arquivo
- `curso-completo-v2.md` — grade inteira
- `aulas/` — uma nota por lição
- `modulos/` — uma nota por módulo

Tags: #econofisica #trading #khemkapital #pesquisa