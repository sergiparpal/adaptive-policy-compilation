# Status

What is known, as of October 21, 2026. **Not a history** — that is the four
`FINDINGS` records, [`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md),
[`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md) and
[`results/FINDINGS_DEFAULT_RULE.md`](results/FINDINGS_DEFAULT_RULE.md),
[`results_sensitivity/FINDINGS_SENSITIVITY.md`](results_sensitivity/FINDINGS_SENSITIVITY.md),
[`results_ilp/FINDINGS_ILP.md`](results_ilp/FINDINGS_ILP.md),
[`results_reuse/FINDINGS_REUSE.md`](results_reuse/FINDINGS_REUSE.md),
[`results_fidelity/FINDINGS_FIDELITY.md`](results_fidelity/FINDINGS_FIDELITY.md),
[`results_edges/FINDINGS_EDGES.md`](results_edges/FINDINGS_EDGES.md),
[`results_primacy/FINDINGS_PRIMACY.md`](results_primacy/FINDINGS_PRIMACY.md),
[`results_why/FINDINGS_WHY.md`](results_why/FINDINGS_WHY.md),
[`results_authorship/FINDINGS_AUTHORSHIP.md`](results_authorship/FINDINGS_AUTHORSHIP.md),
[`results_overlap/FINDINGS_OVERLAP.md`](results_overlap/FINDINGS_OVERLAP.md),
[`results_blind/FINDINGS_BLIND.md`](results_blind/FINDINGS_BLIND.md),
[`results_screen/FINDINGS_SCREEN.md`](results_screen/FINDINGS_SCREEN.md),
[`results_bound/FINDINGS_BOUND.md`](results_bound/FINDINGS_BOUND.md),
[`results_ranking/FINDINGS_RANKING.md`](results_ranking/FINDINGS_RANKING.md),
[`results_students/FINDINGS_STUDENTS.md`](results_students/FINDINGS_STUDENTS.md),
[`results_escalations/FINDINGS_ESCALATIONS.md`](results_escalations/FINDINGS_ESCALATIONS.md),
[`results_spotcheck/FINDINGS_SPOTCHECK.md`](results_spotcheck/FINDINGS_SPOTCHECK.md),
[`results_unreached/FINDINGS_UNREACHED.md`](results_unreached/FINDINGS_UNREACHED.md) and
[`results_manual/FINDINGS_MANUAL.md`](results_manual/FINDINGS_MANUAL.md),
each with its dated errata in place. Every figure here already exists in one
of them.

**The project.** A cheap symbolic engine resolves the cases it covers; on one it
does not cover (an *impasse*), an LLM acts and writes a rule so that next time it
does. Ticket triage: 8 attributes, 8 queues, a hidden policy of 29 rules in 8
priority layers. Four rungs closed, plus an audit of the instrument behind two of
them, plus two pairwise threads — `PLAN_PAIRWISE.md` and `PLAN_PROPOSER_1600.md`,
seven signed rows between them — plus the sensitivity sweep of
`PLAN_SENSITIVITY.md`, five more, which asks how much of rung 1's failure is this
policy's shape, plus ILP as a competitor in `PLAN_ILP.md`, plus **the founding
question itself, on the engine that can answer it, in `PLAN_REUSE.md`** — six
signed rows, closed on 2026-09-30 — plus **its cleanest form, fidelity, in
`PLAN_FIDELITY.md`**: six more, closed on 2026-10-04 — plus **what the edges the
proposer declared at write time bought, in `PLAN_EDGES.md`**: four more, closed
on 2026-10-05 — plus **where the presentation slot decides the pairwise answers,
in `PLAN_PRIMACY.md`**: three more, closed the same day — plus **what the
proposer says it is doing, against what it does, in `PLAN_WHY.md`**: five more,
closed the same day too — plus **the second way's third form, declaration
imposed at write time, in `PLAN_AUTHORSHIP.md`**: five more, closed on
2026-10-06 — plus **that form asked again, with the proposer told to overlap,
in `PLAN_OVERLAP.md`**: four more, closed on 2026-10-07 — plus **declaration
beyond the security keyword, with the rule drafted blind, in `PLAN_BLIND.md`**:
six more, closed on 2026-10-12 — plus **what the screen of compiled rules does to
the model, in `PLAN_SCREEN.md`**: five more, closed on 2026-10-15 — plus **how
much of the residue under rung 3's coverage bound is slack, in
`PLAN_BOUND.md`**: five more, closed on 2026-10-17 — plus **the ranking of the
queues, asked of the model, in `PLAN_RANKING.md`**: six more, closed the same
day — plus **what the proposer's rules buy over a learner fitted to its
answers, in `PLAN_STUDENTS.md`**: six more, closed on 2026-10-18 — plus **what
a reviewer's labels at the escalations buy the order, in
`PLAN_ESCALATIONS.md`**: six more, closed on 2026-10-19 — plus **what a random
audit of the system's decisions buys beside the escalations, in
`PLAN_SPOTCHECK.md`**: six more, closed the same day — plus **what the rules no
label reaches hold, in `PLAN_UNREACHED.md`**: six more, closed on 2026-10-20 —
plus **the policy, given to the proposer at three levels, in `PLAN_MANUAL.md`**:
seven more, closed on 2026-10-21.

**In one sentence.** The priority of a stratified policy is not in the shape of
its rules; of the three ways of supplying it — infer it from the syntax, have the
proposer declare it, learn it from observed behaviour — the first is falsified,
the second has been tried in three forms and supplied almost none of it, and the
third recovers 61% of what full supervision buys, on corpus test.

> **[ERRATUM 2026-09-28] The second clause had been stale since the pairwise
> threads closed, and it is this file's headline.** It read *the second was never
> exercised*, which was true when it was written on 2026-08-09 (`8487a63`): rung 2
> gave the proposer a mechanism that executes declared priority, its rules barely
> overlapped, and none of the edges it proposed was accepted. It stopped being true
> when [`PLAN_PAIRWISE.md`](PLAN_PAIRWISE.md) and
> [`PLAN_PROPOSER_1600.md`](PLAN_PROPOSER_1600.md) asked the proposer for priority
> pair by pair, at 400 and then 1,600 pairs of the learned base: it answers well at
> the pair level, and its answers, compiled on the `hibrido` pool and scored on
> corpus test split 0, at best tie a free ranking of the queues that reads no rule
> — *the answer contains almost no priority*, in the words of
> [`PAIRWISE_WRITEUP.md`](PAIRWISE_WRITEUP.md). The body below reports both
> threads; only this sentence, untouched since it was written, was never
> revisited. **What has still never been run is declaration imposed at write
> time**: Stage E, §11 of `PLAN_PAIRWISE.md`, specified and not authorised. The
> third clause now names its surface, which the erratum to §1 of
> [`FINDINGS4.md`](results4/FINDINGS4.md) fixes as corpus test; its figure did not
> move.
>
> **[NOTE 2026-10-05] The second way's first form now has its score with
> material, and the score splits by surface.** That form is declaration at write
> time, which rung 2 gave the proposer and which had no material at n=100. In
> `PLAN_REUSE.md`'s three runs at n=2000 the engine installed 50 of the edges the
> proposer declared ([`PLAN_EDGES.md`](PLAN_EDGES.md)).
>
> - **On the arrivals they supplied nothing a coin does not.** They were right
>   on a third of the cases they decided. On the cases a coin resolves, a coin
>   is right as often.
> - **Over the function, their direction points at the better rule three times
>   in four**, measured on the exhaustive space.
> - **Nearly all of them are one rule of thumb about one attribute**, the
>   security keyword, which the two surfaces weigh differently.
>
> So the second clause stands on the corpus, the surface the third clause names,
> and not on the space. Stage E is still the one form never run.
> [`results_edges/FINDINGS_EDGES.md`](results_edges/FINDINGS_EDGES.md).
>
> **[NOTE 2026-10-06] The third form has now run, and the second clause counts
> it.** The clause read *two forms* until this note, and the two notes above call
> Stage E never run, which was true when each was written. Stage E is declaration
> imposed at write time, run as [`PLAN_AUTHORSHIP.md`](PLAN_AUTHORSHIP.md): a rule
> that overlapped another was refused until the proposer declared it an exception
> to it or a default under it.
>
> - **The proposer met the requirement by overlapping less.** Most of the rules
>   it wrote overlap no rule written before them, and no CONFLICT arose in three
>   runs of 2,000 arrivals.
> - **On the corpus that left the order almost nothing to do.** Its room was 15
>   and 47 arrivals of 2,000 in two runs, and none in the third.
> - **Over the space the row is unadjudicable.** The run with no room makes the
>   median undefined, as the scorer reads it. In the other two runs the edges
>   filled all of the room and 58% of it.
> - **The bases came out no sounder.** On the corpus, subsumption over them is
>   wrong more often than over v1's.
>
> So the clause holds on the corpus for the third form too, and over the space
> the third form has no verdict.
> [`results_authorship/FINDINGS_AUTHORSHIP.md`](results_authorship/FINDINGS_AUTHORSHIP.md).
>
> **[NOTE 2026-10-07] Over the space the third form has a verdict now, and it is
> the first form's.** [`PLAN_OVERLAP.md`](PLAN_OVERLAP.md) asked again with the
> proposer told that overlap is normal, and asked to declare only where the
> queues differ.
>
> - **It still partitioned in two runs of three** (`O-a` refuted).
>   **[NOTE 2026-10-08]** The third run's overlap is one broad rule, read
>   POST-RUN: without it, that run partitions too.
> - **Where it left room, its declarations filled most of it over the
>   function** (`O-b` holds), and they pointed at the better rule 44 times in 47
>   (`O-c` holds).
> - **Read after the verdicts, nearly all of that is one rule of thumb**: a
>   ticket with the security keyword goes to `SECURITY_INCIDENT`, the rule
>   behind the first form's edges.
> - **On the corpus the order's room was 81 and 15 arrivals of 2,000.**
>
> So the clause stands on the corpus for all three forms. Over the space, the
> first form and the third both supply order, and both through that one rule.
> [`results_overlap/FINDINGS_OVERLAP.md`](results_overlap/FINDINGS_OVERLAP.md).
>
> **[NOTE 2026-10-12] Beyond that rule, the third form's direction is a coin's.**
> [`PLAN_BLIND.md`](PLAN_BLIND.md) took the base out of the proposer's first call,
> which is what `FINDINGS2.md` traced the partition to, and kept the declaration:
> a placement round asked for the same rule, placed against every rule of another
> queue it overlaps. Every row is read where the security keyword is absent.
>
> - **Drafted blind, the proposer crossed** (`K-a` holds).
> - **There, its declarations point at the better rule about one time in two**
>   (`K-b` refuted), **and a fixed ranking of the queues points the same pairs
>   better** (`K-c` refuted). On the arrivals it is the same (`K-e` refuted).
> - **The edges fill most of the order's room over the function** (`K-d` holds),
>   **and read POST-RUN that is mostly resolution**: the same edges pointed by
>   the ranking fill more in every run.
>
> So over the space the order the second way supplies goes through the keyword's
> one rule. Beyond it the declarations resolve conflicts, and point them the way
> a coin would wherever a ranking would not already answer.
> [`results_blind/FINDINGS_BLIND.md`](results_blind/FINDINGS_BLIND.md).
>
> **[NOTE 2026-10-18] The ranking that pointed those pairs better read a key.**
> [`PLAN_RANKING.md`](PLAN_RANKING.md) asked the model for its own ranking of the
> queues and put that ranking in the key's place. On `K-b`'s pairs the median
> stated ranking reads 0.5496 against the declarations' 0.5460: no worse than
> them, by a hair (`M-e` holds, thin). On the arrivals it reads below them,
> which is reported. So *a ranking would already answer* holds for a ranking
> fitted with a key, and only just for one the model states.
> [`results_ranking/FINDINGS_RANKING.md`](results_ranking/FINDINGS_RANKING.md).
>
> **[NOTE 2026-10-18, later] Nor do the proposer's own answers supply it.**
> [`PLAN_STUDENTS.md`](PLAN_STUDENTS.md) handed rung 3's search the queues the
> proposer named at 286 escalations, where the search had had the truth.
> Ordered by them, rung 1's rules are right on 483 cases of corpus test split 0,
> below the 519 of the order they were born in (`T-d` refuted). Handed the truth
> of the same 286 tickets, the search reaches 814. So the order rung 3 finds is
> in the truth of its labels, not in their number, and the proposer's answers
> carry none of it.
> [`results_students/FINDINGS_STUDENTS.md`](results_students/FINDINGS_STUDENTS.md).
>
> **[NOTE 2026-10-19] The third way can be bought where the loop asks, on the
> corpus.** [`PLAN_ESCALATIONS.md`](PLAN_ESCALATIONS.md) handed rung 3's search
> the truth of rung 1's train-half escalations, as a reviewer would supply it,
> at the audit's label budgets.
>
> - **Fifty escalations drawn at random order the rules to 737 of 995 cases of
>   corpus test split 0**, at the median: two thirds of what full supervision
>   gains over arrival order (`J-a` holds).
> - **Fifty random train cases give 717** (`J-b` holds, thin).
> - **Over the space the escalations buy less at every budget** (`J-e` holds).
> - **Labelling the most crowded first buys almost nothing on the arrivals**
>   (`J-d` refuted).
>
> So a reviewer at the escalations buys the order about as well as one of random
> tickets where tickets arrive, and less of it over the function.
> [`results_escalations/FINDINGS_ESCALATIONS.md`](results_escalations/FINDINGS_ESCALATIONS.md).
>
> **[NOTE 2026-10-19, later] A small random audit of the decisions adds little to
> it.** [`PLAN_SPOTCHECK.md`](PLAN_SPOTCHECK.md) labelled every escalation and a
> random draw of the cases rung 1's engine decided itself.
>
> - **Fifty audited decisions add four cases** of corpus test split 0 to the
>   escalations' 814 (`N-a` holds, thin), not half of the 29 that separate them
>   from full supervision (`N-b` refuted).
> - **251 add 19** (`N-e` holds, thin), nearly all of them in the one queue the
>   escalations never teach, `T3_ENGINEERING`, which an order learns all at
>   once or not at all (`N-c` refuted, thin).
> - **Over the space the audited sets fall below the escalations alone**
>   (`N-d` refuted, thin).
>
> So what the escalations leave takes a large audit to buy: half of it lies
> between 100 and 251 audited decisions, at the medians.
> [`results_spotcheck/FINDINGS_SPOTCHECK.md`](results_spotcheck/FINDINGS_SPOTCHECK.md).
>
> **[NOTE 2026-10-20] And it is not in the rules the escalations never reach,
> beyond one.** [`PLAN_UNREACHED.md`](PLAN_UNREACHED.md) moved the 25 rules no
> escalation matches, which the search leaves where its start put them.
>
> - **On corpus test split 0 only `R0545`, the rule `T3_ENGINEERING` turns on,
>   pays at the front.** None of the other 21 distinct rules gains away from
>   the ticket it was written at (`Z-a`, `Z-b` refuted).
> - **None of the 25 decides a test case in the escalations' order**, so
>   deferring them all, which reads no truth, leaves it at 814 (`Z-d` refuted,
>   thin).
> - **Over the space the stake is one rule**, *keyword and severity 1* to
>   `SECURITY_INCIDENT` (`Z-c` holds). Deferring the 25 gains no more than a
>   reshuffle of them does (`Z-e` holds, thin).
>
> So beyond `R0545`, what the escalations leave on the arrivals is not in the
> rules they never reach, and over the function those rules hold one rule's
> worth. [`results_unreached/FINDINGS_UNREACHED.md`](results_unreached/FINDINGS_UNREACHED.md).
>
> **[NOTE 2026-10-21] Authority, the channel none of the three ways tried,
> supplies the priority in one shape and not in the other.**
> [`PLAN_MANUAL.md`](PLAN_MANUAL.md) gave the model the policy itself: a
> catalogue of the queues, a prose manual with a real manual's vague words, and
> the 29 rules as text.
>
> - **Compiled in one answer, the model writes the policy**: the rules exactly,
>   every time (`G-a` holds), and the prose to 0.9929 of the space.
> - **Through the impasse loop, the same texts give bases that decide about a
>   third of the space**: with the rules, 0.3778 against the 1.0000 of
>   compiling them once (`G-d` holds).
> - **With the rules in front of it, the proposer still partitions** (`G-c`
>   holds).
>
> So the priority can be supplied whole by authority, compiled once, and the
> loop does not turn the same manual into it.
> [`results_manual/FINDINGS_MANUAL.md`](results_manual/FINDINGS_MANUAL.md).

---

## Before reading any figure

**Every figure names a surface, and the two are not interchangeable.** The
**corpus** is the modelled arrival distribution, deliberately long-tailed
(`has_security_keyword`: 3% of arrivals against 50% of the attribute space). The
**exhaustive space** is the uniform measure over all 134,400 combinations. The
corpus answers *what would this achieve in deployment* and cannot certify an
optimum — its 2000 draws touch 1743 distinct cases and leave the rest
unconstrained, so an order can be perfect on it and be 0.9455 as a function. The
space answers *is this order the policy*, and weights regions the system will
almost never see. Neither is *the* bound. Rungs 1 to 4 published corpus figures
without saying so; everything below is labelled.

**The sharpest instance measured, 2026-08-15**: two end orders of the same search
disagree on 20.35% of the space and 5.75% of the corpus, and the class carrying
most of that disagreement is not the same class on the two surfaces — 57.5% of it
against 4.6%. Per-class rates do not transfer either, so a figure on one surface
cannot be reweighted into a figure on the other. **Nor does the ordering**: over
the same 2,080 pairs the two surfaces correlate at a Spearman of 0.34, so the
space cannot rank two orders for deployment any more than it can rate them
([`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md), parts two and
three). Name the surface.

**Every finding came from a check costing cents or nothing**, never from the
expensive run. Three failures were caught by a blocking free check, each of which
changed a conclusion:

- **Aug 5** · `harness.ceiling_check`: the engine scores 0.5875 with the
  *perfect* policy loaded. It voided an n=2000 run already paid for
  ([`PREDICTION.md`](PREDICTION.md)).
- **Aug 8** · `rung3.optimizer_check`: the neighbourhood the audit had
  declared, pairwise swaps, cannot solve the 29-rule instance whose optimum is
  1.0000 — 0 of 65 starts reach it.
- **Aug 8** · the same check, on the other surface: the corpus would have
  certified that instrument anyway — orders perfect on its 2000 cases score
  0.9455 and 0.9299 as functions
  ([`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md), Step 0).

Money bought only rung 1's 577 rules and rung 2's eight runs. Rungs 3 and 4 and
the audit cost zero API calls.

---

## The signed rows, and how they came out

**One hundred and twenty-six rows have been signed before the figures they name existed. This
is their scoreboard**, and it is a fact about the drafter rather than about the
material. It exists because the standing calibration note in
[`IDEAS.md`](IDEAS.md) is *directional* — it tells whoever writes the next entry
which way their bands usually err — and a note like that is worth nothing without
a count behind it.

**The convention, stated before the count so that the count can be checked.**

1. **The `Q` rows count.** They live in §0 of `PLAN_ORDER_METRICS.md` instead of
   `IDEAS.md`, and the regime is the same: drafted by Claude on 2026-08-14 and
   signed by Sergi the same day — *I adopt §0 as drafted, without changes* — where
   the signing commit adds only that line and a pointer in §4, so no row of the
   table moved. Same drafter, same shape of band with its own *refuted by* column,
   same "committed before any figure exists".
2. **Rows marked *reported, not adjudicated* are listed apart and are not in the
   denominator.** There was no band to hit or miss, so they are not calibration
   events — but they are signed rows and they are a fact about the drafter, so
   they are counted separately rather than dropped.
3. **One signed row is one event, with the verdict its own record gives it.**
   `S-d` is one refutation and not two, though the record publishes two readings
   of it; `Q-d` is one though only its second half failed. Splitting rows by
   clause would make the denominator depend on drafting style, and hand the next
   drafter an incentive to write fewer clauses to protect the ratio.

| thread | signed | adjudicated | refuted | dead zone | hold | reported |
|---|---|---|---|---|---|---|
| **Q** · the instrument (§0 of `PLAN_ORDER_METRICS.md`) | 6 | 6 | **2** | 0 | 4 | 0 |
| **S** · the corpus surface | 6 | 6 | **4** | 0 | 2 | 0 |
| **R** · rank transfer | 4 | 3 | **1** | 1 | 1 | 1 |
| **C** · the touched points | 4 | 3 | **0** | 1 | 2 | 1 |
| **D** · the rule level | 4 | 3 | **2** | 0 | 1 | 1 |
| **P** · pairwise judgement (§0 of `PLAN_PAIRWISE.md`) | 3 | 3 | **2** | 0 | 1 | 0 |
| **B** · the proposer at 1,600 (§0 of `PLAN_PROPOSER_1600.md`) | 4 | 4 | **2** | 0 | 2 | 0 |
| **A** · the sensitivity sweep (§0 of `PLAN_SENSITIVITY.md`) | 5 | 5 | **2** | 0 | 3 | 0 |
| **I** · ILP as a competitor (§0 of `PLAN_ILP.md`) | 4 | 3 | **2** | 0 | 1 | 0 |
| **U** · the founding question (§0 of `PLAN_REUSE.md`) | 6 | 5 | **1** | 0 | 4 | 1 |
| **F** · fidelity (§0 of `PLAN_FIDELITY.md`) | 6 | 5 | **1** | 0 | 4 | 1 |
| **W** · declared edges (§0 of `PLAN_EDGES.md`) | 4 | 3 | **2** | 0 | 1 | 1 |
| **L** · the slot listed first (§0 of `PLAN_PRIMACY.md`) | 3 | 2 | **1** | 0 | 1 | 1 |
| **Y** · the why texts (§0 of `PLAN_WHY.md`) — *bands set on a development set* | 5 | 4 | **0** | 0 | 4 | 1 |
| **E** · declaration imposed (§0 of `PLAN_AUTHORSHIP.md`) | 5 | 3 | **2** | 0 | 1 | 1 |
| **O** · imposed, with overlap asked for (§0 of `PLAN_OVERLAP.md`) | 4 | 3 | **1** | 0 | 2 | 1 |
| **K** · beyond the keyword, drafted blind (§0 of `PLAN_BLIND.md`) | 6 | 5 | **3** | 0 | 2 | 1 |
| **V** · the screen (§0 of `PLAN_SCREEN.md`) — *three bands set on a development set* | 5 | 4 | **1** | 0 | 3 | 1 |
| **H** · the bound (§0 of `PLAN_BOUND.md`) | 5 | 4 | **1** | 0 | 3 | 1 |
| **M** · the ranking, asked of the model (§0 of `PLAN_RANKING.md`) | 6 | 5 | **3** | 0 | 2 | 1 |
| **T** · the students (§0 of `PLAN_STUDENTS.md`) | 6 | 5 | **2** | 0 | 3 | 1 |
| **J** · the escalations (§0 of `PLAN_ESCALATIONS.md`) | 6 | 5 | **1** | 0 | 4 | 1 |
| **N** · the audit of decisions (§0 of `PLAN_SPOTCHECK.md`) | 6 | 5 | **3** | 0 | 2 | 1 |
| **Z** · the rules no label reaches (§0 of `PLAN_UNREACHED.md`) | 6 | 5 | **3** | 0 | 2 | 1 |
| **G** · the policy, given to the proposer (§0 of `PLAN_MANUAL.md`) | 7 | 6 | **3** | 0 | 3 | 1 |
| **total** | **126** | **105** | **45** | **2** | **58** | **19** |

**Named, so that the table can be recomputed by hand.** Refuted: `Q-d`, `Q-f`,
`S-a`, `S-b`, `S-c`, `S-d`, `R-a`, `D-a`, `D-c`, `P-d`, `P-e`, `B-b`, `B-c`,
`A-a`, `A-b`, `I-a`, `I-c`, `U-d`, `F-c`, `W-b`, `W-c`, `L-a`, `E-a`, `E-b`,
`O-a`, `K-b`, `K-c`, `K-e`, `V-a`, `H-d`, `M-b`, `M-c`, `M-d`, `T-d`, `T-e`, `J-d`, `N-b`,
`N-c`, `N-d`, `Z-a`, `Z-b`, `Z-d`, `G-b`, `G-e`, `G-f`.
Hold: `Q-a`, `Q-b`, `Q-c`, `Q-e`, `S-e`, `S-f`,
`R-c`, `C-b`, `C-c`, `D-b`, `P-c`, `B-a`, `B-d`, `A-c`, `A-d`, `A-e`, `I-d`,
`U-a`, `U-b`, `U-c`, `U-e`, `F-a`, `F-b`, `F-d`, `F-e`, `W-a`, `L-b`, `Y-a`,
`Y-b`, `Y-c`, `Y-d`, `E-d`, `O-b`, `O-c`, `K-a`, `K-d`, `V-b`, `V-c`, `V-d`,
`H-a`, `H-b`, `H-c`, `M-a`, `M-e`, `T-a`, `T-b`, `T-c`, `J-a`, `J-b`, `J-c`,
`J-e`, `N-a`, `N-e`, `Z-c`, `Z-e`, `G-a`, `G-c`, `G-d`.
Reported: `R-d`, `C-d`, `D-d`, `U-f`, `F-f`, `W-d`, `L-c`, `Y-e`, `E-e`, `O-d`,
`K-f`, `V-e`, `H-e`, `M-f`, `T-f`, `J-f`, `N-f`, `Z-f`, `G-g`.

**`I-b` is signed and NOT adjudicated, and it is the first of its kind.** It holds
at one declared beam width and is refuted at the other, so `I-g4` refuses it a
verdict rather than letting the favourable beam pick one. It is in the *signed*
column and out of the *adjudicated* one.
**`E-c` is the second, for another reason.** One run of three left the order no
room, so that run's share is undefined. §0 makes the row unadjudicable if the
median is undefined, and `authorship/score.py`, merged before the signature,
reads a median over such a run as undefined. **Under any other reading of that
median the row would hold**, because the other two runs are above its line. It
is in the *signed* column and out of the *adjudicated* one, beside `I-b`.
**Dead zone: `R-b` and `C-a`** — a row landing between its band and its
refutation line, which is a drafting defect and not a result. **`D` has none**,
because after those two the D entry declared every band's edges to be its own
refutation lines.

**Why the per-thread column and not a single ratio.** The calibration note is
about direction, and one ratio destroys it: `S` at 4 of 6 and `C` at 0 of 3 are
not the same drafting behaviour, and the thread that bet on arrivals *differing*
from the space is the one that stopped being refuted.

**The convention chosen is the milder of the two available, and that is declared
here rather than left to be found later.** With the `Q` rows, 45 of 105 = **42.9%**
refuted; without them, 43 of 99 = **43.4%**. `Q` is in because of the common
drafter and the sample size, not because of the figure — and it moves the figure
0.5 points the flattering way, which is exactly why saying so is not optional.
**The `Y` rows, and three of the `V` rows, flatter it more, and for a reason of
design.** Their bands were set on a development set: the `Y` rows' on the same
model a day earlier, and those of `V-b` to `V-d` on a pilot of 300 decisions the
drafter had read. So they bet that a reading generalises rather than test the
drafter's foresight. Without them the two ratios are 45 of 98 = **45.9%** and 43
of 92 = **46.7%**, which is the reading the calibration note should take.

> **[ERRATUM 2026-08-29] That paragraph had been stale since the `B` thread
> landed, and this file is where it should have been caught.** It read *11 of 24 =
> 45.8%* and *9 of 18 = 50.0%*, which were the counts before `PLAN_PROPOSER_1600`
> added four rows and two refutations; the table three paragraphs above had moved
> and the ratio below it had not. It is exactly the failure this repository
> legislates against everywhere else — a number copied where no test can reach it,
> going stale in silence — committed inside the section whose whole subject is
> keeping a count honest. The figures above are recomputed with `A` included and
> the arithmetic is the same convention, unchanged.
>
> **[NOTE 2026-09-30] Recomputed with the `U` thread, in the same commit as its
> row.** Six rows were signed, five adjudicated, one refuted and one reported. The
> table, the named lists, the count of signed rows in the heading and the two
> ratios above moved together, so this time nothing was left behind.
>
> **[NOTE 2026-10-04] Recomputed with the `F` thread, in the same commit as its
> row.** Six rows were signed, five adjudicated, one refuted and one reported. The
> table, the named lists, the count of signed rows in the heading and the two
> ratios above moved together again.
>
> **[NOTE 2026-10-05] Recomputed with the `W` thread, in the same commit as its
> row.** Four rows were signed, three adjudicated, two refuted and one reported.
> The table, the named lists, the count in the heading, the two ratios and the
> gap between them, now 1.3 points, moved together.
>
> **[NOTE 2026-10-05, later the same day] Recomputed with the `L` thread, in the
> same commit as its row.** Three rows were signed, two adjudicated, one refuted
> and one reported. The table, the named lists, the count in the heading and the
> two ratios moved together; the gap between them is still 1.3 points.
>
> **[NOTE 2026-10-05, later still] Recomputed with the `Y` thread, in the same
> commit as its row.** Five rows were signed, four adjudicated, all four held,
> and one reported. The table, the named lists, the count in the heading and the
> two ratios moved together; the gap between them is now 0.8 points. The ratios
> without the `Y` rows are given beside them, for the reason the paragraph above
> says.
>
> **[NOTE 2026-10-06] Recomputed with the `E` thread, in the same commit as its
> row.** Five rows were signed and three adjudicated: two refuted and one held.
> One was reported, and one is signed and not adjudicated, like `I-b`. The table,
> the named lists, the count in the heading, the two ratios and the two without
> the `Y` rows moved together; the gap between the first two is now 0.9 points.
>
> **[NOTE 2026-10-07] Recomputed with the `O` thread, in the same commit as its
> row.** Four rows were signed and three adjudicated: one refuted and two held.
> One was reported. The table, the named lists, the count in the heading, the two
> ratios and the two without the `Y` rows moved together; the gap between the
> first two is now 0.8 points.
>
> **[NOTE 2026-10-12] Recomputed with the `K` thread, in the same commit as its
> row.** Six rows were signed and five adjudicated: three refuted and two held.
> One was reported. The table, the named lists, the count in the heading, the two
> ratios and the two without the `Y` rows moved together; the gap between the
> first two is now 0.9 points.
>
> **[NOTE 2026-10-15] Recomputed with the `V` thread, in the same commit as its
> row.** Five rows were signed and four adjudicated: one refuted and three held.
> One was reported. Three of the four bands were set on a development set, so
> the two ratios without such rows now leave out `V-b`, `V-c` and `V-d` beside
> the `Y` rows. The table, the named lists, the count in the heading and the four
> ratios moved together; the gap between the first two is now 0.8 points.
>
> **[NOTE 2026-10-17] Recomputed with the `H` thread, in the same commit as its
> row.** Five rows were signed and four adjudicated: one refuted and three held.
> One was reported. None of its bands was set on a development set. The table,
> the named lists, the count in the heading and the four ratios moved together;
> the gap between the first two is now 0.7 points.
>
> **[NOTE 2026-10-18] Recomputed with the `M` thread, in the same commit as its
> row.** Six rows were signed and five adjudicated: three refuted and two held.
> One was reported. None of its bands was set on a development set. The table,
> the named lists, the count in the heading and the four ratios moved together;
> the gap between the first two is still 0.7 points.
>
> **[NOTE 2026-10-18, later] Recomputed with the `T` thread, in the same commit
> as its row.** Six rows were signed and five adjudicated: two refuted and three
> held. One was reported. None of its bands was set on a development set. The
> table, the named lists, the count in the heading and the four ratios moved
> together; the gap between the first two is now 0.6 points.
>
> **[NOTE 2026-10-19] Recomputed with the `J` thread, in the same commit as its
> row.** Six rows were signed and five adjudicated: one refuted and four held.
> One was reported. None of its bands was set on a development set. The table,
> the named lists, the count in the heading and the four ratios moved together;
> the gap between the first two is still 0.6 points.
>
> **[NOTE 2026-10-19, later] Recomputed with the `N` thread, in the same commit as
> its row.** Six rows were signed and five adjudicated: three refuted and two
> held. One was reported. None of its bands was set on a development set. The
> table, the named lists, the count in the heading and the four ratios moved
> together; the gap between the first two is now 0.5 points.
>
> **[NOTE 2026-10-20] Recomputed with the `Z` thread, in the same commit as its
> row.** Six rows were signed and five adjudicated: three refuted and two held.
> One was reported. None of its bands was set on a development set. The table,
> the named lists, the count in the heading and the four ratios moved together;
> the gap between the first two is now 0.6 points.
>
> **[NOTE 2026-10-21] A test reaches this paragraph now.** The erratum above
> called it *a number copied where no test can reach it*.
> [`tests/test_prose_tables.py`](tests/test_prose_tables.py) recomputes the
> table's total row, the count in the heading, the named lists and the four
> ratios. It also reads every named row's verdict in the JSON record that owns
> it, dead-zone and unadjudicated rows included. The next thread still moves
> them all by hand, in the same commit as its row, and the test fails until they
> agree with each other and with the records.
>
> **[NOTE 2026-10-21, later] Recomputed with the `G` thread, in the same commit
> as its row.** Seven rows were signed and six adjudicated: three refuted and
> three held. One was reported. None of its bands was set on a development set.
> The table, the named lists, the count in the heading and the four ratios moved
> together, and the test above read them; the gap between the first two is now
> 0.5 points.

**Where the verdicts are read from.** The `Q` column comes from *the predictions
of §0, one by one* in the first part of
[`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md) — its register table
carries `G1`–`G6` instead — and `S`, `R`, `C` and `D` from the registers of parts
two, three, four and five of the same record; and `P` from the Stage C and
Stage D sections of [`results2/FINDINGS2.md`](results2/FINDINGS2.md) and §8 of
[`results3/FINDINGS3.md`](results3/FINDINGS3.md). All three `P` rows are
adjudicated: the thread is closed. `A` comes from
[`results_sensitivity/FINDINGS_SENSITIVITY.md`](results_sensitivity/FINDINGS_SENSITIVITY.md),
which owns all five; `I` from [`results_ilp/FINDINGS_ILP.md`](results_ilp/FINDINGS_ILP.md);
and `U` from the Stage C section of
[`results_reuse/FINDINGS_REUSE.md`](results_reuse/FINDINGS_REUSE.md), with `U-f`
from its Stage A; and `F` from the Stage C section of
[`results_fidelity/FINDINGS_FIDELITY.md`](results_fidelity/FINDINGS_FIDELITY.md),
with `F-f` from its Stages A and C; and `W` from
[`results_edges/FINDINGS_EDGES.md`](results_edges/FINDINGS_EDGES.md), which owns
all four; and `L` from
[`results_primacy/FINDINGS_PRIMACY.md`](results_primacy/FINDINGS_PRIMACY.md),
which owns all three; and `Y` from
[`results_why/FINDINGS_WHY.md`](results_why/FINDINGS_WHY.md), which owns all
five; and `E` from
[`results_authorship/FINDINGS_AUTHORSHIP.md`](results_authorship/FINDINGS_AUTHORSHIP.md),
which owns all five; and `O` from
[`results_overlap/FINDINGS_OVERLAP.md`](results_overlap/FINDINGS_OVERLAP.md),
which owns all four; and `K` from
[`results_blind/FINDINGS_BLIND.md`](results_blind/FINDINGS_BLIND.md), which owns
all six; and `V` from the Stage C section of
[`results_screen/FINDINGS_SCREEN.md`](results_screen/FINDINGS_SCREEN.md), with
`V-e` from its Stages A and C; and `H` from
[`results_bound/FINDINGS_BOUND.md`](results_bound/FINDINGS_BOUND.md), which owns
all five; and `M` from
[`results_ranking/FINDINGS_RANKING.md`](results_ranking/FINDINGS_RANKING.md),
which owns all six; and `T` from
[`results_students/FINDINGS_STUDENTS.md`](results_students/FINDINGS_STUDENTS.md),
which owns all six; and `J` from
[`results_escalations/FINDINGS_ESCALATIONS.md`](results_escalations/FINDINGS_ESCALATIONS.md),
which owns all six; and `N` from
[`results_spotcheck/FINDINGS_SPOTCHECK.md`](results_spotcheck/FINDINGS_SPOTCHECK.md),
which owns all six; and `Z` from
[`results_unreached/FINDINGS_UNREACHED.md`](results_unreached/FINDINGS_UNREACHED.md),
which owns all six; and `G` from
[`results_manual/FINDINGS_MANUAL.md`](results_manual/FINDINGS_MANUAL.md), which
owns all seven.

> **[ERRATUM 2026-10-21] This paragraph stopped at `V`.** The six threads that
> closed after it, from `H` on 2026-10-17 to `Z` on 2026-10-20, each moved the
> table and the named lists, and none extended this list. It was found while
> writing [`tests/test_prose_tables.py`](tests/test_prose_tables.py), whose
> `THREADS` names the record behind each thread's verdicts and fails when a
> thread on the table has none. No verdict moves.

**Excluded, and this is what makes
the arithmetic reproducible:** `G1`–`G6`, which are the plan's checks and carry no
band; and `S-g`, `C-e` and `D-e`, which the records add as *(not predicted)* and
which nobody signed. **And `P-a` and `P-b` of `PLAN_PAIRWISE.md`, which are
neither**: they were measured on 2026-08-24 *before* anyone signed them, so they
are **spent** — not signed and not adjudicable, in no column of the table and not
in the denominator. §0.1 of that plan records them as outcomes and does not
restore them as predictions. `P-c`, `P-d` and `P-e` are a different case: Sergi
signed them on 2026-08-24, before any figure of theirs existed, and they are in
the table above.

**The `B` rows are the thread's first pre-registered ones.** Sergi signed §0 of
`PLAN_PROPOSER_1600.md` on 2026-08-25, in its own commit and before a single one
of the 1,200 calls was made — `gate_signature` refuses to run the stage otherwise.
§9 and §10 of [`FINDINGS3.md`](results3/FINDINGS3.md) are labelled POST-RUN and
are not calibration events; §11 is, and it is the first in the pairwise thread
that could have surprised its author.

**`B-b` is refuted by 0.0020 and that is not a defeat.** The compiled order scores
0.4804 on `hibrido` / corpus test split 0 against a free queue ranking's 0.4824,
where a coin on direction over the same sample has sd 0.0319. The band's edge is
its own refutation line, so the verdict stands as signed; the reading beside it is
that **1,200 calls bought an order indistinguishable from a baseline that reads no
rule.** `B-c` is refuted by −0.74 of the projection's own deviations, which §8 of
the plan asked to be distinguished from a three-deviation miss.

**`B-d` is the mechanism, and it is why the other two land where they do.** The
proposer's direction rate is **0.8647** on the pairs a queue ranking can already
answer and **0.6391** on the ones it cannot (n 451 and 654; 0.9181 against 0.5813
over the corpus surface). Its accurate part is redundant with a free baseline and
its errors concentrate exactly where that baseline is silent. **`B-a` holds**: the
rate is 0.7312 at 1,600 against 0.6978 at 400, so the instrument did not move —
whatever went wrong, it was not that.

**Both threads are written up as one result** in
[`PAIRWISE_WRITEUP.md`](PAIRWISE_WRITEUP.md), which owns no figure and adds no
measurement: the pair-level rate and the order-level score as a single claim, the
free queue-ranking baseline that makes the second readable, and the four
candidates — budget, compilation, selection, instrument — each ruled out by a free
measurement.

**The drafter predicted three of the four**, expecting `B-b` to hold. That
expectation is in §0 of the plan, was written before the calls, and is a fact
about the drafter in the same way the table above is.

**The `A` rows are the first pre-registered work outside the pairwise threads, and
two of the five bands are the signer's.** Sergi signed §0 of `PLAN_SENSITIVITY.md`
on 2026-08-29 before a single policy was drawn, tightening `A-b` from 0.80 to 0.85
and `A-d` from 0.50 to 0.60 at signature time; a gate refuses to write the record
otherwise. A hold or a miss on those two is weaker evidence about the drafter's
calibration than the other three, and that is recorded in the plan beside the
table rather than left to be inferred.

**`A-a` is refuted upward, and that is the sweep's finding.** The drafter
predicted the refutation and gave the wrong reason — it expected the hidden policy
to score **below** its family at its own ρ and it scores **above**, rank 100 of
101 on the space and **101 of 101 on the corpus**. Four of five verdicts came out
as drafted; the one it got right, it got right for the wrong reason. **`A-b` is
the miss**, and it misses at −0.9945 against a band of ≥ 0.85: the curve is about
as real as a curve gets and the drafter had the sign of ρ backwards.

**The `U` rows ask the question the project was built for, and the drafter got
three of five.** Sergi signed §0 of `PLAN_REUSE.md` on 2026-09-29, before any of
its figures existed. He signed an amendment to §1 on 2026-09-30, before any full
run: the proposer's calls do not reason. A gate refuses every writer of the plan
otherwise. The drafter expected `U-a` to `U-d` to hold and `U-e` to be refuted;
**`U-d` was refuted and `U-e` held.** Two of the holds sit on their lines —
`U-c` at 0.6024 against 0.60 and `U-b` at +0.0207 against 0 — and each has one run
of three on the wrong side. `U-f` is reported: its inputs had been on disk since
August, and the drafter had read their metrics.

**The `F` rows ask the founding question in its cleanest form, and the drafter
got four of five.** Sergi signed §0 of `PLAN_FIDELITY.md` on 2026-10-02, before
any of its figures existed. A gate refuses every writer of the plan otherwise.
The drafter expected all five to hold, and named the ones it trusted least:
`F-d`, then `F-e`, then `F-c`. **`F-c` was refuted, and thinly**: −0.0126 on the
median against a line of 0, inside one standard error, the label §0 fixed in
advance. `F-d` held at 0.7955, well above the line the drafter expected it to
sit on. `F-a` was read once, provisionally, before any base session ran, as §8
of the plan intends, and the record says so. `F-f` is reported.

**The `W` rows ask what declared priority bought once it had material, and the
drafter got one of three.** Sergi signed §0 of `PLAN_EDGES.md` on 2026-10-05,
before any of its figures existed. Nothing in it costs a call, and a gate refuses
its writers otherwise. The drafter expected all three to hold, and trusted `W-b`
least, then `W-c`. **Both were refuted.**

- **`W-b` was refuted upward.** Over the function the declared direction is
  right more often than the pairwise question's, not less.
- **`W-c` was refuted by resolution, not accuracy.** The record names that as a
  defect of the statistic, not a reprieve, and the verdict stands as signed.

`W-a` held. `W-d` is reported.

**The `L` rows ask where the presentation slot decides, and the drafter got one
of two.** Sergi signed §0 of `PLAN_PRIMACY.md` on 2026-10-05, before any of its
figures existed. Nothing in it costs a call, and a gate refuses its writer
otherwise. The drafter expected both rows to hold, and trusted `L-a` least.
**`L-a` was refuted, thinly**: on the queue pair the proposer splits evenly, the
slot effect is +0.1236 against a line of 0.20, inside one standard error. `L-b`
held. `L-c` is reported.

**The `Y` rows ask what the proposer says it is doing, and all four held — as
rows set on a development set were expected to.** Sergi signed §0 of
`PLAN_WHY.md` on 2026-10-05, before any held-out sentence was coded. Its codebook
was frozen on 365 development sentences, and the rows were read on the 1,114 of
the next day's batch. §0 said before the run that four holds would mean the
readings generalise and nothing about foresight, and the scoreboard above marks
the row so. `Y-e` is reported.

**The `E` rows ask whether declaration imposed at write time stratifies the base,
and the three that were read came out as the drafter expected.** Sergi signed §0
of `PLAN_AUTHORSHIP.md` on 2026-10-05, before any of its figures existed, and a
gate refuses its writers otherwise. The drafter expected `E-a` and `E-b` to be
refuted and `E-c` and `E-d` to hold, and trusted `E-c` least.

- **`E-a` and `E-b` were refuted, as expected.** They carry the claims of P3 in
  `ARBITRATION_REPORT.md` §7, which the drafter wrote down to be tested and bet
  against: two refutations the drafter predicted, not two misses.
- **`E-d` held.** `contradice_subsuncion` fired for the first time in the
  project.
- **`E-c` came out neither.** The proposer met the discipline by overlapping
  less, one run left the order no room, and the row is unadjudicable on the
  scorer's reading, as above.

`E-e` is reported.

**The `O` rows ask Stage E's question again with the proposer told to overlap,
and the drafter got two of three.** Sergi signed §0 of `PLAN_OVERLAP.md` on
2026-10-06, before any of its figures existed, and a gate refuses its writers
otherwise. The drafter expected `O-b` to hold and `O-a` and `O-c` to be refuted,
and trusted `O-a` least.

- **`O-a` was refuted and `O-b` held, as expected.** §0 had said what a run
  without room does to `O-b`, and run 3 had none: the rule decided, and the
  verdict needed no reading. That is `E-c`'s lesson, applied.
- **`O-c` held, against the drafter's expectation**, at 0.9362 against a line of
  0.70. Read after the verdicts, 43 of its 47 strict pairs are one declaration
  about the security keyword, and the record says so beside the verdict.

`O-d` is reported.

**The `K` rows ask whether declaration carries direction beyond the security
keyword, and the drafter got two of five.** Sergi signed §0 of `PLAN_BLIND.md`
on 2026-10-11, before any of its figures existed, and a gate refuses its writers
otherwise. The drafter expected `K-a`, `K-b` and `K-e` to hold and `K-c` and
`K-d` to be refuted, and trusted `K-a` least.

- **`K-a` held and `K-c` was refuted, as expected.** `K-a` read 0.2963 against a
  proxy of 0.4444, and `K-c` −0.1759: the Stage C ranking reads the same pairs
  better.
- **`K-b` and `K-e` were refuted**, at 0.5460 and 0.5861 against lines of 0.60.
  §0 had called them the comfortable rows, with lines under the pairwise
  answers' 0.6618 and 0.6455.
- **`K-d` held, against the drafter's expectation**, at 0.6061 against a line of
  0.50. Its statistic rewards resolving, and read POST-RUN most of the fill is
  resolution: a coin pointing the same edges fills 0.40 to 0.45. The record says
  so beside the verdict.

`K-f` is reported.

**The `V` rows ask what the screen of compiled rules does to the model, and the
drafter got three of four.** Sergi signed §0 of `PLAN_SCREEN.md` on 2026-10-14,
before any of its figures existed, and a gate refuses its writers otherwise.
Three of its four bands were set on a development set, the 300 decisions `F-f`
had paired, and read on decisions whose tickets nobody had asked without a
screen. The drafter expected all four to hold, and trusted `V-b` least, then
`V-a`.

- **`V-a` was refuted, thinly**: without a screen the model's answers of
  2026-10-14 agreed with those of 2026-10-03 less than with each other, +0.0615
  against a line of 0.05, inside one standard error. With a screen it held, at
  +0.0284. Its accuracy did not move, and asked under both arms on one day the
  pilot shows the same gap as across the dates.
- **`V-b`, the row it trusted least, held clear of its line**, at +0.0667 on the
  median, 3.5 standard errors above it. The pilot's median run had been +0.030.
- **`V-c` and `V-d` held**, as rows set on a development set were expected to.

`V-e` is reported.

**The `H` rows ask how much of the residue under rung 3's coverage bound is
slack, and the drafter got three of four.** Sergi signed §0 of `PLAN_BOUND.md`
on 2026-10-17, before any of its figures existed, and a gate refuses its writer
otherwise. The drafter expected all four to hold, and trusted `H-a` and `H-b`
least.

- **`H-a` and `H-b`, the rows trusted least, held clear of their lines.** A
  certificate shows 0.8602 of the space's pure residue slack and 0.7847 of its
  hybrid one, against lines of 0.50.
- **`H-c` held**: the certificate settles neither pool.
- **`H-d` was refuted**, at a median of 0.6665 over the corpus's ten train
  halves against a line of 0.75. The row bet the halves where each order was
  fitted would close more than the space, and they closed less.

`H-e` is reported.

**The `M` rows ask what the model states when asked to rank the queues, and the
drafter got four of five verdicts.** Sergi signed §0 of `PLAN_RANKING.md` on
2026-10-17, before any of its figures existed, and a gate refuses every writer
otherwise. The drafter expected three holds and two refutations, and trusted
`M-e` most and `M-d` least. Every row is read on the median of 24 valid asks.

- **`M-a` held**: every answer was a valid total order, and the presentation
  slot moved it by 0.0271 against a line of 0.05.
- **`M-b` was refuted, the one verdict the drafter missed.** The stated ranking
  scores 0.3367 on the hybrid pool at corpus test split 0, against a line of
  0.4632. §0 had warned that what the drafter had seen weakened this row.
- **`M-c` was refuted**, by 0.1457 rather than the thin margin expected.
- **`M-d` was refuted**, at −0.1724. The stated ranking predicts 935 of the
  model's 1,479 pairwise answers, and Stage C's ranking 1,190.
- **`M-e` held, thinly**, at 0.5496 against 0.5460.

`M-f` is reported.

**The only earlier mention of a count does not reconcile with any of this.** The
note inside the D entry says *two of the ten rows signed before today* landed in a
dead zone. The numerator is right and the denominator matches nothing: 20 rows
were signed before that entry and 18 of them adjudicated. It sits inside a signed
prediction block, which is not edited — not even to annotate it — so it stands as
written and this line is the reconciliation.

---

## What is established

**Priority is not recoverable from the syntactic shape of the rules.** Three
criteria falsified, perfect policy loaded, no LLM, on the corpus —
[`results/FINDINGS.md`](results/FINDINGS.md):

- *specificity*: e2e **0.5875**, CONFLICT 25.3%. No monotone function of it can
  work — H01 (2 conditions) must beat H03 (1), H16 (1) must beat H24 (2).
  **Two fifths of that conflict rate is an encoding artifact, and the rest is the
  finding.** The catch-all is `lambda c: True` and the DSL requires a condition,
  so it is written `severity gte 1` and ties instead of yielding. Give it its true
  rank — no oracle, no layer order — and **39.8%** of the corpus conflicts go,
  e2e 0.5875 → **0.6880**; on the exhaustive space **13.6%** of them, 0.2725 →
  **0.3458**. The silent-error count does not move on either surface: the artifact
  inflated abstention, never error. The gain is entirely in the two commonest
  classes and `SECURITY_INCIDENT` and `ONCALL_ESCALATION` gain nothing.
  POST-RUN, no signed row, not a calibration event —
  [`results/FINDINGS_DEFAULT_RULE.md`](results/FINDINGS_DEFAULT_RULE.md).
  **And the artifact is a constant offset across a whole family, not a distortion
  of the shape**: over 1,300 synthetic policies correcting the catch-all lifts e2e
  by 0.0122 to 0.0234 at every ρ and changes the ordering of the bins by nothing
  (`A-e`, difference 0.0000).
- *arrival order*: 100% in design order, 12.8% reversed, **49.3%** random. It
  carries no signal of its own, and in a learned base it runs backwards: defaults
  are born early, exceptions late.
- *subsumption*: silent error **0.0000** over the hand-written policy, **53.12%**
  over the learned base. A proxy for *authored* priority — the 0.0000 measures a
  virtue of the author.

**And 0.5875 is not a worst case: it is nearly the best arrangement of its own
material.** Over 100 synthetic manuals built from the hidden policy's own
conditions, condition counts, actions and layer structure, at its own ρ, it ranks
**101 of 101 on the corpus** and 100 of 101 on the space — and specificity fails
on it anyway. Across 13 values of ρ the curve is monotone at Spearman **−0.9945**,
in the direction opposite to the one the plan predicted: specificity does better
the more a manual puts its **narrow** rules first, and even its best bin medians
0.3605 on the corpus. Every one of the 100 draws at ρ = 0 contains at least one
precedence pair the condition counts violate. Five signed rows, three held —
[`results_sensitivity/FINDINGS_SENSITIVITY.md`](results_sensitivity/FINDINGS_SENSITIVITY.md).

**Execution failure, not representation failure.** Over the exhaustive space the
29 DSL rules are equivalent to their lambdas, and first-match-wins reproduces the
policy exactly.

**The mechanism for executing declared priority works, and on both surfaces.**
Subsumption plus 199 declared edges: e2e **1.0000**, silent error 0.0000, zero
conflicts, zero impasses, on the corpus **and over the 134,400 combinations** —
[`results2/FINDINGS2.md`](results2/FINDINGS2.md), *The same ceiling on the other
surface*. The space row is the one that says *policy-equivalent* rather than *fits
the sample*, and it follows from three premises the record checks and blocks on
rather than from the engine alone.

**What does not travel between the surfaces is level 1 and the price of the
edges.** Subsumption alone covers **0.6315** of the arrivals and **0.2612** of the
function, so the 199 edges buy +0.3685 on one surface and **+0.7388** on the
other; its silent error is 0.0000 on both, which upgrades rung 1's soundness
result from a corpus figure to a statement about the whole function. And **51 of
the 199 edges are never exercised by the corpus** — 12 are load-bearing on the
space and never on the corpus, 0 the other way — so an authorship cost read off
the arrivals is a floor, not the price. POST-RUN, no signed row; it closes
[`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md) §9.2.

**The proposer does not feed it.** Shown the base, the overlap arithmetic
resolved for it and an explicit instruction to overlap, it writes mostly disjoint
rules and argues disjointness as a merit. Showing it the base *reduced* overlap
tenfold (17.5% of pairs → 1.60%); the instruction recovered part of it (7.25%)
and never reached the starting point. Eight runs, ~200 escalations: **2
conflicts, 14 proposed edges, 0 accepted**. `language` appears in 0 of the 8
bases, `channel` and `prior_tickets_30d` in 1 each, though hidden layers built on
them decide 14.5% of the corpus.

**And the population for asking it the other question now exists, with its answer
key.** The 199 declared edges are published pair by pair, each with a witness
ticket drawn from the region where the two rules compete and the queue the hidden
policy sends that ticket to ([`results2/FINDINGS2.md`](results2/FINDINGS2.md),
*the labelled pair benchmark*;
[`pair_benchmark.json`](results2/pair_benchmark.json)). **170 of the 199 carry
such a witness and 29 do not** — in every one of those an earlier layer owns the
whole overlap, so the correct queue for every ticket in it is neither rule's, and
they are counted outside the denominator. That makes the 170 the easier half by
construction, and any rate measured on them an **upper** estimate of what a
proposer would do on all 199. Nothing has been asked of a model: the stage of
[`PLAN_PAIRWISE.md`](PLAN_PAIRWISE.md) that does costs money and is gated on a
row nobody has signed.

> **[ERRATUM 2026-10-04] The last sentence above went stale the afternoon it was
> written.** It reads *nothing has been asked of a model*, and says the stage that
> would ask *is gated on a row nobody has signed*. Both were true when `d280d6a`
> wrote them on 2026-08-24, and neither survived three hours: Sergi signed `P-c`,
> `P-d` and `P-e` in `681d2c9`, and Stage C asked the model 170 of these pairs,
> where `P-c` held (`fcc8b0c`). That run is reported below, under *The proposer
> can pick the right queue between two rules*, an entry `93c07d7` added a minute
> after the run without touching this one. `d280d6a` also wrote the same claim
> into the Stage B section of [`results2/FINDINGS2.md`](results2/FINDINGS2.md),
> where it says what Stage B did not do and the section after it reports Stage C;
> here it described the present. The rest of the paragraph stands, including the
> caveat that a rate on the 170 is an upper estimate for all 199, which *And it is
> an upper estimate* below carries forward. Found on 2026-10-04, reading this file
> for what is open. No figure moves.

**The material contained the signal; the arbitration destroyed it.** The same 577
rules that specificity turned into 0.1829 admit an order scoring **0.8530 ±
0.0062 on corpus test** — *the best of 65 starts, and not a converged value; see
the caveat below* — (train 0.8695: overfitting of the order is 0.0165),
against a coverage bound of 0.9010 on the corpus and 0.8784 on the space —
[`results3/FINDINGS3.md`](results3/FINDINGS3.md) §1 and its 2026-08-08 erratum,
[`order_search_ls.json`](results3/order_search_ls.json). That bound is an **upper
bound by per-case coverage**, not a demonstrated attainable optimum. The same
order scores 0.6105 on the space, and a search seeing all 134,400 cases reaches
0.7905 ([`order_search_ls_fullspace.json`](results3/order_search_ls_fullspace.json)).
The search uses the oracle: the material contains the signal, which is not the
same as it being reachable without labels.

> **[NOTE 2026-10-17] Over the space the bound is now shown out of reach, by
> most of the gap.** `PLAN_BOUND.md` certified, without a solver, cases every
> order loses. No order over the space scores above **0.8028** on the pure pool,
> so the search's 0.7905 is within **0.0123** of the best order there is; on the
> hybrid pool the figures are **0.7767** and **0.0210**. The certificate ran on
> the corpus's train halves too, not on its test halves.
> [`results_bound/FINDINGS_BOUND.md`](results_bound/FINDINGS_BOUND.md).

**The level is robust to the search budget; the order is not.** These are two
different claims and the figure invites fusing them.

*The level.* Quadrupling the multi-start budget moves the best train score by at
most one case in 1005, in 2 of the 5 splits, and in both of those the test score
falls. **The gap from 0.8530 up to the 0.9010 bound does not close by searching
harder** — more budget stops buying generalization before it stops finding train
improvements.

> **[ERRATUM 2026-10-17] Split 4 moved by three cases, not one.** Quadrupling the
> budget moved the best train score by one case in split 0, 883 to 884 of 1,005,
> and by three in split 4, 868 to 871 of 998, already at 129 starts.
> [`results3/start_budget_check.json`](results3/start_budget_check.json) and
> `FINDINGS_AUDIT.md`'s table carry both; this sentence carried only the first.
> Found on 2026-10-17, reading the searched counts for `PLAN_BOUND.md`. The
> paragraph's point stands at that size, and no other figure moves.

*The order.* In all fifteen rows measured — three budgets × five splits —
**exactly one start reaches the best train score**. In splits 1 to 3 the best did
not change between 65 and 257 starts, and yet the 192 extra draws never found it
again: the peak is a singleton that the sample spreads around rather than
concentrates on.

**So a reader of the number can rely on it, and a reader of the order inherits a
draw.** That distinction is not academic here: rung 4 consumes orders, not
scores.

**And the draw is now measured in cases, not inferred.** The end orders the
multi-start discards were regenerated — parity exact on all 31 published rows —
and compared as functions over the **exhaustive space**, pure pool
([`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md),
[`order_metrics.json`](results3/order_metrics.json)). Split 0 at full
supervision: the winner at 65 starts and the winner at 257, **one train case
apart**, decide **11,240 of 134,400 cases differently — 8.36%**; split 4, three
train cases apart, **14,430 — 10.74%**. The 65 end orders are **65 distinct
behavioural signatures**, and so are all 257: no two of them are the same
machine. Positional churn says nothing — a median 99.65% of the rules sit at a
different index between any two of them — and **Kendall tau says nothing
either**, over all pairs or restricted to the 35,457 that can change a decision
(|ρ| ≈ 0.13 both ways). What that kills is the cheap shortcut — a rank statistic
standing in for the exact comparison — and not the premise of the instrument,
which is that decisions are what have to be compared: rank failing even when
restricted is evidence for it. Disagreement concentrates on the **most abundant**
class, `SECURITY_INCIDENT` at 1.53× the overall rate, and is *below* average on
the two scarce ones, where most cases have no correct rule to compete over.

**And on the arrival distribution the same draw costs a fifth of that.** The same
orders and the same instrument, measured over the **corpus** — parity exact on
the same 31 rows ([`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md),
part two; [`order_metrics_corpus.json`](results3/order_metrics_corpus.json)). The
2,080 pairs of split 0's 65 end orders pool to **5.75% of the 2000 corpus cases**
against 20.35% of the space, and the winner at 65 against the winner at 257
differs on **33 of 2000 cases, 1.65%**, against 11,240 of 134,400. On the corpus
test half alone, 6.45% and 2.21%. **Where the disagreement falls changes
completely**: `SECURITY_INCIDENT` carries 57.5% of it on the space and **4.6%**
on the corpus, where `SELF_SERVICE_DEFLECT` carries 44.8% — although per case of
its own class `SECURITY_INCIDENT` still runs at **4.57×** the overall corpus rate
and `ONCALL_ESCALATION` at 3.32×. Per-class rates do **not** transfer between the
two surfaces (`T2_TECHNICAL` −81.6%, `BILLING_SPECIALIST` +165.2%), so no
reweighting turns one into the other. What does not change: **all 257 end orders
are still 257 distinct machines on the corpus**, the closest pair differing on 2
cases of 2000 — and not for lack of material, since the average arriving case
carries 74% more live conflicting pairs than the average point of the space.

**And the space does not even RANK what it cannot rate.** The same 2,080 pairs,
joined across the two records by `(i, j)` — no search, no regeneration, 0.07 s
([`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md), part three;
[`rank_transfer.json`](results3/rank_transfer.json)). Spearman between a pair's
**corpus** disagreement rate and its **space** rate is **0.3364**, and ties cap
it by at most 5×10⁻⁵, so that is not the explanation. Of the 208 pairs closest on
the space, **45 (21.6%)** are among the 208 closest on the corpus. The per-pair
ratio corpus/space is not one factor: **p75/p25 = 1.880**, extremes 0.047 to
1.767, a factor of **37**. And the pair the space calls the most interchangeable
of all 2,080 sits at **rank 1207 of 2080** on the corpus, above its median. So a
reader who used the space record comparatively — *this pair is further apart than
that one* — was reading the wrong surface, and not merely by a constant: the
ordering does not transfer either.

**And the whole of that shift is WHICH points arrive, not how often.** The same
2,080 pairs again, over the **exhaustive space restricted to the 1,743 points
the corpus touches** — 1.30% of it, each point counted once — with the corpus
contributing a mask and nothing else, so every rate stays in `Space`'s
convention ([`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md), part
four; [`order_metrics_touched.json`](results3/order_metrics_touched.json)).
Pooled over those touched points the pairs disagree on **5.68%**, against
**5.75%** of the 2,000 arrivals and **20.35%** of the whole space: the level
transfers to the arrival distribution *before any class weighting is applied*.
Class reweighting rebuilt on the touched rates gives **0.05828** against the
measured 0.057472, **+1.4%** relative, where the same reweighting on the whole
space gave 0.116685, **+103%** — so **98.6%** of that error is which points get
sampled and 1.4% is their multiplicity. `T2_TECHNICAL` carries 98.5% of it: two
orders disagree on **19.69%** of its 36,720 space points and **3.84%** of the
661 the corpus reaches. What this closes is the *why 3.5×* left open by part two
and the *why 0.28 and not 0.57* left open by part three, which were one question
in two units. What it does **not** do is make the space readable as a deployment
surface: the correction is a measurement over a 1.3% sample that only the corpus
can identify, not a per-class factor, so the space record plus the class
frequencies still does not reach 5.75%.

**And it is not the rules that decide which points those are.** The same 2,080
pairs again, over the **exhaustive space, pure pool**, with the touched mask
entering only through a per-rule aggregate
([`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md), part five;
[`order_metrics_rules.json`](results3/order_metrics_rules.json)). A rule's
arrival concentration — the share of the touched points its extension holds over
the share of the space it holds — spans **1,344×** across the 577, and the
predictor built from it, the mean over a pair's disagreement set of the two
winning rules' concentration, reaches a Spearman of **0.4962** against the
measured per-pair ratio and leaves **84.5%** of its spread on a log scale
(p75/p25 1.754 → 1.608). Half the ordering, almost none of the spread. What the same run
does find: a disagreement region is **0.36×** as touched as the rules that win
it, at the median — so the effect is inside a rule's extension, not between rules
— and the chain's *last* link is nearly exact, `κ` against the product of its
conditions' own concentrations giving **0.987**, with `has_security_keyword` at
50% of the space and 4.07% of the touched points. Two by-products: only **25 to
53 rules of 577** hold a territory under any of these orders, and the forbidden
per-case predictor — the arrival density of the disagreement set itself —
correlates **1.0000** with the measured ratio, which is why the run's permutation
test is blocking.

**This caveat applies equally to
[`order_search_ls.json`](results3/order_search_ls.json)**, which produced the
0.8530 with the same optimizer at the same budget, and to every rung 4 figure
from `sweep_ls`. It does not withdraw those figures — they are what the declared
instrument returns — but they are bounded by a draw, not by convergence.
`MULTISTART_STARTS` stays at 64 **because it was declared before the runs that
used it**, and for no reason found here: choosing it by reading test or space
figures would be the failure this project studies, whichever way they came out
([`start_budget_check.json`](results3/start_budget_check.json), FINDINGS_AUDIT
Step 3).

**What an order that searches for nothing scores, on both pools.** The `hibrido`
pool — subsumption plus a declared order, the machine where declared edges live —
had a world record and no floor: nothing measured what *walking* scores there. It
does now, over the full corpus, corpus test (split 0 and the five-split mean) and
the space, with both random-order generators reported separately
([`results3/FINDINGS3.md`](results3/FINDINGS3.md) §6,
[`floor_by_pool.json`](results3/floor_by_pool.json)). Three things it settles,
each naming its surface and its pool. **The hybrid floor is not the pure one
minus a constant**: it is below it on the three corpus index sets (by 0.083 to
0.088) and above it on the space (by 0.111). **`born_at` is worse than shuffling
is a pure-pool statement** — over the space it scores 0.3148 against 0.3768 and
0.3864 on `puro`, and 0.4257 against 0.3867 and 0.3903 on `hibrido`. FINDINGS3
§1's 2026-08-08 erratum holds on the pool it was measured on and the sign
reverses on the other; none of its figures moves. **And reversing `born_at` —
the label-free heuristic worth +0.2520 over the space — is worth +0.0116 on the
pool that matters for declaration.** The two
reversed figures [`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md) cited as *left
unconfirmed* reproduce exactly and now have an owning record; its §2 and its
§9.6 carry the dated erratum. This record **carries no prediction**: the two rows
that predicted it were spent before signature (`PLAN_PAIRWISE.md` §0.1).

**The proposer can pick the right queue between two rules, and most of that is a
queue hierarchy.** Asked 170 times which queue a ticket goes to when two rules
that both match it disagree — the answer known by construction from the hidden
policy's layer order — it answered correctly **150 times, 0.8824** over all 170
with `neither` counting as a failure, against floors of 0.3877 and a 0.50 coin
([`results2/FINDINGS2.md`](results2/FINDINGS2.md), Stage C;
[`pair_judgement_hidden.json`](results2/pair_judgement_hidden.json)). Position
bias is zero — 85 pairs each way, 0.8824 both — and 4 of 170 failed to parse.
**That is the signed row `P-c` holding**, at band `> 0.60`.

**But a fixed order over the eight queues, reading no rule at all, scores
0.9471** — 161 of 170, more than the model got while being shown both rules
([`pair_judgement_baselines.json`](results2/pair_judgement_baselines.json)). That
order is chosen by brute force with the key in hand over all 40,320 permutations,
so it is a winning ticket and not a level; what it bounds is that **at most 9 of
the 170 pairs require reading the rules**. Five queue-pairs appear with both
winners, which is what no ranking of queues can serve. **On those nine the model
is at 5 of 9** — a coin. So the change of question works as a format, and it has
not been shown to supply priority where a hierarchy runs out. Both hold at once
and the second is the one that transfers.

**And it is an upper estimate.** The 29 pairs with no clean witness are outside
the denominator by construction and are the ones where the layer order is
invisible on the surface of the two rules; if all of them were wrong the rate
over the 199 declared edges would be **0.7538**. The pull toward the narrower
rule shows up too: the wrong-edge rate doubles, 0.1212 against 0.0597, when the
rule that should win is the broader one.

**And a ranking of the eight queues, at zero calls, already clears the band the
next stage was going to be judged on.** A total order over the actions induces
one over the 577 rules — sort by the rank of the rule's action, reading no
condition, no extension and no subsumption. The ranking Stage C's answer key
produced over the *hidden* policy's pairs, transferred unchanged, scores
**0.4824** on the `hibrido` pool, corpus test split 0, against P-d's threshold of
0.4632; over the space, 0.5838 against 0.4557
([`results3/FINDINGS3.md`](results3/FINDINGS3.md) §7,
[`queue_hierarchy_floor.json`](results3/queue_hierarchy_floor.json)). A hierarchy
picked *blind* is worth 0.3670, below the floor — knowing which ranking to use is
the whole content of the baseline, and Stage C is where that knowledge came from.

> **[NOTE 2026-10-18] Neither ranking the model gives reaches it.** On the same
> cell the model's revealed ranking, Copeland over its 1,479 pairwise answers,
> scores 0.4693, and the ranking it states when asked scores 0.3367, below the
> blind level. Stage C's knowledge came from the key, and nothing the model
> states or does supplies it
> ([`results_ranking/FINDINGS_RANKING.md`](results_ranking/FINDINGS_RANKING.md);
> `FINDINGS3.md` §14's erratum).

**It is strong exactly where P-d measures and nowhere else.** On the `puro` pool
over the corpus the same family is *worse* than arrival order, 0.4291 against
0.5216, and even the best of the 40,320 does not reach the floor. Once
subsumption has pruned the pool, most of what is left to decide is *which
action*, and a ranking of actions is the instrument for that.

The band does not move — it is signed — and what the control took away was the
power of a *hold* to mean anything, since a free lookup table sits above it
already. **In the event it is the refutation that needed the control**: P-d
landed below the floor, and the ranking's 0.4824 is what says the gap is 0.074
rather than a rounding error. See the entry below.

**And the edges the proposer actually wrote make the order worse than doing
nothing.** 400 calls over the learned base bought 344 declared edges — 1.3% of
the 31,850 pairs that could carry one — and the order they induce scores
**0.4080** on the `hibrido` pool at corpus test split 0, against a `born_at`
floor of 0.4332 and a P-d threshold of 0.4632
([`results3/FINDINGS3.md`](results3/FINDINGS3.md) §8,
[`declared_order.json`](results3/declared_order.json)). **`P-d` is refuted**, and
not by falling short of the margin: by landing below the floor.

**It is the model's choices and not the compilation, and that was checked.** The
same pairs, the same compilation, only the direction of each edge changed: a coin
lands at **0.4314** (sd 0.0243, 50 draws), on the floor; the model sits 0.96
deviations below it and **inverting every one of its answers** puts it at 0.4432,
above the floor. Each gap is inside one deviation, so each alone is a sign and
not an effect.

**And asked directly, the direction turns out to be right, which is the more
useful answer.** Of the declared edges on pairs where one rule is strictly better
over the region the two share, **194 of 278 point at it — 0.6978, six standard
errors above a coin** ([`results3/FINDINGS3.md`](results3/FINDINGS3.md) §9,
[`edge_direction.json`](results3/edge_direction.json)). The pairwise question
elicits real information. What it does not survive is compilation: with the null
sharpened to 2,000 draws the model's order sits at the 15th percentile of coins,
and **the oracle's own directions on the same 400 pairs reach only 0.4593, still
under P-d's 0.4632 threshold and still inside the coin distribution**. So **P-d
was not refuted because the proposer chose badly — it was refuted because 344
edges cannot move a 577-rule order across a 0.03 margin, whoever picks their
direction.** §8's `signal with the wrong sign` is withdrawn there by a dated
erratum.

**And the budget that would have worked is now known, for zero calls.** The
oracle's direction is computable offline on all 31,850 pairs, so the channel's
ceiling against budget is free ([`results3/FINDINGS3.md`](results3/FINDINGS3.md)
§10, [`edge_budget.json`](results3/edge_budget.json)). All on P-d's own cell:
**at 400 a perfect chooser, a 70% chooser and a coin are the same number** —
0.4533, 0.4471, 0.4556 against a coin deviation of 0.0239. Both cross P-d's
0.4632 threshold at **800** and a free queue ranking at **1,600**. So P-d was
adjudicated at the one budget in the range where nothing could be distinguished
from anything, and **doubling it would have flipped the verdict**.

**Accuracy does not wash out with volume**: exhausted, a perfect chooser reaches
0.6834 and a 70% chooser 0.5652, and that 0.12 does not close. **And the whole
channel tops out below search**: 0.6834 against the searched order's 0.7678 on
the same cell, flat from 12,800 edges on. Handed every pair and the right answer
to each, pairwise declaration still stops 0.084 short of what the optimizer
finds. The oracle and noisy curves are exact and projected respectively; what the
actual proposer scores above 400 is unmeasured and would take calls.

> **ERRATUM, 2026-08-26 — the last two claims above have been measured.** *"a free
> queue ranking at 1,600"* is **retracted**: the real proposer was asked at 1,600
> and its order scores **0.4804** against the ranking's 0.4824, so it ties it two
> thousandths low rather than crossing it. And *"what the actual proposer scores
> above 400 is unmeasured"* is no longer true at that budget. The projection was
> not miscomputed — its stated assumption, errors flipping independently and at a
> uniform rate, is what `B-d` refutes. Everything else in these two paragraphs
> stands, including that P-d's quantity does clear its threshold at this budget.
> [`FINDINGS3.md`](results3/FINDINGS3.md) §11 and its erratum to §10;
> [`declared_order_1600.json`](results3/declared_order_1600.json).

**The a/b asymmetry was never an effect; the position bias is.** The proposer
naming `rule_b` more often — 203/162 at 400 pairs, 781/698 at 1,600, unexplained
since Stage D — is entirely its queue ranking: `rule_b` is the later-born rule in
every pair, the ranking favours it on 0.5260 of them, and following it 0.8073 of
the time predicts naming `b` at 0.5160 against an observed 0.5281, a residual of
+0.93 standard errors. **What is real is a primacy effect, and it costs accuracy
rather than merely shifting taste**: the proposer applies its own ranking 0.8534 of
the time when the favoured rule is shown first and 0.7623 when shown second, +3.50
deviations. Specificity was refuted on the way — it names the BROADER rule, against
what its own explanations say, and that too rides on the ranking. POST-RUN,
adjudicates nothing ([`FINDINGS3.md`](results3/FINDINGS3.md) §15,
[`answer_asymmetry.json`](results3/answer_asymmetry.json)).

> **[ERRATUM 2026-10-05] *It costs accuracy rather than merely shifting taste* is
> more than these counts say.** With presentation balanced, the 0.8534 and 0.7623
> follow by arithmetic from the 0.8073 and the 0.5416 above and how the slots
> fell. They are the first-shown preference read through the ranking, and cannot
> tell a taste for the first slot from a loss in the second. **What the randomised
> deal licenses is a floor**: the slot decided the direction of at least about one
> edge in eleven, +0.0911 with a standard error of 0.026. Whether that costs
> accuracy on net is not identified, since each pair was asked in one order. **And
> it has been seen on one population of two.** Stage C, the same model and prompt
> over the hidden policy's pairs, named the rule shown first in 84 of 166 answers,
> 0.506. The difference is 0.87 standard errors, so neither rate is evidence
> against the other. `FINDINGS3.md` §15 owns the arithmetic, in its erratum of the
> same date. No figure moves.

**And where the slot decides, measured.** `PLAN_PRIMACY.md` read the same 1,600
answers for it, at zero calls
([`results_primacy/FINDINGS_PRIMACY.md`](results_primacy/FINDINGS_PRIMACY.md)).
The slot was dealt by a seeded shuffle, so every figure below is a floor on the
share of answers it decided.

- **About one answer in twelve overall**: +0.0823 with `rule_a` as the reference.
- **Not demonstrably a fifth where the proposer splits evenly.** On
  `SELF_SERVICE_DEFLECT vs T2_TECHNICAL` it is +0.1236 against `L-a`'s line of
  0.20, refuted and thin. There the answers name the better rule half the time.
- **Nothing besides which rule is named.** Answers with no edge, and calls
  needed, are the same whichever slot holds the favoured rule (`L-b` holds).
- **The same on both sides of B-d, in both batches, and whichever rule is the
  broader.** So it explains none of B-d's gap.
- **Mostly one queue pair.** On `T1_GENERAL vs T2_TECHNICAL` the slot decides at
  least a fifth of 361 answers, +0.2256. The other 1,118 name the rule listed
  first within noise of a coin. Post-run, picked out after the verdicts.

**And what the proposer says, measured.** `PLAN_WHY.md` coded the sentence it
wrote beside each answer, with a codebook frozen on a development set, and read
the 1,114 sentences of the held-out batch
([`results_why/FINDINGS_WHY.md`](results_why/FINDINGS_WHY.md)).

- **Its "more specific" is true of the extension about half the time.** Answers
  that argue it name the narrower rule 0.5256 of the time, against 0.3941 across
  all answers (`Y-a`).
- **It is not a count of conditions** (`Y-b`). **It is a categorical or exact
  condition the other rule lacks**: 0.7658 against 0.4435 (`Y-c`). For this
  proposer, specificity is how a rule is written, not what it covers.
- **The reason does not mark the right answers**: 0.7395 against 0.7470 on the
  space (`Y-d`). When it counts conditions, rung 1's criterion, it is right about
  as often as a coin.
- **It almost never names the order.** 8 sentences of 1,114 give the list's
  order as the reason, all for the rule listed first, against a slot that
  decides at least one answer in twelve. Post-run.

**And the base those answers were asked about is half copies.** 307 of rung 1's
577 rules have a copy written with the same conditions, so as written the base
holds 353 distinct rules. 93 pairs of copies send the ticket to different queues,
nearly all among the generic queues, and no order can split one: whichever copy
is placed first decides every ticket of theirs that reaches the two. Over the
space the hidden policy agrees more often with the copy written later in 49 of
them and the earlier in 29, so arrival order picks the worse one more often.
POST-RUN, a census
([`FINDINGS3.md`](results3/FINDINGS3.md) §18,
[`identical_rules.json`](results3/identical_rules.json)).

**And the copies were written below ties they could not join.** Replayed, rung
1's engine bore every later copy on a CONFLICT, 201 of 224 of them in a tie among
more specific rules, and none of them ever decided a case. Of the 540 rules born
on a CONFLICT, 36 had more conditions than the tie that bore them, the only ones
that could settle that case. POST-RUN ([`FINDINGS3.md`](results3/FINDINGS3.md)
§19, [`copy_births.json`](results3/copy_births.json)).

**Nothing chooses better than chance, and B-b's line was never reachable at that
budget.** Truth-free rules for dropping declared edges — keep the proposer's
self-consistent core, keep only where it contradicts its own majority — all sit
within **0.7 deviations** of dropping the same number at random, in both
compilations. The topological sort's arrival accident sits +1.24 deviations above
the same edges in a random arrival order: suggestive, not significant. **And a
perfect follower of the proposer's own queue ranking, answering all 1,479 pairs,
scores 0.4402** where that ranking applied as a lookup over all 577 rules scores
0.4824. 1,479 pairs is 4.6% of the 31,850 that could carry an edge, so the channel
at this budget cannot express the baseline `B-b` was signed against — **`B-b` is
refuted as signed and what it measures is at least as much the budget as the
proposer**, whose 0.4804 is in fact above that perfect follower's 0.4402. POST-RUN,
not a signed row ([`FINDINGS3.md`](results3/FINDINGS3.md) §14,
[`edge_dropping.json`](results3/edge_dropping.json)).

> **[NOTE 2026-10-05] *Nothing chooses better than chance* is a null with almost
> no power.** §16 of `FINDINGS3.md` measured what the instrument could show. An
> oracle that keeps the right edges first sits between −0.3 and +3.0 deviations
> above a same-size random choice, about +1.3 at the median. At §14's sizes it is
> +0.9 to +1.6 under the corpus definition. So the selection was not ruled out:
> at 1,479 edges it was not testable. Wrong edges hurt more than right ones help,
> down to −5.5 deviations under MFAS. Read inside that headroom, the proposer's
> stated reasons cut nothing, but one cut. Dropping the edges whose reason is a
> queue's importance, mostly the security keyword, comes near the ceiling in MFAS
> on the corpus: +2.52 against the oracle's +3.0. That is a post-run lead, one
> cut of seven, on one surface
> ([`filter_headroom.json`](results3/filter_headroom.json)).
>
> **[NOTE 2026-10-05, later] Over the space that lead reverses, violently.** §17
> of `FINDINGS3.md` scored §16's selections over the exhaustive space. The same
> cut goes from +2.52 deviations on the corpus to **−11.28** in MFAS, 0.2775,
> under the `born_at` floor. Every edge that names `SECURITY_INCIDENT` the winner
> carries a queue reason, and over the space that queue is the truth for three
> points in eight. The lead was the keyword's split between the surfaces. **And
> §16's oracle bounds selection by direction only**: over the space one
> truth-free cut sits above the oracle of its size and another ten deviations
> below the anti. POST-RUN, with an expectation written before the run whose
> third clause failed ([`filter_space.json`](results3/filter_space.json)).
>
> **[NOTE 2026-10-17] *That ranking applied as a lookup* scores 0.4693, not
> 0.4824.** The 0.4824 is Stage C's ranking. The proposer's own revealed ranking,
> the one the perfect follower follows, was first scored as a lookup by
> `PLAN_RANKING.md`'s Stage A: 467 cases of 995 against Stage C's 480. So the
> proposer's 0.4804 is above its own ranking as a lookup, and `B-b`'s line is a
> ranking the proposer does not hold even without a channel. `B-b` does not move
> (`FINDINGS3.md` §14's erratum,
> [`FINDINGS_RANKING.md`](results_ranking/FINDINGS_RANKING.md)).

**It is the answers, not the compilation — and the sort was hiding it.** The same
1,479 declared edges compiled by minimum feedback arc set instead of the
cycle-refusing topological sort, which silently drops 169 of them first-come-
first-served. Violations fall in every arm and the score goes the other way in two:
the **oracle gains +0.0100** from honouring 19 more of its own edges, while the
**model loses 0.0472** and a **coin loses 0.0623**. So a better compilation is
worth something when the directions are right, and the proposer's edges — honoured
fully — are worse than not honouring them. **Part of §11's 0.4804 was the
compilation's lossiness protecting the score**, which is a different quantity from
what the edges buy and was not separated until now. POST-RUN with an expectation
written before the run, not a signed row
([`FINDINGS3.md`](results3/FINDINGS3.md) §13,
[`mfas_compilation.json`](results3/mfas_compilation.json)).

**The order that was available lived where the proposer was random.** Splitting
the 1,600 run's 1,310 accepted edges by whether a fixed queue ranking could answer
their queue-pair, and compiling each side alone against a coin on its own rows: a
perfect chooser scores **+3.33 coin deviations** on the pairs a ranking cannot
answer and **+0.79** on the ones it can, so essentially all the winnable order is
on the first side. The proposer is at **−0.58** there — inside noise, so no better
than a coin — and its headroom to the oracle is 0.1156 against 0.0050. **A
direction rate of 0.6391 on those pairs is therefore worth nothing at the order
level**: a ranking-shaped error is not a random error, and correlated errors
cancel the correct answers rather than adding to them. POST-RUN, adjudicates
nothing ([`FINDINGS3.md`](results3/FINDINGS3.md) §12,
[`edge_sides.json`](results3/edge_sides.json)).

**What the real proposer buys at 1,600 pairs, measured.** 1,200 calls on top of
Stage D's 400, `hibrido` pool / corpus test split 0. Its direction rate holds at
**0.7312** (n 1105, space definition) against 0.6978 at 400 — the instrument did
not move — and the order those edges compile into scores **0.4804**: over the
0.4332 arrival floor by 0.0472, and level with a free queue ranking that reads no
rule. **The rate is 15 deviations above a coin at the pair level and the order is
0.40 deviations above one.** Almost everything the channel is told is lost in
compilation, which is §9's conclusion at four times the budget. The four signed
rows and their figures are in [`FINDINGS3.md`](results3/FINDINGS3.md) §11;
records [`pair_judgement_1600.json`](results2/pair_judgement_1600.json),
[`edge_direction_1600.json`](results3/edge_direction_1600.json) and
[`declared_order_1600.json`](results3/declared_order_1600.json).

**`P-e` is refuted too, and by a wide margin.** Behavioural distance from 65 end
orders **regenerated on the hybrid pool** — never the published `puro` ones —
comes out at a median **0.4497** of the exhaustive space against a band of ≤0.25.
The declared order is not inside the cloud; it is a different machine from all 65,
whose own members disagree with one another by up to about 20%.

**And the authorship cost is now measured.** With those 344 edges installed the
engine reaches e2e **0.0673** and **abstains on 89%** of corpus test: 885
CONFLICTs in 995 cases, silent error 0.3909 over the 110 it commits to. Rung 2's
hidden policy needs 199 edges for 29 rules and reaches 1.0000; a 577-rule learned
base is not in that neighbourhood. The mechanism is doing what it should — nobody
told it who wins, so it abstains — which is why the conflict rate is the honest
reading and the e2e is not.

**An ordering problem and a material problem are different things.** Six classes
of eight — 1774 of 2000 cases — are pure ordering. `SECURITY_INCIDENT` (20 cases)
and `ONCALL_ESCALATION` (7) are **100% recoverable** and rung 1 gave **0/17** and
**0/7**. But 66.7% of `T3_ENGINEERING` and 64.2% of `ACCOUNT_MANAGER` have no
correct rule covering them at all; no order saves those. Corpus; FINDINGS3 §2.
Which classes get sacrificed is a choice of objective function, and rung 1's
arbitration was making it undeclared (§3).

**Priority is partly learnable from the feedback a real system gives.** Symmetric
supervision beats born_at by **+0.3273**; asymmetry 0 — feedback only on errors,
the only kind a deployed system produces — by **+0.2011**, 61% of it, on corpus
test ([`results4/FINDINGS4.md`](results4/FINDINGS4.md) §1 erratum,
[`sweep_ls.json`](results4/sweep_ls.json)). On the space the same orders give
0.6157 and 0.5757 against the 0.8784 bound: same direction, larger shortfall. The
learner never sees the truth by any route (the record's wording, "the only module
that imports `true_action`", was corrected — `sweep.py` carries an unused
import).

**Cheap supervision is nearly free, and less free than published.** Under the
audited optimizer the label-budget curve reads 0.8530 / 0.8227 / 0.7771 / 0.7410
/ 0.5767 on **corpus test** for 1005 / 251 / 100 / 50 / 10 labels, pure pool.
The headline ratio 5%/100% falls from 0.9147 to **0.8687**: 50 labels still buy
87% of full supervision, on a full supervision that is now worth more
([`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md), Step 3;
[`budget_and_balance_ls.json`](results3/budget_and_balance_ls.json)). On the
**exhaustive space** the same orders give 0.6105 down to 0.3310, and low budgets
transfer proportionally worse.

> **[NOTE 2026-10-19] Drawn from the escalations instead of the train half, on
> split 0, the same budgets buy about as much on corpus test and less over the
> exhaustive space.** At fifty labels the median of five orders is 737 of 995
> against the record's draws' 717 (`J-a` and `J-b` hold, `J-b` thinly). Over the
> space it is 0.3426 against 0.3993 (`J-e` holds). All 316 escalations give 814.
> [`results_escalations/FINDINGS_ESCALATIONS.md`](results_escalations/FINDINGS_ESCALATIONS.md).
>
> **[NOTE 2026-10-19, later] With every escalation labelled, a random audit of
> the decisions climbs the rest of the curve slowly.** Beside the 316 escalations,
> 10, 50, 100 and 251 audited decisions give medians of 814, 818, 826 and 833 on
> corpus test split 0, against the whole train half's 843 (`N-a` to `N-e`).
> Alone, at equal budget, the decisions buy less than random escalations and
> random arrivals at every budget.
> [`results_spotcheck/FINDINGS_SPOTCHECK.md`](results_spotcheck/FINDINGS_SPOTCHECK.md).
>
> **[NOTE 2026-10-20] Along the same curve, the rules no label reaches.** The
> optimizer audit's twenty orders on split 0 leave 247 to 357 rules unreached
> at ten labels and 17 to 28 at 251. Moving all of them below every reached
> rule, which reads no truth, changes the test count by −32 to +9 and the space
> count by −11,500 to +5,185, and changes nothing in nine orders. Reported
> (`Z-f`).
> [`results_unreached/FINDINGS_UNREACHED.md`](results_unreached/FINDINGS_UNREACHED.md).

**Caveat on the low-budget rows, added August 15, 2026.** Step 3 reads them as
*the tie-break regularises*: the objective saturates, most starts tie, ties go to
index 0, so the search returns a sane default. Measured as orders, that reading
is too kind. At 10 labels (split 0, draw 0) the **40 orders tying at the best
train score are 40 distinct machines**, disagreeing with one another on a median
**39.2% of the exhaustive space**. The search is not declining to act; it is
choosing arbitrarily among very different answers and landing on a sane default
by accident of the start order. The figures stand — they are what the declared
instrument returns — but anyone who changes the tie-break or the order of the
declared starts changes which of the 40 ships
([`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md)). **This one
survives the change of surface**: on the corpus those 40 machines still disagree
a median **24.05%** of the 2000 cases, 24.32% of corpus test, against 39.2% of
the space — a fall of 1.6× where full supervision falls by 3.5×.

**Protecting the rare classes costs a quarter of what it looked like.** Balancing
the objective costs the greedy 0.0563 in e2e and buys +0.1735 in balanced
accuracy; under the local search it costs +0.0274 and buys **+0.0576**, corpus
test. Most of what read as objective conflict was search weakness: with no
balancing at all, the local search recovers 19 of 21 attainable ACCOUNT_MANAGER
cases where the greedy recovered 0. On the exhaustive space, macro-recall says
balancing buys the greedy +0.1093 and the local search +0.0201. FINDINGS_AUDIT,
Step 3.

**The signal runs out as the system improves.** Under asymmetric feedback the
volume of labels is proportional to the error rate of the system observed, so
observing a worse π₀ produces a better order. A property of the channel, not of
the learner — the one section of rung 4 the audit left standing (FINDINGS4 §3).

**The founding question, measured on the engine that can answer it: the rules get
reused, and most of their errors are born with them.** `PLAN_REUSE.md` ran rung
2's loop — the engine that executes the hidden policy at 1.0000 — over rung 1's
2,000 cases, three times, with prompt v1 and reasoning off. These are medians of
the three runs, on the corpus, from
[`results_reuse/FINDINGS_REUSE.md`](results_reuse/FINDINGS_REUSE.md):

- **Reused.** Reuse is **0.7381**, far above the 0.30 stopping threshold of
  2026-08-05 and the 0.1176 memorization floor (`U-a` holds). It carries **rung
  1's caveat**: a median 0.2857 of the escalations were CONFLICT, so part of what
  escalated was the arbitration.
- **Wrong at birth.** About three silent errors in five come from rules born with
  the wrong queue (`U-c` holds, at 0.6024 against 0.60). The proposer chose the
  right queue for the ticket in front of it about half the time. **Measured
  directly, about four silent errors in five are ones the model asked afresh
  would make too** (`F-d`, below), so the split by birth undercounts them.
- **No better than a heuristic on scope.** On the scope axis, the rules born right
  err about as much as a fixed heuristic handed the right action (`U-b` holds, at
  +0.0207). That margin moves with where their reuse lands on a steep frontier.
- **The rarest queue is never asked about.** All 7 `ONCALL_ESCALATION` cases were
  decided by a rule, wrongly, in every run, and none escalated (`U-d` refuted). So
  the ILP thread's *what the loop never asks about, no method can learn* belongs
  to compilation by impasse, not to rung 1's conflict trigger.
- **Declared priority got material for the first time.** Edges were accepted in
  every run. `contradice_subsuncion` still never fired. **[NOTE 2026-10-06]** It
  has fired since, under the protocol of `PLAN_AUTHORSHIP.md` (`E-d`, below).

Stage A found the same shape at n=100 in the eight August runs; it is reported,
not adjudicated.

**And the bases that loop wrote leave Stage E little to order where tickets
arrive, and much over the function.** Read whole from case 0, subsumption alone
decides 96% to 99% of the corpus on each of the three, against 8% on rung 1's
base, and is wrong 0.47 to 0.59 of the time. On the corpus its end to end sits
within 0.04 of the hybrid coverage bound, the most any order over its pool could
reach, which is only 0.42 to 0.54. Over the space it sits 0.19 to 0.46 below that
bound. The gap Stage E's second prediction would narrow, between the hybrid and
pure bounds, is already zero or 0.0005 on the corpus and at most 0.006 over the
space. **The proposer declared most of its priority on copies**:
every rule written again was born on a CONFLICT, never decided a case, and
carried 35 of the 64 accepted edges, because the protocol answers an escalation
only with a rule. POST-RUN, with an expectation whose fourth clause failed
([`FINDINGS_REUSE.md`](results_reuse/FINDINGS_REUSE.md), *The three bases, read
for Stage E*; [`structure.json`](results_reuse/structure.json)).

**Fidelity, measured: the rules decide unlike the model would, and compiling
loses it nothing on the cases they decide.** `PLAN_FIDELITY.md` re-asked the
model, twice, on 600 decided cases of each of `PLAN_REUSE.md`'s three bases. It
used prompt v1 with every rule that matches the ticket hidden, so that each
case was the coverage impasse it would have been. Medians of the three runs, on
the corpus, from
[`results_fidelity/FINDINGS_FIDELITY.md`](results_fidelity/FINDINGS_FIDELITY.md):

- **Unfaithful.** The model agrees with itself 0.89 to 0.95 of the time, and
  with the rule that decided the case 0.64 to 0.81 (`F-b` holds, at 0.1838
  against 0.10). The instrument had not moved since the rules were written
  (`F-a` holds, at −0.0075).
- **Not costly.** Asked afresh, it is not right more often than the rules
  (`F-c` refuted, thinly, at −0.0126). It does better where a rule was born
  wrong and worse where one was born right, and the two cancel.
- **The error is the model's own, more than the proxy said.** On the rules'
  errors it is wrong too 0.7955 of the time, mostly with the rule's own wrong
  queue (`F-d` holds). Case by case, `U-c`'s split by birth agrees with that
  0.55 to 0.62 of the time.
- **The rarest queue is in the model.** Shown its screen of compiled rules, it
  names `ONCALL_ESCALATION` on 3, 0 and 2 of the seven tickets (`F-e` holds, at
  2). Without a screen it names it on all seven, 14 answers of 14.
- **And the screen seems to cost it.** On the same 300 cases, one answer each:
  without a screen it is right 0.5233 of the time, with it 0.4600, and the
  rules 0.4267. It is a sign in the same direction in every run, not a measured
  effect. Disagreement with a fresh answer does not find the rules' errors in
  two runs of three. **[NOTE 2026-10-15] Measured by `PLAN_SCREEN.md`, on
  decisions nobody had asked without a screen: it does cost it, through
  deference to the screen's commonest action.** See the entry below.

The last two are reported, not adjudicated.

**What declared priority bought, measured: right over the function, wrong where
tickets arrive.** `PLAN_EDGES.md` scored the edges the proposer declared at write
time in `PLAN_REUSE.md`'s three runs. The engine had installed 50 of them, and
they decided 114 cases. Pooled over the three runs, from
[`results_edges/FINDINGS_EDGES.md`](results_edges/FINDINGS_EDGES.md):

- **Right a third of the time on the arrivals.** On the cases they decided the
  edges were right 0.3246 of the time, worse than the base they sit in (`W-a`
  holds).
- **Right three times in four over the function.** For 34 of 45 edges the
  declared winner is the better rule over the shared region on the exhaustive
  space: 0.7556, above the pairwise question's 0.6978 and 0.7312 (`W-b` refuted
  upward). By the corpus definition it is 0.4118.
- **Better than a coin only by resolving more.** A coin matches the proposer's
  right decisions in 0.0005 of draws (`W-c` refuted), because a flipped edge
  leaves its conflict open. Among the cases it resolves, a coin is right 0.3272
  of the time and the proposer 0.3246. That reading is post-run.
- **One rule of thumb, two surfaces.** 47 of the 50 edges say that on a ticket
  with the security keyword `SECURITY_INCIDENT` wins. The hidden policy sends
  three quarters of the space's keyword points there, and 20 of the corpus's 71
  keyword tickets. From their edges the final bases gain 0.07 to 0.36 of e2e over
  the function, and 0.004 to 0.016 on the arrivals. Post-run.
- **A rare class gained.** 5, 6 and 15 of `SECURITY_INCIDENT`'s right compiled
  decisions came through an edge. The price was 68 `T2_TECHNICAL` tickets sent
  there.

**Declaration imposed at write time, measured: the proposer met it by not
overlapping.** `PLAN_AUTHORSHIP.md` ran `PLAN_REUSE.md`'s loop three more times at
n=2000, under a protocol that refused a rule overlapping another until the
proposer declared it an exception to it or a default under it, nested rules
included. Each final base is read whole, from case 0, and the figures are from
[`results_authorship/FINDINGS_AUTHORSHIP.md`](results_authorship/FINDINGS_AUTHORSHIP.md):

- **It did not nest the base.** Nested pairs are 0.0023 of all pairs on the
  median of the three runs, against the baseline's 0.0160 (`E-a` refuted).
- **Subsumption over the bases is wrong more often, not less.** On the full
  corpus, on the median, it is wrong on 0.6448 of what it decides, at a coverage
  of 0.9925, against the baseline's 0.5521 (`E-b` refuted).
- **One run left nothing to order** (`E-c` unadjudicable). Its base holds one
  overlapping pair, and that pair is nested. Over the space, the installed edges
  of the other two runs filled all of the order's room and 58% of it. The row's
  verdict rests on the scorer's reading of the median, set out in the scoreboard
  above.
- **The proposer contradicted subsumption, for the first time in the project.**
  8 declarations pooled, in two runs of three, each refused by level 1 (`E-d`
  holds). v1 had told it not to declare on nested pairs. **[NOTE 2026-10-06,
  later]** Seven of the eight were idle: a rule widened, with the same queue,
  and declared the winner over the rule it widens. On the one pair with
  different queues, level 1 was right on every point of the region. POST-RUN,
  one case, a reading and not a rate (*The eight refused declarations*).
- **It overlapped less.** 70% to 97% of the rules it wrote overlap no rule before
  them, against 27% to 39% in the baseline. No CONFLICT arose in 6,000 arrivals,
  so the order answer was never used. Reported, not adjudicated (`E-e`).

Beside the baseline's, the loop's own figures show more reuse, more silent
error, and a proposer that chose the right queue less often. Two caveats the
plan declared bear on them: the longer screen a repair round shows the model,
and the five days between the two sets of runs.

**Declaration imposed again, with the proposer told to overlap: it still
partitioned, and where it did not, its edges ordered the function through one
rule.** `PLAN_OVERLAP.md` ran `PLAN_REUSE.md`'s loop three more times at n=2000,
under v2e: rung 2's v2, which tells the proposer that overlap is normal and shows
it the engine's set arithmetic, with v1e's discipline asked only where the
queues differ. Each final base is read whole, from case 0, and the figures are
from
[`results_overlap/FINDINGS_OVERLAP.md`](results_overlap/FINDINGS_OVERLAP.md):

- **It partitioned in two runs of three.** On the median, 0.8049 of the rules it
  wrote overlap no earlier rule of another queue (`O-a` refuted). Run 1, at
  0.2545, overlapped more than any v1 run. **[NOTE 2026-10-08] Through one
  rule.** `R0017`, the keyword rule, covers half the space and is in 38 of the 41
  `O`s of run 1; without it, run 1 reads 0.8545. Read POST-RUN, so the proposer
  partitioned in all three runs, against every rule but one (*What separates
  the run that overlapped*).
  **[NOTE 2026-10-08, later] And `O-a`'s baseline was not like for like.** v1's
  overlap is the keyword too: one broad keyword rule in two runs, and in the
  third the keyword rules it wrote on CONFLICTs, which v2e never did. On births
  on an impasse and without each run's top rule, v1 sits at 0.80 and v2e at 0.98
  on the median: both partitioned, v2e more (*What v1's overlap is made of*).
- **Where it left room, its edges filled most of it over the space**: 73% and
  all of it in runs 1 and 2, 0.8660 under §0's rule (`O-b` holds). Run 3 left
  none.
- **They pointed at the better rule 44 times in 47** (`O-c` holds). Read
  POST-RUN, 43 of the 47 are one declaration: a ticket with the security keyword
  goes to `SECURITY_INCIDENT` before `T2_TECHNICAL`. Those edges also carry most
  of `O-b`'s fill. It is the rule of thumb behind v1's edges, `W-b` above.
- **Asking only where the queues differ removed the idle edges and the
  contradictions**: none was installed between rules of one queue, and none
  contradicted subsumption, against 15 and 8 under v1e (`O-d`).

On the corpus the order's room was 81 and 15 arrivals of 2,000. On the median,
the loop's end to end is 0.4400 under v1, 0.3505 under v1e and 0.3495 under v2e.

**Beyond the security keyword, with the rule drafted blind: the proposer crossed,
and its declarations pointed the way a coin would.** `PLAN_BLIND.md` ran
`PLAN_REUSE.md`'s loop three more times at n=2000, under v2b: v2e with the base
taken out of the first call on an impasse, and one placement round asking for
the same rule, placed against every rule of another queue it overlaps. Every row
is read where `has_security_keyword` is False: the half of the space without
it, and the 1,929 corpus cases without it. The figures are from
[`results_blind/FINDINGS_BLIND.md`](results_blind/FINDINGS_BLIND.md):

- **Drafted blind, it crossed.** On the median 0.2963 of its births met no
  earlier rule of another queue there, against 0.9667 to 1.0000 under v1, v1e
  and v2e (`K-a` holds).
- **There, its declarations point at the better rule 0.5460 of the time**, each
  of 65 older rules counted once (`K-b` refuted). **The Stage C ranking reads
  the same pairs at 0.7219** (`K-c` refuted), and "the new rule always wins" at
  0.5804. On the arrivals the declarations read 0.5861 (`K-e` refuted).
- **Right where a ranking can answer, a coin where it cannot**: 0.8452 against
  0.4747, `B-d`'s split again.
- **The edges fill 0.6061 of the order's room over the function** (`K-d` holds).
  Read POST-RUN, it is mostly resolution: a coin pointing the same edges fills
  0.40 to 0.45, and among what each resolves the declared directions beat a
  coin's clearly in one run of three. The ranking pointing them fills more in
  every run.
- **Run 1's cycles, read POST-RUN, are the base's own order contradicted, and
  not the slot.** Every refusal at a placement in the three runs, 21 for a cycle
  and 7 against subsumption, put below the new rule a listed rule the base
  already ranked above it. In 16 of the 21 that order runs through a rule of the
  new rule's own queue nested in it, which a placement never lists. The slot
  moves nothing a test can see: p 0.24 over 128 pairs placed on opposite sides.
- **And the order those refusals kept is the wrong one, read POST-RUN.** An
  engine that read the base's transitive closure would resolve every one of
  run 1's 1,825 CONFLICT points over the space. It would be right on 10, where
  the declarations the engine refused are right on 535; on the other 1,280
  neither side is. Run 3's 60 points go the other way. Without a forced
  placement, under v1, the closure resolves under 4% of the CONFLICTs.
- **Which edge of a cycle yields is, by age, a draw beyond the keyword, read
  POST-RUN.** The engine lets the newest edge yield. Letting the oldest yield
  instead, read through the closure over the space, gains 655 points of 403,200
  on the three bases with a cycle, v2b's runs 1 and 3 and v2e's run 1. It loses
  115 in run 3, where the older order was right. Beyond the keyword both ages sit inside a coin's draws, the Stage C
  ranking beats 96% of them, and the oracle every one. Under rung 2's engine the
  same trade in run 1 is right on 570 more points and wrong on 1,255 more.
  **[NOTE 2026-10-18]** That ranking read the key. The model's own rankings, put
  in its place, choose as a draw does: the M section below, POST-RUN.

On the median the loop's end to end is 0.5075 under v2b, and the proposer chose
the right queue 0.5521 of the time, the highest of the four protocols, with the
bundle and the date between them as caveats.

**The screen of compiled rules, measured: the model defers to it, and on these
bases that costs it.** `PLAN_SCREEN.md` asked the model, twice, every ticket of
`PLAN_FIDELITY.md`'s draw with the ticket alone, under prompt v1 and with
reasoning off. It set those answers beside `F-f`'s two answers with the screen,
on the decisions whose tickets nobody had asked without one: 429, 405 and 425.
Medians of the three runs, on the corpus, from
[`results_screen/FINDINGS_SCREEN.md`](results_screen/FINDINGS_SCREEN.md):

- **Without its screen the model is right more often**, by 0.0667, in every run;
  0.0774 pooled (`V-b` holds).
- **The screen pulls the model to its commonest action.** Where the model's own
  answer is not that action, the answers with the screen land on it 0.3178 more
  often than a second answer without the screen does (`V-c` holds). Of the 700
  answers the screen changed, 516 went to that action and 24 to a queue it did
  not show.
- **What the screen does follows that action.** Where it is the true queue the
  screen puts the model ahead by 0.1583; where it is not, behind by 0.2054
  (`V-d` holds). On these bases it is the true queue on 0.31, 0.36 and 0.28 of
  the decisions, so the net is a cost.
- **The model without a screen moved a little in twelve days** (`V-a` refuted,
  thinly): its answers agreed with those of 2026-10-03 less than with each
  other, +0.0615 against 0.05, while with a screen it held at +0.0284. Its
  accuracy did not move, and asked under both arms on one day the pilot shows
  the same gap, 0.0633, as across the two dates, 0.0617.
- **The rarest queues are in the model, on a second day.** With the ticket
  alone, both answers name `ONCALL_ESCALATION` on all 7 of its tickets and
  `SECURITY_INCIDENT` on all 20. `ACCOUNT_MANAGER` it names on none of its 65
  held-out decisions. Reported (`V-e`).

So the cost of compiling that `F-c` found nowhere in the rules' own decisions is
in what showing them does to the model's next answer. Its sign belongs to the
base: the same deference to a base right more often than not would pay.

**The ranking of the queues, asked of the model: it states a priority order, and
as an arbitration order that is worth less than a blind draw.**
`PLAN_RANKING.md` asked the model, 24 times, for the one order between the
eight queues that decides which wins when two rules match a ticket and send it to
different queues. Each ask named the queues and nothing else, in twelve
presentation orders. Every answer was scored as a lookup over rung 1's 577 rules,
on the hybrid pool at corpus test split 0, from
[`results_ranking/FINDINGS_RANKING.md`](results_ranking/FINDINGS_RANKING.md):

- **It states a priority order**, the same one 14 times in 24:
  `SECURITY_INCIDENT` first and `SELF_SERVICE_DEFLECT` last in all 24, and the
  technical tiers in escalation order above the specialist queues. Every one of
  its 24 reasons names a priority. The slot barely moves it (`M-a` holds).
- **As an arbitration order it wins 335 cases of 995**, 0.3367: below arrival
  order's 431 and below a ranking picked blind, at the 0.36 percentile of the
  40,320 (`M-b` and `M-c` refuted). Over the space it sits at the 0.89
  percentile.
- **What it states is not what it does** (`M-d` refuted). It predicts 935 of
  the model's own 1,479 pairwise answers, where Stage C's ranking predicts 1,190
  and the model's revealed ranking 1,194. Pairwise the model named
  `BILLING_SPECIALIST` over `T1_GENERAL` 167 times to 13; stated, it ranks
  `T1_GENERAL` above it in 22 of 24 asks.
- **On `K-b`'s pairs it points no worse than the declarations**, 0.5496 against
  0.5460 (`M-e` holds, thin), and on the arrivals worse.
- **The revealed ranking had never been scored as a lookup**: 0.4693. That is
  between the stated ranking and Stage C's, and below the 1,600-call compiled
  order's 0.4804. `FINDINGS3.md` §14 had given it Stage C's 0.4824.
- **Neither ranking the model gives chooses which edge of a cycle yields as the
  key's does, read POST-RUN.** Each was put in the Stage C ranking's place in
  `blind/yielding.py`'s ranking arm, on the three bases with a cycle. Read
  through the closure over the space beyond the keyword:
  - the stated ranking is right on 70,005 points and the revealed one on
    69,435, against the Stage C ranking's 70,675 and arrival's 69,820;
  - 45.5% and 80% of a coin's draws do at least as well, against 4% for the
    Stage C ranking.

  Nearly every cycle is on one queue pair. The revealed ranking puts
  self-service above `T2_TECHNICAL` there, on 86 pairwise answers to 82.

So a free question does not buy the free baseline. The model's competence at
arbitrating queues is in its pairwise answers, and the ranking it states about
them is a different object.

**What the proposer's rules buy over a learner fitted to its answers: on the
arrivals they beat it, and over the function their order costs them.**
`PLAN_STUDENTS.md` trained three students on the queues the proposer named at
rung 1's 579 escalations, and on nothing else. The first is a pruned decision
tree, whose leaves are rules of the frozen DSL. The second is a logistic
regression. The third is the cache's retrieval, `harness/cache_baseline.py`'s
null hypothesis, holding the proposer's answers where it had cached the truth.
They were set beside the 577 rules written from the same answers, from
[`results_students/FINDINGS_STUDENTS.md`](results_students/FINDINGS_STUDENTS.md):

- **On corpus test split 0 the rules in arrival order beat every student**:
  519 of 995, against the tree's 470, the regression's 466 and the cache's 434
  (`T-a` and `T-b` hold).
- **Over the space the tree beats arrival order**, 59,466 points of 134,400
  against 42,310 (`T-c` holds). **Read newest first, the same rules beat the
  tree on both surfaces**: 544 and 76,180.
- **Ordered with the proposer's own answers, the rules do worse than in arrival
  order**: rung 3's search on the 286 train-half answers reaches 483 (`T-d`
  refuted). On the truth of the same 286 tickets it reaches 814, 91% of the
  searched order's gain over arrival.
- **On `PLAN_REUSE.md`'s loop the tree ties the base**: +1, +28 and −50 test
  cases by run, a median of one case (`T-e` refuted, thin).
- **Handed the truth of the 286 train-half tickets, the tree is right on 894**,
  above the searched order's 843. Handed the answers on the same tickets, it
  is right on 500. Reported.
- **The tree on the answers decides all three `ONCALL_ESCALATION` test cases
  right**, through leaves that send severity-1 tickets there, learned from the
  7 answers that named the queue on `T2_TECHNICAL` tickets. No execution of the
  rules decides more than two. Reported, and what those leaves cost elsewhere
  is not counted. **[NOTE 2026-10-18, later] Counted, POST-RUN**: they decide
  45 test cases, 40 of them `T2_TECHNICAL` or `T3_ENGINEERING` in truth, and
  cost the tree 17 cases against arrival, a third of its gap.

So the scope the proposer wrote into each rule is worth something where tickets
arrive, and a learner fitted to its queues does not recover it. What the queues
lack is truth: on the train half the labels cost a tree on the same tickets 394
cases, and the same search, handed the answers, orders the rules worse than
their arrival.

**What a reviewer's labels at the escalations buy the order: on the arrivals,
what labels drawn at random buy; over the function, less.**
`PLAN_ESCALATIONS.md` labelled rung 1's 316 train-half escalations with the
truth, as a reviewer would, and handed sets of them to rung 3's search at the
audit's label budgets. Each set was read beside that record's own random draws
of train cases at the same budget, on split 0, from
[`results_escalations/FINDINGS_ESCALATIONS.md`](results_escalations/FINDINGS_ESCALATIONS.md):

- **Fifty escalations drawn at random order the rules to 737 of 995 on corpus
  test split 0**, at the median of five draws: two thirds of the 324 cases the
  full search gains over arrival order (`J-a` holds).
- **That is about what fifty random train cases buy**: 717 (`J-b` holds,
  thin). At 251 labels the escalations give 816 and the arrivals 820 (`J-c`
  holds), inside the arrivals' own draws, 768 to 829.
- **Labelling the most crowded escalations first buys almost nothing there**:
  523, four cases above arrival order (`J-d` refuted). 49 of the 50 are
  `SELF_SERVICE_DEFLECT` or `BILLING_SPECIALIST` tickets. Labelling the first
  fifty as they came gives 708. Over the space the most crowded give the
  highest share of any set of escalations at 50 and at 251 labels. Reported.
- **Over the space the escalations buy less than random arrivals at every
  budget**: 0.3426 of the 134,400 points at fifty labels, against 0.3993 (`J-e`
  holds). **[NOTE 2026-10-21] Read POST-RUN, the gap lies in the keyword
  half**: at every budget the other half's medians differ by 1,240 points at
  most (`FINDINGS_UNREACHED.md`, *What the keyword holds over the space*).
- **All 316 give 814 on the test split, 91% of the gain**, the figure of the
  286 whose proposal named a queue. They are 18 cases short of the full search
  in `T3_ENGINEERING` alone, a queue that escalated 3 times in 316. Reported.

So a deployment can buy the order from a reviewer at the escalations, where
tickets arrive, about as well as from a reviewer of random tickets. It cannot
buy it there for the function, and of the two rules tried for which to label
first, neither beats a random draw.

**What a random audit of the system's decisions buys beside the escalations:
little at a small budget, and mostly one queue.** `PLAN_SPOTCHECK.md` labelled
all 316 escalations and a random draw of the 689 train-half cases rung 1's
engine decided itself, in five nested draws, and read the order between the
escalations alone and the whole train half, from
[`results_spotcheck/FINDINGS_SPOTCHECK.md`](results_spotcheck/FINDINGS_SPOTCHECK.md):

- **Fifty audited decisions add four cases to the escalations' 814** on corpus
  test split 0, at the median of five orders (`N-a` holds, thin). Half of the
  29-case gap to the whole train half's 843 would be 829 (`N-b` refuted).
- **251 audited decisions reach 833** (`N-e` holds, thin), two thirds of the
  gap; 100 reach 826.
- **`T3_ENGINEERING` is learnt all at once or not at all.** At fifty decisions
  the five orders are right on 19, 0, 2, 1 and 13 of the test split's 57 cases
  of that queue (`N-c` refuted, thin). At 251 every draw is right on 13 to 19.
  Read after the verdicts, it is most of what the audit buys: 13 to 19 of the
  14 to 21 cases gained at 251. **[NOTE 2026-10-19, later] Read POST-RUN, the
  class turns on one rule**: *severity 1 on the api product*. On the test split
  it matches 13 cases, all of that queue. In the train half it matches six
  tickets of that queue, all decisions rung 1 got wrong. No order whose labels
  hold none of the six learns the class, and 22 of the 25 with one do. Moved to
  the front, the rule makes every order learn it, at no cost on the test split.
  **[NOTE 2026-10-20] It was alone.** Of the 25 rules no escalation reaches, it
  is the only one whose move to the front pays on the test split, and over the
  space its move loses 820 points (`PLAN_UNREACHED.md`, below).
- **Over the space the audited sets fall below the escalations alone**: 57,890
  of 134,400 points at fifty decisions against 73,020 (`N-d` refuted, thin),
  and 62,905 at 251. The whole train half is at 81,089.
- **Alone, the decisions are worse labels than random escalations and random
  arrivals** on the test split at every budget: 694 at fifty, against 737 and
  717. Reported.

So a reviewer who answers the escalations and audits a few decisions at random
buys little more than the escalations buy. What the audit buys is mostly the
queue the loop never asked about, and per label a decision is worth less than
an escalation where tickets arrive.

**What the rules no label reaches hold: where tickets arrive, the one already
found; over the function, one more.** `PLAN_UNREACHED.md` took the 25 rules no
escalation matches, which rung 3's search leaves where its start put them, and
moved them in the escalations' order: each alone to the front, read with the
truth, and all below every reached rule, without it, beside 100 random
placements of the same rules. From
[`results_unreached/FINDINGS_UNREACHED.md`](results_unreached/FINDINGS_UNREACHED.md):

- **On corpus test split 0, `R0545` was alone.** Its move gains 13 cases, 12 of
  them away from the ticket it was written at. None of the other 21 distinct
  rules gains away from its own (`Z-a` refuted), so they hold nothing of the
  29-case gap to the whole train half (`Z-b` refuted).
- **None of the 25 decides a test case in that order**, so deferring them leaves
  it at 814 (`Z-d` refuted, thin). Random placements of the same rules run from
  798 to 827.
- **Over the space one rule holds the stake.** `R0019`, *keyword and severity 1*
  to `SECURITY_INCIDENT`, gains 5,900 of the 134,400 points at the front, and
  every other distinct rule loses or changes nothing (`Z-c` holds, on it).
  **[NOTE 2026-10-21] Read POST-RUN**: ten rules above the keyword rule's
  highest copy, at place 52, take those points with another queue,
  `T2_TECHNICAL` the most. Three of them decide no escalation.
- **Deferring the 25 gains 1,560 points over the space**, inside the random
  placements' 65,900 to 77,300 (`Z-e` holds, thin). **[NOTE 2026-10-21] Read
  POST-RUN, it is one rule**: `R0459`, the only one of the 25 that decides a
  point of the space there, hands its keyword points to the keyword rule.
- **Every one of the 25 was written at a test-split ticket.** On their own
  tickets, 11 of the 22 distinct rules' moves lose and one gains. Under full
  supervision the five rules left unreached decide nothing. Reported.

So the rules a set of labels never reaches hold, where tickets arrive, only the
rule the reading after `PLAN_SPOTCHECK.md` found, and over the function one
keyword rule. Deferring them buys nothing a reshuffle of them does not.

**[NOTE 2026-10-21] Over the function, orders labelled differently differ in
the keyword half.** Read POST-RUN by `unreached/keyword_half.py`, over the
escalations stage's sets and the audit stage's draws, twelve cells of budget
and arm. In all twelve the order with the most points over the space has the
most on the keyword half. Pooled, that half carries 1.035 of the cells' spread
over the space, and in eleven cells between 0.89 and 1.42 of it. The reading
also found that the curve's reading had the greedy start wrong. The greedy
takes the rules that score zero in birth order while a labelled case is left,
so it does not put the rules no label reaches at the tail. At ten labels the
`SECURITY_INCIDENT` rules the back move defers sat where their ids put them,
and no swap carried them; two sentences carry dated errata. No verdict moves.
[`results_unreached/FINDINGS_UNREACHED.md`](results_unreached/FINDINGS_UNREACHED.md),
*What the keyword holds over the space*.

**The policy, given to the proposer: compiled once it is written whole, and
through the loop it is not.** `PLAN_MANUAL.md` handed the model the policy at
three levels. The levels were a catalogue of what each queue is for, that
catalogue with a prose manual drafted with a real manual's vague words, and the
29 rules as text. Each level, and the bare names beside them, ran in two shapes.
In one, a single answer writes the whole base. In the other, `PLAN_REUSE.md`'s
loop runs with the manual in its prompt. Everything is from
[`results_manual/FINDINGS_MANUAL.md`](results_manual/FINDINGS_MANUAL.md):

- **Compiled once, the model writes the policy.**
  - From the rules it writes it exactly, in all five asks (`G-a` holds).
  - From the prose it reaches 0.9929 of the space at the median. Every ask
    loses the same 960 points of one rule, the one whose threshold the prose
    calls *muchisimos*.
  - From the names alone, 0.5793.
  - Every compiled base crosses, near the hidden policy's own `K-a`.
- **The catalogue buys nothing over the names.**
  - Compiled, the recall of `ACCOUNT_MANAGER` and `T3_ENGINEERING` is no higher
    (`G-b` refuted, thin).
  - In the loop the proposer picks the right queue at 0.3301 against 0.5210
    (`G-f` refuted).
- **Through the loop the same texts decide about a third of the function.**
  - With the rules, 0.3778 over the space against 1.0000 compiled once (`G-d`
    holds), and with the prose 0.3301 against 0.9929.
  - On the arrivals the rules' bases reach 0.6475. The prose's barely move from
    the names', 0.4810 against 0.4545 (`G-e` refuted, thin).
- **With the rules in front of it, the proposer still partitions**, `K-a`
  0.7349 (`G-c` holds). The prose made it cross more.
- **Handed the rules, it applies them at 0.5666 of its escalations.** With the
  prose it names `ACCOUNT_MANAGER` right on 57 of 63, and
  `ONCALL_ESCALATION`, named right when asked, is hardly ever compiled.

So what the loop lacked was not knowledge. Knowledge is ruled out among the
partition's candidates, on this model and these texts, and the elicitation's
remain.

---

## What was withdrawn, and why

The part a reader cannot reconstruct without reading everything in order.

1. **Rung 3's searched order: 0.7713 → 0.8530** (corpus test). The greedy was
   myopic; a multi-start local search recovered 63% of the gap to the bound.
   Cause: the optimizer audit, validated first against a policy whose optimum is
   1.0000 by construction. FINDINGS3 §4 erratum.
2. **Rung 3's 0.9010 stopped being a "ceiling"** and became an upper bound by
   per-case coverage — no order is known to attain it. Cause: re-reading what
   `ceiling()` computes, not a new measurement. FINDINGS3 §1 erratum.
3. **Rung 3's rehabilitation of arrival order was withdrawn.** "born_at already
   scores 0.52" is a corpus artifact: on the space it is *worse* than shuffling,
   0.3148 against 0.3768. Cause: naming the surface for the first time. FINDINGS3
   §1 erratum of 2026-08-08.
4. **Rung 4's "change of regime" in asymmetry was withdrawn**: +0.067 became
   **+0.2011**, the cliff between asymmetry 0.25 and 0.1 vanished, the
   symmetric-to-asymmetric ratio fell from 3.5x to 1.6x. What read as a property
   of the channel was the shape of a weak learner's failure curve. Cause: the same
   optimizer. FINDINGS4 §1 and §5 errata.
5. **Rung 4's "more noise gives better results" is gone.** Falsifying 10% of the
   labels bought +0.060 and now buys +0.0013, inside its spread; the sweep is a
   monotone degradation curve. Cause: the noise was supplying the restarts the
   search lacked. The record diagnosed that mechanism correctly and refused to
   change the method, which is what later made the fix legitimate. FINDINGS4 §4
   erratum.
6. **Rung 3's "at 1% it collapses to 0.5251, the arrival order without searching
   for anything" was withdrawn.** The same greedy, correctly tie-broken, gives
   **0.5732** at 10 labels: that collapse was substantially an artifact of the
   pre-2026-08-06 tie-break, not of the label budget. Measured by running the
   published greedy and the local search side by side against the untouched
   record, which also showed the tie-break to be worth between −0.0166 and
   +0.0481 depending on the fraction — it changes sign twice across the curve.
   Corpus test. FINDINGS3 §4 erratum of 2026-08-13.
7. **Rung 4's anchor cell was not "completely deterministic."** It spreads 0.0111
   across `PYTHONHASHSEED`, and the null test that had ruled tie-break
   instability out permuted a list the argmax never iterated — a true 0.0000 that
   measured nothing. Cause: the tie-break ran over a `set`. Fixed 2026-08-06,
   worth +0.0002, which is what later separated tie-break from algorithm.
   FINDINGS4 §1 and §4 errata.

---

## What is open

Not all of [`IDEAS.md`](IDEAS.md) — the ones that would change a conclusion.

1. **Whether the residue under the coverage bound is slack or search weakness.** A
   search seeing all 134,400 cases still stops 0.0879 below it, down from the
   greedy's 0.1187 — evidence the bound is loose, not proof, since a heuristic
   that misses a bound never distinguishes the two. Exact optimization would
   settle it. FINDINGS3 §4 erratum.
   **[NOTE 2026-10-17] Mostly answered by `PLAN_BOUND.md`, without a solver.**
   A certificate of cases every order loses shows at least 86% of the space's
   pure residue slack, and 78% of its hybrid one (`H-a`, `H-b`). So the search
   is within 0.0123 of the best order on the pure pool and 0.0210 on the hybrid
   one. That remainder is what is open now, and exact optimization is still what
   would split it. On the corpus's train halves the certificate closed less, a
   median of 0.67 of each residue (`H-d` refuted), and 7 to 23 cases a half are
   unresolved.
   [`results_bound/FINDINGS_BOUND.md`](results_bound/FINDINGS_BOUND.md).
2. **Why the proposer partitions instead of stratifying, and why it wrote nothing
   correct for two classes.** Rung 2's mechanism stays unmeasured until a base
   produces conflicts, and the 66.7%/64.2% material gap has no explanation.
   Undiscriminated: the framing (one ticket, one rule), the model, or rule-writing
   elicitation in general. FINDINGS2, "Why this is NOT a capability failure".
   **[NOTE 2026-09-30]** At n=2000 the base does produce conflicts, and the
   proposer's declared edges were accepted in every run of `PLAN_REUSE.md`'s
   Stage B. So the mechanism has material now. What those edges buy has not been
   measured.
   **[NOTE 2026-10-05] Measured by `PLAN_EDGES.md`.** On the arrivals the edges
   were right on a third of the cases they decided. Over the function their
   direction was right three times in four. Nearly all of it is one rule about
   the security keyword, the attribute the two surfaces weigh most differently.
   What is open now is whether declaration at write time carries direction
   beyond that one attribute.
   [`results_edges/FINDINGS_EDGES.md`](results_edges/FINDINGS_EDGES.md).
   **[NOTE 2026-10-06] Imposing the declaration made the proposer partition
   more, not less** (`PLAN_AUTHORSHIP.md`, `E-e`). That does not tell the three
   candidates apart. It does leave the third form of the second way without a
   verdict over the space: whether imposed declaration supplies order needs a
   protocol that keeps the proposer overlapping, and none has been written.
   [`results_authorship/FINDINGS_AUTHORSHIP.md`](results_authorship/FINDINGS_AUTHORSHIP.md).
   **[NOTE 2026-10-07] Written and run as `PLAN_OVERLAP.md`.** Told that overlap
   is normal, the proposer still partitioned in two runs of three (`O-a`). Where
   it overlapped, its declarations ordered the function through the keyword rule
   of thumb (`O-b`, `O-c`, read POST-RUN). What is open now is what `PLAN_EDGES.md`
   left: whether declaration carries direction beyond that one attribute. Under
   v2e, four strict pairs went one right.
   [`results_overlap/FINDINGS_OVERLAP.md`](results_overlap/FINDINGS_OVERLAP.md).
   **[NOTE 2026-10-12] Answered by `PLAN_BLIND.md`, and the partition's cause
   with it.** Drafted with the base out of view, the proposer crossed (`K-a`),
   the cause `FINDINGS2.md` named; the framing of one ticket and one rule does
   not stop it. Beyond the keyword its declarations point at the better rule
   about one time in two, below a fixed ranking of the queues (`K-b`, `K-c`,
   `K-e`), and their fill is mostly resolution (`K-d`, read POST-RUN). So it
   partitions when it sees the base, and it does not stratify when it does not:
   its declarations carry no direction a ranking lacks. The two missing classes
   are untouched: no declaration changes which queue the model writes.
   [`results_blind/FINDINGS_BLIND.md`](results_blind/FINDINGS_BLIND.md).
   **[NOTE 2026-10-18] The ranking those declarations lose to read a key.** Asked
   for its own ranking, the model states a priority order that points `K-b`'s
   pairs no worse than its declarations, by a hair (`M-e` holds, thin). As an
   arbitration order it loses to a blind draw on the corpus (`M-b`, `M-c`
   refuted). *A direction a ranking lacks* is measured against the key's ranking,
   and the model holds no ranking that good.
   [`results_ranking/FINDINGS_RANKING.md`](results_ranking/FINDINGS_RANKING.md).
   **[NOTE 2026-10-21] Knowledge is ruled out as the partition's cause, and one
   of the two classes is a matter of it.** `PLAN_MANUAL.md` gave the model the
   policy as text.
   - With the 29 rules in front of it, the loop's proposer still partitions
     (`G-c` holds).
   - Asked for the whole base in one answer, the same model writes the policy
     exactly (`G-a` holds), and every base it compiles crosses.
   - So the partition belongs to the loop's elicitation: the three candidates of
     `ARBITRATION_REPORT.md` §5 remain, and knowledge does not join them.
   - With the prose, the proposer names `ACCOUNT_MANAGER` right at nearly
     every escalation of the class, so that class was knowledge.
   - `T3_ENGINEERING` stays low in the loop at every level, and compiled once
     it is whole.
   - What is open now is why the elicitation partitions, and why the loop loses
     what it knows.
   [`results_manual/FINDINGS_MANUAL.md`](results_manual/FINDINGS_MANUAL.md).
3. **~~ILP as a competitor.~~ Run on 2026-08-30**, opened by Sergi and
   pre-registered as `PLAN_ILP.md`. Not Popper or ILASP — neither is installable
   here — but sequential covering over a declared language, gated by an `I-g1`
   that recovers the hidden policy exactly. **On the material the proposer had it
   beats an oracle-using search over the LLM's 577 rules by 0.0342 on the
   arrivals and loses to it by 0.17 as a function.**
   [`results_ilp/FINDINGS_ILP.md`](results_ilp/FINDINGS_ILP.md). What is left open
   is narrower: `ONCALL_ESCALATION` never escalated once, so what the loop never
   asked about, no method can learn. **[NOTE 2026-09-30]** `U-d` settles whose
   property that is: a loop that escalates on coverage never asked about it either,
   in three runs. What is open now is a trigger that would ask, and none is
   specified. **[NOTE 2026-10-04]** The queue is in the model: asked without a
   screen of compiled rules, it names `ONCALL_ESCALATION` on all seven tickets
   (`F-f`). And disagreement with a fresh answer is not that trigger, since it
   finds the rules' errors in one run of three. **[NOTE 2026-10-10]** On the
   proposer's tickets, not its labels: the inducer was handed the true queue of
   every example, and the proposer chose its own, right on 245 of 632. The
   inducer that wins by 0.0342 was trained on all 632, which reach 371 of the
   test split's 995 cases with their true label. No figure and no verdict moves;
   the reading of that win does. §5's erratum of
   [`results_ilp/FINDINGS_ILP.md`](results_ilp/FINDINGS_ILP.md).
   **[NOTE 2026-10-10, later]** Measured, POST-RUN: all of the 0.0342 is on
   those 371, where the inducer is right on all and the order on 337. On the
   other 624, which neither had labelled, they tie at 506, right on different
   cases. §7 of the same record. **[NOTE 2026-10-10, later still]** The control,
   POST-RUN: the same inducer trained on the queues the proposer chose scores
   424 and 437 of 995. That is below the proposer's own rules in arrival order,
   519, which use no truth either; its bet that the inducer would compile the
   proposer's answers better failed. On `ACCOUNT_MANAGER` it scores 0 of 55.
   §8 of the same record.
   **[NOTE 2026-10-18] A regularised student of the same answers loses to the
   rules too, and reaches the rare queue they miss.** `PLAN_STUDENTS.md`'s
   pruned tree on the 579 answers is right on 470 of 995, below the rules in
   arrival order, 519; over the space it is right on 59,466 points against
   their 42,310 (`T-a`, `T-c`). Its leaves send severity-1 tickets to
   `ONCALL_ESCALATION`, learned from the 7 answers that named that queue on
   other tickets. They decide its three test cases right, where no execution
   of the rules decides more than two. So the queue the loop never asked about
   was in its answers to tickets it did ask about. What those leaves cost on
   other severity-1 tickets is not counted. **[NOTE 2026-10-18, later] Counted,
   POST-RUN**: 17 test cases against arrival order, so on both surfaces the
   trade is a loss.
   [`results_students/FINDINGS_STUDENTS.md`](results_students/FINDINGS_STUDENTS.md).
   **[NOTE 2026-10-21] Given the policy, the loop asks about the queue and still
   does not compile it.**
   - Under `PLAN_MANUAL.md`'s rules and prose, `ONCALL_ESCALATION` tickets did
     escalate, and the proposer named the queue right on 15 of 18.
   - In those six runs the rules then decided a later ticket of the class right
     once.
   - Compiled in one answer, from the names alone or from any manual, the model
     put the whole region right every time.
   - So the queue is in the model and the trigger is not the whole gap: what
     the loop writes after asking loses it too.
   [`results_manual/FINDINGS_MANUAL.md`](results_manual/FINDINGS_MANUAL.md).
4. **~~Fidelity: whether a compiled rule decides a later case the way the model
   would have.~~ Measured on 2026-10-04**, pre-registered as `PLAN_FIDELITY.md`.
   **The rules decide unlike the model would, and compiling loses it nothing on
   the cases they decide**; most of their error is the model's own.
   [`results_fidelity/FINDINGS_FIDELITY.md`](results_fidelity/FINDINGS_FIDELITY.md).
   What is left open is what the thread found beside its rows. **The model's
   screen of compiled rules seems to cost it accuracy**, and the rarest queue,
   which it names on every ticket without that screen. That was measured on 100
   cases a run with one answer each, so it is a sign rather than an effect, and
   measuring it would cost calls.
   **[NOTE 2026-10-15] Measured by `PLAN_SCREEN.md`, and it is deference.**
   Without its screen the model is right more often on decisions nobody had
   asked without one (`V-b`). The screen pulls its answer to the screen's
   commonest action (`V-c`), which helps where that action is right and costs
   where it is wrong (`V-d`). On these bases it is wrong about seven times in
   ten. With the ticket alone, both answers named the rare queues on every
   ticket again. What is open now is why the model defers, and whether a base
   right more often would turn the cost into a gain.
   [`results_screen/FINDINGS_SCREEN.md`](results_screen/FINDINGS_SCREEN.md).

---

## What this does not show

**The original hypothesis — do the LLM's rules get reused, or does it memorize
cases? — was measured on 2026-09-30, and it is not clean in the one sense rung 1
was voided for.** It is the question the project was built to answer.

> **[ERRATUM 2026-09-30] The sentence above read *has still never been measured
> cleanly*.** That was true from rung 1's voided run of 2026-08-05 until
> `PLAN_REUSE.md`'s Stage C. That plan asked the question at the horizon it was
> posed at, n=2000, on rung 2's engine, whose ceiling is 1.0000 on both surfaces.
> It asked three times, with the two error axes separated and this horizon's
> memorization floor beside the result. **In the terms signed on 2026-08-05 the
> answer is *reused*:** 0.7381 on the median, far above the 0.30 threshold and the
> 0.1176 floor below.
>
> **It is not clean in the sense rung 1 was voided for; that problem was reduced,
> not removed.** A median 0.2857 of the escalations were CONFLICT, against rung
> 1's 94%, so part of what escalated was the arbitration. §0 of that plan fixed
> this in advance as a caveat on the reading, not on the verdict.
>
> **And the answer is not the one the project was built to hope for.** The rules
> are reused and mostly wrong; most of their errors are born with them; the rarest
> queue is never asked about. See
> [`results_reuse/FINDINGS_REUSE.md`](results_reuse/FINDINGS_REUSE.md) and *What is
> established* above. The erratum of 2026-09-29 below says *the headline of this
> section still stands*; it did when it was written, and this one supersedes it.

Rung 1's **0.158 reuse** describes the arbitration, not the induction: 594 of its
632 escalations (94%) were CONFLICT, exactly what specificity-based arbitration
overproduces, and reuse, rule count, dead rules and the escalation curve are all
products of that loop ([`PREDICTION.md`](PREDICTION.md), "Why the stopping
threshold does not apply"). The engine ceiling underneath it was 0.5875.

Rung 2 built an engine with a 1.0000 ceiling, and then the change that made
declared priority possible — showing the proposer the base — is the one that left
it without material: 2 conflicts in 8 runs.

> **[ERRATUM 2026-09-29] That paragraph ran two kinds of material together, and
> rung 2 had one of them.** It has read this way since `8487a63` wrote it on
> 2026-08-09, two days after the eight n=100 runs were committed. Rung 2 had no
> material for *declared priority*, which needs conflicts. It had all it needed
> for *reuse*, which does not: a rule is reused when it decides a later case, and
> 153 of the eight runs' 155 escalations were coverage impasses under the 1.0000
> engine. `rung2/run2.py` wrote the figure into every record and no record read it
> until [`results2/FINDINGS2.md`](results2/FINDINGS2.md), *Caveats*, took the
> eight rows today: **reuse 0.60 to 1.00, above the 0.30 of the stopping threshold
> in [`PREDICTION.md`](PREDICTION.md) in all eight — with silent error 0.51 to
> 0.89, and a proposer that chose the right queue for the ticket in front of it
> 0.20 to 0.43 of the time.**
>
> **The headline of this section still stands, and both are true.** The rules get
> reused, in the terms the question was signed in, at a hundred cases in this
> configuration; and the question has still not been measured cleanly. A hundred
> cases is a twentieth of the horizon, the memorization floor below exists only at
> n=2000, and the figure mixes the two error axes `CLAUDE.md` Step 5 keeps apart —
> which is why reuse that high beside silent error that high reads as the
> partition [`CHAT_SUMMARY.md`](CHAT_SUMMARY.md) §1 described, not as induction.
> The section said only the second half. No other figure in this file moved.

Whatever measures it next must clear the memorization floor: `keep_k(k=8)`
reaches **0.1176** reuse without inducing anything, purely from the corpus's
12.8% duplicates ([`results/frontier.json`](results/frontier.json)). A figure near
0.118 is noise.
