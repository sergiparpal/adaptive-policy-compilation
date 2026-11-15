"""
WHY THE DOORS DECLARED THEMSELVES ABOVE THE GATEWAY.
`corrections/gateway.py` found few doors into the gateways, and every declared
door's edge its own answer. In L, of the rounds that listed a gateway, nine in
ten put it above their newborn; the doors' answers put their newborn above it.
`FINDINGS_CORRECTIONS.md`, *Why so many rules sit above the gateway*, *What it
does not settle*, item 1, and `IDEAS.md` leave why, and say the reasoning is in
the records. Asked for by Sergi on 2026-11-15, after that reading. Free on the
records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
**A listing** is a round that listed a gateway of `gateway.json` born before it,
once per gateway, as `corrections/gateway.py`'s `answers` counts them. A round
that listed both of L r2's gateways is counted once for each. Its **side** is
what its answer declared of the gateway, whatever the engine did with it:
  climb  the newborn above the gateway, in `beats`;
  cede   the newborn below it, in `loses_to`.
The climbs the engine installed are the declared doors.

For each listing the reading takes, from the record and the space:
- **the other keyword rules**: the rules its round listed, the run's gateways
  left out, of a queue other than SECURITY_INCIDENT, whose region lies inside
  the keyword's half;
- **the security rules**: the rules of SECURITY_INCIDENT its round listed whose
  region strictly contains the gateway's. The gateway beats each of them by
  containment;
- what the answer did with each set: its newborn **above every** one, **below
  every** one, some of each, or none listed;
- the newborn's points against the gateway's, narrower, broader or equal, and
  whether the round's ticket lies inside the gateway.

**Every placement of every round** is also read, each rule a round listed by the
side its answer declared of it, and by the rule's kind: a rule of
SECURITY_INCIDENT, a gateway, another keyword rule, or a rule outside the
keyword's half. N r1 and N r2 have no gateway, and are read for their
placements only.

--------------------------------------------------------------------------
THE DEVELOPMENT SET
--------------------------------------------------------------------------
**L r1 is the development set.** Every clause reads L r2 and L r3, pooled, and
N r3 as the control. What the drafter read of L r1, before writing anything
below:
- **its 78 listings**, each with its newborn's queue, conditions and points, the
  cause of its escalation, its round's length, and what its answer declared of
  the gateway, of the round's other keyword rules and of its security rules;
- **the five climbs' reasoning**, the passages that name the gateway, and the
  same passages of every sixth cede, thirteen in all;
- **the counts of five candidate codes** over those passages, below;
- **every placement of every round**, by kind and side.

**Its counts**, `DEVELOPMENT`, which gate 5 recomputes:
- **the listings**: 78, of which 5 climb and 73 cede. No round's ticket lies
  inside the gateway. 3 of the climbs' newborns are narrower than the gateway,
  and 41 of the cedes';
- **the placements**: below 678 of the 689 rules of SECURITY_INCIDENT, 59 of the
  63 other keyword rules, and 1,890 of the 6,423 rules outside the keyword's
  half;
- **the other keyword rules**: 3 climbs' rounds listed one, and all 3 put their
  newborn above every one. 58 cedes' rounds listed one, and 57 put their newborn
  below every one;
- **the security rules**: every listing's round listed one. 4 of the 5 climbs
  put their newborn below every one, and all 73 cedes.

**What the reasoning says**, read in the passages:
- **The cedes call the gateway security**, by its keyword: "Pierde porque
  security", "Security, so loses_to", "R0061 is about security, so security
  incidents should win".
- **Four of the climbs read it by its queue**: "R0061 is T2, so our rule should
  beat it". **Two say the security rules will win over both anyway**: "since
  security incident rules exist and are higher priority, we can ignore this T2
  rule because if security keyword is true, security incident will win anyway".
  R0062's answer weighed both readings and chose the queue: "I'll treat it as a
  technical rule".
- **One climb, R0273, placed its list by the number of conditions**, and put
  its newborn above every security rule of its round too.

**Codes tried on L r1 and dropped**, because over the passages they told the
sides apart by little or not at all, matched case-blind on the lines that name
the gateway and the two after each:
- that the gateway is not a security incident: 4 of the 5 climbs, 29 of the 73
  cedes;
- that it is security: 3 of the climbs, 53 of the cedes;
- more specific, in English or Spanish: 4 of the climbs, 60 of the cedes;
- that the security rules will win anyway, or the order is irrelevant: 2 of the
  climbs, 32 of the cedes;
- that the gateway is odd or a mistake: 2 of the climbs, 24 of the cedes.
A passage restates the gateway's conditions and queue, and an answer that cedes
weighs both readings before it chooses. So the reading reads what each answer
declared, which is structural.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The listings are `gateway.json`'s.** In every run their counts, by what
     the answer declared of the gateway and what the engine did, are its
     `rounds_that_listed_a_gateway`.
  2. **The installed climbs are `gateway.json`'s door_win edges.**
  3. **Every listing's newborn crosses its gateway**: they share a point,
     neither contains the other, and their queues differ, as v1c lists.
  4. **The engine cannot keep both.** Every installed climb's declared loss to a
     security rule that contains its gateway was refused for a cycle.
  5. **The development set gives `DEVELOPMENT`'s counts.**

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates, prints pass or fail, and
writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
F1 to F4 pool L r2 and L r3. F5 and F6 read N r3, the one N run with a gateway.

  F1. **Keyword rules are placed as security rules.** Of the placements against
      the other keyword rules, the gateways left out, at least three quarters
      put the newborn below.
  F2. **The climbs read them by their queue.** Of the climbs whose round listed
      another keyword rule, at least three quarters put the newborn above every
      such rule.
  F3. **The cedes read them by the keyword.** Of the cedes whose round listed
      another keyword rule, at least three quarters put the newborn below every
      such rule.
  F4. **The climbs still yield to security.** Of the climbs whose round listed a
      security rule, at least three quarters put the newborn below every one.
  F5. **N alike, by queue.** In N r3, F2's statement.
  F6. **N alike, to security.** In N r3, F4's statement.

A share over nothing has no value, and a clause that reads one fails.

**The drafter's account**, from L r1.
- **The round asks for a side against every rule it lists**: `beats` if the
  draft is an exception to it, `loses_to` if it is a general case below it.
- **The answers place the list by the security queue.** They put their newborn
  below nearly every rule of SECURITY_INCIDENT, and above most of the rest,
  because security incidents come first.
- **A keyword rule of another queue is placed as a security rule** (F1). The
  answers call it security, by its keyword. The gateway is such a rule, so nine
  answers in ten put it above their newborn, and put the round's other keyword
  rules above it too (F3).
- **The climbs read it by its queue** (F2): a rule of T2_TECHNICAL, not a
  security incident. Some say the security rules will win over both anyway. So
  they put their newborn above the gateway, and above the round's other keyword
  rules of other queues. The doors are the climbs the engine installed.
- **They still yield to security** (F4). They put their newborn below the
  security rules, in the same answer.
- **The engine cannot keep both.** The gateway lies inside the keyword's
  security rule and beats it by containment. The round does not show that: its
  list gives each rule's declared wins, not what containment orders. The loop
  installs a newborn's wins before its losses. So a climb the engine installs is
  above the security rule too, and its own loss to that rule closes a cycle and
  is refused (gate 4).
- **Not by the ticket, nor by size.** No round's ticket lies inside the
  gateway, and the climbs' newborns are narrower than it about as often as the
  cedes'.
- **N r3 is alike**, with no label (F5, F6). Its gateway is a rule of
  T1_GENERAL.

**The bet is F2.** It says the doors' answers read the keyword rules of other
queues by their queue, and not the gateway alone. **F3 is trusted most**, at 57
of 58 on L r1. **F5 is trusted least**: N r3's gateway is of another queue, and
by queue an answer can put its newborn below a keyword rule of a queue it ranks
above its own.

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole, and `gateway.json` whole: each run's gateways
  and their conditions; the doors, by rule, queue, kind and the policy's
  verdict; the counts of the rounds that listed a gateway, by what the answer
  declared and what the engine did, in every run; the newborns of the pairs
  through a gateway, with their conditions and what their answers declared of
  it, among them L r2's R0095, R0068 and R0073 below it and L r3's R0090 above
  it; R0051's and R0213's conditions;
- L r1, as the development set above;
- in N r1's record, its first escalation's fields and the opening of its
  placement call's reasoning;
- v1c's system prompt at level 1, its placement round and its base paragraph;
- `authorship/loop.py`'s installation order, and `rung2/engine2.py`'s
  containment and `try_edge`.

**What the drafter had not seen**: in L r2, L r3 and N r3, what any answer
declared of a rule other than its gateway, any listing's other keyword rules or
security rules, any placement's kind, and any reasoning.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-15, after `corrections/gateway.py`.
L r1 was read as the development set before the expectation above was written,
and the expectation was committed before the reading ran on the other runs. Not
a signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API
calls.

Usage:  python3 -m corrections.doors --dry-run   # gates 1 to 5; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.doors
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from typing import Any, Sequence

from harness.domain import ATTRIBUTES
from harness.provenance import describe, environment

from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import EDGE_CYCLE, EDGE_OK, Space, strictly_below

from . import fall as fl
from . import forgotten as fg
from . import gateway as gw
from . import plan

F = Fraction
SEC = fl.SEC
UNLABELLED = fl.UNLABELLED

# A listing's side: what the newborn's answer declared of the gateway.
CLIMB, CEDE, NO_SIDE = "climb", "cede", "none"
SIDES = (CLIMB, CEDE, NO_SIDE)
# What an answer did with a set of the rules its round listed.
ABOVE, BELOW, MIXED, NONE_LISTED = "above_every", "below_every", "mixed", "none_listed"
TOWARD = (ABOVE, BELOW, MIXED, NONE_LISTED)
# A placement, by the rule placed against the newborn.
SECURITY, GATEWAY, KEYWORD, OUTSIDE = "security", "gateway", "keyword", "outside"
KINDS = (SECURITY, GATEWAY, KEYWORD, OUTSIDE)
# The newborn's region against the gateway's.
NARROWER, BROADER, EQUAL = "narrower", "broader", "equal"
SIZES = (NARROWER, BROADER, EQUAL)

DEVELOPMENT_RUN = plan.tag(plan.LABELLED, 1)
HELD_OUT = tuple(plan.tag(plan.LABELLED, k) for k in range(2, plan.REPS + 1))
CONTROL = plan.tag(UNLABELLED, 3)

# The expectation's lines.
F1_SHARE = F(3, 4)
F2_SHARE = F(3, 4)
F3_SHARE = F(3, 4)
F4_SHARE = F(3, 4)
F5_SHARE = F(3, 4)
F6_SHARE = F(3, 4)

# The development set's counts, as the docstring gives them; gate 5 recomputes them.
DEVELOPMENT: dict[str, int] = {
    "listings": 78, "climbs": 5, "cedes": 73, "inside": 0,
    "climbs_narrower": 3, "cedes_narrower": 41,
    "security_placed": 689, "security_below": 678,
    "keyword_placed": 63, "keyword_below": 59,
    "outside_placed": 6423, "outside_below": 1890,
    "climbs_with_keyword_rules": 3, "climbs_above_every_keyword_rule": 3,
    "cedes_with_keyword_rules": 58, "cedes_below_every_keyword_rule": 57,
    "climbs_with_security_rules": 5, "climbs_below_every_security_rule": 4,
    "cedes_below_every_security_rule": 73,
}

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-15, after corrections/gateway.py. L r1 is the "
    "development set, read before the expectation in the module's docstring was written; the "
    "expectation was committed before the reading ran on the other runs. Not a signed row; no "
    "verdict moves.")

share, frac = fg.share, fg.frac


def record_path():
    return plan.OUT / "doors.json"


# ---------------------------------------------------------------------------
# Regions
# ---------------------------------------------------------------------------

def extensions(record: dict[str, Any], space: Space) -> dict[str, int]:
    """Every rule's region of the space, from its conditions."""
    return {r["rule_id"]: space.extension(rule_from(r).conditions) for r in record["rules"]}


def keyword_rule(region: int, kw: int) -> bool:
    """A rule whose region lies inside the keyword's half."""
    return region != 0 and region & ~kw == 0


def point(space: Space, case: Any) -> int:
    """The one point of the space a ticket is."""
    m = space.full
    for a in ATTRIBUTES:
        m &= space.mask[a][getattr(case, a)]
    return m


# ---------------------------------------------------------------------------
# What an answer declared
# ---------------------------------------------------------------------------

def side_of(said: dict[str, tuple[str, str]], rid: str) -> str:
    s = said.get(rid, (None, None))[0]
    return CLIMB if s == "beats" else CEDE if s == "loses_to" else NO_SIDE


def toward(said: dict[str, tuple[str, str]], ids: Sequence[str]) -> str:
    """What the answer did with every rule of `ids`: its newborn above every one,
    below every one, or some of each."""
    if not ids:
        return NONE_LISTED
    sides = {said.get(x, (None, None))[0] for x in ids}
    return ABOVE if sides == {"beats"} else BELOW if sides == {"loses_to"} else MIXED


def size_of(newborn: int, gate: int) -> str:
    a, b = newborn.bit_count(), gate.bit_count()
    return NARROWER if a < b else BROADER if a > b else EQUAL


# ---------------------------------------------------------------------------
# One run
# ---------------------------------------------------------------------------

def listings(record: dict[str, Any], gates: list[dict[str, Any]], ext: dict[str, int], kw: int,
             space: Space, corpus: Sequence) -> list[dict[str, Any]]:
    """Every round that listed a gateway born before it, once per gateway, as
    `corrections/gateway.py`'s `answers` counts them: the side its answer
    declared, the newborn against the gateway, and what the answer did with the
    round's other keyword rules and with its security rules that contain the
    gateway."""
    born = erb.births(record)
    rules = {r["rule_id"]: r for r in record["rules"]}
    escs = fg.escalation_at(record)
    gate_ids = {g["rule_id"] for g in gates}
    out = []
    for idx in sorted(born):
        r = born[idx]
        esc = escs.get(idx) or {}
        listed = list(esc.get("listed") or [])
        said = fl.declared(r)
        n = r["rule_id"]
        for g in gates:
            gid = g["rule_id"]
            if idx <= g["born_at"] or gid not in listed:
                continue
            others = sorted(x for x in listed if x not in gate_ids
                            and rules[x]["action"] != SEC and keyword_rule(ext[x], kw))
            secs = sorted(x for x in listed if rules[x]["action"] == SEC
                          and strictly_below(ext[gid], ext[x]))
            en, eg = ext[n], ext[gid]
            out.append({
                "born_at": idx, "newborn": n, "action": r["action"], "cause": esc.get("kind"),
                "gateway": gid, "side": side_of(said, gid),
                "said": list(said.get(gid, ("none", "none"))),
                "listed": len(listed),
                "points": en.bit_count(), "gateway_points": eg.bit_count(),
                "shared": (en & eg).bit_count(), "size": size_of(en, eg),
                "inside": bool(point(space, corpus[idx]) & eg),
                "crosses": (bool(en & eg) and not strictly_below(en, eg)
                            and not strictly_below(eg, en)
                            and r["action"] != rules[gid]["action"]),
                "keyword_rules": others, "keyword_toward": toward(said, others),
                "security_rules": secs, "security_toward": toward(said, secs),
                "security_losses": {x: said[x][1] for x in secs
                                    if said.get(x, (None, None))[0] == "loses_to"},
            })
    return out


def placements(record: dict[str, Any], gates: list[dict[str, Any]], ext: dict[str, int],
               kw: int) -> dict[str, int]:
    """Every rule every round listed, by its kind and the side the answer
    declared of it: a rule of SECURITY_INCIDENT, a gateway, a keyword rule of
    another queue, or a rule outside the keyword's half."""
    born = erb.births(record)
    rules = {r["rule_id"]: r for r in record["rules"]}
    escs = fg.escalation_at(record)
    gate_ids = {g["rule_id"] for g in gates}
    c: Counter = Counter()
    for idx in sorted(born):
        listed = list((escs.get(idx) or {}).get("listed") or [])
        if not listed:
            continue
        said = fl.declared(born[idx])
        for x in listed:
            kind = (SECURITY if rules[x]["action"] == SEC else GATEWAY if x in gate_ids
                    else KEYWORD if keyword_rule(ext[x], kw) else OUTSIDE)
            c[f"{kind}:{side_of(said, x)}"] += 1
    return dict(sorted(c.items()))


def by_side(ls: list[dict[str, Any]], key: str) -> dict[str, dict[str, int]]:
    """The listings of each side, counted by `key`."""
    def name(v: Any) -> str:
        return str(v).lower() if isinstance(v, bool) else str(v)

    return {s: dict(sorted(Counter(name(l[key]) for l in ls if l["side"] == s).items()))
            for s in SIDES if any(l["side"] == s for l in ls)}


def development(run: dict[str, Any]) -> dict[str, int]:
    """The counts the docstring gives of the development set."""
    ls, pl = run["listings"], run["summary"]["placements"]

    def placed(kind: str, side: str | None = None) -> int:
        return sum(v for k, v in pl.items()
                   if k.split(":")[0] == kind and (side is None or k.split(":")[1] == side))

    climbs = [l for l in ls if l["side"] == CLIMB]
    cedes = [l for l in ls if l["side"] == CEDE]
    return {
        "listings": len(ls), "climbs": len(climbs), "cedes": len(cedes),
        "inside": sum(l["inside"] for l in ls),
        "climbs_narrower": sum(l["size"] == NARROWER for l in climbs),
        "cedes_narrower": sum(l["size"] == NARROWER for l in cedes),
        "security_placed": placed(SECURITY), "security_below": placed(SECURITY, CEDE),
        "keyword_placed": placed(KEYWORD), "keyword_below": placed(KEYWORD, CEDE),
        "outside_placed": placed(OUTSIDE), "outside_below": placed(OUTSIDE, CEDE),
        "climbs_with_keyword_rules": sum(bool(l["keyword_rules"]) for l in climbs),
        "climbs_above_every_keyword_rule": sum(l["keyword_toward"] == ABOVE for l in climbs),
        "cedes_with_keyword_rules": sum(bool(l["keyword_rules"]) for l in cedes),
        "cedes_below_every_keyword_rule": sum(l["keyword_toward"] == BELOW for l in cedes),
        "climbs_with_security_rules": sum(bool(l["security_rules"]) for l in climbs),
        "climbs_below_every_security_rule": sum(l["security_toward"] == BELOW for l in climbs),
        "cedes_below_every_security_rule": sum(l["security_toward"] == BELOW for l in cedes),
    }


def read_run(record: dict[str, Any], gateway_run: dict[str, Any], space: Space,
             corpus: Sequence, tag: str | None = None) -> dict[str, Any]:
    """One run's listings of its gateways, every placement of its rounds, and the
    gates. `gateway_run` is the run's entry in `gateway.json`."""
    gates = gateway_run.get("gateways") or []
    ext = extensions(record, space)
    kw = fl.keyword(space)
    ls = listings(record, gates, ext, kw, space, corpus)
    pl = placements(record, gates, ext, kw)
    installed = sorted((l["newborn"], l["gateway"]) for l in ls
                       if l["side"] == CLIMB and l["said"][1] == EDGE_OK)
    summary = {
        "gateways": [g["rule_id"] for g in gates],
        "listings": len(ls),
        "sides": dict(sorted(Counter(l["side"] for l in ls).items())),
        "said": dict(sorted(Counter(f"{l['said'][0]}:{l['said'][1]}" for l in ls).items())),
        "installed": [list(p) for p in installed],
        "keyword_toward": by_side(ls, "keyword_toward"),
        "security_toward": by_side(ls, "security_toward"),
        "size": by_side(ls, "size"),
        "inside": by_side(ls, "inside"),
        "queue": by_side(ls, "action"),
        "cause": by_side(ls, "cause"),
        "placements": pl,
    }
    answers = (gateway_run.get("added_after_the_first_run") or {}).get("answers") or {}
    door_win = sorted((d["door"], d["gateway"]) for d in gateway_run.get("doors") or []
                      if d["kind"] == gw.DOOR_WIN)
    gates_out = [
        {"gate": 1, "what": "the listings are gateway.json's, by what each answer declared of "
                            "its gateway and what the engine did",
         "passes": summary["said"] == dict(sorted(
             (answers.get("rounds_that_listed_a_gateway") or {}).items()))},
        {"gate": 2, "what": "the climbs the engine installed are gateway.json's door_win edges",
         "passes": installed == door_win},
        {"gate": 3, "what": "every listing's newborn crosses its gateway, of another queue",
         "passes": all(l["crosses"] for l in ls)},
        {"gate": 4, "what": "every installed climb's declared loss to a security rule that "
                            "contains its gateway was refused for a cycle",
         "passes": all(why == EDGE_CYCLE for l in ls
                       if l["side"] == CLIMB and l["said"][1] == EDGE_OK
                       for why in l["security_losses"].values())},
    ]
    run = {"summary": summary, "listings": ls, "gates": gates_out}
    if tag == DEVELOPMENT_RUN:
        run["development"] = development(run)
        gates_out.append({"gate": 5, "what": "the development set gives DEVELOPMENT's counts",
                          "passes": run["development"] == DEVELOPMENT})
    return run


def read_all_runs(records: dict[str, dict], gateway_record: dict[str, Any], space: Space,
                  corpus: Sequence) -> dict[str, dict]:
    return {tag: read_run(rec, gateway_record["runs"][tag], space, corpus, tag=tag)
            for tag, rec in records.items()}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    held = [runs[t] for t in HELD_OUT if t in runs]
    ls = [l for r in held for l in r["listings"]]
    pl: Counter = Counter()
    for r in held:
        pl.update(r["summary"]["placements"])
    kw_all = sum(v for k, v in pl.items() if k.split(":")[0] == KEYWORD)
    kw_below = pl.get(f"{KEYWORD}:{CEDE}", 0)

    def count(rows, side, kind, value):
        """Of the listings of `side` whose round listed rules of `kind`, how many
        did `value` with every one."""
        with_ = [l for l in rows if l["side"] == side and l[f"{kind}_rules"]]
        return sum(1 for l in with_ if l[f"{kind}_toward"] == value), len(with_)

    c_k, c_k_of = count(ls, CLIMB, KEYWORD, ABOVE)
    d_k, d_k_of = count(ls, CEDE, KEYWORD, BELOW)
    c_s, c_s_of = count(ls, CLIMB, SECURITY, BELOW)
    n3 = (runs.get(CONTROL) or {}).get("listings") or []
    n_k, n_k_of = count(n3, CLIMB, KEYWORD, ABOVE)
    n_s, n_s_of = count(n3, CLIMB, SECURITY, BELOW)

    def clause(cid, what, part, whole, line, names):
        return {"clause": cid, "what": what,
                "reading": {names[0]: part, "of": whole, "share": frac(share(part, whole))},
                "holds": whole > 0 and F(part, whole) >= line}

    return [
        clause("F1", "over every round of the held-out runs, of the placements against keyword "
                     "rules of other queues, the gateways left out, at least three quarters put "
                     "the newborn below", kw_below, kw_all, F1_SHARE, ("below",)),
        clause("F2", "of the climbs whose round listed another keyword rule of a queue other "
                     "than SECURITY_INCIDENT, at least three quarters put the newborn above "
                     "every such rule", c_k, c_k_of, F2_SHARE, ("above_every",)),
        clause("F3", "of the cedes whose round listed another such rule, at least three "
                     "quarters put the newborn below every one", d_k, d_k_of, F3_SHARE,
               ("below_every",)),
        clause("F4", "of the climbs whose round listed a rule of SECURITY_INCIDENT that "
                     "contains the gateway, at least three quarters put the newborn below every "
                     "such rule", c_s, c_s_of, F4_SHARE, ("below_every",)),
        clause("F5", "in N r3, F2's statement", n_k, n_k_of, F5_SHARE, ("above_every",)),
        clause("F6", "in N r3, F4's statement", n_s, n_s_of, F6_SHARE, ("below_every",)),
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {plan.tag(a, k): json.loads(plan.run_path(a, k).read_text())
               for a in (plan.LABELLED, UNLABELLED) for k in range(1, plan.REPS + 1)}
    return records, json.loads(gw.record_path().read_text())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why the doors declared themselves above the "
                                             "gateway (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 5 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/doors.py writes {record_path()}")
    records, gateway_record = read_all()
    runs = read_all_runs(records, gateway_record, MI.space(), list(MI.corpus()))
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
        "source": {"gateway": str(gw.record_path()),
                   "gateway_from": gateway_record["_env"].get("git_commit")},
        "surface": "every round of each run that listed a gateway of gateway.json born before "
                   "it, once per gateway, by what its answer declared; every placement of every "
                   "round, by the kind of the rule placed",
        "constants": {"F1_SHARE": str(F1_SHARE), "F2_SHARE": str(F2_SHARE),
                      "F3_SHARE": str(F3_SHARE), "F4_SHARE": str(F4_SHARE),
                      "F5_SHARE": str(F5_SHARE), "F6_SHARE": str(F6_SHARE),
                      "DEVELOPMENT_RUN": DEVELOPMENT_RUN, "HELD_OUT": list(HELD_OUT),
                      "CONTROL": CONTROL, "DEVELOPMENT": DEVELOPMENT},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        s = r["summary"]
        print(f"  {t}: gateways {s['gateways']}; {s['listings']} listings, sides {s['sides']}; "
              f"keyword rules {s['keyword_toward']}; security rules {s['security_toward']}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
