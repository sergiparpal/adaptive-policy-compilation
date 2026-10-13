"""
WHY RUNG 1'S LOOP WROTE THE SAME RULE AGAIN. `FINDINGS3.md` §18 found that 307
of rung 1's 577 rules have a copy written with the same conditions, in 83
groups. Rung 1's record keeps each case's outcome and not which rules tied, so
whether a copy was born on a case its earlier copies had sent to escalation was
not read. This replays rung 1's engine over the corpus, adding each rule where
the loop added it, and reads at every birth which rules tied. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
Rung 1's engine decides a case by specificity. Among the rules that match, the
finalists are those with the most conditions. If they carry one queue the
oldest wins; if they carry two or more, the case is a CONFLICT and escalates.
The loop then asks the model, which does not see the base, for a rule, and adds
it if it matches its case.

A rule written the same as an earlier one matches the same cases. So at a later
copy's birth its earlier copies matched the case too, and the case was no
IMPASSE: it escalated on a CONFLICT. **Whose?** Either an earlier copy was a
finalist, tied with a rule of another queue at the same specificity. That is
the group's own tie: the age tie-break never reaches it, and a copy cannot break
it, since a copy has the same conditions. Or the earlier copies were
out-specified, and the tie was among more specific rules: someone else's.

**And a later copy can never decide a case.** Wherever it is a finalist its
earlier copy is one too, as specific and older. If they agree, the older wins;
if they disagree, the case is a CONFLICT.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
`results/llm_run.json`, rung 1's run at n=2000, replayed through
`harness.dsl.RuleEngine`, used and not edited, on the 2,000 cases of seed 17 in
the order the loop met them. Each recorded rule is validated against its own
case and added after that case is decided, as `harness.shadow.run_shadow` does.
The groups are §18's: rules written the same, by `identical_rules.written`. Each
group's earliest rule is its first, and the rest are its later copies.

  births       every rule, by what bore it, IMPASSE or CONFLICT, and by whether
               it is alone, the first of a group, or a later copy.
  own tie      a later copy whose birth's finalists include an earlier copy of
               its group.
    inside     every finalist is of the group: the group's copies disagree.
    outside    a finalist lies outside the group.
  other's tie  the earlier copies matched and were out-specified: the
               finalists are more specific rules, tied among themselves.
  recurs       after an own-tie birth, a later CONFLICT with a rule of the
               group among the finalists.
  per group    after its first rule's birth, the CONFLICTs with a rule of the
               group among the finalists, how many of them bore a copy of it,
               and the cases the group decided.
  fired        the later copies that ever decided a case.

The figures are counts of births and of corpus cases, as the cases arrived.
They read no truth but the record's labels, which gate 1 needs for the correct
counts and the births report beside each rule.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The replay is the run.** Every case's outcome, winner and count of
     matched rules, every rule's id and birth case, and every rule's fire and
     correct counts are the record's.
  2. **Every rule matches its own case**, as the loop's validation required,
     and no case bore two.
  3. **The groups are §18's**: the groups of rules written the same are the 83
     groups `identical_rules.json` lists, rule for rule.
  4. **A group has one specificity**: the rules of each group carry as many
     conditions as each other.

It refuses to write if any fails.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  1. **Every later copy was born on a CONFLICT.**
  2. **In its own tie.** In at least three quarters of the later copies'
     births, an earlier copy of the group was among the finalists.
  3. **Tied with a rule outside the group.** Of those own-tie births, at least
     half have a finalist outside the group.
  4. **The copy did not end the tie.** Of those own-tie births, at least three
     quarters are followed by another CONFLICT with a rule of the group among
     the finalists.
  5. **No later copy ever decided a case.**

**What the drafter had seen**:
  - `FINDINGS3.md` §18's text: 83 groups of 307 rules written the same; 655
    pairs with one queue and 93 with two, the 93 in 21 groups of 85 rules; and
    the two rules of a pair born a median 595 cases apart. Not
    `identical_rules.json`'s rows: of that record only its keys, for gate 3.
  - Rung 1's record's metrics and fields: 594 escalations on a CONFLICT and 38
    on an IMPASSE, 577 rules, 21 rejected and 34 failed proposals, 486 dead
    rules. And that the record keeps each case's outcome, winner and count of
    matched rules, which for a CONFLICT is the count of finalists, but not
    which rules they were.
  - The code of `harness/dsl.py` and `harness/shadow.py`.
  - The gates, run before this commit, which print pass or fail.

**Not seen**: any rule's specificity, what bore any rule, any finalist, which
births are later copies, and any group's later CONFLICTs.

**What is close to known, and what is bet.** The first and the fifth follow from
the engine and the validation, as the question says; they fail only if the
replay is not the run. **The second is the bet on the question**: that the copies
are the engine's own ties, which the age tie-break never reaches, answered again
by a model that does not see them. The third rests on §18's counts. The 62
groups with one queue hold 160 later copies, and their own ties can only be with
rules outside the group; the 21 groups with two queues hold 64. The fourth bets
that a copy, as specific as the tie it was born in, leaves the tie where it was.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: asked for by `IDEAS.md` since §18 left it on 2026-10-05, with the
expectation above written before the reading and committed before it ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. No verdict
moves. Zero API calls.

--------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN: WHERE EACH RULE STANDS AGAINST THE TIE THAT BORE IT
--------------------------------------------------------------------------
The first run found most later copies born in someone else's tie, below it, and
the second clause failed. `against_the_tie` places every rule born on a
CONFLICT against the finalists of the case that bore it:
  - `above`, more conditions than they have: it alone can decide that case;
  - `at`, as many: it joins the tie;
  - `below`, fewer: it is out-specified on its own case.
Each is split by alone, first and later copy. For the later copies born below
the tie, it gives how many conditions they fall short and whether their queue is
one of those tied. And for each status, how many rules carried the true queue of
the case that bore them.

A decomposition of what the first run read, not a measurement, and no
expectation goes with it. Added in its own commit, after the first run of this
module; the record comes from a second run, which must give back every figure
of the first.

Usage:  PYTHONHASHSEED=0 python3 -m rung3.copy_births
"""

from __future__ import annotations

import json
import sys
import time
from collections import Counter
from pathlib import Path

from harness.domain import generate_corpus
from harness.dsl import RuleEngine, RuleValidationError, validate_rule_payload
from harness.provenance import describe, environment

from rung3.identical_rules import groups, written

OUT = Path("results3")
RECORD = "copy_births.json"
RUN = Path("results/llm_run.json")
IDENTICAL = OUT / "identical_rules.json"
N, SEED = 2000, 17                 # rung 1's corpus, as rung3/order_search.py loads it
OWN_MIN = 0.75                     # clause 2
OUTSIDE_MIN = 0.50                 # clause 3
RECURS_MIN = 0.75                  # clause 4

PROVENANCE = (
    "POST-RUN: asked for by IDEAS.md since FINDINGS3.md §18 left it on 2026-10-05. "
    "The expectation in the module's docstring was written before the reading and "
    "committed before it ran. Not a signed row; no verdict moves. Zero API calls.")


# ---------------------------------------------------------------------------
# The replay
# ---------------------------------------------------------------------------

def replay(record: dict, corpus) -> tuple[RuleEngine, list[dict], list[str]]:
    """Rung 1's loop with its own rules: each case decided by the base as it
    stood, each recorded rule validated against its case and added after it,
    fire and correct counts kept as `run_shadow` keeps them. Returns the engine,
    each case's decision with its finalists, and any rule that failed gate 2."""
    by_case: dict[int, list[dict]] = {}
    for d in record["rules"]:
        by_case.setdefault(d["born_at"], []).append(d)
    engine = RuleEngine()
    cases, problems = [], []
    for idx, case in enumerate(corpus):
        outcome, winner, matched = engine.decide(case)
        if outcome == "ACTION":
            winner.fire_count += 1
            if winner.action == record["records"][idx]["truth"]:
                winner.correct_count += 1
        born = []
        for d in by_case.get(idx, []):
            payload = {"action": d["action"], "conditions": d["conditions"],
                       "note": d.get("note", "")}
            try:
                rule = validate_rule_payload(payload, case=case)
            except RuleValidationError as exc:
                problems.append(f"{d['rule_id']}: {exc}")
                continue
            engine.add(rule, born_at=idx)
            born.append(rule.rule_id)
        if len(born) > 1:
            problems.append(f"case {idx} bore {born}")
        cases.append({"idx": idx, "outcome": outcome,
                      "winner": winner.rule_id if winner else None,
                      "n_matched": len(matched),
                      "finalists": ([r.rule_id for r in matched] if outcome == "CONFLICT"
                                    else []),
                      "born": born[0] if born else None})
    return engine, cases, problems


def same_as_record(record: dict, engine: RuleEngine, cases: list[dict]) -> dict:
    """Gate 1: the replay against the record, case by case and rule by rule."""
    recs = record["records"]
    off_cases = [c["idx"] for c, r in zip(cases, recs)
                 if (c["outcome"], c["winner"], c["n_matched"])
                 != (r["outcome"], r["winner_id"], r["n_matched"])]
    mine = [(r.rule_id, r.born_at, r.fire_count, r.correct_count) for r in engine.rules]
    theirs = [(d["rule_id"], d["born_at"], d["fire_count"], d["correct_count"])
              for d in record["rules"]]
    return {"cases_off": off_cases[:20], "n_cases_off": len(off_cases),
            "rules_same": mine == theirs,
            "passes": len(cases) == len(recs) and not off_cases and mine == theirs}


# ---------------------------------------------------------------------------
# What bore each rule
# ---------------------------------------------------------------------------

def group_index(gs: list[list[str]]) -> dict[str, int]:
    return {rid: i for i, g in enumerate(gs) for rid in g}


def classify(rule: str, case: dict, members: list[str], born_at: dict[str, int]) -> dict:
    """A later copy's birth, against its group: whether an earlier copy was a
    finalist, and if so whether a finalist lay outside the group."""
    earlier = [m for m in members if born_at[m] < born_at[rule]]
    fin = set(case["finalists"])
    own = any(m in fin for m in earlier)
    return {"own": own,
            "outside": (any(f not in set(members) for f in fin) if own else None)}


def recurs(after: list[dict], members: set[str]) -> bool:
    """A later CONFLICT with a rule of the group among the finalists."""
    return any(c["outcome"] == "CONFLICT" and members & set(c["finalists"]) for c in after)


def births(record: dict, cases: list[dict], gs: list[list[str]],
           spec: dict[str, int]) -> list[dict]:
    """Every rule, by what bore it and by its group, in the order born."""
    action = {d["rule_id"]: d["action"] for d in record["rules"]}
    born_at = {d["rule_id"]: d["born_at"] for d in record["rules"]}
    truth = [r["truth"] for r in record["records"]]
    index = group_index(gs)
    out = []
    for d in record["rules"]:
        rid, c = d["rule_id"], cases[d["born_at"]]
        g = index.get(rid)
        status = "alone" if g is None else "first" if gs[g][0] == rid else "later"
        row = {"rule": rid, "case": c["idx"], "trigger": c["outcome"], "status": status,
               "group": g, "queue": action[rid], "specificity": spec[rid],
               "queue_was_true": action[rid] == truth[c["idx"]]}
        if c["outcome"] == "CONFLICT":
            row["finalists"] = [[f, action[f], spec[f]] for f in c["finalists"]]
        if status == "later":
            row |= classify(rid, c, gs[g], born_at)
            row["recurs"] = (recurs(cases[c["idx"] + 1:], set(gs[g]))
                             if row["own"] else None)
        out.append(row)
    return out


def per_group(gs: list[list[str]], cases: list[dict], record: dict,
              spec: dict[str, int]) -> list[dict]:
    """Each group after its first rule's birth: its CONFLICTs, what they bore,
    and the cases it decided."""
    action = {d["rule_id"]: d["action"] for d in record["rules"]}
    born_at = {d["rule_id"]: d["born_at"] for d in record["rules"]}
    out = []
    for i, g in enumerate(gs):
        s = set(g)
        after = [c for c in cases if c["idx"] > born_at[g[0]]]
        conflicts = [c for c in after if c["outcome"] == "CONFLICT" and s & set(c["finalists"])]
        out.append({
            "group": i, "rules": g, "queues": sorted({action[r] for r in g}),
            "specificity": spec[g[0]],
            "conflicts": len(conflicts),
            "bore_a_copy": sum(c["born"] in s for c in conflicts),
            "bore_another_rule": sum(c["born"] is not None and c["born"] not in s
                                     for c in conflicts),
            "bore_nothing": sum(c["born"] is None for c in conflicts),
            "decided": sum(c["outcome"] == "ACTION" and c["winner"] in s for c in after),
        })
    return out


def summary(rows: list[dict], engine: RuleEngine) -> dict:
    later = [r for r in rows if r["status"] == "later"]
    own = [r for r in later if r["own"]]
    fired = {r.rule_id: r.fire_count for r in engine.rules}
    return {
        "births": {f"{t} {s}": n for (t, s), n in
                   sorted(Counter((r["trigger"], r["status"]) for r in rows).items())},
        "later_copies": len(later),
        "on_a_conflict": sum(r["trigger"] == "CONFLICT" for r in later),
        "own_tie": len(own),
        "own_tie_outside": sum(r["outside"] for r in own),
        "own_tie_inside": sum(not r["outside"] for r in own),
        "others_tie": len(later) - len(own),
        "own_tie_recurs": sum(r["recurs"] for r in own),
        "later_copies_that_fired": sum(fired[r["rule"]] > 0 for r in later),
        "dead_rules": sum(f == 0 for f in fired.values()),
        "dead_later_copies": sum(fired[r["rule"]] == 0 for r in later),
    }


# ---------------------------------------------------------------------------
# Added after the first run: where each rule stands against the tie
# ---------------------------------------------------------------------------

def place(row: dict) -> str | None:
    """A rule born on a CONFLICT against the finalists that bore it: above,
    at or below their specificity."""
    if row["trigger"] != "CONFLICT":
        return None
    top = max(f[2] for f in row["finalists"])
    return ("above" if row["specificity"] > top else
            "at" if row["specificity"] == top else "below")


def against_the_tie(rows: list[dict]) -> dict:
    conflict = [r for r in rows if r["trigger"] == "CONFLICT"]
    below_copies = [r for r in conflict if r["status"] == "later" and place(r) == "below"]
    gaps = Counter(max(f[2] for f in r["finalists"]) - r["specificity"] for r in below_copies)
    return {
        "born_on_a_conflict": len(conflict),
        "by_place": {p: sum(place(r) == p for r in conflict) for p in ("above", "at", "below")},
        "by_status_and_place": {
            s: {p: sum(r["status"] == s and place(r) == p for r in conflict)
                for p in ("above", "at", "below")}
            for s in ("alone", "first", "later")},
        "later_copies_below": {
            "rules": len(below_copies),
            "conditions_short": {str(k): gaps[k] for k in sorted(gaps)},
            "their_queue_is_a_tied_queue": sum(
                r["queue"] in {f[1] for f in r["finalists"]} for r in below_copies)},
        "queue_true_at_birth": {
            s: [sum(r["queue_was_true"] for r in rows if r["status"] == s),
                sum(r["status"] == s for r in rows)]
            for s in ("alone", "first", "later")},
    }


# ---------------------------------------------------------------------------
# The gates and the expectation
# ---------------------------------------------------------------------------

def check(record: dict, engine: RuleEngine, cases: list[dict], problems: list[str],
          gs: list[list[str]], published: list[list[str]], spec: dict[str, int]) -> list[dict]:
    g1 = same_as_record(record, engine, cases)
    return [
        {"gate": 1, "what": "the replay is the run", "measured": g1, "passes": g1["passes"]},
        {"gate": 2, "what": "every rule matches its own case, and no case bore two",
         "problems": problems, "passes": not problems},
        {"gate": 3, "what": "the groups are §18's",
         "measured": len(gs), "published": len(published),
         "passes": sorted(map(sorted, gs)) == sorted(map(sorted, published))},
        {"gate": 4, "what": "a group has one specificity",
         "passes": all(len({spec[r] for r in g}) == 1 for g in gs)},
    ]


def share(part: int, whole: int) -> float | None:
    return part / whole if whole else None


def read_expectation(s: dict) -> list[dict]:
    own = share(s["own_tie"], s["later_copies"])
    outside = share(s["own_tie_outside"], s["own_tie"])
    again = share(s["own_tie_recurs"], s["own_tie"])
    return [
        {"clause": 1, "what": "every later copy was born on a CONFLICT",
         "reading": [s["on_a_conflict"], s["later_copies"]],
         "holds": s["on_a_conflict"] == s["later_copies"]},
        {"clause": 2, "what": "in at least three quarters of the later copies' births an "
                              "earlier copy was among the finalists",
         "reading": own, "holds": None if own is None else own >= OWN_MIN},
        {"clause": 3, "what": "of those own-tie births, at least half have a finalist "
                              "outside the group",
         "reading": outside, "holds": None if outside is None else outside >= OUTSIDE_MIN},
        {"clause": 4, "what": "of those own-tie births, at least three quarters are "
                              "followed by another CONFLICT with a rule of the group "
                              "among the finalists",
         "reading": again, "holds": None if again is None else again >= RECURS_MIN},
        {"clause": 5, "what": "no later copy ever decided a case",
         "reading": s["later_copies_that_fired"], "holds": s["later_copies_that_fired"] == 0},
    ]


def measure() -> tuple[dict, list[dict]]:
    t = time.time()
    record = json.loads(RUN.read_text())
    corpus = generate_corpus(N, seed=SEED)
    engine, cases, problems = replay(record, corpus)
    spec = {r.rule_id: r.specificity for r in engine.rules}
    gs = groups({d["rule_id"]: written(d["conditions"]) for d in record["rules"]})
    published = json.loads(IDENTICAL.read_text())["written"]["groups_listed"]
    gates = check(record, engine, cases, problems, gs, published, spec)
    rows = births(record, cases, gs, spec)
    s = summary(rows, engine)
    payload = {
        "_env": environment(),
        "what": "why rung 1's loop wrote the same rule again: what bore each of its 577 "
                "rules, and for each later copy whether an earlier copy of it was among "
                "the finalists of the CONFLICT that bore it. Zero API calls.",
        "provenance": PROVENANCE,
        "base": str(RUN),
        "surface": "the 2,000 cases of seed 17, in the order rung 1's loop met them",
        "groups_from": str(IDENTICAL),
        "constants": {"OWN_MIN": OWN_MIN, "OUTSIDE_MIN": OUTSIDE_MIN,
                      "RECURS_MIN": RECURS_MIN},
        "gates": gates,
        "summary": s,
        "births": rows,
        "groups": per_group(gs, cases, record, spec),
        "expectation": read_expectation(s),
        "seconds": round(time.time() - t, 1),
        "added_after_the_first_run": {
            "what": "every rule born on a CONFLICT placed against the finalists that bore "
                    "it, above, at or below their specificity, by status; the later "
                    "copies born below, by how many conditions short and whether their "
                    "queue is a tied one; and each status's rules that carried the true "
                    "queue of their case. A decomposition of what the first run read, "
                    "with no expectation",
            "against_the_tie": against_the_tie(rows)},
    }
    return payload, gates


def main(argv: list[str] | None = None) -> int:
    if argv:
        print(__doc__)
        return 2
    payload, gates = measure()
    print("=" * 78)
    print("WHY RUNG 1'S LOOP WROTE THE SAME RULE AGAIN")
    print("=" * 78)
    print(f"  {describe()}")
    for g in gates:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
    if not all(g["passes"] for g in gates):
        print("\nREFUSED: a gate failed; nothing was written.")
        return 1
    s = payload["summary"]
    print(f"\n  births: {s['births']}")
    print(f"  later copies: {s['later_copies']}, on a CONFLICT {s['on_a_conflict']}")
    print(f"    own tie {s['own_tie']} (outside {s['own_tie_outside']}, inside "
          f"{s['own_tie_inside']}), other's tie {s['others_tie']}")
    print(f"    own tie that recurs: {s['own_tie_recurs']}")
    print(f"    later copies that ever decided a case: {s['later_copies_that_fired']}")
    print(f"  dead rules {s['dead_rules']}, of them later copies {s['dead_later_copies']}")
    a = payload["added_after_the_first_run"]["against_the_tie"]
    print(f"  born on a CONFLICT {a['born_on_a_conflict']}, against the tie {a['by_place']}")
    print(f"    by status {a['by_status_and_place']}")
    print(f"    later copies below {a['later_copies_below']}")
    print(f"    queue true at birth {a['queue_true_at_birth']}")
    for c in payload["expectation"]:
        print(f"  clause {c['clause']}: {c['reading']}  "
              f"{'held' if c['holds'] else 'FAILED' if c['holds'] is False else 'no reading'}")
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2) + "\n")
    print(f"\n  {payload['seconds']:.0f}s, zero API calls\n-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
