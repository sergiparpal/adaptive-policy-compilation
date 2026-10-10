"""
§0's statistics for `PLAN_BLIND.md`, read alike on the baselines and on the runs.

**Beyond the keyword, by construction.** Every row is read where
`has_security_keyword` is False: over that half of the exhaustive space, 67,200 of
its 134,400 points, and over the corpus cases without the keyword. A rule whose
extension lies inside the keyword's half is a *keyword rule*, and no row reads
it. So neither a keyword rule the proposer writes nor the hidden policy's three
keyword rules, which sit at its top layer, can decide anything a row reads.

**One instrument for both, checked both ways.** `K-g2` applies these functions to
`PLAN_REUSE.md`'s, `PLAN_AUTHORSHIP.md`'s and `PLAN_OVERLAP.md`'s records twice:
with the restriction lifted, where they must give back `O-a`, `O-b` and `O-c` as
published, and with it, where they must give the figures §0 declares. Stage C
applies the same functions to this plan's runs.

  K-a  `births_outside`: the base replayed in birth order, every rule that is not
       a keyword rule read against the rules born before it; the share that
       overlap no earlier rule of another queue on the half without the keyword.
  K-b  `edge_rows` and `direction`: the edges the engine accepted and entered in
       the graph, declared at a birth on an impasse, between rules of different
       queues, neither of them a keyword rule; each read for the better rule over
       its shared region without the keyword. **Each older rule counts once**:
       the unit is the rule a birth declared against, its value is the share of
       its strict pairs that point at the better rule, and the reading is the
       mean over the units, pooled over the runs.
  K-c  `fill`: `O-b`'s share of the order's room, over the half of the space
       without the keyword.
  K-d  K-b's edges read for the better rule over the corpus cases without the
       keyword, counted as they arrive, and clustered the same way.
  K-e  reported: what `comparators` and `split_by_queue_pair` read beside K-b
       and K-d, and the rest of §0's list.
"""

from __future__ import annotations

import statistics
from collections import defaultdict
from typing import Any, Callable

from harness.dsl import Condition

from authorship import gates as egates
from authorship import protocol as e
from reuse import structure as st
from rung2.engine2 import EDGE_OK, PriorityEngine, Space, strictly_below
from rung3.edge_direction import better_over_corpus, better_over_space, verdict
from rung3.queue_hierarchy_floor import STAGE_C_HIERARCHY

KW = "has_security_keyword"
IMPASSE = "IMPASSE"
HIT, MISS, TIE, NEITHER = "a", "b", "tie", "neither_ever_right"


# ---------------------------------------------------------------------------
# The restriction
# ---------------------------------------------------------------------------

def outside_mask(space: Space) -> int:
    """The points of the space without the keyword: half of it."""
    return space.extension([Condition(KW, "eq", False)])


def restrict(tmask: dict[str, int], mask: int) -> dict[str, int]:
    return {q: m & mask for q, m in tmask.items()}


def outside_cases(corpus) -> list[int]:
    """The corpus cases without the keyword, by index, in arrival order."""
    return [i for i, c in enumerate(corpus) if not c.has_security_keyword]


def ext_of(rule: dict, space: Space) -> int:
    return space.extension([Condition(c["attr"], c["op"], c["value"])
                            for c in rule["conditions"]])


def is_keyword(ext: int, outside: int) -> bool:
    """A rule whose extension lies inside the keyword's half. With the
    restriction lifted, `outside` is the whole space and no rule is one."""
    return bool(ext) and not ext & outside


# ---------------------------------------------------------------------------
# K-a
# ---------------------------------------------------------------------------

def births_outside(rules: list[dict], space: Space, outside: int) -> dict[str, int]:
    """The base replayed in birth order. A keyword rule is counted apart and read
    against nothing; every other rule is read against the rules born before it,
    on the half without the keyword, and counted alone when it meets none of
    another queue there."""
    seen: list[tuple[int, Any]] = []
    keyword = alone = 0
    for r in sorted(rules, key=lambda r: (r["born_at"], r["rule_id"])):
        ext, action = ext_of(r, space), r["action"]
        if is_keyword(ext, outside):
            keyword += 1
        else:
            alone += not any(ext & x & outside for x, a in seen if a != action)
        seen.append((ext, action))
    return {"born": len(rules), "keyword": keyword, "outside": len(rules) - keyword,
            "alone_outside": alone}


def material(rules: list[dict], space: Space, tmask: dict[str, int],
             outside: int) -> dict[str, int]:
    """What a base would put in front of K-b if every birth were placed against
    every earlier rule of another queue it crosses: the pairs of rules of
    different queues, neither a keyword rule nor nested in the other, that meet
    on the half without the keyword; how many have a strict better rule there;
    and how many older rules carry one. A probe for §0, not a row."""
    ordered = sorted(rules, key=lambda r: (r["born_at"], r["rule_id"]))
    ext = {r["rule_id"]: ext_of(r, space) for r in ordered}
    action = {r["rule_id"]: r["action"] for r in ordered}
    t_out = restrict(tmask, outside)
    units, pairs, strict = set(), 0, 0
    for j, new in enumerate(ordered):
        a = new["rule_id"]
        if is_keyword(ext[a], outside):
            continue
        for old in ordered[:j]:
            b = old["rule_id"]
            if (action[a] == action[b] or is_keyword(ext[b], outside)
                    or not ext[a] & ext[b] & outside
                    or strictly_below(ext[a], ext[b]) or strictly_below(ext[b], ext[a])):
                continue
            pairs += 1
            if verdict(*better_over_space(a, b, ext, action, t_out)) in (HIT, MISS):
                strict += 1
                units.add(b)
    return {"crossing_pairs": pairs, "strict": strict, "units": len(units)}


def k_a(rules: list[dict], space: Space, outside: int) -> float:
    """§0: a run with no birth outside the keyword counts at 1.00, the most
    partitioned a run can be, as `O-a` counts a run with no birth."""
    b = births_outside(rules, space, outside)
    return b["alone_outside"] / b["outside"] if b["outside"] else 1.0


# ---------------------------------------------------------------------------
# K-b and K-d: the edges, and their direction
# ---------------------------------------------------------------------------

def channels_of(record: dict) -> list[str]:
    """Each logged edge's channel. A record without them is v1's, whose edges
    all came with a rule."""
    log = record.get("edge_log") or []
    return record.get("edge_channels") or [e.WRITE] * len(log)


def edge_rows(record: dict, engine: PriorityEngine, tmask: dict[str, int], outside: int,
              sets: list[set[str]] | None = None, truth: list[str] | None = None,
              cases_out: list[int] | None = None) -> list[dict[str, Any]]:
    """Every edge the engine accepted and entered in the graph, in the order it
    accepted them: verdict `ok`, and neither rule's extension strictly inside the
    other's. Each with what the rows read of it. `younger` is the rule born later,
    which on the write channel is the one whose birth declared the edge."""
    action = {r["rule_id"]: r["action"] for r in record["rules"]}
    born = {r["rule_id"]: r["born_at"] for r in record["rules"]}
    outcome = {row["idx"]: row["outcome"] for row in record["records"]}
    t_out = restrict(tmask, outside)
    out = []
    for (w, l, why), ch in zip(record.get("edge_log") or [], channels_of(record)):
        if why != EDGE_OK:
            continue
        ew, el = engine.ext[w], engine.ext[l]
        if strictly_below(el, ew) or strictly_below(ew, el):
            continue
        younger, older = (w, l) if (born[w], w) > (born[l], l) else (l, w)
        row: dict[str, Any] = {
            "winner": w, "loser": l, "channel": ch, "older": older, "younger": younger,
            "younger_born_on": outcome.get(born[younger]),
            "queues": (action[w], action[l]), "same_queue": action[w] == action[l],
            "keyword": is_keyword(ew, outside) or is_keyword(el, outside)}
        if not row["same_queue"]:
            row["space_full"] = verdict(*better_over_space(w, l, engine.ext, action, tmask))
            row["space_out"] = verdict(*better_over_space(w, l, engine.ext, action, t_out))
            if sets is not None:
                row["corpus_out"] = verdict(*better_over_corpus(w, l, sets, truth, action,
                                                                cases_out))
        out.append(row)
    return out


def beyond_the_keyword(row: dict) -> bool:
    """K-b's, K-c's and K-e's population: declared at a birth on an impasse,
    between rules of different queues, neither of them a keyword rule."""
    return (row["channel"] == e.WRITE and row["younger_born_on"] == IMPASSE
            and not row["same_queue"] and not row["keyword"])


def across_queues(row: dict) -> bool:
    """`O-c`'s population, which K-g2 reads with the restriction lifted."""
    return not row["same_queue"]


def outside_the_keyword(row: dict) -> bool:
    """The pairwise answers' population here: two queues, no keyword rule."""
    return not row["same_queue"] and not row["keyword"]


def sets_of(rules: list[dict], corpus) -> list[set[str]]:
    """Every rule matching each corpus case, without building an engine."""
    objs = [(r["rule_id"], [Condition(c["attr"], c["op"], c["value"])
                            for c in r["conditions"]]) for r in rules]
    return [{rid for rid, conds in objs if all(c.holds(case) for c in conds)}
            for case in corpus]


def pair_rows(answers: list[dict], record: dict, space: Space, tmask: dict[str, int],
              outside: int, sets: list[set[str]], truth: list[str],
              cases_out: list[int]) -> list[dict[str, Any]]:
    """The pairwise answers `PLAN_PROPOSER_1600.md` paid for, as rows `direction`
    reads: the declared winner of every answer that declared one, over the base
    of `record`, with the same readings `edge_rows` gives an installed edge."""
    action = {r["rule_id"]: r["action"] for r in record["rules"]}
    born = {r["rule_id"]: r["born_at"] for r in record["rules"]}
    ext = {r["rule_id"]: ext_of(r, space) for r in record["rules"]}
    t_out = restrict(tmask, outside)
    out = []
    for a in answers:
        w, l = a.get("declared_winner"), a.get("declared_loser")
        if not w or not l:
            continue
        younger, older = (w, l) if (born[w], w) > (born[l], l) else (l, w)
        row = {"winner": w, "loser": l, "channel": "pairwise", "older": older,
               "younger": younger, "younger_born_on": None,
               "queues": (action[w], action[l]), "same_queue": action[w] == action[l],
               "keyword": is_keyword(ext[w], outside) or is_keyword(ext[l], outside)}
        if not row["same_queue"]:
            row["space_full"] = verdict(*better_over_space(w, l, ext, action, tmask))
            row["space_out"] = verdict(*better_over_space(w, l, ext, action, t_out))
            row["corpus_out"] = verdict(*better_over_corpus(w, l, sets, truth, action,
                                                            cases_out))
        out.append(row)
    return out


def direction(rows_by_run: list[list[dict]], key: str,
              keep: Callable[[dict], bool] = beyond_the_keyword,
              predict: Callable[[dict], str] | None = None) -> dict[str, Any]:
    """The share of strict pairs whose declared winner is the better rule under
    `key`, three ways: **by older rule**, which adjudicates (§0); pooled over the
    pairs; and by declared winner. With `predict`, the same pairs are read for
    the rule `predict` names instead of the declared winner."""
    by_older: dict[tuple[int, str], list[bool]] = defaultdict(list)
    by_winner: dict[tuple[int, str], list[bool]] = defaultdict(list)
    ties = neither = 0
    for k, rows in enumerate(rows_by_run):
        for row in rows:
            if not keep(row):
                continue
            v = row[key]
            if v == TIE:
                ties += 1
                continue
            if v == NEITHER:
                neither += 1
                continue
            better = row["winner"] if v == HIT else row["loser"]
            named = row["winner"] if predict is None else predict(row)
            by_older[(k, row["older"])].append(named == better)
            by_winner[(k, row["winner"])].append(named == better)
    hits = sum(sum(v) for v in by_older.values())
    strict = sum(len(v) for v in by_older.values())

    def mean_of(units):
        return statistics.mean(sum(v) / len(v) for v in units.values()) if units else None

    return {"units": len(by_older), "reading": mean_of(by_older),
            "hits": hits, "strict": strict, "pooled": hits / strict if strict else None,
            "by_winner": mean_of(by_winner), "winners": len(by_winner),
            "largest_unit": max((len(v) for v in by_older.values()), default=0),
            "ties": ties, "neither_ever_right": neither}


def stage_c_names(row: dict) -> str:
    """The rule a fixed ranking of the queues would name: `rung3`'s Stage C
    hierarchy, fitted on the hidden policy's pairs and read here unchanged."""
    rank = {q: i for i, q in enumerate(STAGE_C_HIERARCHY)}
    qw, ql = row["queues"]
    return row["winner"] if rank[qw] < rank[ql] else row["loser"]


def newborn_names(row: dict) -> str:
    """The rule a proposer that always declared its new rule an exception would
    name."""
    return row["younger"]


def split_by_queue_pair(rows_by_run: list[list[dict]], key: str,
                        keep: Callable[[dict], bool] = beyond_the_keyword) -> dict[str, Any]:
    """`B-d`'s split, on these pairs: a queue pair a fixed ranking cannot answer
    is one whose better rule carries one queue in some of its strict pairs and
    the other in others. The direction is read on each side, by older rule."""
    better_queues: dict[frozenset, set[str]] = defaultdict(set)
    for rows in rows_by_run:
        for row in rows:
            if keep(row) and row[key] in (HIT, MISS):
                qw, ql = row["queues"]
                better_queues[frozenset((qw, ql))].add(qw if row[key] == HIT else ql)
    unreachable = {qp for qp, qs in better_queues.items() if len(qs) > 1}

    def side(name):
        want = name == "unreachable"
        return direction(rows_by_run, key,
                         keep=lambda r: keep(r) and (frozenset(r["queues"]) in unreachable) == want)

    return {"queue_pairs": len(better_queues), "unreachable_queue_pairs": len(unreachable),
            "reachable": side("reachable"), "unreachable": side("unreachable")}


def comparators(rows_by_run: list[list[dict]], key: str,
                keep: Callable[[dict], bool] = beyond_the_keyword) -> dict[str, Any]:
    """Two rules of thumb that read no rule, on K-b's pairs, beside the declared
    direction: a fixed ranking of the queues, and the new rule always winning."""
    return {"declared": direction(rows_by_run, key, keep=keep),
            "stage_c_ranking": direction(rows_by_run, key, keep=keep, predict=stage_c_names),
            "newborn_wins": direction(rows_by_run, key, keep=keep, predict=newborn_names)}


# ---------------------------------------------------------------------------
# K-c: the order's room
# ---------------------------------------------------------------------------

def undefeated_masks(engine: PriorityEngine) -> dict[str, int]:
    """Where each rule is undefeated: its extension, less every rule that beats
    it, by subsumption or by an edge. `authorship.gates.on_space`'s masks."""
    out = {}
    for r in engine.rules:
        dominated = 0
        for b in engine.beats_me(r.rule_id):
            dominated |= engine.ext[b]
        out[r.rule_id] = engine.ext[r.rule_id] & ~dominated
    return out


def e2e_within(undefeated: dict[str, int], action: dict[str, str], tmask: dict[str, int],
               mask: int) -> float:
    """The engine's end to end over the points of `mask`, by masks."""
    return st.subsumption_on_space({rid: m & mask for rid, m in undefeated.items()},
                                   action, restrict(tmask, mask), mask.bit_count())["e2e"]


def fill(record: dict, space: Space, tmask: dict[str, int], mask: int,
         keep: set[str] | None = None) -> dict[str, Any]:
    """`O-b`'s statistic over the points of `mask`: the final base with its
    installed edges, those of the channels in `keep` only if given, against
    subsumption alone and the hybrid bound, which counts the points where some
    rule subsumption leaves undefeated carries the true queue."""
    with_, problems = egates.rebuild_final(record, space, keep)
    alone, _ = egates.rebuild_final(record, space, set())
    action = {r.rule_id: r.action for r in alone.rules}
    u_alone = undefeated_masks(alone)
    reach = 0
    for rid, m in u_alone.items():
        reach |= m & tmask[action[rid]]
    bound = (reach & mask).bit_count() / mask.bit_count()
    a = e2e_within(u_alone, action, tmask, mask)
    w = e2e_within(undefeated_masks(with_), action, tmask, mask)
    return {"e2e": w, "alone": a, "bound": bound, "room": bound - a,
            "share": egates.share(w, a, bound), "reinstall_problems": problems}


def fill_on_corpus(record: dict, space: Space, corpus, labels, cases: list[int]) -> dict[str, Any]:
    """The same over the corpus cases in `cases`, counted as they arrive.
    Reported, never adjudicated (§0)."""
    with_, _ = egates.rebuild_final(record, space)
    alone, _ = egates.rebuild_final(record, space, set())
    sub = [corpus[i] for i in cases]
    lab = [labels[i] for i in cases]
    w = egates.on_corpus(with_, sub, lab)["e2e"]
    a = egates.on_corpus(alone, sub, lab)["e2e"]
    reach = 0
    for case, (truth, _) in zip(sub, lab):
        matched = [r for r in alone.rules if r.matches(case)]
        ids = {r.rule_id for r in matched}
        reach += any(r.action == truth and not (alone.beats_me(r.rule_id) & ids)
                     for r in matched)
    bound = reach / len(sub) if sub else None
    return {"e2e": w, "alone": a, "bound": bound,
            "room": None if bound is None else bound - a,
            "share": None if bound is None else egates.share(w, a, bound)}


def median_with_room(shares: list[float | None], minimum: int) -> dict[str, Any]:
    """`O-b`'s rule, which §0 keeps for K-c: the median over the runs whose room
    is not zero, a run without room named and left out, the median of two runs
    their mean; with fewer than `minimum` runs with room there is no reading."""
    with_room = [i for i, s in enumerate(shares) if s is not None]
    enough = len(with_room) >= minimum
    return {"reading": statistics.median([shares[i] for i in with_room]) if enough else None,
            "runs_with_room": [i + 1 for i in with_room],
            "left_out": [i + 1 for i, s in enumerate(shares) if s is None],
            "unadjudicable": not enough}
