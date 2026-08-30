# ILP as a competitor — what the proposer buys, priced

Record of August 30, 2026. `PLAN_ILP.md`, §0 signed before any figure below
existed and §1 amended and signed the same day, after the blocking checks killed
the declared search method. **Zero API calls; the inducer runs on the standard
library and finishes in under a second.**

**This record owns every figure in it.** It closes item 6 of
[`../EXTERNAL_REVIEW.md`](../EXTERNAL_REVIEW.md) and Step B of rung 3, specified
in five documents since August 2026 and never run, and it answers the question
[`../CHAT_SUMMARY.md`](../CHAT_SUMMARY.md) §3 posed:

> If an inducer with no LLM recovers the layer order, what is the proposer for?

> **PROVENANCE: PRE-REGISTERED.** Four bands with their refutation lines, signed
> before a single rule was induced, with a gate that refuses to write this record
> otherwise. **The drafter expected all four to hold. One did.**

---

## The four rows

| row | band | beam 40 | beam 120 | verdict |
|---|---|---|---|---|
| `I-a` · beats the proposer's material | > 0.8530 | **0.7759** | **0.7628** | **refuted** |
| `I-b` · covers the two starved classes | above both ceilings | T3 0.1930 ✗ · AM 0.7636 ✓ | T3 0.3684 ✓ · AM 0.7455 ✓ | **no verdict** |
| `I-c` · learns the function | ≥ 0.50 | **0.3532** | **0.3715** | **refuted** |
| `I-d` · compresses | ≤ 58 rules | **37** | **30** | holds |

**`I-b` is not reported as a verdict**, and that is `I-g4` doing the job it was
amended into existence for: the row holds at one declared beam width and is
refuted at the other, so the honest answer is that this instrument cannot decide
it. A verdict picked from the favourable beam would have been a verdict picked
after seeing the figure.

---

## 1. The answer to the question, and it depends on one thing

**On the material the proposer actually had, the inducer wins.** On half of it, it
loses. Both figures are below; the band reads the second, which is the
conservative one for the claim `I-a` makes.

```
corpus test split 0, puro, first-match-wins

  the searched order over the 577 LLM rules      0.8472    best of 65 starts, uses the oracle
  the inducer, trained on all 632 escalations    0.8814    +0.0342
  the inducer, trained on the train half (316)   0.7759    −0.0713
  `born_at`, the arrival order                   0.5216
```

**The comparison that answers the question is the first pair.** The 577 rules were
learned over all 2,000 cases — `rung3/order_search.py` declares that leakage in
its own docstring — so the inducer trained on all 632 escalations is matched to
them, contaminated in the same way and to the same degree. On that footing a
sequential-covering learner, given the same tickets and the same labels, beats an
oracle-using search over the LLM's rules by **0.0342**, in **half a second**, with
no model and no API call.

**And on half the material it loses by 0.0713**, which is `I-a`'s banded reading
and is refuted as signed. The two sentences are both true and the second is the
one the plan chose to be judged on.

> **A drafting defect of this plan, and it changes nothing.** `I-a`'s denominator
> is *corpus test split 0* and its line is **0.8530**, which is the **mean of five
> splits**. The split-0 figure is **0.8472**
> ([`../results3/order_search_ls.json`](../results3/order_search_ls.json)). The
> mismatch is the drafter's and it is 0.0058 wide; both verdicts survive it
> unchanged — 0.7759 is below both lines and 0.8814 above both — which is why the
> band is not touched. It is recorded because a line that does not match its own
> denominator is the kind of thing that is quoted later without the caveat.

---

## 2. `I-c`: it wins the arrival distribution and loses the function

```
                                            corpus test split 0      exhaustive space
  the searched order over the 577 rules                  0.8472                0.6033
  the inducer, trained on 632                            0.8814                0.4304
  the inducer, trained on 316                            0.7759                0.3532
```

**`I-c` is refuted on both training sets**, at both beams. The inducer that beats
the LLM's material on the arrivals is **0.17 worse than it as a function**.

That is the sharpest thing in this record, and it is what a surface label is for.
Sequential covering optimises coverage of the cases in front of it; the 632
escalations are the long tail of one distribution, and a list fitted to them
describes that distribution rather than the policy behind it. The searched order
over the LLM's rules is worse on the arrivals and better on the function, because
its material was written rule by rule about *cases* rather than fitted to a
sample.

**Nothing here says which is preferable.** `STATUS.md`'s *Before reading any
figure* has said since August 8 that the two surfaces answer different questions,
and this is the first time in the project that a method wins one and loses the
other by a wide margin in each.

---

## 3. `I-b`: no verdict, and the reason is worth more than the verdict

```
corpus test split 0             n     beam 40      beam 120     the 577 rules' ceiling
  T3_ENGINEERING               57      0.1930        0.3684                     0.3333
  ACCOUNT_MANAGER              55      0.7636        0.7455                     0.3578
```

`ACCOUNT_MANAGER` is over the ceiling by more than double at both beams: the
learned base cannot exceed 39 of 109 there and the inducer reaches 42 of 55 on the
test split. **For that class the material problem is the proposer's**, and it is
now measured rather than inferred: the information was in the 29 examples the
proposer also saw, and it did not write rules that used it.

`T3_ENGINEERING` straddles the ceiling — under it at beam 40, over it at beam 120 —
so the row has no verdict. §1's amendment predicted this shape before the run:
**the class has six training examples.** `SECURITY_INCIDENT` has three and
`ONCALL_ESCALATION` has **none at all — it never escalated once in the whole
n=2000 run.** A row adjudicated on six examples is adjudicated on scarcity.

**What the loop never asked about, no method can learn.** That is a finding about
the impasse loop rather than about either competitor, and it is the one this
thread adds to `IDEAS.md` rather than closing.

---

## 4. `I-d`, and what the instrument cost

`I-d` **holds**: 37 rules at beam 40, 30 at beam 120, against a band of 58, the
hidden policy's 29 and the learned base's 577. The plan declared this row the
weakest of the four before the run — the count is a function of a stopping rule
the executor writes — and it is reported with that caveat intact.

**`I-g1` passes, and it is what makes a loss readable at all.** Complete labels
over all 134,400 cases: a **28-rule** list scoring **1.000000** at beam 40 in 2.1
seconds, **29 rules** and 1.000000 at beam 120. The hidden policy is 29 rules. A
home-made baseline that loses proves nothing; this one recovers the target
exactly when the target is there to recover.

**The method the plan first declared does not work, and its failure is kept
reproducible.** §1 declared a clingo optimisation and
[`../PLAN_ILP.md`](../PLAN_ILP.md) §1's amendment records what happened;
`ilp/asp_encoding.py` is retained unmodified so the figures reproduce:

```
  60 labelled cases,  60 s     60/60 train, optimum not proved
  the real 316,       60 s     173/316 = 0.5475 train, 40-slot cap hit, not proved
  the real 316,      300 s     205/316 = 0.6487 train, cap hit, not proved
  I-g1's instance              16,128,000 `holds/2` atoms before search begins
```

It cannot fit its own training set. Five times the time bought ten points of
*training* accuracy.

---

## 5. The asymmetries, and how to read a win under them

§6 of the plan declares four, and its amendment corrects the claim that all four
favour the inducer:

1. **Batch against sequential**, and on `I-a`'s banded set **fewer examples**: the
   inducer sees 316 where the proposer saw 632. This one runs against the inducer
   on material and for it on batching.
2. **The order is free.** The inducer chooses precedence in the same pass; every
   figure it is compared against needed a separate oracle-using search.
3. **The objective is the score.** It optimises corpus accuracy directly; the
   proposer was asked to write a rule for a ticket and never saw the metric.
4. **The labels are clean** — for both, so this one is even.

**So the honest form of the result is narrower than "the inducer wins".** It is:
*a batch learner that gets the order for free and optimises the metric directly
beats, on the arrival distribution, an oracle-using search over rules a sequential
blind proposer wrote — and loses to it as a function.* Every clause is load-bearing.

---

## 6. What this does not settle

**It is one inducer and we wrote it.** `I-g1` is what makes a loss readable, and
even with it passing, this learner losing is not induction losing. Popper needs
SWI-Prolog, absent and requiring root; ILASP is a closed binary with nothing to
pin. **And the `popper` package on PyPI is not the ILP system** — it is an
unrelated CLI for reproducible papers, which is the kind of mistake that gets
discovered late and cited early.

**It says nothing about the loop.** The inducer is offline and one-shot. Whether
compiling rules *while running* is worth having is untouched by every row here.

**A hold on `I-a` would not have retracted anything, and its refutation does not
vindicate the proposer.** The banded verdict is refuted because the inducer was
handed half the material; on the matched half it wins.

---

## Files

```
ilp/language.py         the 224 conditions; the `in` restriction §2 turns on
ilp/instances.py        the four instances and the two training sets
ilp/induce.py           sequential covering, precision-first, two beams
ilp/asp_encoding.py     the superseded clingo encoding, kept so it reproduces
ilp/induce_check.py     I-g1 to I-g4, blocking, run first and alone
ilp/compare.py          the four rows, gated on the plan's two signatures
results_ilp/induce_check.json   the gate's own record
results_ilp/compare.json        the rows, both training sets, both beams
tests/test_ilp.py       the bands, the language, the gate — and no row's figure
requirements-ilp.txt    clingo, pinned, and only for the superseded encoding
```

Reproducible, in this order:

```
python3 -m ilp.induce_check      # 24 s, must pass
python3 -m ilp.compare           # 13 s
```

`--dry-run` on the comparison runs everything and writes nothing. There is no flag
that skips the signature gate.
