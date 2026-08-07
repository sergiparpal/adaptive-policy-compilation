"""
The dependencies are still pinned.

`requirements.txt` used to say `openai>=1.40.0`, which in practice means
"whichever was around on installation day". With that, rebuilding the
environment of a recorded run is impossible, and a run of the real proposer is
not reproducible even in principle. This test prevents the `>=` from coming back
by oversight.

The check against the live interpreter is skipped if `openai` is not installed:
Steps 0 and 1 and rungs 2, 3 and 4 run on the standard library and must not
require the venv in order to pass the tests.
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
        """If this fails, the live environment is no longer the records':
        either reinstall, or update the pin AND note the change."""
        self.assertEqual(OPENAI_INSTALADO, pines(REQ)["openai"])


if __name__ == "__main__":
    unittest.main()
