"""
Stage C of `PLAN_FIDELITY.md`: the five adjudications, from Stage B's records.
Free, and it refuses while the plan is unsigned.

Every Stage B record is checked first. It must carry this plan's protocol and
the digest of the Stage A record that the checks rebuild (§8). Then, per item, `a₁` and
`a₂` are the two fresh answers, `r` the answer compared with and `y` the true
queue, all read off the records:

  F-a  births, pooled: S − A against the answer recorded at birth   holds at <= 0.05
  F-b  per run: S − A against the deciding rule's action            holds at >= 0.10
  F-c  per run: the model's accuracy minus the rule's               holds at > 0
  F-d  per run: on the rule's errors, the share the model shares    holds at >= 0.60
  F-e  per run: ONCALL tickets that both answers name ONCALL        holds at >= 1

`S` is the share of items whose two answers agree, and `A` the mean of
`½(1[a₁=r] + 1[a₂=r])`. **The median over runs adjudicates F-b to F-e**, each
run's value beside it; F-a is pooled. Every value carries its standard error,
finite-population for the sampled rows. A verdict within one standard error of
its line is labelled thin, and for F-e a count of exactly 1 is (§0). A run
whose sampled decisions lack a valid pair more often than MAX_INVALID_SHARE has
no value (§5.5).

Recorded beside the rows and never in a denominator (§9):
  * `S`, `A` and both accuracies;
  * the four cells — both right, loss, gain, both wrong;
  * every row split by the deciding rule's birth;
  * the proxy against the measurement, and per-rule figures;
  * disagreement as an alarm;
  * `F-a`'s accuracy beside its agreement;
  * the rare classes in counts;
  * Stage A's baselines and the ticket-only arm (`F-f`);
  * the run itself: failures, invalid answers, the pace.

    python3 -m fidelity.score --dry-run
    python3 -m fidelity.score               # refuses while PLAN_FIDELITY.md is unsigned
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import statistics
import sys
from typing import Any, Callable, Iterable

from harness.provenance import describe, environment
from harness.dsl import RuleValidationError

from reuse.analysis import births, median_of
from rung2.engine2 import validate_conditions

from . import ask, plan, sample

HOLDS, REFUTED, NO_VERDICT = "holds", "refuted", "unadjudicable"
REQUIRED = ("births", "base1", "base2", "base3")


# ---------------------------------------------------------------------------
# §0's five lines, as functions, so that their edges can be pinned
# ---------------------------------------------------------------------------

def verdict_f_a(gap: float | None) -> str:
    if gap is None:
        return NO_VERDICT
    return HOLDS if gap <= plan.F_A_MAX_GAP else REFUTED


def verdict_f_b(gap: float | None) -> str:
    if gap is None:
        return NO_VERDICT
    return HOLDS if gap >= plan.F_B_MIN_GAP else REFUTED


def verdict_f_c(difference: float | None) -> str:
    if difference is None:
        return NO_VERDICT
    return HOLDS if difference > plan.F_C_REFUTED_AT_OR_BELOW else REFUTED


def verdict_f_d(share: float | None) -> str:
    if share is None:
        return NO_VERDICT
    return HOLDS if share >= plan.F_D_MIN_SHARE else REFUTED


def verdict_f_e(count: float | None) -> str:
    if count is None:
        return NO_VERDICT
    return HOLDS if count >= plan.F_E_MIN_ONCALL else REFUTED


VERDICTS = {"F-a": verdict_f_a, "F-b": verdict_f_b, "F-c": verdict_f_c,
            "F-d": verdict_f_d, "F-e": verdict_f_e}
LINES = {"F-a": plan.F_A_MAX_GAP, "F-b": plan.F_B_MIN_GAP,
         "F-c": plan.F_C_REFUTED_AT_OR_BELOW, "F-d": plan.F_D_MIN_SHARE,
         "F-e": plan.F_E_MIN_ONCALL}


# ---------------------------------------------------------------------------
# The arithmetic, pure: answers grouped by item
# ---------------------------------------------------------------------------

def group(rows: Iterable[dict]) -> dict[str, dict]:
    """A session's answers by item: each pass's answer, None when not valid."""
    out: dict[str, dict] = {}
    for r in rows:
        e = out.setdefault(r["id"], {"id": r["id"], "kind": r["kind"],
                                     "run": r["run"], "idx": r["idx"],
                                     "labels": r["labels"], "answers": {},
                                     "payloads": {}})
        e["answers"][r["pass"]] = r["action"] if r["valid"] else None
        e["payloads"][r["pass"]] = r.get("payload")
    return out


def valid_pair(e: dict) -> tuple[str, str] | None:
    a1, a2 = e["answers"].get(1), e["answers"].get(2)
    return (a1, a2) if a1 is not None and a2 is not None else None


def mean(xs: list[float]) -> float | None:
    return sum(xs) / len(xs) if xs else None


def standard_error(values: list[float], population: int | None = None) -> float | None:
    """Of a mean of `values`. With `population`, finite-population: the items
    were drawn without replacement from that many (§0)."""
    n = len(values)
    if n < 2:
        return None
    fpc = math.sqrt(max(0.0, 1 - n / population)) if population else 1.0
    return statistics.stdev(values) / math.sqrt(n) * fpc


def agreement_gap(entries: Iterable[dict], against: Callable[[dict], str]) -> dict:
    """`S − A`: two answers agreeing with each other, against their agreeing with
    `against(e)`. The exchangeability null of §2.2 puts it at zero."""
    s, a, d = [], [], []
    for e in entries:
        pair = valid_pair(e)
        if pair is None:
            continue
        r = against(e)
        si = 1.0 if pair[0] == pair[1] else 0.0
        ai = ((pair[0] == r) + (pair[1] == r)) / 2
        s.append(si)
        a.append(ai)
        d.append(si - ai)
    return {"n": len(d), "S": mean(s), "A": mean(a), "gap": mean(d), "values": d}


def accuracy_difference(entries: Iterable[dict]) -> dict:
    """F-c: the model's accuracy, both answers counted, minus the rule's."""
    model, rule, d = [], [], []
    for e in entries:
        pair = valid_pair(e)
        if pair is None:
            continue
        y, r = e["labels"]["truth"], e["labels"]["rule_action"]
        m = ((pair[0] == y) + (pair[1] == y)) / 2
        ru = 1.0 if r == y else 0.0
        model.append(m)
        rule.append(ru)
        d.append(m - ru)
    return {"n": len(d), "model_accuracy": mean(model), "rule_accuracy": mean(rule),
            "difference": mean(d), "values": d}


def own_error_share(entries: Iterable[dict]) -> dict:
    """F-d: on the decisions the rule got wrong, how wrong the model is too."""
    vals = []
    for e in entries:
        pair = valid_pair(e)
        y, r = e["labels"]["truth"], e["labels"]["rule_action"]
        if pair is None or r == y:
            continue
        vals.append(((pair[0] != y) + (pair[1] != y)) / 2)
    return {"n": len(vals), "share": mean(vals), "values": vals}


def oncall_named(entries: Iterable[dict]) -> dict:
    """F-e: the ONCALL tickets on which both answers name the queue."""
    tickets = named = lacking = 0
    for e in entries:
        tickets += 1
        pair = valid_pair(e)
        if pair is None:
            lacking += 1
        elif pair == (plan.ONCALL, plan.ONCALL):
            named += 1
    return {"tickets": tickets, "named_by_both": named, "lacking_a_valid_pair": lacking}


def thin(value: float | None, line: float, se: float | None) -> bool | None:
    if value is None or se is None:
        return None
    return abs(value - line) <= se


def draws(entries: Iterable[dict]):
    """Each valid answer of each item with a valid pair, with its item."""
    for e in entries:
        pair = valid_pair(e)
        if pair is not None:
            for a in pair:
                yield e, a


# ---------------------------------------------------------------------------
# Beside the rows
# ---------------------------------------------------------------------------

def cells(entries: list[dict]) -> dict[str, Any]:
    """§0's decomposition, per answer: both right, loss, gain, both wrong."""
    c = collections.Counter()
    for e, a in draws(entries):
        y, r = e["labels"]["truth"], e["labels"]["rule_action"]
        if a == y and r == y:
            c["both_right"] += 1
        elif a == y:
            c["loss"] += 1                  # rule wrong, model right
        elif r == y:
            c["gain"] += 1                  # rule right, model wrong
        elif a == r:
            c["both_wrong_same_queue"] += 1
        else:
            c["both_wrong_other_queues"] += 1
    total = sum(c.values())
    return {"answers": total, **{k: c[k] for k in ("both_right", "loss", "gain",
            "both_wrong_same_queue", "both_wrong_other_queues")},
            "shares": {k: v / total for k, v in c.items()} if total else {}}


def alarm(entries: list[dict]) -> dict[str, Any]:
    """Disagreement with a fresh answer as a label-free alarm (§9): the rule's
    error rate where the answer disagrees with it and where it agrees."""
    c = collections.Counter()
    for e, a in draws(entries):
        wrong = e["labels"]["rule_action"] != e["labels"]["truth"]
        side = "disagree" if a != e["labels"]["rule_action"] else "agree"
        c[side] += 1
        c[f"{side}_rule_wrong"] += wrong
    return {"answers_disagreeing": c["disagree"], "answers_agreeing": c["agree"],
            "rule_wrong_where_disagreeing": (c["disagree_rule_wrong"] / c["disagree"]
                                             if c["disagree"] else None),
            "rule_wrong_where_agreeing": (c["agree_rule_wrong"] / c["agree"]
                                          if c["agree"] else None)}


def proxy_concordance(entries: list[dict], born_wrong: Callable[[dict], bool]) -> dict:
    """On the rule's errors: how often `U-c`'s split by birth and the fresh
    answer agree on whose error it was. The proxy calls an error the model's own
    when the rule was born wrong."""
    agree = total = 0
    for e, a in draws(entries):
        y = e["labels"]["truth"]
        if e["labels"]["rule_action"] == y:
            continue
        total += 1
        agree += born_wrong(e) == (a != y)
    return {"answers_on_rule_errors": total,
            "concordant": agree, "share": agree / total if total else None}


def per_rule(entries: list[dict], minimum: int = 20) -> dict[str, dict]:
    by: dict[str, list[dict]] = collections.defaultdict(list)
    for e in entries:
        by[e["labels"]["rule_id"]].append(e)
    out = {}
    for rid, es in sorted(by.items()):
        if len(es) < minimum:
            continue
        g = agreement_gap(es, lambda e: e["labels"]["rule_action"])
        c = accuracy_difference(es)
        out[rid] = {"sampled": len(es), "rule_action": es[0]["labels"]["rule_action"],
                    "S": g["S"], "A": g["A"], "model_accuracy": c["model_accuracy"],
                    "rule_accuracy": c["rule_accuracy"], "difference": c["difference"]}
    return out


def run_itself(rows: list[dict], corpus) -> dict[str, Any]:
    validated = 0
    for r in rows:
        if r.get("payload"):
            try:
                validate_conditions(r["payload"], case=corpus[r["idx"]])
                validated += 1
            except RuleValidationError:
                pass
    seconds = [r["seconds"] for r in rows if r.get("seconds") is not None]
    return {"calls": len(rows),
            "failed": sum(1 for r in rows if r.get("failure")),
            "invalid_actions": sum(1 for r in rows if not r["failure"] and not r["valid"]),
            "written_rules_that_would_validate": validated,
            "median_seconds_per_call": statistics.median(seconds) if seconds else None}


# ---------------------------------------------------------------------------
# The rows
# ---------------------------------------------------------------------------

def score_births(rows: list[dict]) -> dict[str, Any]:
    entries = group(rows)
    by_run = collections.defaultdict(list)
    for e in entries.values():
        by_run[e["run"]].append(e)
    whole = agreement_gap(entries.values(), lambda e: e["labels"]["recorded_answer"])
    fresh, recorded = [], []
    for e, a in draws(entries.values()):
        fresh.append(1.0 if a == e["labels"]["truth"] else 0.0)
    for e in entries.values():
        if valid_pair(e) is not None:
            recorded.append(1.0 if e["labels"]["recorded_answer_right"] else 0.0)
    return {
        "value": whole["gap"], "S": whole["S"], "A": whole["A"], "n": whole["n"],
        "prompts": len(entries),
        "standard_error": standard_error(whole["values"]),
        "per_run": {f"run{k}": agreement_gap(v, lambda e: e["labels"]["recorded_answer"])["gap"]
                    for k, v in sorted(by_run.items())},
        "accuracy": {"recorded_answers": mean(recorded), "fresh_answers": mean(fresh)},
    }


def score_run(k: int, rows: list[dict], rec: dict, corpus) -> dict[str, Any]:
    entries = group(rows)
    born, _ = births(rec)
    population = sum(1 for r in rec["records"] if r["outcome"] == "ACTION")
    silent = sum(1 for r in rec["records"] if r["outcome"] == "ACTION" and not r["correct"])
    uniform = [e for e in entries.values() if e["labels"].get("uniform")]
    lacking = sum(1 for e in uniform if valid_pair(e) is None)
    defined = bool(uniform) and lacking / len(uniform) <= plan.MAX_INVALID_SHARE

    b = agreement_gap(uniform, lambda e: e["labels"]["rule_action"])
    c = accuracy_difference(uniform)
    d = own_error_share(uniform)
    oncall = [e for e in entries.values() if e["labels"].get("census") == plan.ONCALL]
    security = [e for e in entries.values() if e["labels"].get("census") == plan.SECURITY]
    e_ = oncall_named(oncall)

    def born_wrong(e: dict) -> bool:
        return not born[e["labels"]["rule_id"]]["proposal_action_correct"]

    split = {}
    for side, keep in (("born_right", False), ("born_wrong", True)):
        es = [e for e in uniform if born_wrong(e) == keep]
        g = agreement_gap(es, lambda e: e["labels"]["rule_action"])
        a = accuracy_difference(es)
        o = own_error_share(es)
        split[side] = {"n": g["n"], "S": g["S"], "A": g["A"], "gap": g["gap"],
                       "model_accuracy": a["model_accuracy"],
                       "rule_accuracy": a["rule_accuracy"],
                       "difference": a["difference"], "own_error_share": o["share"]}
    return {
        "run": k,
        "population": {"decided": population, "silent_errors": silent},
        "validity": {"sampled": len(uniform), "lacking_a_valid_pair": lacking,
                     "defined": defined},
        "rows": {"F-b": b["gap"] if defined else None,
                 "F-c": c["difference"] if defined else None,
                 "F-d": d["share"] if defined else None,
                 "F-e": e_["named_by_both"]},
        "standard_errors": {"F-b": standard_error(b["values"], population),
                            "F-c": standard_error(c["values"], population),
                            "F-d": standard_error(d["values"], silent),
                            "F-e": None},
        "beside": {
            "S": b["S"], "A": b["A"], "n": b["n"], "silent_errors_scored": d["n"],
            "model_accuracy": c["model_accuracy"], "rule_accuracy": c["rule_accuracy"],
            "cells": cells(uniform),
            "by_birth": split,
            "proxy_against_measurement": proxy_concordance(uniform, born_wrong),
            "per_rule": per_rule(uniform),
            "alarm": alarm(uniform),
            "ONCALL": {**e_, "answers_by_queue": dict(collections.Counter(
                a for _, a in draws(oncall)))},
            "SECURITY": {
                "decisions": len(security),
                "rule_wrong": sum(1 for e in security
                                  if e["labels"]["rule_action"] != plan.SECURITY),
                "answers_naming_it": sum(1 for _, a in draws(security)
                                         if a == plan.SECURITY),
                "answers_naming_it_where_the_rule_was_wrong": sum(
                    1 for e, a in draws(security)
                    if a == plan.SECURITY and e["labels"]["rule_action"] != plan.SECURITY),
                "answers": 2 * sum(1 for e in security if valid_pair(e))},
            "run_itself": run_itself(rows, corpus),
        },
    }


def median_row(per_run: list[dict], row: str) -> dict[str, Any]:
    values = [r["rows"][row] for r in per_run]
    med = median_of(values)
    se = None
    if med is not None:
        nearest = min((r for r in per_run if r["rows"][row] is not None),
                      key=lambda r: abs(r["rows"][row] - med))
        se = nearest["standard_errors"][row]
    if row == "F-e":
        is_thin = med == plan.F_E_MIN_ONCALL if med is not None else None
    else:
        is_thin = thin(med, LINES[row], se)
    return {"per_run": values, "median": med, "standard_error_of_the_median_run": se,
            "line": LINES[row], "verdict": VERDICTS[row](med), "thin": is_thin}


def ticket_only_arm(rows: list[dict], bases: dict[int, dict[str, dict]]) -> dict:
    """F-f's paid half: the model without its screen."""
    entries = group(rows)
    sub = [e for e in entries.values() if e["labels"]["sources"]]
    right = agree_rule = agree_b = with_b = 0
    for e in sub:
        a = e["answers"].get(1)
        right += a == e["labels"]["truth"]
        for s in e["labels"]["sources"]:
            agree_rule += a == s["rule_action"]
            b = bases.get(s["run"], {}).get(f"d{s['run']}:{s['idx']}")
            if b is not None and b["answers"].get(1) is not None:
                with_b += 1
                agree_b += a == b["answers"][1]
    sources = sum(len(e["labels"]["sources"]) for e in sub)
    rare = collections.defaultdict(collections.Counter)
    for e in entries.values():
        if e["labels"]["rare"]:
            for a in e["answers"].values():
                rare[e["labels"]["rare"]][str(a)] += 1
    return {"tickets": len(sub),
            "accuracy": right / len(sub) if sub else None,
            "agreement_with_the_rule": agree_rule / sources if sources else None,
            "agreement_with_the_B_answer_on_the_same_case": (agree_b / with_b
                                                             if with_b else None),
            "matched_on_the_same_cases": matched_accuracy(sub, bases),
            "rare_tickets_answers_by_queue": {q: dict(c) for q, c in rare.items()}}


def matched_accuracy(sub: list[dict], bases: dict[int, dict[str, dict]]) -> dict:
    """The model without its screen, with it, and the rule, right on the same
    cases. These are the drawn decisions behind the ticket-only subsample, each
    with a valid first answer in both arms. Added after Stage C first ran
    (POST-RUN): the accuracies above compare a subsample with all 600 drawn,
    and §2.1 built this arm to tell the model from its screen."""
    counts: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for e in sub:
        a, y = e["answers"].get(1), e["labels"]["truth"]
        for s in e["labels"]["sources"]:
            b = bases.get(s["run"], {}).get(f"d{s['run']}:{s['idx']}")
            ab = b["answers"].get(1) if b is not None else None
            if a is None or ab is None:
                continue
            for key in (f"run{s['run']}", "all"):
                c = counts[key]
                c["cases"] += 1
                c["ticket_only_right"] += a == y
                c["B_right"] += ab == y
                c["rule_right"] += s["rule_action"] == y
    return {key: {**dict(c),
                  "ticket_only_accuracy": c["ticket_only_right"] / c["cases"],
                  "B_accuracy": c["B_right"] / c["cases"],
                  "rule_accuracy": c["rule_right"] / c["cases"]}
            for key, c in sorted(counts.items())}


def adjudicate(births_score: dict, per_run: list[dict]) -> dict[str, dict]:
    out = {"F-a": {"value": births_score["value"],
                   "standard_error": births_score["standard_error"],
                   "per_run": births_score["per_run"], "line": LINES["F-a"],
                   "verdict": verdict_f_a(births_score["value"]),
                   "thin": thin(births_score["value"], LINES["F-a"],
                                births_score["standard_error"])}}
    for row in ("F-b", "F-c", "F-d", "F-e"):
        out[row] = median_row(per_run, row)
    return out


# ---------------------------------------------------------------------------

def load_sessions() -> tuple[dict[str, dict], list[str]]:
    found, missing = {}, []
    for s in REQUIRED + ("ticket_only",):
        path = plan.ask_path(s)
        if path.exists():
            found[s] = json.loads(path.read_text())
        elif s in REQUIRED:
            missing.append(str(path))
    return found, missing


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage C of PLAN_FIDELITY.md: the five adjudications.")
    ap.add_argument("--dry-run", action="store_true",
                    help="run the blocking checks and list the records present")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = sample.run_checks(suite=True)
        sample.report(checks)
        found, missing = load_sessions()
        print(f"\n  Stage B records present: {sorted(found)}"
              + (f" — missing {', '.join(missing)}" if missing else ""))
        print("dry run: nothing scored, nothing written")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"fidelity/score.py writes {plan.SCORE_PATH}")
    checks = sample.run_checks(suite=True)
    sample.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    ok, why = ask.sample_matches(checks.design)
    if not ok:
        sys.exit(f"\nREFUSED: {why}.\n")
    found, missing = load_sessions()
    if missing:
        sys.exit(f"\nREFUSED: Stage B is incomplete — missing {', '.join(missing)}\n")
    digest = ask.sample_sha256()
    for name, rec in found.items():
        wrong = {k: rec.get(k) for k, v in ask.protocol().items() if rec.get(k) != v}
        if wrong or rec.get("sample_sha256") != digest:
            sys.exit(f"\nREFUSED: the {name} record was not produced under this "
                     f"protocol and this Stage A record: {wrong or 'sample digest'}\n")

    d = checks.design
    births_score = score_births(found["births"]["rows"])
    per_run = [score_run(k, found[f"base{k}"]["rows"], d.runs[k], d.corpus)
               for k in plan.RUNS]
    verdicts = adjudicate(births_score, per_run)
    for row, v in verdicts.items():
        value = v.get("median", v.get("value"))
        print(f"  {row}  {value}  ->  {v['verdict']}"
              + ("  (thin)" if v["thin"] else ""))
    bases = {k: group(found[f"base{k}"]["rows"]) for k in plan.RUNS}
    stage_a = json.loads(plan.SAMPLE_PATH.read_text())["readout"]
    plan.OUT.mkdir(exist_ok=True)
    plan.SCORE_PATH.write_text(json.dumps({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "stage": "C",
        "surface": ("corpus — seed 17, n=2000, in arrival order: the decided cases "
                    "and births of PLAN_REUSE.md's three Stage B runs"),
        "provenance": "PRE-REGISTERED: §0 signed before any of these figures existed",
        "gates": checks.summary(),
        "sample_sha256": digest,
        "verdicts": verdicts,
        "births": births_score,
        "runs": per_run,
        "F-f": {
            "stage_a_baselines_per_run": {
                name: r["baselines_on_the_draw"] for name, r in stage_a["per_run"].items()},
            "ticket_only": (ticket_only_arm(found["ticket_only"]["rows"], bases)
                            if "ticket_only" in found else None),
        },
        "pace_per_session": {name: run_itself(rec["rows"], d.corpus)["median_seconds_per_call"]
                             for name, rec in found.items()},
    }, indent=2))
    print(f"\n-> {plan.SCORE_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
