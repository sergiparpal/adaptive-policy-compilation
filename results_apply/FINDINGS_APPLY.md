# The rules applied ticket by ticket — findings

Record opened on October 24, 2026, under [`PLAN_APPLY.md`](../PLAN_APPLY.md).
The plan and its package reached `main` in pull request #161. Sergi signed §0
on 2026-10-23, before any figure below existed, in a commit of its own:
`b7bcf0e` on `main`, merged with Stage A in pull request #162.

Every record names in its `_env` the commit it was written from. Four were
written from `main` itself, so their hashes need no translation. Stage A's was
written on the branch of #162, from the signing commit. The rebase merge gave
that commit a new hash on `main`, with the same subject, the same tree and the
same `git patch-id --stable`, and the GitHub API names #162 behind it.

| record | written from | the same commit on `main` | reached `main` in |
|---|---|---|---|
| `sample.json` | `611f4ba`, the signature, on the branch | `b7bcf0e` | #162 |
| `ask_smoke.json` | `263b6d2`, Stage A's commit | `263b6d2` | #163 |
| `ask_pass1.json` | `83a01ab`, the smoke run's commit | `83a01ab` | #164 |
| `ask_pass2.json` | `7643675`, pass 1's commit | `7643675` | #165 |
| `score.json` | `814821d`, pass 2's commit | `814821d` | the pull request of this record |

All five carry one code digest, `3b3acdc8f7ce1943`, with `code_dirty` and
`git_dirty` false. **This record owns every figure in it.**

**All three stages ran on 2026-10-23 and 24, and the six rows are adjudicated:
`X-a`, `X-b`, `X-d`, `X-e` and `X-f` hold, `X-e` thinly, and `X-c` is
refuted.**

- **With the rules in its prompt, the screen costs the proposer about a ninth
  of its escalated tickets**: right on 0.7031 of level 3's decisions without
  it, against 0.5906 with it.
- **And that is about a quarter of what the proposer gets wrong with the
  screen.** The rest is the application's: with the 29 rules in front of it
  and no screen, the model still misroutes three escalated tickets in ten, where
  compiling the same rules once it gets every point right.
- **The screen pulls the answer to its commonest action even with the policy
  in the prompt**, and the rules reach the ticket's answer when nothing else is
  shown: 0.7003 with them against 0.4744 with the names alone, on the same
  tickets.
- **With the prose, the screen costs almost nothing**, +0.0165, within one
  standard error of nothing.

**[NOTE 2026-10-24] Read POST-RUN within one provider's answers, every row
keeps the side of its line where Stage C found it**, and the mix of providers
moves none of them by more than 0.0160. See *Each row within one provider's
answers*, below.

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Its counts were computed
> while drafting, and §0 declared them. Its reference columns were computed
> after the signature, for the first time. Zero API calls.
>
> **PROVENANCE, STAGES B AND C: PRE-REGISTERED.** `X-a` to `X-f` were signed
> before any of their figures existed, and none of their bands was set on a
> development set.

**Surface: the corpus.** Every figure is about tickets of
`generate_corpus(2000, seed=17)` that escalated in one of `PLAN_MANUAL.md`'s
twelve loop runs. The population is the escalations, not the arrivals (§5.3 of
the plan).

---

## Stage A — the checks, the design and the references

**What was run.** `python3 -m apply.sample`, on 2026-10-23, with
`PYTHONHASHSEED=0`, from the signing commit on a clean tree. The record is
[`sample.json`](sample.json).

**The blocking checks passed before anything was written.**

- **`X-g1`.** The suite was green, 2,172 tests. The twelve loop records replay
  with no departure through `fidelity.replay.check`, each under its level's
  system prompt, whose digest is the one `PLAN_MANUAL.md`'s Stage A recorded.
  The loop's choice of queue by level comes back queue by queue as that plan's
  `G-g` holds it: 62 of 119, 34 of 103, 164 of 245 and 183 of 323.
- **`X-g2`.** Every screen is the row's, over 790 escalations. The ticket arm
  is v1's empty base under the level's prompt, case 0's prompt at every level,
  and `PLAN_SCREEN.md`'s digest on 183 of its 183 shared tickets. No builder
  takes a row, and no digest stands for two texts.
- **`X-g3`.** The populations and the schedule are §0's and §1's.
- **`X-g4`.** Signed.

**Every count §0 lists as computed while drafting comes back**, so §0 needs no
erratum.
- 778 decisions, that is 116, 100, 242 and 320 by level. 193 of them are on
  conflict screens, and there are 12 empty screens.
- 676 ticket prompts, 183 of them `PLAN_SCREEN.md`'s at level 0.
- 13 asks share their text with another.

**The reference columns.** Over each level's decisions:

| level | the loop named the right queue | the plurality is the true queue | the same on coverage screens | on conflict screens | the loop's answer is the plurality |
|---|---|---|---|---|---|
| `L₀`, the names | 0.5172 | 0.3966 | 0.3524 | 0.8182 | 0.7241 |
| `L₁`, the catalogue | 0.32 | 0.25 | 0.2698 | 0.2162 | 0.50 |
| `L₂`, and the prose | 0.6653 | 0.3884 | 0.2335 | 0.7333 | 0.4008 |
| `L₃`, the rules | 0.5625 | 0.35 | 0.268 | 0.6429 | 0.5219 |

- **On a coverage screen the plurality is seldom the ticket's queue**: about a
  quarter of the time at levels 2 and 3. On a conflict screen, where every rule
  shown matches the ticket, it is 0.6429 of the time at level 3 and 0.7333 at
  level 2.
- **The loop's answer is the plurality** on half of level 3's decisions, and on
  0.7241 of level 0's. That is not the pull, which `X-d` measures against a
  second answer without the screen.

---

## Stage B — the calls

**Every call ran with reasoning off, at `deepseek/deepseek-v4-flash`, through
the proposer `manual.run.build_proposer(level)` builds**, behind the signature,
the key check, `X-g1` to `X-g3` and Stage A's record each time.

**The smoke run**, [`ask_smoke.json`](ask_smoke.json), asked one decision and
one ticket at each level, on 2026-10-23 between 19:15:01 and 19:15:24 UTC.
- All eight answers were valid on their first attempt.
- Every attempt ended `stop`. Completions ran from 131 to 315 tokens against a
  cap of 1,200, and none reasoned.
- Baidu answered seven, and GMICloud one.

**Pass 1**, [`ask_pass1.json`](ask_pass1.json), run by Sergi in his terminal on
2026-10-23 between 19:35:10 and 20:54:13 UTC, without a resume.
- All 1,454 asks, in Stage A's order, and every answer valid. None failed.
- 1,453 answered on their first attempt. One, `s:L2r2:245`, ran its first
  attempt into the cap and ended `length`; its retry ended `stop`, with 229
  tokens.

**Pass 2**, [`ask_pass2.json`](ask_pass2.json), run by Sergi in his terminal on
2026-10-24 between 06:57:32 and 08:08:20 UTC, without a resume.
- All 1,454 asks, each on its first attempt, each ending `stop`. None failed.
- **Three answers are invalid**: `t:L0:64`, `t:L0:55` and `t:L0:388`, all of
  the ticket arm at level 0, all served by DeepInfra.
  - Each wrote its queue under an empty key instead of `action`.
  - Under §0 an answer is valid only when its `action` is one of the eight
    queues. So they are recorded as written, counted and left out, never
    repaired.
  - Pass 1 answered the same three asks validly.
  - They cost `X-f` 8 of its 320 decisions, under §0's 5% line, and no other
    adjudicated row.

**The providers.** Nine answered pass 1 under one name, and eight pass 2:

| pass | arm | attempts | Baidu | GMICloud | Relace | the rest |
|---|---|---|---|---|---|---|
| 1 | screen | 779 | 438 | 202 | 63 | 76 |
| 1 | ticket | 676 | 486 | 99 | 40 | 51 |
| 2 | screen | 778 | 628 | 28 | 89 | 33 |
| 2 | ticket | 676 | 521 | 12 | 85 | 58 |

**The interleaving did not give the arms the same providers in pass 1.** §5.9
expected it to. Baidu served 0.562 of the screen arm's attempts and 0.719 of
the ticket arm's, and GMICloud 0.259 and 0.146. In pass 2 the mix was closer:
Baidu 0.807 and 0.771. No row is read by provider, so each row compares arms
whose providers partly differ (*What Stage C does not settle*, below).
**[NOTE 2026-10-24]** Read POST-RUN on Baidu's answers alone, every row keeps
its side of its line: *Each row within one provider's answers*, below.

---

## Stage C — the six adjudications

**What was run.** `python3 -m apply.score`, on 2026-10-24, with
`PYTHONHASHSEED=0`, from pass 2's commit on a clean tree. `X-g1` to `X-g4`
passed again, with the suite green. The record is [`score.json`](score.json).

**Every statistic is a fraction of counts, compared with its line exactly.**
The record keeps each as a fraction beside its float. The standard errors are
clustered by ticket.

| row | statistic | line | reading | the decisions | verdict |
|---|---|---|---|---|---|
| X-a | `S − A` over every level, pooled | ≤ 0.05 | **−0.0064**, from **0.9049** and **0.9113** (se 0.0085) | 778, every one read | **holds** |
| X-b | at `L₃`, `acc_t − acc_s` | > 0 | **+0.1125**, from **0.5906** and **0.7031** (se 0.0375) | 320, every one read | **holds** |
| X-c | at `L₃`, `(acc_t − acc_s) / (1 − acc_s)` | ≥ 1/2 | **0.2748**, compared as **−0.1844** against 0 (se 0.0633) | 320, every one read | **refuted** |
| X-d | at `L₃`, where `t₁ ≠ p`: the screen's answers on `p`, less `t₂` on `p` | ≥ 0.10 | **0.1862**, from **0.2766** and **0.0904** (se 0.0383) | 188 of 320 | **holds** |
| X-e | at `L₂`, `acc_t − acc_s` | > 0 | **+0.0165**, from **0.6405** and **0.6570** (se 0.0367) | 242, every one read | **holds, thin** |
| X-f | at `L₃`, `acc_t − acc_u` | ≥ 0.10 | **+0.2260**, from **0.4744** and **0.7003** (se 0.0498) | 312 of 320 | **holds** |

`X-g` is reported, and everything below that is not in the table is its.

**`X-e` is thin, and only `X-e`.** Its value lies within one standard error of
its line. No row is carried by one run: dropping any run's decisions leaves
every verdict where it is.

**The drafter expected exactly this**: `X-a`, `X-b`, `X-d`, `X-e` and `X-f` to
hold, and `X-c` to be refuted. It trusted `X-f` most and `X-c` least. Six of
six went the way §0 bet. That is a fact about this plan, and the scoreboard
counts it; it is not a reason to trust the next drafter more.

### The screen and the application, at level 3

| | right, of 320 decisions | |
|---|---|---|
| the loop, on 2026-10-21 | 0.5625 | its own answer at each escalation |
| the screen arm, today | 0.5906 | the same prompt, two answers |
| the ticket arm, today | 0.7031 | the ticket alone, under the same system prompt |
| the names alone, no screen | 0.4744 | level 0's ticket arm, on 312 of the decisions |
| compiled once | 1.0000 | `G-a`: each of five asks decides every point of the space right, these tickets among them |

- **The screen costs the proposer 0.1125**, and every run agrees on its sign:
  +0.1412, +0.1519 and +0.0350 (`X-b` holds).
- **That is 0.2748 of what the screen arm gets wrong** (`X-c` refuted). The
  ticket arm still misroutes 0.2969 of the decisions. Deciding one ticket
  against the list is lossy without any screen, and that loss is the larger
  part.
- **The rules do reach the ticket**: without a screen they lift the answer by
  0.2260 over the names alone, on the same tickets (`X-f` holds).
- **Today's screen arm stands for the loop**: re-asked its own prompts, the
  model agrees with the loop's answers of 2026-10-21 as often as with itself
  (`X-a` holds).

### The pull

**`X-d` holds: the screen pulls the answer to its plurality with the rules in
the prompt.** On the 188 decisions whose first ticket-arm answer is not the
plurality, the screen arm names it 0.2766 of the time, and a second ticket-arm
answer 0.0904. By run: 0.0769, 0.2867 and 0.1557.

**The plurality is not the only thing the screen pulls toward.** Where the two
arms answer differently, the screen arm's answer is:

| level | the plurality | the first action shown | another action shown | an action not shown |
|---|---|---|---|---|
| `L₀` | 50 | 8 | 6 | 2 |
| `L₁` | 38 | 6 | 21 | 7 |
| `L₂` | 66 | 6 | 83 | 11 |
| `L₃` | 101 | 2 | 94 | 11 |

At level 3, nearly as many changed answers go to another action the screen
shows as to its plurality, 94 against 101. Only 11 go to an action it does not
show.

### Coverage screens and conflict screens

`PLAN_SCREEN.md` §5.9 left the conflict screen unmeasured. Read apart, the two
kinds go opposite ways:

| level | coverage: decisions, `acc_s`, `acc_t` | the screen's cost | conflict: decisions, `acc_s`, `acc_t` | the screen's cost |
|---|---|---|---|---|
| `L₀` | 103, 0.4660, 0.5777 | +0.1117 | 11, 1.0000, 1.0000 | 0 |
| `L₁` | 63, 0.3651, 0.4921 | +0.1270 | 37, 0.1757, 0.4054 | +0.2297 |
| `L₂` | 167, 0.5719, 0.6407 | +0.0689 | 75, 0.7933, 0.6933 | −0.1000 |
| `L₃` | 250, 0.5480, 0.7060 | +0.1580 | 70, 0.7429, 0.6929 | −0.0500 |

- **A coverage screen costs at every level.** It shows rules that do not match
  the ticket, and its plurality is seldom the ticket's queue (Stage A).
- **A conflict screen helps at levels 2 and 3.** It shows rules that match the
  ticket, and there the plurality is the true queue 0.6429 and 0.7333 of the
  time. That is `V-d`'s first clause met where `PLAN_SCREEN.md` never looked.
- **Level 1's conflict screens cost the most**, on 37 decisions where the
  plurality is right a fifth of the time.

These are `X-g`'s, read after the verdicts, and they adjudicate nothing.

### The prose

**`X-e` holds thinly: with the prose in its prompt, the screen costs the
proposer +0.0165.** Its runs read +0.0100, +0.0102 and +0.0455. The coverage
screens cost +0.0689 and the conflict screens give back 0.1000, and the two
nearly cancel. The prose's bases were broader, and their conflict screens more
often right.

### The rarest queues

Counts over the decisions of each class: the screen arm's and the ticket arm's
right answers of two per decision, the names alone's, and the loop's.

| level | queue | decisions | screen arm | ticket arm | names alone | the loop |
|---|---|---|---|---|---|---|
| `L₂` | `ONCALL_ESCALATION` | 9 | 14 of 18 | 18 of 18 | 18 of 18 | 6 |
| `L₂` | `SECURITY_INCIDENT` | 17 | 30 of 34 | 24 of 34 | 34 of 34 | 16 |
| `L₂` | `ACCOUNT_MANAGER` | 60 | 105 of 120 | 79 of 120 | 0 of 119 | 54 |
| `L₂` | `T3_ENGINEERING` | 24 | 15 of 48 | 18 of 48 | 4 of 48 | 9 |
| `L₃` | `ONCALL_ESCALATION` | 9 | 17 of 18 | 18 of 18 | 18 of 18 | 9 |
| `L₃` | `SECURITY_INCIDENT` | 28 | 48 of 56 | 37 of 56 | 56 of 56 | 24 |
| `L₃` | `ACCOUNT_MANAGER` | 28 | 25 of 56 | 47 of 56 | 0 of 53 | 13 |
| `L₃` | `T3_ENGINEERING` | 36 | 18 of 72 | 37 of 72 | 6 of 72 | 8 |

- **At level 3 the screen loses `ACCOUNT_MANAGER` and `T3_ENGINEERING`.**
  Without it the rules name the first right on 47 of 56 answers and the second
  on 37 of 72; with it, on 25 and 18. The names alone never name
  `ACCOUNT_MANAGER`.
- **At level 2 the screen helps `ACCOUNT_MANAGER`**: 105 of 120 with it, 79
  without. The prose's bases route the class, and their rules are what a
  screen shows.
- **`SECURITY_INCIDENT` goes the other way.** With the names alone the model
  names it on every answer; with the rules and no screen, on 37 of 56 at level
  3 and 24 of 34 at level 2. The screen gives some of it back. Which rule the
  model applied there, the notes might say: they are recorded whole, and no
  stage coded them.
- **`ONCALL_ESCALATION` is named on every ticket-arm answer** at both levels.

### The rules written beside the answers

No rule was installed (rule E). Read as written: whether it matches its own
ticket, and how many points off the keyword it spans.

| level | arm | answers | validate | median points off the keyword | at most 840 points |
|---|---|---|---|---|---|
| `L₂` | screen | 484 | 435 | 1,680 | 171 |
| `L₂` | ticket | 298 | 270 | 4,200 | 51 |
| `L₃` | screen | 640 | 632 | 400 | 483 |
| `L₃` | ticket | 342 | 314 | 6,720 | 94 |
| `L₀` | screen | 232 | 232 | 1,260 | 108 |
| `L₀` | ticket | 550 | 544 | 6,720 | 103 |

- **With the screen, the list's rules are narrow, as in the loop**: a median
  of 400 points at level 3, against 1,680 under the prose.
- **Without it, every level writes broad rules**, the names alone too. The
  ticket arm's prompt says the base is empty and the rule is the first, which
  may be what invites breadth (§5.1 of the plan). So this cannot say the screen
  narrows the list's rules: the empty base and the screen differ in more than
  the rules shown.
- **The tickets differ between levels**, so the levels are not set against
  each other here.

### The model on two dates

**On 181 tickets `PLAN_SCREEN.md` asked with the ticket alone on 2026-10-14,**
level 0's ticket arm asked the same prompt today. Two lost a valid answer.
- Each day's two answers agree on 0.9337.
- An answer of one day agrees with one of the other on 0.913.
- They are right on 0.4972 then and 0.5166 today.

So the model moved little in ten days, as `X-a` found over three.

### What the verdicts say

- **The screen is part of why the loop misapplies the rules, and the smaller
  part.** With the 29 rules in its prompt and no screen, the model names the
  right queue on seven escalated tickets in ten. With the screen the loop
  showed, on six. Compiling the same rules once, it writes them exactly.
- **So most of what the loop loses on the acting axis is lost deciding one
  ticket against the list**, inside a prompt that frames the ticket as an
  impasse and asks for a rule. `CHAT_SUMMARY.md` §2.2's erratum said it of
  another prompt: *"With the right information in front of it, it makes the
  same mistake"*.
- **Authority does not remove deference.** With the policy in front of it, the
  model still follows the rules a screen shows. That costs where the screen is
  a coverage screen, and pays where it is a conflict screen of the right
  rules.
- **With the prose the screen costs almost nothing.** Its bases were broader,
  and their conflict screens more often right.

### What Stage C does not settle

1. **Why the application loses three tickets in ten.** Both arms ask for a
   rule, under a prompt that calls the ticket an impasse. A question asking for
   the queue alone would separate the rule-writing task from the application.
   That is a new prompt, and another plan.
2. **Which part of the screen does the work**: the rules shown, or the header
   above them, which tells the proposer that no rule matches (§5.1 of the
   plan). A prompt with the header over an empty list is a new prompt.
3. **The providers.** In pass 1 the arms got different providers, against
   §5.9's expectation. A reading of each row within the answers one provider
   gave is free on the records, and it was not made.
   **[NOTE 2026-10-24] Read POST-RUN**, in *Each row within one provider's
   answers*, below. On Baidu's answers every row keeps its side of its line,
   and against the same decisions the cut moves none by more than 0.0160. On
   one prompt, Baidu is right as often as the providers it shares asks with.
4. **`SECURITY_INCIDENT` under the rules without a screen.** The notes are
   recorded whole, past the loop records' cut, and a reading of which rule
   they cite is free.
5. **Whether the screen narrows the list's rules.** The empty base differs from
   the screen in more than the rules shown, and the levels ask different
   tickets.
6. **One model, one manual, three runs a level, two days**, and providers this
   plan did not pin.

---

## Each row within one provider's answers — POST-RUN

> **POST-RUN.** Asked for by Sergi on 2026-10-24 and run the same day. Zero
> API calls. `apply/providers.py` read every row of Stage C on the answers one
> provider gave, and every ask two answers at a time.
> - **The provider of an answer is its last attempt's**, the one whose text
>   was parsed. One answer took two attempts, both served by Relace.
> - **The expectation was committed before any figure by provider existed.**
>   It is ten clauses in the module's docstring, committed as `4753cf6`. The
>   drafter had read this record whole. From the routing alone, which reads no
>   answer, it had counted which provider gave every answer.
> - **Four gates stood before any write.**
>   - Stage C comes back, through `adjudicate` and through the cut with every
>     provider admitted.
>   - Every answer has one provider.
>   - A ticket has one truth.
>   - The loop's answer has one call.
>
> Not a signed row; no verdict moves. The record is
> [`providers.json`](providers.json). Its `_env` names the branch commit it was
> written from, `4753cf6`, with a clean tree.

**Ten providers answered the two passes under one name, and only Baidu answered
enough of every row's decisions to read a row on its answers.** GMICloud served
a quarter of pass 1's screen arm, and it holds at most 37 decisions of any row;
Relace holds at most 27. Their cells are in the record, below the floor of 100
decisions, and are not read. The clauses of sections 1 and 2 read Baidu.

### 1. Each row on Baidu's answers

On the decisions Stage C read for a row, each arm is cut to the answers Baidu
gave.
- Where Baidu gave both answers of an arm, both are read. Where it gave one,
  that one is read alone.
- A decision drops out where Baidu gave no answer to an arm the row compares.
- `X-d` keeps Stage C's selector, `t₁ ≠ p`, whoever gave `t₁`.
- `X-a` needs both screen answers and the loop's own answer to be Baidu's.

Beside each cut, the same decisions are read with every answer, as Stage C
reads them.

| row | line | Stage C | on Baidu's answers | the same decisions, every answer | decisions |
|---|---|---|---|---|---|
| `X-a`, `S − A` at every level | ≤ 0.05 | −0.0064 | +0.0106 | +0.0106 | 379 of 778 |
| `X-b`, `acc_t − acc_s` at `L₃` | > 0 | +0.1125 | +0.0996 | +0.1037 | 246 of 320 |
| `X-c`, its share at `L₃` | ≥ 1/2 | 0.2748 | 0.2634 | 0.2713 | 246 of 320 |
| `X-d`, the pull at `L₃` | ≥ 0.10 | +0.1862 | +0.1565 | +0.1565 | 115 of 188 |
| `X-e`, `acc_t − acc_s` at `L₂` | > 0 | +0.0165 | +0.0642 | +0.0481 | 187 of 242 |
| `X-f`, `acc_t − acc_u` at `L₃` | ≥ 0.10 | +0.2260 | +0.2491 | +0.2365 | 277 of 312 |

- **Every row stays on the side of its line where Stage C found it.** On
  Baidu's answers the screen still costs the proposer a tenth of level 3's
  decisions, and that is still about a quarter of what it gets wrong.
- **The cut barely moves a row.** Against the same decisions read with every
  answer, Baidu's answers move `X-b` by −0.0041, `X-d` by nothing, `X-e` by
  +0.0160 and `X-f` by +0.0126. The mix of providers moved no row by more than
  that.
- **What moves the values is which decisions are read.** `X-e` reads +0.0642
  on Baidu's answers, against Stage C's +0.0165. Two thirds of that gap is
  already there on the same 187 decisions read with every answer, +0.0481.
- **`X-d` is thin here**: without run L3r2 it falls below its line. Its runs
  read 0, +0.2755 and +0.1184. In Stage C it was not thin.
- **`S − A` rises inside one provider, and stays under its line.** On the 379
  decisions whose three answers Baidu gave, the two screen answers agree 0.9261
  of the time, against Stage C's 0.9049 over every decision. They agree with
  the loop's answer 0.9156 of the time, against 0.9113.

### 2. Each row on the decisions Baidu answered whole

This is Stage C's own estimator, on the decisions where every answer a row
reads is Baidu's, `X-d`'s `t₁` included. These are fewer decisions.

| row | Stage C | Baidu gave every answer | decisions |
|---|---|---|---|
| `X-a` | −0.0064 | +0.0106 | 379 |
| `X-b` | +0.1125 | +0.0054 | 92 |
| `X-c`, its share | 0.2748 | 0.0133 | 92 |
| `X-d` | +0.1862 | +0.1078 | 51, under the plan's floor of 100 |
| `X-e` | +0.0165 | +0.0878 | 74 |
| `X-f` | +0.2260 | +0.1810 | 174 |

- **`X-b`, `X-c` and `X-f` stay on their sides, and `X-b` by a hair.** On the
  92 decisions Baidu answered whole, the screen costs +0.0054. Its standard
  error is 0.0551, and its runs read −0.0385, +0.1316 and −0.1250. That lies
  1.94 standard errors under Stage C's value.
- **It is the decisions, not Baidu.** On those 92 decisions the ticket arm is
  right 0.5978 of the time, against 0.7215 on the 246 of reading A. The screen
  arm is right 0.5924 of the time, against 0.6220. And on reading A's
  decisions, cutting them to Baidu's answers moves `X-b` by −0.0041.

### 3. Whether the providers answer one prompt alike

Every ask has one answer from each pass. These are the asks where Baidu gave
one answer and another provider gave the other, both read against the ticket's
truth:

| Baidu in one pass, in the other | asks | Baidu right | the other right | difference | se |
|---|---|---|---|---|---|
| GMICloud | 218 | 0.5642 | 0.5780 | −0.0138 | 0.0220 |
| Relace | 109 | 0.6606 | 0.6514 | +0.0092 | 0.0378 |
| any other provider | 483 | 0.5694 | 0.5776 | −0.0083 | 0.0144 |

How often the two answers to one ask agree:

| arm | one provider gave both | two providers did |
|---|---|---|
| screen | 0.9256, on 457 asks | 0.8754, on 321 |
| ticket | 0.9069, on 451 | 0.8423, on 222 |

- **On one prompt, Baidu is right as often as the others.** Pooled over the
  other providers, the difference is 0 on the screen arm and −0.0203 on the
  ticket arm.
- **But two providers part more often than one provider parts from itself**,
  on both arms. A second provider changes the answer more often than a second
  call to the same one, and not how often it is right.
- **So the mix of providers could not tilt an arm's accuracy by much.** The
  cut measured the same thing on the rows.

### The expectation, clause by clause

A1 to A7 read section 1, B1 reads section 2, and C1 and C2 read section 3.

| clause | expected | read | verdict |
|---|---|---|---|
| A1 | `X-b` above its line, within 0.05 of Stage C's value | +0.0996 against +0.1125 | holds |
| A2 | `X-c`'s share below 1/2 | 0.2634 | holds |
| A3 | `X-d` at or above its line, on 100 decisions or more | +0.1565 on 115 | holds |
| A4 | `X-e` within 0.05 of Stage C's value | +0.0642 against +0.0165 | holds |
| A5 | `X-f` at or above its line | +0.2491 | holds |
| A6 | `X-a` at or below its line | +0.0106 | holds |
| A7 | the cut moves `X-b`, `X-d`, `X-e` and `X-f` by at most 0.03 each | at most +0.0160, `X-e`'s | holds |
| B1 | on the decisions Baidu answered whole, `X-b`, `X-c` and `X-f` on Stage C's sides | +0.0054, 0.0133 and +0.1810 | holds |
| C1 | Baidu right as often as GMICloud, Relace and the rest pooled, within 0.05 each | −0.0138, +0.0092 and −0.0083 | holds |
| C2 | in each arm, two answers agree more often from one provider than from two | 0.9256 against 0.8754, 0.9069 against 0.8423 | holds |

**Ten of ten held.**
- The drafter trusted C1 least, and it held.
- A4 held at 0.0476 from Stage C's value, against its 0.05.
- B1 held on `X-b` by +0.0054.

### What this reading does not settle

- **Why the decisions Baidu answered whole show almost no screen cost.** Which
  decisions those are is set by where four asks were routed. Whether that
  follows anything about the tickets, or the 92 are a draw that fell low, this
  record does not say. Free on the records.
- **Any provider but Baidu, row by row.** No row can be read on GMICloud's
  answers or on any other provider's. Only the asks set them beside Baidu.

---

## Files

```
results_apply/sample.json       Stage A: the checks, the design with every decision and
                                ask, the sessions' orders, the system prompts, the
                                reference columns
results_apply/ask_smoke.json    Stage B's smoke: one ask of each arm at each level
results_apply/ask_pass1.json    Stage B's pass 1: 1,454 asks, every attempt with its
                                provider, finish reasons and tokens, every answer whole
results_apply/ask_pass2.json    Stage B's pass 2: the same asks in another order
results_apply/score.json        Stage C: the six verdicts with their parts, errors and
                                runs, and X-g
results_apply/providers.json    POST-RUN: each row on one provider's answers and on the
                                decisions it answered whole, the asks two answers at a
                                time, and the expectation clause by clause
```
