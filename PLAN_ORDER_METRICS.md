# PLAN — An instrument that measures orders, not scores

> **[CLOSED 2026-08-14] Executed in full.** §0 was drafted and committed in
> `0f2dcf8` before any figure existed and signed unchanged in `2a59853` the same
> day. **The figures are owned by
> [`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md)**, which also owns
> the filled `G1`-`G6` register that §4 leaves blank here on purpose, and no
> number is to be read off this file. Of the six `Q` rows §0 signed, **all six
> were adjudicated: `Q-d` and `Q-f` refuted, the other four held** — the
> scoreboard is in [`STATUS.md`](STATUS.md). Nothing below is pending work; the
> instrument it built is `rung3/order_metrics*.py`, and its blocking step 0 is
> `tests/test_order_metrics_gate.py`.
>
> **This banner touches neither §0 nor §4's status column**, which are the two
> things this plan says are not edited after signing. It sits above both and
> travels alone, as `e59f36f` did for `PLAN_BUDGET_LS.md` — which is where the
> convention of closing a plan in the file itself comes from, so that anyone
> opening it reads the closure first.
>
> **It does cost §0's signature block one command, so the replacement goes here
> rather than in a later reader's surprise.** The signature says `git diff
> 0f2dcf8 -- PLAN_ORDER_METRICS.md` shows only that line and the §4 pointer. That
> was true until this banner existed; a two-dot diff against the working tree is
> cumulative, so it now shows this text too — 29 insertions where the claim
> predicts 10. **Bound it at the signing commit and it says exactly what it said:**
>
>     git diff 0f2dcf8 2a59853 -- PLAN_ORDER_METRICS.md
>
> §0 itself is unedited either way, and `git log -p PLAN_ORDER_METRICS.md` shows
> that without needing a range. The signature is not touched to say so, because
> it is Sergi's.

**Destination:** repository root, beside `PLAN_BUDGET_LS.md`. **Drafted:**
2026-08-14. **For:** execution by a coding agent, start to finish, without
further design decisions.

This opens the two entries `IDEAS.md` gained on 2026-08-13 — *search budget above
the declared 64 buys labels and sells policy*, and *the peak of the multi-start is
a singleton that spreads* — both of which say the same thing about themselves:
**falsifiable by measuring orders, not scores.**

Four rungs have compared permutations of 577 elements by looking at a scalar. The
mechanical root of that is small and checkable: **no record in `results*/` holds
an order produced by the audited optimizer.** The only complete order the
repository has ever stored is in `results3/order_search.json` — the rung-3 greedy,
which is to say the superseded one. Everything else was scored and discarded.

Where this plan and `CLAUDE.md` disagree, `CLAUDE.md` wins and the agent stops
and says so.

---

## 0. Prediction — written before the run

**Drafted by Claude on 2026-08-14. Not binding until Sergi signs or replaces it**
(`CLAUDE.md`, hard rule 2). The agent **must not** edit this section, before or
after seeing any number. P4 does not start until this section carries a signature
line. Commit the plan before P1, so that `git log -p` can show the prediction
predates every figure.

**Signed — Sergi, 2026-08-14.** I adopt §0 as drafted, without changes.
`git diff 0f2dcf8 -- PLAN_ORDER_METRICS.md` shows only this line and the
pointer in §4, so no row of the table moved. P4 may start.

**What is being bet on.** With first-match-wins, the relative order of two rules
can only change a decision if **both match some common case and they prescribe
different actions**. Measured on the exhaustive space: of the 166,176 pairs,
53,620 co-match and **35,457 conflict — 21.3%**. So roughly four fifths of a
577-element permutation is free: two orders can differ in hundreds of positions
and be the same machine. A rank correlation over all pairs would spend most of
its mass on the part that cannot matter. The bet is that this is not a technicality
but the whole difficulty, and that the honest measure is not a rank statistic at
all but **on how many of the 134,400 cases two orders decide differently** —
exact, and 0.6 ms per order.

| # | prediction | refuted by |
|---|---|---|
| **Q-a** | Split 0, the winner at 65 starts against the winner at 257: they disagree on **≥ 6,910** cases of the space (5.1%). The floor of 3,455 is arithmetic — a space accuracy gap of 0.0257 over 134,400 cases cannot arise from fewer — so the bet is only that gross disagreement is at least twice the net. | Below 6,910. Below 3,455 means the harness is wrong, not the prediction. |
| **Q-b** | **The headline.** At 1% (split 0, draw 0), among the orders that tie at the best train score, the median pairwise disagreement over the space is **above 20%** (26,880 cases). Tying on 10 labels does not make two orders the same machine. | A median below 5%. |
| **Q-c** | At full supervision the 65 end orders give **65 distinct behavioural signatures**, and the best against the runner-up disagree on **more than 2%** of the space despite being ≤ 2 train cases apart. | Any two signatures identical, or under 0.5%. |
| **Q-d** | *Calibration.* Kendall tau over all 577 rules tracks behavioural distance poorly (\|Spearman\| **< 0.5** across the measured pairs); tau restricted to the 35,457 conflicting pairs tracks it well (**> 0.8**). | The restricted metric failing to beat the global one. Then the design premise of this instrument is wrong and the record says so. |
| **Q-e** | Positional churn overstates functional difference: **> 60%** of rules sit at a different index between two end orders while behavioural disagreement stays **below 30%**. | Churn and disagreement of comparable size. |
| **Q-f** | Disagreement concentrates where material is scarce: the per-class rate for **ACCOUNT_MANAGER** and **T3_ENGINEERING** is **≥ 2×** the overall rate. | Either class at or below the overall rate. |

**What this can withdraw.** Step 3 reads the low-budget rows as *the tie-break
regularises*: the objective saturates, 56 of 65 starts tie, ties go to index 0,
index 0 is the greedy, so the search returns the greedy and cannot lose. If Q-b
holds, that reading is too kind. The search would be picking arbitrarily among 56
**very different machines** and merely happening to land on a sane default — safe
by accident of the start order, not by property of the search. That is a caveat
for `STATUS.md` beside the low-budget rows, and a warning to anyone who ever
changes the tie-break or the order of the declared starts.

**Not predictions, invariants** — if they fail, something is broken: `d(a, a) = 0`;
`d(a, b) = d(b, a)`; two orders differing only in non-conflicting pairs are at
distance 0; and every regenerated score equals the published one exactly.

---

## 1. What is built

**One module, `rung3/order_metrics.py`.** Pure functions over orders and
masks. It does not consult the oracle, does not read the corpus, writes no JSON,
and knows nothing about optimizers. Everything it needs arrives as arguments.

```
decisions(order, M, action, full)        -> {action: mask}, undecided_mask
                                            one sweep, 0.6 ms on the space
behavioural_distance(dA, dB, full)       -> agree, disagree, undecided_either
conflicting_pairs(ids, M, action)        -> the pairs whose relative order can
                                            change a decision (35,457 on the space)
tau(a, b, pairs=None)                    -> Kendall tau, over all pairs or a set
positions_moved(a, b)                    -> count and displacement distribution
per_class_disagreement(dA, dB, truth)    -> rate by true class
```

Two rules with different identity and the **same action** decide a case the same
way, so agreement is computed on the **action**, never on which rule fired. A
separate attribution count — do the two orders fire the same rule where they
agree — is reported as a secondary quantity, because it is interesting for
explainability and is not the thing being measured.

---

## 2. Hard invariants

1. The five `[FROZEN]` files are not touched.
2. `MULTISTART_SEED = 17`, `MULTISTART_STARTS = 64`, `DECLARED_NEIGHBOURHOOD` are
   not tuned. This plan reads a budget of 129 and 257 in **diagnosis only**, as
   `start_budget_check` already did; the declared constant does not move, and no
   result of this run is an argument for moving it.
3. No existing file in `results*/` is written to. Tests never write there.
4. Every JSON carries `_env`. Every figure names its surface and its pool.
5. Orders are regenerated, not invented: the parity gate of P4 is what makes a
   regenerated order the same object as the published one.
6. Bad numbers are reported, not fixed; a legitimate change is a **dated erratum**
   in the FINDINGS that owns the figure, original kept beside it.
7. Section 0 is not edited, and P4 does not start without its signature.
8. `PLAN_*.md` travels alone in its commit — the guard of PR #9 enforces it, and
   `--no-verify` is not the way past it.
9. The agent's final report ends with the SHA it pushed.

---

## 3. Phases, with mandatory stops

### P0 — Baseline

Suite green, tree clean, `core.hooksPath` pointing at `.githooks`. Commit the
plan **alone**, as its own commit, before anything else. **STOP** if the suite is
not green.

### P1 — Capture the orders that are currently discarded

`multistart` keeps `rows` with a score per start and returns only `best_order`;
the other 64 end orders are dropped. Add `keep_orders=False`: when true, each row
gains its `"order"`. Additive and nothing else.

Gate: with `keep_orders=False` the returned stats dict is **identical** to today's
for a set of instances — pinned by test, since every existing record was produced
through this function.

### P2 — The instrument

Implement §1. Tests, all on small hand-built instances where the answer is known
by hand rather than by running the code:

- identity and symmetry;
- a three-rule instance with the decision table written out by hand;
- **the motivating property**: two orders differing only in the relative order of
  non-conflicting rules are at behavioural distance 0 while their positional
  distance is large;
- `tau` against a brute-force O(n²) count on ≤ 8 elements, over all pairs and over
  a given pair set;
- `conflicting_pairs` against a brute-force double loop;
- an order that leaves cases undecided, so the undecided branch is exercised.

**STOP** unless the whole suite is green.

### P3 — Step 0 for the instrument (BLOCKING)

The repository's own pattern: validate against an instance whose answer is known
**for a reason** before believing anything the instrument says. Use the 29 rules
of the hidden policy (`rung3/optimizer_check.py::hidden_rules`,
`masks_over_space`):

| check | expected, and why |
|---|---|
| design order vs itself | 0 |
| design order vs a permutation touching only non-conflicting pairs | **0**, and global tau < 1 while restricted tau = 1 |
| design order with two conflicting rules swapped | the disagreement equals the size of the intersection of their masks restricted to the cases neither loses to an earlier rule — computed independently, by hand, in the test |
| design order vs the fully reversed order | large, and reported as the scale |

**STOP and report** on any mismatch. An instrument that cannot recover an answer
known by construction does not get pointed at the real instance.

### P4 — Backwards over what is already measured

Regenerate, capturing orders. All deterministic, no API calls:

- **A.** Split 0, fraction 1.0, pure pool, budgets 65 / 129 / 257 (~135 s).
- **B.** Split 0, fraction 0.01, draw 0, 65 starts — the tied set (~80 s).
- **C.** Split 4, budgets 65 / 257 — the other split where the train score moved,
  so Q-a is not answered on one split (~120 s).

**Parity gate, blocking:** every regenerated `train_score`, `test` and `space`
must equal the published value **exactly** — `results3/start_budget_check.json`
for A and C, `results3/budget_and_balance_ls.json` for B. A mismatch means the
regenerated orders are not the measured ones and nothing below is about them.

Then compute, for each set: the full pairwise behavioural distance matrix, the
two taus, positional churn, per-class rates, and the number of distinct
behavioural signatures.

### P5 — The record

`results3/order_metrics.json`, with `_env` plus `budgets`, `splits`, `fraction`,
`pool`, `surface`, `n_conflicting_pairs`. Store the **signatures and the
distances**, not the 65 orders themselves — except the handful the findings cite,
which are stored explicitly so a reader can check them. Say in `what` which orders
were regenerated and from which published rows.

### P6 — Documentation

- **`results3/FINDINGS_ORDERS.md`**, new, owns these figures. It is not a step of
  the optimizer audit: the audit was about a search, this is about what the search
  returns.
- **`IDEAS.md`**: both 2026-08-13 entries gain what this settled and what it did
  not. If Q-b holds, the *singleton* entry is not closed but sharpened, and the
  *budget* entry now has the instrument it asked for.
- **`STATUS.md`**: the new figures, with surfaces named; and if Q-b holds, the
  caveat beside the low-budget rows of step 3.
- **`README.md`**: a command line and a row in the overwrite table.
- No figure in `README.md`, `CLAUDE.md` or `IDEAS.md` beyond a pointer.

---

## 4. Findings register — mandatory

| id | finding | status |
|---|---|---|
| **G1** | No record in `results*/` holds an order from the audited optimizer; the only stored order is the superseded rung-3 greedy in `order_search.json`. Confirm, and note whether that is worth changing for future runs — reporting, not fixing. | |
| **G2** | Of 166,176 pairs, 53,620 co-match and 35,457 conflict on the space (measured 2026-08-14, to be reproduced). Confirm, and report the same counts over the corpus pool, which is a different and smaller surface. | |
| **G3** | Whether the 65 end orders cluster into few behavioural classes or are all distinct. | |
| **G4** | Any pair with behavioural distance 0 and positional distance > 0 — proof in the real instance of what P2 pins on a toy. | |
| **G5** | Where the greedy start's end order sits relative to the random starts' end orders: inside their cloud or off to one side. | |
| **G6** | Anything the parity gate turns up. | |

**Where the filled register lives.** The status column stays empty in this
file on purpose: the plan is not edited after signing, so that its own log
shows the prediction preceding every figure instead of a diff having to prove
it. `results3/FINDINGS_ORDERS.md` (P6) owns the register, with its findings
dated in place.

---

## 5. Measured cost

Probed 2026-08-14 on a container, pure pool, 577 rules, exhaustive space of
134,400: building the space masks **0.0 s** (they are already cheap once the
extensions are computed), the conflicting-pair census **0.3 s**, one order's full
decision vector **0.6 ms**. A 65 × 65 distance matrix is 2,080 comparisons, so
seconds. The cost is entirely in regenerating the orders: **≈ 6 min** for A, B and
C together. This is an instrument over data already measured, which is why it is
cheap; the reason it cannot be run over stored artefacts is G1.
