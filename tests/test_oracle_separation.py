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

ORACULO = {"hidden_policy", "true_action", "true_rule_id"}

# Components of the online loop: they see the case, decide and propose. None of
# them may consult the true policy.
BUCLE_ONLINE = [
    "harness/dsl.py",
    "harness/domain.py",
    "harness/proposers.py",
    "rung2/engine2.py",
    "rung2/proposers2.py",
    "rung2/hidden_priority.py",
]


def imports_de(path: Path) -> set[str]:
    """Names imported by the module: both the module and the symbols."""
    arbol = ast.parse(path.read_text(), filename=str(path))
    nombres: set[str] = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            for a in nodo.names:
                nombres.update(a.name.split("."))
        elif isinstance(nodo, ast.ImportFrom):
            if nodo.module:
                nombres.update(nodo.module.split("."))
            for a in nodo.names:
                nombres.add(a.name)
    return nombres


class TestElBucleOnlineNoVeElOraculo(unittest.TestCase):

    def test_ningun_componente_online_importa_la_politica(self):
        for rel in BUCLE_ONLINE:
            with self.subTest(rel):
                filtrados = imports_de(REPO / rel) & ORACULO
                self.assertEqual(filtrados, set(),
                                 f"{rel} importa del oraculo: {filtrados}")

    def test_los_ficheros_vigilados_existen(self):
        """If somebody renames a module, the test above would silently stop
        watching it."""
        for rel in BUCLE_ONLINE:
            with self.subTest(rel):
                self.assertTrue((REPO / rel).is_file(), f"falta {rel}")

    def test_quien_si_puede_verlo(self):
        """Measuring offline and labelling the record do consult the oracle. The
        test pins the list so that growing it is a decision, not an oversight."""
        permitidos = {
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
        encontrados = set()
        for root in ("harness", "rung2", "rung3", "rung4"):
            for f in (REPO / root).rglob("*.py"):
                if "__pycache__" in f.parts:
                    continue
                if imports_de(f) & ORACULO:
                    encontrados.add(str(f.relative_to(REPO)))
        if imports_de(REPO / "run_experiment.py") & ORACULO:
            encontrados.add("run_experiment.py")
        encontrados.discard("harness/hidden_policy.py")
        self.assertEqual(encontrados, permitidos)


class TestElCanalDelRung4(unittest.TestCase):
    """The channel is the artefact that contains the risk: if the oracle slips
    in somewhere else, rung 4 measures full supervision."""

    def test_feedback_es_el_unico_del_rung_4_que_toca_el_oraculo(self):
        tocan = {f.name for f in (REPO / "rung4").glob("*.py")
                 if imports_de(f) & ORACULO}
        self.assertEqual(tocan, {"feedback.py"})

    def test_el_aprendiz_no_recibe_la_verdad(self):
        """`greedy_from_reports` only sees {case -> reported action}: its
        signature does not admit the true labels by any route."""
        import inspect

        from rung4.sweep import greedy_from_reports

        params = list(inspect.signature(greedy_from_reports).parameters)
        self.assertEqual(params, ["rules", "pool", "reported", "action", "born"])
        self.assertNotIn("truth", params)

    def test_el_canal_emite_menos_que_la_verdad(self):
        """Its output is strictly poorer: a subset of the cases, and with noise.
        With coverage 0 it emits nothing."""
        from harness.domain import generate_corpus
        from rung4.feedback import Channel

        corpus = generate_corpus(50, seed=17)
        ventana = list(range(50))
        decisiones = {i: "T1_GENERAL" for i in ventana}
        vacio = Channel(coverage=0.0, seed=1).observe(corpus, ventana, decisiones)
        self.assertEqual(vacio, {})
        lleno = Channel(coverage=1.0, asymmetry=1.0, seed=1).observe(
            corpus, ventana, decisiones)
        self.assertLessEqual(len(lleno), len(ventana))

    def test_la_asimetria_condiciona_las_etiquetas_a_los_errores(self):
        """With asymmetry 0 only INCORRECT decisions are observed. It is what
        keeps the channel from being the oracle, and what makes the labelled set
        not i.i.d."""
        from harness.domain import generate_corpus
        from harness.hidden_policy import true_action
        from rung4.feedback import Channel

        corpus = generate_corpus(200, seed=17)
        ventana = list(range(200))
        decisiones = {i: true_action(corpus[i]) for i in ventana}   # perfect pi0
        rep = Channel(coverage=1.0, asymmetry=0.0, seed=1).observe(
            corpus, ventana, decisiones)
        self.assertEqual(rep, {}, "una pi0 que no falla no genera etiqueta alguna")


if __name__ == "__main__":
    unittest.main()
