"""
Stage C of `PLAN_REASONED_RULE.md`: scoring, and the four adjudications. **Free,
and gated.**

It reads Stage A's design, this plan's two passes, `PLAN_QUEUE_ALONE.md`'s and
`PLAN_FIRST_MATCH.md`'s two passes and the loop records, and writes
`results_reasoned_rule/score.json`:

  * **`RR-a` to `RR-d`**, each against its line exactly, as a fraction, with its
    standard error clustered by ticket, *thin* and *unadjudicable* as §0
    defines them;
  * **each row's parts and per-run values**, never summed into the verdict;
  * **`RR-e` in full**, the rules the two rule arms write included, and the run
    itself.

THE LABELS ENTER HERE AND NOWHERE ELSE (rule B). `y` is a loop record row's
`truth`, read by `apply.score.labels`. The answers come from the passes' rows,
which carry none. The rules a ticket matches are read from level 3's frozen
text by `queue_alone.rules`, never from the oracle, and so is the list's first
match over the space that `RR-e` reads the rules written against
(`reasoned_rule/shape.py`).

THE NOTATION IS §0's. Per decision: `t`, `w`, `q` and `r` are the pairs of
answers, pass 1's and pass 2's, of the rule, reasoning rule, plain and
reasoning arms on the decision's ticket. An answer is valid when its `action`
is one of the eight queues and the provider that served it is the pinned one
(rule G); an invalid one is `None` here. A decision enters a row only with
every answer the row reads valid.

`apply/score.py`'s `hits`, `mean`, `frac` and `clustered_se` are called, not
copied (rule A), and `queue_alone/score.py`'s anchor term. The adjudication is
`PLAN_FIRST_MATCH.md`'s, written again for this plan's rows: a statistic, its
error, its runs and its *thin* label are computed exactly as that plan's were.
`RR-d` is held below its line, and has no value where §0 says.

    PYTHONHASHSEED=0 python3 -m reasoned_rule.score --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m reasoned_rule.score
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
from first_match import gates as fmgates
from first_match import score as fmscore
from queue_alone import orders as qorders
from queue_alone import rules as qrules
from queue_alone import score as qscore

from . import gates, plan, population, prompts, shape

F = Fraction
hits, mean, frac, clustered_se = ascore.hits, ascore.mean, ascore.frac, ascore.clustered_se
labels = ascore.labels
RARE = ascore.RARE
ARMS = prompts.ARMS
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
    t: Pair
    w: Pair
    q: Pair
    r: Pair


def units(design: population.Design, by_pass: dict[int, dict[str, dict]],
          lab: dict[str, dict[str, Any]]) -> list[Unit]:
    rs = qrules.rules()
    out = []
    for i, e in sorted(design.decisions.items()):
        hit = qrules.matching(e.prompt.case.as_dict(), rs)

        def pair(arm: str) -> Pair:
            return tuple(answer(by_pass[k].get(prompts.ask_id(arm, e.ticket)))
                         for k in (1, 2))
        out.append(Unit(id=i, run=e.run, ticket=e.ticket, y=lab[i]["y"],
                        hit=tuple(r.id for r in hit), queues=tuple(r.queue for r in hit),
                        t=pair(prompts.RULE), w=pair(prompts.REASONING_RULE),
                        q=pair(prompts.PLAIN), r=pair(prompts.REASONING)))
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


# ---------------------------------------------------------------------------
# RR-b, RR-c and RR-d, over decisions
# ---------------------------------------------------------------------------

HOLDS: dict[str, Callable[[Fraction, Fraction], bool]] = {
    "le": lambda v, line: v <= line,
    "lt": lambda v, line: v < line,
    "gt": lambda v, line: v > line,
    "ge": lambda v, line: v >= line,
}


def no_cost_to_shrink(us: list[Unit]) -> str | None:
    """§0: `RR-d` has no value if `acc_q − acc_t ≤ 0` on its decisions."""
    if acc(us, "q") - acc(us, "t") <= 0:
        return ("without reasoning, asking for a rule costs the queue nothing "
                "(acc_q − acc_t ≤ 0): there is no cost for reasoning to shrink")
    return None


@dataclass(frozen=True)
class Spec:
    id: str
    needs: tuple[str, ...]
    term: Callable[[Unit], Fraction]
    line: Fraction
    rule: str
    no_value: Callable[[list[Unit]], str | None] | None = None


SPECS = (
    Spec("RR-b", ("w", "t"), lambda u: h(u, "w") - h(u, "t"), plan.RR_B_LINE, "gt"),
    Spec("RR-c", ("w",), lambda u: h(u, "w"), plan.RR_C_LINE, "ge"),
    Spec("RR-d", ("r", "w", "q", "t"),
         lambda u: (h(u, "r") - h(u, "w")) - (h(u, "q") - h(u, "t")),
         plan.RR_D_LINE, "lt", no_cost_to_shrink),
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
    elif spec.no_value is not None and (why := spec.no_value(kept)):
        reasons.append(why)
    out["value"] = frac(value)
    out["se"] = clustered_se([(u.ticket, spec.term(u)) for u in kept])
    out["per_run"] = {f"L3r{run}": frac(statistic(spec, [u for u in kept if u.run == run]))
                      for run in runs_of(kept)}
    out["parts"] = {f"acc_{arm}": frac(acc(kept, arm)) for arm in spec.needs}
    if spec.id == "RR-d" and kept:
        out["parts"]["cost_without_reasoning"] = frac(acc(kept, "q") - acc(kept, "t"))
        out["parts"]["cost_with_reasoning"] = frac(acc(kept, "r") - acc(kept, "w"))
    if reasons:
        out.update({"verdict": "unadjudicable", "why": reasons, "thin": None})
        return out
    rest = {run: statistic(spec, [u for u in kept if u.run != run]) for run in runs_of(kept)}
    out.update(thin(value, spec.line, spec.rule, out["se"], rest))
    return out


# ---------------------------------------------------------------------------
# RR-a, over the rule arm's prompts
# ---------------------------------------------------------------------------

def anchor_prompts(design: population.Design, by_pass: dict[int, dict[str, dict]],
                   before_by_pass: dict[int, dict[str, dict]]) -> list[qscore.Prompt]:
    """Today's rule-arm answers on each rule prompt, beside `PLAN_QUEUE_ALONE.md`'s
    valid answers from the pinned provider on the same prompt."""
    out = []
    for a in sorted(design.asks_of(prompts.RULE), key=lambda a: a.id):
        before = tuple(x for k in (1, 2)
                       if (x := qscore.answer(before_by_pass[k].get(a.id))) is not None)
        out.append(qscore.Prompt(id=a.id, ticket=a.ticket,
                                 today=tuple(answer(by_pass[k].get(a.id)) for k in (1, 2)),
                                 before=before))
    return out


def adjudicate_anchor(ps: list[qscore.Prompt]) -> dict[str, Any]:
    kept = [p for p in ps if valid(p.today) and p.before]
    out: dict[str, Any] = {"id": "RR-a", "prompts": len(ps), "read": len(kept),
                           "line": frac(plan.RR_A_MAX_GAP), "holds": "le"}
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
    holds = value <= plan.RR_A_MAX_GAP
    # §0: RR-a reads prompts and not runs, so only the first case of thin applies.
    within = out["se"] is not None and abs(float(value - plan.RR_A_MAX_GAP)) <= out["se"]
    out.update({"verdict": "holds" if holds else "refuted", "thin": within,
                "thin_because": {"within_one_se": within}})
    return out


# ---------------------------------------------------------------------------
# RR-e, reported
# ---------------------------------------------------------------------------

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


PAIRS = (("t", "w"), ("q", "r"), ("t", "q"), ("w", "r"), ("t", "r"), ("w", "q"))


def agreement(us: list[Unit]) -> dict[str, Any]:
    """`S` for each arm, and how often two arms answer alike."""
    cell: dict[str, Any] = {}
    for arm in ARMS:
        kept = [u for u in us if valid(getattr(u, arm))]
        cell[f"S_{arm}"] = frac(mean([F(int(getattr(u, arm)[0] == getattr(u, arm)[1]))
                                      for u in kept]))
    for a, b in PAIRS:
        kept = [u for u in us if valid(getattr(u, a), getattr(u, b))]
        cell[f"{a}_{b}"] = frac(mean([F(sum(int(x == z) for x in getattr(u, a)
                                            for z in getattr(u, b)), 4) for u in kept]))
    return cell


def beside(us: list[Unit], qa_by_pass: dict[int, dict[str, dict]],
           fm_by_pass: dict[int, dict[str, dict]]) -> dict[str, Any]:
    """`PLAN_QUEUE_ALONE.md`'s rule arm, and `PLAN_FIRST_MATCH.md`'s plain and
    reasoning arms, each on the same decisions as today's, valid and from the
    pinned provider. Two other dates: reported, never adjudicated (§5.13)."""
    cells = (("queue_alone_rule_arm", prompts.RULE, qa_by_pass, qscore.answer),
             ("first_match_plain_arm", prompts.PLAIN, fm_by_pass, fmscore.answer),
             ("first_match_reasoning_arm", prompts.REASONING, fm_by_pass, fmscore.answer))
    out: dict[str, Any] = {}
    for name, arm, by_pass, reader in cells:
        kept = []
        for u in us:
            then = tuple(reader(by_pass[k].get(prompts.ask_id(arm, u.ticket))) for k in (1, 2))
            if valid(then):
                kept.append((u, then))
        out[name] = {"decisions": len(kept),
                     "acc_then": frac(mean([hits(then, u.y) for u, then in kept])),
                     "acc_today_on_the_same": frac(mean([h(u, arm) for u, _ in kept
                                                         if valid(getattr(u, arm))]))}
    return out


def rules_written(design: population.Design, by_pass: dict[int, dict[str, dict]]
                  ) -> dict[str, Any]:
    """The rule beside every valid answer of the two rule arms, on every rule
    prompt and in both passes, read by `reasoned_rule/shape.py`; and how often
    the answer wrote `action` first. Reported; no rule is installed (rule E)."""
    out: dict[str, Any] = {}
    for arm in prompts.RULE_ARMS:
        readings, first = [], 0
        for a in sorted(design.asks_of(arm), key=lambda a: a.id):
            for k in (1, 2):
                row = by_pass[k].get(a.id)
                if answer(row) is None:
                    continue
                readings.append(shape.read(row.get("payload"), a.case))
                first += int((row.get("keys") or [None])[0] == "action")
        out[arm] = {**shape.summary(readings), "action_written_first": first}
    return out


def spread(xs: list[int]) -> dict[str, Any]:
    return {"n": len(xs), "min": min(xs) if xs else None,
            "median": statistics.median(xs) if xs else None, "max": max(xs) if xs else None}


def the_calls(recs: dict[str, dict]) -> dict[str, Any]:
    out = {}
    for session, rec in recs.items():
        rows = rec["rows"]
        per_arm: dict[str, dict[str, Any]] = defaultdict(lambda: defaultdict(Counter))
        seconds: dict[str, list[float]] = defaultdict(list)
        completion: dict[str, list[int]] = defaultdict(list)
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
                if att.get("completion_tokens") is not None:
                    completion[arm].append(att["completion_tokens"])
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
            "completion_tokens": {arm: spread(v) for arm, v in sorted(completion.items())},
            "reasoning_tokens": {arm: spread(v) for arm, v in sorted(reasoning_tokens.items())},
            "reasoning": {"recorded": sum(1 for r in rows if r.get("reasoning")),
                          "coded": False},
        }
    return out


# ---------------------------------------------------------------------------
# Stage C
# ---------------------------------------------------------------------------

def score(design: population.Design, recs: dict[str, dict],
          lab: dict[str, dict[str, Any]],
          qa_by_pass: dict[int, dict[str, dict]],
          fm_by_pass: dict[int, dict[str, dict]]) -> dict[str, Any]:
    by_pass = {plan.pass_of(s): {r["id"]: r for r in rec["rows"]} for s, rec in recs.items()
               if s != "smoke"}
    us = units(design, by_pass, lab)
    verdicts: dict[str, Any] = {
        "RR-a": adjudicate_anchor(anchor_prompts(design, by_pass, qa_by_pass))}
    for spec in SPECS:
        verdicts[spec.id] = adjudicate(spec, us)
    rr_e = {"accuracy": accuracy(us),
            "where_errors_go": where_errors_go(design, us),
            "by_governing_rule": by_governing(us),
            "by_true_queue": by_queue(us),
            "agreement": agreement(us),
            "beside": beside(us, qa_by_pass, fm_by_pass),
            "rules_written": rules_written(design, by_pass),
            "the_calls": the_calls(recs)}
    return {"verdicts": verdicts, "RR-e": rr_e}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage C of PLAN_REASONED_RULE.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run RR-g1 to RR-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1
    gate = plan.refuse_unsigned("reasoned_rule/score.py writes Stage C")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    missing = [s for s in plan.SESSIONS[1:] if not plan.ask_path(s).exists()]
    if missing:
        sys.exit(f"\nREFUSED: no record of {missing}; Stage C reads both passes. "
                 "Nothing was written.\n")
    recs = {s: read(s) for s in plan.SESSIONS[1:]}
    out = score(checks.design, recs, labels(), fmgates.queue_alone_passes(),
                gates.first_match_passes())
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "C",
              "signature": gate, "gates": checks.summary(),
              "lines": {"RR-a": frac(plan.RR_A_MAX_GAP), "RR-b": frac(plan.RR_B_LINE),
                        "RR-c": frac(plan.RR_C_LINE), "RR-d": frac(plan.RR_D_LINE)},
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
