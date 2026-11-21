"""
`ranked/losses.py` — the POST-RUN reading of whether a copy's losses, installed
before its wins, would have been kept. No figure of the reading.

What is pinned is the instrument:
- the order a replay tries a birth's edges in: the log's, or its rule's losses
  before its wins, each kind in the log's order, for a copy or for every birth;
- the replays on a record built by hand over the real space. In the record's
  order a copy's loss is refused through its own win, and the two rules stand
  side by side, a conflict. With the copy's losses first, the loss is
  installed, the win refused, and the conflict's points decided right;
- gates 1 and 4 with teeth, on both engines' arms;
- the sides by birth and side, and what a replay changes of them, for the
  copies and for the other births;
- one run read whole: the three replays' bases beside the record's, the points
  gained and lost by true queue, and the copy that costs most;
- gate 3 against `sides.json`'s rows, by hand and on K r3's record, with
  teeth;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import json
import unittest
from unittest import mock

from edges import rebuild as erb
from manual import instrument as MI
from ranked import copies as CO
from ranked import losses as LO
from ranked import plan
from ranked import readings as RD
from tests.test_ranked_copies import BILL, MOBILE, SEV2, SS, UNSIGNED
from tests.test_ranked_refusals import flip
from tests.test_ranked_sides import PRO, loss_record

OK, CYCLE = LO.EDGE_OK, LO.EDGE_CYCLE


def mask(space, conditions):
    return space.extension([CO.TW.Condition(**c) for c in conditions])


class TestTheOrder(unittest.TestCase):

    EDGES = [erb.Edge(0, 4, "R3", "R5", OK), erb.Edge(1, 4, "R2", "R3", CYCLE),
             erb.Edge(2, 4, "R3", "R6", OK), erb.Edge(3, 4, "R7", "R3", OK)]

    def keys(self, first):
        return [e.key for e in LO.ordered(self.EDGES, "R3", first)]

    def test_the_logs(self):
        for first in (None, set(), {"R9"}):
            self.assertEqual(self.keys(first), [0, 1, 2, 3])

    def test_losses_first(self):
        self.assertEqual(self.keys({"R3"}), [1, 3, 0, 2])
        self.assertEqual(self.keys(LO.EVERY), [1, 3, 0, 2])


class TestTheReplays(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space = MI.space()
        m, s, p = (mask(cls.space, c) for c in (MOBILE, SEV2, PRO))
        cls.won = m & s & ~p                    # R2 alone, once R2 stands above R3
        cls.truth = {SS: m & s}

    def replay(self, r, first):
        return LO.replay(r, self.space, self.truth, first)

    def test_the_record(self):
        r = loss_record()
        got = self.replay(r, None)
        self.assertEqual(got["verdict"], {0: OK, 1: OK, 2: OK, 3: CYCLE})
        self.assertEqual(got["right"], 0)       # R2 and R3 side by side: a conflict
        self.assertTrue(LO.is_the_record(r, got, RD.base_of(r, self.space, self.truth)))
        self.assertTrue(LO.only_the_order(r, got))

    def test_the_copys_losses_first(self):
        r = loss_record()
        got = self.replay(r, {"R3"})
        self.assertEqual(got["verdict"], {0: OK, 1: OK, 2: CYCLE, 3: OK})
        self.assertEqual(got["right"], self.won)
        self.assertTrue(LO.only_the_order(r, got))
        self.assertEqual(self.replay(r, LO.EVERY)["verdict"], got["verdict"])
        self.assertEqual(self.replay(r, set())["verdict"], self.replay(r, None)["verdict"])

    def test_in_k(self):
        r = loss_record()
        r["arm"] = plan.RANKED
        got = self.replay(r, None)
        self.assertTrue(LO.is_the_record(r, got, RD.base_of(r, self.space, self.truth)))

    def test_gates_one_and_four_have_teeth(self):
        r = loss_record()
        base = RD.base_of(r, self.space, self.truth)
        got = self.replay(r, {"R3"})
        self.assertFalse(LO.is_the_record(r, got, base))      # another order, other verdicts
        flip(r, 0, CYCLE)
        self.assertFalse(LO.is_the_record(r, self.replay(r, None), base))
        r = loss_record()
        got = self.replay(r, None)
        self.assertFalse(LO.is_the_record(r, got, {"right": self.won}))
        self.assertFalse(LO.only_the_order(r, dict(got, tries=got["tries"] + 1)))
        moved = dict(got["tried_at"])
        moved[0] = 4                            # the log tried it at birth 2
        self.assertFalse(LO.only_the_order(r, dict(got, tried_at=moved)))


class TestTheSides(unittest.TestCase):

    def test_by_birth_and_side(self):
        got = LO.sides_of(loss_record(), {"R3"})
        self.assertEqual([(s["key"], s["birth"], s["rule_id"], s["copy"], s["side"], s["logged"])
                          for s in got],
                         [(0, 2, "R2", False, LO.WIN, OK), (1, 3, "R5", False, LO.WIN, OK),
                          (2, 4, "R3", True, LO.WIN, OK), (3, 4, "R3", True, LO.LOSS, CYCLE)])

    def test_what_a_replay_changes(self):
        sides = LO.sides_of(loss_record(), {"R3"})
        before = {0: OK, 1: OK, 2: OK, 3: CYCLE}
        after = {0: OK, 1: OK, 2: CYCLE, 3: OK}
        self.assertEqual(LO.changed(sides, before, after, True), {
            LO.WIN: {"tried": 1, "refused_in_the_record": 0, "installed_now": 0,
                     "installed_in_the_record": 1, "refused_now": 1},
            LO.LOSS: {"tried": 1, "refused_in_the_record": 1, "installed_now": 1,
                      "installed_in_the_record": 0, "refused_now": 0}})
        self.assertEqual(LO.changed(sides, before, after, False), {
            LO.WIN: {"tried": 2, "refused_in_the_record": 0, "installed_now": 0,
                     "installed_in_the_record": 2, "refused_now": 0},
            LO.LOSS: {"tried": 0, "refused_in_the_record": 0, "installed_now": 0,
                      "installed_in_the_record": 0, "refused_now": 0}})


class TestOneRun(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space = MI.space()
        m, s, p = (mask(cls.space, c) for c in (MOBILE, SEV2, PRO))
        cls.won = m & s & ~p                    # the kept loss: R2 alone above R3
        cls.lost = m & ~s & p                   # the refused win: R5 beside R1 and R3
        cls.truth = {SS: m & s, BILL: m & ~s}
        cls.keyword = cls.space.mask["has_security_keyword"][True]

    def read(self, kept_run):
        r = loss_record()
        copies, _ = CO.copies_of_run(r, self.space)
        return LO.read_run(r, self.space, self.truth, copies, self.keyword, kept_run)[0]

    def test_read_whole(self):
        gained = {"alone": {"most_gained": {"rule_id": "R3", "change": 5}}}
        got = self.read(gained)
        n, k = self.won.bit_count(), self.lost.bit_count()
        rec, cf, ef = got[LO.RECORD], got[LO.COPIES_FIRST], got[LO.EVERY_FIRST]
        self.assertEqual(got["copies"], 1)
        self.assertEqual(sum(rec["halves"]), rec["right"])
        self.assertEqual((cf["change"], cf["gained"], cf["lost"], cf["gained_by_queue"],
                          cf["lost_by_queue"]), (n - k, n, k, {SS: n}, {BILL: k}))
        self.assertEqual(cf["right"], rec["right"] + n - k)
        self.assertEqual(sum(cf["halves"]), cf["right"])
        self.assertEqual((cf["copies"][LO.LOSS]["installed_now"],
                          cf["copies"][LO.WIN]["refused_now"]), (1, 1))
        self.assertEqual((ef["change"], ef["copies"]), (cf["change"], cf["copies"]))
        self.assertEqual(got["costs_most"], {
            "rule_id": "R3", "change": 5,
            "refused_losses": [{"above": "R2", "below": "R3", "side": LO.LOSS,
                                "record": CYCLE, "copies_first": OK}],
            "wins_refused_now": [{"above": "R3", "below": "R5", "side": LO.WIN,
                                  "record": OK, "copies_first": CYCLE}]})

    def test_no_copy_that_costs(self):
        for kept in ({}, {"alone": {"most_gained": None}},
                     {"alone": {"most_gained": {"rule_id": "R3", "change": 0}}}):
            self.assertIsNone(self.read(kept)["costs_most"])


class TestGateThree(unittest.TestCase):

    def test_by_hand(self):
        sides = LO.sides_of(loss_record(), {"R3"})
        self.assertTrue(LO.same_refused_losses(sides, [{"key": 3, "side": "loss"},
                                                       {"key": 9, "side": "win"}]))
        self.assertFalse(LO.same_refused_losses(sides, []))
        self.assertFalse(LO.same_refused_losses(sides, [{"key": 2, "side": "loss"}]))

    def test_on_k_r3(self):
        rec = json.loads(plan.run_path(plan.RANKED, 3).read_text())
        rows = json.loads(LO.sides_path().read_text())["readings"]["runs"]["k_r3"]["rows"]
        copies, _ = CO.copies_of_run(rec, MI.space())
        sides = LO.sides_of(rec, {c["rule_id"] for c in copies})
        self.assertTrue(LO.same_refused_losses(sides, rows))
        dropped = next(i for i, r in enumerate(rows) if r["side"] == "loss")
        self.assertFalse(LO.same_refused_losses(sides, rows[:dropped] + rows[dropped + 1:]))


def run(refused=10, kept=6, wins=3, change=5, right=100, every=110):
    return {LO.COPIES_FIRST: {"right": right, "change": change,
                              "copies": {LO.LOSS: {"refused_in_the_record": refused,
                                                   "installed_now": kept},
                                         LO.WIN: {"refused_now": wins}}},
            LO.EVERY_FIRST: {"right": every}}


def fake(**kw):
    return {"runs": {t: run(**kw) for t in LO.RUNS}}


def holds(readings) -> dict[str, bool]:
    return {c["clause"]: c["holds"] for c in LO.read_expectation(readings)}


CLAUSES = ["O1", "O2", "O3", "O4"]


class TestTheExpectation(unittest.TestCase):

    def test_four_clauses(self):
        self.assertEqual(list(holds(fake())), CLAUSES)

    def test_inside_the_lines(self):
        self.assertEqual(holds(fake()), {c: True for c in CLAUSES})

    def test_at_the_lines(self):
        got = holds(fake(refused=10, kept=5, wins=5, change=0, right=100, every=100))
        self.assertEqual(got, {c: False for c in CLAUSES})

    def test_only_l_reads_o3(self):
        r = fake()
        for t in LO.K_RUNS:
            r["runs"][t][LO.COPIES_FIRST]["change"] = -50
        self.assertEqual(holds(r), {c: True for c in CLAUSES})
        r["runs"]["l_r3"][LO.COPIES_FIRST]["change"] = -1
        self.assertEqual(holds(r), {"O1": True, "O2": True, "O3": False, "O4": True})

    def test_over_nothing(self):
        self.assertEqual(holds({}), {c: False for c in CLAUSES})
        got = holds(fake(refused=0, kept=0, wins=0))
        self.assertEqual(got, {"O1": False, "O2": False, "O3": True, "O4": True})
        r = fake()
        del r["runs"]["l_r1"]
        self.assertEqual(holds(r), {c: False for c in CLAUSES})
        r = fake()
        del r["runs"]["k_r2"][LO.EVERY_FIRST]
        r["runs"]["l_r2"][LO.COPIES_FIRST]["change"] = None
        self.assertEqual(holds(r), {"O1": True, "O2": True, "O3": False, "O4": False})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(LO, "read_inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                LO.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
