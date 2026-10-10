"""
WHO HAD THE LABELS. `PLAN_ILP.md` §6 declared its fourth asymmetry even: the
inducer trains on the true queue of every escalated case, and the proposer, it
said, had received it too. It had not. `OpenRouterProposer.propose` drops the
truth `run_shadow` passes it and the prompt asks the model to decide the queue,
which `tests/test_llm_path.py` has pinned since August 7, 2026. This reads, off
the committed records, what each side had and where the difference lands.
POST-HOC.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
  1. **The proposer's side**, off `results/llm_run.json`: how often it chose the
     right queue — over the escalations, over the proposals that named a queue,
     and over the rules it installed, against the ticket each was born on — and,
     per true class, which queues it named instead. A proposal can fail and bring
     nothing back, or bring back a payload that names no queue; both are read
     apart.
  2. **The inducer's side**, off `ilp/instances.py`: whether the label of each
     training example is the truth the loop recorded for that case.
  3. **The two starved classes of `I-b`**: the base's per-class ceiling — the
     corpus cases of the class that some rule carrying its queue matches — and
     the rules that supply it.
  4. **How far each training set reaches into the test split**: the cases of
     corpus test split 0 identical to an example it labels, by the `Case.key()`
     the split groups on; and, on the escalations that fall there, how often the
     proposer chose right.

It induces nothing and scores no list. Every figure is a count over the two
committed records and the instances `ilp/compare.py` read.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The tally is the record's**: right over the escalations is, to four
     decimals, the run's own `proposal_action_accuracy`, and the escalations,
     failed proposals and rules are its own `metrics`.
  2. **The labels are the record's truth**: on every case of the corpus,
     `instances.truths()` is the `truth` the loop recorded.
  3. **The ceilings are the ones `I-b` was banded against**: each equals
     `compare.I_B_CEILING`, transcribed from `results3/FINDINGS3.md` §2.
  4. **The train half reaches no test case**, which the split's grouping
     promises and the erratum leans on.

It refuses to write if any fails, and while the plan is unsigned, through
`ilp/compare.py`'s gate, called and not copied.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-HOC.** Every figure here was computed on 2026-10-10, while verifying the
erratum, before this module was written. It carries no expectation, because none
written now could have failed: it exists so that the erratum's figures reproduce
from a command. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls; seconds.

Usage:  python3 -m ilp.labels
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path
from typing import Any

from harness.dsl import Condition
from harness.provenance import describe, environment

from . import compare as cmp
from . import instances as inst

RECORD = Path("results_ilp/labels.json")
STARVED = ("ACCOUNT_MANAGER", "T3_ENGINEERING")
FAILED = "(the proposal failed)"
NO_QUEUE = "(a payload with no queue)"
TRAINING_SETS = ("train_316", "train_632")
PROVENANCE = (
    "POST-HOC: every figure here was computed on 2026-10-10, while verifying "
    "FINDINGS_ILP.md §5's erratum, before this module was written. No "
    "expectation, because none written now could have failed. Not a signed row; "
    "no verdict moves.")


def what_it_named(r: dict) -> str:
    """A failed proposal brought no payload back, and its
    `proposal_action_correct` is null; a payload can also come back with no
    queue in it, and then `predicted` is null and the proposal counts wrong."""
    if r["proposal_action_correct"] is None:
        return FAILED
    return NO_QUEUE if r["predicted"] is None else r["predicted"]


def proposer_side(run: dict) -> dict[str, Any]:
    """How often the proposer chose the right queue, three ways, and per class.

    The run's own metric counts a failed proposal and a payload with no queue
    wrong over every escalation, and so does `over_escalations`;
    `over_named` keeps only the proposals that named a queue."""
    esc = [r for r in run["records"] if r["escalated"]]
    said = [what_it_named(r) for r in esc]
    named = sum(1 for s in said if s not in (FAILED, NO_QUEUE))
    right = sum(1 for r in esc if r["proposal_action_correct"])
    truth = {r["idx"]: r["truth"] for r in run["records"]}
    rules = run["rules"]
    born_right = sum(1 for ru in rules if ru["action"] == truth[ru["born_at"]])
    per_class = {}
    for cls in sorted({r["truth"] for r in esc}):
        mine = [r for r in esc if r["truth"] == cls]
        per_class[cls] = {
            "escalations": len(mine),
            "right": sum(1 for r in mine if r["proposal_action_correct"]),
            "named": dict(collections.Counter(
                what_it_named(r) for r in mine).most_common())}
    return {"escalations": len(esc), "failed": said.count(FAILED),
            "no_queue": said.count(NO_QUEUE), "named_a_queue": named,
            "right": right,
            "over_escalations": right / len(esc),
            "over_named": right / named,
            "rules": len(rules), "rules_right_on_birth": born_right,
            "over_rules": born_right / len(rules),
            "per_class": per_class}


def inducer_side(truth: dict[int, str], labels,
                 indices: dict[str, tuple[int, ...]]) -> dict[str, Any]:
    """Whether the label of each training example is the truth the loop
    recorded for that case."""
    return {name: {"examples": len(idx),
                   "labelled_with_the_truth":
                       sum(1 for i in idx if labels[i] == truth[i])}
            for name, idx in indices.items()}


def ceilings(rules: list[dict], corpus, truth: dict[int, str],
             classes=STARVED) -> dict[str, Any]:
    """Per class: the corpus cases some rule carrying the class's queue matches
    — the base's per-class ceiling — and the rules that supply it. A case two
    such rules match counts once."""
    out = {}
    for cls in classes:
        cases = [i for i in range(len(corpus)) if truth[i] == cls]
        routing = [ru for ru in rules if ru["action"] == cls]
        reached: set[int] = set()
        supply = []
        for ru in routing:
            conds = [Condition(c["attr"], c["op"], c["value"])
                     for c in ru["conditions"]]
            hit = [i for i in cases if all(c.holds(corpus[i]) for c in conds)]
            if hit:
                supply.append({"rule_id": ru["rule_id"], "born_at": ru["born_at"],
                               "born_on": truth[ru["born_at"]], "cases": len(hit)})
            reached.update(hit)
        out[cls] = {"corpus_cases": len(cases), "ceiling": len(reached),
                    "rules_routing_here": len(routing),
                    "rules_supplying_it": supply}
    return out


def reach(corpus, indices: dict[str, tuple[int, ...]], test: tuple[int, ...],
          escalations: dict[int, dict]) -> dict[str, Any]:
    """How far each training set reaches into the test split, by case identity,
    and what the proposer chose on the escalations that fall there."""
    test_set = set(test)
    out: dict[str, Any] = {"test_cases": len(test)}
    for name, idx in indices.items():
        keys = {corpus[i].key() for i in idx}
        out[name] = {
            "test_cases_among_its_examples": len(test_set & set(idx)),
            "test_cases_identical_to_an_example":
                sum(1 for i in test if corpus[i].key() in keys)}
    there = [escalations[i] for i in test if i in escalations]
    out["escalations_in_the_test_split"] = {
        "n": len(there),
        "proposer_right": sum(1 for r in there if r["proposal_action_correct"])}
    return out


def check(metrics: dict, proposer: dict, mislabelled: int, ceil: dict,
          reached: dict) -> list[dict]:
    measured = {"proposal_action_accuracy": round(proposer["over_escalations"], 4),
                "escalations": proposer["escalations"],
                "failed_proposals": proposer["failed"],
                "n_rules": proposer["rules"]}
    published = {k: metrics[k] for k in measured}
    ratios = {cls: c["ceiling"] / c["corpus_cases"] for cls, c in ceil.items()}
    crossing = reached["train_316"]["test_cases_identical_to_an_example"]
    return [
        {"gate": 1, "what": "the tally is the record's",
         "measured": measured, "published": published,
         "passes": measured == published},
        {"gate": 2, "what": "the labels are the record's truth",
         "measured": {"corpus_cases_labelled_otherwise": mislabelled},
         "passes": mislabelled == 0},
        {"gate": 3, "what": "the ceilings are the ones I-b was banded against",
         "measured": {cls: [c["ceiling"], c["corpus_cases"]]
                      for cls, c in ceil.items()},
         "published": cmp.I_B_CEILING,
         "passes": all(ratios[cls] == cmp.I_B_CEILING[cls] for cls in ratios)},
        {"gate": 4, "what": "the train half reaches no test case",
         "measured": {"test_cases_identical_to_a_train_316_example": crossing},
         "passes": crossing == 0},
    ]


def report(proposer: dict, inducer: dict, ceil: dict, reached: dict) -> None:
    p = proposer
    print("\n  THE PROPOSER — off results/llm_run.json: it chose each queue")
    print(f"    right over the escalations     {p['right']:>4} of {p['escalations']:<5}"
          f"{p['over_escalations']:.4f}")
    print(f"    right where it named a queue   {p['right']:>4} of {p['named_a_queue']:<5}"
          f"{p['over_named']:.4f}   ({p['failed']} failed, {p['no_queue']} "
          f"named none)")
    print(f"    rules right on their birth     {p['rules_right_on_birth']:>4} of "
          f"{p['rules']:<5}{p['over_rules']:.4f}")
    for cls, c in p["per_class"].items():
        named = ", ".join(f"{q} {n}" for q, n in c["named"].items())
        print(f"      {cls:<22}{c['right']:>4} of {c['escalations']:<4} named: {named}")
    print("\n  THE INDUCER — off ilp/instances.py: it was handed each queue")
    for name, s in inducer.items():
        print(f"    {name:<12}{s['labelled_with_the_truth']:>4} of {s['examples']} "
              f"labelled with the truth")
    print("\n  THE STARVED CLASSES — the base's per-class ceiling")
    for cls, c in ceil.items():
        print(f"    {cls:<22}{c['ceiling']:>4} of {c['corpus_cases']:<4}"
              f"{c['rules_routing_here']} rules route here, "
              f"{len(c['rules_supplying_it'])} supply it")
    print(f"\n  TEST SPLIT 0 — {reached['test_cases']} cases")
    for name in TRAINING_SETS:
        r = reached[name]
        print(f"    {name:<12}{r['test_cases_identical_to_an_example']:>4} identical to "
              f"an example it labels ({r['test_cases_among_its_examples']} are examples)")
    e = reached["escalations_in_the_test_split"]
    print(f"    the proposer, on the {e['n']} escalations there: right on "
          f"{e['proposer_right']}")


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        print(__doc__)
        return 2
    gate = cmp.gate_signature()
    if not gate["passes"]:
        sys.exit(f"\nREFUSED: {cmp.PLAN} is unsigned, so ilp/labels.py writes "
                 "nothing. There is no flag that skips this.\n")
    run = json.loads(inst.RUN.read_text())
    corpus = inst.corpus()
    truth = {r["idx"]: r["truth"] for r in run["records"]}
    labels = inst.truths()
    indices = {name: inst._indices(name) for name in TRAINING_SETS}
    escalations = {r["idx"]: r for r in run["records"] if r["escalated"]}

    proposer = proposer_side(run)
    inducer = inducer_side(truth, labels, indices)
    ceil = ceilings(run["rules"], corpus, truth)
    reached = reach(corpus, indices, inst._indices("test"), escalations)
    mislabelled = sum(1 for i in range(len(corpus)) if labels[i] != truth[i])
    checked = check(run["metrics"], proposer, mislabelled, ceil, reached)

    print("=" * 78)
    print("WHO HAD THE LABELS — POST-HOC, for FINDINGS_ILP.md §5's erratum")
    print("=" * 78)
    for g in checked:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    report(proposer, inducer, ceil, reached)

    RECORD.write_text(json.dumps({
        "_env": environment(split_seed=inst.SPLIT_SEED),
        "what": "who had the labels: the proposer chose each queue, the inducer "
                "was handed it",
        "plan": str(cmp.PLAN),
        "gate": gate,
        "provenance": PROVENANCE,
        "source": {"run": str(inst.RUN), "instances": "ilp/instances.py"},
        "surface": "the corpus, n=2000, seed 17; test split 0 is rung 3's, seed 17",
        "gates": checked,
        "proposer": proposer,
        "inducer": inducer,
        "ceilings": ceil,
        "reach": reached,
    }, indent=2) + "\n")
    print(f"\n-> {RECORD}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
