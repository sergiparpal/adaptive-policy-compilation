"""
`T-g1` to `T-g4` of `PLAN_STUDENTS.md` §8: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  T-g1  The material and the comparators are the records'. The suite is green.
        The answers recount as §1 declares them and as `results_ilp/labels.json`
        and `chosen.json` count rung 1's. Arrival order and its reverse
        reproduce `results3/floor_by_pool.json` on both surfaces, rung 1's own
        engine `order_search.json`'s 0.1829, and rung 3's search, run here with
        the truth on split 0's train half, the published `puro` row. Each
        `PLAN_REUSE.md` base, rebuilt, decides every case of its run as the
        record did, and the mask routes of the rules' side decide every corpus
        case as their engines do.
  T-g2  Each student gives the answer where it is known. The tree, handed the
        truth of the whole space, recovers the policy, and its leaves are a
        valid, disjoint, covering rule base the frozen engine executes as the
        tree predicts. The cache's protocol, run with the truth, gives
        `results/frontier.json`'s three cache rows, as the frozen file does.
        The regression's gradient is right and its fits reach their optimum.
        Every mask route matches point-by-point prediction.
  T-g3  Nothing a student reads holds the truth. Every set's labels are the
        record's `predicted`, and differ from the truth exactly where the
        record marks the proposal wrong. The fitting functions take tickets and
        labels and nothing else, and no module of `students/` imports the
        oracle.
  T-g4  The signature (`students/plan.py`). It does not block a dry run, which
        writes nothing; it blocks every write.

**What a dry run prints is pass or fail and figures that are already published
or known by construction.** It trains no student on the proposer's answers,
searches no order on them, and scores no base of `PLAN_REUSE.md`.
`tests/test_students.py` walks this module's syntax tree to say so: the names
that build or score a row never appear in it.
"""

from __future__ import annotations

import ast
import inspect
import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from harness.cache_baseline import _dist, run_cache_baseline
from harness.ceiling_check import all_cases
from harness.domain import ACTIONS, ATTRIBUTES, DOMAINS, Case
from harness.dsl import RuleEngine, validate_rule_payload
from reuse.gates import run_suite

from . import cache, logistic, material, plan, rules, tree

ORACLE = {"hidden_policy", "true_action", "true_rule_id"}


@dataclass
class Checks:
    tg1: dict
    tg2: dict
    tg3: dict
    tg4: dict
    extra: dict = field(default=None, repr=False)

    @property
    def blocking_pass(self) -> bool:
        return self.tg1["passes"] and self.tg2["passes"] and self.tg3["passes"]

    def summary(self) -> dict[str, Any]:
        return {k: {"passes": v["passes"], "what": v.get("what")}
                for k, v in (("T-g1", self.tg1), ("T-g2", self.tg2),
                             ("T-g3", self.tg3))} | {"T-g4": self.tg4}


def _published() -> dict[str, Any]:
    floors = json.loads(plan.FLOORS.read_text())["floors"]

    def floor(order, surface):
        return next(f["value"] for f in floors if f["order"] == order
                    and f["pool"] == "puro" and f["surface"] == surface)

    row = next(r for r in json.loads(plan.SPLITS.read_text())["splits"]
               if r["split"] == 0 and r["pool"] == "puro")
    refs = json.loads(plan.REFERENCES.read_text())["references_split0"]
    return {
        "arrival_test": floor("born_at", "corpus_test_split0"),
        "arrival_space": floor("born_at", "space"),
        "reversed_test": floor("born_at_reversed", "corpus_test_split0"),
        "reversed_space": floor("born_at_reversed", "space"),
        "specificity_test": refs["specificity_test"],
        "searched": {k: row[k] for k in ("ls_train", "ls_test", "ls_space")},
    }


# ---------------------------------------------------------------------------
# T-g1
# ---------------------------------------------------------------------------

def _labels_by_class(run: str) -> dict[str, dict[str, int]]:
    named = material.answers(run)
    t = material.truth()
    out: dict[str, dict[str, int]] = {}
    for i, q in named.items():
        d = out.setdefault(t[i], {})
        d[q] = d.get(q, 0) + 1
    return out


def _specificity_case(base: rules.Rung1, i: int, ncond: dict[str, int]) -> str | None:
    """Rung 1's engine on one corpus case, from its matched rules."""
    m = base.matched[i]
    if not m:
        return None
    top = max(ncond[r] for r in m)
    finalists = {base.action[r] for r in m if ncond[r] == top}
    return finalists.pop() if len(finalists) == 1 else None


def _decided_at(pred: dict[str, int], i: int, n: int) -> str | None:
    hits = [a for a, m in pred.items() if rules.bit(m, i, n)]
    return hits[0] if len(hits) == 1 else (None if not hits else "OVERLAP")


def published_problems(pub: dict[str, Any]) -> list[str]:
    """Where the records' figures are not the ones §4.2 of the plan quotes."""
    problems = []
    for key in ("arrival_test", "arrival_space", "reversed_test",
                "reversed_space", "specificity_test"):
        if pub[key] != plan.PUBLISHED[key]:
            problems.append(f"{key}: the record says {pub[key]}, the plan "
                            f"{plan.PUBLISHED[key]}")
    if pub["searched"] != plan.PUBLISHED["searched"]:
        problems.append("the searched row is not the plan's")
    return problems


def gate_tg1(suite: bool = True) -> dict[str, Any]:
    pub = _published()
    problems: list[str] = published_problems(pub)

    # The material.
    counted = {run: material.counts(run) for run in material.RUNS}
    for run, c in counted.items():
        if c != plan.MATERIAL[run]:
            problems.append(f"{run}: counts {c}, the plan says {plan.MATERIAL[run]}")
    labels_rec = json.loads(plan.LABELS.read_text())["proposer"]
    if (labels_rec["named_a_queue"], labels_rec["right"]) != (
            counted["rung1"]["answers"], counted["rung1"]["right"]):
        problems.append("rung 1's answers are not labels.json's")
    by_class = _labels_by_class("rung1")
    for cls, row in labels_rec["per_class"].items():
        published = {q: k for q, k in row["named"].items() if not q.startswith("(")}
        if by_class.get(cls, {}) != published:
            problems.append(f"{cls}: the answers by queue are not labels.json's")
    chosen_sets = json.loads(plan.CHOSEN.read_text())["training_sets"]
    if (chosen_sets["chosen_632"], chosen_sets["chosen_316"]) != (
            len(material.answer_set("rung1", "all").idx),
            len(material.answer_set("rung1", "train").idx)):
        problems.append("rung 1's two sets are not chosen.json's")
    for run in material.RUNS[1:]:
        m = material.record(run)["metrics"]
        if round(m["proposal_action_accuracy"] * m["escalations"]) != counted[run]["right"] \
                or m["escalations"] != counted[run]["answers"]:
            problems.append(f"{run}: the right answers are not the record's")
    if any(material.reached(material.answer_set(r, "train")) for r in material.RUNS):
        problems.append("a train half reaches the test split")

    # Rung 1's rules: arrival order, its reverse, its own engine, the search.
    base = rules.rung1()
    test_m = base.test_masks()
    space_m = base.space_masks()
    n_test, n_space = len(base.test), plan.N_SPACE
    got = {
        "arrival_test": rules.scored(base.arrival(), test_m),
        "arrival_space": rules.scored(base.arrival(), space_m),
        "reversed_test": rules.scored(base.reversed_arrival(), test_m),
        "reversed_space": rules.scored(base.reversed_arrival(), space_m),
    }
    if (got["arrival_test"], got["arrival_space"]) != (plan.ARRIVAL_TEST,
                                                       plan.ARRIVAL_SPACE):
        problems.append(f"arrival order scores {got['arrival_test']} and "
                        f"{got['arrival_space']}, not 519 and 42,310")
    for key, n in (("arrival_test", n_test), ("arrival_space", n_space),
                   ("reversed_test", n_test), ("reversed_space", n_space)):
        if round(got[key] / n, 6) != pub[key]:
            problems.append(f"{key}: {got[key]} of {n} is not {pub[key]}")
    spec = rules.specificity_test(base)
    if round(spec, 4) != pub["specificity_test"]:
        problems.append(f"rung 1's engine scores {spec}, not {pub['specificity_test']}")
    train = material.split()[0]
    best, st = rules.search_order(base, base.truth, train)
    searched = {"ls_train": round(st["best_score"] / len(train), 4),
                "ls_test": round(rules.scored(best, test_m) / n_test, 4),
                "ls_space": round(rules.scored(best, space_m) / n_space, 4)}
    if searched != pub["searched"]:
        problems.append(f"the search with the truth gives {searched}, not "
                        f"{pub['searched']}")

    # The mask routes of the rules' side, against their engines, case by case.
    corpus = material.corpus()
    spec_space = rules.specificity_space(base)
    ncond = {r["rule_id"]: len(r["conditions"]) for r in base.rules}
    spec_bad = sum(1 for i, c in enumerate(corpus)
                   if _decided_at(spec_space, rules.space_index(c), n_space)
                   != _specificity_case(base, i, ncond))
    if spec_bad:
        problems.append(f"rung 1's engine over the space disagrees with it on "
                        f"{spec_bad} corpus cases")
    reuse_rows = {}
    for run in material.RUNS[1:]:
        mism = rules.rebuild_mismatches(run)
        engine = rules.reuse_base(run).engine
        reg = rules.regions(engine)
        reg_bad = sum(1 for c in corpus
                      if _decided_at(reg, rules.space_index(c), n_space)
                      != rules.decide_action(engine, c))
        reuse_rows[run] = {"rules": len(engine.rules), "rebuild_mismatches": len(mism),
                           "region_mismatches": reg_bad}
        if mism or reg_bad:
            problems.append(f"{run}: the rebuild or the regions are not the run's")

    tests = run_suite() if suite else {"ran": False, "passes": None}
    if tests["passes"] is False:
        problems.append("the suite is not green")
    return {
        "what": "the material and the comparators are the records'; the suite green",
        "material": counted,
        "published": pub,
        "reproduced": got | {"specificity_test": spec, "searched": searched},
        "reuse_bases": reuse_rows,
        "suite": tests,
        "problems": problems,
        "passes": not problems,
    }


# ---------------------------------------------------------------------------
# T-g2
# ---------------------------------------------------------------------------

def _space_labels() -> list[str]:
    """The truth of every point, read off rung 3's masks: Step 0 of the tree."""
    n = plan.N_SPACE
    labels: list[str | None] = [None] * n
    for a, m in rules.space_truth().items():
        s = format(m, f"0{n}b")
        for i, ch in enumerate(s):
            if ch == "1":
                labels[i] = a
    return labels


def leaf_masks(fitted_tree) -> list[tuple[dict, int]]:
    sp = rules.space()
    out = []
    for payload in tree.rules(fitted_tree):
        rule = validate_rule_payload(payload)
        out.append((payload, sp.extension(rule.conditions)))
    return out


def tree_masks(fitted_tree) -> dict[str, int]:
    out: dict[str, int] = {}
    for payload, m in leaf_masks(fitted_tree):
        out[payload["action"]] = out.get(payload["action"], 0) | m
    return out


def partition_problems(leaves: list[tuple[dict, int]], full: int) -> list[str]:
    seen = 0
    problems = []
    for payload, m in leaves:
        if m & seen:
            problems.append(f"{payload['rule_id']} overlaps an earlier leaf")
        seen |= m
    if seen != full:
        problems.append("the leaves do not cover the space")
    return problems


def engine_of(payloads) -> RuleEngine:
    """The frozen engine, loaded with a tree's leaves as rules."""
    eng = RuleEngine()
    for k, p in enumerate(payloads):
        eng.add(validate_rule_payload(p), born_at=k)
    return eng


def engine_problems(fitted_tree, cases) -> int:
    """Cases the frozen engine does not decide by exactly one leaf, as the
    tree predicts."""
    eng = engine_of(tree.rules(fitted_tree))
    bad = 0
    for c in cases:
        outcome, winner, matched = eng.decide(c)
        if outcome != "ACTION" or len(matched) != 1 or winner.action != fitted_tree.predict(c):
            bad += 1
    return bad


def sample_points(n: int = plan.MASK_CHECK_POINTS, seed: int = plan.MASK_CHECK_SEED):
    rng = random.Random(seed)
    return sorted(rng.sample(range(plan.N_SPACE), n))


def synthetic(cases, seed: int = plan.SYNTHETIC_SEED) -> list[str]:
    """Labels that are neither the truth nor any answer: a fixed function of
    three attributes, with a seeded fifth of them drawn at random."""
    rng = random.Random(seed)
    out = []
    for c in cases:
        if rng.random() < 0.2:
            out.append(rng.choice(ACTIONS))
        else:
            k = (c.severity + DOMAINS["product"].index(c.product)
                 + DOMAINS["channel"].index(c.channel)) % 5
            out.append(ACTIONS[k])
    return out


def _fd_check(seed: int) -> float:
    """Worst relative gap between the analytic gradient and central differences,
    on a seeded synthetic instance."""
    rng = random.Random(seed)
    cases = [Case(**{a: rng.choice(DOMAINS[a]) for a in ATTRIBUTES}) for _ in range(120)]
    fd_labels = synthetic(cases, seed)
    X = [tree.encode(c) for c in cases]
    classes = [a for a in ACTIONS if a in set(fd_labels)]
    data = logistic._data(X, fd_labels, classes)
    C = len(classes)
    w = [rng.uniform(-0.5, 0.5) for _ in range(C * logistic.D)]
    _f, g = logistic.objective(w, data, C, 0.01)
    worst = 0.0
    for j in rng.sample(range(len(w)), 25):
        h = 1e-6
        wp, wm = list(w), list(w)
        wp[j] += h
        wm[j] -= h
        num = (logistic.objective(wp, data, C, 0.01)[0]
               - logistic.objective(wm, data, C, 0.01)[0]) / (2 * h)
        worst = max(worst, abs(num - g[j]) / max(1e-12, abs(num) + abs(g[j])))
    return worst


def gate_tg2() -> dict[str, Any]:
    problems: list[str] = []
    sp = rules.space()
    cases = list(all_cases())
    corpus = list(material.corpus())

    # The tree recovers the policy from the whole space, handed the truth.
    labels = _space_labels()
    t_space = tree.fit(cases, labels)
    right = sum(1 for c, l in zip(cases, labels) if t_space.predict(c) == l)
    leaves = leaf_masks(t_space.tree)
    part = partition_problems(leaves, sp.full)
    points = sample_points()
    eng_bad = engine_problems(t_space.tree, corpus + [cases[i] for i in points])
    if right != plan.N_SPACE:
        problems.append(f"the tree handed the space scores {right}")
    problems.extend(part)
    if eng_bad:
        problems.append(f"the frozen engine disagrees with the tree on {eng_bad} cases")
    tree_row = tree.describe(t_space) | {"right": right, "of": plan.N_SPACE,
                                         "engine_disagreements": eng_bad}

    # The cache is the frozen file's.
    truth = list(material.truth())
    frontier = json.loads(plan.FRONTIER.read_text())["results"]
    cache_rows = {}
    for d in plan.CACHE_DISTANCES:
        mine = cache.online(corpus, truth, d)
        frozen = run_cache_baseline(corpus, d)
        published = frontier[f"cache_{d}"]
        cache_rows[d] = mine == frozen == published
        if not cache_rows[d]:
            problems.append(f"the cache at d<={d} is not the frozen file's")
    rng = random.Random(plan.SYNTHETIC_SEED)
    pairs = [(rng.choice(cases), rng.choice(cases)) for _ in range(2000)]
    if any(cache.distance(a, b) != _dist(a, b) for a, b in pairs):
        problems.append("the cache's distance is not the frozen one")

    # The regression: its gradient, its optimum, its determinism.
    fd = _fd_check(plan.SYNTHETIC_SEED)
    if fd > 1e-5:
        problems.append(f"the gradient is off by {fd}")
    rng = random.Random(plan.SYNTHETIC_SEED + 1)
    syn_cases = [Case(**{a: rng.choice(DOMAINS[a]) for a in ATTRIBUTES})
                 for _ in range(300)]
    syn_labels = synthetic(syn_cases, plan.SYNTHETIC_SEED + 1)
    lr_a = logistic.fit(syn_cases, syn_labels)
    lr_b = logistic.fit(syn_cases, syn_labels)
    lr_row = logistic.describe(lr_a)
    if not (lr_a.fit.converged and lr_row["fold_fits_converged"]):
        problems.append("a fit of the regression did not converge")
    if lr_a.fit.w != lr_b.fit.w:
        problems.append("two fits of the regression differ")

    # Every mask route against point-by-point prediction, on synthetic labels.
    t_syn = tree.fit(syn_cases, syn_labels)
    c_syn = cache.fit(syn_cases, syn_labels)
    routes = {"tree": tree_masks(t_syn.tree), "cache": cache.space_masks(c_syn, sp)}
    mask_bad = {}
    for name, masks in routes.items():
        student = t_syn if name == "tree" else c_syn
        mask_bad[name] = sum(1 for i in points
                             if _decided_at(masks, i, plan.N_SPACE)
                             != student.predict(cases[i]))
    lr_masks = predictions_mask(lr_a, cases)
    mask_bad["logistic"] = sum(1 for i in points
                               if _decided_at(lr_masks, i, plan.N_SPACE)
                               != lr_a.predict(cases[i]))
    if any(mask_bad.values()):
        problems.append(f"a mask route disagrees with its student: {mask_bad}")
    if any(rules.space_index(cases[i]) != i for i in points):
        problems.append("space_index is not all_cases' order")

    return {
        "what": "each student gives the answer where it is known",
        "tree_on_the_space": tree_row,
        "tree_rules": len(leaves),
        "cache_rows_reproduced": cache_rows,
        "regression": {"finite_difference_worst": fd, "synthetic_fit": lr_row,
                       "deterministic": lr_a.fit.w == lr_b.fit.w},
        "mask_route_disagreements": mask_bad,
        "problems": problems,
        "passes": not problems,
    }


def predictions_mask(student, cases) -> dict[str, int]:
    """`{queue: points the student answers it on}`, point by point, in
    `Space`'s convention."""
    n = len(cases)
    flags = {a: bytearray(n) for a in ACTIONS}
    for i, c in enumerate(cases):
        flags[student.predict(c)][i] = 1
    return {a: int("".join(map(str, f)), 2) for a, f in flags.items() if any(f)}


# ---------------------------------------------------------------------------
# T-g3
# ---------------------------------------------------------------------------

def _imports(path: Path) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(), filename=str(path))):
        if isinstance(node, ast.Import):
            for a in node.names:
                names.update(a.name.split("."))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.update(node.module.split("."))
            for a in node.names:
                names.add(a.name)
    return names


def gate_tg3() -> dict[str, Any]:
    problems: list[str] = []
    t = material.truth()
    rows = {}
    for s in material.answer_sets():
        rec = {r["idx"]: r for r in material.record(s.run)["records"]}
        from_record = tuple(rec[i]["predicted"] for i in s.idx)
        wrong_marked = sum(1 for i in s.idx if rec[i]["proposal_action_correct"] is False)
        differ = sum(1 for i, q in zip(s.idx, s.labels) if q != t[i])
        rows[s.name] = {"examples": len(s.idx), "differ_from_truth": differ,
                        "marked_wrong": wrong_marked}
        if s.labels != from_record:
            problems.append(f"{s.name}: the labels are not the record's predicted")
        if differ != wrong_marked:
            problems.append(f"{s.name}: the labels differ from the truth "
                            f"{differ} times, the record marks {wrong_marked}")
    for name, fn in (("tree", tree.fit), ("logistic", logistic.fit),
                     ("cache", cache.fit)):
        if list(inspect.signature(fn).parameters) != ["cases", "labels"]:
            problems.append(f"{name}.fit admits more than tickets and labels")
    pkg = Path(__file__).resolve().parent
    leaking = sorted(f.name for f in pkg.glob("*.py") if _imports(f) & ORACLE)
    if leaking:
        problems.append(f"modules importing the oracle: {leaking}")
    return {"what": "nothing a student reads holds the truth",
            "sets": rows, "oracle_imports": leaking,
            "problems": problems, "passes": not problems}


# ---------------------------------------------------------------------------

def run_all(suite: bool = True) -> Checks:
    return Checks(gate_tg1(suite), gate_tg2(), gate_tg3(), plan.gate_signature())


def report(c: Checks) -> None:
    for name, g in (("T-g1", c.tg1), ("T-g2", c.tg2), ("T-g3", c.tg3)):
        print(f"  {name}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
        for p in g.get("problems", []):
            print(f"        - {p}")
    s = c.tg1.get("suite", {})
    if s.get("ran"):
        print(f"        suite: {s.get('tests')} tests, {s.get('result')}, "
              f"{s.get('seconds')} s")
    t = c.tg2["tree_on_the_space"]
    print(f"        the tree handed the space: {t['right']} of {t['of']}, "
          f"{t['leaves']} leaves of {t['full_leaves']}, k = {t['chosen_k']}")
    g4 = c.tg4
    print(f"  T-g4: {'PASS' if g4['passes'] else 'UNSIGNED'}  {g4['found']} "
          f"signature line(s), {g4['unsigned']} blank")
