# Stage E asked again: imposed declaration, with the proposer kept overlapping — findings

Record opened on October 7, 2026, under [`PLAN_OVERLAP.md`](../PLAN_OVERLAP.md).
Sergi signed §0 on 2026-10-06, before any figure below existed, in a commit of
its own: *PLAN_OVERLAP.md signed by Sergi*. Stage B's four records,
[`run_n20_smoke.json`](run_n20_smoke.json) and
[`run_n2000_r1.json`](run_n2000_r1.json) to [`run_n2000_r3.json`](run_n2000_r3.json),
name in their `_env` the commits they ran from, by their hashes on the branch
they were made on. A rebase merge gives those commits new hashes on `main` with
the same trees, so they are named here by their subjects. Stage C's record is
[`score.json`](score.json). **This record owns every figure in it**, the
baselines' figures the plan computed while it was drafted included: §0 of the
plan declared them, and `O-g2` recomputed each before the signature and again
before this scoring.

**The stage adjudicated its three signed rows on 2026-10-07: one is refuted and
two hold.**

- **The proposer still partitioned** (`O-a` is refuted). In two runs of three,
  80% and all of the rules it wrote overlap no earlier rule of another queue. In
  the other run, 25%. **[NOTE 2026-10-08]** That run's overlap is one rule,
  read POST-RUN: without it, the run reads 0.8545 (*What separates the run that
  overlapped*, below). **[NOTE 2026-10-08, later]** Read the same way, v1
  partitioned too, and v2e more (*What v1's overlap is made of*, below).
- **Where it left room, its declarations filled most of it** (`O-b` holds). They
  filled 73% and all of the order's room over the space in runs 1 and 2. Run 3
  left none, and §0's rule left it out.
- **The declarations it installed pointed at the better rule 44 times in 47**
  (`O-c` holds). **Nearly all of them are one rule of thumb**, read POST-RUN: 43
  of the 47 say that a ticket with the security keyword goes to
  `SECURITY_INCIDENT` before `T2_TECHNICAL`. The other four were right once.
- **The exemption removed the idle edges, and the contradictions with them**
  (`O-d`, reported). No edge between rules of one queue was installed, against
  v1e's 15, and no declaration contradicted subsumption, against v1e's 8.

> **PROVENANCE: PRE-REGISTERED.** `O-a` to `O-c` were signed before any of their
> figures existed. §0 said what a run without room does to `O-b`, what a run
> without a birth reads for `O-a`, and that `O-c` has no verdict with no edge to
> read: the kind of case `PLAN_AUTHORSHIP.md` left to its scorer. Only the first
> arose, and the verdicts need no reading. **`O-d` is reported, not
> adjudicated.** Everything labelled **POST-RUN** below was read after the
> verdicts existed. Stage B spent 136 calls, cents; Stage C spent none.

---

## What was run

**Stage B**, `overlap/run.py`, under v2e, each from a clean tree after the key
check and `O-g1` to `O-g4`, all passing. The full runs were run in Sergi's
terminal.

| record | from the commit | asked on | calls | rules born | refused | repair rounds |
|---|---|---|---|---|---|---|
| smoke, 20 cases | *PLAN_OVERLAP.md signed by Sergi* | 2026-10-06 | 11 | 10 | 0 | 1 |
| run 1, 2,000 cases | *…'s smoke run: 11 calls parsed, 10 rules born, a repair round exercised* | 2026-10-06 | 65 | 55 | 1 | 9 |
| run 2, 2,000 cases | *…'s run 1: 56 escalations, 55 rules born, 9 repair rounds* | 2026-10-07 | 49 | 41 | 1 | 7 |
| run 3, 2,000 cases | *…'s run 2: 42 escalations, 41 rules born, 7 repair rounds* | 2026-10-07 | 11 | 11 | 0 | 0 |

**Every one of the 136 answers ended with `finish_reason` "stop"**, and 132 came
on the first attempt. No run was interrupted, none resumed, and none met a
failed call. Each record was committed before the next run began. The two
refusals:

- **Run 1's one CONFLICT was answered with a copy.** The proposer rewrote the
  rule it wanted to win, `R0017`, and the copy was refused. The order answer the
  escalation offered was not used, here or anywhere else.
- **Run 2 refused one rule left unplaced.** It overlapped 34 rules of other
  queues. The repair round listed all 34, and the second answer still left some
  of them unplaced.

**Stage C**, `PYTHONHASHSEED=0 python3 -m overlap.score`, zero API calls, from a
clean tree at the commit *…'s run 3: 11 escalations, 11 rules born, no repair
round*, after `O-g1` to `O-g4` passed again. It ran once.

---

## The three rows

Each final base read whole, from case 0. The baselines are v1, `PLAN_REUSE.md`'s
three runs, asked on 2026-09-30, and v1e, `PLAN_AUTHORSHIP.md`'s, asked on
2026-10-05.

| row | statistic, surface | band | run 1 | run 2 | run 3 | reading | v1 | v1e | verdict |
|---|---|---|---|---|---|---|---|---|---|
| **O-a** | births overlapping no earlier rule of another queue, overlap read over the space; median | ≤ 0.50 | 0.2545 | 0.8049 | 1.0000 | **0.8049** | 0.3333 | 0.8049 | **refuted** |
| **O-b** | share of the order's room the installed edges fill, exhaustive space; median over the runs with room | ≥ 0.50 | 0.7320 | 1.0000 | no room | **0.8660** | 0.3833 | 0.7899 | **holds** |
| **O-c** | installed edges between queues whose declared winner is the better rule, exhaustive space; pooled | ≥ 0.70 | 23 of 26 | 21 of 21 | none | **44 of 47, 0.9362** | 34 of 45, 0.7556 | 58 of 84, 0.6905 | **holds** |

### What the verdicts say

- **`O-a`: the partition held in two runs of three.** 14 of 55 births, 33 of 41
  and 11 of 11 overlapped no earlier rule of another queue. Run 1 overlapped
  more than any v1 run, whose shares were 0.3226 to 0.4839. **[NOTE 2026-10-08]**
  Through one rule: 38 of its 41 births with a rule of another queue in their
  `O` met `R0017`, which covers half the space (*What separates the run that
  overlapped*). **[NOTE 2026-10-08, later]** And v1's shares are not like for
  like with v2e's: read the same way, v1 partitioned too (*What v1's overlap is
  made of*). Run 3 wrote eleven rules, and none of them met a rule of another
  queue. **The median is v1e's to
  the fourth decimal, by coincidence**: two bases of 41 rules, 33 born alone,
  that share no rule.
- **`O-b`: where there was room, the declarations filled it.**
  - run 1: a room of 67,280 points of the space, half of it, 73% filled; the
    edges lift the end to end from 0.1501 to 0.5166, against a bound of 0.6507;
  - run 2: a room of 25,200 points, all filled, from 0.3104 to 0.4979, the bound;
  - run 3: eleven rules, three overlapping pairs and one of them nested, none
    across queues without nesting, so no room. §0 named such a run and left it
    out, and the median of the other two is their mean.

  **This time §0 said what a run without room does**, and the verdict needs no
  reading of the median.
- **`O-c`: the installed edges pointed right 44 times in 47**, well above both
  baselines. 28 more edges in run 1 had no strict better rule, and 4 had a
  shared region where neither rule is ever right. What the 47 are is the next
  section.

---

## One rule of thumb under `O-b` and `O-c` — POST-RUN

*Read after the verdicts existed, off the runs' records and `score.json`. It
moves no verdict.*

**71 of the 79 installed edges were won by two rules of one kind.**

- **In run 1, `R0017`**, *a ticket with the security keyword goes to
  `SECURITY_INCIDENT`*, born at case 19, won 50 of the 58 installed edges, each
  over a rule of `T2_TECHNICAL`.
- **In run 2, `R0024`**, the same with *severity at most 2*, born at case 44,
  won all 21.

**`O-c` is that declaration.**

- **43 of its 47 strict pairs are those two rules' edges, and all 43 are
  right.** The other four went one right and three wrong.
- **`R0017`'s other 28 edges tie.** On each of their shared regions the truth
  splits exactly between `SECURITY_INCIDENT` and `T2_TECHNICAL`, so neither rule
  is the better one.

**So is `O-b`'s fill.** `R0017`'s edges alone fill 0.7240 of run 1's room, against
0.7320 with every edge; the other edges alone fill 0.0033. In run 2 every
installed edge is `R0024`'s.

**It is the rule of thumb `FINDINGS_EDGES.md` found behind 47 of v1's 50 installed
edges**, which over the function points right because the hidden policy sends
most of the space's keyword points to `SECURITY_INCIDENT`
([`results_edges/FINDINGS_EDGES.md`](../results_edges/FINDINGS_EDGES.md)). Both
rows hold as signed. What they say is narrower than they read: the declarations
this protocol forced point right, and fill the room, where they repeat that one
rule. Elsewhere there are four of them to read.

---

## How the proposer met the protocol — `O-d`, reported

**It partitioned in two runs of three, as under v1e, and overlapped in the
third.**

| per run | v1: 1 · 2 · 3 | v1e: 1 · 2 · 3 | v2e: 1 · 2 · 3 |
|---|---|---|---|
| rules born | 62 · 31 · 42 | 41 · 120 · 30 | 55 · 41 · 11 |
| born overlapping no earlier rule at all | 17 · 12 · 12 | 32 · 84 · 29 | 12 · 30 · 8 |
| born overlapping no earlier rule of another queue, O-a | 20 · 15 · 14 | 33 · 95 · 29 | 14 · 33 · 11 |
| overlap among distinct rules | 0.0713 · 0.1138 · 0.0710 | 0.0366 · 0.0115 · 0.0023 | 0.0566 · 0.0305 · 0.0545 |
| CONFLICTs in the loop's 2,000 arrivals | 30 · 5 · 12 | 0 · 0 · 0 | 1 · 0 · 0 |

**The exemption did its work, and only that.**

- **It was exercised.** On 22 of run 1's 64 calls that computed an overlapped
  set, 6 of run 2's 49 and 3 of run 3's 11, at least one overlapped rule carried
  the new rule's queue and was owed nothing.
- **Nothing idle reached the graph.** The proposer still declared against a rule
  of its own queue 18 times in 127 declarations, 10, 6 and 2. Every one of them
  was inert: 17 refused as `no_solapan` and one redundant with subsumption. No
  edge between rules of one queue was installed, against 15 under v1e.
- **No declaration contradicted subsumption**, against 8 under v1e, seven of
  which joined rules of one queue.
- **The declarations, by verdict**: 79 installed, all between queues; 45 refused
  as `no_solapan`; 2 refused as `cierra_ciclo`; 1 redundant. A third of them
  cited a rule the new one does not overlap, against half under v1e.

### `O-b` on the corpus, pooled, and by channel

§0 asks `O-d` to report these, and adjudicates none.

- **On the corpus the order had little room**: 81 arrivals of 2,000 in run 1
  and 15 in run 2. The edges filled 0.2593 and 1.0000 of it: the end to end went
  from 0.3515 to 0.3620 and from 0.3410 to 0.3485.
- **Pooled over the runs, over the space**, the edges fill 0.8050 of the room.
  §0 adjudicates on the median, because pooled v1 already reads 0.5175.
- **By channel there is nothing to split.** The order channel installed no edge.

### The loop's own figures, beside both baselines

| per run | v1: 1 · 2 · 3 | v1e: 1 · 2 · 3 | v2e: 1 · 2 · 3 |
|---|---|---|---|
| reuse | 0.5323 · 0.8387 · 0.7381 | 1.0000 · 0.9083 · 0.9667 | 1.0000 · 0.9268 · 1.0000 |
| silent error | 0.5939 · 0.5531 · 0.4760 | 0.6420 · 0.6051 · 0.6887 | 0.6404 · 0.6527 · 0.5098 |
| proposal action accuracy | 0.4839 · 0.4839 · 0.5476 | 0.4524 · 0.4380 · 0.2903 | 0.4821 · 0.4048 · 0.4545 |
| end to end | 0.3935 · 0.4400 · 0.5130 | 0.3505 · 0.3710 · 0.3065 | 0.3495 · 0.3400 · 0.4875 |

**On the median, the loop's end to end is 0.4400 under v1, 0.3505 under v1e and
0.3495 under v2e.** The caveats §6 of the plan declared bear on these lines:
the screen grows with v2's rendering and the repair rounds (§6.5), and the
three protocols were asked on 2026-09-30, 2026-10-05 and 2026-10-06 to 07
(§6.6).

### The two rare queues

- **`ONCALL_ESCALATION`**: no rule decides any of its 7 tickets right, in any
  run of any of the three protocols, and v2e escalated none of them. The trigger
  is v1's.
- **`SECURITY_INCIDENT`**: of its 20 tickets, the rules decided 20, 17 and 20,
  and decided right 20, 14 and 0. Runs 1 and 2 are the runs of `R0017` and
  `R0024`.

---

## The expectation, against the verdicts

**The drafter expected `O-b` to hold and `O-a` and `O-c` to be refuted.** `O-a`
and `O-b` came out as expected. `O-a`'s median came out at 0.8049, above the
drafter's guess of about 0.6. **`O-c` held, at 0.9362, against the drafter's
expectation of a refutation.** The drafter reasoned that more overlap would
bring more forced declarations on harder pairs. Instead, 71 of the 79 edges the
proposer installed repeated one easy declaration, and the hard pairs were too
few to weigh.

---

## What this settles, and what it does not

**What it settles.**

- **Imposed declaration makes this proposer partition in two runs of three,
  even when it is told that overlap is normal and asked only where the queues
  differ.** The plan said before the runs that this outcome would close P3 of
  `ARBITRATION_REPORT.md` §7 on this model, and it does, with one qualification:
  run 1 overlapped more than any v1 run did, so the partition is the usual
  outcome and not the only one. **[NOTE 2026-10-08] The qualification does not
  survive a POST-RUN reading.** Run 1's overlap is its births meeting `R0017`.
  Without that one rule, run 1 reads 0.8545, as partitioned as the other two
  (*What separates the run that overlapped*).
- **Where the proposer did overlap, the declarations ordered what subsumption
  left over the function** (`O-b`), in two runs. Read POST-RUN, the ordering is
  one rule of thumb about the security keyword, the one `PLAN_EDGES.md` found
  behind v1's edges.
- **Asking only where the queues differ removes the idle edges and the
  contradictions**, and loses a perfect author nothing (`O-g1`).

**What it does not settle.**

- **Whether forced declarations carry direction beyond the keyword.** Four strict
  pairs, one right, is not a rate.
- **The framing apart from the discipline**, and **the requirement apart from
  the paragraph that states it**: neither had a control arm (§13 of the plan).
- **The corpus.** The order's room there was 81 and 15 arrivals of 2,000.
- **One model, one corpus, three draws**, asked on two days.

---

## What separates the run that overlapped — POST-RUN

*Added 2026-10-08. `overlap/readings.py` → [`readings.json`](readings.json),
`PYTHONHASHSEED=0`, from a clean tree, **zero API calls**. **POST-RUN with an
expectation written before the reading**: it is in the module's docstring, in
the commit *overlap/readings.py: what separates the run that overlapped, the
expectation first*, made before the module read any rule's conditions beyond
`R0017` and `R0024`. Its two gates passed in every run: the replay of the births
gives `O-a`'s count, and every born rule's recorded `O`, rule for rule. Not a
signed row, and it adjudicates nothing.*

`O-a` read 0.2545 in run 1, against 0.8049 and 1.0000. A low share can mean a
proposer writing across the other queues' regions, or one broad rule that every
later birth meets. Each birth's `O` names the rules it met, so the records tell
the two apart.

**It is one broad rule.**

- **Run 1's overlap is `R0017`.** *A ticket with the security keyword goes to
  `SECURITY_INCIDENT`*, born at case 19, covers half the space. It is in the `O`
  of 38 of the 41 births that met a rule of another queue, and every one of the
  38 rules born after it met it. None of them excludes keyword tickets, the only
  way to avoid it.
- **Without it, run 1 partitions like the others.** As if `R0017` met nothing,
  47 of run 1's 55 births overlap no earlier rule of another queue, 0.8545, more
  than run 2's 0.8049.
- **Run 2 is the same, smaller.** `R0024`, the keyword rule with *severity at
  most 2*, born at case 44, covers a quarter of the space and is in 7 of the 8
  `O`s of run 2. Without it, 40 of 41.
- **Run 3 tiled the space with broad rules.** Its eleven rules each cover a
  tenth of the space at the median, against an eightieth in run 1 and a fortieth
  in run 2, and all eleven condition on the customer's tier and the product.
  None of them met a rule of another queue.
- **The runs are front-loaded.** 50 of run 1's 55 rules, 37 of run 2's 41 and
  all of run 3's were born in the first 500 cases.

So **the proposer partitioned in all three runs, measured against every rule
but one**, and run 1's low `O-a` is that one rule's breadth: a rule on the
keyword alone covers half the space, so any later rule that does not mention the
keyword meets it. The partition held in every other respect. Whether run 1's
later rules left the keyword alone because v2 tells the proposer not to narrow a
rule to dodge another, or because they never considered it, these runs cannot
say.

### The expectation, against the reading

| clause | expected | read | |
|---|---|---|---|
| 1 | run 1's top rule is in at least half of its births' `O`s | 38 of 41 | held |
| 2 | without it, run 1's `O-a` is above 0.50 | 0.8545 | held |
| 3 | run 3's median share of the space is the largest | 0.0125 · 0.025 · 0.1 | held |
| 4 | in runs 2 and 3, one attribute is in three rules in four | all of them, in both | held |

The drafter declared the first and third close to known before the reading. The
fourth held and **does not separate the runs**: run 1 conditions 54 of its 55
rules on the product and on the severity. The second is the reading's result.

### What it changes

- **`O-a` stands as signed, and its refutation is stronger than it read.** The
  one run under the line was under it through one rule.
- **The qualification this record gave in *What this settles* does not
  survive**: dated notes say so where it was written.
- **Whether v1's overlap is one rule's breadth too is not read here.** The same
  reading over `PLAN_REUSE.md`'s runs would say, and it is free.

---

## What v1's overlap is made of — POST-RUN

*Added 2026-10-08. `overlap/readings_v1.py` → [`readings_v1.json`](readings_v1.json),
`PYTHONHASHSEED=0`, from a clean tree, **zero API calls**. **POST-RUN with an
expectation written before the reading**, in the commit *overlap/readings_v1.py:
what v1's overlap is made of, the expectation first*, made before the module
read any v1 rule's conditions. A diagnostic was added after the first run, in
its own commit and labelled so, *overlap/readings_v1.py: v1's births on an
impasse, apart — added after the run*; the record comes from a second run at
that commit, which reproduced every figure of the first. Its three gates passed
in every run: the replay gives the v1 shares §0 of the plan declares, the bases
have `structure.json`'s rule counts, and the births on a CONFLICT number each
record's CONFLICTs. Not a signed row, and it adjudicates nothing.*

`O-a`'s baseline is v1, `PLAN_REUSE.md`'s three runs, at 0.3226, 0.4839 and
0.3333. Read the way *What separates the run that overlapped* read v2e's runs,
**it is made of the security keyword too**, in two forms.

- **One broad keyword rule, in runs 2 and 3.**
  - run 3: `R0013`, *a ticket with the security keyword goes to
    `SECURITY_INCIDENT`*, born on case 19, half the space, is in 18 of the 28
    `O`s; without it, 0.5714;
  - run 2: `R0018`, the same with *severity 1*, born on case 44, an eighth of
    the space, is in 9 of the 16; without it, 0.7742.
- **Keyword rules written on CONFLICTs, in run 1.** v1 answered every CONFLICT
  with a rule, and every rule born on one meets a rule of another queue: 30, 5
  and 12 births. In run 1, 28 of the 30 are `SECURITY_INCIDENT` rules on the
  keyword, each meeting the `T2_TECHNICAL` rules it conflicted with. So run 1's
  overlap is spread over those rules: its top rule, `R0020`, a `T2_TECHNICAL`
  rule, is in 29 of its 42 `O`s, and without it run 1 barely moves, 0.3387.
- **v2e bore no rule on a CONFLICT in any run**, off its records.

**The same first tickets wrote the same broad rules under both protocols.** Case
19 is the corpus's first ticket with the security keyword, and case 44 its
third. The rule born on case 19 is *keyword alone, to `SECURITY_INCIDENT`* in
v1's run 3 and v2e's run 1, the runs it carries; on case 44, *keyword with low
severity* in both runs 2. The later rules that do not mention the keyword
overlap it under both protocols: 18 of the 29 born after `R0013` in v1's run 3,
2 excluding the keyword and 9 on it with the same queue, and all 38 born after
`R0017` in v2e's run 1.

### Like for like

v2e's births all came on an impasse. Read on v1's births on an impasse alone,
with the diagnostic added after the first run:

| births on an impasse that overlap no earlier rule of another queue | run 1 | run 2 | run 3 | median |
|---|---|---|---|---|
| v1 | 0.6250 | 0.5769 | 0.4667 | 0.5769 |
| v1, without its top rule | 0.6250 | 0.9231 | 0.8000 | 0.8000 |
| v2e, `O-a` | 0.2545 | 0.8049 | 1.0000 | 0.8049 |
| v2e, without its top rule | 0.8545 | 0.9756 | 1.0000 | 0.9756 |

**Read like for like, v1 partitioned too, and v2e more.** On births on an impasse
and without each run's top rule, v1 sits at 0.80 and v2e at 0.98, both above
`O-a`'s line. The gap `O-a` read between them, 0.3333 against 0.8049, is
mostly births on a CONFLICT and one broad keyword rule.

### The expectation, against the reading

| clause | expected | read | |
|---|---|---|---|
| by construction | every birth on a CONFLICT has a non-empty `O` | 30 of 30, 5 of 5, 12 of 12 | held |
| 2 | without each top rule, v1's median `O-a` at most 0.50 | 0.5714 | **failed** |
| 3 | every v1 top rule is `SECURITY_INCIDENT` on the keyword | runs 2 and 3; run 1's is `T2_TECHNICAL` | **failed** |

The drafter gave the second clause about even odds, reasoning from run 1, whose
births on a CONFLICT do keep its overlap spread. Runs 2 and 3 had few CONFLICTs
and one broad rule each, as v2e's runs did. The third failed on the same run:
its keyword rules are the 28 born on CONFLICTs, not its top rule.

### What it changes

- **`O-a` stands as signed**: 0.8049 is above its line, and so is v2e under every
  reading here.
- **Its baseline was not like for like.** §0 set the line between v1's 0.3333 and
  v1e's 0.8049, nearer the protocol that did not partition. Read on births on an
  impasse and without each top rule, v1 partitioned too, at 0.80, so the line
  sat below both protocols. What v2e changed against v1 is smaller than `O-a`'s
  baseline makes it look: 0.98 against 0.80.
- **Under both protocols, nearly everything `O-a` counted as overlap is the
  security keyword**: the breadth of the rule written for the first keyword
  tickets, and in v1 the keyword rules written on CONFLICTs.

---

## Files

```
results_overlap/run_n20_smoke.json    Stage B: the smoke run
results_overlap/run_n2000_r1.json … run_n2000_r3.json   Stage B: the three runs
results_overlap/score.json            Stage C: O-a to O-c, O-d, both baselines
results_overlap/readings.json         POST-RUN: what separates the run that overlapped
results_overlap/readings_v1.json      POST-RUN: what v1's overlap is made of
overlap/plan.py                       the gate, §11's constants, §0's lines, the baselines §0 declares
overlap/protocol.py                   v2e's texts, the exempted split, the proposer
overlap/loop.py                       rung 2's loop with v2e's proposal path
overlap/rows.py                       §0's statistics, one instrument for baselines and runs
overlap/gates.py                      O-g1 to O-g4
overlap/run.py                        Stage B: spends; guarded
overlap/score.py                      Stage C
overlap/readings.py                   POST-RUN: what separates the run that overlapped
overlap/readings_v1.py                POST-RUN: what v1's overlap is made of
tests/test_overlap.py                 the instrument, no figure
tests/test_overlap_readings.py        the POST-RUN reading, no figure
tests/test_overlap_readings_v1.py     its v1 reading, no figure
```

Reproducible with `PYTHONHASHSEED=0 python3 -m overlap.score`, a few minutes, zero
API calls. `python3 -m overlap.run --dry-run` runs the blocking checks and writes
nothing.
