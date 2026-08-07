"""
Que la suite la corra alguien sin que haya que acordarse.

Tener 227 pruebas y depender de que uno se acuerde de lanzarlas es tener menos
pruebas de las que parece. Hay dos redes, y cubren momentos distintos:

  * `.githooks/pre-commit`, antes de cada commit, en local.
  * `.github/workflows/pruebas.yml`, en cada push y cada PR, incluido lo que se
    empujo con `--no-verify`.

Esto vigila que las dos sigan ahi y sigan corriendo lo que dicen correr. Es
poca cosa, pero es exactamente el tipo de fallo que no avisa: un hook sin
permiso de ejecucion o un flujo renombrado no dan error, simplemente dejan de
correr y nadie se entera hasta que hace falta.

Lo que NO se comprueba aqui es que el hook este instalado: `core.hooksPath` es
configuracion local de cada clon y en CI no esta puesto. La instruccion de
instalarlo va en el README y en la cabecera del propio hook.
"""

from __future__ import annotations

import os
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

HOOK = REPO / ".githooks" / "pre-commit"
FLUJO = REPO / ".github" / "workflows" / "pruebas.yml"

SUITE = "unittest discover"


class TestElHookDePreCommit(unittest.TestCase):

    def test_existe(self):
        self.assertTrue(HOOK.is_file(), f"falta {HOOK.relative_to(REPO)}")

    def test_es_ejecutable(self):
        """Sin el bit de ejecucion git lo ignora en silencio."""
        self.assertTrue(os.access(HOOK, os.X_OK), "el hook no es ejecutable")

    def test_corre_la_suite(self):
        self.assertIn(SUITE, HOOK.read_text())

    def test_dice_como_instalarse(self):
        """El hook se versiona pero no se activa solo: `core.hooksPath` es
        configuracion de cada clon."""
        self.assertIn("core.hooksPath", HOOK.read_text())

    def test_no_necesita_el_venv(self):
        """Si el hook dependiera de `.venv`, un clon recien hecho no podria
        confirmar nada. La suite corre con la biblioteca estandar."""
        self.assertNotIn(".venv", HOOK.read_text())


class TestElFlujoDeCI(unittest.TestCase):

    def setUp(self):
        self.texto = FLUJO.read_text()

    def test_existe(self):
        self.assertTrue(FLUJO.is_file(), f"falta {FLUJO.relative_to(REPO)}")

    def test_corre_la_suite(self):
        self.assertIn(SUITE, self.texto)

    def test_se_dispara_en_push_y_en_pull_request(self):
        for evento in ("push:", "pull_request:"):
            with self.subTest(evento):
                self.assertIn(evento, self.texto)

    def test_cubre_el_minimo_de_python_que_declara_el_README(self):
        """Si alguien sube el suelo en el README, la matriz tiene que seguirle.
        Al reves tambien: una matriz que no incluya el minimo declarado deja la
        afirmacion del README sin comprobar."""
        readme = (REPO / "README.md").read_text()
        minimo = re.search(r"Python (\d+\.\d+)\+", readme)
        self.assertIsNotNone(minimo, "el README ya no declara version minima")
        self.assertIn(f'"{minimo.group(1)}"', self.texto)

    def test_comprueba_que_la_suite_no_escribe_en_los_registros(self):
        """La suite lo afirma en su docstring; el flujo lo verifica despues de
        correrla, que es la unica forma de que la afirmacion no envejezca."""
        self.assertIn("git status --porcelain -- results", self.texto)


if __name__ == "__main__":
    unittest.main()
