# The loop under a channel that hears of half its errors — findings

Record opened on November 7, 2026, under [`PLAN_CHANNEL.md`](../PLAN_CHANNEL.md).
The plan and its package reached `main` in pull request #196, merged on
2026-11-05. Sergi signed §0 on 2026-11-05, before any figure below existed, in a
commit of its own: `4aa0b8f` on `main`.
- **The signature and Stage A** reached `main` in #197.
- **The smoke run** reached it in #198.
- **The six runs** reached it in #199, merged on 2026-11-06.
- **Stage C, this record, the banner that closes the plan and the indexes**
  reached it in #200, merged on 2026-11-07.

Every record names in its `_env` the commit it was written from. Seven were
written on a pull request's branch, and the rebase merge gave each of those
commits a new hash on `main`. Each pair has the same subject, the same tree and
the same `git patch-id --stable`, and the GitHub API names the pull request
behind every `main` commit.

| record | written from | the same commit on `main` | code digest |
|---|---|---|---|
| `sample.json` | `8a4d794`, the signature, on the branch of #197 | `4aa0b8f` | `a9a819726536a4db` |
| `loop_smoke.json` | `70e759c`, Stage A's commit, on the branch of #197 | `e4685b8` | `a9a819726536a4db` |
| `loop_e_r1.json` | `0e49d17`, the smoke run's commit, on `main` (#198) | itself | `a9a819726536a4db` |
| `loop_c_r1.json` | `1dd4307`, e r1's commit, on the branch of #199 | `5b7019f` | `a9a819726536a4db` |
| `loop_e_r2.json` | `3cbfc4e`, c r1's commit, on the branch of #199 | `bb8b0eb` | `a9a819726536a4db` |
| `loop_c_r2.json` | `4c95a28`, e r2's commit, on the branch of #199 | `038753f` | `a9a819726536a4db` |
| `loop_e_r3.json` | `4097e2d`, c r2's commit, on the branch of #199 | `5dfc2d2` | `a9a819726536a4db` |
| `loop_c_r3.json` | `41f5ba0`, e r3's commit, on the branch of #199 | `aa3cc4b` | `a9a819726536a4db` |
| `score.json` | `913c97f`, c r3's commit, on `main` | itself | `a9a819726536a4db` |

- **`git_dirty` is false in `sample.json` alone.** An untracked `AGENTS.md`,
  not this plan's and never committed, appeared at the repository's root at
  12:45 UTC on 2026-11-05, during the smoke run. Every later record carries
  `git_dirty` true for it.
- **`code_dirty` is false in every record, and every record carries one code
  digest.** `main` computes it at `913c97f`, with
  `harness.provenance.code_digest`. The package's code did not change after the
  signature.

**This record owns every figure in it.**

**All three stages ran between 2026-11-05 and 2026-11-07, and the six rows are
adjudicated. `CH-a`, `CH-b`, `CH-d`, `CH-e` and `CH-f` hold, all but `CH-d`
thinly. `CH-c` is refuted, thinly. `CH-g` is reported.**

- **Half the reports compile the policy in the median run.** The channel arm's
  median base decides 0.9499 of the space right. One run of three, c r1, decides
  0.7201. It sends most of `SECURITY_INCIDENT`'s points, 3/8 of the space, to
  other queues.
- **Within one period, halving the reports costs 1/32 of the space between the
  medians.** The error arm's median base decides 0.9811. With c r1 in the channel
  arm's place, the cost would be 0.2610.
- **The error arm compiles the policy again on a new period, and not thinly.**
  Its three bases decide 0.9798, 0.9811 and 0.9868 of the space. Each is above
  every error run of `PLAN_REASONED_LOOP.md`, which decided 0.8898 to 0.9635. It
  recalls all of `ONCALL_ESCALATION` in two runs, and 53/63 of it in the third.
- **Half the reports do not compile the rarest queue.** The channel arm's
  median recall of `ONCALL_ESCALATION` over the space is 2/3. Only c r3 reaches
  the line, at 14/15. c r2's draws make no `H05` ticket reportable, and its base
  recalls 128/315 of the queue, less than the transcriber's 2/3 under the same
  draws.
- **Hearing of half the errors cuts the calls by about a fifth, at the
  medians.** The channel arm's median run made 147 calls and the error arm's
  182: 21/26, 0.8077. c r2 made 250, more than any error run.
- **The drafter expected five rows to hold and `CH-c` to be refuted, and that
  is how they came out.**

**[NOTE 2026-11-07] Read POST-RUN, c r1 lost `SECURITY_INCIDENT` because its
broad drafts were refused.**
- **What it never wrote.** No rule of the queue reaches 0.9014 of the points c
  r1 lost. The keyword's default, a rule of `T2_TECHNICAL`, decides most of
  them.
- **Why it never wrote them.** Its proposer drafted the queue's broad regions,
  and v1b's placement round refused each answer. The answer left out the
  default, which contains every draft of the queue, and level 3's system
  prompt says such a rule needs no declaration.
- **Why c r1 and not the others.** In c r1 the default was born before any
  broad rule of the queue, and every broad draft after it was refused. Of the
  two other runs with a default, c r3 had written `H01`'s region before it, and
  e r1's answers placed it twice in three tries.

See *Why c r1 lost `SECURITY_INCIDENT`*, below.

**[NOTE 2026-11-07, later] Read POST-RUN, c r2 lost 1,640 of the 4,200 points of
`ONCALL_ESCALATION` its draws let it reach.**
- **1,000 were never written.** Its one rule of the queue carries a condition
  `H04` does not have. Its draft of `H04`'s region whole was refused by the
  placement round.
- **640 are contested.** Two later rules of other queues each declared
  themselves below that rule. The engine refused both edges for closing a
  cycle.

See *Why c r2 recalled less `ONCALL_ESCALATION` than its draws allow*, below.

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Its references were
> computed after the signature. Zero API calls.
>
> **PROVENANCE, STAGES B AND C: PRE-REGISTERED.** `CH-a` to `CH-f` were signed
> before any of their figures existed, and none of their bands was set on a
> development set. **`CH-d` and `CH-e` are replications.** Their bands were
> drafted after `PLAN_REASONED_LOOP.md`'s figures had been seen, as §0 says, and
> the scoreboard should read them as replications.
>
> **WHAT WAS SEEN BEFORE STAGE C.** The agent that launched the runs saw, before
> the scorer ran:
> - **Each run's commit message**, which its supervisor wrote from the record.
>   It gives what the run printed, its calls, attempts, refusals and retries,
>   its launches, its `_env` and its pace by round.
> - **Those `calls` are `calls(r)`, the counts `CH-f` reads**, as the scorer's
>   `calls_as_recorded` confirms: 171, 147, 182, 250, 208 and 117. They were
>   pushed to #199 and given to Sergi before Stage C. Their ratio was not
>   computed.
> - **The runs' progress lines**, every 25 cases: rules, escalations and calls
>   asked.
> - **c r2's calls**: their seconds and refused attempts, by hour, to place when
>   Baidu began refusing. Also the texts in its header.
> - **e r3's partial file during the run**: each call's case, round, seconds,
>   attempts and refusals.
> - **One call's row, printed whole**: e r3's first draft, with its
>   declarations and its note. That draft is one of the 563 the record counts.
> - **What OpenRouter billed** for every attempt, read by generation id.
>
> No base, no `space`, no recall and no row was read before Stage C.

**Each figure names its surface.**
- **`CH-a`, `CH-b` and `CH-d`** read the exhaustive space of 134,400 points.
- **`CH-c` and `CH-e`** read its 6,300 points whose true queue is
  `ONCALL_ESCALATION`.
- **`CH-f`** reads the runs' calls.
- **`CH-g`** reads both surfaces and says which.

The corpus is `generate_corpus(2000, seed=17)` in every run. **The arms** are:
- **the channel arm, `c`.** It escalates an IMPASSE or a CONFLICT, and a case
  the engine decides with a queue other than its label, when that case's draw
  falls below 1/2;
- **the error arm, `e`.** It escalates every such case (§0).

---

## Stage A — the checks and the references

**What was run.** `python3 -m channel.sample`, on 2026-11-05, with
`PYTHONHASHSEED=0`, from the signing commit on a clean tree. The record is
[`sample.json`](sample.json).

**The blocking checks passed before anything was written.**
- **`CH-g1`.** `PLAN_REASONED_LOOP.md`'s verdicts came back from its runs.
  - This plan's loop at coverage 1 is that plan's error arm, with the
    transcriber and with run e r1's answers replayed. Replayed, it gives back
    e r1's rules and causes case for case.
  - At coverage 0 the loop is that plan's impasse arm.
  - A run's rebuild is its engine, and the labels agree with the truth.
  - The suite was green.
- **`CH-g2`.** Every text is `PLAN_REASONED_LOOP.md`'s.
  - Every run's draws are rebuilt from their seed strings, and they are §0's.
  - The transcriber gives back §0's figures.
  - The hidden policy goes through v1b's path whole: 29 rules and 253
    declarations, which install rung 2's 199 edges. It decides both surfaces
    right.
- **`CH-g3`.** `ORDER_SEED` drew the error arm first, so the schedule is e r1,
  c r1, e r2, c r2, e r3, c r3. The smoke run is 30 cases under the channel arm,
  with its own draws, and the cap is 400 escalations.
- **`CH-g4`.** One signature line, signed.

**Every figure §0 lists as computed while drafting came back**, items 1 to 6
and 8, so §0 needs no erratum.

**The draws.** One stream of 2,000 floats per channel run, and one for the smoke
run, each from a string seed through SHA-512.

| stream | seed string | digest |
|---|---|---|
| c r1 | `PLAN_CHANNEL/channel/97/r1` | `1347b9525a1e06a3` |
| c r2 | `PLAN_CHANNEL/channel/97/r2` | `e81548d721b99577` |
| c r3 | `PLAN_CHANNEL/channel/97/r3` | `1f60e3d5e68553d4` |
| the smoke run | `PLAN_CHANNEL/channel/97/smoke` | `029047351ae2d471` |

**The transcriber**, under each channel run's draws and under the error trigger.
It is a double that writes, at every escalation, the rule of level 3's text that
governs the ticket, and places it by the text's order.

| under | escalations | calls | wrong decisions reported / not | `space` | `corpus` | `ONCALL_ESCALATION` recall |
|---|---|---|---|---|---|---|
| c r1's draws | 23: 2 impasses and 21 errors | 45 | 21 / 22 | 134,380 of 134,400 | 1,999 of 2,000 | 1 |
| c r2's draws | 22: 2 impasses and 20 errors | 43 | 20 / 12 | 132,280 | 1,996 | 2/3 |
| c r3's draws | 23: 2 impasses and 21 errors | 45 | 21 / 18 | 134,380 | 1,999 | 1 |
| the error trigger | 23: 2 impasses and 21 errors | 45 | 21 / 0 | 134,380 | 1,999 | 1 |
| the smoke run's draws, 30 cases | 9: 2 impasses and 7 errors | 17 | 7 / 13 | 49,420 | 1,107 | 0 |

The last row is the only one §0 does not declare.

---

## Stage B — the runs

**Every call ran at `deepseek/deepseek-v4-flash`, at temperature 0, with
reasoning `{"effort": "high"}` and 16,000 tokens, pinned to Baidu with
fallbacks off.**
- **The path.** Every call went through `PLAN_FIRST_MATCH.md`'s asker with
  `PLAN_REASONED_LOOP.md`'s request, under v1b: level 3's system prompt, a blind
  first call, and v2b's placement round.
- **The checks.** Every launch checked the signature, the key, `CH-g1` to
  `CH-g3` and the records before it, before any call.

**How the runs were launched.** Under §2.5 Sergi chose that the agent launch
them, detached from its harness.
- **The supervisor** ran them one at a time, in §2.3's order.
  - It resumed a run that an outage had stopped, about once an hour from its
    launch.
  - It committed each record alone, through the pre-commit hook, before the
    next run started.
  - It never passed the overwrite flag and never skipped the hook.
- **The pull request.** The supervisor pushed each record to #199. Once both
  `ci-complete` runs on its last head were green, it merged #199 by rebase,
  matching that head.

### The smoke run

[`loop_smoke.json`](loop_smoke.json) ran 30 cases under the channel arm, with
its own draws, on 2026-11-05 from 12:11 to 12:58 UTC.
- **What it did.**
  - It met 13 escalations: 9 impasses and 4 reported errors.
  - It made 21 calls: 13 first calls and 8 placement rounds.
  - 11 rules were born and 2 were refused. No proposal failed.
- **The trigger's record.** Of 10 wrong decisions, the channel reported 4, and
  each escalated. 6 stood.
- **The provider.** Baidu served every attempt that reached the model, and every
  one reasoned and ended `stop`. 36 attempts, across 6 calls, were refused for
  the rate. Each was waited out under `PLAN_REASONED_LOOP.md` §5.5's amendment,
  and none stopped the run.
- **The pace.** Without the calls that met a refusal, the first calls took a
  median of 44.6 seconds and the placement rounds 11.2.
- **The check passed**, so the runs could start. No row reads its answers.
- **A first launch refused before any call.** It started at 11:47 UTC and
  refused at 11:52, because one test of the suite inside `CH-g1` failed.
  - Nothing was spent, and no record was written.
  - Three later runs of the suite passed, one under that launch's own
    environment, and so did the gate of the launch recorded here.
  - The failure was not reproduced.

### The six runs

| run | from its first launch to its record, UTC | launches | escalations | calls | attempts | refused for the rate | billed |
|---|---|---|---|---|---|---|---|
| `e r1` | 11-05 14:36–16:25 | 1 | 90 | 171 | 174 | 1 | $0.081 |
| `c r1` | 11-05 16:28–18:01 | 1 | 79 | 147 | 154 | 5 | $0.067 |
| `e r2` | 11-05 18:04–20:13 | 1 | 95 | 182 | 184 | 0 | $0.095 |
| `c r2` | 11-05 21:04 – 11-06 05:48 | 4 | 131 | 250 | 459 | 204 | $0.170 |
| `e r3` | 11-06 05:51–14:49 | 3 | 106 | 208 | 574 | 366 | $0.276 |
| `c r3` | 11-06 14:53–16:13 | 1 | 62 | 117 | 117 | 0 | $0.104 |

- **Every run reached case 2,000.** None stopped at the cap, and none recorded a
  failed proposal.
- **What was billed** was read from OpenRouter on 2026-11-07, by the generation
  id that each attempt's `call_attempts` keeps. It is not a record of this
  repository.
  - Every attempt that reached the model was found.
  - The six runs came to $0.79, and the smoke run to $0.027.

**Baidu refused for the rate through most of a day.**
- **On 2026-11-05, from 14:36 UTC, it barely refused.** e r1, c r1 and e r2
  met 1, 5 and 0 refusals.
- **From about midnight UTC it refused most attempts.**
  - c r2 met its first refusal at case 1,665.
  - Three outages stopped c r2, at 01:27, 02:16 and 05:34 UTC on 2026-11-06, and
    two stopped e r3, at 07:56 and 12:40. Each was one call refused on all 18
    of its attempts, through every wait.
  - None of those calls is recorded, and each was asked again on the next
    launch.
- **It had stopped refusing by mid-afternoon, UTC.** c r3, from 14:53 to 16:13,
  met no refusal.
- **The smoke run** met its 36 refusals between 12:11 and 12:58 UTC on
  2026-11-05.

**The price per token followed the refusals.** The bills give each attempt's
cost. In the hours in which Baidu refused, an attempt was billed about three
times as much per token as on the afternoon of 2026-11-05.

The price per million prompt tokens was, by hour:
- at most $0.047 in every hour of 2026-11-05 from 14:00 UTC;
- up to $0.14 from 00:00 to 13:00 UTC on 2026-11-06;
- at most $0.086 from 15:00 UTC on 2026-11-06.

Two notes on that reading:
- **It assumes completion tokens at twice the prompt price**, as every listing
  of the model gives them.
- **$0.14 is Baidu's listing** as read at about 11:00 UTC on 2026-11-06: $0.14
  for prompt and $0.28 for completion tokens.

**The supervisor stood still for 47 minutes on 2026-11-05.**
- **What stopped it.** At 20:17 UTC the push of e r2's record met a timeout of
  the Windows credential helper, called through WSL. The supervisor was written
  to stop on a failed push. No run was under way, and no call was spent.
- **How it resumed.** The push went through by hand at 21:03 UTC. c r2 was
  launched at 21:04 from the commit it would have started from, `4c95a28`.
- **What changed.** From then on the supervisor retried a failed push and went
  on.

**[ERRATUM 2026-11-06] c r2's commit message gives the span of its last launch
only**, 05:37 to 05:48 UTC.
- **The run's real span.** It was first launched at 21:04 UTC on 2026-11-05, and
  went through four launches, as the table above gives.
- **Why the commit stands.** It is not amended, because e r3's `_env` names it.
- **What changed.** From e r3 on, the messages give the whole span.

#199's description carries the same erratum.

**The pin held.** Every attempt that reached the model, 1,086 in the six runs,
was served by Baidu and ended `stop`. The 576 refused for the rate carry no
provider.

**The retries.**
- **For the rate**: 1 in e r1, 5 in c r1, 204 in c r2 and 366 in e r3. Each was
  asked again with the same messages after a wait.
- **After a failed parse**: 2 answers each in e r1, c r1 and e r2, and 5 in
  c r2. Each was asked again with v1's retry message.
- **No answer reached the budget.** The longest completion took 14,752 of the
  16,000 tokens, in c r2.

**Every attempt that reached the model reasoned.**
- **The medians.** By run, over those attempts, the median reasoning ran from
  3,520 to 4,168 tokens, and the most was 14,382.
- **The refused attempts are left out of the medians.** The scorer reads e r3's
  at 3,821.5, though 366 of its 574 attempts were refused.
- **The records keep the reasoning whole**, and no stage codes it.

| run | calls | attempts | reached Baidu | refused for the rate | asked again after a failed parse | prompt tokens | completion tokens | reasoning tokens, median | max |
|---|---|---|---|---|---|---|---|---|---|
| `e r1` | 171 | 174 | 173 | 1 | 2 | 380,055 | 731,176 | 3741 | 13,287 |
| `c r1` | 147 | 154 | 149 | 5 | 2 | 317,907 | 594,623 | 3520 | 12,289 |
| `e r2` | 182 | 184 | 184 | 0 | 2 | 416,321 | 833,100 | 4168 | 9,773 |
| `c r2` | 250 | 459 | 255 | 204 | 5 | 578,399 | 1,173,850 | 4036 | 14,382 |
| `e r3` | 208 | 574 | 208 | 366 | 0 | 462,801 | 911,230 | 3821.5 | 11,263 |
| `c r3` | 117 | 117 | 117 | 0 | 0 | 253,961 | 499,120 | 3814 | 9,562 |

**The pace, by run and by round**, in seconds, from `score.json`.
- **Every call counts.** Each call served from a partial file kept its own
  seconds, under `PLAN_REASONED_LOOP.md` §5.5's second amendment, so the rows
  read every call.
- **The calls that met no refusal** are counted beside the rest.

| run | round | calls | median, s | minutes in all | calls that met no refusal | their median, s |
|---|---|---|---|---|---|---|
| `e r1` | first call | 90 | 42.3 | 71.2 | 89 | 41.8 |
| `e r1` | placement | 81 | 19.6 | 34.8 | 81 | 19.6 |
| `c r1` | first call | 79 | 43.0 | 62.2 | 76 | 41.9 |
| `c r1` | placement | 68 | 22.5 | 27.3 | 66 | 21.8 |
| `e r2` | first call | 95 | 49.1 | 79.5 | 95 | 49.1 |
| `e r2` | placement | 87 | 29.2 | 47.2 | 87 | 29.2 |
| `c r2` | first call | 131 | 44.2 | 212.6 | 116 | 42.7 |
| `c r2` | placement | 119 | 29.8 | 180.6 | 103 | 26.5 |
| `e r3` | first call | 106 | 68.0 | 258.7 | 69 | 54.0 |
| `e r3` | placement | 102 | 40.5 | 190.1 | 70 | 33.9 |
| `c r3` | first call | 62 | 44.9 | 48.9 | 62 | 44.9 |
| `c r3` | placement | 55 | 24.7 | 28.3 | 55 | 24.7 |

**How far §1 was.**
- **The calls.** §1 put a channel run between an error run and an impasse run.
  The channel runs made 117, 147 and 250 calls, and the error runs 171, 182 and
  208. c r2 made more than any error run.
- **The money.** §1 expected the six runs to cost under half a dollar, at
  Baidu's listing of 2026-10-25.
  - At that listing their tokens would have cost $0.27.
  - They were billed $0.79, because the price per token was not that listing's
    (above).
- **The time.** §1 expected six to eight hours for the error runs and three to
  six for the channel's, if no provider refused for a day.
  - A run that met no outage took from 1 hour 21 minutes to 2 hours 10 minutes,
    from launch to record.
  - c r2 and e r3, through their outages, took 8 hours 44 minutes and 8 hours
    58 minutes.
- **The smoke run's pace.** It measured the first calls at a median of 44.6
  seconds without refusals, on 8 calls. The runs' first calls that met no
  refusal took medians of 41.8 to 54.0 seconds, by run.

---

## Stage C — the six adjudications

**What was run.** `python3 -m channel.score --dry-run`, then
`PYTHONHASHSEED=0 python3 -m channel.score`, on 2026-11-07, from `913c97f` on
`main`. The tree was clean but for the untracked `AGENTS.md`, so the record's
`_env` carries `git_dirty` true and `code_dirty` false.
- **The checks.** `CH-g1` to `CH-g4` passed in both commands, with the suite
  green.
- **The runs.** All six were read, and none is missing. Every run's rebuilt base
  is the base its record says it ended with, and every run's calls are the calls
  its record counts.
- **The record** is [`score.json`](score.json). Zero API calls.

**Every statistic is a fraction of counts, compared with its line exactly.**
The record keeps each as a fraction beside its float.

| row | statistic | line | reading | read | verdict |
|---|---|---|---|---|---|
| CH-a | the channel arm's median `space(B)` | ≥ 0.90 | **0.9499**, 6383/6720 | 3 runs | **holds, thin** |
| CH-b | the error arm's median `space(B)`, less the channel arm's | ≤ 0.05 | **0.0312**, 1/32, from 0.9811 and 0.9499 | 3 runs an arm | **holds, thin** |
| CH-c | the channel arm's median `recall_ONCALL_ESCALATION(B)` over the space | ≥ 0.90 | **0.6667**, 2/3 | 3 runs | **refuted, thin** |
| CH-d | the error arm's median `space(B)` | ≥ 0.90 | **0.9811**, 6593/6720 | 3 runs | **holds** |
| CH-e | the error arm's median `recall_ONCALL_ESCALATION(B)` over the space | ≥ 0.90 | **1.0000**, 1 | 3 runs | **holds, thin** |
| CH-f | the channel arm's median `calls(r)`, over the error arm's | ≥ 3/4 | **0.8077**, 21/26, from 147 and 182 | 3 runs an arm | **holds, thin** |

`CH-g` is reported, and everything below that is not in the table is its.

**Five verdicts are thin, and each turns on one run or two.**
- **`CH-a`.** c r1's 0.7201, put in place of the median, falls under the line.
- **`CH-b`.** So does c r1, put in place of the channel arm's median: 0.9811 less
  0.7201 is 0.2610. No error run moves it across in place of the error arm's
  median: they leave 0.0299 and 0.0369.
- **`CH-c`.** c r3's 14/15, 0.9333, put in place of the median, would hold it.
- **`CH-e`.** e r2's 53/63, 0.8413, falls under the line.
- **`CH-f`.** Two runs each move it across:
  - c r3's 117 calls, in place of the channel arm's median, read 0.6429;
  - e r3's 208, in place of the error arm's, read 0.7067.

  Both fall under 3/4.

**`CH-d` is not thin.** Its lowest run, e r1, decides 0.9798 of the space.

**Every row had a value.** Each arm has three complete runs.

**Each row's runs:**

| run | `space(B)` | `ONCALL_ESCALATION` recall, space | `calls(r)` |
|---|---|---|---|
| `e r1` | 823/840, 0.9798 | 6,300 of 6,300, 1 | 171 |
| `c r1` | 1613/2240, 0.7201 | 4,200 of 6,300, 2/3 | 147 |
| `e r2` | 6593/6720, 0.9811 | 5,300 of 6,300, 53/63 | 182 |
| `c r2` | 6383/6720, 0.9499 | 2,560 of 6,300, 128/315 | 250 |
| `e r3` | 6631/6720, 0.9868 | 6,300 of 6,300, 1 | 208 |
| `c r3` | 3317/3360, 0.9872 | 5,880 of 6,300, 14/15 | 117 |

**The drafter expected five rows to hold and `CH-c` to be refuted, and that is
how they came out.**
- **The order of trust.** It trusted `CH-f` most, then `CH-d`, `CH-e`, `CH-a`
  and `CH-b`.
- **Where the thin labels departed.** It expected `CH-d`, `CH-e`, `CH-a` and
  `CH-b` to hold thinly. `CH-d` held without being thin, and `CH-f`, expected to
  hold, held thinly.

That is a fact about this plan, and the scoreboard counts it.

### The two arms, on both surfaces

| run | `space` | without the keyword | with it | `corpus` | `K-a` | `cover(r)` |
|---|---|---|---|---|---|---|
| `e r1` | 0.9798 | 0.9595 | 1.0000 | 1,986 of 2,000 | 9/59 | case 658 |
| `c r1` | 0.7201 | 0.9473 | 0.4929 | 1,975 of 2,000 | 11/57 | never |
| `e r2` | 0.9811 | 0.9622 | 1.0000 | 1,962 of 2,000 | 8/71 | case 725 |
| `c r2` | 0.9499 | 0.8997 | 1.0000 | 1,922 of 2,000 | 5/43 | case 658 |
| `e r3` | 0.9868 | 0.9735 | 1.0000 | 1,996 of 2,000 | 5/79 | case 456 |
| `c r3` | 0.9872 | 0.9935 | 0.9810 | 1,999 of 2,000 | 7/47 | case 228 |

- **c r1 loses the keyword half.** It decides 0.9473 of the half without the
  keyword, and 0.4929 of the half with it. Every other run decides the keyword
  half at 0.98 or more.
- **c r2 is the weakest run without the keyword**, at 0.8997.
- **c r3 decides more of the space than any run of either arm**, 0.9872, from
  the fewest calls, 117.
- **On the arrivals the arms barely part.** Every base decides 1,922 to 1,999 of
  the 2,000 cases right.

### The recall of the eight queues

Over the space:

| run | `T1_GENERAL` | `T2_TECHNICAL` | `T3_ENGINEERING` | `BILLING_SPECIALIST` | `SECURITY_INCIDENT` | `ACCOUNT_MANAGER` | `ONCALL_ESCALATION` | `SELF_SERVICE_DEFLECT` |
|---|---|---|---|---|---|---|---|---|
| `e r1` | 0.9655 | 0.9608 | 0.8655 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| `c r1` | 0.9808 | 1.0000 | 0.9487 | 1.0000 | 0.3238 | 0.9440 | 0.6667 | 1.0000 |
| `e r2` | 0.9962 | 0.9749 | 0.9267 | 1.0000 | 1.0000 | 1.0000 | 0.8413 | 1.0000 |
| `c r2` | 0.9598 | 0.9918 | 0.7824 | 1.0000 | 1.0000 | 0.9635 | 0.4063 | 0.9744 |
| `e r3` | 0.9962 | 0.9760 | 0.8924 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| `c r3` | 0.9962 | 1.0000 | 1.0000 | 1.0000 | 0.9746 | 1.0000 | 0.9333 | 1.0000 |

Over the corpus, for the four rarest queues:

| run | `ONCALL_ESCALATION` | `SECURITY_INCIDENT` | `T3_ENGINEERING` | `ACCOUNT_MANAGER` |
|---|---|---|---|---|
| `e r1` | 7 of 7 | 20 of 20 | 117 of 117 | 109 of 109 |
| `c r1` | 4 of 7 | 4 of 20 | 117 of 117 | 104 of 109 |
| `e r2` | 4 of 7 | 20 of 20 | 89 of 117 | 109 of 109 |
| `c r2` | 1 of 7 | 20 of 20 | 111 of 117 | 105 of 109 |
| `e r3` | 7 of 7 | 20 of 20 | 117 of 117 | 109 of 109 |
| `c r3` | 7 of 7 | 20 of 20 | 117 of 117 | 109 of 109 |

- **Every error run recalls `SECURITY_INCIDENT` whole**, on both surfaces. Of
  the channel runs, c r2 does, c r3 recalls 0.9746 of its points, and c r1
  0.3238.
- **`ONCALL_ESCALATION`.** Each error run recalls 1, 53/63 or 1 of its points.
  The channel runs recall 2/3, 128/315 and 14/15.
- **`T3_ENGINEERING`.** No run recalls it whole but c r3. c r2 is lowest, at
  0.7824.

### The channel's reports

| run | coverage | impasses | conflicts | errors escalated | wrong decisions | reported | not reported | decisions that stood | wrong among them |
|---|---|---|---|---|---|---|---|---|---|
| `e r1` | 1 | 29 | 2 | 59 | 59 | 59 | 0 | 1910 | 0 |
| `c r1` | 1/2 | 29 | 1 | 49 | 97 | 49 | 48 | 1921 | 48 |
| `e r2` | 1 | 26 | 1 | 68 | 68 | 68 | 0 | 1905 | 0 |
| `c r2` | 1/2 | 35 | 33 | 63 | 126 | 63 | 63 | 1869 | 63 |
| `e r3` | 1 | 16 | 20 | 70 | 70 | 70 | 0 | 1894 | 0 |
| `c r3` | 1/2 | 22 | 10 | 30 | 53 | 30 | 23 | 1938 | 23 |

- **Every reported wrong decision escalated**, in every run, as §2.2 sets.
- **The channel reported 49 of 97, 63 of 126 and 30 of 53 wrong decisions**:
  0.5052, 0.5000 and 0.5660. The ones it did not report stood: 48, 63 and 23 of
  them.
- **The channel arm's bases erred more often than the error arm's in two runs
  of three.** c r1 and c r2 decided 97 and 126 cases wrongly, where the error
  runs decided 59 to 70. So half of their wrong decisions still came to 49 and
  63 reports.
- **c r2 met 33 conflicts**, where the other runs met 1 to 20.

By true queue, reported of wrong. Every reported one escalated, and no channel
run decided a `T1_GENERAL` ticket wrongly during the run:

| run | `T2_TECHNICAL` | `T3_ENGINEERING` | `ACCOUNT_MANAGER` | `ONCALL_ESCALATION` | `SECURITY_INCIDENT` | `BILLING_SPECIALIST` | `SELF_SERVICE_DEFLECT` |
|---|---|---|---|---|---|---|---|
| `c r1` | 14 of 27 | 7 of 13 | 8 of 26 | 2 of 6 | 11 of 17 | 5 of 6 | 2 of 2 |
| `c r2` | 18 of 36 | 8 of 13 | 3 of 8 | 2 of 7 | 5 of 6 | 10 of 18 | 17 of 38 |
| `c r3` | 4 of 6 | 1 of 3 | 7 of 10 | 3 of 5 | 4 of 4 | 4 of 9 | 7 of 16 |

Over time, reported of wrong, by block of 200 cases:

| run | 0–199 | 200–399 | 400–599 | 600–799 | 800–999 | 1000–1199 | 1200–1399 | 1400–1599 | 1600–1799 | 1800–1999 |
|---|---|---|---|---|---|---|---|---|---|---|
| `c r1` | 14 of 32 | 8 of 19 | 7 of 10 | 5 of 9 | 2 of 7 | 2 of 2 | 6 of 6 | 1 of 2 | 1 of 4 | 3 of 6 |
| `c r2` | 22 of 41 | 9 of 19 | 8 of 18 | 6 of 13 | 5 of 12 | 5 of 9 | 3 of 4 | 0 of 1 | 0 of 3 | 5 of 6 |
| `c r3` | 12 of 24 | 4 of 10 | 5 of 8 | 3 of 4 | 2 of 3 | 0 of 0 | 1 of 1 | 2 of 2 | 0 of 0 | 1 of 1 |

**c r1's `SECURITY_INCIDENT`.** What c r1 lost there was lost after the reports
had come and the drafts had been right.
- **The reports came.** The channel reported 11 of c r1's 17 wrong decisions on
  the queue's tickets, and each escalated.
- **The drafts were right.** The proposer drafted the queue at 12 of the 13
  escalations whose ticket was the queue's.
- **The base still sent most of the queue elsewhere.** Of the 7 security
  tickets c r1's rules decided rather than escalate, they decided 1 right, and
  its final base recalls 0.3238 of the queue's points.
- **A proposer that never errs would have lost nothing.** Under c r1's draws
  the transcriber compiles the whole queue.

So what c r1 lost is the loop's and not the channel's, which is what §0 chose
coverage 1/2 to make it.

### The error escalations by governing rule, beside the supply

Escalated of reportable, for the rules that govern the rarest tickets:

| governing rule | `e r1` | `c r1` | `e r2` | `c r2` | `e r3` | `c r3` |
|---|---|---|---|---|---|---|
| `H04` | 1 of 4 | 1 of 2 | 4 of 4 | 2 of 2 | 2 of 4 | 2 of 2 |
| `H05` | 2 of 3 | 1 of 1 | 1 of 3 | 0 of 0 | 1 of 3 | 1 of 1 |
| `H01` | 4 of 9 | 5 of 5 | 3 of 9 | 3 of 6 | 1 of 9 | 1 of 5 |
| `H02` | 2 of 11 | 6 of 6 | 2 of 11 | 2 of 6 | 5 of 11 | 3 of 7 |
| `H06` | 3 of 8 | 1 of 5 | 2 of 8 | 3 of 6 | 3 of 8 | 1 of 3 |

`H04` governs 4 of the corpus's tickets, `H05` 3, `H01` 9, `H02` 11 and `H06` 8.
In the error arm every one of them is reportable. c r1 escalated on every
reportable `H01` and `H02` ticket, and it is the run that lost the queue they
govern.

### Each run beside the transcriber

| run | escalations, the run / the transcriber | calls | `space` | `ONCALL_ESCALATION` recall |
|---|---|---|---|---|
| `e r1` | 90 / 23 | 171 / 45 | 0.9798 / 0.9999 | 1 / 1 |
| `c r1` | 79 / 23 | 147 / 45 | 0.7201 / 0.9999 | 2/3 / 1 |
| `e r2` | 95 / 23 | 182 / 45 | 0.9811 / 0.9999 | 53/63 / 1 |
| `c r2` | 131 / 22 | 250 / 43 | 0.9499 / 0.9842 | 128/315 / 2/3 |
| `e r3` | 106 / 23 | 208 / 45 | 0.9868 / 0.9999 | 1 / 1 |
| `c r3` | 62 / 23 | 117 / 45 | 0.9872 / 0.9999 | 14/15 / 1 |

- **The loop asked about three to six times as often as the transcriber**, under
  the same draws or trigger.
- **Each run, by how far its base comes from the transcriber's:**
  - c r3 comes within 0.0126 of it, and the error runs within 0.0201;
  - c r2 comes within 0.0344;
  - c r1 comes 0.2798 short.

### The drafts, the verdicts and the placement rounds

| run | drafts right | born | unplaced | refused | changed | placement rounds | rules listed, median [range] |
|---|---|---|---|---|---|---|---|
| `e r1` | 88 of 90, 0.9778 | 68 | 22 | 0 | 0 | 81 | 5 [1–43] |
| `c r1` | 73 of 79, 0.9241 | 62 | 16 | 1 | 0 | 68 | 5 [1–38] |
| `e r2` | 88 of 95, 0.9263 | 79 | 14 | 1 | 1 | 87 | 7 [1–42] |
| `c r2` | 115 of 131, 0.8779 | 94 | 34 | 3 | 0 | 119 | 9 [1–40] |
| `e r3` | 93 of 106, 0.8774 | 88 | 18 | 0 | 0 | 102 | 7 [1–40] |
| `c r3` | 61 of 62, 0.9839 | 52 | 9 | 1 | 0 | 55 | 8 [1–25] |

| run | citations of `H01` to `H29` | other citations | edges by the engine's verdict | copies born | births that are their governing rule's region |
|---|---|---|---|---|---|
| `e r1` | 104 | 664 | 498 ok, 15 closing a cycle, 13 outside the neighbourhood | 1 | 18 of 68 |
| `c r1` | 117 | 471 | 304 ok, 5 closing a cycle, 17 outside the neighbourhood, 1 against containment | 4 | 14 of 62 |
| `e r2` | 91 | 728 | 601 ok, 21 closing a cycle, 10 outside the neighbourhood | 18 | 26 of 79 |
| `c r2` | 169 | 1,170 | 739 ok, 84 closing a cycle, 12 outside the neighbourhood, 5 against containment | 28 | 20 of 94 |
| `e r3` | 210 | 873 | 718 ok, 36 closing a cycle, 3 outside the neighbourhood | 24 | 23 of 88 |
| `c r3` | 69 | 427 | 359 ok, 26 closing a cycle, 9 outside the neighbourhood, 1 against containment | 6 | 23 of 52 |

- **A draft is the first call's queue.** The proposer drafted the right queue at
  518 of the 563 escalations, 0.9201.
- **What ended unplaced.** 113 escalations ended unplaced: a listed rule was left
  out of the second answer. 6 rules were refused and 1 placement changed its
  draft's rule. None of these is born.
- **The citations** count every identifier in `beats` and `loses_to`, over both
  calls of every escalation.
  - The manual's identifiers took the place of the base's in about one citation
    in seven: 760 of 5,093.
  - None of them names a rule of a base, and each is dropped and recorded.
- **c r2's lists ran longest**, a median of 9 rules. The engine refused 84 of
  its edges for closing a cycle.

### The rare queues

| queue | run | escalations | drafted right | tickets decided by rules | decided right |
|---|---|---|---|---|---|
| `ONCALL_ESCALATION` | `e r1` | 3 | 3 | 4 | 4 |
| `ONCALL_ESCALATION` | `c r1` | 2 | 2 | 5 | 1 |
| `ONCALL_ESCALATION` | `e r2` | 5 | 5 | 2 | 2 |
| `ONCALL_ESCALATION` | `c r2` | 2 | 2 | 5 | 0 |
| `ONCALL_ESCALATION` | `e r3` | 3 | 3 | 4 | 4 |
| `ONCALL_ESCALATION` | `c r3` | 4 | 4 | 3 | 1 |
| `SECURITY_INCIDENT` | `e r1` | 7 | 7 | 13 | 13 |
| `SECURITY_INCIDENT` | `c r1` | 13 | 12 | 7 | 1 |
| `SECURITY_INCIDENT` | `e r2` | 6 | 6 | 14 | 14 |
| `SECURITY_INCIDENT` | `c r2` | 6 | 6 | 14 | 13 |
| `SECURITY_INCIDENT` | `e r3` | 6 | 6 | 14 | 14 |
| `SECURITY_INCIDENT` | `c r3` | 4 | 4 | 16 | 16 |
| `T3_ENGINEERING` | `e r1` | 9 | 9 | 108 | 108 |
| `T3_ENGINEERING` | `c r1` | 7 | 7 | 110 | 104 |
| `T3_ENGINEERING` | `e r2` | 36 | 32 | 81 | 81 |
| `T3_ENGINEERING` | `c r2` | 13 | 13 | 104 | 99 |
| `T3_ENGINEERING` | `e r3` | 12 | 11 | 105 | 105 |
| `T3_ENGINEERING` | `c r3` | 6 | 6 | 111 | 109 |
| `ACCOUNT_MANAGER` | `e r1` | 14 | 14 | 95 | 95 |
| `ACCOUNT_MANAGER` | `c r1` | 10 | 10 | 99 | 81 |
| `ACCOUNT_MANAGER` | `e r2` | 12 | 12 | 97 | 97 |
| `ACCOUNT_MANAGER` | `c r2` | 10 | 10 | 99 | 94 |
| `ACCOUNT_MANAGER` | `e r3` | 7 | 7 | 102 | 102 |
| `ACCOUNT_MANAGER` | `c r3` | 11 | 11 | 98 | 95 |

- **In the error arm a decision stands only where it is right**, by
  construction, so its rules decide right every rare ticket they decide.
- **Every channel run's rules decided some rare tickets wrongly, and the
  channel did not report them, so they stood.** That is where the channel arm's
  unreported wrong decisions fall on the rare queues. In c r1, for instance, 4
  `ONCALL_ESCALATION`, 6 `SECURITY_INCIDENT` and 18 `ACCOUNT_MANAGER` tickets
  stood decided wrongly.
- **The proposer drafted the right queue at every rare escalation but six**:
  one in c r1, four in e r2 and one in e r3.

### The direction

`RL-e`'s statistic on this plan's runs, by arm: the share of strict pairs whose
placed edge points at the better rule, by older rule, beyond the keyword. Beside
it is the Stage C ranking's reading on the same pairs and units.

| arm | units | declared: strict pairs right | declared, by older rule | ranking: strict pairs right | ranking, by older rule | difference |
|---|---|---|---|---|---|---|
| channel | 148 | 622 of 712 | 0.8901 | 664 of 712 | 0.9133 | −0.0232 |
| error | 161 | 696 of 796 | 0.8766 | 709 of 796 | 0.9112 | −0.0345 |

In both arms the declared edges point at the better rule less often than a fixed
ranking of the queues does, as in `PLAN_REASONED_LOOP.md` (`RL-e` and `RL-f`
refuted). Reported, and it adjudicates nothing.

### The error arm, across dates

This plan's error runs beside `PLAN_REASONED_LOOP.md`'s, run by run: this plan's
figure first, that plan's after the slash.

| run | `space` | without the keyword | with it | `ONCALL_ESCALATION` recall | `SECURITY_INCIDENT` recall | escalations | rules | `cover(r)` | date |
|---|---|---|---|---|---|---|---|---|---|
| `e r1` | 0.9798 / 0.9601 | 0.9595 / 0.9702 | 1.0000 / 0.9500 | 1.0000 / 0.9333 | 1.0000 / 0.9333 | 90 / 99 | 68 / 76 | case 658 / case 658 | 2026-11-05 / 2026-11-01 |
| `e r2` | 0.9811 / 0.9635 | 0.9622 / 0.9298 | 1.0000 / 0.9973 | 0.8413 / 1.0000 | 1.0000 / 1.0000 | 95 / 120 | 79 / 90 | case 725 / case 228 | 2026-11-05 / 2026-11-02 |
| `e r3` | 0.9868 / 0.8898 | 0.9735 / 0.9561 | 1.0000 / 0.8235 | 1.0000 / 0.7333 | 1.0000 / 0.7667 | 106 / 102 | 88 / 63 | case 456 / case 1 | 2026-11-06 / 2026-11-02 |

- **Over the space, each new error run decided more than its namesake**: 0.9798,
  0.9811 and 0.9868, against 0.9601, 0.9635 and 0.8898.
- **On the new period every error run decides the keyword half whole.** On the
  first, the error runs decided 0.8235 to 0.9973 of it.
- **`ONCALL_ESCALATION` went the other way once.** e r2 recalled 0.8413 of it,
  against its namesake's 1.
- **This is reported, never adjudicated.** It rests on three runs a period, and
  the periods differ in more than the date (§0).

### The online figures

| run | rules | escalations | coverage | reuse | end to end | silent errors | `prop` | rejected | dead |
|---|---|---|---|---|---|---|---|---|---|
| `e r1` | 68 | 90 | 0.9845 | 0.8824 | 0.9840 | 0.0005 | 0.9778 | 22 | 8 |
| `c r1` | 62 | 79 | 0.9850 | 0.8871 | 0.9580 | 0.0274 | 0.9241 | 17 | 7 |
| `e r2` | 79 | 95 | 0.9865 | 0.6582 | 0.9845 | 0.0020 | 0.9368 | 16 | 27 |
| `c r2` | 94 | 131 | 0.9660 | 0.7234 | 0.9320 | 0.0352 | 0.8779 | 37 | 26 |
| `e r3` | 88 | 106 | 0.9820 | 0.6705 | 0.9765 | 0.0056 | 0.8774 | 18 | 29 |
| `c r3` | 52 | 62 | 0.9840 | 0.8654 | 0.9725 | 0.0117 | 0.9839 | 10 | 7 |

These are rung 2's online metrics over the arrivals, as each record keeps them.
The channel arm's silent errors are its unreported wrong decisions.

### What the verdicts say

- **Half the reports compile the policy in the median run, within one period**
  (`CH-a`, `CH-b` and `CH-d` hold).
  - In §0's words, half the reports compile what all of them compile, and a
    deployment that hears of half its errors is enough for this loop, at the
    cost `CH-f` reads.
  - **But two of the three holds are thin, and they turn on one run.** c r1 lost
    more than a quarter of the space, in the queue that is 3/8 of it. Its
    channel had reported most of that queue's wrong decisions, and its proposer
    had drafted them right.
- **The rarest queue needs more reports than half coverage supplies from seven
  tickets** (`CH-c` refuted, and `CH-e` holds).
  - In §0's reading, `STATUS.md`'s third item narrows from the trigger's design
    to the supply of rare tickets.
  - Only c r3 reached the line, and its draws make three of the seven
    reportable.
  - c r2's draws make no `H05` ticket reportable, and its base recalls less of
    the queue than the transcriber does under the same draws.
- **The calls did not follow the reports one for one** (`CH-f` holds, thin).
  - The channel arm's median run made 21/26 of the error arm's median calls,
    while hearing of half its errors.
  - In two runs of three its bases erred more often, and half of more came to
    nearly as many reports. That is the mechanism §0 gave for a ratio near 1: a
    base that repairs more slowly keeps erring, and so keeps being reported.
  - The third channel run, c r3, compiled quickest and asked least. In the
    median's place it would put the ratio under the line, so the verdict is
    thin.
- **The error arm compiled the policy again on a new period** (`CH-d` holds),
  **and the rarest queue again** (`CH-e` holds, thin). Both replicate
  `PLAN_REASONED_LOOP.md`'s thin holds: `CH-d` without being thin, and `CH-e`
  thinly.

### What Stage C does not settle

1. **Why c r1 did not compile `SECURITY_INCIDENT`.** Its reports came and its
   drafts were right. Which of its rules decide the queue's points, and when
   they came to, would take a reading of its base.
   **[NOTE 2026-11-07] Read POST-RUN**, in *Why c r1 lost
   `SECURITY_INCIDENT`*, below. The queue's broad drafts were refused. Each
   answer left out the keyword's default, which contains them all, and the
   placement round asks for a side against it. The default decides the points
   no rule of the queue reaches.
2. **Why c r2 recalled less of `ONCALL_ESCALATION` than the transcriber under
   its draws**, 128/315 against 2/3.
   **[NOTE 2026-11-07, later] Read POST-RUN**, in *Why c r2 recalled less
   `ONCALL_ESCALATION` than its draws allow*, below.
   - **A narrow rule.** Its one rule of the queue is narrower than `H04`, and
     the placement round refused the draft that would have widened it.
   - **Two refused edges.** Two later rules of other queues cross that rule.
     Each declared the right side, and the engine refused both edges for
     closing a cycle.
3. **Whether a hold of `CH-b` rules out a cost of a twentieth.** As §0 said,
   with three runs an arm and runs as far apart as c r1 and c r3, the
   instrument could not see one.
4. **Whether the new period's error arm is better than the first because of the
   period.** Three runs a period, reported only.
5. **Lower coverage, delay, noise and asymmetry, a trigger that reads no truth,
   and another provider** (§13).
6. **One model, one provider, one manual, one arrival order, three runs an arm.**

---

## Why c r1 lost `SECURITY_INCIDENT` — POST-RUN

> **POST-RUN.** Asked for by Sergi on 2026-11-07, after Stage C, and run the
> same day. Zero API calls. `channel/lost.py` did three things in every run:
> - it classed every point of the queue the final base does not decide right
>   by what lost it;
> - it replayed the base in birth order;
> - it read the queue's escalations by verdict.
>
> - **The expectation was committed before any figure of the reading
>   existed.** It is six clauses in the module's docstring, committed as
>   `6a974c0`, which is `f75398e` on `main`. The drafter had read this record
>   whole and `score.json`'s `CH-g`, and no rule, edge or escalation of any run.
> - **Four gates stood before any write.**
>   - The replay is the base, and the queue's points decided right are Stage
>     C's.
>   - The ways partition the loss.
>   - The curve ends at the base.
>   - The escalations are the record's.
> - **One part was added after the first run**, in `715505c`, which is `3fc5d11`
>   on `main`. It reads what the queue's unplaced answers left out, and the
>   rules of another queue that contain the whole queue. It carries no
>   expectation and moves no clause.
>
> Not a signed row; no verdict moves.
> - **The record** is [`lost.json`](lost.json), committed in `c8e1ca7` on
>   `main`. It reached `main` in pull request #202.
> - **Its `_env`** names the branch commit it was written from, `715505c`. It
>   carries `git_dirty` true for the untracked `AGENTS.md` and `code_dirty`
>   false.
> - **The branch commit is `main`'s.** `715505c` and `3fc5d11` have the same
>   subject, the same tree and the same `git patch-id --stable`, and the GitHub
>   API names #202 behind the `main` commit.
> - **Its code digest**, `fbbf138c1fe5e1cb`, is the one `main` computes at
>   `3fc5d11`.

**How a lost point is classed.** A point of the queue the final base does not
decide right is exactly one of:
- **an impasse**: no rule matches it;
- **a conflict**: undefeated rules of different queues match it. It is
  *contested* when a rule of the queue is among them;
- **unwritten**: one other queue decides it, and no rule of the queue matches
  it;
- **outranked**: one other queue decides it, though a rule of the queue matches
  it. It is outranked by an edge when a rule of another queue beats one of the
  queue's there by a declared edge, and by containment otherwise.

### 1. What c r1 lost, and to what

| the queue's points | decided right | lost | unwritten | conflict | outranked | impasse |
|---|---|---|---|---|---|---|
| 50,400 | 16,320 | 34,080 | 30,720, 0.9014 of the lost | 3,360, 0.0986 | 0 | 0 |

- **No rule of the queue reaches nine tenths of what c r1 lost.**
  - The conflicts are between other queues; none is contested.
  - No point is outranked.
- **The unwritten points go to other queues**: 29,240 to `T2_TECHNICAL`, 840 to
  `ONCALL_ESCALATION` and 640 to `ACCOUNT_MANAGER`.
- **One rule decides most of them.** `R0039`, *has_security_keyword eq True* →
  `T2_TECHNICAL`, decides 23,280.
  - It is the keyword's default, `H03`'s queue.
  - It was born at case 238, at an error escalation on a ticket `H03` governs.
- **Next is `R0057`, with 4,200 points**: *keyword, severity 2, pro* →
  `T2_TECHNICAL`.
  - It was born at case 1235, on a ticket `H02` governs.
  - It is the one draft at the queue's tickets that named another queue.
- **The rest go to rules written at tickets without the keyword**, which do not
  exclude it: mostly of `T2_TECHNICAL`, and one each of `ONCALL_ESCALATION` and
  `ACCOUNT_MANAGER`.

### 2. c r1's rules of the queue, and its curve

| rule | born at | cause | the ticket's rule | its region | the queue's points |
|---|---|---|---|---|---|
| `R0019` | 44 | impasse | `H01` | keyword, severity 1, business | 4,200 |
| `R0032` | 155 | error | `H01` | keyword, business, at least 8 prior tickets | 10,400 |
| `R0049` | 739 | error | `H01` | keyword, business or enterprise, billing | 6,720 |

- **All three are narrow.** The widest covers 10,400 of the queue's points,
  13/63, and none is a listed rule's region.
- **The curve only rose.** The base decided 4,200 of the queue's points right
  after case 44, 12,000 after 155 and 16,320 after 739. No birth lost any.

### 3. The queue's escalations in c r1

| case | cause | the ticket's rule | the draft's queue | the draft's points of the queue | rules listed | verdict | rules the answer left out |
|---|---|---|---|---|---|---|---|
| 44 | impasse | `H01` | `SECURITY_INCIDENT` | 4,200 | 8 | born | |
| 155 | error | `H01` | `SECURITY_INCIDENT` | 10,400 | 15 | born | |
| 448 | error | `H02` | `SECURITY_INCIDENT` | 6,720 | 12 | unplaced | 6: `R0039`, which contains the draft, and 5 crossing it |
| 580 | conflict | `H02` | `SECURITY_INCIDENT` | 6,720 | 11 | unplaced | 3: `R0039` and another containing the draft, and 1 crossing it |
| 599 | error | `H02` | `SECURITY_INCIDENT` | 6,720 | 12 | unplaced | `R0039` alone |
| 739 | error | `H01` | `SECURITY_INCIDENT` | 6,720 | 12 | born | |
| 751 | error | `H02` | `SECURITY_INCIDENT` | 3,360 | 5 | unplaced | 3, each crossing the draft |
| 770 | error | `H02` | `SECURITY_INCIDENT` | 6,720 | 14 | unplaced | 3, each containing the draft: `R0039` and two billing rules |
| 1063 | error | `H01` | `SECURITY_INCIDENT` | 33,600 | 30 | unplaced | `R0039` alone |
| 1235 | error | `H02` | `T2_TECHNICAL` | 4,200 | 6 | born | |
| 1264 | error | `H01` | `SECURITY_INCIDENT` | 16,800 | 23 | unplaced | `R0039` alone |
| 1871 | error | `H01` | `SECURITY_INCIDENT` | 33,600 | 38 | unplaced | `R0039` alone |
| 1961 | error | `H02` | `SECURITY_INCIDENT` | 6,720 | 13 | unplaced | 2, each containing the draft: `R0039` and `R0029` |

- **4 of the 13 ended born**: the three rules above, and `R0057`, drafted as
  `T2_TECHNICAL`. **9 ended unplaced**, and every one of them was answered.
- **8 of the 9 unplaced answers left `R0039` out.**
  - It contains every draft of the queue.
  - Level 3's system prompt says a rule nested in another needs no
    declaration.
  - v1b's placement round lists it all the same, and refuses an answer that
    leaves it without a side.
- **6 of the 9 left out only rules nested with their draft.**
- **The broad drafts were all refused.**
  - c r1's proposer drafted `H01`'s region whole twice, at cases 1063 and 1871,
    and drafted 16,800 points at 1264.
  - Each placement round listed 23 to 38 rules.
  - Each answer gave a side to every listed rule but `R0039`.
- **c r1 never drafted `H02`'s region whole.** Its drafts at `H02`'s tickets
  covered 6,720 points or fewer.

### 4. Beside the other five runs

| run | the queue's rules | `H01`'s region born at | `H02`'s region born at | the queue's escalations born / unplaced | a rule containing the whole queue, born at |
|---|---|---|---|---|---|
| `e r1` | 6 | 1704 | 580 | 6 / 1 | `R0047`, case 394 |
| `c r1` | 3 | never | never | 4 / 9 | `R0039`, case 238 |
| `e r2` | 5 | 1063 | 580 | 5 / 1 | none |
| `c r2` | 4 | 1063 | 599 | 4 / 2 | none |
| `e r3` | 5 | 44 | 751 | 5 / 1 | none |
| `c r3` | 3 | 44 | 580 | 3 / 1 | `R0037`, case 394 |

Each rule containing the whole queue is the keyword's default,
*has_security_keyword eq True* → `T2_TECHNICAL`.

- **Every other run wrote both regions whole**, each at one escalation.
- **In c r1 the default came first.** `R0039` was born at case 238, before any
  broad rule of the queue, and from then on every placement round of the queue
  listed it.
- **The other two defaults came later.**
  - **c r3**'s came at case 394. It had already written `H01`'s region at case
    44.
  - **e r1**'s also came at case 394. Its answers placed the default at case
    580, which bore `H02`'s region, and at 1704, which bore `H01`'s. At 1063 its
    answer left the default out, as c r1's did, and the draft was refused.
  - **e r2, c r2 and e r3** never wrote a default.
- **The same ticket drew different drafts.** The first call is blind to the
  base: it sends the system prompt and the ticket, so a ticket's first call is
  the same request in every run.
  - At case 44, e r3 and c r3 drafted `H01`'s region whole, and c r1 drafted
    4,200 points of it.
  - At case 580, three runs drafted `H02`'s region whole, and c r1 drafted
    6,720 points.
- **c r1 did not ask less.** It escalated on 13 of the queue's tickets, where
  the other runs escalated on 4 to 7. What it asked was refused.

### The expectation

| clause | what it says | reading | verdict |
|---|---|---|---|
| L1 | at least half of the lost points are unwritten | 30,720 of 34,080, 0.9014 | holds |
| L2 | at least half of the lost points go to `T2_TECHNICAL` | 29,240 of 34,080, 0.8580 | holds |
| L3 | no rule of the queue covers half of the queue's points or more | the widest covers 10,400 of 50,400, 0.2063 | holds |
| L4 | at least 10 of the queue's escalations ended with their rule born | 4 of 13 | **fails** |
| L5 | after no birth did the base decide half of the queue's points right | at most 16,320, 0.3238 | holds |
| L6 | in each other run some rule of the queue covers half of the queue's points or more | 33,600 in each, 2/3 | holds |

**The drafter expected all six to hold, bet on L1 and trusted L4 least.** L4
failed, and that is where the account was wrong.
- **What it got right.** The points were unwritten, went to the keyword's
  default, and c r1's rules of the queue were narrow.
- **What it got wrong.** It took the narrowness for the proposer's. The
  proposer did draft the queue's regions broad, and the placement round refused
  every broad draft.

### What it says

- **c r1 lost the queue to the keyword's default, by never writing its broad
  regions.** Nine tenths of what it lost lies outside every rule of the queue,
  and the default decides most of it.
- **The proposer drafted those regions, and v1b refused them.**
  - The placement round lists every rule of another queue that meets the
    draft, nested ones included.
  - The default contains every draft of the queue.
  - The proposer left it out, as the system prompt says, and the round refused
    the answer, so the draft was not born.
  - This is the defect `PLAN_REASONED_LOOP.md`'s POST-RUN reading found
    (*Where the unplaced answers come from*). §0 kept it in both arms on
    purpose.
- **c r1 met it because its default came first.** Three runs never wrote a
  default. c r3 wrote `H01`'s region before its default, and e r1's answers
  placed its default twice in three tries. c r1's default was born at case 238,
  before any broad draft.
- **So what c r1 lost is not the channel's.**
  - It asked about the queue more often than any other run.
  - Under its draws the transcriber, which places by the text's order,
    compiles the whole queue.
  - What it lost is v1b's placement round meeting a default born early. The
    same ticket's draft varies between runs, so which comes first is partly
    the draft's draw.
- **What it leaves.** Each of the three broad answers gave a side to every
  listed rule but the one nested with its draft. A round that did not ask for a
  side against a rule nested with the draft would have taken each of them as
  complete. That is the change *Where the unplaced answers come from* asked
  for, and no plan has run it.

---

## Why c r2 recalled less `ONCALL_ESCALATION` than its draws allow — POST-RUN

> **POST-RUN.** Asked for by Sergi on 2026-11-07, after the reading of c r1, and
> run the same day. Zero API calls. `channel/oncall.py` calls `channel/lost.py`'s
> reading for this queue in every run, and does not copy it. It splits each way
> a point was lost by the listed region that holds the point:
> - **`H04`'s part**, 4,200 points, which c r2's draws let the channel reach;
> - **`H05`'s part**, 2,100 points, which they do not.
>
> - **The expectation was committed before any figure of the reading
>   existed.** It is five clauses in the module's docstring, committed as
>   `b1f9e43`, which is `a4d7a6a` on `main`. The drafter had read this record
>   whole, with `lost.json`, and no rule, edge or escalation of this queue in
>   any run.
> - **Five gates stood before any write**: `channel/lost.py`'s four, and one
>   that the two parts are disjoint and hold the queue.
> - **One part was added after the first run**, in `cac4ee9`, which is
>   `dba4376` on `main`. It reads the contested pairs, and the engine's verdict
>   on every edge between their rules. It carries no expectation and moves no
>   clause.
>
> Not a signed row; no verdict moves.
> - **The record** is [`oncall.json`](oncall.json), committed in `0fce727` on
>   `main`. It reached `main` in pull request #205.
> - **Its `_env`** names the branch commit it was written from, `cac4ee9`. It
>   carries `git_dirty` and `code_dirty` false.
> - **The branch commit is `main`'s.** `cac4ee9` and `dba4376` have the same
>   subject, the same tree and the same `git patch-id --stable`, and the GitHub
>   API names #205 behind the `main` commit.
> - **Its code digest**, `9195d9e6aa2860cb`, is the one `main` computes at
>   `dba4376`.

### 1. What c r2 lost, by part

| | the queue's points | decided right | lost | unwritten | conflict | of it contested | outranked or impasse |
|---|---|---|---|---|---|---|---|
| `H04`'s part | 4,200 | 2,560 | 1,640 | 1,000 | 640 | 640 | 0 |
| `H05`'s part | 2,100 | 0 | 2,100 | 1,840 | 260 | 0 | 0 |
| the queue | 6,300 | 2,560 | 3,740 | 2,840 | 900 | 640 | 0 |

- **Its draws allow `H04`'s part whole.** Under them the transcriber decides
  all 4,200 of its points right and none of `H05`'s. c r2 falls short of that
  by 1,640 points: 1,000 unwritten and 640 contested.
- **`H05`'s part is lost whole**, as the draws would have it. No ticket of
  `H05` escalated in c r2.
- **The unwritten points go to rules of other queues written for severity-1
  tickets**: 1,540 to `T2_TECHNICAL`, 1,040 to `T3_ENGINEERING` and 260 to
  `ACCOUNT_MANAGER`.

### 2. Its one rule of the queue, and the draft that was refused

**c r2's only rule of the queue is `R0075`**, born at case 954, on an error at a
ticket `H04` governs.
- **Its region** is *severity 1, enterprise, at least 5 prior tickets*. That is
  `H04`'s region with a condition `H04` does not have: the prior tickets are
  `H13`'s, the rule that sends enterprise tickets with 5 or more prior tickets
  to `ACCOUNT_MANAGER`.
- **What the condition costs.** It holds 3,200 of `H04`'s 4,200 points. The
  1,000 with fewer than 5 prior tickets are the unwritten points of `H04`'s
  part.

| case | cause | the draft's points of the queue | rules listed | verdict |
|---|---|---|---|---|
| 954 | error | 3,200 | 18 | born, as `R0075` |
| 1951 | error | 4,200, `H04`'s region whole | 24 | unplaced |

- **The draft that would have widened it was refused.** At case 1951 the
  proposer drafted `H04`'s region whole. Its answer gave a side to 23 of the 24
  listed rules, and left out `R0022`, a rule of `SECURITY_INCIDENT` that
  crosses the draft. The round refused it, so the draft was not born.
  - The rule left out was not nested with the draft.
  - So this refusal is not the defect of c r1's: the proposer left out a rule
    the round had every reason to list.

### 3. The contested points, and the edges the engine refused

| case | rule born | its queue | its region | its answer | the engine |
|---|---|---|---|---|---|
| 1309 | `R0082` | `T2_TECHNICAL` | integrations, business or enterprise | below `R0075` | refused, closing a cycle |
| 1402 | `R0085` | `ACCOUNT_MANAGER` | integrations, enterprise, at least 5 prior tickets | below `R0075` | refused, closing a cycle |

- **The curve rose once and fell once.** It reached 3,200 after case 954 and
  fell to 2,560 after case 1309, when `R0082` was born.
- **Both rules declared the right side, and both edges were refused.** The run's
  `edge_log` holds each edge, `R0075` over the new rule, with the verdict
  *closing a cycle*.
- **What a refused edge leaves.**
  - The engine refuses an edge when the base already reaches the other way,
    following every edge and every containment through other rules.
  - It decides a point by the direct relations among the rules that match it.
  - Where the rules of that path do not match, the pair stays unordered.
- **At the end the contested pair is `R0075` and `R0085`**, on 640 points:
  integrations tickets of severity 1, without the keyword, from enterprise
  customers with 5 or more prior tickets. `R0085` lies inside `R0082`, so it
  beats it there by containment.
- **c r3 lost 420 points of `H05`'s part the same way.** Its rule of `H05`'s
  region and a rule of `T3_ENGINEERING` are both undefeated there, and the
  engine refused the edge between them for closing a cycle.

### 4. Beside the other five runs

| run | `H04`'s part right | `H05`'s part right | the queue's escalations: case, draft's points, verdict |
|---|---|---|---|
| `e r1` | 4,200 | 2,100 | 257: 420, born · 710: 2,100, born · 954: 4,200, born |
| `c r1` | 4,200 | 0 | 257: 420, unplaced · 1432: 4,200, born |
| `e r2` | 3,200 | 2,100 | 257: 2,100, born · 954: 3,200, born · 982: 840, unplaced · 1432: 4,200, unplaced · 1951: 840, unplaced |
| `c r2` | 2,560 | 0 | 954: 3,200, born · 1951: 4,200, unplaced |
| `e r3` | 4,200 | 2,100 | 257: 2,100, born · 954: 4,200, born · 1951: 4,200, born |
| `c r3` | 4,200 | 1,680 | 710: 2,100, born · 954: 2,100, unplaced · 1432: 840, unplaced · 1951: 4,200, born |

- **The narrow draft at case 954 is the model's, not c r2's.**
  - e r2 drew the same draft at the same ticket, with the same extra
    condition.
  - e r2's draft of `H04`'s region whole, at case 1432, was refused too.
  - e r1 and e r3 drew `H04`'s region whole at case 954.
  - The first call is the same request in every run, so this is the draft's
    draw.
- **Four of the six runs recall `H04`'s part whole at the end**: e r1 and e r3,
  and two channel runs. c r1 wrote it at case 1432 and c r3 at case 1951, each
  at its first draft of `H04`'s region whole.

### The expectation

| clause | what it says | reading | verdict |
|---|---|---|---|
| O1 | at least half of `H04`'s lost points are contested | 640 of 1,640, 0.3902 | **fails** |
| O2 | some rule of the queue holds `H04`'s part whole | none does | **fails** |
| O3 | every escalation on the queue's tickets ended born | 1 of 2 | **fails** |
| O4 | after some birth the base decided more of the queue right than at the end | 3,200 after case 954, against 2,560 | holds |
| O5 | the final base decides no point of `H05`'s part right | none | holds |

**The drafter expected all five to hold, bet on O1, trusted O5 most and O3
least.** O4 and O5 held, and O1, O2 and O3 failed.
- **What the account got wrong.** It had c r2 write `H04`'s region whole and
  lose part of it to contest. c r2 wrote it narrow, and most of what it lost
  was never written.
- **What it got right.** The contest was there, on the points the account
  named, through edges refused for closing a cycle.

### What it says

- **What c r2 lost beyond its draws is the loop's, as c r1's was.** Of the 4,200
  points the channel let it reach, it lost 1,640:
  - **1,000 to a narrow draft.** The model wrote `H04` with an extra condition
    at case 954, in two runs of six. The broad redraft that would have
    repaired it was refused by the placement round.
  - **640 to two refused edges.** Each later rule of another queue declared
    itself below `R0075`, as the policy orders them. The engine refused each
    edge, because the base already ordered the pair the other way through
    other rules.
- **The channel's own share is `H05`'s part.** No ticket of `H05` was
  reportable under c r2's draws, and none escalated.
- **What it leaves.**
  - **An edge refused for closing a cycle is a place where a right
    declaration buys nothing.** Where the cycle runs through rules that do not
    match the contested points, the pair stays in conflict. Which edge of a
    cycle should yield was read POST-RUN on `PLAN_BLIND.md`'s bases
    (`blind/yielding.py`). It has not been read on this plan's.
  - **The narrow draft points at the first call.** At the same ticket the model
    drew the policy's region in some runs and a narrower one in others. Under
    v1b a later, broader draft has no easier way in.

---

## Files

```
results_channel/sample.json        Stage A: the checks, the rare tickets, the space by queue,
                                   H05's points, every channel run's draws, the transcriber
                                   under every draw and trigger, the supply, the hidden
                                   policy through v1b's path, the schedule
results_channel/loop_smoke.json    Stage B's smoke run: 30 cases under the channel arm
results_channel/loop_{e,c}_r{1,2,3}.json
                                   Stage B's six runs: the header with the channel's coverage
                                   and draws, every rule in birth order, the edge log, every
                                   case's row with its cause, its draw and whether its wrong
                                   decision was reported, every escalation whole with its
                                   calls, attempts, seconds and reasoning, and rung 2's metrics
results_channel/score.json         Stage C: the six verdicts with their runs, and CH-g
results_channel/lost.json          POST-RUN: every run's lost points of SECURITY_INCIDENT by
                                   way and winner, the queue's rules, the curve, the queue's
                                   escalations, the expectation's six clauses, and the part
                                   added after the first run: what the unplaced answers left
                                   out, and the rules containing the whole queue
results_channel/oncall.json        POST-RUN: lost.json's reading for ONCALL_ESCALATION in every
                                   run, each way split by H04's part and H05's, the rules
                                   holding H04's part whole, the expectation's five clauses,
                                   and the part added after the first run: the contested
                                   pairs with the engine's verdict on every edge between them
```

What OpenRouter billed was read by generation id, and is kept outside git.
