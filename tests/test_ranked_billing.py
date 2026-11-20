"""
`ranked/billing.py` — the POST-RUN reading of why K r2's base decided `H11`'s
tickets wrong with one queue standing. No figure of the reading.

What is pinned is the instrument:
- a loss's class, from what keeps each matching rule of billing out: none
  matched, declared, containment or mixed;
- who declared the edges at a declared loss, and its verdict;
- one run's losses summed: by queue, by class, by who declared, and the edges
  that keep billing's rules out at the most losses;
- every edge the log accepted, by the birth that first accepted it, its newborn
  at one end;
- the gates with teeth, on K r3's record: the losses are `conflicts.json`'s
  count, billing stands at none, and a moved log or a missing installer fails
  them;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import json
import unittest
from unittest import mock

from manual import instrument as MI
from ranked import billing as BL
from ranked import plan

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SS, T1, AM, BILL = "SELF_SERVICE_DEFLECT", "T1_GENERAL", "ACCOUNT_MANAGER", BL.BILL
WRONG = BL.CP.WRONG


class TestClasses(unittest.TestCase):

    def test_kept(self):
        self.assertEqual(BL.kept_class([]), BL.NONE)
        self.assertEqual(BL.kept_class(["declared", "both"]), BL.DECLARED)
        self.assertEqual(BL.kept_class(["containment", "containment"]), BL.CONTAINMENT)
        self.assertEqual(BL.kept_class(["declared", "containment"]), BL.MIXED)

    def test_by(self):
        self.assertIsNone(BL.by_class([]))
        self.assertEqual(BL.by_class([BL.ABOVE, BL.ABOVE]), BL.ABOVE)
        self.assertEqual(BL.by_class([BL.BILLINGS]), BL.BILLINGS)
        self.assertEqual(BL.by_class([BL.ABOVE, BL.BILLINGS]), BL.BOTH)


def edge(above, by, verdict=WRONG, at=7, queue=SS):
    return {"above": above, "above_queue": queue, "installed_at": at, "by": by,
            "verdict": verdict}


def loss(case, queue, kept, cls, standing=("R1",)):
    return {"case": case, "queue": queue, "decision": queue, "reported": False,
            "standing": list(standing), "billing": kept, "class": cls}


class TestADeclaredLoss(unittest.TestCase):

    def test_side_and_verdict(self):
        x = loss(1, SS, [{"rule": "B1", "kind": "declared", "declared": [edge("R1", BL.ABOVE)],
                          "nested": []},
                         {"rule": "B2", "kind": "both",
                          "declared": [edge("R1", BL.ABOVE)], "nested": ["R5"]}], BL.DECLARED)
        self.assertEqual(BL.declared_side(x), (BL.ABOVE, "wrong"))
        x["billing"][1]["declared"][0]["verdict"] = BL.CP.EVEN
        self.assertEqual(BL.declared_side(x), (BL.ABOVE, "not all wrong"))
        x["billing"][1]["declared"][0]["by"] = BL.BILLINGS
        self.assertEqual(BL.declared_side(x)[0], BL.BOTH)
        self.assertEqual(BL.declared_side(dict(x, **{"class": BL.MIXED})), (None, None))


class TestOneRun(unittest.TestCase):

    def test_summed(self):
        births = {r: {"rule_id": r, "queue": q, "born_at": i}
                  for i, (r, q) in enumerate((("R1", SS), ("R2", T1), ("B1", BILL),
                                              ("B2", BILL)))}
        losses = [
            loss(10, SS, [{"rule": "B1", "kind": "declared",
                           "declared": [edge("R1", BL.ABOVE)], "nested": []}], BL.DECLARED),
            loss(450, SS, [{"rule": "B1", "kind": "declared",
                            "declared": [edge("R1", BL.ABOVE)], "nested": []}], BL.DECLARED),
            loss(460, T1, [{"rule": "B2", "kind": "declared",
                            "declared": [edge("R2", BL.BILLINGS, verdict=BL.CP.RIGHT_VERDICT,
                                              queue=T1)], "nested": []}], BL.DECLARED,
                 standing=("R2",)),
            loss(470, SS, [{"rule": "B1", "kind": "containment", "declared": [],
                            "nested": ["R1"]}], BL.CONTAINMENT),
            loss(5, SS, [], BL.NONE),
        ]
        got = BL.read_run(losses, births)
        self.assertEqual((got["losses"], got["matched"]), (5, 4))
        self.assertEqual(got["by_queue"], {SS: 4, T1: 1})
        self.assertEqual(got["by_class"], {BL.DECLARED: 3, BL.CONTAINMENT: 1, BL.MIXED: 0,
                                           BL.NONE: 1})
        self.assertEqual(got["declared_by"], {BL.ABOVE: 2, BL.BILLINGS: 1, BL.BOTH: 0})
        self.assertEqual(got["declared_wrong"], 2)
        self.assertEqual(got["by_tenth"], {"0": 2, "2": 3})
        self.assertEqual([(e["above"], e["below"], e["losses"]) for e in got["edges"]],
                         [("R1", "B1", 2), ("R2", "B2", 1)])
        self.assertEqual([(r["rule_id"], r["losses"]) for r in got["standing_rules"]],
                         [("R1", 4), ("R2", 1)])


class TestGatesWithTeeth(unittest.TestCase):
    """On K r3's record: the gates pass, and a moved log or a missing installer
    fails them. Nothing of the reading is printed or pinned."""

    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(plan.run_path(plan.RANKED, 3).read_text())
        conflicts = json.loads(BL.conflicts_path().read_text())
        cls.kept = conflicts["readings"]["added"]["arrivals_by_rule"]["k_r3"][BL.RULE]
        cls.space, cls.truth = MI.space(), MI.space_truth()
        cls.corpus = list(MI.corpus())
        cls.installed = BL.installers(cls.record)
        cls.losses, cls.log_ok, cls.stand_ok = BL.losses_of(
            cls.record, cls.space, cls.corpus, cls.installed, cls.truth)

    def test_the_installers(self):
        born = BL.erb.births(self.record)
        newborns = {d["rule_id"] for d in born.values()}
        for (w, l), at in self.installed.items():
            self.assertIn(at["newborn"], (w, l))
            self.assertIn(at["newborn"], newborns)
            self.assertEqual(born[at["born_at"]]["rule_id"], at["newborn"])

    def test_gates_one_and_two(self):
        self.assertTrue(self.log_ok and self.stand_ok)
        self.assertEqual(len(self.losses), self.kept["rung2_wrong"])
        for x in self.losses:
            self.assertFalse({k["rule"] for k in x["billing"]} & set(x["standing"]))
            self.assertNotEqual(x["queue"], BL.BILL)
        logs = self.record["ranked"]["cases"]
        j = next(i for i, c in enumerate(logs) if c["by"] == "rung2")
        logs[j]["by"] = "ranking"
        try:
            self.assertFalse(BL.losses_of(self.record, self.space, self.corpus, self.installed,
                                          self.truth)[1])
        finally:
            logs[j]["by"] = "rung2"

    def test_gate_three(self):
        declared = [d for x in self.losses for k in x["billing"] for d in k["declared"]]
        self.assertTrue(all(d["by"] is not None for d in declared))
        bare, _, _ = BL.losses_of(self.record, self.space, self.corpus, {}, self.truth)
        self.assertTrue(all(d["by"] is None for x in bare for k in x["billing"]
                            for d in k["declared"]))


def fake(n=10, matched=8, declared=5, above=3, wrong=3, k1=(8, 5), k3=(6, 4)):
    def run(m, d):
        return {"losses": n, "matched": m, "by_class": {BL.DECLARED: d}}
    return {"runs": {
        "k_r2": {"losses": n, "matched": matched, "by_class": {BL.DECLARED: declared},
                 "declared_by": {BL.ABOVE: above}, "declared_wrong": wrong},
        "k_r1": run(*k1), "k_r3": run(*k3)}}


def holds(readings) -> dict[str, bool]:
    return {c["clause"]: c["holds"] for c in BL.read_expectation(readings)}


CLAUSES = ["J1", "J2", "J3", "J4", "J5"]


class TestTheExpectation(unittest.TestCase):

    def test_five_clauses(self):
        self.assertEqual(list(holds(fake())), CLAUSES)

    def test_inside_the_lines(self):
        self.assertEqual(holds(fake()), {c: True for c in CLAUSES})

    def test_at_the_lines(self):
        got = holds(fake(matched=5, declared=2, above=1, wrong=1, k1=(8, 4), k3=(6, 3)))
        self.assertEqual(got, {c: False for c in CLAUSES})

    def test_each_edge_alone(self):
        self.assertFalse(holds(fake(k3=(6, 3)))["J5"])
        self.assertTrue(holds(fake(k3=(6, 3)))["J4"])
        self.assertFalse(holds(fake(wrong=2, declared=4, above=3))["J4"])

    def test_over_nothing(self):
        self.assertEqual(holds({}), {c: False for c in CLAUSES})
        self.assertEqual(holds(fake(n=0, matched=0, declared=0, above=0, wrong=0,
                                    k1=(0, 0), k3=(0, 0))), {c: False for c in CLAUSES})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(BL, "read_inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                BL.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
