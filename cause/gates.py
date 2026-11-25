"""
`CA-g1` to `CA-g4` of `PLAN_CAUSE.md` §6: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  CA-g1  The texts. `e`'s and `v`'s prompts are `PLAN_HALVES.md`'s, digest for
         digest, at every ask of every session: as its Stage A record froze
         them, and as its three session records asked them, under the same
         system prompt. `v`'s messages are the loop's first call,
         `reasoned_loop.protocol.messages_for`, at every ticket. `i` and `r` are
         `v`, a blank line and a notice, as `corrections.protocol.base_text`
         sets its report; the review notice is `REPORT` up to the sentence that
         names the queue, with one newline in place of one space; and neither
         notice names a queue or a rule. Every arm's message differs from `v`'s
         in the paragraph alone, and every repetition asks its prompt's
         messages. No builder takes a row, and the digests have teeth. The suite
         is green.
  CA-g2  The request and the instrument. The request is `PLAN_HALVES.md`'s,
         `placement.protocol.request_with` over the loop's request, with
         DeepInfra's pin, and that plan's three session records carry the same
         model, temperature, settings and pin. No module on the asker's path
         names a label, in a name or a string literal, as `N-g2` reads them. And
         the instrument gives back `PLAN_HALVES.md`'s records before it reads a
         new answer: its classes give back that plan's six verdicts and its
         classes by arm, fraction for fraction, and `halves/hidden.py`'s codebook
         gives back its counts on that plan's pass 1.
  CA-g3  The design. The 136 tickets are `PLAN_HALVES.md`'s, as its Stage A
         record keeps them, and every one met a cause in the reasoning loops;
         the seven are the corpus's tickets of `ONCALL_ESCALATION` by level 3's
         list. 544 prompts, 136 an arm; each pass every prompt once, in its
         order rebuilt from `ORDER_SEED`; the rarest queue's session its 28
         prompts four times each; the smoke run two distinct prompts of each
         arm, outside the seven. The partial files are ignored by git, and the
         asker's validity flag is §0's on an empty object.
  CA-g4  The signature (`cause/plan.py`). It does not block a dry run, which
         writes nothing; it blocks every write.

**This module is offline.** It reads `PLAN_HALVES.md`'s answers for one thing
only: to hold the classes and the codebook to the records that published them,
which that plan's Stage C and `halves/hidden.py` did with the same functions. It
reads the loops' causes to hold the tickets, and level 3's list over the space
through `whole.references`, never the oracle. It sends nothing, and it prints no
figure of any plan: a check passes or fails.
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

from corrections import protocol as cprotocol
from escalations import gates as esc_gates
from halves import gates as hgates
from halves import hidden as hhidden
from halves import plan as hplan
from halves import prompts as hprompts
from halves import score as hscore
from placement import protocol as pl_protocol
from reasoned_loop import protocol as p
from reuse.gates import run_suite
from whole import paragraph as W
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
HALVES_SESSIONS = ("pass1", "pass2", "oncall")
OURS = (prompts.EMPTY, prompts.V2B)     # the arms PLAN_HALVES.md asked


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
        return {"CA-g1": self.g1, "CA-g2": self.g2, "CA-g3": self.g3, "CA-g4": self.g4}


def halves_records() -> tuple[dict[str, Any], dict[str, dict]]:
    """`PLAN_HALVES.md`'s Stage A record and its three session records."""
    sample = json.loads(plan.halves_sample().read_text())
    return sample, {s: json.loads(plan.halves_ask(s).read_text()) for s in HALVES_SESSIONS}


def loop_records() -> dict[str, list[tuple[str, dict]]]:
    return hgates.loop_records()


# ---------------------------------------------------------------------------
# CA-g1: the texts
# ---------------------------------------------------------------------------

def e_and_v_are_the_halves(design: population.Design, sample: dict[str, Any],
                           sessions: dict[str, dict]) -> dict[str, Any]:
    """At every ask of `e` and `v`, the digest `PLAN_HALVES.md` froze in its Stage A
    record and asked in its sessions, under the same system prompt and texts."""
    theirs = sample["design"]["asks"]
    mine = {i: a.digest for i, a in design.asks.items() if a.arm in OURS}
    off = sorted(i for i, d in mine.items() if theirs.get(i, {}).get("digest") != d)
    asked = [(r["id"], r["digest"]) for rec in sessions.values() for r in rec["rows"]
             if r["arm"] in OURS]
    rows_off = sorted(i for i, d in asked if mine.get(i) != d)
    texts = sample["texts"]
    out = {"asks": len(mine), "departing": off[:10], "rows_read": len(asked),
           "rows_departing": rows_off[:10],
           "the_system_prompt": (sample["texts_sha16"]["system_prompt"]
                                 == prompts.sha16(prompts.SYSTEM_PROMPT)
                                 and texts["system_prompt"] == prompts.SYSTEM_PROMPT),
           "the_paragraphs": (texts["paragraph_e"] == prompts.EMPTY_BASE
                              and texts["paragraph_v"] == prompts.BLIND_BASE)}
    out["passes"] = (not off and not rows_off and out["the_system_prompt"]
                     and out["the_paragraphs"]
                     and len(mine) == len(OURS) * (plan.N_TICKETS
                                                    + len(plan.ONCALL) * plan.ONCALL_REPEATS)
                     and len(asked) == len(OURS) * (2 * plan.N_TICKETS
                                                     + len(plan.ONCALL) * plan.ONCALL_REPEATS))
    return out


def v_is_the_loops(design: population.Design) -> dict[str, Any]:
    """`v`'s messages are the loop's first call at every ticket."""
    off = [t for t in design.tickets
           if design.asks[prompts.ask_id(prompts.V2B, t)].messages()
           != p.messages_for(design.asks[prompts.ask_id(prompts.V2B, t)].case)]
    return {"tickets": len(design.tickets), "departing": off[:10], "passes": not off}


def the_notices() -> dict[str, Any]:
    """§2.1's texts: each notice set after `v` as the report is, the review notice
    cut from the report as the plan says, and neither naming anything."""
    e, v, i, r = (prompts.PARAGRAPHS[a] for a in prompts.ARMS)
    impasse, review, report = prompts.IMPASSE_NOTICE, prompts.REVIEW_NOTICE, cprotocol.REPORT
    cut = len(review) - 1
    notices = (impasse, review)
    out = {
        "e_is_halves_e": e == hprompts.PARAGRAPHS["e"],
        "v_is_halves_v_and_v2bs": v == hprompts.PARAGRAPHS["v"] == p.BLIND_BASE
                                  == cprotocol.BLIND_BASE,
        "i_is_v_a_blank_line_and_the_impasse_notice": i == v + "\n" + impasse,
        "r_is_v_a_blank_line_and_the_review_notice": r == v + "\n" + review,
        "set_as_the_report_is": all(cprotocol.base_text(q) == v + "\n" + cprotocol.report(q)
                                    for q in ACTIONS),
        "the_review_notice_is_the_report_cut": (review[:cut] == report[:cut]
                                                and report[cut] == " "
                                                and review[cut] == "\n"
                                                and report[cut:].lstrip().startswith("La cola")),
        "the_four_differ": len({e, v, i, r}) == 4,
        "each_ends_its_line": all(x.endswith("\n") for x in (e, v, i, r)),
        "no_notice_names_a_queue": not any(q in x for q in ACTIONS for x in notices),
        "no_notice_names_a_rule": not any(RULE_ID.search(x) for x in notices),
        "no_notice_keeps_a_placeholder": not any("{" in x or "}" in x for x in notices),
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
    a = design.asks[prompts.ask_id(prompts.IMPASSE, design.tickets[0])]
    moved = prompts.digest(a.system, a.user + " ") != a.digest
    return {"digests": len(seen), "collisions": collisions[:10],
            "one_changed_character_moves_the_digest": moved,
            "passes": not collisions and moved}


def gate_g1(design: population.Design, sample: dict[str, Any], sessions: dict[str, dict],
            suite: bool = True) -> dict[str, Any]:
    ev, vl, nt = e_and_v_are_the_halves(design, sample, sessions), v_is_the_loops(design), \
        the_notices()
    op, bd, dg = one_paragraph_apart(design), builders(), digests(design)
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": "e and v are PLAN_HALVES.md's prompts and v the loop's first call; i and r "
                    "are v and a notice as §2.1 says, naming nothing; the arms differ in the "
                    "paragraph alone; no builder takes a row; the digests have teeth; the "
                    "suite green",
            "e_and_v_are_the_halves": ev, "v_is_the_loops": vl, "the_notices": nt,
            "one_paragraph_apart": op, "builders": bd, "digests": dg, "suite": tests,
            "passes": (all(x["passes"] for x in (ev, vl, nt, op, bd, dg))
                       and tests["passes"] is not False)}


# ---------------------------------------------------------------------------
# CA-g2: the request and the instrument
# ---------------------------------------------------------------------------

def the_request(design: population.Design, sessions: dict[str, dict]) -> dict[str, Any]:
    """What the asker sends, built without a client, and what `PLAN_HALVES.md`'s
    session records say they sent."""
    msgs = design.asks[prompts.ask_id(prompts.REVIEW, design.tickets[0])].messages()
    first = {"model": plan.MODEL, "messages": msgs, "max_tokens": plan.MAX_TOKENS,
             "temperature": plan.TEMPERATURE,
             "extra_body": {"reasoning": plan.REASONING, "provider": plan.PROVIDER},
             "response_format": {"type": "json_object"}}
    later = {k: v for k, v in first.items() if k != "response_format"}
    got = [pl_protocol.request_with(plan.PROVIDER, plan.MODEL, prompts.REVIEW, msgs, k)
           for k in (0, 1)]
    same = [rec.get("model") == plan.MODEL and rec.get("temperature") == plan.TEMPERATURE
            and rec.get("settings") == plan.settings() and rec.get("provider") == plan.PROVIDER
            for rec in sessions.values()]
    out = {"first_attempt": got[0] == first, "a_retry": got[1] == later,
           "settings": plan.settings() == {"reasoning": plan.REASONING,
                                           "max_tokens": plan.MAX_TOKENS},
           "the_pin": plan.PROVIDER == {"order": ["deepinfra/fp8"], "allow_fallbacks": False},
           "halves_records": len(sessions), "halves_records_sent_it": all(same)}
    out["passes"] = (out["first_attempt"] and out["a_retry"] and out["settings"]
                     and out["the_pin"] and len(sessions) == len(HALVES_SESSIONS) and all(same))
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
    return {"modules": [f"cause/{n}" for n in ASKER_PATH], "forbidden_names": leaked,
            "passes": not leaked}


def the_instrument(sample: dict[str, Any], sessions: dict[str, dict]) -> dict[str, Any]:
    """The classes give back `PLAN_HALVES.md`'s six verdicts, fraction for
    fraction, and its classes by arm; the codebook gives back
    `halves/hidden.py`'s counts on its pass 1. Only whether each agrees is kept.
    The standard errors are floats, and are not compared (`CLAUDE.md`, on 3.10)."""
    theirs = json.loads(plan.halves_score().read_text())
    got = hscore.score(sessions, sample)
    verdicts = {rid: (v["verdict"] == theirs["verdicts"][rid]["verdict"]
                      and (v["value"] or {}).get("fraction")
                      == (theirs["verdicts"][rid]["value"] or {}).get("fraction"))
                for rid, v in got["verdicts"].items()}
    classes = got["HV-g"]["classes"] == theirs["HV-g"]["classes"]
    codebook = (hhidden.development(sessions["pass1"]["rows"], references._world())
                == (hhidden.DEVELOPMENT, hhidden.DEVELOPMENT_ANSWERS))
    return {"verdicts": verdicts, "classes_by_arm": classes, "the_codebook": codebook,
            "passes": (set(verdicts) == set(hplan.ROWS) and all(verdicts.values())
                       and classes and codebook)}


def gate_g2(design: population.Design, sample: dict[str, Any],
            sessions: dict[str, dict]) -> dict[str, Any]:
    rq, nl = the_request(design, sessions), no_label_on_the_asker_path()
    ins = the_instrument(sample, sessions)
    return {"what": "the request is PLAN_HALVES.md's with DeepInfra's pin, and its records "
                    "sent it; the asker's path names no label; the classes and the codebook "
                    "give back PLAN_HALVES.md's records",
            "the_request": rq, "no_label_on_the_asker_path": nl, "the_instrument": ins,
            "passes": rq["passes"] and nl["passes"] and ins["passes"]}


# ---------------------------------------------------------------------------
# CA-g3: the design
# ---------------------------------------------------------------------------

def causes_at(loops: dict[str, list[tuple[str, dict]]], tickets) -> dict[int, Counter]:
    """By ticket, the causes of its escalations in every run of the reasoning
    loops."""
    t = set(tickets)
    out: dict[int, Counter] = {i: Counter() for i in tickets}
    for runs in loops.values():
        for _, rec in runs:
            for x in rec["records"]:
                if x.get("cause") and x["idx"] in t:
                    out[x["idx"]][x["cause"]] += 1
    return out


def the_tickets(sample: dict[str, Any], loops: dict[str, list[tuple[str, dict]]]
                ) -> dict[str, Any]:
    """`plan.TICKETS` are `PLAN_HALVES.md`'s, and every one met a cause."""
    causes = causes_at(loops, plan.TICKETS)
    oncall = hgates.rarest_queue_tickets()
    out = {"halves_tickets": tuple(sample["design"]["tickets"]) == tuple(plan.TICKETS),
           "the_seven": tuple(oncall) == plan.ONCALL == hplan.ONCALL,
           "every_ticket_met_a_cause": all(causes[t] for t in plan.TICKETS),
           "loop_groups": sorted(loops) == sorted(plan.LOOP_GROUPS)}
    out["passes"] = (all(out.values()) and len(plan.TICKETS) == plan.N_TICKETS
                     == len(set(plan.TICKETS)) and set(plan.ONCALL) <= set(plan.TICKETS))
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
    out = {"the_partial_files_are_ignored": "results_cause/*.partial.jsonl" in ignored}
    out["passes"] = all(out.values())
    return out


def the_askers_flag(design: population.Design) -> dict[str, Any]:
    """§0's validity, as the asker writes it into a row: an empty object from the
    pinned provider is valid; a failed call, a payload that is not an object and
    another provider's answer are not (`PLAN_HALVES.md`'s lesson)."""
    from . import ask as asker       # imported here: the asker imports this module

    a = design.asks[prompts.ask_id(prompts.IMPASSE, design.tickets[0])]
    pinned = [{"provider": plan.PROVIDER_NAME}]

    def flag(payload, failure=None, attempts=pinned) -> bool:
        got = type("Got", (), {"payload": payload, "action": None})()
        return asker.row_of("pass1", 0, a, None if failure else got, failure, attempts,
                            0.0)["valid"]

    out = {"an_empty_object_is_valid": flag({}) is True,
           "a_rule_is_valid": flag({"action": ACTIONS[0], "conditions": []}) is True,
           "a_failed_call_is_not": flag(None, failure="RuntimeError: 429") is False,
           "a_string_is_not": flag("{}") is False,
           "another_provider_is_not": flag({}, attempts=[{"provider": "Baidu"}]) is False}
    out["passes"] = all(out.values())
    return out


def gate_g3(design: population.Design, sample: dict[str, Any],
            loops: dict[str, list[tuple[str, dict]]]) -> dict[str, Any]:
    tk, ss, gd = the_tickets(sample, loops), asks_and_sessions(design), the_guard()
    fl = the_askers_flag(design)
    return {"what": "the tickets are PLAN_HALVES.md's and every one met a cause; the prompts, "
                    "the passes, the rarest queue's session and the smoke run are §2.3's; the "
                    "partial files are ignored; the asker's flag is §0's",
            "the_tickets": tk, "asks_and_sessions": ss, "the_guard": gd,
            "the_askers_flag": fl,
            "passes": tk["passes"] and ss["passes"] and gd["passes"] and fl["passes"]}


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

def run_checks(suite: bool = True) -> Checks:
    design = population.build()
    sample, sessions = halves_records()
    loops = loop_records()
    return Checks(g1=gate_g1(design, sample, sessions, suite=suite),
                  g2=gate_g2(design, sample, sessions),
                  g3=gate_g3(design, sample, loops), g4=plan.gate_signature(), design=design)


def report(checks: Checks) -> None:
    def mark(g: dict) -> str:
        return "PASS" if g["passes"] else "FAIL"

    g1, g2, g3, g4 = checks.g1, checks.g2, checks.g3, checks.g4
    s = g1["suite"]
    print(f"\nCA-g1 {mark(g1)}  e and v are PLAN_HALVES.md's {g1['e_and_v_are_the_halves']['passes']}; "
          f"v is the loop's {g1['v_is_the_loops']['passes']}; the notices "
          f"{g1['the_notices']['passes']}; one paragraph apart "
          f"{g1['one_paragraph_apart']['passes']}; builders {g1['builders']['passes']}; "
          f"digests {g1['digests']['passes']}")
    print(f"      suite {'not run' if not s.get('ran') else s.get('result')}")
    print(f"CA-g2 {mark(g2)}  the request {g2['the_request']['passes']}; no label on the "
          f"asker's path {g2['no_label_on_the_asker_path']['passes']}; the instrument "
          f"{g2['the_instrument']['passes']}")
    ss = g3["asks_and_sessions"]
    print(f"CA-g3 {mark(g3)}  the tickets {g3['the_tickets']['passes']}; prompts by arm "
          f"{ss['prompts']}, repetitions {ss['repetitions']}; sessions {ss['passes']}; the "
          f"guard {g3['the_guard']['passes']}; the asker's flag {g3['the_askers_flag']['passes']}")
    print(f"CA-g4 {'SIGNED' if g4['passes'] else 'UNSIGNED'}  {g4['found']} signature "
          f"line(s), {g4['unsigned']} blank")
    print(f"\nblocking checks: {'PASS' if checks.blocking_pass else 'FAIL'}")
