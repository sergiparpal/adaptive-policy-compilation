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
- **The POST-RUN reading of why the first call writes broad corrections** reached
  it in #244, merged on 2026-11-14.
- **The POST-RUN reading of why the loop's share of the space peaked and fell**
  reached it in #246, merged on 2026-11-14.
- **The POST-RUN reading of why a rule's wins reach the rule it should lose to**
  reached it in #248, merged on 2026-11-14.
- **The POST-RUN reading of why so many rules sit above the gateway** reached
  it in #250, merged on 2026-11-15.
- **The POST-RUN reading of why the doors declared themselves above the
  gateway** reached it in #252, merged on 2026-11-15.
- **The POST-RUN reading of how much of the fall the doors carry** reached it in
  #254, merged on 2026-11-15.

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
>
> **[NOTE 2026-11-14, later] And one more.** [`broad.json`](broad.json) is the
> POST-RUN reading of why the first call writes broad corrections.
> - **It was written from `44ea2c9`**, on the branch of #244, which is `147321b`
>   on `main`: the commit that carries its codebook and its expectation.
> - **Its code digest is `a26162430c936c46`**, because `corrections/broad.py` was
>   added after the reading above. `main` computes it at `147321b`, and still at
>   the merge of #244. The modules Stage C ran did not change.
>
> **[NOTE 2026-11-14, later still] And a third.** [`fall.json`](fall.json) is the
> POST-RUN reading of why the loop's share of the space peaked and fell.
> - **It was written from `a31b396`**, on the branch of #246, which is `1aa3ca0`
>   on `main`: the commit that carries the part added after its first run. Its
>   section below names the commit that carries its expectation.
> - **Its code digest is `c7b7a612cafbf0fb`**, because `corrections/fall.py` was
>   added after the readings above. `main` computes it at `1aa3ca0`, and still
>   at the merge of #246. The modules Stage C ran did not change.
>
> **[NOTE 2026-11-14, last] And a fourth.** [`paths.json`](paths.json) is the
> POST-RUN reading of why a rule's wins reach the rule it should lose to.
> - **It was written from `19201ed`**, on the branch of #248, which is `d58335c`
>   on `main`: the commit that corrects a count of the part added after its
>   first run. Its section below names the commits before it.
> - **Its code digest is `e24481dd56c2b8ba`**, because `corrections/paths.py` was
>   added after the readings above. `main` computes it at `d58335c`, and still
>   at the merge of #248. The modules Stage C ran did not change.
>
> **[NOTE 2026-11-15] And a fifth.** [`gateway.json`](gateway.json) is the
> POST-RUN reading of why so many rules sit above the gateway.
> - **It was written from `bcf20d8`**, on the branch of #250, which is `31a3479`
>   on `main`: the commit that carries the part added after its first run. Its
>   section below names the commit that carries its expectation.
> - **Its code digest is `1757cc92488e3bec`**, because `corrections/gateway.py`
>   was added after the readings above. `main` computes it at `31a3479`, and
>   still at the merge of #250. The modules Stage C ran did not change.
>
> **[NOTE 2026-11-15, later] And a sixth.** [`doors.json`](doors.json) is the
> POST-RUN reading of why the doors declared themselves above the gateway.
> - **It was written from `48900e0`**, on the branch of #252, which is `a46490f`
>   on `main`: the commit that carries the part added after its first run. Its
>   section below names the commit that carries its expectation.
> - **Its code digest is `b4a2acc7fdd0cd3e`**, because `corrections/doors.py`
>   was added after the readings above. `main` computes it at `a46490f`, and
>   still at the merge of #252. The modules Stage C ran did not change.
>
> **[NOTE 2026-11-15, last] And a seventh.** [`carry.json`](carry.json) is the
> POST-RUN reading of how much of the fall the doors carry.
> - **It was written from `f9d3c46`**, on the branch of #254, which is `770931a`
>   on `main`: the commit that carries the part added after its first run. Its
>   section below names the commit that carries its expectation.
> - **Its code digest is `fdf19c791cc3b129`**, because `corrections/carry.py`
>   was added after the readings above. `main` computes it at `770931a`, and
>   still at the merge of #254. Its `_env` says `git_dirty`, for files the
>   session's sandbox mounted in the repository's root, untracked, and
>   `code_dirty` is false. The modules Stage C ran did not change.

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
  **[NOTE 2026-11-14] Read in part POST-RUN, below.** Of the `SECURITY_INCIDENT`
  points L's final bases decide wrongly, 15,390 of 32,690, 41,475 of 43,155 and
  18,600 of 35,400 were right at the run's peak, and are read there with the
  other points lost. In L r1 and L r2 most points lost were left in conflicts. The
  newborn had been declared below a rule of the point's true queue, mostly
  `SECURITY_INCIDENT`'s, and the engine refused the edge for closing a cycle. In
  L r3 most of `SECURITY_INCIDENT`'s went to one correction of `T2_TECHNICAL`,
  nested in the keyword's region. The rest were not right at the peak, and are not
  read. *Why the loop's share of the space peaked and fell*.
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
   **[NOTE 2026-11-14] Read POST-RUN, below.** It writes the queue's general
   rule, which the base mostly holds already, and the report does not make it
   broader. *Why the first call writes broad corrections*.
2. **Whether a correction checked at its birth would keep its ticket.** A loop
   that lists the rule that decided the reported case, or refuses a correction
   that does not decide its own ticket, is a plan with calls.
3. **Why the rules written at conflicts were placed above the corrections.**
   Their placement answers are in the records, and are free to read.

## Why the first call writes broad corrections — POST-RUN

**Asked for by Sergi on 2026-11-14, after the reading above.** It found that
most forgotten corrections never decided their own ticket: a rule nested inside
the correction kept it by containment, and the corrections that lose are the
broad ones. Its *What it does not settle* left why the first call drafts a
correction broader than the rule that erred. This reading asks the records, and
spends nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.broad`, on
2026-11-14, from `44ea2c9` on a clean tree, on the branch of #244, which is
`147321b` on `main`.
- **The commits.** `147321b` on `main` carries the reading's codebook and its
  expectation, written before the reading ran on runs 2 and 3. The record was
  committed alone, as `9c84f6b`. On #244's branch they were `44ea2c9` and
  `7bf3896`. #244 was opened on top of #243 and rebased onto `main` once #243
  merged, which made them `50d70e0` and `93a8b13` before the merge.
- **`44ea2c9`, `50d70e0` and `147321b` have the same subject, the same tree and
  the same `git patch-id --stable`, and so do `7bf3896`, `93a8b13` and
  `9c84f6b`.** `main` after #243's merge had the tree of #243's head, so the
  rebase moved nothing under them. The GitHub API names #244 behind both `main`
  commits.
- **The record is [`broad.json`](broad.json).** Its four gates passed:
  - the reading above's gates pass, and its reading of each born report is the
    one read here;
  - each run's two arms read the same draws;
  - every rule of another queue nested inside a losing correction was left out
    of its round as inside the draft, and none was listed: 101, 73 and 223 of
    them by run;
  - the codebook gives its development counts on run 1.

**What it reads.** Every first call of the six runs. A draft is *valid* when its
conditions build a region, *broad* with one or two conditions and *narrow* with
three or more. A correction *duplicates* a rule when its region equals that of a
rule of the same queue already in the base.
- **Run 1 of each arm is the development set.** The codebook was frozen there,
  and every clause reads runs 2 and 3. The development figures stand in the
  tables beside the held-out ones, marked.
- **The same ticket, with and without the report.** Both arms of a run read the
  same draws, and the first call is blind. So a case that both arms' bases
  decided wrongly, and the channel reported, was asked in messages that differ by
  the report alone (`CR-g1`).

### 1. The report does not widen the draft

| run | reported in both arms | valid pairs | L's draft broader | N's broader | equal | N named the label's queue |
|---|---|---|---|---|---|---|
| r1, development | 91 | 86 | 33 | 50 | 3 | 6 |
| r2 | 82 | 79 | 26 | 46 | 7 | 8 |
| r3 | 99 | 99 | 29 | 62 | 8 | 13 |

- **On the same ticket, the first call without the report wrote the broader
  draft about twice as often.** Of the 163 held-out pairs whose drafts differ in
  points, N's was the broader in 108 and L's in 55.
- **What the report changes is the queue.** N named the label's queue in 21 of
  the 178 held-out pairs. Where both named it, the broader draft was L's in 6
  and N's in 9, and they were equal in 6.

### 2. The losing correction was already in the base

| run | born corrections | left wrong | of them duplicates | duplicates | duplicates left right |
|---|---|---|---|---|---|
| r1, development | 163 | 80 | 42 | 45 | 3 |
| r2 | 158 | 63 | 38 | 46 | 8 |
| r3 | 189 | 105 | 74 | 76 | 2 |

- **Two thirds of the held-out corrections left wrong duplicate a rule of their
  queue**: 112 of 168. The base held that rule already, so the correction added
  nothing.
- **A duplicate does not take its ticket**: 10 of the 122 held-out duplicates
  did.
- **The same correction was written again and again.** In every L run the
  correction born at the most reports was `product = billing ->
  BILLING_SPECIALIST`, one condition: 17 times in r1, 21 in r2 and 33 in r3. It
  took its ticket once.
- **The rule that kept the ticket was never shown.** Each rule of another queue
  nested inside a losing correction was left out of the round as inside the
  draft, as v1c leaves out every nested rule.

### 3. What the reasoning says

Among the first calls at reported errors whose draft is valid:

| run | L's broad drafts | `DEFER` | `ANY` | L's narrow drafts | `DEFER` | `ANY` |
|---|---|---|---|---|---|---|
| r1, development | 76 | 64 | 44 | 133 | 119 | 48 |
| r2 | 71 | 64 | 54 | 131 | 108 | 46 |
| r3 | 102 | 100 | 73 | 133 | 123 | 44 |

- **`DEFER`: the first call leaves the overlaps to the round.** Its reasoning
  takes up that overlapping rules will be listed after the draft in 395 of the
  437 held-out first calls. v2b's paragraph says so.
- **`ANY`: a broad correction is written for any ticket of its kind.** The code
  is in 0.7341 of the held-out broad drafts and 0.3409 of the narrow ones.
- **Both are the prompt's, not the report's.** N's first calls at its reported
  errors carry `DEFER` in 579 of 648 held-out valid drafts, and `ANY` in 167 of
  their 243 broad ones.

### The expectation

Written in `corrections/broad.py`'s docstring and committed before the reading
ran on runs 2 and 3. It is not signed, and it is on no scoreboard.

| clause | runs 2 and 3 | |
|---|---|---|
| B1, L's draft the broader in at most half the differing pairs | 55 of 163 | **holds** |
| B2, at least two fifths of the corrections left wrong duplicate a rule of their queue | 112 of 168 | **holds** |
| B3, at most a fifth of the duplicates take their ticket | 10 of 122 | **holds** |
| B4, `DEFER` in at least three quarters of L's first calls at reported errors | 395 of 437 | **holds** |
| B5, `ANY` at least 0.15 more often among the broad drafts | 0.7341 against 0.3409 | **holds** |
| B6, in each L run the most written correction has one or two conditions and five births or more | 21 and 33 births, one condition | **holds** |

**All six hold, the bet `B2` among them.** Each was drawn from run 1, so each
holding says the reading generalised to runs 2 and 3, not that the drafter
foresaw it.

### What it says

- **The first call writes the queue's general rule.** The system prompt asks
  every call for a generalizable rule for the ticket and its analogous cases,
  and the catalogue gives each queue a general line. Told the true queue, the
  first call writes that line: billing tickets to `BILLING_SPECIALIST`.
- **The report does not make it broad.** Without the report, on the same
  ticket, the first call wrote the broader draft twice as often. What the
  report changes is the queue.
- **The base already holds that rule.** Two thirds of the corrections left
  wrong duplicate it. The same one, billing tickets to `BILLING_SPECIALIST`,
  was written 17, 21 and 33 times.
- **The rule that erred is narrower, of another queue, and inside it.** The
  first call cannot see it. It expects the round to list the overlapping rules,
  and the round leaves every nested rule out. So the narrow wrong rule is never
  shown, and keeps the ticket by the order the system prompt describes: the
  contained rule wins.

### What it does not settle

1. **Whether a first call shown the rule that decided the reported case writes
   a correction that takes its ticket.** A plan with calls.
2. **Whether refusing a duplicate correction, or turning it into a placement
   against the rule that erred, would keep the label.** The loop detects a
   duplicate and bears it anyway. A plan with calls.
3. **Why the narrow rules of another queue were drafted inside the queue's
   general region**, as rules of `SELF_SERVICE_DEFLECT` on billing tickets were
   in run 1. Free on the records.


## Why the loop's share of the space peaked and fell — POST-RUN

**Asked for by Sergi on 2026-11-14, after the two readings above.** Stage C read
L's base after the label at each checkpoint. Its share of the space peaked well
before the last label in every run, and fell, L r2's by a third of the space.
`IDEAS.md` carried why. This reading replays every run's base after every birth,
over the whole space, and spends nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.fall`, on 2026-11-14,
from `a31b396` on a clean tree, on the branch of #246, which is `1aa3ca0` on
`main`.
- **The commits.** `f03b020` on `main` carries the reading and its expectation,
  written before the reading ran. `1aa3ca0` carries the part added after the
  first run, which moves no clause. The record was committed alone, as
  `246c4d4`. On #246's branch they were `67a3f1b`, `a31b396` and `08f56aa`.
- **Each pair has the same subject, the same tree and the same `git patch-id
  --stable`.** The GitHub API names #246 behind the three `main` commits.
- **The record is [`fall.json`](fall.json).** Its five gates passed in all six
  runs:
  - the replay is the base;
  - the curve is Stage C's at every checkpoint, and so is every run's final
    share;
  - every reading is the engine's, at the ends of what each birth changed and at
    every 997th point of the final base;
  - the last losses partition the points lost;
  - the record's order, replayed again, gives the reading's curve and the
    record's refusals.

**What it reads.** Each run's base after every birth, over the space's 134,400
points.
- **The peak** is the first birth after which the most points are right. The
  *points lost* are right at the peak and not right in the final base, and the
  *points gained* the reverse.
- **Each point lost is read at its last loss**, the last birth after the peak
  that took it from right to not right. A newborn takes it alone, by containment
  or by an edge, or leaves it in a *conflict*: undefeated beside a rule of the
  point's true queue, with no edge between them.
- **Arm N is read the same way**, as the control. Both arms of run `k` read the
  same draws.

### 1. The peak, and what fell

| run | births | peak: birth, case, reports before it | share at the peak | final | fall | points lost | points gained |
|---|---|---|---|---|---|---|---|
| L r1 | 282 | 87, case 422, 58 | 0.6896 | 0.5647 | 0.1249 | 28,010 | 11,230 |
| L r2 | 274 | 66, case 309, 34 | 0.7773 | 0.4221 | 0.3553 | 60,845 | 13,095 |
| L r3 | 273 | 81, case 298, 52 | 0.6895 | 0.5618 | 0.1277 | 30,214 | 13,050 |
| N r1 | 322 | 115, case 355, 81 | 0.6004 | 0.5519 | 0.0485 | 11,160 | 4,640 |
| N r2 | 312 | 50, case 138, 32 | 0.6006 | 0.5785 | 0.0221 | 6,340 | 3,375 |
| N r3 | 331 | 295, case 1,095, 284 | 0.6275 | 0.4932 | 0.1343 | 20,615 | 2,560 |

- **Read after every birth, L's peaks stand above Stage C's checkpoints**:
  0.6896, 0.7773 and 0.6895, where the checkpoints showed 0.6539, 0.7597 and
  0.6488. They came after 58, 34 and 52 of the runs' 216, 209 and 235 labels.
- **What fell was mostly `SECURITY_INCIDENT`'s** (Q1 holds): 15,390 of L r1's
  28,010 points lost, 41,475 of L r2's 60,845 and 18,600 of L r3's 30,214. The
  points gained were spread over the other queues.
- **N fell less than L in two pairs and more in one** (Q6 fails). N r3 fell
  0.1343 of the space, where L r3 fell 0.1277.
  - **N r3's peak came late**, at birth 295 of 331, and eight births took all it
    lost.
  - **Two of them took most.** An `ONCALL_ESCALATION` rule, `severity = 1 ∧
    off_hours = true`, was declared above 74 rules and below none. It took 8,400
    points, all `SECURITY_INCIDENT`'s, by edges. An `ACCOUNT_MANAGER` rule,
    `customer_tier = business ∧ prior_tickets_30d ≥ 5 ∧ severity ≥ 3`, took
    8,045, most of them `SECURITY_INCIDENT`'s, and left most in conflicts.
  - **Neither was drafted from a label**: N's proposer is never handed one.

### 2. How it fell

| run | points lost | `SECURITY_INCIDENT`'s | by containment | by an edge | a conflict |
|---|---|---|---|---|---|
| L r1 | 28,010 | 15,390 | 995 | 5,195 | 21,820 |
| L r2 | 60,845 | 41,475 | 7,370 | 8,655 | 44,820 |
| L r3 | 30,214 | 18,600 | 16,315 | 6,747 | 7,152 |
| N r1 | 11,160 | 3,780 | 75 | 5,135 | 5,950 |
| N r2 | 6,340 | 0 | 370 | 5,525 | 445 |
| N r3 | 20,615 | 15,480 | 0 | 10,635 | 9,980 |

- **Most of the points lost were left in a conflict, not taken** (Q2 fails).
  Over the three L runs, 45,277 of 119,069 were taken by a newborn alone. In L r1
  and L r2 the conflicts held 21,820 of 28,010 and 44,820 of 60,845.
- **In L r3 one correction took most, by containment.** `has_security_keyword =
  true ∧ severity ≠ 1 → T2_TECHNICAL` was born at a reported ticket of `H03`, a
  security mention on a small account at low severity. It dropped the tier, its
  severity reached past `H03`'s, and it took 15,960 points of
  `SECURITY_INCIDENT`. In L r2, `has_security_keyword = true ∧ severity ≥ 3 →
  T2_TECHNICAL`, born at a ticket of `H03` too, took 7,240 the same way.
- **Rules of `T2_TECHNICAL` took half of the `SECURITY_INCIDENT` points lost**
  (Q4 holds, the bet): 39,865 of 75,465. It holds on L r3's one rule. By run they
  took 4,790 of 15,390, 19,115 of 41,475 and 15,960 of 18,600, and without L r3
  the share is 0.4204, under the line.
- **The corrections took their share, and no more** (Q3 fails, by 0.0063). They
  took 0.6441 of the points lost, and were 0.6504 of the births after the peaks.
  In L r2, rules born at conflicts took more than the corrections: 32,025 of
  60,845.
- **A few births took most** (Q5 holds). The ten that took the most took 20,465
  of L r1's 28,010 points lost, 41,765 of L r2's 60,845 and 23,796 of L r3's
  30,214.

### 3. Why the conflicts — added after the first run

| run | conflict points | pairs below, refused | pairs above, refused | points where every pair is below, refused |
|---|---|---|---|---|
| L r1 | 21,820 | 79,155 | 5,250 | 18,790 |
| L r2 | 44,820 | 136,505 | 9,455 | 39,250 |
| L r3 | 7,152 | 4,881 | 3,720 | 4,641 |
| N r1 | 5,950 | 555 | 5,615 | 555 |
| N r2 | 445 | 180 | 375 | 80 |
| N r3 | 9,980 | 99,205 | 2,935 | 8,045 |

A pair is a rule undefeated beside the newborn at a point lost by a conflict,
weighed by the points it stands on.

- **Every pair was an edge refused for closing a cycle.** No rule beside a
  newborn went unlisted, was left without a side, or was cited from outside the
  round.
- **In L r1 and L r2 the refused side was mostly the right one.**
  - **The newborn had been declared below the rule of the point's true queue**,
    and that edge was refused.
  - **That rule was mostly `SECURITY_INCIDENT`'s**: on 70,270 of L r1's 84,405
    pair-points, and 131,060 of L r2's 145,960.
  - **At 18,790 of L r1's 21,820 conflict points**, and 39,250 of L r2's 44,820,
    every pair was such a right side, refused.
- **The newborn's own wins closed the cycle.** The loop installs a born rule's
  declarations as v1 does, its wins before its losses.
  - **Nearly every right side refused** in L r1 and L r2 met a cycle that the
    same answer's wins, installed first, had closed. The base had closed it
    before them on 20 of L r1's 79,155 pair-points, and on none of L r2's.
  - **Each win refused** met a cycle the base had closed, as a win must, since
    the wins are tried before the losses.
- **N r3's conflicts came the same way.** 99,205 of its 102,140 pair-points
  were right sides refused, and 98,240 stood on `SECURITY_INCIDENT`'s rules.

**The same births, each birth's losses tried before its wins:**

| run | the record's order: final | fall | `SECURITY_INCIDENT` recall | losses first: final | fall | `SECURITY_INCIDENT` recall |
|---|---|---|---|---|---|---|
| L r1 | 0.5647 | 0.1249 | 0.3514 | 0.7374 | 0.0411 | 0.8333 |
| L r2 | 0.4221 | 0.3553 | 0.1437 | 0.6539 | 0.1331 | 0.6667 |
| L r3 | 0.5618 | 0.1277 | 0.2976 | 0.5678 | 0.1289 | 0.3095 |
| N r1 | 0.5519 | 0.0485 | 0.9250 | 0.5435 | 0.0482 | 0.9250 |
| N r2 | 0.5785 | 0.0221 | 1.0000 | 0.5664 | 0.0248 | 1.0000 |
| N r3 | 0.4932 | 0.1343 | 0.6929 | 0.5459 | 0.0777 | 0.8333 |

- **Losses first, the same declarations keep most of what L r1 and L r2 lost.**
  - **L r1 ends at 0.7374 of the space, and L r2 at 0.6539**, where the record's
    order ends them at 0.5647 and 0.4221.
  - **`SECURITY_INCIDENT`'s recall rises** from 0.3514 to 0.8333, and from
    0.1437 to 0.6667.
  - **L r3, whose fall was taken by containment, barely moves**: from 0.5618 to
    0.5678.
  - **N r3 rises** from 0.4932 to 0.5459. N r1 and N r2 lose 0.0084 and 0.0121.
- **It is not the loop that would have run.** A base installed in another order
  decides the arrivals otherwise, and would have escalated other cases. What it
  shows is what the same births and the same declarations decide in the other
  order.

### The expectation

Written in `corrections/fall.py`'s docstring and committed before the reading
ran. It is not signed, and it is on no scoreboard.

| clause | reading | |
|---|---|---|
| Q1, in each L run at least half of the points lost are `SECURITY_INCIDENT`'s | 0.5494, 0.6817 and 0.6156 | **holds** |
| Q2, at least half of the points lost were taken by a newborn alone | 45,277 of 119,069 | fails |
| Q3, the corrections' share of the points lost at least their share of the births after the peaks | 0.6441 against 0.6504 | fails |
| Q4, at least half of the `SECURITY_INCIDENT` points lost went to rules of `T2_TECHNICAL` | 39,865 of 75,465 | **holds** |
| Q5, in each L run the ten largest takers took at least half of the points lost | 0.7306, 0.6864 and 0.7876 | **holds** |
| Q6, in each pair of runs N's fall smaller than L's | r3: 0.1343 against 0.1277 | fails |

**Q1, Q4 and Q5 hold, and Q2, Q3 and Q6 fail.** The bet `Q4` held on one rule of
L r3, and `Q3` failed by 0.0063.

### What it says

- **The share falls in the keyword half.** Rules of other queues reach into
  `SECURITY_INCIDENT`'s region. Rules written without the keyword cross its
  rules, and corrections at tickets of `H03` nest inside them.
- **In L r1 and L r2, mostly the proposer placed them right, and the engine
  refused the side.** A rule's answer declares it above some rules and below
  others.
  - **The loop installs the wins first**, and through them the rule already
    reaches the one it should lose to. So that loss closes a cycle, and is
    refused.
  - **The pair is left unordered, and its region in conflict.**
- **Installed losses first, the same answers keep most of the region**, in L r1
  and L r2. Where a correction took the region by containment, as in L r3, no
  order of the edges changes it.
- **The label is not needed for it.** N r3 lost a share as large to rules its
  proposer drafted without one. About half went to conflicts that came the same
  way, and 8,400 points to one rule of `ONCALL_ESCALATION` declared above 74
  rules and below none.

### What it does not settle

1. **Whether a loop that installs a rule's losses before its wins keeps its
   share.** The replay in that order keeps the same births, and a loop would
   have escalated other cases. A plan with calls.
2. **Why a rule's wins reach the rule it should lose to.** The reading does not
   trace the cycles' paths. They may run through rules wrongly above
   `SECURITY_INCIDENT`'s, or through rules that do not match the contested
   points. Free on the records.
   **[NOTE 2026-11-14] Read POST-RUN, below: through rules that miss every
   point the pair shares.** They enter `SECURITY_INCIDENT`'s rule through a rule
   nested inside it, born at a reported ticket of `H03`, which the policy's
   verdict calls even. *Why a rule's wins reach the rule it should lose to*.
3. **Whether this is the order Stage C left open.** In L r1 and L r2 the same
   declarations, installed losses first, come within 0.03 of the at-once answers
   at all of their labels, 0.7584 and 0.6252. In L r3 they do not. The at-once
   answer is other rules, installed in their own list order, so the two are not
   separated.


## Why a rule's wins reach the rule it should lose to — POST-RUN

**Asked for by Sergi on 2026-11-14, after the reading above.** It found the
share lost mostly at conflicts, where the engine had refused the right side for
closing a cycle that the newborn's own wins had closed. Its *What it does not
settle*, item 2, left why those wins reach the rule the newborn should lose to:
through rules wrongly above `SECURITY_INCIDENT`'s, or through rules that do not
match the contested points. This reading asks the records, and spends nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.paths`, on
2026-11-14, from `19201ed` on a clean tree, on the branch of #248, which is
`d58335c` on `main`.
- **The commits.** `5c1ac9c` on `main` carries the reading and its expectation,
  written before the reading ran. `63a44d1` carries the part added after the
  first run, which moves no clause.
- **`d58335c` corrects a count of that part.** Its list of the rules above the
  even crossings had added a pair's points once per crossing, and so gave one rule
  more points than its pairs held. The first run's record was not committed, and
  no clause reads the list.
- **The record was committed alone**, as `b1b68e6`. On #248's branch the four
  commits were `f17fb2d`, `5769c4b`, `19201ed` and `c80cd5d`. Each pair has the
  same subject, the same tree and the same `git patch-id --stable`, and the
  GitHub API names #248 behind the four `main` commits.
- **The record is [`paths.json`](paths.json).** Its six gates passed in all six
  runs:
  - the replay is the base;
  - the pairs are `fall.json`'s: in every run their points sum to `beside`'s
    below_refused;
  - every refusal is the engine's;
  - no path touches the pair's points;
  - the classes partition the pairs' points;
  - the engine that refuses only where the cycle is leaves no point without a
    rule undefeated, and decides as its masks do.

**What it reads.** Every right side that `corrections/fall.py`'s `beside` classed
below_refused. At a point lost by a conflict, the newborn `n` had been declared
below `u`, a rule of the point's true queue, and the edge was refused for
closing a cycle. Each pair is read right after `n`'s birth, and weighed by its
points.
- **The paths** are the chains of what beats what from `n` to `u`.
  - **A crossing** is a step from a rule of another queue to a rule of `u`'s
    queue: nested inside it, or declared above it.
  - **The policy's verdict on a crossing** reads the points both of its rules
    match. It is *wrong* when more are `u`'s queue's, *right* when fewer, and
    *even* when as many.
- **A pair is in one of three classes.** It is *wrong_declared* when no path is
  left once the wrong declared crossings are taken out, and *wrong_nested* when
  none is left once the wrong nested ones go too. Otherwise it is *right*.
- **The cycle is never at the pair's points.** `u` is undefeated there, so no
  rule that beats it matches them (gate 4). So the reading asks whether the cycle
  is *somewhere* in the pair's shared region, through rules that all match one of
  its points, or *nowhere*.

### 1. The cycle is nowhere the pair decides

| run | pairs | points | wrong_declared | wrong_nested | right | somewhere | nowhere |
|---|---|---|---|---|---|---|---|
| L r1 | 94 | 79,155 | 25 | 530 | 78,600 | 14,975 | 64,180 |
| L r2 | 134 | 136,505 | 1,935 | 0 | 134,570 | 3,925 | 132,580 |
| L r3 | 19 | 4,881 | 1,621 | 0 | 3,260 | 2,900 | 1,981 |
| N r1 | 2 | 555 | 0 | 75 | 480 | 555 | 0 |
| N r2 | 5 | 180 | 0 | 60 | 120 | 160 | 20 |
| N r3 | 32 | 99,205 | 100 | 0 | 99,105 | 5,620 | 93,585 |

- **The paths need no wrong crossing** (K1 fails). Over L's runs, 4,111 of the
  220,541 pair-points are in pairs a wrong crossing carries, and 3,581 of those
  need a wrong declared one (K2 holds).
- **The cycle is nowhere in the pair's shared region** (K4 fails, the bet). Over
  L's runs, 21,800 of the 220,541 pair-points are in pairs whose cycle runs
  through rules that all match some point both rules of the pair match. For the
  rest, every path runs through a rule that misses every point either rule of
  the pair decides.
- **The paths are long.**
  - **The shortest path** has three or four steps on most of L r1's pair-points,
    four to six on L r2's, and five on N r3's.
  - **The paths' rules touch few of the pair's points**: 290 of L r1's 79,155,
    430 of L r2's 136,505 and 13,280 of N r3's 99,205.
- **The corrections installed less than their share of the wrong declared
  crossings** (K3 fails): 111 of 213, 0.5211, where they were 0.6152 of the
  births.
- **N r3's refused right sides are of L's kind** (K5 fails): 100 of its 99,205
  pair-points need a wrong crossing.

### 2. The even crossings — added after the first run

| run | right | cut once the even crossings are out too | stands on right crossings |
|---|---|---|---|
| L r1 | 78,600 | 70,270 | 8,330 |
| L r2 | 134,570 | 131,060 | 3,510 |
| L r3 | 3,260 | 840 | 2,420 |
| N r1 | 480 | 0 | 480 |
| N r2 | 120 | 40 | 80 |
| N r3 | 99,105 | 98,240 | 865 |

- **The crossings into `SECURITY_INCIDENT` were even.** Taken out too, they cut
  the paths on 70,270 of L r1's 78,600 points of class right, 131,060 of L r2's
  134,570 and 98,240 of N r3's 99,105. Those are all three runs' pair-points of
  `SECURITY_INCIDENT`.
- **The rules above them are the policy's exception, nested in the keyword's
  region.**
  - **In L r1**, `R0061`: `has_security_keyword = true ∧ severity = 4 →
    T2_TECHNICAL`.
  - **In L r2**, `R0048`: `has_security_keyword = true ∧ severity ≥ 4 ∧ product =
    billing → T2_TECHNICAL`, and `R0120`: `has_security_keyword = true ∧ severity
    ≥ 3 → T2_TECHNICAL`.
  - **In L r3**, `R0016`: `has_security_keyword = true ∧ severity ≥ 3 →
    T2_TECHNICAL`, on 840 points.
  - **In N r3**, `R0175`: `has_security_keyword = true ∧ severity = 4 ∧
    customer_tier = free → T1_GENERAL`.
  - **Each was born at a reported ticket of `H03`**, the policy's exception for
    security mentions on small accounts at low severity.
- **Why even.** Each L rule drops the tier. Its points are `SECURITY_INCIDENT`'s
  on the large accounts and `T2_TECHNICAL`'s on the small ones, as many of each.
  N r3's keeps the tier and names `T1_GENERAL` where the policy says
  `T2_TECHNICAL`, so neither of its two queues is the truth there.
- **Such a rule beats the keyword's rule by containment**, so every rule above
  it reaches the keyword's rule through it. A newborn whose wins reach any of
  those rules cannot be placed below the keyword's rule, however far its path
  runs from the contested points.

### 3. An engine that refuses only where the cycle is — added after the first run

| run | the record's engine: final | fall | `SECURITY_INCIDENT` recall | refusing only where the cycle is: final | fall | `SECURITY_INCIDENT` recall | edges refused, record → this engine |
|---|---|---|---|---|---|---|---|
| L r1 | 0.5647 | 0.1249 | 0.3514 | 0.7432 | 0.0333 | 0.7327 | 1,849 → 1,430 |
| L r2 | 0.4221 | 0.3553 | 0.1437 | 0.6154 | 0.1724 | 0.6405 | 2,159 → 1,182 |
| L r3 | 0.5618 | 0.1277 | 0.2976 | 0.5629 | 0.1366 | 0.2976 | 1,597 → 1,462 |
| N r1 | 0.5519 | 0.0485 | 0.9250 | 0.5430 | 0.0691 | 0.9250 | 1,007 → 791 |
| N r2 | 0.5785 | 0.0221 | 1.0000 | 0.5794 | 0.0212 | 1.0000 | 772 → 700 |
| N r3 | 0.4932 | 0.1343 | 0.6929 | 0.5535 | 0.0710 | 0.8333 | 905 → 727 |

This engine refuses an edge for a cycle only when the cycle runs through rules
that all match some point the edge decides. The same births and declarations
are installed in the record's order.

- **It keeps most of what L r1 and L r2 lost.**
  - **L r1 ends at 0.7432 of the space, L r2 at 0.6154 and N r3 at 0.5535**,
    where the record's engine ends them at 0.5647, 0.4221 and 0.4932.
  - **`SECURITY_INCIDENT`'s recall rises** from 0.3514 to 0.7327, from 0.1437 to
    0.6405, and from 0.6929 to 0.8333.
  - **L r3 barely moves**, from 0.5618 to 0.5629: its fall was taken by
    containment. N r1 loses 0.0089, and N r2 gains 0.0009.
- **It leaves no point without a rule undefeated, and decides as its masks do**
  (gate 6). A cycle through rules that miss every point an edge decides is seen
  by no point.
- **Beside `corrections/fall.py`'s losses first**, which ended L r1 at 0.7374, L
  r2 at 0.6539 and N r3 at 0.5459, it keeps more in L r1 and N r3, and less in L
  r2.
- **It is not the loop that would have run.** A base ordered otherwise decides
  the arrivals otherwise, and would have escalated other cases.

### The expectation

Written in `corrections/paths.py`'s docstring and committed before the reading
ran. It is not signed, and it is on no scoreboard.

| clause | reading | |
|---|---|---|
| K1, at least half of L's pair-points in pairs a wrong crossing carries | 4,111 of 220,541 | fails |
| K2, at least half of those need a wrong declared one | 3,581 of 4,111 | **holds** |
| K3, the corrections' share of the wrong declared crossings at least their share of the births | 0.5211 against 0.6152 | fails |
| K4, at least half of L's pair-points in pairs whose cycle is somewhere | 21,800 of 220,541 | fails |
| K5, in N r3, at least half of the pair-points in pairs a wrong crossing carries | 100 of 99,205 | fails |

**K2 holds, and K1, K3, K4 and K5 fail.** The bet `K4` failed: the cycle the
engine refuses is nowhere the pair decides, as `PLAN_CHANNEL.md`'s reading of a
refused right edge had found. `K2` held on 4,111 points.

### What it says

- **On nine of every ten pair-points, the engine refused the right side for a
  cycle no point sees.** The paths run through rules that miss every point the
  pair shares. Installed, the edge would have decided the pair's points rightly,
  and closed a cycle at no point of the base.
- **The gateway is the policy's exception, compiled as a rule nested in the
  keyword's region.** A correction at a ticket of `H03` drops the tier, nests
  inside the keyword's rule and beats it by containment. Every rule above it then
  reaches the keyword's rule, and so does any newborn whose wins reach one of
  them.
- **The label is not needed for it.** N r3's gateway was drafted at a ticket of
  `H03` without one, and named a queue the policy does not.
- **Two levers keep most of the share on the same declarations, with no call**:
  installing a rule's losses before its wins, or refusing a cycle only where it
  is. Neither is the loop that would have run.

### What it does not settle

1. **Whether a loop whose engine refuses a cycle only where it is keeps its
   share.** A plan with calls, and an engine of its own: `rung2/engine2.py` is the
   closed records' engine and is not edited.
2. **Why so many rules sit above the gateway.** The reading does not say which
   declarations put them there, nor why the paths run so long. Free on the
   records.
   **[NOTE 2026-11-15] Read POST-RUN, below: not so many.** About three in ten
   of the rules L bore after the gateway end above it, through few doors, which
   mostly placed themselves above it. The paths are long because the rules above
   accreted on those doors, mostly by their own wins. *Why so many rules sit
   above the gateway*.
3. **Whether a first call that kept `H03`'s tier would have opened no gateway.**
   A plan with calls.

## Why so many rules sit above the gateway — POST-RUN

**Asked for by Sergi on 2026-11-15, after the reading above.** It found the
paths of the refused right sides entering `SECURITY_INCIDENT`'s rule through a
rule nested in the keyword's region, born at a reported ticket of `H03`. Its
*What it does not settle*, item 2, left which declarations put the rules of
other queues above that rule, and why the paths to it run so long. This reading
asks the records, and spends nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.gateway`, on
2026-11-15 in local time, from `bcf20d8` on a clean tree, on the branch of
#250, which is `31a3479` on `main`.
- **The commits.** `f285f8b` on `main` carries the reading and its expectation,
  written before the reading ran. `31a3479` carries the part added after the
  first run, which moves no clause. The first run's record was not committed.
- **The record was committed alone**, as `3ae3f2b`. On #250's branch the three
  commits were `b7512e3`, `bcf20d8` and `51a3039`. Each pair has the same
  subject, the same tree and the same `git patch-id --stable`, and the GitHub
  API names #250 behind the three `main` commits.
- **The record is [`gateway.json`](gateway.json).** Its six gates passed in all
  six runs:
  - the replay is the base;
  - the gateways and the pairs are `paths.json`'s, and each gateway lies inside
    the keyword's region;
  - every edge a birth tries has the rule born there on one side;
  - the rules above the gateways only grow;
  - every newborn of a pair through a gateway reaches one of its gateways, at a
    distance `paths.json`'s shortest path allows;
  - every rule above a gateway is classed once, at a depth of at least one, and
    every door's edge is classed.

**What it reads.**
- **A run's gateways** are the rules `paths.json` gives above its even
  crossings, born at a ticket of `H03`, of a queue other than
  `SECURITY_INCIDENT`: `R0061` in L r1, `R0048` and `R0120` in L r2, `R0016` in
  L r3 and `R0175` in N r3. N r1 and N r2 have none.
- **The base is replayed in birth order.** After each birth the reading takes
  the rules that reach a gateway born so far, by containment and by declared
  edges.
  - **A door** is a rule one step above a gateway: nested inside it, or
    declared above it.
  - **A rule's depth** is the fewest steps from it to a gateway.
- **Each rule above a gateway entered at one birth**, the first after which it
  reaches one:
  - *own_wins*, at its own birth, through one of its declared wins;
  - *containment*, at its own birth, through a rule that contains it;
  - *brought*, at a later birth, through the rule born then;
  - *at_gateway*, at a gateway's birth.
- **The pairs through a gateway** are `paths.json`'s pairs whose even crossings
  run from a gateway. Their newborns are read right after their births, and
  each pair is weighed by its points, as `paths.json` weighs it.

### 1. Not so many

| run | gateways | rules born after the first | above a gateway at the end | rules above, in all | doors | two steps or more away |
|---|---|---|---|---|---|---|
| L r1 | `R0061` | 221 | 66 | 67 | 1 | 66 |
| L r2 | `R0048`, `R0120` | 226 | 100 | 102 | 5 | 97 |
| L r3 | `R0016` | 257 | 49 | 49 | 8 | 41 |
| N r3 | `R0175` | 156 | 5 | 5 | 1 | 4 |

- **About three in ten of the rules L bore after its first gateway end above
  one** (D1 fails): 215 of 704. In N r3, five of 156 do (D6 fails).
- **Few, and enough.** Each newborn of a pair through a gateway reached it at
  its birth through one to seven of its declared wins, of the 1 to 108 it
  declared. None reached it through a rule that contains it. At those births,
  4 to 94 rules sat above a gateway.

### 2. The doors placed themselves

| run | rounds that listed a gateway | it above the newborn, installed | it above, refused for a cycle | the newborn above it, installed | the newborn above, refused for a cycle |
|---|---|---|---|---|---|
| L r1 | 78 | 64 | 9 | 1 | 4 |
| L r2 | 82 | 33 | 35 | 5 | 9 |
| L r3 | 107 | 85 | 12 | 7 | 3 |
| N r3 | 40 | 20 | 1 | 1 | 18 |

A round that listed both of L r2's gateways is counted once for each.

- **Every declared edge from a door into a gateway was the door's own answer**
  (D4 holds): 13 of 13. Three more doors are nested inside a gateway: `R0016`
  and `R0265` in L r2, and `R0210` in L r3.
- **No gateway's answer put a rule above it.** The five gateways' answers
  declared 82 wins and 12 losses, and the engine refused the 12 for closing
  cycles.
- **The rounds that listed a gateway mostly put it above their newborn.** In L,
  238 of the 267 declared the newborn below the gateway, and 29 above it. 13 of
  those 29 were installed: the doors. Over every round, L's answers declared
  their newborn below 8,035 of the 19,921 rules they placed.
- **L r1 has one door.** `R0062`, `customer_tier = business ∧
  prior_tickets_30d ≥ 20 → ACCOUNT_MANAGER`, was born at a conflict at the birth
  after `R0061`'s.
  - **Its answer declared it above 19 rules**, `R0061` among them, and below 9,
    all refused for cycles.
  - **Every one of the 67 rules above `R0061` reaches it only through `R0062`.**
  - **The policy's verdict on the edge is even.** The 200 points the two rules
    share are `SECURITY_INCIDENT`'s, by `H01`.
- **In L r2, `R0051` carries nearly all.** `severity = 4 ∧ customer_tier = pro ∧
  prior_tickets_30d ≥ 15 → T1_GENERAL` was born at a reported error, three
  births after `R0048`.
  - **101 of the 102 rules above a gateway reach it**, itself included, and 63
    reach a gateway only through it.
  - **The policy calls its edge wrong.** The 240 points it shares with `R0048`
    are `T2_TECHNICAL`'s, by `H03`.
- **N r3's one door is right by the policy.** `R0213`, `product = api ∧
  customer_tier = free ∧ severity = 4 ∧ prior_tickets_30d ≥ 10 → T2_TECHNICAL`,
  shares 440 points with `R0175`. All are `T2_TECHNICAL`'s, by `H03`, where
  `R0175` names `T1_GENERAL`. All five rules above `R0175` reach it only
  through `R0213`.

### 3. The rules above entered by their own wins

| run | own_wins | containment | brought | at_gateway |
|---|---|---|---|---|
| L r1 | 52 | 10 | 5 | 0 |
| L r2 | 74 | 23 | 5 | 0 |
| L r3 | 40 | 5 | 4 | 0 |
| N r3 | 5 | 0 | 0 | 0 |

- **Most entered at their own birth, by one of their declared wins** (D2 holds,
  the bet): 166 of L's 218. 38 entered through a rule that contains them, and
  14 were brought up by a later rule. None entered at a gateway's birth.
- **Some against their own answer.** 56 of the 238 declarations in L that put a
  gateway above the newborn were refused. The newborn's wins, installed first,
  already reached the gateway.

### 4. Why the paths run long

| run | one step | two | three | four | five | six |
|---|---|---|---|---|---|---|
| L r1 | | 27,670 | 42,600 | | | |
| L r2 | | 6,920 | 45,160 | 60,200 | 15,000 | 3,780 |
| L r3 | 840 | | | | | |
| N r3 | | | 9,520 | 88,720 | | |

The pair-points through a gateway, by the newborn's distance to it.

- **Nearly every rule above sits two steps or more from every gateway** (D3
  holds): 204 of L's 218, and up to five.
- **The rules above accreted on few doors**, most of them through a win over a
  rule already above. A newborn's nearest win above a gateway was mostly two
  steps or more from it, so most of the newborns' paths run three steps or more
  to it.

### 5. The newborns mostly miss their gateway

- **On most pair-points the newborn shares no point with its gateways** (D5
  holds): 130,420 of L's 202,170.
  - **L r2 carries it**, with 108,420 of 131,060.
  - **In L r1 most pair-points are in pairs whose newborn meets `R0061`**:
    48,270 of the 70,270.
- **An edge between two rules that share no point is never installed.** So such
  a newborn reaches its gateway only through rules that meet both.
- **Of the 17 newborns in L that meet a gateway:**
  - **10 are of `T2_TECHNICAL`, the gateway's own queue.** v1c lists only rules
    of other queues, so their rounds never listed the gateway.
  - **6 were listed it and declared themselves below it.** The engine refused
    that too, for the same cycle: `R0214`, `R0199` and `R0274` in L r1, and
    `R0095`, `R0068` and `R0073` in L r2.
  - **One, L r3's `R0090`, declared itself above it**, and is one of its doors.

### The expectation

Written in `corrections/gateway.py`'s docstring and committed before the reading
ran. It is not signed, and it is on no scoreboard.

| clause | reading | |
|---|---|---|
| D1, of the rules born after their run's first gateway, at least half above one at the end | 215 of 704 | fails |
| D2, of the rules above a gateway at the end, at least half entered own_wins | 166 of 218 | **holds** |
| D3, of those, at least half at a depth of two or more | 204 of 218 | **holds** |
| D4, of the declared edges from a door into a gateway, at least half door_win | 13 of 13 | **holds** |
| D5, at least half of the pair-points in pairs whose newborn shares no point with its gateways | 130,420 of 202,170 | **holds** |
| D6, in N r3, of the rules born after its gateway, at least half above it at the end | 5 of 156 | fails |

**D2, D3, D4 and D5 hold, and D1 and D6 fail.** The bet D2 held. D5, trusted
least, held on L r2's pair-points: on L r1's alone it would have failed. D1 was
the question's own premise, and it failed: the rules above the gateway are not
many.

### What it says

- **The rules above the gateway are few, and the newborns' wins find them.**
  About three in ten of the rules L bore after its gateways end above one, and
  five of 156 in N r3. Each newborn of a refused right side reached a gateway
  through a few of its declared wins.
- **The declared doors put themselves above the gateway, against what most
  answers did.** In L, nine answers in ten that were listed a gateway put it
  above their newborn. The few whose rule was installed above it are the
  declared doors. In L r1 one door, born at the next birth, carries every rule
  above.
- **The paths run long because the rules above accreted on few doors**, mostly
  through a win over a rule already above. So nearly every rule above is two
  steps or more from the gateway.
- **The newborns mostly miss the gateway.** Those that meet it are mostly of its
  queue, and v1c never lists it to them. Six of the seven listed it put it above
  themselves, and their wins had already put them above it.

### What it does not settle

1. **Why the doors declared themselves above the gateway**, where nine answers
   in ten in L put it above. Their reasoning is in the records. Free.
   **[NOTE 2026-11-15] Read POST-RUN, below: they read it by its queue.** The
   answers place a keyword rule of another queue as a security rule, and the
   answers that climbed over the gateway read it as a rule of `T2_TECHNICAL`.
   Most of the doors still put their newborn below the security rule the
   gateway beats by containment, and the engine refused that loss. The rest put
   their newborn above every rule of their list. *Why the doors declared
   themselves above the gateway*.
2. **How much of the fall the doors carry.** A replay of the same births without
   the doors' edges is free on the records. It is not the loop that would have
   run.
   **[NOTE 2026-11-15] Read POST-RUN, below: most of L's.** Without the doors'
   edges, the same births and declarations keep 0.6391 of L's three falls,
   summed. One edge carries more than L r1's, one door L r2's, and L r3 keeps
   nothing. *How much of the fall the doors carry*.

## Why the doors declared themselves above the gateway — POST-RUN

**Asked for by Sergi on 2026-11-15, after the reading above.** It found few doors
into the gateways, each declared one placed by its own answer, where nine answers
in ten in L that were listed a gateway put it above their newborn. Its *What it
does not settle*, item 1, left why. This reading asks the records, and spends
nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.doors`, on 2026-11-15
in local time, from `48900e0` on a clean tree, on the branch of #252, which is
`a46490f` on `main`.
- **The development set.** L r1 was read before the expectation was written:
  its rounds that listed the gateway, what their answers declared, the passages
  of their reasoning that name the gateway, and five candidate codes over those
  passages. The codes told the sides apart by little, so the reading reads what
  each answer declared. Every clause reads L r2 and L r3, pooled, and N r3.
- **The commits.** `0a61c8e` on `main` carries the reading and its
  expectation, written before the reading ran on the other runs. `a46490f`
  carries the part added after the first run, which moves no clause. The first
  run's record was not committed.
- **The record was committed alone**, as `e13cb90`. On #252's branch the three
  commits were `5751982`, `48900e0` and `cba5f86`. Each pair has the same
  subject, the same tree and the same `git patch-id --stable`, and the GitHub
  API names #252 behind the three `main` commits.
- **The record is [`doors.json`](doors.json).** Its gates passed in all six
  runs:
  - the listings are `gateway.json`'s, by what each answer declared of its
    gateway and what the engine did;
  - the climbs the engine installed are its doors' declared edges;
  - every listing's newborn crosses its gateway, of another queue;
  - every installed climb's loss to a security rule that contains its gateway
    was refused for a cycle;
  - L r1 gives the counts the module's docstring gives of it.

**What it reads.**
- **A listing** is a round that listed a gateway born before it, once per
  gateway, as `gateway.json` counts them. Its side is what its answer declared of
  the gateway, whatever the engine did: a *climb* put the newborn above it, a
  *cede* below it. The doors are the climbs the engine installed.
- **For each listing**, what its answer did with two sets of the rules its round
  listed. It put its newborn above every one, below every one, or some of each.
  - **The other keyword rules** are the rules of a queue other than
    `SECURITY_INCIDENT` whose region lies inside the keyword's half, the gateways
    left out.
  - **The security rules** are the rules of `SECURITY_INCIDENT` whose region
    contains the gateway's. The gateway beats each of them by containment.
- **Every placement of every round**, by the kind of rule placed.
- **Added after the first run**: what each answer did with its whole list, and
  with the round's rules of the gateway's queue that are not keyword rules.

### 1. The answers place a keyword rule as a security rule

| run | security rules | other keyword rules | gateways | rules outside the keyword |
|---|---|---|---|---|
| L r1, development | 678 of 689 | 59 of 63 | 73 of 78 | 1,890 of 6,423 |
| L r2 | 921 of 945 | 49 of 59 | 68 of 82 | 1,419 of 5,326 |
| L r3 | 916 of 950 | 88 of 99 | 97 of 107 | 1,777 of 5,026 |
| N r3 | 1,337 of 1,369 | | 21 of 40 | 2,426 of 7,158 |

The placements that put the newborn below the rule placed, by the rule's kind.

- **The answers put their newborn below nearly every security rule** they
  placed, and below a quarter to two fifths of the rules outside the keyword's
  half.
- **They put it below a keyword rule of another queue nearly as often** (F1
  holds): below 137 of the 158 such placements in L r2 and L r3.
- **The gateway is such a rule.** In L, 238 of the 267 rounds that listed one
  put it above their newborn. No round of N r3 listed another keyword rule, and
  21 of its 40 rounds put its gateway, a rule of `T1_GENERAL`, above their
  newborn.

### 2. The climbs read it by its queue

| run | climbs | above every other keyword rule | none listed | cedes | below every other keyword rule | above every one | none listed |
|---|---|---|---|---|---|---|---|
| L r1, development | 5 | 3 | 2 | 73 | 57 | 1 | 15 |
| L r2 | 14 | 10 | 4 | 68 | 50 | | 18 |
| L r3 | 10 | 6 | 4 | 97 | 65 | | 32 |
| N r3 | 19 | | 19 | 21 | | | 21 |

- **Every held-out climb whose round listed another keyword rule put its newborn
  above every one** (F2 holds, the bet): 16 of 16. **Every such cede put its
  newborn below every one** (F3 holds): 115 of 115. An answer places the keyword
  rules of other queues one way, and the gateway with them.
- **The climbs place the gateway as they place its queue.** Added after the
  first run: 21 of the 24 held-out climbs put their newborn above every rule of
  the gateway's queue that is not a keyword rule, and 17 of N r3's 19. Of the
  165 held-out cedes, 67 did too, and still put the gateway above: they place it
  apart from its queue.
- **In L r1's reasoning**, the development set, the cedes call the gateway
  security, by its keyword: "Pierde porque security". The climbs call it a rule
  of `T2_TECHNICAL`: "R0061 is T2, so our rule should beat it".

### 3. Two kinds of climb

| run | climbs | below every security rule | above every rule of the list | above every security rule, not the whole list | no security rule listed |
|---|---|---|---|---|---|
| L r1, development | 5 | 4 | | 1 | |
| L r2 | 14 | 10 | 4 | | |
| L r3 | 10 | 5 | 3 | | 2 |
| N r3 | 19 | 18 | 1 | | |

- **Most climbs still yield to security, in the same answer.** 15 of the 22
  held-out climbs whose round listed a security rule put their newborn below
  every one, short of F4's three quarters. 18 of N r3's 19 did (F6 holds). Two
  of L r1's climbs say the security rules will win over both anyway.
- **The rest put their newborn above every rule of their list**, added after the
  first run: all 7 held-out climbs above every security rule, and N r3's one.
  L r1's R0273 placed its list by the number of conditions, and put its newborn
  above the security rules too.

### 4. The doors

- **8 of L's 13 door edges yield to security**: `R0062` in L r1; `R0051`, and
  `R0143` into both gateways, in L r2; `R0063`, `R0090`, `R0096` and `R0153` in
  L r3. So does N r3's one door, `R0213`.
  - **Each answer declared its newborn below a security rule that contains the
    gateway**, and the engine refused every such loss for a cycle (gate 4).
  - **The door, installed above the gateway, was already above that rule.** The
    loop installs a newborn's wins before its losses, and the gateway beats the
    rule by containment. The round's list gives each rule's declared wins, not
    what containment orders.
- **The other 5 are above every rule of their list**: `R0234`, into both of
  L r2's gateways, and `R0048`, `R0122` and `R0273` in L r3.
- **In each L run, the declared door that carries the most rules above a
  gateway yields to security.** In `gateway.json`, `R0062` carries all 67 of
  L r1's, `R0051` 101 of L r2's 102, and `R0090` 47 of L r3's 49.

### 5. Not by the ticket, nor by size

- **No listing's ticket lies inside its gateway**, in any run. No answer climbed
  to take its own ticket from the gateway.
- **The climbs' newborns are no narrower than the cedes'.** Narrower than the
  gateway: 11 of L r2's 14 climbs and 51 of its 68 cedes; all 10 of L r3's
  climbs and all 97 of its cedes; 5 of N r3's 19 climbs and 5 of its 21 cedes.

### The expectation

Written in `corrections/doors.py`'s docstring after L r1 was read, and committed
before the reading ran on the other runs. It is not signed, and it is on no
scoreboard.

| clause | reading | |
|---|---|---|
| F1, of the placements against other keyword rules, at least three quarters below | 137 of 158 | **holds** |
| F2, of the climbs whose round listed another keyword rule, at least three quarters above every one | 16 of 16 | **holds** |
| F3, of such cedes, at least three quarters below every one | 115 of 115 | **holds** |
| F4, of the climbs whose round listed a security rule, at least three quarters below every one | 15 of 22 | fails |
| F5, in N r3, F2's statement | nothing to read | fails |
| F6, in N r3, F4's statement | 18 of 19 | **holds** |

**F1, F2, F3 and F6 hold, and F4 and F5 fail.** The bet F2 held. F4 failed on
the climbs that put their newborn above every rule of their list. F5, trusted
least, read nothing: no round of N r3 listed another keyword rule, and a share
over nothing fails.

### What it says

- **The answers yield to the security queue, and place a keyword rule of another
  queue as a security rule.** The gateway is a rule of `T2_TECHNICAL` on the
  keyword, so nine answers in ten put it above their newborn.
- **The climbs read the gateway by its queue.** They put their newborn above it,
  as above the round's other keyword rules of other queues, and as above the
  rules of the gateway's own queue outside the keyword.
- **Most climbs still yield to security in the same answer.** The engine cannot
  keep both. The gateway lies inside the keyword's security rule and beats it by
  containment, which the round does not show. Every installed one had its loss
  to that rule refused, and in each L run the declared door that carries the
  most rules above a gateway is of this kind.
- **The other climbs put their newborn above every rule of their list.**
- **Neither the ticket nor the size tells a climb from a cede.**

### What it does not settle

1. **What makes an answer read a keyword rule by its queue.** Both readings
   appear in the same reasonings, and nothing read here tells a climb's round
   from a cede's beyond what its answer did. Free on the records.
2. **Why some answers put their newborn above every rule of their list.** Free
   on the records.
3. **Whether a round that showed what containment orders would have kept the
   doors below the gateway.** A plan with calls.

## How much of the fall the doors carry — POST-RUN

**Asked for by Sergi on 2026-11-15, after the reading above.** The reading of why
so many rules sit above the gateway found them reaching it through few doors.
Its *What it does not settle*, item 2, left how much of what L lost rests on
them. This reading replays the same births and declarations without the doors'
edges, and spends nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.carry`, on 2026-11-15
in local time, from `f9d3c46` with its code clean, on the branch of #254, which
is `770931a` on `main`.
- **The commits.** `971cf17` on `main` carries the reading and its expectation,
  written before the reading ran. `770931a` carries the part added after the
  first run, which moves no clause. The first run's record was not committed.
- **The record was committed alone**, as `7ef2a59`. On #254's branch the three
  commits were `3165456`, `f9d3c46` and `de5fd6b`. Each pair has the same
  subject, the same tree and the same `git patch-id --stable`, and the GitHub
  API names #254 behind the three `main` commits.
- **Its `_env` says `git_dirty`**, because the sandbox the session ran in mounts
  placeholder files in the repository's root, which git counts as untracked.
  `code_dirty` is false, and the code digest, `fdf19c791cc3b129`, is the one
  `main` computes at `770931a`, and still at the merge.
- **The record is [`carry.json`](carry.json).** Its five gates passed in all six
  runs:
  - the replay that leaves nothing out is `fall.json`'s record order, at every
    birth;
  - the edges left out are the records';
  - each replay is the record's order until it leaves an edge out;
  - every replay's masks are its engine's;
  - a run without a gateway leaves nothing out.

**What it reads.** Each run's births and declarations, installed in the record's
order as `corrections/fall.py`'s `order_replay` installs them, with declared
edges left out:
- **the doors' edges**, `gateway.json`'s declared wins of a door over a gateway;
- **every declared win over a gateway**, the doors' and the climbs the engine
  refused;
- **each door's edges alone.**

A door nested inside a gateway beats it by containment, which is no edge, and
stays in every replay. Each replay is read over the space's 134,400 points as
`fall.json` reads the record's order. **What it keeps** is its final less the
record's, set beside the record's fall, peak less final. **Added after the
first run**: where each replay's final base decides otherwise than the record's.

### 1. The doors carry most of L's fall

| run | the record's order: final | fall | without the doors' edges: final | kept | of the fall | `SECURITY_INCIDENT` recall | conflict points |
|---|---|---|---|---|---|---|---|
| L r1 | 0.5647 | 0.1249 | 0.7400 | 23,550 | 1.4035 | 0.3514 → 0.8333 | 36,425 → 10,855 |
| L r2 | 0.4221 | 0.3553 | 0.6353 | 28,660 | 0.6002 | 0.1437 → 0.6667 | 49,705 → 7,225 |
| L r3 | 0.5618 | 0.1277 | 0.5618 | 0 | 0 | 0.2976 → 0.2976 | 13,371 → 11,198 |
| N r3 | 0.4932 | 0.1343 | 0.5474 | 7,285 | 0.4035 | 0.6929 → 0.8333 | 12,435 → 4,290 |

N r1 and N r2 have no gateway, and leave nothing out.

- **One edge carries more than L r1's fall** (C1 holds). Without `R0062`'s edge
  into `R0061`, L r1 keeps 23,550 points, where its record's order fell 16,780
  from its peak. It ends at 0.7400, above that peak.
- **One door carries L r2's** (C2 and C5 hold).
  - **Without its doors' edges, L r2 keeps 28,660 points**, 0.6002 of its fall
    of 47,750.
  - **`R0051`'s edge alone keeps 28,600 of them.**
  - **`R0143`'s and `R0234`'s edges, each alone, keep nothing.**
- **L r3 keeps nothing** (C3 holds). Most of its fall was taken by containment.
- **Over the three L runs, the doors carry most of the fall** (C4 holds, the
  bet): 52,210 points of the 81,694 their falls sum to, 0.6391.
- **N r3 keeps 0.4035 of its fall** (C6 holds), though its one door is right by
  the policy on the points it shares with the gateway.
- **Beside the two levers read before**, the doors replay ends between them in
  L r1, L r2 and N r3. Losses first ended them at 0.7374, 0.6539 and 0.5459, and
  the engine that refuses a cycle only where it is at 0.7432, 0.6154 and 0.5535.
- **No climb the record refused became a door.** With every declared win over a
  gateway left out, every run ends where it ends without the doors' edges.

### 2. What the engine installs instead

| run | refused for a cycle in the record, installed here | the newborns' losses to `SECURITY_INCIDENT`'s rules among them | installed in the record, refused here | refusals for a cycle |
|---|---|---|---|---|
| L r1 | 356 | 211 | 9 | 1,849 → 1,502 |
| L r2 | 916 | 370 | 8 | 2,159 → 1,251 |
| L r3 | 90 | 15 | 3 | 1,597 → 1,510 |
| N r3 | 43 | 35 | 2 | 905 → 864 |

- **Without the doors' edges, the engine installs the right sides it refused.**
  In L r1, 211 of the 356 edges it now installs are newborns' losses to a rule of
  `SECURITY_INCIDENT`, and 370 of L r2's 916.
- **Few edges go the other way**: nine in L r1, eight in L r2.

### 3. Where the replay decides otherwise — added after the first run

| run | gained right | `SECURITY_INCIDENT`'s | lost | the record's conflicts decided | decided wrongly | changed from wrong to wrong | decided to conflict |
|---|---|---|---|---|---|---|---|
| L r1 | 24,570 | 24,290 | 1,020 | 26,870 | 2,580 | 2,980 | 1,300 |
| L r2 | 28,740 | 26,355 | 80 | 42,615 | 14,085 | 14,245 | 135 |
| L r3 | 0 | 0 | 0 | 4,253 | 4,253 | 6,553 | 2,080 |
| N r3 | 7,890 | 7,080 | 605 | 8,310 | 420 | 420 | 165 |

- **What the replay gains is mostly `SECURITY_INCIDENT`'s**, and it loses little:
  1,020 points in L r1, 80 in L r2 and 605 in N r3.
- **In L r3 every point it changes goes from one wrong outcome to another.** The
  4,253 conflicts it decides all go to rules of `T2_TECHNICAL`, on
  `SECURITY_INCIDENT`'s points.
- **In L r2 a third of the conflicts it decides go wrongly**: 14,085 of 42,615.
  - **To rules of `T1_GENERAL`**: 5,050 points of `T2_TECHNICAL` and 4,715 of
    `SECURITY_INCIDENT`.
  - **To rules of `T2_TECHNICAL`**: 4,320 of `SECURITY_INCIDENT`.
- **In L r1, the 2,580 decided wrongly go to rules of `T2_TECHNICAL`**, on
  `SECURITY_INCIDENT`'s points.

### The expectation

Written in `corrections/carry.py`'s docstring and committed before the reading
ran. It is not signed, and it is on no scoreboard.

| clause | reading | |
|---|---|---|
| C1, without its door's edge, L r1 keeps at least half of its fall | 23,550 of 16,780 | **holds** |
| C2, without its doors' edges, L r2 keeps at least half of its fall | 28,660 of 47,750 | **holds** |
| C3, without its doors' edges, L r3 keeps at most a quarter of its fall | 0 of 17,164 | **holds** |
| C4, without their doors' edges, the three L runs keep at least half of their falls, summed | 52,210 of 81,694 | **holds** |
| C5, without `R0051`'s edge alone, L r2 keeps at least half of what it keeps without all its doors' edges | 28,600 of 28,660 | **holds** |
| C6, without its door's edge, N r3 keeps at least a quarter of its fall | 7,285 of 18,055 | **holds** |

**All six hold.** The bet `C4` held, on L r1 and L r2. `C5`, trusted least,
held at 0.9979.

### What it says

- **The doors carry most of L's fall.** One edge carries more than L r1's, and
  one door carries L r2's.
- **Without them, the engine installs the right sides it refused.** The
  newborns' losses to the keyword's rule go in, and the conflicts the fall left
  close mostly in `SECURITY_INCIDENT`'s favour.
- **Where containment took the fall, no edge left out brings it back.** In L r3
  the replay moves points only between wrong outcomes.
- **Rules of other queues still decide wrongly part of what the doors left.**
  The conflicts the replay decides wrongly go to rules of `T2_TECHNICAL` and
  `T1_GENERAL`, on points the policy gives another queue.
- **It is not the loop that would have run.** A base without those edges decides
  the arrivals otherwise, and would have escalated other cases.

### What it does not settle

1. **Whether a loop that refuses a climb over a rule nested in the keyword's
   region keeps its share.** The doors' edges are such climbs. A protocol
   change, with calls.
2. **Which rules decide wrongly the conflicts the replay resolves in L r2.**
   They are rules of `T1_GENERAL` and `T2_TECHNICAL`, on points of
   `T2_TECHNICAL` and `SECURITY_INCIDENT`. Free on the records.

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
- [`broad.json`](broad.json): POST-RUN, why the first call writes broad
  corrections.
- [`fall.json`](fall.json): POST-RUN, why the loop's share of the space peaked
  and fell.
- [`paths.json`](paths.json): POST-RUN, why a rule's wins reach the rule it
  should lose to.
- [`gateway.json`](gateway.json): POST-RUN, why so many rules sit above the
  gateway.
- [`doors.json`](doors.json): POST-RUN, why the doors declared themselves above
  the gateway.
- [`carry.json`](carry.json): POST-RUN, how much of the fall the doors carry.
