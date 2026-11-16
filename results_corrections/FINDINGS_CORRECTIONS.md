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
- **The POST-RUN reading of what makes an answer read a keyword rule by its
  queue** reached it in #256, merged on 2026-11-15.
- **The POST-RUN reading of why some answers put their newborn above every rule
  of their list** reached it in #259, merged on 2026-11-15.
- **The POST-RUN reading of what makes an answer read the list by its
  conditions** reached it in #261, merged on 2026-11-15.
- **The POST-RUN reading of why L loses `ONCALL_ESCALATION`** reached it in
  #263, merged on 2026-11-15.
- **The POST-RUN reading of what the at-once asks wrote for
  `ONCALL_ESCALATION`** reached it in #265, merged on 2026-11-16 in local
  time.
- **The POST-RUN reading of shape or order** reached it in #267, merged on
  2026-11-16.
- **The POST-RUN reading of whether the order the loop lacks is a ranking of
  the queues** reached it in #269, merged on 2026-11-16.
- **The POST-RUN reading of whether the loop declared the ranking it lacks**
  reached it in #271, merged on 2026-11-16.
- **The POST-RUN audit of the citations on both sides** reached it from #273, on
  2026-11-16. The merge answered 502, and GitHub never marked the pull request
  merged, so it was closed by hand.
- **The POST-RUN reading of the ranking the loop declared, as it went** reached
  it in #275, merged on 2026-11-16.

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
>
> **[NOTE 2026-11-15, after it] And an eighth.** [`byqueue.json`](byqueue.json)
> is the POST-RUN reading of what makes an answer read a keyword rule by its
> queue.
> - **It was written from `7379251`**, on the branch of #256, which is `d5c8c19`
>   on `main`: the commit that carries the part added after its first run. Its
>   section below names the commit that carries its expectation.
> - **Its code digest is `3d849b1feeb3c1cd`**, because `corrections/byqueue.py`
>   was added after the readings above. `main` computes it at `d5c8c19`, and
>   still at the merge of #256. Its `_env` says `git_dirty`, for the same files,
>   and `code_dirty` is false. The modules Stage C ran did not change.
>
> **[NOTE 2026-11-15, after the eighth] And a ninth.** [`above.json`](above.json)
> is the POST-RUN reading of why some answers put their newborn above every rule
> of their list.
> - **It was written from `13ce82d`**, on the branch of #259, which is `ccef280`
>   on `main`: the commit that carries its expectation. Nothing was added after
>   its first run.
> - **Its code digest is `ff2e2076bc7bd312`**, because `corrections/above.py`
>   was added after the readings above. `main` computes it at `ccef280`, and
>   still at the merge of #259. Its `_env` says `git_dirty`, for the same files,
>   and `code_dirty` is false. The modules Stage C ran did not change.
>
> **[NOTE 2026-11-15, after the ninth] And a tenth.**
> [`conditions.json`](conditions.json) is the POST-RUN reading of what makes an
> answer read the list by its conditions.
> - **It was written from `a8ca66e`**, on the branch of #261, which is `f33321e`
>   on `main`: the commit that carries the part added after its first run. Its
>   section below names the commit that carries its expectation.
> - **Its code digest is `2b3e6ca0a22c99ae`**, because
>   `corrections/conditions.py` was added after the readings above. `main`
>   computes it at `f33321e`, and still at the merge of #261. Its `_env` says
>   `git_dirty`, for the same files, and `code_dirty` is false. The modules Stage
>   C ran did not change.
>
> **[NOTE 2026-11-15, after the tenth] And an eleventh.**
> [`oncall.json`](oncall.json) is the POST-RUN reading of why L loses
> `ONCALL_ESCALATION`.
> - **It was written from `24753d8`**, on the branch of #263, which is `8292de4`
>   on `main`: the commit that carries the second part added after its first
>   run. Its section below names the commits before it.
> - **Its code digest is `c19988c1a4a6ee4e`**, because `corrections/oncall.py`
>   was added after the readings above. `main` computes it at `8292de4`, and
>   still at the merge of #263. Its `_env` says `git_dirty`, for the same files,
>   and `code_dirty` is false. The modules Stage C ran did not change.
>
> **[NOTE 2026-11-15, after the eleventh] And a twelfth.**
> [`layer.json`](layer.json) is the POST-RUN reading of what the at-once asks
> wrote for `ONCALL_ESCALATION` and the layer below it.
> - **It was written from `5e15c43`**, on the branch of #265, which is `0e72e6e`
>   on `main`: the commit that carries the part added after its first run. Its
>   section below names the commit that carries its expectation.
> - **Its code digest is `f0e1e3d4b07d05d2`**, because `corrections/layer.py`
>   was added after the readings above. `main` computes it at `0e72e6e`, and
>   still at the merge of #265. Its `_env` says `git_dirty`, for the same files,
>   and `code_dirty` is false. The modules Stage C ran did not change.
>
> **[NOTE 2026-11-16, after the twelfth] And a thirteenth.**
> [`shape.json`](shape.json) is the POST-RUN reading of shape or order: what the
> loop's own rules could decide, ordered.
> - **It was written from `770f4dd`**, on the branch of #267, which is `7929328`
>   on `main`: the commit that carries the part added after its first run. Its
>   section below names the commit that carries its expectation.
> - **Its code digest is `36b0735352d7dde6`**, because `corrections/shape.py`
>   was added after the readings above. `main` computes it at `7929328`, and
>   still at the merge of #267. Its `_env` says `git_dirty`, for the same files,
>   and `code_dirty` is false. The modules Stage C ran did not change.
>
> **[NOTE 2026-11-16, after the thirteenth] And a fourteenth.**
> [`hierarchy.json`](hierarchy.json) is the POST-RUN reading of whether the
> order the loop lacks is a ranking of the queues.
> - **It was written from `f5ff529`**, on the branch of #269, which is `f801387`
>   on `main`: the commit that carries the reading and its expectation. Nothing
>   was added after it ran.
> - **Its code digest is `423f43512f91c958`**, because
>   `corrections/hierarchy.py` was added after the readings above. `main`
>   computes it at `f801387`, and still at the merge of #269. Its `_env` says
>   `git_dirty`, for the same files, and `code_dirty` is false. The modules
>   Stage C ran did not change.
>
> **[NOTE 2026-11-16, after the fourteenth] And a fifteenth.**
> [`declared.json`](declared.json) is the POST-RUN reading of whether the loop
> declared the ranking it lacks.
> - **It was written from `62587b8`**, on the branch of #271, which is `6c5c03f`
>   on `main`: the commit that carries the reading and its expectation. Nothing
>   was added after it ran.
> - **Its code digest is `da99302475a446c0`**, because
>   `corrections/declared.py` was added after the readings above. `main`
>   computes it at `6c5c03f`, and still at the merge of #271. Its `_env` says
>   `git_dirty`, for the same files, and `code_dirty` is false. The modules
>   Stage C ran did not change.
>
> **[NOTE 2026-11-16, after the fifteenth] And a sixteenth.**
> [`citations.json`](citations.json) is the POST-RUN audit of the citations on
> both sides: what the readings that read declarations through `declared` move.
> - **It was written from `88c8d91`**, on the branch of #273, which is `f7f1c44`
>   on `main`: the commit that carries the part added after its first run. Its
>   section below names the commit that carries its expectation.
> - **Its code digest is `0c21da60ca73814e`**, because
>   `corrections/citations.py` was added after the readings above. `main`
>   computes it at `f7f1c44`, and still at `0a28202`, the last of #273's
>   commits. Its `_env` says `git_dirty`, for the same files, and `code_dirty`
>   is false. The modules Stage C ran did not change.
>
> **[NOTE 2026-11-16, after the sixteenth] And a seventeenth.**
> [`online.json`](online.json) is the POST-RUN reading of the ranking the loop
> declared, as it went.
> - **It was written from `685f46f`**, on the branch of #275, which is `4e7676d`
>   on `main`: the commit that carries the reading and its expectation. Nothing
>   was added after it ran.
> - **Its code digest is `88db753e70125983`**, because `corrections/online.py`
>   was added after the readings above. `main` computes it at `4e7676d`, and
>   still at the merge of #275. Its `_env` says `git_dirty`, for the same files,
>   and `code_dirty` is false. The modules Stage C ran did not change.

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
  **[NOTE 2026-11-15] The rest read POST-RUN, below, with `ONCALL_ESCALATION`.**
  L wrote the rarest queue whole in every run, and lost it beside or below
  corrections of the policy's layer below it. Installing losses first gives back
  the part left contested, and nothing gives back the part outranked. Of
  `SECURITY_INCIDENT`'s points not right at the peak, L r1 left most in
  conflicts, and L r3 lost all of them to a gateway born at case 19. *Why L loses
  `ONCALL_ESCALATION`*.
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
  **[NOTE 2026-11-15] For the rarest queue at once does not win, read POST-RUN,
  below.** Compiled at once, the same labels lose the whole queue in L r2 and L
  r3, whose labels never name it, and keep 2/3 of it in L r1, whose labels name
  it once. The loop keeps more of it in L r2 and L r3. *What the at-once asks
  wrote for `ONCALL_ESCALATION`*.
  **[NOTE 2026-11-16] Read POST-RUN, below: the order in L r1 and L r2, the
  rules in L r3.** In L r1 and L r2 an order of the loop's own rules, found with
  the truth, decides more of the space than at once. In L r3 no order of them
  reaches it: rules of another queue nested in the keyword's region hold
  `SECURITY_INCIDENT`'s points there by containment. *Shape or order*.
  **[NOTE 2026-11-16] And the order it lacks there is mostly a ranking, read
  POST-RUN below.** Ordered by one ranking of the queues, `SECURITY_INCIDENT`
  first, the loop's own rules decide more of the space than at once in L r1 and
  L r2. Neither its labels nor the model's stated rankings find it. *A ranking
  of the queues as the order*.
  **[NOTE 2026-11-16] And the loop had declared most of it, read POST-RUN
  below.** Gathered by pair of queues, its own placement declarations choose
  one ranking, `SECURITY_INCIDENT` first, which orders its rules above at once
  in L r2 and just below it in L r1. *The ranking the loop declared*.
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
  > **[ERRATUM 2026-11-16] 8,033, read on the other side.** In L r1 and L r2
  > one answer each cited a rule both above, installed, and below, refused for
  > the cycle the first side had closed. `corrections/fall.py`'s `declared`,
  > through which this is counted, keeps the second. Kept on the first, L's
  > answers declared their newborn below 8,033 of the 19,921 rules they
  > placed: *The citations on both sides*, below. No verdict moves.
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

> **[ERRATUM 2026-11-16] 1,889 and 1,418, read on the other side.** In L r1 and
> L r2 one answer each cited a rule outside the keyword both above, installed,
> and below, refused for the cycle the first side had closed.
> `corrections/fall.py`'s `declared`, through which this reading counts, keeps
> the second. Kept on the first, L r1's rules outside the keyword placed below
> are 1,889 of 6,423, and L r2's 1,418 of 5,326: *The citations on both sides*,
> below. No verdict moves.

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
  > **[ERRATUM 2026-11-16] 69, read on the other side.** L r2's `R0198` ceded
  > to both of the run's gateways, and cited `R0176`, a rule of their queue,
  > both above, installed, and below, refused. `declared` keeps the second.
  > Kept on the first, both of its listings put the newborn above every such
  > rule: 69 of the 165 cedes. *The citations on both sides*, below. No
  > verdict moves.
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
   **[NOTE 2026-11-15] Read POST-RUN, below: partly what the list shows.** The
   same draft goes both ways. In L r2 and L r3 the gateway listed before every
   security rule climbed far more often, and a list showing a rule ceding to it
   held the answer down. *What makes an answer read a keyword rule by its
   queue*.
2. **Why some answers put their newborn above every rule of their list.** Free
   on the records.
   **[NOTE 2026-11-15, later] Read POST-RUN, below: mostly what the list
   lacks.** The answers place the security rules as one block and the on-call
   rules nearly so, and put their newborn above the rules that hold its ticket.
   The few above the security block read every rule by its conditions, or are
   their queue's general rule read as a domain. *Why some answers put their
   newborn above every rule of their list*.
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

## What makes an answer read a keyword rule by its queue — POST-RUN

**Asked for by Sergi on 2026-11-15, after the reading above.** The reading of why
the doors declared themselves above the gateway found that an answer places a
keyword rule of another queue as a security rule, and cedes to the gateway,
unless it reads that rule by its queue, and climbs. Its *What it does not
settle*, item 1, left what makes it read them by their queue. This reading asks
the records, and spends nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.byqueue`, on
2026-11-15 in local time, from `7379251` with its code clean, on the branch of
#256, which is `d5c8c19` on `main`.
- **The development set.** L r1 and N r3 were read before the expectation was
  written: every listing with its draft, slot, precedent, cause and reasoning
  tokens, and the side. Every clause reads L r2 and L r3, pooled.
- **The commits.** `f0e1853` on `main` carries the reading and its expectation,
  written before the reading ran on L r2 and L r3. `d5c8c19` carries the part
  added after the first run, which moves no clause. The first run's record was
  not committed.
- **The record was committed alone**, as `ea51576`. On #256's branch the three
  commits were `410f04e`, `7379251` and `068d65b`. Each pair has the same
  subject, the same tree and the same `git patch-id --stable`, and the GitHub
  API names #256 behind the three `main` commits.
- **Its `_env` says `git_dirty`**, for files the session's sandbox mounted in
  the repository's root, untracked. `code_dirty` is false, and the code digest,
  `3d849b1feeb3c1cd`, is the one `main` computes at `d5c8c19`, and still at the
  merge.
- **The record is [`byqueue.json`](byqueue.json).** Its five gates passed in the
  four runs it reads:
  - the listings are `doors.json`'s, rebuilt from the record with the side each
    answer declared;
  - every list is the seeded shuffle v1c showed;
  - every placement call carries its reasoning tokens;
  - every listed rule shown ceding to the gateway had that edge installed at its
    own birth;
  - the development set gives the counts the module's docstring gives of it.

**What it reads.** `doors.json`'s listings, each a round that listed a gateway,
with the side its answer declared: a *climb* above the gateway, or a *cede*
below it. For each listing, what the round gave the answer:
- **the draft**, its queue and conditions;
- **the slot**, where the gateway stands in the list. v1c shows the list in a
  shuffle seeded by the case and the round, so the slot is drawn, not chosen;
- **the precedent**, the listed rules the list shows ceding to the gateway,
  `[pierde con` it`]`, as each rule's accepted declarations render;
- **the cause** of the escalation;
- **the reasoning**, the placement call's reasoning tokens per listed rule.

Two listings of the same draft, listed the same gateway, *disagree* when one
climbs and the other cedes. **Added after the first run**: how many security
rules the list shows before the gateway, and the slot crossed with the
precedent.

### 1. The same draft goes both ways

| run | listings | climbs | pairs of the same draft | that disagree | independent draws at the run's rate |
|---|---|---|---|---|---|
| L r1, development | 78 | 5 | 309 | 26 | 37.1 |
| N r3, development | 40 | 19 | 138 | 71 | 68.8 |
| L r2 | 82 | 14 | 279 | 119 | 79.0 |
| L r3 | 107 | 10 | 841 | 114 | 142.5 |

- **The draft does not set the reading** (B1 holds, the bet). In L r2 and L r3,
  233 of the 1,120 pairs of the same draft disagree, where independent draws at
  each run's climb rate would give 221.5.
- **In N r3, `product = billing → BILLING_SPECIALIST` was listed `R0175` 17
  times, and climbed 7.**

### 2. The slot moves it

| run | the gateway before every security rule | after a security rule |
|---|---|---|
| L r1, development | 2 of 23 | 3 of 55 |
| N r3, development | 5 of 10 | 14 of 30 |
| L r2 | 8 of 25 | 6 of 57 |
| L r3 | 6 of 26 | 4 of 78 |

The listings that climbed, by where the gateway stands in the shuffled list.

- **In L r2 and L r3, the gateway listed before every security rule climbs
  nearly four times as often** (B2 fails): 14 of 51, against 10 of 135, a gap of
  0.2004 where B2 allowed 0.10.
- **The shuffle drew the slot**, so the gap is the presentation's, not the
  draft's or the round's.
- **The development runs did not show it.** In L r1 the gap was 0.0324, on five
  climbs, and in N r3 the gateway climbed about half the time wherever it stood.

### 3. The precedent too, and the two add up

| L r2 and L r3 | no rule shown ceding to the gateway | a rule shown ceding |
|---|---|---|
| the gateway before every security rule | 8 of 19 | 6 of 32 |
| after a security rule | 5 of 39 | 5 of 96 |

- **A list that shows a rule ceding to the gateway holds the answer down** (B3
  holds): 13 of the 61 listings without one climbed, and 11 of the 128 with one.
- **Within each slot the precedent lowers the rate, and within each precedent
  the slot does**: from 8 in 19 at one corner to 5 in 96 at the other. This is
  added after the first run.
- **What counts is whether any security rule comes first.** With none before
  the gateway, 14 of 54 listings climbed. With one, 1 of 41; with two or three,
  5 of 32; with four or more, 4 of 62.

### 4. Not the reasoning's amount

- **The climbs reasoned about as much per listed rule as the cedes** (B4 holds):
  a lower median of 179 tokens against 213 in L r2 and L r3. In the development
  runs, 232 against 208 in L r1, and 194 against 182 in N r3.
- **The cause leans one way**, as `doors.json` had shown. In L r2 and L r3, 21
  of the 133 listings at reported errors climbed, and 3 of the 52 at conflicts.
- **The gateway's queue is not separated from the arm.** Every keyword rule of
  another queue that L's lists showed was of `T2_TECHNICAL`. N r3's only one was
  its gateway, of `T1_GENERAL`.

### The expectation

Written in `corrections/byqueue.py`'s docstring after L r1 and N r3 were read,
and committed before the reading ran on L r2 and L r3. It is not signed, and it
is on no scoreboard.

| clause | reading | |
|---|---|---|
| B1, pairs of the same draft disagree at least half as often as independent draws would | 233 of 1,120, against 221.5 | **holds** |
| B2, the slot moves the climb rate by at most 0.10 | 14 of 51 against 10 of 135, a gap of 0.2004 | fails |
| B3, the rate with no precedent shown at least the rate with one | 13 of 61 against 11 of 128 | **holds** |
| B4, the climbs' reasoning per listed rule within a quarter of the cedes' | 179 against 213 | **holds** |

**B1, B3 and B4 hold, and B2 fails.** The bet `B1` held. `B2`, trusted most,
failed: the development runs had shown no slot effect, and the held-out runs
showed one. `B3`, trusted least, held.

### What it says

- **The reading is not the draft's.** The same draft, listed the same gateway,
  goes both ways about as often as independent draws would.
- **What the list shows moves it.** An answer that meets a security rule before
  the gateway mostly places the gateway with it. An answer whose list shows
  another rule ceding to the gateway mostly cedes too. Together they take the
  climb rate from 8 in 19 to 5 in 96.
- **The slot is the shuffle's**, so this is the round's presentation: v1c's
  seeded order decides part of which answers climb over the gateway.
- **The development set missed it.** L r1 had five climbs, and in N r3 the
  answers climbed about half the time wherever the gateway stood. The bet set on
  it held, and the clause trusted most failed on the held-out runs.

### What it does not settle

1. **Whether a round that lists the security rules first makes fewer doors.**
   v1c's shuffle puts them first in some rounds and not in others. A plan with
   calls.
2. **Why N r3's answers climb about half the time wherever the gateway stands.**
   Its gateway is of `T1_GENERAL` and its arm has no label, and one run cannot
   separate the two.

---

## Why some answers put their newborn above every rule of their list — POST-RUN

**Asked for by Sergi on 2026-11-15, after the reading above.** The reading of why
the doors declared themselves above the gateway found that most climbs still put
their newborn below every security rule of their round, and that the rest put it
above every rule of their list, the security rules included. Its *What it does
not settle*, item 2, left why. This reading asks the records, and spends
nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.above`, on 2026-11-15
in local time, from `13ce82d` with its code clean, on the branch of #259, which
is `ccef280` on `main`.
- **The development set.** L r1 and N r3 were read before the expectation was
  written: every round with what its answer declared of every listed rule, every
  placement by the two rules' queues, conditions and points and by the ticket,
  and the notes and reasoning of the seven rounds above every rule of a list that
  held a security rule. E1 to E4 read L r2 and L r3, pooled. E5 and E6 read
  N r1 and N r2, pooled, as the control.
- **Counts of every run were printed before the development set was chosen**:
  how many rounds put their newborn above every rule, how many lists held a rule
  of `SECURITY_INCIDENT` and how many of those were above every rule, and how
  many newborns were of `SECURITY_INCIDENT`, all of them above every rule. The
  module's docstring says so, and no clause reads them.
- **The commits.** `ccef280` on `main` carries the reading and its expectation,
  written before the reading ran on the other runs. Nothing was added after the
  first run. The first run's record was not committed.
- **The record was committed alone**, as `d24d351`. On #259's branch the two
  commits were `13ce82d` and `59f47e7`. Each pair has the same subject, the same
  tree and the same `git patch-id --stable`, and the GitHub API names #259
  behind both `main` commits.
- **Its `_env` says `git_dirty`**, for the files the session's sandbox mounted
  in the repository's root, untracked. `code_dirty` is false, and the code
  digest, `ff2e2076bc7bd312`, is the one `main` computes at `ccef280`, and still
  at the merge.
- **The record is [`above.json`](above.json).** Its five gates passed in all six
  runs:
  - what each answer declared, rebuilt from its rule's accepted and refused
    edges, is its placement call's `beats` and `loses_to`;
  - every listed rule is of another queue and crosses the newborn;
  - every answer declared a side against every rule of its list;
  - every list is the seeded shuffle v1c showed;
  - the development set gives the counts the module's docstring gives of it.

**What it reads.** Every round of the six runs: a born rule whose round listed
rules, with what its answer declared of each, its newborn above it or below it.
For each round, what the answer did with:
- **its whole list**, its newborn above every rule, below every rule, or some of
  each;
- **the queues put first**: the listed rules of `SECURITY_INCIDENT`, and those of
  `ONCALL_ESCALATION` for a newborn of neither queue;
- **the rules that hold its ticket**, those whose region holds the round's
  ticket, placement by placement and by the cause.

It also reads the draft's conditions, how many security rules the list held, and
two codes over the placement call's note, frozen on the development set: that
the rule is more specific, an exception or adds conditions, and that the note
names security.

### 1. What the list lacks

| run | newborn of `SECURITY_INCIDENT` | list with neither queue's rule | with a rule of `ONCALL_ESCALATION` | with a rule of `SECURITY_INCIDENT` |
|---|---|---|---|---|
| L r1, development | 8 of 8 | 30 of 68 | 1 of 22 | 2 of 170 |
| N r3, development | 14 of 14 | 26 of 56 | 3 of 27 | 5 of 217 |
| L r2 | 14 of 14 | 37 of 79 | 2 of 9 | 3 of 164 |
| L r3 | 15 of 15 | 35 of 71 | 0 of 15 | 4 of 162 |
| N r1 | 17 of 17 | 30 of 86 | 1 of 12 | 2 of 200 |
| N r2 | 20 of 20 | 33 of 74 | 1 of 9 | 3 of 203 |

The rounds that put their newborn above every rule of their list, by their
newborn's queue and what their list held. A list with a rule of
`SECURITY_INCIDENT` is counted there, whatever else it held.

- **A newborn of `SECURITY_INCIDENT` is above every rule of its list**, in every
  run: 88 of 88. These counts were printed before the development set was
  chosen, and no clause reads them.
- **A list with neither queue's rule comes out above every rule about half the
  time**: 72 of 150 in L r2 and L r3.
- **A rule of `ONCALL_ESCALATION` holds the answer down** (E2 holds). Of the
  rounds whose newborn is of neither queue and whose list held no security rule,
  70 of the 148 without an on-call rule put their newborn above every rule, and
  2 of the 24 with one, a ratio of 5.68 where E2 asked 3.
- **A rule of `SECURITY_INCIDENT` holds it down further**: 7 of the 326 rounds
  whose list held one, newborn not of that queue.

### 2. The security rules are one block

- **Every held-out round whose list held two or more security rules placed them
  as one** (E1 holds, trusted most): 228 of 228, 222 below its newborn and 6
  above. In N r1 and N r2, 333 of 334 did, and in the development set 313 of
  313.
- **The on-call rules nearly so.** Of the rounds whose list held two or more,
  newborn of neither queue, 50 of 53 placed them as one in L r2 and L r3, and 90
  of 92 in N r1 and N r2.

### 3. Above the rules that hold the ticket

| | at reported errors, rules that hold the ticket | the rest | at conflicts, rules that hold the ticket | the rest |
|---|---|---|---|---|
| L r1 and N r3, development | 1,077 of 1,139 | 5,484 of 9,824 | 369 of 454 | 2,324 of 4,220 |
| L r2 and L r3 | 813 of 833 | 3,541 of 6,900 | 502 of 615 | 2,296 of 3,996 |
| N r1 and N r2 | 1,089 of 1,204 | 6,787 of 13,059 | 202 of 236 | 586 of 1,673 |

The placements that put the newborn above the listed rule, by whether the rule's
region holds the round's ticket.

> **[ERRATUM 2026-11-16] Three cells move, read on the other side.** One answer
> in L r1, one in L r2 and one in N r1 cited rules both above, installed, and
> below, refused for the cycle the first side had closed: one rule each in L,
> six in N r1. `corrections/fall.py`'s `declared`, through which this reading
> counts, keeps the second. Kept on the first, the development set's rest at
> reported errors is 5,485 of 9,824. L r2's and L r3's rest at conflicts is
> 2,297 of 3,996. N r1's and N r2's rules that hold the ticket at reported
> errors are 1,095 of 1,204, which the line below gives as 1,089. *The
> citations on both sides*, below. No verdict moves.

- **At reported errors the answers put their newborn above nearly every listed
  rule that holds its ticket** (E3 holds): 813 of 833 in L r2 and L r3, and
  about half of the rest.
- **N does it too, without a label**: 1,089 of 1,204. At conflicts, a little
  less, in both arms.

### 4. The few above the security block

| | narrow draft against a short block | the others | four or more conditions | three or fewer | one or two security rules | three or more |
|---|---|---|---|---|---|---|
| L r1 and N r3, development | 4 of 24 | 4 of 363 | 4 of 52 | 4 of 335 | 5 of 118 | 3 of 269 |
| L r2 and L r3 | 1 of 17 | 6 of 309 | 3 of 49 | 4 of 277 | 1 of 123 | 6 of 203 |
| N r1 and N r2 | 0 of 17 | 7 of 386 | 3 of 67 | 4 of 336 | 1 of 91 | 6 of 312 |

The rounds whose list held a rule of `SECURITY_INCIDENT`, newborn not of it,
that put their newborn above every such rule. A narrow draft has four or more
conditions, and a short block one or two security rules.

- **The bet held on one round** (E4 holds, thinly): 1 of the 17 narrow drafts
  against a short block in L r2 and L r3, and 6 of the other 309, a ratio of
  3.03 where E4 asked 3.
- **In N it failed** (E6 fails, trusted least): none of the 17, and 7 of the
  other 386.
- **The cell joined a lead that held to one that reversed.** Drafts of four or
  more conditions went above the block about four times as often as the others,
  in both arms. One or two security rules did not raise it: 12 of the 14
  held-out rounds above the block had three or more. The development set's
  short blocks came from five rounds.
- **By the draft's conditions alone, it is highest at four or more and next at
  one**, in both arms. In L r2 and L r3, one condition went above the block in 2
  of 76 rounds, two in 0 of 82, three in 2 of 119 and four or more in 3 of 49.
  In N r1 and N r2, 1 of 59, 1 of 98, 2 of 179 and 3 of 67.
- **Most went above the whole list** (E5 fails in N): all 7 in L r2 and L r3,
  and 5 of the 7 in N r1 and N r2.

### 5. Two readings, read in the notes

Read after the first run, in a scratch script: the notes of the fourteen rounds
above the block in L r2, L r3, N r1 and N r2.
- **Ten are drafts of three or four conditions that read every rule by its
  conditions.** "La regla es más específica que las reglas de T2_TECHNICAL y
  SECURITY_INCIDENT porque añade condiciones de canal y tier". The keyword's
  rule has one condition.
- **Four are their queue's general rule, read as a domain**: `product = billing`
  twice in L r2, and `severity = 1` and `severity = 1, off_hours` of
  `ONCALL_ESCALATION` in N. "This rule overrides any other routing logic (e.g.,
  security, severity, tier, off-hours)"; "deben ir a guardia independientemente
  del producto, tier o si tienen palabras de seguridad".
- **The two of N above the block and not the whole list** still ceded to some
  rules. One put three rules of `ACCOUNT_MANAGER` above its newborn: "Pierde
  frente a reglas de account manager que requieren muchos tickets previos". The
  other put 25 rules of `T2_TECHNICAL`, `BILLING_SPECIALIST` and `T1_GENERAL`
  above it, which its note calls specialized product rules.
- **The codes frozen on the development set.** The note says more specific, an
  exception or added conditions in 6 of L's 7 and 5 of N's 7, and in 225 of the
  319 held-out rounds below the block in L and 299 of 395 in N. It names
  security in 4 of L's 7 and 6 of N's 7, and in 314 of 319 and 392 of 395 below
  it. The split the development set showed, 4 of 8 against 377 of 379, held in
  L and not in N.

### 6. Not by the draft

- **The drafts listed against security more than once that went above it once
  went below it at their other listings**, in every run that had one:
  `product = billing` 2 times above and 25 below in L r2; `severity = 1` of
  `ONCALL_ESCALATION` once and 7 times, a draft of four conditions of
  `T1_GENERAL` once and once in N r1; `severity = 1, off_hours` of
  `ONCALL_ESCALATION` once and 7 times in N r2.
- **The causes.** 13 of the 14 held-out rounds above the block were at reported
  errors, where 544 of the 729 rounds with a security rule were.

### The expectation

Written in `corrections/above.py`'s docstring after L r1 and N r3 were read, and
committed before the reading ran on the other runs. It is not signed, and it is
on no scoreboard.

| clause | reading | |
|---|---|---|
| E1, of the rounds whose list holds two or more security rules, at least nineteen in twenty place them as one block | 228 of 228 | **holds** |
| E2, above every rule at least three times as often without an on-call rule as with one | 70 of 148 against 2 of 24, a ratio of 5.68 | **holds** |
| E3, at reported errors, of the placements against a rule that holds the ticket, at least nine in ten above | 813 of 833 | **holds** |
| E4, above every security rule at least three times as often for a narrow draft against a short block | 1 of 17 against 6 of 309, a ratio of 3.03 | **holds** |
| E5, in N r1 and N r2, of the rounds above every security rule, at least three quarters above the whole list | 5 of 7 | fails |
| E6, in N r1 and N r2, E4's statement | 0 of 17 against 7 of 386 | fails |

**E1, E2, E3 and E4 hold, and E5 and E6 fail.** The bet E4 held on one round,
and its statement failed in N (E6, trusted least). E1, trusted most, held at
228 of 228.

### What it says

- **Above every rule of the list is mostly what the list lacks.**
  - **The answers put two queues first.** They place the rules of
    `SECURITY_INCIDENT` as one block, nearly always below their newborn, and
    those of `ONCALL_ESCALATION` nearly so.
  - **They put their newborn above the rules that hold its ticket**, with a
    label and without one.
  - **So a list with neither queue's rule often comes out above every rule**,
    about half the time in L, and a newborn of `SECURITY_INCIDENT` always.
- **The few above the security block read the list another way.** Most are
  drafts of three or four conditions that call themselves more specific than
  rules of one condition, as the round's `beats`, an exception, invites. The
  rest are their queue's general rule, read as a domain that wins regardless.
  Most then put their newborn above the whole list.
- **The draft's conditions raise it; the block's length does not.** The cell the
  bet drew joined the two, and held one round in L and none in N.
- **The reading is the answer's, not the draft's.** The same draft went above
  the block once and below it at its other listings.

### What it does not settle

1. **What makes one answer read the list by its conditions and another by its
   queues**, when the same draft does both. The draft's conditions raise it, and
   leave it rare. Whether the list's order moves it, as it moved the reading of
   the gateway, is not read. Free on the records.
   **[NOTE 2026-11-15] Read POST-RUN, below: not the order, and not one
   reading.** The shuffle's order and the precedent shown did not tell the
   climbs from the cedes. The cedes weigh the queue. The climbs mostly count
   conditions, but two rank on-call above security, and some never read a
   security rule on its own. *What makes an answer read the list by its
   conditions*.
2. **Whether a round that defined `beats` by the queue that should decide the
   shared tickets, and not as an exception, would keep the narrow drafts below
   the security block.** A plan with calls.

---

## What makes an answer read the list by its conditions — POST-RUN

**Asked for by Sergi on 2026-11-15, after the reading above.** It found that the
answers place the rules of `SECURITY_INCIDENT` as one block. The few above it
read the list by its conditions, or are their queue's general rule read as a
domain, and the same draft went both ways. Its
*What it does not settle*, item 1, left what makes one answer read the list by
its conditions and another by its queues, and asked whether the list's order
moves it. This reading asks the records, and spends nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.conditions`, on
2026-11-15 in local time, from `a8ca66e` with its code clean, on the branch of
#261, which is `f33321e` on `main`.
- **The development set.** L r1 and N r3 were read before the expectation was
  written. That covered every round whose list held a security rule: its side,
  its list's opening, what the list showed, its reasoning tokens, and its
  passages about the security rules, coded for several candidates. C1 to C4
  pool L r2, L r3, N r1 and N r2, the two arms together, and C5 reads each arm
  apart.
- **The commits.** `663e2b1` on `main` carries the reading and its expectation,
  written before the reading ran on the other runs. `f33321e` carries the part
  added after the first run, which moves no clause. The first run's record was
  not committed.
- **The record was committed alone**, as `8662e3a`. On #261's branch the three
  commits were `798201c`, `a8ca66e` and `04fb81c`. Each pair has the same
  subject, the same tree and the same `git patch-id --stable`, and the GitHub
  API names #261 behind the three `main` commits.
- **Its `_env` says `git_dirty`**, for the files the session's sandbox mounted
  in the repository's root, untracked. `code_dirty` is false, and the code
  digest, `2b3e6ca0a22c99ae`, is the one `main` computes at `f33321e`, and still
  at the merge.
- **The record is [`conditions.json`](conditions.json).** Its five gates passed
  in all six runs:
  - the rounds and their sides against the security rules are `above.json`'s;
  - every list is the seeded shuffle v1c showed;
  - every placement call carries its reasoning and its reasoning tokens;
  - every listed rule shown ceding to a listed security rule had that edge
    installed at its own birth;
  - the development set gives the counts the module's docstring gives of it.

**What it reads.** Every round whose list held a rule of `SECURITY_INCIDENT`,
newborn not of it, by its side: a *climb* above every such rule, a *cede* below
every one. For each, what the round gave the answer and what the answer spent:
- **the order**: whether v1c's seeded shuffle opened the list with a security
  rule, against what chance gives;
- **the precedent**: the listed rules shown ceding to a listed security rule,
  `[pierde con` it`]`, and climbing over one, `[gana a` it`]`;
- **the reasoning**: the placement call's reasoning tokens, against the cedes'
  lower median at the same length of list, binned 1-3, 4-8, 9-20, 21-50 and 51
  or more;
- **the account**: the lines of the reasoning that name a listed security rule,
  each with the two lines after it, coded for priority and for conditions.

**Added after the first run**: whether every such line enumerates the list,
naming at least three of its rules and at least half.

### 1. Not the order, nor the precedent

| | climbs | lists opened with a security rule | the shuffle gives | cedes | lists opened with a security rule | the shuffle gives |
|---|---|---|---|---|---|---|
| L r1 and N r3, development | 8 | 2 | 2.80 | 379 | 130 | 128.78 |
| L r2, L r3, N r1 and N r2 | 14 | 3 | 4.33 | 714 | 249 | 259.57 |

- **The shuffle opened the climbs' lists with a security rule about as often as
  chance would** (C1 holds): 3 of the 14 held-out climbs, where it gives 4.33.
  The cedes' opened so 249 times, where it gives 259.57.
- **A rule shown climbing over a security rule did not raise it**: 1 of the 67
  held-out rounds whose list showed one climbed, and 13 of the 662 without.
- **Nor did the precedent of rules shown ceding**, at a given length of list.
  At lists of 21 to 50, 1 of the 16 rounds with no rule shown ceding climbed, 1
  of the 106 with under a third of the list shown so, and 3 of the 99 with a
  third or more.

### 2. The climbs reasoned less, short of the bet

- **9 of the 14 held-out climbs spent fewer reasoning tokens than the cedes'
  lower median at their length of list** (C2 fails, the bet): short of two
  thirds. In the development set, 2 of 3 and 5 of 5, each against its own run's
  cedes.
- **Not in L** (C5 fails): 4 of 7 in L r2 and L r3, and 5 of 7 in N r1 and N r2.

### 3. The account: the cedes weigh the queue

| | climbs | conditions, never priority | priority | cedes | conditions, never priority | priority |
|---|---|---|---|---|---|---|
| L r1 and N r3, development | 8 | 5 | 3 | 379 | 18 | 354 |
| L r2, L r3, N r1 and N r2 | 14 | 6 | 5 | 714 | 26 | 675 |

The rounds whose passages about the security rules carry each code.

- **The cedes' passages weigh the queue** (C4 holds, trusted most): 26 of the
  714 held-out cedes' speak of conditions and never of priority, and 675 name
  priority.
- **Fewer than half the climbs' passages speak only of conditions** (C3 fails):
  6 of the 14.

### 4. The climbs are not one reading

Read after the first run, in a scratch script: the passages of the fourteen
held-out climbs.
- **Six read every rule by its conditions**, and their passages never name
  priority, as C3 counted.
- **Two read it so and claim priority for their own rule**, or name the task:
  "it's appropriate to prioritize it over the more general rules".
- **The two drafts of `ONCALL_ESCALATION` read by the queue, and rank on-call
  above security**: "Given the critical nature, I think ONCALL_ESCALATION should
  take precedence because it's the immediate response team".
- **One weighed security and climbed all the same.**
- **Three carry neither code.** Their passages about the security rules are the
  list's identifiers, enumerated: "Ahora, debo listar todos los IDs de las
  reglas que se solapan ... Pondré todas en beats". Two are `product = billing`
  in L r2.

**The reasoning splits by the same line.** The five that enumerate the list or
read on-call above security all spent fewer tokens than their length's median.
Of the eight that read by conditions, four did. The one that weighed security
did not.

### 5. The security rules named only in the list — added after the first run

| | climbs | named only in lines that enumerate the list | cedes | so named |
|---|---|---|---|---|
| L r1 and N r3, development | 8 | 3 | 379 | 40 |
| L r2, L r3, N r1 and N r2 | 14 | 3 | 714 | 78 |

- **About twice as often among the climbs**: 3 of the 14 held-out, and 78 of
  the 714 cedes.
- **The measure takes an enumeration written on one line.** It caught one of
  the three passages read as enumerations, and two others. It misses a list
  written one rule to a line, as one of L r2's billing rules wrote it.

### The expectation

Written in `corrections/conditions.py`'s docstring after L r1 and N r3 were
read, and committed before the reading ran on the other runs. It is not signed,
and it is on no scoreboard.

| clause | reading | |
|---|---|---|
| C1, of the climbs, the lists opened with a security rule at least half what the shuffle gives | 3, where it gives 4.33 | **holds** |
| C2, at least two thirds of the climbs spent fewer reasoning tokens than the cedes at their length | 9 of 14 | fails |
| C3, of the climbs, at least half speak of conditions and never of priority | 6 of 14 | fails |
| C4, of the cedes, at most one in ten do | 26 of 714 | **holds** |
| C5, C2's statement in each arm | 4 of 7 in L, 5 of 7 in N | fails |

**C1 and C4 hold, and C2, C3 and C5 fail.** The bet C2 fell short, at 9 of 14
against two thirds. C4, trusted most, held. C5, trusted least, failed in L.

### What it says

- **What the round showed does not set it.** The shuffle's order and the
  precedent of rules ceding to security or climbing over it did not tell the
  climbs from the cedes.
- **The cedes weigh the queue**, nearly every one of them.
- **The climbs are several readings, not one.** Most count conditions. The two
  drafts of `ONCALL_ESCALATION` weigh the queue and rank on-call first. Three
  never read a security rule on their own, and put the whole list in `beats`.
- **They reasoned less, but not as the bet said.** The answers that enumerated
  the list or ranked on-call first reasoned less than the cedes. The ones that
  counted conditions reasoned about as much.

### What it does not settle

1. **Why two drafts of `ONCALL_ESCALATION` rank on-call above security**, when
   34 of the queue's 36 held-out rounds against security cede to it. The catalogue's line calls
   on-call the queue of incidents that cannot wait. Free on the records.
2. **Whether a round that asked for each listed rule's side apart would leave
   fewer answers that place the whole list in one declaration.** A plan with
   calls.

## Why L loses `ONCALL_ESCALATION` — POST-RUN

**Proposed by the agent and asked for by Sergi on 2026-11-15, after the reading
above.** Stage C found L's final bases recalling 0.4, 0.4476 and 0.4341 of the
rarest queue over the space, where N's recall 1, 0.7333 and 1 (`CR-f` refuted).
Its *What Stage C does not settle*, item 1, left which rules decide the points L
loses, and from which labels they were drafted. *Why the loop's share of the
space peaked and fell* had read `SECURITY_INCIDENT`'s points right at each L
run's peak, and none of this queue's. This reading asks the records, and spends
nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.oncall`, on
2026-11-15 in local time, from `24753d8` with its code clean, on the branch of
#263, which is `8292de4` on `main`.
- **The commits.** `4de8f8b` on `main` carries the reading and its expectation,
  written before the reading ran. `863666a` and `8292de4` carry the two parts
  added after the first run, which move no clause. The first run's records were
  not committed.
- **The record was committed alone**, as `afaede6`. On #263's branch the four
  commits were `5f06316`, `2993e46`, `24753d8` and `4cf0f8b`. Each pair has the
  same subject, the same tree and the same `git patch-id --stable`, and the
  GitHub API names #263 behind the four `main` commits.
- **Its `_env` says `git_dirty`**, for the files the session's sandbox mounted
  in the repository's root, untracked. `code_dirty` is false, and the code
  digest, `c19988c1a4a6ee4e`, is the one `main` computes at `8292de4`, and still
  at the merge.
- **The record is [`oncall.json`](oncall.json).** Its 72 gates passed in all
  six runs:
  - `channel/oncall.py`'s five for the queue and `channel/lost.py`'s four for
    `SECURITY_INCIDENT`, gate 1 of each holding the final base's right points
    to Stage C's recall;
  - the takers partition the points another queue decides, and every report
    names its ticket's true queue;
  - the last losses partition what was right once, the replay is the final
    base, and the peak and the points lost at it are `fall.json`'s;
  - each replay is the one `fall.json`, `paths.json` or `carry.json` keeps.
- **One figure was seen before the expectation was written**, and the
  docstring says so: after L r1's peak, the refused right sides against rules of
  the queue weigh 6,300 pair-points in `paths.json`. O1 and O6 rest on it.

**What it reads.** `channel/oncall.py`'s reading of the queue, and
`channel/lost.py`'s of `SECURITY_INCIDENT`, in every run of both arms: each lost
point by the way it was lost. And three parts of its own:
- **who takes the points**: every rule deciding a lost point that one other
  queue decides, with its birth, its ticket's governing rule and the queue the
  report named;
- **when they were lost**: never right after any birth, or at the last loss,
  with `fall.py`'s kind, set against the run's peak;
- **what the levers give back**: the queue's points right in the final base of
  three replays. One installs each birth's losses before its wins, one uses the
  engine that refuses a cycle only where it is, and one leaves out the doors.

**Added after the first run**: the rule that had decided each taker's ticket,
the edges between each taker and the queue's rules, and what each replay turns
right by the way the record lost it.

### 1. Written whole, and lost two ways

| run | lost | contested | outranked | by an edge | by containment | unwritten or impasse | rules of the queue holding `H04`'s part whole |
|---|---|---|---|---|---|---|---|
| L r1 | 3,780 | 1,680 | 2,100 | 1,260 | 840 | 0 | 7 |
| L r2 | 3,480 | 960 | 2,520 | 2,100 | 420 | 0 | 1 |
| L r3 | 3,565 | 1,900 | 1,665 | 1,560 | 105 | 0 | 2 |
| N r1 | 0 | | | | | | 13 |
| N r2 | 1,680 | 0 | 1,680 | 420 | 1,260 | 0 | 10 |
| N r3 | 0 | | | | | | 13 |

- **No lost point is unwritten, in any run.** Every base of either arm holds
  rules of the queue covering `H04`'s part and `H05`'s whole. The label did not
  narrow the queue.
- **What L loses, it loses beside other queues' rules or below them.** Of the
  three runs' 10,825 lost points, 4,540 are contested conflicts and 6,285 are
  outranked. Every conflict is contested.
- **N r2 is the one N run that loses some**: 1,680 of `H04`'s points, to
  `R0023` of `T3_ENGINEERING`, `severity = 1 ∧ off_hours = False ∧
  has_security_keyword = False`, born at case 45 at an impasse. They were never
  right.

### 2. Born at the tickets of the layer below

| run | rules of the queue | born at its own tickets | the first: born at | its ticket | its points of the queue |
|---|---|---|---|---|---|
| L r1 | 19 | 2 | case 58, an impasse | `H07`'s | 6,300 |
| L r2 | 2 | 0 | case 45, an impasse | `H08`'s | 6,300 |
| L r3 | 4 | 2 | case 45, an impasse | `H08`'s | 6,300 |
| N r1 | 24 | 0 | case 45, an impasse | `H08`'s | 6,300 |
| N r2 | 21 | 0 | case 74, a reported error | `H08`'s | 6,300 |
| N r3 | 24 | 0 | case 31, an impasse | `H13`'s | 1,100 |

- **The queue was first written at a ticket of another queue, in every run.**
  Five of the six firsts were born at a severity-1 ticket of `H07` or `H08`,
  `T3_ENGINEERING`'s or `T2_TECHNICAL`'s, and none at a report that named a
  queue. Those five cover the whole queue: L r1's first is `R0027`, `severity =
  1 ∧ has_security_keyword = False`, and L r2's is `R0020`, `severity = 1`.
- **So the queue's rule holds the layer below it too**, as the catalogue's line
  reads severity 1: critical incidents that cannot wait.
- **N wrote it again at its reported errors.** 20 to 22 of each N run's rules of
  the queue were born at reported errors, none at a ticket of the queue. Its
  reports name no queue.
- **L wrote it at its own tickets twice in two runs, and never in L r2.**

### 3. Contested after the peak, outranked before it

| run | lost at the peak | contested | lost before it | outranked |
|---|---|---|---|---|
| L r1 | 2,100 | 1,260 | 1,680 | 1,260 |
| L r2 | 2,220 | 960 | 1,260 | 1,260 |
| L r3 | 1,360 | 880 | 2,205 | 1,185 |

- **What fell after the peak was mostly left contested**: 3,100 of 5,680 (O1
  holds), though under half in L r2, 960 of 2,220.
- **What was lost before it was mostly outranked**: 3,705 of 5,145 (O2 holds).
- **Nearly every lost point had been right after some birth.** 420 of L r1's
  never were, and none of L r2's or L r3's.

### 4. The corrections of the layer below take it

| run | outranked | by `T3_ENGINEERING` | by `T2_TECHNICAL` | by other queues | only by corrections | only by rules born at tickets of `H06` to `H08` |
|---|---|---|---|---|---|---|
| L r1 | 2,100 | 1,260 | 840 | 0 | 2,100 | 2,100 |
| L r2 | 2,520 | 1,680 | 840 | 0 | 2,520 | 2,100 |
| L r3 | 1,665 | 1,020 | 125 | 520 | 1,185 | 545 |

- **By the corrections** (O4 holds): 5,805 of 6,285, every one of L r1's and L
  r2's.
- **Born at the layer's tickets** (O5 holds): 4,745 of 6,285, though only 545 of
  L r3's 1,665. L r3's others were born at tickets of `H10`, `H13`, `H14` and
  `H17`, one of them at a conflict, with no label.
- **Mostly by an edge** (O3 holds): 4,920 of 6,285.
- **Each is a slice of severity 1 by product, and leaves the queue's tiers in.**
  - In L r1, two take 840 each: `R0129` of `T2_TECHNICAL`, `product = mobile ∧
    severity = 1 ∧ off_hours = True ∧ customer_tier ∈ {pro, business,
    enterprise} ∧ has_security_keyword = False`, and `R0266` of
    `T3_ENGINEERING`, `severity = 1 ∧ product = dashboard ∧ customer_tier ∈
    {business, enterprise} ∧ has_security_keyword = False`.
  - In L r2, `R0222` of `T3_ENGINEERING`, `severity = 1 ∧ product = api ∧
    has_security_keyword = False`, takes 1,260, and `R0145` of
    `T2_TECHNICAL`, the same with `product = billing`, takes 840.
  - In L r3, `R0202`, with `R0222`'s conditions, takes 540.
- **The policy gives those slices to the layer only below `H04` and `H05`.** A
  slice that keeps the enterprise tier, or business off hours, takes the queue's
  tickets of its product with it.

### 5. The rule that erred was the queue's — added after the first run

| run | taken points, each taker counted | of takers whose ticket a rule of the queue had decided |
|---|---|---|
| L r1 | 2,100 | 1,680 |
| L r2 | 2,940 | 2,100 |
| L r3 | 1,905 | 125 |

- **In L r1 and L r2 the takers corrected the queue's own rule.** The rule that
  had decided their tickets wrongly was a rule of the queue: `R0027`, or
  `R0179`, the same conditions born at a conflict at case 1114, in L r1; and
  `R0135`, `severity = 1 ∧ off_hours = True`, in L r2. The report named the
  layer's queue, and the correction won over the rule that erred.
- **In L r3 they mostly corrected rules of `T2_TECHNICAL` and
  `T3_ENGINEERING`.**
- **Their own answers' edges against the queue are not one story.**
  - L r2's two largest each declared a win over a rule of the queue, installed.
  - L r1's `R0129` is nested in the rule that erred, and takes its points by
    containment, with no edge.
  - L r1's `R0266` declared itself below the queue's rules eleven times, every
    one refused for a cycle.

### 6. Installing losses first gives back the contested, and only them

| run | contested | losses first | where the cycle is | without the doors |
|---|---|---|---|---|
| L r1 | 1,680 | 1,260 | 0 | 0 |
| L r2 | 960 | 960 | 440 | 0 |
| L r3 | 1,900 | 1,900 | 0 | 0 |

- **Installing each birth's losses first gives back 4,120 of the queue's
  points** (O6 holds), against the 5,680 lost at the peak. It turns none wrong.
- **Every point any replay turns right was contested in the record, in both
  queues, and none outranked.** For `SECURITY_INCIDENT` the losses first give
  back 24,290, 26,355 and 600 in L's runs, and 7,080 in N r3: each run's
  contested points exactly.
- **The engine that refuses only where the cycle is gives back little of the
  queue**: 440 in L r2, turning 640 right and 200 wrong, and none in L r1 or L
  r3.
- **Without the doors nothing comes back for the queue.** The doors climb over a
  gateway in the keyword's region, where the queue has no point.
- **The outranked points stay outranked under every replay.**

### 7. The rest of `SECURITY_INCIDENT`'s

| run | lost before the peak | in a conflict | contested | outranked | by `T2_TECHNICAL` |
|---|---|---|---|---|---|
| L r1 | 17,300 | 11,480 | 8,900 | 5,820 | 5,700 |
| L r2 | 1,680 | 1,545 | 0 | 135 | 30 |
| L r3 | 16,800 | 2,573 | 0 | 14,227 | 11,927 |

- **Under half went to `T2_TECHNICAL`** (O7 fails): 17,657 of 35,780.
- **In L r1 two thirds were left in conflicts.** The gateway `R0061`,
  `has_security_keyword = True ∧ severity = 4`, born at a reported ticket of
  `H03`, took 5,660 by containment.
- **In L r3 the gateway, born at case 19, took most of them.** `R0016`,
  `has_security_keyword = True ∧ severity ≥ 3`, born at a reported ticket of
  `H03`, decides 11,927 of them by containment. None of the 16,800 was ever
  right.

### The expectation

Written in `corrections/oncall.py`'s docstring before the reading ran, and
committed before it. It is not signed, and it is on no scoreboard.

| clause | reading | |
|---|---|---|
| O1, at least half of the queue's points lost at the peak are contested | 3,100 of 5,680 | **holds** |
| O2, at least half of those lost before the peak are outranked | 3,705 of 5,145 | **holds** |
| O3, at least half of the outranked are outranked by an edge | 4,920 of 6,285 | **holds** |
| O4, at least half of the taken are decided only by rules born at a reported error | 5,805 of 6,285 | **holds** |
| O5, at least half are decided only by rules born at tickets of `H06` to `H08` | 4,745 of 6,285 | **holds** |
| O6, installed losses first, the replay gives back half as many as were lost at the peak | 4,120 against 5,680 | **holds** |
| O7, at least half of `SECURITY_INCIDENT`'s points lost before the peak are decided by `T2_TECHNICAL` | 17,657 of 35,780 | fails |

**O1 to O6 hold, and O7 fails.** The bet, O2, held. O1, trusted most, held,
though under half in L r2. O3, trusted least, held. The drafter expected the
corrections to be their queue's general rule, as *Why the first call writes
broad corrections* found. They were slices of severity 1 by product.

### What it says

- **Neither arm ever learned the rarest queue from its own tickets.** Its first
  rule, in every run, was the catalogue's reading of severity 1, written at a
  ticket of the layer below. It covers the queue whole, and the layer too.
- **N keeps the queue because nothing corrects that rule.** Its reports name no
  queue, and at them its proposer wrote the queue again, twenty times a run or
  more. `T3_ENGINEERING`'s recall is 0 in two N runs of three.
- **L corrects the rule and overshoots it.** Its reports name the layer's queue,
  and each correction is a slice of severity 1 by product that keeps the
  queue's tiers. It wins over the rule that erred, mostly by an edge, and takes
  the queue's tickets of its product.
- **What is left contested comes back by order, and what is outranked does
  not.** In both queues, installing each birth's losses first gives back the
  contested points, and no replay gives back an outranked one.
- **So the rarest queue is lost where L learns the layer below it.** The levers
  read so far change what the engine refuses, and the outranked part is what
  the corrections were placed to win.

### What it does not settle

1. **Why a correction at the layer's ticket keeps the queue's tiers**, when the
   ticket's tier is in the prompt. The policy gives the layer no enterprise
   ticket at severity 1, and no business ticket off hours. The first calls'
   reasoning is in the records. Free on the records.
2. **Whether a first call shown the rule that erred would write the correction
   as an exception that leaves the queue's tiers out.** That is the lever *Why
   the first call writes broad corrections* named. A plan with calls.
3. **Whether a catalogue line that bounds the queue by tier would keep the first
   call from writing it at the layer's tickets.** A plan with calls, and a new
   text.
   **[NOTE 2026-11-15] Read in part POST-RUN, below.** Compiled at once, the
   same labels lose the queue where no label names it. The catalogue names no
   tier for the queue, and the prose of level 2 does. *What the at-once asks
   wrote for `ONCALL_ESCALATION`*.
4. **Why 420 of L r1's contested points do not come back with losses first.**
   Free on the records.

## What the at-once asks wrote for `ONCALL_ESCALATION` — POST-RUN

**Proposed by the agent and asked for by Sergi on 2026-11-15, after the reading
above.** It found L's loop writing the rarest queue whole at the layer below it,
and losing it to corrections of that layer that keep the queue's tiers. Two
accounts fit. Either level 1's catalogue names no tier for the queue, so no call
can keep its tiers. Or the loop's shape, one ticket at a time, loses what the
labels carry together, since the same labels compiled at once decide far more of
the space (`CR-d` holds). The at-once asks were paid for in Stage B. This reading
reads them again, for the queue and its layer, and spends nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.layer`, on
2026-11-15 in local time, from `5e15c43` with its code clean, on the branch of
#265, which is `0e72e6e` on `main`.
- **The commits.** `c534c9d` on `main` carries the reading and its expectation,
  written before the reading ran. `0e72e6e` carries the part added after the
  first run, which moves no clause. The first run's record was not committed.
- **The record was committed alone**, as `c2de2bc`. Its message says A1 fell
  below the loop at some checkpoint of every run. It fell below in L r2 and L
  r3, and never in L r1.
- **On #265's branch the three commits were `264010b`, `5e15c43` and
  `9302837`.** Each pair has the same subject, the same tree and the same
  `git patch-id --stable`, and the GitHub API names #265 behind the three
  `main` commits.
- **Its `_env` says `git_dirty`**, for the files the session's sandbox mounted
  in the repository's root, untracked. `code_dirty` is false, and the code
  digest, `f0e1e3d4b07d05d2`, is the one `main` computes at `0e72e6e`, and still
  at the merge.
- **The record is [`layer.json`](layer.json).** Its 16 gates passed:
  - each L session's labels are its run's reported errors, and each ask's are
    the first ones, as many as its checkpoint; the prior's carry none;
  - each chosen answer, installed, gives the share of the space and the
    installation summary `score.json` keeps for it, in L's sessions and the
    prior's;
  - each loop base after a checkpoint's label gives the share `score.json`
    keeps;
  - the readings partition in every base, and the layer is the first match of
    `H06`, `H07` and `H08`.
- **The labels' make-up was counted before the expectation was written**, and
  the docstring says so.

**What it reads.** Every at-once answer Stage C read, installed as `CR-d` reads
it, beside the loop's base after the same label:
- three asks at each of L's checkpoints, at 10, 20, 40, 80 and 160 labels and at
  all of them, and the prior's five asks with no label;
- in each base, the queue's points by `channel/lost.py`'s ways, and the layer:
  the 10,500 points of severity 1, outside the keyword, that are not the queue's,
  `H06`'s, `H07`'s and `H08`'s;
- the queue's rules, and whether they name `customer_tier`.

**Added after the first run**: each label of the queue with its ticket, and how
many times each answer's reasoning writes `ONCALL_ESCALATION`.

### 1. At once the queue goes, unless a label names it

The median of each checkpoint's three answers, and the loop's base after the
same label:

| run | labels | of the queue | of the layer | at once: the queue | at once: the layer right | the loop: the queue | the loop: the layer right |
|---|---|---|---|---|---|---|---|
| L r1 | 10 | 0 | 0 | 1 | 0 | 0.6 | 0.04 |
| | 20 | 0 | 1 | 2/3 | 0.32 | 0.6 | 0.12 |
| | 40 | 1 | 2 | 1 | 0.48 | 0.8 | 0.1962 |
| | 80 | 1 | 5 | 2/3 | 0.84 | 0.4984 | 0.3162 |
| | 160 | 1 | 12 | 2/3 | 0.76 | 0.5333 | 0.36 |
| | 216, all | 1 | 17 | 2/3 | 1 | 0.4 | 0.44 |
| L r2 | 10 | 0 | 2 | 2/3 | 0.36 | 0.8 | 0.52 |
| | 20 | 0 | 2 | 2/3 | 0.2171 | 0.8 | 0.52 |
| | 40 | 0 | 2 | 2/3 | 0.2895 | 0.6984 | 0.52 |
| | 80 | 0 | 6 | 0 | 0.4 | 0.6 | 0.4571 |
| | 160 | 0 | 14 | 0 | 0.84 | 0.6 | 0.72 |
| | 209, all | 0 | 15 | 0 | 0.76 | 0.4476 | 0.5581 |
| L r3 | 10 | 0 | 0 | 1 | 0 | 0 | 0 |
| | 20 | 0 | 2 | 2/3 | 0.32 | 0.7833 | 0.18 |
| | 40 | 0 | 3 | 0 | 0.8095 | 0.5833 | 0.38 |
| | 80 | 0 | 4 | 0 | 0.44 | 0.2913 | 0.5 |
| | 160 | 0 | 9 | 0 | 0.76 | 0.7103 | 0.56 |
| | 235, all | 0 | 12 | 0 | 0.6 | 0.4341 | 0.76 |

- **In L r2 and L r3 no label names the queue, and at once it is gone.** From 80
  labels in L r2, and 40 in L r3, the median answer recalls none of it. At all
  their labels, none of the six answers writes a rule of the queue (A2 and A4
  fail).
- **In L r1 one label names it, and at once keeps 2/3 of it.**
- **The loop keeps more of it than at once in L r2 and L r3** (A1 fails), 0.4476
  and 0.4341 at all labels. Its rule of the queue was born before the labels,
  and stays.
- **At once learns the layer** (A3 holds): at all labels it decides right 1,
  0.76 and 0.6 of it. That is more than the loop in L r1 and L r2, and less in L
  r3.

### 2. Without a label, the catalogue's reading

The five prior answers write one rule of the queue each:
- three over severity 1, alone or outside the keyword. They recall the whole
  queue and take the whole layer as the queue;
- two over severity 1 off hours. They recall 2/3 of the queue, and take 4,200 of
  the layer's points.

**The median takes the whole layer as the queue** (A5 holds), and recalls the
whole queue (A6 holds). It is the reading every loop's first rule of the queue
wrote.

### 3. What the labels say, and the answers read — added after the first run

- **L r1's one label of the queue is a ticket of `H05`**, case 257: severity 1,
  business, off hours, `dashboard`.
- **Its answers wrote the queue off hours.** At all labels:
  - one wrote `severity = 1 ∧ customer_tier ∈ {business, enterprise} ∧
    off_hours = True`;
  - one wrote the same as two rules, one per tier;
  - one wrote the label's own combination, which recalls 1/15.

  None wrote `H04`'s enterprise tickets in hours, a third of the queue.
- **At all of L r2's and L r3's labels, each answer's reasoning writes the
  queue's identifier one to three times.** Most of those passages note that no
  label names the queue, and leave it out:
  - "ONCALL_ESCALATION for critical? We haven't seen ONCALL_ESCALATION in
    corrections. Possibly for severity 1 with off_hours? But no examples. So we
    may not need it." (L r2, the first ask);
  - "No ONCALL_ESCALATION appears in corrections, so maybe it's for specific
    cases not shown." (L r3, the third).
- **Some guess it would be severity 1 off hours**, as two of the prior's five
  wrote it: "critical incidents outside hours" (L r3, the second).

### The expectation

Written in `corrections/layer.py`'s docstring before the reading ran, and
committed before it. It is not signed, and it is on no scoreboard.

| clause | reading | |
|---|---|---|
| A1, at every checkpoint of each L run, at once recalls at least as much of the queue as the loop | at every checkpoint of L r1, at none of L r2's, and at L r3's only at 10 labels | fails |
| A2, at all labels, at once recalls at least 9/10 of the queue, in each L run | 2/3, 0 and 0 | fails |
| A3, at all labels, at once decides right at least half of the layer, in each L run | 1, 0.76 and 0.6 | **holds** |
| A4, at all labels, at least two of three answers write a rule of the queue naming the tier | 3, 0 and 0 | fails |
| A5, without a label, the median prior answer takes at least half of the layer as the queue | all of it | **holds** |
| A6, without a label, the median prior answer recalls at least 9/10 of the queue | all of it | **holds** |

**A3, A5 and A6 hold, and A1, A2 and A4 fail.** The bet, A2, failed. A5, trusted
most, held. A4, trusted least, failed, though not as the drafter feared: L r2's
and L r3's answers wrote no rule of the queue at all.

### What it says

- **For the rarest queue, the loss is information, not shape.** Compiled at
  once, the same labels lose the whole queue in the two runs whose labels never
  name it. In the run whose labels name it once, they keep 2/3.
- **The layer's labels take the catalogue's reading away, and nothing puts the
  queue back.** Without a label, the catalogue writes the queue over severity
  1, the layer with it. With a few of the layer's tickets labelled, the answers
  stop writing the queue, and say why: no correction names it.
- **One label of the queue is read off hours.** It was a ticket of `H05`, and
  the catalogue's line, incidents that cannot wait for the next shift, reads so
  too.
- **So the loop keeps more of the rarest queue than at once.** It keeps what is
  left of its first rule, an error the corrections did not reach.
- **Neither shape gets the queue's tiers from level 1.** The catalogue does not
  name them, and the labels name the queue once in three runs. The prose of
  level 2 names them: a critical ticket of an enterprise client calls the on-call
  team, and of a business client only off hours.

### What it does not settle

1. **Whether the prose of level 2 keeps the queue at once, on the same labels.**
   The at-once asks are asks only, so this costs cents. A plan with calls.
2. **Whether a label of the queue in hours would complete it at once.** No run's
   labels hold one. A plan with calls.
3. **Why L r3's at-once answers decide less of the layer than its loop.** Free on
   the records.

## Shape or order — POST-RUN

**Proposed by the agent and asked for by Sergi on 2026-11-16, after the reading
above.** Compiled at once, L's labels give a base far better than the loop's
(`CR-d` holds). Two accounts fit:
- **shape.** The loop's rules are worse than an answer written whole;
- **order.** They are as good, and the loop orders them worse: by containment,
  by the edges it declared one birth at a time, and by what the engine refused.
For the rarest queue the reading above found information. For the rest of the
space no reading had separated the two. The replays of *Why the loop's share of
the space peaked and fell* and *How much of the fall the doors carry* keep the
loop's own declarations. Installing each base in the other's order is not
defined, since the two are different rules. This reading asks instead what each
set of rules decides in the best order rung 2's engine can install, and spends
nothing.

**The orders rung 2's engine can install.** The engine lets a rule strictly
inside another beat it wherever both match, so it can install an order as
written when every rule strictly inside another comes before it. Installed as
`CR-d` installs an answer, such an order closes no cycle, and the engine decides
each point by the order's first rule that matches it. **No base of the same
rules decides right more than the best such order**: a base's own graph,
completed into one such order, decides every point the base decides as the base
does.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.shape`, on
2026-11-16 in local time, from `770f4dd` with its code clean, on the branch of
#267, which is `7929328` on `main`. It ran in three processes, one for each L
run.
- **The commits.** `cf71953` on `main` carries the reading and its expectation,
  written before the reading ran. `7929328` carries the part added after the
  first run, which moves no clause. The first run's record was not committed.
- **The record was committed alone**, as `82294e7`.
- **On #267's branch the three commits were `b13930c`, `770f4dd` and
  `9629c84`.** Each pair has the same subject, the same tree and the same
  `git patch-id --stable`, and the GitHub API names #267 behind the three
  `main` commits.
- **Its `_env` says `git_dirty`**, for the files the session's sandbox mounted
  in the repository's root, untracked. `code_dirty` is false, and the code
  digest, `36b0735352d7dde6`, is the one `main` computes at `7929328`, and still
  at the merge.
- **The record is [`shape.json`](shape.json).** Its 16 gates passed:
  - **the search found the hidden policy's optimum**, all 134,400 points, from
    the 64 declared random starts alone. 11 of them found it, the first at start
    4;
  - each L run's final base and its three at-once answers at all labels are
    Stage C's;
  - every order read installs into a fresh rung 2 engine and closes no cycle,
    and the engine and first match each give it the share the search reckons;
  - completing a base loses nothing, and no order decides more than its rules'
    bound;
  - where a bound falls short, its three ways partition the points it leaves.

**The search.** Rung 3's declared optimizer: moves and swaps, strict
improvement only, from 64 random starts of seed 17. It is kept to the orders the
engine can install. A move or a swap that would put a rule after one strictly
around it is skipped, and each random start is first repaired. Where
containment is silent it is rung 3's search, move for move. It searches the
contested points only, where the rules undefeated by containment carry more than
one queue.

**What it reads.** Each L run's final base, five ways:
- **the record**: `CR-d`'s `space(B)`;
- **completed**: its own graph completed into one order, otherwise by birth, so
  its conflicts go to the rule born first;
- **by its labels**: the completed order, searched from there alone on the
  run's labels, the reported errors with their true queues. It is what a loop
  that reordered its base on its own labels would keep;
- **with the truth**: the best order the search finds over the space, the
  completed order first among its 65 starts;
- **the bound**: the points some rule undefeated by containment gets right. No
  order decides more.

Each run's three at-once answers at all labels are read four ways: the record,
completed in their list's order, with the truth, and the bound.

**Added after the first run**: where each final base's bound falls short, by
how its points are lost, the rules that hold them, and what the median at-once
answer decides right among them.

### 1. In L r1 and L r2 the loop's rules hold more than at once, and in L r3 they do not

The share of the space:

| run | at once | the loop: record | completed | by its labels | with the truth | bound |
|---|---|---|---|---|---|---|
| L r1 | 0.7584 | 0.5647 | 0.5983 | 0.6115 | 0.8610 | 0.8957 |
| L r2 | 0.6252 | 0.4221 | 0.4637 | 0.5738 | 0.7837 | 0.8522 |
| L r3 | 0.7725 | 0.5618 | 0.5801 | 0.6127 | 0.6903 | 0.7192 |

- **In L r1 and L r2 the gap is order.** An order of the loop's own rules
  decides 0.8610 and 0.7837 of the space, more than at once. The loop wrote the
  rules of a better base than the answer's, and did not order them so.
- **In L r3 it is the rules.** No order of them reaches at once: their bound,
  0.7192, is below its 0.7725. S1 and S2 fail on L r3 alone.
- **The orders found are floors.** Each loop's best came from one random start
  of the 65, and the starts ended far apart, the lowest at 0.5699, 0.6278 and
  0.6609. From the completed order the search stopped at 0.7571, 0.7262 and
  0.6868. In L r3 the bound settles the row without the search.
- **Completing gives back little** (S3 fails). It adds 0.0335, 0.0416 and
  0.0183 of the space, against half gaps of 0.0968, 0.1016 and 0.1053.
- **The labels buy some order, and not at once's** (S4 holds).
  - **The space.** Searched on its labels, the completed base gains 0.0132,
    0.1102 and 0.0326.
  - **The labels.** It then decides right 165, 181 and 163 of its 216, 209 and
    235 labels, against 108, 107 and 103 as recorded.
  - **The halves.** It gains outside the keyword half, 3,775, 11,400 and 6,202
    points. In it, it loses 2,000 in L r1 and 1,820 in L r3, and gains 3,405 in L
    r2. It recalls less of `SECURITY_INCIDENT` than its record in L r1 and L r3,
    and more in L r2.

### 2. Where the order gains, and where at once stands

- **With the truth, the order gains most in the keyword half in L r1 and L r2**
  (S5 holds). It gains 24,465 and 33,580 points there, net, against 15,350 and
  15,025 outside. In L r3 it gains 1,900 there, against 15,362 outside.
- **It is `SECURITY_INCIDENT`'s region.** The queue's recall goes from 0.3514 to
  0.8333 in L r1, from 0.1437 to 0.6667 in L r2, and from 0.2976 to 0.3333 in L
  r3. In every run that is every point of the queue that containment leaves the
  loop's rules: section 3.
- **The rarest queue pays for it in L r1 and L r2.** `ONCALL_ESCALATION`'s recall
  falls from 0.4 to 0.3492 and from 0.4476 to 0.2952, and in L r3 rises from
  0.4341 to 0.5611.
- **At once is at or near its own best** (S6 holds). The median answer gains 0,
  0 and 0.0080 with the truth over its record, against the loop's 0.2962, 0.3616
  and 0.1284. In L r1 and L r2 two of the three answers already decide everything
  their bound allows.

### 3. Where the bound falls short — added after the first run

The points no rule undefeated by containment gets right, by how they are lost:

| run | short of the bound | no rule matches | no matching rule carries the true queue | the right rule lost to containment | of them `SECURITY_INCIDENT`'s | the median answer right among them |
|---|---|---|---|---|---|---|
| L r1 | 14,020 | 0 | 765 | 13,255 | 8,400 | 11,455 |
| L r2 | 19,870 | 0 | 1,040 | 18,830 | 16,800 | 17,760 |
| L r3 | 37,739 | 50 | 1,425 | 36,264 | 33,600 | 36,484 |

- **Almost all of it is lost to containment.** A rule of the point's true queue
  matches it, and so does a rule strictly inside that rule, and no order changes
  that.
- **Most of it is `SECURITY_INCIDENT`'s**, held by rules of other queues nested
  in the keyword's region:
  - **L r3**: two rules of `T2_TECHNICAL`, 16,800 points each. One is the
    gateway born at case 19, the keyword at severity 3 or more. The other, born
    at case 529, is the keyword at every severity but 1, and holds severity 2,
    where the gateway does not reach. Between them they hold two thirds of the
    queue's points;
  - **L r1**: the gateway `R0061`, of `T2_TECHNICAL`, the keyword at severity 4,
    born at case 238: 8,400;
  - **L r2**: one rule of `T2_TECHNICAL`, the keyword at severity 3 or more,
    born at case 754, with 8,400. Beside it, one of `T1_GENERAL`, the keyword at
    severity 4, born at case 1,895, with 7,610.
- **At once decides right most of what the loop's bound leaves**: 11,455, 17,760
  and 36,484 of those points. That includes every point of `SECURITY_INCIDENT`
  among them.

### The expectation

Written in `corrections/shape.py`'s docstring before the reading ran, and
committed before it. It is not signed, and it is on no scoreboard.

| clause | reading | |
|---|---|---|
| S1, in every L run, the loop's bound is at least at once | 0.8957, 0.8522 and 0.7192, against 0.7584, 0.6252 and 0.7725 | fails |
| S2, in every L run, the loop's rules with the truth decide at least as much of the space as at once | 0.8610, 0.7837 and 0.6903 | fails |
| S3, in at least two of L's runs, completing the loop's base gives back at least half of the gap | 0.0335, 0.0416 and 0.0183, against 0.0968, 0.1016 and 0.1053 | fails |
| S4, in every L run, the loop's base by its labels decides less of the space than at once | 0.6115, 0.5738 and 0.6127 | **holds** |
| S5, in L r1 and in L r2, the points the loop's rules with the truth decide right, less the record's, are more in the keyword half than outside it | 24,465 against 15,350, and 33,580 against 15,025 | **holds** |
| S6, in every L run, the median answer's gain with the truth over its record is smaller than the loop's | 0, 0 and 0.0080, against 0.2962, 0.3616 and 0.1284 | **holds** |

**S4, S5 and S6 hold, and S1, S2 and S3 fail.** The bet, S2, failed on L r3
alone, and so did S1, trusted most. The drafter had read that L r3's fall was
mostly containment, and still bet that the bound would clear at once there. S3,
trusted least, failed in every run.

### What it says

- **In L r1 and L r2 the gap is order.** An order of the loop's own rules
  decides more than at once. Rules nested in the keyword's region already held a
  sixth and a third of `SECURITY_INCIDENT`'s points, and what was left was
  enough. The loop ordered its rules, one declaration at a time, into a base
  that decides less, and most of what it lost is that queue's region.
- **In L r3 the gap is the rules.** Two rules of `T2_TECHNICAL` nested in the
  keyword's region hold two thirds of `SECURITY_INCIDENT`'s points by
  containment, and no order gives them back. At once decides them right.
- **So shape or order has no single answer.** The same loop, under the same
  kind of labels, lost by its order in two runs and by its rules in the third.
- **Neither completing nor the labels finds the order.** Completing by birth
  gives back little. Searched from there on its labels, the base gains some, most
  in L r2, and stays below at once in every run. What it gains lies mostly
  outside the keyword half, and the order found with the truth gains most inside
  it. The corpus holds few tickets of that half, and so do its labels.
- **The answers are ordered about as well as their rules allow.** The loop's
  rules allow more in L r1 and L r2, and its order gets far less of it.

### What it does not settle

1. **How far below their ceiling the orders found are.** Each loop's best came
   from one start of 65, below its bound. `PLAN_BOUND.md`'s certificate could
   tighten the bound. Free.
2. **Whether the model would order the loop's rules well.** Its at-once answers
   are near their own best. Handed the loop's final base and its labels, and
   asked for the rules in order, would it find what the search found? Asks only,
   cents. A plan with calls.
3. **What the labels bought in L r2**, and why so much more than in L r1 and L
   r3. Free on the records.

## A ranking of the queues as the order — POST-RUN

**Proposed by the agent and asked for by Sergi on 2026-11-16, after the reading
above.** In L r1 and L r2 an order of the loop's own rules, found with the
truth, decides more of the space than at once. Neither completing the base by
birth nor searching it on its own labels found that order (*Shape or order*),
and the levers left were calls, the model asked to order the loop's rules among
them. This reading asks first whether the order the loop lacks is a ranking of
the eight queues: one fixed order between them, which an operator could give
once, a few labels could fit, or a model has already stated. There are 40,320,
and every one is read. It spends nothing.

**A ranking, as an order rung 2's engine can install.**
`rung3/queue_hierarchy_floor.py` sorts the rules by their queue's rank. Rung 2's
engine lets a rule strictly inside another beat it wherever both match, so an
order it installs puts every such rule before the rule around it (*Shape or
order*). Where a rule of a lower-ranked queue lies strictly inside one of a
higher-ranked queue, no order keeps both the ranking and containment. Two
constructions place the pair:
- **pulled**, which the clauses read: each rule as early as its queue's rank and
  containment allow, the rules nested in it just before it, in its place;
- **waiting**: each rule at its own queue's rank, a rule waiting for every rule
  nested in it.
Where containment is silent both are rung 3's order, by rank and then by birth.
Inside a queue the ties go by birth.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.hierarchy`, on
2026-11-16 in local time, from `f5ff529` with its code clean, on the branch of
#269, which is `f801387` on `main`. It ran in three processes, one for each L
run, and read the hidden policy's rules in the parent.
- **The commits.** `f801387` on `main` carries the reading and its
  expectation, written before the reading ran. Nothing was added after it.
- **The record was committed alone**, as `b40fff7`.
- **On #269's branch the two commits were `f5ff529` and `eb355d9`.** Each pair
  has the same subject, the same tree and the same `git patch-id --stable`, and
  the GitHub API names #269 behind the two `main` commits.
- **Its `_env` says `git_dirty`**, for the files the session's sandbox mounted
  in the repository's root, untracked. `code_dirty` is false, and the code
  digest, `423f43512f91c958`, is the one `main` computes at `f801387`, and still
  at the merge.
- **The record is [`hierarchy.json`](hierarchy.json).** Its 18 gates passed:
  - each L run's final base and its three at-once answers at all labels are
    Stage C's. On this reading's instances, the record, the bound and the order
    with the truth that `shape.json` keeps give its figures;
  - every order of every ranking, under both constructions, puts every rule
    strictly inside another before it. Every order reported installs into a
    fresh rung 2 engine and closes no cycle, and the engine and first match each
    give it the share read;
  - no ranking decides more than its rules' bound;
  - each set of rules was read under all 40,320 rankings, and every ranking on
    record is one of them.

**What it reads.** Each L run's final base under every ranking and both
constructions:
- **the best ranking**, chosen with the truth;
- **the blind rankings**, all 40,320, and grouped by the place they give
  `SECURITY_INCIDENT`;
- **the rankings its labels choose**: those that decide the most of the run's
  labels right, the reported errors with their true queues;
- **the rankings on record**:
  - **stated**: the 24 the model gave in `PLAN_RANKING.md`'s session, asked for
    the order that decides which queue wins a contested ticket and shown the
    queues' names alone, and their Borda count;
  - **revealed**: Copeland over the model's pairwise answers about rung 1's
    learned base;
  - **Stage C's**: the ranking that best fits the answer key of the hidden
    policy's 170 labelled pairs. It reads the policy, on another object.

Each run's three at-once answers, and the hidden policy's own rules written as
an answer, are read under every ranking too.

### 1. One ranking orders the loop's rules above at once in L r1 and L r2

The share of the space, the first three columns from `shape.json`:

| run | at once | the loop: completed | with the truth | best ranking | Stage C's | stated, median | by its labels, median | blind, median |
|---|---|---|---|---|---|---|---|---|
| L r1 | 0.7584 | 0.5983 | 0.8610 | 0.7796 | 0.7779 | 0.6806 | 0.4470 | 0.3907 |
| L r2 | 0.6252 | 0.4637 | 0.7837 | 0.7091 | 0.7077 | 0.5794 | 0.5285 | 0.3430 |
| L r3 | 0.7725 | 0.5801 | 0.6903 | 0.6173 | 0.6173 | 0.5169 | 0.5302 | 0.3654 |

- **In L r1 and L r2 a ranking is enough** (Y2 holds, the bet). Ordered by
  their best ranking, the loop's own rules decide more of the space than at
  once. They stay below their order with the truth (Y1 holds).
- **It puts `SECURITY_INCIDENT` first**, in every run (Y3 holds).
  - **L r1's best** is `SECURITY_INCIDENT`, `BILLING_SPECIALIST`,
    `ONCALL_ESCALATION`, `ACCOUNT_MANAGER`, `T3_ENGINEERING`, `T2_TECHNICAL`,
    `SELF_SERVICE_DEFLECT`, `T1_GENERAL`.
  - **L r2's** puts `ONCALL_ESCALATION`, `ACCOUNT_MANAGER` and `T3_ENGINEERING`
    next, and **L r3's** is Stage C's.
  - **The rankings that put the queue first** decide 0.6703, 0.5638 and 0.4895
    of the space at their median.
- **It takes the keyword half as the order with the truth does.** In L r1 and
  L r3 it decides right the same points there, 58,800 and 33,600, and in L r2
  47,040 against 48,520. What it lacks lies outside: 45,980 points there
  against 56,915 in L r1, 48,265 against 56,810 in L r2, and 49,370 against
  59,171 in L r3.
- **It keeps more of the rarest queue than the order with the truth.**
  `ONCALL_ESCALATION`'s recall is 0.4667, 0.8667 and 0.7833 under it, against
  0.3492, 0.2952 and 0.5611.
- **Stage C's ranking comes within 0.002 of the best**, and in L r3 it is the
  best. It was fitted on the hidden policy's pairs, not on these runs.

### 2. What the loop had does not find it

- **The labels do not choose it** (Y4 holds).
  - **L r1's never place `SECURITY_INCIDENT`.** 128 rankings decide the most of
    its labels right, 120 of 216, and they put the queue in each of the eight
    places 16 times. At their median they decide 0.4470 of the space, below the
    base completed.
  - **L r2's and L r3's place it in the first four.** They choose 4 rankings
    and 60, which decide 0.5285 and 0.5302 at their median.
  - **The best of each set decides 0.7762, 0.6756 and 0.5801**, and nothing in
    the labels picks it out.
  - **The rankings fit the labels between the base completed and the
    completed order searched on them** (*Shape or order*): 120, 138 and 119
    labels right, against 116, 107 and 107, and 165, 181 and 163.
- **The model's stated rankings take the keyword half and give the rest away**
  (Y5 fails, on L r3 alone).
  - **All 24 put `SECURITY_INCIDENT` first.** The modal one, given by 14 asks
    and their Borda count, decides right in the keyword half what the best
    ranking does, in every run.
  - **It puts `ACCOUNT_MANAGER` seventh of eight**, below every technical tier,
    `T1_GENERAL` and `BILLING_SPECIALIST`. The queue's recall falls to 0.0000,
    0.0037 and 0.0347.
  - **At their median they decide 0.6806, 0.5794 and 0.5169**: above the base
    completed in L r1 and L r2, below it in L r3, and below at once in every
    run.
- **The revealed ranking puts `ONCALL_ESCALATION` first**, and loses part of
  the keyword half: `SECURITY_INCIDENT`'s recall is 0.5, 0.3333 and 0.1667
  under it. It decides 0.5894, 0.5585 and 0.5093.

### 3. Pulled, waiting, the answers and the policy

- **Waiting, no ranking reaches at once in L r1 and L r2** (Y6 holds). The
  best decides 0.6564, 0.4905 and 0.6004. There the queue's rule waits for the
  rules of other queues nested in it, behind the rules of the queues ranked
  between. `SECURITY_INCIDENT`'s recall is 0.6686, 0.3421 and 0.3333 under the
  best.
- **The at-once answers are rankings already.** Each answer's best ranking
  decides at least what its own list does, and in six of the nine what its
  order with the truth does. Ranked the same way, the median answer decides
  0.7584, 0.6981 and 0.7725: less than the loop's rules in L r1 and L r2, more
  in L r3.
- **The hidden policy lies near a ranking.**
  - **Its own rules, under their best ranking, decide 0.9756 of the space.**
    The ranking is `SECURITY_INCIDENT`, `ONCALL_ESCALATION`, `ACCOUNT_MANAGER`,
    `T2_TECHNICAL`, `T3_ENGINEERING`, `BILLING_SPECIALIST`,
    `SELF_SERVICE_DEFLECT`, `T1_GENERAL`, the first of 12 that tie.
  - **They fall short at two of the three contradictions the drafter read**:
    `BILLING_SPECIALIST`'s recall is 0.7135, and `T3_ENGINEERING`'s 0.8411.
  - **The third costs nothing.** `T2_TECHNICAL` and `SELF_SERVICE_DEFLECT` are
    decided whole. Read again after the run, earlier rules of the policy decide
    every point their three rules share, so no point sees that contradiction.
    The docstring keeps it, as it was written before the reading ran.
  - **The rankings on record**: Stage C's decides 0.9321 of it, the stated
    rankings 0.8867 at their median, and the revealed one 0.7836.

### The expectation

Written in `corrections/hierarchy.py`'s docstring before the reading ran, and
committed before it. It is not signed, and it is on no scoreboard.

| clause | reading | |
|---|---|---|
| Y1, in every L run, the best ranking of the loop's rules decides less of the space than its rules with the truth | 0.7796, 0.7091 and 0.6173, against 0.8610, 0.7837 and 0.6903 | **holds** |
| Y2, in L r1 and in L r2, the best ranking of the loop's rules decides more of the space than at once | 0.7796 and 0.7091, against 0.7584 and 0.6252 | **holds** |
| Y3, in every L run, the best ranking of the loop's rules puts `SECURITY_INCIDENT` first | first in all three | **holds** |
| Y4, in every L run, the rankings its labels choose decide, at their median, less of the space than at once | 0.4470, 0.5285 and 0.5302, against 0.7584, 0.6252 and 0.7725 | **holds** |
| Y5, in every L run, the model's stated rankings decide, at their median, more of the space than the loop's base completed | 0.6806, 0.5794 and 0.5169, against 0.5983, 0.4637 and 0.5801 | fails |
| Y6, in L r1 and in L r2, the best ranking pulled decides more of the space than the best ranking waiting | 0.7796 and 0.7091, against 0.6564 and 0.4905 | **holds** |

**Y1, Y2, Y3, Y4 and Y6 hold, and Y5 fails.** The bet, Y2, held. Y5, trusted
least, failed on L r3 alone: there the stated rankings lose more outside the
keyword half than the base completed by birth does. Y4 could not fail in L r3,
as its account said.

### What it says

- **In L r1 and L r2 the order the loop lacks is mostly one ranking of the
  queues**, with `SECURITY_INCIDENT` first. Ordered by it, the loop's own rules
  beat at once there. What the ranking leaves to an order chosen rule by rule
  lies outside the keyword half. There the policy orders some pairs of queues
  one way in one region and the other way in another.
- **Such a ranking exists without these runs.** Stage C's comes within 0.002 of
  the best. It was fitted on which of two of the policy's rules should win, 170
  times: knowledge of the policy, not of the runs.
- **What the loop had does not give it.** Its labels never place
  `SECURITY_INCIDENT` in L r1, and choose rankings that decide less than its
  base completed there. The model's stated rankings place the queue first and
  give `ACCOUNT_MANAGER` away: asked for an order, the model gave a priority, as
  `PLAN_RANKING.md` found.
- **How a ranking meets containment matters as much as the ranking.** Pulled,
  the best ranking beats at once in L r1 and L r2. Waiting, none does.
- **In L r3 no ranking helps**, as no order does: rules of another queue nested
  in the keyword's region hold the queue's points.
- **The at-once answers are rankings already, and the policy lies near one.**
  Ranked the same way, the loop's rules beat the answers in two runs of three.

### What it does not settle

1. **A loop that orders its rules by a ranking.** These are the loop's final
   rules, ordered after the run. A loop whose engine installed each birth by a
   fixed ranking would decide other cases on the way, escalate others, and
   write other rules. Calls, and a plan.
2. **Where a deployment would get the ranking.** Stage C's was fitted on the
   hidden policy's answer key. Whether the model gives it when shown the order
   at work, as `PLAN_RANKING.md` left open, or how few labelled pairs fit it,
   is not read. The first is asks, cents.
3. **What the best ranking leaves outside the keyword half**: which pairs of
   queues it orders against the order with the truth, and on how many points.
   Free on the records.
4. **The tie-break inside a queue.** Where containment pulls a rule into
   another queue's place, its birth sets its place among that queue's rules.
   Another tie-break could move the figures. Not read.

## The ranking the loop declared — POST-RUN

**Proposed by the agent and asked for by Sergi on 2026-11-16, after the reading
above.** In L r1 and L r2 one ranking of the queues orders the loop's own rules
above at once, and neither the run's labels nor the model's stated rankings find
it (*A ranking of the queues as the order*). This reading asks whether the loop
had declared it. At every birth, the placement round's answer declared the
newborn above or below rules of other queues. Gathered by pair of queues, the
declarations choose rankings, and those order the loop's rules as the reading
above orders them, pulled. It spends nothing.

**The declarations.** Each citation of each answer is one vote for the queue
it declared above, whether the engine installed it, refused it for closing a
cycle, or never ruled on it because the round had not shown the rule
(outside). A citation of a rule of the newborn's own queue is left out.
`corrections/fall.py`'s `declared` keeps one citation a rule. This reading
keeps one a rule and side, because in L r1 and L r2 one answer each cited a
rule on both sides. The rankings the declarations choose are those, of the
40,320, that agree with the most votes.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.declared`, on
2026-11-16 in local time, from `62587b8` with its code clean, on the branch of
#271, which is `6c5c03f` on `main`.
- **The commits.** `6c5c03f` on `main` carries the reading and its
  expectation, written before the reading ran. Nothing was added after it.
- **The record was committed alone**, as `51c9f45`.
- **On #271's branch the two commits were `62587b8` and `7dc6f7a`.** Each pair
  has the same subject, the same tree and the same `git patch-id --stable`, and
  the GitHub API names #271 behind the two `main` commits.
- **Its `_env` says `git_dirty`**, for the files the session's sandbox mounted
  in the repository's root, untracked. `code_dirty` is false, and the code
  digest, `da99302475a446c0`, is the one `main` computes at `6c5c03f`, and still
  at the merge.
- **The record is [`declared.json`](declared.json).** Its 15 gates passed:
  - each L run's final base is Stage C's, and its instance `shape.json`'s;
  - every declaration the engine ruled on is in the run's edge log, with the
    verdict read, and every edge of the log is one of them;
  - the run's best ranking in `hierarchy.json`, read here, decides what that
    record keeps;
  - every order read installs into a fresh rung 2 engine and closes no cycle,
    and the engine and first match each give it the share read. No ranking
    read decides more than the rules' bound.

### 1. The loop declared one ranking, `SECURITY_INCIDENT` first

- **The votes.** L r1's answers cast 7,254: 5,405 installed and 1,849 refused.
  L r2's cast 6,460: 4,254 installed, 2,159 refused and 47 outside the round.
  27 more cited rules of the newborn's own queue the round had not shown, and
  are left out. L r3's cast 6,182: 4,586 installed and 1,596 refused.
- **One ranking a run** (W1 holds). The votes leave no pair of queues even, and
  choose one ranking in every run:
  - **L r1 and L r3**: `SECURITY_INCIDENT`, `ONCALL_ESCALATION`,
    `T3_ENGINEERING`, `ACCOUNT_MANAGER`, `T2_TECHNICAL`,
    `SELF_SERVICE_DEFLECT`, `BILLING_SPECIALIST`, `T1_GENERAL`;
  - **L r2**: the same, with `BILLING_SPECIALIST` fifth.
- **Few votes go against `SECURITY_INCIDENT`**: 11 of 1,236 that meet it in L
  r1, 24 of 1,985 in L r2, and 34 of 1,557 in L r3.

### 2. It orders the loop's rules better than the loop did

The share of the space, the first two columns from `shape.json` and the next
two from `hierarchy.json`:

| run | at once | the loop: completed | best ranking | stated, median | the ranking declared | from the installed votes alone |
|---|---|---|---|---|---|---|
| L r1 | 0.7584 | 0.5983 | 0.7796 | 0.6806 | 0.7495 | 0.7495 |
| L r2 | 0.6252 | 0.4637 | 0.7091 | 0.5794 | 0.6861 | 0.6419 |
| L r3 | 0.7725 | 0.5801 | 0.6173 | 0.5169 | 0.5987 | 0.5330 |

- **Above the base completed and the stated rankings, in every run** (W3 and
  W6 hold).
- **Above at once in L r2, and 0.0089 of the space below it in L r1** (W2, the
  bet, fails on L r1 alone).
- **It takes the keyword half as the best ranking does**: 58,800, 47,040 and
  33,600 points there. What it lacks lies outside: 41,935, 45,170 and 46,870
  points, against the best ranking's 45,980, 48,265 and 49,370.
- **What it lacks is mostly the queues of the billing tickets.**
  `ACCOUNT_MANAGER`'s recall is 0.7226, 0.7591 and 0.7810 under it, against the
  best ranking's 0.8321, 0.9562 and 0.8929. `BILLING_SPECIALIST`'s is 0.2990
  and 0.1374 in L r1 and L r3, against 0.7018 and 0.2866, and
  `SELF_SERVICE_DEFLECT`'s 0.4488 in L r2, against 0.9593.

### 3. The refused votes were the righter ones

- **Most votes agree with the best ranking**: 0.6023, 0.7537 and 0.7624 of
  them (W4 holds).
- **The refused agree more often than the installed**: 0.7123 against 0.5647
  in L r1, and 0.7767 against 0.7426 in L r2 (W5 holds). In L r3, 0.8352
  against 0.7370.
- **Gathered from the installed votes alone**, the ranking is the same in L r1,
  and decides less in L r2 and L r3, in L r3 less than the base completed.
  What the engine refused carried part of the order.

### The expectation

Written in `corrections/declared.py`'s docstring before the reading ran, and
committed before it. It is not signed, and it is on no scoreboard.

| clause | reading | |
|---|---|---|
| W1, in every L run, every ranking its declarations choose puts `SECURITY_INCIDENT` first | one ranking a run, `SECURITY_INCIDENT` first in all three | **holds** |
| W2, in L r1 and in L r2, the rankings its declarations choose decide, at their median, more of the space than at once | 0.7495 and 0.6861, against 0.7584 and 0.6252 | fails |
| W3, in every L run, they decide, at their median, more of the space than the loop's base completed | 0.7495, 0.6861 and 0.5987, against 0.5983, 0.4637 and 0.5801 | **holds** |
| W4, in every L run, more than half of its votes agree with the best ranking | 0.6023, 0.7537 and 0.7624 | **holds** |
| W5, in L r1 and in L r2, the votes the engine refused agree with the best ranking more often than those it installed | 0.7123 and 0.7767, against 0.5647 and 0.7426 | **holds** |
| W6, in every L run, the rankings its declarations choose decide, at their median, more of the space than the model's stated rankings at theirs | 0.7495, 0.6861 and 0.5987, against 0.6806, 0.5794 and 0.5169 | **holds** |

**W1, W3, W4, W5 and W6 hold, and W2 fails.** The bet, W2, failed on L r1
alone, by 0.0089 of the space. W1, trusted least, held: the answers that climb
left no pair with `SECURITY_INCIDENT` even.

### What it says

- **The loop declared most of the order it lacks.** Gathered by pair of
  queues, its own declarations choose one ranking, `SECURITY_INCIDENT` first.
  It orders the loop's rules better than the base the loop installed, in every
  run. It beats at once in L r2, and falls just short in L r1.
- **The loop lost it installing its declarations one at a time.** The votes
  the engine refused for closing a cycle agree with the best ranking more often
  than those it installed. Without them the ranking decides less in two runs of
  three.
- **Declaring beside the rules, the model ranks queues better than with their
  names alone.** The same model put `ACCOUNT_MANAGER` fourth in every run's
  declared ranking, and seventh in the ranking it stated most often. The two
  differ in more than the rules in sight: the loop reasoned and had level 1's
  catalogue, and the stated rankings were asked with reasoning off.
- **What it misses is mostly the queues of the billing tickets**:
  `ACCOUNT_MANAGER`'s in every run, `BILLING_SPECIALIST`'s in L r1 and L r3,
  and `SELF_SERVICE_DEFLECT`'s in L r2.
- **So a lever needs no new input.** A loop that gathered its own declarations
  into one ranking, and installed its rules by it, would need no labels, no
  operator and no new question. Whether it would keep this while writing its
  rules is calls.

### What it does not settle

1. **A loop that installs by the ranking its declarations choose.** These are
   the final declarations, gathered after the run. A loop that ranked as it
   went would decide other cases on the way and write other rules. Calls, and
   a plan.
   **[NOTE 2026-11-16] Replayed POST-RUN, below, on the loop's own births.** It
   keeps what conflicts cost, and not what containment costs. *The ranking the
   loop declared, as it went*.
2. **The readings that read declarations through `corrections/fall.py`'s
   `declared`.** It keeps one citation a rule, and in L r1 and L r2 one answer
   each cited a rule on both sides. `fall.py`, `conditions.py`, `gateway.py`,
   `above.py`, `byqueue.py` and `doors.py` read declarations through it.
   Whether a figure of theirs moves is not read. Free on the records.
   **[NOTE 2026-11-16] Read POST-RUN, below: seven figures move, by one to six,
   and no verdict.** *The citations on both sides*.
3. **Why the declarations put `BILLING_SPECIALIST` low.** In L r1 most of its
   votes against `ONCALL_ESCALATION`, `ACCOUNT_MANAGER` and
   `SELF_SERVICE_DEFLECT` go against it. Free on the records.

## The citations on both sides — POST-RUN

**Proposed by the agent and asked for by Sergi on 2026-11-16, after the reading
above.** `corrections/fall.py`'s `declared` keeps one citation a rule, and in L
r1 and L r2 one answer each cited a rule on both sides (*The ranking the loop
declared*). Six readings read the answers' declarations through it, and three
more read their records. This audit asks which of their figures move when the
side `declared` drops is the one kept. It spends nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.citations`, on
2026-11-16 in local time, from `88c8d91` with its code clean, on the branch of
#273, which is `f7f1c44` on `main`. It runs the nine readings in the order their
records feed one another, each writing to a temporary directory, three times:
- **as committed**, on the runs as they are;
- **the other side**, on copies of the runs in which every answer that cites a
  rule on both sides cites it only on the side `declared` drops, in the rule's
  lists and in its placement call's answer;
- **past the pins**, added after the first run: the same copies, with the
  development counts that `doors.py`, `byqueue.py`, `above.py` and
  `conditions.py` write in their code compared, recorded and let through.

Each record is compared with the first pass's leaf by leaf, but for `_env` and
`source`, and so is every clause's verdict.
- **The commits.** `7f89683` on `main` carries the audit and its expectation,
  written before it ran. `f7f1c44` carries the third pass, added after the
  first run, which moves no clause. The first run's record was not committed.
- **The record was committed alone**, as `78522ec`.
- **On #273's branch the three commits were `7dd08f7`, `88c8d91` and
  `6c3427d`.** Each pair has the same subject, the same tree and the same
  `git patch-id --stable`. GitHub's API names no pull request behind the
  `main` commits, since it never marked #273 merged.
- **Its `_env` says `git_dirty`**, for the files the session's sandbox mounted
  in the repository's root, untracked. `code_dirty` is false, and the code
  digest, `0c21da60ca73814e`, is the one `main` computes at `f7f1c44`, and
  still at `0a28202`.
- **The record is [`citations.json`](citations.json).** Its 3 gates passed:
  the citations match the runs' edge logs, the copies change only the citations
  on both sides, and as committed the nine readings give their records.

### 1. Eight citations on both sides, in three answers

| run | answer | its queue | the rules it cites on both sides |
|---|---|---|---|
| L r1 | `R0159` | `T1_GENERAL` | `R0021`, of `SELF_SERVICE_DEFLECT` |
| L r2 | `R0198` | `SELF_SERVICE_DEFLECT` | `R0176`, of `T2_TECHNICAL` |
| N r1 | `R0263` | `T1_GENERAL` | five of `T2_TECHNICAL`, and `R0033`, of `SELF_SERVICE_DEFLECT` |

- **Every one was declared above, installed, and below, refused** for the cycle
  the first side had closed. The loop installs a newborn's wins first, and
  `declared` keeps the refused side.
- **None is in L r3, N r2 or N r3.**

### 2. What moves

On the second pass `doors.py` and `above.py` refused at their gate 5, which
holds L r1's development counts, written in their code, to what they compute.
Those counts moved, and the four readings after them could not run. Past the
pins:

| reading | leaves that move | where |
|---|---|---|
| `fall.py`, `paths.py` | 0 | |
| `gateway.py` | 12 | every answer's sides, in L r1, L r2 and N r1 |
| `doors.py` | 11 | the placements outside the keyword, in L r1, L r2 and N r1, and L r2's two listings of `R0198`'s round |
| `byqueue.py`, `conditions.py`, `carry.py`, `oncall.py` | 0 | |
| `above.py` | 19 | the placements by cause, in L r1, L r2 and N r1, and N r1's round of `R0263` |

- **Every count moves by the citations on both sides it counts**: by one or
  two in L r1 and L r2, where `R0198`'s round is listed twice, and by up to six
  in N r1.
- **No clause of the nine readings changes its verdict.**
- **Seven figures this record cites move**, in three sections, and each now
  carries a dated erratum:
  - *Why so many rules sit above the gateway*: L's answers declared their
    newborn below 8,033 of the 19,921 rules they placed, not 8,035;
  - *Why the doors declared themselves above the gateway*: the rules outside
    the keyword placed below are 1,889 of 6,423 in L r1 and 1,418 of 5,326 in
    L r2, not 1,890 and 1,419. Of the 165 held-out cedes, 69 put their newborn
    above every rule of the gateway's queue that is not a keyword rule, not 67;
  - *Why some answers put their newborn above every rule of their list*:
    5,485 of 9,824, 2,297 of 3,996 and 1,095 of 1,204, not 5,484, 2,296 and
    1,089.
- **Nothing `STATUS.md`, `IDEAS.md` or `CLAUDE.md` cites moves.**

### The expectation

Written in `corrections/citations.py`'s docstring before the audit ran, and
committed before it. It is not signed, and it is on no scoreboard.

| clause | reading | |
|---|---|---|
| Z1, the rules an answer cites on both sides are R0021, cited by L r1's R0159, and R0176, cited by L r2's R0198 | eight, six of them cited by N r1's R0263 | fails |
| Z2, under the other side, gateway.json and above.json move | `gateway.json` 12 leaves; `above.py` refused | fails |
| Z3, fall.json does not move | 0 leaves | **holds** |
| Z4, paths, doors, byqueue, conditions, carry and oncall do not move | `paths.json` 0 leaves; `doors.py` refused, and the four after it could not run | fails |
| Z5, no clause of the nine readings changes its verdict | six readings refused or could not run | fails |
| Z6, every reading writes under the other side | six did not | fails |

**Z3 holds, and Z1, Z2, Z4, Z5 and Z6 fail.**
- **Z1, trusted least, failed on N's runs**, which `corrections/declared.py`
  never read.
- **Z2, Z4, Z5 and Z6 failed on the second pass's refusals.** A pin of counts
  refuses any change below it.
- **Past the pins**, added after the first run and read by no clause,
  `gateway.py` and `above.py` move, as Z2 said, and `doors.py` moves too,
  against Z4. The drafter's account held that neither answer's round could list
  a keyword rule. `R0198` does not exclude the keyword, and its round listed
  both of L r2's gateways. No verdict changes, as Z5 said.

### What it says

- **The figures that move are counts of sides**, and each moves by its
  citations on both sides. They lie in three readings, `gateway.py`, `doors.py`
  and `above.py`, and no verdict moves.
- **The rest of what the nine readings found stands.** That covers the
  conflicts the loop left and the cycles that closed them, the rules above the
  gateways and the doors, the codes, what the doors carry, and why L loses
  `ONCALL_ESCALATION`.
- **A pin of counts refuses any change below it.** The development counts that
  four readings write in their code made two of them refuse, and stopped four
  more. An audit that changes a record has to let such pins through to see
  what moves, and say so.

### What it does not settle

1. **Which side the answers meant.** Each of the three declared its newborn
   above and below the same rules, in one answer. The records keep both sides.
   The audit reads each, and neither is the answer's alone.
2. **Whether readings of other threads key citations by rule.** The loops of
   `PLAN_REASONED_LOOP.md`, `PLAN_CHANNEL.md`, `PLAN_PLACEMENT.md` and
   `PLAN_WHOLE.md` record their declarations the same way. Free on the records.

## The ranking the loop declared, as it went — POST-RUN

**Proposed by the agent and asked for by Sergi on 2026-11-16, after the audit
above.** Gathered after the run, the loop's declarations choose one ranking that
orders its final rules above at once in L r2, and just below it in L r1 (*The
ranking the loop declared*). A loop that ranked its base by its own
declarations while it ran is calls and a plan. This reading replays each L
run's births in their order, and after every birth orders the base so far by
the ranking its declarations so far choose. It spends nothing.

**The replay.** After each birth the votes are those of the answers born so
far, read as *The ranking the loop declared* reads them. Of the rankings that
agree with the most of them, the replay takes the earliest in
`itertools.permutations(ACTIONS)`: a loop must take one, and that rule reads no
truth. It orders the base so far under the pulled construction, and reads it
over the space as rung 2's engine decides. **It is a replay, not the loop that
would have run**: its rules are the ones the loop wrote.

**What was run.** `PYTHONHASHSEED=0 python3 -m corrections.online`, on
2026-11-16 in local time, from `685f46f` with its code clean, on the branch of
#275, which is `4e7676d` on `main`.
- **The commits.** `4e7676d` on `main` carries the reading and its
  expectation, written before the reading ran. Nothing was added after it.
- **The record was committed alone**, as `89576d3`.
- **On #275's branch the two commits were `685f46f` and `f21ec45`.** Each pair
  has the same subject, the same tree and the same `git patch-id --stable`, and
  the GitHub API names #275 behind the two `main` commits.
- **Its `_env` says `git_dirty`**, for the files the session's sandbox mounted
  in the repository's root, untracked. `code_dirty` is false, and the code
  digest, `88db753e70125983`, is the one `main` computes at `4e7676d`, and still
  at the merge.
- **The record is [`online.json`](online.json).** Its 12 gates passed:
  - each L run's final base is Stage C's;
  - after the last birth the votes, the ranking and what it decides are
    `declared.json`'s;
  - the record's curve is `fall.json`'s, and at each checkpoint it gives the
    loop's share `score.json` keeps;
  - at each checkpoint, the base installed in the replay's order into a fresh
    rung 2 engine closes no cycle, and the engine and first match each decide
    what the replay reads.

### 1. At the checkpoints

The share of the space at each count of labels, the loop's and at once's from
`score.json`:

| run | | 10 | 20 | 40 | 80 | 160 | all |
|---|---|---|---|---|---|---|---|
| L r1 | the replay | 0.5231 | 0.5686 | 0.6272 | 0.7408 | 0.7541 | 0.7495 |
| | the loop | 0.5241 | 0.5755 | 0.5162 | 0.6539 | 0.6170 | 0.5647 |
| | at once | 0.5944 | 0.6051 | 0.6952 | 0.4760 | 0.7890 | 0.7584 |
| L r2 | the replay | 0.6391 | 0.7398 | 0.7433 | 0.6997 | 0.7228 | 0.6861 |
| | the loop | 0.6810 | 0.7597 | 0.7512 | 0.5490 | 0.5116 | 0.4221 |
| | at once | 0.5541 | 0.5594 | 0.5250 | 0.3829 | 0.6240 | 0.6252 |
| L r3 | the replay | 0.2398 | 0.6402 | 0.6422 | 0.5759 | 0.5907 | 0.5987 |
| | the loop | 0.3158 | 0.6488 | 0.6338 | 0.5477 | 0.5089 | 0.5618 |
| | at once | 0.5713 | 0.6051 | 0.4607 | 0.6122 | 0.6928 | 0.7725 |

- **In L r2 the replay is above at once at every checkpoint** (U4 holds, the
  bet), and above the loop from 80 labels on.
- **In L r1 it is above the loop from 40 labels on**, and above at once at 80
  labels only.
- **In L r3 it is above the loop from 40 labels on**, and below at once from
  80 labels on.

### 2. The peak, the fall and the ranking

| run | the replay: peak | at birth | final | the record: peak | at birth | final |
|---|---|---|---|---|---|---|
| L r1 | 0.7638 | 257 | 0.7495 | 0.6896 | 87 | 0.5647 |
| L r2 | 0.7596 | 65 | 0.6861 | 0.7773 | 66 | 0.4221 |
| L r3 | 0.7002 | 81 | 0.5987 | 0.6895 | 81 | 0.5618 |

- **In L r1 the replay does not fall.** It peaks late, at birth 257 of 282,
  and ends 0.0142 below its peak. From the record's peak on it is never below
  the record.
- **In L r2 and L r3 it falls**, by 0.0735 and 0.1015 (U3 fails).
  - **The largest drop of each is a rule nested in the keyword's region.** In
    L r2, the birth of `R0120`, of `T2_TECHNICAL`, the keyword at severity 3 or
    more, takes 7,560 points. In L r3, the birth of `R0104`, of `T2_TECHNICAL`,
    the keyword at every severity but 1, takes 16,800. Each holds
    `SECURITY_INCIDENT`'s points by containment (*Shape or order*, section 3),
    and no ranking moves containment.
  - **After the record's peak the replay falls below it** at 13 births in L r2
    and 7 in L r3 (U2 fails).
  - **In L r2 the replay's peak, 0.7596, is below the record's, 0.7773** (U6
    fails), one birth before it.
- **The ranking puts `SECURITY_INCIDENT` first early**, for good from births
  23, 25 and 62 (U1 holds).
- **Its lower places settle late.** The ranking changes 21, 23 and 32 times,
  and is the final one for good only from births 250, 257 and 265. At the
  record's peak it is not the final ranking in any run (U5 fails).

### The expectation

Written in `corrections/online.py`'s docstring before the reading ran, and
committed before it. It is not signed, and it is on no scoreboard.

| clause | reading | |
|---|---|---|
| U1, in every L run, the replay's ranking puts `SECURITY_INCIDENT` first for good by the record's peak birth | from births 23, 25 and 62, against peaks at 87, 66 and 81 | **holds** |
| U2, in every L run, at every birth from the record's peak on, the replay decides at least as much of the space as the record | below it at 0, 13 and 7 births | fails |
| U3, in every L run, the replay's final is within 0.02 of the space of its own peak | 0.0142, 0.0735 and 0.1015 below it | fails |
| U4, in L r2, at every checkpoint from 40 labels on, the replay decides more of the space than at once | 0.7433, 0.6997, 0.7228 and 0.6861, against 0.5250, 0.3829, 0.6240 and 0.6252 | **holds** |
| U5, in every L run, the replay's ranking at the record's peak birth is its final ranking | in none | fails |
| U6, in every L run, the replay's peak is at least the record's | 0.7638, 0.7596 and 0.7002, against 0.6896, 0.7773 and 0.6895 | fails |

**U1 and U4 hold, and U2, U3, U5 and U6 fail.** The bet, U4, held, and so did
U1, trusted most. U5, trusted least, failed in every run. U2 and U3 failed on L
r2 and L r3, and U6 on L r2 alone.

### What it says

- **Ranked as it went, the loop keeps what conflicts cost it.** L r1's replay
  rises nearly to the end and does not fall. In every run the replay ends
  above the record.
- **It does not keep what containment costs it.** In L r2 and L r3 it falls
  where a rule of another queue is born nested in the keyword's region. A
  ranking orders rules, and does not undo containment.
- **In L r2 it beats at once at every checkpoint.** On these births, a loop that
  ranked as it went would have beaten compiling at once there all along. In L
  r1 and L r3 it does not.
- **The ranking needs few births for its first place, and many for the rest.**
  `SECURITY_INCIDENT` comes first by birth 62 in every run, and the lower places
  move until births 250, 257 and 265.
- **So two levers remain, and both are calls**: a loop that ranks as it goes,
  and a rule of another queue kept from being born nested in the keyword's
  region. The replay shows what the first buys on these births, and the second
  is what it leaves.

### What it does not settle

1. **The loop that ranks as it goes.** These are the loop's own births. A loop
   that ranked its base as it went would decide other cases on the way,
   escalate others and write other rules. Calls, and a plan.
2. **The tie rule.** Early on, many rankings tie, and the replay takes the
   earliest. Another rule that reads no truth could move the early curve. Free
   on the records.
3. **What the other drops are.** The largest drop of L r2 and of L r3 is a birth
   nested in the keyword's region. The others are not read. Free on the
   records.

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
- [`byqueue.json`](byqueue.json): POST-RUN, what makes an answer read a keyword
  rule by its queue.
- [`above.json`](above.json): POST-RUN, why some answers put their newborn above
  every rule of their list.
- [`conditions.json`](conditions.json): POST-RUN, what makes an answer read the
  list by its conditions.
- [`oncall.json`](oncall.json): POST-RUN, why L loses `ONCALL_ESCALATION`.
- [`layer.json`](layer.json): POST-RUN, what the at-once asks wrote for
  `ONCALL_ESCALATION` and the layer below it.
- [`shape.json`](shape.json): POST-RUN, shape or order: what the loop's own
  rules could decide, ordered.
- [`hierarchy.json`](hierarchy.json): POST-RUN, whether the order the loop lacks
  is a ranking of the queues.
- [`declared.json`](declared.json): POST-RUN, whether the loop declared the
  ranking it lacks.
- [`citations.json`](citations.json): POST-RUN, the citations on both sides:
  what the readings that kept one move.
- [`online.json`](online.json): POST-RUN, the ranking the loop declared, as it
  went.
