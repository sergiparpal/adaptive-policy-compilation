"""
`ranked/conflicts.py` — the POST-RUN reading of where K r2's conflicts fell, and
which births made them. No figure of the reading.

What is pinned is the instrument:
- a case's group, by the winner's queue and the runner-up's, either way;
- the rules behind a group, on cases built by hand: the cases each rule stands
  at, those that went wrong, those its queue won, and their order;
- K r2 at the others' deflection conflicts, on cases built by hand: who decided
  each arrival, whether right, and whether the queue that won or lost there
  stood; and no value without a run;
- the rules that won the errors, by group;
- the gates with teeth, on K r3's record: they pass on it, and a figure moved by
  one fails them;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import json
import unittest
from unittest import mock

from manual import instrument as MI
from ranked import conflicts as CF
from ranked import engine as E
from ranked import plan

SS, T2, T1, BILL, AM = CF.SS, CF.T2, CF.T1, CF.BILL, CF.AM
SEC = "SECURITY_INCIDENT"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}


class TestGroups(unittest.TestCase):

    def test_either_way(self):
        self.assertEqual(CF.group_of([SS, T2]), "deflection")
        self.assertEqual(CF.group_of([T2, SS, AM]), "deflection")
        self.assertEqual(CF.group_of([SS, T1]), "deflection")
        self.assertEqual(CF.group_of([AM, BILL]), "billing")
        self.assertEqual(CF.group_of([SS, BILL]), "billing")
        self.assertEqual(CF.group_of([AM, SS]), "rest")
        self.assertEqual(CF.group_of([T2, T1, SS]), "rest")      # the first two decide
        self.assertEqual(CF.group_of([SEC, T2]), "rest")


def case(idx, queues, standing, decision, truth, by=E.RANKING, governing="H24", reported=False):
    return {"case": idx, "by": by, "queues": list(queues), "standing": standing,
            "truth": truth, "governing": governing, "decision": decision,
            "right": decision is not None and decision == truth, "reported": reported}


def birth(rid, queue, kind="ERROR", report=None, verdict="nacida"):
    return {"rule_id": rid, "queue": queue, "born_at": 1, "kind": kind, "verdict": verdict,
            "escalation_rule": rid, "report": report, "governing": "H01",
            "birth_truth": queue, "right_at_birth": True, "conditions": [], "attributes": [],
            "points": 1, "own_points": 1}


BIRTHS = {r: birth(r, q) for r, q in (("R1", SS), ("R2", T1), ("R3", T2), ("R4", BILL),
                                      ("R5", AM), ("R6", SS))}


class TestBehind(unittest.TestCase):

    def test_the_rules_and_their_counts(self):
        cases = [case(1, [SS, T1], {SS: ["R1"], T1: ["R2"]}, SS, SS),
                 case(2, [SS, T1], {SS: ["R1", "R6"], T1: ["R2"]}, SS, T1, governing="H29"),
                 case(3, [T2, SS], {T2: ["R3"], SS: ["R6"]}, T2, SS),
                 case(4, [AM, BILL], {AM: ["R5"], BILL: ["R4"]}, AM, BILL),
                 case(5, [SS], {SS: ["R1"]}, SS, SS, by=E.RUNG2)]
        got = CF.behind(cases, BIRTHS, "deflection")
        self.assertEqual((got["cases"], got["wrong"]), (3, 2))
        rows = {r["rule_id"]: r for r in got["rules"]}
        self.assertEqual([r["rule_id"] for r in got["rules"]], ["R1", "R2", "R6", "R3"])
        self.assertEqual((rows["R1"]["cases"], rows["R1"]["wrong"], rows["R1"]["won"]), (2, 1, 2))
        self.assertEqual((rows["R6"]["cases"], rows["R6"]["wrong"], rows["R6"]["won"]), (2, 2, 1))
        self.assertEqual((rows["R3"]["cases"], rows["R3"]["won"]), (1, 1))
        self.assertEqual(got["by_governing"], {"H24": {"cases": 2, "wrong": 1},
                                               "H29": {"cases": 1, "wrong": 1}})
        self.assertEqual(got["by_pair"][f"{SS} / {T2}"], {"cases": 1, "wrong": 1})
        self.assertEqual(CF.behind(cases, BIRTHS, "billing")["cases"], 1)
        self.assertEqual(CF.behind(cases, BIRTHS, "rest")["cases"], 0)


class TestAtTheOthers(unittest.TestCase):

    def runs(self):
        k1 = [case(1, [SS, T1], {SS: ["R1"], T1: ["R2"]}, SS, SS),
              case(2, [T2, SS], {T2: ["R3"], SS: ["R1"]}, T2, T2),
              case(3, [AM, BILL], {AM: ["R5"], BILL: ["R4"]}, AM, AM)]
        k3 = [case(1, [SS, T1], {SS: ["R1"], T1: ["R2"]}, SS, SS),
              case(4, [SS, T1], {SS: ["R1"], T1: ["R2"]}, SS, T1, governing="H29")]
        k2 = [case(1, [SS], {SS: ["R6"]}, SS, SS, by=E.RUNG2),
              case(2, [T2, SS], {T2: ["R3"], SS: ["R6"]}, T2, T2),
              case(3, [AM], {AM: ["R5"]}, AM, AM, by=E.RUNG2),
              case(4, [], {}, None, T1, by=None, governing="H29")]
        return {"k_r1": k1, "k_r2": k2, "k_r3": k3}

    def test_each_arrival_once(self):
        got = CF.at_the_others(self.runs())
        self.assertEqual([r["case"] for r in got["rows"]], [1, 2, 4])     # 3 is billing's
        self.assertEqual(got["cases"], 3)
        self.assertEqual(got["by"], {E.RANKING: 1, E.RUNG2: 1, "None": 1})
        self.assertEqual(got["right"], 2)
        self.assertEqual(got["right_by"], {E.RANKING: 1, E.RUNG2: 1, "None": 0})
        self.assertEqual(got["one_queue_was"], {SS: 1})
        self.assertEqual(sorted(got["rows"][0]["others"]), ["k_r1", "k_r3"])

    def test_which_queue_stood(self):
        rows = {r["case"]: r for r in CF.at_the_others(self.runs())["rows"]}
        self.assertTrue(rows[1]["winners_queue_stood"])
        self.assertFalse(rows[1]["losers_queue_stood"])
        self.assertTrue(rows[2]["winners_queue_stood"] and rows[2]["losers_queue_stood"])
        self.assertFalse(rows[4]["winners_queue_stood"] or rows[4]["losers_queue_stood"])

    def test_no_value_without_a_run(self):
        runs = self.runs()
        del runs["k_r3"]
        self.assertIsNone(CF.at_the_others(runs))


class TestErrors(unittest.TestCase):

    def test_the_winners_rules_by_group(self):
        cases = [case(1, [BILL, SS], {BILL: ["R4"], SS: ["R1"]}, BILL, SS, governing="H12"),
                 case(2, [BILL, SS], {BILL: ["R4"], SS: ["R6"]}, BILL, SS, governing="H12"),
                 case(3, [AM, BILL], {AM: ["R5"], BILL: ["R4"]}, AM, BILL, governing="H11"),
                 case(4, [AM, BILL], {AM: ["R5"], BILL: ["R4"]}, AM, AM, governing="H09"),
                 case(5, [T2, SS], {T2: ["R3"], SS: ["R1"]}, T2, SS)]
        got = CF.errors(cases, BIRTHS)
        self.assertEqual(got["billing"]["wrong"], 3)
        self.assertEqual([(r["rule_id"], r["wrong"]) for r in got["billing"]["winner_rules"]],
                         [("R4", 2), ("R5", 1)])
        self.assertEqual(got["billing"]["by_truth_and_decision"],
                         {f"H11: {BILL} -> {AM}": 1, f"H12: {SS} -> {BILL}": 2})
        self.assertEqual([r["rule_id"] for r in got["deflection"]["winner_rules"]], ["R3"])
        self.assertEqual(got["rest"]["wrong"], 0)


class TestGatesWithTeeth(unittest.TestCase):
    """On K r3's record: the gates pass, and one figure moved fails them. Nothing
    of the reading is printed or pinned."""

    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(plan.run_path(plan.RANKED, 3).read_text())
        cls.kept = json.loads(CF.readings_path().read_text())["readings"]["A"]["cases"]["k_r3"]
        cls.space, cls.truth = MI.space(), MI.space_truth()
        cls.corpus = list(MI.corpus())
        cls.cases, cls.ok = CF.cases_of(cls.record, cls.space, cls.corpus)
        cls.births = CF.births_of(cls.record, cls.space, cls.truth)

    def test_gate_one(self):
        self.assertTrue(CF.same_as_a(self.cases, self.kept))
        moved = [dict(r) for r in self.kept]
        moved[0]["right"] = not moved[0]["right"]
        self.assertFalse(CF.same_as_a(self.cases, moved))
        self.assertFalse(CF.same_as_a(self.cases, self.kept[1:]))
        self.assertFalse(CF.same_as_a([], []))

    def test_gate_two(self):
        self.assertTrue(self.ok)
        logs = self.record["ranked"]["cases"]
        i = next(i for i, c in enumerate(logs) if c["by"] == "ranking")
        logs[i]["queues"] = list(reversed(logs[i]["queues"]))
        try:
            self.assertFalse(CF.cases_of(self.record, self.space, self.corpus)[1])
        finally:
            logs[i]["queues"] = list(reversed(logs[i]["queues"]))
        j = next(i for i, c in enumerate(logs) if c["by"] == "rung2")
        logs[j]["by"] = None
        try:
            self.assertFalse(CF.cases_of(self.record, self.space, self.corpus)[1])
        finally:
            logs[j]["by"] = "rung2"

    def test_gate_three(self):
        self.assertTrue(CF.born_of_its_escalation(self.cases, self.births))
        rid = next(r for c in self.cases if c["by"] == E.RANKING
                   for rs in c["standing"].values() for r in rs)
        moved = dict(self.births)
        moved[rid] = dict(moved[rid], verdict="sin_situar")
        self.assertFalse(CF.born_of_its_escalation(self.cases, moved))
        moved[rid] = dict(self.births[rid], escalation_rule="R9999")
        self.assertFalse(CF.born_of_its_escalation(self.cases, moved))

    def test_a_birth_is_its_rule(self):
        for d in self.record["rules"]:
            b = self.births[d["rule_id"]]
            self.assertEqual((b["queue"], b["born_at"]), (d["action"], d["born_at"]))
            self.assertEqual(b["right_at_birth"], b["queue"] == b["birth_truth"])
            self.assertLessEqual(b["own_points"], b["points"])


def fake(n1=10, top1=6, n3=10, top3=6, cases=10, rung2=6, right=6,
         winners=(("R1", "ERROR", BILL, BILL), ("R2", "ERROR", AM, AM))):
    def rules(top):
        return [{"cases": top}] if top else []

    return {
        "behind": {"k_r1": {"deflection": {"cases": n1, "rules": rules(top1)}},
                   "k_r3": {"deflection": {"cases": n3, "rules": rules(top3)}}},
        "k_r2_at_the_others": {"cases": cases, "right": right,
                               "by": {E.RANKING: 1, E.RUNG2: rung2, "None": 0}},
        "errors": {"k_r2": {"billing": {"winner_rules": [
            {"rule_id": r, "kind": k, "report": rep, "queue": q} for r, k, rep, q in winners]}}},
    }


def holds(readings) -> dict[str, bool]:
    return {c["clause"]: c["holds"] for c in CF.read_expectation(readings)}


CLAUSES = ["G1", "G2", "G3", "G4", "G5"]


class TestTheExpectation(unittest.TestCase):

    def test_five_clauses(self):
        self.assertEqual(list(holds(fake())), CLAUSES)

    def test_inside_the_lines(self):
        self.assertEqual(holds(fake()), {c: True for c in CLAUSES})

    def test_at_the_lines(self):
        four = tuple((f"R{k}", "ERROR", BILL, BILL) for k in range(4))
        got = holds(fake(top1=5, rung2=5, right=5, winners=four[:1] + (("R9", "IMPASSE",
                                                                         None, AM),) + four[1:]))
        self.assertEqual(got, {c: False for c in CLAUSES})

    def test_each_edge_alone(self):
        self.assertFalse(holds(fake(top3=5))["G1"])
        three = tuple((f"R{k}", "ERROR", BILL, BILL) for k in range(3))
        self.assertTrue(holds(fake(winners=three))["G4"])
        self.assertFalse(holds(fake(winners=three + (("R3", "ERROR", AM, AM),)))["G4"])
        self.assertFalse(holds(fake(winners=(("R1", "ERROR", SS, BILL),)))["G5"])
        self.assertTrue(holds(fake(winners=(("R1", "ERROR", SS, BILL),)))["G4"])

    def test_over_nothing(self):
        self.assertEqual(holds({}), {c: False for c in CLAUSES})
        self.assertEqual(holds(fake(n1=0, top1=0, cases=0, winners=())),
                         {c: False for c in CLAUSES})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(CF, "read_inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                CF.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
