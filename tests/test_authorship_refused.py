"""
THE DECLARATIONS LEVEL 1 REFUSED — the reading and its gates, no figure.

**No figure is pinned here.** They live in `results_authorship/refused.json` and
in `results_authorship/FINDINGS_AUTHORSHIP.md`. What is pinned is what makes the
reading the one the module's docstring describes:

  * only `contradice_subsuncion` verdicts are read, each with its channel;
  * a pair is read over the narrower rule's region, the declared winner first,
    with each queue counted on its own on the corpus, so that a pair carrying
    one queue is a tie on both surfaces and never a direction;
  * the pooled rate leaves ties and pairs neither rule is ever right on apart;
  * the expectation is read clause by clause;
  * the module refuses while `PLAN_AUTHORSHIP.md` is unsigned, before it reads
    a record or writes anything.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from authorship import plan
from authorship import refused as rf

X, Y, S = "QUEUE_X", "QUEUE_Y", "SECURITY_INCIDENT"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def rules(**actions):
    return {rid: {"rule_id": rid, "action": a, "born_at": i * 10, "conditions": []}
            for i, (rid, a) in enumerate(actions.items())}


class TestWhatIsRead(unittest.TestCase):

    def test_only_the_refusals_with_their_channel(self):
        record = {"edge_log": [["W", "L", "contradice_subsuncion"], ["A", "B", "ok"],
                               ["C", "D", "no_solapan"], ["E", "F", "contradice_subsuncion"]],
                  "edge_channels": ["write", "write", "write", "order"]}
        self.assertEqual(rf.refused(record), [("W", "L", "write"), ("E", "F", "order")])

    def test_a_record_without_channels_is_all_write(self):
        record = {"edge_log": [["W", "L", "contradice_subsuncion"]]}
        self.assertEqual(rf.refused(record), [("W", "L", "write")])


class TestAPair(unittest.TestCase):
    # L is inside W: W covers points 0-3, L covers points 0-1.
    EXT = {"L": 0b0011, "W": 0b1111}

    def test_different_queues_over_the_narrower_region(self):
        rs = rules(L=X, W=Y)                       # L born first, W later
        tmask = {X: 0b0001, Y: 0b1110}             # on L's region: one X, one Y
        sets = [{"W", "L"}, {"W", "L"}, {"W", "L"}, {"W"}]
        truth = [Y, Y, X, Y]
        row = rf.read_pair("W", "L", "write", rs, self.EXT, tmask, sets, truth)
        self.assertTrue(row["strictly_inside"])
        self.assertEqual(row["being_born"], "winner")
        self.assertEqual(row["space"], {"region": 2, "truth_is_winner": 1,
                                        "truth_is_loser": 1, "better": "tie"})
        self.assertEqual(row["corpus"], {"region": 3, "truth_is_winner": 2,
                                         "truth_is_loser": 1, "better": "a"})

    def test_one_queue_is_a_tie_on_both_surfaces(self):
        rs = rules(L=X, W=X)
        tmask = {X: 0b0011, Y: 0b1100}
        sets = [{"W", "L"}] * 3
        truth = [X, X, Y]
        row = rf.read_pair("W", "L", "write", rs, self.EXT, tmask, sets, truth)
        self.assertTrue(row["same_queue"])
        self.assertEqual(row["space"]["better"], "tie")
        self.assertEqual(row["corpus"]["better"], "tie")

    def test_a_rule_missing_from_the_base_is_said_so(self):
        row = rf.read_pair("W", "L", "write", rules(L=X), self.EXT, {}, [], [])
        self.assertFalse(row["in_final_base"])


class TestPooled(unittest.TestCase):

    def test_ties_and_neither_are_apart(self):
        rows = [{"in_final_base": True, "space": {"better": v}}
                for v in ("a", "a", "b", "tie", "neither_ever_right")]
        got = rf.direction(rows, "space")
        self.assertEqual((got["winner_better"], got["loser_better"], got["tie"],
                          got["neither_ever_right"]), (2, 1, 1, 1))
        self.assertAlmostEqual(got["rate"], 2 / 3)

    def test_no_strict_pair_has_no_rate(self):
        rows = [{"in_final_base": True, "space": {"better": "tie"}}]
        self.assertIsNone(rf.direction(rows, "space")["rate"])


class TestTheExpectation(unittest.TestCase):

    def test_clause_by_clause(self):
        row = {"being_born": "winner", "same_queue": False, "queues": {"winner": S}}
        rows = [row] * 5 + [dict(row, same_queue=True, queues={"winner": X})] * 3
        got = {e["clause"]: e["holds"] for e in rf.read_expectation(
            rows, {"rate": 0.75}, {"rate": 0.5})}
        self.assertEqual(got, {"by construction": True, 1: True, "2, space": True,
                               "2, corpus": True, 3: True})
        fewer = rows[:2] + rows[5:]                # two of five differ, two name S
        got = {e["clause"]: e["holds"] for e in rf.read_expectation(
            fewer, {"rate": 0.5}, {"rate": None})}
        self.assertEqual(got, {"by construction": True, 1: False, "2, space": False,
                               "2, corpus": None, 3: False})
        older = [dict(row, being_born="loser")] + rows[1:]
        self.assertFalse(rf.read_expectation(older, {"rate": None},
                                             {"rate": None})[0]["holds"])


class TestUnsigned(unittest.TestCase):

    def test_it_refuses_before_reading_or_writing(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(rf.gates, "load",
                               side_effect=AssertionError("read")) as load, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                rf.main([])
        load.assert_not_called()
        write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
