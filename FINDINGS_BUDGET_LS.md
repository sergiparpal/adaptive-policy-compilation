# Findings register — Audit Step 3 (`budget_and_balance` with the audited optimizer)

The register §5 of [`PLAN_BUDGET_LS.md`](PLAN_BUDGET_LS.md) makes mandatory. It
is a **working file**, not a record: at phase P7 it is folded into
[`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md), which is the record
that will own the Step 3 figures, and this file goes away with the plan.

**Opened 2026-08-12. Phases P0, P1, P2 and P3 are done; P4 onward are not**, so
every entry that depends on the label-budget curve is still open. §0 of the plan
carries no signature and P4 does not start without it (plan invariant 10).

**2026-08-13** — a blocking check Sergi called for before P4, which P2 could not
have made, **found a real defect in the instrument** (F10) and forced two more
entries (F11, F12). It is recorded here in full because it is the cleanest
example in this branch of a gate passing for the wrong reason.

**No figure of the new curve exists yet.** What is below is the instrument, the
harness and one reproduced configuration.

---

## The register

| id | finding | status |
|---|---|---|
| **F1** | `tests/test_provenance.py::ESCRITORES` and `tests/test_record_guard.py::LIBRES` under-list the modules that write records, against the README table `ESCRITORES` says it mirrors. | **CONFIRMED.** Reported, not fixed — see below. |
| **F2** | Greedy-today vs published, per row: the size of the 2026-08-06 tie-break fix on this record, never measured. | **OPEN** — needs P4. Machinery in place and verified. |
| **F3** | Any configuration with `exhausted: true`. | **OPEN** for the curve. 390 weighted local searches in P2: none exhausted. |
| **F4** | Configurations where LS is worse than the greedy on **test**. Expected at low budget (P-c). | **OPEN** — needs P4. |
| **F5** | Per-fraction cost; in probing, LS from the greedy start was slower at partial budgets than at full supervision. | **OPEN** — needs P4. One point consistent with the probe. |
| **F6** | Any class whose `ceiling` differs from the published `per_class_split0`. | **OPEN** — needs P5. |
| **F7** | This work extends F1's drift: `peldano3.optimizer_check_wt` writes a record and is in neither pinned list nor the README table, and P6 will add `budget_and_balance_ls`. | **NEW, open for P7.** |
| **F8** | Pairwise `swap` alone cannot reach the weighted optimum either: 0 of 65 starts on both instances. | **NEW, confirmed in P2.** |
| **F9** | The optimum is never reached from the greedy start under weights — always from a random restart. | **NEW, confirmed in P2.** |
| **F10** | `class_counts_from_masks` returned the per-class **ceiling**, not the class size. It agrees with the truth only where every case is winnable, which is true of the hidden policy and false of the 577 rules. **The P2 gate could not see it.** | **NEW, CONFIRMED 2026-08-13. Fixed: the function now refuses; P5 uses `Counter(truth)`.** |
| **F11** | The restart budget's *"below 1e-8"* is calibrated at a 1-in-4 hit rate measured **without** weights. At the measured weighted rates it is **1.8e-3** on the corpus, five orders of magnitude worse. | **NEW, recomputed and recorded. Constant untouched.** |
| **F12** | `move+swap` reaches the optimum from **fewer** starts than `move` alone on the corpus, weighted and unweighted alike; and the tie on the space that the declaration rested on has broken. | **NEW, confirmed.** |

---

## F1 — the pinned lists under-list the writers · CONFIRMED

Verified by discovering the writers mechanically (every `write_text(json.dumps`
under `harness/`, `peldano2/`, `peldano3/`, `peldano4/` and `run_experiment.py`)
and differencing against each pinned list.

**Missing from `ESCRITORES`:** `peldano3.optimizer_check`,
`peldano3.order_search_ls`, `peldano4.sweep_ls`. The list's own comment says
*"the list is in the README, in the table «reproducing a figure overwrites its
own record»"*, and the README table does carry all three.

**Missing from `LIBRES`:** the same three. The other absences from that list —
`run_experiment`, `peldano2.run2`, `peldano2.compare_runs`,
`peldano2.note_audit` — are **not** drift: `LIBRES` is the list of writers that
must *not* import the guard, and those four are guarded on purpose. The plan's
wording of F1 is right for both lists; only that nuance is worth adding.

**Why no test catches it.** The two tests over `ESCRITORES` divide the work in a
way that leaves a gap: `test_los_escritores_conocidos_importan_environment`
iterates the pinned list, so an absent module is simply never checked, and
`test_ningun_escritor_de_JSON_se_queda_sin_env` does discover new writers but
only asks that they carry `_env` — which all of them do. Under-listing is
therefore silent by construction.

**Not fixed here, deliberately**, per the instruction opening this branch: it is
pre-existing drift, it predates this work, and folding a repair into a branch
that is measuring something else would make the diff say two things at once.

---

## F7 — this branch widens F1 · NEW

`peldano3/optimizer_check_wt.py` writes `results3/optimizer_check_wt.json` and
appears in neither pinned list nor the README overwrite table. P6 will add
`peldano3/budget_and_balance_ls.py` → `results3/budget_and_balance_ls.json`.

**P7 owes the README table a new row**, asked for explicitly on 2026-08-13:

> | `peldano3/optimizer_check_wt.py` | `results3/optimizer_check_wt.json` | no, on purpose |

alongside the row P7 already plans for `budget_and_balance_ls.py`. Whoever
repairs F1 should take all of them in one pass. Recorded here so the new drift is
a decision rather than an oversight — which is the reason the lists are pinned at
all.

---

## F8 — `swap` alone fails under weights too · CONFIRMED (P2)

On the class-balanced objective, over the 29 rules of the hidden policy, with
the multi-start's 65 declared starts:

| instance | `move` | `swap` | `move+swap` |
|---|---|---|---|
| corpus | **1.000000**, 9/65 | 0.995523, **0/65** | **1.000000**, 6/65 |
| exhaustive space | **1.000000**, 11/65 | 0.992092, **0/65** | **1.000000**, 4 starts, 12/65 |

Figures are balanced accuracy — the weighted score over its known optimum
`L × (number of classes)`. Record:
[`results3/optimizer_check_wt.json`](results3/optimizer_check_wt.json).

This is the same shape of failure Step 0 found unweighted (0.9356 over the
space, 0 of 65), now confirmed for the second objective. It is a fact about the
method, not a reason to widen anything: `move+swap` is the declared
neighbourhood, it is what P4 and P5 will run, and it is what passed.

The design order is a **fixed point** of all three neighbourhoods on both
instances, so the search never walks away from a global optimum — which is the
cheapest way to see that the objective being maximized is the declared one.

---

## F9 — under weights the restarts are what find the optimum · NEW (P2)

The unweighted greedy sits at **0.4346** balanced on the corpus and **0.7753**
on the space, against 0.7365 and 0.8993 unweighted e2e: the greedy that is a
reasonable start for total accuracy is a poor one for the balanced objective,
which is what a greedy maximizing the wrong quantity should look like.

It never reaches the optimum. Every first hit is a random restart — start 6
(`aleatorio 4`) on the corpus, start 4 (`aleatorio 2`) on the space.

**Consequence for P5, and it is already what D2 declares:** the balanced
configuration's start 0 must be `budget_and_balance.greedy(..., weights=w)`, the
*balanced* greedy, not the unweighted one used here. Start 0 is what makes the
multi-start provably no worse than the record's single greedy run, and that
guarantee only holds against the greedy the record actually used for that
objective.

---

## F10 — the mask counts were per-class ceilings · CONFIRMED, and the gate could not see it

Predicted by Sergi before P4, on the reasoning that the masks yield the ceiling
and not the class size, and confirmed on the real instance — 577 rules, split 0
train, pure pool:

| clase | `Counter(truth)` | de máscaras | falta | % |
|---|---|---|---|---|
| T2_TECHNICAL | 362 | 357 | 5 | 98.6% |
| SELF_SERVICE_DEFLECT | 253 | 237 | 16 | 93.7% |
| BILLING_SPECIALIST | 135 | 135 | 0 | 100% |
| T1_GENERAL | 127 | 127 | 0 | 100% |
| **T3_ENGINEERING** | 60 | **19** | 41 | **31.7%** |
| **ACCOUNT_MANAGER** | 54 | **18** | 36 | **33.3%** |
| SECURITY_INCIDENT | 10 | 10 | 0 | 100% |
| ONCALL_ESCALATION | 4 | 4 | 0 | 100% |
| **total** | 1005 | 907 | **98** | |

The union of the correct masks counts the cases of a class that *some correct
rule matches*. That is the per-class ceiling. It equals the class size only when
every case is winnable.

**Why it would have mattered.** The shortfall lands precisely on the two classes
FINDINGS3 §2 records as materially broken — 66.7% of T3_ENGINEERING and 64.2% of
ACCOUNT_MANAGER have no correct rule at all. Weighting by `L/19` instead of
`L/60` inflates T3_ENGINEERING **3.2×** and ACCOUNT_MANAGER **3.0×**: exactly the
classes the balanced objective exists to protect, and exactly the direction that
flatters it. §2 would have compared the record's greedy, weighted by
`1/Counter(truth)`, against a search weighted by a ceiling, and reported the
difference as the optimizer.

**Why P2 could not catch it.** On the hidden policy every case is covered by its
own rule, so ceiling and class size coincide and the derivation is exact. The
gate reaching `L × classes` was evidence for the *search*, and none at all for
the *counting* — the instance was the one instance where the bug is invisible. A
step 0 validates against an instance whose optimum is known; this is the failure
mode where the instance is also the one that hides the defect.

**What was done, and it is not silent.** `class_counts_from_masks` now checks its
precondition — the union of the correct masks against `full` — and **raises**
rather than return a ceiling a caller would read as a count. It keeps working for
P2, where the precondition holds, and refuses everywhere else. The old signature
would not even have raised; it took a fourth argument to make the check possible.

For P5 the objective is built by `budget_and_balance_ls.balanced_objective`,
from `Counter(truth[i] for i in label_idx)` — the very expression
`budget_and_balance.main` uses — and it returns the greedy's float weights and
the search's integer weights **from one Counter object**, with the identity
checked at runtime and the proportionality `wt[r] × counts[action[r]] == L`
pinned by test. The two forms cannot diverge because there is only one count.

---

## F11 — the restart budget does not hold at the measured rate · RECOMPUTED

`local_search.py` justifies 64 starts thus: *"At a one-in-four rate, 64 starts
miss altogether with probability 0.75\*\*64, below 1e-8."* That rate was measured
**unweighted**, in Step 0. Recomputed at the weighted rates, over the 64 random
starts alone — the greedy occupies index 0 and hits in none of the six
configurations, so it is not part of the budget:

| instancia · vecindario | aciertos | tasa | IC95 tasa | fallo | IC95 fallo |
|---|---|---|---|---|---|
| corpus · move | 9/64 | 0.1406 | [0.0664, 0.2502] | 6.1e-05 | [9.9e-09, 1.2e-02] |
| corpus · swap | 0/64 | 0.0000 | [0.0000, 0.0560] | 1.00 | [2.5e-02, 1.00] |
| **corpus · move+swap** | **6/64** | **0.0938** | [0.0352, 0.1930] | **1.8e-03** | [1.1e-06, **1.0e-01**] |
| espacio · move | 11/64 | 0.1719 | [0.0890, 0.2868] | 5.7e-06 | [4.0e-10, 2.6e-03] |
| espacio · swap | 0/64 | 0.0000 | [0.0000, 0.0560] | 1.00 | [2.5e-02, 1.00] |
| **espacio · move+swap** | **12/64** | **0.1875** | [0.1008, 0.3046] | **1.7e-06** | [8.0e-11, 1.1e-03] |

Intervals are exact (Clopper-Pearson, 95%, standard library only). The figures
are in `results3/optimizer_check_wt.json` under `restart_budget`, per instance
and neighbourhood, beside the inherited claim for comparison.

**The declared neighbourhood on the corpus is five orders of magnitude worse
than the inherited claim** — 1.8e-03 against 1.0e-08 — and the honest reading is
the interval, whose upper end is **0.10**: a fresh set of 64 starts could miss
entirely about one time in ten. On the space, the instance that validates, the
point estimate is 1.7e-06, still two orders worse than claimed.

Three caveats, all of which cut against over-reading the table:

- The point estimate reuses the same draws that produced the rate, so it is not
  an independent prediction. The interval is the honest part.
- It is measured on **29 rules**. P4 and P5 run on 577, where the rate has no
  reason to be this one and cannot be measured at all, since no optimum is known
  there. That is the whole reason the gate exists on a known instance.
- `0.75**64` is `1.0091e-08`, marginally *above* the "below 1e-8" the comment
  claims. Immaterial, but this entry is about the claim, so it is stated exactly.

**The constant is not touched.** `MULTISTART_STARTS = 64` was declared before the
runs that used it, and changing it after seeing a result is `CLAUDE.md` rule 6
under another name — the same reasoning that made the 2026-08-08 instrument
change legitimate makes this one illegitimate. What is recomputed is the claim
made *about* the constant, which is not the constant. A test pins that the three
declared constants still read 17, 64 and `move+swap`.

---

## F12 — the richer neighbourhood is not uniformly the better one · CONFIRMED

Hits out of the random starts, weighted against the unweighted Step 0 record:

| instancia | `move` (sin pesos → con pesos) | `move+swap` (sin pesos → con pesos) |
|---|---|---|
| corpus | 16/65 → **9/64** | 13/65 → **6/64** |
| espacio exhaustivo | 9/65 → **11/64** | 9/65 → **12/64** |

**On the corpus `move` alone reaches the optimum from more starts than
`move+swap`**, and it already did unweighted (16 against 13); weights widen it (9
against 6). Both still reach it, so it is not a failure — the composite
alternates passes and can converge to a different local optimum from the same
start — but it does refute the intuition that a richer neighbourhood hits at
least as often, and the quantity it costs is exactly the hit rate F11's budget
depends on.

**And the tie the declaration rested on has broken.** `local_search.py` records
that `move+swap` was chosen over the cheaper option partly because the two came
out *indistinguishable* on the 29-rule instance — "same optimum, same first hit
at start 9, same 9/65" — which is true of the exhaustive space unweighted.
Under weights they separate there too, this time in `move+swap`'s favour: 12/64
against 11/64, first hit at start 4 against start 6.

Nothing here argues for changing the declared neighbourhood, and the reasoning
recorded next to it — that the two do not contain each other, and that the
failure Step 0 found sits behind a coordinated change of four or more positions —
is untouched by any of this. What the entry records is that the sample of size
one it called a tie is no longer a tie, and that on the corpus the declared
choice has the worse rate of the two.

---

## What the finished phases established

**P0.** Suite green at `7728d60` (315 tests, 1 skip: `openai` absent from the
system interpreter, expected without the venv). Hooks enabled.

**P1 — the weighted objective.** Threaded through `score_order`,
`best_insertion`, `move_pass`, `swap_pass`, `local_search` and `multistart`. The
cost gate was met: measured against the previous revision on the real instance
(577 rules, split 0, pure pool), alternating runs in one process to keep CPU
frequency and cold caches out of it, the unweighted path costs **+1.1%** —
budget was 10% — and returns identical orders and identical stats.

The first, non-alternating measurement said *−25%*, on code that had not been
touched. Anyone repeating this should alternate.

**P2 — the weighted step 0. PASSES**, and its verdict stands: F8, F9. 21 s.

The verdict stands, but **P2 turned out to prove less than it looked like it
proved** (F10). It validated the search against a known optimum, which is what
it claims to do; it did not validate the *construction of the optimum*, because
the instance that makes the optimum knowable is also the instance on which the
faulty count is correct. Worth carrying into P4: a gate certifies the thing it
varies, and the weights were not varied.

**P3 — harness parity. PASSES**, all three checks exact:

| check | published | today |
|---|---|---|
| `budget_and_balance.greedy` ≡ `order_search.greedy_order` | same order | same order |
| split 0, frac 1.0, pure: greedy test | 0.7487 | **0.7487** |
| idem, local search test | 0.8472 | **0.8472** |
| idem, coverage length | 559 | **559** |
| born_at over the exhaustive space | 0.3148 | **0.3148** |

The best start also reproduces: `aleatorio 13`, index 14. 34 s.

Two secondary observations, neither a finding yet:

- **F5's one data point.** That configuration — 65 starts at full supervision —
  took 32 s, about 0.49 s per start, consistent with the plan's probe of 0.29 s
  from the greedy and 0.48 s from a random start. It says nothing about partial
  budgets, which is where F5 lives.
- **F4 does not apply at full supervision**: LS 0.8472 against greedy 0.7487 on
  split 0. F4 is a prediction about *low* budget.
- The space masks build in **0.8 s**, against the plan's estimated 2.3 s.
