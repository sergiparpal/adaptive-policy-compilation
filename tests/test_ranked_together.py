"""
`ranked/together.py` — the POST-RUN reading of why billing's copies declared
sides the base could not hold together. No figure of the reading.

What is pinned is the instrument:
- the pairs of a birth on engines built by hand: a win and a loss whose lower
  rule reaches the upper one, and none where the win or the loss closes a cycle
  alone or the lower rule does not reach the upper; a rule cited on both sides
  counted apart; each pair once;
- the doors read off one shortest path, the same as every step tried;
- what carries a path, with the wrong steps or the wrong declared steps taken
  out; what the round shows, a listed rule's own `beats` and `loses_to` and
  never a containment; where the cycle is;
- one run read whole on a record built by hand over the real space: the copy's
  win and loss held apart by a declared step its lower rule's own answer
  installed, both sides right and the step wrong, the cycle somewhere, the step
  shown by the round and not shown without the list, and the named copy's round
  kept whole;
- gates 3 and 4 with teeth, and gate 4 on K r3's record against `sides.json`'s
  rows; gate 5 on fake records;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import copy
import json
import unittest
from unittest import mock

from edges import rebuild as erb
from manual import instrument as MI
from ranked import copies as CO
from ranked import plan
from ranked import refusals as RF
from ranked import together as TG
from tests.test_ranked_copies import BILL, MOBILE, SEV2, SS, T1, UNSIGNED
from tests.test_ranked_losses import mask
from tests.test_ranked_refusals import Engine, flip
from tests.test_ranked_sides import PRO, loss_record

OK, CYCLE = TG.EDGE_OK, TG.EDGE_CYCLE
RIGHT, WRONG, EVEN = TG.RIGHT, TG.WRONG, TG.CP.EVEN


def edge(key, winner, loser, verdict=OK, birth=9):
    return erb.Edge(key, birth, winner, loser, verdict)


class TestThePairs(unittest.TestCase):

    def engine(self, nested=(), declared=()):
        ext = {r: 0b1111 for r in ("N", "D", "U", "X", "M", "H")}
        return Engine(ext, nested=nested, declared=declared)

    def test_a_pair(self):
        eng = self.engine(declared=[("D", "X"), ("X", "U")])
        pairs, both = TG.pairs_at(eng, "N", [edge(0, "N", "D"), edge(1, "U", "N", CYCLE)])
        self.assertEqual([(w.loser, lo.winner) for w, lo in pairs], [("D", "U")])
        self.assertEqual(both, [])

    def test_none_where_the_lower_rule_does_not_reach_the_upper(self):
        eng = self.engine(declared=[("U", "X")])
        self.assertEqual(TG.pairs_at(eng, "N", [edge(0, "N", "D"), edge(1, "U", "N")]), ([], []))

    def test_none_where_the_win_closes_alone(self):
        # D reaches N through M, nested in N.
        eng = self.engine(nested=[("M", "N")], declared=[("D", "M"), ("D", "U")])
        self.assertEqual(TG.pairs_at(eng, "N", [edge(0, "N", "D"), edge(1, "U", "N")]), ([], []))

    def test_none_where_the_loss_closes_alone(self):
        # N reaches U through H, which holds N.
        eng = self.engine(nested=[("N", "H")], declared=[("H", "U"), ("D", "U")])
        self.assertEqual(TG.pairs_at(eng, "N", [edge(0, "N", "D"), edge(1, "U", "N")]), ([], []))

    def test_a_rule_cited_on_both_sides(self):
        pairs, both = TG.pairs_at(self.engine(), "N", [edge(0, "N", "D"), edge(1, "D", "N")])
        self.assertEqual(pairs, [])
        self.assertEqual([(w.key, lo.key) for w, lo in both], [(0, 1)])

    def test_each_pair_once_and_only_with_both_kinds(self):
        eng = self.engine(declared=[("D", "U")])
        edges = [edge(0, "N", "D"), edge(1, "U", "N"), edge(2, "U", "N")]
        self.assertEqual(len(TG.pairs_at(eng, "N", edges)[0]), 1)
        self.assertEqual(TG.pairs_at(eng, "N", edges[:1]), ([], []))
        self.assertEqual(TG.pairs_at(eng, "N", edges[1:]), ([], []))


class TestWhatHoldsThem(unittest.TestCase):

    def test_doors_off_one_path_are_every_steps(self):
        cases = [
            [("D", "X"), ("X", "U")],                              # both steps are doors
            [("D", "X"), ("X", "U"), ("D", "Y"), ("Y", "U")],      # none is
            [("D", "X"), ("X", "Y"), ("X", "Z"), ("Y", "U"), ("Z", "U")],   # D -> X alone
        ]
        for declared in cases:
            eng = Engine({r: 0b1 for r in "DXYZU"}, declared=declared)
            nodes = TG.CP.forward(eng, "D") & TG.CP.backward(eng, "U")
            every = {(d["upper"], d["lower"])
                     for d in RF.doors_of(eng, "U", "D", nodes, {}, 0, {r: SS for r in "DXYZU"})}
            self.assertEqual(set(TG.doors(eng, "D", "U", nodes)), every)
        self.assertEqual(TG.doors(Engine({"D": 1, "U": 1}), "D", "U", {"D", "U"}), [])

    def test_what_carries_a_path(self):
        # D -> X -> U, declared. On the points X and U share, U's queue is the
        # truth, so X above U is wrong; D above X is even.
        ext = {"D": 0b1111, "X": 0b0011, "U": 0b1111}
        eng = Engine(ext, declared=[("D", "X"), ("X", "U")])
        steps = TG.Steps(eng, {"D": T1, "X": T1, "U": SS}, {SS: 0b0011})
        nodes = TG.CP.forward(eng, "D") & TG.CP.backward(eng, "U")
        self.assertEqual((steps.verdict("X", "U"), steps.verdict("D", "X")), (WRONG, EVEN))
        self.assertFalse(TG.reaches_without(eng, "D", "U", nodes,
                                            lambda x, y: steps.verdict(x, y) != WRONG))
        self.assertTrue(TG.reaches_without(eng, "D", "U", nodes, lambda x, y: True))
        # A second path, D nested in Y and Y declared above U, with no wrong
        # step: X above U is still wrong, and no longer carries every path.
        ext = {"D": 0b1111, "X": 0b0011, "Y": 0b111111, "U": 0b111111}
        eng = Engine(ext, nested=[("D", "Y")], declared=[("D", "X"), ("X", "U"), ("Y", "U")])
        steps = TG.Steps(eng, {"D": BILL, "X": T1, "Y": BILL, "U": SS},
                         {SS: 0b0011, BILL: 0b111100})
        nodes = TG.CP.forward(eng, "D") & TG.CP.backward(eng, "U")
        self.assertEqual((steps.verdict("X", "U"), steps.verdict("Y", "U"),
                          steps.verdict("D", "Y")), (WRONG, RIGHT, EVEN))
        self.assertTrue(TG.reaches_without(eng, "D", "U", nodes,
                                           lambda x, y: steps.verdict(x, y) != WRONG))
        self.assertEqual(TG.doors(eng, "D", "U", nodes), [])

    def test_what_the_round_shows(self):
        eng = Engine({r: 0b1 for r in "ABC"}, nested=[("A", "C")], declared=[("A", "B")])
        shown = TG.shown_steps({"A": ["B"]}, {"B": []}, ["A"])
        self.assertTrue(shown(eng, "A", "B"))
        self.assertFalse(shown(eng, "A", "C"))                  # containment, never shown
        self.assertFalse(TG.shown_steps({"A": ["B"]}, {}, ["B"])(eng, "A", "B"))
        self.assertTrue(TG.shown_steps({}, {"B": ["A"]}, ["B"])(eng, "A", "B"))
        self.assertFalse(TG.shown_steps({}, {"B": ["A"]}, ["A"])(eng, "A", "B"))


def held_record(listed=True):
    """`loss_record`: R5's answer declared it above R2. R3, a copy of R1,
    declares itself above R5, installed, and below R2, refused: R5 already
    reached R2. The round listed R5 and R2."""
    r = loss_record()
    esc = r["escalations"][3]
    esc["listed"] = ["R5", "R2"] if listed else []
    esc["calls"].append({"payload": {"beats": ["R5"], "loses_to": ["R2"], "note": "above R5"},
                         "reasoning": "R2 first, then the copy, then R5."})
    return r


class TestOneRun(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space = MI.space()
        m, s = mask(cls.space, MOBILE), mask(cls.space, SEV2)
        cls.truth = {SS: m & s, BILL: m & ~s}

    def read(self, r, named=()):
        copies, _ = CO.copies_of_run(r, self.space)
        return TG.read_run(r, self.space, self.truth, copies, named)

    def test_read_whole(self):
        reading, got = self.read(held_record())
        c = reading["copies"]
        self.assertEqual((c["births_that_tried_a_side"], c["births_that_tried_a_win_and_a_loss"],
                          c["births_with_a_pair"], c["pairs"], c["losses"], c["wins"]),
                         (1, 1, 1, 1, 1, 1))
        self.assertEqual((c["both_right"], c["carried"], c["shown"], c["door"], c["across"]),
                         (1, {"wrong": 1, "wrong_declared": 1}, 1, 1, 0))
        self.assertEqual(c["where"], {TG.SOMEWHERE: 1, TG.NOWHERE: 0})
        self.assertEqual(reading["others"]["pairs"], 0)
        self.assertEqual(reading["by_queues"], [{"lower_queue": T1, "upper_queue": SS, "pairs": 1}])
        (row,) = reading["rows"]
        self.assertEqual((row["newborn"], row["lower"], row["upper"], row["birth"],
                          row["win_verdict"], row["loss_verdict"], row["door_count"]),
                         ("R3", "R5", "R2", 4, RIGHT, RIGHT, 1))
        (door,) = reading["doors"]
        self.assertEqual((door["upper"], door["lower"], door["kind"], door["verdict"],
                          door["installed_at"], door["installed_by"], door["by_a_copy"],
                          door["pairs"]),
                         ("R5", "R2", TG.DECLARED, WRONG, 3, "R5", False, 1))
        self.assertTrue(got["log_ok"] and got["order_ok"])

    def test_not_shown_without_the_list(self):
        reading, _ = self.read(held_record(listed=False))
        self.assertEqual((reading["copies"]["pairs"], reading["copies"]["shown"]), (1, 0))

    def test_the_named_copy(self):
        reading, _ = self.read(held_record(), named=("R3",))
        n = reading["named"]["R3"]
        self.assertEqual((n["rule_id"], n["born_at"], n["kind"]), ("R3", 4, "ERROR"))
        rnd = n["round"]
        self.assertEqual((rnd["listed"], rnd["beats"], rnd["loses_to"], rnd["note"],
                          rnd["reasoning"]),
                         (["R5", "R2"], ["R5"], ["R2"], "above R5",
                          "R2 first, then the copy, then R5."))
        self.assertEqual(len(rnd["shown_as"]), 2)
        self.assertTrue(rnd["shown_as"][0].startswith("R5: SI ") and "[gana a R2]" in rnd["shown_as"][0])
        (pair,) = n["pairs"]
        self.assertEqual([p["rule_id"] for p in pair["path"]], ["R5", "R2"])
        self.assertEqual(pair["path"][0]["step_to_next"],
                         {"kind": TG.DECLARED, "verdict": WRONG, "installed_at": 3,
                          "installed_by": "R5"})
        self.assertNotIn("step_to_next", pair["path"][1])

    def test_gate_three_has_teeth(self):
        r = held_record()
        flip(r, 2, CYCLE)                    # the win, logged as refused
        _, got = self.read(r)
        self.assertFalse(got["order_ok"])
        self.assertFalse(got["log_ok"])

    def test_gate_four_has_teeth(self):
        _, got = self.read(held_record())
        rows = [{"key": 3, "side": TG.LOSS, "closes": TG.OWN},
                {"key": 2, "side": TG.WIN, "closes": TG.OWN}]
        self.assertTrue(TG.same_losses(got, rows))
        self.assertFalse(TG.same_losses(got, rows + [{"key": 7, "side": TG.LOSS,
                                                     "closes": TG.OWN}]))
        self.assertFalse(TG.same_losses(got, [dict(rows[0], closes=RF.EITHER)]))


class TestGateFourOnARecord(unittest.TestCase):
    """On K r3's record: gate 4 passes against `sides.json`'s rows, and fails with
    one of them taken out. Nothing of the reading is printed or pinned."""

    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(plan.run_path(plan.RANKED, 3).read_text())
        cls.rows = json.loads(TG.sides_path().read_text())["readings"]["runs"]["k_r3"]["rows"]
        space = MI.space()
        copies, _ = CO.copies_of_run(cls.record, space)
        cls.got = TG.replay(cls.record, space, MI.space_truth(), copies)

    def test_it_passes_and_has_teeth(self):
        self.assertTrue(self.got["log_ok"] and self.got["order_ok"])
        self.assertTrue(TG.same_losses(self.got, self.rows))
        losses = [r for r in self.rows if r["side"] == TG.LOSS and r["closes"] == TG.OWN]
        if losses:
            short = [r for r in self.rows if r is not losses[0]]
            self.assertFalse(TG.same_losses(self.got, short))


class TestGateFive(unittest.TestCase):

    def lost(self, newborns):
        return {"lost": {"top": [{"newborn": n} for n in newborns]}}

    def test_the_two_copies(self):
        copies = [{"rule_id": r} for r in TG.NAMED]
        a, b = TG.NAMED
        self.assertTrue(TG.named_are_lost(self.lost([a, b, a, b, "R9"]), copies))
        self.assertFalse(TG.named_are_lost(self.lost([a, b, a, "R9"]), copies))
        self.assertFalse(TG.named_are_lost(self.lost([a, b, a]), copies))
        self.assertFalse(TG.named_are_lost(self.lost([a, b, a, b]), copies[:1]))
        self.assertFalse(TG.named_are_lost(None, copies))


def run(pairs=10, both=6, carried=6, nowhere=6, shown=0):
    return {"copies": {"pairs": pairs, "both_right": both, "carried": {"wrong": carried},
                       "where": {TG.NOWHERE: nowhere}, "shown": shown}}


def good():
    return {"win_verdict": RIGHT, "loss_verdict": RIGHT, "carried_wrong": True}


def fake(named=None, **kw):
    runs = {t: run(**kw) for t in TG.RUNS}
    runs[TG.NAMED_RUN]["named"] = (named if named is not None else
                                   {r: {"pairs": [good()]} for r in TG.NAMED})
    return {"runs": runs}


def holds(readings) -> dict[str, bool]:
    return {c["clause"]: c["holds"] for c in TG.read_expectation(readings)}


CLAUSES = ["Q1", "Q2", "Q3", "Q4", "Q5"]


class TestTheExpectation(unittest.TestCase):

    def test_five_clauses(self):
        self.assertEqual(list(holds(fake())), CLAUSES)

    def test_inside_the_lines(self):
        self.assertEqual(holds(fake()), {c: True for c in CLAUSES})

    def test_at_the_lines(self):
        a, b = TG.NAMED
        named = {a: {"pairs": [good()]}, b: {"pairs": [dict(good(), carried_wrong=False)]}}
        got = holds(fake(named=named, pairs=10, both=5, carried=5, nowhere=5, shown=6))
        self.assertEqual(got, {c: False for c in CLAUSES})
        # A tenth shown is not fewer than a tenth: 6 runs of 1 of 10 is 6 of 60.
        self.assertFalse(holds(fake(shown=1))["Q4"])
        self.assertTrue(holds(fake(shown=0))["Q4"])

    def test_q5_reads_every_pair_of_both(self):
        a, b = TG.NAMED
        self.assertFalse(holds(fake(named={a: {"pairs": [good()]}, b: {"pairs": []}}))["Q5"])
        self.assertFalse(holds(fake(named={a: {"pairs": [good()]}}))["Q5"])
        wrong = {a: {"pairs": [good(), dict(good(), loss_verdict=EVEN)]}, b: {"pairs": [good()]}}
        self.assertFalse(holds(fake(named=wrong))["Q5"])

    def test_over_nothing(self):
        self.assertEqual(holds({}), {c: False for c in CLAUSES})
        got = holds(fake(named={}, pairs=0, both=0, carried=0, nowhere=0, shown=0))
        self.assertEqual(got, {c: False for c in CLAUSES})
        r = fake()
        del r["runs"]["k_r3"]
        self.assertEqual(holds(r), {"Q1": False, "Q2": False, "Q3": False, "Q4": False,
                                    "Q5": True})
        r = copy.deepcopy(fake())
        r["runs"]["l_r1"]["copies"]["carried"]["wrong"] = None
        self.assertFalse(holds(r)["Q2"])
        r = copy.deepcopy(fake())
        r["runs"]["l_r1"]["copies"]["shown"] = True
        self.assertFalse(holds(r)["Q4"])


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(TG, "read_inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                TG.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
