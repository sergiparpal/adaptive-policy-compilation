"""
The rows `PLAN_WHY.md` reads, and the statistics of its §0. Pure functions over
records already loaded: nothing here opens a file.

A ROW is one answer that named one of its two rules and carried a `why`. It
holds what the proposer was shown and what it said, and nothing it was not
shown, except the truth, which a row of the learned base carries from
`results2/pair_sample_1600.json` and a Stage C row from its own benchmark.

  named, other      the rule the answer named, and the one it did not
  narrower          the named rule's extension is strictly smaller
  more_conditions   it has strictly more conditions, as listed in the question
  categorical       it carries a categorical or exact condition the other
                    lacks (`codebook.categorical_edge`)
  right_space,      it is the better rule over the shared region, under each
  right_corpus      definition; None where neither rule is strictly better
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Callable, Iterable

from . import codebook as cb


def _row(*, batch, index, named_label, why, named_conds, other_conds, ext_named,
         ext_other, right_space, right_corpus, queue_pair) -> dict:
    codes = cb.code(why)
    la, lb = cb.labels(why)
    return {
        "batch": batch, "index": index, "named_label": named_label,
        "why": why, "codes": codes, "label_a": la, "label_b": lb,
        "language": cb.language(why),
        "narrower": ext_named < ext_other,
        "more_conditions": len(named_conds) > len(other_conds),
        "equal_conditions": len(named_conds) == len(other_conds),
        "categorical": cb.categorical_edge(named_conds, other_conds),
        "right_space": right_space, "right_corpus": right_corpus,
        "queue_pair": queue_pair,
    }


def learned_rows(answers: Iterable[dict], truth: dict[int, dict] | None,
                 batch_of: Callable[[dict], str]) -> list[dict]:
    """Rows of the learned base, from answers in `pair_judgement_1600.json`'s
    or Stage D's format. `truth` maps a row's index to its entry in
    `pair_sample_1600.json`; None leaves the truth out."""
    out = []
    for r in answers:
        if r["declared"] not in ("a_beats_b", "b_beats_a") or not r.get("why"):
            continue
        w = r["rule_a"] if r["declared"] == "a_beats_b" else r["rule_b"]
        o = r["rule_b"] if w == r["rule_a"] else r["rule_a"]
        first, second = cb.listed_rules(r["question"])
        named_label = "A" if r["shown_as"]["A"] == w else "B"
        nc, oc = (first, second) if named_label == "A" else (second, first)
        ext = {r["rule_a"]: r["extension_a"], r["rule_b"]: r["extension_b"]}

        def right(surface):
            if truth is None:
                return None
            b = truth[r["index"]][f"better_{surface}"]
            best = r["rule_a"] if b == "a" else r["rule_b"] if b == "b" else None
            return None if best is None else best == w
        out.append(_row(batch=batch_of(r), index=r["index"], named_label=named_label,
                        why=r["why"], named_conds=nc, other_conds=oc,
                        ext_named=ext[w], ext_other=ext[o],
                        right_space=right("space"), right_corpus=right("corpus"),
                        queue_pair=" vs ".join(sorted((r["action_a"], r["action_b"])))))
    return out


def hidden_rows(answers: Iterable[dict]) -> list[dict]:
    """Rows of Stage C, the hidden policy's pairs: the truth is the winner,
    known by construction, so `right_space` and `right_corpus` are the same."""
    out = []
    for r in answers:
        if r["outcome"] not in ("correct", "wrong") or not r.get("why"):
            continue
        winner_first = r["winner_shown_as"] == "A"
        named_is_winner = r["outcome"] == "correct"
        named_label = "A" if named_is_winner == winner_first else "B"
        first, second = cb.listed_rules(r["question"])
        nc, oc = (first, second) if named_label == "A" else (second, first)
        ew, el = r["winner_extension"], r["loser_extension"]
        out.append(_row(batch="stage_c", index=r["index"], named_label=named_label,
                        why=r["why"], named_conds=nc, other_conds=oc,
                        ext_named=ew if named_is_winner else el,
                        ext_other=el if named_is_winner else ew,
                        right_space=named_is_winner, right_corpus=named_is_winner,
                        queue_pair=" vs ".join(sorted((r["winner_action"],
                                                       r["loser_action"])))))
    return out


# ---------------------------------------------------------------------------
# The statistics
# ---------------------------------------------------------------------------

def share(rows: Iterable[dict], key: str) -> dict:
    """The share of rows whose `key` is true, over the rows where it is not
    None, with its binomial error."""
    vals = [r[key] for r in rows if r[key] is not None]
    n, hits = len(vals), sum(1 for v in vals if v)
    p = hits / n if n else None
    return {"n": n, "hits": hits, "share": p,
            "standard_error": math.sqrt(p * (1 - p) / n) if n else None}


def difference(a: dict, b: dict) -> dict:
    """The first share minus the second, with the unpooled error."""
    if a["share"] is None or b["share"] is None:
        return {"first": a, "second": b, "difference": None, "standard_error": None}
    return {"first": a, "second": b, "difference": a["share"] - b["share"],
            "standard_error": math.sqrt(a["standard_error"] ** 2
                                        + b["standard_error"] ** 2)}


def with_code(rows, code: str) -> list[dict]:
    return [r for r in rows if code in r["codes"]]


def without_code(rows, code: str) -> list[dict]:
    return [r for r in rows if code not in r["codes"]]


def spec_not_count(rows) -> list[dict]:
    return [r for r in rows if "spec" in r["codes"] and "count" not in r["codes"]]


def census(rows: list[dict]) -> dict:
    """How often each code, label and language occurs."""
    n = len(rows)
    codes = Counter(c for r in rows for c in r["codes"])
    return {"n": n,
            "codes": {k: codes.get(k, 0) for k in cb.CODES},
            "no_reason_code": sum(1 for r in rows
                                  if not r["codes"] & {"spec", "queue", "match", "order"}),
            "labels": {"A_only": sum(1 for r in rows if r["label_a"] and not r["label_b"]),
                       "B_only": sum(1 for r in rows if r["label_b"] and not r["label_a"]),
                       "both": sum(1 for r in rows if r["label_a"] and r["label_b"]),
                       "neither": sum(1 for r in rows
                                      if not r["label_a"] and not r["label_b"])},
            "languages": dict(sorted(Counter(r["language"] for r in rows).items()))}


def section_0(rows: list[dict]) -> dict:
    """The four statistics of §0, on whatever rows they are given. The stage
    gives them the held-out answers; `Y-g3` gives them the development set,
    whose values §0 already declares."""
    spec = with_code(rows, "spec")
    snc = spec_not_count(rows)
    return {
        "Y-a": share(spec, "narrower"),
        "Y-b": share(snc, "more_conditions"),
        "Y-c": difference(share(snc, "categorical"),
                          share(without_code(rows, "spec"), "categorical")),
        "Y-d": difference(share(spec, "right_space"),
                          share(without_code(rows, "spec"), "right_space")),
    }
