# Manim — Lab 01 GBM

Animações pedagógicas dos resultados da simulação.

## Setup

Na raiz do repo (Python ≥ 3.11 recomendado; aqui usamos 3.12):

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install manim   # ou: pip install -e ".[manim]"
```

Dependências de sistema: `ffmpeg`, `cairo` (já comuns via Homebrew).

## Render

```bash
source .venv/bin/activate
export PYTHONPATH=src

# preview rápido (480p)
manim -pql modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo/manim/scenes.py GBMPathsScene
manim -pql .../scenes.py DensityConvergenceScene
manim -pql .../scenes.py MonteCarloConvergenceScene
manim -pql .../scenes.py Lab01Full

# 1080p
manim -pqh modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo/manim/scenes.py Lab01Full
```

Saída padrão: `media/videos/...` (gitignored). Copie os mp4 finais para `outputs/lab01-gbm/manim/` se quiser arquivar localmente.

## Cenas

| Cena | O que mostra |
|------|----------------|
| `GBMPathsScene` | Paths + E[S_t] + túnel ±2σ (usa σ=0.20 p/ visual) |
| `DensityConvergenceScene` | Histograma S_T preenchendo a pdf (σ=0.02) |
| `MonteCarloConvergenceScene` | Erro vs N em log–log + 1/√N |
| `Lab01Full` | Intro + fórmulas + teaser de paths |
