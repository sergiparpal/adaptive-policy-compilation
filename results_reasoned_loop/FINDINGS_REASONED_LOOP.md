# The loop with reasoning on — findings

Record opened on November 3, 2026, under
[`PLAN_REASONED_LOOP.md`](../PLAN_REASONED_LOOP.md). The plan and its package
reached `main` in pull request #181, merged on 2026-10-31. Sergi signed §0 on
2026-10-31, before any figure below existed, in a commit of its own: `0acf19e`
on `main`. He signed §5.5's two amendments on 2026-10-31 and 2026-11-02, each
before any figure it governs existed: `c09f464` and `c6d7278` on `main`.
- **Stage A and the first amendment** reached `main` in #182.
- **The smoke run** reached it in #185.
- **Runs e r1 and i r1** reached it in #186.
- **The other four runs, with the second amendment,** reached it in #189.
- **Stage C, this record, the banner that closes the plan and the indexes**
  reached it in #190.

Every record names in its `_env` the commit it was written from. Five were
written on a pull request's branch, and the rebase merge gave each of those
commits a new hash on `main`. Each pair has the same subject, the same tree and
the same `git patch-id --stable`, and the GitHub API names the pull request
behind every `main` commit.

| record | written from | the same commit on `main` | code digest |
|---|---|---|---|
| `sample.json` | `8418afa`, the signature, on the branch of #182 | `0acf19e` | `acda5713d4d86014` |
| `loop_smoke.json` | `3025edd`, on `main` (#183) | itself | `714e0fc67f491061` |
| `loop_e_r1.json` | `b4b5fc3`, the smoke run's commit, on `main` | itself | `714e0fc67f491061` |
| `loop_i_r1.json` | `c2b1ffd`, e r1's commit, on the branch of #186 | `23943cb` | `714e0fc67f491061` |
| `loop_e_r2.json` | `967ab70`, i r1's commit, on `main` | itself | `714e0fc67f491061` |
| `loop_i_r2.json` | `5c24d0e`, the second amendment's signature, on the branch of #189 | `c6d7278` | `c4f449559edea52f` |
| `loop_e_r3.json` | `5047cab`, i r2's commit, on the branch of #189 | `ff4a4c6` | `c4f449559edea52f` |
| `loop_i_r3.json` | `a003aee`, e r3's commit, on the branch of #189 | `045aa73` | `c4f449559edea52f` |
| `score.json` | `8d37a7c`, i r3's commit, on `main` | itself | `c4f449559edea52f` |

- **e r2 was launched from `b7362d6`**, i r1's commit on the branch of #186,
  whose tree is `967ab70`'s. During its first resume the checkout moved to
  `main`, onto the same tree, so its record names `967ab70`.
- **Every record carries `git_dirty` and `code_dirty` false.**
- **Each code digest is the one `main` computes at the commit beside it.** Each
  was recomputed from that commit's tree with `harness.provenance.code_digest`.
  The package's code changed twice after Stage A, and each change is one of
  §5.5's signed amendments.

**This record owns every figure in it.**

**All three stages ran between 2026-10-31 and 2026-11-03, and the seven rows
are adjudicated. `RL-a`, `RL-c`, `RL-d` and `RL-g` hold, `RL-a`, `RL-d` and
`RL-g` thinly. `RL-b` is refuted, thinly. `RL-e` and `RL-f` are refuted.**

- **Asked also where its base decides wrongly, the loop with reasoning on
  compiles the policy.** The error arm's median base decides 0.9601 of the
  space right, against the impasse arm's 0.4614.
- **For the first time a loop compiles `ONCALL_ESCALATION`.** The error arm's
  median recall of the queue over the space is 14/15, 0.9333. Every impasse run
  reads 0.
- **The standing trigger did not stop asking early.** One impasse run of three
  covered the space before case 200, and one never did. No impasse run wrote
  the list's default at its first `H29` ticket. Their bases came to cover the
  space through narrow rules, or not at all.
- **The proposer drafts the right queue at 371 of its 408 escalations**,
  0.9093. At the impasses and conflicts it is right on 0.9398. At the errors,
  tickets the base had decided wrongly, it is right on 0.8884.
- **Its placements do not point the way the list orders.** Beyond the keyword
  they point at the better rule on 0.7657 by older rule, and a fixed ranking of
  the queues reads 0.8595 on the same pairs.
- **Yet in the error arm the same edges decide the order's room better than
  that ranking does**, in every run, on the same half of the space. In one run
  they do better than pointing every edge at its better rule. That reading is reported, and it qualifies
  what `RL-e` and `RL-f` measure (Stage C, *The fill*).

**[NOTE 2026-11-03] Read POST-RUN, direction and fill part in the error arm over
what `RL-e` counts.** 147 of the 169 pairs it counts against the proposer there
decide no point of the base. Third rules govern the whole shared region of 98 of
the 169. Where an edge does decide points, the proposer pointed it the way
the points ask on 0.87 to 0.94 of the units, depending on how a reversal the
engine would refuse is counted. That is above the ranking under every reading.
In the impasse arm the two do not part. See *What each placed edge decides*,
below.

**[NOTE 2026-11-03] Read POST-RUN, most unplaced answers come from the
protocol's two texts.** The system prompt tells the proposer not to declare
against a rule nested with its own, and the placement round lists such rules
and asks for a side against each. 56 of the 95 unplaced escalations left out
only rules nested with their draft. A nested rule was left out seven times as
often as a crossing one. See *Where the unplaced answers come from*, below.

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Its references were
> computed after the signature. Zero API calls.
>
> **PROVENANCE, STAGES B AND C: PRE-REGISTERED.** `RL-a` to `RL-g` were signed
> before any of their figures existed, and none of their bands was set on a
> development set.
>
> **WHAT WAS SEEN BEFORE STAGE C.**
> - The drafter of §5.5's second amendment saw e r2's `metrics` block, and the
>   amendment says so.
> - Reading e r3's record for its commit message printed its `v1b` block. That
>   block holds figures `RL-h` reports and no band reads.
> - The same reading printed one call's row whole: e r3's first draft, with the
>   start of its reasoning. That draft is one of the 408 `RL-a` reads.
> - Pull request #189 lists all three.

**Each figure names its surface.**
- **`RL-c`, `RL-d` and `RL-g`** read the exhaustive space of 134,400 points.
- **`RL-e` and `RL-f`** read its half without the security keyword.
- **`RL-a`** reads the escalations, and **`RL-b`** the arrivals' order.
- **`RL-h`** reads both surfaces and says which.

The corpus is `generate_corpus(2000, seed=17)` in every run. **The arms** are
the impasse arm, `i`, with the loop's standing trigger, and the error arm, `e`,
which also escalates a ticket the base decided with the wrong queue (§0).

---

## Stage A — the checks and the references

**What was run.** `python3 -m reasoned_loop.sample`, on 2026-10-31, with
`PYTHONHASHSEED=0`, from the signing commit on a clean tree. The record is
[`sample.json`](sample.json).

**The blocking checks passed before anything was written.**
- **`RL-g1`.** `PLAN_REASONED_RULE.md`'s checks passed and its four verdicts
  came back. `PLAN_MANUAL.md`'s three level-3 runs came back through this
  instrument. The list's first match, read from level 3's text, gives each of
  the 134,400 points of the space the queue the policy gives it. The labels
  agree with the text, a run's rebuild is its engine, and the suite was green.
- **`RL-g2`.** The texts carry their sources' digests. The hidden policy
  through v1b's path was born whole: 29 rules and 253 declarations, every one
  accepted, which installed rung 2's 199 edges. It decides both surfaces right.
  The transcriber ran as declared.
- **`RL-g3`.** `ORDER_SEED` drew the error arm first, so the schedule is e r1,
  i r1, e r2, i r2, e r3, i r3.
- **`RL-g4`.** Signed.

**Every figure §0 lists as computed while drafting came back**, so §0 needs no
erratum.

**The transcriber.** A double that answers every first call with the rule of
level 3's text that governs the ticket, and places it by the text's order
(§5.6). It ran through this plan's loop under both triggers.

| | escalations | rules | declarations accepted | `space` | `corpus` | `K-a` | `cover(r)` |
|---|---|---|---|---|---|---|---|
| under the impasse trigger | 2, both impasses, at cases 0 and 1 | 2: `H13` and `H29` | 1 of 1 | 14,820 of 134,400, 0.1103 | 298 of 2,000, 0.1490 | 1/2 | case 1 |
| under the error trigger | 23: 2 impasses and 21 errors, the last at case 954 | 23, all but `H21`, `H22`, `H23`, `H25`, `H27` and `H28` | 148 of 148 | 134,380 of 134,400 | 1,999 of 2,000 | 1/20 | case 1 |

- **Under the standing trigger it stops at case 1.** That case is an `H29`
  ticket, and `H29`'s region is the whole space, so nothing escalates again.
- **Its error run reads `RL-e`'s statistic at 71/75, 0.9467**, over 15 units:
  55 of its 59 strict pairs point at the better rule. The Stage C ranking reads
  403/450 on the same pairs, so `RL-f` reads 23/450, 0.0511. Its impasse run
  places no edge that `RL-e` reads.

**The tickets.**
- **`H29` governs 163 of the 2,000 arrivals.** The first five arrive at cases
  1, 21, 50, 64 and 86.
- **`ONCALL_ESCALATION` has 7 tickets**, at cases 257, 710, 954, 982, 1432,
  1783 and 1951. `H04` governs 4 of them and `H05` 3.
- **`SECURITY_INCIDENT` has 20 tickets, `ACCOUNT_MANAGER` 109 and
  `T3_ENGINEERING` 117.**

**The rules `PLAN_REASONED_RULE.md`'s two rule arms wrote**, over both passes,
read against the rule that governs their ticket. The regions are over the
space.

| governing rule | the reasoning rule arm's answers | the governing rule's region | inside it | the rule arm's, reasoning off: the governing rule's region |
|---|---|---|---|---|
| `H29` | 28 | 12 | 16 | 1 |
| `H28` | 16 | 10 | 6 | 0 |
| `H16` | 34 | 23 | 10 | 4 |
| `H18` | 40 | 19 | 15 | 0 |
| `H12` | 16 | 9 | 7 | 0 |

Without reasoning, the rule arm wrote the whole space on 6 of its 342 answers,
5 of them on tickets another rule governs.

**`PLAN_MANUAL.md`'s level-3 loop runs, read through this instrument.** They ran
on 2026-10-21 with reasoning off, under v1 with its screen and the standing
trigger.

| run | `space` | `corpus` | `K-a` | `cover(r)` | escalations | `prop` | `ONCALL_ESCALATION` recall, space |
|---|---|---|---|---|---|---|---|
| L3 r1 | 0.3339 | 0.6475 | 61/82 | never | 86 | 0.5465 | 0.2603 |
| L3 r2 | 0.3952 | 0.4995 | 2/3 | never | 136 | 0.5147 | 0.0635 |
| L3 r3 | 0.3778 | 0.6550 | 61/83 | never | 101 | 0.6535 | 0.2667 |

---

## Stage B — the runs

**Every call ran at `deepseek/deepseek-v4-flash`, at temperature 0, with
reasoning `{"effort": "high"}` and 16,000 tokens, pinned to Baidu with
fallbacks off.** Every call went through `PLAN_FIRST_MATCH.md`'s asker with this
plan's request, under v1b: level 3's system prompt, a blind first call, and v2b's
placement round against the base's rules of other queues that the draft
overlaps (§5). Every launch checked the signature, the key, `RL-g1` to `RL-g3`
and the records before it, before any call.

**How the runs were launched.** §1 placed every run in Sergi's terminal.
- **Who launched them.** The agent launched each one at Sergi's request,
  detached from its own harness so that the run outlived it.
- **The supervisor.** From e r2 on, a supervisor resumed a run that an outage
  had stopped, about once an hour, as Sergi asked.
- **Its limits.** It launched one run at a time and never passed the overwrite
  flag.

### The rate limit, and §5.5's first amendment

**Every launch of the smoke run on 2026-10-31 met HTTP 429 from Baidu**,
*"temporarily rate-limited upstream"*. Under §5.5 as signed, a call refused on
all three attempts was kept as a failed proposal whenever the next call was
answered. So a saturated provider could leave an escalation without a rule, and
§9's smoke check could not pass a run that met a rate limit at all.

**The amendment, signed on 2026-10-31.**
- **A call refused for the rate on every attempt is waited out.** It is asked
  again with the same messages after waits of 60, 120, 240, 480 and 960
  seconds.
- **Once every wait is spent, the run stops**, recording nothing of that call,
  and the same command resumes from the run's partial file.
- **A call any attempt of which reached the model keeps the signed rule.**
- **The smoke check reads the attempts that reached the model.**

The third launch's partial, written under the text as signed, is set aside
outside git. The first launch under the amendment was refused on all 18
attempts of its first call, and recorded nothing.

### The smoke run

[`loop_smoke.json`](loop_smoke.json) ran 30 cases under the error arm on
2026-11-01, from 09:20 to 09:44 UTC.
- **What it did.** It met 15 escalations and made 25 calls: 15 first calls and
  10 placement rounds. 14 rules were born and 1 was refused.
- **The provider.** Baidu served every attempt, and every attempt reasoned and
  ended `stop`. None was refused for the rate.
- **The pace.** The first calls took a median of 42.5 seconds and the placement
  rounds 11.1. One first call took 734 seconds, at 14 tokens a second.
- **The check passed**, so the runs could start. No row reads its answers.

### The six runs

| run | asked, UTC | launches | escalations | calls | attempts | refused for the rate | cost |
|---|---|---|---|---|---|---|---|
| `e r1` | 11-01 10:44–13:18 | 1 | 99 | 189 | 189 | 0 | $0.047 |
| `i r1` | 11-01 13:58–14:48 | 1 | 41 | 70 | 73 | 1 | $0.016 |
| `e r2` | 11-01 14:53 – 11-02 17:51 | 19 | 120 | 233 | 796 | 563 | $0.061 |
| `i r2` | 11-02 19:03–19:28 | 1 | 28 | 45 | 46 | 0 | $0.010 |
| `e r3` | 11-02 19:46–21:54 | 1 | 102 | 202 | 203 | 0 | $0.050 |
| `i r3` | 11-02 22:27–22:41 | 1 | 18 | 35 | 35 | 0 | $0.006 |

- **Every run reached case 2,000.** None stopped at the cap, and none recorded
  a failed proposal.
- **The cost** is at Baidu's listing of 2026-10-25. The six runs came to
  $0.19, and the smoke run to half a cent.

**e r2 ran through a day of outages.**
- **It stopped 17 times**, each time on one call Baidu refused on all 18 of its
  attempts, through every wait. None of those calls is recorded, and each was
  asked again on the next launch.
- **It was resumed 18 times**, about once an hour.
- **563 of its 796 attempts were refused for the rate**, on 82 calls. One call
  was answered on its 18th attempt.
- **One resume spent nothing.** `RL-g1` refused the fifteenth. A linked worktree
  outside the session had set `core.bare = true` in the repository's shared
  `.git/config`, so `git status` failed, and a test with it. The setting was
  undone outside the session, and the next resume passed every gate.

**§5.5's second amendment, signed on 2026-11-02, before i r2 started.**
- **What e r2's last launch did.** It served 141 answers from the partial file,
  and the loop timed the replay, not the call. The record keeps 0.0 seconds for
  140 of them and 0.04 for one.
- **What was lost.** The partial had kept each call's own seconds, and the run
  deletes it once the record is written.
- **The change.** A call served from the partial now keeps the seconds the
  partial kept.
- **What Stage C does with e r2.** It reads e r2's pace without those 141 calls,
  `UNTIMED = {"e_r2": 141}`. It refuses before writing unless they are the calls
  timed under a second and the call after them is not.
- **The change never ran.** No run after the amendment was resumed.

**The pin held.** Every attempt that reached the model, 778 in the six runs, was
served by Baidu and ended `stop`. The 564 refused for the rate carry no provider.

**The retries.**
- **i r1.** One call was refused for the rate once and answered on the retry.
  Two answers failed to parse and were asked again with v1's retry message.
- **i r2 and e r3.** One answer each failed to parse, though it ended `stop` at
  5,099 and 3,963 tokens. Each was asked again with v1's retry message.
- **e r2.** It retried only for the rate, 563 times.
- **No answer reached the budget.** The longest completion took 14,002 of the
  16,000 tokens.

**Every attempt that reached the model reasoned.**
- **The first calls** reasoned a median of 4,845.5 tokens over their 410
  attempts, and at most 13,766.
- **The placement rounds** reasoned a median of 2,556 over their 368, and at
  most 11,254.
- **The response carried the reasoning every time.** The records keep it whole,
  and no stage codes it.

**The record's median of reasoning tokens counts the attempts refused for the
rate**, which carry none. So `score.json` reads it at 0 for e r2 and at 3,625
for i r1. Over the attempts that reached the model, the medians are 4,467 and
3,692.5, both read from the run records' `call_attempts`. The other runs met no
refusal, and their medians stand as the record gives them.

**The pace, by run and by round.** It is in seconds, from `score.json`.
- **e r2's rows** read only the 92 calls its last launch asked. Its first 141
  calls are left out, as the second amendment says.
- **The calls that met no refusal** are counted beside the rest.

| run | round | calls | median | minutes in all | calls that met no refusal | their median |
|---|---|---|---|---|---|---|
| `e r1` | first call | 99 | 49.9 | 96.5 | 99 | 49.9 |
| `e r1` | placement | 90 | 33.4 | 57.9 | 90 | 33.4 |
| `i r1` | first call | 41 | 54.2 | 38.1 | 41 | 54.2 |
| `i r1` | placement | 29 | 21.1 | 11.9 | 28 | 19.6 |
| `e r2` | first call | 46 | 54.6 | 44.5 | 44 | 54.4 |
| `e r2` | placement | 46 | 46.0 | 40.3 | 44 | 46.0 |
| `i r2` | first call | 28 | 44.0 | 20.6 | 28 | 44.0 |
| `i r2` | placement | 17 | 14.1 | 4.2 | 17 | 14.1 |
| `e r3` | first call | 102 | 44.5 | 82.0 | 102 | 44.5 |
| `e r3` | placement | 100 | 24.8 | 46.0 | 100 | 24.8 |
| `i r3` | first call | 18 | 32.0 | 11.1 | 18 | 32.0 |
| `i r3` | placement | 17 | 11.6 | 3.4 | 17 | 11.6 |

**How far §1 was.**
- **The calls.** §1 set the stand-in's 2 to 88 escalations against an impasse
  run, and 30 to 147 against an error run. The runs met 18 to 41, and 99 to 120.
  The transcriber's 2 and about 45 calls were far below both arms.
- **The money.** §1 expected the six runs to cost under a dollar, and they cost
  $0.19.
- **The prompts.** A first call sent a median of 1,785 prompt tokens, where §1
  said about 1,850. A placement round sent 2,139 to 2,762 by run.
- **The time.** §1 priced a call at 25 seconds, from the reasoning rule asks of
  `PLAN_REASONED_RULE.md`. A first call took a median of 32.0 to 54.6 seconds
  by run.
  - **Why.** It reasoned about twice as long as those asks did: a median of
    4,845.5 tokens, against 2,126 and 2,288.
  - **The placement rounds**, which §1 could not price, took 11.6 to 46.0
    seconds.
  - **The smoke run** had measured the first calls at 42.5 seconds, on its 15
    first calls, and the runs bore that out.
- **The length of a run.** An impasse run asked for 15 to 50 minutes. An error
  run asked for 2 hours 8 minutes to 2 hours 34 minutes, when no outage stopped
  it.

---

## Stage C — the seven adjudications

**What was run.** `python3 -m reasoned_loop.score`, on 2026-11-03, with
`PYTHONHASHSEED=0`, from `8d37a7c` on `main` on a clean tree.
- **The checks.** `RL-g1` to `RL-g4` passed again, with the suite green.
- **The runs.** All six were read and none is missing. Every run's rebuilt base
  is the base its record says it ended with.
- **e r2's untimed calls** are where its record puts them.
- **The record** is [`score.json`](score.json).

**Every statistic is a fraction of counts, compared with its line exactly.**
The record keeps each as a fraction beside its float.

| row | statistic | line | reading | read | verdict |
|---|---|---|---|---|---|
| RL-a | over every escalation of both arms' runs, the right drafts | ≥ 0.90 | **0.9093**, 371 of 408 | 6 runs | **holds, thin** |
| RL-b | the share of the impasse arm's runs whose `cover(r)` falls before case 200 | ≥ 2/3 | **0.3333**, 1 of 3 | 3 runs | **refuted, thin** |
| RL-c | the error arm's median `space(B)`, less the impasse arm's | ≥ 0.10 | **+0.4987**, from 0.9601 and 0.4614 | 3 runs an arm | **holds** |
| RL-d | the error arm's median `space(B)` | ≥ 0.90 | **0.9601**, 1613/1680 | 3 runs | **holds, thin** |
| RL-e | the direction by older rule, pooled over both arms' runs, beyond the keyword | ≥ 0.90 | **0.7657**, over **202** units, from **815** of **1,019** strict pairs | 6 runs | **refuted** |
| RL-f | `RL-e`'s reading, less the Stage C ranking's on the same pairs and units | ≥ 0.00 | **−0.0937**, the ranking reading **0.8595** | 6 runs | **refuted** |
| RL-g | the error arm's median `recall_ONCALL_ESCALATION(B)` over the space | ≥ 0.90 | **0.9333**, 14/15 | 3 runs | **holds, thin** |

`RL-h` is reported, and everything below that is not in the table is its.

**Four verdicts are thin, and each turns on one run.**
- **`RL-a`.** Without e r1 it reads 0.8997.
- **`RL-b`.** One more impasse run covering the space before case 200 would have
  held it, at 2/3.
- **`RL-d`.** e r3's 0.8898, put in place of the median, falls under the line.
- **`RL-g`.** So does e r3's 11/15, 0.7333.

**`RL-c` is not thin.** The nearest any one run comes is i r2's 0.5775 in place
of the impasse arm's median, which leaves 0.3826.

**Every row had a value.** Each arm has three complete runs, `RL-a` reads 408
escalations against its minimum of 60, and `RL-e` reads 202 units against its
minimum of 20.

**Each row's runs:**

| run | drafts right | share | `cover(r)` | `space(B)` | `ONCALL_ESCALATION` recall, space |
|---|---|---|---|---|---|
| `i r1` | 39 of 41 | 0.9512 | case 722 | 0.4614 | 0 |
| `i r2` | 25 of 28 | 0.8929 | never | 0.5775 | 0 |
| `i r3` | 18 of 18 | 1.0000 | case 162 | 0.3430 | 0 |
| `e r1` | 93 of 99 | 0.9394 | case 658 | 0.9601 | 14/15 |
| `e r2` | 103 of 120 | 0.8583 | case 228 | 0.9635 | 1 |
| `e r3` | 93 of 102 | 0.9118 | case 1 | 0.8898 | 11/15 |

**The drafter expected all seven rows to hold.** Four held, three of them
thinly.
- **`RL-c`, trusted most, held by the widest margin.**
- **`RL-b`, trusted least, was refuted, thinly.**
- **`RL-e` and `RL-f`, trusted third and fourth, were refuted, and not thinly.**

That is a fact about this plan, and the scoreboard counts it.

### The two arms, on both surfaces

| run | `space` | without the keyword | with it | `corpus` | `K-a` |
|---|---|---|---|---|---|
| `i r1` | 0.4614 | 0.6043 | 0.3185 | 0.7565 | 11/36 |
| `i r2` | 0.5775 | 0.5676 | 0.5875 | 0.7045 | 1/2 |
| `i r3` | 0.3430 | 0.6110 | 0.0750 | 0.8110 | 1/16 |
| `e r1` | 0.9601 | 0.9702 | 0.9500 | 0.9950 | 8/65 |
| `e r2` | 0.9635 | 0.9298 | 0.9973 | 0.9720 | 3/41 |
| `e r3` | 0.8898 | 0.9561 | 0.8235 | 0.9900 | 1/55 |

- **The error arm compiles the policy on both surfaces.** Its bases decide 0.89
  to 0.96 of the space right, and 0.972 to 0.995 of the corpus.
- **The impasse arm's bases decide a third to three fifths of the space**, and
  between 0.70 and 0.81 of the corpus.
- **The keyword splits the impasse arm unevenly.** i r3 decides 0.6110 of the
  half without the keyword and 0.0750 of the half with it. Its base sends no
  ticket to `SECURITY_INCIDENT`, the queue of most of that half.

**`PLAN_REUSE.md`'s online set**, read as rung 2's metrics read it:

| run | rules born | escalations: impasse, conflict, error | CONFLICTs | reuse | silent error | online e2e | `prop` | decisions that stood, wrong |
|---|---|---|---|---|---|---|---|---|
| `i r1` | 37 | 41, 0, 0 | 0 | 1.0000 | 0.2476 | 0.7370 | 0.9512 | 485 of 1,959 |
| `i r2` | 25 | 28, 0, 0 | 0 | 1.0000 | 0.2992 | 0.6910 | 0.8929 | 590 of 1,972 |
| `i r3` | 16 | 18, 0, 0 | 0 | 1.0000 | 0.1912 | 0.8015 | 1.0000 | 379 of 1,982 |
| `e r1` | 76 | 31, 6, 62 | 6 | 0.8026 | 0.0020 | 0.9795 | 0.9394 | 0 of 1,901 |
| `e r2` | 90 | 27, 13, 80 | 13 | 0.6222 | 0.0071 | 0.9730 | 0.8583 | 0 of 1,880 |
| `e r3` | 63 | 2, 0, 100 | 0 | 0.8095 | 0.0045 | 0.9945 | 0.9118 | 0 of 1,898 |

- **The impasse arm decides a fifth to three tenths of its arrivals wrongly, and
  never asks about them.** None of its runs met a CONFLICT, and every rule it
  wrote fired.
- **Under the error trigger no wrong decision of the base stands**, because the
  trigger asks on every one. Its silent errors are the proposer's own wrong
  answers at error escalations: 4, 14 and 9. Each such case's record carries
  the proposer's answer as its action.
- **Copies were born in the error arm only**: 6, 23 and 6 rules whose extension
  equals an existing rule's.

### The drafts, by cause

Each case's record keeps whether the proposer named the right queue, and that
gives `RL-a`'s counts run by run. Split by the escalation's cause, pooled over
each arm's runs:

| arm | cause | right drafts |
|---|---|---|
| impasse | impasse | 82 of 87, 0.9425 |
| error | impasse | 56 of 60, 0.9333 |
| error | conflict | 18 of 19, 0.9474 |
| error | error | 215 of 242, 0.8884 |

**The errors are where the drafts fall below 0.90.** An error escalation is a
ticket a rule of the base decided wrongly, as §0 warned, and the proposer is
not told so (§6.1). At the impasses and conflicts of both arms, it is right on
156 of 166, 0.9398. That is below `RR-c`'s 0.9672, on another population.

### Cover, and why the impasse arm kept asking

The rule whose birth completed each run's cover, read from the run records:

| run | `cover(r)` | the rule born there |
|---|---|---|
| `i r1` | case 722 | `customer_tier eq enterprise AND severity gte 3` → `T1_GENERAL`, its 37th and last rule |
| `i r2` | never | its 25 rules leave part of the space uncovered; its last was born at case 762 |
| `i r3` | case 162 | `product eq mobile AND severity eq 4` → `T1_GENERAL`, its 16th and last rule |
| `e r1` | case 658 | `severity eq 1 AND product eq mobile` → `T2_TECHNICAL` |
| `e r2` | case 228 | `product eq api AND severity lte 2` → `T3_ENGINEERING` |
| `e r3` | case 1 | `severity gte 1` → `T1_GENERAL`, `H29`'s region |

- **At case 1, the first `H29` ticket, no impasse run wrote `H29`'s region.**
  - i r1 drafted `product eq dashboard AND severity eq 3` → `T2_TECHNICAL`, the
    wrong queue.
  - i r2 wrote a three-condition `T1_GENERAL` rule, and i r3 a two-condition
    one.
- **i r1's and i r3's bases covered the space by tiling it with narrow rules**,
  and stopped asking with the rule that closed the last gap. i r2's never
  closed it, and no arrival after case 762 fell in what was left.
- **Only e r3 wrote the default at case 1.** Under the standing trigger that
  would have ended its asking there, as it ended the transcriber's. Under the
  error trigger it was asked 100 more times, each on an error.

**So the impasse arm compiled more than the transcriber did under the same
trigger**: 0.3430 to 0.5775 of the space, against 0.1103. It did not write the
default, and kept asking. It still compiled far less than the error arm,
because it never asks where a rule decides wrongly.

### The births, against the list

| run | rules born | a listed rule's region | the governing rule's region |
|---|---|---|---|
| `i r1` | 37 | 10 | 10 |
| `i r2` | 25 | 8 | 8 |
| `i r3` | 16 | 7 | 7 |
| `e r1` | 76 | 21 | 21 |
| `e r2` | 90 | 21 | 20 |
| `e r3` | 63 | 18 | 18 |

**In the loop, the proposer wrote the governing rule's region on 84 of its 307
births, about a quarter.** Asked once, without a loop, the reasoning rule arm
wrote it on 250 of 342 answers. The populations differ: here the births exclude
refused rules, and the tickets are the loop's escalations. And the first call's
line for the base differs. It says *no se te muestra en este paso*, where the
re-ask's said *vacia. Esta es la primera regla*. Nothing here says which of
these narrowed the rules.

### The escalations' verdicts, and the placement rounds

| run | born | unplaced | rejected | changed |
|---|---|---|---|---|
| `i r1` | 37 | 3 | 1 | 0 |
| `i r2` | 25 | 3 | 0 | 0 |
| `i r3` | 16 | 2 | 0 | 0 |
| `e r1` | 76 | 21 | 1 | 1 |
| `e r2` | 90 | 28 | 1 | 1 |
| `e r3` | 63 | 38 | 1 | 0 |

- **95 of the 408 escalations ended unplaced**: a listed rule was left out of
  the second answer, or the placement never came back.
  - 4 rules failed the validator, and 2 placements changed the draft's rule.
  - Every attempt ended `stop`, so the 95 are answers, not lost calls.
- **A refused rule is not born** (§2.2), but its answer still decides the case.
  Under the error trigger, a later ticket the base still decides wrongly
  escalates again. e r3 left 38 of its 102 escalations unplaced.

| run | rounds | rules listed, median | max | citations of `H01` to `H29` | other citations | edges by the engine's verdict |
|---|---|---|---|---|---|---|
| `i r1` | 29 | 2 | 13 | 47 | 101 | 91 ok, 2 closing a cycle, 9 outside the neighbourhood |
| `i r2` | 17 | 2 | 11 | 20 | 45 | 43 ok, 7 outside the neighbourhood |
| `i r3` | 17 | 1 | 5 | 14 | 32 | 32 ok |
| `e r1` | 90 | 7 | 59 | 126 | 943 | 616 ok, 65 closing a cycle, 5 outside the neighbourhood |
| `e r2` | 113 | 8 | 60 | 213 | 1,201 | 857 ok, 43 closing a cycle, 9 outside the neighbourhood |
| `e r3` | 100 | 7.5 | 39 | 147 | 744 | 447 ok, 16 closing a cycle, 8 outside the neighbourhood, 1 against containment |

- **The citations** count every identifier in `beats` and `loses_to`, over both
  calls of every escalation.
- **The manual's identifiers took the place of the base's in about one citation
  in six**: 567 of 3,633. None of them names a rule of a base, and each is
  dropped and recorded (§5.2).
- **The error arm's lists ran long**, up to 60 rules. The engine refused 124 of
  its edges for closing a cycle, and 2 of the impasse arm's.

### The direction, beyond `RL-e`

`RL-e`'s population is every placed edge the engine accepted, between rules of
different queues, neither of them a keyword rule.

| reading | units | reading by older rule | strict pairs pointing at the better rule |
|---|---|---|---|
| beyond the keyword, `RL-e` | 202 | 0.7657 | 815 of 1,019, 0.7998 |
| over the whole space | 199 | 0.7762 | 812 of 1,009 |
| on the corpus cases without the keyword | 185 | 0.7593 | 679 of 859 |
| the new rule always wins, on `RL-e`'s pairs | 202 | 0.5545 | 537 of 1,019 |
| the Stage C ranking, on `RL-e`'s pairs (`RL-f`) | 202 | 0.8595 | |

- **By declared winner** the reading is 0.7176, over 200 winners. The largest
  unit holds 28 pairs. No pair was a tie, and 65 were left out because neither
  rule is ever right on their shared region.
- **`B-d`'s split.**
  - **Pairs a fixed ranking can answer.** These are pairs whose better rule
    always carries the same queue. They cover 12 of the 20 queue pairs, and on
    them the placements read 0.9364 by older rule, over 127 units.
  - **Pairs the policy points both ways.** On the other 8 queue pairs the
    placements read 0.6916, over 164 units.
  - **The units overlap**, because an older rule can carry pairs of both kinds.
- **Across protocols.** `K-b`, under v2b with reasoning off and no manual, read
  0.5460 by older rule on 65 units, and the ranking 0.7219 on its pairs. Here
  the direction is higher and the ranking is still above it. That comparison
  crosses protocols and populations, and adjudicates nothing.

### The fill of the order's room

The room is the points of the half without the keyword where some rule that
subsumption leaves undefeated carries the true queue, and subsumption alone
does not decide them right. Every arm installs the run's own accepted edges, on
its final rules. Only the direction of each edge between two queues changes:
- **declared**, as the proposer declared it;
- **ranking**, at the queue the Stage C ranking puts first;
- **coin**, by a fair coin, over 200 draws;
- **newborn**, at the rule born later;
- **oracle**, at the better rule over the pair's shared region, `RL-e`'s
  notion of right.

The share of the room each arm decides right:

| run | room, points | edges | declared | ranking | coin, mean (central 90%) | newborn | oracle |
|---|---|---|---|---|---|---|---|
| `i r1` | 22,020 | 91 | 0.6177 | 0.8233 | 0.4069 (0.2284–0.5753) | 0.2516 | 0.9233 |
| `i r2` | 15,920 | 43 | 0.8869 | 0.9146 | 0.4181 (0.1281–0.7864) | 0.1131 | 1.0000 |
| `i r3` | 22,320 | 32 | 0.8656 | 1.0000 | 0.3593 (0.1828–0.5681) | 0.2276 | 1.0000 |
| `e r1` | 31,972 | 616 | 0.9637 | 0.8643 | 0.4230 (0.2816–0.5632) | 0.4478 | 0.9525 |
| `e r2` | 46,080 | 857 | 0.9410 | 0.7371 | 0.3212 (0.2245–0.4374) | 0.3346 | 0.9983 |
| `e r3` | 23,740 | 447 | 0.9843 | 0.7767 | 0.4696 (0.3117–0.6411) | 0.6790 | 0.9983 |

- **The declared edges' lead is not resolving.** In the error arm they resolve
  0.9937, 0.9896 and 0.9983 of the room, and decide 0.9698, 0.9509 and 0.9860
  of what they resolve right. The ranking resolves 1.0000, 0.9475 and 0.9983,
  and decides 0.8643, 0.7779 and 0.7781 of it right.
- **In the error arm the declared edges fill more of the room than the ranking
  does, in every run.** In e r1 they also fill more than the oracle. So pointing
  every edge at its pair's better rule is not what decides the base's points
  right. A third rule can govern most of a pair's shared region, which is why
  exact list order reads 71/75 and not 1 on `RL-e`'s statistic (§0).
- **In the impasse arm the ranking fills more than the declared edges**, in
  every run.
- **No coin draw reached the declared fill in the error arm.**

**What this does to `RL-e` and `RL-f`.** Both are refuted as signed, and stay
so. They read whether each placed edge points at its pair's better rule, and
the proposer does that less often than a ranking does. The fill reads what the
edges decide together. There, in the error arm, the proposer's edges beat the
ranking. These readings are reported and adjudicate nothing.

### The rarest queues

Escalations of each queue, the drafts among them that named it, and the
arrivals of the queue the base decided, with how many it decided right:

| run | `ONCALL_ESCALATION` escalations | drafts right | decided by a rule | right | `SECURITY_INCIDENT` escalations | drafts right | decided by a rule | right |
|---|---|---|---|---|---|---|---|---|
| `i r1` | 0 | 0 | 7 | 0 | 1 | 1 | 19 | 3 |
| `i r2` | 0 | 0 | 7 | 0 | 1 | 1 | 19 | 12 |
| `i r3` | 0 | 0 | 7 | 0 | 0 | 0 | 20 | 0 |
| `e r1` | 3 | 3 | 4 | 4 | 13 | 13 | 7 | 7 |
| `e r2` | 6 | 6 | 1 | 1 | 6 | 6 | 14 | 14 |
| `e r3` | 6 | 6 | 1 | 1 | 10 | 10 | 10 | 10 |

- **The impasse arm never escalated an `ONCALL_ESCALATION` ticket**, and its
  rules sent all 7 elsewhere, in every run. Its bases never ask about a ticket a
  rule covers.
- **The error arm named the queue at every escalation of it**, 15 of 15, and
  its bases decided right every ticket of it they decided.
- **`SECURITY_INCIDENT` behaves the same way.** Every draft at its escalations
  named it, 29 of 29 in the error arm. Every ticket of it the error arm's bases
  decided, they decided right. The impasse arm's bases decided 15 of its 58
  right.

`ACCOUNT_MANAGER` and `T3_ENGINEERING` are read the same way in the record.
Every draft at their escalations named them, in every run. The error arm's
bases decided every ticket of theirs right. The impasse arm's decided 52, 45
and 42 of `ACCOUNT_MANAGER`'s right, and 74, 0 and 0 of `T3_ENGINEERING`'s.

### The recall of the eight queues

Over the space:

| queue | `i r1` | `i r2` | `i r3` | `e r1` | `e r2` | `e r3` |
|---|---|---|---|---|---|---|
| `T1_GENERAL` | 0.7759 | 0.8391 | 1.0000 | 0.9962 | 0.7893 | 0.9962 |
| `T2_TECHNICAL` | 0.5370 | 0.6340 | 0.5697 | 0.9989 | 0.9336 | 0.9695 |
| `T3_ENGINEERING` | 0.5257 | 0.0000 | 0.0000 | 0.8142 | 1.0000 | 1.0000 |
| `BILLING_SPECIALIST` | 0.6959 | 0.5029 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| `SECURITY_INCIDENT` | 0.3333 | 0.6667 | 0.0000 | 0.9333 | 1.0000 | 0.7667 |
| `ACCOUNT_MANAGER` | 0.4959 | 0.5377 | 0.5450 | 1.0000 | 0.9209 | 0.9859 |
| `ONCALL_ESCALATION` | 0.0000 | 0.0000 | 0.0000 | 0.9333 | 1.0000 | 0.7333 |
| `SELF_SERVICE_DEFLECT` | 0.9837 | 0.9488 | 0.9674 | 1.0000 | 0.9860 | 1.0000 |

Over the corpus:

| queue | `i r1` | `i r2` | `i r3` | `e r1` | `e r2` | `e r3` |
|---|---|---|---|---|---|---|
| `T1_GENERAL` | 0.7137 | 0.8941 | 1.0000 | 0.9961 | 0.9020 | 0.9961 |
| `T2_TECHNICAL` | 0.7658 | 0.7080 | 0.7934 | 0.9945 | 0.9725 | 0.9793 |
| `T3_ENGINEERING` | 0.6752 | 0.0000 | 0.0000 | 0.9658 | 1.0000 | 1.0000 |
| `BILLING_SPECIALIST` | 0.5756 | 0.4871 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| `SECURITY_INCIDENT` | 0.2500 | 0.7500 | 0.0000 | 1.0000 | 1.0000 | 0.8500 |
| `ACCOUNT_MANAGER` | 0.5046 | 0.4312 | 0.3945 | 1.0000 | 0.9725 | 1.0000 |
| `ONCALL_ESCALATION` | 0.0000 | 0.0000 | 0.0000 | 0.8571 | 1.0000 | 0.8571 |
| `SELF_SERVICE_DEFLECT` | 0.9697 | 0.9556 | 0.9636 | 1.0000 | 0.9838 | 1.0000 |

### Beside the references

| | `space` | `corpus` | escalations | `cover(r)` |
|---|---|---|---|---|
| the transcriber, impasse trigger | 0.1103 | 0.1490 | 2 | case 1 |
| the impasse arm, by run | 0.4614, 0.5775, 0.3430 | 0.7565, 0.7045, 0.8110 | 41, 28, 18 | 722, never, 162 |
| `PLAN_MANUAL.md`'s level-3 loop, by run | 0.3339, 0.3952, 0.3778 | 0.6475, 0.4995, 0.6550 | 86, 136, 101 | never in any |
| the transcriber, error trigger | 134,380 of 134,400 | 1,999 of 2,000 | 23 | case 1 |
| the error arm, by run | 0.9601, 0.9635, 0.8898 | 0.9950, 0.9720, 0.9900 | 99, 120, 102 | 658, 228, 1 |
| the 29 rules compiled once, `G-a` | 1.0000 | | | |

- **The impasse arm against `PLAN_MANUAL.md`'s level-3 loop.** That loop ran
  with reasoning off, under v1's screen, on 2026-10-21.
  - Against it, the impasse arm compiled more of the space, 0.4614 at the
    median against 0.3778, and drafted the right queue far more often: `prop`
    0.9512, 0.8929 and 1.0000, against 0.5465, 0.5147 and 0.6535.
  - It asked less than half as often, and its `K-a` is lower.
  - That loop recalled `ONCALL_ESCALATION` on 0.2603, 0.0635 and 0.2667 of the
    queue's space, where the impasse arm recalls none.
  - The comparison crosses dates and protocols, and §13 reports it without
    adjudicating it.
- **The error arm comes within a tenth of the transcriber under its trigger** in
  every run but e r3. The transcriber asked 23 times; the error arm asked 99 to
  120.

### What the verdicts say

- **What limits the loop with reasoning on is the trigger** (`RL-c` holds, and
  `RL-b` is refuted, thinly). §0 read this pair in advance. The impasse arm kept
  asking, and still compiled less, because it never asks where a rule already
  decides wrongly. Its bases decide a fifth to three tenths of the arrivals
  wrongly.
- **Asked on its errors, the loop compiles the policy** (`RL-d` holds, thin).
  - Its median base decides 0.9601 of the space right, and two runs of three
    reach 0.96.
  - The third, e r3, wrote the default at case 1, and left 38 of its 102
    escalations unplaced. It reached 0.8898.
- **For the first time a loop compiles `ONCALL_ESCALATION`** (`RL-g` holds,
  thin).
  - It does so only under a trigger that reads the truth of every arrival, and
    e r3's base recalls 0.7333 of the queue's space.
  - What stays open of `STATUS.md`'s third item is a trigger a deployment
    could have.
- **The proposer of the loop chooses its queue nearly as the re-ask did**
  (`RL-a` holds, thin), and least well where the base had erred.
- **Its placements do not point as the list orders** (`RL-e` and `RL-f`
  refuted).
  - Edge by edge, a fixed ranking of the queues points the same pairs better.
  - Where a ranking can answer a queue pair, the placements point right on
    0.9364. Where the policy points the pair both ways, on 0.6916.
  - The manual's identifiers took the place of the base's in about one
    citation in six.
  - Read together over the room, the error arm's edges decide more of it right
    than the ranking's do.

### What Stage C does not settle

1. **Why the loop's proposer wrote narrow rules.** It wrote the governing
   rule's region on about a quarter of its births. At case 1 no impasse run
   wrote the default, which the re-ask wrote on 12 of 28 `H29` tickets. The
   first call's base line, the population and the loop itself all differ from
   the re-ask, and nothing here separates them.
2. **Why direction and fill part.** `RL-e` reads each pair alone, over its
   shared region. The fill reads the base's points with every edge in place. A
   reading would set each edge's verdict beside the points it decides.
   **[NOTE 2026-11-03] Read POST-RUN**, in *What each placed edge decides*,
   below. In the error arm the pairs `RL-e` counts against the proposer mostly
   decide nothing, because third rules govern their shared region. The edges
   that decide points mostly point right. In the impasse arm they do not part.
3. **Where the unplaced answers come from.** 95 of 408 escalations ended
   unplaced, 38 in e r3. The reasoning is recorded whole on every attempt, and
   coded by no stage.
   **[NOTE 2026-11-03] Read POST-RUN**, in *Where the unplaced answers come
   from*, below. Most left out rules nested with their draft, as the system
   prompt says to, in a round that lists them. e r3's count is its default,
   which contains every later draft.
4. **A trigger that reads no truth.** The error arm reads the label of every
   arrival, as no deployment could (§13).
5. **Reasoning in the loop apart from v1b.** No reasoning-off arm ran under
   v1b. The level-3 loop beside the impasse arm crosses dates and protocols
   (§13).
6. **The arrivals' order.** One corpus, in which the default arrives second.
7. **One model, one provider, one manual, one effort, three runs an arm.**

---

## What each placed edge decides — POST-RUN

> **POST-RUN.** Asked for by Sergi on 2026-11-03, after the plan closed, and run
> the same day. Zero API calls. `reasoned_loop/decided.py` set each edge of
> Stage C's rows beside the points it decides, over the half of the space
> without the keyword, where `RL-e` and the fill read.
> - **The expectation was committed before any figure of the reading
>   existed.** It is five clauses in the module's docstring, committed as
>   `35669cd`, which is `0d9a648` on `main`. The drafter had read this record
>   whole, and `score.json`'s fill by run and arm.
> - **Five gates stood before any write.**
>   - `RL-e` and `RL-f`'s ranking come back exactly.
>   - Every run's room and declared fill come back.
>   - The fill's engine is Stage C's graph.
>   - A reversal read by masks is the engine's reinstall through `try_edge`, on
>     the first edges of every run whose reversal the engine accepts.
>   - Added after the first run: the record already on disk comes back.
> - **The module was extended after its first run, with no expectation**, in
>   `444ece2`, which is `2943170` on `main`. Most of the reversals it counts
>   would close a cycle (section 5, below). The record comes from the second
>   run, which gave back every figure of the first. The first run's record is
>   in `d0c2a8b` on `main`.
>
> Not a signed row; no verdict moves. The record is [`decided.json`](decided.json).
> It reached `main` in pull request #192. Its `_env` names the branch commit it
> was written from, `444ece2`, with a clean tree. That commit and `2943170` have
> the same subject, the same tree and the same `git patch-id --stable`, and the
> GitHub API names #192 behind the `main` commit. Its code digest,
> `40f5b242c7e09b6f`, is the one `main` computes at `2943170`.

**How an edge is read.**
- **The reversal** points one edge the other way and leaves every other edge in
  place. It is read by masks, with the engine's own rule: a rule is undefeated
  exactly where no rule that beats it matches.
- **What an edge decides** is the points whose rightness its reversal changes.
  Its **point verdict** is `a` when the declared direction decides more of them
  right, `b` when the reversal does, and *none* when the reversal changes no
  point.
- **The pair verdict** is `RL-e`'s: the better rule over the pair's whole shared
  region.
- **The free verdict** reads the same region, less the points where third rules
  defeat both rules of the pair. The edge cannot decide anything there.
- **A missing pair** is one whose pair verdict is `b`: `RL-e` counts it against
  the proposer.

### 1. The pair verdict against the point verdict

`RL-e`'s strict pairs, by arm:

| arm | pair verdict | pairs | point `a` | point `b` | tie | decides no point |
|---|---|---|---|---|---|---|
| error | `a` | 729 | 356 | 0 | 1 | 372 |
| error | `b`, missing | 169 | 3 | 19 | 0 | 147 |
| impasse | `a` | 86 | 68 | 0 | 0 | 18 |
| impasse | `b`, missing | 35 | 0 | 20 | 0 | 15 |

- **In the error arm, 147 of the 169 missing pairs decide no point.** Reversed,
  they change nothing the base decides. 19 cost points, and 3 decide their
  points right.
- **Where both verdicts are strict, they almost always agree.** Of the 466 edges
  of both arms that decide points, 3 have pair verdict `b` and point verdict
  `a`, and none the other way. So the better rule over a pair's region is nearly
  always the better winner where the edge decides. Edges acting together do not
  carry the parting.
- **In the impasse arm the missing pairs do decide points.** 20 of 35 cost
  points, and 15 decide none.

### 2. `RL-e`'s statistic, read three ways

By older rule, on `RL-e`'s population, with the Stage C ranking on the same
pairs:

| arm | verdict | units | strict pairs | declared | ranking |
|---|---|---|---|---|---|
| error | pair, `RL-e`'s | 164 | 898 | 0.7811 | 0.8533 |
| error | free | 157 | 636 | 0.8510 | 0.8593 |
| error | point | 135 | 378 | 0.9422 | 0.8680 |
| error | pair, where the point is strict | 135 | 378 | 0.9378 | 0.8725 |
| impasse | pair, `RL-e`'s | 38 | 121 | 0.6992 | 0.8860 |
| impasse | free | 36 | 103 | 0.7405 | 0.8796 |
| impasse | point | 33 | 88 | 0.7435 | 0.8687 |
| both | pair: `RL-e` and `RL-f`'s ranking | 202 | 1,019 | 0.7657 | 0.8595 |
| both | point | 168 | 466 | 0.9032 | 0.8682 |

- **In the error arm, the direction rises as the reading narrows to what the
  edge decides.** It reads 0.7811 over the whole shared region, 0.8510 off the
  points third rules govern, and 0.9422 on the points it decides. The ranking
  stays near 0.86 throughout.
- **On the edges that decide points, the pair verdict itself reads 0.9378.** So
  what moves the statistic is which pairs are read, not how each is judged.
- **In the impasse arm the ranking stays above the proposer on every reading**,
  as it fills more of the room.

### 3. What the missing pairs weigh, and who governs them

The error arm's strict pairs. The points are summed edge by edge, so a point two
reversals change counts twice.

| pair verdict | pairs | changing a point | points gained | points lost | mean points changed | median share third rules govern | wholly governed |
|---|---|---|---|---|---|---|---|
| `a` | 729 | 357 | 212,577 | 725 | 292.6 | 1/2 | 164 |
| `b`, missing | 169 | 22 | 360 | 3,396 | 22.2 | 1 | 98 |

- **Third rules govern the missing pairs.** More than half of them have their
  whole shared region under third rules, against fewer than a quarter of the
  pairs pointed right.
- **A missing pair weighs about a thirteenth of a pair pointed right**, in the
  points its reversal changes.
- **In the impasse arm third rules govern little.** The median share is 0 for
  both kinds of pair.

### 4. The points no single edge decides

| run | the room's right points | changed by some single reversal | by none |
|---|---|---|---|
| `i r1` | 13,602 | 10,958 | 2,644 |
| `i r2` | 14,120 | 14,120 | 0 |
| `i r3` | 19,320 | 19,320 | 0 |
| `e r1` | 30,812 | 24,112 | 6,700 |
| `e r2` | 43,360 | 36,280 | 7,080 |
| `e r3` | 23,368 | 21,500 | 1,868 |

In the error arm, between a twelfth and a fifth of the room's right points are
decided by several edges at once, or by none of them alone.

### 5. The reversals the engine would refuse — added after the first run

- **813 of the 1,084 rows of `RL-e`'s population carry a reversal that would
  close a cycle**: 752 of the error arm's 956, and 61 of the impasse arm's 128.
  The engine would refuse each of them.
- **Where every rule of such a cycle matches, the reversed relation leaves no
  rule undefeated.** The first run counted what the base gets right there as a
  gain of the declared direction. That is 129,046 of the 212,937 points the
  error arm's reversals gained, and 12,710 of the impasse arm's 60,463.
- **So the point verdict leaned toward the declared direction by
  construction.** The engine has no such alternative. The module was extended
  to read each edge again two ways, with no expectation:
  - **discounted**: without the gains at those points;
  - **against the engine's alternative**: the reversal where the engine would
    accept it, and the edge taken out where it would refuse it.

| arm | reading | units | strict | declared | ranking | missing pairs costing points | mean points changed, `a` / missing |
|---|---|---|---|---|---|---|---|
| error | as written | 135 | 378 | 0.9422 | 0.8680 | 19 of 169 | 292.6 / 22.2 |
| error | discounted | 98 | 177 | 0.8683 | 0.8121 | 19 of 169 | 115.6 / 22.2 |
| error | the engine's alternative | 94 | 166 | 0.9293 | 0.8067 | 8 of 169 | 115.2 / 10.3 |
| impasse | as written | 33 | 88 | 0.7435 | 0.8687 | 20 of 35 | 703.2 / 378.5 |
| impasse | discounted | 33 | 76 | 0.7297 | 0.8687 | 20 of 35 | 555.4 / 378.5 |
| impasse | the engine's alternative | 30 | 70 | 0.8305 | 0.8667 | 14 of 35 | 555.3 / 290.5 |

- **On the error arm's points the proposer points better than the ranking under
  every reading**, by 0.06 to 0.12.
- **In the impasse arm the ranking points better under every reading.**
- **Sections 1 to 3 read as written.** Their story holds on the other two
  readings. The missing pairs that decide no point go from 147 to 158 against
  the engine's alternative.

### The expectation

| clause | what it says | as written | discounted | the engine's alternative |
|---|---|---|---|---|
| D1 | fewer than half of the error arm's missing pairs have point verdict `b` | holds, 19/169 | holds, 19/169 | holds, 8/169 |
| D2 | the point verdict reads at least 0.90 by older rule, error arm | holds, 0.9422 | **fails**, 0.8683 | holds, 0.9293 |
| D3 | on the point verdicts the ranking reads below in the error arm and above in the impasse arm | holds | holds | holds |
| D4 | third rules govern a higher median share of the missing pairs, error arm | holds, 1 against 1/2 | the same | the same |
| D5 | a reversal changes fewer points on average among the missing pairs, error arm | holds, 22.2 against 292.6 | holds | holds |

**The drafter expected all five to hold, and trusted D2 least, then D3.** As
written, all five held. The cycle's points had not been foreseen. With them, D2
falls on either side of its line depending on how a reversal the engine would
refuse is counted. The other four hold on every reading.

### What it says

- **In the error arm, direction and fill part over what `RL-e` counts.**
  - Most pairs it counts against the proposer decide nothing. Third rules
    govern their shared region, and reversing them changes no point the base
    decides.
  - Where an edge does decide points, its pair verdict and its point verdict
    nearly always agree. There the proposer pointed it right on 0.87 to 0.94 of
    the units, above the ranking on every reading.
  - The fill weighs points, so it reads the edges that decide them.
- **In the impasse arm they do not part.** Third rules govern little, the
  missing pairs cost points, and the ranking points the deciding edges better
  than the proposer on every reading. That matches the fill, where the ranking
  fills more.
- **`RL-e` and `RL-f` stand as signed.** They read every placed edge, as §0
  asked. What this adds is that, in the error arm, the edges they count against
  the proposer mostly decide nothing.
- **What it leaves.** Why so many of the error arm's edges sit on regions third
  rules govern is not read here. The placement round lists every rule of
  another queue the draft overlaps over the whole space, and asks for a side
  against each.

---

## Where the unplaced answers come from — POST-RUN

> **POST-RUN.** Asked for by Sergi on 2026-11-03, after the plan closed, and run
> the same day. Zero API calls. `reasoned_loop/unplaced.py` read every rule a
> placement round listed in two ways. By masks, it read the rule's relation to
> the draft over the space. By a codebook, it read what the placement call's
> reasoning says of it.
> - **The codebook was frozen on the first run of each arm**, i r1 and e r1,
>   and committed with the expectation before any reasoning of a second or
>   third run was read, as `186e96d`, which is `ad01f3a` on `main`. The
>   expectation is five clauses in the module's docstring. The drafter had read the development runs' reasoning around
>   every rule left out at their 24 unplaced escalations, and this record
>   whole.
> - **Five gates stood before any write.**
>   - The census is `score.json`'s and the loop's own.
>   - Every answer read kept the draft's rule.
>   - The codebook is the one committed, with the sets split by run.
>   - Every placement call read carries its reasoning, and its attempts ended
>     `stop`.
>   - Added after the first run: the record already on disk comes back.
> - **The module was extended after its first run, with no expectation**
>   (section 4, below), in `8c924f6`, which is `046f934` on `main`. The record
>   comes from the second run, which gave back every figure of the first. The
>   first run's record is in `6e5157e` on `main`.
>
> Not a signed row; no verdict moves. The record is
> [`unplaced.json`](unplaced.json). It reached `main` in pull request #192. Its
> `_env` names the branch commit it was written from, `8c924f6`, with a clean
> tree. That commit and `046f934` have the same subject, the same tree and the
> same `git patch-id --stable`, and the GitHub API names #192 behind the `main`
> commit. Its code digest, `a7947cd502a024e6`, is the one `main` computes at
> `046f934`.

**Two texts the proposer reads disagree.**
- **The system prompt**, level 3's: *"Si tu regla es un caso particular de
  otra, no declares nada: el nivel 1 ya lo resuelve."*
- **The placement message**, v2b's: *"Situala frente a cada una de la
  lista."*
- **The list** is `O`, every rule of another queue that meets the draft over the
  space. So it holds rules nested with the draft, which subsumption already
  orders.

The validator requires a side against every rule of `O`. A rule left without one
leaves the answer unplaced, and the rule is not born. **What a side against a
rule inside the draft or containing it would add**, by `rung2/engine2.py`'s
`try_edge`:
- With the narrower rule on top, the edge is accepted as redundant and enters
  nothing.
- With the narrower rule below, it is refused as contradicting subsumption.

**What the codes are.**
- `nested`: the reasoning says the rule is nested.
- `apart`: it says the two do not overlap, or the rule does not apply.
- *Never named*: its identifier appears nowhere in the reasoning.

They are read on the sentences that name a rule and on the one after. Every
count of a code is approximate, so what is read is the rules left out against
the rules placed.

### 1. What is left out, by masks

Each listed rule's relation to the draft over the space, with the rules left
out among those listed:

| relation | development | held-out | all runs |
|---|---|---|---|
| nested: inside the draft | 6 of 35 | 99 of 171 | 105 of 206, 0.5097 |
| nested: containing the draft | 30 of 69 | 80 of 245 | 110 of 314, 0.3503 |
| nested: equal to the draft | 0 of 8 | 0 of 28 | 0 of 36 |
| crossing | 56 of 1,023 | 98 of 1,846 | 154 of 2,869, 0.0537 |

- **A nested rule is left out about seven times as often as a crossing one**,
  0.3867 against 0.0537 over every run. On the held-out runs it is 0.4032
  against 0.0531.
- **A rule equal to the draft is never left out.**
- **The impasse arm left out few rules of either relation**: 3 of 15 nested and
  14 of 180 crossing, at 8 unplaced escalations.

### 2. What the reasoning says of the rules it left out

| cause | development | held-out |
|---|---|---|
| nested, and said nested | 34 | 124 |
| nested, not said | 2 | 55 |
| crossing, said apart | 27 | 27 |
| crossing, said nested | 11 | 6 |
| crossing, never named | 6 | 2 |
| crossing, named with neither claim | 12 | 63 |
| rules left out | 92 | 277 |

**Saying apart, among crossing rules:**

| set | left out | placed |
|---|---|---|
| development | 27 of 56 | 53 of 967 |
| held-out | 27 of 98 | 127 of 1,748 |

- **In the development runs the reasoning names nearly every rule it leaves
  out, and says why.** Nested ones it calls nested, in the system prompt's
  words. On i r1's case 42: *"R0006 es un subconjunto de nuestra regla ... la
  regla más contenida (R0006) debería ganar. No necesitamos declarar nada."*
  Crossing ones it mostly calls apart, or takes for nested.
- **On the held-out runs the claims about single rules thin out.** 55 nested
  rules left out go unsaid, 51 of them never named, and 63 crossing ones are
  named with neither claim. Section 4 says where they are.
- **The codebook errs both ways.** *"Tampoco nuestra regla está contenida en
  R0001"* reads as nested, because its negation begins 27 characters before
  the term, past the 25 the codebook reads. The comparison with the rules placed
  is what carries the reading.

### 3. The expectation

| clause | what it says | held-out | verdict |
|---|---|---|---|
| U1 | a nested rule is left out at least four times as often as a crossing one | 0.4032 against 0.0531 | **holds** |
| U2 | at least three quarters of the missing nested rules are said nested | 124 of 179, 0.6927 | **fails** |
| U3 | at least half of the missing crossing rules are said apart or nested | 33 of 98, 0.3367 | **fails** |
| U4 | among crossing rules, saying apart is at least four times as frequent among the missing as among the placed | 0.2755 against 0.0727, 3.79 times | **fails** |
| U5 | at least half of e r3's unplaced escalations left out a rule whose region is the whole space | 32 of 38, 0.8421 | **holds** |

**The drafter expected all five to hold, and trusted U2 most and U5 least.**
The two that read structure held, and the three that read what the reasoning
says of single rules failed. U2, the clause trusted most, was among them.

### 4. Each unplaced escalation by what it left out — added after the first run

**Three of e r2's escalations left out 82 of the held-out runs' 277 missing
rules.** The clauses count rules, so these three weigh what 82 small ones would.
- **Case 1033 drafted the catch-all**, `severity gte 1` → `T1_GENERAL`.
  - Every one of the 52 rules listed lies inside it, and the answer placed none
    of them.
  - Its note: *"Catch-all rule covering all tickets. All overlapping rules are
    more specific subsets and automatically win via level 1 containment, so no
    explicit priority declarations are needed."*
  - The reasoning speaks of the list as a whole, and names 50 of the 52 rules
    nowhere.
- **Cases 954 and 1850 placed only the rules nested with their draft.** They
  left out 17 and 13 crossing rules.
  - 1850's reasoning: *"The instruction says 'Situala frente a cada una de la
    lista' but in practice we only put in beats/loses_to those that have the
    relationship."*
  - 954's: *"we must only list those where our rule is an exception (i.e., our
    condition is a subset of the other's)"*.
  - The placement message defines `beats` as an exception and `loses_to` as a
    general case. These answers read both as containment, so a crossing rule
    has no side.

Read once per escalation, by the relations of what each left out and of what it
placed, reading no text:

| what the escalation left out | development | held-out | all runs |
|---|---|---|---|
| only rules nested with the draft | 14 | 42 | 56 |
| only crossing rules, placing only nested ones | 2 | 4 | 6 |
| every listed rule, all of them crossing | 1 | 5 | 6 |
| only crossing rules, beside crossing ones placed | 2 | 11 | 13 |
| rules of both relations | 5 | 9 | 14 |
| unplaced escalations | 24 | 71 | 95 |

- **Counted once per escalation, the two sets agree.** 14 of 24 and 42 of 71
  left out only nested rules. Every rule left out has a stated cause at 17 of
  24 and 50 of 71 (the first run's readings).
- **The error arm carries the nested ones**: 55 of its 87 unplaced
  escalations.
- **The impasse arm's 8 are different.** 5 of them left out every listed rule,
  all of them crossing, and 1 left out only nested ones.

### 5. e r3's count is its default

- **e r3 wrote `severity gte 1` → `T1_GENERAL` at case 1.** Every later draft
  of another queue lies inside it, so it was listed at every one of e r3's 38
  unplaced escalations. It was left out at 32 of them (U5).
- **So the default accounts for most of e r3's unplaced escalations**, 38 of
  its 102, the most of any run (Stage C).
- **e r2 drafted the same catch-all at case 1033** (section 4). By then 52 rules
  of other queues stood in its base, it left out all of them, and the catch-all
  was not born.

### What it says

- **Most unplaced answers come from the protocol's two texts.**
  - The system prompt tells the proposer not to declare against a rule nested
    with its own, because subsumption orders it.
  - The placement round lists such rules and asks for a side against each.
  - With reasoning on, the proposer follows the system prompt. 56 of the 95
    unplaced escalations left out only nested rules, and a nested rule was left
    out seven times as often as a crossing one.
- **A second reading of the same texts places only the nested rules**, taking
  `beats` and `loses_to` for containment. By structure, 12 escalations left out
  only crossing rules while placing only nested ones or nothing.
- **A side against a rule inside the draft or containing it changes nothing
  the engine orders.** Leaving it out costs the birth. The rule is refused
  whole, its placements against crossing rules with it. Under the error
  trigger, a later ticket the base still decides wrongly escalates again
  (Stage C).
- **The codebook's claims about single rules did not carry to the held-out
  runs.** There the largest escalations spoke of the list as a whole, or
  applied a rule to it. The structure carried the reading.
- **What it leaves.**
  - Would a placement round that listed only crossing rules, or that asked for
    nested ones too, leave fewer answers unplaced, and change what the loop
    compiles? That is a change of protocol, calls, and a plan.
  - Why the proposer never leaves out a rule equal to its draft is not read
    here.

---

## Files

```
results_reasoned_loop/sample.json        Stage A: the checks, the transcriber under both triggers,
                                         the hidden policy through v1b's path, the H29 and rare
                                         tickets, the rules PLAN_REASONED_RULE.md's rule arms
                                         wrote, PLAN_MANUAL.md's level-3 runs, the schedule
results_reasoned_loop/loop_smoke.json    Stage B's smoke run: 30 cases under the error arm
results_reasoned_loop/loop_{e,i}_r{1,2,3}.json
                                         Stage B's six runs: the header, every rule in birth
                                         order, the edge log, every case's row with its cause,
                                         every escalation whole with its calls, attempts,
                                         seconds and reasoning, and rung 2's metrics
results_reasoned_loop/score.json         Stage C: the seven verdicts with their runs, and RL-h
results_reasoned_loop/decided.json       POST-RUN: each placed edge beside the points it decides,
                                         by run and arm, the expectation's five clauses, and the
                                         reading added after the first run
results_reasoned_loop/unplaced.json      POST-RUN: every rule a placement round listed, by its
                                         relation to the draft and by what the reasoning says of
                                         it, the codebook, the expectation's five clauses, and each
                                         unplaced escalation by what it left out
```

The smoke run's partial from before the first amendment,
`loop_smoke.before_amendment.partial.jsonl`, is kept outside git, as the
amendment says.
