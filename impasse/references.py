"""
The references of `PLAN_IMPASSE.md` §5.5 and Stage A, all free, and the readings
of a run that Stage C shares with them. **Never on the proposer's path.**

A FIRST-CALL DRAFT, AND ITS CAUSE. Every escalation's first-call draft is classed
by `whole/references.py`'s `first_drafts`, called, which is `placement/cost.py`'s
`draft_class` with the draft's breadth: against its ticket's governing rule, the
first listed rule whose region holds the ticket. Its cause is the one the
record's escalation keeps, `channel.loop.escalates`'s: IMPASSE, CONFLICT or
ERROR. A draft of another queue is `wrong_queue`, one naming no valid rule
`no_rule`, an empty object among them; both are left out of every share, above
and below, and counted.

THE STATISTICS OF §0, on any run's record:

  `impasses(r)`  the run's escalations whose cause is an IMPASSE;
  `whole_I(r)`   of its first-call drafts at impasses that name the right queue
                 and a valid rule, the share classed `whole`;
  `whole_D`      the same over the drafts whose ticket a rule of `plan.DEFAULTS`
                 governs, pooled over an arm's runs by Stage C;
  `born_W(r)`    of its first-call drafts at impasses classed `whole`, the share
                 whose escalation ended with the rule born.

THE GROUPS, §0's figure 8, off the text's 29 regions alone: `cause/narrow.py`'s
`held` and `group`, called, over every listed rule. A rule's group counts the
rules of another queue whose regions lie whole inside its own.

THE DRAFTING READING, §0's figures 1 to 6, on `PLAN_PLACEMENT.md`'s three v1c
runs and `PLAN_WHOLE.md`'s six, read-only. Figure 5 sets every point a final base
does not decide right against the listed rule that governs it, as
`placement/cost.py`'s `read_run` reads it, and each rule against the causes of
the escalations at its tickets. Figure 6 reads how `H01`'s first ticket, case 44,
met each base, and the first later case at which a first call drafted `H01`'s
region whole.

THE TRANSCRIBER is `placement/references.py`'s, through `whole/references.py`,
called. It writes the governing rule's region and places it by the list's order,
and ignores the text either arm carries: its figures under v1n are its figures
under v1c.

It reads the proposer's answers `PLAN_PLACEMENT.md` and `PLAN_WHOLE.md` paid for,
and no answer this plan buys.
"""

from __future__ import annotations

import collections
import json
from fractions import Fraction
from functools import lru_cache
from typing import Any

from authorship import protocol as e
from cause import narrow as CN
from placement import cost as PC
from placement import plan as pl_plan
from whole import plan as wh_plan
from whole import references as W

from . import plan

F = Fraction
LEFT_OUT_OF_THE_SHARE = W.LEFT_OUT_OF_THE_SHARE        # wrong_queue, no_rule
WHOLE = "whole"
NONE, FEW, MANY = CN.NONE, CN.FEW, CN.MANY
H01, CASE_44 = "H01", 44
_world = W._world
median = W.median


# ---------------------------------------------------------------------------
# The groups (figure 8)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def _groups() -> str:
    space, _, regions, _, queues = _world()
    rows = {g: CN.held(regions[g], g, regions, queues) for g in regions}
    return json.dumps({g: {"holds": rows[g], "group": CN.group(len(rows[g]))}
                       for g in sorted(rows, key=lambda h: int(h[1:]))})


def groups() -> dict[str, dict[str, Any]]:
    """Every listed rule, the rules of another queue whose regions lie inside its
    own, and its group, by `cause/narrow.py`'s `held` and `group`."""
    return json.loads(_groups())


def group_of(rule: str) -> str:
    return groups()[rule]["group"]


def groups_of_rules() -> dict[str, list[str]]:
    """Figure 8: the rules of each group but `none`, in the list's order."""
    g = groups()
    return {grp: [r for r in g if g[r]["group"] == grp] for grp in (MANY, FEW)}


# ---------------------------------------------------------------------------
# One run's drafts, with their causes
# ---------------------------------------------------------------------------

def drafts_of(record: dict[str, Any]) -> list[dict[str, Any]]:
    """Every escalation's first-call draft, classed and with its breadth
    (`whole/references.py`), with its cause and its governing rule's group."""
    kind = {esc["idx"]: esc["kind"] for esc in record["escalations"]}
    return [{**d, "cause": kind[d["idx"]], "group": group_of(d["governing"])}
            for d in W.first_drafts(record)]


def counted(drafts: list[dict[str, Any]]) -> list[int]:
    """`[held whole, right-queue drafts naming a valid rule]` over `drafts`."""
    right = [d for d in drafts if d["class"] not in LEFT_OUT_OF_THE_SHARE]
    return [sum(1 for d in right if d["class"] == WHOLE), len(right)]


def share(pair: list[int]) -> Fraction | None:
    return F(pair[0], pair[1]) if pair[1] else None


def at(drafts: list[dict[str, Any]], cause: str) -> list[dict[str, Any]]:
    return [d for d in drafts if d["cause"] == cause]


def impasses(record: dict[str, Any]) -> int:
    """`impasses(r)`: the escalations whose cause is an IMPASSE."""
    return sum(1 for esc in record["escalations"] if esc["kind"] == plan.IMPASSE)


def by_cause(drafts: list[dict[str, Any]]) -> dict[str, list[int]]:
    """Figure 2: whole and right-queue drafts at each cause."""
    return {c: counted(at(drafts, c)) for c in plan.CAUSES}


def by_group(drafts: list[dict[str, Any]]) -> dict[str, list[int]]:
    """Figure 3: whole and right-queue drafts at impasses, by the governing rule's
    group."""
    imp = at(drafts, plan.IMPASSE)
    return {g: counted([d for d in imp if d["group"] == g]) for g in (NONE, FEW, MANY)}


def at_the_defaults(drafts: list[dict[str, Any]]) -> list[int]:
    """`whole_D`'s counts in one run: the right-queue drafts at impasses whose
    ticket a rule of `plan.DEFAULTS` governs, and those classed `whole`."""
    return counted([d for d in at(drafts, plan.IMPASSE) if d["governing"] in plan.DEFAULTS])


def defaults_met(drafts: list[dict[str, Any]]) -> dict[str, int]:
    """The impasse escalations at each default's tickets, every draft counted."""
    met = collections.Counter(d["governing"] for d in at(drafts, plan.IMPASSE)
                              if d["governing"] in plan.DEFAULTS)
    return {g: met.get(g, 0) for g in plan.DEFAULTS}


def born_of(drafts: list[dict[str, Any]]) -> dict[str, int]:
    """Figure 4: the whole drafts at impasses, and how their escalations ended."""
    whole = [d for d in at(drafts, plan.IMPASSE) if d["class"] == WHOLE]
    return {"whole": len(whole),
            "born": sum(1 for d in whole if d["verdict"] == e.BORN),
            "unplaced": sum(1 for d in whole if d["verdict"] == e.UNPLACED),
            "refused": sum(1 for d in whole if d["verdict"] == e.REJECTED)}


def born_w(drafts: list[dict[str, Any]]) -> Fraction | None:
    """`born_W(r)`. None when no first-call draft at an impasse is whole (§0)."""
    b = born_of(drafts)
    return F(b["born"], b["whole"]) if b["whole"] else None


# ---------------------------------------------------------------------------
# Where a base lost its points, by the causes its rules' tickets met (figure 5)
# ---------------------------------------------------------------------------

NO_IMPASSE, SOME_IMPASSE, ONLY_IMPASSES, NO_ESCALATION = (
    "no_impasse", "an_impasse_and_another_cause", "only_impasses", "no_ticket_escalated")
LOST_TAGS = (NO_IMPASSE, SOME_IMPASSE, ONLY_IMPASSES, NO_ESCALATION)


def lost_by_causes(record: dict[str, Any]) -> dict[str, Any]:
    """Every point the final base does not decide right, set against the listed
    rule that governs it (`placement/cost.py`'s `read_run`, called), and each rule
    against the causes of the escalations at its tickets in the run."""
    space, cases, regions, truth, queues = _world()
    kind = {esc["idx"]: esc["kind"] for esc in record["escalations"]}
    run = PC.read_run(record, space, regions, PC.governed_masks(regions), truth, queues,
                      cases)
    out = {t: 0 for t in LOST_TAGS}
    rules = {}
    for g, r in run["rules"].items():
        causes = {kind[d["idx"]] for d in r["drafts"]}
        t = (NO_ESCALATION if not causes else ONLY_IMPASSES if causes == {plan.IMPASSE}
             else SOME_IMPASSE if plan.IMPASSE in causes else NO_IMPASSE)
        out[t] += r["lost"]
        if r["lost"]:
            rules[g] = {"lost": r["lost"], "tag": t, "class": r["class"],
                        "causes": dict(sorted(collections.Counter(
                            kind[d["idx"]] for d in r["drafts"]).items()))}
    return {"lost": sum(out.values()), **out, "right": run["right"], "rules": rules}


# ---------------------------------------------------------------------------
# H01's first ticket (figure 6)
# ---------------------------------------------------------------------------

def h01_case_44(record: dict[str, Any], drafts: list[dict[str, Any]]) -> list[Any]:
    """How case 44 met the base, its first call's class and verdict, and the
    first later case at which a first call drafted `H01`'s region whole."""
    row = next(r for r in record["records"] if r["idx"] == CASE_44)
    mine = next((d for d in drafts if d["idx"] == CASE_44), None)
    later = sorted(d["idx"] for d in drafts
                   if d["governing"] == H01 and d["class"] == WHOLE and d["idx"] > CASE_44)
    how = row.get("cause") or "decided"
    return [how, mine and mine["class"], mine and mine["verdict"],
            later[0] if later else None]


# ---------------------------------------------------------------------------
# §0's figures 1 to 6 and 8: the drafting reading
# ---------------------------------------------------------------------------

def closed_runs() -> dict[str, dict[str, Any]]:
    """The nine runs the drafting reading reads, read-only, by name."""
    out = {}
    for rep in range(1, pl_plan.REPS + 1):
        out[f"pl_v1c_r{rep}"] = json.loads(pl_plan.run_path("v1c", rep).read_text())
    for arm in wh_plan.ARMS:
        for rep in range(1, wh_plan.REPS + 1):
            out[f"wh_{arm}_r{rep}"] = json.loads(wh_plan.run_path(arm, rep).read_text())
    return out


def v1c_names() -> list[str]:
    return [f"{p}_v1c_r{rep}" for p in ("pl", "wh") for rep in (1, 2, 3)]


@lru_cache(maxsize=None)
def _drafting_reading() -> str:
    esc, whole, grp, born, lost, h01, met = {}, {}, {}, {}, {}, {}, {}
    pooled = {NONE: [0, 0], FEW: [0, 0], MANY: [0, 0]}
    for name, rec in closed_runs().items():
        ds = drafts_of(rec)
        kinds = collections.Counter(x["kind"] for x in rec["escalations"])
        esc[name] = [len(rec["escalations"]), *(kinds.get(c, 0) for c in
                                                (plan.IMPASSE, plan.CONFLICT, plan.ERROR))]
        whole[name] = by_cause(ds)
        grp[name] = by_group(ds)
        born[name] = born_of(ds)
        h01[name] = h01_case_44(rec, ds)
        if name.split("_")[1] == "v1c":
            lb = lost_by_causes(rec)
            lost[name] = [lb["lost"], *(lb[t] for t in LOST_TAGS)]
            for g in pooled:
                pooled[g] = [a + b for a, b in zip(pooled[g], grp[name][g])]
            for g, n in defaults_met(ds).items():
                met[g] = met.get(g, 0) + n
    return json.dumps({"escalations": esc, "whole_by_cause": whole, "groups": grp,
                       "groups_pooled_v1c": pooled, "impasses_at_defaults_v1c": met,
                       "born": born, "lost": lost, "h01_case_44": h01,
                       "groups_of_rules": groups_of_rules()})


def drafting_reading() -> dict[str, Any]:
    """§0's figures 1 to 6 and 8, recomputed from the closed records and the
    text."""
    return json.loads(_drafting_reading())


def drafting_as_declared(got: dict[str, Any]) -> dict[str, bool]:
    """Each of §0's figures against `got`, and figure 7, the schedule."""
    d = plan.DECLARED
    keys = ("escalations", "whole_by_cause", "groups", "groups_pooled_v1c",
            "impasses_at_defaults_v1c", "born", "lost", "h01_case_44", "groups_of_rules")
    out = {k: got.get(k) == d.get(k) for k in keys}
    out["schedule"] = [list(x) for x in plan.schedule()] == d.get("schedule")
    out["defaults"] = list(plan.DEFAULTS) == got["groups_of_rules"][MANY]
    return out


def transcriber_figures() -> dict[str, Any]:
    """The transcriber under v1c and every draw, `placement/references.py`'s."""
    return W.transcriber_figures()
