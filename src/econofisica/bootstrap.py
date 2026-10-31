"""Fallback de import quando o pacote ainda não está instalado (pip install -e .)."""

from __future__ import annotations

import sys
from pathlib import Path


def ensure_src_on_path(start: Path | None = None) -> Path | None:
    """
    Se `econofisica` não importar, adiciona <repo>/src ao sys.path.

    Retorna o path de src adicionado, ou None se já havia pacote instalado.
    """
    try:
        import econofisica  # noqa: F401

        return None
    except ImportError:
        pass

    here = (start or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        src = candidate / "src"
        if (src / "econofisica").is_dir():
            sp = str(src)
            if sp not in sys.path:
                sys.path.insert(0, sp)
            return src
    return None
