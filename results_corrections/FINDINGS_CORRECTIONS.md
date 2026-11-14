# The learning regime: a report that carries the true queue, under level 1's catalogue — findings

Record opened on November 14, 2026, under
[`PLAN_CORRECTIONS.md`](../PLAN_CORRECTIONS.md). Sergi signed §0 on 2026-11-12,
before any figure below existed, in a commit of its own: `6908564` on `main`.
- **The plan, its package, the signature, Stage A, the smoke runs, the six runs
  and the five at-once sessions** reached `main` in #239, merged on 2026-11-14.
- **The scorer's correction during Stage C, Stage C, this record, the banner that
  closes the plan and the indexes** reached it in #240, the pull request this
  record was opened in, merged on 2026-11-14.
- **The POST-RUN reading of why the final base forgets its corrections** reached
  it in #242, merged on 2026-11-14.

Every record names in its `_env` the commit it was written from. All but the
last were written on #239's branch, and the last on #240's. The rebase merge
gave each of those commits a new hash on `main`. Each pair has the same subject,
the same tree and the same `git patch-id --stable`: each branch sat on `main`
throughout, so the rebase moved nothing under it.

| record | written from, on #239's branch | the same commit on `main` | code digest | `git_dirty`, `code_dirty` |
|---|---|---|---|---|
| `sample.json` | `443f027`, the signature | `6908564` | `df7fa48670a7e1ca` | false, false |
| `loop_smoke_n.json` | `b29f68f`, Stage A's commit | `177a501` | `df7fa48670a7e1ca` | false, false |
| `loop_smoke_l.json` | `6102b1f`, N's smoke run's commit | `faf10de` | `df7fa48670a7e1ca` | false, false |
| `atonce_smoke.json` | `ae100d7`, L's smoke run's commit | `2adaec6` | `df7fa48670a7e1ca` | false, false |
| `atonce_prior.json` | `57e5534`, the smoke session's commit | `7e2390f` | `df7fa48670a7e1ca` | false, false |
| `loop_l_r1.json` | `39d9142`, the prior session's commit | `d051902` | `df7fa48670a7e1ca` | false, false |
| `atonce_l_r1.json` | `fe891f4`, L r1's commit | `61a7147` | `df7fa48670a7e1ca` | false, false |
| `loop_n_r1.json` | `a407197`, session l_r1's commit | `cdfdde1` | `df7fa48670a7e1ca` | false, false |
| `loop_l_r2.json` | `c51efc3`, N r1's commit | `e8ca733` | `df7fa48670a7e1ca` | false, false |
| `atonce_l_r2.json` | `319383a`, L r2's commit | `7774b77` | `df7fa48670a7e1ca` | false, false |
| `loop_n_r2.json` | `b05aed3`, session l_r2's commit | `8d20907` | `df7fa48670a7e1ca` | false, false |
| `loop_l_r3.json` | `f6bf3f0`, N r2's commit | `d9ddc02` | `df7fa48670a7e1ca` | false, false |
| `atonce_l_r3.json` | `08de8bf`, L r3's commit | `13aa838` | `df7fa48670a7e1ca` | false, false |
| `loop_n_r3.json` | `7ed362d`, session l_r3's commit | `27b5fc9` | `df7fa48670a7e1ca` | false, false |
| `score.json` | `9a157db`, the scorer's correction, on #240's branch | `c36164c` | `fa4f7a8c91feae8c` | false, false |

**`git_dirty` and `code_dirty` are false in every record.** Stage A and Stage B
carry one code digest, `df7fa48670a7e1ca`. The package's code did not change
between the signature and the last run.

**`score.json` carries another digest, because `corrections/score.py` was
corrected during Stage C.**
- **What stopped.** Stage C's first launch, from `7341b62`, stopped in
  `corpus_split`, a reading of `CR-g` that adjudicates nothing. It raised a
  `KeyError` on N r1. That function read each arrival's truth off the record,
  and a run the cap stops keeps rows only for the cases it read: N r1 stopped at
  case 1,276. Its final base still decides all 2,000 arrivals.
- **What it wrote and printed: nothing.** The scorer computes the rows before
  `CR-g`, and prints them only after the record is written. So no verdict and no
  figure of Stage C existed when the function was corrected.
- **The correction**, `c36164c` on `main` (`9a157db` on #240's branch), reads
  every arrival's truth off the corpus labels, `plan.labels()`, the ones the
  trigger reads. It keeps the cases the run read beside the online figure. No
  row's statistic reads that function.
- **`main` computes `score.json`'s digest at `c36164c`**, and still at the merge
  of #240: no later commit of #240 changed code the digest reads.

> **[NOTE 2026-11-14] One more record, written after Stage C by code added
> after it.** [`forgotten.json`](forgotten.json) is the POST-RUN reading of why
> the final base forgets its corrections.
> - **It was written from `f15bcae`**, on the branch of #242, which is `2bf3345`
>   on `main`. Its section below names the commit that carries its expectation.
> - **Its code digest is `3a4358941b384393`**, not Stage C's, because
>   `corrections/forgotten.py` was added after Stage C. `main` computes it at
>   `2bf3345`, and still at the merge of #242. The modules Stage C ran did not
>   change.

**This record owns every figure in it.**

**All three stages ran between 2026-11-12 and 2026-11-14, and the six rows are
adjudicated. `CR-a`, `CR-c` and `CR-d` hold, and `CR-b`, `CR-e` and `CR-f` are
refuted, `CR-e` thinly. `CR-g` is reported.**

- **The label is followed.** L's proposer named the reported queue at every
  first call that named one: 209 of 209, 202 of 202 and 235 of 235 (`CR-a`
  holds).
- **It teaches the two queues the catalogue misses, and not the function.**
  - **On `ACCOUNT_MANAGER` and `T3_ENGINEERING`**, L's median mean recall over
    the space stands 0.3962 above N's: 0.5590 against 0.1628 (`CR-c` holds).
  - **Over the whole space**, L's median base decides 0.5618 and N's 0.5519, a
    gap of 0.0099, under the line of a tenth (`CR-b` refuted).
  - **What L gains on those two queues it loses elsewhere.** On
    `SECURITY_INCIDENT` its bases recall 0.3514, 0.1437 and 0.2976, where N's
    recall 0.925, 1 and 0.6929. On `ONCALL_ESCALATION` they recall 0.4, 0.4476
    and 0.4341, where N's recall 1, 0.7333 and 1. That is reported, under
    `CR-g`.
- **The loop does not keep what it is told.** At the end of each L run, its
  final base decides right 128 of the 252 arrivals that are labelled tickets or
  their repeats, 128 of 249 and 115 of 263. Its base's share of the space peaked
  well before its last label and fell: L r2's from 0.7597 at its 20th label to
  0.4221 at its 209th.
- **Inducing at once from the same corrections decides far more than the loop**
  (`CR-d` holds). The asks at all of a run's labels decided 0.7584, 0.6252 and
  0.7725 of the space at their medians. That is 0.1937, 0.2031 and 0.2106 above
  the loop's own base, run for run.
- **The catalogue alone, compiled at once with reasoning on, decides 0.6451 of
  the space** at the median of its five asks. That is more than any final base of
  either loop, which reached 0.4221 to 0.5785. That is reported.
- **A learner handed the same labels and not the catalogue matches the loop**
  (`CR-e` refuted, thin). The best of them decided 0.4343, 0.4858 and 0.6042 of
  the space. It beat the loop in runs 2 and 3 and lost in run 1, and the median
  difference is −0.0423.
- **The rarest queue was not compiled with its label** (`CR-f` refuted): L's
  median recall of `ONCALL_ESCALATION` is 0.4341.
- **It cost $3.6653 and a day and a half of calls.** §1 expected two to four
  dollars for the six runs and under a dollar for the asks, and three to four
  days. The six runs were billed $3.4345, the at-once sessions $0.2182 and the
  smoke runs $0.0125.
- **The drafter expected `CR-a` to `CR-e` to hold and `CR-f` to be refuted.**
  Four of the six came out so. **Its bet, `CR-d`, held.** The misses are `CR-b`
  and `CR-e`, and both are the loop's: it learned its corrections' queues and
  not the function.

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Its references were
> computed after the signature. §0's four figures had been seen while drafting
> or completing the plan, as §0 says. Zero API calls.
>
> **PROVENANCE, STAGES B AND C: PRE-REGISTERED.** `CR-a` to `CR-f` were signed
> before any of their figures existed, and none of their bands was set on a
> development set. None of them replicates a closed row.
>
> **WHAT WAS SEEN BEFORE STAGE C.** The agent that launched the runs saw,
> before the scorer ran:
> - **Each record's commit message**, which the supervisor wrote from the record.
>   It gives the record's span and launches, the providers that served it, its
>   attempts' finish reasons, the attempts refused for the rate, its failures and
>   its `_env`, and nothing a row reads.
> - **The supervisor's log**: each launch, record, commit and push, with its
>   hour.
> - **The runs' progress lines**, read about every half hour. Each gives the
>   case, the rules, the escalations and the calls asked.
> - **Each run's closing lines**: its rules, escalations, conflicts, failed
>   proposals, rejected rules, calls and cap. Beside them, the label's route
>   check: how many reported errors were handed their own label, or that none
>   was.
> - **Each at-once session's validity**, by checkpoint, and its attempts that
>   reached the budget. No answer was installed and no space computed.
> - **The smoke records and their bills**, before the first run.
> - **L r1's call seconds**, by round, and its reasoning tokens, read on
>   2026-11-13 to answer how long the runs took.
> - **N r1's partial file**, after the outage below: its answers kept, and the
>   case of the last.
> - **Every record's bill**, read by generation id after the last run.
>
> No space, no recall, no followed share, no at-once reading and no learner was
> computed before Stage C. Stage C's first launch printed nothing.

**Each figure names its surface.** Every adjudicated row reads the exhaustive
space of 134,400 points, as `PLAN_PLACEMENT.md`'s rows read it, but `CR-a`, which
reads first calls.
- **A point a base leaves undecided** counts as wrong, for the loop's bases, the
  at-once answers and every learner.
- **The arrivals are in-sample** wherever a label was read, and no row reads
  them. `CR-g` splits them into the labelled tickets, with their repeats, and the
  rest, and gives the online figure beside them.
- **The labelled tickets are points of the space**: 206, 205 and 228 distinct
  ones by L run, under 0.2% of it.

**The two arms differ in one paragraph, at reported errors.** Both ran
`PLAN_PLACEMENT.md`'s v1c at level 1: the catalogue in v1's loop prompt, reasoning
on at high effort, every call pinned to DeepInfra's fp8 endpoint, under
`PLAN_CHANNEL.md`'s channel at coverage 1/2 and its draws. At an escalation
caused by a reported error, L's first call carried, after v2b's paragraph, §5.2's
report: the ticket is not an impasse, the engine decided it, a reviewer marked
the decision wrong, and its true queue is named. N's carried nothing.

---

## Stage A — the checks and the references

**What was run.** `python3 -m corrections.sample`, on 2026-11-12, with
`PYTHONHASHSEED=0`, from the signature on a clean tree. `CR-g1` to `CR-g3` passed,
with the suite green, and `CR-g4` found the plan signed. The record is
[`sample.json`](sample.json).
- **`CR-g1`.** On `PLAN_PLACEMENT.md`'s three v1c runs, both arms with level 3's
  system prompt gave back the runs' records and v1c's messages, at all 479 calls.
  Arm `l`'s messages differed by the report alone, at the 129 reported errors and
  with their labels. At level 1 every call differed by the system prompt alone.
- **`CR-g3`'s instruments.** The inducer handed the whole space decided all of
  it, at both beams. So did the tree handed the whole space, and the 29 hidden
  rules installed as an at-once answer.

**§0's four figures came back as declared**, so §0 needs no erratum:
- the level-3 first calls that named the true queue at reported errors;
- the six v1c runs' escalations, reports and calls;
- the 257 arrivals that repeat an earlier ticket;
- the schedule, l r1, n r1, l r2, n r2, l r3 and n r3.

---

## Stage B — the runs and the asks

**What was run.** Every step was asked through `scratch/`'s supervisor, launched
by the agent as §2.8 let Sergi choose, one at a time and each record committed
alone. The supervisor's file is kept outside the tree.
1. The smoke runs, N then L, and the at-once smoke session, on 2026-11-12. Their
   bills were read before the first run.
2. The prior session and the six runs in §2.3's order, each L run followed by its
   at-once session, from 2026-11-12 to 2026-11-14.

**Every attempt was served by DeepInfra, and none was refused for the rate.** No
call failed. 28 of the runs' attempts ended `length`, cut at the loop's 16,000
tokens, and failed to parse. The asker asked each again, as it asks every
unparsed answer, and every second answer parsed.

| record | from, UTC | to, UTC | hours | launches | calls | attempts | median call | billed |
|---|---|---|---|---|---|---|---|---|
| `loop_smoke_n` | 11-12 22:54 | 11-12 23:02 | 0.13 | 1 | 19 | 19 | 24.1 s | $0.0061 |
| `loop_smoke_l` | 11-12 23:10 | 11-12 23:16 | 0.10 | 1 | 23 | 23 | 17.0 s | $0.0064 |
| `loop_l_r1` | 11-12 23:44 | 11-13 07:55 | 8.17 | 1 | 722 | 726 | 24.3 s | $0.5630 |
| `loop_n_r1` | 11-13 08:39 | 11-13 17:06 | 8.46 | 2 | 783 | 785 | 20.9 s | $0.5631 |
| `loop_l_r2` | 11-13 17:14 | 11-13 22:43 | 5.49 | 1 | 715 | 723 | 17.6 s | $0.5507 |
| `loop_n_r2` | 11-13 23:07 | 11-14 02:56 | 3.82 | 1 | 791 | 794 | 12.4 s | $0.6136 |
| `loop_l_r3` | 11-14 03:04 | 11-14 07:08 | 4.07 | 1 | 686 | 690 | 12.5 s | $0.5202 |
| `loop_n_r3` | 11-14 07:36 | 11-14 12:27 | 4.85 | 1 | 783 | 790 | 14.2 s | $0.6239 |

**N r1 was resumed once.** WSL restarted on 2026-11-13 at 10:24 UTC and took the
supervisor and the run with it. The run's partial file held 228 answers, the last
at case 318, written at 10:22. The supervisor was launched again at 11:48. The
run served the 228 answers from the file, each checked against the request paid
for, and asked the rest. Its span includes the hour and a half between.

**The cap stopped every N run, and no L run.**

| run | escalations | impasses | reported errors | conflicts | stopped at the cap | empty objects |
|---|---|---|---|---|---|---|
| L r1 | 377 | 36 | 216 | 125 | — | 26 |
| N r1 | 400 | 35 | 318 | 47 | case 1,276 | 15 |
| L r2 | 368 | 41 | 209 | 118 | — | 26 |
| N r2 | 400 | 31 | 326 | 43 | case 1,538 | 4 |
| L r3 | 348 | 39 | 235 | 74 | — | 0 |
| N r3 | 400 | 26 | 323 | 51 | case 1,222 | 0 |

- **Every L run handed each reported error its own label, and no other case one.
  No N run handed any.** `corrections/run.py`'s check read each record after it
  was written, and Stage C read every record again.
- **An empty object** is a call DeepInfra answered with `{}`, which the loop
  records as a rule refused as invalid, as §2.6 kept it. Every labelled ticket an
  empty object lost is in the record, and the next report in its region brought
  the label again.

**The at-once sessions asked four at a time, and every ask was valid.**

| session | labels | asks | valid | attempts | at the budget | median ask | billed |
|---|---|---|---|---|---|---|---|
| smoke | 0 and 2 | 2 | 2 | 2 | 0 | 132 s | $0.0037 |
| prior | 0 | 5 | 5 | 5 | 0 | 86 s | $0.0062 |
| l_r1 | 10 to 216 | 18 | 18 | 19 | 1 | 254 s | $0.0702 |
| l_r2 | 10 to 209 | 18 | 18 | 19 | 1 | 89 s | $0.0661 |
| l_r3 | 10 to 235 | 18 | 18 | 20 | 2 | 112 s | $0.0720 |

- **No ask needed a re-ask.** Four attempts ended at the 32,000 tokens of §2.4's
  budget, `length`. The asker asked each again, as it asks every unparsed
  answer, and each second answer was valid.
- **The smoke session met no refusal for the rate at four workers**, so every
  later session ran four at a time, and each record says so.

**What it cost.** $3.6653 in all, for 4,615 attempts, each billed and read by
generation id. The bills are kept outside the tree.
- **The money.** §1 expected two to four dollars for the six runs, and they were
  billed $3.4345. The asks were billed $0.2182, under §1's dollar.
- **The time.** §1 expected three to four days of calls. From L r1's first answer
  to N r3's record took 36.7 hours, the outage included. The calls answered
  faster than `PLAN_WHOLE.md`'s, at medians of 12 to 24 seconds a call.

---

## Stage C — the six adjudications

**What was run.** `python3 -m corrections.score`, on 2026-11-14, with
`PYTHONHASHSEED=0`, from `9a157db` on a clean tree, on #240's branch: `c36164c`
on `main`. `CR-g1` to `CR-g3` passed
again, with the suite green. Nothing was missing: six runs and five sessions. The
record is [`score.json`](score.json).
- **What was checked of every run.** Its base, rebuilt, is the run's. Its calls
  are as recorded, and it handed labels by §4's route alone.
- **This was Stage C's second launch.** The first stopped before writing
  anything, as the record's header says.

**Every statistic is a fraction of counts, compared with its line exactly.** The
record keeps each as a fraction beside its float.

| row | statistic | line | reading | the runs | verdict |
|---|---|---|---|---|---|
| CR-a | the median over L's runs of `followed(r)` | ≥ 0.95 | **1** | 209 of 209, 202 of 202, 235 of 235 | **holds** |
| CR-b | L's median `space(B)`, less N's | ≥ 0.10 | **0.0099**, from 0.5618 and 0.5519 | L 0.5647, 0.4221, 0.5618; N 0.5519, 0.5785, 0.4932 | **refuted** |
| CR-c | L's median `pair(B)`, less N's | ≥ 0.25 | **0.3962**, from 0.5590 and 0.1628 | L 0.5260, 0.5763, 0.5590; N 0.1061, 0.1628, 0.2062 | **holds** |
| CR-d | the median over L's runs of `space(A(r))` less `space(B)` | ≥ 0 | **0.2031** | 0.1937, 0.2031, 0.2106 | **holds** |
| CR-e | the median over L's runs of `space(B)` less `best(r)` | > 0 | **−0.0423** | 0.1304, −0.0637, −0.0423 | **refuted, thin** |
| CR-f | the median over L's runs of `recall_ONCALL_ESCALATION(B)` | ≥ 0.90 | **0.4341** | 0.4, 0.4476, 0.4341 | **refuted** |

`CR-g` is reported, and everything below that is not in the table is its.

**`CR-e` is thin.** Run 1's difference, put in place of the median, would put the
row on the other side of its line. No other verdict is thin: no single run, put
in place of its arm's median, moves `CR-a` to `CR-d` or `CR-f`.

### The two arms, queue by queue

The recall of every queue over the space, by run. The rows of `CR-b`, `CR-c` and
`CR-f` read these bases.

| run | `space` | `T1` | `T2` | `T3` | billing | security | account | on-call | self-service |
|---|---|---|---|---|---|---|---|---|---|
| L r1 | 0.5647 | 0.7193 | 0.8589 | 0.4328 | 0.7127 | 0.3514 | 0.6192 | 0.4 | 0.414 |
| L r2 | 0.4221 | 0.6772 | 0.5809 | 0.7408 | 0.8392 | 0.1437 | 0.4118 | 0.4476 | 0.75 |
| L r3 | 0.5618 | 0.772 | 0.9161 | 0.6797 | 0.5275 | 0.2976 | 0.4383 | 0.4341 | 0.8674 |
| N r1 | 0.5519 | 0.2921 | 0.2605 | 0 | 0.9386 | 0.925 | 0.2123 | 1 | 0.0593 |
| N r2 | 0.5785 | 0.1973 | 0.3133 | 0.2298 | 0.9386 | 1 | 0.0958 | 0.7333 | 0.0756 |
| N r3 | 0.4932 | 0.1849 | 0.3068 | 0 | 0.7602 | 0.6929 | 0.4124 | 1 | 0.1977 |

- **The label moves the queues the catalogue misreads.** L's bases recall `T1`,
  `T2`, `T3` and self-service far more than N's, every run, and
  `ACCOUNT_MANAGER` more in every run, by little in run 3.
- **And L loses the queues the catalogue already holds.** N's bases keep
  `SECURITY_INCIDENT`, `BILLING_SPECIALIST` and `ONCALL_ESCALATION` from the
  catalogue. L's lose most of `SECURITY_INCIDENT`, more than half of
  `ONCALL_ESCALATION`, and some of billing, in every run.
- **So the space does not move** (`CR-b` refuted). Why L's rules take those
  regions is not read here.

### The loop does not keep its corrections

- **Its final base decides about half of its own labelled tickets right.** On the
  arrivals that are labelled tickets or their repeats, L's final bases are right
  on 128 of 252, 128 of 249 and 115 of 263. On the other arrivals they are right
  on 1,402 of 1,748, 1,382 of 1,751 and 1,436 of 1,737.
- **The online figure is not the base's.** Each decision as it was taken counts a
  reported ticket right, because its proposer named the label. L was right online
  on 1,670, 1,675 and 1,733 of 2,000. N was right on 657 of 1,277, 843 of 1,539
  and 620 of 1,223 cases read.
- **N's final bases** are right on 983, 1,031 and 899 of the 2,000 arrivals.
- **L's base rose and fell.** Its share of the space, after the label at each
  checkpoint:

| L run | 10 labels | 20 | 40 | 80 | 160 | all |
|---|---|---|---|---|---|---|
| r1, 216 labels | 0.5241 | 0.5755 | 0.5162 | 0.6539 | 0.6170 | 0.5647 |
| r2, 209 labels | 0.6810 | 0.7597 | 0.7512 | 0.5490 | 0.5116 | 0.4221 |
| r3, 235 labels | 0.3158 | 0.6488 | 0.6338 | 0.5477 | 0.5089 | 0.5618 |

L's runs met more conflicts than N's: 125, 118 and 74 against 47, 43 and 51,
though N's runs read fewer cases before the cap stopped them.

### At once, and the learners, on the same labels

The median of the space over the three at-once asks at each checkpoint, and the
best of the learners trained on the same labels:

| L run | | 10 labels | 20 | 40 | 80 | 160 | all |
|---|---|---|---|---|---|---|---|
| r1 | at once | 0.5944 | 0.6051 | 0.6952 | 0.4760 | 0.7890 | 0.7584 |
| r1 | best learner | 0.1079 | 0.1757 | 0.3058 | 0.3583 | 0.4157 | 0.4343 |
| r2 | at once | 0.5541 | 0.5594 | 0.5250 | 0.3829 | 0.6240 | 0.6252 |
| r2 | best learner | 0.2499 | 0.3587 | 0.3466 | 0.3894 | 0.4278 | 0.4858 |
| r3 | at once | 0.5713 | 0.6051 | 0.4607 | 0.6122 | 0.6928 | 0.7725 |
| r3 | best learner | 0.1732 | 0.2732 | 0.3015 | 0.3344 | 0.4492 | 0.6042 |

- **At all of a run's labels, at once is ahead of the loop by about a fifth of
  the space** in every run (`CR-d` holds). Along the way it was not always
  ahead. It was below the loop's base at 80 labels in run 1, at 10, 20, 40 and 80
  in run 2, and at 20 and 40 in run 3. Every at-once median at 160 labels and at
  all of them is above the loop's.
- **With no label, the catalogue compiled at once decides 0.6451 of the space**,
  the median of its five asks, 0.6171 to 0.6676. Every L run's at-once answer at
  all of its labels is above it in runs 1 and 3, and below it in run 2.
- **The learners grow with the labels, and the loop does not.** At all of a run's
  labels the best was the tree in runs 1 and 2 and the logistic regression in run
  3. The inducer reached 0.3439 to 0.5325, and the cache 0.2695 to 0.3371.
- **The table of tickets decides its labelled points and nothing else**: 206, 205
  and 228 of the space's 134,400.
- **The control on the proposer's own answers.** The students trained on every
  first call of an L run that named a queue, with the label where reported. That
  is 350, 342 and 348 answers. Their best decided 0.5385, 0.4738 and 0.7054 of the
  space, above the loop's own base in runs 2 and 3.

### What the verdicts say

- **The label reaches the proposer and is written** (`CR-a`). What the loop
  writes from it teaches the label's own queues (`CR-c`).
- **The loop does not learn the function from it** (`CR-b` refuted). Its rules
  take regions the catalogue already held, its final base forgets about half of
  its own labelled tickets, and its share of the space peaked well before its
  last label in every run.
- **The same model, handed the same corrections at once, writes a base far better
  than the loop's** (`CR-d`). Handed none, it writes one better than either
  loop's final base.
- **A learner without the catalogue does as well as the loop** on the same labels
  (`CR-e` refuted, thin). So in this regime the loop's model and its catalogue add
  nothing a learner of the labels lacks.
- **The rarest queue stays lost** (`CR-f` refuted). N kept it from the catalogue,
  and L lost about half of it.

### What Stage C does not settle

- **Why L's rules take the regions the catalogue held.** `SECURITY_INCIDENT` and
  `ONCALL_ESCALATION` are lost under L and kept under N. Which rules decide their
  lost points, and from which labels they were drafted, is free on the records.
- **Why the final base forgets its own labelled tickets.** Whether a later rule,
  a declared edge or a refused placement takes each one back is free on the
  records, ticket by ticket.
  **[NOTE 2026-11-14] Read POST-RUN, below.** Mostly none of the three: about
  half the forgotten corrections never decided their own ticket, because a rule
  nested inside them, mostly the one that had erred there, kept it by
  containment. A quarter were never born, mostly unplaced, and a quarter were
  taken back, mostly by an edge. *Why the final base forgets its corrections*.
- **Whether the report or the label does it.** L's paragraph says both, and the
  third arm of §2.2 was not run.
- **Whether at once wins because of the shape or because of the order.** The
  at-once answer is installed in its own list order, and the loop's base is
  ordered by containment and declared edges. No row separates the two.
- **One model, one provider, one manual level, one coverage, one arrival order,
  and three runs an arm.**

## Why the final base forgets its corrections — POST-RUN

**Asked for by Sergi on 2026-11-14, after Stage C.** Stage C found that L's
final bases decide right about half of their own labelled tickets, though the
proposer named the label at every first call that named a queue (`CR-a`).
*What Stage C does not settle* left why: whether a later rule, a declared edge
or a refused placement takes each one back. This reading asks the records, and
spends nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.forgotten`, on
2026-11-14, from `f15bcae` on a clean tree, on the branch of #242, which is
`2bf3345` on `main`.
- **The commits.** `cefaa74` on `main` carries the reading and its expectation,
  written before the reading ran. `2bf3345` carries the part added after the
  first run, which moves no clause. The record was committed alone, as
  `157b509`. On #242's branch they were `c2d180d`, `f15bcae` and `292f8b6`.
- **Each pair has the same subject, the same tree and the same `git patch-id
  --stable`.** The GitHub API names #242 behind the three `main` commits.
- **The record is [`forgotten.json`](forgotten.json).** Its five gates passed in
  all three L runs:
  - the replay is the base;
  - the labels are the record's, as many as Stage C counts;
  - the final base on the labelled arrivals is Stage C's: 128 of 252, 128 of 249
    and 115 of 263;
  - every reading is the engine's;
  - the classes partition the labelled points.

**What it reads.** A *labelled point* is the ticket of a reported error that was
handed its label, counted once however often it arrived. The base is replayed in
birth order, and each labelled point is read right after its first report's
birth, then right after every later birth whose rule matches it. Each point is
in one class:
- **kept**: the final base decides it right;
- **never born**: never right after its report, and no report of it bore a rule;
- **never right**: never right after its report, though a report of it bore a
  rule;
- **taken back**: right after some birth, and wrong at the end.

### 1. Half the forgotten corrections never took their ticket

| L run | labelled points | kept | forgotten | never born | never right | taken back |
|---|---|---|---|---|---|---|
| r1 | 206 | 104 | 102 | 28 | 46 | 28 |
| r2 | 205 | 106 | 99 | 28 | 45 | 26 |
| r3 | 228 | 100 | 128 | 24 | 72 | 32 |

- **The largest class is never right**: 46 of 102, 45 of 99 and 72 of 128
  forgotten points. Their correction was born, and never decided its own ticket.
- **About a quarter were never born**, and about a quarter were taken back.

**Half the corrections born at a report left their own ticket wrong.** Of the
510 reports of the three runs that bore a rule, 262 left their point decided
right just after the birth: 83 of 163, 95 of 158 and 84 of 189.

| L run | born reports | right just after the birth | beaten there by a rule nested inside | in conflict | beaten by an edge |
|---|---|---|---|---|---|
| r1 | 163 | 83 | 63 | 15 | 2 |
| r2 | 158 | 95 | 56 | 3 | 4 |
| r3 | 189 | 84 | 91 | 10 | 4 |

- **Nearly always a rule nested inside the correction kept the ticket**: 210 of
  the 248 born reports left wrong. The correction was broader than a rule
  already matching its ticket, and the engine lets the nested rule win there by
  containment.
- **Usually it was the rule that had erred there.** In 132 of the 210, the rule
  that decided the reported case is among the nested rules that beat the
  correction. In 145 of the 210, more than one nested rule beats it.
- **No side was asked.** v1c's placement round lists only the rules that cross
  the draft. A rule nested inside it is ordered by containment, and is not
  listed.
- **No correction was born outside its own ticket, or for another queue.**

**The corrections that lose are the broad ones.** The born reports, pooled over
the three runs, by the correction's conditions:

| conditions | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| right just after the birth | 1 | 37 | 108 | 80 | 28 | 6 | 2 |
| left wrong | 90 | 83 | 55 | 18 | 2 | 0 | 0 |

- **One correction of one condition in 91 took its ticket**, against 116 of the
  136 with four conditions or more.
- **By points of the space**, the lower median of a correction left wrong is
  13,440, 20,160 and 16,800 points by run. A correction that took its ticket
  has 2,100, 3,360 and 3,360.
- **The rule that erred was mostly another correction.** It had been born at a
  reported error in 37 of 63 nested reports, 41 of 56 and 67 of 91.

### 2. The corrections never born

- **Their reports were mostly unplaced**: 68 of their 82 reports over the three
  runs. 12 were refused as invalid rules and 2 changed the rule in the
  placement round.
- **By run**: 24 unplaced, 4 refused and 2 changed in L r1; 20 unplaced and 8
  refused in L r2; 24 unplaced in L r3.

### 3. The corrections taken back

| L run | taken back | by an edge | by a conflict | by containment | the newborn born at a conflict | at a reported error |
|---|---|---|---|---|---|---|
| r1 | 28 | 15 | 11 | 2 | 18 | 10 |
| r2 | 26 | 23 | 3 | 0 | 15 | 10 |
| r3 | 32 | 23 | 8 | 1 | 15 | 17 |

One newborn of L r2 was born at an impasse.
- **They were taken mostly by an edge**: 61 of 86. A later rule matching the
  point was declared above the rule that decided it. In 53 of the 86 the point's
  own correction was undefeated there before the loss.
- **The takers were born at conflicts more often than births are**: 48 of 86,
  where 216 of the 829 births of the three runs were. A rule born at a conflict
  was written without a label.
- **The points had stood right for hundreds of cases**: lower medians of 355,
  414 and 266 cases between the last gain, or the first report, and the loss.
- **Then they were not seen again.** 83 of the 86 did not arrive again after
  the loss, and of the three that did, one was reported. The channel reports a
  wrong decision only at an arrival.
- **Points kept were lost too.** 22, 14 and 26 kept points were lost at least
  once, and decided right again before the end.

**In the final base**, in `channel/lost.py`'s ways, the 329 forgotten points are
outranked by an edge at 257, in conflict at 49, outranked by containment at 21
and unwritten at 2. In those ways a point is outranked by an edge when any rule
of another queue that matches it beats any rule of its queue there by a declared
edge. So the final ways do not say which defeat decided it: the history above
does.

### The expectation

Written in `corrections/forgotten.py`'s docstring and committed before the
reading ran. It is not signed, and it is on no scoreboard.

| clause | reading | |
|---|---|---|
| F1, never born at least a quarter of the forgotten, each run | 28 of 102, 28 of 99, 24 of 128 | **fails** |
| F2, taken back at least a quarter of the forgotten, each run | 28 of 102, 26 of 99, 32 of 128 | **holds** |
| F3, right just after the birth, at least three quarters of the born reports | 262 of 510, 0.5137 | **fails** |
| F4, at least half the last losses to a newborn deciding alone | 64 of 86, 0.7442 | **holds** |
| F5, the takers born at a reported error at least as often as births are | 0.4302 against 0.6152 | **fails** |
| F6, at least three quarters of the points taken back not seen again | 83 of 86, 0.9651 | **holds** |

- **F2 holds at its line in L r3**, 32 of 128 being a quarter exactly.
- **F1 fails in L r3 alone**, the run with no empty object, as the drafter
  trusted it least.
- **The drafter's account failed where it mattered.** It expected the born
  corrections to take their tickets (`F3`), and the corrections to take each
  other's tickets back (`F5`, the bet). Both fail.

### What it says

- **The loop mostly did not forget its corrections: it never kept them.** About
  half the corrections born at a report did not decide their own ticket. Each
  was drafted broader than a rule already deciding it, mostly the rule that had
  erred there. That rule was mostly an earlier correction. It is nested inside
  the new one, so it keeps the ticket by containment, and the placement round
  never lists it.
- **A quarter of the forgotten points were never compiled**, mostly because the
  placement round left the draft unplaced.
- **A quarter were taken back**, mostly by a rule written at a conflict and
  declared above the rule that decided them. They were not seen again.
- **And nothing checks a correction after its birth.** Most labelled points
  were reported once: 216, 209 and 235 reports over 206, 205 and 228 points.
  The loop takes a born correction as written, whether or not it decides its
  own ticket.

### What it does not settle

1. **Why the first call drafts a correction broader than the rule that erred.**
   It is blind, and told only that the engine decided the ticket and that the
   decision was wrong. Its reasoning is in the records, and is free to read.
2. **Whether a correction checked at its birth would keep its ticket.** A loop
   that lists the rule that decided the reported case, or refuses a correction
   that does not decide its own ticket, is a plan with calls.
3. **Why the rules written at conflicts were placed above the corrections.**
   Their placement answers are in the records, and are free to read.

---

## Files

- [`sample.json`](sample.json): Stage A.
- `loop_smoke_n.json`, `loop_smoke_l.json`: the smoke runs.
- `loop_l_r1.json` to `loop_l_r3.json`, `loop_n_r1.json` to `loop_n_r3.json`: the
  six runs.
- `atonce_smoke.json`, `atonce_prior.json`, `atonce_l_r1.json` to
  `atonce_l_r3.json`: the at-once sessions.
- [`score.json`](score.json): Stage C, the six verdicts and `CR-g`.
- [`forgotten.json`](forgotten.json): POST-RUN, why the final base forgets its
  corrections.
