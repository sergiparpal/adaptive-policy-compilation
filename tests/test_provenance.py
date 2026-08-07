"""
El registro de entorno que acompana a cada JSON de resultados.

Incluye la comprobacion que importa de verdad: que el bloque `_env` no filtra la
clave de la API (regla dura 7). Solo se lee una variable de entorno,
`PYTHONHASHSEED`, y esta prueba lo fija por si alguien anade otra sin pensarlo.

La ultima clase recorre el codigo buscando escritores de JSON y exige que todos
cuelguen su `_env`. Es lo que evita que el siguiente script que se anada vuelva
a producir registros sin procedencia, que es como se llego a la deuda original.
"""

from __future__ import annotations

import importlib
import json
import re
import unittest
from pathlib import Path
from unittest import mock

from harness import provenance
from harness.provenance import code_digest, describe, environment

REPO = Path(__file__).resolve().parent.parent

CLAVES = {"recorded_at", "python", "openai", "platform", "pythonhashseed",
          "git_commit", "git_dirty", "code_digest"}

# Modulos que vuelcan un JSON de resultados. La lista esta en el README, en la
# tabla "reproducir una cifra sobrescribe su propio registro".
ESCRITORES = [
    "run_experiment",
    "harness.subsumption_check",
    "harness.learned_subsumption",
    "peldano2.ceiling_check2",
    "peldano2.compare_runs",
    "peldano2.note_audit",
    "peldano2.run2",
    "peldano3.order_search",
    "peldano3.budget_and_balance",
    "peldano4.sweep",
]

CODE_ROOTS = ("harness", "peldano2", "peldano3", "peldano4", "run_experiment.py")


class TestEnvironment(unittest.TestCase):

    def test_lleva_las_claves_declaradas(self):
        self.assertEqual(set(environment()), CLAVES)

    def test_es_serializable_a_json(self):
        json.dumps(environment())

    def test_la_marca_de_tiempo_es_UTC_en_segundos(self):
        self.assertRegex(environment()["recorded_at"],
                         r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

    def test_admite_campos_extra(self):
        e = environment(seed=17, n=2000)
        self.assertEqual(e["seed"], 17)
        self.assertEqual(e["n"], 2000)

    def test_los_extra_pueden_sobreescribir(self):
        self.assertEqual(environment(python="3.99")["python"], "3.99")

    def test_recoge_PYTHONHASHSEED(self):
        with mock.patch.dict("os.environ", {"PYTHONHASHSEED": "7"}):
            self.assertEqual(environment()["pythonhashseed"], "7")

    def test_sin_PYTHONHASHSEED_queda_null(self):
        """`null` significa "sin fijar", es decir aleatorio. Es informacion."""
        with mock.patch.dict("os.environ", clear=True):
            self.assertIsNone(environment()["pythonhashseed"])

    def test_NO_filtra_la_clave_de_la_API(self):
        falsa = "sk-or-v1-000ESTOESUNSECRETO000"
        with mock.patch.dict("os.environ", {"OPENROUTER_API_KEY": falsa,
                                            "ANTHROPIC_API_KEY": falsa}):
            volcado = json.dumps(environment())
        self.assertNotIn(falsa, volcado)
        self.assertNotIn("API_KEY", volcado)

    def test_describe_es_una_linea(self):
        linea = describe()
        self.assertNotIn("\n", linea)
        self.assertIn("python", linea)


class TestCodeDigest(unittest.TestCase):

    def test_es_estable_entre_llamadas(self):
        self.assertEqual(code_digest(), code_digest())

    def test_tiene_la_longitud_declarada(self):
        self.assertEqual(len(code_digest()), provenance.DIGEST_CHARS)

    def test_cambia_si_cambia_el_codigo(self):
        with mock.patch.object(provenance, "REPO", Path(self.tmp)):
            uno = code_digest()
            (Path(self.tmp) / "harness" / "x.py").write_text("y = 2\n")
            dos = code_digest()
        self.assertNotEqual(uno, dos)

    def test_no_depende_del_nombre_del_directorio_raiz(self):
        """El digest es del contenido: mover el repo no lo cambia."""
        with mock.patch.object(provenance, "REPO", Path(self.tmp)):
            uno = code_digest()
        otro = Path(self.tmp2)
        (otro / "harness").mkdir(parents=True)
        (otro / "harness" / "x.py").write_text("y = 1\n")
        (otro / "run_experiment.py").write_text("pass\n")
        with mock.patch.object(provenance, "REPO", otro):
            dos = code_digest()
        self.assertEqual(uno, dos)

    def test_no_incluye_las_pruebas(self):
        """Cambiar una prueba no cambia ninguna cifra; el digest no debe
        moverse por ello."""
        self.assertNotIn("tests", provenance.CODE_ROOTS)

    def test_sin_fuentes_devuelve_None(self):
        with mock.patch.object(provenance, "REPO", Path(self.vacio)):
            self.assertIsNone(code_digest())

    def setUp(self):
        import tempfile

        self._dirs = [tempfile.TemporaryDirectory() for _ in range(3)]
        self.tmp, self.tmp2, self.vacio = (d.name for d in self._dirs)
        (Path(self.tmp) / "harness").mkdir()
        (Path(self.tmp) / "harness" / "x.py").write_text("y = 1\n")
        (Path(self.tmp) / "run_experiment.py").write_text("pass\n")

    def tearDown(self):
        for d in self._dirs:
            d.cleanup()


class TestGit(unittest.TestCase):

    def test_fuera_de_un_repo_no_revienta(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(provenance, "REPO", Path(tmp)):
                e = environment()
        self.assertIsNone(e["git_commit"])
        self.assertIsNone(e["git_dirty"])

    def test_dentro_del_repo_hay_commit(self):
        e = environment()
        self.assertRegex(e["git_commit"], r"^[0-9a-f]{40}$")
        self.assertIsInstance(e["git_dirty"], bool)


class TestTodosLosEscritoresRegistranEntorno(unittest.TestCase):

    def test_los_escritores_conocidos_importan_environment(self):
        for nombre in ESCRITORES:
            with self.subTest(nombre):
                mod = importlib.import_module(nombre)
                self.assertIn("environment", vars(mod),
                              f"{nombre} no importa harness.provenance.environment")

    def test_ningun_escritor_de_JSON_se_queda_sin_env(self):
        """Descubre escritores NUEVOS: cualquier `write_text(json.dumps(...))`
        del codigo debe llevar su bloque `_env` al lado."""
        sin_env = []
        for root in CODE_ROOTS:
            p = REPO / root
            ficheros = [p] if p.is_file() else [
                f for f in p.rglob("*.py") if "__pycache__" not in f.parts]
            for f in ficheros:
                src = f.read_text()
                if re.search(r"write_text\(\s*json\.dumps", src) and '"_env"' not in src:
                    sin_env.append(str(f.relative_to(REPO)))
        self.assertEqual(sin_env, [], f"escriben JSON sin procedencia: {sin_env}")


if __name__ == "__main__":
    unittest.main()
