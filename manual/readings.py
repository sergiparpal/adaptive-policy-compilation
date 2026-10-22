"""
THREE THINGS STAGE C LEFT FREE ON THE RECORDS. `FINDINGS_MANUAL.md`, *What
Stage C does not settle*, names five things its runs do not settle, and says of
three that the records can answer them without a call: why the prose made the
loop cross more than the rules did (its item 1, the part a reading reaches),
what level 3's dropped declarations would have decided (item 3), and which rule
decided `SECURITY_INCIDENT` wrong under the prose, and when it was born (item
4). `IDEAS.md` carries the three under *What `PLAN_MANUAL.md` opens*. POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**The twelve loop runs**, `results_manual/loop_L{k}_r{r}.json`: `PLAN_REUSE.md`'s
loop under v1, with level k's manual in the prompt. Each record keeps every rule
with its birth case, the edges accepted at its birth and the declarations
dropped there. It keeps every arrival with its truth, the hidden rule that
governs it (`truth_rule`), how it was decided and by which rule, and the rules
shown to the proposer when it escalated.

**The ticket's rule.** Every arrival is governed by one rule of the hidden
policy: the first of `HIDDEN_DSL` its ticket matches. That rule has an
*extension*, the points of the space its conditions match, and a *region*, the
part of its extension no higher rule takes, where it decides under first match.
The regions partition the space.

**`K-a`**, `PLAN_BLIND.md`'s statistic as `manual/instrument.py` reads it. The
base is replayed in birth order. A rule that is not a keyword rule, one whose
extension lies inside the keyword's half, is *alone* when it meets no earlier
rule of another queue on the half without the keyword. `K-a` is the share
alone. A rule that meets one *crosses*.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  A. **Why the prose made the loop cross more than the rules did.** Every birth
     `K-a` reads, in all twelve runs, is set against its ticket's rule H by its
     extension E:
     - `region`: E inside H's region. A ticket written out whole is one point
       of it.
     - `rule`: E inside H's extension and not inside its region. This is H as
       written, or part of it, reaching the regions of rules above H.
     - `beyond`: E not inside H's extension.
     For each level and class it counts the births, how many cross, and how
     many name the ticket's queue. Beside them: the births' conditions and
     their extension off the keyword, and how many are H's region exactly or
     H as written. A crossing birth is *nested* when every rule of another
     queue it meets contains it or lies inside it, over the space, and
     *partial* otherwise. **The gap** is between L₂'s and L₃'s pooled `K-a`:
     the alone births over the births read, summed over a level's three
     runs. It is split by the classes' mix, reading each level's rates on the
     other level's mix.
  B. **What level 3's dropped declarations would have decided.** These are
     the declarations L₃'s runs cited against the manual's own identifiers,
     `H01` to `H29`, which no base holds. Each names a rule R, born at a
     ticket, a direction, and a hidden rule H.
     1. **The claim, against the policy.** Over the points E(R) and E(H)
        share, a declaration is:
        - `inert` if they share none;
        - `idle` if R names H's queue;
        - *at stake* otherwise. Its direction is read as
          `rung3/edge_direction.py` reads an edge: for the side whose queue is
          the truth on more of the shared points.
        Whether one extension contains the other, and whether the
        declaration agrees with that containment, is counted beside.
     2. **The claim, translated.** Two translations, fixed here before any is
        counted:
        - `T1`, H as written: the rules shown at R's birth with H's extension
          and H's queue;
        - `T2`, H's parts: the rules shown at R's birth with H's queue and an
          extension inside H's.
        Each declaration becomes one edge per rule its translation names,
        pointed as declared. The engine tries each at R's birth, in the place
        the declaration held in the answer. The base is rebuilt as
        `edges/rebuild.py` rebuilds it, births held where the record has them,
        and read beside the record's: the final base over the space and the
        corpus, and the arrivals as the rules decided them. The rules that
        would have qualified in the base but were not shown are counted
        beside.
  C. **`SECURITY_INCIDENT` under the prose.** It reads every arrival whose
     truth is the class, twenty a run, in all twelve runs, L₂'s first:
     - how it was decided as it arrived, and by which rule;
     - for every rule that decided one: its conditions and queue, its birth
       and the ticket it was born on, whether it is a keyword rule, and how
       many it decided right;
     - for every ticket a rule decided wrong: the rules of the class that
       matched it then, and what defeated them.
     Over the space, it reads which rules decide the class's 50,400 points in
     each of L₂'s final bases.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
- The twelve loop records, read-only.
- `results_manual/score.json`, for gates 1 and 4: each run's `K-a`, its cells
  and its rare queues.
- `HIDDEN_DSL`, through `manual/instrument.py`'s regions and its rules'
  extensions. The truth over the space is `manual/instrument.py`'s.

Every function that exists is called, not copied:
- the rebuild is `edges.rebuild.rebuild`;
- the logged edges by birth are `edges.rebuild.edges_by_birth`;
- `K-a`'s walk is `blind.rows.births_outside`;
- the direction is `rung3.edge_direction`'s.
A translation enters the rebuild as an edge written into a copy of the record,
where the dropped declaration stood.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The runs are the records'.** Rebuilt, every run decides every arrival
     as its record did, by the same rule. Its final base scores what
     `score.json` says on both surfaces.
  2. **The policy is one convention.**
     - The hidden rules' regions partition the space.
     - Each region lies inside its rule's extension and inside its queue's
       truth.
     - In every record, each arrival's `truth_rule` is the first hidden rule
       its ticket matches, and its truth is that rule's queue.
  3. **The answers are the records'.**
     - At every birth, the answer's declarations come back in order from the
       row's reasons, the rule's dropped edges and the edge log.
     - Every birth row is an escalation that bore its rule, and every rule
       shown was born before it.
     - The declarations dropped outside the neighbourhood all cite a hidden
       rule. They number 29, 26 and 6 in L₃'s runs and none elsewhere.
  4. **Two routes agree.**
     - Every run's own walk gives `births_outside`'s counts and
       `score.json`'s `K-a`.
     - The class's tickets decided, and decided right, are `score.json`'s.
     - A copy of a record with no translation written in rebuilds to the
       record's decisions and base.

It refuses to write if any gate fails, and while `PLAN_MANUAL.md` is unsigned,
like every writer of the package. `--dry-run` runs the four gates, prints pass
or fail, and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  A1. **Births in `region` cross less often than births in `rule` and `beyond`
      together**, pooled over a level's runs, at L₁, L₂ and L₃. A rule inside
      one region meets only the rules that reach into it. L₀'s births never
      cross (`K-a` 1 in all three runs), so A1 does not read L₀.
  A2. **L₃'s births fall in `region` more often than L₂'s**, pooled. The list
      hands the proposer its ticket's rule and every rule above it.
      `FINDINGS_MANUAL.md` names *a proposer writing each rule's effective
      region* among the candidates.
  A3. **The mix carries more than half of the gap between L₂'s and L₃'s
      pooled `K-a`**, under both readings: L₂'s rates on L₃'s mix, and L₃'s
      on L₂'s. The gap is read as L₃'s less L₂'s, and must be positive, as
      the two levels' medians are.
  A4. **L₂'s births reach `beyond` their ticket's rule more often than
      L₃'s.** The prose states its sections by queue and by product, and a
      rule that generalises one of its sentences crosses the rules' borders.
  B1. **At least a quarter of the 61 are idle or inert.** Under v1 the
      proposer declares against rules of its own queue: seven of the eight
      declarations `PLAN_AUTHORSHIP.md`'s level 1 refused were.
  B2. **Of the declarations at stake with a strict better side over the
      space, at least three quarters point at it.** The list is the policy's
      order, and compiled once the proposer transcribes it without error.
  B3. **Under `T1`, fewer than a quarter of the 61 have a rule to name among
      the rules shown.** The loop's bases partition, so they seldom hold a
      hidden rule as written.
  B4. **Under either translation, in every run, the edges installed change the
      decision on fewer than 1,344 points of the space, a hundredth, and on
      fewer than 20 arrivals.** The rules shown at an impasse seldom meet the
      new rule. Of the declarations L₃'s runs made against rules of the base,
      the engine refused about half as disjoint.
  C1. **In each of L₂'s runs, one rule decides more than half of the class's
      tickets the rules decide.**
  C2. **In each, that rule routes to `T2_TECHNICAL`**: §1's remainder, *las
      revisa soporte tecnico*.
  C3. **And it is a keyword rule**: its extension lies inside the keyword's
      half.
  C4. **No rule of the class matched any of the class's tickets that a rule
      decided wrong, in any of L₂'s runs.** What decided them faced no rule of
      the class.

The drafter trusts C4 least, then A3 and B1. **Read beside them, and not
clauses**:
- the nested and partial crossings at each level;
- the deciding rules of the class at L₀, L₁ and L₃;
- the containment the 61 declarations agree or disagree with;
- the arrivals each translation changes, right and wrong.

**What the drafter had seen**:
- `FINDINGS_MANUAL.md` whole, every figure in it;
- `STATUS.md`'s and `IDEAS.md`'s entries on `PLAN_MANUAL.md`;
- `PLAN_MANUAL.md`'s texts, §5.3's table, §6 and §13;
- L₃ r1's level-3 system prompt, its first three rules with their notes, one
  rule's dropped edges, and two escalated rows;
- for every run, its number of rules, the count of declarations dropped at its
  births, by direction and by whether each cites a hidden rule or a rule of
  the base, and its `edges_proposed`, `edges_accepted` and `edge_reasons`;
- `score.json`'s cell of L₂ r1, read to learn the record's layout: its `K-a`
  as a reduced fraction, its two surfaces, and its rare queues, which
  `FINDINGS_MANUAL.md` publishes.

**Not seen**:
- any rule of L₀'s, L₁'s or L₂'s runs, or of L₃'s beyond r1's first three;
- any birth's class, and the conditions or extension of any birth but those
  three;
- which rule decided any arrival of `SECURITY_INCIDENT`, at any level;
- what any of the 61 declarations cites against what it declares, any
  translation, and any count of one.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: asked for on 2026-10-22, after `PLAN_MANUAL.md`'s Stage C, with the
expectation above written and committed before the first run. Not a signed row,
not on `STATUS.md`'s scoreboard, not a calibration event. Zero API calls.

Usage:  python3 -m manual.readings --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m manual.readings
"""

from __future__ import annotations

import copy
import json
import statistics
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable, Sequence

from harness.ceiling_check import HIDDEN_DSL
from harness.dsl import Condition
from harness.provenance import describe, environment

from blind import rows as brows
from edges.rebuild import edges_by_birth, rebuild
from fidelity.replay import OUTSIDE
from rung2.engine2 import EDGE_OK, strictly_below
from rung3.edge_direction import better_over_space, verdict

from . import instrument as I
from . import plan
from .score import plain

SI, T2 = "SECURITY_INCIDENT", "T2_TECHNICAL"
CLASSES = ("region", "rule", "beyond")
TRANSLATIONS = ("T1", "T2")
TRANSLATED = "traducida"          # the reason a translated edge carries in a record's copy
BEATS, LOSES = "beats", "loses_to"
DROPPED = {(3, 1): 29, (3, 2): 26, (3, 3): 6}    # FINDINGS_MANUAL.md, Stage B2
A1_LEVELS = (1, 2, 3)

# The expectation's lines.
A3_SHARE = Fraction(1, 2)
B1_IDLE = Fraction(1, 4)
B2_HIT = Fraction(3, 4)
B3_T1 = Fraction(1, 4)
B4_POINTS = 1344
B4_ARRIVALS = 20
C1_SHARE = Fraction(1, 2)

PROVENANCE = (
    "POST-RUN: asked for on 2026-10-22, after PLAN_MANUAL.md's Stage C. The "
    "expectation in the module's docstring was written and committed before the "
    "first run. Not a signed row; no verdict moves.")


class AnswerError(Exception):
    """A birth's declarations do not come back from its record."""


def record_path() -> Path:
    return plan.OUT / "readings.json"


def name(run: tuple[int, int]) -> str:
    return f"L{run[0]} r{run[1]}"


def contains(big: int, small: int) -> bool:
    return small & ~big == 0


def frac(cell: dict) -> Fraction:
    """A fraction as `manual/score.py`'s record writes it."""
    return Fraction(cell["fraction"])


def share(part: int, whole: int) -> Fraction | None:
    return Fraction(part, whole) if whole else None


# ---------------------------------------------------------------------------
# The policy and the records
# ---------------------------------------------------------------------------

def hidden_rules() -> dict[str, dict[str, Any]]:
    """Each hidden rule's queue, extension, region and corpus cases, by id."""
    sp = I.space()
    regions = I.hidden_regions()
    return {rid: {"queue": action,
                  "ext": sp.extension([Condition(a, o, v) for a, o, v in conds]),
                  "region": regions[rid]["mask"], "cases": regions[rid]["cases"]}
            for rid, conds, action in HIDDEN_DSL}


def load_runs() -> dict[tuple[int, int], dict]:
    """The twelve loop records by (level, rep), in §2.5's order."""
    return {(lv, rep): json.loads(plan.loop_path(lv, rep).read_text())
            for rep, lv in plan.loop_schedule()}


def load_scored() -> dict[tuple[int, int], dict]:
    s = json.loads(plan.score_path().read_text())
    return {(int(lv), r["rep"]): r for lv, rs in s["G-g"]["runs"].items() for r in rs}


# ---------------------------------------------------------------------------
# A: the births, against their tickets' rules
# ---------------------------------------------------------------------------

def classify(E: int, H: dict) -> str:
    if contains(H["region"], E):
        return "region"
    if contains(H["ext"], E):
        return "rule"
    return "beyond"


def births_read(rules: Sequence[dict], rows: dict[int, dict], hidden: dict,
                ext: dict[str, int], outside: int) -> list[dict]:
    """Every rule `K-a` reads, in birth order, set against its ticket's rule."""
    seen: list[tuple[str, int, str]] = []
    out = []
    for r in sorted(rules, key=lambda r: (r["born_at"], r["rule_id"])):
        E, q = ext[r["rule_id"]], r["action"]
        if not brows.is_keyword(E, outside):
            row = rows[r["born_at"]]
            H = hidden[row["truth_rule"]]
            met = [(rid, x) for rid, x, a in seen if a != q and E & x & outside]
            out.append({
                "rule_id": r["rule_id"], "born_at": r["born_at"], "queue": q,
                "ticket_rule": row["truth_rule"], "truth": row["truth"],
                "birth_outcome": row["outcome"], "right_queue": q == row["truth"],
                "class": classify(E, H),
                "region_exactly": E == H["region"], "as_written": E == H["ext"],
                "one_point": E.bit_count() == 1,
                "conditions": len(r["conditions"]),
                "points_outside": (E & outside).bit_count(),
                "crosses": bool(met), "met": [rid for rid, _ in met],
                "nested": bool(met) and all(contains(x, E) or contains(E, x)
                                            for _, x in met),
            })
        seen.append((r["rule_id"], E, q))
    return out


def summary(births: Sequence[dict]) -> dict[str, Any]:
    """A level's births, pooled over its runs, by class."""
    by = {c: {"births": 0, "cross": 0, "right_queue": 0, "nested": 0} for c in CLASSES}
    for b in births:
        d = by[b["class"]]
        d["births"] += 1
        d["cross"] += b["crosses"]
        d["right_queue"] += b["right_queue"]
        d["nested"] += b["nested"]
    n = len(births)
    alone = sum(not b["crosses"] for b in births)
    crossing = [b for b in births if b["crosses"]]
    med = (lambda k: statistics.median(b[k] for b in births) if births else None)
    return {"births": n, "alone": alone, "k_a": share(alone, n), "classes": by,
            "class_share": {c: share(by[c]["births"], n) for c in CLASSES},
            "cross_rate": {c: share(by[c]["cross"], by[c]["births"]) for c in CLASSES},
            "region_exactly": sum(b["region_exactly"] for b in births),
            "as_written": sum(b["as_written"] for b in births),
            "one_point": sum(b["one_point"] for b in births),
            "conditions_median": med("conditions"),
            "points_outside_median": med("points_outside"),
            "crossing": {"nested": sum(b["nested"] for b in crossing),
                         "partial": sum(not b["nested"] for b in crossing)}}


def alone_rate(d: dict) -> Fraction | None:
    return share(d["births"] - d["cross"], d["births"])


def on_mix(rates_of: dict, mix_of: dict) -> Fraction | None:
    """One level's alone rates by class, read on another level's mix. None when
    a class the mix holds has no birth to give it a rate."""
    n = sum(mix_of[c]["births"] for c in CLASSES)
    if not n:
        return None
    total = Fraction(0)
    for c in CLASSES:
        w = mix_of[c]["births"]
        if w:
            r = alone_rate(rates_of[c])
            if r is None:
                return None
            total += Fraction(w, n) * r
    return total


def mix_split(low: dict, high: dict) -> dict[str, Any]:
    """The gap between two levels' pooled `K-a`, high less low, and the share of
    it the classes' mix carries under each level's rates."""
    ka_l, ka_h = low["k_a"], high["k_a"]
    gap = ka_h - ka_l if ka_l is not None and ka_h is not None else None
    l_on_h = on_mix(low["classes"], high["classes"])
    h_on_l = on_mix(high["classes"], low["classes"])
    ok = bool(gap)
    return {"gap": gap, "low_rates_on_high_mix": l_on_h, "high_rates_on_low_mix": h_on_l,
            "mix_share_low_rates": (l_on_h - ka_l) / gap if ok and l_on_h is not None
            else None,
            "mix_share_high_rates": (ka_h - h_on_l) / gap if ok and h_on_l is not None
            else None}


# ---------------------------------------------------------------------------
# B: the declarations, in the order the answers gave them
# ---------------------------------------------------------------------------

def answers(record: dict) -> dict[int, list[tuple]]:
    """Every birth's declarations in the order its answer gave them:
    `("logged", edge)` for one the engine tried, `("outside", direction, ref)`
    for one dropped before it, because the rule it cites was not shown."""
    logged = edges_by_birth(record)
    born = {r["born_at"]: r for r in record["rules"]}
    out: dict[int, list[tuple]] = {}
    for row in record["records"]:
        reasons = row.get("edge_reasons") or []
        if not reasons:
            continue
        rule = born.get(row["idx"])
        if rule is None:
            raise AnswerError(f"case {row['idx']}: declarations and no birth")
        rid = rule["rule_id"]
        drops = list(rule.get("dropped_edges") or [])
        tried = list(logged.get(row["idx"], []))
        items: list[tuple] = []
        i = j = 0
        for why in reasons:
            if why == OUTSIDE:
                if i >= len(drops) or drops[i].count(":") != 1:
                    raise AnswerError(f"case {row['idx']}: a drop outside the "
                                      "neighbourhood the rule does not keep")
                direction, ref = drops[i].split(":")
                if direction not in (BEATS, LOSES):
                    raise AnswerError(f"case {row['idx']}: direction {direction!r}")
                items.append(("outside", direction, ref))
                i += 1
                continue
            if j >= len(tried):
                raise AnswerError(f"case {row['idx']}: the log ran out")
            e = tried[j]
            j += 1
            sides = ([(BEATS, e.loser)] if e.winner == rid else []) + \
                    ([(LOSES, e.winner)] if e.loser == rid else [])
            if not sides:
                raise AnswerError(f"case {row['idx']}: an edge without its rule")
            if why == EDGE_OK:
                if not any(ref in (rule.get(d) or []) for d, ref in sides):
                    raise AnswerError(f"case {row['idx']}: an accepted edge the "
                                      "rule does not keep")
            else:
                if i >= len(drops) or drops[i] not in {f"{d}:{ref}:{why}"
                                                       for d, ref in sides}:
                    raise AnswerError(f"case {row['idx']}: a refusal the rule "
                                      "does not keep")
                i += 1
            items.append(("logged", e))
        if i != len(drops) or j != len(tried):
            raise AnswerError(f"case {row['idx']}: drops or edges left over")
        out[row["idx"]] = items
    return out


def dropped(record: dict) -> list[dict]:
    """The declarations dropped outside the neighbourhood, in answer order, each
    with its place among its birth's drops."""
    rid = {r["born_at"]: r["rule_id"] for r in record["rules"]}
    out = []
    for idx, items in sorted(answers(record).items()):
        k = 0
        for it in items:
            if it[0] == "outside":
                out.append({"case": idx, "k": k, "rule": rid[idx],
                            "direction": it[1], "cites": it[2]})
                k += 1
    return out


def claim(d: dict, ext: dict[str, int], action: dict[str, str], hidden: dict,
          tmask: dict[str, int]) -> dict[str, Any]:
    """A dropped declaration read against the policy, over the points the rule
    and the hidden rule it cites share."""
    R, Hid = d["rule"], d["cites"]
    H = hidden[Hid]
    e_r, e_h = ext[R], H["ext"]
    shared = e_r & e_h
    if e_r == e_h:
        containment = "equal"
    elif strictly_below(e_r, e_h):
        containment = "rule_inside_cited"
    elif strictly_below(e_h, e_r):
        containment = "cited_inside_rule"
    else:
        containment = None
    narrower_wins = {"rule_inside_cited": BEATS, "cited_inside_rule": LOSES}
    out: dict[str, Any] = {
        "shared_points": shared.bit_count(), "containment": containment,
        "agrees_with_containment": (d["direction"] == narrower_wins[containment]
                                    if containment in narrower_wins else None)}
    if not shared:
        out["kind"] = "inert"
    elif action[R] == H["queue"]:
        out["kind"] = "idle"
    else:
        wins = better_over_space(R, Hid, {R: e_r, Hid: e_h},
                                 {R: action[R], Hid: H["queue"]}, tmask)
        v = verdict(*wins)
        declared = "a" if d["direction"] == BEATS else "b"
        out.update({"kind": "at_stake", "wins": list(wins),
                    "point": ("hit" if v == declared else "miss")
                    if v in ("a", "b") else v})
    return out


def counterparts(H: dict, ids: Iterable[str], ext: dict[str, int],
                 action: dict[str, str]) -> dict[str, list[str]]:
    """The rules among `ids` each translation names for hidden rule H."""
    ids = list(ids)
    return {"T1": [r for r in ids if action[r] == H["queue"] and ext[r] == H["ext"]],
            "T2": [r for r in ids if action[r] == H["queue"]
                   and contains(H["ext"], ext[r])]}


def pairs_of(d: dict, names: Sequence[str]) -> list[tuple[str, str]]:
    """The edges a declaration becomes, (winner, loser), pointed as declared."""
    return [(d["rule"], c) if d["direction"] == BEATS else (c, d["rule"]) for c in names]


def written_in(record: dict, edges: dict[tuple[int, int], list[tuple[str, str]]]
               ) -> tuple[dict, dict[tuple[int, int], list[int]]]:
    """A copy of the record with translated edges written in. `edges` maps
    `(case, k)`, the k-th declaration dropped outside the neighbourhood at that
    case's birth, to the edges it becomes. Each enters the row's reasons and the
    edge log where the declaration stood, with the reason `TRANSLATED`, so that
    `rebuild` tries it there. Returns the copy and each translated edge's key."""
    rec = copy.deepcopy(record)
    log = list(rec.get("edge_log") or [])
    new_log: list = []
    keys: dict[tuple[int, int], list[int]] = {}
    pos = 0
    for row in rec["records"]:
        reasons = row.get("edge_reasons") or []
        if not reasons:
            continue
        new: list[str] = []
        k = 0
        for why in reasons:
            if why != OUTSIDE:
                new.append(why)
                new_log.append(log[pos])
                pos += 1
                continue
            pairs = edges.get((row["idx"], k), [])
            if pairs:
                for w, l in pairs:
                    keys.setdefault((row["idx"], k), []).append(len(new_log))
                    new.append(TRANSLATED)
                    new_log.append([w, l, TRANSLATED])
            else:
                new.append(OUTSIDE)
            k += 1
        row["edge_reasons"] = new
    if pos != len(log):
        raise AnswerError(f"{len(log) - pos} edge_log entries belong to no row")
    rec["edge_log"] = new_log
    return rec, keys


def decided_by_queue(engine) -> dict[str, int]:
    """Where each queue's rules are undefeated, by masks."""
    action = {r.rule_id: r.action for r in engine.rules}
    out: dict[str, int] = {}
    for rid, m in brows.undefeated_masks(engine).items():
        out[action[rid]] = out.get(action[rid], 0) | m
    return out


def points_changed(a, b) -> int:
    """The points of the space where two bases' decisions differ."""
    qa, qb = decided_by_queue(a), decided_by_queue(b)
    changed = 0
    for q in set(qa) | set(qb):
        changed |= qa.get(q, 0) ^ qb.get(q, 0)
    return changed.bit_count()


def arrivals_right(decisions: dict, truth: Sequence[str]) -> int:
    return sum(1 for i, d in decisions.items()
               if d.outcome == "ACTION" and d.action == truth[i])


def same_decisions(a: dict, b: dict) -> bool:
    return a.keys() == b.keys() and all(
        (a[i].outcome, a[i].winner_id, a[i].action)
        == (b[i].outcome, b[i].winner_id, b[i].action) for i in a)


# ---------------------------------------------------------------------------
# C: the class, as it arrived
# ---------------------------------------------------------------------------

def class_tickets(record: dict, engine) -> list[dict]:
    """Every arrival of the class, as it was decided, with the rules of the
    class that matched it then and what defeated them."""
    corpus = I.corpus()
    action = {r.rule_id: r.action for r in engine.rules}
    born = {r["born_at"]: r for r in record["rules"]}
    out = []
    for row in record["records"]:
        if row["truth"] != SI:
            continue
        idx = row["idx"]
        t: dict[str, Any] = {"case": idx, "ticket_rule": row["truth_rule"],
                             "outcome": row["outcome"], "escalated": row["escalated"],
                             "winner": row["winner_id"], "named": row["predicted"],
                             "right": bool(row["correct"])}
        if row["outcome"] == "ACTION":
            matched = {r.rule_id for r in engine.rules
                       if r.born_at < idx and r.matches(corpus[idx])}
            t["matched"] = sorted(matched)
            t["class_rules"] = [
                {"rule_id": s,
                 "by_subsumption": sorted(engine.sub_below[s] & matched),
                 "by_declaration": sorted(engine.decl_below[s] & matched)}
                for s in sorted(matched) if action[s] == SI]
        if idx in born:
            t["born"] = {"rule_id": born[idx]["rule_id"], "queue": born[idx]["action"]}
        out.append(t)
    return out


def rule_card(rid: str, record: dict, engine, outside: int,
              tmask: dict[str, int]) -> dict[str, Any]:
    """A rule as the class's reading shows it."""
    rows = {r["idx"]: r for r in record["records"]}
    d = next(r for r in record["rules"] if r["rule_id"] == rid)
    rule = next(r for r in engine.rules if r.rule_id == rid)
    E = engine.ext[rid]
    birth = rows[d["born_at"]]
    return {"rule_id": rid, "rule": rule.render(), "queue": d["action"],
            "born_at": d["born_at"], "birth_outcome": birth["outcome"],
            "birth_truth": birth["truth"], "birth_ticket_rule": birth["truth_rule"],
            "birth_has_keyword": bool(I.corpus()[d["born_at"]].has_security_keyword),
            "keyword_rule": brows.is_keyword(E, outside),
            "points": E.bit_count(), "class_points": (E & tmask[SI]).bit_count(),
            "fire_count": d["fire_count"], "correct_count": d["correct_count"],
            "note": d.get("note", "")}


def class_over_space(engine, tmask: dict[str, int]) -> dict[str, Any]:
    """Who decides the class's points over the space: by queue, and by rule
    where its queue is the only one undefeated."""
    region = tmask[SI]
    by_q = decided_by_queue(engine)
    one = two = 0
    for m in by_q.values():
        two |= one & m
        one |= m
    only = one & ~two
    action = {r.rule_id: r.action for r in engine.rules}
    rules = {rid: (m & only & region).bit_count()
             for rid, m in brows.undefeated_masks(engine).items() if m & only & region}
    return {"points": region.bit_count(),
            "by_queue": {q: (m & only & region).bit_count() for q, m in sorted(by_q.items())
                         if m & only & region},
            "conflict": (two & region).bit_count(), "impasse": (region & ~one).bit_count(),
            "rules": [{"rule_id": rid, "queue": action[rid], "points": n}
                      for rid, n in sorted(rules.items(), key=lambda kv: (-kv[1], kv[0]))]}


def class_reading(record: dict, engine, outside: int, tmask: dict[str, int]
                  ) -> dict[str, Any]:
    tickets = class_tickets(record, engine)
    deciders = Counter(t["winner"] for t in tickets if t["outcome"] == "ACTION")
    right = Counter(t["winner"] for t in tickets if t["outcome"] == "ACTION" and t["right"])
    esc = [t for t in tickets if t["escalated"]]
    cards = []
    for rid, n in sorted(deciders.items(), key=lambda kv: (-kv[1], kv[0])):
        card = rule_card(rid, record, engine, outside, tmask)
        card.update({"decided": n, "decided_right": right[rid],
                     "arrived_by_its_birth": sum(1 for t in tickets
                                                 if t["case"] <= card["born_at"])})
        cards.append(card)
    return {"tickets": tickets,
            "decided": sum(deciders.values()), "decided_right": sum(right.values()),
            "escalated": len(esc), "named_right": sum(t["named"] == SI for t in esc),
            "first_arrival": min((t["case"] for t in tickets), default=None),
            "deciders": cards}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def less(a: Fraction | None, b: Fraction | None) -> bool:
    return a is not None and b is not None and a < b


def read_expectation(A: dict, B: dict, C: dict) -> list[dict[str, Any]]:
    lv = A["levels"]
    out = []

    def clause(c: str, holds: bool, reading: str) -> None:
        out.append({"clause": c, "holds": bool(holds), "reading": reading})

    a1 = {}
    for k in A1_LEVELS:
        s = lv[str(k)]["classes"]
        inside = share(s["region"]["cross"], s["region"]["births"])
        other = share(s["rule"]["cross"] + s["beyond"]["cross"],
                      s["rule"]["births"] + s["beyond"]["births"])
        a1[k] = (inside, other)
    clause("A1", all(less(*a1[k]) for k in A1_LEVELS),
           "; ".join(f"L{k}: region {fmt(a1[k][0])} against {fmt(a1[k][1])}"
                     for k in A1_LEVELS))
    r2, r3 = lv["2"]["class_share"]["region"], lv["3"]["class_share"]["region"]
    clause("A2", less(r2, r3), f"region: L3 {fmt(r3)} against L2 {fmt(r2)}")
    m = A["mix"]
    lo, hi = m["mix_share_low_rates"], m["mix_share_high_rates"]
    clause("A3", m["gap"] is not None and m["gap"] > 0 and lo is not None
           and hi is not None and lo > A3_SHARE and hi > A3_SHARE,
           f"gap {fmt(m['gap'])}; the mix carries {fmt(lo)} on L2's rates and "
           f"{fmt(hi)} on L3's")
    b2_, b3_ = lv["2"]["class_share"]["beyond"], lv["3"]["class_share"]["beyond"]
    clause("A4", less(b3_, b2_), f"beyond: L2 {fmt(b2_)} against L3 {fmt(b3_)}")

    n = B["declarations"]
    kinds = B["kinds"]
    idle = kinds.get("idle", 0) + kinds.get("inert", 0)
    clause("B1", n and Fraction(idle, n) >= B1_IDLE, f"{idle} of {n} idle or inert")
    hit, miss = B["points"].get("hit", 0), B["points"].get("miss", 0)
    clause("B2", hit + miss > 0 and Fraction(hit, hit + miss) >= B2_HIT,
           f"{hit} of {hit + miss} at stake with a strict better side point at it")
    t1 = B["counterparts"]["T1"]["shown"]
    clause("B3", n and Fraction(t1, n) < B3_T1, f"{t1} of {n} have a T1 rule shown")
    worst = max(((r["points_changed"], r["arrivals_changed"])
                 for t in TRANSLATIONS for r in B["translations"][t]["runs"].values()),
                default=(0, 0))
    clause("B4", all(r["points_changed"] < B4_POINTS and r["arrivals_changed"] < B4_ARRIVALS
                     for t in TRANSLATIONS for r in B["translations"][t]["runs"].values()),
           f"at most {worst[0]} points and {worst[1]} arrivals change, under either")

    l2 = [C["runs"][f"L2 r{r}"] for r in (1, 2, 3)]
    tops = [x["deciders"][0] if x["deciders"] else None for x in l2]
    clause("C1", all(t is not None and Fraction(t["decided"], x["decided"]) > C1_SHARE
                     for t, x in zip(tops, l2)),
           "; ".join(f"r{i}: {t['rule_id']} {t['decided']} of {x['decided']}"
                     if t else f"r{i}: none" for i, (t, x) in enumerate(zip(tops, l2), 1)))
    clause("C2", all(t is not None and t["queue"] == T2 for t in tops),
           ", ".join(t["queue"] if t else "none" for t in tops))
    clause("C3", all(t is not None and t["keyword_rule"] for t in tops),
           ", ".join(str(t["keyword_rule"]) if t else "none" for t in tops))
    faced = sum(1 for x in l2 for t in x["tickets"]
                if t["outcome"] == "ACTION" and not t["right"] and t["class_rules"])
    clause("C4", faced == 0, f"{faced} wrong decisions faced a rule of the class")
    return out


def fmt(x: Any) -> str:
    if x is None:
        return "none"
    if isinstance(x, Fraction):
        return f"{float(x):.4f}"
    return str(x)


# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry = "--dry-run" in argv
    if [a for a in argv if a != "--dry-run"]:
        print(__doc__)
        return 2
    gate = plan.refuse_unsigned("manual/readings.py writes nothing")
    t0 = time.time()
    recs, sc, hidden = load_runs(), load_scored(), hidden_rules()
    sp, corpus, tmask, outside = I.space(), list(I.corpus()), I.space_truth(), I.outside()
    full = (1 << sp.n) - 1
    off: dict[str, list] = defaultdict(list)

    print("=" * 78)
    print("PLAN_MANUAL.md — THREE READINGS STAGE C LEFT FREE — POST-RUN")
    print("=" * 78)

    # Gate 1: the runs are the records'.
    built = {}
    for run, rec in recs.items():
        rb = rebuild(rec, corpus, sp)
        built[run] = rb
        for row in rec["records"]:
            d = rb.decisions[row["idx"]]
            if (d.outcome, d.winner_id) != (row["outcome"], row["winner_id"]) or (
                    row["outcome"] == "ACTION" and d.action != row["predicted"]):
                off["1"].append(f"{name(run)}:{row['idx']}")
        cells = sc[run]["cells"]
        if (I.over_space(rb.engine)["correct"] != cells["space"]["correct"]
                or I.over_corpus(rb.engine)["correct"] != cells["corpus"]["correct"]):
            off["1"].append(f"{name(run)}:base")

    # Gate 2: the policy is one convention.
    union = 0
    for rid, H in hidden.items():
        union |= H["region"]
        if not (contains(H["ext"], H["region"]) and contains(tmask[H["queue"]], H["region"])):
            off["2"].append(f"the region of {rid}")
    if union != full or sum(H["region"].bit_count() for H in hidden.values()) != sp.n:
        off["2"].append("the regions do not partition the space")
    first = {i: rid for rid, H in hidden.items() for i in H["cases"]}
    if sorted(first) != list(range(len(corpus))):
        off["2"].append("a corpus case without its rule")
    for run, rec in recs.items():
        for row in rec["records"]:
            if (row["truth_rule"] != first.get(row["idx"])
                    or row["truth"] != hidden[row["truth_rule"]]["queue"]):
                off["2"].append(f"{name(run)}:{row['idx']}")

    # Gate 3: the answers are the records'.
    drops: dict[tuple[int, int], list[dict]] = {}
    for run, rec in recs.items():
        rows = {r["idx"]: r for r in rec["records"]}
        born = {r["rule_id"]: r["born_at"] for r in rec["rules"]}
        if len(set(born.values())) != len(born):
            off["3"].append(f"{name(run)}: two births at one case")
        for r in rec["rules"]:
            row = rows[r["born_at"]]
            if not row["escalated"] or row["rejected_reason"] is not None:
                off["3"].append(f"{name(run)}:{r['rule_id']} born off an escalation")
        for row in rec["records"]:
            if any(born.get(s, row["idx"]) >= row["idx"] for s in row["shown_ids"] or []):
                off["3"].append(f"{name(run)}:{row['idx']} shows a rule not yet born")
        try:
            drops[run] = dropped(rec)
        except AnswerError as exc:
            off["3"].append(f"{name(run)}: {exc}")
            continue
        if (any(d["cites"] not in hidden for d in drops[run])
                or len(drops[run]) != DROPPED.get(run, 0)):
            off["3"].append(f"{name(run)}: {len(drops[run])} drops outside")

    # Gate 4: two routes agree.
    births: dict[tuple[int, int], list[dict]] = {}
    for run, rec in recs.items():
        rows = {r["idx"]: r for r in rec["records"]}
        ext = dict(built[run].engine.ext)
        births[run] = births_read(rec["rules"], rows, hidden, ext, outside)
        b = brows.births_outside(rec["rules"], sp, outside)
        alone = sum(not x["crosses"] for x in births[run])
        ka = Fraction(alone, len(births[run])) if births[run] else Fraction(1)
        if (b["outside"], b["alone_outside"]) != (len(births[run]), alone) \
                or ka != frac(sc[run]["k_a"]) or ka != I.k_a_exact(rec["rules"]):
            off["4"].append(f"{name(run)}:k_a")
        si = [r for r in rec["records"] if r["truth"] == SI and r["outcome"] == "ACTION"]
        rare = sc[run]["rare"][SI]
        if (len(si), sum(bool(r["correct"]) for r in si)) != (
                rare["decided_by_a_rule"], rare["decided_right"]):
            off["4"].append(f"{name(run)}:class")
        copy_, keys = written_in(rec, {})
        again = rebuild(copy_, corpus, sp)
        if keys or not same_decisions(again.decisions, built[run].decisions) or \
                points_changed(again.engine, built[run].engine):
            off["4"].append(f"{name(run)}:copy")

    checked = [{"gate": g, "what": what, "off": off.get(g, []), "passes": not off.get(g)}
               for g, what in (("1", "the runs are the records'"),
                               ("2", "the policy is one convention"),
                               ("3", "the answers are the records'"),
                               ("4", "two routes agree"))]
    for g in checked:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}"
              + ("" if g["passes"] else f"  off: {g['off'][:12]}"))
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if dry:
        print(f"\n  --dry-run: the gates ran and nothing was written "
              f"({time.time() - t0:.0f} s).")
        return 0

    # A: the births, by level.
    A = {"runs": {name(run): summary(births[run]) for run in recs},
         "levels": {str(lv): summary([b for run in recs if run[0] == lv
                                      for b in births[run]]) for lv in plan.LEVELS},
         "births": {name(run): births[run] for run in recs}}
    A["mix"] = mix_split(A["levels"]["2"], A["levels"]["3"])

    # B: level 3's dropped declarations.
    rows_b, counts = [], {t: Counter() for t in TRANSLATIONS}
    trans: dict[str, dict] = {t: {"runs": {}} for t in TRANSLATIONS}
    for run in sorted(r for r in recs if r[0] == 3):
        rec, eng = recs[run], built[run].engine
        rows = {r["idx"]: r for r in rec["records"]}
        action = {r.rule_id: r.action for r in eng.rules}
        born = {r.rule_id: r.born_at for r in eng.rules}
        edges = {t: {} for t in TRANSLATIONS}
        for d in drops[run]:
            H = hidden[d["cites"]]
            shown = list(rows[d["case"]]["shown_ids"] or [])
            unshown = [r for r, b in sorted(born.items(), key=lambda kv: (kv[1], kv[0]))
                       if b < d["case"] and r not in shown]
            on, off_ = (counterparts(H, shown, eng.ext, action),
                        counterparts(H, unshown, eng.ext, action))
            row = d | {"run": name(run), "rule_queue": action[d["rule"]],
                       "cited_queue": H["queue"],
                       "claim": claim(d, eng.ext, action, hidden, tmask),
                       "T1": {"shown": on["T1"], "unshown": off_["T1"]},
                       "T2": {"shown": on["T2"], "unshown": off_["T2"]}}
            for t in TRANSLATIONS:
                counts[t]["shown" if on[t] else "unshown" if off_[t] else "none"] += 1
                if on[t]:
                    edges[t][(d["case"], d["k"])] = pairs_of(d, on[t])
            rows_b.append(row)
        truth = [r["truth"] for r in sorted(rec["records"], key=lambda r: r["idx"])]
        base = built[run]
        for t in TRANSLATIONS:
            copy_, keys = written_in(rec, edges[t])
            rb = rebuild(copy_, corpus, sp)
            tried = Counter(rb.tried[k] for ks in keys.values() for k in ks)
            installed = sum(1 for ks in keys.values() for k in ks if k in rb.installed)
            changed = [i for i in rb.decisions
                       if (rb.decisions[i].outcome, rb.decisions[i].action)
                       != (base.decisions[i].outcome, base.decisions[i].action)]
            trans[t]["runs"][name(run)] = {
                "declarations": len(edges[t]),
                "edges": sum(len(v) for v in edges[t].values()),
                "tried": dict(tried), "installed": installed,
                "space": [I.over_space(base.engine)["correct"],
                          I.over_space(rb.engine)["correct"]],
                "corpus": [I.over_corpus(base.engine)["correct"],
                           I.over_corpus(rb.engine)["correct"]],
                "points_changed": points_changed(base.engine, rb.engine),
                "arrivals_right": [arrivals_right(base.decisions, truth),
                                   arrivals_right(rb.decisions, truth)],
                "arrivals_changed": len(changed),
                "arrivals_changed_right": [
                    sum(1 for i in changed if base.decisions[i].outcome == "ACTION"
                        and base.decisions[i].action == truth[i]),
                    sum(1 for i in changed if rb.decisions[i].outcome == "ACTION"
                        and rb.decisions[i].action == truth[i])]}
    B = {"declarations": len(rows_b),
         "by_run": dict(Counter(r["run"] for r in rows_b)),
         "directions": dict(Counter(r["direction"] for r in rows_b)),
         "kinds": dict(Counter(r["claim"]["kind"] for r in rows_b)),
         "points": dict(Counter(r["claim"]["point"] for r in rows_b
                                if r["claim"]["kind"] == "at_stake")),
         "containment": dict(Counter(f"{r['claim']['containment']}|"
                                     f"{r['claim']['agrees_with_containment']}"
                                     for r in rows_b)),
         "cited": dict(Counter(r["cites"] for r in rows_b).most_common()),
         "counterparts": {t: {"shown": counts[t]["shown"], "unshown": counts[t]["unshown"],
                              "none": counts[t]["none"]} for t in TRANSLATIONS},
         "translations": trans, "rows": rows_b}

    # C: the class, as it arrived, and over the space under the prose.
    C = {"runs": {name(run): class_reading(recs[run], built[run].engine, outside, tmask)
                  for run in recs},
         "space": {name(run): class_over_space(built[run].engine, tmask)
                   for run in recs if run[0] == 2}}

    expectation = read_expectation(A, B, C)
    for e in expectation:
        print(f"  {e['clause']}: {'holds' if e['holds'] else 'FAILS'}  {e['reading']}")

    record_path().write_text(json.dumps(plain({
        "_env": environment(),
        "what": "why the prose made the loop cross more than the rules did, what "
                "level 3's dropped declarations would have decided, and which rule "
                "decided SECURITY_INCIDENT wrong under the prose",
        "plan": str(plan.PLAN),
        "gate": gate,
        "provenance": PROVENANCE,
        "source": {"records": [str(plan.loop_path(lv, rep)) for (lv, rep) in recs]
                   + [str(plan.score_path())],
                   "policy": "HIDDEN_DSL, through manual/instrument.py's regions"},
        "surface": "the exhaustive space, 134,400 points, and the corpus's 2,000 "
                   "arrivals; each run's final base read whole, and the arrivals "
                   "as the rules decided them; every count against the truth",
        "gates": checked,
        "A": A,
        "B": B,
        "C": C,
        "expectation": expectation,
        "seconds": round(time.time() - t0, 1),
    }), indent=2, default=str) + "\n")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
