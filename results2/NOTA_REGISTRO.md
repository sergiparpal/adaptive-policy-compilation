# Record notes

## August 6, 2026 — `results/subsumption.json` changed date during Step 1 of rung 2

Step 1 of rung 2 requires checking that rung 1 still reproduces. That check is
done by running the original scripts:

    python3 -m harness.ceiling_check
    python3 -m harness.subsumption_check

`ceiling_check` writes nothing. `subsumption_check` **does**: it finishes by
dumping `results/subsumption.json`. On re-running it, the file was rewritten.

**Nothing was lost.** The computation is entirely deterministic — fixed corpus
with seed 17, frozen hidden policy, exhaustive space of 134,400 combinations —
and the rewritten content is identical to the previous one. Verified field by
field after the rewrite:

    order.ordered_pairs                        61
    order.possible_pairs                      406
    order.incomparable_pairs                  345
    order.contradictions_with_layer_order       0
    arbitration.subsumption.action           1263
    arbitration.subsumption.conflict          737
    arbitration.subsumption.correct          1263
    arbitration.subsumption.e2e            0.6315
    arbitration.subsumption.silent_error      0.0
    concentration_curve k=10                0.8415
    concentration_curve k=20                0.8870
    concentration_curve k=50                0.9495

The only thing that changed is the `mtime`: from Aug 6 14:20 to Aug 6 16:23.

## Why this is put on record

Rung 1 is a closed record and its figures must keep reproducing. A modification
date later than the closing, with no explanation, is indistinguishable from
tampering. It is noted here that the change was produced by the verification and
not by a re-execution with different parameters.

Everything rung 2 produces goes to `results2/` and does not touch `results/`.

## How to re-verify without writing again

    python3 -m harness.subsumption_check | head -20

The on-screen output contains the same figures; the dump to disk is a side effect
of the rung 1 script that is not fixed here, because `harness/` is a closed
record and modifying it would have the same problem we are trying to avoid.

---

## August 7, 2026 — six records re-run so they would earn their `_env`

That day `harness/provenance.py` was added, which hangs an `_env` block off every
JSON with the interpreter, the platform, `PYTHONHASHSEED`, the commit and a
digest of the code. No published record carried it: the field appears when the
figure is re-run, and nothing had been re-run.

The **six that are deterministic and cost zero API calls** were re-run, which are
exactly those where reproducing cannot change anything:

    python3 run_experiment.py frontier                          # results/frontier.json
    python3 -m harness.subsumption_check                        # results/subsumption.json
    python3 -m harness.learned_subsumption                      # results/learned_subsumption.json
    python3 -m peldano2.ceiling_check2                          # results2/ceiling2.json
    python3 -m peldano2.compare_runs results2/llm_run2_*.json   # results2/comparativa.json
    python3 -m peldano2.note_audit  results2/llm_run2_*.json    # results2/note_audit.json

**Not a single datum changed.** Verified by structural comparison against the
version in git, not by eye: for the first four, the whole object minus the `_env`
key equals the published one; for the last two, the rows under `rows` equal the
published list, all 8, in the same order.

The last two did **change shape**, which was expected and the reason they were
re-run: their writers went from dumping a bare list to dumping
`{"_env": …, "rows": […]}`, which is the only way to hang provenance off them.
They were invoked with the glob of the eight runs; calling them with a single
file would have shrunk the record from 8 to 1, which is data loss and not a
change of digits.

### What was NOT re-run, and why

- `results/llm_run.json`, `results/llm_run_n100_smoke.json` and the eight
  `results2/llm_run2_*.json`: reproducing them costs money and **they would not
  come out the same** — the proposer is not deterministic at `temperature 0`.
  Besides, `llm_run.json` is the base of 577 rules that rungs 3 and 4 start from
  (hard rule 4).
- `results3/order_search.json`, `results3/budget_and_balance.json` and
  `results4/sweep.json`: they are free and deterministic, but re-running them
  **does move the digits**, because the August 6 tie-break fix is not yet
  incorporated into their published figures. It is deferred on purpose, to be
  done together with the serious optimizer.

### The `git_dirty` of these six, and a trap when re-running them in a batch

All six say `git_dirty: false`, `code_dirty: false` and `git_commit: 684f0e9`,
with the same `code_digest` `43e91ada22e9587f`. That is: that commit identifies
exactly the code that produced the six figures.

(They were re-run three times the same day, all free and all with identical
content: the first to earn the `_env`, the second with the tree already
committed, and the third after splitting the dirty flag, which changes the
`code_digest` because it touches `harness/provenance.py`. What follows is what
was learned along the way.)

It took two attempts, and the reason deserves to be noted because it will happen
to anyone repeating this. **Running the six back to back does not give
`git_dirty: false` except in the first one**: each script leaves its JSON
modified, so the tree the second one sees is already dirty, and the third one
more so. On the first pass only `frontier.json` came out clean and the other five
said `true`.

The flag was not lying, but it was measuring what does not matter: what dirtied
the tree were *records*, not code. The correct way is to run each script from a
clean tree, set its JSON aside and restore the tree before the next one:

    for each script:
        check that `git status --porcelain` is empty
        run the script
        copy its JSON to a temporary file
        git checkout -- results results2
    at the end, put all six in place at once

None of the six reads another's output, so the order does not matter. This way
each `_env` block tells the truth about the code that ran, which is what the
field exists for.

**The block no longer forces this dance in order to know that.** Out of this came
the split of the flag into `git_dirty` (whole tree) and `code_dirty` (only
`CODE_ROOTS`), which is the one that decides whether `git_commit` identifies what
ran. With both, a back-to-back batch would have said
`git_dirty: true, code_dirty: false` and would have read correctly the first
time. The dance is kept here because it still gives the cleanest possible
provenance — both flags `false` — and because the procedure holds for any other
batch.

What was **not** done is narrowing the flag that already existed: three of these
six — `learned_subsumption`, `compare_runs` and `note_audit` — read records from
`results*/` **as input**, so a modified and uncommitted JSON breaks the
traceability of those figures without touching a line of code, and a single flag
narrowed to `CODE_ROOTS` would have kept quiet about it.

### Why the commit they cite is not the one that contains them

A record cannot carry inside it the hash of the commit that transports it. The
six were produced with the tree clean at `684f0e9` and were committed in the
following commit, which touches only these six JSON files and this note: not a
line of `harness/`, `peldano2..4/` or `run_experiment.py`. That is why
`code_digest` is still the same in both commits, and `git_commit: 684f0e9` still
identifies the code exactly.

---

## August 7, 2026 — the `code_digest` moved: everything was translated to English

The prose of the repository went from Spanish to English: the ten `.md`
documents, and the comments and docstrings of every `.py`, of
`.githooks/pre-commit`, of the two `.github/` files and of the two
`requirements*.txt`.

**Consequence on the provenance:** `code_digest` is a sha256 of the **bytes** of
`CODE_ROOTS`, comments included, so it moved:

    before  43e91ada22e9587f
    after   d9406dbe1d2ca233

**Not one figure changed.** Nothing was touched but prose: no logic, no
threshold, no seed. The evidence, in the order it was checked:

- the 249 tests pass, and they are the ones that pin 0.5875 · 0.6315 · 1.0000 ·
  1.0000, the mock frontier, the corpus, and that replay `results/llm_run.json`
  and `results2/llm_run2_n100.json` rule by rule and record by record;
- `python3 -m harness.ceiling_check` still prints the 134,400 combinations
  verified, `DSL ≡ lambdas: OK`, `first-match-wins ≡ true_action: OK`, and
  ACTION 1495 / CONFLICT 505 / silent error 0.2140 / e2e 0.5875, with 1.0000 for
  the design order;
- `ruff check` reports exactly the same 27 findings as before the translation.

### Why this is put on record

For the same reason as the `mtime` note at the top of this file: a digest that
stops matching, with no explanation, is indistinguishable from code that changed
what it does. Here what changed is what the code *says*, not what it *computes*.

The six records that carry `_env` keep citing `43e91ada22e9587f` at `684f0e9`,
and that remains correct: that digest identifies the code that produced them.
What no longer holds is that it matches the current tree — which is the point of
the field, and the reason it is worth writing down that the discrepancy is a
translation and not a change of behaviour.

### What was NOT done, and why

**They were not re-run.** It is free and deterministic, and the content would
come out identical field by field: only `recorded_at`, `git_commit` and
`code_digest` would move. It is left for whoever next has a reason to re-run
them, rather than done as a side effect of a translation — the same criterion as
everywhere else in this file.

The five frozen files of hard rule 1 (`hidden_policy.py`, `domain.py`, `dsl.py`,
`shadow.py`, `cache_baseline.py`) were touched, with Sergi's explicit
authorization and in comments and docstrings only.

**What stays in Spanish, on purpose:** the prompts of `harness/proposers.py` and
`peldano2/proposers2.py`, because they are the text that produced the records
and `tests/doubles.py` replays the runs against them; and the printed output,
the error messages and the identifiers, because the docs quote those tables as
expected results and the tests match those messages. When a block in the README
or in `CLAUDE.md` shows an expected result, compare the **numbers**.
