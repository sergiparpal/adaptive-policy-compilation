"""
Registro de entorno para los JSON de resultados.

MOTIVO. Hasta el 7 de agosto de 2026 ningun registro guardaba con que codigo ni
con que interprete se habia producido. El desempate no determinista del voraz
—descubierto el 6 de agosto, cuando ya habia dos peldanos cerrados sobre el— es
exactamente el tipo de defecto que este modulo hace visible: dependia de
`PYTHONHASHSEED`, que ahora queda anotado en cada archivo.

QUE SE GUARDA, Y PARA QUE SIRVE CADA CAMPO

  recorded_at     cuando se produjo. Un registro re-corrido sin cambiar nada
                  mueve SOLO este campo: `git diff` sobre el resto es entonces
                  la comprobacion de que la cifra sigue reproduciendo.
  python          version del interprete.
  openai          version del SDK, o null si no esta instalado (los pasos que
                  no llaman a la API corren con la biblioteca estandar).
  platform        sistema y arquitectura.
  pythonhashseed  el valor de la variable de entorno. `null` significa SIN
                  FIJAR, es decir aleatorio: es informacion, no ausencia de
                  ella. Cualquier cifra sensible al orden de iteracion de un
                  set producida con `null` es sospechosa por construccion.
  git_commit      commit de HEAD, o null fuera de un repositorio.
  git_dirty       si el arbol tenia cambios sin confirmar. Con `true`, el
                  commit NO identifica el codigo que corrio; el digest si.
  code_digest     sha256 (16 hex) del codigo que produce las cifras: todos los
                  .py de harness/, peldano2/, peldano3/, peldano4/ y
                  run_experiment.py. Identifica el codigo aunque el arbol este
                  sucio o no haya git. `tests/` queda fuera a proposito:
                  cambiar una prueba no cambia ningun numero.

Este modulo no mide nada y no lo importa ninguna de las especificaciones
congeladas. Es metadato, y va bajo la clave `_env` para que se lea como tal.
"""

from __future__ import annotations

import hashlib
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent

# Codigo que produce cifras. El orden no importa: el digest ordena por ruta.
CODE_ROOTS = ("harness", "peldano2", "peldano3", "peldano4", "run_experiment.py")

DIGEST_CHARS = 16


def _openai_version() -> str | None:
    try:
        from importlib.metadata import version

        return version("openai")
    except Exception:
        return None


def _git(*args: str) -> str | None:
    """Salida de un git acotado al repo, o None si git no esta o falla."""
    try:
        p = subprocess.run(
            ("git", "-C", str(REPO), *args),
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return p.stdout.strip() if p.returncode == 0 else None


def _source_files() -> list[Path]:
    files: list[Path] = []
    for root in CODE_ROOTS:
        p = REPO / root
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            files.extend(f for f in p.rglob("*.py") if "__pycache__" not in f.parts)
    return sorted(files, key=lambda f: f.relative_to(REPO).as_posix())


def code_digest() -> str | None:
    """Huella del codigo fuente. Depende del contenido, no de git."""
    files = _source_files()
    if not files:
        return None
    h = hashlib.sha256()
    for f in files:
        h.update(f.relative_to(REPO).as_posix().encode())
        h.update(b"\0")
        h.update(f.read_bytes())
        h.update(b"\0")
    return h.hexdigest()[:DIGEST_CHARS]


def environment(**extra: Any) -> dict[str, Any]:
    """El bloque `_env` que acompana a cada JSON de resultados."""
    commit = _git("rev-parse", "HEAD")
    status = _git("status", "--porcelain")
    env: dict[str, Any] = {
        "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "python": platform.python_version(),
        "openai": _openai_version(),
        "platform": platform.platform(),
        "pythonhashseed": os.environ.get("PYTHONHASHSEED"),
        "git_commit": commit,
        "git_dirty": bool(status) if status is not None else None,
        "code_digest": code_digest(),
    }
    env.update(extra)
    return env


def describe() -> str:
    """Una linea legible, para imprimir al pie de un informe."""
    e = environment()
    seed = e["pythonhashseed"] or "sin fijar"
    dirty = "" if e["git_dirty"] is False else "+sucio"
    commit = (e["git_commit"] or "sin git")[:8]
    return (f"python {e['python']} · openai {e['openai'] or '—'} · "
            f"PYTHONHASHSEED {seed} · {commit}{dirty} · "
            f"codigo {e['code_digest']}")


if __name__ == "__main__":
    import json

    print(json.dumps(environment(), indent=2))
    print(describe(), file=sys.stderr)
