"""
`ranked/lost.py` — the POST-RUN reading of why L r2 lost under the copies'
losses first. No figure of the reading.

What is pinned is the instrument:
- the changed edges between two replays, missing or added, with their kind;
- where an edge reaches: a missing edge frees its lower rule where its upper
  matches, an added edge defeats it, and only where the lower rule's queue is
  not the point's truth, on masks built by hand;
- the points by kind, any and alone, and the points no edge reaches;
- one run read whole on a record built by hand over the real space. The
  copy's win, refused by the replay, frees a rule of another queue at the
  points the replay loses, and its kept loss defeats a rule at the points it
  gains. Each edge is read with its verdict, and the win is closed by the
  copy's own loss;
- gates 2 to 4 with teeth, in both arms;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from unittest import mock

from manual import instrument as MI
from ranked import copies as CO
from ranked import lost as LT
from ranked import plan
from tests.test_ranked_copies import BILL, MOBILE, SEV2, SS, T1, UNSIGNED
from tests.test_ranked_losses import mask
from tests.test_ranked_sides import PRO, loss_record

OK, CYCLE = LT.EDGE_OK, LT.EDGE_CYCLE


class TestTheChangedEdges(unittest.TestCase):

    def test_missing_and_added(self):
        r = loss_record()
        rec = {"verdict": {0: OK, 1: OK, 2: OK, 3: CYCLE}}
        got = {"verdict": {0: OK, 1: OK, 2: CYCLE, 3: OK}}
        c = LT.changed_edges(r, {"R3"}, rec, got)
        self.assertEqual(sorted(c), [2, 3])
        self.assertEqual((c[2]["winner"], c[2]["loser"], c[2]["kind"], c[2]["change"], c[2]["birth"]),
                         ("R3", "R5", LT.CW, LT.MISSING, 4))
        self.assertEqual((c[3]["kind"], c[3]["change"], c[3]["side"]), (LT.CL, LT.ADDED, LT.LOSS))
        other = LT.changed_edges(r, set(), rec, got)
        self.assertEqual({k: v["kind"] for k, v in other.items()}, {2: LT.OE, 3: LT.OE})


class TestWhereAnEdgeReaches(unittest.TestCase):

    def test_freeing_only_a_wrong_rule(self):
        ext = {"Z": 0b0111, "Y": 0b1110}
        before, after = {"Y": 0b1000}, {"Y": 0b1110}      # Y freed on 0b0110
        truth = {SS: 0b0100}
        action = {"Z": BILL, "Y": SS}
        edges = [{"key": 7, "winner": "Z", "loser": "Y"}]
        self.assertEqual(LT.freeing(0b1111, before, after, ext, action, truth, edges),
                         {7: 0b0010})                     # 0b0100 is Y's own queue's point
        self.assertEqual(LT.freeing(0b1111, before, after, ext, action, truth, edges, wrong=False),
                         {7: 0b0110})
        self.assertEqual(LT.freeing(0b0001, before, after, ext, action, truth, edges), {})

    def test_by_kind(self):
        changed = {1: {"kind": LT.CW}, 2: {"kind": LT.CL}, 3: {"kind": LT.CW}}
        got = LT.by_kind(0b11111, {1: 0b00011, 2: 0b00110, 3: 0b01000}, changed,
                         {BILL: 0b01111, SS: 0b10000})
        self.assertEqual((got["points"], got["unreached"]), (5, 1))
        self.assertEqual(got["any"], {LT.CW: 3, LT.CL: 2, LT.OE: 0})
        self.assertEqual(got["alone"], {LT.CW: 2, LT.CL: 1, LT.OE: 0})
        self.assertEqual(got["any_by_queue"][LT.CW], {BILL: 3})


class TestOneRun(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space = MI.space()
        m, s, p = (mask(cls.space, c) for c in (MOBILE, SEV2, PRO))
        cls.won, cls.lost = m & s & ~p, m & ~s & p
        cls.truth = {SS: m & s, BILL: m & ~s}

    def read(self, r):
        copies, _ = CO.copies_of_run(r, self.space)
        return LT.read_run(r, self.space, self.truth, copies)

    def test_read_whole(self):
        reading, got = self.read(loss_record())
        n, k = self.won.bit_count(), self.lost.bit_count()
        self.assertEqual(reading["changed"], {LT.MISSING: {LT.CW: 1, LT.CL: 0, LT.OE: 0},
                                              LT.ADDED: {LT.CW: 0, LT.CL: 1, LT.OE: 0}})
        lost, gained = reading["lost"], reading["gained"]
        self.assertEqual((lost["points"], lost["any"][LT.CW], lost["alone"][LT.CW],
                          lost["unreached"]), (k, k, k, 0))
        self.assertEqual(lost["any_by_queue"][LT.CW], {BILL: k})
        self.assertEqual((gained["points"], gained["any"][LT.CL], gained["unreached"]), (n, n, 0))
        self.assertEqual(lost["by_kind"][LT.CW]["edges"], 1)
        self.assertEqual(lost["by_kind"][LT.CW][LT.CP.RIGHT_VERDICT], 1)
        top = lost["top"][0]
        self.assertEqual((top["winner"], top["loser"], top["queues"], top["points"],
                          top["newborn_queue"]), ("R3", "R5", [BILL, T1], k, BILL))
        self.assertEqual(lost["closes"], {LT.OWN: 1, LT.CONTAINMENT: 0, LT.EITHER: 0})
        self.assertTrue(got["reached"])
        self.assertTrue(LT.the_graphs_difference(got["changed"], got["rec"]["engine"],
                                                 got["got"]["engine"]))

    def test_in_k(self):
        r = loss_record()
        r["arm"] = plan.RANKED
        self.assertTrue(self.read(r)[1]["reached"])

    def test_gate_four_has_teeth(self):
        _, got = self.read(loss_record())
        rec_eng, got_eng = got["rec"]["engine"], got["got"]["engine"]
        changed = {k: dict(v) for k, v in got["changed"].items()}
        changed[2]["change"] = None
        self.assertFalse(LT.the_graphs_difference(changed, rec_eng, got_eng))
        self.assertFalse(LT.the_graphs_difference({3: got["changed"][3]}, rec_eng, got_eng))

    def test_gate_two_has_teeth(self):
        reading, _ = self.read(loss_record())
        kept = {"copies": {LT.WIN: {"refused_now": 1, "installed_now": 0},
                           LT.LOSS: {"refused_now": 0, "installed_now": 1}}}
        self.assertTrue(LT.as_kept(reading["changed"], kept))
        kept["copies"][LT.WIN]["refused_now"] = 2
        self.assertFalse(LT.as_kept(reading["changed"], kept))

    def test_gate_three_in_k_has_teeth(self):
        ext = {"Z": 0b0011, "Y": 0b0011}
        missing = [{"winner": "Z", "loser": "Y"}]
        self.assertTrue(LT.reached_all(0b0001, {"Y": 0}, {"Y": 0b0011}, ext, missing, []))
        self.assertFalse(LT.reached_all(0b0100, {"Y": 0}, {"Y": 0b0011}, ext, missing, []))


def run(lost=10, through=6, edges=4, right=3, own=2, either=1, contained=1):
    return {"lost": {"points": lost, "any": {LT.CW: through},
                     "by_kind": {LT.CW: {"edges": edges, "right": right}},
                     "closes": {LT.OWN: own, LT.CONTAINMENT: contained, LT.EITHER: either}}}


def fake(l1=2, l3=3, **kw):
    runs = {"l_r2": run(**kw), "l_r1": run(through=l1), "l_r3": run(through=l3)}
    return {"runs": runs}


def holds(readings) -> dict[str, bool]:
    return {c["clause"]: c["holds"] for c in LT.read_expectation(readings)}


CLAUSES = ["P1", "P2", "P3", "P4"]


class TestTheExpectation(unittest.TestCase):

    def test_four_clauses(self):
        self.assertEqual(list(holds(fake())), CLAUSES)

    def test_inside_the_lines(self):
        self.assertEqual(holds(fake()), {c: True for c in CLAUSES})

    def test_at_the_lines(self):
        got = holds(fake(l1=3, l3=2, lost=10, through=5, edges=4, right=2, own=1, either=1,
                         contained=2))
        self.assertEqual(got, {c: False for c in CLAUSES})

    def test_over_nothing(self):
        self.assertEqual(holds({}), {c: False for c in CLAUSES})
        got = holds(fake(lost=0, through=0, edges=0, right=0, own=0, either=0, contained=0))
        self.assertEqual(got, {c: False for c in CLAUSES})
        r = fake()
        del r["runs"]["l_r1"]
        self.assertEqual(holds(r), {"P1": True, "P2": True, "P3": True, "P4": False})
        r = fake()
        r["runs"]["l_r2"]["lost"]["closes"][LT.EITHER] = None
        self.assertFalse(holds(r)["P3"])


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(LT, "read_inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                LT.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
