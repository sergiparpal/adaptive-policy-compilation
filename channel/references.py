"""
The references of `PLAN_CHANNEL.md` §5.4 and Stage A, all free. **Never on the
proposer's path.**

THE TRANSCRIBER is `PLAN_REASONED_LOOP.md`'s double for the proposer,
`reasoned_loop.references.Transcriber`, called (rule A). At every escalation it
drafts the rule of level 3's text that governs the ticket and places it by the
text's order. Run through this plan's loop, `channel.loop.run_loop`, at the error
arm's coverage and at the channel's with each run's draws, it shows what each
trigger, and each draw, allows a proposer that never errs (§6.12). It bounds
nothing about the model.

THE HIDDEN POLICY THROUGH v1b's PATH is `reasoned_loop.references`', called.

THE SUPPLY each run's draws leave (§5.4): by governing rule, the corpus tickets,
the ones each run's draws make reportable, the transcriber's error escalations,
and the error escalations `PLAN_REASONED_LOOP.md`'s error runs made there, with
the wrong decisions its impasse runs let stand. The governing rule of a ticket is
the one its label names, which `RL-g1` held to level 3's text case by case.

STAGE A's OTHER READINGS are §0's figures 1 to 3: the rare queues' tickets, the
space by true queue, and the draws by run. Everything here reads the labels the
triggers read, the text, the draws, or `PLAN_REASONED_LOOP.md`'s paid records,
read-only; the truth over the space is `manual.instrument`'s, which reads it
where the closed threads read it. None reads an answer this plan buys.
"""

from __future__ import annotations

import collections
import json
from fractions import Fraction
from functools import lru_cache
from typing import Any

from manual import instrument as MI
from reasoned_loop import plan as rl_plan
from reasoned_loop import references as rl_refs
from rung2.engine2 import PriorityEngine

from . import loop, plan

RARE = rl_refs.RARE
ONCALL, SECURITY = "ONCALL_ESCALATION", "SECURITY_INCIDENT"


# ---------------------------------------------------------------------------
# The transcriber under a channel
# ---------------------------------------------------------------------------

def run_transcriber(coverage: Fraction, draws=None, n: int = plan.N):
    """The transcriber through this plan's loop over the first `n` cases, and
    the record it leaves, in a paid run's shape."""
    engine = PriorityEngine(space=MI.space())
    res = loop.run_loop(list(MI.corpus())[:n], plan.labels()[:n], engine,
                        rl_refs.Transcriber(engine), coverage,
                        None if draws is None else draws[:n])
    return res, engine, loop.record_of(res, engine)


def figures(res, engine) -> dict[str, Any]:
    """What a transcriber's run shows: its escalations by cause, its calls, its
    base on both surfaces and the recall of every queue over the space."""
    esc = res.loop.escalations
    causes = collections.Counter(x.kind for x in esc)
    sp, co = MI.over_space(engine), MI.over_corpus(engine)
    oncall = sp["recall"][ONCALL]
    return {"escalations": len(esc), "impasses": causes.get(plan.IMPASSE, 0),
            "conflicts": causes.get(plan.CONFLICT, 0), "errors": causes.get(plan.ERROR, 0),
            "calls": res.loop.calls, "rules": [r.note for r in engine.rules],
            "written": [[x.idx, x.kind, rl_refs.written(x)] for x in esc],
            "channel": res.summary()["channel"],
            "space_right": sp["correct"], "space_points": sp["n"],
            "corpus_right": co["correct"], "corpus_cases": co["n"],
            "recall_oncall": str(Fraction(oncall["right"], oncall["of"])),
            "recall_space": {q: [v["right"], v["of"]] for q, v in sp["recall"].items()},
            "cover": res.cover, "stopped_at": res.stopped_at}


def transcriber(arm: str, rep: int | None = None) -> dict[str, Any]:
    """The transcriber under `arm`: the error arm, or the channel arm with run
    `rep`'s draws, or with the smoke run's over the smoke run's cases when `rep`
    is None."""
    name = plan.stream(arm, rep)
    draws = None if name is None else plan.draws(name)
    n = plan.SMOKE_N if (arm == plan.SMOKE_ARM and rep is None) else plan.N
    res, engine, rec = run_transcriber(plan.COVERAGE[arm], draws, n)
    return {"figures": figures(res, engine), "result": res, "engine": engine,
            "record": rec, "stream": name, "n": n}


def transcribed() -> dict[str, dict[str, Any]]:
    """The transcriber under every draw and trigger §5.4 names, by run name:
    each channel run's draws, and the error trigger."""
    out = {f"c_r{rep}": transcriber("c", rep) for rep in range(1, plan.REPS + 1)}
    out["e"] = transcriber("e")
    return out


def as_declared(name: str, got: dict[str, Any]) -> dict[str, bool]:
    """Each figure §0 declares for the transcriber's run `name`, against `got`."""
    if name == "e":
        want = plan.DECLARED["transcriber_error"]
    else:
        want = plan.DECLARED["transcriber_channel"][name.split("_")[1]]
    return {k: got[k] == v for k, v in want.items()}


# ---------------------------------------------------------------------------
# §0's figures 1 to 3
# ---------------------------------------------------------------------------

def rare_tickets() -> dict[str, Any]:
    """§0's figure 1, off the labels the triggers read."""
    labels = plan.labels()
    out: dict[str, Any] = {}
    for q in (ONCALL, SECURITY):
        at = [i for i, (y, _) in enumerate(labels) if y == q]
        out[q] = {"tickets": len(at)}
        if q == ONCALL:
            out[q]["at"] = at
        out[q]["governed"] = dict(sorted(collections.Counter(labels[i][1] for i in at).items()))
    return out


def space_by_queue() -> dict[str, int]:
    """§0's figure 2: the points of the space whose true queue each queue is."""
    return {q: m.bit_count() for q, m in
            sorted(MI.space_truth().items(), key=lambda kv: -kv[1].bit_count())}


def governed_points(rule_id: str) -> int:
    """The points of the space a listed rule governs under the text's first
    match: its region less every earlier rule's. Read off the text."""
    region = rl_refs.regions()
    taken = 0
    for r in rl_refs.text_rules():
        if r.id == rule_id:
            return (region[r.id] & ~taken).bit_count()
        taken |= region[r.id]
    raise KeyError(rule_id)


def reportable_cases(name: str, coverage: Fraction = plan.COVERAGE["c"]) -> list[int]:
    """The cases whose wrong decision a stream's draws would report: fixed
    before the run, whatever the base decides."""
    return [t for t, u in enumerate(plan.draws(name)) if plan.reportable(coverage, u)]


def draws_by_run() -> dict[str, Any]:
    """§0's figure 3: each channel run's reportable cases, and its reportable
    rare tickets by governing rule."""
    labels = plan.labels()
    out: dict[str, Any] = {}
    for rep in range(1, plan.REPS + 1):
        name = f"r{rep}"
        ok = set(reportable_cases(name))
        row: dict[str, Any] = {"reportable": len(ok)}
        for q in (ONCALL, SECURITY):
            at = [i for i, (y, _) in enumerate(labels) if y == q]
            rules = sorted({labels[i][1] for i in at})
            by_rule = {r: sum(1 for i in at if labels[i][1] == r and i in ok) for r in rules}
            if q == ONCALL:
                row[q] = {"at": [i for i in at if i in ok], "by_rule": by_rule}
            else:
                row[q] = {"reportable": sum(1 for i in at if i in ok), "by_rule": by_rule}
        out[name] = row
    return out


def draws_as_declared(got: dict[str, Any]) -> dict[str, bool]:
    return {name: got.get(name) == want for name, want in plan.DECLARED["draws"].items()}


# ---------------------------------------------------------------------------
# The supply (§5.4), and §0's figure 8
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def _closed_run(arm: str, rep: int) -> str:
    return rl_plan.run_path(arm, rep).read_text()


def closed_runs(arm: str) -> list[dict]:
    """`PLAN_REASONED_LOOP.md`'s three runs of an arm, read-only."""
    return [json.loads(_closed_run(arm, rep)) for rep in range(1, rl_plan.REPS + 1)]


def supply(error_run: dict[str, Any] | None = None) -> dict[str, Any]:
    """By governing rule: the rule's queue, its corpus tickets, the ones each
    channel run's draws make reportable, the transcriber's error escalations
    under the error trigger, `PLAN_REASONED_LOOP.md`'s error runs' and the
    wrong decisions its impasse runs let stand."""
    labels = plan.labels()
    error_run = error_run or transcriber("e")
    tx = collections.Counter(labels[x.idx][1] for x in error_run["result"].loop.escalations
                             if x.kind == plan.ERROR)
    e_runs, i_runs = closed_runs("e"), closed_runs("i")
    ok = {rep: set(reportable_cases(f"r{rep}")) for rep in range(1, plan.REPS + 1)}

    def errors(rec, rule):
        return sum(1 for r in rec["records"] if r["cause"] == plan.ERROR and r["truth_rule"] == rule)

    def stood_wrong(rec, rule):
        return sum(1 for r in rec["records"] if r["cause"] is None and r["outcome"] == "ACTION"
                   and not r["correct"] and r["truth_rule"] == rule)

    rules: dict[str, Any] = {}
    for r in rl_refs.text_rules():
        at = [i for i, (_, rule) in enumerate(labels) if rule == r.id]
        rules[r.id] = {"queue": r.queue, "tickets": len(at),
                       "reportable": [sum(1 for i in at if i in ok[k]) for k in sorted(ok)],
                       "transcriber": tx.get(r.id, 0),
                       "error_runs": [errors(rec, r.id) for rec in e_runs],
                       "impasse_runs_wrong_stood": [stood_wrong(rec, r.id) for rec in i_runs]}
    return {"rules": rules,
            "error_escalations": {"error_runs": [rec["v1b"]["arm_escalations"][plan.ERROR]
                                                 for rec in e_runs],
                                  "transcriber": sum(tx.values())},
            "impasse_wrong_decisions_stood": [rec["v1b"]["silent_errors_among_them"]
                                              for rec in i_runs]}


def supply_as_declared(got: dict[str, Any]) -> dict[str, bool]:
    want = plan.DECLARED["supply"]
    stood = got["impasse_wrong_decisions_stood"]
    return {"rules": all([got["rules"][k]["queue"], got["rules"][k]["tickets"],
                          got["rules"][k]["transcriber"], got["rules"][k]["error_runs"]] == v
                         for k, v in want["rules"].items()),
            "error_escalations": got["error_escalations"] == want["error_escalations"],
            "impasse_wrong_decisions_stood": {"min": min(stood), "max": max(stood)}
            == want["impasse_wrong_decisions_stood"]}


def hidden_through_path() -> dict[str, Any]:
    """`PLAN_REASONED_LOOP.md` §5.6's reference, called."""
    return rl_refs.hidden_through_path()
