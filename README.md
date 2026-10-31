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

Cada módulo tem: `lessons/` · `study/` · `labs/` (quando existir).

Detalhes: [`docs/curriculum.md`](docs/curriculum.md) · [`docs/trilhas.md`](docs/trilhas.md) · [`docs/COURSE_STRUCTURE.md`](docs/COURSE_STRUCTURE.md) · [`docs/mapa-aulas.md`](docs/mapa-aulas.md)

## Mapa dos módulos

| # | Módulo | Conteúdo | Lab |
|---|--------|----------|-----|
| [M01](modules/M01-fundamentos) | Fundamentos | 5 aulas + study | **Lab 01 vendedor sem hedge** |
| [M02](modules/M02-dinamica-gregas) | Dinâmica e gregas | 3 aulas + study | **Lab 01 GBM + Manim** |
| [M03](modules/M03-curva-juros) | Curva de juros | 3 aulas + study | — |
| [M04](modules/M04-superficie-vol) | Superfície de vol | 6 aulas + study | — |
| [M05](modules/M05-econofisica-entropia) | Entropia e risco | 4 aulas + study | — |
| [M06](modules/M06-histerese-caudas) | Histerese e caudas | 2 aulas + study | — |
| [M07](modules/M07-portfolio-fatores) | Portfólio | 4 aulas + study | — |
| [M08](modules/M08-variancia-garch) | GARCH | 1 aula + study | — |
| [M09](modules/M09-labs-beta-fragilidade) | Beta / R+/R− | 2 aulas + study | — |
| [M10](modules/M10-capstone-janus) | Capstone Janus | 2 aulas + study | — |

## Começar agora

Índice de labs: [`docs/LABS.md`](docs/LABS.md)

### Setup

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,manim]"   # pacote instalável — sem PYTHONPATH
# fallback: pip install -r requirements.txt && pip install -e .
pytest -q
```

### 1) M01 — Vendedor sem hedge (*wait-and-see*)

```bash
python modules/M01-fundamentos/labs/01-vendedor-sem-hedge/run_lab.py --plot
# sim.npz gerado → Manim reutiliza (ou simula de novo se ausente)
manim -pql modules/M01-fundamentos/labs/01-vendedor-sem-hedge/manim/scenes.py NakedSellerPnLScene
```

### 2) M02 — GBM + convergência Monte Carlo

```bash
python modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo/run_lab.py --plot
manim -pql modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo/manim/scenes.py DensityConvergenceScene
```

## Estrutura do repositório

```text
econofisica/
├── docs/                       # curriculum, trilhas, mapa
├── modules/M0X-.../
│   ├── lessons/                # 32 aulas (markdown)
│   ├── study/                  # overview · resumo · guia
│   └── labs/…/manim/           # animações reproduzíveis
├── src/econofisica/            # biblioteca compartilhada
├── scripts/import_course_from_vault.py
└── NOTICE.md                   # proveniência educacional
```

> Mídia pesada do vault (podcast/vídeo/slides ~1.3 GB) **não** entra no Git — preferimos Manim gerado a partir dos labs.

## Princípios

- **Teoria → código → validação.** Todo lab compara resultado empírico com solução fechada (quando existir).
- **Reproduzível.** Seeds fixas; parâmetros explícitos; sem magic numbers escondidos.
- **Incremental.** Cada lab reutiliza funções do `src/` em vez de copiar pasta.
- **Aberto.** MIT — use, adapte, ensine.

## Contribuir

Issues e PRs são bem-vindos: novos labs, correções de notação, melhorias de didática. Veja [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Licença

[MIT](LICENSE) © Matheus Cardoso (@mosscardoso)
