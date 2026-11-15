"""
`corrections/layer.py` — the POST-RUN reading of what the at-once asks wrote for
`ONCALL_ESCALATION` and the layer below it, no figure.

What is pinned is the instrument, on answers built by hand over the real space
and policy:
- a tiered answer, which keeps the queue for enterprise and business off hours
  and gives the layer its queues;
- the catalogue's reading, severity 1 to the queue;
- the loop's slices, the same with a rule of `T3_ENGINEERING` for severity 1 and
  the api nested in it.
Also pinned:
- the layer as the first match of `H06`, `H07` and `H08`;
- each base's reading, and its partitions;
- the asks chosen as Stage C chooses them, and the medians;
- one L run built by hand, its session and its Stage C curve made by
  `corrections/score.py`'s own `at_once` and `base_after`, every gate passing on
  it, and gates 1 to 3 each failing on its own;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
Added after the first run: a label of the queue with its ticket's attributes,
and how many times a reasoning writes the queue's identifier.
"""

from __future__ import annotations

import copy
import json
import unittest
from fractions import Fraction
from unittest import mock

from channel import lost as L
from channel import oncall as O
from corrections import layer as C
from corrections import plan
from corrections import score as sc
from manual import instrument as MI
from reasoned_loop import references as rl_refs
from reuse import structure as st

SPACE = MI.space()
TRUTH = MI.space_truth()
REGIONS = rl_refs.regions()
PARTS = O.parts(TRUTH[C.QUEUE], REGIONS)
LAYER = C.layer_of(SPACE, TRUTH)
ON, T3, T2 = C.QUEUE, C.T3, C.T2
IMP, ERR = plan.IMPASSE, plan.ERROR
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
M_ = SPACE.mask


def c_(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


def r_(action, *conds):
    return {"action": action, "conditions": list(conds), "beats": [], "loses_to": [], "note": ""}


SEV1 = c_("severity", "eq", 1)
API = c_("product", "eq", "api")
TIERED = {"rules": [r_(ON, SEV1, c_("customer_tier", "eq", "enterprise")),
                    r_(ON, SEV1, c_("customer_tier", "eq", "business"),
                       c_("off_hours", "eq", True)),
                    r_(T3, SEV1, c_("customer_tier", "eq", "business")),
                    r_(T3, SEV1, API),
                    r_(T2, SEV1)]}
BROAD = {"rules": [r_(ON, SEV1)]}
SLICES = {"rules": [r_(ON, SEV1), r_(T3, SEV1, API)]}


def read(payload):
    return C.read_base(C.installed(payload).engine, TRUTH, PARTS, LAYER)


class TestTheLayer(unittest.TestCase):

    def test_it_is_the_first_match_of_the_layer(self):
        self.assertEqual(LAYER, C.first_match_of_the_layer(REGIONS))
        self.assertTrue(LAYER)
        self.assertFalse(LAYER & TRUTH[ON])
        self.assertFalse(LAYER & M_["has_security_keyword"][True])


class TestABase(unittest.TestCase):

    def test_a_tiered_answer_keeps_the_queue_and_learns_the_layer(self):
        rd, ok = read(TIERED)
        self.assertTrue(ok)
        self.assertEqual(rd["recall"][ON], 1)
        self.assertEqual(rd["queue"]["right"], TRUTH[ON].bit_count())
        self.assertEqual(rd["layer"][C.RIGHT], LAYER.bit_count())
        self.assertEqual(rd["queue_rules"]["naming_the_tier"], 2)
        self.assertTrue(rd["queue_rules"]["holding_h04_whole"])
        self.assertTrue(rd["queue_rules"]["holding_h05_whole"])
        self.assertEqual(rd["queue_right_by_part"], {k: m.bit_count() for k, m in PARTS.items()})

    def test_the_catalogues_reading_takes_the_layer(self):
        rd, ok = read(BROAD)
        self.assertTrue(ok)
        self.assertEqual(rd["recall"][ON], 1)
        self.assertEqual(rd["layer"][C.AS_QUEUE], LAYER.bit_count())
        self.assertEqual(rd["recall"][T3], 0)
        self.assertEqual(rd["queue_rules"]["naming_the_tier"], 0)

    def test_the_loops_slices_take_the_queue(self):
        rd, ok = read(SLICES)
        self.assertTrue(ok)
        api = M_["product"]["api"]
        self.assertEqual(rd["queue"]["by_containment"], (TRUTH[ON] & api).bit_count())
        self.assertEqual(rd["queue"]["right"], (TRUTH[ON] & ~api).bit_count())
        self.assertEqual(rd["layer"][C.RIGHT], (LAYER & api & TRUTH[T3]).bit_count())
        self.assertEqual(rd["layer"][C.AS_QUEUE], (LAYER & ~api).bit_count())


class TestTheAsks(unittest.TestCase):

    def test_the_first_valid_answer_in_reask_order(self):
        rows = [{"checkpoint": 10, "k": 0, "reask": 1, "position": 0, "valid": True, "payload": "b"},
                {"checkpoint": 10, "k": 0, "reask": 0, "position": 5, "valid": False, "payload": "a"},
                {"checkpoint": 10, "k": 1, "reask": 0, "position": 1, "valid": True, "payload": "c"},
                {"checkpoint": 10, "k": 0, "reask": 2, "position": 2, "valid": True, "payload": "d"}]
        got = [(j, k, r["payload"]) for j, k, r in C.chosen({"rows": rows})]
        self.assertEqual(got, [(10, 0, "b"), (10, 1, "c")])

    def test_the_medians(self):
        reads = [read(p)[0] for p in (TIERED, BROAD, SLICES)]
        m = C.medians(reads, LAYER.bit_count())
        self.assertEqual(m["asks"], 3)
        self.assertEqual(m["queue_recall"]["fraction"], "1")
        self.assertEqual(m["asks_naming_the_tier"], 1)
        self.assertEqual(C.medians([], 1), {"asks": 0})


# One L run built by hand: the catalogue's rule born at an impasse at a ticket of
# H08, and two corrections at reported tickets of the layer.
def rule(rid, born, action, *conds):
    return {"rule_id": rid, "born_at": born, "action": action, "conditions": list(conds),
            "beats": [], "loses_to": [], "dropped_edges": [], "note": ""}


BIRTHS = [(IMP, "H08", T2, rule("R0001", 0, ON, SEV1)),
          (ERR, "H07", T3, rule("R0002", 1, T3, SEV1, API)),
          (ERR, "H08", T2, rule("R0003", 2, T2, SEV1, c_("customer_tier", "eq", "free")))]


def record(handed=None):
    rows = [{"idx": r["born_at"], "truth": truth, "truth_rule": gov, "cause": cause,
             "escalated": True, "edge_reasons": []} for cause, gov, truth, r in BIRTHS]
    handed = handed if handed is not None else {
        str(r["born_at"]): truth for cause, _, truth, r in BIRTHS if cause == ERR}
    return {"arm": "l", "rules": [r for *_, r in BIRTHS], "records": rows, "edge_log": [],
            "reports_handed": handed,
            "escalations": [{"idx": r["born_at"], "kind": cause, "verdict": L.BORN,
                             "rule_id": r["rule_id"], "listed": [], "copy_of": None,
                             "calls": [{"payload": {"action": r["action"],
                                                    "conditions": r["conditions"]}}]}
                            for cause, _, _, r in BIRTHS]}


REC = record()
PAIRS = [list(p) for p in C.ask.labelled(REC)]
J = plan.checkpoints(len(PAIRS))[-1]


def session(payloads=(TIERED, BROAD, SLICES), labelled=None):
    lab = PAIRS if labelled is None else labelled
    return {"labelled": lab,
            "rows": [{"checkpoint": J, "k": k, "reask": 0, "position": k, "valid": True,
                      "labelled": lab[:J], "payload": p} for k, p in enumerate(payloads)]}


def curve(ses=None):
    """Stage C's curve of the run, by `corrections/score.py`'s own functions."""
    asked = sc.at_once(ses or session())
    idx = C.ask.labelled(REC)[J - 1][0]
    return [{"labels": J, "case": idx, "loop": sc.frac(sc.base_after(REC, idx)),
             "at_once": {**asked[J], "space": sc.frac(asked[J]["space"])}}]


CURVE = curve()


def run(rec=None, ses=None, cur=None):
    return C.read_run(rec or REC, ses or session(), cur or CURVE, TRUTH, PARTS, LAYER)


def gate(r, k):
    return next(g["passes"] for g in r["gates"] if g["gate"] == k)


class TestTheRun(unittest.TestCase):

    def test_every_gate_passes(self):
        r = run()
        self.assertEqual([g["gate"] for g in r["gates"] if not g["passes"]], [])

    def test_the_checkpoint(self):
        c = run()["checkpoints"][0]
        self.assertEqual(c["make_up"], {"labels": 2, "naming_the_queue": 0,
                                        "tickets_of_the_layer": 2,
                                        "of_the_layer_by_queue": {T2: 1, T3: 1},
                                        "queue_tickets": []})
        self.assertEqual(c["at_once"]["median"]["asks"], 3)
        self.assertEqual([a["reasoning_names_the_queue"] for a in c["at_once"]["asks"]], [0, 0, 0])
        # The loop's base is the catalogue's rule with its two slices.
        loop, _ = C.read_base(C.loop_base(REC, 2), TRUTH, PARTS, LAYER)
        self.assertEqual(c["loop"]["queue"], loop["queue"])

    def test_gate_1_fails_on_other_labels(self):
        ses = session()
        ses["rows"][1]["labelled"] = ses["rows"][1]["labelled"][:1]
        self.assertFalse(gate(run(ses=ses, cur=curve(ses)), 1))

    def test_gate_2_fails_on_another_answer(self):
        cur = copy.deepcopy(CURVE)
        cur[0]["at_once"]["asks"][0]["space"] = sc.frac(Fraction(1, 2))
        self.assertFalse(gate(run(cur=cur), 2))

    def test_gate_3_fails_on_another_loop(self):
        cur = copy.deepcopy(CURVE)
        cur[0]["loop"] = sc.frac(Fraction(1, 3))
        self.assertFalse(gate(run(cur=cur), 3))

    def test_the_prior(self):
        ses = {"labelled": [], "rows": [{"checkpoint": 0, "k": k, "reask": 0, "position": k,
                                          "valid": True, "labelled": [], "payload": p}
                                         for k, p in enumerate((BROAD, BROAD, TIERED))]}
        stored = {str(j): {**v, "space": sc.frac(v["space"])} for j, v in sc.at_once(ses).items()}
        got = C.read_prior(ses, stored, TRUTH, PARTS, LAYER)
        self.assertTrue(all(g["passes"] for g in got["gates"]))
        self.assertEqual(got["asked"]["median"]["layer_as_the_queue"]["fraction"], "1")

    def test_the_record_holds_no_mask(self):
        text = json.dumps(st._rounded(run()), default=C.plain)
        self.assertLess(max(len(t) for t in text.split()), 200)


def fake_run(at_once_recalls, loop_recalls, layer_right, naming):
    cps = []
    for a, l in zip(at_once_recalls, loop_recalls):
        cps.append({"labels": len(cps), "loop": {"recall": {ON: sc.frac(Fraction(l))}},
                    "at_once": {"median": {"queue_recall": sc.frac(Fraction(a)),
                                           "layer_right": sc.frac(Fraction(layer_right)),
                                           "asks_naming_the_tier": naming}}})
    return {"checkpoints": cps}


def fake_prior(as_queue, recall):
    return {"asked": {"median": {"layer_as_the_queue": sc.frac(Fraction(as_queue)),
                                 "queue_recall": sc.frac(Fraction(recall))}}}


class TestTheExpectation(unittest.TestCase):

    def clauses(self, runs, prior):
        return {c["clause"]: c["holds"] for c in C.read_expectation(runs, prior)}

    def test_at_the_lines(self):
        runs = {t: fake_run(["1/2", "9/10"], ["1/2", "9/10"], "1/2", 2) for t in C.L_RUNS}
        self.assertEqual(self.clauses(runs, fake_prior("1/2", "9/10")),
                         {f"A{k}": True for k in range(1, 7)})

    def test_below_the_lines(self):
        runs = {t: fake_run(["1/2", "8/10"], ["1/2", "9/10"], "2/5", 1) for t in C.L_RUNS}
        self.assertEqual(self.clauses(runs, fake_prior("2/5", "8/10")),
                         {f"A{k}": False for k in range(1, 7)})

    def test_each_run_apart(self):
        runs = {t: fake_run(["1", "1"], ["0", "0"], "1", 3) for t in C.L_RUNS}
        runs[C.L_RUNS[1]] = fake_run(["1", "1/2"], ["0", "0"], "1/4", 1)
        got = self.clauses(runs, fake_prior("1", "1"))
        self.assertEqual({k: got[k] for k in ("A1", "A2", "A3", "A4")},
                         {"A1": True, "A2": False, "A3": False, "A4": False})

    def test_over_nothing(self):
        got = self.clauses({}, {"asked": None})
        self.assertEqual(got, {f"A{k}": False for k in range(1, 7)})


class TestAddedAfterTheFirstRun(unittest.TestCase):

    def test_a_label_of_the_queue_with_its_ticket(self):
        corpus = list(MI.corpus())
        got = C.make_up([(5, ON), (6, T2)], {5: {"truth_rule": "H05"}, 6: {"truth_rule": "H08"}},
                        corpus)
        self.assertEqual(got["naming_the_queue"], 1)
        self.assertEqual(got["queue_tickets"],
                         [{"case": 5, "governing": "H05",
                           **{a: getattr(corpus[5], a) for a in C.TICKET}}])
        self.assertNotIn("queue_tickets", C.make_up([(5, ON)], {5: {"truth_rule": "H05"}}))

    def test_what_the_reasoning_names(self):
        self.assertEqual(C.names_the_queue({"reasoning": "ONCALL_ESCALATION? no ONCALL_ESCALATION"}),
                         2)
        self.assertEqual(C.names_the_queue({"reasoning": "on-call, guardia"}), 0)
        self.assertEqual(C.names_the_queue({}), 0)


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(C, "read_all", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                C.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
