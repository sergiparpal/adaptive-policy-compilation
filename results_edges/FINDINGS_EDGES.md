# What the edges declared at write time bought — findings

Record opened on October 5, 2026, under [`PLAN_EDGES.md`](../PLAN_EDGES.md).
Sergi signed §0 on 2026-10-05, before any figure below existed, in a commit of
its own: *PLAN_EDGES.md signed by Sergi*. The stage's record,
[`score.json`](score.json), names that commit in its `_env` as `c0a8df7`, its
hash on the branch it was made on. A rebase merge gives it a new hash on `main`
with the same tree, so it is named here by its subject. The post-run readings
are a second record, [`readings.json`](readings.json). It was written from the
commit that adds them, *edges/readings.py: the post-run readings of
PLAN_EDGES.md's stage, in a record of their own*, and names the stage's record
as its source. **This record owns every figure in it.**

**The stage adjudicated all three signed rows on 2026-10-05: one holds and two
are refuted.**

- **On the cases they decided, the edges were right a third of the time**
  (`W-a` holds).
- **Over the function, the direction the proposer declared points at the better
  rule three times in four** (`W-b` is refuted upward).
- **Against a coin, the proposer's directions buy more right decisions, but
  only because they resolve more conflicts.** Among the cases they resolve,
  they are right no more often than a coin (`W-c` is refuted; the reading is
  post-run).
- **The same edges are right over the function and wrong where tickets arrive.**
  47 of the 50 installed edges are one rule of thumb: on a ticket with the
  security keyword, `SECURITY_INCIDENT` wins. The hidden policy sends three
  quarters of such tickets there over the space, and 20 of the corpus's 71
  (post-run).

> **PROVENANCE: PRE-REGISTERED.** `W-a` to `W-c` were signed before any of their
> figures existed. **`W-d` is reported, not adjudicated**: its census reproduces
> figures the drafter computed with a truth-free probe before drafting, which §0
> declares as already seen, and the rest of it is computed here for the first
> time. Everything labelled **POST-RUN** below was computed after the verdicts
> existed, by someone who had seen them, and is a reading, not a bet. Those
> figures were first computed by hand, and then by `edges/readings.py`. Its
> record, `readings.json`, carries that provenance, and every one of them
> reproduces there. Zero API calls.

---

## What was run

`PYTHONHASHSEED=0 python3 -m edges.score`, on 2026-10-05, from the signing commit
with a clean tree: 87 s, zero API calls. The record is
[`score.json`](score.json).

**The blocking checks passed again before any label of `D` was read.**

- **`W-g1`.** The hybrid engine executes the hidden policy at 1.0000 on the
  corpus and on the space, and the suite is green, 1,200 tests. The three Stage
  B records reproduce themselves. The space labels partition the 134,400 points
  and give `T2_TECHNICAL` its published 36,720.
- **`W-g2`.** Each run rebuilds exactly with its edges. Without them it departs
  only from ACTION to CONFLICT, on 37, 16 and 61 cases.
- **`W-g3`.** The counterfactual rebuild is the record given the declared
  directions, and the replay without edges given none. The coin is identical
  under three hash seeds.
- **`W-g4`.** Signed.

**Surfaces.**

- **`W-a` and `W-c`: the corpus.** That is `generate_corpus(2000, seed=17)` in
  arrival order: `D`, the cases the edges decided in `PLAN_REUSE.md`'s three
  Stage B runs.
- **`W-b`: the exhaustive space**, over the shared region of each installed
  edge. Its corpus definition is in `W-d`.
- **The static readings: both.** Each run's final base as a machine, deciding
  every case at once. That is not the run.

## The census — the figures §0 declared, measured

| | run 1 | run 2 | run 3 | all |
|---|---|---|---|---|
| edges tried by `try_edge` | 33 | 6 | 36 | 75 |
| refused as `no_solapan` | 3 | 0 | 8 | 11 |
| accepted | 30 | 6 | 28 | 64 |
| — consistent with subsumption, never installed | 13 | 0 | 1 | 14 |
| — **installed** | **17** | **6** | **27** | **50** |
| installed, joining rules with different actions | 17 | 6 | 27 | 50 |
| installed, born on a conflict / a coverage screen | 17 / 0 | 6 / 0 | 12 / 15 | 35 / 15 |
| installed, the newborn rule winning / losing | 17 / 0 | 6 / 0 | 18 / 9 | 41 / 9 |
| installed, sharing no corpus case | 0 | 0 | 7 | 7 |
| installed, sharing two corpus cases or fewer | 6 | 2 | 21 | 29 |
| **`D`, the cases the edges decided** | **37** | **16** | **61** | **114** |

**Every figure §0 declared from the probe reproduces exactly**, the ranges
included. Per edge, the shared corpus cases run from 1 to 18, 1 to 8 and 0 to 14,
and the shared space points from 200 to 16,800, 420 to 5,040 and 40 to 16,800.
No accepted edge fell on a pair already installed, and no coin draw had an edge
refused for closing a cycle.

## The three rows

**Every verdict is read pooled over the three runs** (§2.1 of the plan), and
each run's value sits beside it.

| row | statistic | run 1 | run 2 | run 3 | pooled | band | verdict |
|---|---|---|---|---|---|---|---|
| `W-a` | share of `D` decided right | 0.1351 (5/37) | 0.3750 (6/16) | 0.4262 (26/61) | **0.3246** (37/114) | < 0.50 | **holds** |
| `W-b` | installed edges pointing at the better rule, space | 0.9231 (12/13) | 1.0000 (6/6) | 0.6154 (16/26) | **0.7556** (34/45) | < 0.60 | **refuted** |
| `W-c` | coin draws scoring at least the proposer | 0.1255 | 0.0715 | 0.0135 | **0.0005** | ≥ 0.05 | **refuted** |

None of the three is thin. `W-a`'s error is 0.1036, clustered by `winner_id`
over six rules (§5.8), and the value is 0.1754 from its line. `W-b`'s is 0.0641
over 45 qualifying edges. `W-c`'s Monte Carlo error is 0.0005.

**The drafter expected all three to hold, and trusted `W-b` least, then `W-c`.
Both were refuted.** One of three called right: the row it trusted most.

### What the verdicts say

**1. On the cases they decided, the edges were right a third of the time.**
`W-a` holds at 0.3246: 37 right decisions and 77 silent errors. The base they sit
in is right 0.41 to 0.52 of the time it decides
([`FINDINGS_REUSE.md`](../results_reuse/FINDINGS_REUSE.md), Stage C), so the
edges decide worse than the rest of it. **Six rules are credited with all 114
decisions.** A decided case is credited to the oldest rule left undefeated, and
the newborn that declared the edge was usually siding with an older rule of its
own queue. In run 1 a single rule, `R0021`, is credited with all 37, right 5
times.

**2. Over the function, the declared direction points at the better rule three
times in four.** `W-b` is refuted upward at 0.7556: 34 of 45 edges with a strictly
better rule over their shared region, counted as
[`FINDINGS3.md`](../results3/FINDINGS3.md) §9 counts it. Ties: none. Edges whose
two rules are never right there: 5. That is above what the pairwise question drew,
0.6978 at 400 pairs and 0.7312 at 1,600, on the same definition. **The row's
claim, that write time is the weaker channel, is false over the function.**
The populations differ, as §0 said they do, and the next section says what this
one is made of.

**3. `W-c` is refuted, and what refutes it is resolution, not accuracy.**
*POST-RUN reading; the verdict stands as signed.* The proposer's directions
decide all 114 cases: 37 right, 77 wrong. A coin draw, on average, decides 18.88
right, 38.44 wrong and leaves **56.68 unresolved**.

- **Flipping an edge does not hand its cases to the other rule. It leaves the
  conflict open.** On a conflict screen the newborn takes the action of one of
  the contenders and declares that it beats the others. Inverted, the losers
  beat the newborn, but still not the contender it sided with. Flipping every
  edge leaves 112 of the 114 cases in CONFLICT.
- **Among the cases a coin does resolve, it is right 0.3272 of the time on
  average** (sd 0.0935), against the proposer's 0.3246. 52.35% of draws do at
  least as well.
- **Net of its errors, the proposer is worse than a coin.** Right minus wrong is
  −40 for the proposer, against a coin's mean of −19.55 (sd 10.58). 97.55% of
  draws do at least as well.
- **It holds run by run.** Among resolved cases, 52%, 53% and 52% of draws do at
  least as well as the proposer. Net, 99.6%, 75.7% and 73.5% do.

**The statistic §0 signed rewards resolving, and the drafter did not see it.**
§5.10 of the plan anticipated a flipped edge closing a cycle, which never
happened, and not this. It is a defect of drafting, declared here. **It moves no
verdict: `W-c` stands refuted as signed.** What it measures is that the proposer's
directions decide where a coin's leave a conflict.

### The mechanism — one rule of thumb, right over the function and wrong where tickets arrive

*POST-RUN. Computed after the verdicts, to read them;
[`readings.json`](readings.json).*

**47 of the 50 installed edges have `SECURITY_INCIDENT` as the declared winner,
on a shared region inside `has_security_keyword = True`.**

- **38 are `SECURITY_INCIDENT` over `T2_TECHNICAL`.** On the space, 28 of them
  point at the better rule and 10 at the worse.
- **The rest of the 47** are over `T1_GENERAL`, `BILLING_SPECIALIST` and
  `SELF_SERVICE_DEFLECT`. On the space, 4 point at the better rule and 5 are
  over regions where neither rule is ever right.
- **The other 3 edges** are `T2_TECHNICAL` over `SELF_SERVICE_DEFLECT`. On the
  space, 2 point at the better rule and 1 at the worse.

**The hidden policy splits that region by tier and severity.**

- **The rules.** `H01` and `H02` send a ticket with the security keyword to
  `SECURITY_INCIDENT` when its tier is business or enterprise, or its severity
  is 2 or lower. `H03` sends the rest to `T2_TECHNICAL`.
- **Over the space** that is 12 of the 16 tier and severity cells: 50,400 of
  the 67,200 keyword points, three quarters, read off the space's labels.
- **Over the arrivals** it is 20 of the corpus's 71 keyword tickets. The other
  51 are `T2_TECHNICAL`.

**So the proposer declared the space's majority, and the arrivals carry its
minority.**

**On `D` that is most of the story.**

- **The keyword decision.** 94 of the 114 cases were sent to
  `SECURITY_INCIDENT` by rules conditioned on the security keyword, and 26 were
  right. All 68 wrong ones were `T2_TECHNICAL`.
- **The other 20** were sent to `T2_TECHNICAL`. `R0014` decided 11, all right.
  `R0027` decided 9, all wrong: their true queue was `SELF_SERVICE_DEFLECT`.
- **The split of §5.9.** Some contending rule carried the true queue on 90 of
  the 114 cases, and the edges picked it on 37. 53 errors are of direction and
  24 are material. In run 1, 20 of the 32 errors are material.
- **By the corpus definition, `W-b` reads 0.4118**: 14 of 34 edges, with 4 ties
  and 12 where neither rule is ever right. On the space it is 0.7556.

**Pointing every edge the way the space prefers buys nothing on the arrivals.**
The oracle arm turns each edge towards `W-b`'s better rule. Pooled, it decides 37
right, 63 wrong and 14 unresolved, against the proposer's 37, 77 and 0. In run 3
it trades 13 wrong decisions for 13 conflicts and gains no right one.

**And the rare class is where the edges paid off.**

- **`SECURITY_INCIDENT` gained.** The rules' right decisions on it were 5, 6 and
  18 by run ([`FINDINGS_REUSE.md`](../results_reuse/FINDINGS_REUSE.md)), and 5,
  6 and 15 of them came through an edge.
- **The price was paid in `T2_TECHNICAL`.** 32, 10 and 26 of its tickets were
  sent to `SECURITY_INCIDENT` instead.

**Which class to protect is the choice of objective function that `FINDINGS3.md`
§3 describes. The edges made it, and nothing declared it.**

### The final bases as machines, on both surfaces (`W-d`)

Each run's final base deciding every case at once, with and without its
installed edges. **This is not the run**: it decides early cases with rules born
later, which is why its figures differ from the run's own.

| | run 1 | run 2 | run 3 |
|---|---|---|---|
| **corpus** e2e, with / without edges | 0.4035 / 0.3985 | 0.4470 / 0.4430 | 0.5245 / 0.5090 |
| corpus silent error, with / without | 0.5941 / 0.5875 | 0.5528 / 0.5521 | 0.4752 / 0.4712 |
| corpus CONFLICTs, with / without | 12 / 68 | 1 / 22 | 1 / 75 |
| corpus cases the edges resolve, right | 56, 10 (0.1786) | 21, 8 (0.3810) | 74, 31 (0.4189) |
| **space** e2e, with / without edges | 0.3063 / 0.1750 | 0.2951 / 0.2232 | 0.5536 / 0.1967 |
| space silent error, with / without | 0.5882 / 0.6667 | 0.6777 / 0.7253 | 0.4359 / 0.6291 |
| space CONFLICTs, with / without | 34,440 / 63,840 | 11,340 / 25,200 | 2,520 / 63,120 |
| space points the edges resolve, right | 29,400, 17,640 (0.6000) | 13,860, 9,660 (0.6970) | 60,600, 47,960 (0.7914) |

**The same edges buy +0.0050, +0.0040 and +0.0155 of e2e on the arrivals, and
+0.1313, +0.0719 and +0.3568 over the function.**

- **On the arrivals they raise the silent error rate.** Over the function they
  lower it.
- **Without its edges, run 3's final base is a CONFLICT on 63,120 of the space's
  134,400 points**, 47%. With them it is a CONFLICT on 2,520.

### Recorded beside the rows and never in a denominator

- **The six deciding rules.**
  - **Run 1:** `R0021`, *security keyword → `SECURITY_INCIDENT`*, born on a
    coverage screen at case 44, decided all 37, right 5. It declared no edge.
    The 17 newborns that sided with it did.
  - **Run 2:** `R0012`, *security keyword, free tier → `SECURITY_INCIDENT`*,
    decided 15, right 5. `R0018`, *security keyword, severity 1*, decided 1,
    right.
  - **Run 3:** `R0013`, *security keyword → `SECURITY_INCIDENT`*, born on a
    coverage screen at case 19, decided 41, right 15. It wins 15 installed
    edges: 6 it declared at its birth, and 9 that later rules declared by
    naming it in `loses_to`. `R0014` and `R0027` are the two `T2_TECHNICAL`
    rules above.
- **The coin, pooled**: mean 18.884 right decisions, sd 7.0703, from 3 to 37,
  95th percentile 30. One draw of the 2,000 ties the proposer, and none beats it.
- **Per run**, the coin's right, wrong and unresolved means are 2.50, 15.79 and
  18.71; 3.01, 5.08 and 7.91; and 13.37, 17.57 and 30.06.
- **The inverted arm** decides 1 right, 1 wrong and leaves 112 unresolved.
- **Clusters.** `W-a`'s 114 cases fall in one cluster in run 1, two in run 2 and
  three in run 3. Run 1's own error is therefore undefined, and its 0.1351 is one
  rule's.

---

## What this settles, and what it does not

**It answers `STATUS.md`'s *What is open*, item 2: what the edges bought.**

- **Over the arrivals, little, and badly.** They decided 114 cases and were
  right on a third. They beat a coin only by deciding where a coin would leave
  a conflict, and were right no more often on what they decided.
- **Over the function, a great deal.** Their direction is right three times in
  four, and they lift the final bases' e2e by 0.07 to 0.36.
- **The same 50 edges do both.** Nearly all of them are one decision about one
  attribute, and the two surfaces weigh that attribute differently.

**What it does not settle.**

- **Whether this is a property of write-time declaration or of one attribute.**
  47 of 50 edges and 94 of 114 decisions are the security keyword. Three other
  edges, all in run 3, are not a population, and nothing here says what the
  proposer declares where no attribute is skewed between the two surfaces.
- **The trajectory.** What the loop would have done without its edges would take
  calls (§10.1 of the plan).
- **What escalating would have bought instead.** It needs the model's answers on
  the conflict screens these cases would have reached (§10.2).
- **Imposed declaration.** v1 lets the proposer declare or not. Stage E of
  [`PLAN_PAIRWISE.md`](../PLAN_PAIRWISE.md) remains the form never run (§10.3).
- **Accuracy among resolved cases, pre-registered.** That is the comparison
  `W-c` should have made. Its figure now exists, so it can only be reported:
  0.3272 for a coin, 0.3246 for the proposer.

---

## Files

```
results_edges/score.json         the census, W-a to W-c per run and pooled, W-d;
                                 every coin draw's right, wrong, unresolved and
                                 refused counts
results_edges/readings.json      POST-RUN: the coin read among resolved cases
                                 and net, the rules that decided D, D by queue,
                                 the installed edges by the keyword, the keyword
                                 on both surfaces, SECURITY_INCIDENT's ledger
edges/plan.py                    the gate and §8's constants; §0's three lines
edges/rebuild.py                 the counterfactual rebuild; W-g3's child
edges/gates.py                   W-g1 to W-g4
edges/score.py                   the stage
edges/readings.py                the post-run readings
```
