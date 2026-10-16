"""
`H-g1` to `H-g4` of `PLAN_BOUND.md` §6: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  H-g1  The instances are the record's. The suite is green. Rebuilt here, every
        instance's coverage bound is the published one: 0.8784 and 0.8531 over
        the space, and each split's train ceiling to the last digit. Every
        published score is at most its bound, and every corpus score is a
        whole number of cases. And the signatures the certificate is built on
        score three random orders exactly as `score_order` does, on every
        instance: what the certificate bounds is what the search maximised.
  H-g2  The one instance whose optimum is known. On the hidden policy's pure
        pool the design order wins every case, so no cycle can exist: the
        certificate must find none, on the corpus and on the space. On its
        hybrid pool the certificate must verify and stay at or above what the
        design order and the greedy order score.
  H-g3  Validity where every order can be enumerated. On `BRUTE_INSTANCES`
        random instances of at most `BRUTE_MAX_RULES` rules, the certified bound
        is never below the exact optimum, `verify` accepts every certificate,
        and it refuses every certificate with a multiplicity inflated past a
        capacity.
  H-g4  The signature (`bound/plan.py`). It does not block a dry run, which
        writes nothing; it blocks every write.

**What a dry run prints is pass or fail and figures that are already
published**: the bounds and the searched scores of the records, and, for H-g2
and H-g3, figures about the hidden policy and synthetic instances. **H-g1 is the
only check that touches the 577 rules, and it never packs a cycle**: it builds
their signatures to score orders with, and prints nothing about them.
`tests/test_bound.py` walks this module's syntax tree to say so.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from reuse.gates import run_suite
from rung3.local_search import greedy_order_from_masks, random_order, score_order

from . import instances as I
from . import plan
from .certificate import (Instance, brute_force, certificate, classes,
                          signatures, verify)


@dataclass
class Checks:
    hg1: dict
    hg2: dict
    hg3: dict
    hg4: dict
    base: dict = field(default=None, repr=False)
    space: dict = field(default=None, repr=False)
    corpus: dict = field(default=None, repr=False)
    pub: dict = field(default=None, repr=False)

    @property
    def blocking_pass(self) -> bool:
        return self.hg1["passes"] and self.hg2["passes"] and self.hg3["passes"]

    def summary(self) -> dict[str, Any]:
        return {k: {"passes": v["passes"], "what": v.get("what")}
                for k, v in (("H-g1", self.hg1), ("H-g2", self.hg2),
                             ("H-g3", self.hg3))} | {"H-g4": self.hg4}


# ---------------------------------------------------------------------------
# The decomposition the certificate rests on, checked against the search
# ---------------------------------------------------------------------------

def score_by_signatures(inst: Instance, order: list[str], cls=None, sig=None) -> int:
    """An order's score read off the signatures: the uncontested cases, plus
    every signature whose first right class comes before its first wrong one.
    If this disagrees with `score_order` the certificate bounds something else."""
    cls = classes(inst) if cls is None else cls
    sig = signatures(inst, cls) if sig is None else sig
    rank_of = {rid: k for k, rid in enumerate(order)}
    crank = [min(rank_of[r] for r in members) for members, _, _ in cls]
    won = sig.uncontested
    for (r, x), w in zip(sig.keys, sig.weight):
        if min(crank[j] for j in r) < min(crank[j] for j in x):
            won += w
    return won


def plumbing(inst: Instance) -> bool:
    cls = classes(inst)
    sig = signatures(inst, cls)
    for k in range(plan.PLUMBING_ORDERS):
        order = random_order(inst.ids, seed=plan.PLUMBING_SEED + k)
        if score_by_signatures(inst, order, cls, sig) != score_order(
                order, inst.M, inst.W, inst.full):
            return False
    return True


def coverage(inst: Instance) -> int:
    reach = 0
    for rid in inst.ids:
        reach |= inst.W[rid]
    return reach.bit_count()


# ---------------------------------------------------------------------------
# H-g1
# ---------------------------------------------------------------------------

def gate_hg1(base, space, corpus, pub, suite: bool = True) -> dict:
    problems = []
    rows = {}
    for name, inst in space.items():
        p = pub["space"][name]
        cov = coverage(inst)
        ok = (round(cov / inst.n, 4) == p["bound"] and inst.n == plan.N_SPACE
              and p["attained"] <= p["bound"])
        sig_cov = signatures(inst).coverable
        ok = ok and sig_cov == cov
        plumb = plumbing(inst)
        rows[f"espacio/{name}"] = {"bound_published": p["bound"],
                                   "attained_published": p["attained"],
                                   "bound_reproduces": ok, "plumbing": plumb}
        if not (ok and plumb):
            problems.append(f"espacio/{name}")
    for (s, name), inst in corpus.items():
        p = pub["corpus"][(s, name)]
        cov = coverage(inst)
        whole = all(v is not None for v in p["sources"].values())
        ok = (abs(cov / inst.n - p["bound_share"]) < 1e-12 and inst.n == p["n"]
              and whole and p["attained"] <= cov)
        ok = ok and signatures(inst).coverable == cov
        plumb = plumbing(inst)
        rows[f"corpus train {s}/{name}"] = {
            "bound_published": round(p["bound_share"], 4),
            "attained_published": p["attained"], "n": p["n"],
            "sources": p["sources"], "bound_reproduces": ok, "plumbing": plumb}
        if not (ok and plumb):
            problems.append(f"corpus train {s}/{name}")
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": ("the suite is green; every instance's coverage bound is the "
                     "published one; every published score is a whole count at "
                     "or under its bound; the signatures score random orders as "
                     "score_order does"),
            "instances": rows, "problems": problems, "suite": tests,
            "passes": not problems and tests["passes"] is not False}


# ---------------------------------------------------------------------------
# H-g2
# ---------------------------------------------------------------------------

def gate_hg2() -> dict:
    rows = {}
    ok_all = True
    for key, (inst, design) in I.hidden_instances().items():
        cert = certificate(inst)
        v = verify(inst, cert)
        design_score = score_order(design, inst.M, inst.W, inst.full)
        greedy = greedy_order_from_masks(inst.ids, inst.M, inst.W, inst.full,
                                         tail_key=lambda r: r)
        greedy_score = score_order(greedy, inst.M, inst.W, inst.full)
        if key.endswith("puro"):
            ok = (v["ok"] and cert["nu"] == 0 and cert["coverable"] == inst.n
                  and design_score == inst.n)
        else:
            ok = (v["ok"] and cert["bound"] >= max(design_score, greedy_score))
        rows[key] = {"n": inst.n, "coverable": cert["coverable"], "nu": cert["nu"],
                     "bound": cert["bound"], "design_order": design_score,
                     "greedy_order": greedy_score, "verified": v["ok"],
                     "passes": ok}
        ok_all = ok_all and ok
    return {"what": ("the hidden policy: no cycle on its pure pool, where the "
                     "design order wins every case; on its hybrid pool the "
                     "certificate verifies and stays at or above two orders"),
            "instances": rows, "passes": ok_all}


# ---------------------------------------------------------------------------
# H-g3
# ---------------------------------------------------------------------------

def random_instance(rng: random.Random, n_rules: int, n_cases: int,
                    p_match: float, n_actions: int, copy: float = 0.2) -> Instance:
    """A small instance with a random truth and random rules, some of them
    copies of an earlier rule's extension under the same or another action,
    which is what makes classes and two-sided conflicts appear."""
    truth = [rng.randrange(n_actions) for _ in range(n_cases)]
    ids, M, W, prev = [], {}, {}, []
    for i in range(n_rules):
        if prev and rng.random() < copy:
            m, a = rng.choice(prev)
            if rng.random() < 0.5:
                a = rng.randrange(n_actions)
        else:
            m = sum(1 << c for c in range(n_cases) if rng.random() < p_match)
            a = rng.randrange(n_actions)
        rid = f"R{i:02d}"
        ids.append(rid)
        M[rid] = m
        W[rid] = sum(1 << c for c in range(n_cases)
                     if (m >> c) & 1 and truth[c] == a)
        prev.append((m, a))
    return Instance("sintetica", ids, M, W, n_cases)


def gate_hg3() -> dict:
    rng = random.Random(plan.BRUTE_SEED)
    below = tight = refused = mutated = with_cycles = 0
    for _ in range(plan.BRUTE_INSTANCES):
        inst = random_instance(rng, rng.randint(2, plan.BRUTE_MAX_RULES),
                               rng.randint(3, 30), rng.choice((0.3, 0.5, 0.7)),
                               rng.choice((2, 3, 4)))
        cert = certificate(inst)
        v = verify(inst, cert)
        opt = brute_force(inst)
        if not v["ok"] or cert["bound"] < opt:
            below += 1
        tight += cert["bound"] == opt
        if cert["cycles"]:
            with_cycles += 1
            bad = {**cert, "cycles": [list(c) for c in cert["cycles"]]}
            bad["cycles"][0] = [bad["cycles"][0][0] + inst.n, bad["cycles"][0][1]]
            bad["nu"] = cert["nu"] + inst.n
            mutated += 1
            refused += not verify(inst, bad)["ok"]
    return {"what": ("on random instances small enough to enumerate every order: "
                     "the certified bound is never below the exact optimum, every "
                     "certificate verifies, and an inflated one is refused"),
            "instances": plan.BRUTE_INSTANCES, "invalid": below,
            "tight": tight, "with_cycles": with_cycles,
            "inflated_refused": f"{refused} of {mutated}",
            "passes": below == 0 and refused == mutated}


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

def run_all(suite: bool = True) -> Checks:
    base = I.learned()
    space = I.space_instances(base)
    corpus = I.corpus_instances(base)
    pub = I.published()
    return Checks(hg1=gate_hg1(base, space, corpus, pub, suite=suite),
                  hg2=gate_hg2(), hg3=gate_hg3(), hg4=plan.gate_signature(),
                  base=base, space=space, corpus=corpus, pub=pub)


def report(c: Checks) -> None:
    mark = {True: "PASS", False: "FAIL", None: "—"}
    print("=" * 78)
    print(f"{plan.PLAN} — blocking checks (§6), zero API calls")
    print("=" * 78)
    g = c.hg1
    t = g["suite"]
    print(f"  H-g1  {mark[g['passes']]}  test suite: " + (
        f"{t['tests']} tests, {t['result']} ({t['seconds']} s)" if t["ran"]
        else "not run here"))
    for k, r in g["instances"].items():
        print(f"              {k:<24} bound {r['bound_published']}  searched "
              f"{r['attained_published']}  reproduces {r['bound_reproduces']}  "
              f"signatures score as score_order {r['plumbing']}")
    g = c.hg2
    print(f"  H-g2  {mark[g['passes']]}  the hidden policy:")
    for k, r in g["instances"].items():
        print(f"              {k:<16} n {r['n']}  coverable {r['coverable']}  "
              f"nu {r['nu']}  bound {r['bound']}  design {r['design_order']}  "
              f"greedy {r['greedy_order']}  verified {r['verified']}")
    g = c.hg3
    print(f"  H-g3  {mark[g['passes']]}  {g['instances']} enumerable instances: "
          f"{g['invalid']} invalid, {g['tight']} tight, {g['with_cycles']} with "
          f"cycles, inflated refused {g['inflated_refused']}")
    s = c.hg4
    print(f"  H-g4  {'SIGNED' if s['passes'] else 'UNSIGNED'}  {s['found']} "
          f"signature line(s), {s['unsigned']} blank"
          + ("" if s["passes"] else " — nothing may be scored or written"))
    print(f"\n  blocking checks: {'ALL PASS' if c.blocking_pass else 'FAILED'}")
