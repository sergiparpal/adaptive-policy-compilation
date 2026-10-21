"""
Stage C of `PLAN_MANUAL.md`: scoring, and the six adjudications. **Free.**

It reads the compile session and the twelve loop runs, scores every valid ask
and every run on every cell §0 names, and adjudicates `G-a` to `G-f` against
their lines, exactly, as fractions of counts. *Thin* and *unadjudicable* are
§0's, not this module's:

  * a row reading a level with fewer than `MIN_VALID_ASKS` valid asks, or fewer
    than `MIN_RUNS` runs, is unadjudicable;
  * a verdict is thin when one ask or run, put in place of its own arm's median,
    would put the statistic on the other side of the line — for `G-f`, when
    dropping any one run of either level would.

`G-g`, reported and not adjudicated, is everything else §0 lists.

    PYTHONHASHSEED=0 python3 -m manual.score --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m manual.score
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
from fractions import Fraction
from typing import Any

from harness.provenance import describe, environment

from blind import rows as brows
from overlap.rows import o_a
from reuse.structure import copies

from . import compile as C
from . import gates, plan
from . import instrument as I
from .sample import cells

ONLINE = ("reuse_rate", "silent_error_rate", "e2e_accuracy", "proposal_action_accuracy",
          "escalations", "conflicts", "impasses", "n_rules", "failed_proposals",
          "rejected_rules", "edges_proposed", "edges_accepted", "edge_reasons")
RARE_CLASSES = ("ONCALL_ESCALATION", "SECURITY_INCIDENT")


# ---------------------------------------------------------------------------
# One ask, one run
# ---------------------------------------------------------------------------

def providers(attempts: list[dict]) -> Counter:
    return Counter(str(a.get("provider")) for a in attempts)


def score_ask(row: dict) -> dict[str, Any]:
    out: dict[str, Any] = {"pass": row["pass"], "level": row["level"],
                           "valid": row["valid"], "why_invalid": row.get("why_invalid"),
                           "failure": row.get("failure"),
                           "providers": dict(providers(row.get("call_attempts") or []))}
    if not row["valid"]:
        return out
    raw, _ = C.rules_of(row["payload"])
    inst = C.install(raw, I.space())
    rules = [r.as_dict() for r in inst.rules]
    c = cells(inst.engine)
    out.update({
        "installed": inst.summary(), "rejected": inst.rejected,
        "inversions": len(C.inversions(inst)),
        "first_match_space": I.first_match_over_space(inst.rules),
        "cells": c, "space": I.exact(c["space"]), "corpus": I.exact(c["corpus"]),
        "macro_recall": I.macro_recall(c["space"]),
        "k_a": I.k_a_exact(rules), "o_a": o_a(rules, I.space()),
        "reproduces": I.reproduces(inst.engine), "by_region": I.by_region(inst.engine),
    })
    return out


def first_full_cover(record: dict) -> int | None:
    """§6.7: the case at which the run's base first covered the whole space, if
    it did. From that case on, nothing impasses."""
    sp = I.space()
    full = (1 << sp.n) - 1
    acc = 0
    for r in sorted(record["rules"], key=lambda r: (r["born_at"], r["rule_id"])):
        acc |= brows.ext_of(r, sp)
        if acc == full:
            return r["born_at"]
    return None


def score_run(record: dict) -> dict[str, Any]:
    eng = I.final_engine(record)
    rules = record["rules"]
    c = cells(eng)
    ext = {r.rule_id: eng.ext[r.rule_id] for r in eng.rules}
    action = {r.rule_id: r.action for r in eng.rules}
    attempts = [a for x in record.get("calls") or [] for a in x.get("call_attempts") or []]
    esc = [r for r in record["records"] if r["escalated"]]
    return {
        "level": record["level"], "rep": record["rep"],
        "dates": [record.get("started_at"), record["_env"].get("recorded_at")],
        "cells": c, "space": I.exact(c["space"]), "corpus": I.exact(c["corpus"]),
        "macro_recall": I.macro_recall(c["space"]),
        "k_a": I.k_a_exact(rules), "o_a": o_a(rules, I.space()),
        "prop": I.proposals(record),
        "online": {k: record["metrics"].get(k) for k in ONLINE},
        "rare": {q: {"escalated": sum(1 for r in esc if r["truth"] == q),
                     "decided_by_a_rule": sum(1 for r in record["records"]
                                              if r["truth"] == q and r["outcome"] == "ACTION"),
                     "decided_right": sum(1 for r in record["records"]
                                          if r["truth"] == q and r["outcome"] == "ACTION"
                                          and r["correct"])}
                 for q in RARE_CLASSES},
        "first_full_cover": first_full_cover(record),
        "copies": copies(rules, ext, action, listed=False),
        "reproduces": I.reproduces(eng), "by_region": I.by_region(eng),
        "edge_rows": brows.edge_rows(record, eng, I.space_truth(), I.outside()),
        "providers": dict(providers(attempts)),
    }


# ---------------------------------------------------------------------------
# The rows
# ---------------------------------------------------------------------------

def median_of(values: list[Fraction], minimum: int) -> Fraction | None:
    return statistics.median(values) if len(values) >= minimum else None


def side(stat: Fraction, line: Fraction, above: bool) -> bool:
    """Whether `stat` is on the band's side of `line`: `>=` or, for G-c, `>`."""
    return stat > line if above else stat >= line


def single(values: list[Fraction], line: Fraction, minimum: int,
           above: bool = False) -> dict[str, Any]:
    med = median_of(values, minimum)
    if med is None:
        return {"verdict": "unadjudicable", "n": len(values), "values": values}
    holds = side(med, line, above)
    return {"verdict": "holds" if holds else "refuted", "statistic": med,
            "thin": any(side(v, line, above) != holds for v in values),
            "n": len(values), "values": values}


def difference(a: list[Fraction], b: list[Fraction], line: Fraction,
               min_a: int, min_b: int) -> dict[str, Any]:
    ma, mb = median_of(a, min_a), median_of(b, min_b)
    if ma is None or mb is None:
        return {"verdict": "unadjudicable", "n": [len(a), len(b)], "values": [a, b]}
    stat = ma - mb
    holds = side(stat, line, False)
    alternatives = [v - mb for v in a] + [ma - v for v in b]
    return {"verdict": "holds" if holds else "refuted", "statistic": stat,
            "medians": [ma, mb],
            "thin": any(side(x, line, False) != holds for x in alternatives),
            "n": [len(a), len(b)], "values": [a, b]}


def pooled_prop(runs: list[dict]) -> Fraction | None:
    right = sum(r["prop"]["right"] for r in runs)
    asked = sum(r["prop"]["escalations"] for r in runs)
    return Fraction(right, asked) if asked else None


def pooled_difference(a: list[dict], b: list[dict], line: Fraction) -> dict[str, Any]:
    pa, pb = pooled_prop(a), pooled_prop(b)
    if len(a) < plan.MIN_RUNS or len(b) < plan.MIN_RUNS or pa is None or pb is None:
        return {"verdict": "unadjudicable", "n": [len(a), len(b)]}
    stat = pa - pb
    holds = side(stat, line, False)
    flips = []
    for i in range(len(a)):
        p = pooled_prop(a[:i] + a[i + 1:])
        flips.append(p is not None and side(p - pb, line, False) != holds)
    for i in range(len(b)):
        p = pooled_prop(b[:i] + b[i + 1:])
        flips.append(p is not None and side(pa - p, line, False) != holds)
    return {"verdict": "holds" if holds else "refuted", "statistic": stat,
            "pooled": [pa, pb], "thin": any(flips), "n": [len(a), len(b)]}


def verdicts(asks: dict[int, list[dict]], runs: dict[int, list[dict]]) -> dict[str, Any]:
    def c(level: int, key: str) -> list[Fraction]:
        return [x[key] for x in asks[level] if x["valid"]]

    def l(level: int, key: str) -> list[Fraction]:
        return [x[key] for x in runs[level]]

    va, vr = plan.MIN_VALID_ASKS, plan.MIN_RUNS
    return {
        "G-a": single(c(3, "space"), plan.G_A_LINE, va),
        "G-b": difference(c(1, "macro_recall"), c(0, "macro_recall"), plan.G_B_LINE, va, va),
        "G-c": single(l(3, "k_a"), plan.G_C_LINE, vr, above=True),
        "G-d": difference(c(3, "space"), l(3, "space"), plan.G_D_LINE, va, vr),
        "G-e": difference(l(2, "corpus"), l(0, "corpus"), plan.G_E_LINE, vr, vr),
        "G-f": pooled_difference(runs[1], runs[0], plan.G_F_LINE),
    }


# ---------------------------------------------------------------------------
# G-g
# ---------------------------------------------------------------------------

def reported(asks: dict[int, list[dict]], runs: dict[int, list[dict]],
             missing: list[str]) -> dict[str, Any]:
    reuse = [I.final_engine(rec) for rec in I.reuse_records()]
    drift = {"plan_reuse_2026_09_30": [
        {"online": {k: rec["metrics"].get(k) for k in ONLINE},
         "space": I.exact(I.over_space(eng)), "corpus": I.exact(I.over_corpus(eng)),
         "k_a": I.k_a_exact(rec["rules"])}
        for rec, eng in zip(I.reuse_records(), reuse)],
        "l_0_today": [{"online": r["online"], "space": r["space"], "corpus": r["corpus"],
                       "k_a": r["k_a"]} for r in runs[0]]}
    direction = {lv: brows.direction([r["edge_rows"] for r in runs[lv]], "space_out")
                 for lv in plan.LEVELS}
    return {
        "asks": {lv: asks[lv] for lv in plan.LEVELS},
        "runs": {lv: [{k: v for k, v in r.items() if k != "edge_rows"} for r in runs[lv]]
                 for lv in plan.LEVELS},
        "prop_by_level": {lv: {"pooled": pooled_prop(runs[lv]),
                               "by_queue": _pool_queues(runs[lv])} for lv in plan.LEVELS},
        "k_b_beyond_the_keyword": {lv: d for lv, d in direction.items()},
        "k_b_reported_where_it_has_20_units": {lv: d["units"] >= 20
                                               for lv, d in direction.items()},
        "drift": drift,
        "missing": missing,
    }


def _pool_queues(rs: list[dict]) -> dict[str, list[int]]:
    acc: dict[str, list[int]] = {}
    for r in rs:
        for q, v in r["prop"]["by_queue"].items():
            a = acc.setdefault(q, [0, 0])
            a[0] += v["right"]
            a[1] += v["of"]
    return acc


# ---------------------------------------------------------------------------

def load() -> tuple[dict[int, list[dict]], dict[int, list[dict]], list[str]]:
    rec = json.loads(plan.compile_path("session").read_text())
    asks: dict[int, list[dict]] = {lv: [] for lv in plan.LEVELS}
    for row in sorted(rec["rows"], key=lambda r: r["position"]):
        asks[row["level"]].append(score_ask(row))
    runs: dict[int, list[dict]] = {lv: [] for lv in plan.LEVELS}
    missing = []
    for rep, lv in plan.loop_schedule():
        path = plan.loop_path(lv, rep)
        if not path.exists():
            missing.append(str(path))
            continue
        runs[lv].append(score_run(json.loads(path.read_text())))
    return asks, runs, missing


def plain(x: Any) -> Any:
    """Fractions as `p/q` strings beside their float, for a JSON record."""
    if isinstance(x, Fraction):
        return {"fraction": f"{x.numerator}/{x.denominator}", "value": float(x)}
    if isinstance(x, dict):
        return {str(k): plain(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [plain(v) for v in x]
    return x


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage C of PLAN_MANUAL.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run G-g1 to G-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1
    gate = plan.refuse_unsigned("manual/score.py writes Stage C")
    if not plan.compile_path("session").exists():
        sys.exit(f"\nREFUSED: no compile session at {plan.compile_path('session')}. "
                 "Nothing was written.\n")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    asks, runs, missing = load()
    v = verdicts(asks, runs)
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "C",
              "signature": gate, "gates": checks.summary(),
              "lines": {"G-a": plan.G_A_LINE, "G-b": plan.G_B_LINE, "G-c": plan.G_C_LINE,
                        "G-d": plan.G_D_LINE, "G-e": plan.G_E_LINE, "G-f": plan.G_F_LINE},
              "verdicts": v, "G-g": reported(asks, runs, missing)}
    plan.score_path().write_text(json.dumps(plain(record), indent=2, default=str))
    for row, r in v.items():
        stat = r.get("statistic")
        print(f"  {row}: {r['verdict']:<14} {'' if stat is None else f'{float(stat):.4f}'}"
              f"{'  (thin)' if r.get('thin') else ''}")
    print(f"\n-> {plan.score_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
