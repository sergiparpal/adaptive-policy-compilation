"""
SEPARACION DEL ORACULO, comprobada sobre los imports.

`hidden_policy.py` se declara a si mismo asi: "este modulo es el ORACULO. Sirve
para etiquetar el corpus y para medir offline. NUNCA debe ser consultado por el
motor de reglas, por el proponente ni por ningun componente del bucle online".

Es la afirmacion de la que depende que las cifras signifiquen algo, y hasta
ahora vivia solo en un docstring. Estas pruebas la vuelven mecanica: leen el AST
de cada modulo y miran quien importa que. Un import basta para suspender —no
hace falta que se use—, porque un import sin usar es exactamente lo que hubo en
`peldano4/sweep.py` hasta el 6 de agosto de 2026, contradiciendo por escrito lo
que afirmaba `FINDINGS4.md`.

El mismo control cubre el otro extremo: en el peldano 4, `feedback.py` debe
seguir siendo el UNICO modulo que toca el oraculo. Si deja de serlo, "aprender
del feedback" pasa a ser supervision completa con otro nombre y el peldano no
mide lo que dice medir.
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

ORACULO = {"hidden_policy", "true_action", "true_rule_id"}

# Componentes del bucle online: ven el caso, deciden y proponen. Ninguno puede
# consultar la politica verdadera.
BUCLE_ONLINE = [
    "harness/dsl.py",
    "harness/domain.py",
    "harness/proposers.py",
    "peldano2/engine2.py",
    "peldano2/proposers2.py",
    "peldano2/hidden_priority.py",
]


def imports_de(path: Path) -> set[str]:
    """Nombres importados por el modulo: tanto el modulo como los simbolos."""
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
        """Si alguien renombra un modulo, la prueba de arriba dejaria de
        vigilarlo en silencio."""
        for rel in BUCLE_ONLINE:
            with self.subTest(rel):
                self.assertTrue((REPO / rel).is_file(), f"falta {rel}")

    def test_quien_si_puede_verlo(self):
        """Medir offline y etiquetar el registro si consultan el oraculo. La
        prueba fija la lista para que crecer sea una decision, no un descuido."""
        permitidos = {
            "harness/shadow.py",            # etiqueta el registro, no decide
            "harness/cache_baseline.py",    # baseline: el LLM habria acertado
            "harness/ceiling_check.py",     # medicion offline
            "harness/subsumption_check.py",
            "harness/learned_subsumption.py",
            "run_experiment.py",
            "peldano2/shadow2.py",
            "peldano2/ceiling_check2.py",
            "peldano3/order_search.py",
            "peldano3/budget_and_balance.py",
            "peldano4/feedback.py",
        }
        encontrados = set()
        for root in ("harness", "peldano2", "peldano3", "peldano4"):
            for f in (REPO / root).rglob("*.py"):
                if "__pycache__" in f.parts:
                    continue
                if imports_de(f) & ORACULO:
                    encontrados.add(str(f.relative_to(REPO)))
        if imports_de(REPO / "run_experiment.py") & ORACULO:
            encontrados.add("run_experiment.py")
        encontrados.discard("harness/hidden_policy.py")
        self.assertEqual(encontrados, permitidos)


class TestElCanalDelPeldano4(unittest.TestCase):
    """El canal es el artefacto que contiene el riesgo: si el oraculo se cuela
    en otro sitio, el peldano 4 mide supervision completa."""

    def test_feedback_es_el_unico_del_peldano_4_que_toca_el_oraculo(self):
        tocan = {f.name for f in (REPO / "peldano4").glob("*.py")
                 if imports_de(f) & ORACULO}
        self.assertEqual(tocan, {"feedback.py"})

    def test_el_aprendiz_no_recibe_la_verdad(self):
        """`greedy_from_reports` solo ve {caso -> accion reportada}: su firma
        no admite las etiquetas verdaderas por ninguna via."""
        import inspect

        from peldano4.sweep import greedy_from_reports

        params = list(inspect.signature(greedy_from_reports).parameters)
        self.assertEqual(params, ["rules", "pool", "reported", "action", "born"])
        self.assertNotIn("truth", params)

    def test_el_canal_emite_menos_que_la_verdad(self):
        """Su salida es estrictamente mas pobre: un subconjunto de los casos, y
        con ruido. Con cobertura 0 no emite nada."""
        from harness.domain import generate_corpus
        from peldano4.feedback import Channel

        corpus = generate_corpus(50, seed=17)
        ventana = list(range(50))
        decisiones = {i: "T1_GENERAL" for i in ventana}
        vacio = Channel(coverage=0.0, seed=1).observe(corpus, ventana, decisiones)
        self.assertEqual(vacio, {})
        lleno = Channel(coverage=1.0, asymmetry=1.0, seed=1).observe(
            corpus, ventana, decisiones)
        self.assertLessEqual(len(lleno), len(ventana))

    def test_la_asimetria_condiciona_las_etiquetas_a_los_errores(self):
        """Con asimetria 0 solo se observan decisiones INCORRECTAS. Es lo que
        impide que el canal sea el oraculo, y lo que hace que el conjunto
        etiquetado no sea i.i.d."""
        from harness.domain import generate_corpus
        from harness.hidden_policy import true_action
        from peldano4.feedback import Channel

        corpus = generate_corpus(200, seed=17)
        ventana = list(range(200))
        decisiones = {i: true_action(corpus[i]) for i in ventana}   # pi0 perfecta
        rep = Channel(coverage=1.0, asymmetry=0.0, seed=1).observe(
            corpus, ventana, decisiones)
        self.assertEqual(rep, {}, "una pi0 que no falla no genera etiqueta alguna")


if __name__ == "__main__":
    unittest.main()
