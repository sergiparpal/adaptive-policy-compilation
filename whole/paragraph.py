"""
WHETHER THE BLIND PARAGRAPH IS WHY THE LOOP'S FIRST CALL CUTS.
`whole/oncall.py` read the first calls at the rarest queue's tickets. Every cut's
note framed the draft as the end of a conflict between its governing rule and a
crossing rule of another queue, which the draft lies inside and beats by
containment, and every first call is told the ticket is an impasse.

The impasse frame alone does not cut. `PLAN_REASONED_RULE.md`'s reasoning rule
arm `w` asked level 3's system prompt, the frame included, with reasoning on.
It wrote the governing rule's region on 250 of its 342 answers
(`FINDINGS_REASONED_RULE.md`). Its user message opens *"BASE DE REGLAS: vacia.
Esta es la primera regla."* The loop's first call opens with v2b's paragraph
instead: the base is not shown, and a rule that overlaps rules of another queue
will be listed afterwards. Everything else the two send is the same text.
Asked for by Sergi on 2026-11-10, after Stage C, in place of a reading by the
escalation's cause, which the blind first call cannot see. Free on the records.
POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
At every ticket the rule arm answered and a loop escalated, set each answer of
the rule arm beside the loop's first calls at the same ticket. The answers come
from the same model, with level 3's system prompt, reasoning at high effort and
16,000 tokens. The groups:

  rule_arm       `PLAN_REASONED_RULE.md`'s arm `w`, two passes: the empty base;
  reasoned_loop  `PLAN_REASONED_LOOP.md`'s six runs, on Baidu: v2b's paragraph;
  channel        `PLAN_CHANNEL.md`'s six runs, on Baidu: v2b's paragraph;
  placement      `PLAN_PLACEMENT.md`'s six runs, on DeepInfra: v2b's paragraph;
  whole_v1c      this plan's three v1c runs, on DeepInfra: v2b's paragraph;
  whole_v1d      this plan's three v1d runs, on DeepInfra: T1.

Every answer is classed as Stage C classes a first-call draft
(`placement/cost.py`'s `draft_class`):
- whole, which holds its part;
- cut by one listed rule or by two;
- other;
- wrong queue, or no rule.

A group's share is the share of its right-queue answers that hold their part.
For each loop group, the rule arm is read on that group's shared tickets only.
Its *gap* is the rule arm's share there less the group's. Both shares are pooled
over answers; the ticket-weighted shares are reported beside them.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. The rule arm's system prompt is the loops' text, and its digest is each
     loop record's `system_prompt` digest.
  2. The rule arm's model and request settings are each loop record's.
  3. At every shared ticket, the rule arm's user message less the empty base is
     the loop's first message less v2b's paragraph. Each loop record's paragraph
     digest is v2b's, or T1's for v1d.
  4. Every rule-arm row read is of arm `w`.
  5. This plan's first calls are classed as Stage C classed them.

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  P1. **The empty base writes the region more often on Baidu's tickets.** The
      gap of `reasoned_loop` and of `channel` is at least a tenth each.
  P2. **And on DeepInfra's.** The gap of `placement` and of `whole_v1c` is at
      least a tenth each.
  P3. **The provider matters little beside the paragraph.** The four v2b
      groups' gaps lie within a tenth of one another.
  P4. **T1 closes part of the gap.** `whole_v1d`'s gap is above zero and below
      `whole_v1c`'s.

**The drafter's account.** The two prompts are the same but for one paragraph,
and that paragraph is why the loop cuts.
- **Under the empty base**, the reasoning applies the list, finds the rule that
  governs the ticket, and writes its region as a first rule. Nothing it was told
  makes a conflict.
- **Under v2b's paragraph**, it is told a rule of another queue may overlap its
  own and will be listed. Under the impasse frame it reads that as the engine's
  conflict. It settles the conflict among the listed rules the ticket matches by
  writing their intersection, which the system prompt's level 1 orders with no
  side declared.
- **The provider and the period matter less.** `PLAN_PLACEMENT.md`'s POST-RUN
  reading of the births found that DeepInfra holds its part no less often than
  Baidu over every birth.
- **T1 asks for the region and keeps the overlap sentence**, so it closes part of
  the gap.
- **The bet is P1**, Baidu beside Baidu. It holds the provider, and only the
  period and the loop around the call differ.
- **P1 is trusted most**, since the rule arm's 250 of 342 stands far above any
  loop's share of whole first drafts.
- **P3 is trusted least.** The bridge found DeepInfra cutting at the rarest
  queue's tickets where Baidu wrote the part whole.

**What the drafter had seen**:
- `FINDINGS_REASONED_RULE.md`'s summary of the rules its arms wrote, and the
  number of rows of each arm.
- The rule arm's system prompt, user message and settings, set beside the
  loop's. Each loop record's header: its protocol, the digests of its texts, its
  model and its settings.
- How many tickets each loop group shares with the rule arm.
- `FINDINGS_WHOLE.md` whole, with this plan's first-call classes by run and by
  queue, and its two POST-RUN readings.
- `FINDINGS_PLACEMENT.md`'s figure 1, `PLAN_PLACEMENT.md`'s whole shares by run,
  and its POST-RUN readings of the births and the bridge.

**What the drafter had not seen**: the class of any answer of the rule arm, or
of any loop's first call, at a ticket the two share. That includes the shares
at those tickets, and any loop's first-call share on Baidu.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-10, after Stage C. The expectation
above was written and committed before the reading ran. Not a signed row, not on
`STATUS.md`'s scoreboard, not a calibration event. Zero API calls.

Usage:  python3 -m whole.paragraph --dry-run   # gates 1 to 5; writes nothing
        PYTHONHASHSEED=0 python3 -m whole.paragraph
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from typing import Any

from harness.provenance import describe, environment

from channel import plan as ch_plan
from placement import cost as PC
from placement import plan as pl_plan
from queue_alone import prompts as qprompts
from reasoned_loop import plan as rl_plan
from reasoned_loop import protocol as LP
from reasoned_rule import plan as rr_plan
from reasoned_rule import prompts as RP
from reuse import structure as st
from rung2.proposers2 import user_msg

from . import plan, protocol, references

F = Fraction
RULE_ARM = RP.REASONING_RULE        # "w": the rule-writing prompt, reasoning on
EMPTY_BASE = qprompts.EMPTY_BASE    # "BASE DE REGLAS: vacia. Esta es la primera regla.\n"
GAP = F(1, 10)                      # P1 and P2's line, and P3's spread
BAIDU = ("reasoned_loop", "channel")
DEEPINFRA = ("placement", "whole_v1c")
LOOPS = BAIDU + DEEPINFRA + ("whole_v1d",)
PARAGRAPH = {"reasoned_loop": "blind_base", "channel": "blind_base", "placement": "blind_base",
             "whole_v1c": "blind_base", "whole_v1d": "whole_base"}
RIGHT_OUT = ("wrong_queue", "no_rule")   # left out of a share, as whole(r) leaves them

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-10, after Stage C. The expectation in the "
    "module's docstring was written and committed before the reading ran. Not a signed row; "
    "no verdict moves.")


def record_path():
    return plan.OUT / "paragraph.json"


def sha16(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# The records
# ---------------------------------------------------------------------------

def loop_paths() -> dict[str, list[tuple[str, Any]]]:
    out: dict[str, list[tuple[str, Any]]] = {g: [] for g in LOOPS}
    for arm, rep in rl_plan.schedule():
        out["reasoned_loop"].append((f"{arm}_r{rep}", rl_plan.run_path(arm, rep)))
    for arm, rep in ch_plan.schedule():
        out["channel"].append((f"{arm}_r{rep}", ch_plan.run_path(arm, rep)))
    for arm, rep in pl_plan.schedule():
        out["placement"].append((f"{arm}_r{rep}", pl_plan.run_path(arm, rep)))
    for arm, rep in plan.schedule():
        out[f"whole_{arm}"].append((f"{arm}_r{rep}", plan.run_path(arm, rep)))
    return out


def rule_arm_rows() -> list[dict[str, Any]]:
    rows = []
    for name in ("pass1", "pass2"):
        rec = json.loads(rr_plan.ask_path(name).read_text())
        rows += [{**r, "_pass": name} for r in rec["rows"] if r.get("arm") == RULE_ARM]
    return rows


# ---------------------------------------------------------------------------
# Classing an answer
# ---------------------------------------------------------------------------

def classed(idx: int, payload: dict | None) -> str:
    """An answer's class against its ticket's governing rule, as Stage C classes a
    first-call draft."""
    space, cases, regions, truth, queues = references._world()
    esc = {"idx": idx, "verdict": None, "calls": [{"round": 0, "payload": payload or {}}]}
    return PC.draft_class(esc, cases[idx], space, regions, truth, queues)["class"]


def share(classes: list[str]) -> dict[str, Any]:
    right = [c for c in classes if c not in RIGHT_OUT]
    held = sum(1 for c in right if c == "whole")
    out = {"answers": len(classes), "right_queue": len(right), "whole": held,
           "share": F(held, len(right)) if right else None}
    out["by_class"] = {c: classes.count(c) for c in sorted(set(classes))}
    return out


def ticket_weighted(by_ticket: dict[int, list[str]]) -> Fraction | None:
    """The mean over tickets of each ticket's share, over the tickets with a
    right-queue answer."""
    shares = [s["share"] for s in (share(cs) for cs in by_ticket.values())
              if s["share"] is not None]
    return sum(shares, F(0)) / len(shares) if shares else None


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def gates(rule_rows: list[dict], loops: dict[str, list[tuple[str, dict]]],
          shared: dict[str, set[int]], stage_c_ok: bool) -> list[dict[str, Any]]:
    _, cases, _, _, _ = references._world()
    system = RP.system_prompt(RULE_ARM)
    headers = [(g, t, r) for g, runs in loops.items() for t, r in runs]
    digests = {"blind_base": sha16(LP.BLIND_BASE), "whole_base": sha16(protocol.WHOLE_BASE)}
    every = sorted(set().union(*shared.values())) if shared else []
    same_rest = all(
        RP.user_message(RULE_ARM, cases[i]).removeprefix(EMPTY_BASE)
        == user_msg(cases[i], LP.BLIND_BASE).removeprefix(LP.BLIND_BASE)
        and RP.user_message(RULE_ARM, cases[i]).startswith(EMPTY_BASE)
        for i in every)
    return [
        {"gate": 1, "what": "the rule arm's system prompt is the loops'",
         "passes": system == LP.SYSTEM_PROMPT
                   and all((r.get("texts_sha16") or {}).get("system_prompt") == sha16(system)
                           for _, _, r in headers)},
        {"gate": 2, "what": "the rule arm's model and request settings are each loop record's",
         "passes": all(r.get("model") == rr_plan.MODEL
                       and r.get("settings") == rr_plan.settings(RULE_ARM)
                       for _, _, r in headers)},
        {"gate": 3, "what": "the messages differ in the base paragraph alone, and each loop "
                            "record sent its group's paragraph",
         "passes": bool(every) and same_rest
                   and all((r.get("texts_sha16") or {}).get(PARAGRAPH[g]) == digests[PARAGRAPH[g]]
                           for g, _, r in headers)},
        {"gate": 4, "what": "every rule-arm row read is of arm w",
         "passes": bool(rule_rows) and all(r.get("arm") == RULE_ARM for r in rule_rows)},
        {"gate": 5, "what": "this plan's first calls are classed as Stage C classed them",
         "passes": stage_c_ok},
    ]


# ---------------------------------------------------------------------------
# The reading
# ---------------------------------------------------------------------------

def read(rule_rows: list[dict], loops: dict[str, list[tuple[str, dict]]],
         stage_c: dict[str, Any]) -> dict[str, Any]:
    rule_by_ticket: dict[int, list[str]] = {}
    providers: dict[str, dict[str, int]] = {"rule_arm": {}}
    for r in rule_rows:
        rule_by_ticket.setdefault(r["ticket"], []).append(classed(r["ticket"], r.get("payload")))
        p = str(r.get("served_by"))
        providers["rule_arm"][p] = providers["rule_arm"].get(p, 0) + 1
    tickets = set(rule_by_ticket)
    groups: dict[str, Any] = {}
    shared: dict[str, set[int]] = {}
    stage_c_ok = True
    for g, runs in loops.items():
        by_ticket: dict[int, list[str]] = {}
        provs: dict[str, int] = {}
        for t, rec in runs:
            drafts = references.first_drafts(rec)
            if g.startswith("whole_"):
                sc = {d["idx"]: d["class"] for d in stage_c["WR-g"]["runs"][t]["first_drafts"]}
                stage_c_ok &= all(sc.get(d["idx"]) == d["class"] for d in drafts)
            for d in drafts:
                if d["idx"] in tickets:
                    by_ticket.setdefault(d["idx"], []).append(d["class"])
            for esc in rec["escalations"]:
                if esc["idx"] in tickets:
                    for a in ((esc.get("calls") or [{}])[0].get("call_attempts") or []):
                        if a.get("error") is None:
                            p = str(a.get("provider"))
                            provs[p] = provs.get(p, 0) + 1
        shared[g] = set(by_ticket)
        mine = [c for cs in by_ticket.values() for c in cs]
        rules = [c for i in shared[g] for c in rule_by_ticket[i]]
        s_loop, s_rule = share(mine), share(rules)
        gap = (s_rule["share"] - s_loop["share"]
               if s_rule["share"] is not None and s_loop["share"] is not None else None)
        groups[g] = {"runs": [t for t, _ in runs], "shared_tickets": len(shared[g]),
                     "loop": s_loop, "rule_arm_there": s_rule, "gap": gap,
                     "loop_ticket_weighted": ticket_weighted(by_ticket),
                     "rule_arm_ticket_weighted": ticket_weighted(
                         {i: rule_by_ticket[i] for i in shared[g]})}
        providers[g] = provs
    return {"rule_arm": {"tickets": len(tickets), **share([c for cs in rule_by_ticket.values()
                                                           for c in cs])},
            "groups": groups, "providers": providers, "_shared": shared, "_stage_c_ok": stage_c_ok}


def expectation(groups: dict[str, Any]) -> list[dict[str, Any]]:
    gap = {g: groups[g]["gap"] for g in LOOPS}
    v2b = [gap[g] for g in BAIDU + DEEPINFRA]
    return [
        {"clause": "P1", "what": "the gap of reasoned_loop and of channel is at least a tenth "
                                 "each",
         "reading": {g: gap[g] for g in BAIDU},
         "holds": all(gap[g] is not None and gap[g] >= GAP for g in BAIDU)},
        {"clause": "P2", "what": "the gap of placement and of whole_v1c is at least a tenth each",
         "reading": {g: gap[g] for g in DEEPINFRA},
         "holds": all(gap[g] is not None and gap[g] >= GAP for g in DEEPINFRA)},
        {"clause": "P3", "what": "the four v2b groups' gaps lie within a tenth of one another",
         "reading": {"spread": (max(v2b) - min(v2b)) if None not in v2b else None},
         "holds": None not in v2b and max(v2b) - min(v2b) < GAP},
        {"clause": "P4", "what": "whole_v1d's gap is above zero and below whole_v1c's",
         "reading": {"whole_v1d": gap["whole_v1d"], "whole_v1c": gap["whole_v1c"]},
         "holds": None not in (gap["whole_v1d"], gap["whole_v1c"])
                  and 0 < gap["whole_v1d"] < gap["whole_v1c"]},
    ]


def frac(x):
    return None if x is None else {"fraction": str(x), "value": float(x)}


def jsonable(obj):
    if isinstance(obj, Fraction):
        return frac(obj)
    if isinstance(obj, dict):
        return {k: jsonable(v) for k, v in obj.items() if not str(k).startswith("_")}
    if isinstance(obj, (list, tuple)):
        return [jsonable(v) for v in obj]
    return obj


def read_all() -> tuple[list[dict], dict[str, list[tuple[str, dict]]], dict[str, Any]]:
    loops = {g: [(t, json.loads(p.read_text())) for t, p in runs]
             for g, runs in loop_paths().items()}
    return rule_arm_rows(), loops, json.loads(plan.score_path().read_text())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Whether the blind paragraph is why the loop's "
                                             "first call cuts (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 5 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"whole/paragraph.py writes {record_path()}")
    rule_rows, loops, stage_c = read_all()
    got = read(rule_rows, loops, stage_c)
    checked = gates(rule_rows, loops, got["_shared"], got["_stage_c_ok"])
    for g in checked:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    clauses = expectation(got["groups"])
    record_path().write_text(json.dumps(st._rounded(jsonable({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"rule_arm": [str(rr_plan.ask_path(n)) for n in ("pass1", "pass2")],
                   "loops": {g: [str(p) for _, p in runs] for g, runs in loop_paths().items()},
                   "score": str(plan.score_path())},
        "surface": "the corpus's escalated tickets, each answer's region over the space",
        "paragraphs": {"rule_arm": EMPTY_BASE, "v2b": LP.BLIND_BASE, "T1": protocol.WHOLE_BASE},
        "constants": {"GAP": str(GAP), "RULE_ARM": RULE_ARM},
        "gates": checked,
        "rule_arm": got["rule_arm"],
        "groups": got["groups"],
        "providers": got["providers"],
        "expectation": clauses,
    })), indent=2, default=str, ensure_ascii=False) + "\n")
    for c in clauses:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
