"""
F1, CLOSED — the lists that name the record writers are derived from the tree,
not typed out beside it.

--------------------------------------------------------------------------
WHAT F1 WAS, AND WHY IT KEPT COMING BACK
--------------------------------------------------------------------------
[`results3/FINDINGS_AUDIT.md`](../results3/FINDINGS_AUDIT.md), finding **F1**:
*"`tests/test_provenance.py::WRITERS` and `tests/test_record_guard.py::FREE`
under-list the modules that write records, against the README table `WRITERS`
says it mirrors."* Reported, not fixed. **F7** then declared the README table
resolved — *"which now carries all three rows"* — and it was, on the day it was
written. Six days later the pairwise thread had added thirteen writers and none
of them reached the table, so the audit's own resolution had lapsed and nobody
knew until an audit on 2026-08-30 walked the tree by hand.

**That is the whole shape of the defect, and it is not carelessness.** Nobody did
anything wrong: a thread added modules and the list that claimed to mirror them
was somewhere else. **A claim that two things agree decays on its own unless
something checks it**, and in this repository everything that *is* checked —
`_env`, the code digest, oracle separation, the signed bands — has never drifted,
while three things asserted only in prose drifted in a single week.

So the lists are gone. `WRITERS` and `FREE` were deleted with this module; what
they asserted is asserted here over **every** writer the tree contains, which is
strictly more than either list ever held. Their per-entry notes said which record
each writer must never land on, and that belongs in the modules' own docstrings,
where it already is.

--------------------------------------------------------------------------
WHAT COUNTS AS A WRITER, AND WHY THE TEST FOR IT IS A REGEX
--------------------------------------------------------------------------
`write_text(json.dumps(...))` — the same pattern
`tests/test_provenance.py::test_no_JSON_writer_is_left_without_env` has used
since August 7 to discover new writers. It is syntactic, so a module that wrote
a record some other way would slip past; that is a known limit of the check and
not a new one, and `test_the_pattern_finds_what_it_claims_to` pins the pattern
against a module known to match.

--------------------------------------------------------------------------
`run_experiment.py` IS ONE FILE WITH TWO ANSWERS
--------------------------------------------------------------------------
It imports the guard — `run_experiment.py llm` refuses to overwrite a paid record
— and `run_experiment.py frontier` deliberately rewrites its own. The README
table therefore carries two rows for one module, and the guard check below keys
on modules while `tests/test_record_guard.py::test_frontier_is_not_guarded` keeps
checking the command by behaviour. It is the one place where a per-module
derivation is not the whole truth, and it is named rather than smoothed over.
"""

from __future__ import annotations

import ast
import importlib
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# The packages that produce figures — `harness.provenance.CODE_ROOTS`, which is
# the same list the code digest hashes. Imported rather than repeated: a second
# copy of this tuple is the defect this module exists to close.
from harness.provenance import CODE_ROOTS  # noqa: E402

WRITES_JSON = re.compile(r"write_text\(\s*json\.dumps")

# The one module that defines the guard rather than using it.
GUARD_MODULE = "harness/record_guard.py"
# The one writer whose commands disagree; see the module docstring.
TWO_ANSWERS = "run_experiment.py"


def _sources() -> list[Path]:
    out: list[Path] = []
    for root in CODE_ROOTS:
        p = REPO / root
        if p.is_file():
            out.append(p)
        elif p.is_dir():
            out.extend(f for f in p.rglob("*.py") if "__pycache__" not in f.parts)
    return sorted(out, key=lambda f: f.relative_to(REPO).as_posix())


def writers() -> set[str]:
    """Every module in the tree that writes a JSON record."""
    return {f.relative_to(REPO).as_posix() for f in _sources()
            if WRITES_JSON.search(f.read_text())}


def guarded() -> set[str]:
    """Every module that uses `record_guard.refuse_overwrite`."""
    return {f.relative_to(REPO).as_posix() for f in _sources()
            if "refuse_overwrite" in f.read_text()
            and f.relative_to(REPO).as_posix() != GUARD_MODULE}


def imports_of(path: Path) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(), filename=str(path))):
        if isinstance(node, ast.Import):
            for a in node.names:
                names.update(a.name.split("."))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.update(node.module.split("."))
            for a in node.names:
                names.add(a.name)
    return names


def readme_table() -> dict[str, str]:
    """The `reproducing a figure overwrites its own record` table, as
    `{module: guarded column}`. A row may name a command after the module —
    `run_experiment.py llm` — and the module is the part before the space."""
    rows: dict[str, str] = {}
    for m in re.finditer(r"^> \| `([^`]+?)` \| `[^`]+` \| (.+?) \|$",
                         (REPO / "README.md").read_text(), re.M):
        module = m.group(1).split(" ")[0]
        note = m.group(2)
        # Two rows for one module: guarded wins, and the command-level truth is
        # `test_record_guard.py::test_frontier_is_not_guarded`.
        if module in rows and "yes" in rows[module].lower():
            continue
        rows[module] = note
    return rows


class TestTheReadmeTableMirrorsTheTree(unittest.TestCase):
    """The check that would have caught the six-day drift on the day it started."""

    def test_every_writer_in_the_tree_is_in_the_table(self):
        missing = sorted(writers() - set(readme_table()))
        self.assertEqual(missing, [], f"writers absent from the README table: "
                                      f"{missing}")

    def test_every_row_of_the_table_is_a_writer_in_the_tree(self):
        """The other direction, which catches a module deleted or renamed while
        its row stayed behind."""
        extra = sorted(set(readme_table()) - writers())
        self.assertEqual(extra, [], f"rows with no writer behind them: {extra}")

    def test_the_table_is_not_trivially_empty(self):
        """A parser that silently matched nothing would make both tests above
        pass."""
        self.assertGreater(len(readme_table()), 30)
        self.assertGreater(len(writers()), 30)


class TestEveryWriterHangsItsEnvironment(unittest.TestCase):
    """What `WRITERS` asserted, over every writer instead of a chosen few."""

    def test_they_all_import_environment(self):
        for module in sorted(writers()):
            with self.subTest(module):
                self.assertIn("environment", imports_of(REPO / module))

    def test_the_module_object_carries_it_too(self):
        """The import could be shadowed or unused; this is the run-time half."""
        for module in sorted(writers()):
            name = module[:-3].replace("/", ".")
            with self.subTest(name):
                self.assertIn("environment", vars(importlib.import_module(name)))


class TestOnlyWhatCostsMoneyIsGuarded(unittest.TestCase):
    """What `FREE` asserted, derived. Re-running a deterministic free record IS
    the reproducibility check — that only `recorded_at` moves is the signal that
    everything still holds — so a guard on one would obstruct the thing it is
    there to protect."""

    def test_the_guarded_set_is_what_the_table_marks_guarded(self):
        marked = {m for m, note in readme_table().items()
                  if "yes" in note.lower()}
        self.assertEqual(guarded(), marked)

    def test_the_guarded_writers_are_the_ones_that_spend(self):
        """Three modules, and each of them costs API calls: the rung 1 run, the
        rung 2 runs, and the only module in the repository that spends."""
        self.assertEqual(guarded(), {"run_experiment.py", "rung2/run2.py",
                                     "rung2/pair_judgement.py"})

    def test_no_free_writer_imports_the_guard(self):
        for module in sorted(writers() - guarded()):
            with self.subTest(module):
                self.assertNotIn("refuse_overwrite",
                                 (REPO / module).read_text())

    def test_the_module_that_defines_the_guard_is_not_counted_as_using_it(self):
        self.assertNotIn(GUARD_MODULE, guarded())
        self.assertIn("refuse_overwrite", (REPO / GUARD_MODULE).read_text())


class TestTheDerivationItself(unittest.TestCase):
    """A derived list is only as good as its derivation, so the derivation is
    checked rather than trusted — the same reason `A-g3` exists in
    `PLAN_SENSITIVITY.md`."""

    def test_the_pattern_finds_what_it_claims_to(self):
        self.assertIn("rung3/order_search.py", writers())
        self.assertNotIn("harness/dsl.py", writers())

    def test_it_walks_the_roots_the_digest_hashes(self):
        """If a new package produced figures and were not in `CODE_ROOTS`, its
        records would carry a digest that ignored the code that made them — and
        this module would not see its writers either. One tuple, two jobs."""
        self.assertIn("sensitivity", CODE_ROOTS)
        self.assertIn("ilp", CODE_ROOTS)
        for module in writers():
            with self.subTest(module):
                self.assertTrue(any(module == r or module.startswith(r + "/")
                                    for r in CODE_ROOTS))

    def test_run_experiment_is_the_one_module_with_two_answers(self):
        """It is guarded and one of its commands is not, so the README carries
        two rows for it. Named here so that a future reader does not read the
        collapse as a bug."""
        self.assertIn(TWO_ANSWERS, guarded())
        rows = [m for m in re.findall(r"^> \| `([^`]+?)` \|",
                                      (REPO / "README.md").read_text(), re.M)
                if m.split(" ")[0] == TWO_ANSWERS]
        self.assertEqual(len(rows), 2)


if __name__ == "__main__":
    unittest.main()
