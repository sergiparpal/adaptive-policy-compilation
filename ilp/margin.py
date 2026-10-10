"""
WHERE THE +0.0342 COMES FROM. `FINDINGS_ILP.md` §1 reads the inducer trained on
all 632 escalations at 0.8814 on corpus test split 0, against 0.8472 for the
searched order over the 577 LLM rules. Its erratum of 2026-10-10 found that 371
of the split's 995 cases are identical to an example that inducer was trained on
with its true label, and left open how much of the +0.0342 rests on them. This
splits the margin, case by case, between those 371 and the other 624. POST-RUN.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
  1. **The searched order, rebuilt.** No record holds an order from the
     declared optimizer — `rung3/local_search.py::multistart` says why — so
     split 0's is searched again on the `puro` pool by `rung3/order_search_ls.py`'s
     own `search`, the greedy and the 64 declared starts, and its test cases are
     read one by one, first match wins.
  2. **The four induced lists**, induced again by `ilp/induce.py` as
     `ilp/compare.py` induces them: `train_632` and `train_316`, at both beams.
  3. **The partition**: the 371 test cases identical, by `Case.key()`, to an
     example of `train_632`, of which 316 are those examples, and the 624 that
     are not.

Per list and for the order, the cases right in each part; per beam, the margin
of the `train_632` list over the order in each part, in cases and over the 995.
Beside them, unbet: the pool's ceiling in each part, the cases some matching
rule gets right, and the `train_316` lists, which saw none of the 371 labelled.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The order is the published one**: rebuilt, it reproduces split 0's row
     of `results3/order_search_ls.json` — the start it came from, and its train
     and test scores to four decimals.
  2. **The split is the instances'**: rung 3's test half of split 0 is
     `ilp/instances.py`'s `test`, case for case.
  3. **The lists are the published ones**: each reproduces its training fit and
     its test count in `results_ilp/compare.json`.
  4. **The partition is `labels.json`'s**: 371 reached, 316 of them examples.

It refuses to write if any fails, and while the plan is unsigned, through
`ilp/compare.py`'s gate, called and not copied.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  1. **By construction, the `train_632` lists decide all 371 right, at both
     beams.** They fit their 632 examples (`compare.json`), a list decides
     identical cases identically, and the truth is a function of the case. So
     their 877 right split as 371 and 506, and the margin in each part turns on
     one number: the order's cases right among the 371, `a`. The 371 carry
     `371 − a` of the margin's 34 cases and the 624 carry `a − 337`.
  2. **The 371 carry the whole margin, or more**: `a` is at most 337, so on the
     624 the inducer is at or below the order, at both beams. The drafter gives
     it about five in six.
  3. **And the order is right on a smaller share of the 371 than of the 624**,
     which is `a` at most 314 and implies 2. They are the escalations of the
     test half and their duplicates — cases on which the base disagreed or said
     nothing when they arrived — and the search placed the rules born on them
     only through the train cases those rules also match. The drafter gives it
     about three in four.

**What the drafter had seen**: `FINDINGS_ILP.md` and its errata; `compare.json`,
including both `train_632` lists' fit of 632 of 632, their 877 right on the test
split, and the `train_316` lists' 772 and 759; split 0's `puro` row of
`order_search_ls.json`, 0.8472, so 843 right; `labels.json`, including the 124
of the 316 test escalations on which the proposer chose right; and
`ARBITRATION_REPORT.md`'s 594 CONFLICTs among the 632 escalations. **Not seen**:
any test case decided by the order or by any list, and any figure restricted to
the 371 or to the 624.

--------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN, AND LABELLED SO
--------------------------------------------------------------------------
The first run put the order on 337 of the 371, exactly the number at which the
624 carry nothing, and both `train_632` lists on 506 of the 624, the order's
own count. Two things were added for that, after reading it:

  5. **A fifth gate, the masks are the cases**: the order replayed case by case,
     each case decided by the first of its matching rules in the order, gives
     the same cases right as the masks, bit for bit.
  -  **Whether a tie is of cases or of counts**: per beam and per part, the
     cases the `train_632` list and the order both get right, only one of
     them, and neither.

Both were written by someone who had read the first run, and the record comes
from a second run, which reproduced every figure of the first. Neither is a bet.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: asked for on 2026-10-10, after the erratum, with the expectation
above written and committed before the first run. Not a signed row, not on
`STATUS.md`'s scoreboard, not a calibration event. Zero API calls; the search
takes about half a minute.

Usage:  python3 -m ilp.margin
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from harness.provenance import describe, environment
from rung3.local_search import build_masks
from rung3.order_search import build_tables, load, split, subsumption_below
from rung3.order_search_ls import search

from . import compare as cmp
from . import induce as ind
from . import instances as inst

RECORD = Path("results_ilp/margin.json")
ORDER_RECORD = Path("results3/order_search_ls.json")
COMPARE_RECORD = Path("results_ilp/compare.json")
LABELS_RECORD = Path("results_ilp/labels.json")
SPLIT, POOL = 0, "puro"
LISTS = tuple((t, b) for t in ("train_632", "train_316") for b in ind.BEAM_WIDTHS)
PROVENANCE = (
    "POST-RUN: asked for on 2026-10-10, after FINDINGS_ILP.md's erratum. The "
    "expectation in the module's docstring was written and committed before the "
    "first run. Not a signed row; no verdict moves.")


def won_by_order(order, M, W, full) -> int:
    """The cases an order gets right, as a mask: `score_order`'s walk, keeping
    the bits it counts."""
    remaining, ok = full, 0
    for rid in order:
        fires = M[rid] & remaining
        if fires:
            ok |= W[rid] & fires
            remaining ^= fires
            if not remaining:
                break
    return ok


def won_by_list(induced, ext, truth, n) -> int:
    """The cases a decision list gets right, as a mask: `induce.score`'s walk,
    keeping the bits it counts."""
    full = (1 << n) - 1
    remaining, ok = full, 0
    for body, action in induced.rules:
        covered = full
        for j in body:
            covered &= ext[j]
        hit = covered & remaining
        ok |= hit & truth.get(action, 0)
        remaining &= ~hit
    return ok


def replay_order(order, pool, action, truth, idxs) -> int:
    """The same cases as `won_by_order`, reached another way: each case decided
    by the first of its matching rules in the order, one case at a time."""
    pos = {rid: p for p, rid in enumerate(order)}
    won = 0
    for k, i in enumerate(idxs):
        if pool[i]:
            first = min(pool[i], key=pos.__getitem__)
            if action[first] == truth[i]:
                won |= 1 << k
    return won


def agreement(a: int, b: int, part: int) -> dict[str, int]:
    """Within `part`: the cases both masks get right, only one, and neither."""
    return {"both": (a & b & part).bit_count(),
            "only_the_list": (a & ~b & part).bit_count(),
            "only_the_order": (b & ~a & part).bit_count(),
            "neither": (part & ~a & ~b).bit_count()}


def partition(corpus, examples, test) -> tuple[int, int]:
    """Over the test cases, as masks by position: those identical to an
    example, and among them those that are one."""
    keys = {corpus[i].key() for i in examples}
    mine = set(examples)
    reached = own = 0
    for k, i in enumerate(test):
        if corpus[i].key() in keys:
            reached |= 1 << k
            if i in mine:
                own |= 1 << k
    return reached, own


def parts(won: int, reached: int, full: int) -> dict[str, int]:
    return {"reached": (won & reached).bit_count(),
            "not_reached": (won & full & ~reached).bit_count(),
            "total": (won & full).bit_count()}


def margin(a: dict, b: dict, n: int) -> dict[str, Any]:
    """`a` over `b`, part by part, in cases and over the `n` test cases."""
    out: dict[str, Any] = {}
    for part in ("reached", "not_reached", "total"):
        d = a[part] - b[part]
        out[part] = {"cases": d, "points": d / n}
    total = out["total"]["cases"]
    out["share_from_reached"] = out["reached"]["cases"] / total if total else None
    return out


def compute() -> dict[str, Any]:
    """The order rebuilt, the four lists induced, the partition: everything a
    gate or a reading needs, as masks over the test split's positions."""
    corpus, rules, ext, conds = load()
    action = {r["rule_id"]: r["action"] for r in rules}
    born = {r["rule_id"]: r["born_at"] for r in rules}
    ids = [r["rule_id"] for r in rules]
    below = subsumption_below(rules, ext)
    matched, _undef, truth = build_tables(corpus, rules, conds, below)
    tr, te = split(corpus, truth, seed=17 + SPLIT)
    M, W, full = build_masks(ids, matched, truth, action, tr)
    tM, tW, tfull = build_masks(ids, matched, truth, action, te)
    _greedy, best, st = search(ids, M, W, full, born)
    ceiling = 0
    for rid in ids:
        ceiling |= tW[rid]

    test = inst._indices("test")
    s_ext, s_truth, s_n = inst.instance("test")
    lists = {}
    for train, beam in LISTS:
        t_ext, t_truth, t_n = inst.instance(train)
        got = ind.induce(t_ext, t_truth, t_n, beam=beam)
        lists[(train, beam)] = {
            "won": won_by_list(got, s_ext, s_truth, s_n),
            "train_correct": won_by_list(got, t_ext, t_truth, t_n).bit_count(),
            "n_rules": got.n_rules}
    reached, own = partition(inst.corpus(), inst._indices("train_632"), test)
    return {"rung3_test": list(te), "test": list(test), "full": tfull,
            "n_train": len(tr), "order": {"won": won_by_order(best, tM, tW, tfull),
                                          "replayed": replay_order(best, matched,
                                                                   action, truth, te),
                                          "train_score": st["best_score"],
                                          "best_from": st["best_from"]},
            "ceiling": ceiling, "lists": lists, "reached": reached, "own": own}


def check(c: dict, order_row: dict, runs: dict, reach: dict) -> list[dict]:
    n = len(c["test"])
    o = c["order"]
    order_measured = {"best_from": o["best_from"],
                      "ls_train": round(o["train_score"] / c["n_train"], 4),
                      "ls_test": round(o["won"].bit_count() / n, 4)}
    order_published = {k: order_row[k] for k in order_measured}
    lists_measured = {f"{t}|{b}": [v["train_correct"], v["won"].bit_count()]
                      for (t, b), v in c["lists"].items()}
    lists_published = {k: [runs[k]["train_score"]["correct"], runs[k]["test"]["correct"]]
                       for k in lists_measured}
    part_measured = [c["reached"].bit_count(), c["own"].bit_count()]
    part_published = [reach["train_632"]["test_cases_identical_to_an_example"],
                      reach["train_632"]["test_cases_among_its_examples"]]
    return [
        {"gate": 1, "what": "the order is the published one",
         "measured": order_measured, "published": order_published,
         "passes": order_measured == order_published},
        {"gate": 2, "what": "the split is the instances'",
         "measured": {"rung3_test_equals_instances_test": c["rung3_test"] == c["test"]},
         "passes": c["rung3_test"] == c["test"]},
        {"gate": 3, "what": "the lists are the published ones",
         "measured": lists_measured, "published": lists_published,
         "passes": lists_measured == lists_published},
        {"gate": 4, "what": "the partition is labels.json's",
         "measured": part_measured, "published": part_published,
         "passes": part_measured == part_published},
        {"gate": 5, "what": "the masks are the cases (added after the first run)",
         "measured": {"replay_equals_masks": o["replayed"] == o["won"]},
         "passes": o["replayed"] == o["won"]},
    ]


def agreements(c: dict) -> dict[str, Any]:
    """Added after the first run: per beam and per part, whose cases right the
    `train_632` list's and the order's are."""
    full, reached = c["full"], c["reached"]
    sides = {"reached": reached, "not_reached": full & ~reached}
    return {str(b): {part: agreement(c["lists"][("train_632", b)]["won"],
                                     c["order"]["won"], mask)
                     for part, mask in sides.items()}
            for b in ind.BEAM_WIDTHS}


def readings(c: dict) -> dict[str, Any]:
    full, reached, own = c["full"], c["reached"], c["own"]
    n = len(c["test"])
    order = parts(c["order"]["won"], reached, full)
    order["reached_split"] = {
        "examples": (c["order"]["won"] & own).bit_count(),
        "duplicates": (c["order"]["won"] & reached & ~own).bit_count()}
    lists = {f"{t}|{b}": {**parts(v["won"], reached, full), "n_rules": v["n_rules"]}
             for (t, b), v in c["lists"].items()}
    margins = {str(b): margin(lists[f"train_632|{b}"], order, n)
               for b in ind.BEAM_WIDTHS}
    return {"parts": {"test": n, "reached": reached.bit_count(),
                      "of_which_examples": own.bit_count(),
                      "not_reached": n - reached.bit_count()},
            "order": order, "ceiling": parts(c["ceiling"], reached, full),
            "lists": lists, "margins": margins}


def read_expectation(r: dict) -> list[dict]:
    p, o = r["parts"], r["order"]
    beams = [str(b) for b in ind.BEAM_WIDTHS]
    on_reached = o["reached"] / p["reached"]
    on_rest = o["not_reached"] / p["not_reached"]
    return [
        {"clause": "by construction",
         "what": "the train_632 lists decide all 371 right, at both beams",
         "reading": {b: r["lists"][f"train_632|{b}"]["reached"] for b in beams},
         "holds": all(r["lists"][f"train_632|{b}"]["reached"] == p["reached"]
                      for b in beams)},
        {"clause": 2,
         "what": "the 371 carry the whole margin or more: on the 624 the inducer "
                 "is at or below the order, at both beams",
         "reading": {b: r["margins"][b]["not_reached"]["cases"] for b in beams},
         "holds": all(r["margins"][b]["not_reached"]["cases"] <= 0 for b in beams)},
        {"clause": 3,
         "what": "the order is right on a smaller share of the 371 than of the 624",
         "reading": {"on_the_371": on_reached, "on_the_624": on_rest},
         "holds": on_reached < on_rest},
    ]


def report(r: dict) -> None:
    p = r["parts"]
    print(f"\n  TEST SPLIT 0 — {p['test']} cases: {p['reached']} reached by "
          f"train_632 ({p['of_which_examples']} its own examples), "
          f"{p['not_reached']} not")
    print(f"  {'':<26}{'the 371':>10}{'the 624':>10}{'total':>8}")
    rows = [("the searched order", r["order"]), ("the pool's ceiling", r["ceiling"])]
    rows += [(k, v) for k, v in r["lists"].items()]
    for name, v in rows:
        print(f"  {name:<26}{v['reached']:>10}{v['not_reached']:>10}{v['total']:>8}")
    for b, m in r["margins"].items():
        print(f"\n  MARGIN, train_632 at beam {b} over the order, in cases")
        print(f"    on the 371 {m['reached']['cases']:>+5}   on the 624 "
              f"{m['not_reached']['cases']:>+5}   total {m['total']['cases']:>+5} "
              f"({m['total']['points']:+.4f})")


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        print(__doc__)
        return 2
    gate = cmp.gate_signature()
    if not gate["passes"]:
        sys.exit(f"\nREFUSED: {cmp.PLAN} is unsigned, so ilp/margin.py writes "
                 "nothing. There is no flag that skips this.\n")
    order_row = next(r for r in json.loads(ORDER_RECORD.read_text())["splits"]
                     if r["split"] == SPLIT and r["pool"] == POOL)
    runs = json.loads(COMPARE_RECORD.read_text())["runs"]
    reach = json.loads(LABELS_RECORD.read_text())["reach"]

    print("=" * 78)
    print("WHERE THE +0.0342 COMES FROM — POST-RUN, FINDINGS_ILP.md §1's erratum")
    print("=" * 78)
    c = compute()
    checked = check(c, order_row, runs, reach)
    for g in checked:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    r = readings(c)
    report(r)
    expectation = read_expectation(r)
    print()
    for e in expectation:
        print(f"  expectation {e['clause']}: {'holds' if e['holds'] else 'FAILS'}  "
              f"{e['what']}")
    agree = agreements(c)
    print("\n  ADDED AFTER THE FIRST RUN — whose cases right, train_632 against the order")
    for b, by_part in agree.items():
        for part, a in by_part.items():
            print(f"    beam {b:>3} · {part:<12} both {a['both']:>4} · only the list "
                  f"{a['only_the_list']:>3} · only the order {a['only_the_order']:>3} · "
                  f"neither {a['neither']:>3}")

    RECORD.write_text(json.dumps({
        "_env": environment(split_seed=inst.SPLIT_SEED, beams=list(ind.BEAM_WIDTHS)),
        "what": "the +0.0342 of FINDINGS_ILP.md §1, split between the 371 test "
                "cases the 632-trained inducer saw labelled and the other 624",
        "plan": str(cmp.PLAN),
        "gate": gate,
        "provenance": PROVENANCE,
        "source": {"order": f"{ORDER_RECORD}, split {SPLIT}, {POOL}, rebuilt by "
                            "rung3/order_search_ls.py's search",
                   "lists": f"{COMPARE_RECORD}, induced again",
                   "partition": str(LABELS_RECORD)},
        "surface": "corpus test split 0, 995 cases, puro, first match wins",
        "gates": checked,
        **r,
        "expectation": expectation,
        "added_after_the_first_run": {
            "what": "gate 5, the order replayed case by case against its masks; "
                    "and per beam and part, the cases the train_632 list and the "
                    "order both get right, only one, and neither",
            "provenance": "Written after the first run, by someone who had read "
                          "it. The record comes from a second run, which "
                          "reproduced every figure of the first. Not a bet.",
            "agreement": agree,
        },
    }, indent=2) + "\n")
    print(f"\n-> {RECORD}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
