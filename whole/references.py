"""
The references of `PLAN_WHOLE.md` §5.5 and Stage A, all free, and the readings
of a run that Stage C shares with them. **Never on the proposer's path.**

`whole(r)`, §0's statistic and figure 1. Every escalation's first-call draft is
classed by `placement/cost.py`'s `draft_class`, called: against its ticket's
governing rule, the first listed rule whose region holds the ticket, as
`placement/births.py` classes a birth. A draft *holds its part* when its class is
`whole`: it names the governing rule's queue, and every point of the governing
rule's region whose true queue is that queue lies in its extension. A draft of
another queue is `wrong_queue`, and one naming no valid rule is `no_rule`; both
are left out of the share, above and below, and counted. It is read on the first
call's answer, born or not.

THE LISTS A WHOLE DRAFT WOULD MEET, §0's figure 2. Each of `PLAN_PLACEMENT.md`'s
v1c records, read-only, is replayed in birth order: each rule added at the case
it was born at, and its edges tried after it in `edge_log` order, as
`edges/rebuild.py` pairs them. Before each recorded escalation, v1c's list is
taken for the governing rule's region whole, of the governing rule's queue,
through `placement.protocol.listing_of`, and set beside the list the run sent.
**The replay is checked where the record allows it**: wherever the first call
drafted a valid rule that met another queue, the rebuilt base's `O`, v1c's list
and what it left out must be the recorded ones.

THE TRANSCRIBER, §0's figure 3, is `placement/references.py`'s, called: v1c's
loop with `PLAN_REASONED_LOOP.md`'s transcriber, under each of `PLAN_CHANNEL.md`'s
draws. It writes the governing rule's region and places it by the list's order,
so it is the proposer v1d asks for, and it ignores the text either arm carries.
Its figures under v1d are its figures under v1c.

WHERE THE LEVEL-1 SENTENCE AND THE PARAGRAPH PULL APART, §0's figure 5, off the
text's 29 regions alone. Every listed rule but the catch-all lies strictly inside
some lower rule, so a whole draft is a particular case of that rule, and
containment orders it right, as the system prompt's sentence says. The two texts
pull apart only at the lower rules a governing rule crosses.

WHAT A WHOLE BIRTH CANNOT DECIDE, reported in `WR-g`: the points of its part that
lie inside a narrower rule of another queue. Containment ranks such a rule above
it, v1c's round never lists it, and no side installs anything against it (§6.12).

It reads the proposer's answers `PLAN_PLACEMENT.md` paid for, by masks, and no
answer this plan buys.
"""

from __future__ import annotations

import collections
import json
from fractions import Fraction
from functools import lru_cache
from typing import Any, Iterator

from blind import rows as brows
from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from placement import births as BI
from placement import cost as PC
from placement import oncall as PO
from placement import plan as pl_plan
from placement import protocol as pl_protocol
from placement import references as pl_refs
from reasoned_loop import governed as gv
from reasoned_loop import references as rl_refs
from rung2.engine2 import PriorityEngine, strictly_below

from . import plan

F = Fraction
ONCALL = "ONCALL_ESCALATION"
LEFT_OUT_OF_THE_SHARE = ("wrong_queue", "no_rule")
median = pl_refs.median            # the middle of three, the mean of two (§0)


@lru_cache(maxsize=None)
def _world() -> tuple:
    return (MI.space(), MI.corpus(), rl_refs.regions(), MI.space_truth(),
            BI.listed_queues())


# ---------------------------------------------------------------------------
# whole(r): §0's statistic, on any run's record
# ---------------------------------------------------------------------------

THE_REGION, WIDER, WITHIN_OR_ACROSS = "the_region", "wider", "within_or_across"


def breadth(esc: dict[str, Any], case) -> str | None:
    """A first-call draft's extension against its governing rule's region: the
    region itself, wider than it, or neither. None for a draft naming no valid
    rule. A draft that holds its part may be any of the three (§6.13)."""
    space, _, regions, _, _ = _world()
    payload = ((esc.get("calls") or [{}])[0].get("payload")) or {}
    if not payload.get("conditions"):
        return None
    ext = PO.draft_ext(payload, space)
    if ext is None:
        return None
    g = regions[PO.matched(gv.point_of(case, space), regions)[0]]
    return THE_REGION if ext == g else WIDER if ext & g == g else WITHIN_OR_ACROSS


def first_drafts(record: dict[str, Any]) -> list[dict[str, Any]]:
    """Every escalation's first-call draft, classed (`placement/cost.py`), with
    its breadth."""
    space, cases, regions, truth, queues = _world()
    return [{**PC.draft_class(esc, cases[esc["idx"]], space, regions, truth, queues),
             "breadth": breadth(esc, cases[esc["idx"]])}
            for esc in sorted(record["escalations"], key=lambda x: x["idx"])]


def whole_of(drafts: list[dict[str, Any]]) -> dict[str, Any]:
    """`whole(r)` over classed drafts: those of the right queue that hold their
    part, over those of the right queue. None when no draft names the right
    queue (§0)."""
    right = [d for d in drafts if d["class"] not in LEFT_OUT_OF_THE_SHARE]
    held = [d for d in right if d["class"] == "whole"]
    return {"drafts": len(drafts), "right_queue": len(right), "held": len(held),
            "wrong_queue": sum(1 for d in drafts if d["class"] == "wrong_queue"),
            "no_rule": sum(1 for d in drafts if d["class"] == "no_rule"),
            "share": F(len(held), len(right)) if right else None,
            "by_class": dict(sorted(collections.Counter(d["class"] for d in drafts).items())),
            "held_by_breadth": dict(sorted(collections.Counter(
                str(d.get("breadth")) for d in held).items()))}


def whole_share(record: dict[str, Any]) -> dict[str, Any]:
    """`whole(r)` for one run, with every draft and the share by queue."""
    drafts = first_drafts(record)
    _, _, _, _, queues = _world()
    by_queue: dict[str, list[int]] = {}
    for d in drafts:
        if d["class"] in LEFT_OUT_OF_THE_SHARE:
            continue
        q = by_queue.setdefault(queues[d["governing"]], [0, 0])
        q[0] += d["class"] == "whole"
        q[1] += 1
    return {**whole_of(drafts), "by_queue": dict(sorted(by_queue.items())), "rows": drafts}


# ---------------------------------------------------------------------------
# The bases a run stood on
# ---------------------------------------------------------------------------

def bases_before(record: dict[str, Any]) -> Iterator[tuple[dict[str, Any], PriorityEngine]]:
    """Each escalation of a record, in case order, with the base as it stood
    before it. The same engine is yielded each time, grown in place."""
    space = MI.space()
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    births, bi = sorted(born), 0
    engine = PriorityEngine(space=space)
    for esc in sorted(record["escalations"], key=lambda x: x["idx"]):
        idx = esc["idx"]
        while bi < len(births) and births[bi] < idx:
            b = births[bi]
            engine.add(rule_from(born[b]), born_at=b, keep_id=True)
            for ed in by_birth.get(b, []):
                engine.try_edge(ed.winner, ed.loser)
            bi += 1
        yield esc, engine


def as_recorded(esc: dict[str, Any], engine: PriorityEngine) -> bool | None:
    """Whether the rebuilt base gives back the recorded round: `O`, v1c's list
    and what it left out. None where the record has nothing to hold it to."""
    c0 = (esc.get("calls") or [{}])[0]
    if not c0.get("overlapped") or c0.get("payload") is None:
        return None
    draft = brows.ext_of({"conditions": c0["payload"]["conditions"]}, MI.space())
    got = pl_protocol.listing_of(engine, draft, c0["payload"]["action"])
    return (set(got["overlapped"]) == set(c0["overlapped"])
            and set(got["kept"]) == set(esc.get("listed") or [])
            and got["left_out"] == (c0.get("left_out") or {}))


def lists_of(record: dict[str, Any]) -> dict[str, Any]:
    """Figure 2 for one v1c run: at each escalation, v1c's list for the
    governing rule's region whole, beside the list the run sent."""
    space, cases, regions, _, queues = _world()
    rows, checked, departing = [], 0, []
    for esc, engine in bases_before(record):
        idx = esc["idx"]
        gov = PO.matched(gv.point_of(cases[idx], space), regions)[0]
        whole = pl_protocol.listing_of(engine, regions[gov], queues[gov])
        rows.append({"idx": idx, "governing": gov, "queue": queues[gov],
                     "whole_list": len(whole["kept"]),
                     "sent_list": len(esc.get("listed") or [])})
        ok = as_recorded(esc, engine)
        if ok is not None:
            checked += 1
            if not ok:
                departing.append(idx)
    whole_sizes = [F(r["whole_list"]) for r in rows]
    sent_sizes = [F(r["sent_list"]) for r in rows]
    return {"escalations": len(rows),
            "whole_median": str(median(whole_sizes)) if rows else None,
            "sent_median": str(median(sent_sizes)) if rows else None,
            "whole_max": max(r["whole_list"] for r in rows) if rows else None,
            "rare": [[r["idx"], r["governing"], r["whole_list"], r["sent_list"]]
                     for r in rows if r["queue"] == ONCALL],
            "rounds_checked": checked, "departing": departing,
            "replay_ok": checked > 0 and not departing, "rows": rows}


# ---------------------------------------------------------------------------
# §0's figures 1 to 3: the drafting reading
# ---------------------------------------------------------------------------

def placement_record(arm: str, rep: int) -> dict[str, Any]:
    """One of `PLAN_PLACEMENT.md`'s six runs, read-only."""
    return json.loads(pl_plan.run_path(arm, rep).read_text())


@lru_cache(maxsize=None)
def _drafting_reading() -> str:
    whole, lists, rare = {}, {}, {}
    for arm in pl_plan.ARMS:
        for rep in range(1, pl_plan.REPS + 1):
            rec = placement_record(arm, rep)
            got = whole_of(first_drafts(rec))
            whole[f"{arm}_r{rep}"] = [got["held"], got["right_queue"]]
            if arm == "v1c":
                ls = lists_of(rec)
                lists[f"v1c_r{rep}"] = {k: ls[k] for k in ("escalations", "whole_median",
                                                            "sent_median", "whole_max")}
                lists[f"v1c_r{rep}"]["replay"] = {"rounds_checked": ls["rounds_checked"],
                                                  "departing": ls["departing"],
                                                  "replay_ok": ls["replay_ok"]}
                rare[f"v1c_r{rep}"] = ls["rare"]
    v1c = [F(*whole[f"v1c_r{rep}"]) for rep in range(1, pl_plan.REPS + 1)]
    transcriber = {f"r{rep}": pl_refs.transcriber("v1c", rep)["figures"]["recall_oncall"]
                   for rep in range(1, pl_plan.REPS + 1)}
    relations = text_relations()
    return json.dumps({"whole": whole, "whole_median_v1c": str(median(v1c)),
                       "lists": lists, "lists_rare": rare,
                       "transcriber_oncall": transcriber,
                       "text_relations": {k: v for k, v in relations.items() if k != "rows"},
                       "text_relations_rows": relations["rows"]})


def drafting_reading() -> dict[str, Any]:
    """§0's figures 1 to 3 and 5, recomputed from `PLAN_PLACEMENT.md`'s records
    and the text."""
    return json.loads(_drafting_reading())


def drafting_as_declared(got: dict[str, Any]) -> dict[str, bool]:
    """Each of §0's figures 1 to 3 and 5 against `got`, and the replay figure 2
    rests on."""
    d = plan.DECLARED
    lists = {k: {x: v for x, v in got["lists"][k].items() if x != "replay"}
             for k in got["lists"]}
    return {
        "whole": got["whole"] == d["whole"],
        "whole_median_v1c": F(got["whole_median_v1c"]) == F(d["whole_median_v1c"]),
        "lists": lists == d["lists"],
        "lists_rare": got["lists_rare"] == d["lists_rare"],
        "transcriber_oncall": all(F(got["transcriber_oncall"][k]) == F(v)
                                  for k, v in d["transcriber_oncall"].items()),
        "replay": all(v["replay"]["replay_ok"] for v in got["lists"].values()),
        "text_relations": got["text_relations"] == d["text_relations"],
    }


# ---------------------------------------------------------------------------
# §0's figure 5: where the level-1 sentence and the paragraph pull apart
# ---------------------------------------------------------------------------

def text_relations() -> dict[str, Any]:
    """Off the text's 29 regions alone: for each listed rule, the lower rules
    whose regions contain it strictly, those whose regions lie inside it, and
    those it crosses, with the crossing ones of another queue. A whole draft is
    a particular case of the first kind, where containment orders it right; the
    level-1 sentence and the paragraph pull apart only at the third (§6.11)."""
    regions, queues = rl_refs.regions(), BI.listed_queues()
    ids = sorted(regions)
    rows = {}
    for i, g in enumerate(ids):
        lower = ids[i + 1:]
        contains = [x for x in lower if strictly_below(regions[g], regions[x])]
        inside = [x for x in lower if strictly_below(regions[x], regions[g])]
        crosses = [x for x in lower if regions[x] & regions[g] and regions[x] != regions[g]
                   and x not in contains and x not in inside]
        rows[g] = {"contained_by": contains, "holds_inside": inside, "crosses": crosses,
                   "crosses_another_queue": [x for x in crosses if queues[x] != queues[g]]}
    return {
        "lower_containing_pairs": sum(len(r["contained_by"]) for r in rows.values()),
        "lower_crossing_pairs": sum(len(r["crosses"]) for r in rows.values()),
        "rules_inside_a_lower_rule": sum(1 for r in rows.values() if r["contained_by"]),
        "rules_holding_a_lower_rule": sum(1 for r in rows.values() if r["holds_inside"]),
        "rules_crossing_another_queue": sum(1 for r in rows.values()
                                            if r["crosses_another_queue"]),
        "rare": {g: [len(rows[g]["contained_by"]), len(rows[g]["crosses"]),
                     len(rows[g]["crosses_another_queue"])] for g in ("H04", "H05")},
        "rows": rows}


# ---------------------------------------------------------------------------
# What Stage C reads of a run beside whole(r), and Stage A of the references
# ---------------------------------------------------------------------------

def births_of(record: dict[str, Any]) -> dict[str, Any]:
    """Every birth classed as `placement/births.py` classes it, and its counts."""
    space, cases, regions, truth, queues = _world()
    births = BI.read_run(record, space, regions, truth, queues, cases)
    return {"counts": BI.counts(births),
            "rows": [{k: b[k] for k in ("rule_id", "born_at", "action", "governing",
                                        "class", "is_the_region")} for b in births]}


def lost_of(record: dict[str, Any]) -> dict[str, Any]:
    """The points the final base loses, by what was drafted for the rule that
    governs them, as `placement/cost.py` reads them."""
    space, cases, regions, truth, queues = _world()
    run = PC.read_run(record, space, regions, PC.governed_masks(regions), truth, queues,
                      cases)
    tag = "run"
    return {"right": run["right"], "by_class": PC.totals({tag: run}, [tag]),
            "outside_the_rarest_queue": PC.totals({tag: run}, [tag], PC.RARE_RULES),
            "by_queue": PC.by_queue({tag: run}, [tag]),
            "rules": {g: {k: r[k] for k in ("queue", "points", "lost", "class")}
                      for g, r in run["rules"].items()}}


def inside_whole_births(record: dict[str, Any]) -> dict[str, Any]:
    """§6.12: by governing rule with a whole birth, the rules of another queue
    strictly inside one of its whole births in the final base, and how many of
    the points the rule governs they lie on. Containment ranks each of them above
    the whole birth there, so it cannot take those points whatever it declares,
    and v1c's round never lists them. Beside them, the governed points the final
    base loses, and how many of those lie inside such rules. A governed point is
    one whose first match is the rule, so the counts add up over rules without
    counting a point twice."""
    space, cases, regions, truth, queues = _world()
    eng = MI.final_engine(record)
    right = PC.right_mask(eng, truth)
    governed = PC.governed_masks(regions)
    by_gov: dict[str, dict[str, Any]] = {}
    for b in BI.read_run(record, space, regions, truth, queues, cases):
        if b["class"] != "whole":
            continue
        g = by_gov.setdefault(b["governing"], {"births": [], "inside": set(), "mask": 0})
        g["births"].append(b["rule_id"])
        ext = eng.ext[b["rule_id"]]
        for r in eng.rules:
            if r.action != b["action"] and strictly_below(eng.ext[r.rule_id], ext):
                g["inside"].add(r.rule_id)
                g["mask"] |= eng.ext[r.rule_id]
    rows = {}
    for gov, g in sorted(by_gov.items()):
        mine = governed[gov]
        lost = mine & ~right
        rows[gov] = {"births": g["births"], "inside": sorted(g["inside"]),
                     "governed_points": mine.bit_count(),
                     "governed_inside": (mine & g["mask"]).bit_count(),
                     "governed_lost": lost.bit_count(),
                     "lost_inside": (lost & g["mask"]).bit_count()}
    total = {k: sum(r[k] for r in rows.values())
             for k in ("governed_points", "governed_inside", "governed_lost", "lost_inside")}
    return {"governing_rules": len(rows),
            "with_another_queue_inside": sum(1 for r in rows.values() if r["inside"]),
            **total, "rows": rows}


def transcriber_figures() -> dict[str, Any]:
    """The transcriber under v1c and every draw, `placement/references.py`'s."""
    return {f"v1c_{pl_plan.stream('v1c', rep)}": pl_refs.transcriber("v1c", rep)["figures"]
            for rep in (1, 2, 3, None)}
