"""
Stage C of `PLAN_QUEUE_ALONE.md`: scoring, and the six adjudications. **Free,
and gated.**

It reads Stage A's design, this plan's two passes, `PLAN_APPLY.md`'s two passes
and the twelve loop records, and writes `results_queue_alone/score.json`:

  * **`QA-a` to `QA-f`**, each against its line exactly, as a fraction, with its
    standard error clustered by ticket, *thin* and *unadjudicable* as §0
    defines them;
  * **each row's parts and per-run values**, never summed into the verdict;
  * **`QA-g` in full**, §5.6's classes among it, and the run itself.

THE LABELS ENTER HERE AND NOWHERE ELSE (rule B). `y` is a loop record row's
`truth`, read by `apply.score.labels`. The answers come from the passes' rows,
which carry none.

THE NOTATION IS §0's. Per decision at level `k`: `t`, `i` and `q` are the pairs
of answers, pass 1's and pass 2's, of the rule, impasse and plain arms at level
`k` on the decision's ticket; `t0`, `i0` and `q0` the same at level 0. An answer
is valid when its `action` is one of the eight queues and the provider that
served it is the pinned one (rule G); an invalid one is `None` here. A decision
enters a row only with every answer the row reads valid.

`apply/score.py`'s `hits`, `mean`, `frac` and `clustered_se` are called, not
copied (rule A). The adjudication is that module's, written again for this
plan's units: a row's statistic, its error, its runs and its *thin* label are
computed exactly as `PLAN_APPLY.md`'s were.

    PYTHONHASHSEED=0 python3 -m queue_alone.score --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m queue_alone.score
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable

from harness.domain import ACTIONS
from harness.provenance import describe, environment

from apply import score as ascore

from . import gates, plan, population, prompts, rules

F = Fraction
hits, mean, frac, clustered_se = ascore.hits, ascore.mean, ascore.frac, ascore.clustered_se
labels = ascore.labels
RARE = ascore.RARE
PAIRS = ("t", "i", "q", "t0", "i0", "q0")


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


def valid(*pairs: tuple[str | None, str | None]) -> bool:
    return all(a is not None for pair in pairs for a in pair)


# ---------------------------------------------------------------------------
# The decisions, with their answers
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Unit:
    id: str
    level: int
    run: int
    ticket: int
    y: str
    t: tuple[str | None, str | None]
    i: tuple[str | None, str | None]
    q: tuple[str | None, str | None]
    t0: tuple[str | None, str | None]
    i0: tuple[str | None, str | None]
    q0: tuple[str | None, str | None]


def units(design: population.Design, by_pass: dict[int, dict[str, dict]],
          lab: dict[str, dict[str, Any]]) -> list[Unit]:
    out = []
    for i, e in sorted(design.decisions.items()):
        def pair(arm: str, level: int) -> tuple[str | None, str | None]:
            aid = prompts.ask_id(arm, level, e.ticket)
            return tuple(answer(by_pass[k].get(aid)) for k in (1, 2))
        out.append(Unit(id=i, level=e.level, run=e.run, ticket=e.ticket, y=lab[i]["y"],
                        t=pair(prompts.RULE, e.level), i=pair(prompts.IMPASSE, e.level),
                        q=pair(prompts.PLAIN, e.level), t0=pair(prompts.RULE, 0),
                        i0=pair(prompts.IMPASSE, 0), q0=pair(prompts.PLAIN, 0)))
    return out


def acc(us: list[Unit], arm: str) -> Fraction | None:
    return mean([hits(getattr(u, arm), u.y) for u in us])


# ---------------------------------------------------------------------------
# QA-b to QA-f
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
    offset: Fraction = F(0)        # the statistic is the mean of the terms plus this
    level: int = 3


def h(u: Unit, arm: str) -> Fraction:
    return hits(getattr(u, arm), u.y)


SPECS = (
    Spec("QA-b", ("q", "t"), lambda u: h(u, "q") - h(u, "t"), plan.QA_B_LINE, "gt"),
    Spec("QA-c", ("q", "t"), lambda u: 2 * h(u, "q") - h(u, "t"), F(0), "ge",
         offset=F(-1)),
    Spec("QA-d", ("q", "i", "t"), lambda u: h(u, "q") - 2 * h(u, "i") + h(u, "t"),
         plan.QA_D_LINE, "ge"),
    Spec("QA-e", ("q",), lambda u: h(u, "q"), plan.QA_E_LINE, "ge"),
    Spec("QA-f", ("q", "t", "q0", "t0"),
         lambda u: (h(u, "q") - h(u, "t")) - (h(u, "q0") - h(u, "t0")), plan.QA_F_LINE,
         "gt"),
)


def statistic(spec: Spec, us: list[Unit]) -> Fraction | None:
    m = mean([spec.term(u) for u in us])
    return None if m is None else m + spec.offset


def share(us: list[Unit]) -> Fraction | None:
    """`(acc_q − acc_t) / (1 − acc_t)`, what `QA-c` publishes beside the
    comparison it decides by."""
    a_q, a_t = acc(us, "q"), acc(us, "t")
    if a_q is None or a_t is None or a_t == 1:
        return None
    return (a_q - a_t) / (1 - a_t)


def parts(spec: Spec, us: list[Unit]) -> dict[str, Any]:
    """The accuracies a row is made of, side by side."""
    return {f"acc_{arm}": frac(acc(us, arm)) for arm in spec.needs}


def adjudicate(spec: Spec, all_units: list[Unit]) -> dict[str, Any]:
    population_ = [u for u in all_units if u.level == spec.level]
    kept = [u for u in population_ if valid(*(getattr(u, a) for a in spec.needs))]
    missing = len(population_) - len(kept)
    out: dict[str, Any] = {"id": spec.id, "level": spec.level,
                           "decisions": len(population_), "missing": missing,
                           "read": len(kept), "line": frac(spec.line), "holds": spec.rule}
    reasons = []
    if not population_ or F(missing, len(population_)) > plan.MAX_INVALID_SHARE:
        reasons.append("more than 5% of its decisions lack the valid answers it reads")
    if spec.id == "QA-c":
        # §0: the line is the share's, 1/2, and the row is decided by the same
        # comparison written without the division.
        out["line"] = frac(plan.QA_C_LINE)
        out["share"] = frac(share(kept))
        out["compared_as"] = "2·acc_q − acc_t − 1 against 0"
        if kept and acc(kept, "t") == 1:
            reasons.append("acc_t is 1")
    if spec.id == "QA-d":
        gain = mean([h(u, "q") - h(u, "t") for u in kept])
        out["gain"] = frac(gain)
        if gain is None or gain <= 0:
            reasons.append("acc_q − acc_t ≤ 0: there is no gain to apportion")
    value = statistic(spec, kept)
    if value is None:
        reasons.append("no decision to read")
    out["value"] = frac(value)
    out["se"] = clustered_se([(u.ticket, spec.term(u)) for u in kept])
    runs = sorted({(u.level, u.run) for u in kept})
    out["per_run"] = {f"L{lv}r{r}": frac(statistic(spec, [u for u in kept
                                                         if (u.level, u.run) == (lv, r)]))
                      for lv, r in runs}
    out["parts"] = parts(spec, kept)
    if reasons:
        out.update({"verdict": "unadjudicable", "why": reasons, "thin": None})
        return out
    holds = HOLDS[spec.rule](value, spec.line)
    flips = []
    for key in runs:
        rest = statistic(spec, [u for u in kept if (u.level, u.run) != key])
        if rest is not None and HOLDS[spec.rule](rest, spec.line) != holds:
            flips.append(f"L{key[0]}r{key[1]}")
    within = out["se"] is not None and abs(float(value - spec.line)) <= out["se"]
    out.update({"verdict": "holds" if holds else "refuted",
                "thin": within or bool(flips),
                "thin_because": {"within_one_se": within, "dropping_one_run_flips": flips}})
    return out


# ---------------------------------------------------------------------------
# QA-a, over the rule arm's prompts
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Prompt:
    id: str
    ticket: int
    today: tuple[str | None, str | None]
    before: tuple[str, ...]        # PLAN_APPLY.md's valid answers from the pinned provider


def apply_answer(row: dict | None) -> str | None:
    """A `PLAN_APPLY.md` answer, valid and served by the pinned provider."""
    if row is None or row.get("action") not in ACTIONS:
        return None
    attempts = row.get("call_attempts") or []
    if not attempts or attempts[-1].get("provider") != plan.PROVIDER_NAME:
        return None
    return row["action"]


def anchor_prompts(design: population.Design, by_pass: dict[int, dict[str, dict]],
                   apply_by_pass: dict[int, dict[str, dict]]) -> list[Prompt]:
    out = []
    for aid, a in sorted(design.asks.items()):
        if a.arm != prompts.RULE:
            continue
        before = tuple(x for k in (1, 2)
                       if (x := apply_answer(apply_by_pass[k].get(aid))) is not None)
        out.append(Prompt(id=aid, ticket=a.ticket,
                          today=tuple(answer(by_pass[k].get(aid)) for k in (1, 2)),
                          before=before))
    return out


def anchor_term(p: Prompt) -> Fraction:
    """`S − A` for one prompt: whether today's two answers agree, less their
    mean agreement with `PLAN_APPLY.md`'s answers from the pinned provider."""
    s = F(int(p.today[0] == p.today[1]))
    a = F(sum(int(x == b) for x in p.today for b in p.before), 2 * len(p.before))
    return s - a


def adjudicate_anchor(ps: list[Prompt]) -> dict[str, Any]:
    kept = [p for p in ps if valid(p.today) and p.before]
    out: dict[str, Any] = {"id": "QA-a", "prompts": len(ps), "read": len(kept),
                           "line": frac(plan.QA_A_MAX_GAP), "holds": "le"}
    value = mean([anchor_term(p) for p in kept])
    out["value"] = frac(value)
    out["se"] = clustered_se([(p.ticket, anchor_term(p)) for p in kept])
    out["parts"] = {
        "S": frac(mean([F(int(p.today[0] == p.today[1])) for p in kept])),
        "A": frac(mean([F(sum(int(x == b) for x in p.today for b in p.before),
                          2 * len(p.before)) for p in kept]))}
    if len(kept) < plan.MIN_ANCHOR_PROMPTS or value is None:
        out.update({"verdict": "unadjudicable", "thin": None,
                    "why": [f"fewer than {plan.MIN_ANCHOR_PROMPTS} prompts hold today's "
                            "two answers valid and one of PLAN_APPLY.md's from the "
                            "pinned provider"]})
        return out
    holds = value <= plan.QA_A_MAX_GAP
    # §0: QA-a reads prompts and not runs, so only the first case of thin applies.
    within = out["se"] is not None and abs(float(value - plan.QA_A_MAX_GAP)) <= out["se"]
    out.update({"verdict": "holds" if holds else "refuted", "thin": within,
                "thin_because": {"within_one_se": within}})
    return out


# ---------------------------------------------------------------------------
# QA-g, reported
# ---------------------------------------------------------------------------

def every_row_at(level: int, us: list[Unit]) -> dict[str, Any]:
    here = [u for u in us if u.level == level]

    def on(*arms: str) -> list[Unit]:
        return [u for u in here if valid(*(getattr(u, a) for a in arms))]
    out: dict[str, Any] = {"decisions": len(here)}
    out["acc"] = {arm: frac(acc(on(arm), arm)) for arm in PAIRS}
    for spec in SPECS:
        kept = on(*spec.needs)
        out[spec.id] = {"read": len(kept), "value": frac(statistic(spec, kept))}
    out["QA-c"]["share"] = frac(share(on("q", "t")))
    return out


def by_ticket(level: int, us: list[Unit]) -> dict[str, Any]:
    """Each arm's accuracy with every ticket counted once, however many times the
    loop escalated it."""
    out = {}
    for arm in PAIRS:
        seen: dict[int, Fraction] = {}
        for u in us:
            if u.level == level and valid(getattr(u, arm)):
                seen.setdefault(u.ticket, h(u, arm))
        out[arm] = {"tickets": len(seen), "acc": frac(mean(list(seen.values())))}
    return out


def by_queue(us: list[Unit]) -> dict[str, Any]:
    """Counts, so that the rare queues read as counts (§0)."""
    out: dict[str, Any] = {}
    for lv in plan.LEVELS:
        rows: dict[str, Counter] = defaultdict(Counter)
        for u in us:
            if u.level != lv:
                continue
            c = rows[u.y]
            c["decisions"] += 1
            for arm in PAIRS:
                pair = getattr(u, arm)
                c[f"{arm}_answers"] += sum(1 for a in pair if a is not None)
                c[f"{arm}_right"] += sum(1 for a in pair if a is not None and a == u.y)
        out[str(lv)] = {q: dict(c) for q, c in sorted(rows.items())}
    out["rare"] = list(RARE)
    return out


def classes(design: population.Design, us: list[Unit],
            before: dict[str, dict[str, tuple[str | None, str | None]]]) -> dict[str, Any]:
    """§5.6: every answer at level 3 against the 29 rules, read from the level's
    text. `before` holds `PLAN_APPLY.md`'s ticket and screen arms by decision."""
    out: dict[str, Any] = {}
    cases = {i: e.prompt.case.as_dict() for i, e in design.decisions.items()}
    for arm in ("t", "i", "q", "apply_ticket", "apply_screen"):
        c: Counter = Counter()
        for u in us:
            if u.level != 3:
                continue
            pair = getattr(u, arm) if arm in PAIRS else before[arm].get(u.id, (None, None))
            for a in pair:
                if a is None:
                    continue
                c[rules.classify(a, cases[u.id])] += 1
                c["most_conditions"] += int(a == rules.most_conditions_queue(cases[u.id]))
                c["answers"] += 1
        out[arm] = dict(c)
    return out


def agreement(us: list[Unit]) -> dict[str, Any]:
    """`S` for each arm, and how often two arms answer alike, by level."""
    out: dict[str, Any] = {}
    for lv in plan.LEVELS:
        here = [u for u in us if u.level == lv]
        cell: dict[str, Any] = {}
        for arm in ("t", "i", "q"):
            kept = [u for u in here if valid(getattr(u, arm))]
            cell[f"S_{arm}"] = frac(mean([F(int(getattr(u, arm)[0] == getattr(u, arm)[1]))
                                          for u in kept]))
        for a, b in (("t", "i"), ("i", "q"), ("t", "q")):
            kept = [u for u in here if valid(getattr(u, a), getattr(u, b))]
            cell[f"{a}_{b}"] = frac(mean([F(sum(int(x == z) for x in getattr(u, a)
                                                for z in getattr(u, b)), 4)
                                          for u in kept]))
        out[str(lv)] = cell
    return out


def apply_beside(us: list[Unit], before: dict[str, dict[str, tuple]],
                 lab: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """`PLAN_APPLY.md`'s ticket and screen arms and the loop's own answer, on the
    same decisions, at every level."""
    out = {}
    for lv in plan.LEVELS:
        here = [u for u in us if u.level == lv]
        cell = {}
        for arm in ("apply_ticket", "apply_screen"):
            kept = [u for u in here if valid(before[arm].get(u.id, (None, None)))]
            cell[arm] = frac(mean([hits(before[arm][u.id], u.y) for u in kept]))
        cell["loop"] = frac(mean([F(int(lab[u.id]["loop"] == u.y)) for u in here]))
        out[str(lv)] = cell
    return out


def the_calls(recs: dict[str, dict]) -> dict[str, Any]:
    out = {}
    for session, rec in recs.items():
        rows = rec["rows"]
        per_arm: dict[str, dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))
        for r in rows:
            arm = r["arm"]
            for att in r.get("call_attempts") or []:
                per_arm[arm]["providers"][att.get("provider")] += 1
                per_arm[arm]["finish_reasons"][att.get("finish_reason")] += 1
                per_arm[arm]["tokens"]["prompt"] += att.get("prompt_tokens") or 0
                per_arm[arm]["tokens"]["completion"] += att.get("completion_tokens") or 0
                per_arm[arm]["tokens"]["reasoning"] += att.get("reasoning_tokens") or 0
        notes = [len(str(r["payload"].get("note"))) for r in rows
                 if isinstance(r.get("payload"), dict) and r["payload"].get("note")]
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
            "notes": {"recorded": len(notes), "coded": False},
        }
    return out


# ---------------------------------------------------------------------------
# Stage C
# ---------------------------------------------------------------------------

def apply_records() -> dict[int, dict[str, dict]]:
    """`PLAN_APPLY.md`'s two passes, by pass and ask id."""
    return {k: {r["id"]: r for r in json.loads(plan.apply_ask(s).read_text())["rows"]}
            for k, s in ((1, "pass1"), (2, "pass2"))}


def apply_answers(design: population.Design,
                  apply_by_pass: dict[int, dict[str, dict]]) -> dict[str, dict[str, tuple]]:
    """`PLAN_APPLY.md`'s ticket and screen arms by decision, as that plan read
    them: any provider, the action valid."""
    out: dict[str, dict[str, tuple]] = {"apply_ticket": {}, "apply_screen": {}}
    for i, e in design.decisions.items():
        tid = prompts.ask_id(prompts.RULE, e.level, e.ticket)
        sid = f"s:{i}"
        out["apply_ticket"][i] = tuple(ascore.answer(apply_by_pass[k].get(tid)) for k in (1, 2))
        out["apply_screen"][i] = tuple(ascore.answer(apply_by_pass[k].get(sid)) for k in (1, 2))
    return out


def score(design: population.Design, recs: dict[str, dict],
          lab: dict[str, dict[str, Any]],
          apply_by_pass: dict[int, dict[str, dict]]) -> dict[str, Any]:
    by_pass = {plan.pass_of(s): {r["id"]: r for r in rec["rows"]} for s, rec in recs.items()
               if s != "smoke"}
    us = units(design, by_pass, lab)
    verdicts = {"QA-a": adjudicate_anchor(anchor_prompts(design, by_pass, apply_by_pass))}
    verdicts.update({spec.id: adjudicate(spec, us) for spec in SPECS})
    before = apply_answers(design, apply_by_pass)
    qa_g = {"by_level": {str(lv): every_row_at(lv, us) for lv in plan.LEVELS},
            "by_ticket": {str(lv): by_ticket(lv, us) for lv in plan.LEVELS},
            "by_true_queue": by_queue(us),
            "classes_at_L3": classes(design, us, before),
            "agreement": agreement(us),
            "apply_beside": apply_beside(us, before, lab),
            "the_calls": the_calls(recs)}
    return {"verdicts": verdicts, "QA-g": qa_g}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage C of PLAN_QUEUE_ALONE.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run QA-g1 to QA-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1
    gate = plan.refuse_unsigned("queue_alone/score.py writes Stage C")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    missing = [s for s in plan.SESSIONS[1:] if not plan.ask_path(s).exists()]
    if missing:
        sys.exit(f"\nREFUSED: no record of {missing}; Stage C reads both passes. "
                 "Nothing was written.\n")
    recs = {s: read(s) for s in plan.SESSIONS[1:]}
    out = score(checks.design, recs, labels(), apply_records())
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "C",
              "signature": gate, "gates": checks.summary(),
              "lines": {"QA-a": frac(plan.QA_A_MAX_GAP), "QA-b": frac(plan.QA_B_LINE),
                        "QA-c": frac(plan.QA_C_LINE), "QA-d": frac(plan.QA_D_LINE),
                        "QA-e": frac(plan.QA_E_LINE), "QA-f": frac(plan.QA_F_LINE)},
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
