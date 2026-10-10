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

> **[ERRATUM 2026-10-10] Matched on the tickets, not on the labels.** The inducer
> trained on all 632 was handed the true queue of every one; the proposer saw the
> same tickets and chose their queues itself, right on 245 of the 632 (§5's
> erratum). And the contamination is not of the same degree: **316** of those
> escalations fall in test split 0, and **371 of its 995 cases, 0.373,** are
> identical to an example this inducer was trained on with its true label. On
> those same 316 tickets the proposer chose right **124** times, and its rules
> carry what it chose. So *"given the same tickets and the same labels"* is false,
> 0.8814 against 0.8472 is not like for like, and how much of the **+0.0342** rests
> on those 371 cases is not measured. The train half reaches none of them — the
> split groups by case identity — which is one more reason the band reads the 316.
> Figures from `python3 -m ilp.labels`, into [`labels.json`](labels.json).
>
> **[NOTE 2026-10-10, later] Measured since, POST-RUN: all of it.** The searched
> order is right on 337 of the 371 and the inducer on all of them; on the other 624
> they tie, 506 to 506, at both beams. §7.

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

> **[ERRATUM 2026-10-10] The information was in the labels, and the proposer
> never had them.** It saw the 29 tickets and named `ACCOUNT_MANAGER` on **one**:
> 14 went to `T2_TECHNICAL`, 7 to `BILLING_SPECIALIST`, 4 to `T3_ENGINEERING`, 2
> to `T1_GENERAL` and 1 to `SELF_SERVICE_DEFLECT`. **Only 2 of the 577 rules route
> to that queue**, and those two supply the base's whole ceiling there, 39 of 109:
> one was born on that one ticket, the other on a `T1_GENERAL` ticket the proposer
> sent there by mistake. So the problem is still the proposer's, but on the acting
> axis — choosing the queue — and not on the writing of rules, which are the two
> axes `CLAUDE.md` asks to keep apart. This half of `I-b` sets an inducer handed
> the label 29 times against a proposer that named it once, and it cannot show
> that the information was in what the proposer saw. `T3_ENGINEERING`'s six
> escalations, two named right, are too few to read either way. Figures from
> `python3 -m ilp.labels`.

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

> **[ERRATUM 2026-10-10] The fourth asymmetry is not even: the proposer was never
> given the label, and the honest form is missing a clause.** `run_shadow` passes
> every proposer the truth as `true_action_hint`. The mocks return it;
> `OpenRouterProposer.propose` drops it and sends the ticket alone, under a prompt
> whose first instruction is to *decide* the queue. `tests/test_llm_path.py` has
> pinned that since August 7, 2026, three weeks before the plan said otherwise,
> and rung 1's record agrees:
>
> ```
>                                             right    of     rate
>   the proposer, over the escalations          245   632   0.3877   the run's proposal_action_accuracy
>   the same, where it named a queue            245   579   0.4231   34 failed, 19 named none
>   its 577 rules, against the birth ticket     244   577   0.4229
>   the inducer's labels, train_632             632   632   1
>   the inducer's labels, train_316             316   316   1
> ```
>
> **So three of the four favour the inducer outright, and this one most** — which
> is what the plan's §6 counted in its own header, against the item's *even*. The
> honest form, with the clause it was missing:
>
> *a batch learner **handed the true queue of every example, which the proposer
> had to choose**, that gets the order for free and optimises the metric directly
> beats, on the arrival distribution, an oracle-using search over rules a
> sequential blind proposer wrote — and loses to it as a function.*
>
> **No figure and no verdict moves**, and three passages of this record carry
> their own erratum: §1's *same labels*, §3's *information in the 29 examples* and
> §6's *matched half*. Both refutations stand with one more advantage on the
> inducer's side than the plan counted. **And no baseline in this repository
> competes for the decision with the information the proposer had**: `keep_k` and
> `random_k` are handed the true action by design, declared in
> `harness/proposers.py`, and the semantic cache of `harness/cache_baseline.py`
> caches the truth as if the LLM had given it. The figures are owned here;
> `python3 -m ilp.labels` reproduces them into [`labels.json`](labels.json),
> POST-HOC: they were computed while verifying this erratum, before that module
> was written.
>
> **[NOTE 2026-10-10, later] The honest form narrows once more.** §7 measured
> where the win on the arrivals comes from: all of it from the test cases the
> inducer was handed. On the cases neither side had labelled it ties the searched
> order, so *beats, on the arrival distribution* holds only through the answers it
> was given.
>
> **[NOTE 2026-10-10, later still] And handed the proposer's answers instead, it
> loses to the proposer's own rules.** No baseline here competes for the decision
> with the proposer's information, and that still holds. §8 holds a control on
> the compilation: the same inducer, trained on the queues the proposer chose,
> scores 424 and 437 of 995. The proposer's rules, run in arrival order with no
> truth anywhere, score 519.

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

> **[ERRATUM 2026-10-10] Matched on the tickets only.** On all 632 the inducer had
> every true queue, the proposer chose them, and 371 of the test split's 995 cases
> were identical to its labelled examples. §1's and §5's errata.

---

## 7. Where the +0.0342 comes from — POST-RUN

> **PROVENANCE: POST-RUN.** Asked for on 2026-10-10, after §1's erratum left it
> open. The expectation was written in `ilp/margin.py`'s docstring and committed
> before the first run. Two readings were added after reading it, and are
> labelled so in the module and in [`margin.json`](margin.json). Not a signed
> row, not on `STATUS.md`'s scoreboard, not a calibration event.

**All of it comes from the 371.** On the test cases the 632-trained inducer was
handed the answer to, it is right on all 371 and the searched order on 337. On
the other 624, which neither side had labelled, they tie at 506, at both beams.

```
corpus test split 0, puro                    the 371   the 624    total
  the searched order over the 577 rules          337       506      843   0.8472
  the inducer, train_632, beams 40 and 120       371       506      877   0.8814
  margin                                         +34         0      +34  +0.0342

  the pool's ceiling: some matching rule right   359       536      895
  the inducer, train_316, beam 40                324       448      772   0.7759
  the inducer, train_316, beam 120               315       444      759   0.7628
```

The order is split 0's, rebuilt by rung 3's own search: it reproduces the
published row, and a replay case by case gives the same cases right as its masks.
The 371 are the 316 test-half escalations, of which the order gets 288, and 55
duplicates, of which it gets 49. **On the 316 the proposer had named the right
queue 124 times**, and the base the order searched over gets 288 of them right.

**The tie on the 624 is a tie of counts, not of cases.** At beam 40 each side is
right on 51 cases the other gets wrong, and 67 defeat both; at beam 120 it is 65
each, and 53. On the 371 the order's 337 are all among the inducer's.

**The expectation, clause by clause:**

- *By construction, the 632-trained lists decide all 371 right.* **Holds.**
- *2. The 371 carry the whole margin or more.* **Holds, on its edge.** The order
  is right on exactly 337, the number at which the 624 carry nothing.
- *3. The order is right on a smaller share of the 371 than of the 624.*
  **Fails: 0.9084 against 0.8109.** The drafter's reason was that the 371 are
  where the base was weakest when they arrived. They are where it is strongest
  now:
  - 594 of the 632 escalations were CONFLICTs, cases that rules of two queues
    already matched.
  - The base ends with a right rule for 359 of the 371, whatever queue the
    proposer named. The pool's ceiling is 0.9677 there, against 0.8590 on the
    624.
  - The inducer that saw none of the 371 labelled is better on them too: 0.8733
    against 0.7179 at beam 40, and 0.8491 against 0.7115 at beam 120.

  The 624 were decided by a rule when they arrived and were never asked about,
  and no rule is right for one case in seven of them.

**What it does to §1 and §5.** §1's +0.0342 is the answer key: the 34 cases
among the 371 that the order gets wrong and the inducer was handed. On the cases
neither side saw labelled, the inducer does exactly as well as an oracle-searched
order over the proposer's rules, and no better. §5's honest form narrows once
more:

*a batch learner handed the true queue of every example, which gets the order
for free and optimises the metric directly, ties, on the arrivals neither side
had labelled, an oracle-using search over the rules a sequential blind proposer
wrote; it beats it only by the cases it was handed, and loses to it as a
function.*

No figure of §1 and no verdict moves. Figures from `python3 -m ilp.margin`, into
[`margin.json`](margin.json).

---

## 8. The control: the inducer on the queues the proposer chose — POST-RUN

> **PROVENANCE: POST-RUN.** Asked for on 2026-10-10, after §7. The expectation
> was written in `ilp/chosen.py`'s docstring and committed before the first run.
> Two readings were added after reading it, and are labelled so in the module
> and in [`chosen.json`](chosen.json). Not a signed row, not on `STATUS.md`'s
> scoreboard, not a calibration event.

**Handed the proposer's answers instead of the truth, the inducer falls below the
proposer's own rules, even in arrival order.** This is the same inducer, on the
same tickets, with each labelled by the queue the proposer named for it. The
training sets are the 579 escalations on which it named one, and the 286 of them
in the train half. Every list is scored against the truth:

```
corpus test split 0, puro, 995 cases        right   accuracy    space   AM of 55   rules
  the proposer's queues, 579, beam 40         424     0.4261   0.4425       0       200, at the cap
  the proposer's queues, 579, beam 120        437     0.4392   0.4436       0       197
  the proposer's queues, 286, beam 40         451     0.4533   0.4628       0       105
  the proposer's queues, 286, beam 120        413     0.4151   0.4556       0        95
  the proposer's rules, arrival order         519     0.5216   0.3148
  the proposer's rules, searched order        843     0.8472   0.6033
  the truth, 316 tickets, beams 40 / 120  772 / 759            0.3532 / 0.3715   21 / 24    37 / 30
  the truth, 632 tickets, beams 40 / 120  877 / 877   0.8814   0.4304 / 0.3939   42 / 41    46 / 54
```

On §7's partition, the four lists get 146 to 170 of the 371 and 257 to 293 of
the 624. The searched order gets 337 and 506.

**The expectation, clause by clause:**

- *1. Every list on the proposer's queues scores below the searched order.*
  **Holds**, by 392 to 430 cases.
- *2. The labels are worth more than the tickets: the 579 tickets the proposer
  labelled score below the 316 labelled with the truth.* **Holds**: 424 against
  772 at beam 40, 437 against 759 at beam 120.
- *3. The bet: the inducer compiles the proposer's answers better than the
  proposer did, scoring above `born_at`'s 519.* **Fails**, at 424 and 437. At
  beam 40 the list hit the 200-rule cap with 26 examples undecided. At beam 120
  it did not, and still falls short by 82.
- *4. `ACCOUNT_MANAGER` goes with the labels: at or below the base's ceiling,
  0.3578.* **Holds, at 0 of 55** in all four lists. The lists handed the truth
  reach 41 and 42. The proposer named that queue twice.

**What the control says.** The inducer's advantage in §1 was its labels. Given
the proposer's answers, it compresses them badly: 95 to 200 rules, against 30 to
54 on the truth, and it fits only 549 to 566 of its own 579 labels. On the
arrivals it decides worse than the rules the proposer wrote from the same
answers, run in the order they were born, with no truth anywhere. That is the
first comparison in this record made on the same information, and the
proposer's rules win it. Two limits apply:
- It is one inducer, precision-first and unregularised, which fits noisy labels
  case by case; §6's first limit applies to it in full.
- The proposer's rules here are the 577 it installed, so the 2 queues named on a
  rule that validation rejected train the inducer and no rule.

**And over the space, the proposer's queues beat the truth, through one
attribute.** This reading was not bet on, and was made after the first run:

```
space, 134,400 points                    keyword half          no keyword
  most common true queue, its share      SECURITY_INCIDENT 0.75   T2_TECHNICAL 0.2964
  the truth, the four lists              0.1500 to 0.2292       0.5064 to 0.6377
  the proposer's queues, the four lists  0.5702 to 0.6119       0.2993 to 0.3169
```

Half the space carries the security keyword, and three quarters of that half
goes to `SECURITY_INCIDENT`. The proposer sends keyword tickets there. The
escalations hold only three true `SECURITY_INCIDENT` cases, so the lists handed
the truth barely learn the mapping. On the half without the keyword, those
lists are about twice as good, and the lists on the proposer's queues sit near
that half's majority share. The keyword is a handful of the arrivals, which is
why it moves the space and not the test split.

No figure of §1 to §7 and no verdict moves. Figures from `python3 -m ilp.chosen`,
into [`chosen.json`](chosen.json).

---

## Files

```
ilp/language.py         the 224 conditions; the `in` restriction §2 turns on
ilp/instances.py        the four instances and the two training sets
ilp/induce.py           sequential covering, precision-first, two beams
ilp/asp_encoding.py     the superseded clingo encoding, kept so it reproduces
ilp/induce_check.py     I-g1 to I-g4, blocking, run first and alone
ilp/compare.py          the four rows, gated on the plan's two signatures
ilp/labels.py           POST-HOC, 2026-10-10: who had the labels, §5's erratum
ilp/margin.py           POST-RUN, 2026-10-10: where the +0.0342 comes from, §7
ilp/chosen.py           POST-RUN, 2026-10-10: the inducer on the proposer's queues, §8
results_ilp/induce_check.json   the gate's own record
results_ilp/compare.json        the rows, both training sets, both beams
results_ilp/labels.json         the erratum's figures, behind four gates
results_ilp/margin.json         §7's figures, behind five gates, and the expectation
results_ilp/chosen.json         §8's figures, behind four gates, and the expectation
tests/test_ilp.py       the bands, the language, the gate — and no row's figure
tests/test_ilp_labels.py   how labels.py counts — and no figure
tests/test_ilp_margin.py   how margin.py counts — and no figure
tests/test_ilp_chosen.py   how chosen.py builds and reads — and no figure
requirements-ilp.txt    clingo, pinned, and only for the superseded encoding
```

Reproducible, in this order:

```
python3 -m ilp.induce_check      # 24 s, must pass
python3 -m ilp.compare           # 13 s
python3 -m ilp.labels            # under a second; POST-HOC, §5's erratum
python3 -m ilp.margin            # about 40 s; POST-RUN, §7
python3 -m ilp.chosen            # about 30 s; POST-RUN, §8
```

`--dry-run` on the comparison runs everything and writes nothing. There is no flag
that skips the signature gate.
