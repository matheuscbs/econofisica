# Manim — Lab M02.01 GBM

```bash
pip install -e ".[manim]"
python modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo/run_lab.py   # gera sim.npz

manim -pql modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo/manim/scenes.py GBMPathsScene
manim -pql modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo/manim/scenes.py DensityConvergenceScene
manim -pql modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo/manim/scenes.py MonteCarloConvergenceScene
manim -pql modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo/manim/scenes.py Lab01Full
```

SoT: `econofisica.labs.M02_GBM`. Density/convergência preferem `sim.npz` (S_T chunked) em vez de realocar 100k paths.

| Cena | O que mostra |
|------|----------------|
| `GBMPathsScene` | Paths + E[S_t] + túnel ±2σ (`sigma_wide`) |
| `DensityConvergenceScene` | Histograma S_T → pdf |
| `MonteCarloConvergenceScene` | Erro vs N + 1/√N |
| `Lab01Full` | Intro + fórmulas + teaser |
