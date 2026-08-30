# PLAN_ILP — what does the proposer buy that a symbolic inducer would not

**Status: drafted by Claude on 2026-08-29, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign one. **Nothing runs and no
record is written until Sergi has signed §0**, and the signature has to land
before any figure named here exists — in its own commit, staged by name.

**Opened by Sergi on 2026-08-29.** Item 6 of
[`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md), Step B of rung 3, specified in five
documents and never run. [`STATUS.md`](STATUS.md) carried it as *open and still
unauthorized*, which under this repository's convention means the scope was his to
open; [`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md) put one condition
on it — *"comparing against a number you know is unstable says little. After this
audit"* — and that condition is met: the audit closed on 2026-08-08 and rung 3's
figures have been stable since.

**The question, in the form the repository has always posed it**
([`CHAT_SUMMARY.md`](CHAT_SUMMARY.md) §3, row 5):

> If an inducer with no LLM recovers the layer order, what is the proposer for?

**What it does not touch.** Nothing here can move rung 1's falsification of
specificity, rung 2's mechanism, or the pairwise threads. It is a **baseline**:
it measures what the same material yields to a competitor, and a baseline that
wins does not retract a finding — it reprices it.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**Every row names its denominator, its surface and — where an order is scored —
its pool.** Rows are read on the `puro` machine, because what the inducer emits is
an **ordered decision list executed first-match-wins**, which is that machine and
not the hybrid one. Scoring a decision list against a `hibrido` figure would be
the pool error [`CHAT_SUMMARY.md`](CHAT_SUMMARY.md)'s erratum of 2026-08-17
dismantles.

| id | claim | denominator | band | refuted by |
|---|---|---|---|---|
| **I-a** | **The inducer beats the proposer's material.** From the same 632 escalated cases, the induced decision list scores above what an oracle-using search extracts from the 577 rules the LLM wrote | e2e on corpus **test split 0**, `puro`, trained only on escalations falling in the train split | **> 0.8530** | **≤ 0.8530** |
| **I-b** | **The material problem is the proposer's, not the domain's.** For the two classes where the learned base has no correct rule in two thirds of its cases, the inducer writes rules that cover them | per-class accuracy on corpus test split 0 for `T3_ENGINEERING` and `ACCOUNT_MANAGER`, both classes, against the learned base's own per-class ceiling of **0.333** and **0.358** | **above the ceiling in both classes** | **at or below it in either** |
| **I-c** | **What it learns is the function, not the sample.** The same list, scored where the corpus cannot reach | e2e over the **exhaustive space**, 134,400 cases | **≥ 0.50** | **< 0.50** |
| **I-d** | **It compresses.** The list is closer to the manual's size than to the base's | number of rules in the induced list, against 29 for the hidden policy and 577 for the learned base | **≤ 58** | **> 58** |

**Signed by Sergi: Sergi Parpal (date: 2026-08-30)**

**What the drafter expects, written down so the scoreboard can score it.**
`I-a` **holds**, `I-b` **holds**, `I-c` **holds**, `I-d` **holds**. Four of four,
which is a weaker prediction than it looks and is declared as such below.

The reasoning is one paragraph. The inducer optimises the thing it is scored on,
over a hypothesis language that contains the target, with all 632 labelled
examples in front of it at once; the proposer wrote one rule at a time, blind to
the base, and never declared an order at all. **The interesting outcome is not
which wins but by how much, and on which of the four axes** — and `I-b` is the
row worth running the plan for, because it is the only one that separates *the
proposer wrote the wrong rules* from *those cases were never learnable from what
it was shown*.

**`I-d` is the weakest of the four as a test, and that is said before the run.**
The rule count is a function of the regularisation in an objective this plan's
executor writes, so a hold measures the encoding as much as the induction. It
stays because the number is worth owning — nobody has ever measured how few rules
this domain needs — and the caveat stays because a band whose value I can tune is
not a test. Compare `A-d` of [`PLAN_SENSITIVITY.md`](PLAN_SENSITIVITY.md), which
was declared weak in advance and landed at 1.00.

**If `I-a` is refuted the finding is worth more, not less.** It would say the 577
rules contain something an optimal search over the same examples does not find —
which is the first positive result this project would have about the proposer, and
the one it has been unable to produce for four rungs. The drafter does not expect
it, and says so here so that a refutation cannot later be presented as the
expected outcome.

---

## 1. The competitor, and exactly what it is given

> **[AMENDED 2026-08-30 — three corrections, all found by the blocking checks of
> §4 before any row was read, and none of them optional.]**
>
> **(1) The search method is not clingo.** §1 declared the objective *"expressed
> as clingo optimisation priorities"* and §9 defended the choice. The encoding was
> built — conditions chosen per rule slot, so grounding is linear rather than the
> **839,070** candidate bodies a body-enumerating encoding would need — and it
> does not scale:
>
> | instance | time | result |
> |---|---|---|
> | 60 labelled cases | 60 s | 60/60 train, optimum **not** proved |
> | the real 316 | 60 s | **173/316 = 0.5475** train, 40-slot cap hit, not proved |
> | the real 316 | 300 s | **205/316 = 0.6487** train, cap hit, not proved |
>
> It cannot fit its own training set, let alone `I-g1`'s 134,400 cases, whose
> fact base alone is **16,128,000** `holds/2` atoms. Five times the time buys ten
> points of *training* accuracy.
>
> **What replaces it passes `I-g1` exactly as signed.** Sequential covering,
> precision-first, beam search over the same declared language: on complete labels
> over all 134,400 cases it returns a **28-rule** list scoring **1.000000**, in
> **7.8 seconds**; at a wider beam, 29 rules and 1.000000. The hidden policy is 29
> rules. The gate that authorises changing the instrument is the one that failed,
> which is the only thing that makes it legitimate — `CLAUDE.md` on the optimizer
> audit of 2026-08-08, in those words.
>
> **The cost, stated rather than discovered later.** The competitor stops being
> *optimal under a declared objective* and becomes *a standard rule learner*. That
> is a weaker instrument and a **better-matched** one: the question this repository
> has always asked is what an inducer with no LLM recovers, and a practitioner
> reaches for sequential covering, not for an exact solver. `I-g4` changes with it
> — see §4.
>
> **(2) §6's claim that all four asymmetries favour the inducer is false**, and
> §1's split discipline is why. `rung3/order_search.py` declares the leakage in
> its own docstring: *"the 577 rules were learned over the 2000 cases… the test
> set is not data unseen by the RULES; it is data unseen by the ORDER."* So the
> proposer's rules saw all 632 escalations, and training the inducer on the
> **316** that fall in the train half hands it **less** than the proposer had.
>
> Neither training set is clean, and the amendment reports both rather than
> picking: on 316 the *rules* are handicapped and the *order* is matched, since
> the 0.8530 order was searched on train only; on 632 the rules are matched and
> the order is advantaged. **`I-a` stays banded on the 316**, which is the
> conservative choice for the claim it makes, and the 632 figure is reported
> beside it.
>
> **(3) `I-b`'s two classes are nearly absent from the material, and that was not
> known when the row was drafted.** Among the escalations:
>
> ```
>                          train half   all 632   test split
>   T3_ENGINEERING                  3         6           57
>   ACCOUNT_MANAGER                12        29           55
>   SECURITY_INCIDENT               0         3           10
>   ONCALL_ESCALATION               0         0            3
> ```
>
> **`ONCALL_ESCALATION` never escalated once in the whole run.** `I-b` is
> therefore banded on the **632** set, which is the matched one — the inducer gets
> the 6 and the 29 the proposer got — and the row carries this warning in its own
> record: *it can be refuted by scarcity rather than by induction, and if both the
> proposer and the inducer fail there, neither this plan nor the learned base can
> say whether a third method would.* §9's limit 4 said the shape of this; the
> counts make it concrete.
>
> **No band moves.** The four rows of §0 keep their numbers and their refutation
> lines to the digit. What changes is the search method, which training set each
> of two rows is read on, and one false sentence in §6.
>
> **Nothing of any row was computed to reach this.** The figures above are §4
> quantities — training-set fits, fact-base sizes, class counts and `I-g1` on an
> instance whose answer is known — none of which carries a band.

**Signed by Sergi: Sergi Parpal (date: 2026-08-30)**

*Outside the quotation deliberately: §8's gate reads signature lines at the start
of a line, and one indented into a blockquote would be invisible to it. The
drafter wrote it inside first and the check caught it.*


**Input: the 632 escalated cases of `results/llm_run.json`, with their correct
action.** That is what the proposer saw, case by case, and it is the only input
that makes `I-a` a comparison rather than an analogy. The alternative — all 2,000
— is a different and easier question and is **not** what any band reads on; it is
measured anyway and reported beside, as the inducer's own ceiling.

**Split discipline.** Rung 3's corpus test split 0 (seed 17) partitions the 2,000.
The inducer trains **only on escalations whose case falls in the train half** and
is scored on the test half. Training on escalations from the test half would score
the inducer on what it memorised, and the comparison figures it is read against —
0.8530 and the per-class ceilings — are test-split figures.

**Output: an ordered list of rules in the frozen DSL**, executed first-match-wins.
Same schema the proposer emits, same engine, no new arbitration. The order is part
of what the inducer produces, which is precisely what the proposer never supplied
and what rungs 3 and 4 had to search for.

**The objective, declared here and not tuned afterwards:** cover the training
cases with a decision list built one rule at a time; at each step take the body of
at most three conditions, over the declared language, with the highest **precision**
on the cases not yet decided, breaking ties by coverage; stop when nothing is left
to decide. The action of a rule is the majority true action over what it covers.
*(Amended 2026-08-30, above: this replaces the clingo optimisation, which does not
scale and fails `I-g1`.)*

---

## 2. The hypothesis language, and the operator that nearly broke it

The DSL's condition space is not finite in a usable sense: `in` ranges over
subsets, and `prior_tickets_30d` has 21 values, so `in` alone contributes
2²¹ conditions on one attribute. The language is therefore **declared and
enumerated**:

| operator | where | how many |
|---|---|---|
| `eq` | every attribute, every value | 47 |
| `neq` | every attribute, every value | 47 |
| `lte`, `gte` | the two numeric attributes | 50 |
| `in` | attributes with at most 5 values, subsets of size 2 … n−1 | 80 |

**224 conditions.** The `in` restriction is the one decision that could have
silently invalidated the plan: `customer_tier` has **four** values — `free`,
`pro`, `business`, `enterprise` — so the hidden policy's
`customer_tier in [business, enterprise]` is **not** `neq free`, which would also
admit `pro`. Dropping `in`, or restricting it to complements, would put the target
outside the language and make `I-g1` unreachable for a reason that has nothing to
do with induction. It is checked rather than argued: `I-g2`.

**Bodies are conjunctions of at most three conditions with distinct attributes**,
generated bottom-up from the training cases — a body enters the candidate set only
if it covers at least one training case. Three is the hidden policy's own maximum.

---

## 3. Reference figures, with the record that owns each

Nothing here is produced by this plan, and no number below may be read off this
file when it is cited later.

| figure | value | surface / pool | owning record |
|---|---|---|---|
| searched order over the 577 rules | **0.8530** | corpus test, `puro`, mean of 5 splits, each best of 65 starts | [`results3/order_search_ls.json`](results3/order_search_ls.json), owned by [`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md) |
| the same, hybrid pool | 0.7734 | corpus test, `hibrido`, same double aggregation | same |
| coverage bound over those rules | 0.9010 / 0.8540 | corpus, `puro` / `hibrido` | [`results3/FINDINGS3.md`](results3/FINDINGS3.md) §1 with its erratum |
| `born_at` floor | 0.5216 | corpus test split 0, `puro` | [`results3/floor_by_pool.json`](results3/floor_by_pool.json) |
| per-class ceiling, `T3_ENGINEERING` | 39 of 117 | corpus | [`results3/FINDINGS3.md`](results3/FINDINGS3.md) §2 |
| per-class ceiling, `ACCOUNT_MANAGER` | 39 of 109 | corpus | same |
| the learned base | 577 rules from 632 escalations | — | `results/llm_run.json` → `metrics` |
| the hidden policy under first-match-wins | 1.0000 | corpus and space | [`results/FINDINGS.md`](results/FINDINGS.md) route 2, [`results2/FINDINGS2.md`](results2/FINDINGS2.md) |

**`0.8530` is a best-of-65 and must be read as one.**
[`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md) establishes that the
65 end orders are 65 distinct behavioural machines and that comparing against the
maximum is comparing against a winning ticket. `I-a` is banded against it anyway,
and deliberately: it is the **most favourable** number the proposer's material has
ever produced, so an inducer that clears it clears everything below it, and the
row cannot be accused of picking a weak opponent. The distribution of the 65 is
reported beside the verdict.

---

## 4. Blocking checks, before any row is read

Carry no band, adjudicate nothing, are excluded from every denominator. **Each one
aborts the run.** The discipline is `harness.ceiling_check`'s and
`rung3.optimizer_check`'s: measure the instrument before the instrument measures
anything else. **It matters more here than anywhere else in this repository,
because this competitor is one we wrote** — a home-made baseline that loses proves
nothing at all.

- **`I-g1` · Step 0 for the inducer.** Given **complete** labels — every one of
  the 134,400 cases with its true action — the inducer must return a decision list
  scoring **1.0000** over the space. The target is representable (`I-g2`) and the
  labels are complete, so anything less is the search, not the material. *This is
  the check that decides whether any row below may be believed.*
- **`I-g2` · the target is inside the language.** Each of the 29 hidden rules must
  be expressible as a body in the declared language, and the list of 29 must score
  1.0000 when executed first-match-wins. Without it `I-g1` could fail for a reason
  that is not about induction.
- **`I-g3` · no leak.** The inducer sees training cases and their actions, and
  nothing else: not the hidden rules, not the layer order, not the test split, not
  `results/llm_run.json`'s rules. Checked on the inputs actually passed, the way
  `rung2/pair_judgement.py::gate_no_leak` checks the emitted text.
- **`I-g4` · the method is heuristic, and every row is read at two beam widths.**
  *(Amended 2026-08-30.)* Sequential covering proves nothing, so the original
  form of this gate — *clingo either proves the optimum or it does not* — has no
  content under the new method and pretending otherwise would be worse than
  dropping it. What replaces it is the property that can actually be checked: a
  row whose verdict changes between the two declared beam widths is **not
  reported as a verdict**. `I-g1` already passes at both (28 rules and 29 rules,
  1.000000 either way), which is what makes this a real check rather than a
  formality.

---

## 5. What it costs

**Zero API calls.** One new dependency: `clingo`, from PyPI, a wheel with no build
step, verified installing and solving on this machine at **5.8.2**.

**It does not go in `requirements.txt`.** That file is the environment the *paid*
records were produced with and its `openai` pin is what makes them rebuildable;
adding an unrelated solver to it would corrupt that meaning. A separate
`requirements-ilp.txt`, pinned the same way, with the same lock discipline.

**Runtime is the open risk and is declared as one.** The candidate space is
hundreds of conditions and thousands of bodies, and exact optimisation over
decision lists is not cheap. A time limit is therefore part of the protocol rather
than an accident: **declared before the run, recorded in the `_env`, and
surfaced by `I-g4` on every row.** If clingo cannot prove optimality within it,
that is a result about the method and gets reported as one — hard rule 6.

---

## 6. The asymmetries, declared before running

A baseline comparison is worth what its disclosed asymmetries are worth. **Three
of the four favour the inducer and the first one does not** — the amendment above
corrects a sentence that claimed all four did — and none is hidden:

1. **Batch against sequential — and, on `I-a`'s banded set, fewer examples.** The
   inducer sees its examples at once; the proposer saw one at a time and could not
   revise. But the proposer saw **632** and `I-a` bands the inducer on the **316**
   of the train half, so on that row this asymmetry runs **against** the inducer on
   the material and for it on the batching. The 632 figure is reported beside.
2. **The order is free.** The inducer emits a list, so it chooses precedence as
   part of the same optimisation. The proposer emitted unordered rules, and every
   figure it is compared against needed a separate oracle-using search to supply
   what the inducer gets for nothing.
3. **The objective is the score.** The inducer optimises corpus accuracy directly;
   the proposer was asked to write a rule for a ticket and was never shown the
   metric.
4. **The labels are clean.** The 632 come with their true action. The proposer got
   the true action too, per case — so this one is even, and it is listed to make
   clear that it was checked rather than assumed.

**What follows from them.** If the inducer wins, the honest sentence is *a batch
optimiser with the order for free beats a sequential blind proposer*, which is
weaker than *the proposer is useless* and is what `I-a` will support. If it loses
under these four advantages, that is a much stronger statement in the other
direction, which is why the refutation of `I-a` would be worth more than its hold.

---

## 7. Where the code and the record live

**Not in `harness/`, not in a rung.** As `sensitivity/` was, and for the same
reason [`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md) §8 gives: this is a
baseline against rung 1's material, not a step past rung 4.

Drafter's proposal, and the naming is Sergi's to overrule:

```
ilp/__init__.py
ilp/language.py            the 224 conditions and the candidate bodies
ilp/induce.py              the ASP encoding and the clingo call
ilp/induce_check.py        I-g1 to I-g4, blocking, run first and alone
ilp/compare.py             the four rows, gated on §0 of this file
results_ilp/FINDINGS_ILP.md
results_ilp/induce_check.json
results_ilp/compare.json
requirements-ilp.txt
```

Tests pin the four bands as named constants, the declared time limit and the
language's size, in the way `tests/test_sensitivity.py` pins `A_B_MIN_SPEARMAN` —
so that moving a band after seeing a figure is visible in a diff.

---

## 8. The gate

`compare.py` refuses to **write its record** while §0 of **this file** is
unsigned. No flag skips it; `--dry-run` builds the encoding, runs `I-g1` to
`I-g4` and writes nothing.

**It reads `PLAN_ILP.md` and no other plan**, and it counts **every** line
beginning `**Signed by Sergi:`, requiring all of them filled — the shape
`sensitivity/sweep.py` arrived at after `PLAN_SENSITIVITY.md` acquired a second
signature and a gate that stopped at the first would have reported `ok` over an
unsigned amendment.

One constant fixed here, before any figure exists, and not to be tuned
afterwards: **`SPLIT_SEED = 17`**, which is rung 3's own.

---

## 9. What this plan cannot settle, declared before it runs

1. **It is one inducer, and we wrote it.** `I-g1` is what makes a loss readable at
   all, and even with `I-g1` passing, *this* encoding losing is not *induction*
   losing. Popper needs SWI-Prolog, which is not installed and needs root; ILASP
   is a closed binary with no source to pin. **And the `popper` package on PyPI is
   not the ILP system** — it is an unrelated CLI for reproducible papers, which is
   the kind of mistake that would have been discovered late and cited early.
2. **It says nothing about the loop.** The inducer is offline and one-shot. The
   experiment this project is about is a system that compiles rules while it runs,
   and no row here touches whether that loop is worth having.
3. **A hold on `I-a` does not retract anything.** The four asymmetries of §6 are
   the reading, and every one of them favours the inducer.
4. **The two starved classes may be unlearnable from 632 cases for reasons that
   are nobody's fault.** `I-b` compares against the learned base's ceiling on the
   same examples, which is the fairest available control — but if both the
   proposer and the inducer fail there, this plan cannot say whether a third
   method would.
