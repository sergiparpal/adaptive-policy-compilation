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
- that the writer refuses unsigned before it reads or writes;
- and, added after the first run: what keeps a rule that matches a point from
  standing there; the arrivals by the rule governing them; how each pair of the
  ranking's cases stayed unordered, refused, never tried or installed; what
  kept the losing queue out of K r2; and every edge of K r3's log tried with
  its newborn at one end, which a moved entry breaks.
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


# ---------------------------------------------------------------------------
# Added after the first run
# ---------------------------------------------------------------------------

class FakeEngine:
    def __init__(self, ext, sub_below, decl_below):
        self.ext, self.sub_below, self.decl_below = ext, sub_below, decl_below

    def beats_me(self, rid):
        return self.sub_below[rid] | self.decl_below[rid]


class TestWhatKeepsARuleOut(unittest.TestCase):

    def test_each_kind(self):
        eng = FakeEngine(ext={"A": 0b111, "N": 0b001, "D": 0b011, "F": 0b100},
                         sub_below={"A": {"N"}, "N": set(), "D": set(), "F": set()},
                         decl_below={"A": {"D", "F"}, "N": set(), "D": set(), "F": set()})
        self.assertEqual(CF.defeat(eng, "A", 0b001), "both")          # N nested, D declared
        self.assertEqual(CF.defeat(eng, "A", 0b010), "declared")      # D alone matches
        self.assertEqual(CF.defeat(eng, "A", 0b100), "declared")      # F declared above it
        eng.decl_below["A"] = set()
        self.assertEqual(CF.defeat(eng, "A", 0b001), "containment")
        self.assertEqual(CF.defeat(eng, "A", 0b010), "neither")


class TestArrivalsByRule(unittest.TestCase):

    def test_who_decided_each(self):
        cases = [case(1, [BILL, SS], {}, BILL, SS, governing="H12"),
                 case(2, [SS], {}, SS, SS, by=E.RUNG2, governing="H12"),
                 case(3, [BILL], {}, BILL, SS, by=E.RUNG2, governing="H12"),
                 case(4, [], {}, None, BILL, by=None, governing="H11"),
                 case(5, [AM, BILL], {}, AM, AM, governing="H09")]
        got = CF.arrivals_by_rule(cases)
        self.assertEqual(list(got), ["H09", "H11", "H12"])
        self.assertEqual(got["H12"], {"arrivals": 3, "ranking_right": 0, "ranking_wrong": 1,
                                      "rung2_right": 1, "rung2_wrong": 1, "nobody": 0})
        self.assertEqual(got["H11"]["nobody"], 1)
        self.assertEqual(got["H09"]["ranking_right"], 1)


class TestUnordered(unittest.TestCase):

    def test_refused_never_tried_installed(self):
        action = {"R1": SS, "R2": T2, "R3": T2, "R4": BILL, "R5": SS, "R6": AM}
        history = {frozenset(("R1", "R2")): [("R1", "R2", "cierra_ciclo")],
                   frozenset(("R4", "R5")): [("R5", "R4", "cierra_ciclo")],
                   frozenset(("R6", "R4")): [("R6", "R4", "ok")]}
        cases = [case(1, [T2, SS], {T2: ["R2"], SS: ["R1"]}, T2, T2, governing="H16"),
                 case(2, [T2, SS], {T2: ["R3"], SS: ["R1"]}, T2, SS),
                 case(3, [BILL, SS], {BILL: ["R4"], SS: ["R5"]}, BILL, SS, governing="H12"),
                 case(4, [AM, BILL], {AM: ["R6"], BILL: ["R4"]}, AM, BILL, governing="H11"),
                 case(5, [SS], {SS: ["R1"]}, SS, SS, by=E.RUNG2)]
        got = CF.unordered(cases, history, action)
        kinds = {r["case"]: r["kind"] for r in got["rows"]}
        self.assertEqual(kinds, {1: "refused", 2: "never_tried", 3: "refused", 4: "installed"})
        named = {r["case"]: r["refused_named_the_truth"] for r in got["rows"]}
        self.assertEqual((named[1], named[3]), (False, True))   # SS above T2 at T2's; SS at SS's
        d = got["by_group"]["deflection"]
        self.assertEqual((d["cases"], d["refused"]["cases"], d["refused"]["right"],
                          d["never_tried"]["cases"]), (2, 1, 1, 1))
        self.assertEqual(d["refused"]["verdicts"], {"cierra_ciclo": 1})
        self.assertEqual(got["by_group"]["billing"]["refused"]["named_the_truth"], 1)
        self.assertEqual(got["by_group"]["billing"]["installed"]["cases"], 1)


class TestWhatKeptOut(unittest.TestCase):

    def test_each_class(self):
        others = {"rows": [
            {"case": c, "others": {"k_r1": {"won": T2, "lost": SS, "right": True}}}
            for c in (1, 2, 3, 4, 5, 6)]}
        k2 = [dict(case(1, [T2], {T2: ["R2"]}, T2, T2, by=E.RUNG2),
                   kept_out={"R1": [SS, "declared"], "R9": [T1, "containment"]}),
              dict(case(2, [T2], {T2: ["R2"]}, T2, T2, by=E.RUNG2),
                   kept_out={"R1": [SS, "both"], "R5": [SS, "declared"]}),
              dict(case(3, [T2], {T2: ["R2"]}, T2, T2, by=E.RUNG2),
                   kept_out={"R1": [SS, "containment"], "R5": [SS, "declared"]}),
              dict(case(4, [T2], {T2: ["R2"]}, T2, T2, by=E.RUNG2), kept_out={}),
              dict(case(5, [SS], {SS: ["R1"]}, SS, T2, by=E.RUNG2), kept_out={}),
              dict(case(6, [T2, SS], {T2: ["R2"], SS: ["R1"]}, T2, T2), kept_out={})]
        got = CF.what_kept_out(others, k2)
        self.assertEqual({r["case"]: r["class"] for r in got["rows"]},
                         {1: "declared", 2: "declared", 3: "mixed", 4: "none matched",
                          5: "a losing queue stood alone"})
        self.assertEqual(got["arrivals"], 5)
        self.assertEqual(got["by_class"]["a losing queue stood alone"], {"arrivals": 1, "right": 0})
        self.assertEqual(got["rows"][0]["kept_out"], {"R1": [SS, "declared"]})
        self.assertIsNone(CF.what_kept_out(None, k2))


class TestTheEdgesNewborns(unittest.TestCase):

    def test_on_k_r3(self):
        record = json.loads(plan.run_path(plan.RANKED, 3).read_text())
        self.assertTrue(CF.newborn_at_one_end(record))
        log = record["edge_log"]
        i = next(k for k, e in enumerate(log) if e[2] == "ok")
        others = [d["rule_id"] for d in record["rules"] if d["rule_id"] not in log[i][:2]]
        log[i] = [others[0], others[1], log[i][2]]
        self.assertFalse(CF.newborn_at_one_end(record))


if __name__ == "__main__":
    unittest.main()
