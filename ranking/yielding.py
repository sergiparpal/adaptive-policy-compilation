"""
WHICH EDGE OF A CYCLE YIELDS, UNDER THE MODEL'S OWN RANKINGS. `blind/yielding.py`
read which edge of a cycle should yield on the twelve paid bases of rung 2's
loop, under five priorities over the declarations. Beyond the keyword its
ranking arm chose better than 96% of a coin's draws. That arm's ranking is Stage
C's, which was chosen with the hidden policy's answer key in hand
(`FINDINGS_BLIND.md`, erratum of 2026-10-16), so a deployed system could not
apply it. `PLAN_RANKING.md` produced two rankings that read no label, the one the
model states and the one its pairwise answers reveal, and put neither in that
arm. This puts each in Stage C's place. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
Which edge of a cycle yields is a priority over the declarations: the engine
installs them in turn and refuses each that would close a cycle.
`blind/yielding.py`'s ranking arm installs first the declarations whose winner's
queue the ranking puts above the loser's, then those within one queue, then
those against it, each group in arrival order, so an edge against the ranking
yields first. Put a ranking the model gives in that arm: does it choose which
edge yields as the key's ranking does, or as a draw does?

**The trajectory is held fixed**, as there. Each run's final rules and every
declaration it made are read as they are, and only which declarations the
engine keeps changes.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
`blind/yielding.py`'s bases, declarations, engines, surfaces and halves, through
its own functions, called and not edited. Three rankings go in its ranking arm:

  stage_c   `rung3/queue_hierarchy_floor.py`'s `STAGE_C_HIERARCHY`: the
            published ranking arm, installed again here as gate 2's anchor.
  revealed  the model's revealed ranking on the learned base, Copeland over its
            1,479 declared pairwise answers: `sample.json`'s
            `revealed.learned.order`, which gate 3 rebuilds from the answers.
  stated    the ranking of each of the 24 valid asks of `ask_session.json`, six
            distinct ones. The stated arm is read on the median of the 24 asks,
            as `M-e` was, each ask taking its ranking's count.

Beside them, `blind/yielding.py`'s own arms, arrival, recency, Stage C's and the
oracle's, and its coin, 200 seeded shuffles per base, all recomputed and gated
to `yielding.json` figure for figure. For each base, arm and engine: the counts
`blind/yielding.py` reads against the arrival arm, over the space and the
corpus, whole and by halves of the space, and the declarations each arm refused,
with how many of them the keyword's queue wins. Pooled over the bases with a
refusal for a cycle, and, for each model arm, the share of the coin's draws right
on at least as many points.

**Not read**: the hidden policy's revealed ranking, Copeland over the model's
answers about that policy's own pairs. It is one adjacent swap from Stage C's,
and it was asked about rules a deployed system would not hold.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **`blind/yielding.py`'s gates pass again**, its eight, the hidden policy kept
     whole under every order among them.
  2. **The instrument is `yielding.json`'s.** Recomputed, every count of every
     base, arm, engine, surface and half, the coin's summaries, the pool, the
     split of the coin's draws and the expectation's readings equal the record's,
     to the precision it publishes. And `stage_c`, installed by this module's
     ranking arm, installs in `blind.yielding.priority`'s order, refuses the
     declarations the record's ranking arm refuses and reads its counts, in every
     base.
  3. **The rankings are `PLAN_RANKING.md`'s records'.** The revealed ranking is
     the one Copeland gives over the declared answers again. The 24 asks are
     permutations of the eight queues, `score.json`'s asks in order, and their
     Borda aggregate is the one `score.json` publishes.
  4. **Every model arm is acyclic and full**, and **without a cycle it keeps the
     arrival arm's edges**, in every base.

It refuses to write if any fails, and while `PLAN_RANKING.md` is unsigned, like
every writer of the package. `--dry-run` runs the gates, prints pass or fail
and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Clauses 2 to 4 are read through the closure, where only direction differs, on
the half of the space without the keyword, the surface `PLAN_BLIND.md` reads,
pooled over the three bases with a refusal for a cycle: v2e's run 1 and v2b's
runs 1 and 3. That half is read first because `blind/yielding.py`'s three failed
clauses were decided on the other one. The keyword half, the whole space, rung
2's engine and the corpus are reported beside them and decide nothing.

  1. **Where the cycle is small, each model ranking lets yield an edge another
     arm already lets yield.** In v2e's run 1 the revealed arm refuses what the
     Stage C arm refuses, and every stated ranking what the recency arm refuses.
     In v2b's run 3 the revealed arm refuses what the arrival arm refuses, and
     every stated ranking what the Stage C arm refuses.
  2. **Neither ranking the model gives chooses as the key's does.** The revealed
     arm and the stated arm are each right on fewer points than the Stage C arm.
  3. **Each chooses as a draw does.** The revealed arm's right points and the
     stated arm's both lie inside the coin's central 90%.
  4. **The stated ranking chooses better than the revealed one.** The stated arm
     is right on more points than the revealed arm.
  5. **Neither lets the keyword rule's edges yield.** In no base does the
     revealed ranking or any stated ranking refuse a declaration whose winner is
     of `SECURITY_INCIDENT`.

**What the drafter had seen**:
  - `FINDINGS_BLIND.md` whole, with the section `blind/yielding.py` wrote. That
    section gives each deterministic arm's right points through the closure over
    the space, by base, and pooled by half. It gives the coin's mean and central
    90%, rung 2's engine in v2b's run 1, and which declarations each
    deterministic arm refuses in each base, in the words of *Which edges yield*.
  - `FINDINGS_RANKING.md` whole: the three rankings, their lookups and their
    readings on `K-b`'s and `K-e`'s pairs.
  - The queues of the rules on the two small cycles, looked up to draft clause 1.
    In v2e's run 1: `R0001` T1_GENERAL, `R0007` BILLING_SPECIALIST, `R0017`
    SECURITY_INCIDENT, `R0024` T2_TECHNICAL. In v2b's run 3: `R0004` and `R0020`
    T2_TECHNICAL, `R0005` SELF_SERVICE_DEFLECT.
  - The six distinct stated rankings and how many asks gave each.
  - `blind/yielding.py`'s code and tests, and how long it takes.
  - The gates, run before this commit, which print pass or fail.

**Not seen**:
  - any count of an arm under a model ranking;
  - which declarations either ranking refuses in v2b's run 1;
  - the queues of the rules on that run's cycles beyond those
    `FINDINGS_BLIND.md` names;
  - `yielding.json` beyond what that record prints;
  - the coin's draws one by one.

**What is close to known, and what is bet.** Clause 1 follows from the queues
and the rankings, if the two small cycles are what `FINDINGS_BLIND.md` says they
are. With it, beyond the keyword and against the arrival arm:
  - the revealed arm reads +270 in v2e's run 1 and 0 in v2b's run 3;
  - the stated arm reads 0 and −115.

So clauses 2 to 4 are bets on v2b's run 1 alone. There the arrival arm refused
32 declarations and the Stage C arm 31. Beyond the keyword, by that record's
figures per base and pooled, the Stage C arm gained 700 points there, the
recency arm 560 and the oracle 1,000. Pooled, against the coin's 68,840 to
70,650, what each clause needs in that run:
  - clause 2: the revealed arm below +585 and the stated arm below +970;
  - clause 3: the revealed arm between −1,250 and +560, and the stated arm
    between −865 and +945;
  - clause 4: the stated arm 386 points or more above the revealed arm.

The argument is the self-service rules:
  - Most of the Stage C arm's refusals in that run are self-service or general
    rules declared over technical ones.
  - The revealed ranking differs from Stage C's on four queue pairs:
    ONCALL_ESCALATION against SECURITY_INCIDENT, ACCOUNT_MANAGER against
    T3_ENGINEERING and BILLING_SPECIALIST, and SELF_SERVICE_DEFLECT against
    T2_TECHNICAL, which it puts above. If the technical rules of those refusals
    are T2_TECHNICAL's, as `R0024` was in v2e's run 1, the last pair is theirs.
    The revealed arm then keeps the self-service edges the Stage C arm lets
    yield, and lets technical ones yield instead.
  - The stated ranking differs from Stage C's on seven: ACCOUNT_MANAGER against
    BILLING_SPECIALIST, T1_GENERAL, T2_TECHNICAL and T3_ENGINEERING,
    BILLING_SPECIALIST against T1_GENERAL and T2_TECHNICAL, and T1_GENERAL
    against SELF_SERVICE_DEFLECT. None of the refusals `FINDINGS_BLIND.md` names
    for the Stage C arm in that run involves them.
  - On `K-b`'s pairs the two rankings read alike, 0.5563 and 0.5496. So clause 4
    bets that on the edges that close cycles the self-service pairs decide.

Clause 5 bets that no cycle closes among the declarations a model ranking
installs first.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: asked for after `PLAN_RANKING.md`'s verdicts existed and after
`blind/yielding.py` read which edge of a cycle should yield, with the
expectation above written before the reading and committed before it ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. No verdict
moves. Zero API calls.

Usage:  PYTHONHASHSEED=0 python3 -m ranking.yielding
        PYTHONHASHSEED=0 python3 -m ranking.yielding --dry-run   # the gates; writes nothing
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from typing import Any, Sequence

from harness.domain import generate_corpus
from harness.provenance import describe, environment

from authorship import gates as egates
from blind import closure, rows
from blind import plan as blind_plan
from blind import yielding as by
from reuse import structure as st
from rung2.engine2 import EDGE_CYCLE, Space
from rung3.order_search_ls import space_truth_masks
from rung3.queue_hierarchy_floor import STAGE_C_HIERARCHY

from . import gates, plan
from . import instrument as I

READ_PATH = plan.OUT / "yielding.json"
SESSION_PATH = plan.ask_path("session")
HALF = "outside"                          # PLAN_BLIND.md's surface, read first
SMALL = {("v2e", 1): {"revealed": "ranking", "stated": "recency"},   # clause 1: the
         ("v2b", 3): {"revealed": "arrival", "stated": "ranking"}}   # arm each refuses as
PROVENANCE = (
    "POST-RUN: asked for after PLAN_RANKING.md's verdicts existed and after "
    "blind/yielding.py read which edge of a cycle should yield. The expectation in "
    "the module's docstring was written before the reading and committed before it "
    "ran. Not a signed row; no verdict moves.")


# ---------------------------------------------------------------------------
# The ranking arm, with the ranking as an argument
# ---------------------------------------------------------------------------

def by_ranking(decls: list[dict], action: dict[str, str],
               hierarchy: Sequence[str]) -> list[dict]:
    """`blind.yielding.priority("ranking")` with `hierarchy` in Stage C's place:
    first the declarations whose winner's queue it ranks above the loser's, then
    those within one queue, then those against it, each group in arrival order.
    An edge against the ranking yields first."""
    rank = {q: i for i, q in enumerate(hierarchy)}

    def group(d: dict) -> int:
        a, b = rank[action[d["winner"]]], rank[action[d["loser"]]]
        return 0 if a < b else 1 if a == b else 2

    return sorted(by.ordered(decls), key=lambda d: (group(d), d["k"]))


def stated_rankings(session: dict) -> list[dict]:
    """The distinct rankings of the session's valid asks, the most asked first
    and ties by first ask, each with the asks that gave it."""
    seen: dict[tuple[str, ...], dict] = {}
    for r in session["rows"]:
        if r["valid"]:
            key = tuple(r["ranking"])
            seen.setdefault(key, {"order": list(key), "asks": []})["asks"].append(
                [r["pid"], r["pass"]])
    out = sorted(seen.values(), key=lambda s: -len(s["asks"]))   # stable
    for i, s in enumerate(out, 1):
        s["name"], s["n"] = f"stated_{i}", len(s["asks"])
    return out


def median_ask(values: dict[str, float], stated: Sequence[dict]) -> float:
    """The median over the valid asks, each ask taking its ranking's value."""
    return statistics.median(values[s["name"]] for s in stated for _ in range(s["n"]))


def rankings_of(sample: dict, stated: Sequence[dict]) -> dict[str, list[str]]:
    return {"stage_c": list(STAGE_C_HIERARCHY),
            "revealed": list(sample["revealed"]["learned"]["order"]),
            **{s["name"]: list(s["order"]) for s in stated}}


# ---------------------------------------------------------------------------
# One base
# ---------------------------------------------------------------------------

def read_rankings(record: dict, space: Space, tmask: dict[str, int],
                  mult: dict[int, int], outside: int,
                  rankings: dict[str, Sequence[str]]) -> dict[str, Any]:
    """Each ranking's arm on one base, against the arrival arm, as
    `blind.yielding.read_base` reads its own arms."""
    decls, _ = by.attribute(record)
    bare, _ = egates.rebuild_final(record, space, set())
    action = {r.rule_id: r.action for r in bare.rules}
    arrival_eng, _ = by.install(bare, by.priority("arrival", decls, action, bare.ext, tmask))
    m_arrival = by.masks(arrival_eng, tmask)
    arms: dict[str, Any] = {}
    for name, hierarchy in rankings.items():
        eng, refused = by.install(bare, by_ranking(decls, action, hierarchy))
        m = by.masks(eng, tmask)
        arms[name] = {
            "kept": len(by.edges_of(eng)),
            "refused": [by.brief(d) | {"queues": [action[d["winner"]], action[d["loser"]]]}
                        for d in refused],
            "keyword_refused": by.keyword_winners(refused, action),
            **by.reading(m, m_arrival, mult),
            "halves": by.by_half(m, m_arrival, mult, outside, space.full),
            "_acyclic_and_full": by.acyclic_and_full(eng, refused),
            "_one_with_arrival": by.edges_of(eng) == by.edges_of(arrival_eng),
        }
    blinds = [d["k"] for d in by.priority("ranking", decls, action, bare.ext, tmask)]
    mine = [d["k"] for d in by_ranking(decls, action, STAGE_C_HIERARCHY)]
    return {"cycle": any(d["verdict"] == EDGE_CYCLE for d in decls), "arms": arms,
            "_stage_c_order_is_blinds": mine == blinds}


def public(arm: dict) -> dict:
    return {k: v for k, v in arm.items() if not k.startswith("_")}


# ---------------------------------------------------------------------------
# Pooled, and the coin's draws
# ---------------------------------------------------------------------------

def pool_rankings(per_base: dict, names: Sequence[str]) -> dict[str, Any]:
    """Each ranking's counts summed over the bases with a cycle, whole and by
    halves of the space."""
    keys = [k for k, b in per_base.items() if b["cycle"]]

    def total(path) -> int:
        return sum(path(per_base[k]["arms"]) for k in keys)

    whole = {n: {e: {s: {c: total(lambda a, n=n, e=e, s=s, c=c: a[n][e][s][c])
                         for c in by.COUNTS} for s in by.SURFACES} for e in by.ENGINES}
             for n in names}
    halves = {n: {e: {h: {s: {c: total(lambda a, n=n, e=e, h=h, s=s, c=c:
                                       a[n]["halves"][e][h][s][c])
                              for c in by.COUNTS} for s in by.SURFACES} for h in by.HALVES}
                  for e in by.ENGINES} for n in names}
    return {"bases": [f"{p} {r}" for p, r in keys], "whole": whole, "halves": halves}


def coin_draws(bases: dict) -> dict[str, Any]:
    """The coin's right points summed over the bases with a cycle, draw by draw,
    whole and by halves, per engine and surface."""
    keys = [k for k, b in bases.items() if b["cycle"]]
    whole = {e: {s: [sum(bases[k]["_draws"][i][e][s]["right"] for k in keys)
                     for i in range(by.N_COIN)] for s in by.SURFACES} for e in by.ENGINES}
    halves = {e: {h: {s: [sum(bases[k]["_draws_halves"][i][e][h][s]["right"] for k in keys)
                          for i in range(by.N_COIN)] for s in by.SURFACES}
                  for h in by.HALVES} for e in by.ENGINES}
    return {"whole": whole, "halves": halves}


def at_least(draws: Sequence[float], value: float) -> float:
    """The share of the coin's draws right on at least `value` points."""
    return sum(x >= value for x in draws) / len(draws)


def stated_median(pooled: dict, stated: Sequence[dict]) -> dict[str, Any]:
    """The stated arm: every pooled count's median over the 24 asks."""
    names = [s["name"] for s in stated]

    def med(get) -> float:
        return median_ask({n: get(n) for n in names}, stated)

    whole = {e: {s: {c: med(lambda n, e=e, s=s, c=c: pooled["whole"][n][e][s][c])
                     for c in by.COUNTS} for s in by.SURFACES} for e in by.ENGINES}
    halves = {e: {h: {s: {c: med(lambda n, e=e, h=h, s=s, c=c:
                                 pooled["halves"][n][e][h][s][c])
                          for c in by.COUNTS} for s in by.SURFACES} for h in by.HALVES}
              for e in by.ENGINES}
    return {"whole": whole, "halves": halves}


def shares(pooled: dict, coin: dict, names: Sequence[str]) -> dict[str, Any]:
    """For each arm, the share of the coin's draws right on at least as many
    points, per engine and surface, whole and by halves."""
    return {n: {"whole": {e: {s: at_least(coin["whole"][e][s],
                                          pooled["whole"][n][e][s]["right"])
                              for s in by.SURFACES} for e in by.ENGINES},
                "halves": {e: {h: {s: at_least(coin["halves"][e][h][s],
                                               pooled["halves"][n][e][h][s]["right"])
                                   for s in by.SURFACES} for h in by.HALVES}
                           for e in by.ENGINES}}
            for n in names}


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def roundtrip(x: Any) -> Any:
    """What a record would carry of `x`: rounded as `blind/yielding.py` writes."""
    return json.loads(json.dumps(st._rounded(x), default=str))


def agrees(a: Any, b: Any) -> bool:
    """`ranking.gates.close`, structure for structure."""
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(agrees(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(agrees(x, y) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool):
        return a is b
    return gates.close(a, b)


def published_view(bases: dict) -> dict:
    """`blind.yielding.main`'s bases, as it writes them."""
    return {f"{p} {r}": {k: v for k, v in b.items() if not k.startswith("_")}
            for (p, r), b in bases.items()}


def same_as_blinds(mine: dict, theirs: dict, halves: dict) -> bool:
    """The Stage C ranking through this module's arm, against the record's
    ranking arm on one base."""
    return (mine["kept"] == theirs["kept"]
            and [d["k"] for d in mine["refused"]] == [d["k"] for d in theirs["refused"]]
            and all(mine[e] == theirs[e] for e in by.ENGINES)
            and mine["halves"] == halves)


def check(published: dict, recomputed: dict, per_base: dict, bases: dict,
          sample: dict, session: dict, score: dict, stated: Sequence[dict],
          revealed_again: Sequence[str]) -> list[dict]:
    """Gates 1 to 4. `recomputed` is what `blind/yielding.py` writes, computed
    again here."""
    blind_gates = recomputed["gates"]
    out = [{"gate": 1, "what": "blind/yielding.py's gates pass again",
            "passes": all(g["passes"] for g in blind_gates)}]
    parts = (("gates", ["gates"]), ("bases", ["bases"]), ("pooled", ["pooled"]),
             ("expectation", ["expectation"]),
             ("halves", ["added_after_the_first_run", "halves"]),
             ("by_what_the_coin_refused", ["added_after_the_second_run",
                                           "by_what_the_coin_refused"]))
    for name, path in parts:
        theirs = published
        for p in path:
            theirs = theirs[p]
        out.append({"gate": 2, "what": f"yielding.json's {name} come back",
                    "passes": agrees(roundtrip(recomputed[name]), theirs)})
    out.append({"gate": 2, "what": "stage_c installs in blind.yielding.priority's order",
                "passes": all(b["_stage_c_order_is_blinds"] for b in per_base.values())})
    out.append({"gate": 2, "what": "stage_c refuses and reads as the record's ranking arm",
                "passes": all(same_as_blinds(per_base[k]["arms"]["stage_c"],
                                             bases[k]["arms"]["ranking"],
                                             bases[k]["_halves"]["ranking"])
                              for k in per_base)})

    valid = [r for r in session["rows"] if r["valid"]]
    asked = [r["ranking"] for r in valid]
    out += [
        {"gate": 3, "what": "the revealed ranking is Copeland over the answers again",
         "passes": list(sample["revealed"]["learned"]["order"]) == list(revealed_again)},
        {"gate": 3, "what": "every valid ask is a permutation of the eight queues",
         "passes": len(valid) >= plan.MIN_VALID_ASKS
         and all(sorted(r) == sorted(plan.QUEUES) for r in asked)},
        {"gate": 3, "what": "the asks are score.json's, in order",
         "passes": asked == [a["ranking"] for a in score["M-f"]["asks"]]},
        {"gate": 3, "what": "their Borda aggregate is score.json's",
         "passes": I.borda(asked) == score["M-f"]["borda"]["order"]},
        {"gate": 3, "what": "the distinct stated rankings cover the valid asks",
         "passes": sum(s["n"] for s in stated) == len(valid)},
    ]
    arms = [(k, n, a) for k, b in per_base.items() for n, a in b["arms"].items()]
    out += [
        {"gate": 4, "what": "every model arm is acyclic and full",
         "passes": all(a["_acyclic_and_full"] for _, _, a in arms)},
        {"gate": 4, "what": "without a cycle every model arm keeps the arrival arm's edges",
         "passes": all(a["_one_with_arrival"] for k, _, a in arms
                       if not per_base[k]["cycle"])},
    ]
    return out


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(per_base: dict, bases: dict, halves: dict, pooled: dict,
                     stated: Sequence[dict]) -> list[dict]:
    """The five clauses. `bases` and `halves` are `blind/yielding.py`'s, computed
    again; `pooled` is this module's, with `stated` the distinct asks."""
    def ks(refused: list[dict]) -> list[int]:
        return sorted(d["k"] for d in refused)

    small = {}
    for key, want in SMALL.items():
        mine, theirs = per_base[key]["arms"], bases[key]["arms"]
        small[f"{key[0]} {key[1]}"] = {
            "revealed": {"as": want["revealed"],
                         "same": ks(mine["revealed"]["refused"])
                         == ks(theirs[want["revealed"]]["refused"])},
            "stated": {"as": want["stated"],
                       "same": all(ks(mine[s["name"]]["refused"])
                                   == ks(theirs[want["stated"]]["refused"])
                                   for s in stated)}}

    def right(source: dict, arm: str) -> float:
        return source[arm]["closure"][HALF]["space"]["right"]

    ranking = right(halves["pooled"]["arms"], "ranking")
    revealed = right(pooled["halves"], "revealed")
    told = median_ask({s["name"]: right(pooled["halves"], s["name"]) for s in stated},
                      stated)
    lo, hi = halves["pooled"]["coin"][HALF]["closure"]["space"]["right"]["central"]
    keyword = {f"{p} {r}": {n: a["keyword_refused"] for n, a in b["arms"].items()
                            if n != "stage_c"}
               for (p, r), b in per_base.items()}
    return [
        {"clause": 1, "what": "in v2e's run 1 the revealed arm refuses as the Stage C arm and "
                              "every stated ranking as recency; in v2b's run 3 the revealed "
                              "arm as arrival and every stated ranking as the Stage C arm",
         "reading": small,
         "holds": all(x["revealed"]["same"] and x["stated"]["same"] for x in small.values())},
        {"clause": 2, "what": "pooled beyond the keyword through the closure, the revealed "
                              "and the stated arm each right on fewer points than the Stage "
                              "C arm",
         "reading": {"revealed": revealed, "stated": told, "stage_c": ranking},
         "holds": revealed < ranking and told < ranking},
        {"clause": 3, "what": "pooled beyond the keyword through the closure, the revealed "
                              "and the stated arm inside the coin's central 90%",
         "reading": {"revealed": revealed, "stated": told, "coin_central": [lo, hi]},
         "holds": lo <= revealed <= hi and lo <= told <= hi},
        {"clause": 4, "what": "pooled beyond the keyword through the closure, the stated "
                              "arm right on more points than the revealed arm",
         "reading": {"stated": told, "revealed": revealed},
         "holds": told > revealed},
        {"clause": 5, "what": "in no base does a model ranking refuse a declaration the "
                              "keyword's queue wins",
         "reading": keyword,
         "holds": all(v == 0 for b in keyword.values() for v in b.values())},
    ]


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------

def load(path, what: str) -> dict:
    if not path.exists():
        sys.exit(f"\nREFUSED: {what} is not there: {path}\n")
    return json.loads(path.read_text())


def report(checked: list[dict]) -> None:
    for g in checked:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Which edge of a cycle yields, under the "
                                             "model's own rankings (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run the gates, print pass or fail, write nothing")
    args = ap.parse_args(argv)
    if not args.dry_run:
        plan.refuse_unsigned(f"ranking/yielding.py writes {READ_PATH}")

    published = load(by.READ_PATH, "blind/yielding.py's record")
    published_closure = load(closure.READ_PATH, "blind/closure.py's record")
    sample = load(plan.SAMPLE_PATH, "Stage A's record")
    session = load(SESSION_PATH, "the session's record")
    score = load(plan.SCORE_PATH, "Stage C's record")

    space = Space()
    tmask = space_truth_masks(space)
    corpus = generate_corpus(blind_plan.N, seed=blind_plan.SEED)
    bits = [closure.point_of(space, c) for c in corpus]
    mult = by.multiplicity(bits)
    outside = rows.outside_mask(space)
    records = {(p, r): json.loads(closure.record_path(p, r).read_text())
               for p in closure.PROTOCOLS for r in blind_plan.BASELINE_REPS}

    bases = {key: by.read_base(key, rec, space, tmask, mult, outside)
             for key, rec in records.items()}
    pool = by.pooled(bases)
    halves = by.halves_of(bases)
    recomputed = {"gates": by.check(bases, records, published_closure,
                                    by.stop_zero(space, tmask), tmask, bits),
                  "bases": published_view(bases), "pooled": pool,
                  "expectation": by.read_expectation(bases, pool), "halves": halves,
                  "by_what_the_coin_refused": by.keyword_split_of(bases)}

    stated = stated_rankings(session)
    rankings = rankings_of(sample, stated)
    per_base = {key: read_rankings(rec, space, tmask, mult, outside, rankings)
                for key, rec in records.items()}
    checked = check(published, recomputed, per_base, bases, sample, session, score,
                    stated, I.revealed_learned()[0])
    report(checked)
    if not all(g["passes"] for g in checked):
        if args.dry_run:
            print("\ndry run: a gate failed; nothing was written")
            return 1
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: every gate passes; nothing read beyond them, nothing written")
        return 0

    names = list(rankings)
    pooled = pool_rankings(per_base, names)
    coin = coin_draws(bases)
    expectation = read_expectation(per_base, bases, halves, pooled, stated)
    told = stated_median(pooled, stated)
    for x in expectation:
        print(f"  clause {x['clause']}: {'held' if x['holds'] else 'FAILED'}")
    READ_PATH.write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "provenance": PROVENANCE,
        "source": {"yielding": str(by.READ_PATH), "closure": str(closure.READ_PATH),
                   "records": {f"{p} {r}": str(closure.record_path(p, r))
                               for p, r in records},
                   "revealed": f"{plan.SAMPLE_PATH}::revealed.learned.order",
                   "stated": f"{SESSION_PATH}::rows[valid].ranking"},
        "surfaces": {"space": "the exhaustive space, 134,400 points, uniform",
                     "corpus": "the 2,000 cases of seed 17, as they arrive",
                     "outside": "has_security_keyword False: 67,200 points, and the "
                                "1,929 corpus cases without it",
                     "keyword": "has_security_keyword True: 67,200 points, and the "
                                "71 corpus cases with it"},
        "constants": {"N_COIN": by.N_COIN, "YIELD_SEED": by.YIELD_SEED,
                      "CENTRAL": by.CENTRAL, "HALF": HALF},
        "rankings": {"stage_c": rankings["stage_c"], "revealed": rankings["revealed"],
                     "stated": stated},
        "gates": checked,
        "bases": {f"{p} {r}": ({"cycle": True,
                                "arms": {n: public(a) for n, a in b["arms"].items()}}
                               if b["cycle"] else {"cycle": False})
                  for (p, r), b in per_base.items()},
        "pooled": {"bases": pooled["bases"], "whole": pooled["whole"],
                   "halves": pooled["halves"],
                   "stated_median": told,
                   "at_least": shares(pooled, coin, names),
                   "stated_median_at_least": {
                       "whole": {e: {s: at_least(coin["whole"][e][s],
                                                 told["whole"][e][s]["right"])
                                     for s in by.SURFACES} for e in by.ENGINES},
                       "halves": {e: {h: {s: at_least(coin["halves"][e][h][s],
                                                      told["halves"][e][h][s]["right"])
                                          for s in by.SURFACES} for h in by.HALVES}
                                  for e in by.ENGINES}}},
        "beside": {"what": "blind/yielding.py's pooled arms and coin, computed again and "
                           "gated equal to results_blind/yielding.json, which owns them",
                   "whole": {"arms": pool["arms"], "coin": pool["coin"]},
                   "halves": halves["pooled"]},
        "expectation": expectation,
    }), indent=2, default=str) + "\n")
    print(f"\n-> {READ_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
