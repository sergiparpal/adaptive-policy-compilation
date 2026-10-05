"""
The stage of `PLAN_PRIMACY.md`: `L-a`, `L-b`, and the readings of `L-c`.
Zero API calls.

It refuses while the plan is unsigned, before it measures, builds or writes
anything. Then it runs `L-g1` to `L-g4` again, all blocking. Only after both
does it compute a figure of §0.

WHAT IT MEASURES (§0 and §7 of the plan):

  L-a   on the queue pair §2.1's rule picks, the slot effect with one of its two
        queues as the reference: the share of declared answers naming that queue
        when its rule is listed first, minus the share when it is listed second.
        Either queue gives the same value.
  L-b   over every row whose queue pair has a favoured queue, the share with no
        edge when the favoured rule is listed second, minus the share when it is
        listed first.
  L-c   reported, not adjudicated. The first-listed rate and the slot effect:
        overall; on B-d's two sides and on the pairs with no strictly better
        rule, under both definitions of the better rule; by batch; by queue
        pair; by the breadth of the rule listed first; and on Stage C. `L-b`'s
        split into parse failures and third queues, and the retries. And on
        `L-a`'s queue pair, how often the answer names the better rule.

NO SURFACE FOR `L-a` AND `L-b`: they are properties of what was said, and no
truth enters them. Where the truth enters `L-c`, the definition of the better
rule is named, space or corpus as `rung3/edge_direction.py` defines them, and
read from `results2/pair_sample_1600.json`. No module of this package imports
the oracle.

    python3 -m primacy.score --dry-run   # L-g1..L-g4; writes nothing
    python3 -m primacy.score             # refuses while PLAN_PRIMACY.md is unsigned
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from typing import Any

from harness.provenance import environment

from . import gates, plan
from . import rows as R


# ---------------------------------------------------------------------------
# The verdicts
# ---------------------------------------------------------------------------

def verdict_l_a(d: float | None, se: float | None, n1: int, n2: int) -> dict:
    """`L-a` holds at d >= 0.20. Unadjudicable with fewer than
    `L_A_MIN_SIDE` answers in either slot."""
    if d is None or min(n1, n2) < plan.L_A_MIN_SIDE:
        return {"value": d, "se": se, "line": plan.L_A_LINE,
                "verdict": "unadjudicable", "thin": False}
    return {"value": d, "se": se, "line": plan.L_A_LINE,
            "verdict": "holds" if d >= plan.L_A_LINE else "refuted",
            "thin": se is not None and abs(d - plan.L_A_LINE) < se}


def verdict_l_b(diff: float | None, se: float | None) -> dict:
    """`L-b` holds at |difference| < 0.025, refuted at 0.025 or beyond on
    either side."""
    if diff is None:
        return {"value": diff, "se": se, "line": plan.L_B_LINE,
                "verdict": "unadjudicable", "thin": False}
    return {"value": diff, "se": se, "line": plan.L_B_LINE,
            "verdict": "holds" if abs(diff) < plan.L_B_LINE else "refuted",
            "thin": se is not None and abs(abs(diff) - plan.L_B_LINE) < se}


# ---------------------------------------------------------------------------
# The rows of §0
# ---------------------------------------------------------------------------

def l_a(ans: list[dict]) -> dict:
    qp = tuple(sorted(plan.L_A_QUEUE_PAIR))
    ref = qp[0]
    on = [r for r in ans if R.queue_pair(r) == qp]
    out = R.slot_effect(on, lambda r: R.rule_with_action(r, ref))
    out.update({"queue_pair": R.pair_key(qp), "reference_queue": ref})
    return out


def l_b(ans: list[dict], maj: dict) -> dict:
    return R.none_by_favoured_slot(ans, maj)


# ---------------------------------------------------------------------------
# L-c, reported
# ---------------------------------------------------------------------------

def readings(c: gates.Checks, maj: dict) -> dict[str, Any]:
    ans = c.src["answers"]
    truth = {o["index"]: o for o in c.sample["oracle"]}

    def better(r: dict, surface: str) -> str | None:
        b = truth[r["index"]][f"better_{surface}"]
        return r["rule_a"] if b == "a" else r["rule_b"] if b == "b" else None

    def block(rows: list[dict], ref=None) -> dict:
        out = {"first_listed": R.first_listed_rate(rows)}
        if ref is not None:
            out["slot_effect"] = R.slot_effect(rows, ref)
        return out

    out: dict[str, Any] = {
        "overall": {
            "first_listed": R.first_listed_rate(ans),
            "slot_effect_rule_a_reference": R.slot_effect(ans, lambda r: r["rule_a"]),
            "slot_effect_favoured_reference": R.slot_effect(
                ans, lambda r: R.favoured_rule(r, maj)),
        }}

    sides = {}
    for surface in ("space", "corpus"):
        far_pairs = set(c.sample["split_for_B_d"][surface]["unreachable_queue_pairs"])
        strict = [r for r in ans if better(r, surface) is not None]
        far = [r for r in strict if R.pair_key(R.queue_pair(r)) in far_pairs]
        near = [r for r in strict if R.pair_key(R.queue_pair(r)) not in far_pairs]

        def ref(r, s=surface):
            return better(r, s)
        sides[surface] = {
            "reachable": block(near, ref), "unreachable": block(far, ref),
            "all_strict": block(strict, ref),
            "no_strict_better": block([r for r in ans if better(r, surface) is None]),
        }
    out["by_b_d_side"] = sides

    out["by_batch"] = {
        k: block([r for r in ans if r["answer_from"] == k], lambda r: r["rule_a"])
        for k in ("stage_d", "this_run")}

    by_qp = {}
    counts = R.per_queue_pair(ans)
    for key in sorted(counts, key=lambda k: (-sum(counts[k].values()), k)):
        n = sum(counts[key].values())
        if n < plan.READING_MIN_ROWS:
            continue
        q = key.split(" vs ")[0]
        on = [r for r in ans if R.pair_key(R.queue_pair(r)) == key]
        by_qp[key] = {"declared": n, "majority_share": max(counts[key].values()) / n,
                      **block(on, lambda r, q=q: R.rule_with_action(r, q))}
    out["by_queue_pair"] = by_qp

    def ext(r: dict, rule: str) -> int:
        return r["extension_a"] if rule == r["rule_a"] else r["extension_b"]
    broader = [r for r in ans if ext(r, R.first_rule(r)) > ext(r, R.second_rule(r))]
    narrower = [r for r in ans if ext(r, R.first_rule(r)) < ext(r, R.second_rule(r))]
    out["by_breadth_of_the_rule_listed_first"] = {
        "broader_first": block(broader), "narrower_first": block(narrower),
        "equal_extensions_counted_apart": len(ans) - len(broader) - len(narrower)}

    two_way = [r for r in c.hidden["answers"] if r["outcome"] in ("correct", "wrong")]
    first = [r for r in two_way if r["winner_shown_as"] == "A"]
    second = [r for r in two_way if r["winner_shown_as"] == "B"]
    named_first = (sum(1 for r in first if r["outcome"] == "correct")
                   + sum(1 for r in second if r["outcome"] == "wrong"))
    n = len(two_way)
    se = math.sqrt(0.25 / n)
    out["stage_c"] = {
        "what": "the hidden policy's 170 pairs, the same prompt and model; "
                "two-way answers only",
        "first_listed": {"n": n, "hits": named_first, "rate": named_first / n,
                         "twice_minus_one": 2 * named_first / n - 1,
                         "standard_error": se,
                         "deviations_from_a_coin": (named_first / n - 0.5) / se},
        "slot_effect_winner_reference": R.two_sample(
            sum(1 for r in first if r["outcome"] == "correct"), len(first),
            sum(1 for r in second if r["outcome"] == "correct"), len(second)),
    }

    retried, answered = Counter(), Counter()
    for r in ans:
        f = R.favoured_rule(r, maj)
        if f is None or r["answer"] is None:
            continue
        slot = "first" if R.first_rule(r) == f else "second"
        answered[slot] += 1
        retried[slot] += r["attempts"] > 1
    out["retries_by_favoured_slot"] = {
        "what": "among rows with an answer, the share that needed a retry when the "
                "favoured rule is listed second, minus when listed first",
        **R.two_sample(retried["second"], answered["second"],
                       retried["first"], answered["first"])}

    qp = tuple(sorted(plan.L_A_QUEUE_PAIR))
    on = [r for r in R.declared(ans) if R.queue_pair(r) == qp]
    direction = {}
    for surface in ("space", "corpus"):
        strict = [r for r in on if better(r, surface) is not None]
        hits = sum(1 for r in strict if R.winner(r) == better(r, surface))
        direction[surface] = {"n": len(strict), "named_the_better_rule": hits,
                              "rate": hits / len(strict) if strict else None}
    out["l_a_queue_pair_against_the_truth"] = direction
    return out


# ---------------------------------------------------------------------------
# The stage
# ---------------------------------------------------------------------------

def score(c: gates.Checks) -> dict[str, Any]:
    ans = c.src["answers"]
    maj = R.majority(ans)
    a, b = l_a(ans), l_b(ans, maj)
    return {
        "verdicts": {
            "L-a": verdict_l_a(a["difference"], a["standard_error"], a["n1"], a["n2"]),
            "L-b": verdict_l_b(b["difference"], b["standard_error"]),
        },
        "L-a": a, "L-b": b,
        "L-c": readings(c, maj),
    }


def rounded(x: Any, places: int = 6) -> Any:
    """The record rounds when it is written, and only then (`rows.two_sample`)."""
    if isinstance(x, float):
        return round(x, places)
    if isinstance(x, dict):
        return {k: rounded(v, places) for k, v in x.items()}
    if isinstance(x, list):
        return [rounded(v, places) for v in x]
    return x


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="PLAN_PRIMACY.md: L-a, L-b and the readings of L-c. Zero API calls.")
    ap.add_argument("--dry-run", action="store_true",
                    help="run L-g1 to L-g4 and stop; nothing scored, nothing written")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_all(suite=True)
        gates.report(checks)
        print("dry run: nothing scored, nothing written")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"primacy/score.py writes {plan.SCORE_PATH}")
    checks = gates.run_all(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    result = score(checks)
    print()
    for row, v in result["verdicts"].items():
        value = "—" if v["value"] is None else f"{v['value']:+.4f}"
        print(f"  {row}  {value} (se {v['se'] or 0:.4f}, line {v['line']})  ->  "
              f"{v['verdict']}" + ("  (thin)" if v["thin"] else ""))
    plan.OUT.mkdir(exist_ok=True)
    plan.SCORE_PATH.write_text(json.dumps(rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "stage": "scoring",
        "surface": {
            "L-a": "none: a property of the answers on one queue pair; no truth "
                   "enters it",
            "L-b": "none: a property of the answers; no truth enters it",
            "L-c": "none, except where a block names the definition of the better "
                   "rule, space or corpus, read from results2/pair_sample_1600.json",
        },
        "provenance": "PRE-REGISTERED: §0 signed before any of these figures existed",
        "constants": {"source": str(plan.SOURCE), "position_seed": plan.POSITION_SEED,
                      "l_a_queue_pair": list(plan.L_A_QUEUE_PAIR),
                      "l_a_selection": {"min_rows": plan.L_A_SELECT_MIN_ROWS,
                                        "majority_below": plan.L_A_SELECT_BELOW},
                      "l_a_min_side": plan.L_A_MIN_SIDE,
                      "reading_min_rows": plan.READING_MIN_ROWS,
                      "lines": {"L-a": plan.L_A_LINE, "L-b": plan.L_B_LINE}},
        "gates": checks.summary(),
        **result,
    }), indent=2) + "\n")
    print(f"\nwrote {plan.SCORE_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
