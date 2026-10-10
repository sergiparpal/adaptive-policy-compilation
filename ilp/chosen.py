"""
THE INDUCER ON THE QUEUES THE PROPOSER CHOSE. §5's erratum of `FINDINGS_ILP.md`
found that the inducer was handed the true queue of every example while the
proposer chose its own, and §7 that all of the inducer's +0.0342 is the answer
key. This is the control both leave open: the same inducer, on the same tickets,
labelled with the queue the proposer named for each instead of the truth. It
compiles the proposer's own answers, as the 577 rules do, so what separates it
from them is the compiler. POST-RUN.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
  1. **Two training sets.** `chosen_632`: every escalation on which the
     proposer named a queue, labelled with that queue — the 632 less the 34
     proposals that failed and the 19 that named none. `chosen_316`: those of
     them in rung 3's train half. Both are built by `ilp/instances.py`'s own
     `masks`, with the proposer's queues where `instances.instance` puts the
     truth.
  2. **Four lists**, induced by `ilp/induce.py` at both beams and scored as
     `ilp/compare.py` scores — against the truth, on corpus test split 0 and over
     the exhaustive space — with the two classes of `I-b` and §7's partition of
     the test split into the 371 and the 624.
  3. **Beside them, from the records that own them**: the searched order over
     the 577 rules (`results3/order_search_ls.json`, `results_ilp/margin.json`);
     the same rules in arrival order, `born_at` (`results3/floor_by_pool.json`);
     and the lists handed the truth (`results_ilp/compare.json`).

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The labels are the record's**: the queues named number 579, and 245 of
     them are right, as `labels.json` counts them.
  2. **The instrument is `compare.py`'s**: the same code, given the truth instead
     of the proposer's queues, reproduces the four published lists' test counts.
  3. **The sets nest**: `chosen_316` inside `chosen_632` and `train_316`, and
     `chosen_632` inside `train_632`.

It refuses to write if any fails, and while the plan is unsigned, through
`ilp/compare.py`'s gate, called and not copied.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  1. **Below the searched order**: on test split 0 every list trained on the
     proposer's queues scores below the order's 843 of 995, 0.8472, on both sets
     and at both beams. The drafter gives it nineteen in twenty.
  2. **The labels are worth more than the tickets**: the `chosen_632` lists, on
     579 tickets the proposer labelled, score below the `train_316` lists, on 316
     tickets labelled with the truth — below 0.7759 at beam 40 and 0.7628 at
     beam 120. Nine in ten.
  3. **The bet: the inducer compiles the proposer's answers better than the
     proposer did.** The `chosen_632` lists score above the proposer's own rules
     in arrival order, `born_at`'s 519 of 995, 0.5216, at both beams. Neither
     uses the truth; the inducer still sees its examples at once and chooses its
     own order. About even odds.
  4. **`ACCOUNT_MANAGER` goes with the labels**: the `chosen_632` lists score at
     or below the base's per-class ceiling there, 0.3578, at both beams, where the
     lists handed the truth score 0.7636 and 0.7455. The proposer named that
     queue twice, once on a ticket of that class. Four in five.

**What the drafter had seen**: `FINDINGS_ILP.md` with its errata and §7;
`compare.json`, every figure of the four lists handed the truth; `labels.json`,
including the queues the proposer named per class; `margin.json`; split 0's
row of `order_search_ls.json`; and `floor_by_pool.json`. **Not seen**: any list
induced on the proposer's queues, or any figure of one.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: asked for on 2026-10-10, after §7, with the expectation above
written and committed before the first run. Not a signed row, not on
`STATUS.md`'s scoreboard, not a calibration event. Zero API calls; under a
minute.

Usage:  python3 -m ilp.chosen
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from harness.provenance import describe, environment

from . import compare as cmp
from . import induce as ind
from . import instances as inst
from .margin import partition, parts, won_by_list

RECORD = Path("results_ilp/chosen.json")
LABELS_RECORD = Path("results_ilp/labels.json")
COMPARE_RECORD = Path("results_ilp/compare.json")
MARGIN_RECORD = Path("results_ilp/margin.json")
ORDER_RECORD = Path("results3/order_search_ls.json")
FLOOR_RECORD = Path("results3/floor_by_pool.json")
STARVED = ("ACCOUNT_MANAGER", "T3_ENGINEERING")
SETS = ("chosen_316", "chosen_632")
PROVENANCE = (
    "POST-RUN: asked for on 2026-10-10, after FINDINGS_ILP.md §7. The "
    "expectation in the module's docstring was written and committed before the "
    "first run. Not a signed row; no verdict moves.")


def chosen(records: list[dict]) -> dict[int, str]:
    """The queue the proposer named on each escalation that named one: not a
    proposal that failed, nor a payload with no queue in it."""
    return {r["idx"]: r["predicted"] for r in records
            if r["escalated"] and r["proposal_action_correct"] is not None
            and r["predicted"] is not None}


def instance_of(idx, labels):
    """`instances.masks` over the corpus cases of `idx`, labelled by `labels`,
    which is indexed by case: the truth, or the queues the proposer named."""
    corpus = inst.corpus()
    return inst.masks([corpus[i] for i in idx], [labels[i] for i in idx])


def read_list(train_idx, labels, beam, test, space, reached) -> dict[str, Any]:
    """One list, induced on `labels` and scored against the truth."""
    ext, lab, n = instance_of(train_idx, labels)
    got = ind.induce(ext, lab, n, beam=beam)
    s_ext, s_truth, s_n = test
    t = ind.score(got, s_ext, s_truth, s_n)
    won = won_by_list(got, s_ext, s_truth, s_n)
    return {"examples": n, "n_rules": got.n_rules, "hit_the_cap": got.hit_the_cap,
            "left_undecided_on_train": got.left_undecided,
            "fit_to_its_labels": ind.score(got, ext, lab, n)["correct"],
            "test": {"correct": t["correct"], "accuracy": t["accuracy_end_to_end"],
                     "per_class": {c: t["per_class"][c] for c in STARVED}},
            "space": ind.score(got, *space)["accuracy_end_to_end"],
            "partition": parts(won, reached, (1 << s_n) - 1)}


def compute(run: dict) -> dict[str, Any]:
    named = chosen(run["records"])
    truth = {r["idx"]: r["truth"] for r in run["records"]}
    train = {t: inst._indices(t) for t in ("train_316", "train_632")}
    idx = {"chosen_632": tuple(sorted(named)),
           "chosen_316": tuple(sorted(set(named) & set(train["train_316"])))}
    test, space = inst.instance("test"), inst.instance("space")
    reached, _own = partition(inst.corpus(), train["train_632"], inst._indices("test"))
    replicated = {}
    for t, t_idx in train.items():
        for beam in ind.BEAM_WIDTHS:
            ext, lab, n = instance_of(t_idx, inst.truths())
            got = ind.induce(ext, lab, n, beam=beam)
            replicated[f"{t}|{beam}"] = ind.score(got, *test)["correct"]
    lists = {f"{s}|{beam}": read_list(idx[s], named, beam, test, space, reached)
             for s in SETS for beam in ind.BEAM_WIDTHS}
    return {"named": named, "truth": truth, "train": train, "idx": idx,
            "replicated": replicated, "lists": lists}


def check(c: dict, labels_rec: dict, runs: dict) -> list[dict]:
    named, truth, idx, train = c["named"], c["truth"], c["idx"], c["train"]
    p = labels_rec["proposer"]
    measured = [len(named), sum(1 for i, q in named.items() if q == truth[i])]
    published = [p["named_a_queue"], p["right"]]
    replicated = c["replicated"]
    counts = {k: runs[k]["test"]["correct"] for k in replicated}
    nest = (set(idx["chosen_316"]) <= set(idx["chosen_632"])
            and set(idx["chosen_316"]) <= set(train["train_316"])
            and set(idx["chosen_632"]) <= set(train["train_632"]))
    return [
        {"gate": 1, "what": "the labels are the record's",
         "measured": measured, "published": published, "passes": measured == published},
        {"gate": 2, "what": "the instrument is compare.py's",
         "measured": replicated, "published": counts, "passes": replicated == counts},
        {"gate": 3, "what": "the sets nest",
         "measured": {s: len(idx[s]) for s in SETS}, "passes": nest},
    ]


def references(runs: dict, margin_rec: dict, order_row: dict, floors: list) -> dict:
    """Every figure the lists are read against, from the record that owns it."""
    born = {f["surface"]: f["value"] for f in floors
            if f["order"] == "born_at" and f["pool"] == "puro"}
    order = margin_rec["order"]
    return {
        "test_cases": margin_rec["parts"]["test"],
        "order": {"test_correct": order["total"], "test": order_row["ls_test"],
                  "space": order_row["ls_space"], "on_the_371": order["reached"],
                  "on_the_624": order["not_reached"]},
        "born_at": {"test": born["corpus_test_split0"], "space": born["space"]},
        "handed_the_truth": {
            k: {"test_correct": r["test"]["correct"],
                "test": r["test"]["accuracy_end_to_end"],
                "space": r["space"]["accuracy_end_to_end"],
                "per_class": {c: r["test"]["per_class"][c] for c in STARVED}}
            for k, r in runs.items()},
    }


def read_expectation(lists: dict, refs: dict) -> list[dict]:
    beams = [str(b) for b in ind.BEAM_WIDTHS]
    n = refs["test_cases"]

    def correct(s, b):
        return lists[f"{s}|{b}"]["test"]["correct"]

    def am(s, b):
        return lists[f"{s}|{b}"]["test"]["per_class"]["ACCOUNT_MANAGER"]["accuracy"]

    born = round(refs["born_at"]["test"] * n)
    truth_316 = {b: refs["handed_the_truth"][f"train_316|{b}"]["test_correct"]
                 for b in beams}
    return [
        {"clause": 1, "what": "every list on the proposer's queues scores below "
                              "the searched order, both sets, both beams",
         "reading": {f"{s}|{b}": correct(s, b) for s in SETS for b in beams},
         "holds": all(correct(s, b) < refs["order"]["test_correct"]
                      for s in SETS for b in beams)},
        {"clause": 2, "what": "the chosen_632 lists score below the train_316 "
                              "lists, beam for beam",
         "reading": {b: [correct("chosen_632", b), truth_316[b]] for b in beams},
         "holds": all(correct("chosen_632", b) < truth_316[b] for b in beams)},
        {"clause": 3, "what": "the chosen_632 lists score above born_at, the "
                              "proposer's rules in arrival order, at both beams",
         "reading": {b: [correct("chosen_632", b), born] for b in beams},
         "holds": all(correct("chosen_632", b) > born for b in beams)},
        {"clause": 4, "what": "on ACCOUNT_MANAGER the chosen_632 lists score at or "
                              "below the base's ceiling, at both beams",
         "reading": {b: am("chosen_632", b) for b in beams},
         "holds": all(am("chosen_632", b) <= cmp.I_B_CEILING["ACCOUNT_MANAGER"]
                      for b in beams)},
    ]


def report(lists: dict, refs: dict) -> None:
    n = refs["test_cases"]
    print(f"\n  {'':<30}{'test':>8}{'of':>6}{'acc':>9}{'space':>9}"
          f"{'the 371':>9}{'the 624':>9}{'AM':>8}{'T3':>8}{'rules':>7}")
    for k, v in lists.items():
        pc = v["test"]["per_class"]
        print(f"  {'proposer queues, ' + k:<30}{v['test']['correct']:>8}{n:>6}"
              f"{v['test']['accuracy']:>9.4f}{v['space']:>9.4f}"
              f"{v['partition']['reached']:>9}{v['partition']['not_reached']:>9}"
              f"{pc['ACCOUNT_MANAGER']['correct']:>5}/{pc['ACCOUNT_MANAGER']['n']:<2}"
              f"{pc['T3_ENGINEERING']['correct']:>5}/{pc['T3_ENGINEERING']['n']:<2}"
              f"{v['n_rules']:>7}")
    o, b = refs["order"], refs["born_at"]
    print(f"  {'the searched order':<30}{o['test_correct']:>8}{n:>6}{o['test']:>9.4f}"
          f"{o['space']:>9.4f}{o['on_the_371']:>9}{o['on_the_624']:>9}")
    print(f"  {'born_at, arrival order':<30}{round(b['test'] * n):>8}{n:>6}"
          f"{b['test']:>9.4f}{b['space']:>9.4f}")
    for k, v in refs["handed_the_truth"].items():
        print(f"  {'the truth, ' + k:<30}{v['test_correct']:>8}{n:>6}{v['test']:>9.4f}"
              f"{v['space']:>9.4f}")


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        print(__doc__)
        return 2
    gate = cmp.gate_signature()
    if not gate["passes"]:
        sys.exit(f"\nREFUSED: {cmp.PLAN} is unsigned, so ilp/chosen.py writes "
                 "nothing. There is no flag that skips this.\n")
    run = json.loads(inst.RUN.read_text())
    labels_rec = json.loads(LABELS_RECORD.read_text())
    runs = json.loads(COMPARE_RECORD.read_text())["runs"]
    margin_rec = json.loads(MARGIN_RECORD.read_text())
    order_row = next(r for r in json.loads(ORDER_RECORD.read_text())["splits"]
                     if r["split"] == 0 and r["pool"] == "puro")
    floors = json.loads(FLOOR_RECORD.read_text())["floors"]

    print("=" * 78)
    print("THE INDUCER ON THE QUEUES THE PROPOSER CHOSE — POST-RUN")
    print("=" * 78)
    c = compute(run)
    checked = check(c, labels_rec, runs)
    for g in checked:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    refs = references(runs, margin_rec, order_row, floors)
    report(c["lists"], refs)
    expectation = read_expectation(c["lists"], refs)
    print()
    for e in expectation:
        print(f"  expectation {e['clause']}: {'holds' if e['holds'] else 'FAILS'}  "
              f"{e['what']}")

    RECORD.write_text(json.dumps({
        "_env": environment(split_seed=inst.SPLIT_SEED, beams=list(ind.BEAM_WIDTHS)),
        "what": "the inducer trained on the queues the proposer chose, on the "
                "same tickets, scored against the truth: a control on the compiler",
        "plan": str(cmp.PLAN),
        "gate": gate,
        "provenance": PROVENANCE,
        "source": {"labels": f"{inst.RUN}, the queue each escalation's proposal named",
                   "references": [str(p) for p in (ORDER_RECORD, MARGIN_RECORD,
                                                   FLOOR_RECORD, COMPARE_RECORD)]},
        "surface": "corpus test split 0, 995 cases, and the exhaustive space, "
                   "134,400; scored against the truth, first match wins",
        "gates": checked,
        "training_sets": {s: len(c["idx"][s]) for s in SETS},
        "lists": c["lists"],
        "references": refs,
        "expectation": expectation,
    }, indent=2) + "\n")
    print(f"\n-> {RECORD}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
