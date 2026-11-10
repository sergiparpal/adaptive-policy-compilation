# The first call that asks for the governing rule's region whole — findings

Record opened on November 10, 2026, under [`PLAN_WHOLE.md`](../PLAN_WHOLE.md).
Sergi signed §0 on 2026-11-09, before any figure below existed, in a commit of
its own: `eb1fa29` on `main`.
- **The plan, its package, the signature, Stage A and the smoke run** reached
  `main` in #220, merged on 2026-11-09.
- **The six runs** reached it in #221, merged on 2026-11-10.
- **Stage C, this record, the banner that closes the plan and the indexes**
  reach it in #222, the pull request this record was opened in.
- **The POST-RUN reading of why v1d cut at the rarest queue's tickets** reached
  it in #223, merged on 2026-11-10.

Every record names in its `_env` the commit it was written from. Seven were
written on a pull request's branch, and the rebase merge gave each of those
commits a new hash on `main`. Each pair has the same subject, the same tree and
the same `git patch-id --stable`, and the GitHub API names the pull request
behind every `main` commit.

| record | written from | the same commit on `main` | code digest |
|---|---|---|---|
| `sample.json` | `5e87ecd`, the signature, on the branch of #220 | `eb1fa29` | `fe2b9de93993b6e0` |
| `loop_smoke.json` | `7c46bc2`, Stage A's commit, on the branch of #220 | `ed424bf` | `fe2b9de93993b6e0` |
| `loop_v1c_r1.json` | `2f3d457`, the smoke run's commit, on `main` (#220) | itself | `fe2b9de93993b6e0` |
| `loop_v1d_r1.json` | `d0e6369`, v1c r1's commit, on the branch of #221 | `987f862` | `fe2b9de93993b6e0` |
| `loop_v1c_r2.json` | `4a10369`, v1d r1's commit, on the branch of #221 | `a716f47` | `fe2b9de93993b6e0` |
| `loop_v1d_r2.json` | `62bc805`, v1c r2's commit, on the branch of #221 | `fd930c4` | `fe2b9de93993b6e0` |
| `loop_v1c_r3.json` | `2aa7928`, v1d r2's commit, on the branch of #221 | `f99e18d` | `fe2b9de93993b6e0` |
| `loop_v1d_r3.json` | `27f0a62`, v1c r3's commit, on the branch of #221 | `8439684` | `fe2b9de93993b6e0` |
| `score.json` | `0ed0a20`, v1d r3's commit, on `main` (#221) | itself | `fe2b9de93993b6e0` |

**`git_dirty` and `code_dirty` are false in every record, and every record carries
one code digest.** `main` computes it at `0ed0a20`, with
`harness.provenance.code_digest`. The package's code did not change after the
signature.

> **[NOTE 2026-11-10] One more record, written after Stage C by code added
> after it.** [`oncall.json`](oncall.json) is the POST-RUN reading of why v1d
> cut at the rarest queue's tickets.
> - **It was written from `1be27c8`**, on the branch of #223, which is `5e4200f`
>   on `main`. Its section below names the pair's checks.
> - **Its code digest is `baf839d592e56583`**, not the package's, because
>   `whole/oncall.py` was added after Stage C. `main` computes it at `5e4200f`.
>   The modules Stage C ran did not change.

**This record owns every figure in it.**

**All three stages ran on 2026-11-09 and 2026-11-10, and the six rows are
adjudicated. `WR-c` holds, thinly, `WR-d` holds, and `WR-e` holds, thinly.
`WR-a`, `WR-b` and `WR-f` are refuted. `WR-g` is reported.**

- **Told, the first call wrote the region whole more often, and not three times
  in four.** v1d's median run held its part in 28 of 51 right-queue first-call
  drafts, 0.5490. This plan's v1c held it in 35 of 80 at the median, and
  `PLAN_PLACEMENT.md`'s v1c in 35 of 92.
  - Across v1d's three runs, 41 of its 153 right-queue drafts were still the
    governing rule's region cut by one listed rule.
- **At the rarest queue's tickets the paragraph did not take.** Of v1d's 8
  first-call drafts there, 6 were cuts by one rule and 2 the region whole. Of
  v1c's 7, 3 were cuts and 4 whole.
  - Three of v1d's ended unplaced, one of its two whole drafts among them. All
    seven of v1c's were born.
- **So v1d recalled less of the rarest queue than v1c, run for run.** Its
  median recall of `ONCALL_ESCALATION` over the space is 1/3, and v1c's 11/15.
  Under each set of draws, v1d's recall less v1c's is −3/5, 0 and −2/3.
- **v1c still lost the queue on the new period, thinly.** Its median recall is
  11/15. v1c r3 recalled all of it, under draws that let the transcriber
  compile it.
- **Elsewhere the whole drafts paid.** v1d's median base decides 0.9574 of the
  space, and v1c's 0.9192.
  - Every v1c base lost a sixth of `SECURITY_INCIDENT`, 8,400 of its 50,400
    points, under a rule of that queue for which no first-call draft held its
    part.
  - v1d's bases lost at most 1,260 of those points.
- **The round refused v1d's drafts about as often as v1c's.** v1d's median run
  left 7 of its 58 escalations unplaced, and v1c's 8 of 88: a ratio of 1.3276,
  under the line of 3/2, and thin.
- **v1d asked less.** Its three runs escalated 161 times and made 298 calls.
  v1c's escalated 244 times and made 457.
- **The drafter expected all six rows to hold.** Three held, two of them
  thinly, and `WR-a`, the row it trusted most, was refuted.

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Its references were
> recomputed after the signature. Figures 1 to 4 had been seen while drafting,
> and figure 5 before the signature, as §0 says. Zero API calls.
>
> **PROVENANCE, STAGES B AND C: PRE-REGISTERED.** `WR-a` to `WR-f` were signed
> before any of their figures existed, and none of their bands was set on a
> development set. **`WR-e` is a replication** of `PL-f` on a new period. Its
> line is `PL-f`'s, drafted after that row's figures had been seen, as §0
> says, and the scoreboard should read it as a replication.
>
> **WHAT WAS SEEN BEFORE STAGE C.** The agent that launched the runs saw, before
> the scorer ran:
> - **Each record's commit message**, which the supervisor wrote from the
>   record. It gives the run's span and launches, the providers that served it,
>   its attempts' finish reasons, the attempts refused for the rate and its
>   `_env`. It gives no `whole(r)`, `space`, recall or ratio, and counts no
>   escalation, call, verdict or round, though §0 would have allowed the last
>   four (*What the runs' commits may show*).
> - **The supervisor's log**: each launch, record, commit, push and merge, with
>   its hour.
> - **The runs' progress lines**, read about every half hour. Each gives the
>   case reached, and the rules born, escalations and calls so far.
> - **The smoke run's record**, before the first run: its calls, attempts,
>   providers, finish reasons, pace by round, tokens and bill. No row reads it.
>
> The runs' bills were read after #221 merged, beside the scorer. No base, no
> `space`, no recall, no `whole(r)`, no `refused(r)` and no row was read before
> Stage C.

**Each figure names its surface.**
- **`WR-d`** reads the exhaustive space of 134,400 points. **`WR-b`, `WR-e`
  and `WR-f`** read its 6,300 points whose true queue is `ONCALL_ESCALATION`.
- **`WR-a`** reads the runs' first-call drafts of the right queue.
- **`WR-c`** reads the runs' escalations.
- **`WR-g`** reads both surfaces and says which.

The corpus is `generate_corpus(2000, seed=17)` in every run. **Both arms run
`PLAN_CHANNEL.md`'s channel arm, under `PLAN_PLACEMENT.md`'s v1c round.** A case
escalates on an IMPASSE or a CONFLICT, and on a wrong decision whose draw falls
below 1/2. Run `k` of either arm reads the draws of `PLAN_CHANNEL.md`'s c r`k`.
- **v1c** is `PLAN_PLACEMENT.md`'s v1c arm, called and not changed.
- **v1d** is v1c with one change, to the first call. v2b's paragraph on the
  base is replaced by T1 (§2.1, §5.2), which asks for the region of the list's
  rule that governs the ticket, whole. T1 names no queue and no rule.

---

## Stage A — the checks and the references

**What was run.** `python3 -m whole.sample`, on 2026-11-09, with
`PYTHONHASHSEED=0`, from the signing commit on a clean tree. The record is
[`sample.json`](sample.json).

**The blocking checks passed before anything was written.**
- **`WR-g1`.** `PLAN_PLACEMENT.md`'s six verdicts came back from its runs, and
  its own `PL-g1` to `PL-g3` passed.
  - This plan's v1c is that plan's v1c. With each of its three v1c runs'
    answers replayed, it gives back the run's record.
  - At every one of those runs' 479 calls, 253 first calls and 226 placement
    calls, v1d's proposer with v2b's text sends v1c's messages byte for byte,
    and with T1 the same but for the one paragraph.
  - The suite was green.
- **`WR-g2`.** v1c's texts are the ones `PLAN_PLACEMENT.md`'s v1c runs sent,
  and v1d's are v1c's but for T1.
  - **T1** is quoted in the plan, has §5.2's digest, keeps v2b's first
    sentence, names no queue and no rule, and is ASCII.
  - **Both arms send that plan's request**, with its pin.
  - **The drafting reading** gives back §0's figures 1 to 3 and 5.
- **`WR-g3`.** `ORDER_SEED` drew v1c first, so the schedule is v1c r1, v1d r1,
  v1c r2, v1d r2, v1c r3, v1d r3.
  - The smoke run is 30 cases under v1d, with `PLAN_CHANNEL.md`'s smoke draws.
  - The coverage is 1/2, and the cap is 400 escalations.
  - Run `k` of both arms reads `PLAN_PLACEMENT.md`'s draws of run `k`.
- **`WR-g4`.** One signature line, signed.

**Every figure §0 lists as computed while drafting came back**, figures 1 to 5,
so §0 needs no erratum.

**Figure 1: `whole(r)` on `PLAN_PLACEMENT.md`'s six runs.** v1c's median is
35/92.

| run | right-queue first-call drafts that hold their part | share |
|---|---|---|
| `PLAN_PLACEMENT.md`'s `v1c r1` | 35 of 92 | 0.3804 |
| `PLAN_PLACEMENT.md`'s `v1c r2` | 19 of 64 | 0.2969 |
| `PLAN_PLACEMENT.md`'s `v1c r3` | 35 of 85 | 0.4118 |
| `PLAN_PLACEMENT.md`'s `v1b r1` | 38 of 79 | 0.4810 |
| `PLAN_PLACEMENT.md`'s `v1b r2` | 39 of 82 | 0.4756 |
| `PLAN_PLACEMENT.md`'s `v1b r3` | 27 of 73 | 0.3699 |

**Figure 2: the lists a whole draft would have met**, on v1c's three bases
rebuilt before each recorded escalation, beside the lists those escalations
were sent.

| run | escalations | rules listed, median, as sent | rules a whole draft would have met, median | the longest |
|---|---|---|---|---|
| `PLAN_PLACEMENT.md`'s `v1c r1` | 98 | 5 | 9 | 35 |
| `PLAN_PLACEMENT.md`'s `v1c r2` | 68 | 4 | 11/2 | 23 |
| `PLAN_PLACEMENT.md`'s `v1c r3` | 87 | 5 | 6 | 43 |

**Figure 3, and the transcriber.** The transcriber is a double that writes, at
every escalation, the rule of level 3's text that governs the ticket, and places
it by the text's order. Under v1c and each run's draws:

| under | escalations | calls | `space`, of 134,400 | `corpus` | `ONCALL_ESCALATION` recall |
|---|---|---|---|---|---|
| run 1's draws | 23: 2 impasses and 21 errors | 42 | 134,380 | 1,999 of 2,000 | 1 |
| run 2's draws | 22: 2 impasses and 20 errors | 40 | 132,280 | 1,996 of 2,000 | 2/3 |
| run 3's draws | 23: 2 impasses and 21 errors | 42 | 134,380 | 1,999 of 2,000 | 1 |
| the smoke run's draws, 30 cases | 9: 2 impasses and 7 errors | 16 | 49,420 | 1,107 of 2,000 | 0 |

**Figure 5: the text's relations.** Of level 3's 29 rules, 28 lie strictly
inside a lower rule, in 61 pairs, and none holds a lower rule inside it. 233
pairs cross. 26 of the 29 cross a lower rule of another queue. `H04` lies
inside 4 lower rules and crosses 12, all of another queue; `H05` lies inside 5
and crosses 12, all of another queue.

**The draws are `PLAN_CHANNEL.md`'s.** Each stream is 2,000 floats from a string
seed through SHA-512.

| stream | seed string | digest |
|---|---|---|
| run 1 | `PLAN_CHANNEL/channel/97/r1` | `1347b9525a1e06a3` |
| run 2 | `PLAN_CHANNEL/channel/97/r2` | `e81548d721b99577` |
| run 3 | `PLAN_CHANNEL/channel/97/r3` | `1f60e3d5e68553d4` |
| the smoke run | `PLAN_CHANNEL/channel/97/smoke` | `029047351ae2d471` |

**The texts.** The two arms share the system prompt (`7b883f03a863d647`), the
placement template (`ccfd0eceba1468b2`) and the retry message
(`ca7b3803f1bef2dd`). v1c's first call carries v2b's paragraph
(`8de0ebf50ce9a54b`) and v1d's T1 (`1e054d7554c5c4f4`). Their fingerprints are
`8dc358cab48635e6` and `b957b6fa64f55478`.

---

## Stage B — the runs

**Every call ran at `deepseek/deepseek-v4-flash`, at temperature 0, with
reasoning `{"effort": "high"}` and 16,000 tokens.**
- **The pin.** The smoke run and the six runs were pinned to DeepInfra's fp8
  endpoint, `deepinfra/fp8`, with fallbacks off. There was no bridge (§2.6).
- **The path.** Every call went through `PLAN_FIRST_MATCH.md`'s asker with
  `PLAN_REASONED_LOOP.md`'s request, under level 3's system prompt.
  - The first call is blind. It carries v2b's paragraph under v1c, and T1 under
    v1d.
  - Then comes v1c's placement round, in both arms.
- **The checks.** Every launch checked the signature, the key, `WR-g1` to
  `WR-g3` and the records before it, before any call.

**How the runs were launched.** Under §2.5 Sergi chose that the agent launch
them.
- **The supervisor**, detached from the agent's harness, ran the six runs one
  at a time, in §2.3's order.
  - It committed each record alone, through the pre-commit hook, before the
    next run started.
  - It never passed the overwrite flag and never skipped the hook.
- **The pull request.** It pushed each record to #221, which it opened on its
  first push. Once both `ci-complete` runs on its last head were green, it
  merged #221 by rebase, matching that head.
- **`PLAN_PLACEMENT.md`'s supervisor skipped its first push.** That one read an
  empty list of pull requests as a closed one. This supervisor read an empty
  list as none, and every push went through on its first attempt.

### The smoke run

[`loop_smoke.json`](loop_smoke.json) ran 30 cases under v1d, with
`PLAN_CHANNEL.md`'s smoke draws, on 2026-11-09 from 09:12 to 09:33 UTC.
- **What it did.**
  - It met 14 escalations: 12 impasses and 2 reported errors.
  - It made 25 calls: 14 first calls and 11 placement rounds.
  - 11 rules were born and the validator refused 3. No proposal failed, and no
    round ended unplaced.
- **v1c's list.** 12 escalations met a rule of another queue. 11 rounds were
  sent, and 1 was not, because every rule its draft met was left out. In all, 2
  rules were left out, each containing its draft.
- **The trigger's record.** Of 5 wrong decisions, the channel reported 2, which
  escalated. 3 stood.
- **v1d's paragraph.** The record's header and its `base_text` carry T1.
- **The provider.** DeepInfra served every attempt, every one reasoned and
  ended `stop`, and none was refused for the rate.
- **The pace.** The first calls took a median of 77.1 seconds and the placement
  rounds 9.1.
- **The bill**, read by generation id before the first run, was $0.0194 for its
  25 attempts. That is $0.080 per million prompt tokens, taking completion
  tokens at twice the prompt price, as every listing of the model gives them.
- **The check passed**, so the runs could start. No row reads its answers.

### The six runs

| run | from its start to its record, UTC | how long | launches | escalations | calls | attempts | refused for the rate | billed |
|---|---|---|---|---|---|---|---|---|
| `v1c r1` | 11-09 09:53 – 11-09 12:16 | 2 h 24 min | 1 | 88 | 168 | 168 | 0 | $0.130 |
| `v1d r1` | 11-09 12:23 – 11-09 13:58 | 1 h 35 min | 1 | 48 | 91 | 91 | 0 | $0.075 |
| `v1c r2` | 11-09 14:08 – 11-09 17:06 | 2 h 58 min | 1 | 72 | 132 | 132 | 0 | $0.115 |
| `v1d r2` | 11-09 17:12 – 11-09 20:41 | 3 h 28 min | 1 | 58 | 110 | 110 | 0 | $0.096 |
| `v1c r3` | 11-09 20:47 – 11-10 02:25 | 5 h 38 min | 1 | 84 | 157 | 157 | 0 | $0.151 |
| `v1d r3` | 11-10 02:31 – 11-10 05:35 | 3 h 04 min | 1 | 55 | 97 | 97 | 0 | $0.082 |

- **A run's start is its record's `started_at`**, which the launch's checks
  precede by three to five minutes.
- **Every run reached case 2,000 in one launch.** None stopped at the cap, none
  resumed, and none recorded a failed proposal.
- **No attempt was refused for the rate.** Every one of the 755 attempts in the
  six runs reached the model. DeepInfra served each, and each ended `stop`. No
  call was asked again.
- **What was billed** was read from OpenRouter on 2026-11-10, by the generation
  id that each attempt's `call_attempts` keeps. It is not a record of this
  repository.
  - Every attempt was found.
  - The six runs came to $0.649: v1c's three to $0.396, and v1d's to $0.253.
    The smoke run came to $0.019.
- **The price per token did not move much.** By run, the price per million
  prompt tokens, completion at twice it, was between $0.0795 and $0.0840.

**Every attempt reasoned.** By run, the median reasoning ran from 3,047 to 4,067
tokens, and the most was 13,339. The records keep the reasoning whole, and no
stage codes it.

| run | calls | attempts | reached DeepInfra | refused for the rate | asked again | prompt tokens | completion tokens | reasoning tokens, median | max |
|---|---|---|---|---|---|---|---|---|---|
| `v1c r1` | 168 | 168 | 168 | 0 | 0 | 338,137 | 650,033 | 3401.0 | 11,012 |
| `v1d r1` | 91 | 91 | 91 | 0 | 0 | 194,384 | 374,342 | 3705 | 10,154 |
| `v1c r2` | 132 | 132 | 132 | 0 | 0 | 272,518 | 571,163 | 3767.5 | 13,339 |
| `v1d r2` | 110 | 110 | 110 | 0 | 0 | 235,248 | 464,403 | 3307.0 | 9,996 |
| `v1c r3` | 157 | 157 | 157 | 0 | 0 | 336,755 | 730,989 | 4067 | 11,885 |
| `v1d r3` | 97 | 97 | 97 | 0 | 0 | 201,091 | 394,617 | 3047 | 12,982 |

**The pace, by run and by round**, in seconds, from `score.json`. No call met a
refusal, so every call's seconds are its own.

| run | round | calls | median, s | minutes in all |
|---|---|---|---|---|
| `v1c r1` | first call | 88 | 63.7 | 103.4 |
| `v1c r1` | placement | 80 | 26.2 | 40.1 |
| `v1d r1` | first call | 48 | 72.6 | 69.3 |
| `v1d r1` | placement | 43 | 30.1 | 26.1 |
| `v1c r2` | first call | 72 | 98.5 | 126.6 |
| `v1c r2` | placement | 60 | 51.3 | 51.3 |
| `v1d r2` | first call | 58 | 132.7 | 141.7 |
| `v1d r2` | placement | 52 | 58.0 | 66.7 |
| `v1c r3` | first call | 84 | 168.9 | 235.0 |
| `v1c r3` | placement | 73 | 61.6 | 102.8 |
| `v1d r3` | first call | 55 | 116.8 | 139.1 |
| `v1d r3` | placement | 42 | 59.2 | 44.5 |

**The first calls slowed into the night.** In the order the runs ran, their
medians were 63.7, 72.6, 98.5, 132.7, 168.9 and 116.8 seconds. v1c r3 ran from
20:47 to 02:25 UTC and was the slowest.

> **[ERRATUM 2026-11-10] How far §1 was**, as §12 asks.
> - **The calls.** §1 said that whole drafts list more rules, so v1d should send
>   more rounds and longer ones.
>   - It sent fewer: 137 rounds across its runs against v1c's 213, because it
>     escalated less, 161 times against 244.
>   - Its lists were not longer. 16 of its 137 rounds listed eleven rules or
>     more, against 42 of v1c's 213.
> - **The money.** §1 expected one to two dollars for the six runs. They were
>   billed $0.649.
>   - At DeepInfra's listing as read on 2026-11-06, $0.09 per million prompt
>     tokens and $0.18 per million completion tokens, their tokens would have
>     cost $0.715.
> - **The time.** §1 expected 18 to 30 hours. The six runs took 19 hours 7
>   minutes between them, and 19 hours 42 minutes from the first's start to the
>   last's record.
> - **The smoke run's pace.** It measured the first calls at a median of 77.1
>   seconds, on 14 calls. The runs' first calls took medians of 63.7 to 168.9
>   seconds, by run.

---

## Stage C — the six adjudications

**What was run.** `PYTHONHASHSEED=0 python3 -m whole.score`, on 2026-11-10,
from `0ed0a20` on `main`, on a clean tree.
- **The checks.** `WR-g1` to `WR-g4` passed, with the suite green, before
  anything was written.
- **The runs.** All six were read, and none is missing. Every run's rebuilt base
  is the base its record says it ended with, and every run's calls are the calls
  its record counts.
- **The record** is [`score.json`](score.json). Zero API calls.

**Every statistic is a fraction of counts, compared with its line exactly.**
The record keeps each as a fraction beside its float.

| row | statistic | line | reading | read | verdict |
|---|---|---|---|---|---|
| WR-a | v1d's median `whole(r)` | ≥ 3/4 | **0.5490**, 28/51 | 3 runs | **refuted** |
| WR-b | v1d's median `recall_ONCALL_ESCALATION(B)` over the space | ≥ 0.90 | **0.3333**, 1/3 | 3 runs | **refuted** |
| WR-c | v1d's median `refused(r)`, over v1c's median | ≤ 3/2 | **1.3276**, 77/58, from 7/58 and 1/11 | 3 runs an arm | **holds, thin** |
| WR-d | v1c's median `space(B)`, less v1d's | ≤ 1/40 | **−0.0382**, −257/6720, from 0.9192 and 0.9574 | 3 runs an arm | **holds** |
| WR-e | v1c's median `recall_ONCALL_ESCALATION(B)` over the space | < 0.90 | **0.7333**, 11/15 | 3 runs | **holds, thin** |
| WR-f | the median over the three pairs of v1d r k's recall of the queue less v1c r k's | ≥ 1/4 | **−0.6000**, −3/5 | 3 pairs | **refuted** |

`WR-g` is reported, and everything below that is not in the table is its.

**Two verdicts are thin.**
- **`WR-c`.** Two runs, each put in place of its arm's median, would refute
  it. v1c r2's 5/72 in place of v1c's median reads 1.7379, and v1d r3's 8/55
  in place of v1d's reads 1.6000.
- **`WR-e`.** v1c r3's recall of 1, put in place of the median, would refute
  it.

**Four are not.**
- **`WR-a`.** No v1d run reaches the line. The highest, v1d r1, holds its part
  in 27 of 47 drafts, 0.5745.
- **`WR-b`.** No v1d run reaches the line. The highest, v1d r2, recalls 2/3.
- **`WR-d`.** v1c's highest run in place of v1c's median leaves −0.0352, and
  v1d's lowest in place of v1d's leaves −0.0290. Both stay under 1/40.
- **`WR-f`.** No pair reaches the line. The highest difference, under run 2's
  draws, is 0.

**Every row had a value.** Each arm has three complete runs, every v1d run has
first-call drafts of the right queue, and v1c's median `refused(r)` is not 0.

**Each row's runs:**

| run | `whole(r)` | `ONCALL_ESCALATION` recall, space | `refused(r)` | `space(B)` |
|---|---|---|---|---|
| `v1c r1` | 44 of 85, 0.5176 | 4,620 of 6,300, 11/15, 0.7333 | 8 of 88, 0.0909 | 2059/2240, 0.9192 |
| `v1c r2` | 23 of 66, 0.3485 | 4,200 of 6,300, 2/3, 0.6667 | 5 of 72, 0.0694 | 15389/16800, 0.9160 |
| `v1c r3` | 35 of 80, 0.4375 | 6,300 of 6,300, 1 | 10 of 84, 0.1190 | 2479/2688, 0.9222 |
| `v1d r1` | 27 of 47, 0.5745 | 840 of 6,300, 2/15, 0.1333 | 5 of 48, 0.1042 | 3217/3360, 0.9574 |
| `v1d r2` | 30 of 55, 0.5455 | 4,200 of 6,300, 2/3, 0.6667 | 7 of 58, 0.1207 | 549/560, 0.9804 |
| `v1d r3` | 28 of 51, 0.5490 | 2,100 of 6,300, 1/3, 0.3333 | 8 of 55, 0.1455 | 531/560, 0.9482 |

**`WR-f`'s pairs**, each under one set of draws:

| pair | v1c's recall of the queue | v1d's | v1d less v1c | the transcriber's, under the same draws |
|---|---|---|---|---|
| run 1's draws | 11/15 | 2/15 | −3/5 | 1 |
| run 2's draws | 2/3 | 2/3 | 0 | 2/3 |
| run 3's draws | 1 | 1/3 | −2/3 | 1 |

**The drafter expected all six rows to hold. Three held, two of them thinly,
and `WR-a`, `WR-b` and `WR-f` were refuted.**
- **The order of trust.** It trusted `WR-a` most, then `WR-d`, `WR-e`, `WR-f`,
  `WR-b` and `WR-c`.
- **Where it departed.** `WR-a`, first in that order, was refuted, and so were
  `WR-f` and `WR-b`, fourth and fifth. `WR-c`, last, was expected to hold
  thinly, and held thinly.
- **What §0 said of that expectation.** All six holding is the worst
  calibration pattern on `STATUS.md`'s scoreboard, and Sergi should read the
  bands as more likely too comfortable than too strict.

That is a fact about this plan, and the scoreboard counts it.

### The first-call drafts

A first-call draft is the rule the first call of an escalation drafts, before
any placement round. It holds its part when it holds the points of its governing
rule's region whose truth is its queue, by `placement/cost.py`'s class. Its
breadth sets its extension against the governing rule's region.

| run | first-call drafts | right queue | wrong queue | no rule | hold their part | cut by one rule | cut by two | other | holding their part: the region / wider / within or across |
|---|---|---|---|---|---|---|---|---|---|
| `v1c r1` | 88 | 85 | 3 | 0 | 44 | 28 | 1 | 12 | 40 / 1 / 3 |
| `v1d r1` | 48 | 47 | 0 | 1 | 27 | 10 | 1 | 9 | 25 / 1 / 1 |
| `v1c r2` | 72 | 66 | 2 | 4 | 23 | 21 | 0 | 22 | 21 / 0 / 2 |
| `v1d r2` | 58 | 55 | 0 | 3 | 30 | 16 | 0 | 9 | 29 / 0 / 1 |
| `v1c r3` | 84 | 80 | 1 | 3 | 35 | 18 | 0 | 27 | 32 / 0 / 3 |
| `v1d r3` | 55 | 51 | 0 | 4 | 28 | 15 | 0 | 8 | 28 / 0 / 0 |

- **v1d's drafts held their part in 85 of 153**, across its three runs, and
  v1c's in 102 of 231.
- **The cuts remained.** 41 of v1d's 153 were the governing rule's region cut by
  one listed rule, and 67 of v1c's 231.
- **A draft that held its part was nearly always the region itself**: 82 of
  v1d's 85, and 93 of v1c's 102. Under v1d, 1 was wider than the region and 2
  lay within or across it.
- **v1d drafted no wrong queue**, and wrote no rule 8 times. v1c drafted the
  wrong queue 6 times, and wrote no rule 7.

**Beside `PLAN_PLACEMENT.md`'s v1c runs, under the same draws.** It crosses
dates, and decides nothing.

| draws | `PLAN_PLACEMENT.md`'s v1c | this plan's v1c | v1d |
|---|---|---|---|
| run 1's draws | 35 of 92, 0.3804 | 44 of 85, 0.5176 | 27 of 47, 0.5745 |
| run 2's draws | 19 of 64, 0.2969 | 23 of 66, 0.3485 | 30 of 55, 0.5455 |
| run 3's draws | 35 of 85, 0.4118 | 35 of 80, 0.4375 | 28 of 51, 0.5490 |

Under each set of draws, v1d's share is the highest of the three, and this
plan's v1c's is above `PLAN_PLACEMENT.md`'s.

**By the draft's queue**, the drafts that held their part, of the right-queue
drafts:

| queue | `v1c r1` | `v1d r1` | `v1c r2` | `v1d r2` | `v1c r3` | `v1d r3` |
|---|---|---|---|---|---|---|
| `T1_GENERAL` | 1 of 3 | 1 of 3 | 0 of 6 | 1 of 2 | 1 of 10 | 1 of 2 |
| `T2_TECHNICAL` | 5 of 22 | 7 of 19 | 7 of 25 | 9 of 22 | 11 of 31 | 13 of 24 |
| `T3_ENGINEERING` | 4 of 6 | 4 of 4 | 3 of 5 | 4 of 6 | 4 of 5 | 3 of 5 |
| `BILLING_SPECIALIST` | 2 of 5 | 3 of 3 | 4 of 8 | 2 of 2 | 5 of 8 | 3 of 3 |
| `SECURITY_INCIDENT` | 1 of 5 | 3 of 3 | 0 of 8 | 3 of 5 | 2 of 8 | 1 of 2 |
| `ACCOUNT_MANAGER` | 3 of 7 | 5 of 7 | 5 of 6 | 5 of 9 | 4 of 7 | 4 of 9 |
| `ONCALL_ESCALATION` | 1 of 3 | 1 of 3 | 1 of 1 | 1 of 2 | 2 of 3 | 0 of 3 |
| `SELF_SERVICE_DEFLECT` | 27 of 34 | 3 of 5 | 3 of 7 | 5 of 7 | 6 of 8 | 3 of 3 |

### The rarest queue's first calls

Every first-call draft at a ticket that `H04` or `H05` governs, the two rules of
`ONCALL_ESCALATION`:

| run | case | governing rule | drafted queue | class | breadth | verdict |
|---|---|---|---|---|---|---|
| `v1c r1` | 257 | `H05` | `ONCALL_ESCALATION` | cut by one | within or across | born |
| `v1c r1` | 1432 | `H04` | `ONCALL_ESCALATION` | cut by one | within or across | born |
| `v1c r1` | 1951 | `H04` | `ONCALL_ESCALATION` | whole | the region | born |
| `v1d r1` | 257 | `H05` | `ONCALL_ESCALATION` | whole | the region | unplaced |
| `v1d r1` | 1432 | `H04` | `ONCALL_ESCALATION` | cut by one | within or across | born |
| `v1d r1` | 1951 | `H04` | `ONCALL_ESCALATION` | cut by one | within or across | unplaced |
| `v1c r2` | 954 | `H04` | `ONCALL_ESCALATION` | whole | the region | born |
| `v1d r2` | 710 | `H05` | `ONCALL_ESCALATION` | cut by one | within or across | unplaced |
| `v1d r2` | 954 | `H04` | `ONCALL_ESCALATION` | whole | the region | born |
| `v1c r3` | 710 | `H05` | `ONCALL_ESCALATION` | whole | the region | born |
| `v1c r3` | 1432 | `H04` | `ONCALL_ESCALATION` | cut by one | within or across | born |
| `v1c r3` | 1951 | `H04` | `ONCALL_ESCALATION` | whole | the region | born |
| `v1d r3` | 710 | `H05` | `ONCALL_ESCALATION` | cut by one | within or across | born |
| `v1d r3` | 1432 | `H04` | `ONCALL_ESCALATION` | cut by one | within or across | born |
| `v1d r3` | 1951 | `H04` | `ONCALL_ESCALATION` | cut by one | within or across | born |

- **v1d cut there more often than v1c.** 6 of its 8 drafts were the governing
  rule's region cut by one rule, against 3 of v1c's 7.
- **Three of v1d's ended unplaced.** Under run 1's draws, `H05`'s whole draft at
  case 257 and a cut of `H04`'s at case 1951 left a listed rule without a side.
  Under run 2's, a cut of `H05`'s at case 710 did. All seven of v1c's were
  born.
- **Under run 2's draws v1c never escalated an `H05` ticket.**

What the final bases lost of the two rules' regions, by what was drafted for
them:

| run | `H04`: lost of governed, by what was drafted | `H05` |
|---|---|---|
| `v1c r1` | 0 of 4,200, whole born | 1,680 of 2,100, cuts only |
| `v1d r1` | 3,360 of 4,200, cuts only | 2,100 of 2,100, whole not born |
| `v1c r2` | 0 of 4,200, whole born | 2,100 of 2,100, no escalation |
| `v1d r2` | 0 of 4,200, whole born | 2,100 of 2,100, cuts only |
| `v1c r3` | 0 of 4,200, whole born | 0 of 2,100, whole born |
| `v1d r3` | 2,520 of 4,200, cuts only | 1,680 of 2,100, cuts only |

### The births, and the lost points

The births by class, as `placement/births.py` reads them:

| run | births | their governing rule's region whole | cut by one rule | cut by two | other | wrong queue | narrow | narrow where a cut is possible | of them cut by one rule | cut by a rule of another queue |
|---|---|---|---|---|---|---|---|---|---|---|
| `v1c r1` | 77 | 40 | 23 | 1 | 10 | 3 | 34 | 27 | 23 | 21 |
| `v1d r1` | 41 | 24 | 9 | 0 | 8 | 0 | 17 | 13 | 9 | 8 |
| `v1c r2` | 60 | 21 | 18 | 0 | 20 | 1 | 38 | 29 | 18 | 17 |
| `v1d r2` | 44 | 25 | 13 | 0 | 6 | 0 | 19 | 16 | 13 | 12 |
| `v1c r3` | 69 | 27 | 17 | 0 | 24 | 1 | 41 | 25 | 17 | 15 |
| `v1d r3` | 40 | 21 | 11 | 0 | 8 | 0 | 19 | 17 | 11 | 11 |

| run | rules born | the governing rule's region | some listed rule's region |
|---|---|---|---|
| `v1c r1` | 77 | 37 | 37 |
| `v1d r1` | 41 | 22 | 22 |
| `v1c r2` | 60 | 19 | 20 |
| `v1d r2` | 44 | 25 | 25 |
| `v1c r3` | 69 | 24 | 24 |
| `v1d r3` | 40 | 21 | 21 |

The lost points by what was drafted for their governing rule, as
`placement/cost.py` reads them. Each cell gives the points lost of the points
those rules govern, and how many rules:

| run | points lost | no escalation | a whole draft born | a whole draft, none born | cuts only | other narrow drafts | no right-queue draft |
|---|---|---|---|---|---|---|---|
| `v1c r1` | 10,860 | 20 of 2,350 (5) | 760 of 108,750 (21) | 0 of 0 (0) | 10,080 of 18,900 (2) | 0 of 4,400 (1) | 0 of 0 (0) |
| `v1d r1` | 5,720 | 20 of 3,190 (6) | 240 of 113,790 (19) | 2,100 of 2,100 (1) | 3,360 of 10,920 (2) | 0 of 4,400 (1) | 0 of 0 (0) |
| `v1c r2` | 11,288 | 2,120 of 3,520 (6) | 120 of 66,300 (16) | 0 of 0 (0) | 480 of 2,100 (1) | 8,568 of 62,480 (6) | 0 of 0 (0) |
| `v1d r2` | 2,640 | 20 of 3,190 (6) | 520 of 122,390 (21) | 0 of 6,720 (1) | 2,100 of 2,100 (1) | 0 of 0 (0) | 0 of 0 (0) |
| `v1c r3` | 10,450 | 0 of 840 (4) | 1,945 of 86,920 (20) | 0 of 0 (0) | 0 of 0 (0) | 8,505 of 46,640 (5) | 0 of 0 (0) |
| `v1d r3` | 6,960 | 20 of 3,190 (6) | 2,260 of 106,010 (19) | 0 of 0 (0) | 4,680 of 8,400 (3) | 0 of 16,800 (1) | 0 of 0 (0) |

- **v1c's bases lost 10,860, 11,288 and 10,450 points**, and v1d's 5,720, 2,640
  and 6,960.
- **A sixth of `SECURITY_INCIDENT`.** In every v1c base, 8,400 of the queue's
  50,400 points were lost, under a rule for which no first-call draft of the
  right queue held its part: `H02` in v1c r1, whose drafts were all cuts, and
  `H01` in v1c r2 and v1c r3.
- **Under v1d**, a whole draft of `H01` was born in every run, and one of `H02`
  in two. v1d r3 lost 1,260 points under `H01`.
- **Outside the rarest queue**, v1c's bases lost 9,180, 9,188 and 10,450 points,
  and v1d's 260, 540 and 2,760.

**A narrower rule of another queue inside a whole birth cost little.** By
governing rule with a whole birth:

| run | governing rules with a whole birth | with a narrower rule of another queue inside it | points they govern | of them inside such a rule | lost | lost inside such a rule |
|---|---|---|---|---|---|---|
| `v1c r1` | 21 | 14 | 108,750 | 1,480 | 760 | 660 |
| `v1d r1` | 19 | 9 | 113,790 | 0 | 240 | 0 |
| `v1c r2` | 16 | 9 | 66,300 | 0 | 120 | 0 |
| `v1d r2` | 21 | 10 | 122,390 | 0 | 520 | 0 |
| `v1c r3` | 20 | 11 | 86,920 | 150 | 1,945 | 150 |
| `v1d r3` | 19 | 14 | 106,010 | 0 | 2,260 | 0 |

### The two arms, on both surfaces

| run | `space` | without the keyword | with it | `corpus` | `K-a` | `cover(r)` |
|---|---|---|---|---|---|---|
| `v1c r1` | 0.9192 | 0.9634 | 0.8750 | 1,947 of 2,000 | 5/71 | case 64 |
| `v1d r1` | 0.9574 | 0.9149 | 1.0000 | 1,990 of 2,000 | 3/37 | case 64 |
| `v1c r2` | 0.9160 | 0.9570 | 0.8750 | 1,988 of 2,000 | 8/51 | never |
| `v1d r2` | 0.9804 | 0.9607 | 1.0000 | 1,996 of 2,000 | 1/37 | case 50 |
| `v1c r3` | 0.9222 | 0.9695 | 0.8750 | 1,972 of 2,000 | 7/61 | case 658 |
| `v1d r3` | 0.9482 | 0.9152 | 0.9812 | 1,984 of 2,000 | 5/36 | case 50 |

- **v1d decides the keyword half whole in two runs, and 0.9812 of it in the
  third.** Every v1c base decides 0.8750 of it.
- **Without the keyword v1c's bases decide more**: 0.9570 to 0.9695, against
  v1d's 0.9149 to 0.9607. The half holds the rarest queue.
- **On the arrivals**, v1d's bases decide 1,984 to 1,996 of the 2,000 cases
  right, and v1c's 1,947 to 1,988.
- **`cover(r)`** is the case at which the base's rules first cover every point.
  It came at case 50 in v1d r2 and v1d r3, case 64 in v1c r1 and v1d r1, and
  case 658 in v1c r3. It never came in v1c r2.

### The recall of the eight queues

Over the space:

| run | `T1_GENERAL` | `T2_TECHNICAL` | `T3_ENGINEERING` | `BILLING_SPECIALIST` | `SECURITY_INCIDENT` | `ACCOUNT_MANAGER` | `ONCALL_ESCALATION` | `SELF_SERVICE_DEFLECT` |
|---|---|---|---|---|---|---|---|---|
| `v1c r1` | 0.9962 | 1.0000 | 1.0000 | 1.0000 | 0.8333 | 0.9939 | 0.7333 | 0.8465 |
| `v1d r1` | 0.9962 | 1.0000 | 0.9756 | 1.0000 | 1.0000 | 0.9976 | 0.1333 | 1.0000 |
| `v1c r2` | 0.9962 | 0.9922 | 0.9413 | 1.0000 | 0.8333 | 1.0000 | 0.6667 | 1.0000 |
| `v1d r2` | 0.9962 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9684 | 0.6667 | 1.0000 |
| `v1c r3` | 1.0000 | 0.9880 | 0.9535 | 0.9357 | 0.8333 | 0.9611 | 1.0000 | 0.9651 |
| `v1d r3` | 0.9962 | 0.9728 | 0.9413 | 1.0000 | 0.9750 | 1.0000 | 0.3333 | 1.0000 |

Over the corpus, for the four rarest queues:

| run | `ONCALL_ESCALATION` | `SECURITY_INCIDENT` | `T3_ENGINEERING` | `ACCOUNT_MANAGER` |
|---|---|---|---|---|
| `v1c r1` | 6 of 7 | 18 of 20 | 117 of 117 | 106 of 109 |
| `v1d r1` | 1 of 7 | 20 of 20 | 117 of 117 | 106 of 109 |
| `v1c r2` | 4 of 7 | 18 of 20 | 116 of 117 | 109 of 109 |
| `v1d r2` | 4 of 7 | 20 of 20 | 117 of 117 | 109 of 109 |
| `v1c r3` | 7 of 7 | 17 of 20 | 116 of 117 | 107 of 109 |
| `v1d r3` | 3 of 7 | 20 of 20 | 115 of 117 | 109 of 109 |

- **`SECURITY_INCIDENT`.** Every v1c base recalls 0.8333 of its points, and 18,
  18 and 17 of its 20 tickets. v1d's recall 1, 1 and 0.9750 of its points, and
  all 20 tickets.
- **`ONCALL_ESCALATION`.** v1c's bases recall 11/15, 2/3 and 1 of its points,
  and v1d's 2/15, 2/3 and 1/3.
- **`SELF_SERVICE_DEFLECT`.** v1c r1 recalls 0.8465 of it. Every other base
  recalls at least 0.9651.

### The placement rounds

`O` is every rule of another queue that a draft meets. v1c's list, in both arms,
lists a rule of `O` or leaves it out, and a left-out rule carries its reason:
inside the draft, containing it, or crossing it on a region already governed.

| run | rounds sent | rounds not sent | `O`, every rule of another queue met | rules listed | listed: crossing / equal | left out: inside / containing / governed |
|---|---|---|---|---|---|---|
| `v1c r1` | 80 | 3 | 780 | 332 | 331 / 1 | 179 / 123 / 146 |
| `v1d r1` | 43 | 1 | 313 | 230 | 230 / 0 | 19 / 50 / 14 |
| `v1c r2` | 60 | 0 | 469 | 401 | 401 / 0 | 10 / 20 / 38 |
| `v1d r2` | 52 | 1 | 409 | 285 | 285 / 0 | 21 / 72 / 31 |
| `v1c r3` | 73 | 1 | 783 | 633 | 633 / 0 | 16 / 18 / 116 |
| `v1d r3` | 42 | 4 | 280 | 168 | 168 / 0 | 23 / 65 / 24 |

- **Every unplaced answer left out only crossing rules**, in both arms: 23 under
  v1c and 20 under v1d.
- **Rounds not sent**, because every rule their draft met was left out: 4 under
  v1c and 6 under v1d.

| run | unplaced answers | by what they left without a side |
|---|---|---|
| `v1c r1` | 8 | crossing 8 |
| `v1d r1` | 5 | crossing 5 |
| `v1c r2` | 5 | crossing 5 |
| `v1d r2` | 7 | crossing 7 |
| `v1c r3` | 10 | crossing 10 |
| `v1d r3` | 8 | crossing 8 |

**The refusals by the length of the list**, over each arm's three runs:

| arm, three runs | lists of 1 rule: unplaced of rounds | 2 to 5 | 6 to 10 | 11 or more |
|---|---|---|---|---|
| v1c | 7 of 36 | 5 of 88 | 4 of 47 | 7 of 42 |
| v1d | 8 of 27 | 7 of 66 | 4 of 28 | 1 of 16 |

- **Under v1d the refusals did not rise with the list's length.** 8 of 27
  rounds with one rule ended unplaced, 7 of 66 with two to five, 4 of 28 with
  six to ten, and 1 of 16 with eleven or more.
- **`PLAN_PLACEMENT.md`'s v1c runs**, read the same way before the signature,
  gave 6 of 31, 5 of 83, 5 of 64 and 6 of 48.

| run | rounds | rules listed, median | the longest | lists at `ONCALL_ESCALATION` drafts | at `SECURITY_INCIDENT` drafts |
|---|---|---|---|---|---|
| `v1c r1` | 80 | 2 | 20 | 2, 5, 13 | 2, 7, 7, 8, 20 |
| `v1d r1` | 43 | 4 | 29 | 5, 6, 14 | 15, 17, 29 |
| `v1c r2` | 60 | 4.5 | 30 | 21 | 3, 3, 7, 11, 14, 17, 20, 30 |
| `v1d r2` | 52 | 4 | 20 | 3, 20 | 4, 8, 12, 13, 15 |
| `v1c r3` | 73 | 6 | 45 | 6, 17, 23 | 3, 5, 8, 15, 16, 17, 37, 45 |
| `v1d r3` | 42 | 3 | 12 | 3, 3, 3 | 7, 12 |

### The drafts, the verdicts and the edges

| run | drafts of the right queue | born | unplaced | refused | placement rounds | rules listed, median [range] |
|---|---|---|---|---|---|---|
| `v1c r1` | 85 of 88, 0.9659 | 77 | 8 | 3 | 80 | 2 [1–20] |
| `v1d r1` | 47 of 48, 0.9792 | 41 | 5 | 2 | 43 | 4 [1–29] |
| `v1c r2` | 66 of 72, 0.9167 | 60 | 5 | 7 | 60 | 4.5 [1–30] |
| `v1d r2` | 55 of 58, 0.9483 | 44 | 7 | 6 | 52 | 4 [1–20] |
| `v1c r3` | 80 of 84, 0.9524 | 69 | 10 | 5 | 73 | 6 [1–45] |
| `v1d r3` | 51 of 55, 0.9273 | 40 | 8 | 7 | 42 | 3 [1–12] |

| run | citations of `H01` to `H29` | other citations | edges by the engine's verdict | copies born |
|---|---|---|---|---|
| `v1c r1` | 98 | 310 | 288 ok, 10 closing a cycle, 18 outside the neighbourhood | 23 |
| `v1d r1` | 101 | 207 | 191 ok, 12 closing a cycle, 4 outside the neighbourhood | 5 |
| `v1c r2` | 129 | 371 | 340 ok, 24 closing a cycle, 9 outside the neighbourhood | 6 |
| `v1d r2` | 120 | 248 | 227 ok, 9 closing a cycle, 4 outside the neighbourhood | 4 |
| `v1c r3` | 107 | 481 | 440 ok, 17 closing a cycle, 7 outside the neighbourhood | 6 |
| `v1d r3` | 128 | 137 | 128 ok, 7 closing a cycle, 13 outside the neighbourhood | 2 |

- **v1c bore 206 rules, and v1d 125.** The validator refused 15 rules in each
  arm.
- **The citations** count every identifier in `beats` and `loses_to`, over both
  calls of every escalation.
  - The manual's identifiers made 334 of v1c's 1,496 citations, and 349 of
    v1d's 941.
  - None of them names a rule of a base, and each is dropped and recorded.
- **No edge was refused against containment**, in either arm.

**Every v1d birth whose round left a rule out carried the ticket's queue**, and
117 of v1c's 119:

| run | births whose round left a rule out | of them with the ticket's queue |
|---|---|---|
| `v1c r1` | 58 | 57 |
| `v1d r1` | 28 | 28 |
| `v1c r2` | 25 | 24 |
| `v1d r2` | 33 | 33 |
| `v1c r3` | 36 | 36 |
| `v1d r3` | 29 | 29 |

### The edges refused for closing a cycle

An edge the engine refused for closing a cycle is *right* when its declared
winner is the better rule over the pair's shared region, by
`rung3/edge_direction.py`'s `verdict`. It is read on the whole space and on the
half without the keyword. Beside each right edge are the points of the shared
region on which the final base leaves both rules undefeated, where the edge
would decide now. Of those, the record counts where its winner's queue is the
truth.

| run | edges refused for closing a cycle | space: right / wrong / tie or neither ever right | without the keyword: right / wrong / tie or neither | the right ones' shared points both rules still hold at the end | of them, where the winner's queue is the truth |
|---|---|---|---|---|---|
| v1c, three runs | 51 | 37 / 13 / 1 | 37 / 13 / 1 | 160 | 160 |
| v1d, three runs | 28 | 17 / 9 / 2 | 17 / 9 / 2 | 304 | 304 |
| `v1c r1` | 10 | 7 / 3 / 0 | 7 / 3 / 0 | 0 | 0 |
| `v1d r1` | 12 | 9 / 3 / 0 | 9 / 3 / 0 | 264 | 264 |
| `v1c r2` | 24 | 21 / 2 / 1 | 21 / 2 / 1 | 160 | 160 |
| `v1d r2` | 9 | 5 / 4 / 0 | 5 / 4 / 0 | 0 | 0 |
| `v1c r3` | 17 | 9 / 8 / 0 | 9 / 8 / 0 | 0 | 0 |
| `v1d r3` | 7 | 3 / 2 / 2 | 3 / 2 / 2 | 40 | 40 |

- **v1c's three runs had 51 refused edges, 37 of them right. v1d's had 28, 17
  of them right.**
- **The right ones leave few points open**: 160 under v1c and 304 under v1d, all
  where the winner's queue is the truth.

### The channel's reports

| run | impasses | conflicts | wrong decisions | reported | reported and escalated | not reported |
|---|---|---|---|---|---|---|
| `v1c r1` | 26 | 4 | 105 | 58 | 58 | 47 |
| `v1d r1` | 17 | 4 | 61 | 27 | 27 | 34 |
| `v1c r2` | 35 | 10 | 56 | 27 | 27 | 29 |
| `v1d r2` | 14 | 7 | 68 | 37 | 37 | 31 |
| `v1c r3` | 39 | 4 | 73 | 41 | 41 | 32 |
| `v1d r3` | 17 | 2 | 76 | 36 | 36 | 40 |

- **Every reported wrong decision escalated**, in every run, as
  `PLAN_CHANNEL.md` §2.2 sets.
- **The channel reported 126 of v1c's 234 wrong decisions and 100 of v1d's
  205.** The ones it did not report stood.

Reported and escalated, of the base's wrong decisions, for the rules that govern
the rarest tickets:

| governing rule | `v1c r1` | `v1d r1` | `v1c r2` | `v1d r2` | `v1c r3` | `v1d r3` |
|---|---|---|---|---|---|---|
| `H04` | 2 of 4 | 2 of 4 | 1 of 1 | 1 of 1 | 2 of 4 | 2 of 4 |
| `H05` | 1 of 2 | 1 of 3 | 0 of 3 | 0 of 2 | 1 of 2 | 1 of 3 |
| `H01` | 1 of 2 | 2 of 3 | 3 of 5 | 1 of 1 | 2 of 5 | 0 of 0 |
| `H02` | 4 of 9 | 1 of 3 | 4 of 6 | 4 of 5 | 4 of 4 | 1 of 1 |
| `H06` | 1 of 2 | 1 of 2 | 2 of 3 | 3 of 3 | 1 of 2 | 2 of 5 |

Under run 2's draws no `H05` ticket is reportable, and none escalated in either
arm.

### The rare queues

| queue | run | escalations | drafted right | tickets decided by rules | decided right |
|---|---|---|---|---|---|
| `ONCALL_ESCALATION` | `v1c r1` | 3 | 3 | 4 | 1 |
| `ONCALL_ESCALATION` | `v1d r1` | 3 | 3 | 4 | 0 |
| `ONCALL_ESCALATION` | `v1c r2` | 1 | 1 | 6 | 3 |
| `ONCALL_ESCALATION` | `v1d r2` | 2 | 2 | 5 | 3 |
| `ONCALL_ESCALATION` | `v1c r3` | 3 | 3 | 4 | 1 |
| `ONCALL_ESCALATION` | `v1d r3` | 3 | 3 | 4 | 0 |
| `SECURITY_INCIDENT` | `v1c r1` | 5 | 5 | 15 | 9 |
| `SECURITY_INCIDENT` | `v1d r1` | 3 | 3 | 17 | 14 |
| `SECURITY_INCIDENT` | `v1c r2` | 8 | 8 | 12 | 8 |
| `SECURITY_INCIDENT` | `v1d r2` | 5 | 5 | 15 | 14 |
| `SECURITY_INCIDENT` | `v1c r3` | 8 | 8 | 12 | 9 |
| `SECURITY_INCIDENT` | `v1d r3` | 2 | 2 | 18 | 18 |
| `T3_ENGINEERING` | `v1c r1` | 6 | 6 | 111 | 105 |
| `T3_ENGINEERING` | `v1d r1` | 4 | 4 | 113 | 112 |
| `T3_ENGINEERING` | `v1c r2` | 5 | 5 | 112 | 111 |
| `T3_ENGINEERING` | `v1d r2` | 7 | 6 | 110 | 109 |
| `T3_ENGINEERING` | `v1c r3` | 5 | 5 | 112 | 107 |
| `T3_ENGINEERING` | `v1d r3` | 5 | 5 | 112 | 103 |
| `ACCOUNT_MANAGER` | `v1c r1` | 7 | 7 | 102 | 97 |
| `ACCOUNT_MANAGER` | `v1d r1` | 8 | 7 | 101 | 87 |
| `ACCOUNT_MANAGER` | `v1c r2` | 6 | 6 | 103 | 96 |
| `ACCOUNT_MANAGER` | `v1d r2` | 10 | 9 | 99 | 87 |
| `ACCOUNT_MANAGER` | `v1c r3` | 7 | 7 | 102 | 99 |
| `ACCOUNT_MANAGER` | `v1d r3` | 9 | 9 | 100 | 94 |

- **The proposer drafted the right queue at every escalation of
  `ONCALL_ESCALATION`**, in every run: 15 of 15. It drafted the right queue at
  every escalation of `SECURITY_INCIDENT` too: 31 of 31.
- **As they arrived, the queue's other tickets were mostly decided wrongly.**
  Of the tickets the bases decided without escalating, v1c's decided 1 of 4, 3
  of 6 and 1 of 4 right, and v1d's 0 of 4, 3 of 5 and 0 of 4. The final bases
  are read in the recall tables above.

### Each run beside the transcriber, and beside `PLAN_PLACEMENT.md`'s runs

Under its own draws:

| run | escalations, the run / the transcriber | calls | `space` | `ONCALL_ESCALATION` recall |
|---|---|---|---|---|
| `v1c r1` | 88 / 23 | 168 / 42 | 0.9192 / 0.9999 | 11/15 / 1 |
| `v1d r1` | 48 / 23 | 91 / 42 | 0.9574 / 0.9999 | 2/15 / 1 |
| `v1c r2` | 72 / 22 | 132 / 40 | 0.9160 / 0.9842 | 2/3 / 2/3 |
| `v1d r2` | 58 / 22 | 110 / 40 | 0.9804 / 0.9842 | 2/3 / 2/3 |
| `v1c r3` | 84 / 23 | 157 / 42 | 0.9222 / 0.9999 | 1 / 1 |
| `v1d r3` | 55 / 23 | 97 / 42 | 0.9482 / 0.9999 | 1/3 / 1 |

- **v1d asked two to three times as often as the transcriber**, and v1c more
  than three times.
- **Under run 2's draws v1d r2 decides 0.9804 of the space**, against the
  transcriber's 0.9842, and recalls the transcriber's 2/3 of the queue.

Under the same draws, `PLAN_PLACEMENT.md`'s v1c run on 2026-11-07 and 2026-11-08,
then this plan's v1c and v1d runs:

| draws | `space`: `PLAN_PLACEMENT.md`'s v1c / v1c / v1d | `ONCALL_ESCALATION` recall | `refused(r)` | calls |
|---|---|---|---|---|
| run 1's draws | 0.9674 / 0.9192 / 0.9574 | 8/15 / 11/15 / 2/15 | 5/49 / 1/11 / 5/48 | 186 / 168 / 91 |
| run 2's draws | 0.9683 / 0.9160 / 0.9804 | 128/315 / 2/3 / 2/3 | 1/17 / 5/72 / 7/58 | 126 / 132 / 110 |
| run 3's draws | 0.9510 / 0.9222 / 0.9482 | 1/15 / 1 / 1/3 | 8/87 / 5/42 / 8/55 | 167 / 157 / 97 |

- **This plan's v1c decides less of the space than `PLAN_PLACEMENT.md`'s**, run
  for run, and recalls more of the rarest queue.
- **This is reported, never adjudicated.** It crosses dates.

### The direction

`RL-e`'s statistic on this plan's runs, by arm: the share of strict pairs whose
placed edge points at the better rule, by older rule, beyond the keyword. Beside
it is the Stage C ranking's reading on the same pairs and units.

| arm | units | declared: strict pairs right | declared, by older rule | ranking: strict pairs right | ranking, by older rule | difference |
|---|---|---|---|---|---|---|
| v1c | 135 | 542 of 612 | 0.9120 | 578 of 612 | 0.9437 | −0.0317 |
| v1d | 73 | 203 of 248 | 0.8069 | 221 of 248 | 0.8769 | −0.0700 |

- **In both arms the declared edges point at the better rule less often than a
  fixed ranking of the queues does**, as in `PLAN_REASONED_LOOP.md` (`RL-e` and
  `RL-f` refuted), `PLAN_CHANNEL.md` and `PLAN_PLACEMENT.md`.
- **The gap is −0.0317 under v1c, and −0.0700 under v1d.**
- Reported, and it adjudicates nothing.

### The online figures

| run | rules | escalations | coverage | reuse | end to end | silent errors | `prop` | rejected | dead |
|---|---|---|---|---|---|---|---|---|---|
| `v1c r1` | 77 | 88 | 0.9850 | 0.6623 | 0.9600 | 0.0254 | 0.9318 | 11 | 26 |
| `v1d r1` | 41 | 48 | 0.9895 | 0.8293 | 0.9715 | 0.0182 | 0.9583 | 7 | 7 |
| `v1c r2` | 60 | 72 | 0.9775 | 0.8333 | 0.9615 | 0.0164 | 0.8750 | 12 | 10 |
| `v1d r2` | 44 | 58 | 0.9895 | 0.9091 | 0.9720 | 0.0177 | 0.9138 | 14 | 4 |
| `v1c r3` | 69 | 84 | 0.9785 | 0.7971 | 0.9610 | 0.0179 | 0.9286 | 15 | 14 |
| `v1d r3` | 40 | 55 | 0.9905 | 0.8750 | 0.9675 | 0.0232 | 0.8727 | 15 | 5 |

These are rung 2's online metrics over the arrivals, as each record keeps them.
`silent errors` is its `silent_error_rate`: of the cases the engine decided with
a queue, the share whose record is wrong. `rejected` counts the escalations
whose rule was not born, unplaced or refused.

### What the verdicts say

- **Told, the first call writes the region whole more often, and still cuts**
  (`WR-a` refuted).
  - v1d's median run held its part in 0.5490 of its drafts, against 0.4375 in
    v1c's, within the period. About one draft in four was still the governing
    rule's region cut by one rule.
  - In §0's reading, the system prompt's level-1 sentence outweighs the
    paragraph, and a text that asks for the region whole is not enough at the
    first call.
- **The paragraph did not reach the rarest queue** (`WR-b` and `WR-f`
  refuted).
  - At the queue's tickets v1d cut 6 times in 8, and v1c 3 times in 7.
  - Three of v1d's drafts there ended unplaced, `H05`'s one whole draft among
    them.
  - Run for run, v1d recalled less of the queue than v1c, and never more.
- **v1c lost the queue again, thinly** (`WR-e` holds, thin).
  - Its median recall is 11/15, and v1c r3 recalled all of it.
  - In `PLAN_PLACEMENT.md` the same arm's median was 128/315 (`PL-f`
    refuted).
  - Here v1c drafted whole at 4 of the queue's 7 tickets. The draft's breadth
    is partly the draw's, as §0 said against this row.
- **Where whole drafts were born, they paid** (`WR-d` holds).
  - v1d's median base decides 0.0382 more of the space than v1c's.
  - What v1c lost and v1d did not is mostly a sixth of `SECURITY_INCIDENT`,
    under `H01` or `H02`, where no v1c first-call draft held its part.
- **The round did not refuse whole drafts much more** (`WR-c` holds, thin).
  - Under v1d the refusals did not rise with the list's length, and its lists
    were no longer than v1c's.
  - A born whole draft took away later escalations, as §0 said it might: v1d
    escalated 161 times against v1c's 244.
- **So the text moved the drafts, and not where the queue needed them.**
  - More than half the right-queue first calls held their part in every v1d
    run, and its median base decides 0.0382 more of the space than the
    period's v1c.
  - The rarest queue's tickets drew cuts under T1, and one whole draft there was
    refused. The loop under v1d did not compile the queue in any run.

### What Stage C does not settle

1. **Why v1d cut at the rarest queue's tickets more often than v1c.** Eight
   drafts stand against seven. Whether T1's wording, the system prompt's
   level-1 sentence or the draw is why would take a reading of those calls'
   notes and reasoning, which the records keep whole and no stage codes.
   **[NOTE 2026-11-10] Read POST-RUN**, in *Why v1d cut at the rarest queue's
   tickets*, below.
   - **Every cut was an intersection.** It is the governing rule's region cut by
     the first crossing rule a cut changes. Its note frames it as the end of a
     conflict, and says it wins by containment.
   - **The escalations were reported errors, framed as impasses.**
   - **T1 went mostly unquoted.** v1d's reasoning quoted it in 3 of its 8 first
     calls there. Where a cut quoted it, its second sentence was read as the
     cut's licence.
2. **Why every v1c base lost a sixth of `SECURITY_INCIDENT` here**, when
   `PLAN_PLACEMENT.md`'s v1c bases lost almost none of it. Which drafts of `H01`
   and `H02` were born, and when, would take a reading of those bases.
3. **Whether T1's ambiguity moved any draft** (§6.10): *el resto de su región*
   can be read as the draft's region or as the governing rule's.
4. **Whether a round that accepts a partial placement** would have kept v1d's
   whole draft of `H05` (§2.2).
5. **T2**, the text that names the cut and asks for nothing (§2.1).
6. **One model, one provider, one manual, one arrival order, one coverage, and
   three runs an arm.**

---

## Why v1d cut at the rarest queue's tickets — POST-RUN

> **POST-RUN.** Asked for by Sergi on 2026-11-10, after Stage C, and run the same
> day. Zero API calls. `whole/oncall.py` reads every first call on a ticket of
> `ONCALL_ESCALATION` in the six runs: 8 under v1d and 7 under v1c. For each it
> reads:
> - what the draft cut its part by, through `placement/oncall.py`'s reading,
>   called and not copied;
> - the call's note and sides;
> - its reasoning, by a codebook;
> - the placement round that followed.
>
> - **The codebook and the expectation were committed before any figure of the
>   reading existed**, in `a00187e`, which is `43323fe` on `main`. The codebook
>   was frozen on the smoke run's 14 first calls. The drafter had seen no
>   condition, note, side, reasoning or placement answer of a first call on a
>   ticket of the queue in the six runs.
> - **Three codes tried on the smoke run were dropped, because nothing told them
>   apart.**
>   - Level 1 or a particular case is in 13 of its 14 reasonings, and the
>     governing rule's identifier in all 14.
>   - At each of the 6 tickets that have a rule a cut by would change, that rule
>     stands within 300 characters of a containment word.
>
>   The reasoning walks every rule and argues containment about all of them. What
>   sets one call apart is whether it engages T1.
> - **Five gates stood before any write.**
>   - Every such escalation is governed by `H04` or `H05`, and its ticket lies
>     first in that rule's region.
>   - Each call's governing rule, class and verdict are Stage C's.
>   - Each call keeps its reasoning and its payload.
>   - The codebook gives its development counts on the smoke run.
> - **One part was added after the first run**, in `1be27c8`, which is `5e4200f`
>   on `main`: each escalation's
>   cause, and the queue the base had decided. It carries no expectation and moves
>   no clause. The five clauses came back the same from both commits.
>
> Not a signed row; no verdict moves.
> - **The record** is [`oncall.json`](oncall.json), committed in `1658269` on
>   `main`. It reached `main` in #223. It keeps every such call's quotes of T1,
>   the passage where its answer is composed, and its note, in the record's
>   Spanish.
> - **Its `_env`** names `1be27c8`, with `git_dirty` and `code_dirty` false.
>   `1be27c8` and `5e4200f` have the same subject, the same tree and the same
>   `git patch-id --stable`, and the GitHub API names #223 behind the `main`
>   commit.
> - **Its code digest**, `baf839d592e56583`, is the one `main` computes at
>   `5e4200f`.

### 1. What each first call cut, and what it was answering

| run | case | governing rule | the draft | cut by | the condition it adds | escalated as | the base had decided | verdict |
|---|---|---|---|---|---|---|---|---|
| `v1c r1` | 257 | `H05` | cut by one rule | `H20` | product dashboard | error | `T2_TECHNICAL` | born |
| `v1c r1` | 1432 | `H04` | cut by one rule | `H07`, `H15`, `H16` | product api | error | `T3_ENGINEERING` | born |
| `v1c r1` | 1951 | `H04` | whole | — | — | error | `T2_TECHNICAL` | born |
| `v1d r1` | 257 | `H05` | whole | — | — | error | `T2_TECHNICAL` | unplaced |
| `v1d r1` | 1432 | `H04` | cut by one rule | `H07`, `H15`, `H16` | product api | error | `T3_ENGINEERING` | born |
| `v1d r1` | 1951 | `H04` | cut by one rule | `H17`, `H18` | product integrations | error | `T2_TECHNICAL` | unplaced |
| `v1c r2` | 954 | `H04` | whole | — | — | error | `ACCOUNT_MANAGER` | born |
| `v1d r2` | 710 | `H05` | cut by one rule | `H17`, `H18` | product integrations | conflict | none | unplaced |
| `v1d r2` | 954 | `H04` | whole | — | — | error | `ACCOUNT_MANAGER` | born |
| `v1c r3` | 710 | `H05` | whole | — | — | error | `T3_ENGINEERING` | born |
| `v1c r3` | 1432 | `H04` | cut by one rule | `H07`, `H15`, `H16` | product api | error | `T3_ENGINEERING` | born |
| `v1c r3` | 1951 | `H04` | whole | — | — | error | `T2_TECHNICAL` | born |
| `v1d r3` | 710 | `H05` | cut by one rule | `H17`, `H18` | product integrations | error | `T3_ENGINEERING` | born |
| `v1d r3` | 1432 | `H04` | cut by one rule | `H07`, `H15`, `H16` | product api | error | `T3_ENGINEERING` | born |
| `v1d r3` | 1951 | `H04` | cut by one rule | `H17`, `H18` | product integrations | error | `T3_ENGINEERING` | born |

- **Every cut is its governing rule's region cut by the first lower listed rule
  the ticket matches that a cut changes** (Q1 holds).
  - That is `H07` at case 1432, `H17` at cases 1951 and 710, and `H20` at case
    257 under v1c.
  - Each cut adds one condition, the product of that rule. Other listed rules
    give the same intersection: `H15` and `H16` at case 1432, and `H18` at cases
    1951 and 710.
- **At case 1432 both arms cut alike**, in all four first calls (Q2 holds).
- **14 of the 15 escalations were reported errors.** The base had decided each of
  those tickets, wrongly, to `T2_TECHNICAL`, `T3_ENGINEERING` or
  `ACCOUNT_MANAGER`. The fifteenth, v1d r2's at case 710, was a conflict.
- **Every first call was told the ticket is an impasse.** The system prompt
  opens, in translation, *"The symbolic engine could not decide this ticket"*.
  The user message heads the ticket *"TICKET AT AN IMPASSE"*. The channel tells
  the proposer nothing else.

### 2. What the notes say

- **Every cut's note frames the draft as the end of a conflict.**
  - It names the governing rule and the crossing rule of another queue, and says
    the draft lies inside both.
  - It says the draft wins by containment, with no side declared.
  - The codebook counts 8 of the 9 cuts (Q5 holds). The ninth, v1d r3's at case
    1432, says it wins *"por contencion"*, a word the codebook did not carry.

  v1d r1's note at case 1432, in translation:

  > A rule that resolves the overlap between H04 (severity=1, enterprise ->
  > ONCALL) and H07 (severity=1, api -> T3). Being a particular case of both, it
  > wins automatically by containment.

- **Every whole draft's note frames the draft as the governing rule**, the
  policy's or the manual's, and declares priority over the crossing rules. v1d
  r2's at case 954, in translation:

  > This rule captures the case of severity 1 with an enterprise customer, which
  > under the company's policy must go to ONCALL_ESCALATION (H04). Priority is
  > declared against H13 (enterprise with prior_tickets_30d>=5), H20 (dashboard
  > with severity<=2) and H21 (pt with severity<=2), because those rules overlap
  > without containment, and rule H04 must prevail for coming earlier in the
  > manual's order.

So the first call answers the impasse it is told of in one of two ways. It writes
the intersection, which wins by containment, or the governing rule whole, with
sides declared. T1 asks for the second.

### 3. Whether the reasoning engaged T1

| run | case | the draft | `T1` | `T1e` | reads T1 | `INSIDE` in the note | reasoning, characters | reasoning tokens |
|---|---|---|---|---|---|---|---|---|
| `v1d r1` | 257 | whole | 1 | 0 | yes | 0 | 21,199 | 5,329 |
| `v1d r1` | 1432 | cut by one rule | 1 | 0 | yes | 1 | 9,554 | 2,440 |
| `v1d r1` | 1951 | cut by one rule | 0 | 0 | no | 2 | 22,826 | 5,728 |
| `v1d r2` | 710 | cut by one rule | 0 | 0 | no | 1 | 21,640 | 5,498 |
| `v1d r2` | 954 | whole | 0 | 0 | no | 0 | 14,402 | 3,615 |
| `v1d r3` | 710 | cut by one rule | 3 | 0 | yes | 1 | 15,388 | 3,930 |
| `v1d r3` | 1432 | cut by one rule | 0 | 0 | no | 0 | 18,521 | 4,655 |
| `v1d r3` | 1951 | cut by one rule | 0 | 0 | no | 1 | 12,973 | 3,308 |

- **v1d's reasoning quoted T1 in 3 of its 8 first calls**: 2 of its 6 cuts and 1
  of its 2 whole drafts. In the smoke run's first calls it did in 6 of 14. No
  reasoning said T1 in English.
- **Four of v1d's six cuts never quoted it** (Q3 holds).
- **v1d r2's whole draft at case 954 did not quote it either** (Q4 fails). Its
  note reads the governing rule as the policy's, as v1c's whole drafts do,
  without T1.
- **Where a cut quoted T1, the reasoning read its second sentence as licence.**
  T1 says not to add conditions to lie inside a lower rule. Its reason, in
  translation: *"a rule inside another only beats that other, and the rest of
  its region stays with rules of other queues"*.
  - **v1d r1 at case 1432**, in translation: *"This means that if our rule is a
    subset of H04, it will only beat H04, but it could also overlap other rules.
    In this case it is also a subset of H07, so it will also beat H07."*
  - **v1d r3 at case 710** read T1's first sentence as *"take that rule (H05)
    and then, if needed, add conditions so that it is more specific than the
    ones that overlap. That is what we have done."* Of the second, it asked
    whether a subset of H05 would fail to beat H17, and answered: *"No, it is
    also a subset of H17"*.
- **Where the whole draft quoted T1**, v1d r1 at case 257, the reasoning asked,
  in its own English: *"so the rule we write should be exactly H05?"*. The round
  then left that draft unplaced.

### 4. The rounds that refused v1d's drafts

| run | case | the draft | rules listed | left without a side | of which queue | placed above | placed below |
|---|---|---|---|---|---|---|---|
| `v1d r1` | 257 | whole | 14 | 12 | `T2_TECHNICAL` 6, `T3_ENGINEERING` 3, `BILLING_SPECIALIST` 2, `SECURITY_INCIDENT` 1 | 2 | 0 |
| `v1d r1` | 1951 | cut by one rule | 6 | 4 | `SECURITY_INCIDENT` 3, `T2_TECHNICAL` 1 | 2 | 0 |
| `v1d r2` | 710 | cut by one rule | 3 | 2 | `SECURITY_INCIDENT` 2 | 1 | 0 |

- **The whole draft of `H05` met 14 rules and placed 2.** It left 12 without a
  side, rules of four queues.
- **The two refused cuts by `H17` left out rules of `SECURITY_INCIDENT`**:
  three of four, and two of two.

### The expectation

| clause | what it says | reading | verdict |
|---|---|---|---|
| Q1 | every v1d cut is its governing rule's region cut by the first lower listed rule the ticket matches that a cut by would change | 6 of 6 | holds |
| Q2 | at every ticket where both arms' first calls cut, every cut there is by the same rules | case 1432: H07/H15/H16 | holds |
| Q3 | in at least 4 of v1d's cuts the reasoning neither quotes T1 nor says it in English | 4 of 6 | holds |
| Q4 | in both of v1d's whole drafts on tickets of the queue the reasoning quotes T1 or says it in English | 1 of 2 | **fails** |
| Q5 | at least half of the cuts, over both arms, carry a note that says the draft lies inside another rule | 8 of 9 | holds |

**The drafter expected all five to hold, bet on Q3, trusted Q1 most and Q4
least.** Four held, and Q4 failed.
- **What the account got right.**
  - The cuts are the ones `PLAN_PLACEMENT.md`'s runs made, by the first lower
    listed rule a cut changes.
  - The notes say they win by containment.
  - Most cuts never quoted T1.
- **What it got wrong.** A whole draft also came from a reasoning that never
  quoted T1, as the caution on Q4 said it might. And T1 did not only go unread.
  Where a cut quoted it, its second sentence was read as the cut's reason.
- **What it did not foresee.** The escalations were reported errors, framed to the
  proposer as impasses. The notes answer an impasse.

### What it says

- **The first call answers the impasse it is told of.**
  - At the queue's tickets the base had decided a wrong queue, and the first call
    is told the engine could not decide.
  - Its notes look for the conflict, and find it where the governing rule
    overlaps a crossing rule of another queue.
  - The cut is the intersection of the two, which level 1 orders with no side
    declared.
- **T1 reached few of these first calls, and where it reached a cut, it was read
  as permission.** Its second sentence says what a nested rule wins. The
  reasoning took that for the cut's justification: inside both rules, the draft
  beats both. Whether T2's wording, which names the cut and asks for nothing,
  would be read otherwise is not tested.
- **The one whole draft of `H05` that T1 produced was refused**, for leaving rules
  of other queues without a side.
- **What it leaves.**
  - **The frame.** Set an escalation that tells the proposer the base decided
    wrongly, and what it decided, beside one that calls the ticket an impasse.
    Calls.
  - **T1's second sentence**, rewritten so that it cannot be read as a cut's
    licence. Calls.
  - **The four cuts that never quoted T1.** Whether their reasoning reached the
    paragraph at all is not read beyond the codebook. The record keeps the
    passage where each composed its answer.

---

## Files

```
results_whole/sample.json        Stage A: the checks, the drafting reading (§0's figures 1
                                 to 5), the transcriber under every draw, the schedule, the
                                 channels, the streams, and both arms' texts, digests and
                                 fingerprints
results_whole/loop_smoke.json    Stage B's smoke run: 30 cases under v1d
results_whole/loop_{v1c,v1d}_r{1,2,3}.json
                                 Stage B's six runs: the header with the protocol, the pin,
                                 the coverage, the draws and the paragraph sent, every rule
                                 in birth order, the edge log, every case's row with its
                                 cause and its draw, every escalation whole with its list,
                                 what v1c's round left out and why, its calls, attempts,
                                 seconds and reasoning, and rung 2's metrics
results_whole/score.json         Stage C: the six verdicts with their runs, and WR-g
results_whole/oncall.json        POST-RUN: whole/oncall.py's reading of every first call on a
                                 ticket of ONCALL_ESCALATION in the six runs: its cut, the
                                 condition it adds, its escalation's cause and the base's
                                 decision, its note and sides, its codes, its quotes of T1,
                                 the passage where its answer is composed, its placement
                                 round, the codebook with its development counts, the five
                                 gates and the expectation's five clauses
```

What OpenRouter billed was read by generation id, and is kept outside git.
