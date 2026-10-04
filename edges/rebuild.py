"""
The counterfactual rebuild of `PLAN_EDGES.md`: a Stage B run of `PLAN_REUSE.md`
decided again over its own base, with each edge pointed as an arm says.

WHAT IS HELD FIXED, AND WHY (§5.3 of the plan). Every rule is born at the case
the record says, after that case is decided, whatever this rebuild decided
there. Every edge is tried at its birth, in `edge_log` order. Only the direction
of the installed edges changes between arms. So an arm measures what the edges
in force decide. It does not measure what the loop would have done without
them: that would have escalated other cases and born other rules, and knowing
it would take calls. A case the record escalated is never one of `D`.

WHAT IT IS BUILT OVER. `fidelity/replay.py`'s `rule_from` turns a recorded rule
back into a rule, and `F-g2` checks that replay. This module pairs the
`edge_log` with the births the way that replay does, and differs from it in one
thing: it adds a rule at its birth even where the arm decided the case, which
the replay never needs to do. `W-g3` checks that, given the declared
directions, it decides every case as the record did, and that, given no
installed edge, it decides every case as the replay without edges does.

THE ARMS. `directions` maps an edge's key, its position in the `edge_log`, to
DECLARED, FLIPPED or ABSENT. An edge not named is tried as logged. Flipping an
edge that would close a cycle is refused by `try_edge`, as the engine would
refuse it, and the rebuild says so in `tried`.

NO LABEL IS READ HERE. Decisions are outcomes, winners and actions. The labels
are read by `edges/score.py`, after the gate, off the records.

    python3 -m edges.rebuild --fingerprint   # W-g3's child; prints a digest
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass, field
from typing import NamedTuple

from harness.domain import generate_corpus
from rung2.engine2 import PriorityEngine, Space, strictly_below

from fidelity.replay import OUTSIDE, Replay, rule_from

from . import plan

DECLARED, FLIPPED, ABSENT = "declared", "flipped", "absent"
OK = "ok"


class RebuildError(Exception):
    """The record cannot be paired with its own edge log. It stops the plan."""


@dataclass(frozen=True)
class Edge:
    key: int          # its position in the run's edge_log
    birth: int        # the case whose birth tried it
    winner: str       # as declared
    loser: str
    verdict: str      # as logged


class Decision(NamedTuple):
    outcome: str
    winner_id: str | None
    action: str | None
    n_matched: int
    contenders: tuple[str, ...]   # the undefeated rules, on a CONFLICT


@dataclass
class Rebuild:
    decisions: dict[int, Decision]
    tried: dict[int, str]                 # edge key -> what try_edge returned
    installed: set[int]                   # keys that entered the declared graph
    engine: PriorityEngine = field(repr=False)


# ---------------------------------------------------------------------------
# The record, read
# ---------------------------------------------------------------------------

def load_runs() -> dict[int, dict]:
    return {k: json.loads(plan.run_path(k).read_text()) for k in plan.RUNS}


def births(record: dict) -> dict[int, dict]:
    """Every rule of the record by the case it was born at."""
    return {r["born_at"]: r for r in record["rules"]}


def edges_by_birth(record: dict) -> dict[int, list[Edge]]:
    """The `edge_log`, paired with the births that tried it. A row's
    `edge_reasons` lists its edges in order. One citing a rule the proposer was
    not shown was dropped before `try_edge` and is not in the log."""
    log = list(record.get("edge_log") or [])
    out: dict[int, list[Edge]] = {}
    pos = 0
    for row in record["records"]:
        for why in row.get("edge_reasons") or []:
            if why == OUTSIDE:
                continue
            if pos >= len(log):
                raise RebuildError(f"case {row['idx']}: the edge_log ran out")
            winner, loser, logged = log[pos]
            if logged != why:
                raise RebuildError(f"case {row['idx']}: the row says {why}, "
                                   f"the log says {logged}")
            out.setdefault(row["idx"], []).append(
                Edge(pos, row["idx"], winner, loser, logged))
            pos += 1
    if pos != len(log):
        raise RebuildError(f"{len(log) - pos} edge_log entries belong to no row")
    born = births(record)
    for idx in out:
        if idx not in born:
            raise RebuildError(f"case {idx} tried edges and bore no rule")
    return out


def all_edges(record: dict) -> list[Edge]:
    return [e for es in edges_by_birth(record).values() for e in es]


# ---------------------------------------------------------------------------
# The rebuild
# ---------------------------------------------------------------------------

def rebuild(record: dict, corpus, space: Space, *,
            directions: dict[int, str] | None = None,
            only: set[int] | None = None) -> Rebuild:
    """Decide the corpus over the run's base, its births and the timing of its
    edges as recorded, each edge pointed as `directions` says. With `only`,
    just those cases are decided; every birth still happens."""
    directions = directions or {}
    born = births(record)
    by_birth = edges_by_birth(record)
    engine = PriorityEngine(space=space)
    decisions: dict[int, Decision] = {}
    tried: dict[int, str] = {}
    installed: set[int] = set()
    for idx, case in enumerate(corpus):
        if only is None or idx in only:
            outcome, winner, involved = engine.decide(case)
            decisions[idx] = Decision(
                outcome,
                winner.rule_id if winner else None,
                winner.action if winner else None,
                len(involved),
                tuple(r.rule_id for r in involved) if outcome == "CONFLICT" else ())
        d = born.get(idx)
        if d is None:
            continue
        engine.add(rule_from(d), born_at=idx, keep_id=True)
        for e in by_birth.get(idx, []):
            how = directions.get(e.key, DECLARED)
            if how == ABSENT:
                tried[e.key] = ABSENT
                continue
            w, l = (e.winner, e.loser) if how == DECLARED else (e.loser, e.winner)
            before = l in engine.decl_above.get(w, set())
            got = engine.try_edge(w, l)
            tried[e.key] = got
            if got == OK and not before and l in engine.decl_above.get(w, set()):
                installed.add(e.key)
    return Rebuild(decisions, tried, installed, engine)


def classify(record: dict, declared: Rebuild) -> dict[int, str]:
    """Every logged edge, by what it did under its declared direction:
    `installed`; `redundant`, accepted as consistent with subsumption and never
    installed (§5.1); `duplicate`, accepted over a pair already installed; or
    the refusal `try_edge` gave it."""
    ext = declared.engine.ext
    out = {}
    for e in all_edges(record):
        got = declared.tried.get(e.key)
        if got != OK:
            out[e.key] = got or "never_tried"
        elif e.key in declared.installed:
            out[e.key] = "installed"
        elif strictly_below(ext[e.winner], ext[e.loser]):
            out[e.key] = "redundant"
        else:
            out[e.key] = "duplicate"
    return out


def replay_without_edges(record: dict, corpus, space: Space) -> dict[int, Decision]:
    """The rebuild §0 defines `D` with: `fidelity/replay.py`'s, without the
    edges, called and not copied. Its decisions in this module's shape."""
    out = {}
    for m in Replay(record, corpus, space, with_edges=False).moments():
        out[m.idx] = Decision(
            m.outcome,
            m.winner.rule_id if m.winner else None,
            m.winner.action if m.winner else None,
            len(m.involved),
            tuple(r.rule_id for r in m.involved) if m.outcome == "CONFLICT" else ())
    return out


def edge_decided(record: dict, none: dict[int, Decision]) -> tuple[list[int], dict[str, int]]:
    """`D` of §0: the cases the record decides that the rebuild without its
    edges leaves in CONFLICT. Beside it, every departure by kind. §5.2 says the
    only kind there can be is that one, and `W-g2` checks it."""
    d: list[int] = []
    kinds: dict[str, int] = {}
    for row in record["records"]:
        got = none[row["idx"]]
        if (got.outcome, got.winner_id) == (row["outcome"], row["winner_id"]):
            continue
        if row["outcome"] == "ACTION" and got.outcome == "CONFLICT":
            kind = "action_to_conflict"
            d.append(row["idx"])
        elif row["outcome"] == "ACTION" and got.outcome == "ACTION":
            kind = ("same_action_other_winner" if got.action == row["predicted"]
                    else "other_action")
        else:
            kind = f"{row['outcome']}_to_{got.outcome}".lower()
        kinds[kind] = kinds.get(kind, 0) + 1
    return d, kinds


def without_installed(installed: set[int]) -> dict[int, str]:
    return {k: ABSENT for k in installed}


def coin_directions(installed: list[int], rng) -> dict[int, str]:
    """One draw: every installed edge, in `edge_log` order, pointed by a fair
    coin."""
    return {k: (FLIPPED if rng.getrandbits(1) else DECLARED) for k in installed}


# ---------------------------------------------------------------------------
# W-g3's child: the coin under one PYTHONHASHSEED
# ---------------------------------------------------------------------------

def digest(seq) -> str:
    h = hashlib.sha256()
    for x in seq:
        h.update(str(x).encode())
        h.update(b"\0")
    return h.hexdigest()[:16]


def fingerprint(draws: int = plan.FINGERPRINT_DRAWS) -> dict[str, str]:
    """The first `draws` coin draws of every run, as the decisions they make on
    `D`, digested. Outcomes and actions only: no label is read. The witness is
    the iteration order of a set of rule ids, which does depend on the hash
    seed; if it does not move between seeds, the comparison proves nothing."""
    corpus = generate_corpus(plan.N, seed=plan.SEED)
    space = Space()
    out, ids = [], []
    for k, rec in load_runs().items():
        installed = sorted(rebuild(rec, corpus, space).installed)
        d, _ = edge_decided(rec, replay_without_edges(rec, corpus, space))
        rng = plan.coin_rng(k)
        for _ in range(draws):
            arm = rebuild(rec, corpus, space, only=set(d),
                          directions=coin_directions(installed, rng))
            out.append((k, tuple((i, arm.decisions[i].outcome, arm.decisions[i].action)
                                 for i in d)))
        ids += [r["rule_id"] for r in rec["rules"]]
    return {"draws": digest(out), "witness": digest(set(ids))}


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if args != ["--fingerprint"]:
        print(__doc__)
        return 2
    print(json.dumps(fingerprint()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
