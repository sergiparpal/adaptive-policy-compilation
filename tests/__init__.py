"""
Harness tests.

WHAT THEY COVER, AND WHY THESE AND NOT OTHERS

This repository is not a library: it is an experiment whose product is FIGURES.
What has to be protected is not an API, it is the numbers the `FINDINGS` cite
and that must keep reproducing. Hence the two families:

  * INVARIANTS — properties that must be true by construction. The main one:
    the 29 rules written in the DSL are equivalent to the `hidden_policy`
    predicates over the 134,400 combinations of the space, and evaluating them
    with first-match-wins reproduces the policy exactly. It is the claim the
    whole of rung 1 rests on ("execution failure, not representation failure").

  * SNAPSHOTS — the published figures, pinned to the digit: specificity ceiling
    0.5875, subsumption alone 0.6315, hybrid 1.0000, the mock frontier and the
    corpus statistics. If one of these tests fails, the correct answer is NOT to
    update the expected number: it is to find out what changed and, if the
    change is legitimate, to date the erratum in the corresponding `FINDINGS`,
    which is how this project records corrections.

SUITE RULE: no test writes to `results*/`. The records are the product of the
experiment and only whoever runs the experiment on purpose rewrites them. That
is why the tests call the measurement functions and never the scripts'
`main()`, which do dump their JSON.

Rungs 3 and 4 are covered by DETERMINISM, not by snapshot: their published
figures are those of the code prior to the tie-break fix of August 6, 2026 and
are pending a re-run. Pinning the new values here would create a second official
figure that no FINDINGS backs.

    python3 -m unittest discover -v       # everything, zero API calls
"""
