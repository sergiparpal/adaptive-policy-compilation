# PLAN_SENSITIVITY — how much of rung 1's failure is the correlation, and how much is this policy

**Status: drafted by Claude on 2026-08-29, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing runs and no
record is written until Sergi has signed §0**, and the signature has to land
before any figure named here exists — in its own commit, staged by name.

**This plan exists because the same objection has now been raised three times by
three readers who did not know about each other.**
[`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md) §9.1 states it:

> The hidden policy may be adversarial to specificity by construction. In it,
> priority and number of conditions are nearly orthogonal *by design*. That makes
> the falsification correct —one counterexample is enough to knock down
> "specificity is reliable"— but it says nothing about how often real policies
> have that shape.

An outside reading of the public tree reached it independently on 2026-08-29
([`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md) §1.4), and the erratum of that date in
[`results/FINDINGS.md`](results/FINDINGS.md) sharpened it: the policy was written
by the same author as the engine that fails on it. §9.1 wrote the limit down and
left it. **This plan measures it instead of writing it down a fourth time.**

**What it does not touch.** The falsification of specificity is not at stake here
and no row below can move it. It rests on an impossibility internal to the
policy — `H01` must beat `H03` and `H16` must beat `H24`, incompatible under any
criterion monotone in the number of conditions — and a frequency measurement
cannot reach an impossibility. **What is at stake is the generalization**: whether
rung 1's 0.5875 is what this shape of policy costs, or what *this* policy costs.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them — the convention `PLAN_ORDER_METRICS.md` adopted after two dead zones.

**Every row names its denominator here, before the run**, and **every row names
its surface**. Rows are read on the **exhaustive space** unless the row says
otherwise, because a synthetic policy has no arrival distribution of its own: the
corpus is 2,000 draws over attributes that were sampled without reference to any
policy, so it is a legitimate second surface and is reported everywhere, but the
space is the one the bands are set on.

**Amended 2026-08-29, before signature and before any figure of this plan
exists.** Sergi tightened two bands: `A-b` from `≥ 0.80` to `≥ 0.85`, and `A-d`
from `≥ 0.50` to `≥ 0.60`. Both moves make the row **harder** to hold; no band was
loosened, and no claim, denominator, surface or refutation convention changed. The
drafter's expectations below are unchanged, and what each tightened row now
tolerates is stated with them.

**It is recorded because it changes what the scoreboard may read into those two
rows.** [`STATUS.md`](STATUS.md)'s count of signed rows is *a fact about the
drafter*; `A-b` and `A-d` are now the drafter's claims with the **signer's** lines
on two of them. A hold or a miss on either is weaker evidence about the drafter's
calibration than the other three, and the row that the plan is really worth
running for — `A-a` — is untouched by this.

| id | claim | denominator | band | refuted by |
|---|---|---|---|---|
| **A-a** | **The hidden policy is not an outlier in its own family.** At its own ρ, its e2e under specificity sits inside the family's spread | the family draws at the ρ bin containing the hidden policy, e2e on the space, published catch-all encoding | inside the central **90%** of that bin | outside it |
| **A-b** | **The curve is real**: e2e under specificity rises with ρ across the swept range | median e2e per ρ bin, space | Spearman(ρ, median e2e) **≥ 0.85** | **< 0.85** |
| **A-c** | **Alignment is not enough**: even at maximum ρ, specificity does not execute the policies, because equal counts still tie and a tie with different actions is CONFLICT | median e2e at the top ρ bin, space | **≤ 0.95** | **> 0.95** |
| **A-d** | **The shape is common, not exotic**: at ρ = 0 most policies contain at least one *required* precedence pair that the condition counts violate, so no monotone function of specificity can execute them | fraction of draws in the ρ = 0 bin with ≥ 1 violation; structural, no engine involved | **≥ 0.60** | **< 0.60** |
| **A-e** | **The default rule is a pedestal, not the shape**: correcting the catch-all's rank lifts the curve without bending it | \|Spearman(ρ, median e2e) published − Spearman(ρ, median e2e) corrected\|, space | **≤ 0.15** | **> 0.15** |

**Signed by Sergi: I adopt §0 with the two bands amended today at my request — A-b at ≥ 0.85 and A-d at ≥ 0.60 — and the other three rows as drafted. (date: 2026-08-29)**

**What the drafter expects, written down so the scoreboard can score it.**
`A-b`, `A-c`, `A-d` and `A-e` hold. **`A-a` is refuted**, and it is the row worth
running the plan for.

**The two tightened rows are still expected to hold, and this is what each now
tolerates.** `A-b` is a Spearman over **13** bin medians, so `< 0.85` requires
`Σd² > 54`: several bins badly out of order, not one inversion — a curve with a
single adjacent swap still scores 0.99. Moving the line from 0.80 to 0.85 removes
the range where the row could have been held by a visibly ragged curve, which is
the right direction for a row whose whole claim is *the curve is real*. `A-d` is a
fraction over 100 draws in one bin, and the drafter expects it **well above either
line**: at ρ = 0 the counts are permuted at random across a structure whose
required inequalities number in the hundreds — the hidden policy alone yields at
least the 199 that `hidden_priority` declares — so a draw with *zero* violations
would need an almost perfect accident.

**Which makes `A-d` the weakest of the five as a test, at 0.60 no less than at
0.50, and that is said here rather than discovered afterwards.** If it lands near
1.00 it will have confirmed something the impossibility proof already implies,
and its value will be the *number* it puts on «common», not the verdict. The row
stays because that number is worth owning; the caveat stays because a band both
lines clear is not a test.

The reasoning is one paragraph. A random permutation of the condition counts
across the layer structure hits a given ρ by many different arrangements; the
hidden policy hits its ρ by one particular arrangement, the one a person writing
a real triage manual produces — **broad overrides on top**. `H03`
(`has_security_keyword`, one condition, layer 0) and `H16` (`product == "api"`,
one condition, layer 4) are broad rules placed high, and the rules that rob them
are narrow rules placed low. That is not what ρ measures; ρ would be the same if
the broad rules sat at the bottom. So the drafter expects the hidden policy to
score **below** its own family at its own ρ.

**If `A-a` is refuted the finding gets narrower and more useful, not weaker.**
The honest headline stops being *specificity-based arbitration fails* and becomes
*specificity-based arbitration fails on policies with broad overrides on top,
which is how layered manuals are written* — a claim about a recognisable class
rather than about one file. If `A-a` holds, the objection §9.1 raised three times
is answered and the 0.5875 generalizes to the family as drawn.

---

## 1. The one knob, and everything held against it

**ρ is the Spearman rank correlation between a rule's layer index and its number
of conditions**, computed over the rules of the policy. The hidden policy's own ρ
is approximately −0.18; **the run recomputes it and no row reads it from this
file.**

**The knob is the assignment, not the material.** For each draw the generator
permutes a **fixed multiset of condition counts** across a **fixed layer
structure**, and rejects until the achieved ρ falls in the target bin. Held
constant across every point of the sweep, so that ρ is the only thing that moves:

| held fixed | value | why |
|---|---|---|
| number of rules | 29 | so the count of pairs that can collide does not move with ρ |
| number of layers | 8 | the stratification depth is not the variable |
| layer sizes | the hidden policy's: 3, 5, 4, 2, 6, 3, 3, 3 | same |
| multiset of condition counts | the hidden policy's, exactly | this is what gets permuted; drawing new counts would move ρ *and* the specificity distribution together |
| action vocabulary | the 8 of `harness.domain` | |
| domain, attribute weights, corpus | frozen — hard rule 4 | the corpus is policy-independent by construction, so the same 2,000 cases are relabelled per policy |
| the engine | `harness.dsl.RuleEngine`, untouched — hard rule 1 | the point is to measure *this* arbitration, not a new one |

**The hidden policy is a member of its own family**, reachable by supplying its
own permutation. That is what makes `A-a` a comparison and not an analogy, and
check `A-g3` pins it.

**Two encodings, every point, always.** Each policy is measured twice: with the
catch-all encoded as the DSL forces it (`severity gte 1`, one condition, which
ties with every one-condition rule) and with the catch-all given its true rank
below everything. Reporting one curve would leave `A-e` unanswerable and would
repeat rung 1's own confound at family scale.

---

## 2. What is measured per draw

**Per policy, on both surfaces, under both encodings:** coverage, CONFLICT rate,
silent error, e2e — the four quantities `harness.ceiling_check` already prints,
computed the same way.

**And one structural quantity that needs no engine at all**, which is `A-d`'s:
the **violation count**. For every ordered pair `(i, j)` with `i` in an earlier
layer than `j`, whose extensions overlap over the space and whose actions differ,
specificity can only get it right if `count(i) > count(j)`. Collect those required
inequalities and count how many the actual counts violate. **Zero violations means
some monotone function of specificity could execute the policy; one or more means
none can.** It is `results/FINDINGS.md`'s impossibility proof turned into a
counter, and it is free.

---

## 3. Reference figures, with the record that owns each

Nothing here is produced by this plan, and no number below may be read off this
file when it is cited later.

| figure | value | surface | owning record |
|---|---|---|---|
| specificity, perfect policy loaded | e2e **0.5875**, CONFLICT 505 | corpus | [`results/FINDINGS.md`](results/FINDINGS.md), route 1 |
| birth order, perfect policy loaded | e2e **1.0000** | corpus | same |
| the exhaustive space | **134,400** combinations | — | same, and `harness/ceiling_check.py` |

**Deliberately absent: the catch-all control's two rows.** They exist as an
in-memory probe reported in [`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md) §3, owned
by no record and carrying that warning. **No band above depends on them**: `A-e`
compares two curves this plan produces itself, precisely so that an unowned
number cannot enter a signed row. See §6.

---

## 4. Blocking checks, before any row is read

Carry no band, adjudicate nothing, are excluded from every denominator — the
convention `PLAN_ORDER_METRICS.md` uses for `G1`–`G6`. **Each one aborts the
run.**

- **`A-g1` · Step 0 for this instrument.** Every generated policy must be executed
  at **e2e 1.0000** by first-match-wins in layer order, over the exhaustive space.
  A generator that emits policies the engine cannot execute even with the correct
  arbitration measures the generator, not specificity. *This is the same check
  that voided a paid run on 2026-08-05 and the same one `rung3.optimizer_check`
  makes before the optimizer is trusted.*
- **`A-g2` · the knob is the knob.** Achieved ρ within 0.02 of the bin centre for
  every draw, reported as a distribution and not asserted.
- **`A-g3` · parity with the hidden policy.** Supplied its own permutation, its
  own conditions and its own actions, the generator's evaluation path must return
  **0.5875 / 505 / 0.2140** on the corpus and reproduce
  `harness.ceiling_check` exactly. Without this, `A-a` compares two different
  measurement paths and means nothing.
- **`A-g4` · every rule reachable.** No rule fully shadowed by the ones above it
  under first-match-wins, and exactly one catch-all, in the last layer. A policy
  with dead rules has a different effective size, which would confound ρ with N.

---

## 5. What it costs

**Zero API calls.** Standard library. Measured on this machine, naive
per-case evaluation, before any optimisation:

| | |
|---|---|
| build the space, once | 0.18 s |
| one policy, corpus (2,000) | 0.01 s |
| one policy, space (134,400) | 0.90 s |

**Reference configuration — 13 ρ bins × 100 draws × 2 encodings: about 40
minutes.** 500 draws would be about 3 h 20 min and is not the drafter's
recommendation for a first pass: 100 draws resolve a central-90% comparison,
which is all `A-a` asks.

**That is an upper bound on the cost, not a floor.** `rung2.engine2.Space`
already builds per-`(attribute, value)` bitmasks over the 134,400 cases and
computes an extension as an AND of big integers rather than a sweep. An
implementation on those masks would cut the space column by a large factor. The
naive figure is given because it is the one that was measured, and the executor
picks.

---

## 6. The dependency on the default-rule control, which is interpretive and not numeric

[`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md) item 2 measures the catch-all's
contribution **to the published 0.5875 specifically**, and owns that figure in a
record with `provenance: POST-RUN`. This plan measures the same effect **across
the family**, in `A-e`, from two curves it generates itself.

They are not substitutes and the order matters: **item 2 first.** If this plan
runs first, `A-e` will report that correcting the catch-all lifts the curve, and
nobody will know whether the published figure for the hidden policy moves the
same way — which is the number a reader of rung 1 actually holds. Item 2 costs
minutes.

**No row here is blocked on it**, and that is deliberate: a signed band that
depends on an unowned figure is a band that can be adjudicated by choosing when
to measure the other thing.

---

## 7. Where the code and the record live

**Not in `harness/`.** `hidden_policy.py`, `domain.py` and `dsl.py` are frozen
(hard rule 1), and the whole point is to leave rung 1's record reproducing
untouched while measuring around it. A new top-level package, as `rung2/` was
created rather than editing `dsl.py`.

Drafter's proposal, and the naming is Sergi's to overrule:

```
sensitivity/__init__.py
sensitivity/generator.py       the family: permute counts over a fixed layer structure
sensitivity/generator_check.py A-g1 to A-g4, blocking, run first and alone
sensitivity/sweep.py           the sweep, both surfaces, both encodings
results_sensitivity/FINDINGS_SENSITIVITY.md
results_sensitivity/sweep.json
```

**`results5/` is deliberately not proposed.** Numbering it as a rung would make
it rung 5, and both `ARBITRATION_REPORT.md` §8 and the 2026-08-29 outside reading
independently warn against answering the last rung's instrumentation with another
rung. This is a control on rung 1, not a step past rung 4.

Tests pin `A-g3`'s parity and the two constants of §8, in the way
`tests/test_declared_order.py` pins `P_D_MARGIN` and `P_E_BAND` — so that moving
a band after seeing a figure is visible in a diff.

---

## 8. The gate, and why a free run gets one

`rung2/pair_judgement.py` is gated because it spends. **This plan spends
nothing, and still gets a gate**, because what the gate protects is not money: it
is that the bands were signed before the figures existed. On a free run the only
thing standing between a draft and a post-hoc band is the commit order, and a
commit order is an honour system.

`sweep.py` refuses to **write its record** while §0 of **this file** is unsigned.
No flag skips it; a `--dry-run` builds every policy, runs `A-g1` to `A-g4` and
writes nothing.

**It reads `PLAN_SENSITIVITY.md` and no other plan.** Until 2026-08-25 the
existing gate read `PLAN_PAIRWISE.md` whatever it was gating, so a run under a
different plan would have found a closed thread's signature and reported `ok`. A
gate that reads the wrong file is worse than no gate, because it is believed.

Two constants fixed here, before any figure exists, and not to be tuned
afterwards: **`SWEEP_SEED = 17`** and **`SWEEP_DRAWS = 100`**.

---

## 9. What this plan cannot settle, declared before it runs

1. **The family is synthetic and its realism is asserted, not measured.** It holds
   the hidden policy's layer structure and count multiset fixed, which makes the
   comparison in `A-a` exact and makes the family *this policy's neighbourhood*
   rather than *the space of real manuals*. How often real triage manuals put
   broad overrides on top is not measurable in this repository and is not
   measured anywhere else in it either. `A-d` is the closest this gets, and it is
   a statement about the family.
2. **ρ is one summary of a structure that has more than one dimension.** The
   drafter's own expectation for `A-a` is that ρ misses the thing that matters —
   *where* the broad rules sit, not how counts correlate with depth. If `A-a` is
   refuted, the follow-up question is what statistic *does* capture it, and this
   plan does not name one. That is the right order: measure that ρ is
   insufficient before proposing its replacement.
3. **It says nothing about the learned base.** Every figure here is over
   hand-authored stratified policies with the perfect arbitration available. The
   577-rule learned base is a different object with a different failure, already
   recorded in [`results3/FINDINGS3.md`](results3/FINDINGS3.md).
4. **It cannot rehabilitate specificity.** No outcome of any row makes
   specificity-based arbitration usable here, for the reason in the header. The
   best case for specificity is that `A-a` holds and rung 1's number turns out to
   be typical of its family — which is a statement about how far the number
   travels, not about whether the mechanism works.
