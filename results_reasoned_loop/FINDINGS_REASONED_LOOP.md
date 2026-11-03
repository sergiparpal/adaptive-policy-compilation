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
3. **Where the unplaced answers come from.** 95 of 408 escalations ended
   unplaced, 38 in e r3. The reasoning is recorded whole on every attempt, and
   coded by no stage.
4. **A trigger that reads no truth.** The error arm reads the label of every
   arrival, as no deployment could (§13).
5. **Reasoning in the loop apart from v1b.** No reasoning-off arm ran under
   v1b. The level-3 loop beside the impasse arm crosses dates and protocols
   (§13).
6. **The arrivals' order.** One corpus, in which the default arrives second.
7. **One model, one provider, one manual, one effort, three runs an arm.**

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
```

The smoke run's partial from before the first amendment,
`loop_smoke.before_amendment.partial.jsonl`, is kept outside git, as the
amendment says.
