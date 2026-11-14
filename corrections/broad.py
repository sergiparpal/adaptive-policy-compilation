"""
WHY THE FIRST CALL WRITES BROAD CORRECTIONS.
`corrections/forgotten.py` found it. Of the 510 corrections born at a report in
the three L runs, 248 left their own ticket wrong just after the birth. In 210 of
those a rule nested inside the correction beat it there by containment, and the
corrections that lose are the broad ones. `FINDINGS_CORRECTIONS.md`, *Why the
final base forgets its corrections*, *What it does not settle*, item 1, carries
the question: why the first call drafts a correction broader than the rule that
erred. Asked for by Sergi on 2026-11-14, after that reading. Free on the
records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
Every first call of the six runs is read: its draft's queue, its conditions,
its points of the space, the rule it duplicates if any, and its reasoning. A
draft is *valid* when its payload carries a list of conditions that builds a
region. It is *broad* with one or two conditions, and *narrow* with three or
more. Four readings:

1. **With and without the report, on the same ticket.** Both arms of run k read
   the draws of stream r`k`, and the first call is blind. So a case that both
   arms' bases decided wrongly, and the channel reported, was asked of both
   arms' first calls in messages that differ by the report alone (`CR-g1`). Of
   such a pair of valid drafts, which is broader in points of the space.
2. **The losing correction, against the base.** For every correction born at a
   report of an L run, read by `corrections/forgotten.py`, it reads whether its
   region is one the base already held. A *duplicate* is a correction whose
   region equals that of a rule of the same queue in the base when it was
   drafted. It also reads whether the correction left its ticket right.
3. **The correction written most often.** For each L run, the born correction
   written at the most reports, by its conditions and queue.
4. **What the reasoning says**, by a codebook of two codes frozen on the
   development set, below.

--------------------------------------------------------------------------
THE DEVELOPMENT SET, AND THE CODEBOOK FROZEN ON IT
--------------------------------------------------------------------------
**Run 1 of each arm is the development set.** Every clause reads runs 2 and 3.
What the drafter read of run 1, before writing anything below:
- **the pairs.** 91 tickets were reported in both L r1 and N r1, and 86 gave two
  valid drafts. L's was broader in 33, N's in 50, and they were equal in 3. N's
  draft named the label's queue in 6 of the 86;
- **the drafts' conditions** at L r1's reported errors, impasses and conflicts;
- **the losing corrections.** The born corrections L r1 left wrong were 80. 42
  of them duplicate a rule of the same queue, against 3 of the 83 left right.
  The most written was `product = billing -> BILLING_SPECIALIST`, born 17 times
  and never right. Each rule of another queue nested inside a losing
  correction, 101 in all, was left out of the round as inside the draft;
- **three reasonings read whole** of one-condition corrections of billing, and
  the counts of the candidate codes below by arm and breadth.

Each code is one anchored pattern, matched case-blind on a first call's
reasoning:
  DEFER  the reasoning takes up that overlapping rules are listed after the
         draft: "se te listaran", "listaran", "will be listed", "listed after",
         "nos mostraran", "will show", "after seeing the conflicts";
  ANY    it writes the rule for any ticket of a kind: "any", "all", "every",
         "cualquier", "todos los" or "todas las" within 30 characters of a
         ticket or a case.

**Their counts on run 1**, among first calls at reported errors whose draft is
valid, as broad / narrow, are `DEVELOPMENT`, which gate 4 recomputes:

              L r1           N r1
  drafts      76 / 133       105 / 204
  DEFER       64 / 119       91 / 166
  ANY         44 / 48        67 / 54

**Codes tried on run 1 and dropped**, because they told broad from narrow by
little or not at all:
- the catalogue's words for the queue, and the manual, in nearly every
  reasoning of both arms;
- that the more specific rules win by containment, about one in six in L;
- simple, too broad, too specific, and an existing rule that misrouted the
  ticket.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The corrections are `forgotten.py`'s.** Its five gates pass in every L
     run, and its reading of each born report is the one read here.
  2. **The pairs share their draws.** Each run's L and N records carry the same
     draws digest.
  3. **The round left the nested rules out.** In every L run, each rule of
     another queue nested inside a losing correction is in that first call's
     left-out rules as inside the draft, and was not listed.
  4. **The codebook gives `DEVELOPMENT`'s counts on run 1.**

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates, prints pass or fail,
and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads runs 2 and 3. B1 to B5 pool them, and B6 reads each L run.

  B1. **The report does not widen the draft.** Among the pairs of valid drafts
      on the same ticket that differ in points, L's is the broader in at most
      half.
  B2. **The losing correction was already in the base.** Of the corrections born
      at a report and left wrong just after the birth, at least two fifths
      duplicate a rule of the same queue.
  B3. **A duplicate does not take its ticket.** Of the born corrections that
      duplicate a rule of the same queue, at most a fifth left their ticket
      right.
  B4. **The first call leaves the overlaps to the round.** `DEFER` is in at
      least three quarters of L's first calls at reported errors whose draft is
      valid.
  B5. **A broad correction is written for any ticket of its kind.** Among L's
      first calls at reported errors, `ANY`'s share among the broad drafts is
      at least 0.15 above its share among the narrow ones.
  B6. **One correction is written again and again.** In each L run, the born
      correction written at the most reports has one or two conditions, and
      was born at five reports or more.

A share over nothing has no value, and a clause that reads one fails.

**The drafter's account**, from run 1.
- **The first call writes the queue's general rule.** The system prompt asks
  every call for "UNA regla generalizable" for the ticket and its analogous
  cases. The catalogue gives each queue a general line. Told the true queue,
  the first call writes that line as a rule: billing tickets to
  `BILLING_SPECIALIST`.
- **The report does not make it broader.** Without the report, on the same
  ticket, the first call writes as broad a draft or broader.
- **The base already holds that rule.** The correction duplicates it, so it
  adds nothing. The rule that erred is narrower, of another queue, and inside
  it.
- **The first call cannot see that rule, and does not expect to.** It is blind,
  and expects the round to list the overlapping rules, as v2b's paragraph says.
  It says the more specific rules will win by containment, as the system prompt
  says. v1c's round lists no rule nested inside the draft, so the narrow wrong
  rule is never shown, and keeps the ticket.

**The bet is B2.** **B4 is trusted most**, at 0.88 on run 1. **B1 is trusted
least**: a pair is one ask of each arm, and the first call's breadth changes
from ask to ask.

**What the drafter had seen**, beyond run 1:
- `FINDINGS_CORRECTIONS.md` whole, with its section *Why the final base forgets
  its corrections*;
- `forgotten.json`'s tables for all three L runs: each run's born reports by
  conditions and their regions' lower medians; its nested reports with their
  erring rules' causes; its last losses;
- the field names of a first call's row, its `left_out` and `copy_of`.

**What the drafter had not seen** of runs 2 and 3: any first call's draft,
queue or reasoning, any pair, any duplicate, the correction written most often,
or any round's left-out rules.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-14, after `corrections/forgotten.py`.
The codebook and the expectation above were written and committed before the
reading ran on runs 2 and 3. Not a signed row, not on `STATUS.md`'s scoreboard,
not a calibration event. Zero API calls.

Usage:  python3 -m corrections.broad --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.broad
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

from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import Condition, Space

from . import forgotten as fg
from . import plan

F = Fraction

DEVELOPMENT_REP = 1                    # run 1 of each arm
HELD_OUT = (2, 3)
BROAD_MOST = 2                         # a broad draft has at most two conditions

CODES = {
    "DEFER": re.compile(
        r"se te listar|listar[aá]n|will be listed|be listed|listed (?:later|after)"
        r"|nos mostrar[aá]n|se nos mostrar|will (?:be )?show|then the system will"
        r"|after seeing (?:the )?conflicts|placement round|se mostrar[aá]n", re.I),
    "ANY": re.compile(
        r"\b(?:any|all|every|cualquier|todos los|todas las)\b[^.]{0,30}"
        r"\b(?:ticket|tickets|caso|casos)\b", re.I),
}

# The codes' counts on run 1, among first calls at reported errors whose draft
# is valid; gate 4 recomputes them.
DEVELOPMENT = {
    "l": {"broad": {"drafts": 76, "DEFER": 64, "ANY": 44},
          "narrow": {"drafts": 133, "DEFER": 119, "ANY": 48}},
    "n": {"broad": {"drafts": 105, "DEFER": 91, "ANY": 67},
          "narrow": {"drafts": 204, "DEFER": 166, "ANY": 54}},
}

# The expectation's lines.
B1_SHARE = F(1, 2)
B2_SHARE = F(2, 5)
B3_SHARE = F(1, 5)
B4_SHARE = F(3, 4)
B5_GAP = F(3, 20)
B6_TIMES = 5

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-14, after corrections/forgotten.py. The "
    "codebook and the expectation in the module's docstring were written and committed "
    "before the reading ran on runs 2 and 3. Not a signed row; no verdict moves.")


def record_path():
    return plan.OUT / "broad.json"


def share(part: int, whole: int) -> Fraction | None:
    return F(part, whole) if whole else None


def frac(x: Fraction | None) -> dict[str, Any] | None:
    return None if x is None else {"fraction": str(x), "value": float(x)}


# ---------------------------------------------------------------------------
# A first call, read
# ---------------------------------------------------------------------------

def region(payload: Any, space: Space) -> int | None:
    """The points of the space a draft covers, or None if it builds no region."""
    if not isinstance(payload, dict) or not isinstance(payload.get("conditions"), list) \
            or not payload["conditions"]:
        return None
    try:
        return space.extension([Condition(**c) for c in payload["conditions"]])
    except (TypeError, ValueError, KeyError):
        return None


def codes(reasoning: str | None) -> dict[str, bool]:
    return {k: bool(p.search(reasoning or "")) for k, p in CODES.items()}


def first_calls(record: dict[str, Any], space: Space) -> dict[int, dict[str, Any]]:
    """Every escalation's first call, by its case: its cause and verdict, its
    draft's queue, conditions and points, and its reasoning's codes."""
    out = {}
    for esc in record["escalations"]:
        calls = esc.get("calls") or []
        if not calls:
            continue
        call = calls[0]
        payload = call.get("payload")
        ext = region(payload, space)
        out[esc["idx"]] = {
            "idx": esc["idx"], "cause": esc["kind"], "verdict": esc["verdict"],
            "valid": ext is not None,
            "action": payload.get("action") if isinstance(payload, dict) else None,
            "conditions": len(payload["conditions"]) if ext is not None else None,
            "points": ext.bit_count() if ext is not None else None,
            "codes": codes(call.get("reasoning")),
        }
    return out


def breadth(n_conditions: int) -> str:
    return "broad" if n_conditions <= BROAD_MOST else "narrow"


def code_counts(calls: dict[int, dict[str, Any]], cause: str) -> dict[str, dict[str, int]]:
    """Among first calls of `cause` whose draft is valid, by breadth: how many,
    and how many carry each code."""
    out = {b: {"drafts": 0, **{k: 0 for k in CODES}} for b in ("broad", "narrow")}
    for c in calls.values():
        if c["cause"] != cause or not c["valid"]:
            continue
        row = out[breadth(c["conditions"])]
        row["drafts"] += 1
        for k in CODES:
            row[k] += c["codes"][k]
    return out


# ---------------------------------------------------------------------------
# The pairs
# ---------------------------------------------------------------------------

def pairs(l_calls: dict[int, dict[str, Any]], n_calls: dict[int, dict[str, Any]]
          ) -> dict[str, Any]:
    """The cases reported in both arms, and of their valid pairs which draft is
    broader in points, overall and where both name the same queue."""
    both = sorted(i for i in set(l_calls) & set(n_calls)
                  if l_calls[i]["cause"] == n_calls[i]["cause"] == plan.ERROR)
    out = {"reported_in_both": len(both), "valid_pairs": 0,
           "l_broader": 0, "n_broader": 0, "equal": 0,
           "same_queue": {"pairs": 0, "l_broader": 0, "n_broader": 0, "equal": 0}}
    for i in both:
        a, b = l_calls[i], n_calls[i]
        if not (a["valid"] and b["valid"]):
            continue
        out["valid_pairs"] += 1
        k = "l_broader" if a["points"] > b["points"] else (
            "n_broader" if b["points"] > a["points"] else "equal")
        out[k] += 1
        if a["action"] == b["action"]:
            out["same_queue"]["pairs"] += 1
            out["same_queue"][k] += 1
    return out


# ---------------------------------------------------------------------------
# The corrections born at a report
# ---------------------------------------------------------------------------

def signature(rule: dict[str, Any]) -> str:
    conds = sorted(rule["conditions"], key=lambda c: (c["attr"], c["op"], str(c["value"])))
    return " & ".join(f"{c['attr']} {c['op']} {c['value']}" for c in conds) + \
        f" -> {rule['action']}"


def corrections(record: dict[str, Any], run: dict[str, Any]) -> dict[str, Any]:
    """Every correction born at a report, as `forgotten.py` read it right after
    its birth, against the base it was drafted over: whether it duplicates a
    rule of the same queue, and the one written most often."""
    rules = {r["rule_id"]: r for r in record["rules"]}
    escs = fg.escalation_at(record)
    born = [b for x in run["points"] for b in x["at_born_reports"]]
    rows = []
    for b in born:
        copy = escs[b["report"]].get("copy_of")
        rule = rules[b["rule_id"]]
        rows.append({"report": b["report"], "rule_id": b["rule_id"], "right": b["right"],
                     "why": b["why"], "conditions": len(rule["conditions"]),
                     "duplicate": copy is not None and rules[copy]["action"] == rule["action"],
                     "copy_of": copy, "signature": signature(rule)})
    lost = [r for r in rows if not r["right"]]
    dups = [r for r in rows if r["duplicate"]]
    most = Counter(r["signature"] for r in rows).most_common(1)
    top = None
    if most:
        sig, times = most[0]
        mine = [r for r in rows if r["signature"] == sig]
        top = {"signature": sig, "born_at_reports": times, "conditions": mine[0]["conditions"],
               "right": sum(1 for r in mine if r["right"])}
    return {"born": len(rows), "left_wrong": len(lost),
            "left_wrong_duplicates": sum(1 for r in lost if r["duplicate"]),
            "duplicates": len(dups), "duplicates_right": sum(1 for r in dups if r["right"]),
            "most_written": top, "rows": rows}


def nested_left_out(record: dict[str, Any], run: dict[str, Any]) -> dict[str, int]:
    """Gate 3: each rule of another queue nested inside a losing correction, and
    whether its first call left it out as inside the draft, or listed it."""
    rules = {r["rule_id"]: r for r in record["rules"]}
    escs = fg.escalation_at(record)
    out = Counter()
    for x in run["points"]:
        for b in x["at_born_reports"]:
            if b["why"] != fg.NESTED:
                continue
            esc = escs[b["report"]]
            left = (esc["calls"][0].get("left_out") or {})
            listed = set(esc.get("listed") or [])
            mine = rules[b["rule_id"]]["action"]
            for n in b["nested"]:
                if rules[n]["action"] == mine:
                    continue
                out["listed" if n in listed else f"left_out:{left.get(n)}"] += 1
    return dict(out)


# ---------------------------------------------------------------------------
# Every run, read
# ---------------------------------------------------------------------------

def read_all_runs(records: dict[str, dict], score: dict[str, Any], corpus: Sequence,
                  space: Space, forgotten_runs: dict[str, dict] | None = None
                  ) -> dict[str, Any]:
    """The six runs read, and the four gates. `forgotten_runs` is
    `forgotten.read_run`'s reading of each L run, computed here by default."""
    fr = forgotten_runs if forgotten_runs is not None else {
        plan.tag(plan.LABELLED, k): fg.read_run(records[plan.tag(plan.LABELLED, k)], corpus,
                                                 space, fg.stage_c_of(score,
                                                                      plan.tag(plan.LABELLED, k)))
        for k in range(1, plan.REPS + 1)}
    calls = {t: first_calls(rec, space) for t, rec in records.items()}
    runs: dict[str, Any] = {}
    gates_ok = {1: True, 2: True, 3: True}
    for k in range(1, plan.REPS + 1):
        lt, nt = plan.tag(plan.LABELLED, k), plan.tag("n", k)
        gates_ok[1] &= all(g["passes"] for g in fr[lt]["gates"])
        gates_ok[2] &= records[lt].get("draws_sha16") == records[nt].get("draws_sha16")
        left = nested_left_out(records[lt], fr[lt])
        gates_ok[3] &= set(left) <= {"left_out:inside"}
        runs[f"r{k}"] = {
            "pairs": pairs(calls[lt], calls[nt]),
            "corrections": corrections(records[lt], fr[lt]),
            "nested_left_out": left,
            "codes": {"l": code_counts(calls[lt], plan.ERROR),
                      "n": code_counts(calls[nt], plan.ERROR)},
            "conditions_by_cause": {
                arm: {cause: dict(sorted(Counter(
                    c["conditions"] for c in calls[t].values()
                    if c["cause"] == cause and c["valid"]).items()))
                    for cause in (plan.ERROR, plan.IMPASSE, plan.CONFLICT)}
                for arm, t in (("l", lt), ("n", nt))},
        }
    dev = runs[f"r{DEVELOPMENT_REP}"]["codes"]
    dev_ok = {a: {b: {k: dev[a][b][k] for k in ("drafts", *CODES)} for b in ("broad", "narrow")}
              for a in ("l", "n")} == DEVELOPMENT
    gates = [
        {"gate": 1, "what": "the corrections are forgotten.py's, its gates passing",
         "passes": gates_ok[1]},
        {"gate": 2, "what": "the pairs share their draws", "passes": gates_ok[2]},
        {"gate": 3, "what": "the round left the nested rules of another queue out as inside",
         "passes": gates_ok[3]},
        {"gate": 4, "what": "the codebook gives DEVELOPMENT's counts on run 1",
         "passes": dev_ok},
    ]
    return {"runs": runs, "gates": gates}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(runs: dict[str, Any]) -> list[dict[str, Any]]:
    held = [runs[f"r{k}"] for k in HELD_OUT]
    lb = sum(r["pairs"]["l_broader"] for r in held)
    nb = sum(r["pairs"]["n_broader"] for r in held)
    lw = sum(r["corrections"]["left_wrong"] for r in held)
    lwd = sum(r["corrections"]["left_wrong_duplicates"] for r in held)
    d = sum(r["corrections"]["duplicates"] for r in held)
    dr = sum(r["corrections"]["duplicates_right"] for r in held)
    cl = {b: {k: sum(r["codes"]["l"][b][k] for r in held) for k in ("drafts", *CODES)}
          for b in ("broad", "narrow")}
    drafts = cl["broad"]["drafts"] + cl["narrow"]["drafts"]
    defer = cl["broad"]["DEFER"] + cl["narrow"]["DEFER"]
    any_b = share(cl["broad"]["ANY"], cl["broad"]["drafts"])
    any_n = share(cl["narrow"]["ANY"], cl["narrow"]["drafts"])
    tops = {f"l_r{k}": runs[f"r{k}"]["corrections"]["most_written"] for k in HELD_OUT}
    return [
        {"clause": "B1", "what": "among differing pairs on the same ticket, L's draft is the "
                                 "broader in at most half",
         "reading": {"l_broader": lb, "of_differing": lb + nb,
                     "share": frac(share(lb, lb + nb))},
         "holds": lb + nb > 0 and F(lb, lb + nb) <= B1_SHARE},
        {"clause": "B2", "what": "at least two fifths of the corrections left wrong duplicate "
                                 "a rule of the same queue",
         "reading": {"duplicates": lwd, "of_left_wrong": lw, "share": frac(share(lwd, lw))},
         "holds": lw > 0 and F(lwd, lw) >= B2_SHARE},
        {"clause": "B3", "what": "at most a fifth of the duplicates left their ticket right",
         "reading": {"right": dr, "of_duplicates": d, "share": frac(share(dr, d))},
         "holds": d > 0 and F(dr, d) <= B3_SHARE},
        {"clause": "B4", "what": "DEFER in at least three quarters of L's first calls at "
                                 "reported errors with a valid draft",
         "reading": {"defer": defer, "of": drafts, "share": frac(share(defer, drafts))},
         "holds": drafts > 0 and F(defer, drafts) >= B4_SHARE},
        {"clause": "B5", "what": "ANY's share among the broad drafts at least 0.15 above its "
                                 "share among the narrow ones",
         "reading": {"broad": frac(any_b), "narrow": frac(any_n),
                     "gap": frac(None if any_b is None or any_n is None else any_b - any_n)},
         "holds": any_b is not None and any_n is not None and any_b - any_n >= B5_GAP},
        {"clause": "B6", "what": "in each L run the correction born at the most reports has "
                                 "one or two conditions and five births or more",
         "reading": tops,
         "holds": all(t is not None and t["conditions"] <= BROAD_MOST
                      and t["born_at_reports"] >= B6_TIMES for t in tops.values())},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {plan.tag(arm, k): json.loads(plan.run_path(arm, k).read_text())
               for arm in plan.ARMS for k in range(1, plan.REPS + 1)}
    return records, json.loads(plan.score_path().read_text())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why the first call writes broad corrections "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 4 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/broad.py writes {record_path()}")
    records, score = read_all()
    got = read_all_runs(records, score, list(MI.corpus()), MI.space())
    for g in got["gates"]:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
    if not all(g["passes"] for g in got["gates"]):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    expectation = read_expectation(got["runs"])
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"score": str(plan.score_path()),
                   "score_from": score["_env"].get("git_commit")},
        "surface": "the first calls of the six runs, and the corrections born at a "
                   "report of each L run",
        "development": {"rep": DEVELOPMENT_REP, "held_out": list(HELD_OUT),
                        "counts": DEVELOPMENT,
                        "codes": {k: p.pattern for k, p in CODES.items()}},
        "constants": {"BROAD_MOST": BROAD_MOST, "B1_SHARE": str(B1_SHARE),
                      "B2_SHARE": str(B2_SHARE), "B3_SHARE": str(B3_SHARE),
                      "B4_SHARE": str(B4_SHARE), "B5_GAP": str(B5_GAP),
                      "B6_TIMES": B6_TIMES},
        "gates": got["gates"],
        "runs": got["runs"],
        "expectation": expectation,
    }), indent=2, default=str) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
