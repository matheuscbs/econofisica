# Estrutura do curso

Layout pensado para estudar em ordem, achar labs rápido e gerar mídia reproduzível.

```text
econofisica/
├── README.md                 # porta de entrada
├── docs/
│   ├── curriculum.md         # grade M01–M10
│   ├── trilhas.md            # Trader / Quant / Risco
│   ├── mapa-aulas.md         # índice das 32 aulas
│   ├── curriculum-topics.csv
│   └── COURSE_STRUCTURE.md   # este arquivo
├── modules/
│   └── M0X-<slug>/
│       ├── README.md         # pergunta + links
│       ├── lessons/          # A01… An  (teoria)
│       ├── study/            # overview, resumo, guia
│       └── labs/
│           └── 01-.../
│               ├── README.md
│               ├── run_lab.py
│               └── manim/    # animações do lab
├── src/econofisica/          # biblioteca compartilhada
└── scripts/
    └── import_course_from_vault.py
```

## O que entra no Git

| Conteúdo | Sim? | Motivo |
|----------|------|--------|
| Markdown de aulas/estudo | sim | texto leve, versionável |
| Código dos labs + Manim | sim | núcleo do curso |
| CSV / curriculum | sim | mapa |
| mp4 / m4a / pptx / pdf do vault | **não** | ~1.3 GB; use Manim ou LFS depois |

## Fluxo de estudo por módulo

1. `README.md` do módulo — pergunta-guia  
2. `lessons/A0k-…md` — conceito + aplicação  
3. `study/resumo.md` — visão rápida  
4. `labs/…/run_lab.py` — validação numérica  
5. `labs/…/manim/` — animação do resultado  

## Reimportar do vault

```bash
python scripts/import_course_from_vault.py
```
