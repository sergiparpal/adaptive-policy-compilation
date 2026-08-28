# Rung 3 — finding

Record. August 6, 2026. Base: the 577 rules the LLM wrote in rung 1
(`results/llm_run.json`). Corpus of 2000 cases, seed 17. Zero LLM calls in the
whole rung.

---

## 1. The central result

**In rung 1 the material contained the signal and the arbitration destroyed it.**

The 577 rules cover the 2000 cases — not one is left without a rule that matches
it — and in **90.1%** of them some matching rule has the correct action. That
number is the exact ceiling of any total order: if no rule covering a case has
the correct action, no order saves it. It comes out without searching for
anything.

> **[ERRATUM 2026-08-06]** The 90.1% is an **upper bound by per-case coverage**,
> not a demonstrated global optimum. `ceiling()` checks, case by case, that
> *some* correct rule exists among those covering it. It does not check that
> **a single total order** exists capable of making the correct rule win
> simultaneously in all those cases, which is a strictly stronger condition. As
> an upper bound it is valid — no order can exceed it — but the maximum actually
> attainable by some order may be lower. Calling it a "ceiling" without
> qualification invites reading it as attainable. See the erratum in section 4.

Searching for an order over half the corpus and evaluating it on the other half,
never seen by the order:

```
              train              test               GAP
pure       0.7779±0.0275     0.7711±0.0352     0.0068±0.0203
hybrid     0.7848±0.0080     0.7496±0.0093     0.0351±0.0118
```

**The gap is essentially zero.** Two of the five splits have it negative
(−0.0161 and −0.0090), and the dispersion across splits (±0.0352) is five times
the mean gap (0.0068): overfitting of the order is not detectable above the
split noise.

Against the references, all on test:

```
ceiling                                     0.8995
searched order (greedy), pure               0.7518
searched order (greedy), hybrid             0.7317
arrival order (born_at)                     0.5216
random order (mean of 50)                   0.4227
specificity-based arbitration               0.1829
subsumption alone (conflict = failure)      0.0412
```

Four times specificity. And the arrival order — which rung 1 wrote off as
useless — already scores 0.52: specificity-based arbitration was worse than
barely ordering anything.

> **[ERRATUM 2026-08-08] Every figure in this section is measured on the CORPUS,
> and the corpus is not a neutral surface.** `harness/domain.py` samples it from
> a deliberately long-tailed distribution: `has_security_keyword` is true in 3%
> of arrivals against 50% of the attribute space, `severity=1` in 5% against
> 25%, `prior_tickets_30d` truncated-geometric against uniform over 21 values.
> Measured over the exhaustive 134,400 combinations instead, on the same 577
> rules and the same pure pool:
>
> ```
>                          corpus    espacio exhaustivo
> cota por cobertura       0.9010                0.8784
> orden buscado (voraz)    0.7713                0.4931
> born_at                  0.5216                0.3148
> aleatorio                0.4227                0.3768
> ```
>
> **The claim that "the arrival order already scores 0.52" does not survive the
> change of surface. Over the case space, born_at is WORSE than shuffling** —
> 0.3148 against 0.3768 — and the sentence above reverses. The early-born rules
> are defaults fitted to the common distribution, which is exactly what a 2000-
> draw sample of that distribution rewards and what a uniform measure does not.
> The comparison against specificity survives; the rehabilitation of arrival
> order does not.
>
> Neither surface is *the* honest one and this record should have said which it
> was using. The corpus is the modelled arrival distribution, so it answers
> "what would this base achieve in deployment" — but it cannot certify an
> optimum or identify a decision function, because 2000 draws touch 1743 of
> 134,400 cases and leave the rest unconstrained. The exhaustive space answers
> "is this order the policy" and cannot answer the first question, because it
> weights regions the system will almost never see. See
> `results3/order_search_ls.json`.

The two critical classes are **100% recoverable**: `SECURITY_INCIDENT` (20 cases)
and `ONCALL_ESCALATION` (7). In rung 1 they gave **0/17** and **0/7**. The
correct rules were written. The engine never let them win.

Rung 2's hybrid arbitration is **worse** than pure ordering over a learned base
(0.7496 versus 0.7711) and is the only one with a consistent gap. Subsumption
costs 0.047 of ceiling: it removes correct rules from the bidding. Consistent
with what was measured in rung 1, where it did not turn out sound over a learned
base.

---

## 2. An ordering problem and a material problem are different things

Rungs 1 and 2 measured them together. Separated, with the per-class ceiling:

```
class                   corpus  ceiling  unrecoverable      nature of the failure
T2_TECHNICAL               726      714       12   1.7%     ordering
SELF_SERVICE_DEFLECT       495      457       38   7.7%     ordering
BILLING_SPECIALIST         271      271        0   0.0%     ordering
T1_GENERAL                 255      255        0   0.0%     ordering
SECURITY_INCIDENT           20       20        0   0.0%     ordering
ONCALL_ESCALATION            7        7        0   0.0%     ordering
T3_ENGINEERING             117       39       78  66.7%     MATERIAL
ACCOUNT_MANAGER            109       39       70  64.2%     MATERIAL
```

- **Ordering problem.** The material is written and what decides whether it gets
  used is the arbitration, or the objective function. Six classes out of eight,
  1774 of the 2000 cases.
- **Material problem.** Two thirds of `T3_ENGINEERING` and of `ACCOUNT_MANAGER`
  do not have a single correct rule covering them. No order, no objective
  function and no arbitration saves them. There the proposer did not write what
  was needed.

The distinction matters because the repairs are opposite: one is fixed in the
engine and the other only in the proposer. Measured together, both read as "the
LLM does not work".

---

## 3. The undeclared knob

Which classes get sacrificed is a choice of objective function, and in rung 1 the
arbitration was setting it without anyone having put it there.

The default greedy search maximizes total correct decisions. The balanced variant
weights each case by 1/|class| on train, so that every class contributes equally:

```
objective                  e2e test   balanced accuracy
total correct                0.7707              0.5241
class-balanced               0.7150              0.6936
                             -5.6 pts            +17.0 pts
```

By class, on test (split 0):

```
class                     test  ceiling  total  balanc.  % ceil tot  % ceil bal
T2_TECHNICAL               364      357    318      295         89%         83%
SELF_SERVICE_DEFLECT       242      220    191      157         87%         71%
BILLING_SPECIALIST         136      136     90      110         66%         81%
T1_GENERAL                 128      128    128      128        100%        100%
T3_ENGINEERING              57       20     14        5         70%         25%
ACCOUNT_MANAGER             55       21      0        5          0%         24%
SECURITY_INCIDENT           10       10      7       10         70%        100%
ONCALL_ESCALATION            3        3      0        3          0%        100%
```

For **5.6 points of aggregate**, `ONCALL_ESCALATION` goes from 0/3 to **3/3** and
`SECURITY_INCIDENT` from 7/10 to **10/10** — the two critical classes at 100% of
their ceiling. `BILLING_SPECIALIST` improves from 66% to 81%.

It is paid for by `SELF_SERVICE_DEFLECT` (87% → 71%), `T2_TECHNICAL` (89% → 83%)
and above all **`T3_ENGINEERING`, which gets worse, from 70% to 25%**. Balancing
is neither free nor uniformly better: it redistributes, and one of the classes
that loses is one of those that had the least ceiling.

The point is not that balancing is preferable. It is that the choice exists, is
explicit in the objective function, and was previously being made without being
declared. Rung 1's 0/17 for `SECURITY_INCIDENT` was not a property of the system:
it was the undeclared consequence of maximizing total correct decisions with an
arbitration that also did it badly.

> **[ERRATUM 2026-08-13] Most of the sacrifice was the greedy's, not the
> objective's.** Step 3 of the audit re-ran this section with the declared
> multi-start local search, same split 0, same pure pool, same two objectives —
> only the search changed
> ([`FINDINGS_AUDIT.md`](FINDINGS_AUDIT.md) Step 3;
> [`budget_and_balance_ls.json`](budget_and_balance_ls.json)).
>
> ```
> clase                  techo   ESTE REGISTRO   voraz hoy   BL hoy   % techo
>                                (total)         (total)     (total)  (BL, total)
> T2_TECHNICAL             357        318            318       341       96%
> SELF_SERVICE_DEFLECT     220        191            191       212       96%
> BILLING_SPECIALIST       136         90             90       124       91%
> T1_GENERAL               128        128            128       124       97%
> T3_ENGINEERING            20         14             14        18       90%
> ACCOUNT_MANAGER           21          0              0        19       90%
> SECURITY_INCIDENT         10          7              4         5       50%
> ONCALL_ESCALATION          3          0              0         0        0%
> ```
>
> **Under the SAME total objective**, a competent optimizer takes six of the eight
> classes to 90% or more of their ceiling. `ACCOUNT_MANAGER` goes from **0 of 21
> to 19 of 21** with no balancing at all, `BILLING_SPECIALIST` from 66% to 91%,
> `T3_ENGINEERING` from 70% to 90%. The 0% and the 66% this section reads as
> *"which classes get sacrificed is a choice of objective function"* were
> substantially a property of the greedy search, not of the objective.
>
> **The knob is real, and it is smaller and narrower than published.** What
> survives is exactly the two rarest classes: under the total objective the local
> search still leaves `SECURITY_INCIDENT` at 5 of 10 and `ONCALL_ESCALATION` at
> **0 of 3**. For those two the trade this section describes is genuine. For
> `ACCOUNT_MANAGER`, which is where the case was made most vividly, it is not.
>
> In aggregate the same correction: balancing costs the greedy 0.0563 and buys
> +0.1735 in balanced accuracy; under the local search it costs +0.0274 and buys
> **+0.0576**. Over the exhaustive space, macro-recall says it buys the greedy
> +0.1093 and the local search +0.0201.
>
> **Two further notes on this table.** The tie-break fix of 2026-08-06 moves
> exactly one cell of it: `SECURITY_INCIDENT` under the total objective, from 7
> to 4. Every other cell reproduces, and the balanced column reproduces in all
> eight. And the balanced local search is *worse* than the balanced greedy on the
> two smallest classes — `ONCALL_ESCALATION` 2 of 3 against 3 of 3,
> `SECURITY_INCIDENT` 9 of 10 against 10 of 10 — while scoring higher on the
> weighted train objective: with 4 and 10 training cases, maximizing macro-recall
> harder does not generalize.
>
> **The same claim also lives in code, where an erratum cannot reach it.** The
> module docstring of `rung3/budget_and_balance.py` states that the greedy
> *"maximizes total correct decisions and **therefore** sacrifices the rare
> classes: on test it gave 0/21 on ACCOUNT_MANAGER and 0/3 on
> ONCALL_ESCALATION"*. Both figures remain true of the greedy; the *therefore* is
> what this erratum withdraws. It is deliberately **not** rewritten — that file
> produces `budget_and_balance.json` and `harness/provenance.py` hashes it into
> the `code_digest` those records carry, so editing prose there moves a
> provenance signal while no figure moves. It is recorded here instead: **that
> docstring carries figures with no erratum attached to them**, and this is the
> erratum.
>
> **This record's own figures are not modified.** Reproduced with
> `python3 -m rung3.budget_and_balance_ls`. Zero API calls.

---

## 4. Caveats

All of them necessary so that the result is not read as more than it is.

**The search uses the oracle.** The greedy search picks each rule by counting
correct and incorrect decisions against `true_action` over the train cases. That
is supervision the shadow loop never has: its only trigger is an impasse or a
conflict, never "the answer was incorrect". What is demonstrated is that **the
material contains the signal**, not that it is attainable without labels.

**The 50 labels buy the order, not the material.** With partial supervision —
simple random sampling of the train set, because stratifying would require
knowing the very labels being rationed — the curve holds up:

```
 fraction    labels    test e2e       sd      min      max
     100%      1005      0.7707   0.0374   0.7425   0.8430
      25%       251      0.7681   0.0326   0.7290   0.8522
      10%       100      0.7488   0.0352   0.6500   0.8053
       5%        50      0.7049   0.0535   0.5596   0.8241
       1%        10      0.5251   0.0628   0.3850   0.6577
```

At 25% the loss is 0.0026, practically free. At 5% — 50 cases, 2.5% of the corpus
— 0.7049 remains, 78% of the ceiling. At 1% it collapses to 0.5251, which is the
arrival order without searching for anything. But **those 50 labels are not the
system's total supervision**: the 577 rules cost 632 LLM calls over the full
corpus, already paid for. Saying "it works with 50 labels" would omit that cost.

> **[ERRATUM 2026-08-13] Re-measured with the audited optimizer. The curve
> survives, the collapse at 1% does not, and part of this table was never the
> optimizer at all.** Step 3 of the audit
> ([`FINDINGS_AUDIT.md`](FINDINGS_AUDIT.md), which owns the new figures) re-ran
> both sections of `budget_and_balance` under the same protocol — same corpus,
> same seed 17, same five splits, same fractions, same draw seeds, same pure
> pool — changing only the search. Record:
> [`budget_and_balance_ls.json`](budget_and_balance_ls.json).
>
> **The table above is left exactly as it was**, and it is *pre-tie-break*: it
> predates the 2026-08-06 fix. Re-running the same greedy today, with the fix,
> gives a third column, and the difference is not small nor of one sign:
>
> ```
>  frac   etiq   ESTE REGISTRO   VORAZ HOY   diferencia   BUSQUEDA LOCAL HOY
>  100%   1005      0.7707        0.7713      +0.0006          0.8530
>   25%    251      0.7681        0.7630      -0.0051          0.8227
>   10%    100      0.7488        0.7342      -0.0146          0.7771
>    5%     50      0.7049        0.6883      -0.0166          0.7410
>    1%     10      0.5251        0.5732      +0.0481          0.5767
> ```
>
> **The sentence "at 1% it collapses to 0.5251, which is the arrival order
> without searching for anything" is withdrawn.** That figure is substantially an
> artifact of the old tie-break: the same greedy, correctly tie-broken, gives
> **0.5732** at 1%. The collapse is real but shallower, and it does not reach
> born_at.
>
> **"50 labels are practically free": the claim genuinely changes with the
> denominator, so all three readings are given.** They do not agree, and one of
> them moves in the *opposite* direction:
>
> ```
> lectura                                        publicado    BL hoy   direccion
> como fraccion de la supervision plena            0.9147    0.8687    empeora
> como perdida absoluta en e2e test                0.0658    0.1120    empeora
> como fraccion de la cota por cobertura (0.9010)   78.2%     82.2%    MEJORA
> ```
>
> As a **fraction of full supervision** the 5% budget falls from 91% to 87%, and
> in **absolute loss** it nearly doubles, from 0.0658 to 0.1120 — both because the
> better optimizer raises the ceiling of comparison: full supervision now buys
> 0.8530 instead of 0.7707, so the same 50 labels fall further behind. But as a
> **fraction of the coverage bound** — how much of what any order could achieve
> those 50 labels actually capture — it *improves*, from 78.2% to 82.2%.
>
> The sentence above this erratum uses the third denominator ("78% of the
> ceiling") and the headline of the section uses the first. Under the audited
> optimizer they now point opposite ways, which is exactly why the denominator has
> to be stated. Nothing here settles which reading is the right one; what is
> withdrawn is the assumption that it does not matter.
>
> **The high variance at low budget does not grow, it shrinks.** Against this
> record's sd of 0.0535 at 5% and 0.0628 at 1%, the local search gives 0.0478 and
> 0.0710; against the *tie-broken* greedy measured in the same run, 0.0590 and
> 0.0739, the local search is less dispersed at both budgets.
>
> **Why, and it is the interesting part.** The number of the 65 starts that tie
> at the best train score goes 1.00, 2.88, 8.84, 18.44, **56.44** as the budget
> shrinks, and the distinct train scores go 32.4 down to **1.4**. At 10 labels
> the objective no longer separates orders at all; ties go to the earliest start,
> which is the greedy, so at 1% the multi-start returns the greedy's own order in
> 22 of 25 configurations. The optimizer cannot help where the objective has
> stopped being informative, and it cannot hurt either.
>
> **§2, the balanced greedy, moves further.** This record measures balancing as
> costing 0.0557 in e2e and buying +0.1695 in balanced accuracy. Under the local
> search it costs +0.0274 and buys **+0.0576** — because the local search under
> the *total* objective already reaches 0.6299 balanced accuracy against the
> greedy's 0.5201, recovering 19 of 21 attainable ACCOUNT_MANAGER cases where the
> greedy recovered 0. Most of what this record read as an objective conflict was
> search weakness.
>
> **This record's own figures are not modified**: they are corrected from above,
> as rung 1 was. Reproduced with `python3 -m rung3.budget_and_balance_ls`.
> Zero API calls.

**High variance at low budget.** At 5%, standard deviation 0.0535 and range
0.5596–0.8241. The mean holds up; one particular draw of 50 labels can give 0.56.

**The greedy search has no global guarantee.** It is the classic greedy search
for decision lists: locally optimal at each step over the live cases, with no
known approximation ratio for this objective, and with no subsequent local
search. Measured: searching for the order **over the test set itself** still
leaves it **0.1187** below the ceiling on average. Almost all the gap between
0.77 and 0.90 is weakness of the search method, not a lack of generalization.

> **[ERRATUM 2026-08-06]** The last sentence is not demonstrated. What was
> measured is that the greedy search, searching over the test set itself, stays
> 0.1187 away from the bound. That cleanly separates search from generalization
> — the gap does not come from evaluating out of sample — but it **does not
> establish that those 0.1187 are attainable by any order at all**. The bound is
> by per-case coverage (see the erratum in section 1) and the real maximum over
> total orders may be lower. The correct claim is: *the gap between 0.77 and 0.90
> is not explained by a lack of generalization; how much of it is greedy-search
> weakness and how much is an unattainable bound remains unmeasured.* Exact
> optimization or a stronger global bound would be needed.
>
> Further later evidence that the greedy search is weak, though it does not bound
> the optimum either: in rung 4 it turned out that perturbing its objective with
> noise improves it against the truth (0.7574 → 0.8337), and that changing the
> tie-break moves the result by ~0.011.

> **[ERRATUM 2026-08-08] Measured. The greedy search was the main problem, and
> the bound was not loose.** The audit of the optimizer
> (`results3/FINDINGS_AUDIT.md`, `PLAN_AUDIT.md` when this erratum was written)
> built a
> multi-start local search — seed 17, 64 random starts plus the greedy at
> position 0, neighbourhood `move+swap`, all declared before running — and put it
> through the same protocol as this record: same corpus, same seed 17, same five
> splits, same two pools, same objective. Only the search changed.
>
> ```
> pool puro, 5 particiones, sobre el CORPUS
>                              train              test               GAP
> voraz (este registro)    0.7775±0.0278     0.7713±0.0381     0.0062
> busqueda local           0.8695±0.0052     0.8530±0.0062     0.0165±0.0098
> ```
>
> **0.7713 becomes 0.8530.** The gap to the corpus bound was 0.1297 and the
> optimizer recovers **+0.0817 of it, 63%**. Overfitting of the order grows from
> 0.006 to 0.017, an eighth of what was gained. So the sentence this erratum
> hangs off — "almost all the gap between 0.77 and 0.90 is weakness of the search
> method" — turns out to have been **substantially right**, and the erratum of
> 2026-08-06 that withdrew it was correctly cautious rather than correct.
>
> **The tie-break is now separated from the algorithm, which is why neither was
> re-run until both could be.** The tie-break fix alone moves test by **+0.0002**
> (0.7711 → 0.7713); the algorithm moves it by +0.0817. The fragility measured
> across `PYTHONHASHSEED` was variance, not bias.
>
> **On the exhaustive space the story is different and worse**, and this record
> could not have seen it:
>
> ```
> pool puro, sobre los 134,400 casos
> cota por cobertura                              0.8784
> busqueda directa sobre el espacio               0.7905     resto 0.0879
> orden buscado sobre train del corpus            0.6105
> voraz de este registro                          0.4931
> ```
>
> The order that scores 0.8530 on corpus test scores 0.6105 as a function. Of
> that 0.268 shortfall, **0.180 is the change of measure** — an order fitted to
> the arrival distribution carried onto a uniform one — and **0.088 survives a
> search that sees every one of the 134,400 cases**. That 0.088 is what the
> erratum above called unmeasured. It is now partly measured: this record's
> greedy left 0.1187 under the bound searching over its own test set; the new
> optimizer leaves 0.0879 searching over the whole space. The residue shrank by a
> quarter and did not close, which is evidence — not proof — that the coverage
> bound is somewhat loose. A heuristic that fails to reach a bound never
> distinguishes "unreachable" from "still too weak".
>
> The hybrid pool remains worse than pure ordering under the new optimizer too:
> 0.7734 against 0.8530 on corpus test. Rung 2's arbitration does not become
> competitive over a learned base by optimizing harder.
>
> Records: `results3/order_search_ls.json`,
> `results3/order_search_ls_fullspace.json`, `results3/optimizer_check.json`.
> Reproduced with `python3 -m rung3.order_search_ls`. Zero API calls. **This
> record's own figures are not modified**: they are corrected from above, as
> rung 1 was.

**The rules were learned over the full corpus.** `born_at` runs from 0 to 1998.
The test set is not data unseen by the rules; it is data unseen by the order. The
split controls overfitting of the order and only that. The gap of a whole system
would be larger. That is why the split was grouped by case identity: 23.1% of the
corpus has an exact twin and a random split would have rewarded memorizing.

---

## 5. What it rewrites of rung 1

`results/FINDINGS.md` is a closed record and **is not modified**. It is corrected
from above, not from within. What changes is this:

**The headline was not "the LLM does not induce reusable structure". It was "the
LLM was inducing structure and the engine was destroying it".**

What still stands from that record, untouched:

- priority in a stratified policy is not recoverable from the syntactic shape of
  the rules; the three routes (specificity, arrival order, subsumption) remain
  falsified
- rung 1's engine ceiling with the perfect policy loaded: 58.75%
- the formulation of a syntactic proxy for authored priority
- generalization from the catch-all's residue
- the proposer's attribute blindness

What gets re-framed:

- **The material was far better than any metric from that run suggested.** Reuse
  0.158, silent error 0.484 and e2e 0.353 described what the arbitration
  extracted, not what the rules contained. The ceiling of those same rules is
  0.90.
- **"Compilation destroyed capability"** was true and is now more precise: it is
  not that the compiled rules were bad, it is that the correct ones existed and
  never won. `SECURITY_INCIDENT` is 100% recoverable and gave 0/17.
- **The stopping threshold** (reuse < 0.30) was applied to a figure that was
  already voided by the engine ceiling. This rung does not rehabilitate it —
  reuse still has not been measured cleanly — but it confirms that stopping the
  project over that 0.158 would have meant stopping it over a measurement of the
  arbitration.

What this rung does **not** demonstrate: that the loop can find that order. The
search sees labels; the loop does not. Still open.

---

## 6. The floor by pool — what an order that searches for nothing scores

*Added 2026-08-24. `rung3/floor_by_pool.py` → `results3/floor_by_pool.json`, run
with `PYTHONHASHSEED=0`. No search of any kind — no greedy, no local search, no
multi-start — and zero API calls. `results/llm_run.json` is read-only. It is
stage A of `PLAN_PAIRWISE.md`.*

**What was missing.** `results3/order_search_ls.json` carries a `"pool"` field on
every row and, under it, only greedy and local-search scores. There was a world
record for the `hibrido` pool and no measurement at all of what *walking* scores
there — and `hibrido` is the pool where declared edges live. Three further
figures had no owning record either: `born_at` and the random mean over the
**full** corpus, and reversed `born_at` over the space. They came from the ad hoc
probe of `CHAT_SUMMARY.md` §2.1, which declares its own protocol unofficial.

**The gate, which ran first and is blocking.** Six figures that are not new
reproduce under the protocol each one was measured with: `born_at` 0.5216 and
the random mean 0.4227 on corpus test **split 0** (this record,
`order_search.json`); 0.5115 and 0.4172 on the **full** corpus (the unowned
probe); 0.3148 and 0.3768 over the space (§1's erratum of 2026-08-08, and
`budget_and_balance_ls.json`). All six land inside their tolerance, and the two
published deviations reproduce as population deviations: 0.0711 and 0.1026.

**The generator is part of the protocol, and there are two of them.**
`local_search.random_order(ids, seed)` sorts the ids and shuffles once per seed;
`order_search.py:344-350` advances a single `random.Random(17)` fifty times over
the rules' appearance order. The corpus figures above came from the second and
the space figure from the first — no single generator reproduces all three. Every
random line below therefore names its generator, and both are reported for every
cell.

### The floors

Order families that search for nothing, both pools, four index sets. `puro` is
first-match-wins with subsumption off; `hibrido` is subsumption as a
non-overridable base level with an order on top, and it is a different machine —
these columns do not chain.

```
                                        puro   hibrido        sd puro / hibrido

FULL CORPUS, 2000 cases
  born_at                             0.5115    0.4285
  born_at reversed                    0.5420    0.5165
  random x50, order_search.py         0.4172    0.4332        0.0711 / 0.0384
  random x50, random_order            0.4212    0.4262        0.0706 / 0.0471

CORPUS TEST, SPLIT 0 (seed 17) — the record's index set, 995 cases
  born_at                             0.5216    0.4332
  born_at reversed                    0.5467    0.5327
  random x50, order_search.py         0.4227    0.4445        0.0710 / 0.0382
  random x50, random_order            0.4251    0.4340        0.0690 / 0.0455

CORPUS TEST, MEAN OF 5 SPLITS (seeds 17..21) — reproduces neither
  born_at                             0.5150    0.4315
  born_at reversed                    0.5452    0.5230
  random x50, order_search.py         0.4219    0.4386        (mean of 5 means)
  random x50, random_order            0.4248    0.4308        (mean of 5 means)

SPACE, all 134,400 combinations
  born_at                             0.3148    0.4257
  born_at reversed                    0.5668    0.4373
  random x50, order_search.py         0.3864    0.3903        0.0981 / 0.0534
  random x50, random_order            0.3768    0.3867        0.1026 / 0.0445
```

The two corpus-test blocks are two index sets, not one figure and its refinement.
Split 0 is the only one that reproduces 0.5216 and 0.4227; the five-split mean is
the more stable statistic and reproduces neither. Its random rows are a **mean
over five splits of a mean over fifty draws** — two aggregations stacked, which is
why they carry no single deviation.

### What the new cells say

**The `hibrido` floor is not the `puro` floor with a constant subtracted.** On the
three corpus surfaces it is *below* the pure one by 0.083 to 0.088; over the space
it is *above* it by 0.111. The order of the two pools reverses with the surface,
so neither pair licenses reading the other.

**Over the space, arrival order beats a shuffle on the hybrid pool and loses to
one on the pure pool.** 0.4257 against 0.3867 and 0.3903 on `hibrido`; 0.3148
against 0.3768 and 0.3864 on `puro`. What §1's erratum of 2026-08-08 says —
*over the case space, `born_at` is worse than shuffling* — is a **pure-pool**
statement and does not survive the change of pool. The hybrid margin is
+0.039 and +0.035 against
deviations of 0.0445 and 0.0534: under one deviation, so it is a sign and not an
improvement, in the same sense that erratum used the phrase.

**Over the corpus, arrival order on the hybrid pool is indistinguishable from a
shuffle, and which side of it you land on depends on the generator.** On the full
corpus `born_at` scores 0.4285, above `random_order`'s 0.4262 and below
`order_search.py`'s 0.4332. Both gaps are under a sixth of the corresponding
deviation. A write-up naming one generator could have published either sign of the
same comparison; that is the concrete cost of the unlabelled random baseline, and
it is why every line above carries its generator.

**Reversal is worth almost nothing on the pool where declared edges live.** Over
the space, reversing `born_at` gains **+0.2520** on `puro` (0.3148 → 0.5668) and
**+0.0116** on `hibrido` (0.4257 → 0.4373). The headline of the probe — a
label-free heuristic recovering most of what a search with an oracle recovers — is
a property of the pure pool. Over the corpus the contrast runs the other way and
is much smaller: the hybrid pool gains +0.088 to +0.100 from reversal and the pure
pool +0.025 to +0.031.

**The hybrid pool's random orders vary about half as much as the pure pool's**
(deviations 0.0382-0.0534 against 0.0690-0.1026, on all four index sets).
Subsumption prunes the pool before the order is consulted, so on the cases it
resolves there is nothing left for a permutation to move; `FINDINGS_AUDIT.md`
measures one instance of that pruning — 181 of the 577 rules match nothing on
corpus train once subsumption has run. **That is a reading of the deviations
and of a figure measured on one surface, not a measurement of its own**: what
this record establishes is the spread, not its cause.

### What this record does not claim

**It carries no prediction.** `PLAN_PAIRWISE.md` §0.1: the two rows that predicted
these figures were measured on 2026-08-24 before anyone signed them, by an audit
that ran this stage's gate to check that a correct implementation could pass it.
They are spent and are not restored. Nothing here may be reported as a band that
held; what the stage delivers is an owner, a script and an `_env` for figures that
had none.

**It leaves one thing for the stage that uses it.** `PLAN_PAIRWISE.md` §10
scores a declared order against "the `hibrido` `born_at` floor", on corpus
test, without saying which of the two corpus-test index sets that is:
**0.4332** on split 0, or **0.4315** as the five-split mean. The two differ
by 0.0017 and the band drafted for that comparison is ±0.03, so the choice is
unlikely to change a verdict — but it has to be made before the figure exists,
not after, and it is not this record's to make.

**Files added by this section**

```
rung3/floor_by_pool.py            the floors: two pools, four index sets, two
                                  random generators, six-row reproduction gate
results3/floor_by_pool.json       the record
tests/test_floor_by_pool.py       the gate is blocking, the generators are
                                  transcribed, no figure pinned
```

Reproducible with `PYTHONHASHSEED=0 python3 -m rung3.floor_by_pool`
(`--checks` runs the gate alone). Two seconds, zero API calls.

---

## 7. What a queue ranking alone scores, and what that does to P-d

*Added 2026-08-24. `rung3/queue_hierarchy_floor.py` →
`results3/queue_hierarchy_floor.json`, `PYTHONHASHSEED=0`, 220 s, zero API
calls. It is the control Stage C's result made necessary, run before Stage D
spends anything.*

**Why it exists.** Stage C asked a model 170 times which of two rules should win
a ticket and got 0.8824. A baseline that reads **no rule at all** — a fixed total
order over the eight queues — scored 0.9471 on the same pairs, and on the nine
pairs no queue ordering can reach the model was at 5 of 9
(`results2/FINDINGS2.md`, Stage C). Stage D spends 300–500 calls asking that
question of the learned base and compiles the answers into an order, which **P-d**
bands against the `hibrido` `born_at` floor plus 0.03. So one question has to be
answered first, and it costs nothing: **how much of that band does a lookup table
already reach?**

**What a hierarchy is here.** A total order over the eight actions induces one
over the 577 rules: sort by the rank of the rule's action. It reads no condition,
no extension, no overlap and no subsumption — only which queue each rule sends a
ticket to. All **40,320** of them are scored.

### The result, on the pool where declared edges live

```
hibrido                      floor    +0.03    stage_c     best/40320     mean
  full corpus               0.4285   0.4585     0.4805         0.5240   0.3676
  corpus test, split 0      0.4332   0.4632     0.4824         0.5266   0.3670
  corpus test, 5 splits     0.4315   0.4615     0.4806         0.5250   0.3658
  space                     0.4257   0.4557     0.5838         0.5997   0.3180
```

`stage_c` is the ranking Stage C's answer key produced over the **hidden**
policy's pairs, transferred here unchanged — the closest thing available to *the
ranking the model appears to be using*, fitted on a different object and so
costing no labels from this base.

**It clears P-d's band on all four surfaces, at zero calls.** 0.4824 against a
threshold of 0.4632 on the record's own index set; 0.5838 against 0.4557 over the
space.

**`best` is a winning ticket and `mean` is the level.** The maximum over the
40,320 is taken with the labels in hand — the same object as the best of 65
starts in `PLAN_PAIRWISE.md` §2 — while a hierarchy picked blind is worth 0.3670,
*below* the `born_at` floor. Knowing which queue ranking to use is the whole
content of the baseline, and Stage C is where that knowledge came from.

**The tie-break inside a class cannot change the score, and it is provable.**
Under a class-grouped order the winner of a case belongs to the highest-ranked
action among those of the rules matching it, and every rule in that class carries
that action. The decision, and so the score, is a function of the hierarchy alone.
Both tie-breaks are computed and gated against each other, and eight random
shuffles within the classes give the identical figure. Two consequences: the
control cannot have been weakened by a badly chosen tie-break, and `best` is the
**exact ceiling** of the family rather than the best anyone happened to find.

### The contrast that says where this bites

```
puro                         floor              stage_c     best/40320
  corpus test, split 0      0.5216               0.4291         0.5015
  space                     0.3148               0.5756         0.6058
```

On the **pure** pool over the corpus the hierarchy is *worse* than arrival order
— 0.4291 against 0.5216 — and even the best of the 40,320 does not reach the
floor. The queue ranking is not a strong order in general. **It is strong exactly
on the machine P-d measures**, which is what makes it a problem for P-d and not a
curiosity: once subsumption has pruned the pool, most of what is left to decide is
*which action*, and a ranking of actions is precisely the instrument for that.

### What this does to P-d, stated carefully

**It does not refute it and it does not move it.** P-d was signed on 2026-08-24
with its band and its refutation line, and it will be adjudicated on the order
Stage D's declared edges induce, exactly as written. A baseline is not a
refutation and this record adjudicates nothing.

**What it does is take away the band's power to discriminate.** A declared order
scoring 0.47 on corpus test would *hold* P-d and would still be **worse than a
free lookup table**. So a hold can no longer be read as evidence that declaration
contributes a channel — which is what §10's own interpretation section wanted
from it: *landing on the floor → declaration contributes no channel; landing
between floor and the cloud → it contributes and is not enough*. Between the
floor and the cloud there is now a third thing sitting at 0.4824 that cost
nothing.

**The comparison that recovers the discrimination costs zero calls**: score the
declared order and the hierarchy order side by side, on the same pool and the
same index set. Stage D can report it whatever P-d does. Building that comparison
is a control and not an amendment; **changing P-d's band is an amendment, and
after a baseline is known it would be hard rule 6 wearing a different hat.** The
band stays as signed.

**Files added by this section**

```
rung3/queue_hierarchy_floor.py       all 40,320 hierarchies, two pools, four
                                     surfaces, with the floor READ from stage A
results3/queue_hierarchy_floor.json  the record
tests/test_queue_hierarchy_floor.py  the induced order reads only the action,
                                     the enumeration is the whole group, the
                                     tie-break gate, the floor read gate
```

Reproducible with `PYTHONHASHSEED=0 python3 -m rung3.queue_hierarchy_floor`.
Under four minutes, zero API calls.

---

## 8. What the declared edges do — P-d and P-e, both refuted

*Added 2026-08-24. `rung3/declared_order.py` → `results3/declared_order.json`,
`PYTHONHASHSEED=0`, 339 s, zero API calls. It scores the 344 edges Stage D
bought (`results2/FINDINGS2.md`, Stage D) and adjudicates two signed rows.*

**There is no truth for those pairs and none is invented here.** Nothing below is
a correct-edge rate. What is measured is what the edges *do*.

### As an order

The edges are a partial order; compiling them is a topological sort whose ready
set is drained in `born_at` order, so a rule no edge touches keeps its arrival
position. `born_at` **is** the floor, so the comparison is exactly *what the edges
added to it*. A gate checks the compiled order honours all 344; none is broken.

**575 of the 577 rules moved off their arrival position.** 344 edges is 1.1% of
the 31,850 pairs that could carry one, but the sort cascades: a rule held back
shifts everything behind it. So this is the edges' global effect and not a local
tweak.

```
pool     surface              declared    floor  hierarchy   vs floor   vs hier
puro     full corpus            0.4700   0.5115     0.4285    -0.0415   +0.0415
puro     corpus test, split 0   0.4764   0.5216     0.4291    -0.0452   +0.0472
puro     space                  0.3830   0.3148     0.5756    +0.0682   -0.1926
hibrido  full corpus            0.4060   0.4285     0.4805    -0.0225   -0.0745
hibrido  corpus test, split 0   0.4080   0.4332     0.4824    -0.0251   -0.0744
hibrido  space                  0.4564   0.4257     0.5838    +0.0306   -0.1274
```

**P-d is REFUTED.** Signed at *strictly above the floor by more than 0.03*, it
needed 0.4632 on the `hibrido` pool at corpus test split 0 and got **0.4080** —
**below the floor itself**, by 0.0251. The declared edges did not fail to add
enough; they made the order worse than doing nothing.

The free queue ranking scores **0.4824** on that same cell. The control was built
because a *hold* would have been unreadable; in the event it is the refutation
that needs it, and it says the gap is 0.074 rather than a rounding error.

### The direction control — the model's choices, not the compilation

A single low score cannot separate *the model chose badly* from *compiling any
edges this way hurts*. So: the same 365 pairs, the same compilation, the same
scoring, and only the **direction** of each edge changed.

```
the model                0.4080
a coin on direction      0.4314   sd 0.0243   (50 draws, seed 17)
the model INVERTED       0.4432
the born_at floor        0.4332
```

**A coin lands on the floor** — 0.4314 against 0.4332 — so the compilation is not
what costs the 0.025. The model sits **0.96 deviations below the coin** and
inverting every one of its answers puts it **0.48 above**, and above the floor.

Read carefully: both gaps are inside one deviation of the coin distribution, so
each on its own is a **sign and not an established effect**. What is harder to
dismiss is that they point the same way, and that the span from the model to its
own inverse is 0.0352 — about one and a half coin deviations. On this base, with
this model and this prompt, **the declared direction carries signal with the wrong
sign.**

That is the same shape as `results/FINDINGS.md`'s finding about arrival order —
*it does not lack signal, it lacks a sign* — arrived at by a different route and
on a different channel.

> **[ERRATUM 2026-08-24] The last two paragraphs are wrong, and §9 measures the
> thing they inferred.** The sign is not inverted. Asked directly — of the
> declared edges on pairs where one rule is strictly better over the region the
> two share, how many point at it — the answer is **194 of 278, 0.6978**, which
> is **6.6 standard errors above a coin**, and 0.6299 on the corpus surface, 4.4
> above. The declared direction is right about seven times in ten.
>
> What was wrong was reading an order-level score as evidence about directions.
> With the null sharpened from 50 draws to 2,000, the model's 0.4080 has
> **14.7%** of coins at or below it: unremarkable, not a deficit. The `sign and
> not an established effect` hedge was right and the sentence that followed it
> went further than the hedge allowed.
>
> **What replaces it is a stronger finding, not a weaker one.** Compiling the
> ORACLE's own directions on these same 400 pairs scores 0.4523 and 0.4593 —
> above the floor, below P-d's 0.4632 threshold, and still inside the coin
> distribution. At this budget the direction of the edges barely moves the
> order whoever chooses it, so **P-d was not refuted because the model chose
> badly. It was refuted because 344 edges cannot move a 577-rule order across a
> 0.03 margin at all.** §9 has the figures.

### As a machine — P-e

The 65 end orders were **regenerated on the hybrid pool**, not read from
`order_metrics.json`, whose 65 are `puro`: a hybrid order and a pure order can
decide differently for no reason except the pool, and that difference would enter
the distance as if it were disagreement about priority. 296 s, `move+swap`, seed
17, 64 starts plus the greedy.

Behavioural distance over the exhaustive space, hybrid pool: **median 0.4497**,
min 0.3482, max 0.5490.

**P-e is REFUTED.** Signed at *median pairwise disagreement ≤ 25% of the space*,
it landed at 45.0% — nearly twice the band, and well outside a cloud whose own
members disagree with one another by up to about 20%. The declared order is not
inside the behavioural cloud; it is a different machine from all 65.

### As a hybrid engine — the number that reframes the rest

```
e2e             0.0673        995 corpus test cases
CONFLICT        0.8894        885 of 995
IMPASSE         0.0000
ACTION            110 cases committed
silent error    0.3909        of those 110
```

With 344 declared edges installed, **the engine abstains on 89% of the corpus**.
Rung 2's hidden policy reaches e2e 1.0000 with zero conflicts on 199 edges over
**29** rules; here 344 edges over **577** rules leave almost everything
unresolved.

That is not a failure of the edges' quality — it is the authorship cost showing
its true size. `results2/FINDINGS2.md` closes with *the cost of authorship is not
measured on a learned base*. It is now, and the answer is that **400 calls buy
1.3% of the pairs that need one**, and the engine behaves accordingly. The
conflict rate is the honest reading of that: the mechanism is abstaining, which
is what it is supposed to do when nobody has told it who wins.

### What this closes and what it does not

**It closes the pairwise-judgement thread as specified.** Three signed rows,
three verdicts: P-c held on the hidden policy, P-d and P-e are refuted on the
learned base. The change of question works as a *format* — 91% of the calls
returned a well-formed edge — and the edges it produces do not order the base.

**It does not show the model cannot do this.** One base, one model, one prompt,
one budget, and a direction control whose two halves are each inside a deviation.
What it shows is that this protocol, at this budget, produced an order worse than
arrival order and a machine outside the cloud.

**And it does not touch the second material problem.** For `T3_ENGINEERING` and
`ACCOUNT_MANAGER` no correct rule exists at all; no edge and no order recovers
those cases, and nothing here changes that.

**Files added by this section**

```
rung3/declared_order.py            the three scorings, the direction control
results3/declared_order.json       the record
tests/test_declared_order.py       the compilation, which is where a wrong
                                   answer would have looked right
```

Reproducible with `PYTHONHASHSEED=0 python3 -m rung3.declared_order`. Under six
minutes, zero API calls.

---

## 9. The direction is right; the compilation is where it is lost

*Added 2026-08-24. `rung3/edge_direction.py` → `results3/edge_direction.json`,
`PYTHONHASHSEED=0`, 20 s, zero API calls — it reads the 400 answers Stage D
already paid for. **POST-RUN**: written after P-d and P-e were adjudicated, by
someone who had already seen the direction control. Nothing here is a bet that
could have failed and no signed row moves.*

**A different truth from the one §10 denied.** `PLAN_PAIRWISE.md` §10 says *there
is no truth for these pairs*, and about the object it means — the hidden policy's
**layer order** over rules it never wrote — that is right and stays right. This
measures another one and never calls it a layer relation: over the cases in
`ext(A) ∩ ext(B)`, **which rule's action is the true action more often**. Ties,
and pairs where neither rule is ever right, go outside every denominator.

### 1. Does the declared direction point at the better rule? Yes, clearly

```
surface   pointed at it    n    rate      se     vs a coin
space         194          278   0.6978   0.0300   +6.60 sd
corpus        177          281   0.6299   0.0298   +4.36 sd

outside the denominator
space     tie 32 · neither ever right 66 · no edge declared 24
corpus    tie  2 · neither ever right 93 · no edge declared 24
```

**The model is right about seven times in ten**, and on this denominator that is
six standard errors from a coin. The pairwise question does elicit real
information about which of two rules should win.

**The `neither` box is the material problem again**: on 66 pairs over the space
and 93 over the corpus, the true action on the shared region is some third queue
throughout, so neither rule can be the right winner. That is 17% and 23% of the
sample, and no edge fixes it.

### 2. Would the right direction have helped? Barely

The same 400 pairs with every edge pointing at the better rule, compiled and
scored exactly as the run's were — `hibrido` pool, corpus test split 0:

```
the model                 0.4080
the model INVERTED        0.4432
the ORACLE's direction    0.4523   (space definition of better)
the ORACLE's direction    0.4593   (corpus definition)
the born_at floor         0.4332
P-d's threshold           0.4632
```

**Even the oracle's own directions do not clear P-d's band.** 0.4593 against
0.4632, on a channel where every edge points the right way by construction.

### 3. The null, sharpened from 50 draws to 2,000

```
coin on direction   mean 0.4318   sd 0.0228   [0.3538, 0.4985]

                    score    coins at or below    coins at or above
the model          0.4080          14.7%                86.2%
inverted           0.4432          69.7%                32.3%
oracle, space      0.4523          82.5%                18.7%
oracle, corpus     0.4593          88.9%                12.1%
```

**Every one of them sits inside the coin distribution.** The model is not
significantly below it; the oracle is not significantly above it.

### What this establishes, and what it withdraws

**It withdraws §8's `signal with the wrong sign`**, which is why that section now
carries a dated erratum. The inference ran from an order-level score to a claim
about directions, and the direct measurement contradicts it: the directions are
right 70% of the time. The hedge in §8 — *a sign and not an established effect* —
was correct, and the sentence after it went further than the hedge allowed.

**What replaces it is stronger.** The pairwise channel carries real signal about
which rule should win, and **that signal does not survive compilation into an
order at this budget**. 344 edges over 577 rules is 1.1% of the pairs that could
carry one; the coin's own spread over direction, 0.0228, swamps the 0.051 that
separates the model from the oracle. So:

> **P-d was not refuted because the proposer chose badly. It was refuted because
> 344 edges cannot move a 577-rule order across a 0.03 margin, whoever chooses
> their direction.** The band was out of reach at this budget before a single
> call was made.

That is a statement about the protocol, not about the model, and it is the one
that transfers. It also says what a next attempt would have to change: **the
budget, not the prompt.** Whether the channel pays at 3,000 edges or 30,000 is
unmeasured, and this record cannot say — what it can say is that measuring it at
400 was never going to answer the question P-d asked.

**It does not rehabilitate the proposer either.** Seven in ten on a two-way
choice, on the half of the population where a better rule exists at all, with 17%
to 23% of pairs having no right answer among the two shown — that is the same
proposer Stage C measured, doing about as well, and the queue-ranking control of
§7 still applies to it.

**Files added by this section**

```
rung3/edge_direction.py         the better rule per pair, the oracle's own
                                directions compiled, and a 2,000-draw null
results3/edge_direction.json    the record, with its provenance field
```

Reproducible with `PYTHONHASHSEED=0 python3 -m rung3.edge_direction`. Twenty
seconds, zero API calls.

---

## 10. The channel does pay with more edges, and 400 was the worst place to ask

*Added 2026-08-24. `rung3/edge_budget.py` → `results3/edge_budget.json`,
`PYTHONHASHSEED=0`, 173 s, **zero API calls**. **POST-RUN**, like §9: written
after P-d and P-e were adjudicated.*

**Why it needs no money.** §9 left one question open — whether the pairwise
channel pays at a budget nobody paid for — and the oracle's direction is
computable offline for every one of the 31,850 pairs. So the channel's **ceiling**
as a function of budget is free. The proposer's own curve beyond 400 is not, and
this does not pretend otherwise: it projects at the accuracy §9 measured and says
so on every line.

Everything below is on **one cell**: `hibrido` pool, corpus test split 0 — P-d's
own. Budgets are **nested**: the population shuffled once at seed 17, each budget
a prefix of that shuffle. A tie offers no edge.

```
  budget   edges   oracle    noisy     coin   coin sd
     400     303   0.4533   0.4471   0.4556    0.0239
     800     604   0.4774   0.4633   0.4472    0.0227
    1600    1174   0.5497   0.4981   0.4519    0.0182
    3200    2303   0.6030   0.4982   0.4553    0.0264
    6400    4484   0.6492   0.5443   0.4897    0.0249
   12800    8815   0.6683   0.5566   0.4877    0.0314
   25600   17521   0.6834   0.5652   0.4951    0.0290
   31850   21692   0.6784   0.5628   0.4977    0.0292
```

`oracle` is exact: every offered pair pointed at the rule that gets more of the
shared region right. `noisy` is a **projection**, the same directions flipped
independently at 0.3022 — the rate §9 measured the proposer missing — and it is
the shape of the answer rather than the answer, because Stage C found the
proposer's accuracy varies by queue-pair and its errors are therefore neither
independent nor evenly spread.

### The ladder, all of it on the same cell

```
born_at floor, which is a budget of zero            0.4332
the model's 344 edges at budget 400                 0.4080
P-d's threshold                                     0.4632
a free queue ranking (§7)                           0.4824
the channel at 70% accuracy, exhausted              0.5652
the channel with a perfect chooser, exhausted       0.6834
the searched order, best of 65 starts               0.7678
the coverage bound (FULL corpus, not this cell)     0.8540
```

### Three things this settles

**1. The channel pays, and P-d would have held at 800.** The oracle crosses P-d's
threshold at **800** and so does the 70%-accurate projection — 0.4633 against
0.4632, by a hair, but the next rung up is 0.4981. Doubling the budget flips the
verdict. **P-d was refuted at the one budget in this range where nothing could
have been distinguished from anything.**

**2. At 400 the three curves are the same number.** 0.4533, 0.4471 and 0.4556,
against a coin deviation of 0.0239. A perfect chooser, a 70% chooser and a coin
are indistinguishable there. That is §9's conclusion arrived at from the other
side, and it is the sharpest statement of what went wrong: the budget was chosen
before anyone knew the curve, and it landed on the flat part.

**3. Accuracy does not wash out with volume.** The gap between the perfect
chooser and the 70% one is 0.12 at full budget and does not close — 0.6834
against 0.5652. More edges do not compensate for choosing them badly, which is
worth stating because the opposite is the natural guess.

### And the ceiling of the whole channel is below what search reaches

An **exhausted** pairwise channel with a **perfect** chooser reaches **0.6834**
where the searched order on the same cell reaches **0.7678**. The gap is 0.084
and it is not a budget effect — the curve is flat from 12,800 on, and at 31,850
it is slightly *lower* than at 25,600, because more edges mean more constraints
and more cycle refusals with no compensating gain.

So the pairwise channel is not an alternative route to what search finds. Even
handed every pair and the right answer to each, it stops well short. What it is
instead is a route that needs no labels of the kind search uses — and that
comparison, oracle against oracle, is not the one that matters for a proposer.

### What is measured and what is projected, one last time

**Measured, exactly**: the oracle curve, the coin curve, and their crossings.
**Projected, under a stated assumption**: the noisy curve. **Not measured at
all**: what the actual proposer scores at any budget above 400. That would take
calls, and the honest budget for the question §9 left open is now known —
somewhere around 800 to answer P-d, around 1,600 to beat a free queue ranking.

> **ERRATUM, 2026-08-26.** The last clause of that sentence is **wrong**, and §11
> is the measurement that says so. The proposer was asked at 1,600 and its order
> scores **0.4804** against the free queue ranking's **0.4824** — it does not beat
> it, it ties it two thousandths low. The projection this section published for
> that budget, **0.4981**, sits 0.0177 above what the proposer actually reached.
>
> The projection was not miscomputed; its **assumption** was wrong, and this
> section named it: errors flipped *independently and at a uniform rate*. §11's
> `B-d` measures that assumption directly for the first time and refutes it — the
> proposer's direction rate is 0.8647 on the pairs a queue ranking can already
> answer and 0.6391 on the ones it cannot. Errors that concentrate on the
> informative pairs buy less order than the same number of errors spread evenly,
> which is exactly the gap between 0.4981 and 0.4804.
>
> What this section got **right** is not withdrawn: the channel does pay with more
> edges, 400 was the worst place to ask, and P-d clears its threshold at this
> budget — 0.4804 against 0.4632. Only the sentence about beating a queue ranking
> at 1,600 is retracted.

**Files added by this section**

```
rung3/edge_budget.py         the four curves, nested at seed 17
results3/edge_budget.json    the record, with its provenance field
```

Reproducible with `PYTHONHASHSEED=0 python3 -m rung3.edge_budget`. Three minutes,
zero API calls.

---

## 11. The real proposer at 1,600: it holds its accuracy, and buys nothing with it

*Added 2026-08-26. `PLAN_PROPOSER_1600.md`, §0 signed 2026-08-25 before any figure
of it existed. `rung2/pair_judgement.py` → `results2/pair_judgement_1600.json`
(**1,200 API calls**, 4 h 11); `rung3/edge_direction.py` →
`results3/edge_direction_1600.json` and `rung3/declared_order.py` →
`results3/declared_order_1600.json`, both `PYTHONHASHSEED=0` and **zero API
calls**. This is the first section of the thread that is **pre-registered rather
than post-run**: the four rows were signed before the calls were made.*

Everything below is on **one cell**: `hibrido` pool, corpus test split 0. Where a
figure sits elsewhere it is labelled. The population is 1,600 pairs — Stage D's
400 plus 1,200 drawn uniformly from the remaining 31,450 at seed 25 — so the two
budgets are **nested** and the comparison between them is one population at two
sizes.

### The four rows

```
row  band                        measured              verdict
B-a  |rate - 0.6978| <= 0.05     0.7312  (n 1105)      HOLDS
B-b  > 0.4824                    0.4804                REFUTED
B-c  >= 0.4981                   0.4804                REFUTED
B-d  unreachable < reachable     0.6391 vs 0.8647      HOLDS
```

The drafter's own expectation, recorded in §0 before the calls: *B-a holds, B-b
holds, B-c refuted, B-d holds*. **Three of four.** `B-b` is the miss, and the way
it misses is the finding.

### B-a — the proposer is the same instrument at both budgets

Of the pairs with a strict better rule under the **space** definition **and** a
declared edge, the fraction of edges pointing at the better rule:

```
                        n      rate      se     deviations from a coin
400  (Stage D)        278    0.6978   0.030          +6.60
1600 (Stage B)       1105    0.7312   0.015         +15.37
```

`|0.7312 - 0.6978| = 0.0334`, inside the signed 0.05. Over the corpus surface the
same quantity is 0.6715 on n 1093. The proposer did not degrade, did not improve
materially, and quadrupling the sample bought a rate two standard errors from the
one measured on 400. **Whatever goes wrong later, it is not that the instrument
moved.**

### B-b — 1,200 calls to tie a free queue ranking, two thousandths low

```
pool     surface              declared    floor  ranking  vs floor  vs ranking
puro     corpus_full            0.4905   0.5115   0.4285   -0.0210    +0.0620
puro     corpus_test_split0     0.4915   0.5216   0.4291   -0.0302    +0.0623
puro     space                  0.4805   0.3148   0.5756   +0.1657    -0.0951
hibrido  corpus_full            0.4695   0.4285   0.4805   +0.0410    -0.0110
hibrido  corpus_test_split0     0.4804   0.4332   0.4824   +0.0472    -0.0020
hibrido  space                  0.5463   0.4257   0.5838   +0.1206    -0.0375
```

`B-b` is the `hibrido` / corpus test split 0 row and it is **refuted by 0.0020**.

**That number should not be read as a defeat by the ranking.** The coin's own
spread on this exact sample is sd 0.0319 over 200 draws, so the margin is a
fifteenth of a deviation. The signed band is `> 0.4824` and its edge is its own
refutation line, so the verdict is REFUTED and stays REFUTED; the honest sentence
beside it is that **after 1,200 calls the compiled order and a free ranking of
eight queues are the same number.**

What did move is the floor: +0.0472 over `born_at`, against +0.0000 at 400 —
Stage D's 344 edges scored 0.4080, *below* the 0.4332 floor. So the budget bought
a real gain over arrival order. It did not buy a gain over a baseline that reads
no rule and costs nothing.

### B-c — refuted, and inside the projection's own noise

```
                                        value       sd
the order                              0.4804        —
the projection, as §10 published it    0.4981   0.0155   (edge_budget's shuffle)
the projection, on THIS sample         0.5011   0.0280   (200 draws)
a coin on direction, on THIS sample    0.4697   0.0319   (200 draws)
the oracle, on THIS sample             0.5739        —
```

The order sits **−0.74 projection deviations** below it. §8 of the plan asked for
this distinction explicitly: a refutation by less than the projection's own
deviation is a different event from one by three of them, and this is the first
kind. `B-c` is refuted as signed, and the projection is not thereby shown to be
wildly optimistic — only optimistic, and for a reason `B-d` names.

### B-d — the errors fall exactly where they cost most

The split is a property of the **oracle and the sample**, fixed and gated by
`rung2/pair_sample_1600.py` before a single call was made, and read here rather
than derived from the answers it predicts. A queue-pair a fixed ranking cannot
answer is one that appears with **both** better-rules.

```
surface   side          n      rate
space     unreachable  654    0.6391
space     reachable    451    0.8647     difference -0.2256
corpus    unreachable  800    0.5813
corpus    reachable    293    0.9181     difference -0.3368
```

**This is the mechanism, and it explains B-b and B-c together.** The proposer is
near-excellent — 0.86, and 0.92 on the corpus surface — precisely on the pairs a
free queue ranking already gets right, and drops to 0.64 (0.58) precisely on the
pairs that carry the information a ranking does not have. Stage C's finding that
its competence is largely a fixed ranking of the eight queues
(`results2/pair_judgement_baselines.json`) is here again, measured on the learned
base and against the oracle rather than against a label.

So the 1,200 calls bought a rate of 0.7312 whose *accurate part* is redundant with
a baseline that costs nothing, and whose *errors* are concentrated where the
baseline is silent. An order compiled from that cannot beat the baseline, and the
budget is not what stopped it.

### A rate 15 deviations above a coin that produces an order 0.40 deviations above one

```
the model's order                            0.4804
a coin on direction, 2000 draws       mean   0.4672  sd 0.0290   -> +0.40 dev
the model INVERTED                           0.4372              -> -1.16 dev
every direction from the oracle              0.5246              -> p(high) 0.023
```

Knowing which of two rules is better **73% of the time** yields an order
indistinguishable from choosing at random (`p(low) 0.68`). Even the **oracle's own
directions** on these 1,600 pairs reach only 0.5246 here. The pairwise channel
loses most of what is put into it in compilation, which is §9's conclusion holding
at four times the budget with a much sharper instrument.

### What the calls actually returned

```
                     Stage D (400)    Stage B (1600)
parse failures      35  = 8.75%      82  = 5.12%
no edge             35  = 8.75%      121 = 7.56%
a_beats_b                     162             698
b_beats_a                     203             781
accepted by try_edge          344            1310
cycles refused                 21             169
rules moved off arrival   575/577         576/577
queue-pairs constant        14/24           10/25
```

**The parse-failure rate came down.** `IDEAS.md` carried its tripling from 2.4%
(Stage C) to 8.75% (Stage D) as an unexplained mechanism, with the same model,
settings and prompt. At four times the sample it is 5.12%, between the two. The
tripling looks like sampling noise on small denominators rather than a shift, and
**the prompt was not touched** — rule 5 of the plan, and the whole point of
recording a surprise instead of chasing it.

**Cycles rose faster than edges.** 169 refused against 21, which is 11.4% of
declared edges against 5.8%. As the graph fills, more of what the proposer says
cannot be installed at all, and the accepted set is increasingly shaped by which
answers arrived first. At the full population §10 already showed this turning
negative.

### The presentation-position asymmetry, outside every denominator

No row predicts it and it is reported apart from them. Presentation order is
balanced exactly by construction.

```
                          winner shown first   rate    deviations
400  (Stage D)                 197 / 168      0.5397      +1.52
1600 (Stage B)                 801 / 678      0.5416      +3.20
```

**The effect held its size and became significant.** The proposer prefers the rule
it is shown first, by about four points. But it is nearly free: the direction rate
is 0.7143 when `rule_a` was shown first and 0.7473 when it was shown second, so
the bias moves which side gets named far more than whether the naming is right.
This does **not** explain Stage D's 203/162, which is about which rule wins and
survives at 698/781 — the two are different questions and conflating them is how
the asymmetry stayed unexplained.

### As a hybrid engine, for completeness

```
                   400 edges    1310 edges
e2e                   0.0673        0.1819
silent error          0.3909        0.3418   (n 110 -> 275)
CONFLICT rate         0.8894        0.7236
IMPASSE rate          0.0000        0.0000
```

More edges resolve more cases — CONFLICT falls 0.17 and e2e nearly triples — and
the cases newly resolved are wrong about a third of the time. Both rates are
published with their own denominators because they have different ones: `silent
error` is over the cases the engine COMMITS to.

### What this settles, and what it does not

**Settles.** The question `IDEAS.md` carried as *what the real proposer scores
above 400 calls* is answered at one budget: **0.4804 at 1,600**, on `hibrido` /
corpus test split 0. §10's projection for that budget was 0.4981, and §10's
sentence about beating a queue ranking at 1,600 is retracted in its own erratum.

**Does not settle.** Whether more budget would eventually clear the ranking. §10's
oracle curve is flat from 12,800 on and its ceiling is 0.6834 against search's
0.7678, so the room is real but bounded — and `B-d` says the proposer spends its
errors in the worst possible place, which no budget repairs.

**Does not touch.** The material problem. Of the 1,600 pairs, **282** have no
right winner among the two rules shown under the space definition and **409**
under the corpus one — between a sixth and a quarter, as before. No edge fixes a
pair where the truth is a third queue.

**P-d and P-e are not re-adjudicated here.** They were signed in §0 of
`PLAN_PAIRWISE.md` and adjudicated on Stage D's 400; both records carry the same
computation on this population with the word `verdict` removed and
`adjudicates: false` in its place. For the record and not as a verdict: the P-d
quantity is 0.4804 against its 0.4632 threshold, which is §10's prediction that a
larger budget flips it, and the P-e quantity is a median behavioural distance of
0.4663 against its 0.25 band.

**Files added by this section**

```
rung2/pair_sample_1600.py            the nested 1,600-pair sample and its gates
results2/pair_sample_1600.json       the sample, the oracle's verdicts, B-d's split
results2/pair_judgement_1600.json    1,200 calls; 400 answers reused from Stage D
results3/edge_direction_1600.json    B-a, B-d, the position split
results3/declared_order_1600.json    B-b, B-c, the recomputed coin and projection
```

Reproducible for free from the answers already paid for:

```
PYTHONHASHSEED=0 python3 -m rung2.pair_sample_1600
PYTHONHASHSEED=0 python3 -m rung3.edge_direction --source results2/pair_judgement_1600.json \
    --out results3/edge_direction_1600.json --split results2/pair_sample_1600.json
PYTHONHASHSEED=0 python3 -m rung3.declared_order --source results2/pair_judgement_1600.json \
    --out results3/declared_order_1600.json --split results2/pair_sample_1600.json \
    --accuracy results3/edge_direction_1600.json
```

Four minutes and nine minutes respectively. The 1,200 calls are not reproducible:
the proposer is not deterministic at temperature 0, and `harness/record_guard.py`
guards the record for that reason.

---

## 12. Where the order was available, and where the proposer was random

*Added 2026-08-26. `rung3/edge_sides.py` → `results3/edge_sides.json`,
`PYTHONHASHSEED=0`, 42 s, **zero API calls**. **POST-RUN**, like §9 and §10:
written after `B-a` to `B-d` were adjudicated, by someone who had already seen
`B-d` hold. **It adjudicates nothing** and no signed row moves — it is reported
beside §11's rows, never among them.*

`B-d` measured the proposer's direction **rate** on each side of the split. §11
measured what all 1,310 edges **compile into**. Neither says what each side
**buys**, and a rate is not a score: the reachable side could be carrying the
whole order and the unreachable side none of it, or the reverse, and `B-b` would
read 0.4804 either way.

All on `hibrido` pool, corpus test split 0 — `B-b`'s own cell. Each subset is
compiled **independently, through a fresh engine**, because whether an edge closes
a cycle depends on the edges already in; the edges a subset yields alone are not
the subset of the edges the whole run yielded, and both counts are published.

### Each side against its own coin, because sizes differ

**A subset with more edges scores higher for having more edges.** 654 rows and 451
rows do not start level, so comparing their raw scores would measure the split's
sizes and call it competence. Each side is therefore read against a coin on **its
own rows** — same compilation, same scoring, only the direction randomised, 200
draws — and against **its own oracle**, which is the ceiling available to any
proposer on those rows.

```
side           rows  edges    model     coin      sd     devs   oracle  o devs
reachable       451    421   0.4392   0.4288  0.0195   +0.53   0.4442   +0.79
unreachable     654    600   0.4251   0.4423  0.0296   -0.58   0.5407   +3.33
no_side         374    345   0.4553   0.4495  0.0282   +0.20   0.4332   -0.58
all            1479   1310   0.4804   0.4692  0.0266   +0.42   0.5357   +2.49
born_at floor                0.4332
```

### The two things this says

**1. Every bit of available order lives on the side a ranking cannot answer.** A
perfect chooser on the unreachable pairs scores **+3.33 coin deviations**; on the
reachable pairs it manages **+0.79**, and its headroom over the proposer there is
**0.0050** — five ten-thousandths. The pairs a free queue ranking already answers
have almost nothing left to win, whoever answers them. That is the structural
reason `B-b` could not have been won on the reachable side however good the
proposer was on it, and it is worth stating because `B-d`'s 0.8647 invites the
opposite reading.

**2. On the side that matters the proposer is indistinguishable from random.**
−0.58 deviations, which is inside noise: the honest statement is **no better than
a coin**, not *worse than one*. Its headroom to the oracle there is **0.1156**,
twenty-three times the reachable side's.

So the 0.6391 direction rate `B-d` measured on the unreachable pairs is worth
**nothing at the order level**. Getting 64% of those directions right buys no more
order than getting them at random — because a ranking-shaped error is not a random
error. When the proposer is wrong on a pair a ranking cannot answer, it is wrong
in the direction the ranking would have chosen, and correlated errors of that kind
cancel the correct answers instead of adding to them.

**And the +0.42 the whole run scores comes from the two subsets with no headroom.**
`reachable` at +0.53 and `no_side` at +0.20, on 0.0050 and −0.0221 of headroom
respectively.

### An invariant that came out exactly

`no_side`'s oracle is **0.4332**, the `born_at` floor to the digit, and its oracle
offers are **0**. Those pairs have no strict better rule, so a perfect chooser
declares nothing on them and the compiled order is arrival order. It is the one
structural check the decomposition has — it would break the moment the split and
the oracle disagreed about which pairs have a winner — and
`tests/test_edge_sides.py` pins it.

### What it changes about what to do next

**It closes the density run before it was specified.** `IDEAS.md` carried a cheap
follow-up: a population built only from unreachable pairs, 1,600 calls at four
times the density. That would sharpen a rate whose order-level value is measurably
zero. **The rate is not the bottleneck and more of it is not the answer.**

**It moves the live question to the compilation.** The oracle reaches +3.33
deviations on the same rows the proposer reaches −0.58, so the information is
there and the protocol can carry it. What loses it is either the proposer's
correlated errors or the topological sort with an arrival tie-break — and
`IDEAS.md`'s minimum-feedback-arc-set item is the free experiment that separates
those two, because it changes the compilation while holding the answers fixed.

**Files added by this section**

```
rung3/edge_sides.py         the decomposition, its coins and its oracles
results3/edge_sides.json    the record, with its provenance field
```

Reproducible with `PYTHONHASHSEED=0 python3 -m rung3.edge_sides`. Forty seconds,
zero API calls.

---

## 13. It is the answers, not the compilation — and the sort was hiding it

*Added 2026-08-26. `rung3/mfas_compilation.py` → `results3/mfas_compilation.json`,
`PYTHONHASHSEED=0`, 3 s, **zero API calls**. **POST-RUN, with an expectation
written before the run** and recorded in the module and the record. **It is not a
signed row**: it is not on `STATUS.md`'s scoreboard and it is not a calibration
event. It adjudicates nothing.*

§12 left two candidates for where the pairwise channel loses what it is told, and
did not separate them: the proposer's errors are correlated in the ranking's
direction, or the compilation loses it. This changes **only** the compilation —
same 1,479 declared edges, same rules, same cell — and separates them.

### What the baseline was quietly discarding

`try_edge` refuses any edge that would close a cycle **in the order it arrives**.
Of 1,479 declared edges it installed 1,310 and dropped **169**, and which 169
depends on nothing but sequence. The compiled order then honours every edge it
kept, so `gate_order_respects_edges` passes and the pipeline looks lossless from
inside while having thrown away 11% of what it was told.

Minimum feedback arc set keeps every edge and minimises violations. Both
compilations are therefore scored on the same fidelity metric — **violations over
all 1,479** — which is the number the two can be compared on and which no record
before this one published.

### The instrument failed its own gate first, and that is recorded

The first run of this module searched only from the `born_at` order and finished
with **28** violations on the oracle's edges where the topological sort achieved
**24**. A search that loses to the baseline at the baseline's own objective cannot
say anything about compilation: the score difference would have been a fact about
the search. The baseline is now one of three declared starts, so `mfas <=
topological` holds by construction, and `gate_beats_the_baseline` blocks the run
rather than trusting it. It is the same discipline as `harness.ceiling_check` —
measure the instrument before the instrument measures anything.

### The result

```
arm        edges  topo hon.  mfas hon.  +held     topo     mfas     gain
model       1479       1350       1413    +63   0.4804   0.4332  -0.0472
oracle      1105       1081       1100    +19   0.5357   0.5457  +0.0100
coin        1479       1103       1278   +175   0.4985   0.4362  -0.0623
born_at                                         0.4332
```

Violations fell in every arm — 129 → 66 for the model, 24 → 5 for the oracle, 376
→ 201 for the coin. **The compilation got strictly better at its stated job in all
three, and the score went the other way in two of them.**

### The three readings, and the expectation they were checked against

The expectation written before the run: *MFAS honours materially more edges; the
model's score does not improve materially; the oracle's does.* **All three held,
and the model's held more strongly than stated** — it did not fail to improve, it
fell 0.0472.

**1. The mechanism works when the input carries signal.** The oracle gains
**+0.0100** from honouring 19 more of its own edges. So a better compilation is
worth something, and cycle refusal was a real loss — for directions that are
right.

**2. The model behaves like the coin.** Both degrade under faithful compilation,
by 0.0472 and 0.0623. The proposer's declared edges are not merely uninformative
about the order: **honoured fully, they are worse than not honouring them.**

**3. The topological sort was accidentally protecting the score.** Discarding 169
edges first-come-first-served happened to discard harmful ones, and that is where
a good part of §11's 0.4804 came from. The figure stands — it is what that
compilation gives — but *what the proposer's edges buy* and *what that
compilation's lossiness buys* were not separated until now, and they are not the
same quantity.

### An exact coincidence, checked rather than assumed

The model's MFAS order scores **0.433166**, the `born_at` floor **to the digit**.
It is not the arrival order: it differs from it in **576 of 577** positions. Both
land on 431 correct of 995 test cases — the same count by different routes, which
is unremarkable on a denominator of 995 and would have been a bug on any other. It
was checked because exact equality invites suspicion, and the check is the reason
it can be reported as a coincidence.

### What keeps it comparable

Every start has the property and the search preserves it: a rule with no incident
declared edge has a delta of zero at every position, so it is never moved on its
own account and **the untouched rules keep their arrival order relative to each
other**. Their absolute indices shift as constrained rules move past them, which is
equally true of Kahn's algorithm — §11 reports 576 of 577 rules off their arrival
index for exactly that reason. **No random restarts**: they would scramble the
untouched rules against each other and change the score for a reason having
nothing to do with the edges.

**The objective never sees the truth.** It minimises violations of declared edges
and nothing else; the truth enters only to score the finished order. An optimizer
that saw the labels would be `order_search_ls`, which reaches 0.7678 and answers a
different question.

### What it settles

**The compilation is not the bottleneck, and §12's first candidate is the one that
survives.** The information is in the protocol — the oracle improves under a
compilation that keeps more of it — and the proposer's answers do not contain the
order however faithfully they are compiled. `IDEAS.md`'s minimum-feedback-arc-set
item is closed by this section, and it closed in the direction that removes an
excuse rather than one that offers a route.

**Files added by this section**

```
rung3/mfas_compilation.py        the two compilations, the arms and the gate
results3/mfas_compilation.json   the record, with its expectation field
```

Reproducible with `PYTHONHASHSEED=0 python3 -m rung3.mfas_compilation`. Three
seconds, zero API calls.

---

## 14. Nothing chooses better than chance — and 0.4824 was never reachable

*Added 2026-08-26. `rung3/edge_dropping.py` → `results3/edge_dropping.json`,
`PYTHONHASHSEED=0`, 28 s, **zero API calls**. **POST-RUN, with an expectation
written before the run.** **Not a signed row**, not on `STATUS.md`'s scoreboard,
not a calibration event.*

§13 left one route open: the cycle-refusing sort was dropping 169 edges by arrival
accident and that dropping *helped*, so a compilation that drops **deliberately**
might do better. This tests it, and it also answers a question the thread had been
assuming rather than measuring.

### The trap this is built around

**"Drop edges until the score improves" is hard rule 6 wearing a hat.** A rule
that consults the score is search with extra steps. So three constraints, all
fixed before the run:

1. **Every rule reads only the answers.** §12's reachable/unreachable split is
   derived from the **oracle** and is therefore forbidden as a dropping criterion,
   however tempting — the right diagnostic and the wrong instrument.
2. **Every rule is reported, not the best one.**
3. **Every filter is read against a random drop of the same size.** §13 showed
   dropping *at all* moves the score, so a filter compared only against "keep
   everything" measures how many edges it removed and calls it selection.

The ranking is the proposer's own: Copeland over the queue pairs it decided, from
the 1,479 answers and nothing else, ties broken by how often a queue was named a
winner and then alphabetically.

```
1. ONCALL_ESCALATION   2. SECURITY_INCIDENT   3. T3_ENGINEERING
4. BILLING_SPECIALIST  5. ACCOUNT_MANAGER     6. SELF_SERVICE_DEFLECT
7. T2_TECHNICAL        8. T1_GENERAL
```

### No filter beats its own control

```
filter          kept     topo     mfas  rnd topo      sd   devs  rnd mfas      sd   devs
keep_all        1479   0.4804   0.4332    0.4626  0.0144  +1.24    0.4344  0.0066  -0.19
consistent      1194   0.4372   0.4442    0.4509  0.0210  -0.65    0.4376  0.0184  +0.36
inconsistent     285   0.4070   0.4070    0.4271  0.0292  -0.69    0.4330  0.0325  -0.80
born_at floor          0.4332
```

Every filter sits within **0.7 deviations** of dropping the same number at random,
in both compilations. **Nothing here is a selection effect.** Keeping the
proposer's self-consistent core does nothing; keeping only the edges where it
contradicted its own majority does nothing.

### The arrival accident was not a selection either

The right control is the **same edges fed in a random arrival order** and refused
by the same mechanism — which isolates whether arrival order specifically is worth
anything. The baseline's 0.4804 sits **+1.24 deviations** above that control's
0.4626 (sd 0.0144). Suggestive, not significant, and not a rule anyone could have
chosen in advance.

> **A control that was wrong, recorded rather than quietly fixed.** The first
> version sampled 1,310 rows — the number the accident keeps. Those go through
> `try_edge` again and install about **1,166**, some 144 fewer than the baseline's
> 1,310, which are all installed by construction. The gap it reported was partly a
> smaller edge set. Measured at 20 draws before being discarded.

### And the line the thread had been aiming at was out of reach all along

**Added after seeing `consistent` land near the floor rather than near 0.4824, and
labelled as a diagnostic rather than folded in.** It changes what was *declared*
rather than which declarations are kept, so it is not a candidate filter.

A **perfect follower of that same ranking**, answering all 1,479 pairs, scores
**0.4402** topological and **0.4302** MFAS. The same ranking applied as a **lookup
over all 577 rules** scores **0.4824**.

**1,479 pairs is 4.6% of the 31,850 that could carry an edge.** A ranking applied
as a lookup orders every rule; the same ranking expressed as edges at this budget
orders 4.6% of the pairs and leaves the rest at arrival order. They are not the
same object and they do not score alike.

So **`B-b`'s 0.4824 was not reachable through this channel at 1,600 pairs by any
ranking-following strategy, perfect play included.** `B-b` is refuted as signed and
the verdict stands; what changes is what the refutation *means*. It was read as
*the proposer failed to beat a free baseline*. It is at least as much *the channel
cannot express that baseline at this budget* — and the proposer's 0.4804 is in fact
**above** the perfect ranking-follower's 0.4402 under the same compilation.

Under MFAS the distinction dissolves and everything collapses toward the floor:
model 0.4332, follower 0.4302, floor 0.4332. Which is §13 again — the variation
under the topological sort is its lossiness, not the answers.

### The expectation, and the half of it that was wrong

Written before the run: *`consistent` lands near the queue ranking's level;
`inconsistent` at or below the floor; the arrival accident is not special.*

The second and third held. **The first was wrong**, and usefully so: `consistent`
landed at 0.4372/0.4442, near the floor and nowhere near 0.4824. The reason is the
4.6% above — compiling a ranking as sparse pairwise edges is not applying it — and
that error is what produced the diagnostic that reframes `B-b`.

### What it closes

**`IDEAS.md`'s deliberate-dropping route is closed, and the channel has no
remaining excuse.** Not the budget (§10), not the compilation (§13), not the
selection of what to compile (here). What is left is the finding itself: the
proposer's competence is a queue ranking, a queue ranking is worth 0.4824 as a
lookup and about 0.44 as sparse edges, and neither is near the 0.7678 search finds.

**Files added by this section**

```
rung3/edge_dropping.py        the filters, their controls and the diagnostic
results3/edge_dropping.json   the record, with its expectation field
```

Reproducible with `PYTHONHASHSEED=0 python3 -m rung3.edge_dropping`. Thirty
seconds, zero API calls.

---

## 15. The asymmetry was never a thing — but the position effect is

*Added 2026-08-27. `rung3/answer_asymmetry.py` → `results3/answer_asymmetry.json`,
`PYTHONHASHSEED=0`, under a second, **zero API calls**. **POST-RUN**, written
after the thread closed. **It adjudicates nothing** and no signed row moves. The
four hypotheses were declared before the measurement and all four are reported,
including the drafter's favourite, which was wrong.*

Stage D came back 203 `b_beats_a` against 162 `a_beats_b`; `results2/FINDINGS2.md`
left it unexplained and it survived quadrupling, 781 against 698. It was the
pairwise thread's last genuinely open question.

### It survived because two effects were being called one thing

**`rule_b` is not a position.** The pairs are ordered by rule id, ids are assigned
in birth order, so `rule_b` is the **later-born** rule in 100% of pairs and never
necessarily the one shown second — presentation order is dealt separately and
balanced exactly. *Naming `b` more often* and *preferring the rule shown second*
are different claims about different axes. Conflating them is how this stayed open
through three sections.

That also disposes of one hypothesis before any measurement: **birth order is not
separable from the asymmetry**, since `names_b` and `names_later_born` are
necessarily the same number. It restates the question rather than answering it,
and it is kept in the table to make that visible.

### The four hypotheses and their marginals

```
                     rate      devs     base rate of the population
names_b            0.5281     +2.16     the ranking favours b   0.5260
names_broader      0.6038     +7.98     b is the narrower rule  0.4814
names_later_born   0.5281     +2.16     b is later-born         1.0000
follows_ranking    0.8073    +23.64
names_first_shown  0.5416     +3.20
```

A marginal cannot separate `H1` from `H2`: breadth and the ranking's favourite
coincide on **922 of 1,479** pairs, so each would look like the other.

### H2 — the asymmetry is the population's, not the proposer's

Two independent ways of asking, both saying the same thing.

**Symmetry.** It follows its own ranking **0.7946** when the ranking favours `a`
and **0.8188** when it favours `b` — a difference of +0.0242, **+0.93 deviations**.
A `b`-preference the ranking did not explain would have shown up here as following
it more when it happens to point at `b`. It does not.

**Prediction.** The ranking favours `b` on 0.5260 of pairs and the proposer follows
it 0.8073 of the time. Those two numbers alone predict naming `b` at **0.5160**
against an observed **0.5281** — a residual of **+0.0121, +0.93 standard errors**.

**So the asymmetry is a property of the pairs that were sampled, not of the
proposer.** The queue ranking happens to favour the later-born rule slightly more
often than not, and a ranking-follower inherits that. Nothing needs explaining.

### H1 — and the drafter's favourite hypothesis was wrong twice over

`H1` said it prefers the **narrower** rule, on the evidence of its own `why`
texts — *"La regla A es mas especifica..."*. The marginal already contradicts it:
it names the **broader** rule 0.6038 of the time, +7.98 deviations the other way.

But the marginal is not the test. **The pairs that decide are the 557 where the
ranking and breadth point in opposite directions**, because there a
ranking-follower and a breadth-preferrer choose differently:

```
                              n     follows ranking   names broader
ranking and breadth agree   922            0.8297          0.8297
they disagree               557            0.7702          0.2298
```

Where they conflict it follows the ranking **0.7702**, +12.75 deviations from a
coin, and names the broader rule only 0.2298. **Breadth is not a preference of its
own; it rides on the ranking**, which favours broad rules on 62.3% of these pairs.

So `H1` is refuted, and the interesting part is *how*: the proposer's stated reason
and its behaviour point in opposite directions. It says "more specific" and it
names the broader rule — and neither is what it is actually doing, which is
applying a queue ranking. **This is one sentence and not a measurement**: nothing
here reads those strings systematically, and a proper treatment of the `why` texts
would be its own work.

### H4 — the position effect is real, and it is not a preference

The earlier reading was that the winner is the rule shown first 0.5416 of the time,
+3.20 deviations. That is a preference. The sharper question is whether the slot
changes how **reliably** it applies its own ranking:

```
the ranking's favourite shown first :  0.8534
the ranking's favourite shown second:  0.7623
difference +0.0911, +3.50 deviations
```

**Same proposer, same ranking, nine points worse from the second slot.** It is an
accuracy effect and not a taste, it is the largest well-identified bias in the
thread after the ranking itself, and it is the one thing here that would show up in
any pairwise elicitation protocol.

### What it closes and what it leaves

**Closed.** The a/b asymmetry, which was never an effect. `IDEAS.md`'s last open
pairwise question goes with it.

**Left open, and newly sharp.** Why the second slot costs nine points of adherence.
Nothing here explains it — balanced presentation removes the trivial account, and
the remaining candidates (attention to the first-described option, the shape of the
prompt) are not distinguishable from this record. It is a property of the
elicitation rather than of this policy or this rule base, which is what makes it
worth naming.

**Files added by this section**

```
rung3/answer_asymmetry.py        the features, the conflict test, the position test
results3/answer_asymmetry.json   the record, with its four declared hypotheses
```

Reproducible with `PYTHONHASHSEED=0 python3 -m rung3.answer_asymmetry`. Under a
second, zero API calls.

---

## Files

```
rung3/order_search.py         exact ceiling, greedy search, split, references
rung3/budget_and_balance.py   label budget and balanced greedy

results3/order_search.json       ceilings, five splits, order found
results3/budget_and_balance.json supervision curve and objective comparison
```

Reproducible with `python3 -m rung3.order_search` and
`python3 -m rung3.budget_and_balance`. Zero API calls.

Step B — ILP (Popper/ILASP) as a gauge of the layer order and as a competitor
inducing rules on its own — has not been run. It remains unauthorized.
