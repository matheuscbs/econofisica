# Manim — Lab M01.01 Vendedor sem hedge

```bash
pip install -e ".[manim]"
python modules/M01-fundamentos/labs/01-vendedor-sem-hedge/run_lab.py   # gera sim.npz

manim -pql modules/M01-fundamentos/labs/01-vendedor-sem-hedge/manim/scenes.py NakedSellerPnLScene
manim -pql modules/M01-fundamentos/labs/01-vendedor-sem-hedge/manim/scenes.py PathsByMoneynessScene
manim -pql modules/M01-fundamentos/labs/01-vendedor-sem-hedge/manim/scenes.py LabM01SellerFull
```

SoT: `econofisica.labs.M01_VENDEDOR`. Artifact: `outputs/lab-m01-vendedor-sem-hedge/sim.npz` (ou `ECONOFISICA_ARTIFACT`).

| Cena | Conteúdo |
|------|----------|
| `PathsByMoneynessScene` | Paths ITM vs OTM + strike |
| `NakedSellerPnLScene` | Histograma do P&L + marcações |
| `LabM01SellerFull` | Intro pedagógica curta |
