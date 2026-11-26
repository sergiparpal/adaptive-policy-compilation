# What the loop's first call writes when it is told why its ticket escalated — findings

Record opened on November 26, 2026, under [`PLAN_CAUSE.md`](../PLAN_CAUSE.md).
Sergi signed §0 on 2026-11-25, before any figure below existed, in a commit of
its own: `8fbc42f` on `main`.
- **The plan, its package, the signature, Stage A, the smoke run and the three
  sessions** reached `main` in #308, merged on 2026-11-26.
- **Stage C, this record, the banner that closes the plan and the indexes**
  reached it in #309, merged on 2026-11-26.
- **The POST-RUN reading of two things Stage C left free** reached it in
  #310, merged on 2026-11-26 at Sergi's word.

Every record names in its `_env` the commit it was written from. Five were
written on the branch of #308, and the rebase merge gave each of those commits
a new hash on `main`. Each pair has the same subject and the same `git
patch-id --stable`.
- **The trees of each pair differ in one file.** `main` gained #307, an erratum
  to `FINDINGS_HALVES.md`, while the branch was open, and the rebase set the
  branch's commits on top of it.
- **Nothing under `cause/` or `results_cause/` differs.**

| record | written from | the same commit on `main` | code digest | `git_dirty`, `code_dirty` |
|---|---|---|---|---|
| `sample.json` | `fda8b47`, the signature, on the branch of #308 | `8fbc42f` | `af3d8aae3b48e215` | true, false |
| `ask_smoke.json` | `2e689d4`, Stage A's commit, on the branch of #308 | `53275c3` | `af3d8aae3b48e215` | true, false |
| `ask_pass1.json` | `c294e9a`, the smoke run's commit, on the branch of #308 | `754f870` | `af3d8aae3b48e215` | true, false |
| `ask_pass2.json` | `19f4943`, pass 1's commit, on the branch of #308 | `12629dc` | `af3d8aae3b48e215` | true, false |
| `ask_oncall.json` | `a03f54e`, pass 2's commit, on the branch of #308 | `ad699c3` | `af3d8aae3b48e215` | true, false |
| `score.json` | `56bfefc`, the rarest queue's session's commit, on `main` (#308) | itself | `af3d8aae3b48e215` | true, false |

**`code_dirty` is false in every record, and every record carries one code
digest**, which `main` computes at `56bfefc`. The package's code did not change
between the signature and Stage C.

**`git_dirty` is true in every record, for files that are not the
repository's.** Empty placeholder files sat untracked in the repository's root
throughout, named `.bashrc`, `.gitconfig`, `.claude/` and the like, as in
`PLAN_CORRECTIONS.md`'s records. No module reads them, and no commit staged
one.

**[NOTE 2026-11-26, later] And two POST-RUN records.**
[`review.json`](review.json) and [`general.json`](general.json) are the
POST-RUN reading of two things Stage C left free.
- **They were written from `485b7d6`**, on the branch of #310, which is
  `4b2dfc7` on `main`: the commit that adds both readings and their
  expectations.
- **Their code digest is `0c4414106f60c424`**, because `cause/review.py` and
  `cause/general.py` were added after Stage C. `main` computes it at `4b2dfc7`,
  and still at the merge of #310. Their `_env` says `git_dirty`, for the same
  files, and `code_dirty` is false. The modules Stage C ran did not change.

**[NOTE 2026-11-26, last] And a third.** [`narrow.json`](narrow.json) is the
POST-RUN reading of one thing those two left free.
- **It was written from `482180e`**, on the branch `cause-narrow`: the commit
  that adds the reading and its expectation.
- **Its code digest is `d7cf6d135e7fbc18`**, because `cause/narrow.py` was
  added after them. Its `_env` says `git_dirty`, for the same files, and
  `code_dirty` is false. The modules the two readings ran did not change.

**This record owns every figure in it.**

**All three stages ran on 2026-11-25 and 2026-11-26. `CA-a`, `CA-b`, `CA-c`
and `CA-f` hold. `CA-d` is refuted, thin, and `CA-e` is unadjudicable.
`CA-g` is reported.** All 1,208 asks came back valid, from the pinned provider.

- **Told that no rule of the base matches its ticket, the first call writes the
  governing rule's region whole as often as under the empty base.** The arms
  were asked in one period, of one provider, interleaved. Over both passes at
  the 136 tickets:
  - the impasse notice wrote the region in 189 of its 247 right-queue answers,
    0.7652;
  - the empty base wrote it in 200 of 267, 0.7491;
  - v2b's paragraph wrote it in 87 of 264, 0.3295.

  The notice gave back more than half the gap (`CA-c` holds), and in fact all
  of it.
- **And it stops naming a conflict between two listed rules** (`CA-f` holds).
  The codebook's `BETWEEN` marked 15 of the impasse notice's 247 right-queue
  answers, 0.0607. It marked 196 of v2b's 264, 0.7424, and 72 of the empty
  base's 267.
- **Its cuts by a listed rule nearly vanish.** 8 of its 247 right-queue answers
  were cut by one listed rule, against 87 of v2b's 264 and 35 of the empty
  base's 267. Most of what it did not write whole was *other*: 50 answers.
- **Told that a reviewer marked the engine's decision wrong, the first call
  names another queue.** 259 of the review notice's 272 answers named a queue
  other than the governing rule's. The other arms named a wrong queue 5 times
  (the empty base), 8 times (v2b's paragraph) and 25 times (the impasse notice).
  - **So `CA-d` read the review notice on 13 answers** (`CA-d` refuted, thin),
    and its refutation is about those 13.
  - **And `CA-e` has no value.** Of the rarest queue's seven tickets, two
    carried a right-queue answer under both the review notice and v2b's
    paragraph. §0 asks for five.
- **At the rarest queue's tickets, the impasse notice wrote the region in 40 of
  42 answers**, against 15 of 42 under v2b's paragraph. But the loops on record
  never met an impasse there. Every escalation at those tickets was a reported
  error or a conflict (§0's figure 3). The notice that gives the region back
  there is not the one a loop would send there.
- **The instrument held.** Asked again, v2b's paragraph wrote the region as it
  did in `PLAN_HALVES.md`, ticket by ticket: a mean difference of −0.0259,
  with an error of 0.0325, over 135 tickets (`CA-a` holds). The gap between the
  empty base and v2b's paragraph was 0.4195, where that plan found 0.4131
  (`CA-b` holds).

---

## Stage A — the checks, the design and the references

**What was run.** `PYTHONHASHSEED=0 python3 -m cause.sample`, on 2026-11-25,
from `fda8b47`, the signature's commit, on the branch of #308. The record is
[`sample.json`](sample.json).
- **`CA-g1` to `CA-g3` passed with the suite green, and `CA-g4` read the plan
  signed.**
- **§0's three figures came back as declared**: the tickets, the causes the
  reasoning loops met at them, and the causes at `T₇`.
- **The design is §0's.** 4 arms at 136 tickets make 544 prompts. Each pass
  asks every prompt once, the arms interleaved. The rarest queue's session asks
  the 28 prompts at `T₇` four times more: 112 asks.
- **`e` and `v` are `PLAN_HALVES.md`'s prompts**, byte for byte. Stage A checks
  their digests against the ones that plan's Stage A record froze.

---

## Stage B — the asks

**What was run.** `cause/ask.py`, the loop's own first call, under level 3's
manual, with reasoning on and pinned to DeepInfra's fp8 endpoint (§2.6). Its
asker is `PLAN_FIRST_MATCH.md`'s, as `PLAN_HALVES.md` called it, with
`placement/`'s pin.
- **The smoke run** asked two tickets an arm, 8 asks, on 2026-11-25 from 11:06
  to 11:15 UTC. The agent launched it detached from its harness. Its check
  passed: every answer was valid, and every attempt was served by DeepInfra,
  reasoned and ended `stop`.
- **The two passes and the rarest queue's session** were launched by the agent,
  as Sergi chose under §2.5, through a supervisor detached from the agent's
  harness.
  - **What it did.** It ran them one at a time and committed each record
    alone, through the pre-commit hook. Then it pushed the record to #308.
  - **What it never did.** It never passed the overwrite flag, never skipped
    the hook, and never merged.
  - **Each session ran in one launch.** No outage stopped one, and none was
    resumed.

| session | asks | first answer kept | last answer kept | valid | failed | retried |
|---|---|---|---|---|---|---|
| smoke run | 8 | 2026-11-25 11:06 | 2026-11-25 11:15 | 8 | 0 | 0 |
| pass 1 | 544 | 2026-11-25 11:40:32 | 2026-11-25 20:42:56 | 544 | 0 | 0 |
| pass 2 | 544 | 2026-11-25 20:52:17 | 2026-11-26 05:21:06 | 544 | 0 | 0 |
| the rarest queue's session | 112 | 2026-11-26 05:29:46 | 2026-11-26 07:10:23 | 112 | 0 | 0 |

**Every attempt of the four sessions was served by DeepInfra and ended
`stop`.** None was refused for the rate, so none was waited out. Every ask is
one attempt.

| session | median prompt tokens | median completion tokens | median reasoning tokens | median seconds | mean seconds | billed, by generation id |
|---|---|---|---|---|---|---|
| pass 1 | 1,798.5 | 4,324.5 | 4,157 | 53.0 | 59.9 | $0.4970 |
| pass 2 | 1,798.5 | 4,444.5 | 4,261 | 49.0 | 56.2 | $0.4928 |
| the rarest queue's session | 1,798.5 | 4,146 | 4,009 | 51.2 | 54.3 | $0.0940 |

**The bill was $1.0927 in all**, the smoke run's $0.0089 included, for 1,208
attempts, every one billed. It is read by generation id, with the key in the
environment.
- **§1's estimate was about $1.34 for the 1,200 asks after the smoke run.** It
  took the smoke run's price per token. The 1,200 cost $1.0838.
- **The effective price fell across the sessions.** It is read as the bill
  over the prompt tokens plus twice the completion tokens. A million such
  tokens cost $0.0828 in the smoke run, $0.0816 in pass 1, $0.0803 in pass 2
  and $0.0790 in the rarest queue's session. Nothing here says why.

---

## Stage C — the six adjudications

**What was run.** `PYTHONHASHSEED=0 python3 -m cause.score`, on 2026-11-26.
It ran from `main` at `56bfefc`, after #308 had merged, and wrote its record at
07:35 UTC.
- **Its dry run ran first.** In both, `CA-g1` to `CA-g4` passed again, with the
  suite green.
- **The record** is [`score.json`](score.json).

**Every statistic is a ratio of integer counts, compared with its line
exactly.** The record keeps each as a fraction beside its float. The standard
errors are clustered by ticket, and only mark *thin*.

**No answer was invalid as §0 reads it**, so no row lost its value to invalid
answers.

| row | statistic | line | reading | read | verdict |
|---|---|---|---|---|---|
| CA-a | the mean, over the tickets where `v` named the right queue both today and in `PLAN_HALVES.md`'s two passes, of today's share less that plan's | from −1/10 to 1/10 | **−0.0259**, −7/270 (se 0.0325) | 135 tickets, both passes | **holds** |
| CA-b | `W_e − W_v` | ≥ 1/5 | **0.4195**, 9857/23496, from **0.7491** and **0.3295** (se 0.0356) | 136 tickets, both passes | **holds** |
| CA-c | `W_i − (W_e + W_v)/2` | ≥ 0 | **0.2259**, 2621767/11607024, with `W_i` **0.7652** (se 0.0345) | 136 tickets, both passes | **holds** |
| CA-d | `W_i − W_r` | ≥ 1/10 | **0.0729**, 18/247, from **0.7652** and **0.6923** (se 0.1350) | 136 tickets, both passes; 13 right-queue answers under `r` | **refuted, thin** |
| CA-e | `W_r⁷ − W_v⁷` | ≥ 1/5 | no value: 2 of `T₇`'s tickets carry a right-queue answer under both `r` and `v`, and §0 asks for 5 | `T₇`'s 7 tickets, both passes and the rarest queue's session | **unadjudicable** |
| CA-f | `B_v − B_i` | ≥ 1/5 | **0.6817**, 11113/16302, from **0.7424** and **0.0607** (se 0.0299) | 136 tickets, both passes | **holds** |

`CA-g` is reported, and everything below that is not in the table is its.

**`CA-d` is thin on both of §0's counts.**
- **It lies within one standard error of its line.** It is 0.0271 below the
  line, against an error of 0.1350. The error is that large because `W_r`
  rests on 13 answers.
- **Pass 2 alone puts it on the other side.** Read on pass 2 alone it is
  0.2623, above the line, and on pass 1 alone −0.2320.

**No other verdict is thin.**
- **No other statistic lies within one standard error of its line**, or of the
  nearer edge of `CA-a`'s band. `CA-a` comes nearest: −0.0259 lies 0.0741
  inside the band's lower edge, against an error of 0.0325.
- **Neither pass alone puts any of them on the other side:**

| row | pass 1 alone | pass 2 alone | both passes | standard error |
|---|---|---|---|---|
| `CA-a` | −0.0269 (−7/260) | −0.0265 (−7/264) | −0.0259 (−7/270) | 0.0325 |
| `CA-b` | 0.3860 (354/917) | 0.4528 (8069/17822) | 0.4195 (9857/23496) | 0.0356 |
| `CA-c` | 0.2467 (28282/114625) | 0.2051 (445925/2174284) | 0.2259 (2621767/11607024) | 0.0345 |
| `CA-d` | −0.2320 (−29/125) | 0.2623 (16/61) | 0.0729 (18/247) | 0.1350 |
| `CA-f` | 0.6688 (10952/16375) | 0.6945 (11269/16226) | 0.6817 (11113/16302) | 0.0299 |

**`CA-e` has no value, by §0's own rule.** Two of `T₇`'s seven tickets, 710
and 1783, carried a right-queue answer under both `r` and `v`, and §0 gives the
row no value with fewer than five.
- **Both shares are kept.** `W_r⁷` is 1/3, from the 3 right-queue answers among
  `r`'s 42 at `T₇`. `W_v⁷` is 5/14, from 42.
- **Leaving one ticket out is not read** for a row with no value.
- **Its verdict is written `unadjudicable`**, the scorer's word for a row with
  no value, which `cause/score.py` takes from `halves/score.py`. This is the
  first record whose row carries that word as its verdict string.
  `tests/test_prose_tables.py` read only `"unadjudicable": true` as a flag, and
  learns to read the string in the commit that adds this thread.

**`CA-c` and `CA-f` had a value.** §0 gives `CA-c` none if `W_e − W_v` is a
tenth or less, and it is 0.4195. It gives `CA-f` none if `B_v` is a fifth or
less, and it is 0.7424.

**The drafter expected `CA-a`, `CA-b`, `CA-c`, `CA-d` and `CA-f` to hold, and
`CA-e` to be refuted.** It trusted `CA-b` most, then `CA-a`, `CA-d`, `CA-f` and
`CA-c`. Its bet was `CA-c`.
- **Four of the six came out as expected**: `CA-a`, `CA-b`, `CA-c` and `CA-f`.
- **Its bet, `CA-c`, holds**, by more than six of its standard errors.
- **`CA-d`, which it trusted third, is refuted, thin.** Its account of the
  review notice was about the region, and the notice moved the queue.
- **`CA-e`, which it expected to be refuted, has no value**, for the same
  reason.

That is a fact about this plan, and the scoreboard counts it.

### The four arms

Every count below reads both passes at the 136 tickets, 272 answers an arm,
unless it says otherwise.

| arm | wrong queue | right-queue answers, `R` | whole | cut by one listed rule | cut by two | other | `W` | `BETWEEN` | `B` |
|---|---|---|---|---|---|---|---|---|---|
| `e`, the empty base | 5 | 267 | 200 | 35 | 0 | 32 | 0.7491 | 72 | 0.2697 |
| `v`, v2b's paragraph | 8 | 264 | 87 | 87 | 2 | 88 | 0.3295 | 196 | 0.7424 |
| `i`, the impasse notice | 25 | 247 | 189 | 8 | 0 | 50 | 0.7652 | 15 | 0.0607 |
| `r`, the review notice | 259 | 13 | 9 | 2 | 0 | 2 | 0.6923 | 3 | 0.2308 |

- **No answer of any arm was classed *no rule*,** and every valid answer named
  a queue.
- **By pass:**
  - `W_e` was 0.7143 and 0.7836;
  - `W_v` was 0.3282 and 0.3308;
  - `W_i` was 0.7680 and 0.7623;
  - `W_r` was 1.0000 on pass 1's 5 right-queue answers, and 0.5000 on pass
    2's 8.
- **Weighted by ticket** rather than pooled, `W` was 0.7426, 0.3199, 0.7597 and
  0.6667, in the table's order.
- **The empty base beside `PLAN_HALVES.md`'s.** Today it wrote the region in
  200 of 267, 0.7491. That plan's, asked on the same prompts and pin two weeks
  earlier, wrote it in 201 of 260, 0.7731. No row reads this.

### The review notice names another queue

**259 of its 272 answers at the 136 tickets named a queue other than the
governing rule's, and 39 of its 42 at `T₇`.** None named no queue, and none
was classed *no rule*.
- **It is the steadiest arm.** A prompt's two answers in the passes shared a
  class in 125 of its 136 prompts, against 99 under the impasse notice, 83
  under the empty base and 75 under v2b's paragraph. Almost all were wrong
  queue twice.
- **Its 13 right-queue answers are what `CA-d` read.** 9 of the 13 were whole.
  `BETWEEN` marked 3 of them. `B_v − B_r`, `CA-f`'s statistic under the other
  notice, is 0.5117 (reported).
- **Which queue it names, and why, this record does not read** (*What Stage C
  does not settle*, below).

### By queue and by governing rule

**By the ticket's true queue**, whole answers out of right-queue answers, both
passes:

| ticket's queue | `e` | `v` | `i` | `r` |
|---|---|---|---|---|
| `ACCOUNT_MANAGER` | 21 of 22 | 9 of 22 | 21 of 22 | 2 of 2 |
| `BILLING_SPECIALIST` | 9 of 10 | 9 of 10 | 10 of 10 | 1 of 1 |
| `ONCALL_ESCALATION` | 11 of 14 | 5 of 14 | 12 of 14 | 1 of 1 |
| `SECURITY_INCIDENT` | 27 of 38 | 14 of 38 | 32 of 37 | 1 of 2 |
| `SELF_SERVICE_DEFLECT` | 24 of 30 | 14 of 29 | 24 of 28 | 3 of 3 |
| `T1_GENERAL` | 27 of 40 | 4 of 38 | 9 of 39 | none |
| `T2_TECHNICAL` | 65 of 92 | 18 of 91 | 59 of 75 | 1 of 2 |
| `T3_ENGINEERING` | 16 of 21 | 14 of 22 | 22 of 22 | 0 of 2 |

- **At every queue's tickets but one, the impasse notice wrote the region at
  least as often as the empty base did.**
- **The exception is `T1_GENERAL`**: 9 of 39, against the empty base's 27 of 40.
  By governing rule, the impasse notice wrote the region at the tickets of
  `H08`, `H28` and `H29` in 13 of 51 answers, against the empty base's 40 of
  55.
- **Most of the impasse notice's 25 wrong-queue answers fell at
  `T2_TECHNICAL`'s tickets**: it had 75 right-queue answers there, where the
  empty base had 92.

### The rarest queue's tickets

Every answer at `T₇`, both passes and the rarest queue's session, six to a
prompt, by class:

| ticket | governing rule | `e` | `v` | `i` | `r` |
|---|---|---|---|---|---|
| 257 | `H05` | 5 whole, 1 other | 4 whole, 2 cut by one | 6 whole | 6 wrong queue |
| 710 | `H05` | 5 whole, 1 other | 2 whole, 1 cut by one, 3 other | 6 whole | 5 wrong queue, 1 cut by one |
| 954 | `H04` | 4 whole, 1 cut by one, 1 other | 2 whole, 3 cut by one, 1 other | 5 whole, 1 other | 6 wrong queue |
| 982 | `H04` | 4 whole, 1 cut by one, 1 other | 1 whole, 5 cut by one | 5 whole, 1 cut by one | 6 wrong queue |
| 1432 | `H04` | 2 whole, 4 cut by one | 6 cut by one | 6 whole | 6 wrong queue |
| 1783 | `H05` | 6 whole | 6 whole | 6 whole | 4 wrong queue, 1 whole, 1 cut by one |
| 1951 | `H04` | 4 whole, 2 cut by one | 5 cut by one, 1 other | 6 whole | 6 wrong queue |

- **The impasse notice wrote the region in 40 of 42**, the empty base in 30 of
  42, and v2b's paragraph in 15 of 42.
- **`W_i⁷ − W_v⁷`, `CA-e`'s statistic under the other notice, is 0.5952**
  (reported).
- **No loop on record would have sent the impasse notice there.** In the 24
  reasoning loops, every escalation at `T₇` was a reported error, but one
  conflict at 710 and one at 954 (§0's figure 3).

### Where the loops met each cause

`CA-g` reads each notice at the tickets where a DeepInfra loop met its cause.
These are §0's figure 2's tickets, both passes.
- **At the 54 tickets where one met an impasse**, `W_i` was 0.7212, `W_e`
  0.7664 and `W_v` 0.3962.
- **At the 63 where one met a reported error**, `W_r` was 1/2, on the few
  right-queue answers `r` gave there. `W_e` was 0.7603 and `W_v` 0.3554.

### What the first call declares, and its codes

**Each arm's valid answers over the three sessions, 300 an arm**, declared
`beats` or `loses_to`:
- 48 under the empty base;
- 144 under v2b's paragraph;
- 144 under the impasse notice;
- 99 under the review notice.

**Every declaration cited the manual's identifiers.** None cited a rule of a
base, since none was shown.

**`halves/hidden.py`'s codes**, over each arm's right-queue answers at the 136
tickets, both passes:

| code | `e` (267) | `v` (264) | `i` (247) | `r` (13) |
|---|---|---|---|---|
| `EMPTY`, the base read as empty | 248 | 7 | 49 | 0 |
| `HIDDEN`, the base read as hidden | 0 | 85 | 245 | 8 |
| `CONFLICT`, a conflict or an overlap named | 150 | 259 | 38 | 5 |
| `BETWEEN`, a conflict named between two listed rules | 72 | 196 | 15 | 3 |
| `INSIDE`, the draft placed inside another rule | 56 | 148 | 54 | 6 |
| `RESOLVES`, the draft said to resolve a conflict | 64 | 105 | 21 | 3 |

- **The impasse notice's reasoning read the base as hidden**, as v2b's
  paragraph says it is, in 245 of 247 answers. It named a conflict in 38.
- **v2b's paragraph** named one in 259 of 264.

### Agreement between the passes

A prompt's two answers in the passes shared a class:
- in 99 of 136 prompts under the impasse notice, 0.7279;
- in 83 under the empty base, 0.6103;
- in 75 under v2b's paragraph, 0.5515;
- in 125 under the review notice, 0.9191.

### What the verdicts say

**`CA-b`, `CA-c` and `CA-f` hold.** §0 read that conjunction before the
signature. Told that no rule matches its ticket, the first call stops reading a
conflict between two of the manual's rules, and gives back at least half the
gap. *"A loop that tells its first call the cause at an impasse has reason to
expect whole drafts there, and the loop plan follows (§12)."* The notice gave
back all of the gap, and its reasoning still read the base as hidden. The
hidden base does not make the first call cut when the first call is told why
the engine stopped.

**`CA-d` is refuted while `CA-c` holds, and §0's reading of that does not fit
what the notice did.** §0 read it as *"any account that is not a conflict gives
the region back, and the review notice does as well as the impasse notice"*.
- **Among the 13 answers that named the right queue, it does**, and `CA-d` is
  thin there.
- **But what the review notice moved was the queue.** 259 of its 272 answers
  named another one. §0 did not foresee that, and no row bands it.
- **A loop that sent this notice at a reported error would mostly get back a
  rule of another queue**, whatever region it drew.
  - **At the 63 tickets where a DeepInfra loop met a reported error**, `r` named
    the right queue in few answers.
  - **The rarest queue's tickets are such tickets.** Every escalation on record
    there but two was a reported error, and `r` named another queue in 39 of its
    42 answers there.

**`CA-e` has no value**, for that reason. Under the impasse notice, the rarest
queue's tickets gave the region back almost every time. But that is the notice
the loops would not have sent there.

**`CA-a` holds.** Today's v2b's paragraph writes the region as `PLAN_HALVES.md`'s
did. So the other rows describe the model that plan read, on the provider that
served both.

### What Stage C does not settle

- **Which queue the review notice names, and why.**
  - **What the records hold.** Each ask keeps the queue it names, its note and
    its reasoning. Stage C counts the wrong-queue answers, and does not tabulate
    which queue they name.
  - **The obvious account is untested.** The model would take the engine's
    decision to be the manual's first match, and name the next rule's queue.
    A POST-RUN reading could set each named queue against the list's later
    matches, and read the reasoning.

  **[NOTE 2026-11-26, later] Read POST-RUN: the model takes the decision for
  the manual's first match.** Every answer's reasoning set the reviewer's mark
  against the governing rule. Most named the next matched rule's queue, as an
  exception nested in the governing rule's region. *Two things Stage C left
  free*, A, below.
- **Whether a loop that sends the impasse notice at its impasses compiles more.**
  The notices were asked alone, at tickets the loops escalated, with the base
  hidden and no placement round. A loop's first call would see the same text.
  The tickets it meets, their causes and every round after the first are the
  loop's (§12).
- **What a review notice would do if it said what the engine decided.** This
  one names no queue, no rule and no decision, so the model had to guess which
  decision erred.
- **Why the impasse notice cuts at `T1_GENERAL`'s tickets**, where it wrote the
  region less often than the empty base. No row reads a queue alone.

  **[NOTE 2026-11-26, later] Read POST-RUN: the cut is the defaults'.** At the
  tickets of `H08`, `H28` and `H29` the notice is read as the default missing
  from the base, and the model writes a narrowing of it kept to its ticket.
  v2b's paragraph had narrowed there the same way. *Two things Stage C left
  free*, B, below.

---

## Two things Stage C left free — POST-RUN

**Asked for by Sergi on 2026-11-26, after Stage C.** *What Stage C does not
settle*, above, names two things the records can answer without a call: which
queue the review notice names, and why, its first item, and why the impasse
notice cuts at `T1_GENERAL`'s tickets, its fourth. These two readings answer
both on the records alone. They spend nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m cause.review` and
`PYTHONHASHSEED=0 python3 -m cause.general`, on 2026-11-26, from `485b7d6` with
its code clean, on the branch of #310, which is `4b2dfc7` on `main`.
- **`4b2dfc7` carries both readings and their expectations**, written and
  committed before either ran on the held-out answers. Each record was
  committed alone after it, as `c7e065f` and `e1c73bc` on `main`.
- **On #310's branch the six commits were `485b7d6`, `da28caa`, `7a991ab`,
  `5a7f597`, `54b0836` and `d9f3dd9`.** Each pair has the same subject, the
  same tree and the same `git patch-id --stable`, and the GitHub API names #310
  behind the six `main` commits.
- **Their `_env` says `git_dirty`**, for the sandbox's empty placeholders in
  the repository's root, untracked. `code_dirty` is false, and the code digest
  is `0c4414106f60c424`.
- **The records are [`review.json`](review.json) and
  [`general.json`](general.json).** Each passed its four gates:
  - every answer of the three sessions is valid as §0 reads it;
  - the passes' classes, recounted by arm, are Stage C's;
  - every answer keeps its reasoning and its payload;
  - its code's counts on pass 1 come back.

**Pass 1 is the development set.** Each code was frozen on it, and every clause
reads the held-out answers: those of pass 2 and of the rarest queue's session.
That session asks only `T₇`'s seven tickets, four times each, so they weigh
more in the held-out answers than in a pass.

### A. Which queue the review notice names, and why

**What it reads.** Every valid answer of `r`: 164 held out, 136 of pass 2 and
28 of the rarest queue's session.
- **The runner-up** is the first rule the ticket matches whose queue is not the
  governing rule's. `H29` matches every ticket, so only the tickets that match
  no rule but `T1_GENERAL`'s have none.
- **The place** of the queue an answer names is the governing rule's, the
  runner-up's, a later matched rule's, or none of theirs.
- **`MARK`** reads the reasoning: the governing rule's identifier or its queue's
  name within the 400 characters before a word of the reviewer's mark. The
  other arms carry no reviewer, so their hits are the code's noise.

| place of the queue it names | pass 1, development | pass 2 | the rarest queue's session | held out |
|---|---|---|---|---|
| the governing rule's | 5 | 8 | 2 | 10 |
| the runner-up's | 89 | 82 | 13 | 95 |
| a later rule's | 14 | 16 | 13 | 29 |
| none of the matched rules' | 28 | 30 | 0 | 30 |

- **It names the runner-up's queue** (V1 holds, by one answer). 95 of the 135
  held-out wrong-queue answers at tickets with a runner-up did, 0.7037.
  - **Pass 2 alone** gives 82 of 109, and 80 of 103 outside `T₇`.
  - **The rarest queue's session** gave 13 of 26.
- **It writes that queue as an exception nested in the governing rule** (V2 and
  V3 hold).
  - **134 of the 154 wrong-queue answers** drafted a region inside the
    governing rule's.
  - **120 of the 124 that named a matched rule's queue** drafted inside the
    first such rule's region, and 48 of them drafted the two rules'
    intersection exactly.
  - **Most declared nothing.** 55 of the 154 declared a side, and 33 of them
    declared the draft above the governing rule.
- **Where no matched rule has the queue it names, it climbs the support
  ladder** (V4 holds). 22 of those 30 answers named the tier above the
  governing rule's queue.
  - **At the tickets only `T1_GENERAL`'s rules match**, 18 of the 19 answers
    named `T2_TECHNICAL`.
  - **At `T2_TECHNICAL`'s tickets**, 4 named `T3_ENGINEERING`.
- **The reasoning sets the reviewer's mark against the governing rule** (V5
  holds). `MARK` was in all 164 answers of `r`, and in 35 of the other arms'
  492: 11 under the empty base, 7 under v2b's paragraph and 17 under the
  impasse notice.

**By the governing rule's queue**, the place of what `r`'s held-out answers
named:

| governing rule's queue | answers | the runner-up's | a later rule's | none | the governing rule's |
|---|---|---|---|---|---|
| `T2_TECHNICAL` | 48 | 39 | 1 | 6 | 2 |
| `ONCALL_ESCALATION` | 35 | 15 | 17 | 0 | 3 |
| `T1_GENERAL` | 20 | 1 | 0 | 19 | 0 |
| `SECURITY_INCIDENT` | 19 | 10 | 6 | 1 | 2 |
| `SELF_SERVICE_DEFLECT` | 15 | 12 | 0 | 2 | 1 |
| `ACCOUNT_MANAGER` | 11 | 9 | 1 | 1 | 0 |
| `T3_ENGINEERING` | 11 | 7 | 2 | 0 | 2 |
| `BILLING_SPECIALIST` | 5 | 2 | 2 | 1 | 0 |

**At the rarest queue's tickets it passes over severity 1's default** (V6, the
bet, fails). 15 of the 32 wrong-queue answers there named the runner-up's
queue. The held-out answers at `T₇`, five a ticket:

| ticket | governing rule | runner-up | what `r` named |
|---|---|---|---|
| 257 | `H05` | `H06`, `T3_ENGINEERING` | `T3_ENGINEERING` 4, `T2_TECHNICAL` 1 |
| 710 | `H05` | `H06`, `T3_ENGINEERING` | `T3_ENGINEERING` 4, `ONCALL_ESCALATION` 1 |
| 1432 | `H04` | `H07`, `T3_ENGINEERING` | `T3_ENGINEERING` 5 |
| 1783 | `H05` | `H06`, `T3_ENGINEERING` | `T3_ENGINEERING` 2, `ONCALL_ESCALATION` 2, `T2_TECHNICAL` 1 |
| 954 | `H04` | `H08`, `T2_TECHNICAL` | `ACCOUNT_MANAGER` 5, the queue of `H13` |
| 982 | `H04` | `H08`, `T2_TECHNICAL` | `ACCOUNT_MANAGER` 5, the queue of `H09` |
| 1951 | `H04` | `H08`, `T2_TECHNICAL` | `T3_ENGINEERING` 5, the queue of `H17` |

- **Where the runner-up is a rule of engineering**, the model named its queue
  in 15 of 20 answers.
- **Where it is `H08`, severity 1 to `T2_TECHNICAL`, the model never named its
  queue.** In all 15 it named the queue of the next rule its ticket matches,
  past `H08`.
- **Read after the verdicts, the later answers outside `T₇` passed over rules
  of the same kind.** 11 of their 12 passed over `H03` at 6, `H12` at 3 and
  `H18` at 2. Each is a rule of one condition that closes a block of the list,
  as `H08` closes severity 1's. It is not every such rule: `H28` and `H29`,
  which close theirs, were the runner-up whose queue an answer named 29
  times.

### B. Why the impasse notice cuts at `T1_GENERAL`'s tickets

**What it reads.** Every valid right-queue answer of `e`, `v` and `i`: 162, 161
and 150 held out.
- **The three rules are Stage C's**: `H08`, `H28` and `H29`, where *By queue and
  by governing rule*, above, found the notice writing the region least beside
  the empty base. Stage C made that selection on both passes, and the reading
  takes it as given. `H28` and `H29` govern all of `T1_GENERAL`'s tickets but
  one, which is `H23`'s.
- **`ABSENT`** reads the reasoning: the governing rule said not to be in the
  base, its identifier and a word of absence within one sentence.
- **`GAP`** reads the note: the draft said to cover what no rule covers.

Whole answers out of right-queue answers, pass 2, by governing rule. The rarest
queue's session asked none of these tickets.

| governing rule | `e` | `v` | `i` |
|---|---|---|---|
| `H08`, severity 1 to `T2_TECHNICAL` | 8 of 9 | 0 of 9 | 2 of 7 |
| `H23`, phone at off hours to `T1_GENERAL` | 1 of 1 | 0 of 1 | 1 of 1 |
| `H28`, business and enterprise to `T1_GENERAL` | 5 of 7 | 2 of 7 | 1 of 7 |
| `H29`, every ticket to `T1_GENERAL` | 8 of 12 | 0 of 12 | 2 of 12 |

- **The notice is read as the governing rule missing from the base** (D1
  holds). `ABSENT` was in 146 of `i`'s 150 answers, against 49 of `e`'s 162 and
  83 of `v`'s 161.
- **At the three rules' tickets, what the notice writes instead of the region
  is a narrowing kept to its ticket** (D2 holds).
  - **19 of `i`'s 21 answers not whole there** were *other*, inside the
    governing rule's region and covering their ticket.
  - **The other two** were cuts by one listed rule, both at `H08`'s tickets.
  - **Summed answer by answer, the 21 held** 36,735 of the 97,380 points of
    their rules' parts, 0.3772.
- **Under v2b's paragraph it was no cut by a listed rule either** (D3 holds).
  21 of `v`'s 26 answers not whole there were *other*.
- **The codebook found *gap* in half of those notes** (D4 fails). `GAP` was in
  11 of the 21, and in 8 of `i`'s 116 whole answers at the other tickets.
  - **Read after the verdict, six of the ten notes it missed say the same in
    other words**: *no explicit routing in the existing rules*, *lack
    coverage*, *que no tienen regla asignada*, *no existe ninguna regla que
    cubra*, *no atendidos por reglas específicas*, *no son capturados por
    reglas específicas*.
  - **The patterns were frozen on pass 1**, whose notes used two of those
    phrasings once each.
- **The empty base's notes do not call it so** (D5 holds): 2 of `e`'s 28
  answers at the three rules' tickets.
- **Elsewhere, the notice's narrowings were not called gaps** (D6, the bet,
  fails). `GAP` was in none of `i`'s 8 answers not whole at the other tickets.
  Read by hand after the verdict, two of them say it in other words.
- **Two notes give the account in so many words.**
  - **At ticket 725, under `H08`**: *"The generic severity 1 rule (H08) is
    absent, so we add this specific rule to route critical mobile issues to
    technical support"*.
  - **At ticket 1807, under `H08`**: *"Segun el manual, para severity=1 la
    accion es T2_TECHNICAL (H08), pero esa regla no esta en la base."*

### The expectation

Written in the two modules' docstrings before either reading ran on the
held-out answers, and committed before them, in `4b2dfc7` on `main`. It is not
signed, and it is on no scoreboard.

| clause | reading | |
|---|---|---|
| V1, among `r`'s wrong-queue answers at tickets with a runner-up, at least 0.70 name the runner-up's queue | 95 of 135 | **holds** |
| V2, at least 0.80 of `r`'s wrong-queue answers draft inside the governing rule's region | 134 of 154 | **holds** |
| V3, of those naming a matched rule's queue, at least 0.80 draft inside the first such rule's region | 120 of 124 | **holds** |
| V4, of those naming a queue no matched rule has, at least 0.70 name the tier above the governing rule's queue | 22 of 30 | **holds** |
| V5, `MARK` in at least 0.90 of `r`'s answers, and in at most 0.25 of the other arms' | 164 of 164, and 35 of 492 | **holds** |
| V6, at `T₇`'s tickets, at least half of `r`'s wrong-queue answers name the runner-up's queue | 15 of 32 | fails |
| D1, `ABSENT` in at least 0.90 of `i`'s answers, and in at most 0.40 of `e`'s | 146 of 150, and 49 of 162 | **holds** |
| D2, under `i`, at least 0.80 of the answers not whole at the three rules' tickets are narrowings kept to their ticket | 19 of 21 | **holds** |
| D3, under `v`, at least 0.60 of the answers not whole there are *other* | 21 of 26 | **holds** |
| D4, `GAP` in at least 0.60 of `i`'s answers not whole there, and in at most 0.20 of `i`'s whole answers at the other tickets | 11 of 21, and 8 of 116 | fails |
| D5, `GAP` in at most 0.15 of `e`'s answers at the three rules' tickets | 2 of 28 | **holds** |
| D6, `GAP` in at least half of `i`'s answers not whole at the other tickets | none of 8 | fails |

**V1 to V5 hold, and V6 fails. D1, D2, D3 and D5 hold, and D4 and D6 fail.**
- **Both bets failed**: V6 at `T₇`'s tickets, where the model passed over
  `H08`, and D6 at the other tickets, where the notice's narrowings were not
  called gaps.
- **V1, trusted most, held by one answer.** The rarest queue's session asks
  `T₇` four times, and pass 2 alone held by more.
- **D1, trusted most, held.** D4 failed on its codebook: the notes said *gap*
  in words its patterns, frozen on pass 1, did not hold.

### What it says

- **Told that a reviewer marked the decision wrong, and nothing of the
  decision, the model takes it for the manual's first match.** Every answer's
  reasoning set the mark against the governing rule.
  - **Then it rules that queue out**, and names the next matched rule's.
  - **It writes it as an exception nested in the governing rule's region**,
    which wins there by containment.
  - **Where no rule of another queue matches, it climbs the support ladder.**
- **So the notice moved the queue because the model guessed the decision, and
  guessed the queue that is right.** At a reported error the base decided
  another queue than the manual's first match. A notice that names what the
  base decided would not leave it to the guess.
- **At the rarest queue's tickets the guess passes over severity 1's default.**
  Where the runner-up was `H08`, the model named the queue of the next rule
  past it, an account manager's or engineering's, and never `T2_TECHNICAL`.
- **Told that no rule of the base matches, the model reads the governing rule
  as missing from the base, and writes it back, but at a default.** At the
  tickets of `H08`, `H28` and `H29` it writes instead a narrowing of the default
  kept to its ticket: the ticket's own combination inside the default's
  region. Two notes say so: the default is absent, so a specific rule is added.
- **The cut at `T1_GENERAL`'s tickets is the defaults', and v2b's paragraph
  made it too.** Its answers not whole there were narrowings of the same kind,
  and not cuts by a listed rule. What the notice took away, a conflict read
  between two listed rules, was never what cut there.

### What it does not settle

1. **Why the model writes a narrowing instead of the missing default.** The
   notes say the default is absent and add a specific rule. They do not say
   why specific. Pass 1's reasoning named the default's breadth in most
   answers at the three rules' tickets, whole or not, so breadth told nothing
   apart there. Free on the records, with a codebook built for it.
   **[NOTE 2026-11-26, last] Read POST-RUN: the narrowing is a particular case
   of the missing default, which holds many rules of other queues.** Where the
   model narrows, under every arm, its reasoning places the draft inside the
   governing rule. Told that no rule matches, it writes a missing rule back
   where few rules of other queues lie inside it. At the three, which hold
   many, it mostly writes a rule nested in the default instead. *One thing the
   two readings left free*, C, below.
2. **What a review notice that names the decision does.** At a reported error
   the loop knows the queue its base decided and the rule that decided it.
   Whether the model then keeps the governing rule's queue, and still passes
   over a default, takes calls. It is Stage C's third item.
3. **Whether a loop that sends the impasse notice compiles more**, with
   narrowings to expect at the defaults' tickets. Stage C's second item, and
   calls.

---

## One thing the two readings left free — POST-RUN

**Asked for by Sergi on 2026-11-26, after the two readings.** Their *What it
does not settle*, above, names one more thing the records can answer without a
call: why the model writes a narrowing instead of the missing default, its first
item. This reading answers it on the records alone. It spends nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m cause.narrow`, on 2026-11-26,
from `482180e` with its code clean, on the branch `cause-narrow`.
- **The commit.** `482180e` carries the reading and its expectation, written
  and committed before it ran on the held-out answers. Nothing was added after
  the run.
- **The record was committed alone**, as `7e24681`.
- **Its `_env` says `git_dirty`**, for the sandbox's empty placeholders in the
  repository's root, untracked. `code_dirty` is false, and the code digest is
  `d7cf6d135e7fbc18`.
- **The record is [`narrow.json`](narrow.json).** Its five gates passed:
  - every answer of the three sessions is valid as §0 reads it;
  - the passes' classes, recounted by arm, are Stage C's;
  - every answer keeps its reasoning and its payload;
  - its codes' counts on pass 1 come back, over the answers B read there;
  - of the rules that govern the passes' tickets, those whose regions hold four
    or more rules of another queue are the three, and those that hold one to
    three are `H03`, `H12`, `H16` and `H18`.

**Pass 1 is the development set**, as in A and B, and every clause reads the
held-out answers. The three rules and the few govern none of the rarest queue's
tickets, so the clauses at their tickets read pass 2.

### C. Why the model narrows a missing default

**What it reads.** Every valid right-queue answer of `e`, `v` and `i`, as B
does: 162, 161 and 150 held out.
- **A rule's group** counts the rules of another queue whose regions lie whole
  inside the rule's region, the rule aside. It reads the manual's regions, and
  no truth.
  - **The many**, four or more, are the three. `H08` holds `H04` to `H07`,
    `H28` holds 7, and `H29` holds all 26 rules of another queue.
  - **The few**, one to three, are `H03`, `H12`, `H16` and `H18`. They close the
    keyword's, billing's, the api's and the integrations' blocks of the list, as
    the three close theirs.
  - **None** is every other rule that governs a ticket of the passes.
- **`INSIDE`** reads the reasoning: a sentence that places a draft inside the
  governing rule. The draft is called a *subset* of the rule, *contained* in it
  or *more specific than* it, or the rule is said to *contain* the draft.
- **`CONTAINER`** reads the reasoning: a sentence that places the other rules
  inside the draft, or has the draft yield to the more specific rules.
- **`HOLDS_NONE`** reads no text: the draft holds no rule of another queue.

Whole answers out of right-queue answers, held out, by the governing rule's
group. The few and the three were asked in the passes alone.

| governing rule's group | `e` | `v` | `i` |
|---|---|---|---|
| none | 76 of 96 | 46 of 96 | 91 of 95 |
| few, `H03`, `H12`, `H16` and `H18` | 27 of 38 | 6 of 37 | 25 of 29 |
| many, the three | 21 of 28 | 2 of 28 | 5 of 26 |

The answers that carry each code, held out, out of the answers in the row
above them:

| | `e` whole | `e` not whole | `v` whole | `v` not whole | `i` whole | `i` not whole |
|---|---|---|---|---|---|---|
| answers at the three rules' tickets | 21 | 7 | 2 | 26 | 5 | 21 |
| `INSIDE` | 7 | 6 | 2 | 25 | 0 | 12 |
| `CONTAINER` | 4 | 1 | 0 | 1 | 3 | 0 |
| `HOLDS_NONE` | 0 | 6 | 1 | 26 | 1 | 21 |
| answers at the other tickets | 103 | 31 | 52 | 81 | 116 | 8 |
| `INSIDE` | 21 | 30 | 31 | 79 | 19 | 6 |

- **Where the model narrows, its reasoning places the draft inside the governing
  rule** (S2 holds). Under `e` and `i`, `INSIDE` was in 54 of the 67 answers not
  whole, and in 47 of the 245 whole ones. Under `v`, which S2 leaves out, it was
  in 104 of 107 and in 33 of 54.
- **At a missing default it did so in just over half** (S1 fails). `INSIDE` was
  in 12 of `i`'s 21 answers not whole at the three rules' tickets, where pass 1
  had 14 of 17. The line asked for 13.
  - **Read by hand after the verdict, three of the nine misses say it in other
    words**: *Actually it's a subset of H08*, *that would be more specific than
    H08 if H08 existed*, and, past the code's window, *if that rule existed, it
    would cover all tickets including ours, and our rule would be a subset*, of
    `H29`.
  - **The other six never set the draft inside the default**, by its identifier
    or as the catch-all. Each note calls the draft what no rule covers. Three
    say it in `GAP`'s words. The other three say it in words B lists among
    `GAP`'s misses: *que no tienen regla asignada*, *no atendidos por reglas
    específicas*, *no son capturados por reglas específicas*.
- **Under the empty base, its narrowings there were particular cases of the
  default too** (S6, the bet, holds): 6 of `e`'s 7.
- **The narrowing holds no rule of another queue** (S4 holds). 53 of the 54
  answers not whole at the three rules' tickets held none. The one that held
  some was `e`'s at ticket 106, under `H28`: it held `H04`, `H09` and `H13`.
- **A missing rule that holds few is written back** (S5 holds). Under `i`, 25 of
  the 29 right-queue answers at the few's tickets were whole: 4 of 4 at `H03`, 3
  of 4 at `H12`, 11 of 11 at `H16` and 7 of 10 at `H18`.
- **Written whole, the default is reasoned as the rule the others lie inside**
  (S3 holds, at its line). `CONTAINER` was in 3 of the 7 whole answers of `v`
  and `i` at the three rules' tickets, all three of them `i`'s. It was in 1 of
  the 47 answers not whole. The line asked for 3.
- **The groups go another way under the empty base**, as they did on pass 1. It
  wrote the few whole in 27 of 38, and the three in 21 of 28.

### The expectation

Written in the module's docstring before the reading ran on the held-out
answers, and committed before it, in `482180e`. It is not signed, and it is on
no scoreboard.

| clause | reading | |
|---|---|---|
| S1, under `i`, `INSIDE` in at least 0.60 of the answers not whole at the three rules' tickets | 12 of 21 | fails |
| S2, under `e` and `i`, over every ticket, `INSIDE` in at least 0.75 of the answers not whole, and in at most 0.25 of the whole ones | 54 of 67, and 47 of 245 | **holds** |
| S3, under `v` and `i`, at the three rules' tickets, `CONTAINER` in at least 0.40 of the whole answers, and in at most 0.15 of those not whole | 3 of 7, and 1 of 47 | **holds** |
| S4, at the three rules' tickets, at least 0.85 of the answers not whole, under `e`, `v` and `i` together, hold no rule of another queue | 53 of 54 | **holds** |
| S5, under `i`, at least 0.70 of the right-queue answers at the few's tickets are whole | 25 of 29 | **holds** |
| S6, under `e`, `INSIDE` in at least 0.60 of the answers not whole at the three rules' tickets | 6 of 7 | **holds** |

**S2 to S6 hold, and S1 fails.**
- **The bet held**: S6, under the empty base.
- **S4, trusted most, held**, and so did S2. S1, trusted third, failed by one
  answer, and partly on its codebook: three of its misses said it in other
  words.
- **S3 held at its line**, on 7 whole answers.

### What it says

- **When the model narrows, it writes a particular case of the governing rule.**
  Under every arm, its reasoning places the draft inside the rule, and the draft
  holds no rule of another queue.
- **Told that no rule matches, it writes the missing rule back where few rules
  of other queues lie inside it.** At the three, where many do, it mostly does
  not.
- **There, most of its narrowings are particular cases of the missing default,
  *if it existed*, and the rest fill what they call a gap.** When it writes the
  default whole, its reasoning has the other rules lie inside it and beat it.
- **So the narrowing at a missing default is the model declining to write a rule
  under which rules it believes stand would nest.** It writes one nested in the
  default instead. The declarations do not explain it. `H29` holds every rule
  of another queue, so written whole it needs no declaration, and 10 of `i`'s
  12 answers there were narrowed.
- **The codes say which account goes with the narrowing, not that a text caused
  it.** The system prompt calls the proposer the system's exception component,
  and says a particular case of another rule needs no declaration. Only a text
  that says otherwise could tell whether that is why.

### What it does not settle

1. **Whether a text gets the default written whole.** The impasse notice could
   say that the rules nested in the missing rule stand, and win inside it
   without a declaration. Or the system prompt could say what a rule that
   holds others does under level 1. It is the loop with the impasse notice's
   question too. Calls.
2. **Why the empty base writes the few whole less often than the three.** Under
   `e` the groups run the other way, on both passes. Free on the records.

---

## Files

- [`sample.json`](sample.json): Stage A. The design, the texts and their
  digests, the tickets with their governing rules, and §0's three figures.
- [`ask_smoke.json`](ask_smoke.json): the smoke run's 8 asks.
- [`ask_pass1.json`](ask_pass1.json) and [`ask_pass2.json`](ask_pass2.json):
  the two passes, 544 asks each, each with its call attempts.
- [`ask_oncall.json`](ask_oncall.json): the rarest queue's session, 112 asks.
- [`score.json`](score.json): Stage C. The six verdicts with their fractions,
  errors and passes, and `CA-g`.
- [`review.json`](review.json): POST-RUN, which queue the review notice names,
  and why. Every answer of `r` read, and of the other arms the code alone,
  with the six clauses.
- [`general.json`](general.json): POST-RUN, why the impasse notice cuts at
  `T1_GENERAL`'s tickets. Every right-queue answer of `e`, `v` and `i` read,
  with the six clauses.
- [`narrow.json`](narrow.json): POST-RUN, why the model narrows a missing
  default. Every right-queue answer of `e`, `v` and `i` read, with what its
  governing rule and its draft hold of the rules of another queue, its two
  codes and the six clauses.

Every ask keeps its prompt and its digest, the answer's payload, which holds its
note, and its reasoning, whole. It also keeps its call attempts as
`call_attempts`: generation id, provider, model, both finish reasons and the
tokens.
