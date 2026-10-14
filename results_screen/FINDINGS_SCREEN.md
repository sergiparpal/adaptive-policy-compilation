# What the screen of compiled rules does to the model — findings

Record opened on October 14, 2026, under [`PLAN_SCREEN.md`](../PLAN_SCREEN.md).
Sergi signed §0 on 2026-10-14, before any figure below existed, in a commit of
its own: *PLAN_SCREEN.md signed by Sergi*. Every record names in its `_env` the
commit of the branch it was written on. A rebase merge gives those commits new
hashes on `main` with the same trees. **This record owns every figure in it.**

**Stage A ran on 2026-10-14, and nothing is adjudicated yet.** Stage B's smoke
session passed the same day. The four rows wait for the anchor and the
ticket-only session.

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Row `V-e` carries no band.
> Its pilot half reproduces figures the drafter computed with a scratch probe
> before drafting, which §0 of the plan declares as already seen. Its held-out
> half was computed here for the first time, after the signature. Zero API calls.

---

## Stage A — the checks, the populations and the free readout

**What was run.** `python3 -m screen.sample`, on 2026-10-14, with
`PYTHONHASHSEED=0`, on a clean tree. It took about two and a half minutes,
almost all of it the suite inside `V-g1`. The record is
[`sample.json`](sample.json).

**Surface: the corpus.** That is `generate_corpus(2000, seed=17)` in arrival
order, the decided cases of `PLAN_REUSE.md`'s three Stage B records as
`PLAN_FIDELITY.md` drew them. Nothing here is measured on the exhaustive space.

**Stage A ran twice, and the second run is the record.**

- **The first run**, from the signature's commit, lacked the counts and spreads
  §0 lists as seen, which §7 makes this record's to own. Every figure it did
  carry, the second run gives back. It was discarded before any commit.
- **The module gained them** in *screen/sample.py: Stage A measures the counts
  and spreads §0 lists as seen*. The second run is that commit's.

**The blocking checks passed before anything was computed.**

- **`V-g1`.**
  - The suite was green, 1,599 tests.
  - `PLAN_FIDELITY.md`'s F-g1 to F-g3 passed, and its Stage A record is the
    design they rebuild.
  - Its Stage C, re-run in memory with its own functions, gave back its
    `score.json` to a relative 1e-12.
  - Every one of its session records is under its protocol and behind its Stage
    A record.
- **`V-g2`.** 1,184 ticket-only prompts, every one v1's empty base, and the 301
  that `F-f` asked carry the digests it recorded. The 300 anchor prompts are
  `F-f`'s B prompts, rebuilt to the digest. The plurality is defined on every
  decision.
- **`V-g3`.** The pilot is the first 100 of each draw. The held-out decisions
  are 429, 405 and 425, none of them on a ticket `F-f` asked, and every one of
  their screens shows a rule.
- **`V-g4`.** Signed.

### The counts and the pilot, measured

**Every figure §0 lists as already seen reproduces**, so §0 needs no erratum.
On the pilot, `t` is `F-f`'s one answer without a screen of 2026-10-03, and
`b₁`, `b₂` its two answers with the screen.

| §0's figure | measured |
|---|---|
| tickets in the draw and census; asked by `F-f`; behind the pilot | 1,184; 301; 276 |
| held-out decisions; with two valid answers with the screen | 429 · 405 · 425; 426 · 405 · 423 |
| tickets behind the held-out decisions; serving more than one | 883; 303 |
| rules on a held-out screen | 4 to 12, 12 at the median |
| the pilot's net, `t`'s accuracy less the mean of `b₁`'s and `b₂`'s | +0.130 · +0.030 · +0.025; pooled +0.0617, se 0.028 |
| `t` alone right, against `b₁` alone right | 48 against 29 |
| the plurality is the true queue | 0.26 · 0.40 · 0.24; pooled 0.30 |
| where it is, the screen ahead by | 0.178, on 90 |
| where it is not, the screen behind by | 0.167, on 210 |
| `b₁` is the plurality where `t` is not | 0.534 · 0.660 · 0.243; pooled 0.455, on 178 |
| the spreads: the net, the two cells, the pull | 0.484; 0.429 and 0.476; 0.498 |

The agreements and the table by true queue reproduce as well, figure for
figure. They are in the record's `readout.pilot`.

### The held-out decisions, without a single new answer

Computed here for the first time. These are the figures §10 kept behind the
gate.

| | run 1 | run 2 | run 3 |
|---|---|---|---|
| held-out decisions | 429 | 405 | 425 |
| the screen's plurality is the true queue | 0.3077 | 0.3630 | 0.2847 |
| `V-d`'s cells, plurality right and wrong | 132 and 297 | 147 and 258 | 121 and 304 |

**What it says.**

1. **The held-out screens are the pilot's kind.** Their plurality is the true
   queue on about three decisions in ten, as on the pilot. A copier that
   answered it would be right that often.
2. **Every cell of `V-d` is populated.** The smallest holds 121 decisions,
   against §0's minimum of 50. So no run can lose a value of `V-d` to its
   population; only invalid answers could take one.
3. **The class mix is the draw's, less the rare classes.** Every queue's share of
   the held-out decisions is within 1.7 points of its share of the whole draw.
   No held-out decision is of a rare class, as §2.1 said: `F-f` asked every
   rare-class ticket. The rare classes are `V-e`'s census.

### What Stage A does not settle

Nothing in it is adjudicable. The rows need the answers without a screen, which
Stage B buys. The smoke session goes first, then the anchor, then the ticket-only
session, each on Sergi's word, each record committed before the next.

---

## Stage B

Sergi gave the go-ahead for the smoke session on 2026-10-14, and for nothing
beyond it. Each later session waits for its own go-ahead (§8).

**The smoke session passed and opens the others.** `screen.ask --session smoke`,
2026-10-14, with `PYTHONHASHSEED=0`, from Stage A's commit and a clean tree. The
checks of §8 ran in order before any call.

- **The key** was an API key OpenRouter accepts, not a management key.
- **`V-g1` to `V-g4` passed**, with the suite green at 1,599 tests.
- **Stage A's record held** the same sessions, prompts and decisions the checks
  rebuilt.

What came back:

- **All 10 answers were valid**: five ticket-only prompts and five anchor
  prompts, each in one attempt.
- **Every call carried `reasoning: {"effort": "none"}`**, and so does the record.
- **Every attempt's `finish_reason` was recorded, and all ten were `stop`.** This
  is the first record of the thread to keep one; `PLAN_FIDELITY.md`'s never did.
- **The partial file was gone once the record was written.**

The record is [`ask_smoke.json`](ask_smoke.json). Its answers enter no row, and
none is read here.

**The pace.** The calls took 2.49 s at the median, from 1.96 to 17.51 s, and
39.7 s in all. At that median the anchor's 300 calls would take about 13 minutes
and the ticket-only session's 2,368 about 1.6 hours. Ten calls are few, so the
planning figures stay §1's: about half an hour and 2.5 hours.

---

## Files

```
results_screen/sample.json       Stage A: the checks, the populations, the
                                 sessions with every prompt's digest, and V-e's
                                 free half
results_screen/ask_smoke.json    Stage B, the smoke session: 10 of 10 valid;
                                 it opens the other sessions and enters no row
```
