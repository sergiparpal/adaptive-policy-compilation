"""A smoke test of the Distiller's rerun file (sergiparpal/distiller, task 19).

Not to be merged: it lives on a pull request that is closed after its shadow
run, and that run's record is deleted, as PR 184's was. Its two tests fail
only in the distiller workflow's shadow job, where GITHUB_JOB is "shadow", so
the suite stays green everywhere else, the pre-commit hook and ci-complete
included.
"""

import os
import unittest
from pathlib import Path

IN_SHADOW = os.environ.get("GITHUB_JOB") == "shadow"
MARK = Path(os.environ.get("RUNNER_TEMP", "/nonexistent")) / "distiller-rerun-smoke-mark"


@unittest.skipUnless(IN_SHADOW, "only in the distiller workflow's shadow job")
class TestTheRerunFile(unittest.TestCase):

    def test_fails_once_then_passes(self):
        """Fails in the full run and passes in the rerun: not reproduced."""
        if not MARK.exists():
            MARK.write_text("seen\n")
            self.fail("the first run in this job fails on purpose")

    def test_fails_every_time(self):
        """Fails in both runs: a failure that the rerun confirms."""
        self.fail("fails on purpose in every run of the shadow job")
