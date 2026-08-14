"""
The environment record that accompanies every results JSON.

It includes the check that really matters: that the `_env` block does not leak
the API key (hard rule 7). Only one environment variable is read,
`PYTHONHASHSEED`, and this test pins that in case somebody adds another without
thinking.

The last class walks the code looking for JSON writers and requires all of them
to hang their `_env`. It is what prevents the next script added from producing
records without provenance again, which is how the original debt came about.
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
          "git_commit", "git_dirty", "code_dirty", "code_digest"}

# Modules that dump a results JSON. The list is in the README, in the table
# "reproducing a figure overwrites its own record".
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
    # Added 2026-08-15 with the module. It does not close F1 of the optimizer
    # audit — this list still under-lists the writers the README table carries —
    # it only keeps the newest one from joining the omission.
    "peldano3.order_metrics_run",
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
        """`null` means "unset", that is, random. It is information."""
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
        """The digest is of the content: moving the repo does not change it."""
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
        """Changing a test changes no figure; the digest must not move because
        of it."""
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
        self.assertIsNone(e["code_dirty"])

    def test_dentro_del_repo_hay_commit(self):
        e = environment()
        self.assertRegex(e["git_commit"], r"^[0-9a-f]{40}$")
        self.assertIsInstance(e["git_dirty"], bool)
        self.assertIsInstance(e["code_dirty"], bool)


class TestLasDosBanderasDeSuciedad(unittest.TestCase):
    """`git_dirty` and `code_dirty` are not redundant, and the difference
    matters.

    Only `code_dirty` decides whether `git_commit` identifies the code that ran.
    `git_dirty` covers the rest, which is not always harmless: three writers
    read records from `results*/` as INPUT. Splitting them (Aug 7, 2026) came
    out of re-running six records back to back, where each script dirtied the
    tree for the next one with its own output.

    A fake repo is set up because the distinction cannot be provoked in the real
    one without dirtying it.
    """

    def setUp(self):
        import subprocess
        import tempfile

        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "harness").mkdir()
        (self.repo / "harness" / "x.py").write_text("y = 1\n")
        (self.repo / "results").mkdir()
        (self.repo / "results" / "cifra.json").write_text("{}\n")

        def git(*args):
            subprocess.run(("git", "-C", str(self.repo), *args),
                           check=True, capture_output=True)

        git("init", "-q")
        git("add", "-A")
        git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "base")

    def tearDown(self):
        self._tmp.cleanup()

    def _env(self):
        with mock.patch.object(provenance, "REPO", self.repo):
            return environment()

    def test_con_el_arbol_limpio_las_dos_son_falsas(self):
        e = self._env()
        self.assertEqual((e["git_dirty"], e["code_dirty"]), (False, False))

    def test_un_registro_modificado_ensucia_el_arbol_pero_no_el_codigo(self):
        """The batch case: one script's output does not invalidate the next
        one's commit, and until now the two looked the same."""
        (self.repo / "results" / "cifra.json").write_text('{"a": 1}\n')
        e = self._env()
        self.assertEqual((e["git_dirty"], e["code_dirty"]), (True, False))

    def test_el_codigo_modificado_ensucia_las_dos(self):
        (self.repo / "harness" / "x.py").write_text("y = 2\n")
        e = self._env()
        self.assertEqual((e["git_dirty"], e["code_dirty"]), (True, True))

    def test_un_fichero_de_codigo_sin_seguimiento_tambien_cuenta(self):
        """A new module without `git add` changes what runs just as a modified
        one does, and the digest already picks it up; the flag must too."""
        (self.repo / "harness" / "nuevo.py").write_text("z = 3\n")
        e = self._env()
        self.assertEqual((e["git_dirty"], e["code_dirty"]), (True, True))

    def test_la_linea_legible_distingue_los_dos_casos(self):
        with mock.patch.object(provenance, "REPO", self.repo):
            self.assertNotIn("sucio", describe())
            (self.repo / "results" / "cifra.json").write_text('{"a": 1}\n')
            self.assertIn("+arbol-sucio", describe())
            (self.repo / "harness" / "x.py").write_text("y = 2\n")
            self.assertIn("+codigo-sucio", describe())


class TestTodosLosEscritoresRegistranEntorno(unittest.TestCase):

    def test_los_escritores_conocidos_importan_environment(self):
        for nombre in ESCRITORES:
            with self.subTest(nombre):
                mod = importlib.import_module(nombre)
                self.assertIn("environment", vars(mod),
                              f"{nombre} no importa harness.provenance.environment")

    def test_ningun_escritor_de_JSON_se_queda_sin_env(self):
        """Discovers NEW writers: any `write_text(json.dumps(...))` in the code
        must carry its `_env` block alongside."""
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
