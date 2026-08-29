# Rung 2 — finding

Record. August 6, 2026. Corpus n=100, seeds 17/18/19/20, model
`deepseek/deepseek-v4-flash`, eight runs (four per prompt version).

> Quotations from the proposer's notes and from the prompt are reproduced
> **verbatim** from the records, which are in Spanish; an English rendering
> follows each one in italics.

---

## The central result

**The change introduced to MAKE declared priority POSSIBLE is the one that made
it impossible to measure.**

Rung 1 concluded that priority is not recoverable from the syntactic shape of
the rules, and that the necessary information was not in the proposer's context:
it saw a ticket and no other rule. Rung 2 gave it that information — the existing
rule base — and a schema field for declaring priority.

Giving it the base **reduced the overlap between its rules by a factor of 10**:
from 17.5% of the pairs without the base in view, to 1.6% with it. Without
overlap there is no conflict, and without conflict there is no priority to
declare. The mechanism never received material to exercise it:

```
eight runs · ~200 escalations
  total conflicts         2
  proposed edges         14
  ACCEPTED edges          0
  EDGE_CONTRADICTS        0
```

`EDGE_CONTRADICTS` — the counter designed in this rung to detect whether the
proposer declares priorities that contradict subsumption — has measured nothing,
in none of the eight runs. Not because the proposer got it right: because the
situation in which that counter can increment was never reached.

## Two different claims, which must not be confused

**First: the hybrid engine correctly executes a layered policy.** Step 0 loaded
the 29 rules of the hidden policy with their declared priority relations — 61
pairs ordered by subsumption plus 199 minimal declared edges, derived from the
layer order — and measured over the corpus of 2000 with seed 17:

```
arbitration                             e2e   sil.err  CONFLICT  IMPASSE
specificity (rung 1)                 0.5875    0.2140       505        0
subsumption alone (rung 1)           0.6315    0.0000       737        0
HYBRID (rung 2)                      1.0000    0.0000         0        0
```

2000 ACTION, 2000 correct, zero silent errors, zero conflicts. The arbitration
redesign **works**. Reproducible for free with
`python3 -m rung2.ceiling_check2`.

> **[NOTE 2026-08-29] That table is a CORPUS table, and the row now has its other
> surface.** Over the 134,400 combinations the hybrid engine also gives 1.0000,
> with zero conflicts and zero impasses, so the 1.0000 above is not *"it fits the
> 1,743 cases the corpus touches"* — the engine is **policy-equivalent** to the
> hidden policy. The other two rows do not travel like that: subsumption alone
> falls from 0.6315 to **0.2612**, so what the 199 edges buy is +0.3685 on the
> arrivals and **+0.7388** on the function. Section *The same ceiling on the other
> surface*, at the foot of this record, owns those figures and the reading;
> `ARBITRATION_REPORT.md` §9.2 is what asked for them.

**Second: no material arrives to exercise it.** This is what these eight runs
measure, and it is independent of the above. A correct mechanism that receives no
input is not refuted by that; it is left unmeasured.

Confusing the two claims would mean reading this record as "hybrid arbitration
does not work", which is the opposite of what Step 0 says.

## The result about the proposer's behaviour

**A proposer that is given the existing rule base, the exact overlap information,
and the explicit instruction to overlap, writes mostly disjoint rules and argues
it as a merit. It treats the base as a partition to be completed, not as a
hierarchy with exceptions.**

One qualification about that formulation, because the numbers do not support it
in its strong form: the explicit instruction **did have a measurable effect**.
Overlap rose from 1.60% on average (v1) to 7.25% (v2). What did not change is the
nature of the behaviour or its consequence. The exact form of the finding is:

> Showing it the base **reduces** overlap relative to not showing it. Without the
> base in view (rung 1) it wrote rules that overlapped on 17.5% of the pairs;
> with the base in front of it, 1.6%. Explicitly instructing it to overlap
> recovers part of the ground (7.25%) but does not even reach half of the
> starting point, and in eight runs it **never** produced material enough to
> exercise the declared-priority mechanism.

---

## What is verifiable

### 1. Overlap collapses when it is shown the base, at the same rule density

```
base                          rules  cond/rule  overlap%  ov.diff%  nest  CONF
RUNG 1  n=100 (no base)          16       2.94      17.5       8.3     1     1
RUNG 1  n=2000 (no base)        577       3.06      32.3      21.3  8599   594

RUNG 2  v1  seed 17              40       3.73       2.9       2.8     0     0
RUNG 2  v1  seed 18              14       2.86       2.2       0.0     2     0
RUNG 2  v1  seed 19              12       3.00       1.5       1.5     0     0
RUNG 2  v1  seed 20              26       2.92       0.0       0.0     0     0

RUNG 2  v2  seed 17               6       2.33      13.3       6.7     2     0
RUNG 2  v2  seed 18               9       2.89      11.1       5.6     2     1
RUNG 2  v2  seed 19              12       3.67       1.5       0.0     1     0
RUNG 2  v2  seed 20              26       3.54       3.1       0.3     9     1
```

`overlap%` and `ov.diff%` are percentages over the total pairs in the base;
`nest` is a count of nested pairs; `CONF` the conflicts the engine declared
during the run. The `CONF` columns for rung 1 come from its specificity engine
and are not comparable with those of rung 2, which come from the hybrid engine:
they are listed only to situate the order of magnitude.

Dispersion between runs of the same prompt:

```
        conditions/rule          overlap %             conflicts
v1      mean 3.13  sd 0.35    mean 1.60  sd 1.10        0 0 0 0
v2      mean 3.11  sd 0.54    mean 7.25  sd 5.04        0 1 0 1
```

**The condition density is identical across the three populations** (2.94 without
base; 3.13 with base v1; 3.11 with base v2). It does not narrow the rules. What
changes is where it places them: it picks attribute combinations that tile the
space instead of stacking on top of it.

The number of rules varies from 6 to 40 with an identical prompt, so that
quantity is noise and is not used for anything here.

### 2. The notes argue for disjointness, and do so more under v2

```
notes that explicitly argue for disjointness
  v1:  8/40 (20%)   5/14 (36%)   2/12 (17%)   4/26 (15%)     mean 22%
  v2:  5/6  (83%)   4/9  (44%)   7/12 (58%)   9/26 (35%)     mean 55%
```

The count is by literal markers and is crude. The quotations are the evidence.
**All of the following are v2 notes**, written under a prompt that says *"El
solape entre reglas es NORMAL y es lo que se espera"* [*Overlap between rules is
NORMAL and is what is expected*] and *"No estreches una regla ni le añadas
condiciones para esquivar a otra: eso no resuelve el conflicto, lo esconde"*
[*Do not narrow a rule or add conditions to it to dodge another one: that does
not resolve the conflict, it hides it*]:

```
[v2 s17 R0003]  free AND severity eq 4 -> T1_GENERAL          (0 correct of 21)
  "Al restringir el tier y la severidad, la regla es DISJUNTA con las existentes
   (R0001/R0002 se centran en enterprise/dashboard y severidad...)"
  -> "By restricting the tier and the severity, the rule is DISJOINT from the
      existing ones (R0001/R0002 focus on enterprise/dashboard and severity...)"

[v2 s18 R0002]  billing AND severity lte 3 AND pro -> T2_TECHNICAL   (0 of 5)
  "...cubriendo casos similares SIN SOLAPAMIENTO con reglas existentes"
  -> "...covering similar cases WITHOUT OVERLAP with existing rules"

[v2 s18 R0005]  billing AND severity eq 4 -> BILLING_SPECIALIST      (2 of 7)
  "NO SE SOLAPA con reglas existentes porque todas requieren severity <=3 o tier free."
  -> "It DOES NOT OVERLAP with existing rules because they all require
      severity <=3 or tier free."

[v2 s18 R0006]  pro|business|enterprise AND sev eq 4 AND product neq billing
  "Esta regla llena ese vacío y ES DISJUNTA DE TODAS las reglas existentes por
   severidad o producto."
  -> "This rule fills that gap and IS DISJOINT FROM ALL existing rules by
      severity or product."

[v2 s19 R0002]  free AND product neq billing AND no-security -> T1_GENERAL  (0 of 33)
  "La regla es DISJUNTA con R0001 (product=billing) y NO SE SOLAPA con ninguna otra"
  -> "The rule is DISJOINT from R0001 (product=billing) and DOES NOT OVERLAP
      with any other"

[v2 s19 R0005]  pro|business AND sev in [2,3] AND integrations
  "...llenando el VACÍO dejado por las reglas existentes... NO HAY SOLAPAMIENTO
   porque product es disjunto de los ya cubiertos."
  -> "...filling the GAP left by the existing rules... THERE IS NO OVERLAP
      because product is disjoint from those already covered."

[v2 s20 R0005]  pro|business AND billing AND off_hours AND sev in [2,3]
  "NO SE SOLAPA con reglas existentes (todas requieren free)."
  -> "It DOES NOT OVERLAP with existing rules (they all require free)."
```

The pattern is always the same: it identifies a gap in the partition, fills it,
and presents the absence of overlap as justification for the rule. For it the
base is not a stack of layers where the new rule has to place itself; it is an
incomplete mosaic.

### 3. The priority mechanism never received material

```
eight runs · ~200 escalations
  proposed edges              14
  ACCEPTED edges               0
  EDGE_CONTRADICTS             0
  total conflicts              2
```

The 14 proposed edges all fell to `no_solapan` [*they do not overlap*]: they cite
rules whose extension does not intersect that of the new rule.
`EDGE_CONTRADICTS` — the instrument designed to detect whether the proposer
contradicts subsumption — **has measured nothing in any of the eight runs**,
because the situation where subsumption has something to say was never reached.

The only two occasions on which the engine did produce a conflict:

```
v2 seed 18, case 35: CONFLICT between R0001 and R0005
  the proposer answered with action T1_GENERAL and ZERO edges
  (truth: SELF_SERVICE_DEFLECT)

v2 seed 20, case 65: CONFLICT between R0013 and R0017
  the proposal failed to parse; there was neither rule nor edges
```

Two opportunities in eight runs. One squandered, one lost to malformed JSON.

### 4. The attributes it never uses

```
attribute              runs (of 8) it appears in
severity                8/8
customer_tier           8/8
product                 8/8
has_security_keyword    5/8
off_hours               2/8
prior_tickets_30d       1/8
channel                 1/8
language                0/8
```

`language` appears in none of the eight bases. `channel` and `prior_tickets_30d`
in one each. The hidden policy has entire layers built on those attributes:
H11/H13/H14/H25/H26 depend on `prior_tickets_30d` and decide 14.5% of the corpus;
H22/H23 depend on `channel`; H21 on `language`.

The extreme case is v2 with seed 17: six rules that use only `customer_tier`,
`severity` and `product` (twice). A two-dimensional partition over an eight-layer
policy, with coverage 0.940 and silent error 0.7553.

---

## Why this is NOT a capability failure of the model

There are two reasons, and the second is an experiment.

**First: it reasons relationally as soon as it is given something to reason
with.** In rung 1 the notes described the presented ticket. In rung 2, with the
base in front of it, they cite rules by identifier and argue about them:

```
[v1 s17 R0017]  "...se requiere atención técnica (T2) en lugar de general (T1)
                 porque la severidad es más crítica que la del caso R0014 (severity=3)"
  -> "...technical attention (T2) is required rather than general (T1) because
      the severity is more critical than that of case R0014 (severity=3)"

[v1 s17 R0014]  "...Debe perder contra R0012 que cubre off_hours=true con prioridad."
  -> "...It must lose against R0012, which covers off_hours=true with priority."

[v2 s17 R0029]  "...Esta regla es un caso particular de las reglas de T2_TECHNICAL,
                 pero al ser más específica y de mayor prioridad, el nivel 1 la resuelve"
  -> "...This rule is a particular case of the T2_TECHNICAL rules, but being more
      specific and of higher priority, level 1 resolves it"
```

That last one is correct: it understands that subsumption resolves the nesting
without a declaration. The faculty of reasoning about priority between rules is
present.

**Second: its other error was removed and the behaviour did not change.** Under
v1 it systematically miscalculated extensions — it claimed overlap between
`billing` and `integrations`, which are disjoint; it wrote that `off_hours` is
mutually exclusive and declared the edge anyway. One could argue that the problem
was arithmetic, not conceptual.

v2 hands it that arithmetic resolved by the engine: for each rule shown, which
conditions the ticket fails, the size of its extension, which pairs are disjoint,
and the inference rule stated explicitly. All computed over the 134,400
combinations and none of it derivable by the model.

Result: **five of the fourteen badly proposed edges are v2's**, three of them in
escalations where the neighbourhood explicitly marked which conditions the ticket
failed for each cited rule. With the correct information in front of it, it makes
the same mistake.

It is not that it cannot compute the overlap. It is that the operation it
performs — find a gap and fill it — does not require computing it, and that is
the operation it performs even when asked for another one.

---

## Caveats

**One model.** Everything is `deepseek/deepseek-v4-flash`. Whether another model,
or a more capable one, partitions the same way is unknown.

**n=100 runs.** Bases of 6 to 40 rules. The number of rules varies so much across
seeds with an identical prompt that the quantity is noise; the conclusions rest
on the overlap, the attributes and the notes, which are stable. Nothing here says
what would happen at n=2000.

**Non-determinism at temperature 0.** Verified in rung 1: same prompt, same case,
same seed, different rules. That is why each configuration was run with four
different corpora instead of one, and why the number of rules is not used as
evidence.

**The engine is not the problem.** See above, "Two different claims": Step 0
gives e2e 1.0000 with the perfect policy loaded. Nothing that follows in this
record casts doubt on that.

**The cost of authorship is not measured on a learned base.** The 199 edges of
Step 0 are what a perfect author declares for 29 rules. How many would be needed
for a learned base, and whether a proposer could produce them, is precisely what
these eight runs never got to put to the test.

> **[ERRATUM 2026-08-24] Both halves are measured now, and the first answers the
> second.** Stage D below asked a proposer for 400 of those edges and got 344
> into the graph. The population needing one is **31,850** pairs, so 400 calls
> buy **1.3%** of it — and with those 344 installed the engine abstains on **89%**
> of corpus test (`results3/FINDINGS3.md` §8). The authorship cost of a 577-rule
> learned base is not of the order of the 199 edges a perfect author declares for
> 29 rules.
>
> Whether a proposer *could* produce them is answered separately, and badly: the
> order those 344 edges induce scores **below** the arrival order they started
> from, and inverting every one of them scores above it. The caveat is
> discharged; what replaces it is not more encouraging.

---

## The labelled pair benchmark

*Added 2026-08-24. `rung2/pair_benchmark.py` → `results2/pair_benchmark.json`, run
with `PYTHONHASHSEED=0`. Stage B of `PLAN_PAIRWISE.md`. Zero API calls, no model,
no decision, nothing in `rung2/` modified.*

**Why it exists.** The finding above is that the mechanism works and the material
never arrives. `PLAN_PAIRWISE.md` changes the question put to the proposer — from
*write a rule* to *here are two rules that both match this ticket, which queue
does it go to?* — and the first thing to do with a new question is ask it where
the answer is already known. This section builds that population. **It measures
nothing**: it produces pairs, witnesses and a key.

**The four boxes, which are a property of the frozen policy.** `hidden_priority.py`
sorts the 406 pairs of the 29 hidden rules into 112 disjoint extensions, 61
already ordered by subsumption, 34 with the same action and **199 declared edges
with a known winner**, rejecting none. They partition: 112 + 61 + 34 + 199 = 406.
This run gates on all four and on the zero.

**170 of the 199 carry a clean witness; 29 do not.** A witness is a case from
`ext(winner) ∩ ext(loser)` — the region where the two rules compete — restricted
to the cases whose **true** action is the winner's, taking the lowest such index.
Deterministic: no sampling and no seed. The restriction is not cosmetic, and the
29 are what it costs.

```
199  declared edges, winner known
170  with a clean witness      <- the benchmark, and its denominator
 29  with none                 <- recorded, counted apart, outside it

overlap over the 199, cases of the exhaustive space   min 80   median 2,560   max 33,600
clean cases over the 170                              min 20   median   840   max 16,800
overlap over the 29 without a witness                 min 200  median 4,200   max 33,600
```

**What the 29 lose it to, measured rather than assumed.** In every one of them an
**earlier layer owns the whole overlap**, so the correct queue for every ticket
there is neither rule's: 29 of 29, no exception. `PLAN_PAIRWISE.md` §7 described
this as *a third rule from an even earlier layer* — the direction is exactly
right and the number is not. Only **7 of the 29** lose the region to a single
rule; the other 22 lose it to between 2 and 13 of them, and the region's true
action is `SECURITY_INCIDENT` in 28 of the 29 and `ONCALL_ESCALATION` in 14 (a
pair can have several). `H01` appears among the owners of 25 of the 29 and `H02`
of 11. The record names the owning rules and their case counts per pair, so this
is a lookup and not a second measurement.

The clearest instance: `H03 > H04` overlaps on 4,200 cases and **all 4,200** are
won by `H01`, whose action is `SECURITY_INCIDENT` — neither `T2_TECHNICAL` nor
`ONCALL_ESCALATION`. There is no ticket in that region whose correct answer is on
the menu of the two rules shown.

**Read the 29 as a bias and not only as a loss, because that is what the
denominator means.** They are precisely the pairs where the layer order is
invisible on the surface of the two rules shown — the ones where a reader with
only those two rules in front of them could not be right. **The 170 that survive
are therefore the easier half by construction, and any rate measured on them is
an UPPER estimate of what a proposer would do on all 199.** They are also the
larger overlaps: median 4,200 cases against 2,560 over the whole 199, which is
the same fact from the other side — the wider the region two rules share, the
more of it an earlier layer has already claimed.

**The population of the 170.** By the winner's action: `SECURITY_INCIDENT` 43,
`T2_TECHNICAL` 39, `ONCALL_ESCALATION` 24, `T3_ENGINEERING` 24,
`ACCOUNT_MANAGER` 22, `BILLING_SPECIALIST` 13, `SELF_SERVICE_DEFLECT` 4,
`T1_GENERAL` 1. Winner and loser never share an action — the 34 same-action pairs
were filtered upstream — so a pair has exactly one right answer and one wrong one
among the two rules shown.

**Three gates, all blocking**: the four boxes against `hidden_priority`'s
published partition; 170 and 29 against what `PLAN_PAIRWISE.md` §7 measured and
budgeted the next stage on; and byte-identical witnesses from two independent
builds. `tests/test_pair_benchmark.py` repeats the third across three
`PYTHONHASHSEED` values in separate processes, with the child printing its own
randomization witness so the check cannot pass by proving that hashing stopped
being randomized.

**The bit convention is where this could have gone wrong silently.**
`engine2.Space` is MSB-first — case index `i` is bit `n-1-i`, so the
lowest-indexed case in a mask is its **highest** set bit. An LSB-first reading
returns a valid case index that is not the case the two rules compete over, and
every figure built on top of it would look plausible. Two assertions run on every
emitted witness and stop the run: both rules match it, and its true action is the
winner's. The test suite additionally rebuilds all 199 witnesses with the plan's
own list comprehension over `true_action` and checks that the mask formulation
agrees on every one.

**Why this module may see the oracle.** It imports `true_action` and
`true_rule_id`, and was added to the allowlist in
`tests/test_oracle_separation.py` deliberately, in the commit that created it. It
measures offline against a known key, decides nothing, and no component of the
online loop imports it — and the key is written into the record openly, which is
what makes this a benchmark rather than a leak.

**What it does not do.** It does not put the question to a model; that is stage C
of `PLAN_PAIRWISE.md` and it is gated on a signature that does not exist yet. It
says nothing about the learned base: these are the 29 hand-written rules, whose
layer order is known. And it does not measure the cost of authorship on a learned
base — the last caveat above still stands untouched.

**Files added by this section**

```
rung2/pair_benchmark.py         the 199 declared pairs with their witnesses
results2/pair_benchmark.json    the record: per pair, the witness ticket, the
                                overlap, and for the 29 the rules that own it
tests/test_pair_benchmark.py    the three gates, the bit convention, the two
                                assertions provoked, determinism across seeds
```

Reproducible with `PYTHONHASHSEED=0 python3 -m rung2.pair_benchmark`
(`--checks` runs the gates alone, `--digest` prints the determinism
fingerprint). Three seconds, zero API calls.

---

## Stage C — the pairwise question, and what its rate is made of

*Run 2026-08-24 with `PYTHONHASHSEED=0`. `rung2/pair_judgement.py --hidden` →
`results2/pair_judgement_hidden.json`, 170 calls at
`deepseek/deepseek-v4-flash`, temperature 0, sequential, 18 minutes, cents.
`rung2/pair_judgement_baselines.py` → `results2/pair_judgement_baselines.json`,
zero API calls. Stage C of `PLAN_PAIRWISE.md`, run after Sergi signed §0 in
`a69f9ca`.*

**The question.** Instead of *write a rule*, the model was shown a ticket, two
rules that both match it, and asked which queue the ticket goes to. The correct
answer is known by construction: the winner's action, from the hidden policy's
layer order. Population: the 170 clean-witness pairs of the benchmark above.

### The result

```
correct 150   wrong 16   neither 4   (all 4 parse failures, 0 off-menu)

over all 170 pairs, `neither` a failure      0.8824   <- adjudicates P-c
over the 166 two-way answers                 0.9036
                                     floors: 0.3877  proposal_action_accuracy
                                             0.5000  a coin between the two
```

**P-c holds.** It was signed at band `> 0.60`, refuted at `≤ 0.60`, adjudicated
on `correct / 170` — the denominator §0 named on 2026-08-24, before the run. The
rate clears the band and both floors.

Two protocol facts, both clean. **Position bias is zero**: the winner was shown
first in 85 pairs and second in 85, and the rate is **0.8824 in both** — 75
correct out of 85 either way. And the format holds: 4 parse failures in 170, no
answer outside the eight queues, one retry recovered.

### And the baseline that reads no rule beats it

A **fixed total order over the eight queues** — answer with the higher-ranked of
the two on offer, reading no rule, no ticket, no condition — scores **161/170 =
0.9471**. That is more than the model got while being shown both rules.

```
best fixed queue hierarchy, over all 40,320 orders     0.9471   161/170
the same 40,320 orders: mean 0.5000, median 0.5000, sd 0.1346, worst 0.0529
the model, shown both rules and the ticket             0.8824   150/170
```

**That order is a world record and must be read as one.** It is chosen by brute
force *with the answer key in hand*; nothing without labels could pick it. It is
the same kind of object as the best of 65 starts in §2 of the plan — a winning
ticket, not a level — which is why the whole distribution is published beside it,
and why the mean is exactly 0.5 by symmetry rather than by measurement.

What it legitimately bounds is the thing worth knowing: **at most 9 of the 170
pairs require reading the rules at all.**

### The decomposition, which is the actual finding

```
                                 n     model correct    rate
where the hierarchy is right    161      145           0.9006
where the hierarchy is wrong      9        5           0.5556   (a coin is 0.50)
```

The nine are the pairs a queue ordering is *structurally* unable to answer: five
queue-pairs appear in the benchmark with **both** winners — `T2_TECHNICAL` vs
`BILLING_SPECIALIST`, `T3_ENGINEERING` vs `ACCOUNT_MANAGER` and three more,
covering 29 rule-pairs between them — so no ranking of queues can serve both
directions. Those nine are the only pairs here where priority is a fact about the
two *rules* rather than about the two *queues*, and they are the only ones where
a correct answer is evidence about pairwise judgement.

**On them the model is at 5 of 9.** That is a coin, on n=9.

**The model is not itself a hierarchy**, and this is worth separating: on 9 of
the 27 queue-pairs it was asked about it did not always answer the same queue. It
is reading something. What the decomposition says is that what it reads does not
help where the hierarchy runs out.

### The rest of the record

**By breadth of the correct winner**, the split §9 asked for because it tests
`narrow ≠ correct` directly:

```
the correct winner is the broader rule    n=101   0.8614   wrong-edge 0.1212
the correct winner is the narrower rule   n= 69   0.9130   wrong-edge 0.0597
```

Twice the wrong-edge rate when the broader rule is the one that should win. The
pull toward the narrower rule is real and it is the same pull that gives
subsumption 53.12% silent error over the learned base — measured here on a
policy where the right answer is known, and on a model rather than on a
criterion.

**By the winner's queue**: `ONCALL_ESCALATION` 24/24 and `SECURITY_INCIDENT`
41/43 at the top, `ACCOUNT_MANAGER` 17/22 and `T3_ENGINEERING` 20/24 at the
bottom. The single `T1_GENERAL` pair was answered wrongly.

**The `try_edge` histogram, outside every denominator** and recorded because it
is free: 158 `ok`, 8 `cierra_ciclo`. Of the six verdicts only those two can fire
here — a witness guarantees overlap, so `EDGE_DISJOINT`, the verdict that
rejected all 14 edges rung 2 ever got, is unreachable by construction. **The
acceptance rate is 166/166 minus the cycles and it measures the protocol, not the
proposer.** It is not a result and it is not in any denominator.

### What this does and does not establish

**It does establish that the change of question works as a format.** Rung 2 got
2 conflicts and 0 accepted edges out of eight runs; this got 166 well-formed
answers out of 170 with no position bias and no off-menu queue. The mechanism
that had no material now has material.

**It does not establish that the model supplies priority.** 0.8824 is mostly a
queue hierarchy, and where the hierarchy cannot reach the model is at chance.
Both sentences are true at once and the second is the one that transfers.

**And the 0.8824 is an upper estimate for the full edge set.** The 29 pairs with
no clean witness are outside the denominator by construction, and they are
precisely the ones where the layer order is invisible on the surface of the two
rules shown. If every one of them were wrong the rate over all 199 declared edges
would be **150/199 = 0.7538**; the true figure is somewhere between that and
0.8824, and this protocol cannot narrow it.

### What Stage D must now control for, before spending anything

`PLAN_PAIRWISE.md` §10 samples 300–500 pairs of the learned base and scores the
declared edges as an order. **There is no truth for those pairs**, so the
decomposition above cannot be repeated there — which makes it more important, not
less, that the control is built in *before* the calls.

The cheap control this run points at: **compare the declared order against the
order a fixed queue hierarchy would induce over the same 577 rules**, which costs
zero calls. If the two agree, the 300–500 calls bought an ordering that a lookup
table would have produced. §10 as signed does not ask for that comparison, and
the figures above say it is the first thing it should ask for.

That is a change to a signed plan and it is not the agent's to make.

**Files added by this section**

```
rung2/pair_judgement.py                  the pairwise question, with the gates
                                         that refuse to spend while P-c is
                                         unsigned and while a question could leak
rung2/pair_judgement_baselines.py        the queue-hierarchy baseline and the
                                         decomposition; reads, never rewrites
results2/pair_judgement_hidden.json      the run: 170 answers, per-pair
results2/pair_judgement_hidden_smoke.json  the 10-pair smoke path
results2/pair_judgement_baselines.json   the baseline record
tests/test_pair_judgement.py             the three leaks, the four gates
tests/test_pair_judgement_baselines.py   the arithmetic, and the permutation
                                         identity that says the maximum is one
```

The smoke path is kept and labelled `partial_run`. Its 10/10 says nothing: the
benchmark is ordered by the winner's layer, so its first ten pairs all have `H01`
as winner — a security keyword against anything else, the easiest slice there is.
It was run to check the shape of the output, and that is all it checked.

---

## Stage D — the same question over the learned base, where there is no truth

*Run 2026-08-24 with `PYTHONHASHSEED=0`. `rung2/pair_judgement.py --learned` →
`results2/pair_judgement_learned.json`, 400 calls at
`deepseek/deepseek-v4-flash`, temperature 0, sequential, 51 minutes, cents. What
the edges DO is scored in `results3/FINDINGS3.md` §8; this section is the run.*

**The population, and the filter that is not optional.** The three conditions
`hidden_priority.py` uses, applied to the 577 rules of rung 1:

```
166,176  pairs of the 577 rules
112,556  disjoint extensions              (can never compete)
  8,599  subsumption-comparable           (structure already decides)
 13,171  same action                      (it does not matter who wins)
 31,850  the population — 19.2%
```

A constant fraction of the quadratic, not a lower order. The 8,599 are the box
worth naming: on those a declared edge cannot enter the graph whichever way the
model answers — `try_edge` returns `EDGE_CONTRADICTS` for the broader rule and a
redundant `EDGE_OK` that mutates nothing for the narrower — so dropping that
filter would have spent about one call in ten on an answer inert by construction,
and one of those wasted calls would have scored as an acceptance.

**400 pairs sampled deterministically at seed 17: 1.3% of the population.**

### What came back

```
365  named one of the two queues          162 a-beats-b · 203 b-beats-a
 35  named nothing                        all 35 parse failures, 0 off-menu
344  edges entered the graph
 21  refused, cierra_ciclo
```

**Which rejection verdicts have now been seen working, stated precisely.** Rung
2's fourteen rejected edges were all `no_solapan`, and this protocol makes that
one unreachable by drawing every witness from the intersection. What it exercises
instead is `cierra_ciclo`: **8 refusals in Stage C and 21 here**. Two of the six
verdicts have now been observed doing work in a real run.

**`EDGE_CONTRADICTS` still has not, and this protocol cannot make it.** The
caveat `PLAN_PAIRWISE.md` §5.3 records — *any conclusion resting on it rests on a
counter nobody has seen work* — stands untouched: the population filters
subsumption-comparable pairs out precisely so that no call is wasted on one, which
is the same thing as guaranteeing that verdict never fires. Retiring the caveat
would take a protocol that deliberately offers such a pair, and this is not one.

**Two numbers that are not conclusions and are recorded anyway.** The parse
failure rate is **8.75%** here against 2.4% in Stage C, on the same model, the
same settings and the same prompt; the population is the only thing that changed.
And the direction split is 203/162 towards the rule shown **second**, while the
presentation order is balanced exactly 200/200 — so it is not a position
artefact, and what it is instead is not measured here.

### The control this stage was authorised with

Stage C found the proposer's competence is largely a fixed ranking of the eight
queues. The same question asked of these answers, needing no labels: for each
unordered pair of queues, how often each side was named.

**Constant on 14 of the 24 queue-pairs it was asked about — 58.3%.** Stage C's
proposer was constant on 18 of 27, 66.7%. So it varies somewhat more here: it is
reading something beyond the ranking. Whether what it reads helps is the question
`results3/FINDINGS3.md` §8 answers, and the answer is no.

### What this section does not say

**No correct-edge rate exists here and none is computed.** The hidden policy's
layer order says nothing about rules it never wrote. Acceptance is not a result
either: every witness comes from `ext(A) ∩ ext(B)`, so `EDGE_DISJOINT` — the
verdict that rejected all 14 edges rung 2 ever got — is unreachable by
construction, and the 344/365 acceptance measures the protocol.

**Files added by this section**

```
rung2/pair_judgement.py --learned          the population, the sample, the calls
results2/pair_judgement_learned.json       the record: 400 answers, per pair
results2/pair_judgement_learned_smoke.json the 10-pair smoke path
```

Reproducible with
`PYTHONHASHSEED=0 python3 -m rung2.pair_judgement --learned --budget 400`;
`--dry-run` builds every question and spends nothing. The destination is guarded
by `harness/record_guard.py`: the record cost money and a re-run does not give
the same thing back.

---

## The same ceiling on the other surface

Added August 29, 2026. Zero API calls, four seconds. It closes limit 2 of
[`ARBITRATION_REPORT.md`](../ARBITRATION_REPORT.md) §9 — *"the hybrid engine's
1.0000 is a corpus figure … it is the cheapest pending check of all the ones
named here"* — and it is item 3 of [`EXTERNAL_REVIEW.md`](../EXTERNAL_REVIEW.md)'s
plan. Reproducible with `python3 -m rung2.ceiling_check2_space`;
`results2/ceiling2_space.json` is the raw record.

> **PROVENANCE: POST-RUN.** Written after the figures were seen; no band was
> drafted, none is claimed, no signed row moves. **Unlike the default-rule
> control, this one's figures did not exist beforehand**, so it could have been
> pre-registered, and §4 of `EXTERNAL_REVIEW.md` — which says items 4 and 5 are
> *"the only two whose figures do not yet exist"* — is wrong about this item. The
> mitigation is partial and stating it exactly is the point: **the ceiling was
> derivable in advance** from two facts already in the records (see *Why the
> 1.0000 is not luck*), so a band on it would have been a bet on arithmetic; **the
> other three figures were not derivable** and could have carried one.

### The four rows

Perfect policy loaded, 29 rules, no LLM.

| surface | arbitration | coverage | e2e | CONFLICT | silent |
|---|---|---|---|---|---|
| corpus (n=2000, seed 17) | hybrid: subsumption + 199 edges | 1.0000 | **1.0000** | 0 | 0 |
| exhaustive space (134,400) | hybrid: subsumption + 199 edges | 1.0000 | **1.0000** | 0 | 0 |
| corpus (n=2000, seed 17) | subsumption alone (level 1) | 0.6315 | 0.6315 | 737 | 0 |
| exhaustive space (134,400) | subsumption alone (level 1) | **0.2612** | **0.2612** | 99,298 | 0 |

The first and third rows are the published ones and they are **gates** here, not
results: the module re-measures them and refuses to print anything if either has
moved. Row 3 belongs to [`../results/FINDINGS.md`](../results/FINDINGS.md),
route 3.

**What 1.0000 means is not the same on the two surfaces**, which is the whole
reason for measuring twice. On the corpus it means *fits the sample*: 2,000 draws
touch 1,743 distinct cases and leave the rest of the function unconstrained — an
order can be perfect on the corpus and be 0.9455 as a function
([`../results3/FINDINGS_AUDIT.md`](../results3/FINDINGS_AUDIT.md), Step 0). On the
space it means **policy-equivalent**: on every case that exists, the engine
decides what first-match-wins decides. That is the claim rung 2 was always read as
making, and until now it was not the claim that had been measured.

### Why the 1.0000 is not luck

It follows from three facts, each already published elsewhere, and the module
measures all three and blocks on them rather than assuming any:

1. **Subsumption never contradicts the layer order** — 0 of the 406 pairs
   (`../results/FINDINGS.md`, route 3).
2. **The validator rejected no declared edge** — 0 of 199.
3. **No pair that needs an edge lacks one**: overlapping, incomparable by
   subsumption, and disagreeing on the action.

Given those, take the earliest-born rule `A` matching a case — its action is the
truth. Any other matching rule `B` is either subsumed by `A` (defeated), or
incomparable with a different action (defeated by the declared edge premise 3
guarantees), or carries `A`'s action (harmless). `A` itself is never defeated,
because that would need premise 1 to fail or an edge pointing backwards, and none
is declared. So the undefeated set is action-unanimous on `A`'s action, on
**every** case.

**The consequence is worth more than the figure.** The ceiling does not depend on
the surface at all; it depends on those three premises. A learned base has no
**author** to satisfy premise 1 — `../results/FINDINGS.md`'s own formulation is
that subsumption is a proxy for *authored* priority, and the 0.0000 measures a
virtue of the author — and rung 1 measured the consequence: that same criterion
gives 53.12% silent error over the 577 learned rules. The 1.0000 is a property of
a well-authored policy plus a complete set of edges, not of the engine alone.

### What the corpus could not have said

**Level 1 alone falls by more than half.** Subsumption covers 63.15% of the
arrivals and 26.12% of the function. The structure an author puts into the shape
of the rules carries most of what a deployed system sees and a quarter of what the
policy is. Its silent error is **0.0000 on both surfaces**, which upgrades rung 1's
soundness result from a corpus figure to a statement about the whole function:
level 1 abstains rather than inventing, everywhere, not just on the sampled cases.

**So the edges buy +0.3685 on the corpus and +0.7388 on the space.** The same 199
edges, twice the work. Read as authorship cost: the fraction of the policy that
has to be *declared* rather than *derived* is twice as large as the arrival
distribution suggests.

**And a quarter of that authorship never shows up in the arrivals at all.**

| | corpus | space |
|---|---|---|
| edges that ever fire (both endpoints match one case) | 148 of 199 | **199 of 199** |
| edges that are ever the sole defeater of their loser | 60 | 72 |
| cases whose decision needs a declared edge | 737 (0.3685) | 99,298 (0.7388) |

**51 of the 199 edges are never exercised by the corpus** — their two rules never
match the same arriving ticket, so no run over the corpus can tell whether they
are right, wrong or missing. And the asymmetry is one-directional: 12 edges are
the sole defeater somewhere on the space and never on the corpus, **0 the other
way**. The corpus's load-bearing set is a strict subset of the space's, so an
authorship cost read off the arrivals is a **floor**, not the price.

**On removability, precisely.** An edge that is never the sole defeater on a
surface can be deleted, one at a time, without changing a single decision on that
surface. That does not license deleting a set of them at once — two edges can be
individually redundant and jointly necessary — and joint removability is not
measured here.

### What this section does not say

It says nothing about the **learned** base: every figure above has the perfect
policy loaded, and the 199 edges are derived from a layer order the proposer never
saw. Rung 2's actual finding — that the mechanism never received material, 2
conflicts and 0 accepted edges in eight runs — is untouched by any of this. Nor
does it make the space the right surface for a deployment claim: the two answer
different questions, and this record now names which one each figure answers.

---

## Files

```
rung2/engine2.py            hybrid engine: subsumption + declared priority
rung2/hidden_priority.py    the 29 rules with their derived minimal edges
rung2/ceiling_check2.py     STEP 0 — engine ceiling
rung2/ceiling_check2_space.py  the same ceiling over the 134,400 combinations
rung2/proposers2.py         prompts v1 and v2, neighbourhood v1 and v2
rung2/shadow2.py            shadow loop
rung2/run2.py               run CLI
rung2/compare_runs.py       comparison across runs
rung2/note_audit.py         attributes used and notes arguing disjointness

results2/ceiling2.json         Step 0 ceiling
results2/ceiling2_space.json   Step 0 on the exhaustive space, and per edge
results2/llm_run2_n100*.json   the eight runs, each with its full prompt
results2/comparison.json       comparison table
results2/note_audit.json       audit of notes and attributes
results2/CHANGELOG.md          record of the v1 -> v2 change
results2/RECORD_NOTES.md       why the mtime of results/subsumption.json changed
```

The full texts of both prompts are inside each `llm_run2_*.json`, in the
`system_prompt` field, next to the figures they produced.
