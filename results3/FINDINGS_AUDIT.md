# Validity audit of rungs 3 and 4 — the optimizer

**This is not rung 5.** It is an audit of the search procedure that produced the
figures of rungs 3 and 4. The outcome may be *"the numbers move and so do the
conclusions"*, and that has to be writable without it looking like a setback.

Everything here costs **zero API calls**.

> **[NOTE 2026-08-10] This file was `PLAN_AUDIT.md` at the repo root** until the
> audit closed. It was written as a plan and executed in full; it is kept because
> it is the record that **owns** figures nothing else carries — the Step 0
> multi-start table, the 0.9455 / 0.9299 of orders perfect on the corpus, the
> cost of `move+swap` — and because it carries the prediction Sergi filled in by
> hand before the run (hard rule 2), which cannot be regenerated. Moved here so
> that a plan that is done stops reading as work pending. **The `peldano3/`
> scripts still name it `PLAN_AUDIT`**, in comments and in one printed line, and
> that was left standing on purpose. Those comments are accurate about what they
> describe: what the plan asked for, under the name it had when they were
> written. And `harness/provenance.py` hashes every `.py` under `peldano3/` into
> the `code_digest` that `optimizer_check.json`, `order_search_ls.json`,
> `order_search_ls_fullspace.json` and `sweep_ls.json` carry, so editing them for
> a cosmetic rename moves a figure-provenance signal while no figure moves.

---

## Why

Three independent signs point at the same weakness in the greedy search:

| sign | figure | where |
|---|---|---|
| noise **improves** the result — it acts as a random restart | 0.8337 against truth with 30% of labels falsified, vs 0.7574 with clean ones | `results4/FINDINGS4.md` |
| searching over the test set itself still leaves a large gap under the bound | 0.12 | `results3/FINDINGS3.md` |
| the tie-break changed the result at all | amplitude 0.011 across `PYTHONHASHSEED` | erratum of 2026-08-06 |

None of that is measurement noise: it is one weakness seen from three angles.
And it contaminates backwards — the 0.77 of rung 3 and the +0.067 of rung 4 both
come out of that searcher.

**What the tie-break fix already told us.** Fixing it moved the aggregate from
0.7711 to 0.7713 — two ten-thousandths. So the tie-break was responsible for
*variance*, not *bias*. The weakness is not instability in how ties are broken;
it is the algorithm itself. The greedy is genuinely myopic.

That raises the stakes: if the problem is myopia rather than noise, pairwise
swaps should recover a substantial share of the gap. If they recover almost
nothing, then the 0.9010 bound is loose and that has to be said.

---

## Step 0 — validate the optimizer before using it

**Blocking. Do this first.**

Run the local search on the **perfect hidden policy** (29 rules), where the
optimum is known: 1.0000 under the design order.

- Start from the greedy order, which under specificity-style arbitration is
  known to be far from optimal.
- Apply the local search.
- **Does it reach 1.0000?**

If the local search cannot recover a known optimum over 29 rules, it is
insufficient, and nothing it says about the 577 learned rules means anything.
**Stop and report.**

This is the same pattern as `harness.ceiling_check`: measure the ceiling of the
instrument before using the instrument to measure something else. It has saved
this project twice.

---

## Step 1 — local search over the 577 rules

Start from the greedy order, apply pairwise swaps until no improvement. Same
corpus (seed 17), same five splits, same protocol as `peldano3/order_search.py`,
so the numbers are comparable to the record.

Report train, test and the gap, against the existing references:

```
greedy (post tie-break fix)   test 0.7713 ± 0.0381
coverage bound                     0.9010     <- upper bound by per-case coverage,
                                                NOT a demonstrated global optimum
born_at                            0.5216
random (mean of 50)                0.4227
```

### The three questions this answers

1. **How much of the 0.77 → 0.90 gap does it recover?**
   A lot → the bound was reachable and rung 3 *underestimated* the LLM's material.
   Little → the bound is loose and the attribution of that gap must be corrected
   again.

2. **Does noise still help?** Re-run the rung 4 noise sweep with the new
   optimizer. If noise stops helping, that confirms it was acting as a random
   restart. If it still helps, there is something else going on.

3. **Does the asymmetry regime change survive?** This is the one that matters.
   The +0.067 vs +0.235 is the *only* claim rung 4 contributes, and it currently
   rests on a searcher we know is weak. If a serious optimizer extracts much more
   from scarce, asymmetric labels, that figure rises and the "regime change"
   softens. **It might not survive.**

---

## Step 2 — re-run rungs 3 and 4

Only after Steps 0 and 1 are reported and approved.

As a **pull request**, so the diff shows exactly what moved and `_env` records
which code produced it. The previous figures stay in the history rather than
being replaced.

Because the tie-break fix is already in the working tree and unexecuted, the
same diff separates two effects that would otherwise be confounded:

- what the **tie-break** moved (expected: ~0.0002, i.e. nothing)
- what the **algorithm** moved (unknown)

That separation is the whole reason the fix was left unexecuted. Do not lose it.

Dated errata go in `results3/FINDINGS3.md` and `results4/FINDINGS4.md`, in place,
with the original text visible — the convention already established on
2026-08-06.

---

## Prediction — fill in before running

Two parts, because they are now separable. Sergi fills this in; the agent does
not (hard rule 2).

Filled in by Sergi on August 8, 2026, before running anything. Transcribed
verbatim; the agent did not author it (hard rule 2).

| question | prediction | result |
|---|---|---|
| Does local search reach 1.0000 on the perfect policy? (yes/no) | yes | **yes**, with multi-start — **no** in one run (2026-08-08) |
| Test e2e over the 577 rules (greedy gives 0.7713, bound 0.9010) | 0.82 | **0.8530** ± 0.0062 (2026-08-08) |
| Does the asymmetry regime change survive? (yes/no) | no | **no** — the 3.5x gap becomes 1.6x (2026-08-08) |

**If the first one fails, the other two mean nothing.** Same lesson as Step 0 of
rung 1, applied to the optimizer instead of the engine.

Stopping threshold: 0.78 on row 2 — recovering less than 20% of the 0.13 gap
means the greedy was not the main problem, and the weakness lies in the bound or
in the material rather than in the search.

Row 1 is blocking: if local search fails to recover a known optimum over 29
rules, rows 2 and 3 mean nothing and the audit stops there.

Divergence from Claude: Claude said the asymmetry regime change "might not
survive" without committing. Sergi predicts it does not survive.

**Step 0, first run — FAILED.** August 8, 2026. One run from the greedy start,
as this plan specified. Both neighbourhoods missed, three orders of magnitude
apart: pairwise swaps stopped at 0.9356 over the exhaustive space (8,660 wrong
cases of 134,400), relocation at 0.999851 (20 wrong). The residue was a single
inverted relation — H26 at rank 24 beating H23 at rank 27, against a design
order that puts H23 first — and it was a genuine local optimum: the best single
swap and the best single relocation both gave +0, and no permutation of three
positions improved it. Repairing the inversion in isolation costs accuracy
(swapping the pair, −190 cases; lifting H23, −40), which is what made it a basin
rather than an oversight.

**Step 0, second run — PASSES.** Sergi authorized changing the instrument. The
repair is the one the failure pointed at, restarts, and not a wider
neighbourhood, which would have been tuned to the symptom. Constants declared in
`local_search.py` and fixed before the run: seed 17, 64 random starts, plus the
greedy at position 0 so the multi-start can never return worse than the single
run. The criterion is 1.0000 over the **exhaustive space**; the corpus is
measured and validates nothing.

```
                        one run   multi-start   1st hit   reach it
espacio · move         0.999851      1.000000         9       9/65
espacio · swap         0.935565      0.994196         —       0/65
espacio · move+swap    0.999851      1.000000         9       9/65
corpus  · move         0.999500      1.000000         4      16/65
corpus  · swap         0.957500      0.985000         —       0/65
corpus  · move+swap    0.999500      1.000000         4      13/65
```

**Pairwise swaps never reach it**, with or without restarts: 0/65 on both
instances, 780 wrong cases at best over the exhaustive space. That is a result
about the method, which is what this plan asked for, and it stays in the record.

**The corpus would have certified a wrong instrument twice over.** It hides the
swap failure — 0.9575 there against 0.9356 over the space — and worse, the
orders that score a perfect 1.0000 on its 2000 cases score only **0.9455** and
**0.9299** over the full space. Fitting the corpus exactly is not recovering the
policy. The order found over the exhaustive space scores 1.0000 on both, and is
not the design permutation: it is a different one inducing the same decision
function, which is what policy equivalence means here.

---

## Step 1 result — August 8, 2026

`results3/order_search_ls.json` · `results4/sweep_ls.json`. Same corpus, same
seed 17, same five splits, same objective, same channel. Only the search changed.

**The greedy baseline reproduces the record exactly**, which is what makes the
rest comparable: 0.7713 ± 0.0381 on test against the 0.7713 this plan cites, and
0.7775 train against the record's 0.7779. The tie-break fix is confirmed worth
+0.0002 on test — the separation this plan was built to preserve, now measured.

```
pool puro, 5 particiones      train              test               GAP
voraz (registro)          0.7775±0.0278     0.7713±0.0381     0.0062
busqueda local            0.8695±0.0052     0.8530±0.0062     0.0165±0.0098

pool hibrido
voraz                     0.7792±0.0110     0.7460±0.0069
busqueda local            0.8128±0.0075     0.7734±0.0097     0.0394±0.0153
```

**Answer to question 1: a lot.** The gap was 0.1297 (0.9010 − 0.7713) and the
optimizer recovers **+0.0817, 63% of it**. The greedy was the main problem and
the bound was not loose. Overfitting of the order stays small — the gap grows
from 0.006 to 0.017, an eighth of the recovered accuracy.

**Answer to question 3: the regime change does not survive.**

```
asimetria    registro   ahora    etiquetas
      1.0    +0.2348   +0.3273        1010
      0.5    +0.2738   +0.3274         751
     0.25    +0.1901   +0.3115         622
      0.1    +0.0969   +0.2818         544
      0.0    +0.0671   +0.2011         498
```

The record's cliff between 0.25 and 0.1 is gone. What is left is a gradual
decline, and the symmetric-to-asymmetric ratio falls from **3.5x to 1.6x**. The
anchor cell that carried the claim moves from 0.5887 to **0.7227**: three times
the margin the record credited to a realistic channel. The rung 4 headline —
"not a gradual limit but a change of regime" — was substantially an artifact of
a weak learner starved of restarts.

What is NOT touched: the structural claim of FINDINGS4 section 3, that the
volume of signal is proportional to the error rate of the observed system. That
is a property of the channel, not of the learner, and no optimizer changes it.

**Answer to question 2: noise has stopped helping.**

```
ruido    registro   ahora     desv
  0.0      0.7564  0.8489   0.0023
  0.1      0.8163  0.8502   0.0070
  0.3      0.8171  0.8318   0.0104
  0.5      0.7004  0.7812   0.0160
```

In the record, falsifying 10% of the labels bought +0.060 and 30% bought +0.061,
which is impossible as an effect of supervision and is what made it diagnostic.
Now 10% is +0.0013 — flat, inside its own spread — and 30% and 50% degrade
monotonically. The noise was acting as a random restart, exactly as suspected.
Once the restarts are declared instead of being smuggled in through the channel,
the anomaly disappears and the sweep reads as the degradation curve it should
always have been. FINDINGS4's refusal to read those curves as degradation was
the right call about the wrong mechanism.

The re-run reproduces the anchors and the asymmetry cells digit for digit, and
`ruido e=0` returns the `simetrica a=1` figures exactly, as the same channel
configuration must.

**The exhaustive space says something the corpus cannot.** The same orders,
scored over all 134,400 cases:

```
                       corpus test   espacio    cota espacio
voraz                       0.7713    0.4931          0.8784
busqueda local              0.8530    0.6105          0.8784
born_at                     0.5216    0.3148
aleatorio                   0.4251    0.3768
```

The optimizer improves the space score too, 0.4931 to 0.6105, so the gain is not
purely corpus-fitting. But against the space bound the shortfall is **0.268**,
five times the 0.048 that remains on corpus test. And **born_at is worse than
random over the real case space** (0.3148 against 0.3768) while beating it on the
corpus (0.5216 against 0.4227): rung 3's remark that "the arrival order already
scores 0.52" is a corpus artifact. The early-born rules are defaults fitted to
the common distribution.

**The direct search over the exhaustive space splits that 0.268 in two.**
Searching the order over the whole space, with no split — the analogue of rung
3's "search over the test set itself" — gives 0.7905 on the pure pool and 0.7557
on the hybrid:

```
pool puro, sobre los 134,400 casos
cota por cobertura                              0.8784
busqueda directa sobre el espacio               0.7905     resto 0.0879
orden buscado sobre train del corpus            0.6105
voraz del registro                              0.4931
aleatorio                                       0.3768
born_at                                         0.3148
```

So of the 0.268: **0.180 is fitting to the corpus distribution** — the order is
searched over a 2000-draw sample and loses that much when carried to the whole
space — and **0.088 survives even when the search sees every case**. Two thirds
distribution, one third search or slack in the bound.

That 0.088 is what FINDINGS3's erratum of 2026-08-06 left open: *"how much of it
is greedy-search weakness and how much is an unattainable bound remains
unmeasured."* It is now partly measured. Rung 3's greedy left 0.1187 under the
bound searching over its own test set; this optimizer leaves 0.0879 searching
over the entire space. The residue shrank by a quarter and did not close, which
is evidence that the coverage bound is somewhat loose — evidence, not proof,
because a heuristic that fails to reach a bound never distinguishes the two.

Cost of that diagnostic: 1375 s for the pure pool and **8471 s for the hybrid**,
which is where the 8x hybrid penalty really shows.

**Cost of `move+swap` at 577 rules**, as required: corpus protocol 1997 s,
rung 4 anchors and asymmetry 1253 s. Per search, 0.6 s on the pure pool and
4-5 s on the hybrid — the hybrid is ~8x worse because subsumption leaves 181 of
the 577 rules matching nothing on train, and the swap scan cannot skip pairs
involving them. `move` alone reached an identical train score in probing at a
twentieth of the cost. The neighbourhood is affordable here and would not be at
another order of magnitude of rules.

---

## Step 3 result — August 13, 2026

`budget_and_balance` was the last figure of rungs 3 and 4 produced entirely by
the superseded greedy, and the source of *"50 labels are enough to order"* — the
premise rung 4 was opened on. It has now been re-measured with the declared
optimizer, under the plan `PLAN_BUDGET_LS.md`, and **this section owns the new
figures**.

Same corpus of 2000 at seed 17, same five splits, same pure pool, same
fractions, same draw seeds, same simple random subsampling, same evaluation over
the whole test half. Only the optimizer changed. Record:
[`budget_and_balance_ls.json`](budget_and_balance_ls.json). 1663 s, zero API
calls, one process.

**Provenance, since one flag reads badly on its own.** That record carries
`code_dirty: false` at `a69890b`, which is the flag that matters: the commit
identifies the code that ran. It also carries `git_dirty: true`, and that is
**only** `README.md` and `IDEAS.md`, edited during the run while the P7
documentation was being written. Neither is under `CODE_ROOTS`, neither is read
by anything, and no input to the figures was uncommitted. The two flags are split
precisely so this case is distinguishable from a code change
(`harness/provenance.py`); a `true` with no explanation beside it is not
traceability, so this is the explanation.

**How the step was executed, and one procedural gap.** Seven phases, each
committed before the next: the plan first, so the phases are measured against
something already on the record; then the weighted objective; then two blocking
gates; then the run; then this. Two things are worth carrying:

- **The unweighted path did not slow down.** Threading class weights through
  `score_order`, `best_insertion`, `move_pass`, `swap_pass`, `local_search` and
  `multistart` costs **+1.1%** when `wt=None`, measured against the previous
  revision on the real instance with the two revisions alternating in one
  process, and returns identical orders and identical stats. The budget was 10%.
  The first, non-alternating measurement said *−25%* on code that had not been
  touched; anyone repeating this should alternate.
- **Harness parity was checked before any figure.** Split 0 at full supervision
  on the pure pool reproduces `order_search_ls.json` exactly — greedy test
  0.7487, local search 0.8472, coverage length 559, and even the winning start,
  `aleatorio 13` at index 14 — and born_at over the exhaustive space gives
  0.3148. The two greedy implementations produce one order. All of it is in the
  record's `checks`.

**§0 is signed, and the signature arrived after the run.** For most of this step
the file carried the prediction and no signature line: Sergi authorized P4 in
conversation, before it was launched, while `PLAN_BUDGET_LS.md` stayed
byte-identical to the commit that introduced it. He added the line on
2026-08-13, after the figures existed, and it says so itself — the prediction was
drafted on 2026-08-12, was immutable in `6b8311b` before any number existed, and
§0 was never edited in between, which `git log -p PLAN_BUDGET_LS.md` verifies.
The substance of hard rule 2 held; the file was late in showing it.

**One traceability defect, and it is the agent's.** That signature reached the
repository inside commit `b9b0f5f`, whose subject is *"Run the start-budget
diagnostic over all five splits, not one"* and whose message does not mention it:
a `git add -A` swept the working-tree edit in alongside the code change. Anyone
auditing the plan with `git log --oneline -- PLAN_BUDGET_LS.md` therefore lands
on a commit about a diagnostic, not on a signing event. Nothing was altered and
the diff is honest, but the signing is the one act in this step that should have
had a commit of its own, and staging by wildcard is what cost it.

*Addendum, 2026-08-14.* The route this took is now closed at the cheapest point:
`.githooks/pre-commit` refuses a commit that stages `PREDICTION.md` or a root
`PLAN_*.md` together with any other file, and hard rule 2 of `CLAUDE.md` states
the norm the guard only partly enforces — the hook is skipped by `--no-verify`,
so it stops the careless version of this defect and nothing that is trying to get
past it. Neither the figures above nor the commit under discussion change; what
changes is that the same wildcard would now fail loudly.

**A blocking gate was run first, and it found a defect.** The class-weighted
objective got its own step 0 (`optimizer_check_wt.py`): the hidden policy in
design order maximizes every non-negative-weight objective at once, so the
weighted optimum is `L × (number of classes)` by construction. `move+swap`
reaches it — 4 starts on the exhaustive space, 12 of 64 — and pairwise `swap`
alone does not, 0 of 64 on both instances, the same failure shape step 0 found
unweighted. What the gate could **not** see is recorded below.

### The three columns

The old record is deliberately pre-tie-break and is untouched, so for the first
time the 2026-08-06 tie-break fix and the optimizer are separated on this
record. Corpus test, pure pool, 5 splits × 5 draws (1 draw at full supervision):

```
                 PUBLICADO   VORAZ HOY               BUSQUEDA LOCAL HOY
 frac   etiq     (pre-des.)  (post-des.)   F2      media      sd     min     max   espacio
 100%   1005       0.7707      0.7713   +0.0006   0.8530  0.0062  0.8472  0.8640   0.6105
  25%    251       0.7681      0.7630   -0.0051   0.8227  0.0179  0.7719  0.8462   0.5103
  10%    100       0.7488      0.7342   -0.0146   0.7771  0.0308  0.7206  0.8373   0.4876
   5%     50       0.7049      0.6883   -0.0166   0.7410  0.0478  0.5769  0.8145   0.4487
   1%     10       0.5251      0.5732   +0.0481   0.5767  0.0710  0.4874  0.7276   0.3310
```

**The tie-break fix changes sign twice** (column F2) and is largest where the
record's headline claim lives: at 1% it is worth **+0.0481** on its own. So
FINDINGS3 §4's *"at 1% it collapses to 0.5251, which is the arrival order
without searching for anything"* is substantially a tie-break artifact — the
greedy alone, correctly tie-broken, gives 0.5732 there, and the collapse is
shallower than published before any optimizer is involved.

### Why 64 restarts behave completely differently across the curve

With a fixed seed there is no hit rate to estimate and no known optimum to hit,
so what is recorded is how the 65 starts spread:

```
 frac    arranques en el mejor    puntuaciones distintas (de 65)
 100%           1.00                        32.4
  25%           2.88                        13.6
  10%           8.84                         6.5
   5%          18.44                         3.6
   1%          56.44                         1.4
```

This is the mechanism the prediction bet on, measured directly. At full
supervision **exactly one start of 65 reaches the best train score** in every one
of the five configurations, and 32 distinct scores come out: the objective
separates orders finely and the answer rides on a single shuffle. At 1% the
train objective has 1.4 distinct values and 56 of 65 starts tie at the top — it
has stopped discriminating between orders altogether.

**And that is what decided P-c.** Ties between starts go to the earliest index,
and index 0 is the record's greedy (D2). At 1% the greedy start therefore wins
**25 of 25** configurations, and the order returned is *identical* to the
greedy's in 22 of them. The multi-start cannot lose to the greedy at low budget
because at low budget it usually **is** the greedy.

### The predictions, one by one

| # | verdict | measured |
|---|---|---|
| **P-a** | **HOLDS** (gate) | 0.8530 ± 0.0062, min 0.8472, max 0.8640, space 0.6105 — reproduces `order_search_ls.json` digit for digit. |
| **P-b** | **REFUTED** | Gains +0.0817, +0.0597, +0.0429, **+0.0527**, +0.0035. Not monotone — it grows from 10% to 5%, the stated refutation — and at 5% it is +0.0527 against the predicted ≤ +0.02. Only the "≥ +0.07 at 100%" clause holds. |
| **P-c** | **REFUTED** | At 1% LS 0.5767 against greedy 0.5732: LS ≥ greedy, which is the refutation verbatim. |
| **P-d** | **NOT REFUTED, threshold missed** | Ratio 5%/100% falls from the published **0.9147** to **0.8687**. Below the 0.90 that would refute it, above the 0.85 it predicted. Greedy-today's own ratio is 0.8924. And the direction depends on the denominator — see the FINDINGS3 §4 erratum, where the same budget *improves* from 78.2% to 82.2% as a fraction of the coverage bound. |
| **P-e** | **REFUTED** | LS sd 0.0478 at 5% (predicted > 0.0535) and 0.0710 at 1% (predicted > 0.0628). Against greedy-today in the same run — 0.0590 and 0.0739 — the LS sd is **smaller at both**, which is the refutation verbatim. Against the published greedy it is smaller at 5% and larger at 1%. |
| **P-f** | **HOLDS** | Space/corpus ratio 0.7157, 0.6203, 0.6275, 0.6055, 0.5740. Every row far below its corpus figure and low budgets losing proportionally more, with one inversion between 25% and 10%. |
| **P-g** | **REFUTED** | Balancing costs the LS **+0.0274** against the published 0.0557 — less, as predicted — but buys **+0.0576** in balanced accuracy against the published +0.1695. The gain moved the other way, which is the refutation. |

**P-b, P-c and P-e are not three independent failures. They are one fact about
the instrument, seen three times.** §0 bet that a stronger optimizer would buy
most where the objective is informative and could *actively lose* where it is
not, "maximising harder the thing that has stopped being a proxy". The first half
is right. The second never happens, and cannot, because of how the instrument is
built:

1. **The objective saturates.** Distinct train scores across the 65 starts fall
   32.4 → 13.6 → 6.5 → 3.6 → **1.4**. At 10 labels the train objective assigns
   essentially one value to every order it is shown.
2. **The multi-start degenerates into the greedy.** Ties between starts go to the
   lowest index and index 0 is the record's greedy (D2). At 1%, 56 of 65 starts
   tie at the top, the greedy start wins **25 of 25** configurations, and the
   returned order is *identical* to the greedy's in 22 of them.
3. **So the tie-break at index 0 acts as a regularizer.** Where the objective
   stops discriminating, the search stops moving, and what it returns is the
   baseline. That is why P-c fails (LS cannot be worse than something it is
   returning), why P-b's gain flattens to +0.0035 instead of going negative, and
   why P-e finds *less* dispersion rather than more: the low-budget rows are
   partly the greedy's own variance, not the search's.

**F4 is the shape of the actual risk, and it is not at the bottom of the curve.**
Configurations where the local search ends up worse than the greedy on test: 0 of
5 at 100%, 1 of 25 at 25%, **3 of 25 at 10%**, 2 of 25 at 5%, **0 of 25 at 1%**.
The danger is not where the objective is noise — there the instrument declines to
act — but in the middle, where it is informative enough to move the search off
the greedy and not informative enough for the move to generalize.

The prediction's mechanism was therefore right about the objective and wrong
about the consequence, because it did not account for its own D2. A design
decision taken for a different reason — start 0 is the greedy, so the comparison
is honest in one direction — turned out to determine the entire shape of the
low-budget half of the curve.

The invariants held: LS ≥ greedy on **train** in all 115 configurations, no
configuration hit the `max_rounds` safety net, every per-class `ceiling` equals
the published one, and ACCOUNT_MANAGER stays capped at 21 of 55.

**P-g is refuted by its own mechanism being right.** It reasoned that part of
the greedy's sacrifice of rare classes was search weakness rather than objective
conflict. That is exactly what happened — and it is why the gain shrank. Under
the **total** objective the local search already reaches 0.6299 balanced accuracy
where the greedy reached 0.5201, so balancing has far less left to buy. On split
0 the greedy under the total objective gets **0 of 21** attainable
ACCOUNT_MANAGER cases and the local search gets **19 of 21**, with no balancing
at all.

### §2 — the balanced objective, on both surfaces

```
 objetivo   optimizador   e2e test   acierto bal.   e2e espacio   MACRO-RECALL espacio
 total       voraz          0.7713      0.5201        0.4931            0.5393
 total       BL             0.8530      0.6299        0.6105            0.6271
 balanceado  voraz          0.7150      0.6936        0.6420            0.6486
 balanceado  BL             0.8256      0.6875        0.6573            0.6472

 coste de balancear / ganancia en acierto balanceado / ganancia en macro espacio
   voraz   +0.0563   +0.1735   +0.1093
   BL      +0.0274   +0.0576   +0.0201
```

Greedy-today reproduces the published §2 to the digit on the balanced row
(0.7150 and 0.6936), which is what makes the comparison readable.

All four macro-recall figures are in the record, for **both objectives × both
optimizers**, in `objective_comparison[objetivo][quien].macro_space`, and per
split in `objective_runs` as `greedy_macro_space` and `ls_macro_space`. It is a
fourth measurement rather than a restatement of the third: `e2e espacio` weights
every one of the 134,400 cases equally, macro-recall weights every *class*
equally on that same uniform surface.

**On the uniform measure the balanced objective almost stops paying under a good
optimizer.** Macro-recall over the exhaustive space: balancing buys the greedy
+0.1093 and the local search **+0.0201**, and the balanced local search (0.6472)
does not beat the balanced greedy (0.6486). The corpus is long-tailed and the
space is uniform, so this is the surface where the two objectives had to diverge
most — and it is where the optimizer absorbs almost all of the difference.

**The balanced objective overfits the smallest classes.** On split 0 the balanced
local search scores *worse* than the balanced greedy on the two rarest classes —
ONCALL_ESCALATION 2 of 3 against 3 of 3, SECURITY_INCIDENT 9 of 10 against 10 of
10 — while scoring higher on the weighted train objective. With 4 and 10 training
cases, maximizing weighted train recall harder does not generalize.

### Is 0.8530 converged? No — and where more starts help train, they hurt test

The `n_at_best = 1.00` above is not a curiosity, it is a warning: a figure that
one start of 65 reaches is a maximum over draws. All five splits at full
supervision, run again with 128 and 256 random starts — nested by construction,
the larger budgets begin with the record's 64 — give
([`start_budget_check.json`](start_budget_check.json)):

```
 part  arranques    train  (bruto)     test   espacio   en el mejor   distintas
    0         65   0.8786      883   0.8472    0.6033             1          36
    0        129   0.8786      883   0.8472    0.6033             1          46
    0        257   0.8796      884   0.8442    0.5776             1          53
    1     65/129/257  0.8697   874   0.8472    0.5835             1     33/45/49
    2     65/129/257  0.8626   879   0.8522    0.6604             1     32/44/51
    3     65/129/257  0.8670   867   0.8640    0.5868             1     26/34/39
    4         65   0.8697      868   0.8543    0.6183             1          35
    4        129   0.8727      871   0.8473    0.6048             1          44
    4        257   0.8727      871   0.8473    0.6048             1          47
```

**The best train score moves in 2 of the 5 splits** — split 0 at 256 starts,
split 4 already at 128. So 0.8530 is a maximum over draws rather than a converged
optimum, and on this instance nothing can say whether a 258th start would move it
again. In the other three splits it does not budge at four times the budget,
which is evidence of local convergence and not proof of it.

**Where the train score improves, test and space both get worse — 2 of 2.**
Split 0: test 0.8472 → **0.8442**, space 0.6033 → **0.5776**. Split 4: test
0.8543 → **0.8473**, space 0.6183 → **0.6048**. Mean where it moves: **−0.0050**
on corpus test and **−0.0196** on the exhaustive space. The direction is
consistent; the *frequency* is 2 in 5, so split 0 was not a fluke of sign but it
was the more extreme of the two.

This is §0's own mechanism — maximising harder something that has stopped being a
proxy — appearing at **full supervision** when the restart budget grows, rather
than at low budget where §0 expected it. At 1005 labels the train objective is
still a good proxy at the scale of 0.08 and already a bad one at the scale of
0.001.

**One thing is universal across all 15 rows: `n_at_best` is 1.** At 65, 129 and
257 starts, in every split, exactly one start reaches the best train score. The
sample never concentrates; only the spread grows (26–36 distinct scores at 65,
39–53 at 257). Whatever budget this instrument is given, its answer rests on a
single shuffle.

**`MULTISTART_STARTS` stays 64 because it was declared before the runs that used
it.** That is the entire reason, and it is deliberately not contingent on
anything in the table above. An earlier draft of this section added *"the more so
since 256 came out worse on both evaluation surfaces"*, which is an argument that
must not be made: it picks a hyperparameter by reading the test and space
figures, which is rule 6 with its sign reversed and no better for happening to
support the constant already in force. The 256-start result is a fact about the
instrument, not a reason for a constant.

What the diagnostic produces is a caveat, and it reaches further than this
record: **`order_search_ls` published the 0.8530 with the same optimizer at the
same budget**, and `sweep_ls` did the same for rung 4. Those figures are what the
declared instrument returns; they are not optima, and they are bounded by a draw.
Recorded in `STATUS.md` beside the figure, which is where a reader meets it.

### What it costs, and what it does not settle

1663 s for 115 configurations on the pure pool, against ~2 min for the greedy
that produced the original record. The exhaustive-space transfer added 0.9 s to
build the masks and about a millisecond per order scored.

Per configuration the cost falls monotonically with the budget — 33.0 s at 100%,
18.4 at 25%, 12.8 at 10%, 9.4 at 5%, 3.4 at 1% — with no inversion. The probe
reported in the plan had it the other way round, with partial budgets slower than
full supervision; that probe was one start on one split and the full grid does
not reproduce it.

Not settled: whether the coverage bound is loose (Step 1's open question is
untouched here), and whether any of this survives on the hybrid pool, which
`budget_and_balance` never used and which is ~8× slower.

### The register of findings

The plan required a findings register. It was kept as a working file during the
run and is folded in here, because figures have exactly two homes — the FINDINGS
that owns them and `STATUS.md` — and a third document carrying them is the
duplication this project keeps having to undo.

| id | finding | status |
|---|---|---|
| **F1** | `tests/test_provenance.py::ESCRITORES` and `tests/test_record_guard.py::LIBRES` under-list the modules that write records, against the README table `ESCRITORES` says it mirrors. | **CONFIRMED.** Reported, not fixed. |
| **F2** | The 2026-08-06 tie-break fix, per row: never measured on this record. | **CONFIRMED**, changes sign twice, +0.0481 at 1%. Above. |
| **F3** | Any configuration hitting the `max_rounds` safety net. | **NONE**, 0 of 115, plus 390 weighted searches in P2. |
| **F4** | Configurations where the local search is worse than the greedy on test. | **6 of 105**, peaking at 10%, none at 1%. Above. |
| **F5** | Per-fraction cost: the plan's probe had partial budgets slower than full supervision. | **REFUTED as stated.** Cost falls monotonically. |
| **F6** | Any class whose `ceiling` differs from the published `per_class_split0`. | **NONE.** All eight identical. |
| **F7** | This work adds record writers absent from both pinned lists and the README table. | **Resolved for the README**, which now carries all three rows. The pinned lists are F1 and stay unfixed. |
| **F8** | Pairwise `swap` alone cannot reach the weighted optimum either. | **CONFIRMED**, 0 of 64 on both instances. |
| **F9** | Under weights the optimum is never reached from the greedy start. | **CONFIRMED**, always from a restart. |
| **F10** | `class_counts_from_masks` returned the per-class **ceiling**, not the class size. **The P2 gate could not see it.** | **CONFIRMED and fixed** before any figure was produced. |
| **F11** | The restart budget's *"below 1e-8"* is calibrated to an unweighted 1-in-4 rate. | **RECOMPUTED.** Constant untouched. |
| **F12** | `move+swap` reaches the weighted optimum from fewer starts than `move` alone on the corpus. | **CONFIRMED.** |
| **F13** | The balanced objective overfits the smallest classes. | **OBSERVED.** Above, and in the FINDINGS3 §3 erratum. |
| **F14** | At full supervision exactly one start of 65 reaches the best train score. | **MEASURED.** Above. |
| **F15** | 0.8530 is not converged: more starts improve train in 2 of 5 splits, and in 2 of those 2 the test and space scores fall. | **MEASURED over five splits.** Above. |
| **F16** | The tie-break moves exactly one cell of the per-class table: SECURITY_INCIDENT under the total objective, 7 → 4. | **CONFIRMED.** FINDINGS3 §3 erratum. |
| **F17** | *"50 labels are practically free"* changes direction with the denominator. | **CONFIRMED.** FINDINGS3 §4 erratum. |

**F10, in full, because it is the one that nearly cost a figure.** The weighted
objective needs the number of cases per class. The first implementation derived
it from the masks — the union of `W[r]` over the rules of each action — to keep
the module free of the oracle. That quantity is the per-class **ceiling**: it
counts the cases of a class that *some correct rule matches*, and equals the
class size only where every case is winnable. On split 0's train, over the 577
rules:

```
clase                   Counter(truth)   de mascaras   falta
T2_TECHNICAL                       362           357       5
SELF_SERVICE_DEFLECT               253           237      16
BILLING_SPECIALIST                 135           135       0
T1_GENERAL                         127           127       0
T3_ENGINEERING                      60            19      41
ACCOUNT_MANAGER                     54            18      36
SECURITY_INCIDENT                   10            10       0
ONCALL_ESCALATION                    4             4       0
total                             1005           907      98
```

The shortfall lands on the two classes FINDINGS3 §2 records as materially broken.
Weighting by `L/19` instead of `L/60` inflates T3_ENGINEERING 3.2× and
ACCOUNT_MANAGER 3.0× — exactly the classes the balanced objective exists to
protect, in the direction that flatters it. §2 would have compared the record's
greedy, weighted by `1/Counter(truth)`, against a search weighted by a ceiling,
and reported the difference as the optimizer.

**The gate could not catch it, and that is the general lesson.** On the hidden
policy every case is covered by its own rule, so ceiling and class size coincide
and the derivation is exact. Step 0 reaching `L × classes` was evidence for the
*search* and none at all for the *counting*: the instance that makes an optimum
knowable was also the instance on which the defect is invisible. A gate certifies
what it varies, and the weights were not varied. Found by a check on the real
instance, called for after P2 had already passed.

`class_counts_from_masks` is deleted; the module reads `true_action` and is
declared in `tests/test_oracle_separation.py`. Avoiding the oracle import bought
nothing and cost a defect.

**F8, F9 and F11 — the weighted gate.** Over the 29 rules of the hidden policy,
balanced accuracy as a fraction of the known optimum:

```
instancia            move            swap             move+swap
corpus         1.000000  9/64   0.995523  0/64   1.000000   6/64
espacio        1.000000 11/64   0.992092  0/64   1.000000  12/64
```

The design order is a fixed point of all three neighbourhoods on both instances.
Pairwise swaps fail exactly as they did unweighted in Step 0. The greedy at index
0 hits in none of the six configurations, so every hit is a restart, and the
unweighted greedy is a poor start for the balanced objective — 0.4346 balanced on
the corpus against 0.7365 unweighted e2e.

`local_search.py` justifies its 64 starts by *"at a one-in-four rate, 64 starts
miss altogether with probability 0.75\*\*64, below 1e-8"*. That rate was measured
**unweighted**. At the weighted rates, over the 64 random starts, with exact
Clopper-Pearson intervals:

```
instancia · vecindario    aciertos   tasa     IC95 tasa        fallo    IC95 fallo
corpus · move+swap           6/64   0.0938  [0.035, 0.193]   1.8e-03  [1.1e-06, 1.0e-01]
espacio · move+swap         12/64   0.1875  [0.101, 0.305]   1.7e-06  [8.0e-11, 1.1e-03]
```

against an inherited `0.75**64` of `1.01e-08` — marginally above the "below 1e-8"
the comment claims. On the corpus the declared neighbourhood is five orders of
magnitude from it, with an interval reaching 0.10. The point estimate reuses the
draws that produced the rate, so the interval is the honest part; and this is 29
rules, not the 577 of §1 and §2, where no rate can be measured at all. **The
constant is not touched:** what is recomputed is the claim made about it.

**F12.** `move` alone reaches the weighted optimum from more starts than
`move+swap` on the corpus — 9/64 against 6/64, and already 16/65 against 13/65
unweighted. On the exhaustive space the tie that `local_search.py` cites when
declaring the neighbourhood ("same first hit at start 9, same 9/65") has broken
under weights, this time in `move+swap`'s favour, 12/64 against 11/64. Nothing
here argues for changing the declared neighbourhood; what it records is that the
sample of size one called a tie is no longer one.

**F1 and F7 — a pinned list that stopped mirroring its source.** `ESCRITORES`
says in its own comment that it mirrors the README's overwrite table, and omits
`peldano3.optimizer_check`, `peldano3.order_search_ls` and `peldano4.sweep_ls`,
all three of which the README lists. `LIBRES` omits the same three; its other
absences — `run_experiment`, `run2`, `compare_runs`, `note_audit` — are not drift,
since those are guarded on purpose and `LIBRES` is the list of writers that must
*not* import the guard. No test catches the omission: one iterates the pinned
list, so an absent module is never checked, and the other discovers new writers
but only asks that they carry `_env`, which they all do.

Reported and deliberately **not** fixed here: it predates this work, and folding
a repair into a branch measuring something else would make the diff say two
things at once. This branch adds three more writers to the same gap; the README
table now carries all of them, the pinned lists still do not.

---

## Deliberately out of scope

- **ILP as a competitor.** Still the uncomfortable question — if it induces
  comparable rules with no LLM, what is the proposer for? But comparing against a
  number you know is unstable says little. After this audit.
- **Online order.** Only meaningful if rung 4's Step A survives the optimizer.
- **Why the proposer partitions instead of stratifying.** The most interesting
  open question from rung 2 and the only one with no measurement behind it. It is
  expensive and depends on nothing above — it can wait.

---

## Rules in force

Seed 17. Oracle separation. Frozen files untouched. Report bad numbers without
fixing them. Snapshot tests: if one fails, the expected number is **not**
updated — you find out what changed and date an erratum. Mandatory stops:
after Step 0, after Step 1.
