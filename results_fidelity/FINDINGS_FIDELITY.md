# Would the model have decided as its rules do? — findings

Record opened on October 2, 2026, under [`PLAN_FIDELITY.md`](../PLAN_FIDELITY.md).
Sergi signed §0 on 2026-10-02, before any figure below existed: `ebe124d` on
`main`, merged from `4c81b17` in pull request #81. Every record names in its
`_env` the commit of the branch it was written on. A rebase merge gives those
commits new hashes on `main` with the same trees: Stage A's `3e6136f` is
`1b15ce1` there. **This record owns every figure in it.**

**Stage C adjudicated all five signed rows on 2026-10-04: four hold and one is
refuted.** `F-c` is the refutation, and it is thin.

- **The rules decide unlike the model would** (`F-b`).
- **Yet on the decisions they make, the model asked afresh is not right more
  often.** It gains where a rule was born wrong and loses where one was born
  right, and the two cancel.
- **Most of the silent error is the model's own** (`F-d`).
- **The rarest queue is one the model knows** (`F-e`). Without its screen of
  compiled rules, the model names it on every one of its tickets (`F-f`).

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Row `F-f` carries no band.
> Part of it reproduces figures the drafter computed with a scratch probe before
> drafting, which §0 of the plan declares as already seen. The rest, the two
> free baselines, is computable from data on disk. Those two were computed here
> for the first time, after the signature. Zero API calls.
>
> **PROVENANCE, STAGES B AND C: PRE-REGISTERED.** `F-a` to `F-e` were signed
> before any of their figures existed. `F-a` was read once, provisionally,
> after the births session and before any base session, as Stage B records.
> Stage C adjudicated it. `F-f`'s comparison on the same cases was added after
> Stage C first ran: POST-RUN, and reported only.

---

## Stage A — the checks, the draw and the free readout

**What was run.** `python3 -m fidelity.sample`, on 2026-10-02, with
`PYTHONHASHSEED=0`, from the package commit and a clean tree. It took about a
minute, almost all of it the test suite inside `F-g1`. The record is
[`sample.json`](sample.json). **Surface: the corpus.** That is
`generate_corpus(2000, seed=17)` in arrival order, the cases of
`PLAN_REUSE.md`'s three Stage B records. Nothing here is measured on the
exhaustive space.

**The blocking checks passed before anything was computed.**

- **`F-g1`.** The suite was green, 1,157 tests. Each Stage B record reproduces
  its own metrics, fire counts, births and corpus labels, under Stage B's model
  and reasoning setting.
- **`F-g2`.** Each run, rebuilt case by case from its record alone, reproduces
  every decision, every escalation's screen, every edge verdict and every final
  count. Its system prompt is v1's, byte for byte.
- **`F-g3`.** No B screen shows a rule that matches its ticket, or the deciding
  rule. Every B screen carries v1's coverage header, and every ticket-only
  prompt is the empty-base rendering. The draw, the census and the smoke run
  are as §2 and §8 sign them. That every birth prompt is the request rung 2's
  loop actually built is checked in `tests/test_fidelity.py` against the SDK
  double's replay of the four v1 n=100 records, and the suite ran it.
- **`F-g4`.** Signed.

### The draw and the sessions

| | run 1 | run 2 | run 3 | all |
|---|---|---|---|---|
| decided cases | 1,938 | 1,969 | 1,958 | 5,865 |
| drawn uniformly | 600 | 600 | 600 | 1,800 |
| rare-class decisions the draw missed, added as census | 11 | 17 | 13 | 41 |
| B prompts asked twice | 611 | 617 | 613 | 1,841 |
| silent errors in the draw, `F-d`'s population | 341 | 346 | 278 | 965 |
| `ONCALL_ESCALATION` decisions, `F-e`'s census | 7 | 7 | 7 | 21 |

The births session asks the 135 birth prompts twice. The ticket-only session
asks 301 distinct tickets once and the 27 rare-class tickets of the corpus a
second time. The smoke run asks five items of each arm once, one of them a
birth on a conflict screen. **That comes to 4,295 calls**, against about 4,300
in §1 of the plan. Every `F-d` population is above the 100 that §6 requires,
so `F-d` is adjudicable.

### The drafter's figures, measured

§0 of the plan lists figures from a scratch probe the drafter ran before
drafting. The plan says a figure that does not reproduce is an erratum to it,
not a silent edit. **All of them reproduce exactly but one.**

| figure in §0 | declared | measured |
|---|---|---|
| decided cases | 5,865 | 5,865 |
| design A: the deciding rule on the screen / first in it | 5,864 / 5,498 | 5,864 / 5,498 |
| design B′: another matching rule on the screen / one with the deciding action | 1,002 / 1,000 | 1,002 / 1,000 |
| design B: a shown rule with the deciding action / that action a plurality | 5,398 / 3,363 | 5,398 / 3,363 |
| design B: a shown rule's edges cite a hidden rule | 2,154 | 2,154 |
| coverage births: screens, answer shown, answer a plurality, right | 85, 73, 61, 48 | 85, 73, 61, 48 |
| conflict births: screens, answer shown, answer a plurality, right | 47, 47, 44, 20 | 47, 47, 44, 20 |
| births whose screen cites a rule not shown | 72 | 72 |
| **the replay without its edges: cases departing** | **74, 32, 122** | **37, 16, 61** |

**The last row is the drafter's error, and it halves exactly.** The probe
counted each departing case twice: once for the decision that departed, and once
for the birth the rebuild then failed to find there. The finding it stood for
holds: without the edges, every run's rebuild departs from its record, which is
what makes `F-g2` a check rather than a formality. §0 of the plan carries a
dated erratum.

The rest of §0's list reproduces as declared. The concentration of decisions
is 33, 26 and 31 deciding rules, of which 8, 5 and 6 decide half. The births
are crossed by outcome as `U-c` split them. In every run, the seven
`ONCALL_ESCALATION` tickets were decided four times by `R0001` and three times
by a rule sending one product at severity ≤ 3 to `T2_TECHNICAL`. No proposal
in any Stage B run, any of the four smoke runs or any of the eight August n=100
runs named `ONCALL_ESCALATION`. Rung 1's proposer named it 7 times, all on
free or pro tickets at severity 1 whose true queue is `T2_TECHNICAL`. One of
them is case 74, which Stage B's run 1 sent to `T2_TECHNICAL`. The median
prompt sizes and the pace of the earlier paid sessions reproduce too. All of
it is under `readout` in the record.

**One pace figure is now bounded, not quoted.** §1 of the plan gives Stage B's
run 1 about 29 s per call, from *about thirty minutes* in `FINDINGS_REUSE.md`.
The records' own timestamps bound it at 32.8 s per call or less, with that
run's suite taken out. Runs 2 and 3 come out at 8.0 and 8.8 s or less, which
is §1's *under about 9 s*.

### The two free baselines, measured for the first time

What a model that only copied its screen would score, on the 1,800 drawn
decisions, each B screen as the prompt would show it. *Plurality* is the
commonest action on the screen, a tie going to the action shown first. *First*
is the action of the rule shown first.

| | run 1 | run 2 | run 3 | all |
|---|---|---|---|---|
| the deciding rule right | 259 · 0.4317 | 254 · 0.4233 | 322 · 0.5367 | 835 · 0.4639 |
| plurality agrees with the rule | 406 · 0.6767 | 326 · 0.5433 | 273 · 0.4550 | 1,005 · 0.5583 |
| plurality right | 181 · 0.3017 | 221 · 0.3683 | 163 · 0.2717 | 565 · 0.3139 |
| first agrees with the rule | 129 · 0.2150 | 103 · 0.1717 | 343 · 0.5717 | 575 · 0.3194 |
| first right | 137 · 0.2283 | 207 · 0.3450 | 202 · 0.3367 | 546 · 0.3033 |

### What it says

**1. Copying the screen would lose capability, by about fifteen points.** In every
run, the screen's plurality is right less often than the rule that decided the
case: by 0.130, 0.055 and 0.265, and by 0.150 over all 1,800. So `F-c` cannot
hold for a model that answers from its screen. It holds only if the model reads
the ticket and the ticket beats the rule. At the births the proposer answered
with a plurality action on 61 of 85 coverage screens. These baselines say what
that habit costs if it carries over to the decided cases.

**2. Copying alone would put rule–model agreement at about 0.56.** That is how
often the plurality action is the deciding rule's. `F-b` compares the model's
agreement with the rule against its agreement with itself, not against this
figure. But a model whose `A` lands near 0.56 is answering much as a copier
would.

**3. The screens are what §2.1 said they would be.** Design A shows the answer
key on 5,864 of 5,865 decisions. Design B hides it without breaking v1's header.
Every one of the 1,841 B prompts in the sessions passed `F-g3`'s checks.

### What Stage A does not settle

- **Anything about the model's answers.** None has been asked for. The
  baselines describe a copier, not the model, and nothing here is a prediction
  of where `F-b` to `F-e` will land.
- **The pace of Stage B.** The earlier sessions disagree by a factor of four,
  and the smoke run will measure this one.

---

## Stage B

Sergi gave the go-ahead for the smoke session on 2026-10-02, and for nothing
beyond it. Each later session waits for its own go-ahead (§8).

**The smoke session passed and opens the others.** `fidelity.ask --session
smoke`, 2026-10-02, with `PYTHONHASHSEED=0`, from `4f4c16c` on `main` and a
clean tree. The checks of §8 ran in order before any call. The key was an API
key OpenRouter accepts, not a management key. `F-g1` to `F-g4` passed, with the
suite green at 1,157 tests. Stage A's record held the same draw, sessions and
prompts the checks rebuilt.

- **All 15 answers were valid** (5 birth prompts, 5 B prompts, 5 ticket-only
  prompts), and none failed.
- **Every call carried `reasoning: {"effort": "none"}`**, and so does the
  record.
- **The partial file was gone once the record was written.**

The record is [`ask_smoke.json`](ask_smoke.json). Its answers enter no row, and
none is read here.

**The pace is a fifth of what §1 planned on.** The calls took 2.33 s at the
median, from 1.50 to 5.44 s, and 38.8 s in all. That is 2.59 s on average,
against the 12.6 s §1 budgeted from the longest earlier session. At this pace
the five remaining sessions, 4,280 calls, take about three hours rather than
fifteen. Fifteen calls are few, and run 1 of `PLAN_REUSE.md` ran about four
times slower than runs 2 and 3 on the same day. So the planning figure stays
§1's, and this one is reported beside it.

**The births session: 268 answers of 270 valid.** Sergi gave the go-ahead for
this session alone. `fidelity.ask --session births`, 2026-10-02,
`PYTHONHASHSEED=0`, from `bc5d94f` and a clean tree. The smoke check, the key
check, `F-g1` to `F-g4` and the Stage A match all passed before any call. Each
of the 135 birth prompts was asked twice, in two passes. The record is
[`ask_births.json`](ask_births.json).

- **Both failures are one prompt**, `b1:598`, the birth at case 598 of run 1.
  In each pass it came back empty three times, retries included, about 44 s per
  pass. It is a conflict screen showing twelve rules, the most a screen shows.
  At birth, on 2026-09-30, the proposer answered it with 11 declared edges,
  where no other birth of the three runs has more than 7.
- **Why it came back empty is not known.** That its answer was by far the
  longest fits a reply cut by the 1,200-token cap. Checking it would cost calls
  outside the protocol, so it was not checked.
- **What §5.5 does with it.** The prompt leaves `F-a`'s denominator: 134 of the
  135 birth prompts have two valid answers. The breaker did not trip, and
  rightly: two failures a pass apart are not an outage.
- **The pace was 2.89 s per call at the median and 4.56 s on average**, pulled
  up by those two and a slower tail: 20.5 minutes of calls.

**`F-a`, read once the births were in, as §8 intends: provisional.** §8 runs
the births before the bases so that the instrument is measured before most of
the spend. So `F-a` was computed with Stage C's own function on this record,
before any base session ran:

- **The value.** `S − A = −0.0075`: the two fresh answers agree 0.9254 of the
  time, and a fresh answer agrees with the one recorded on 2026-09-30 0.9328 of
  the time. The standard error is 0.0191, over 134 prompts.
- **Per run**: −0.0246, −0.0161 and +0.0238.
- **Against the line.** At the signed line, ≤ 0.05, it would hold, and not
  thin.
- **Accuracy.** The fresh answers are right 0.5261 of the time, against 0.5000
  for the recorded ones on the same prompts.

**This is not the verdict.** Stage C adjudicates `F-a` with the other rows,
from this record, and owns the figure. It is written here because it was known
before the bases were asked, and the record should say what was known when.

**The base1 session: 1,214 answers of 1,222 valid, in two segments.** On Sergi's
go-ahead, `fidelity.ask --session base1`, 2026-10-02, `PYTHONHASHSEED=0`, from
`9ce7a69` and a clean tree. The record is [`ask_base1.json`](ask_base1.json).

- **The first segment was cut at 306 answers.** It ran as a background command,
  and the harness ends those after about 30 minutes. The partial file kept
  every answer (§5.8). Only the call in flight was lost; it was paid for and is
  in no record.
- **The second segment resumed in Sergi's terminal**, at 18:57:52Z, which the
  record keeps under `resumed_at`. No prompt was asked twice in a pass.
- **Two refused attempts came between them.** §8's key check refused a key twice,
  each time before any call. The shell's startup was replacing the key
  `CLAUDE.md` rule 7 documents with one OpenRouter rejects. Loading the key the
  way rule 7 documents fixed it.
- **The eight failures fall on seven items**, all in the uniform draw: `d1:171`
  failed in both passes. Each came back empty or cut off mid-JSON after three
  attempts.
- **That is the symptom the reasoning setting cured on 2026-09-30**, then at 5
  of 15 calls and here at 8 of 1,222. Why these eight is not known: the record
  does not keep `finish_reason`.
- **Run 1's value is defined.** 7 of the 600 drawn items lack a valid pair,
  0.0117, under §5.5's 0.05.
- **The pace by the wall clock: about 119 minutes of calling**, 5.9 s per
  answer. Over the same spans the per-call timer adds up to about 5% more than
  the wall clock does, and why is not known; its median is 4.09 s.

**The base2 session: 1,234 answers of 1,234 valid.** On Sergi's go-ahead,
`fidelity.ask --session base2`, 2026-10-02, `PYTHONHASHSEED=0`, run in Sergi's
terminal from `7b627a8` and a clean tree, in one segment. The checks of §8
passed before any call. The record is [`ask_base2.json`](ask_base2.json).

- **No call failed.** Every one of the 617 items has two valid answers: the 600
  drawn and 17 rare-class decisions the draw missed.
- **The pace by the wall clock: 118.7 minutes of calling**, 5.8 s per answer.
  The per-call timer adds up to about 8% more over the same span, the gap
  `base1` showed; its median is 4.88 s.

**The base3 session: 1,223 answers of 1,226 valid.** On Sergi's go-ahead,
`fidelity.ask --session base3`, 2026-10-03, `PYTHONHASHSEED=0`, run in Sergi's
terminal from `bed22d3` and a clean tree, in one segment. The checks of §8
passed before any call. The record is [`ask_base3.json`](ask_base3.json).

- **Three failures on two items**, both in the uniform draw, each coming back
  empty after three attempts: `d3:297` in both passes and `d3:74` in the
  second.
- **Run 3's value is defined.** 2 of the 600 drawn items lack a valid pair,
  0.0033.
- **The pace by the wall clock: 91.8 minutes of calling**, 4.5 s per answer.
  The per-call timer adds up to about 7% more; its median is 3.56 s.

**The ticket-only session: 328 answers of 328 valid.** On Sergi's go-ahead,
`fidelity.ask --session ticket_only`, 2026-10-03, `PYTHONHASHSEED=0`, run in
Sergi's terminal from `30bb483` and a clean tree, in one segment. The checks of
§8 passed before any call. The record is
[`ask_ticket_only.json`](ask_ticket_only.json).

- **What was asked.** The 301 distinct tickets once, and the 27 rare-class
  tickets a second time, exactly as Stage A planned them.
- **No call failed.**
- **The pace by the wall clock: 20.8 minutes**, 3.8 s per answer.
- **A second launch of the same session spent nothing.** Once this record
  existed, `harness/record_guard.py` refused that launch before the client was
  built.

**Stage B is complete: 4,295 calls, 4,282 answers valid.** The 13 failures are
listed by session above: 2 in the births session, 8 in `base1` and 3 in
`base3`. Each of the three bases has a defined value under §5.5, and `F-a` has
two valid answers on 134 of its 135 prompts.

---

## Stage C — the five adjudications

**What was run.** `python3 -m fidelity.score`, on 2026-10-04, with
`PYTHONHASHSEED=0`, from `43c4065` and a clean tree. Every blocking check passed
first, and every Stage B record carried this plan's protocol and Stage A's
digest. The record is [`score.json`](score.json).

**Stage C ran twice, and the second run is the record.** Its first run, from
`75aa22f`, was never committed. Its F-f block compared the ticket-only arm's
accuracy, over a subsample, with the B arm's over all 600 drawn decisions.
`43c4065` added the comparison on the same cases (POST-RUN, reported only).
The second run reproduced the first's verdicts, per-run values and births
block exactly.

**Surface: the corpus.** That is the decided cases and births of
`PLAN_REUSE.md`'s three Stage B runs, seed 17, in arrival order. `F-b` to `F-e`
are read on the median of the three runs, and `F-a` pooled over the births.

| row | statistic | run 1 | run 2 | run 3 | value | band | verdict |
|---|---|---|---|---|---|---|---|
| `F-a` | `S − A` against the answer of 2026-09-30, births | −0.0246 | −0.0161 | +0.0238 | **−0.0075** (se 0.0191, n 134) | ≤ 0.05 | **holds** |
| `F-b` | `S − A` against the deciding rule | 0.1838 | 0.2642 | 0.1388 | **0.1838** (se 0.0163) | ≥ 0.10 | **holds** |
| `F-c` | the model's accuracy minus the rule's | −0.0126 | +0.0383 | −0.0460 | **−0.0126** (se 0.0162) | > 0 | **refuted, thin** |
| `F-d` | on the rule's errors, the share the model is wrong too | 0.7955 | 0.7413 | 0.8791 | **0.7955** (se 0.0177) | ≥ 0.60 | **holds** |
| `F-e` | `ONCALL_ESCALATION` tickets named so by both answers, of 7 | 3 | 0 | 2 | **2** | ≥ 1 | **holds** |

**The drafter expected all five to hold, and got four.** It trusted `F-d` least,
then `F-e`, then `F-c`. `F-c` is the refutation, and it lands within one
standard error of its line, as §0 labels in advance. `F-d` held well above the
line the drafter expected it to sit on. `F-e` held at the count of one or two
the drafter expected.

### What the verdicts say

**1. The instrument had not moved.** `F-a` holds. Re-asked their birth prompts,
the model agrees with its answers of 2026-09-30 (0.9328) as often as with itself
(0.9254). The fresh answers are right 0.5261 of the time, the recorded ones
0.5000. So whatever separates the model from its rules below, it is not a
different model.

**2. Compiled rules decide unlike the model would.** `F-b` holds in every run.
Asked twice, the model agrees with itself 0.8921, 0.9083 and 0.9498 of the time.
It agrees with the rule that decided the case 0.7083, 0.6442 and 0.8110 of the
time. If a rule were just one more draw of the model, those two would match.
Instead about one decision in five goes to a queue the model, asked afresh,
would not choose.

**3. But compiling does not lose capability on the decisions it makes.** `F-c`
is refuted, thinly. Asked afresh, the model is right 0.4224, 0.4617 and 0.4908
of the time, where the rules are right 0.4351, 0.4233 and 0.5368. It does better
in run 2 alone. The disagreement of point 2 is real; it is not a loss.

**The two pulls of §0 are both there, and they cancel.**

| | run 1 | run 2 | run 3 |
|---|---|---|---|
| rules born wrong: the model minus the rule | +0.0142 | +0.1377 | +0.0343 |
| rules born right: the model minus the rule | −0.0436 | −0.0403 | −0.0973 |

On decisions by rules born wrong, the model asked afresh would do better:
compiling froze a bad answer. On decisions by rules born right it would do
worse: the rule holds a right answer the model does not reliably give again.

**4. Most of the silent error is the model's own, more than the proxy said.**
`F-d` holds at 0.7955. On the cases a rule decided wrongly, the model asked
afresh is wrong too about four times in five. Mostly it is wrong the same way:
it repeats the rule's own wrong queue on 476 of 670, 398 of 692 and 450 of 554
answers.

`U-c`'s split by birth put three silent errors in five on the rules born wrong,
and read the rest as scope errors the model would not make. **The direct
measure says the rest are mostly the model's too.** On the errors of rules born
right, the model is wrong 0.8661, 0.6558 and 0.8596 of the time. Case by case,
the split by birth and the fresh answer agree on whose error it was 0.5507,
0.6171 and 0.5830 of the time. **As a proxy for the error being the model's own,
the split by birth undercounts it, and case by case it is little better than a
coin.**

**5. The rarest queue is in the model, and the screen can talk it out of it.**
`F-e` holds at a median of 2. Under design B, both answers name
`ONCALL_ESCALATION` on 3, 0 and 2 of the seven tickets. Without a screen (`F-f`,
below), they name it on all seven, 14 answers of 14. So the queue `U-d` found
the loop never asked about is one the model knows. In run 2's base, the compiled
rules on its screen talked it out of the queue every time.

### Recorded beside the rows, and never in a denominator

- **The infidelity sits in a few rules.** These are figures for rules with at
  least 20 sampled decisions.
  - `R0001` (*enterprise, any severity → `T1_GENERAL`*, born at case 0 in every
    run): the model agrees with it on 0.00, 0.00 and 0.03 of its decisions. Its
    accuracy minus the rule's is −0.10, +0.20 and +0.24.
  - The rules sending tickets to `SELF_SERVICE_DEFLECT` draw agreement from 0.00
    to 0.12. Run 3's `R0015` is right on all 22 sampled decisions where the
    model, asked afresh, is right on none.
  - The `T2_TECHNICAL` rules mostly draw agreement of 0.8 to 1.0 and an accuracy
    difference near zero. Run 2's `R0011` is the exception: agreement 0.30, the
    model 0.44 ahead.
- **Disagreement is no alarm.** Where a fresh answer disagrees with the rule,
  the rule is wrong 0.5607, 0.6885 and 0.4602 of the time. Where it agrees, it is
  wrong 0.5667, 0.5149 and 0.4639 of the time. Only run 2 shows any signal, so
  re-asking the model would not have found the rules' errors in the other two.
- **`SECURITY_INCIDENT`, in counts.** Run 2's rules decided 11 of the class's 17
  cases wrongly. Asked afresh under B, the model named `SECURITY_INCIDENT` on 21
  of those 22 answers: rung 1's *compilation destroyed capability*
  ([`PREDICTION.md`](../PREDICTION.md)), seen again in one base of three. In
  runs 1 and 3 every compiled decision on the class was right. There the model
  named the class on 10 of 10 answers and on 28 of 36.
- **`F-f`, the model without its screen.** On the same 300 drawn decisions, one
  answer from each arm:

  | | run 1 | run 2 | run 3 | all |
  |---|---|---|---|---|
  | ticket only (no screen) | 0.52 | 0.51 | 0.54 | **0.5233** |
  | design B (the screen) | 0.39 | 0.48 | 0.51 | **0.4600** |
  | the deciding rule | 0.34 | 0.39 | 0.55 | **0.4267** |

  - **Without its screen the model does better in every run.** By 0.06 pooled
    it beats itself with the screen, and by 0.10 it beats the rules.
  - **Each figure is 100 cases with one answer per arm.** This record computes
    no standard error for them, so they are a sign in a consistent direction,
    not a measured effect.
  - **The rare classes, without the screen.** On all 27 rare-class tickets it
    names the true queue in every answer: `SECURITY_INCIDENT` 40 of 40 and
    `ONCALL_ESCALATION` 14 of 14.
  - **Beside the copier.** Stage A's copier answering its screen's plurality is
    right 0.3017, 0.3683 and 0.2717 of the time, and the model under B 0.4224,
    0.4617 and 0.4908. So the model under B reads more than its screen. But the
    screen still costs it, and nothing in §0 measured that.
- **The run itself.**
  - **Failures:** 13 of 4,295 calls, none an outage.
  - **Written rules that would validate:** 1,198, 1,214 and 1,223 of the 1,222,
    1,234 and 1,226 calls of the three base sessions.
  - **Median seconds per call by the timer:** births 2.89, the bases 4.09, 4.88
    and 3.56, ticket only 3.17.

### What Stage C does not settle

- **Why the screen costs the model.** The B screen shows the nearest compiled
  rules, and the model answers from it more than it should (§5.2). Whether any
  context would do the same, or only a screen of compiled rules, is not
  measured. Nor is whether the cost would survive more than one answer per
  ticket.
- **Whether the gains and losses of point 3 cancel elsewhere.** They cancel
  here, over one corpus and three bases of one model.
- **Why thirteen calls came back empty or cut off.** The records keep no
  `finish_reason`.
- **A trigger.** Point 5 says the rarest queue was in the model. The alarm above
  says disagreement with a fresh answer would not have found the rules' errors.
  A trigger that asks about a class before a rule swallows it is still another
  plan.

---

## Files

```
results_fidelity/sample.json   Stage A, F-f's free half: the checks, the draw,
                               the sessions with every prompt's digest, the readout
results_fidelity/ask_smoke.json   Stage B, the smoke session: 15 of 15 valid;
                               it opens the other sessions and enters no row
results_fidelity/ask_births.json  Stage B, the births session: 268 of 270 valid,
                               the two failures one prompt; F-a's record
results_fidelity/ask_base1.json   Stage B, base 1: 1,214 of 1,222 valid, in two
                               segments, resumed once
results_fidelity/ask_base2.json   Stage B, base 2: 1,234 of 1,234 valid
results_fidelity/ask_base3.json   Stage B, base 3: 1,223 of 1,226 valid
results_fidelity/ask_ticket_only.json   Stage B, the ticket-only arm: 328 of 328
                               valid; F-f's paid half
results_fidelity/score.json    Stage C: F-a to F-e, per run and on the median,
                               and everything recorded beside them
fidelity/plan.py               the gate and §10's constants; §0's five lines
fidelity/replay.py             a Stage B record rebuilt case by case; F-g2
fidelity/prompts.py            the three prompts, built with rung 2's functions
fidelity/sample.py             Stage A
fidelity/ask.py                Stage B, the one that spends
fidelity/score.py              Stage C
```
