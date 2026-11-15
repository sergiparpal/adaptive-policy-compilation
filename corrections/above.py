"""
WHY SOME ANSWERS PUT THEIR NEWBORN ABOVE EVERY RULE OF THEIR LIST.
`corrections/doors.py` found that most climbs over the gateway still put their
newborn below every security rule their round listed. The rest put it above
every rule of their list, the security rules included.
`FINDINGS_CORRECTIONS.md`, *Why the doors declared themselves above the
gateway*, *What it does not settle*, item 2, and `IDEAS.md` leave why. Asked for
by Sergi on 2026-11-15, after `corrections/byqueue.py`. Free on the records.
POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
**A round** is a born rule whose round listed rules. What its answer declared of
each is what `corrections/fall.py`'s `declared` reads: the newborn above the
rule, in `beats`, or below it, in `loses_to`. What the answer did with a set of
the listed rules is what `corrections/doors.py`'s `toward` says: its newborn
above every one, below every one, or some of each. Every round of the six runs
is read.

For each round the reading takes:
- **the whole list**, and what the answer did with it;
- **the queues put first**: the listed rules of SECURITY_INCIDENT, and of
  ONCALL_ESCALATION for a newborn of neither, and what the answer did with each
  queue's rules;
- **the ticket**: each placement, by whether its rule's region holds the round's
  ticket, and by the cause of the escalation;
- **the draft**: its queue, its conditions, and its key, as
  `corrections/byqueue.py` keys a draft;
- **the note** of the placement call, whole, coded for two things below.

Also read, with no clause:
- each side of the security block by cause, by the draft's conditions and by
  the block's length;
- the notes' codes on each side;
- the drafts listed against security more than once that went above it once.

--------------------------------------------------------------------------
THE DEVELOPMENT SET
--------------------------------------------------------------------------
**L r1 and N r3 are the development set**, one run of each arm. E1 to E4 read
L r2 and L r3, pooled. E5 and E6 read N r1 and N r2, pooled, as the control.
What the drafter read of L r1 and N r3, before writing anything below:
- **every round**, with:
  - its newborn's queue, cause, conditions and points, and its list's length;
  - what its answer declared of every listed rule;
  - each listed rule's queue, conditions and points, and whether its region
    holds the ticket;
- **every placement**, by the newborn's queue and the listed rule's, by the
  conditions and the points of the two, and by the cause and the ticket;
- **the rounds above every rule of a list that holds a rule of
  SECURITY_INCIDENT**, two in L r1 and five in N r3. Their lists, their notes
  and their placement calls' reasoning were read whole;
- **the notes of every round whose list holds a rule of SECURITY_INCIDENT**,
  counted for the two codes below and for two that were dropped.

**Its counts**, `DEVELOPMENT`, which gate 5 recomputes. Each pair gives L r1
first and N r3 second.
- **The rounds**: 268 and 314. 41 and 48 put their newborn above every rule of
  their list, and every newborn of SECURITY_INCIDENT did, 8 and 14.
- **The security block.** Some rounds' lists hold two or more rules of
  SECURITY_INCIDENT, newborn not of it: 138 and 175. None of them put its
  newborn above some of those rules and below others.
- **Above the block.** 3 and 5 rounds put their newborn above every rule of
  SECURITY_INCIDENT their list held, and 2 and 5 of those above every rule of
  their list.
- **The oncall rule.** These are the rounds whose newborn is of neither queue and
  whose list holds no rule of SECURITY_INCIDENT.
  - **With no rule of ONCALL_ESCALATION listed**, 28 of 65 and 15 of 45 put
    their newborn above every rule of their list.
  - **With one listed**, 1 of 22 and 3 of 27 did.
- **Narrow drafts, short blocks.** These are the rounds whose list holds a rule
  of SECURITY_INCIDENT, newborn not of it. The cell is a draft of four or more
  conditions, against a list with one or two such rules.
  - **In the cell**, 1 of 11 and 3 of 13 put their newborn above every such
    rule.
  - **Outside it**, 2 of 159 and 2 of 204 did.
- **The ticket, at reported errors.**
  - **Against a listed rule whose region holds the ticket**, 504 of 510 and 573
    of 629 placements put the newborn above.
  - **Against the rest**, 1,870 of 3,304 and 3,614 of 6,520 did.

**What the notes say**, in the rounds whose list holds a rule of
SECURITY_INCIDENT, newborn not of it:
- **All 8 above the block say their rule is more specific**, an exception, or
  adds conditions: "La regla específica por producto (billing) es más concreta
  que cualquier regla que no incluya esa condición"; "This rule is more specific
  than R0072 and R0022 because it adds conditions". So do 264 of the 379 below
  it.
- **4 of the 8 name security in their note**, and 377 of the 379 below it.
- **Their reasoning counts conditions.** "R0022 solo requiere security_keyword
  true. Claramente R0022 es más general, y mi regla es más específica".
  - **The keyword's rule has one condition.**
  - **The round defines `beats` as an exception**, "de modo que la tuya manda
    donde casen las dos".
- **The queue's general rule reads its product as its domain.** `product =
  billing` went above every rule, "incluso si otras reglas genéricas (seguridad,
  severidad, off-hours, etc.) también casan".

**Codes tried and dropped.**
- **Over the notes.** Priority or criticality was in 5 of the 8 above the block
  and 283 of the 379 below it. A claim to win over any other rule was in 4 of
  the 8 and 72 of the 379.
- **Over the reasoning.** Specificity was in every reasoning, and priority in
  all but five.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **What each answer declared is its placement call's.** Rebuilt from its
     rule's accepted and refused edges, it is the call's `beats` and `loses_to`.
  2. **Every listed rule is of another queue and crosses the newborn.** They
     share a point and neither contains the other, as v1c lists.
  3. **Every answer declared a side against every rule of its list.**
  4. **Every list is the seeded shuffle v1c showed.**
  5. **The development set gives `DEVELOPMENT`'s counts.**

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates, prints pass or fail, and
writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
E1 to E4 pool L r2 and L r3. E5 and E6 pool N r1 and N r2.

  E1. **The security rules are one block.** Of the rounds whose list holds two
      or more rules of SECURITY_INCIDENT, newborn not of it, at least nineteen
      in twenty put the newborn above every one or below every one.
  E2. **A rule of ONCALL_ESCALATION holds the answer down.** Take the rounds
      whose newborn is of neither SECURITY_INCIDENT nor ONCALL_ESCALATION, and
      whose list holds no rule of SECURITY_INCIDENT. The share that put the
      newborn above every rule of their list is at least three times as high
      without a rule of ONCALL_ESCALATION as with one.
  E3. **The ticket.** At reported errors, of the placements against a listed
      rule whose region holds the round's ticket, at least nine in ten put the
      newborn above.
  E4. **Narrow drafts against short blocks.** Take the rounds whose list holds a
      rule of SECURITY_INCIDENT, newborn not of it. The share that put the
      newborn above every such rule is at least three times as high in one cell
      as in the others. The cell is a draft of four or more conditions, against
      a list with one or two such rules.
  E5. **Above the block, above the list.** Take the rounds that put their
      newborn above every rule of SECURITY_INCIDENT their list holds, newborn not
      of it. At least three quarters put it above every rule of their list.
  E6. **N alike.** E4's statement, in the control.

**Edge cases.**
- A share over nothing has no value, and a clause that reads one fails.
- A ratio holds where its first share is above nothing and at least the line
  times the second. It fails where either side has no round.

**The drafter's account**, from L r1 and N r3.
- **The answers put two queues first.**
  - **SECURITY_INCIDENT.** They place its rules as one block, nearly always
    below their newborn (E1).
  - **ONCALL_ESCALATION.** For a newborn of neither queue, they place its rules
    nearly as a block.
- **They put their newborn above the rules that would take its ticket** (E3),
  and above about half the rest.
- **So above every rule of the list is mostly what the list lacks.**
  - **A newborn of SECURITY_INCIDENT** is above every rule of its list.
  - **A list with neither queue's rule** comes out above every rule nearly half
    the time.
  - **With a rule of ONCALL_ESCALATION**, it seldom does (E2).
  - **With one of SECURITY_INCIDENT**, it does about once in fifty.
- **The few above the security rules read the list by its conditions.**
  - **Their notes** say their rule is more specific, an exception, or adds
    conditions, as the round's `beats` asks.
  - **The keyword's rule has one condition.** Read so, every rule of the list is
    more general, and they put their newborn above all of it (E5).
- **They do it with a narrow draft against a short block** (E4, E6). The more
  conditions the draft has, and the fewer security rules the list shows, the
  more general those rules look beside it.
- **Not by the draft.** A draft listed against security more than once that went
  above it once went below it at its other listings.

**The bet is E4.** It says what makes an answer read the security rules by their
conditions: a draft with many conditions, against few of those rules. **E1 is
trusted most**, at 313 of 313. **E6 is trusted least**: its cell held 13 rounds
in N r3, and 3 of them went above.

**What the drafter had seen**:
- **`FINDINGS_CORRECTIONS.md` whole, and `doors.json` and `byqueue.json`
  whole.** Among them, for every run:
  - every placement, by the kind of rule placed;
  - each listing of a gateway, by what its answer did with the round's security
    rules and with its whole list.
  In L r2 and L r3, seven climbs over the gateway put their newborn above every
  security rule of their round that contains the gateway, and above every rule
  of their list.
- **Counts printed before the development set was chosen**, for every run:
  - how many rounds showed a list;
  - how many put their newborn above every rule, below every rule, or some of
    each;
  - how many lists held a rule of SECURITY_INCIDENT, and how many of those put
    their newborn above every rule of the list;
  - how many newborns were of SECURITY_INCIDENT. Every one of them was above
    every rule of its list. That count is why no clause reads them.
- **L r1 and N r3**, as the development set above.
- **The prompts**: v1c's system prompt at level 1, its placement round and its
  report.

**What the drafter had not seen**: in L r2, L r3, N r1 and N r2, beyond those
counts and `doors.json`'s listings:
- what any answer did with its rules of SECURITY_INCIDENT, or of
  ONCALL_ESCALATION, as a set;
- any round's cause, draft, list length or ticket;
- any note or reasoning;
- any placement by the ticket.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-15, after `corrections/byqueue.py`.
L r1 and N r3 were read as the development set before the expectation above was
written, and the expectation was committed before the reading ran on the other
runs. Not a signed row, not on `STATUS.md`'s scoreboard, not a calibration
event. Zero API calls.

Usage:  python3 -m corrections.above --dry-run   # gates 1 to 5; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.above
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from fractions import Fraction
from typing import Any, Sequence

from harness.provenance import describe, environment

from edges import rebuild as erb
from manual import instrument as MI
from reasoned_loop import protocol as rp
from reuse import structure as st
from rung2.engine2 import Space, strictly_below

from . import byqueue as bq
from . import doors as dr
from . import fall as fl
from . import forgotten as fg
from . import plan

F = Fraction
SEC = fl.SEC
ONC = "ONCALL_ESCALATION"
ERROR = plan.ERROR
UNLABELLED = fl.UNLABELLED
ABOVE, BELOW, MIXED, NONE_LISTED = dr.ABOVE, dr.BELOW, dr.MIXED, dr.NONE_LISTED
CLIMB, CEDE = dr.CLIMB, dr.CEDE

DEVELOPMENT_RUNS = (plan.tag(plan.LABELLED, 1), plan.tag(UNLABELLED, 3))
HELD_OUT = tuple(plan.tag(plan.LABELLED, k) for k in range(2, plan.REPS + 1))
CONTROL = tuple(plan.tag(UNLABELLED, k) for k in range(1, plan.REPS))

# A draft is narrow at this many conditions, and a block of security rules short
# at this many.
NARROW = 4
SHORT = 2

# The expectation's lines.
E1_SHARE = F(19, 20)
E2_RATIO = F(3)
E3_SHARE = F(9, 10)
E4_RATIO = F(3)
E5_SHARE = F(3, 4)
E6_RATIO = F(3)

# Codes over a placement call's note, frozen on the development set. Also read,
# with no clause.
CODES = {
    "conditions": re.compile(r"espec[ií]fic|specific|excepci|exception|a[ñn]ade|\badds?\b"
                             r"|adicional|additional|subconjunto|subset|concret", re.I),
    "security": re.compile(r"segur|secur", re.I),
}

# The development set's counts, as the docstring gives them; gate 5 recomputes them.
DEVELOPMENT: dict[str, dict[str, Any]] = {
    DEVELOPMENT_RUNS[0]: {
        "rounds": 268, "above_every": 41, "newborn_security": 8, "newborn_security_above": 8,
        "security_listed": 170, "block_rounds": 138, "block_mixed": 0,
        "above_every_security": 3, "above_every_security_and_list": 2,
        "no_oncall": [28, 65], "oncall": [1, 22], "narrow_short": [1, 11], "others": [2, 159],
        "ticket_at_errors": [504, 510], "elsewhere_at_errors": [1870, 3304]},
    DEVELOPMENT_RUNS[1]: {
        "rounds": 314, "above_every": 48, "newborn_security": 14, "newborn_security_above": 14,
        "security_listed": 217, "block_rounds": 175, "block_mixed": 0,
        "above_every_security": 5, "above_every_security_and_list": 5,
        "no_oncall": [15, 45], "oncall": [3, 27], "narrow_short": [3, 13], "others": [2, 204],
        "ticket_at_errors": [573, 629], "elsewhere_at_errors": [3614, 6520]},
}

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-15, after corrections/byqueue.py. L r1 and N r3 "
    "are the development set, read before the expectation in the module's docstring was "
    "written; the expectation was committed before the reading ran on the other runs. Not a "
    "signed row; no verdict moves.")

share, frac = fg.share, fg.frac


def record_path():
    return plan.OUT / "above.json"


# ---------------------------------------------------------------------------
# One round
# ---------------------------------------------------------------------------

def first_queues(queue: str) -> set[str]:
    """The queues the answers put first, against a newborn of `queue`:
    SECURITY_INCIDENT, and ONCALL_ESCALATION for a newborn of neither."""
    return set() if queue == SEC else {SEC} if queue == ONC else {SEC, ONC}


def note_of(esc: dict[str, Any], rule: dict[str, Any]) -> str:
    """The placement call's note, whole; the rule's own if the call kept none."""
    call = bq.placement_call(esc) or {}
    return (call.get("payload") or {}).get("note") or rule.get("note") or ""


def rounds(record: dict[str, Any], ext: dict[str, int], space: Space,
           corpus: Sequence) -> list[dict[str, Any]]:
    """Every born rule whose round showed a list: what its answer did with the
    list, with its rules of SECURITY_INCIDENT and of ONCALL_ESCALATION, and with
    the rules whose region holds its ticket."""
    born = erb.births(record)
    rules = {r["rule_id"]: r for r in record["rules"]}
    escs = fg.escalation_at(record)
    out = []
    for idx in sorted(born):
        r = born[idx]
        esc = escs.get(idx) or {}
        listed = list(esc.get("listed") or [])
        if not listed:
            continue
        said = fl.declared(r)
        q = r["action"]
        pt = dr.point(space, corpus[idx])
        secs = [x for x in listed if rules[x]["action"] == SEC]
        oncs = [x for x in listed if rules[x]["action"] == ONC]
        first = [x for x in listed if rules[x]["action"] in first_queues(q)]
        ticket = [x for x in listed if pt & ext[x]]
        out.append({
            "born_at": idx, "newborn": r["rule_id"], "queue": q, "cause": esc.get("kind"),
            "draft": bq.draft_key(r), "conditions": len(r["conditions"]),
            "listed": len(listed),
            "list_toward": dr.toward(said, listed),
            "security": len(secs), "security_toward": dr.toward(said, secs),
            "oncall": len(oncs), "oncall_toward": dr.toward(said, oncs),
            "first": len(first), "first_toward": dr.toward(said, first),
            "ticket": len(ticket), "ticket_toward": dr.toward(said, ticket),
            "placed": {"ticket": dict(sorted(Counter(dr.side_of(said, x)
                                                     for x in ticket).items())),
                       "elsewhere": dict(sorted(Counter(dr.side_of(said, x) for x in listed
                                                        if x not in ticket).items()))},
            "codes": {k: bool(p.search(note_of(esc, r))) for k, p in CODES.items()},
        })
    return out


# ---------------------------------------------------------------------------
# What the rounds give
# ---------------------------------------------------------------------------

def count(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(r[key]) for r in rows).items()))


def rate(rows: list[dict[str, Any]], hit) -> dict[str, Any]:
    n = sum(1 for r in rows if hit(r))
    return {"hits": n, "of": len(rows), "rate": frac(share(n, len(rows)))}


def group(r: dict[str, Any]) -> str:
    """A round by its newborn's queue and what its list holds of the queues put
    first."""
    if r["queue"] == SEC:
        return "newborn_security"
    if r["security"]:
        return "security_listed"
    if r["queue"] != ONC and r["oncall"]:
        return "oncall_listed"
    return "neither_listed"


def against_security(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The rounds whose list holds a rule of SECURITY_INCIDENT, newborn not of it."""
    return [r for r in rows if r["queue"] != SEC and r["security"]]


def narrow_short(r: dict[str, Any]) -> bool:
    return r["conditions"] >= NARROW and r["security"] <= SHORT


def summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, list] = {}
    for r in rows:
        groups.setdefault(group(r), []).append(r)
    sec = against_security(rows)
    onc = [r for r in rows if r["queue"] not in (SEC, ONC) and r["oncall"] >= 2]
    above_sec = [r for r in sec if r["security_toward"] == ABOVE]
    by_cause: dict[str, Counter] = {}
    for r in rows:
        c = by_cause.setdefault(str(r["cause"]), Counter())
        for where in ("ticket", "elsewhere"):
            for side, v in r["placed"][where].items():
                c[f"{where}:{side}"] += v
    return {
        "rounds": len(rows),
        "list_toward": count(rows, "list_toward"),
        "by_group": {g: count(v, "list_toward") for g, v in sorted(groups.items())},
        "security_block": count([r for r in sec if r["security"] >= 2], "security_toward"),
        "oncall_block": count(onc, "oncall_toward"),
        "above_every_security": {"rounds": len(above_sec),
                                 "list_toward": count(above_sec, "list_toward")},
        "narrow_short": {
            "narrow_short": rate([r for r in sec if narrow_short(r)],
                                 lambda r: r["security_toward"] == ABOVE),
            "others": rate([r for r in sec if not narrow_short(r)],
                           lambda r: r["security_toward"] == ABOVE)},
        "placements_by_cause": {k: dict(sorted(v.items())) for k, v in sorted(by_cause.items())},
    }


def also(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Read with no clause: what each side of the security block says in its
    note, by cause, by the draft's conditions, by the block's length, and the
    drafts listed against security more than once."""
    sec = against_security(rows)
    sides = {s: [r for r in sec if r["security_toward"] == s] for s in (ABOVE, BELOW)}
    drafts: dict[str, Counter] = {}
    for r in sec:
        drafts.setdefault(r["draft"], Counter())[r["security_toward"]] += 1
    both = {d: dict(sorted(c.items())) for d, c in sorted(drafts.items())
            if c.get(ABOVE) and sum(c.values()) > 1}

    def by(key) -> dict[str, dict[str, Any]]:
        g: dict[str, list] = {}
        for r in sec:
            g.setdefault(str(key(r)), []).append(r)
        return {k: rate(v, lambda r: r["security_toward"] == ABOVE) for k, v in sorted(g.items())}

    return {
        "codes": {s: {k: rate(v, lambda r, k=k: r["codes"][k]) for k in CODES}
                  for s, v in sides.items()},
        "above_security_by_cause": by(lambda r: r["cause"]),
        "above_security_by_conditions": by(lambda r: min(r["conditions"], NARROW)),
        "above_security_by_block": by(lambda r: min(r["security"], SHORT + 1)),
        "drafts_above_security_listed_again": both,
    }


def development(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """The counts the docstring gives of a run of the development set."""
    s = summary(rows)
    sec = against_security(rows)
    err = s["placements_by_cause"].get(ERROR) or {}
    neither = [r for r in rows if r["queue"] not in (SEC, ONC) and not r["security"]]
    return {
        "rounds": len(rows),
        "above_every": sum(r["list_toward"] == ABOVE for r in rows),
        "newborn_security": sum(r["queue"] == SEC for r in rows),
        "newborn_security_above": sum(r["queue"] == SEC and r["list_toward"] == ABOVE
                                      for r in rows),
        "security_listed": len(sec),
        "block_rounds": sum(r["security"] >= 2 for r in sec),
        "block_mixed": sum(r["security"] >= 2 and r["security_toward"] == MIXED for r in sec),
        "above_every_security": sum(r["security_toward"] == ABOVE for r in sec),
        "above_every_security_and_list": sum(r["security_toward"] == ABOVE
                                             and r["list_toward"] == ABOVE for r in sec),
        "no_oncall": [sum(r["list_toward"] == ABOVE for r in neither if not r["oncall"]),
                      sum(1 for r in neither if not r["oncall"])],
        "oncall": [sum(r["list_toward"] == ABOVE for r in neither if r["oncall"]),
                   sum(1 for r in neither if r["oncall"])],
        "narrow_short": [s["narrow_short"]["narrow_short"]["hits"],
                         s["narrow_short"]["narrow_short"]["of"]],
        "others": [s["narrow_short"]["others"]["hits"], s["narrow_short"]["others"]["of"]],
        "ticket_at_errors": [err.get(f"ticket:{CLIMB}", 0),
                             sum(v for k, v in err.items() if k.startswith("ticket:"))],
        "elsewhere_at_errors": [err.get(f"elsewhere:{CLIMB}", 0),
                                sum(v for k, v in err.items() if k.startswith("elsewhere:"))],
    }


# ---------------------------------------------------------------------------
# One run
# ---------------------------------------------------------------------------

def read_run(record: dict[str, Any], space: Space, corpus: Sequence,
             tag: str | None = None) -> dict[str, Any]:
    ext = dr.extensions(record, space)
    rows = rounds(record, ext, space, corpus)
    rules = {r["rule_id"]: r for r in record["rules"]}
    born = erb.births(record)
    escs = fg.escalation_at(record)

    def payload_sides(idx: int) -> dict[str, str]:
        p = (bq.placement_call(escs[idx]) or {}).get("payload") or {}
        out = {x: "beats" for x in p.get("beats") or []}
        out.update({x: "loses_to" for x in p.get("loses_to") or []})
        return out

    def crosses(n: str, x: str) -> bool:
        a, b = ext[n], ext[x]
        return (bool(a & b) and not strictly_below(a, b) and not strictly_below(b, a)
                and rules[n]["action"] != rules[x]["action"])

    def shown(idx: int) -> bool:
        esc = escs[idx]
        listed = list(esc.get("listed") or [])
        first = (esc.get("calls") or [{}])[0].get("listed")
        return rp.listing(sorted(listed), idx, 0) == listed and first == listed

    idxs = [r["born_at"] for r in rows]
    gates_out = [
        {"gate": 1, "what": "what each answer declared, rebuilt from its rule's accepted and "
                            "refused edges, is its placement call's beats and loses_to",
         "passes": all({x: s for x, (s, _) in fl.declared(born[i]).items()} == payload_sides(i)
                       for i in idxs)},
        {"gate": 2, "what": "every listed rule is of another queue and crosses the newborn",
         "passes": all(crosses(born[i]["rule_id"], x) for i in idxs
                       for x in escs[i].get("listed") or [])},
        {"gate": 3, "what": "every answer declared a side against every rule of its list",
         "passes": all(dr.side_of(fl.declared(born[i]), x) != dr.NO_SIDE for i in idxs
                       for x in escs[i].get("listed") or [])},
        {"gate": 4, "what": "every list is the seeded shuffle v1c showed",
         "passes": all(shown(i) for i in idxs)},
    ]
    run = {"summary": summary(rows), "also_read": also(rows), "rounds": rows,
           "gates": gates_out}
    if tag in DEVELOPMENT_RUNS:
        run["development"] = development(rows)
        gates_out.append({"gate": 5, "what": "the development set gives DEVELOPMENT's counts",
                          "passes": run["development"] == DEVELOPMENT.get(tag)})
    return run


def read_all_runs(records: dict[str, dict], space: Space, corpus: Sequence) -> dict[str, dict]:
    return {tag: read_run(rec, space, corpus, tag=tag) for tag, rec in records.items()}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def pooled(runs: dict[str, dict[str, Any]], tags: Sequence[str]) -> list[dict[str, Any]]:
    return [r for t in tags if t in runs for r in runs[t]["rounds"]]


def block(rows: list[dict[str, Any]]) -> tuple[int, int]:
    b = [r for r in against_security(rows) if r["security"] >= 2]
    return sum(r["security_toward"] in (ABOVE, BELOW) for r in b), len(b)


def oncall_split(rows: list[dict[str, Any]]) -> tuple[tuple[int, int], tuple[int, int]]:
    """The rounds whose newborn is of neither queue and whose list holds no rule
    of SECURITY_INCIDENT, above every rule of their list: without a rule of
    ONCALL_ESCALATION, and with one."""
    n = [r for r in rows if r["queue"] not in (SEC, ONC) and not r["security"]]
    out = []
    for keep in (lambda r: not r["oncall"], lambda r: bool(r["oncall"])):
        g = [r for r in n if keep(r)]
        out.append((sum(r["list_toward"] == ABOVE for r in g), len(g)))
    return out[0], out[1]


def ticket_at_errors(rows: list[dict[str, Any]]) -> tuple[int, int]:
    c: Counter = Counter()
    for r in rows:
        if r["cause"] == ERROR:
            c.update(r["placed"]["ticket"])
    return c.get(CLIMB, 0), sum(c.values())


def narrow_split(rows: list[dict[str, Any]]) -> tuple[tuple[int, int], tuple[int, int]]:
    """The rounds against security above every such rule: in the cell of a narrow
    draft against a short block, and outside it."""
    sec = against_security(rows)
    out = []
    for keep in (narrow_short, lambda r: not narrow_short(r)):
        g = [r for r in sec if keep(r)]
        out.append((sum(r["security_toward"] == ABOVE for r in g), len(g)))
    return out[0], out[1]


def wholesale(rows: list[dict[str, Any]]) -> tuple[int, int]:
    a = [r for r in against_security(rows) if r["security_toward"] == ABOVE]
    return sum(r["list_toward"] == ABOVE for r in a), len(a)


def share_clause(cid: str, what: str, got: tuple[int, int], line: Fraction) -> dict[str, Any]:
    part, whole = got
    return {"clause": cid, "what": what,
            "reading": {"part": part, "of": whole, "share": frac(share(part, whole))},
            "holds": whole > 0 and F(part, whole) >= line}


def ratio_clause(cid: str, what: str, got: tuple[tuple[int, int], tuple[int, int]],
                 line: Fraction) -> dict[str, Any]:
    (ha, na), (hb, nb) = got
    ra, rb = share(ha, na), share(hb, nb)
    holds = ra is not None and rb is not None and ra > 0 and ra >= line * rb
    ratio = ra / rb if ra is not None and rb else None
    return {"clause": cid, "what": what,
            "reading": {"first": {"part": ha, "of": na, "share": frac(ra)},
                        "second": {"part": hb, "of": nb, "share": frac(rb)},
                        "ratio": frac(ratio)},
            "holds": holds}


def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    held = pooled(runs, HELD_OUT)
    ctrl = pooled(runs, CONTROL)
    return [
        share_clause("E1", "of the rounds whose list holds two or more rules of "
                           "SECURITY_INCIDENT, newborn not of it, at least nineteen in twenty put "
                           "the newborn above every one or below every one", block(held), E1_SHARE),
        ratio_clause("E2", "of the rounds whose newborn is of neither SECURITY_INCIDENT nor "
                           "ONCALL_ESCALATION and whose list holds no rule of SECURITY_INCIDENT, "
                           "the share above every rule of their list is at least three times as "
                           "high without a rule of ONCALL_ESCALATION as with one",
                     oncall_split(held), E2_RATIO),
        share_clause("E3", "at reported errors, of the placements against a listed rule whose "
                           "region holds the round's ticket, at least nine in ten put the newborn "
                           "above", ticket_at_errors(held), E3_SHARE),
        ratio_clause("E4", "of the rounds whose list holds a rule of SECURITY_INCIDENT, newborn "
                           "not of it, the share above every such rule is at least three times as "
                           "high where the draft has four or more conditions and the list one or "
                           "two such rules as in the others", narrow_split(held), E4_RATIO),
        share_clause("E5", "in N r1 and N r2, of the rounds above every rule of "
                           "SECURITY_INCIDENT their list holds, newborn not of it, at least three "
                           "quarters above every rule of their list", wholesale(ctrl), E5_SHARE),
        ratio_clause("E6", "in N r1 and N r2, E4's statement", narrow_split(ctrl), E6_RATIO),
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> dict[str, dict]:
    return {plan.tag(a, k): json.loads(plan.run_path(a, k).read_text())
            for a in (plan.LABELLED, UNLABELLED) for k in range(1, plan.REPS + 1)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why some answers put their newborn above every "
                                             "rule of their list (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 5 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/above.py writes {record_path()}")
    records = read_all()
    runs = read_all_runs(records, MI.space(), list(MI.corpus()))
    checked = [{"run": t, **g} for t, r in runs.items() for g in r["gates"]]
    for g in checked:
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    expectation = read_expectation(runs)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "surface": "every born rule of each run whose round listed rules, by what its answer "
                   "declared of every listed rule; every placement, by whether the rule's "
                   "region holds the round's ticket",
        "constants": {"NARROW": NARROW, "SHORT": SHORT,
                      "E1_SHARE": str(E1_SHARE), "E2_RATIO": str(E2_RATIO),
                      "E3_SHARE": str(E3_SHARE), "E4_RATIO": str(E4_RATIO),
                      "E5_SHARE": str(E5_SHARE), "E6_RATIO": str(E6_RATIO),
                      "CODES": {k: p.pattern for k, p in CODES.items()},
                      "DEVELOPMENT_RUNS": list(DEVELOPMENT_RUNS), "HELD_OUT": list(HELD_OUT),
                      "CONTROL": list(CONTROL), "DEVELOPMENT": DEVELOPMENT},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        s = r["summary"]
        print(f"  {t}: {s['rounds']} rounds, lists {s['list_toward']}; security block "
              f"{s['security_block']}; above every security rule "
              f"{s['above_every_security']['list_toward']}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
