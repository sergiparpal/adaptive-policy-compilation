"""
`QA-g1` to `QA-g4` of `PLAN_QUEUE_ALONE.md` §6: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  QA-g1  The inputs reproduce themselves. The suite is green. `PLAN_APPLY.md`'s
         own `X-g1` to `X-g3` pass, called. Its design, rebuilt, is
         `results_apply/sample.json`'s, and its six verdicts come back from its
         two passes as `results_apply/score.json` holds them. The 29 rules,
         read from level 3's frozen text by first match, give every escalated
         ticket the truth its loop record holds.
  QA-g2  The prompts are §5.1's. Every rule-arm prompt carries the digest
         `PLAN_APPLY.md` recorded for it. The plain and impasse system prompts
         differ in exactly §5.1's two sentences, and their user messages in the
         first line; the impasse arm's message is the rule arm's without the
         empty-base line. v1's block is cut from v1, once, and the manual's
         block is `manual.prompts.block`'s, at levels 1 to 3 and only there.
         The answer asks for `action` and nothing else. No builder takes a
         record's row, one changed character moves a digest, and no digest
         stands for two texts. The requests themselves are checked through
         `tests/doubles.py`'s SDK double in `tests/test_queue_alone.py`, which
         `QA-g1`'s suite runs.
  QA-g3  The populations and the schedule are §0's and §1's: 676 prompts an
         arm, 275, 81, 149 and 171 by level, on `PLAN_APPLY.md`'s decisions;
         each pass every prompt once, in its order rebuilt from `ORDER_SEED`;
         the smoke run one prompt of each arm at each level.
  QA-g4  The signature (`queue_alone/plan.py`). It does not block a dry run,
         which writes nothing; it blocks every write.

**This module is offline.** It reads labels for two things only: to hold the 29
rules to the truth, and to recompute `PLAN_APPLY.md`'s verdicts. It sends
nothing.
"""

from __future__ import annotations

import difflib
import inspect
import json
from collections import Counter
from dataclasses import dataclass, replace
from typing import Any

from apply import ask as apply_ask
from apply import gates as apply_gates
from apply import population as apop
from apply import score as ascore
from manual import prompts as mprompts
from reuse.gates import run_suite
from rung2.proposers2 import SYSTEM_PROMPT_V1

from . import plan, population, prompts, rules

# What a builder may be handed. A row of a record carries the truth (rule B).
BUILDER_PARAMETERS = {"ask": ("arm", "level", "ticket", "case"),
                      "system_prompt": ("arm", "level"),
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
        return {"QA-g1": self.g1, "QA-g2": self.g2, "QA-g3": self.g3, "QA-g4": self.g4}


# ---------------------------------------------------------------------------
# QA-g1
# ---------------------------------------------------------------------------

def same_verdict(got: dict[str, Any], theirs: dict[str, Any]) -> bool:
    """A row as Stage C recorded it: its value and runs exactly, the decisions
    it read, its verdict and its thin label. The standard error is a float and
    labels only, so it is left to `thin`."""
    def fr(d: dict | None) -> str | None:
        return d["fraction"] if d else None
    return (fr(got.get("value")) == fr(theirs.get("value"))
            and {k: fr(v) for k, v in got.get("per_run", {}).items()}
            == {k: fr(v) for k, v in theirs.get("per_run", {}).items()}
            and got.get("read") == theirs.get("read")
            and got.get("verdict") == theirs.get("verdict")
            and got.get("thin") == theirs.get("thin"))


def apply_rows(design: apop.Design) -> dict[str, Any]:
    """`PLAN_APPLY.md`'s six verdicts, again, from its two passes."""
    recorded = json.loads(plan.apply_score().read_text())["verdicts"]
    by_pass = {k: {r["id"]: r for r in json.loads(plan.apply_ask(s).read_text())["rows"]}
               for k, s in ((1, "pass1"), (2, "pass2"))}
    units = ascore.units(design, by_pass, ascore.labels())
    off = [spec.id for spec in ascore.SPECS
           if not same_verdict(ascore.adjudicate(spec, units), recorded[spec.id])]
    return {"rows": len(ascore.SPECS), "departing": off, "passes": not off}


def the_rules(design: apop.Design) -> dict[str, Any]:
    """The 29 rules from level 3's text give every escalated ticket its truth."""
    rs = rules.rules()
    lab = ascore.labels()
    ids = [r.id for r in rs]
    wrong = [i for i, e in sorted(design.escalations.items())
             if rules.first_queue(e.prompt.case.as_dict(), rs) != lab[i]["y"]]
    out = {"rules": len(rs), "in_order": ids == [f"H{k:02d}" for k in range(1, 30)],
           "escalations": len(design.escalations), "first_match_not_truth": wrong[:10]}
    out["passes"] = len(rs) == 29 and out["in_order"] and not wrong
    return out


def gate_g1(design: population.Design, suite: bool = True) -> dict[str, Any]:
    checks = apply_gates.run_checks(suite=False)
    ok, why = apply_ask.sample_matches(design.apply)
    rows = apply_rows(design.apply)
    rl = the_rules(design.apply)
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": "PLAN_APPLY.md's checks pass, its design is its Stage A's and its "
                    "verdicts come back; the 29 rules read from level 3's text give "
                    "every escalated ticket its truth; the suite green",
            "apply_checks": checks.blocking_pass, "apply_design": {"passes": ok, "why": why},
            "apply_rows": rows, "rules": rl, "suite": tests,
            "passes": (checks.blocking_pass and ok and rows["passes"] and rl["passes"]
                       and tests["passes"] is not False)}


# ---------------------------------------------------------------------------
# QA-g2
# ---------------------------------------------------------------------------

def rule_arm(design: population.Design) -> dict[str, Any]:
    recorded = json.loads(plan.apply_sample().read_text())["design"]["asks"]
    asks = [a for a in design.asks.values() if a.arm == prompts.RULE]
    off = [a.id for a in asks
           if recorded.get(a.id, {}).get("digest") != a.digest
           or recorded[a.id]["arm"] != "ticket"]
    return {"prompts": len(asks), "not_plan_applys": off[:10], "passes": not off}


def changed_lines(a: str, b: str) -> list[int]:
    """The line numbers of `a` that differ from `b`, line for line."""
    out = []
    for tag, i1, i2, _, _ in difflib.SequenceMatcher(None, a.splitlines(),
                                                     b.splitlines()).get_opcodes():
        if tag != "equal":
            out.extend(range(i1, i2))
    return out


def texts() -> dict[str, Any]:
    """§5.1's claims, read off the texts the package builds."""
    out: dict[str, Any] = {}
    block = prompts.v1_block()
    out["v1_block_once_in_v1"] = SYSTEM_PROMPT_V1.count(block) == 1
    by_level = {}
    for lv in plan.LEVELS:
        q, i = prompts.system_prompt(prompts.PLAIN, lv), prompts.system_prompt(prompts.IMPASSE, lv)
        manual = mprompts.block(lv) if lv else None
        by_level[lv] = {
            "plain_and_impasse_differ_in_two_lines": changed_lines(q, i) == [0, 2],
            "the_rest_is_the_same": q.replace(prompts.PLAIN_HEAD, prompts.IMPASSE_HEAD, 1) == i,
            "v1_block_once": q.count(block) == 1 and i.count(block) == 1,
            "manual_block": (q.count(manual) == 1 and i.count(manual) == 1) if manual
            else mprompts.MANUAL_HEADER not in q + i,
            "answer_is_action_alone": q.endswith(prompts.ANSWER) and i.endswith(prompts.ANSWER),
        }
    out["levels"] = by_level
    design = population.build()
    case = next(iter(design.asks.values())).case
    plain, impasse, rule = (prompts.user_message(arm, case) for arm in
                            (prompts.PLAIN, prompts.IMPASSE, prompts.RULE))
    out["users"] = {
        "plain_and_impasse_differ_in_the_first_line": changed_lines(plain, impasse) == [0],
        "rule_is_the_empty_base_line_then_impasse":
            rule == prompts.EMPTY_BASE + "\n" + impasse,
    }
    out["answer_names_action_alone"] = (
        json.loads(prompts.ANSWER.split("\n\n", 1)[1].replace('"<accion para este ticket>"',
                                                             '""')) == {"action": ""})
    out["passes"] = (out["v1_block_once_in_v1"] and out["answer_names_action_alone"]
                     and all(all(v.values()) for v in by_level.values())
                     and all(out["users"].values()))
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
    a = next(x for x in design.asks.values() if x.arm == prompts.PLAIN)
    moved = prompts.digest(a.system, a.user + " ") != a.digest
    return {"asks": len(design.asks), "distinct": len(seen), "collisions": collisions[:10],
            "one_changed_character_moves_the_digest": moved,
            "passes": not collisions and moved and len(seen) == len(design.asks)}


def gate_g2(design: population.Design) -> dict[str, Any]:
    ra, tx, bd, dg = rule_arm(design), texts(), builders(), digests(design)
    return {"what": "the rule arm is PLAN_APPLY.md's ticket arm, digest for digest; the "
                    "new arms are §5.1's and differ as it says; no builder takes a row; "
                    "the digests have teeth. The requests are tests/test_queue_alone.py's, "
                    "through the SDK double",
            "rule_arm": ra, "texts": tx, "builders": bd, "digests": dg,
            "passes": ra["passes"] and tx["passes"] and bd["passes"] and dg["passes"]}


# ---------------------------------------------------------------------------
# QA-g3
# ---------------------------------------------------------------------------

def populations(design: population.Design) -> dict[str, Any]:
    per = Counter((a.arm, a.level) for a in design.asks.values())
    prompts_by = {arm: {lv: per[(arm, lv)] for lv in plan.LEVELS} for arm in prompts.ARMS}
    decisions = {lv: len(design.apply.decisions_at(lv)) for lv in plan.LEVELS}
    out = {"prompts": prompts_by, "decisions": decisions}
    out["passes"] = (all(v == plan.TICKET_PROMPTS for v in prompts_by.values())
                     and decisions == plan.DECISIONS)
    return out


def schedule(design: population.Design) -> dict[str, Any]:
    rebuilt = population.sessions_for(design.asks)
    every = sorted(design.asks)
    passes = {s: sorted(design.sessions[s]) == every for s in plan.SESSIONS[1:]}
    smoke = design.sessions["smoke"]
    per = Counter((design.asks[i].level, design.asks[i].arm) for i in smoke)
    out = {
        "rebuilt_from_the_seed": rebuilt == design.sessions,
        "each_pass_holds_every_prompt_once": passes,
        "the_passes_differ": design.sessions["pass1"] != design.sessions["pass2"],
        "smoke": smoke,
        "smoke_one_of_each_arm_at_each_level": (
            len(smoke) == len(set(smoke)) == len(prompts.ARMS) * len(plan.LEVELS)
            and all(per[(lv, arm)] == plan.SMOKE_PER_ARM_AND_LEVEL
                    for lv in plan.LEVELS for arm in prompts.ARMS)),
    }
    out["passes"] = (out["rebuilt_from_the_seed"] and all(passes.values())
                     and out["the_passes_differ"]
                     and out["smoke_one_of_each_arm_at_each_level"])
    return out


def gate_g3(design: population.Design) -> dict[str, Any]:
    po, sc = populations(design), schedule(design)
    return {"what": "the populations are §0's and the sessions §1's",
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
    print(f"\nQA-g1 {mark(g1)}  PLAN_APPLY.md's checks {g1['apply_checks']}, its design "
          f"{g1['apply_design']['passes']}, its verdicts departing "
          f"{g1['apply_rows']['departing'] or 'none'}; the 29 rules give "
          f"{g1['rules']['escalations']} escalations their truth: {g1['rules']['passes']}")
    print(f"      suite {'not run' if not s.get('ran') else s.get('result')}")
    dg = g2["digests"]
    print(f"QA-g2 {mark(g2)}  rule arm {g2['rule_arm']['prompts']} prompts, PLAN_APPLY.md's "
          f"{g2['rule_arm']['passes']}; §5.1's texts {g2['texts']['passes']}; builders "
          f"{g2['builders']['passes']}; {dg['distinct']} digests for {dg['asks']} prompts, "
          f"teeth {dg['one_changed_character_moves_the_digest']}")
    po = g3["populations"]
    print(f"QA-g3 {mark(g3)}  prompts by arm {po['prompts'][prompts.RULE]}, decisions "
          f"{po['decisions']}; schedule {g3['schedule']['passes']}")
    print(f"QA-g4 {'SIGNED' if g4['passes'] else 'UNSIGNED'}  {g4['found']} signature "
          f"line(s), {g4['unsigned']} blank")
    print(f"\nblocking checks: {'PASS' if checks.blocking_pass else 'FAIL'}")
