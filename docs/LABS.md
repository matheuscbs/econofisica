# Índice de labs

Cada lab vive em `modules/M0X-…/labs/<nn>-<slug>/` com:

| Arquivo | Papel |
|---------|--------|
| `README.md` | enunciado, fórmulas, como rodar |
| `run_lab.py` | simulação + relatório |
| `RESULTS.md` | como ler a saída |
| `manim/` | animações (quando existir) |

Código reutilizável → `src/econofisica/`.

## Labs ativos

| Módulo | Lab | Ideia-chave | Aula |
|--------|-----|-------------|------|
| [M01](../modules/M01-fundamentos) | [01 — Vendedor sem hedge](../modules/M01-fundamentos/labs/01-vendedor-sem-hedge) | Call vendida *naked*: cauda de perdas | M01.A02–A03 |
| [M02](../modules/M02-dinamica-gregas) | [01 — GBM Monte Carlo](../modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo) | Momentos teóricos + convergência MC | M02.A01 |

## Ordem sugerida de execução

```text
M01 Lab 01  →  por que wait-and-see quebra
M02 Lab 01  →  o motor GBM por baixo
(próximo)   →  delta hedge dinâmico / BSM
```

## Convenção ao criar um lab novo

1. Pasta `labs/NN-slug-kebab/`
2. **SoT de parâmetros** em `src/econofisica/labs/<slug>.py` (`@dataclass` frozen)
3. Importar de `src/econofisica` (não copiar GBM); preferir `simulate_gbm_terminal` quando só precisar de \(S_T\)
4. `run_lab.py` salva `sim.npz` via `save_lab_npz`; Manim lê com `resolve_artifact_path` / `ECONOFISICA_ARTIFACT`
5. `--plot` para PNG em `outputs/`
6. Manim opcional, sem depender de LaTeX local
7. Testes golden em `tests/` para fórmulas novas
8. Linkar no README do módulo + neste índice
9. Setup do aluno: `pip install -e .` (bootstrap de `src/` só como fallback)
