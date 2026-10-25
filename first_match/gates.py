"""
`FM-g1` to `FM-g4` of `PLAN_FIRST_MATCH.md` §6: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  FM-g1  The inputs reproduce themselves. The suite is green.
         `PLAN_QUEUE_ALONE.md`'s own `QA-g1` to `QA-g3` pass, called, and they
         hold the 29 rules to the truth of all 790 escalations. Its design,
         rebuilt, is `results_queue_alone/sample.json`'s. Its six verdicts come
         back from its two passes as `score.json` holds them, and its POST-RUN
         order reading comes back as `orders.json` holds it.
  FM-g2  The prompts are §5.1's. Every plain-arm prompt carries the digest
         `PLAN_QUEUE_ALONE.md` recorded for its plain arm at level 3. Every
         reasoning-arm prompt is the plain arm's on the same ticket, text for
         text. The naming arm's system prompt is the plain arm's with §5.1's
         line added and nothing else changed, its user message is the plain
         arm's, and its answer asks for `rule` and then `action`. No builder
         takes a record's row, one changed character moves a digest, and no
         digest stands for two texts. The requests themselves are checked
         through `tests/doubles.py`'s SDK double in `tests/test_first_match.py`,
         which `FM-g1`'s suite runs.
  FM-g3  The populations and the schedule are §0's and §1's: 171 prompts an
         arm on level 3's 320 decisions, each served once in every arm; each
         pass every prompt once, in its order rebuilt from `ORDER_SEED`; the
         smoke run two distinct prompts of each arm.
  FM-g4  The signature (`first_match/plan.py`). It does not block a dry run,
         which writes nothing; it blocks every write.

**This module is offline.** It reads labels for one thing only: to recompute
`PLAN_QUEUE_ALONE.md`'s verdicts and order reading from that plan's records,
and compare them with what those records hold. It sends nothing, and it prints
no figure of either: a check passes or fails.
"""

from __future__ import annotations

import difflib
import inspect
import json
from collections import Counter
from dataclasses import dataclass
from typing import Any

from queue_alone import ask as qask
from queue_alone import gates as qgates
from queue_alone import orders as qorders
from queue_alone import population as qpop
from queue_alone import prompts as qprompts
from queue_alone import rules as qrules
from queue_alone import score as qscore
from reuse.gates import run_suite

from . import plan, population, prompts

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
        return {"FM-g1": self.g1, "FM-g2": self.g2, "FM-g3": self.g3, "FM-g4": self.g4}


# ---------------------------------------------------------------------------
# FM-g1
# ---------------------------------------------------------------------------

def exact(x: Any) -> Any:
    """A record's content with every float dropped: a fraction kept as its text,
    so that what a check compares is counts and fractions only (§6)."""
    if isinstance(x, dict):
        if set(x) == {"fraction", "value"}:
            return x["fraction"]
        return {k: exact(v) for k, v in x.items() if not isinstance(v, float)}
    if isinstance(x, list):
        return [exact(v) for v in x if not isinstance(v, float)]
    return x


def queue_alone_passes() -> dict[int, dict[str, dict]]:
    """`PLAN_QUEUE_ALONE.md`'s two passes, by pass and ask id."""
    return {k: {r["id"]: r for r in json.loads(plan.queue_alone_ask(s).read_text())["rows"]}
            for k, s in ((1, "pass1"), (2, "pass2"))}


def queue_alone_rows(design: qpop.Design, by_pass: dict[int, dict[str, dict]]
                     ) -> dict[str, Any]:
    """`PLAN_QUEUE_ALONE.md`'s six verdicts, again, from its two passes."""
    recorded = json.loads(plan.queue_alone_score().read_text())["verdicts"]
    units = qscore.units(design, by_pass, qscore.labels())
    got = {"QA-a": qscore.adjudicate_anchor(
        qscore.anchor_prompts(design, by_pass, qscore.apply_records()))}
    got.update({spec.id: qscore.adjudicate(spec, units) for spec in qscore.SPECS})
    off = [rid for rid in sorted(recorded)
           if rid not in got or not qgates.same_verdict(got[rid], recorded[rid])]
    return {"rows": len(got), "departing": off, "passes": not off and len(got) == 6}


def queue_alone_orders(design: qpop.Design, by_pass: dict[int, dict[str, dict]]
                       ) -> dict[str, Any]:
    """`PLAN_QUEUE_ALONE.md`'s POST-RUN reading of where the order errors go,
    again, from its two passes: every count and fraction as `orders.json`
    holds it."""
    recorded = json.loads(plan.queue_alone_orders().read_text())
    units = qscore.units(design, by_pass, qscore.labels())
    answers = qorders.level3_answers(units, design)
    rs = qrules.rules()
    arms = {arm: qorders.arm_reading(answers[arm], rs) for arm in qorders.ARMS}
    spec = {arm: qorders.specificity(answers[arm], rs) for arm in qorders.ARMS}
    off = [k for k, mine in (("arms", arms), ("specificity", spec))
           if exact(json.loads(json.dumps(mine, default=str))) != exact(recorded[k])]
    return {"arms": list(arms), "departing": off, "passes": not off}


def gate_g1(design: population.Design, suite: bool = True) -> dict[str, Any]:
    qd = design.queue_alone
    checks = qgates.run_checks(suite=False)
    ok, why = qask.sample_matches(qd)
    by_pass = queue_alone_passes()
    rows = queue_alone_rows(qd, by_pass)
    orders = queue_alone_orders(qd, by_pass)
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": "PLAN_QUEUE_ALONE.md's checks pass, its design is its Stage A's, its "
                    "verdicts and its order reading come back from its passes; the suite "
                    "green",
            "queue_alone_checks": checks.blocking_pass,
            "queue_alone_design": {"passes": ok, "why": why},
            "queue_alone_rows": rows, "queue_alone_orders": orders, "suite": tests,
            "passes": (checks.blocking_pass and ok and rows["passes"] and orders["passes"]
                       and tests["passes"] is not False)}


# ---------------------------------------------------------------------------
# FM-g2
# ---------------------------------------------------------------------------

def plain_arm(design: population.Design) -> dict[str, Any]:
    """Every plain-arm prompt is `PLAN_QUEUE_ALONE.md`'s plain arm at level 3."""
    recorded = json.loads(plan.queue_alone_sample().read_text())["design"]["asks"]
    asks = design.asks_of(prompts.PLAIN)
    off = [a.id for a in asks
           if recorded.get(a.id, {}).get("digest") != a.digest
           or recorded[a.id]["arm"] != qprompts.PLAIN or recorded[a.id]["level"] != plan.LEVEL]
    theirs = sorted(i for i, r in recorded.items()
                    if r["arm"] == qprompts.PLAIN and r["level"] == plan.LEVEL)
    return {"prompts": len(asks), "not_queue_alones": off[:10],
            "every_one_of_theirs": sorted(a.id for a in asks) == theirs,
            "passes": not off and sorted(a.id for a in asks) == theirs}


def reasoning_arm(design: population.Design) -> dict[str, Any]:
    """Every reasoning-arm prompt is the plain arm's on the same ticket."""
    off = [a.id for a in design.asks_of(prompts.REASONING)
           if (a.system, a.user) != (design.asks[prompts.ask_id(prompts.PLAIN, a.ticket)].system,
                                     design.asks[prompts.ask_id(prompts.PLAIN, a.ticket)].user)]
    return {"prompts": len(design.asks_of(prompts.REASONING)), "not_the_plain_arms": off[:10],
            "passes": not off}


def changed_lines(a: str, b: str) -> list[tuple[str, list[str], list[str]]]:
    """Each place where the lines of `a` and `b` differ: the change, and the lines
    it takes from each side."""
    al, bl = a.splitlines(), b.splitlines()
    return [(tag, al[i1:i2], bl[j1:j2])
            for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, al, bl).get_opcodes()
            if tag != "equal"]


def texts(design: population.Design) -> dict[str, Any]:
    """§5.1's claims, read off the texts the package builds."""
    plain, naming = prompts.system_prompt(prompts.PLAIN), prompts.system_prompt(prompts.NAMING)
    case = design.asks_of(prompts.PLAIN)[0].case
    out: dict[str, Any] = {
        "plain_is_queue_alones": plain == qprompts.system_prompt(qprompts.PLAIN, plan.LEVEL),
        "plain_ends_with_its_answer": plain.endswith(prompts.PLAIN_ANSWER),
        "naming_adds_one_line": changed_lines(plain, naming)
        == [("insert", [], [prompts.NAMING_LINE])],
        "naming_answer_is_plain_answer_with_the_line": prompts.NAMING_ANSWER
        == prompts.PLAIN_ANSWER.replace("{\n", "{\n" + prompts.NAMING_LINE + "\n", 1),
        "the_rest_is_the_same": naming.replace(prompts.NAMING_LINE + "\n", "", 1) == plain,
        "users_are_the_plain_arms": len({prompts.user_message(arm, case)
                                         for arm in prompts.ARMS}) == 1
        and prompts.user_message(prompts.PLAIN, case)
        == qprompts.user_message(qprompts.PLAIN, case),
    }
    template = json.loads(prompts.NAMING_ANSWER.split("\n\n", 1)[1]
                          .replace('"<identificador de la regla que se aplica a este ticket>"',
                                   '""')
                          .replace('"<accion para este ticket>"', '""'))
    out["naming_asks_rule_then_action"] = list(template) == ["rule", "action"]
    out["the_identifiers"] = list(prompts.IDENTIFIERS) == [r.id for r in qrules.rules()]
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
    a = design.asks_of(prompts.NAMING)[0]
    moved = prompts.digest(a.system, a.user + " ") != a.digest
    return {"asks": len(design.asks), "texts": len(texts_), "distinct": len(seen),
            "collisions": collisions[:10], "one_changed_character_moves_the_digest": moved,
            "passes": not collisions and moved and len(seen) == len(texts_)}


def gate_g2(design: population.Design) -> dict[str, Any]:
    pa, ra = plain_arm(design), reasoning_arm(design)
    tx, bd, dg = texts(design), builders(), digests(design)
    return {"what": "the plain arm is PLAN_QUEUE_ALONE.md's at level 3, digest for digest; "
                    "the reasoning arm's texts are the plain arm's; the naming arm adds "
                    "§5.1's line and nothing else; no builder takes a row; the digests have "
                    "teeth. The requests are tests/test_first_match.py's, through the SDK "
                    "double",
            "plain_arm": pa, "reasoning_arm": ra, "texts": tx, "builders": bd, "digests": dg,
            "passes": all(x["passes"] for x in (pa, ra, tx, bd, dg))}


# ---------------------------------------------------------------------------
# FM-g3
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
    print(f"\nFM-g1 {mark(g1)}  PLAN_QUEUE_ALONE.md's checks {g1['queue_alone_checks']}, its "
          f"design {g1['queue_alone_design']['passes']}, its verdicts departing "
          f"{g1['queue_alone_rows']['departing'] or 'none'}, its order reading departing "
          f"{g1['queue_alone_orders']['departing'] or 'none'}")
    print(f"      suite {'not run' if not s.get('ran') else s.get('result')}")
    dg = g2["digests"]
    print(f"FM-g2 {mark(g2)}  plain arm {g2['plain_arm']['prompts']} prompts, "
          f"PLAN_QUEUE_ALONE.md's {g2['plain_arm']['passes']}; reasoning arm the plain "
          f"arm's {g2['reasoning_arm']['passes']}; §5.1's texts {g2['texts']['passes']}; "
          f"builders {g2['builders']['passes']}; {dg['distinct']} digests for {dg['texts']} "
          f"texts, teeth {dg['one_changed_character_moves_the_digest']}")
    po = g3["populations"]
    print(f"FM-g3 {mark(g3)}  prompts by arm {po['prompts']}, decisions {po['decisions']}; "
          f"schedule {g3['schedule']['passes']}")
    print(f"FM-g4 {'SIGNED' if g4['passes'] else 'UNSIGNED'}  {g4['found']} signature "
          f"line(s), {g4['unsigned']} blank")
    print(f"\nblocking checks: {'PASS' if checks.blocking_pass else 'FAIL'}")
