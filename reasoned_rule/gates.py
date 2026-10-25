"""
`RR-g1` to `RR-g4` of `PLAN_REASONED_RULE.md` §6: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  RR-g1  The inputs reproduce themselves. The suite is green.
         `PLAN_FIRST_MATCH.md`'s own `FM-g1` to `FM-g3` pass, called; they call
         `PLAN_QUEUE_ALONE.md`'s, which hold the 29 rules to the truth of all
         790 escalations. Its design, rebuilt, is
         `results_first_match/sample.json`'s, and its six verdicts come back
         from its two passes as `score.json` holds them. The 29 rules of level
         3's text, applied in order to the 134,400 points of the space, give
         every point the queue the policy gives it.
  RR-g2  The prompts are the closed plans'. Every rule-arm prompt carries the
         digest `PLAN_QUEUE_ALONE.md` recorded for its rule arm at level 3, and
         every plain-arm prompt the digest it recorded for its plain arm, which
         `PLAN_FIRST_MATCH.md` recorded for its plain and reasoning arms too.
         Every reasoning-rule-arm prompt is the rule arm's on the same ticket,
         text for text, and every reasoning-arm prompt the plain arm's. No
         builder takes a record's row, one changed character moves a digest,
         and no digest stands for two texts. The requests themselves are
         checked through `tests/doubles.py`'s SDK double in
         `tests/test_reasoned_rule.py`, which `RR-g1`'s suite runs.
  RR-g3  The population and the schedule are §0's and §1's: 171 prompts an
         arm on level 3's 320 decisions, each served once in every arm; each
         pass every prompt once, in its order rebuilt from `ORDER_SEED`; the
         smoke run two distinct prompts of each arm.
  RR-g4  The signature (`reasoned_rule/plan.py`). It does not block a dry run,
         which writes nothing; it blocks every write.

**This module is offline.** It reads labels for one thing only: to recompute
`PLAN_FIRST_MATCH.md`'s verdicts from that plan's records and compare them with
what those records hold, which its own checks do for `PLAN_QUEUE_ALONE.md`'s.
The policy over the space is read through `rung3.order_search_ls`, a module
already allowed to see the oracle. It sends nothing, and it prints no figure of
any plan: a check passes or fails.
"""

from __future__ import annotations

import inspect
import json
from collections import Counter
from dataclasses import dataclass
from typing import Any

from harness.domain import ACTIONS
from rung3.order_search_ls import space_truth_masks

from first_match import ask as fmask
from first_match import gates as fmgates
from first_match import score as fmscore
from queue_alone import gates as qgates
from queue_alone import prompts as qprompts
from queue_alone import rules as qrules
from reuse.gates import run_suite

from . import plan, population, prompts, shape

# What a builder may be handed. A row of a record carries the truth (rule B).
BUILDER_PARAMETERS = {"ask": ("arm", "ticket", "case"),
                      "system_prompt": ("arm",),
                      "user_message": ("arm", "case")}


@dataclass
class Checks:
    g1: dict
    g2: dict
    g3: dict
    g4: dict
    design: population.Design

    @property
    def blocking_pass(self) -> bool:
        return self.g1["passes"] and self.g2["passes"] and self.g3["passes"]

    def summary(self) -> dict[str, Any]:
        """What a record carries about the checks it was written behind."""
        return {"RR-g1": self.g1, "RR-g2": self.g2, "RR-g3": self.g3, "RR-g4": self.g4}


# ---------------------------------------------------------------------------
# RR-g1
# ---------------------------------------------------------------------------

def first_match_passes() -> dict[int, dict[str, dict]]:
    """`PLAN_FIRST_MATCH.md`'s two passes, by pass and ask id."""
    return {k: {r["id"]: r for r in json.loads(plan.first_match_ask(s).read_text())["rows"]}
            for k, s in ((1, "pass1"), (2, "pass2"))}


def first_match_rows(fd) -> dict[str, Any]:
    """`PLAN_FIRST_MATCH.md`'s six verdicts, again, from its two passes."""
    recorded = json.loads(plan.first_match_score().read_text())["verdicts"]
    by_pass = first_match_passes()
    us = fmscore.units(fd, by_pass, fmscore.labels())
    got = {"FM-a": fmscore.adjudicate_anchor(
        fmscore.anchor_prompts(fd, by_pass, fmgates.queue_alone_passes())),
           "FM-c": fmscore.adjudicate_naming(us)}
    got.update({spec.id: fmscore.adjudicate(spec, us) for spec in fmscore.SPECS})
    off = [rid for rid in sorted(recorded)
           if rid not in got or not qgates.same_verdict(got[rid], recorded[rid])]
    return {"rows": len(got), "departing": off, "passes": not off and len(got) == 6}


def the_list_over_the_space() -> dict[str, Any]:
    """The list's first match, read from level 3's text, is the policy at every
    point of the space."""
    sp = shape.space()
    mine = shape.first_match_masks()
    theirs = space_truth_masks(sp)
    off = sorted(q for q in set(mine) | set(theirs) if mine.get(q, 0) != theirs.get(q, 0))
    covered = 0
    for m in mine.values():
        covered |= m
    return {"points": sp.n, "queues": sorted(theirs), "departing": off,
            "every_point_decided": covered == sp.full,
            "passes": (not off and covered == sp.full and sp.n == 134400
                       and set(theirs) <= set(ACTIONS))}


def gate_g1(design: population.Design, suite: bool = True) -> dict[str, Any]:
    fm = fmgates.run_checks(suite=False)
    ok, why = fmask.sample_matches(fm.design)
    rows = first_match_rows(fm.design)
    over = the_list_over_the_space()
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": "PLAN_FIRST_MATCH.md's checks pass, its design is its Stage A's, its "
                    "verdicts come back from its passes; the list's first match is the "
                    "policy over the space; the suite green",
            "first_match_checks": fm.blocking_pass,
            "first_match_design": {"passes": ok, "why": why},
            "first_match_rows": rows, "the_list_over_the_space": over, "suite": tests,
            "passes": (fm.blocking_pass and ok and rows["passes"] and over["passes"]
                       and tests["passes"] is not False)}


# ---------------------------------------------------------------------------
# RR-g2
# ---------------------------------------------------------------------------

def theirs(design: population.Design, arm: str, recorded: dict[str, dict],
           their_arm: str) -> dict[str, Any]:
    """Every prompt of `arm` is a closed plan's prompt of `their_arm` at level 3,
    digest for digest, and every one of those is here."""
    asks = design.asks_of(arm)
    off = [a.id for a in asks
           if recorded.get(a.id, {}).get("digest") != a.digest
           or recorded[a.id]["arm"] != their_arm or recorded[a.id]["level"] != plan.LEVEL]
    every = sorted(i for i, r in recorded.items()
                   if r["arm"] == their_arm and r["level"] == plan.LEVEL)
    return {"prompts": len(asks), "departing": off[:10],
            "every_one_of_theirs": sorted(a.id for a in asks) == every,
            "passes": not off and sorted(a.id for a in asks) == every}


def closed_plans(design: population.Design) -> dict[str, Any]:
    """The rule and plain arms are `PLAN_QUEUE_ALONE.md`'s, and the plain and
    reasoning arms carry the digests `PLAN_FIRST_MATCH.md` recorded."""
    qa = json.loads(plan.queue_alone_sample().read_text())["design"]["asks"]
    fm = json.loads(plan.first_match_sample().read_text())["design"]["asks"]
    out = {"rule_arm_is_queue_alones": theirs(design, prompts.RULE, qa, qprompts.RULE),
           "plain_arm_is_queue_alones": theirs(design, prompts.PLAIN, qa, qprompts.PLAIN),
           "plain_arm_is_first_matchs": theirs(design, prompts.PLAIN, fm, "q"),
           "reasoning_arm_is_first_matchs": theirs(design, prompts.REASONING, fm, "r")}
    out["passes"] = all(v["passes"] for v in out.values())
    return out


def reasoned_arms(design: population.Design) -> dict[str, Any]:
    """Every reasoning arm's prompt is its quiet arm's on the same ticket."""
    pairs = ((prompts.REASONING_RULE, prompts.RULE), (prompts.REASONING, prompts.PLAIN))
    off = [a.id for arm, quiet in pairs for a in design.asks_of(arm)
           if (a.system, a.user) != (design.asks[prompts.ask_id(quiet, a.ticket)].system,
                                     design.asks[prompts.ask_id(quiet, a.ticket)].user)]
    return {"prompts": sum(len(design.asks_of(arm)) for arm, _ in pairs),
            "not_their_quiet_arms": off[:10], "passes": not off}


def texts(design: population.Design) -> dict[str, Any]:
    """§5.1's claims, read off the texts the package builds."""
    case = design.asks_of(prompts.RULE)[0].case
    rule = qprompts.system_prompt(qprompts.RULE, plan.LEVEL)
    plain = qprompts.system_prompt(qprompts.PLAIN, plan.LEVEL)
    out = {
        "rule_arms_send_the_rule_prompt": all(
            (prompts.system_prompt(a), prompts.user_message(a, case))
            == (rule, qprompts.user_message(qprompts.RULE, case)) for a in prompts.RULE_ARMS),
        "plain_arms_send_the_plain_prompt": all(
            (prompts.system_prompt(a), prompts.user_message(a, case))
            == (plain, qprompts.user_message(qprompts.PLAIN, case))
            for a in (prompts.PLAIN, prompts.REASONING)),
        "the_rule_prompt_writes_a_rule": '"conditions"' in rule and "beats" in rule,
        "the_rule_user_message_is_the_empty_base": prompts.user_message(
            prompts.RULE, case).startswith(qprompts.EMPTY_BASE),
        "every_arm_holds_the_list": all(
            r.id in prompts.system_prompt(a) for a in prompts.ARMS for r in qrules.rules()),
    }
    out["passes"] = all(out.values())
    return out


def builders() -> dict[str, Any]:
    got = {name: tuple(inspect.signature(getattr(prompts, name)).parameters)
           for name in BUILDER_PARAMETERS}
    return {"parameters": got, "passes": got == BUILDER_PARAMETERS}


def digests(design: population.Design) -> dict[str, Any]:
    seen: dict[str, set[tuple[str, str]]] = {}
    for a in design.asks.values():
        seen.setdefault(a.digest, set()).add((a.system, a.user))
    collisions = [d for d, t in seen.items() if len(t) > 1]
    texts_ = {(a.system, a.user) for a in design.asks.values()}
    a = design.asks_of(prompts.REASONING_RULE)[0]
    moved = prompts.digest(a.system, a.user + " ") != a.digest
    return {"asks": len(design.asks), "texts": len(texts_), "distinct": len(seen),
            "collisions": collisions[:10], "one_changed_character_moves_the_digest": moved,
            "passes": (not collisions and moved and len(seen) == len(texts_)
                       and len(texts_) == 2 * plan.TICKET_PROMPTS)}


def gate_g2(design: population.Design) -> dict[str, Any]:
    cp, ra = closed_plans(design), reasoned_arms(design)
    tx, bd, dg = texts(design), builders(), digests(design)
    return {"what": "the rule and plain arms are PLAN_QUEUE_ALONE.md's at level 3, digest "
                    "for digest, and the plain and reasoning arms PLAN_FIRST_MATCH.md's; "
                    "each reasoning arm's texts are its quiet arm's; no builder takes a row; "
                    "the digests have teeth. The requests are tests/test_reasoned_rule.py's, "
                    "through the SDK double",
            "closed_plans": cp, "reasoned_arms": ra, "texts": tx, "builders": bd,
            "digests": dg,
            "passes": all(x["passes"] for x in (cp, ra, tx, bd, dg))}


# ---------------------------------------------------------------------------
# RR-g3
# ---------------------------------------------------------------------------

def populations(design: population.Design) -> dict[str, Any]:
    per = Counter(a.arm for a in design.asks.values())
    served = {arm: Counter(i for aid, a in design.asks.items() if a.arm == arm
                           for i in design.serves[aid]) for arm in prompts.ARMS}
    every_once = {arm: set(c) == set(design.decisions) and set(c.values()) == {1}
                  for arm, c in served.items()}
    out = {"prompts": {arm: per[arm] for arm in prompts.ARMS},
           "decisions": len(design.decisions), "every_decision_served_once": every_once}
    out["passes"] = (all(per[arm] == plan.TICKET_PROMPTS for arm in prompts.ARMS)
                     and len(design.asks) == len(prompts.ARMS) * plan.TICKET_PROMPTS
                     and len(design.decisions) == plan.DECISIONS
                     and all(every_once.values()))
    return out


def schedule(design: population.Design) -> dict[str, Any]:
    rebuilt = population.sessions_for(design.asks)
    every = sorted(design.asks)
    passes = {s: sorted(design.sessions[s]) == every for s in plan.SESSIONS[1:]}
    smoke = design.sessions["smoke"]
    per = Counter(design.asks[i].arm for i in smoke)
    out = {
        "rebuilt_from_the_seed": rebuilt == design.sessions,
        "each_pass_holds_every_prompt_once": passes,
        "the_passes_differ": design.sessions["pass1"] != design.sessions["pass2"],
        "smoke": smoke,
        "smoke_two_distinct_of_each_arm": (
            len(smoke) == len(set(smoke)) == len(prompts.ARMS) * plan.SMOKE_PER_ARM
            and all(per[arm] == plan.SMOKE_PER_ARM for arm in prompts.ARMS)),
    }
    out["passes"] = (out["rebuilt_from_the_seed"] and all(passes.values())
                     and out["the_passes_differ"] and out["smoke_two_distinct_of_each_arm"])
    return out


def gate_g3(design: population.Design) -> dict[str, Any]:
    po, sc = populations(design), schedule(design)
    return {"what": "the population is §0's and the sessions §1's",
            "populations": po, "schedule": sc, "passes": po["passes"] and sc["passes"]}


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

def run_checks(suite: bool = True) -> Checks:
    design = population.build()
    return Checks(g1=gate_g1(design, suite=suite), g2=gate_g2(design),
                  g3=gate_g3(design), g4=plan.gate_signature(), design=design)


def report(checks: Checks) -> None:
    def mark(g: dict) -> str:
        return "PASS" if g["passes"] else "FAIL"

    g1, g2, g3, g4 = checks.g1, checks.g2, checks.g3, checks.g4
    s = g1["suite"]
    print(f"\nRR-g1 {mark(g1)}  PLAN_FIRST_MATCH.md's checks {g1['first_match_checks']}, its "
          f"design {g1['first_match_design']['passes']}, its verdicts departing "
          f"{g1['first_match_rows']['departing'] or 'none'}; the list over the space "
          f"{g1['the_list_over_the_space']['passes']}")
    print(f"      suite {'not run' if not s.get('ran') else s.get('result')}")
    dg = g2["digests"]
    print(f"RR-g2 {mark(g2)}  the closed plans' prompts {g2['closed_plans']['passes']}; "
          f"reasoning arms their quiet arms' {g2['reasoned_arms']['passes']}; texts "
          f"{g2['texts']['passes']}; builders {g2['builders']['passes']}; "
          f"{dg['distinct']} digests for {dg['texts']} texts, teeth "
          f"{dg['one_changed_character_moves_the_digest']}")
    po = g3["populations"]
    print(f"RR-g3 {mark(g3)}  prompts by arm {po['prompts']}, decisions {po['decisions']}; "
          f"schedule {g3['schedule']['passes']}")
    print(f"RR-g4 {'SIGNED' if g4['passes'] else 'UNSIGNED'}  {g4['found']} signature "
          f"line(s), {g4['unsigned']} blank")
    print(f"\nblocking checks: {'PASS' if checks.blocking_pass else 'FAIL'}")
