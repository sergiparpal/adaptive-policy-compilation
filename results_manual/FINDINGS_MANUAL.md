# The policy, given to the proposer at three levels — findings

Record opened on October 21, 2026, under [`PLAN_MANUAL.md`](../PLAN_MANUAL.md).
The plan, its package, Sergi's signature of §0, every record below and these
findings reached `main` in pull request #155. Sergi signed §0 on 2026-10-21,
before any figure below existed, in a commit of its own: `d65bdf8` on `main`.

Every record names in its `_env` the commit of the branch it was written on, as
that commit was made and pushed. The rebase merge of #155 gave each of those
commits a new hash on `main`. Each pair below has the same subject, the same
tree and the same `git patch-id --stable`, and the GitHub API names #155 behind
every `main` commit:

| record | written from, on the branch | the same commit on `main` |
|---|---|---|
| `sample.json` | `02bbcd9`, the signature | `d65bdf8` |
| `compile_smoke.json` | `ac9f5f9`, the commit of Stage A's record | `2d914c8` |
| `compile_session.json` | `347244b`, the commit of the compile smoke | `c06d524` |
| `loop_smoke.json` | `bffe539`, the commit of the compile session | `a1573ad` |
| `loop_L{0..3}_r{1..3}.json` | `61e4b5c`, the commit of the loop smoke, all twelve | `54034dc` |
| `score.json` | `a654db7`, the commit of the twelve runs | `80c60ad` |

All of them carry one code digest, `430fa47dbaf069b8`, with `code_dirty`
false. That digest identifies the code that wrote them, and it is the one
`main` computes after the merge. Eleven of the
twelve loop records say `git_dirty: true`: each found the earlier runs' records
written and not yet committed, the case `harness/provenance.py` describes for
records written back to back. **This record owns every figure in it.**

**All three stages ran on 2026-10-21, and the six rows are adjudicated: `G-a`,
`G-c` and `G-d` hold; `G-b` and `G-e` are refuted, thinly, and `G-f` is
refuted.**

- Handed the policy, the model compiles it in one answer: the 29 rules
  exactly, and the prose manual to 0.9929 of the space.
- The loop, with the same texts in its prompt, compiles a base that decides
  about a third of the space, and with the rules in front of it the proposer
  still partitions.
- The catalogue of what each queue is for buys nothing on the two queues no
  loop base had routed to, and it lowers the proposer's choice of queue at the
  escalations.
- **What the loop lacked was not knowledge.**

The smoke runs' answers enter no row.

**Three readings Stage C left free were read POST-RUN on 2026-10-22**, in their
own section below. About half of the gap in crossing between the prose and the
rules is how broad the proposer writes. The dropped declarations decide
nothing. `SECURITY_INCIDENT` was lost under the prose to ordinary rules, none of
which excludes the keyword.

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Every figure of Stage A
> was computed while drafting, and §0 declared it so. The free stage gave it a
> record. Zero API calls.

---

## Stage A — the checks and the references

**What was run.** `python3 -m manual.sample`, on 2026-10-21, with
`PYTHONHASHSEED=0`, on a clean tree at the signature's commit. The record is
[`sample.json`](sample.json).

**The blocking checks passed before anything was computed.**

- **`G-g1`.** The hidden policy, written as a compile answer and installed by
  `manual/compile.py`, gives back `rung2/hidden_priority.py`'s 199 edges pair
  by pair, refuses none, and scores 1.0000 on both surfaces. Its first-match
  reading and `measure` agree, and listed in reverse it scores 0.4232 over the
  space. Through this plan's instrument, `PLAN_REUSE.md`'s three records give
  back `W-d`'s figures, `K-a`'s v1 baselines and each record's
  `proposal_action_accuracy`, and they agree on every corpus label. The suite
  was green, 2,047 tests.
- **`G-g2`.** The three texts are §5's, by digest. The rules are rebuilt from
  `HIDDEN_DSL` character for character and parse back. The prose's omissions
  cost nothing, and every prompt is its level-0 prompt plus the manual's block.
- **`G-g3`.** The compile path runs from parse to score, and the order of Stage
  B is rebuilt from `ORDER_SEED`.
- **`G-g4`.** Signed.

**Every figure §0 lists as seen while drafting comes back**, so §0 needs no
erratum.

- **`PLAN_REUSE.md`'s three bases.**
  - Over the space: 0.30625, 0.29509 and 0.55357, and beyond the keyword
    0.3125, 0.3464 and 0.3696.
  - On the corpus: 0.4035, 0.4470 and 0.5245.
  - `K-a`: 1, 1 and 13/16.
  - The recall of `ACCOUNT_MANAGER` and of `T3_ENGINEERING` is 0 on both
    surfaces.
  - The proposer was right on 0 of 13 `ACCOUNT_MANAGER` escalations and 0 of 12
    `T1_GENERAL` ones.
- **The hidden policy** reads 1.0000 and its `K-a` is 1/13.
- **§5.3's masses** are recomputed rule by rule.

---

## Stage B — the calls

**Every call ran on 2026-10-21, with reasoning off, at
`deepseek/deepseek-v4-flash`**, behind the key check and `G-g1` to `G-g3` each
time. The order was §2.5's.

### B1, the manual compiled once

**The smoke run**, [`compile_smoke.json`](compile_smoke.json), 16:04 to 16:06
UTC, asked each level once.

- All four answers parsed on their first attempt, holding 22, 23, 25 and 29
  rules for levels 1, 0, 2 and 3.
- All four ended `stop`, with 1,651 to 2,160 completion tokens against a cap
  of 16,000 and no reasoning token.
- Relace served levels 1 and 0, and Baidu levels 2 and 3.

**The session**, [`compile_session.json`](compile_session.json), 16:12 to 16:21
UTC, asked five passes over the four levels.

- **All 20 asks are valid.** Level 3's five answers hold 29 rules each, and the
  others 15 to 37.
- **Nineteen parsed on their first attempt.** The twentieth, pass 3 at level 0,
  ran its first attempt into the cap: `finish_reason` `length` at 16,000
  completion tokens, with 253 rules begun. Rung 2's retry, without JSON mode,
  parsed into 15 rules. §0 counts an ask as one call with rung 2's retries, so
  it is valid, and both texts are in the record.
- **Baidu answered 20 of the 21 attempts**, and Relace one, at level 1.

### B2, the loop with the manual in its prompt

**The smoke run**, [`loop_smoke.json`](loop_smoke.json), ran 20 cases at level 3
in 40 seconds.

- It had 12 escalations, each answered on its first attempt, ending `stop`,
  and every proposal parsed into a rule.
- **Of the 9 edges the proposer declared, 8 cited the manual's own rules**,
  `H10` to `H28`, which are not rules of the base. The engine dropped them as
  outside the neighbourhood, as rung 2 drops any identifier the list did not
  show.
- Sergi chose to run as signed: §4's rule 5 forbids adjusting the prompt once
  a smoke run has been read, and §6.3 counts the translation as part of what is
  measured.

**The twelve runs**, [`loop_L{0..3}_r{1..3}.json`](.), were run by Sergi in his
terminal, back to back in §2.5's order, between 16:40 and 17:58 UTC.

- **There were 790 escalations**, from 12 in L₁ r1 to 136 in L₃ r2.
- **Every proposal parsed**: 788 on the first attempt, and two on the second.
- **26 rules were rejected**, every one because it did not match the ticket
  that gave rise to it. **23 of them were at level 2**: 1, 12 and 10 in its
  three runs. Two were at level 3 and one at level 1. *The commit that added
  the runs said 22 at level 2. It is 23, and this record owns the figure.*
- **At level 3 the proposer again declared against the manual's own rules.**
  29, 26 and 6 declarations were dropped as outside the neighbourhood. No other
  level had one.
- **Baidu answered 670 of the 792 attempts.** GMICloud, StreamLake, Relace,
  DeepInfra, SiliconFlow, Azure and Parasail answered the rest, under one model
  name (§6.10).

---

## Stage C — the six adjudications

**What was run.** `python3 -m manual.score`, on 2026-10-21, with
`PYTHONHASHSEED=0`, from the twelve runs' commit on a clean tree. `G-g1` to
`G-g4` passed again, with the suite green. Nothing was missing: twenty valid
asks and twelve runs. The record is [`score.json`](score.json).

**Every statistic is a fraction of counts, compared with its line exactly.**
The record keeps each as a fraction beside its float.

| row | statistic | line | reading | the asks or runs | verdict |
|---|---|---|---|---|---|
| G-a | the median over C₃'s valid asks of `space` | ≥ 0.95 | **1.0000** | five asks, each at 1 | **holds** |
| G-b | C₁'s median mean recall of `ACCOUNT_MANAGER` and `T3_ENGINEERING` over the space, less C₀'s | ≥ 0.10 | **−0.0127**, from **0.3465** and **0.3592** | C₁ 0.0779 to 0.5036; C₀ 0.2233 to 0.5169 | **refuted, thin** |
| G-c | the median over L₃'s runs of `K-a` | > 0.50 | **0.7349** | 0.7439, 0.6667 and 0.7349 | **holds** |
| G-d | C₃'s median `space`, less the median over L₃'s runs of `space` | ≥ 0.10 | **0.6222**, from **1.0000** and **0.3778** | L₃ 0.3339, 0.3952 and 0.3778 | **holds** |
| G-e | L₂'s median `corpus`, less L₀'s | ≥ 0.10 | **0.0265**, from **0.4810** and **0.4545** | L₂ 0.401, 0.481 and 0.526; L₀ 0.212, 0.543 and 0.4545 | **refuted, thin** |
| G-f | `prop(L₁) − prop(L₀)`, each pooled over its three runs | ≥ 0.10 | **−0.1909**, from **0.3301** and **0.5210** | L₁ 34 of 103; L₀ 62 of 119 | **refuted** |

`G-g` is reported, and everything below that is not in the table is its.

**The drafter expected `G-a`, `G-d` and `G-e` to hold and the other three to
be refuted, and got four of the six.** The misses are `G-c`, the row the
drafter trusted least, which held, and `G-e`, which was refuted.

**`G-b` and `G-e` are thin.**
- **`G-b`**: one ask of either arm, in place of its median, would put the row on
  the other side of the line. That is C₁'s ask at 0.5036, or C₀'s at 0.2233.
- **`G-e`**: so would L₀'s first run, at 0.212.

### Compiled once: what each level buys

Medians over the five asks of each level.

| level | `space` | beyond the keyword | the keyword's half | `corpus` | `ACCOUNT_MANAGER`, space | `T3_ENGINEERING`, space | `K-a` |
|---|---|---|---|---|---|---|---|
| C₀, the names | 0.5793 | 0.4086 | 0.7500 | 0.4445 | 0.181 | 0.538 | 0.0526 to 0.0714 |
| C₁, the catalogue | 0.5732 | 0.3965 | 0.7500 | 0.4185 | 0.282 | 0.411 | 0.0278 to 0.1053 |
| C₂, and the prose | 0.9929 | 0.9857 | 1.0000 | 0.9920 | 0.942 | 1.000 | 0.1304 to 0.1579 |
| C₃, the rules | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.000 | 1.000 | 1/13, each |

- **The rules are transcribed, every time.** All five answers reproduce the 29
  hidden rules to the extension and queue, and the derivation gives back the
  199 edges in each.
- **The prose loses three quarters of a hundredth, and it loses it where its
  words are vaguest.**
  - **Every one of the five asks loses the same 960 points of `H14`'s 6,240**,
    *a business client with muchisimos tickets*. Summed over the five, that is
    80 of the region's 245 corpus cases.
  - **The other losses are each one ask's.** One ask, at 0.9583 over the space,
    also lost the defaults' whole region, `H28`'s and `H29`'s 4,640 points.
    Another lost 20 points of `H23`'s.
  - **Every other region came back whole in every ask**, so §5.3's other vague
    words were read as the policy means them.
  - **Each answer reproduces 14 or 15 hidden rules exactly.**
- **The catalogue buys nothing over the names**: 0.5732 against 0.5793 over the
  space, and the two rare queues no better (`G-b`). It moves recall between
  queues. `T1_GENERAL` rises from 0.046 to 0.513 over the space, and
  `T2_TECHNICAL` falls from 0.229 to 0.131.
- **No answer listed a rule above one it strictly contains with another
  queue**, and no derived edge was refused. So in all 20 asks the engine's
  reading and a first-match reading of the list are the same figure (§6.3).
- **Every compiled base crosses.** Even the names alone give `K-a` near 0.06,
  near the hidden policy's own 1/13. Asked for a whole policy, the model writes
  defaults with exceptions over them, at every level.
- **The names alone put `ONCALL_ESCALATION` right on every point of its region,
  in every ask.** No base the loop has written, at any level, has done that.

### The loop: what each level buys

Each run in §2.5's order, r1, r2 and r3. The loop's figures are its final base,
read whole.

| level | `space` | median | `corpus` | median | `K-a` | `prop`, pooled |
|---|---|---|---|---|---|---|
| L₀, the names | 0.15, 0.3571, 0.4101 | 0.3571 | 0.212, 0.543, 0.4545 | 0.4545 | 1, 1, 1 | 62 of 119, 0.5210 |
| L₁, the catalogue | 0.5412, 0.5882, 0.4495 | 0.5412 | 0.3835, 0.426, 0.31 | 0.3835 | 1, 0.5652, 0.3167 | 34 of 103, 0.3301 |
| L₂, and the prose | 0.3301, 0.3095, 0.369 | 0.3301 | 0.401, 0.481, 0.526 | 0.4810 | 0.3182, 0.439, 0.4857 | 164 of 245, 0.6694 |
| L₃, the rules | 0.3339, 0.3952, 0.3778 | 0.3778 | 0.6475, 0.4995, 0.655 | 0.6475 | 0.7439, 0.6667, 0.7349 | 183 of 323, 0.5666 |

- **With the policy in its prompt, the loop's base decides 0.3778 of the
  function**, against the 1.0000 the same text compiles to in one answer
  (`G-d`). The prose gives 0.3301, against 0.9929. **Where compiling once buys
  the most, the loop keeps the least of it.** Taking the median of each level,
  compiling once is ahead by 0.6222 with the rules and 0.6628 with the prose,
  and by 0.2222 with the names and 0.0320 with the catalogue.
- **Where tickets arrive the rules help, and the prose barely does.**
  - L₃'s bases decide 0.6475 of the corpus at the median, the highest of any
    level. That is reported.
  - L₂'s decide 0.4810 against L₀'s 0.4545 (`G-e`, refuted thinly). L₀'s three
    runs span 0.212 to 0.543 between them, wider than any gap the levels make.
- **The catalogue lifts the space and lowers the corpus.** Its runs decide the
  keyword's half better than any other level's: 0.75, 0.75 and 0.6062 of it.
  On the arrivals they decide less than the names do.
- **The loop's losses are where `U-d` put them.**
  - **The keyword's half of the space is lost at every level but the
    catalogue's**: 0.1 to 0.3435 of it under the names, 0.0681 to 0.2 under the
    prose, and 0.1 to 0.3271 under the rules.
  - **The hidden policy's top layers go with it.** Summed over L₃'s three runs,
    `H01`'s region is 91% lost over the space, `H04`'s 90% and `H07`'s 86%, and
    `H14`, `H17` and `H26` are lost whole.
  - **A broad rule written for a common ticket decides its exceptions before
    any of them can escalate**, and the manual does not stop the proposer
    writing it.
- **A base that covered the whole space stopped impassing.** That happened
  at case 401 and case 367 under the names, at 658 and 162 under the
  catalogue, and at 1,799 under the prose. Under the rules it never happened.

### The partition

**`G-c` holds: with the 29 rules in front of it, the proposer still
partitions**, `K-a` 0.7439, 0.6667 and 0.7349. That is `IDEAS.md`'s stronger
reading: the partition belongs to the elicitation and not to what the model
knows.

- **Every compiled base crosses**, at every level, with `K-a` between 0.0278
  and 0.1579 (above).
- **The prose made the loop cross more than the rules did.** L₂'s runs read
  0.3182, 0.439 and 0.4857, all under `K-a`'s line, against the rules' 0.67 to
  0.74.
- **Under the names it partitioned completely**, 1 in all three runs, as in
  `PLAN_REUSE.md`'s.
- **So the form the knowledge comes in moves the partition, and a list of
  rules moves it least.** These runs cannot say why.

### The two classes, and the rarest

- **`ACCOUNT_MANAGER` is a matter of knowing the policy, not the queue's
  purpose.**
  - With the prose, the proposer named it right on 57 of its 63 escalations,
    and L₂'s bases route 0.854, 0.837 and 0.562 of its region over the space to
    it.
  - With the catalogue, 3 of 16, and its bases 0, 0.389 and 0.292.
  - With the names, 2 of 14.
  - With the rules, 16 of 31, and its bases 0.467, 0.543 and 0.465.
- **`T3_ENGINEERING` stays low in the loop at every level**: 0 of 4 escalations
  under the names, 1 of 14 under the catalogue, 9 of 24 under the prose and 8
  of 36 under the rules. Its recall over the space is at most 0.308 in any run,
  where every compiled answer at level 2 or 3 gets it whole.
- **`ONCALL_ESCALATION` is named and hardly ever compiled.**
  - With the rules, the proposer named it right on all 9 of its escalations,
    and with the prose on 6 of 9.
  - Afterwards, the rules decided a later `ONCALL_ESCALATION` ticket right once
    in the six runs of those two levels, in L₂ r2.
  - Under the names none of its 7 tickets escalated, as in every
    `PLAN_REUSE.md` run (`U-d`).
  - Compiled once, every ask at every level put the class right on every point
    of its region.
- **`SECURITY_INCIDENT` went the other way under the prose.** In L₂'s runs the
  rules decided 8, 15 and 20 of the class's 20 tickets as they arrived, and
  none of them right. Under the catalogue they decided 20, 20 and 17, and all
  of them right.

### The proposer's choice of queue

**`G-f` is refuted: with the catalogue the proposer picked the right queue on
0.3301 of the escalations, against 0.5210 with the names alone.**

- **`T2_TECHNICAL` carries most of the fall**: 14 of 36 under the catalogue,
  37 of 42 under the names.
- `T1_GENERAL` rises, from 1 of 18 to 5 of 15.
- **The escalations differ in mix between the levels** (§6.6), so a part of the
  fall may be which tickets escalated rather than which queue was chosen.

**Handed the rules, the proposer applies them at 0.5666**, 183 of 323. That is
against the 1.0000 at which it transcribes them.

- `T3_ENGINEERING` is 8 of 36 and `T2_TECHNICAL` 67 of 114.
- With the prose it is right more often, 0.6694.

**So deciding one ticket with the policy in the prompt is not transcribing the
policy.** Every one of those escalations showed the proposer a screen of
neighbouring rules, and `PLAN_SCREEN.md` measured that a screen pulls the
model's answer to its commonest action. These runs do not separate the two.

### The date, and the providers

**L₀ against `PLAN_REUSE.md`'s runs of 2026-09-30**, the same protocol three
weeks apart:

| figure | 2026-09-30, three runs | 2026-10-21, three runs |
|---|---|---|
| `space`, final base | 0.3063, 0.2951, 0.5536 | 0.15, 0.3571, 0.4101 |
| `corpus`, final base | 0.4035, 0.4470, 0.5245 | 0.212, 0.543, 0.4545 |
| online e2e | 0.3935, 0.44, 0.513 | 0.206, 0.535, 0.4375 |
| `prop`, pooled | 68 of 135 | 62 of 119 |
| CONFLICTs | 30, 5, 12 | 0, 0, 11 |
| `K-a` | 1, 1, 13/16 | 1, 1, 1 |

The medians are close and the runs spread widely on both dates. Nothing here
separates a drift from the spread.

**The providers.** B1's session went almost all to Baidu. B2's 792 attempts
went to eight providers under one name, 670 of them Baidu. These records keep
each attempt's provider. No row is read by provider, and with this mix none
could be.

### What the verdicts say

- **What the loop lacked was not knowledge.** The same model, handed the same
  text, writes the policy in one answer: exactly from the rules, and within a
  hundredth of the space from a manual with a real manual's vague words. Put
  in the loop's prompt, the same text yields a base that decides about a third
  of the function, and with the rules the proposer still partitions.
  `ARBITRATION_REPORT.md` §5 left three candidates for the partition, and this
  plan added knowledge as a fourth. On this model and these texts knowledge is
  ruled out. The three of §5 remain: the framing of one ticket and one rule,
  the model, and elicitation by rule-writing in general.
- **Knowing what a queue is for is not knowing the policy.** The catalogue
  buys nothing compiled and costs the loop's choice of queue. The prose fixes
  `ACCOUNT_MANAGER`'s choice. The rest of the material problem lives in what
  the loop does with a right choice: a broad rule, an exception never asked
  about, a name never compiled.
- **The authority channel exists outside its perfect limit, and only in one
  shape.** Compiled once, a real manual buys nearly the whole function. Through
  the impasse loop, it buys the arrivals almost nothing (`G-e`).

### What Stage C does not settle

1. **Why the loop partitions with the policy in front of it.** v1's framing,
   one ticket and one rule, the base shown at every impasse, or a proposer
   writing each rule's effective region: these runs do not separate them. The
   prose made it cross more, which a reading of the rules it wrote could
   explain. A run of the loop under v2 with the manual would test the framing.
   Calls.
   **[NOTE 2026-10-22] The reading is done, POST-RUN** (*Three readings Stage
   C left free*, below). About half of the gap is breadth: with the rules the
   proposer writes narrower rules, and narrow rules seldom meet another
   queue's. A birth's place against its ticket's own rule carries little of it.
   The run under v2 is still open.
2. **Why the proposer applies the rules at 0.5666.** Asking the escalated
   tickets again with the manual and no screen would separate the screen's pull
   from the application itself. Calls.
3. **What level 3's dropped declarations cost.** 61 declarations against the
   manual's own rules never reached the base. A reading of what they would
   have decided is free on the records.
   **[NOTE 2026-10-22] Nothing, read POST-RUN** (below). Translated into the
   rules the proposer was shown, they change no decision of any final base.
4. **`SECURITY_INCIDENT` under the prose.** Which rule decided the class's
   tickets wrong, and when it was born, is free on the records.
   **[NOTE 2026-10-22] No one rule, read POST-RUN** (below). The class was
   decided by ordinary rules written for other tickets, none of which excludes
   the keyword. Under the catalogue 81 of 102 rules do.
5. **One manual, one model, one prompt, one date, three runs a level**, with a
   spread between runs as wide as most of the gaps between levels, and eight
   providers behind one name.

---

## Three readings Stage C left free — POST-RUN

> **POST-RUN.** Asked for on 2026-10-22, after Stage C, and run the same day.
> `manual/readings.py` wrote its twelve-clause expectation in its docstring
> and was committed before the first run. It read the twelve loop records and
> `score.json`, and rebuilt every run with `edges/rebuild.py`. Four gates
> stood before any write:
> - every run rebuilds to its record, arrival by arrival and on both surfaces;
> - the hidden rules' regions partition the space, and every arrival's rule is
>   the first it matches;
> - every birth's declarations come back from its record in the order the
>   answer gave them;
> - two routes give each run's `K-a`, its class counts, and an untranslated
>   copy of its record.
>
> **Three of its clauses failed on its own convention**, below.
> `manual/after_readings.py` read the same births again where `K-a` reads,
> and two things the first record showed beside its clauses. It was written
> after that record, with most of its figures first computed in a scratch
> exploration, so **none of its figures is a bet**.
>
> Not signed rows; no verdict moves. Zero API calls. The records are
> [`readings.json`](readings.json) and
> [`after_readings.json`](after_readings.json).

### 1. Why the prose made the loop cross more than the rules did

**The classes as drafted read the wrong surface.** The first reading set every
birth `K-a` reads against its ticket's rule, the hidden rule that governs the
ticket it was born on:
- `region`: inside the part of that rule where it decides under first match;
- `rule`: inside the rule as written, and reaching the regions above it;
- `beyond`: outside it.
It read the three over the whole space. `K-a` reads the half without the
keyword, and only `H01` to `H03` decide the other half. So a rule that does not
exclude the keyword reaches their regions, and it can never fall in `region`.

No birth of L₀, L₂ or L₃ did, and A1 to A3 fail by construction. L₁'s 16 are
rules that exclude the keyword. `IDEAS.md`
carried the lesson from `blind/yielding.py`, *read a reading on the plan's own
surface first*, and the drafter did not apply it. The record stands as written.

**Read where `K-a` reads**, with every extension cut to the half without the
keyword. Pooled over each level's three runs:

| level | births read | `region`, cross | `rule`, cross | `beyond`, cross | `K-a`, pooled |
|---|---|---|---|---|---|
| L₀, the names | 103 | 9, 0 | 56, 0 | 38, 0 | 1 |
| L₁, the catalogue | 94 | 16, 1 | 42, 21 | 36, 29 | 0.4574 |
| L₂, and the prose | 205 | 44, 22 | 110, 65 | 51, 37 | 0.3951 |
| L₃, the rules | 279 | 107, 24 | 148, 48 | 24, 9 | 0.7097 |

- **With the rules, more births stay inside their ticket's region**: 107 of
  279, against 44 of 205 with the prose. Fewer reach beyond their ticket's
  rule: 24 against 51, the one clause about the classes that held as drafted
  (A4).
- **But the classes' mix carries little of the gap.** The gap between the two
  pooled `K-a` is 0.3146.
  - Read with L₂'s rates on L₃'s mix, the mix carries 0.1184 of it.
  - Read with L₃'s rates on L₂'s mix, it carries 0.0799.
- **L₃'s births cross less in every class**: 22 of 107 against 22 of 44 in
  `region`, 48 of 148 against 65 of 110 in `rule`, and 9 of 24 against 37 of 51
  in `beyond`.

So the candidate Stage C named, *a proposer writing each rule's effective
region*, is not what moves the partition. More of L₃'s births do stay inside
their ticket's region, and that mix carries about a tenth of the gap.

**Breadth carries about half of the gap.** Breadth is a birth's points off the
keyword. The bands are cut at the quartiles of L₂'s and L₃'s births pooled:
240, 840 and 1,680 points.

| points off the keyword | L₂, births and cross | L₃, births and cross |
|---|---|---|
| 240 or fewer | 19, 5 | 108, 15 |
| 241 to 840 | 45, 22 | 95, 26 |
| 841 to 1,680 | 71, 48 | 39, 13 |
| more than 1,680 | 70, 49 | 37, 27 |

- **Crossing rises with breadth at both levels**, and L₃ writes most of its
  births in the two narrowest bands, L₂ most of its in the two broadest.
  The median birth spans 640 points off the keyword with the rules, and 1,680
  with the prose.
- **The bands' mix carries 0.4743 of the gap on L₂'s rates, and 0.4681 on
  L₃'s.**
- **The other half is inside the bands.** In the three narrower ones L₃'s
  births cross less than L₂'s of the same breadth. The rules they could meet
  are L₃'s own narrower ones, and these readings do not separate the two.
- **Crossing is mostly partial overlap at both levels**, not a default and its
  exception. Over the space, 18 of L₂'s 124 crossing births are nested in every
  rule they meet or contain it, and 16 of L₃'s 81.

So the form the knowledge comes in moves about half of the partition through
how broad the proposer writes. The list of rules makes it write narrow rules.
Narrow rules meet fewer rules of another queue, so the base partitions.

### 2. What level 3's dropped declarations would have decided

**The 61 declarations** are 29, 26 and 6 in L₃'s three runs: 39 say the new rule
beats a hidden rule, and 22 that it loses to one. They cite 24 of the 29.

**Against the policy, most say nothing.** 22 cite a rule whose extension the
declaring rule never meets, and 12 one of its own queue: 34 of 61 are inert or
idle (B1 holds). Of the 27 at stake, 20 have a strict better side over the
points the two share, and 9 point at it (B2 fails). On the other 7 neither
queue is ever right there.

**Whose declarations were right, read after the record.** They split by the
queue the declaring rule names:

| the declaring rule's queue, for its own ticket | rules | at stake | point at the better side | miss it | neither ever right |
|---|---|---|---|---|---|
| right | 1 | 6 | 6 | 0 | 0 |
| wrong | 8 | 21 | 3 | 11 | 7 |

- **The one right rule is `R0053` of L₃ r1**, an `ONCALL_ESCALATION` rule born
  on a ticket `H05` governs. It declared itself above six lower hidden rules, and
  each points at the better side.
- **Most of the misses are one rule, `R0112` of L₃ r2.** It is also an
  `ONCALL_ESCALATION` rule, born on a ticket `H08` sends to `T2_TECHNICAL`. It
  declared itself above ten hidden rules. It missed seven, and on three neither
  side is ever right.

So the proposer read the list's order, and its declarations went wrong where
the queue it named did. The right side is one rule, so this is a reading and
not a rate.

**Beside the direction, the containment.** In 29 declarations the declaring rule
lies inside the hidden rule it cites, and 25 of those call it the winner, which
subsumption would have made it anyway. 4 call it the loser.

**Translated into the rules the proposer was shown, they decide nothing a base
did not.** The two translations were fixed before any was counted:
- `T1`, the hidden rule as written: 4 of the 61 have one among the rules shown
  (B3 holds), and none more in the base unshown.
- `T2`, its parts, the shown rules of its queue inside its extension: 21 have
  them, and 5 more had them in the base unshown.

Each translated edge was tried at its rule's birth, where the declaration stood:

| translation | declarations | edges | disjoint | accepted | installed | points of the space changed | arrivals changed |
|---|---|---|---|---|---|---|---|
| `T1` | 4 | 4 | 3 | 1 | 1 | 0 | 1 |
| `T2` | 21 | 32 | 24 | 8 | 5 | 0 | 4 |

- **Every final base decides both surfaces exactly as its record's does**,
  under either translation (B4 holds).
- **As the arrivals came, five decisions moved in the six rebuilds**, and one of
  them became right, in L₃ r1 under `T2`.

So the dropped declarations cost nothing. Most were idle or inert. Most had no
rule shown to stand for the hidden rule they cite, and under `T2` the engine
refused 24 of the 32 translated edges as disjoint.

### 3. `SECURITY_INCIDENT` under the prose

The class has 20 arrivals. `H01` governs 9, a business or enterprise ticket with
the keyword. `H02` governs 11, the keyword at severity 2 or less from a free or
pro account.
For each run, r1 to r3:

| level | decided by a rule, right | escalated, named right | keyword rules in the base | rules that exclude the keyword |
|---|---|---|---|---|
| L₀, the names | 20, 0 · 17, 0 · 8, 3 | 0 · 3, 0 · 12, 12 | 0 · 4 · 12 | 6 of 119 |
| L₁, the catalogue | 20, 20 · 20, 20 · 17, 17 | 0 · 0 · 3, 3 | 1 · 1 · 6 | 81 of 102 |
| L₂, and the prose | 8, 0 · 15, 0 · 20, 0 | 12, 12 · 5, 4 · 0 | 12 · 5 · 0 | 0 of 222 |
| L₃, the rules | 16, 0 · 13, 6 · 3, 3 | 4, 0 · 7, 7 · 17, 17 | 4 · 21 · 17 | 0 of 321 |

A keyword rule is one whose extension lies inside the keyword's half.

**Which rule did it: no one rule.**
- **Under the prose, 5, 12 and 8 rules decided the class's tickets wrong** in
  the three runs. None is a keyword rule, and in each run four or five of them
  were born before the class's first ticket, at case 44 (C1, C2 and C3 fail).
- **The one that decided most is `R0003` of r3**: *mobile or dashboard,
  severity 2 or less, not enterprise* sends it to `T2_TECHNICAL`. It was born
  at case 3 and decided 9.
- **No wrong decision met a rule of the class** (C4 holds). What decided them
  stood in no rule of the class's way.

**When, and why there.**
- **The class met bases written for other tickets.** Every rule of the prose's
  bases reaches the keyword's half, since none excludes it. Under the catalogue
  81 of 102 rules do, and under the names 6 of 119.
- **The first arrival with the keyword is case 19 in every run**, a ticket `H03`
  sends to `T2_TECHNICAL`.
  - Under the catalogue it met no rule in all three runs. The proposer named
    `SECURITY_INCIDENT`, wrongly for that ticket, and wrote *the keyword* to
    `SECURITY_INCIDENT`, the whole half. In r1 and r2 that is the base's one
    keyword rule, and it decided all 20 of the class right.
  - Under the prose an ordinary rule that reaches the keyword's half decided
    it, in all three runs. The keyword reached the proposer only with the
    class's own tickets.
- **What the prose's proposer wrote then.**
  - **In r1**, `H01` as the prose states it, at case 44: the keyword from a
    business or enterprise account. It wrote the same rule eight more times.
    Every later `H01` ticket was a CONFLICT, escalated, and was named right. `H02`'s free accounts got a rule of the class
    at case 580, and its pro accounts none. Ordinary rules decided 8 of `H02`'s
    tickets wrong.
  - **In r2**, the same rule narrowed to severity 2 or less, §1's *or* read as
    *and*. It also wrote a rule sending the keyword from a free account at
    severity 2 or less to `T2_TECHNICAL`. That gives part of `H02`'s region to
    the queue §1 gives the remainder.
  - **In r3**, no keyword rule at all. Ordinary rules decided all 20, all
    wrong.
- **Over the space**, of the class's 50,400 points, L₂'s final bases send
  9,260, 1,215 and 0 to the class. They leave 32,740, 20,545 and 2,800 in
  CONFLICT.

So under the prose the class went astray because nothing kept the keyword out
of the ordinary rules. The rules the class did get were §1's sentence, exact or
misread, and they crossed the ordinary rules. The catalogue kept the class by
being wrong once: it sent a ticket of another queue to the class, at a ticket
no rule matched. The same rule matches `H03`'s tickets, whose truth is
`T2_TECHNICAL`, too.

### The expectation, clause by clause

| clause | expected | read | verdict |
|---|---|---|---|
| A1 | births in `region` cross less often than the others, at L₁, L₂ and L₃ | no birth of L₂ or L₃ is in `region` | **fails** |
| A2 | L₃'s births fall in `region` more often than L₂'s | none of either | **fails** |
| A3 | the classes' mix carries more than half of the gap | 0.0831 and 0.0479 | **fails** |
| A4 | L₂'s births reach `beyond` their ticket's rule more often than L₃'s | 51 of 205 against 24 of 279 | holds |
| B1 | at least a quarter of the 61 are idle or inert | 34 of 61 | holds |
| B2 | at least three quarters of those with a strict better side point at it | 9 of 20 | **fails** |
| B3 | fewer than a quarter have a `T1` rule among those shown | 4 of 61 | holds |
| B4 | under either translation, fewer than 1,344 points and 20 arrivals change in every run | none and at most 3 | holds |
| C1 | in each of L₂'s runs one rule decides more than half of the class's tickets the rules decide | 3 of 8, 3 of 15, 9 of 20 | **fails** |
| C2 | that rule routes to `T2_TECHNICAL` | `T1_GENERAL` twice, `T2_TECHNICAL` once | **fails** |
| C3 | and it is a keyword rule | none of the three | **fails** |
| C4 | no rule of the class matched a ticket of it that a rule decided wrong | none did | holds |

**Four of twelve held.**
- A1 to A3 fail on the reading's own convention, above. Read where `K-a` reads,
  after the record, the first two would hold and the third would not.
- B2 bet that a proposer handed the list's order reads it. It does, where its
  rule names the right queue, and most of the declarations at stake came from
  rules that did not.
- C1 to C3 bet that a rule about security, misread, decided the class. It was
  the base's ordinary rules.

The drafter trusted C4 least, then A3 and B1. C4 and B1 held, and A3 failed.

### What these readings do not settle

- **Why the list makes the proposer write narrower rules.** The notes it wrote
  beside each rule might say. Reading them is a codebook's work, and
  `PLAN_WHY.md` says to anchor its patterns.
- **The half of the gap inside the bands**: L₃'s births or the narrower rules
  they could meet. A reading of what each birth's earlier rules span would
  split them. Free.
- **Why the catalogue makes the proposer exclude the keyword and the prose
  does not.** The catalogue names what `SECURITY_INCIDENT` is for and states
  no precedence. The prose states one, *antes que nada*, and the list of rules
  states its order. Rung 2's engine applies neither: only declared edges and
  containment order its rules. Whether the proposer leaves the keyword to a
  precedence it was told about, the notes might say.
- **Whether a loop that kept the keyword out of its ordinary rules would keep
  the class under the prose.** That is a run, with calls and a plan of its own.

---

## Files

```
results_manual/sample.json           Stage A: the checks, the texts and prompts with their
                                     digests, the order of Stage B, the references and
                                     §5.3's masses
results_manual/compile_smoke.json    Stage B1's smoke: one ask a level, every attempt with
                                     its provider, finish reasons and tokens
results_manual/compile_session.json  Stage B1's session: twenty asks, five passes over the
                                     four levels, every attempt's text kept
results_manual/loop_smoke.json       Stage B2's smoke: twenty cases at level 3
results_manual/loop_L{k}_r{r}.json   Stage B2's twelve runs, PLAN_REUSE.md's layout, with
                                     the level, the texts' digests and the system prompt
results_manual/score.json            Stage C: the six verdicts with every ask's and run's
                                     cells, and G-g
results_manual/readings.json         POST-RUN: every birth against its ticket's rule, the
                                     61 dropped declarations read and translated, the
                                     class's arrivals, the gates, the expectation
results_manual/after_readings.json   POST-RUN, after it: the births on K-a's own surface
                                     and by breadth, the declarations by their rule's
                                     queue, the keyword rule by rule
```
