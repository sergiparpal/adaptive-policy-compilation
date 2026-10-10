"""
`K-g1` to `K-g4` of `PLAN_BLIND.md` §7 — the blocking checks, all free.

They run before any record of the plan is written and before any call is made,
and **any failure stops the plan before a figure exists**. They are brought
forward to before signature, so that a failure becomes a fix to the draft and
not a signed amendment.

  K-g1  STOP 0, for the engine and the blind path. The hidden policy written
        through `loop.propose_blind`: each of its 29 rules drafted blind, on a
        ticket it matches, and placed in the placement round against every
        earlier rule of another queue it overlaps, in the direction of the layer
        order. Every rule must be born, every declaration accepted, the 199 edges
        of the policy must be the ones installed, and the engine must execute the
        policy at 1.0000, with no silent error, CONFLICT or IMPASSE, on the corpus
        and over the space. And the suite is green.
  K-g2  The instrument reproduces what is paid for. `rows.py`, the instrument
        Stage C reads the runs with, applied to the three baselines' nine runs:
        with the keyword's restriction lifted it gives `O-a`, `O-b` and `O-c` as
        `PLAN_OVERLAP.md` declares and publishes them; with it, every figure §0
        declares of the baselines, of rung 1's blind births and of the pairwise
        answers `PLAN_PROPOSER_1600.md` paid for.
  K-g3  The loop does what §5 says, and nothing else. With the blind draft off,
        `PLAN_OVERLAP.md`'s smoke run and three runs replay through
        `blind/loop.py`, case by case, rule by rule, edge by edge and call by
        call. The labels agree across the baselines and rung 1, the smoke corpus
        is the head of the full one, and the v2b texts hash to the declared
        fingerprint.
  K-g4  The signature (`blind/plan.py`). It blocks every write and every call,
        and not a dry run, which writes nothing.

**What a dry run prints is pass or fail, and figures the plan or a published
record already states.** No figure of Stage B or C exists to print.
"""

from __future__ import annotations

import json
import statistics
from dataclasses import asdict, dataclass
from typing import Any

from harness.ceiling_check import HIDDEN_DSL, all_cases
from harness.domain import generate_corpus

from authorship import gates as egates
from authorship import protocol as e
from authorship.refused import matched_sets
from overlap import plan as overlap_plan
from overlap import protocol as v2e
from reuse.gates import run_suite
from rung2.ceiling_check2_space import measure as measure_engine
from rung2.engine2 import EDGE_OK, PriorityEngine, Space, validate_conditions
from rung2.hidden_priority import build_hidden_engine
from rung2.proposers2 import neighbourhood
from rung3.order_search_ls import space_truth_masks

from . import loop, plan, rows
from . import protocol as p

load = egates.load
labels_of = egates.labels_of


def r4(x):
    return None if x is None else round(x, 4)


# ---------------------------------------------------------------------------
# K-g1
# ---------------------------------------------------------------------------

class HiddenAuthor:
    """A proposer that writes the hidden policy through v2b's path: the draft is
    the rule, and the placement answer is the same rule losing to every rule
    listed, since every earlier rule is of an earlier layer. It reads `O` off the
    engine it is handed, as the loop computes it. Only for `K-g1`."""

    name = "hidden-author"

    def __init__(self, engine: PriorityEngine):
        self.engine = engine
        self.payload: dict | None = None

    def write(self, conds, action) -> None:
        self.payload = {"action": action, "beats": [], "loses_to": [], "note": "H",
                        "conditions": [{"attr": a, "op": o, "value": x}
                                       for a, o, x in conds]}

    def first(self, case, base_text, idx):
        return e.Answer(self.payload["action"], self.payload, json.dumps(self.payload),
                        "stop", 1)

    def repair(self, case, base_text, previous, message, idx):
        rule = validate_conditions(self.payload, case=None)
        o, _ = p.split_overlapped(self.engine, self.engine.space.extension(rule.conditions),
                                  rule.action)
        placed = dict(self.payload, loses_to=o)
        return e.Answer(placed["action"], placed, json.dumps(placed), "stop", 1)


def witness(space: Space, cases: list, ext: int):
    """The lowest-indexed case of the space in `ext`: case `i` is bit `n - 1 - i`."""
    return cases[space.n - ext.bit_length()]


def gate_kg1(suite: bool = True) -> dict[str, Any]:
    space = Space()
    cases = list(all_cases())
    _ref, minimal, _ = build_hidden_engine(space)
    engine = PriorityEngine(space=space)
    author = HiddenAuthor(engine)
    channels: list[str] = []
    verdicts: dict[str, int] = {}
    born = declarations = exempted = 0
    for i, (rid, conds, action) in enumerate(HIDDEN_DSL):
        author.write(conds, action)
        ext = space.extension(validate_conditions(author.payload, case=None).conditions)
        o, s = p.split_overlapped(engine, ext, action)
        declarations += len(o)
        exempted += len(s)
        res = loop.propose_blind(engine, witness(space, cases, ext), i, "IMPASSE", [],
                                 p.BLIND_BASE, author, channels)
        born += res["esc"].verdict == e.BORN
        for why in res["reasons"]:
            verdicts[why] = verdicts.get(why, 0) + 1
    named = {r.rule_id: HIDDEN_DSL[k][0] for k, r in enumerate(engine.rules)}
    installed = {(named[w], named[l]) for l, ws in engine.decl_below.items() for w in ws}
    surfaces = {}
    for name, cs in (("corpus", generate_corpus(plan.N, seed=plan.SEED)), ("space", cases)):
        m = measure_engine(engine, cs, name, "hybrid, the policy written through v2b")
        surfaces[name] = {
            "e2e": m["accuracy_end_to_end"], "silent_errors": m["silent_errors_abs"],
            "conflict": m["conflict"], "impasse": m["impasse"],
            "passes": (m["accuracy_end_to_end"] == 1.0 and m["silent_errors_abs"] == 0
                       and m["conflict"] == 0 and m["impasse"] == 0)}
    tests = run_suite() if suite else {"ran": False, "passes": None}
    counts = {"born": born, "declarations": declarations, "installed": len(installed),
              "exempted": exempted}
    edges_ok = (verdicts == {EDGE_OK: declarations} and installed == set(minimal)
                and counts == plan.DECLARED.get("hidden"))
    return {
        "what": "the hidden policy written through v2b's blind path, every overlapped "
                "rule of another queue placed by layer order in the placement round, "
                "executed at 1.0000 on corpus and space; the suite green",
        **counts, "minimal_edges": len(minimal), "verdicts": verdicts,
        "surfaces": surfaces, "suite": tests,
        "passes": edges_ok and all(x["passes"] for x in surfaces.values())
                  and tests["passes"] is not False,
    }


# ---------------------------------------------------------------------------
# K-g2
# ---------------------------------------------------------------------------

def read_runs(paths, corpus, space: Space, tmask, outside: int, cases_out) -> dict[str, Any]:
    """`rows.py` over the runs of one protocol, with the restriction lifted and
    with it, as Stage C reads this plan's runs."""
    out: dict[str, Any] = {"o_a": [], "k_a": [], "births": [], "o_b": [], "k_d": [],
                           "k_d_room": [], "edge_rows": []}
    for path in paths:
        record = load(path)
        engine, problems = egates.rebuild_final(record, space)
        if problems:
            raise ValueError(f"{path}: an accepted edge did not re-install: {problems}")
        truth = [t for t, _ in labels_of(record)]
        out["o_a"].append(rows.k_a(record["rules"], space, space.full))
        out["k_a"].append(rows.k_a(record["rules"], space, outside))
        out["births"].append(rows.births_outside(record["rules"], space, outside))
        out["o_b"].append(rows.fill(record, space, tmask, space.full)["share"])
        f = rows.fill(record, space, tmask, outside)
        out["k_d"].append(f["share"])
        out["k_d_room"].append(f["room"])
        out["edge_rows"].append(rows.edge_rows(record, engine, tmask, outside,
                                               matched_sets(engine, corpus), truth, cases_out))
    return out


def summary_of(read: dict[str, Any]) -> dict[str, Any]:
    """What §0 declares of one protocol, at the digits it gives them."""
    er = read["edge_rows"]
    o_c = rows.direction(er, "space_full", keep=rows.across_queues)
    k_b = rows.comparators(er, "space_out")
    k_e = rows.direction(er, "corpus_out")
    census = [(sum(1 for x in rs if not x["same_queue"]),
               sum(1 for x in rs if not x["same_queue"] and x["keyword"])) for rs in er]

    def d(x):
        return (x["units"], r4(x["reading"]), x["hits"], x["strict"])

    return {
        "o_a": tuple(r4(x) for x in read["o_a"]),
        "k_a": tuple(r4(x) for x in read["k_a"]),
        "k_a_median": r4(statistics.median(read["k_a"])),
        "o_b": tuple(r4(x) for x in read["o_b"]),
        "k_d": tuple(r4(x) for x in read["k_d"]),
        "o_c": (o_c["hits"], o_c["strict"]),
        "k_b": d(k_b["declared"]),
        "k_b_stage_c": d(k_b["stage_c_ranking"]),
        "k_e": d(k_e),
        "across_queues_and_keyword": tuple(census),
    }


def pairwise_reference(space: Space, tmask, outside: int, corpus, cases_out) -> dict[str, Any]:
    """The answers `PLAN_PROPOSER_1600.md` paid for, over rung 1's base, read with
    the same instrument: the declared winner of every answer that declared one,
    on the pairs where neither rule is a keyword rule."""
    rung1 = load(plan.RUNG1)
    answers = load(plan.PAIRWISE)["answers"]
    truth = [t for t, _ in labels_of(rung1)]
    pr = rows.pair_rows(answers, rung1, space, tmask, outside,
                        rows.sets_of(rung1["rules"], corpus), truth, cases_out)
    keep = rows.outside_the_keyword
    space_ = rows.comparators([pr], "space_out", keep=keep)
    corpus_ = rows.comparators([pr], "corpus_out", keep=keep)
    split = rows.split_by_queue_pair([pr], "space_out", keep=keep)

    def d(x):
        return (x["units"], r4(x["reading"]), x["hits"], x["strict"])

    return {"answers_with_a_pair": len(pr),
            "keyword_pairs": sum(1 for x in pr if x["keyword"]),
            "space": {k: d(x) for k, x in space_.items()},
            "corpus": {k: d(x) for k, x in corpus_.items()},
            "split": {"unreachable_queue_pairs": split["unreachable_queue_pairs"],
                      "queue_pairs": split["queue_pairs"],
                      "reachable": d(split["reachable"]),
                      "unreachable": d(split["unreachable"])}}


def rung1_blind_births(space: Space, tmask, outside: int) -> dict[str, Any]:
    """Rung 1's base, the one base this model wrote without seeing it. K-a's
    statistic on growing prefixes in birth order, which mix births on an impasse
    with births on a CONFLICT; and on the rules born on an impasse alone, the
    births v2b's blind draft makes, with the strict pairs beyond the keyword they
    would put in front of K-b. Only that last count reads the truth."""
    rung1 = load(plan.RUNG1)
    rules = sorted(rung1["rules"], key=lambda r: (r["born_at"], r["rule_id"]))
    outcome = {row["idx"]: row["outcome"] for row in rung1["records"]}
    out: dict[str, Any] = {}
    for k in (20, 50, 100):
        b = rows.births_outside(rules[:k], space, outside)
        out[str(k)] = {"k_a": r4(b["alone_outside"] / b["outside"]),
                       "on_an_impasse": sum(1 for r in rules[:k]
                                            if outcome.get(r["born_at"]) == rows.IMPASSE)}
    imp = [r for r in rules if outcome.get(r["born_at"]) == rows.IMPASSE]
    b = rows.births_outside(imp, space, outside)
    out["impasse_born"] = {"rules": len(imp), "k_a": r4(b["alone_outside"] / b["outside"]),
                           **rows.material(imp, space, tmask, outside)}
    return out


def measure() -> dict[str, Any]:
    """Every figure `K-g2` checks, measured."""
    corpus = generate_corpus(plan.N, seed=plan.SEED)
    space = Space()
    tmask = space_truth_masks(space)
    outside = rows.outside_mask(space)
    cases_out = rows.outside_cases(corpus)
    reads = {name: read_runs([path(k) for k in plan.BASELINE_REPS], corpus, space,
                             tmask, outside, cases_out)
             for name, path in plan.BASELINES.items()}
    return {"outside": {"space": outside.bit_count(), "corpus": len(cases_out)},
            "baselines": {name: summary_of(r) for name, r in reads.items()},
            "rung1_blind_births": rung1_blind_births(space, tmask, outside),
            "pairwise": pairwise_reference(space, tmask, outside, corpus, cases_out)}


def published() -> dict[str, Any]:
    """`O-a`, `O-b` and `O-c` of the three baselines, as `PLAN_OVERLAP.md`
    declares v1's and v1e's and `results_overlap/score.json` publishes v2e's."""
    v = load(plan.OVERLAP_SCORE)["verdicts"]
    out = {name: {"o_a": overlap_plan.DECLARED_O_A[name],
                  "o_b": overlap_plan.DECLARED_O_B[name],
                  "o_c": overlap_plan.DECLARED_O_C[name]} for name in ("v1", "v1e")}
    out["v2e"] = {"o_a": tuple(r4(x) for x in v["O-a"]["per_run"]),
                  "o_b": tuple(r4(x) for x in v["O-b"]["per_run"]),
                  "o_c": (v["O-c"]["hits"], v["O-c"]["strict"])}
    return out


def gate_kg2() -> dict[str, Any]:
    m = measure()
    pub = published()
    checks: dict[str, bool] = {}
    for name, b in m["baselines"].items():
        for key in ("o_a", "o_b", "o_c"):
            checks[f"{key.replace('_', '-').upper()} {name}, as published"] = (
                b[key] == tuple(pub[name][key]))
    declared = plan.DECLARED
    checks["the halves without the keyword"] = m["outside"] == declared.get("outside")
    for name, b in m["baselines"].items():
        want = (declared.get("baselines") or {}).get(name) or {}
        checks[f"§0's figures, {name}"] = all(
            b[k] == want.get(k) for k in b if k not in ("o_a", "o_b", "o_c"))
    checks["rung 1's blind births"] = m["rung1_blind_births"] == declared.get("rung1_blind_births")
    checks["the pairwise answers"] = m["pairwise"] == declared.get("pairwise")
    return {"what": "the instrument Stage C uses, read on the nine paid runs with the "
                    "restriction lifted against what is published, and with it against "
                    "§0's figures; rung 1's blind births; the pairwise answers",
            "checks": checks, "measured": m, "passes": all(checks.values())}


# ---------------------------------------------------------------------------
# K-g3
# ---------------------------------------------------------------------------

class ReplayV2E:
    """A v2e run's answers, served back by case and round, with v2e's screens. A
    failed call fails again with the message it recorded. Only for `K-g3`; it
    never reaches a model."""

    name = "replay(v2e)"

    def __init__(self, record: dict):
        self.calls = {(x["idx"], c["round"]): c
                      for x in record.get("escalations") or [] for c in x["calls"]}

    def build_base(self, engine, case, undefeated):
        shown, kind = neighbourhood(engine, case, undefeated)
        return shown, kind, v2e.render_base(shown, kind, engine, case)

    def _serve(self, idx: int, round_: int) -> e.Answer:
        c = self.calls[(idx, round_)]
        if c["failure"] is not None:
            raise e.ProposalFailed(c["failure"], c["finish_reason"], c["attempts"])
        return e.Answer(c["payload"].get("action"), c["payload"], c["raw"],
                        c["finish_reason"], c["attempts"])

    def first(self, case, base_text, idx):
        return self._serve(idx, 0)

    def repair(self, case, base_text, previous, message, idx):
        return self._serve(idx, 1)


def without_seconds(escalations: list[dict]) -> list[dict]:
    return [dict(x, calls=[{k: c[k] for k in c if k != "seconds"} for c in x["calls"]])
            for x in escalations]


def parity(record: dict, space: Space) -> dict[str, Any]:
    """One of `PLAN_OVERLAP.md`'s runs, replayed through `blind/loop.py` with the
    blind draft off, on its own corpus and with its own labels."""
    corpus = generate_corpus(record["n"], seed=record["seed"])
    engine = PriorityEngine(space=space)
    res = loop.run_loop(corpus, labels_of(record), engine, ReplayV2E(record), blind=False)
    got = egates.as_json([asdict(x) for x in res.escalations])
    checks = {
        "records": egates.as_json([vars(r) for r in res.run.records]) == record["records"],
        "rules": egates.as_json([r.as_dict() for r in engine.rules]) == record["rules"],
        "edge_log": egates.as_json(engine.edge_log) == record["edge_log"],
        "edge_channels": res.edge_channels == record["edge_channels"],
        "metrics": egates.as_json(res.run.metrics) == record["metrics"],
        "calls": without_seconds(got) == without_seconds(record["escalations"]),
    }
    return {"run": record["rep"], **checks, "passes": all(checks.values())}


def gate_kg3() -> dict[str, Any]:
    space = Space()
    corpus = generate_corpus(plan.N, seed=plan.SEED)
    rung1 = labels_of(load(plan.RUNG1))
    runs = {name: [load(path(k)) for k in plan.BASELINE_REPS]
            for name, path in plan.BASELINES.items()}
    labels_agree = all(labels_of(r) == rung1 for rs in runs.values() for r in rs)
    head = ([c.as_dict() for c in generate_corpus(plan.SMOKE_N, seed=plan.SEED)]
            == [c.as_dict() for c in corpus[:plan.SMOKE_N]])
    replays = [parity(r, space) for r in [load(plan.V2E_SMOKE)] + runs["v2e"]]
    fp = p.fingerprint()
    checks = {"labels_agree": labels_agree, "smoke_is_the_head": head,
              "v2e_replays": all(r["passes"] for r in replays),
              "fingerprint": fp == plan.FINGERPRINT}
    return {"what": "the labels, the head of the corpus, PLAN_OVERLAP.md's runs replayed "
                    "through the loop with the blind draft off, and the v2b texts' hash",
            **checks, "replay_rows": replays,
            "fingerprint_measured": fp, "fingerprint_declared": plan.FINGERPRINT,
            "passes": all(checks.values())}


# ---------------------------------------------------------------------------

@dataclass
class Checks:
    kg1: dict[str, Any]
    kg2: dict[str, Any]
    kg3: dict[str, Any]
    kg4: dict[str, Any]

    @property
    def blocking_pass(self) -> bool:
        return all(c["passes"] for c in (self.kg1, self.kg2, self.kg3))

    def summary(self) -> dict[str, Any]:
        return {"K-g1": {k: self.kg1[k] for k in ("passes", "born", "declarations",
                                                   "installed", "exempted", "surfaces",
                                                   "suite")},
                "K-g2": {k: self.kg2[k] for k in ("passes", "checks")},
                "K-g3": self.kg3,
                "K-g4": self.kg4}


def run_all(suite: bool = True) -> Checks:
    return Checks(kg1=gate_kg1(suite=suite), kg2=gate_kg2(), kg3=gate_kg3(),
                  kg4=plan.gate_signature())


def report(c: Checks) -> None:
    mark = {True: "PASS", False: "FAIL", None: "—"}
    print("=" * 78)
    print(f"{plan.PLAN} — blocking checks (§7), zero API calls")
    print("=" * 78)
    g1 = c.kg1
    s = g1["surfaces"]
    print(f"  K-g1  {mark[g1['passes']]}  hidden policy through v2b: {g1['born']} born, "
          f"{g1['declarations']} declarations, {g1['installed']} installed of "
          f"{g1['minimal_edges']}, {g1['exempted']} exempted; corpus e2e "
          f"{s['corpus']['e2e']:.4f}, space e2e {s['space']['e2e']:.4f}")
    t = g1["suite"]
    print("              test suite: " + (
        f"{t['tests']} tests, {t['result']} ({t['seconds']} s)" if t["ran"]
        else "not run here"))
    print(f"  K-g2  {mark[c.kg2['passes']]}  the instrument reproduces what is paid for")
    for name, ok in c.kg2["checks"].items():
        print(f"          {name:<40} {mark[ok]}")
    g3 = c.kg3
    print(f"  K-g3  {mark[g3['passes']]}  labels {mark[g3['labels_agree']]}, smoke head "
          f"{mark[g3['smoke_is_the_head']]}, v2e replays {mark[g3['v2e_replays']]}, "
          f"fingerprint {mark[g3['fingerprint']]} ({g3['fingerprint_measured']})")
    print(f"  K-g4  {mark[c.kg4['passes']]}  signature: {c.kg4['found']} line(s), "
          f"{c.kg4['unsigned']} blank")
