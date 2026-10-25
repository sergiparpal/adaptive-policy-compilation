# The queue asked alone — findings

Record opened on October 24, 2026, under
[`PLAN_QUEUE_ALONE.md`](../PLAN_QUEUE_ALONE.md). The plan and its package
reached `main` in pull request #169. Sergi signed §0 on 2026-10-24, before any
figure below existed, in a commit of its own: `a1c18d5` on `main`, merged with
Stage A and the smoke run in pull request #170.

Every record names in its `_env` the commit it was written from. Three were
written from `main` itself, so their hashes need no translation. Stage A's
record and the smoke run's were written on the branch of #170, from the
signature's commit and from Stage A's. The rebase merge gave each of those
commits a new hash on `main`. Each pair has the same subject, the same tree and
the same `git patch-id --stable`, and the GitHub API names #170 behind both
`main` commits.

| record | written from | the same commit on `main` | reached `main` in |
|---|---|---|---|
| `sample.json` | `e320147`, the signature, on the branch | `a1c18d5` | #170 |
| `ask_smoke.json` | `544738f`, Stage A's commit, on the branch | `e3780dc` | #170 |
| `ask_pass1.json` | `6b1e54d`, the smoke run's commit | `6b1e54d` | #171 |
| `ask_pass2.json` | `c295ab0`, pass 1's commit | `c295ab0` | #172 |
| `score.json` | `1b07dc5`, pass 2's commit | `1b07dc5` | the pull request of this record |

All five carry one code digest, `6d3a44106cf8b106`, with `code_dirty` and
`git_dirty` false. **This record owns every figure in it.**

**All three stages ran on 2026-10-24, and the six rows are adjudicated:
`QA-a`, `QA-b` and `QA-f` hold; `QA-c`, `QA-d` and `QA-e` are refuted, `QA-d`
thinly.**

- **Asked for the queue alone, with the 29 rules in its prompt, the model is
  right on 0.7689 of level 3's escalated decisions**, against 0.6840 when it is
  asked for a rule.
- **That recovers about a quarter of what the rule arm gets wrong**, and leaves
  one decision in four wrong. Asked plainly, the model does not apply the list
  as exactly as it transcribes it.
- **The gain splits about evenly** between the impasse framing and the
  rule-writing apparatus.
- **With the names alone the plain question loses**, so what it buys at level 3
  is the list's.
- **Read beside the verdicts**, asked for the queue alone the model almost
  always names the queue of a rule the ticket matches. What it misses is the
  order of the list.

**[NOTE 2026-10-25] Read POST-RUN, the order errors are the next rule.** On
134 of the plain arm's 141 they name the queue of the second rule the ticket
matches. They are neither the default nor the more specific rule. See *Where
the order errors go*, below.

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Its counts were computed
> while drafting, and §0 declared them. Its reference columns were computed
> after the signature, for the first time. Zero API calls.
>
> **PROVENANCE, STAGES B AND C: PRE-REGISTERED.** `QA-a` to `QA-f` were signed
> before any of their figures existed, and none of their bands was set on a
> development set.

**Surface: the corpus.** Every figure is about tickets of
`generate_corpus(2000, seed=17)` that escalated in one of `PLAN_MANUAL.md`'s
twelve loop runs. The population is the escalations, not the arrivals (§5.4 of
the plan).

---

## Stage A — the checks, the design and the references

**What was run.** `python3 -m queue_alone.sample`, on 2026-10-24, with
`PYTHONHASHSEED=0`, from the signing commit on a clean tree. The record is
[`sample.json`](sample.json).

**The blocking checks passed before anything was written.**
- **`QA-g1`.** The suite was green. `PLAN_APPLY.md`'s own `X-g1` to `X-g3`
  passed, its design is its Stage A's, and its six verdicts come back from its
  two passes. The 29 rules, read from level 3's frozen text by first match,
  give all 790 escalations the truth their loop records hold.
- **`QA-g2`.** The rule arm's 676 prompts carry the digests `PLAN_APPLY.md`
  recorded. The plain and impasse arms differ as §5.1 says, and 2,028 prompts
  carry 2,028 digests.
- **`QA-g3`.** The populations and the schedule are §0's and §1's.
- **`QA-g4`.** Signed.

**Every count §0 lists as computed while drafting comes back**, so §0 needs no
erratum.
- 676 prompts an arm: 275, 81, 149 and 171 by level.
- 778 decisions: 116, 100, 242 and 320.
- What parts the arms, which `QA-g2` reads off the texts.

**The reference columns, at level 3.** They adjudicate nothing.
- **A decision's ticket matches between 1 and 9 of the 29 rules**, most often
  3, which 89 of the 320 do.
- **On 270 of the 320 a lower match gives another queue**, so the list's order
  decides them.
- **Two copiers, scored on the truth.**
  - One answers the queue of the matching rule with the most conditions, which
    is how rung 1's engine arbitrated. It is right on 279 of 320, 0.8719.
  - One answers the commonest queue among the matching rules. It is right on
    170, 0.5313.
- **`PLAN_APPLY.md`'s answers in §5.6's classes**, 640 an arm at level 3:

| arm of `PLAN_APPLY.md` | first | order | matching |
|---|---|---|---|
| the ticket arm, which is this plan's rule arm | 450 | 135 | 55 |
| the screen arm | 378 | 193 | 69 |

---

## Stage B — the calls

**Every call ran with reasoning off, at `deepseek/deepseek-v4-flash`, pinned to
Baidu with fallbacks off**, behind the signature, the key check, `QA-g1` to
`QA-g3` and Stage A's record each time.
- The rule arm went through the proposer `manual.run.build_proposer(level)`
  builds, with the pin wrapped around its client.
- The impasse and plain arms went through the package's asker.

**The smoke run**, [`ask_smoke.json`](ask_smoke.json), asked one prompt of each
arm at each level, on 2026-10-24 between 13:53:46 and 13:54:01 UTC.
- All twelve answers were valid on their first attempt, and every attempt was
  served by Baidu.
- Every attempt ended `stop`, and none reasoned.
- The rule arm's completions ran 109 to 154 tokens. The impasse and plain arms'
  ran 14 to 16, and carried `action` alone.

**Pass 1**, [`ask_pass1.json`](ask_pass1.json), was run by Sergi in his
terminal on 2026-10-24 between 14:23:20 and 15:15:50 UTC, without a resume.
- **All 2,028 asks, and 2,027 answers valid.**
- **Seven attempts failed with OpenRouter's 429**: the model *"is temporarily
  rate-limited upstream"*.
  - `q:L3:567` lost all three of its attempts and is recorded as failed. It
    serves two decisions at level 3.
  - Three asks were answered on a later attempt.

**Pass 2**, [`ask_pass2.json`](ask_pass2.json), was run by Sergi in his
terminal on 2026-10-24 between 15:54:56 and 16:44:53 UTC, without a resume.
- **All 2,028 asks, and 2,027 answers valid.**
- **Nine attempts failed with the same 429.**
  - `i:L2:1491` lost all three and serves one decision at level 2, which no
    adjudicated row reads.
  - Five asks were answered on a later attempt.

**The pin held.** Every answer of both passes was served by Baidu, and no
attempt went to another provider. A rate-limited attempt failed rather than
moving, as fallbacks off makes it.

**Eight answers were given with v1's JSON retry message in the
conversation.** v1's loop retries any failed attempt by telling the model that
its last answer was not valid JSON, and the asker does the same. After a 429
there was no answer, so the eight asks answered on a later attempt carry a
prompt the first attempt did not. They are valid under §0, and none of them is
read apart.

---

## Stage C — the six adjudications

**What was run.** `python3 -m queue_alone.score`, on 2026-10-24, with
`PYTHONHASHSEED=0`, from pass 2's commit on a clean tree. `QA-g1` to `QA-g4`
passed again, with the suite green. The record is [`score.json`](score.json).

**Every statistic is a fraction of counts, compared with its line exactly.**
The record keeps each as a fraction beside its float. The standard errors are
clustered by ticket.

| row | statistic | line | reading | read | verdict |
|---|---|---|---|---|---|
| QA-a | over the ticket prompts, `S − A` | ≤ 0.05 | **+0.0062**, from **0.9187** and **0.9125** (se 0.0092) | 603 of 676 prompts | **holds** |
| QA-b | at `L₃`, `acc_q − acc_t` | > 0 | **+0.0849**, from **0.7689** and **0.6840** (se 0.0356) | 318 of 320 | **holds** |
| QA-c | at `L₃`, `(acc_q − acc_t) / (1 − acc_t)` | ≥ 1/2 | **0.2687**, compared as **−0.1462** against 0 (se 0.0601) | 318 of 320 | **refuted** |
| QA-d | at `L₃`, `(acc_q − acc_i) − (acc_i − acc_t)` | ≥ 0 | **−0.0031**, from **0.7689**, **0.7280** and **0.6840** (se 0.0507) | 318 of 320 | **refuted, thin** |
| QA-e | at `L₃`, `acc_q` | ≥ 0.90 | **0.7689** (se 0.0351) | 318 of 320 | **refuted** |
| QA-f | at `L₃`, `(acc_q − acc_t) − (acc_q⁰ − acc_t⁰)` | > 0 | **+0.1258**, from **0.7689** and **0.6840** with the rules, **0.4261** and **0.4670** with the names alone (se 0.0416) | 318 of 320 | **holds** |

`QA-g` is reported, and everything below that is not in the table is its.

**`QA-d` is thin, and only `QA-d`.** Its value lies within one standard error
of its line, and dropping run L3r1 or run L3r2 would put it on the other side.
No other row is carried by one run.

**The drafter expected `QA-a`, `QA-b`, `QA-d` and `QA-f` to hold, and `QA-c`
and `QA-e` to be refuted.** Five of six went the way §0 bet. `QA-d`, which the
drafter trusted least, went the other way, thinly. That is a fact about this
plan, and the scoreboard counts it.

### The queue alone, at level 3

| | right, on the 318 decisions every row reads | |
|---|---|---|
| the rule arm | 0.6840 | v1 with the rules, the ticket alone, asked for a rule |
| the impasse arm | 0.7280 | the same framing, asked for the queue alone |
| the plain arm | 0.7689 | the same rules, asked for the queue alone |
| compiled once | 1.0000 | `G-a` |

- **Asking for the queue alone helps**, by +0.0849 over the rule arm, and every
  run agrees on its sign: +0.0833, +0.1185 and +0.0404 (`QA-b` holds).
- **It recovers 0.2687 of what the rule arm gets wrong** (`QA-c` refuted), and
  it leaves the model short of the list by a quarter of the decisions: right on
  0.7689 against §0's 0.90 (`QA-e` refuted). Its runs read 0.7679, 0.7778 and
  0.7576.
- **The two steps are about equal.** From the rule arm to the impasse arm the
  model gains 0.0440, and from the impasse arm to the plain arm 0.0409. So the
  rule-writing apparatus and the impasse framing each carry about half of the
  gain, and `QA-d` is refuted by −0.0031, inside its noise.
- **Today's rule arm stands for `PLAN_APPLY.md`'s.** Re-asked under one
  provider, it agrees with that plan's Baidu answers 0.9125 of the time, and
  with itself 0.9187 (`QA-a` holds). It is right on 0.6840 of these decisions,
  where `PLAN_APPLY.md`'s ticket arm was right on 0.7031 of all 320.

### What the plain question buys

**`QA-f` holds: the gain is the list's.** On the same level-3 tickets, with the
names alone, the plain arm is right on 0.4261 and the rule arm on 0.4670. So
without a manual the plain question loses, and with the 29 rules it gains.
Its runs read +0.1131, +0.1741 and +0.0707.

### What the model still gets wrong

Every answer at level 3, classified against the 29 rules as §5.6 defines it:

| arm | answers | first | order | matching |
|---|---|---|---|---|
| the rule arm | 640 | 439 | 139 | 62 |
| the impasse arm | 640 | 467 | 164 | 9 |
| the plain arm | 638 | 491 | 141 | 6 |
| `PLAN_APPLY.md`'s ticket arm | 640 | 450 | 135 | 55 |
| `PLAN_APPLY.md`'s screen arm | 640 | 378 | 193 | 69 |

- **Asked for the queue alone, the model almost never names a queue no
  matching rule gives**: 6 answers of 638, against the rule arm's 62.
- **The order errors stay.** 141 of the plain arm's answers name the queue of a
  rule the ticket matches lower in the list, against the rule arm's 139.
- **So what the plain question removes is the matching errors, and what is left
  of the application is the list's order.** The model finds a rule that covers
  the ticket, and not the first.
- **A mechanical reading of the same list does better.** The copier that
  answers the queue of the matching rule with the most conditions is right on
  0.8719 of these decisions (Stage A). It applies the list by specificity,
  which is not the order the text states, and still beats every arm.

These are `QA-g`'s, read after the verdicts, and they adjudicate nothing.

### Every level

Each arm on the decisions where its own two answers are valid:

| level | decisions | rule arm | impasse arm | plain arm |
|---|---|---|---|---|
| `L₀`, the names | 116 | 0.6250 | 0.6638 | 0.6379 |
| `L₁`, the catalogue | 100 | 0.4450 | 0.4800 | 0.4400 |
| `L₂`, and the prose | 242 | 0.6426 | 0.5954 | 0.6281 |
| `L₃`, the rules | 320 | 0.6859 | 0.7297 | 0.7689 |

- **Only the rules gain from the plain question.** With the names or the
  catalogue the three arms sit within four points of each other.
- **With the prose the plain question does not help**: −0.0145 against the rule
  arm, and the impasse arm is the lowest of the three.
- **Read with every ticket once**, however often the loop escalated it, level
  3's arms are right on 0.6735, 0.7412 and 0.7751.

### The rarest queues

Counts of right answers, two per decision:

| level | queue | decisions | rule arm | impasse arm | plain arm | the names alone, plain |
|---|---|---|---|---|---|---|
| `L₂` | `ONCALL_ESCALATION` | 9 | 18 of 18 | 16 of 18 | 18 of 18 | 14 of 18 |
| `L₂` | `SECURITY_INCIDENT` | 17 | 24 of 34 | 18 of 34 | 20 of 34 | 34 of 34 |
| `L₂` | `ACCOUNT_MANAGER` | 60 | 78 of 120 | 59 of 120 | 80 of 120 | 0 of 120 |
| `L₂` | `T3_ENGINEERING` | 24 | 18 of 48 | 11 of 48 | 4 of 48 | 13 of 48 |
| `L₃` | `ONCALL_ESCALATION` | 9 | 18 of 18 | 18 of 18 | 18 of 18 | 15 of 18 |
| `L₃` | `SECURITY_INCIDENT` | 28 | 36 of 56 | 20 of 56 | 27 of 56 | 56 of 56 |
| `L₃` | `ACCOUNT_MANAGER` | 28 | 36 of 56 | 33 of 56 | 35 of 56 | 0 of 56 |
| `L₃` | `T3_ENGINEERING` | 36 | 35 of 72 | 38 of 72 | 41 of 72 | 9 of 72 |

- **`SECURITY_INCIDENT` goes the other way again.** With the names alone the
  model names it on every answer. With the rules it names it on 36, 20 and 27
  answers of 56, the impasse arm least. `PLAN_APPLY.md` found the same of its
  ticket arm.
- **`T3_ENGINEERING` gains from the plain question with the rules, and loses
  with the prose**: 41 of 72 at level 3, and 4 of 48 at level 2.
- **`ONCALL_ESCALATION` is named on every answer of every arm at level 3.**

### Agreement

At level 3 a prompt's two answers agree 0.8969 of the time in the rule arm,
0.9344 in the impasse arm and 0.9591 in the plain arm. The rule and plain arms
answer alike 0.7862 of the time.

### What the verdicts say

- **The rule-writing prompt costs the application something, and not most of
  it.** Asked for the queue alone, with the 29 rules and no screen, the model
  is right on three escalated tickets in four. Asked for a rule, on two in
  three.
- **The framing and the rule share that cost about evenly.** Neither is the
  mechanism alone.
- **What remains is the list's order.** Asked plainly, the model nearly always
  names a queue the ticket's rules give, and on more than a fifth of its
  answers not the first rule's. Compiling the same list once, it writes it
  exactly.
- **Read with `PLAN_APPLY.md`'s figures, which `QA-a` licenses, the loss
  falls in three parts.** That plan's screen took about a quarter of what the
  loop's proposer got wrong at level 3. The rule-writing prompt takes a smaller
  part. Most of the rest is choosing among rules that all cover the ticket. The
  two records were asked on the same tickets with the same rule arm, on
  consecutive days and under different routing.

### What Stage C does not settle

1. **Why the model, asked plainly, follows a lower rule.** Reasoning is off and
   the list is 29 rules long. A question that asks which rule applies, before
   its queue, would separate finding the first match from naming it. Reasoning
   on is §12's third item.
   **[NOTE 2026-10-25] Which lower rule, read POST-RUN**: the next one, in
   *Where the order errors go*, below. Why is still open.
2. **The rule-writing prompt without the impasse framing**, the fourth cell
   (§12, first item).
3. **The plain question with a screen** (§12, second item).
4. **The prose.** The plain question does not help at level 2, and it costs
   `T3_ENGINEERING` there. Why is not read.
5. **`SECURITY_INCIDENT` under the rules.** Which rule the rule arm's notes
   cite on those tickets is free on the records: they are recorded whole.
6. **The retry after a rate limit.** Eight answers were given with v1's JSON
   retry message in the conversation. A protocol that pins a provider meets
   429s, and should retry a failed call without telling the model its answer
   was malformed.
7. **One model, one provider, one manual, two passes, one day.**

---

## Where the order errors go — POST-RUN

> **POST-RUN.** Asked for by Sergi on 2026-10-25, after the plan closed, and
> run the same day. Zero API calls. `queue_alone/orders.py` read every valid
> answer of the three arms at level 3 against the 29 rules of level 3's frozen
> text, as §5.6 did. No oracle is read.
> - **The expectation was committed before any figure of the reading
>   existed.** It is five clauses in the module's docstring, committed as
>   `2ac1b2d`, which is `c08db88` on `main`, with what the drafter had seen.
> - **Four gates stood before any write.**
>   - The classes come back from `score.json`, and the copiers from
>     `sample.json`.
>   - `H29` matches every level-3 ticket, and the first match gives every
>     decision its truth.
>   - The order errors partition.
>
> Not a signed row; no verdict moves. The record is [`orders.json`](orders.json).
> It reached `main` in pull request #174. Its `_env` names the branch commit it
> was written from, `2ac1b2d`, with a clean tree. That commit and `c08db88` have
> the same subject, the same tree and the same `git patch-id --stable`, and the
> GitHub API names #174 behind the `main` commit. Its code digest,
> `ec9245821cd8466d`, is the one `main` computes after the merge.

**The terms.** A ticket's matching rules, in the list's order, are `r₁, r₂, …`,
and `r₁` gives its truth. An order error names the queue of some lower matching
rule, and the rule it follows is the highest such rule. **The runner-up** is the
first matching rule that gives another queue than `r₁`'s. **The catch-all** is
`H29`, *severity gte 1*, which matches every ticket. **The most specific** rule is
the matching rule with the most conditions.

### The next rule

| arm | order errors | the second matching rule's queue | the runner-up's | the catch-all's | the most specific rule's |
|---|---|---|---|---|---|
| the rule arm | 139 | 131 | 133 | 16 | 35 |
| the impasse arm | 164 | 153 | 153 | 10 | 30 |
| the plain arm | 141 | 134 | 135 | 5 | 33 |

- **The model names the next rule.** 134 of the plain arm's 141 order errors
  name the queue of the second rule the ticket matches, and 135 the
  runner-up's. Every other order error names the third rule's.
- **All three arms do it.** The rule arm sends 133 of its 139 to the
  runner-up, and the plain arm 135 of 141, 0.9568 against 0.9574. Asking for
  the queue alone removed the matching errors and did not move where the order
  errors go.
- **They are not a fall to the default.** Five of the plain arm's 141 follow
  the catch-all.
- **Nor are they specificity.** Where the most-conditions rule gives another
  queue than the first's, the plain arm names it on 33 of 82 answers, and the
  first rule's on 43.

### The rules passed over

The plain arm's order errors by the rule that governs the ticket, beside its
answers on the tickets that rule governs:

| governing rule | what it says | order errors | answers |
|---|---|---|---|
| `H18` | integrations → `T2_TECHNICAL` | 30 | 68 |
| `H02` | the keyword and severity ≤ 2 → `SECURITY_INCIDENT` | 29 | 36 |
| `H16` | api → `T2_TECHNICAL` | 15 | 68 |
| `H17` | integrations and severity ≤ 2 → `T3_ENGINEERING` | 13 | 28 |
| `H15` | api and severity ≤ 2 → `T3_ENGINEERING` | 12 | 36 |
| `H13` | enterprise and 5 or more prior tickets → `ACCOUNT_MANAGER` | 12 | 18 |
| `H14` | business and 8 or more prior tickets → `ACCOUNT_MANAGER` | 9 | 22 |

The other governing rules carry 21 order errors between them.

- **A few rules carry the errors.** `H18`, `H02` and `H16` carry 74 of the 141.
- **Three of them sit just above the broader rule that follows them.** `H02`
  is the keyword with severity at most 2, and `H03`, the next rule, the keyword
  alone. `H15` and `H17` are api and integrations at severity at most 2, and
  `H16` and `H18` the same products at any severity. On the tickets each of the
  three governs, the runner-up is that broader rule. So an order error there
  that names the runner-up takes the general rule over the exception the list
  puts above it. The plain arm makes 29 order errors on 36 answers under
  `H02`, 12 on 36 under `H15` and 13 on 28 under `H17`.
- **`H02` is where `SECURITY_INCIDENT` is lost.** Its tickets carry the
  keyword, and the rule after it sends them to `T2_TECHNICAL`. The plain arm is
  wrong on 29 of its 56 answers on that class at level 3, and makes 29 order
  errors under `H02`.
- **The rules the plain arm's order errors follow most** are `H03` (29), `H24`
  (23), `H28` (20) and `H26` (16): the keyword alone, the free tier at severity
  3 or more, the business and enterprise tiers, and severity 4 with no prior
  ticket.

### The expectation, clause by clause

| clause | expected | read | verdict |
|---|---|---|---|
| O1 | at least half of the plain arm's order errors name the runner-up's queue | 135 of 141 | holds |
| O2 | fewer than one in five follow the catch-all | 5 of 141 | holds |
| O3 | where the most-conditions rule gives another queue, the plain arm names it on at least half | 33 of 82 | **fails** |
| O4 | three governing rules carry at least half of the plain arm's order errors | 74 of 141 | holds |
| O5 | the rule and plain arms send theirs to the runner-up within 0.15 of each other | 0.9568 and 0.9574 | holds |

**Four of five held.** O3, which the drafter trusted least, failed: the model
does not read the list by specificity, and at the three pairs above it reads
against it.

### What this reading does not settle

- **Why the model takes the next rule.** Whether it misreads the first rule's
  conditions, or reads the exception as covered by the general rule below it,
  these answers cannot say. A question for the rule that applies would show
  which rule the model believes it is applying.
- **Which rule follows which, beyond the runner-up.** The record counts the
  rules passed over and the rules followed apart. Where the runner-up is fixed
  by construction, as at the three pairs above, the two meet.

---

## Files

```
results_queue_alone/sample.json     Stage A: the checks, the design with every prompt and
                                    the decisions it serves, the sessions' orders, the
                                    system prompts, the reference columns
results_queue_alone/ask_smoke.json  Stage B's smoke: one ask of each arm at each level
results_queue_alone/ask_pass1.json  Stage B's pass 1: 2,028 asks, every attempt with its
                                    provider, finish reasons and tokens, every answer whole
results_queue_alone/ask_pass2.json  Stage B's pass 2: the same asks in another order
results_queue_alone/score.json      Stage C: the six verdicts with their parts, errors and
                                    runs, and QA-g
results_queue_alone/orders.json     POST-RUN: where the order errors go at level 3, by arm,
                                    and the expectation clause by clause
```
