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

---

## Files

```
rung2/engine2.py            hybrid engine: subsumption + declared priority
rung2/hidden_priority.py    the 29 rules with their derived minimal edges
rung2/ceiling_check2.py     STEP 0 — engine ceiling
rung2/proposers2.py         prompts v1 and v2, neighbourhood v1 and v2
rung2/shadow2.py            shadow loop
rung2/run2.py               run CLI
rung2/compare_runs.py       comparison across runs
rung2/note_audit.py         attributes used and notes arguing disjointness

results2/ceiling2.json         Step 0 ceiling
results2/llm_run2_n100*.json   the eight runs, each with its full prompt
results2/comparison.json       comparison table
results2/note_audit.json       audit of notes and attributes
results2/CHANGELOG.md          record of the v1 -> v2 change
results2/RECORD_NOTES.md       why the mtime of results/subsumption.json changed
```

The full texts of both prompts are inside each `llm_run2_*.json`, in the
`system_prompt` field, next to the figures they produced.
