# What the loop's first call writes when it is told why its ticket escalated — findings

Record opened on November 26, 2026, under [`PLAN_CAUSE.md`](../PLAN_CAUSE.md).
Sergi signed §0 on 2026-11-25, before any figure below existed, in a commit of
its own: `8fbc42f` on `main`.
- **The plan, its package, the signature, Stage A, the smoke run and the three
  sessions** reached `main` in #308, merged on 2026-11-26.
- **Stage C, this record, the banner that closes the plan and the indexes**
  reach it in the pull request this record was opened in.

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

Every ask keeps its prompt and its digest, the answer's payload, which holds its
note, and its reasoning, whole. It also keeps its call attempts as
`call_attempts`: generation id, provider, model, both finish reasons and the
tokens.
