"""
WHAT MAKES AN ANSWER READ A KEYWORD RULE BY ITS QUEUE.
`corrections/doors.py` found that an answer places a keyword rule of another
queue as a security rule, and so puts the gateway above its newborn, unless it
reads that rule by its queue, and climbs. Each answer read the round's keyword
rules one way, but for one cede of L r1. `FINDINGS_CORRECTIONS.md`, *Why the doors declared themselves
above the gateway*, *What it does not settle*, item 1, and `IDEAS.md` leave what
makes an answer read them by their queue. Asked for by Sergi on 2026-11-15,
after `corrections/carry.py`. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
**The listings are `doors.json`'s**: every round that listed a gateway, once per
gateway, with the side its answer declared, a *climb* above the gateway or a
*cede* below it. For each listing the reading takes four things the round gave
the answer, and one the answer spent:
- **the draft**: the newborn's queue and conditions, against the gateway;
- **the slot**: where the gateway stands in the round's list. v1c shows the list
  in a seeded shuffle of the case and the round, so the slot is drawn, not
  chosen. The reading asks whether the gateway stands before every rule of
  SECURITY_INCIDENT the list shows;
- **the precedent**: how many of the listed rules the list shows ceding to the
  gateway, `[pierde con` it`]`, as each rule's accepted declarations render;
- **the cause** of the escalation;
- **the reasoning**: the placement call's reasoning tokens, per listed rule.

**The same draft** is the same queue and conditions, listed the same gateway. Of
two listings of the same draft, a pair *disagrees* when one climbs and the other
cedes. Were each answer a draw at its run's climb rate `p`, a pair would
disagree with chance `2p(1 - p)`.

**Also read**, for each run and with no clause: the climb rate by each feature,
by the gateway's half of the list, and by the rules the list shows climbing
over the gateway; and every placement of every round against a keyword rule of
another queue, by that rule's queue.

--------------------------------------------------------------------------
THE DEVELOPMENT SET
--------------------------------------------------------------------------
**L r1 and N r3 are the development set**, L r1 for its one gateway of
`T2_TECHNICAL` and N r3 for its climbs, 19 of its 40 listings. Every clause
reads L r2 and L r3, pooled. What the drafter read of L r1 and N r3, before
writing anything below:
- **every listing**, with its draft, its slot, its list's length and security
  rules, its precedent, its cause and its reasoning tokens, and the side;
- **the same drafts**: in N r3, `product = billing -> BILLING_SPECIALIST` was
  listed `R0175` 17 times, and climbed 7. In L r1 it was listed `R0061` 25
  times, and climbed once;
- **the reasoning passages** that name the gateway, read for
  `corrections/doors.py`.

**Its counts**, `DEVELOPMENT`, which gate 5 recomputes:
- **the climbs**: 5 of L r1's 78 listings, and 19 of N r3's 40;
- **the same drafts**: L r1's pairs of listings of the same draft disagree 26
  times in 309, against 37 that independent draws at its rate would give.
  N r3's disagree 71 times in 138, against 69;
- **the slot**: in L r1, 2 of the 23 listings whose gateway stands before every
  security rule climbed, and 3 of the other 55. In N r3, 5 of 10 and 14 of 30;
- **the precedent**: in L r1, 2 of the 13 listings whose list shows no rule
  ceding to the gateway climbed, and 3 of the other 65. In N r3, 18 of 37, and 1
  of 3;
- **the reasoning**: the climbs' median reasoning tokens per listed rule, the
  lower median, is 232 in L r1 against the cedes' 208, and 194 in N r3 against
  182.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The listings are `doors.json`'s**: rebuilt from the record, every round
     after a gateway's birth that listed it, with the side its answer declared.
  2. **Every listing's list is the seeded shuffle v1c showed**: rebuilt by
     `reasoned_loop.protocol.listing` from its rules, it is the round's list in
     its order, and the one the round's first call kept.
  3. **Every listing's placement call carries its reasoning tokens.**
  4. **The precedent is the record's**: every listed rule shown ceding to the
     gateway had that edge installed at its own birth, by the record's edge log.
  5. **The development set gives `DEVELOPMENT`'s counts.**

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates, prints pass or fail, and
writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause pools L r2 and L r3. A climb rate is over listings.

  B1. **Not the draft.** The pairs of listings of the same draft disagree at
      least half as often as independent draws at their run's climb rate
      would.
  B2. **Not the slot.** The climb rate of the listings whose gateway stands
      before every security rule of the list, and that of the listings whose
      list shows a security rule before it, differ by at most 0.10.
  B3. **The precedent, if anything, holds the answer down.** The climb rate of
      the listings whose list shows no rule ceding to the gateway is at least
      that of the listings whose list shows one.
  B4. **Not the reasoning's amount.** The climbs' median reasoning tokens per
      listed rule lie within a quarter of the cedes'.

A share over nothing has no value, and a clause that reads one fails.

**The drafter's account**, from the development set.
- **The same draft goes both ways.** In N r3 one draft climbed 7 times in 17,
  and pairs of the same draft disagreed as often as independent draws would. In
  L r1, where climbs are rare, they disagreed somewhat less than such draws
  would.
- **The slot is drawn, and it barely moved the rate.** The gateway before every
  security rule, or after one, changed L r1's rate and N r3's by about 0.03.
- **The precedent leaned one way in L r1**, where the rounds whose list showed
  no rule ceding climbed more. In N r3 almost no list showed one.
- **The climbs reasoned about as much per listed rule as the cedes.**
- **So nothing the round gives the answer decides the reading.** It is the
  answer's, drawn at a rate that is the run's: about one in sixteen in L r1,
  and about one in two in N r3, whose gateway is of `T1_GENERAL`.

**The bet is B1.** It says the reading is drawn, and not set by the draft.
**B2 is trusted most**: the slot is the one feature the protocol drew at random,
and it moved neither development run. **B3 is trusted least**: it leans on L r1
alone, and on a few listings.

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole, and `doors.json`, `gateway.json` and
  `carry.json` whole: each run's listings, sides, causes, queues and sizes, and
  its climbs' ranks; L r2's and L r3's climb rates;
- L r1 and N r3, as the development set above;
- v1c's placement round and its listing, `reasoned_loop.protocol.listing`, and
  how a rule renders its accepted declarations in the list.

**What the drafter had not seen**: in L r2 and L r3, any listing's slot,
precedent, reasoning tokens or draft group.

--------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN: HOW MANY SECURITY RULES COME FIRST, AND THE SLOT
WITH THE PRECEDENT
--------------------------------------------------------------------------
The first run found B2 failing: in L r2 and L r3 the listings whose gateway
stands before every security rule climbed far more often than the rest. And B3
held, so the precedent leaned the same way. Read in a scratch script, the two
added to each other. So this part reads:
- **for each listing, how many security rules its list shows before the
  gateway**, and each run's climb rate by that count;
- **each run's climb rate by the slot crossed with the precedent.**
It was tried on the records in a scratch script before it was written here. It
was written after the four clauses above had been read: B1, B3 and B4 hold, and
B2 fails. It carries no expectation and moves no clause, and it adds no gate.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-15, after `corrections/carry.py`.
L r1 and N r3 were read as the development set before the expectation above was
written, and the expectation was committed before the reading ran on L r2 and
L r3. Not a signed row, not on `STATUS.md`'s scoreboard, not a calibration
event. Zero API calls.

Usage:  python3 -m corrections.byqueue --dry-run   # gates 1 to 5; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.byqueue
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from statistics import median_low
from typing import Any

from harness.provenance import describe, environment

from edges import rebuild as erb
from manual import instrument as MI
from reasoned_loop import protocol as rp
from reuse import structure as st
from rung2.engine2 import EDGE_OK, Space

from . import doors as dr
from . import fall as fl
from . import forgotten as fg
from . import plan

F = Fraction
SEC = fl.SEC
UNLABELLED = fl.UNLABELLED
CLIMB, CEDE = dr.CLIMB, dr.CEDE

DEVELOPMENT_RUNS = (plan.tag(plan.LABELLED, 1), plan.tag(UNLABELLED, 3))
HELD_OUT = tuple(plan.tag(plan.LABELLED, k) for k in range(2, plan.REPS + 1))

# The expectation's lines.
B1_SHARE = F(1, 2)
B2_GAP = F(1, 10)
B4_BAND = F(1, 4)

# The development set's counts, as the docstring gives them; gate 5 recomputes them.
DEVELOPMENT: dict[str, dict[str, Any]] = {
    plan.tag(plan.LABELLED, 1): {
        "listings": 78, "climbs": 5, "pairs": 309, "disagree": 26, "expected": 37,
        "before": [2, 23], "after": [3, 55], "no_precedent": [2, 13], "precedent": [3, 65],
        "median_per_rule": {CLIMB: 232, CEDE: 208}},
    plan.tag(UNLABELLED, 3): {
        "listings": 40, "climbs": 19, "pairs": 138, "disagree": 71, "expected": 69,
        "before": [5, 10], "after": [14, 30], "no_precedent": [18, 37], "precedent": [1, 3],
        "median_per_rule": {CLIMB: 194, CEDE: 182}},
}

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-15, after corrections/carry.py. L r1 and N r3 "
    "are the development set, read before the expectation in the module's docstring was "
    "written; the expectation was committed before the reading ran on L r2 and L r3. Not a "
    "signed row; no verdict moves.")

ADDED = (
    "Added after the first run, after its four clauses were read: each listing's count of the "
    "security rules its list shows before the gateway, and each run's climb rate by that count "
    "and by the slot crossed with the precedent. Tried in a scratch script first. No "
    "expectation; no clause moves.")

share, frac = fg.share, fg.frac


def record_path():
    return plan.OUT / "byqueue.json"


# ---------------------------------------------------------------------------
# One listing
# ---------------------------------------------------------------------------

def draft_key(rule: dict[str, Any]) -> str:
    """A draft's queue and conditions, in a canonical order."""
    conds = sorted((c["attr"], c["op"], json.dumps(c["value"])) for c in rule["conditions"])
    return json.dumps([rule["action"], conds])


def placement_call(esc: dict[str, Any]) -> dict[str, Any] | None:
    calls = [c for c in esc.get("calls") or [] if c.get("round", 0) >= 1]
    return calls[-1] if calls else None


def reasoning_tokens(call: dict[str, Any] | None) -> int | None:
    """The reasoning tokens of a call's attempts, or None if they are not kept."""
    att = (call or {}).get("call_attempts") or []
    toks = [a.get("reasoning_tokens") for a in att]
    if not att or any(not isinstance(t, int) for t in toks):
        return None
    return sum(toks)


def rows_of(record: dict[str, Any], doors_run: dict[str, Any]) -> list[dict[str, Any]]:
    """Each of `doors.json`'s listings of a run, with what its round gave the
    answer and what the answer spent."""
    rules = {r["rule_id"]: r for r in record["rules"]}
    escs = fg.escalation_at(record)
    out = []
    for l in doors_run.get("listings") or []:
        esc = escs[l["born_at"]]
        listed = list(esc.get("listed") or [])
        g = l["gateway"]
        slot = listed.index(g)
        secs = [i for i, x in enumerate(listed) if rules[x]["action"] == SEC]
        ceded = [x for x in listed if x != g and g in (rules[x].get("loses_to") or [])]
        climbed = [x for x in listed if x != g and g in (rules[x].get("beats") or [])]
        call = placement_call(esc)
        toks = reasoning_tokens(call)
        out.append({
            "born_at": l["born_at"], "newborn": l["newborn"], "gateway": g, "side": l["side"],
            "cause": l["cause"], "draft": draft_key(rules[l["newborn"]]),
            "listed": len(listed), "slot": slot,
            "first_half": slot * 2 < len(listed),
            "security_listed": len(secs),
            "before_every_security": (all(slot < i for i in secs) if secs else None),
            "security_before": sum(1 for i in secs if i < slot),
            "ceded_shown": ceded, "climbed_shown": climbed,
            "reasoning_tokens": toks,
            "per_rule": (F(toks, len(listed)) if toks is not None else None)})
    return out


# ---------------------------------------------------------------------------
# What the rows give
# ---------------------------------------------------------------------------

def rate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    c = sum(r["side"] == CLIMB for r in rows)
    return {"climbs": c, "of": len(rows), "rate": frac(share(c, len(rows)))}


def by(rows: list[dict[str, Any]], key) -> dict[str, dict[str, Any]]:
    """The climb rate of the rows, split by `key`."""
    groups: dict[str, list] = {}
    for r in rows:
        groups.setdefault(str(key(r)).lower(), []).append(r)
    return {k: rate(v) for k, v in sorted(groups.items())}


def same_drafts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """The pairs of listings of the same draft and gateway: how many disagree,
    and how many independent draws at the rows' climb rate would."""
    p = share(sum(r["side"] == CLIMB for r in rows), len(rows)) or F(0)
    groups: dict[tuple, list] = {}
    for r in rows:
        groups.setdefault((r["gateway"], r["draft"]), []).append(r["side"])
    pairs = disagree = 0
    both = 0
    for sides in groups.values():
        k, c = len(sides), sides.count(CLIMB)
        pairs += k * (k - 1) // 2
        disagree += c * (k - c)
        both += k >= 2 and 0 < c < k
    expected = pairs * 2 * p * (1 - p)
    return {"drafts": len(groups), "repeated": sum(1 for s in groups.values() if len(s) >= 2),
            "both_ways": both, "pairs": pairs, "disagree": disagree,
            "expected": frac(expected) if pairs else None}


def medians(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """The lower median of reasoning tokens per listed rule, by side."""
    out = {}
    for side in (CLIMB, CEDE):
        xs = [r["per_rule"] for r in rows if r["side"] == side and r["per_rule"] is not None]
        out[side] = frac(median_low(xs)) if xs else None
    return out


def keyword_placements(record: dict[str, Any], space: Space) -> dict[str, dict[str, int]]:
    """Every placement of every round against a keyword rule of a queue other
    than SECURITY_INCIDENT, by that rule's queue and the side declared."""
    rules = {r["rule_id"]: r for r in record["rules"]}
    ext = dr.extensions(record, space)
    kw = fl.keyword(space)
    out: dict[str, Counter] = {}
    for idx, r in sorted(erb.births(record).items()):
        listed = (fg.escalation_at(record).get(idx) or {}).get("listed") or []
        if not listed:
            continue
        said = fl.declared(r)
        for x in listed:
            q = rules[x]["action"]
            if q != SEC and dr.keyword_rule(ext[x], kw):
                out.setdefault(q, Counter())[dr.side_of(said, x)] += 1
    return {q: dict(sorted(c.items())) for q, c in sorted(out.items())}


def added(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Added after the first run: the climb rate by how many security rules the
    list shows before the gateway, and by the slot crossed with the precedent."""
    def many(k: int) -> str:
        return "0" if k == 0 else "1" if k == 1 else "2-3" if k <= 3 else "4+"

    slot = [r for r in rows if r["before_every_security"] is not None]
    return {"security_before": by(rows, lambda r: many(r["security_before"])),
            "slot_by_precedent": by(slot, lambda r: (
                ("before_every_security" if r["before_every_security"]
                 else "after_a_security_rule") + "/"
                + ("some_ceding" if r["ceded_shown"] else "none_ceding")))}


def development(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """The counts the docstring gives of a development run."""
    before = [r for r in rows if r["before_every_security"] is True]
    after = [r for r in rows if r["before_every_security"] is False]
    none = [r for r in rows if not r["ceded_shown"]]
    some = [r for r in rows if r["ceded_shown"]]
    sd = same_drafts(rows)
    md = medians(rows)
    return {"listings": len(rows), "climbs": sum(r["side"] == CLIMB for r in rows),
            "pairs": sd["pairs"], "disagree": sd["disagree"],
            "expected": round(float(F(sd["expected"]["fraction"]))) if sd["expected"] else None,
            "before": [rate(before)["climbs"], len(before)],
            "after": [rate(after)["climbs"], len(after)],
            "no_precedent": [rate(none)["climbs"], len(none)],
            "precedent": [rate(some)["climbs"], len(some)],
            "median_per_rule": {s: (round(float(F(v["fraction"]))) if v else None)
                                for s, v in md.items()}}


# ---------------------------------------------------------------------------
# One run
# ---------------------------------------------------------------------------

def read_run(record: dict[str, Any], doors_run: dict[str, Any], space: Space,
             tag: str | None = None) -> dict[str, Any]:
    rows = rows_of(record, doors_run)
    escs = fg.escalation_at(record)
    by_birth = erb.edges_by_birth(record)
    born_at = {r["rule_id"]: r["born_at"] for r in record["rules"]}
    want = sorted((l["born_at"], l["newborn"], l["gateway"], l["side"])
                  for l in doors_run.get("listings") or [])
    got = rebuilt(record, {l["gateway"] for l in doors_run.get("listings") or []})

    def shuffled(idx: int) -> bool:
        esc = escs[idx]
        listed = list(esc.get("listed") or [])
        first = (esc.get("calls") or [{}])[0].get("listed")
        return rp.listing(sorted(listed), idx, 0) == listed and first == listed

    def installed(winner: str, loser: str) -> bool:
        return any(e.winner == winner and e.loser == loser and e.verdict == EDGE_OK
                   for e in by_birth.get(born_at[loser], []))

    gates_out = [
        {"gate": 1, "what": "the listings are doors.json's, rebuilt from the record with "
                            "the side each answer declared",
         "passes": got == want},
        {"gate": 2, "what": "every listing's list is the seeded shuffle v1c showed",
         "passes": all(shuffled(r["born_at"]) for r in rows)},
        {"gate": 3, "what": "every listing's placement call carries its reasoning tokens",
         "passes": all(r["reasoning_tokens"] is not None for r in rows)},
        {"gate": 4, "what": "every listed rule shown ceding to the gateway had that edge "
                            "installed at its own birth",
         "passes": all(installed(r["gateway"], x) for r in rows for x in r["ceded_shown"])},
    ]
    run = {"summary": {
        "listings": len(rows), "climbs": rate(rows),
        "same_drafts": same_drafts(rows),
        "slot": by([r for r in rows if r["before_every_security"] is not None],
                   lambda r: "before_every_security" if r["before_every_security"]
                   else "after_a_security_rule"),
        "half": by(rows, lambda r: "first_half" if r["first_half"] else "second_half"),
        "precedent": by(rows, lambda r: "some_ceding" if r["ceded_shown"] else "none_ceding"),
        "climbing_shown": by(rows, lambda r: "some_climbing" if r["climbed_shown"]
                             else "none_climbing"),
        "cause": by(rows, lambda r: r["cause"]),
        "median_per_rule": medians(rows),
        "keyword_placements": keyword_placements(record, space)},
        "added_after_the_first_run": added(rows),
        "rows": [{**r, "ceded_shown": len(r["ceded_shown"]),
                  "climbed_shown": len(r["climbed_shown"]),
                  "per_rule": frac(r["per_rule"]) if r["per_rule"] is not None else None}
                 for r in rows],
        "gates": gates_out}
    if tag in DEVELOPMENT_RUNS:
        run["development"] = development(rows)
        gates_out.append({"gate": 5, "what": "the development set gives DEVELOPMENT's counts",
                          "passes": run["development"] == DEVELOPMENT.get(tag)})
    return run


def rebuilt(record: dict[str, Any], gates: set[str]) -> list[tuple]:
    """Every round after a gateway's birth that listed it, once per gateway, with
    the side its answer declared, rebuilt from the record."""
    born = erb.births(record)
    born_at = {r["rule_id"]: r["born_at"] for r in record["rules"]}
    escs = fg.escalation_at(record)
    out = []
    for idx in sorted(born):
        listed = (escs.get(idx) or {}).get("listed") or []
        said = fl.declared(born[idx])
        for g in sorted(gates, key=lambda x: born_at[x]):
            if born_at[g] < idx and g in listed:
                out.append((idx, born[idx]["rule_id"], g, dr.side_of(said, g)))
    return sorted(out)


def read_all_runs(records: dict[str, dict], doors_record: dict[str, Any],
                  space: Space) -> dict[str, dict]:
    return {tag: read_run(rec, doors_record["runs"][tag], space, tag=tag)
            for tag, rec in records.items()}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    held = [runs[t] for t in HELD_OUT if t in runs]
    rows = [r for run in held for r in run["rows"]]

    def climbs(rs):
        return sum(r["side"] == CLIMB for r in rs), len(rs)

    pairs = sum(run["summary"]["same_drafts"]["pairs"] for run in held)
    disagree = sum(run["summary"]["same_drafts"]["disagree"] for run in held)
    expected = sum((F(run["summary"]["same_drafts"]["expected"]["fraction"])
                    for run in held if run["summary"]["same_drafts"]["expected"]), F(0))
    before = [r for r in rows if r["before_every_security"] is True]
    after = [r for r in rows if r["before_every_security"] is False]
    (cb, nb), (ca, na) = climbs(before), climbs(after)
    none = [r for r in rows if not r["ceded_shown"]]
    some = [r for r in rows if r["ceded_shown"]]
    (cn, nn), (cs, ns) = climbs(none), climbs(some)

    def per(rs, side):
        xs = [F(r["per_rule"]["fraction"]) for r in rs
              if r["side"] == side and r["per_rule"] is not None]
        return median_low(xs) if xs else None

    mc, md = per(rows, CLIMB), per(rows, CEDE)
    return [
        {"clause": "B1", "what": "the pairs of listings of the same draft disagree at least "
                                 "half as often as independent draws at their run's climb "
                                 "rate would",
         "reading": {"disagree": disagree, "pairs": pairs, "expected": frac(expected)},
         "holds": pairs > 0 and expected > 0 and F(disagree) >= B1_SHARE * expected},
        {"clause": "B2", "what": "the climb rates of the listings whose gateway stands before "
                                 "every security rule and of the rest differ by at most 0.10",
         "reading": {"before": [cb, nb], "after": [ca, na],
                     "gap": frac(abs(F(cb, nb) - F(ca, na))) if nb and na else None},
         "holds": nb > 0 and na > 0 and abs(F(cb, nb) - F(ca, na)) <= B2_GAP},
        {"clause": "B3", "what": "the climb rate of the listings whose list shows no rule "
                                 "ceding to the gateway is at least that of the rest",
         "reading": {"none_ceding": [cn, nn], "some_ceding": [cs, ns]},
         "holds": nn > 0 and ns > 0 and F(cn, nn) >= F(cs, ns)},
        {"clause": "B4", "what": "the climbs' median reasoning tokens per listed rule lie within "
                                 "a quarter of the cedes'",
         "reading": {"climbs": frac(mc), "cedes": frac(md)},
         "holds": mc is not None and md is not None and md > 0
                  and abs(mc - md) <= B4_BAND * md},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict], dict[str, Any]]:
    tags = DEVELOPMENT_RUNS + HELD_OUT
    records = {}
    for a in (plan.LABELLED, UNLABELLED):
        for k in range(1, plan.REPS + 1):
            if plan.tag(a, k) in tags:
                records[plan.tag(a, k)] = json.loads(plan.run_path(a, k).read_text())
    return records, json.loads(dr.record_path().read_text())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="What makes an answer read a keyword rule by its "
                                             "queue (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 5 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/byqueue.py writes {record_path()}")
    records, doors_record = read_all()
    runs = read_all_runs(records, doors_record, MI.space())
    checked = [{"run": t, **g} for t, r in runs.items() for g in r["gates"]]
    for g in checked:
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    expectation = read_expectation(runs)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "added_after_the_first_run": ADDED,
        "source": {"doors": str(dr.record_path()),
                   "doors_from": doors_record["_env"].get("git_commit")},
        "surface": "doors.json's listings of L r1, L r2, L r3 and N r3, each with what its round "
                   "gave the answer and what the answer spent",
        "constants": {"B1_SHARE": str(B1_SHARE), "B2_GAP": str(B2_GAP), "B4_BAND": str(B4_BAND),
                      "DEVELOPMENT_RUNS": list(DEVELOPMENT_RUNS), "HELD_OUT": list(HELD_OUT),
                      "DEVELOPMENT": DEVELOPMENT},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        s = r["summary"]
        print(f"  {t}: climbs {s['climbs']['climbs']}/{s['climbs']['of']}; same drafts "
              f"{s['same_drafts']['disagree']}/{s['same_drafts']['pairs']}; slot {s['slot']}; "
              f"precedent {s['precedent']}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
