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


def pins(path: Path) -> dict[str, str]:
    out = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = PIN.match(line)
        if m:
            out[m.group(1).lower().replace("_", "-")] = m.group(2)
    return out


class TestRequirements(unittest.TestCase):

    def test_everything_declared_is_pinned_with_double_equals(self):
        loose_ones = []
        for line in REQ.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if not PIN.match(line):
                loose_ones.append(line)
        self.assertEqual(loose_ones, [], f"dependencias sin clavar: {loose_ones}")

    def test_openai_is_declared(self):
        self.assertIn("openai", pins(REQ))

    def test_the_lock_exists_and_is_consistent(self):
        self.assertTrue(LOCK.is_file())
        self.assertEqual(pins(LOCK)["openai"], pins(REQ)["openai"])

    def test_the_lock_is_pinned_throughout(self):
        self.assertGreater(len(pins(LOCK)), 10)
        not_a_comment = [x for x in LOCK.read_text().splitlines()
                         if x.strip() and not x.strip().startswith("#")]
        self.assertEqual(len(not_a_comment), len(pins(LOCK)))

    @unittest.skipIf(OPENAI_INSTALADO is None, "openai no instalado (sin venv)")
    def test_the_installed_version_is_the_pinned_one(self):
        """If this fails, the live environment is no longer the records':
        either reinstall, or update the pin AND note the change."""
        self.assertEqual(OPENAI_INSTALADO, pins(REQ)["openai"])


if __name__ == "__main__":
    unittest.main()
