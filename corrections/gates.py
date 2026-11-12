"""
`CR-g1` to `CR-g4` of `PLAN_CORRECTIONS.md` §7: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They are written and run before the signature, so
that a failure becomes a fix to the draft rather than a signed amendment.

  CR-g1  The arms are what they claim. The suite is green, and
         `PLAN_PLACEMENT.md`'s own blocking checks pass: its loop, its list,
         its texts, its requests, its draws and its labels. On each of that
         plan's three v1c runs, served its answers by `channel.gates.Replay`:
           * arm `n`'s proposer with level 3's system prompt is v1c: the loop
             gives back the run's record, and every call's messages are v1c's,
             byte for byte;
           * arm `l`'s, the same, gives back the same record. Its messages are
             `n`'s at every call but those of an escalation caused by a
             reported error. There they carry the report, naming that case's
             corpus label, right after v2b's paragraph, and nothing else
             changes. The cases handed a report are exactly those
             escalations;
           * at level 1 the messages are the same but for the system prompt.
  CR-g2  The texts and the requests. Arm `n` sends level 1's system prompt and
         v1c's other three texts, by digest. Arm `l` sends the same and §2.1's
         R1, quoted in §5.2 of the plan byte for byte, which names no rule and
         one queue, the reported ticket's. The at-once asks send level 1's
         compile prompt and §2.4's header, quoted in §5.3, and with no label
         `PLAN_MANUAL.md`'s level-1 compile messages exactly. Both arms send
         `PLAN_PLACEMENT.md`'s request with its pin. The at-once asks send the
         same with their budget, read without building a client. §0's figures
         1 to 3 come back from the records.
  CR-g3  The schedule and the instruments. Six runs, the arms alternating
         from the arm `ORDER_SEED` draws; the smoke runs 30 cases an arm on
         `PLAN_CHANNEL.md`'s smoke draws; coverage 1/2; the cap 400; §2.4's
         constants. `harness/ask_pool.py` is imported by the at-once asker and
         by no other module of the package. Each competitor's ceiling,
         `EXTERNAL_REVIEW.md` §1.1's *Step 0*:
           * the inducer's `I-g1`;
           * the tree handed the whole space, `PLAN_STUDENTS.md`'s `T-g2`;
           * the 29 hidden rules installed as an at-once answer, by
             `PLAN_MANUAL.md`'s installer, deciding the space whole.
  CR-g4  The signature (`corrections/plan.py`). It does not block a dry run,
         which writes nothing; it blocks every write.

**No float decides a check.** Counts are compared as integers and digests as
strings.

**This module is offline.** It reads the corpus labels to check the label's
route, and the policy through the instruments' own gates, modules already
allowed to carry it. It sends nothing, and what a dry run prints is pass or
fail, and figures §0 or a published record already states.
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from harness.domain import ACTIONS

from channel import gates as ch_gates
from ilp import induce_check
from manual import gates as m_gates
from manual import instrument as MI
from manual import prompts as mprompts
from placement import gates as pl_gates
from placement import plan as pl_plan
from placement import protocol as pl_protocol
from placement import run as pl_run
from reasoned_loop import protocol as p
from reuse.gates import run_suite
from rung2.engine2 import PriorityEngine
from students import gates as st_gates
from whole import plan as wr_plan

from . import loop, plan, prompts, protocol

as_json = pl_gates.as_json
Replay = ch_gates.Replay
replay_is_the_run = ch_gates.replay_is_the_run
PACKAGE = Path(__file__).resolve().parent


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
        return {"CR-g1": self.g1, "CR-g2": self.g2, "CR-g3": self.g3, "CR-g4": self.g4}


# ---------------------------------------------------------------------------
# CR-g1
# ---------------------------------------------------------------------------

def placements_own_checks() -> dict[str, Any]:
    """`PL-g1` to `PL-g3`, called, without the suite this module runs once."""
    got = pl_gates.run_checks(suite=False)
    return {"PL-g1": got.g1["passes"], "PL-g2": got.g2["passes"], "PL-g3": got.g3["passes"],
            "draws": got.g1["draws"]["passes"], "labels": got.g1["labels"]["passes"],
            "passes": got.blocking_pass}


def v1c_capture(paid: dict[str, Any]):
    """v1c's own proposer class, whose `answer` keeps the messages and serves
    the paid answer instead of asking."""
    replay = Replay(paid)

    class Capture(pl_run.Stamped):
        name = "replay"

        def __init__(self) -> None:
            self.sent: list[list[Any]] = []

        def answer(self, idx: int, round_: int, messages) -> p.Answer:
            self.sent.append([idx, round_, messages])
            return replay.answer(idx, round_)

    return Capture()


def capture(paid: dict[str, Any], system: str):
    """This plan's proposer with `system` as its system prompt, keeping what
    each call was built from and sent, and serving the paid answers."""
    replay = Replay(paid)

    class Capture(protocol.Reporting):
        name = "replay"

        def __init__(self) -> None:
            self.sent: list[list[Any]] = []
            self.inputs: list[tuple] = []
            self.reports: dict[int, str] = {}
            self.system = system

        def first(self, case, idx: int) -> p.Answer:
            self.inputs.append((idx, 0, case, None, "", self.reports.get(idx)))
            return super().first(case, idx)

        def placement(self, case, draft, message: str, idx: int,
                      listed: list[str] | None = None) -> p.Answer:
            self.inputs.append((idx, 1, case, draft, message, self.reports.get(idx)))
            return super().placement(case, draft, message, idx, listed)

        def answer(self, idx: int, round_: int, messages) -> p.Answer:
            self.sent.append([idx, round_, messages])
            return replay.answer(idx, round_)

    return Capture()


def replayed(proposer, arm: str, draws) -> dict[str, Any]:
    """This plan's loop of `arm` over the corpus with `draws`, a fresh engine
    and `proposer`, timed by a clock that reads 0."""
    engine = PriorityEngine(space=MI.space())
    res = loop.run_loop(list(MI.corpus()), plan.labels(), engine, proposer, arm, draws,
                        clock=lambda: 0.0)
    return as_json(loop.record_of(res, engine))


def replays(rep: int) -> dict[str, Any]:
    """§7: on `PLAN_PLACEMENT.md`'s run `v1c r<rep>`, this plan's two arms at
    level 3 are v1c, and arm `l` differs by the report alone, where a reported
    error escalated, and at level 1 by the system prompt alone."""
    paid = json.loads(pl_plan.run_path("v1c", rep).read_text())
    draws = plan.draws(plan.stream("n", rep))
    labels = plan.labels()
    c, n3, l3 = v1c_capture(paid), capture(paid, p.SYSTEM_PROMPT), capture(paid, p.SYSTEM_PROMPT)
    rec_c = as_json(_replay_v1c(c, draws))
    rec_n, rec_l = replayed(n3, "n", draws), replayed(l3, "l", draws)
    errors = {esc["idx"] for esc in paid["escalations"] if esc["kind"] == plan.ERROR}
    reported = set(l3.reports)
    apart = (len(l3.sent) == len(n3.sent)
             and all(x[:2] == y[:2] and (protocol.one_report_apart(x[2], y[2], l3.reports[x[0]])
                                         if x[0] in l3.reports else x[2] == y[2])
                     for x, y in zip(n3.sent, l3.sent)))
    level1 = all(_only_the_system_apart(inputs, sent)
                 for inputs, sent in zip(n3.inputs, n3.sent))
    out = {"calls": len(c.sent),
           "replay_is_the_run": replay_is_the_run(rec_c, paid),
           "n_is_v1c": rec_n == rec_c and as_json(n3.sent) == as_json(c.sent),
           "l_record_is_n": rec_l == rec_n,
           "reported_errors": len(errors),
           "reports_where_reported": reported == errors,
           "reports_are_the_labels": all(q == labels[i][0] for i, q in l3.reports.items()),
           "n_handed_none": not n3.reports,
           "one_report_apart": apart,
           "level_1_differs_by_the_system_prompt": level1,
           "placement_calls": sum(1 for x in c.sent if x[1] == 1)}
    out["passes"] = (out["calls"] > 0 and out["reported_errors"] > 0
                     and out["placement_calls"] > 0
                     and all(v for k, v in out.items() if isinstance(v, bool)))
    return out


def _replay_v1c(proposer, draws) -> dict[str, Any]:
    engine = PriorityEngine(space=MI.space())
    res = loop.run_loop(list(MI.corpus()), plan.labels(), engine, proposer, "n", draws,
                        clock=lambda: 0.0)
    return loop.record_of(res, engine)


def _only_the_system_apart(inputs: tuple, sent: list) -> bool:
    """A call rebuilt with level 1's system prompt differs from the one sent at
    level 3 by its first message alone."""
    _idx, _round, case, draft, message, queue = inputs
    at1 = protocol.messages_for(case, draft, message, queue=queue,
                                system=protocol.SYSTEM_PROMPT)
    at3 = sent[2]
    return (len(at1) == len(at3) and at1[1:] == at3[1:]
            and at1[0] == {"role": "system", "content": protocol.SYSTEM_PROMPT}
            and at3[0] == {"role": "system", "content": p.SYSTEM_PROMPT})


def gate_g1(suite: bool = True) -> dict[str, Any]:
    own = placements_own_checks()
    reps = {f"v1c_r{rep}": replays(rep) for rep in range(1, pl_plan.REPS + 1)}
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": "PLAN_PLACEMENT.md's own blocking checks pass; on its three v1c runs' "
                    "answers both arms at level 3 are v1c, arm l differs by the report alone, "
                    "at the reported errors and with their labels, and level 1 by the system "
                    "prompt alone; the suite green",
            "placement_checks": own, "replays": reps, "suite": tests,
            "passes": (own["passes"] and all(r["passes"] for r in reps.values())
                       and tests["passes"] is not False)}


# ---------------------------------------------------------------------------
# CR-g2
# ---------------------------------------------------------------------------

def quoted_in_the_plan(text: str, path: Path | None = None) -> bool:
    """Whether the plan quotes `text` in a fenced block, byte for byte."""
    body = (path or plan.PLAN).read_text()
    blocks = re.findall(r"^```text\n(.*?)^```$", body, flags=re.S | re.M)
    return text in blocks


def texts() -> dict[str, Any]:
    n, l, v1c = protocol.digests("n"), protocol.digests("l"), p.digests()
    out = {"n_keys": sorted(n) == ["blind_base", "placement_template", "retry_message",
                                   "system_prompt"],
           "n_shares_three_with_v1c": all(n[k] == v1c[k] for k in ("blind_base",
                                                                   "placement_template",
                                                                   "retry_message")),
           "system_prompt_level_1": (n["system_prompt"] == plan.SYSTEM_PROMPT_SHA16
                                     and protocol.SYSTEM_PROMPT
                                     == mprompts.loop_system_prompt(1)),
           "v1c_system_prompt_level_3": v1c["system_prompt"] == plan.LEVEL3_SYSTEM_PROMPT_SHA16,
           "l_is_n_and_the_report": ({k: v for k, v in l.items() if k != "report"} == n
                                     and l["report"] == plan.REPORT_SHA16),
           "report_quoted": quoted_in_the_plan(protocol.REPORT),
           "report_names_no_rule_and_no_queue": (protocol.names_no_rule(protocol.REPORT)
                                                 and not protocol.queues_named(protocol.REPORT)),
           "report_names_its_queue": all(protocol.queues_named(protocol.report(q)) == [q]
                                         for q in ACTIONS),
           "report_ascii": protocol.REPORT.isascii() and protocol.REPORT.endswith("\n"),
           "fingerprints_differ": protocol.fingerprint("n") != protocol.fingerprint("l"),
           "at_once_system_prompt": (prompts.digests()["system_prompt"]
                                     == plan.COMPILE_PROMPT_SHA16),
           "at_once_header": prompts.digests()["header"] == plan.AT_ONCE_HEADER_SHA16,
           "header_quoted": quoted_in_the_plan(prompts.HEADER),
           "header_names_no_rule_and_no_queue": (protocol.names_no_rule(prompts.HEADER)
                                                 and not protocol.queues_named(prompts.HEADER)),
           "no_label_is_plan_manuals": prompts.messages([]) == mprompts.compile_messages(1)}
    out["passes"] = all(out.values())
    return out


def requests() -> dict[str, Any]:
    """§2.10 and §2.4: both arms send `PLAN_PLACEMENT.md`'s request with its pin;
    the at-once asks send it with their budget."""
    msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}]
    out: dict[str, Any] = {}
    for attempt in (0, 1):
        theirs = pl_protocol.request_with(pl_plan.PROVIDER, pl_plan.MODEL, "v1c", msgs, attempt)
        ours = {arm: pl_protocol.request_with(plan.PROVIDER, plan.MODEL, arm, msgs, attempt)
                for arm in plan.ARMS}
        once = prompts.request(plan.PROVIDER, plan.MODEL, "at once", msgs, attempt)
        out[f"both_arms_placements_{attempt}"] = ours["n"] == ours["l"] == theirs
        out[f"at_once_but_for_the_budget_{attempt}"] = (
            {**once, "max_tokens": None} == {**theirs, "max_tokens": None}
            and once["max_tokens"] == plan.AT_ONCE_MAX_TOKENS == 2 * plan.MAX_TOKENS)
    out["pin"] = (plan.PROVIDER == pl_plan.PROVIDER
                  == {"order": ["deepinfra/fp8"], "allow_fallbacks": False}
                  and plan.PROVIDER_NAME == "DeepInfra")
    return {**out, "passes": all(out.values())}


def drafting_reading() -> dict[str, Any]:
    """§0's figures 1 to 3, recomputed from the records `main` holds."""
    runs = {f"placement_v1c_r{k}": pl_plan.run_path("v1c", k) for k in (1, 2, 3)}
    runs.update({f"whole_v1c_r{k}": wr_plan.run_path("v1c", k) for k in (1, 2, 3)})
    first, counts = {}, {}
    for name, path in runs.items():
        rec = json.loads(path.read_text())
        truth = {r["idx"]: r["truth"] for r in rec["records"]}
        errors = [esc for esc in rec["escalations"] if esc["kind"] == plan.ERROR]
        named = 0
        for esc in errors:
            call = (esc.get("calls") or [None])[0]
            payload = (call or {}).get("payload")
            if isinstance(payload, dict) and payload.get("action") == truth[esc["idx"]]:
                named += 1
        first[name] = [named, len(errors)]
        counts[name] = [len(rec["escalations"]), len(errors), rec["calls"]]
    cases = list(MI.corpus())
    seen, repeats = set(), 0
    for c in cases:
        repeats += c.key() in seen
        seen.add(c.key())
    return {"first_calls_true_queue": first, "escalations_reports_calls": counts,
            "repeated_arrivals": repeats}


def drafting() -> dict[str, Any]:
    got = drafting_reading()
    declared = {k: got[k] == plan.DECLARED[k] for k in got}
    return {"as_declared": declared, "passes": all(declared.values())}


def gate_g2() -> dict[str, Any]:
    tx, rq, dr = texts(), requests(), drafting()
    return {"what": "arm n sends level 1's system prompt and v1c's other texts, arm l the same "
                    "and §2.1's R1, quoted in the plan; the at-once asks send level 1's compile "
                    "prompt and §2.4's header, quoted, and PLAN_MANUAL.md's messages with no "
                    "label; PLAN_PLACEMENT.md's request with its pin, the at-once asks with "
                    "their budget; §0's figures 1 to 3 come back",
            "texts": tx, "requests": rq, "drafting": dr,
            "passes": all(x["passes"] for x in (tx, rq, dr))}


# ---------------------------------------------------------------------------
# CR-g3
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


def instruments() -> dict[str, Any]:
    """Each competitor's ceiling, handed the whole truth: `EXTERNAL_REVIEW.md`
    §1.1's *Step 0*."""
    ilp = induce_check.i_g1()
    tree = st_gates.gate_tg2()
    installer = m_gates.installer_on_the_policy()
    return {"ilp_I_g1": ilp["passes"], "students_T_g2": tree["passes"],
            "at_once_installer": installer["passes"],
            "passes": ilp["passes"] and tree["passes"] and installer["passes"]}


def gate_g3() -> dict[str, Any]:
    order = plan.schedule()
    arms = [a for a, _ in order]
    out = {"schedule": [list(x) for x in order],
           "as_declared": [list(x) for x in order] == plan.DECLARED["schedule"],
           "six_runs_three_an_arm": (len(order) == len(set(order)) == 2 * plan.REPS
                                     and all(arms.count(a) == plan.REPS for a in plan.ARMS)),
           "the_arms_alternate": all(a != b for a, b in zip(arms, arms[1:])),
           "each_repetition_in_order": [r for _, r in order] == sorted(r for _, r in order),
           "smoke": (plan.SMOKE_N == 30 and plan.SMOKE_ARMS == ("n", "l")
                     and all(plan.stream(a, None) == "smoke" for a in plan.SMOKE_ARMS)),
           "coverage": plan.COVERAGE == Fraction(1, 2) == pl_plan.COVERAGE,
           "cap": plan.MAX_ESCALATIONS == pl_plan.MAX_ESCALATIONS == 400,
           "draws_are_placements": all(plan.channel_of(a, r) == pl_plan.channel_of("v1c", r)
                                       for a, r in order),
           "at_once": (plan.CHECKPOINTS == (10, 20, 40, 80, 160, 320)
                       and plan.ASKS_PER_CHECKPOINT == 3 and plan.PRIOR_ASKS == 5
                       and plan.SMOKE_ASKS == 2 and plan.WORKERS == 4
                       and plan.MAX_REASKS == 2 and plan.AT_ONCE_MAX_TOKENS == 32000),
           "the_pool_is_for_asks": the_pool_is_for_asks()}
    ins = instruments()
    out["instruments"] = ins
    out["passes"] = all(v for k, v in out.items() if k not in ("schedule", "instruments")) \
        and ins["passes"]
    return {"what": "six runs alternating from the arm the seed draws; the smoke runs 30 cases "
                    "an arm on PLAN_CHANNEL.md's smoke draws; coverage 1/2; the cap 400; "
                    "§2.4's constants; the ask pool for the asks alone; each competitor's "
                    "ceiling", **out}


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

def run_checks(suite: bool = True) -> Checks:
    return Checks(g1=gate_g1(suite=suite), g2=gate_g2(), g3=gate_g3(),
                  g4=plan.gate_signature())


def report(checks: Checks) -> None:
    def mark(g: dict) -> str:
        return "PASS" if g["passes"] else "FAIL"

    g1, g2, g3, g4 = checks.g1, checks.g2, checks.g3, checks.g4
    s, reps = g1["suite"], g1["replays"]
    print(f"\nCR-g1 {mark(g1)}  PLAN_PLACEMENT.md's PL-g1 to PL-g3 "
          f"{g1['placement_checks']['passes']}; on its v1c runs, n is v1c "
          f"{all(r['n_is_v1c'] for r in reps.values())}, l one report apart "
          f"{all(r['one_report_apart'] for r in reps.values())} at "
          f"{sum(r['reported_errors'] for r in reps.values())} reported errors, with their "
          f"labels {all(r['reports_are_the_labels'] for r in reps.values())}; level 1 by the "
          f"system prompt alone {all(r['level_1_differs_by_the_system_prompt'] for r in reps.values())}")
    print(f"      suite {'not run' if not s.get('ran') else s.get('result')}")
    print(f"CR-g2 {mark(g2)}  texts {g2['texts']['passes']}; requests "
          f"{g2['requests']['passes']}; figures 1 to 3 {g2['drafting']['passes']}")
    print(f"CR-g3 {mark(g3)}  the schedule {g3['schedule']}; the instruments' ceilings "
          f"{g3['instruments']['passes']}")
    print(f"CR-g4 {'SIGNED' if g4['passes'] else 'UNSIGNED'}  {g4['found']} signature "
          f"line(s), {g4['unsigned']} blank")
    print(f"\nblocking checks: {'PASS' if checks.blocking_pass else 'FAIL'}")
