"""
Child process of `test_order_determinism.py`. Not a test: it does not start with
`test_` and `unittest discover` does not collect it.

Runs the greedy search of rungs 3 and 4 and prints a JSON with four
fingerprints. It is invoked several times with a different `PYTHONHASHSEED`; the
parent compares.

    python3 -m tests.hashseed_child        # from the repository root
"""

from __future__ import annotations

import hashlib
import json
import sys

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

    print(json.dumps({
        "set_iteration": control,
        "greedy_p3": digest(order),
        "greedy_p4": digest(order4),
        "test_p3": round(evaluate(order, matched, truth, action, te), 6),
        "n_rules": len(rules),
        "n_reports": len(rep),
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
