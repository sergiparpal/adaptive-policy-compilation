"""
`PL-g1` to `PL-g4` of `PLAN_PLACEMENT.md` §7: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They are written and run before the signature, so
that a failure becomes a fix to the draft rather than a signed amendment.

  PL-g1  The inputs reproduce themselves. The suite is green.
         `PLAN_CHANNEL.md`'s six verdicts come back from its six runs, through
         its scorer, called. This plan's loop under v1b is that plan's channel
         arm: served run `c r1`'s answers by `channel.gates.Replay`, it gives
         `channel.loop.run_loop`'s record case for case, and the replay is the
         run. v1c with both exclusions off is v1b on the same replay. Every
         stream of draws has the digest `PLAN_CHANNEL.md`'s records carry. The
         labels the trigger reads agree with `manual.instrument`'s truth.
  PL-g2  The protocol is §5's. Every text is `PLAN_REASONED_LOOP.md` §5.1's, as
         that plan's own check reads it, and the text `PLAN_CHANNEL.md`'s six
         runs sent, by digest. The requests are `reasoned_loop.protocol.Asker`'s
         but for the pin, read without building a client. v1c's list on v1b's
         recorded rounds gives back §0's figures 1 to 3. The hidden policy
         through v1c's path gives back figure 5, and through v1b's path its 199
         edges and every point and case right. The transcriber gives back figure
         6 under both protocols. What v1c leaves out decides nothing.
  PL-g3  The schedule is §2.4's: six runs, the arms alternating from the arm
         `ORDER_SEED` draws; the smoke run 30 cases under v1c with
         `PLAN_CHANNEL.md`'s smoke draws; the bridge's tickets and its order of
         providers rebuilt from `BRIDGE_SEED`; the cap 400 escalations.
  PL-g4  The signature (`placement/plan.py`). It does not block a dry run, which
         writes nothing; it blocks every write.

**No float decides a check.** Draws are compared by digest, values as fractions
and counts as integers; a closed plan's verdicts are compared on their fractions,
verdicts and labels, never on a float beside them.

**This module is offline.** It reads labels to recompute a closed plan's verdicts
and to hold the trigger's labels to the truth, and the policy through
`reasoned_loop.gates`' and `placement.references`' own readings, modules already
allowed to carry it. It sends nothing, and what a dry run prints is pass or fail,
and figures §0 or a published record already states.
"""

from __future__ import annotations

import functools
import json
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from channel import gates as ch_gates
from channel import loop as ch_loop
from channel import plan as ch_plan
from channel import score as ch_score
from manual import instrument as MI
from queue_alone import plan as qa_plan
from reasoned_loop import gates as rl_gates
from reasoned_loop import protocol as p
from reuse.gates import run_suite
from rung2.engine2 import PriorityEngine

from . import loop, plan, protocol, references

as_json = ch_gates.as_json
projection = ch_gates.projection
Replay = ch_gates.Replay


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
        return {"PL-g1": self.g1, "PL-g2": self.g2, "PL-g3": self.g3, "PL-g4": self.g4}


# ---------------------------------------------------------------------------
# PL-g1
# ---------------------------------------------------------------------------

def closed_verdicts() -> dict[str, Any]:
    """`PLAN_CHANNEL.md`'s six verdicts, again, from its six runs."""
    recorded = json.loads(ch_plan.score_path().read_text())["verdicts"]
    records, missing = ch_score.read_records()
    runs = {a: [ch_score.read_run(rec) for rec in records[a]] for a in ch_plan.ARMS}
    got = {rid: ch_score.row(rid, runs) for rid in ch_score.ROWS}
    off = [rid for rid in sorted(recorded)
           if rid not in got or projection(got[rid]) != projection(recorded[rid])]
    return {"rows": len(got), "missing_runs": missing, "departing": off,
            "passes": not off and not missing and len(got) == len(recorded) == 6}


def replayed(run_loop, paid: dict[str, Any], draws) -> dict[str, Any]:
    """A loop over the corpus at coverage 1/2 with `draws`, a fresh engine and
    `paid`'s answers served back, timed by a clock that always reads 0 so that
    the seconds cannot part two loops."""
    engine = PriorityEngine(space=MI.space())
    res = run_loop(list(MI.corpus()), plan.labels(), engine, Replay(paid), plan.COVERAGE,
                   draws, clock=lambda: 0.0)
    return as_json(loop.record_of(res, engine))


def the_loop_is_channels() -> dict[str, Any]:
    """§7: under v1b this plan's loop is `PLAN_CHANNEL.md`'s channel arm, record
    for record, on run `c r1`'s answers; and v1c with both exclusions off is v1b
    on the same answers."""
    paid = json.loads(ch_plan.run_path("c", 1).read_text())
    draws = plan.draws("r1")
    ours = replayed(functools.partial(loop.run_loop, propose=loop.ESCALATIONS["v1b"]),
                    paid, draws)
    theirs = replayed(ch_loop.run_loop, paid, draws)
    off = functools.partial(protocol.propose_v1c, nested=False, governed=False)
    v1c_off = replayed(functools.partial(loop.run_loop, propose=off), paid, draws)
    parts = {k: ours[k] == theirs[k] for k in theirs}
    out = {"parts": parts, "replay_is_the_run": ch_gates.replay_is_the_run(ours, paid),
           "v1c_off_is_v1b": protocol.without_v1c_keys(v1c_off) == ours,
           "escalations": len(ours["escalations"])}
    out["passes"] = all(parts.values()) and out["replay_is_the_run"] and out["v1c_off_is_v1b"]
    return out


def draws_are_channels() -> dict[str, Any]:
    """§5.3: every stream this plan reads has the digest `PLAN_CHANNEL.md`'s
    records carry for it."""
    recorded = {f"r{rep}": json.loads(ch_plan.run_path("c", rep).read_text())
                for rep in range(1, ch_plan.REPS + 1)}
    recorded["smoke"] = json.loads(ch_plan.smoke_path().read_text())
    got = {name: (rec.get("draws_sha16") == plan.draws_digest(name)
                  and rec.get("draws_seed") == plan.draw_seed(name))
           for name, rec in recorded.items()}
    return {"streams": got, "passes": all(got.values()) and set(got) == set(plan.STREAMS)}


def gate_g1(suite: bool = True) -> dict[str, Any]:
    closed = closed_verdicts()
    lp = the_loop_is_channels()
    dr = draws_are_channels()
    lab = ch_gates.labels_against_the_truth()
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": "PLAN_CHANNEL.md's verdicts come back from its runs; under v1b this plan's "
                    "loop is that plan's channel arm on run c r1's answers, and v1c with both "
                    "exclusions off is v1b; every stream of draws is that plan's; the labels "
                    "agree with the truth; the suite green",
            "closed_verdicts": closed, "loop": lp, "draws": dr, "labels": lab,
            "suite": tests,
            "passes": (closed["passes"] and lp["passes"] and dr["passes"]
                       and lab["passes"] and tests["passes"] is not False)}


# ---------------------------------------------------------------------------
# PL-g2
# ---------------------------------------------------------------------------

def texts() -> dict[str, Any]:
    """§5.1: every text is its source's, by `PLAN_REASONED_LOOP.md`'s own check,
    and the text `PLAN_CHANNEL.md`'s six runs sent, by digest."""
    theirs = rl_gates.texts()
    sent = {f"{a}_r{r}": json.loads(ch_plan.run_path(a, r).read_text())
            for a, r in ch_plan.schedule()}
    by_digest = {name: rec.get("texts_sha16") == p.digests()
                 and rec.get("fingerprint") == p.fingerprint() for name, rec in sent.items()}
    out = {"reasoned_loop_check": theirs["passes"], "sent_by_channels_runs": by_digest,
           "system_prompt_digest": p.sha256(p.SYSTEM_PROMPT)[:16] == plan.SYSTEM_PROMPT_SHA16}
    out["passes"] = (out["reasoned_loop_check"] and all(by_digest.values())
                     and out["system_prompt_digest"] and len(by_digest) == 6)
    return out


def requests() -> dict[str, Any]:
    """§1, §2.8: this plan's request is `reasoned_loop.protocol.Asker`'s but for
    the pin, on a first attempt and on a retry, for every pin it sends."""
    holder = type("Holder", (), {"model": plan.MODEL})()
    msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}]
    out: dict[str, Any] = {}
    for name, pin in {"runs": plan.PROVIDER, **plan.BRIDGE_PINS}.items():
        for attempt in (0, 1):
            ours = protocol.request_with(pin, plan.MODEL, "v1c", msgs, attempt)
            theirs = p.Asker.request(holder, "v1b", msgs, attempt)
            same_but_pin = ({**ours, "extra_body": {**ours["extra_body"], "provider": None}}
                            == {**theirs, "extra_body": {**theirs["extra_body"], "provider": None}})
            out[f"{name}_{attempt}"] = same_but_pin and ours["extra_body"]["provider"] == pin
    out["pins"] = (plan.BRIDGE_PINS["deepinfra"] == plan.PROVIDER
                   and plan.BRIDGE_PINS["baidu"] == qa_plan.PROVIDER
                   and plan.PROVIDER == {"order": ["deepinfra/fp8"], "allow_fallbacks": False}
                   and plan.BRIDGE_NAMES == {"baidu": qa_plan.PROVIDER_NAME,
                                             "deepinfra": plan.PROVIDER_NAME})
    return {**out, "passes": all(out.values())}


def drafting() -> dict[str, Any]:
    """§0's figures 1 to 3, by this package's own list on v1b's recorded rounds.
    Figure 4 is Stage A's."""
    got = references.drafting_reading()
    declared = references.drafting_as_declared(got)
    checked = {k: v for k, v in declared.items() if k != "breadth"}
    return {"as_declared": checked, "passes": all(checked.values())}


def hidden_policy() -> dict[str, Any]:
    """§0's figure 5 through v1c's path; through v1b's, `PLAN_REASONED_LOOP.md`'s
    own check, and this module's copy of the path holds to that plan's."""
    v1c = references.hidden_v1c_figures(references.hidden("v1c"))
    theirs = {k: v for k, v in rl_gates.hidden_policy().items() if k != "engine"}
    copy = references.v1b_path_is_reasoned_loops()
    out = {"v1c": v1c, "v1c_as_declared": v1c == plan.DECLARED["hidden_v1c"],
           "v1b": {k: theirs[k] for k in ("born", "installed", "the_199_edges", "space",
                                          "corpus", "passes")},
           "v1b_copy": copy["same"]}
    out["passes"] = out["v1c_as_declared"] and theirs["passes"] and copy["passes"]
    return out


def transcriber() -> dict[str, Any]:
    """§0's figure 6, under both protocols and every draw."""
    got = {name: references.transcriber_as_declared(name, t["figures"])
           for name, t in references.transcribed().items()}
    return {"as_declared": got, "passes": all(all(v.values()) for v in got.values())}


def gate_g2() -> dict[str, Any]:
    tx, rq, dr, hp, tr = texts(), requests(), drafting(), hidden_policy(), transcriber()
    lo = references.left_out_decides_nothing()
    return {"what": "every text is PLAN_REASONED_LOOP.md's and PLAN_CHANNEL.md's runs sent "
                    "it; the requests are that plan's but for the pin; v1c's list on v1b's "
                    "recorded rounds is §0's figures 1 to 3; the hidden policy through both "
                    "paths and the transcriber are §0's; what v1c leaves out decides nothing",
            "texts": tx, "requests": rq, "drafting": dr, "hidden_policy": hp,
            "transcriber": tr, "left_out": lo,
            "passes": all(x["passes"] for x in (tx, rq, dr, hp, tr, lo))}


# ---------------------------------------------------------------------------
# PL-g3
# ---------------------------------------------------------------------------

def gate_g3() -> dict[str, Any]:
    order = plan.schedule()
    arms = [a for a, _ in order]
    bridge = references.bridge_reading()
    declared = references.bridge_as_declared(bridge)
    asks = plan.bridge_asks()
    out = {"schedule": [list(x) for x in order],
           "as_declared": [list(x) for x in order] == plan.DECLARED["schedule"],
           "six_runs_three_an_arm": (len(order) == len(set(order)) == 2 * plan.REPS
                                     and all(arms.count(a) == plan.REPS for a in plan.ARMS)),
           "the_arms_alternate": all(a != b for a, b in zip(arms, arms[1:])),
           "each_repetition_in_order": [r for _, r in order] == sorted(r for _, r in order),
           "smoke": ([plan.SMOKE_N, plan.SMOKE_ARM] == [30, "v1c"]
                     and plan.stream(plan.SMOKE_ARM, None) == "smoke"),
           "coverage": plan.COVERAGE == Fraction(1, 2) == ch_plan.COVERAGE["c"],
           "bridge": declared,
           "bridge_asks": (len(asks) == 2 * plan.BRIDGE_TICKETS * plan.BRIDGE_ASKS
                           and all(sorted(pv for i, pv in asks if i == t)
                                   == sorted(plan.BRIDGE_PROVIDERS)
                                   for t in plan.bridge_tickets())),
           "cap": plan.MAX_ESCALATIONS == 400}
    out["passes"] = (all(v for k, v in out.items() if k not in ("schedule", "bridge"))
                     and all(declared.values()))
    return {"what": "the six runs alternate from the arm the seed draws; the smoke run is 30 "
                    "cases under v1c with PLAN_CHANNEL.md's smoke draws; the bridge's tickets "
                    "and order are rebuilt from their seed; the cap is 400 escalations", **out}


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

def run_checks(suite: bool = True) -> Checks:
    return Checks(g1=gate_g1(suite=suite), g2=gate_g2(), g3=gate_g3(),
                  g4=plan.gate_signature())


def report(checks: Checks) -> None:
    def mark(g: dict) -> str:
        return "PASS" if g["passes"] else "FAIL"

    g1, g2, g3, g4 = checks.g1, checks.g2, checks.g3, checks.g4
    s, lp = g1["suite"], g1["loop"]
    print(f"\nPL-g1 {mark(g1)}  PLAN_CHANNEL.md's verdicts departing "
          f"{g1['closed_verdicts']['departing'] or 'none'}; the loop under v1b is its "
          f"channel arm {all(lp['parts'].values())} (the replay is the run "
          f"{lp['replay_is_the_run']}); v1c off is v1b {lp['v1c_off_is_v1b']}; the draws "
          f"{g1['draws']['passes']}; the labels {g1['labels']['passes']}")
    print(f"      suite {'not run' if not s.get('ran') else s.get('result')}")
    hp, lo = g2["hidden_policy"], g2["left_out"]
    print(f"PL-g2 {mark(g2)}  texts {g2['texts']['passes']}; requests "
          f"{g2['requests']['passes']}; figures 1 to 3 {g2['drafting']['passes']}; the hidden "
          f"policy through v1c {hp['v1c_as_declared']} and v1b {hp['v1b']['passes']}; the "
          f"transcriber {g2['transcriber']['passes']}; {lo['pairs']} rules left out, none "
          f"deciding anything {lo['passes']}")
    print(f"PL-g3 {mark(g3)}  the schedule {g3['schedule']}; the bridge "
          f"{all(g3['bridge'].values())}")
    print(f"PL-g4 {'SIGNED' if g4['passes'] else 'UNSIGNED'}  {g4['found']} signature "
          f"line(s), {g4['unsigned']} blank")
    print(f"\nblocking checks: {'PASS' if checks.blocking_pass else 'FAIL'}")
