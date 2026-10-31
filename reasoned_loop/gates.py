"""
`RL-g1` to `RL-g4` of `PLAN_REASONED_LOOP.md` §7: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  RL-g1  The inputs reproduce themselves. The suite is green.
         `PLAN_REASONED_RULE.md`'s own checks pass, called, and its four
         verdicts come back from its two passes as its `score.json` holds them.
         `PLAN_MANUAL.md`'s three level-3 runs, rebuilt through this plan's
         instrument, give back the `space`, `corpus` and `K-a` its record holds.
         The list's first match is the policy over the space. The labels the
         error trigger reads agree with level 3's text on every corpus case. A
         run's rebuilt base is the engine the run ended with, here on the
         transcriber's two runs.
  RL-g2  The protocol is §5's. Every text is its source's. The hidden policy
         written through v1b's path is born whole, every declaration accepted,
         `rung2/hidden_priority.py`'s 199 edges installed, and every point of
         the space and case of the corpus decided right. The transcriber gives
         back §0's figures under both triggers. The requests, the retry by
         cause and the validator's verdicts are `tests/test_reasoned_loop.py`'s,
         through the SDK double and on cases built by hand, which `RL-g1`'s
         suite runs.
  RL-g3  The schedule is §2.6's: six runs, the arms alternating from the arm
         `ORDER_SEED` draws, the smoke run 30 cases under the error arm, the cap
         400 escalations.
  RL-g4  The signature (`reasoned_loop/plan.py`). It does not block a dry run,
         which writes nothing; it blocks every write.

**This module is offline.** It reads labels to recompute closed plans' verdicts
and figures and to hold the error trigger's labels to the text. The policy over
the space is read through `rung3.order_search_ls` and `manual.instrument`, and
the 199 edges through `rung2.hidden_priority`, modules already allowed to carry
it. It sends nothing, and what a dry run prints is pass or fail, and figures §0
or a published record already states.
"""

from __future__ import annotations

import ast
import inspect
import json
import textwrap
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from authorship import protocol as e
from blind import plan as bplan
from blind import protocol as v2b
from first_match import gates as fmgates
from manual import instrument as MI
from manual import plan as mplan
from manual import prompts as mprompts
from queue_alone import gates as qgates
from queue_alone import rules as qrules
from reasoned_rule import gates as rrgates
from reasoned_rule import plan as rrplan
from reasoned_rule import score as rrscore
from reuse.gates import run_suite
from rung2.engine2 import EDGE_OK, Space
from rung2.hidden_priority import build_hidden_engine
from rung2.proposers2 import OpenRouterProposer2

from . import plan, references
from . import protocol as p


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
        return {"RL-g1": self.g1, "RL-g2": self.g2, "RL-g3": self.g3, "RL-g4": self.g4}


# ---------------------------------------------------------------------------
# RL-g1
# ---------------------------------------------------------------------------

def reasoned_rule_rows(design) -> dict[str, Any]:
    """`PLAN_REASONED_RULE.md`'s four verdicts, again, from its two passes."""
    recorded = json.loads(rrplan.score_path().read_text())["verdicts"]
    recs = {s: rrscore.read(s) for s in rrplan.SESSIONS[1:]}
    got = rrscore.score(design, recs, rrscore.labels(), fmgates.queue_alone_passes(),
                        rrgates.first_match_passes())["verdicts"]
    off = [rid for rid in sorted(recorded)
           if rid not in got or not qgates.same_verdict(got[rid], recorded[rid])]
    return {"rows": len(got), "departing": off, "passes": not off and len(got) == 4}


def manual_level_3() -> dict[str, Any]:
    """`PLAN_MANUAL.md`'s level-3 runs through this plan's instrument, against
    the figures its record holds."""
    recorded = {r["rep"]: r for r in
                json.loads(mplan.score_path().read_text())["G-g"]["runs"]["3"]}
    mine = references.manual_level_3()
    off = [m["rep"] for m in mine
           if any(m[k] != recorded[m["rep"]][k]["fraction"] for k in ("space", "corpus", "k_a"))
           or m["cover"] != recorded[m["rep"]]["first_full_cover"]]
    return {"runs": len(mine), "departing": off, "passes": not off and len(mine) == 3}


def labels_against_the_text() -> dict[str, Any]:
    """The labels the error trigger is handed give every corpus case the queue
    and the rule level 3's text gives it by first match."""
    corpus, labels = MI.corpus(), plan.labels()
    queue = [i for i, (c, (y, _)) in enumerate(zip(corpus, labels))
             if qrules.first_queue(c.as_dict()) != y]
    rule = [i for i, (c, (_, r)) in enumerate(zip(corpus, labels))
            if references.governing(c).id != r]
    return {"cases": len(labels), "queue_departs": queue[:10], "rule_departs": rule[:10],
            "source": str(plan.labels_path()),
            "passes": len(labels) == plan.N == len(corpus) and not queue and not rule}


def same_engine(a, b) -> bool:
    """Two engines hold the same rules, born at the same cases, and the same
    declared edges."""
    def rules(eng):
        return [(r.rule_id, r.born_at, r.action, eng.ext[r.rule_id]) for r in eng.rules]

    def edges(eng):
        return {rid: set(ws) for rid, ws in eng.decl_below.items() if ws}
    return rules(a) == rules(b) and edges(a) == edges(b)


def rebuilds(runs: dict[str, dict]) -> dict[str, Any]:
    """§7: a run's rebuild, `manual.instrument.final_engine`, is the engine the
    run ended with."""
    got = {arm: same_engine(MI.final_engine(r["record"]), r["engine"])
           for arm, r in runs.items()}
    return {"runs": got, "passes": all(got.values())}


def gate_g1(transcribed: dict[str, dict], suite: bool = True) -> dict[str, Any]:
    rr = rrgates.run_checks(suite=False)
    rows = reasoned_rule_rows(rr.design)
    ml = manual_level_3()
    over = rrgates.the_list_over_the_space()
    lab = labels_against_the_text()
    rb = rebuilds(transcribed)
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": "PLAN_REASONED_RULE.md's checks pass and its verdicts come back; "
                    "PLAN_MANUAL.md's level-3 runs come back through this instrument; the "
                    "list's first match is the policy over the space; the labels agree with "
                    "the text; a run's rebuild is its engine; the suite green",
            "reasoned_rule_checks": rr.blocking_pass, "reasoned_rule_rows": rows,
            "manual_level_3": ml, "the_list_over_the_space": over,
            "labels": lab, "rebuilds": rb, "suite": tests,
            "passes": (rr.blocking_pass and rows["passes"] and ml["passes"]
                       and over["passes"] and lab["passes"] and rb["passes"]
                       and tests["passes"] is not False)}


# ---------------------------------------------------------------------------
# RL-g2
# ---------------------------------------------------------------------------

def string_constants(fn) -> set[str]:
    """Every string a function's source spells, adjacent literals joined as the
    parser joins them."""
    tree = ast.parse(textwrap.dedent(inspect.getsource(fn)))
    return {n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)}


def texts() -> dict[str, Any]:
    """§5.1: each text is its source's."""
    manual_run = json.loads(mplan.loop_path(3, 1).read_text())
    rr_sample = json.loads(rrplan.sample_path().read_text())
    blind_run = json.loads(bplan.run_path(1).read_text())
    case = MI.corpus()[0]
    draft = p.Answer("T1_GENERAL", {"action": "T1_GENERAL"}, None, "stop", 1)
    first, second = p.messages_for(case), p.messages_for(case, draft, "colocala")
    out = {
        "system_prompt_is_manual_level_3s": p.SYSTEM_PROMPT == manual_run["system_prompt"],
        "system_prompt_is_the_rule_arms": all(
            p.SYSTEM_PROMPT == rr_sample["system_prompts"][arm]["text"] for arm in ("t", "w")),
        "system_prompt_digest": p.sha256(p.SYSTEM_PROMPT)[:16] == plan.SYSTEM_PROMPT_SHA16,
        "system_prompt_holds_the_list": all(r.id in p.SYSTEM_PROMPT for r in qrules.rules()),
        "blind_base_is_v2bs": p.BLIND_BASE == blind_run["blind_base"],
        "placement_template_is_v2bs": p.PLACEMENT_TEMPLATE == blind_run["placement_template"],
        "v2b_as_signed": v2b.fingerprint() == bplan.FINGERPRINT,
        "retry_message_is_v1s": (p.RETRY_MSG == mprompts.RETRY_MSG
                                 and p.RETRY_MSG in string_constants(OpenRouterProposer2.propose)),
        "the_first_call": ([m["role"] for m in first] == ["system", "user"]
                           and first[1]["content"].startswith(p.BLIND_BASE)),
        "the_placement_call": ([m["role"] for m in second]
                               == ["system", "user", "assistant", "user"]
                               and second[:2] == first and second[2]["content"] == p.turn(draft)
                               and second[3]["content"] == "colocala"),
    }
    out["passes"] = all(out.values())
    return out


def hidden_policy() -> dict[str, Any]:
    """§5.6: the policy through v1b's path, and the 199 edges."""
    got = references.hidden_through_path()
    _ref, minimal, _ = build_hidden_engine(Space())
    counts = {"born": got["born"], "declarations": got["declarations"],
              "installed": len(got["installed"])}
    sp, co = got["space"], got["corpus"]
    out = {**counts, "verdicts": got["verdicts"],
           "every_declaration_accepted": got["verdicts"] == {EDGE_OK: got["declarations"]},
           "the_199_edges": sorted(list(x) for x in minimal) == got["installed"],
           "space": [sp["correct"], sp["n"]], "corpus": [co["correct"], co["n"]],
           "as_declared": counts == plan.DECLARED["hidden"]}
    out["passes"] = (out["every_declaration_accepted"] and out["the_199_edges"]
                     and sp["correct"] == sp["n"] and co["correct"] == co["n"]
                     and out["as_declared"])
    return out


def transcriber(transcribed: dict[str, dict]) -> dict[str, Any]:
    """§0's figures for the transcriber, under both triggers."""
    got = {arm: references.as_declared(arm, r["figures"]) for arm, r in transcribed.items()}
    return {"as_declared": got, "passes": all(all(v.values()) for v in got.values())}


def verdict_names() -> dict[str, Any]:
    """The validator's verdicts are v2b's and v1e's names."""
    names = {"born": e.BORN, "changed": p.CHANGED, "unplaced": e.UNPLACED,
             "rejected": e.REJECTED, "order": e.ORDER_WITHOUT_CONFLICT, "failed": e.FAILED}
    return {"names": names, "passes": len(set(names.values())) == len(names)}


def gate_g2(transcribed: dict[str, dict]) -> dict[str, Any]:
    tx, hp, tr, vn = texts(), hidden_policy(), transcriber(transcribed), verdict_names()
    return {"what": "every text is its source's; the hidden policy through v1b's path is "
                    "born whole with its 199 edges and decides both surfaces right; the "
                    "transcriber gives back §0's figures. The requests, the retry and the "
                    "validator's verdicts are tests/test_reasoned_loop.py's",
            "texts": tx, "hidden_policy": hp, "transcriber": tr, "verdicts": vn,
            "passes": all(x["passes"] for x in (tx, hp, tr, vn))}


# ---------------------------------------------------------------------------
# RL-g3
# ---------------------------------------------------------------------------

def gate_g3() -> dict[str, Any]:
    order = plan.schedule()
    arms = [a for a, _ in order]
    out = {"schedule": [list(x) for x in order],
           "rebuilt_from_the_seed": order == plan.schedule(),
           "six_runs_three_an_arm": (len(order) == len(set(order)) == 2 * plan.REPS
                                     and all(arms.count(a) == plan.REPS for a in plan.ARMS)),
           "the_arms_alternate": all(a != b for a, b in zip(arms, arms[1:])),
           "each_repetition_in_order": [r for _, r in order] == sorted(r for _, r in order),
           "smoke": [plan.SMOKE_N, plan.SMOKE_ARM] == [30, "e"],
           "cap": plan.MAX_ESCALATIONS == 400}
    out["passes"] = all(v for k, v in out.items() if k != "schedule")
    return {"what": "the six runs alternate from the arm the seed draws; the smoke run is 30 "
                    "cases under the error arm; the cap is 400 escalations", **out}


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

def run_checks(suite: bool = True) -> Checks:
    transcribed = {arm: references.transcriber_figures(arm) for arm in plan.ARMS}
    return Checks(g1=gate_g1(transcribed, suite=suite), g2=gate_g2(transcribed),
                  g3=gate_g3(), g4=plan.gate_signature())


def report(checks: Checks) -> None:
    def mark(g: dict) -> str:
        return "PASS" if g["passes"] else "FAIL"

    g1, g2, g3, g4 = checks.g1, checks.g2, checks.g3, checks.g4
    s = g1["suite"]
    print(f"\nRL-g1 {mark(g1)}  PLAN_REASONED_RULE.md's checks {g1['reasoned_rule_checks']}, "
          f"its verdicts departing {g1['reasoned_rule_rows']['departing'] or 'none'}; "
          f"PLAN_MANUAL.md's level-3 runs departing {g1['manual_level_3']['departing'] or 'none'}; "
          f"the list over the space {g1['the_list_over_the_space']['passes']}; the labels "
          f"{g1['labels']['passes']}; the rebuilds {g1['rebuilds']['passes']}")
    print(f"      suite {'not run' if not s.get('ran') else s.get('result')}")
    hp = g2["hidden_policy"]
    print(f"RL-g2 {mark(g2)}  texts {g2['texts']['passes']}; the hidden policy through v1b: "
          f"{hp['born']} born, {hp['declarations']} declarations, {hp['installed']} edges "
          f"installed, the 199 {hp['the_199_edges']}; the transcriber as declared "
          f"{g2['transcriber']['passes']}")
    print(f"RL-g3 {mark(g3)}  the schedule {g3['schedule']}")
    print(f"RL-g4 {'SIGNED' if g4['passes'] else 'UNSIGNED'}  {g4['found']} signature "
          f"line(s), {g4['unsigned']} blank")
    print(f"\nblocking checks: {'PASS' if checks.blocking_pass else 'FAIL'}")


def frac(x: Fraction) -> dict[str, Any]:
    return {"fraction": str(x), "value": float(x)}
