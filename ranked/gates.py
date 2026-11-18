"""
`RK-g1` to `RK-g4` of `PLAN_RANKED.md` §7: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They are written and run before the signature, so
that a failure becomes a fix to the draft rather than a signed amendment. One
did: the first draft's engine failed the check on the transcriber, and §2.2 of
the plan says what replaced it.

  RK-g1  The arms are what they claim. The suite is green, and
         `PLAN_CORRECTIONS.md`'s own blocking checks pass. On each of that
         plan's three L runs, served its answers by `channel.gates.Replay`:
           * arm `l` gives back the run: its rules, its edges and every case's
             outcome and cause, with a label handed at each reported error and
             nowhere else;
           * arm `k`'s engine with rung 2's decision put back gives back the
             same record, and the same messages at every call. So the arms
             differ in the decision alone;
           * that engine's ranking after every birth is the one
             `results_corrections/online.json` keeps, and its votes at the end
             are `declared.json`'s;
           * on the run's final base, arm `k`'s engine decides every corpus
             case as rung 2's does, but where rung 2's returns CONFLICT. There
             it decides by its ranking, as `ranked/reading.py` reads the base
             over the space.
         And arm `k`'s engine overrides `decide`, and nothing else rung 2's
         engine defines.
  RK-g2  The texts, the requests and the declared figures. Both arms send
         `PLAN_CORRECTIONS.md`'s arm L's texts, by digest, and its request with
         the pin. The at-once asks send that plan's texts and request. §0's
         figures 2 to 7 come back.
  RK-g3  The schedule and the instruments. Six runs, the arms alternating from
         the arm `ORDER_SEED` draws; the smoke runs; coverage 1/2; the cap 400;
         §2.6's constants; a session after every run; the ask pool imported by
         the at-once asker alone. **Step 0**: under the transcriber and each
         draw, arm `k`'s engine gives back, case for case, the record rung 2's
         engine gives, and its ranking decides no case. Each competitor's
         ceiling, as `CR-g3` reads it.
  RK-g4  The signature (`ranked/plan.py`). It does not block a dry run, which
         writes nothing; it blocks every write.

**No float decides a check.** Counts are compared as integers, shares as
fractions and digests as strings.

**One did, until 2026-11-18, and it was the wall clock's.** Step 0 compared two
records whole, and a record keeps the seconds each call took, rounded to
hundredths. `RK-g1`'s replays are timed by a clock that reads 0. Step 0's loop
was not, and neither was the reference it is set against, which
`placement/references.py` builds.

- **What happened.** On 2026-11-18, after both smoke runs, Step 0 refused the
  at-once smoke session twice, before any spend.
- **What parted the records.** Followed again with the difference printed, that
  launch's path parted them in one field of 40,606: the seconds of one call of
  the transcriber, 0.03 under arm `k`'s engine and 0.0 in the reference. Every
  rule, citation, edge and case was the same, and the ranking decided no case.
- **Why every time.** The path refused each of the four times it was followed,
  at the same call both times its difference was printed. It passed once its
  allocations were perturbed. The pause is the size of that process's
  collections of the oldest generation, which fall where a path's own
  allocations put them. That is an inference: no collection was seen inside
  the call.
- **What changed.** Step 0 compares the two records without their calls'
  seconds (`without_the_clock`), and whole otherwise. `tests/test_ranked.py`
  pins that it leaves out nothing else.

**This module is offline.** It reads the corpus labels, and the policy through
the manual's level-3 text and the instruments' own gates, modules already
allowed to carry it. It sends nothing. What a dry run prints is pass or fail,
and figures §0 or a published record already states.
"""

from __future__ import annotations

import ast
import json
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from harness.domain import ACTIONS

from blind import rows as brows
from channel import gates as ch_gates
from corrections import declared as DC
from corrections import gates as cr_gates
from corrections import online as cr_online
from corrections import plan as cr_plan
from corrections import prompts as cr_prompts
from corrections import protocol as cr_protocol
from manual import instrument as MI
from placement import gates as pl_gates
from placement import loop as pl_loop
from placement import protocol as pl_protocol
from placement import references as pl_refs
from queue_alone import rules as qrules
from reasoned_loop import protocol as p
from reasoned_loop import references as rl_refs
from reuse.gates import run_suite
from rung2.engine2 import PriorityEngine

from . import engine as E
from . import loop, plan
from . import reading as R
from . import setaside as SA

as_json = pl_gates.as_json
replay_is_the_run = ch_gates.replay_is_the_run
PACKAGE = Path(__file__).resolve().parent
L_TAGS = tuple(f"l_r{k}" for k in range(1, cr_plan.REPS + 1))


@dataclass
class Checks:
    g1: dict
    g2: dict
    g3: dict
    g4: dict

    @property
    def blocking_pass(self) -> bool:
        return self.g1["passes"] and self.g2["passes"] and self.g3["passes"]

    def summary(self) -> dict[str, Any]:
        """What a record carries about the checks it was written behind."""
        return {"RK-g1": self.g1, "RK-g2": self.g2, "RK-g3": self.g3, "RK-g4": self.g4}


def closed(rep: int) -> dict[str, Any]:
    """`PLAN_CORRECTIONS.md`'s L run `rep`, as `main` holds it."""
    return json.loads(cr_plan.run_path(cr_plan.LABELLED, rep).read_text())


# ---------------------------------------------------------------------------
# RK-g1
# ---------------------------------------------------------------------------

class PutBack(E.RankedEngine):
    """Arm `k`'s engine with rung 2's decision put back, so that a replay of an
    L run follows the run: only for `RK-g1`."""

    def decide(self, case):
        return PriorityEngine.decide(self, case)


def replayed(proposer, arm: str, draws, engine: PriorityEngine) -> dict[str, Any]:
    """This plan's loop of `arm` over the corpus with `draws`, on `engine`, timed
    by a clock that reads 0."""
    res = loop.run_loop(list(MI.corpus()), plan.labels(), engine, proposer, arm, draws,
                        clock=lambda: 0.0)
    return as_json(loop.record_of(res, engine))


def same_run(ours: dict[str, Any], paid: dict[str, Any]) -> bool:
    """The replay gave back the paid run: its rules with their citations, its
    edge log, and every case's outcome, winner, queue and cause."""
    def cases(rec):
        return [(r["idx"], r["outcome"], r["winner_id"], r["predicted"], r["cause"],
                 r["reported"]) for r in rec["records"]]
    theirs = as_json(paid)
    return (replay_is_the_run(ours, paid) and ours["rules"] == theirs["rules"]
            and ours["edge_log"] == theirs["edge_log"] and cases(ours) == cases(theirs))


def decides_as_claimed(engine: E.RankedEngine) -> dict[str, Any]:
    """On a base, arm `k`'s own decision at every corpus case: rung 2's, but at a
    CONFLICT, where it is the first queue of its ranking among the undefeated
    rules', as the reading over the space takes it."""
    space = engine.space
    action = {r.rule_id: r.action for r in engine.rules}
    queues = R.by_queue(brows.undefeated_masks(engine), action)
    ranking = engine.ranking
    same = at_conflicts = as_read = True
    conflicts = 0
    for case in MI.corpus():
        o2, w2, inv2 = PriorityEngine.decide(engine, case)
        ok, wk, _ = E.RankedEngine.decide(engine, case)
        here = R.point_of(case, space)
        present = [q for q in ranking if queues[q] & here]
        if o2 == "CONFLICT":
            conflicts += 1
            at_conflicts &= (ok == "ACTION" and wk in inv2
                             and wk.action == E.pick(inv2, ranking).action)
        else:
            same &= (ok, wk) == (o2, w2)
        as_read &= (wk.action if wk else None) == (present[0] if present else None)
    return {"conflicts": conflicts, "as_rung_2_elsewhere": same,
            "by_the_ranking_at_conflicts": at_conflicts, "as_the_space_is_read": as_read}


def replays(rep: int, online: dict[str, Any], declared: dict[str, Any]) -> dict[str, Any]:
    """§7, on `PLAN_CORRECTIONS.md`'s run L r`rep`."""
    paid = closed(rep)
    tag = L_TAGS[rep - 1]
    draws = plan.draws(plan.stream(plan.CONTROL, rep))
    labels = plan.labels()
    space = MI.space()
    l, k = (cr_gates.capture(paid, cr_protocol.SYSTEM_PROMPT) for _ in range(2))
    rec_l = replayed(l, plan.CONTROL, draws, loop.engine_for(plan.CONTROL, space))
    put_back = PutBack(space=space)
    rec_k = replayed(k, plan.RANKED, draws, put_back)
    errors = {esc["idx"] for esc in paid["escalations"] if esc["kind"] == plan.ERROR}
    log = [(x["rule_id"], x["ranking"], x["tied"]) for x in put_back.ranking_log]
    kept = [(x["rule_id"], x["ranking"], x["tied"]) for x in online["runs"][tag]["curve"]]
    out = {"calls": len(l.sent), "reported_errors": len(errors),
           "placement_calls": sum(1 for x in l.sent if x[1] == 1),
           "l_is_the_run": same_run(rec_l, paid),
           "reports_where_reported": set(l.reports) == errors == set(k.reports),
           "reports_are_the_labels": all(q == labels[i][0] for i, q in l.reports.items()),
           "k_put_back_is_l": rec_k == rec_l,
           "k_sends_what_l_sends": as_json(k.sent) == as_json(l.sent),
           "ranking_is_the_replays": log == kept,
           "votes_are_the_records": (put_back.final()["votes"]
                                     == declared["runs"][tag]["votes"]["all"]),
           "decides": decides_as_claimed(put_back)}
    out["passes"] = (out["calls"] > 0 and out["reported_errors"] > 0
                     and out["placement_calls"] > 0 and out["decides"]["conflicts"] > 0
                     and all(v for v in out.values() if isinstance(v, bool))
                     and all(v for v in out["decides"].values() if isinstance(v, bool)))
    return out


def decide_alone() -> bool:
    """Arm `k`'s engine overrides `decide`, and nothing else rung 2's defines."""
    theirs = {n for n, v in vars(PriorityEngine).items() if callable(v) and not n.startswith("__")}
    mine = {n for n in theirs if n in vars(E.RankedEngine)}
    return mine == {"decide"}


def corrections_own_checks() -> dict[str, Any]:
    """`CR-g1` to `CR-g3`, called, without the suite this module runs once."""
    got = cr_gates.run_checks(suite=False)
    return {"CR-g1": got.g1["passes"], "CR-g2": got.g2["passes"], "CR-g3": got.g3["passes"],
            "instruments": got.g3["instruments"]["passes"], "passes": got.blocking_pass}


def gate_g1(own: dict[str, Any], suite: bool = True) -> dict[str, Any]:
    online = json.loads(cr_online.record_path().read_text())
    declared = json.loads(DC.record_path().read_text())
    reps = {tag: replays(rep, online, declared) for rep, tag in enumerate(L_TAGS, start=1)}
    alone = decide_alone()
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": "PLAN_CORRECTIONS.md's own blocking checks pass; on its three L runs' "
                    "answers arm l gives back the run, arm k with rung 2's decision put back "
                    "gives back the same record and messages, its ranking is the replay's at "
                    "every birth and its votes the record's, and its own decision is rung 2's "
                    "but at a CONFLICT, where the ranking decides; it overrides decide alone; "
                    "the suite green",
            "corrections_checks": own, "replays": reps, "decide_alone": alone, "suite": tests,
            "passes": (own["passes"] and alone and all(r["passes"] for r in reps.values())
                       and tests["passes"] is not False)}


# ---------------------------------------------------------------------------
# RK-g2
# ---------------------------------------------------------------------------

def texts() -> dict[str, Any]:
    from . import run as rrun      # the headers; run.py imports this module

    sent, v1c = cr_protocol.digests(plan.TEXTS_OF), p.digests()
    heads = {a: rrun.protocol_header(a, plan.N, plan.tag(a, 1), 1) for a in plan.ARMS}
    once = cr_prompts.digests()
    out = {"keys": sorted(sent) == ["blind_base", "placement_template", "report",
                                    "retry_message", "system_prompt"],
           "system_prompt_level_1": sent["system_prompt"] == cr_plan.SYSTEM_PROMPT_SHA16,
           "report_r1": sent["report"] == cr_plan.REPORT_SHA16,
           "three_are_v1cs": all(sent[k] == v1c[k] for k in ("blind_base",
                                                             "placement_template",
                                                             "retry_message")),
           "both_arms_the_same_texts": (heads["l"]["texts_sha16"] == heads["k"]["texts_sha16"]
                                        == sent and heads["l"]["fingerprint"]
                                        == heads["k"]["fingerprint"]
                                        == cr_protocol.fingerprint(plan.TEXTS_OF)),
           "the_arms_differ_by_the_engine": ({k for k in heads["l"] if heads["l"][k] != heads["k"][k]}
                                            == {"arm", "run", "engine", "engine_rule"}),
           "at_once_system_prompt": once["system_prompt"] == cr_plan.COMPILE_PROMPT_SHA16,
           "at_once_header": once["header"] == cr_plan.AT_ONCE_HEADER_SHA16}
    out["passes"] = all(out.values())
    return out


def requests() -> dict[str, Any]:
    """§2.12 and §2.6: both arms send `PLAN_CORRECTIONS.md`'s request with its
    pin; the at-once asks send it with their budget."""
    msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}]
    out: dict[str, Any] = {}
    for attempt in (0, 1):
        theirs = pl_protocol.request_with(cr_plan.PROVIDER, cr_plan.MODEL, cr_plan.LABELLED,
                                          msgs, attempt)
        ours = [pl_protocol.request_with(plan.PROVIDER, plan.MODEL, arm, msgs, attempt)
                for arm in plan.ARMS]
        once = cr_prompts.request(plan.PROVIDER, plan.MODEL, "at once", msgs, attempt)
        out[f"both_arms_corrections_{attempt}"] = ours[0] == ours[1] == theirs
        out[f"at_once_but_for_the_budget_{attempt}"] = (
            {**once, "max_tokens": None} == {**theirs, "max_tokens": None}
            and once["max_tokens"] == plan.AT_ONCE_MAX_TOKENS == 2 * plan.MAX_TOKENS)
    out["pin"] = (plan.PROVIDER == cr_plan.PROVIDER
                  == {"order": ["deepinfra/fp8"], "allow_fallbacks": False}
                  and plan.PROVIDER_NAME == "DeepInfra")
    return {**out, "passes": all(out.values())}


def transcriber_under(engine: PriorityEngine, rep: int, clock=time.monotonic):
    """The transcriber through `PLAN_PLACEMENT.md`'s loop under v1c, on `engine`,
    with run `rep`'s draws, timed by `clock`: the wall clock's, as that plan's
    own reference is."""
    return pl_loop.run_loop(list(MI.corpus()), plan.labels(), engine,
                            rl_refs.Transcriber(engine), plan.COVERAGE,
                            plan.draws(plan.stream(plan.RANKED, rep)),
                            propose=pl_protocol.propose_v1c, clock=clock)


def without_the_clock(record: dict[str, Any]) -> dict[str, Any]:
    """A loop's record without the seconds of its calls: readings of the wall
    clock, and nothing an engine gives. Two loops timed by the wall clock agree
    on them only while every call rounds to no hundredth of a second, and one
    slow call parts two records that agree on everything else. Nothing else is
    left out, and `record` is not changed."""
    rec = as_json(record)
    for esc in rec["escalations"]:
        for call in esc["calls"]:
            call.pop("seconds", None)
    return rec


def set_aside_reading() -> dict[str, Any]:
    """§0's figure 2: the two designs set aside, and rung 2's engine, under the
    transcriber and each draw."""
    space, truth = MI.space(), MI.space_truth()
    out: dict[str, Any] = {}
    for count in (SA.EVERY, SA.DISTINCT):
        right, esc, last = [], [], []
        for rep in range(1, plan.REPS + 1):
            total = SA.Total(space=space, count=count)
            res = transcriber_under(total, rep)
            right.append(SA.right_of(total, truth))
            esc.append(len(res.loop.escalations))
            last.append(total.tally.ranking[-1])
        out[count] = {"right": right, "escalations": esc, "last": last}
    refs = [pl_refs.transcriber("v1c", rep)["figures"] for rep in range(1, plan.REPS + 1)]
    out["rung 2"] = {"right": [f["space_right"] for f in refs],
                     "escalations": [f["escalations"] for f in refs]}
    return out


def first_call_right(record: dict[str, Any]) -> int:
    """Of a record's CONFLICT escalations, those whose first call named the
    case's true queue."""
    truth = {r["idx"]: r["truth"] for r in record["records"]}
    n = 0
    for esc in record["escalations"]:
        if esc["kind"] != plan.CONFLICT:
            continue
        payload = ((esc.get("calls") or [None])[0] or {}).get("payload")
        n += isinstance(payload, dict) and payload.get("action") == truth[esc["idx"]]
    return n


def closed_runs_reading() -> dict[str, Any]:
    """§0's figures 3 to 5, off `PLAN_CORRECTIONS.md`'s three L runs."""
    space, truth = MI.space(), MI.space_truth()
    corpus = list(MI.corpus())
    finals: dict[str, list] = {"as recorded": [], SA.EVERY: [], SA.DISTINCT: [],
                               "arm K's engine": []}
    went: dict[str, list] = {"peak": [], "peak_birth": [], plan.SECURITY: [], plan.ONCALL: []}
    asked: dict[str, list] = {"cases": [], "ranking_right": [], "first_call_right": []}
    sound = True
    for rep in range(1, cr_plan.REPS + 1):
        rec = closed(rep)
        got = R.as_it_went(rec, space, truth)
        sound &= got["sound"]
        curve = got["curve"]
        finals["as recorded"].append(curve[-1]["rung2"])
        finals["arm K's engine"].append(curve[-1]["ranked"])
        for count in (SA.EVERY, SA.DISTINCT):
            finals[count].append(SA.right_of(SA.fed(rec, space, count), truth))
        top = R.summary(curve, "ranked")
        went["peak"].append(top["peak"])
        went["peak_birth"].append(top["peak_birth"])
        recall = R.recall_of(got["final"]["ranked"], truth)
        for q in (plan.SECURITY, plan.ONCALL):
            went[q].append(str(Fraction(*recall[q])))
        cases = list(R.asked_conflicts(rec, corpus, space))
        asked["cases"].append(len(cases))
        asked["ranking_right"].append(sum(1 for c in cases if c["decided"] == c["truth"]))
        asked["first_call_right"].append(first_call_right(rec))
    return {"final_bases": finals, "as_it_went": went, "asked_conflicts": asked,
            "sound": sound}


def pair_arrivals() -> dict[str, list]:
    """§0's figure 6, on the corpus: the arrivals at which the policy's own rules
    exercise `T3_ENGINEERING` and `ACCOUNT_MANAGER` against each other. The
    policy is read off the manual's level-3 text, which is the policy at every
    point (`PLAN_REASONED_RULE.md`'s first check)."""
    cases = list(MI.corpus())
    draws = [plan.draws(f"r{k}") for k in range(1, plan.REPS + 1)]

    def count(governing: set[str], also: set[str]) -> list:
        hit = []
        for i, c in enumerate(cases):
            ids = [r.id for r in qrules.matching(c.as_dict())]
            if ids and ids[0] in governing and also & set(ids[1:]):
                hit.append(i)
        return [len(hit), [sum(1 for i in hit if plan.reportable(plan.COVERAGE, d[i]))
                           for d in draws]]

    return {"churn_that_t3_routing_matches": count({"H13", "H14"}, {"H15", "H17"}),
            "severity_1_t3_that_churn_matches": count({"H06", "H07"}, {"H13", "H14"})}


def drafting_reading() -> dict[str, Any]:
    """§0's figures 2 to 7, recomputed."""
    got = closed_runs_reading()
    return {"set_aside": set_aside_reading(), "final_bases": got["final_bases"],
            "as_it_went": got["as_it_went"], "asked_conflicts": got["asked_conflicts"],
            "pair_arrivals": pair_arrivals(),
            "schedule": [list(x) for x in plan.schedule()], "sound": got["sound"]}


def drafting(got: dict[str, Any] | None = None) -> dict[str, Any]:
    got = got or drafting_reading()
    declared = {k: got[k] == plan.DECLARED[k] for k in plan.DECLARED}
    return {"as_declared": declared, "sound": got["sound"],
            "passes": got["sound"] and all(declared.values())}


def gate_g2(reading: dict[str, Any] | None = None) -> dict[str, Any]:
    tx, rq, dr = texts(), requests(), drafting(reading)
    return {"what": "both arms send PLAN_CORRECTIONS.md's arm L's texts, by digest, and its "
                    "request with the pin, and differ in their headers by the engine alone; "
                    "the at-once asks send that plan's texts and request with their budget; "
                    "§0's figures 2 to 7 come back",
            "texts": tx, "requests": rq, "drafting": dr,
            "passes": all(x["passes"] for x in (tx, rq, dr))}


# ---------------------------------------------------------------------------
# RK-g3
# ---------------------------------------------------------------------------

def imports_of(path: Path) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(), filename=str(path))):
        if isinstance(node, ast.Import):
            for a in node.names:
                names.update(a.name.split("."))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.update(node.module.split("."))
            for a in node.names:
                names.add(a.name)
    return names


def the_pool_is_for_asks() -> bool:
    users = sorted(f.name for f in PACKAGE.glob("*.py") if "ask_pool" in imports_of(f))
    return users == ["ask.py"]


def step_zero_at(rep: int, space, clock=time.monotonic) -> dict[str, Any]:
    """Step 0 under run `rep`'s draws, with arm `k`'s loop timed by `clock`.

    The reference is `PLAN_PLACEMENT.md`'s own, which its module built and timed
    by the wall clock, and that package is called and not edited. So the two
    records are compared without their calls' seconds, and whole otherwise."""
    engine = E.RankedEngine(space=space, keep_log=True)
    res = transcriber_under(engine, rep, clock)
    ref = pl_refs.transcriber("v1c", rep)
    taken = sum(1 for c in engine.case_log if c["by"] == E.RANKING)
    return {"record_is_rung_2s": (without_the_clock(pl_loop.record_of(res, engine))
                                  == without_the_clock(ref["record"])),
            "decided_by_the_ranking": taken,
            "space_right": MI.over_space(engine)["correct"]}


def step_zero() -> dict[str, Any]:
    """Step 0, as `EXTERNAL_REVIEW.md` §1.1 makes it a method: under a proposer
    that never errs, arm `k`'s engine gives back the record rung 2's engine
    gives, case for case, and its ranking decides nothing."""
    space = MI.space()
    out: dict[str, Any] = {f"r{rep}": step_zero_at(rep, space)
                           for rep in range(1, plan.REPS + 1)}
    out["passes"] = all(v["record_is_rung_2s"] and v["decided_by_the_ranking"] == 0
                        for v in out.values())
    return out


def gate_g3(own: dict[str, Any]) -> dict[str, Any]:
    order = plan.schedule()
    arms = [a for a, _ in order]
    fresh = E.RankedEngine(space=MI.space())
    out = {"schedule": [list(x) for x in order],
           "as_declared": [list(x) for x in order] == plan.DECLARED["schedule"],
           "six_runs_three_an_arm": (len(order) == len(set(order)) == 2 * plan.REPS
                                     and all(arms.count(a) == plan.REPS for a in plan.ARMS)),
           "the_arms_alternate": all(a != b for a, b in zip(arms, arms[1:])),
           "each_repetition_in_order": [r for _, r in order] == sorted(r for _, r in order),
           "smoke": (plan.SMOKE_N == 30 and plan.SMOKE_ARMS == ("l", "k")
                     and all(plan.stream(a, None) == "smoke" for a in plan.SMOKE_ARMS)),
           "coverage": plan.COVERAGE == Fraction(1, 2) == cr_plan.COVERAGE,
           "cap": plan.MAX_ESCALATIONS == cr_plan.MAX_ESCALATIONS == 400,
           "draws_are_corrections": all(plan.channel_of(a, r)
                                        == cr_plan.channel_of(cr_plan.LABELLED, r)
                                        for a, r in order),
           "at_once": ((plan.CHECKPOINTS, plan.ASKS_PER_CHECKPOINT, plan.PRIOR_ASKS,
                        plan.SMOKE_ASKS, plan.WORKERS, plan.MAX_REASKS,
                        plan.AT_ONCE_MAX_TOKENS)
                       == ((10, 20, 40, 80, 160, 320), 3, 5, 2, 4, 2, 32000)),
           "a_session_after_every_run": (plan.sessions() == ("smoke", "prior", *(
               plan.tag(a, r) for a, r in order))),
           "the_pool_is_for_asks": the_pool_is_for_asks(),
           "before_any_vote_the_domains_order": (fresh.ranking == tuple(ACTIONS)
                                                 == E.rankings()[0]
                                                 and len(E.rankings()) == plan.N_RANKINGS)}
    zero = step_zero()
    out["step_zero"] = zero
    out["competitors_ceilings"] = own["instruments"]
    out["passes"] = (all(v for k, v in out.items() if k not in ("schedule", "step_zero"))
                     and zero["passes"])
    return {"what": "six runs alternating from the arm the seed draws; the smoke runs 30 cases "
                    "an arm on PLAN_CHANNEL.md's smoke draws; coverage 1/2; the cap 400; "
                    "§2.6's constants and a session after every run; the ask pool for the "
                    "asks alone; Step 0: under the transcriber and each draw, arm k's engine "
                    "gives back rung 2's record and its ranking decides nothing; each "
                    "competitor's ceiling", **out}


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

def run_checks(suite: bool = True) -> Checks:
    own = corrections_own_checks()
    return Checks(g1=gate_g1(own, suite=suite), g2=gate_g2(), g3=gate_g3(own),
                  g4=plan.gate_signature())


def report(checks: Checks) -> None:
    def mark(g: dict) -> str:
        return "PASS" if g["passes"] else "FAIL"

    g1, g2, g3, g4 = checks.g1, checks.g2, checks.g3, checks.g4
    s, reps = g1["suite"], g1["replays"]
    print(f"\nRK-g1 {mark(g1)}  PLAN_CORRECTIONS.md's CR-g1 to CR-g3 "
          f"{g1['corrections_checks']['passes']}; on its L runs, arm l is the run "
          f"{all(r['l_is_the_run'] for r in reps.values())}, arm k with rung 2's decision "
          f"put back is arm l {all(r['k_put_back_is_l'] and r['k_sends_what_l_sends'] for r in reps.values())}, "
          f"its ranking is the replay's {all(r['ranking_is_the_replays'] for r in reps.values())}, "
          f"its own decision is rung 2's but at "
          f"{sum(r['decides']['conflicts'] for r in reps.values())} conflicts "
          f"{all(all(v for v in r['decides'].values() if isinstance(v, bool)) for r in reps.values())}; "
          f"it overrides decide alone {g1['decide_alone']}")
    print(f"      suite {'not run' if not s.get('ran') else s.get('result')}")
    print(f"RK-g2 {mark(g2)}  texts {g2['texts']['passes']}; requests "
          f"{g2['requests']['passes']}; figures 2 to 7 {g2['drafting']['passes']}")
    print(f"RK-g3 {mark(g3)}  the schedule {g3['schedule']}; Step 0 under the transcriber "
          f"{g3['step_zero']['passes']}; the competitors' ceilings "
          f"{g3['competitors_ceilings']}")
    print(f"RK-g4 {'SIGNED' if g4['passes'] else 'UNSIGNED'}  {g4['found']} signature "
          f"line(s), {g4['unsigned']} blank")
    print(f"\nblocking checks: {'PASS' if checks.blocking_pass else 'FAIL'}")
