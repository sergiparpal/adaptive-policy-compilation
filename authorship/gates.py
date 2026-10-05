"""
`E-g1` to `E-g4` of `PLAN_AUTHORSHIP.md` §7 — the blocking checks, all free.

They run before any record of the plan is written and before any call is made,
and **any failure stops the plan before a figure exists**. They are brought
forward to before signature, so that a failure becomes a fix to the draft and
not a signed amendment.

  E-g1  STOP 0, for the engine and for the declaration path. The hidden
        policy's 29 rules enter a fresh rung 2 engine one by one, each placing
        itself against the earlier ones through the loop's own
        `install_declarations`, which is how v1e installs a born rule's edges.
        The 199 edges must all be accepted, and the engine must execute the
        policy at 1.0000, with no silent error, CONFLICT or IMPASSE, on the
        corpus and over the space. And the suite is green.
  E-g2  The baseline reproduces. `reuse/structure.py`'s profile of each of
        `PLAN_REUSE.md`'s three final bases equals `results_reuse/structure.json`;
        each base rebuilt with its installed edges decides the corpus and the
        space exactly as `results_edges/score.json` publishes; and the shares
        and the nesting §0 declares come out of those figures to the digit §0
        gives them.
  E-g3  The loop and the validator do what §5 says, and nothing else. The
        labels the loop is handed agree across `PLAN_REUSE.md`'s records and
        rung 1's, and the smoke run's corpus is the head of the full one. With
        v1e off, each of the three runs replays through `authorship/loop.py`
        into its own record, case by case, rule by rule and verdict by
        verdict. With v1e on, the copy check refuses exactly the 44 later
        copies `structure.json` lists. And the v1e texts hash to the declared
        fingerprint.
  E-g4  The signature (`authorship/plan.py`). It blocks every write and every
        call, and not a dry run, which writes nothing.

**What a dry run prints is pass or fail, and figures the plan or a published
record already states.** No figure of Stage B or C exists to print.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from harness.ceiling_check import HIDDEN_DSL, all_cases
from harness.domain import generate_corpus
from harness.dsl import Condition

from fidelity.replay import rule_from
from reuse import structure as st
from reuse.gates import run_suite
from rung2.ceiling_check2_space import measure
from rung2.engine2 import (EDGE_CONTRADICTS, EDGE_CYCLE, EDGE_DISJOINT, EDGE_OK,
                           EDGE_SELF, EDGE_UNKNOWN, PriorityEngine, Rule2, Space)
from rung2.hidden_priority import build_hidden_engine
from rung2.proposers2 import ProposalError, neighbourhood, render_base_v1
from rung3.order_search import subsumption_below
from rung3.order_search_ls import space_truth_masks

from . import loop, plan
from . import protocol as p

VERDICTS = {EDGE_OK, EDGE_UNKNOWN, EDGE_DISJOINT, EDGE_SELF, EDGE_CONTRADICTS,
            EDGE_CYCLE}


# ---------------------------------------------------------------------------
# What the checks and Stage C share: the records, the labels, a final engine
# ---------------------------------------------------------------------------

def load(path: Path) -> dict:
    return json.loads(path.read_text())


def labels_of(record: dict) -> list[tuple[str, str]]:
    return [(r["truth"], r["truth_rule"]) for r in record["records"]]


def baseline_labels() -> list[tuple[str, str]]:
    """The labels the loop is handed: run 1's, which `E-g3` checks against the
    other two runs and rung 1's record of the same corpus."""
    return labels_of(load(plan.baseline_path(plan.BASELINE_REPS[0])))


def rebuild_final(record: dict, space: Space,
                  keep: set[str] | None = None) -> tuple[PriorityEngine, list[str]]:
    """A run's final engine: every rule, then every edge the engine accepted, in
    the order it accepted them, from the channels in `keep` (all, by default).
    A record without `edge_channels` is v1's, whose edges all came with a rule.
    Returns the engine and any accepted edge that did not re-install."""
    engine = PriorityEngine(space=space)
    for d in sorted(record["rules"], key=lambda r: r["born_at"]):
        engine.add(rule_from(d), born_at=d["born_at"], keep_id=True)
    log = record.get("edge_log") or []
    chans = record.get("edge_channels") or [p.WRITE] * len(log)
    problems = []
    for (w, l, why), ch in zip(log, chans):
        if why != EDGE_OK or (keep is not None and ch not in keep):
            continue
        got = engine.try_edge(w, l)
        if got != EDGE_OK:
            problems.append(f"{w} over {l} re-installed as {got}")
    return engine, problems


def on_space(engine: PriorityEngine, tmask: dict[str, int], n: int) -> dict[str, Any]:
    """The engine over the space by masks. A rule is undefeated at a point
    exactly where no rule that beats it, by subsumption or by an edge, matches;
    a point is decided when the undefeated rules there carry one queue. That is
    `PriorityEngine.decide`, point for point, and `E-g2` checks it against the
    case-by-case figures `results_edges/score.json` publishes."""
    undefeated = {}
    for r in engine.rules:
        dominated = 0
        for b in engine.beats_me(r.rule_id):
            dominated |= engine.ext[b]
        undefeated[r.rule_id] = engine.ext[r.rule_id] & ~dominated
    action = {r.rule_id: r.action for r in engine.rules}
    return st.subsumption_on_space(undefeated, action, tmask, n)


def on_corpus(engine: PriorityEngine, corpus, labels) -> dict[str, Any]:
    """The engine over the corpus, case by case, against the record's labels."""
    c, right = Counter(), 0
    for case, (truth, _) in zip(corpus, labels):
        outcome, winner, _ = engine.decide(case)
        if outcome == "ACTION":
            c["action"] += 1
            right += winner.action == truth
        else:
            c["conflict" if outcome == "CONFLICT" else "impasse"] += 1
    return st.arbitration(c, right, len(labels))


def share(with_edges: float, alone: float, bound: float) -> float | None:
    """E-c's statistic: what the edges add over subsumption alone, over what an
    order could add at most. Undefined where there is no room."""
    room = bound - alone
    return (with_edges - alone) / room if room > 0 else None


def distinct_nesting(rules: list[dict], space: Space) -> float | None:
    """Nested pairs over all pairs, among rules covering different tickets: the
    first-born of each extension stands for its copies (§0, E-a)."""
    ext = {r["rule_id"]: space.extension([Condition(c["attr"], c["op"], c["value"])
                                          for c in r["conditions"]]) for r in rules}
    seen, distinct = set(), []
    for r in sorted(rules, key=lambda r: (r["born_at"], r["rule_id"])):
        if ext[r["rule_id"]] in seen:
            continue
        seen.add(ext[r["rule_id"]])
        distinct.append(r)
    n = len(distinct)
    possible = n * (n - 1) // 2
    below = subsumption_below(distinct, ext)
    return sum(len(below[r["rule_id"]]) for r in distinct) / possible if possible else None


# ---------------------------------------------------------------------------
# E-g1
# ---------------------------------------------------------------------------

def gate_eg1(suite: bool = True) -> dict[str, Any]:
    space = Space()
    _ref, declared, _ = build_hidden_engine(space)
    winners_of = defaultdict(list)
    for w, l in declared:
        winners_of[l].append(w)
    engine = PriorityEngine(space=space)
    allowed = {rid for rid, _, _ in HIDDEN_DSL}
    channels: list[str] = []
    verdicts = Counter()
    for i, (rid, conds, action) in enumerate(HIDDEN_DSL):
        rule = Rule2(rule_id=rid, action=action,
                     conditions=[Condition(attr=a, op=o, value=v) for a, o, v in conds])
        engine.add(rule, born_at=i, keep_id=True)
        _n, _acc, reasons = loop.install_declarations(
            engine, rule, {"loses_to": winners_of[rid]}, allowed, p.WRITE, channels)
        verdicts.update(reasons)
    installed = sum(len(s) for s in engine.decl_below.values())
    surfaces = {}
    for name, cases in (("corpus", generate_corpus(plan.N, seed=plan.SEED)),
                        ("space", list(all_cases()))):
        m = measure(engine, cases, name, "hybrid, edges through v1e's path")
        surfaces[name] = {
            "e2e": m["accuracy_end_to_end"], "silent_errors": m["silent_errors_abs"],
            "conflict": m["conflict"], "impasse": m["impasse"],
            "passes": (m["accuracy_end_to_end"] == 1.0 and m["silent_errors_abs"] == 0
                       and m["conflict"] == 0 and m["impasse"] == 0)}
    tests = run_suite() if suite else {"ran": False, "passes": None}
    edges_ok = dict(verdicts) == {EDGE_OK: len(declared)} and installed == len(declared)
    return {
        "what": "the hidden policy, its 199 edges entered as v1e declarations, "
                "executed at 1.0000 on corpus and space; the suite green",
        "declared": len(declared), "installed": installed, "verdicts": dict(verdicts),
        "surfaces": surfaces, "suite": tests,
        "passes": edges_ok and all(s["passes"] for s in surfaces.values())
                  and tests["passes"] is not False,
    }


# ---------------------------------------------------------------------------
# E-g2
# ---------------------------------------------------------------------------

def gate_eg2() -> dict[str, Any]:
    corpus = generate_corpus(plan.N, seed=plan.SEED)
    space = Space()
    tmask = space_truth_masks(space)
    structure = load(plan.BASELINE_STRUCTURE)
    published = load(plan.BASELINE_EDGES)
    rows = []
    for k, rep in enumerate(plan.BASELINE_REPS):
        record = load(plan.baseline_path(rep))
        labels = labels_of(record)
        profile = st.profile(st.from_record(plan.baseline_path(rep)), corpus, space, tmask)
        same_profile = st._rounded(profile) == structure["profiles"][f"reuse_r{rep}"]
        engine, problems = rebuild_final(record, space)
        corpus_with = on_corpus(engine, corpus, labels)
        space_with = on_space(engine, tmask, space.n)
        static = published["runs"][f"run{rep}"]["static"]
        edges_match = (corpus_with["e2e"] == static["corpus"]["with_edges"]["e2e"]
                       and space_with["e2e"] == static["space"]["with_edges"]["e2e"])
        fill_space = share(space_with["e2e"], profile["subsumption"]["space"]["e2e"],
                           profile["bounds"]["hibrido"]["space"])
        fill_corpus = share(corpus_with["e2e"], profile["subsumption"]["corpus"]["e2e"],
                            profile["bounds"]["hibrido"]["corpus"])
        nesting = distinct_nesting(record["rules"], space)
        declared_ok = (round(fill_space, 4) == plan.DECLARED_FILL_SPACE[k]
                       and round(fill_corpus, 4) == plan.DECLARED_FILL_CORPUS[k]
                       and round(nesting, 4) == plan.DECLARED_DISTINCT_NESTING[k])
        rows.append({
            "rep": rep, "profile_reproduces": same_profile,
            "edges_reinstall": not problems, "with_edges_reproduce": edges_match,
            "fill_space": fill_space, "fill_corpus": fill_corpus,
            "distinct_nesting": nesting, "declared_in_section_0": declared_ok,
            "passes": same_profile and not problems and edges_match and declared_ok})
    return {"what": "PLAN_REUSE.md's three bases: structure.json's profiles, "
                    "results_edges/score.json's end to end with edges, and §0's "
                    "baseline shares and nesting, recomputed",
            "rows": rows, "passes": all(r["passes"] for r in rows)}


# ---------------------------------------------------------------------------
# E-g3
# ---------------------------------------------------------------------------

class ReplayV1:
    """A v1 run's proposals, served back in order: each escalation's payload
    rebuilt from the rule it bore, its row's `edge_reasons` and the
    `edge_log`. A citation dropped as outside the neighbourhood is in the rule's
    `dropped_edges` and not in the log, and the row's reasons say where it
    fell. Only for `E-g3`; it never reaches a model."""

    name = "replay(v1)"

    def __init__(self, record: dict):
        born = {r["born_at"]: r for r in record["rules"]}
        log = list(record.get("edge_log") or [])
        self.payloads: dict[int, dict | None] = {}
        pos = 0
        for row in record["records"]:
            if not row["escalated"]:
                continue
            d = born.get(row["idx"])
            if d is None:
                self.payloads[row["idx"]] = None
                continue
            outside = []
            for x in d.get("dropped_edges") or []:
                parts = x.split(":")
                if not (len(parts) >= 3 and parts[-1] in VERDICTS):
                    outside.append((parts[0], ":".join(parts[1:])))
            cites: dict[str, list[str]] = {"beats": [], "loses_to": []}
            for why in row.get("edge_reasons") or []:
                if why == p.OUTSIDE:
                    direction, ref = outside.pop(0)
                else:
                    w, l, _logged = log[pos]
                    pos += 1
                    direction, ref = (("beats", l) if w == d["rule_id"]
                                      else ("loses_to", w))
                cites[direction].append(ref)
            self.payloads[row["idx"]] = {"action": d["action"],
                                         "conditions": d["conditions"],
                                         "note": d.get("note", ""), **cites}
        self.queue = [row["idx"] for row in record["records"] if row["escalated"]]
        self.pos = 0

    def build_base(self, engine, case, undefeated):
        shown, kind = neighbourhood(engine, case, undefeated)
        return shown, kind, render_base_v1(shown, kind, engine, case)

    def propose(self, case, base_text):
        idx = self.queue[self.pos]
        self.pos += 1
        payload = self.payloads[idx]
        if payload is None:
            raise ProposalError("replayed failure")
        return payload["action"], payload


def as_json(x: Any) -> Any:
    return json.loads(json.dumps(x, default=str))


def parity(record: dict, corpus, space: Space) -> dict[str, Any]:
    """One v1 run, replayed through `authorship/loop.py` with v1e off."""
    engine = PriorityEngine(space=space)
    res = loop.run_loop(corpus, labels_of(record), engine, ReplayV1(record), v1e=False)
    checks = {
        "records": as_json([vars(r) for r in res.run.records]) == record["records"],
        "rules": as_json([r.as_dict() for r in engine.rules]) == record["rules"],
        "edge_log": as_json(engine.edge_log) == record["edge_log"],
        "metrics": as_json(res.run.metrics) == record["metrics"],
    }
    return {**checks, "passes": all(checks.values())}


def copies_flagged(record: dict, space: Space) -> list[str]:
    """§5.2's copy check over a run's births, in order. A refused copy is not
    added, as v1e would not add it."""
    engine = PriorityEngine(space=space)
    flagged = []
    for d in sorted(record["rules"], key=lambda r: r["born_at"]):
        rule = rule_from(d)
        if p.copies_of(engine, space.extension(rule.conditions)):
            flagged.append(d["rule_id"])
            continue
        engine.add(rule, born_at=d["born_at"], keep_id=True)
    return flagged


def gate_eg3() -> dict[str, Any]:
    space = Space()
    corpus = generate_corpus(plan.N, seed=plan.SEED)
    records = {rep: load(plan.baseline_path(rep)) for rep in plan.BASELINE_REPS}
    rung1 = labels_of(load(plan.RUNG1))
    labels_agree = all(labels_of(r) == rung1 for r in records.values())
    head = ([c.as_dict() for c in generate_corpus(plan.SMOKE_N, seed=plan.SEED)]
            == [c.as_dict() for c in corpus[:plan.SMOKE_N]])
    replays = {rep: parity(r, corpus, space) for rep, r in records.items()}
    vehicles = load(plan.BASELINE_STRUCTURE)["post_run"]["vehicles"]
    copies = {}
    for rep, r in records.items():
        expected = {row["rule_id"] for row in vehicles[f"reuse_r{rep}"]["rows"]}
        got = copies_flagged(r, space)
        copies[rep] = {"flagged": len(got), "expected": len(expected),
                       "passes": set(got) == expected and len(got) == len(expected)}
    fp = p.fingerprint()
    checks = {
        "labels_agree": labels_agree, "smoke_is_the_head": head,
        "replays": all(v["passes"] for v in replays.values()),
        "copies": all(v["passes"] for v in copies.values())
                  and sum(v["flagged"] for v in copies.values()) == 44,
        "fingerprint": fp == plan.FINGERPRINT,
    }
    return {"what": "the labels, the head of the corpus, the v1 replay through the "
                    "loop, the copy check on the baseline, and the v1e texts' hash",
            **checks, "replay_rows": replays, "copy_rows": copies,
            "fingerprint_measured": fp, "fingerprint_declared": plan.FINGERPRINT,
            "passes": all(checks.values())}


# ---------------------------------------------------------------------------

@dataclass
class Checks:
    eg1: dict[str, Any]
    eg2: dict[str, Any]
    eg3: dict[str, Any]
    eg4: dict[str, Any]

    @property
    def blocking_pass(self) -> bool:
        return all(c["passes"] for c in (self.eg1, self.eg2, self.eg3))

    def summary(self) -> dict[str, Any]:
        return {"E-g1": {"passes": self.eg1["passes"],
                         "surfaces": self.eg1["surfaces"],
                         "suite": self.eg1["suite"]},
                "E-g2": {"passes": self.eg2["passes"],
                         "rows": [{k: v for k, v in r.items()} for r in self.eg2["rows"]]},
                "E-g3": {k: v for k, v in self.eg3.items() if k != "replay_rows"},
                "E-g4": self.eg4}


def run_all(suite: bool = True) -> Checks:
    return Checks(eg1=gate_eg1(suite=suite), eg2=gate_eg2(), eg3=gate_eg3(),
                  eg4=plan.gate_signature())


def report(c: Checks) -> None:
    mark = {True: "PASS", False: "FAIL", None: "—"}
    print("=" * 78)
    print(f"{plan.PLAN} — blocking checks (§7), zero API calls")
    print("=" * 78)
    s = c.eg1["surfaces"]
    print(f"  E-g1  {mark[c.eg1['passes']]}  hidden policy, {c.eg1['installed']} of "
          f"{c.eg1['declared']} edges installed through v1e's path: corpus e2e "
          f"{s['corpus']['e2e']:.4f}, space e2e {s['space']['e2e']:.4f}")
    t = c.eg1["suite"]
    print("              test suite: " + (
        f"{t['tests']} tests, {t['result']} ({t['seconds']} s)" if t["ran"]
        else "not run here"))
    print(f"  E-g2  {mark[c.eg2['passes']]}  the baseline reproduces")
    for r in c.eg2["rows"]:
        print(f"          run {r['rep']}: profile {mark[r['profile_reproduces']]}, "
              f"edges re-install {mark[r['edges_reinstall']]}, end to end with "
              f"edges {mark[r['with_edges_reproduce']]}, §0's figures "
              f"{mark[r['declared_in_section_0']]} (space share "
              f"{r['fill_space']:.4f}, corpus share {r['fill_corpus']:.4f}, "
              f"nesting {r['distinct_nesting']:.4f})")
    g = c.eg3
    print(f"  E-g3  {mark[g['passes']]}  labels {mark[g['labels_agree']]}, smoke head "
          f"{mark[g['smoke_is_the_head']]}, v1 replay {mark[g['replays']]}, copies "
          f"{mark[g['copies']]}, fingerprint {mark[g['fingerprint']]} "
          f"({g['fingerprint_measured']})")
    print(f"  E-g4  {mark[c.eg4['passes']]}  signature: {c.eg4['found']} line(s), "
          f"{c.eg4['unsigned']} blank")
