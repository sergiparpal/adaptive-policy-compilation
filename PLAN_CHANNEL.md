# PLAN_CHANNEL — the loop with reasoning on, under a trigger a deployment could have: half its errors reported, beside the error arm again

**Status: drafted by Claude on 2026-11-04, unsigned.** Corrected before
signature on 2026-11-05, where the package written to it showed the draft
inexact; each correction is dated in place, and no row and no line moved. Under
hard rule 2 of `CLAUDE.md` a model may draft a band and may not sign it. **Nothing runs and no
record is written until Sergi has signed §0.** The signature has to land before
any figure named here exists, in its own commit, staged by name. That includes
Stage A, which spends nothing: §11 says why.

**Asked for by Sergi on 2026-11-04**, on the item
[`STATUS.md`](STATUS.md)'s *What is open* ends its third item on, and
[`IDEAS.md`](IDEAS.md) carries first under *What `PLAN_REASONED_LOOP.md` opens*:
*a trigger a deployment could have*. Two choices were his before this was
drafted, each made after the drafter showed him the free reading below:

- **The trigger is rung 4's feedback channel at coverage 1/2.** A decision the
  base gets wrong is reported with probability 1/2, at once, and a decision it
  gets right never is: asymmetry 0, delay 0, noise 0
  ([`rung4/feedback.py`](rung4/feedback.py)). He chose that coverage over 1/4.
- **The second arm is the error arm again, not a second coverage.** Three new
  runs of `PLAN_REASONED_LOOP.md`'s error arm alternate with the channel's, so
  that the plan's comparison is made within one period.

**The item.** `PLAN_REASONED_LOOP.md` ran rung 2's loop with level 3's manual
and reasoning on, under two triggers
([`FINDINGS_REASONED_LOOP.md`](results_reasoned_loop/FINDINGS_REASONED_LOOP.md)).

- **Asked also where its base decided wrongly, it compiled the policy.** The
  error arm's median base decides 0.9601 of the space right (`RL-d`, held
  thinly), and recalls 14/15 of `ONCALL_ESCALATION` (`RL-g`, held thinly).
- **Under the standing trigger it did not.** The impasse arm's median base
  decides 0.4614 of the space, and no impasse run recalls any of the rarest
  queue.
- **The error trigger reads the label of every arrival**, as no deployment
  could. A deployment hears of some of its errors, late or noisily: a ticket
  sent to the wrong team is reassigned, and not every one is. Rung 4 called that
  trigger's cell *the best possible case of a realistic channel, with feedback on
  every error and none lost* (`FINDINGS4.md` §1): a deployment has it only if
  every misrouted ticket is reassigned.

**What the drafter found before drafting, and why these two arms.** All of it is
free, and none of it reads an answer this plan buys.

- **The transcriber under rung 4's coverages.** `PLAN_REASONED_LOOP.md`'s
  transcriber is a double that writes, at every escalation, the rule of level
  3's text that governs the ticket, and places it by the text's order. Run
  through that plan's loop with the error trigger thinned to a coverage `c`,
  over 50 draws of the channel at each coverage of rung 4's sweep, delay 0:

  | coverage | escalations, median [range] | `space`, median [min–max] | draws with `ONCALL` whole / none | `SECURITY` whole / none |
  |---|---|---|---|---|
  | 1, the error arm | 23 [23–23] | 0.9999 [0.9999–0.9999] | 50 / 0 | 50 / 0 |
  | 1/2 | 23 [22–23] | 0.9999 [0.9842–0.9999] | 43 / 0 | 50 / 0 |
  | 1/4 | 22 [19–23] | 0.9842 [0.6092–0.9999] | 17 / 2 | 39 / 1 |
  | 1/10 | 20 [17–23] | 0.8530 [0.5217–0.9842] | 2 / 19 | 21 / 6 |
  | 1/20 | 17 [13–21] | 0.7931 [0.4586–0.9405] | 0 / 33 | 6 / 17 |
  | 1/50 | 14 [9–18] | 0.5164 [0.3110–0.7967] | 0 / 41 | 0 / 31 |

  A proposer that never errs needs one report per rule of the list, and at
  coverage 1/2 it nearly always gets it. At 1/4 the channel's luck alone moves
  it from 0.61 to 0.9999 of the space.
- **Delay barely moves the final base.** At coverage 1, delays of 50 to 400
  cases left every draw's base unchanged. At 1/4 they lowered the median from
  0.9842 to between 0.9686 and 0.9561. In that reading a delayed report
  escalated its ticket only if the base still misrouted it when the report
  arrived, and a report due after the last case was lost.
- **The loop's proposer is not the transcriber: it asked again where the
  transcriber asked once.** `PLAN_REASONED_LOOP.md`'s error runs escalated on
  62, 80 and 100 errors, against the transcriber's 21. Where tickets are many
  that costs nothing: under the standing trigger each base decided 379 to 590
  arrivals wrongly. Where they are few, the error arm used up most of them:

  | governing rule | queue | its tickets in the corpus | the transcriber's error escalations | the error runs' (r1 / r2 / r3) |
  |---|---|---|---|---|
  | `H04` | `ONCALL_ESCALATION` | 4 | 1 | 2 / 4 / 3 |
  | `H05` | `ONCALL_ESCALATION` | 3 | 1 | 1 / 2 / 3 |
  | `H01` | `SECURITY_INCIDENT` | 9 | 1 | 6 / 5 / 4 |
  | `H02` | `SECURITY_INCIDENT` | 11 | 1 | 6 / 1 / 6 |
  | `H06` | `T3_ENGINEERING` | 8 | 1 | 5 / 2 / 1 |

  A channel at coverage 1/2 can report at most half of those tickets, in
  expectation.
- **`SECURITY_INCIDENT` is 3/8 of the space and 1% of the arrivals.** Its 50,400
  points are more than any other queue's; its 20 tickets fewer than any but
  `ONCALL_ESCALATION`'s 7. The error run whose base decided least of the space,
  0.8898, recalled 0.7667 of it.

So a channel at half coverage costs a proposer that never errs almost nothing,
and the question is what it costs this proposer, which asks again where tickets
are few. **Coverage 1/2 is chosen so that what the loop loses is the loop's, not
the channel's**: at 1/4, three runs could not tell the proposer from the draw.
**The error arm is run again so that the comparison is not made across dates**:
`PLAN_SCREEN.md` found the model's answers moved between two dates, and a plan
that compares across dates should ask both arms on one day where it can
(`CLAUDE.md`). It also replicates `RL-d` and `RL-g`, both of which held thinly.

**The question, in its cleanest form.** With level 3's manual in the prompt,
reasoning on, and v1b's placement round:

- does a loop that hears of half its errors compile the policy?
- how much of what the error arm compiles does it lose, within one period?
- does it compile the rarest queue?
- does the error arm compile the policy again, on a new period?
- does hearing of half the errors halve the calls?

**Two arms.** Both run `PLAN_REASONED_LOOP.md`'s loop on rung 2's engine, at
n=2000 and seed 17, three runs each, under one protocol, **v1b**, unchanged, with
reasoning on. The arms alternate.

- **The channel arm, `c`**, escalates a case on an IMPASSE or a CONFLICT. It
  also escalates a case the engine decides with a queue other than its label,
  **when that case's draw falls below 1/2**.
  - Every case has one draw, fixed before the run from a string seed (§2.1). A
    draw belongs to a case whether or not the base decides it wrongly, so a
    run's reportable cases are fixed before it starts, and about half of them.
  - The trigger reads the truth of the arrival, as the error arm's does. The
    proposer is handed no label, and is not told that the decision was wrong.
- **The error arm, `e`**, is `PLAN_REASONED_LOOP.md`'s error arm: it escalates
  every case the engine decides with the wrong queue. It is the channel at
  coverage 1, and this plan's loop at coverage 1 is that plan's loop (`CH-g1`).
  It is a reference no deployment has. That is what makes it a clean comparator,
  as `EXTERNAL_REVIEW.md` §1.5 says of `keep_k`'s hint.

The arms send the same prompts. They differ only in which wrong decisions they
ask about.

**What it changes in what is measured, said first.**

- **The channel arm reads the label of every arrival, and acts on half of the
  wrong ones.** In a deployment the world would supply the report, a ticket
  reassigned; here the corpus labels stand in for it, as rung 4's channel read
  the oracle. What reaches the loop is strictly less than the error arm's: the
  wrong decisions whose draw is below 1/2, and nothing about the rest or about
  the right ones.
- **Both arms break rung 2's invariant on purpose**, as `PLAN_REASONED_LOOP.md`'s
  error arm did. `ARBITRATION_REPORT.md` §3, level 3: *"The escalation trigger is
  only coverage or conflict, never 'the answer was incorrect'"*, and that is what
  makes the silent error measurable.
  - The same section calls the conflict count *"the only instrument a deployed
    system has for knowing it is lost"*. A ticket reassigned by the team that
    received it is another instrument a deployment has, and rung 4 modelled it
    (`FINDINGS4.md` §2). This plan asks what the loop compiles when that
    instrument hears of half its errors.
  - The channel arm's silent errors are its unreported wrong decisions, and the
    record counts them.
- **This channel is poorer than rung 4's.** There a reassignment *brings the
  correct action* (`FINDINGS4.md` §2). Here a report only makes the loop ask,
  and the proposer is handed the ticket alone. An unreported wrong decision
  stands exactly as a right one does: nothing the loop or the proposer sees
  separates them, as rung 4 declared of silence.
- **Coverage is rung 4's**, the probability that a wrong decision is reported.
  It is not a rule's coverage, nor `cover(r)`, nor rung 3's coverage bound.
- **No rung-4 figure is an expectation here.** Rung 4 learned an order offline
  over rung 1's fixed 577 rules, and what a feedback channel would extract from
  other material is unmeasured (`ARBITRATION_REPORT.md` §5 and §9.5). It has no
  audited figure at this plan's cell. What carries is a property of the channel,
  which its audit left standing: the volume of reports is proportional to the
  observed system's error rate, and falls as the system improves
  (`FINDINGS4.md` §3).
- **In `CHAT_SUMMARY.md` §1's terms**, priority enters only through an external
  channel: declaration, feedback or authority. Both arms hold the authority
  channel, the manual, and use feedback only to ask. Neither the order nor the
  queue comes through it, and no row separates the two.
- **The error arm's new runs are not `PLAN_REASONED_LOOP.md`'s runs.** They are
  its protocol on new dates. `CH-b`, `CH-d` and `CH-e` read this plan's runs
  only; the two periods are set side by side in `CH-g`, and that comparison is
  reported, never adjudicated.
- **v1b's two defects are kept on purpose.** Read POST-RUN in that plan's record,
  its placement round lists rules nested with the draft, which the system
  prompt says need no declaration, and lists rules whose conflict with the draft
  the base already decides. Mending either would make the protocol differ from
  the error arm it is compared with across plans, and the trigger would no
  longer be the only change. Both arms here carry both defects alike.
- **Reasoning is on**, as in `PLAN_REASONED_LOOP.md`, against `PLAN_REUSE.md`
  §1's amendment, for this plan's calls only.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**The runs.** `R = 3` runs per arm. Each run is `PLAN_REUSE.md`'s loop over the
2,000 cases of `generate_corpus(2000, seed=17)`, with a fresh rung 2 engine,
under v1b. The arms alternate, as §2.3 sets.

**The statistics.** Each is a ratio of integer counts. **Each is compared with its
line exactly, as a fraction.** No rounding enters a verdict.

- **`B`, a run's final base.** Its rules, and the edges the engine accepted,
  rebuilt from the record. `CH-g1` holds the rebuilt base to the engine the run
  ended with, and Stage C to the rules and edges the record says it ended with.
- **`space(B)`.** `PLAN_MANUAL.md`'s statistic: the share of the 134,400 points
  of the exhaustive space that `B` decides right under rung 2's engine. A
  CONFLICT or an IMPASSE is not right. It is computed by
  `manual.instrument.over_space`.
- **`recall_q(B)`.** Of the points whose true queue is `q`, the share `B` sends to
  `q`. The same function computes it.
- **`calls(r)`.** The calls run `r` made: one per escalation, and one per
  placement round sent. An attempt retried inside a call is not another call.
- **The median** of three runs is the middle one, and of two runs their mean.

**The unit, *thin*, and when a row has no value.** All of it is settled here and
not in the scorer, which is where `PLAN_AUTHORSHIP.md`'s `E-c` lost its verdict.

- **Every adjudicated row reads medians over an arm's runs.**
- **A verdict is labelled *thin*** when any one run of an arm the row reads, put
  in place of that arm's median, would put the statistic on the other side of
  its line. That is `PLAN_MANUAL.md`'s test. The label does not change the
  verdict.
- **What a spread between runs as wide as a line does.** `PLAN_REASONED_LOOP.md`'s
  error runs decided 0.8898 to 0.9635 of the space: a spread of 0.0737, wider
  than `CH-b`'s line. So `CH-b`'s verdict may well be thin whichever way it
  falls, and *thin* is how the record says so. No line was widened to absorb
  that spread, and none will be.
- **What one run does to `CH-c`.** Run `c r2`'s draws make no `H05` ticket
  reportable, so none can escalate there on an error, and under the standing
  trigger no ticket of the queue ever escalated otherwise. `H05` governs a third
  of the queue's points; the transcriber recalls 2/3 of the queue under those
  draws.
  Unless the proposer writes `H05`'s region from another ticket, `CH-c` holds
  only if `c r1` and `c r3` both reach its line.
- **A run is complete** when it reaches case 2,000, or the cap of §1.
  - A run that cannot be completed leaves its arm with fewer runs. The rows read
    the runs that exist, and the record names the missing one.
  - A row that reads an arm with fewer than two runs has no value.
- **A row with no value is unadjudicable**, and the record says so.

**Which side had the label**, for every arm and reference. This was checked
against the prompts and the code while drafting, and not recalled, as `CLAUDE.md`
asks of any plan that sets a comparison on the proposer:

| who | what it is handed | reads a label? |
|---|---|---|
| the proposer, both arms | the 29 rules in order, under *"Se aplica la primera regla de la lista cuyas condiciones casa el ticket."* | **yes, in effect**: every ticket's label is derivable from the text by first match (`PLAN_MANUAL.md` §6.2) |
| the error arm's trigger | the truth of every arrival, read from the corpus labels | **yes**, but only whether the base's decision is right. It is never handed to the proposer, and the proposer is not told why it was asked (§6.1) |
| the channel arm's trigger | the truth of every arrival, and one draw per case fixed before the run | **yes**, whether the base's decision is right, and it acts only where it is wrong and the draw is below 1/2. Nothing of it reaches the proposer |
| the transcriber references (§5.4) | level 3's text, applied by first match; the truth and the draws, as its arm's trigger reads them | yes |

- **No arm sees an example.** The loop sees the arrivals as they come, as every
  loop has.
- **No baseline is fitted to the proposer's answers.** The references are
  mechanical, and they read the text, the truth or the draws, never an answer.

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **CH-a** | **Half the reports compile the policy.** A loop that hears of half its errors compiles it within a tenth of the space | the median over `c`'s runs of `space(B)` | **≥ 0.90** | **< 0.90** |
| **CH-b** | **Halving the reports costs at most a twentieth of the function**, within one period | the median over `e`'s runs of `space(B)`, less the median over `c`'s runs | **≤ 0.05** | **> 0.05** |
| **CH-c** | **Half the reports compile the rarest queue** | the median over `c`'s runs of `recall_ONCALL_ESCALATION(B)` over the space | **≥ 0.90** | **< 0.90** |
| **CH-d** | **The error arm compiles the policy again**, on a new period: `RL-d` replicated | the median over `e`'s runs of `space(B)` | **≥ 0.90** | **< 0.90** |
| **CH-e** | **And the rarest queue again**: `RL-g` replicated | the median over `e`'s runs of `recall_ONCALL_ESCALATION(B)` over the space | **≥ 0.90** | **< 0.90** |
| **CH-f** | **Hearing of half the errors does not halve the calls** | the median over `c`'s runs of `calls(r)`, over the median over `e`'s runs | **≥ 3/4** | **< 3/4** |
| **CH-g** | *Reported, not adjudicated.* **What the drafter could not band** | Every run of both arms on every surface: `space` whole and on each keyword half, `corpus(B)` read whole, the recall of all eight queues on both surfaces, `K-a`, and `cover(r)`. `PLAN_REUSE.md`'s online set per run, with escalations by cause (impasse, conflict, error). For the channel arm, the wrong decisions by whether their draw reported them, and the reported ones by whether they escalated: by queue, by governing rule and over time. Each channel run beside the transcriber under its own draws, and each error run beside the transcriber under the error trigger. The error escalations by governing rule in each run, beside the corpus tickets of that rule and the reportable ones. Every escalation's verdict, with its finish reasons. The placement rounds: the sizes of their lists, citations of `H01` to `H29`, and edges by the engine's verdict. `RL-e`'s direction and the Stage C ranking's on this plan's runs, by arm. This plan's error runs beside `PLAN_REASONED_LOOP.md`'s, figure by figure, across dates. The calls: providers, finish reasons, tokens, reasoning tokens over the attempts that reached the model, seconds by round, and retries by cause. The reasoning, recorded whole and not coded | — | — |

**Signed by Sergi: ________ (date: ________)**

**Why each row, and why these lines.**

- **`CH-a` is `RL-d`, on the channel arm.** Its statistic and line are `RL-d`'s,
  so that a reading here and `RL-d`'s there mean the same thing: within a tenth
  of the space of compiling the policy once (`G-a`).
- **`CH-b` is the plan's comparison.** The arms differ in which wrong decisions
  they ask about and nothing else, within one period, under one provider.
  - **The line is a twentieth, half of `RL-c`'s tenth.** `RL-c` asked whether a
    trigger is the limit, and a tenth was its line. This asks whether halving a
    trigger's reports costs little, which is a finer claim.
  - **The transcriber's own cost is far below it.** Under this plan's draws the
    transcriber loses nothing in two runs and 2,100 points, 0.0156, in the
    third. So a twentieth leaves the loop about three times the channel's worst
    cost to a proposer that never errs.
  - **A hold does not rule out a cost of that size.** With three runs an arm
    and a spread between runs of 0.07, the instrument could not see one. The
    record says so beside the verdict, whichever it is.
- **`CH-c` is `RL-g`, on the channel arm.** Its statistic and line are `RL-g`'s.
  Read *What one run does to `CH-c`*, above, before reading the verdict.
- **`CH-d` and `CH-e` are `RL-d` and `RL-g`, on a new period.** They make
  `CH-b`'s comparator this plan's own runs, and they test whether two thin holds
  replicate. Their lines are those rows' lines.
  - **Their bands were drafted after the first period's figures were seen.**
    What they pre-register is the new period's figure, which does not exist
    (`EXTERNAL_REVIEW.md` §5.6). But a replication surprises its author less
    than a first measurement, and `EXTERNAL_REVIEW.md` §3 asks that such a
    difference be recorded rather than assumed: the scoreboard should read their
    verdicts as replications.
- **`CH-f` reads what the deployment pays.**
  - **If the calls followed the reports**, hearing of half the errors would halve
    them, and the ratio would be near 1/2. **If they followed the repairs the
    base needs**, a report that does not come now comes later, from another
    wrong decision in the same region, and the ratio would be near 1.
  - **Rung 4's §3 is the mechanism for the second.** With asymmetry 0 the volume
    of reports is proportional to the observed system's error rate. A base that
    repairs more slowly keeps erring, and so keeps being reported.
  - **The line is the midpoint, 3/4.**
  - **The transcriber reads 1**: 45, 43 and 45 calls under the channel's draws,
    against 45 under the error trigger.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **`CLAUDE.md`**, whole.
- **`STATUS.md`**: the list of its sections; *What is open*, with every dated
  note in it; the scoreboard's opening and its totals row. Not *What is
  established*, nor *What was withdrawn*, nor *What this does not show*, nor the
  scoreboard's table.
- **`IDEAS.md`**:
  - its header, *Pending and already specified*, and *What
    `PLAN_REASONED_LOOP.md` opens*;
  - *What the outside reading of October 2026 proposes*, from its opening to
    the end of its proposals, and *What `ARBITRATION_REPORT.md` §7 proposes*;
  - *Technical debt*;
  - the titles of the items in every other section.
- **The reasoned-loop thread.**
  - `PLAN_REASONED_LOOP.md`: its opening, §0 to §4, §5.1 to §5.4, §5.6, and §6
    to §13. Not §5.5 whole: its resume and its two amendments were read in
    `reasoned_loop/plan.py`'s account of them.
  - `FINDINGS_REASONED_LOOP.md`: its opening, to its third dated note; its table
    of runs with their dates, calls and costs; and the lines on the pace and on
    the transcriber's figures that §1 and §3 cite.
- **The three analytical documents `CLAUDE.md` asks a new one to read first,
  and `results4/FINDINGS4.md`.** A subagent of the drafter read all four whole
  for this plan, with `CHAT_SUMMARY.md`'s errata, and reported every passage
  bearing on it with its place. The drafter read directly the passages this plan
  rests on:
  - `ARBITRATION_REPORT.md` §3's level 3, on the trigger and the error
    detector; its reservation in §5 that neither a searched order nor
    feedback's figure travels with a new base; §9.5; and §7's P1, on a result
    between floor and distribution;
  - `CHAT_SUMMARY.md` §1;
  - `EXTERNAL_REVIEW.md` §1.5's paragraph on `keep_k`'s hint, §3's paragraph on
    figures seen before a band, and §5.6;
  - `FINDINGS4.md` §1's lines on its cell at coverage 1 and asymmetry 0, and §2
    and §3 whole, with their erratum and note;
  - `rung4/feedback.py`'s `observe`, whole.

  The subagent also reported that no rule in the four documents bears on thin
  rows, medians of three runs or providers. Those rules are `CLAUDE.md`'s, and
  this plan follows them there.
- **The code read.**
  - `reasoned_loop/loop.py` and `reasoned_loop/references.py`, whole.
  - `reasoned_loop/plan.py`'s constants, its gate's account and `labels`.
  - `manual/instrument.py`'s `over_space` and `over_corpus`.
  - `rung4/feedback.py`'s account of its parameters and its `Channel`, and
    `rung4/sweep.py`'s grid.
  - `tests/test_prose_tables.py`'s `THREADS`.
- **Records read for a figure.**
  - `results_reasoned_loop/sample.json`: the rare queues' tickets and the
    transcriber's figures.
  - `results_reasoned_loop/score.json`: `RL-c`, `RL-d` and `RL-g` by run, and
    `RL-h`'s runs: their `space` whole and by keyword half, their recall by
    queue, their escalations and calls.
  - `results_reasoned_loop/loop_{i,e}_r{1..3}.json`: each case's cause, its
    governing rule, and whether a decision that stood was right.
- **Figures computed while drafting**, by scripts kept outside the tree. Stage A
  recomputes the first six, and its record will own them. None of them reads an
  answer this plan buys.
  1. **The rare queues' tickets.** `ONCALL_ESCALATION` has 7, at cases 257, 710,
     954, 982, 1432, 1783 and 1951; `H04` governs 4 of them and `H05` 3.
     `SECURITY_INCIDENT` has 20; `H01` governs 9 and `H02` 11.
  2. **The space by true queue.** Of the 134,400 points, `SECURITY_INCIDENT`'s
     are 50,400; `T2_TECHNICAL`'s 36,720; `ACCOUNT_MANAGER`'s 16,440;
     `T3_ENGINEERING`'s 8,180; `BILLING_SPECIALIST`'s 6,840;
     `ONCALL_ESCALATION`'s 6,300; `T1_GENERAL`'s 5,220; `SELF_SERVICE_DEFLECT`'s
     4,300.
  3. **The channel's draws, by run.** The seeds were fixed by rule before any
     draw was computed (§11), and these are the first and only draws computed
     under them; no seed was tried and set aside.

     | run | reportable cases | reportable `ONCALL_ESCALATION` tickets | by rule | reportable `SECURITY_INCIDENT` tickets | by rule |
     |---|---|---|---|---|---|
     | `c r1` | 1,000 of 2,000 | 3 of 7: cases 257, 1432, 1951 | `H04` 2 of 4, `H05` 1 of 3 | 11 of 20 | `H01` 5 of 9, `H02` 6 of 11 |
     | `c r2` | 1,025 | 2: cases 954, 1951 | `H04` 2, `H05` 0 | 12 | `H01` 6, `H02` 6 |
     | `c r3` | 1,015 | 3: cases 710, 1432, 1951 | `H04` 2, `H05` 1 | 12 | `H01` 5, `H02` 7 |

  4. **The transcriber under the channel arm, by run.**
     - `c r1` and `c r3`: 23 escalations, 2 impasses and 21 errors; 45 calls;
       134,380 points of the space, and 1,999 arrivals read whole.
     - `c r2`: 22 escalations, 2 impasses and 20 errors; 43 calls; 132,280
       points, and 1,996 arrivals. It recalls 2/3 of `ONCALL_ESCALATION`: no
       `H05` ticket is reportable, and `H05` governs 2,100 of the queue's 6,300
       points.
  5. **The transcriber under the error arm**: 23 escalations, 45 calls and
     134,380 points, as `PLAN_REASONED_LOOP.md` §0 lists it.
  6. **The schedule.** `ORDER_SEED` draws the error arm first, so the order is
     `e r1`, `c r1`, `e r2`, `c r2`, `e r3`, `c r3`.
  7. **The drafting reading above**: the transcriber under rung 4's six
     coverages and four delays, 50 draws each, from draws that are not this
     plan's (`channel-draft/0` to `/49`). Sergi saw it, and the table of tickets
     the error runs used, when he chose the coverage and the second arm. Stage A
     does not recompute it.
  8. **The error runs' escalations by governing rule**, read off
     `PLAN_REASONED_LOOP.md`'s records, and the wrong decisions its impasse runs
     let stand, by rule. The table above is a part of it, and Stage A records
     it whole.
- **[Added before signature, 2026-11-05] What writing the package showed.** The
  package was written, and its checks run, before the signature, as §7 asks.
  - **The code read** adds `reasoned_loop/protocol.py`, `gates.py`, `sample.py`,
    `run.py` and `score.py`, and `tests/test_reasoned_loop.py`, whole.
  - **`CH-g1` to `CH-g3` pass.** They print pass or fail, and two of their
    booleans go beyond §0's figures: this plan's loop at coverage 1, fed run
    `e r1`'s answers, gives back that run's rules and causes case for case; and
    every figure of items 1 to 6 and 8 above comes back as declared.
  - **Stage C's scorer was run in memory on the transcriber's four runs**, to
    test the code, and nothing was written. Its verdicts there are the ones
    items 4 and 5 already imply: on a proposer that never errs every row holds.
    It also showed one figure the list above did not: under `c r2`'s draws the
    transcriber's base made 32 wrong decisions, of which the channel reported
    20, each of which escalated, and 12 stood.

**Not seen, because nothing has produced it:**

- any loop run under the channel trigger, with any proposer but the
  transcriber;
- any error run on the new period;
- any base either arm compiles here;
- the smoke run, and so the pace of a channel run (§1).

**What the drafter expects, written down so the scoreboard can score it.**
**Five hold and one is refuted.** The drafter trusts `CH-f` most, then `CH-d`,
`CH-e`, `CH-a` and `CH-b`, and expects `CH-c` to be refuted.

- **`CH-f` holds.** The transcriber reads 1. Where tickets are many, a report
  that does not come comes later: under the standing trigger each base let 379
  to 590 wrong decisions stand. Against it: where tickets are few, reports run
  out, and the loop asks less there than the error arm did.
- **`CH-d` holds, thinly.** The same protocol, the same provider and the same
  arm held `RL-d` at 0.9601. Against it: that hold was thin, and one of its three
  runs decided 0.8898.
- **`CH-e` holds, thinly.** `RL-g` held at 14/15, and one of its runs recalled
  11/15. Against it: the same.
- **`CH-a` holds, thinly.** At coverage 1/2 the transcriber loses at most 0.0156,
  and every channel run can report 11 or 12 of the 20 `SECURITY_INCIDENT`
  tickets, where the error runs used 6 to 12. Against it:
  - `SECURITY_INCIDENT` is 3/8 of the space, and the error run that recalled
    0.7667 of it decided 0.8898;
  - the loop asks again where tickets are few, and half of them cannot be
    reported.
- **`CH-b` holds, thinly.** If `CH-a` and `CH-d` hold, their medians are likely
  within a twentieth. Against it: the spread between runs is wider than the
  line.
- **`CH-c` is refuted.** `c r2` cannot report `H05`, and `c r1` and `c r3` can
  each report three `ONCALL_ESCALATION` tickets, the last at case 1951. The
  error runs used three to six, and recalled 11/15 to 1. Against it: `e r1`
  reached 14/15 with three, and a proposer that writes `H05`'s region from an
  `H04` ticket would not need `H05`'s.

**The drafter's record argues against trusting that.**

- **The scoreboard.** On `STATUS.md`'s, 54 of 134 adjudicated rows were refuted.
- **The last plan.** `PLAN_REASONED_LOOP.md`'s drafter expected all seven rows
  to hold and got four.
- **What was done about it, rather than said.**
  - No band here was set on a development set.
  - Four lines are closed threads' own: `CH-a`'s, `CH-c`'s, `CH-d`'s and
    `CH-e`'s are `RL-d`'s and `RL-g`'s. `CH-b`'s is half of `RL-c`'s, and
    `CH-f`'s is the midpoint of the two hypotheses it separates.
  - A verdict one run carries is labelled *thin* in advance, and `CH-c`'s
    dependence on two runs is declared above.

Sergi should read the bands as more likely too comfortable than too strict, and
tighten them at signature if he disagrees.

**How the rows read together.**

- **`CH-a`, `CH-b` and `CH-d` hold.** Half the reports compile what all of them
  compile, within one period. A deployment that hears of half its errors is
  enough for this loop, at the cost `CH-f` reads.
- **`CH-d` holds and `CH-a` is refuted.** Halving the reports costs the policy.
  `CH-g` says where: the drafter expects the rare queues, and
  `SECURITY_INCIDENT`'s weight in the space.
- **`CH-d` is refuted.** The error arm did not compile the policy again on a new
  period. `RL-d`'s hold was thin, and `CH-a` and `CH-b` then read against a
  weaker comparator. `CH-g` sets both periods side by side.
- **The channel arm lands between the levels.** If it decides more of the space
  than `PLAN_REASONED_LOOP.md`'s impasse runs, and more than a twentieth less
  than this plan's error runs, half the reports contribute and are not enough. In
  `ARBITRATION_REPORT.md` §7's words, that *is a result and not a tie*.
- **`CH-c` is refuted and `CH-e` holds.** The rarest queue needs more reports
  than half coverage supplies from seven tickets. `STATUS.md`'s third item then
  narrows from the trigger's design to the supply of rare tickets.
- **`CH-c` holds.** For the first time a trigger a deployment could have
  compiles `ONCALL_ESCALATION`.
- **`CH-f` is refuted.** The loop's calls follow its reports, and a deployment
  that hears of fewer errors pays less and compiles what `CH-a` reads.

---

## 1. What is bought, and what is already paid for

**Already paid for, and free to read.** Read-only, under hard rule 4:

- **`results_reasoned_loop/`**: `PLAN_REASONED_LOOP.md`'s six runs, its Stage A
  and its Stage C. `CH-g` sets its error runs beside this plan's.
- **`results_reuse/run_n2000_r{1,2,3}.json`**: the corpus labels, as
  `manual.instrument` reads them. They are also what both triggers read.
- **`results_manual/score.json`**: the rules compiled once, `C₃` (§3).

**Bought.** Two arms of three loop runs each at n=2000, and one smoke run of 30
cases under the channel arm.

- **Every call goes through `PLAN_REASONED_LOOP.md`'s proposer**, and so through
  `PLAN_FIRST_MATCH.md`'s asker and `harness/call_record.py`, with that plan's
  request: the model and temperature 0, `response_format` on the first attempt,
  reasoning `{"effort": "high"}` and 16,000 tokens, and the pin to Baidu.

**The calls.** One per escalation, and a second when the placement round has
rules to list. What `PLAN_REASONED_LOOP.md`'s runs made, read off its record:

| run | escalations | calls | asked, without rate limits |
|---|---|---|---|
| `e r1` | 99 | 189 | 2 h 34 min |
| `e r2` | 120 | 233 | — (it met a day of refusals for the rate, and took 27 hours) |
| `e r3` | 102 | 202 | 2 h 08 min |
| `i r1` to `i r3` | 18 to 41 | 35 to 70 | 14 to 50 min |

A channel run should fall between an error run and an impasse run. `CH-f` bets
nearer the first. **The smoke run measures the channel arm's pace before the
first run**; it rests on the few escalations 30 cases make, and the findings
will say how far the estimate was.

**The cap.** A run stops at its 400th escalation, at most 800 calls. Its record
says so, its final base is the base at that case, and the rows read it as a run
(§0). No run of `PLAN_REASONED_LOOP.md` came near it.

**The money.** `PLAN_REASONED_LOOP.md`'s six runs cost $0.19 at Baidu's listing
of 2026-10-25, and its smoke run half a cent. This plan's six should cost under
half a dollar. At the cap, every call spending its 16,000 tokens, the six would
cost under four dollars.

**The time.** About six to eight hours for the error runs and three to six for
the channel's, one after another, if no provider refuses for a day. One of
`PLAN_REASONED_LOOP.md`'s runs met such a day. §5.3 says how a run waits it out
and resumes, and §2.5 where the runs are launched.

**What is not bought.**

- **Another coverage, a delay, noise or asymmetry.** The drafting reading
  covers the transcriber under them (§0). Sergi chose 1/2 over 1/4.
- **An impasse arm on the new period.** `RL-c`'s contrast is not this plan's.
  `PLAN_REASONED_LOOP.md`'s impasse runs are read beside the channel arm in
  `CH-g`, across dates.
- **Random escalation**, which reads no truth.
- **No other level**, no screen, no other model, provider, effort or budget.

---

## 2. The choices that have to be made at signature time

Each is the drafter's recommendation, and each is Sergi's to overrule. A choice
that changes a row is a change to §0, and belongs in the same signed commit. The
two choices Sergi made before the drafting, the coverage and the second arm, are
not repeated here.

### 2.1 One draw per case, per run, fixed before the run — the drafter recommends it

**Each channel run has its own draws**: 2,000 floats from
`random.Random(f"PLAN_CHANNEL/channel/{CHANNEL_SEED}/r{rep}")`, one per case in
arrival order, drawn before the first case. A wrong decision on case `t` is
reported when its draw is below 1/2.

- **A draw belongs to the case, not to the decision.** It is drawn whether or not
  the base will err there. So the run's reportable cases are fixed before it
  starts, and do not depend on what the proposer writes.
- **The draws are nested across coverages.** A case reported at 1/4 would be
  reported at 1/2. The drafting reading leans on that, and a later plan at
  another coverage can reuse the same draws.
- **The transcriber's reference under the same draws is exact.** It shows what
  each run's draws allow a proposer that never errs (§5.4).
- **A string seed goes through SHA-512**, so the draws depend on no
  `PYTHONHASHSEED`.

**Why not `rung4.feedback.Channel.observe`.** It takes every draw from one
sequence over a window of decisions already taken: one per case, and a second
for every case it reports, to draw the noise even when the noise is 0. So the
draw that decides a case depends on how many earlier cases were reported, and so
on the decisions before it. It also reads the oracle, and it is the one module
of rung 4 that may. Here the draw must exist before the decision, and the labels
are handed in (rule B).

**The alternative** gives the three runs one set of draws. The arm's spread
would then be the proposer's alone, and its result would rest on one draw.

### 2.2 A reported error escalates at once, as the error arm's does — the drafter recommends it

With delay 0, a reported wrong decision escalates when its case arrives. The
proposer's answer replaces the decision, as at any escalation, and the rule it
writes is born before the next case. At coverage 1 that is the error arm, step
for step.

**The alternative** lets the wrong decision stand and escalates the ticket at a
later case. The drafting reading found that barely moves the final base, and it
would make the arms differ in two ways.

### 2.3 Three runs an arm, the arms alternating, and the cap — the drafter recommends it

- **Three runs** is `PLAN_REASONED_LOOP.md`'s count.
- **The order.** `ORDER_SEED` draws which arm runs first, and then the arms
  alternate: one run of each in every repetition. If Stage B spans two days or
  more, both arms have runs on each.
- **The cap**, 400 escalations a run, as `PLAN_REASONED_LOOP.md`'s.

### 2.4 The smoke run is 30 cases under the channel arm — the drafter recommends it

The channel arm is this plan's new path. The smoke run takes its own draws,
`random.Random(f"PLAN_CHANNEL/channel/{CHANNEL_SEED}/smoke")`, and must show,
before the first run:

- every attempt that reached the model served by the pinned provider, reasoned,
  and ended `stop`;
- a rule born, and a placement round answered;
- the trigger's record: for every wrong decision, its draw and whether it
  escalated.

**The alternative** smokes the error arm, whose path `PLAN_REASONED_LOOP.md`'s
smoke run already tried.

### 2.5 Where the runs are launched — Sergi's choice; the drafter has no recommendation

- **In Sergi's terminal**, where a run outlives no harness.
- **Or by the agent, at Sergi's request, detached from its harness**, as
  `PLAN_REASONED_LOOP.md`'s runs were: a supervisor runs them one at a time,
  resumes a run an outage has stopped, commits each record before the next run
  starts, and never passes the overwrite flag.

Either way the order is §2.3's, and no two runs are ever side by side.

### 2.6 Everything else is `PLAN_REASONED_LOOP.md`'s, as signed

The first call is blind at every escalation, the placement round is v2b's and a
refused rule is not born, a copy is born, the reasoning setting is
`PLAN_FIRST_MATCH.md`'s on both calls, and Baidu is pinned (that plan's §2.1 to
§2.5). Changing any of them here would make this plan's error arm another arm
than that plan's.

### 2.7 `PREDICTION.md`

Not touched. It is rung 1's long run, and this plan is not it (hard rule 2).

---

## 3. Reference figures, with the record that owns each

Nothing here is produced by this plan. `CH-g1` recomputes what it checks against
its record, rather than publishing it again.

| figure | value | owning record |
|---|---|---|
| the 29 rules compiled once, `C₃` | 1.0000 of the space, in every ask (`G-a`) | `results_manual/score.json`, published by `FINDINGS_MANUAL.md` |
| `PLAN_REASONED_LOOP.md`'s error arm, 2026-11-01 and 02 | `space` 0.9601, 0.9635 and 0.8898, median 0.9601 (`RL-d`, held thinly); `recall_ONCALL` 14/15, 1 and 11/15, median 14/15 (`RL-g`, held thinly); `recall_SECURITY` 0.9333, 1 and 0.7667 | `results_reasoned_loop/score.json`, published by `FINDINGS_REASONED_LOOP.md` |
| its impasse arm | `space` 0.4614, 0.5775 and 0.3430, median 0.4614; `recall_ONCALL` 0 in every run | same |
| its contrast | `RL-c`, 0.4987, held | same |
| its drafts | the right queue at 371 of 408 escalations, 0.9093; 0.8884 at the errors (`RL-a`, held thinly) | same |
| its calls, pace and cost | 35 to 233 calls a run; a first call took a median of 32.0 to 54.6 seconds by run; $0.19 for the six runs | same |
| the transcriber under its two triggers | 2 escalations and 14,820 points under the impasse trigger; 23 escalations and 134,380 points under the error trigger | `results_reasoned_loop/sample.json`, published by the same |
| rung 4's channel | coverage, asymmetry, delay and noise, as `FINDINGS4.md` §2 defines them; its sweep's grid. No audited figure exists at this plan's cell, and no row reads any rung-4 figure | `results4/`, published by `FINDINGS4.md` |

---

## 4. Non-negotiable rules

`CLAUDE.md`'s own numbering, so that cross-references point at the right rule.

1. **Do not modify the frozen specification.** This plan reads
   `harness/domain.py` and `harness/ceiling_check.py`, and edits no frozen file.
   Under `harness/` it touches only `provenance.py`'s list of code roots, which
   is plumbing (§11).
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A
   signed plan travels alone, staged by name, in its own commit.
3. **Do not parallelise.** Each run is strictly sequential: a rule born at case
   `t` decides case `t+1`. The runs go one after another, never side by side,
   and each run's record is committed before the next starts.
4. **Seed 17, no regeneration.** Every record under `results_reasoned_loop/`,
   `results_manual/` and `results_reuse/` is read-only.
   `harness/record_guard.py` guards this plan's paid records, and the flag that
   overrides it is not typed without Sergi asking.
5. **Do not adjust a prompt, a text or the schema.** Every text is
   `PLAN_REASONED_LOOP.md` §5.1's, byte for byte, and `CH-g2` checks each by
   digest. Once the smoke run has been read, nothing moves.
6. **If the numbers come out badly, report them.** A channel that compiles
   nothing is a result, and so is an error arm that does not replicate.
7. **The API key goes in the environment.** It is loaded without printing,
   checked by its length, and read off OpenRouter's key endpoint as an API key
   and not a management key before any call (`reuse.run.key_check`).

And this plan's own, lettered:

A. **Called and not edited:** `reasoned_loop/`, `first_match/`, `blind/`,
   `authorship/`, `manual/`, `reuse/`, `edges/` and `rung2/`.
   - The protocol, the proposer and the escalation are `reasoned_loop`'s:
     `reasoned_loop.protocol` and `reasoned_loop.loop.propose_v1b`.
   - The transcriber is `reasoned_loop.references.Transcriber`.
   - The instrument is `manual.instrument`'s.
   - Rung 4's channel is cited for its parameters and not imported.

B. **No label reaches a prompt.**
   - **Both triggers read the corpus labels, handed in**, as
     `PLAN_REASONED_LOOP.md`'s error trigger reads them: from `PLAN_REUSE.md`'s
     records, never from the oracle.
   - **No module on the proposer's path imports the oracle.** That path is
     `channel/loop.py` and `channel/run.py`, with the modules of
     `reasoned_loop/` they call. Neither imports by name the oracle,
     `HIDDEN_DSL`, `harness.ceiling_check`, `rung2.hidden_priority` or
     `rung4.feedback`. Both join `ONLINE_LOOP` and the authority channel's
     watch.
   - **The draws read no label.** They are drawn from the seed alone, before
     the run.

C. **Every record carries `_env`**, with:
   - the model, the temperature, the reasoning setting, the token budget and the
     provider pin;
   - the arm, the run, the coverage, the draws' seed string and their digest,
     and the digests of the system prompt, `BLIND_BASE` and
     `PLACEMENT_TEMPLATE`;
   - every call's `call_attempts`, and the cause of every retry.

   Every command runs with `PYTHONHASHSEED=0` set explicitly.

D. **The constants of §11 are fixed here and pinned by tests**, so that moving
   one after a figure exists is visible in a diff.

E. **What the model writes is recorded whole**, as `PLAN_REASONED_LOOP.md`'s rule
   E says: every call's payload with its keys in the order written, and its
   reasoning. No stage codes a note or the reasoning.

F. **The order of Stage B is §9's**, and the module refuses a run out of it.

G. **The provider is pinned on every call.** A call that another provider served
   is recorded and counted, and its answer still decides its case, as in
   `PLAN_REASONED_LOOP.md`'s rule G.

H. **A failed call is never answered with v1's retry message.** Only a failed
   parse is (`PLAN_FIRST_MATCH.md`'s rule).

I. **The triggers read the truth, and nothing else decides by it.** The engine
   never decides by a label. The proposer never sees one, and is never told
   that the base erred, in either arm.
   - **[Corrected before signature, 2026-11-05]** The draft said nothing else
     reads the truth. The loop also reads the label to score what was decided,
     into the record, as rung 2's loop always has: whether the decision that
     stood, or the proposer's answer, was right; and a rule's `correct_count`,
     which the engine keeps for the record and neither reads nor shows the
     proposer.

---

## 5. The protocol

### 5.1 v1b, unchanged

The texts, the escalation, the placement round and its validator are
`PLAN_REASONED_LOOP.md` §5.1 and §5.2's, with their corrections before
signature, called from `reasoned_loop/` and not copied. Only the trigger is
this plan's.

### 5.2 The two triggers

Both arms escalate a case when the engine returns IMPASSE or CONFLICT.

- **The error arm** also escalates a case the engine decides with a queue that
  is not the case's label: `PLAN_REASONED_LOOP.md` §5.3, with its addition
  before signature. An error escalation's rule is not counted as fired.
- **The channel arm** also escalates such a case **when its draw is below 1/2**.
  A wrong decision whose draw is 1/2 or above stands, as any decision does
  under the impasse trigger, and its rule is counted as fired.
- **A case the base leaves undecided escalates as an impasse in both arms.**
  Rung 4 counted such a case as a wrong decision, reported with probability `c`.
  Here no draw reaches it.
- **The trigger is one function, in `channel/loop.py`.** It is the only code of
  the loop that reads a label to decide anything the loop does, and a test pins
  that, rather than intent (`FINDINGS4.md` §2's erratum).
  - **[Corrected before signature, 2026-11-05]** The draft said it is the only
    code of the package that compares a decision with a label. That is false:
    the loop compares the decision that stood, and the proposer's answer, with
    the label once each, to score them into the record (rule I), and the
    offline modules read labels to score and to check. The tests pin what holds
    instead. Labels and draws that leave every cause unchanged leave the
    proposer's calls, its messages and the base unchanged. Every comparison with
    the label on the proposer's path is listed in a test, so that a new one is a
    decision.
- **Both keep the cause of every escalation**: impasse, conflict or error, and
  on an error the queue and the rule the engine gave. The cause is named
  `ERROR` in both arms, so that `PLAN_REASONED_LOOP.md`'s scorer reads them
  alike.

### 5.3 What a run records, and how it resumes

- **What it records** is `PLAN_REASONED_LOOP.md` §5.4's record, and, for the
  channel arm:
  - the coverage, the draws' seed string and the digest of the 2,000 draws;
  - on every case's row, its draw, and whether its wrong decision was reported.
- **How it resumes** is `PLAN_REASONED_LOOP.md` §5.5's, with both its signed
  amendments, called and not copied.
  - **A call refused for the rate on every attempt is waited out**, after
    each wait of `RATE_LIMIT_WAIT`. Once every wait is spent it is an outage:
    the run stops unrecorded, and the same command resumes from the git-ignored
    partial file.
  - **A call served from the partial file keeps the seconds the file kept.**
  - **Both are tested before the first run**, on runs built by hand, as
    `CLAUDE.md` asks of a plan whose runs resume.

### 5.4 The references Stage A computes

- **The transcriber** runs through this plan's loop under the error trigger,
  and under the channel trigger with each run's draws and the smoke run's. It
  shows what each trigger, and each draw, allows a proposer that never errs
  (§6.12).
- **The hidden policy through v1b's path**, as `PLAN_REASONED_LOOP.md` §5.6 runs
  it.
- **The supply each run's draws leave**: by governing rule, the corpus tickets,
  the reportable ones, and the error escalations `PLAN_REASONED_LOOP.md`'s
  error runs made there.

---

## 6. Known traps

**6.1 — Both arms' error escalations are told they are impasses.** v1 calls the
model the system's exception component, and the user message labels the ticket
*TICKET EN IMPASSE*. On an error escalation both are false: the engine decided,
wrongly. The arms keep `PLAN_REASONED_LOOP.md`'s prompts so that the trigger is
their only difference (that plan's §6.1).

**6.2 — Level 3 hands over the label** (`PLAN_MANUAL.md` §6.2). Every row
measures what the loop compiles from a policy it holds as text.

**6.3 — Both triggers read the truth.** The error arm asks exactly where its base
is wrong. The channel arm asks where its base is wrong and a draw says the error
was reported. Neither is free in a deployment, where the report comes from the
world. Here the corpus labels stand in for the world, as rung 4's channel read
the oracle.

**6.4 — The online figures are corrected online.** A reported error's decision
is replaced by the proposer's answer, and an unreported one stands. So the
channel arm's online e2e counts half its errors as corrected, and the error arm's
counts all of them. They are reported, never set against each other, and no row
reads them.

**6.5 — A draw is the case's, not the region's.** Two arrivals of one ticket get
two draws. A run whose draws leave a rule's tickets all unreportable cannot be
taught that rule by an error escalation: `c r2` and `H05` (§0).

**6.6 — `SECURITY_INCIDENT` weighs 3/8 of the space.** `space(B)` moves with its
recall more than with any other queue's. Every space figure in `CH-g` is split
by the keyword, as `PLAN_UNREACHED.md`'s findings ask.

**6.7 — v1b's two defects are kept** (*What it changes*, above). Both arms list
rules nested with the draft, and rules whose conflict the base already decides,
and both pay for it in refusals and repairs alike.

**6.8 — One period is not one day.** The six runs alternate over half a day or
more, and a day of refusals for the rate can split them across days. The
alternation puts both arms on each day the runs span. `CH-g` gives every run's
dates.

**6.9 — The error arm here is not `PLAN_REASONED_LOOP.md`'s.** It is its
protocol on new dates. Set beside that plan's runs, it reads a replication
across dates, reported in `CH-g`.

**6.10 — Reasoning at temperature 0, and one provider** (`PLAN_REASONED_LOOP.md`
§6.13 and §6.15). A provider may not honour temperature 0 while the model
reasons, and Baidu serves this model at fp8. The runs of one arm may part for
those reasons as well as for their bases. Each run's value is published.

**6.11 — Back-to-back runs leave `git_dirty` true**, because each finds the
earlier records not yet committed. Rule 3 of §4 commits each record before the
next run, and `code_dirty` is what identifies the code.

**6.12 — What the transcriber is not.** It writes the governing rule and places
it right every time. It bounds nothing about the model. It shows what each
trigger and each draw allow a proposer that never errs.

**6.13 — The draws change the trajectory, not only the dose.** A different set
of wrong decisions escalates, the base grows differently, and so do the
decisions the channel can report next. `CH-b` reads the dose and the trajectory
together, and no row separates them.

---

## 7. Blocking checks, before any record is written

All are free and all run by `--dry-run`. **Any failure stops the plan before a
figure exists.**

**CH-g1 — The inputs reproduce themselves.** Blocking in the sense of
`harness.ceiling_check`.

- **The suite.** `python3 -m unittest discover` is green.
- **`PLAN_REASONED_LOOP.md`'s verdicts.** `RL-a` to `RL-g` come back from its
  records, through its scorer, called and not copied.
- **This plan's loop at coverage 1 is that plan's error arm.** With the
  transcriber, and with the answers of that plan's run `e r1` served back in
  order by a replay double, this plan's loop and `reasoned_loop.loop.run_loop`
  under arm `e` give the same record, case for case.
  - **[Corrected before signature, 2026-11-05]** The replay serves each answer
    at the case and round that run asked for it, and refuses any other call.
    The check also holds the replay to the run: its rules and causes are
    `e r1`'s, case for case.
- **At coverage 0 it is that plan's impasse arm**, on the transcriber.
- **The rebuilt base.** A run's rebuild equals the engine the run ended with,
  on the transcriber's runs here; at Stage C it is held to the record.
  - **[Added before signature, 2026-11-05] The trigger's record.** On the same
    runs, every case's row is held to its draw and to the rule of §2.1: a row
    says a wrong decision was reported exactly when its draw falls below the
    coverage, and it escalated exactly then. The smoke check reads the same.
- **The labels.** The corpus labels the triggers read agree with
  `manual.instrument.corpus_truth` on every case.
- **No float decides a check.** Values are compared as fractions, and counts as
  integers.

**CH-g2 — The protocol and the draws are §5's.**

- **The texts.** Each text of `PLAN_REASONED_LOOP.md` §5.1 matches its source by
  digest.
- **The requests.** Checked through `tests/doubles.py`'s SDK double, as `RL-g2`
  checks them: the reasoning setting, the budget, the pin, temperature 0, and
  `response_format` on the first attempt.
- **The draws.** Each run's draws are rebuilt from `CHANNEL_SEED`. Their
  reportable cases, and their reportable rare tickets by rule, are §0's.
- **The transcriber gives back §0's figures** under each run's draws and under
  the error trigger.
- **The hidden policy through v1b's path** gives back the 199 edges and 1.0000
  on both surfaces.

**CH-g3 — The schedule is §2.3's and §9's.**

- The six runs' order is rebuilt from `ORDER_SEED`.
- The smoke run is 30 cases under the channel arm, with its own draws.
- The cap is 400 escalations.

**CH-g4 — The signature**, §11.

---

## 8. Stage A — the references (free, gated)

**Deliverable.** `channel/sample.py` → `results_channel/sample.json`.

- **`CH-g1` to `CH-g3`.**
- **The references, recomputed and owned by this record:** §0's figures 1 to 6
  and 8, the transcriber under every draw and trigger, and the hidden policy
  through v1b's path.

**It produces nothing adjudicable.** It runs after §0 is signed, so that a figure
§0 did not declare cannot inform a band. If one of §0's declared figures does not
come back, Stage A's findings carry an erratum to §0, dated, and no band moves.

## 9. Stage B — the runs (gated on §0)

**Deliverable.** `channel/run.py` → `results_channel/loop_smoke.json`, then the
six runs `loop_{c,e}_r{1..3}.json` in §2.3's order. **Each record is committed
before the next run starts.**

**Every run, before any call:**

1. **`--dry-run`** runs `CH-g1` to `CH-g3` and stops. It builds no client and
   needs no key.
2. **The signature (`CH-g4`).** While `PLAN_CHANNEL.md` carries a blank
   signature line, the module exits here.
3. **What comes before it.**
   - **The smoke record**, with what §2.4 asks of it.
   - **Stage A's record.**
   - **Every run before this one** in §2.3's order.

   If the smoke run fails, the runs do not start, and what would change is a
   signed amendment.
4. **The key**, by `reuse.run.key_check`, called rather than copied.
5. **`CH-g1` to `CH-g3`, blocking.**
6. **The destination.** A paid record is never overwritten.
7. **The client, and the calls**, sequential, under hard rule 3.

**The smoke run's pace is reported before the first run**, by call and by round.
It decides nothing, and no row reads its answers.

## 10. Stage C — scoring, and the six adjudications (free)

**Deliverable.** `channel/score.py` → `results_channel/score.json`, and
`results_channel/FINDINGS_CHANNEL.md`, which owns every figure.

- **`CH-a` to `CH-f`**, each against its line, exactly. Each carries *thin* and
  *unadjudicable* as §0 defines them.
- **Each row's per-run values**, never summed into the verdict.
- **`CH-g` in full.**
- **The runs themselves.** Failed calls, refusals by verdict, answers from
  another provider, retries by cause, attempts refused for the rate,
  reasoning tokens over the attempts that reached the model, and the pace by run
  and by round, over the calls that met no refusal as well as over all.

---

## 11. The gate, and where the code lives

**Every module of this package that writes a record refuses while §0 is
unsigned.** `channel/sample.py` and `channel/score.py` spend nothing.
`channel/run.py` refuses before it constructs a client. **The free stages get
the gate because what it protects is the order of events, not money.** A record
of this plan written before the signature would be a figure that existed before
its band.

**The gate reads `PLAN_CHANNEL.md` and no other plan, and it counts every
signature line**, with `reuse/plan.py`'s counting called with this plan's path
and minimum. `MIN_SIGNATURES = 1` today, for §0. An amendment carries its own
line and raises it. No flag skips the gate.

**Constants fixed here, before any figure exists, not to be tuned afterwards, and
pinned by tests:**

- **The client.** Imported from `reasoned_loop/plan.py`, and so from
  `first_match/plan.py`, and not retyped: `MODEL`, `TEMPERATURE`, `REASONING`,
  `MAX_TOKENS`, `MAX_RETRIES`, `CALL_RETRY_WAIT`, `PROVIDER`, `PROVIDER_NAME`,
  `RATE_LIMITED` and `RATE_LIMIT_WAIT`.
- **The protocol.** `PROTOCOL = "v1b"`, `LEVEL = 3`, and
  `SYSTEM_PROMPT_SHA16 = "7b883f03a863d647"`, imported likewise.
- **The arms.** `ARMS = ("c", "e")`, in that order, because `ORDER_SEED`'s draw
  picks from it. `COVERAGE = {"c": Fraction(1, 2), "e": Fraction(1)}`.
- **The runs.** `REPS = 3`, `N = 2000` and `SEED = 17`; `SMOKE_N = 30` and
  `SMOKE_ARM = "c"`; `MAX_ESCALATIONS = 400` and
  `MAX_CONSECUTIVE_FAILURES = 5`.
- **The seeds.** `ORDER_SEED = 89` and `CHANNEL_SEED = 97`.
  - **They are new**, and were fixed by rule: the next two primes after
    `PLAN_REASONED_LOOP.md`'s 83. Every closed thread's seeds are 17 to 20, 25,
    41, 43, 47, 53, 59, 61, 67, 71, 73, 79 and 83, and values from 1000 up.
  - **`ORDER_SEED` draws one thing**, which arm runs first, from
    `f"PLAN_CHANNEL/order/{ORDER_SEED}"`.
  - **`CHANNEL_SEED` draws the channel**: one stream per channel run,
    `f"PLAN_CHANNEL/channel/{CHANNEL_SEED}/r{rep}"`, and one for the smoke run,
    `.../smoke`.
  - **Both are string seeds**, through SHA-512, and depend on no
    `PYTHONHASHSEED`.
  - **The placement listing is not these seeds'.** It keeps v2b's
    `LISTING_SEED`, through `blind.protocol.listing`.
- **`DECLARED`** holds the figures §0 lists as computed while drafting, as
  `reasoned_loop/plan.py`'s holds that plan's.
- **The lines of §0.** They are fractions, and every comparison with them is
  exact.
  - `CH_A_LINE = Fraction(9, 10)`.
  - `CH_B_LINE = Fraction(1, 20)`.
  - `CH_C_LINE = Fraction(9, 10)`.
  - `CH_D_LINE = Fraction(9, 10)`.
  - `CH_E_LINE = Fraction(9, 10)`.
  - `CH_F_LINE = Fraction(3, 4)`.

**The names.**

- **The package is `channel/`.** No module of the standard library has that
  name.
- **The rows are `CH-a` to `CH-g`, with two letters.** Every single capital
  already names a thread, and `QA`, `FM`, `RR` and `RL` are taken.
- **The protocol is still v1b.** This plan adds a trigger, not a protocol.

Drafter's proposal for the layout; the naming is Sergi's to overrule:

```
channel/__init__.py
channel/plan.py        the gate, the constants of §11 and the draws
channel/loop.py        the loop with a coverage, calling reasoned_loop's escalation   [proposer's path]
channel/references.py  the transcriber under every draw and trigger, and the supply table
channel/gates.py       CH-g1 to CH-g4
channel/sample.py      Stage A
channel/run.py         Stage B: it spends                                            [proposer's path]
channel/score.py       Stage C
results_channel/FINDINGS_CHANNEL.md
results_channel/sample.json  loop_smoke.json  loop_{c,e}_r{1..3}.json  score.json
tests/test_channel.py
```

**The plumbing goes in the same commit as the modules:**

- **`CODE_ROOTS`.** `channel` joins it in `harness/provenance.py`, and joins the
  oracle scan's roots in `tests/test_oracle_separation.py`.
- **`ONLINE_LOOP` and the authority channel.** The two modules marked above join
  both, with rule B's comment. Every call sends the manual's text.
- **The partial files**, `results_channel/*.partial.jsonl`, join `.gitignore`.
- **The guarded writers** in `tests/test_writer_lists.py` grow by one.
- **The call site.** The proposer is `reasoned_loop`'s, which asks through
  `first_match/ask.py`'s asker. That asker is already a classified call site and
  carries the call recorder, so `tests/test_call_record.py`'s list does not
  grow.
- **The README's table of writers** gains its rows, and so does its table of
  tests.

**The list of modules allowed to see the oracle does not grow.** Tests touch no
network.

---

## 12. Definition of done

- [ ] Records under `results_channel/` with `_env`. Each carries the model, the
      temperature, the reasoning setting, the budget, the pin, the arm, the run,
      the coverage, the draws' seed string and digest, the texts' digests and
      `call_attempts`. All were produced with `PYTHONHASHSEED=0`.
- [ ] `CH-g1` to `CH-g4` passed before any record was written. The key check and
      the smoke run came before the first run, and each run's record was
      committed before the next began.
- [ ] Before the first run, the smoke run showed what §2.4 asks of it.
- [ ] The plumbing of §11, and tests pinning:
      - the constants, the seeds and the gate;
      - the draws, rebuilt from their seed strings;
      - both triggers, on runs built by hand, and that coverage 1 is the error
        arm and coverage 0 the impasse arm;
      - that the trigger is the only code of the loop that reads a label to
        decide anything, and that nothing it reads reaches a prompt
        (**[corrected before signature, 2026-11-05]**, §5.2);
      - the resume, and that a resumed record keeps each call's own seconds;
      - the exactness of §0's comparisons, *thin*, and each row's conditions for
        having no value;
      - the gate's verdicts on fake plans, and the count of signature lines,
        never whether this plan is signed.

      The transcriber's figures are `CH-g2`'s and Stage A's, never a test's,
      because no test runs the loop over the corpus.

      The whole suite is green on 3.10 and 3.12.
- [ ] Every figure in prose names its surface, its arm, its denominator and its
      runs.
- [ ] `results_channel/FINDINGS_CHANNEL.md` owns every figure, with a dated
      erratum wherever it corrects something already published. That includes
      this plan's §0 *already seen*, if Stage A does not reproduce it, and §1's
      estimates of the pace and the calls.
- [ ] `STATUS.md`: the scoreboard gains the `CH` thread. *What is open* narrows
      its third item by what this plan settles, and its second if `CH-g` bears
      on it.
- [ ] `IDEAS.md`: *A trigger a deployment could have* is narrowed, with what
      this plan opens.
- [ ] `tests/test_prose_tables.py`'s `THREADS` gains `CH`, and its `TABLES`
      gains `FINDINGS_CHANNEL.md`'s verdict table.
- [ ] This plan is indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, records and this plan are in separate commits. The plan and its
      signature are each alone in their commits.

---

## 13. What this plan cannot settle, declared before it runs

1. **Lower coverage.** Only 1/2 is bought. At 1/4 the drafting reading found the
   channel's luck alone moving the transcriber across 0.61 to 0.9999 of the
   space.
2. **Delay, noise and asymmetry.** None is run. Delay barely moved the
   transcriber's final base in the drafting reading; it moves the online
   figures, which no row reads. Noise and asymmetry would add reports of right
   decisions, and with them calls.
3. **A trigger that reads no truth.** Random escalation is not run.
4. **Telling the proposer the base erred.** Neither arm's prompts say so (§6.1).
5. **v1b's defects.** Kept in both arms (§6.7). What a round that lists only
   what the engine can still order would compile is another plan.
6. **The draws.** One set per run, fixed by the seed. What other draws would do
   is read on the transcriber only.
7. **An impasse arm on the new period.** Not run; `RL-c`'s contrast stays across
   dates where `CH-g` sets it.
8. **One model, one provider, one manual, one arrival order, three runs an
   arm.**
