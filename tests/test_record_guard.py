"""
The guard against overwriting the records that cannot be regenerated.

WHAT IT IS PROTECTING, AND WHY IT NEEDS ITS OWN TESTS

Until August 8, 2026 `run_experiment.py llm` wrote `results/llm_run.json`
whatever `--n` it was given, so `llm --n 100` — the cheap command the
getting-started recommends — destroyed the 2000-case record that is the input
of rungs 3 and 4. Money and non-determinism make that loss irreversible.

Three families here, and they answer different questions:

  * THE GUARD in isolation: what it refuses, what it lets through and what it
    says when it refuses. The message is part of the contract — a guard that
    aborts without saying what would be lost only teaches people to reach for
    the flag.

  * THE DESTINATIONS: that the naming rule no longer collides across `--n`, and
    that the guard fires from inside the commands BEFORE spending a call. That
    last one is the whole point: aborting after 632 calls would be worse than
    not guarding.

  * WHAT MUST NOT BE GUARDED: the deterministic, free records. Re-running them
    is the reproducibility check and a guard there would obstruct it. Rungs 3
    and 4 are pending a re-run with a serious optimizer, and that too must stay
    unobstructed.

Like the rest of the suite, this module writes nothing to `results*/`: it works
in temporary directories and the last class checks precisely that.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import run_experiment
from harness.record_guard import (
    FLAG,
    RecordExists,
    describe,
    refuse_overwrite,
    refuse_shrink,
)
from peldano2 import compare_runs, note_audit, run2

REPO = Path(__file__).resolve().parent.parent

# A record with everything the message quotes, in the shape rung 1 writes.
REGISTRO = {
    "_env": {"recorded_at": "2026-08-06T01:31:12Z", "n": 2000, "seed": 17},
    "model": "deepseek/deepseek-v4-flash",
    "metrics": {"n_rules": 577, "llm_calls": 632},
    "rules": [{"rule_id": f"r{i}"} for i in range(577)],
    "records": [{}] * 2000,
}


# One row of `compare_runs`, with the keys its report prints. It stands in for
# `analyse` so that no test has to read the eight real runs.
FILA = {
    "file": "llm_run2_n100.json", "seed": 17, "prompt_version": "v1",
    "n_rules": 30, "mean_conditions": 2.0, "cond_hist": {2: 30},
    "overlap_pct": 1.0, "overlapping_diff_action": 0, "nested_pairs": 0,
    "conflicts": 0, "impasses": 0, "edges_proposed": 0, "edges_accepted": 0,
    "edge_reasons": {}, "coverage": 0.5, "silent_error_rate": 0.1,
    "e2e": 0.5, "mean_ext_size": 100,
}


class ConDirectorioTemporal(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def escribir(self, nombre: str, dato) -> Path:
        p = self.dir / nombre
        p.write_text(json.dumps(dato))
        return p


# ---------------------------------------------------------------------------
# The guard on the destination
# ---------------------------------------------------------------------------

class TestRechazoDelDestino(ConDirectorioTemporal):

    def test_un_destino_libre_pasa_sin_ruido(self):
        destino = self.dir / "no_existe.json"
        self.assertEqual(refuse_overwrite(destino, overwrite=False), destino)

    def test_un_destino_ocupado_aborta(self):
        p = self.escribir("llm_run.json", REGISTRO)
        with self.assertRaises(RecordExists):
            refuse_overwrite(p, overwrite=False)

    def test_con_la_bandera_explicita_deja_pasar(self):
        p = self.escribir("llm_run.json", REGISTRO)
        self.assertEqual(refuse_overwrite(p, overwrite=True), p)

    def test_no_borra_ni_copia_nada_al_abortar(self):
        """Refuse by default and make NO automatic copy: silent backups pile up
        and people stop looking at them."""
        p = self.escribir("llm_run.json", REGISTRO)
        antes = sorted(x.name for x in self.dir.iterdir())
        huella = hashlib.sha256(p.read_bytes()).hexdigest()
        with self.assertRaises(RecordExists):
            refuse_overwrite(p, overwrite=False)
        self.assertEqual(sorted(x.name for x in self.dir.iterdir()), antes)
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), huella)

    def test_un_directorio_como_destino_tambien_aborta(self):
        (self.dir / "carpeta").mkdir()
        with self.assertRaises(RecordExists):
            refuse_overwrite(self.dir / "carpeta", overwrite=False)

    def test_un_json_ilegible_no_desactiva_la_guarda(self):
        """An unreadable file is still a file that would be lost. The failure
        degrades the description, it does not lift the refusal."""
        p = self.dir / "roto.json"
        p.write_text("{esto no es JSON")
        with self.assertRaises(RecordExists) as e:
            refuse_overwrite(p, overwrite=False)
        self.assertIn("no se pudo leer como JSON", str(e.exception))


class TestElMensajeDiceQueSePerderia(ConDirectorioTemporal):
    """A guard that aborts without saying what is at stake only teaches people
    to type the flag."""

    def mensaje(self, dato=REGISTRO, nombre="llm_run.json") -> str:
        p = self.escribir(nombre, dato)
        with self.assertRaises(RecordExists) as e:
            refuse_overwrite(p, overwrite=False,
                             exits=("--out OTRO", f"{FLAG} a proposito"))
        return str(e.exception)

    def test_nombra_el_fichero(self):
        self.assertIn("llm_run.json", self.mensaje())

    def test_lleva_fecha_modelo_casos_reglas_y_llamadas(self):
        m = self.mensaje()
        self.assertIn("2026-08-06T01:31:12Z", m)
        self.assertIn("deepseek/deepseek-v4-flash", m)
        self.assertIn("2000", m)
        self.assertIn("577", m)
        self.assertIn("632", m)

    def test_ofrece_las_dos_salidas(self):
        m = self.mensaje()
        self.assertIn("--out", m)
        self.assertIn(FLAG, m)

    def test_explica_que_no_se_puede_regenerar(self):
        self.assertIn("determinista", self.mensaje())

    def test_la_bandera_no_se_llama_force(self):
        """It must name what it does, so that it does not get typed out of
        habit."""
        self.assertEqual(FLAG, "--overwrite-record")
        self.assertNotIn("--force", self.mensaje())


class TestDescripcionDeRegistrosReales(unittest.TestCase):
    """Against the records on disk, read-only. Two of them —the ones that cost
    money— have no `_env`, which is exactly the case the description has to
    survive."""

    def test_el_registro_del_peldano_1_se_describe_entero(self):
        lineas = dict(describe(REPO / "results" / "llm_run.json"))
        self.assertEqual(lineas["modelo"], "deepseek/deepseek-v4-flash")
        self.assertEqual(lineas["casos"], "2000")
        self.assertEqual(lineas["reglas"], "577")
        self.assertEqual(lineas["llamadas al modelo"], "632")

    def test_sin_bloque_env_usa_la_fecha_del_fichero_y_lo_dice(self):
        """An mtime is weaker evidence than a `recorded_at` and must not pass
        for one."""
        lineas = dict(describe(REPO / "results" / "llm_run.json"))
        self.assertIn("no lleva bloque _env", lineas["registrado"])

    def test_el_registro_del_peldano_2_se_describe_entero(self):
        lineas = dict(describe(REPO / "results2" / "llm_run2_n100.json"))
        self.assertEqual(lineas["casos"], "100")
        self.assertEqual(lineas["semilla"], "17")


# ---------------------------------------------------------------------------
# The guard on the number of rows
# ---------------------------------------------------------------------------

class TestRechazoDelEncogimiento(ConDirectorioTemporal):
    """`compare_runs` and `note_audit` rewrite with whatever they are passed as
    an argument. The destination never changes, so the other check cannot see
    this one: what shrinks is the record."""

    def ocho_filas(self) -> Path:
        return self.escribir("comparativa.json", {
            "_env": {}, "rows": [{"file": f"llm_run2_{i}.json"} for i in range(8)]})

    def test_ocho_filas_por_ocho_pasan(self):
        refuse_shrink(self.ocho_filas(), [{}] * 8, overwrite=False)

    def test_mas_filas_pasan(self):
        refuse_shrink(self.ocho_filas(), [{}] * 9, overwrite=False)

    def test_una_fila_sobre_ocho_aborta(self):
        with self.assertRaises(RecordExists) as e:
            refuse_shrink(self.ocho_filas(), [{}], overwrite=False)
        self.assertIn("8", str(e.exception))
        self.assertIn("llm_run2_0.json", str(e.exception))

    def test_con_la_bandera_explicita_encoge(self):
        refuse_shrink(self.ocho_filas(), [{}], overwrite=True)

    def test_sin_registro_previo_no_hay_nada_que_encoger(self):
        refuse_shrink(self.dir / "no_existe.json", [{}], overwrite=False)

    def test_la_forma_antigua_de_lista_pelada_no_revienta(self):
        """Before Aug 7, 2026 these two records were a bare list. Nothing on
        disk is like that any more, but a guard that crashed on an old file
        would be worse than the loss it prevents."""
        p = self.escribir("viejo.json", [{"file": "a"}, {"file": "b"}])
        refuse_shrink(p, [{}], overwrite=False)


# ---------------------------------------------------------------------------
# The destinations of the commands
# ---------------------------------------------------------------------------

class TestElNombreDeSalidaYaNoColisiona(unittest.TestCase):

    def ruta(self, **kw) -> Path:
        args = argparse.Namespace(n=2000, seed=17, out=None)
        vars(args).update(kw)
        return run_experiment.llm_out_path(args)

    def test_el_humo_y_la_tirada_larga_escriben_ficheros_distintos(self):
        """The defect this whole change comes from."""
        self.assertNotEqual(self.ruta(n=100), self.ruta(n=2000))

    def test_la_n_va_en_el_nombre(self):
        self.assertEqual(self.ruta(n=100).name, "llm_run_n100.json")
        self.assertEqual(self.ruta(n=2000).name, "llm_run_n2000.json")

    def test_la_semilla_solo_aparece_si_no_es_la_fijada(self):
        self.assertEqual(self.ruta(n=100, seed=17).name, "llm_run_n100.json")
        self.assertEqual(self.ruta(n=100, seed=18).name,
                         "llm_run_n100_seed18.json")

    def test_ninguna_invocacion_por_defecto_apunta_al_registro_publicado(self):
        """`results/llm_run.json` is the input of rungs 3 and 4. Since Aug 8,
        2026 it is no longer the destination of anything: reaching it takes
        `--out` AND the flag."""
        for n in (50, 100, 500, 2000):
            self.assertNotEqual(self.ruta(n=n).name, "llm_run.json")

    def test_out_manda_sobre_todo_lo_demas(self):
        self.assertEqual(self.ruta(out="/tmp/x.json"), Path("/tmp/x.json"))


class TestLaEtiquetaDelPeldano2(unittest.TestCase):
    """The same defect on the other paid command, and worse: the rung 2 line
    the README recommends —`--n 100 --seed 17 --prompt-version v2`— wrote on
    top of the v1 record with that same name."""

    def test_reproduce_los_nombres_que_ya_estan_en_disco(self):
        for esperado, (n, seed, v) in {
            "n100": (100, 17, "v1"),
            "n100_v2": (100, 17, "v2"),
            "n100_seed18": (100, 18, "v1"),
            "n100_v2_seed18": (100, 18, "v2"),
        }.items():
            with self.subTest(esperado):
                self.assertEqual(run2.default_tag(n, seed, v), esperado)

    def test_los_ficheros_que_nombra_existen(self):
        """Not decoration: it is what makes the naming rule the same one the
        eight recorded runs already follow."""
        for tag in ("n100", "n100_v2", "n100_seed18", "n100_v2_seed18"):
            with self.subTest(tag):
                self.assertTrue(
                    (REPO / "results2" / f"llm_run2_{tag}.json").exists())

    def test_la_version_del_prompt_ya_no_colisiona(self):
        self.assertNotEqual(run2.default_tag(100, 17, "v1"),
                            run2.default_tag(100, 17, "v2"))


class TestAbortaAntesDeGastar(ConDirectorioTemporal):
    """The check runs at STARTUP. Aborting after 632 calls would be worse than
    not guarding at all, so what is measured here is that nobody was called."""

    def test_llm_aborta_sin_construir_el_proponente(self):
        (self.dir / "llm_run_n100.json").write_text(json.dumps(REGISTRO))
        args = argparse.Namespace(n=100, seed=17, provider="openrouter",
                                  model=None, out=None, overwrite_record=False)
        with mock.patch.object(run_experiment, "OUT", self.dir), \
                mock.patch.object(run_experiment, "run_shadow") as tirada, \
                mock.patch.object(run_experiment, "generate_corpus") as corpus, \
                self.assertRaises(SystemExit) as e:
            run_experiment.cmd_llm(args)
        tirada.assert_not_called()
        corpus.assert_not_called()
        self.assertIn("ABORTADO", str(e.exception))

    def test_llm_con_la_bandera_no_aborta(self):
        """The escape hatch has to work; otherwise the guard is a wall."""
        (self.dir / "llm_run_n100.json").write_text(json.dumps(REGISTRO))
        args = argparse.Namespace(n=100, seed=17, provider="openrouter",
                                  model=None, out=None, overwrite_record=True)
        with mock.patch.object(run_experiment, "OUT", self.dir), \
                mock.patch.object(run_experiment, "generate_corpus",
                                  side_effect=RuntimeError("paso la guarda")), \
                self.assertRaises(RuntimeError):
            run_experiment.cmd_llm(args)

    def test_run2_aborta_sin_construir_el_proponente(self):
        (self.dir / "llm_run2_n100.json").write_text(json.dumps(REGISTRO))
        argv = ["--n", "100"]
        with mock.patch.object(run2, "OUT", self.dir), \
                mock.patch.object(run2, "run_shadow2") as tirada, \
                mock.patch.object(run2, "OpenRouterProposer2") as prop, \
                mock.patch("sys.argv", ["run2", *argv]), \
                self.assertRaises(SystemExit) as e:
            run2.main()
        tirada.assert_not_called()
        prop.assert_not_called()
        self.assertIn("ABORTADO", str(e.exception))

    def test_la_guarda_del_llm_mira_el_destino_no_la_bandera(self):
        """`--out` onto an occupied file aborts just the same, otherwise it
        would be the way around the guard."""
        ocupado = self.dir / "otro.json"
        ocupado.write_text(json.dumps(REGISTRO))
        args = argparse.Namespace(n=100, seed=17, provider="openrouter",
                                  model=None, out=str(ocupado),
                                  overwrite_record=False)
        with mock.patch.object(run_experiment, "generate_corpus") as corpus, \
                self.assertRaises(SystemExit):
            run_experiment.cmd_llm(args)
        corpus.assert_not_called()


class TestElEncogimientoDesdeLosComandos(ConDirectorioTemporal):

    def preparar(self, modulo):
        registro = self.dir / "registro.json"
        registro.write_text(json.dumps(
            {"_env": {}, "rows": [{"file": f"r{i}.json"} for i in range(8)]}))
        return mock.patch.object(modulo, "RECORD", registro)

    def test_compare_runs_con_un_solo_fichero_aborta(self):
        with self.preparar(compare_runs), \
                mock.patch.object(compare_runs, "analyse", return_value={}), \
                self.assertRaises(SystemExit) as e:
            compare_runs.main(["results2/llm_run2_n100.json"])
        self.assertIn("MAS PEQUENO", str(e.exception))

    def test_note_audit_con_un_solo_fichero_aborta(self):
        with self.preparar(note_audit), \
                mock.patch.object(note_audit, "audit", return_value={}), \
                self.assertRaises(SystemExit) as e:
            note_audit.main(["results2/llm_run2_n100.json"])
        self.assertIn("MAS PEQUENO", str(e.exception))

    def test_aborta_antes_de_imprimir_el_informe(self):
        """Otherwise it prints a report suggesting everything went fine and
        then dies."""
        with self.preparar(compare_runs), \
                mock.patch.object(compare_runs, "analyse", return_value={}), \
                contextlib.redirect_stdout(io.StringIO()) as salida, \
                self.assertRaises(SystemExit):
            compare_runs.main(["uno.json"])
        self.assertEqual(salida.getvalue(), "")

    def test_la_bandera_no_se_cuela_como_nombre_de_fichero(self):
        vistos = []
        with self.preparar(compare_runs), \
                mock.patch.object(compare_runs, "analyse",
                                  side_effect=lambda p, s: vistos.append(p) or FILA), \
                contextlib.redirect_stdout(io.StringIO()):
            compare_runs.main(["uno.json", FLAG])
        self.assertEqual(vistos, [Path("uno.json")])


# ---------------------------------------------------------------------------
# What must NOT be guarded
# ---------------------------------------------------------------------------

class TestLoQueSeQuedaSinGuarda(unittest.TestCase):
    """Three levels, and only one needs a guard.

    Re-running the deterministic, free records IS the reproducibility check:
    that only `recorded_at` moves is the signal that everything still holds. And
    `order_search`, `budget_and_balance` and `sweep` are pending a re-run with a
    serious optimizer — that work is planned and the guard must not obstruct it.
    """

    LIBRES = [
        "harness.subsumption_check",
        "harness.learned_subsumption",
        "peldano2.ceiling_check2",
        "peldano3.order_search",
        "peldano3.budget_and_balance",
        "peldano4.sweep",
    ]

    def test_los_deterministas_y_gratis_no_importan_la_guarda(self):
        import importlib

        for nombre in self.LIBRES:
            with self.subTest(nombre):
                mod = importlib.import_module(nombre)
                self.assertNotIn("refuse_overwrite", vars(mod))

    def test_frontier_no_esta_guardado(self):
        """`run_experiment.py frontier` shares a module with `llm`, so it is
        checked by behaviour and not by import: it costs nothing and rewrites
        its own record on purpose."""
        import inspect

        fuente = inspect.getsource(run_experiment.cmd_frontier)
        self.assertNotIn("refuse_overwrite", fuente)


class TestLaSuiteNoEscribeEnResults(unittest.TestCase):
    """The suite rule, checked for this module in particular: everything above
    works in temporary directories."""

    RECORDS = ("results", "results2", "results3", "results4")

    def test_los_registros_siguen_intactos(self):
        for d in self.RECORDS:
            for f in sorted((REPO / d).glob("*.json")):
                with self.subTest(f.name):
                    # If any test above had written here, the mtime would have
                    # moved past the start of the process.
                    self.assertLess(f.stat().st_mtime, _ARRANQUE, f)


_ARRANQUE = __import__("time").time()


if __name__ == "__main__":
    unittest.main()
