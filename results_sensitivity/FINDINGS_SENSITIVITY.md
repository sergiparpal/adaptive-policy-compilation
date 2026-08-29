# The sensitivity sweep — how much of rung 1's failure is this policy's shape

Record of August 29, 2026. `PLAN_SENSITIVITY.md`, §0 signed **before any figure
below existed** and §1 amended and signed the same day, after the blocking checks
killed the first construction. 13 ρ bins × 100 draws × 2 surfaces × 2 encodings,
**74 seconds and zero API calls**.

**This record owns every figure in it.** It closes item 5 of
[`../EXTERNAL_REVIEW.md`](../EXTERNAL_REVIEW.md) and answers the objection §9.1 of
[`../ARBITRATION_REPORT.md`](../ARBITRATION_REPORT.md) raised and left written
down, which three independent readers reached separately.

> **PROVENANCE: PRE-REGISTERED.** Five bands with their refutation lines, signed
> by Sergi in their own commit before a single policy was drawn, with a gate that
> refuses to write this record otherwise. It is the first pre-registered work
> outside the pairwise threads, and the two rows Sergi tightened at signature time
> — `A-b` from 0.80 to 0.85 and `A-d` from 0.50 to 0.60 — carry his lines rather
> than the drafter's.

---

## The five rows

Read on the **exhaustive space**, **published** catch-all encoding — the surface
and encoding §0 fixes.

| row | claim, in short | band | measured | verdict |
|---|---|---|---|---|
| `A-a` | the hidden policy is not an outlier in its own family | inside the central 90% of its bin | **0.2725** against **[0.0534, 0.2235]** | **refuted** |
| `A-b` | e2e rises with ρ | Spearman ≥ 0.85 | **−0.9945** | **refuted** |
| `A-c` | even at maximum ρ, specificity does not execute the policies | median ≤ 0.95 | **0.0605** | holds |
| `A-d` | the shape that defeats specificity is common | ≥ 0.60 of the ρ=0 draws | **1.00** | holds |
| `A-e` | the default rule is a pedestal, not the shape | \|ΔSpearman\| ≤ 0.15 | **0.0000** | holds |

**Three hold, two refuted.** The drafter's expectation, recorded in §0 before the
run: *`A-b`, `A-c`, `A-d` and `A-e` hold; `A-a` is refuted.* Four of five verdicts
came out as predicted — **and the one it predicted correctly it predicted for the
wrong reason**, which §3 below is about.

---

## 1. The curve is real, it is strong, and it runs the other way

```
        ρ    space published    space corrected    corpus published
   −0.6000            0.2443             0.2676              0.3605
   −0.5000            0.2164             0.2337              0.3362
   −0.4000            0.1932             0.2105              0.3030
   −0.3000            0.1717             0.1883              0.2908
   −0.2000            0.1585             0.1724              0.2605
   −0.1532            0.1378             0.1538              0.2565     ← the hidden policy's ρ
   −0.1000            0.1439             0.1561              0.2587
    0.0000            0.1200             0.1410              0.2110
    0.1000            0.1054             0.1193              0.1990
    0.2000            0.0927             0.1076              0.1767
    0.3000            0.0751             0.0879              0.1490
    0.4000            0.0637             0.0806              0.1412
    0.5000            0.0605             0.0727              0.1388
```

Median e2e per bin, 100 draws each. **Spearman(ρ, median e2e) = −0.9945 on both
surfaces and under both encodings** — one inversion in thirteen bins, at
ρ = −0.1.

`A-b` asked for `≥ 0.85` and got `−0.9945`, so it is **refuted as signed** and the
verdict stands. But the honest sentence beside it is not *the curve is not real*:
the curve is about as real as a curve gets, and **the drafter had the sign of ρ
backwards.**

**Why the sign is what it is, and it is arithmetic rather than a surprise.**
ρ is the correlation between a rule's **layer index** and its **number of
conditions**. Specificity picks the rule with the most conditions; first-match-wins
picks the one in the earliest layer. The two agree when the rules with more
conditions sit **earlier**, which is *negative* ρ. `A-b` asserted that alignment
improves as ρ *rises*, and what rising ρ actually describes is narrow rules pushed
deep — the arrangement on which specificity is most wrong.

So the row that was drafted as *the curve is real* turned out to be a claim about
its direction, and the direction was wrong. The measurement is the sharper
statement in both branches: **specificity does better the more a manual puts its
narrow rules first, and that is a property of the arrangement rather than of the
material.**

---

## 2. The mechanism, measured rather than argued

The chain has one link and both halves of it are measured.

```
        ρ    required inequalities    violated    rate    median e2e (space, published)
   −0.6000                     232         121   0.517                          0.2443
   −0.3000                     236         145   0.622                          0.1717
   −0.1532                     233         157   0.674                          0.1378
    0.0000                     235         168   0.721                          0.1200
    0.3000                     235         193   0.821                          0.0751
    0.5000                     233         206   0.882                          0.0605
```

A *required inequality* is §2 of the plan's: for a pair `(i, j)` with `i` in an
earlier layer, overlapping extensions and different actions, specificity can only
get it right if `count(i) > count(j)`. It needs no engine.

- **Spearman(ρ, violation rate) = 1.0.** Perfectly monotone.
- **Spearman(violation rate, median e2e) = −0.9945.**
- **The number of required inequalities does not move** — 230 to 236 across the
  whole sweep. It is the fraction violated that rises, not the population.

So ρ moves e2e by moving how many of the precedence relations the condition counts
contradict, which is `results/FINDINGS.md`'s impossibility proof turned into a
dose-response curve.

---

## 3. `A-a` is refuted, and it is refuted **upward**

```
                          hidden policy    its bin's central 90%    bin max    rank
space, published                 0.2725       [0.0534, 0.2235]       0.3058   100 / 101
corpus, published                0.5875       [0.1215, 0.4125]       0.5265   101 / 101
```

**On the corpus the hidden policy beats every one of the 100 draws at its own ρ.**
On the space it beats 99 of 100.

The drafter expected `A-a` to be refuted and said why: *the hidden policy hits its
ρ by the one particular arrangement a person writing a real triage manual produces
— broad overrides on top — and the rules that rob them are narrow rules placed
low; so the drafter expects the hidden policy to score **below** its own family at
its own ρ.* **It scores above.** The verdict matches the prediction and the
reasoning behind it does not.

**What that does to rung 1's headline is the opposite of what §0 anticipated.**
§0 wrote: *"If `A-a` is refuted the finding gets narrower and more useful… the
honest headline stops being 'specificity-based arbitration fails' and becomes
'specificity-based arbitration fails on policies with broad overrides on top'."*
That reading assumed the refutation would be downward — an unusually hostile
policy. Refuted upward says the reverse:

> **Rung 1's 0.5875 was measured on nearly the most favourable arrangement of its
> own material, and specificity fails on it anyway.** The number is not a worst
> case. Of 100 alternative manuals built from the same conditions, the same
> condition counts, the same actions and the same layer structure, at the same ρ,
> not one does better on the corpus.

The finding gets **broader**, not narrower.

**And ρ is not what makes it favourable.** Its violation rate is 0.634 against its
bin's median 0.674 and range [0.608, 0.725] — better than average and squarely
inside. That small an edge in the counter does not produce a rank of 100 of 101.
Whatever the hidden policy has, neither ρ nor the violation count captures it, and
this plan does not name a statistic that does. §9's limit 2 anticipated exactly
this and said the follow-up question is *what statistic would* — that question is
now the open one, and it is sharper than when it was written.

---

## 4. `A-c`, `A-d`, `A-e`

**`A-c` holds, by a distance that makes the band look generous.** At the top bin
the median is **0.0605** against a line of 0.95. Alignment does not rescue
specificity at any point of the sweep: the best bin in the whole family, ρ = −0.6,
medians **0.2443** on the space and **0.3605** on the corpus. There is no ρ at
which this arbitration executes a layered policy.

**`A-d` holds at 1.00, and the number is the result rather than the verdict.**
Every one of the 100 draws at ρ = 0 contains at least one violated required
inequality — the median draw violates **168 of 235**. The band was drafted at 0.50,
tightened by Sergi to 0.60, and the measurement is 1.00; the drafter said before
the run that `A-d` was the weakest of the five as a test, *at 0.60 no less than at
0.50*, and it was. What it buys is the number: **the shape that makes specificity
impossible is not common in this family, it is universal.** The hidden policy is no
exception — 147 violations of 232.

**`A-e` holds exactly.** Correcting the catch-all's rank lifts e2e at every bin, by
**0.0122 to 0.0234**, and changes the ordering of the bins by nothing at all: the
two Spearman coefficients are equal to four decimals, so the difference is
**0.0000**. The default rule is a pedestal, precisely as drafted. That also
transfers the item-2 control's finding from one policy to a family: the encoding
artifact is a constant offset, not a distortion of the shape.

---

## 5. What the blocking checks cost, and what they caught

`A-g1` to `A-g4` ran first and alone, and **`A-g4` aborted the plan's original
construction**. `results_sensitivity/generator_check.json` owns those figures; the
short version is in §1 of the plan, dated and signed, and it is why there is an
amendment at all:

- A member of the family was originally *the 29 hidden rules re-assigned to the 29
  positions*. **0 of 24,888** ρ-accepted permutations had zero dead rules, the
  hidden policy itself has three, and mean dead rules ran **5.39 at ρ = −0.6 to
  16.38 at ρ = +0.5**, Spearman(ρ, dead) = **1.0**.
- The curve would then have confounded *alignment helps* with *the policy got
  smaller*, at correlation 1 with the knob.
- The amended construction synthesises bodies from the manual's own 23 conditions
  and requires each rule to claim a case no earlier rule has claimed. **Effective
  size is 29 in every draw of the sweep**, so the confound cannot exist.

`A-g3` is the licence for everything above: the bitmask evaluation path returns
what the frozen `RuleEngine` returns on the hidden policy, field by field —
**0.5875 / 505 / 0.2140** on the corpus — and, unasked, also reproduces the
default-rule control's 0.6880 and 0.3458.

---

## 6. Limits, declared

**The acceptance rate falls with ρ and is collinear with it.** Requiring every rule
to be live accepts 56.5% of count-permutations at ρ = −0.6 and 18.4% at ρ = +0.5;
Spearman(acceptance rate, median e2e) = 0.945. The *sign* of the curve is explained
by the violation-rate chain, which is structural and does not depend on the filter
— but **this design cannot separate the filter's selection effect from ρ's own**,
and a reader who wants the magnitude to the second decimal should know that.

**The family is synthetic and its realism is asserted, not measured** — §9's limit
1, sharpened by §1's amendment: the bodies are drawn now too, not only the
arrangement. What it buys is that every member is a policy someone could execute,
with all 29 rules live, which the first construction's members were not.

**ρ is one summary of a structure with more than one dimension** — §9's limit 2,
and §3 above is it coming true.

**It says nothing about the learned base**, and **it cannot rehabilitate
specificity** — §9's limits 3 and 4, both untouched by any row.

---

## Files

```
sensitivity/generator.py          the family: counts permuted, bodies synthesised
sensitivity/measure.py            the evaluation path, both surfaces and encodings
sensitivity/generator_check.py    A-g1 to A-g4, blocking, run first and alone
sensitivity/sweep.py              the sweep and the five rows, gated on the plan
results_sensitivity/generator_check.json   the gate's own record
results_sensitivity/sweep.json             1,300 draws, per bin and per draw
tests/test_sensitivity.py         the bands, the grid, the parity, the gate —
                                  and no figure of the sweep
```

Reproducible, in this order:

```
PYTHONHASHSEED=0 python3 -m sensitivity.generator_check   # 61 s, must pass
PYTHONHASHSEED=0 python3 -m sensitivity.sweep             # 74 s
```

`--dry-run` on the sweep draws every policy, re-runs `A-g2` and `A-g4` on each and
writes nothing. There is no flag that skips the signature gate.
