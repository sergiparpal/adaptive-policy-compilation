"""
Environment record for the results JSON files.

MOTIVE. Until August 7, 2026 no record stored which code or which interpreter it
had been produced with. The greedy search's non-deterministic tie-break
—discovered on August 6, when two rungs were already closed on top of it— is
exactly the kind of defect this module makes visible: it depended on
`PYTHONHASHSEED`, which is now noted in every file.

WHAT IS STORED, AND WHAT EACH FIELD IS FOR

  recorded_at     when it was produced. A record re-run without changing
                  anything moves ONLY this field: `git diff` over the rest is
                  then the check that the figure still reproduces.
  python          interpreter version.
  openai          SDK version, or null if it is not installed (the steps that
                  do not call the API run on the standard library).
  platform        system and architecture.
  pythonhashseed  the value of the environment variable. `null` means UNSET,
                  that is, random: it is information, not the absence of it.
                  Any figure sensitive to the iteration order of a set produced
                  with `null` is suspect by construction.
  git_commit      HEAD commit, or null outside a repository.
  git_dirty       whether the tree had ANYTHING uncommitted, anywhere.
  code_dirty      whether the uncommitted part touched the code (CODE_ROOTS).
                  It is the one that decides whether `git_commit` identifies
                  what ran: with `false`, that commit IS the code, even if
                  `git_dirty` says `true`.

  Both are needed and they are not redundant. `code_dirty` answers for the
  code; `git_dirty` warns about the rest, and the rest is not always harmless:
  `learned_subsumption`, `compare_runs` and `note_audit` read records from
  `results*/` AS INPUT, so a modified and uncommitted JSON also breaks the
  traceability of the figure, without touching a line of code. Narrowing the
  single flag to CODE_ROOTS would have kept quiet about it.

  The common case, and the reason for splitting them (Aug 7, 2026): re-running
  several records back to back. The first runs with a clean tree and from then
  on each script has left its own JSON modified, so all the others recorded
  `git_dirty: true` because of the previous one's output. The flag was not
  lying; it was measuring something else. See results2/RECORD_NOTES.md.
  code_digest     sha256 (16 hex) of the code that produces the figures: every
                  .py in harness/, rung2/, rung3/, rung4/ and
                  run_experiment.py. It identifies the code even if the tree is
                  dirty or there is no git. `tests/` is left out on purpose:
                  changing a test changes no number.

This module measures nothing and none of the frozen specifications import it. It
is metadata, and it goes under the `_env` key so that it reads as such.
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

# Code that produces figures. Order does not matter: the digest sorts by path.
# `sensitivity` added 2026-08-29 with the package: it produces figures, so a
# digest that ignored it would identify the wrong code for its records.
CODE_ROOTS = ("harness", "rung2", "rung3", "rung4", "sensitivity",
              "run_experiment.py")

DIGEST_CHARS = 16


def _openai_version() -> str | None:
    try:
        from importlib.metadata import version

        return version("openai")
    except Exception:
        return None


def _git(*args: str) -> str | None:
    """Output of a git call scoped to the repo, or None if git is absent/fails."""
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
    """Fingerprint of the source code. Depends on content, not on git."""
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
    """The `_env` block that accompanies every results JSON."""
    commit = _git("rev-parse", "HEAD")
    tree = _git("status", "--porcelain")
    # The same status scoped to the code. With `--`, git does not confuse a
    # non-existent path with a branch, and CODE_ROOTS mixes dirs and a file.
    code = _git("status", "--porcelain", "--", *CODE_ROOTS)
    env: dict[str, Any] = {
        "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "python": platform.python_version(),
        "openai": _openai_version(),
        "platform": platform.platform(),
        "pythonhashseed": os.environ.get("PYTHONHASHSEED"),
        "git_commit": commit,
        "git_dirty": bool(tree) if tree is not None else None,
        "code_dirty": bool(code) if code is not None else None,
        "code_digest": code_digest(),
    }
    env.update(extra)
    return env


def describe() -> str:
    """A readable one-liner, to print at the foot of a report."""
    e = environment()
    seed = e["pythonhashseed"] or "sin fijar"
    # The mark says what to distrust. Without git nothing is marked: the commit
    # itself already says that.
    if e["code_dirty"]:
        marker = "+codigo-sucio"
    elif e["git_dirty"]:
        marker = "+arbol-sucio"
    else:
        marker = ""
    commit = (e["git_commit"] or "sin git")[:8]
    return (f"python {e['python']} · openai {e['openai'] or '—'} · "
            f"PYTHONHASHSEED {seed} · {commit}{marker} · "
            f"codigo {e['code_digest']}")


if __name__ == "__main__":
    import json

    print(json.dumps(environment(), indent=2))
    print(describe(), file=sys.stderr)
