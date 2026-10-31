# Manim — Lab M01.01 Vendedor sem hedge

```bash
source .venv/bin/activate
export PYTHONPATH=src

manim -pql modules/M01-fundamentos/labs/01-vendedor-sem-hedge/manim/scenes.py NakedSellerPnLScene
manim -pql modules/M01-fundamentos/labs/01-vendedor-sem-hedge/manim/scenes.py PathsByMoneynessScene
manim -pql modules/M01-fundamentos/labs/01-vendedor-sem-hedge/manim/scenes.py LabM01SellerFull
```

| Cena | Conteúdo |
|------|----------|
| `PathsByMoneynessScene` | Paths ITM vs OTM + strike |
| `NakedSellerPnLScene` | Histograma do P&L + marcações |
| `LabM01SellerFull` | Intro pedagógica curta |
