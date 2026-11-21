"""
`ranked/sides.py` — the POST-RUN reading of why the copies' declared sides
closed cycles. No figure of the reading.

What is pinned is the instrument:
- one shortest path, on engines built by hand: as long as the path helper
  counts, the lowest-numbered step first on a tie, and none where none is;
- the originals' order against the other rule, on a win and on a loss:
  repeats, contradicts, both and unordered;
- what the rules at the copy include;
- the replay on records built by hand over the real space: a copy's win
  refused through a rule nested in it, which contradicts its original's order,
  and a copy's loss refused through its own win, which repeats it; each read
  where it was tried, every side tallied by its verdict, and gates 1, 3 and 4
  kept, with teeth;
- one run read whole: the refused sides summed, the rules at the copy, the
  doors with their births, the copy that costs most read off `copies.json`'s
  `alone`, and the record's rows without the paths' rules;
- gate 2 on K r3's record against `copies.json`'s rows, with teeth;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import json
import unittest
from unittest import mock

from manual import instrument as MI
from ranked import copies as CO
from ranked import plan
from ranked import refusals as RF
from ranked import sides as SD
from tests.test_ranked_copies import (BILL, MOBILE, MOBILE_PRO, SEV2, SS, T1, UNSIGNED, esc,
                                      refused_record, rows, rule)
from tests.test_ranked_refusals import Engine, flip

PRO = [{"attr": "customer_tier", "op": "eq", "value": "pro"}]


def win_record():
    """`refused_record`: R3, a copy of R1, declares itself above R2, which
    already reaches R3 through R4, nested in R3 and in R1. R4 erred at R3's
    ticket."""
    r = refused_record()
    r["records"][4]["engine_rule"] = "R4"
    return r


def loss_record():
    """R2 declared itself above R1, and R5 above R2. R3, a copy of R1, declares
    itself above R5, installed, then below R2, refused: R3 reaches R2 through
    its own win over R5. R1 already stood below R2."""
    r = {"arm": "l",
         "rules": [rule("R1", BILL, 1, MOBILE), rule("R2", SS, 2, SEV2, beats=["R1"]),
                   rule("R5", T1, 3, PRO, beats=["R2"]),
                   dict(rule("R3", BILL, 4, MOBILE, beats=["R5"]),
                        dropped_edges=["loses_to:R2:cierra_ciclo"])],
         "escalations": [esc(1, "R1", [], kind="IMPASSE"), esc(2, "R2", [], kind="IMPASSE"),
                         esc(3, "R5", [], kind="IMPASSE"), esc(4, "R3", ["R1"])],
         "records": rows(),
         "edge_log": [["R2", "R1", "ok"], ["R5", "R2", "ok"], ["R3", "R5", "ok"],
                      ["R2", "R3", "cierra_ciclo"]]}
    r["records"][2]["edge_reasons"] = ["ok"]
    r["records"][3]["edge_reasons"] = ["ok"]
    r["records"][4]["edge_reasons"] = ["ok", "cierra_ciclo"]
    return r


class TestOnePath(unittest.TestCase):

    def test_shortest_and_lowest_first(self):
        # L -> A -> W, L -> B -> W and L -> C -> X -> W.
        eng = Engine({"W": 0b1111, "L": 0b0110, "A": 0b0011, "B": 0b0101, "C": 0b0100,
                      "X": 0b0001},
                     declared=[("L", "B"), ("L", "A"), ("L", "C"), ("A", "W"), ("B", "W"),
                               ("C", "X"), ("X", "W")])
        nodes = SD.CP.forward(eng, "L") & SD.CP.backward(eng, "W")
        got = SD.one_path(eng, "L", "W", nodes)
        self.assertEqual(got, ["L", "A", "W"])
        self.assertEqual(len(got) - 1, SD.CP.shortest(eng, "L", "W", nodes))

    def test_only_through_the_nodes(self):
        eng = Engine({"W": 0b111, "L": 0b110, "A": 0b011, "X": 0b001},
                     declared=[("L", "A"), ("A", "W"), ("L", "X"), ("X", "W")])
        self.assertEqual(SD.one_path(eng, "L", "W", {"L", "X", "W"}), ["L", "X", "W"])

    def test_none_and_itself(self):
        eng = Engine({"W": 0b011, "L": 0b110})
        self.assertIsNone(SD.one_path(eng, "L", "W", {"L", "W"}))
        self.assertEqual(SD.one_path(eng, "L", "L", {"L"}), ["L"])


class TestTheOriginalsOrder(unittest.TestCase):

    EXT = {"C": 0b0011, "O": 0b0011, "P": 0b0011, "X": 0b0110}

    def order(self, newborn_wins, declared, originals=("O",)):
        eng = Engine(self.EXT, declared=declared)
        w, l = ("C", "X") if newborn_wins else ("X", "C")
        return SD.original_order(eng, w, l, "C", list(originals))

    def test_on_a_win(self):
        self.assertEqual(self.order(True, [("X", "O")]), SD.CONTRADICTS)
        self.assertEqual(self.order(True, [("O", "X")]), SD.REPEATS)

    def test_on_a_loss(self):
        self.assertEqual(self.order(False, [("X", "O")]), SD.REPEATS)
        self.assertEqual(self.order(False, [("O", "X")]), SD.CONTRADICTS)

    def test_both_and_neither(self):
        self.assertEqual(self.order(True, [("X", "O"), ("P", "X")], ("O", "P")), SD.BOTH)
        self.assertEqual(self.order(True, []), SD.UNORDERED)


class TestThrough(unittest.TestCase):

    def test_what_the_rules_at_the_copy_include(self):
        births = {"A": {"queue": BILL, "right_at_birth": True},
                  "B": {"queue": SS, "right_at_birth": False},
                  "D": {"queue": BILL, "right_at_birth": True}}
        copy = {"queue": BILL, "erring": "B"}
        got = SD.through({"nested_at_newborn": ["A", "B"]}, births, copy, {"D"})
        self.assertEqual(got, {"another_queue": True, "wrong_at_its_birth": True,
                               "the_rule_that_erred": True, "a_copy": False})
        got = SD.through({"nested_at_newborn": ["D"]}, births, {"queue": BILL, "erring": None},
                         {"D"})
        self.assertEqual(got, {"another_queue": False, "wrong_at_its_birth": False,
                               "the_rule_that_erred": False, "a_copy": True})
        self.assertEqual(SD.through({"nested_at_newborn": []}, births, copy, set()),
                         {k: False for k in SD.THROUGH})


class TestTheReplay(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space = MI.space()
        cls.mobile = cls.space.extension([CO.TW.Condition(**c) for c in MOBILE])
        cls.truth = {BILL: cls.mobile}

    def replay(self, r):
        copies, ok = CO.copies_of_run(r, self.space)
        self.assertTrue(ok)
        return SD.replay(r, self.space, self.truth, copies)

    def test_a_win_through_a_rule_nested_in_the_copy(self):
        got = self.replay(win_record())
        self.assertTrue(got["log_ok"] and got["met_ok"])
        self.assertEqual(list(got["found"]), [2])
        s = got["found"][2]
        self.assertEqual((s["copy"], s["other"], s["side"], s["closes"], s["where"]),
                         ("R3", "R2", SD.WIN, SD.CONTAINMENT, SD.SOMEWHERE))
        self.assertEqual((s["nested_at_newborn"], s["original"], s["path"]),
                         (["R4"], SD.CONTRADICTS, ["R2", "R4", "R3"]))
        self.assertEqual(got["tried"]["copies"][SD.EDGE_CYCLE], 1)
        self.assertEqual(sum(got["tried"]["copies"].values()), 1)
        self.assertEqual((got["tried"]["others"][SD.EDGE_OK],
                          sum(got["tried"]["others"].values()), got["elsewhere"]), (2, 2, 0))
        self.assertTrue(RF.same_base(got["engine"], win_record(), self.space))

    def test_a_loss_through_its_own_win(self):
        got = self.replay(loss_record())
        self.assertTrue(got["log_ok"] and got["met_ok"])
        self.assertEqual(list(got["found"]), [3])
        s = got["found"][3]
        self.assertEqual((s["other"], s["side"], s["closes"], s["nested_at_newborn"]),
                         ("R2", SD.LOSS, SD.OWN, []))
        self.assertEqual((s["original"], s["path"]), (SD.REPEATS, ["R3", "R5", "R2"]))
        self.assertEqual({k: v for k, v in got["tried"]["copies"].items() if v},
                         {SD.EDGE_OK: 1, SD.EDGE_CYCLE: 1})
        self.assertEqual({k: v for k, v in got["tried"]["others"].items() if v}, {SD.EDGE_OK: 2})

    def test_gates_one_and_three_have_teeth(self):
        r = loss_record()
        flip(r, 0, "cierra_ciclo")
        got = self.replay(r)
        self.assertFalse(got["log_ok"])
        r = loss_record()
        flip(r, 2, "cierra_ciclo")              # the copy's installed win, logged refused
        got = self.replay(r)
        self.assertFalse(got["log_ok"] or got["met_ok"])

    def test_gate_four_has_teeth(self):
        got = self.replay(loss_record())
        eng = got["engine"]
        eng.decl_above["R5"].discard("R2")
        self.assertFalse(RF.same_base(eng, loss_record(), self.space))


class TestOneRun(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space = MI.space()
        cls.truth = {BILL: cls.space.extension([CO.TW.Condition(**c) for c in MOBILE])}

    def read(self, r, kept_run):
        copies, _ = CO.copies_of_run(r, self.space)
        return SD.read_run(r, self.space, self.truth, copies, kept_run)[0]

    def test_summed_with_the_rules_and_the_doors(self):
        gained = {"alone": {"most_gained": {"rule_id": "R3", "change": 5, "keyword": 0}}}
        got = self.read(win_record(), gained)
        a = got["refused"]["all"]
        self.assertEqual((a["sides"], a["copies"], a["side"], a["door"]),
                         (1, 1, {SD.WIN: 1, SD.LOSS: 0}, 1))
        self.assertEqual((a["closes"][SD.CONTAINMENT], a["where"][SD.SOMEWHERE],
                          a["original"][SD.CONTRADICTS]), (1, 1, 1))
        self.assertEqual(a["through"], {"another_queue": 1, "wrong_at_its_birth": 1,
                                        "the_rule_that_erred": 1, "a_copy": 0})
        self.assertEqual((got["refused"][SD.WIN]["sides"], got["refused"][SD.LOSS]["sides"]),
                         (1, 0))
        self.assertEqual([(x["rule_id"], x["queue"], x["sides"]) for x in got["at_the_copy"]],
                         [("R4", T1, 1)])
        self.assertEqual({(d["upper"], d["lower"], d["kind"], d["upper_born_at"],
                           d["lower_born_at"]) for d in got["doors"]},
                         {("R2", "R4", SD.RF.DECLARED, 3, 2), ("R4", "R3", SD.RF.NESTED, 2, 4)})
        row = got["rows"][0]
        self.assertNotIn("path_rules", row)
        self.assertEqual((row["path_rule_count"], row["erring"], row["erring_nested"]),
                         (1, "R4", True))
        most = got["costs_most"]
        self.assertEqual((most["rule_id"], most["change"]), ("R3", 5))
        self.assertEqual([(x["rule_id"], x["queue"], x["born_at"]) for x in most["sides"][0]["path"]],
                         [("R2", SS, 3), ("R4", T1, 2), ("R3", BILL, 4)])

    def test_no_copy_that_costs(self):
        for kept in ({}, {"alone": {"most_gained": None}},
                     {"alone": {"most_gained": {"rule_id": "R3", "change": 0, "keyword": 0}}}):
            self.assertIsNone(self.read(win_record(), kept)["costs_most"])


class TestGateTwoOnARecord(unittest.TestCase):

    def test_on_k_r3(self):
        rec = json.loads(plan.run_path(plan.RANKED, 3).read_text())
        kept = json.loads(SD.copies_path().read_text())["readings"]["runs"]["k_r3"]["rows"]
        copies, ok = CO.copies_of_run(rec, MI.space())
        self.assertTrue(SD.same_copies(copies, kept, ok))
        self.assertFalse(SD.same_copies(copies, kept, False))
        self.assertFalse(SD.same_copies(copies[:-1], kept, ok))
        moved = [dict(c, originals=c["originals"] + ["R9999"]) if i == 0 else c
                 for i, c in enumerate(copies)]
        self.assertFalse(SD.same_copies(moved, kept, ok))


def run(tc=10, rc=3, to=20, ro=4, sides=6, wins=4, losses=2, own=1, either=1, nowhere=4):
    def tried(n, k):
        return dict({v: 0 for v in SD.TRIED}, **{SD.EDGE_OK: n - k, SD.EDGE_CYCLE: k})
    return {"tried": {"copies": tried(tc, rc), "others": tried(to, ro)},
            "refused": {"all": {"sides": sides, "side": {SD.WIN: wins, SD.LOSS: sides - wins},
                                "where": {SD.NOWHERE: nowhere, SD.SOMEWHERE: sides - nowhere}},
                        SD.LOSS: {"sides": losses,
                                  "closes": {SD.OWN: own, SD.CONTAINMENT: losses - own - either,
                                             SD.EITHER: either}}}}


def fake(**kw):
    return {"runs": {t: run(**kw) for t in SD.RUNS}}


def holds(readings) -> dict[str, bool]:
    return {c["clause"]: c["holds"] for c in SD.read_expectation(readings)}


CLAUSES = ["N1", "N2", "N3", "N4"]


class TestTheExpectation(unittest.TestCase):

    def test_four_clauses(self):
        self.assertEqual(list(holds(fake())), CLAUSES)

    def test_inside_the_lines(self):
        self.assertEqual(holds(fake()), {c: True for c in CLAUSES})
        self.assertTrue(holds(fake(own=2, either=0))["N3"])

    def test_at_the_lines(self):
        got = holds(fake(tc=10, rc=2, to=20, ro=4, sides=6, wins=3, losses=2, own=1, either=0,
                         nowhere=3))
        self.assertEqual(got, {c: False for c in CLAUSES})

    def test_pooled_over_the_runs(self):
        r = fake()
        r["runs"]["k_r2"] = run(rc=0, wins=0, own=0, either=0, nowhere=0)
        self.assertEqual(holds(r), {c: True for c in CLAUSES})
        del r["runs"]["l_r1"]
        self.assertEqual(holds(r), {c: False for c in CLAUSES})

    def test_over_nothing(self):
        self.assertEqual(holds({}), {c: False for c in CLAUSES})
        got = holds(fake(tc=0, rc=0, sides=0, wins=0, losses=0, own=0, either=0, nowhere=0))
        self.assertEqual(got, {c: False for c in CLAUSES})
        r = fake()
        del r["runs"]["l_r3"]["refused"][SD.LOSS]
        r["runs"]["l_r3"]["tried"]["others"] = None
        self.assertEqual(holds(r), {"N1": False, "N2": True, "N3": False, "N4": True})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(SD, "read_inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                SD.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
