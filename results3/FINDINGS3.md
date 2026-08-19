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
