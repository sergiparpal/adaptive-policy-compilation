"""
WHAT THE AT-ONCE ASKS WROTE FOR `ONCALL_ESCALATION` AND THE LAYER BELOW IT.
`corrections/oncall.py` found that L's loop writes the rarest queue whole at the
layer below it, which is the catalogue's reading of severity 1. It then loses
the queue to corrections of that layer: slices of severity 1 by product that
keep the queue's tiers. Two accounts fit:
- **information.** Level 1's catalogue names no tier for the queue, so no call
  can keep tiers it is never told;
- **shape.** The loop sees one ticket at a time, and loses what the labels carry
  together. The same labels compiled at once decide far more of the space
  (`CR-d` holds).
`FINDINGS_CORRECTIONS.md`, *Why L loses `ONCALL_ESCALATION`*, *What it does not
settle*, and `IDEAS.md` carry the question. Proposed by the agent and asked for
by Sergi on 2026-11-15, after `corrections/oncall.py`. Free on the records: the
asks were paid for in Stage B. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
**Every at-once answer Stage C read, and the loop's base beside it:**
- **the L runs' at-once sessions**: three asks at each checkpoint, at 10, 20,
  40, 80 and 160 labels and at all of them. Each ask's answer is its first
  valid one in re-ask order, as `corrections/score.py`'s `at_once` chooses it,
  installed as `CR-d` reads it;
- **the prior session**: five asks with no label, the catalogue alone;
- **the loop's base at each checkpoint**, right after the same label, as
  `corrections/score.py`'s `base_after` rebuilds it.

**Each base is read over the space:**
- **the queue's points** by `channel/lost.py`'s ways: right, an impasse, a
  conflict, contested or not, unwritten, or outranked by an edge or by
  containment. Also the queue's points right in `H04`'s part and in `H05`'s;
- **the layer**: the points of severity 1, outside the keyword, whose true
  queue is not the queue's. They are `H06`'s, `H07`'s and `H08`'s, of
  `T3_ENGINEERING` and `T2_TECHNICAL`. Each is read as decided right, decided as
  the queue, decided as another queue, or left in a conflict or an impasse;
- **the recall of `T3_ENGINEERING` and of `T2_TECHNICAL`** over the space;
- **the rules of the queue**: how many, how many name `customer_tier`, and which
  hold `H04`'s part whole and `H05`'s.

**Each checkpoint also gives what its labels hold**: how many name the queue,
and how many are tickets of the layer, by queue. A median is over a
checkpoint's asks, quantity by quantity.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The labels are the record's.** Each L session's labels are its run's
     reported errors in arrival order, each with the queue its report named.
     Each ask's labels are the first ones, as many as its checkpoint. The prior's
     asks carry none.
  2. **The answers are Stage C's.** Each checkpoint's chosen answers, installed,
     give the share of the space and the installation summary `score.json`
     keeps for each ask, in order. So do the prior's.
  3. **The loop's bases are Stage C's**: at each checkpoint, the share of the
     space `score.json` keeps.
  4. **The readings partition.** In every base the ways partition the queue's
     points, and the layer's readings partition the layer. The layer is the
     first match of `H06`, `H07` and `H08` over the space.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates, prints pass or fail,
and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
A1 to A4 read L's three runs, each apart, and A5 and A6 the prior's five asks.

  A1. **At least the loop.** At every checkpoint of each L run, the median
      at-once answer recalls at least as much of the queue as the loop's base
      after the same label.
  A2. **The queue whole, at once.** At all of each L run's labels, the median
      at-once answer recalls at least 9/10 of the queue.
  A3. **The layer learned, at once.** At all of each L run's labels, the median
      at-once answer decides right at least half of the layer's points.
  A4. **By the tier.** At all of each L run's labels, at least two of the run's
      three at-once answers write a rule of the queue that names
      `customer_tier`.
  A5. **The catalogue reads severity 1 as on-call.** Without a label, the
      median prior answer decides as the queue at least half of the layer's
      points.
  A6. **And keeps the queue.** Without a label, the median prior answer recalls
      at least 9/10 of the queue.

A median of nothing has no value, and a clause that reads one fails.

**The drafter's account.**
- **Without a label the catalogue is all there is.** Every loop's first rule of
  the queue read severity 1 as on-call (`corrections/oncall.py`), and the prior
  answers do the same: A5 and A6.
- **The labels show the layer, not the queue.** At all of its labels L r1's
  hold one ticket of the queue, and L r2's and L r3's none. They hold 17, 15
  and 12 tickets of the layer, mostly `H08`'s, labelled `T2_TECHNICAL`.
- **Seen together, those tickets bound the queue.** By the policy's first match
  none of them is enterprise, nor business off hours. An answer that writes the
  whole base at once can keep the queue where none of them falls, and give the
  layer its queues: A1 to A3.
- **The loop sees them one at a time, blind.** It writes each as its product's
  slice of severity 1 across the tiers. That is its shape, not the information.

**The bet is A2.** **A5 is trusted most**: every loop's first rule of the queue
did it. **A4 is trusted least**: an answer can keep the queue by listing the
layer's rules first, or nesting them, and write the queue's rule as severity 1
alone.

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole. That includes its Stage C table of the
  at-once asks' median share of the space by checkpoint, with the prior's median
  and range, and its section on why L loses the queue, with `oncall.json`
  whole;
- each L session's checkpoints and validity, and the labels' make-up above,
  counted for this reading;
- `manual/compile.py`'s `install`, `corrections/score.py`'s `at_once` and
  `base_after`, and `corrections/ask.py`'s `labelled`;
- the catalogue's text, the prose's paragraph on the critical tickets and the
  rules' text.

**What the drafter had not seen**: any at-once answer's rules, any base's
reading of any queue at a checkpoint, the prior answers' rules, and any
answer's reasoning.

--------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN: THE QUEUE'S LABELS, AND WHAT THE REASONING NAMES
--------------------------------------------------------------------------
The first run found the at-once answers writing no rule of the queue at all at
all of L r2's and L r3's labels, which name the queue nowhere. At L r1's, which
name it once, they wrote it off hours. So this part reads:
- **the queue's labelled tickets**: at each checkpoint, each label that names
  the queue, with its ticket's governing rule, severity, tier, hours and
  product, from the corpus;
- **what the reasoning names**: for each answer, how many times its reasoning
  writes the queue's identifier, `ONCALL_ESCALATION`.
It was tried on the records in a scratch script before it was written here,
after the six clauses above had been read: A3, A5 and A6 hold, and A1, A2 and
A4 fail. It carries no expectation and moves no clause.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Proposed by the agent and asked for by Sergi on 2026-11-15, after
`corrections/oncall.py`. The expectation above was written and committed before
the reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m corrections.layer --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.layer
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from typing import Any, Sequence

from harness.provenance import describe, environment

from channel import lost as L
from channel import oncall as O
from edges.rebuild import rebuild
from manual import compile as MC
from manual import instrument as MI
from reasoned_loop import references as rl_refs
from reasoned_loop import score as rl_score
from reuse import structure as st
from rung2.engine2 import PriorityEngine, Space

from . import ask
from . import forgotten as fg
from . import plan

F = Fraction
QUEUE = O.QUEUE                    # ONCALL_ESCALATION
T3, T2 = "T3_ENGINEERING", "T2_TECHNICAL"
H04, H05 = O.REACHED, O.UNREACHED  # the listed rules whose regions hold the queue
LAYER = ("H06", "H07", "H08")      # the policy's layer right below the queue's
ABOVE = ("H01", "H02", "H03", "H04", "H05")
TIER = "customer_tier"
L_RUNS = tuple(plan.tag(plan.LABELLED, k) for k in range(1, plan.REPS + 1))
PRIOR = "prior"

# How a point of the layer is read.
RIGHT, AS_QUEUE, OTHER, CONFLICT, IMPASSE = ("right", "as_the_queue", "as_another_queue",
                                              "conflict", "impasse")
LAYER_READINGS = (RIGHT, AS_QUEUE, OTHER, CONFLICT, IMPASSE)
WAYS = ("right", "lost") + L.WAYS + ("contested", "by_edge", "by_containment")

# The expectation's lines.
WHOLE = F(9, 10)
HALF = F(1, 2)
A4_ASKS = 2

PROVENANCE = (
    "POST-RUN: proposed by the agent and asked for by Sergi on 2026-11-15, after "
    "corrections/oncall.py. The expectation in the module's docstring was written and "
    "committed before the reading ran. Not a signed row; no verdict moves.")
ADDED = (
    "Added after the first run, after its six clauses were read: at each checkpoint, each "
    "label that names the queue with its ticket's governing rule, severity, tier, hours and "
    "product; and for each answer, how many times its reasoning writes ONCALL_ESCALATION. "
    "Tried in a scratch script first. No expectation; no clause moves.")
TICKET = ("severity", "customer_tier", "off_hours", "product", "has_security_keyword")

median = rl_score.median
share, frac = fg.share, fg.frac


def record_path():
    return plan.OUT / "layer.json"


def plain(x: Any) -> Any:
    """`forgotten.py`'s `plain`, and a string for anything else."""
    y = fg.plain(x)
    return str(y) if y is x else y


# ---------------------------------------------------------------------------
# The layer
# ---------------------------------------------------------------------------

def layer_of(space: Space, truth: dict[str, int]) -> int:
    """The points of severity 1, outside the keyword, whose true queue is not the
    queue's."""
    m = space.mask
    return m["severity"][1] & m["has_security_keyword"][False] & ~truth[QUEUE]


def first_match_of_the_layer(regions: dict[str, int]) -> int:
    """Gate 4's: where `H06`, `H07` or `H08` is the policy's first match."""
    mine = above = 0
    for h in LAYER:
        mine |= regions[h]
    for h in ABOVE:
        above |= regions[h]
    return mine & ~above


# ---------------------------------------------------------------------------
# A base, read
# ---------------------------------------------------------------------------

def read_base(engine: PriorityEngine, truth: dict[str, int], parts: dict[str, int],
              layer: int) -> tuple[dict[str, Any], bool]:
    """One base over the space: the queue's ways and parts, the layer, the
    recall of `T3_ENGINEERING` and `T2_TECHNICAL`, and the queue's rules. Also
    whether its readings partition, for gate 4."""
    w = L.ways(engine, truth[QUEUE], QUEUE)
    _, und, covered = L.by_action(engine)
    alone = L.decided_alone(und)
    decided = right = 0
    for q, m in alone.items():
        decided |= m
        right |= m & truth.get(q, 0)
    lay = {RIGHT: layer & right,
           AS_QUEUE: layer & alone.get(QUEUE, 0),
           CONFLICT: layer & covered & ~decided,
           IMPASSE: layer & ~covered}
    lay[OTHER] = layer & decided & ~lay[RIGHT] & ~lay[AS_QUEUE]
    union, total = 0, 0
    for m in lay.values():
        union |= m
        total += m.bit_count()
    ok = L.partitions(w, truth[QUEUE]) and union == layer and total == layer.bit_count()
    rules = [r for r in engine.rules if r.action == QUEUE]
    sp = MI.over_space(engine)
    out = {
        "space": F(sp["correct"], sp["n"]),
        "queue": {k: w[k].bit_count() for k in WAYS},
        "queue_right_by_part": {k: (w["right"] & m).bit_count() for k, m in parts.items()},
        "layer": {k: lay[k].bit_count() for k in LAYER_READINGS},
        "recall": {q: share((alone.get(q, 0) & truth[q]).bit_count(), truth[q].bit_count())
                   for q in (QUEUE, T3, T2)},
        "queue_rules": {
            "rules": len(rules),
            "naming_the_tier": sum(1 for r in rules if any(c.attr == TIER for c in r.conditions)),
            "holding_h04_whole": O.holds_whole(engine, QUEUE, parts[H04]),
            "holding_h05_whole": O.holds_whole(engine, QUEUE, parts[H05]),
            "conditions": [[[c.attr, c.op, c.value] for c in r.conditions] for r in rules]},
    }
    return out, ok


def medians(reads: Sequence[dict[str, Any]], layer_points: int) -> dict[str, Any]:
    """A checkpoint's medians over its asks, quantity by quantity."""
    if not reads:
        return {"asks": 0}

    def med(xs):
        return median(list(xs))

    return {"asks": len(reads),
            "space": frac(med(r["space"] for r in reads)),
            "queue_recall": frac(med(r["recall"][QUEUE] for r in reads)),
            "t3_recall": frac(med(r["recall"][T3] for r in reads)),
            "t2_recall": frac(med(r["recall"][T2] for r in reads)),
            "layer_right": frac(med(F(r["layer"][RIGHT], layer_points) for r in reads)),
            "layer_as_the_queue": frac(med(F(r["layer"][AS_QUEUE], layer_points)
                                           for r in reads)),
            "asks_naming_the_tier": sum(1 for r in reads if r["queue_rules"]["naming_the_tier"])}


def stored_base(r: dict[str, Any]) -> dict[str, Any]:
    """A base's reading as the record keeps it: its fractions as fractions."""
    return {**r, "space": frac(r["space"]),
            "recall": {q: frac(v) for q, v in r["recall"].items()}}


# ---------------------------------------------------------------------------
# The asks
# ---------------------------------------------------------------------------

def chosen(session: dict[str, Any]) -> list[tuple[int, int, dict[str, Any]]]:
    """Each checkpoint's asks, each its first valid answer in re-ask order, as
    `corrections/score.py`'s `at_once` chooses them, by checkpoint and ask."""
    rows = sorted(session["rows"], key=lambda r: (r["reask"], r["position"]))
    got: dict[tuple[int, int], dict] = {}
    for r in rows:
        if r["valid"] and (r["checkpoint"], r["k"]) not in got:
            got[(r["checkpoint"], r["k"])] = r
    return [(j, k, got[(j, k)]) for (j, k) in sorted(got)]


def installed(payload: Any) -> MC.Installed:
    raw, _ = MC.rules_of(payload)
    return MC.install(raw, MI.space())


def labels_are_the_records(session: dict[str, Any], record: dict[str, Any] | None) -> bool:
    """Gate 1."""
    lab = [list(p) for p in ask.labelled(record)] if record is not None else []
    if [list(p) for p in session.get("labelled") or []] != lab:
        return False
    return all([list(p) for p in r["labelled"]] == lab[:r["checkpoint"]] for r in session["rows"])


def make_up(pairs: Sequence[tuple[int, str]], rows: dict[int, dict],
            corpus: Sequence | None = None) -> dict[str, Any]:
    """What a checkpoint's labels hold: those that name the queue, and the
    tickets of the layer by the queue named. Given the corpus, each label that
    names the queue with its ticket: added after the first run."""
    lay = Counter(q for i, q in pairs if rows[i].get("truth_rule") in LAYER)
    out = {"labels": len(pairs), "naming_the_queue": sum(1 for _, q in pairs if q == QUEUE),
           "tickets_of_the_layer": sum(lay.values()),
           "of_the_layer_by_queue": dict(sorted(lay.items()))}
    if corpus is not None:
        out["queue_tickets"] = [{"case": i, "governing": rows[i].get("truth_rule"),
                                 **{a: getattr(corpus[i], a) for a in TICKET}}
                                for i, q in pairs if q == QUEUE]
    return out


def names_the_queue(row: dict[str, Any]) -> int:
    """Added after the first run: how many times an answer's reasoning writes
    the queue's identifier."""
    return (row.get("reasoning") or "").count(QUEUE)


def read_session(session: dict[str, Any], stored: dict[str, Any], truth: dict[str, int],
                 parts: dict[str, int], layer: int) -> tuple[dict[int, dict[str, Any]], bool, bool]:
    """Every chosen answer of a session, read, with its checkpoint's medians.
    `stored` is Stage C's reading of the session, by checkpoint. Also gate 2 and
    gate 4 for the session."""
    by_j: dict[int, list[tuple[int, dict[str, Any], dict[str, Any]]]] = {}
    ok4 = True
    for j, k, row in chosen(session):
        inst = installed(row["payload"])
        rd, ok = read_base(inst.engine, truth, parts, layer)
        ok4 &= ok
        rd["reasoning_names_the_queue"] = names_the_queue(row)
        by_j.setdefault(j, []).append((k, rd, inst.summary()))
    ok2 = sorted(int(j) for j in stored) == sorted(by_j)
    out = {}
    for j, asks in sorted(by_j.items()):
        keep = stored.get(str(j)) or stored.get(j) or {}
        kept = keep.get("asks") or []
        ok2 &= (len(kept) == len(asks)
                and all(F(s["space"]["fraction"]) == rd["space"] and s["installed"] == summ
                        for s, (_, rd, summ) in zip(kept, asks)))
        out[j] = {"asks": [{"k": k, **stored_base(rd)} for k, rd, _ in asks],
                  "median": medians([rd for _, rd, _ in asks], layer.bit_count())}
    return out, ok2, ok4


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def loop_base(record: dict[str, Any], idx: int) -> PriorityEngine:
    """`corrections/score.py`'s `base_after`, keeping the engine."""
    return rebuild(record, list(MI.corpus())[:idx + 1], MI.space(), only=set()).engine


def read_run(record: dict[str, Any], session: dict[str, Any], curve: Sequence[dict[str, Any]],
             truth: dict[str, int], parts: dict[str, int], layer: int) -> dict[str, Any]:
    """One L run: each checkpoint's labels, the loop's base after them and the
    at-once answers, and the gates. `curve` is Stage C's `CR-g` curve of the
    run."""
    pairs = ask.labelled(record)
    rows = {r["idx"]: r for r in record["records"]}
    corpus = list(MI.corpus())
    stored = {str(c["labels"]): c["at_once"] for c in curve if c.get("at_once")}
    asked, ok2, ok4 = read_session(session, stored, truth, parts, layer)
    ok3 = True
    checkpoints = []
    for c in curve:
        j, idx = c["labels"], c["case"]
        eng = loop_base(record, idx)
        rd, ok = read_base(eng, truth, parts, layer)
        ok4 &= ok
        ok3 &= rd["space"] == F(c["loop"]["fraction"])
        checkpoints.append({"labels": j, "case": idx, "make_up": make_up(pairs[:j], rows, corpus),
                            "loop": stored_base(rd), "at_once": asked.get(j)})
    gates = [
        {"gate": 1, "what": "the labels are the record's",
         "passes": labels_are_the_records(session, record)},
        {"gate": 2, "what": "the answers are Stage C's", "passes": ok2 and bool(asked)},
        {"gate": 3, "what": "the loop's bases are Stage C's", "passes": ok3 and bool(curve)},
        {"gate": 4, "what": "the readings partition", "passes": ok4},
    ]
    return {"checkpoints": checkpoints, "gates": gates}


def read_prior(session: dict[str, Any], stored: dict[str, Any], truth: dict[str, int],
               parts: dict[str, int], layer: int) -> dict[str, Any]:
    """The prior: five asks with no label."""
    asked, ok2, ok4 = read_session(session, stored, truth, parts, layer)
    gates = [
        {"gate": 1, "what": "the labels are the record's",
         "passes": labels_are_the_records(session, None)},
        {"gate": 2, "what": "the answers are Stage C's", "passes": ok2 and bool(asked)},
        {"gate": 4, "what": "the readings partition", "passes": ok4},
    ]
    return {"asked": asked.get(0), "gates": gates}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(runs: dict[str, dict[str, Any]], prior: dict[str, Any]) -> list[dict[str, Any]]:
    got = {t: runs[t] for t in L_RUNS if t in runs}

    def value(m: dict[str, Any] | None, key: str) -> Fraction | None:
        x = (m or {}).get(key)
        return None if x is None else F(x["fraction"])

    def last(r: dict[str, Any]) -> dict[str, Any]:
        return ((r["checkpoints"][-1] if r["checkpoints"] else {}).get("at_once") or {}).get(
            "median") or {}

    a1 = {}
    for t, r in got.items():
        a1[t] = [{"labels": c["labels"],
                  "at_once": value((c.get("at_once") or {}).get("median"), "queue_recall"),
                  "loop": F(c["loop"]["recall"][QUEUE]["fraction"])
                  if c["loop"]["recall"][QUEUE] else None} for c in r["checkpoints"]]
    a1_holds = bool(got) and all(
        rows and all(x["at_once"] is not None and x["loop"] is not None
                     and x["at_once"] >= x["loop"] for x in rows) for rows in a1.values())
    a2 = {t: value(last(r), "queue_recall") for t, r in got.items()}
    a3 = {t: value(last(r), "layer_right") for t, r in got.items()}
    a4 = {t: last(r).get("asks_naming_the_tier") for t, r in got.items()}
    pm = (prior.get("asked") or {}).get("median") or {}
    a5, a6 = value(pm, "layer_as_the_queue"), value(pm, "queue_recall")

    def each(vals: dict[str, Any], line) -> bool:
        return bool(vals) and all(v is not None and v >= line for v in vals.values())

    return [
        {"clause": "A1", "what": "at every checkpoint of each L run, the median at-once answer "
                                 "recalls at least as much of the queue as the loop's base",
         "reading": {t: [{**x, "at_once": frac(x["at_once"]), "loop": frac(x["loop"])}
                         for x in rows] for t, rows in a1.items()},
         "holds": a1_holds},
        {"clause": "A2", "what": "at all of each L run's labels, the median at-once answer "
                                 "recalls at least 9/10 of the queue",
         "reading": {t: frac(v) for t, v in a2.items()}, "holds": each(a2, WHOLE)},
        {"clause": "A3", "what": "at all of each L run's labels, the median at-once answer "
                                 "decides right at least half of the layer's points",
         "reading": {t: frac(v) for t, v in a3.items()}, "holds": each(a3, HALF)},
        {"clause": "A4", "what": "at all of each L run's labels, at least two of its three "
                                 "at-once answers write a rule of the queue naming customer_tier",
         "reading": a4, "holds": each(a4, A4_ASKS)},
        {"clause": "A5", "what": "without a label, the median prior answer decides as the queue "
                                 "at least half of the layer's points",
         "reading": frac(a5), "holds": a5 is not None and a5 >= HALF},
        {"clause": "A6", "what": "without a label, the median prior answer recalls at least 9/10 "
                                 "of the queue",
         "reading": frac(a6), "holds": a6 is not None and a6 >= WHOLE},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def session_path(name: str):
    return plan.OUT / f"atonce_{name}.json"


def read_all() -> tuple[dict[str, dict], dict[str, dict], dict[str, Any]]:
    records = {t: json.loads(plan.run_path(plan.LABELLED, k).read_text())
               for k, t in enumerate(L_RUNS, start=1)}
    sessions = {name: json.loads(session_path(name).read_text()) for name in L_RUNS + (PRIOR,)}
    return records, sessions, json.loads(plan.score_path().read_text())


def read_everything(records: dict[str, dict], sessions: dict[str, dict], score: dict[str, Any],
                    space: Space, truth: dict[str, int],
                    regions: dict[str, int]) -> tuple[dict[str, Any], dict[str, Any], list]:
    parts = O.parts(truth[QUEUE], regions)
    layer = layer_of(space, truth)
    runs = {t: read_run(records[t], sessions[t], score["CR-g"]["curves"][t], truth, parts,
                        layer) for t in L_RUNS if t in records}
    prior = read_prior(sessions[PRIOR], score["CR-g"]["prior"], truth, parts, layer)
    layer_gate = {"gate": 4, "run": None,
                  "what": "the layer is the first match of H06, H07 and H08",
                  "passes": layer == first_match_of_the_layer(regions)}
    checked = ([{"run": t, **g} for t, r in runs.items() for g in r["gates"]]
               + [{"run": PRIOR, **g} for g in prior["gates"]] + [layer_gate])
    return runs, prior, checked


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="What the at-once asks wrote for "
                                             "ONCALL_ESCALATION and the layer below it "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 4 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/layer.py writes {record_path()}")
    records, sessions, score = read_all()
    space, truth = MI.space(), MI.space_truth()
    runs, prior, checked = read_everything(records, sessions, score, space, truth,
                                           rl_refs.regions())
    for g in checked:
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    expectation = read_expectation(runs, prior)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "added_after_the_first_run": ADDED,
        "source": {"score": str(plan.score_path()),
                   "score_from": score["_env"].get("git_commit"),
                   "sessions": {n: str(session_path(n)) for n in sessions},
                   "sessions_from": {n: s["_env"].get("git_commit") for n, s in sessions.items()}},
        "surface": "the whole space, 134,400 points: every at-once answer Stage C read, "
                   "installed as CR-d reads it, and the loop's base after each checkpoint's "
                   "label",
        "layer": {"rules": list(LAYER), "points": layer_of(space, truth).bit_count(),
                  "what": "the points of severity 1, outside the keyword, whose true queue is "
                          "not ONCALL_ESCALATION's"},
        "constants": {"WHOLE": str(WHOLE), "HALF": str(HALF), "A4_ASKS": A4_ASKS},
        "gates": checked,
        "runs": runs,
        "prior": prior,
        "expectation": expectation,
    }), indent=2, default=plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        last = r["checkpoints"][-1]
        m = (last.get("at_once") or {}).get("median") or {}
        print(f"  {t} at {last['labels']} labels: at once, the queue "
              f"{(m.get('queue_recall') or {}).get('value')}, the layer right "
              f"{(m.get('layer_right') or {}).get('value')}; the loop, the queue "
              f"{(last['loop']['recall'][QUEUE] or {}).get('value')}")
    pm = (prior.get("asked") or {}).get("median") or {}
    print(f"  prior: the queue {(pm.get('queue_recall') or {}).get('value')}, the layer as the "
          f"queue {(pm.get('layer_as_the_queue') or {}).get('value')}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
