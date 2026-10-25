# The first match — findings

Record opened on October 25, 2026, under
[`PLAN_FIRST_MATCH.md`](../PLAN_FIRST_MATCH.md). The plan, its package,
Sergi's signature and every record below reached `main` together in pull
request #176, merged on 2026-10-25. Sergi signed §0 on 2026-10-25, before any
figure below existed, in a commit of its own: `ba64894` on `main`.

Every record names in its `_env` the commit it was written from. All five were
written on the branch of #176, and the rebase merge gave each of those commits
a new hash on `main`. Each pair has the same subject, the same tree and the
same `git patch-id --stable`, and the GitHub API names #176 behind every `main`
commit.

| record | written from, on the branch of #176 | the same commit on `main` |
|---|---|---|
| `sample.json` | `e405c35`, the signature | `ba64894` |
| `ask_smoke.json` | `80e45f9`, Stage A's commit | `8ee89c4` |
| `ask_pass1.json` | `36aefe5`, the smoke run's commit | `e9d249c` |
| `ask_pass2.json` | `698a99a`, pass 1's commit | `5b86558` |
| `score.json` | `ea24ef2`, pass 2's commit | `371084b` |

All five carry one code digest, `d9ea475aeac77bf4`, with `code_dirty` and
`git_dirty` false, and it is the one `main` computes after the merge. **This
record owns every figure in it.**

**All three stages ran on 2026-10-25, and the six rows are adjudicated:
`FM-a`, `FM-c`, `FM-d`, `FM-e` and `FM-f` hold; `FM-b` is refuted. No row is
thin.**

- **With reasoning on, the model applies the 29 rules on every one of level 3's
  escalated decisions.** All 640 of its answers are right, in every run and in
  both passes.
- **Asked plainly without reasoning, it is right on 0.7422 of them**, and
  asked to name the rule that applies before the queue, on 0.6078.
- **Where the naming arm gives a lower rule's queue, it names a lower rule**: 107
  of its 113 order errors that name a rule. It never names the first rule and
  writes another queue. On all 640 of its answers its queue is the queue of the
  rule it names.
- **What naming costs is a new error.** On 168 answers it names a rule the
  ticket does not match, `H26` on 88 and `H27` on 57, and writes that rule's
  queue.

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Its references were
> computed after the signature, for the first time. Zero API calls.
>
> **PROVENANCE, STAGES B AND C: PRE-REGISTERED.** `FM-a` to `FM-f` were signed
> before any of their figures existed, and none of their bands was set on a
> development set.

**Surface: the corpus.** Every figure is about tickets of
`generate_corpus(2000, seed=17)` that escalated in one of `PLAN_MANUAL.md`'s
three level-3 loop runs. The population is the escalations, not the arrivals
(§5.4 of the plan).

---

## Stage A — the checks, the design and the references

**What was run.** `python3 -m first_match.sample`, on 2026-10-25, with
`PYTHONHASHSEED=0`, from the signing commit on a clean tree. The record is
[`sample.json`](sample.json).

**The blocking checks passed before anything was written.**
- **`FM-g1`.** The suite was green. `PLAN_QUEUE_ALONE.md`'s own `QA-g1` to
  `QA-g3` passed, and they hold the 29 rules to the truth of all 790
  escalations. Its design is its Stage A's, and its six verdicts and its
  POST-RUN order reading come back from its two passes.
- **`FM-g2`.** The plain arm's 171 prompts carry the digests
  `PLAN_QUEUE_ALONE.md` recorded for its plain arm at level 3. The reasoning
  arm's texts are the plain arm's, and the naming arm adds §5.1's line and
  nothing else. 513 prompts carry 342 distinct texts, one digest each.
- **`FM-g3`.** The population and the schedule are §0's and §1's.
- **`FM-g4`.** Signed.

**Every count §0 lists as computed while drafting comes back**, so §0 needs no
erratum: 513 prompts, 171 an arm, on level 3's 320 decisions, each decision
served once in each arm.

**The 320 decisions lie on 170 tickets.** The 171st prompt, ticket 0's, serves
none. Ticket 0 is the first arrival of every run, and it escalated before any
rule existed, so it never had a screen. `FM-a`, which reads prompts, reads it.

**The references.** They adjudicate nothing.
- **The rules each decision's ticket matches, in the list's order, and its
  runner-up.** On 224 of the 320 decisions the runner-up is the second matching
  rule. On 50 no lower match gives another queue, the complement of the 270
  `PLAN_QUEUE_ALONE.md`'s Stage A published.
- **`PLAN_QUEUE_ALONE.md`'s plain answers on the 171 prompts**: 341 valid,
  every one served by Baidu, and the one ask that plan lost to rate limits.

---

## Stage B — the calls

**Every call ran at `deepseek/deepseek-v4-flash`, pinned to Baidu with
fallbacks off**, behind the signature, the key check, `FM-g1` to `FM-g3` and
Stage A's record each time. Every call went through the package's asker.
- **The plain and naming arms** ran with reasoning `{"effort": "none"}` and
  1,200 tokens, as `PLAN_QUEUE_ALONE.md`'s plain arm did.
- **The reasoning arm** ran with reasoning `{"effort": "high"}` and 16,000
  tokens.

**The smoke run**, [`ask_smoke.json`](ask_smoke.json), asked two prompts of
each arm on 2026-10-25 between 11:36:50 and 11:37:07 UTC.
- All six answers were valid on their first attempt, and every attempt was
  served by Baidu and ended `stop`.
- The plain and naming arms did not reason. Their completions ran 15 and 22
  to 23 tokens, and both naming answers wrote `rule` before `action` and named
  a rule.
- The reasoning arm reasoned 217 and 1,037 tokens, and the response carried
  the reasoning both times.

**Pass 1**, [`ask_pass1.json`](ask_pass1.json), was run by Sergi in his
terminal on 2026-10-25 between 12:00:51 and 12:18:21 UTC, without a resume.
**Pass 2**, [`ask_pass2.json`](ask_pass2.json), followed between 12:31:35 and
12:47:45 UTC, without a resume.
- **All 1,026 asks, 513 a pass, were answered validly on their first
  attempt.** No call failed and no parse failed.
- **The pin held.** Every attempt of both passes was served by Baidu, and every
  one ended `stop`.
- **The plain and naming arms did not reason.** All 342 naming answers wrote
  `rule` before `action`, and every one named one of the 29 identifiers.
- **The reasoning arm reasoned on every ask**: 45 to 1,061 tokens in pass 1,
  with a median of 349, and 49 to 855 in pass 2, with a median of 322. No
  answer came near its 16,000. The response carried the reasoning every time,
  and the record keeps it whole. No stage codes it.
- **A reasoning ask took 3.97 seconds at the median in pass 1 and 3.7 in pass
  2**, and 10.82 at the most. A plain or naming ask took about a second.

**§0's retry was never exercised.** A failed call would have been retried with
the same messages, and only a failed parse with v1's message. In 1,032 calls
neither happened. So no answer here was given with v1's retry message in the
conversation.

**What it cost.** The two passes sent 1.31 million prompt tokens and received
0.13 million completion tokens, 113,463 of them reasoning. At the price
Baidu's listing gave on 2026-10-25 that is about four cents. Each pass took 16
to 17.5 minutes. §1 had priced the reasoning arm at about 85 minutes a pass,
for want of any recorded call that reasoned.

---

## Stage C — the six adjudications

**What was run.** `python3 -m first_match.score`, on 2026-10-25, with
`PYTHONHASHSEED=0`, from pass 2's commit on a clean tree. `FM-g1` to `FM-g4`
passed again, with the suite green. The record is [`score.json`](score.json).

**Every statistic is a fraction of counts, compared with its line exactly.**
The record keeps each as a fraction beside its float. The standard errors are
clustered by ticket. **Every row reads all 320 decisions**: no answer was
invalid.

| row | statistic | line | reading | read | verdict |
|---|---|---|---|---|---|
| FM-a | over the plain prompts, `S − A` | ≤ 0.05 | **−0.0117**, from **0.9181** and **0.9298** (se 0.0160) | 171 of 171 prompts | **holds** |
| FM-b | at `L₃`, `acc_n − acc_q` | > 0 | **−0.1344**, from **0.6078** and **0.7422** (se 0.0413) | 320 of 320 | **refuted** |
| FM-c | over the naming arm's order errors that name a rule, the share naming a lower match | ≥ 1/2 | **0.9469**, **107** of **113** (se 0.0283) | 320 of 320 | **holds** |
| FM-d | at `L₃`, `acc_r − acc_q` | > 0 | **+0.2578**, from **1.0000** and **0.7422** (se 0.0358) | 320 of 320 | **holds** |
| FM-e | at `L₃`, `acc_r` | ≥ 0.90 | **1.0000** (se 0) | 320 of 320 | **holds** |
| FM-f | at `L₃`, `acc_r − acc_n` | > 0 | **+0.3922**, from **1.0000** and **0.6078** (se 0.0399) | 320 of 320 | **holds** |

`FM-g` is reported, and everything below that is not in the table is its.

**No row is thin.** No value lies within one standard error of its line, and
no run's decisions, dropped, would put one on the other side. `FM-b`'s three
runs read −0.1176, −0.1741 and −0.0950. `FM-d`'s read +0.2529, +0.2556 and
+0.2650. `FM-e` reads 1 in each.

**The drafter expected all six rows to hold.** Five did. `FM-b`, which the
drafter trusted least, was refuted, by more than three standard errors. That
is a fact about this plan, and the scoreboard counts it.

### The three arms, at level 3

| | right, on the 320 decisions | |
|---|---|---|
| the plain arm | 0.7422 | the queue alone, reasoning off |
| the naming arm | 0.6078 | the rule that applies, then its queue, reasoning off |
| the reasoning arm | 1.0000 | the plain arm's prompt, reasoning on |
| compiled once | 1.0000 | `G-a` |

- **Reasoning applies the list exactly.** The reasoning arm is right on all 640
  of its answers. Its two answers to each prompt agree on every one, so the
  passes did not part either.
- **Without reasoning, today's plain arm stands for `PLAN_QUEUE_ALONE.md`'s**
  (`FM-a` holds). Its two answers to one prompt agree 0.9181 of the time, and
  0.9298 with that plan's. On the 318 decisions that plan's rows read, it was
  right on 0.7689 on 2026-10-24 and is right on 0.7406 today.
- **Naming the rule first costs 0.1344**, every run agreeing on the sign
  (`FM-b` refuted). It is about a seventh of the decisions.
- **Read by ticket**, with each of the 170 tickets counted once however often
  the loop escalated it, the arms are right on 0.7471, 0.6147 and 1.0000.

### What the naming arm names

The naming arm's 640 answers, by the class of the rule each names and by the
class of its queue:

| its queue is | the first rule | a lower match | a rule the ticket does not match | answers |
|---|---|---|---|---|
| the first rule's, the truth | 343 | 22 | 24 | 389 |
| a lower match's, an order error | 0 | 107 | 6 | 113 |
| no matching rule's | 0 | 0 | 138 | 138 |
| all | 343 | 129 | 168 | 640 |

- **The queue follows the name.** On all 640 answers the queue is the queue of
  the rule named. Every answer names one of the 29 identifiers.
- **The order errors are of finding, not of naming** (`FM-c` holds). On 107 of
  its 113 order errors the naming arm names the lower rule whose queue it
  writes, and on none the first rule. It believes a lower rule applies.
- **A lower name is mostly the next matching rule**: 103 of 129.
- **The new error is a rule the ticket does not match.** On 168 answers, a
  quarter, the arm names a rule whose conditions the ticket fails. On 138 of
  them that rule's queue is no matching rule's, which is why the arm's matching
  errors rise from the plain arm's 8 to 138.
  - **Two rules carry it.** The arm names `H26`, *severity eq 4 AND
    prior_tickets_30d eq 0* to `SELF_SERVICE_DEFLECT`, on 88 such answers. It
    names `H27`, *severity lte 2* to `T2_TECHNICAL`, on 57.
  - **`H27` is named where it cannot hold.** It is named 41 times on tickets the
    catch-all governs. `H27` matches every ticket of severity 1 or 2, and it
    stands above the catch-all, so every such ticket has severity 3 or 4. On
    those tickets the arm never names `H29`, and is right on none of their 54
    answers.
  - **Which condition of `H26` the tickets fail is not read.** The arm names it
    27 times where `H18` governs, 19 where `H28` does and 18 where `H16` does.

**On the plain arm's order errors, the same ticket in the same pass.** Of the
plain arm's 157 order errors, the naming arm names:
- on 85, the lower rule whose queue the plain arm gave;
- on 43, the first rule, and is right;
- on 5, another lower match;
- on 24, a rule the ticket does not match.

**Where naming helps and where it costs**, in right answers by the rule that
governs the ticket:

| governing rule | what it says | plain | naming | reasoning |
|---|---|---|---|---|
| `H02` | the keyword and severity ≤ 2 → `SECURITY_INCIDENT` | 4 of 36 | 10 of 36 | 36 of 36 |
| `H15` | api and severity ≤ 2 → `T3_ENGINEERING` | 24 of 36 | 36 of 36 | 36 of 36 |
| `H17` | integrations and severity ≤ 2 → `T3_ENGINEERING` | 12 of 28 | 23 of 28 | 28 of 28 |
| `H16` | api → `T2_TECHNICAL` | 49 of 68 | 29 of 68 | 68 of 68 |
| `H18` | integrations → `T2_TECHNICAL` | 31 of 68 | 6 of 68 | 68 of 68 |
| `H28` | business or enterprise → `T1_GENERAL` | 46 of 46 | 24 of 46 | 46 of 46 |
| `H29` | the catch-all → `T1_GENERAL` | 46 of 54 | 0 of 54 | 54 of 54 |

- **Naming finds two of the three exceptions** that sit above their general
  rule: `H15` whole, and most of `H17`. `H02`, the keyword at low severity,
  stays mostly lost.
- **It costs on the general rules and the defaults**: `H16`, `H18`, `H28` and
  the catch-all, where the unmatched names fall.

### Where the plain arm's errors go, today

Today's plain arm, in `PLAN_QUEUE_ALONE.md` §5.6's classes: 475 first, 157
order and 8 matching, of 640 answers.
- **The order errors are the next rule again.** 152 of the 157 name the queue
  of the second rule the ticket matches, which is the runner-up on all 152.
  The other 5 name the third's. Six follow the catch-all, and 31 the more
  specific rule.
- **The same rules carry them.** `H18`, `H02` and `H16` carry 88 of the 157:
  37 order errors on `H18`'s 68 answers, 32 on `H02`'s 36 and 19 on `H16`'s
  68.

So the reading `PLAN_QUEUE_ALONE.md` made POST-RUN comes back on today's plain
arm, asked a day later.

### The rarest queues

Counts of right answers, two per decision:

| queue | decisions | plain | naming | reasoning |
|---|---|---|---|---|
| `ONCALL_ESCALATION` | 9 | 18 of 18 | 18 of 18 | 18 of 18 |
| `SECURITY_INCIDENT` | 28 | 24 of 56 | 30 of 56 | 56 of 56 |
| `ACCOUNT_MANAGER` | 28 | 33 of 56 | 34 of 56 | 56 of 56 |
| `T3_ENGINEERING` | 36 | 38 of 72 | 61 of 72 | 72 of 72 |

- **With reasoning, every rare queue is named wherever the list gives it.**
  `SECURITY_INCIDENT`, which the plain arm loses at `H02`, is right on all 56
  answers.
- **Naming lifts `T3_ENGINEERING`**, through `H15` and `H17`.

### Agreement

Read over decisions, a prompt's two answers agree 0.9313 of the time in the
plain arm, 0.8938 in the naming arm and 1.0000 in the reasoning arm. The plain
and naming arms answer alike 0.6992 of the time.

### What the verdicts say

- **Without reasoning, the model does not find the first match.** Made to name
  the rule it applies, it names a lower one and writes that rule's queue
  (`FM-c` holds). The order errors are a belief about which rule applies, not
  a slip from the rule it found to another queue.
- **Naming the rule is not a step of deliberation.** The identifier is chosen
  as loosely as the queue was, and the queue follows it. It finds two of the
  three exceptions, and it names rules the ticket does not match on a quarter
  of its answers, so on balance it costs (`FM-b` refuted).
- **With reasoning on, the model applies the 29 rules exactly** on every
  escalated decision of level 3 (`FM-e` holds), with about 330 reasoning
  tokens an ask. So what the plain question leaves wrong is what this model
  does with a 29-rule first-match list when it does not reason (`FM-d` and
  `FM-f` hold).
- **Read with the threads before it.** The proposer's calls have had reasoning
  off since `PLAN_REUSE.md` §1's amendment of 2026-09-30, which turned it off
  because it spent the answer's 1,200 tokens. `PLAN_MANUAL.md`'s loop runs,
  `PLAN_APPLY.md` and `PLAN_QUEUE_ALONE.md` were all asked with it off. Their
  figures stand as figures of the model with reasoning off. That is the setting
  under which the loop did not apply what it was told.

### What Stage C does not settle

1. **Why the model, without reasoning, names rules the ticket does not match.**
   `H26` and `H27` carry most of it. Which of their conditions the model
   misreads is in no record, and the reasoning arm makes no such error.
2. **The naming question with reasoning on**, the fourth cell (§12 of the plan,
   first item).
3. **What the reasoning says.** It is recorded whole on all 342 reasoning asks
   and coded by no stage. A reading of it would need a codebook frozen before
   the held-out reasoning is read.
4. **The loop with reasoning on.** The loop's proposer writes rules with
   reasoning off and 1,200 tokens. Whether reasoning carries into the
   rule-writing prompt, and into what the loop compiles, is a new run under a
   larger budget, and a plan.
5. **The other levels.** Nothing here asks the prose or the names with
   reasoning, so `QA-f`'s control was not run for reasoning (§2.3 of the plan).
6. **One model, one provider, one manual, one effort, two passes, one day.**

---

## Files

```
results_first_match/sample.json     Stage A: the checks, the design with every prompt and the
                                    decisions it serves, the sessions' orders, the system
                                    prompts, each arm's settings, the references
results_first_match/ask_smoke.json  Stage B's smoke: two asks of each arm
results_first_match/ask_pass1.json  Stage B's pass 1: 513 asks, every attempt with its provider,
                                    finish reasons and tokens, every answer whole with its keys
                                    in order, and the reasoning arm's reasoning
results_first_match/ask_pass2.json  Stage B's pass 2: the same asks in another order
results_first_match/score.json      Stage C: the six verdicts with their parts, errors and runs,
                                    and FM-g
```
