"""
§0's statistics, read alike on the baselines and on the runs.

**One instrument for both.** `O-g2` applies these functions to `PLAN_REUSE.md`'s
and `PLAN_AUTHORSHIP.md`'s records and refuses unless they give the figures §0
declares, and Stage C applies the same functions to this plan's runs. So the
instrument that reads the runs is the one that already reproduced the baselines.

  O-a  `births`: the rules of a base replayed in birth order, each against the
       rules born before it; the share of births that overlap no earlier rule of
       another queue. Overlap is read over the exhaustive space.
  O-b  `fill`: the final base rebuilt with its installed edges, against
       subsumption alone and the hybrid bound, on both surfaces; its share of the
       order's room is `E-c`'s. `o_b_reading` applies §0's rule: the median over
       the runs with room, at least two of them.
  O-c  `installed` and `direction`: the edges the engine accepted and entered in
       the graph, the ones between rules of different queues read for the better
       rule over their shared region, `W-b`'s statistic; `o_c_reading` pools the
       runs.
  O-d  `by_queue`: every logged declaration, by its class and by whether its two
       rules carry one queue.
"""

from __future__ import annotations

import statistics
from collections import Counter
from typing import Any

from harness.dsl import Condition

from authorship import gates as egates
from authorship.score import base_rules
from reuse import structure as st
from rung2.engine2 import EDGE_OK, PriorityEngine, Space, strictly_below
from rung3.edge_direction import better_over_space, verdict

INSTALLED, REDUNDANT = "installed", "redundant"
SAME, DIFFERENT = "same", "different"


def ext_of(rule: dict, space: Space) -> int:
    return space.extension([Condition(c["attr"], c["op"], c["value"])
                            for c in rule["conditions"]])


# --- O-a ---------------------------------------------------------------------

def births(rules: list[dict], space: Space) -> dict[str, int]:
    """The base replayed in birth order: how many rules were born, how many
    overlapped no earlier rule, and how many overlapped no earlier rule of
    another queue."""
    seen: list[tuple[int, Any]] = []
    alone_any = alone_other = 0
    for r in sorted(rules, key=lambda r: (r["born_at"], r["rule_id"])):
        ext, action = ext_of(r, space), r["action"]
        alone_any += not any(ext & x for x, _ in seen)
        alone_other += not any(ext & x for x, a in seen if a != action)
        seen.append((ext, action))
    return {"born": len(rules), "alone": alone_any, "alone_from_other_queues": alone_other}


def o_a(rules: list[dict], space: Space) -> float | None:
    b = births(rules, space)
    return b["alone_from_other_queues"] / b["born"] if b["born"] else None


# --- O-b ---------------------------------------------------------------------

def fill(record: dict, corpus, space: Space, tmask: dict[str, int],
         keep: set[str] | None = None, profile: dict | None = None) -> dict[str, Any]:
    """The final base with its installed edges, those of the channels in `keep`
    only if given, against subsumption alone and the hybrid bound."""
    profile = profile or st.profile(base_rules(record), corpus, space, tmask)
    engine, problems = egates.rebuild_final(record, space, keep)
    with_ = {"space": egates.on_space(engine, tmask, space.n)["e2e"],
             "corpus": egates.on_corpus(engine, corpus, egates.labels_of(record))["e2e"]}
    out: dict[str, Any] = {"reinstall_problems": problems}
    for surface in ("space", "corpus"):
        alone = profile["subsumption"][surface]["e2e"]
        bound = profile["bounds"]["hibrido"][surface]
        out[surface] = {"e2e": with_[surface], "alone": alone, "bound": bound,
                        "room": bound - alone,
                        "share": egates.share(with_[surface], alone, bound)}
    return out


def o_b_reading(shares: list[float | None]) -> dict[str, Any]:
    """§0's rule: the median over the runs whose room is not zero, a run without
    room named and left out, the median of two runs their mean; with fewer than
    `plan.O_B_MIN_RUNS_WITH_ROOM` runs with room there is no reading."""
    from . import plan
    with_room = [i for i, s in enumerate(shares) if s is not None]
    left_out = [i for i, s in enumerate(shares) if s is None]
    enough = len(with_room) >= plan.O_B_MIN_RUNS_WITH_ROOM
    return {"reading": statistics.median([shares[i] for i in with_room]) if enough else None,
            "runs_with_room": [i + 1 for i in with_room],
            "left_out": [i + 1 for i in left_out],
            "unadjudicable": not enough}


def pooled_fill(fills: list[dict], surface: str = "space") -> float | None:
    """What every run's installed edges add, over every run's room. Reported
    beside O-b, never adjudicated (§0)."""
    room = sum(f[surface]["room"] for f in fills)
    gain = sum(f[surface]["e2e"] - f[surface]["alone"] for f in fills)
    return gain / room if room > 0 else None


# --- O-c and O-d ---------------------------------------------------------------

def installed(record: dict, engine: PriorityEngine) -> list[dict]:
    """The edges the engine accepted and entered in the graph: verdict `ok` and
    neither rule's extension strictly inside the other's, so not redundant with
    subsumption. Each with whether its two rules carry one queue."""
    action = {r["rule_id"]: r["action"] for r in record["rules"]}
    out = []
    for w, l, why in record.get("edge_log") or []:
        if why != EDGE_OK:
            continue
        ew, el = engine.ext[w], engine.ext[l]
        if strictly_below(el, ew) or strictly_below(ew, el):
            continue
        out.append({"winner": w, "loser": l, "same_queue": action[w] == action[l]})
    return out


def direction(record: dict, engine: PriorityEngine, tmask: dict[str, int]) -> dict[str, Any]:
    """`W-b`'s reading of the installed edges between rules of different queues:
    the declared winner passed first, the better rule over the shared region on
    the exhaustive space. Edges within a queue are counted apart: no direction
    can make them right or wrong."""
    action = {r["rule_id"]: r["action"] for r in record["rules"]}
    edges = installed(record, engine)
    c = Counter()
    for edge in edges:
        if edge["same_queue"]:
            continue
        c[verdict(*better_over_space(edge["winner"], edge["loser"], engine.ext,
                                     action, tmask))] += 1
    return {"hits": c["a"], "misses": c["b"], "tie": c["tie"],
            "neither_ever_right": c["neither_ever_right"],
            "installed": len(edges),
            "installed_same_queue": sum(1 for x in edges if x["same_queue"])}


def o_c_reading(directions: list[dict]) -> dict[str, Any]:
    """Pooled over the runs, §0: hits over the pairs with a strict better rule."""
    hits = sum(d["hits"] for d in directions)
    strict = hits + sum(d["misses"] for d in directions)
    return {"hits": hits, "strict": strict, "reading": hits / strict if strict else None}


def by_queue(record: dict, engine: PriorityEngine) -> dict[str, int]:
    """Every logged declaration, as `class/same` or `class/different`: the class
    is `installed` or `redundant` for an accepted one, and the verdict for a
    refused one."""
    action = {r["rule_id"]: r["action"] for r in record["rules"]}
    c = Counter()
    for w, l, why in record.get("edge_log") or []:
        if why == EDGE_OK:
            ew, el = engine.ext[w], engine.ext[l]
            cls = REDUNDANT if (strictly_below(el, ew) or strictly_below(ew, el)) else INSTALLED
        else:
            cls = why
        c[f"{cls}/{SAME if action.get(w) == action.get(l) else DIFFERENT}"] += 1
    return dict(sorted(c.items()))


def same_queue_share(counts: dict[str, int], only: tuple[str, ...] | None = None,
                     exclude: tuple[str, ...] = ()) -> tuple[int, int]:
    """(declarations between rules of one queue, declarations), over the classes
    in `only` if given, and leaving out the classes in `exclude`."""
    def kept(cls: str) -> bool:
        return (only is None or cls in only) and cls not in exclude
    rows = {k: n for k, n in counts.items() if kept(k.split("/")[0])}
    return sum(n for k, n in rows.items() if k.endswith("/" + SAME)), sum(rows.values())
