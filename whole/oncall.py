"""
WHY v1d CUT AT THE RAREST QUEUE'S TICKETS.
Stage C found it. At the tickets of `ONCALL_ESCALATION`, v1d's first call cut its
governing rule's region at 6 of its 8 drafts, against v1c's 3 of 7, though T1
asks for that region whole (`WR-a`, `WR-b` and `WR-f` refuted).
`FINDINGS_WHOLE.md`, *What Stage C does not settle*, item 1, and `IDEAS.md` carry
the question. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
For every first call on a ticket of the queue, in all six runs:
- **what it cut its part by**, by `placement/oncall.py`'s reading, called and not
  copied. That is the listed rules the ticket matches, in the list's order, and
  the first of them after the governing rule a cut by would change. It also
  gives the listed rules whose region, cut by the governing rule's region, is
  the draft exactly. Beside them are the conditions the draft adds to its
  governing rule's.
- **its note whole**, the identifiers it cites, and its sides;
- **its reasoning, read by a codebook of anchored patterns** frozen on the smoke
  run's first calls before any reasoning of the six runs was read (below);
- **the placement round that followed**, if any: the rules of the base it was
  listed, the rules the answer left without a side, and its sides and note.

--------------------------------------------------------------------------
THE CODEBOOK, FROZEN ON THE SMOKE RUN
--------------------------------------------------------------------------
The reasoning is long, from 7,680 to 35,500 characters in the smoke run's
first calls, in Spanish with English passages. It walks the list rule by rule,
quotes the prompt's texts, and composes the answer at its end. Each code is a
set of anchored patterns, matched case-blind:

  T1      the reasoning quotes T1's instruction: "region entera" or "anadas
          condiciones", accented or not;
  T1e     it says it in English: a whole, entire or full region, or that it
          should or must not add conditions;
  INSIDE  the note says the draft lies inside another rule: a particular case,
          contained, inside, a subset, an intersection.

**On the smoke run's 14 first calls**, all under v1d: T1 in 6, T1e in 1, either
in 6, and INSIDE in 7 notes. They are `DEVELOPMENT`, and gate 5 recomputes them.

**Three codes were tried there and dropped, because nothing told them apart.**
- **Level 1.** "Nivel 1", "level 1" or a particular case is in 13 of the 14
  reasonings.
- **The governing rule.** Its identifier is in all 14.
- **The first rule a cut by would change.** At the 6 tickets that have one, its
  identifier stands within 300 characters of a containment word in all 6.

The reasoning names every rule and argues containment about all of them, so
only whether it engages T1 sets one call apart from another. T1 is never in the
last 1,500 characters, where the answer is composed: 0 of 14.

So, **for each call, beside its codes**, the record keeps two things:
- the 700 characters that follow each of up to three quotes of T1, where the
  reasoning reads it;
- the last 1,500 characters, where the answer is composed.

A reader can check every code against the text.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. every escalation on a ticket of the queue is governed by `H04` or `H05`;
  2. each such ticket lies first in its governing rule's region;
  3. each such first call's governing rule, class and verdict are Stage C's
     (`score.json`'s `first_drafts`);
  4. every such first call keeps its reasoning and its payload;
  5. the codebook gives `DEVELOPMENT`'s counts on the smoke run's first calls.

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads the first calls on tickets of the queue, in all six runs. A
*cut* is a draft Stage C classes as a cut, by one listed rule or by two.

  Q1. **The cuts are `PLAN_PLACEMENT.md`'s.** Every v1d cut is its governing
      rule's region cut by the first lower listed rule the ticket matches that
      a cut by would change.
  Q2. **Both arms cut alike.** At every ticket where both arms' first calls
      cut, every cut there is by the same rules.
  Q3. **The cuts skipped T1.** In at least four of v1d's six cuts, the reasoning
      neither quotes T1 nor says it in English.
  Q4. **The whole drafts read it.** In both of v1d's whole drafts on tickets of
      the queue, the reasoning quotes T1 or says it in English.
  Q5. **The notes say containment.** At least half of the cuts, over both arms,
      carry a note that says the draft lies inside another rule.

**The drafter's account.** At these tickets the cut is the loop's default, as
`PLAN_PLACEMENT.md` found on the same provider.
- **What the first call does.** It cuts the governing rule's region by the first
  lower listed rule the ticket matches, a rule of another queue that crosses
  `H04` or `H05`. The note says the cut wins there by containment.
- **What T1 changes.** Only a reasoning that reads it. The reasoning walks the 29
  rules, finds the first match, and spends itself on the overlaps. Where it
  quotes T1, it weighs the instruction and writes the region whole. Where it
  does not, the default cut follows.
- **The bet is Q3.** If it fails, the reasoning read T1 and cut anyway. Then the
  700 characters after each quote say why: the level-1 sentence, or §6.10's
  reading of *el resto de su región* as the draft's own region.
- **Q1 is trusted most.** It is what the same provider did in `PLAN_PLACEMENT.md`'s
  runs, 11 of 15 drafts at the queue's tickets.
- **Q4 is trusted least.** Two drafts carry it, and a whole draft can also come
  from a reasoning that never weighs the instruction.

**What the drafter had seen**:
- `FINDINGS_WHOLE.md` whole. For each of the queue's first calls it gives the
  run, the case, the governing rule, the queue drafted, Stage C's class and
  breadth, and the verdict. For each run it gives what the final base lost of
  `H04`'s and `H05`'s regions, and the lengths of the lists at the queue's
  drafts.
- `score.json`'s `first_drafts` for those calls, which carry the same.
- **The smoke run's 14 first calls**, the codebook's development set: counts of
  candidate phrases in their reasoning, windows around T1's sentences in the
  reasoning of cases 1, 3, 6 and 9, and the head and tail of case 3's.
- **The field names** of an escalation, a call, a payload and an attempt, read in
  `loop_smoke.json`.
- `placement/oncall.py`, its record's FINDINGS section, and the POST-RUN sections
  of `FINDINGS_PLACEMENT.md`.

**What the drafter had not seen**: any condition, note, side, reasoning or
placement answer of a first call on a ticket of the queue in this plan's six
runs, and which rule any of them cut by.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-10, after Stage C. The codebook and
the expectation above were written and committed before the reading ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API
calls.

Usage:  python3 -m whole.oncall --dry-run   # gates 1 to 5; writes nothing
        PYTHONHASHSEED=0 python3 -m whole.oncall
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

from harness.provenance import describe, environment

from manual import instrument as MI
from placement import oncall as PO
from reasoned_loop import governed as gv
from reasoned_loop import references as rl_refs
from reuse import structure as st

from . import plan

QUEUE = PO.QUEUE                   # ONCALL_ESCALATION
H04, H05 = PO.H04, PO.H05          # the listed rules whose regions hold the queue
PARTS = (H04, H05)

# The codebook, frozen on the smoke run's first calls before the reading ran.
CODEBOOK: dict[str, tuple[str, ...]] = {
    "T1": (r"\bregi[oó]n\s+entera\b", r"\ba[nñ]adas\s+condiciones\b"),
    "T1e": (r"\b(?:whole|entire|full)\s+region\b",
            r"\b(?:should|must)\s+not\s+add\b[^.\n]{0,40}?\bconditions?\b"),
    "INSIDE": (r"\bcaso\s+particular\b", r"\bcontenid[ao]s?\b", r"\bdentro\s+de\b",
               r"\bsubconjunto\b", r"\bintersecci[oó]n\b"),
}
READ_IN = {"T1": "reasoning", "T1e": "reasoning", "INSIDE": "note"}
DEVELOPMENT = {"calls": 14, "T1": 6, "T1e": 1, "T1_or_T1e": 6, "INSIDE": 7}

WINDOW = 700        # the characters kept after each quote of T1
QUOTES = 3          # at most this many quotes kept a call
TAIL = 1500         # the last characters of the reasoning, where the answer is composed

# The expectation's lines.
Q3_SKIPPED = 4      # of v1d's six cuts
Q5_HALF = (1, 2)    # of the cuts, over both arms

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-10, after Stage C. The codebook and the "
    "expectation in the module's docstring were written and committed before the reading "
    "ran. Not a signed row; no verdict moves.")


def record_path():
    return plan.OUT / "oncall.json"


# ---------------------------------------------------------------------------
# The codebook
# ---------------------------------------------------------------------------

def count(code: str, text: str | None) -> int:
    """How many times a code's patterns match a text, case-blind."""
    return sum(len(re.findall(p, text or "", re.I)) for p in CODEBOOK[code])


def reads_t1(reasoning: str | None) -> bool:
    return count("T1", reasoning) + count("T1e", reasoning) > 0


def quotes(reasoning: str | None) -> list[dict[str, Any]]:
    """Up to `QUOTES` quotes of T1, each with the `WINDOW` characters that start
    at it. A quote that starts inside the last window kept is not kept again."""
    text = reasoning or ""
    starts = sorted({m.start() for c in ("T1", "T1e") for p in CODEBOOK[c]
                     for m in re.finditer(p, text, re.I)})
    out, end = [], -1
    for s in starts:
        if s < end:
            continue
        out.append({"at": s, "text": text[s:s + WINDOW]})
        end = s + WINDOW
        if len(out) == QUOTES:
            break
    return out


def development(smoke: dict) -> dict[str, int]:
    """The codebook's counts on the smoke run's first calls (gate 5)."""
    firsts = [c for e in smoke["escalations"] for c in e.get("calls") or []
              if c.get("round") == 0]
    note = lambda c: (c.get("payload") or {}).get("note")
    return {"calls": len(firsts),
            "T1": sum(1 for c in firsts if count("T1", c.get("reasoning"))),
            "T1e": sum(1 for c in firsts if count("T1e", c.get("reasoning"))),
            "T1_or_T1e": sum(1 for c in firsts if reads_t1(c.get("reasoning"))),
            "INSIDE": sum(1 for c in firsts if count("INSIDE", note(c)))}


# ---------------------------------------------------------------------------
# Each first call on a ticket of the queue
# ---------------------------------------------------------------------------

def same_condition(a: dict, b: dict) -> bool:
    norm = lambda v: sorted(v) if isinstance(v, list) else v
    return (a.get("attr"), a.get("op"), norm(a.get("value"))) == \
           (b.get("attr"), b.get("op"), norm(b.get("value")))


def extra_conditions(conditions: list[dict] | None, governing: list[dict]) -> list[dict]:
    """The draft's conditions that are none of its governing rule's."""
    return [c for c in conditions or [] if not any(same_condition(c, g) for g in governing)]


def placement_of(esc: dict, queues: dict[str, str]) -> dict[str, Any] | None:
    """The placement round that followed the first call, if any: the rules of the
    base it listed, with their queues, the rules its answer left without a side,
    and its sides and note."""
    calls = esc.get("calls") or []
    second = next((c for c in calls if c.get("round") == 1), None)
    if second is None:
        return None
    listed = (calls[0].get("listed") or []) if calls else []
    p = second.get("payload") or {}
    return {"listed": [[r, queues.get(r)] for r in listed],
            "left_without_a_side": second.get("unplaced"),
            "beats": p.get("beats"), "loses_to": p.get("loses_to"), "note": p.get("note"),
            "failure": second.get("failure")}


def first_calls(run: str, record: dict, stage_c_drafts: list[dict], space, regions: dict[str, int],
                cases: tuple, governing_conditions: dict[str, list[dict]]) -> list[dict[str, Any]]:
    """Every escalation on a ticket of the queue: its first call read whole."""
    rows = {r["idx"]: r for r in record["records"]}
    stage_c = {d["idx"]: d for d in stage_c_drafts}
    queues = {r["rule_id"]: r["action"] for r in record["rules"]}
    out = []
    for esc in record["escalations"]:
        row = rows.get(esc["idx"], {})
        if row.get("truth") != QUEUE:
            continue
        gov = row.get("truth_rule")
        c0 = (esc.get("calls") or [{}])[0]
        payload = c0.get("payload") or {}
        d = PO.draft_ext(payload, space)
        m = PO.matched(gv.point_of(cases[esc["idx"]], space), regions)
        cut = PO.cut_by(d, gov, regions)
        first = PO.first_cutting(m, gov, regions)
        sc = stage_c.get(esc["idx"], {})
        reasoning = c0.get("reasoning")
        note = payload.get("note")
        tokens = [a.get("reasoning_tokens") for a in c0.get("call_attempts") or []
                  if a.get("error") is None]
        out.append({
            "run": run, "arm": run.split("_")[0], "idx": esc["idx"], "governing": gov,
            "class": sc.get("class"), "breadth": sc.get("breadth"),
            "stage_c_governing": sc.get("governing"), "stage_c_verdict": sc.get("verdict"),
            "verdict": esc.get("verdict"), "rule_id": esc.get("rule_id"),
            "action": payload.get("action"), "conditions": payload.get("conditions"),
            "governing_conditions": governing_conditions.get(gov),
            "extra_conditions": extra_conditions(payload.get("conditions"),
                                                 governing_conditions.get(gov) or []),
            "matched": m, "first_match_is_governing": bool(m) and m[0] == gov,
            "first_cutting_match": first, "cut_by": cut,
            "cut_by_the_first_cutting_match": bool(cut) and first in cut,
            "note": note, "note_cites": sorted(set(PO.CITED.findall(note or ""))),
            "beats": payload.get("beats"), "loses_to": payload.get("loses_to"),
            "codes": {"T1": count("T1", reasoning), "T1e": count("T1e", reasoning),
                      "INSIDE": count("INSIDE", note)},
            "reads_t1": reads_t1(reasoning),
            "quotes_of_t1": quotes(reasoning),
            "answer_composed": (reasoning or "")[-TAIL:],
            "reasoning_chars": len(reasoning or ""),
            "reasoning_tokens": tokens[-1] if tokens else None,
            "has_reasoning": bool(reasoning), "has_payload": bool(payload),
            "placement": placement_of(esc, queues),
        })
    return out


def is_cut(row: dict) -> bool:
    return str(row.get("class") or "").startswith("cut_by")


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def gates(rows: list[dict], dev: dict[str, int]) -> list[dict[str, Any]]:
    return [
        {"gate": 1, "what": "every escalation on a ticket of the queue is governed by H04 or H05",
         "passes": bool(rows) and all(r["governing"] in PARTS for r in rows)},
        {"gate": 2, "what": "each such ticket lies first in its governing rule's region",
         "passes": all(r["first_match_is_governing"] for r in rows)},
        {"gate": 3, "what": "each such first call's governing rule, class and verdict are "
                            "Stage C's",
         "passes": all(r["class"] is not None and r["stage_c_governing"] == r["governing"]
                       and r["stage_c_verdict"] == r["verdict"] for r in rows)},
        {"gate": 4, "what": "every such first call keeps its reasoning and its payload",
         "passes": all(r["has_reasoning"] and r["has_payload"] for r in rows)},
        {"gate": 5, "what": "the codebook gives DEVELOPMENT's counts on the smoke run's first "
                            "calls",
         "reading": dev, "passes": dev == DEVELOPMENT},
    ]


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def expectation(rows: list[dict]) -> list[dict[str, Any]]:
    v1d = [r for r in rows if r["arm"] == "v1d"]
    v1d_cuts = [r for r in v1d if is_cut(r)]
    v1d_whole = [r for r in v1d if r["class"] == "whole"]
    cuts = [r for r in rows if is_cut(r)]
    by_ticket: dict[int, list[dict]] = {}
    for r in cuts:
        by_ticket.setdefault(r["idx"], []).append(r)
    both = {i: rs for i, rs in by_ticket.items() if {r["arm"] for r in rs} == {"v1c", "v1d"}}
    skipped = sum(1 for r in v1d_cuts if not r["reads_t1"])
    inside = sum(1 for r in cuts if r["codes"]["INSIDE"])
    num, den = Q5_HALF
    return [
        {"clause": "Q1", "what": "every v1d cut is its governing rule's region cut by the first "
                                 "lower listed rule the ticket matches that a cut by would change",
         "reading": [[r["run"], r["idx"], r["cut_by"], r["first_cutting_match"]] for r in v1d_cuts],
         "holds": bool(v1d_cuts) and all(r["cut_by_the_first_cutting_match"] for r in v1d_cuts)},
        {"clause": "Q2", "what": "at every ticket where both arms' first calls cut, every cut "
                                 "there is by the same rules",
         "reading": {i: [[r["run"], r["cut_by"]] for r in rs] for i, rs in sorted(both.items())},
         "holds": bool(both) and all(len({tuple(r["cut_by"] or []) for r in rs}) == 1
                                     for rs in both.values())},
        {"clause": "Q3", "what": f"in at least {Q3_SKIPPED} of v1d's cuts the reasoning neither "
                                 "quotes T1 nor says it in English",
         "reading": {"skipped": skipped, "of": len(v1d_cuts)},
         "holds": skipped >= Q3_SKIPPED},
        {"clause": "Q4", "what": "in both of v1d's whole drafts on tickets of the queue the "
                                 "reasoning quotes T1 or says it in English",
         "reading": {"reading_it": sum(1 for r in v1d_whole if r["reads_t1"]),
                     "of": len(v1d_whole)},
         "holds": bool(v1d_whole) and all(r["reads_t1"] for r in v1d_whole)},
        {"clause": "Q5", "what": "at least half of the cuts, over both arms, carry a note that "
                                 "says the draft lies inside another rule",
         "reading": {"saying_it": inside, "of": len(cuts)},
         "holds": bool(cuts) and inside * den >= num * len(cuts)},
    ]


def summary(rows: list[dict]) -> dict[str, Any]:
    out = {}
    for arm in plan.ARMS:
        rs = [r for r in rows if r["arm"] == arm]
        cuts = [r for r in rs if is_cut(r)]
        whole = [r for r in rs if r["class"] == "whole"]
        out[arm] = {"first_calls": len(rs), "cuts": len(cuts), "whole": len(whole),
                    "cuts_reading_t1": sum(1 for r in cuts if r["reads_t1"]),
                    "whole_reading_t1": sum(1 for r in whole if r["reads_t1"]),
                    "cuts_by_the_first_cutting_match":
                        sum(1 for r in cuts if r["cut_by_the_first_cutting_match"]),
                    "cuts_saying_inside": sum(1 for r in cuts if r["codes"]["INSIDE"])}
    return out


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict], dict[str, Any], dict]:
    records = {plan.tag(arm, rep): json.loads(plan.run_path(arm, rep).read_text())
               for arm, rep in plan.schedule()}
    return (records, json.loads(plan.score_path().read_text()),
            json.loads(plan.smoke_path().read_text()))


def read_rows(records: dict[str, dict], stage_c: dict[str, Any]) -> list[dict[str, Any]]:
    space, regions, cases = MI.space(), rl_refs.regions(), MI.corpus()
    conds = {r.id: rl_refs.payload_of(r)["conditions"] for r in rl_refs.text_rules()}
    runs = stage_c["WR-g"]["runs"]
    return [row for t, rec in records.items()
            for row in first_calls(t, rec, runs[t]["first_drafts"], space, regions, cases, conds)]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why v1d cut at the rarest queue's tickets "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 5 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"whole/oncall.py writes {record_path()}")
    records, stage_c, smoke = read_all()
    rows = read_rows(records, stage_c)
    checked = gates(rows, development(smoke))
    for g in checked:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    clauses = expectation(rows)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"score": str(plan.score_path()),
                   "score_from": stage_c["_env"].get("git_commit"),
                   "development": str(plan.smoke_path())},
        "queue": QUEUE,
        "codebook": {k: {"patterns": list(v), "read_in": READ_IN[k]} for k, v in CODEBOOK.items()},
        "development": DEVELOPMENT,
        "constants": {"WINDOW": WINDOW, "QUOTES": QUOTES, "TAIL": TAIL,
                      "Q3_SKIPPED": Q3_SKIPPED, "Q5_HALF": list(Q5_HALF)},
        "gates": checked,
        "summary": summary(rows),
        "first_calls": rows,
        "expectation": clauses,
    }), indent=2, default=str, ensure_ascii=False) + "\n")
    for c in clauses:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
