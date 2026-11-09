"""
`WR-g1` to `WR-g4` of `PLAN_WHOLE.md` §7: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They are written and run before the signature, so
that a failure becomes a fix to the draft rather than a signed amendment.

  WR-g1  The inputs reproduce themselves. The suite is green.
         `PLAN_PLACEMENT.md`'s six verdicts come back from its six runs, through
         its scorer, called, and its own blocking checks `PL-g1` to `PL-g3` pass:
         its loop, its list, its texts, its requests, its draws and its labels.
         This plan's v1c is that plan's: served each of its three v1c runs'
         answers by `channel.gates.Replay`, the loop gives back the run's rules
         and causes case for case. v1d with v2b's text is v1c: on the same
         replays, v1d's proposer sends v1c's messages at every call, byte for
         byte; with §2.1's text, the same but for the first user message's
         paragraph.
  WR-g2  The protocol is §5's. v1c's four texts are the ones `PLAN_PLACEMENT.md`'s
         v1c runs sent, by digest. v1d's system prompt, placement message and
         retry message are v1c's; its paragraph is §2.1's T1, by digest, quoted
         in §5.2 of the plan byte for byte, opening with v2b's first sentence
         and naming no queue and no rule. Both arms send one request,
         `PLAN_PLACEMENT.md`'s with its pin, read without building a client.
         §0's figures 1 to 3 come back from `PLAN_PLACEMENT.md`'s records, and
         figure 5 from the text.
  WR-g3  The schedule is §2.3's: six runs, the arms alternating from the arm
         `ORDER_SEED` draws; the smoke run 30 cases under v1d with
         `PLAN_CHANNEL.md`'s smoke draws; the coverage 1/2; the cap 400.
  WR-g4  The signature (`whole/plan.py`). It does not block a dry run, which
         writes nothing; it blocks every write.

**No float decides a check.** Values are compared as fractions and counts as
integers; a closed plan's verdicts are compared on their fractions, verdicts and
labels, never on a float beside them.

**This module is offline.** It reads labels to recompute a closed plan's verdicts,
and the policy through `placement.gates`' and `placement.references`' own
readings, modules already allowed to carry it. It sends nothing, and what a dry
run prints is pass or fail, and figures §0 or a published record already states.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from channel import gates as ch_gates
from manual import instrument as MI
from placement import gates as pl_gates
from placement import loop as pl_loop
from placement import plan as pl_plan
from placement import protocol as pl_protocol
from placement import score as pl_score
from reasoned_loop import protocol as p
from reuse.gates import run_suite
from rung2.engine2 import PriorityEngine

from . import plan, protocol, references

as_json = pl_gates.as_json
projection = pl_gates.projection
Replay = pl_gates.Replay
replay_is_the_run = ch_gates.replay_is_the_run


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
        return {"WR-g1": self.g1, "WR-g2": self.g2, "WR-g3": self.g3, "WR-g4": self.g4}


# ---------------------------------------------------------------------------
# WR-g1
# ---------------------------------------------------------------------------

def closed_verdicts() -> dict[str, Any]:
    """`PLAN_PLACEMENT.md`'s six verdicts, again, from its six runs."""
    recorded = json.loads(pl_plan.score_path().read_text())["verdicts"]
    records, missing = pl_score.read_records()
    runs = {a: [pl_score.read_run(rec) for rec in records[a]] for a in pl_plan.ARMS}
    got = {rid: pl_score.row(rid, runs) for rid in pl_score.ALL_ROWS}
    off = [rid for rid in sorted(recorded)
           if rid not in got or projection(got[rid]) != projection(recorded[rid])]
    return {"rows": len(got), "missing_runs": missing, "departing": off,
            "passes": not off and not missing and len(got) == len(recorded) == 6}


def placements_own_checks() -> dict[str, Any]:
    """`PL-g1` to `PL-g3`, called, without the suite this module runs once."""
    got = pl_gates.run_checks(suite=False)
    return {"PL-g1": got.g1["passes"], "PL-g2": got.g2["passes"], "PL-g3": got.g3["passes"],
            "draws": got.g1["draws"]["passes"], "labels": got.g1["labels"]["passes"],
            "passes": got.blocking_pass}


def capturing(cls, paid: dict[str, Any], base: str | None = None):
    """An instance of an arm's proposer class whose two calls build the
    messages the class would send, and whose `answer` keeps them and serves
    `paid`'s answer for the case and round instead of asking."""
    replay = Replay(paid)

    class Capture(cls):
        name = "replay"

        def __init__(self) -> None:
            self.sent: list[list[Any]] = []
            if base is not None:
                self.base = base

        def answer(self, idx: int, round_: int, messages) -> p.Answer:
            self.sent.append([idx, round_, messages])
            return replay.answer(idx, round_)

    return Capture()


def replayed_with(proposer, draws) -> dict[str, Any]:
    """This plan's loop, `PLAN_PLACEMENT.md`'s under v1c, over the corpus with
    `draws`, a fresh engine and `proposer`, timed by a clock that reads 0."""
    engine = PriorityEngine(space=MI.space())
    res = pl_loop.run_loop(list(MI.corpus()), plan.labels(), engine, proposer, plan.COVERAGE,
                           draws, propose=pl_loop.ESCALATIONS["v1c"], clock=lambda: 0.0)
    return as_json(pl_loop.record_of(res, engine))


def v1c_replays(rep: int) -> dict[str, Any]:
    """§7: on `PLAN_PLACEMENT.md`'s run `v1c r<rep>`, this plan's v1c is that
    run, and v1d is v1c but for the one paragraph."""
    paid = json.loads(pl_plan.run_path("v1c", rep).read_text())
    draws = plan.draws(plan.stream("v1c", rep))
    c = capturing(protocol.PROPOSERS["v1c"], paid)
    d0 = capturing(protocol.PROPOSERS["v1d"], paid, base=p.BLIND_BASE)
    d = capturing(protocol.PROPOSERS["v1d"], paid)
    rec_c, rec_d0, rec_d = (replayed_with(x, draws) for x in (c, d0, d))
    calls = len(c.sent)
    out = {"calls": calls,
           "replay_is_the_run": replay_is_the_run(rec_c, paid),
           "records_alike": rec_c == rec_d0 == rec_d,
           "v2b_text_is_v1c": as_json(d0.sent) == as_json(c.sent),
           "one_paragraph_apart": (len(d.sent) == calls and all(
               x[:2] == y[:2] and protocol.one_paragraph_apart(x[2], y[2])
               for x, y in zip(c.sent, d.sent))),
           "first_calls": sum(1 for x in c.sent if x[1] == 0),
           "placement_calls": sum(1 for x in c.sent if x[1] == 1)}
    out["passes"] = (calls > 0 and out["replay_is_the_run"] and out["records_alike"]
                     and out["v2b_text_is_v1c"] and out["one_paragraph_apart"]
                     and out["placement_calls"] > 0)
    return out


def gate_g1(suite: bool = True) -> dict[str, Any]:
    closed = closed_verdicts()
    own = placements_own_checks()
    replays = {f"v1c_r{rep}": v1c_replays(rep) for rep in range(1, pl_plan.REPS + 1)}
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": "PLAN_PLACEMENT.md's verdicts come back from its runs and its own blocking "
                    "checks pass; this plan's v1c is that plan's v1c on its three runs' "
                    "answers, and v1d with v2b's text is v1c, and with T1 is v1c but for one "
                    "paragraph, at every call; the suite green",
            "closed_verdicts": closed, "placement_checks": own, "replays": replays,
            "suite": tests,
            "passes": (closed["passes"] and own["passes"]
                       and all(r["passes"] for r in replays.values())
                       and tests["passes"] is not False)}


# ---------------------------------------------------------------------------
# WR-g2
# ---------------------------------------------------------------------------

def quoted_in_the_plan(text: str, path=None) -> bool:
    """Whether the plan quotes `text` in a fenced block, byte for byte."""
    body = (path or plan.PLAN).read_text()
    blocks = re.findall(r"^```text\n(.*?)^```$", body, flags=re.S | re.M)
    return text in blocks


def texts() -> dict[str, Any]:
    """§5: v1c's texts are the ones `PLAN_PLACEMENT.md`'s v1c runs sent; v1d's
    are v1c's but for the paragraph, which is §2.1's T1."""
    sent = {f"v1c_r{rep}": json.loads(pl_plan.run_path("v1c", rep).read_text())
            for rep in range(1, pl_plan.REPS + 1)}
    sent["smoke"] = json.loads(pl_plan.smoke_path().read_text())
    by_digest = {name: rec.get("texts_sha16") == protocol.digests("v1c")
                 and rec.get("fingerprint") == protocol.fingerprint("v1c")
                 for name, rec in sent.items()}
    c, d = protocol.digests("v1c"), protocol.digests("v1d")
    out = {"v1c_is_reasoned_loops": (protocol.texts("v1c") == p.texts()
                                     and c == p.digests()
                                     and protocol.fingerprint("v1c") == p.fingerprint()),
           "sent_by_placements_v1c_runs": by_digest,
           "system_prompt_digest": c["system_prompt"] == plan.SYSTEM_PROMPT_SHA16,
           "v1d_shares_three": all(d[k] == c[k] for k in ("system_prompt",
                                                          "placement_template",
                                                          "retry_message")),
           "v1d_keys": sorted(d) == ["placement_template", "retry_message", "system_prompt",
                                     "whole_base"],
           "whole_base_digest": d["whole_base"] == plan.WHOLE_BASE_SHA16,
           "blind_base_digest": c["blind_base"] == plan.BLIND_BASE_SHA16,
           "first_sentence": (protocol.WHOLE_BASE.startswith(protocol.FIRST_SENTENCE)
                              and p.BLIND_BASE.startswith(protocol.FIRST_SENTENCE)),
           "names_nothing": protocol.names_nothing(protocol.WHOLE_BASE),
           "ascii": protocol.WHOLE_BASE.isascii() and protocol.WHOLE_BASE.endswith("\n"),
           "quoted_in_the_plan": quoted_in_the_plan(protocol.WHOLE_BASE),
           "fingerprints_differ": protocol.fingerprint("v1c") != protocol.fingerprint("v1d")}
    out["passes"] = all(all(v.values()) if isinstance(v, dict) else v for v in out.values())
    return out


def requests() -> dict[str, Any]:
    """§2.6, §2.7: both arms send one request, `PLAN_PLACEMENT.md`'s, with its
    pin, on a first attempt and on a retry."""
    holder = type("Holder", (), {"model": plan.MODEL})()
    msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}]
    out: dict[str, Any] = {}
    for attempt in (0, 1):
        ours = {arm: pl_protocol.request_with(plan.PROVIDER, plan.MODEL, arm, msgs, attempt)
                for arm in plan.ARMS}
        theirs = p.Asker.request(holder, "v1b", msgs, attempt)
        out[f"same_for_both_arms_{attempt}"] = ours["v1c"] == ours["v1d"]
        out[f"placements_but_for_the_pin_{attempt}"] = (
            {**ours["v1d"], "extra_body": {**ours["v1d"]["extra_body"], "provider": None}}
            == {**theirs, "extra_body": {**theirs["extra_body"], "provider": None}}
            and ours["v1d"]["extra_body"]["provider"] == plan.PROVIDER)
    out["pin"] = (plan.PROVIDER == pl_plan.PROVIDER
                  == {"order": ["deepinfra/fp8"], "allow_fallbacks": False}
                  and plan.PROVIDER_NAME == pl_plan.PROVIDER_NAME == "DeepInfra")
    out["asker"] = pl_protocol.Asker.__mro__[1] is p.Asker
    return {**out, "passes": all(out.values())}


def drafting() -> dict[str, Any]:
    """§0's figures 1 to 3, from `PLAN_PLACEMENT.md`'s records, and 5, from the
    text."""
    got = references.drafting_reading()
    declared = references.drafting_as_declared(got)
    return {"as_declared": declared, "passes": all(declared.values())}


def gate_g2() -> dict[str, Any]:
    tx, rq, dr = texts(), requests(), drafting()
    return {"what": "v1c's texts are the ones PLAN_PLACEMENT.md's v1c runs sent, and v1d's are "
                    "v1c's but for §2.1's T1, quoted in the plan; both arms send that plan's "
                    "request with its pin; §0's figures 1 to 3 and 5 come back",
            "texts": tx, "requests": rq, "drafting": dr,
            "passes": all(x["passes"] for x in (tx, rq, dr))}


# ---------------------------------------------------------------------------
# WR-g3
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
           "smoke": ([plan.SMOKE_N, plan.SMOKE_ARM] == [30, "v1d"]
                     and plan.stream(plan.SMOKE_ARM, None) == "smoke"),
           "coverage": plan.COVERAGE == Fraction(1, 2) == pl_plan.COVERAGE,
           "cap": plan.MAX_ESCALATIONS == pl_plan.MAX_ESCALATIONS == 400,
           "draws_are_placements": all(plan.channel_of(a, r) == pl_plan.channel_of("v1c", r)
                                       for a, r in order)}
    out["passes"] = all(v for k, v in out.items() if k != "schedule")
    return {"what": "the six runs alternate from the arm the seed draws; the smoke run is 30 "
                    "cases under v1d with PLAN_CHANNEL.md's smoke draws; the coverage is 1/2; "
                    "the cap is 400 escalations; run k of both arms reads PLAN_PLACEMENT.md's "
                    "draws of run k", **out}


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
    s, own = g1["suite"], g1["placement_checks"]
    reps = g1["replays"]
    print(f"\nWR-g1 {mark(g1)}  PLAN_PLACEMENT.md's verdicts departing "
          f"{g1['closed_verdicts']['departing'] or 'none'}; its PL-g1 to PL-g3 "
          f"{own['passes']}; v1c is its v1c on "
          f"{sum(r['replay_is_the_run'] for r in reps.values())} of {len(reps)} runs; v1d with "
          f"v2b's text is v1c {all(r['v2b_text_is_v1c'] for r in reps.values())}, and with T1 "
          f"one paragraph apart {all(r['one_paragraph_apart'] for r in reps.values())}, over "
          f"{sum(r['calls'] for r in reps.values())} calls")
    print(f"      suite {'not run' if not s.get('ran') else s.get('result')}")
    print(f"WR-g2 {mark(g2)}  texts {g2['texts']['passes']}; requests "
          f"{g2['requests']['passes']}; figures 1 to 3 and 5 {g2['drafting']['passes']}")
    print(f"WR-g3 {mark(g3)}  the schedule {g3['schedule']}")
    print(f"WR-g4 {'SIGNED' if g4['passes'] else 'UNSIGNED'}  {g4['found']} signature "
          f"line(s), {g4['unsigned']} blank")
    print(f"\nblocking checks: {'PASS' if checks.blocking_pass else 'FAIL'}")
