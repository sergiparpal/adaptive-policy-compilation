# PLAN_PROPOSER_1600 — the real proposer, at the budget that discriminates

**Status: drafted by Claude on 2026-08-25, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **No stage runs until
Sergi has signed the rows that govern its output**, and the signature has to land
before any figure named here exists — in its own commit, staged by name.

**This plan exists because `PLAN_PAIRWISE.md` asked its question at the wrong
budget.** P-d was adjudicated at 400 pairs, and `results3/FINDINGS3.md` §10 then
showed that at 400 a perfect chooser, a 70%-accurate chooser and a coin are the
same number. The band was never wrong; the place it was tested was. The budget
curve says where the curve separates, and this plan goes there.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them — the convention `PLAN_ORDER_METRICS.md` adopted after two dead zones, and
which `PLAN_PAIRWISE.md` had to repair mid-flight.

**Every row names its denominator here, before the run.** `PLAN_PAIRWISE.md` §0
did not, for `P-c`, and the denominator had to be chosen afterwards under an
amendment. That is a defect this table does not repeat.

**Every figure below is on one cell**: `hibrido` pool, corpus test split 0 — the
cell every reference line in §3 is measured on. No figure in this plan lives on
any other, and none may be compared to one that does.

| id | claim | denominator | band | refuted by |
|---|---|---|---|---|
| **B-a** | The proposer's correct-direction rate is stable between budgets: at 1,600 pairs it is close to what 400 gave | pairs with a strict better rule under the **space** definition **and** a declared edge — §9's own denominator | `\|rate − 0.6978\| ≤ 0.05` | `> 0.05` |
| **B-b** | The order its edges induce beats what a **free** ranking of the eight queues scores | the order's score on the cell above | `> 0.4824` | `≤ 0.4824` |
| **B-c** | It reaches the projection made from its own measured accuracy | the same score | `≥ 0.4981` | `< 0.4981` |
| **B-d** | Its errors concentrate where they cost most: the direction rate is **lower** on the pairs a queue ranking cannot answer than on the ones it can | the two rates, each on its own side of the split, both reported with their `n` | `rate(unreachable) < rate(reachable)` | `rate(unreachable) ≥ rate(reachable)` |

**Signed by Sergi: ______________________ (date: __________)**

**What the drafter expects, written down so the scoreboard can score it.** `B-a`
holds, `B-b` holds, `B-c` is **refuted**, `B-d` holds. The reasoning is one
sentence: the projection behind 0.4981 flips each direction *independently and
at a uniform rate*, and Stage C measured the proposer's accuracy varying by
queue-pair — so its errors should be correlated, should fall harder on the pairs
that carry the information a ranking does not, and should therefore buy less
order than the same number of independent errors would. `B-d` is that mechanism
stated as a measurement; `B-c` is its consequence. If `B-c` holds and `B-d` is
refuted, the projection was right and this paragraph was wrong.

---

## 1. What is being bought, and what is already paid for

**1,600 pairs, of which 400 already have answers.**
`results2/pair_judgement_learned.json` holds 400 answers sampled uniformly at
seed 17 from the 31,850-pair population.
This plan adds **1,200 more**, drawn uniformly from the remaining 31,450, and
scores the union.

**The union is a uniform sample of 1,600 and that is not a hand-wave**: drawing
`k₁` uniformly without replacement and then `k₂` uniformly from what is left
gives a subset distributed exactly as one uniform draw of `k₁ + k₂`. So the
1,600-point and the 400-point sit on the same population and the comparison
between them is nested, which is what `B-a` needs.

**Cost.** 1,200 calls. Stage D ran 400 in 3,045 s — 7.6 s per call, sequential —
so this is about **2 h 30 min** and cents at `deepseek/deepseek-v4-flash`.

---

## 2. The choice that has to be made at signature time

**Reusing the 400 saves a third of the budget and adds one uncontrolled
variable.** They were asked on 2026-08-24 against a hosted model that can change
underneath a name; the 1,200 would be asked on another date. `PLAN_PAIRWISE.md`
§3 already records that the proposer is not deterministic at temperature 0, and
this adds date to the list of things that are not held fixed.

Two options, and the second is not the drafter's to pick:

- **Reuse.** 1,200 new calls. The nesting is exact and the dates are not.
- **Re-ask everything.** 1,600 new calls, one date, and the 400 become a
  *replication* of Stage D under an identical protocol — which is itself a
  measurement nobody has: how much a proposer's answers move between dates.

The drafter's recommendation is **reuse**, on the grounds that 2 h 30 min against
3 h 20 min is not the constraint and the date variable is small next to what is
being measured. **But the second option buys a figure the first does not**, and
whether that figure is worth 400 calls is a judgement about money, which
`PLAN_PAIRWISE.md` §9 established belongs to Sergi. **§0's bands do not change
either way**; only §7's population does.

---

## 3. Reference figures, with the record that owns each

Nothing here is produced by this plan. **All on `hibrido`, corpus test split 0**,
which is the only cell this plan uses.

| figure | value | what it is | owning record |
|---|---|---|---|
| `born_at` floor | 0.4332 | a budget of zero | `results3/floor_by_pool.json` |
| the proposer at 400 | 0.4080 | what Stage D bought | `results3/declared_order.json` |
| a free queue ranking | 0.4824 | reads no rule; budget-independent | `results3/queue_hierarchy_floor.json` |
| coin on direction @1,600 | 0.4519, sd 0.0182 | the null at this budget | `results3/edge_budget.json` |
| projection @1,600 | 0.4981, sd 0.0155 | 70% accuracy, errors independent | same |
| oracle ceiling @1,600 | 0.5497 | every direction right | same |
| searched order | 0.7678 | best of 65 starts, same cell | `results3/order_search_ls.json` |
| direction rate @400 | 0.6978, se 0.030, n 278 | space definition | `results3/edge_direction.json` |

**Why 1,600 and not some other number.** At 400 those three curves are 0.4533,
0.4471 and 0.4556 against a coin deviation of 0.0239 — one number. At 1,600 they
are 0.5497, 0.4981 and 0.4519 against a deviation of 0.0182: the gaps are about
2.5 deviations each. **The budget is chosen to make the rows adjudicable, and
that choice is made before the rows are signed rather than after they fail.**

---

## 4. Non-negotiable rules

`CLAUDE.md`'s own numbering, so that cross-references point at the right rule.

1. **Do not modify the frozen specification.** If one has a bug, stop and say so.
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A
   signed plan travels alone, staged by name, in its own commit.
3. **Do not parallelise.** The calls are sequential.
4. **Seed 17, no regeneration, and `results/llm_run.json` is read-only.**
   `harness/record_guard.py` guards this plan's destination too; the flag is not
   typed without Sergi asking.
5. **Do not adjust the prompt or the schema.** Not before a recorded result and
   not in this plan at all: the prompt is Stage D's, unchanged, or the comparison
   with the 400 is void.
6. **If the numbers come out badly, report them.** Both this thread's signed rows
   so far came out refuted and the records say so.
7. **The API key goes in the environment.** `eval "$(grep -m1 '^export
   OPENROUTER_API_KEY=' ~/.bashrc)"`, checked with `${#OPENROUTER_API_KEY}`.

And this plan's own, lettered:

A. **Do not touch the constants of the closed thread.** `P_D_MARGIN`, `P_E_BAND`,
   `POSITION_SEED`, `SAMPLE_SEED`, `SHUFFLE_SEED`, `DIRECTION_SEED`,
   `N_DIRECTION_DRAWS`. They belong to adjudicated rows.
B. **Every new record carries `_env`**, and every figure-producing command runs
   with `PYTHONHASHSEED=0` set explicitly.
C. **The scoring code is the closed thread's, called and not copied.**
   `declared_order.topological_order`, `accepted_from`, `reset_declared` and
   `floor` produced the adjudicated figures; a reimplementation here would make
   the 400-point and the 1,600-point incomparable for a reason that has nothing
   to do with the proposer.

---

## 5. Known traps

**5.1 — The nesting is in the sample, not in the shuffle.** `edge_budget` nests
its budgets by shuffling the population once at seed 17 and taking prefixes.
Stage D did **not** use that shuffle: it used `sample_population`, which is
`random.Random(17).sample`. **The two do not agree**, and `random.sample(N, 1600)`
is not a superset of `random.sample(N, 400)`. The extension must therefore be
built as *Stage D's 400, plus 1,200 drawn from the complement* — never by
re-running a sampler at a larger size and hoping.

> **ERRATUM, 2026-08-25, found while implementing §6.** The first half of that
> paragraph holds and holds hard: over this population the shuffle's first 400
> and the sample's first 400 share **not one pair**. The second half is **false
> at this scale**. `random.Random(17).sample(range(31850), 400)` *is* an exact
> prefix of `random.Random(17).sample(range(31850), 1600)` under CPython 3.12:
> both budgets take the selection-set branch of `random.sample`, so they share
> one draw stream and the smaller comes out inside the larger.
>
> **The instruction does not change and neither does anything downstream** — the
> load-bearing word in it was always *hoping*. The nesting is an undocumented
> implementation detail: it disappears as soon as the two budgets straddle the
> branch boundary of the sampler's `setsize` heuristic, which depends on both `n`
> and `k`, and it is not a promise the language makes. `tests/test_pair_sample_1600.py`
> carries the counterexample and the coincidence side by side, and Stage A rests
> on the complement plus `gate_base_is_a_subset`, which checks the result instead
> of trusting the route.
>
> Written by the drafter, before §0 was signed and before any figure of this plan
> existed. No row moves and no band is touched.

**5.2 — The proposer's `no edge` and the oracle's `tie` are different events.**
At 1,600 the oracle offers nothing on 353 pairs, because neither rule is ever
right or both are right equally often. The proposer offers nothing when it names
a third queue or fails to parse — 35 of 400 in Stage D, 8.75%. The two counts
must never be added, shared or compared; each belongs to its own denominator and
`B-a`'s excludes both for different reasons.

**5.3 — The parse-failure rate is a known unknown.** It tripled between Stage C
and Stage D with model, settings and prompt held fixed (2.4% → 8.75%), and
`IDEAS.md` lists the mechanism as unexplained. At 1,200 calls expect on the order
of a hundred, and **do not let that surprise become a reason to change the
prompt**: rule 5.

**5.4 — `B-d` needs both sides of its split populated, and that is checkable
before spending.** The pairs a queue ranking cannot answer are those whose
queue-pair appears with **both** better-rules under the oracle. If the 1,600
leave too few on the unreachable side, `B-d` is unadjudicable and the run should
know that before it starts, not after. §6 makes it a gate.

**5.5 — Reusing the 400 imports Stage D's date.** See §2. Whichever option is
signed, the record states which, and any comparison between the two halves is
labelled with it.

---

## 6. Stage A — extend the sample and check the split (free, no API calls)

**Deliverable.** `rung2/pair_sample_1600.py` → `results2/pair_sample_1600.json`.
New `tests/test_pair_sample_1600.py`.

**What it does.** Reads Stage D's 400 pairs, draws 1,200 more from the complement
at a seed declared here — **`EXTENSION_SEED = 25`**, distinct from every seed the
closed thread used so that no accident makes the two samples share structure —
and writes the union. Then, for each of the 1,600, the oracle's better rule under
both definitions, reusing `edge_direction.better_over_space` and
`better_over_corpus` unchanged.

**Gates, all blocking:**

- the 400 of Stage D are a subset of the 1,600, and appear with the same pair ids;
- the union has exactly 1,600 distinct pairs, all from the 31,850 population;
- the population census still gives 31,850 under the three conditions;
- **`B-d`'s split is populated**: the number of the 1,600 whose queue-pair appears
  with both better-rules is reported, and if either side falls below 100 pairs the
  stage says so and `B-d` is declared unadjudicable **before** any call is made.

**This stage carries no prediction, and that was checked rather than assumed.**
`B-a` and `B-d` are about *the proposer's* rate on these pairs, which needs the
calls; `B-b` and `B-c` are about *the order its answers induce*. Nothing in §0
predicts the population split, the sample, or the oracle's own directions. That
check is here because `PLAN_PAIRWISE.md` §0.1 records two rows lost to skipping
it: **costing no money is not the same as costing no prediction.**

---

## 7. Stage B — the calls (1,200, gated on §0)

**Deliverable.** `rung2/pair_judgement.py --learned --budget 1600 --sample
results2/pair_sample_1600.json` → `results2/pair_judgement_1600.json`.

**Protocol, unchanged from Stage D in every respect that could move a figure:**
same prompt, `deepseek/deepseek-v4-flash`, `temperature=0`,
`response_format={"type": "json_object"}`, `max_retries=2`, sequential, the same
three leaks closed and the same four gates before a call — population, no leak,
balanced presentation order, signature.

**Only the population changes**, and the module already takes it as an argument
everywhere except the sampling step, which is the one thing this plan adds.

**Answers already held are not re-asked** under the reuse option, and the record
marks each row with the date its answer came from.

**Run the smoke path on 20 pairs first** and check the shape before the sweep.

**Cost.** 1,200 calls, about 2 h 30 min. Cents.

---

## 8. Stage C — scoring, and the four adjudications (free)

**Deliverable.** `rung3/declared_order.py --source` the record below →
`results3/declared_order_1600.json`, plus
`rung3/edge_direction.py --source ...` → `results3/edge_direction_1600.json`.

Both modules already do everything this needs; what they gain is a `--source`
flag, and **that is the whole code change** — rule C above.

**`B-a`** comes off `edge_direction`'s agreement block, space definition,
denominator as declared. **`B-b`** and **`B-c`** come off `declared_order`'s order
score on `hibrido` / corpus test split 0, compared against 0.4824 and 0.4981.
**`B-d`** needs one new function: split the agreement denominator by whether the
pair's queue-pair appears with both better-rules, and report the two rates with
their `n`.

**Also record, outside every denominator:** the `try_edge` verdict histogram, the
parse-failure count, the no-edge count, the count of ties, and the direction split
by presentation position — the 203/162 asymmetry Stage D found unexplained, which
at four times the sample is either a real effect or a coincidence that will not
survive.

**And the two figures that make the row readable rather than merely true:** the
coin's own distribution at 1,600 recomputed on this exact sample, and the
projection recomputed at whatever accuracy `B-a` lands on rather than at 0.6978.
A refutation of `B-c` by less than the projection's own deviation is a different
event from one by three of them, and the record says which.

---

## 9. Definition of done

- [ ] Records under `results*/` with `_env`, produced with `PYTHONHASHSEED=0`.
- [ ] Every gate of §6 passed before a call was made.
- [ ] Tests added, whole suite green with `python3 -m unittest discover`.
- [ ] Every figure in prose names its **surface**, its **pool** and its
      **denominator**; every random baseline names its **generator**.
- [ ] A section appended to `results3/FINDINGS3.md`, with a dated erratum
      wherever it corrects something already published — including §10, whose
      projection this plan is the first direct test of.
- [ ] `STATUS.md` updated: the scoreboard gains four rows in the `B` thread, and
      the entry points at the record rather than copying a figure.
- [ ] `IDEAS.md`: the item *what the real proposer scores above 400 calls* is
      closed or narrowed, and whatever this opens is added.
- [ ] Code, records and this plan in **separate commits**; the plan and its
      signature alone in theirs.

---

## 10. What this plan does not do

- **It does not raise the budget to where the channel saturates.** The oracle
  curve is flat from 12,800 pairs on. This measures the proposer where the rows
  are adjudicable, not where the channel stops paying, and a figure here says
  nothing about 12,800.
- **It does not close the gap to search.** Even exhausted and perfect, the
  channel reaches 0.6834 against 0.7678 on this cell. Nothing at 1,600 changes
  that, and a good result here is still a result about a channel that has a
  ceiling below the optimizer's.
- **It does not touch the material problem.** Between a sixth and a quarter of
  the population has no right winner among the two rules shown. No edge fixes it.
- **It does not attack authorship at its source.** That is Stage E of
  `PLAN_PAIRWISE.md`, still specified and still unsigned.
- **It does not change the prompt.** If the answer is that the proposer
  underperforms its own projection, the repair is a different plan and it starts
  from a recorded result, which is rule 5.
