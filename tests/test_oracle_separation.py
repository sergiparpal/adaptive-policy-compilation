"""
ORACLE SEPARATION, checked over the imports.

`hidden_policy.py` declares itself thus: "this module is the ORACLE. It exists
to label the corpus and to measure offline. It must NEVER be consulted by the
rule engine, by the proposer or by any component of the online loop".

It is the claim on which the figures meaning anything depends, and until now it
lived only in a docstring. These tests make it mechanical: they read each
module's AST and look at who imports what. An import is enough to fail —it does
not need to be used— because an unused import is exactly what was in
`rung4/sweep.py` until August 6, 2026, contradicting in writing what
`FINDINGS4.md` claimed.

The same control covers the other end: in rung 4, `feedback.py` must remain the
ONLY module that touches the oracle. If it stops being so, "learning from
feedback" becomes full supervision under another name and the rung does not
measure what it says it measures.
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

ORACLE = {"hidden_policy", "true_action", "true_rule_id"}

# Components of the online loop: they see the case, decide and propose. None of
# them may consult the true policy.
ONLINE_LOOP = [
    "harness/dsl.py",
    "harness/domain.py",
    "harness/proposers.py",
    "rung2/engine2.py",
    "rung2/proposers2.py",
    "rung2/hidden_priority.py",
]


def imports_of(path: Path) -> set[str]:
    """Names imported by the module: both the module and the symbols."""
    tree = ast.parse(path.read_text(), filename=str(path))
    names: set[str] = set()
    for nodo in ast.walk(tree):
        if isinstance(nodo, ast.Import):
            for a in nodo.names:
                names.update(a.name.split("."))
        elif isinstance(nodo, ast.ImportFrom):
            if nodo.module:
                names.update(nodo.module.split("."))
            for a in nodo.names:
                names.add(a.name)
    return names


class TestTheOnlineLoopDoesNotSeeTheOracle(unittest.TestCase):

    def test_no_online_component_imports_the_policy(self):
        for rel in ONLINE_LOOP:
            with self.subTest(rel):
                filtered = imports_of(REPO / rel) & ORACLE
                self.assertEqual(filtered, set(),
                                 f"{rel} importa del oraculo: {filtered}")

    def test_the_watched_files_exist(self):
        """If somebody renames a module, the test above would silently stop
        watching it."""
        for rel in ONLINE_LOOP:
            with self.subTest(rel):
                self.assertTrue((REPO / rel).is_file(), f"falta {rel}")

    def test_who_may_see_it(self):
        """Measuring offline and labelling the record do consult the oracle. The
        test pins the list so that growing it is a decision, not an oversight."""
        allowed_names = {
            "harness/shadow.py",            # labels the record, does not decide
            "harness/cache_baseline.py",    # baseline: the LLM would be right
            "harness/ceiling_check.py",     # offline measurement
            "harness/subsumption_check.py",
            "harness/learned_subsumption.py",
            "run_experiment.py",
            "rung2/shadow2.py",
            "rung2/ceiling_check2.py",
            "rung3/order_search.py",
            "rung3/budget_and_balance.py",
            "rung3/optimizer_check.py",   # offline: the optimizer's own ceiling
            # offline: the weighted optimizer's ceiling. Added 2026-08-13, and
            # deliberately: it first tried to count the classes off the masks to
            # avoid this import, and the masks give the per-class CEILING, which
            # equals the class size only where every case is winnable — true of
            # the hidden policy, false of the 577 rules by 98 cases in 1005.
            # Avoiding the oracle bought nothing and cost a defect the gate
            # could not see.
            "rung3/optimizer_check_wt.py",
            "rung3/order_search_ls.py",   # offline: labels the two instances
            "rung4/feedback.py",
        }
        found = set()
        for root in ("harness", "rung2", "rung3", "rung4"):
            for f in (REPO / root).rglob("*.py"):
                if "__pycache__" in f.parts:
                    continue
                if imports_of(f) & ORACLE:
                    found.add(str(f.relative_to(REPO)))
        if imports_of(REPO / "run_experiment.py") & ORACLE:
            found.add("run_experiment.py")
        found.discard("harness/hidden_policy.py")
        self.assertEqual(found, allowed_names)


class TestTheRung4Channel(unittest.TestCase):
    """The channel is the artefact that contains the risk: if the oracle slips
    in somewhere else, rung 4 measures full supervision."""

    def test_feedback_is_the_only_rung_4_module_touching_the_oracle(self):
        tocan = {f.name for f in (REPO / "rung4").glob("*.py")
                 if imports_of(f) & ORACLE}
        self.assertEqual(tocan, {"feedback.py"})

    def test_the_learner_does_not_receive_the_truth(self):
        """`greedy_from_reports` only sees {case -> reported action}: its
        signature does not admit the true labels by any route."""
        import inspect

        from rung4.sweep import greedy_from_reports

        params = list(inspect.signature(greedy_from_reports).parameters)
        self.assertEqual(params, ["rules", "pool", "reported", "action", "born"])
        self.assertNotIn("truth", params)

    def test_the_channel_emits_less_than_the_truth(self):
        """Its output is strictly poorer: a subset of the cases, and with noise.
        With coverage 0 it emits nothing."""
        from harness.domain import generate_corpus
        from rung4.feedback import Channel

        corpus = generate_corpus(50, seed=17)
        window = list(range(50))
        decisions = {i: "T1_GENERAL" for i in window}
        empty = Channel(coverage=0.0, seed=1).observe(corpus, window, decisions)
        self.assertEqual(empty, {})
        full_one = Channel(coverage=1.0, asymmetry=1.0, seed=1).observe(
            corpus, window, decisions)
        self.assertLessEqual(len(full_one), len(window))

    def test_the_asymmetry_conditions_the_labels_on_the_errors(self):
        """With asymmetry 0 only INCORRECT decisions are observed. It is what
        keeps the channel from being the oracle, and what makes the labelled set
        not i.i.d."""
        from harness.domain import generate_corpus
        from harness.hidden_policy import true_action
        from rung4.feedback import Channel

        corpus = generate_corpus(200, seed=17)
        window = list(range(200))
        decisions = {i: true_action(corpus[i]) for i in window}   # perfect pi0
        rep = Channel(coverage=1.0, asymmetry=0.0, seed=1).observe(
            corpus, window, decisions)
        self.assertEqual(rep, {}, "una pi0 que no falla no genera etiqueta alguna")


if __name__ == "__main__":
    unittest.main()
