# The rule written with reasoning on — findings

Record opened on October 25, 2026, under
[`PLAN_REASONED_RULE.md`](../PLAN_REASONED_RULE.md). The plan, its package,
Sergi's signature and every record below are on the branch of pull request
#178, which is open as this is written. Sergi signed §0 on 2026-10-25, before
any figure below existed, in a commit of its own: `bfd69f5` on that branch.

Every record names in its `_env` the commit it was written from. All five were
written on the branch of #178. The rebase merge will give each of those commits
a new hash on `main`, and a commit after the merge names them.

| record | written from, on the branch of #178 |
|---|---|
| `sample.json` | `bfd69f5`, the signature |
| `ask_smoke.json` | `0a8eb2e`, Stage A's commit |
| `ask_pass1.json` | `e2b812e`, the smoke run's commit |
| `ask_pass2.json` | `37a89e1`, pass 1's commit |
| `score.json` | `931927f`, pass 2's commit |

All five carry one code digest, `7f577a9c4b826525`, with `code_dirty` and
`git_dirty` false. **This record owns every figure in it.**

**All three stages ran on 2026-10-25, and the four rows are adjudicated:
`RR-a`, `RR-b` and `RR-c` hold; `RR-d` is refuted, thinly.**

- **With reasoning on, the model asked for a rule chooses the right queue on
  0.9672 of level 3's escalated decisions**, against 0.7219 with reasoning off.
  That is 157 more right answers of 640, nine tenths of the 178 the rule arm
  gets wrong.
- **Asked for the queue alone with reasoning on, it is right on every
  decision again**, as it was for `PLAN_FIRST_MATCH.md`.
- **So asking for a rule still costs the queue a little with reasoning on**:
  21 answers of 640, against the plain question's none. With reasoning off it
  cost 13 of 640 today. Reasoning did not shrink that cost, and the difference
  lies inside its noise.
- **With reasoning on, the rule the model writes is the governing rule.** On 250
  of its 342 answers the rule's region over the space is the region of the
  listed rule that governs the ticket, against 165 with reasoning off. Read
  alone, as first rules of an empty base, its rules give their queue to about
  three tenths of the points they cover.

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Its references were
> computed after the signature. Zero API calls.
>
> **PROVENANCE, STAGES B AND C: PRE-REGISTERED.** `RR-a` to `RR-d` were signed
> before any of their figures existed, and none of their bands was set on a
> development set.

**Surface: the corpus.** Every figure is about tickets of
`generate_corpus(2000, seed=17)` that escalated in one of `PLAN_MANUAL.md`'s
three level-3 loop runs. The population is the escalations, not the arrivals
(§5.4 of the plan). **The one exception is the reading of the rules written**,
which reads each rule's region over the exhaustive space of 134,400 points, and
says so where it does.

---

## Stage A — the checks, the design and the references

**What was run.** `python3 -m reasoned_rule.sample`, on 2026-10-25, with
`PYTHONHASHSEED=0`, from the signing commit on a clean tree. The record is
[`sample.json`](sample.json).

**The blocking checks passed before anything was written.**
- **`RR-g1`.** The suite was green. `PLAN_FIRST_MATCH.md`'s own `FM-g1` to
  `FM-g3` passed, and they call `PLAN_QUEUE_ALONE.md`'s, which hold the 29 rules
  to the truth of all 790 escalations. Its design is its Stage A's, and its six
  verdicts come back from its two passes. The list's first match, read from
  level 3's text, gives every one of the 134,400 points of the space the queue
  the policy gives it.
- **`RR-g2`.** The rule arm's 171 prompts carry the digests
  `PLAN_QUEUE_ALONE.md` recorded for its rule arm at level 3, and the plain
  arm's the digests it recorded for its plain arm, which `PLAN_FIRST_MATCH.md`
  recorded for its plain and reasoning arms too. Each reasoning arm's texts are
  its quiet arm's. 684 prompts carry 342 distinct texts, one digest each.
- **`RR-g3`.** The population and the schedule are §0's and §1's.
- **`RR-g4`.** Signed.

**Every count §0 lists as computed while drafting comes back**, so §0 needs no
erratum: 684 prompts, 171 an arm, on level 3's 320 decisions, each decision
served once in each arm, on 170 tickets.

**The references.** They adjudicate nothing.
- **The rules each decision's ticket matches, in the list's order, and its
  runner-up.** On 224 of the 320 decisions the runner-up is the second matching
  rule, and on 50 no lower match gives another queue, as
  `PLAN_FIRST_MATCH.md`'s Stage A found.
- **`PLAN_QUEUE_ALONE.md`'s rule-arm answers on the 171 rule prompts**: 342,
  every one valid and served by Baidu.

---

## Stage B — the calls

**Every call ran at `deepseek/deepseek-v4-flash`, pinned to Baidu with
fallbacks off**, behind the signature, the key check, `RR-g1` to `RR-g3` and
Stage A's record each time. Every call went through the package's asker, which
is `PLAN_FIRST_MATCH.md`'s with this plan's settings in its request.
- **The rule and plain arms** ran with reasoning `{"effort": "none"}` and 1,200
  tokens.
- **The reasoning rule and reasoning arms** ran with reasoning
  `{"effort": "high"}` and 16,000 tokens.

**The smoke run**, [`ask_smoke.json`](ask_smoke.json), asked two prompts of
each arm on 2026-10-25 between 15:29:22 and 15:30:18 UTC.
- All eight answers were valid on their first attempt, and every attempt was
  served by Baidu and ended `stop`.
- The rule and plain arms did not reason. The rule arm's completions ran 127
  and 130 tokens.
- The reasoning arm reasoned 150 and 216 tokens. The reasoning rule arm
  reasoned 1,540 and 2,501, and took 17.3 and 25.6 seconds.

**Pass 1**, [`ask_pass1.json`](ask_pass1.json), was run by Sergi in his
terminal on 2026-10-25 between 15:41:29 and 17:27:59 UTC, without a resume.
**Pass 2**, [`ask_pass2.json`](ask_pass2.json), followed between 17:45:10 and
19:30:37 UTC, without a resume.
- **All 1,368 asks, 684 a pass, were answered validly on their first
  attempt.** No call failed and no parse failed.
- **The pin held.** Every attempt of both passes was served by Baidu, and every
  one ended `stop`.
- **The rule and plain arms did not reason.** The rule arm's completions ran a
  median of 133 tokens in both passes.
- **The reasoning arm reasoned on every ask**: 57 to 1,064 tokens in pass 1,
  with a median of 314, and 55 to 922 in pass 2, with a median of 304.
- **The reasoning rule arm reasoned on every ask**: 400 to 9,883 tokens in pass
  1, with a median of 2,126, and 390 to 11,430 in pass 2, with a median of
  2,288. Its longest answer took 11,585 of its 16,000 tokens. Every one of its
  answers wrote `action` first.
- **The response carried the reasoning every time** it reasoned, and the record
  keeps it whole. No stage codes it.

**§0's retry was never exercised.** A failed call would have been retried with
the same messages, and only a failed parse with v1's message. In 1,376 calls
neither happened.

**What it cost, and how far §1 was.**
- **The money.** The two passes sent 2.07 million prompt tokens and received
  1.19 million completion tokens, 1.09 million of them reasoning. At the price
  Baidu's listing gave on 2026-10-25 that is just under ten cents: the edge of
  §1's *under ten at any length the drafter expects*.
- **The time.** §1 priced a pass at about an hour, at fifteen seconds a
  reasoning rule ask. The smoke run's pace pointed to about 80 minutes. Each
  pass took 106.5 and 105.5 minutes, and the reasoning rule arm took 85.5 and
  84.3 of them, at 22.74 and 24.72 seconds an ask at the median.

---

## Stage C — the four adjudications

**What was run.** `python3 -m reasoned_rule.score`, on 2026-10-25, with
`PYTHONHASHSEED=0`, from pass 2's commit on a clean tree. `RR-g1` to `RR-g4`
passed again, with the suite green. The record is [`score.json`](score.json).

**Every statistic is a fraction of counts, compared with its line exactly.**
The record keeps each as a fraction beside its float. The standard errors are
clustered by ticket. **Every row reads all 320 decisions, and `RR-a` all 171
rule prompts**: no answer was invalid.

| row | statistic | line | reading | read | verdict |
|---|---|---|---|---|---|
| RR-a | over the rule prompts, `S − A` | ≤ 0.05 | **+0.0175**, from **0.9006** and **0.8830** (se 0.0203) | 171 of 171 prompts | **holds** |
| RR-b | at `L₃`, `acc_w − acc_t` | > 0 | **+0.2453**, from **0.9672** and **0.7219** (se 0.0353) | 320 of 320 | **holds** |
| RR-c | at `L₃`, `acc_w` | ≥ 0.90 | **0.9672** (se 0.0096) | 320 of 320 | **holds** |
| RR-d | at `L₃`, `(acc_r − acc_w) − (acc_q − acc_t)` | < 0 | **+0.0125**, from **0.0328** with reasoning and **0.0203** without (se 0.0413) | 320 of 320 | **refuted, thin** |

`RR-e` is reported, and everything below that is not in the table is its.

**`RR-d` is thin, and only `RR-d`.** Its value lies within one standard error
of its line, and dropping run L3r3 would put it on the other side. Its three
runs read +0.0118, −0.0222 and +0.0600. `RR-b`'s read +0.2412, +0.2741 and
+0.2100, and `RR-c`'s 0.9706, 0.9593 and 0.9750.

**`RR-d` had a value.** §0 gives it none if asking for a rule costs the queue
nothing with reasoning off. Today it cost 0.0203, so the row was read.

**The drafter expected all four rows to hold.** Three did. `RR-d`, which the
drafter trusted least, was refuted, thinly. That is a fact about this plan,
and the scoreboard counts it. The drafter's guess for the reasoning rule arm
was 0.97, and it landed on 0.9672.

### The four arms, at level 3

| | right, on the 320 decisions | |
|---|---|---|
| the rule arm | 0.7219 | asked for a rule, reasoning off |
| the reasoning rule arm | 0.9672 | asked for a rule, reasoning on |
| the plain arm | 0.7422 | asked for the queue alone, reasoning off |
| the reasoning arm | 1.0000 | asked for the queue alone, reasoning on |
| compiled once | 1.0000 | `G-a` |

- **Reasoning carries into the rule-writing prompt** (`RR-b` and `RR-c`
  hold). The reasoning rule arm is right on 619 of its 640 answers, the rule
  arm on 462. The 157 more right answers are nine tenths of the 178 the rule
  arm gets wrong.
- **Asking for a rule still costs a little with reasoning on.** The reasoning
  arm is right on all 640 of its answers, so the 21 answers the reasoning rule
  arm gets wrong are the rule-writing prompt's, 0.0328.
- **With reasoning off it cost less than it did on 2026-10-24.** Today's plain
  arm stands 0.0203 above today's rule arm. `PLAN_QUEUE_ALONE.md` measured
  +0.0849 (`QA-b`). The plain arm is where it was, and the rule arm is higher
  (below). So `RR-d` compares two costs of a few points each, and finds the
  one with reasoning no smaller (`RR-d` refuted, thin).
- **Read by ticket**, with each of the 170 tickets counted once however often
  the loop escalated it, the arms are right on 0.7029, 0.9559, 0.7529 and
  1.0000.

### Beside the closed plans, on the same decisions

| arm | then | today |
|---|---|---|
| the rule arm, `PLAN_QUEUE_ALONE.md`'s, 2026-10-24 | 0.6859 | 0.7219 |
| the plain arm, `PLAN_FIRST_MATCH.md`'s, earlier on 2026-10-25 | 0.7422 | 0.7422 |
| the reasoning arm, `PLAN_FIRST_MATCH.md`'s, earlier on 2026-10-25 | 1.0000 | 1.0000 |

- **The rule arm agrees with its answers of 2026-10-24 about as often as it
  agrees with itself** (`RR-a` holds), and it is right more often today: 0.7219
  against 0.6859. `RR-a` reads agreement, not accuracy, and says the instrument
  is the same one. The rise is reported, and it is why today's cost without
  reasoning is a quarter of `QA-b`'s.
- **The reasoning arm is right on every decision again**, a few hours after
  `PLAN_FIRST_MATCH.md`'s `FM-e`.

### What each arm gets wrong

Every answer at level 3, classified against the 29 rules as
`PLAN_QUEUE_ALONE.md` §5.6 defines it:

| arm | answers | first | order | matching |
|---|---|---|---|---|
| the rule arm | 640 | 462 | 119 | 59 |
| the reasoning rule arm | 640 | 619 | 20 | 1 |
| the plain arm | 640 | 475 | 159 | 6 |
| the reasoning arm | 640 | 640 | 0 | 0 |

The order errors, by where they go:

| arm | order errors | the second matching rule's queue | the runner-up's | the catch-all's | the most specific rule's |
|---|---|---|---|---|---|
| the rule arm | 119 | 111 | 113 | 18 | 27 |
| the reasoning rule arm | 20 | 18 | 20 | 1 | 10 |
| the plain arm | 159 | 153 | 153 | 5 | 32 |

- **Reasoning removes both kinds of error from the rule arm**: its matching
  errors fall from 59 to 1, and its order errors from 119 to 20.
- **What is left is the list's order, as before.** Every one of the reasoning
  rule arm's 20 order errors names the runner-up's queue.
- **The plain arm's errors go where they went**: 153 of its 159 order errors
  name the runner-up's queue, as `PLAN_QUEUE_ALONE.md`'s and
  `PLAN_FIRST_MATCH.md`'s plain arms did.

Right answers, by the rule that governs the ticket, where the arms part:

| governing rule | what it says | rule | reasoning rule | plain | reasoning |
|---|---|---|---|---|---|
| `H02` | the keyword and severity ≤ 2 → `SECURITY_INCIDENT` | 19 of 36 | 36 of 36 | 0 of 36 | 36 of 36 |
| `H15` | api and severity ≤ 2 → `T3_ENGINEERING` | 24 of 36 | 36 of 36 | 24 of 36 | 36 of 36 |
| `H17` | integrations and severity ≤ 2 → `T3_ENGINEERING` | 7 of 28 | 28 of 28 | 15 of 28 | 28 of 28 |
| `H16` | api → `T2_TECHNICAL` | 57 of 68 | 66 of 68 | 48 of 68 | 68 of 68 |
| `H18` | integrations → `T2_TECHNICAL` | 45 of 68 | 60 of 68 | 31 of 68 | 68 of 68 |
| `H12` | billing → `SELF_SERVICE_DEFLECT` | 13 of 30 | 28 of 30 | 30 of 30 | 30 of 30 |
| `H24` | free tier and severity ≥ 3 → `SELF_SERVICE_DEFLECT` | 18 of 30 | 30 of 30 | 29 of 30 | 30 of 30 |
| `H26` | severity 4 and no prior ticket → `SELF_SERVICE_DEFLECT` | 10 of 16 | 13 of 16 | 13 of 16 | 16 of 16 |
| `H23` | phone, off hours, not enterprise → `T1_GENERAL` | 6 of 6 | 3 of 6 | 0 of 6 | 6 of 6 |
| `H29` | the catch-all → `T1_GENERAL` | 15 of 54 | 53 of 54 | 48 of 54 | 54 of 54 |

- **The reasoning rule arm's 21 wrong answers lie under eight governing
  rules**: eight under `H18`, three under `H23`, three under `H26`, and one or
  two under each of five others.
- **The rule arm without reasoning loses most under the catch-all and
  `H12`**, where it is right on 15 of 54 answers and 13 of 30, and the plain
  arm on 48 and 30.

### The rarest queues

Counts of right answers, two per decision:

| queue | decisions | rule | reasoning rule | plain | reasoning |
|---|---|---|---|---|---|
| `ONCALL_ESCALATION` | 9 | 18 of 18 | 18 of 18 | 18 of 18 | 18 of 18 |
| `SECURITY_INCIDENT` | 28 | 39 of 56 | 55 of 56 | 20 of 56 | 56 of 56 |
| `ACCOUNT_MANAGER` | 28 | 47 of 56 | 56 of 56 | 33 of 56 | 56 of 56 |
| `T3_ENGINEERING` | 36 | 36 of 72 | 72 of 72 | 41 of 72 | 72 of 72 |

**With reasoning on, the rule-writer names every rare queue wherever the list
gives it but one answer**, a `SECURITY_INCIDENT` ticket under `H01`.

### The rules the rule arms write

Every valid answer of the two rule arms on every rule prompt, 171 prompts in
each pass, read by `reasoned_rule/shape.py`. **The regions are over the
exhaustive space**, and each rule is read alone, as the first rule of an empty
base, which is what v1 tells the model it is (§5.10 of the plan).

| | the rule arm, reasoning off | the reasoning rule arm |
|---|---|---|
| answers read | 342 | 342 |
| rules that validate under rung 2's validator | 342 | 342 |
| rules that match their ticket | 303 | 342 |
| one condition, two, three or more | 83, 230, 29 | 113, 181, 48 |
| points of the space a rule covers, at the median | 16,800 | 16,800 |
| rules whose region is a listed rule's | 244 | 257 |
| … the listed rule that governs the ticket | 165 | 250 |
| share of the covered points the list's first match gives the rule's queue, pooled | 0.2827 | 0.3048 |
| rules right on every point they cover | 30 | 42 |
| answers declaring `beats` or `loses_to` | 0 | 43, every one citing the list's identifiers |

- **With reasoning on, the model transcribes the governing rule.** On 250 of
  342 answers the rule's region is exactly the region of the listed rule that
  governs the ticket. With reasoning off it does so on 165, and on 39 answers
  it writes a rule its own ticket does not match, which v1 forbids.
- **Read alone, a listed rule's region is broader than what the list gives
  it.** The rules above it take part of its points. So the reasoning rule arm's
  rules, read alone over the space, give their queue to about three tenths of
  the points they cover. A rule written as a listed rule's region decides the
  rest as the list would only beneath the rules above it.
- **Its edges cite the list.** 43 answers declare an edge, and every one names
  an identifier of the manual, `H01` to `H29`, which no base holds. Nothing here
  tries them.

These readings adjudicate nothing, and a narrower rule is right on its region
more easily: each share is read beside its points.

### Agreement

Read over decisions, a prompt's two answers agree 0.9062 of the time in the
rule arm, 0.9406 in the reasoning rule arm, 0.9406 in the plain arm and 1.0000
in the reasoning arm. The reasoning rule arm answers like the reasoning arm
0.9672 of the time, and the rule arm like the plain arm 0.7469.

### What the verdicts say

- **Reasoning carries into the queue a rule-writer chooses.** Asked for a rule
  under v1's impasse framing, with the 29 rules in its prompt and no screen,
  the model is right on 0.9672 of level 3's escalated decisions with reasoning
  on, against 0.7219 with it off (`RR-b` and `RR-c` hold). The plan's third
  candidate, a framing that turns reasoning against the list, can account at
  most for the 21 answers the reasoning rule arm gets wrong, and nothing here
  says what turned those.
- **Asking for a rule costs a few points with reasoning on**, 0.0328 against
  the plain question with reasoning. **Reasoning did not make that cost smaller
  than it is without** (`RR-d` refuted, thin): both are a few points today, and
  the difference lies inside its noise.
- **What the rule-writer writes, with reasoning, is the list.** On nearly three
  answers in four its rule covers exactly the region of the rule that governs
  the ticket, and every rule it writes matches its ticket. Read alone over the
  space, its rules give their queue to about three tenths of the points they
  cover.
- **Read with the threads before it.** The loop's proposer has written rules
  with reasoning off since `PLAN_REUSE.md` §1's amendment of 2026-09-30, and
  `PLAN_MANUAL.md`'s loops ran so. That amendment turned reasoning off to keep
  the instrument August measured and because reasoning spent the answer's
  1,200 tokens. Here the rule-writing prompt with reasoning took a median of
  about 2,200 reasoning tokens a call, and up to 11,430.

### What Stage C does not settle

1. **The loop with reasoning on.** What it compiles is not read here. A loop
   whose proposer transcribes the governing rule would need the rules above it
   placed above it, which rung 2's engine gives through containment and
   declared edges. Containment covers an exception nested in its general rule,
   such as `H15` in `H16`; it does not cover rules that cross, such as the
   keyword's and a product's. The edges the reasoning rule arm declares name
   the manual's identifiers, which no base holds, and `PLAN_MANUAL.md`'s engine
   dropped every such declaration. That is a run, under the budget this plan
   measured, and a plan of its own.
2. **Where the reasoning rule arm's 21 errors come from.** Its reasoning is
   recorded whole on every ask and coded by no stage. A reading would need a
   codebook frozen on part of it before the rest is read.
3. **Which part of the rule-writing prompt costs under reasoning**, the impasse
   framing or the apparatus. The impasse arm was not asked with reasoning
   (§12 of the plan).
4. **Why the rule arm without reasoning was right more often today** than on
   2026-10-24, on the same prompts and the same provider.
5. **The screen with reasoning, the naming question with reasoning, and the
   other levels.** None was asked.
6. **One model, one provider, one manual, one effort, two passes, one day.**

---

## Files

```
results_reasoned_rule/sample.json     Stage A: the checks, the design with every prompt and the
                                      decisions it serves, the sessions' orders, the system
                                      prompts, each arm's settings, the references
results_reasoned_rule/ask_smoke.json  Stage B's smoke: two asks of each arm
results_reasoned_rule/ask_pass1.json  Stage B's pass 1: 684 asks, every attempt with its provider,
                                      finish reasons and tokens, every answer whole with its keys
                                      in order, the rules written, and both reasoning arms'
                                      reasoning
results_reasoned_rule/ask_pass2.json  Stage B's pass 2: the same asks in another order
results_reasoned_rule/score.json      Stage C: the four verdicts with their parts, errors and runs,
                                      and RR-e
```
