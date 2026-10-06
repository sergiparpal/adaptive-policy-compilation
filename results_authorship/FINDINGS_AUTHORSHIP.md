# Stage E, the discipline of authorship imposed at write time — findings

Record opened on October 6, 2026, under [`PLAN_AUTHORSHIP.md`](../PLAN_AUTHORSHIP.md).
Sergi signed §0 on 2026-10-05, before any figure below existed, in a commit of
its own: *PLAN_AUTHORSHIP.md signed by Sergi*. Stage B's four records,
[`run_n20_smoke.json`](run_n20_smoke.json) and
[`run_n2000_r1.json`](run_n2000_r1.json) to [`run_n2000_r3.json`](run_n2000_r3.json),
name in their `_env` the commits they ran from, by their hashes on the branch
they were made on. A rebase merge gives those commits new hashes on `main` with
the same trees, so they are named here by their subjects. Stage C's record is
[`score.json`](score.json). **This record owns every figure in it.**

**The stage adjudicated three of its four signed rows on 2026-10-06: two are
refuted and one holds. The fourth, `E-c`, is unadjudicable.**

- **The discipline did not nest the base** (`E-a` is refuted). Nested pairs fell
  below the baseline's.
- **Subsumption over the bases is wrong more often, not less**, at the same
  coverage (`E-b` is refuted).
- **One run left nothing to order** (`E-c` is unadjudicable). In the two that
  did, the installed edges filled all of the order's room over the space and
  58% of it, both above the line. The scorer, merged before the signature, reads
  a median over a run without a share as undefined, so the row is not read on
  the two that remain. **Under any other reading of the median it would
  hold**, as the section on the verdicts says.
- **The proposer contradicted subsumption 8 times** (`E-d` holds). It is the
  first time the verdict `contradice_subsuncion` has fired in any run of the
  project. **[NOTE 2026-10-06, later]** Seven of the eight were between rules
  carrying one queue, where no decision changes. On the eighth, level 1 was
  right over the whole region. POST-RUN, in *The eight refused declarations*,
  below.
- **The proposer met the discipline by not overlapping** (`E-e`, reported). In
  the three runs, 70% to 97% of the rules it wrote overlap no rule before them,
  against 27% to 39% in the baseline, and not one CONFLICT arose in 6,000
  arrivals. The order answer was never used.

> **PROVENANCE: PRE-REGISTERED.** `E-a` to `E-d` were signed before any of their
> figures existed. **`E-e` is reported, not adjudicated.** Its baseline column
> was added to `authorship/score.py` after the stage's first scoring, which
> wrote `E-e` for the runs only, though §0 asks for it beside the baseline. The
> second scoring, from the commit that added it, reproduced every verdict and
> every figure of the first. **The reading that leaves `E-c` unadjudicable is
> the scorer's, not §0's**: §0 does not say what one run without a share does to
> the median, and `authorship/score.py` does, merged before the signature.
> Everything labelled **POST-RUN** below was read after the verdicts existed.
> Stage B spent 243 calls, cents; Stage C spent none.

---

## What was run

**Stage B**, `authorship/run.py`, under v1e, each from a clean tree after the key
check and `E-g1` to `E-g4`, all passing.

| record | from the commit | calls | rules born | refused | repair rounds |
|---|---|---|---|---|---|
| smoke, 20 cases | *PLAN_AUTHORSHIP.md signed by Sergi* | 18 | 17 | 0 | 1 |
| run 1, 2,000 cases | *…'s smoke run: 18 calls parsed, 17 rules born, a repair round exercised* | 50 | 41 | 1 | 8 |
| run 2, 2,000 cases | *…'s run 1: 42 escalations, 41 rules born, 8 repair rounds* | 144 | 120 | 1 | 23 |
| run 3, 2,000 cases | *…'s run 2: 121 escalations, 120 rules born, 23 repair rounds* | 31 | 30 | 1 | 0 |

**Every one of the 243 answers ended with `finish_reason` "stop"**, and 238 came
on the first attempt. No run was interrupted, none resumed, and none met a
failed call. Each record was committed before the next run began. The three
refusals were one rule that did not match its ticket and one with a duplicated
condition, both v1's checks, and one rule a repair round left unplaced.

**Stage C**, `PYTHONHASHSEED=0 python3 -m authorship.score`, zero API calls,
after `E-g1` to `E-g4` passed again: the hidden policy at 1.0000 through v1e's
declaration path, the baseline reproduced, the v1 replay, the 44 copies and the
fingerprint. It ran twice, as the provenance says; the record is the second.

---

## The four rows

Each statistic on each final base read whole, from case 0, as
`reuse/structure.py` read the baseline. The median adjudicates.

| row | statistic, surface | band | run 1 | run 2 | run 3 | median | baseline | verdict |
|---|---|---|---|---|---|---|---|---|
| **E-a** | nested pairs over all pairs | ≥ 0.05 | 0.0037 | 0.0014 | 0.0023 | **0.0023** | 0.0160 | **refuted** |
| **E-b** | subsumption alone, full corpus: silent error, coverage | ≤ 0.45 and ≥ 0.90 | 0.6448, 0.9925 | 0.6050, 0.9760 | 0.6890, 1.0000 | **0.6448, 0.9925** | 0.5521, 0.966 | **refuted** |
| **E-c** | share of the order's room the installed edges fill, exhaustive space | ≥ 0.50 | 1.0000 | 0.5798 | undefined | **undefined** | 0.3833 | **unadjudicable** |
| **E-d** | `contradice_subsuncion` verdicts, pooled | ≥ 1 | 2 | 6 | 0 | **8** | 0 | **holds** |

### What the verdicts say

- **`E-a`: the proposer did not write exceptions inside the rules they override.**
  3 nested pairs of 820, 10 of 7,140 and 1 of 435. The baseline, over distinct
  rules, had 0.0160 at the median. The drafter expected the refutation: a
  declaration works without nesting.
- **`E-b`: the bases are no sounder.** Subsumption alone decides nearly all the
  corpus and is wrong on 0.60 to 0.69 of what it decides, against 0.47 to 0.59 in
  the baseline. Over the space the same figure is 0.76 to 0.85. The drafter
  expected this one too: on the corpus subsumption sits at what the rules allow,
  and a discipline about placing rules does not change which queue the model
  writes.
- **`E-c`: the row cannot be read, and the reason is the finding.** Run 3's base
  holds one overlapping pair of 435, and that pair is nested. No pair could carry
  an edge, subsumption leaves no conflict over the space, and the order's room is
  zero points, so the share is undefined. **The other two runs are above the
  line**:
  - run 1: a room of 33,600 points of the space, all of it filled; the edges
    lift the end to end from 0.1823 to 0.4323, the hybrid bound;
  - run 2: a room of 27,560 points, 58% filled, from 0.1841 to 0.3030.
  They are two runs, not the row.
- **That verdict rests on a reading, and the reading is the scorer's.** §0 says
  that a room of zero leaves the share undefined, and that if the median is
  undefined the row is unadjudicable. It does not say what one undefined run
  does to a median of three. `authorship/score.py` does: a median over a run
  without a share is undefined, and a test pins it. Both were merged with the
  package, before the signature and before any run. **Under any other reading
  of the median the row holds**: whatever value run 3's share is given, the
  median of the three is 0.5798 or above, and without run 3 it is 0.7899. The
  record keeps the reading written down before the runs. Adopting another now
  would also adopt the verdict the drafter expected.
- **`E-d`: made to place a contained rule, the proposer sometimes called it a
  default.** 2 and 6 such declarations in runs 1 and 2, none in run 3. Level 1
  refused each one, as the engine was built to. v1 had told the proposer not to
  declare on nested pairs, so the verdict had never had a chance to fire.
  **[NOTE 2026-10-06, later]** In all eight the rule being placed contains the
  earlier one, and the proposer called the earlier one the default. Seven of
  the eight pairs carry one queue. See *The eight refused declarations*, below.

---

## How the proposer met the discipline — `E-e`, reported

**It overlapped less.** The discipline asks for a declaration against every rule
a new one overlaps, and a rule that overlaps nothing needs none.

| per run | baseline (v1): 1 · 2 · 3 | Stage E (v1e): 1 · 2 · 3 |
|---|---|---|
| rules born | 62 · 31 · 42 | 41 · 120 · 30 |
| born overlapping no earlier rule | 17 · 12 · 12 | **32 · 84 · 29** |
| as a share of the rules born | 0.27 · 0.39 · 0.29 | **0.78 · 0.70 · 0.97** |
| overlap among distinct rules | 0.0713 · 0.1138 · 0.0710 | **0.0366 · 0.0115 · 0.0023** |
| CONFLICTs in the loop's 2,000 arrivals | 30 · 5 · 12 | **0 · 0 · 0** |

- **No CONFLICT, so no order answer.** The order channel installed no edge in
  any run, and every installed edge came with a rule: 28, 76 and 1 accepted, 2, 6
  and 0 refused as contradicting subsumption.
- **Half the declarations were inert.** 29, 68 and 29 cited a rule the new one
  does not overlap, refused as `no_solapan`. The proposer placed itself against
  rules it was shown, not against the overlap the engine computes, and the
  repair rounds supplied the rest.
- **This is the trap §6.3 of the plan named**: *a proposer can obey by
  partitioning*. It is also the mechanism `ARBITRATION_REPORT.md` §3 describes,
  partitioning removes the error detector, now produced by the protocol meant to
  impose stratification.

### `E-c` on the corpus, and by channel

§0 asks `E-e` to report both, and adjudicates neither.

- **On the corpus the order had almost no room.** 15 and 47 arrivals of 2,000
  in runs 1 and 2, none in run 3. The installed edges filled 1.0000 and 0.4681
  of it, lifting the end to end from 0.3525 to 0.3600 and from 0.3855 to
  0.3965. The baseline's shares were 0.2326, 0.3636 and 0.4429.
- **By channel there is nothing to split.** The order channel installed no
  edge. Read with the write channel's edges alone every row is the row itself;
  read with the order channel's alone, `E-c`'s share is 0 where it is defined,
  because the end to end is subsumption's.

### The loop's own figures, beside the baseline

| per run | baseline: 1 · 2 · 3 | Stage E: 1 · 2 · 3 |
|---|---|---|
| reuse | 0.5323 · 0.8387 · 0.7381 | 1.0000 · 0.9083 · 0.9667 |
| silent error | 0.5939 · 0.5531 · 0.4760 | 0.6420 · 0.6051 · 0.6887 |
| proposal action accuracy | 0.4839 · 0.4839 · 0.5476 | 0.4524 · 0.4380 · 0.2903 |
| end to end | 0.3935 · 0.4400 · 0.5130 | 0.3505 · 0.3710 · 0.3065 |

**More reused, more often wrong, and the proposer chose the right queue less
often.** Two caveats the plan declared bear on the last two lines: a repair round
puts more rules in front of the model, which `PLAN_FIDELITY.md` found a sign may
cost it accuracy (§6.2), and the baseline was asked on 2026-09-30 and these runs
on 2026-10-05 (§6.4).

### The two rare queues

- **`ONCALL_ESCALATION`**: no rule decides any of its 7 tickets right, in any
  run of either protocol. Stage E escalated 0, 2 and 1 of them, against none in
  the baseline. The trigger is v1's, and the plan expected nothing better.
- **`SECURITY_INCIDENT`**: of its 20 tickets, the rules decided 19, 18 and 20,
  and decided right 14, 5 and 0. The baseline's rules decided 5, 17 and 18, and
  decided right 5, 6 and 18.

---

## The expectation, against the verdicts

**The drafter expected `E-c` and `E-d` to hold and `E-a` and `E-b` to be
refuted.** `E-a`, `E-b` and `E-d` came out as expected. `E-c`, the row the
drafter trusted least, came out neither: the plan named the partition trap in
§6.3 and did not guard the statistic against it, so the run that fell into the
trap took the row with it. §0 said that a run without room has no share, and
left what that does to a median of three to the scorer. **A plan that
adjudicates a median of shares should say in §0 itself what one run without room
does to the median**, because that sentence decides the row as surely as the
band does.

---

## What this settles, and what it does not

**What it settles.**

- **The third form of the second way has now been run.** Declaration imposed at
  write time, on this loop, produced partition rather than stratification. The
  proposer avoided most of the overlaps it would have had to declare.
- **P3's mechanism does not work through the base.** The discipline neither
  nested the rules (`E-a`) nor made subsumption over them sounder (`E-b`).
- **`contradice_subsuncion` has fired.** The counter `ARBITRATION_REPORT.md` §5
  called *a counter nobody has seen work* has now counted 8 contradictions, in
  two runs of three.

**What it does not settle.**

- **Whether imposed declaration supplies order.** `E-c` is unadjudicable. Where
  the proposer did overlap, its edges filled the room well, in two runs. A
  protocol that kept the proposer overlapping, v2's instruction to overlap
  joined to this discipline for instance, would be the test, and it is another
  plan.
- **The discipline alone.** The order answer was never used, so the bundle §6.1
  warned about reduced to the discipline and the copy refusal. Whether the
  partition comes from the requirement or from the instruction that states it
  cannot be separated in these runs.
- **The screen and the date** (§6.2, §6.4), which bear on the loop's own
  figures.
- **One model, one corpus, three draws.**

---

## The eight refused declarations — POST-RUN

*Added 2026-10-06. `authorship/refused.py` → [`refused.json`](refused.json),
`PYTHONHASHSEED=0`, from a clean tree, **zero API calls**. **POST-RUN with an
expectation written before the reading**: it is in the module's docstring, in
the commit *authorship/refused.py: the declarations level 1 refused, the
expectation first*, made before the module had read any of the eight. Its four
gates passed: the refusals are the ones `E-d` counted, each still contradicts
subsumption on the final base, that base reproduces Stage C's end to end on
both surfaces, and the truth masks partition the space. Not a signed row, and it
adjudicates nothing.*

`E-d` counted the declarations, and this reads whether they were right. Each
says that a rule should beat a rule strictly inside it, so over the narrower
rule's region the truth says which of the two queues holds. That is how `W-b` of
`PLAN_EDGES.md` read the installed edges.

**Seven of the eight were idle.**

- **All eight are a new rule claiming to beat an earlier rule inside it**, as
  the records force: no CONFLICT arose, so every rule was born on a ticket no
  earlier rule matched, and none of them can sit inside an earlier one.
- **Each new rule is the earlier one with a bound loosened.** Severity at most
  3 becomes at most 4; severity exactly 2 becomes at most 2; prior tickets
  exactly 0 or 2 become at most 2. Two of them drop a condition as well. All
  eight new rules send the ticket to `T2_TECHNICAL`.
- **Seven carry the same queue as the rule they claim to beat.** Over the
  narrower region nothing changes whichever way level 1 rules, so the refusal
  cost nothing and saved nothing. On two of them the truth over that region is
  never `T2_TECHNICAL`: 240 and 40 points of the space where both rules are
  wrong.
- **On the one pair with different queues, level 1 was right everywhere.** In
  run 2, `R0068`, which sends the ticket to `T2_TECHNICAL`, claimed to beat
  `R0025`, which sends it to `SELF_SERVICE_DEFLECT`. Over `R0025`'s region the
  truth is `SELF_SERVICE_DEFLECT` on all 40 points of the space and on both of
  its arrivals, and `T2_TECHNICAL` on none.

**So subsumption against declaration has met its first case, and only one.**
Where something was at stake, subsumption was right and the declaration was
wrong. One pair is a reading, not a rate.

### The expectation, against the reading

| clause | expected | read | |
|---|---|---|---|
| by construction | the declared winner is the rule being born | 8 of 8 | held |
| 1 | at least 5 of the 8 carry different queues | 1 of 8 | **failed** |
| 2, space | the declared winner is the better rule in more than half of the strict pairs | 0 of 1 | **failed** |
| 2, corpus | the same in half or fewer | 0 of 1 | held |
| 3 | most name `SECURITY_INCIDENT` as the winner's queue | 0 of 8 | **failed** |

**The drafter read the eight as edges like `PLAN_EDGES.md`'s, and they were
not.** Those were claims about whose queue holds where two rules disagree, and
nearly all of them were about the security keyword. Under v1e the proposer has
to declare against every rule it overlaps, whether the queues agree or not, and
when it widens a rule it calls the wider one the winner. What the expectation
missed is the discipline itself: it asks for a declaration where nothing is at
stake. The corpus clause held only because the one strict pair went against the
declared winner on both surfaces.

### What it changes

- **`E-d` stands as signed, and seven of the eight contradictions it counted
  are idle.** Each is a widening declared as a priority between rules with one
  queue, which no arbitration can make matter.
- **The discipline asked for declarations where nothing was at stake, and got
  them.** How many of the declarations level 1 accepted are between rules with
  one queue is not read here. It is free.

---

## Files

```
results_authorship/run_n20_smoke.json    Stage B: the smoke run
results_authorship/run_n2000_r1.json … run_n2000_r3.json   Stage B: the three runs
results_authorship/score.json            Stage C: E-a to E-d, E-e, the baseline
results_authorship/refused.json          POST-RUN: the eight refused declarations
authorship/plan.py                       the gate, §11's constants, §0's lines
authorship/protocol.py                   v1e's texts, the validator, the proposer
authorship/loop.py                       rung 2's loop with v1e's proposal path
authorship/gates.py                      E-g1 to E-g4
authorship/run.py                        Stage B: spends; guarded
authorship/score.py                      Stage C
authorship/refused.py                    POST-RUN: the refused declarations
tests/test_authorship.py                 the instrument, no figure
tests/test_authorship_refused.py         the POST-RUN reading, no figure
```

Reproducible with `PYTHONHASHSEED=0 python3 -m authorship.score`, about a minute
and a half, zero API calls, and the POST-RUN section with
`PYTHONHASHSEED=0 python3 -m authorship.refused`. `python3 -m authorship.run --dry-run` runs the
blocking checks and writes nothing.
