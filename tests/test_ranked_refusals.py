"""
`ranked/refusals.py` — the POST-RUN reading of why the refusals fell where they
did. No figure of the reading.

What is pinned is the instrument:
- the refusals read off `conflicts.json`'s rows, one for each refused edge at
  each case;
- a step's kind, and what closes a cycle at the newborn: its own answer,
  containment, or either, on engines built by hand;
- the doors, the steps every path passes through, with the birth of a declared
  one;
- a refused edge read whole: its side, where its cycle is, its shortest path
  and the policy's verdict;
- one run's refusals summed, by group, and apart where the cycle is nowhere;
- the gates with teeth, on K r3's record: they pass on it, and a moved verdict
  or a target the log never refused fails them;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import json
import unittest
from unittest import mock

from manual import instrument as MI
from ranked import plan
from ranked import refusals as RF

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SS, T2, BILL = "SELF_SERVICE_DEFLECT", "T2_TECHNICAL", "BILLING_SPECIALIST"


class Engine:
    """What the reading asks of rung 2's engine, built by hand: `x` beats `y`
    by containment when `y` is in `sub_above[x]`, by declaration when in
    `decl_above[x]`."""

    def __init__(self, ext, nested=(), declared=()):
        self.ext = dict(ext)
        self.sub_above = {r: set() for r in ext}
        self.sub_below = {r: set() for r in ext}
        self.decl_above = {r: set() for r in ext}
        self.decl_below = {r: set() for r in ext}
        for x, y in nested:
            self.sub_above[x].add(y)
            self.sub_below[y].add(x)
        for x, y in declared:
            self.decl_above[x].add(y)
            self.decl_below[y].add(x)

    def wins_over(self, rid):
        return self.sub_above[rid] | self.decl_above[rid]

    def beats_me(self, rid):
        return self.sub_below[rid] | self.decl_below[rid]


class TestTheRefusals(unittest.TestCase):

    def test_one_for_each_edge_at_each_case(self):
        rows = [{"case": 4, "group": "billing", "right": False,
                 "refused": [{"above": "A", "below": "B", "verdict": "cierra_ciclo"},
                             {"above": "C", "below": "B", "verdict": "cierra_ciclo"}]},
                {"case": 9, "group": "rest", "right": True,
                 "refused": [{"above": "A", "below": "B", "verdict": "cierra_ciclo"}]}]
        got = RF.refusals_of(rows)
        self.assertEqual([(u["case"], u["above"], u["below"]) for u in got],
                         [(4, "A", "B"), (4, "C", "B"), (9, "A", "B")])
        self.assertEqual(got[0]["group"], "billing")
        self.assertFalse(got[0]["right"])


class TestWhatClosesTheCycle(unittest.TestCase):

    def test_a_win_closed_by_a_rule_nested_in_the_newborn(self):
        # W is the newborn and declared itself above L; L beats X, X is nested in W.
        eng = Engine({"W": 0b1111, "L": 0b0110, "X": 0b0011},
                     nested=[("X", "W")], declared=[("L", "X")])
        nodes = RF.CP.forward(eng, "L") & RF.CP.backward(eng, "W")
        self.assertEqual(nodes, {"L", "X", "W"})
        self.assertEqual(RF.closes(eng, "W", "L", "W", set(), nodes), RF.CONTAINMENT)
        self.assertEqual(RF.step_kind(eng, "X", "W"), RF.NESTED)
        self.assertEqual(RF.step_kind(eng, "L", "X"), RF.DECLARED)

    def test_a_loss_closed_by_the_newborns_own_win(self):
        # L is the newborn; its own win over Y, installed at its birth, reaches W.
        eng = Engine({"W": 0b0111, "L": 0b0110, "Y": 0b1110},
                     declared=[("L", "Y"), ("Y", "W")])
        nodes = RF.CP.forward(eng, "L") & RF.CP.backward(eng, "W")
        self.assertEqual(RF.closes(eng, "W", "L", "L", {("L", "Y")}, nodes), RF.OWN)

    def test_either(self):
        eng = Engine({"W": 0b0111, "L": 0b0110, "Y": 0b1110, "Z": 0b1111},
                     nested=[("L", "Z")], declared=[("L", "Y"), ("Y", "W"), ("Z", "W")])
        nodes = RF.CP.forward(eng, "L") & RF.CP.backward(eng, "W")
        self.assertEqual(RF.closes(eng, "W", "L", "L", {("L", "Y")}, nodes), RF.EITHER)
        self.assertIsNone(RF.closes(eng, "W", "L", "Q", set(), nodes))   # no newborn at an end


class TestTheDoors(unittest.TestCase):

    def test_steps_every_path_passes(self):
        # Two paths L -> A -> X -> W and L -> B -> X -> W: X -> W is the one door.
        eng = Engine({"W": 0b11111, "L": 0b00110, "A": 0b00011, "B": 0b00101,
                      "X": 0b00001},
                     nested=[("X", "W")], declared=[("L", "A"), ("L", "B"), ("A", "X"),
                                                    ("B", "X")])
        nodes = RF.CP.forward(eng, "L") & RF.CP.backward(eng, "W")
        action = {r: SS for r in eng.ext}
        got = RF.doors_of(eng, "W", "L", nodes, {("A", "X"): 7}, 9, action)
        self.assertEqual([(d["upper"], d["lower"], d["kind"]) for d in got],
                         [("X", "W", RF.NESTED)])
        eng2 = Engine(eng.ext, nested=[("X", "W")], declared=[("L", "A"), ("A", "X")])
        nodes2 = RF.CP.forward(eng2, "L") & RF.CP.backward(eng2, "W")
        got2 = {(d["upper"], d["lower"]): d for d in
                RF.doors_of(eng2, "W", "L", nodes2, {("A", "X"): 7, ("L", "A"): 9}, 9, action)}
        self.assertEqual(set(got2), {("L", "A"), ("A", "X"), ("X", "W")})
        self.assertEqual((got2[("A", "X")]["installed_at"], got2[("A", "X")]["at_this_birth"]),
                         (7, False))
        self.assertTrue(got2[("L", "A")]["at_this_birth"])
        self.assertIsNone(got2[("X", "W")]["installed_at"])


class TestOneRefusedEdge(unittest.TestCase):

    def test_somewhere_and_nowhere(self):
        # W and L share point 1 and point 2. The path L -> X -> W runs through X.
        truth = {SS: 0b0010, T2: 0b0101}
        action = {"W": SS, "L": T2, "X": SS}
        near = Engine({"W": 0b0111, "L": 0b0110, "X": 0b0010},
                      nested=[("X", "W")], declared=[("L", "X")])
        got = RF.analyse(near, "W", "L", "W", 5, set(), {}, action, truth)
        self.assertEqual((got["side"], got["closes"], got["where"], got["shortest"]),
                         (RF.WIN, RF.CONTAINMENT, RF.SOMEWHERE, 2))
        self.assertEqual(got["path_rules"], ["X"])
        self.assertEqual(got["verdict"], RF.CP.EVEN)          # one shared point each
        far = Engine({"W": 0b1111, "L": 0b0110, "X": 0b1000},
                     nested=[("X", "W")], declared=[("L", "X")])
        self.assertEqual(RF.analyse(far, "W", "L", "W", 5, set(), {}, action, truth)["where"],
                         RF.NOWHERE)

    def test_no_path(self):
        eng = Engine({"W": 0b011, "L": 0b110})
        got = RF.analyse(eng, "W", "L", "W", 5, set(), {}, {"W": SS, "L": T2},
                         {SS: 0b010, T2: 0b100})
        self.assertFalse(got["reaches"])
        self.assertIsNone(got["closes"])
        self.assertEqual(got["doors"], [])


class TestOneRun(unittest.TestCase):

    def test_summed(self):
        found = {("W", "L"): {"side": RF.WIN, "closes": RF.CONTAINMENT, "where": RF.NOWHERE,
                              "verdict": RF.CP.WRONG,
                              "doors": [{"upper": "X", "lower": "W", "kind": RF.NESTED}]},
                 ("V", "L"): {"side": RF.LOSS, "closes": RF.OWN, "where": RF.SOMEWHERE,
                              "verdict": RF.CP.RIGHT_VERDICT, "doors": []}}
        units = [{"case": 1, "group": "deflection", "right": True, "above": "W", "below": "L"},
                 {"case": 2, "group": "deflection", "right": False, "above": "W", "below": "L"},
                 {"case": 2, "group": "billing", "right": False, "above": "V", "below": "L"}]
        action = {"W": T2, "V": BILL, "L": SS}
        got = RF.read_run(units, found, {1: T2, 2: BILL}, action)
        a = got["all"]
        self.assertEqual((a["refusals"], a["cases"], a["door"]), (3, 2, 2))
        self.assertEqual(a["side"], {RF.WIN: 2, RF.LOSS: 1})
        self.assertEqual(a["closes"], {RF.OWN: 1, RF.CONTAINMENT: 2, RF.EITHER: 0})
        self.assertEqual(a["where"], {RF.SOMEWHERE: 1, RF.NOWHERE: 2})
        self.assertEqual((a["ranking_right"], a["declared_names_the_truth"]), (1, 2))
        self.assertEqual(got["by_group"]["deflection"]["refusals"], 2)
        n = got["nowhere"]
        self.assertEqual((n["refusals"], n["ranking_right"], n["declared_names_the_truth"],
                          n["both"], n["neither"]), (2, 1, 1, 1, 1))
        self.assertEqual(got["doors"][0]["refusals"], 2)
        self.assertEqual([e["refusals"] for e in got["edges"]], [1, 2])


def flip(record: dict, pos: int, verdict: str) -> str:
    """Set the verdict of the log's edge at `pos`, in the log and in its row's
    `edge_reasons` alike, and return the old one."""
    k = 0
    for row in record["records"]:
        reasons = row.get("edge_reasons") or []
        for i, why in enumerate(reasons):
            if why == RF.erb.OUTSIDE:
                continue
            if k == pos:
                old, reasons[i] = reasons[i], verdict
                record["edge_log"][pos][2] = verdict
                return old
            k += 1
    raise AssertionError("no such edge")


class TestGatesWithTeeth(unittest.TestCase):
    """On K r3's record: the gates pass, and a moved verdict or a target the
    log never refused fails them. Nothing of the reading is printed or pinned."""

    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(plan.run_path(plan.RANKED, 3).read_text())
        conflicts = json.loads(RF.conflicts_path().read_text())
        cls.rows = conflicts["readings"]["added"]["unordered"]["k_r3"]["rows"]
        cls.space, cls.truth = MI.space(), MI.space_truth()
        cls.targets = {(u["above"], u["below"]) for u in RF.refusals_of(cls.rows)}
        cls.got = RF.replay(cls.record, cls.space, cls.truth, cls.targets)

    def test_gates_one_and_two(self):
        self.assertTrue(self.got["log_ok"] and self.got["met_ok"])
        self.assertEqual(set(self.got["found"]), self.targets)
        ok = next(i for i, e in enumerate(self.record["edge_log"]) if e[2] == "ok")
        old = flip(self.record, ok, "cierra_ciclo")
        try:
            self.assertFalse(RF.replay(self.record, self.space, self.truth,
                                       self.targets)["log_ok"])
        finally:
            flip(self.record, ok, old)
        e = self.record["edge_log"][ok]
        self.assertFalse(RF.replay(self.record, self.space, self.truth,
                                   self.targets | {(e[0], e[1])})["met_ok"])

    def test_gate_three(self):
        self.assertTrue(RF.same_base(self.got["engine"], self.record, self.space))
        eng = self.got["engine"]
        w = next(r for r, s in eng.decl_above.items() if s)
        lost = next(iter(eng.decl_above[w]))
        eng.decl_above[w].discard(lost)
        try:
            self.assertFalse(RF.same_base(eng, self.record, self.space))
        finally:
            eng.decl_above[w].add(lost)


def fake(nowhere=6, own=4, door=6, n=10):
    a = {"refusals": n, "where": {RF.NOWHERE: nowhere, RF.SOMEWHERE: n - nowhere},
         "closes": {RF.OWN: own, RF.CONTAINMENT: n - own - 1, RF.EITHER: 1}, "door": door}
    return {"runs": {t: {"all": dict(a)} for t in RF.K_RUNS}}


def holds(readings) -> dict[str, bool]:
    return {c["clause"]: c["holds"] for c in RF.read_expectation(readings)}


CLAUSES = ["I1", "I2", "I3"]


class TestTheExpectation(unittest.TestCase):

    def test_three_clauses(self):
        self.assertEqual(list(holds(fake())), CLAUSES)

    def test_inside_the_lines(self):
        self.assertEqual(holds(fake()), {c: True for c in CLAUSES})

    def test_at_the_lines(self):
        self.assertEqual(holds(fake(nowhere=5, own=5, door=5)), {c: False for c in CLAUSES})

    def test_one_run_fails_each(self):
        r = fake()
        r["runs"]["k_r2"]["all"] = dict(r["runs"]["k_r2"]["all"], door=5,
                                        where={RF.NOWHERE: 5, RF.SOMEWHERE: 5})
        self.assertEqual(holds(r), {"I1": False, "I2": True, "I3": False})

    def test_over_nothing(self):
        self.assertEqual(holds({}), {c: False for c in CLAUSES})
        self.assertEqual(holds(fake(nowhere=0, own=0, door=0, n=0)),
                         {c: False for c in CLAUSES})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(RF, "read_inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                RF.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
