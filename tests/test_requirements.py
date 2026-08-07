"""
Las dependencias siguen clavadas.

`requirements.txt` decia `openai>=1.40.0`, que en la practica significa "la que
hubiera el dia de la instalacion". Con eso, reconstruir el entorno de una tirada
registrada es imposible, y una tirada del proponente real no es reproducible ni
en principio. Esta prueba impide que el `>=` vuelva por descuido.

La comprobacion contra el interprete vivo se salta si `openai` no esta
instalado: los Pasos 0 y 1 y los peldanos 2, 3 y 4 corren con la biblioteca
estandar y no deben exigir el venv para pasar las pruebas.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REQ = REPO / "requirements.txt"
LOCK = REPO / "requirements.lock.txt"

PIN = re.compile(r"^([A-Za-z0-9_.\-]+)\s*==\s*([0-9][^\s#]*)\s*$")

try:
    from importlib.metadata import version as _version

    OPENAI_INSTALADO = _version("openai")
except Exception:                                   # noqa: BLE001
    OPENAI_INSTALADO = None


def pines(path: Path) -> dict[str, str]:
    out = {}
    for linea in path.read_text().splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        m = PIN.match(linea)
        if m:
            out[m.group(1).lower().replace("_", "-")] = m.group(2)
    return out


class TestRequirements(unittest.TestCase):

    def test_todo_lo_declarado_esta_clavado_con_igual_igual(self):
        sueltas = []
        for linea in REQ.read_text().splitlines():
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            if not PIN.match(linea):
                sueltas.append(linea)
        self.assertEqual(sueltas, [], f"dependencias sin clavar: {sueltas}")

    def test_openai_esta_declarado(self):
        self.assertIn("openai", pines(REQ))

    def test_el_lock_existe_y_es_consistente(self):
        self.assertTrue(LOCK.is_file())
        self.assertEqual(pines(LOCK)["openai"], pines(REQ)["openai"])

    def test_el_lock_esta_entero_clavado(self):
        self.assertGreater(len(pines(LOCK)), 10)
        no_comentario = [x for x in LOCK.read_text().splitlines()
                         if x.strip() and not x.strip().startswith("#")]
        self.assertEqual(len(no_comentario), len(pines(LOCK)))

    @unittest.skipIf(OPENAI_INSTALADO is None, "openai no instalado (sin venv)")
    def test_la_version_instalada_es_la_clavada(self):
        """Si esto falla, el entorno vivo ya no es el de los registros: o se
        reinstala, o se actualiza el pin Y se anota el cambio."""
        self.assertEqual(OPENAI_INSTALADO, pines(REQ)["openai"])


if __name__ == "__main__":
    unittest.main()
