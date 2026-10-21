# The policy, given to the proposer at three levels — findings

Record opened on October 21, 2026, under [`PLAN_MANUAL.md`](../PLAN_MANUAL.md).
The plan, its package, Sergi's signature of §0 and every record below are in
pull request #155. Sergi signed §0 on 2026-10-21, before any figure below
existed, in a commit of its own: `02bbcd9` on the branch.

Every record names in its `_env` the commit of the branch it was written on:

| record | written from, on the branch |
|---|---|
| `sample.json` | `02bbcd9`, the signature |
| `compile_smoke.json` | `ac9f5f9` |
| `compile_session.json` | `347244b` |
| `loop_smoke.json` | `bffe539` |
| `loop_L{0..3}_r{1..3}.json` | `61e4b5c`, all twelve |
| `score.json` | `a654db7` |

All of them carry one code digest, `430fa47dbaf069b8`, with `code_dirty`
false, and that digest identifies the code that wrote them. Eleven of the
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
2. **Why the proposer applies the rules at 0.5666.** Asking the escalated
   tickets again with the manual and no screen would separate the screen's pull
   from the application itself. Calls.
3. **What level 3's dropped declarations cost.** 61 declarations against the
   manual's own rules never reached the base. A reading of what they would
   have decided is free on the records.
4. **`SECURITY_INCIDENT` under the prose.** Which rule decided the class's
   tickets wrong, and when it was born, is free on the records.
5. **One manual, one model, one prompt, one date, three runs a level**, with a
   spread between runs as wide as most of the gaps between levels, and eight
   providers behind one name.

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
```
