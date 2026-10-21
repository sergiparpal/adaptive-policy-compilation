"""
The three manuals of `PLAN_MANUAL.md` §5, read from the files they are frozen in.

**This module is the one route by which the hidden policy reaches the proposer,
and it reaches it as text.** The three files under `manual/texts/` were written
before the signature and are pinned by their digests in §5 of the plan and in
`tests/test_manual.py`. Nothing here imports the oracle, `HIDDEN_DSL` or
`rung2.hidden_priority`: the proposer's path reads a file, and the file is what
the plan declares it to be. `manual/gates.py`'s `G-g2` is where the files are
held against the policy — the rules rebuilt from
`harness.ceiling_check.HIDDEN_DSL` character for character — and that module is
offline.

A level is made of parts, and the parts are the files:

  level 0  nothing: the bare names of the eight queues, as every prompt in the
           tree has given them.
  level 1  the catalogue: one line per queue saying what it is for.
  level 2  the catalogue, then the prose: a manual with a real manual's
           ambiguity, drafted by Claude knowing the policy (§2.1 of the plan
           says what that costs). The prose names teams, and the catalogue is
           what ties each team to its queue.
  level 3  the rules: the 29 rules as text, in their order. The transcription
           bound.

The texts are in Spanish and without accents, as the prompts they go into are:
they are prompt content, not documentation.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

LEVELS = (0, 1, 2, 3)
PARTS = {0: (), 1: ("catalogue",), 2: ("catalogue", "prose"), 3: ("rules",)}
FILES = ("catalogue", "prose", "rules")
TEXT_DIR = Path(__file__).resolve().parent / "texts"


def part_path(part: str) -> Path:
    if part not in FILES:
        raise ValueError(f"no manual part {part!r}: {FILES}")
    return TEXT_DIR / f"{part}.txt"


def part(name: str) -> str:
    """One frozen file, exactly as it is on disk."""
    return part_path(name).read_text(encoding="ascii")


def text(level: int) -> str | None:
    """The manual of `level`: its parts, each without its final newline, joined
    by one blank line. None at level 0."""
    if level not in LEVELS:
        raise ValueError(f"no level {level!r}: {LEVELS}")
    if level == 0:
        return None
    return "\n\n".join(part(p).rstrip("\n") for p in PARTS[level])


def digest(name: str) -> str:
    """sha256 of one frozen file's bytes."""
    return hashlib.sha256(part_path(name).read_bytes()).hexdigest()


def digests() -> dict[str, str]:
    return {name: digest(name) for name in FILES}
