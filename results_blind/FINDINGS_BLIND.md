# Declaration beyond the keyword, with the rule drafted blind — findings

Record opened on October 12, 2026, under [`PLAN_BLIND.md`](../PLAN_BLIND.md).
Sergi signed §0 on 2026-10-11, before any figure below existed, in a commit of
its own: *PLAN_BLIND.md singed by Sergi*. Stage B's four records,
[`run_n20_smoke.json`](run_n20_smoke.json) and
[`run_n2000_r1.json`](run_n2000_r1.json) to [`run_n2000_r3.json`](run_n2000_r3.json),
name in their `_env` the commits they ran from, by their hashes on the branch
they were made on. A rebase merge gives those commits new hashes on `main` with
the same trees, so they are named here by their subjects. Stage C's record is
[`score.json`](score.json), and the three POST-RUN readings' are
[`readings.json`](readings.json), [`cycles.json`](cycles.json) and
[`closure.json`](closure.json). **This record owns every figure in it**, the
figures the plan computed while it was drafted included: §0 declared them, and
`K-g2` recomputed each before the signature and again before every run and the
scoring.

**The stage adjudicated its five signed rows on 2026-10-12: two hold and three
are refuted.** Every row is read where `has_security_keyword` is False.

- **Drafting blind made the proposer cross** (`K-a` holds). On the median, 0.2963
  of its births met no earlier rule of another queue there, against 0.9667 to
  1.0000 under the three baselines.
- **There, its declarations point at the better rule about one time in two**
  (`K-b` is refuted): 0.5460 by older rule, on 65 older rules.
- **A fixed ranking of the queues points the same pairs better** (`K-c` is
  refuted): 0.7219, a margin of −0.1759. Even "the new rule always wins" reads
  0.5804.
- **On the arrivals it is the same** (`K-e` is refuted): 0.5861, on 66 units.
- **The edges fill most of the order's room** (`K-d` holds, 0.6061), **and read
  POST-RUN that is mostly resolution.** A coin pointing the same edges fills
  0.40 to 0.45 of it, partly because its directions close cycles; among what
  each resolves, the declared directions beat a coin's clearly in one run of
  three. The ranking, pointing the same edges, fills more in every run.

> **PROVENANCE: PRE-REGISTERED.** `K-a` to `K-e` were signed before any of their
> figures existed. §0 said what a run without a birth outside the keyword reads
> for `K-a`, what too few units do to `K-b`, `K-c` and `K-e`, and what a run
> without room does to `K-d`. None of those cases arose. **`K-f` is reported, not
> adjudicated.** Everything labelled **POST-RUN** below was read after the
> verdicts existed. Stage B spent 287 calls, cents; Stage C and the reading spent
> none.

---

## What was run

**Stage B**, `blind/run.py`, under v2b, each from a clean tree after the key check
and `K-g1` to `K-g4`, all passing, with `PYTHONHASHSEED=0`. The full runs were run
in Sergi's terminal.

| record | from the commit | recorded (UTC) | calls | escalations | rules born | placement rounds | CONFLICTs |
|---|---|---|---|---|---|---|---|
| smoke, 20 cases | *PLAN_BLIND.md singed by Sergi* | 2026-10-10 22:25 | 22 | 14 | 13 | 8 | 0 |
| run 1, 2,000 cases | *…'s smoke run: 22 calls parsed, 13 rules born, 8 placement rounds exercised* | 2026-10-10 22:40 | 135 | 96 | 45 | 39 | 43 |
| run 2, 2,000 cases | *…'s run 1: 96 escalations, 45 rules born, 39 placement rounds* | 2026-10-11 08:57 | 57 | 33 | 28 | 24 | 0 |
| run 3, 2,000 cases | *…'s run 2: 33 escalations, 28 rules born, 24 placement rounds* | 2026-10-12 19:06 | 73 | 45 | 40 | 28 | 2 |

**Every one of the 287 answers ended with `finish_reason` "stop"**, and 285 came
on the first attempt. No call failed, no run was interrupted or resumed, and
each record was committed before the next run began. **One attempt at run 3 was
refused by the gate before anything was built**: it was launched from `main`,
where §0 is unsigned, because the signature sits on the plan's branch. Nothing
was spent, and the same command from the branch is the run above.

**Stage C**, `PYTHONHASHSEED=0 python3 -m blind.score`, zero API calls, from a
clean tree at the commit *…'s run 3: 45 escalations, 40 rules born, 28 placement
rounds*, after `K-g1` to `K-g4` passed again. It ran once.

**The POST-RUN reading**, `blind/readings.py`, ran twice. The first run, at the
commit that wrote its expectation, read `K-d` under other directions. **§0 says
each run's own value is published beside every row's reading, and `score.json`
pools `K-b`, `K-c` and `K-e` without giving each run's.** A decomposition was
added after the first run, in its own commit and labelled so; the record comes
from the second run, which gives back every figure of the first.

**The second POST-RUN reading**, `blind/cycles.py`, added on 2026-10-13, ran
twice too, each time from a clean tree. The first run, at the commit that wrote
its expectation, read why run 1 closed cycles. **It found every one closed by a
mechanism the expectation had not framed**, so a decomposition of what it had
read was added after it, in its own commit and labelled so. The record comes
from the second run, which gives back every figure of the first.

**The third POST-RUN reading**, `blind/closure.py`, added the same day, ran
once, from a clean tree at the commit that wrote its expectation.

---

## The five rows

Each final base read whole, from case 0. The baselines are v1, `PLAN_REUSE.md`'s
three runs, asked on 2026-09-30; v1e, `PLAN_AUTHORSHIP.md`'s, asked on
2026-10-05; and v2e, `PLAN_OVERLAP.md`'s, asked on 2026-10-06 and 07.

| row | statistic, surface | band | run 1 | run 2 | run 3 | reading | v1 | v1e | v2e | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| **K-a** | births overlapping no earlier rule of another queue, keyword rules apart, on the half of the space without the keyword; median | ≤ 0.50 | 0.2500 | 0.2963 | 0.3784 | **0.2963** | 1.0000 | 0.9667 | 1.0000 | **holds** |
| **K-b** | declared winner is the better rule over the shared region on that half, each older rule once, pooled; at least 20 units | ≥ 0.60 | 0.5455 | 0.7063 | 0.4397 | **0.5460**, 65 units, 111 of 198 | no unit | 0.5000, 2 units | 0.2500, 2 units | **refuted** |
| **K-c** | K-b less the Stage C ranking's reading on the same pairs | ≥ 0.00 | −0.1184 | −0.1656 | −0.2426 | **−0.1759**; the ranking 0.7219 | — | 0.0000 | −0.5000 | **refuted** |
| **K-d** | `O-b`'s share of the order's room on that half; median over the runs with room | ≥ 0.50 | 0.6061 | 0.6455 | 0.4496 | **0.6061** | under two runs with room | under two | under two | **holds** |
| **K-e** | K-b's edges over the 1,929 corpus cases without the keyword, each older rule once, pooled; at least 20 units | ≥ 0.60 | 0.5982 | 0.6803 | 0.5069 | **0.5861**, 66 units, 114 of 191 | no unit | 0.5000, 2 units | 0.0000, 2 units | **refuted** |

The run-by-run values of K-b, K-c and K-e are the decomposition the reading added
after its first run; the readings are the pooled ones §0 adjudicates.

### What the verdicts say

- **`K-a`: the blind draft did what it was for.** 11 of run 1's 44 births outside
  the keyword met no earlier rule of another queue there, 8 of run 2's 27, and 14
  of run 3's 37. The baselines read 0.8125 at their lowest. With the restriction
  lifted the shares are 0.1556, 0.1786 and 0.3250, where v2e read 0.2545,
  0.8049 and 1.0000. **The partition `FINDINGS2.md` traced to the base in view
  lifts when the base is out of view**, at n=2000 and beyond the keyword.
- **`K-b`: beyond the keyword the direction is near a coin's.** 111 of 198 strict
  pairs point at the better rule, 0.5606 pooled, and 0.5460 with each of the 65
  older rules counted once. By declared winner it is 0.5022. The runs read 0.5455,
  0.7063 and 0.4397.
- **`K-c`: a lookup table does better.** The Stage C hierarchy, which reads no
  rule, names the better rule on the same pairs 0.7219 of the time by older rule,
  and does better than the declared directions in every run. "The new rule always
  wins", the other rule of thumb `K-f` reads, gets 0.5804.
- **`K-d`: the edges fill the room**, 0.6061 on the median, and all three runs had
  room. What that is made of is a POST-RUN reading, two sections below.
- **`K-e`: no split by surface.** On the arrivals the direction is 0.5861, close
  to its reading over the function. The ranking reads 0.6848 there.

---

## Beyond the keyword: right where a ranking would be, a coin elsewhere

*From `score.json`, and the decomposition of `readings.json`.*

**Where a ranking can answer, the declarations are right; where it cannot, they
are a coin.** `B-d`'s split, on K-b's pairs: 3 of the 7 queue pairs carry the
better rule on both sides, and a fixed ranking cannot answer them.

- **On the pairs a ranking can answer**, the declared direction is right 0.8452
  by older rule, 18 of 26, on 14 units.
- **On the pairs it cannot**, 0.4747, 93 of 172, on 55 units.

It is the pattern `B-d` found in the pairwise answers about rung 1's blind rules,
0.8277 against 0.5801, now at write time: **the accurate part is what a ranking
already knows, and where the policy needs more than a ranking the direction is a
coin's.**

**The keyword is still where the direction is.** The edges K-b leaves out for
the keyword, declared at a birth on an impasse between rules of different
queues, read over the whole space: 0.8655 by older rule, 55 of 65, on 34 units.
Every installed edge between queues, whole space and every channel, `O-c`'s
statistic: 149 of 240, 0.6208.

**Against the pairwise answers it is a step down.** The same model, asked pair by
pair about rung 1's blind rules beyond the keyword, read 0.6618 by older rule over
the function and 0.6455 on the arrivals (§0). At write time it reads 0.5460 and
0.5861.

---

## K-d's fill, under other directions — POST-RUN

*Read after the verdicts existed, by `blind/readings.py` → `readings.json`, with
its expectation written and committed before it ran. It moves no verdict: `K-d`
stands as signed.*

The room is made of points where subsumption leaves rules of different queues in
conflict and one of them carries the true queue, and an edge between the rules in
conflict resolves such a point whichever way it points.
The reading installs the same accepted edges, in the same order, pointed five
ways, over the half of the space without the keyword:

| fill | run 1 | run 2 | run 3 |
|---|---|---|---|
| declared, `K-d` | 0.6061 | 0.6455 | 0.4496 |
| a coin, mean of 200 draws | 0.4030 | 0.4522 | 0.4433 |
| the Stage C ranking | 0.6239 | 0.7754 | 0.6271 |
| the new rule always wins | 0.5524 | 0.5179 | 0.4502 |
| the better rule of each edge | 0.8415 | 0.8704 | 0.8488 |

**Part of the declared arm's lead over a coin is resolution.**

- **The declared directions resolve almost the whole room**: 0.9516, 1.0000 and
  0.9933 of it.
- **A coin's resolve less**: 0.7685, 0.7977 and 0.9016 on average, because they
  close cycles the declared ones did not. Every draw had an edge refused, 30.5,
  13.8 and 23.7 on average.
- **Among what each resolves**, the declared arm is right 0.6370, 0.6455 and
  0.4526 of the time, and a coin 0.5239, 0.5650 and 0.4914 on average. **6%, 25.5%
  and 72.5% of the draws do at least as well as the declared arm.** It beats a
  coin's direction clearly in one run of three.
- **No arm loses a point** subsumption alone decided right.

**So `K-d` holds on a graph that resolves the room, with a direction above a
coin's in one run.** The same edges pointed by a fixed ranking of the queues fill
more in every run, and pointed at the better rule of each pair they fill 0.84 to
0.87: the edges themselves could have ordered the room, and the declarations'
directions were a coin's in two runs of three.

### The expectation, against the reading

| clause | expected | read | |
|---|---|---|---|
| 1 | a coin's mean fill between 0.40 and 0.60 in every run | 0.4030, 0.4522, 0.4433 | held |
| 2 | the declared fill inside the coin's central 90% in two runs of three | runs 2 and 3; run 1 above it | held |
| 3 | the declared arm resolves more of the room than a coin's mean in every run | 0.95 against 0.77, 1.00 against 0.80, 0.99 against 0.90 | held |
| 4 | the ranking fills more than the declared arm in every run | 0.6239, 0.7754, 0.6271 | held |
| 5 | the better rule of each edge fills at least 0.85 in every run | 0.8415, 0.8704, 0.8488 | **failed** |

The drafter declared the first and the third close to known for run 1 before the
reading. The fifth failed narrowly: in two runs the best direction of each edge, taken
pair by pair, filled 0.8415 and 0.8488, and why it falls short is not read here.

---

## How the proposer met the protocol — `K-f`, reported

**It crossed, and placed what it crossed.**

- **Births**: 45, 28 and 40; one born on a CONFLICT, in run 1, the rest on an
  impasse. Keyword rules among them: 1, 1 and 3.
- **Placement rounds**: 39, 24 and 28, listing 1 to 12 rules, 1 to 10, and 1 to
  22. **No placement answer changed the rule**, so `cambiada` never fired, and one
  per run left a rule unplaced.
- **Refused drafts**: 8, 4 and 2 rules that did not validate, every one of them
  for not matching its ticket.
- **Declarations**: 172, 70 and 118. Accepted: 136, 69 and 113. Refused as
  closing a cycle: 32, 0 and 3. Refused as contradicting subsumption: 4, 1 and 2.

**Run 1's CONFLICTs come from its refused cycles.** §2 of the plan expected
CONFLICTs rare, because under a forced placement a pair is left unordered only by
a refused declaration, and of the refused ones only a cycle leaves two crossing
rules unordered: a contradiction leaves them nested, for subsumption to order.
That is the mechanism, and the frequency was wrong: run 1's
placements closed 20 cycles on the write channel, and the first of its 43
CONFLICTs came at case 76. The proposer answered 30 of them with a copy of a
rule, which v2e's path refuses: copies of five rules, 14 of them of `R0034`. It
answered 12 with an order, whose edges were refused 12 times for closing a
cycle, and bore one rule. Runs 2 and 3 closed 0 and 1 cycle on placement, and had 0 and
2 CONFLICTs.

### The loop's own figures, beside the three baselines

| per run | v1: 1 · 2 · 3 | v1e: 1 · 2 · 3 | v2e: 1 · 2 · 3 | v2b: 1 · 2 · 3 |
|---|---|---|---|---|
| reuse | 0.5323 · 0.8387 · 0.7381 | 1.0000 · 0.9083 · 0.9667 | 1.0000 · 0.9268 · 1.0000 | 0.9556 · 0.9286 · 1.0000 |
| silent error | 0.5939 · 0.5531 · 0.4760 | 0.6420 · 0.6051 · 0.6887 | 0.6404 · 0.6527 · 0.5098 | 0.4669 · 0.4611 · 0.5049 |
| proposal action accuracy | 0.4839 · 0.4839 · 0.5476 | 0.4524 · 0.4380 · 0.2903 | 0.4821 · 0.4048 · 0.4545 | 0.5521 · 0.5152 · 0.5778 |
| end to end | 0.3935 · 0.4400 · 0.5130 | 0.3505 · 0.3710 · 0.3065 | 0.3495 · 0.3400 · 0.4875 | 0.5075 · 0.5300 · 0.4840 |

The baselines' columns are `FINDINGS_OVERLAP.md`'s. **On the median the loop's
end to end is 0.5075 under v2b**, against 0.4400 under v1 and about 0.35 under
v1e and v2e, **and the proposer chose the right queue for the ticket in front of
it 0.5521 of the time**, against 0.4839 under v1. Two caveats bear on these lines,
the ones §6 of the plan declared: the protocol is a bundle, and the runs were asked
three to twelve days after the baselines. `FINDINGS_FIDELITY.md` found a sign that a
screen of compiled rules costs the model accuracy, and a first call with no screen
is where that sign would show. Reported, never adjudicated.

### The two rare queues

- **`ONCALL_ESCALATION`**: no rule decides any of its 7 tickets right, in any run,
  and none of them escalated. The trigger is v1's.
- **`SECURITY_INCIDENT`**: of its 20 tickets, the rules decided 19, 20 and 19, all
  of them right.

---

## Why run 1 closed cycles — POST-RUN

*Read after the verdicts existed, by `blind/cycles.py` → `cycles.json`, with its
expectation written and committed before it ran. It moves no verdict. It reads no
truth, so it names no surface: only the placements the runs recorded and the
order the engine held when each was made.*

Each run is replayed through `blind/loop.py` with its own answers, record for
record, and the engine is forked at every call. Every refusal for a cycle, 32, 0
and 3, comes back on the fork of its call, with the path that closes it.

**The cycles are the base's own order, contradicted by a placement that never
saw it.**

- **Every refusal for a cycle at a placement closes the same way**: run 1's 20
  and run 3's one. The new rule contains an earlier rule. Subsumption ranks the
  narrower rule above the broader one, so a listed rule already ranked above that
  earlier rule was above the new rule before the new rule declared anything. The
  answer placed it below, and that declaration closed the cycle.
- **They sit on five births in run 1, with 7, 5, 4, 3 and 1 refusals, and on one
  in run 3.** Run 3's is the rule run 1 bore on the same case, 56.
- **In 16 of the 21, the earlier rule is of the new rule's own queue**, and a
  placement never lists those. The other five are one birth's. There the earlier
  rule was listed, and the answer placed it below the new rule too, against
  subsumption.

The largest is `R0040`, born in run 1 on case 987: a self-service rule for the
free tier, at severity 3 or 4, off hours. It contains `R0005`, the same rule with
at least five prior tickets, born on case 5. Eight rules born between them had
each been placed above `R0005` at their births: six technical, one billing, and
the keyword rule. `R0040`'s placement put it below the keyword rule and above the
other seven. Each of those seven declarations closed a cycle. `R0005` was never on
the list: it is of `R0040`'s queue.

**What the base had already decided.** This part was added after the first run.
It is a decomposition of what that run read, with no expectation. On each
placement it takes the listed rules the base had already ranked against the new
one, before any of its declarations.

| per run | 1 | 2 | 3 | pooled |
|---|---|---|---|---|
| births that met one | 6 | 2 | 4 | 12 |
| listed rules already ranked above the new one | 31 | 7 | 5 | 43 |
| of those, placed below it, against the base | 24 | 1 | 3 | 28 |
| refused for a cycle · against subsumption | 20 · 4 | 0 · 1 | 1 · 2 | 21 · 7 |
| listed rules not yet ranked, placed below the new one | 98 of 116 | 42 of 63 | 80 of 111 | 219 of 287 |

- **No listed rule was already ranked below a new one.**
- **Every refusal at a placement in the three runs is one of these 28, and all
  28 were refused.** A placement was refused exactly where it contradicted an
  order the base already held.
- **The answers show no sign of reading that order.** They placed 0.65 of the
  rules already above the new one below it, and 0.76 of the rules not yet
  ranked. Of the 15 that agreed with the base, 9 are keyword rules: a listed
  rule of `SECURITY_INCIDENT` was put above the new one 43 of the 44 times one
  was listed.

**So run 1 had more to contradict, and contradicted most of it.** Its births met
31 listed rules already above them, against 7 and 5 in runs 2 and 3. Its cycles
run through four early narrow rules, `R0004`, `R0005`, `R0014` and `R0015`. Many
later rules had been placed above them, and five later, broader rules contained
them. The proposer placed below its new rule most of what it was shown, as it
does everywhere.

**The slot moves nothing a test can see.**

- **Over the 128 pairs of listed rules a placement put on opposite sides**, the
  rule placed above the new one was listed second more often than first. That is
  −0.17 per pair pooled, with p 0.24 against 10,000 within-round permutations,
  and 0.64, 0.20 and 0.60 run by run.
- **The tilt is the last slot's.** 21 of the 67 rules listed last were placed
  above the new one, against 13 of the 67 listed first.
- **The slot could not have decided the cycles**, because none of them is a pair
  inside the list. Run 1 has the only three inverted pairs, and each sat on a
  `beats` already refused for containment.

**Asked again, the proposer answered the same.** All 12 of run 1's order-channel
refusals repeat, winner and loser, a declaration refused at a placement. They fall
on 6 distinct pairs, and three of `R0040`'s pairs account for 9. Each of run 1's 6
accepted order edges reverses one. Run 3's two order-channel refusals both repeat
its one.

### The expectation, against the reading

| clause | expected | read | |
|---|---|---|---|
| 1 | the slot statistic over mixed pairs, pooled, p ≥ 0.05 | 0.2424 | held |
| 2 | the inversion statistic, pooled, p ≥ 0.05 | 0.3346, on 3 pairs | held, on pairs that closed nothing |
| 3 | run 1's refusals from at most 6 births | 5 | held |
| 4 | run 1's inverted share at least twice runs 2 and 3's | 0.0109 against 0 | held, on pairs that closed nothing |
| 5 | at least 9 of run 1's 12 order refusals repeat a placement's | 12 | held |

**Five of five, on a wrong frame.** The drafter assumed a cycle at a placement
is a pair inverted inside the list, and bet clauses 2 and 4 on it. None of the 21
is. Those two clauses held on pairs that closed no cycle, and clause 4's 0.0109
against 0 says nothing about room. What answered the question was classifying
every refusal by what closed it, which the reading did beside its bets. The
decomposition above was added only after that.

---

## What the base's transitive order would decide — POST-RUN

*Read after the verdicts existed, by `blind/closure.py` → `closure.json`, with
its expectation written and committed before it ran. It moves no verdict. It is
read over the exhaustive space, uniform over its 134,400 points, and over the
2,000 corpus cases as they arrive.*

Rung 2's engine defeats a rule only with a rule that beats it directly and
matches the case. The *closure engine* defeats it with any rule that matches and
reaches it, through subsumption and declared edges together. The order is
acyclic, so the closure can only resolve a CONFLICT, to a queue in contention,
and it changes no decision. The reading rebuilds the final base of each of the
twelve paid runs of the loop at n=2000, three per protocol, and reads both
engines.

Every gate passes:
- each base gives back its published share of the order's room;
- the masks give `PriorityEngine.decide` on every corpus case;
- the closure changes no decision;
- the hidden policy is still 1.0000 through the closure.

**Under v2b, the closure resolves every CONFLICT, and decides them wrongly.**

| v2b, over the space | run 1 | run 2 | run 3 | pooled |
|---|---|---|---|---|
| CONFLICT points | 1,825 | 0 | 60 | 1,885 |
| resolved by the closure | 1,825 | — | 60 | 1,885 |
| the closure's queue is the true one | 10 | — | 60 | 70, 0.037 |
| a queue it overrules is | 535 | — | 0 | 535, 0.284 |
| no queue in contention is | 1,280 | — | 0 | 1,280, 0.679 |
| a coin over the queues in contention, expected | 272.5 | — | 30 | 302.5, 0.160 |
| the Stage C ranking | 520 | — | 0 | 520, 0.276 |
| end to end added | 0.0001 | 0 | 0.0004 | |

- **Every resolved point lies where a declaration refused for a cycle met the
  rule it was declared against.** The closure reads exactly the order the
  refusals kept.
- **In run 1 that order is the wrong one.** On 545 points a queue in contention
  is the true one. On 535 of them it is the queue the closure overrules: the
  side of the declaration the engine refused. On the other 1,280 points, neither
  side is right.
- **Run 3's one pair goes the other way**: the closure is right on all 60 points.
- **On the arrivals it reads the same.** Of v2b's 25 CONFLICT cases, the closure
  is right on 5, the side it overrules on 17, and neither on 3.

**Without a forced placement, the closure resolves little.**
- **Under v1** it resolves 0.037, 0.037 and none of the CONFLICT points over the
  space, of 34,440, 11,340 and 2,520. There the CONFLICTs are pairs that no chain
  orders.
- **Under v1e** no final base has a CONFLICT point.
- **Under v2e** only run 1 has any: 1,580, all resolved. The closure is right on
  950 of them and the overruled side on 630.
- **Over the function** the closure adds at most 0.0071 to any base's end to end
  over the space, in v2e's run 1, and under 0.0005 to any of v2b's.

### The expectation, against the reading

| clause | expected | read | |
|---|---|---|---|
| 1 | under v1e, v2e and v2b the closure resolves every CONFLICT, in every run with one | all, in the three runs that have one | held |
| 2 | under v1 it resolves less than half | 0.037, 0.037, none | held |
| 3 | pooled over v2b, the closure is right within 0.10 of a coin | 0.037 against 0.160 | **failed** |
| 4 | pooled over v2b, the ranking is right more often than the closure | 0.276 against 0.037 | held |
| 5 | in every v2b run the closure adds less than 0.01 | 0.0001, 0, 0.0004 | held |

**The third clause failed in the opposite direction from a coin.** The drafter
expected the base's order beyond the keyword to point the way its declarations
point, near a coin's. On v2b's contested points it points away from the truth:
of the 605 points where one side is right, 535 belong to the declaration the
engine refused.

The first clause was close to known, and it held. The forced protocols left a
CONFLICT point in only three of their nine runs.

---

## The expectation, against the verdicts

**The drafter expected `K-a`, `K-b` and `K-e` to hold and `K-c` and `K-d` to be
refuted. Two of five came out as expected**, `K-a` and `K-c`.

- **`K-b` and `K-e` were refuted**, the rows §0 called comfortable. The drafter
  set their lines under the pairwise answers' 0.6618 and 0.6455 and reasoned that
  nothing makes a declaration at write time worse than an answer to a question.
  At write time, about the proposer's own new rule, the direction was lower.
- **`K-d` held**, which the drafter expected refuted. Its statistic rewards
  resolving, the lesson `CLAUDE.md` records from `W-c`, and the drafter did not
  apply it to `O-b`'s statistic when it reused it. The POST-RUN reading above
  says what the hold rests on.
- **`K-a` held where the drafter trusted it least**, at 0.2963 against a proxy of
  0.4444.

---

## What this settles, and what it does not

**What it settles.**

- **Beyond the security keyword, declaration at write time carries direction
  barely above a coin's, and below a fixed ranking of the queues.** It answers the
  item `PLAN_EDGES.md` and `PLAN_OVERLAP.md` left: the keyword's rule of thumb was
  most of what the channel carried, and where it does not reach, the direction is
  right where a ranking would be and a coin's where it would not.
- **The partition was the base in view.** Drafted without it, at n=2000, the
  proposer crossed on 0.70 of its births on the median, beyond the keyword.
- **Under a forced placement the order's room fills, by resolution.** The graph
  resolves the room; a coin's directions resolve less of it, and a ranking's
  directions over the same edges fill more.

**What it does not settle.**

- **The blind draft apart from the placement**, and **the rules apart from the
  channel**: §13 of the plan declared both. Blind rules are not v2e's rules.
- **Why the loop's figures rose.** The bundle and the date are not separated.
- **Why run 1 closed cycles and runs 2 and 3 hardly did.** The records keep every
  placement and its listing order, so it can be read.
  **[NOTE 2026-10-13] Read POST-RUN**, in *Why run 1 closed cycles* above, and it
  is not the slot. Each cycle is the base's own order, contradicted by a placement
  that never saw it, and run 1 had more of that order to contradict.
- **One model, one corpus, three draws**, asked on three days.

---

## Files

```
results_blind/run_n20_smoke.json       Stage B: the smoke run
results_blind/run_n2000_r1.json … run_n2000_r3.json   Stage B: the three runs
results_blind/score.json               Stage C: K-a to K-e, K-f, the baselines
results_blind/readings.json            POST-RUN: K-d under other directions, and
                                       K-b to K-e run by run
results_blind/cycles.json              POST-RUN: why run 1 closed cycles, and what
                                       the base had already decided
results_blind/closure.json             POST-RUN: what the base's transitive order
                                       would decide, on the twelve bases
blind/plan.py                          the gate, §11's constants, §0's lines, the
                                       figures §0 declares
blind/protocol.py                      v2b's texts, the blind screen, the placement,
                                       the same-rule check, the proposer
blind/loop.py                          rung 2's loop with v2b's blind path
blind/rows.py                          §0's statistics, one instrument for
                                       baselines and runs
blind/gates.py                         K-g1 to K-g4
blind/run.py                           Stage B: spends; guarded
blind/score.py                         Stage C
blind/readings.py                      POST-RUN: K-d under other directions
blind/cycles.py                        POST-RUN: why run 1 closed cycles
blind/closure.py                       POST-RUN: the closure engine, beside rung 2's
tests/test_blind.py                    the instrument, no figure
tests/test_blind_readings.py           the POST-RUN reading of K-d, no figure
tests/test_blind_cycles.py             the POST-RUN reading of the cycles, no figure
tests/test_blind_closure.py            the POST-RUN reading of the closure, no figure
```

Reproducible with `PYTHONHASHSEED=0 python3 -m blind.score`,
`PYTHONHASHSEED=0 python3 -m blind.readings`,
`PYTHONHASHSEED=0 python3 -m blind.cycles` and
`PYTHONHASHSEED=0 python3 -m blind.closure`, minutes, zero API calls.
`python3 -m blind.run --dry-run` runs the blocking checks and writes nothing.
