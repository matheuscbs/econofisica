# Contribuindo

Obrigado por ajudar o curso [@mosscardoso](https://instagram.com/mosscardoso) / [econofisica](https://github.com/matheuscbs/econofisica).

## Fluxo

1. Fork + branch a partir de `main` (`lab/m02-gbm`, `docs/curriculum`, …).
2. Um lab ou uma correção por PR.
3. Todo lab novo precisa de:
   - `README.md` com pergunta, fórmulas e como rodar
   - funções testáveis em `src/econofisica/` quando forem reutilizáveis
   - script `run_lab.py` (ou notebook + script) com saída reproduzível (`seed` fixa)
4. Não commitar `.venv/`, outputs grandes, dados proprietários ou chaves.

## Estilo de código

- Python 3.10+, type hints leves, docstrings curtas em PT ou EN (consistente no arquivo).
- Preferir NumPy vetorizado; evitar loops Python em caminhos quentes.
- Nomes de parâmetros financeiros padrão: `S0`, `mu`, `sigma`, `T`, `dt`.

## Escopo editorial

Este repo é **conteúdo original** de estudo prático. Não cole material proprietário de terceiros. Conceitos clássicos (GBM, BSM, GARCH…) são domínio público — a redação e o código devem ser nossos.
