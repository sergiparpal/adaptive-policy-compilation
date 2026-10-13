"""
WHAT THE BASE'S TRANSITIVE ORDER WOULD DECIDE. Rung 2's engine decides a case by
direct defeats among the rules that match it. A rule beaten only through a chain
whose middle rule does not match stays undefeated. `blind/cycles.py` found that
this is how run 1 of `PLAN_BLIND.md` got its CONFLICTs: a refused declaration
leaves two crossing rules without an edge, the base orders them only through the
rule that closed the cycle, and where that rule does not match, the two conflict.
An engine that read the transitive closure would decide those points. This reads
what it would decide, and whether rightly. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
The closure engine is rung 2's with one change: a matching rule is defeated when
any rule that reaches it, through subsumption and declared edges together,
matches too, where rung 2's needs a rule that beats it directly. The order is
acyclic, because the engine refuses every edge that would close a cycle. So at
any point the closure removes rules from the undefeated set and never all of
them. **It changes no decision and adds no IMPASSE**: it can only resolve a
CONFLICT, to one of the queues left in contention.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
The final base of each of the twelve paid runs of rung 2's loop at n=2000, three
per protocol: v1 (`PLAN_REUSE.md`), v1e (`PLAN_AUTHORSHIP.md`), v2e
(`PLAN_OVERLAP.md`) and v2b (`PLAN_BLIND.md`). Each is rebuilt with every
accepted edge, in the order accepted, as Stage C rebuilds it. Each is read over
the exhaustive space and over the 2,000 corpus cases, counted as they arrive:

  conflicts     the points where the engine as it is leaves a CONFLICT.
  resolved      those where the closure leaves one queue.
  closure       of the resolved points, those where that queue is the true one.
  overruled     those where the true queue is one the closure overrules: one the
                engine as it is left in contention there.
  neither       those where no queue in contention is the true one.
  coin          a fair coin over the queues in contention, its expected hits.
  ranking       the queue rung 3's Stage C hierarchy ranks highest among them.
  end to end    over the whole surface, with and without the closure.

And the resolved points that lie where a declaration refused for a cycle met the
rule it was declared against. Pooled by protocol, beside each run's own reading.
It reads the truth, so it names its surfaces: the space, uniform over the
134,400 points, and the corpus, as the cases arrive.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The engine is the published one.** For each base, `rows.fill`'s share of
     the order's room over the space is `O-b`'s or `K-f`'s as published, at the
     published precision. Its end to end with every edge is this reading's.
  2. **The masks are the engine.** On every corpus case of every base, the direct
     masks give `PriorityEngine.decide`'s outcome and queue. The closure masks
     give a closure decided case by case.
  3. **The closure changes no decision.** Every point the engine as it is
     decides keeps its queue. No IMPASSE is added, and no CONFLICT appears.
  4. **STOP 0.** The hidden policy's engine, read through the closure, is still
     1.0000 on the corpus and over the space.
  5. **The truth is the records'.** On every corpus case the truth masks give
     the label every base's record carries.

It refuses to write if any fails, and while the plan is unsigned, like every
writer of the package.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  1. **Under a forced placement, the closure resolves every CONFLICT.** In every
     run of v1e, v2e and v2b with a CONFLICT point over the space, it resolves
     all of them.
  2. **Without one, it resolves few.** In every run of v1 with a CONFLICT point
     over the space, it resolves less than half of them.
  3. **Where it resolves, it decides as a coin would.** Pooled over v2b's three
     runs, over the space, the closure is right on a share of the resolved
     points within 0.10 of a coin's.
  4. **A ranking does better.** Pooled over v2b's runs, over the space, the
     Stage C ranking is right on more of the resolved points than the closure.
  5. **It buys little over the function.** In every v2b run, the closure adds
     less than 0.01 to the end to end over the space.

A run with no CONFLICT point over the space is named and left out of the first
two clauses. With no resolved point in v2b, the third and fourth have no
reading.

**What the drafter had seen**:
  - `FINDINGS_BLIND.md`, `score.json`, `readings.json` and `cycles.json`. These
    include each v2b run's end to end over the space with every edge.
  - The share of the room the declared arm resolved on the half without the
    keyword: about 0.95 in run 1, all of it in run 2, nearly all in run 3.
  - The 20 refused declarations of run 1, of which order answers later installed
    6 the other way.
  - `PLAN_OVERLAP.md`'s published `O-b` shares, for gate 1.
  - The engine's code.

**Not seen**: any closure decision, any count of CONFLICT points in any final
base, any truth on those points, and the hidden policy's rules.

**What is close to known, and what is bet.** The first clause is close to known.
Under v1e, v2e and v2b every rule is born placed against every earlier rule of
another queue it overlaps. Of the declarations refused, a contradiction leaves
the pair nested, for subsumption to order. A cycle leaves it ordered through
the rule that closed it. So no two rules of different queues are left unordered,
and the closure should resolve every point. The clause fails only if that
argument misses something. The other four are the bets:
  - the second, that without a forced placement the base leaves pairs no chain
    orders;
  - the third and fourth, that the base's order beyond the keyword points the way
    `K-b` and `K-c` found the declarations it is made of point;
  - the fifth, that the points are few.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: asked for after `PLAN_BLIND.md`'s verdicts existed and after
`blind/cycles.py` named the mechanism, with the expectation above written before
the reading and committed before it ran. Not a signed row, not on `STATUS.md`'s
scoreboard, not a calibration event. No verdict moves. Zero API calls.

Usage:  PYTHONHASHSEED=0 python3 -m blind.closure
"""

from __future__ import annotations

import json
import sys
from typing import Any

from harness.domain import ATTRIBUTES, generate_corpus
from harness.dsl import Condition
from harness.provenance import describe, environment

from authorship import gates as egates
from reuse import structure as st
from rung2.engine2 import EDGE_CYCLE, PriorityEngine, Space
from rung2.hidden_priority import build_hidden_engine
from rung3.order_search_ls import space_truth_masks
from rung3.queue_hierarchy_floor import STAGE_C_HIERARCHY

from . import plan, rows

READ_PATH = plan.OUT / "closure.json"
PROTOCOLS = ("v1", "v1e", "v2e", "v2b")
FORCED = ("v1e", "v2e", "v2b")         # the protocols that place every overlap
COIN_BAND = 0.10                       # clause 3
MAX_GAIN = 0.01                        # clause 5
PROVENANCE = (
    "POST-RUN: asked for after PLAN_BLIND.md's verdicts existed and after "
    "blind/cycles.py named the mechanism. The expectation in the module's docstring "
    "was written before the reading and committed before it ran. Not a signed row; "
    "no verdict moves.")
COUNTS = ("conflicts", "resolved", "closure", "overruled", "neither", "ranking",
          "in_refused_regions", "direct_correct", "closure_correct", "n")


def record_path(protocol: str, rep: int):
    return plan.run_path(rep) if protocol == "v2b" else plan.BASELINES[protocol](rep)


# ---------------------------------------------------------------------------
# The two engines, by masks
# ---------------------------------------------------------------------------

def ancestors(engine: PriorityEngine) -> dict[str, set[str]]:
    """Every rule that reaches each rule, through subsumption and declared edges
    together: what defeats it under the closure, wherever it matches."""
    out = {}
    for r in engine.rules:
        seen: set[str] = set()
        stack = list(engine.beats_me(r.rule_id))
        while stack:
            cur = stack.pop()
            if cur not in seen:
                seen.add(cur)
                stack.extend(engine.beats_me(cur))
        out[r.rule_id] = seen
    return out


def undefeated(engine: PriorityEngine, beaters: dict[str, set[str]]) -> dict[str, int]:
    """Where each rule is undefeated: its extension, less that of every rule in
    `beaters`. With `beats_me` it is `rows.undefeated_masks`."""
    out = {}
    for r in engine.rules:
        dominated = 0
        for b in beaters[r.rule_id]:
            dominated |= engine.ext[b]
        out[r.rule_id] = engine.ext[r.rule_id] & ~dominated
    return out


def by_queue(masks: dict[str, int], action: dict[str, str]) -> dict[str, int]:
    out: dict[str, int] = {}
    for rid, m in masks.items():
        out[action[rid]] = out.get(action[rid], 0) | m
    return out


def cover(queues: dict[str, int]) -> tuple[int, int]:
    """The points some queue's undefeated rules reach, and those two or more
    queues reach: covered, and in CONFLICT."""
    one = two = 0
    for m in queues.values():
        two |= one & m
        one |= m
    return one, two


def engines(engine: PriorityEngine) -> dict[str, dict[str, int]]:
    """The undefeated rules' masks by queue, as the engine is and under the
    closure."""
    action = {r.rule_id: r.action for r in engine.rules}
    direct = {r.rule_id: set(engine.beats_me(r.rule_id)) for r in engine.rules}
    return {"direct": by_queue(undefeated(engine, direct), action),
            "closure": by_queue(undefeated(engine, ancestors(engine)), action)}


def decide_closure(engine: PriorityEngine, beaters: dict[str, set[str]], case) -> tuple[str, set[str]]:
    """A case decided under the closure, rule by rule: the outcome and the
    queues left undefeated."""
    matched = [r for r in engine.rules if r.matches(case)]
    if not matched:
        return "IMPASSE", set()
    ids = {r.rule_id for r in matched}
    queues = {r.action for r in matched if not (beaters[r.rule_id] & ids)}
    return ("ACTION" if len(queues) == 1 else "CONFLICT"), queues


def point_of(space: Space, case) -> int:
    """The case's single bit in `Space`'s convention."""
    return space.extension([Condition(a, "eq", getattr(case, a)) for a in ATTRIBUTES])


def queues_at(queues: dict[str, int], bit: int) -> set[str]:
    return {q for q, m in queues.items() if m & bit}


# ---------------------------------------------------------------------------
# What the closure resolves, and who is right there
# ---------------------------------------------------------------------------

def at_least(queues: dict[str, int]) -> list[int]:
    """`out[k]`: the points k queues or more reach. `out[0]` is every point."""
    out = [-1]
    for m in queues.values():
        out.append(0)
        for k in range(len(out) - 1, 0, -1):
            out[k] |= out[k - 1] & m
    return out


def exactly(k_mask: list[int], k: int) -> int:
    return k_mask[k] & ~(k_mask[k + 1] if k + 1 < len(k_mask) else 0)


def read_space(q: dict[str, dict[str, int]], tmask: dict[str, int], n: int,
               refused: int) -> dict[str, Any]:
    """The counts over the space: points, and the coin's expected hits."""
    direct, closure = q["direct"], q["closure"]
    one_d, two_d = cover(direct)
    one_c, two_c = cover(closure)
    resolved = two_d & ~two_c
    right_c = 0
    for a, m in closure.items():
        right_c |= m & resolved & tmask.get(a, 0)
    contention_right = 0
    for a, m in direct.items():
        contention_right |= m & resolved & tmask.get(a, 0)
    assigned = ranked_right = 0
    for a in STAGE_C_HIERARCHY:
        pick = direct.get(a, 0) & resolved & ~assigned
        assigned |= pick
        ranked_right |= pick & tmask.get(a, 0)
    k_mask = at_least(direct)
    coin = sum((exactly(k_mask, k) & resolved & contention_right).bit_count() / k
               for k in range(2, len(k_mask)))
    only_d, only_c = one_d & ~two_d, one_c & ~two_c
    return {"n": n, "conflicts": two_d.bit_count(), "resolved": resolved.bit_count(),
            "closure": right_c.bit_count(),
            "overruled": (contention_right & ~right_c).bit_count(),
            "neither": (resolved & ~contention_right).bit_count(),
            "coin": coin, "ranking": ranked_right.bit_count(),
            "in_refused_regions": (resolved & refused).bit_count(),
            "direct_correct": sum((only_d & m & tmask.get(a, 0)).bit_count()
                                  for a, m in direct.items()),
            "closure_correct": sum((only_c & m & tmask.get(a, 0)).bit_count()
                                   for a, m in closure.items())}


def read_corpus(q: dict[str, dict[str, int]], bits: list[int], truth: list[str],
                refused: int) -> dict[str, Any]:
    """The same counts over the corpus cases, as they arrive."""
    out = {k: 0 for k in COUNTS} | {"coin": 0.0, "n": len(bits)}
    for bit, t in zip(bits, truth):
        d, c = queues_at(q["direct"], bit), queues_at(q["closure"], bit)
        if len(d) == 1:
            out["direct_correct"] += t in d
        if len(c) == 1:
            out["closure_correct"] += t in c
        if len(d) < 2:
            continue
        out["conflicts"] += 1
        if len(c) != 1:
            continue
        out["resolved"] += 1
        out["in_refused_regions"] += bool(refused & bit)
        out["closure"] += t in c
        out["overruled"] += t in d and t not in c
        out["neither"] += t not in d
        out["coin"] += (t in d) / len(d)
        out["ranking"] += next(a for a in STAGE_C_HIERARCHY if a in d) == t
    return out


def shares(counts: dict[str, Any]) -> dict[str, Any]:
    """Each count over the resolved points, the resolved over the conflicts, and
    the end to end with and without the closure."""
    r, n = counts["resolved"], counts["n"]
    out = {k: (counts[k] / r if r else None)
           for k in ("closure", "overruled", "neither", "coin", "ranking",
                     "in_refused_regions")}
    out["resolved_of_conflicts"] = (r / counts["conflicts"] if counts["conflicts"]
                                    else None)
    out["e2e"] = counts["direct_correct"] / n
    out["e2e_closure"] = counts["closure_correct"] / n
    out["gain"] = out["e2e_closure"] - out["e2e"]
    return out


def pooled(readings: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {k: sum(r[k] for r in readings) for k in COUNTS} | {
        "coin": sum(r["coin"] for r in readings)}
    return {"counts": counts, "shares": shares(counts)}


def refused_region(record: dict, ext: dict[str, int]) -> int:
    """Where a declaration refused for a cycle met the rule it was declared
    against, on any channel."""
    out = 0
    for w, l, why in record.get("edge_log") or []:
        if why == EDGE_CYCLE and w in ext and l in ext:
            out |= ext[w] & ext[l]
    return out


# ---------------------------------------------------------------------------
# One base
# ---------------------------------------------------------------------------

def read_base(record: dict, space: Space, tmask: dict[str, int], corpus,
              bits: list[int]) -> dict[str, Any]:
    engine, problems = egates.rebuild_final(record, space)
    q = engines(engine)
    refused = refused_region(record, engine.ext)
    truth = [t for t, _ in egates.labels_of(record)]
    on_space = read_space(q, tmask, space.n, refused)
    on_corpus = read_corpus(q, bits, truth, refused)
    beaters = ancestors(engine)
    agree = True
    for case, bit in zip(corpus, bits):
        outcome, winner, involved = engine.decide(case)
        d = queues_at(q["direct"], bit)
        want = ({winner.action} if outcome == "ACTION"
                else {r.action for r in involved} if outcome == "CONFLICT" else set())
        c_outcome, c_queues = decide_closure(engine, beaters, case)
        agree = agree and d == want and (len(d) >= 2) == (outcome == "CONFLICT")
        agree = agree and queues_at(q["closure"], bit) == c_queues
    one_d, two_d = cover(q["direct"])
    one_c, two_c = cover(q["closure"])
    kept = all((m & (one_d & ~two_d)) & ~(q["closure"].get(a, 0) & (one_c & ~two_c)) == 0
               for a, m in q["direct"].items())
    return {"space": {"counts": on_space, "shares": shares(on_space)},
            "corpus": {"counts": on_corpus, "shares": shares(on_corpus)},
            "rules": len(engine.rules),
            "acyclic": all(r.rule_id not in beaters[r.rule_id] for r in engine.rules),
            "gates": {"reinstall_problems": problems, "masks_are_the_engine": agree,
                      "no_decision_changes": kept and one_c == one_d and two_c & ~two_d == 0,
                      "labels": truth}}


def published_share(protocol: str, rep: int, overlap: dict, score: dict) -> tuple[Any, float]:
    """`O-b`'s share over the space as published, and its precision."""
    if protocol == "v2b":
        return score["runs"][rep - 1]["K-f"]["fills"]["all"]["space_full"]["share"], 5e-7
    if protocol == "v2e":
        return overlap["runs"][rep - 1]["O-b"], 5e-7
    return overlap["baselines"][protocol]["o_b_shares"][rep - 1], 5e-5


# ---------------------------------------------------------------------------
# The gates and the expectation
# ---------------------------------------------------------------------------

def check(bases: dict, records: dict, space: Space, tmask: dict[str, int], corpus,
          bits: list[int], overlap: dict, score: dict) -> list[dict]:
    out = []
    truth_at = [next(a for a, m in tmask.items() if m & bit) for bit in bits]
    for (protocol, rep), b in bases.items():
        rec = records[(protocol, rep)]
        filled = rows.fill(rec, space, tmask, space.full)
        pub, tol = published_share(protocol, rep, overlap, score)
        same = (filled["share"] is None if pub is None
                else filled["share"] is not None and abs(filled["share"] - pub) <= tol)
        e2e_same = abs(filled["e2e"] - b["space"]["shares"]["e2e"]) < 1e-12
        g = b["gates"]
        out += [
            {"gate": 1, "base": f"{protocol} {rep}", "what": "the engine is the published one",
             "measured": filled["share"], "published": pub,
             "passes": same and e2e_same and not g["reinstall_problems"]},
            {"gate": 2, "base": f"{protocol} {rep}", "what": "the masks are the engine",
             "passes": g["masks_are_the_engine"] and b["acyclic"]},
            {"gate": 3, "base": f"{protocol} {rep}", "what": "the closure changes no decision",
             "passes": g["no_decision_changes"]},
            {"gate": 5, "base": f"{protocol} {rep}", "what": "the truth is the records'",
             "passes": g["labels"] == truth_at},
        ]
    hidden, _, _ = build_hidden_engine(space)
    q = engines(hidden)
    one, two = cover(q["closure"])
    on_space = sum(((one & ~two) & m & tmask.get(a, 0)).bit_count()
                   for a, m in q["closure"].items()) / space.n
    beaters = ancestors(hidden)
    on_corpus = sum(decide_closure(hidden, beaters, c)[1] == {t}
                    for c, t in zip(corpus, truth_at)) / len(corpus)
    out.append({"gate": 4, "base": "the hidden policy", "what": "STOP 0 through the closure",
                "measured": {"space": on_space, "corpus": on_corpus},
                "passes": on_space == 1.0 and on_corpus == 1.0})
    return out


def read_expectation(bases: dict) -> list[dict]:
    def resolved_share(protocol, rep):
        s = bases[(protocol, rep)]["space"]["counts"]
        return s["resolved"] / s["conflicts"] if s["conflicts"] else None

    forced = {f"{p} {r}": resolved_share(p, r) for p in FORCED for r in plan.BASELINE_REPS}
    v1 = {f"v1 {r}": resolved_share("v1", r) for r in plan.BASELINE_REPS}
    v2b = pooled([bases[("v2b", r)]["space"]["counts"] for r in plan.BASELINE_REPS])
    s = v2b["shares"]
    gains = {f"v2b {r}": bases[("v2b", r)]["space"]["shares"]["gain"]
             for r in plan.BASELINE_REPS}
    read3 = None if s["closure"] is None else abs(s["closure"] - s["coin"]) <= COIN_BAND
    read4 = None if s["closure"] is None else s["ranking"] > s["closure"]
    return [
        {"clause": 1, "what": "under v1e, v2e and v2b the closure resolves every CONFLICT "
                              "point over the space, in every run with one",
         "reading": forced,
         "holds": all(x == 1.0 for x in forced.values() if x is not None)},
        {"clause": 2, "what": "under v1 it resolves less than half of them, in every run "
                              "with one",
         "reading": v1, "holds": all(x < 0.5 for x in v1.values() if x is not None)},
        {"clause": 3, "what": "pooled over v2b, the closure's share right on the resolved "
                              "points is within 0.10 of a coin's",
         "reading": [s["closure"], s["coin"]], "holds": read3},
        {"clause": 4, "what": "pooled over v2b, the Stage C ranking is right on more of the "
                              "resolved points than the closure",
         "reading": [s["ranking"], s["closure"]], "holds": read4},
        {"clause": 5, "what": "in every v2b run the closure adds less than 0.01 to the end "
                              "to end over the space",
         "reading": gains, "holds": all(g < MAX_GAIN for g in gains.values())},
    ]


def main(argv: list[str] | None = None) -> int:
    if argv:
        print(__doc__)
        return 2
    plan.refuse_unsigned(f"blind/closure.py writes {READ_PATH}")
    score = json.loads(plan.SCORE_PATH.read_text())
    overlap = json.loads(plan.OVERLAP_SCORE.read_text())
    space = Space()
    tmask = space_truth_masks(space)
    corpus = generate_corpus(plan.N, seed=plan.SEED)
    bits = [point_of(space, c) for c in corpus]
    records = {(p, r): json.loads(record_path(p, r).read_text())
               for p in PROTOCOLS for r in plan.BASELINE_REPS}
    bases = {key: read_base(rec, space, tmask, corpus, bits) for key, rec in records.items()}
    checked = check(bases, records, space, tmask, corpus, bits, overlap, score)
    for g in checked:
        print(f"  gate {g['gate']} {g['base']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    for b in bases.values():
        del b["gates"]["labels"]
    READ_PATH.write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "provenance": PROVENANCE,
        "source": {"records": {f"{p} {r}": str(record_path(p, r)) for p, r in records},
                   "score": str(plan.SCORE_PATH), "overlap_score": str(plan.OVERLAP_SCORE)},
        "surfaces": {"space": "the exhaustive space, 134,400 points, uniform",
                     "corpus": "the 2,000 cases of seed 17, as they arrive"},
        "constants": {"COIN_BAND": COIN_BAND, "MAX_GAIN": MAX_GAIN,
                      "ranking": STAGE_C_HIERARCHY},
        "gates": checked,
        "bases": {f"{p} {r}": b for (p, r), b in bases.items()},
        "pooled": {p: {s: pooled([bases[(p, r)][s]["counts"] for r in plan.BASELINE_REPS])
                       for s in ("space", "corpus")} for p in PROTOCOLS},
        "expectation": read_expectation(bases),
    }), indent=2, default=str) + "\n")
    print(f"\n-> {READ_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
