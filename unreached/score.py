"""
THE STAGE of `PLAN_UNREACHED.md` §8: the rules no label reaches, moved.

It refuses while §0 is unsigned, before it builds or measures anything; no flag
skips that. `--dry-run` runs `Z-g1` to `Z-g3` and writes nothing. Then, in this
order:

  1. **The blocking checks**, `unreached/gates.py`. They search the orders the
     stage reads, two endpoints and the curve's twenty, and check each against
     its record.
  2. **The two endpoints**, the escalations alone and the whole train half.
     For each, the rules no labelled case matches, and for every one of them:
     its place in the order, the test cases it matches and decides there, and
     its move alone to the front, read on the test split by first match, split
     at its birth ticket, and by masks, and over the space by masks.
  3. **The back move and the coin** for each endpoint, on both surfaces: every
     unreached rule below every reached one, and 100 seeded placements of the
     same rules among the reached.
  4. **The curve**: the optimizer audit's twenty random-arrival orders, read the
     same way, the coin left out.
  5. **`Z-a` to `Z-e`**, each with §0's label, and the readings of `Z-f`.

It refuses to write if the two routes on the test split ever disagree.

Surfaces: corpus test split 0, 995 cases, and the exhaustive space, 134,400
points, `puro` pool, every count against the truth.

PROVENANCE: PRE-REGISTERED. §0 was signed before any figure here existed; the
gate is what says so.

    python3 -m unreached.score --dry-run           # Z-g1..Z-g3, blocking; writes nothing
    PYTHONHASHSEED=0 python3 -m unreached.score    # Z-a to Z-e, and the readings of Z-f
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from typing import Any, Sequence

from escalations import instrument as I
from escalations.selections import escalations
from harness.provenance import describe, environment
from rung3.local_search import score_order

from . import gates, moves, plan

median = statistics.median


def inside(x, values) -> bool:
    return min(values) <= x <= max(values)


def first_match(order: Sequence[str], matched, cases) -> dict[int, str | None]:
    rank = {rid: k for k, rid in enumerate(order)}
    return {i: (min(matched[i], key=rank.__getitem__) if matched[i] else None)
            for i in cases}


def read_rule(inst, order: list[str], rid: str, base: dict, masks: dict) -> dict[str, Any]:
    """One rule moved alone to the front of `order`, on both surfaces."""
    _tr, te = I.halves(inst)
    truth, action, matched, corpus = (inst["truth"], inst["action"], inst["matched"],
                                      inst["corpus"])
    cases = [i for i in te if rid in matched[i]]
    birth = moves.birth_ticket(corpus, inst["born"][rid], cases)
    fm = first_match(order, matched, cases)
    was = {i: action[fm[i]] == truth[i] for i in cases}
    now = {i: action[rid] == truth[i] for i in cases}
    d_birth = sum(now[i] - was[i] for i in cases if i in birth)
    d_away = sum(now[i] - was[i] for i in cases if i not in birth)
    moved = moves.front(order, rid)
    d_test = score_order(moved, *masks["test"]) - base["test"]
    d_space = score_order(moved, *masks["space"]) - base["space"]
    return {"queue": action[rid], "born_at": inst["born"][rid], "rank": order.index(rid),
            "test_cases": len(cases), "birth_ticket_cases": len(birth),
            "decided_in_order": sum(1 for i in cases if fm[i] == rid),
            "right_in_order": sum(was.values()), "right_moved": sum(now.values()),
            "delta_test": d_test, "delta_test_birth": d_birth,
            "delta_test_away": d_away, "delta_space": d_space,
            "routes_agree": d_test == d_birth + d_away}


def read_order(inst, order: list[str], labelled, masks: dict,
               coin: bool) -> dict[str, Any]:
    """An order, its unreached rules each moved to the front, all moved to the
    back, and, if asked, the coin's placements."""
    _tr, te = I.halves(inst)
    ids, matched, rules = inst["ids"], inst["matched"], inst["rules"]
    U = moves.unreached(ids, matched, labelled)
    base = {"test": score_order(order, *masks["test"]),
            "space": score_order(order, *masks["space"])}
    b = moves.back(order, U)
    out: dict[str, Any] = {
        "labels": len(labelled), "unreached": U,
        "distinct": moves.distinct(rules, U), "copies": moves.copies(rules, U),
        "order": base | {"rare": gates.rare(I.per_class(inst, order, te))},
        "rules": {rid: read_rule(inst, order, rid, base, masks) for rid in U},
        "back": {"test": score_order(b, *masks["test"]),
                 "space": score_order(b, *masks["space"]),
                 "rare": gates.rare(I.per_class(inst, b, te))},
    }
    if coin:
        placed = [moves.coin(order, U, d) for d in range(plan.COIN_DRAWS)]
        t = [score_order(o, *masks["test"]) for o in placed]
        s = [score_order(o, *masks["space"]) for o in placed]
        out["coin"] = {"test": t, "space": s,
                       "test_summary": [min(t), median(t), max(t)],
                       "space_summary": [min(s), median(s), max(s)]}
    return out


def stake(read: dict, rids: Sequence[str], field: str) -> dict[str, Any]:
    """What moving each of `rids` alone to the front gains, losses as zero."""
    d = {r: read["rules"][r][field] for r in rids}
    return {"gainers": sorted(r for r, x in d.items() if x > 0),
            "losers": sorted(r for r, x in d.items() if x < 0),
            "sum_of_gains": sum(max(x, 0) for x in d.values())}


def verdicts(esc: dict) -> list[dict[str, Any]]:
    others = [r for r in esc["distinct"] if r != plan.KEY_RULE]
    away = stake(esc, others, "delta_test_away")
    space = stake(esc, esc["distinct"], "delta_space")
    bt, bs = esc["back"]["test"], esc["back"]["space"]
    ct, cs = esc["coin"]["test"], esc["coin"]["space"]
    return [
        {"row": "Z-a", "statistic": "test split 0: the distinct rules no escalation "
                                    "reaches, the key rule aside, whose move alone to "
                                    "the front gains away from its birth ticket",
         "value": len(away["gainers"]), "gainers": away["gainers"], "line": plan.Z_A_LINE,
         "holds": len(away["gainers"]) >= plan.Z_A_LINE, "thin": None},
        {"row": "Z-b", "statistic": "test split 0: the same rules, what each move gains "
                                    "away from its birth ticket, losses as zero, summed",
         "value": away["sum_of_gains"], "line": plan.Z_B_LINE,
         "holds": away["sum_of_gains"] >= plan.Z_B_LINE, "thin": None},
        {"row": "Z-c", "statistic": "space: every distinct rule no escalation reaches, "
                                    "what each move alone to the front gains, losses as "
                                    "zero, summed",
         "value": space["sum_of_gains"], "gainers": space["gainers"],
         "line": plan.Z_C_LINE, "holds": space["sum_of_gains"] >= plan.Z_C_LINE,
         "thin": None},
        {"row": "Z-d", "statistic": "test split 0: the escalations' order with every "
                                    "rule no escalation reaches moved below every rule "
                                    "one reaches",
         "value": bt, "line": plan.Z_D_LINE, "holds": bt > plan.Z_D_LINE,
         "thin": inside(bt, ct)},
        {"row": "Z-e", "statistic": "space: the same order, the count right of 134,400",
         "value": bs, "line": plan.Z_E_LINE, "holds": bs > plan.Z_E_LINE,
         "thin": inside(bs, cs)},
    ]


def curve_row(inst, order: list[str], labelled, masks: dict, start: str) -> dict:
    r = read_order(inst, order, labelled, masks, coin=False)
    away = stake(r, r["distinct"], "delta_test_away")
    test = stake(r, r["distinct"], "delta_test")
    space = stake(r, r["distinct"], "delta_space")
    return {"labels": r["labels"], "best_from": start,
            "unreached": len(r["unreached"]), "distinct": len(r["distinct"]),
            "order": r["order"], "back": r["back"],
            "stake_test": {"gainers": len(test["gainers"]), "losers": len(test["losers"]),
                           "sum_of_gains": test["sum_of_gains"]},
            "stake_test_away": {"gainers": len(away["gainers"]),
                                "sum_of_gains": away["sum_of_gains"]},
            "stake_space": {"gainers": len(space["gainers"]),
                            "losers": len(space["losers"]),
                            "sum_of_gains": space["sum_of_gains"]},
            "routes_agree": all(x["routes_agree"] for x in r["rules"].values())}


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry = "--dry-run" in argv
    if not dry:
        gate = plan.refuse_unsigned("unreached/score.py writes nothing")
    t0 = time.time()
    print("=" * 78)
    print("PLAN_UNREACHED.md — THE RULES NO LABEL REACHES, MOVED")
    print("=" * 78)
    checks = gates.run_all(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    if dry:
        print(f"\n  --dry-run: the checks ran and nothing was written "
              f"({time.time() - t0:.0f} s).")
        return 0

    inst = I.instance()
    tr, _te = I.halves(inst)
    escs = escalations(tr)
    orders = checks.zg1.pop("orders")
    starts = checks.zg1["starts"]
    sM, sW, sfull, _sn = I.space_masks()
    masks = {"test": I.test_masks(), "space": (sM, sW, sfull)}

    endpoints = {}
    for name, labelled in (("escalations", escs), ("full", tr)):
        endpoints[name] = read_order(inst, orders["endpoints"][name], labelled, masks,
                                     coin=True) | {"best_from": starts[name]}
        e = endpoints[name]
        print(f"  {name:<12} {len(e['unreached'])} unreached   back "
              f"{e['back']['test']} · {e['back']['space']}   order "
              f"{e['order']['test']} · {e['order']['space']}")
    curve = {}
    for key, order in orders["curve"].items():
        k, d = (int(x) for x in key.split("|"))
        curve[key] = curve_row(inst, order, I.record_draw(inst, k, d), masks,
                               starts[key])
        print(f"  {key:<8} {curve[key]['unreached']:>3} unreached   back "
              f"{curve[key]['back']['test'] - curve[key]['order']['test']:+d} · "
              f"{curve[key]['back']['space'] - curve[key]['order']['space']:+d}")

    disagree = [f"{n}:{r}" for n, e in endpoints.items()
                for r, x in e["rules"].items() if not x["routes_agree"]]
    disagree += [k for k, c in curve.items() if not c["routes_agree"]]
    if disagree:
        sys.exit(f"\nREFUSED: the two routes disagree on {disagree}; nothing was "
                 "written.\n")

    rows = verdicts(endpoints["escalations"])
    for r in rows:
        label = "" if r["thin"] is None else (", thin" if r["thin"] else "")
        print(f"  {r['row']}: {'holds' if r['holds'] else 'REFUTED'}{label}  "
              f"{r['value']} against {r['line']}")

    plan.OUT.mkdir(exist_ok=True)
    plan.SCORE_PATH.write_text(json.dumps({
        "_env": environment(split_seed=plan.SPLIT_SEED, coin_seed=plan.COIN_SEED,
                            coin_draws=plan.COIN_DRAWS, budgets=list(plan.BUDGETS)),
        "what": "the rules no label reaches in rung 3's labelled orders: each moved "
                "alone to the front, read with the truth, and all moved to the back, "
                "beside 100 random placements, on both surfaces",
        "plan": str(plan.PLAN),
        "gate": gate,
        "provenance": "PRE-REGISTERED: §0 signed before any figure here existed",
        "surface": "corpus test split 0, 995 cases, and the exhaustive space, 134,400 "
                   "points; puro pool; every count against the truth",
        "gates": {"Z-g1": checks.zg1, "Z-g2": checks.zg2, "Z-g3": checks.zg3,
                  "Z-g4": checks.zg4},
        "rows": {r["row"]: r for r in rows},
        "endpoints": endpoints,
        "curve": curve,
        "orders": orders,
        "seconds": round(time.time() - t0, 1),
    }, indent=2) + "\n")
    print(f"\n-> {plan.SCORE_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
