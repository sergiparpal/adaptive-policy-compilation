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
peldano3/order_search.py         exact ceiling, greedy search, split, references
peldano3/budget_and_balance.py   label budget and balanced greedy

results3/order_search.json       ceilings, five splits, order found
results3/budget_and_balance.json supervision curve and objective comparison
```

Reproducible with `python3 -m peldano3.order_search` and
`python3 -m peldano3.budget_and_balance`. Zero API calls.

Step B — ILP (Popper/ILASP) as a gauge of the layer order and as a competitor
inducing rules on its own — has not been run. It remains unauthorized.
