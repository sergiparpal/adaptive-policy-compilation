"""
Stage C of `PLAN_FIRST_MATCH.md`: scoring, and the six adjudications. **Free,
and gated.**

It reads Stage A's design, this plan's two passes, `PLAN_QUEUE_ALONE.md`'s two
passes and the loop records, and writes `results_first_match/score.json`:

  * **`FM-a` to `FM-f`**, each against its line exactly, as a fraction, with its
    standard error clustered by ticket, *thin* and *unadjudicable* as §0
    defines them;
  * **each row's parts and per-run values**, never summed into the verdict;
  * **`FM-g` in full**, and the run itself.

THE LABELS ENTER HERE AND NOWHERE ELSE (rule B). `y` is a loop record row's
`truth`, read by `apply.score.labels`. The answers come from the passes' rows,
which carry none. The rules a ticket matches are read from level 3's frozen
text by `queue_alone.rules`, never from the oracle.

THE NOTATION IS §0's. Per decision: `q`, `n` and `r` are the pairs of answers,
pass 1's and pass 2's, of the plain, naming and reasoning arms on the
decision's ticket, and `rho` the pair of rules the naming arm names. An answer
is valid when its `action` is one of the eight queues and the provider that
served it is the pinned one (rule G); an invalid one is `None` here, and so is
the rule of an invalid naming answer or of one that names no rule. A decision
enters a row only with every answer the row reads valid.

`apply/score.py`'s `hits`, `mean`, `frac` and `clustered_se` are called, not
copied (rule A), and `queue_alone/score.py`'s anchor term. The adjudication is
`PLAN_QUEUE_ALONE.md`'s, written again for this plan's rows: a statistic, its
error, its runs and its *thin* label are computed exactly as that plan's were.
`FM-c` reads answers rather than decisions, as §0 says.

    PYTHONHASHSEED=0 python3 -m first_match.score --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m first_match.score
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable

from harness.domain import ACTIONS
from harness.provenance import describe, environment

from apply import score as ascore
from queue_alone import orders as qorders
from queue_alone import rules as qrules
from queue_alone import score as qscore

from . import gates, plan, population, prompts

F = Fraction
hits, mean, frac, clustered_se = ascore.hits, ascore.mean, ascore.frac, ascore.clustered_se
labels = ascore.labels
RARE = ascore.RARE
Pair = tuple  # (pass 1's, pass 2's)


def read(session: str) -> dict[str, Any]:
    return json.loads(plan.ask_path(session).read_text())


def answer(row: dict | None) -> str | None:
    """A row's action if valid under rule G, `None` otherwise or if there is no
    row."""
    if row is None or row.get("action") not in ACTIONS:
        return None
    if row.get("served_by") != plan.PROVIDER_NAME:
        return None
    return row["action"]


def named(row: dict | None) -> str | None:
    """The rule a valid naming-arm answer names, as §0 defines it, or `None`."""
    if answer(row) is None or not isinstance(row.get("payload"), dict):
        return None
    return prompts.named_rule(row["payload"].get("rule"))


def valid(*pairs: Pair) -> bool:
    return all(a is not None for pair in pairs for a in pair)


# ---------------------------------------------------------------------------
# The decisions, with their answers
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Unit:
    id: str
    run: int
    ticket: int
    y: str
    hit: tuple[str, ...]           # the rules the ticket matches, in the list's order
    queues: tuple[str, ...]        # and their queues
    q: Pair
    n: Pair
    rho: Pair
    r: Pair


def units(design: population.Design, by_pass: dict[int, dict[str, dict]],
          lab: dict[str, dict[str, Any]]) -> list[Unit]:
    rs = qrules.rules()
    out = []
    for i, e in sorted(design.decisions.items()):
        hit = qrules.matching(e.prompt.case.as_dict(), rs)

        def rows(arm: str) -> list[dict | None]:
            return [by_pass[k].get(prompts.ask_id(arm, e.ticket)) for k in (1, 2)]
        out.append(Unit(id=i, run=e.run, ticket=e.ticket, y=lab[i]["y"],
                        hit=tuple(r.id for r in hit), queues=tuple(r.queue for r in hit),
                        q=tuple(answer(x) for x in rows(prompts.PLAIN)),
                        n=tuple(answer(x) for x in rows(prompts.NAMING)),
                        rho=tuple(named(x) for x in rows(prompts.NAMING)),
                        r=tuple(answer(x) for x in rows(prompts.REASONING))))
    return out


def h(u: Unit, arm: str) -> Fraction:
    return hits(getattr(u, arm), u.y)


def acc(us: list[Unit], arm: str) -> Fraction | None:
    return mean([h(u, arm) for u in us])


def klass(a: str, u: Unit) -> str:
    """`PLAN_QUEUE_ALONE.md` §5.6's class of an answer, by its queue."""
    if u.queues and a == u.queues[0]:
        return "first"
    if a in u.queues[1:]:
        return "order"
    return "matching"


def rule_class(rho: str | None, u: Unit) -> str:
    """§0's class of a named rule: the first, a lower match, unmatched, or
    none named."""
    if rho is None:
        return "none"
    if u.hit and rho == u.hit[0]:
        return "first"
    if rho in u.hit[1:]:
        return "lower"
    return "unmatched"


# ---------------------------------------------------------------------------
# FM-b, FM-d, FM-e and FM-f, over decisions
# ---------------------------------------------------------------------------

HOLDS: dict[str, Callable[[Fraction, Fraction], bool]] = {
    "le": lambda v, line: v <= line,
    "gt": lambda v, line: v > line,
    "ge": lambda v, line: v >= line,
}


@dataclass(frozen=True)
class Spec:
    id: str
    needs: tuple[str, ...]
    term: Callable[[Unit], Fraction]
    line: Fraction
    rule: str


SPECS = (
    Spec("FM-b", ("n", "q"), lambda u: h(u, "n") - h(u, "q"), plan.FM_B_LINE, "gt"),
    Spec("FM-d", ("r", "q"), lambda u: h(u, "r") - h(u, "q"), plan.FM_D_LINE, "gt"),
    Spec("FM-e", ("r",), lambda u: h(u, "r"), plan.FM_E_LINE, "ge"),
    Spec("FM-f", ("r", "n"), lambda u: h(u, "r") - h(u, "n"), plan.FM_F_LINE, "gt"),
)


def statistic(spec: Spec, us: list[Unit]) -> Fraction | None:
    return mean([spec.term(u) for u in us])


def runs_of(us: list[Unit]) -> list[int]:
    return sorted({u.run for u in us})


def thin(value: Fraction, line: Fraction, rule: str, se: float | None,
         rest: dict[int, Fraction | None]) -> dict[str, Any]:
    """§0's two cases of *thin*: within one standard error of the line, or a run
    whose decisions, dropped, would put the statistic on the other side."""
    holds = HOLDS[rule](value, line)
    flips = [f"L3r{run}" for run, v in sorted(rest.items())
             if v is not None and HOLDS[rule](v, line) != holds]
    within = se is not None and abs(float(value - line)) <= se
    return {"verdict": "holds" if holds else "refuted", "thin": within or bool(flips),
            "thin_because": {"within_one_se": within, "dropping_one_run_flips": flips}}


def adjudicate(spec: Spec, population_: list[Unit]) -> dict[str, Any]:
    kept = [u for u in population_ if valid(*(getattr(u, a) for a in spec.needs))]
    missing = len(population_) - len(kept)
    out: dict[str, Any] = {"id": spec.id, "level": plan.LEVEL,
                           "decisions": len(population_), "missing": missing,
                           "read": len(kept), "line": frac(spec.line), "holds": spec.rule}
    reasons = []
    if not population_ or F(missing, len(population_)) > plan.MAX_INVALID_SHARE:
        reasons.append("more than 5% of its decisions lack the valid answers it reads")
    value = statistic(spec, kept)
    if value is None:
        reasons.append("no decision to read")
    out["value"] = frac(value)
    out["se"] = clustered_se([(u.ticket, spec.term(u)) for u in kept])
    out["per_run"] = {f"L3r{run}": frac(statistic(spec, [u for u in kept if u.run == run]))
                      for run in runs_of(kept)}
    out["parts"] = {f"acc_{arm}": frac(acc(kept, arm)) for arm in spec.needs}
    if reasons:
        out.update({"verdict": "unadjudicable", "why": reasons, "thin": None})
        return out
    rest = {run: statistic(spec, [u for u in kept if u.run != run]) for run in runs_of(kept)}
    out.update(thin(value, spec.line, spec.rule, out["se"], rest))
    return out


# ---------------------------------------------------------------------------
# FM-c, over the naming arm's answers
# ---------------------------------------------------------------------------

def naming_answers(us: list[Unit]) -> list[tuple[Unit, str, str | None]]:
    """Every valid naming-arm answer at the decisions, with the rule it names."""
    return [(u, a, rho) for u in us for a, rho in zip(u.n, u.rho) if a is not None]


def named_order_errors(us: list[Unit]) -> list[tuple[Unit, str, str]]:
    """The naming arm's order errors that name a rule."""
    return [(u, a, rho) for u, a, rho in naming_answers(us)
            if klass(a, u) == "order" and rho is not None]


def lower_share(us: list[Unit]) -> tuple[Fraction | None, int, int]:
    """`FM-c`'s statistic: of the named order errors, the share naming a lower
    match; with its numerator and denominator."""
    errs = named_order_errors(us)
    lower = sum(1 for u, _, rho in errs if rule_class(rho, u) == "lower")
    return (F(lower, len(errs)) if errs else None), lower, len(errs)


def adjudicate_naming(population_: list[Unit]) -> dict[str, Any]:
    kept = [u for u in population_ if valid(u.n)]
    missing = len(population_) - len(kept)
    answers = naming_answers(kept)
    unnamed = sum(1 for _, _, rho in answers if rho is None)
    value, lower, n = lower_share(kept)
    out: dict[str, Any] = {"id": "FM-c", "level": plan.LEVEL,
                           "decisions": len(population_), "missing": missing,
                           "read": len(kept), "answers": len(answers),
                           "unnamed": unnamed, "named_order_errors": n, "lower": lower,
                           "line": frac(plan.FM_C_LINE), "holds": "ge",
                           "compared_as": "2·lower − named against 0"}
    reasons = []
    if not population_ or F(missing, len(population_)) > plan.MAX_INVALID_SHARE:
        reasons.append("more than 5% of its decisions lack the valid answers it reads")
    if not answers or F(unnamed, len(answers)) > plan.MAX_UNNAMED_SHARE:
        reasons.append("more than 5% of the naming arm's valid answers name no rule")
    if n < plan.MIN_NAMED_ORDER_ERRORS:
        reasons.append(f"fewer than {plan.MIN_NAMED_ORDER_ERRORS} of the naming arm's "
                       "order errors name a rule")
    out["value"] = frac(value)
    out["se"] = clustered_se([(u.ticket, F(int(rule_class(rho, u) == "lower")))
                              for u, _, rho in named_order_errors(kept)])
    out["per_run"] = {f"L3r{run}": frac(lower_share([u for u in kept if u.run == run])[0])
                      for run in runs_of(kept)}
    if value is None:
        reasons.append("no named order error to read")
    if reasons:
        out.update({"verdict": "unadjudicable", "why": reasons, "thin": None})
        return out
    rest = {run: lower_share([u for u in kept if u.run != run])[0] for run in runs_of(kept)}
    out.update(thin(value, plan.FM_C_LINE, "ge", out["se"], rest))
    return out


# ---------------------------------------------------------------------------
# FM-a, over the plain arm's prompts
# ---------------------------------------------------------------------------

def anchor_prompts(design: population.Design, by_pass: dict[int, dict[str, dict]],
                   before_by_pass: dict[int, dict[str, dict]]) -> list[qscore.Prompt]:
    """Today's plain answers on each plain prompt, beside `PLAN_QUEUE_ALONE.md`'s
    valid answers from the pinned provider on the same prompt."""
    out = []
    for a in sorted(design.asks_of(prompts.PLAIN), key=lambda a: a.id):
        before = tuple(x for k in (1, 2)
                       if (x := qscore.answer(before_by_pass[k].get(a.id))) is not None)
        out.append(qscore.Prompt(id=a.id, ticket=a.ticket,
                                 today=tuple(answer(by_pass[k].get(a.id)) for k in (1, 2)),
                                 before=before))
    return out


def adjudicate_anchor(ps: list[qscore.Prompt]) -> dict[str, Any]:
    kept = [p for p in ps if valid(p.today) and p.before]
    out: dict[str, Any] = {"id": "FM-a", "prompts": len(ps), "read": len(kept),
                           "line": frac(plan.FM_A_MAX_GAP), "holds": "le"}
    value = mean([qscore.anchor_term(p) for p in kept])
    out["value"] = frac(value)
    out["se"] = clustered_se([(p.ticket, qscore.anchor_term(p)) for p in kept])
    out["parts"] = {
        "S": frac(mean([F(int(p.today[0] == p.today[1])) for p in kept])),
        "A": frac(mean([F(sum(int(x == b) for x in p.today for b in p.before),
                          2 * len(p.before)) for p in kept]))}
    if len(kept) < plan.MIN_ANCHOR_PROMPTS or value is None:
        out.update({"verdict": "unadjudicable", "thin": None,
                    "why": [f"fewer than {plan.MIN_ANCHOR_PROMPTS} prompts hold today's "
                            "two answers valid and one of PLAN_QUEUE_ALONE.md's from the "
                            "pinned provider"]})
        return out
    holds = value <= plan.FM_A_MAX_GAP
    # §0: FM-a reads prompts and not runs, so only the first case of thin applies.
    within = out["se"] is not None and abs(float(value - plan.FM_A_MAX_GAP)) <= out["se"]
    out.update({"verdict": "holds" if holds else "refuted", "thin": within,
                "thin_because": {"within_one_se": within}})
    return out


# ---------------------------------------------------------------------------
# FM-g, reported
# ---------------------------------------------------------------------------

ARMS = ("q", "n", "r")


def accuracy(us: list[Unit]) -> dict[str, Any]:
    """Each arm on the decisions where its own two answers are valid, with its
    runs, and by ticket with every ticket counted once."""
    out: dict[str, Any] = {}
    for arm in ARMS:
        kept = [u for u in us if valid(getattr(u, arm))]
        seen: dict[int, Fraction] = {}
        for u in kept:
            seen.setdefault(u.ticket, h(u, arm))
        out[arm] = {"decisions": len(kept), "acc": frac(acc(kept, arm)),
                    "per_run": {f"L3r{run}": frac(acc([u for u in kept if u.run == run], arm))
                                for run in runs_of(kept)},
                    "by_ticket": {"tickets": len(seen), "acc": frac(mean(list(seen.values())))}}
    return out


def where_errors_go(design: population.Design, us: list[Unit]) -> dict[str, Any]:
    """Every answer in §5.6's classes, and each arm's order errors by where they
    go, with `PLAN_QUEUE_ALONE.md`'s reading called (`queue_alone/orders.py`)."""
    rs = qrules.rules()
    out: dict[str, Any] = {}
    for arm in ARMS:
        triples = [(a, design.decisions[u.id].prompt.case.as_dict(), u.y)
                   for u in us for a in getattr(u, arm) if a is not None]
        reading = qorders.arm_reading(triples, rs)
        out[arm] = {**reading,
                    "second_matching_rule": sum(
                        1 for u in us for a in getattr(u, arm)
                        if a is not None and klass(a, u) == "order" and len(u.queues) > 1
                        and a == u.queues[1]),
                    "specificity": qorders.specificity(triples, rs)}
    return out


def naming(us: list[Unit], rows: list[dict]) -> dict[str, Any]:
    """The naming arm's named rules: their classes over all its answers and over
    its order errors, whether its queue is the named rule's, whether a lower
    name is the next matching rule, and whether `rule` came first."""
    answers = naming_answers(us)
    over_all = Counter(rule_class(rho, u) for u, _, rho in answers)
    errors = [(u, a, rho) for u, a, rho in answers if klass(a, u) == "order"]
    over_errors = Counter(rule_class(rho, u) for u, _, rho in errors)
    queue_of = {r.id: r.queue for r in qrules.rules()}
    named_ = [(u, a, rho) for u, a, rho in answers if rho is not None]
    consistent = sum(1 for _, a, rho in named_ if a == queue_of[rho])
    lower = [(u, rho) for u, _, rho in named_ if rule_class(rho, u) == "lower"]
    next_rule = sum(1 for u, rho in lower if rho == u.hit[1])
    by_answer_class: dict[str, Counter] = defaultdict(Counter)
    for u, a, rho in answers:
        by_answer_class[klass(a, u)][rule_class(rho, u)] += 1
    named_on_errors = Counter(rho for _, _, rho in errors if rho is not None)
    valid_rows = [r for r in rows if r.get("arm") == prompts.NAMING and answer(r) is not None]
    rule_first = sum(1 for r in valid_rows if (r.get("keys") or [None])[0] == "rule")
    return {"answers": len(answers), "classes": dict(over_all),
            "order_errors": len(errors), "classes_over_order_errors": dict(over_errors),
            "by_answer_class": {k: dict(v) for k, v in sorted(by_answer_class.items())},
            "named": len(named_), "queue_is_the_named_rules": consistent,
            "lower_names": len(lower), "lower_name_is_the_next_matching_rule": next_rule,
            "rules_named_on_order_errors": dict(named_on_errors.most_common()),
            "valid_rows": len(valid_rows), "rule_written_first": rule_first}


def paired(us: list[Unit]) -> dict[str, Any]:
    """On each pass's order errors of today's plain arm, what the naming arm
    names on the same ticket in the same pass."""
    queue_of = {r.id: r.queue for r in qrules.rules()}
    c: Counter = Counter()
    for u in us:
        for q_, rho, n_ in zip(u.q, u.rho, u.n):
            if q_ is None or klass(q_, u) != "order":
                continue
            c["plain_order_errors"] += 1
            if n_ is None:
                c["naming_invalid"] += 1
            elif rho is None:
                c["names_no_rule"] += 1
            elif rho == u.hit[0]:
                c["names_the_first"] += 1
            elif rho in u.hit[1:] and queue_of[rho] == q_:
                c["names_the_rule_the_plain_arm_followed"] += 1
            elif rho in u.hit[1:]:
                c["names_another_lower_match"] += 1
            else:
                c["names_an_unmatched_rule"] += 1
    return dict(c)


def by_governing(us: list[Unit]) -> dict[str, Any]:
    """Each arm's right answers by the rule that governs the ticket, `m₁`."""
    out: dict[str, Counter] = defaultdict(Counter)
    for u in us:
        g = u.hit[0] if u.hit else None
        c = out[g]
        c["decisions"] += 1
        for arm in ARMS:
            pair = getattr(u, arm)
            c[f"{arm}_answers"] += sum(1 for a in pair if a is not None)
            c[f"{arm}_right"] += sum(1 for a in pair if a is not None and a == u.y)
    return {g: dict(c) for g, c in sorted(out.items(), key=lambda kv: str(kv[0]))}


def by_queue(us: list[Unit]) -> dict[str, Any]:
    """Counts, so that the rare queues read as counts (§0)."""
    rows: dict[str, Counter] = defaultdict(Counter)
    for u in us:
        c = rows[u.y]
        c["decisions"] += 1
        for arm in ARMS:
            pair = getattr(u, arm)
            c[f"{arm}_answers"] += sum(1 for a in pair if a is not None)
            c[f"{arm}_right"] += sum(1 for a in pair if a is not None and a == u.y)
    return {"by_true_queue": {q: dict(c) for q, c in sorted(rows.items())}, "rare": list(RARE)}


def agreement(us: list[Unit]) -> dict[str, Any]:
    """`S` for each arm, and how often two arms answer alike."""
    cell: dict[str, Any] = {}
    for arm in ARMS:
        kept = [u for u in us if valid(getattr(u, arm))]
        cell[f"S_{arm}"] = frac(mean([F(int(getattr(u, arm)[0] == getattr(u, arm)[1]))
                                      for u in kept]))
    for a, b in (("q", "n"), ("q", "r"), ("n", "r")):
        kept = [u for u in us if valid(getattr(u, a), getattr(u, b))]
        cell[f"{a}_{b}"] = frac(mean([F(sum(int(x == z) for x in getattr(u, a)
                                            for z in getattr(u, b)), 4) for u in kept]))
    return cell


def queue_alone_beside(us: list[Unit], before_by_pass: dict[int, dict[str, dict]]
                       ) -> dict[str, Any]:
    """`PLAN_QUEUE_ALONE.md`'s plain arm on the same decisions, valid and from the
    pinned provider, beside today's."""
    def before(u: Unit) -> Pair:
        aid = prompts.ask_id(prompts.PLAIN, u.ticket)
        return tuple(qscore.answer(before_by_pass[k].get(aid)) for k in (1, 2))
    kept = [u for u in us if valid(before(u))]
    return {"decisions": len(kept), "acc_queue_alone": frac(mean([hits(before(u), u.y)
                                                                  for u in kept])),
            "acc_today_on_the_same": frac(mean([h(u, "q") for u in kept if valid(u.q)]))}


def the_calls(recs: dict[str, dict]) -> dict[str, Any]:
    out = {}
    for session, rec in recs.items():
        rows = rec["rows"]
        per_arm: dict[str, dict[str, Any]] = defaultdict(lambda: defaultdict(Counter))
        seconds: dict[str, list[float]] = defaultdict(list)
        reasoning_tokens: dict[str, list[int]] = defaultdict(list)
        for r in rows:
            arm = r["arm"]
            seconds[arm].append(r.get("seconds") or 0.0)
            for cause in r.get("retries") or []:
                per_arm[arm]["retries"][cause] += 1
            for att in r.get("call_attempts") or []:
                per_arm[arm]["providers"][att.get("provider")] += 1
                per_arm[arm]["finish_reasons"][att.get("finish_reason")] += 1
                per_arm[arm]["tokens"]["prompt"] += att.get("prompt_tokens") or 0
                per_arm[arm]["tokens"]["completion"] += att.get("completion_tokens") or 0
                per_arm[arm]["tokens"]["reasoning"] += att.get("reasoning_tokens") or 0
                if att.get("reasoning_tokens") is not None:
                    reasoning_tokens[arm].append(att["reasoning_tokens"])
        out[session] = {
            "answers": len(rows), "valid": sum(1 for r in rows if answer(r) is not None),
            "invalid_action": sum(1 for r in rows if r.get("failure") is None
                                  and r.get("action") not in ACTIONS),
            "served_elsewhere": sum(1 for r in rows if r.get("served_by")
                                    not in (None, plan.PROVIDER_NAME)),
            "failed": sum(1 for r in rows if r.get("failure") is not None),
            "retried": sum(1 for r in rows if (r.get("attempts") or 0) > 1),
            "started_at": rec.get("started_at"), "finished_at": rec.get("finished_at"),
            "by_arm": {arm: {k: dict(v) for k, v in d.items()} for arm, d in per_arm.items()},
            "seconds": {arm: {"asks": len(v), "total": round(sum(v), 1),
                              "median": statistics.median(v) if v else None}
                        for arm, v in sorted(seconds.items())},
            "reasoning_tokens": {arm: {"attempts": len(v), "min": min(v) if v else None,
                                       "median": statistics.median(v) if v else None,
                                       "max": max(v) if v else None}
                                 for arm, v in sorted(reasoning_tokens.items())},
            "reasoning": {"recorded": sum(1 for r in rows if r.get("reasoning")),
                          "coded": False},
        }
    return out


# ---------------------------------------------------------------------------
# Stage C
# ---------------------------------------------------------------------------

def score(design: population.Design, recs: dict[str, dict],
          lab: dict[str, dict[str, Any]],
          before_by_pass: dict[int, dict[str, dict]]) -> dict[str, Any]:
    by_pass = {plan.pass_of(s): {r["id"]: r for r in rec["rows"]} for s, rec in recs.items()
               if s != "smoke"}
    us = units(design, by_pass, lab)
    verdicts: dict[str, Any] = {
        "FM-a": adjudicate_anchor(anchor_prompts(design, by_pass, before_by_pass))}
    for spec in SPECS[:1]:
        verdicts[spec.id] = adjudicate(spec, us)
    verdicts["FM-c"] = adjudicate_naming(us)
    for spec in SPECS[1:]:
        verdicts[spec.id] = adjudicate(spec, us)
    rows = [r for s, rec in recs.items() if s != "smoke" for r in rec["rows"]]
    fm_g = {"accuracy": accuracy(us),
            "where_errors_go": where_errors_go(design, us),
            "naming": naming(us, rows),
            "paired": paired(us),
            "by_governing_rule": by_governing(us),
            "by_true_queue": by_queue(us),
            "agreement": agreement(us),
            "queue_alone_beside": queue_alone_beside(us, before_by_pass),
            "the_calls": the_calls(recs)}
    return {"verdicts": verdicts, "FM-g": fm_g}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage C of PLAN_FIRST_MATCH.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run FM-g1 to FM-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1
    gate = plan.refuse_unsigned("first_match/score.py writes Stage C")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    missing = [s for s in plan.SESSIONS[1:] if not plan.ask_path(s).exists()]
    if missing:
        sys.exit(f"\nREFUSED: no record of {missing}; Stage C reads both passes. "
                 "Nothing was written.\n")
    recs = {s: read(s) for s in plan.SESSIONS[1:]}
    out = score(checks.design, recs, labels(), gates.queue_alone_passes())
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "C",
              "signature": gate, "gates": checks.summary(),
              "lines": {"FM-a": frac(plan.FM_A_MAX_GAP), "FM-b": frac(plan.FM_B_LINE),
                        "FM-c": frac(plan.FM_C_LINE), "FM-d": frac(plan.FM_D_LINE),
                        "FM-e": frac(plan.FM_E_LINE), "FM-f": frac(plan.FM_F_LINE)},
              **out}
    plan.score_path().parent.mkdir(parents=True, exist_ok=True)
    plan.score_path().write_text(json.dumps(record, indent=2, default=str))
    for rid, v in out["verdicts"].items():
        val = v["value"]["value"] if v.get("value") else None
        print(f"  {rid}: {v['verdict']}{', thin' if v.get('thin') else ''} "
              f"({val if val is None else round(val, 4)}, se {v.get('se')})")
    print(f"\n-> {plan.score_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
