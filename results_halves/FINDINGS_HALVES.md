# Which half of v2b's base paragraph makes the loop's first call cut — findings

Record opened on November 12, 2026, under [`PLAN_HALVES.md`](../PLAN_HALVES.md).
Sergi signed §0 on 2026-11-10, before any figure below existed, in a commit of
its own: `a2fda84` on `main`.
- **The plan, its package, the signature, Stage A and the smoke run** reached
  `main` in #229, merged on 2026-11-10.
- **The three sessions** reached it in #232, merged on 2026-11-11.
- **Stage C, this record, the banner that closes the plan and the indexes**
  reach it in #235, the pull request this record was opened in.
- **The POST-RUN reading of why the hidden half cuts** reached it in #236,
  merged on 2026-11-12.

Every record names in its `_env` the commit it was written from. Four were
written on a pull request's branch, and the rebase merge gave each of those
commits a new hash on `main`. Each pair has the same subject and the same `git
patch-id --stable`, and the GitHub API names the pull request behind every
`main` commit.
- **The two pairs of #229 have the same tree.**
- **The two of #232 do not.** `main` gained #230, #231 and #233 while the
  sessions ran, and the rebase set the sessions' commits on top of them. The
  trees differ in the files those three pull requests changed, and in nothing
  under `results_halves/`.

| record | written from | the same commit on `main` | code digest | `git_dirty`, `code_dirty` |
|---|---|---|---|---|
| `sample.json` | `48cda60`, the signature, on the branch of #229 | `a2fda84` | `40800a2d3dcedf68` | false, false |
| `ask_smoke.json` | `835d00b`, Stage A's commit, on the branch of #229 | `32eb892` | `40800a2d3dcedf68` | false, false |
| `ask_pass1.json` | `39287bb`, the smoke run's commit, on `main` (#229) | itself | `40800a2d3dcedf68` | false, false |
| `ask_pass2.json` | `c219609`, pass 1's commit, on the branch of #232 | `05ebcdd` | `40800a2d3dcedf68` | false, false |
| `ask_oncall.json` | `7750e23`, pass 2's commit, on the branch of #232 | `edfdcb1` | `40800a2d3dcedf68` | false, false |
| `score.json` | `180b874`, #234's merge, on `main` (#234) | itself | `82958f7008a0d0f9` | false, false |

**`git_dirty` and `code_dirty` are false in every record.** The sample, the
smoke run and the three sessions carry one code digest, `40800a2d3dcedf68`,
which `main` computes at `39287bb`. The package's code did not change between
the signature and the last session.

**`score.json` carries another digest, because `main` gained two changes to the
code before Stage C ran.**
- **#230 corrected `halves/score.py`, before Stage C**, as `5b1e253` on `main`.
  - **What §0 says.** An answer is valid when the call came back, after its
    retries, with a payload that parses, from the pinned provider.
  - **What the asker flagged.** Its flag also asks for an action among the
    eight queues, so an empty object came back flagged invalid. Four of pass
    1's first 126 answers were one.
  - **What the scorer reads now.** §0's definition. It classes an empty object
    *no rule*, and keeps the asker's flag as `valid_as_recorded`.
  - **When.** No figure of Stage C existed when this was corrected, and no
    answer was classed to find it. `main` computes `fc8f3b274d4dfcfb` from
    `5b1e253` to `d85ae3c`.
- **#234 added `harness/ask_pool.py`**, which no module of `halves/` imports.
  `main` computes `82958f7008a0d0f9` at `180b874`.

> **[NOTE 2026-11-12] One more record, written after Stage C by code added
> after it.** [`hidden.json`](hidden.json) is the POST-RUN reading of why the
> hidden half cuts.
> - **It was written from `e8b70aa`**, on the branch of #236, which is `d2b2e34`
>   on `main`. Its section below names the pair's checks.
> - **Its code digest is `fa32ca570f2a482b`**, not Stage C's, because
>   `halves/hidden.py` was added after Stage C. `main` computes it at `d2b2e34`.
>   The modules Stage C ran did not change.

**This record owns every figure in it.**

**All three stages ran between 2026-11-10 and 2026-11-12, and the six rows are
adjudicated. `HV-a`, `HV-b`, `HV-d` and `HV-e` hold, and `HV-c` and `HV-f` are
refuted. No verdict is thin. `HV-g` is reported.**

- **The paragraph's gap is not the period's.** Asked in one period, of one
  provider, with the arms interleaved:
  - the empty base wrote its ticket's governing region whole in 201 of its 260
    right-queue answers, 0.7731;
  - v2b's paragraph wrote it in 90 of 250, 0.3600 (`HV-b` holds).

  The reading that proposed this plan had found gaps of 0.4298 to 0.4841
  across dates and providers. This one is 0.4131.
- **The hidden half carries all of it.** v2b's first half alone says the base
  is not shown and asks for a rule for this ticket.
  - **It wrote the region in 0.3008 of its answers**, below v2b's whole
    paragraph. That is 0.2658 below the midpoint the plan's bet needed it above
    (`HV-c` refuted).
  - **Against the empty base it costs 0.4723** (`HV-d` holds), more than the
    gap itself.
- **The overlap half costs on its own, and only beside the empty base.**
  - **After the empty base**, the clause that overlapping rules of another
    queue will be listed lowered the share from 0.7731 to 0.6332 (`HV-e`
    holds).
  - **After the hidden half** it did not lower it. v2b's whole paragraph stands
    0.0592 above the hidden half alone.
  - **So the halves interact.** `(W_h − W_v) − (W_e − W_o)` is −0.1991,
    reported and not banded.
- **At the rarest queue's seven tickets, dropping the overlap half gave nothing
  back** (`HV-f` refuted). The hidden half wrote the region in 19 of its 40
  right-queue answers there, and v2b's paragraph in 20 of 40.
- **The instrument held** (`HV-a` holds). Ticket by ticket, today's `v` wrote
  the region 0.0360 more often than the DeepInfra loops' first calls had, at
  the same 99 tickets.
- **Told that the base is hidden, the first call declares against the manual.**
  `v` and `h` declared `beats` or `loses_to` in 133 and 144 of their 300 valid
  answers, `e` in 35 and `o` in 78. Every declaration cited the manual's
  identifiers, which no base holds.
- **A prompt's two answers in the passes shared a class about half the time**:
  in 0.51 to 0.58 of the 136 prompts, by arm.
- **It cost $1.1164 and about a day of calls.** §1 expected one to two dollars,
  and 30 to 44 hours one ask at a time. The asks took 23.8 hours, summed.
- **The drafter expected `HV-a` to `HV-e` to hold and `HV-f` to be refuted.**
  Five of the six came out so. **Its bet, `HV-c`, was refuted**: the half it
  expected to cost less carried more than the whole gap.

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Its references were
> computed after the signature. §0's four figures had been seen while drafting,
> as §0 says. Zero API calls.
>
> **PROVENANCE, STAGES B AND C: PRE-REGISTERED.** `HV-a` to `HV-f` were signed
> before any of their figures existed, and none of their bands was set on a
> development set.
> - **`HV-a` and `HV-b` are replications.** Each sets a figure a POST-RUN
>   reading had published, `whole/paragraph.py`'s, against a new period. For
>   `HV-b`'s empty base it is a new provider too.
> - **§0 asks the scoreboard to read them as replications**, as it reads
>   `PL-e`'s and `WR-e`'s.
>
> **WHAT WAS SEEN BEFORE STAGE C.** The agent that launched the sessions saw,
> before the scorer ran:
> - **Each session's commit message**, which the supervisor wrote from the
>   record. It gives the session's span and launches, the providers that served
>   it, its attempts' finish reasons, the attempts refused for the rate, its
>   failures and its `_env`. It gives no class, share or row, as §0 says.
> - **The supervisor's log**: each launch, record, commit and push, with its
>   hour.
> - **The sessions' progress lines**, read from time to time. Each gives the
>   ask's count, its arm and ticket, and the queue its answer named.
> - **Each session's closing line**: its answers, how many the asker flagged
>   valid, and its failures.
> - **The smoke run's record**, before pass 1: its calls, providers, finish
>   reasons, pace and bill. No row reads it.
> - **Four of pass 1's answers, on 2026-11-10.** They were among its first 126,
>   and came back flagged invalid. They were empty objects. DeepInfra served
>   all four, and all ended `stop`. Nothing else of them was read, and #230
>   corrected the scorer before Stage C (above).
> - **The rarest queue's partial file, on 2026-11-11 at 18:26 UTC**, read at 16
>   answers for its pace, its providers and the asker's flag.
>
> No class, no `W` and no row was computed before Stage C. The bills were read
> after it.

**Each figure names its surface.** Every ticket is one of
`generate_corpus(2000, seed=17)`'s that a reasoning loop escalated. Every class
reads its answer's region over the exhaustive space of 134,400 points, as
`whole/paragraph.py` reads it. No row reads the arrivals.
- **`HV-b` to `HV-e`** read both passes at the 136 tickets of `T`.
- **`HV-f`** reads both passes and the rarest queue's session at `T₇`, the
  queue's seven tickets.
- **`HV-a`** reads `v` in both passes beside `PLAN_PLACEMENT.md`'s six runs and
  `PLAN_WHOLE.md`'s three v1c runs, ticket by ticket.
- **`HV-g`** says which sessions each of its readings reads.

**The four arms differ in one paragraph**: the one that stands where the base
would be, at the head of the first call's user message (§2.1 of the plan).
- **`e`, the empty base**: *"BASE DE REGLAS: vacia. Esta es la primera regla."*
- **`v`, v2b's paragraph**: the base is not shown in this step, write your rule
  for this ticket; *"si se solapa con reglas existentes de OTRA cola, se te
  listaran despues."*
- **`h`, the hidden half alone**: v2b's paragraph up to its semicolon, closed by
  a full stop.
- **`o`, the overlap half on the empty base**: `e`'s line closed by a semicolon,
  then v2b's clause.

Every other byte of each request is the loop's first call under v1c: level 3's
system prompt, the ticket, reasoning at high effort with 16,000 tokens and
temperature 0. Every call was pinned to DeepInfra's fp8 endpoint.

---

## Stage A — the checks, the design and the references

**What was run.** `PYTHONHASHSEED=0 python3 -m halves.sample`, on 2026-11-10 at
12:29 UTC, from the signing commit on a clean tree. The record is
[`sample.json`](sample.json).

**The blocking checks passed before anything was written**, with the suite
green: `HV-g1`, the texts; `HV-g2`, the request and the instrument; `HV-g3`,
the design. `HV-g4` found the plan signed.

**§0's four figures came back as declared**, so §0 needs no erratum: the
tickets, their governing rules, `HV-a`'s tickets and the pace on DeepInfra.
The record keeps them under `figures`, and its `figures_not_back` is empty.

**The references adjudicate nothing.** Each is a list of classes, ticket by
ticket, of answers already paid for:
- the rule arm's answers at the 133 tickets it asked: `PLAN_REASONED_RULE.md`'s
  arm `w`, asked of Baidu on 2026-10-25;
- each of the five loop groups' first calls, at the tickets of `T` it
  escalated;
- `HV-a`'s comparator: the DeepInfra loops' first calls under v2b's paragraph,
  pooled, at 102 tickets.

`HV-g` sets them beside today's answers, below.

---

## Stage B — the asks

**Every call ran at `deepseek/deepseek-v4-flash`, pinned to DeepInfra's fp8
endpoint with fallbacks off.** It ran with reasoning `{"effort": "high"}`,
16,000 tokens, temperature 0, and `response_format` on the first attempt.
- **Each launch checked** the signature, the turn, the key, `HV-g1` to `HV-g3`
  and Stage A's record before any call.
- **The asker is the loop's**: `reasoned_loop.protocol.Live` over
  `placement.protocol.Asker`, with its pin.

| session | from its first kept answer to its last | span | launches | asks | attempts | valid as §0 reads it | flagged by the asker | failed | served by | finish reasons | retries |
|---|---|---|---|---|---|---|---|---|---|---|---|
| the smoke run | 2026-11-10 12:41 to 2026-11-10 12:55 UTC | 0 h 15 min | 1 | 8 | 8 | 8 | 0 | 0 | DeepInfra 8 | `stop` 8 | none |
| pass 1 | 2026-11-10 13:18 to 2026-11-10 23:01 UTC | 9 h 43 min | 1 | 544 | 544 | 544 | 18 | 0 | DeepInfra 544 | `stop` 544 | none |
| pass 2 | 2026-11-10 23:15 to 2026-11-11 17:56 UTC | 18 h 41 min | 2 | 544 | 545 | 544 | 17 | 0 | DeepInfra 545 | `stop` 544, `length` 1 | parse 1 |
| the rarest queue's session | 2026-11-11 18:05 to 2026-11-11 20:18 UTC | 2 h 14 min | 1 | 112 | 112 | 112 | 7 | 0 | DeepInfra 112 | `stop` 112 | none |

- **The smoke run**, [`ask_smoke.json`](ask_smoke.json), asked two tickets of
  each arm on 2026-11-10.
  - Every answer was valid. Every attempt was served by DeepInfra, reasoned and
    ended `stop`.
  - Its bill, read by generation id before pass 1, was at the price §1
    assumed.
  - Its pace, a mean of 118.5 seconds an ask, put the sessions at about 39
    hours. It rested on eight asks.
- **Pass 1**, [`ask_pass1.json`](ask_pass1.json), ran in one launch. Its
  commit's push failed five times, on the Windows credential helper through
  WSL. The supervisor went on, and the agent pushed the commit by hand the next
  morning and opened #232.
- **Pass 2**, [`ask_pass2.json`](ask_pass2.json), ran in two launches.
  - **WSL shut down under its first**, at about 00:48 UTC, after 86 answers;
    the last was kept at 00:48:46. It booted again at 07:01.
  - **The agent relaunched the supervisor at 07:41**, and the session resumed
    from its partial file at 07:44:34, with its checks passed. No call was made
    for 6 h 56 min.
  - **The record's `started_at` is that resume's.** The span above runs from its
    first kept answer. Each resumed answer keeps its own seconds.
  - **One attempt reached the budget.** At ticket 35 under `h`, the first
    attempt ended `length` at 16,000 completion tokens. Retried with v1's
    message, as §0's retry by cause says, it answered in 2,426. It is the
    session's one retry.
- **The rarest queue's session**, [`ask_oncall.json`](ask_oncall.json), ran in
  one launch: the 28 prompts at `T₇`, four times each.
- **No call failed, and no attempt was refused for the rate.** Every attempt
  that reached the model was served by DeepInfra.
- **The merge of #232.**
  - **The CI did not run.** GitHub's incidents of that evening, in Webhooks from
    20:22 to 20:26 UTC and in Actions from 20:48 to 21:21, left the three CI
    runs on the last head queued with no job.
  - **The supervisor did not merge.** It waited two hours and stopped at 22:27.
  - **What the agent did, at Sergi's word.** It ran the tests workflow on the
    branch, and closed and reopened the pull request. Both `ci-complete` runs
    were green on `1947bbc`, and #232 was merged by rebase at 23:00:39,
    matching that head.

**The asker's flag and §0's validity.** The asker's flag also asks that an
answer name one of the eight queues, which §0 does not. It flagged 42 answers
that §0 reads as valid. Every one was an empty object, classed *no rule*:

| arm | flagged by the asker, valid as §0 reads it | of them, an empty object | their class |
|---|---|---|---|
| `e`, the empty base | 10 | 10 | 10 no rule |
| `v`, v2b's paragraph | 15 | 15 | 15 no rule |
| `h`, the hidden half alone | 9 | 9 | 9 no rule |
| `o`, the overlap half on the empty base | 8 | 8 | 8 no rule |

**So every answer of the three sessions is valid as §0 reads it**, and no row
lost an answer to invalidity. Each row's share of invalid answers is zero.

| session | seconds an ask, median / mean | longest ask, seconds | prompt tokens, median | completion tokens, median / most | reasoning tokens, median / most | seconds summed |
|---|---|---|---|---|---|---|
| the smoke run | 118.2 / 118.5 | 234.1 | 1,747 | 5,008 / 7,235 | 4,942 / 7,168 | 0.3 h |
| pass 1 | 58.9 / 64.5 | 303.9 | 1,748 | 4,598 / 13,427 | 4,369 / 13,092 | 9.7 h |
| pass 2 | 70.3 / 76.4 | 673.0 | 1,753 | 4,456 / 16,000 | 4,328 / 11,953 | 11.6 h |
| the rarest queue's session | 67.2 / 72.9 | 199.1 | 1,748 | 4,296 / 11,395 | 3,958 / 11,518 | 2.3 h |
| **all four** |  |  |  |  |  | **23.8 h** |

**What it cost, and how far §1 was.**

| session | attempts billed | billed | prompt tokens | completion tokens | provider | per million prompt tokens, completion at twice |
|---|---|---|---|---|---|---|
| the smoke run | 8 of 8 | $0.0067 | 13,974 | 33,452 | DeepInfra | $0.0832 |
| pass 1 | 544 of 544 | $0.5048 | 950,380 | 2,647,997 | DeepInfra | $0.0808 |
| pass 2 | 545 of 545 | $0.5044 | 952,150 | 2,639,114 | DeepInfra | $0.0810 |
| the rarest queue's session | 112 of 112 | $0.1004 | 195,720 | 519,574 | DeepInfra | $0.0813 |
| **all four** | 1,209 of 1,209 | **$1.1164** | 2,112,224 | 5,840,137 |  | $0.0809 |

- **The money.** $1.1164 for 1,209 attempts, inside §1's one to two dollars, at
  the price §1 assumed: $0.081 per million prompt tokens, with completion at
  twice that.
- **The time.** §1 priced the 1,208 asks at 30 to 44 hours one at a time, and
  the smoke run's pace pointed to about 39.
  - **The passes ran faster than either**: at a median of 58.9 and 70.3 seconds
    an ask, against the 77 to 112 of §0's fourth figure.
  - **The asks took 23.8 hours, summed.**
  - **From the smoke run's first answer to the rarest queue's last**, 31 h 37
    min passed. For 6 h 56 min of them WSL was down.

---

## Stage C — the six adjudications

**What was run.** `PYTHONHASHSEED=0 python3 -m halves.score`, on 2026-11-12 at
07:11 UTC, from `main` at `180b874` on a clean tree, after #232 had merged.
`HV-g1` to `HV-g4` passed again, with the suite green. The record is
[`score.json`](score.json).

**Every statistic is a ratio of integer counts, compared with its line
exactly.** The record keeps each as a fraction beside its float. The standard
errors are clustered by ticket, and only mark *thin*. **No answer was invalid
as §0 reads it**, so every row has a value and reads every answer it names.

| row | statistic | line | reading | read | verdict |
|---|---|---|---|---|---|
| HV-a | the mean, over the tickets where `v` and the DeepInfra loops' first calls both named the right queue, of `v`'s share less theirs | from −1/10 to 1/10 | **0.0360**, 2993/83160 (se 0.0370) | 99 tickets, both passes | **holds** |
| HV-b | `W_e − W_v` | ≥ 1/5 | **0.4131**, 537/1300, from **0.7731** and **0.3600** (se 0.0375) | 136 tickets, both passes | **holds** |
| HV-c | `W_h − (W_e + W_v)/2` | > 0 | **−0.2658**, −22111/83200, with `W_h` **0.3008** (se 0.0267) | 136 tickets, both passes | **refuted** |
| HV-d | `W_e − W_h` | ≥ 1/10 | **0.4723**, 7859/16640, from **0.7731** and **0.3008** (se 0.0348) | 136 tickets, both passes | **holds** |
| HV-e | `W_e − W_o` | ≥ 1/10 | **0.1399**, 9419/67340, from **0.7731** and **0.6332** (se 0.0359) | 136 tickets, both passes | **holds** |
| HV-f | `W_h⁷ − W_v⁷` | ≥ 1/5 | **−0.0250**, −1/40, from **0.4750** and **0.5000** (se 0.1075) | `T₇`'s 7 tickets, both passes and the rarest queue's session | **refuted** |

`HV-g` is reported, and everything below that is not in the table is its.

**No verdict is thin.**
- **No statistic lies within one standard error of its line.** `HV-e` comes
  nearest: 0.0399 above its line, against an error of 0.0359.
- **Neither pass alone puts any of `HV-a` to `HV-e` on the other side:**

| row | pass 1 alone | pass 2 alone | both passes | standard error |
|---|---|---|---|---|
| `HV-a` | 0.0140 (1103/78960) | 0.0713 (5513/77280) | 0.0360 (2993/83160) | 0.0370 |
| `HV-b` | 0.4584 (1863/4064) | 0.3668 (1985/5412) | 0.4131 (537/1300) | 0.0375 |
| `HV-c` | −0.2317 (−3767/16256) | −0.3005 (−4337/14432) | −0.2658 (−22111/83200) | 0.0267 |
| `HV-d` | 0.4609 (59/128) | 0.4839 (511/1056) | 0.4723 (7859/16640) | 0.0348 |
| `HV-e` | 0.1094 (7/64) | 0.1697 (2935/17292) | 0.1399 (9419/67340) | 0.0359 |

- **Nor does leaving out any one of `T₇`'s tickets move `HV-f` across its
  line:**

| ticket left out | its governing rule | `W_h⁷ − W_v⁷` without it |
|---|---|---|
| 257 | `H05` | 0.0160 (19/1190) |
| 710 | `H05` | −0.0882 (−3/34) |
| 954 | `H04` | −0.0160 (−19/1190) |
| 982 | `H04` | −0.0739 (−44/595) |
| 1432 | `H04` | 0.0151 (9/595) |
| 1783 | `H05` | −0.0588 (−1/17) |
| 1951 | `H04` | 0.0294 (1/34) |

**`HV-c` had a value.** §0 gives it none if `W_e − W_v` is a tenth or less, and
it is 0.4131.

**The drafter expected `HV-a`, `HV-b`, `HV-c`, `HV-d` and `HV-e` to hold, and
`HV-f` to be refuted.** It trusted `HV-b` most, then `HV-a`, `HV-c`, `HV-e` and
`HV-d`.
- **Five of the six came out as expected**, the two it trusted most among them.
- **Its bet, `HV-c`, was refuted.** The hidden half it expected to cost less
  than the overlap half costs more than the whole gap.
- **`HV-d`, the row it trusted least, holds**, by more than ten of its standard
  errors.

That is a fact about this plan, and the scoreboard counts it.

### The four arms

| arm | `W`, both passes | the mean of its tickets' shares | pass 1 | pass 2 | at `T₇`, with the rarest queue's session |
|---|---|---|---|---|---|
| `e`, the empty base | 0.7731 (201/260) | 0.7684 (209/272) | 0.7812 (25/32) | 0.7652 (101/132) | 0.8205 (32/39) |
| `v`, v2b's paragraph | 0.3600 (9/25) | 0.3444 (31/90) | 0.3228 (41/127) | 0.3984 (49/123) | 0.5000 (1/2) |
| `h`, the hidden half alone | 0.3008 (77/256) | 0.2904 (79/272) | 0.3203 (41/128) | 0.2812 (9/32) | 0.4750 (19/40) |
| `o`, the overlap half on the empty base | 0.6332 (164/259) | 0.6418 (43/67) | 0.6719 (43/64) | 0.5954 (78/131) | 0.6750 (27/40) |

- **`e` against `v`** is the gap the reading found, asked in one period:
  0.7731 against 0.3600.
- **`h` lies below `v` in both passes**: by 0.0025 in pass 1, and by 0.1171 in
  pass 2.
- **`o` lies between them, nearer `e`**, at 0.6332.
- **At `T₇` every arm writes the region more often than over `T`**, and `h` and
  `v` stand level: 0.4750 and 0.5000.

Every valid answer of both passes, by class:

| arm | valid answers | whole | cut by one | cut by two | other | wrong queue | no rule |
|---|---|---|---|---|---|---|---|
| `e`, the empty base | 272 | 201 | 30 | 0 | 29 | 4 | 8 |
| `v`, v2b's paragraph | 272 | 90 | 79 | 0 | 81 | 9 | 13 |
| `h`, the hidden half alone | 272 | 77 | 83 | 2 | 94 | 8 | 8 |
| `o`, the overlap half on the empty base | 272 | 164 | 52 | 0 | 43 | 7 | 6 |

- **Where `h` and `v` lose the region, it goes to the narrower classes.** `v`
  has 79 cuts by one listed rule and 81 *other*, and `h` 83 and 94, with two
  cuts by two. `e` has 30 and 29.
- **Few answers name the wrong queue or no valid rule**: 4 to 9 and 6 to 13 of
  272, by arm. So no hold here is carried by answers lost to the wrong queue,
  which §0 asked `HV-g` to show.

Every right-queue answer of the three sessions, by class and by breadth against
its governing region:

| arm | right-queue answers, all three sessions | whole: the region itself | whole: wider | whole: neither | cut: neither | other: neither |
|---|---|---|---|---|---|---|
| `e`, the empty base | 286 | 223 | 0 | 1 | 33 | 29 |
| `v`, v2b's paragraph | 276 | 94 | 1 | 8 | 89 | 84 |
| `h`, the hidden half alone | 283 | 81 | 0 | 10 | 97 | 95 |
| `o`, the overlap half on the empty base | 285 | 176 | 1 | 5 | 59 | 44 |

**No hold is carried by drafts wider than the region.** One answer of `v` and
one of `o` is wider. Every other whole answer is the region itself, or covers
the part without being the region.

### By queue and by governing rule

Right-queue answers classed *whole*, both passes, at the tickets of `T`:

| the ticket's queue | tickets | `e` | `v` | `h` | `o` |
|---|---|---|---|---|---|
| `T1_GENERAL` | 20 | 22 of 35 | 3 of 35 | 4 of 39 | 25 of 38 |
| `T2_TECHNICAL` | 48 | 67 of 91 | 22 of 88 | 13 of 87 | 53 of 88 |
| `T3_ENGINEERING` | 11 | 20 of 21 | 12 of 19 | 12 of 21 | 15 of 22 |
| `BILLING_SPECIALIST` | 5 | 8 of 10 | 5 of 10 | 5 of 9 | 8 of 9 |
| `SECURITY_INCIDENT` | 19 | 31 of 38 | 17 of 37 | 13 of 36 | 21 of 38 |
| `ACCOUNT_MANAGER` | 11 | 18 of 22 | 11 of 22 | 10 of 22 | 12 of 22 |
| `ONCALL_ESCALATION` | 7 | 9 of 13 | 7 of 14 | 5 of 13 | 9 of 14 |
| `SELF_SERVICE_DEFLECT` | 15 | 26 of 30 | 13 of 25 | 15 of 29 | 21 of 28 |

**`h` and `v` lose the region most under `T1_GENERAL` and `T2_TECHNICAL`.**
There `h` wrote it in 4 of 39 and 13 of 87 answers, and `v` in 3 of 35 and 22
of 88. `e` wrote it in 22 of 35 and 67 of 91, and `o` in 25 of 38 and 53 of 88.

| governing rule | its queue | tickets | `e` | `v` | `h` | `o` |
|---|---|---|---|---|---|---|
| `H01` | `SECURITY_INCIDENT` | 9 | 17 of 18 | 11 of 17 | 5 of 16 | 10 of 18 |
| `H02` | `SECURITY_INCIDENT` | 10 | 14 of 20 | 6 of 20 | 8 of 20 | 11 of 20 |
| `H03` | `T2_TECHNICAL` | 4 | 5 of 8 | 2 of 8 | 0 of 8 | 4 of 8 |
| `H04` | `ONCALL_ESCALATION` | 4 | 4 of 7 | 5 of 8 | 3 of 7 | 5 of 8 |
| `H05` | `ONCALL_ESCALATION` | 3 | 5 of 6 | 2 of 6 | 2 of 6 | 4 of 6 |
| `H07` | `T3_ENGINEERING` | 1 | 2 of 2 | 1 of 1 | 2 of 2 | 2 of 2 |
| `H08` | `T2_TECHNICAL` | 9 | 13 of 17 | 0 of 17 | 1 of 14 | 11 of 16 |
| `H09` | `ACCOUNT_MANAGER` | 4 | 5 of 8 | 4 of 8 | 3 of 8 | 5 of 8 |
| `H10` | `BILLING_SPECIALIST` | 3 | 5 of 6 | 3 of 6 | 4 of 6 | 4 of 5 |
| `H11` | `BILLING_SPECIALIST` | 2 | 3 of 4 | 2 of 4 | 1 of 3 | 4 of 4 |
| `H12` | `SELF_SERVICE_DEFLECT` | 4 | 7 of 8 | 2 of 8 | 2 of 8 | 5 of 8 |
| `H13` | `ACCOUNT_MANAGER` | 4 | 7 of 8 | 3 of 8 | 3 of 8 | 3 of 8 |
| `H14` | `ACCOUNT_MANAGER` | 3 | 6 of 6 | 4 of 6 | 4 of 6 | 4 of 6 |
| `H15` | `T3_ENGINEERING` | 5 | 9 of 10 | 5 of 8 | 4 of 10 | 6 of 10 |
| `H16` | `T2_TECHNICAL` | 15 | 21 of 30 | 11 of 28 | 9 of 30 | 19 of 27 |
| `H17` | `T3_ENGINEERING` | 5 | 9 of 9 | 6 of 10 | 6 of 9 | 7 of 10 |
| `H18` | `T2_TECHNICAL` | 16 | 20 of 28 | 4 of 27 | 0 of 27 | 13 of 29 |
| `H19` | `T2_TECHNICAL` | 1 | 2 of 2 | 2 of 2 | 1 of 2 | 2 of 2 |
| `H20` | `T2_TECHNICAL` | 3 | 6 of 6 | 3 of 6 | 2 of 6 | 4 of 6 |
| `H22` | `SELF_SERVICE_DEFLECT` | 1 | 2 of 2 | 2 of 2 | 2 of 2 | 2 of 2 |
| `H23` | `T1_GENERAL` | 1 | 1 of 1 | 2 of 2 | 0 of 2 | 0 of 2 |
| `H24` | `SELF_SERVICE_DEFLECT` | 7 | 12 of 14 | 7 of 11 | 8 of 14 | 10 of 13 |
| `H26` | `SELF_SERVICE_DEFLECT` | 3 | 5 of 6 | 2 of 4 | 3 of 5 | 4 of 5 |
| `H28` | `T1_GENERAL` | 7 | 9 of 13 | 1 of 12 | 4 of 14 | 11 of 13 |
| `H29` | `T1_GENERAL` | 12 | 12 of 21 | 0 of 21 | 0 of 23 | 14 of 23 |

- **Under the catch-all, `H29`, neither `v` nor `h` ever wrote the region**: 0
  of 21 and 0 of 23. `e` wrote it in 12 of 21, and `o` in 14 of 23.
- **Under `H18` and `H08` they almost never did.** They wrote it in 4 of 27 and
  0 of 27 under `H18`, and in 0 of 17 and 1 of 14 under `H08`.
- **Under no governing rule did `h` write the region more often than `e`.**

### The rarest queue's tickets

Both passes and the rarest queue's session, six answers an arm at each ticket:

| ticket | governing rule | `e` | `v` | `h` | `o` |
|---|---|---|---|---|---|
| 257 | `H05` | 6 whole | 5 whole, 1 cut | 3 whole, 2 cut, 1 no rule | 5 whole, 1 cut |
| 710 | `H05` | 5 whole, 1 cut | 2 cut, 4 other | 2 whole, 3 cut, 1 other | 3 whole, 2 cut, 1 no rule |
| 954 | `H04` | 4 whole, 1 cut, 1 no rule | 4 whole, 1 cut, 1 no rule | 4 whole, 1 cut, 1 other | 4 whole, 1 cut, 1 other |
| 982 | `H04` | 6 whole | 6 cut | 1 whole, 4 cut, 1 no rule | 3 whole, 2 cut, 1 no rule |
| 1432 | `H04` | 2 whole, 3 cut, 1 no rule | 2 whole, 3 cut, 1 no rule | 1 whole, 5 cut | 3 whole, 3 cut |
| 1783 | `H05` | 6 whole | 4 whole, 1 cut, 1 other | 5 whole, 1 cut | 5 whole, 1 cut |
| 1951 | `H04` | 3 whole, 1 cut, 1 other, 1 no rule | 5 whole, 1 other | 3 whole, 3 cut | 4 whole, 1 cut, 1 other |

- **At 982, `e` wrote the region in all six answers**, `v` cut in all six, and
  `h` in four. At 1432 every arm cut at least half the time, `e` included.
- **At 710, `v` never wrote the region.** It cut twice, and drafted *other* four
  times. `h` wrote it twice.
- **`HV-f`'s value stays on its side of the line whichever ticket is left
  out**, as the table above shows.

### What the first call declares

| arm | valid answers, all three sessions | declaring `beats` or `loses_to` | citing the manual's identifiers |
|---|---|---|---|
| `e`, the empty base | 300 | 35 | 35 |
| `v`, v2b's paragraph | 300 | 133 | 133 |
| `h`, the hidden half alone | 300 | 144 | 144 |
| `o`, the overlap half on the empty base | 300 | 78 | 78 |

- **The paragraphs that say a base exists and is hidden declare most**: `v` in
  133 of its 300 valid answers, and `h` in 144. Told that the base is empty,
  `e` declared in 35 and `o` in 78.
- **Every declaration names the manual's identifiers**, `H01` to `H29`, which no
  base holds. In a loop the engine drops such a declaration (`PLAN_MANUAL.md`).

### Agreement between the passes

| arm | prompts | the same class in both passes | share |
|---|---|---|---|
| `e`, the empty base | 136 | 79 | 0.5809 (79/136) |
| `v`, v2b's paragraph | 136 | 78 | 0.5735 (39/68) |
| `h`, the hidden half alone | 136 | 70 | 0.5147 (35/68) |
| `o`, the overlap half on the empty base | 136 | 70 | 0.5147 (35/68) |

**A prompt's two answers in the passes shared a class in about half the
prompts**: 0.51 to 0.58, by arm. So a single ask at a ticket says little about
the class that ticket draws. The shares above are read over many tickets, not
ticket by ticket.

### Beside the references, across dates and providers

| comparison | the reference's provider | tickets | today | the reference |
|---|---|---|---|---|
| `e` beside `PLAN_REASONED_RULE.md`'s arm `w` | Baidu | 133 | 0.7765 (66/85) | 0.8110 (103/127) |
| `v` beside `PLAN_REASONED_LOOP.md`'s first calls | Baidu | 94 | 0.3391 (59/174) | 0.3872 (91/235) |
| `v` beside `PLAN_CHANNEL.md`'s first calls | Baidu | 99 | 0.3497 (64/183) | 0.3984 (51/128) |
| `v` beside `PLAN_PLACEMENT.md`'s first calls | DeepInfra | 90 | 0.3964 (67/169) | 0.3834 (97/253) |
| `v` beside `PLAN_WHOLE.md`'s v1c first calls | DeepInfra | 80 | 0.4200 (21/50) | 0.3684 (7/19) |
| `v` beside `PLAN_WHOLE.md`'s v1d first calls, under T1 | DeepInfra | 62 | 0.4224 (49/116) | 0.5842 (59/101) |

- **`e` stands near the rule arm** that the reading set beside the loops: 0.7765
  at its 133 tickets, against 0.8110 from Baidu on 2026-10-25.
- **`v` stands near the loops' first calls under v2b's paragraph, on both
  providers**: 0.3391 to 0.4200 today, against 0.3684 to 0.3984.
- **v1d's first calls under T1 wrote the region more often than today's `v`**:
  0.5842 against 0.4224, at their 62 tickets.

### What the verdicts say

- **The cut is the hidden half's** (`HV-c` refuted, `HV-d` holds).
  - **Told that the base is not shown**, and asked for a rule for its ticket,
    the first call wrote the governing region in about three answers in ten.
    That is a little less often than under v2b's whole paragraph.
  - **Told that the base is empty** and its rule is the first, it wrote it in
    about three in four.
- **The overlap clause costs only where the base is said to be empty**
  (`HV-e` holds). Beside the hidden half it costs nothing, so the halves
  interact.
- **The gap is the paragraph's, not the period's** (`HV-b` holds), and today's
  `v` is the loops' first call (`HV-a` holds).
- **At the rarest queue's tickets, dropping the overlap half gives nothing
  back** (`HV-f` refuted), as the drafter expected. Read with the rows above,
  there is nothing there for it to give back: the hidden half alone cuts as `v`
  does.
- **So, as §0 read this pair in advance, dropping the overlap half would not be
  enough.** A blind loop cannot send an empty base, so the next text must say
  something else about the base it hides.
- **The declarations follow the same line.** The two paragraphs that say a base
  exists and is hidden declared against the manual in nearly half their
  answers. The two that say it is empty did so in about a tenth and a quarter
  of theirs.

### What Stage C does not settle

1. **What a loop compiles under another text.** No loop ran.
   - **None of the four arms is that text.** `h` cuts as `v` does, and a blind
     loop cannot send `e` or `o`.
   - **Which text a blind loop could send** in place of v2b's first half, and
     what it would compile, is the loop plan §12 names.
2. **Why the hidden half cuts.** The notes and the reasoning are recorded whole,
   and no stage codes them. One open question is whether the model takes the
   manual's rules for the hidden base's. The declarations bear on it, and a
   reading of the notes would test it.
   **[NOTE 2026-11-12] Read POST-RUN**, in *Why the hidden half cuts*, below.
   Told that the base is hidden, the first call reads the engine's impasse as a
   conflict between two of the manual's rules, and the cut settles it by
   containment. Told that it is empty, it mostly says the engine has no rule
   yet.
3. **Which of the hidden half's two sentences cuts**: that the base is not
   shown, or that the rule is for this ticket. `e` against `h` sets both of one
   paragraph's sentences against both of the other's, as the plan said first.
4. **The level-1 sentence**, which stays byte for byte in every arm (§12 of the
   plan).
5. **The interaction's size.** It is reported, not banded: its error is about
   the sum of four arms' errors.
6. **Tickets the reasoning loops never escalated, and the arrivals.** Every
   class reads the space.
7. **One model, one provider, one manual and one period.**

---

## Why the hidden half cuts — POST-RUN

**Asked for by Sergi on 2026-11-12, after Stage C.** Stage C found the cut in
v2b's first half. Told only that the base is not shown, and asked for a rule for
its ticket, the first call wrote the governing region about as rarely as under
the whole paragraph (`HV-c` refuted, `HV-d` holds). *What Stage C does not
settle* left why. This reading asks the records, and spends nothing.

**What was run.** `PYTHONHASHSEED=0 python3 -m halves.hidden`, on 2026-11-12,
from `e8b70aa` on a clean tree, which is `d2b2e34` on `main`. That commit
carries the reading's codebook and its expectation, written before it ran on the
held-out answers. The record was committed alone, as `9e41ac7` on `main`.
- **Each pair has the same subject, the same tree and the same `git patch-id
  --stable`.** The GitHub API names #236 behind both `main` commits.
- **The record is [`hidden.json`](hidden.json).** Gates 1 to 4 passed:
  - every answer is valid as §0 reads it;
  - the passes' classes are Stage C's;
  - every answer keeps its reasoning and its payload;
  - the codebook's counts on pass 1 come back.

**What it reads.** Every valid answer of the right queue, under the four arms:
- its class, as Stage C classes it, and for a cut the listed rules it is cut by;
- its note, and its declarations;
- its reasoning, by a codebook of anchored patterns.

A *crossing rule* is a listed rule after the governing one that the ticket
matches, and whose region does not contain the governing rule's.

**The codebook was frozen on pass 1**, and every clause reads the held-out
answers: those of pass 2 and of the rarest queue's session. The reasoning is
mostly in English and quotes the prompt in Spanish. It quotes the impasse frame,
and asks why the engine could not decide the ticket. The codes:
- **`CONFLICT`**: within 600 characters after a mention of the impasse, a word of
  conflict or overlap, both rules matching, neither containing the other, or
  deciding between rules;
- **`BETWEEN`**: a conflict named between two listed rules, "between H.. and
  H..";
- **`EMPTY`**: the base taken as empty: no rules, an empty base, the rule as the
  first;
- **`HIDDEN`**: the hidden-base sentence read: "no se te muestra", "not shown",
  "hidden";
- **`INSIDE` and `RESOLVES`**, read in the note: the draft lies inside another
  rule, and it resolves a conflict.

The codes that told nothing apart on pass 1 were dropped there, and the module
names them.

### 1. The cut is one operation, in every arm

| arm | held-out cuts | cut by the first crossing rule | note citing a crossing rule | whole answers whose note cites one |
|---|---|---|---|---|
| `e`, the empty base | 19 | 18 of 19 | 17 of 19 | 4 of 124 |
| `v`, v2b's paragraph | 51 | 46 of 51 | 50 of 51 | 22 of 62 |
| `h`, the hidden half alone | 56 | 52 of 56 | 56 of 56 | 17 of 50 |
| `o`, the overlap half on the empty base | 36 | 33 of 36 | 35 of 36 | 14 of 96 |
| **all four** | 162 | 149 of 162 | 158 of 162 | 57 of 332 |

- **Every arm cuts the same way.** 149 of the 162 held-out cuts are the
  governing region cut by the first crossing rule the ticket matches. 158 carry
  a note that cites a crossing rule. The whole answers' notes cite one in 57 of
  332.
- **So the arms differ in how often they cut**, not in what a cut is.

### 2. How each arm reads the impasse

Every held-out answer of the right queue:

| arm | right-queue answers | `CONFLICT` | `BETWEEN` | `EMPTY` | `HIDDEN` |
|---|---|---|---|---|---|
| `e`, the empty base | 158 | 91 of 158 | 32 of 158 | 153 of 158 | 0 of 158 |
| `v`, v2b's paragraph | 149 | 143 of 149 | 111 of 149 | 3 of 149 | 70 of 149 |
| `h`, the hidden half alone | 155 | 150 of 155 | 115 of 155 | 8 of 155 | 56 of 155 |
| `o`, the overlap half on the empty base | 157 | 140 of 157 | 71 of 157 | 125 of 157 | 1 of 157 |

- **Told that the base is hidden, the first call reads the impasse as a conflict
  in nearly every answer**: `h` in 150 of 155, and `v` in 143 of 149.
- **Told that it is empty, it does so in a little over half**: `e` in 91 of 158.
  It takes the base at its word in 153 of 158 answers, where `h` does so in 8 of
  155.
- **Beside the empty base, the overlap clause brings the conflict back**: `o`
  reads one in 140 of 157. Most of its answers still take the base as empty,
  125 of 157.

### 3. What goes with the cut, inside each arm

| arm | cuts where `BETWEEN` | cuts where not |
|---|---|---|
| `e`, the empty base | 14 of 32 | 5 of 126 |
| `v`, v2b's paragraph | 43 of 111 | 8 of 38 |
| `h`, the hidden half alone | 47 of 115 | 9 of 40 |
| `o`, the overlap half on the empty base | 32 of 71 | 4 of 86 |

| arm | class | answers | `BETWEEN` | `EMPTY` | `HIDDEN` | declaring `beats` or `loses_to` | declaring against a crossing rule |
|---|---|---|---|---|---|---|---|
| `e` | whole | 124 | 15 of 124 | 124 of 124 | 0 of 124 | 8 of 124 | 5 of 124 |
| `e` | cut | 19 | 14 of 19 | 16 of 19 | 0 of 19 | 8 of 19 | 6 of 19 |
| `e` | other | 15 | 3 of 15 | 13 of 15 | 0 of 15 | 4 of 15 | 2 of 15 |
| `v` | whole | 62 | 44 of 62 | 1 of 62 | 45 of 62 | 41 of 62 | 29 of 62 |
| `v` | cut | 51 | 43 of 51 | 0 of 51 | 10 of 51 | 15 of 51 | 11 of 51 |
| `v` | other | 36 | 24 of 36 | 2 of 36 | 15 of 36 | 13 of 36 | 5 of 36 |
| `h` | whole | 50 | 37 of 50 | 3 of 50 | 27 of 50 | 40 of 50 | 23 of 50 |
| `h` | cut | 56 | 47 of 56 | 0 of 56 | 7 of 56 | 12 of 56 | 10 of 56 |
| `h` | other | 49 | 31 of 49 | 5 of 49 | 22 of 49 | 25 of 49 | 11 of 49 |
| `o` | whole | 96 | 30 of 96 | 91 of 96 | 1 of 96 | 21 of 96 | 15 of 96 |
| `o` | cut | 36 | 32 of 36 | 16 of 36 | 0 of 36 | 10 of 36 | 8 of 36 |
| `o` | other | 25 | 9 of 25 | 18 of 25 | 0 of 25 | 9 of 25 | 5 of 25 |

- **Under the empty base, a named conflict is where the cuts are.** Where `e`'s
  reasoning names a conflict between two listed rules, 14 of 32 answers are
  cuts. Where it does not, 5 of 126 are.
- **Under the overlap half on the empty base, the cuts doubt the base.** `o`'s
  whole answers take it as empty in 91 of 96, and its cuts in 16 of 36.
- **Under the hidden half, a conflict is read almost everywhere, and the answers
  part by how they settle it.**
  - **`h`'s whole answers declare a side.** They declare `beats` or `loses_to`
    in 40 of 50, and against a crossing rule in 23. Its cuts declare in 12 of
    56.
  - **`v`'s split the same way**: 41 of 62 against 15 of 51.
- **And the whole answers read the hidden-base sentence more** (`HIDDEN`): `h`'s
  in 27 of 50 and its cuts in 7 of 56; `v`'s in 45 of 62 and 10 of 51.

### The expectation

Written in `halves/hidden.py`'s docstring and committed before the reading ran
on the held-out answers. It is not signed, and it is on no scoreboard.

| clause | on pass 1, the development set | held out |  |
|---|---|---|---|
| Q1 | cut by the first crossing 0.9138; note cites a crossing rule 0.9310 | cut by the first crossing 0.9198; note cites a crossing rule 0.9753 | **holds** |
| Q2 | h 0.9922; e 0.5547; gap 0.4375 | h 0.9677; e 0.5759; gap 0.3918 | **holds** |
| Q3 | gap 0.3619 | gap 0.3978 | **holds** |
| Q4 | e 0.9688; h 0.0547 | e 0.9684; h 0.0516 | **holds** |
| Q5 | gap 0.4520 | gap 0.5035 | **holds** |
| Q6 | gap 0.4634 | gap 0.4150 | **holds** |

**All six hold, the bet `Q6` among them.** Each clause was drawn from pass 1.
So each one holding says the pattern generalised to pass 2 and the rarest
queue's session, not that the drafter foresaw it. That is how `STATUS.md`'s
scoreboard reads the bands `PLAN_WHY.md` set on a development set.

### What it says

- **The hidden half cuts because it leaves the impasse to be explained by a
  conflict.** Every first call is told the engine could not decide its ticket.
  - **Told that the base is empty**, the model mostly says the engine has no
    rule yet, and writes the governing rule's region.
  - **Told only that the base is not shown**, it supposes the engine holds rules
    like the manual's. It finds the ticket in the governing rule and in a
    crossing rule of another queue, and reads the impasse as their conflict.
- **The cut is how it settles that conflict by containment.** It writes the
  governing region cut by the crossing rule, a draft inside both, and its note
  says so. The other settlement is the governing rule with sides declared. That
  is how most of the hidden half's whole answers end.
- **The same link holds where the conflict is rarer.**
  - **Under the empty base**, the answers that name a conflict between two rules
    are the ones that cut.
  - **Beside the empty base**, the overlap clause makes some answers doubt it,
    and those are the cuts. That is what `HV-e` measured.
- **What the reading does not say.** These are codes of what the model writes,
  and *"the model's explanations are not its reasons"* (`EXTERNAL_REVIEW.md`
  §2). They say which account each answer gives, and that the account goes with
  the class on a held-out set. They do not say that the account caused the
  class.

### What it does not settle

1. **Which of the hidden half's two sentences does it**: that the base is not
   shown, or that the rule is for this ticket. Calls.
2. **Whether telling the first call why the engine stopped closes the gap.** A
   text a blind loop can send, which says the engine holds no rule like the
   manual's or names what it could not decide, set beside v1c in a loop, is a
   plan with calls.
3. **The rarest queue.** The clauses pool its seven tickets with the rest of
   `T`.

---

## Files

```
results_halves/sample.json      Stage A: the checks, the design with every ask and its digest, the
                                sessions' orders, the texts, each ticket's governing rule, the
                                references
results_halves/ask_smoke.json   Stage B's smoke run: two tickets of each arm
results_halves/ask_pass1.json   Stage B's pass 1: 544 asks, every attempt with its provider, finish
                                reasons and tokens, every answer whole with its reasoning
results_halves/ask_pass2.json   Stage B's pass 2: the same asks in another order
results_halves/ask_oncall.json  Stage B's rarest queue's session: the 28 prompts at T₇, four times
                                each
results_halves/score.json       Stage C: the six verdicts with their parts, errors and passes, and
                                HV-g
```

The bills, the supervisor and its logs are kept outside git.
