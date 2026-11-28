"""
`IM-g1` to `IM-g4` of `PLAN_IMPASSE.md` §7: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They are written and run before the signature, so
that a failure becomes a fix to the draft rather than a signed amendment.

  IM-g1  The inputs reproduce themselves. The suite is green.
         `PLAN_PLACEMENT.md`'s and `PLAN_WHOLE.md`'s verdicts come back from their
         runs, through their scorers, called, and `PLAN_WHOLE.md`'s own blocking
         checks pass, which call `PLAN_PLACEMENT.md`'s. This plan's v1c is those
         plans' v1c: served each of their six v1c runs' answers by
         `placement.gates.Replay`, the loop gives back the run's rules and causes
         case for case. v1n told no impasse is v1c, call for call. And v1n is v1c
         but for the notice, at the impasses alone: at every call of an impasse
         escalation the messages are v1c's but for the first user message's
         paragraph, at every other call they are v1c's, and the notice was sent at
         exactly the record's impasses.
  IM-g2  The protocol is §5's. v1c's four texts are the ones the six v1c runs
         sent, by digest. v1n's are v1c's four and the notice's paragraph, which is
         `PLAN_CAUSE.md`'s arm `i`'s by digest and as that plan's three sessions
         sent it, opens with v2b's paragraph, names no queue and no rule, and is
         quoted in §5.2 of the plan byte for byte. Both arms send one request,
         `PLAN_PLACEMENT.md`'s with its pin, read without building a client. The
         proposer's path names no label, in a name or a string literal, as `N-g2`
         reads them. §0's figures 1 to 6 and 8 come back from the records and the
         text, and `DEFAULTS` is `cause/narrow.py`'s group *many*.
  IM-g3  The schedule is §2.3's: six runs, the arms alternating from the arm
         `ORDER_SEED` draws; the smoke run 30 cases under v1n with
         `PLAN_CHANNEL.md`'s smoke draws; the coverage 1/2; the cap 400; run `k`
         of both arms reading `PLAN_PLACEMENT.md`'s draws of run `k`; the partial
         files ignored by git.
  IM-g4  The signature (`impasse/plan.py`). It does not block a dry run, which
         writes nothing; it blocks every write.

**No float decides a check.** Values are compared as fractions and counts as
integers; a closed plan's verdicts are compared on their fractions, verdicts and
labels, never on a float beside them.

**This module is offline.** It reads labels to recompute closed plans' verdicts,
and the policy through `placement`'s, `whole`'s and `cause`'s own readings,
modules already allowed to carry it. It sends nothing, and what a dry run prints
is pass or fail.
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from cause import plan as c_plan
from channel import gates as ch_gates
from escalations import gates as esc_gates
from manual import instrument as MI
from placement import gates as pl_gates
from placement import loop as pl_loop
from placement import plan as pl_plan
from placement import protocol as pl_protocol
from reasoned_loop import protocol as p
from reuse.gates import run_suite
from rung2.engine2 import PriorityEngine
from whole import gates as wh_gates
from whole import plan as wh_plan
from whole import score as wh_score

from . import plan, protocol, references

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
as_json = pl_gates.as_json
projection = pl_gates.projection
Replay = pl_gates.Replay
replay_is_the_run = ch_gates.replay_is_the_run

# The modules on the proposer's path, and the names they may not carry: `PLAN_SPOTCHECK.md`'s
# `N-g2` names, the label's and the record fields that carry it or the system's own decision.
PROPOSER_PATH = ("plan.py", "protocol.py", "run.py")
FORBIDDEN = esc_gates.TRUTH_NAMES | {"truth_rule", "correct", "proposal_action_correct",
                                     "predicted"}
CAUSE_SESSIONS = ("pass1", "pass2", "oncall")


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
        return {"IM-g1": self.g1, "IM-g2": self.g2, "IM-g3": self.g3, "IM-g4": self.g4}


# ---------------------------------------------------------------------------
# IM-g1
# ---------------------------------------------------------------------------

def closed_runs_v1c() -> dict[str, dict[str, Any]]:
    """The six v1c runs this plan's v1c is held to, read-only, by name."""
    out = {f"pl_v1c_r{rep}": json.loads(pl_plan.run_path("v1c", rep).read_text())
           for rep in range(1, pl_plan.REPS + 1)}
    out.update({f"wh_v1c_r{rep}": json.loads(wh_plan.run_path("v1c", rep).read_text())
                for rep in range(1, wh_plan.REPS + 1)})
    return out


def whole_verdicts() -> dict[str, Any]:
    """`PLAN_WHOLE.md`'s six verdicts, again, from its six runs."""
    recorded = json.loads(wh_plan.score_path().read_text())["verdicts"]
    records, missing = wh_score.read_records()
    runs = {a: [wh_score.read_run(rec) for rec in records[a]] for a in wh_plan.ARMS}
    got = {rid: wh_score.row(rid, runs) for rid in wh_score.ALL_ROWS}
    off = [rid for rid in sorted(recorded)
           if rid not in got or projection(got[rid]) != projection(recorded[rid])]
    return {"rows": len(got), "missing_runs": missing, "departing": off,
            "passes": not off and not missing and len(got) == len(recorded) == 6}


def wholes_own_checks() -> dict[str, Any]:
    """`WR-g1` to `WR-g3`, called, without the suite this module runs once. They
    call `PLAN_PLACEMENT.md`'s `PL-g1` to `PL-g3` and its verdicts."""
    got = wh_gates.run_checks(suite=False)
    return {"WR-g1": got.g1["passes"], "WR-g2": got.g2["passes"], "WR-g3": got.g3["passes"],
            "placement_verdicts": got.g1["closed_verdicts"]["passes"],
            "placement_checks": got.g1["placement_checks"]["passes"],
            "passes": got.blocking_pass}


def capturing(cls, paid: dict[str, Any], **attrs):
    """An instance of an arm's proposer class whose two calls build the messages
    the class would send, and whose `answer` keeps them and serves `paid`'s
    answer for the case and round instead of asking."""
    replay = Replay(paid)

    class Capture(cls):
        name = "replay"

        def __init__(self) -> None:
            self.sent: list[list[Any]] = []
            self.impasse = False
            self.notice_at: list[int] = []
            for k, v in attrs.items():
                setattr(self, k, v)

        def answer(self, idx: int, round_: int, messages) -> p.Answer:
            self.sent.append([idx, round_, messages])
            return replay.answer(idx, round_)

    return Capture()


def replayed_with(proposer, draws, propose) -> dict[str, Any]:
    """`placement`'s loop over the corpus with `draws`, a fresh engine, `proposer`
    and `propose`, timed by a clock that reads 0."""
    engine = PriorityEngine(space=MI.space())
    res = pl_loop.run_loop(list(MI.corpus()), plan.labels(), engine, proposer, plan.COVERAGE,
                           draws, propose=propose, clock=lambda: 0.0)
    return as_json(pl_loop.record_of(res, engine))


def v1c_replay(name: str, paid: dict[str, Any]) -> dict[str, Any]:
    """§7: on one closed v1c run, this plan's v1c is that run; v1n told no impasse
    is v1c; and v1n is v1c but for the notice, at the run's impasses alone."""
    draws = plan.draws(plan.stream("v1c", int(name[-1])))
    c = capturing(protocol.PROPOSERS["v1c"], paid)
    n0 = capturing(protocol.PROPOSERS["v1n"], paid, notice=False)
    n = capturing(protocol.PROPOSERS["v1n"], paid)
    rec_c = replayed_with(c, draws, protocol.ESCALATIONS["v1c"])
    rec_n0 = replayed_with(n0, draws, protocol.ESCALATIONS["v1n"])
    rec_n = replayed_with(n, draws, protocol.ESCALATIONS["v1n"])
    impasses = sorted(esc["idx"] for esc in paid["escalations"]
                      if esc["kind"] == plan.IMPASSE)
    at = set(impasses)
    calls = len(c.sent)
    apart = (len(n.sent) == calls and all(
        x[:2] == y[:2] and (protocol.apart_by_the_notice(x[2], y[2]) if x[0] in at
                            else x[2] == y[2])
        for x, y in zip(as_json(c.sent), as_json(n.sent))))
    out = {"calls": calls,
           "replay_is_the_run": replay_is_the_run(rec_c, paid),
           "records_alike": rec_c == rec_n0 == rec_n,
           "told_no_impasse_is_v1c": as_json(n0.sent) == as_json(c.sent) and not n0.notice_at,
           "apart_at_the_impasses_alone": apart,
           "notice_at_the_impasses": n.notice_at == impasses,
           "impasses": len(impasses),
           "first_calls": sum(1 for x in c.sent if x[1] == 0),
           "placement_calls": sum(1 for x in c.sent if x[1] == 1),
           "calls_with_the_notice": sum(1 for x in n.sent if x[0] in at)}
    out["passes"] = (calls > 0 and out["replay_is_the_run"] and out["records_alike"]
                     and out["told_no_impasse_is_v1c"] and out["apart_at_the_impasses_alone"]
                     and out["notice_at_the_impasses"] and out["impasses"] > 0
                     and out["placement_calls"] > 0)
    return out


def gate_g1(suite: bool = True) -> dict[str, Any]:
    closed = wh_gates.closed_verdicts()
    whole = whole_verdicts()
    own = wholes_own_checks()
    replays = {name: v1c_replay(name, rec) for name, rec in closed_runs_v1c().items()}
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": "PLAN_PLACEMENT.md's and PLAN_WHOLE.md's verdicts come back from their "
                    "runs and PLAN_WHOLE.md's blocking checks pass; this plan's v1c is those "
                    "plans' v1c on their six v1c runs' answers; v1n told no impasse is v1c, "
                    "and v1n is v1c but for the notice, at the impasses alone and at every "
                    "one of them; the suite green",
            "placement_verdicts": closed, "whole_verdicts": whole, "whole_checks": own,
            "replays": replays, "suite": tests,
            "passes": (closed["passes"] and whole["passes"] and own["passes"]
                       and all(r["passes"] for r in replays.values())
                       and tests["passes"] is not False)}


# ---------------------------------------------------------------------------
# IM-g2
# ---------------------------------------------------------------------------

def quoted_in_the_plan(text: str, path: Path | None = None) -> bool:
    """Whether the plan quotes `text` in a fenced `text` block, byte for byte."""
    body = (path or plan.PLAN).read_text()
    blocks = re.findall(r"^```text\n(.*?)^```$", body, flags=re.S | re.M)
    return text in blocks


def cause_sessions() -> dict[str, dict[str, Any]]:
    """`PLAN_CAUSE.md`'s three session records, read-only."""
    return {s: json.loads((c_plan.OUT / f"ask_{s}.json").read_text()) for s in CAUSE_SESSIONS}


def texts() -> dict[str, Any]:
    """§5: v1c's texts are the ones the six v1c runs sent; v1n's are v1c's and
    `PLAN_CAUSE.md`'s arm `i`'s paragraph, as that plan's sessions sent it."""
    sent = {name: {"texts_sha16": rec.get("texts_sha16"), "fingerprint": rec.get("fingerprint")}
            for name, rec in closed_runs_v1c().items()}
    sent["pl_smoke"] = {k: json.loads(pl_plan.smoke_path().read_text()).get(k)
                        for k in ("texts_sha16", "fingerprint")}
    by_digest = {name: rec["texts_sha16"] == protocol.digests("v1c")
                 and rec["fingerprint"] == protocol.fingerprint("v1c")
                 for name, rec in sent.items()}
    sessions = cause_sessions()
    c, n = protocol.digests("v1c"), protocol.digests("v1n")
    nb = protocol.NOTICE_BASE
    out = {"v1c_is_reasoned_loops": (protocol.texts("v1c") == p.texts()
                                     and c == p.digests()
                                     and protocol.fingerprint("v1c") == p.fingerprint()),
           "sent_by_the_v1c_runs": by_digest,
           "system_prompt_digest": c["system_prompt"] == plan.SYSTEM_PROMPT_SHA16,
           "v1n_shares_v1cs_four": all(n[k] == c[k] for k in c),
           "v1n_keys": sorted(n) == sorted([*c, protocol.NOTICE_KEY]),
           "notice_base_digest": n[protocol.NOTICE_KEY] == plan.NOTICE_BASE_SHA16,
           "blind_base_digest": c["blind_base"] == plan.BLIND_BASE_SHA16,
           "sent_by_plan_causes_sessions": {
               s: (rec.get("texts_sha16", {}).get("paragraph_i") == plan.NOTICE_BASE_SHA16
                   and (rec.get("paragraphs") or {}).get("i") == nb)
               for s, rec in sessions.items()},
           "opens_with_v2bs_paragraph": nb == p.BLIND_BASE + protocol.SEPARATOR
                                         + protocol.NOTICE,
           "names_nothing": protocol.names_nothing(nb),
           "ascii": nb.isascii() and nb.endswith("\n"),
           "quoted_in_the_plan": quoted_in_the_plan(nb),
           "fingerprints_differ": protocol.fingerprint("v1c") != protocol.fingerprint("v1n")}
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
        out[f"same_for_both_arms_{attempt}"] = ours["v1c"] == ours["v1n"]
        out[f"placements_but_for_the_pin_{attempt}"] = (
            {**ours["v1n"], "extra_body": {**ours["v1n"]["extra_body"], "provider": None}}
            == {**theirs, "extra_body": {**theirs["extra_body"], "provider": None}}
            and ours["v1n"]["extra_body"]["provider"] == plan.PROVIDER)
    out["pin"] = (plan.PROVIDER == pl_plan.PROVIDER
                  == {"order": ["deepinfra/fp8"], "allow_fallbacks": False}
                  and plan.PROVIDER_NAME == pl_plan.PROVIDER_NAME == "DeepInfra")
    out["asker"] = pl_protocol.Asker.__mro__[1] is p.Asker
    return {**out, "passes": all(out.values())}


def literals_in(path: Path) -> set[str]:
    """Every string literal in a module, docstrings included."""
    tree = ast.parse(path.read_text(), filename=str(path))
    return {n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)}


def no_label_on_the_proposers_path() -> dict[str, Any]:
    leaked = {}
    for name in PROPOSER_PATH:
        path = HERE / name
        found = sorted((esc_gates.names_in(path) | literals_in(path)) & FORBIDDEN)
        if found:
            leaked[name] = found
    return {"modules": [f"impasse/{n}" for n in PROPOSER_PATH], "forbidden_names": leaked,
            "passes": not leaked}


def drafting() -> dict[str, Any]:
    """§0's figures 1 to 6 and 8, from the closed records and the text, and 7."""
    got = references.drafting_reading()
    declared = references.drafting_as_declared(got)
    return {"as_declared": declared, "passes": all(declared.values())}


def gate_g2() -> dict[str, Any]:
    tx, rq, nl, dr = texts(), requests(), no_label_on_the_proposers_path(), drafting()
    return {"what": "v1c's texts are the ones the six v1c runs sent, and v1n's are v1c's and "
                    "PLAN_CAUSE.md's arm i's paragraph, quoted in the plan; both arms send "
                    "PLAN_PLACEMENT.md's request with its pin; the proposer's path names no "
                    "label; §0's figures come back, and DEFAULTS is cause/narrow.py's many",
            "texts": tx, "requests": rq, "no_label_on_the_proposers_path": nl,
            "drafting": dr, "passes": all(x["passes"] for x in (tx, rq, nl, dr))}


# ---------------------------------------------------------------------------
# IM-g3
# ---------------------------------------------------------------------------

def gate_g3() -> dict[str, Any]:
    order = plan.schedule()
    arms = [a for a, _ in order]
    ignored = (REPO / ".gitignore").read_text()
    out = {"schedule": [list(x) for x in order],
           "as_declared": [list(x) for x in order] == plan.DECLARED["schedule"],
           "six_runs_three_an_arm": (len(order) == len(set(order)) == 2 * plan.REPS
                                     and all(arms.count(a) == plan.REPS for a in plan.ARMS)),
           "the_arms_alternate": all(a != b for a, b in zip(arms, arms[1:])),
           "each_repetition_in_order": [r for _, r in order] == sorted(r for _, r in order),
           "smoke": ([plan.SMOKE_N, plan.SMOKE_ARM] == [30, "v1n"]
                     and plan.stream(plan.SMOKE_ARM, None) == "smoke"),
           "coverage": plan.COVERAGE == Fraction(1, 2) == pl_plan.COVERAGE,
           "cap": plan.MAX_ESCALATIONS == pl_plan.MAX_ESCALATIONS == 400,
           "draws_are_placements": all(plan.channel_of(a, r) == pl_plan.channel_of("v1c", r)
                                       for a, r in order),
           "the_partial_files_are_ignored": f"{plan.OUT.name}/*.partial.jsonl" in ignored}
    out["passes"] = all(v for k, v in out.items() if k != "schedule")
    return {"what": "the six runs alternate from the arm the seed draws; the smoke run is 30 "
                    "cases under v1n with PLAN_CHANNEL.md's smoke draws; the coverage is 1/2; "
                    "the cap is 400 escalations; run k of both arms reads PLAN_PLACEMENT.md's "
                    "draws of run k; the partial files are ignored by git", **out}


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
    s, reps = g1["suite"], g1["replays"]
    print(f"\nIM-g1 {mark(g1)}  PLAN_PLACEMENT.md's verdicts departing "
          f"{g1['placement_verdicts']['departing'] or 'none'}, PLAN_WHOLE.md's "
          f"{g1['whole_verdicts']['departing'] or 'none'}; WR-g1 to WR-g3 "
          f"{g1['whole_checks']['passes']}; v1c is their v1c on "
          f"{sum(r['replay_is_the_run'] for r in reps.values())} of {len(reps)} runs; v1n "
          f"told no impasse is v1c {all(r['told_no_impasse_is_v1c'] for r in reps.values())}, "
          f"and apart by the notice at the impasses alone "
          f"{all(r['apart_at_the_impasses_alone'] for r in reps.values())}, over "
          f"{sum(r['calls'] for r in reps.values())} calls")
    print(f"      suite {'not run' if not s.get('ran') else s.get('result')}")
    print(f"IM-g2 {mark(g2)}  texts {g2['texts']['passes']}; requests "
          f"{g2['requests']['passes']}; no label on the proposer's path "
          f"{g2['no_label_on_the_proposers_path']['passes']}; figures "
          f"{g2['drafting']['passes']}")
    print(f"IM-g3 {mark(g3)}  the schedule {g3['schedule']}")
    print(f"IM-g4 {'SIGNED' if g4['passes'] else 'UNSIGNED'}  {g4['found']} signature "
          f"line(s), {g4['unsigned']} blank")
    print(f"\nblocking checks: {'PASS' if checks.blocking_pass else 'FAIL'}")
