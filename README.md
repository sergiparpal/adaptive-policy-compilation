# Adaptive policy compilation

A cheap symbolic engine resolves the cases it covers; when it fails to cover one
(an *impasse*), an LLM acts and writes a new rule so that next time it does cover
it. Domain: support-ticket triage — 8 attributes, 8 queues, and a hidden policy
of 29 rules spread over 8 priority layers.

> **Arriving cold? Start at [`STATUS.md`](STATUS.md).** It is the snapshot of
> what is known today — what is established and on which surface it was
> measured, what was withdrawn and why, and what is open — with a pointer to the
> record behind each figure. This file, from *Rung 1* onwards, is the
> specification and the operating procedure.

> **Note on language.** The prose of this repository is in English; the code is
> not. Module, package and field names stay as they are (`rung2/` = rung 2),
> and the scripts still print their tables in Spanish. When a block below shows
> expected output, compare the **numbers**, not the words.

## Four closed rungs, two closed threads, and where their figures live

**A figure has exactly two homes: the FINDINGS record that owns it, and
[`STATUS.md`](STATUS.md), which indexes it and names the surface it was measured
on.** None appears in this file. A number copied into a README has no erratum
attached and no test behind it, so when the record that owns it is corrected the
copy goes stale in silence — which is how the four rungs' headline figures ended
up in four places at once.

| rung | what it took on | record |
|---|---|---|
| **1** · engine ceiling | whether priority can be inferred from the shape of the rules | [`results/FINDINGS.md`](results/FINDINGS.md) |
| **2** · declared priority | whether the proposer will declare it, given a mechanism that executes it | [`results2/FINDINGS2.md`](results2/FINDINGS2.md) |
| **3** · priority by search | whether rung 1's material contained an order worth having | [`results3/FINDINGS3.md`](results3/FINDINGS3.md) |
| **4** · priority from feedback | whether that order is learnable from what a deployed system observes | [`results4/FINDINGS4.md`](results4/FINDINGS4.md) |
| **audit** · the optimizer | whether the search that produced rungs 3 and 4 was strong enough to believe | [`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md) |
| **control** · the default rule | how much of rung 1's conflict rate is the DSL's one-condition minimum rather than the thesis it is cited for | [`results/FINDINGS_DEFAULT_RULE.md`](results/FINDINGS_DEFAULT_RULE.md) |
| **A** · the sensitivity sweep | how much of rung 1's failure is this policy's shape, over a family of 1,300 synthetic manuals | [`results_sensitivity/FINDINGS_SENSITIVITY.md`](results_sensitivity/FINDINGS_SENSITIVITY.md) |
| **I** · ILP as a competitor | what the LLM proposer buys that a symbolic inducer would not, on the same 632 tickets — though only the inducer was handed their queues | [`results_ilp/FINDINGS_ILP.md`](results_ilp/FINDINGS_ILP.md) |
| **P** · pairwise judgement | whether changing the question — *which of these two rules wins?* — gets the proposer to supply the priority it would not write | [`results2/FINDINGS2.md`](results2/FINDINGS2.md) Stages C–D, [`results3/FINDINGS3.md`](results3/FINDINGS3.md) §§6–10 |
| **B** · the proposer at 1,600 | whether it was the budget — asked at the budget where a perfect chooser, a 70% chooser and a coin stop being the same number | [`results3/FINDINGS3.md`](results3/FINDINGS3.md) §§11–15 |
| **U** · the founding question | whether the rules an LLM writes get reused or memorize cases, asked on rung 2's engine, which can execute the policy — closed 2026-09-30 | [`results_reuse/FINDINGS_REUSE.md`](results_reuse/FINDINGS_REUSE.md) |
| **F** · fidelity | whether a compiled rule decides a later case the way the model would have, asked afresh on the same case — closed 2026-10-04 | [`results_fidelity/FINDINGS_FIDELITY.md`](results_fidelity/FINDINGS_FIDELITY.md) |
| **W** · declared edges | what the edges the proposer declared at write time bought, once a growing base gave them material: on the cases they decided, against a coin, and over the function — closed 2026-10-05 | [`results_edges/FINDINGS_EDGES.md`](results_edges/FINDINGS_EDGES.md) |
| **L** · the slot listed first | where the presentation slot decides the pairwise answers already paid for, and whether it does anything else to them — closed 2026-10-05 | [`results_primacy/FINDINGS_PRIMACY.md`](results_primacy/FINDINGS_PRIMACY.md) |
| **Y** · the why texts | what the proposer says it is doing beside each pairwise answer, against what it does, with a codebook frozen on a development set — closed 2026-10-05 | [`results_why/FINDINGS_WHY.md`](results_why/FINDINGS_WHY.md) |
| **E** · declaration imposed | whether a proposer made to declare, against every rule a new one overlaps, whether it is an exception to it or a default under it, writes a stratified base — Stage E, the second way's third form — closed 2026-10-06 | [`results_authorship/FINDINGS_AUTHORSHIP.md`](results_authorship/FINDINGS_AUTHORSHIP.md) |
| **O** · imposed, with overlap asked for | Stage E's question asked again, with the proposer told that overlap is normal and asked to declare only where the queues differ: does it keep overlapping, and do its declarations order what subsumption leaves — closed 2026-10-07 | [`results_overlap/FINDINGS_OVERLAP.md`](results_overlap/FINDINGS_OVERLAP.md) |
| **K** · beyond the keyword, drafted blind | whether declaration carries direction beyond the security keyword, with the base taken out of the proposer's first call and a placement round forcing the declaration — closed 2026-10-12 | [`results_blind/FINDINGS_BLIND.md`](results_blind/FINDINGS_BLIND.md) |
| **V** · the screen | what the screen of compiled rules does to the model: asked with the ticket alone on decisions its rules made, is it right more often, and does it defer to the screen — closed 2026-10-15 | [`results_screen/FINDINGS_SCREEN.md`](results_screen/FINDINGS_SCREEN.md) |
| **H** · the bound | how much of the residue under rung 3's coverage bound is slack: a certificate, found without a solver and checked from the masks alone, of cases every order loses — closed 2026-10-17 | [`results_bound/FINDINGS_BOUND.md`](results_bound/FINDINGS_BOUND.md) |
| **M** · the ranking, asked of the model | what the model states when asked for the one order between the eight queues that decides a contested ticket, scored as a lookup over rung 1's rules against the ranking that read the key — closed 2026-10-17 | [`results_ranking/FINDINGS_RANKING.md`](results_ranking/FINDINGS_RANKING.md) |
| **T** · the students | what the proposer's rules buy over a learner fitted to its answers: a pruned tree, a logistic regression and the cache's retrieval, trained on the queues it named at the escalations and set beside the rules written from them — closed 2026-10-18 | [`results_students/FINDINGS_STUDENTS.md`](results_students/FINDINGS_STUDENTS.md) |
| **J** · the escalations | what a reviewer's labels at the escalations buy the order: rung 3's search handed the truth of rung 1's train-half escalations at the audit's label budgets, set beside that record's own random draws, with three rules for which to label first — closed 2026-10-19 | [`results_escalations/FINDINGS_ESCALATIONS.md`](results_escalations/FINDINGS_ESCALATIONS.md) |
| **N** · the audit of decisions | what a random audit of the system's decisions buys beside the escalations: rung 3's search handed the truth of every train-half escalation and of a random draw of the cases rung 1's engine decided itself, in nested draws, read between the escalations alone and the whole train half — closed 2026-10-19 | [`results_spotcheck/FINDINGS_SPOTCHECK.md`](results_spotcheck/FINDINGS_SPOTCHECK.md) |
| **Z** · the rules no label reaches | what the rules no labelled case matches hold in rung 3's labelled orders: each moved alone to the front with the truth reading the result, and all moved below the rest without it, beside random placements of them, in the escalations' order and along the label curve — closed 2026-10-20 | [`results_unreached/FINDINGS_UNREACHED.md`](results_unreached/FINDINGS_UNREACHED.md) |
| **G** · the policy, given to the proposer | the authority channel: the policy handed to the model as a catalogue of the queues, a prose manual and the 29 rules as text, compiled once in one answer and inside `PLAN_REUSE.md`'s loop, to separate what the model knows from what the loop elicits — closed 2026-10-21 | [`results_manual/FINDINGS_MANUAL.md`](results_manual/FINDINGS_MANUAL.md) |
| **X** · the rules applied ticket by ticket | `PLAN_MANUAL.md`'s escalations asked again on one day, with their screen and with the ticket alone under the same manual, and the ticket alone under the names, to separate what the screen costs from what is lost applying the rules — closed 2026-10-24 | [`results_apply/FINDINGS_APPLY.md`](results_apply/FINDINGS_APPLY.md) |
| **QA** · the queue asked alone | `PLAN_APPLY.md`'s ticket prompts asked again on one day, pinned to one provider, in three arms: the rule-writing prompt, the same impasse framing asking for the queue alone, and a plain question for the queue, to separate the rule-writing task from the application — closed 2026-10-24 | [`results_queue_alone/FINDINGS_QUEUE_ALONE.md`](results_queue_alone/FINDINGS_QUEUE_ALONE.md) |
| **FM** · the first match | `PLAN_QUEUE_ALONE.md`'s level-3 plain prompts asked again on one day, pinned to one provider, in three arms: the plain question, the same question asking for the rule that applies before its queue, and the plain question with reasoning on, to separate finding the first match from naming its queue, and both from thinking it through — closed 2026-10-25 | [`results_first_match/FINDINGS_FIRST_MATCH.md`](results_first_match/FINDINGS_FIRST_MATCH.md) |
| **RR** · the rule written with reasoning on | `PLAN_QUEUE_ALONE.md`'s level-3 rule and plain prompts asked again on one day, pinned to one provider, in four arms: the rule-writing prompt and the plain question, each with reasoning off and on, to see whether reasoning carries into the queue a rule-writer chooses before any loop runs, and to read the rules it writes — closed 2026-10-25 | [`results_reasoned_rule/FINDINGS_REASONED_RULE.md`](results_reasoned_rule/FINDINGS_REASONED_RULE.md) |
| **RL** · the loop with reasoning on | `PLAN_REUSE.md`'s loop run with level 3's manual and reasoning on, pinned to one provider, a blind first call and a placement round against the base, three runs an arm: under the standing trigger, and asked also where the base decides wrongly, to see whether what limits a reasoning loop is its trigger or the order its rules get — closed 2026-11-03 | [`results_reasoned_loop/FINDINGS_REASONED_LOOP.md`](results_reasoned_loop/FINDINGS_REASONED_LOOP.md) |
| **CH** · half the errors reported | `PLAN_REASONED_LOOP.md`'s loop run again with level 3's manual and reasoning on, pinned to one provider, under rung 4's feedback channel at coverage 1/2 beside the error arm again, three runs an arm alternating in one period, to see what a loop compiles from a trigger a deployment could have — closed 2026-11-07 | [`results_channel/FINDINGS_CHANNEL.md`](results_channel/FINDINGS_CHANNEL.md) |
| **PL** · the placement round | `PLAN_CHANNEL.md`'s channel arm run again with level 3's manual and reasoning on, pinned to another provider, three runs under v1b's placement round and three under one that lists only what the engine can still order, alternating, each pair under one set of draws, beside a same-day bridge of first calls asked of both providers, to see whether v1b's refusals were the protocol's and what the loop compiles without them — closed 2026-11-08 | [`results_placement/FINDINGS_PLACEMENT.md`](results_placement/FINDINGS_PLACEMENT.md) |
| **WR** · the region asked for whole | `PLAN_PLACEMENT.md`'s v1c arm run again with level 3's manual and reasoning on, pinned to DeepInfra, beside v1d, whose first call asks for the governing rule's region whole, three runs an arm alternating, each pair under one set of draws, to see whether the loop's narrow rules were the first call's text and what whole first drafts compile — closed 2026-11-10 | [`results_whole/FINDINGS_WHOLE.md`](results_whole/FINDINGS_WHOLE.md) |
| **HV** · the paragraph's halves | the loop's first call asked alone at 136 tickets the reasoning loops escalated, with level 3's manual and reasoning on, pinned to DeepInfra, under four paragraphs where the base would be — the empty base, v2b's paragraph, its first half alone and its overlap clause on the empty base — in two passes and a session of the rarest queue's tickets, to see which half of v2b's paragraph makes the first call cut — closed 2026-11-12 | [`results_halves/FINDINGS_HALVES.md`](results_halves/FINDINGS_HALVES.md) |
| **CR** · the learning regime | `PLAN_PLACEMENT.md`'s v1c at level 1, the catalogue, with reasoning on, pinned to DeepInfra, under the channel at coverage 1/2, with and without a report that carries the reported ticket's true queue, beside the same labels compiled at once and handed to the inducer and the students, to see whether the loop learns what its prompt does not hold — closed 2026-11-14 | [`results_corrections/FINDINGS_CORRECTIONS.md`](results_corrections/FINDINGS_CORRECTIONS.md) |

**The two `P`/`B` rows have a write-up.**
[`PAIRWISE_WRITEUP.md`](PAIRWISE_WRITEUP.md) presents both threads as one result
instead of fifteen sections: the proposer answers the pairwise question well and
the answer contains almost no priority, with the free baseline that makes the
second half readable, the mechanism that joins the two, and the four things that
could have been blamed and were each ruled out by a free measurement. **It owns no
figure** — every number in it names the record that owns it, its surface and its
pool.

Each FINDINGS carries its **dated errata in place**: rungs 3 and 4 were
re-measured on August 8, 2026 and their headline figures moved, and on August 24,
2026 `FINDINGS3.md` §8 withdrew a conclusion of its own that §9 then measured
directly. In both cases the original text is kept beside the correction rather
than replaced. **Read the erratum before citing any number.**
[`IDEAS.md`](IDEAS.md) keeps what remains open, including the known technical
debt.

> **From "Rung 1" onwards, this file describes the specification and the
> operating procedure of that rung.** They remain valid as procedure, not as
> project status.

### Three documents that read the records instead of adding to them

Three more files sit at the root, and until recently nothing indexed them:
[`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md), the report on *which rule wins
when several match and disagree*, written against the records as they stood on
2026-08-16; [`CHAT_SUMMARY.md`](CHAT_SUMMARY.md), the summary of the
conversation of August 11, 2026, reviewed once against the records it cites —
on August 12, which its own header says is still the last review — and corrected
in four places since; and [`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md), a reading
of the project written from outside it on 2026-08-29 by a model that had only the
public tree, adjudicated line by line against the code and the records, with the
plan that came out of the contrast. **None owns a figure and none is a record.**
They cite, with the record that owns each number named; where one disagrees with
a record, the record wins; and all three carry their own dated errata in place,
exactly as the FINDINGS do.

**A fourth root document is not one of these three.**
[`PAIRWISE_WRITEUP.md`](PAIRWISE_WRITEUP.md) also owns no figure and also cites
with the owner named, but it is not a reading of the records against each other —
it is the **write-up** of one thread's result, and it is indexed above with the
rungs it belongs to. It is the deliverable; these three are the criticism.

**They are worth the detour before writing a new analysis**, which is what §9.8
of the first is about: it re-derived three corrections the second had already
made, by another route and without knowing them. **The third document is that
warning coming true a second time**: its §1.4 records that the review's headline
recommendation restates a limit §9.1 of the first already had written down, this
time from a reader who had seen neither. Three independent readings converging is
evidence for the conclusions — and a warning that this repository already
contains analysis a new document may be repeating. §4, rule C of
[`PLAN_PAIRWISE.md`](PLAN_PAIRWISE.md) turns that into a step rather than a
suggestion.

---

## Reproducing the four rungs

**All of this costs zero API calls and runs on the standard library**, no venv.
These are the measurements that underpin the four records; next to each command,
what it should print.

```bash
# --- RUNG 1 · the engine ceiling and the frontier ------------------------
python3 -m harness.ceiling_check      # specificity engine vs. design order
python3 run_experiment.py frontier    # the keep_k mocks and the cache baseline
python3 -m harness.default_rule_control  # the same ceiling with the catch-all at
                                      # its true rank, beside the published row

# --- RUNG 2 · hybrid engine: subsumption + declared priority -------------
python3 -m rung2.ceiling_check2    # STOP 0 of rung 2; must PASS
python3 -m rung2.ceiling_check2_space  # the same ceiling over the 134,400
                                   # combinations, and what the 199 edges buy
python3 -m rung2.compare_runs results2/llm_run2_*.json   # the 8 runs
python3 -m rung2.note_audit  results2/llm_run2_*.json    # attributes and notes

# --- RUNG 3 · order by search over the corpus ----------------------------
python3 -m rung3.order_search      # coverage bound, greedy order, splits
python3 -m rung3.budget_and_balance  # label curve and balanced greedy

# --- RUNG 4 · order learned from a feedback channel ----------------------
python3 -m rung4.sweep             # coverage/asymmetry/delay/noise sweeps

# --- A · the sensitivity family, a control on rung 1 ----------------------
python3 -m sensitivity.generator_check   # A-g1..A-g4, blocking, first and alone
python3 -m sensitivity.sweep             # 13 ρ bins × 100 draws; gated on §0
python3 -m sensitivity.sweep --dry-run   # draws everything, writes nothing

# --- I · ILP as a competitor, on the tickets the proposer saw -------------
python3 -m ilp.induce_check              # I-g1..I-g4, blocking, first and alone
python3 -m ilp.compare                   # the four rows; gated on §0 and §1
python3 -m ilp.labels                    # POST-HOC · who had the labels, §5's erratum
python3 -m ilp.margin                    # POST-RUN · where the inducer's margin comes from, ~35 s
python3 -m ilp.chosen                    # POST-RUN · the inducer on the queues the proposer chose

# --- AUDIT of the optimizer that produced rungs 3 and 4 ------------------
python3 -m rung3.optimizer_check   # optimizer ceiling: must give 1.0000
python3 -m rung3.optimizer_check_wt  # idem for the class-weighted objective
python3 -m rung3.order_search_ls   # rung 3 redone with the audited optimizer (33 min)
python3 -m rung4.sweep_ls          # rung 4 redone with the audited optimizer (42 min)
python3 -m rung3.budget_and_balance_ls  # label curve and balanced objective (28 min)

# --- THE ORDERS BEHIND THOSE FIGURES, compared as orders ------------------
python3 -m rung3.order_metrics_run # regenerates and measures orders (12 min)
python3 -m rung3.order_metrics_run --checks   # parity gate only (6 min)
python3 -m rung3.order_metrics_corpus  # the same orders over the corpus (7 min)
python3 -m rung3.order_metrics_corpus --s-e-argmin  # amends its own record in place
python3 -m rung3.rank_transfer     # joins the two records above (seconds)
python3 -m rung3.order_metrics_touched  # the space, restricted to the points
                                      # the corpus touches (7 min)
python3 -m rung3.order_metrics_touched --checks   # its four gates only

# --- P · pairwise judgement (the free half) -------------------------------
python3 -m rung3.floor_by_pool     # what a no-search order scores, both pools
python3 -m rung2.pair_benchmark    # the 199 labelled pairs and their witnesses
python3 -m rung2.pair_benchmark --checks       # its three gates only
python3 -m rung3.queue_hierarchy_floor  # what a queue ranking scores (4 min)
python3 -m rung2.pair_judgement_baselines  # what the stage C rate is made of
python3 -m rung3.declared_order    # the three scorings + the control (6 min)
python3 -m rung3.edge_direction    # is the direction right, and would right help
python3 -m rung3.edge_budget       # does the channel pay with more edges (3 min)

# --- B · the proposer at 1,600 (the free half) ----------------------------
python3 -m rung2.pair_sample_1600  # the nested 1,600-pair sample and its gates
python3 -m rung3.edge_sides        # what each side of the split BUYS
python3 -m rung3.mfas_compilation  # is it the answers or the compilation
python3 -m rung3.edge_dropping     # does deliberate dropping beat chance
python3 -m rung3.answer_asymmetry  # why it names rule_b more often
python3 -m rung3.filter_headroom   # how much any selection could have shown
python3 -m rung3.filter_space      # the same cuts, scored on the space
python3 -m rung3.identical_rules   # rules written twice, with two queues
python3 -m rung3.copy_births       # why rung 1 wrote them again
```

The two scorings of that thread take the records it produced, so they carry
their source and destination explicitly:

```bash
python3 -m rung3.edge_direction --source results2/pair_judgement_1600.json \
    --out results3/edge_direction_1600.json --split results2/pair_sample_1600.json
python3 -m rung3.declared_order --source results2/pair_judgement_1600.json \
    --out results3/declared_order_1600.json --split results2/pair_sample_1600.json \
    --accuracy results3/edge_direction_1600.json
```

**The three commands of those threads that cost money are not in the blocks
above**, and none of them runs while §0 of **the plan that governs the run** is
unsigned — a gate refuses before the client is even constructed. **Which plan is
an argument, because there is more than one**: until 2026-08-25 the gate read
`PLAN_PAIRWISE.md` whatever it was gating, so a 1,600-pair run would have found
that closed thread's signature, reported `ok`, and spent 1,200 calls on rows
nobody had signed. `--dry-run` builds every question, checks every gate and spends
nothing:

```bash
python3 -m rung2.pair_judgement --hidden  --dry-run   # 170 calls if run
python3 -m rung2.pair_judgement --learned --dry-run   # 400 calls if run
python3 -m rung2.pair_judgement --learned --budget 1600 \
    --sample results2/pair_sample_1600.json --reuse --dry-run  # 1200 if run
```

The first two are gated on [`PLAN_PAIRWISE.md`](PLAN_PAIRWISE.md), the third on
[`PLAN_PROPOSER_1600.md`](PLAN_PROPOSER_1600.md). The third also refuses without
`--reuse` or `--reask-all`: §2 of its plan makes that a decision about money, and
the module will not take a default for it.

**[`PLAN_REUSE.md`](PLAN_REUSE.md) closed on 2026-09-30**, the founding question on
rung 2's engine. Sergi signed §0 on 2026-09-29 and an amendment to §1 the next day
— the proposer's calls do not reason — each before any figure it governs existed.
Its record is [`results_reuse/FINDINGS_REUSE.md`](results_reuse/FINDINGS_REUSE.md).
Its gate reads that plan and no other, requires both signatures, and guards all
five of its writers, the free ones too.

Stages A and C are free, and they reproduce from the committed records. **Stage B
spent**: its records are guarded, and a re-run neither overwrites them nor gives
the same draws back. A paid run does not start without Sergi asking for it.

```bash
python3 -m reuse.run --dry-run            # U-g1..U-g4, blocking; writes nothing
python3 -m reuse.readout                  # Stage A · the eight n=100 records
python3 -m reuse.score                    # Stage C · the five rows, from the runs
python3 -m reuse.structure                # POST-RUN · the bases, read for Stage E
.venv/bin/python -m reuse.run --smoke     # Stage B · spends · only on Sergi's say
.venv/bin/python -m reuse.run --rep 1     # then --rep 2 and --rep 3, never in parallel
```

**[`PLAN_FIDELITY.md`](PLAN_FIDELITY.md) closed on 2026-10-04**: the founding
question in its cleanest form. Sergi signed §0 on 2026-10-02, before any of its
figures existed. On a case a compiled rule decided, would the model, asked
afresh, have chosen the same queue, and been right more often than the rule? It
re-asked the model on prompts rebuilt from `PLAN_REUSE.md`'s Stage B records, so
nothing was re-run. Its record is
[`results_fidelity/FINDINGS_FIDELITY.md`](results_fidelity/FINDINGS_FIDELITY.md).
Its gate reads that plan and no other, counts every signature line, and guards
all three of its writers, the free ones too.

Stages A and C are free, and they reproduce from the committed records. **Stage B
spent**: its records are guarded, and a re-run neither overwrites them nor gives
the same answers back. A paid session does not start without Sergi asking for
it, and one that is interrupted resumes where it stopped.

```bash
python3 -m fidelity.ask --dry-run                  # F-g1..F-g4, blocking; writes nothing
python3 -m fidelity.sample                         # Stage A · the draw and the free readout
python3 -m fidelity.score                          # Stage C · the five rows, from the sessions
.venv/bin/python -m fidelity.ask --session smoke   # Stage B · spends · only on Sergi's say
.venv/bin/python -m fidelity.ask --session births  # then base1, base2, base3, ticket_only
```

Their destinations are guarded by `harness/record_guard.py`: those records cost
money and a re-run does not give the same thing back.

**[`PLAN_EDGES.md`](PLAN_EDGES.md) closed on 2026-10-05**: what the edges the
proposer declared at write time bought, once `PLAN_REUSE.md`'s growing base gave
them material. Sergi signed §0 on 2026-10-05, before any of its figures existed.
It rebuilt each Stage B run from its record and scored the edges three ways: on
the cases they decided, against a coin over their directions, and over the
function. Its record is
[`results_edges/FINDINGS_EDGES.md`](results_edges/FINDINGS_EDGES.md). Its gate
reads that plan and no other, and guards both of its writers.

**It spends nothing.** It reproduces from the committed records in about two
minutes, most of it the suite inside its first check.

```bash
python3 -m edges.score --dry-run   # W-g1..W-g4, blocking; writes nothing
python3 -m edges.score             # the census, W-a to W-c, and W-d
python3 -m edges.readings          # POST-RUN · the readings the verdicts needed
```

**[`PLAN_PRIMACY.md`](PLAN_PRIMACY.md) closed on 2026-10-05**: where the
presentation slot decides the pairwise answers `PLAN_PROPOSER_1600.md` paid for,
and whether it does anything else to them. Sergi signed §0 on 2026-10-05, before
any of its figures existed. It reads the 1,600 answers with the truth per pair
and checks first that every slot was the seeded deal, the premise of every floor
it reports. Its record is
[`results_primacy/FINDINGS_PRIMACY.md`](results_primacy/FINDINGS_PRIMACY.md). Its
gate reads that plan and no other, and guards its one writer.

**It spends nothing.** It reproduces from the committed records in about a
minute, nearly all of it the suite inside its first check.

```bash
python3 -m primacy.score --dry-run   # L-g1..L-g4, blocking; writes nothing
python3 -m primacy.score             # L-a, L-b, and the readings of L-c
```

**[`PLAN_WHY.md`](PLAN_WHY.md) closed on 2026-10-05**: what the proposer says it
is doing in the sentence it wrote beside each pairwise answer, against what it
does. Sergi signed §0 on 2026-10-05, before any held-out sentence was coded. Its
codebook was frozen on a development set, Stage D's and Stage C's sentences, and
its rows read the batch answered the next day. Its record is
[`results_why/FINDINGS_WHY.md`](results_why/FINDINGS_WHY.md). Its gate reads that
plan and no other, and guards its one writer.

**It spends nothing.** It reproduces from the committed records in about a
minute, nearly all of it the suite inside its first check.

```bash
python3 -m why.score --dry-run   # Y-g1..Y-g4, blocking; writes nothing
python3 -m why.score             # Y-a to Y-d, and the readings of Y-e
```

**[`PLAN_AUTHORSHIP.md`](PLAN_AUTHORSHIP.md) closed on 2026-10-06**: Stage E,
declaration imposed at write time, on `PLAN_REUSE.md`'s loop. Sergi signed §0 on
2026-10-05, before any of its figures existed. Under its protocol, v1e, a rule
that overlaps another is refused until the proposer declares it an exception to
it or a default under it, nested rules included. Its record is
[`results_authorship/FINDINGS_AUTHORSHIP.md`](results_authorship/FINDINGS_AUTHORSHIP.md).
Its gate reads that plan and no other, and guards both of its writers. Its
Stage A writes nothing: the baseline is `reuse/structure.py`'s reading of
`PLAN_REUSE.md`'s bases, in that plan's block above, with `PLAN_EDGES.md`'s
table, and `E-g2` reproduces both.

Stage C is free, and it reproduces from the committed records. **Stage B
spent**: its records are guarded, and a re-run neither overwrites them nor gives
the same rules back. A paid run does not start without Sergi asking for it, and
one that is interrupted resumes where it stopped.

```bash
python3 -m authorship.run --dry-run            # E-g1..E-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m authorship.score   # Stage C · E-a to E-d, and E-e
PYTHONHASHSEED=0 python3 -m authorship.refused # POST-RUN · the refused declarations
.venv/bin/python -m authorship.run --smoke     # Stage B · spends · only on Sergi's say
.venv/bin/python -m authorship.run --rep 1     # then --rep 2 and --rep 3, never in parallel
```

**[`PLAN_OVERLAP.md`](PLAN_OVERLAP.md) closed on 2026-10-07**: Stage E's question
asked again, with the proposer kept overlapping if it would be. Sergi signed §0
on 2026-10-06, before any of its figures existed. Under its protocol, v2e, the
proposer is told that overlap is normal, as rung 2's v2 tells it, and is
required to declare only against the rules of another queue it overlaps. Its
record is
[`results_overlap/FINDINGS_OVERLAP.md`](results_overlap/FINDINGS_OVERLAP.md). Its
gate reads that plan and no other, and guards both of its writers. Its Stage A
writes nothing: the baselines are `PLAN_REUSE.md`'s and `PLAN_AUTHORSHIP.md`'s
records, read by the instrument Stage C uses, and `O-g2` reproduces every figure
§0 takes from them.

Stage C is free, and it reproduces from the committed records. **Stage B
spent**: its records are guarded, and a re-run neither overwrites them nor gives
the same rules back. A paid run does not start without Sergi asking for it, and
one that is interrupted resumes where it stopped.

```bash
python3 -m overlap.run --dry-run              # O-g1..O-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m overlap.score     # Stage C · O-a to O-c, and O-d
PYTHONHASHSEED=0 python3 -m overlap.readings  # POST-RUN · the run that overlapped
PYTHONHASHSEED=0 python3 -m overlap.readings_v1  # POST-RUN · the same, over v1
.venv/bin/python -m overlap.run --smoke       # Stage B · spends · only on Sergi's say
.venv/bin/python -m overlap.run --rep 1       # then --rep 2 and --rep 3, never in parallel
```

**[`PLAN_BLIND.md`](PLAN_BLIND.md) closed on 2026-10-12**: whether declaration
carries direction beyond the security keyword, the one attribute behind nearly
every edge declared before it. Sergi signed §0 on 2026-10-11, before any of its
figures existed. Under its protocol, v2b, the proposer drafts its rule on an
impasse with no rule shown, and a placement round then asks for the same rule,
placed against every rule of another queue it overlaps. Every row is read where
the keyword is absent. Its record is
[`results_blind/FINDINGS_BLIND.md`](results_blind/FINDINGS_BLIND.md). Its gate
reads that plan and no other, and guards its three writers. Its Stage A writes
nothing: the baselines are the three earlier protocols' records, read by the
instrument Stage C uses, and `K-g2` reproduces every figure §0 takes from them.

Stage C is free, and it reproduces from the committed records. **Stage B
spent**: its records are guarded, and a re-run neither overwrites them nor gives
the same rules back. A paid run does not start without Sergi asking for it, and
one that is interrupted resumes where it stopped.

```bash
python3 -m blind.run --dry-run                # K-g1..K-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m blind.score       # Stage C · K-a to K-e, and K-f
PYTHONHASHSEED=0 python3 -m blind.readings    # POST-RUN · K-d under other directions
PYTHONHASHSEED=0 python3 -m blind.cycles      # POST-RUN · why run 1 closed cycles
PYTHONHASHSEED=0 python3 -m blind.closure     # POST-RUN · what the transitive order would decide
PYTHONHASHSEED=0 python3 -m blind.yielding    # POST-RUN · which edge of a cycle should yield
.venv/bin/python -m blind.run --smoke         # Stage B · spends · only on Sergi's say
.venv/bin/python -m blind.run --rep 1         # then --rep 2 and --rep 3, never in parallel
```

**[`PLAN_SCREEN.md`](PLAN_SCREEN.md) closed on 2026-10-15**: what the screen of
compiled rules does to the model. Sergi signed §0 on 2026-10-14, before any of
its figures existed. It asked the model, under prompt v1 and with reasoning
off, every ticket of `PLAN_FIDELITY.md`'s draw with the ticket alone, twice, and
set the answers beside that plan's answers with the screen, on decisions whose
tickets nobody had asked without one. Its record is
[`results_screen/FINDINGS_SCREEN.md`](results_screen/FINDINGS_SCREEN.md). Its
gate reads that plan and no other, and guards its three writers. `fidelity/` is
called by it and not edited.

Stages A and C are free, and they reproduce from the committed records.
**Stage B spent**: its records are guarded, and a re-run neither overwrites them
nor gives the same answers back. A paid session does not start without Sergi
asking for it, and one that is interrupted resumes where it stopped.

```bash
python3 -m screen.ask --dry-run                   # V-g1..V-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m screen.sample         # Stage A · the populations, the free readout
PYTHONHASHSEED=0 python3 -m screen.score          # Stage C · V-a to V-d, and V-e
.venv/bin/python -m screen.ask --session smoke    # Stage B · spends · only on Sergi's say
.venv/bin/python -m screen.ask --session anchor   # then --session ticket_only, never in parallel
```

**[`PLAN_BOUND.md`](PLAN_BOUND.md) closed on 2026-10-17**: how much of the
residue between rung 3's best searched order and its coverage bound is slack.
Sergi signed §0 on 2026-10-17, before any of its figures existed. It packs
cycles of cases each of whose right rules are all wrong for the next, which no
order can all get right, into a certificate of cases every order loses. The
certificate is checked from the masks alone, on the instances the audited
search ran on. Its record is
[`results_bound/FINDINGS_BOUND.md`](results_bound/FINDINGS_BOUND.md). Its gate
reads that plan and no other, and guards its one writer.

**It spends nothing.** It reproduces from the committed records in about two
minutes, nearly all of it the suite inside its first check.

```bash
python3 -m bound.score --dry-run           # H-g1..H-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m bound.score    # H-a to H-d, and the readings of H-e
```

**[`PLAN_RANKING.md`](PLAN_RANKING.md) closed on 2026-10-17**: what the model
states when asked to rank the queues. Sergi signed §0 on 2026-10-17, before any
of its figures existed. It asked the model, with reasoning off, for the one
order between the eight queues that decides which wins a contested ticket. The
question named the queues and nothing else, in twelve presentation orders, each
asked twice, and every answer was scored as a lookup over rung 1's 577 rules.
Its record is
[`results_ranking/FINDINGS_RANKING.md`](results_ranking/FINDINGS_RANKING.md).
Its gate reads that plan and no other, and guards its three writers. `rung3/`,
`rung2/` and `blind/` are called by it and not edited.

Stages A and C are free, and they reproduce from the committed records in about
ten minutes each. Nearly all of that is the first check's enumeration of the
40,320 hierarchies and the suite inside it. **Stage B spent**: its records are
guarded, and a re-run neither overwrites them nor gives the same answers back. A
paid session does not start without Sergi asking for it.

```bash
python3 -m ranking.ask --dry-run                  # M-g1..M-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m ranking.sample        # Stage A · the presentations, the revealed rankings
PYTHONHASHSEED=0 python3 -m ranking.score         # Stage C · M-a to M-e, and M-f
PYTHONHASHSEED=0 python3 -m ranking.yielding      # POST-RUN · which edge of a cycle yields, under its rankings
.venv/bin/python -m ranking.ask --session smoke   # Stage B · spends · only on Sergi's say
.venv/bin/python -m ranking.ask --session session # then the session, never in parallel
```

**[`PLAN_STUDENTS.md`](PLAN_STUDENTS.md) closed on 2026-10-18**: what the
proposer's rules buy over a learner fitted to its answers. Sergi signed §0 on
2026-10-18, before any of its figures existed. It trained three students on the
queues the proposer named at the escalations, and on nothing else: a pruned
decision tree whose leaves are rules of the frozen DSL, a logistic regression,
and the cache's retrieval. It set them beside the rules written from the same
answers, on rung 1's record and on `PLAN_REUSE.md`'s three runs. Its record is
[`results_students/FINDINGS_STUDENTS.md`](results_students/FINDINGS_STUDENTS.md).
Its gate reads that plan and no other, and guards its one writer. `ilp/`,
`rung3/` and `edges/` are called by it and not edited.

**It spends nothing.** It reproduces from the committed records in about five
and a half minutes, about half of it the suite inside its first check.

```bash
python3 -m students.score --dry-run           # T-g1..T-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m students.score    # T-a to T-e, and the readings of T-f
PYTHONHASHSEED=0 python3 -m students.readings # POST-RUN · the three readings it left open
```

**[`PLAN_ESCALATIONS.md`](PLAN_ESCALATIONS.md) closed on 2026-10-19**: what a
reviewer's labels at the escalations buy the order. Sergi signed §0 on
2026-10-19, before any of its figures existed. It handed rung 3's search the
truth of sets of rung 1's train-half escalations, at the audit's label budgets
and with the audit's own instrument, and set each beside that record's own
random draws of train cases at the same budget. Three rules chose which
escalations to label first. Its record is
[`results_escalations/FINDINGS_ESCALATIONS.md`](results_escalations/FINDINGS_ESCALATIONS.md).
Its gate reads that plan and no other, and guards its one writer. `rung3/`,
`students/` and `reuse/` are called by it and not edited.

**It spends nothing.** It reproduces from the committed records in about twelve
minutes, about a third of it the suite inside its first check.

```bash
python3 -m escalations.score --dry-run          # J-g1..J-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m escalations.score   # J-a to J-e, and the readings of J-f
```

**[`PLAN_SPOTCHECK.md`](PLAN_SPOTCHECK.md) closed on 2026-10-19**: what a random
audit of the system's decisions buys beside the escalations. Sergi signed §0 on
2026-10-19, before any of its figures existed. It handed rung 3's search the
truth of every train-half escalation and of a random draw of the cases rung 1's
engine decided itself, at the optimizer audit's label budgets and in nested
draws, and read each order between the escalations alone and the whole train
half. The decisions alone were read beside, on the same draws. Its record is
[`results_spotcheck/FINDINGS_SPOTCHECK.md`](results_spotcheck/FINDINGS_SPOTCHECK.md).
Its gate reads that plan and no other, and guards its one writer.
`escalations/`, `rung3/` and `reuse/` are called by it and not edited.

**It spends nothing.** It reproduces from the committed records in about fifteen
minutes, about a sixth of it the suite inside its first check.

```bash
python3 -m spotcheck.score --dry-run          # N-g1..N-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m spotcheck.score   # N-a to N-e, and the readings of N-f
PYTHONHASHSEED=0 python3 -m spotcheck.readings  # POST-RUN · which tickets teach T3_ENGINEERING
```

**[`PLAN_UNREACHED.md`](PLAN_UNREACHED.md) closed on 2026-10-20**: what the rules
no label reaches hold, and what deferring them buys. Sergi signed §0 on
2026-10-20, before any of its figures existed. It took the rules no labelled
case matches, which rung 3's search leaves where its start put them, and moved
them in the escalations' order and the whole train half's: each alone to the
front, read with the truth, and all below every reached rule, without it,
beside random placements of the same rules. The optimizer audit's label curve
was read the same way. Its record is
[`results_unreached/FINDINGS_UNREACHED.md`](results_unreached/FINDINGS_UNREACHED.md).
Its gate reads that plan and no other, and guards its one writer.
`escalations/`, `spotcheck/`, `rung3/` and `reuse/` are called by it and not
edited.

**It spends nothing.** It reproduces from the committed records in about eleven
minutes, about a third of it the suite inside its first check.

```bash
python3 -m unreached.score --dry-run          # Z-g1..Z-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m unreached.score   # Z-a to Z-e, and the readings of Z-f
PYTHONHASHSEED=0 python3 -m unreached.keyword_half  # POST-RUN · what the keyword holds over the space
```

**[`PLAN_MANUAL.md`](PLAN_MANUAL.md) closed on 2026-10-21**: the authority
channel, the policy given to the proposer at three levels. Sergi signed §0 on
2026-10-21, before any of its figures existed.
- **The levels.** It handed the model the policy, with reasoning off, as a
  catalogue of what each queue is for, as that catalogue with a prose manual,
  and as the 29 rules as text.
- **The shapes.** It ran each level, and the bare names beside them, compiled
  once in one answer and inside `PLAN_REUSE.md`'s loop.

Its record is
[`results_manual/FINDINGS_MANUAL.md`](results_manual/FINDINGS_MANUAL.md). Its
gate reads that plan and no other, and guards its four writers. `rung2/`,
`reuse/`, `edges/`, `blind/` and `rung3/` are called by it and not edited.

Stages A and C are free, and each reproduces from the committed records in a
few minutes, most of it the suite inside its first check. **Stages B1 and B2
spent**: their records are guarded, and a re-run neither overwrites them nor
gives the same answers back. A paid run does not start without Sergi asking for
it. B2's twelve runs take over an hour between them, so they ran in Sergi's
terminal.

```bash
python3 -m manual.run --dry-run                  # G-g1..G-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m manual.sample        # Stage A · the texts, the prompts, the references
PYTHONHASHSEED=0 python3 -m manual.score         # Stage C · G-a to G-f, and G-g
PYTHONHASHSEED=0 python3 -m manual.readings      # POST-RUN · three readings Stage C left free
PYTHONHASHSEED=0 python3 -m manual.after_readings  # POST-RUN · the first, on K-a's own surface
PYTHONHASHSEED=0 python3 -m manual.notes         # POST-RUN · the notes, on a codebook frozen on the first runs
.venv/bin/python -m manual.ask --session smoke   # Stage B1 · spends · only on Sergi's say
.venv/bin/python -m manual.ask --session session # then the session, never in parallel
.venv/bin/python -m manual.run --smoke           # Stage B2 · spends · twenty cases at level 3
.venv/bin/python -m manual.run --level 0 --rep 1 # then the twelve runs, in §2.5's order
```

**[`PLAN_APPLY.md`](PLAN_APPLY.md) closed on 2026-10-24**: the rules applied
ticket by ticket, with and without the screen. Sergi signed §0 on 2026-10-23,
before any of its figures existed.
- **What it asked.** It took every escalation of `PLAN_MANUAL.md`'s twelve loop
  runs whose screen was not empty, and asked it again on one day, with
  reasoning off, each prompt twice. One arm got the escalation's own prompt,
  screen and all, rebuilt from the records. The other got the ticket alone,
  under the same system prompt and v1's empty base. The ticket alone was also
  asked under the bare names.
- **Why.** At the escalations the proposer applied the rules it was given far
  below the exactness with which it transcribes them, and nothing had
  separated the screen's pull from the application itself.

Its record is
[`results_apply/FINDINGS_APPLY.md`](results_apply/FINDINGS_APPLY.md). Its gate
reads that plan and no other, and guards its three writers. `manual/`,
`fidelity/` and `rung2/` are called by it and not edited.

Stages A and C are free, and each reproduces from the committed records in a
few minutes, most of it the suite inside its first check. **Stage B spent**:
its records are guarded, and a re-run neither overwrites them nor gives the
same answers back. A paid run does not start without Sergi asking for it. Each
pass took over an hour, so they ran in Sergi's terminal.

```bash
python3 -m apply.ask --dry-run                                # X-g1..X-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m apply.sample                      # Stage A · the design and the references
PYTHONHASHSEED=0 python3 -m apply.score                       # Stage C · X-a to X-f, and X-g
PYTHONHASHSEED=0 python3 -m apply.providers                   # POST-RUN · each row within one provider's answers
PYTHONHASHSEED=0 .venv/bin/python -m apply.ask --session smoke  # Stage B · spends · only on Sergi's say
PYTHONHASHSEED=0 .venv/bin/python -m apply.ask --session pass1  # then pass 1, then pass 2, never in parallel
```

**[`PLAN_QUEUE_ALONE.md`](PLAN_QUEUE_ALONE.md) closed on 2026-10-24**: the
queue asked alone, without a rule to write. Sergi signed §0 on 2026-10-24,
before any of its figures existed.
- **What it asked.** It took `PLAN_APPLY.md`'s ticket prompts and asked them
  again on one day, each twice, every call pinned to one provider, in three
  arms. One is `PLAN_APPLY.md`'s ticket arm, which asks for a rule. One keeps
  that arm's impasse framing and asks for the queue alone. One asks plainly for
  the queue.
- **Why.** With the rules in its prompt and no screen, the proposer still
  misapplied them at the escalations, inside a prompt that frames the ticket as
  an impasse and asks for a rule. Nothing had separated the rule-writing task
  from the application.

Its record is
[`results_queue_alone/FINDINGS_QUEUE_ALONE.md`](results_queue_alone/FINDINGS_QUEUE_ALONE.md).
Its gate reads that plan and no other, and guards its three writers. `apply/`,
`manual/`, `fidelity/` and `rung2/` are called by it and not edited.

Stages A and C are free, and each reproduces from the committed records in a
few minutes, most of it the suite inside its first check. **Stage B spent**:
its records are guarded, and a re-run neither overwrites them nor gives the
same answers back. A paid run does not start without Sergi asking for it. Each
pass took under an hour, in Sergi's terminal.

```bash
python3 -m queue_alone.ask --dry-run                                # QA-g1..QA-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m queue_alone.sample                      # Stage A · the design and the references
PYTHONHASHSEED=0 python3 -m queue_alone.score                       # Stage C · QA-a to QA-f, and QA-g
PYTHONHASHSEED=0 python3 -m queue_alone.orders                      # POST-RUN · where the order errors go
PYTHONHASHSEED=0 .venv/bin/python -m queue_alone.ask --session smoke  # Stage B · spends · only on Sergi's say
PYTHONHASHSEED=0 .venv/bin/python -m queue_alone.ask --session pass1  # then pass 1, then pass 2, never in parallel
```

**[`PLAN_FIRST_MATCH.md`](PLAN_FIRST_MATCH.md) closed on 2026-10-25**: the
first match, asked by name and with reasoning on. Sergi signed §0 on
2026-10-25, before any of its figures existed.
- **What it asked.** It took `PLAN_QUEUE_ALONE.md`'s plain prompts at level 3
  and asked them again on one day, each twice, every call pinned to one
  provider, in three arms. One is that plan's plain question for the queue. One
  asks for the identifier of the rule that applies before its queue. One asks
  the plain question with reasoning on.
- **Why.** Asked plainly with the 29 rules in its prompt, the model still
  passed over the first rule that matches, on a quarter of the escalated
  decisions, and nearly always to the next one. Nothing had separated finding
  the first match from naming its queue, or either from thinking it through.

Its record is
[`results_first_match/FINDINGS_FIRST_MATCH.md`](results_first_match/FINDINGS_FIRST_MATCH.md).
Its gate reads that plan and no other, and guards its three writers.
`queue_alone/`, `apply/`, `manual/`, `fidelity/` and `rung2/` are called by it
and not edited.

Stages A and C are free, and each reproduces from the committed records in a
few minutes, most of it the suite inside its first check. **Stage B spent**:
its records are guarded, and a re-run neither overwrites them nor gives the
same answers back. A paid run does not start without Sergi asking for it. Each
pass took under twenty minutes, in Sergi's terminal.

```bash
python3 -m first_match.ask --dry-run                                # FM-g1..FM-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m first_match.sample                      # Stage A · the design and the references
PYTHONHASHSEED=0 python3 -m first_match.score                       # Stage C · FM-a to FM-f, and FM-g
PYTHONHASHSEED=0 .venv/bin/python -m first_match.ask --session smoke  # Stage B · spends · only on Sergi's say
PYTHONHASHSEED=0 .venv/bin/python -m first_match.ask --session pass1  # then pass 1, then pass 2, never in parallel
```

**[`PLAN_REASONED_RULE.md`](PLAN_REASONED_RULE.md) closed on 2026-10-25**: the
rule written with reasoning on. Sergi signed §0 on 2026-10-25, before any of
its figures existed.
- **What it asked.** It took `PLAN_QUEUE_ALONE.md`'s rule and plain prompts at
  level 3 and asked them again on one day, each twice, every call pinned to
  one provider, in four arms: the rule-writing prompt and the plain question,
  each with reasoning off and on. No prompt is new.
- **Why.** With reasoning on, the plain question had applied the 29 rules on
  every escalated decision. The loop's proposer is asked for a rule, and has
  asked with reasoning off since `PLAN_REUSE.md` §1's amendment. Nothing had
  asked whether reasoning carries into the rule-writing prompt, before any
  loop pays for it.

Its record is
[`results_reasoned_rule/FINDINGS_REASONED_RULE.md`](results_reasoned_rule/FINDINGS_REASONED_RULE.md).
Its gate reads that plan and no other, and guards its three writers.
`first_match/`, `queue_alone/`, `apply/`, `manual/`, `fidelity/`, `reuse/` and
`rung2/` are called by it and not edited; its asker is `first_match/`'s.

Stages A and C are free, and each reproduces from the committed records in a
few minutes, most of it the suite inside its first check. **Stage B spent**:
its records are guarded, and a re-run neither overwrites them nor gives the
same answers back. A paid run does not start without Sergi asking for it. Each
pass took about an hour and three quarters, in Sergi's terminal, most of it the
rule written with reasoning on.

```bash
python3 -m reasoned_rule.ask --dry-run                                # RR-g1..RR-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m reasoned_rule.sample                      # Stage A · the design and the references
PYTHONHASHSEED=0 python3 -m reasoned_rule.score                       # Stage C · RR-a to RR-d, and RR-e
PYTHONHASHSEED=0 .venv/bin/python -m reasoned_rule.ask --session smoke  # Stage B · spends · only on Sergi's say
PYTHONHASHSEED=0 .venv/bin/python -m reasoned_rule.ask --session pass1  # then pass 1, then pass 2, never in parallel
```

**[`PLAN_REASONED_LOOP.md`](PLAN_REASONED_LOOP.md) closed on 2026-11-03**: the
loop with reasoning on. Sergi signed §0 on 2026-10-31, before any of its
figures existed, and §5.5's two amendments on 2026-10-31 and 2026-11-02.
- **What it asked.** It ran `PLAN_REUSE.md`'s loop at n=2000 on rung 2's
  engine, three runs an arm, with level 3's manual and reasoning on, every call
  pinned to one provider.
  - **The protocol.** The first call is blind to the base, and a placement
    round sets each rule against the base's rules of other queues that it
    overlaps. That is v1b.
  - **The arms.** One has the standing trigger. The other also escalates a
    ticket the base decided wrongly, reading its label and never handing it to
    the proposer.
- **Why.** With reasoning on, the model asked for a rule had chosen the queue
  the list gives and written the list's rules. What a loop compiles from such a
  proposer depends on the order its rules get, and on which tickets it is asked
  about.

Its record is
[`results_reasoned_loop/FINDINGS_REASONED_LOOP.md`](results_reasoned_loop/FINDINGS_REASONED_LOOP.md).
Its gate reads that plan and no other, counts its three signature lines, and
guards its six writers. `first_match/`, `queue_alone/`, `reasoned_rule/`,
`manual/`, `blind/`, `authorship/`, `reuse/` and `rung2/` are called by it and
not edited; its asker is `first_match/`'s.

Stages A and C are free, and each reproduces from the committed records in a
few minutes, most of it the suite inside its first check. **Stage B spent**:
its records are guarded, and a re-run neither overwrites them nor gives the
same rules back. A paid run does not start without Sergi asking for it. An
impasse run asked for up to an hour and an error run for about two and a half,
when no outage stopped it. A run stopped by an outage resumes from its partial
file with the same command.

```bash
python3 -m reasoned_loop.run --dry-run                                  # RL-g1..RL-g3, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m reasoned_loop.sample                        # Stage A · the transcriber and the references
PYTHONHASHSEED=0 python3 -m reasoned_loop.score                         # Stage C · RL-a to RL-g, and RL-h
PYTHONHASHSEED=0 python3 -m reasoned_loop.decided                       # POST-RUN · what each placed edge decides
PYTHONHASHSEED=0 python3 -m reasoned_loop.unplaced                      # POST-RUN · where the unplaced answers come from
PYTHONHASHSEED=0 python3 -m reasoned_loop.governed                      # POST-RUN · why its edges sit on regions third rules govern
PYTHONHASHSEED=0 .venv/bin/python -m reasoned_loop.run --smoke          # Stage B · spends · only on Sergi's say
PYTHONHASHSEED=0 .venv/bin/python -m reasoned_loop.run --arm e --rep 1  # then §2.6's order, one run at a time
```

**[`PLAN_CHANNEL.md`](PLAN_CHANNEL.md) closed on 2026-11-07**: the loop under a
trigger a deployment could have. Sergi signed §0 on 2026-11-05, before any of
its figures existed.
- **What it asked.** It ran `PLAN_REASONED_LOOP.md`'s loop again at n=2000 on
  rung 2's engine, with level 3's manual and reasoning on, every call pinned to
  one provider, under v1b. Three runs an arm alternated in one period.
  - **The channel arm** escalates an impasse or a conflict, and a wrong decision
    of the base when that case's draw, fixed before the run, falls below 1/2.
    That is rung 4's feedback channel at coverage 1/2, with no delay and no
    noise.
  - **The error arm** is `PLAN_REASONED_LOOP.md`'s, run again: it escalates
    every wrong decision.
  - **Neither arm** hands the proposer the label, or tells it that the base
    erred.
- **Why.** Asked on every error, the loop had compiled the policy, but that
  trigger reads the truth of every arrival, as no deployment could. A deployment
  hears of some of its errors.

Its record is
[`results_channel/FINDINGS_CHANNEL.md`](results_channel/FINDINGS_CHANNEL.md).
Its gate reads that plan and no other, counts its signature line, and guards its
five writers. `reasoned_loop/`, `manual/`, `blind/`, `authorship/`, `reuse/` and
`rung2/` are called by it and not edited; its proposer and its asker are
`reasoned_loop/`'s.

Stages A and C are free, and each reproduces from the committed records in a
few minutes, most of it the suite inside its first check. **Stage B spent**:
its records are guarded, and a re-run neither overwrites them nor gives the
same rules back. A paid run does not start without Sergi asking for it. A run
asked for about an hour and a half to two hours when no outage stopped it. A
run stopped by an outage resumes from its partial file with the same command.

```bash
python3 -m channel.run --dry-run                                  # CH-g1..CH-g3, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m channel.sample                        # Stage A · the draws, the transcriber and the references
PYTHONHASHSEED=0 python3 -m channel.score                         # Stage C · CH-a to CH-f, and CH-g
PYTHONHASHSEED=0 python3 -m channel.lost                          # POST-RUN · why c r1 lost SECURITY_INCIDENT
PYTHONHASHSEED=0 python3 -m channel.oncall                        # POST-RUN · why c r2 recalled less ONCALL_ESCALATION
PYTHONHASHSEED=0 .venv/bin/python -m channel.run --smoke          # Stage B · spends · only on Sergi's say
PYTHONHASHSEED=0 .venv/bin/python -m channel.run --arm e --rep 1  # then §2.3's order, one run at a time
```

**[`PLAN_PLACEMENT.md`](PLAN_PLACEMENT.md) closed on 2026-11-08**: the placement
round that lists only what the engine can still order, beside v1b. Sergi signed
§0 on 2026-11-07, before any of its figures existed.
- **What it asked.** It ran `PLAN_CHANNEL.md`'s channel arm again at n=2000 on
  rung 2's engine, with level 3's manual and reasoning on, every call pinned to
  DeepInfra's fp8 endpoint. Three runs of each round alternated, run `k` of each
  under the draws of `PLAN_CHANNEL.md`'s c r`k`.
  - **v1b** is that plan's round, unchanged. It lists every rule of another
    queue the draft meets, and refuses an answer that leaves one without a side.
  - **v1c** leaves out of that list the rules nested with the draft, which
    containment already orders, and those whose shared region with it third
    rules already govern. A round whose list comes out empty is not sent.
  - **A bridge** asked 40 first calls of Baidu and of DeepInfra on one day,
    before the first run.
- **Why.** Read POST-RUN, most of the loop's unplaced answers had left out a
  nested rule, as level 3's system prompt says to, and in `PLAN_CHANNEL.md`'s
  c r1 that refusal cost a queue.

Its record is
[`results_placement/FINDINGS_PLACEMENT.md`](results_placement/FINDINGS_PLACEMENT.md).
Its gate reads that plan and no other, counts its signature line, and guards its
three writers. `channel/`, `reasoned_loop/`, `queue_alone/`, `manual/`, `blind/`,
`authorship/`, `edges/`, `fidelity/`, `reuse/`, `rung2/` and `rung3/` are called
by it and not edited; its proposer and its asker are `reasoned_loop/`'s, with this
plan's pin.

Stages A and C are free, and each reproduces from the committed records in a
few minutes, most of it the suite inside its first check. **Stage B spent**:
its records are guarded, and a re-run neither overwrites them nor gives the
same rules back. A paid run does not start without Sergi asking for it. A run
took two to four and a half hours on DeepInfra, which refused no call for the
rate. A run stopped by an outage resumes from its partial file with the same
command.

```bash
python3 -m placement.run --dry-run                                    # PL-g1..PL-g3, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m placement.sample                          # Stage A · the drafting reading, the transcriber and the references
PYTHONHASHSEED=0 python3 -m placement.score                           # Stage C · PL-a to PL-f, and PL-g
PYTHONHASHSEED=0 python3 -m placement.oncall                          # POST-RUN · why the runs under run 3's draws lost ONCALL_ESCALATION
PYTHONHASHSEED=0 python3 -m placement.provider                        # POST-RUN · whether the cut is the provider's, on the bridge
PYTHONHASHSEED=0 python3 -m placement.births                          # POST-RUN · whether the cut is why the loop's births are narrow
PYTHONHASHSEED=0 python3 -m placement.cost                            # POST-RUN · what the cuts cost
PYTHONHASHSEED=0 .venv/bin/python -m placement.run --smoke            # Stage B · spends · only on Sergi's say
PYTHONHASHSEED=0 .venv/bin/python -m placement.run --bridge           # then the bridge, before the first run
PYTHONHASHSEED=0 .venv/bin/python -m placement.run --arm v1c --rep 1  # then §2.4's order, one run at a time
```

**[`PLAN_WHOLE.md`](PLAN_WHOLE.md) closed on 2026-11-10**: a first call that asks
for the governing rule's region whole, beside v1c. Sergi signed §0 on 2026-11-09,
before any of its figures existed.
- **What it asked.** It ran `PLAN_PLACEMENT.md`'s v1c arm again at n=2000 on
  rung 2's engine, with level 3's manual and reasoning on, every call pinned to
  DeepInfra's fp8 endpoint. Three runs of each arm alternated, run `k` of each
  under the draws of `PLAN_CHANNEL.md`'s c r`k`.
  - **v1c** is that plan's arm, unchanged.
  - **v1d** replaces one paragraph of v1c's first call by T1, which asks for the
    region of the list's rule that governs the ticket, whole. It names no queue
    and no rule.
- **Why.** Read POST-RUN, `PLAN_PLACEMENT.md`'s narrow births were mostly the
  governing rule's region cut by one listed rule, and the cuts cost the rarest
  queue.

Its record is
[`results_whole/FINDINGS_WHOLE.md`](results_whole/FINDINGS_WHOLE.md). Its gate
reads that plan and no other, counts its signature line, and guards its three
writers. `placement/`, `channel/`, `reasoned_loop/`, `manual/`, `blind/`,
`authorship/`, `edges/`, `fidelity/`, `reuse/` and `rung2/` are called by it and
not edited; its proposer and its asker are `placement/`'s, with that plan's pin.

Stages A and C are free, and each reproduces from the committed records in a
few minutes, most of it the suite inside its first check. **Stage B spent**:
its records are guarded, and a re-run neither overwrites them nor gives the
same rules back. A paid run does not start without Sergi asking for it. A run
took one and a half to six hours on DeepInfra, which refused no call for the
rate. A run stopped by an outage resumes from its partial file with the same
command.

```bash
python3 -m whole.run --dry-run                                    # WR-g1..WR-g3, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m whole.sample                          # Stage A · the drafting reading, the transcriber and the references
PYTHONHASHSEED=0 python3 -m whole.score                           # Stage C · WR-a to WR-f, and WR-g
PYTHONHASHSEED=0 python3 -m whole.oncall                          # POST-RUN · why v1d cut at the rarest queue's tickets
PYTHONHASHSEED=0 python3 -m whole.security                        # POST-RUN · why every v1c base lost a sixth of SECURITY_INCIDENT
PYTHONHASHSEED=0 python3 -m whole.paragraph                       # POST-RUN · whether the blind paragraph is why the first call cuts
PYTHONHASHSEED=0 .venv/bin/python -m whole.run --smoke            # Stage B · spends · only on Sergi's say
PYTHONHASHSEED=0 .venv/bin/python -m whole.run --arm v1c --rep 1  # then §2.3's order, one run at a time
```

**[`PLAN_HALVES.md`](PLAN_HALVES.md) closed on 2026-11-12**: which half of v2b's
base paragraph makes the loop's first call cut. Sergi signed §0 on 2026-11-10,
before any of its figures existed.
- **What it asked.** It asked the loop's first call alone, with level 3's manual
  and reasoning on, every call pinned to DeepInfra's fp8 endpoint, at 136
  tickets the reasoning loops escalated. Four arms differ in the paragraph that
  stands where the base would be:
  - **`e`**, the empty base;
  - **`v`**, v2b's paragraph: the base is not shown, and overlapping rules of
    another queue will be listed;
  - **`h`**, its first half alone;
  - **`o`**, its overlap clause on the empty base.

  Two passes asked every prompt once, the arms interleaved, and a third session
  asked the rarest queue's seven tickets four times more.
- **Why.** Read POST-RUN, the loops' first calls under v2b's paragraph wrote the
  governing region about half as often as the same model under an empty base,
  and the two prompts differ in that paragraph alone.

Its record is [`results_halves/FINDINGS_HALVES.md`](results_halves/FINDINGS_HALVES.md). Its
gate reads that plan and no other, counts its signature line, and guards its
three writers. `whole/`, `placement/`, `reasoned_loop/`, `first_match/`,
`fidelity/`, `authorship/`, `reasoned_rule/`, `queue_alone/`, `escalations/`,
`reuse/` and `rung2/` are called by it and not edited; its asker is the loop's,
with `placement/`'s pin.

Stages A and C are free, and each reproduces from the committed records in a
few minutes, most of it the suite inside its first check. **Stage B spent**:
its records are guarded, and a re-run neither overwrites them nor gives the
same answers back. A paid session does not start without Sergi asking for it.
A pass took about ten to twelve hours of calls on DeepInfra, which refused no
call for the rate. A session stopped by an outage resumes from its partial file
with the same command.

```bash
python3 -m halves.ask --dry-run                                  # HV-g1..HV-g3, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m halves.sample                        # Stage A · the design and the references
PYTHONHASHSEED=0 python3 -m halves.score                         # Stage C · HV-a to HV-f, and HV-g
PYTHONHASHSEED=0 python3 -m halves.hidden                        # POST-RUN · why the hidden half cuts
PYTHONHASHSEED=0 .venv/bin/python -m halves.ask --session smoke  # Stage B · spends · only on Sergi's say
PYTHONHASHSEED=0 .venv/bin/python -m halves.ask --session pass1  # then pass2 and oncall, one session at a time
```

**[`PLAN_CORRECTIONS.md`](PLAN_CORRECTIONS.md) closed on 2026-11-14**: the
learning regime, a report that carries the true queue under level 1's catalogue.
Sergi signed §0 on 2026-11-12, before any of its figures existed.
- **What it asked.** It ran `PLAN_PLACEMENT.md`'s v1c at level 1, the catalogue,
  with reasoning on, every call pinned to DeepInfra's fp8 endpoint, under
  `PLAN_CHANNEL.md`'s channel at coverage 1/2: three runs an arm, alternating.
  - **Arm L**'s first call, at an escalation caused by a reported error, carried
    a report naming the ticket's true queue.
  - **Arm N**'s carried nothing.
  - **Beside L's labels**, the model compiled the same labels at once, at
    checkpoints, through `harness/ask_pool.py`, and `PLAN_ILP.md`'s inducer and
    `PLAN_STUDENTS.md`'s students learned them.
- **Why.** No LLM proposer in this tree had been handed a label, so this is the
  first protocol in which the system could learn what its prompt does not hold.
  The technical review of November 11, 2026 proposed it.

Its record is [`results_corrections/FINDINGS_CORRECTIONS.md`](results_corrections/FINDINGS_CORRECTIONS.md). Its
gate reads that plan and no other, counts its signature line, and guards its
four writers. `placement/`, `channel/`, `reasoned_loop/`, `manual/`, `ilp/`,
`students/`, `edges/`, `whole/`, `blind/`, `authorship/`, `reuse/`,
`first_match/` and `rung2/` are called by it and not edited. It breaks the
oracle's separation on purpose, by one route, which its tests pin.

Stages A and C are free, and each reproduces from the committed records in under
ten minutes, most of it the suite inside its first check. **Stage B
spent**: its records are guarded, and a re-run neither overwrites them nor gives
the same rules back. A paid run does not start without Sergi asking for it. A
run took about four to eight and a half hours of calls on DeepInfra, which
refused no call for the rate. A run stopped by an outage resumes from its partial file with
the same command.

```bash
python3 -m corrections.run --dry-run                                  # CR-g1..CR-g3, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m corrections.sample                        # Stage A · the references
PYTHONHASHSEED=0 python3 -m corrections.score                         # Stage C · CR-a to CR-f, and CR-g
PYTHONHASHSEED=0 python3 -m corrections.forgotten                     # POST-RUN · why the final base forgets its corrections
PYTHONHASHSEED=0 .venv/bin/python -m corrections.run --smoke --arm n  # Stage B · spends · only on Sergi's say
PYTHONHASHSEED=0 .venv/bin/python -m corrections.ask --session smoke  # then §9's order, one step at a time
```

What each of them should produce is in the record it belongs to; the corrected
figures are indexed in [`STATUS.md`](STATUS.md). And before touching anything,
the test suite — **no API calls and no writes to `results*/`**:

```bash
python3 -m unittest discover
```

The pre-commit hook and CI run it on their own; to enable the hook in your
clone, once:

```bash
git config core.hooksPath .githooks
```

> **Rungs 3 and 4 do not reproduce their published figures to the digit, and
> since August 8, 2026 those figures are also superseded.** Two separate things,
> now separated by measurement:
>
> - **The tie-break**, non-deterministic because it depended on `PYTHONHASHSEED`,
>   fixed on August 6, 2026. `order_search` no longer prints what the record
>   says, by a margin in the fourth decimal.
> - **The algorithm.** The greedy search was weak. A multi-start local search,
>   validated first against the hidden policy whose optimum is known by
>   construction, moved rung 3's test and withdrew rung 4's "change of regime".
>
> Leaving the tie-break fix unexecuted until the optimizer arrived is what made
> those two separable, and what each was worth is in the errata both rungs'
> FINDINGS carry; the original records are untouched beside the new ones.
>
> **Which surface a figure is measured on now matters and is stated** — the
> long-tailed corpus or the uniform case space, which answer different questions
> and can rank two orders in opposite directions. See
> [`STATUS.md`](STATUS.md), "Before reading any figure".
>
> The ceilings that do not depend on any search reproduce exactly and are
> unaffected.

**The only thing that costs money** is the real proposer, which needs the venv
and the key (see *Getting started*):

```bash
.venv/bin/python run_experiment.py llm --n 100                      # rung 1
.venv/bin/python -m rung2.run2 --n 100 --seed 17 --prompt-version v2   # rung 2
```

They write `results/llm_run_n100.json` and `results2/llm_run2_n100_v2.json`. If
the file is already there they abort without spending anything; see the warning
below.

`rung2/run2.py` accepts `--prompt-version v1|v2`; both versions of the prompt
are kept in the code and every run stores in full the one it used. The record of
the change is in [`results2/CHANGELOG.md`](results2/CHANGELOG.md).

> ⚠️ **Reproducing a figure overwrites its own record.** Nearly all the scripts
> above dump their JSON on finishing, over the published file:
>
> | script | file it rewrites | guarded |
> |---|---|---|
> | `run_experiment.py frontier` | `results/frontier.json` | no, on purpose |
> | `run_experiment.py llm` | `results/llm_run_n<N>.json` | **yes** |
> | `harness/subsumption_check.py` | `results/subsumption.json` | no, on purpose |
> | `harness/default_rule_control.py` | `results/default_rule_control.json` | no, on purpose |
> | `harness/learned_subsumption.py` | `results/learned_subsumption.json` | no, on purpose |
> | `rung2/ceiling_check2.py` | `results2/ceiling2.json` | no, on purpose |
> | `rung2/ceiling_check2_space.py` | `results2/ceiling2_space.json` | no, on purpose |
> | `sensitivity/generator_check.py` | `results_sensitivity/generator_check.json` | no, on purpose |
> | `sensitivity/sweep.py` | `results_sensitivity/sweep.json` | **refuses while the plan is unsigned** |
> | `ilp/induce_check.py` | `results_ilp/induce_check.json` | no, on purpose |
> | `ilp/compare.py` | `results_ilp/compare.json` | **refuses while the plan is unsigned** |
> | `ilp/labels.py` | `results_ilp/labels.json` | **refuses while the plan is unsigned** |
> | `ilp/margin.py` | `results_ilp/margin.json` | **refuses while the plan is unsigned** |
> | `ilp/chosen.py` | `results_ilp/chosen.json` | **refuses while the plan is unsigned** |
> | `reuse/frontier.py` | `results_reuse/frontier.json` | **refuses while the plan is unsigned** |
> | `reuse/readout.py` | `results_reuse/readout_n100.json` | **refuses while the plan is unsigned** |
> | `reuse/run.py` | `results_reuse/run_n*.json` | **yes** — and it refuses while the plan is unsigned |
> | `reuse/score.py` | `results_reuse/score.json` | **refuses while the plan is unsigned** |
> | `reuse/structure.py` | `results_reuse/structure.json` | **refuses while the plan is unsigned** |
> | `authorship/run.py` | `results_authorship/run_n*.json` | **yes** — and it refuses while the plan is unsigned |
> | `authorship/score.py` | `results_authorship/score.json` | **refuses while the plan is unsigned** |
> | `authorship/refused.py` | `results_authorship/refused.json` | **refuses while the plan is unsigned** |
> | `overlap/run.py` | `results_overlap/run_n*.json` | **yes** — and it refuses while the plan is unsigned |
> | `overlap/score.py` | `results_overlap/score.json` | **refuses while the plan is unsigned** |
> | `overlap/readings.py` | `results_overlap/readings.json` | **refuses while the plan is unsigned** |
> | `overlap/readings_v1.py` | `results_overlap/readings_v1.json` | **refuses while the plan is unsigned** |
> | `blind/run.py` | `results_blind/run_n*.json` | **yes** — and it refuses while the plan is unsigned |
> | `blind/score.py` | `results_blind/score.json` | **refuses while the plan is unsigned** |
> | `blind/readings.py` | `results_blind/readings.json` | **refuses while the plan is unsigned** |
> | `blind/cycles.py` | `results_blind/cycles.json` | **refuses while the plan is unsigned** |
> | `blind/closure.py` | `results_blind/closure.json` | **refuses while the plan is unsigned** |
> | `blind/yielding.py` | `results_blind/yielding.json` | **refuses while the plan is unsigned** |
> | `fidelity/sample.py` | `results_fidelity/sample.json` | **refuses while the plan is unsigned** |
> | `fidelity/ask.py` | `results_fidelity/ask_*.json` | **yes** — and it refuses while the plan is unsigned |
> | `fidelity/score.py` | `results_fidelity/score.json` | **refuses while the plan is unsigned** |
> | `screen/sample.py` | `results_screen/sample.json` | **refuses while the plan is unsigned** |
> | `screen/ask.py` | `results_screen/ask_*.json` | **yes** — and it refuses while the plan is unsigned |
> | `screen/score.py` | `results_screen/score.json` | **refuses while the plan is unsigned** |
> | `ranking/sample.py` | `results_ranking/sample.json` | **refuses while the plan is unsigned** |
> | `ranking/ask.py` | `results_ranking/ask_*.json` | **yes** — and it refuses while the plan is unsigned |
> | `ranking/score.py` | `results_ranking/score.json` | **refuses while the plan is unsigned** |
> | `ranking/yielding.py` | `results_ranking/yielding.json` | **refuses while the plan is unsigned** |
> | `manual/sample.py` | `results_manual/sample.json` | **refuses while the plan is unsigned** |
> | `manual/ask.py` | `results_manual/compile_*.json` | **yes** — and it refuses while the plan is unsigned |
> | `manual/run.py` | `results_manual/loop_*.json` | **yes** — and it refuses while the plan is unsigned |
> | `manual/score.py` | `results_manual/score.json` | **refuses while the plan is unsigned** |
> | `manual/readings.py` | `results_manual/readings.json` | **refuses while the plan is unsigned** |
> | `manual/after_readings.py` | `results_manual/after_readings.json` | **refuses while the plan is unsigned** |
> | `manual/notes.py` | `results_manual/notes.json` | **refuses while the plan is unsigned** |
> | `apply/sample.py` | `results_apply/sample.json` | **refuses while the plan is unsigned** |
> | `apply/ask.py` | `results_apply/ask_*.json` | **yes** — and it refuses while the plan is unsigned |
> | `apply/score.py` | `results_apply/score.json` | **refuses while the plan is unsigned** |
> | `apply/providers.py` | `results_apply/providers.json` | **refuses while the plan is unsigned** |
> | `queue_alone/sample.py` | `results_queue_alone/sample.json` | **refuses while the plan is unsigned** |
> | `queue_alone/ask.py` | `results_queue_alone/ask_*.json` | **yes** — and it refuses while the plan is unsigned |
> | `queue_alone/score.py` | `results_queue_alone/score.json` | **refuses while the plan is unsigned** |
> | `queue_alone/orders.py` | `results_queue_alone/orders.json` | **refuses while the plan is unsigned** |
> | `first_match/sample.py` | `results_first_match/sample.json` | **refuses while the plan is unsigned** |
> | `first_match/ask.py` | `results_first_match/ask_*.json` | **yes** — and it refuses while the plan is unsigned |
> | `first_match/score.py` | `results_first_match/score.json` | **refuses while the plan is unsigned** |
> | `reasoned_rule/sample.py` | `results_reasoned_rule/sample.json` | **refuses while the plan is unsigned** |
> | `reasoned_rule/ask.py` | `results_reasoned_rule/ask_*.json` | **yes** — and it refuses while the plan is unsigned |
> | `reasoned_rule/score.py` | `results_reasoned_rule/score.json` | **refuses while the plan is unsigned** |
> | `reasoned_loop/sample.py` | `results_reasoned_loop/sample.json` | **refuses while the plan is unsigned** |
> | `reasoned_loop/run.py` | `results_reasoned_loop/loop_*.json` | **yes** — and it refuses while the plan is unsigned |
> | `reasoned_loop/score.py` | `results_reasoned_loop/score.json` | **refuses while the plan is unsigned** |
> | `reasoned_loop/decided.py` | `results_reasoned_loop/decided.json` | **refuses while the plan is unsigned** |
> | `reasoned_loop/unplaced.py` | `results_reasoned_loop/unplaced.json` | **refuses while the plan is unsigned** |
> | `reasoned_loop/governed.py` | `results_reasoned_loop/governed.json` | **refuses while the plan is unsigned** |
> | `channel/sample.py` | `results_channel/sample.json` | **refuses while the plan is unsigned** |
> | `channel/run.py` | `results_channel/loop_*.json` | **yes** — and it refuses while the plan is unsigned |
> | `channel/score.py` | `results_channel/score.json` | **refuses while the plan is unsigned** |
> | `channel/lost.py` | `results_channel/lost.json` | **refuses while the plan is unsigned** |
> | `channel/oncall.py` | `results_channel/oncall.json` | **refuses while the plan is unsigned** |
> | `placement/sample.py` | `results_placement/sample.json` | **refuses while the plan is unsigned** |
> | `placement/run.py` | `results_placement/loop_*.json, bridge.json` | **yes** — and it refuses while the plan is unsigned |
> | `placement/score.py` | `results_placement/score.json` | **refuses while the plan is unsigned** |
> | `placement/oncall.py` | `results_placement/oncall.json` | **refuses while the plan is unsigned** |
> | `placement/provider.py` | `results_placement/provider.json` | **refuses while the plan is unsigned** |
> | `placement/births.py` | `results_placement/births.json` | **refuses while the plan is unsigned** |
> | `placement/cost.py` | `results_placement/cost.json` | **refuses while the plan is unsigned** |
> | `whole/sample.py` | `results_whole/sample.json` | **refuses while the plan is unsigned** |
> | `whole/run.py` | `results_whole/loop_*.json` | **yes** — and it refuses while the plan is unsigned |
> | `whole/score.py` | `results_whole/score.json` | **refuses while the plan is unsigned** |
> | `whole/oncall.py` | `results_whole/oncall.json` | **refuses while the plan is unsigned** |
> | `whole/security.py` | `results_whole/security.json` | **refuses while the plan is unsigned** |
> | `whole/paragraph.py` | `results_whole/paragraph.json` | **refuses while the plan is unsigned** |
> | `halves/sample.py` | `results_halves/sample.json` | **refuses while the plan is unsigned** |
> | `halves/ask.py` | `results_halves/ask_*.json` | **yes** — and it refuses while the plan is unsigned |
> | `halves/score.py` | `results_halves/score.json` | **refuses while the plan is unsigned** |
> | `halves/hidden.py` | `results_halves/hidden.json` | **refuses while the plan is unsigned** |
> | `corrections/sample.py` | `results_corrections/sample.json` | **refuses while the plan is unsigned** |
> | `corrections/run.py` | `results_corrections/loop_*.json` | **yes** — and it refuses while the plan is unsigned |
> | `corrections/ask.py` | `results_corrections/atonce_*.json` | **yes** — and it refuses while the plan is unsigned |
> | `corrections/score.py` | `results_corrections/score.json` | **refuses while the plan is unsigned** |
> | `corrections/forgotten.py` | `results_corrections/forgotten.json` | **refuses while the plan is unsigned** |
> | `edges/score.py` | `results_edges/score.json` | **refuses while the plan is unsigned** |
> | `edges/readings.py` | `results_edges/readings.json` | **refuses while the plan is unsigned** |
> | `primacy/score.py` | `results_primacy/score.json` | **refuses while the plan is unsigned** |
> | `bound/score.py` | `results_bound/score.json` | **refuses while the plan is unsigned** |
> | `students/score.py` | `results_students/score.json` | **refuses while the plan is unsigned** |
> | `students/readings.py` | `results_students/readings.json` | **refuses while the plan is unsigned** |
> | `escalations/score.py` | `results_escalations/score.json` | **refuses while the plan is unsigned** |
> | `spotcheck/score.py` | `results_spotcheck/score.json` | **refuses while the plan is unsigned** |
> | `spotcheck/readings.py` | `results_spotcheck/readings.json` | **refuses while the plan is unsigned** |
> | `unreached/score.py` | `results_unreached/score.json` | **refuses while the plan is unsigned** |
> | `unreached/keyword_half.py` | `results_unreached/keyword_half.json` | **refuses while the plan is unsigned** |
> | `why/score.py` | `results_why/score.json` | **refuses while the plan is unsigned** |
> | `rung2/compare_runs.py` | `results2/comparison.json` | only against shrinking |
> | `rung2/note_audit.py` | `results2/note_audit.json` | only against shrinking |
> | `rung2/run2.py` | `results2/llm_run2_<tag>.json` | **yes** |
> | `rung3/order_search.py` | `results3/order_search.json` | no, on purpose |
> | `rung3/budget_and_balance.py` | `results3/budget_and_balance.json` | no, on purpose |
> | `rung4/sweep.py` | `results4/sweep.json` | no, on purpose |
> | `rung3/optimizer_check.py` | `results3/optimizer_check.json` | no, on purpose |
> | `rung3/optimizer_check_wt.py` | `results3/optimizer_check_wt.json` | no, on purpose |
> | `rung3/order_search_ls.py` | `results3/order_search_ls.json` | no, on purpose |
> | `rung3/budget_and_balance_ls.py` | `results3/budget_and_balance_ls.json` | **partial runs get their own name** |
> | `rung3/budget_and_balance_ls.py --start-budget` | `results3/start_budget_check.json` | no, on purpose |
> | `rung4/sweep_ls.py` | `results4/sweep_ls.json` | **partial runs get their own name** |
> | `rung3/order_metrics_run.py` | `results3/order_metrics.json` | no, on purpose |
> | `rung3/order_metrics_corpus.py` | `results3/order_metrics_corpus.json` | no, on purpose |
> | `rung3/rank_transfer.py` | `results3/rank_transfer.json` | no, on purpose |
> | `rung3/order_metrics_touched.py` | `results3/order_metrics_touched.json` | no, on purpose |
> | `rung3/order_metrics_rules.py` | `results3/order_metrics_rules.json` | no, on purpose |
> | `rung3/territory_holders.py` | `results3/territory_holders.json` | no, on purpose |
> | `rung2/pair_benchmark.py` | `results2/pair_benchmark.json` | no, on purpose |
> | `rung2/pair_judgement.py` | `results2/pair_judgement_*.json` | **yes** — it spends, gated on the plan that governs the run |
> | `rung2/pair_judgement_baselines.py` | `results2/pair_judgement_baselines.json` | no, on purpose |
> | `rung2/pair_sample_1600.py` | `results2/pair_sample_1600.json` | no, on purpose |
> | `rung3/floor_by_pool.py` | `results3/floor_by_pool.json` | no, on purpose |
> | `rung3/queue_hierarchy_floor.py` | `results3/queue_hierarchy_floor.json` | no, on purpose |
> | `rung3/declared_order.py` | `results3/declared_order*.json` | no, on purpose |
> | `rung3/edge_direction.py` | `results3/edge_direction*.json` | no, on purpose |
> | `rung3/edge_budget.py` | `results3/edge_budget.json` | no, on purpose |
> | `rung3/edge_sides.py` | `results3/edge_sides.json` | no, on purpose |
> | `rung3/mfas_compilation.py` | `results3/mfas_compilation.json` | no, on purpose |
> | `rung3/edge_dropping.py` | `results3/edge_dropping.json` | no, on purpose |
> | `rung3/answer_asymmetry.py` | `results3/answer_asymmetry.json` | no, on purpose |
> | `rung3/filter_headroom.py` | `results3/filter_headroom.json` | no, on purpose |
> | `rung3/filter_space.py` | `results3/filter_space.json` | no, on purpose |
> | `rung3/identical_rules.py` | `results3/identical_rules.json` | no, on purpose |
> | `rung3/copy_births.py` | `results3/copy_births.json` | no, on purpose |
>
> **[NOTE 2026-08-30] Thirteen rows were added on this date and the table had
> been incomplete since 2026-08-24.** `results3/FINDINGS_AUDIT.md` records the
> under-listing of the pinned lists as F1 and says of the README table that F7
> *"resolved it, which now carries all of them"* — true when written, and false
> from the moment the pairwise thread started adding writers. The pinned lists
> in `tests/` are still F1 and still unfixed; this table is complete again, and
> the audit's F7 line now carries its own dated note.
>
> **[NOTE 2026-08-30, later the same day] F1 is closed and this table is now
> checked.** `tests/test_writer_lists.py` derives the writers from the tree and
> fails if this table and the tree disagree **in either direction**, so a row
> missing here or a module deleted from under a row breaks the suite instead of
> waiting for an audit. The pinned lists it replaced were deleted rather than
> updated: a list that has to be remembered is the defect, not its contents.

> Of everything executed in this README, only `harness/ceiling_check.py` and
> `run_experiment.py models` write nothing — plus the `--dry-run` forms:
> `sensitivity/sweep.py --dry-run` and `ilp/compare.py --dry-run`, which build
> every policy, run every gate and write no record on purpose, and the four of
> `reuse/`, which run `PLAN_REUSE.md`'s blocking checks and write nothing, and
> the three of `fidelity/`, which run `PLAN_FIDELITY.md`'s, and
> `edges/score.py --dry-run`, which runs `PLAN_EDGES.md`'s, and
> `primacy/score.py --dry-run`, which runs `PLAN_PRIMACY.md`'s, and
> `why/score.py --dry-run`, which runs `PLAN_WHY.md`'s, and
> `authorship/run.py --dry-run`, which runs `PLAN_AUTHORSHIP.md`'s, and
> `overlap/run.py --dry-run`, which runs `PLAN_OVERLAP.md`'s, and
> `blind/run.py --dry-run`, which runs `PLAN_BLIND.md`'s, and the three of
> `screen/`, which run `PLAN_SCREEN.md`'s, and `bound/score.py --dry-run`,
> which runs `PLAN_BOUND.md`'s, and the three of `ranking/`, which run
> `PLAN_RANKING.md`'s, and `students/score.py --dry-run`, which runs
> `PLAN_STUDENTS.md`'s, and `escalations/score.py --dry-run`, which runs
> `PLAN_ESCALATIONS.md`'s, and `spotcheck/score.py --dry-run`, which runs
> `PLAN_SPOTCHECK.md`'s, and `unreached/score.py --dry-run`, which runs
> `PLAN_UNREACHED.md`'s, and the four of `manual/`, which run
> `PLAN_MANUAL.md`'s, and the three of `apply/`, which run
> `PLAN_APPLY.md`'s, and the three of `queue_alone/`, which run
> `PLAN_QUEUE_ALONE.md`'s, and the three of `first_match/`, which run
> `PLAN_FIRST_MATCH.md`'s, and the three of `reasoned_rule/`, which run
> `PLAN_REASONED_RULE.md`'s, and the three of `reasoned_loop/`, which run
> `PLAN_REASONED_LOOP.md`'s, and the three of `channel/`, which run
> `PLAN_CHANNEL.md`'s, and the three of `placement/`, which run
> `PLAN_PLACEMENT.md`'s, and the three of `whole/`, which run
> `PLAN_WHOLE.md`'s, and the three of `halves/`, which run
> `PLAN_HALVES.md`'s, and the four of `corrections/`, which run
> `PLAN_CORRECTIONS.md`'s.
>
> **Since August 8, 2026 the two paid commands refuse to overwrite.** The guard
> is in [`harness/record_guard.py`](harness/record_guard.py) and it distinguishes
> three levels, because only one of them needs protecting.
>
> **What is guarded: what costs money and is not deterministic.**
> `run_experiment.py llm` and `rung2/run2.py`. If the destination is occupied
> they abort **before spending a single call** — the check is at startup, not at
> the end — with a message that reads the existing file and says what would be
> lost: when it was recorded, with what model, how many cases, how many rules and
> how many calls it cost. It makes no automatic copy: silent backups pile up and
> people stop looking at them. Two ways out, both explicit:
>
> ```bash
> .venv/bin/python run_experiment.py llm --n 100 --out results/otra_tirada.json
> .venv/bin/python run_experiment.py llm --n 100 --overwrite-record
> ```
>
> The flag is not called `--force` on purpose: it names what it does, so that it
> does not get typed out of habit. And the guard is on the **destination**, not
> on the flag that chose it — `--out` onto an occupied file aborts just the same.
>
> **The `--n` collision is gone too.** Until that date `llm` wrote
> `results/llm_run.json` whatever `--n` it was given, so the smoke test and the
> full run shared a file: `llm --n 100`, the cheap step of the *Getting started*,
> destroyed the 2000-case record. The n now goes in the name —
> `llm_run_n100.json`, `llm_run_n2000.json` — which is what rung 2 already did
> (`llm_run2_n100.json`) and what the smoke record on disk already looked like
> (`llm_run_n100_smoke.json`). The seed only appears when it is not 17. A
> deliberate consequence: **`results/llm_run.json` is no longer the destination of
> any invocation**; it is the closed record of rung 1 and the input of rungs 3
> and 4, and reaching it now takes `--out` *and* the flag. Reproducing that
> figure writes `llm_run_n2000.json`, and comparing the two is a separate,
> deliberate step. `rung2/run2.py` got the same fix on its `--tag`: it now
> includes the prompt version and the seed, so the rung 2 line recommended above
> no longer writes on top of the v1 record.
>
> **What is NOT guarded, also on purpose.** The deterministic, free records:
> re-running them **is** the reproducibility check, and a guard there would get
> in the way. Nor `order_search`, `budget_and_balance` and `sweep`, whose re-run
> with a serious optimizer is planned.
>
> In rungs 1 and 2 the rest of the computation is deterministic and the content
> comes out identical — what changes is the modification date of a closed record,
> see [`results2/RECORD_NOTES.md`](results2/RECORD_NOTES.md). In rungs 3 and 4
> **the content does change**, because the tie-break fix moves the digits.
>
> **The other trap, the one that is about arguments and not about the
> destination.** `compare_runs` and `note_audit` rewrite with **whatever they are
> passed**. Invoking them with one file instead of with
> `results2/llm_run2_*.json` shrinks the record from 8 runs to 1: not a change of
> digits, data loss. Their destination never changes, so the guard above cannot
> see it; what they check is the row count, and they refuse to leave fewer rows
> than they found. Equal or more goes through untouched, which is exactly the
> free reproduction with the full glob. To shrink one on purpose, the same flag.
>
> Since August 7, 2026 there is one more detail: each JSON carries an `_env`
> block with the provenance (see *The tests and the provenance*). When you
> re-run a figure that has not changed, `git diff` shows **only** the
> `recorded_at` field moving — which is precisely the check that it still
> reproduces. The six deterministic, free records in the table already carry it:
> they were re-run that same day to earn it, with the content identical field by
> field ([`results2/RECORD_NOTES.md`](results2/RECORD_NOTES.md)). In that pass
> `comparison.json` and `note_audit.json` also adopted their new shape,
> `{"_env": …, "rows": […]}` instead of the bare list, with the same 8 rows.
>
> **For everything else the safeguard is still git**, and for everything else it
> is enough: `git status` gives away what was touched and
> `git checkout -- <file>` restores it. The records are versioned precisely for
> this. What the guard adds is the one case where git arrives too late — a record
> that cost money and cannot be produced again.

---

## The tests and the provenance

Two different nets, with different purposes.

### The test suite

```bash
python3 -m unittest discover            # 0 API calls, no writes to results*/
python3 -m unittest tests.test_ceilings -v      # a single module
```

It needs no venv and **does not write to `results*/`**: it calls the measurement
functions, never the scripts' `main()`, which do dump their JSON.

What it covers, and why those things:

| module | what it protects |
|---|---|
| `test_encoding_invariant.py` | the 29 DSL rules ≡ their lambdas, and first-match-wins ≡ `true_action`, over the **134,400** combinations. This is the claim that "execution failure, not representation failure" rests on |
| `test_ceilings.py` | the four ceilings to the digit, with their conflict counts and the declared edges |
| `test_default_rule_control.py` | the fifth ceiling, on both surfaces: the specificity engine with the catch-all at its true rank, plus the two invariants that say the control never changes a decision already taken and never resolves a conflict wrongly |
| `test_ceiling2_space.py` | the hybrid ceiling over the exhaustive space, level 1 alone on both surfaces, and the three premises that make the space figure a consequence rather than a coincidence |
| `test_sensitivity.py` | the sensitivity instrument: the five signed bands as named constants, the two constants of §8, the ρ grid, `A-g3`'s parity against the frozen engine, and the gate that counts signatures instead of stopping at the first. **No figure of the sweep** |
| `test_ilp.py` | the ILP instrument: the four signed bands, the 224-condition language with the 29 hidden rules inside it, `I-g3`'s no-leak property, first-match-wins on a list checkable by hand, and the gate. **No figure of the four rows** |
| `test_reuse.py` | the `PLAN_REUSE.md` instrument: §10's constants and §0's five lines, each verdict at its edge, `F` checked by hand, births and the split on a record small enough to check by hand, `U-g2` and `U-g3` on the real inputs, every writer refusing unsigned before it builds the client or writes, the full runs refusing without a smoke run that worked, every paid run refusing a management key — with OpenRouter's endpoint always replaced, so no test reaches the network — and §1's amendment: the proposer's `reasoning` setting sent on every call, retries included, and never by default. **No figure of the plan** |
| `test_fidelity.py` | the `PLAN_FIDELITY.md` instrument: §10's constants and §0's five lines, each verdict at its edge, the gate on one signature line with `PLAN_REUSE.md`'s default untouched, `F-g2` on the three Stage B records and its teeth, every birth prompt against the request rung 2's loop built when the SDK double replays the four v1 n=100 records, the draw and the sessions on the real records, Stage C's arithmetic by hand, every writer refusing unsigned before it builds the client or writes, the smoke and key checks with OpenRouter's endpoint always replaced, and Stage B end to end through the double — resuming, and stopping on an outage. **No figure of the plan** |
| `test_why.py` | the `PLAN_WHY.md` instrument: the constants, the codebook's fingerprint and the development figures pinned, each verdict at its edge, the gate counting every signature line, the codebook on hand-written sentences in Spanish, English and Chinese, the labels and the categorical edge by hand, the rows and §0's statistics by hand, the whole stage end to end on a synthetic record, `Y-g1` to `Y-g3` on the real records with a changed fingerprint, figure and sentence caught, the checks handing the codebook only development sentences, and the writer refusing unsigned before it measures or writes. **No figure of the plan** |
| `test_primacy.py` | the `PLAN_PRIMACY.md` instrument: §8's constants and §0's two lines, each verdict at its edge, the gate counting every signature line, §0's definitions by hand — the slot effect, its symmetry on one queue pair, the favoured queue and a tie —, the whole stage end to end on a synthetic record whose verdicts are worked by hand, `L-g1` to `L-g3` on the real records with a tampered deal and a tampered row caught, the dry run's checks never reaching §0's statistics, and the writer refusing unsigned before it measures or writes. **No figure of the plan** |
| `test_edges.py` | the `PLAN_EDGES.md` instrument: §8's constants and §0's three lines, each verdict at its edge, the gate counting every signature line, the counterfactual rebuild on a scripted run — the record given the declared directions, the replay without edges given none, every departure an ACTION that becomes a CONFLICT, every birth in every arm —, `W-g2` and `W-g3`'s identities on the three Stage B records, the stage's arithmetic and the post-run readings by hand, and both writers refusing unsigned before they measure, read or write. **No figure of the plan** |
| `test_authorship.py` | the `PLAN_AUTHORSHIP.md` instrument: §11's constants and §0's lines, the gate reading that plan and counting, v1e as v1 with one paragraph replaced and its texts hashing to the declared fingerprint, the order paragraph shown only on a conflict, the validator — copies, overlaps, what counts as placed, the seeded listing —, the loop on small worlds through an order answer, a copy, a repair round that places and one that does not, and a failed call, v1's line replayed on a recorded baseline run, the resume — a changed request refused, an outage stopping without keeping its failures —, the smoke check, every writer refusing unsigned, and Stage C's arithmetic by hand, each row at its line and an undefined share unadjudicable. **No figure of the plan** |
| `test_overlap.py` | the `PLAN_OVERLAP.md` instrument: §11's constants and §0's lines, the plan's text for them and the gate counting every signature line, v2e as v2 with one sentence replaced and its texts hashing to the declared fingerprint, v1e's order paragraph only on a conflict, the exempted split into `O` and `S`, the loop on small worlds — an overlap within a queue owing nothing, one across queues placed or refused, a copy, an order answer, rung 2's path with the discipline off —, rung 2's four v2 runs replayed through the loop, §0's statistics at their edges, O-b's rule for runs without room included, every writer refusing unsigned, and the smoke check. **No figure of the plan** |
| `test_blind.py` | the `PLAN_BLIND.md` instrument: §11's constants and §0's lines, the plan's text for them and the gate counting every signature line, v2b as v2e with one paragraph added and its texts hashing to the declared fingerprint, the blind screen on an impasse and v2e's on a conflict, the same-rule check, the blind path on small worlds — a draft that meets no other queue born on one call, one that does placed in a round listing exactly those rules, and a placement that changes the rule, leaves one unplaced or never comes back refused, as are a copy, a rule off its ticket and an order on an impasse —, `PLAN_OVERLAP.md`'s runs replayed through the loop with the blind draft off, §0's statistics at their edges — keyword rules apart, each older rule once, the comparators, the split, and the rules for too few units and for runs without room —, every writer refusing unsigned, and the smoke check. **No figure of the plan** |
| `test_blind_readings.py` | `blind/readings.py`, the POST-RUN reading of `K-d`: how each arm points an edge, an edge within a queue left as declared, what an arm resolves and gets right in the room on small worlds, the coin seeded and summarised, the run-by-run decomposition, the expectation's clauses at their edges, and the writer refusing unsigned. **No figure of the plan** |
| `test_blind_cycles.py` | `blind/cycles.py`, the POST-RUN reading of why run 1 closed cycles: the fork leaving the engine untouched, the side each listed rule is placed on, the ordered and inverted pairs, why an edge closes a cycle in each of the ways a birth can close one, what the base had already decided on small worlds, the slot statistic and its seeded permutation null, the slices of the log each escalation wrote, the smoke run replayed with its forks, the expectation's clauses at their edges, and the writer refusing unsigned. **No figure of the plan** |
| `test_blind_closure.py` | `blind/closure.py`, the POST-RUN reading of what the base's transitive order would decide: the ancestors a chain gives, the undefeated masks with and without the closure, a CONFLICT the closure resolves and one no chain orders, who is right on what it resolves, the coin's and the ranking's counts, the same on corpus cases, the case-by-case closure against the masks, the hidden policy still executed through the closure, the expectation's clauses at their edges, and the writer refusing unsigned. **No figure of the plan** |
| `test_blind_yielding.py` | `blind/yielding.py`, the POST-RUN reading of which edge of a cycle should yield: the log given back to the escalations that wrote it, the order each arm installs the declarations in, which edge yields under arrival and under recency, the ranking's and the oracle's groups, the coin seeded, every arm acyclic and full, what changes against arrival under rung 2's engine and through the closure, the corpus counted as it arrives, the coin's summaries and the pool, the hidden policy kept whole under every order, the expectation's clauses at their edges, the two halves of the space and the coin's draws by what they refused, added after the first and second runs, and the writer refusing unsigned. **No figure of the plan** |
| `test_screen.py` | the `PLAN_SCREEN.md` instrument: §10's constants and §0's lines, each verdict at its edge, the gate counting every signature line, the populations and the tickets counted by their attributes on the real records, every prompt against the digests `PLAN_FIDELITY.md` recorded and a changed screen moving one, `V-g1` giving back `PLAN_FIDELITY.md`'s Stage C to 1e-12 and catching a tampered record, the wrapped client sending every request unchanged and keeping each attempt's `finish_reason`, §0's rule for a run without a value and for the median by hand, every writer refusing unsigned before it builds the client or writes, the smoke and key checks with OpenRouter's endpoint always replaced, Stage B end to end through the double, and Stage C over the double's records with the held-out labels masked. **No figure of the plan** |
| `test_bound.py` | the `PLAN_BOUND.md` instrument: §8's constants, the finder's two and §0's lines, each verdict at its edge, the gate counting every signature line, the argument by hand — a two-case cycle, a ring of three, a cycle by containment and the same shape without it, copies merged, and the hybrid pool's counterexample to a subsumption edge —, `verify` refusing each way a certificate can be wrong and reaching nothing of the finder's, validity against the exact optimum, the packing stopping only when no cycle is left, the same certificate under three values of `PYTHONHASHSEED`, `H-g1` to `H-g3` on the real records with a tampered bound caught, the dry run never packing a cycle on rung 1's rules, the stage on synthetic instances worked by hand with its two refusals, and the writer refusing unsigned before it measures or writes. **No figure of the plan** |
| `test_ranking.py` | the `PLAN_RANKING.md` instrument: §10's constants with the client imported from rung 2's judge and reasoning off, the three lines read from their records and moving with them, the gate counting every signature line, the twelve presentations and a changed order moving a digest, an injected ticket, rule, queue or omission caught, validity at every edge §0 names, the instrument's arithmetic by hand, one cell of `M-g1` and all of `M-g3` on the real records with a tampered row caught, the dry run computing no rate but the published one and scoring no ranking, every writer refusing unsigned before it builds the client or writes, the smoke and key checks with OpenRouter's endpoint always replaced, Stage B end to end through the double, and Stage C over asks that state Stage C's own ranking. **No figure of the plan** |
| `test_students.py` | the `PLAN_STUDENTS.md` instrument: §3's and §10's constants and §0's lines, the gate counting every signature line, the thin label at its edge, the tree by hand — its splits and their order, growth, the plurality's tie-break, folds grouped by ticket, the pruning sequence and the choice of `k` — and its leaves as valid, disjoint, covering rules the frozen engine executes, the regression's features, gradient, optimum and choice of `λ`, the cache's distance, tie-break and protocol against the frozen file, every mask route against point-by-point prediction, the material and the rules' side on the real records with a tampered figure caught, the stage's second routes on decisions alone and its glue on a synthetic set, the dry run training nothing on the answers by its syntax tree, each verdict at its edge, the writer refusing unsigned, and the students under three values of `PYTHONHASHSEED`. **No figure of the plan** |
| `test_students_readings.py` | `students/readings.py`, the POST-RUN readings `PLAN_STUDENTS.md` left open: the derivation of the two `ONCALL_ESCALATION` leaves' points recomputed by brute force from the hidden policy, the mask of the points an order gets right against `score_order`, a mask by true queue and two predictions deciding alike, each clause of the expectation at its edge, and the writer refusing unsigned before it reads or fits. **No figure of the reading** |
| `test_escalations.py` | the `PLAN_ESCALATIONS.md` instrument: §9's constants, §1's material and §0's lines, the gate counting every signature line, the three selection rules by hand and `selections.py` naming no truth by its syntax tree, the material recomputed and the comparators read off the audit's record, the record's own draw rebuilt, the dry run handing the search no set of escalations but the 286 named by `gates.py`'s syntax tree, each verdict and thin label at its edge, and the writer refusing unsigned before it checks or writes. **No figure of the plan** |
| `test_spotcheck.py` | the `PLAN_SPOTCHECK.md` instrument: §9's constants, §1's material and each draw's make-up and §0's lines, the gate counting every signature line, the nested draws and the two arms by hand, `selections.py` naming no truth in a name or a string, and the literal check catching the subscript a name check misses, the material recomputed and the endpoints as their records hold them, the dry run handing the search no set holding decisions but the whole train half by `gates.py`'s syntax tree, each verdict and thin label at its edge, and the writer refusing unsigned before it checks or writes. **No figure of the plan** |
| `test_spotcheck_readings.py` | `spotcheck/readings.py`, the POST-RUN reading of which tickets teach `T3_ENGINEERING`: first match, the rules' right counts and the key rule by hand with its tie, the move to the front, the two routes of its second gate agreeing on arrival order, each clause of the expectation at its edge, and the writer refusing unsigned before it searches. **No figure of the reading** |
| `test_unreached.py` | the `PLAN_UNREACHED.md` instrument: §9's constants, §1's material, its table of the 25 rules and §0's lines, the gate counting every signature line, the front move, the back move and the coin by hand, reach read off matching, copies as rules written the same, `moves.py` naming no truth in a name or a string, the material, the table, the copies and the curve's reach recomputed, a rule's front move on a toy instance by first match and by masks, the dry run applying no move to a searched order but the published one by `gates.py`'s syntax tree, each verdict and thin label at its edge, a copy counted once, and the writer refusing unsigned before it checks or writes. **No figure of the plan** |
| `test_unreached_keyword_half.py` | `unreached/keyword_half.py`, the POST-RUN reading of what the keyword holds over the space: the rules it names, the material it derives and the expectation's lines, an order's split by the keyword and its copy place and who decides a region on masks by hand, the back move rule by rule summing to the move with no point a reached rule decided moving, a rule's path read as rises, the record's greedy rebuilt as a start and a toy search replayed pass by pass to where the whole search ends, the cells' top and squared deviations exactly, each clause of the expectation at its edge, and the writer refusing unsigned before it searches. **No figure of the reading** |
| `test_manual.py` | the `PLAN_MANUAL.md` instrument: §11's constants with the model and reasoning off imported from `PLAN_REUSE.md` and §0's lines as exact fractions, the gate counting every signature line, the three texts against §5's digests and the rules rebuilt from `HIDDEN_DSL` and parsed back, the catalogue and the prose with an injected leak caught, every prompt its level-0 prompt plus the manual's block and level 0 v1's to the byte, the installer deriving the hidden policy's 199 edges with a reversed list and a refused rule caught, the instrument against `PLAN_REUSE.md`'s published figures, the order of Stage B pinned and rotated, the requests through the SDK double differing from v1's only in the system message, every writer refusing unsigned before it builds a client or writes, a run out of its turn refused, Stage B end to end through the double, and Stage C's verdicts, thin labels and exact comparisons by hand. **No figure of the plan** |
| `test_manual_readings.py` | `manual/readings.py`, the POST-RUN readings of what `PLAN_MANUAL.md`'s Stage C left free: the counts it checks, the translations it names and the expectation's lines, a birth read against its ticket's rule with its crossing nested or partial on masks by hand, a level's pooled summary and the gap split by the classes' mix exactly, a birth's declarations brought back in the answer's order with a record that does not keep them refused, translated edges written into a copy of the record only where the declaration stood, a dropped declaration read against the policy, the rules each translation names and the edges it becomes, the points where two bases decide differently, each clause of the expectation at its edge, and the writer refusing unsigned before it reads a record. **No figure of the reading** |
| `test_manual_after_readings.py` | `manual/after_readings.py`, the POST-RUN reading written after `readings.json`: the names it reads by, a hidden rule cut to the half without the keyword and a birth classed there, a band at its cut, a level split by any partition when runs share rule ids, the mix split over any partition's keys giving back `manual/readings.py`'s over the classes, a condition that admits only tickets without the keyword, the class's arrivals counted by rule, outcome and rightness, and the writer refusing unsigned before it reads a record. **No figure of the reading** |
| `test_manual_notes.py` | `manual/notes.py`, the POST-RUN reading of the proposer's notes: the codebook's fingerprint written a second time, what each code matches and the anchors that keep a pattern inside its word, the cited hidden rules in order and once, the sets split by repetition, a birth narrow at its cut, the split read on the narrow rate, a code's mix exactly and the tickets' mix on its common support, a birth nested in a rule its note cites on masks, a run's rules read with their kind and the rules shown, a level's keyword reading, each clause of the expectation at its edge, and the writer refusing unsigned before it reads a record. **No figure of the reading** |
| `test_apply.py` | the `PLAN_APPLY.md` instrument: §10's constants with the client imported from `PLAN_MANUAL.md` and §0's lines as exact fractions, the gate counting every signature line, the population rebuilt from the twelve loop records with §0's counts and every screen the row's, the ticket names and what each ask serves, nothing in the design carrying a label, the screen arm the escalation's own prompt and the ticket arm case 0's at every level and `PLAN_SCREEN.md`'s at level 0, the digests' teeth, the requests through the SDK double at every level and in both arms, every writer refusing unsigned before it builds a client or writes, a pass refused before its smoke run, Stage B end to end through the double with a resumed session and an outage, no label in what the proposer path reads, and Stage C's terms, clustered error, thin labels and exact lines by hand. **No figure of the plan** |
| `test_apply_providers.py` | `apply/providers.py`, the POST-RUN reading of each `PLAN_APPLY.md` row within one provider's answers: the names it reads by, the provider of an answer as its last attempt's, an arm cut to one provider's answers as `hits` reads it, each row's cut on units built by hand with `X-d`'s selector kept and `X-a` needing the loop's answer, reading B's filter, a cut cell through `adjudicate` with two answers and one read twice reaching alike, the asks two answers at a time, each clause of the expectation at its edge, and the writer refusing unsigned before it reads a record. **No figure of the reading** |
| `test_queue_alone.py` | the `PLAN_QUEUE_ALONE.md` instrument: §10's constants with the client imported from `PLAN_MANUAL.md`, §2.3's pin and §0's lines as exact fractions, the gate counting every signature line, the design built on `PLAN_APPLY.md`'s ticket prompts with the rule arm's ids and digests that plan's and what each prompt serves, §5.1's texts verbatim with v1's block cut from v1 and the sentences and line that part the arms, the requests through the SDK double in every arm with the pin added and nothing else changed, every writer refusing unsigned before it builds a client or writes, a pass refused before its smoke run, Stage B end to end through the double with an answer from another provider invalid, a resumed session, an outage and the smoke check's pin, the 29 rules read from text and §5.6's classes on tickets built by hand, and Stage C's terms, anchor, unadjudicable rows, thin labels and exact lines by hand. **No figure of the plan** |
| `test_queue_alone_orders.py` | `queue_alone/orders.py`, the POST-RUN reading of where the order errors go: the names it reads by and the catch-all as the list's last rule, one answer read against a ticket's matching rules built by hand with the rule it follows, its rank, the runner-up, the catch-all and the most specific rule, an arm's classes, ranks, shares and top three, the specificity reading where the most-conditions rule differs, each clause of the expectation at its edge, and the writer refusing unsigned before it reads a record. **No figure of the reading** |
| `test_first_match.py` | the `PLAN_FIRST_MATCH.md` instrument: §10's constants with the client and the pin imported from `PLAN_QUEUE_ALONE.md`, each arm's reasoning setting and budget, and §0's lines as exact fractions, the gate counting every signature line, the design built on `PLAN_QUEUE_ALONE.md`'s level-3 plain prompts with the plain arm's ids and digests that plan's and the reasoning arm's texts the plain arm's, §5.1's line verbatim and the only thing that parts the naming arm from the plain one, the named rule read from an answer's field, the requests through the SDK double in every arm with the pin and the reasoning setting, a failed call retried with the same messages after a wait and a failed parse with v1's message, every writer refusing unsigned before it builds a client or writes, a pass refused before its smoke run, Stage B end to end through the double with the reasoning and the keys' order kept, an answer from another provider invalid, a resumed session, an outage and the smoke check's reasoning, pin and named rules, and Stage C's terms, the named rules' classes, the anchor, every reason a row has no value, thin labels and exact lines by hand. **No figure of the plan** |
| `test_reasoned_rule.py` | the `PLAN_REASONED_RULE.md` instrument: §10's constants with the client, the pin, both reasoning settings and both budgets imported from `PLAN_FIRST_MATCH.md`, each arm's settings, and §0's lines as exact fractions, the gate counting every signature line, the design built on `PLAN_QUEUE_ALONE.md`'s level-3 rule and plain prompts with their ids and digests that plan's and `PLAN_FIRST_MATCH.md`'s and each reasoning arm's texts its quiet arm's, the requests through the SDK double in every arm with the pin and the reasoning setting, the rule arm's request `PLAN_QUEUE_ALONE.md`'s rule arm's and the plain and reasoning arms' `PLAN_FIRST_MATCH.md`'s, the asker that plan's with a failed call retried with the same messages after a wait and a failed parse with v1's message, every writer refusing unsigned before it builds a client or writes, a pass refused before its smoke run, Stage B end to end through the double with the rule, the reasoning and the keys' order kept, an answer from another provider invalid, a resumed session, an outage and the smoke check's reasoning and pin, the rules written read against a list built by hand over the space with the share always beside the points, and Stage C's terms, `RR-d` held below its line and its condition for having no value, the anchor, every reason a row has no value, thin labels and exact lines by hand. **No figure of the plan** |
| `test_reasoned_loop.py` | the `PLAN_REASONED_LOOP.md` instrument: §11's constants with the client, the pin, the reasoning setting and the budget imported from `PLAN_FIRST_MATCH.md`, §0's lines as exact fractions and its declared figures, the schedule from the seed, the gate counting every signature line, v1b's texts their sources' and the two calls' messages with the draft as the assistant's turn, the requests through the SDK double with the pin and the reasoning setting, the asker that plan's with a failed call retried with the same messages after a wait and a failed parse with v1's message, a call refused for the rate waited out and, through every wait, an outage that stops the run unrecorded (§5.5's amendment), the escalation on engines built by hand: a rule born without a placement, the placement round over `O` in v2b's order, a changed rule, an unplaced one, a citation of the manual's numbers, an order answer, a rule that does not match and a copy born, both triggers and the cap on corpora built by hand, the resumable proposer keeping each answer's keys, reasoning, retries and provider through a resume and nothing of a call refused for the rate, an answer or a failure served from the partial file keeping the seconds the file kept for it and not the replay's (§5.5's second amendment), every writer refusing unsigned before it builds a client or writes, a run refused before Stage A, the smoke run and its turn, the smoke check's pin, reasoning and placement over the attempts that reached the model, and Stage C's terms on runs built by hand: the pace without the calls refused for the rate and without the calls whose record keeps the replay's time, the exact direction beside `blind.rows`', medians of two and three runs, thin labels and every reason a row has no value. **No figure of the plan** |
| `test_reasoned_loop_decided.py` | `reasoned_loop/decided.py`, the POST-RUN reading of what each placed edge decides: the masks the base is read by against the fill's count, one edge reversed by masks against the engine's reinstall, a reversal that would close a cycle, an edge whose pair and point verdicts agree, one where a third rule governs the region its pair verdict is read on and the two part, one that decides nothing, the room's right points no single reversal changes, the readings on rows built by hand, the expectation's clauses at their edges, what was added after the first run: the points a reversal leaves without a rule and the engine's alternative, on a cycle worked by hand, the record on disk coming back, and the writer refusing unsigned before it reads or writes. **No figure of the reading** |
| `test_reasoned_loop_unplaced.py` | `reasoned_loop/unplaced.py`, the POST-RUN reading of where the unplaced answers come from: the codebook's fingerprint written a second time, the reasoning split into sentences in its three languages, a rule's text with the sentence after it, what each code matches and the anchors that keep a pattern inside its word, a negation near a term and a question, the relation to the draft on masks and each cause, a placement round read from a record built by hand with its three gates and their teeth, the readings on rows built by hand split by repetition, the expectation's clauses at their edges, what was added after the first run: each unplaced escalation's signature and the record on disk coming back, and the writer refusing unsigned before it reads or writes. **No figure of the reading** |
| `test_reasoned_loop_governed.py` | `reasoned_loop/governed.py`, the POST-RUN reading of why the error arm's edges sit on regions third rules govern: a ticket's point of the space, a pair's shared region split into what was governed at listing, by the draft's own answer, later and never, on a base worked by hand, a later point given to the birth that completed it with a repair told from another error and from an impasse, governance that never goes back, the replay's final graph the engine's, an error birth whose deciding rule is not in the base, the readings on rows built by hand, the expectation's clauses at their edges, and the writer refusing unsigned before it reads or writes. **No figure of the reading** |
| `test_channel.py` | the `PLAN_CHANNEL.md` instrument: §11's constants with the client, the pin, the reasoning setting, the budget and the protocol imported from `PLAN_REASONED_LOOP.md`, the seeds, §0's lines as exact fractions on their own sides and `DECLARED` against §0's text, the schedule from the seed, the gate counting every signature line, the draws rebuilt from their seed strings, one per case from 0 to 1, no two streams alike, nested across coverages and the same under any `PYTHONHASHSEED`, `reportable` compared exactly, the trigger on its own, the loop on corpora built by hand: coverage 1 that plan's error arm and coverage 0 its impasse arm record for record, at 1/2 a wrong decision escalating by its draw and one not reported standing and firing, the cap, a channel it cannot read refused, the trigger the only reader of the label that decides anything: labels and draws that leave the causes unchanged leave the proposer's calls, its messages and the base unchanged, nothing the trigger reads handed to the proposer, and every comparison with the label on the proposer's path listed, the resume keeping each call's own seconds and refusing a partial file written under other draws, every writer refusing unsigned before it builds a client or writes, a run refused before Stage A, the smoke run and its turn, a Stage A record under other draws refused, the smoke check with the trigger's record, the replay double, the record comparison and a closed verdict's projection on records built by hand, and Stage C's terms: exact lines on both sides, medians of two and three runs, thin labels, every reason a row has no value, the calls without the attempts refused for the rate, and the channel's reports by queue, rule and time. **No figure of the plan** |
| `test_channel_lost.py` | `channel/lost.py`, the POST-RUN reading of why c r1 lost `SECURITY_INCIDENT`, on a base worked by hand: every way a point of the queue is lost, each on a ticket chosen for it — an impasse, a conflict contested or not, unwritten, outranked by an edge or by containment — the ways partitioning the queue's points, an edge between two rules of the queue not counted against it, the winners and the queue's rules with their births, the replay's final base the rebuild's and its curve ending at the base, the escalations' verdicts and gate 4, the expectation's clauses at their edges, the writer refusing unsigned before it reads or writes, and, added after the first run, an unplaced answer's left-out rules by their relation to the draft. **No figure of the reading** |
| `test_channel_oncall.py` | `channel/oncall.py`, the POST-RUN reading of why c r2 recalled less `ONCALL_ESCALATION` than its draws allow, over `channel/lost.py`'s reading: the queue's points split by `H04`'s region and `H05`'s, gate 5 on a split that overlaps or misses a point, each way's points in each part, the rules of the queue holding a part whole, the expectation's clauses at their edges, the writer refusing unsigned before it reads or writes, and, added after the first run, a contested pair with the refused edge between its rules. **No figure of the reading** |
| `test_placement.py` | the `PLAN_PLACEMENT.md` instrument: §11's constants with the client imported from `PLAN_REASONED_LOOP.md` and this plan's pin, the seeds the next two primes after 97, §0's lines as exact fractions, `DECLARED` against §0's text, the schedule, and the gate counting every signature line; v1c's list on bases built by hand, a rule inside the draft and one containing it left out, an equal one kept, a wholly governed one left out, a partly governed one kept, and an empty list sending no call; v1c with both exclusions off giving v1b's record and the loop under v1b `PLAN_CHANNEL.md`'s, on a corpus built by hand; labels and draws that leave the causes unchanged leaving every list, call and base unchanged, nothing the trigger reads handed to the proposer and every comparison with the label listed; the resume with each call's own seconds and the hour it was kept, and a partial file under another protocol or other draws refused; nothing built, asked or written unsigned, the dry runs building no client, and a run refusing before the key without what comes before it; the smoke check with a rule left out; the bridge's tickets and order from their seed strings, under any hash seed; the request `PLAN_REASONED_LOOP.md`'s but for the pin, through the SDK double; Stage C's exact lines, medians, thin labels on medians and on `PL-c`'s count, every reason a row has no value, and `refused(r)`; and an omitted edge deciding nothing on engines built by hand. **No figure of the plan** |
| `test_placement_oncall.py` | `placement/oncall.py`, the POST-RUN reading of why the runs under run 3's draws lost `ONCALL_ESCALATION`, over `channel/oncall.py`'s reading: this plan's Stage C handed to that reader under the key it reads, each draft set against its ticket's part on a record built by hand — one that holds its part, a narrower one, one with no condition, and a ticket of another queue left out — gate 6 on an escalation whose governing rule holds no part, the expectation's clauses at their edges and on either run of the pair, a reading without value, the writer refusing unsigned before it reads or writes, and, added after the first run, the listed rules a ticket matches in order and which of them contain the governing rule's region, the first a cut by would change, a draft cut by it past a containing match and one not cut, the notes with their anchored identifiers, a record read whole, and gate 7. **No figure of the reading** |
| `test_placement_provider.py` | `placement/provider.py`, the POST-RUN reading of whether the cut of the rarest queue's drafts is the provider's, on the bridge, on records built by hand: an answer read as a run's draft — one that holds its part, a cut by the first match a cut changes, one with no condition — with its note's identifiers, gate 1 on a ticket asked twice, not asked of a provider, asked past the first call or not at all, gate 2 on a ticket governed outside the queue or lying first in another rule's region, each ticket's row with both answers, the runs' drafts as `oncall.json` keeps them, gate 3 on points that differ, the drafts counted by ticket, the expectation's clauses at their edges and a reading without value, and the writer refusing unsigned before it reads or writes. **No figure of the reading** |
| `test_placement_cost.py` | `placement/cost.py`, the POST-RUN reading of what the cuts cost, on a list, a base and records built by hand: the listed rules' governed regions partitioning the space and gate 2 on a split that misses a point, the points a base decides right with a conflict left out, a draft classed as a birth is, born or not, and one naming no rule, each class a governing rule falls in and their precedence, a run read whole with each rule's lost points, gate 1 against Stage C's fraction and gate 3, the totals by class and the lost points by queue, the expectation's clauses at their edges with the rarest queue left out of the first, a reading without value, and the writer refusing unsigned before it reads or writes. **No figure of the reading** |
| `test_placement_births.py` | `placement/births.py`, the POST-RUN reading of whether the cut is why the loop's births are narrow, on a list and births built by hand: each class a birth falls in — the wrong queue, whole, cut by one listed rule with the first match a cut changes and the cutting rule's queue, cut by two, and other — gate 1 on a row naming another governing rule, gate 2 on counts that differ from Stage C's, gate 3, the counts, the expectation's clauses at their edges and arm by arm, a reading without value, and the writer refusing unsigned before it reads or writes. **No figure of the reading** |
| `test_whole.py` | the `PLAN_WHOLE.md` instrument: §11's constants with the client and the pin imported from `PLAN_PLACEMENT.md`, the seed the next prime after 103 and no closed thread's, §0's lines as exact fractions on their own sides, `DECLARED` against §0's text, the schedule, and the gate counting every signature line; v1d's paragraph by digest, opening with v2b's first sentence, naming no queue and no rule, and quoted in the plan; v1d's messages v1c's with that one paragraph replaced, on the first call and on the placement call, v2b's text giving v1c's messages back, and a first message that is not v1c's refused; the texts' digests and fingerprints of both arms; v1d's proposer sending v1d's messages through the resumable proposer and v1c's class sending v1c's, a loop on a corpus built by hand giving the same record under both and messages one paragraph apart; the resume with each call's own seconds, and a partial file under the other arm or other draws refused; nothing built, asked or written unsigned, the dry runs building no client, a run refusing before the key without what comes before it, and the turn; the smoke check with v1d's paragraph; the request `PLAN_PLACEMENT.md`'s for both arms, through the SDK double; `whole(r)` on drafts built by hand, with the drafts' breadth; and Stage C's exact lines on every side, medians, `WR-f`'s pairs read by repetition, thin labels and every reason a row has no value. **No figure of the plan** |
| `test_corrections.py` | the `PLAN_CORRECTIONS.md` instrument: the constants with the client and the pin imported from `PLAN_PLACEMENT.md`, level 1, the seed the next prime after 107, §0's lines as exact fractions on their own sides, the schedule, the checkpoints, and the gate counting every signature line without pinning whether the plan is signed; the report by digest, naming one queue and no rule, quoted in the plan; the messages, v1c's with level 3's system prompt and no report, one report apart with it, and one system prompt apart at level 1; **the label's route**, on a corpus built by hand: arm l's proposer handed the reported case's own label at its two calls and nowhere else, arm n's none, and the same record under both; the at-once asks, `PLAN_MANUAL.md`'s level-1 compile messages with no label, the labels read off an L record and refused when they are not its reported errors', the design, the re-asks and the validity flag on an empty object; the learners' plumbing; Stage C's exact lines, medians, thin labels and every reason a row has no value; and nothing built, asked or written unsigned. **No figure of the plan** |
| `test_corrections_forgotten.py` | `corrections/forgotten.py`, the POST-RUN reading of why the final base forgets its corrections, on a run built by hand with six labelled points: one kept, one never born, its report left unplaced, one never right, its correction broader than the rule that erred there, and three taken back, by containment, by an edge and by a conflict; each loss's newborn with its cause, a point arriving again unreported after its loss, the final ways of the forgotten points, why a born report does not leave its point right for each reason, the five gates passing on that run and each failing on its own, a label that is not the reported case's refused, the expectation's clauses at their edges and over nothing, and the writer refusing unsigned before it reads or writes. **No figure of the reading** |
| `test_whole_oncall.py` | `whole/oncall.py`, the POST-RUN reading of why v1d cut at the rarest queue's tickets, over `placement/oncall.py`'s reading of each cut: the codebook's anchored patterns, each matched and each refused where a longer word or another phrase would fool it; the quotes of T1 kept with their windows, one inside the last window not kept again, and at most three a call; the development counts recomputed on the smoke run, which gate 5 reads; a first call on a ticket of the queue read on a record built by hand, with its cut, its added condition, its codes, its note and its placement round, and a ticket of another queue left out; the five gates, each failing on its own; the expectation's clauses at their edges and a reading without value; the writer refusing unsigned before it reads or writes; and, added after the first run, each first call's escalation cause and the queue the base had decided. **No figure of the reading** |
| `test_whole_security.py` | `whole/security.py`, the POST-RUN reading of why every v1c base lost a sixth of `SECURITY_INCIDENT`, over `channel/lost.py`'s reading of the queue: the queue's two parts, `H01`'s and `H02`'s, partitioning its points, and a pair that does not; the rules of the queue holding a part whole on a base built by hand; one part read on that base, its ways partitioning it, the keyword's default deciding what no rule of the queue reaches, and its curve; every first call on a ticket of the queue with its class read off the drafts and the conditions it adds, and a ticket of another queue left out; gate 7 failing on a class or a verdict that is not Stage C's; the losing part and the expectation's clauses at their edges; the writer refusing unsigned before it reads or writes; and, added after the first run, the lost points by tier, severity and product. **No figure of the reading** |
| `test_whole_paragraph.py` | `whole/paragraph.py`, the POST-RUN reading of whether the blind paragraph is why the loop's first call cuts: an answer classed as Stage C classes a first-call draft on a real ticket, the governing rule's region whole, a wrong queue and no rule; a group's share over its right-queue answers and the ticket-weighted share; the five gates, each failing on its own; the expectation's clauses at their edges and a group without value; the record's fractions, and its private keys left out; and the writer refusing unsigned before it reads or writes. **No figure of the reading** |
| `test_halves_hidden.py` | `halves/hidden.py`, the POST-RUN reading of why the hidden half cuts: the codebook's anchored patterns, each matched and each refused where a longer word, another phrase or a distant impasse would fool it; an answer on ticket 1432 read whole and read cut by the first crossing rule, with its note and its declarations; a session's reading keeping only valid answers of the right queue; the development counts recomputed on pass 1, which gate 4 reads; the four gates, each failing on its own; the expectation's clauses at their edges and a clause without value; the record's fractions and `_env`; and the writer refusing unsigned before it reads or writes. **No figure of the reading** |
| `test_ranking_yielding.py` | `ranking/yielding.py`, the POST-RUN reading of which edge of a cycle yields under the model's rankings: the ranking arm with the ranking as an argument, `blind/yielding.py`'s under Stage C's hierarchy and another edge yielding under another, the stated rankings gathered from a session and the median over the asks, the coin's share at or above an arm, the pools, the comparison with a record and its teeth, the expectation's clauses at their edges, and the writer refusing unsigned. **No figure of the plan** |
| `test_writer_lists.py` | that the record-writer table above still mirrors the tree, in both directions, and that every writer hangs its `_env` and only the writers that spend are guarded. It **derives** all of it: the hand lists it replaced under-listed the tree for six days (F1 of the optimizer audit) |
| `test_frontier.py` | the dry-run verification of Step 1 and the memorization floor |
| `test_domain.py` | the corpus: its unique-case count, its duplicate rate and the 8 classes with theirs |
| `test_dsl.py` | the frozen DSL, including the **recorded defect** (CONFLICT is returned before the age tie-break), pinned on purpose |
| `test_shadow.py` | the semantics of the metrics, and that the only escalation trigger is the impasse — never "the answer was incorrect" |
| `test_engine2.py` | bitmasks ≡ `Condition.holds`, and the six verdicts of the edge validator |
| `test_oracle_separation.py` | that no component of the online loop imports the oracle, and that `feedback.py` remains the only module in rung 4 that touches it |
| `test_order_determinism.py` | that the greedy search of rungs 3 and 4 gives the same order under three `PYTHONHASHSEED` values, with a witness confirming that hashing really is randomized |
| `test_proposal_parsing.py` | the parsing of what the proposer returns, in both versions |
| `test_llm_path.py` | the **whole** LLM path, replaying the recorded runs without spending (see below) |
| `test_provenance.py` | the `_env` block, that it does not leak the key, that no JSON writer is left without one, and that the records without one are exactly the thirteen closed by decision, read off the records themselves |
| `test_prose_tables.py` | that a prose table says what the record that owns it says: `STATUS.md`'s scoreboard adds up — totals, the count in its heading, the named lists, the four ratios — and names each row with the verdict its JSON record gives; every FINDINGS' verdict table carries its record's verdicts, thin labels and figures in bold; and every verdict cited in parentheses by the documents that copy them is its record's. It reads tables and row names, never free prose, and each check is shown catching a tampered copy. **No figure is pinned**: it reads both sides |
| `test_record_guard.py` | the guard on the records that cost money: what it refuses, that it aborts **before** spending a call, that the output name no longer collides across `--n`, and that the free records stay unguarded |
| `test_call_record.py` | what a paid call keeps per attempt (generation id, provider, model, both finish reasons, tokens) from a response shaped like OpenRouter's and from the bare double; that the recorder changes no request and no response; that every paid client carries it and every record path keeps it; and that no call site in the tree goes unrecorded without a stated exemption |
| `test_ask_pool.py` | `harness/ask_pool.py`, which asks a session's prompts several at a time. With one worker it writes what `halves/ask.py`'s loop writes, line for line, through the real asker under an SDK double: answers, isolated failures, the breaker, an interrupt and the resume. With several workers it gives the same rows by position, each with its own call's attempts, and never more asks in flight than workers. It also covers the breaker read in the order the asks come back, the drain after a stop, the hold while a worker waits, and that no loop imports it (hard rule 3). **No plan uses it yet** |
| `test_automation.py` | that the hook and the CI workflow are still there and still run what they say they run |

If a *snapshot* test fails, the expected number **is not updated**: you find out
what changed and, if the change is legitimate, you date the erratum in the
corresponding `FINDINGS`. Rungs 3 and 4 are covered by determinism rather than
by snapshot, on purpose: their published figures are those of the code prior to
the tie-break fix and are pending a re-run.

> **[NOTE 2026-10-20] They are no longer pending.** The optimizer audit re-ran
> both rungs, with the tie-break fixed, into new records that carry `_env`
> (August 8 and 13, 2026), and the FINDINGS carry the corrected figures as dated
> errata. The three pre-fix records stay as published, without `_env`, by
> Sergi's decision: *The `_env` block*, below.

### The LLM path, without spending

Of the path that costs money, only the parsing was tested. The rest — building
the request, reading the SDK's response, retrying, validating, inserting the
rule into the base, computing the metrics — is now tested with a **double that
replaces the SDK client, not the proposer**: `OpenRouterProposer` and
`OpenRouterProposer2` run in full and the only thing that does not happen is the
HTTP request.

The responses do not come from a separate script but **from the published record
itself**, so that the replay is the run that produced the figures:

| record | what it reproduces, exactly |
|---|---|
| `results/llm_run.json` | the n=2000 run: every escalation, the rules it produced, the metrics and the raw per-case records |
| `results2/llm_run2_n100.json` | the n=100 run: the same, plus the priority edges with their verdict |

That also yields a figure that is in no record — **what those escalations really
cost in calls**, higher than the escalation count because parse failures are
retried. It lives where it is derived, in the header of
[`tests/doubles.py`](tests/doubles.py), together with the enumeration of which
part of each response is reconstructed verbatim and which part is only the
failure mode: the raw text was never stored.

### Who runs the suite

Nobody has to remember:

```bash
git config core.hooksPath .githooks     # once per clone
```

[`.githooks/pre-commit`](.githooks/pre-commit) runs the suite before every
commit — no venv, no API — and aborts it on failure. It also refuses one shape of
commit before running anything: `PREDICTION.md` or a root `PLAN_*.md` staged
together with any other file. Committing them is not the problem; committing them
*accompanied* is, because a signature that shares a commit with a diagnostic gets
filed under the diagnostic and stops being findable in the log — which is how
Sergi's signature of §0 arrived on 2026-08-13, inside a commit about the
start-budget diagnostic.

The whole hook is skipped with `git commit --no-verify`, guard included, so
"it is only documentation" is no longer the licence it was: what the guard
rejects *is* a documentation commit, and going around it to slip a signature in
accompanied is the one thing the guard exists to stop — there you split the
commit. What survives of that licence is narrower — prose no snapshot covers,
with no plan in the same commit — and it never covers a failing test: the
expected number is not updated and the commit is not forced either.

Which makes the guard a norm and not an enforcement, and it is worth saying
plainly: it catches carelessness — a wildcard in a hurry, the 2026-08-13 case —
and it catches nothing that is trying to get past it, an agent reaching for
`--no-verify` by reflex included. Making it binding would take a server-side
hook or a check in CI, disproportionate for a failure that has happened once and
altered nothing. A guard trusted for more than it can do is worse than no guard.

[`.github/workflows/tests.yml`](.github/workflows/tests.yml) does the same on
every push and every PR — including what was pushed with `--no-verify` — on
**3.10 and 3.12**: the minimum this README declares and the interpreter that
produced the records. And it adds a step the suite cannot do on its own: check,
after running it, that `results*/` is still intact.

**`main` is protected, so changes arrive by pull request.** A GitHub ruleset —
the same one as the rest of the repositories in this account — requires a PR (no
approvals: zero reviewers), forbids force-pushes and deletion, and requires one
status check: **`ci-complete`**. That check is the aggregate job at the end of
the workflow; it depends on the matrix and fails unless every leg succeeded.

**Merge the head CI signed, not the tab you left open.** On 2026-08-13
[PR #7](https://github.com/sergiparpal/adaptive-policy-compilation/pull/7) was
merged with two commits in flight: they did not go in, and for a while `main`
published a Step 3 saying §0 carried no signature when the signature was already
in `main`. **The ruleset cannot catch this and is not meant to** — `ci-complete`
was green on the head that got merged and the required check was satisfied.
Nothing failed; the page was simply older than the branch. It is a race, and the
only thing that catches a race is looking before pressing the button:

```bash
gh pr view <N> --json headRefOid --jq .headRefOid    # what GitHub will merge
git rev-parse origin/<branch>                        # what is on the branch
```

If the two differ, the page is stale: reload it and read the diff again. That
comparison needs both halves, so whoever pushed the branch says which SHA they
pushed, and it is the last line of the report.

The aggregation is the point. Requiring `suite (3.10)` directly would work until
the floor moves, and then the ruleset would be waiting forever for a check that
no longer exists — an unsatisfiable required check blocks every merge without
failing anything. For the same reason the job name is load-bearing: renaming
`ci-complete` without touching the ruleset blocks every merge, in silence. Half
of that decision lives in the repository settings and the other half in the
workflow, so `tests/test_automation.py` pins the half that is versioned.

The actions are pinned to the **full SHA** with their version in a comment
alongside, never to a tag: a tag can be repointed by its owner at other code, a
commit cannot. It is the convention of the rest of the repositories in this
account. To bump one, resolve the new tag to its commit —
`gh api repos/actions/checkout/commits/vX.Y.Z --jq .sha` — and change SHA and
comment together; there is a test that checks they travel together.

Each job carries `timeout-minutes: 10` over a suite that finishes in seconds: it
is not a speed
target, it is what turns a hung job into a failure instead of six hours of
runner. And superseded runs are cancelled… **except on `main`**. Here commits go
straight to `main` and the workflow status is the only record that a given
commit passed the suite; with a plain `cancel-in-progress: true`, pushing three
commits in a row leaves the first two *cancelled* forever — they did not fail,
they simply never got to answer.

And since a pinned SHA **does not age noisily** — it sits still and silent —
[`.github/dependabot.yml`](.github/dependabot.yml) proposes the bump every week.
It watches the actions and **not** `pip`, on purpose: the `openai` pin and the
lock's transitive closure are not an outdated dependency, they are the
provenance of the environment that produced the records, and a weekly PR
proposing to bump them would train the habit of merging without looking.

[`.github/workflows/distiller.yml`](.github/workflows/distiller.yml) runs the
[Distiller](https://github.com/sergiparpal/distiller), pinned to one commit,
**in shadow**. On every push to `main`, once a day and on demand, its
`coverage-at-m` job runs the suite under pytest with per-test coverage and keeps
the data file as the artifact `coverage-at-m-<sha>`. On every PR, its `shadow`
job runs the whole suite under pytest, takes as M the first commit, walking back
from the merge-base, with such an artifact from a run of this repository on the
base branch, runs `distiller evaluate` over both and keeps its record as an
artifact. It blocks nothing: neither job is part of `ci-complete`, and a failing
test never turns it red, because the verdict on the suite is still `tests.yml`'s;
only a failure of its own instrument does. pytest is installed there and nowhere
else, so the suite itself still runs on the standard library. Its floor and the
script that picks M are in [`.github/distiller/`](.github/distiller/).

### The `_env` block

Each results JSON opens with the provenance of the figure:

```json
"_env": {
  "recorded_at": "2026-08-07T14:38:14Z",
  "python": "3.12.3",
  "openai": null,
  "platform": "Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.39",
  "pythonhashseed": null,
  "git_commit": "97cabc1f…",
  "git_dirty": false,
  "code_dirty": false,
  "code_digest": "7ef0ec6d89ec4d85",
  "seed": 17
}
```

`pythonhashseed: null` means **unset**, that is, random: it is information, not
the absence of it — any figure sensitive to the iteration order of a `set`
produced that way is suspect by construction, which is exactly what happened to
the greedy search of rungs 3 and 4. `code_digest` is a sha256 of the code that
produces figures (`harness/`, `rung2..4/`, `run_experiment.py`; the tests are
left out), so it identifies the version even if the tree is dirty or there is no
git.

**The digests recorded before August 19, 2026 cannot be reproduced, and no
figure of theirs changed.** That day the packages `peldano2/`, `peldano3/` and
`peldano4/` were renamed to `rung2/`, `rung3/` and `rung4/`. `code_digest`
hashes each file's relative path along with its content, so renaming the
directories moves every digest without touching a single number: the records
above keep the digest of the layout they were produced under, and re-running any
of them today reproduces its figures and prints a different digest. A digest
mismatch across that date is the rename, not a figure that stopped reproducing;
across any other date it is what it has always been.

**There are two dirty flags and they are not redundant.** `code_dirty` is the
one that decides whether `git_commit` identifies what ran: with `false`, that
commit **is** the code. `git_dirty` covers everything else in the tree, and
everything else is not always harmless — `learned_subsumption`, `compare_runs`
and `note_audit` read records from `results*/` **as input**, so a modified and
uncommitted JSON also breaks traceability without touching a line of code. That
is why the broad flag was not narrowed: it was split in two (August 7, 2026,
while re-running six records back to back and discovering that each script
dirtied the tree for the next one with its own output; see
[`results2/RECORD_NOTES.md`](results2/RECORD_NOTES.md)).

The field appears in each file when that figure is re-run, so carrying it or not
splits the records today into two groups:

| they carry it | still without it, and why |
|---|---|
| `frontier.json`, `subsumption.json`, `learned_subsumption.json`, `ceiling2.json`, `comparison.json`, `note_audit.json` — re-run on August 7, 2026, identical content | `llm_run.json`, `llm_run_n100_smoke.json` and the 8 `llm_run2_*.json` runs: reproducing them **costs money** and they do not come out the same (the proposer is not deterministic at `temperature 0`) |
| | `order_search.json`, `budget_and_balance.json`, `sweep.json`: they are free and deterministic, but re-running them **does move digits** (the tie-break fix) and it is deferred to be done together with the serious optimizer |

Put another way: what is still missing `_env` is exactly what cannot be
reproduced for free or what must not be reproduced yet.

> **[NOTE 2026-10-20] The right-hand column is closed, by Sergi's decision:
> those thirteen records will never carry `_env`, and every other record
> does.** A paid record run again would be another record, not this one with a
> block, and the three free ones run again would move their digits; they are
> kept as published beside the audit's `_ls` records. `tests/test_provenance.py`
> pins the list in both directions. The reasons are in [`IDEAS.md`](IDEAS.md),
> *Technical debt*.

---

## Rung 1

Static world · realizable hidden policy · **pure shadow** (no rule is ever
activated).

The single objective of this rung: **measure the reuse rate and the silent error**
of the rules an LLM writes. Nothing else. If reuse comes out low, the
architecture does not hold up and we stop.

**That objective was not met.** The run was voided by the engine ceiling before
reuse was interpretable, and it still has not been measured cleanly. What was
established is in the four records above.

> **[NOTE 2026-09-30] It has been measured since, on rung 2's engine**, by
> [`PLAN_REUSE.md`](PLAN_REUSE.md): three runs at this rung's horizon, with the two
> error axes kept apart. The rules are reused, and most of their errors are born
> with them. Part of what escalated was still conflict, so the reading carries
> this rung's caveat. The figures are in
> [`results_reuse/FINDINGS_REUSE.md`](results_reuse/FINDINGS_REUSE.md), which owns
> them, and [`STATUS.md`](STATUS.md), which indexes them. None is copied here.

---

## Frozen specification

**Case** — 8 attributes, sampled with a long-tail distribution:

| attribute | domain |
|---|---|
| `has_security_keyword` | bool (3% True) |
| `severity` | 1..4 (1=critical, 5%) |
| `customer_tier` | free / pro / business / enterprise (50/30/15/5) |
| `product` | dashboard / billing / api / mobile / integrations |
| `channel` | portal / email / chat / phone (phone 5%) |
| `prior_tickets_30d` | 0..20, truncated geometric |
| `off_hours` | bool (28%) |
| `language` | en / es / pt / de / fr |

**Actions** — 8 queues: `T1_GENERAL`, `T2_TECHNICAL`, `T3_ENGINEERING`,
`BILLING_SPECIALIST`, `SECURITY_INCIDENT`, `ACCOUNT_MANAGER`,
`ONCALL_ESCALATION`, `SELF_SERVICE_DEFLECT`.

**Hidden policy** — 29 rules prioritized into 8 layers (security overrides →
SLO/on-call → billing → churn risk → product → language/staffing → deflection →
defaults). First match wins. A hierarchical structure with real exceptions, not
independent rules.

**Expressible in the DSL, NOT executable by the engine.** The distinction was
verified on August 5, 2026 and is central to reading everything else:

- **Representation: correct.** Verified exhaustively over the **134,400
  combinations of the case space** that the 29 rules written in the DSL are
  equivalent to their original predicates, and that evaluating them with "first
  match wins" reproduces `true_action` exactly. The DSL loses nothing.
- **Execution: broken.** With those same 29 rules loaded into `RuleEngine` and no
  LLM involved, the engine gets a large fraction of the corpus wrong and declares
  CONFLICT on a quarter of it — the figures are in [`STATUS.md`](STATUS.md) and
  the record is [`results/FINDINGS.md`](results/FINDINGS.md). Specificity-based
  arbitration cannot execute a policy prioritized by layers: in this policy,
  priority and number of conditions are nearly orthogonal.

The "rung 1 condition" (realizable hidden policy) holds at the level of
representation and fails at the level of execution. Reproducible for free with
`python3 -m harness.ceiling_check`.

**Rule schema** — the proposer never emits code:

```json
{"action": "T3_ENGINEERING",
 "conditions": [{"attr": "product", "op": "eq", "value": "api"},
                {"attr": "severity", "op": "lte", "value": 2}],
 "note": "..."}
```

Operators: `eq`, `neq`, `lte`, `gte`, `in`. `lte`/`gte` only over `severity` and
`prior_tickets_30d`.

**Engine** — three outcomes: `ACTION`, `IMPASSE` (coverage), `CONFLICT`
(logical). Conflicts resolved by specificity; a tie with different actions →
escalation.

**Escalation trigger** — *only* a coverage impasse or a conflict. **Never** "the
answer was incorrect". That restriction is what makes the silent error
measurable.

---

## Invariants of the experiment

1. **Oracle separation.** `hidden_policy.py` labels the record. Neither the
   engine nor the proposer ever consults it.
2. **Pure shadow.** No rule is activated. Tickets are independent, so the shadow
   is exact, not an approximation.
3. **The proposer does not touch the base.** It emits a payload; a deterministic
   validator accepts or rejects it.
4. **Fixed corpus.** Seed 17. It is not regenerated between variants.

---

## Step 0 is mandatory and blocking

```bash
python3 -m harness.ceiling_check
```

Loads the true hidden policy into the engine and measures its accuracy with no
LLM involved. If the engine cannot execute the correct policy, no measurement
over learned rules means anything. Until it gives ~100%, any LLM run is voided
in advance — which is what happened to the run of August 5, 2026 (see
[`PREDICTION.md`](PREDICTION.md)).

It costs zero API calls and is re-run after **any** change to the DSL, to the
arbitration or to the hidden policy.

**Part of what that ceiling counts as a conflict is an encoding artifact, and
since 2026-08-29 a control says how much.** The catch-all is `lambda c: True`, the
schema requires at least one condition, so it is written `severity gte 1` and the
engine counts it as specific — it ties with every single-condition layer rule
instead of yielding.

```bash
python3 -m harness.default_rule_control
```

Same ceiling, same criterion, the catch-all at its true rank; both surfaces; and
the published row is a **blocking gate** rather than a row, so it cannot move
quietly. The ranking it uses reads only `DOMAINS` and the rule — no layer order,
no oracle — which is what makes it a control on the encoding rather than a
criterion handed the answer. **It does not lift STOP 0.** Its figures are owned by
[`results/FINDINGS_DEFAULT_RULE.md`](results/FINDINGS_DEFAULT_RULE.md) and indexed
in [`STATUS.md`](STATUS.md).

---

## Getting started (5 minutes)

Requires **Python 3.10+**. Check with `python3 --version`.

Everything that does not call the LLM — the ceilings, `frontier` and rungs 2, 3
and 4 — works **with the standard library alone**. The venv is needed only for
the real proposer.

```bash
git clone https://github.com/sergiparpal/adaptive-policy-compilation.git
cd adaptive-policy-compilation

# 0. MANDATORY, and before anything else: the engine ceiling. 0 API calls.
#    If it does not give ~100%, STOP: nothing that follows will be interpretable.
python3 -m harness.ceiling_check

# 1. Check that everything works WITHOUT spending anything
python3 -m unittest discover
python3 run_experiment.py frontier

# 1b. Make the suite run by itself before every commit. Once per clone.
git config core.hooksPath .githooks

# 2. Virtual environment and SDK installation.
#    CAREFUL: on Debian/Ubuntu a global `pip install` fails with
#    "externally-managed-environment" (PEP 668). The venv avoids it, and it is
#    also in .gitignore, so it does not dirty the repo.
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 3. Key from openrouter.ai -> Keys. It goes in the environment, NEVER in a file
#    in the repo. If you export it in another terminal, the process will not
#    inherit it.
export OPENROUTER_API_KEY=sk-or-...        # Windows: set OPENROUTER_API_KEY=...

# 4. (optional) look up the exact slug of a model
.venv/bin/python run_experiment.py models deepseek

# 5. Smoke test first: see real rules and validate the parsing
#    -> results/llm_run_n100.json
.venv/bin/python run_experiment.py llm --n 100

# 6. Fill in PREDICTION.md, and only then the full run
#    -> results/llm_run_n2000.json. It does NOT touch results/llm_run.json,
#    which is the closed record of rung 1 and the input of rungs 3 and 4.
.venv/bin/python run_experiment.py llm --n 2000
```

**Environment in which the published results were produced:** recorded per file,
in the `_env` block each results JSON has carried since August 7, 2026 — Python,
`openai`, platform and commit, alongside the figure they produced.
`requirements.txt` pins that exact `openai` version and `requirements.lock.txt`
stores the full transitive closure; to rebuild the environment to the digit,
install the lock instead of `requirements.txt`.

**Default provider: OpenRouter.** Default model `deepseek/deepseek-v4-flash`.
Alternatives (all of them need the venv, because they call the LLM):

```bash
.venv/bin/python run_experiment.py llm --model openai/gpt-5.6-luna
.venv/bin/python run_experiment.py llm --model deepseek/deepseek-v4-flash-0731   # pinned revision
.venv/bin/python run_experiment.py llm --provider anthropic --model claude-haiku-4-5-20251001
```

With `--provider anthropic` you would additionally need the `anthropic` package
— which `requirements.txt` leaves commented out — and `ANTHROPIC_API_KEY`
instead of the OpenRouter one.

Having the proposer NOT be Claude is preferable: the harness and the hidden
policy were written by Claude, and it is better for the proposer to come from
another family.

**Cost.** Only escalations cost a call. With V4 Flash at around $0.09/$0.18 per
million tokens and a few hundred escalations at ~1,100 input tokens and ~200
output tokens, the full run costs cents. Verify it with `--n 100`.

**Duration.** The loop is **strictly sequential** and cannot be parallelized:
each new rule changes whether the next case escalates or not. Count on a few
minutes for 2000 cases, not seconds.

**Robustness.** Cheap models return dirty JSON. The parser tolerates markdown
fences, preambles and epilogues; unrecoverable failures are counted in
`failed_proposals` and invalid schemas in `rejected_rules`, without aborting the
run. If those two numbers come out high, the problem is the prompt, not the
architecture.

**Determinism: there is none.** The corpus is deterministic (seed 17), but the
proposer is not, not even at `temperature 0`. Verified on August 5, 2026: same
prompt, same case, same seed, and the rules born from the first cases differ
between the n=100 run and the n=2000 one. Two consequences:

- **the smoke test is not a prefix of the full run** — do not extrapolate from
  one to the other;
- **a comparison between models does not have the model as its only variable**
  unless several sampling seeds are averaged per model.

---

## How to read the frontier

The `keep_k` mocks do not "generalize": **they partition the case space into a
grid** by fixing the k most informative attributes with `eq`. They are therefore
a semantic cache parameterized by granularity — the mandatory baseline, already
included.

The LLM has an advantage the mocks do not have: it can use `lte`, `gte`, `in`
and choose thresholds.

> **[NOTE 2026-10-10] And the mocks have one the LLM does not: they are handed
> the right queue.** `run_shadow` passes every proposer the truth; the mocks
> return it, and the LLM drops it and decides the queue itself, which
> `tests/test_llm_path.py` pins. So the frontier fixes the action and measures
> scope alone — deliberately, as `harness/proposers.py` declares — and the
> semantic cache of `harness/cache_baseline.py` is handed the truth the same way.
> No baseline here competes for the decision with the information the LLM had.
> What that did to the ILP comparison is §5's erratum of
> [`results_ilp/FINDINGS_ILP.md`](results_ilp/FINDINGS_ILP.md).

**The frontier is NOT a region to beat.** It was in the original specification;
the ceiling verification (Step 0) invalidated it as a reference, and the
threshold that used to be set here is withdrawn:

- **The mocks are structurally immune to the engine's defect.** All the rules of
  `keep_k(k)` have exactly k conditions. With uniform specificity, arbitration
  can never invert priorities, and the tie-break falls to `born_at`, which is the
  correct semantics. The hidden policy, by contrast, mixes rules of 1 to 3
  conditions in which the *less* specific rule usually has *more* priority —
  exactly the case arbitration resolves backwards.
- **`keep_k(k=4)` scores better than the true policy under this engine**, on both
  silent error and end-to-end accuracy — the comparison is in
  [`results/FINDINGS.md`](results/FINDINGS.md), route 1. A crude grid beats the
  oracle, and not by being a better policy: by not suffering the priority
  inversions arbitration imposes.

That is: the "region to beat" was **above the ceiling of the system itself**.
Measuring against it would have measured the mock's immunity to the defect, not
the proposer's inductive capacity. No new threshold is set until Step 0 gives
~100%.

The `frontier` figures remain reproducible and serve to check that nothing got
corrupted in copying. They are not usable as a quality reference.

Reference: the majority-class rate is in `results/frontier.json`, next to the
mocks it is there to situate. Hidden policy: 29 rules.

---

## Before running `llm`: fill in PREDICTION.md

This is not ceremony. Without a threshold written in advance, any result is
going to look promising.

---

## What was deliberately NOT here in rung 1

Concept drift, regret against the best representable policy, ILP as a
competitor, empirical impasse detectors, partial feedback, ASP, activation,
versioning, rollback.

Of that list, **partial feedback happened**: rung 4 implemented it as a channel
parameterized by coverage, asymmetry, delay and noise. The rest is still
undone, including **ILP as a competitor**, which was specified as Step B of
rung 3 and never run.

> **[NOTE 2026-10-05] ILP as a competitor has been run since**, on August 30,
> 2026, pre-registered as [`PLAN_ILP.md`](PLAN_ILP.md). Its figures are in
> [`results_ilp/FINDINGS_ILP.md`](results_ilp/FINDINGS_ILP.md), which owns them,
> and [`STATUS.md`](STATUS.md), which indexes them. None is copied here. The
> paragraph above went on saying *never run* for five weeks after.

(Rung 2 added **declared priority**, which was not on this list because in
rung 1 it had not yet been identified as the missing piece.)

Everything open is in [`IDEAS.md`](IDEAS.md), together with what the four rungs
opened and did not resolve.

---

## Repository structure

The modules use relative imports, so **each package must keep its folder**. If
the files end up flat you will see
`ModuleNotFoundError: No module named 'harness'`.

```
adaptive-policy-compilation/
├── run_experiment.py        rung 1 CLI (frontier · llm · models)
├── requirements.txt         `openai` pinned, for the real proposer
├── requirements.lock.txt    transitive closure of the records' environment
├── README.md  CLAUDE.md  IDEAS.md  STATUS.md  LICENSE  .gitignore
├── PREDICTION.md  PLAN_*.md   signed plans — each travels alone in its commit
├── ARBITRATION_REPORT.md    three readings of the records; they own no figure —
├── CHAT_SUMMARY.md          see *Three documents that read the records*, above
├── EXTERNAL_REVIEW.md       the 2026-08-29 review from outside, adjudicated
├── PAIRWISE_WRITEUP.md      the P and B threads as one result; owns no figure
│
├── harness/                 RUNG 1 — frozen spec and original engine
│   ├── domain.py            case, actions, corpus (seed 17)          [FROZEN]
│   ├── hidden_policy.py     the 29 rules in 8 layers · the ORACLE    [FROZEN]
│   ├── dsl.py               rule schema and RuleEngine               [FROZEN]
│   ├── shadow.py            shadow loop and metrics                  [FROZEN]
│   ├── cache_baseline.py    semantic cache baseline                  [FROZEN]
│   ├── proposers.py         keep_k/random_k mocks and LLM proposers
│   ├── provenance.py        the `_env` block attached to every JSON
│   ├── record_guard.py      refusal to overwrite the records that cost money
│   ├── call_record.py       what each paid call says about itself, per attempt
│   ├── ask_pool.py          a session's asks, several at a time; no plan uses it yet
│   ├── ceiling_check.py     STEP 0 · ceiling of the specificity engine
│   ├── default_rule_control.py  the same ceiling with the catch-all at its rank
│   ├── subsumption_check.py partial order by semantic subsumption
│   └── learned_subsumption.py  the same criterion over the learned base
│
├── rung2/                hybrid engine: subsumption + declared priority
│   ├── engine2.py           two-level arbitration
│   ├── hidden_priority.py   the 29 rules with their minimal edges
│   ├── ceiling_check2.py    STEP 0 of rung 2 (gives 100%)
│   ├── ceiling_check2_space.py  the same, over the 134,400 combinations
│   ├── proposers2.py        v1/v2 prompts and bounded neighbourhood
│   ├── shadow2.py  run2.py  compare_runs.py  note_audit.py
│   │                        —— pairwise judgement ——
│   ├── pair_benchmark.py    the 199 labelled pairs, with witnesses
│   ├── pair_judgement.py    the pairwise question · THE ONLY MODULE THAT SPENDS
│   ├── pair_judgement_baselines.py  what the stage C rate is made of
│   └── pair_sample_1600.py  the nested 1,600-pair sample, gated before it spends
│
├── rung3/                order by search over the corpus, no LLM
│   ├── order_search.py      coverage bound, greedy search, split
│   ├── budget_and_balance.py  label budget and balanced greedy
│   │                        —— the audited optimizer ——
│   ├── local_search.py      move/swap, multi-start · the DECLARED optimizer
│   ├── optimizer_check.py   its ceiling, against a known optimum
│   ├── optimizer_check_wt.py  the same for the class-weighted objective
│   ├── order_search_ls.py   rung 3 redone with it
│   ├── budget_and_balance_ls.py  the label curve redone with it
│   │                        —— orders compared AS orders ——
│   ├── order_metrics.py     what an order decides; behavioural distance
│   ├── order_metrics_run.py  regenerates the end orders and gates them
│   ├── order_metrics_corpus.py  the same, over the arrival distribution
│   ├── order_metrics_touched.py  the space restricted to points the corpus hits
│   ├── order_metrics_rules.py  arrival concentration at the rule level
│   ├── rank_transfer.py     joins the space and corpus records
│   ├── territory_holders.py  which rules ever win a case
│   │                        —— pairwise judgement ——
│   ├── floor_by_pool.py     what a no-search order scores, both pools
│   ├── queue_hierarchy_floor.py  what a ranking of the 8 queues alone scores
│   ├── declared_order.py    the three scorings of stage D, and the control
│   ├── edge_direction.py    is the declared direction right, and does it help
│   ├── edge_budget.py       does the channel pay with more edges
│   │                        —— the proposer at 1,600 ——
│   ├── edge_sides.py        what each side of the queue-ranking split buys
│   ├── mfas_compilation.py  the answers or the compilation? same edges, fewer lost
│   ├── edge_dropping.py     does deliberate dropping beat chance
│   ├── answer_asymmetry.py  the a/b asymmetry, and the position effect
│   ├── filter_headroom.py   how much any selection of the edges could have shown
│   ├── filter_space.py      the same selections, scored over the space
│   ├── identical_rules.py   rules written twice, with two queues
│   └── copy_births.py       why rung 1's loop wrote them again
│
├── sensitivity/          A · a family of synthetic manuals, swept by ρ
│   ├── generator.py         counts permuted, bodies drawn from the manual's own
│   ├── measure.py           the evaluation path, both surfaces, both encodings
│   ├── generator_check.py   A-g1..A-g4 · blocking, and it killed the first family
│   └── sweep.py             the five signed rows, gated on PLAN_SENSITIVITY.md
│
├── ilp/                  I · a symbolic inducer, as a competitor with no LLM
│   ├── language.py          the 224 declared conditions
│   ├── instances.py         the four instances and the two training sets
│   ├── induce.py            sequential covering · standard library only
│   ├── asp_encoding.py      the clingo encoding I-g1 killed, kept reproducible
│   ├── induce_check.py      I-g1..I-g4 · blocking
│   ├── compare.py           the four rows, gated on PLAN_ILP.md
│   ├── labels.py            POST-HOC · who had the labels: the proposer chose, the inducer was handed
│   ├── margin.py            POST-RUN · the inducer's margin, split between the test cases it saw labelled and the rest
│   └── chosen.py            POST-RUN · the control: the inducer on the queues the proposer chose
│
├── fidelity/             F · the model re-asked on the cases its rules decided
│   ├── plan.py              the gate and §10's constants; §0's five lines
│   ├── replay.py            a Stage B record rebuilt case by case · F-g2
│   ├── prompts.py           birth, B and ticket-only prompts, rung 2's own
│   ├── sample.py            Stage A · F-g1..F-g3, the draw, the free readout
│   ├── ask.py               Stage B · the calls · spends
│   └── score.py             Stage C · the five rows, gated on PLAN_FIDELITY.md
│
├── screen/               V · the model asked with the ticket alone on decisions its rules made
│   ├── plan.py              the gate and §10's constants; §0's lines
│   ├── sample.py            Stage A · V-g1..V-g3, the populations, the free readout
│   ├── ask.py               Stage B · the calls, each attempt's finish_reason · spends
│   └── score.py             Stage C · V-a to V-d and V-e, gated on PLAN_SCREEN.md
│
├── bound/                H · how much of the residue under the coverage bound is slack
│   ├── plan.py              the gate and §8's constants; §0's lines
│   ├── certificate.py       the argument, the finder, verify, brute force
│   ├── instances.py         the twelve instances and what the records publish
│   ├── gates.py             H-g1..H-g4 · blocking, run before any write
│   └── score.py             the stage · H-a to H-d, the readings of H-e
│
├── ranking/              M · the ranking of the queues, asked of the model
│   ├── plan.py              the gate and §10's constants; three of §0's lines read
│   ├── question.py          the question, the twelve presentations, validity · M-g2
│   ├── instrument.py        the cells, a score, predicts, the revealed ranking
│   ├── gates.py             M-g1..M-g4 · blocking, run before any write
│   ├── sample.py            Stage A · the presentations, the free readout
│   ├── ask.py               Stage B · the calls, each attempt kept · spends
│   ├── score.py             Stage C · M-a to M-e and M-f, gated on PLAN_RANKING.md
│   └── yielding.py          POST-RUN · which edge of a cycle yields, under its rankings
│
├── students/             T · what the proposer's rules buy over a learner fitted to its answers
│   ├── plan.py              the gate and §10's constants; §0's lines
│   ├── material.py          the answers by set, their reach, the truth's route
│   ├── tree.py              the pruned tree, and its leaves as DSL rules
│   ├── logistic.py          the logistic regression, L-BFGS
│   ├── cache.py             the cache's retrieval over the answers, and its masks
│   ├── rules.py             the rules' side: arrival, rung 1's engine, the search, the bases
│   ├── gates.py             T-g1..T-g4 · blocking, run before any write
│   ├── score.py             the stage · T-a to T-e, the readings of T-f
│   └── readings.py          POST-RUN · the three readings the stage left open
│
├── escalations/          J · what a reviewer's labels at the escalations buy the order
│   ├── plan.py              the gate and §9's constants; §1's material and §0's lines
│   ├── selections.py        the 316 escalations and the three rules that choose; no truth
│   ├── instrument.py        the audit's label-budget search, on a given labelled set
│   ├── gates.py             J-g1..J-g4 · blocking, run before any write
│   └── score.py             the stage · J-a to J-e, the readings of J-f
│
├── spotcheck/            N · what a random audit of the decisions buys beside the escalations
│   ├── plan.py              the gate and §9's constants; §1's material, the draws' make-up, §0's lines
│   ├── selections.py        the 689 decisions, the nested draws, the two arms; no truth
│   ├── gates.py             N-g1..N-g4 · blocking, run before any write
│   ├── score.py             the stage · N-a to N-e, the readings of N-f
│   └── readings.py          POST-RUN · which tickets teach T3_ENGINEERING
│
├── unreached/            Z · what the rules no label reaches hold, and what deferring them buys
│   ├── plan.py              the gate and §9's constants; §1's material, the table of the 25, §0's lines
│   ├── moves.py             reach, the front move, the back move, the coin, copies; no truth
│   ├── gates.py             Z-g1..Z-g4 · blocking, run before any write
│   ├── score.py             the stage · Z-a to Z-e, the readings of Z-f
│   └── keyword_half.py      POST-RUN · what the keyword holds over the space
│
├── manual/               G · the policy, given to the proposer at three levels
│   ├── plan.py              the gate and §11's constants; §0's lines as fractions
│   ├── texts/               catalogue.txt, prose.txt, rules.txt · §5, frozen
│   ├── levels.py            the texts and their digests · the proposer's path
│   ├── prompts.py           the loop's prompt and the compile question · the proposer's path
│   ├── compile.py           a compile answer, installed into rung 2 · the proposer's path
│   ├── instrument.py        the scorers of §0, called from rung 2, 3 and the closed threads
│   ├── gates.py             G-g1..G-g4 · blocking; level 3 rebuilt from HIDDEN_DSL
│   ├── sample.py            Stage A · the design and the references
│   ├── ask.py               Stage B1 · the manual compiled once · spends
│   ├── run.py               Stage B2 · the loop with the manual · spends
│   ├── score.py             Stage C · G-a to G-f and G-g, gated on PLAN_MANUAL.md
│   ├── readings.py          POST-RUN · the crossing, level 3's dropped declarations, the class under the prose
│   ├── after_readings.py    POST-RUN, after it · the crossing on K-a's own surface, and the keyword rule by rule
│   └── notes.py             POST-RUN · the proposer's notes, coded on a codebook frozen on the first runs
│
├── apply/                X · the rules applied ticket by ticket, with and without the screen
│   ├── plan.py              the gate and §10's constants; §0's lines as fractions
│   ├── population.py        the decisions and the tickets, rebuilt from PLAN_MANUAL.md's loop records
│   ├── prompts.py           both arms' prompts and the plurality · the proposer's path
│   ├── gates.py             X-g1..X-g4 · blocking
│   ├── sample.py            Stage A · the design and the references
│   ├── ask.py               Stage B · the two passes · spends · the proposer's path
│   ├── score.py             Stage C · X-a to X-f and X-g, gated on PLAN_APPLY.md
│   └── providers.py         POST-RUN · each row within one provider's answers, and the asks two at a time
│
├── queue_alone/          QA · the queue asked alone, with and without a rule to write
│   ├── plan.py              the gate and §10's constants; §2.3's pin; §0's lines as fractions
│   ├── prompts.py           the three arms' prompts, §5.1's texts · the proposer's path
│   ├── population.py        the prompts and the sessions, on PLAN_APPLY.md's population
│   ├── rules.py             the 29 rules read from level 3's text, for QA-g1 and §5.6
│   ├── gates.py             QA-g1..QA-g4 · blocking
│   ├── sample.py            Stage A · the design and the references
│   ├── ask.py               Stage B · the smoke run and the two passes · spends · the proposer's path
│   ├── score.py             Stage C · QA-a to QA-f and QA-g, gated on PLAN_QUEUE_ALONE.md
│   └── orders.py            POST-RUN · where the order errors go: the next matching rule
│
├── first_match/          FM · the first match, asked by name and with reasoning on
│   ├── plan.py              the gate and §10's constants; each arm's settings; §0's lines as fractions
│   ├── prompts.py           the three arms' prompts, §5.1's line, the rule an answer names · the proposer's path
│   ├── population.py        the prompts and the sessions, on PLAN_QUEUE_ALONE.md's level-3 plain prompts
│   ├── gates.py             FM-g1..FM-g4 · blocking
│   ├── sample.py            Stage A · the design and the references
│   ├── ask.py               Stage B · the smoke run and the two passes · spends · the proposer's path
│   └── score.py             Stage C · FM-a to FM-f and FM-g, gated on PLAN_FIRST_MATCH.md
│
├── reasoned_rule/        RR · the rule written with reasoning on
│   ├── plan.py              the gate and §10's constants, imported from first_match/; each arm's settings
│   ├── prompts.py           the four arms' prompts, every one a closed plan's · the proposer's path
│   ├── population.py        the prompts and the sessions, on PLAN_QUEUE_ALONE.md's level-3 prompts
│   ├── gates.py             RR-g1..RR-g4 · blocking
│   ├── sample.py            Stage A · the design and the references
│   ├── ask.py               Stage B · the smoke run and the two passes · spends · the proposer's path
│   ├── shape.py             the rules written, read alone over the space against the list's first match
│   └── score.py             Stage C · RR-a to RR-d and RR-e, gated on PLAN_REASONED_RULE.md
│
├── reasoned_loop/        RL · the loop with reasoning on
│   ├── plan.py              the gate and §11's constants, imported from first_match/; §0's lines
│   ├── protocol.py          v1b's texts and messages, the proposer over first_match/'s asker · the proposer's path
│   ├── loop.py              the loop under both triggers: the blind draft and the placement round · the proposer's path
│   ├── references.py        the transcriber, the hidden policy through v1b's path, the tickets
│   ├── gates.py             RL-g1..RL-g4 · blocking
│   ├── sample.py            Stage A · the references
│   ├── run.py               Stage B · the smoke run and the six runs · spends · resumes · the proposer's path
│   ├── score.py             Stage C · RL-a to RL-g and RL-h, gated on PLAN_REASONED_LOOP.md
│   ├── decided.py           POST-RUN · each placed edge beside the points it decides
│   ├── unplaced.py          POST-RUN · where the unplaced answers come from, on a frozen codebook
│   └── governed.py          POST-RUN · each placed pair's region by when third rules came to govern it
│
├── channel/              CH · half the errors reported
│   ├── plan.py              the gate, §11's constants imported from reasoned_loop/, the draws; §0's lines
│   ├── loop.py              the loop with a coverage, calling reasoned_loop/'s escalation · the proposer's path
│   ├── references.py        the transcriber under every draw and trigger, and the supply table
│   ├── gates.py             CH-g1..CH-g4 · blocking
│   ├── sample.py            Stage A · the references
│   ├── run.py               Stage B · the smoke run and the six runs · spends · resumes · the proposer's path
│   ├── score.py             Stage C · CH-a to CH-f and CH-g, gated on PLAN_CHANNEL.md
│   ├── lost.py              POST-RUN · why c r1 lost SECURITY_INCIDENT: every lost point by what lost it
│   └── oncall.py            POST-RUN · why c r2 recalled less ONCALL_ESCALATION than its draws allow
│
├── placement/            PL · the placement round that lists only what the engine can still order
│   ├── plan.py              the gate, §11's constants, the pins and the draws imported from channel/; §0's lines
│   ├── protocol.py          v1c's list, its round and the pinned asker · the proposer's path
│   ├── loop.py              the loop under either round, at channel/'s coverage · the proposer's path
│   ├── references.py        the drafting reading, the transcriber under every round and draw, the bridge's tickets
│   ├── gates.py             PL-g1..PL-g4 · blocking
│   ├── sample.py            Stage A · the references
│   ├── run.py               Stage B · the smoke run, the bridge and the six runs · spends · resumes · the proposer's path
│   ├── score.py             Stage C · PL-a to PL-f and PL-g, gated on PLAN_PLACEMENT.md
│   ├── oncall.py            POST-RUN · why the runs under run 3's draws lost ONCALL_ESCALATION
│   ├── provider.py          POST-RUN · whether the cut is the provider's: the bridge at the queue's tickets
│   ├── births.py            POST-RUN · whether the cut is why the loop's births are narrow
│   └── cost.py              POST-RUN · what the cuts cost: each base's lost points by what was drafted for their rule
│
├── whole/                WR · a first call that asks for the governing rule's region whole, beside v1c
│   ├── plan.py              the gate, §11's constants, the client and the pin imported from placement/; §0's lines
│   ├── protocol.py          T1, v1d's messages and its proposer · the proposer's path
│   ├── references.py        the drafting reading, whole(r) and the drafts' breadth, the text's relations, the transcriber
│   ├── gates.py             WR-g1..WR-g4 · blocking
│   ├── sample.py            Stage A · the references
│   ├── run.py               Stage B · the smoke run and the six runs · spends · resumes · the proposer's path
│   ├── score.py             Stage C · WR-a to WR-f and WR-g, gated on PLAN_WHOLE.md
│   ├── oncall.py            POST-RUN · why v1d cut at the rarest queue's tickets: each first call's cut, note and reasoning
│   ├── security.py          POST-RUN · why every v1c base lost a sixth of SECURITY_INCIDENT: each way, each part, each first call
│   └── paragraph.py         POST-RUN · whether the blind paragraph is why the first call cuts: the empty base beside the loops, ticket for ticket
│
├── halves/               HV · which half of v2b's base paragraph makes the loop's first call cut
│   ├── plan.py              the gate and the constants: the request, the pin, the tickets, the sessions, the limits, §0's lines
│   ├── prompts.py           the four arms' texts and messages · the proposer's path
│   ├── population.py        the asks and the sessions · the proposer's path
│   ├── gates.py             HV-g1..HV-g4 · blocking
│   ├── sample.py            Stage A · the design and the references
│   ├── ask.py               Stage B · the smoke run, the two passes and the rarest queue's session · spends · resumes · the proposer's path
│   ├── score.py             Stage C · HV-a to HV-f and HV-g, gated on PLAN_HALVES.md
│   └── hidden.py            POST-RUN · why the hidden half cuts: each answer's cut, note, declarations and reasoning codes
│
├── corrections/          CR · the learning regime: a report that carries the true queue, under level 1's catalogue
│   ├── plan.py              the gate, the constants, the draws and §0's declared figures and lines; the client is PLAN_PLACEMENT.md's, pin included
│   ├── protocol.py          the two arms' messages: level 1's system prompt and the report · the proposer's path
│   ├── loop.py              PLAN_PLACEMENT.md's loop with each arm's escalation · the label's one route · the proposer's path
│   ├── prompts.py           the at-once asks' messages and request · the proposer's path
│   ├── gates.py             CR-g1..CR-g4 · blocking
│   ├── sample.py            Stage A · the references
│   ├── run.py               Stage B · the smoke runs and the six runs · spends · resumes · the proposer's path
│   ├── ask.py               Stage B · the at-once sessions, four asks at a time · spends · resumes · the proposer's path
│   ├── learners.py          the inducer at two beams, the three students and the table on the labels, and the control on the proposer's own answers
│   ├── score.py             Stage C · CR-a to CR-f and CR-g, gated on PLAN_CORRECTIONS.md
│   └── forgotten.py         POST-RUN · why the final base forgets its corrections: each labelled point classed, its born reports read, and its last loss
│
├── edges/                W · what the edges declared at write time bought
│   ├── plan.py              the gate and §8's constants; §0's three lines
│   ├── rebuild.py           a Stage B run rebuilt, each edge declared, flipped or absent
│   ├── gates.py             W-g1..W-g4 · blocking, run before any write
│   ├── score.py             the stage · the census, W-a to W-c, W-d
│   └── readings.py          POST-RUN readings of the stage's record
│
├── primacy/              L · where the presentation slot decides the pairwise answers
│   ├── plan.py              the gate and §8's constants; §0's two lines
│   ├── rows.py              §0's definitions and statistics, pure functions
│   ├── gates.py             L-g1..L-g4 · blocking, run before any write
│   └── score.py             the stage · L-a, L-b, the readings of L-c
│
├── why/                  Y · what the proposer says it is doing, against what it does
│   ├── plan.py              the gate, the codebook's fingerprint, the development figures
│   ├── codebook.py          the codebook, frozen on the development set
│   ├── rows.py              the rows and §0's statistics, pure functions
│   ├── gates.py             Y-g1..Y-g4 · blocking, run before any write
│   └── score.py             the stage · Y-a to Y-d, the readings of Y-e
│
├── authorship/           E · declaration imposed at write time, Stage E
│   ├── plan.py              the gate and §11's constants; §0's lines; the fingerprint
│   ├── protocol.py          v1e's texts, the validator, the proposer
│   ├── loop.py              rung 2's loop with v1e's proposal path
│   ├── gates.py             E-g1..E-g3 · blocking, run before any write
│   ├── run.py               Stage B · the three runs · spends
│   ├── score.py             Stage C · E-a to E-d, E-e, gated on PLAN_AUTHORSHIP.md
│   └── refused.py           POST-RUN · the declarations level 1 refused, against the truth
│
├── overlap/              O · Stage E asked again, with the proposer told to overlap
│   ├── plan.py              the gate, §11's constants, §0's lines, the baselines §0 declares
│   ├── protocol.py          v2e's texts, the exempted split, the proposer
│   ├── loop.py              rung 2's loop with v2e's proposal path
│   ├── rows.py              §0's statistics, one instrument for baselines and runs
│   ├── gates.py             O-g1..O-g3 · blocking, run before any write
│   ├── run.py               Stage B · the three runs · spends
│   ├── score.py             Stage C · O-a to O-c, O-d, gated on PLAN_OVERLAP.md
│   ├── readings.py          POST-RUN · what separates the run that overlapped
│   └── readings_v1.py       POST-RUN · the same reading of v1's three bases
│
├── blind/                K · beyond the keyword, with the rule drafted blind
│   ├── plan.py              the gate, §11's constants, §0's lines, the figures §0 declares
│   ├── protocol.py          v2b's texts, the blind screen, the placement, the proposer
│   ├── loop.py              rung 2's loop with v2b's blind path
│   ├── rows.py              §0's statistics, read where the keyword is absent
│   ├── gates.py             K-g1..K-g3 · blocking, run before any write
│   ├── run.py               Stage B · the three runs · spends
│   ├── score.py             Stage C · K-a to K-e, K-f, gated on PLAN_BLIND.md
│   ├── readings.py          POST-RUN · K-d under other directions
│   ├── cycles.py            POST-RUN · why run 1 closed cycles
│   ├── closure.py           POST-RUN · what the transitive order would decide
│   └── yielding.py          POST-RUN · which edge of a cycle should yield
│
├── reuse/                U · the founding question, on rung 2's engine
│   ├── plan.py              the gate and §10's constants; §0's five lines
│   ├── analysis.py          births, the split by birth, F and the gap
│   ├── frontier.py          keep_k through the frozen loop · U-g3
│   ├── gates.py             U-g1..U-g4 · blocking, run before any write
│   ├── readout.py           Stage A · the eight n=100 records
│   ├── run.py               Stage B · rung 2's loop at n=2000 · spends
│   ├── score.py             Stage C · the five rows, gated on PLAN_REUSE.md
│   └── structure.py         POST-RUN · the final bases, read for Stage E
│
├── rung4/                priority learned from a feedback channel
│   ├── feedback.py          the channel; the only one that consults the oracle
│   ├── sweep.py             coverage, asymmetry, delay and noise sweeps
│   └── sweep_ls.py          the same, with the audited optimizer
│
├── tests/                   the suite · `python3 -m unittest discover`
│   ├── fixtures.py          corpus and exhaustive space, built once
│   ├── doubles.py           the recorded SDK client: the LLM path without paying
│   ├── hashseed_child.py    child process for the `PYTHONHASHSEED` control
│   └── test_*.py            invariants and snapshots (see *The tests*)
│
├── .githooks/pre-commit     the suite before every commit (must be enabled)
├── .github/workflows/       tests.yml: the suite on every push and PR, on 3.10 and 3.12
│                            distiller.yml: the Distiller, in shadow, outside ci-complete
├── .github/distiller/       the Distiller's floor and the script that picks M
├── .github/dependabot.yml   bumps the actions; does NOT touch the pip pins
│
└── results/  results2/  results3/  results4/  results_sensitivity/  results_ilp/
    results_reuse/  results_fidelity/  results_edges/  results_primacy/  results_why/
    results_authorship/  results_overlap/  results_blind/  results_screen/
    results_bound/  results_ranking/  results_students/  results_escalations/
    results_spotcheck/  results_unreached/  results_manual/  results_apply/
    results_queue_alone/  results_first_match/  results_reasoned_rule/
    results_reasoned_loop/  results_channel/  results_placement/  results_whole/  results_halves/
    results_corrections/
    The records. FINDINGS*.md are the conclusions with their dated
    errata; the .json files are the raw data, for post-hoc slicing
    without paying for any run again. They are versioned on purpose:
    they are the product of the experiment, not transient output.
```

**`.venv/` is in `.gitignore`** and is rebuilt entirely from
`requirements.txt`. Do not version it: the first commit did, and the history had
to be purged.

The five files marked `[FROZEN]` define the experiment. If you think one of them
has a bug, **stop and say so**; do not fix it on your own. See the hard rules in
[`CLAUDE.md`](CLAUDE.md).
