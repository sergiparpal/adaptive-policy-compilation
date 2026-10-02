"""
Stage A of `PLAN_FIDELITY.md`: the blocking checks, the draw and the free
readout. It spends nothing and asks nothing.

THE CHECKS (§6). All are blocking, and the paid stage runs them again before any
call.

  F-g1  The inputs reproduce themselves. The suite is green, and each Stage B
        record passes PLAN_REUSE.md's own check, `reuse.gates.check_record`,
        against the labels the frozen loop writes. No module here imports the
        oracle.
  F-g2  The replay is exact (`fidelity/replay.py`).
  F-g3  The prompts and the draw are what §2 signs.
        * A B screen holds no rule that matches its ticket, carries v1's
          coverage header and never shows the deciding rule.
        * A ticket-only prompt is the empty-base rendering.
        * The draw has PER_RUN distinct decided cases per run.
        * The census holds every rare-class decision of each run.
        * The smoke run asks at least one birth on a conflict screen.
        That every birth prompt is what the loop sent is checked in
        `tests/test_fidelity.py`, against the requests rung 2's loop builds
        when `tests/doubles.py` replays the four v1 n=100 records, and F-g1's
        suite runs that test. F-d's population is reported here too: a run
        whose draw holds fewer than MIN_SILENT_ERRORS silent errors makes F-d
        unadjudicable before a call is made, as §6 says. It does not block
        the other rows.
  F-g4  The signature (`fidelity/plan.py`).

THE DRAW (§2.3). Each run's decided cases are sampled uniformly, without
replacement, PER_RUN of them, on that run's own stream. Every decision whose
true queue is ONCALL_ESCALATION or SECURITY_INCIDENT joins as a census. The
labels come off the Stage B records and are used only to choose the census
and to count, never to build a prompt.

THE SESSIONS (§8): smoke, births, base1 to base3, ticket_only. Each session's
items are listed once, and each pass is its own seeded order over them. The
ticket-only arm asks the distinct tickets of the first TICKET_ONLY_PER_RUN of
each run's draw once, and the 27 rare-class tickets twice. Its prompt depends
on the ticket alone. Every item carries the digest of its prompt, and
`fidelity/ask.py` rebuilds every prompt and refuses if one differs.

THE READOUT, `F-f`'s free half (§7). Every figure §0 of the plan lists as
*already seen*, measured by this module so that this record owns it. Beside
them are the two free baselines for the B arm: the screen's plurality action
and its first rule's action, with each one's agreement with the deciding rule
and its accuracy. Nobody had computed those accuracies before this ran.

    python3 -m fidelity.sample --dry-run     # F-g1..F-g4; writes nothing
    python3 -m fidelity.sample               # refuses while PLAN_FIDELITY.md is unsigned
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from harness.domain import generate_corpus
from harness.dsl import RuleEngine
from harness.proposers import KeepKProposer
from harness.provenance import describe, environment
from harness.shadow import run_shadow

from reuse import analysis as reuse_analysis
from reuse import frontier as reuse_frontier
from reuse import gates as reuse_gates
from reuse import plan as reuse_plan
from rung2.engine2 import Space
from rung2.proposers2 import neighbourhood

from . import plan, prompts, replay

RUNG1 = Path("results/llm_run.json")
SMOKES = "run_n20_smoke*.json"            # PLAN_REUSE.md's four smoke records
PACE = {"stage_d": Path("results2/pair_judgement_learned.json"),
        "extension_1600": Path("results2/pair_judgement_1600.json")}


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------

def load_runs() -> dict[int, dict]:
    return {k: json.loads(plan.run_path(k).read_text()) for k in plan.RUNS}


def truth_labels(corpus) -> list[tuple[str, str]]:
    """What the frozen loop labels each case of the corpus, read off its own
    records, as `reuse/frontier.py` reads them. This module never touches the
    oracle."""
    return reuse_frontier.truth_sequence(
        run_shadow(corpus, RuleEngine(), KeepKProposer(1)))


# ---------------------------------------------------------------------------
# F-g1, F-g2
# ---------------------------------------------------------------------------

def gate_fg1(runs: dict[int, dict], truth, suite: bool = True) -> dict[str, Any]:
    rows = {}
    for k, rec in runs.items():
        problems = reuse_gates.check_record(rec, n=plan.N, seed=plan.SEED,
                                            prompt=plan.PROMPT, truth=truth)
        for key, want in (("model", plan.MODEL), ("reasoning", plan.REASONING)):
            if rec.get(key) != want:
                problems.append(f"{key} {rec.get(key)!r}: Stage B's is {want!r}")
        rows[f"run{k}"] = {"problems": problems[:10], "passes": not problems}
    tests = reuse_gates.run_suite() if suite else {"ran": False, "passes": None}
    return {
        "what": ("the suite is green, and each Stage B record reproduces its own "
                 "metrics, fire counts, births and corpus labels, under Stage B's "
                 "model and reasoning setting"),
        "records": rows,
        "suite": tests,
        "passes": all(r["passes"] for r in rows.values())
                  and tests["passes"] is not False,
    }


def gate_fg2(runs: dict[int, dict], corpus, space: Space) -> dict[str, Any]:
    rows = {f"run{k}": replay.check(rec, corpus, space) for k, rec in runs.items()}
    return {"what": ("each run rebuilt case by case from its record alone "
                     "reproduces every decision, screen, edge verdict and final "
                     "count, and its system prompt is v1's"),
            "runs": rows, "passes": all(r["passes"] for r in rows.values())}


# ---------------------------------------------------------------------------
# The draw, the items and the sessions
# ---------------------------------------------------------------------------

@dataclass
class Design:
    runs: dict[int, dict]
    corpus: list
    space: Space
    draw: dict[int, dict]
    sessions: dict[str, dict]
    items: dict[str, dict]                    # by item id
    prompts: dict[str, prompts.Prompt] = field(repr=False)
    problems: list[str] = field(default_factory=list)


def draw_run(k: int, rec: dict) -> dict[str, Any]:
    decided = [r["idx"] for r in rec["records"] if r["outcome"] == "ACTION"]
    census = {q: [r["idx"] for r in rec["records"]
                  if r["outcome"] == "ACTION" and r["truth"] == q] for q in plan.RARE}
    return {"population": len(decided),
            "uniform": plan.sample_rng(k).sample(decided, plan.PER_RUN),
            "census": census}


def session(name: str, ids: list[str], second: list[str]) -> dict[str, Any]:
    """One session: its items once, and each pass its own seeded order."""
    first = list(ids)
    plan.order_rng(name, 1).shuffle(first)
    passes = [first]
    if second:
        again = list(second)
        plan.order_rng(name, 2).shuffle(again)
        passes.append(again)
    return {"items": list(ids), "passes": passes}


def build_design(runs: dict[int, dict], corpus, space: Space) -> Design:
    draw = {k: draw_run(k, rec) for k, rec in runs.items()}
    items: dict[str, dict] = {}
    built: dict[str, prompts.Prompt] = {}
    problems: list[str] = []
    births: list[str] = []
    bases: dict[int, list[str]] = {}

    for k, rec in runs.items():
        uniform = set(draw[k]["uniform"])
        census = {i: q for q, idxs in draw[k]["census"].items() for i in idxs}
        bases[k] = []
        for m in replay.Replay(rec, corpus, space).moments():
            if m.outcome == "ACTION" and (m.idx in uniform or m.idx in census):
                p = prompts.hidden(m.engine, m.case)
                problems += [f"run {k}, case {m.idx}: {x}"
                             for x in prompts.check_hidden(p, m.engine, m.winner.rule_id)]
                iid = f"d{k}:{m.idx}"
                items[iid] = {"id": iid, "kind": prompts.HIDDEN, "run": k, "idx": m.idx,
                              "uniform": m.idx in uniform, "census": census.get(m.idx),
                              "screen": p.screen, "shown_ids": list(p.shown_ids),
                              "digest": p.digest}
                built[iid] = p
                bases[k].append(iid)
            elif m.outcome != "ACTION" and m.row.get("escalated"):
                p = prompts.birth(m.engine, m.case, m.undefeated)
                iid = f"b{k}:{m.idx}"
                items[iid] = {"id": iid, "kind": prompts.BIRTH, "run": k, "idx": m.idx,
                              "screen": p.screen, "shown_ids": list(p.shown_ids),
                              "digest": p.digest}
                built[iid] = p
                births.append(iid)
        missing = sorted((set(draw[k]["uniform"]) | set(census))
                         - {items[i]["idx"] for i in bases[k]})
        if missing:
            problems.append(f"run {k}: {len(missing)} drawn cases found no moment")

    # The ticket-only arm: distinct tickets, a prompt per ticket (§2.1, C).
    tickets: dict[tuple, dict] = {}

    def ticket(idx: int) -> dict:
        key = corpus[idx].key()
        if key not in tickets:
            tickets[key] = {"id": f"t:{idx}", "kind": prompts.TICKET_ONLY,
                            "run": None, "idx": idx, "sources": [], "rare": None}
        return tickets[key]

    for k in runs:
        for idx in draw[k]["uniform"][:plan.TICKET_ONLY_PER_RUN]:
            ticket(idx)["sources"].append([k, idx])
    for r in runs[plan.RUNS[0]]["records"]:
        if r["truth"] in plan.RARE:
            ticket(r["idx"])["rare"] = r["truth"]
    for t in tickets.values():
        p = prompts.ticket_only(corpus[t["idx"]])
        problems += [f"ticket {t['idx']}: {x}" for x in prompts.check_ticket_only(p)]
        t["digest"] = p.digest
        items[t["id"]] = t
        built[t["id"]] = p

    sessions = {"births": session("births", births, births)}
    for k in runs:
        sessions[f"base{k}"] = session(f"base{k}", bases[k], bases[k])
    t_ids = [t["id"] for t in tickets.values()]
    sessions["ticket_only"] = session("ticket_only", t_ids,
                                      [i for i in t_ids if items[i]["rare"]])
    sessions["smoke"] = smoke_session(sessions, items)
    return Design(runs=runs, corpus=corpus, space=space, draw=draw,
                  sessions=sessions, items=items, prompts=built, problems=problems)


def smoke_session(sessions: dict[str, dict], items: dict[str, dict]) -> dict:
    """§8: five items of each arm once, at least one a birth on a conflict
    screen. The first five of each arm's first pass, in the order the session
    itself would ask them."""
    n = plan.SMOKE_PER_ARM
    births = sessions["births"]["passes"][0]
    first = births[:n]
    if not any(items[i]["screen"] == prompts.CONFLICT for i in first):
        conflict = next((i for i in births if items[i]["screen"] == prompts.CONFLICT), None)
        if conflict is not None:
            first = first[:-1] + [conflict]
    ids = (first + sessions["base1"]["passes"][0][:n]
           + sessions["ticket_only"]["passes"][0][:n])
    return {"items": ids, "passes": [ids]}


def gate_fg3(design: Design) -> dict[str, Any]:
    problems = list(design.problems)
    populations = {}
    for k, d in design.draw.items():
        uniform = d["uniform"]
        rows = design.runs[k]["records"]
        if len(set(uniform)) != plan.PER_RUN or any(rows[i]["outcome"] != "ACTION"
                                                    for i in uniform):
            problems.append(f"run {k}: the draw is not {plan.PER_RUN} distinct "
                            "decided cases")
        census_items = {design.items[i]["idx"] for i in design.sessions[f"base{k}"]["items"]
                        if design.items[i]["census"]}
        every = {r["idx"] for r in rows
                 if r["outcome"] == "ACTION" and r["truth"] in plan.RARE}
        if census_items != every:
            problems.append(f"run {k}: the census misses rare-class decisions")
        populations[f"run{k}"] = {
            "silent_errors_in_draw": sum(1 for i in uniform if not rows[i]["correct"]),
            "oncall_census": len(d["census"][plan.ONCALL]),
        }
    smoke = design.sessions["smoke"]["items"]
    if not any(design.items[i]["kind"] == prompts.BIRTH
               and design.items[i]["screen"] == prompts.CONFLICT for i in smoke):
        problems.append("the smoke run asks no birth on a conflict screen")
    f_d_ok = all(p["silent_errors_in_draw"] >= plan.MIN_SILENT_ERRORS
                 for p in populations.values())
    kinds = collections.Counter(i["kind"] for i in design.items.values())
    return {
        "what": ("no B screen shows a rule matching its ticket or the deciding rule, "
                 "and each carries v1's coverage header; ticket-only prompts are the "
                 "empty-base rendering; the draw, the census and the smoke run are "
                 "what §2 and §8 sign"),
        "prompts": dict(kinds),
        "first_problems": problems[:10],
        "F-d_population": {"per_run": populations,
                           "minimum": plan.MIN_SILENT_ERRORS,
                           "F-d_adjudicable": f_d_ok},
        "passes": not problems,
    }


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

@dataclass
class Checks:
    fg1: dict
    fg2: dict
    fg3: dict
    fg4: dict
    design: Design = field(repr=False)

    @property
    def blocking_pass(self) -> bool:
        return self.fg1["passes"] and self.fg2["passes"] and self.fg3["passes"]

    def summary(self) -> dict[str, Any]:
        """What a record carries about the checks it was written behind."""
        return {"F-g1": self.fg1, "F-g2": self.fg2, "F-g3": self.fg3,
                "F-g4": self.fg4}


def run_checks(suite: bool = True) -> Checks:
    runs = load_runs()
    corpus = generate_corpus(plan.N, seed=plan.SEED)
    space = Space()
    fg1 = gate_fg1(runs, truth_labels(corpus), suite=suite)
    fg2 = gate_fg2(runs, corpus, space)
    design = build_design(runs, corpus, space)
    return Checks(fg1=fg1, fg2=fg2, fg3=gate_fg3(design),
                  fg4=plan.gate_signature(), design=design)


def report(c: Checks) -> None:
    """Pass or fail, and only figures already published: nothing of `F-f`."""
    mark = {True: "PASS", False: "FAIL"}
    print("=" * 78)
    print(f"{plan.PLAN} — blocking checks (§6), zero API calls")
    print("=" * 78)
    ok = sum(1 for r in c.fg1["records"].values() if r["passes"])
    t = c.fg1["suite"]
    print(f"  F-g1  {mark[c.fg1['passes']]}  the Stage B records reproduce "
          f"themselves: {ok} of {len(c.fg1['records'])}")
    print("              test suite: " + (
        f"{t['tests']} tests, {t['result']} ({t['seconds']} s)" if t["ran"]
        else "not run here"))
    for name, r in c.fg1["records"].items():
        for p in r["problems"][:3]:
            print(f"              {name}: {p}")
    ok = sum(1 for r in c.fg2["runs"].values() if r["passes"])
    print(f"  F-g2  {mark[c.fg2['passes']]}  the replay is exact: {ok} of "
          f"{len(c.fg2['runs'])} runs")
    for name, r in c.fg2["runs"].items():
        for p in r["first_problems"][:3]:
            print(f"              {name}: {p}")
    print(f"  F-g3  {mark[c.fg3['passes']]}  prompts and draw as signed "
          f"({', '.join(f'{v} {k}' for k, v in sorted(c.fg3['prompts'].items()))})")
    for p in c.fg3["first_problems"][:5]:
        print(f"              {p}")
    if not c.fg3["F-d_population"]["F-d_adjudicable"]:
        print("              F-d is UNADJUDICABLE: a run's draw holds fewer than "
              f"{plan.MIN_SILENT_ERRORS} silent errors")
    g = c.fg4
    print(f"  F-g4  {'SIGNED' if g['passes'] else 'UNSIGNED'}  {g['found']} "
          f"signature line(s), {g['unsigned']} blank"
          + ("" if g["passes"] else " — nothing may be written or spent"))
    print(f"\n  blocking checks: {'ALL PASS' if c.blocking_pass else 'FAILED'}")


# ---------------------------------------------------------------------------
# The readout: F-f's free half
# ---------------------------------------------------------------------------

def _plurality_set(actions) -> set[str]:
    counts = collections.Counter(actions)
    top = max(counts.values())
    return {a for a, n in counts.items() if n == top}


def _cites(rules, ids_off_screen) -> bool:
    return any(e in ids_off_screen for r in rules for e in r.beats + r.loses_to)


def _share(top: list[int], total: int, k: int) -> float:
    return sum(top[:k]) / total if total else 0.0


def read_run(k: int, rec: dict, design: Design) -> dict[str, Any]:
    born, _ = reuse_analysis.births(rec)
    uniform = set(design.draw[k]["uniform"])
    screens = collections.Counter()
    births = collections.Counter()
    base = collections.Counter()
    cross = collections.Counter()
    deciders = collections.Counter()
    oncall, security_actions = [], collections.Counter()
    escalated_rare = {q: collections.Counter() for q in plan.RARE}
    chars_hidden, chars_birth = [], []

    for m in replay.Replay(rec, design.corpus, design.space).moments():
        row = m.row
        if m.outcome == "ACTION":
            w = m.winner
            screens["decided"] += 1
            deciders[w.rule_id] += 1
            matching = [r for r in m.engine.rules if r.matches(m.case)]
            # A: v1 as it stands
            shown, _ = neighbourhood(m.engine, m.case, [])
            ids = [r.rule_id for r in shown]
            screens["A_deciding_rule_shown"] += w.rule_id in ids
            screens["A_deciding_rule_first"] += bool(ids) and ids[0] == w.rule_id
            # B': only the deciding rule hidden
            shown, _ = neighbourhood(SimpleNamespace(
                rules=[r for r in m.engine.rules if r is not w]), m.case, [])
            still = [r for r in shown if r.matches(m.case)]
            screens["B'_another_matching_rule_shown"] += bool(still)
            screens["B'_one_with_the_deciding_action"] += any(
                r.action == w.action for r in still)
            # B: every matching rule hidden
            p = prompts.hidden(m.engine, m.case)
            chars_hidden.append(p.chars)
            hidden_ids = {r.rule_id for r in matching}
            by_id = {r.rule_id: r for r in m.engine.rules}
            on_screen = [by_id[i] for i in p.shown_ids]
            screens["B_screen_empty"] += not p.shown_ids
            screens["B_some_shown_rule_has_the_deciding_action"] += (
                w.action in p.shown_actions)
            screens["B_deciding_action_is_a_plurality_action"] += bool(
                p.shown_actions) and w.action in _plurality_set(p.shown_actions)
            screens["B_a_shown_rule_cites_a_hidden_rule"] += _cites(on_screen, hidden_ids)
            # the uniform draw: the two free baselines
            if m.idx in uniform:
                r_, y = row["predicted"], row["truth"]
                base["n"] += 1
                for name, guess in (("plurality", prompts.plurality(p)),
                                    ("first_shown", prompts.first_shown(p))):
                    base[f"{name}_agrees_with_rule"] += guess == r_
                    base[f"{name}_right"] += guess == y
                base["rule_right"] += r_ == y
            # births crossed with outcome: U-c's split, recomputed
            b = "born_right" if born[w.rule_id]["proposal_action_correct"] else "born_wrong"
            cross[f"{b}, rule_{'right' if row['correct'] else 'wrong'}"] += 1
            if row["truth"] == plan.ONCALL:
                d = next(x for x in rec["rules"] if x["rule_id"] == w.rule_id)
                oncall.append({"idx": m.idx, "truth_rule": row["truth_rule"],
                               "ticket": m.case.as_dict(), "rule": w.rule_id,
                               "action": w.action, "born_at": d["born_at"],
                               "conditions": [f"{c['attr']} {c['op']} {c['value']}"
                                              for c in d["conditions"]]})
            elif row["truth"] == plan.SECURITY:
                security_actions[w.action] += 1
        elif row.get("escalated"):
            p = prompts.birth(m.engine, m.case, m.undefeated)
            chars_birth.append(p.chars)
            if row["truth"] in plan.RARE:
                escalated_rare[row["truth"]][row["predicted"]] += 1
            births["births"] += 1
            if not p.shown_ids:
                births["empty_screen"] += 1
                continue
            s = p.screen
            births[f"{s}_screens"] += 1
            births[f"{s}_answer_was_a_shown_action"] += row["predicted"] in p.shown_actions
            births[f"{s}_answer_was_a_plurality_action"] += (
                row["predicted"] in _plurality_set(p.shown_actions))
            births[f"{s}_answer_right"] += bool(row["proposal_action_correct"])
            by_id = {r.rule_id: r for r in m.engine.rules}
            off = {r.rule_id for r in m.engine.rules} - set(p.shown_ids)
            births["a_shown_rule_cites_an_unshown_rule"] += _cites(
                [by_id[i] for i in p.shown_ids], off)

    top = sorted(deciders.values(), reverse=True)
    total = sum(top)
    cumulative, needed = 0, {}
    for i, n in enumerate(top, 1):
        cumulative += n
        for frac in (0.5, 0.8):
            if f"{frac}" not in needed and cumulative >= frac * total:
                needed[f"{frac}"] = i
    return {
        "decided": screens["decided"],
        "screens": dict(screens),
        "births": dict(births),
        "baselines_on_the_draw": dict(base),
        "decisions_by_birth_and_outcome": dict(cross),
        "concentration": {"deciding_rules": len(deciders),
                          "rules_for_half": needed.get("0.5"),
                          "rules_for_four_fifths": needed.get("0.8"),
                          "top_five_share": round(_share(top, total, 5), 4)},
        "ONCALL_decisions": oncall,
        "SECURITY_decisions_by_rule_action": dict(security_actions),
        "rare_escalations_by_answer": {q: dict(c) for q, c in escalated_rare.items()},
        "median_chars": {"hidden": statistics.median(chars_hidden),
                         "birth": statistics.median(chars_birth)},
    }


def named_oncall() -> dict[str, dict]:
    """§0: no Stage B run, smoke run or August n=100 run named the queue; rung 1
    did. Escalations whose answer named ONCALL_ESCALATION, per record."""
    paths = ([plan.run_path(k) for k in plan.RUNS]
             + sorted(plan.run_path(1).parent.glob(SMOKES))
             + [p for _, _, p in reuse_plan.EIGHT] + [RUNG1])
    out = {}
    for path in paths:
        esc = [r for r in json.loads(path.read_text())["records"] if r.get("escalated")]
        named = [r for r in esc if r.get("predicted") == plan.ONCALL]
        out[str(path)] = {"escalations": len(esc), "named_ONCALL": len(named),
                          "true_queue_when_named": dict(collections.Counter(
                              r["truth"] for r in named))}
    return out


def rung1_severity_one(corpus, runs: dict[int, dict]) -> dict[str, Any]:
    """Rung 1's escalations at severity 1, a different prompt with no base shown,
    and the one ticket it shares with Stage B's run 1."""
    esc = [r for r in json.loads(RUNG1.read_text())["records"]
           if r.get("escalated") and corpus[r["idx"]].severity == 1]
    named = [{"idx": r["idx"], "tier": corpus[r["idx"]].customer_tier,
              "truth": r["truth"]} for r in esc if r["predicted"] == plan.ONCALL]
    shared = {r["idx"] for r in esc} & {
        r["idx"] for r in runs[1]["records"]
        if r["escalated"] and corpus[r["idx"]].severity == 1
        and r["truth"] != plan.SECURITY}
    return {
        "escalations": len(esc),
        "answers": dict(collections.Counter(str(r["predicted"]) for r in esc)),
        "true_queues": dict(collections.Counter(r["truth"] for r in esc)),
        "named_ONCALL": named,
        "non_security_tickets_shared_with_stage_b_run1": [
            {"idx": i, "rung1": next(r["predicted"] for r in esc if r["idx"] == i),
             "stage_b_run1": runs[1]["records"][i]["predicted"],
             "truth": runs[1]["records"][i]["truth"]} for i in sorted(shared)],
    }


def pace(runs: dict[int, dict]) -> dict[str, Any]:
    """§1's table, off the records. For Stage B only `_env` timestamps exist:
    the gap between one record and the next bounds a run from above, checks
    and commits included."""
    out = {}
    for name, path in PACE.items():
        d = json.loads(path.read_text())
        calls = d.get("calls_made", len(d["answers"]))
        out[name] = {"record": str(path), "seconds": d["seconds"], "calls": calls,
                     "seconds_per_call": round(d["seconds"] / calls, 2)}
    stamps = [("smoke", json.loads(reuse_plan.SMOKE_PATH.read_text())["_env"]["recorded_at"])]
    stamps += [(f"run{k}", runs[k]["_env"]["recorded_at"]) for k in plan.RUNS]
    def when(stamp: str) -> datetime:
        return datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")

    bounds = {}
    for (_, a), (name, b) in zip(stamps, stamps[1:]):
        rec = runs[int(name[3:])]
        calls = rec["metrics"]["escalations"]
        span = (when(b) - when(a)).total_seconds()
        suite = rec["gates"]["U-g1"]["suite"]["seconds"]
        bounds[name] = {"seconds_since_previous_record": span, "calls": calls,
                        "its_suite_seconds": suite,
                        "at_most_seconds_per_call": round(span / calls, 1),
                        "at_most_without_its_suite": round((span - suite) / calls, 1)}
    out["stage_b"] = {"recorded_at": dict(stamps), "bounds": bounds}
    return out


def readout(design: Design) -> dict[str, Any]:
    per_run = {f"run{k}": read_run(k, rec, design) for k, rec in design.runs.items()}
    pooled: dict[str, int] = collections.Counter()
    for r in per_run.values():
        pooled.update({f"screens.{k}": v for k, v in r["screens"].items()})
        pooled.update({f"births.{k}": v for k, v in r["births"].items()})
        pooled.update({f"baselines.{k}": v for k, v in r["baselines_on_the_draw"].items()})
    return {
        "replay_without_edges": {
            f"run{k}": replay.check(rec, design.corpus, design.space,
                                    with_edges=False)["decisions_departing"]
            for k, rec in design.runs.items()},
        "per_run": per_run,
        "pooled": dict(sorted(pooled.items())),
        "named_ONCALL_at_escalations": named_oncall(),
        "rung1_at_severity_1": rung1_severity_one(design.corpus, design.runs),
        "pace_of_earlier_paid_sessions": pace(design.runs),
    }


def payload(checks: Checks) -> dict[str, Any]:
    d = checks.design
    return {
        "_env": environment(seed=plan.SEED),
        "plan": str(plan.PLAN),
        "stage": "A",
        "row": "F-f",
        "provenance": ("POST-SIGNATURE, REPORTED: written after §0 was signed. Part "
                       "of the readout reproduces the drafter's scratch figures, "
                       "which §0 declares as already seen. This record now owns "
                       "them. The baselines' accuracies were computed here for "
                       "the first time"),
        "surface": ("corpus — seed 17, n=2000, in arrival order: the cases of the "
                    "three Stage B records of PLAN_REUSE.md"),
        "inputs": [str(plan.run_path(k)) for k in plan.RUNS],
        "gates": checks.summary(),
        "protocol": {"model": plan.MODEL, "prompt_version": plan.PROMPT,
                     "reasoning": plan.REASONING, "draws": plan.DRAWS,
                     "per_run": plan.PER_RUN,
                     "ticket_only_per_run": plan.TICKET_ONLY_PER_RUN,
                     "smoke_per_arm": plan.SMOKE_PER_ARM,
                     "sample_seed": plan.SAMPLE_SEED, "order_seed": plan.ORDER_SEED},
        "draw": {f"run{k}": v for k, v in d.draw.items()},
        "sessions": d.sessions,
        "items": d.items,
        "readout": readout(d),
    }


def show(out: dict) -> None:
    r = out["readout"]
    p = r["pooled"]
    print(f"\nreplay without edges, decisions departing: {r['replay_without_edges']}")
    print(f"decided cases: {p['screens.decided']}")
    for key in ("A_deciding_rule_shown", "A_deciding_rule_first",
                "B'_another_matching_rule_shown", "B'_one_with_the_deciding_action",
                "B_some_shown_rule_has_the_deciding_action",
                "B_deciding_action_is_a_plurality_action",
                "B_a_shown_rule_cites_a_hidden_rule", "B_screen_empty"):
        print(f"  {key:<45}{p.get('screens.' + key, 0)}")
    n = p["baselines.n"]
    print(f"baselines on the draw (n={n}): rule right {p['baselines.rule_right']}, "
          f"plurality agrees {p['baselines.plurality_agrees_with_rule']} / right "
          f"{p['baselines.plurality_right']}, first shown agrees "
          f"{p['baselines.first_shown_agrees_with_rule']} / right "
          f"{p['baselines.first_shown_right']}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage A of PLAN_FIDELITY.md: the checks, the draw, the readout.")
    ap.add_argument("--dry-run", action="store_true",
                    help="run F-g1 to F-g4; write nothing and show nothing of F-f")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = run_checks(suite=True)
        report(checks)
        print("\ndry run: nothing written, and nothing of F-f computed for display")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"fidelity/sample.py writes {plan.SAMPLE_PATH}")
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
