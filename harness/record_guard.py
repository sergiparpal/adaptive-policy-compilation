"""
Guard against overwriting the records that cannot be regenerated.

MOTIVE. Until August 8, 2026 `run_experiment.py llm` wrote `results/llm_run.json`
whatever `--n` it was given. So the cheap, recommended command of the
getting-started — `llm --n 100` — destroyed the 2000-case record that is the
input of rungs 3 and 4. And that record is not reproducible: it costs money and
the proposer is not deterministic at `temperature 0`, so a new run does not
give the same thing back.

The README already documented it and concluded that git was safeguard enough.
It is, after the fact and if you notice before committing on top. For this
particular case it is not.

WHAT IS GUARDED, AND WHAT IS DELIBERATELY NOT

  * GUARDED — the records that cost money and are not deterministic:
    `results/llm_run*.json` and `results2/llm_run2_*.json`. Losing them is
    irreversible.

  * NOT GUARDED — the deterministic, free figures (`frontier`,
    `subsumption_check`, `learned_subsumption`, `ceiling_check2`,
    `compare_runs`, `note_audit`). Re-running them IS the reproducibility check:
    that only `recorded_at` moves is the signal that everything still holds. A
    guard there would get in the way.

  * NOT GUARDED EITHER — `order_search`, `budget_and_balance` and `sweep`, whose
    re-run with a serious optimizer is planned. Blocking them would obstruct
    work that is already scheduled.

TWO DIFFERENT FAILURES, TWO CHECKS

  `refuse_overwrite` answers the DESTINATION: the file already exists and would
  be replaced. `refuse_shrink` answers the ARGUMENTS: `compare_runs` and
  `note_audit` rewrite their record with whatever they are passed, so invoking
  them with one file instead of with the glob shrinks it from 8 rows to 1
  without the destination changing at all.

DESIGN. Refuse by default and make no automatic copy: silent backups pile up and
people stop looking at them. The check runs at STARTUP, before spending a single
call — aborting after 632 calls would be worse than not guarding at all. And the
escape hatch is not called `--force`: it names what it does, so that it does not
get typed out of habit.

This module measures nothing and writes nothing. No frozen specification imports
it.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

FLAG = "--overwrite-record"


class RecordExists(Exception):
    """The destination is occupied, or the record would shrink.

    It carries the whole already-formatted message: whoever catches it prints
    it and leaves. It is raised instead of exiting so that the tests can
    exercise the guard without killing the process.
    """


# ---------------------------------------------------------------------------
# Reading what would be lost
# ---------------------------------------------------------------------------

def _load(path: Path) -> dict[str, Any] | None:
    """The record as a dict, or None if it cannot be read as such.

    An unreadable file is still a file that would be lost, so the failure does
    not disable the guard: it only degrades the description.
    """
    try:
        d = json.loads(path.read_text())
    except (OSError, ValueError):
        return None
    return d if isinstance(d, dict) else None


def _file_date(path: Path) -> str:
    try:
        ts = path.stat().st_mtime
    except OSError:
        return "?"
    return (datetime.fromtimestamp(ts, timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ"))


def describe(path: Path) -> list[str]:
    """What the file holds, as `label  value` lines.

    Read from the `_env` block and from the record's own metrics. The ten
    records that cost money still have no `_env` — precisely the ones this
    guard protects — so when it is missing the file's date is used, and it is
    said to be the file's date: an mtime is weaker evidence than a
    `recorded_at` and it must not pass for one.
    """
    d = _load(path)
    if d is None:
        return [("registrado", f"{_file_date(path)}  (fecha del fichero; "
                               f"no se pudo leer como JSON)")]

    env = d.get("_env") or {}
    lines: list[tuple[str, str]] = []

    if env.get("recorded_at"):
        lines.append(("registrado", str(env["recorded_at"])))
    else:
        lines.append(("registrado", f"{_file_date(path)}  (fecha del fichero; "
                                    f"no lleva bloque _env)"))

    if d.get("model"):
        lines.append(("modelo", str(d["model"])))

    # The number of cases is in three possible places depending on the rung and
    # on whether the record predates `_env`. The records themselves are the
    # last resort and the most reliable: there is one per case.
    n = env.get("n", d.get("n"))
    if n is None and isinstance(d.get("records"), list):
        n = len(d["records"])
    if n is not None:
        lines.append(("casos", str(n)))

    seed = env.get("seed", d.get("seed"))
    if seed is not None:
        lines.append(("semilla", str(seed)))
    if d.get("prompt_version"):
        lines.append(("prompt", str(d["prompt_version"])))

    metrics = d.get("metrics") or {}
    if isinstance(d.get("rules"), list):
        lines.append(("reglas", str(len(d["rules"]))))
    elif metrics.get("n_rules") is not None:
        lines.append(("reglas", str(metrics["n_rules"])))

    # What it cost to produce, which is the argument for not throwing it away.
    if metrics.get("llm_calls") is not None:
        lines.append(("llamadas al modelo", str(metrics["llm_calls"])))

    return lines


def _block(path: Path, lines: Sequence[tuple[str, str]]) -> list[str]:
    return [f"  {path}"] + [f"    {k:<20}{v}" for k, v in lines]


# ---------------------------------------------------------------------------
# The two checks
# ---------------------------------------------------------------------------

def refuse_overwrite(path: Path, *, overwrite: bool,
                     exits: Sequence[str] = ()) -> Path:
    """Abort if `path` exists, unless it was asked for on purpose.

    The guard is on the DESTINATION, not on the flag that chose it: `--out`
    pointing at an occupied file aborts just the same, otherwise it would be a
    way around this.
    """
    if overwrite or not path.exists():
        return path

    if path.is_dir():
        raise RecordExists(
            f"\nABORTADO: el destino existe y es un directorio.\n\n  {path}\n")

    detalle = "\n".join(_block(path, describe(path)))
    salidas = "\n".join(f"    {s}" for s in exits)
    raise RecordExists(
        "\nABORTADO: el destino ya existe y no se sobrescribe solo.\n\n"
        f"{detalle}\n\n"
        "  Este registro cuesta dinero y NO se puede regenerar: el proponente\n"
        "  no es determinista a temperature 0, asi que una tirada nueva no\n"
        "  devolvera lo mismo.\n\n"
        "  Salidas:\n"
        f"{salidas}\n"
    )


def refuse_shrink(path: Path, new_rows: Sequence[Any], *,
                  overwrite: bool, hint: str = "") -> None:
    """Abort if the record already there has MORE rows than what is going to
    be written.

    This is the second trap the README documents: `compare_runs` and
    `note_audit` rewrite with whatever they are passed as an argument, so
    invoking them with one file instead of with `results2/llm_run2_*.json`
    shrinks the record from 8 runs to 1. It is not a change of digits, it is
    data loss — and the destination never changes, so `refuse_overwrite` cannot
    see it.

    Equal or more rows go through untouched: re-running these two with the full
    glob is the free reproducibility check and must not be obstructed.
    """
    if overwrite or not path.exists():
        return

    d = _load(path)
    if d is None:
        return
    old = d.get("rows") if isinstance(d.get("rows"), list) else None
    if old is None:
        return
    if len(new_rows) >= len(old):
        return

    tenia = ", ".join(str(r.get("file", "?")) for r in old
                      if isinstance(r, dict)) or "?"
    raise RecordExists(
        "\nABORTADO: escribirias un registro MAS PEQUENO que el que ya hay.\n\n"
        f"  {path}\n"
        f"    filas ahora           {len(old)}\n"
        f"    filas que escribirias {len(new_rows)}\n"
        f"    tiradas registradas   {tenia}\n\n"
        "  Estos dos comandos reescriben con lo que se les pase como\n"
        "  ARGUMENTO. Con un fichero suelto en vez del glob, el registro\n"
        "  encoge y las demas tiradas se pierden.\n\n"
        "  Salidas:\n"
        f"{hint or '    pasa el glob completo'}\n"
        f"    {FLAG}      encogerlo a proposito\n"
    )


def or_exit(fn, *args, **kwargs):
    """Run one of the checks and turn its refusal into a clean exit.

    Callers use this; the tests use the checks directly and read the message
    from the exception.
    """
    try:
        return fn(*args, **kwargs)
    except RecordExists as e:
        sys.exit(str(e))
