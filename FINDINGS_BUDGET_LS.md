# Findings register — Audit Step 3 (`budget_and_balance` with the audited optimizer)

The register §5 of [`PLAN_BUDGET_LS.md`](PLAN_BUDGET_LS.md) makes mandatory. It
is a **working file**, not a record: at phase P7 it is folded into
[`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md), which is the record
that will own the Step 3 figures, and this file goes away with the plan.

**Opened 2026-08-12. Closed 2026-08-13: all seven phases are done.** The figures
belong to [`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md), Step 3,
which owns them, and are indexed in [`STATUS.md`](STATUS.md). What is here is the
register of findings, several of which have no home in either.

**Two entries deserve reading before the rest.** F10 is a real defect in the
instrument, found by a blocking check Sergi called for after P2 had already
passed — the cleanest example in this branch of a gate passing for the wrong
reason. F2 is a published sentence withdrawn by a column nobody had thought to
compute.

**One procedural gap, and it is not mine to close.** §0 of the plan carries the
prediction and Sergi authorized P4 by saying it was signed, but
`PLAN_BUDGET_LS.md` is byte-identical to commit `6b8311b` and **contains no
signature line**. The agent is forbidden from editing §0 (plan invariant 10,
`CLAUDE.md` hard rule 2), so it is recorded here instead. The substance of the
rule held: the prediction was committed, immutable, before any number existed.

---

## The register

| id | finding | status |
|---|---|---|
| **F1** | `tests/test_provenance.py::ESCRITORES` and `tests/test_record_guard.py::LIBRES` under-list the modules that write records, against the README table `ESCRITORES` says it mirrors. | **CONFIRMED.** Reported, not fixed — see below. |
| **F2** | Greedy-today vs published, per row: the size of the 2026-08-06 tie-break fix on this record, never measured. | **CONFIRMED and larger than expected.** It changes sign twice and reaches **+0.0481** at 1%. |
| **F3** | Any configuration with `exhausted: true`. | **NONE.** 0 of 115 configurations, plus 390 weighted searches in P2. |
| **F4** | Configurations where LS is worse than the greedy on **test**. Expected at low budget (P-c). | **6 of 105, and not where predicted**: 0/1/3/2/0 by fraction, peaking at 10%, none at 1%. |
| **F5** | Per-fraction cost; in probing, LS from the greedy start was slower at partial budgets than at full supervision. | **REFUTED as stated.** Cost per configuration falls monotonically with the budget. |
| **F6** | Any class whose `ceiling` differs from the published `per_class_split0`. | **NONE.** All eight ceilings and class sizes identical. |
| **F7** | This work extends F1's drift: `peldano3.optimizer_check_wt` writes a record and is in neither pinned list nor the README table, and P6 will add `budget_and_balance_ls`. | **NEW, open for P7.** |
| **F8** | Pairwise `swap` alone cannot reach the weighted optimum either: 0 of 65 starts on both instances. | **NEW, confirmed in P2.** |
| **F9** | The optimum is never reached from the greedy start under weights — always from a random restart. | **NEW, confirmed in P2.** |
| **F10** | `class_counts_from_masks` returned the per-class **ceiling**, not the class size. It agrees with the truth only where every case is winnable, which is true of the hidden policy and false of the 577 rules. **The P2 gate could not see it.** | **NEW, CONFIRMED 2026-08-13. Fixed: the function now refuses; P5 uses `Counter(truth)`.** |
| **F11** | The restart budget's *"below 1e-8"* is calibrated at a 1-in-4 hit rate measured **without** weights. At the measured weighted rates it is **1.8e-3** on the corpus, five orders of magnitude worse. | **NEW, recomputed and recorded. Constant untouched.** |
| **F12** | `move+swap` reaches the optimum from **fewer** starts than `move` alone on the corpus, weighted and unweighted alike; and the tie on the space that the declaration rested on has broken. | **NEW, confirmed.** |
| **F13** | The balanced objective **overfits the smallest classes**: on split 0 the balanced LS scores worse than the balanced greedy on ONCALL_ESCALATION (2/3 vs 3/3) and SECURITY_INCIDENT (9/10 vs 10/10). | **NEW, observed in P5.** |
| **F14** | At full supervision **exactly one start of 65** reaches the best train score, in all five configurations. 64 restarts look tight precisely where the objective is informative. | **NEW, measured in P4.** |

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

## F2 — the tie-break fix changes sign twice, and is largest at 1% · CONFIRMED

The old record is pre-tie-break and untouched, so running the same greedy today
isolates the 2026-08-06 fix from the optimizer for the first time:

| frac | este registro | voraz hoy | **F2** |
|---|---|---|---|
| 100% | 0.7707 | 0.7713 | **+0.0006** |
| 25% | 0.7681 | 0.7630 | **−0.0051** |
| 10% | 0.7488 | 0.7342 | **−0.0146** |
| 5% | 0.7049 | 0.6883 | **−0.0166** |
| 1% | 0.5251 | 0.5732 | **+0.0481** |

At full supervision it is the +0.0002…+0.0006 the audit already knew about. In
the middle of the curve it is *negative* and an order of magnitude larger. At 1%
it is **+0.0481**, which is enough to withdraw a published sentence on its own:
FINDINGS3 §4's "at 1% it collapses to 0.5251, the arrival order without searching
for anything" describes the old tie-break, not the label budget.

Nobody had a reason to expect this, and it is only visible because the plan
insisted on three columns rather than two.

---

## F3 — the safety net was never hit · NONE

`exhausted: true` in **0 of 115** configurations, on top of the 390 weighted
local searches of P2. Strict improvement over a bounded integer is doing what the
module claims it does.

---

## F4 — where the local search loses on test · 6 OF 105, NOT WHERE PREDICTED

| frac | configuraciones con LS < voraz en test |
|---|---|
| 100% | 0 of 5 |
| 25% | 1 of 25 |
| 10% | **3 of 25** |
| 5% | 2 of 25 |
| 1% | **0 of 25** |

P-c expected the losses at the *smallest* budget. There are none there, and the
peak is at 10%. The reason is structural and is the same one that refuted P-c:
at 1% the objective has 1.4 distinct values across 65 starts, ties go to the
earliest index, index 0 is the greedy, and so the multi-start returns the
greedy's own order in 22 of 25 configurations. It cannot lose to something it is
returning.

The losses cluster where the objective is *partially* informative — enough to
move the search off the greedy, not enough for the move to generalize.

---

## F5 — cost falls with the budget · REFUTED AS STATED

The probe reported in the plan had LS from the greedy start slower at partial
budgets (~2 s) than at full supervision (~0.3 s), which would have made 25% the
most expensive row per configuration. Measured over the whole grid, per
configuration:

| frac | s/config | total |
|---|---|---|
| 100% | **33.0** | 165 s |
| 25% | 18.4 | 460 s |
| 10% | 12.8 | 321 s |
| 5% | 9.4 | 236 s |
| 1% | 3.4 | 85 s |

Monotone in the budget, with no inversion. 25% is the most expensive *row* only
because it is the first with 25 configurations instead of 5. The probe measured
one start on one split; the full grid does not reproduce it.

---

## F6 — the pool and the split did not move · NONE

All eight classes match the published `per_class_split0` exactly, in both `test`
and `ceiling`. ACCOUNT_MANAGER stays capped at 21 of 55, which was named as an
invariant in §0.

---

## F13 — the balanced objective overfits the smallest classes · NEW

On split 0 test, the balanced local search scores **worse** than the balanced
greedy on the two rarest classes, while scoring higher on the weighted train
objective it is maximizing:

| clase | test | techo | voraz balanceado | BL balanceado |
|---|---|---|---|---|
| ONCALL_ESCALATION | 3 | 3 | **3** | **2** |
| SECURITY_INCIDENT | 10 | 10 | **10** | **9** |

Those classes have 4 and 10 training cases. Maximizing macro-recall harder on a
handful of labels does not generalize, and the classes where it fails are exactly
the ones the objective exists to protect — the same two `CLAUDE.md` singles out
as the most critical and the rarest.

It is a small absolute number and one split, so it is recorded as an
observation, not a conclusion. But it is the direction that matters.

---

## F14 — 64 restarts are comfortable exactly where they are useless · NEW

Starts of 65 reaching the best train score, and distinct end scores:

| frac | en el mejor | puntuaciones distintas |
|---|---|---|
| 100% | **1.00** | 32.4 |
| 25% | 2.88 | 13.6 |
| 10% | 8.84 | 6.5 |
| 5% | 18.44 | 3.6 |
| 1% | **56.44** | **1.4** |

This is what the fields Sergi asked for were meant to expose, and the answer is
uncomfortable. **At full supervision exactly one start of 65 reaches the best
score, in all five configurations.** The result rides on a single shuffle, and
with no known optimum on this instance there is no way to tell whether a 66th
start would beat it. Where the objective is informative, 64 restarts look tight.

Where they look comfortable — 56 of 65 tied at 1% — they are comfortable because
the objective has stopped distinguishing anything, which is the opposite of
reassuring. F11's recomputed miss probability was measured on the 29-rule
instance and does not transfer here; this is what can be said instead.

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

The space masks build in **0.8 s**, against the plan's estimated 2.3 s.

**P4, P5 and P6 — the run.** One process, full run, canonical name, **1663 s**
(28 min) against the plan's estimate of 43. `code_dirty: false` at `a69890b`,
105 configurations in §1 and 10 in §2, saves after every fraction and every §2
split. Every blocking check passed: the three of P3, the P-a gate at 0.8530
exactly, and the P5 identity between §2's total rows and §1's full-supervision
rows.

**The predictions fell 2 held, 4 refuted, 1 short of its own threshold.** They
are answered one by one in FINDINGS_AUDIT Step 3. The one worth repeating here is
**P-g, which is refuted by its own reasoning being correct**: it bet that part of
the greedy's sacrifice of rare classes was search weakness rather than objective
conflict, and that this would make balancing buy *more*. The mechanism was right
and the consequence is the opposite — because the better optimizer rescues the
rare classes under the *total* objective (ACCOUNT_MANAGER 0 of 21 → 19 of 21),
there is far less left for balancing to buy, so the gain falls from +0.1695 to
+0.0576.

**P7 — documentation.** FINDINGS_AUDIT gains Step 3 and owns the figures;
FINDINGS3 §4 gains a dated erratum with the original table untouched beside it;
STATUS.md moves open item 1 into what is established and adds a seventh
withdrawal; README gains the command and three table rows, including the one F7
asked for; IDEAS.md marks the half-resolved note closed for
`budget_and_balance`. No figure was put in README, CLAUDE.md or IDEAS.md.
