"""
`HV-g1` to `HV-g4` of `PLAN_HALVES.md` §6: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  HV-g1  The texts. `e`'s prompts are `PLAN_REASONED_RULE.md`'s arm `w`'s,
         digest for digest, at every ticket that arm asked, under the rule
         arm's own system prompt, which is the loop's. `v`'s messages are the
         loop's first call, `reasoned_loop.protocol.messages_for`, at every
         ticket, and every loop record `whole/paragraph.py` reads sent the
         loop's system prompt and its group's paragraph. `h` and `o` are cut and
         joined from `v` and `e` exactly as §2.1 says, and no paragraph names a
         queue or a rule. Every arm's message differs from `v`'s in the
         paragraph alone, and every repetition asks its prompt's messages. No
         builder takes a row, and the digests have teeth. The suite is green.
  HV-g2  The request and the instrument. The request is the loop's first
         call's, `placement.protocol.request_with` over the loop's request, with
         DeepInfra's pin, and `PLAN_PLACEMENT.md`'s and `PLAN_WHOLE.md`'s v1c
         records carry the same model, temperature, settings and pin. No module
         on the asker's path names a label, in a name or a string literal, as
         `N-g2` reads them. And the classes give back `whole/paragraph.py`'s
         record from the closed answers, count for count, before they read a
         new one.
  HV-g3  The design. The 136 tickets come back from the closed records: the
         rule arm's tickets a reasoning loop's first call met, and the rarest
         queue's tickets it did not ask, whose seven are the corpus's tickets of
         `ONCALL_ESCALATION` by level 3's list. 544 prompts, 136 an arm; each
         pass every prompt once, in its order rebuilt from `ORDER_SEED`; the
         rarest queue's session its 28 prompts four times each; the smoke run
         two distinct prompts of each arm, outside the seven. The partial
         files are ignored by git; the guard in front of every paid record is
         pinned by `tests/test_writer_lists.py`.
  HV-g4  The signature (`halves/plan.py`). It does not block a dry run, which
         writes nothing; it blocks every write.

**This module is offline.** It reads the closed records' answers for one thing
only: to hold the classes to the record that published them, which
`whole/paragraph.py` did with the same functions. It reads the rarest queue's
tickets off level 3's list over the space, through `whole.references`, never the
oracle. It sends nothing, and it prints no figure of any plan: a check passes or
fails.
"""

from __future__ import annotations

import ast
import inspect
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from harness.domain import ACTIONS

from blind import protocol as v2b
from escalations import gates as esc_gates
from placement import oncall as PO
from placement import protocol as pl_protocol
from queue_alone import prompts as qprompts
from reasoned_loop import governed as gv
from reasoned_loop import protocol as p
from reuse.gates import run_suite
from rung2.proposers2 import render_base_v1
from whole import paragraph as W
from whole import protocol as wprotocol
from whole import references

from . import plan, population, prompts

HERE = Path(__file__).resolve().parent
REPO = HERE.parent

# What a builder may be handed. A row of a record carries the label (rule B).
BUILDER_PARAMETERS = {"ask": ("arm", "ticket", "case", "rep"),
                      "paragraph": ("arm",),
                      "system_prompt": ("arm",),
                      "user_message": ("arm", "case")}

# The modules on the asker's path, and the names they may not carry. These are
# `PLAN_SPOTCHECK.md`'s `N-g2` names: the label's, and the record fields that
# carry it or the system's own decision.
ASKER_PATH = ("plan.py", "prompts.py", "population.py", "ask.py")
FORBIDDEN = esc_gates.TRUTH_NAMES | {"truth_rule", "correct", "proposal_action_correct",
                                     "predicted"}
RULE_ID = re.compile(r"\b(?:H\d\d|R\d{4})\b")


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
        return {"HV-g1": self.g1, "HV-g2": self.g2, "HV-g3": self.g3, "HV-g4": self.g4}


def loop_records() -> dict[str, list[tuple[str, dict]]]:
    return {g: [(t, json.loads(path.read_text())) for t, path in runs]
            for g, runs in W.loop_paths().items()}


# ---------------------------------------------------------------------------
# HV-g1: the texts
# ---------------------------------------------------------------------------

def e_is_the_rule_arms(design: population.Design) -> dict[str, Any]:
    """At every ticket `PLAN_REASONED_RULE.md`'s arm `w` asked, `e`'s prompt
    carries the digest that arm recorded there, in both passes."""
    recorded: dict[int, set[str]] = {}
    for r in W.rule_arm_rows():
        recorded.setdefault(r["ticket"], set()).add(r["digest"])
    shared = [t for t in design.tickets if t in recorded]
    off = [t for t in shared
           if recorded[t] != {design.asks[prompts.ask_id(prompts.EMPTY, t)].digest}]
    system = qprompts.system_prompt(qprompts.RULE, plan.LEVEL) == prompts.SYSTEM_PROMPT
    return {"rule_arm_tickets": len(recorded), "shared": len(shared), "departing": off[:10],
            "the_rule_arms_system_prompt_is_the_loops": system,
            "passes": (not off and system and len(recorded) == plan.RULE_ARM_TICKETS
                       and len(shared) == plan.SHARED)}


def v_is_the_loops(design: population.Design,
                   loops: dict[str, list[tuple[str, dict]]]) -> dict[str, Any]:
    """`v`'s messages are the loop's first call at every ticket, and every loop
    record sent the loop's system prompt and its group's paragraph."""
    off = [t for t in design.tickets
           if design.asks[prompts.ask_id(prompts.V2B, t)].messages()
           != p.messages_for(design.asks[prompts.ask_id(prompts.V2B, t)].case)]
    sent = {"blind_base": W.sha16(prompts.BLIND_BASE),
            "whole_base": W.sha16(wprotocol.WHOLE_BASE)}
    wrong = [f"{g} {t}" for g, runs in loops.items() for t, rec in runs
             if (rec.get("texts_sha16") or {}).get("system_prompt")
             != W.sha16(prompts.SYSTEM_PROMPT)
             or (rec.get("texts_sha16") or {}).get(W.PARAGRAPH[g]) != sent[W.PARAGRAPH[g]]]
    return {"tickets": len(design.tickets), "departing": off[:10],
            "records": sum(len(r) for r in loops.values()), "records_departing": wrong,
            "passes": not off and not wrong and set(loops) == set(plan.LOOP_GROUPS)}


def the_halves() -> dict[str, Any]:
    """§2.1's texts, cut and joined as the plan says, naming no queue and no
    rule."""
    e, v, h, o = (prompts.PARAGRAPHS[a] for a in prompts.ARMS)
    cut = v.index(prompts.SEMICOLON)
    four = (e, v, h, o)
    out = {
        "e_is_v1s_empty_base": e == render_base_v1([], "") == qprompts.EMPTY_BASE,
        "v_is_v2bs": v == v2b.BLIND_BASE == p.BLIND_BASE,
        "h_is_v_up_to_its_semicolon": h == v[:cut] + ".\n",
        "o_is_e_with_vs_clause": o == e[:-2] + ";\n" + v[cut + len(prompts.SEMICOLON):],
        "v_comes_back_from_h_and_o": h[:-2] + prompts.SEMICOLON + o.split(";\n", 1)[1] == v,
        "the_four_differ": len(set(four)) == 4,
        "each_ends_its_line": all(x.endswith("\n") for x in four),
        "none_names_a_queue": not any(q in x for q in ACTIONS for x in four),
        "none_names_a_rule": not any(RULE_ID.search(x) for x in four),
    }
    out["passes"] = all(out.values())
    return out


def one_paragraph_apart(design: population.Design) -> dict[str, Any]:
    """At every ticket each arm sends the loop's system prompt, and a user
    message that is `v`'s with the paragraph replaced. Every repetition asks
    its prompt's messages."""
    off = []
    for t in design.tickets:
        rest = design.asks[prompts.ask_id(prompts.V2B, t)].user.removeprefix(prompts.BLIND_BASE)
        for arm in prompts.ARMS:
            a = design.asks[prompts.ask_id(arm, t)]
            if (a.system != prompts.SYSTEM_PROMPT or not a.user.startswith(prompts.PARAGRAPHS[arm])
                    or a.user.removeprefix(prompts.PARAGRAPHS[arm]) != rest):
                off.append(a.id)
    reps = [a for a in design.asks.values() if a.rep]
    unlike = [a.id for a in reps if a.messages() != design.asks[a.prompt].messages()]
    return {"departing": off[:10], "repetitions": len(reps), "repetitions_departing": unlike[:10],
            "passes": not off and not unlike}


def builders() -> dict[str, Any]:
    got = {name: tuple(inspect.signature(getattr(prompts, name)).parameters)
           for name in BUILDER_PARAMETERS}
    return {"parameters": got, "passes": got == BUILDER_PARAMETERS}


def digests(design: population.Design) -> dict[str, Any]:
    seen: dict[str, set[tuple[str, str]]] = {}
    for a in design.asks.values():
        seen.setdefault(a.digest, set()).add((a.system, a.user))
    collisions = [d for d, t in seen.items() if len(t) > 1]
    a = design.asks[prompts.ask_id(prompts.HIDDEN, design.tickets[0])]
    moved = prompts.digest(a.system, a.user + " ") != a.digest
    return {"digests": len(seen), "collisions": collisions[:10],
            "one_changed_character_moves_the_digest": moved,
            "passes": not collisions and moved}


def gate_g1(design: population.Design, loops: dict[str, list[tuple[str, dict]]],
            suite: bool = True) -> dict[str, Any]:
    er, vl, hv = e_is_the_rule_arms(design), v_is_the_loops(design, loops), the_halves()
    op, bd, dg = one_paragraph_apart(design), builders(), digests(design)
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": "e is the rule arm w's prompts and v the loop's first call; h and o are "
                    "cut and joined as §2.1 says and name nothing; the arms differ in the "
                    "paragraph alone; no builder takes a row; the digests have teeth; the "
                    "suite green",
            "e_is_the_rule_arms": er, "v_is_the_loops": vl, "the_halves": hv,
            "one_paragraph_apart": op, "builders": bd, "digests": dg, "suite": tests,
            "passes": (all(x["passes"] for x in (er, vl, hv, op, bd, dg))
                       and tests["passes"] is not False)}


# ---------------------------------------------------------------------------
# HV-g2: the request and the instrument
# ---------------------------------------------------------------------------

def the_request(design: population.Design,
                loops: dict[str, list[tuple[str, dict]]]) -> dict[str, Any]:
    """What the asker sends, built without a client, and what the DeepInfra
    loops' records say they sent."""
    msgs = design.asks[prompts.ask_id(prompts.HIDDEN, design.tickets[0])].messages()
    first = {"model": plan.MODEL, "messages": msgs, "max_tokens": plan.MAX_TOKENS,
             "temperature": plan.TEMPERATURE,
             "extra_body": {"reasoning": plan.REASONING, "provider": plan.PROVIDER},
             "response_format": {"type": "json_object"}}
    later = {k: v for k, v in first.items() if k != "response_format"}
    got = [pl_protocol.request_with(plan.PROVIDER, plan.MODEL, prompts.HIDDEN, msgs, k)
           for k in (0, 1)]
    records = [rec for g in plan.HV_A_GROUPS for _, rec in loops[g]]
    same = [rec.get("model") == plan.MODEL and rec.get("temperature") == plan.TEMPERATURE
            and rec.get("settings") == plan.settings() and rec.get("provider") == plan.PROVIDER
            for rec in records]
    out = {"first_attempt": got[0] == first, "a_retry": got[1] == later,
           "settings": plan.settings() == {"reasoning": plan.REASONING,
                                           "max_tokens": plan.MAX_TOKENS},
           "the_pin": plan.PROVIDER == {"order": ["deepinfra/fp8"], "allow_fallbacks": False},
           "deepinfra_records": len(records), "deepinfra_records_sent_it": all(same)}
    out["passes"] = (out["first_attempt"] and out["a_retry"] and out["settings"]
                     and out["the_pin"] and bool(records) and all(same))
    return out


def literals_in(path: Path) -> set[str]:
    """Every string literal in a module, docstrings included."""
    tree = ast.parse(path.read_text(), filename=str(path))
    return {n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)}


def no_label_on_the_asker_path() -> dict[str, Any]:
    leaked = {}
    for name in ASKER_PATH:
        path = HERE / name
        found = sorted((esc_gates.names_in(path) | literals_in(path)) & FORBIDDEN)
        if found:
            leaked[name] = found
    return {"modules": [f"halves/{n}" for n in ASKER_PATH], "forbidden_names": leaked,
            "passes": not leaked}


COUNTS = ("answers", "right_queue", "whole", "by_class")


def counts_of(share: dict[str, Any]) -> dict[str, Any]:
    return {k: share.get(k) for k in COUNTS}


def the_instrument(loops: dict[str, list[tuple[str, dict]]]) -> dict[str, Any]:
    """The classes give back `whole/paragraph.py`'s record from the closed
    answers, count for count. Only whether each group agrees is kept."""
    rec = json.loads(plan.paragraph_record().read_text())
    stage_c = json.loads(W.plan.score_path().read_text())
    got = W.read(W.rule_arm_rows(), loops, stage_c)
    groups = {}
    for g, mine in got["groups"].items():
        theirs = rec.get("groups", {}).get(g, {})
        groups[g] = (mine["shared_tickets"] == theirs.get("shared_tickets")
                     and counts_of(mine["loop"]) == counts_of(theirs.get("loop", {}))
                     and counts_of(mine["rule_arm_there"])
                     == counts_of(theirs.get("rule_arm_there", {})))
    rule_arm = counts_of(got["rule_arm"]) == counts_of(rec.get("rule_arm", {}))
    return {"groups": groups, "rule_arm": rule_arm, "classed_as_stage_c": got["_stage_c_ok"],
            "passes": (rule_arm and got["_stage_c_ok"] and set(groups) == set(plan.LOOP_GROUPS)
                       and all(groups.values()))}


def gate_g2(design: population.Design,
            loops: dict[str, list[tuple[str, dict]]]) -> dict[str, Any]:
    rq, nl, ins = the_request(design, loops), no_label_on_the_asker_path(), the_instrument(loops)
    return {"what": "the request is the loop's first call's with DeepInfra's pin, and the "
                    "DeepInfra loops sent it; the asker's path names no label; the classes "
                    "give back whole/paragraph.py's record",
            "the_request": rq, "no_label_on_the_asker_path": nl, "the_instrument": ins,
            "passes": rq["passes"] and nl["passes"] and ins["passes"]}


# ---------------------------------------------------------------------------
# HV-g3: the design
# ---------------------------------------------------------------------------

def rarest_queue_tickets() -> list[int]:
    """The corpus's tickets whose first matching rule of level 3's list sends
    them to `ONCALL_ESCALATION`, read over the space through `whole.references`."""
    space, cases, regions, _, queues = references._world()
    return [i for i, c in enumerate(cases)
            if queues[PO.matched(gv.point_of(c, space), regions)[0]] == "ONCALL_ESCALATION"]


def the_tickets(loops: dict[str, list[tuple[str, dict]]]) -> dict[str, Any]:
    """`plan.TICKETS`, rebuilt from the closed records."""
    asked = {r["ticket"] for r in W.rule_arm_rows()}
    met = {e["idx"] for runs in loops.values() for _, rec in runs for e in rec["escalations"]}
    oncall = rarest_queue_tickets()
    added = sorted(set(oncall) - asked)
    rebuilt = sorted((asked & met) | set(added))
    out = {"rule_arm_tickets": len(asked), "met": len(asked & met), "added": added,
           "oncall": oncall, "every_oncall_ticket_met": set(oncall) <= met,
           "rebuilt_is_the_plans": rebuilt == list(plan.TICKETS)}
    out["passes"] = (out["rebuilt_is_the_plans"] and len(asked) == plan.RULE_ARM_TICKETS
                     and len(asked & met) == plan.SHARED and tuple(oncall) == plan.ONCALL
                     and tuple(added) == plan.ADDED and out["every_oncall_ticket_met"]
                     and len(plan.TICKETS) == plan.N_TICKETS == len(set(plan.TICKETS)))
    return out


def asks_and_sessions(design: population.Design) -> dict[str, Any]:
    base = [a for a in design.asks.values() if a.rep == 0]
    reps = [a for a in design.asks.values() if a.rep]
    per = Counter(a.arm for a in base)
    every = sorted(population.base_ids(design.tickets))
    smoke = design.sessions["smoke"]
    smoke_per = Counter(design.asks[i].arm for i in smoke)
    out = {
        "prompts": {arm: per[arm] for arm in prompts.ARMS},
        "repetitions": len(reps),
        "rebuilt_from_the_seed": population.sessions_for(design.tickets) == design.sessions,
        "each_pass_holds_every_prompt_once": {s: sorted(design.sessions[s]) == every
                                              for s in plan.PASSES},
        "the_passes_differ": design.sessions["pass1"] != design.sessions["pass2"],
        "the_rarest_queues_session": (sorted(design.sessions["oncall"])
                                      == sorted(population.oncall_ids())
                                      and len(design.sessions["oncall"])
                                      == len(prompts.ARMS) * len(plan.ONCALL) * plan.ONCALL_REPEATS),
        "its_repetitions": all(a.ticket in plan.ONCALL and 1 <= a.rep <= plan.ONCALL_REPEATS
                               for a in reps),
        "smoke": smoke,
        "smoke_two_distinct_of_each_arm_outside_the_seven": (
            len(smoke) == len(set(smoke)) == len(prompts.ARMS) * plan.SMOKE_PER_ARM
            and all(smoke_per[arm] == plan.SMOKE_PER_ARM for arm in prompts.ARMS)
            and all(design.asks[i].ticket not in plan.ONCALL for i in smoke)),
    }
    out["passes"] = (all(per[arm] == plan.N_TICKETS for arm in prompts.ARMS)
                     and len(base) == len(prompts.ARMS) * plan.N_TICKETS
                     and out["rebuilt_from_the_seed"]
                     and all(out["each_pass_holds_every_prompt_once"].values())
                     and out["the_passes_differ"] and out["the_rarest_queues_session"]
                     and out["its_repetitions"]
                     and out["smoke_two_distinct_of_each_arm_outside_the_seven"])
    return out


def the_guard() -> dict[str, Any]:
    """The partial files are ignored by git. That the paid records are guarded
    is pinned by `tests/test_writer_lists.py`, which reads the guard's name in
    the modules; naming it here would count this module as a writer."""
    ignored = (REPO / ".gitignore").read_text()
    out = {"the_partial_files_are_ignored": "results_halves/*.partial.jsonl" in ignored}
    out["passes"] = all(out.values())
    return out


def gate_g3(design: population.Design,
            loops: dict[str, list[tuple[str, dict]]]) -> dict[str, Any]:
    tk, ss, gd = the_tickets(loops), asks_and_sessions(design), the_guard()
    return {"what": "the tickets come back from the closed records; the prompts, the "
                    "passes, the rarest queue's session and the smoke run are §2.3's; the "
                    "partial files are ignored",
            "the_tickets": tk, "asks_and_sessions": ss, "the_guard": gd,
            "passes": tk["passes"] and ss["passes"] and gd["passes"]}


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

def run_checks(suite: bool = True) -> Checks:
    design = population.build()
    loops = loop_records()
    return Checks(g1=gate_g1(design, loops, suite=suite), g2=gate_g2(design, loops),
                  g3=gate_g3(design, loops), g4=plan.gate_signature(), design=design)


def report(checks: Checks) -> None:
    def mark(g: dict) -> str:
        return "PASS" if g["passes"] else "FAIL"

    g1, g2, g3, g4 = checks.g1, checks.g2, checks.g3, checks.g4
    s = g1["suite"]
    print(f"\nHV-g1 {mark(g1)}  e is the rule arm's {g1['e_is_the_rule_arms']['passes']}; v is the "
          f"loop's {g1['v_is_the_loops']['passes']}; the halves {g1['the_halves']['passes']}; one "
          f"paragraph apart {g1['one_paragraph_apart']['passes']}; builders "
          f"{g1['builders']['passes']}; digests {g1['digests']['passes']}")
    print(f"      suite {'not run' if not s.get('ran') else s.get('result')}")
    print(f"HV-g2 {mark(g2)}  the request {g2['the_request']['passes']}; no label on the "
          f"asker's path {g2['no_label_on_the_asker_path']['passes']}; the instrument "
          f"{g2['the_instrument']['passes']}")
    ss = g3["asks_and_sessions"]
    print(f"HV-g3 {mark(g3)}  the tickets {g3['the_tickets']['passes']}; prompts by arm "
          f"{ss['prompts']}, repetitions {ss['repetitions']}; sessions {ss['passes']}; the "
          f"guard {g3['the_guard']['passes']}")
    print(f"HV-g4 {'SIGNED' if g4['passes'] else 'UNSIGNED'}  {g4['found']} signature "
          f"line(s), {g4['unsigned']} blank")
    print(f"\nblocking checks: {'PASS' if checks.blocking_pass else 'FAIL'}")
