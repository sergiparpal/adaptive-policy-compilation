"""
`corrections/oncall.py` — the POST-RUN reading of why L loses
`ONCALL_ESCALATION`, no figure.

What is pinned is the instrument, on one run built by hand over the real space
and the real policy. Its rule of the queue `Q` holds `H04`'s region, and the
queue loses points in each way:
- `C`, of `T3_ENGINEERING`, born at a reported error of `H06`, writes the
  severity-1 business tickets, `H05`'s part among them, which no rule of the
  queue matches: unwritten;
- `A`, of `T3_ENGINEERING`, born at a reported error, nested in `Q`, takes its
  api tickets by containment;
- `X`, of `ACCOUNT_MANAGER`, born at a reported error, crosses `Q` and is
  declared above it, so it takes their shared points by an edge;
- `Y`, of `T2_TECHNICAL`, born at a conflict, crosses `Q`, beats `X`, and its
  declared loss to `Q` is refused for the cycle that win closes, so their
  shared points are contested. Installed losses first, `Q` beats it.
Also pinned:
- Stage C's recall handed as a count, and -1 where it is no whole count;
- each rule's birth, and the reports held to the tickets' true queues;
- the partitions of the taken points, and the history of a lost point;
- the replays, each the one its record keeps, and what each gives back;
- every gate on that run, and gates 6 to 8 each failing on its own;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
Added after the first run, on the same run and on one with a later rule of the
queue: the rule that erred at each taker's ticket, and the edges between each
taker and the queue's rules, its own and the later ones, by verdict.
"""

from __future__ import annotations

import copy
import json
import unittest
from fractions import Fraction
from unittest import mock

from channel import lost as L
from channel import oncall as O
from corrections import carry as cr
from corrections import fall as fl
from corrections import oncall as C
from corrections import paths as pa
from corrections import plan
from harness.ceiling_check import all_cases
from manual import instrument as MI
from reasoned_loop import references as rl_refs
from reuse import structure as st
from rung2.engine2 import EDGE_CYCLE, EDGE_OK

SPACE = MI.space()
TRUTH = MI.space_truth()
CASES = list(all_cases())
REGIONS = rl_refs.regions()
ON, SEC, T2, T3, AM = ("ONCALL_ESCALATION", "SECURITY_INCIDENT", "T2_TECHNICAL",
                       "T3_ENGINEERING", "ACCOUNT_MANAGER")
IMP, ERR, CON = plan.IMPASSE, plan.ERROR, plan.CONFLICT
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
TAG = "l_r1"
M_ = SPACE.mask


def c_(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


def r_(rid, born, action, conds):
    return {"rule_id": rid, "born_at": born, "action": action, "conditions": list(conds),
            "beats": [], "loses_to": [], "dropped_edges": [], "note": ""}


SEV1 = c_("severity", "eq", 1)
ENTERPRISE = c_("customer_tier", "eq", "enterprise")
# (cause, the ticket's governing rule, its true queue, the rule born there)
BIRTHS = [
    (IMP, "H04", ON, r_("Q", 0, ON, [SEV1, ENTERPRISE])),
    (IMP, "H01", SEC, r_("S", 1, SEC, [c_("has_security_keyword", "eq", True)])),
    (ERR, "H06", T3, r_("C", 2, T3, [SEV1, c_("customer_tier", "eq", "business")])),
    (ERR, "H07", T3, r_("A", 3, T3, [SEV1, ENTERPRISE, c_("product", "eq", "api")])),
    (ERR, "H13", AM, r_("X", 4, AM, [ENTERPRISE, c_("prior_tickets_30d", "gte", 5)])),
    (CON, "H08", T2, r_("Y", 5, T2, [c_("product", "eq", "mobile")])),
]
# Each birth's edges in the record's order: Y's win first, then its refused loss.
EDGES = [(1, "S", "Q"), (4, "X", "Q"), (5, "Y", "X"), (5, "Q", "Y", EDGE_CYCLE)]


def record(arm="l", births=None, edges=None, handed=None, erred=None):
    births = births or BIRTHS
    erred = erred or {}
    rows = [{"idx": rule["born_at"], "truth": truth, "truth_rule": gov, "cause": cause,
             "escalated": True, "reported": cause == ERR, "edge_reasons": [],
             "engine_rule": (erred.get(rule["born_at"]) or (None, None))[0],
             "engine_action": (erred.get(rule["born_at"]) or (None, None))[1]}
            for cause, gov, truth, rule in births]
    log = []
    for born, w, l, *why in (edges if edges is not None else EDGES):
        reason = why[0] if why else EDGE_OK
        rows[born]["edge_reasons"].append(reason)
        log.append([w, l, reason])
    if handed is None:
        handed = ({str(rule["born_at"]): truth for cause, _, truth, rule in births
                   if cause == ERR} if arm == "l" else {})
    return {"arm": arm, "rules": [rule for *_, rule in births], "records": rows,
            "edge_log": log, "reports_handed": handed,
            "escalations": [{"idx": rule["born_at"], "kind": cause, "listed": [],
                             "verdict": L.BORN, "rule_id": rule["rule_id"], "copy_of": None,
                             "calls": [{"payload": {"action": rule["action"],
                                                    "conditions": rule["conditions"]}}]}
                            for cause, _, _, rule in births]}


REC = record()
ENGINE = cr.replay(REC, SPACE, TRUTH)["engine"]
N_ = SPACE.n


def counts_of(rec):
    """A Stage C for the hand-built run: its own final base's recall."""
    eng = cr.replay(rec, SPACE, TRUTH)["engine"]
    out = {}
    for q in C.QUEUES:
        right = L.ways(eng, TRUTH[q], q)["right"].bit_count()
        out[q] = {"fraction": str(Fraction(right, TRUTH[q].bit_count()))}
    return {"CR-g": {"runs": {TAG: {"recall": out}}}}


def fall_run(rec):
    """What `fall.json` keeps of the run."""
    eng = cr.replay(rec, SPACE, TRUTH)["engine"]
    right = sum(L.ways(eng, TRUTH[q], q)["right"].bit_count() for q in TRUTH)
    stage_c = {"space": {"fraction": str(Fraction(right, N_))}, "curve": []}
    got = fl.read_run(rec, SPACE, TRUTH, CASES, stage_c, final=eng)
    return json.loads(json.dumps(st._rounded(got), default=C.plain))


def paths_run(rec):
    """What `paths.json` keeps of the run's where replay."""
    w = pa.where_replay(rec, SPACE, TRUTH, CASES)
    return {"added_after_the_first_run": {"where": {"engine": st._rounded(
        fl.order_summary({**w, "cycles": w["refused"]}, TRUTH, N_))}}}


def carry_run(rec):
    """What `carry.json` keeps of the run's doors replay, with no door."""
    return {"replays": {C.DOORS: st._rounded(cr.summary(cr.replay(rec, SPACE, TRUTH),
                                                       TRUTH, N_))}}


NO_GATEWAY = {"gateways": [], "doors": []}


def read(rec=None, frun=None, prun=None, crun=None):
    rec = rec or REC
    stage_c = C.stage_c_counts(counts_of(rec), {q: TRUTH[q].bit_count() for q in C.QUEUES})
    oncall = O.read_all_runs({TAG: rec}, stage_c)[TAG]
    return C.read_run(rec, oncall, SPACE, TRUTH, CASES, REGIONS, stage_c,
                      frun or fall_run(rec), prun or paths_run(rec), crun or carry_run(rec),
                      NO_GATEWAY, TAG)


RUN = read()


def gate(run, k, queue=None):
    return all(g["passes"] for g in run["gates"] if g["gate"] == k and g["queue"] == queue)


class TestStageC(unittest.TestCase):

    def test_a_recall_is_handed_as_a_count(self):
        score = {"CR-g": {"runs": {"l_r1": {"recall": {ON: {"fraction": "2/5"},
                                                      SEC: {"fraction": "1"}}}}}}
        got = C.stage_c_counts(score, {ON: 6300, SEC: 50400})
        self.assertEqual(got["CH-g"]["runs"]["l_r1"]["recall_space"],
                         {ON: [2520, 6300], SEC: [50400, 50400]})

    def test_a_recall_that_is_no_whole_count_gives_minus_one(self):
        score = {"CR-g": {"runs": {"l_r1": {"recall": {ON: {"fraction": "1/7"}}}}}}
        got = C.stage_c_counts(score, {ON: 6300 + 1})
        self.assertEqual(got["CH-g"]["runs"]["l_r1"]["recall_space"][ON], [-1, 6301])


class TestTheBirths(unittest.TestCase):

    def test_each_rule_with_its_birth(self):
        b = C.births_of(REC)
        self.assertEqual(b["C"], {"born_at": 2, "cause": ERR, "truth": T3, "governing": "H06",
                                  "label": T3})
        self.assertEqual(b["Y"]["label"], None)
        self.assertEqual(b["Q"]["cause"], IMP)

    def test_the_reports_are_the_truth(self):
        self.assertTrue(C.reports_are_the_truth(REC))
        self.assertTrue(C.reports_are_the_truth(record(arm="n")))

    def test_a_report_naming_another_queue_fails(self):
        self.assertFalse(C.reports_are_the_truth(record(handed={"2": T3, "3": T2, "4": AM})))

    def test_a_reported_error_without_its_report_fails(self):
        self.assertFalse(C.reports_are_the_truth(record(handed={"2": T3, "3": T3})))

    def test_an_n_record_that_handed_a_report_fails(self):
        self.assertFalse(C.reports_are_the_truth(record(arm="n", handed={"2": T3})))


class TestTheTakers(unittest.TestCase):

    def setUp(self):
        self.w = L.ways(ENGINE, TRUTH[ON], ON)
        self.summary, self.masks = C.takers(self.w, C.births_of(REC), ENGINE, REC,
                                            O.parts(TRUTH[ON], REGIONS))

    def test_the_queue_loses_in_every_way(self):
        w = self.w
        for k in ("unwritten", "by_containment", "by_edge", "contested"):
            self.assertTrue(w[k], k)
        # The unwritten points are H05's part, which C writes, but its mobile
        # tickets, where C and Y are left in a conflict no rule of the queue sees.
        h05 = O.parts(TRUTH[ON], REGIONS)[O.UNREACHED]
        mobile = M_["product"]["mobile"]
        self.assertEqual(w["unwritten"], h05 & ~mobile)
        self.assertEqual(w["conflict"] & h05, h05 & mobile)
        self.assertFalse(w["contested"] & h05)

    def test_the_partitions_cover_the_taken_points(self):
        taken = C.taken_of(self.w)
        self.assertTrue(taken)
        for m in self.masks.values():
            self.assertTrue(C.partitions_ok(m, taken))
        self.assertEqual(sum(self.summary["by_cause"].values()), taken.bit_count())

    def test_the_corrections_and_the_layer(self):
        by_rule = {r["rule_id"]: r for r in self.summary["takers"]}
        self.assertEqual(set(by_rule), {"C", "A", "X", "Y"})
        self.assertEqual(by_rule["C"]["unwritten"], by_rule["C"]["taken"])
        self.assertEqual(by_rule["A"]["by_edge"], 0)
        self.assertEqual(by_rule["X"]["by_edge"], by_rule["X"]["taken"])
        # C, A and X were born at reported errors; Y at a conflict.
        y_alone = self.masks["by_cause"][C.NONE]
        self.assertEqual(y_alone.bit_count(), by_rule["Y"]["taken"])
        # C, A and Y were born at tickets of H06, H07 and H08; X at one of H13.
        self.assertEqual(self.masks["by_layer"][C.NONE].bit_count(), by_rule["X"]["taken"])

    def test_a_partition_by_hand(self):
        got = C.partition({"a": 0b0110, "b": 0b0011}, 0b0111, lambda r: r == "a")
        self.assertEqual(got, {C.EVERY: 0b0100, C.SOME: 0b0010, C.NONE: 0b0001})
        self.assertFalse(C.partitions_ok({C.EVERY: 0b01, C.NONE: 0b01}, 0b01))


class TestTheHistory(unittest.TestCase):

    def test_by_hand(self):
        def s(i, rid, right, lost, kind):
            return {"idx": i, "rule_id": rid, "action": T3, "cause": ERR, "right": right,
                    "lost": lost, **{k: (lost if k == kind else 0) for k in fl.LOSSES}}
        steps = [s(0, "a", 0b0011, 0, fl.CONFLICT), s(1, "b", 0b0001, 0b0010, fl.BY_EDGE),
                 s(2, "c", 0b0011, 0, fl.CONFLICT), s(3, "d", 0b0000, 0b0011, fl.BY_CONTAINMENT)]
        births = {k: {"label": None, "governing": "H06"} for k in "abcd"}
        got, masks = C.history(steps, 2, 0b0111, 0b0111, births)
        self.assertEqual(got["never_right"], 1)
        self.assertEqual(masks["never"], 0b0100)
        # Point 1 was lost at b, regained at c and lost again at d: d is its last loss.
        self.assertEqual([(r["rule_id"], r["points"], r["after_the_peak"])
                          for r in got["losses"]], [("d", 2, True)])
        self.assertTrue(C.history_ok(masks, got, 0b0111))
        self.assertFalse(C.history_ok({**masks, "never": 0b0101}, got, 0b0111))

    def test_on_the_run(self):
        h = RUN["history"][ON]
        kinds = h["last_losses"]["by_kind"]
        self.assertTrue(all(kinds[k] for k in fl.LOSSES), kinds)
        # H05's part was an impasse until C wrote it: never right.
        self.assertGreaterEqual(h["never_right"], 2100)
        self.assertEqual(h["never_right"] + h["last_losses"]["points"], h["lost"])


class TestTheLevers(unittest.TestCase):

    def test_the_masks_replay_is_each_replay(self):
        rec_order = cr.replay(REC, SPACE, TRUTH)
        plain = C.masks_replay(REC, SPACE, TRUTH)
        for k in ("curve", "right", "security", "conflict", "cycles"):
            self.assertEqual(plain[k], rec_order[k], k)
        lf = C.masks_replay(REC, SPACE, TRUTH, losses_first=True)
        ref = fl.order_replay(REC, SPACE, TRUTH, losses_first=True)
        for k in ("curve", "right", "security", "conflict", "cycles"):
            self.assertEqual(lf[k], ref[k], k)
        wh = C.masks_replay(REC, SPACE, TRUTH, where=True)
        ref = pa.where_replay(REC, SPACE, TRUTH, CASES)
        self.assertEqual((wh["curve"], wh["right"], wh["cycles"]),
                         (ref["curve"], ref["right"], ref["refused"]))
        self.assertTrue(all(g["masks_ok"] for g in (plain, lf, wh)))

    def test_the_losses_first_give_the_contested_points_back(self):
        g = RUN["levers"]["by_queue"][ON]
        self.assertGreater(g[C.LOSSES_FIRST]["gives_back"], 0)
        self.assertEqual(g[C.LOSSES_FIRST]["turned_wrong"], 0)
        # With no door, the doors replay is the record's order.
        self.assertEqual(g[C.DOORS]["gives_back"], 0)
        self.assertEqual(RUN["levers"]["doors_left_out"], [])


class TestTheRun(unittest.TestCase):

    def test_every_gate_passes(self):
        failed = [(g["gate"], g["queue"]) for g in RUN["gates"] if not g["passes"]]
        self.assertEqual(failed, [])
        self.assertEqual(sorted({(g["gate"], g["queue"]) for g in RUN["gates"]}),
                         sorted([(k, ON) for k in range(1, 6)] + [(k, SEC) for k in range(1, 5)]
                                + [(k, None) for k in (6, 7, 8)]))

    def test_the_split_by_the_peak_covers_the_lost_points(self):
        for q in C.QUEUES:
            p = RUN["by_peak"][q]
            w = L.ways(ENGINE, TRUTH[q], q)
            self.assertEqual(p[C.AT_PEAK]["lost"] + p[C.BEFORE_PEAK]["lost"],
                             w["lost"].bit_count())

    def test_gate_6_fails_on_a_wrong_report(self):
        rec = record(handed={"2": T3, "3": T2, "4": AM})
        self.assertFalse(gate(read(rec, fall_run(REC), paths_run(REC), carry_run(REC)), 6))

    def test_gate_7_fails_on_another_peak(self):
        frun = fall_run(REC)
        frun["summary"]["peak"]["birth"] += 1
        self.assertFalse(gate(read(REC, frun), 7))

    def test_gate_7_fails_on_other_points_lost_at_the_peak(self):
        frun = fall_run(REC)
        frun["summary"]["lost"]["by_true_queue"][ON] = 1 + frun["summary"]["lost"][
            "by_true_queue"].get(ON, 0)
        self.assertFalse(gate(read(REC, frun), 7))

    def test_gate_8_fails_on_another_curve(self):
        frun = fall_run(REC)
        frun["curve"][-1]["right"] += 1
        self.assertFalse(gate(read(REC, frun), 8))

    def test_gate_8_fails_on_another_replay(self):
        frun = fall_run(REC)
        frun["added_after_the_first_run"]["orders"]["losses_first"]["refused_for_a_cycle"] += 1
        self.assertFalse(gate(read(REC, frun), 8))
        prun = paths_run(REC)
        prun["added_after_the_first_run"]["where"]["engine"]["conflict"]["points"] += 1
        self.assertFalse(gate(read(REC, None, prun), 8))
        crun = carry_run(REC)
        crun["replays"][C.DOORS]["final"]["right"] += 1
        self.assertFalse(gate(read(REC, None, None, crun), 8))

    def test_the_record_holds_no_mask(self):
        text = json.dumps(st._rounded(RUN), default=C.plain)
        self.assertLess(max(len(t) for t in text.split()), 200)


def fake(at_lost, contested, before_lost, outranked, by_edge, outr_all, taken, every_err,
         every_layer, gives_back, sec_before, sec_t2):
    return {"by_peak": {ON: {C.AT_PEAK: {"lost": at_lost, "contested": contested},
                             C.BEFORE_PEAK: {"lost": before_lost, "outranked": outranked}},
                        SEC: {C.BEFORE_PEAK: {"lost": sec_before, "by_queue": {T2: sec_t2}}}},
            "oncall": {"reading": {"ways": {"by_edge": by_edge, "outranked": outr_all}}},
            "takers": {ON: {"points": taken, "by_cause": {C.EVERY: every_err},
                            "by_layer": {C.EVERY: every_layer}}},
            "levers": {"by_queue": {ON: {C.LOSSES_FIRST: {"gives_back": gives_back}}}}}


class TestTheExpectation(unittest.TestCase):

    def clauses(self, runs):
        return {c["clause"]: c["holds"] for c in C.read_expectation(runs)}

    def test_at_the_lines(self):
        runs = {t: fake(10, 5, 10, 5, 3, 6, 8, 4, 4, 5, 10, 5) for t in C.L_RUNS}
        self.assertEqual(self.clauses(runs), {f"O{k}": True for k in range(1, 8)})

    def test_below_the_lines(self):
        runs = {t: fake(10, 4, 10, 4, 2, 6, 8, 3, 3, 4, 10, 4) for t in C.L_RUNS}
        self.assertEqual(self.clauses(runs), {f"O{k}": False for k in range(1, 8)})

    def test_pooled_not_each(self):
        runs = {C.L_RUNS[0]: fake(10, 0, 10, 0, 0, 6, 8, 0, 0, 0, 10, 0),
                C.L_RUNS[1]: fake(10, 10, 10, 10, 6, 6, 8, 8, 8, 10, 10, 10),
                C.L_RUNS[2]: fake(10, 5, 10, 5, 3, 6, 8, 4, 4, 5, 10, 5)}
        self.assertEqual(self.clauses(runs), {f"O{k}": True for k in range(1, 8)})

    def test_over_nothing(self):
        runs = {t: fake(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) for t in C.L_RUNS}
        self.assertEqual(self.clauses(runs), {f"O{k}": False for k in range(1, 8)})

    def test_a_replay_that_takes_points_away_gives_nothing_back(self):
        runs = {t: fake(10, 5, 10, 5, 3, 6, 8, 4, 4, -5, 10, 5) for t in C.L_RUNS}
        self.assertFalse(self.clauses(runs)["O6"])

    def test_n_runs_are_not_read(self):
        runs = {t: fake(10, 5, 10, 5, 3, 6, 8, 4, 4, 5, 10, 5) for t in C.L_RUNS}
        runs["n_r1"] = fake(100, 0, 100, 0, 0, 60, 80, 0, 0, 0, 100, 0)
        self.assertEqual(self.clauses(runs), {f"O{k}": True for k in range(1, 8)})


class TestAddedAfterTheFirstRun(unittest.TestCase):

    def test_the_rule_that_erred_and_the_takers_own_edges(self):
        rec = record(erred={2: ("Q", ON), 3: ("Q", ON), 4: ("S", SEC)})
        rows = RUN["takers"][ON]["takers"]
        action = {r["rule_id"]: r["action"] for r in rec["rules"]}
        got = C.erred_and_edges(rec, rows, ON, action)
        by = {t["rule_id"]: t for t in got["takers"]}
        self.assertEqual(by["C"]["erred"], {"rule_id": "Q", "action": ON})
        self.assertEqual(by["Y"]["erred"], {"rule_id": None, "action": None})
        # X declared its win over Q; Y its loss to Q, refused. Y's win over X is
        # not against the queue.
        self.assertEqual(by["X"]["edges"][C.OWN], {C.WINS: {EDGE_OK: 1}, C.LOSSES: {}})
        self.assertEqual(by["Y"]["edges"][C.OWN], {C.WINS: {}, C.LOSSES: {EDGE_CYCLE: 1}})
        self.assertEqual(by["Y"]["edges"][C.LATER], {C.WINS: {}, C.LOSSES: {}})
        self.assertEqual(got["taken_by_the_erred_queue"],
                         {ON: by["C"]["taken"] + by["A"]["taken"], SEC: by["X"]["taken"],
                          "None": by["Y"]["taken"]})

    def test_a_later_rule_of_the_queue(self):
        births = BIRTHS + [(IMP, "H05", ON, r_("P", 6, ON, [SEV1, c_("off_hours", "eq", True)]))]
        rec = record(births=births, edges=EDGES + [(6, "P", "C"), (6, "Y", "P", EDGE_CYCLE)])
        rows = [{"rule_id": "C", "born_at": 2, "action": T3, "cause": ERR, "taken": 10},
                {"rule_id": "Y", "born_at": 5, "action": T2, "cause": CON, "taken": 5}]
        action = {r["rule_id"]: r["action"] for r in rec["rules"]}
        got = {t["rule_id"]: t for t in C.erred_and_edges(rec, rows, ON, action)["takers"]}
        self.assertEqual(got["C"]["edges"][C.LATER], {C.WINS: {}, C.LOSSES: {EDGE_OK: 1}})
        self.assertEqual(got["Y"]["edges"][C.LATER], {C.WINS: {EDGE_CYCLE: 1}, C.LOSSES: {}})
        self.assertEqual(got["Y"]["edges"][C.OWN], {C.WINS: {}, C.LOSSES: {EDGE_CYCLE: 1}})

    def test_the_run_carries_it(self):
        self.assertEqual(set(RUN["added_after_the_first_run"]), set(C.QUEUES))
        self.assertEqual(len(RUN["added_after_the_first_run"][ON]["takers"]),
                         len(RUN["takers"][ON]["takers"]))


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(C, "read_all", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                C.main([])
        self.assertIn("unsigned", str(got.exception))

    def test_the_hand_built_run_is_not_mutated_by_a_read(self):
        before = copy.deepcopy(REC)
        read(REC)
        self.assertEqual(REC, before)


if __name__ == "__main__":
    unittest.main()
