"""
WHICH TICKETS TEACH `T3_ENGINEERING`. `FINDINGS_SPOTCHECK.md`, *What this does
not settle*, names the question, and `IDEAS.md` carries it as a free reading.
An order of the stage learns that queue all at once or not at all, and the
number of its tickets in a draw does not decide which: one ticket among ten
audited decisions taught it, and three among fifty did not. This reads the
stage's orders to say which tickets, and whether the class turns on one rule's
place. POST-RUN.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  A. **Which rule decides the class.** In the whole train half's order, which
     rule is the first match of the `T3_ENGINEERING` test cases it gets right.
     In every order of the stage, how many of them that rule decides.
  B. **What beats it where the class is not learnt.** On the `T3_ENGINEERING`
     test cases that rule matches and an order gets wrong, the queue of the
     rule that wins them.
  C. **Which tickets teach it.** Every labelled `T3_ENGINEERING` ticket of every
     set, whether that rule matches it, and whether the set's order gets it
     right.
  D. **One move.** Every order with that rule moved to the front, on the
     `T3_ENGINEERING` test cases and on the whole test split.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
The orders are searched again by `escalations/instrument.py`'s
`labelled_order`, called and not copied. It runs on the 40 sets of
`spotcheck/selections.py` and on the two endpoints, the escalations alone and
the whole train half. The search is deterministic, so a re-run is the stage's
order, and gate 1 says so. The orders are kept in the record, which the stage's
record did not do.

**The key rule** is fixed by the whole train half's order alone, before any
other order is read. It is the rule that is the first match of the most
`T3_ENGINEERING` test cases that order gets right, the earlier in that order on
a tie. An order *learns* the class when it is right on 13 or more of the 57,
and *does not* when it is right on 2 or fewer: `FINDINGS_SPOTCHECK.md`'s two
clusters.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The orders are the record's.** Each scores on the test split, over the
     space and on the four rare queues what `score.json` says, the two
     endpoints included.
  2. **Two routes agree.** Every order's `T3_ENGINEERING` count by first match
     equals its count by masks over the 57 cases, `score_order`'s. So does the
     same order with the key rule moved to the front.

It refuses to write if either fails, and while `PLAN_SPOTCHECK.md` is unsigned,
like every writer of the package.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  E1. **In the whole train half's order, the key rule decides at least 13 of
      its 18 right `T3_ENGINEERING` cases.** The jump from 2 or fewer to 13 or
      more, with one labelled ticket, reads like one rule moving.
  E2. **In every order that learns the class, the key rule decides at least 13
      of the cases it gets right.**
  E3. **In every order that does not, the key rule decides none.** At least two
      thirds of the `T3_ENGINEERING` cases it matches go to `T2_TECHNICAL`
      rules, the queue rung 1's engine decided 50 of the 57 decisions of that
      queue as.
  E4. **Moved to the front, the key rule makes every one of the 42 orders learn
      the class.**
  E5. **Moved to the front in every order that does not learn the class, it
      raises the order's count on the whole test split too.** The drafter
      trusts this one least: at the front it also takes every other ticket it
      matches.
  E6. **None of the escalations' three `T3_ENGINEERING` tickets is matched by
      the key rule, and draw 4's one among its first ten decisions is.** The
      escalations alone are right on none of the 57, and that draw's ten
      decisions taught 13.
  E7. **None of draw 1's three among its first fifty decisions is matched by
      the key rule.** Both of that draw's orders at fifty are right on none.
  E8. **No order whose labels hold no `T3_ENGINEERING` ticket the key rule
      matches learns the class. At least four in five of those whose labels
      hold one do.**

**What the drafter had seen**:
- `results_spotcheck/score.json` whole: every order's counts and every set's
  cases and make-up;
- `FINDINGS_SPOTCHECK.md`;
- `PLAN_SPOTCHECK.md`'s table of the draws;
- `results_escalations/score.json`;
- the optimizer audit's per-class count on split 0, whose 18 and 20 E1 reads.

**Not seen**: rung 1's `T3_ENGINEERING` rules; which rules match which test
case or ticket of that queue; any order; the key rule.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: asked for on 2026-10-19, after the stage, with the expectation
above written and committed before the first run. Not a signed row, not on
`STATUS.md`'s scoreboard, not a calibration event. Zero API calls; about ten
minutes, most of them the 42 searches.

Usage:  PYTHONHASHSEED=0 python3 -m spotcheck.readings
"""

from __future__ import annotations

import json
import sys
import time
from collections import Counter
from typing import Any, Sequence

from escalations import instrument as I
from escalations.selections import escalations
from harness.provenance import describe, environment
from rung3.local_search import build_masks, score_order

from . import plan, selections

RECORD = plan.OUT / "readings.json"
T3 = "T3_ENGINEERING"
LEARNT = 13                        # FINDINGS_SPOTCHECK.md's two clusters
NOT_LEARNT = 2
ENDPOINTS = ("full", "escalations")
PROVENANCE = (
    "POST-RUN: asked for on 2026-10-19, after PLAN_SPOTCHECK.md's stage. The "
    "expectation in the module's docstring was written and committed before the "
    "first run. Not a signed row; no verdict moves.")

# The expectation's lines.
E1_LINE = 13
E3_SHARE = (2, 3)
E8_SHARE = (4, 5)


# ---------------------------------------------------------------------------
# Orders, read on a set of cases
# ---------------------------------------------------------------------------

def first_match(order: Sequence[str], matched, cases) -> dict[int, str | None]:
    """The rule that decides each case, first match wins; None if none
    matches."""
    rank = {rid: k for k, rid in enumerate(order)}
    return {i: (min(matched[i], key=rank.__getitem__) if matched[i] else None)
            for i in cases}


def right_by_rule(order, matched, truth, action, cases) -> Counter:
    """How many of `cases` each rule decides right."""
    fm = first_match(order, matched, cases)
    return Counter(r for i, r in fm.items()
                   if r is not None and action[r] == truth[i])


def key_rule(order, matched, truth, action, cases) -> str:
    """The rule deciding the most of `cases` right in `order`, the earlier in
    it on a tie."""
    counts = right_by_rule(order, matched, truth, action, cases)
    rank = {rid: k for k, rid in enumerate(order)}
    return min(counts, key=lambda r: (-counts[r], rank[r]))


def moved_to_front(order: Sequence[str], rid: str) -> list[str]:
    return [rid] + [r for r in order if r != rid]


def t3_cases(inst) -> list[int]:
    _tr, te = I.halves(inst)
    return [i for i in te if inst["truth"][i] == T3]


def read_order(order, inst, key, labelled, t3_m, test_m) -> dict[str, Any]:
    """One order, read on the 57 `T3_ENGINEERING` test cases."""
    truth, action, matched = inst["truth"], inst["action"], inst["matched"]
    cases = t3_cases(inst)
    fm = first_match(order, matched, cases)
    right = {i for i, r in fm.items() if r is not None and action[r] == truth[i]}
    by_rule = Counter(fm[i] for i in right)
    key_matched = [i for i in cases if key in matched[i]]
    lost_to = Counter(action[fm[i]] for i in key_matched if i not in right)
    moved = moved_to_front(order, key)
    moved_fm = first_match(moved, matched, cases)
    labelled_t3 = [i for i in labelled if truth[i] == T3]
    lab_fm = first_match(order, matched, labelled_t3)
    return {
        "test": score_order(order, *test_m),
        "t3_right": len(right),
        "t3_right_by_masks": score_order(order, *t3_m),
        "key_decides": by_rule.get(key, 0),
        "key_rank": list(order).index(key),
        "deciding_rules": dict(by_rule.most_common()),
        "key_matched_t3": len(key_matched),
        "key_matched_lost_to": dict(lost_to.most_common()),
        "moved": {
            "test": score_order(moved, *test_m),
            "t3_right": sum(1 for i, r in moved_fm.items()
                            if r is not None and action[r] == truth[i]),
            "t3_right_by_masks": score_order(moved, *t3_m),
        },
        "labelled_t3": [{"case": i, "key_matches": key in matched[i],
                         "right": lab_fm[i] is not None and action[lab_fm[i]] == T3}
                        for i in labelled_t3],
    }


def footprint(inst, rid: str, cases) -> dict[str, int]:
    """The cases of `cases` a rule matches, by true queue."""
    truth, matched = inst["truth"], inst["matched"]
    return dict(Counter(truth[i] for i in cases if rid in matched[i]).most_common())


def describe_rule(inst, rid: str) -> dict[str, Any]:
    rule = next(r for r in inst["rules"] if r["rule_id"] == rid)
    return {"rule_id": rid, "action": rule["action"], "born_at": rule["born_at"],
            "conditions": [f"{c.attr} {c.op} {c.value}" for c in inst["conds"][rid]],
            "note": rule.get("note")}


# ---------------------------------------------------------------------------
# Gates and expectation
# ---------------------------------------------------------------------------

def recorded(record: dict, name: str) -> dict:
    return record["endpoints"][name] if name in ENDPOINTS else record["results"][name]


def check(orders: dict, readings: dict, record: dict, inst) -> list[dict[str, Any]]:
    _tr, te = I.halves(inst)
    sM, sW, sfull, _sn = I.space_masks()
    off = []
    for name, order in orders.items():
        rec = recorded(record, name)
        got = (readings[name]["test"], score_order(order, sM, sW, sfull),
               I.per_class(inst, order, te))
        if got != (rec["test"], rec["space"], rec["per_class"]):
            off.append(name)
    routes = [name for name, r in readings.items()
              if r["t3_right"] != r["t3_right_by_masks"]
              or r["moved"]["t3_right"] != r["moved"]["t3_right_by_masks"]]
    return [{"gate": 1, "what": "the orders are the record's", "orders": len(orders),
             "off": off, "passes": not off},
            {"gate": 2, "what": "two routes agree on T3_ENGINEERING", "off": routes,
             "passes": not routes}]


def has_key_label(r: dict) -> bool:
    return any(t["key_matches"] for t in r["labelled_t3"])


def read_expectation(readings: dict[str, dict]) -> list[dict[str, Any]]:
    learnt = {n: r for n, r in readings.items() if r["t3_right"] >= LEARNT}
    not_learnt = {n: r for n, r in readings.items() if r["t3_right"] <= NOT_LEARNT}
    full = readings["full"]
    lost = sum(sum(r["key_matched_lost_to"].values()) for r in not_learnt.values())
    lost_t2 = sum(r["key_matched_lost_to"].get("T2_TECHNICAL", 0)
                  for r in not_learnt.values())
    esc = readings["escalations"]["labelled_t3"]
    d4 = readings["audit|10|4"]["labelled_t3"]
    d1 = readings["audit|50|1"]["labelled_t3"]
    without = [n for n, r in readings.items() if not has_key_label(r)]
    with_ = [n for n, r in readings.items() if has_key_label(r)]
    with_learnt = [n for n in with_ if readings[n]["t3_right"] >= LEARNT]
    return [
        {"clause": "E1", "holds": full["key_decides"] >= E1_LINE,
         "reading": f"the key rule decides {full['key_decides']} of the whole "
                    f"train half's {full['t3_right']}"},
        {"clause": "E2", "holds": all(r["key_decides"] >= E1_LINE for r in learnt.values()),
         "reading": f"{len(learnt)} orders learn the class; the key rule decides "
                    f"{sorted(r['key_decides'] for r in learnt.values())}"},
        {"clause": "E3",
         "holds": (all(r["key_decides"] == 0 for r in not_learnt.values())
                   and lost_t2 * E3_SHARE[1] >= E3_SHARE[0] * lost),
         "reading": f"{len(not_learnt)} orders do not; the key rule decides "
                    f"{sorted(r['key_decides'] for r in not_learnt.values())}; "
                    f"{lost_t2} of the {lost} cases it matches there go to T2_TECHNICAL"},
        {"clause": "E4", "holds": all(r["moved"]["t3_right"] >= LEARNT
                                      for r in readings.values()),
         "reading": "moved to the front: " + str(sorted(
             r["moved"]["t3_right"] for r in readings.values()))},
        {"clause": "E5", "holds": all(r["moved"]["test"] > r["test"]
                                      for r in not_learnt.values()),
         "reading": "on the whole test split, moved less as searched: " + str(sorted(
             r["moved"]["test"] - r["test"] for r in not_learnt.values()))},
        {"clause": "E6", "holds": (not any(t["key_matches"] for t in esc)
                                   and len(d4) == 1 and d4[0]["key_matches"]),
         "reading": f"the escalations' {len(esc)}: "
                    f"{[t['key_matches'] for t in esc]}; draw 4's at ten: "
                    f"{[t['key_matches'] for t in d4]}"},
        {"clause": "E7", "holds": not any(t["key_matches"] for t in d1),
         "reading": f"draw 1's at fifty: {[t['key_matches'] for t in d1]}"},
        {"clause": "E8",
         "holds": (not any(readings[n]["t3_right"] >= LEARNT for n in without)
                   and len(with_learnt) * E8_SHARE[1] >= E8_SHARE[0] * len(with_)),
         "reading": f"{len(without)} orders hold no key-matched ticket, "
                    f"{sum(readings[n]['t3_right'] >= LEARNT for n in without)} of them "
                    f"learn; {len(with_learnt)} of the {len(with_)} that hold one learn"},
    ]


# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        print(__doc__)
        return 2
    gate = plan.refuse_unsigned("spotcheck/readings.py writes nothing")
    t0 = time.time()
    record = json.loads(plan.SCORE_PATH.read_text())
    inst = I.instance()
    tr, te = I.halves(inst)
    escs = escalations(tr)
    decs = selections.decisions(tr)
    sets = {"full": list(tr), "escalations": list(escs)}
    sets |= selections.selections(escs, decs)

    print("=" * 78)
    print("PLAN_SPOTCHECK.md — WHICH TICKETS TEACH T3_ENGINEERING — POST-RUN")
    print("=" * 78)
    orders = {}
    for name, sel in sets.items():
        orders[name] = list(I.labelled_order(inst, sel)[0])
        print(f"  searched {name}", flush=True)

    cases = t3_cases(inst)
    key = key_rule(orders["full"], inst["matched"], inst["truth"], inst["action"], cases)
    t3_m = build_masks(inst["ids"], inst["matched"], inst["truth"], inst["action"], cases)
    test_m = I.test_masks()
    readings = {name: read_order(orders[name], inst, key, sets[name], t3_m, test_m)
                for name in sets}
    checked = check(orders, readings, record, inst)
    for g in checked:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")

    expectation = read_expectation(readings)
    for e in expectation:
        print(f"  {e['clause']}: {'holds' if e['holds'] else 'FAILS'}  {e['reading']}")

    RECORD.write_text(json.dumps({
        "_env": environment(split_seed=plan.SPLIT_SEED, draws=plan.DRAWS,
                            audit_seed=plan.AUDIT_SEED, budgets=list(plan.BUDGETS)),
        "what": "which tickets teach T3_ENGINEERING: the rule that decides the "
                "class, what beats it, which labelled tickets it matches, and the "
                "orders with it moved to the front",
        "plan": str(plan.PLAN),
        "gate": gate,
        "provenance": PROVENANCE,
        "source": {"record": str(plan.SCORE_PATH),
                   "orders": "searched again by escalations/instrument.py's "
                             "labelled_order on the stage's 40 sets and two endpoints"},
        "surface": "corpus test split 0, its 57 T3_ENGINEERING cases and its 995 "
                   "cases; every count against the truth",
        "gates": checked,
        "key_rule": describe_rule(inst, key)
                    | {"test_footprint": footprint(inst, key, te),
                       "train_footprint": footprint(inst, key, tr)},
        "readings": readings,
        "orders": orders,
        "expectation": expectation,
        "seconds": round(time.time() - t0, 1),
    }, indent=2) + "\n")
    print(f"\n-> {RECORD}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
