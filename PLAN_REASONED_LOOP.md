# PLAN_REASONED_LOOP — the loop with reasoning on: what a proposer that applies the list compiles, under the standing trigger and under feedback on its errors

**Status: drafted by Claude on 2026-10-27, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing runs and no
record is written until Sergi has signed §0.** The signature has to land before
any figure named here exists, in its own commit, staged by name. That includes
Stage A, which spends nothing: §11 says why.

**Asked for by Sergi on 2026-10-27**, on the item
[`STATUS.md`](STATUS.md)'s *What is open* ends its second item on, and
[`IDEAS.md`](IDEAS.md) carries first under *What `PLAN_REASONED_RULE.md` opens*:
*the loop with reasoning on*. Two choices were his before this was drafted:

- **The order comes from a placement round.** Every rule the proposer writes is
  placed against the base's own rules of other queues that it overlaps, as
  `PLAN_BLIND.md`'s v2b places it (§5).
- **Two arms.** One is the loop's standing trigger. The other is the same loop,
  which also escalates a ticket the base decided wrongly (§2). Sergi chose it
  after the drafter showed him the free reading below.

**The item.** `PLAN_REASONED_RULE.md` asked level 3's escalated tickets for a
rule, with the 29 rules in the prompt, no screen, and reasoning on
([`FINDINGS_REASONED_RULE.md`](results_reasoned_rule/FINDINGS_REASONED_RULE.md)).

- **The model chose the right queue on 0.9672 of the decisions** (`RR-c`).
- **Its rule was usually the listed rule that governs the ticket.** On 250 of
  its 342 answers the rule covered exactly that rule's region.
- **What a loop compiles from such a proposer depends on the order its rules
  get.** Rung 2's engine orders nested rules by containment, and crossing ones
  only by declared edges.
- **The edges this proposer declares cite the manual's identifiers**, `H01` to
  `H29`, which no base holds. `PLAN_MANUAL.md`'s engine dropped every such
  declaration ([`FINDINGS_MANUAL.md`](results_manual/FINDINGS_MANUAL.md), Stage
  B2).

**What the drafter found before drafting, and why there are two arms.** The loop
asks only where its base leaves a ticket uncovered or contested.

- **The second arrival of the corpus is the list's default.** Case 1 is governed
  by `H29`, the list's last rule, `severity gte 1` → `T1_GENERAL`, which every
  point of the space matches.
- **A rule written as `H29`'s region covers the space.** Under rung 2's engine
  every later rule nests inside it and wins where it matches, so the base stays
  consistent. But no ticket can impasse again, and the loop asks only on a
  CONFLICT.
- **A perfect transcriber stops at case 1.** Take a proposer that writes, at
  every escalation, the rule that governs the ticket, and places it by the
  list's order. It ends with two rules, and its base decides 14,820 of the
  134,400 points of the space right: 0.1103.
- **The model writes that rule when it reasons.** On the 28 answers whose ticket
  `H29` governs, `PLAN_REASONED_RULE.md`'s reasoning rule arm wrote `H29`'s whole
  region on 12. Its rule arm without reasoning did so on 1. That fits
  `PLAN_MANUAL.md`'s level-3 loop, which wrote without reasoning: *a base that
  covered the whole space stopped impassing … Under the rules it never
  happened*.
- **The same transcriber, also escalating where the base decides wrongly, asks
  23 times.** Its base decides 134,380 of the 134,400 points right.

The drafter computed each of those figures while drafting, and Stage A
recomputes them (§0, *What the drafter had already seen*). The mechanism has
been named before from the other side. `CHAT_SUMMARY.md` §1 says *partitioning
does not eliminate the errors — it eliminates the error detector*. A rule that
covers the space removes the detector too.

**So two limits compete for what a reasoning loop compiles.** One is the order
its rules get; the other is the trigger that asks. The two arms separate them.

**The question, in its cleanest form.** With level 3's manual in the prompt,
reasoning on, and every rule placed against the base's rules of other queues
that it overlaps:

- does the loop's proposer choose its queues as the re-ask did?
- does the standing trigger stop asking early?
- does a trigger that also asks on errors compile what the standing one does
  not?
- does the proposer place its rules the way the list orders them, better than a
  fixed ranking of the queues?
- is the rarest queue compiled, when the loop is asked about it? No loop has
  compiled it so far.

**Two arms.** Both run on rung 2's engine, at n=2000 and seed 17, three runs
each, under one protocol, **v1b** (§5), with reasoning on.

- **The impasse arm, `i`**, has the loop's standing trigger: a ticket escalates
  on an IMPASSE or a CONFLICT.
- **The error arm, `e`**, escalates on those too, and also on a ticket the base
  decides with the wrong queue.
  - The trigger reads the truth of the arrival.
  - The proposer is handed no label, and is not told that the decision was wrong
    (§6.1).

The arms send the same prompts. They differ only in which tickets they ask
about.

**What it changes in what is measured, said first.**

- **The founding question is changed again.** With the 29 rules in the prompt,
  the loop is asked whether a policy it was handed survives compilation, as
  `PLAN_MANUAL.md` asked. Here a proposer that applies that policy writes the
  rules.
- **The error arm breaks one of the loop's invariants, on purpose.**
  `rung2/shadow2.py` says the only trigger is an IMPASSE or a CONFLICT, *never
  "the answer was incorrect"*. The error arm adds that trigger.
  - It is rung 4's feedback at asymmetry 0 and full coverage: a report arrives
    exactly when a decision was wrong ([`FINDINGS4.md`](results4/FINDINGS4.md),
    its table of parameters).
  - It is used to ask the proposer, and never to hand it the label.
- **Reasoning is on, against `PLAN_REUSE.md` §1's amendment**, for this plan's
  calls only. The setting is `PLAN_FIRST_MATCH.md`'s, which
  `PLAN_REASONED_RULE.md` used for its two reasoning arms.
- **No prompt text is new.** The system prompt is `PLAN_MANUAL.md`'s level-3
  loop prompt, byte for byte. The line that stands for the base and the
  placement message are v2b's. What is new is their combination, reasoning in
  the loop, and the error trigger.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**The runs.** `R = 3` runs per arm. Each run is `PLAN_REUSE.md`'s loop over the
2,000 cases of `generate_corpus(2000, seed=17)`, with a fresh rung 2 engine, under
v1b. The arms alternate, as §2.6 sets.

**The statistics.** Each is a ratio of integer counts. **Each is compared with its
line exactly, as a fraction.** No rounding enters a verdict.

- **`B`, a run's final base.** Its rules, and the edges the engine accepted,
  rebuilt from the record. `RL-g1` holds the rebuilt base to the engine the run
  ended with.
- **`space(B)`.** `PLAN_MANUAL.md`'s statistic: the share of the 134,400 points
  of the exhaustive space that `B` decides right under rung 2's engine. A
  CONFLICT or an IMPASSE is not right. It is computed by
  `manual.instrument.over_space`.
- **`recall_q(B)`.** Of the points whose true queue is `q`, the share `B` sends to
  `q`. The same function computes it.
- **A draft** is the queue the first call of an escalation names.
  - A draft is right when it is the true queue of the ticket.
  - A first call that fails, with no answer, counts as a draft not right.
- **`cover(r)`** is the first case of run `r` after which every point of the
  space matches some rule of its base. It is *none* if that never happens.
- **The direction** is `PLAN_BLIND.md`'s `K-b` statistic, through
  `blind.rows.edge_rows` and `blind.rows.direction`, with this plan's
  population.
  - **Which edges.** Every edge a placement round declared that the engine
    accepted and entered in the graph, between rules of different queues,
    neither of them a keyword rule.
  - **How each is read.** For the better rule over the shared region, on the
    half of the space without the keyword.
  - **The unit.** Each older rule counts once, for `PLAN_BLIND.md` §0's reason.
    The reading is pooled over the runs of both arms, and a rule of one run is a
    unit apart from any rule of another.
- **The ranking's reading** takes the same pairs and the same units. It reads them
  for the rule the Stage C hierarchy names (`blind.rows.stage_c_names`), as
  `K-c` read it.

**The unit, *thin*, and when a row has no value.** All of it is settled here and
not in the scorer, which is where `PLAN_AUTHORSHIP.md`'s `E-c` lost its verdict.

- **Pooled rows.** `RL-a`, `RL-e` and `RL-f` pool over runs. Each run's value is
  published beside the pooled one and adjudicates nothing.
- **Median rows.** `RL-c`, `RL-d` and `RL-g` read medians over an arm's runs. The
  median of three runs is the middle one, and of two runs their mean.
- **The count row.** `RL-b` counts runs.
- **A verdict is labelled *thin*** when any of the following would put the
  statistic on the other side of its line. The label does not change the
  verdict.
  - For a pooled row, dropping any one run.
  - For a median row, any one run of either arm put in place of its arm's
    median. That is `PLAN_MANUAL.md`'s test.
  - For `RL-b`, one run on the other side.
- **A run is complete** when it reaches case 2,000, or the cap of §1.
  - A run that cannot be completed leaves its arm with fewer runs. The rows read
    the runs that exist, and the record names the missing one.
  - A row that reads an arm with fewer than two runs has no value.
- **Minimum material.**
  - `RL-a` has no value with fewer than 60 escalations pooled.
  - `RL-e` and `RL-f` have none with fewer than 20 units.
- **A row with no value is unadjudicable**, and the record says so.

**Which side had the label**, for every arm and reference. This was checked
against the prompts and the code while drafting, and not recalled, as `CLAUDE.md`
asks of any plan that sets a comparison on the proposer:

| who | what it is handed | reads a label? |
|---|---|---|
| the proposer, both arms | the 29 rules in order, under *"Se aplica la primera regla de la lista cuyas condiciones casa el ticket."* | **yes, in effect**: every ticket's label is derivable from the text by first match (`PLAN_MANUAL.md` §6.2) |
| the error arm's trigger | the truth of every arrival, read from the corpus labels | **yes**, but only whether the base's decision is right. It is never handed to the proposer, and the proposer is not told why it was asked (§6.1) |
| the impasse arm's trigger | the base and the ticket | no |
| the transcriber references (§5.6) | level 3's text, applied by first match; under the error trigger, also the truth | yes |
| `C₃`, the rules compiled once (§3) | level 3's text | yes |

- **No arm sees an example.** The loop sees the arrivals as they come, as every
  loop has.
- **No baseline is fitted to the proposer's answers.** The references are
  mechanical, and they read the text or the truth, never an answer.

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **RL-a** | **Reasoning carries into the loop's choice of queue.** The proposer drafts the right queue at its escalations about as often as the re-ask did | over every escalation of both arms' runs: the right drafts, over the escalations | **≥ 0.90** | **< 0.90** |
| **RL-b** | **The standing trigger stops asking early.** With reasoning on, the impasse arm's base comes to cover the whole space within the first tenth of the arrivals | the share of `i`'s runs whose `cover(r)` falls before case 200 | **≥ 2/3** | **< 2/3** |
| **RL-c** | **What the loop lacks is the trigger.** Asking also on errors buys at least a tenth of the function | the median over `e`'s runs of `space(B)`, less the median over `i`'s runs | **≥ 0.10** | **< 0.10** |
| **RL-d** | **Asked on its errors, the loop compiles the policy**, within a tenth of the space of compiling it once | the median over `e`'s runs of `space(B)` | **≥ 0.90** | **< 0.90** |
| **RL-e** | **Beyond the keyword, its placements point at the better rule**, as the list orders it | the direction, by older rule, pooled over both arms' runs, on the half of the space without the keyword; at least 20 units | **≥ 0.90** | **< 0.90** |
| **RL-f** | **And they know more than a fixed ranking of the queues** | `RL-e`'s reading, less the Stage C ranking's reading on the same pairs and units; unadjudicable whenever `RL-e` is | **≥ 0.00** | **< 0.00** |
| **RL-g** | **Asked on its errors, the loop compiles the rarest queue** | the median over `e`'s runs of `recall_ONCALL_ESCALATION(B)` over the space | **≥ 0.90** | **< 0.90** |
| **RL-h** | *Reported, not adjudicated.* **What the drafter could not band** | Every run of both arms on every surface: `space` whole and on each keyword half, `corpus(B)` read whole, the recall of all eight queues on both surfaces, `K-a`, and `cover(r)`. `PLAN_REUSE.md`'s online set per run: reuse, silent error, online e2e, the record's `prop`, escalations by cause (impasse, conflict, error), CONFLICTs, rules born and copies born. Every escalation's verdict, with its finish reasons. The placement rounds: the sizes of their lists, citations of `H01` to `H29`, and edges by the engine's verdict. `RL-e`'s reading on the whole space and on the corpus cases without the keyword, pooled over pairs and by declared winner, with the largest unit, the ties, *the new rule always wins* on the same pairs, and `B-d`'s split. The fill of the order's room, beside the same edges pointed by a coin and by the Stage C ranking. Each born rule against the list: whether its region is a listed rule's, and the governing rule's. `ONCALL_ESCALATION`'s and `SECURITY_INCIDENT`'s escalations and compiled decisions. The transcriber references beside each arm. `PLAN_MANUAL.md`'s level-3 runs beside the impasse arm, figure by figure, across dates and protocols. The rules `PLAN_REASONED_RULE.md`'s rule arms wrote, by governing rule. The calls: providers, finish reasons, tokens, reasoning tokens, seconds by round, and retries by cause. The reasoning, recorded whole and not coded | — | — |

**Signed by Sergi: Sergi Parpal (date: 2026-10-31)**

**Why each row, and why these lines.**

- **`RL-a` bridges the loop to the re-ask.** Its line is `RR-c`'s, so that a
  reading here and `RR-c`'s there mean the same thing. The first call is the
  reasoning rule arm's prompt in all but the line that stands for the base. The
  population is not that arm's: it is the loop's own escalations, the error
  arm's included.
- **`RL-b` reads the mechanism the transcriber shows.** A tenth of the arrivals
  is 200 cases. The transcriber covers the space at case 1, and the first five
  `H29` tickets arrive at cases 1, 21, 50, 64 and 86. It is counted in runs, as
  `PLAN_SPOTCHECK.md`'s findings ask of a quantity a run gets all at once or not
  at all.
- **`RL-c` is the plan's comparison.** The arms differ in the trigger and nothing
  else, on one day, under one provider. The line is `G-d`'s, a tenth of the
  space.
- **`RL-d` is `G-d` read the other way.** Compiled once, the 29 rules decide the
  whole space (`G-a`), and within a tenth of that is 0.90.
- **`RL-e` reads the edges where `K-b` read them.** It is beyond the keyword, by
  older rule, so that the two readings mean the same thing. `K-b` read 0.5460
  without the manual and without reasoning.
  - The list fixes the direction of every pair, and with reasoning the model
    applied the list (`FM-e`, `RR-c`).
  - The line is `RR-c`'s and `FM-e`'s, a tenth below exact.
- **`RL-f` is `K-c`, with `K-c`'s line.** A ranking of the queues reads no rule,
  and it pointed `K-b`'s pairs at 0.7219, so `RL-e` alone could read a direction
  a lookup table matches.
- **[ADDED BEFORE SIGNATURE, 2026-10-31] What exact list order reads on these
  two statistics.** It is found by placing every edge of the transcriber's
  error run by the list's order.
  - **`RL-e` reads 71/75, 0.9467, not 1.** Its *better rule* is the one whose
    queue is right more often over the pair's shared region beyond the keyword.
    A third rule above both can govern most of that region with the later rule's
    queue, and then the list's earlier rule is not the better one. So `RL-e`'s
    line leaves less than a twentieth for the proposer's own errors, on a base
    of the list's rules.
  - **`RL-f` reads 23/450, 0.0511.** On the same pairs the Stage C ranking
    reads 403/450. A placer that follows the list exactly beats a fixed ranking
    by about a twentieth there.
  - **No line moved.** Both figures are Stage A's, beside the transcriber's
    other figures. Sergi may move either line at signature, and that is his to
    decide.
- **`RL-g` reads `STATUS.md`'s third open item.** No loop has compiled
  `ONCALL_ESCALATION`. Compiled once, every ask at every level put the class
  right on every point of its region (`FINDINGS_MANUAL.md`). The line is a tenth
  below whole.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **`STATUS.md`**:
  - its opening, to the dated notes under its one-sentence headline;
  - the scoreboard's opening and its tally;
  - *What is open*, with every dated note in it;
  - *What this does not show*.

  Not *What is established*, nor *What was withdrawn*, nor the scoreboard's
  table.
- **`IDEAS.md`**:
  - its header and *No longer here*, and *Pending and already specified*;
  - the sections on `PLAN_REASONED_RULE.md`, `PLAN_FIRST_MATCH.md`,
    `PLAN_QUEUE_ALONE.md`, `PLAN_APPLY.md` and `PLAN_MANUAL.md`;
  - *What the outside reading of October 2026 proposes*, and *What
    `ARBITRATION_REPORT.md` §7 proposes*;
  - *Technical debt*'s *What that leaves open*, and *Prior to the four rungs*;
  - the titles of the items in every other section.
- **The reasoned-rule thread.** `PLAN_REASONED_RULE.md` and
  `FINDINGS_REASONED_RULE.md`, whole, with every figure they publish.
- **The manual thread.** `PLAN_MANUAL.md` from its opening to the end of §3, and
  `FINDINGS_MANUAL.md` from its opening to the end of Stage C, with the figures
  they publish there.
- **The blind thread.** `PLAN_BLIND.md`'s §0, and `FINDINGS_BLIND.md`'s summary
  and verdict table.
- **The three analytical documents `CLAUDE.md` asks a new one to read first.**
  They were not read whole for this plan. The passages it rests on were read
  directly:
  - `ARBITRATION_REPORT.md` §5, its diagnosis, and §9, its limits;
  - `CHAT_SUMMARY.md`'s header, §1, and §2 with its errata, as
    `PLAN_PAIRWISE.md` §4's rule C asks;
  - `EXTERNAL_REVIEW.md` §5.
- **`results4/FINDINGS4.md`**: the lines that define its asymmetry parameter.
- **The code the package calls, read whole unless marked.**
  - `rung2/engine2.py`, `rung2/proposers2.py` and `rung2/shadow2.py`.
  - `blind/protocol.py` and `blind/loop.py`, and `blind/rows.py` to `K-c`'s room.
  - `overlap/protocol.py`, `overlap/loop.py` and `authorship/protocol.py`.
  - `manual/run.py`, `manual/prompts.py`, `manual/texts/rules.txt`, and
    `manual/instrument.py`'s `over_space`, `over_corpus` and `final_engine`.
  - `first_match/plan.py`, and `first_match/ask.py`'s `Asker`.
  - `rung2/hidden_priority.py`'s derivation.
  - `reuse/plan.py`'s gate.
  - `tests/test_prose_tables.py`'s `THREADS`.
- **Records read for a figure.**
  - `results_reasoned_rule/ask_pass1.json` and `ask_pass2.json`: the rules the
    two rule arms wrote, read against the rule that governs each ticket.
  - `results_reasoned_rule/sample.json`'s and `results_manual/loop_L3_r1.json`'s
    system prompts, compared with `manual.prompts.loop_system_prompt(3)`. All
    three are one text: 5,044 characters, digest `7b883f03a863d647`.
- **Figures computed while drafting**, by scripts kept outside the tree. Stage A
  recomputes the first five, and its record will own them. None of them reads an
  answer this plan buys.
  1. **The `H29` tickets.** 163 of the 2,000 arrivals; the first five at cases 1,
     21, 50, 64 and 86.
  2. **The rare queues' tickets.**
     - `ONCALL_ESCALATION` has 7 tickets, at cases 257, 710, 954, 982, 1432, 1783
       and 1951. `H04` governs 4 of them and `H05` 3.
     - `SECURITY_INCIDENT` has 20, `ACCOUNT_MANAGER` 109 and `T3_ENGINEERING` 117.
  3. **The transcriber under the impasse trigger** (§5.6).
     - It escalated at cases 0 and 1, wrote `H13` and `H29`, and asked nothing
       after.
     - Its base decides 14,820 of the 134,400 points right, 0.1103, and 298 of
       the 2,000 arrivals, read whole.
  4. **The transcriber under the error trigger.**
     - It escalated 23 times: 2 impasses and 21 errors, the last at case 954.
     - It wrote 23 of the hidden rules: all but `H21`, `H22`, `H23`, `H25`,
       `H27` and `H28`.
     - Its placement rounds made 148 declarations, every one accepted.
     - Its base decides 134,380 of the 134,400 points right. Its `K-a` is 1/20.
     - Beyond the keyword it holds 64 pairs that cross without nesting, 59 with
       a strict better rule, on 15 older rules.
  5. **The rules `PLAN_REASONED_RULE.md`'s rule arms wrote, by the rule that
     governs the ticket.** Over both passes' valid answers:

     | governing rule | answers | reasoning rule arm: the governing region | inside it | rule arm: the governing region |
     |---|---|---|---|---|
     | `H29` | 28 | 12 | 16 | 1 |
     | `H28` | 16 | 10 | 6 | 0 |
     | `H16` | 34 | 23 | 10 | 4 |
     | `H18` | 40 | 19 | 15 | 0 |
     | `H12` | 16 | 9 | 7 | 0 |

     The rule arm without reasoning wrote `H29`'s region, the whole space, on 6
     of its 342 answers, 5 of them on tickets other rules govern.
  6. **Under random escalation, not part of this plan.** The transcriber was
     also escalated at random on a share of the covered arrivals, three draws
     each:

     | share escalated | escalations | `space` |
     |---|---|---|
     | 2% | 40 to 48 | 0.41 to 0.45 |
     | 5% | 104 to 132 | 0.56 to 0.83 |
     | 10% | 187 to 215 | 0.59 to 0.92 |

     Sergi saw these figures when he chose the arms.
  7. **A stand-in for the proposer, for pricing only.**
     - **What it does.** It takes the governing queue 0.967 of the time, and
       otherwise the runner-up's. It writes the governing rule's region 0.73 of
       the time, and `H29`'s 0.43, and otherwise that region narrowed by one of
       the ticket's values. It points each placed edge right with a fixed
       chance, and a placement is refused 0.05 of the time.
     - **What it asked.** Over three draws at each setting:
       - under the impasse trigger, 2 to 88 times a run;
       - under the error trigger, 30 to 147 times.
     - **When its impasse arm covered the space.** In one draw of three it
       covered at case 1. In the others it covered at cases 100 and 147 with
       edges right 9 times in 10, and at 956 and 1,742 with every edge right.
     - **Where it stands.** It is kept nowhere, and no row and no reference reads
       it.
- **Writing the package, after the draft above was committed.**
  - **The code it calls**, read for its signatures and behaviour:
    - `authorship/run.py`'s `Resumable`, `open_partial` and `digest`;
    - `authorship/loop.py`'s `Escalation`, `call_row` and
      `install_declarations`;
    - `blind/loop.py`'s helpers, `blind/gates.py`'s `witness`, and
      `blind/readings.py`'s `read_run`;
    - `edges/rebuild.py`'s `rebuild`, `manual/score.py`'s `first_full_cover`,
      `queue_alone/rules.py`, `reasoned_rule/shape.py`, and the entry points of
      `reasoned_rule/gates.py` and `reasoned_rule/score.py`;
    - `reuse/gates.py`'s `run_suite`, `reuse/structure.py`'s `arbitration`,
      `harness/call_record.py` and `tests/doubles.py`.
  - **The lists the plumbing joins**: `tests/test_call_record.py`'s call sites,
    `tests/test_oracle_separation.py`'s watched modules, and
    `tests/test_writer_lists.py`'s guarded writers.
  - **The package's checks, run before the signature.** `RL-g1` to `RL-g3` pass
    with the suite green. They recompute `PLAN_REASONED_RULE.md`'s four
    verdicts and `PLAN_MANUAL.md`'s level-3 figures and compare them with their
    records. They recompute figures 3, 4 and the hidden policy's, and compare
    them with this list. Every one came back.
  - **Stage A's other figures, recomputed while writing it.** Figures 1, 2 and
    5 came back as listed.
  - **Stage C, run on copies of the transcriber's runs.** To try the scorer, the
    drafter scored three copies of each arm's transcriber run, in memory, never
    written. That printed §0's seven statistics on the transcriber:

    | row | the transcriber's reading |
    |---|---|
    | `RL-a` | 1 |
    | `RL-b` | 1, every run covering the space at case 1 |
    | `RL-c` | 427/480 |
    | `RL-d` | 6,719/6,720 |
    | `RL-e` | 71/75, on 15 units a run, 55 of 59 strict pairs |
    | `RL-f` | 23/450, the Stage C ranking reading 403/450 |
    | `RL-g` | 1 |

    None of them is an answer of the model. **`RL-e`'s and `RL-f`'s were not
    foreseen**, and they bear on how those rows read (*Why each row*, below).
    Stage A records them, beside the transcriber's other figures.
  - **Every test builds its rules, tickets, engines and runs by hand.**
- **OpenRouter.** Not read for this plan. §3 cites the price
  `PLAN_FIRST_MATCH.md`'s drafter read on 2026-10-25.

**Not seen, because nothing has produced it:**

- any loop run with reasoning on;
- any placement answer given with reasoning on;
- any base such a loop compiles;
- any escalation triggered by an error, at any setting;
- how long a reasoning placement round takes, and so the pace of a run (§1).

**What the drafter expects, written down so the scoreboard can score it.**
**All seven hold.** The drafter trusts `RL-c` most, then `RL-a`, `RL-f`, `RL-e`,
`RL-g` and `RL-d`, and `RL-b` least.

- **`RL-a` holds.** The reasoning rule arm was right on 0.9672 of level 3's
  escalated decisions, and this first call differs from its prompt in one line.
  Against it:
  - an error escalation is a ticket the base decided wrongly, often an exception
    under a broad rule;
  - the reasoning rule arm's few errors lay under such rules: `H18`, `H23` and
    `H26`.
- **`RL-b` holds, and the drafter trusts it least.** The transcriber covers the
  space at case 1, and the reasoning rule arm wrote `H29`'s region on 12 of 28
  answers. Against it:
  - **the stand-in covered before case 200 in only some draws**: two of three at
    one setting, and one of three at the other;
  - **here the line for the base reads differently.** It says *no se te muestra
    en este paso*, where `PLAN_REASONED_RULE.md`'s read *vacia. Esta es la
    primera regla*, and a proposer told a base exists may write narrower;
  - **a narrower `T1_GENERAL` rule can hide later `H29` tickets.** If it covers
    them, they never escalate and are never written.
- **`RL-c` holds, by a wide margin.** If `RL-b` holds, the impasse arm's base is
  a few rules under a default. If not, that arm still never asks where a rule
  already decides wrongly, and the error arm does. Against it: if the error arm's
  placements are often refused or wrong, that arm compiles less too.
- **`RL-d` holds.** The transcriber decides all but 20 points of the space with
  23 asks. The stand-in reached 0.93 to 1.00 when 9 edges in 10 pointed right.
  Against it:
  - refused placements, wrong edges and narrower rules;
  - the space's regions where no arrival falls;
  - the cap of §1.
- **`RL-e` holds.** Placing a rule against another is a question about two
  rules. Without reasoning, shown two hidden rules and a witness ticket, the
  model named the right winner on 0.8824 of the hidden policy's clean pairs
  (`FINDINGS2.md`, Stage C). Against it:
  - the base's rules are not all the list's rules;
  - the lists can be long, and the slot decides some answers
    (`PLAN_PRIMACY.md`);
  - an edge that a narrower rule declares is right over a region the list
    describes only in part;
  - **[added before signature, 2026-10-31]** a placer that follows the list
    exactly reads 71/75 on the transcriber's base, so the proposer has less
    than a twentieth to lose.
- **`RL-f` holds.** The policy points some queue pairs both ways (`B-d`'s split),
  and a ranking cannot follow them. Against it: on pairs a ranking answers, a
  ranking is right whenever the list is.
- **`RL-g` holds.** Under the error trigger, an `ONCALL_ESCALATION` ticket the
  base decides wrongly escalates, and the reasoning rule arm named the queue on
  every such decision (18 of 18). Against it:
  - a narrower rule leaves part of the region to the severity-1 rules;
  - an edge misplaced against `H09` or `H13` gives part of it to
    `ACCOUNT_MANAGER`.

**The drafter's record argues against trusting that.**

- **The scoreboard.** On `STATUS.md`'s, 51 of 127 adjudicated rows were refuted.
- **The last plan.** `PLAN_REASONED_RULE.md`'s drafter expected four holds and
  got three, and missed the row it trusted least.
- **This plan expects every row to hold.** Six of the seven rest on the
  transcriber and on one re-ask, and neither is a loop that reasons.
- **What was done about it, rather than said.**
  - No band here was set on a development set.
  - Every line is a closed thread's or the claim's own edge. `RL-a`'s and
    `RL-e`'s are `RR-c`'s, `RL-c`'s and `RL-d`'s are `G-d`'s, and `RL-f`'s is
    `K-c`'s.
  - A verdict a single run carries is labelled *thin* in advance.

Sergi should read the bands as more likely too comfortable than too strict, and
tighten them at signature if he disagrees.

**How the rows read together.**

- **`RL-b`, `RL-c` and `RL-d` hold.** A proposer that applies the list stops
  the standing loop from asking, and a loop asked on its errors compiles the
  policy. What limits the loop is the trigger, not the order.
- **`RL-c` holds and `RL-b` is refuted.** The impasse arm kept asking and still
  compiled less: it never asks where a rule already decides wrongly. The trigger
  is still the limit, by a different route.
- **`RL-c` is refuted.** The error arm compiles no more than the impasse arm.
  `RL-e` and the refusals reported in `RL-h` then say whether the order failed
  them both.
- **`RL-d` is refuted while `RL-e` holds.** The error arm placed its rules right
  and still fell short. The narrower rules, the refusals and the cap, all in
  `RL-h`, say why.
- **`RL-e` is refuted.** With the list in front of it and reasoning on, the
  proposer still does not place its rules the way the list orders them.
  - `RL-f` then says whether a ranking does better.
  - `RL-h` says whether the identifiers of the manual took the place of the
    base's.
- **`RL-a` is refuted.** The proposer of the loop is not the proposer of the
  re-ask. The first call's base line and the error arm's tickets are what
  differ, and `RL-h` splits the drafts by cause.
- **`RL-g` holds.** For the first time a loop compiles `ONCALL_ESCALATION`.
  `STATUS.md`'s third item narrows to a trigger a deployment could have.

---

## 1. What is bought, and what is already paid for

**Already paid for, and free to read.** Read-only, under hard rule 4:

- **`results_manual/loop_L3_r{1..3}.json`** and **`results_manual/score.json`**:
  `PLAN_MANUAL.md`'s level-3 loop and the rules compiled once. They are
  references, and `RL-h` sets them beside the impasse arm.
- **`results_reasoned_rule/`**: `RR-c`, the pace and the reasoning tokens of a
  reasoning rule ask, and the rules its arms wrote.
- **`results_blind/score.json`**: `K-b`'s and `K-c`'s readings.
- **`results_reuse/run_n2000_r{1,2,3}.json`**: the corpus labels, as
  `manual.instrument` reads them. They are also what the error arm's trigger
  reads (§5.3).

**Bought.** Two arms of three loop runs each at n=2000, and one smoke run of 30
cases under the error arm.

- **Every call goes through `PLAN_FIRST_MATCH.md`'s asker**, with this plan's
  request, and through `harness/call_record.py`.
- **Every request sends**:
  - the model and temperature 0, with `response_format` on the first attempt;
  - reasoning `{"effort": "high"}` and 16,000 tokens;
  - the provider pin of §2.5.

**The calls.** One per escalation, and a second when the placement round has
rules to list (§5.2).

| run | the transcriber's calls | the stand-in's escalations |
|---|---|---|
| an impasse run | 2 | 2 to 88 |
| an error run | about 45 | 30 to 147 |

The transcriber's calls are recomputed by Stage A. The stand-in's escalations are
the drafter's pricing aid only (§0). An escalation is one or two calls.

**The cap.** A run stops at its 400th escalation, at most 800 calls. Its record
says so, its final base is the base at that case, and the rows read it as a run
(§0). Neither the transcriber nor the stand-in came near it.

**The money.** The price is Baidu's listing for this model on 2026-10-25:
$0.02226 per million prompt tokens and $0.04452 per million completion tokens
(§3).

- **A first call** sends about 1,850 prompt tokens. That is
  `PLAN_REASONED_RULE.md`'s rule prompt and one longer line.
- **A placement call** sends a few hundred more: the first answer, and the
  listed rules.
- **The completions.** A reasoning rule ask took a median of 2,126 and 2,288
  reasoning tokens in the two passes of `PLAN_REASONED_RULE.md`, and at most
  11,430.
- **At the cap**, 4,800 calls each spending its 16,000 tokens would cost under
  four dollars.
- **At any length the drafter expects**, the six runs cost under a dollar.

**The time.** A reasoning rule ask took 22.74 and 24.72 seconds at the median.

- **The placement call's pace is not known**, because nothing recorded has
  reasoned before placing. **The smoke run measures both calls before the first
  run.** It rests on about ten escalations, and the findings will say how far
  the estimate was.
- **At 25 seconds a call:**
  - an impasse run takes from a minute to over an hour;
  - an error run from about twenty minutes to a few hours;
  - a run at the cap, nearly six hours.
- **Every run belongs in Sergi's terminal**, because it outlives a background
  command of the agent's harness.

**What is not bought.**

- **A reasoning-off arm under v1b.** It would isolate reasoning in the loop. The
  impasse arm is set beside `PLAN_MANUAL.md`'s level-3 runs instead, across
  dates and protocols, and reported (§13).
- **Random escalation**, `IDEAS.md`'s candidate that reads no truth. Its
  transcriber figures are above.
- **No other level**, no screen, no other model, provider, effort or budget.

---

## 2. The choices that have to be made at signature time

Each is the drafter's recommendation, and each is Sergi's to overrule. A choice
that changes a row is a change to §0, and belongs in the same signed commit. The
two choices Sergi made before the drafting, the placement round and the two
arms, are not repeated here.

### 2.1 The first call is blind, at every escalation — the drafter recommends it

The first call shows no rule of the base: where v1 shows its screen, v1b sends
v2b's line, `BLIND_BASE`. Four reasons:

- **v1's screens state facts that are false at an error escalation.**
  - A coverage screen opens *"ninguna casa este ticket"*.
  - A conflict screen says the engine *"no ha podido decidir"* because the rules
    conflict.
  - On a ticket a rule decided wrongly, both are false. A blind line is true at
    every escalation, so the arms can send the same prompts.
- **The first call is then the reasoning rule arm's prompt** in everything but
  that line, and `RR-c` measured that prompt.
- **The screen's pull is not known with reasoning on.** `PLAN_SCREEN.md` and
  `PLAN_APPLY.md` measured it with reasoning off. A blind first call keeps that
  unknown out of every row.
- **`PLAN_BLIND.md`'s blind draft made the proposer cross** (`K-a`), and a
  stratified base crosses.

**The alternative** keeps v1's screen on an impasse and a conflict, and goes
blind only on an error. The arms would then differ in their prompts as well as
in their trigger, and `RL-c` would read both differences together.

### 2.2 The placement round is v2b's, and a refused rule is not born — the drafter recommends it

**Placement.** After the first call, the engine lists the existing rules of
another queue that the draft overlaps. It asks for **the same rule**, placed
against each of them, in `PLACEMENT_TEMPLATE`'s words. The second answer is held
to v2b's validator:

- it must be a rule that matches the ticket;
- it must be the draft's rule, with the same queue and the same extension;
- it must place every listed rule, by citing it in `beats` or `loses_to`.

A failure is refused with its verdict, and a refused rule is not installed, as
in v2b.

**The alternative** installs the draft with whatever edges the second answer
placed, and records the rest. It would keep rules a strict validator throws
away. It would also install rules that cross without an order, which is what the
placement round is for.

### 2.3 A copy is born — the drafter recommends it

v1b has no copy check. A rule whose extension equals an existing rule's is born
and placed like any other, as in v1. v1e, v2e and v2b refused copies. Two
reasons not to here:

- **A blind draft cannot see what exists**, so a copy is not the proposer's
  choice.
- **At a conflict or an error, a copy is how a blind proposer corrects the
  base.**
  - A wrong rule is corrected by the same region with another queue, placed
    above it.
  - A conflict is resolved by a copy of the rule that should win, placed above
    the other.
  - Refused, the region would err or conflict forever, and under the error
    trigger every later ticket in it would escalate.

**The alternative** is v1e's refusal, with the same counts reported.

### 2.4 The reasoning setting is `PLAN_FIRST_MATCH.md`'s, on both calls — the drafter recommends it

**`{"effort": "high"}`, with `max_tokens` 16,000**, imported from
`first_match/plan.py` and not retyped. It is the setting `RR-c` was read under.
The longest reasoning rule answer took 11,585 tokens. A placement answer cites
more rules, and the smoke run must show that it fits (§9).

**The alternative** gives the placement call a larger budget. Baidu's listing
allows up to 131,072 completion tokens. The two calls of one escalation would
then carry different settings.

### 2.5 One provider, pinned — the drafter recommends Baidu

**Every request carries OpenRouter's provider routing, with fallbacks off:**
`{"order": ["baidu"], "allow_fallbacks": false}`. It is `PLAN_FIRST_MATCH.md`'s
pin, imported and not retyped. It served every answer of `PLAN_FIRST_MATCH.md`'s
and `PLAN_REASONED_RULE.md`'s passes. `PLAN_MANUAL.md`'s loop runs were served by
eight providers under one name.

### 2.6 Three runs an arm, the arms alternating, and the cap — the drafter recommends it

- **Three runs** is `PLAN_REUSE.md`'s and `PLAN_MANUAL.md`'s count.
- **The order.** `ORDER_SEED` draws which arm runs first, and then the arms
  alternate: one run of each in every repetition. If Stage B spans two days,
  both arms have runs on both.
- **The cap**, 400 escalations a run, is set so that a run that keeps erring
  ends. It is not set to bound what a run may compile.

### 2.7 `PREDICTION.md`

Not touched. It is rung 1's long run, and this plan is not it (hard rule 2).

---

## 3. Reference figures, with the record that owns each

Nothing here is produced by this plan. `RL-g1` recomputes what it checks against
its record, rather than publishing it again.

| figure | value | owning record |
|---|---|---|
| the 29 rules compiled once, `C₃` | 1.0000 of the space, in every ask (`G-a`) | `results_manual/score.json`, published by `FINDINGS_MANUAL.md` |
| `PLAN_MANUAL.md`'s level-3 loop, reasoning off, v1's screen, the standing trigger, 2026-10-21 | `space` 0.3339, 0.3952 and 0.3778, median 0.3778; `corpus` 0.6475, 0.4995 and 0.655; `K-a` 0.7439, 0.6667 and 0.7349; `prop` 183 of 323, 0.5666 | same |
| the same runs' dropped declarations, and their space | 29, 26 and 6 declarations against the manual's identifiers, dropped as outside the neighbourhood; no run's base covered the whole space | same, Stage B2 and *The loop* |
| `ONCALL_ESCALATION` in the loop with the manual | named right on all 9 of level 3's escalations of the class; a later ticket of the class decided right once in the six runs of levels 2 and 3 | same, *The two classes, and the rarest* |
| the reasoning rule arm, at level 3 | 0.9672 of 320 decisions (`RR-c`); its rule the governing rule's region on 250 of 342 answers; 43 answers declaring an edge, every one citing `H01` to `H29` | `results_reasoned_rule/score.json`, published by `FINDINGS_REASONED_RULE.md` |
| its reasoning and pace | 400 to 9,883 reasoning tokens in pass 1, median 2,126; 390 to 11,430 in pass 2, median 2,288; 22.74 and 24.72 seconds an ask at the median | same, Stage B |
| `K-b` and `K-c`, v2b, reasoning off, no manual | 0.5460 by older rule, on 65 units; the Stage C ranking 0.7219 on the same pairs, so `K-c` −0.1759 | `results_blind/score.json`, published by `FINDINGS_BLIND.md` |
| rung 2's ceiling | 1.0000 on the corpus and over the space, with 199 declared edges; subsumption alone 0.6315 and 0.261176 | `results2/ceiling2.json` and `ceiling2_space.json`, published by `FINDINGS2.md` |
| the hidden policy's own `K-a` | 1/13 | `results_manual/sample.json`, published by `FINDINGS_MANUAL.md` |
| the pairwise question at level 3, reasoning off | the right winner on 0.8824 of 170 clean pairs | `results2/pair_judgement_baselines.json`, published by `FINDINGS2.md`, Stage C |
| Baidu's listing for the model | `baidu/fp8`; $0.02226 per million prompt tokens and $0.04452 per million completion tokens; up to 131,072 completion tokens | OpenRouter's endpoints listing, read on 2026-10-25 by `PLAN_FIRST_MATCH.md`'s drafter. Not a record of this repository |

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
4. **Seed 17, no regeneration.** Every record under `results_manual/`,
   `results_reasoned_rule/`, `results_blind/` and `results_reuse/` is read-only.
   `harness/record_guard.py` guards this plan's paid records, and the flag that
   overrides it is not typed without Sergi asking.
5. **Do not adjust a prompt, a text or the schema.**
   - The system prompt is `manual.prompts.loop_system_prompt(3)`, byte for byte.
   - The user message is `rung2.proposers2.user_msg` over v2b's `BLIND_BASE`.
   - The placement message is v2b's `PLACEMENT_TEMPLATE`.
   - The retry message is v1's.
   - Once the smoke run has been read, nothing moves.
6. **If the numbers come out badly, report them.** A loop that reasons and
   compiles nothing is a result, and so is a trigger that changes nothing.
7. **The API key goes in the environment.** It is loaded without printing,
   checked by its length, and read off OpenRouter's key endpoint as an API key
   and not a management key before any call (`reuse.run.key_check`).

And this plan's own, lettered:

A. **Called and not edited:** `blind/`, `overlap/`, `authorship/`, `manual/`,
   `first_match/`, `reasoned_rule/`, `reuse/`, `edges/` and `rung2/`.
   - The texts are `blind.protocol`'s and `manual.prompts`'.
   - The validator's parts are `blind.protocol`'s and `authorship.protocol`'s:
     `split_overlapped`, `listing`, `same_rule`, `unplaced` and
     `placement_message`.
   - The declarations are installed by `authorship.loop.install_declarations`.
   - The asker is `first_match.ask.Asker`, with this plan's request.
   - The instrument is `manual.instrument`'s and `blind.rows`'.

B. **No label reaches a prompt.**
   - **The error trigger reads the corpus labels, handed in**, as v2e's and v2b's
     loops read theirs: from `PLAN_REUSE.md`'s records, never from the oracle.
   - **No module on the proposer's path imports the oracle.** That path is
     `reasoned_loop/protocol.py`, `reasoned_loop/loop.py` and
     `reasoned_loop/run.py`. None of them imports by name the oracle,
     `HIDDEN_DSL`, `harness.ceiling_check` or `rung2.hidden_priority`. All three
     join `ONLINE_LOOP` and the authority channel's watch.
   - **The transcriber references read level 3's text** by first match, and the
     corpus labels. They are never on the proposer's path, and the list of
     modules allowed to see the oracle does not grow.

C. **Every record carries `_env`**, with:
   - the model, the temperature, the reasoning setting, the token budget and the
     provider pin;
   - the arm, the run, and the digests of the system prompt, `BLIND_BASE` and
     `PLACEMENT_TEMPLATE`;
   - every call's `call_attempts`, and the cause of every retry.

   Every command runs with `PYTHONHASHSEED=0` set explicitly.

D. **The constants of §11 are fixed here and pinned by tests**, so that moving
   one after a figure exists is visible in a diff.

E. **What the model writes is recorded whole**, because `Rule2` keeps only a
   note's first 280 characters. That covers every call's payload with its keys
   in the order written, and its reasoning when the response carries it. No
   stage codes a note or the reasoning.
   - **[Corrected before signature, 2026-10-31] The raw text is not kept.**
     This rule read *its raw text* in the payload's list. The asker of rule A
     is called and not copied. It keeps the payload it parsed, and not the text
     it parsed it from. So every call row records `raw` as None.

F. **The order of Stage B is §9's**, and the module refuses a run out of it.

G. **The provider is pinned on every call.** A call that another provider served
   is recorded. Its answer still decides the case and still writes its rule,
   because a loop cannot skip an escalation. It is counted, and `RL-h` reports
   it by run.

H. **A failed call is never answered with v1's retry message.** Only a failed
   parse is (`PLAN_FIRST_MATCH.md`'s rule).

I. **The error arm's trigger reads the truth and nothing else does.** The engine
   never sees a label. The proposer never sees one, and is never told that the
   base erred.

---

## 5. The protocol, v1b

### 5.1 The texts — none is new

| text | what it is | where it comes from |
|---|---|---|
| system prompt | v1 with level 3's manual inserted before the operators: 5,044 characters, digest `7b883f03a863d647` | `manual.prompts.loop_system_prompt(3)`, which `PLAN_MANUAL.md`'s level-3 loop and `PLAN_REASONED_RULE.md`'s two rule arms sent |
| user message | `TICKET EN IMPASSE:` and the ticket, after the line that stands for the base | `rung2.proposers2.user_msg` |
| the line for the base | *"BASE DE REGLAS: no se te muestra en este paso. Escribe tu regla para este ticket; si se solapa con reglas existentes de OTRA cola, se te listaran despues."* | `blind.protocol.BLIND_BASE` |
| the placement message | the overlapped rules of another queue, rendered as the engine renders them, and the request for the same rule placed against each | `blind.protocol.PLACEMENT_TEMPLATE`, filled by `blind.protocol.placement_message` |
| the retry message | *"Tu respuesta anterior no era JSON valido…"* | v1's |

`RL-g2` checks each by digest against its source.

### 5.2 One escalation, in either arm

1. **The draft.** The first call sends the system prompt and the user message.
   Its answer decides the case online, as in every loop, until a second answer
   replaces it.
2. **The draft is read.**
   - An answer carrying `order` is refused, as on any v2b impasse.
   - A rule that fails rung 2's validator is rejected. It must match the ticket.
   - The draft's own `beats` and `loses_to` cite nothing listed. They are
     recorded and never installed.
3. **`O` and `S`.** `O` is the existing rules of another queue whose extension
   meets the draft's; `S` is those of its own queue. Both are recorded on the
   call (`blind.protocol.split_overlapped`).
4. **No rule to place.** With `O` empty, the rule is born with no second call.
5. **The placement.** Otherwise one placement round lists `O`, in
   `blind.protocol.listing`'s seeded order. The second call sends the first two
   messages, then the draft as the assistant's turn, then the placement message.
   - **[Corrected before signature, 2026-10-31] The turn is the draft's payload,
     serialized**, its keys in the order the model wrote them. This step read
     *the draft's raw text*, which is what v2b sent. The asker keeps no raw text
     (rule E).
6. **The second answer** decides the case. It is held to §2.2's validator. A
   rule not the draft's is refused as *changed*. A rule leaving a listed rule
   unplaced is refused as *unplaced*. A placement that never came back is
   refused as *unplaced*.
7. **The birth.** The rule is installed, and its citations of listed rules go
   through `try_edge`, each with the engine's verdict:
   - `ok`;
   - redundant with containment;
   - against containment;
   - closing a cycle.

   A citation of anything not listed is dropped and recorded: an identifier of
   the manual, or a rule not in `O`.

### 5.3 The two triggers

- **The impasse arm** escalates a case when the engine returns IMPASSE or
  CONFLICT, as every loop has.
- **The error arm** escalates on those, and also when the engine returns ACTION
  with a queue that is not the case's label. The label is handed in, as rule B
  says.
  - The record keeps the cause of every escalation: impasse, conflict or error.
  - On an error it also keeps the queue the engine gave, and the rule that gave
    it.
  - **[Added before signature, 2026-10-31] An error escalation's rule is not
    counted as fired.** Its decision did not stand: the proposer's answer
    replaced it, as at any escalation. So rung 2's reuse figures mean the same
    under both arms.

### 5.4 What a run records

- **The header.** The protocol, the arm, the run, the seed, the digests and the
  settings.
- **The engine's state.** `metrics`, from `rung2.shadow2.compute_metrics2`, and
  every rule in birth order. `edge_log`, with each edge's channel.
- **Every case's row**, with its cause when it escalated.
- **Every escalation whole.** Its calls, each with:
  - the payload, its keys in order, its raw text and its reasoning;
  - `call_attempts`, `finish_reason`, the seconds and the retries by cause.

  Then `O`, `S`, the listing, what was left unplaced, and the verdict.
- **Two counts.** `cover(r)`. How many calls another provider served.

### 5.5 A run that dies keeps what it paid for

> **[AMENDED 2026-10-31 — drafted by Claude after the smoke run's third launch,
> before any run of §2.6 and before any figure of §0 existed. One change to how
> a call refused for the rate is waited for and recorded.]**
>
> **What the smoke run met.** It was launched three times on 2026-10-31. Each
> launch stopped on five failed calls in a row, the last of each refused with
> HTTP 429, *"temporarily rate-limited upstream"*. When the second stopped,
> OpenRouter's endpoint listing gave Baidu's endpoint as up, with full uptime
> over the last half hour.
>
> - **The first two**, stopped at 11:01 and 11:19 UTC, failed on their first
>   five calls and recorded nothing.
> - **The third**, launched at 15:24 UTC, recorded two calls before it stopped
>   at 15:44.
>   - Case 0's call was refused for the rate on all three of its attempts.
>   - Case 1's was refused twice and answered on its third attempt, by Baidu,
>     reasoned and ended `stop`.
>   - The next five calls failed, and the run stopped.
>
> Under this section as signed, case 0's call was kept as a failed proposal,
> because the next call was answered. `authorship/run.py`, which this section
> calls, keeps one failure as an answer the model did not give. So case 0's
> escalation has no rule because the provider was saturated, and the model never
> saw the request. **Nothing here reads an answer of the smoke run**, only which
> attempts came back.
>
> **Two things follow from the text as signed.**
>
> 1. **A call refused for the rate is recorded as an answer the model did not
>    give** whenever fewer than five fail in a row. A run would read the
>    provider's load as the model's, and every row reads which rules were born.
> 2. **The smoke check cannot pass a run that met a rate limit.** §9's step 3
>    requires every attempt to have been served by the pinned provider,
>    reasoned and ended `stop`. An attempt refused for the rate was served by no
>    one, and the third launch's partial file already holds five.
>
> **The change.**
>
> - **A call refused for the rate on every attempt is an outage, never an
>   answer.** An attempt is refused for the rate when `harness/call_record.py`
>   keeps it with `RATE_LIMITED = "RateLimitError"`, the class `openai` raises
>   on HTTP 429.
> - **It is waited out.** Such a call is asked again, with the same messages,
>   after each wait of `RATE_LIMIT_WAIT = (60, 120, 240, 480, 960)` seconds in
>   turn: about half an hour in all. The asker starts again each time, with its
>   own retries, so the first attempt after a wait carries `response_format`, as
>   a call's first attempt does.
> - **If every wait is spent, the run stops**, and the call is not recorded,
>   whatever the streak. The failures pending before it are not recorded
>   either, as on five failed calls in a row, and the resume asks them again.
>   The same command resumes there.
> - **A call any attempt of which reached the model keeps this section's rule.**
>   It is recorded if it failed alone, and five in a row stop the run. The waits
>   never ask it again.
> - **What an answered call keeps.** Its `call_attempts` and its retries by cause
>   include every attempt refused for the rate, and its seconds every wait.
> - **The smoke check reads the attempts that reached the model.** Each must have
>   been served by the pinned provider, reasoned and ended `stop`, as §9 says,
>   and there must be at least one. The attempts refused for the rate are counted
>   and fail nothing. Any other failed attempt still fails it.
> - **Stage C reports the attempts refused for the rate**, and the pace by round
>   over the calls none of whose attempts was refused, beside the pace over every
>   call (§10).
> - **The header carries `RATE_LIMIT_WAIT`.** So the third launch's partial file,
>   written under the text as signed, is refused on a resume, as a partial left
>   under another protocol is. It is kept, renamed
>   `results_reasoned_loop/loop_smoke.before_amendment.partial.jsonl` and
>   git-ignored, and the smoke run starts again from case 0. That costs the one
>   answer it paid for, under a thousandth of a dollar.
> - **The time.** A call the provider keeps refusing now waits about half an hour
>   before it stops a run, where it waited forty seconds.
>
> **What does not move.** No band, line, row, prompt, schema, setting, seed,
> trigger, the cap or the pin. No request is new: each attempt after a wait is
> the call's first attempt again, byte for byte. Only when a refused call is sent
> again changes, and what is kept of it. Stage A's record stands, since its
> fingerprint and schedule are unchanged. `MIN_SIGNATURES = 2`, so this line and
> §0's are both required. Pointers mark the sections this changes: §9's step 3,
> §10, §11 and §12.

**Signed by Sergi: ________ (date: ________)**

*Outside the quotation deliberately, as in `PLAN_REUSE.md`: the gate reads
signature lines at the start of a line, and one inside a blockquote would be
invisible to it.*

Each escalation's answers are appended, as they arrive, to a git-ignored partial
file. The same command resumes there. It replays the run from case 0 with the
recorded answers, and checks each against the request it would send. It then
goes on live.

A run of five failed calls in a row stops the run without recording them,
because an outage is not answers.

### 5.6 The references Stage A computes

- **The transcriber.** It is a double that answers every first call with the
  rule of level 3's text that governs the ticket, the first rule it matches. It
  places that rule by the text's order: a rule earlier in the list wins. It runs
  through this plan's own loop, under both triggers. It reads the text, and the
  labels for the error trigger, and never the oracle.
- **The hidden policy through v1b's path.** The 29 rules of the text are drafted
  in order and placed by the text's order. The run must give back the 199 edges
  of `rung2/hidden_priority.py` and 1.0000 on both surfaces, as `PLAN_BLIND.md`'s
  `K-g1` found for v2b's path.

---

## 6. Known traps

**6.1 — The error arm's escalations are told they are impasses.** v1 calls the
model the system's exception component, and says *"El motor simbolico no ha
podido decidir este ticket"*. The user message labels the ticket *TICKET EN
IMPASSE*.

- On an error escalation both statements are false. The engine decided, wrongly.
- The arms keep the same prompts so that the trigger is their only difference,
  and so the proposer is not told that the base erred. That fact is part of a
  label.
- A deployment that reports errors would know it. It could say so, which is
  another prompt and another plan.

**6.2 — Level 3 hands over the label** (`PLAN_MANUAL.md` §6.2). Every row
measures what the loop compiles from a policy it holds as text. None reads
level 3 as something the model knew.

**6.3 — The trigger reads the truth.** The error arm asks exactly where its base
is wrong, which no deployment knows for free. It is the most generous trigger
there is, and `RL-d` reads the error arm's compilation under it. What a trigger
that reads no truth would buy is not read here (§13).

**6.4 — The online figures of the error arm are corrected online.** Each error
escalation replaces the base's wrong decision with the proposer's answer. So its
online e2e and silent error count feedback as accuracy. They are reported beside
the impasse arm's, never set against them, and no row reads them.

**6.5 — The manual's identifiers.**

- A text that numbers its rules invites the proposer to cite them
  (`PLAN_MANUAL.md`).
- In the placement round, a citation of `H01` to `H29` is outside the listing
  and is dropped. A listed rule placed only by its manual number is left
  unplaced, and the rule is refused.
- `RL-h` counts both. If the refusals are many, the impasse arm may never write
  `H29`'s region, and the error arm will escalate again where they fall.

**6.6 — Nested pairs are placed too.** `O` holds every overlapped rule of another
queue, nested or not, as in v2b.

- A declaration that agrees with containment is accepted, and changes nothing.
- One against containment is refused by the engine and counted:
  `contradice_subsuncion`.
- `RL-e` reads only the edges entered in the graph, so neither kind enters it.

**6.7 — A copy is born** (§2.3). Two rules with one extension and one queue
change no decision. With two queues and no edge between them, they conflict on
their region. `RL-h` counts copies of each kind.

**6.8 — The listing's slot.** The listed rules come in a seeded order per case and
round, v2b's. Position may decide some placements (`PLAN_PRIMACY.md`). The
record keeps the order, so a slot reading is possible afterwards.

**6.9 — A long list and the budget.**

- A placement answer cites every listed rule, and its reasoning weighs each.
- An answer cut off by its budget comes back empty or cut short, with
  `finish_reason: "length"`. That is a failed parse, retried under rule H.
- If the retry fails too, the placement never came back, and the rule is
  refused.
- **[Corrected before signature, 2026-10-31] A placement call is retried with
  its own four messages.** The first bullet said a failed parse is retried
  *with v1's message*. `PLAN_FIRST_MATCH.md`'s asker, called and not copied,
  appends that message only to a request of two messages. That is a first
  call. A placement call's failed parse is retried with the same messages.

**6.10 — A fill rewards resolving.** No row reads the fill of the order's room.
`RL-h` sets it beside the same edges pointed by a coin and by the Stage C
ranking, as `blind/readings.py` does.

**6.11 — Edges that share a rule.** A broad rule that every later birth meets
would carry a rate pooled over edges. `RL-e` counts each older rule once,
`K-b`'s unit, and `RL-h` gives the reading by pairs and by winner beside it.

**6.12 — The surfaces.**

- `RL-c`, `RL-d` and `RL-g` read the exhaustive space. `RL-e` and `RL-f` read
  its half without the keyword. `RL-a` and `RL-b` read the run itself.
- Every space figure in `RL-h` is split by the keyword, as `PLAN_UNREACHED.md`'s
  findings ask.
- The corpus figures read the base whole. Every rule was born on an arrival, so
  they include the tickets the rules were written on.

**6.13 — Reasoning at temperature 0.** A provider may not honour temperature 0
while the model reasons. The runs of one arm may part for that reason as well as
for their bases. Each run's value is published.

**6.14 — Back-to-back runs leave `git_dirty` true**, because each finds the
earlier records not yet committed. Rule 3 of §4 commits each record before the
next run, and `code_dirty` is what identifies the code (`PLAN_MANUAL.md`'s
findings).

**6.15 — One provider is not the model.** Baidu serves this model at fp8. Every
figure here is that provider's serving of it.

**6.16 — `cover(r)` is not the end of the impasse arm.** After its base covers
the space, that arm still escalates on a CONFLICT. Under forced placement a
conflict needs a refused edge or a refused rule. So `RL-b` reads when the arm
can no longer ask about an uncovered ticket, not when it stops asking.

**6.17 — What the transcriber is not.** It writes the governing rule and places
it right every time. It bounds nothing about the model. It shows what each
trigger allows a proposer that never errs.

---

## 7. Blocking checks, before any record is written

All are free and all run by `--dry-run`. **Any failure stops the plan before a
figure exists.**

**RL-g1 — The inputs reproduce themselves.** Blocking in the sense of
`harness.ceiling_check`.

- **The suite.** `python3 -m unittest discover` is green.
- **`PLAN_REASONED_RULE.md`'s checks.** They pass through
  `reasoned_rule.gates.run_checks`, called and not copied, and they call
  `PLAN_FIRST_MATCH.md`'s and `PLAN_QUEUE_ALONE.md`'s in turn. `RR-a` to `RR-d`
  come back from its passes.
- **`PLAN_MANUAL.md`'s level-3 loop.** Its three runs, rebuilt through this
  plan's instrument, give back their `space`, `corpus` and `K-a` as
  `results_manual/score.json` records them.
- **The rebuilt base.** A run's rebuild equals the engine the run ended with,
  rule for rule and edge for edge. This holds on the transcriber's runs here, and
  on every run at Stage C.
  - **[Corrected before signature, 2026-10-31] At Stage C it is held to the
    record.** A paid run's engine is not kept beside its record. So Stage C
    holds each rebuild to the rules and accepted edges the record says the run
    ended with. Stage C refuses to write if one departs.
- **The list's first match.** Level 3's text, applied in order to the 134,400
  points, gives every point the queue `rung3.order_search_ls.space_truth_masks`
  gives it.
- **The labels.** The corpus labels the trigger reads agree with
  `manual.instrument.corpus_truth` on every case.
- **No float decides a check.** Values are compared as fractions, and counts as
  integers.

**RL-g2 — The protocol is §5's.**

- **The texts.** Each text of §5.1 matches its source by digest.
- **The requests.** These are checked through `tests/doubles.py`'s SDK double.
  - Every request carries the reasoning setting, the budget, the pin,
    temperature 0, and `response_format` on its first attempt.
  - The placement call sends the draft as the assistant's turn: its payload,
    serialized, as §5.2's correction says.
  - A failed call is retried with the same messages. A first call's failed
    parse is retried with v1's message, as §6.9's correction says.
- **The hidden policy through v1b's path** gives back the 199 edges and 1.0000 on
  both surfaces (§5.6).
- **The transcriber gives back §0's figures.**
  - Under the impasse trigger: escalations at cases 0 and 1, and 14,820 points
    of the space.
  - Under the error trigger: 23 escalations, 23 rules, 148 declarations
    accepted, and 134,380 points.
- **The validator's verdicts**, each on a case built by hand: a changed rule, an
  unplaced one, a citation of a manual identifier, a copy, and an order answer.

**RL-g3 — The schedule is §2.6's and §9's.**

- The six runs' order is rebuilt from `ORDER_SEED`.
- The smoke run is 30 cases under the error arm.
- The cap is 400 escalations.

**RL-g4 — The signature**, §11.

---

## 8. Stage A — the references (free, gated)

**Deliverable.** `reasoned_loop/sample.py` → `results_reasoned_loop/sample.json`.

- **`RL-g1` to `RL-g3`.**
- **The references, recomputed and owned by this record:**
  - the transcriber under both triggers, with every figure §0 lists;
  - the hidden policy through v1b's path;
  - the `H29` tickets and the rare queues' tickets;
  - the rules `PLAN_REASONED_RULE.md`'s rule arms wrote, by governing rule;
  - `PLAN_MANUAL.md`'s level-3 runs through this plan's instrument.

**It produces nothing adjudicable.** It runs after §0 is signed, so that a figure
§0 did not declare cannot inform a band. If one of §0's declared figures does not
come back, Stage A's findings carry an erratum to §0, dated, and no band moves.

## 9. Stage B — the runs (gated on §0)

**Deliverable.** `reasoned_loop/run.py` → `results_reasoned_loop/loop_smoke.json`,
then the six runs `loop_{i,e}_r{1..3}.json` in §2.6's order. **Each record is
committed before the next run starts.**

**Every run, before any call:**

1. **`--dry-run`** runs `RL-g1` to `RL-g3` and stops. It builds no client and
   needs no key.
2. **The signature (`RL-g4`).** While `PLAN_REASONED_LOOP.md` carries a blank
   signature line, the module exits here.
3. **What comes before it.**
   - **The smoke record**, under this protocol. Every attempt must have been
     served by the pinned provider, reasoned, and ended `stop`. **[Amended
     2026-10-31, §5.5: every attempt that reached the model.]** At least one
     rule must have been born, and at least one placement round must have been
     answered.
   - **Stage A's record.**
   - **Every run before this one** in §2.6's order.

   If the smoke run fails, the runs do not start, and what would change is a
   signed amendment.
4. **The key**, by `reuse.run.key_check`, called rather than copied.
5. **`RL-g1` to `RL-g3`, blocking.**
6. **The destination.** A paid record is never overwritten.
7. **The client, and the calls**, sequential, under hard rule 3.

**The smoke run's pace is reported before the first run**, by call and by round.
It decides nothing, and no row reads its answers.

## 10. Stage C — scoring, and the seven adjudications (free)

**Deliverable.** `reasoned_loop/score.py` → `results_reasoned_loop/score.json`,
and `results_reasoned_loop/FINDINGS_REASONED_LOOP.md`, which owns every figure.

- **`RL-a` to `RL-g`**, each against its line, exactly. Each carries *thin* and
  *unadjudicable* as §0 defines them.
- **Each row's per-run values**, never summed into the verdict.
- **`RL-h` in full.**
- **The runs themselves.** Failed calls, refusals by verdict, answers from
  another provider, retries by cause, reasoning tokens, and the pace by run and
  by round. **[Amended 2026-10-31, §5.5: and the attempts refused for the rate,
  with the pace over the calls that met none.]**

---

## 11. The gate, and where the code lives

**Three modules write this plan's records, and all three refuse while §0 is
unsigned.** `reasoned_loop/sample.py` and `reasoned_loop/score.py` spend nothing.
`reasoned_loop/run.py` refuses before it constructs a client. **The free stages
get the gate because what it protects is the order of events, not money.** A
record of this plan written before the signature would be a figure that existed
before its band.

**The gate reads `PLAN_REASONED_LOOP.md` and no other plan, and it counts every
signature line**, with `reuse/plan.py`'s counting called with this plan's path
and minimum. `MIN_SIGNATURES = 1` today, for §0. An amendment carries its own
line and raises it. No flag skips the gate.

**Constants fixed here, before any figure exists, not to be tuned afterwards, and
pinned by tests:**

- **The client.**
  - `MODEL`, `TEMPERATURE`, `PROVIDER` and `PROVIDER_NAME` are imported from
    `first_match.plan`.
  - `REASONING = first_match.plan.REASONING_ON`, `{"effort": "high"}`.
  - `MAX_TOKENS = first_match.plan.MAX_TOKENS_REASONING`, 16,000.
  - `MAX_RETRIES = 2` and `CALL_RETRY_WAIT = (10, 30)`, `first_match.plan`'s.
  - **[Amended 2026-10-31, §5.5]** `RATE_LIMITED = "RateLimitError"` and
    `RATE_LIMIT_WAIT = (60, 120, 240, 480, 960)`.
- **The protocol.**
  - `PROTOCOL = "v1b"` and `LEVEL = 3`.
  - The texts are imported from `manual.prompts`, `rung2.proposers2` and
    `blind.protocol`, and their digests are pinned.
  - **[Added before signature, 2026-10-31]** `SYSTEM_PROMPT_SHA16 =
    "7b883f03a863d647"`, §5.1's digest, and `DECLARED`, the figures §0 lists as
    computed while drafting, as `blind/plan.py`'s `DECLARED` holds that plan's.
- **The arms.**
  - `ARMS = ("i", "e")`.
  - `TRIGGERS = {"i": ("IMPASSE", "CONFLICT"), "e": ("IMPASSE", "CONFLICT",
    "ERROR")}`.
- **The runs.**
  - `REPS = 3`, `N = 2000` and `SEED = 17`.
  - `SMOKE_N = 30` and `SMOKE_ARM = "e"`.
  - `MAX_ESCALATIONS = 400` and `MAX_CONSECUTIVE_FAILURES = 5`.
- **The seed.** `ORDER_SEED = 83`.
  - **It is new.** It is distinct from every seed a closed thread uses: 17 to 20,
    25, 41, 43, 47, 53, 59, 61, 67, 71, 73 and 79, and values from 1000 up.
  - **It draws one thing:** which arm runs first.
  - **It is hash-free.** It is a string seed, through SHA-512.
  - **The placement listing is not this seed's.** It keeps v2b's
    `LISTING_SEED`, through `blind.protocol.listing`.
- **The limits.**
  - `MIN_SIGNATURES = 1`. **[Amended 2026-10-31, §5.5: `MIN_SIGNATURES = 2`.]**
  - `MIN_ESCALATIONS = 60` and `MIN_UNITS = 20`.
  - `COVER_BEFORE = 200`.
- **The lines of §0.** They are fractions, and every comparison with them is
  exact.
  - `RL_A_LINE = Fraction(9, 10)`.
  - `RL_B_LINE = Fraction(2, 3)`.
  - `RL_C_LINE = Fraction(1, 10)`.
  - `RL_D_LINE = Fraction(9, 10)`.
  - `RL_E_LINE = Fraction(9, 10)`.
  - `RL_F_LINE = 0`.
  - `RL_G_LINE = Fraction(9, 10)`.

**The names.**

- **The package is `reasoned_loop/`.** No module of the standard library has that
  name.
- **The rows are `RL-a` to `RL-h`, with two letters.** Every single capital
  already names a thread, and `tests/test_prose_tables.py` reads one or two.
- **The protocol is v1b.** No closed thread uses the name.

Drafter's proposal for the layout; the naming is Sergi's to overrule:

```
reasoned_loop/__init__.py
reasoned_loop/plan.py        the gate and the constants of §11
reasoned_loop/protocol.py    v1b's texts, the messages, the proposer over first_match's asker   [proposer's path]
reasoned_loop/loop.py        the loop with both triggers, the draft and the placement            [proposer's path]
reasoned_loop/references.py  the transcriber and the hidden policy through v1b's path
reasoned_loop/gates.py       RL-g1 to RL-g4
reasoned_loop/sample.py      Stage A
reasoned_loop/run.py         Stage B: it spends                                               [proposer's path]
reasoned_loop/score.py       Stage C
results_reasoned_loop/FINDINGS_REASONED_LOOP.md
results_reasoned_loop/sample.json  loop_smoke.json  loop_{i,e}_r{1..3}.json  score.json
tests/test_reasoned_loop.py
```

**The plumbing goes in the same commit as the modules:**

- **`CODE_ROOTS`.** `reasoned_loop` joins it in `harness/provenance.py`, and
  joins the oracle scan's roots in `tests/test_oracle_separation.py`.
- **`ONLINE_LOOP` and the authority channel.** The three modules marked above
  join both, with rule B's comment. Every call sends the manual's text.
- **The partial files**, `results_reasoned_loop/*.partial.jsonl`, join
  `.gitignore`.
- **The guarded writers** in `tests/test_writer_lists.py` grow by one.
- **The call site.** The proposer asks through `first_match/ask.py`'s asker, as
  `reasoned_rule/ask.py` does. That asker is already a classified call site and
  carries the call recorder, so `tests/test_call_record.py`'s list does not
  grow. Every escalation still keeps its `call_attempts`.
- **The README's table of writers** gains its rows, and so does its table of
  tests.

**The list of modules allowed to see the oracle does not grow.** Tests touch no
network.

---

## 12. Definition of done

- [ ] Records under `results_reasoned_loop/` with `_env`. Each carries the
      model, the temperature, the reasoning setting, the budget, the pin, the
      arm, the run, the texts' digests and `call_attempts`. All were produced
      with `PYTHONHASHSEED=0`.
- [ ] `RL-g1` to `RL-g4` passed before any record was written. The key check and
      the smoke run came before the first run, and each run's record was
      committed before the next began.
- [ ] Before the first run: every attempt of the smoke run was served by the
      pinned provider, reasoned, and ended `stop`. **[Amended 2026-10-31, §5.5:
      every attempt that reached the model.]** A rule was born, and a
      placement round was answered.
- [ ] The plumbing of §11, and tests pinning:
      - the constants and the gate;
      - the texts against their sources' digests;
      - the requests, the pin and the reasoning setting included;
      - the retry by cause;
      - both triggers, the validator's verdicts and the resume, on runs built by
        hand;
      - the transcriber's and the hidden policy's figures;
      - the exactness of §0's comparisons, *thin*, and each row's conditions for
        having no value.

      **[Corrected before signature, 2026-10-31]** The transcriber's figures are
      `RL-g2`'s and Stage A's, never a test's, because no test runs the loop over
      the corpus. A test that pinned them would give them a second home. The
      tests pin the hidden policy through v1b's path, born whole and deciding
      both surfaces right, which is the instrument on a policy whose answer is
      known.

      The whole suite is green on 3.10 and 3.12.
- [ ] Every figure in prose names its surface, its arm, its denominator and its
      runs.
- [ ] `results_reasoned_loop/FINDINGS_REASONED_LOOP.md` owns every figure, with
      a dated erratum wherever it corrects something already published. That
      includes this plan's §0 *already seen*, if Stage A does not reproduce it,
      and §1's estimates of the pace and the calls.
- [ ] `STATUS.md`: the scoreboard gains the `RL` thread. *What is open* narrows
      its second and third items by what this plan settles.
- [ ] `IDEAS.md`: *The loop with reasoning on* is narrowed, with what this plan
      opens.
- [ ] `tests/test_prose_tables.py`'s `THREADS` gains `RL`, and its `TABLES`
      gains `FINDINGS_REASONED_LOOP.md`'s verdict table.
- [ ] This plan is indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, records and this plan are in separate commits. The plan and its
      signature are each alone in their commits.

---

## 13. What this plan cannot settle, declared before it runs

1. **Reasoning in the loop, apart from v1b.** No reasoning-off arm runs under
   v1b. The impasse arm is set beside `PLAN_MANUAL.md`'s level-3 runs across
   dates and protocols, and that comparison is reported, never adjudicated.
2. **A trigger that reads no truth.** The error arm reads the label of every
   arrival. A deployment would report only some errors, late or noisily: rung
   4's coverage, delay and noise. Random escalation, which reads none, is not
   run.
3. **The screen with reasoning.** Every first call is blind (§2.1).
4. **Telling the proposer the base erred.** The error arm's prompts do not say
   so (§6.1).
5. **The other levels.** Only level 3, whose text is the policy, is given.
6. **The arrivals' order.** One corpus, seed 17, in which the list's default
   arrives second.
7. **One model, one provider, one manual, three runs an arm.**
