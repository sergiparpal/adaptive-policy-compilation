"""
`O-g1` to `O-g4` of `PLAN_OVERLAP.md` §7 — the blocking checks, all free.

They run before any record of the plan is written and before any call is made,
and **any failure stops the plan before a figure exists**. They are brought
forward to before signature, so that a failure becomes a fix to the draft and
not a signed amendment.

  O-g1  STOP 0, for the engine and the exempted declaration path. The hidden
        policy written under v2e's discipline: its 29 rules enter a fresh rung 2
        engine one by one, each placed against every earlier rule of another
        queue it overlaps, in the direction of the layer order, through the
        loop's own installation. Every declaration must be accepted, the 199
        edges of the policy must be the ones installed, and the engine must
        execute the policy at 1.0000, with no silent error, CONFLICT or IMPASSE,
        on the corpus and over the space. And the suite is green.
  O-g2  The baselines reproduce. `rows.py`, the instrument Stage C reads the
        runs with, applied to `PLAN_REUSE.md`'s and `PLAN_AUTHORSHIP.md`'s
        records and to rung 2's eight n=100 records, gives every figure §0
        declares; v1's O-c equals `results_edges/score.json`'s `W-b`, and v1e's
        O-b shares equal `results_authorship/score.json`'s `E-c`.
  O-g3  The loop and the validator do what §5 says, and nothing else. With the
        discipline off, each of rung 2's four v2 records replays through
        `overlap/loop.py`, case by case, rule by rule and verdict by verdict.
        With it on, on every call of v1e's records that computed an overlapped
        set, the exempted split gives back v1e's set, the rules of another
        queue as `O` and those of the new rule's queue as `S`. The labels agree
        across the baselines and rung 1, the smoke corpus is the head of the
        full one, and the v2e texts hash to the declared fingerprint.
  O-g4  The signature (`overlap/plan.py`). It blocks every write and every call,
        and not a dry run, which writes nothing.

**What a dry run prints is pass or fail, and figures the plan or a published
record already states.** No figure of Stage B or C exists to print.
"""

from __future__ import annotations

import json
import statistics
from dataclasses import dataclass
from typing import Any

from harness.ceiling_check import HIDDEN_DSL, all_cases
from harness.domain import DOMAINS, generate_corpus
from harness.dsl import Condition

from authorship import gates as egates
from authorship import loop as eloop
from authorship import protocol as e
from fidelity.replay import rule_from
from reuse.gates import run_suite
from rung2.ceiling_check2_space import measure
from rung2.engine2 import EDGE_OK, PriorityEngine, Rule2, Space, validate_conditions
from rung2.hidden_priority import build_hidden_engine
from rung2.proposers2 import ProposalError, neighbourhood, render_base_v2
from rung3.order_search_ls import space_truth_masks

from . import loop, plan, rows
from . import protocol as v

load = egates.load
labels_of = egates.labels_of


def r4(x):
    return None if x is None else round(x, 4)


# ---------------------------------------------------------------------------
# O-g1
# ---------------------------------------------------------------------------

def gate_og1(suite: bool = True) -> dict[str, Any]:
    space = Space()
    _ref, minimal, _ = build_hidden_engine(space)
    engine = PriorityEngine(space=space)
    allowed = {rid for rid, _, _ in HIDDEN_DSL}
    channels: list[str] = []
    verdicts: dict[str, int] = {}
    declarations = exempted = 0
    for i, (rid, conds, action) in enumerate(HIDDEN_DSL):
        rule = Rule2(rule_id=rid, action=action,
                     conditions=[Condition(attr=a, op=o, value=x) for a, o, x in conds])
        o, s = v.split_overlapped(engine, space.extension(rule.conditions), action)
        declarations += len(o)
        exempted += len(s)
        engine.add(rule, born_at=i, keep_id=True)
        # every earlier rule is of an earlier layer, so it wins: `loses_to`
        _n, _acc, reasons = eloop.install_declarations(
            engine, rule, {"loses_to": o}, allowed, e.WRITE, channels)
        for why in reasons:
            verdicts[why] = verdicts.get(why, 0) + 1
    installed = {(w, l) for l, ws in engine.decl_below.items() for w in ws}
    surfaces = {}
    for name, cases in (("corpus", generate_corpus(plan.N, seed=plan.SEED)),
                        ("space", list(all_cases()))):
        m = measure(engine, cases, name, "hybrid, the policy written under v2e")
        surfaces[name] = {
            "e2e": m["accuracy_end_to_end"], "silent_errors": m["silent_errors_abs"],
            "conflict": m["conflict"], "impasse": m["impasse"],
            "passes": (m["accuracy_end_to_end"] == 1.0 and m["silent_errors_abs"] == 0
                       and m["conflict"] == 0 and m["impasse"] == 0)}
    tests = run_suite() if suite else {"ran": False, "passes": None}
    counts = {"declarations": declarations, "installed": len(installed),
              "exempted": exempted}
    edges_ok = (verdicts == {EDGE_OK: declarations}
                and installed == set(minimal)
                and counts == plan.DECLARED_HIDDEN)
    return {
        "what": "the hidden policy written under v2e's discipline, every overlapped "
                "rule of another queue placed by layer order, executed at 1.0000 on "
                "corpus and space; the suite green",
        **counts, "minimal_edges": len(minimal), "verdicts": verdicts,
        "surfaces": surfaces, "suite": tests,
        "passes": edges_ok and all(s["passes"] for s in surfaces.values())
                  and tests["passes"] is not False,
    }


# ---------------------------------------------------------------------------
# O-g2
# ---------------------------------------------------------------------------

def read_baseline(paths, corpus, space: Space, tmask: dict[str, int]) -> dict[str, Any]:
    """`rows.py` over three runs of one protocol, as Stage C reads this plan's."""
    out = {"o_a": [], "fill": [], "direction": [], "by_queue": []}
    for path in paths:
        record = load(path)
        engine, _ = egates.rebuild_final(record, space)
        out["o_a"].append(rows.o_a(record["rules"], space))
        out["fill"].append(rows.fill(record, corpus, space, tmask))
        out["direction"].append(rows.direction(record, engine, tmask))
        out["by_queue"].append(rows.by_queue(record, engine))
    shares = [f["space"]["share"] for f in out["fill"]]
    pooled_counts: dict[str, int] = {}
    for c in out["by_queue"]:
        for k, n in c.items():
            pooled_counts[k] = pooled_counts.get(k, 0) + n
    return {**out, "o_a_median": statistics.median(out["o_a"]),
            "o_b_shares": shares, "o_b": rows.o_b_reading(shares),
            "o_b_pooled": rows.pooled_fill(out["fill"]),
            "o_c": rows.o_c_reading(out["direction"]),
            "by_queue_pooled": pooled_counts}


def gate_og2() -> dict[str, Any]:
    corpus = generate_corpus(plan.N, seed=plan.SEED)
    space = Space()
    tmask = space_truth_masks(space)
    base = {"v1": read_baseline([plan.v1_path(k) for k in plan.BASELINE_REPS],
                                corpus, space, tmask),
            "v1e": read_baseline([plan.v1e_path(k) for k in plan.BASELINE_REPS],
                                 corpus, space, tmask)}
    checks: dict[str, bool] = {}
    for proto, b in base.items():
        checks[f"O-a {proto}"] = (tuple(r4(x) for x in b["o_a"]) == plan.DECLARED_O_A[proto]
                                  and r4(b["o_a_median"]) == plan.DECLARED_O_A_MEDIAN[proto])
        checks[f"O-b {proto}"] = (tuple(r4(x) for x in b["o_b_shares"])
                                  == plan.DECLARED_O_B[proto]
                                  and r4(b["o_b"]["reading"]) == plan.DECLARED_O_B_READING[proto]
                                  and r4(b["o_b_pooled"]) == plan.DECLARED_O_B_POOLED[proto])
        checks[f"O-c {proto}"] = ((b["o_c"]["hits"], b["o_c"]["strict"])
                                  == plan.DECLARED_O_C[proto])
    v1e = base["v1e"]
    checks["O-c v1e by run"] = (tuple((d["hits"], d["hits"] + d["misses"])
                                      for d in v1e["direction"])
                                == plan.DECLARED_O_C_V1E_RUNS)
    checks["v1e installed"] = (tuple(d["installed"] for d in v1e["direction"])
                               == plan.DECLARED_V1E_INSTALLED
                               and sum(d["installed_same_queue"] for d in v1e["direction"])
                               == plan.DECLARED_V1E_INSTALLED_SAME_QUEUE)
    q = plan.DECLARED_BY_QUEUE
    checks["by queue"] = (
        rows.same_queue_share(v1e["by_queue_pooled"]) == q["v1e"]["all"]
        and rows.same_queue_share(v1e["by_queue_pooled"], exclude=("no_solapan",))
        == q["v1e"]["not_no_solapan"]
        and rows.same_queue_share(base["v1"]["by_queue_pooled"]) == q["v1"]["all"]
        and rows.same_queue_share(base["v1"]["by_queue_pooled"],
                                  only=(rows.INSTALLED, rows.REDUNDANT)) == q["v1"]["accepted"])
    # Against the records that publish them.
    w_b = load(plan.BASELINE_EDGES)["runs"]
    checks["v1's O-c is W-b"] = all(
        (d["hits"], d["hits"] + d["misses"]) == (w_b[f"run{k}"]["W-b"]["space"]["hits"],
                                                 w_b[f"run{k}"]["W-b"]["space"]["n"])
        for k, d in zip(plan.BASELINE_REPS, base["v1"]["direction"]))
    e_c = load(plan.BASELINE_V1E_SCORE)["verdicts"]["E-c"]["per_run"]
    checks["v1e's O-b is E-c"] = [None if s is None else round(s, 6)
                                  for s in v1e["o_b_shares"]] == e_c
    n100 = {"v1": [rows.o_a(load(p)["rules"], space) for p in plan.RUNG2_V1],
            "v2": [rows.o_a(load(p)["rules"], space) for p in plan.RUNG2_V2]}
    checks["O-a at n=100"] = all(tuple(round(x, 2) for x in n100[k])
                                 == plan.DECLARED_O_A_N100[k] for k in n100)
    return {"what": "§0's baseline figures, read by the instrument Stage C uses, and "
                    "checked against W-b and E-c as published",
            "checks": checks,
            "measured": {proto: {"o_a": [r4(x) for x in b["o_a"]],
                                 "o_a_median": r4(b["o_a_median"]),
                                 "o_b_shares": [r4(x) for x in b["o_b_shares"]],
                                 "o_b": {**b["o_b"], "reading": r4(b["o_b"]["reading"])},
                                 "o_b_pooled": r4(b["o_b_pooled"]),
                                 "o_c": b["o_c"],
                                 "by_queue": b["by_queue_pooled"]}
                         for proto, b in base.items()},
            "o_a_n100": {k: [round(x, 2) for x in xs] for k, xs in n100.items()},
            "passes": all(checks.values())}


# ---------------------------------------------------------------------------
# O-g3
# ---------------------------------------------------------------------------

FAILED = "proposal_failed: "
NOT_MATCHING = "la regla no casa el caso que la origino"


class ReplayV2(egates.ReplayV1):
    """A v2 run's proposals, served back in order. `ReplayV1`'s reconstruction,
    with v2's rendering, which only the text of the prompt depends on, and two
    escalations it cannot rebuild, which rung 2's v2 records hold and
    `PLAN_REUSE.md`'s did not: a failed call is failed again with the message it
    recorded, and a rule refused for not matching its ticket is proposed again as
    a rule that does not match it, with the queue the record keeps. Any other
    refusal stops the replay. Only for `O-g3`; it never reaches a model."""

    name = "replay(v2)"

    def __init__(self, record: dict):
        super().__init__(record)
        self.rows = {row["idx"]: row for row in record["records"] if row["escalated"]}

    def build_base(self, engine, case, undefeated):
        shown, kind = neighbourhood(engine, case, undefeated)
        return shown, kind, render_base_v2(shown, kind, engine, case)

    def propose(self, case, base_text):
        idx = self.queue[self.pos]
        if self.payloads[idx] is not None:
            return super().propose(case, base_text)
        self.pos += 1
        row = self.rows[idx]
        reason = row["rejected_reason"] or ""
        if reason.startswith(FAILED):
            raise ProposalError(reason[len(FAILED):])
        if reason == NOT_MATCHING:
            other = next(x for x in DOMAINS["language"] if x != case.language)
            return row["predicted"], {
                "action": row["predicted"], "beats": [], "loses_to": [], "note": "",
                "conditions": [{"attr": "language", "op": "eq", "value": other}]}
        raise ValueError(f"case {idx}: a refusal this replay cannot rebuild: {reason!r}")


def parity(record: dict, space: Space) -> dict[str, Any]:
    """One of rung 2's v2 runs, replayed through `overlap/loop.py` with the
    discipline off, on its own corpus and with its own labels."""
    corpus = generate_corpus(record["n"], seed=record["seed"])
    engine = PriorityEngine(space=space)
    res = loop.run_loop(corpus, labels_of(record), engine, ReplayV2(record), v2e=False)
    checks = {
        "records": egates.as_json([vars(r) for r in res.run.records]) == record["records"],
        "rules": egates.as_json([r.as_dict() for r in engine.rules]) == record["rules"],
        "edge_log": egates.as_json(engine.edge_log) == record["edge_log"],
        "metrics": egates.as_json(res.run.metrics) == record["metrics"],
    }
    return {"seed": record["seed"], **checks, "passes": all(checks.values())}


def exempted_splits(record: dict, space: Space) -> dict[str, Any]:
    """v1e's recorded overlapped sets, split by v2e: on every call that computed
    one, the engine as it stood at that case gives back the recorded set, the
    rules of another queue as `O` and those of the proposed rule's queue as `S`."""
    rules = sorted(record["rules"], key=lambda r: (r["born_at"], r["rule_id"]))
    engine = PriorityEngine(space=space)
    born = 0
    calls = matched = 0
    for esc in sorted(record.get("escalations") or [], key=lambda x: x["idx"]):
        while born < len(rules) and rules[born]["born_at"] < esc["idx"]:
            engine.add(rule_from(rules[born]), born_at=rules[born]["born_at"], keep_id=True)
            born += 1
        for call in esc["calls"]:
            if "overlapped" not in call:
                continue
            calls += 1
            payload = call["payload"]
            proposed = validate_conditions(payload, case=None)
            ext = space.extension(proposed.conditions)
            o, s = v.split_overlapped(engine, ext, payload["action"])
            action = {r.rule_id: r.action for r in engine.rules}
            recorded = call["overlapped"]
            matched += (sorted(o + s) == sorted(recorded)
                        and o == [r for r in recorded if action[r] != payload["action"]]
                        and s == [r for r in recorded if action[r] == payload["action"]])
    return {"calls": calls, "matched": matched, "passes": calls > 0 and calls == matched}


def gate_og3() -> dict[str, Any]:
    space = Space()
    corpus = generate_corpus(plan.N, seed=plan.SEED)
    rung1 = labels_of(load(plan.RUNG1))
    v1 = [load(plan.v1_path(k)) for k in plan.BASELINE_REPS]
    v1e = [load(plan.v1e_path(k)) for k in plan.BASELINE_REPS]
    labels_agree = all(labels_of(r) == rung1 for r in v1 + v1e)
    head = ([c.as_dict() for c in generate_corpus(plan.SMOKE_N, seed=plan.SEED)]
            == [c.as_dict() for c in corpus[:plan.SMOKE_N]])
    replays = [parity(load(p), space) for p in plan.RUNG2_V2]
    splits = [exempted_splits(r, space) for r in v1e]
    fp = v.fingerprint()
    checks = {
        "labels_agree": labels_agree, "smoke_is_the_head": head,
        "replays": all(r["passes"] for r in replays),
        "exempted_splits": all(s["passes"] for s in splits),
        "fingerprint": fp == plan.FINGERPRINT,
    }
    return {"what": "the labels, the head of the corpus, rung 2's v2 runs replayed "
                    "through the loop, the exempted split on v1e's recorded sets, "
                    "and the v2e texts' hash",
            **checks, "replay_rows": replays, "split_rows": splits,
            "fingerprint_measured": fp, "fingerprint_declared": plan.FINGERPRINT,
            "passes": all(checks.values())}


# ---------------------------------------------------------------------------

@dataclass
class Checks:
    og1: dict[str, Any]
    og2: dict[str, Any]
    og3: dict[str, Any]
    og4: dict[str, Any]

    @property
    def blocking_pass(self) -> bool:
        return all(c["passes"] for c in (self.og1, self.og2, self.og3))

    def summary(self) -> dict[str, Any]:
        return {"O-g1": {k: self.og1[k] for k in ("passes", "declarations", "installed",
                                                   "exempted", "surfaces", "suite")},
                "O-g2": {k: self.og2[k] for k in ("passes", "checks")},
                "O-g3": {k: x for k, x in self.og3.items() if k != "replay_rows"},
                "O-g4": self.og4}


def run_all(suite: bool = True) -> Checks:
    return Checks(og1=gate_og1(suite=suite), og2=gate_og2(), og3=gate_og3(),
                  og4=plan.gate_signature())


def report(c: Checks) -> None:
    mark = {True: "PASS", False: "FAIL", None: "—"}
    print("=" * 78)
    print(f"{plan.PLAN} — blocking checks (§7), zero API calls")
    print("=" * 78)
    g1 = c.og1
    s = g1["surfaces"]
    print(f"  O-g1  {mark[g1['passes']]}  hidden policy under v2e: {g1['declarations']} "
          f"declarations, {g1['installed']} installed of {g1['minimal_edges']}, "
          f"{g1['exempted']} exempted; corpus e2e {s['corpus']['e2e']:.4f}, space e2e "
          f"{s['space']['e2e']:.4f}")
    t = g1["suite"]
    print("              test suite: " + (
        f"{t['tests']} tests, {t['result']} ({t['seconds']} s)" if t["ran"]
        else "not run here"))
    print(f"  O-g2  {mark[c.og2['passes']]}  the baselines reproduce")
    for name, ok in c.og2["checks"].items():
        print(f"          {name:<20} {mark[ok]}")
    g3 = c.og3
    print(f"  O-g3  {mark[g3['passes']]}  labels {mark[g3['labels_agree']]}, smoke head "
          f"{mark[g3['smoke_is_the_head']]}, v2 replays {mark[g3['replays']]}, exempted "
          f"splits {mark[g3['exempted_splits']]}, fingerprint {mark[g3['fingerprint']]} "
          f"({g3['fingerprint_measured']})")
    print(f"  O-g4  {mark[c.og4['passes']]}  signature: {c.og4['found']} line(s), "
          f"{c.og4['unsigned']} blank")


def as_json(x: Any) -> Any:
    return json.loads(json.dumps(x, default=str))
