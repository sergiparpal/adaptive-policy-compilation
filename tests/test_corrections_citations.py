"""
`corrections/citations.py` — the POST-RUN audit of the citations on both sides:
what the readings that read declarations through `corrections/fall.py`'s
`declared` move. No figure of the audit.

What is pinned is the instrument:
- a rule an answer cites on both sides found, and one cited twice on one side
  not;
- the copy of a run: the side `declared` keeps leaves the rule's lists and its
  placement call's answer, so `declared` gives the other side, and nothing else
  changes; gate 2 passes on it and fails on a copy that changes more;
- the leaves where two records differ, and a record read but for `_env` and
  `source`;
- a pass over a reading built for the test: it reads the copies where the pass
  says so, writes where the pass says, is read as refused where it fails, and
  the pass puts every path back;
- the comparison of two passes: leaves moved, clauses flipped, a refusal;
- added after the first run: a pinned count let through, alone and by run,
  and a pass past the pins that lets a reading's gate 5 through, names the
  failing gate where it refuses, and puts the pin back;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from corrections import citations as CI
from corrections import fall as fl
from corrections import plan
from rung2.engine2 import EDGE_CYCLE, EDGE_OK
from tests.test_corrections_shape import UNSIGNED


def rule(rid, action, born, beats=(), loses_to=(), dropped=()):
    return {"rule_id": rid, "action": action, "born_at": born, "beats": list(beats),
            "loses_to": list(loses_to), "dropped_edges": list(dropped)}


def esc(idx, beats=(), loses_to=()):
    return {"idx": idx, "calls": [{"round": 0},
                                  {"round": 1, "payload": {"beats": list(beats),
                                                           "loses_to": list(loses_to)}}]}


# R2 cites R1 on both sides, above installed and below refused; R3 cites R1 twice
# on one side.
RECORD = {
    "rules": [rule("R1", "SECURITY_INCIDENT", 1),
              rule("R2", "T1_GENERAL", 2, beats=["R1"], dropped=[f"loses_to:R1:{EDGE_CYCLE}"]),
              rule("R3", "T2_TECHNICAL", 3, loses_to=["R1", "R1"])],
    "escalations": [esc(1), esc(2, beats=["R1"], loses_to=["R1"]), esc(3, loses_to=["R1"])],
    "edge_log": [["R2", "R1", EDGE_OK], ["R1", "R2", EDGE_CYCLE], ["R1", "R3", EDGE_OK]],
}


class TestTheCitationsOnBothSides(unittest.TestCase):

    def test_found_and_not(self):
        self.assertEqual(CI.both_sides(RECORD["rules"][1]),
                         {"R1": [("beats", EDGE_OK), ("loses_to", EDGE_CYCLE)]})
        self.assertEqual(CI.both_sides(RECORD["rules"][2]), {})
        got = CI.listed({"l_r1": RECORD})
        self.assertEqual([(f["run"], f["rule"], f["ref"], f["declared_keeps"]) for f in got],
                         [("l_r1", "R2", "R1", "loses_to")])


class TestTheCopy(unittest.TestCase):

    def test_the_kept_side_leaves_the_rule_and_the_answer(self):
        copy_, where = CI.other_side(RECORD)
        self.assertEqual(fl.declared(RECORD["rules"][1])["R1"], ("loses_to", EDGE_CYCLE))
        self.assertEqual(fl.declared(copy_["rules"][1])["R1"], ("beats", EDGE_OK))
        self.assertEqual(copy_["escalations"][1]["calls"][1]["payload"],
                         {"beats": ["R1"], "loses_to": []})
        self.assertEqual(copy_["edge_log"], RECORD["edge_log"])
        self.assertEqual(len(where), 1)
        self.assertEqual({d["path"] for d in CI.leaves(RECORD, copy_)}, CI.allowed(where))

    def test_the_record_is_not_touched(self):
        before = json.dumps(RECORD, sort_keys=True)
        CI.other_side(RECORD)
        self.assertEqual(json.dumps(RECORD, sort_keys=True), before)

    def test_gate_two(self):
        self.assertTrue(CI.gate_two({"l_r1": RECORD})["passes"])
        real = CI.other_side

        def more(record):
            copy_, where = real(record)
            copy_["rules"][0]["action"] = "T2_TECHNICAL"
            return copy_, where

        with mock.patch.object(CI, "other_side", side_effect=more):
            self.assertFalse(CI.gate_two({"l_r1": RECORD})["passes"])

    def test_gate_one(self):
        self.assertTrue(CI.gate_one({"l_r1": RECORD})["passes"])
        less = {**RECORD, "edge_log": RECORD["edge_log"][:1]}
        self.assertFalse(CI.gate_one({"l_r1": less})["passes"])


class TestTheLeaves(unittest.TestCase):

    def test_leaves(self):
        a = {"x": 1, "y": [1, 2], "z": {"w": "a"}, "only_a": 0}
        b = {"x": 1, "y": [1, 3], "z": {"w": "b"}, "only_b": 0}
        got = {d["path"]: (d["as_committed"], d["other_side"]) for d in CI.leaves(a, b)}
        self.assertEqual(got, {"y[1]": (2, 3), "z.w": ("a", "b"), "only_a": (0, None),
                               "only_b": (None, 0)})
        self.assertEqual(CI.leaves({"l": [1]}, {"l": [1, 2]}),
                         [{"path": "l", "as_committed": [1], "other_side": [1, 2]}])
        self.assertEqual(CI.leaves(a, a), [])

    def test_but_for_env_and_source(self):
        self.assertEqual(CI.without_env({"_env": 1, "source": 2, "runs": 3}), {"runs": 3})
        self.assertIsNone(CI.without_env(None))


def fake_reading(name: str, fail_on_copy: bool = False) -> types.ModuleType:
    """A reading that records which file `plan.run_path` gave it for L r1."""
    mod = types.ModuleType(f"corrections.{name}")
    mod.OUT = Path(tempfile.mkdtemp())

    def record_path():
        return mod.OUT / f"{name}.json"

    def main(argv=None):
        read = str(plan.run_path("l", 1))
        committed = read == str(plan.OUT / "loop_l_r1.json")
        if fail_on_copy and not committed:
            raise ValueError("cannot run")
        mod.record_path().write_text(json.dumps({"_env": {}, "read": read,
                                                 "expectation": [{"clause": "X1",
                                                                  "holds": committed}]}))
        return 0

    mod.record_path, mod.main = record_path, main
    return mod


class TestAPass(unittest.TestCase):

    def run_with(self, mods, name):
        runs = {"l_r1": RECORD}
        with mock.patch.object(CI, "ORDER", tuple(mods)), \
                mock.patch.dict(sys.modules, {f"corrections.{m}": mod for m, mod in mods.items()}):
            with tempfile.TemporaryDirectory() as tmp:
                return CI.run_pass(name, Path(tmp), runs)

    def test_the_pass_reads_the_copies_and_puts_every_path_back(self):
        mods = {"fake": fake_reading("fake")}
        run_path, record_path = plan.run_path, mods["fake"].record_path
        first = self.run_with(mods, "as_committed")
        second = self.run_with(mods, "other_side")
        self.assertEqual(first["fake"]["record"]["read"], str(plan.OUT / "loop_l_r1.json"))
        self.assertNotEqual(second["fake"]["record"]["read"], str(plan.OUT / "loop_l_r1.json"))
        self.assertTrue(second["fake"]["record"]["read"].endswith("loop_l_r1.json"))
        self.assertIs(plan.run_path, run_path)
        self.assertIs(mods["fake"].record_path, record_path)
        got = CI.compare(first["fake"], second["fake"])
        self.assertIsNone(got["refused"])
        self.assertEqual(got["clauses"], [{"clause": "X1", "as_committed": True,
                                           "other_side": False}])

    def test_a_reading_that_fails_is_read_as_refused(self):
        mods = {"fake": fake_reading("fake", fail_on_copy=True)}
        run_path = plan.run_path
        second = self.run_with(mods, "other_side")
        self.assertIsNotNone(second["fake"]["refused"])
        self.assertIsNone(second["fake"]["record"])
        self.assertIs(plan.run_path, run_path)
        got = CI.compare({"record": {}, "refused": None}, second["fake"])
        self.assertIsNotNone(got["refused"])
        self.assertIsNone(got["moved"])


def pinned_reading(name: str, pin: dict) -> types.ModuleType:
    """A reading with a development pin its gate 5 holds the run's counts to: the
    counts are what `plan.run_path` gave it."""
    mod = fake_reading(name)

    def main(argv=None):
        read = str(plan.run_path("l", 1))
        counts = {"committed": read == str(plan.OUT / "loop_l_r1.json")}
        if counts != mod.DEVELOPMENT:
            print("  gate 5 run l_r1: FAIL  the development set gives DEVELOPMENT's counts")
            raise SystemExit("REFUSED: a gate failed; nothing was written.")
        mod.record_path().write_text(json.dumps({"_env": {}, "development": counts}))
        return 0

    mod.main = main
    mod.DEVELOPMENT = pin
    return mod


class TestPastThePins(unittest.TestCase):
    """Added after the first run."""

    def test_a_pin_let_through(self):
        t = CI.Through({"a": 1})
        self.assertTrue({"a": 2} == t)
        self.assertTrue(t == {"a": 1})
        self.assertFalse({"a": 2} != t)
        self.assertEqual(CI.differed(t), {"compared": 3, "differed": True})
        self.assertEqual(dict(t), {"a": 1})

    def test_pins_by_run(self):
        pin = CI.let_through({"l_r1": {"a": 1}, "n_r3": {"a": 2}})
        self.assertIsInstance(pin, CI.ThroughByRun)
        self.assertTrue({"a": 9} == pin.get("l_r1"))
        self.assertIs(pin.get("l_r1"), pin.get("l_r1"))
        self.assertEqual(CI.differed(pin), {"l_r1": {"compared": 1, "differed": True}})
        self.assertIsInstance(CI.let_through({"a": 1}), CI.Through)
        self.assertEqual(json.loads(json.dumps(pin)), {"l_r1": {"a": 1}, "n_r3": {"a": 2}})

    def test_the_pass_lets_the_pin_through_and_puts_it_back(self):
        pin = {"committed": True}
        mods = {"fake": pinned_reading("fake", pin)}
        with mock.patch.object(CI, "PINNED", ("fake",)):
            second = TestAPass.run_with(self, mods, "other_side")
            third = TestAPass.run_with(self, mods, "past_the_pins")
        self.assertIn("gate 5 run l_r1: FAIL", second["fake"]["refused"])
        self.assertIsNone(third["fake"]["refused"])
        self.assertEqual(third["fake"]["record"]["development"], {"committed": False})
        self.assertEqual(third["fake"]["pin"], {"compared": 1, "differed": True})
        self.assertIs(mods["fake"].DEVELOPMENT, pin)


def readings(moved=None, refused=None, clauses=None):
    moved = moved or {}
    out = {}
    for m in CI.ORDER:
        out[m] = {"refused": (refused or {}).get(m), "moved": moved.get(m, 0),
                  "clauses": (clauses or {}).get(m, [])}
    return out


FOUND = [{"run": "l_r1", "rule": "R0159", "ref": "R0021"},
         {"run": "l_r2", "rule": "R0198", "ref": "R0176"}]


def holds(found, rd):
    return {c["clause"]: c["holds"] for c in CI.read_expectation(found, rd)}


class TestTheExpectation(unittest.TestCase):

    def test_inside_the_lines(self):
        self.assertEqual(set(holds(FOUND, readings({"gateway": 3, "above": 1})).values()), {True})

    def test_past_the_lines(self):
        got = holds(FOUND + [{"run": "n_r1", "rule": "R1", "ref": "R2"}],
                    readings({"gateway": 0, "above": 2, "fall": 1, "carry": 4},
                             clauses={"above": [{"clause": "E1"}]}))
        self.assertEqual(got, {"Z1": False, "Z2": False, "Z3": False, "Z4": False,
                               "Z5": False, "Z6": True})

    def test_a_refusal(self):
        got = holds(FOUND, readings({"gateway": 3, "above": 1}, refused={"conditions": "gate 1"}))
        self.assertEqual(got, {"Z1": True, "Z2": True, "Z3": True, "Z4": False, "Z5": False,
                               "Z6": False})

    def test_over_nothing(self):
        self.assertEqual(set(holds([], {}).values()), {False})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(CI, "records", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                CI.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
