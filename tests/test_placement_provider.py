"""
`placement/provider.py` — the POST-RUN reading of whether the cut of the rarest
queue's drafts is the provider's, on the bridge, no figure.

What is pinned, on records built by hand:
- an answer read as a run's draft: one that holds its part, a cut by the first
  matched rule a cut changes, one with no condition, and the identifiers its note
  cites;
- gate 1 on a ticket asked twice, not asked of a provider, or asked past the
  first call, and on no ticket at all;
- gate 2 on a ticket governed by a rule that holds no part of the queue, and on
  one that lies first in another rule's region;
- each ticket's row with both providers' answers;
- the runs' drafts as `oncall.json` keeps them, gate 3 on points that differ, and
  the drafts counted by ticket;
- the expectation's clauses at their edges, and a reading without value;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from blind import rows as brows
from harness.domain import Case
from placement import plan
from placement import provider as V
from rung2.engine2 import Space

SPACE = Space()
OC = "ONCALL_ESCALATION"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def cond_(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


def ext(*conds):
    return brows.ext_of({"conditions": list(conds)}, SPACE)


def case_(**kw):
    values = dict(has_security_keyword=False, severity=1, customer_tier="enterprise",
                  product="api", channel="email", prior_tickets_30d=0, off_hours=False,
                  language="en")
    values.update(kw)
    return Case(**values)


SEV1 = cond_("severity", "eq", 1)
REGIONS = {
    "H04": ext(SEV1, cond_("customer_tier", "eq", "enterprise")),
    "H05": ext(SEV1, cond_("customer_tier", "eq", "business"), cond_("off_hours", "eq", True)),
    "H07": ext(SEV1, cond_("product", "eq", "api")),
    "H08": ext(SEV1),
    "H17": ext(cond_("product", "eq", "integrations"), cond_("severity", "lte", 2)),
    "H29": ext(cond_("severity", "gte", 1)),
}
TRUTH = REGIONS["H04"] | REGIONS["H05"]
PARTS = {"H04": REGIONS["H04"], "H05": REGIONS["H05"]}
H04_CASE = case_()                                        # severity 1, enterprise, api
H05_CASE = case_(customer_tier="business", off_hours=True, product="integrations")
CASES = (H04_CASE, H05_CASE)
LABELS = ((OC, "H04"), (OC, "H05"))


def payload_(*conds, note=""):
    return {"action": OC, "conditions": list(conds), "note": note}


class TestAnAnswer(unittest.TestCase):

    def read(self, payload, case=H04_CASE, gov="H04"):
        return V.read_draft(payload, case, gov, SPACE, PARTS, REGIONS, TRUTH)

    def test_an_answer_that_holds_its_part(self):
        got = self.read(payload_(SEV1, cond_("customer_tier", "eq", "enterprise"),
                                 note="H04 antes que H07."))
        self.assertTrue(got["holds_part"])
        self.assertEqual((got["cut_by"], got["cites"]), ([], ["H04", "H07"]))
        self.assertFalse(got["cut_by_the_first_cutting_match"])

    def test_a_cut_by_the_first_match_a_cut_changes(self):
        got = self.read(payload_(SEV1, cond_("customer_tier", "eq", "enterprise"),
                                 cond_("product", "eq", "api")))
        self.assertFalse(got["holds_part"])
        self.assertEqual((got["cut_by"], got["first_cutting_match"]), (["H07"], "H07"))
        self.assertTrue(got["cut_by_the_first_cutting_match"])
        self.assertEqual(got["draft_part_points"], (REGIONS["H04"] & REGIONS["H07"]).bit_count())

    def test_an_answer_with_no_condition(self):
        got = self.read({})
        self.assertFalse(got["holds_part"])
        self.assertEqual((got["queue"], got["draft_points"], got["cut_by"]), (None, None, None))


def ask_(idx, provider, round_=0, payload=None):
    return {"idx": idx, "provider": provider, "round": round_, "payload": payload,
            "served_by": provider, "finish_reason": "stop"}


class TestTheBridge(unittest.TestCase):

    def test_gate_1(self):
        bridge = {"asks": [ask_(0, V.BAIDU), ask_(0, V.DEEPINFRA), ask_(1, V.BAIDU),
                           ask_(1, V.DEEPINFRA), ask_(9, V.BAIDU)]}
        self.assertTrue(V.asked_once(V.asks_at(bridge, [0, 1]), [0, 1]))
        twice = {"asks": bridge["asks"] + [ask_(1, V.BAIDU)]}
        self.assertFalse(V.asked_once(V.asks_at(twice, [0, 1]), [0, 1]))
        missing = {"asks": bridge["asks"][:3]}
        self.assertFalse(V.asked_once(V.asks_at(missing, [0, 1]), [0, 1]))
        later = {"asks": bridge["asks"][:3] + [ask_(1, V.DEEPINFRA, round_=1)]}
        self.assertFalse(V.asked_once(V.asks_at(later, [0, 1]), [0, 1]))
        self.assertFalse(V.asked_once({}, []))

    def test_gate_2(self):
        self.assertTrue(V.governed_first([0, 1], LABELS, CASES, SPACE, REGIONS))
        self.assertFalse(V.governed_first([0], ((OC, "H07"),), CASES, SPACE, REGIONS))
        self.assertFalse(V.governed_first([0], ((OC, "H05"),), CASES, SPACE, REGIONS))

    def test_each_ticket_with_both_answers(self):
        whole = payload_(SEV1, cond_("customer_tier", "eq", "enterprise"))
        cut = payload_(SEV1, cond_("customer_tier", "eq", "enterprise"),
                       cond_("product", "eq", "api"))
        asks = V.asks_at({"asks": [ask_(0, V.BAIDU, payload=whole),
                                   ask_(0, V.DEEPINFRA, payload=cut)]}, [0])
        got = V.bridge_answers(asks, [0], LABELS, CASES, SPACE, PARTS, REGIONS, TRUTH)[0]
        self.assertEqual((got["governing"], got["part_points"]),
                         ("H04", REGIONS["H04"].bit_count()))
        self.assertTrue(got[V.BAIDU]["holds_part"])
        self.assertFalse(got[V.DEEPINFRA]["holds_part"])
        self.assertEqual(got[V.DEEPINFRA]["cut_by"], ["H07"])
        self.assertEqual(got[V.BAIDU]["finish_reason"], "stop")


class TestTheRuns(unittest.TestCase):

    def test_the_drafts_as_oncall_json_keeps_them(self):
        oncall = {"runs": {"v1c_r3": {
            "drafts": [{"idx": 0, "governing": "H04", "draft_queue_points": 5,
                        "draft_part_points": 5, "holds_part": False, "verdict": "nacida"}],
            "cuts": [{"idx": 0, "cut_by": ["H07"], "cut_by_the_first_cutting_match": True}]}}}
        got = V.placement_drafts(oncall)["v1c_r3"][0]
        self.assertEqual((got["cut_by"], got["cut_by_the_first_cutting_match"]),
                         (["H07"], True))
        self.assertEqual((got["holds_part"], got["verdict"]), (False, "nacida"))

    def test_gate_3(self):
        read = {"c_r1": [{"idx": 0, "draft_queue_points": 5}, {"idx": 1, "draft_queue_points": 7}]}
        recorded = {"runs": {"c_r1": {"reading": {"escalations": [
            {"idx": 0, "draft_queue_points": 5}, {"idx": 1, "draft_queue_points": 7}]}}}}
        self.assertTrue(V.same_points(read, recorded))
        recorded["runs"]["c_r1"]["reading"]["escalations"][1]["draft_queue_points"] = 8
        self.assertFalse(V.same_points(read, recorded))
        self.assertFalse(V.same_points({}, recorded))

    def test_the_drafts_counted_by_ticket(self):
        drafts = {"a": [{"idx": 0, "holds_part": True}, {"idx": 5, "holds_part": True}],
                  "b": [{"idx": 0, "holds_part": False}]}
        got = V.by_ticket(drafts, [0, 1])
        self.assertEqual((got[0]["drafts"], got[0]["holding_the_part"], got[0]["runs"]),
                         (2, 1, ["a", "b"]))
        self.assertEqual(got[1]["drafts"], 0)
        self.assertNotIn(5, got)


def row_(idx, gov, baidu_whole, deepinfra_whole, deepinfra_cut=None, first=True):
    return {"idx": idx, "governing": gov,
            V.BAIDU: {"holds_part": baidu_whole, "cut_by": None},
            V.DEEPINFRA: {"holds_part": deepinfra_whole, "cut_by": deepinfra_cut,
                          "first_cutting_match": "H07",
                          "cut_by_the_first_cutting_match": bool(deepinfra_cut) and first}}


class TestTheExpectation(unittest.TestCase):

    def holds(self, rows):
        return [c["holds"] for c in V.read_expectation({r["idx"]: r for r in rows})]

    def test_clause_by_clause_at_their_edges(self):
        account = [row_(1, "H04", True, False, ["H07"]), row_(2, "H04", True, False, ["H17"]),
                   row_(3, "H04", False, False), row_(4, "H05", False, True)]
        self.assertEqual(self.holds(account), [True] * 4)
        against = [row_(1, "H04", True, True), row_(2, "H04", False, False, ["H07"], False),
                   row_(3, "H05", False, True)]
        self.assertEqual(self.holds(against), [False] * 4)

    def test_q3_needs_strictly_more(self):
        rows = [row_(1, "H04", True, False, ["H07"]), row_(2, "H05", False, True)]
        self.assertFalse(self.holds(rows)[2])

    def test_a_reading_without_value_does_not_hold(self):
        x = self.holds([row_(1, "H05", False, False)])
        self.assertEqual((x[0], x[1], x[3]), (False, False, False))

    def test_the_lines(self):
        self.assertEqual((V.Q2_WHOLE, V.QUEUE, V.BAIDU, V.DEEPINFRA),
                         (2, OC, "baidu", "deepinfra"))
        self.assertEqual(len(V.CHANNEL_RUNS), 6)


class TestUnsigned(unittest.TestCase):

    def test_it_refuses_before_reading_or_writing(self):
        for argv in ([], ["--dry-run"]):
            with self.subTest(argv=argv), \
                 mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                 mock.patch.object(Path, "read_text",
                                   side_effect=AssertionError("read")) as read, \
                 mock.patch.object(Path, "write_text",
                                   side_effect=AssertionError("wrote")) as write:
                with self.assertRaises(SystemExit):
                    V.main(argv)
                read.assert_not_called()
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
