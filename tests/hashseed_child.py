"""
Child process of `test_order_determinism.py`. Not a test: it does not start with
`test_` and `unittest discover` does not collect it.

Runs the greedy search of rungs 3 and 4, plus the multi-start local search the
audit added on August 8, 2026, and prints a JSON of fingerprints. It is invoked
several times with a different `PYTHONHASHSEED`; the parent compares.

The local search is here for the reason rung 4 recorded the hard way: a
same-process determinism test permuted something that did not govern the
tie-break, returned a variance of 0.0000, and that zero was read as proof. Only
varying `PYTHONHASHSEED` exercises the real mechanism, so any new optimizer that
figures in a published number gets signed here too.

    python3 -m tests.hashseed_child        # from the repository root
"""

from __future__ import annotations

import hashlib
import json
import sys

from peldano3.local_search import (declared_starts, greedy_order_from_masks,
                                   multistart)
from peldano3.optimizer_check import (hidden_rules, masks_over_corpus,
                                      tail_key_factory)
from peldano3.order_search import (build_tables, evaluate, greedy_order, load,
                                   split, subsumption_below)
from peldano4.feedback import Channel
from peldano4.sweep import greedy_from_reports, pi0_decisions


def digest(seq) -> str:
    h = hashlib.sha256()
    for x in seq:
        h.update(str(x).encode())
        h.update(b"\0")
    return h.hexdigest()[:16]


def main() -> int:
    corpus, rules, ext, conds = load()
    action = {r["rule_id"]: r["action"] for r in rules}
    born = {r["rule_id"]: r["born_at"] for r in rules}
    below = subsumption_below(rules, ext)
    matched, undef, truth = build_tables(corpus, rules, conds, below)
    ids = [r["rule_id"] for r in rules]
    tr, te = split(corpus, truth, seed=17)

    # WITNESS: the iteration order of a set of strings DOES depend on
    # PYTHONHASHSEED. It serves to distinguish "the fix works" from "there were
    # no ties to break here".
    control = digest(set(ids))

    order = greedy_order(rules, matched, truth, action, tr)

    dec = pi0_decisions(matched, sorted(ids, key=lambda r: born[r]), action, tr)
    rep = Channel(coverage=0.5, asymmetry=0.0, delay=0, noise=0.1,
                  seed=0).observe(corpus, tr, dec, window_end=max(tr))
    order4 = greedy_from_reports(rules, matched, rep, action, born)

    # The audit's optimizer, over the 29-rule instance so that this stays cheap.
    # The 577 are not touched here: no figure of Step 1 is produced by a test.
    hids, hconds, haction, hborn = hidden_rules()
    hM, hW, hfull = masks_over_corpus(hids, hconds, haction, corpus)
    hgreedy = greedy_order_from_masks(
        hids, hM, hW, hfull, tail_key=tail_key_factory(hM, hW, hborn))
    hbest, hstats = multistart(declared_starts(hids, first=hgreedy),
                               hM, hW, hfull, neighbourhood="move+swap")

    print(json.dumps({
        "set_iteration": control,
        "greedy_p3": digest(order),
        "greedy_p4": digest(order4),
        "test_p3": round(evaluate(order, matched, truth, action, te), 6),
        "n_rules": len(rules),
        "n_reports": len(rep),
        "multistart_order": digest(hbest),
        "multistart_score": hstats["best_score"],
        "multistart_from": hstats["best_from"],
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
