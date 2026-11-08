# The placement round that lists only what the engine can still order — findings

Record opened on November 8, 2026, under [`PLAN_PLACEMENT.md`](../PLAN_PLACEMENT.md).
The plan and its package reached `main` in pull request #207, merged on
2026-11-07. Sergi signed §0 on 2026-11-07, before any figure below existed, in a
commit of its own: `0b39ae8` on `main`.
- **The signature, Stage A and the smoke run** reached `main` in #208, merged on
  2026-11-07.
- **The bridge and the six runs** reached it in #209, merged on 2026-11-08.
- **Stage C, this record, the banner that closes the plan and the indexes**
  reach it in #210, the pull request this record was opened in.
- **The POST-RUN reading of `ONCALL_ESCALATION`** reached it in #211, merged on
  2026-11-08.

Every record names in its `_env` the commit it was written from. Eight were
written on a pull request's branch, and the rebase merge gave each of those
commits a new hash on `main`. Each pair has the same subject, the same tree and
the same `git patch-id --stable`, and the GitHub API names the pull request
behind every `main` commit.

| record | written from | the same commit on `main` | code digest |
|---|---|---|---|
| `sample.json` | `c3ac216`, the signature, on the branch of #208 | `0b39ae8` | `f89d036fc2068249` |
| `loop_smoke.json` | `54bcf72`, Stage A's commit, on the branch of #208 | `495fb50` | `f89d036fc2068249` |
| `bridge.json` | `2273b6b`, the smoke run's commit, on `main` (#208) | itself | `f89d036fc2068249` |
| `loop_v1c_r1.json` | `9f4b314`, the bridge's commit, on the branch of #209 | `21caf98` | `f89d036fc2068249` |
| `loop_v1b_r1.json` | `350480d`, v1c r1's commit, on the branch of #209 | `bfcf3f3` | `f89d036fc2068249` |
| `loop_v1c_r2.json` | `59aa7f1`, v1b r1's commit, on the branch of #209 | `2afa07b` | `f89d036fc2068249` |
| `loop_v1b_r2.json` | `99f5204`, v1c r2's commit, on the branch of #209 | `b2e230a` | `f89d036fc2068249` |
| `loop_v1c_r3.json` | `84f40ab`, v1b r2's commit, on the branch of #209 | `bab19b2` | `f89d036fc2068249` |
| `loop_v1b_r3.json` | `ba97952`, v1c r3's commit, on the branch of #209 | `33252d2` | `f89d036fc2068249` |
| `score.json` | `da0cb01`, v1b r3's commit, on `main` | itself | `f89d036fc2068249` |

**`git_dirty` and `code_dirty` are false in every record, and every record carries
one code digest.** `main` computes it at `da0cb01`, with
`harness.provenance.code_digest`. The package's code did not change after the
signature.

> **[NOTE 2026-11-08] One more record, written after Stage C by code added
> after it.** [`oncall.json`](oncall.json) is the POST-RUN reading of
> `ONCALL_ESCALATION`.
> - **It was written from `9cb6dd0`**, on the branch of #211, which is `e798813`
>   on `main`. Its section below names the pair's checks.
> - **Its code digest is `74dd22f0826b3731`**, not the package's, because
>   `placement/oncall.py` was added after Stage C. The modules Stage C ran did
>   not change.
>
> **[NOTE 2026-11-08, later] And a second.** [`provider.json`](provider.json)
> reads the bridge at the queue's tickets. It carries code digest
> `a515c2a31d3ccfbe`, because `placement/provider.py` was added after both.
> Its section below says what it was written from.

**This record owns every figure in it.**

**All three stages ran on 2026-11-07 and 2026-11-08, and the six rows are
adjudicated. `PL-a`, `PL-b`, `PL-c` and `PL-d` hold, `PL-c` thinly, as §0 said
every hold of it would be. `PL-e` is refuted, thinly, and `PL-f` is refuted.
`PL-g` is reported.**

- **The new round takes most of the refusals away.** v1c's median run left 8 of
  its 87 escalations unplaced, and v1b's 21 of 86: a ratio of 0.3766.
  - Each of v1c's 22 unplaced answers left out a rule crossing its draft.
  - Of v1b's 59, 28 left out only rules nested with their draft, which v1c never
    lists.
- **Under the new round, half the reports compile the policy in every run.**
  v1c's three bases decide 0.9674, 0.9683 and 0.9510 of the space. Each decides
  the keyword half whole or within 0.0015 of it.
- **It costs nothing against v1b within one period, and its median run is
  better.** v1b's median base decides 0.8968 of the space, 0.0706 less than
  v1c's.
- **v1b does not compile the policy again on the new period and provider.** Its
  bases decide 0.8778, 0.9601 and 0.8968. The two below 0.90 lose part of
  `SECURITY_INCIDENT`, recalling 0.7667 and 0.9206 of its points. Each v1c base
  recalls at least 0.9980 of them.
- **Neither arm compiles the rarest queue.** v1c's median recall of
  `ONCALL_ESCALATION` over the space is 128/315.
  - Run 3's draws let the transcriber compile the whole queue, and let
    `PLAN_CHANNEL.md`'s c r3 recall 14/15 of it on Baidu.
  - Under them, v1c recalls 1/15 of it and v1b none.
- **The drafter expected five rows to hold and `PL-f` to be refuted.** `PL-e`,
  expected to hold thinly, was refuted thinly.

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Its references were
> computed after the signature. Zero API calls.
>
> **PROVENANCE, STAGES B AND C: PRE-REGISTERED.** `PL-a` to `PL-f` were signed
> before any of their figures existed, and none of their bands was set on a
> development set. **`PL-e` is a replication** of `CH-a` on a new period and a
> new provider. Its band was drafted after `CH-a`'s figures had been seen, as §0
> says, and the scoreboard should read it as a replication.
>
> **WHAT WAS SEEN BEFORE STAGE C.** The agent that launched the runs saw, before
> the scorer ran:
> - **Each record's commit message**, which the supervisor wrote from the
>   record. It gives the run's span and launches, the providers that served it,
>   its attempts' finish reasons, the attempts refused for the rate and its
>   `_env`. It counts nothing a row reads (§6.18).
> - **The supervisor's log**: each launch, record, commit and push, with its hour.
> - **The runs' progress, read as the case reached and nothing else.** The
>   bridge's was read as the ask, its case and its provider.
> - **The smoke run's record**, before the bridge: its calls, attempts,
>   providers, finish reasons, pace by round, tokens and bill. No row reads it.
> - **v1b r1's partial file during the run**: how many of its attempts had been
>   refused for the rate or had failed, none, and the hour of its last answer.
> - **v1b r2's record once it was written**: its one attempt that ended at the
>   token budget, and that no call had failed outright.
>
> The bridge's bills and the runs' were read after Stage C. No base, no `space`,
> no recall, no `refused(r)` and no row was read before Stage C.

**Each figure names its surface.**
- **`PL-b`, `PL-c`, `PL-d` and `PL-e`** read the exhaustive space of 134,400
  points.
- **`PL-f`** reads its 6,300 points whose true queue is `ONCALL_ESCALATION`.
- **`PL-a`** reads the runs' escalations.
- **`PL-g`** reads both surfaces and says which.

The corpus is `generate_corpus(2000, seed=17)` in every run. **Both arms run
`PLAN_CHANNEL.md`'s channel arm.** A case escalates on an IMPASSE or a CONFLICT,
and on a wrong decision whose draw falls below 1/2. Run `k` of either arm reads
the draws of `PLAN_CHANNEL.md`'s c r`k`.
- **v1b** is that arm, called and not changed, on DeepInfra.
- **v1c** is v1b with one change, to the placement round's list. It lists a rule
  of another queue that the draft meets only when neither extension strictly
  contains the other, and some point of their shared region is not governed
  when the round is listed (§5.2).

---

## Stage A — the checks and the references

**What was run.** `python3 -m placement.sample`, on 2026-11-07, with
`PYTHONHASHSEED=0`, from the signing commit on a clean tree. The record is
[`sample.json`](sample.json).

**The blocking checks passed before anything was written.**
- **`PL-g1`.** `PLAN_CHANNEL.md`'s verdicts came back from its runs.
  - Under v1b this plan's loop is that plan's channel arm. With run c r1's
    answers replayed, it gives back c r1's record part by part.
  - v1c with both exclusions off is v1b.
  - Every stream of draws is that plan's, and the labels agree with the truth.
  - The suite was green.
- **`PL-g2`.** Every text is `PLAN_REASONED_LOOP.md`'s, as `PLAN_CHANNEL.md`'s
  runs sent it, and every request is §1's.
  - The drafting reading gives back §0's figures 1 to 3.
  - The hidden policy goes through v1c's path whole: 29 rules born and 192 edges
    installed, against v1b's 199. It decides both surfaces right.
  - The transcriber gives back §0's figures.
  - 182 rules were left out on the hidden policy's path and the transcriber's
    v1c runs, the smoke draws' included. None of them changes which rules are
    undefeated at any point.
- **`PL-g3`.** `ORDER_SEED` drew v1c first, so the schedule is v1c r1, v1b r1,
  v1c r2, v1b r2, v1c r3, v1b r3.
  - The smoke run is 30 cases under v1c, with `PLAN_CHANNEL.md`'s smoke draws.
  - The cap is 400 escalations.
  - The bridge's tickets and order are §0's figure 8.
- **`PL-g4`.** One signature line, signed.

**Every figure §0 lists as computed while drafting came back**, figures 1 to 8,
so §0 needs no erratum.

**The draws are `PLAN_CHANNEL.md`'s.** Each stream is 2,000 floats from a string
seed through SHA-512.

| stream | seed string | digest |
|---|---|---|
| run 1 | `PLAN_CHANNEL/channel/97/r1` | `1347b9525a1e06a3` |
| run 2 | `PLAN_CHANNEL/channel/97/r2` | `e81548d721b99577` |
| run 3 | `PLAN_CHANNEL/channel/97/r3` | `1f60e3d5e68553d4` |
| the smoke run | `PLAN_CHANNEL/channel/97/smoke` | `029047351ae2d471` |

**The transcriber**, under each protocol and each run's draws. It is a double
that writes, at every escalation, the rule of level 3's text that governs the
ticket, and places it by the text's order.

| under | protocol | escalations | calls | rounds that met a rule of another queue | rules listed | rounds not sent | `space`, of 134,400 | `corpus`, of 2,000 | `ONCALL_ESCALATION` recall |
|---|---|---|---|---|---|---|---|---|---|
| run 1's draws | v1b | 23: 2 impasses and 21 errors | 45 | 22 | 148 | 0 | 134,380 | 1,999 | 1 |
| run 1's draws | v1c | 23: 2 impasses and 21 errors | 42 | 22 | 108 | 3 | 134,380 | 1,999 | 1 |
| run 2's draws | v1b | 22: 2 impasses and 20 errors | 43 | 21 | 132 | 0 | 132,280 | 1,996 | 2/3 |
| run 2's draws | v1c | 22: 2 impasses and 20 errors | 40 | 21 | 98 | 3 | 132,280 | 1,996 | 2/3 |
| run 3's draws | v1b | 23: 2 impasses and 21 errors | 45 | 22 | 148 | 0 | 134,380 | 1,999 | 1 |
| run 3's draws | v1c | 23: 2 impasses and 21 errors | 42 | 22 | 111 | 3 | 134,380 | 1,999 | 1 |
| the smoke run's draws, 30 cases | v1b | 9: 2 impasses and 7 errors | 17 | 8 | 20 | 0 | 49,420 | 1,107 of 2,000 | 0 |
| the smoke run's draws, 30 cases | v1c | 9: 2 impasses and 7 errors | 16 | 8 | 10 | 1 | 49,420 | 1,107 of 2,000 | 0 |

- **Under each draw, v1c's transcriber escalates, compiles and decides exactly
  as v1b's**, in three calls fewer, and in one call fewer under the smoke draws.
- **A round is not sent** when its list comes out empty, and the draft is born
  at once.

---

## Stage B — the runs

**Every call ran at `deepseek/deepseek-v4-flash`, at temperature 0, with
reasoning `{"effort": "high"}` and 16,000 tokens.**
- **The pin.** The smoke run and the six runs were pinned to DeepInfra's fp8
  endpoint, `deepinfra/fp8`, with fallbacks off. The bridge's Baidu asks carried
  `PLAN_QUEUE_ALONE.md`'s pin.
- **The path.** Every call went through `PLAN_FIRST_MATCH.md`'s asker with
  `PLAN_REASONED_LOOP.md`'s request, under level 3's system prompt: a blind
  first call, then the placement round, v1b's or v1c's.
- **The checks.** Every launch checked the signature, the key, `PL-g1` to
  `PL-g3` and the records before it, before any call.

**How the runs were launched.** Under §2.7 Sergi chose that the agent launch
them.
- **The supervisor**, detached from the agent's harness, ran the bridge, then
  the six runs one at a time, in §2.4's order.
  - It committed each record alone, through the pre-commit hook, before
    anything else started.
  - It never passed the overwrite flag and never skipped the hook.
- **The pull request.** It pushed each record to #209. Once both `ci-complete`
  runs on its last head were green, it merged #209 by rebase, matching that
  head.
- **It skipped its first push.** Its test for an open pull request read a field
  of an empty list, which printed `null null`. It took the pull request for a
  closed one and did not push the bridge's commit.
  - The agent pushed the branch and opened #209 by hand at 20:29 UTC on
    2026-11-07, as v1c r1 began.
  - Every later push, and the merge, went through the supervisor. No run waited
    on it.

### The smoke run

[`loop_smoke.json`](loop_smoke.json) ran 30 cases under v1c, with
`PLAN_CHANNEL.md`'s smoke draws, on 2026-11-07 from 18:08 to 18:34 UTC.
- **What it did.**
  - It met 16 escalations: 15 impasses and 1 reported error.
  - It made 22 calls: 16 first calls and 6 placement rounds.
  - 15 rules were born and 1 was refused. No proposal failed.
- **v1c's list.** 8 escalations met a rule of another queue. 6 rounds were sent
  and 2 were not, because every rule they met lay inside the draft. 3 rounds
  left a rule out.
- **The trigger's record.** Of 3 wrong decisions, the channel reported 1, which
  escalated. 2 stood.
- **The provider.** DeepInfra served every attempt, every one reasoned and
  ended `stop`, and none was refused for the rate.
- **The pace.** The first calls took a median of 78.3 seconds and the placement
  rounds 16.9.
- **The bill**, read by generation id before the bridge, was $0.0187 for its 22
  attempts. That is $0.080 per million prompt tokens, taking completion tokens
  at twice the prompt price, as every listing of the model gives them.
- **The check passed**, so the bridge and the runs could start. No row reads its
  answers.

### The bridge

[`bridge.json`](bridge.json) asked §5.5's 40 first calls of Baidu and of
DeepInfra, each once, on 2026-11-07 from 18:48 to 20:25 UTC, in one launch and
before the first run.
- **The tickets** are §0's figure 8: the 20 of `SECURITY_INCIDENT`, the 7 of
  `ONCALL_ESCALATION`, and 13 drawn from the other tickets `PLAN_CHANNEL.md`'s
  channel runs escalated. DeepInfra was asked first at 22 of them and Baidu at
  18.
- **Every attempt reached its pinned provider and ended `stop`**, 40 on each.
  None was refused for the rate, and none was asked again.
- **The pace.** Baidu's answers took a median of 51.2 seconds, and DeepInfra's
  72.4.
- **The bills.** Baidu's 40 attempts were billed $0.024 and DeepInfra's $0.041:
  $0.044 and $0.082 per million prompt tokens, completion at twice it.

| | Baidu | DeepInfra |
|---|---|---|
| answered with a rule | 40 of 40 | 39 of 40 |
| with the ticket's queue | 40 | 39 |
| whose region is the governing rule's | 18 | 13 |

- **Between the two, on the 39 tickets both answered with a rule**, the queue
  was the same on all 39, and the rule, queue and extension, on 20.
- **Baidu against itself.** `PLAN_CHANNEL.md`'s runs recorded Baidu's drafts of
  the same tickets on 2026-11-05 and 2026-11-06. Against them, Baidu's answers
  of this day make 47 pairs, with the same queue on 46 and the same rule on 21.
- **DeepInfra's answer without a rule** is case 1704's: an empty object, `{}`,
  after 3,915 reasoning tokens.
  - It holds a JSON object, so it is not a failed parse, and the retry by cause
    did not ask it again.
  - Baidu's answer at the same ticket is a rule of `SECURITY_INCIDENT`.

**What it says.** On one day, the two providers chose the same queue on every
ticket both answered. They wrote the same rule on about half, which is about as
often as Baidu writes the same rule across days. DeepInfra wrote the governing
rule's region on 13 of its 39 rules, and Baidu on 18 of its 40. Reported; it
decides nothing, and nothing it answered reached a run.

### The six runs

| run | from its start to its record, UTC | how long | launches | escalations | calls | attempts | refused for the rate | billed |
|---|---|---|---|---|---|---|---|---|
| `v1c r1` | 11-07 20:32 – 11-08 01:05 | 4 h 33 min | 1 | 98 | 186 | 186 | 0 | $0.171 |
| `v1b r1` | 11-08 01:11 – 11-08 05:04 | 3 h 52 min | 1 | 83 | 158 | 158 | 0 | $0.150 |
| `v1c r2` | 11-08 05:10 – 11-08 07:36 | 2 h 26 min | 1 | 68 | 126 | 126 | 0 | $0.101 |
| `v1b r2` | 11-08 07:43 – 11-08 10:22 | 2 h 40 min | 1 | 86 | 165 | 166 | 0 | $0.156 |
| `v1c r3` | 11-08 10:29 – 11-08 13:12 | 2 h 44 min | 1 | 87 | 167 | 167 | 0 | $0.141 |
| `v1b r3` | 11-08 13:18 – 11-08 15:20 | 2 h 02 min | 1 | 78 | 148 | 148 | 0 | $0.124 |

- **A run's start is its record's `started_at`**, which the launch's checks
  precede by about three minutes.
- **Every run reached case 2,000 in one launch.** None stopped at the cap, and
  none recorded a failed proposal.
- **No attempt was refused for the rate.** Every one of the 951 attempts in the
  six runs reached the model.
- **The pin held.** DeepInfra served every attempt.
- **Every attempt ended `stop` but one.** In v1b r2 a first call's first attempt
  spent the whole budget of 16,000 tokens and ended `length`. It was asked again
  with v1's retry message, and the second attempt answered.
- **What was billed** was read from OpenRouter on 2026-11-08, after Stage C, by
  the generation id that each attempt's `call_attempts` keeps. It is not a
  record of this repository.
  - Every attempt that reached the model was found.
  - The six runs came to $0.84, the smoke run to $0.019 and the bridge to
    $0.065.
- **The price per token did not move.** In every hour of the runs, the price per
  million prompt tokens, completion at twice it, was between $0.079 and $0.084.

**Every attempt reasoned.** By run, the median reasoning ran from 3,465 to 4,130
tokens, and the most was 13,851. The records keep the reasoning whole, and no
stage codes it.

| run | calls | attempts | reached DeepInfra | refused for the rate | asked again after a failed parse | prompt tokens | completion tokens | reasoning tokens, median | max |
|---|---|---|---|---|---|---|---|---|---|
| `v1c r1` | 186 | 186 | 186 | 0 | 0 | 398,378 | 846,779 | 3779.5 | 12,741 |
| `v1b r1` | 158 | 158 | 158 | 0 | 0 | 356,795 | 736,985 | 3803 | 11,783 |
| `v1c r2` | 126 | 126 | 126 | 0 | 0 | 260,267 | 497,556 | 3546 | 11,924 |
| `v1b r2` | 165 | 166 | 166 | 0 | 1 | 362,218 | 779,433 | 4130 | 12,695 |
| `v1c r3` | 167 | 167 | 167 | 0 | 0 | 355,868 | 697,591 | 3465 | 13,851 |
| `v1b r3` | 148 | 148 | 148 | 0 | 0 | 319,386 | 613,670 | 3733.5 | 11,239 |

**The pace, by run and by round**, in seconds, from `score.json`. No call met a
refusal, so every call's seconds are its own.

| run | round | calls | median, s | minutes in all |
|---|---|---|---|---|
| `v1c r1` | first call | 98 | 106.0 | 186.5 |
| `v1c r1` | placement | 88 | 44.1 | 86.8 |
| `v1b r1` | first call | 83 | 90.9 | 150.4 |
| `v1b r1` | placement | 75 | 55.5 | 82.0 |
| `v1c r2` | first call | 68 | 79.7 | 103.4 |
| `v1c r2` | placement | 58 | 35.9 | 42.8 |
| `v1b r2` | first call | 86 | 68.5 | 105.7 |
| `v1b r2` | placement | 79 | 33.8 | 54.0 |
| `v1c r3` | first call | 87 | 73.1 | 115.1 |
| `v1c r3` | placement | 80 | 28.4 | 48.5 |
| `v1b r3` | first call | 78 | 54.9 | 83.9 |
| `v1b r3` | placement | 70 | 24.0 | 37.7 |

**The first calls grew faster over the period.** In the order the runs ran,
their medians were 106.0, 90.9, 79.7, 68.5, 73.1 and 54.9 seconds.

**How far §1 was.**
- **The calls.** §1 expected a v1c run to make fewer calls than a v1b run. At
  the medians it made more: v1c's runs made 186, 126 and 167 calls, and v1b's
  158, 165 and 148. Only under run 2's draws did v1c make fewer.
- **The money.** §1 expected the six runs to cost about a dollar, at DeepInfra's
  listing as read on 2026-11-06: $0.09 per million prompt tokens and $0.18 per
  million completion tokens.
  - At that listing their tokens would have cost $0.94.
  - They were billed $0.84, about nine tenths of the listing.
- **The time.** §1 gave the six runs eight to twelve hours, and the bridge about
  an hour, if DeepInfra's pace was Baidu's.
  - It was slower. The six runs took 18 hours 17 minutes between them, and 18
    hours 48 minutes from the first's start to the last's record.
  - The bridge took 1 hour 37 minutes.
- **The smoke run's pace.** It measured the first calls at a median of 78.3
  seconds, on 16 calls. The runs' first calls took medians of 54.9 to 106.0
  seconds, by run.

---

## Stage C — the six adjudications

**What was run.** `PYTHONHASHSEED=0 python3 -m placement.score`, on 2026-11-08,
from `da0cb01` on `main`, on a clean tree.
- **The checks.** `PL-g1` to `PL-g4` passed, with the suite green, before
  anything was written.
- **The runs.** All six were read, and none is missing. Every run's rebuilt base
  is the base its record says it ended with, and every run's calls are the calls
  its record counts.
- **The record** is [`score.json`](score.json). Zero API calls.

**Every statistic is a fraction of counts, compared with its line exactly.**
The record keeps each as a fraction beside its float.

| row | statistic | line | reading | read | verdict |
|---|---|---|---|---|---|
| PL-a | v1c's median `refused(r)`, over v1b's median | ≤ 3/4 | **0.3766**, 688/1827, from 8/87 and 21/86 | 3 runs an arm | **holds** |
| PL-b | v1c's median `space(B)` | ≥ 0.90 | **0.9674**, 743/768 | 3 runs | **holds** |
| PL-c | the number of v1c's runs whose `space(B)` is at least 0.90 | 3 | **3**, of three | 3 runs | **holds, thin** |
| PL-d | v1b's median `space(B)`, less v1c's | ≤ 0.05 | **−0.0706**, −949/13440, from 0.8968 and 0.9674 | 3 runs an arm | **holds** |
| PL-e | v1b's median `space(B)` | ≥ 0.90 | **0.8968**, 24107/26880 | 3 runs | **refuted, thin** |
| PL-f | v1c's median `recall_ONCALL_ESCALATION(B)` over the space | ≥ 0.90 | **0.4063**, 128/315 | 3 runs | **refuted** |

`PL-g` is reported, and everything below that is not in the table is its.

**Two verdicts are thin.**
- **`PL-c` is thin by construction**, as §0 said every hold of it is: it needs all
  three runs. Its lowest run, v1c r3, decides 0.9510 of the space, 0.0510 above
  the line.
- **`PL-e`.** v1b r2's 0.9601, put in place of the median, would hold it.

**Four are not.**
- **`PL-a`.** v1c's highest share, 10/98 in v1c r1, over v1b's median reads
  0.4179. v1b's lowest, 13/78 in v1b r3, under v1c's median reads 0.5517. Both
  stay under 3/4.
- **`PL-b`.** Its lowest run, v1c r3, decides 0.9510.
- **`PL-d`.** v1b r2's 0.9601 in place of v1b's median leaves −0.0073, and v1c
  r3's 0.9510 in place of v1c's leaves −0.0542.
  - As §0 said, with three runs an arm, a hold does not rule out a cost of a
    twentieth.
  - Here none of the six runs moves the statistic across the line.
- **`PL-f`.** No v1c run reaches the line. The highest, v1c r1, recalls 8/15.

**Every row had a value.** Each arm has three complete runs, and v1b's median
`refused(r)` is not 0.

**Each row's runs:**

| run | `space(B)` | `ONCALL_ESCALATION` recall, space | `refused(r)` |
|---|---|---|---|
| `v1b r1` | 1573/1792, 0.8778 | 4,360 of 6,300, 218/315, 0.6921 | 25 of 83, 0.3012 |
| `v1b r2` | 1613/1680, 0.9601 | 3,400 of 6,300, 34/63, 0.5397 | 21 of 86, 0.2442 |
| `v1b r3` | 24107/26880, 0.8968 | 0 of 6,300, 0 | 13 of 78, 0.1667 |
| `v1c r1` | 743/768, 0.9674 | 3,360 of 6,300, 8/15, 0.5333 | 10 of 98, 0.1020 |
| `v1c r2` | 2169/2240, 0.9683 | 2,560 of 6,300, 128/315, 0.4063 | 4 of 68, 0.0588 |
| `v1c r3` | 913/960, 0.9510 | 420 of 6,300, 1/15, 0.0667 | 8 of 87, 0.0920 |

**The drafter expected five rows to hold and `PL-f` to be refuted. Four held,
and `PL-e` was refuted.**
- **The order of trust.** It trusted `PL-a` most, then `PL-b`, `PL-d`, `PL-e` and
  `PL-c`, and expected `PL-f` to be refuted.
- **Where it departed.** `PL-e`, fourth in that order, was expected to hold
  thinly and was refuted thinly.
- **The thin labels** came out where it expected them: `PL-c`'s by construction,
  and `PL-e`'s.

That is a fact about this plan, and the scoreboard counts it.

### The two arms, on both surfaces

| run | `space` | without the keyword | with it | `corpus` | `K-a` | `cover(r)` |
|---|---|---|---|---|---|---|
| `v1c r1` | 0.9674 | 0.9349 | 1.0000 | 1,991 of 2,000 | 2/25 | never |
| `v1b r1` | 0.8778 | 0.9330 | 0.8226 | 1,979 of 2,000 | 7/48 | case 50 |
| `v1c r2` | 0.9683 | 0.9366 | 1.0000 | 1,989 of 2,000 | 7/50 | case 658 |
| `v1b r2` | 0.9601 | 0.9202 | 1.0000 | 1,963 of 2,000 | 7/57 | never |
| `v1c r3` | 0.9510 | 0.9036 | 0.9985 | 1,992 of 2,000 | 2/33 | case 116 |
| `v1b r3` | 0.8968 | 0.8663 | 0.9274 | 1,975 of 2,000 | 5/49 | case 658 |

- **v1c decides the keyword half whole in two runs, and 0.9985 of it in the
  third.** v1b decides 0.8226 of it in v1b r1 and 0.9274 in v1b r3.
- **Without the keyword the arms are closer.** v1c's runs decide 0.9036 to
  0.9366 of that half, and v1b's 0.8663 to 0.9330.
- **On the arrivals the arms barely part.** Every base decides 1,963 to 1,992 of
  the 2,000 cases right.
- **`cover(r)` is the case at which the base's rules first cover every point.**
  It came at case 50 in v1b r1, 116 in v1c r3, and 658 in v1c r2 and v1b r3. It
  never came in v1c r1 and v1b r2.

### The recall of the eight queues

Over the space:

| run | `T1_GENERAL` | `T2_TECHNICAL` | `T3_ENGINEERING` | `BILLING_SPECIALIST` | `SECURITY_INCIDENT` | `ACCOUNT_MANAGER` | `ONCALL_ESCALATION` | `SELF_SERVICE_DEFLECT` |
|---|---|---|---|---|---|---|---|---|
| `v1c r1` | 0.9674 | 0.9966 | 0.8655 | 1.0000 | 1.0000 | 0.9976 | 0.5333 | 1.0000 |
| `v1b r1` | 0.9962 | 0.9935 | 0.7035 | 1.0000 | 0.7667 | 0.9976 | 0.6921 | 1.0000 |
| `v1c r2` | 0.9962 | 0.9978 | 0.9487 | 1.0000 | 1.0000 | 1.0000 | 0.4063 | 1.0000 |
| `v1b r2` | 0.9655 | 0.9521 | 1.0000 | 1.0000 | 1.0000 | 0.9684 | 0.5397 | 1.0000 |
| `v1c r3` | 0.9962 | 1.0000 | 1.0000 | 1.0000 | 0.9980 | 0.9684 | 0.0667 | 0.9860 |
| `v1b r3` | 0.9962 | 0.9617 | 0.7561 | 0.9846 | 0.9206 | 0.9976 | 0.0000 | 1.0000 |

Over the corpus, for the four rarest queues:

| run | `ONCALL_ESCALATION` | `SECURITY_INCIDENT` | `T3_ENGINEERING` | `ACCOUNT_MANAGER` |
|---|---|---|---|---|
| `v1c r1` | 5 of 7 | 20 of 20 | 117 of 117 | 106 of 109 |
| `v1b r1` | 6 of 7 | 14 of 20 | 110 of 117 | 106 of 109 |
| `v1c r2` | 1 of 7 | 20 of 20 | 117 of 117 | 109 of 109 |
| `v1b r2` | 2 of 7 | 20 of 20 | 117 of 117 | 105 of 109 |
| `v1c r3` | 1 of 7 | 20 of 20 | 117 of 117 | 109 of 109 |
| `v1b r3` | 0 of 7 | 16 of 20 | 110 of 117 | 106 of 109 |

- **`SECURITY_INCIDENT`.** Every v1c run recalls at least 0.9980 of its points,
  and all 20 of its tickets. v1b recalls 0.7667 of its points in v1b r1, 1 in
  v1b r2 and 0.9206 in v1b r3.
- **`ONCALL_ESCALATION`.** v1c's runs recall 8/15, 128/315 and 1/15 of its
  points, and v1b's 218/315, 34/63 and none. v1b r1 is the highest of the six,
  at 0.6921.
- **`T3_ENGINEERING`.** v1b r1 and v1b r3 recall 0.7035 and 0.7561 of it. Every
  other run recalls at least 0.8655.

### The placement rounds

`O` is every rule of another queue that a draft meets: the list v1b sends. Under
v1c each rule of `O` is listed or left out, and a left-out rule carries its
reason: inside the draft, containing it, or governed over their shared region.

| run | rounds sent | rounds not sent | `O`, the rules v1b would list | rules listed | listed: crossing / equal / inside / containing | left out: inside / containing / governed |
|---|---|---|---|---|---|---|
| `v1c r1` | 88 | 0 | 910 | 653 | 652 / 1 / 0 / 0 | 40 / 103 / 114 |
| `v1b r1` | 75 | 0 | 816 | 816 | 641 / 4 / 53 / 118 | — |
| `v1c r2` | 58 | 0 | 428 | 352 | 351 / 1 / 0 / 0 | 18 / 25 / 33 |
| `v1b r2` | 79 | 0 | 750 | 750 | 657 / 1 / 33 / 59 | — |
| `v1c r3` | 80 | 1 | 847 | 613 | 612 / 1 / 0 / 0 | 55 / 96 / 83 |
| `v1b r3` | 70 | 0 | 614 | 614 | 541 / 1 / 25 / 47 | — |

- **v1c left 567 rules of 2,185 out of its lists**: 113 inside the draft, 224
  containing it, and 230 crossing it on a region already governed.
- **v1c's lists hold crossing and equal rules only**, as §5.2 sets. v1b's held
  111 rules inside their draft and 224 containing it, beside 1,839 crossing and
  6 equal.
- **One round was not sent**, in v1c r3, because every rule its draft met was
  left out.

**The unplaced answers, by what they left without a side:**

| run | unplaced answers | left out only nested rules | left out only crossing rules | left out both |
|---|---|---|---|---|
| `v1c r1` | 10 | 0 | 10 | 0 |
| `v1b r1` | 25 | 17 | 3 | 5 |
| `v1c r2` | 4 | 0 | 4 | 0 |
| `v1b r2` | 21 | 6 | 13 | 2 |
| `v1c r3` | 8 | 0 | 8 | 0 |
| `v1b r3` | 13 | 5 | 5 | 3 |

- **Every one of v1c's 22 unplaced answers left out only crossing rules.** Its
  lists hold nothing else to leave out.
- **Of v1b's 59, 28 left out only nested rules**, which v1c never lists. 21 left
  out only crossing ones, and 10 both.
- **Crossing rules were left out in both arms**, in about as many rounds: 22
  answers in v1c's 226 rounds, and 31 in v1b's 224 that left out at least one
  crossing rule.

### The drafts, the verdicts and the edges

| run | drafts right | born | unplaced | refused | placement rounds | rules listed, median [range] |
|---|---|---|---|---|---|---|
| `v1c r1` | 92 of 98, 0.9388 | 80 | 10 | 8 | 88 | 6 [1–29] |
| `v1b r1` | 79 of 83, 0.9518 | 56 | 25 | 2 | 75 | 9 [1–30] |
| `v1c r2` | 64 of 68, 0.9412 | 58 | 4 | 6 | 58 | 5 [1–21] |
| `v1b r2` | 82 of 86, 0.9535 | 62 | 21 | 3 | 79 | 9 [1–28] |
| `v1c r3` | 85 of 87, 0.9770 | 75 | 8 | 4 | 80 | 5 [1–41] |
| `v1b r3` | 73 of 78, 0.9359 | 60 | 13 | 5 | 70 | 6 [1–39] |

| run | citations of `H01` to `H29` | other citations | edges by the engine's verdict | copies born | births that are their governing rule's region |
|---|---|---|---|---|---|
| `v1c r1` | 154 | 592 | 506 ok, 58 closing a cycle, 1 outside the neighbourhood | 17 | 27 of 80 |
| `v1b r1` | 179 | 713 | 423 ok, 38 closing a cycle, 20 outside the neighbourhood, 1 against containment | 6 | 22 of 56 |
| `v1c r2` | 70 | 323 | 300 ok, 8 closing a cycle, 8 outside the neighbourhood | 4 | 17 of 58 |
| `v1b r2` | 119 | 613 | 472 ok, 30 closing a cycle, 15 outside the neighbourhood, 1 against containment | 13 | 25 of 62 |
| `v1c r3` | 144 | 556 | 491 ok, 28 closing a cycle, 14 outside the neighbourhood | 12 | 26 of 75 |
| `v1b r3` | 99 | 535 | 409 ok, 60 closing a cycle, 4 outside the neighbourhood | 10 | 21 of 60 |

- **A draft is the first call's queue.** The proposer drafted the right queue at
  241 of v1c's 253 escalations and 234 of v1b's 247.
- **What ended unplaced or refused.** 22 escalations ended unplaced under v1c and
  59 under v1b. The validator refused 18 rules under v1c and 10 under v1b. None
  of these is born.
- **v1c bore 213 rules, and v1b 178.**
- **The citations** count every identifier in `beats` and `loses_to`, over both
  calls of every escalation.
  - The manual's identifiers took the place of the base's in about one citation
    in five: 765 of 4,097.
  - None of them names a rule of a base, and each is dropped and recorded.
- **No v1c edge was refused against containment.** Under v1b, two were.
- **The births that are their governing rule's region**: 70 of v1c's 213, and 68
  of v1b's 178.

**Every v1c birth whose round left a rule out carried the ticket's queue**
(§6.19).

| run | births whose round left a rule out | of them with the ticket's queue | by the birth's queue |
|---|---|---|---|
| `v1c r1` | 47 | 47 | `T2_TECHNICAL` 19, `T3_ENGINEERING` 8, `ACCOUNT_MANAGER` 6, `SELF_SERVICE_DEFLECT` 6, `ONCALL_ESCALATION` 3, `SECURITY_INCIDENT` 3, `BILLING_SPECIALIST` 2 |
| `v1c r2` | 26 | 26 | `T2_TECHNICAL` 11, `SECURITY_INCIDENT` 5, `SELF_SERVICE_DEFLECT` 5, `ACCOUNT_MANAGER` 2, `ONCALL_ESCALATION` 1, `T1_GENERAL` 1, `T3_ENGINEERING` 1 |
| `v1c r3` | 53 | 53 | `T2_TECHNICAL` 18, `SELF_SERVICE_DEFLECT` 10, `T3_ENGINEERING` 9, `ACCOUNT_MANAGER` 7, `SECURITY_INCIDENT` 5, `BILLING_SPECIALIST` 2, `ONCALL_ESCALATION` 1, `T1_GENERAL` 1 |

A refusal taken away can be an error born. Under v1c none of the 126 births
whose round left a rule out was an error of queue.

### The edges refused for closing a cycle

An edge the engine refused for closing a cycle is *right* when its declared
winner is the better rule over the pair's shared region, by
`rung3/edge_direction.py`'s `verdict`. It is read on the whole space and on the
half without the keyword. Beside each right edge are the points of the shared
region on which the final base leaves both rules undefeated, where the edge
would decide now. Of those, the record counts where its winner's queue is the
truth. No refused edge joined two rules of one queue.

| run | edges refused for closing a cycle | space: right / wrong / tie or neither ever right | without the keyword: right / wrong / tie or neither | the right ones' shared points both rules still hold at the end | of them, where the winner's queue is the truth |
|---|---|---|---|---|---|
| v1b, three runs | 128 | 54 / 38 / 36 | 33 / 36 / 59 | 6,340 | 4,900 |
| v1c, three runs | 94 | 59 / 28 / 7 | 58 / 28 / 8 | 460 | 440 |
| `v1c r1` | 58 | 40 / 14 / 4 | 40 / 14 / 4 | 430 | 430 |
| `v1b r1` | 38 | 15 / 14 / 9 | 15 / 12 / 11 | 730 | 730 |
| `v1c r2` | 8 | 2 / 4 / 2 | 2 / 4 / 2 | 0 | 0 |
| `v1b r2` | 30 | 10 / 17 / 3 | 10 / 17 / 3 | 1,320 | 1,320 |
| `v1c r3` | 28 | 17 / 10 / 1 | 16 / 10 / 2 | 30 | 10 |
| `v1b r3` | 60 | 29 / 7 / 24 | 8 / 7 / 45 | 4,290 | 2,850 |
| `PLAN_CHANNEL.md`'s `c r1` | 5 | 1 / 1 / 3 | 1 / 1 / 3 | 840 | 420 |
| `PLAN_CHANNEL.md`'s `c r2` | 84 | 44 / 35 / 5 | 43 / 35 / 6 | 2,000 | 2,000 |
| `PLAN_CHANNEL.md`'s `c r3` | 26 | 14 / 2 / 10 | 11 / 2 / 13 | 420 | 420 |

- **v1c's runs had fewer refused edges, and its right ones leave far fewer points
  open.** v1b's 54 right edges leave 6,340 points to both rules at the end, 4,900
  of them where the winner's queue is the truth. v1c's 59 leave 460, 440 of them
  so.
- **v1b r3 carries most of v1b's**: 4,290 points.
- **`PLAN_CHANNEL.md`'s channel runs** are read the same way, and give back that
  record's 5, 84 and 26 refused edges.
- **What it does not separate.** v1c's list changes which edges enter the graph,
  and so which edges close a cycle. No row separates the exclusions' effect on the
  graph from their effect on the asks (§6.11, §13).

### The channel's reports

| run | impasses | conflicts | errors escalated | wrong decisions | reported | not reported | decisions that stood | wrong among them |
|---|---|---|---|---|---|---|---|---|
| `v1c r1` | 37 | 18 | 43 | 83 | 43 | 40 | 1902 | 40 |
| `v1b r1` | 21 | 12 | 50 | 92 | 50 | 42 | 1917 | 42 |
| `v1c r2` | 32 | 3 | 33 | 66 | 33 | 33 | 1932 | 33 |
| `v1b r2` | 26 | 12 | 48 | 103 | 48 | 55 | 1914 | 55 |
| `v1c r3` | 28 | 6 | 53 | 95 | 53 | 42 | 1913 | 42 |
| `v1b r3` | 29 | 10 | 39 | 73 | 39 | 34 | 1922 | 34 |

- **Every reported wrong decision escalated**, in every run, as `PLAN_CHANNEL.md`
  §2.2 sets.
- **The channel reported 129 of v1c's 244 wrong decisions and 137 of v1b's 268.**
  The ones it did not report stood.
- **v1c r1 met 18 conflicts**, more than any other run, and 37 impasses. Its rules
  never covered the space.

Reported and escalated, of the base's wrong decisions, for the rules that
govern the rarest tickets:

| governing rule | `v1c r1` | `v1b r1` | `v1c r2` | `v1b r2` | `v1c r3` | `v1b r3` |
|---|---|---|---|---|---|---|
| `H04` | 2 of 4 | 1 of 3 | 2 of 4 | 2 of 4 | 2 of 4 | 2 of 4 |
| `H05` | 1 of 1 | 1 of 1 | 0 of 3 | 0 of 3 | 1 of 3 | 1 of 3 |
| `H01` | 1 of 1 | 2 of 2 | 2 of 2 | 1 of 1 | 3 of 5 | 3 of 6 |
| `H02` | 3 of 6 | 5 of 9 | 4 of 5 | 1 of 2 | 4 of 4 | 2 of 2 |
| `H06` | 2 of 4 | 3 of 4 | 1 of 1 | 1 of 1 | 2 of 3 | 2 of 6 |

`H04` governs 4 of the corpus's tickets, `H05` 3, `H01` 9, `H02` 11 and `H06` 8.
Under run 2's draws no `H05` ticket is reportable, and none escalated in either
arm.

### The rare queues

| queue | run | escalations | drafted right | tickets decided by rules | decided right |
|---|---|---|---|---|---|
| `ONCALL_ESCALATION` | `v1c r1` | 3 | 3 | 4 | 2 |
| `ONCALL_ESCALATION` | `v1b r1` | 2 | 2 | 5 | 3 |
| `ONCALL_ESCALATION` | `v1c r2` | 2 | 2 | 5 | 0 |
| `ONCALL_ESCALATION` | `v1b r2` | 2 | 2 | 5 | 0 |
| `ONCALL_ESCALATION` | `v1c r3` | 3 | 3 | 4 | 0 |
| `ONCALL_ESCALATION` | `v1b r3` | 3 | 3 | 4 | 0 |
| `SECURITY_INCIDENT` | `v1c r1` | 5 | 4 | 15 | 12 |
| `SECURITY_INCIDENT` | `v1b r1` | 8 | 8 | 12 | 8 |
| `SECURITY_INCIDENT` | `v1c r2` | 6 | 6 | 14 | 13 |
| `SECURITY_INCIDENT` | `v1b r2` | 3 | 3 | 17 | 16 |
| `SECURITY_INCIDENT` | `v1c r3` | 8 | 8 | 12 | 10 |
| `SECURITY_INCIDENT` | `v1b r3` | 7 | 7 | 13 | 10 |
| `T3_ENGINEERING` | `v1c r1` | 11 | 11 | 106 | 99 |
| `T3_ENGINEERING` | `v1b r1` | 16 | 15 | 101 | 90 |
| `T3_ENGINEERING` | `v1c r2` | 5 | 4 | 112 | 111 |
| `T3_ENGINEERING` | `v1b r2` | 8 | 8 | 109 | 100 |
| `T3_ENGINEERING` | `v1c r3` | 10 | 10 | 107 | 101 |
| `T3_ENGINEERING` | `v1b r3` | 6 | 5 | 111 | 107 |
| `ACCOUNT_MANAGER` | `v1c r1` | 8 | 8 | 101 | 97 |
| `ACCOUNT_MANAGER` | `v1b r1` | 9 | 9 | 100 | 92 |
| `ACCOUNT_MANAGER` | `v1c r2` | 6 | 6 | 103 | 97 |
| `ACCOUNT_MANAGER` | `v1b r2` | 13 | 13 | 96 | 91 |
| `ACCOUNT_MANAGER` | `v1c r3` | 10 | 10 | 99 | 90 |
| `ACCOUNT_MANAGER` | `v1b r3` | 9 | 8 | 100 | 93 |

- **The proposer drafted the right queue at every escalation of
  `ONCALL_ESCALATION`**, in every run: 15 of 15.
- **The rules then decided the queue's other tickets wrongly.** In four runs of
  six they decided none of them right: both runs under run 2's draws and both
  under run 3's.
- **`SECURITY_INCIDENT`.** In every run but one the proposer drafted the queue at
  every escalation of it. v1b r1 escalated on 8 of its tickets and its rules
  decided 8 of the 12 others right.

### Each run beside the transcriber, and beside `PLAN_CHANNEL.md`'s runs

Under its own draws and protocol:

| run | escalations, the run / the transcriber | calls | `space` | `ONCALL_ESCALATION` recall |
|---|---|---|---|---|
| `v1c r1` | 98 / 23 | 186 / 42 | 0.9674 / 0.9999 | 8/15 / 1 |
| `v1b r1` | 83 / 23 | 158 / 45 | 0.8778 / 0.9999 | 218/315 / 1 |
| `v1c r2` | 68 / 22 | 126 / 40 | 0.9683 / 0.9842 | 128/315 / 2/3 |
| `v1b r2` | 86 / 22 | 165 / 43 | 0.9601 / 0.9842 | 34/63 / 2/3 |
| `v1c r3` | 87 / 23 | 167 / 42 | 0.9510 / 0.9999 | 1/15 / 1 |
| `v1b r3` | 78 / 23 | 148 / 45 | 0.8968 / 0.9999 | 0 / 1 |

- **The loop asked three to four times as often as the transcriber**, and v1c r1
  more than four times.
- **Under run 3's draws the transcriber recalls the whole of
  `ONCALL_ESCALATION`.** v1c r3 recalls 1/15 of it and v1b r3 none.

Under the same draws, `PLAN_CHANNEL.md`'s channel run on Baidu, then this plan's
v1b and v1c runs on DeepInfra:

| draws | `space`: `c` / v1b / v1c | `ONCALL_ESCALATION` recall | `refused(r)` | calls |
|---|---|---|---|---|
| run 1 | 0.7201 / 0.8778 / 0.9674 | 2/3 / 218/315 / 8/15 | 16/79 / 25/83 / 5/49 | 147 / 158 / 186 |
| run 2 | 0.9499 / 0.9601 / 0.9683 | 128/315 / 34/63 / 128/315 | 34/131 / 21/86 / 1/17 | 250 / 165 / 126 |
| run 3 | 0.9872 / 0.8968 / 0.9510 | 14/15 / 0 / 1/15 | 9/62 / 1/6 / 8/87 | 117 / 148 / 167 |

- **Under run 1's draws**, c r1 decided 0.7201 of the space; v1b r1 decides
  0.8778 and v1c r1 0.9674.
- **Under run 2's**, the three are within 0.0184 of each other.
- **Under run 3's**, c r3 decided 0.9872, more than either arm here.
- **This is reported, never adjudicated.** It crosses dates and providers, and
  the bridge reads first calls only (§0).

### The direction

`RL-e`'s statistic on this plan's runs, by arm: the share of strict pairs whose
placed edge points at the better rule, by older rule, beyond the keyword. Beside
it is the Stage C ranking's reading on the same pairs and units.

| arm | units | declared: strict pairs right | declared, by older rule | ranking: strict pairs right | ranking, by older rule | difference |
|---|---|---|---|---|---|---|
| v1b | 121 | 436 of 580 | 0.7622 | 551 of 580 | 0.9384 | −0.1762 |
| v1c | 142 | 537 of 661 | 0.8130 | 622 of 661 | 0.9501 | −0.1371 |

- **In both arms the declared edges point at the better rule less often than a
  fixed ranking of the queues does**, as in `PLAN_REASONED_LOOP.md` (`RL-e` and
  `RL-f` refuted) and `PLAN_CHANNEL.md`.
- **The gap is wider here**: −0.1762 and −0.1371, against −0.0232 and −0.0345 in
  `PLAN_CHANNEL.md`'s arms.
- Reported, and it adjudicates nothing.

### The online figures

| run | rules | escalations | coverage | reuse | end to end | silent errors | `prop` | rejected | dead |
|---|---|---|---|---|---|---|---|---|---|
| `v1c r1` | 80 | 98 | 0.9725 | 0.7375 | 0.9500 | 0.0231 | 0.8980 | 18 | 21 |
| `v1b r1` | 56 | 83 | 0.9835 | 0.8750 | 0.9620 | 0.0219 | 0.9398 | 27 | 7 |
| `v1c r2` | 58 | 68 | 0.9825 | 0.8966 | 0.9640 | 0.0188 | 0.9118 | 10 | 6 |
| `v1b r2` | 62 | 86 | 0.9810 | 0.8065 | 0.9515 | 0.0301 | 0.9419 | 24 | 12 |
| `v1c r3` | 75 | 87 | 0.9830 | 0.8267 | 0.9605 | 0.0229 | 0.9540 | 12 | 13 |
| `v1b r3` | 60 | 78 | 0.9805 | 0.8833 | 0.9610 | 0.0199 | 0.9103 | 18 | 7 |

These are rung 2's online metrics over the arrivals, as each record keeps them.
`silent errors` is its `silent_error_rate`: of the cases the engine decided with
a queue, the share whose record is wrong. `rejected` counts the escalations
whose rule was not born, unplaced or refused.

### What the verdicts say

- **The refusals were mostly the protocol's, and a round that lists only what the
  engine can still order takes them away** (`PL-a` holds).
  - The median run's share of escalations ending unplaced fell from 21/86 to
    8/87.
  - **What remains is crossing rules left out.** v1c lists them as v1b does, and
    its unplaced answers left out nothing else. Of v1b's, 28 of 59 left out only
    nested rules.
  - **So the proposer's omissions follow the texts**, the first of §0's two
    hypotheses: it leaves out what the system prompt says needs no side.
  - **Part of the hold is mechanical**, as §0 said. An answer cannot leave out a
    rule it is not shown. The rows that read the truth are `PL-b` to `PL-f`.
- **With those refusals gone, the loop compiles the policy in every run**
  (`PL-b` holds, and `PL-c` holds, thin).
  - v1c's three bases decide 0.9510 to 0.9683 of the space.
  - Each decides the keyword half whole or nearly, and none loses
    `SECURITY_INCIDENT`.
  - In §0's reading, the defect `PLAN_CHANNEL.md` kept on purpose is then why its
    c r1 lost the policy.
- **The new round costs nothing against v1b within one period** (`PL-d` holds).
  Its median base decides 0.0706 more of the space than v1b's.
- **v1b did not compile the policy again on the new period and provider**
  (`PL-e` refuted, thin).
  - Two of its three bases decide less than 0.90 of the space, and both lose part
    of `SECURITY_INCIDENT` and of `T3_ENGINEERING`.
  - In §0's reading, `PL-d` then reads against a weaker comparator than
    `PLAN_CHANNEL.md`'s channel arm.
  - Whether v1b lost the keyword half the way c r1 did is not read here.
- **Neither round compiles the rarest queue** (`PL-f` refuted).
  - §0 read this outcome, with `PL-b` holding, as the third item of `STATUS.md`'s
    *What is open* staying at the supply of rare tickets.
  - **The runs say more than supply.** Run 3's draws let the transcriber compile
    the whole queue. Under them, at every escalation of the queue, the proposer
    drafted the right queue, and the bases recall 1/15 of it under v1c and none
    under v1b.
  - So where the channel supplied the tickets, the loop still lost the queue,
    under both rounds.

### What Stage C does not settle

1. **Why v1b r1 and v1b r3 lost part of `SECURITY_INCIDENT`.** Whether the
   keyword's default came before the queue's broad drafts, and v1b's round
   refused them as it did in c r1, would take `channel/lost.py`'s reading of
   these runs.
2. **Why the runs under run 3's draws lost `ONCALL_ESCALATION`**, in both arms,
   with the queue drafted right at every escalation of it. Which rules decide its
   points, and when they came, would take a reading of those bases.
   **[NOTE 2026-11-08] Read POST-RUN**, in *Why the runs under run 3's draws lost
   `ONCALL_ESCALATION`*, below. No draft was its part whole. Each first call cut
   the governing rule's region by a lower listed rule the ticket matches, or by
   several products. Under v1b none of the cuts was born, and under v1c one was.
3. **Which exclusion does what** (§13, item 1). The rounds are classed by what
   each exclusion left out. What each does to the graph, and so to the edges
   refused for a cycle, is not separated.
4. **Why v1c's runs asked more often** under two draws of three, where §1
   expected fewer calls.
5. **Whether the provider or the period moved v1b.** The bridge reads first
   calls only, and they agree on the queue at every ticket.
6. **The error arm and the impasse arm under v1c, a crossing rule left out, a
   right edge refused for a cycle, a nested pair level 1 orders wrongly, and the
   manual's identifiers** (§13).
7. **One model, one provider, one manual, one arrival order, one coverage, and
   three runs an arm.**

---

## Why the runs under run 3's draws lost `ONCALL_ESCALATION` — POST-RUN

> **POST-RUN.** Asked for by Sergi on 2026-11-08, after Stage C, and run the same
> day. Zero API calls. `placement/oncall.py` calls `channel/oncall.py`'s reading
> for this queue in every run of this plan, and does not copy it. That reading
> splits each way a point was lost by the listed region that holds the point:
> **`H04`'s part**, 4,200 points, and **`H05`'s part**, 2,100. Under run 3's
> draws the channel reached both. In each arm it reported two of `H04`'s four
> tickets and one of `H05`'s three.
>
> - **The expectation was committed before any figure of the reading
>   existed.** It is six clauses in the module's docstring, committed as
>   `7796708`, which is `cd4a60c` on `main`. The drafter had read this record
>   whole. It had seen no rule, edge, escalation or draft of this queue in any of
>   this plan's runs, nor `bridge.json`'s answers at its tickets, nor
>   `results_channel/oncall.json`.
> - **Seven gates stood before any write.**
>   - Gates 1 to 5 are `channel/oncall.py`'s.
>   - Gate 6: every escalation on a ticket of the queue is governed by `H04` or
>     `H05`.
>   - Gate 7, added after the first run: each such ticket lies first in its
>     governing rule's region.
> - **One part was added after the first run**, in `2dc1325`, which is
>   `8a8c67d` on `main`. It reads what each draft cut its part by, and each
>   call's note. Its flag was changed once, in `9cb6dd0`, which is `e798813` on
>   `main`, after a run of it and before any of its figures was cited. It first
>   read the very next rule the ticket matches, which for most tickets was `H06`
>   or `H08`. Those regions contain the governing rule's, so a cut by them
>   changes nothing. The part carries no expectation and moves no clause.
> - **The six clauses came back the same from each of the three commits the
>   reading ran from**, `cd4a60c`, `8a8c67d` and `e798813` on `main`.
>
> Not a signed row; no verdict moves.
> - **The record** is [`oncall.json`](oncall.json), committed in `afbab53` on
>   `main`. It reached `main` in pull request #211.
> - **Its `_env`** names the branch commit it was written from, `9cb6dd0`, the
>   flag's change. It carries `git_dirty` and `code_dirty` false.
> - **The branch commit is `main`'s.** `9cb6dd0` and `e798813` have the same
>   subject, the same tree and the same `git patch-id --stable`, and the GitHub
>   API names #211 behind the `main` commit.
> - **Its code digest**, `74dd22f0826b3731`, is the one `main` computes at
>   `e798813`.

### 1. What the two runs lost, by part

| run | part | the queue's points | decided right | lost | unwritten | conflict or outranked |
|---|---|---|---|---|---|---|
| `v1c r3` | `H04`'s | 4,200 | 0 | 4,200 | 4,200 | 0 |
| `v1c r3` | `H05`'s | 2,100 | 420 | 1,680 | 1,680 | 0 |
| `v1b r3` | `H04`'s | 4,200 | 0 | 4,200 | 4,200 | 0 |
| `v1b r3` | `H05`'s | 2,100 | 0 | 2,100 | 2,100 | 0 |

- **Every point either run lost is unwritten.** Another queue decides it, and
  no rule of the queue matches it. Neither run has an impasse, a conflict or an
  outranked point on the queue.
- **To whom.**
  - In v1c r3, 3,360 points go to `T2_TECHNICAL` and 2,520 to
    `T3_ENGINEERING`.
  - In v1b r3, 4,140 go to `T2_TECHNICAL`, 1,260 to `T3_ENGINEERING`, 640 to
    `ACCOUNT_MANAGER` and 260 to `BILLING_SPECIALIST`.
- **Through which rules.** The record lists every rule of another queue that is
  undefeated on the lost points.
  - In v1c r3 they are ten rules of `T2_TECHNICAL` and `T3_ENGINEERING`, seven of
    them of the form *severity 1 and one product*.
  - In v1b r3, `R0053`, *severity 1* to `T2_TECHNICAL`, born at case 851,
    contains the whole queue and is undefeated on 2,520 of its points.
  - In v1c r3 the rule that contains the whole queue is `R0029`, *severity 1 or
    more* to `T1_GENERAL`, born at case 116. It is undefeated on none of the
    lost points.

### 2. The queue's drafts, and what became of them

The same three tickets escalated in both runs. The draft is the first call's
rule, and its points are those of the ticket's part.

| case | governing rule | the draft | its points of the part | under v1c r3 | under v1b r3 |
|---|---|---|---|---|---|
| 710 | `H05` | `H05`'s region cut by `H17`, product integrations | 420 of 2,100 | born, as `R0058` | unplaced: its answer left out `R0028`, a rule of `T3_ENGINEERING` containing the draft |
| 1432 | `H04` | `H04`'s region cut by `H07`, product api | 840 of 4,200 | refused: the placement answer named no action | unplaced: it left out 4 rules containing the draft and 6 crossing it |
| 1951 | `H04` | v1c r3: `H04`'s region with four products of five. v1b r3: cut by `H17`, product integrations | 3,360 and 840 of 4,200 | unplaced: its answer gave no side to any of the 29 crossing rules listed | unplaced: it left out 2 containing rules and 7 crossing |

- **No draft held its part whole.** At cases 710 and 1432 both runs drew the
  same extension. At case 1951 they drew different ones.
- **The first call cut the governing rule's region, and its note says why.**
  Five of the six drafts are that region cut by exactly the first listed rule
  below it that the ticket matches and that a cut changes: `H07` or `H17`. Each
  first call's note names that rule. In translation from the record's Spanish,
  at case 1432 under v1c:

  > This rule combines the conditions of H04 (severity=1, enterprise) and H07
  > (severity=1, product=api) to resolve the conflict, being a more specific
  > case of both. Automatic containment prioritises it over H04 and H07, without
  > any need to declare priority.

  - **Three of the five notes say the cut wins by containment**, with no side
    declared.
  - **The other two declare a side against `H17`.** That is the manual's
    identifier, which names no rule of a base and is dropped.
- **v1b refused every cut**, as it refused c r1's drafts of `SECURITY_INCIDENT`.
  - At case 710 the only rule the answer left out contains the draft. The
    answer says why, in translation: *R0028 (integrations + severity<=2 -> T3)
    is contained automatically, so it is not declared.*
  - At cases 1432 and 1951 the answers also left out rules that cross the draft.
- **v1c bore one of its three** (`P4` fails).
  - At case 1432 the placement round's answer named no action, and the
    validator refused it.
  - At case 1951 the draft covers four products. Its answer gave no side to any
    of the 29 rules listed, all crossing it. Its note said the draft is a
    particular case of `H04` and of the product rules, and so wins by automatic
    containment. A rule with four products lies inside no rule with one, and the
    round left it unplaced.
- **The curve.** v1c r3 decided 420 of the queue's points after case 710, when
  `R0058` was born, and never more. v1b r3 never decided any.

### 3. Beside the other four runs, and beside `PLAN_CHANNEL.md`'s

| run | `H04`'s part right | `H05`'s part right | the queue's drafts: case, part, points of it, verdict |
|---|---|---|---|
| `v1c r1` | 1,680 | 1,680 | 257: `H05`, whole, born · 1432: `H04`, 840, born · 1951: `H04`, 840, born |
| `v1b r1` | 2,520 | 1,840 | 257: `H05`, whole, born · 1432: `H04`, 2,520, born |
| `v1c r2` | 2,560 | 0 | 954: `H04`, 3,200, born · 1951: `H04`, 840, unplaced |
| `v1b r2` | 3,400 | 0 | 954: `H04`, 3,200, born · 1951: `H04`, 840, born |
| `v1c r3` | 0 | 420 | 710: `H05`, 420, born · 1432: `H04`, 840, refused · 1951: `H04`, 3,360, unplaced |
| `v1b r3` | 0 | 0 | 710: `H05`, 420, unplaced · 1432: `H04`, 840, unplaced · 1951: `H04`, 840, unplaced |

- **No draft at a ticket of `H04` was `H04`'s region whole, in eleven.** Of the
  queue's 15 drafts in the six runs, 11 are their governing rule's region cut by
  exactly the first lower listed rule the ticket matches that a cut changes:
  `H07`, `H13` or `H17`.
  - Two are `H05`'s region whole, both at case 257, under run 1's draws.
  - Two cut `H04`'s region by several products at once: v1b r1's at case 1432
    and v1c r3's at case 1951.
- **What a run recalls of `H04`'s part is what its born cuts hold**, less 640
  points v1c r2 lost to an edge. v1c r1 and v1b r2 bore two cuts each, and v1b
  r1 one wider cut.
- **On Baidu the queue's tickets drew the region whole more often.**
  `results_channel/oncall.json` gives each escalation's governing rule and its
  draft's points of the queue, the points `FINDINGS_CHANNEL.md` tables in *Why
  c r2 recalled less `ONCALL_ESCALATION` than its draws allow*. In
  `PLAN_CHANNEL.md`'s six runs, 7 of the 13 drafts at tickets of `H04` held
  4,200 of the queue's points, the part's size. Under run 3's draws c r3 drew
  `H05`'s region whole at case 710 and `H04`'s at case 1951, and recalled 14/15
  of the queue.

### The expectation

| clause | what it says | reading | verdict |
|---|---|---|---|
| P1 | in both runs no draft at an escalation of the queue holds its ticket's part whole | none of 3, in each | holds |
| P2 | in both runs no rule of the queue holds `H04`'s part whole, and none holds `H05`'s | none does | holds |
| P3 | in both runs at least half of the lost points are unwritten | 5,880 of 5,880, and 6,300 of 6,300 | holds |
| P4 | in v1c r3 every escalation of the queue ended with its rule born | 1 of 3 | **fails** |
| P5 | in v1b r3 no escalation of the queue ended with its rule born | 0 of 3 | holds |
| P6 | in both runs after no birth did the base decide half of the queue's points right or more | 420 and 0, of 6,300 | holds |

**The drafter expected all six to hold, bet on P1, trusted P6 most and P5
least.** Five held, and P4 failed.
- **What the account got right.** The drafts were narrower than their parts, and
  what they did not reach stayed with the rules that had decided it before any
  draft. v1b refused all three, and at case 710 for the reason the account gave:
  the one rule left out contains the draft.
- **What it got wrong.** v1c did not bear its drafts. Of three it bore one,
  refused one whose placement answer named no action, and left one unplaced
  whose answer claimed containment over crossing rules. Under v1b two of the
  three refusals also left out crossing rules, which the account did not name.

### What it says

- **What lost the queue under run 3's draws is the first call's cut.** It was
  not the supply, and not the round alone.
  - The channel reported three of the queue's seven tickets in each run, and at
    each the proposer drafted the right queue.
  - In this plan's six runs it drafted `H04`'s region whole at none of eleven
    escalations. It drafted `H05`'s whole only at case 257, which run 3's draws
    do not report.
  - Born, the cuts of either run would still have left part of each part
    unwritten, since none holds a part whole (P1). The rounds' refusals took
    the rest.
  - The transcriber writes the governing rule's region whole and places it by
    the list's order. That is why it compiles the queue under the same draws.
- **The cut is how the proposer ordered its rule without declaring a side.**
  - The ticket matches its governing rule and lower listed rules.
  - At 11 of the queue's 15 escalations in the six runs, the proposer wrote the
    governing rule's region cut by the first of those a cut changes.
  - Under run 3's draws, three of the five cuts carry a note saying the cut beats
    both rules by containment, with no side declared.
  - Born, a cut decides only its own points. The rest of the part stays with the
    rules that decided it before any draft.
- **What it leaves.**
  - **Provider or period.** No draft at a ticket of `H04` was its region whole
    on DeepInfra, against seven of thirteen on Baidu in the other plan's
    period. The bridge asked the first calls at the queue's seven tickets of
    both providers on one day. Whether DeepInfra cut them there too is free on
    `bridge.json`.
    **[NOTE 2026-11-08] Read POST-RUN**, in *Whether the cut is the provider's*,
    below. At the two tickets that compiled the queue for c r3, DeepInfra cut
    the part at every ask, the bridge's included. At two others both providers
    cut it the same way.
  - **Whether the cut is why the loop writes narrow rules.** `PL-g` counts 70 of
    v1c's 213 births and 68 of v1b's 178 as their governing rule's region.
    Whether the others are cuts by a lower listed rule the ticket matches is free
    on the records.
  - **The two refusals v1c keeps, seen here.** One placement answer named no
    action. Another claimed containment over rules that cross its draft.

---

## Whether the cut is the provider's — POST-RUN

> **POST-RUN.** Asked for by Sergi on 2026-11-08, after the reading above, and
> run the same day. Zero API calls. `placement/provider.py` reads the bridge at
> the queue's seven tickets.
> - **What the bridge asked.** On 2026-11-07, before the first run, it asked
>   the first call both arms send, level 3's system prompt and the ticket under
>   v2b's blind base, once of Baidu and once of DeepInfra.
> - **How it is read.** Each answer is read as `placement/oncall.py` reads a
>   run's draft.
> - **What it is set beside.** The runs' first-call drafts at the same tickets:
>   this plan's six on DeepInfra, from `oncall.json`, and `PLAN_CHANNEL.md`'s six
>   on Baidu, read from their records the same way.
>
> - **The expectation was committed before any figure of the reading
>   existed.** It is four clauses in the module's docstring, in the commit that
>   added the module. The drafter had seen no answer of either provider in
>   `bridge.json`.
> - **Three gates stood before any write.**
>   - Each ticket was asked once of each provider, in its first call.
>   - Each is governed by `H04` or `H05`, and lies first in its region.
>   - `PLAN_CHANNEL.md`'s drafts, read here, give back
>     `results_channel/oncall.json`'s points.
>
> Not a signed row; no verdict moves.
> - **The record** is [`provider.json`](provider.json). Its `_env` names the
>   commit that added the module, with `git_dirty` and `code_dirty` false. Its
>   code digest is `a515c2a31d3ccfbe`.

### 1. The bridge's answers at the queue's tickets

| ticket | governing rule | Baidu | DeepInfra |
|---|---|---|---|
| 257 | `H05` | whole | whole |
| 710 | `H05` | whole | cut by four products, 1,680 of 2,100 |
| 954 | `H04` | whole | whole |
| 982 | `H04` | cut by `H09`, product billing, 840 of 4,200 | the same |
| 1432 | `H04` | cut by `H07`, product api, 840 of 4,200 | the same |
| 1783 | `H05` | whole | whole |
| 1951 | `H04` | whole | cut by `H17`, product integrations, 840 of 4,200 |

*Whole* is a draft that holds its ticket's part whole.

- **Both providers named `ONCALL_ESCALATION` at every ticket.** Every answer
  ended `stop`, served by its pinned provider.
- **At five tickets the two answers name the same conditions.** At three of
  them both hold the part whole, and at two both make the same cut.
- **Where they differ, Baidu holds the part and DeepInfra cuts it**, at 710 and
  1951. The reverse never happened.
- **Both providers cut at 982 and 1432**, each time by the first lower listed
  rule the ticket matches that a cut changes, as the runs' drafts did.

### 2. Beside the runs

| ticket | governing rule | DeepInfra, run drafts holding the part | DeepInfra, the bridge | Baidu, run drafts holding the part | Baidu, the bridge |
|---|---|---|---|---|---|
| 257 | `H05` | 2 of 2 | whole | 2 of 4 | whole |
| 710 | `H05` | 0 of 2 | cut | 2 of 2 | whole |
| 954 | `H04` | 0 of 2 | whole | 2 of 5 | whole |
| 982 | `H04` | no draft | cut | 0 of 1 | cut |
| 1432 | `H04` | 0 of 4 | cut | 2 of 3 | cut |
| 1783 | `H05` | no draft | whole | no draft | whole |
| 1951 | `H04` | 0 of 5 | cut | 3 of 4 | whole |

- **At the tickets of `H04`, DeepInfra held the part at none of its eleven run
  drafts and at one of its four bridge answers.** Baidu held it at seven of
  thirteen and at two of four.
- **At 710 and 1951 the difference holds at every ask recorded.** DeepInfra
  cut the part at all nine: three at 710 and six at 1951. Baidu held it at
  seven of eight, and its one cut was e r2's at 1951.
- **Elsewhere one ask a ticket reads a provider loosely.** At 954 DeepInfra held
  `H04`'s part on the bridge, where both of its runs that escalated there cut it
  by `H13`. At 1432 Baidu cut it on the bridge, where two of its three run
  drafts held it.

### The expectation

| clause | what it says | reading | verdict |
|---|---|---|---|
| Q1 | none of DeepInfra's four answers at tickets of `H04` holds `H04`'s part whole | 1 of 4, at 954 | **fails** |
| Q2 | at least two of Baidu's four answers at tickets of `H04` hold `H04`'s part whole | 2 of 4, at 954 and 1951 | holds |
| Q3 | at more tickets Baidu's answer holds its part whole and DeepInfra's does not than the reverse | 2, at 710 and 1951, against none | holds |
| Q4 | every DeepInfra answer that one listed rule cuts is cut by the first matched rule a cut changes, and there is one | 3 of 3, at 982, 1432 and 1951 | holds |

**The drafter expected all four to hold, bet on Q3, trusted Q1 most and Q2
least.** Three held. Q1, the clause trusted most, failed: DeepInfra held
`H04`'s part once, at 954.

### What it says

- **On one day and one request, DeepInfra cut where Baidu did not, and never
  the reverse.** Of the queue's seven tickets, Baidu's answer held the part at
  five and DeepInfra's at three.
- **The cut is not DeepInfra's alone.** Both providers cut at 982 and 1432, the
  same way. The request makes the cut, and DeepInfra makes it more often.
- **Under run 3's draws the difference fell on the two tickets that mattered.**
  - The queue's escalations there were at 710, 1432 and 1951.
  - At 710 and 1951 DeepInfra cut at every ask, and Baidu wrote the part
    whole at seven asks of eight.
  - c r3, on Baidu, recalled 14/15 of the queue from its drafts at 710 and 1951,
    each holding its part whole.
  - At 1432 both providers cut.
  - So this plan's two runs under those draws lost the queue's region at the
    first call, at the two tickets where Baidu's asks wrote it whole at seven of
    eight.
- **One ask a ticket is a sign, not an effect.** Away from 710 and 1951 each
  provider's answers at a ticket differ from ask to ask. The bridge's two
  tickets of difference are consistent with the runs, and they are two.
- **What it leaves.**
  - **A provider's spread beside the difference.** Each first call asked
    several times of each provider on one day would measure it. Calls.
  - **Why the request cuts.** Both providers cut where the first lower listed
    rule a cut changes adds the ticket's product: api at 1432, by `H07`, and
    billing at 982, by `H09`. A text that asks for the governing rule's region
    whole is another plan. Calls.

---

## Files

```
results_placement/sample.json        Stage A: the checks, the drafting reading, the hidden
                                     policy through v1c's path, the transcriber under every
                                     protocol and draw, the rules left out and why, the
                                     schedule, the bridge's tickets and order, the streams
results_placement/loop_smoke.json    Stage B's smoke run: 30 cases under v1c
results_placement/bridge.json        Stage B's bridge: 40 first calls, each asked of Baidu and
                                     of DeepInfra, every answer whole with its reasoning, its
                                     call_attempts and its hour
results_placement/loop_{v1b,v1c}_r{1,2,3}.json
                                     Stage B's six runs: the header with the protocol, the
                                     pin, the coverage and the draws, every rule in birth
                                     order, the edge log, every case's row with its cause and
                                     its draw, every escalation whole with its list, what v1c
                                     left out and why, its calls, attempts, seconds and
                                     reasoning, and rung 2's metrics
results_placement/score.json         Stage C: the six verdicts with their runs, and PL-g
results_placement/oncall.json        POST-RUN: channel/oncall.py's reading of ONCALL_ESCALATION
                                     in every run, each way split by H04's part and H05's, the
                                     rules holding either part whole, each draft against its
                                     ticket's part, the expectation's six clauses, and the part
                                     added after the first run: what each draft cut its part
                                     by, and each call's note
results_placement/provider.json      POST-RUN: the bridge's two answers at each of the queue's
                                     seven tickets read as drafts, the runs' first-call drafts
                                     at the same tickets on DeepInfra and on Baidu, and the
                                     expectation's four clauses
```

What OpenRouter billed was read by generation id, and is kept outside git.
