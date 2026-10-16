"""
The instances `PLAN_BOUND.md` bounds, and the published scores it bounds them
against. Zero API calls, and nothing here writes.

THE INSTANCES are exactly what rung 3's audited search was run on, built by the
functions that built them, imported rather than copied:

  space   the exhaustive 134,400 cases, both pools, from
          `rung3.order_search_ls.space_pools`, the masks the direct search over
          the space was scored on.
  corpus  the train half of each of the five splits, both pools, from
          `rung3.order_search.build_tables`, `split` and
          `rung3.local_search.build_masks`, the masks the search per split was
          fitted on. The train half and not the test half, because that is
          where an order was searched for: a bound on cases the order never saw
          says nothing about how well the search searched.

THE PUBLISHED SCORES are read from the records, never recomputed: re-running the
direct search over the space costs about 2.7 hours, and its published figure is
the one `STATUS.md` cites.

  space   `full_space_direct[pool].local_search`, to four decimals.
  corpus  the best train score any record publishes for that split and pool:
          the declared search's (`order_search_ls.json`) and, on the pure pool,
          the budget diagnostic's 64, 128 and 256 starts
          (`start_budget_check.json`). With about a thousand train cases, four
          decimals identify the count exactly, and `count_from` checks that.

No module of this package imports the oracle. The truth enters through
`build_tables` and `space_truth_masks`, which `tests/test_oracle_separation.py`
already lists among the modules allowed to see it.
"""

from __future__ import annotations

import json
from pathlib import Path

from harness.domain import generate_corpus
from rung2.engine2 import Space
from rung3 import order_search
from rung3.local_search import build_masks
from rung3.optimizer_check import hidden_rules, masks_over_corpus
from rung3.order_search_ls import space_pools, space_truth_masks

from . import plan
from .certificate import Instance


def load_json(path: Path) -> dict:
    return json.loads(Path(path).read_text())


# ---------------------------------------------------------------------------
# The 577 rules
# ---------------------------------------------------------------------------

def learned():
    """Rung 1's base, its two corpus pools and the truth, as rung 3 built them."""
    corpus, rules, ext, conds = order_search.load()
    ids = [r["rule_id"] for r in rules]
    action = {r["rule_id"]: r["action"] for r in rules}
    below = order_search.subsumption_below(rules, ext)
    matched, undef, truth = order_search.build_tables(corpus, rules, conds, below)
    return {"corpus": corpus, "rules": rules, "ids": ids, "action": action,
            "conds": conds, "below": below, "truth": truth,
            "pools": {"puro": matched, "hibrido": undef}}


def space_instances(base) -> dict[str, Instance]:
    sp = space_pools(base["ids"], base["conds"], base["action"], base["below"])
    return {name: Instance(f"espacio/{name}", base["ids"], M, W, n)
            for name, (M, W, _, n) in sp.items()}


def corpus_instances(base) -> dict[tuple[int, str], Instance]:
    out = {}
    for s in range(plan.N_SPLITS):
        tr, _ = order_search.split(base["corpus"], base["truth"],
                                   seed=plan.SPLIT_SEED + s)
        for name in plan.POOLS:
            M, W, _ = build_masks(base["ids"], base["pools"][name], base["truth"],
                                  base["action"], tr)
            out[(s, name)] = Instance(f"corpus train {s}/{name}", base["ids"],
                                      M, W, len(tr))
    return out


# ---------------------------------------------------------------------------
# The hidden policy: the one instance whose optimum is known
# ---------------------------------------------------------------------------

def hidden_instances() -> dict[str, tuple[Instance, list[str]]]:
    """The 29 rules on both surfaces and both pools, each with the design
    order. On the pure pool the design order scores every case: no cycle can
    exist there, and a certificate that found one would be wrong."""
    ids, conds, action, born = hidden_rules()
    design = sorted(ids, key=lambda r: born[r])
    space = Space()
    ext = {r: space.extension(conds[r]) for r in ids}
    tmask = space_truth_masks(space)
    rules = [{"rule_id": r} for r in ids]
    below = order_search.subsumption_below(rules, ext)
    out = {}
    for name in plan.POOLS:
        if name == "puro":
            M = dict(ext)
        else:
            M = {}
            for r in ids:
                dominated = 0
                for b in below[r]:
                    dominated |= ext[b]
                M[r] = ext[r] & ~dominated
        W = {r: M[r] & tmask[action[r]] for r in ids}
        out[f"espacio/{name}"] = (Instance(f"oculta espacio/{name}", ids, M, W,
                                           space.n), design)
    corpus = generate_corpus(2000, seed=17)
    M, W, _ = masks_over_corpus(ids, conds, action, corpus)
    out["corpus/puro"] = (Instance("oculta corpus/puro", ids, M, W, len(corpus)),
                          design)
    return out


# ---------------------------------------------------------------------------
# What the records publish
# ---------------------------------------------------------------------------

def count_from(share: float, n: int) -> int | None:
    """The count a four-decimal share of `n` cases stands for, if exactly one
    does; None if four decimals cannot tell."""
    c = round(share * n)
    hits = [k for k in (c - 1, c, c + 1) if 0 <= k <= n and round(k / n, 4) == share]
    return hits[0] if len(hits) == 1 else None


def published() -> dict:
    """The bounds and the best searched scores the records publish, per
    instance. Counts on the corpus, four-decimal shares on the space."""
    fs = load_json(plan.FULLSPACE)
    ls = load_json(plan.SPLITS)
    budget = load_json(plan.BUDGET)
    ceil = load_json(plan.CEILINGS)

    space = {}
    for name in plan.POOLS:
        space[name] = {
            "bound": fs["bounds"][name]["espacio"],
            "attained": fs["full_space_direct"][name]["local_search"],
            "attained_from": f"{plan.FULLSPACE} full_space_direct.{name}.local_search",
        }

    corpus = {}
    for s in range(plan.N_SPLITS):
        crow = next(r for r in ceil["splits"] if r["split"] == s)
        for name in plan.POOLS:
            row = next(r for r in ls["splits"] if r["split"] == s and r["pool"] == name)
            n = row["n_train"]
            sources = {"order_search_ls (65 starts)": count_from(row["ls_train"], n)}
            if name == "puro":
                for b in budget["rows"]:
                    if b["split"] == s:
                        sources[f"start_budget_check ({b['starts']} starts)"] = b["train_score"]
            best = max(v for v in sources.values() if v is not None)
            corpus[(s, name)] = {
                "n": n,
                "bound_share": crow[f"{name}_ceil_train"],
                "attained": best,
                "sources": sources,
            }
    return {"space": space, "corpus": corpus}
