"""
Stage A of `PLAN_SCREEN.md`: the blocking checks, the populations, the sessions
and the free readout. It spends nothing and asks nothing.

THE CHECKS (§6). All are blocking, and the paid stage runs them again before any
call.

  V-g1  The inputs reproduce themselves.
        * The suite is green.
        * `PLAN_FIDELITY.md`'s own F-g1 to F-g3 pass on its inputs, and its Stage
          A record is the design they rebuild (`fidelity.ask.sample_matches`).
        * Its Stage C, re-run here in memory with `fidelity.score`'s own
          functions on its session records, gives back
          `results_fidelity/score.json`: the verdicts, the births, every run's
          rows and standard errors, and F-f's ticket-only arm. Floats agree to
          FLOAT_REL_TOL, because another interpreter may round a standard
          deviation one unit in the last place away.
        * Every one of those session records carries its plan's protocol and
          the digest of its Stage A record.
  V-g2  The prompts are `PLAN_FIDELITY.md`'s.
        * Every ticket's prompt is v1's empty-base rendering, built by
          `fidelity.prompts.ticket_only`, and for the 301 tickets F-f asked its
          digest is the one F-f's Stage A recorded.
        * Every anchor prompt is F-f's B prompt for that decision, rebuilt by
          `fidelity`'s replay, with the digest recorded there. That every B
          prompt hides every rule matching its ticket is F-g3's, above.
        * The plurality is defined for every pilot and held-out decision.
  V-g3  The populations are §0's.
        * The pilot is the first PILOT_PER_RUN of each draw.
        * The held-out set has HELD_OUT_SIZES decisions, none of them on a
          ticket F-f asked, and every one of their screens shows a rule.
        * At most MAX_INVALID_SHARE of each run's held-out decisions lack two
          valid answers with the screen.
        * The tickets number TICKETS, F-f's ASKED_BY_F_F among them, and each
          session asks what §1 says, every ticket in each pass.
  V-g4  The signature (`screen/plan.py`).

A TICKET IS ITS ATTRIBUTES, `Case.key()`, as `PLAN_FIDELITY.md` keyed its
ticket-only arm (§0). The corpus repeats tickets, and the prompt without a
screen depends on the attributes alone, so two cases with the same attributes
are one ticket. A ticket's id is `t:` and its smallest case index, and a ticket
F-f asked carries the id F-f gave it, under `asked_by_F_f`.

THE POPULATIONS (§0). The pilot is the first PILOT_PER_RUN decisions of each
run's uniform draw: the ones F-f paired. The held-out decisions are the rest of
the draw, less every decision on a ticket F-f asked. Every decision carries its
B prompt's digest and the screen's plurality action, `fidelity.prompts.plurality`,
which reads no label.

THE SESSIONS (§1 and §8): smoke, anchor, ticket_only. The ticket-only session
asks every ticket of the draw and the census, in TICKET_ONLY_DRAWS passes, each
its own seeded order. The anchor asks the pilot's B prompts once. The smoke run
asks the first SMOKE_PER_ARM of each.

THE READOUT, `V-e`'s free half (§7), written only after the signature.
  * The pilot, as the drafter's scratch probe read it: every figure §0 lists as
    already seen, measured by this module so that this record owns it.
  * The held-out decisions, without a single new answer: the share whose
    screen's plurality is the true queue (which is also the accuracy of a
    copier that answers it), the size of each cell of `V-d`, and the class mix
    beside the draw's.
The labels come off `PLAN_FIDELITY.md`'s records and are used only to count,
never to build a prompt.

    python3 -m screen.sample --dry-run     # V-g1..V-g4; writes nothing
    python3 -m screen.sample               # refuses while PLAN_SCREEN.md is unsigned
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from harness.provenance import describe, environment

from fidelity import ask as fidelity_ask
from fidelity import prompts
from fidelity import sample as fidelity_sample
from fidelity import score as fidelity_score
from reuse import gates as reuse_gates

from . import plan

TICKET_ONLY, HIDDEN = prompts.TICKET_ONLY, prompts.HIDDEN
PILOT, HELD_OUT = "pilot", "held_out"


# ---------------------------------------------------------------------------
# Inputs: PLAN_FIDELITY.md's records, read and never written (rule B)
# ---------------------------------------------------------------------------

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_paths() -> dict[str, Path]:
    out = {"sample": plan.FIDELITY_SAMPLE, "score": plan.FIDELITY_SCORE,
           "ticket_only": plan.FIDELITY_TICKET_ONLY}
    out.update({f"base{k}": plan.fidelity_base(k) for k in plan.RUNS})
    return out


def load_fidelity_sessions() -> tuple[dict[str, dict], list[str]]:
    """F-f's session records: births, the three bases and the ticket-only arm."""
    return fidelity_score.load_sessions()


def fidelity_bases(found: dict[str, dict]) -> dict[int, dict[str, dict]]:
    """Its answers with the screen, grouped by decision: `d<run>:<case>`."""
    return {k: fidelity_score.group(found[f"base{k}"]["rows"])
            for k in plan.RUNS if f"base{k}" in found}


# ---------------------------------------------------------------------------
# The design: the populations, the tickets, the items and the sessions
# ---------------------------------------------------------------------------

@dataclass
class Design:
    fidelity: fidelity_sample.Design = field(repr=False)
    pilot: dict[int, list[int]]
    held_out: dict[int, list[int]]
    decisions: dict[str, dict]                # d<run>:<case>, pilot and held-out
    tickets: dict[str, dict]                  # t<smallest case>, by Case.key()
    items: dict[str, dict]                    # what a session asks
    sessions: dict[str, dict]
    prompts: dict[str, prompts.Prompt] = field(repr=False)
    problems: list[str] = field(default_factory=list)

    def ticket_of(self, run: int, idx: int) -> str:
        return self.decisions[f"d{run}:{idx}"]["ticket"]


def session(name: str, ids: list[str], draws: int) -> dict[str, Any]:
    """One session: its items once, and each pass its own seeded order."""
    passes = []
    for pass_no in range(1, draws + 1):
        order = list(ids)
        plan.order_rng(name, pass_no).shuffle(order)
        passes.append(order)
    return {"items": list(ids), "passes": passes}


def build_design(fid: fidelity_sample.Design) -> Design:
    corpus = fid.corpus
    problems: list[str] = []

    def key(idx: int) -> tuple:
        return corpus[idx].key()

    # The tickets F-f asked on 2026-10-03, by key, with the id F-f gave them.
    asked = {key(it["idx"]): iid for iid, it in fid.items.items()
             if it["kind"] == TICKET_ONLY}

    pilot = {k: list(fid.draw[k]["uniform"][:plan.PILOT_PER_RUN]) for k in plan.RUNS}
    held_out = {k: [i for i in fid.draw[k]["uniform"][plan.PILOT_PER_RUN:]
                    if key(i) not in asked] for k in plan.RUNS}

    # Every case of the draw, of each run's census, and every rare-class case
    # of the corpus, as F-f's ticket-only arm took them: grouped by ticket.
    cases: dict[tuple, set[int]] = collections.defaultdict(set)
    rare: dict[tuple, str] = {}
    for k in plan.RUNS:
        for i in fid.draw[k]["uniform"]:
            cases[key(i)].add(i)
        for idxs in fid.draw[k]["census"].values():
            for i in idxs:
                cases[key(i)].add(i)
    for r in fid.runs[plan.RUNS[0]]["records"]:
        if r["truth"] in plan.RARE:
            cases[key(r["idx"])].add(r["idx"])
            rare[key(r["idx"])] = r["truth"]

    tickets: dict[str, dict] = {}
    items: dict[str, dict] = {}
    built: dict[str, prompts.Prompt] = {}
    ticket_of_key: dict[tuple, str] = {}
    for kk, idxs in sorted(cases.items(), key=lambda kv: min(kv[1])):
        rep = min(idxs)
        tid = f"t:{rep}"
        p = prompts.ticket_only(corpus[rep])
        problems += [f"ticket {rep}: {x}" for x in prompts.check_ticket_only(p)]
        f_id = asked.get(kk)
        if f_id is not None and fid.items[f_id]["digest"] != p.digest:
            problems.append(f"ticket {rep}: its prompt is not the one F-f asked as {f_id}")
        tickets[tid] = {"id": tid, "kind": TICKET_ONLY, "run": None, "idx": rep,
                        "cases": sorted(idxs), "asked_by_F_f": f_id,
                        "rare": rare.get(kk), "serves": [], "digest": p.digest}
        ticket_of_key[kk] = tid
        built[tid] = p
    if set(asked) - set(ticket_of_key):
        problems.append("a ticket F-f asked is outside the draw and the census")

    decisions: dict[str, dict] = {}
    for k in plan.RUNS:
        for population, idxs in ((PILOT, pilot[k]), (HELD_OUT, held_out[k])):
            for i in idxs:
                did = f"d{k}:{i}"
                p = fid.prompts.get(did)
                if p is None or fid.items[did]["kind"] != HIDDEN:
                    problems.append(f"{did}: PLAN_FIDELITY.md built no B prompt for it")
                    continue
                tid = ticket_of_key[key(i)]
                tickets[tid]["serves"].append([k, i])
                decisions[did] = {"id": did, "run": k, "idx": i, "population": population,
                                  "ticket": tid, "digest": p.digest,
                                  "shown_ids": list(p.shown_ids),
                                  "shown_actions": list(p.shown_actions),
                                  "plurality": prompts.plurality(p),
                                  "first_shown": prompts.first_shown(p)}
                if population == PILOT:
                    items[did] = {"id": did, "kind": HIDDEN, "run": k, "idx": i,
                                  "ticket": tid, "digest": p.digest,
                                  "shown_ids": list(p.shown_ids)}
                    built[did] = p
    items.update(tickets)

    anchor = [f"d{k}:{i}" for k in plan.RUNS for i in pilot[k]]
    sessions = {"anchor": session("anchor", anchor, plan.ANCHOR_DRAWS),
                "ticket_only": session("ticket_only", list(tickets),
                                       plan.TICKET_ONLY_DRAWS)}
    smoke = (sessions["ticket_only"]["passes"][0][:plan.SMOKE_PER_ARM]
             + sessions["anchor"]["passes"][0][:plan.SMOKE_PER_ARM])
    sessions["smoke"] = {"items": smoke, "passes": [smoke]}
    return Design(fidelity=fid, pilot=pilot, held_out=held_out, decisions=decisions,
                  tickets=tickets, items=items, sessions=sessions, prompts=built,
                  problems=problems)


# ---------------------------------------------------------------------------
# V-g1: the inputs reproduce themselves
# ---------------------------------------------------------------------------

def _norm(x: Any) -> Any:
    return json.loads(json.dumps(x))


# How close two floats must be to count as the same figure. The interpreter that
# wrote PLAN_FIDELITY.md's record and the one re-running its Stage C may round a
# standard deviation differently: Python 3.11 changed how `statistics.stdev`
# takes its square root, and on 3.10 three of the record's standard errors come
# back one or two units in the last place away (CI, 2026-10-14). Any real change
# to an input moves a figure by far more than this.
FLOAT_REL_TOL = 1e-12
FLOAT_ABS_TOL = 1e-15


def same(a: Any, b: Any) -> bool:
    """Equal, structure for structure, with floats compared to FLOAT_REL_TOL.
    A bool is never a number here, and an int is compared exactly."""
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, float) or isinstance(b, float):
        return (isinstance(a, (int, float)) and isinstance(b, (int, float))
                and math.isclose(a, b, rel_tol=FLOAT_REL_TOL, abs_tol=FLOAT_ABS_TOL))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def fidelity_stage_c(fid: fidelity_sample.Design, found: dict[str, dict]) -> list[str]:
    """`PLAN_FIDELITY.md`'s Stage C, re-run in memory with its own functions,
    against the record it wrote. Every difference is a problem."""
    if any(s not in found for s in fidelity_score.REQUIRED + ("ticket_only",)):
        return ["PLAN_FIDELITY.md's session records are incomplete"]
    births = fidelity_score.score_births(found["births"]["rows"])
    per_run = [fidelity_score.score_run(k, found[f"base{k}"]["rows"], fid.runs[k],
                                        fid.corpus) for k in plan.RUNS]
    verdicts = fidelity_score.adjudicate(births, per_run)
    arm = fidelity_score.ticket_only_arm(found["ticket_only"]["rows"],
                                         fidelity_bases(found))
    stored = json.loads(plan.FIDELITY_SCORE.read_text())
    differs = []
    if not same(_norm(verdicts), stored.get("verdicts")):
        differs.append("its verdicts")
    if not same(_norm(births), stored.get("births")):
        differs.append("its births")
    stored_runs = {r.get("run"): r for r in stored.get("runs", [])}
    for r in per_run:
        for part in ("rows", "standard_errors"):
            if not same(_norm(r[part]), stored_runs.get(r["run"], {}).get(part)):
                differs.append(f"run {r['run']}'s {part}")
    if not same(_norm(arm), (stored.get("F-f") or {}).get("ticket_only")):
        differs.append("F-f's ticket-only arm")
    return [f"re-run in memory, PLAN_FIDELITY.md's Stage C does not give back {d}"
            for d in differs]


def fidelity_records(found: dict[str, dict]) -> list[str]:
    """Every session record under F-f's protocol, behind F-f's Stage A record."""
    digest = fidelity_ask.sample_sha256()
    protocol = fidelity_ask.protocol()
    problems = []
    for name, rec in sorted(found.items()):
        wrong = sorted(k for k, v in protocol.items() if rec.get(k) != v)
        if wrong:
            problems.append(f"{name}: not under PLAN_FIDELITY.md's protocol ({wrong})")
        if rec.get("sample_sha256") != digest:
            problems.append(f"{name}: not behind PLAN_FIDELITY.md's Stage A record")
    return problems


def gate_vg1(fid_checks: fidelity_sample.Checks, found: dict[str, dict],
             missing: list[str], suite: bool = True) -> dict[str, Any]:
    problems = [f"missing {m}" for m in missing]
    if not fid_checks.blocking_pass:
        problems.append("PLAN_FIDELITY.md's own F-g1 to F-g3 do not pass")
    ok, why = fidelity_ask.sample_matches(fid_checks.design)
    if not ok:
        problems.append(f"PLAN_FIDELITY.md's Stage A record: {why}")
    if not missing:
        problems += fidelity_records(found)
        problems += fidelity_stage_c(fid_checks.design, found)
    tests = reuse_gates.run_suite() if suite else {"ran": False, "passes": None}
    return {
        "what": ("the suite is green; PLAN_FIDELITY.md's F-g1 to F-g3 pass and its "
                 "Stage A record is the design they rebuild; its Stage C, re-run in "
                 "memory, gives back its score.json; and every session record is "
                 "under its protocol, behind its Stage A record"),
        "fidelity_checks": {"F-g1": fid_checks.fg1["passes"],
                            "F-g2": fid_checks.fg2["passes"],
                            "F-g3": fid_checks.fg3["passes"]},
        "first_problems": problems[:10],
        "suite": tests,
        "passes": not problems and tests["passes"] is not False,
    }


# ---------------------------------------------------------------------------
# V-g2: the prompts are PLAN_FIDELITY.md's
# ---------------------------------------------------------------------------

def gate_vg2(design: Design) -> dict[str, Any]:
    problems = list(design.problems)
    recorded = json.loads(plan.FIDELITY_SAMPLE.read_text())["items"]
    asked = 0
    for t in design.tickets.values():
        if t["asked_by_F_f"] is not None:
            asked += 1
            if recorded.get(t["asked_by_F_f"], {}).get("digest") != t["digest"]:
                problems.append(f"{t['id']}: not the prompt F-f's Stage A recorded")
    for k in plan.RUNS:
        for i in design.pilot[k]:
            did = f"d{k}:{i}"
            if recorded.get(did, {}).get("digest") != design.items[did]["digest"]:
                problems.append(f"{did}: not the B prompt F-f's Stage A recorded")
    undefined = [d for d, x in design.decisions.items() if x["plurality"] is None]
    if undefined:
        problems.append(f"{len(undefined)} decisions have no plurality action")
    kinds = collections.Counter(i["kind"] for i in design.items.values())
    return {
        "what": ("every ticket-only prompt is v1's empty-base rendering, and the one "
                 "F-f asked where it asked one; every anchor prompt is F-f's B prompt, "
                 "rebuilt; the plurality is defined for every decision"),
        "prompts": dict(kinds),
        "tickets_asked_by_F_f": asked,
        "first_problems": problems[:10],
        "passes": not problems,
    }


# ---------------------------------------------------------------------------
# V-g3: the populations are §0's
# ---------------------------------------------------------------------------

def gate_vg3(design: Design, bases: dict[int, dict[str, dict]]) -> dict[str, Any]:
    problems = []
    per_run = {}
    fid = design.fidelity
    asked = {t["id"] for t in design.tickets.values() if t["asked_by_F_f"] is not None}
    for k in plan.RUNS:
        rows = fid.runs[k]["records"]
        if (design.pilot[k] != list(fid.draw[k]["uniform"][:plan.PILOT_PER_RUN])
                or len(design.pilot[k]) != plan.PILOT_PER_RUN):
            problems.append(f"run {k}: the pilot is not the first "
                            f"{plan.PILOT_PER_RUN} of the draw")
        held = design.held_out[k]
        if len(held) != plan.HELD_OUT_SIZES[k]:
            problems.append(f"run {k}: {len(held)} held-out decisions, §0 says "
                            f"{plan.HELD_OUT_SIZES[k]}")
        if any(design.ticket_of(k, i) in asked for i in held):
            problems.append(f"run {k}: a held-out decision is on a ticket F-f asked")
        if any(rows[i]["outcome"] != "ACTION" for i in held):
            problems.append(f"run {k}: a held-out case is not a decision")
        if any(not design.decisions[f"d{k}:{i}"]["shown_ids"] for i in held):
            problems.append(f"run {k}: a held-out screen shows no rule")
        lacking = sum(1 for i in held
                      if fidelity_score.valid_pair(bases.get(k, {}).get(f"d{k}:{i}",
                                                   {"answers": {}})) is None)
        share = lacking / len(held) if held else 1.0
        if share > plan.MAX_INVALID_SHARE:
            problems.append(f"run {k}: {lacking} held-out decisions lack two valid "
                            "answers with the screen")
        per_run[f"run{k}"] = {"pilot": len(design.pilot[k]), "held_out": len(held),
                              "held_out_lacking_two_answers_with_the_screen": lacking}
    if len(design.tickets) != plan.TICKETS:
        problems.append(f"{len(design.tickets)} tickets, §0 says {plan.TICKETS}")
    if len(asked) != plan.ASKED_BY_F_F:
        problems.append(f"{len(asked)} of the tickets were asked by F-f, §0 says "
                        f"{plan.ASKED_BY_F_F}")
    to = design.sessions["ticket_only"]
    if (len(to["passes"]) != plan.TICKET_ONLY_DRAWS
            or any(sorted(p) != sorted(design.tickets) for p in to["passes"])):
        problems.append("the ticket-only session does not ask every ticket in each pass")
    anchor = design.sessions["anchor"]
    pilot_ids = sorted(f"d{k}:{i}" for k in plan.RUNS for i in design.pilot[k])
    if (len(anchor["passes"]) != plan.ANCHOR_DRAWS
            or any(sorted(p) != pilot_ids for p in anchor["passes"])):
        problems.append("the anchor does not ask the pilot's B prompts once")
    smoke = design.sessions["smoke"]["items"]
    if collections.Counter(design.items[i]["kind"] for i in smoke) != {
            TICKET_ONLY: plan.SMOKE_PER_ARM, HIDDEN: plan.SMOKE_PER_ARM}:
        problems.append("the smoke run is not five of each arm")
    return {
        "what": ("the pilot is the first 100 of each draw; the held-out decisions are "
                 "§0's, on tickets F-f never asked, each with a screen and at most 5% "
                 "without two valid answers with it; the tickets are §0's; and each "
                 "session asks what §1 says"),
        "per_run": per_run,
        "tickets": len(design.tickets),
        "tickets_asked_by_F_f": len(asked),
        "first_problems": problems[:10],
        "passes": not problems,
    }


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

@dataclass
class Checks:
    vg1: dict
    vg2: dict
    vg3: dict
    vg4: dict
    design: Design = field(repr=False)
    found: dict = field(default_factory=dict, repr=False)

    @property
    def blocking_pass(self) -> bool:
        return self.vg1["passes"] and self.vg2["passes"] and self.vg3["passes"]

    def summary(self) -> dict[str, Any]:
        """What a record carries about the checks it was written behind."""
        return {"V-g1": self.vg1, "V-g2": self.vg2, "V-g3": self.vg3,
                "V-g4": self.vg4}


def run_checks(suite: bool = True) -> Checks:
    fid_checks = fidelity_sample.run_checks(suite=False)
    found, missing = load_fidelity_sessions()
    design = build_design(fid_checks.design)
    return Checks(vg1=gate_vg1(fid_checks, found, missing, suite=suite),
                  vg2=gate_vg2(design),
                  vg3=gate_vg3(design, fidelity_bases(found)),
                  vg4=plan.gate_signature(), design=design, found=found)


def report(c: Checks) -> None:
    """Pass or fail, and only counts §0 already states: nothing of `V-e`."""
    mark = {True: "PASS", False: "FAIL"}
    print("=" * 78)
    print(f"{plan.PLAN} — blocking checks (§6), zero API calls")
    print("=" * 78)
    t = c.vg1["suite"]
    print(f"  V-g1  {mark[c.vg1['passes']]}  the inputs reproduce themselves: "
          f"PLAN_FIDELITY.md's F-g1..F-g3 {c.vg1['fidelity_checks']}")
    print("              test suite: " + (
        f"{t['tests']} tests, {t['result']} ({t['seconds']} s)" if t["ran"]
        else "not run here"))
    for p in c.vg1["first_problems"][:5]:
        print(f"              {p}")
    print(f"  V-g2  {mark[c.vg2['passes']]}  the prompts are PLAN_FIDELITY.md's "
          f"({', '.join(f'{v} {k}' for k, v in sorted(c.vg2['prompts'].items()))}; "
          f"{c.vg2['tickets_asked_by_F_f']} tickets F-f asked)")
    for p in c.vg2["first_problems"][:5]:
        print(f"              {p}")
    sizes = ", ".join(str(r["held_out"]) for r in c.vg3["per_run"].values())
    print(f"  V-g3  {mark[c.vg3['passes']]}  the populations are §0's: held out "
          f"{sizes}; {c.vg3['tickets']} tickets")
    for p in c.vg3["first_problems"][:5]:
        print(f"              {p}")
    g = c.vg4
    print(f"  V-g4  {'SIGNED' if g['passes'] else 'UNSIGNED'}  {g['found']} "
          f"signature line(s), {g['unsigned']} blank"
          + ("" if g["passes"] else " — nothing may be written or spent"))
    print(f"\n  blocking checks: {'ALL PASS' if c.blocking_pass else 'FAILED'}")


# ---------------------------------------------------------------------------
# The readout: V-e's free half
# ---------------------------------------------------------------------------

def _mean(xs: list[float]) -> float | None:
    return sum(xs) / len(xs) if xs else None


def _se(xs: list[float]) -> float | None:
    return statistics.stdev(xs) / math.sqrt(len(xs)) if len(xs) > 1 else None


def pilot_pairs(design: Design, found: dict[str, dict]) -> list[dict]:
    """Each pilot decision with F-f's one answer without a screen (`t`, asked on
    2026-10-03), its two with it, its labels and its screen. The pairing is
    F-f's own: a ticket-only item serves the decisions with its key."""
    old = fidelity_score.group(found["ticket_only"]["rows"])
    bases = fidelity_bases(found)
    out = []
    for k in plan.RUNS:
        for i in design.pilot[k]:
            d = design.decisions[f"d{k}:{i}"]
            f_id = design.tickets[d["ticket"]]["asked_by_F_f"]
            t = old.get(f_id, {}).get("answers", {}).get(1)
            b = bases[k].get(d["id"])
            if t is None or b is None or b["answers"].get(1) is None:
                continue
            out.append({"run": k, "y": b["labels"]["truth"],
                        "rule": b["labels"]["rule_action"], "t": t,
                        "b1": b["answers"].get(1), "b2": b["answers"].get(2),
                        "p": d["plurality"], "shown": set(d["shown_actions"])})
    return out


def read_pilot(pairs: list[dict]) -> dict[str, Any]:
    """§0's *already seen*, measured: the drafter's probe, owned here."""
    def block(ps: list[dict]) -> dict[str, Any]:
        def acc(field_: str) -> float | None:
            return _mean([1.0 if p[field_] == p["y"] else 0.0 for p in ps])

        def b_mean(p: dict) -> float:
            bs = [b for b in (p["b1"], p["b2"]) if b is not None]
            return sum(b == p["y"] for b in bs) / len(bs)

        net = [(1.0 if p["t"] == p["y"] else 0.0) - b_mean(p) for p in ps]
        right = [p for p in ps if p["p"] == p["y"]]
        wrong = [p for p in ps if p["p"] != p["y"]]
        off = [p for p in ps if p["t"] != p["p"]]
        on = [p for p in ps if p["t"] == p["p"]]
        both = [p for p in ps if p["b2"] is not None]
        return {
            "decisions": len(ps),
            "without_screen_accuracy": acc("t"),
            "with_screen_accuracy_mean_of_two": _mean([b_mean(p) for p in ps]),
            "with_screen_first_answer_accuracy": acc("b1"),
            "net": _mean(net), "net_standard_error": _se(net),
            "t_alone_right": sum(1 for p in ps if p["t"] == p["y"] != p["b1"]),
            "b1_alone_right": sum(1 for p in ps if p["b1"] == p["y"] != p["t"]),
            "plurality_is_the_true_queue": _mean([1.0 if p["p"] == p["y"] else 0.0
                                                  for p in ps]),
            "where_plurality_right": {
                "n": len(right),
                "b1_minus_t": _mean([(p["b1"] == p["y"]) - (p["t"] == p["y"])
                                     for p in right])},
            "where_plurality_wrong": {
                "n": len(wrong),
                "t_minus_b1": _mean([(p["t"] == p["y"]) - (p["b1"] == p["y"])
                                     for p in wrong])},
            "pull": {"where_t_is_not_p": {"n": len(off), "b1_is_p": _mean(
                         [1.0 if p["b1"] == p["p"] else 0.0 for p in off])},
                     "where_t_is_p": {"n": len(on), "b1_is_p": _mean(
                         [1.0 if p["b1"] == p["p"] else 0.0 for p in on])}},
            "agreement": {
                "b1_b2": _mean([1.0 if p["b1"] == p["b2"] else 0.0 for p in both]),
                "t_b1": _mean([1.0 if p["t"] == p["b1"] else 0.0 for p in ps]),
                "t_rule": _mean([1.0 if p["t"] == p["rule"] else 0.0 for p in ps]),
                "b1_rule": _mean([1.0 if p["b1"] == p["rule"] else 0.0 for p in ps])},
            "b1_is_a_shown_action": _mean([1.0 if p["b1"] in p["shown"] else 0.0
                                           for p in ps]),
            "t_is_a_shown_action": _mean([1.0 if p["t"] in p["shown"] else 0.0
                                          for p in ps]),
            "true_queue_shown": sum(1 for p in ps if p["y"] in p["shown"]),
        }

    by_queue = collections.defaultdict(list)
    for p in pairs:
        by_queue[p["y"]].append(p)
    return {
        "per_run": {f"run{k}": block([p for p in pairs if p["run"] == k])
                    for k in plan.RUNS},
        "pooled": block(pairs),
        "by_true_queue": {
            q: {"decisions": len(ps),
                "t_accuracy": _mean([1.0 if p["t"] == q else 0.0 for p in ps]),
                "b1_accuracy": _mean([1.0 if p["b1"] == q else 0.0 for p in ps])}
            for q, ps in sorted(by_queue.items(), key=lambda kv: -len(kv[1]))},
    }


def read_held_out(design: Design, found: dict[str, dict]) -> dict[str, Any]:
    """What the held-out decisions are, without a single new answer."""
    bases = fidelity_bases(found)
    out = {}
    for k in plan.RUNS:
        held = [bases[k][f"d{k}:{i}"] for i in design.held_out[k]
                if f"d{k}:{i}" in bases[k]]
        right = sum(1 for e in held
                    if design.decisions[e["id"]]["plurality"] == e["labels"]["truth"])
        drawn = [bases[k][f"d{k}:{i}"] for i in design.fidelity.draw[k]["uniform"]
                 if f"d{k}:{i}" in bases[k]]
        out[f"run{k}"] = {
            "decisions": len(held),
            "plurality_is_the_true_queue": right / len(held) if held else None,
            "copier_accuracy": right / len(held) if held else None,
            "V-d_cells": {"plurality_right": right, "plurality_wrong": len(held) - right},
            "class_mix": dict(collections.Counter(e["labels"]["truth"] for e in held)),
            "class_mix_of_the_whole_draw": dict(collections.Counter(
                e["labels"]["truth"] for e in drawn)),
        }
    return out


def readout(design: Design, found: dict[str, dict]) -> dict[str, Any]:
    return {"pilot": read_pilot(pilot_pairs(design, found)),
            "held_out": read_held_out(design, found)}


def payload(checks: Checks) -> dict[str, Any]:
    d = checks.design
    return {
        "_env": environment(seed=plan.SEED),
        "plan": str(plan.PLAN),
        "stage": "A",
        "row": "V-e, its free half",
        "provenance": ("POST-SIGNATURE, REPORTED: written after §0 was signed. The "
                       "pilot's readout reproduces the drafter's scratch figures, "
                       "which §0 declares as already seen; this record now owns "
                       "them. The held-out readout was computed here for the first "
                       "time"),
        "surface": ("corpus — seed 17, n=2000, in arrival order: the decided cases of "
                    "PLAN_REUSE.md's three Stage B runs, as PLAN_FIDELITY.md drew them"),
        "inputs": {name: {"path": str(p), "sha256": sha256(p)}
                   for name, p in input_paths().items()},
        "gates": checks.summary(),
        "protocol": {"model": plan.MODEL, "prompt_version": plan.PROMPT,
                     "reasoning": plan.REASONING, "pilot_per_run": plan.PILOT_PER_RUN,
                     "ticket_only_draws": plan.TICKET_ONLY_DRAWS,
                     "anchor_draws": plan.ANCHOR_DRAWS,
                     "smoke_per_arm": plan.SMOKE_PER_ARM, "order_seed": plan.ORDER_SEED},
        "pilot": {f"run{k}": v for k, v in d.pilot.items()},
        "held_out": {f"run{k}": v for k, v in d.held_out.items()},
        "decisions": d.decisions,
        "tickets": d.tickets,
        "sessions": d.sessions,
        "items": {i: {"kind": it["kind"], "digest": it["digest"]}
                  for i, it in d.items.items()},
        "readout": readout(d, checks.found),
    }


def show(out: dict) -> None:
    p = out["readout"]["pilot"]["pooled"]
    print(f"\nthe pilot, pooled ({p['decisions']} decisions): without the screen "
          f"{p['without_screen_accuracy']:.4f}, with it "
          f"{p['with_screen_accuracy_mean_of_two']:.4f}, net {p['net']:+.4f}")
    for name, r in out["readout"]["held_out"].items():
        print(f"held out, {name}: {r['decisions']} decisions, plurality right on "
              f"{r['plurality_is_the_true_queue']:.4f}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage A of PLAN_SCREEN.md: the checks, the populations, the readout.")
    ap.add_argument("--dry-run", action="store_true",
                    help="run V-g1 to V-g4; write nothing and show nothing of V-e")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = run_checks(suite=True)
        report(checks)
        print("\ndry run: nothing written, and nothing of V-e computed for display")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"screen/sample.py writes {plan.SAMPLE_PATH}")
    checks = run_checks(suite=True)
    report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    out = payload(checks)
    show(out)
    plan.OUT.mkdir(exist_ok=True)
    plan.SAMPLE_PATH.write_text(json.dumps(out, indent=2))
    print(f"\n-> {plan.SAMPLE_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
