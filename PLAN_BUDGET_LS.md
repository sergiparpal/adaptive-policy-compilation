# PLAN — Audit Step 3: `budget_and_balance` with the audited optimizer

> **[CLOSED 2026-08-14] Executed in full.** The seven phases merged in
> [#7](https://github.com/sergiparpal/adaptive-policy-compilation/pull/7), their
> tail — the §0 signature among it — in
> [#8](https://github.com/sergiparpal/adaptive-policy-compilation/pull/8), and
> the process guard that the step's one traceability defect earned in
> [#9](https://github.com/sergiparpal/adaptive-policy-compilation/pull/9). **The
> figures are owned by
> [`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md), Step 3**, and no
> number is to be read off this file. Nothing below is pending work: what is kept
> here is §0, the prediction immutable before any number existed, and its four
> refuted bets.

**Destination:** repository root, next to `PLAN_AUDIT` (referenced from
`rung3/local_search.py`). **Drafted:** 2026-08-12. **For:** execution by a
coding agent, start to finish, without further design decisions.

This plan closes open item **nº 1 of `STATUS.md`**: `budget_and_balance` is the
only figure of rungs 3 and 4 still produced entirely by the superseded greedy,
and it is the source of *50 labels are enough to order* — the premise rung 4 was
opened on. It is the only remaining item that can **withdraw** a published
figure.

Nothing here authorises touching the frozen specification, the optimizer's
declared constants, or any existing record. Where this plan and `CLAUDE.md`
disagree, `CLAUDE.md` wins and the agent stops and says so.

---

## 0. Prediction — written before the run

**Drafted by Claude on 2026-08-12. It is not binding until Sergi signs or
replaces it** (`CLAUDE.md`, hard rule 2: predictions are his). The agent **must
not** edit this section, before or after seeing any number. Phase P4 does not
start until this section carries a signature line.

**Signed by Sergi, 2026-08-13, after the run.** The prediction was drafted on
2026-08-12 and became immutable in commit `6b8311b`, before any figure existed;
the authorization for P4 was given before launching it and §0 has not been
edited since — `git log -p PLAN_BUDGET_LS.md` verifies it. The signature arrives
late; the prediction does not.

**Mechanism being bet on.** At 1005 labels the train objective separates orders
finely. At 50 it is an integer out of 50 with massive ties, and at 10 it is
noise. The multi-start keeps the order with the best **train** score and breaks
ties by start index, which is uncorrelated with test performance. A stronger
optimizer therefore buys the most where the objective is informative and can
actively lose where it is not: it maximises harder the thing that has stopped
being a proxy.

| # | prediction | refuted by |
|---|---|---|
| **P-a** | The 100% row lands at **0.8530 ± 0.0062** on corpus test. | Anything else. This is a gate, not a bet: the same protocol already published it (`order_search_ls.json`, pure pool). A miss means the harness differs and the whole curve is uninterpretable. |
| **P-b** | The gain of LS over the greedy on **test** shrinks monotonically as the budget shrinks: ≥ +0.07 at 100%, and **≤ +0.02 at 5%**. | A flat or growing gain across budgets. |
| **P-c** | At **1%** (10 labels) LS is **worse on test** than the greedy. | LS ≥ greedy at 1%. |
| **P-d** | The headline ratio falls: 5%/100% goes from the published **0.915** (0.7049/0.7707) to **below 0.85**. | A ratio ≥ 0.90. This is the prediction that decides whether "50 labels are practically free" survives. |
| **P-e** | Dispersion grows at low budget: sd at 5% **above 0.0535**, at 1% **above 0.0628**. | Smaller sd than the greedy's at both. |
| **P-f** | On the exhaustive space every row sits far below its corpus figure, and the **low-budget rows lose proportionally more**, because a small label sample can only encode the arrival distribution. | Low budgets transferring as well as full supervision. |
| **P-g** | §2: with a competent optimizer, balancing costs **less** in aggregate than the published −0.0557 and buys **more** than the published +0.1695 in balanced accuracy — part of the greedy's sacrifice of rare classes was search weakness, not objective conflict. | Either quantity moving the other way. |

**Not predictions, invariants** — if they fail, something is broken, not
surprising: LS ≥ greedy on **train** in every configuration (the greedy is start
0); the `ceiling` column of the per-class table does not move (it is
search-independent); ACCOUNT_MANAGER stays capped at 21 of 55 test cases.

**What the whole thing is worth.** If P-d holds, `FINDINGS3` §4 gets a dated
erratum and rung 4's opening premise is withdrawn. If P-d fails, "50 labels are
enough" survives a stronger optimizer and gets *stronger*, and that is a result
too (`CLAUDE.md` rule 6).

---

## 1. What changes and what does not

**Only the optimizer.** Decision-list greedy → the multi-start local search
declared in `rung3/local_search.py`: seed 17, 64 random starts plus the
record's greedy at index 0, neighbourhood `move+swap`.

**Identical, and to be verified as identical:** corpus of 2000 at seed 17; the
five splits (`split(corpus, truth, seed=17 + s)`, grouped by case identity,
stratified by action, 50/50); the pure pool (`matched` from `build_tables`);
`FRACTIONS = [1.0, 0.25, 0.10, 0.05, 0.01]`; `N_DRAWS = 5`; `N_SPLITS = 5`; the
draw seeds `random.Random(1000 * s + d)`; simple random subsampling, never
stratified (stratifying would need the labels being rationed); evaluation always
over the whole test half.

**Two figures move**, and both are in `results3/budget_and_balance.json`:

```
 fraction  labels   test e2e      sd      min      max
     100%    1005     0.7707  0.0374   0.7425   0.8430
      25%     251     0.7681  0.0326   0.7290   0.8522
      10%     100     0.7488  0.0352   0.6500   0.8053
       5%      50     0.7049  0.0535   0.5596   0.8241
       1%      10     0.5251  0.0628   0.3850   0.6577

 objective          e2e test    balanced acc
 total                0.7707          0.5241
 balanced             0.7150          0.6936
```

Those figures are **pre-tie-break** (the record predates the 2026-08-06 fix,
which is already in the file). So the run produces **three columns**, not two:
published, greedy-today, local-search-today. The delta between the first two is
the tie-break and is a finding in its own right.

---

## 2. The four decisions, declared

### D1 — The balanced objective gets a weighted local search, and it is cheap

`local_search.py` scores an **integer count** of cases won; its termination and
its freedom from tie-breaking both rest on that. The balanced objective weights
each case by 1/|class|. Naively that costs per-class masks and ~8× the work.

**It does not, because of this lemma:** every case in `W[r]` has label
`action[r]`, since `W[r]` is by construction the subset of `M[r]` the rule gets
right. **The class of a win is a function of the rule, not of the case.** So a
class-weighted objective is exactly the unweighted machinery with each rule's hit
count scaled by one integer:

```
wt[r] = L // n[action[r]]        L = lcm{ n[c] : c in classes present in the labelled subset }
                                 n[c] = cases of class c in the labelled subset
```

`L` integral keeps the score a bounded integer, so *strict improvement* still
guarantees termination and no move is ever applied on a tie. Big `L` is fine —
Python ints. The weighted score is `L · Σ_c recall_c`, i.e. macro-recall up to a
constant, which is what `per_class` already reports as balanced accuracy.

**Where it applies** (all four places count hits attributable to the firing
rule):

- `score_order`: `ok += wt[rid] * (W[rid] & fires).bit_count()`
- `_prefix_states`, `_score_after_swap`: same substitution
- `best_insertion`: `B[k] = wt[r] * (Wr & remaining).bit_count()`; `acc +=
  wt[rest[k]] * (hits & Mr).bit_count()`; `C += wt[rest[k]] * (hits &
  not_Mr).bit_count()`

**Not** in `greedy_order_from_masks`: its step criterion is `hit − miss`, and a
*miss* can belong to any class, so its weight is not a function of the rule. The
weighted start does not come from there — see D2.

API: thread an optional `wt=None` through `score_order`, `best_insertion`,
`move_pass`, `swap_pass`, `local_search`, `multistart`; `None` means uniform and
must remain **bit-identical** to today's behaviour.

### D2 — Start 0 is the record's greedy, tail included

For both objectives the first start is `rung3.budget_and_balance.greedy(...)`
called with the same arguments the record used (`weights=None` for §1 and the
total objective, `weights=w` for the balanced one). That function already returns
a complete order, tail sorted by train precision then `born_at`. Consequences,
both wanted: the multi-start can never be worse **on train** than the single
greedy run, and the difference measured is the optimizer and nothing else.

Random starts are full shuffles and have no tail; rules the objective cannot see
never move, because no move is applied without strict improvement.

### D3 — A new record, and the old one is never touched

- Write `results3/budget_and_balance_ls.json`, with `_env`.
- `results3/budget_and_balance.json` is **read-only for this work**. It is
  deliberately pre-tie-break and without `_env` so the old numbers stay
  reproducible beside the new ones (`IDEAS.md`).
- **Never run `python3 -m rung3.budget_and_balance`.** It is unguarded and
  dumps over that record on finishing. To obtain greedy-today, import and call
  `budget_and_balance.greedy` / `order_search.evaluate` — never a script's
  `main()`. This is the same discipline the test suite follows.
- Partial runs get their own name, following `rung4/sweep_ls.py::record_name`:
  a full run writes `budget_and_balance_ls.json`; `--sections budget` writes
  `budget_and_balance_ls_budget.json`, and so on. Every save rewrites the whole
  document from the rows of *this* process, which is why a partial run must not
  land on the canonical name.
- Save after every fraction and after every split of §2, not only at the end: the
  run is tens of minutes and an interrupted one must not lose its rows.

### D4 — Both surfaces, because the space transfer is nearly free

Each configuration reports its corpus test figure (primary, comparable with the
record) **and** the score of the same order over the exhaustive space of 134,400
combinations, pure pool. `rung4/sweep_ls.py` already reports a `space` column
per row; this follows it, and `STATUS.md` requires the surface to be named.

Measured cost of the addition: **2.3 s** to build the space masks once, **~1 ms**
per order scored. The hybrid pool stays out of scope: `budget_and_balance` never
used it, and it is ~8× slower.

---

## 3. Hard invariants

1. The five `[FROZEN]` files are not touched. If one looks wrong, stop and say so.
2. `MULTISTART_SEED = 17`, `MULTISTART_STARTS = 64`, `DECLARED_NEIGHBOURHOOD =
   "move+swap"` are **not yours to tune** (`CLAUDE.md`). Changing one after
   seeing a result is rule 6 under another name.
3. No existing file in `results*/` is written to. The tests never write there.
4. The instances are the record's instances: same splits, same fractions, same
   draw seeds, same pool. Only the optimizer changes.
5. Start 0 of every multi-start is the record's greedy.
6. No move is applied on a tie; every score stays a bounded integer.
7. Bad numbers are reported, not fixed. No snapshot expectation is edited to
   match a new measurement; a legitimate change gets a **dated erratum** in the
   FINDINGS that owns the figure, original kept beside it.
8. Every JSON written carries `_env` (`harness.provenance.environment(**extras)`).
9. Every figure names its **surface** (corpus test / exhaustive space) and its
   **pool** (pure).
10. Section 0 is not edited by the agent, and P4 does not start without its
    signature line.
11. If the new module imports the oracle, it is added **deliberately** to the
    `permitidos` set in `tests/test_oracle_separation.py`, with a comment saying
    it is an offline measurement. The list is pinned so that growing it is a
    decision, not an oversight.

---

## 4. Phases, with mandatory stops

### P0 — Baseline

```
git status                       # tree clean before starting
python3 -m unittest discover     # green, 0 API calls, no writes to results*/
git config core.hooksPath .githooks
```

Record the commit. **STOP** if the suite is not green: nothing below is
interpretable.

### P1 — The weighted objective in `local_search.py`

Implement D1. Add to `tests/test_local_search.py`:

- **Uniform equivalence.** On ≥ 50 random instances (small: ~20 rules, ~40
  cases), `wt` all-ones returns the *same order and the same score* as `wt=None`,
  for `score_order`, `best_insertion`, `move_pass`, `swap_pass`, `local_search`.
- **Weighted score is right.** `score_order(..., wt)` equals a naive
  first-match-wins recomputation that walks cases one at a time and adds
  `L // n[class]`.
- **`best_insertion` is exhaustive.** Its `(position, score)` equals brute force
  over every reinsertion, weighted and unweighted.
- **Termination.** `stats["exhausted"]` is False on every instance.
- **Cost.** The unweighted path does not slow by more than ~10% (the run budget
  in §8 depends on it).

**STOP** unless the full suite is green.

### P2 — Step 0 for the weighted instrument (BLOCKING)

The repo's own pattern: validate an instrument against an instance whose optimum
is known **for a reason**, before believing anything it says. Reuse
`rung3/optimizer_check.py`: `hidden_rules()`, `masks_over_space()`,
`masks_over_corpus()`.

The 29 rules of the hidden policy in design order get **every** case right, so
they maximise every positive-weight objective simultaneously. The weighted
optimum is therefore known by construction: `L × (number of classes present)`.

Run the weighted multi-start on both instances. Report, per instance: whether the
optimum was reached, `starts_until_first_hit`, `n_hits`, and whether the design
order is a fixed point (a search that walks away from a global optimum is
broken).

**STOP and report** if the optimum is not reached. Do not proceed to figures, do
not adjust constants, do not widen the neighbourhood. That is precisely the
situation of 2026-08-08, and it was resolved by Sergi, not by the agent.

### P3 — Harness parity, no figures yet (BLOCKING)

Three checks, all against published numbers:

| check | expected | source |
|---|---|---|
| `budget_and_balance.greedy(..., full train)` ≡ `order_search.greedy_order(...)` | same order | two implementations of one algorithm |
| split 0, frac 1.0, pure pool: `greedy_test` / `ls_test` / `coverage_length` | **0.7487** / **0.8472** / **559** | `results3/order_search_ls.json`, `splits[0]` |
| space harness: `score_order(sorted(ids), M_space, W_space, full) / 134400` | **0.3148** | born_at on the space (`sorted(ids)` is born_at order; verified) |

**STOP** on any mismatch: the instances or the surfaces differ from the record's
and nothing downstream is comparable.

### P4 — §1, the label-budget curve

105 configurations: 5 splits × 1 draw at frac 1.0, plus 5 splits × 5 draws at
each of the other four. Per configuration record: `fraction, split, draw, labels,
greedy_train, greedy_test, greedy_space, ls_train, ls_test, ls_space, best_from,
best_from_index, rounds, exhausted, coverage_length, seconds`.

Print, per fraction, a table with published / greedy-today / LS-today, their sd,
min, max, the space column and the elapsed seconds. Save after every fraction.

### P5 — §2, the balanced objective

5 splits × {total, balanced}, weighted LS for the balanced one. Report aggregate
e2e test and balanced accuracy for greedy and LS under both objectives, the cost
of balancing in aggregate, the gain in balanced accuracy, and the per-class table
for split 0 with its `ceiling` column and both optimizers.

**Identity check:** the total-objective rows must be *identical* to the frac 1.0
rows of P4 — same call, same instances. The published record satisfies it
(0.7707 in both places). A mismatch is a bug in the new harness.

### P6 — The record

Write `results3/budget_and_balance_ls.json`:

```json
{
  "_env": { "...": "...", "n_splits": 5, "n_draws": 5,
            "fractions": [1.0, 0.25, 0.1, 0.05, 0.01],
            "neighbourhood": "move+swap", "multistart_seed": 17,
            "multistart_starts": 64 },
  "what": "step 3 of the rungs 3/4 audit: the label-budget curve and the balanced objective, re-measured with the declared multi-start local search",
  "pool": "puro",
  "surfaces": ["corpus test", "espacio exhaustivo"],
  "n_rules": 577, "n_cases": 2000, "n_space": 134400,
  "references": { "publicado pre-desempate": { "...": "the five rows and the two objectives" },
                  "born_at corpus": 0.5216, "born_at espacio": 0.3148,
                  "aleatorio corpus": 0.4227,
                  "ls supervision plena, pool puro (order_search_ls)": 0.8530 },
  "label_budget": [ { "fraction": 1.0, "labels": 1005, "n_runs": 5,
                      "greedy": {"test_mean": 0, "test_sd": 0, "test_min": 0, "test_max": 0, "space_mean": 0},
                      "ls":     {"test_mean": 0, "test_sd": 0, "test_min": 0, "test_max": 0, "space_mean": 0},
                      "delta_test_mean": 0, "coverage_length_mean": 0, "seconds": 0 } ],
  "label_budget_runs": [ { "...": "one row per configuration, fields listed in P4" } ],
  "objective_comparison": { "total": {"...": "greedy and ls, e2e_test_mean, balanced_acc_mean, space_mean"},
                            "balanced": {"...": "idem"} },
  "per_class_split0": { "CLASS": {"test": 0, "ceiling": 0,
                                  "greedy_total": 0, "greedy_balanced": 0,
                                  "ls_total": 0, "ls_balanced": 0} },
  "checks": { "...": "the three P3 checks and the P5 identity, with their verdicts" },
  "seconds_total": 0
}
```

CLI: `python3 -m rung3.budget_and_balance_ls [--sections budget,balanced]`.

### P7 — Documentation

Figures have exactly two homes: the FINDINGS that owns them and `STATUS.md`.

- **`results3/FINDINGS_AUDIT.md`** gains a **Step 3** section: what was re-run,
  the three columns, the answers to P-a…P-g, and the cost. This is the owner of
  the new figures.
- **`results3/FINDINGS3.md` §4** gains a dated erratum beside the 50-label table,
  pointing at the new record. The original table stays untouched.
- **`STATUS.md`**: open item 1 moves out of "What is open" — into "What is
  established" or "What was withdrawn" according to the result — with its surface
  named, and the index gains the new record.
- **`README.md`**: a command line under the AUDIT block, and a row in the
  overwrite table (`budget_and_balance_ls.py` → `results3/budget_and_balance_ls.json`,
  "partial runs get their own name").
- **`IDEAS.md`**: the "half-resolved 2026-08-08" note updated — `budget_and_balance`
  is no longer the one that was never re-run.
- No figure goes into `README.md`, `CLAUDE.md` or `IDEAS.md`.

---

## 5. Findings register — mandatory

The run is not finished until this table is filled in and reported, including a
line for every entry below, confirmed or refuted, plus anything new.

| id | finding | status |
|---|---|---|
| **F1** | `tests/test_provenance.py::WRITERS` lists neither `rung3.order_search_ls`, `rung4.sweep_ls` nor `rung3.optimizer_check`, though the README table it says it mirrors does list them. Same for `FREE` in `tests/test_record_guard.py`. Pre-existing drift between a pinned list and its stated source. **Report it; do not fix it silently as part of this work.** | |
| **F2** | Greedy-today vs published, per row: the size of the 2026-08-06 tie-break fix on this record, never measured. | |
| **F3** | Any configuration with `exhausted: true` — the safety net was hit, which the module says must not pass silently. | |
| **F4** | Configurations where LS is worse than the greedy on **test**. Expected at low budget (P-c); it is the finding, not a bug. Count them per fraction. | |
| **F5** | Per-fraction cost. In probing, LS from the greedy start was **slower** at partial budgets (~2 s) than at full supervision (~0.3 s), making 25% the most expensive row. Confirm or refute; it is a fact about the instrument. | |
| **F6** | Any class whose `ceiling` differs from the published `per_class_split0`. Would mean the pool or the split moved. | |

---

## 6. Measured cost

Probed on 2026-08-12 on a container, pure pool, 577 rules, split 0 — an estimate,
not a promise; the run must print its own seconds per fraction.

| fraction | labels | rules matching ≥1 label | LS from greedy | LS from random | configs | estimate |
|---|---|---|---|---|---|---|
| 100% | 1005 | 572 | 0.29 s | 0.48 s | 5 | 2.6 min |
| 25% | 251 | 560 | 1.96 s | 0.57 s | 25 | 16.0 min |
| 10% | 100 | 518 | 2.62 s | 0.34 s | 25 | 10.3 min |
| 5% | 50 | 479 | 1.82 s | 0.23 s | 25 | 6.8 min |
| 1% | 10 | 330 | 1.19 s | 0.09 s | 25 | 2.9 min |

**§1 ≈ 38 min** at 65 starts per configuration; §2 adds 10 configurations at full
supervision (≈ 5 min, the weighted half at comparable cost per D1); the space
transfer adds 2.3 s plus ~1 ms per order. The estimate of *1–2 h* in
`CHAT_SUMMARY.md` §3 is the right order of magnitude on a slower machine.
