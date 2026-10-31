"""Persistência leve de resultados de lab (npz) — reuse Manim / plots."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np


def save_lab_npz(path: Path | str, **arrays: Any) -> Path:
    """Salva arrays nomeados em .npz comprimido."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out, **arrays)
    return out


def load_lab_npz(path: Path | str) -> dict[str, np.ndarray]:
    """Carrega .npz → dict de arrays (cópia em memória)."""
    data = np.load(Path(path), allow_pickle=False)
    return {k: data[k] for k in data.files}


def resolve_artifact_path(
    default: Path | str | None = None,
    env_var: str = "ECONOFISICA_ARTIFACT",
) -> Path | None:
    """Prioridade: env ECONOFISICA_ARTIFACT → default se existir."""
    import os

    env = os.environ.get(env_var)
    if env:
        p = Path(env)
        return p if p.is_file() else None
    if default is None:
        return None
    p = Path(default)
    return p if p.is_file() else None
