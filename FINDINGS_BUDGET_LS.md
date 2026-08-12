# Findings register — Audit Step 3 (`budget_and_balance` with the audited optimizer)

The register §5 of [`PLAN_BUDGET_LS.md`](PLAN_BUDGET_LS.md) makes mandatory. It
is a **working file**, not a record: at phase P7 it is folded into
[`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md), which is the record
that will own the Step 3 figures, and this file goes away with the plan.

**Opened 2026-08-12. Phases P0, P1, P2 and P3 are done; P4 onward are not**, so
every entry that depends on the label-budget curve is still open. §0 of the plan
carries no signature and P4 does not start without it (plan invariant 10).

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

P7 already plans a README row for the second; it must cover the first as well,
and whoever repairs F1 should take all of them in one pass. Recorded here so the
new drift is a decision rather than an oversight — which is the reason the lists
are pinned at all.

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

**P2 — the weighted step 0. PASSES.** Above, F8 and F9. 21 s.

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
