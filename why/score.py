"""
The stage of `PLAN_WHY.md`: `Y-a` to `Y-d` on the held-out answers, and the
readings of `Y-e`. Zero API calls.

It refuses while the plan is unsigned, before it measures, builds or writes
anything. Then it runs `Y-g1` to `Y-g4` again, all blocking. Only after both
does it code a held-out `why`.

WHAT IT MEASURES (§0 and §7 of the plan), over the 1,114 declared answers of
the batch answered on 2026-08-25, each with its `why`:

  Y-a   among the answers whose `why` argues specificity, the share whose named
        rule has the smaller extension
  Y-b   among those that argue it without counting conditions, the share whose
        named rule has more conditions
  Y-c   the share of those whose named rule carries a categorical or exact
        condition the other lacks, minus the same share among answers that do
        not argue specificity
  Y-d   on pairs with a strictly better rule on the space, the direction rate of
        answers that argue specificity minus that of answers that do not
  Y-e   reported: the census of codes, labels and languages; the direction rate
        by code under both definitions; the codes by B-d's side; the labels
        against the named rule; every `order` sentence and five quotations per
        code; and every held-out row with its codes. The development figures
        sit beside them.

THE TRUTH enters `Y-d` and `Y-e` only, read per pair from
`results2/pair_sample_1600.json` under both of `rung3/edge_direction.py`'s
definitions. No module of this package imports the oracle.

    python3 -m why.score --dry-run   # Y-g1..Y-g4; writes nothing
    python3 -m why.score             # refuses while PLAN_WHY.md is unsigned
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from harness.provenance import environment

from . import gates, plan
from . import rows as R


# ---------------------------------------------------------------------------
# The verdicts
# ---------------------------------------------------------------------------

def _thin(value, se, line):
    return se is not None and abs(value - line) < se


def verdict_y_a(s: dict) -> dict:
    lo, hi = plan.Y_A_BAND
    v, se, n = s["share"], s["standard_error"], s["n"]
    if v is None or n < plan.MIN_ROWS:
        return {"value": v, "se": se, "band": [lo, hi], "verdict": "unadjudicable",
                "thin": False}
    return {"value": v, "se": se, "band": [lo, hi],
            "verdict": "holds" if lo <= v <= hi else "refuted",
            "thin": _thin(v, se, lo) or _thin(v, se, hi)}


def verdict_y_b(s: dict) -> dict:
    line = plan.Y_B_REFUTED_AT_OR_ABOVE
    v, se, n = s["share"], s["standard_error"], s["n"]
    if v is None or n < plan.MIN_ROWS:
        return {"value": v, "se": se, "line": line, "verdict": "unadjudicable",
                "thin": False}
    return {"value": v, "se": se, "line": line,
            "verdict": "holds" if v < line else "refuted", "thin": _thin(v, se, line)}


def _groups_too_small(d: dict) -> bool:
    return (d["difference"] is None or d["first"]["n"] < plan.MIN_ROWS
            or d["second"]["n"] < plan.MIN_ROWS)


def verdict_y_c(d: dict) -> dict:
    line = plan.Y_C_MIN_DIFFERENCE
    v, se = d["difference"], d["standard_error"]
    if _groups_too_small(d):
        return {"value": v, "se": se, "line": line, "verdict": "unadjudicable",
                "thin": False}
    return {"value": v, "se": se, "line": line,
            "verdict": "holds" if v >= line else "refuted", "thin": _thin(v, se, line)}


def verdict_y_d(d: dict) -> dict:
    line = plan.Y_D_MAX_ABS_DIFFERENCE
    v, se = d["difference"], d["standard_error"]
    if _groups_too_small(d):
        return {"value": v, "se": se, "line": line, "verdict": "unadjudicable",
                "thin": False}
    return {"value": v, "se": se, "line": line,
            "verdict": "holds" if abs(v) < line else "refuted",
            "thin": _thin(abs(v), se, line)}


# ---------------------------------------------------------------------------
# Y-e, reported
# ---------------------------------------------------------------------------

def by_code(rows: list[dict]) -> dict:
    out = {}
    for code in ("spec", "count", "queue", "match", "order"):
        sub = R.with_code(rows, code)
        out[code] = {"n": len(sub), "right_space": R.share(sub, "right_space"),
                     "right_corpus": R.share(sub, "right_corpus")}
    none = [r for r in rows if not r["codes"] & {"spec", "queue", "match", "order"}]
    out["no_reason_code"] = {"n": len(none), "right_space": R.share(none, "right_space"),
                             "right_corpus": R.share(none, "right_corpus")}
    for surface in ("space", "corpus"):
        out[f"queue_minus_rest_{surface}"] = R.difference(
            R.share(R.with_code(rows, "queue"), f"right_{surface}"),
            R.share(R.without_code(rows, "queue"), f"right_{surface}"))
    return out


def by_side(rows: list[dict], sample: dict) -> dict:
    far = set(sample["split_for_B_d"]["space"]["unreachable_queue_pairs"])
    out = {}
    for side in ("reachable", "unreachable", "no_strict_better"):
        if side == "no_strict_better":
            sub = [r for r in rows if r["right_space"] is None]
        else:
            sub = [r for r in rows if r["right_space"] is not None
                   and (r["queue_pair"] in far) == (side == "unreachable")]
        out[side] = {"n": len(sub),
                     "spec": sum(1 for r in sub if "spec" in r["codes"]),
                     "queue": sum(1 for r in sub if "queue" in r["codes"])}
    return out


def labels_against_the_named_rule(rows: list[dict]) -> dict:
    out = {"named_only": 0, "other_only": 0, "both": 0, "neither": 0}
    for r in rows:
        named = r["label_a"] if r["named_label"] == "A" else r["label_b"]
        other = r["label_b"] if r["named_label"] == "A" else r["label_a"]
        key = ("both" if named and other else "named_only" if named
               else "other_only" if other else "neither")
        out[key] += 1
    return out


def quotes(rows: list[dict]) -> dict:
    ordered = sorted(rows, key=lambda r: r["index"])
    out = {code: [{"index": r["index"], "why": r["why"]}
                  for r in ordered if code in r["codes"]][:plan.QUOTES_PER_CODE]
           for code in ("spec", "count", "queue", "match")}
    out["order_all"] = [{"index": r["index"], "why": r["why"]}
                        for r in ordered if "order" in r["codes"]]
    out["spec_naming_the_broader_rule"] = [
        {"index": r["index"], "why": r["why"]} for r in ordered
        if "spec" in r["codes"] and not r["narrower"]][:plan.QUOTES_PER_CODE]
    return out


def per_row(rows: list[dict]) -> list[dict]:
    return [{"index": r["index"], "codes": sorted(r["codes"]),
             "label_a": r["label_a"], "label_b": r["label_b"],
             "language": r["language"], "named_label": r["named_label"],
             "narrower": r["narrower"], "more_conditions": r["more_conditions"],
             "categorical": r["categorical"], "right_space": r["right_space"],
             "right_corpus": r["right_corpus"]}
            for r in sorted(rows, key=lambda r: r["index"])]


# ---------------------------------------------------------------------------
# The stage
# ---------------------------------------------------------------------------

def held_out_rows(c: gates.Checks) -> list[dict]:
    return R.learned_rows(gates.part(c.src, plan.TEST_BATCH),
                          gates.truth_by_index(c.sample), lambda r: plan.TEST_BATCH)


def score(c: gates.Checks) -> dict[str, Any]:
    rows = held_out_rows(c)
    s = R.section_0(rows)
    dev = gates.development_rows(c.src, c.hidden, c.sample)
    return {
        "verdicts": {"Y-a": verdict_y_a(s["Y-a"]), "Y-b": verdict_y_b(s["Y-b"]),
                     "Y-c": verdict_y_c(s["Y-c"]), "Y-d": verdict_y_d(s["Y-d"])},
        "section_0": s,
        "Y-e": {
            "census": R.census(rows),
            "base_rates": {k: R.share(rows, k) for k in
                           ("narrower", "more_conditions", "categorical",
                            "right_space", "right_corpus")},
            "by_code": by_code(rows),
            "by_b_d_side_space": by_side(rows, c.sample),
            "labels_against_the_named_rule": labels_against_the_named_rule(rows),
            "quotes": quotes(rows),
            "development": {k: {"census": R.census(v), "section_0": R.section_0(v)}
                            for k, v in dev.items()},
        },
        "rows": per_row(rows),
    }


def rounded(x: Any, places: int = 6) -> Any:
    if isinstance(x, float):
        return round(x, places)
    if isinstance(x, dict):
        return {k: rounded(v, places) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [rounded(v, places) for v in x]
    if isinstance(x, frozenset):
        return sorted(x)
    return x


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="PLAN_WHY.md: Y-a to Y-d, and the readings of Y-e. Zero API calls.")
    ap.add_argument("--dry-run", action="store_true",
                    help="run Y-g1 to Y-g4 and stop; nothing scored, nothing written")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_all(suite=True)
        gates.report(checks)
        print("dry run: nothing scored, nothing written")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"why/score.py writes {plan.SCORE_PATH}")
    checks = gates.run_all(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    result = score(checks)
    print()
    for row, v in result["verdicts"].items():
        value = "—" if v["value"] is None else f"{v['value']:+.4f}"
        line = v.get("band", v.get("line"))
        print(f"  {row}  {value} (se {v['se'] or 0:.4f}, line {line})  ->  "
              f"{v['verdict']}" + ("  (thin)" if v["thin"] else ""))
    plan.OUT.mkdir(exist_ok=True)
    plan.SCORE_PATH.write_text(json.dumps(rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "stage": "scoring",
        "surface": {
            "Y-a, Y-b, Y-c": "none: properties of what was said and of the two rules "
                             "shown; no truth enters them",
            "Y-d": "the exhaustive space: the better rule over the shared region, "
                   "rung3/edge_direction.py's definition",
            "Y-e": "both definitions wherever the truth enters, each named",
        },
        "provenance": ("PRE-REGISTERED on a held-out batch: §0 signed before any "
                       "held-out why was coded; the codebook was frozen on the "
                       "development set, whose figures §0 declares"),
        "constants": {"codebook_digest": plan.CODEBOOK_DIGEST,
                      "dev_batch": plan.DEV_BATCH, "test_batch": plan.TEST_BATCH,
                      "min_rows": plan.MIN_ROWS,
                      "lines": {"Y-a": list(plan.Y_A_BAND),
                                "Y-b": plan.Y_B_REFUTED_AT_OR_ABOVE,
                                "Y-c": plan.Y_C_MIN_DIFFERENCE,
                                "Y-d": plan.Y_D_MAX_ABS_DIFFERENCE}},
        "gates": checks.summary(),
        **result,
    }), indent=2, ensure_ascii=False) + "\n")
    print(f"\nwrote {plan.SCORE_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
