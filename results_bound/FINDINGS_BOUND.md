# How much of the residue is slack — findings

Record opened on October 17, 2026, under [`PLAN_BOUND.md`](../PLAN_BOUND.md).
Sergi signed §0 on 2026-10-17, before any figure below existed, in a commit of
its own: *PLAN_BOUND §0 singed by Sergi*. The stage's record,
[`score.json`](score.json), names that commit in its `_env` as `93444ac`, its
hash on the branch it was made on. A rebase merge gives it a new hash on `main`
with the same tree, so it is named here by its subject. **This record owns every
figure in it.**

**The stage adjudicated the four signed rows on 2026-10-17: three hold and one
is refuted.**

- **Over the space, most of the residue `STATUS.md` asks about is slack, and it
  is certified.** On the pure pool, no order over the 134,400 cases scores above
  0.8028, against the coverage bound's 0.8784. The audited search reached
  0.7905, so at least 86% of its 0.0879 residue is unattainable by any order
  (`H-a` holds). On the hybrid pool no order scores above 0.7767, against
  0.8531, and the search reached 0.7557: at least 78% of the residue is slack
  (`H-b` holds).
- **So the search is within 0.0123 of the best order on the pure pool, and
  within 0.0210 on the hybrid one.** That is all that remains open of the
  question, and the certificate cannot say how it splits.
- **It settles neither pool** (`H-c` holds).
- **On the corpus's train halves the certificate closes less, not more**: a
  median of 0.67 of the residue over the ten instances, against a line of 0.75
  (`H-d` is refuted). It closes 0.44 to 0.65 of it on the pure pool and 0.68 to
  0.78 on the hybrid one. Between 7 and 23 cases per half stay unresolved.

> **PROVENANCE: PRE-REGISTERED.** `H-a` to `H-d` were signed before any of their
> figures existed. **`H-e` is reported, not adjudicated**, and every figure in it
> is computed here for the first time. Nothing in this record was selected after
> the verdicts. Zero API calls.

---

## What was run

`PYTHONHASHSEED=0 python3 -m bound.score`, on 2026-10-17, from the signing
commit with a clean tree: 102 s, nearly all of it the suite, and zero API calls.
The record is [`score.json`](score.json), and it carries every certificate.

**The blocking checks passed again before any cycle was packed on rung 1's
rules.**

- **`H-g1`.**
  - The suite is green, 1,671 tests.
  - All twelve instances reproduce their published coverage bounds.
  - Their signatures score random orders as `score_order` does.
- **`H-g2`.** The hidden policy: no cycle on the space's two pools or the
  corpus's pure pool, and every certificate verifies.
- **`H-g3`.** On 2,000 instances small enough to enumerate every order:
  - none of the certified bounds is below the exact optimum, and 1,770 equal it;
  - all 1,174 inflated certificates are refused.
- **`H-g4`.** Signed.

**And the stage's own two checks passed on all twelve instances.** Every
certificate passed `verify`, which rebuilds it from the masks alone. And no
certified bound fell below the score an order had reached. Either failure would
have stopped the stage before it wrote anything.

**Notation**, the plan's.

- `CB` is the coverage bound in cases and `A` the best searched score a record
  publishes.
- `ν` is the cases the certificate shows every order loses, and `TB = CB − ν`
  is the certified bound.
- The **residue** is `CB − A`, and the **share** is `ν` over it.

On the space `A` is published to four decimals, so its residue and its share are
read to that precision.

---

## The four rows

| row | surface and pool | `CB` | `A` | `ν` | `TB` | residue → after | share | band | verdict |
|---|---|---|---|---|---|---|---|---|---|
| `H-a` | space, pure | 118,060 (0.8784) | 0.7905 | 10,165 | 107,895 (0.8028) | 0.0879 → 0.0123 | **0.8602** | ≥ 0.50 | **holds** |
| `H-b` | space, hybrid | 114,659 (0.8531) | 0.7557 | 10,274 | 104,385 (0.7767) | 0.0974 → 0.0210 | **0.7847** | ≥ 0.50 | **holds** |
| `H-c` | space, both | | | | | | met on neither | met on neither | **holds** |
| `H-d` | corpus train halves, both | per instance, below | | | | | median **0.6665** | ≥ 0.75 | **refuted** |

Neither space share is *thin*. Read through the rounding of `A`, they lie in
0.8597 to 0.8607 and 0.7843 to 0.7851, far from their line.

**The ten instances of `H-d`.** Counts are cases of each split's train half.

| split | pool | n | `CB` | `A` | `ν` | `TB` | residue | after | share |
|---|---|---|---|---|---|---|---|---|---|
| 0 | pure | 1,005 | 907 | 884 | 15 | 892 | 23 | 8 | 0.6522 |
| 0 | hybrid | 1,005 | 862 | 830 | 25 | 837 | 32 | 7 | 0.7812 |
| 1 | pure | 1,005 | 908 | 874 | 19 | 889 | 34 | 15 | 0.5588 |
| 1 | hybrid | 1,005 | 867 | 819 | 34 | 833 | 48 | 14 | 0.7083 |
| 2 | pure | 1,019 | 920 | 879 | 18 | 902 | 41 | 23 | 0.4390 |
| 2 | hybrid | 1,019 | 877 | 826 | 38 | 839 | 51 | 13 | 0.7451 |
| 3 | pure | 1,000 | 897 | 867 | 16 | 881 | 30 | 14 | 0.5333 |
| 3 | hybrid | 1,000 | 856 | 809 | 32 | 824 | 47 | 15 | 0.6809 |
| 4 | pure | 998 | 909 | 871 | 19 | 890 | 38 | 19 | 0.5000 |
| 4 | hybrid | 998 | 858 | 802 | 41 | 817 | 56 | 15 | 0.7321 |

The median of ten is the mean of the fifth and sixth, 0.6522 and 0.6809. No
instance met.

**The drafter expected all four to hold, and trusted `H-a` and `H-b` least. Both
held, clear of their lines. The row refuted is `H-d`, the one trusted more.**

### What the verdicts say

**1. Over the space, the coverage bound is loose by at least 0.0756 on the pure
pool and 0.0764 on the hybrid one.** Those are `ν` over the 134,400 cases. They
are most of each residue: the 2026-08-08 erratum to `FINDINGS3.md` §4 called the
pure residue *evidence, not proof*, that the bound is *somewhat loose*. It is
loose by most of it, and that is proved: the certificate is in the record, and
`verify` checks it from the masks.

**2. So the audited search over the space is close to the best order there is.**
On the pure pool it is at most 0.0123 below it, and on the hybrid one at most
0.0210. Whatever search weakness the space hides fits inside those two figures.
Exact optimisation is what would split them, as `STATUS.md` said of the whole
residue. It now has a seventh of that room on the pure pool and a fifth on the
hybrid one.

**3. The certificate settles neither pool**, as `H-c` bet. On each, 0.0123 and
0.0210 is far above the rounding of the published score.

**4. On the corpus, the surface changed the answer, the other way from the bet.**
§0 argued that the train halves, where each order was fitted, would close more
than the space, and set the line at 0.75 to be refuted if they did not. They
closed less. Every pure-pool half closed less than either pool over the space,
0.44 to 0.65, and every hybrid half closed less than the space's hybrid pool,
0.68 to 0.78. **What is left is 7 to 23 cases a half.** It could be slack the
certificate cannot see or the search's shortfall, and nothing here splits them.

---

## The structure the certificate rests on — `H-e`, reported

| instance | classes | contested cases | signatures | of them with one right class (cases) | nodes | cycles | `ν` by cycle length | `ν` across the 17 starts |
|---|---|---|---|---|---|---|---|---|
| space, pure | 361 | 117,200 | 3,714 | 931 (41,565) | 990 | 295 | 2: 10,165 | 9,995 to 10,165 |
| space, hybrid | 312 | 113,039 | 3,498 | 1,614 (66,476) | 936 | 356 | 2: 10,084 · 3: 140 · 4: 50 | 10,069 to 10,274 |
| corpus, pure, five halves | 353 to 357 | 885 to 910 | 520 to 549 | 35 to 44 (55 to 80) | 332 to 347 | 10 to 13 | nearly all 2 | a spread of 0 or 1 |
| corpus, hybrid, five halves | 288 to 293 | 814 to 838 | 487 to 506 | 101 to 109 (187 to 206) | 299 to 323 | 20 to 31 | nearly all 2 | a spread of 1 to 3 |

**What the table shows, and it is reported, not adjudicated.**

- **Almost all of the certified loss is two-case cycles.** These are pairs of
  cases each of whose right rules are all wrong for the other. On the pure pool
  over the space, all of it is. Longer cycles add 190 cases on the hybrid pool
  and a handful on the corpus.
- **Merging interchangeable rules does real work.** 577 rules become 361 classes
  on the space's pure pool and 312 on its hybrid one: copies, and rules that
  match the same cases.
- **Cases with a single right class are a minority**: 35% of the contested cases
  on the pure space and 59% on the hybrid. On the corpus's pure halves they are
  6% to 9%, and on its hybrid halves 23% to 25%.
- **Containment is what makes the space's certificate possible**, since most
  contested cases have several right classes. The pure halves of the corpus,
  where single-right cases are scarcest, are where the certificate closed least.
  That is a correlation across ten instances and two surfaces, not a cause.
- **The starts barely matter.** On the space the seventeen starts spread by 170
  and 205 cases, about 2% of `ν`. The start kept was a shuffle, 9 and 4. On the
  corpus they spread by 0 to 3 cases.
- **The space's certificates took 2.3 and 1.6 seconds.** Each certificate
  carries one case per signature in every cycle, so anyone can run `verify` on
  it.

---

## What this settles, and what it does not

**It answers `STATUS.md`'s first open item as far as a certificate can.**

- **Over the space, most of the residue is slack**: at least 86% on the pure
  pool and 78% on the hybrid one. Not a heuristic's failure to reach a bound,
  but a proof that no order reaches it.
- **The search's possible shortfall over the space is at most 0.0123 and
  0.0210.**
- **The audit's two readings of the bound** were *not loose* on the corpus and
  *somewhat loose* over the space. On the space it is loose by most of the
  residue. On the corpus's train halves, the only corpus instances measured
  here, it is loose by 15 to 41 cases of about a thousand. That is 44% to 78%
  of each half's residue. Dated notes in `FINDINGS3.md` §4 and
  `FINDINGS_AUDIT.md` point here.

**What it does not settle**, as §10 of the plan declared before it ran:

- **The remainder.** 0.0123 and 0.0210 over the space, 7 to 23 cases per train
  half. In increasing cost, three things would narrow it:
  - a stronger certificate, such as the exact loss of cases that share a pool,
    or the exact least loss over small blocks of rules;
  - a longer search, which would be a new instrument;
  - exact optimisation with a solver.
- **The test halves.** No order was searched on them, so a bound there says
  nothing about the search.
- **Other bases, and rung 4's figures.** The certificate runs on any instance.
  None of those was in the rows.
- **Why the corpus closed less.** The pure halves, with the fewest single-right
  cases, closed least. Whether the certificate is weaker there or the search is,
  this record cannot say.

---

## Files

```
results_bound/score.json   the checks, H-a to H-d, H-e, and every certificate
bound/plan.py              the gate and §8's constants; §0's lines
bound/certificate.py       the argument, the finder, verify, brute force
bound/instances.py         the twelve instances and what the records publish
bound/gates.py             H-g1 to H-g4
bound/score.py             the stage
```

Reproducible with `PYTHONHASHSEED=0 python3 -m bound.score`, about two minutes,
nearly all of it the suite, and zero API calls. `--dry-run` runs the checks and
writes nothing.
