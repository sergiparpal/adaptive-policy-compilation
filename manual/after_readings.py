"""
AFTER THE READINGS: `K-a`'S OWN SURFACE, AND WHAT THE THREE READINGS FOUND
BESIDE THEIR CLAUSES. `manual/readings.py` read three things Stage C left free,
and its record, `results_manual/readings.json`, holds four of its twelve
clauses. Three failed on the reading's own convention, not on the bases:
- it read A's classes over the whole space, and `K-a` reads the half without
  the keyword;
- a rule that does not name the keyword reaches the keyword's half, which only
  `H01` to `H03` decide;
- so such a rule can never lie inside the region of a lower rule, and no birth
  of L₀, L₂ or L₃ fell in `region`.
This module reads A again where `K-a` reads, and two things the record showed
beside its clauses. POST-RUN, **and nothing in it is a bet**: see PROVENANCE.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  A. **Why the prose made the loop cross more than the rules did, on `K-a`'s
     surface.** Every birth `K-a` reads is classed as `manual/readings.py`
     classes it, with each extension cut to the half without the keyword:
     the birth's, its ticket's rule's, and that rule's region. Beside the
     classes, a second partition: **breadth**, the birth's points off the
     keyword. Its bands are cut at the quartiles of L₂'s and L₃'s births
     pooled. For each partition and level: the births and how many cross.
     The gap between L₂'s and L₃'s pooled `K-a` is split by each partition's
     mix, each level's rates read on the other's mix.
  B. **Whose declarations against the manual were right.** The declarations
     at stake with a strict better side over the space, split by whether the
     declaring rule names the queue of the ticket it was born on.
  C. **Why the class went astray under the prose and not under the
     catalogue.**
     - For each level: how many rules exclude the keyword, their extension
       inside the half without it.
     - For each run: the first arrival with the keyword, how it was decided
       and by which rule; and the keyword rules, the ones inside the keyword's
       half, with their queues and births.
     - The class's arrivals by the hidden rule that governs them, `H01` or
       `H02`, by how they were decided, and whether rightly.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
- `results_manual/readings.json`, for gate 1;
- the twelve loop records, rebuilt by `edges.rebuild.rebuild`;
- `HIDDEN_DSL`, through `manual/readings.py`'s `hidden_rules`.
Every function `manual/readings.py` has is called, not copied: the births are
its `births_read`, the classes its `classify`. What is new is only the cut to
the half without the keyword, the bands, and a mix split that takes any
partition's keys.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The births and the class are the reading's.**
     - Every run's births, by rule, crossing and whole-space class, are
       `readings.json`'s.
     - The class's arrivals, decided and right, are `readings.json`'s.
     - The mix split by whole-space classes, through this module's split,
       is `readings.json`'s.
  2. **The halves are the policy's.**
     - The regions of `H01` to `H03` lie in the keyword's half, and every
       other region lies in the half without it.
     - A birth whose extension lies off the keyword has one class on both
       surfaces.
  3. **Two routes give the exclusion.** A rule's extension lies in the half
     without the keyword exactly when one of its conditions admits only
     `False` for the keyword.
  4. **The bands partition the births.** Every birth falls in exactly one
     band, the bands' counts sum to each level's births, and no band is empty
     among the births that cut it.

It refuses to write if any fails, and while `PLAN_MANUAL.md` is unsigned.
`--dry-run` runs the four, prints pass or fail, and writes nothing.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN, after `readings.json`**, asked for on 2026-10-22 when three of
that record's clauses were found to fail on its own convention. **Before
writing this module, the drafter computed most of what it records** in a
scratch exploration of the records, after reading `readings.json`:
- the classes off the keyword;
- crossing by the pooled quartiles of breadth;
- the declarations at stake beside their rules' queues;
- the rules that exclude the keyword;
- the class's arrivals by hidden rule and outcome.
**So no figure here could have surprised its author.** It carries no
expectation, is not a signed row, is not on `STATUS.md`'s scoreboard, and
moves no verdict. Zero API calls.

Usage:  python3 -m manual.after_readings --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m manual.after_readings
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Sequence

from harness.provenance import describe, environment

from blind import rows as brows
from edges.rebuild import rebuild

from . import instrument as I
from . import plan
from . import readings as R
from .score import plain

KW = brows.KW
KEYWORD_RULES = ("H01", "H02", "H03")     # the hidden policy's first layer
BANDS = ("b1", "b2", "b3", "b4")
PROVENANCE = (
    "POST-RUN, after results_manual/readings.json: written on 2026-10-22 when "
    "three of that record's clauses were found to fail on its own convention. "
    "The drafter computed most of these figures in a scratch exploration before "
    "writing the module, so none is a bet. No expectation; no verdict moves.")


def record_path() -> Path:
    return plan.OUT / "after_readings.json"


# ---------------------------------------------------------------------------
# A, off the keyword
# ---------------------------------------------------------------------------

def off_keyword(H: dict, outside: int) -> dict:
    """A hidden rule's extension and region, cut to the half without the keyword."""
    return {"ext": H["ext"] & outside, "region": H["region"] & outside}


def classes_off(births: Sequence[dict], ext: dict[str, int], hidden: dict,
                outside: int) -> dict[str, str]:
    """Every birth's class, read where `K-a` reads."""
    return {b["rule_id"]: R.classify(ext[b["rule_id"]] & outside,
                                     off_keyword(hidden[b["ticket_rule"]], outside))
            for b in births}


def edges_of(values: Sequence[int]) -> list[float]:
    """The quartiles that cut the bands."""
    return statistics.quantiles(values, n=4)


def band(points: int, cuts: Sequence[float]) -> str:
    return BANDS[sum(points > c for c in cuts)]


def split(items: Sequence[tuple[dict, str]], keys: Sequence[str]) -> dict[str, Any]:
    """A level's births, pooled, by the part of a partition each falls in. Each
    item is a birth and its part: a level pools three runs, whose rule ids
    repeat, so the part travels with the birth."""
    by = {k: {"births": 0, "cross": 0} for k in keys}
    for b, part in items:
        d = by[part]
        d["births"] += 1
        d["cross"] += b["crosses"]
    n = len(items)
    alone = sum(not b["crosses"] for b, _ in items)
    return {"births": n, "alone": alone, "k_a": R.share(alone, n), "parts": by,
            "part_share": {k: R.share(by[k]["births"], n) for k in keys},
            "cross_rate": {k: R.share(by[k]["cross"], by[k]["births"]) for k in keys}}


def on_mix(rates_of: dict, mix_of: dict, keys: Sequence[str]) -> Fraction | None:
    """`manual/readings.py`'s `on_mix`, over any partition's keys."""
    n = sum(mix_of[k]["births"] for k in keys)
    if not n:
        return None
    total = Fraction(0)
    for k in keys:
        w = mix_of[k]["births"]
        if w:
            r = R.alone_rate(rates_of[k])
            if r is None:
                return None
            total += Fraction(w, n) * r
    return total


def mix_split(low: dict, high: dict, keys: Sequence[str]) -> dict[str, Any]:
    """`manual/readings.py`'s `mix_split`, over any partition's keys."""
    ka_l, ka_h = low["k_a"], high["k_a"]
    gap = ka_h - ka_l if ka_l is not None and ka_h is not None else None
    l_on_h = on_mix(low["parts"], high["parts"], keys)
    h_on_l = on_mix(high["parts"], low["parts"], keys)
    ok = bool(gap)
    return {"gap": gap, "low_rates_on_high_mix": l_on_h, "high_rates_on_low_mix": h_on_l,
            "mix_share_low_rates": (l_on_h - ka_l) / gap if ok and l_on_h is not None
            else None,
            "mix_share_high_rates": (ka_h - h_on_l) / gap if ok and h_on_l is not None
            else None}


# ---------------------------------------------------------------------------
# C, the keyword
# ---------------------------------------------------------------------------

def admits_only_false(cond: dict) -> bool:
    """A condition on the keyword that lets only tickets without it through."""
    if cond["attr"] != KW:
        return False
    op, v = cond["op"], cond["value"]
    return ((op == "eq" and v is False) or (op == "neq" and v is True)
            or (op == "in" and list(v) == [False]))


def excludes_keyword(rule: dict) -> bool:
    return any(admits_only_false(c) for c in rule["conditions"])


def first_keyword_arrival(record: dict, engine, outside: int) -> dict[str, Any]:
    corpus = I.corpus()
    row = next(r for r in sorted(record["records"], key=lambda r: r["idx"])
               if corpus[r["idx"]].has_security_keyword)
    out = {"case": row["idx"], "truth": row["truth"], "ticket_rule": row["truth_rule"],
           "outcome": row["outcome"], "named": row["predicted"],
           "winner": row["winner_id"]}
    if row["winner_id"]:
        out["winner_rule"] = next(r.render() for r in engine.rules
                                  if r.rule_id == row["winner_id"])
        out["winner_reaches_keyword"] = bool(engine.ext[row["winner_id"]] & ~outside)
    born = [r for r in engine.rules if r.born_at == row["idx"]]
    if born:
        out["born"] = born[0].render()
    return out


def keyword_rules(record: dict, engine, outside: int) -> list[dict[str, Any]]:
    """The rules inside the keyword's half, in birth order."""
    rows = {r["idx"]: r for r in record["records"]}
    return [{"rule_id": r.rule_id, "rule": r.render(), "queue": r.action,
             "born_at": r.born_at, "birth_truth": rows[r.born_at]["truth"],
             "birth_ticket_rule": rows[r.born_at]["truth_rule"],
             "points": engine.ext[r.rule_id].bit_count()}
            for r in engine.rules if brows.is_keyword(engine.ext[r.rule_id], outside)]


def class_arrivals(record: dict) -> dict[str, int]:
    """The class's arrivals by governing rule, outcome and whether right."""
    c = Counter(f"{r['truth_rule']}|{r['outcome']}|{'right' if r['correct'] else 'wrong'}"
                for r in record["records"] if r["truth"] == R.SI)
    return dict(sorted(c.items()))


# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry = "--dry-run" in argv
    if [a for a in argv if a != "--dry-run"]:
        print(__doc__)
        return 2
    gate = plan.refuse_unsigned("manual/after_readings.py writes nothing")
    t0 = time.time()
    before = json.loads(R.record_path().read_text())
    recs, hidden = R.load_runs(), R.hidden_rules()
    sp, corpus, outside = I.space(), list(I.corpus()), I.outside()
    off: dict[str, list] = defaultdict(list)

    print("=" * 78)
    print("PLAN_MANUAL.md — AFTER THE READINGS — POST-RUN")
    print("=" * 78)

    built = {run: rebuild(rec, corpus, sp) for run, rec in recs.items()}
    births, cls_off = {}, {}
    for run, rec in recs.items():
        eng = built[run].engine
        rows = {r["idx"]: r for r in rec["records"]}
        births[run] = R.births_read(rec["rules"], rows, hidden, dict(eng.ext), outside)
        cls_off[run] = classes_off(births[run], eng.ext, hidden, outside)

    # Gate 1: the births and the class are the reading's.
    for run in recs:
        theirs = before["A"]["births"][R.name(run)]
        if [(b["rule_id"], b["crosses"], b["class"]) for b in births[run]] != \
                [(b["rule_id"], b["crosses"], b["class"]) for b in theirs]:
            off["1"].append(f"{R.name(run)}:births")
        mine = R.class_reading(recs[run], built[run].engine, outside, I.space_truth())
        c = before["C"]["runs"][R.name(run)]
        if (mine["decided"], mine["decided_right"], mine["escalated"]) != (
                c["decided"], c["decided_right"], c["escalated"]):
            off["1"].append(f"{R.name(run)}:class")
    whole = {lv: split([(b, b["class"]) for run in recs if run[0] == lv
                        for b in births[run]], R.CLASSES) for lv in (2, 3)}
    again = plain(mix_split(whole[2], whole[3], R.CLASSES))
    if any(again[k] != before["A"]["mix"][k] for k in again):
        off["1"].append("the mix split")

    # Gate 2: the halves are the policy's.
    for rid, H in hidden.items():
        inside_kw = not H["region"] & outside
        if H["region"] and inside_kw != (rid in KEYWORD_RULES):
            off["2"].append(rid)
    for run in recs:
        eng = built[run].engine
        for b in births[run]:
            if not eng.ext[b["rule_id"]] & ~outside and cls_off[run][b["rule_id"]] != b["class"]:
                off["2"].append(f"{R.name(run)}:{b['rule_id']}")

    # Gate 3: two routes give the exclusion.
    for run, rec in recs.items():
        eng = built[run].engine
        for r in rec["rules"]:
            if excludes_keyword(r) != (eng.ext[r["rule_id"]] & ~outside == 0):
                off["3"].append(f"{R.name(run)}:{r['rule_id']}")

    # Gate 4: the bands partition the births.
    cuts = edges_of([b["points_outside"] for run in recs if run[0] in (2, 3)
                     for b in births[run]])
    bands = {run: {b["rule_id"]: band(b["points_outside"], cuts) for b in births[run]}
             for run in recs}
    for lv in plan.LEVELS:
        s = split([(b, bands[run][b["rule_id"]]) for run in recs if run[0] == lv
                   for b in births[run]], BANDS)
        if sum(p["births"] for p in s["parts"].values()) != s["births"]:
            off["4"].append(f"L{lv}")
    held = Counter(bands[run][b["rule_id"]] for run in recs if run[0] in (2, 3)
                   for b in births[run])
    if any(not held[k] for k in BANDS):
        off["4"].append("an empty band")

    checked = [{"gate": g, "what": what, "off": off.get(g, []), "passes": not off.get(g)}
               for g, what in (("1", "the births and the class are the reading's"),
                               ("2", "the halves are the policy's"),
                               ("3", "two routes give the exclusion"),
                               ("4", "the bands partition the births"))]
    for g in checked:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}"
              + ("" if g["passes"] else f"  off: {g['off'][:12]}"))
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if dry:
        print(f"\n  --dry-run: the gates ran and nothing was written "
              f"({time.time() - t0:.0f} s).")
        return 0

    # A: both partitions, by level, and the gap split by each.
    def pooled(lv: int, key_of: dict, keys: Sequence[str]) -> dict:
        return split([(b, key_of[run][b["rule_id"]]) for run in recs if run[0] == lv
                      for b in births[run]], keys)
    A = {"classes_off_keyword": {str(lv): pooled(lv, cls_off, R.CLASSES)
                                 for lv in plan.LEVELS},
         "bands": {"cuts": cuts,
                   "levels": {str(lv): pooled(lv, bands, BANDS) for lv in plan.LEVELS}},
         "births_points_outside_median": {
             str(lv): statistics.median(b["points_outside"] for run in recs
                                        if run[0] == lv for b in births[run])
             for lv in plan.LEVELS}}
    A["mix_classes_off_keyword"] = mix_split(A["classes_off_keyword"]["2"],
                                             A["classes_off_keyword"]["3"], R.CLASSES)
    A["mix_bands"] = mix_split(A["bands"]["levels"]["2"], A["bands"]["levels"]["3"], BANDS)

    # B: the declarations at stake, by whether their rule names its ticket's queue.
    truth_at = {run: {r["idx"]: r["truth"] for r in rec["records"]}
                for run, rec in recs.items()}
    born_at = {run: {r["rule_id"]: (r["born_at"], r["action"]) for r in rec["rules"]}
               for run, rec in recs.items()}
    rows_b = []
    for row in before["B"]["rows"]:
        if row["claim"]["kind"] != "at_stake":
            continue
        run = tuple(int(x[1:]) for x in row["run"].split())
        b, q = born_at[run][row["rule"]]
        rows_b.append({"run": row["run"], "rule": row["rule"], "queue": q,
                       "ticket_truth": truth_at[run][b], "names_its_queue": q == truth_at[run][b],
                       "direction": row["direction"], "cites": row["cites"],
                       "point": row["claim"]["point"]})
    B = {"rows": rows_b,
         "by_queue_named": {f"{'right' if k else 'wrong'}_queue": dict(Counter(
             r["point"] for r in rows_b if r["names_its_queue"] == k)) for k in (True, False)},
         "rules": {f"{'right' if k else 'wrong'}_queue": len({(r["run"], r["rule"])
                                                              for r in rows_b
                                                              if r["names_its_queue"] == k})
                   for k in (True, False)}}

    # C: the keyword, rule by rule.
    C = {"levels": {str(lv): {"rules": sum(len(recs[run]["rules"]) for run in recs
                                           if run[0] == lv),
                              "exclude_keyword": sum(excludes_keyword(r) for run in recs
                                                     if run[0] == lv
                                                     for r in recs[run]["rules"]),
                              "keyword_rules": sum(len(keyword_rules(recs[run],
                                                                     built[run].engine,
                                                                     outside))
                                                   for run in recs if run[0] == lv)}
                    for lv in plan.LEVELS},
         "runs": {R.name(run): {
             "first_keyword_arrival": first_keyword_arrival(recs[run], built[run].engine,
                                                            outside),
             "keyword_rules": keyword_rules(recs[run], built[run].engine, outside),
             "class_arrivals": class_arrivals(recs[run])} for run in recs}}

    for lv in plan.LEVELS:
        a, c = A["classes_off_keyword"][str(lv)], C["levels"][str(lv)]
        print(f"  L{lv}: {a['births']} births read, off-keyword classes "
              f"{ {k: (v['births'], v['cross']) for k, v in a['parts'].items()} }; "
              f"{c['exclude_keyword']} of {c['rules']} rules exclude the keyword")
    for name_, m in (("classes", A["mix_classes_off_keyword"]), ("bands", A["mix_bands"])):
        print(f"  mix by {name_}: {R.fmt(m['mix_share_low_rates'])} on L2's rates, "
              f"{R.fmt(m['mix_share_high_rates'])} on L3's")

    record_path().write_text(json.dumps(plain({
        "_env": environment(),
        "what": "manual/readings.py's A read on K-a's own surface, and what its "
                "B and C showed beside their clauses",
        "plan": str(plan.PLAN),
        "gate": gate,
        "provenance": PROVENANCE,
        "follows": str(R.record_path()),
        "surface": "the half of the space without the keyword for A, as K-a reads "
                   "it; the space for B's declarations; the corpus's arrivals for C",
        "gates": checked,
        "A": A,
        "B": B,
        "C": C,
        "seconds": round(time.time() - t0, 1),
    }), indent=2, default=str) + "\n")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
