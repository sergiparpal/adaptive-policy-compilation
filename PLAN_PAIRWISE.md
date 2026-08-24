# PLAN_PAIRWISE — declared priority by pairwise judgement

**Status: drafted, unsigned. Two of its five rows are already spent — see §0.1.**
§0 carries prediction bands drafted by Claude on 2026-08-23. Under hard rule 2 of
`CLAUDE.md` a model may draft a band but may not sign it: **no stage runs until
Sergi has signed the rows that govern its output**, and the signature has to land
before any figure named here exists.

**The first draft of this paragraph said Stages A and B "spend nothing and may run
before the signature". That sentence is what spent P-a and P-b**, on 2026-08-24,
at a cost of zero euros and two predictions. The rows predict Stage A's own
output, so licensing Stage A to run unsigned licensed measuring them unsigned.
**Costing no money is not the same as costing no prediction**, and the free stages
are exactly the ones where that is easy to forget. The rule that replaces it:
**a stage does not run before the rows about its output are signed, whatever it
costs.** Stages A and B are free and still gated; C and D are gated twice, by
signature and by the stage before them.

**Commit discipline, and it applies to this file.** `PLAN_*.md` at the root is a
signed plan and **travels alone in its own commit, staged by name**, never
alongside code or results. `.githooks/pre-commit` refuses the accompanied commit;
`--no-verify` is not the way past it. The signature commit adds the signature line
and nothing else.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event; a row landing between its band and its
refutation line is a **dead zone**, which is a drafting defect and not a result
(`STATUS.md` records two of those already, `R-b` and `C-a`). The convention that
prevents it is the one the `D` entry of `PLAN_ORDER_METRICS.md` adopted after
those two: **a band's edge is its own refutation line**, so band and refutation
partition the axis and nothing can fall between them.

**The first draft of this table did not follow it.** P-c banded `> 0.60` and
refuted at `≤ 0.50`; P-d banded `> floor + 0.03` and refuted at `≤ floor`; P-e
banded `≤ 25%` and refuted at `> 40%`. Three open intervals, in a table whose own
preamble promised none. They are closed below. Where a stage also needs a
*separate* threshold to decide whether to continue — P-c does — that threshold is
written as a **kill switch in §9 and not as the refutation line**, because the two
answer different questions: the refutation line asks whether the claim was wrong,
the kill switch asks whether to spend more money.

**The first draft of P-c also left its denominator unnamed, and there are two of
them.** An answer is `correct` (the winner's queue), `wrong` (the loser's) or
`neither` — another queue, off the menu, or unparseable. So "the correct-edge
rate" is either `correct / 170` or `correct / (correct + wrong)`, and the second
is the more flattering. **P-c is adjudicated on the first**, `neither` counting
as a failure, and the row below says so.

The reason is the floor it is measured against, not a preference for severity. A
coin between the two rules shown **always commits**: over 170 pairs it names one
of the two every time and is right on about half, so its rate is 0.50 whichever
way you count it. A model that answers `neither` has not been beaten by the coin
there — it has declined to play. Scoring it on `correct / (correct + wrong)`
compares it on the subset where it committed against a baseline that commits
everywhere, which makes every failure to commit free. `results3/FINDINGS3.md` §3
already records what happens when three denominators travel unlabelled in one
block.

Two things follow, and they are written here rather than discovered later. The
`neither` count is **reported beside the rate**, because a run that fails P-c by
declining to answer and one that fails it by answering wrongly are different
findings. And both rates go in the record — the second labelled as the
non-adjudicating one — so a reader can see the gap instead of taking this
paragraph's word for it.

*Amended 2026-08-24, before Stage C had run and before any figure of it existed.
The instrument was already written when this was settled, which is why the
stricter of the two readings is the one adopted: an author who has seen the
shape of the apparatus but none of its output should not be picking the
denominator that flatters it. Sergi may overrule this in the signature; that is
what signing is for.*

| id | claim | band | refuted by |
|---|---|---|---|
| **P-a** | — | **SPENT before signature, see §0.1** | — |
| **P-b** | — | **SPENT before signature, see §0.1** | — |
| **P-c** | On the hidden policy's labelled pairs (Stage C), the proposer's correct-edge rate **over all 170 pairs, `neither` counting as a failure**, beats a coin between the two rules it is shown | `> 0.60` | `≤ 0.60` |
| **P-d** | On the learned base (Stage D), the order induced by the declared edges beats the hybrid `born_at` floor Stage A measures | strictly above that floor by `> 0.03` | `≤ floor + 0.03` |
| **P-e** | That same order lands **inside** the behavioural cloud of the 65 end orders, not outside it | median pairwise disagreement with the 65 `≤ 25%` of the space, measured on the **same pool** as the 65 | `> 25%` of the space |

**Signed by Sergi: I adopt §0 as drafted, without changes: the
three signable rows — P-c, P-d and P-e — with their bands and their refutation
lines as they stand, and P-c adjudicated on `correct / 170` with `neither`
counting as a failure, as the 2026-08-24 amendment sets it. P-a and P-b are
spent and are not restored. `git diff 44eace3 -- PLAN_PAIRWISE.md` shows only
this line, so no row of the table moved. Stage C may run. (date: 2026/08/24)**

*Three rows remain signable. P-c governs Stage C; P-d and P-e govern Stage D and
cannot be adjudicated unless Stage C clears its kill switch first. Stage A and
Stage B now carry no prediction at all — they are measurement, and §0.1 says why.*

---

## 0.1 The two spent rows — P-a and P-b

**Measured 2026-08-24, before anyone signed them. They cannot be un-measured, so
they are recorded here as outcomes and not restored as predictions.** A band
defended after its figure is known is not a prediction, and redrafting one around
a number already seen is hard rule 6 wearing a different hat.

How it happened, because the mechanism is the transferable part: an audit of this
document ran §6's reproduction gate to check that a correct implementation could
pass it. That gate is built out of `born_at` over both pools and all three
surfaces — which is precisely what P-a and P-b predict. §0's first draft licensed
the run by declaring Stage A free to proceed unsigned. **No API call was spent and
both rows were lost anyway.**

What came out, `puro` against `hibrido`, every figure naming its surface:

| order | surface | `puro` | `hibrido` |
|---|---|---|---|
| `born_at` | full corpus | 0.5115 | 0.4285 |
| `born_at` | corpus test, split 0 | 0.5216 | 0.4332 |
| `born_at` | corpus test, mean of 5 splits | 0.5150 | 0.4315 |
| `born_at` | space | 0.3148 | 0.4257 |
| `born_at` reversed | full corpus | 0.5420 | 0.5165 |
| `born_at` reversed | corpus test, split 0 | 0.5467 | 0.5327 |
| `born_at` reversed | space | **0.5668** | 0.4373 |

Against what the two rows had said: the hybrid `born_at` floor on corpus test is
0.4332 on split 0 and 0.4315 over five, inside P-a's `[0.42, 0.52]` and strictly
below the pure floor; reversed `born_at` over the space, pure, is 0.5668, inside
P-b's `[0.55, 0.58]`. **Neither counts as adjudicated.** `STATUS.md`'s thread
table counts a row only once it has been *signed* and then measured, and these
were measured first — so they belong in no column of it, which is exactly what
being spent means.

**These are audit measurements and no record owns them.** Stage A still has to run
and write `results3/floor_by_pool.json`; until it does, nothing here may be cited
elsewhere in the repository. What Stage A loses is only its status as a test of a
prediction. What it keeps is its whole purpose: giving these figures an owner, a
script and an `_env`.

**One thing the audit settled for free, and it belongs to the record it corrects.**
`ARBITRATION_REPORT.md` warns that of the six probe figures it prints, "the two
figures of the reversed order are the ones left unconfirmed". Both reproduce
exactly: 0.5420 full corpus and 0.5668 space, pure pool. That is an erratum owed
to `ARBITRATION_REPORT.md`, and Stage A's write-up is where it lands.

---

## 1. What this project is, in ten lines

An engine triages support tickets. Eight attributes, eight queues, a **hidden
policy of 29 rules in 8 priority layers** that the system never sees. A cheap
symbolic engine resolves what it covers; on a case it does not cover it escalates
to an LLM, which writes a rule so that next time it does. Rung 1 produced a
learned base of **577 rules** (`results/llm_run.json`).

The finding that organises everything: **the priority of a stratified policy is
not in the shape of the rules.** Not in condition count (an engine loaded with the
*perfect* policy scores 0.5875 under specificity arbitration), not in age, not in
subsumption. Priority is a relation *between* rules and enters only through an
external channel: declaration, feedback or authority.

**The bottleneck is not the mechanism.** Rung 2's hybrid engine (subsumption +
declared edges) executes a perfect author's declaration at e2e **1.0000** over the
corpus. What it never got is material: across eight runs the proposer generated
**2 conflicts, 14 proposed edges, 0 accepted**, and all 14 were rejected for the
same reason (`no_solapan` — the cited rule does not overlap).

This plan attacks that. It does not attack the second material problem
(`T3_ENGINEERING` 66.7% and `ACCOUNT_MANAGER` 64.2% of cases with *no correct rule
at all*), and it does not measure the project's founding question (reuse vs
memorisation). Both are out of scope and stay open.

---

## 2. Vocabulary you must not blur

Every figure in this repository names two things. A figure without both is
unreadable and must not be produced.

**Surface.**
- **corpus** — the modelled arrival distribution, n=2000, seed 17, deliberately
  long-tailed. Answers *what would this achieve in deployment*. Its 2000 draws
  touch 1743 distinct cases, so it cannot certify an optimum.
- **space** — the uniform measure over all **134,400** attribute combinations.
  Answers *is this order the policy*.

They do not rank the same: over the same 2,080 pairs the Spearman between the two
surfaces is **0.34**. A figure on one cannot be reweighted into a figure on the
other.

**Pool.**
- **`puro`** — first-match-wins over a total order, subsumption **off**.
- **`hibrido`** — subsumption as a non-overridable base level, plus a declared
  order on top. This is where declared edges live.

The two are different machines and their figures never chain. Over the 577 learned
rules: bound 0.9010 / searched 0.8530 on `puro`; bound 0.8540 / searched 0.7734 on
`hibrido` (`results3/order_search_ls.json`, `results3/FINDINGS3.md`,
`results3/FINDINGS_AUDIT.md`). **The two pairs do not share a surface and the line
above is not licence to treat them as if they did**: the bounds are over the
**full corpus**, all 2000 cases (`rung3/order_search_ls.py:200`, which passes
`list(range(len(corpus)))`), and the searched figures are **corpus test**. The
0.047 is lost in the *bound*, not in the search: once subsumption prunes, **181 of
the 577 rules match nothing** on train.

**And 0.8530 / 0.7734 are not single numbers off a single run.** Each is the
**mean over the five splits** of that split's best of 65 starts
(`rung3/order_search_ls.py:266`: `statistics.mean([r["ls_test"] for r in pure])`).
Two aggregations stacked, and the plan that cites either has to say which one it
means. The 65 end orders of one split are **65 distinct behavioural machines**:
two of them one train case apart decide 8.36% of the space differently. Comparing
anything against that maximum is comparing it against a winning ticket, not a
level.

---

## 3. Reference figures, with the record that owns each

Nothing below is produced by this plan; it is what the plan is scored against.

| figure | value | surface / pool | owning record |
|---|---|---|---|
| coverage bound | 0.9010 | corpus, `puro` | `results3/FINDINGS3.md` |
| coverage bound | 0.8540 | corpus, `hibrido` | `results3/FINDINGS_AUDIT.md` |
| searched order (LS) | 0.8530 | corpus test, `puro`, **mean of 5 splits, each the best of 65 starts** | `results3/order_search_ls.json` |
| searched order (LS) | 0.7734 | corpus test, `hibrido`, **same double aggregation** | `results3/order_search_ls.json` |
| `born_at` | 0.5216 | corpus **test, split 0 only**, `puro` | `REF` in `rung3/order_search_ls.py`, from `FINDINGS3.md` |
| random (mean of 50) | 0.4227 | corpus **test, split 0 only**, `puro`, **record generator** (trap 5.5) | same |
| `born_at` | 0.5115 | **full** corpus, `puro` | **unofficial probe**, `CHAT_SUMMARY.md` §2.1 |
| random (mean of 50) | 0.4172 | **full** corpus, `puro`, **record generator** (trap 5.5) | **unofficial probe**, same |
| `born_at` | 0.3148 | space, `puro` | `results3/FINDINGS3.md` erratum, `budget_and_balance_ls.json` |
| random (mean of 50) | 0.3768 | space, `puro`, **`random_order` generator** (trap 5.5) | `results3/FINDINGS3.md` erratum |
| `born_at` reversed | 0.5668 | space, `puro` | **unofficial probe**, no record owns it |
| `proposal_action_accuracy` | 0.3877 | 632 escalations, 594 CONFLICT | `results/llm_run.json` → `metrics` |
| subsumption silent error | 0.5312 over 160 of 2000 cases committed | corpus, learned base | `results/FINDINGS.md`, `results3/FINDINGS_AUDIT.md` |
| `born_at`, **`hibrido` pool** | **NOT MEASURED** | — | — |

**That last row is why Stage A exists.** Verified against
`results3/order_search_ls.json`: its rows carry `"pool": "puro"/"hibrido"` but
only greedy and local-search scores. There is a world record and no measurement of
what walking scores. Without it nothing Stage D produces can be scored.

**Which of these an owner already exists for, because the probe block is mixed.**
0.5216 and 0.4227 are the record's (`results3/order_search.json`); 0.3148 and
0.3768 verify exactly against the `FINDINGS3.md` erratum. **0.5115, 0.4172 and
0.5668 have no owning record and no script in the tree** — they come from the ad
hoc probe of `CHAT_SUMMARY.md` §2.1, and `ARBITRATION_REPORT.md` carries the
warning that says so. Stage A gives those three an owner for the first time.

They are an *outcome* of Stage A, never a target — see hard rule 6. Three of them
have now been measured by the audit of 2026-08-24 and are transcribed in §0.1;
that transcription is not an owning record and does not discharge Stage A.

---

## 4. Non-negotiable rules for the agent

Extracted from `CLAUDE.md`; read the original before starting. **The numbering
below is `CLAUDE.md`'s own**, and deliberately: §3, §9 and §11 of this document
cite hard rules by number, and the first draft of this section renumbered them
1–10, which made every one of those cross-references point at the wrong rule.
This plan's own additional constraints are lettered underneath so the two sets can
never be confused.

1. **Do not modify the frozen specification**: `harness/hidden_policy.py`,
   `harness/domain.py`, `harness/dsl.py`, `harness/shadow.py`,
   `harness/cache_baseline.py`. If one has a bug, stop and say so.
2. **Do not fill in or edit `PREDICTION.md`** — Sergi does, by hand — **and a
   signed plan travels alone**, staged by name, in its own commit. That covers
   this file and its signature line.
3. **Do not parallelise the loop.** It is strictly sequential.
4. **Seed 17. Do not regenerate the corpus. Do not overwrite
   `results/llm_run.json`.** It is not a log: it is the learned rule base rungs 3
   and 4 start from, and the proposer is not deterministic even at temperature 0.
   `harness/record_guard.py` refuses it; `--overwrite-record` is not typed without
   Sergi asking.
5. **Do not adjust a prompt or schema before having a recorded result.** This is
   why Stage E cannot start before Stage D has a record.
6. **If the numbers come out badly, report them; do not fix them.** Adjusting
   until the curve looks nice is the exact Goodhart failure this experiment
   studies.
7. **The API key.** `OPENROUTER_API_KEY` lives in the environment, never in a
   file. An `export` in Sergi's interactive shell does not reach yours, and the
   Debian guard in `~/.bashrc` returns early for non-interactive shells. What
   works:
   ```
   eval "$(grep -m1 '^export OPENROUTER_API_KEY=' ~/.bashrc)"
   ```
   Check with `${#OPENROUTER_API_KEY}` (the length). Never print the value.

And this plan's own, lettered:

A. **Do not modify `rung2/engine2.py`, `rung2/proposers2.py` or
   `rung2/hidden_priority.py`.** They are the closed record of rung 2 and their
   figures must keep reproducing. Everything here is **new modules** that import
   them.
B. **Every new JSON record carries `_env`** from `harness.provenance.environment()`,
   written under the `_env` key, following `rung3/order_search_ls.py`. Run every
   figure-producing script with `PYTHONHASHSEED=0` set explicitly and let the
   field record it: `null` means unset, that is, random, and any figure sensitive
   to set iteration order produced with `null` is suspect by construction.
C. **Read `CHAT_SUMMARY.md`'s errata before writing any new analytical
   document.** `ARBITRATION_REPORT.md` §9.8 records that it independently
   re-derived three corrections that document had already made. Do not make it
   three times.

---

## 5. Known traps in the code

**5.1 — Bit order is MSB-first, and getting it wrong fails silently.**
`rung2.engine2.Space` builds masks with `int("".join(...), 2)`, so **case index
`i` lives at bit position `n - 1 - i`**, with `n = 134400`. Verified empirically:
for the first case, the *most significant* bit is set and bit 0 is not.

```python
# case index -> bit
bit = 1 << (space.n - 1 - i)
# bit position -> case index
i = space.n - 1 - position
# lowest-indexed case in a mask: take the HIGHEST set bit
i = space.n - mask.bit_length()
```

An agent that assumes LSB-first will build witnesses from the wrong cases and
every downstream figure will be quietly wrong. **Assert your way out of it**: any
witness case you build must satisfy `rule.matches(case)` for both rules of the
pair. If that assertion ever fails, stop.

**5.2 — `try_edge` has six verdicts, five of them rejections.** The verdict
constants are `rung2/engine2.py:220-225` and the function that returns them is
`rung2/engine2.py:295`: `EDGE_SELF`, `EDGE_UNKNOWN`, `EDGE_DISJOINT`
(`"no_solapan"`), `EDGE_CONTRADICTS`, `EDGE_CYCLE`, `EDGE_OK`. Note that
`EDGE_OK` is also returned when the edge is *redundant* with subsumption but
consistent with it (`engine2.py:305`) — accepted, and it returns **before**
touching `decl_below` / `decl_above`, so it adds nothing to the graph. And **the
validator cannot check that the declared winner is the correct one**: existence,
overlap, non-contradiction and acyclicity are properties of the graph; truth is
not in the graph. A false, well-formed edge goes in without resistance.

**5.3 — `EDGE_CONTRADICTS` has never incremented in any run**, not because the
proposer gets it right but because the situation was never reached. Any conclusion
resting on it rests on a counter nobody has seen work.

**5.4 — `Rule2.render()` deliberately omits `correct_count`.** It is derived from
the oracle. Never show it to the model. The test that keeps that true is
`tests/test_engine2.py:263`, `TestRender.test_does_not_leak_the_right_answer`, which
sets `correct_count = 3` and asserts the string never contains it — **not**
`tests/test_oracle_separation.py`, which only walks import graphs and would not
notice a leak through a rendered string. Keep both passing; they guard different
doors.

**5.5 — There are TWO random-order generators in the tree and they disagree.**
`local_search.random_order(ids, seed)` sorts the ids and shuffles once per seed.
`rung3/order_search.py:345-351` uses a different one: a single `random.Random(17)`
shuffling the rules' **appearance** order fifty times in sequence. Different
sequences, different means. Measured 2026-08-24, pure pool, 50 draws each:

| surface | `random_order`, seeds 0..49 | `order_search.py` generator | the record publishes |
|---|---|---|---|
| corpus test, split 0 | 0.4251 sd 0.0690 | **0.4227** sd 0.0710 | 0.4227 |
| full corpus | 0.4212 sd 0.0706 | **0.4172** sd 0.0711 | 0.4172 |
| space | **0.3768** sd 0.1026 | 0.3864 sd 0.0981 | 0.3768 |

**The corpus figures came from one generator and the space figure from the other.**
No single generator reproduces all three. A stage that prescribes `random_order`
everywhere — as the first draft of §6 did — fails its own corpus gates on a
**correct** implementation and sends the agent hunting for a bug in its pool
construction that is not there. §6 names the generator per row for that reason.

**5.6 — The record's corpus-test references are split 0, not the mean of five.**
`rung3/order_search.py:344` and `rung3/order_search_ls.py:266-274` compute
`born_at` and the random mean on `te0` from `split(corpus, truth, seed=17)` alone,
while the searched orders printed in the same table are means over five splits.
Two index sets in one block, unlabelled. Measured 2026-08-24, `puro`, `born_at`:
**0.5216** on split 0 against **0.5150** as the five-split mean — thirty-three
times §6's tolerance apart. The five-split mean is the more stable statistic and
you may prefer it, but then you are not reproducing 0.5216 and must not report
that you are.

---

## 6. Stage A — the floor by pool (free, no API calls)

**Why.** There is no measurement of what a no-search order scores on the pool
where declared edges actually live. Every later stage needs it.

**Deliverable.** New `rung3/floor_by_pool.py` → `results3/floor_by_pool.json`.
New `tests/test_floor_by_pool.py`.

**Ingredients, all existing:**

```python
from rung3.order_search import load, build_tables, split, subsumption_below
from rung3.local_search import build_masks, score_order, random_order
from rung3.order_search_ls import space_pools, space_truth_masks
from harness.provenance import environment, describe
```

`load()` returns `(corpus, rules, ext, conds)` — the corpus at seed 17 and the 577
rules read from `results/llm_run.json` (read only). Then:

```python
below   = subsumption_below(rules, ext)
matched, undef, truth = build_tables(corpus, rules, conds, below)
pools   = {"puro": matched, "hibrido": undef}      # exactly as order_search_ls does
```

`build_masks(ids, pool, truth, action, idxs)` returns `(M, W, full)`;
`score_order(order, M, W, full)` returns the count of cases won with the right
action. Divide by `len(idxs)`.

**What to score — three order families, two pools, three surfaces:**

| order family | how |
|---|---|
| `born_at` | `ids` sorted ascending by `r["born_at"]` |
| `born_at` reversed | the same, descending |
| random × 50 | **two generators, both reported** — see trap 5.5 and the gate below |

| surface | index set |
|---|---|
| full corpus | `range(len(corpus))` |
| corpus test, split 0 | `split(corpus, truth, seed=17)[1]` — **the record's own index set** |
| corpus test, 5 splits | `split(corpus, truth, seed=17+s)`, `s` in `0..4`; report the mean **and** the per-split values |
| space | masks from `space_pools(ids, conds, action, below)`, normalised by its own `n` |

**Report both corpus-test index sets.** Split 0 is the only one that reproduces
the record (trap 5.6); the five-split mean is the better statistic. Neither
substitutes for the other, and the whole point of this stage is that the label is
on the same line as the number.

**Built-in reproduction gate. Run it first and abort on failure.** These are not
new figures; they must come out. **Each row carries the protocol that produced
it**, because three of the six are unreproducible without it:

| # | pool / surface / order | protocol the record used | target |
|---|---|---|---|
| G1 | `puro` / corpus test / `born_at` | **split 0 only** — not the five-split mean | **0.5216 ± 0.0002** |
| G2 | `puro` / corpus test / random mean | **`order_search.py` generator** (trap 5.5), split 0 only | **0.4227 ± 0.002** |
| G3 | `puro` / full corpus / `born_at` | all 2000 indices | **0.5115 ± 0.0002** |
| G4 | `puro` / full corpus / random mean | **`order_search.py` generator** (trap 5.5) | **0.4172 ± 0.002**, sd ≈ 0.0711 |
| G5 | `puro` / space / `born_at` | `space_pools`, normalised by `n` | **0.3148 ± 0.0002** |
| G6 | `puro` / space / random mean | **`random_order(ids, seed)`, seeds 0..49** (trap 5.5) | **0.3768 ± 0.002**, sd ≈ 0.1026 |

**G1, G2, G5 and G6 gate against a record** (`results3/order_search.json` and the
`FINDINGS3.md` erratum). **G3 and G4 gate against an unowned probe** — they are
here because they are the only check available on the full-corpus surface, and
because giving them an owner is what this stage is for. Say which kind each is in
the write-up; a probe that gates is still a probe.

If any of the six misses, **stop and report**. Do not adjust to fit. A miss means
the pool construction, the index set or the generator differs from the record's,
and that has to be understood before a new figure is added on top. **A miss on G2,
G4 or G6 is a generator mismatch until proven otherwise** — check trap 5.5 before
suspecting anything else.

**The new figures this stage produces** (nothing owns them today):

- `hibrido` / full corpus, corpus test, space × `born_at`, reversed, random — the
  floor Stage D is scored against, and it exists nowhere today.
- `puro` / space / `born_at` reversed, and `puro` / full corpus / `born_at`
  reversed — which finally gives those probe figures an owning record and
  discharges `ARBITRATION_REPORT.md`'s "left unconfirmed" warning.

**This stage carries no prediction.** P-a and P-b were spent before signature
(§0.1) and are not restored. Stage A is now pure measurement, and that changes
nothing about what it must produce — the record, the script, the `_env` and the
labels. It changes only what may be claimed afterwards: **not** that a band held,
only that a figure now has an owner.

**Definition of done.** JSON written with `_env`; the six gate figures reproduce
under the protocols named above; tests green under `python3 -m unittest discover`;
a short section appended to `results3/FINDINGS3.md` naming surface, pool **and
generator** on every line; a dated erratum to `ARBITRATION_REPORT.md` for the two
reversed-order figures it left unconfirmed; `STATUS.md` gains a pointer. The
figures transcribed in §0.1 are audit measurements, not this record — reproduce
them, do not copy them.

---

## 7. Stage B — the labelled pair benchmark (free, no API calls)

**Why.** Stage C needs pairs whose correct winner is known by construction, so the
whole idea can be killed before a euro is spent on the learned base.

**The substrate already exists.** `rung2/hidden_priority.py` derives the minimal
edge set from the hidden policy's layer order. Verified by running it:

```
29 rules → 406 pairs
  112  disjoint extensions            (can never compete)
   61  already ordered by subsumption (no declaration needed)
   34  same action                    (it does not matter who wins)
  199  DECLARED EDGES, winner known   ← the benchmark
    0  rejected
```

`build_hidden_engine()` returns `(engine, declared, stats)` where `declared` is the
list of `(winner_id, loser_id)` pairs. Do not modify that module; import it.

**Deliverable.** New `rung2/pair_benchmark.py` → `results2/pair_benchmark.json`.
New `tests/test_pair_benchmark.py`.

**And an edit to `tests/test_oracle_separation.py`, in the same commit.** Its
`test_who_may_see_it` compares the set of modules importing `hidden_policy`,
`true_action` or `true_rule_id` against a **literal allowlist**, with
`assertEqual`. `rung2/pair_benchmark.py` imports `true_action`, so the whole suite
goes red the moment the file exists until it is added to that list — next to
`rung2/ceiling_check2.py`, with a comment saying why it is allowed: it measures
offline against a known key and never decides anything. **That is not a workaround,
it is the mechanism working**: the test's own docstring says growing the list must
be a decision rather than an oversight. Make it deliberately, and do not silence
the test any other way.

Stage A needs no such edit: `rung3/floor_by_pool.py` imports the oracle through
`order_search.build_tables`, never by name, so the AST walk does not see it.

**Building a witness, which is the whole point.** For each declared edge, the
witness is a case drawn from `ext(winner) & ext(loser)` — the region where the two
rules actually compete. The answer to "which queue does this ticket go to?" *is*
the edge, and checking it costs an `&` of two integers.

**But not any case in the intersection will do.** A third rule from an even earlier
layer may also match there, in which case the hidden policy's true action is
neither rule's. So:

```python
inter = engine.ext[w] & engine.ext[l]
# restrict to cases where the truth is the winner's action
clean = [i for i in cases_of(inter) if true_action(cases[i]) == action[w]]
```

with `true_action` from `harness.hidden_policy` and the index conversion of §5.1.
Take the **lowest clean case index** (deterministic — no sampling, no seed
needed).

- Pairs with at least one clean witness → the benchmark, and its denominator.
- Pairs with none → recorded, **counted separately, outside the denominator**, with
  the reason. Their count is a result of this stage.

**Measured 2026-08-24, so nobody has to guess: 170 of the 199 declared pairs have
a clean witness and 29 do not.** The 29 lose it to a third rule from an even
earlier layer owning the whole intersection, not to an empty one — intersection
sizes over the 199 run min 80, median 2,560, max 33,600 cases. Eleven of the 29
have `H03` as winner. Stage B must reproduce those two counts; they are a gate on
it in the same sense §6's six are a gate on Stage A.

**Read the 29 as a bias and not only as a loss.** They are precisely the pairs
where the layer order is invisible on the surface of the two rules shown, so the
170 that survive are the easier half by construction. Stage C's rate is therefore
an **upper** estimate of what the proposer would do on all 199. Write that
sentence into the record; it is not a caveat, it is what the denominator means.

**Assertions that must hold for every emitted witness** — if any fails, stop:

1. both rules match the case (`Rule2.matches`);
2. `true_action(case) == action[winner]`;
3. re-running the script produces byte-identical witnesses.

**Record, per pair:** `winner`, `loser`, both actions, witness case index, the
witness case as a dict, `popcount(inter)`, `clean` true/false. Plus the four-box
counts above, so the record checks itself: `112 + 61 + 34 + 199 == 406`.

**Definition of done.** JSON with `_env`; tests asserting the four counts, the
three assertions, and determinism across two runs; the `results2/FINDINGS2.md`
addendum. Zero API calls.

---

## 8. The metric trap — read before Stages C and D

This section governs both and is the reason the plan exists in this shape.

**Acceptance rate is not a result here, and reporting it as one would be a
regression.** All 14 edges rejected across rung 2's eight runs fell to
`EDGE_DISJOINT` (`no_solapan`). A witness drawn from `ext(A) ∩ ext(B)` guarantees
overlap **by construction**, so `EDGE_DISJOINT` becomes unreachable and the
acceptance rate rises from 0/14 *whatever the model does*. It measures the
protocol, not the proposer.

**And the validator cannot check truth** (§5.2). So at 39% accuracy what this
protocol would produce is **accepted and false edges** — converting a visible
rejection into a silent error, which is the exact conversion this project exists
to avoid.

Therefore, in both stages:

> **Count correct edges. Never accepted edges.**

The `try_edge` verdict histogram is still recorded — it is cheap and it is
information about the graph — but it goes in a separate block of the JSON, under a
key that says so, **outside every denominator**, with a note naming **every**
verdict this protocol makes unreachable. In Stage C that is three, not one: the
pairs come from `hidden_priority.py`, which already filtered out disjoint
extensions, subsumption-comparable pairs and same-action pairs, so
`EDGE_DISJOINT`, `EDGE_CONTRADICTS` and the redundant-`EDGE_OK` branch
(`engine2.py:305`) can none of them fire. A histogram of five buckets that can
only ever land in two is worth recording and worth labelling as such.

---

## 9. Stage C — the kill switch (170 calls, cents, gated on §0)

**Why.** Test the change of question where the answer is already known. If the
model cannot pick the right winner *with the solution key in hand*, the format was
never the problem, and Stage D is cancelled before spending anything on the
learned base.

**Deliverable.** New `rung2/pair_judgement.py --hidden` →
`results2/pair_judgement_hidden.json`.

**Protocol.**

- Population: the clean-witness pairs from Stage B — **170**, measured, not
  estimated (§7). The 29 without a clean witness are outside the denominator and
  reported alongside it.
- Per pair, one call. Show: the witness ticket, and **exactly two rules**, rendered
  with `Rule2.render()` (which already omits `correct_count` — keep it that way).
- Ask for the **queue**, not for a winner id. Two reasons: the answer is then the
  same output type as the 0.3877 baseline, which makes the comparison legitimate;
  and the edge is derived deterministically from it. Winner and loser always have
  different actions here (the 34 same-action pairs were excluded upstream), so the
  three outcomes are well-defined:
  - answer == winner's action → **correct edge**
  - answer == loser's action → **wrong edge**
  - anything else (another queue, unparseable) → **neither**, counted apart

  **`neither` is inside P-c's denominator and counts as a failure**
  (§0). It is *counted apart* in the sense that its own tally is
  published beside the rate — failing by declining to answer and
  failing by answering wrongly are different findings — not in the
  sense of being removed from it. `correct / (correct + wrong)` is
  recorded too and adjudicates nothing.
- Model and settings identical to rung 2 so the comparison holds:
  `deepseek/deepseek-v4-flash`, `temperature=0`, `response_format={"type":
  "json_object"}`, `max_retries=2`. Reuse `rung2.proposers2.parse_payload`; write a
  new thin client in the new module rather than touching `proposers2.py`.
- Sequential. No parallelism (hard rule 3).

**The two floors, and the second is the one that matters.**

- **0.3877** — `proposal_action_accuracy` from `results/llm_run.json`: the same
  operation (a ticket in front, a queue to decide) under the old framing. It is the
  natural comparison and it is **too lenient**, because that task was an 8-way
  choice and this one presents two candidates.
- **0.50** — a coin between the two rules shown. This is the real bar. A protocol
  that beats 0.3877 but not 0.50 has demonstrated nothing except that showing two
  options narrows the choice to two options.

**This paragraph used to say "the refutation line of P-c uses the coin,
deliberately", and it stopped being true when the band moved.** The refutation
line went to `≤ 0.60` — the band's own edge — when §0 closed its three dead
zones, and this sentence was left behind one paragraph above the text that
corrects it. The coin is the **kill switch**, not the refutation line. What
follows is the reconciliation, and it is the one to read.

**The refutation line and the kill switch are two different lines, and §0 now
keeps them apart.** P-c is refuted at `≤ 0.60` — its band's own edge, so no dead
zone. The kill switch sits lower, at the coin:

- **`≤ 0.50` → stop.** The protocol has not beaten a two-way guess. Write it up as
  a negative result and go no further; that is a result (hard rule 6).
- **`0.50 < rate ≤ 0.60` → P-c is refuted, and Stage D is a decision for Sergi,
  not for the agent.** The claim failed; whether the residue is worth 300–500
  calls is a judgement about money, and it is his. Report and wait.
- **`> 0.60` → P-c holds and Stage D may run**, subject to its own signed rows.

Refuted-but-not-dead is a real state and it now has a name instead of an open
interval.

**Also record**, outside the denominator: verdict histogram (§8), pairs with no
clean witness, parse failures, and the wrong-edge rate broken down by whether the
winner is the *broader* or the *narrower* rule of the pair. That last split is
cheap and it tests the "narrow ≠ correct" mechanism directly.

**Cost.** 170 calls at flash pricing. Cents. Run the smoke path on 10 pairs first
and check the output shape before the full sweep.

---

## 10. Stage D — the learned base (≈300–500 calls, gated on Stage C)

**Only if Stage C beat its refutation line.**

**Deliverable.** `rung2/pair_judgement.py --learned` →
`results2/pair_judgement_learned.json`.

**Population.** Pairs from the 577 rules of `results/llm_run.json` satisfying the
same three conditions `hidden_priority.py` uses: extensions **overlap**, they are
**subsumption-incomparable**, and their **actions differ**. Over the space that is
**31,850 of the 166,176 pairs — 19.2%**, measured 2026-08-24. A constant fraction
of the quadratic, not a lower order; do not repeat the claim that this is
sub-quadratic.

**Do not use 35,457 here, which the first draft of this section did.** That figure
— `results3/order_metrics.json`, `pair_census_space_pure.conflicting` — is what
`rung3/order_metrics.py:216` computes, and it applies **two** of the three
conditions: co-match and differing actions, with no subsumption filter at all. The
3,607-pair difference is subsumption-comparable, and on exactly those a declared
edge cannot enter the graph whichever way the model answers: `try_edge` returns
`EDGE_CONTRADICTS` if it names the broader rule and a redundant `EDGE_OK` that
mutates nothing if it names the narrower one (`rung2/engine2.py:302-306`).
Sampling from 35,457 spends about one call in ten on a pair whose answer is inert
by construction — and, worse, one of those wasted calls scores as an acceptance.

Sample deterministically at seed 17 down to the budget: 300–500 pairs.

**There is no truth for these pairs.** State it plainly in the record: no
correct-edge rate exists here. What is measured is what the declared edges *do*.

**Scoring, and it has three parts:**

1. **As a hybrid engine.** Install the accepted edges into a `PriorityEngine` over
   the 577 rules and measure e2e, silent error, CONFLICT and IMPASSE rates on
   corpus test. Compare against the `hibrido` numbers, never against `puro`
   ones — scoring a hybrid result against 0.8530 inflates the bar by ~0.08 by
   reading another engine's surface.
2. **As an order, against the floor from Stage A** — the `hibrido` `born_at`
   floor, which did not exist before this plan. This is **P-d**.
3. **As a machine, against the 65.** A score inside the distribution of the 65 end
   orders is *not* evidence that the order is the policy: the 65 tie on score and
   disagree on up to 20.35% of the space, and the two surfaces correlate at 0.34.
   So compute the **behavioural distance** — the fraction of the space, and of the
   corpus, on which the declared order and each of the 65 decide differently —
   reusing the machinery of `rung3/order_metrics.py`. This is **P-e**, and it is
   the part that distinguishes "scored well" from "is the policy". **Two warnings,
   and budget the stage only after reading both.**

   **Warning 1 — the 65 orders are not stored, and the first draft of this line
   said they were.** `results3/order_metrics.json` holds their twelve-character
   *signatures* and five `cited_orders`; it does not hold 65 orders.
   `local_search.multistart` says so in writing — "no record in `results*/` holds
   an order from this optimizer" — and `keep_orders` exists precisely because they
   must be recomputed. P-e therefore costs a fresh 65-start multi-start, not a
   lookup from a file. At the hybrid pool's measured 4-5 s per search
   (`FINDINGS_AUDIT.md`) that is roughly five minutes per split: cheap, but it has
   to be *in* the plan rather than assumed away.

   **Warning 2 — the 65 are a different machine.** They are `puro`, splits 0 and 4
   (`order_metrics.json`: `pool = puro`). Stage D's order runs inside a
   `PriorityEngine`, which is `hibrido`. Point 1 above forbids chaining the two for
   scores, and the same prohibition holds for behaviour: a hybrid order and a pure
   order can decide differently for no reason except the pool, which would enter
   the distance as if it were disagreement about priority. So **regenerate the 65
   on the hybrid pool** and compare like with like. That is what P-e means and what
   its band is measured on. Reporting the pure-pool distance instead is publishable
   only with the label "pool and order measured together" on the same line as the
   figure — and it does not adjudicate P-e.

**Interpretation, written before the figures exist.** Landing on the floor →
declaration contributes no channel. Landing between floor and the cloud →
it contributes and is not enough, which is a result and not a tie. Landing inside
the cloud → the strongest outcome available from this experiment, and still not a
demonstration that the base is right, because the cloud itself is 65 different
machines.

---

## 11. Stage E — authorship discipline at write time (specified, NOT authorised)

**Do not start this before Stage D has a written record** (hard rule 5 of
`CLAUDE.md`, in §4's numbering: no prompt or schema change before a recorded
result). It needs its own signed §0 in its own `PLAN_*.md`, and it costs money.

**The measured cause it attacks.** Subsumption is sound over the hand-written
policy (silent error 0.0000) and gives **53.12% silent error over the learned
base** — over the 160 of 2000 cases where it commits at all, coverage 0.0800.
Two distinct failures: there is hardly any nesting to detect (**5.17%** of pairs,
against 15% for the hand-written policy), and when there is, it crowns narrow but
wrong rules. **Narrow ≠ correct.** The criterion is measuring a virtue of the
*author*, not of itself.

**The change.** Stop assuming the discipline and impose it. When the proposer
writes a rule that overlaps existing ones, the validator **rejects it unless it
declares, for each overlapped rule, whether it is an *exception to* it or a
*default under* it**. The engine already computes exactly which rules those are
(`sub_below` / `sub_above`, and the overlap arithmetic `render_base_v2` already
puts in front of the model). This converts an inference problem into a declaration
problem with a bounded number of locally answerable questions.

**Two predictions, and the second is the one nobody has posed:**

1. *Soundness* — silent error of subsumption over a base produced this way falls
   well below 53.12% **at comparable or greater coverage**. Without that condition
   the prediction fulfils itself by making the criterion even more mute.
2. *Bound* — the 0.047 gap between the hybrid bound (0.8540) and the pure one
   (0.9010) narrows. This is the one that decides whether level 1 stops having a
   price or merely stops lying. If soundness improves and the bound does not move,
   this fixes half the problem and subsumption still silences a third of the base.

---

## 12. Definition of done, per stage

For every stage:

- [ ] Record written under `results*/` with `_env` from `harness.provenance`.
- [ ] `PYTHONHASHSEED=0` set explicitly for the run.
- [ ] Tests added under `tests/`, whole suite green with **`python3 -m unittest
      discover`** — the project's runner, the one `.githooks/pre-commit:104` and
      `.github/workflows/tests.yml:82` both use. Not `pytest`: it is in neither
      `requirements.txt` nor `.venv`, and prescribing it invites an agent to
      install a dependency the records' environment does not have.
- [ ] Every figure in prose names its **surface** and its **pool** — and, for any
      random baseline, its **generator** (trap 5.5).
- [ ] A section appended to the owning `FINDINGS`, with a dated erratum if it
      corrects something already published.
- [ ] `STATUS.md` updated: a pointer, never a copy of the figure.
- [ ] Code and results in their own commits; `PLAN_*.md` and signatures alone in
      theirs.
- [ ] If the stage added a module that imports the oracle,
      `tests/test_oracle_separation.py`'s allowlist was edited **deliberately**, in
      the same commit, with a comment saying why the module may see it.

---

## 13. What this plan does not do

Stated so that nobody reads it as more than it is.

- **It does not touch the second material problem.** For `T3_ENGINEERING` (66.7%)
  and `ACCOUNT_MANAGER` (64.2%) no correct rule exists at all. No edge, no order
  and no arbiter recovers those cases. Six of eight classes — 1774 of 2000 cases —
  are a pure ordering problem; those two are not.
- **It does not measure the founding question.** Whether the LLM's rules get reused
  or whether it memorises cases has still never been measured cleanly. Rung 1's
  0.158 reuse describes the arbitration, not the induction (594 of its 632
  escalations were CONFLICT). Whatever measures it next must clear the memorisation
  floor: `keep_k(k=8)` reaches **0.1176** reuse without inducing anything, purely
  from the corpus's 12.8% duplicates. A figure near 0.118 is noise.
- **It does not license a pipeline.** Do not build a detector / deterministic
  arbiter / LLM arbiter / critic / verifier / compiler stack on the strength of a
  passing Stage C. Building the apparatus and discovering nothing comes down the
  pipe already happened once, is documented, and cost the project its only
  mechanism that works without error.
- **Figures do not travel.** Neither the 0.8530 nor the feedback channel's 61%
  survives a change of base; both were measured over rung 1's 577 rules. And the
  61% is a gain over `born_at` (+0.2011 of +0.3273), not a multiplier of anything.
  Do not chain them.
