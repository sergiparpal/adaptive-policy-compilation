"""
WHY DOES IT NAME `rule_b` MORE OFTEN? Two candidate effects, one of them real.

--------------------------------------------------------------------------
THE QUESTION, AND WHY IT SURVIVED THREE SECTIONS
--------------------------------------------------------------------------
Stage D came back 203 `b_beats_a` against 162 `a_beats_b`, and
`results2/FINDINGS2.md` left it unexplained. At four times the sample it survived
— 781 against 698 — so `IDEAS.md` kept it as the pairwise thread's last genuinely
open question.

**It survived partly because two different effects were being called one thing.**
`rule_b` is not a position: the pairs are ordered by rule id, ids are assigned in
birth order, so `rule_b` is always the LATER-BORN rule and never necessarily the
one shown second. Presentation order is dealt separately and balanced exactly.
Naming `rule_b` more often and preferring the rule shown second are different
claims about different axes, and conflating them is how the thing stayed open.

--------------------------------------------------------------------------
FOUR HYPOTHESES, DECLARED BEFORE THE MEASUREMENT
--------------------------------------------------------------------------
  `H1 specificity`  it prefers the narrower rule. Its own `why` texts say so:
                    *"La regla A es mas especifica..."*.
  `H2 the ranking`  it is the queue ranking again — later-born rules tend to sit
                    in better-ranked queues, so following the ranking produces the
                    asymmetry without any preference for `b`.
  `H3 birth order`  recency as such.
  `H4 position`     the presentation slot.

`H3` is not separable from the asymmetry itself: `rule_b` is later-born in 100% of
pairs by construction, so `names_later_born` and `names_b` are the same number and
`H3` restates the question rather than answering it. It is kept in the table to
make that visible.

--------------------------------------------------------------------------
THE TEST THAT SEPARATES THEM
--------------------------------------------------------------------------
A marginal rate cannot tell `H1` from `H2`: breadth and the ranking's favourite
coincide on most pairs, so each would look like the other. **The pairs that decide
are the ones where the two point in OPPOSITE directions** — there a follower of
the ranking and a preferrer of broad rules make different choices, and counting
which happens is the whole experiment.

For the asymmetry itself the test is symmetry: does it follow its own ranking
**equally often whichever side the ranking points at**? If it followed the ranking
more when the ranking happens to favour `b`, that would be a `b`-preference the
ranking does not explain. If it follows it equally, the asymmetry is the
population's and not the proposer's.

The ranking is the proposer's own, from `rung3.edge_dropping.revealed_ranking` —
Copeland over the queue pairs it decided, from the answers and nothing else. **No
truth enters any of this**: every quantity here is a property of what was said and
of the rules' shapes.

--------------------------------------------------------------------------
WHAT IT DOES NOT DO
--------------------------------------------------------------------------
It adjudicates nothing and no row moves. **POST-RUN**, written after the whole
thread closed. It does not analyse the `why` texts: the contrast between what the
proposer says it is doing and what it does is worth one sentence in the record and
is not a measurement, because nothing here reads those strings systematically.

Usage:  PYTHONHASHSEED=0 python3 -m rung3.answer_asymmetry
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from harness.provenance import describe, environment
from rung3.edge_dropping import revealed_ranking

OUT = Path("results3")
RECORD = "answer_asymmetry.json"
SOURCE = Path("results2/pair_judgement_1600.json")

PROVENANCE = (
    "POST-RUN, written after PLAN_PROPOSER_1600 closed. It adjudicates nothing "
    "and no signed row moves. The four hypotheses were declared before the "
    "measurement and all four are reported, including the drafter's favourite, "
    "which was wrong. Zero API calls.")


def se(n):
    return (0.25 / n) ** 0.5 if n else None


def rate_block(hits, n, what):
    r = hits / n if n else None
    s = se(n)
    return {"what": what, "n": n, "hits": hits,
            "rate": round(r, 4) if r is not None else None,
            "standard_error": round(s, 4) if s else None,
            "deviations_from_a_coin": round((r - 0.5) / s, 2) if s else None}


def features(rows, rank):
    """One row per declared edge, every feature a property of what was said."""
    out = []
    for r in rows:
        names_a = r["declared"] == "a_beats_b"
        broader_is_a = r["a_is_broader"]
        higher_is_a = rank[r["action_a"]] < rank[r["action_b"]]
        first_is_a = r["a_shown_as"] == "A"
        out.append({
            "names_b": not names_a,
            "names_broader": names_a == broader_is_a,
            "names_later_born": not names_a,     # b is later-born by construction
            "follows_ranking": names_a == higher_is_a,
            "names_first_shown": names_a == first_is_a,
            "ranking_favours_a": higher_is_a,
            "ranking_and_breadth_agree": higher_is_a == broader_is_a,
            "favoured_shown_first": higher_is_a == first_is_a,
        })
    return out


def symmetry_of_following(feats):
    """
    Does it follow its own ranking equally, whichever side the ranking points at?

    This is the test for the asymmetry. A `b`-preference the ranking does not
    explain would show up as following the ranking MORE when the ranking happens
    to favour `b`.
    """
    a = [f for f in feats if f["ranking_favours_a"]]
    b = [f for f in feats if not f["ranking_favours_a"]]
    ra = sum(1 for f in a if f["follows_ranking"]) / len(a)
    rb = sum(1 for f in b if f["follows_ranking"]) / len(b)
    d = rb - ra
    sed = (0.25 / len(a) + 0.25 / len(b)) ** 0.5
    return {
        "what": "the rate at which it follows its own queue ranking, split by "
                "which side the ranking points at. Equal rates mean the a/b "
                "asymmetry belongs to the population and not to the proposer.",
        "when_the_ranking_favours_a": rate_block(
            sum(1 for f in a if f["follows_ranking"]), len(a),
            "follows the ranking"),
        "when_the_ranking_favours_b": rate_block(
            sum(1 for f in b if f["follows_ranking"]), len(b),
            "follows the ranking"),
        "difference": round(d, 4), "standard_error": round(sed, 4),
        "deviations": round(d / sed, 2) if sed else None,
    }


def predicted_names_b(feats):
    """What naming `b` would be if the ranking were the whole story."""
    n = len(feats)
    p_fav_b = sum(1 for f in feats if not f["ranking_favours_a"]) / n
    p_follow = sum(1 for f in feats if f["follows_ranking"]) / n
    pred = p_fav_b * p_follow + (1 - p_fav_b) * (1 - p_follow)
    obs = sum(1 for f in feats if f["names_b"]) / n
    return {
        "what": "naming `b` predicted from the ranking alone: the ranking "
                "favours `b` on some fraction of pairs and the proposer follows "
                "it at some rate, and those two numbers alone give a prediction.",
        "ranking_favours_b_in": round(p_fav_b, 4),
        "follows_the_ranking": round(p_follow, 4),
        "predicted": round(pred, 4), "observed": round(obs, 4),
        "residual": round(obs - pred, 4),
        "residual_in_standard_errors": round((obs - pred) / se(n), 2),
    }


def conflict_test(feats):
    """
    Where the ranking and breadth disagree, which one does it obey?

    The only pairs that can tell `H1` from `H2`. On the rest both hypotheses
    predict the same answer and the marginal rate cannot separate them.
    """
    out = {}
    for key, name in ((True, "ranking_and_breadth_agree"),
                      (False, "they_disagree")):
        part = [f for f in feats if f["ranking_and_breadth_agree"] is key]
        out[name] = {
            "n": len(part),
            "follows_ranking": rate_block(
                sum(1 for f in part if f["follows_ranking"]), len(part),
                "follows the ranking"),
            "names_broader": rate_block(
                sum(1 for f in part if f["names_broader"]), len(part),
                "names the broader rule"),
        }
    out["what"] = ("on the disagreeing pairs a ranking-follower and a "
                   "breadth-preferrer choose differently, so the split decides "
                   "between H1 and H2. On the agreeing pairs both predict the "
                   "same answer and nothing can be learned.")
    return out


def position_test(feats):
    """Does the slot change how reliably it applies its own ranking?"""
    first = [f for f in feats if f["favoured_shown_first"]]
    second = [f for f in feats if not f["favoured_shown_first"]]
    rf = sum(1 for f in first if f["follows_ranking"]) / len(first)
    rs = sum(1 for f in second if f["follows_ranking"]) / len(second)
    d = rf - rs
    sed = (0.25 / len(first) + 0.25 / len(second)) ** 0.5
    return {
        "what": "the rate at which it follows its own ranking, split by whether "
                "the rule that ranking favours was shown first or second. This "
                "is not a preference but an ACCURACY difference: the same "
                "proposer applying the same ranking, worse from one slot.",
        "favoured_shown_first": rate_block(
            sum(1 for f in first if f["follows_ranking"]), len(first),
            "follows the ranking"),
        "favoured_shown_second": rate_block(
            sum(1 for f in second if f["follows_ranking"]), len(second),
            "follows the ranking"),
        "difference": round(d, 4), "standard_error": round(sed, 4),
        "deviations": round(d / sed, 2) if sed else None,
    }


def main(argv=None) -> int:
    t_start = time.time()
    if not SOURCE.exists():
        print(f"ABORTED: {SOURCE} is not there.")
        return 1
    rows = [r for r in json.loads(SOURCE.read_text())["answers"]
            if r["declared"] != "none"]
    order, rank, _c = revealed_ranking(rows)
    feats = features(rows, rank)
    n = len(feats)

    print("=" * 78)
    print("WHY DOES IT NAME `rule_b` MORE OFTEN?")
    print("=" * 78)
    print(f"  {n} declared edges · zero API calls · POST-RUN, adjudicates nothing")
    print(f"  {describe()}")

    base = {
        "b_is_the_narrower_rule": round(
            sum(1 for r in rows if r["a_is_broader"]) / n, 4),
        "b_is_later_born": round(
            sum(1 for r in rows if r["born_b"] > r["born_a"]) / n, 4),
        "the_ranking_favours_b": round(
            sum(1 for f in feats if not f["ranking_favours_a"]) / n, 4),
    }
    print("\n  BASE RATES OF THE POPULATION ASKED (before any answer)")
    for k, v in base.items():
        print(f"    {k:<28}{v:.4f}")

    marg = {k: rate_block(sum(1 for f in feats if f[k]), n, k)
            for k in ("names_b", "names_broader", "names_later_born",
                      "follows_ranking", "names_first_shown")}
    print("\n  MARGINAL RATES")
    for k, v in marg.items():
        print(f"    {k:<20}{v['hits']:>5}/{n} = {v['rate']:.4f}   "
              f"{v['deviations_from_a_coin']:+6.2f} devs")

    sym, pred = symmetry_of_following(feats), predicted_names_b(feats)
    print("\n  H2 — IS THE ASYMMETRY JUST THE RANKING?")
    print(f"    follows the ranking when it favours a: "
          f"{sym['when_the_ranking_favours_a']['rate']:.4f}")
    print(f"    follows the ranking when it favours b: "
          f"{sym['when_the_ranking_favours_b']['rate']:.4f}")
    print(f"    difference {sym['difference']:+.4f}  "
          f"{sym['deviations']:+.2f} devs")
    print(f"    naming b predicted from the ranking alone {pred['predicted']:.4f}"
          f" vs observed {pred['observed']:.4f}  "
          f"residual {pred['residual']:+.4f} "
          f"({pred['residual_in_standard_errors']:+.2f} se)")

    conf = conflict_test(feats)
    print("\n  H1 vs H2 — WHERE THEY DISAGREE")
    for k in ("ranking_and_breadth_agree", "they_disagree"):
        c = conf[k]
        print(f"    {k:<28}n {c['n']:>4}   follows ranking "
              f"{c['follows_ranking']['rate']:.4f}   names broader "
              f"{c['names_broader']['rate']:.4f}")

    posn = position_test(feats)
    print("\n  H4 — DOES THE SLOT CHANGE HOW WELL IT APPLIES ITS OWN RANKING?")
    print(f"    favoured rule shown first : "
          f"{posn['favoured_shown_first']['rate']:.4f}")
    print(f"    favoured rule shown second: "
          f"{posn['favoured_shown_second']['rate']:.4f}")
    print(f"    difference {posn['difference']:+.4f}  "
          f"{posn['deviations']:+.2f} devs")

    payload = {
        "_env": environment(),
        "what": "why the proposer names `rule_b` more often than `rule_a`, the "
                "pairwise thread's last open question. Reads answers already "
                "paid for; zero API calls.",
        "provenance": PROVENANCE,
        "adjudicates_nothing":
            "no row of any plan is read here and none moves.",
        "two_effects_were_being_called_one":
            "`rule_b` is the LATER-BORN rule in 100% of pairs by construction, "
            "never necessarily the one shown second; presentation order is dealt "
            "separately and balanced exactly. Naming `b` more often and "
            "preferring the rule shown second are different claims about "
            "different axes, and conflating them is how this stayed open.",
        "no_truth_enters":
            "every quantity is a property of what was said and of the rules' "
            "shapes. The ranking is the proposer's own, Copeland over the queue "
            "pairs it decided.",
        "hypotheses_declared_before_the_measurement": {
            "H1_specificity": "it prefers the narrower rule; its own `why` texts "
                              "say so",
            "H2_the_ranking": "the queue ranking again — following it produces "
                              "the asymmetry without any preference for `b`",
            "H3_birth_order": "recency as such. NOT SEPARABLE: `b` is later-born "
                              "in 100% of pairs, so this restates the question",
            "H4_position": "the presentation slot",
        },
        "n_declared_edges": n,
        "revealed_ranking": order,
        "base_rates_of_the_population": base,
        "marginal_rates": marg,
        "H2_symmetry_of_following": sym,
        "H2_naming_b_predicted_from_the_ranking": pred,
        "H1_vs_H2_where_they_disagree": conf,
        "H4_position": posn,
        "seconds": round(time.time() - t_start, 1),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {time.time() - t_start:.1f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
