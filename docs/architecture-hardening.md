# Architecture hardening (Evaluate → Improve)

Aplicado a partir do audit 2026-10-31.

| Item | Status |
|------|--------|
| LabConfig SoT (`src/econofisica/labs/`) | done |
| `simulate_gbm_terminal` + chunks | done |
| `sim.npz` artifact + Manim reuse | done |
| `pip install -e .` + bootstrap fallback | done |
| pytest golden (`tests/`) | done |

Não introduzimos filas, cache distribuído nem microserviços — só padrões já no repo.
