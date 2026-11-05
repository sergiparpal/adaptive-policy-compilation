"""
`CH-g1` to `CH-g4` of `PLAN_CHANNEL.md` §7: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed amendment.

  CH-g1  The inputs reproduce themselves. The suite is green.
         `PLAN_REASONED_LOOP.md`'s seven verdicts come back from its six runs
         through its scorer, `reasoned_loop.score`, called. This plan's loop at
         coverage 1 gives `reasoned_loop.loop.run_loop`'s record under its error
         arm, case for case, with the transcriber and with the answers of that
         plan's run `e r1` served back by a replay double; and at coverage 0 its
         record under the impasse arm, with the transcriber. A run's rebuilt
         base is the engine the run ended with, on the transcriber's runs here.
         The labels the triggers read agree with `manual.instrument`'s truth on
         every case.
  CH-g2  The protocol and the draws are §5's and §2.1's. Every text is
         `PLAN_REASONED_LOOP.md` §5.1's source's, as that plan's own check reads
         it, and is the text its six runs sent, by digest. Each run's draws are
         rebuilt from their seed strings, and their reportable cases and rare
         tickets are §0's. The transcriber gives back §0's figures under each
         run's draws and under the error trigger. The hidden policy through v1b's
         path gives back the 199 edges and every point and case right, as
         `PLAN_REASONED_LOOP.md`'s own check reads it. The requests, through the
         SDK double, are `tests/test_reasoned_loop.py`'s, which `CH-g1`'s suite
         runs.
  CH-g3  The schedule is §2.3's: six runs, the arms alternating from the arm
         `ORDER_SEED` draws; the smoke run 30 cases under the channel arm, with
         its own draws; the cap 400 escalations.
  CH-g4  The signature (`channel/plan.py`). It does not block a dry run, which
         writes nothing; it blocks every write.

**No float decides a check.** Draws are compared with the coverage as a fraction,
values as fractions and counts as integers; a closed plan's verdicts are compared
on their fractions, verdicts and labels, never on a float beside them.

**This module is offline.** It reads labels to recompute a closed plan's verdicts
and to hold the triggers' labels to the truth, and the policy through
`reasoned_loop.gates`' own checks, modules already allowed to carry it. It sends
nothing, and what a dry run prints is pass or fail, and figures §0 or a published
record already states.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from authorship import protocol as e
from manual import instrument as MI
from reasoned_loop import gates as rl_gates
from reasoned_loop import loop as rl_loop
from reasoned_loop import plan as rl_plan
from reasoned_loop import protocol as p
from reasoned_loop import references as rl_refs
from reasoned_loop import score as rl_score
from reuse.gates import run_suite
from rung2.engine2 import PriorityEngine

from . import loop, plan, references

CHANNEL_KEYS = ("draw", "reported")      # what a case's row carries beyond rung 2's


@dataclass
class Checks:
    g1: dict
    g2: dict
    g3: dict
    g4: dict

    @property
    def blocking_pass(self) -> bool:
        return self.g1["passes"] and self.g2["passes"] and self.g3["passes"]

    def summary(self) -> dict[str, Any]:
        """What a record carries about the checks it was written behind."""
        return {"CH-g1": self.g1, "CH-g2": self.g2, "CH-g3": self.g3, "CH-g4": self.g4}


def as_json(x: Any) -> Any:
    return json.loads(json.dumps(x, default=str))


# ---------------------------------------------------------------------------
# CH-g1
# ---------------------------------------------------------------------------

def projection(row: dict[str, Any]) -> dict[str, Any]:
    """A recorded verdict without its floats: its fractions, its verdict, its
    thin label, its runs and its counts. The floats beside them label only."""
    out = {}
    for k, v in as_json(row).items():
        if isinstance(v, float):
            continue
        out[k] = v["fraction"] if isinstance(v, dict) and "fraction" in v else v
    return out


def closed_verdicts() -> dict[str, Any]:
    """`PLAN_REASONED_LOOP.md`'s seven verdicts, again, from its six runs."""
    recorded = json.loads(rl_plan.score_path().read_text())["verdicts"]
    records, missing = rl_score.read_records()
    got = rl_score.score(records)["verdicts"]
    off = [rid for rid in sorted(recorded)
           if rid not in got or projection(got[rid]) != projection(recorded[rid])]
    return {"rows": len(got), "missing_runs": missing, "departing": off,
            "passes": not off and not missing and len(got) == len(recorded) == 7}


class ReplayDesync(Exception):
    """The loop asked for a call the record never made. Not a `ProposalError`,
    so the loop does not swallow it."""


class Replay:
    """A proposer double that serves a paid run's answers back, each where the
    run asked for it, by case and round, and raises on any other call. A call
    that failed is served as the failure it was."""

    name = "replay"

    def __init__(self, record: dict[str, Any]):
        self.rows = {(esc["idx"], c["round"]): c
                     for esc in record["escalations"] for c in esc.get("calls") or []}
        self.asked: list[tuple[int, int]] = []

    def answer(self, idx: int, round_: int) -> p.Answer:
        self.asked.append((idx, round_))
        row = self.rows.get((idx, round_))
        if row is None:
            raise ReplayDesync(f"case {idx}, round {round_}: the record made no such call")
        if row["failure"] is not None:
            raise e.ProposalFailed(row["failure"], row["finish_reason"], row["attempts"],
                                   list(row.get("call_attempts") or []))
        return p.Answer(row["payload"].get("action"), row["payload"], row["raw"],
                        row["finish_reason"], row["attempts"],
                        list(row.get("call_attempts") or []),
                        **{k: row.get(k) for k in p.EXTRA})

    def first(self, case, idx: int) -> p.Answer:
        return self.answer(idx, 0)

    def placement(self, case, draft, message: str, idx: int,
                  listed: list[str] | None = None) -> p.Answer:
        return self.answer(idx, 1)


def same_record(ours: dict[str, Any], theirs: dict[str, Any]) -> dict[str, bool]:
    """This plan's record against `PLAN_REASONED_LOOP.md`'s, part by part: every
    case's row on that plan's keys, and the summary on that plan's keys."""
    a, b = as_json(ours), as_json(theirs)
    out = {"records": [{k: v for k, v in r.items() if k not in CHANNEL_KEYS}
                       for r in a["records"]] == b["records"],
           "v1b": {k: v for k, v in a["v1b"].items() if k != "channel"} == b["v1b"]}
    for k in ("metrics", "calls", "rules", "edge_log", "edge_channels", "escalations"):
        out[k] = a[k] == b[k]
    return out


def trigger_kept(rec: dict[str, Any], coverage: Fraction, draws=None) -> bool:
    """The record of the trigger (§5.3, §2.4): every row carries its case's draw,
    or none without draws; an IMPASSE or a CONFLICT is its own cause and nothing
    is said of a report; and a row says whether its decision was reported where,
    and only where, the engine decided with a queue other than the label, as
    `plan.reportable` says from the draw, and escalated as an `ERROR` exactly
    then. At coverage 1 every wrong decision is reported; at 0 none is."""
    for r in rec["records"]:
        draw = None if draws is None else draws[r["idx"]]
        if r["draw"] != draw:
            return False
        if r["outcome"] != "ACTION":
            if r["reported"] is not None or r["cause"] != r["outcome"]:
                return False
            continue
        decided = r["engine_action"] if r["cause"] == plan.ERROR else r["predicted"]
        wrong = decided != r["truth"]
        if (r["reported"] is not None) != wrong:
            return False
        if wrong and r["reported"] != plan.reportable(coverage, draw):
            return False
        if r["cause"] != (plan.ERROR if wrong and r["reported"] else None):
            return False
    return True


def both_loops(proposer_of, coverage: Fraction, arm: str) -> dict[str, Any]:
    """This plan's loop at `coverage` and `reasoned_loop`'s under `arm`, over the
    corpus, each with a fresh engine and a fresh proposer, timed by a clock that
    always reads 0 so that the seconds cannot part them."""
    corpus, labels = list(MI.corpus()), plan.labels()
    recs = []
    for run in (lambda eng, prop: loop.run_loop(corpus, labels, eng, prop, coverage,
                                                 clock=lambda: 0.0),
                lambda eng, prop: rl_loop.run_loop(corpus, labels, eng, prop, arm,
                                                   clock=lambda: 0.0)):
        engine = PriorityEngine(space=MI.space())
        res = run(engine, proposer_of(engine))
        recs.append(loop.record_of(res, engine))
    parts, kept = same_record(*recs), trigger_kept(recs[0], coverage)
    return {"parts": parts, "trigger_kept": kept,
            "escalations": len(recs[0]["escalations"]), "record": recs[0],
            "passes": all(parts.values()) and kept}


def replay_is_the_run(replayed: dict[str, Any], paid: dict[str, Any]) -> bool:
    """The replay bore the paid run's rules, at its cases, and escalated where
    it did, for the same causes: the double serves the run it says it serves."""
    def rules(rec):
        return [(r["rule_id"], r["born_at"], r["action"], r["conditions"]) for r in rec["rules"]]
    return (rules(as_json(replayed)) == rules(paid)
            and [r["cause"] for r in replayed["records"]] == [r["cause"] for r in paid["records"]])


def coverage_one_and_zero() -> dict[str, Any]:
    """§7: this plan's loop at coverage 1 is that plan's error arm, with the
    transcriber and with run `e r1`'s answers replayed; at 0, its impasse arm."""
    paid = json.loads(rl_plan.run_path("e", 1).read_text())
    one_t = both_loops(rl_refs.Transcriber, Fraction(1), "e")
    one_r = both_loops(lambda engine: Replay(paid), Fraction(1), "e")
    zero_t = both_loops(rl_refs.Transcriber, Fraction(0), "i")
    faithful = replay_is_the_run(one_r.pop("record"), paid)
    for got in (one_t, zero_t):
        del got["record"]
    return {"one_transcriber": one_t, "one_replay": {**one_r, "replay_is_the_run": faithful},
            "zero_transcriber": zero_t,
            "passes": one_t["passes"] and one_r["passes"] and faithful and zero_t["passes"]}


def rebuilds(transcribed: dict[str, dict]) -> dict[str, Any]:
    """§7: a run's rebuild, `manual.instrument.final_engine`, is the engine the
    run ended with, on the transcriber's runs; and each run's record of the
    trigger is `trigger_kept`, with that run's draws."""
    got = {name: rl_gates.same_engine(MI.final_engine(as_json(r["record"])), r["engine"])
           for name, r in transcribed.items()}
    kept = {name: trigger_kept(as_json(r["record"]), plan.COVERAGE[name[0]],
                               None if r["stream"] is None else plan.draws(r["stream"]))
            for name, r in transcribed.items()}
    return {"runs": got, "trigger_kept": kept,
            "passes": all(got.values()) and all(kept.values())}


def labels_against_the_truth() -> dict[str, Any]:
    """The labels the triggers read give every corpus case the queue
    `manual.instrument` labels it with."""
    labels, truth = plan.labels(), MI.corpus_truth()
    off = [i for i, ((y, _), t) in enumerate(zip(labels, truth)) if y != t]
    return {"cases": len(labels), "departing": off[:10], "source": str(plan.labels_path()),
            "passes": len(labels) == len(truth) == plan.N and not off}


def gate_g1(transcribed: dict[str, dict], suite: bool = True) -> dict[str, Any]:
    closed = closed_verdicts()
    arms = coverage_one_and_zero()
    rb = rebuilds(transcribed)
    lab = labels_against_the_truth()
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": "PLAN_REASONED_LOOP.md's verdicts come back from its runs; this plan's "
                    "loop at coverage 1 is that plan's error arm, with the transcriber and "
                    "with run e r1's answers replayed, and at coverage 0 its impasse arm; a "
                    "run's rebuild is its engine; the labels agree with the truth; the suite "
                    "green",
            "closed_verdicts": closed, "coverage": arms, "rebuilds": rb, "labels": lab,
            "suite": tests,
            "passes": (closed["passes"] and arms["passes"] and rb["passes"]
                       and lab["passes"] and tests["passes"] is not False)}


# ---------------------------------------------------------------------------
# CH-g2
# ---------------------------------------------------------------------------

def texts() -> dict[str, Any]:
    """§5.1: every text is its source's, by `PLAN_REASONED_LOOP.md`'s own check,
    and the text that plan's six runs sent, by digest."""
    theirs = rl_gates.texts()
    sent = {f"{a}_r{r}": json.loads(rl_plan.run_path(a, r).read_text())
            for a, r in rl_plan.schedule()}
    by_digest = {name: rec.get("texts_sha16") == p.digests()
                 and rec.get("fingerprint") == p.fingerprint() for name, rec in sent.items()}
    out = {"reasoned_loop_check": theirs["passes"], "sent_by_its_runs": by_digest,
           "system_prompt_digest": p.sha256(p.SYSTEM_PROMPT)[:16] == plan.SYSTEM_PROMPT_SHA16}
    out["passes"] = (out["reasoned_loop_check"] and all(by_digest.values())
                     and out["system_prompt_digest"] and len(by_digest) == 6)
    return out


def the_draws() -> dict[str, Any]:
    """§2.1: every stream rebuilt from its seed string, one draw per case, each
    from 0 to 1, no two streams alike; and §0's figure 3."""
    rebuilt = {}
    for name in plan.STREAMS:
        rng = random.Random(f"PLAN_CHANNEL/channel/{plan.CHANNEL_SEED}/{name}")
        rebuilt[name] = (tuple(rng.random() for _ in range(plan.N)) == plan.draws(name)
                         and plan.draw_seed(name) == f"PLAN_CHANNEL/channel/97/{name}"
                         and all(0 <= u < 1 for u in plan.draws(name)))
    distinct = len({plan.draws(name) for name in plan.STREAMS}) == len(plan.STREAMS)
    figures = references.draws_by_run()
    declared = references.draws_as_declared(figures)
    out = {"rebuilt": rebuilt, "distinct": distinct, "as_declared": declared,
           "digests": {name: plan.draws_digest(name) for name in plan.STREAMS}}
    out["passes"] = all(rebuilt.values()) and distinct and all(declared.values())
    return out


def transcriber(transcribed: dict[str, dict]) -> dict[str, Any]:
    """§0's figures 4 and 5 for the transcriber, under each run's draws and
    under the error trigger."""
    got = {name: references.as_declared(name, r["figures"]) for name, r in transcribed.items()}
    return {"as_declared": got, "passes": all(all(v.values()) for v in got.values())}


def gate_g2(transcribed: dict[str, dict]) -> dict[str, Any]:
    tx, dr, tr, hp = texts(), the_draws(), transcriber(transcribed), rl_gates.hidden_policy()
    hp = {k: v for k, v in hp.items() if k != "engine"}
    return {"what": "every text is PLAN_REASONED_LOOP.md's and its runs sent it; every run's "
                    "draws are rebuilt from their seed and are §0's; the transcriber gives "
                    "back §0's figures; the hidden policy through v1b's path is born whole "
                    "with its 199 edges and decides both surfaces right. The requests are "
                    "tests/test_reasoned_loop.py's",
            "texts": tx, "draws": dr, "transcriber": tr, "hidden_policy": hp,
            "passes": all(x["passes"] for x in (tx, dr, tr, hp))}


# ---------------------------------------------------------------------------
# CH-g3
# ---------------------------------------------------------------------------

def gate_g3() -> dict[str, Any]:
    order = plan.schedule()
    arms = [a for a, _ in order]
    out = {"schedule": [list(x) for x in order],
           "as_declared": [list(x) for x in order] == plan.DECLARED["schedule"],
           "six_runs_three_an_arm": (len(order) == len(set(order)) == 2 * plan.REPS
                                     and all(arms.count(a) == plan.REPS for a in plan.ARMS)),
           "the_arms_alternate": all(a != b for a, b in zip(arms, arms[1:])),
           "each_repetition_in_order": [r for _, r in order] == sorted(r for _, r in order),
           "smoke": ([plan.SMOKE_N, plan.SMOKE_ARM] == [30, "c"]
                     and plan.stream(plan.SMOKE_ARM, None) == "smoke"
                     and plan.draw_seed("smoke") not in {plan.draw_seed(f"r{r}")
                                                         for r in range(1, plan.REPS + 1)}),
           "coverages": plan.COVERAGE == {"c": Fraction(1, 2), "e": Fraction(1)},
           "cap": plan.MAX_ESCALATIONS == 400}
    out["passes"] = all(v for k, v in out.items() if k != "schedule")
    return {"what": "the six runs alternate from the arm the seed draws; the smoke run is 30 "
                    "cases under the channel arm with its own draws; the cap is 400 "
                    "escalations", **out}


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

def run_checks(suite: bool = True) -> Checks:
    transcribed = references.transcribed()
    return Checks(g1=gate_g1(transcribed, suite=suite), g2=gate_g2(transcribed),
                  g3=gate_g3(), g4=plan.gate_signature())


def report(checks: Checks) -> None:
    def mark(g: dict) -> str:
        return "PASS" if g["passes"] else "FAIL"

    g1, g2, g3, g4 = checks.g1, checks.g2, checks.g3, checks.g4
    s, cov = g1["suite"], g1["coverage"]
    print(f"\nCH-g1 {mark(g1)}  PLAN_REASONED_LOOP.md's verdicts departing "
          f"{g1['closed_verdicts']['departing'] or 'none'}; coverage 1 is its error arm: "
          f"transcriber {cov['one_transcriber']['passes']}, replay of e r1 "
          f"{cov['one_replay']['passes']} (the run itself "
          f"{cov['one_replay']['replay_is_the_run']}); coverage 0 is its impasse arm "
          f"{cov['zero_transcriber']['passes']}; the rebuilds {g1['rebuilds']['passes']}; "
          f"the labels {g1['labels']['passes']}")
    print(f"      suite {'not run' if not s.get('ran') else s.get('result')}")
    hp = g2["hidden_policy"]
    print(f"CH-g2 {mark(g2)}  texts {g2['texts']['passes']}; the draws rebuilt and as "
          f"declared {g2['draws']['passes']}; the transcriber as declared "
          f"{g2['transcriber']['passes']}; the hidden policy through v1b: {hp['born']} born, "
          f"{hp['installed']} edges installed, the 199 {hp['the_199_edges']}")
    print(f"CH-g3 {mark(g3)}  the schedule {g3['schedule']}")
    print(f"CH-g4 {'SIGNED' if g4['passes'] else 'UNSIGNED'}  {g4['found']} signature "
          f"line(s), {g4['unsigned']} blank")
    print(f"\nblocking checks: {'PASS' if checks.blocking_pass else 'FAIL'}")
