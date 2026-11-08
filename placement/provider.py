"""
WHETHER THE CUT IS THE PROVIDER'S.
`placement/oncall.py` found the first call cutting the rarest queue's drafts. In
this plan's six runs, on DeepInfra, no draft at a ticket of `H04` was `H04`'s
region whole, in eleven. In `PLAN_CHANNEL.md`'s six runs, on Baidu, seven of
thirteen held the part's size. The two plans ran in different periods, so that
reading cannot say whether the provider cut the drafts or the period did.
`FINDINGS_PLACEMENT.md`, *Why the runs under run 3's draws lost
`ONCALL_ESCALATION`*, and `IDEAS.md` carry the question. The bridge can answer
it. On 2026-11-07, before the first run, it asked the first call both arms send
at each of the queue's seven tickets, once of Baidu and once of DeepInfra. Free
on the records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
For each of the queue's seven tickets, each provider's answer in the bridge,
read as `placement/oncall.py` reads a run's draft:
- the queue it names;
- its draft against the ticket's part, `H04`'s or `H05`'s: its points of the
  part, and whether it holds the part whole;
- the listed rules whose region, cut by the governing rule's, is the draft, and
  whether the first matched rule a cut changes is one of them;
- the listed identifiers its note cites.

Beside them, at the same tickets, the first-call drafts of the runs: this plan's
six on DeepInfra, as `oncall.json` records them, and `PLAN_CHANNEL.md`'s six on
Baidu, read from their records the same way.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. the bridge asked each of the queue's seven tickets once of each provider,
     in its first call;
  2. each ticket is governed by `H04` or `H05`, and lies first in its governing
     rule's region;
  3. the drafts read from `PLAN_CHANNEL.md`'s records give back the points of the
     queue that `results_channel/oncall.json` records for each escalation.

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates, prints pass or fail, and
writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads the bridge's answers at the queue's seven tickets, four of
`H04`'s and three of `H05`'s.

  Q1. **DeepInfra cut `H04`.** None of DeepInfra's four answers at tickets of
      `H04` holds `H04`'s part whole.
  Q2. **Baidu wrote it whole.** At least two of Baidu's four answers at tickets
      of `H04` hold `H04`'s part whole.
  Q3. **The provider, ticket by ticket.** At more of the seven tickets Baidu's
      answer holds its part whole and DeepInfra's does not than the reverse.
  Q4. **The same cut.** Every DeepInfra answer at a ticket of the queue that one
      listed rule cuts is cut by the first matched rule a cut changes, and there
      is at least one such answer.

**The drafter's account.** The cut is DeepInfra's. Asked the same request on
the same day, its first call writes the governing rule's region cut by the next
listed rule a cut changes, and Baidu's writes the region whole more often.
- **Why it expects that.** In the runs DeepInfra cut every draft at a ticket of
  `H04`, eleven of eleven, and Baidu's drafts held the part's size at seven of
  thirteen. Over the bridge's 40 tickets DeepInfra wrote the governing rule's
  region on 13 of its 39 rules, and Baidu on 18 of its 40 (`PL-g`).
- **The bet is Q3.**
- **Q2 is trusted least.** Baidu cut six of its thirteen drafts at tickets of
  `H04` in the runs, and one ask a ticket gives each of its four answers that
  chance again.
- **Q1 is trusted most.** It is the runs' eleven of eleven, asked once more.

**What the drafter had seen**:
- `FINDINGS_PLACEMENT.md` whole, its POST-RUN section included, and
  `oncall.json`, which holds this plan's run drafts at the queue's tickets;
- `results_channel/oncall.json`'s points of the queue for each of
  `PLAN_CHANNEL.md`'s escalations of the queue, with their governing rules;
- `bridge.json`'s field names, its stage, its blind base, the rounds and
  providers of its asks, and `plan.DECLARED`'s seven tickets of the queue;
- Stage C's reading of the bridge in `placement/score.py`, and its counts in the
  FINDINGS.

**What the drafter had not seen**: any answer of either provider in
`bridge.json`, at the queue's tickets or elsewhere.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-08, after `placement/oncall.py`'s
reading. The expectation above was written and committed before the reading ran.
Not a signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero
API calls.

Usage:  python3 -m placement.provider --dry-run   # gates 1 to 3; writes nothing
        PYTHONHASHSEED=0 python3 -m placement.provider
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from harness.provenance import describe, environment

from channel import oncall as O
from channel import plan as ch_plan
from manual import instrument as MI
from reasoned_loop import governed as gv
from reasoned_loop import references as rl_refs
from reuse import structure as st
from rung2.engine2 import Space

from . import oncall as PO
from . import plan, references

QUEUE = PO.QUEUE
H04, H05 = PO.H04, PO.H05
BAIDU, DEEPINFRA = plan.BRIDGE_PROVIDERS   # in the bridge's own order
CHANNEL_RUNS = tuple((arm, rep) for arm in ("e", "c") for rep in (1, 2, 3))

# The expectation's line.
Q2_WHOLE = 2

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-08, after placement/oncall.py's reading. "
    "The expectation in the module's docstring was written and committed before the "
    "reading ran. Not a signed row; no verdict moves.")


def record_path():
    return plan.OUT / "provider.json"


def queue_tickets() -> list[int]:
    """The bridge's tickets of the queue, as §0's figure 8 declares them."""
    return sorted(plan.DECLARED["bridge"][QUEUE])


# ---------------------------------------------------------------------------
# One answer, read as a run's draft
# ---------------------------------------------------------------------------

def read_draft(payload: dict | None, case, gov: str | None, space: Space,
               parts: dict[str, int], regions: dict[str, int],
               truth: int) -> dict[str, Any]:
    """A first call's answer against its ticket's part, as `placement/oncall.py`
    reads a run's draft: its points, whether it holds the part whole, and what it
    cut the governing rule's region by."""
    payload = payload or {}
    d = PO.draft_ext(payload, space)
    part = parts.get(gov)
    m = PO.matched(gv.point_of(case, space), regions)
    cut = PO.cut_by(d, gov, regions)
    first = PO.first_cutting(m, gov, regions)
    note = payload.get("note")
    return {"queue": payload.get("action"), "conditions": payload.get("conditions"),
            "draft_points": None if d is None else d.bit_count(),
            "draft_queue_points": None if d is None else (d & truth).bit_count(),
            "draft_part_points": None if d is None or part is None else (d & part).bit_count(),
            "holds_part": d is not None and part is not None and d & part == part,
            "cut_by": cut, "first_cutting_match": first,
            "cut_by_the_first_cutting_match": bool(cut) and first in cut,
            "note": note, "cites": sorted(set(PO.CITED.findall(note or "")))}


# ---------------------------------------------------------------------------
# The bridge
# ---------------------------------------------------------------------------

def asks_at(bridge: dict, tickets: list[int]) -> dict[tuple[int, str], list[dict]]:
    """The bridge's asks at the given tickets, by ticket and provider."""
    out: dict[tuple[int, str], list[dict]] = {}
    for a in bridge["asks"]:
        if a["idx"] in tickets:
            out.setdefault((a["idx"], a["provider"]), []).append(a)
    return out


def asked_once(asks: dict[tuple[int, str], list[dict]], tickets: list[int]) -> bool:
    """Gate 1."""
    return bool(tickets) and all(
        len(asks.get((i, p), [])) == 1 and asks[(i, p)][0].get("round") == 0
        for i in tickets for p in (BAIDU, DEEPINFRA))


def governed_first(tickets: list[int], labels, cases, space: Space,
                   regions: dict[str, int]) -> bool:
    """Gate 2."""
    for i in tickets:
        gov = labels[i][1]
        m = PO.matched(gv.point_of(cases[i], space), regions)
        if gov not in (H04, H05) or not m or m[0] != gov:
            return False
    return True


def bridge_answers(asks: dict[tuple[int, str], list[dict]], tickets: list[int], labels,
                   cases, space: Space, parts: dict[str, int], regions: dict[str, int],
                   truth: int) -> dict[int, dict[str, Any]]:
    """Each ticket of the queue: its governing rule, its part, and each provider's
    answer read as a draft."""
    out = {}
    for i in tickets:
        gov = labels[i][1]
        row: dict[str, Any] = {"idx": i, "governing": gov,
                               "part_points": parts[gov].bit_count() if gov in parts else None}
        for p in (BAIDU, DEEPINFRA):
            a = (asks.get((i, p)) or [{}])[0]
            row[p] = {**read_draft(a.get("payload"), cases[i], gov, space, parts, regions,
                                   truth),
                      "served_by": a.get("served_by"), "finish_reason": a.get("finish_reason")}
        out[i] = row
    return out


# ---------------------------------------------------------------------------
# The runs' first-call drafts at the same tickets
# ---------------------------------------------------------------------------

def placement_drafts(oncall: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """This plan's six runs, as `oncall.json` records each draft and its cut."""
    out = {}
    for t, run in oncall["runs"].items():
        cuts = {c["idx"]: c for c in run["cuts"]}
        out[t] = [{"idx": d["idx"], "governing": d["governing"],
                   "draft_queue_points": d["draft_queue_points"],
                   "draft_part_points": d["draft_part_points"], "holds_part": d["holds_part"],
                   "cut_by": cuts[d["idx"]]["cut_by"],
                   "cut_by_the_first_cutting_match":
                       cuts[d["idx"]]["cut_by_the_first_cutting_match"],
                   "verdict": d["verdict"]} for d in run["drafts"]]
    return out


def channel_drafts(records: dict[str, dict], space: Space, parts: dict[str, int],
                   regions: dict[str, int], truth: int, cases) -> dict[str, list[dict[str, Any]]]:
    """`PLAN_CHANNEL.md`'s six runs, each draft read from its record as
    `placement/oncall.py` reads this plan's."""
    out = {}
    for t, rec in records.items():
        ds = PO.drafts(rec, MI.final_engine(rec), space, parts, regions, truth)
        cuts = {c["idx"]: c for c in PO.cuts(rec, space, regions, cases)}
        out[t] = [{"idx": d["idx"], "governing": d["governing"],
                   "draft_queue_points": d["draft_queue_points"],
                   "draft_part_points": d["draft_part_points"], "holds_part": d["holds_part"],
                   "cut_by": cuts[d["idx"]]["cut_by"],
                   "cut_by_the_first_cutting_match":
                       cuts[d["idx"]]["cut_by_the_first_cutting_match"],
                   "verdict": d["verdict"]} for d in ds]
    return out


def same_points(read: dict[str, list[dict]], recorded: dict[str, Any]) -> bool:
    """Gate 3: each escalation's points of the queue, read here, are the ones
    `results_channel/oncall.json` records."""
    for t, ds in read.items():
        theirs = {e["idx"]: e["draft_queue_points"]
                  for e in recorded["runs"][t]["reading"]["escalations"]}
        if {d["idx"]: d["draft_queue_points"] for d in ds} != theirs:
            return False
    return bool(read)


def by_ticket(drafts: dict[str, list[dict]], tickets: list[int]) -> dict[int, dict[str, Any]]:
    """At each ticket, the runs' drafts: how many, and how many held the part."""
    out = {i: {"drafts": 0, "holding_the_part": 0, "runs": []} for i in tickets}
    for t, ds in drafts.items():
        for d in ds:
            if d["idx"] in out:
                out[d["idx"]]["drafts"] += 1
                out[d["idx"]]["holding_the_part"] += d["holds_part"]
                out[d["idx"]]["runs"].append(t)
    return out


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(answers: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = list(answers.values())
    h04 = [r for r in rows if r["governing"] == H04]

    def whole(rs, p):
        return sum(1 for r in rs if r[p]["holds_part"])

    baidu_only = [r["idx"] for r in rows
                  if r[BAIDU]["holds_part"] and not r[DEEPINFRA]["holds_part"]]
    deepinfra_only = [r["idx"] for r in rows
                      if r[DEEPINFRA]["holds_part"] and not r[BAIDU]["holds_part"]]
    cut = [r for r in rows if r[DEEPINFRA]["cut_by"]]
    return [
        {"clause": "Q1", "what": "none of DeepInfra's answers at tickets of H04 holds H04's "
                                 "part whole",
         "reading": {"whole": whole(h04, DEEPINFRA), "of": len(h04)},
         "holds": bool(h04) and whole(h04, DEEPINFRA) == 0},
        {"clause": "Q2", "what": f"at least {Q2_WHOLE} of Baidu's answers at tickets of H04 "
                                 "hold H04's part whole",
         "reading": {"whole": whole(h04, BAIDU), "of": len(h04)},
         "holds": whole(h04, BAIDU) >= Q2_WHOLE},
        {"clause": "Q3", "what": "at more tickets Baidu's answer holds its part whole and "
                                 "DeepInfra's does not than the reverse",
         "reading": {"baidu_only": baidu_only, "deepinfra_only": deepinfra_only,
                     "of": len(rows)},
         "holds": len(baidu_only) > len(deepinfra_only)},
        {"clause": "Q4", "what": "every DeepInfra answer one listed rule cuts is cut by the "
                                 "first matched rule a cut changes, and there is one",
         "reading": {t["idx"]: {"cut_by": t[DEEPINFRA]["cut_by"],
                                "first_cutting_match": t[DEEPINFRA]["first_cutting_match"]}
                     for t in cut},
         "holds": bool(cut) and all(t[DEEPINFRA]["cut_by_the_first_cutting_match"]
                                    for t in cut)},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict, dict, dict, dict[str, dict]]:
    bridge = json.loads(plan.bridge_path().read_text())
    oncall = json.loads(PO.record_path().read_text())
    channel_oncall = json.loads((ch_plan.OUT / "oncall.json").read_text())
    channel = {ch_plan.tag(arm, rep): references.closed_record("channel", arm, rep)
               for arm, rep in CHANNEL_RUNS}
    return bridge, oncall, channel_oncall, channel


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Whether the cut is the provider's: the "
                                             "bridge at the queue's tickets (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 3 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"placement/provider.py writes {record_path()}")
    bridge, oncall, channel_oncall, channel = read_all()
    space, cases, labels = MI.space(), MI.corpus(), plan.labels()
    truth = MI.space_truth()[QUEUE]
    regions = rl_refs.regions()
    parts = O.parts(truth, regions)
    tickets = queue_tickets()
    asks = asks_at(bridge, tickets)
    baidu_runs = channel_drafts(channel, space, parts, regions, truth, cases)
    gates = [
        {"gate": 1, "what": "the bridge asked each of the queue's tickets once of each "
                            "provider, in its first call",
         "passes": asked_once(asks, tickets)},
        {"gate": 2, "what": "each ticket is governed by H04 or H05, and lies first in its "
                            "governing rule's region",
         "passes": governed_first(tickets, labels, cases, space, regions)},
        {"gate": 3, "what": "the drafts read from PLAN_CHANNEL.md's records give back "
                            "results_channel/oncall.json's points",
         "passes": same_points(baidu_runs, channel_oncall)},
    ]
    for g in gates:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
    if not all(g["passes"] for g in gates):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    answers = bridge_answers(asks, tickets, labels, cases, space, parts, regions, truth)
    deepinfra_runs = placement_drafts(oncall)
    expectation = read_expectation(answers)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"bridge": str(plan.bridge_path()),
                   "bridge_from": bridge["_env"].get("git_commit"),
                   "oncall": str(PO.record_path()),
                   "oncall_from": oncall["_env"].get("git_commit"),
                   "channel_oncall": str(ch_plan.OUT / "oncall.json")},
        "surface": "the exhaustive space, 134,400 points, for each answer's draft",
        "queue": QUEUE,
        "tickets": tickets,
        "constants": {"Q2_WHOLE": Q2_WHOLE},
        "gates": gates,
        "bridge": answers,
        "runs": {"deepinfra": {"drafts": deepinfra_runs,
                               "by_ticket": by_ticket(deepinfra_runs, tickets)},
                 "baidu": {"drafts": baidu_runs, "by_ticket": by_ticket(baidu_runs, tickets)}},
        "expectation": expectation,
    }), indent=2, default=str) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
