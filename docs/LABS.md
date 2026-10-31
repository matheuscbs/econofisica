# Índice de labs

Cada lab vive em `modules/M0X-…/labs/<nn>-<slug>/` com:

| Arquivo | Papel |
|---------|--------|
| `README.md` | enunciado, fórmulas, como rodar |
| `run_lab.py` | simulação + relatório |
| `RESULTS.md` | como ler a saída |
| `manim/` | animações (quando existir) |

Código reutilizável → `src/econofisica/`. Config SoT → `src/econofisica/labs/`.

## Labs ativos

| Módulo | Lab | Ideia-chave | Aula |
|--------|-----|-------------|------|
| [M01](../modules/M01-fundamentos) | [01 — GBM Monte Carlo](../modules/M01-fundamentos/labs/01-gbm-monte-carlo) | Momentos teóricos + convergência MC | **M01.A02** |
| [M01](../modules/M01-fundamentos) | [02 — Vendedor sem hedge](../modules/M01-fundamentos/labs/02-vendedor-sem-hedge) | Call naked: cauda de perdas | **M01.A03** |

## Ordem sugerida de execução

```text
M01 Lab 01  →  motor GBM + validação MC          (A02)
M01 Lab 02  →  por que wait-and-see quebra       (A03)
M02 Lab …   →  túnel / sensores / gregas         (A01+)
```

## Convenção ao criar um lab novo

1. Pasta `labs/NN-slug-kebab/` alinhada à **lesson** do módulo  
2. SoT em `src/econofisica/labs/<slug>.py`  
3. Preferir `simulate_gbm_terminal` quando só precisar de \(S_T\)  
4. `sim.npz` + Manim opcional  
5. Testes golden em `tests/`  
6. Atualizar este índice + README do módulo  
