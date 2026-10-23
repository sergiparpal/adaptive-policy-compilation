"""
`X-g1` to `X-g4` of `PLAN_APPLY.md` §6: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  X-g1  The inputs reproduce themselves. The suite is green. Each of the twelve
        loop records replays with no departure through `fidelity.replay.check`:
        every outcome, winner and number of matched rules, every escalation's
        shown ids and kind, every edge verdict, every rule's counts. Its system
        prompt is its level's, byte for byte, with the digest
        `PLAN_MANUAL.md`'s Stage A recorded. The loop's choice of queue, pooled
        by level, comes back queue by queue as that plan's `G-g` holds it.
  X-g2  The prompts are the loop's. Every screen-arm prompt is the escalation's
        own, rebuilt, with the row's shown ids and kind, and never empty. Every
        ticket-arm prompt is v1's empty-base rendering. At each level the ticket
        arm's prompt for case 0's ticket is the empty-screen escalations'
        prompt. Level 0's prompts are `PLAN_SCREEN.md`'s on the tickets that
        plan asked. No builder takes a record's row, one changed shown rule
        moves a digest, and no digest stands for two texts. The requests
        themselves are checked through `tests/doubles.py`'s SDK double in
        `tests/test_apply.py`, which `X-g1`'s suite runs.
  X-g3  The populations and the schedule are §0's and §1's: the decisions, the
        conflict screens, the empty screens and the ticket prompts by level;
        each pass every ask once, in its order rebuilt from `ORDER_SEED`; the
        smoke run one ask of each arm at each level.
  X-g4  The signature (`apply/plan.py`). It does not block a dry run, which
        writes nothing; it blocks every write.

**This module is offline.** It reads the loop records' labels for one thing
only, the loop's choice of queue against `PLAN_MANUAL.md`'s `G-g`, and sends
nothing.
"""

from __future__ import annotations

import hashlib
import inspect
import json
from collections import Counter
from dataclasses import dataclass, replace
from typing import Any

from fidelity import prompts as fprompts
from fidelity.replay import check as replay_check
from manual import instrument as MI
from reuse.gates import run_suite

from . import plan, population, prompts

# What a builder may be handed. A row of a record carries the truth (rule B).
BUILDER_PARAMETERS = {"screen_ask": ("ask_id", "level", "prompt"),
                      "ticket_ask": ("ask_id", "level", "case")}


@dataclass
class Checks:
    xg1: dict
    xg2: dict
    xg3: dict
    xg4: dict
    design: population.Design

    @property
    def blocking_pass(self) -> bool:
        return self.xg1["passes"] and self.xg2["passes"] and self.xg3["passes"]

    def summary(self) -> dict[str, Any]:
        """What a record carries about the checks it was written behind."""
        return {"X-g1": self.xg1, "X-g2": self.xg2, "X-g3": self.xg3, "X-g4": self.xg4}


# ---------------------------------------------------------------------------
# X-g1
# ---------------------------------------------------------------------------

def manual_prompt_digests() -> dict[int, str]:
    rec = json.loads(plan.manual_sample().read_text())
    return {int(lv): v["sha256"] for lv, v in rec["design"]["prompts"]["loop"].items()}


def replays() -> dict[str, Any]:
    published = manual_prompt_digests()
    runs = []
    for lv in plan.LEVELS:
        for rep in range(1, plan.REPS + 1):
            rec = population.record(lv, rep)
            got = replay_check(rec, list(population.corpus()), population.space())
            departures = (got["decisions_departing"] + got["screens_departing"]
                          + got["edge_problems"] + got["rules_whose_counts_depart"])
            sp = rec["system_prompt"]
            digest = hashlib.sha256(sp.encode()).hexdigest()
            row = {"level": lv, "rep": rep, "departures": departures,
                   "first_problems": [p for p in got["first_problems"]
                                      if "system prompt" not in p],
                   "system_prompt_is_the_levels": sp == prompts.system_prompt(lv),
                   "digest_is_plan_manuals": digest == published[lv],
                   "record_says_the_same": rec.get("prompt_sha256") == published[lv]}
            row["passes"] = (departures == 0 and row["system_prompt_is_the_levels"]
                             and row["digest_is_plan_manuals"]
                             and row["record_says_the_same"])
            runs.append(row)
    return {"runs": runs, "passes": all(r["passes"] for r in runs)}


def loop_choice() -> dict[str, Any]:
    """The loop's choice of queue by level, pooled over its runs, against
    `PLAN_MANUAL.md`'s `G-g`. `manual.instrument.proposals` counts it, called."""
    published = json.loads(plan.manual_score().read_text())["G-g"]["prop_by_level"]
    out = {}
    for lv in plan.LEVELS:
        right = of = 0
        by: dict[str, list[int]] = {}
        for rep in range(1, plan.REPS + 1):
            got = MI.proposals(population.record(lv, rep))
            right += got["right"]
            of += got["escalations"]
            for q, c in got["by_queue"].items():
                acc = by.setdefault(q, [0, 0])
                acc[0] += c["right"]
                acc[1] += c["of"]
        pub = published[str(lv)]
        out[lv] = {"fraction": f"{right}/{of}", "published": pub["pooled"]["fraction"],
                   "by_queue_agrees": by == {q: list(v) for q, v in pub["by_queue"].items()}}
        out[lv]["passes"] = out[lv]["fraction"] == out[lv]["published"] \
            and out[lv]["by_queue_agrees"]
    return {"levels": out, "passes": all(v["passes"] for v in out.values())}


def gate_xg1(suite: bool = True) -> dict[str, Any]:
    rp, lc = replays(), loop_choice()
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": "the twelve loop records replay with no departure, under their "
                    "level's system prompt, and the loop's choice of queue is "
                    "PLAN_MANUAL.md's; the suite green",
            "replays": rp, "loop_choice": lc, "suite": tests,
            "passes": rp["passes"] and lc["passes"] and tests["passes"] is not False}


# ---------------------------------------------------------------------------
# X-g2
# ---------------------------------------------------------------------------

def screens(design: population.Design) -> dict[str, Any]:
    systems = {lv: population.record(lv, 1)["system_prompt"] for lv in plan.LEVELS}
    departing, empty_decisions, wrong_empty, not_birth = [], [], [], []
    for i, e in design.escalations.items():
        if (tuple(e.prompt.shown_ids), e.prompt.screen) != e.recorded[:2] \
                or not e.recorded[2]:
            departing.append(i)
        if not e.has_screen and e.prompt.base_text != prompts.EMPTY_BASE:
            wrong_empty.append(i)
    for i, e in design.decisions.items():
        a = design.asks[population.screen_ask_id(i)]
        if not a.shown_ids:
            empty_decisions.append(i)
        if (a.case, a.base_text, a.system) != (e.prompt.case, e.prompt.base_text,
                                                systems[e.level]):
            not_birth.append(i)
    return {"escalations": len(design.escalations), "departing": departing[:10],
            "decisions_with_an_empty_screen": empty_decisions[:10],
            "empty_screens_not_v1s_empty_base": wrong_empty[:10],
            "asks_not_the_escalations_prompt": not_birth[:10],
            "passes": not (departing or empty_decisions or wrong_empty or not_birth)}


def tickets(design: population.Design) -> dict[str, Any]:
    asks = [a for a in design.asks.values() if a.arm == prompts.TICKET]
    not_alone = [a.id for a in asks if fprompts.check_ticket_only(a)]
    # Teeth: case 0's ticket at each level is, byte for byte, the prompt every
    # empty-screen escalation of that level was asked.
    case0 = {}
    for i in design.empty:
        e = design.escalations[i]
        a = design.asks[population.ticket_ask_id(e.level, e.ticket)]
        case0[i] = (a.system, a.user) == (population.record(e.level, e.run)["system_prompt"],
                                          e.prompt.user)
    # Level 0 is PLAN_SCREEN.md's ticket-only prompt, on the tickets it asked.
    screen = json.loads(plan.SCREEN_TICKET_ONLY.read_text())
    theirs = {}
    for r in screen["rows"]:
        if r.get("idx") is not None:
            theirs.setdefault(population.ticket_of(population.corpus()[r["idx"]]),
                              set()).add(r["digest"])
    shared = {t: design.asks[population.ticket_ask_id(0, t)].digest
              for t in theirs if population.ticket_ask_id(0, t) in design.asks}
    same = sum(1 for t, d in shared.items() if theirs[t] == {d})
    return {"ticket_asks": len(asks), "not_the_empty_base": not_alone[:10],
            "case_0_is_the_empty_screens_prompt": case0,
            "shared_with_plan_screen": len(shared), "same_digest": same,
            "passes": (not not_alone and case0 and all(case0.values())
                       and len(shared) == plan.SHARED_WITH_SCREEN
                       and same == len(shared))}


def builders() -> dict[str, Any]:
    got = {name: tuple(inspect.signature(getattr(prompts, name)).parameters)
           for name in BUILDER_PARAMETERS}
    return {"parameters": got, "passes": got == BUILDER_PARAMETERS}


def digests(design: population.Design) -> dict[str, Any]:
    texts: dict[str, set[tuple[str, str]]] = {}
    for a in design.asks.values():
        texts.setdefault(a.digest, set()).add((a.system, a.user))
    collisions = [d for d, t in texts.items() if len(t) > 1]
    # Asks with the same text are not collisions: early in a run the base can
    # be the same in two runs, and each escalation is still its own decision.
    per_text = Counter((a.system, a.user) for a in design.asks.values())
    # Teeth: one shown rule changed in one prompt moves its digest.
    a = next(x for x in design.asks.values() if x.arm == prompts.SCREEN)
    lines = a.base_text.splitlines()
    changed = replace(a, base_text="\n".join([lines[0], lines[1] + " "] + lines[2:]) + "\n")
    moved = changed.digest != a.digest
    plural = [i for i in design.decisions
              if prompts.plurality(design.asks[population.screen_ask_id(i)]) is None]
    return {"asks": len(design.asks), "distinct_texts": len(texts),
            "collisions": collisions[:10],
            "asks_sharing_a_text_with_another": sum(n for n in per_text.values() if n > 1),
            "one_changed_rule_moves_the_digest": moved,
            "decisions_without_a_plurality": plural[:10],
            "passes": not collisions and moved and not plural}


def gate_xg2(design: population.Design) -> dict[str, Any]:
    sc, tk, bd, dg = screens(design), tickets(design), builders(), digests(design)
    return {"what": "the screen arm is each escalation's own prompt, the ticket arm v1's "
                    "empty base under the level's prompt, PLAN_SCREEN.md's at level 0; "
                    "no builder takes a row; the digests have teeth. The requests are "
                    "tests/test_apply.py's, through the SDK double",
            "screens": sc, "tickets": tk, "builders": bd, "digests": dg,
            "passes": sc["passes"] and tk["passes"] and bd["passes"] and dg["passes"]}


# ---------------------------------------------------------------------------
# X-g3
# ---------------------------------------------------------------------------

def populations(design: population.Design) -> dict[str, Any]:
    decisions = {lv: len(design.decisions_at(lv)) for lv in plan.LEVELS}
    conflicts = {lv: sum(1 for e in design.decisions_at(lv)
                         if e.prompt.screen == prompts.CONFLICT) for lv in plan.LEVELS}
    ticket_asks = Counter(a.level for a in design.asks.values() if a.arm == prompts.TICKET)
    screen_asks = sum(1 for a in design.asks.values() if a.arm == prompts.SCREEN)
    out = {"decisions": decisions, "conflict_screens": conflicts,
           "empty_screens": len(design.empty),
           "ticket_prompts": {lv: ticket_asks[lv] for lv in plan.LEVELS},
           "screen_prompts": screen_asks}
    out["passes"] = (decisions == plan.DECISIONS and conflicts == plan.CONFLICT_DECISIONS
                     and out["empty_screens"] == plan.EMPTY_SCREENS
                     and out["ticket_prompts"] == plan.TICKET_PROMPTS
                     and screen_asks == sum(plan.DECISIONS.values()))
    return out


def schedule(design: population.Design) -> dict[str, Any]:
    rebuilt = population.sessions_for(design.decisions, design.asks)
    every = sorted(design.asks)
    passes = {s: sorted(design.sessions[s]) == every for s in plan.SESSIONS[1:]}
    smoke = design.sessions["smoke"]
    per_level = Counter((design.asks[i].level, design.asks[i].arm) for i in smoke)
    out = {
        "rebuilt_from_the_seed": rebuilt == design.sessions,
        "each_pass_holds_every_ask_once": passes,
        "the_passes_differ": design.sessions["pass1"] != design.sessions["pass2"],
        "smoke": smoke,
        "smoke_one_of_each_arm_at_each_level": (
            len(smoke) == len(set(smoke)) == 2 * len(plan.LEVELS)
            and all(per_level[(lv, arm)] == plan.SMOKE_PER_ARM_AND_LEVEL
                    for lv in plan.LEVELS for arm in prompts.ARMS)),
    }
    out["passes"] = (out["rebuilt_from_the_seed"] and all(passes.values())
                     and out["the_passes_differ"]
                     and out["smoke_one_of_each_arm_at_each_level"])
    return out


def gate_xg3(design: population.Design) -> dict[str, Any]:
    po, sc = populations(design), schedule(design)
    return {"what": "the populations are §0's and the sessions §1's",
            "populations": po, "schedule": sc, "passes": po["passes"] and sc["passes"]}


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

def run_checks(suite: bool = True) -> Checks:
    design = population.build()
    return Checks(xg1=gate_xg1(suite=suite), xg2=gate_xg2(design), xg3=gate_xg3(design),
                  xg4=plan.gate_signature(), design=design)


def report(checks: Checks) -> None:
    def mark(g: dict) -> str:
        return "PASS" if g["passes"] else "FAIL"

    g1, g2, g3, g4 = checks.xg1, checks.xg2, checks.xg3, checks.xg4
    bad = [f"L{r['level']}r{r['rep']}" for r in g1["replays"]["runs"] if not r["passes"]]
    print(f"\nX-g1 {mark(g1)}  twelve replays, departing {bad or 'none'}; the loop's "
          "choice by level " + ", ".join(f"L{lv} {v['fraction']} ({v['published']})"
                                         for lv, v in g1["loop_choice"]["levels"].items()))
    s = g1["suite"]
    print(f"      suite {'not run' if not s.get('ran') else s.get('result')}")
    tk, dg = g2["tickets"], g2["digests"]
    print(f"X-g2 {mark(g2)}  screens {g2['screens']['passes']} over "
          f"{g2['screens']['escalations']} escalations; ticket arm "
          f"{tk['ticket_asks']} asks, case 0 {all(tk['case_0_is_the_empty_screens_prompt'].values())}, "
          f"PLAN_SCREEN.md's digest on {tk['same_digest']} of {tk['shared_with_plan_screen']}; "
          f"builders {g2['builders']['passes']}; {dg['distinct_texts']} texts for "
          f"{dg['asks']} asks, collisions {len(dg['collisions'])}, teeth "
          f"{dg['one_changed_rule_moves_the_digest']}")
    po = g3["populations"]
    print(f"X-g3 {mark(g3)}  decisions {po['decisions']}, conflict screens "
          f"{po['conflict_screens']}, empty {po['empty_screens']}, ticket prompts "
          f"{po['ticket_prompts']}; schedule {g3['schedule']['passes']}")
    print(f"X-g4 {'SIGNED' if g4['passes'] else 'UNSIGNED'}  {g4['found']} signature "
          f"line(s), {g4['unsigned']} blank")
    print(f"\nblocking checks: {'PASS' if checks.blocking_pass else 'FAIL'}")
