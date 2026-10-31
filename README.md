# Econofísica — @mosscardoso

Curso open-source de **econofísica aplicada a mercados**: do modelo de preço ao risco de regime, com labs em Python.

**Autor:** [@mosscardoso](https://instagram.com/mosscardoso) · [matheuscbs](https://github.com/matheuscbs)  
**Repo:** [github.com/matheuscbs/econofisica](https://github.com/matheuscbs/econofisica)

> Material educacional. Não é recomendação de investimento.

## Por que este curso

Mercados não são só “previsão de preço”. São sistemas com leis efetivas: difusão, entropia, histerese, variância que propaga e resposta assinada ao risco. Este repositório é a **referência prática** — teoria curta, código legível, labs que você roda e valida.

## Como estudar

| Perfil | Ordem sugerida |
|--------|----------------|
| **Trader** | M01 → M02 → M05 → M06 → M08 → M09 → M10 |
| **Quant** | M01 → M04 → M08 → M09 → M10 (M05–M07 em paralelo) |
| **Risco** | M05 → M06 → M07 → M08 → M09 → M10 |

Cada módulo tem: pergunta-guia · conceitos · labs · leituras.

Detalhes: [`docs/curriculum.md`](docs/curriculum.md) · [`docs/trilhas.md`](docs/trilhas.md)

## Mapa dos módulos

| # | Módulo | Status |
|---|--------|--------|
| [M01](modules/M01-fundamentos) | Fundamentos: preço mínimo, delta, Itô, risco-neutro | roadmap |
| [M02](modules/M02-dinamica-gregas) | Dinâmica, gregas e path dependence | **Lab 01 ativo** |
| [M03](modules/M03-curva-juros) | Curva de juros e produtos de taxa | roadmap |
| [M04](modules/M04-superficie-vol) | Superfície de vol e modelos de smile | roadmap |
| [M05](modules/M05-econofisica-entropia) | Econofísica: informação, entropia e risco | roadmap |
| [M06](modules/M06-histerese-caudas) | Histerese, caudas e previsibilidade | roadmap |
| [M07](modules/M07-portfolio-fatores) | Portfólio: Markowitz → fatores | roadmap |
| [M08](modules/M08-variancia-garch) | Variância que propaga (ARCH/GARCH) | roadmap |
| [M09](modules/M09-labs-beta-fragilidade) | Labs: beta operacional e R+/R− | roadmap |
| [M10](modules/M10-capstone-janus) | Capstone: regimes frágil/antifrágil | roadmap |

## Começar agora — Lab 01 (GBM + Monte Carlo)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo/run_lab.py
```

Você vai:
1. Calcular média/variância teóricas do log-preço e de \(S_T\)
2. Avaliar a densidade log-normal
3. Simular trajetórias discretas do GBM
4. Validar convergência Monte Carlo para \(N \in \{10^3, 10^4, 10^5\}\)

Guia: [`modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo`](modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo)

## Estrutura do repositório

```text
econofisica/
├── docs/                  # curriculum, trilhas, glossário
├── modules/M0X-.../       # teoria + labs por módulo
├── src/econofisica/       # biblioteca compartilhada (cresce com os labs)
├── notebooks/             # notebooks opcionais de exploração
├── requirements.txt
└── README.md
```

## Princípios

- **Teoria → código → validação.** Todo lab compara resultado empírico com solução fechada (quando existir).
- **Reproduzível.** Seeds fixas; parâmetros explícitos; sem magic numbers escondidos.
- **Incremental.** Cada lab reutiliza funções do `src/` em vez de copiar pasta.
- **Aberto.** MIT — use, adapte, ensine.

## Contribuir

Issues e PRs são bem-vindos: novos labs, correções de notação, melhorias de didática. Veja [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Licença

[MIT](LICENSE) © Matheus Cardoso (@mosscardoso)
