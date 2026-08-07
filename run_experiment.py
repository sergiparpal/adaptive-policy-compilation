#!/usr/bin/env python3
"""
Rung 1: static world, realizable policy, pure shadow.

Usage:
  python run_experiment.py frontier              # mock sweep, 0 calls
  python run_experiment.py llm                   # real proposer
  python run_experiment.py llm --n 500 --model claude-sonnet-5
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# The script's directory always on sys.path, wherever it is run from.
sys.path.insert(0, str(Path(__file__).resolve().parent))

if not (Path(__file__).resolve().parent / "harness" / "domain.py").exists():
    sys.exit(
        "\nERROR DE ESTRUCTURA: no encuentro harness/domain.py\n\n"
        "Los modulos deben estar dentro de una subcarpeta 'harness/':\n\n"
        "  adaptive-triage/\n"
        "    run_experiment.py\n"
        "    harness/\n"
        "      __init__.py  domain.py  dsl.py  shadow.py\n"
        "      proposers.py  hidden_policy.py  cache_baseline.py\n\n"
        "Si los descargaste sueltos y quedaron planos, desde esta carpeta:\n"
        "  mkdir -p harness && mv domain.py dsl.py shadow.py proposers.py \\\n"
        "      hidden_policy.py cache_baseline.py harness/ && touch harness/__init__.py\n"
    )

from harness.domain import generate_corpus
from harness.dsl import RuleEngine
from harness.hidden_policy import HIDDEN_POLICY_SIZE, true_action
from harness.cache_baseline import run_cache_baseline
from harness.provenance import environment
from harness.proposers import KeepKProposer, RandomKProposer
from harness.shadow import run_shadow

OUT = Path("results")


def corpus_stats(corpus) -> dict:
    from collections import Counter

    actions = Counter(true_action(c) for c in corpus)
    uniq = len({c.key() for c in corpus})
    majority = actions.most_common(1)[0]
    return {
        "n": len(corpus),
        "unique_cases": uniq,
        "duplicate_rate": round(1 - uniq / len(corpus), 4),
        "action_distribution": dict(actions.most_common()),
        "majority_class_baseline": round(majority[1] / len(corpus), 4),
    }


def print_row(name: str, m: dict) -> None:
    print(
        f"  {name:<16}"
        f"{m['n_rules']:>7}"
        f"{m['reuse_rate'] if m['reuse_rate'] is not None else 0:>9.3f}"
        f"{m['silent_error_rate'] if m['silent_error_rate'] is not None else 0:>10.3f}"
        f"{m['escalation_rate']:>9.3f}"
        f"{(m['final_decile_escalation_rate'] or 0):>10.3f}"
        f"{m['coverage']:>9.3f}"
        f"{m['dead_rules']:>8}"
    )


def header() -> None:
    print(
        f"  {'estrategia':<16}{'reglas':>7}{'reuso':>9}{'err.sil':>10}"
        f"{'escal':>9}{'esc.d10':>10}{'cobert':>9}{'muertas':>8}"
    )
    print("  " + "-" * 68)


def cmd_frontier(args) -> None:
    corpus = generate_corpus(args.n, seed=args.seed)
    stats = corpus_stats(corpus)

    print("=" * 72)
    print("CORPUS")
    print("=" * 72)
    print(f"  casos: {stats['n']}   unicos: {stats['unique_cases']}   "
          f"duplicados: {stats['duplicate_rate']:.1%}")
    print(f"  politica oculta: {HIDDEN_POLICY_SIZE} reglas")
    print(f"  baseline clase mayoritaria: {stats['majority_class_baseline']:.1%}")
    print("  distribucion de acciones:")
    for a, c in stats["action_distribution"].items():
        print(f"    {a:<22}{c:>6}  {c/stats['n']:>7.1%}")

    print()
    print("=" * 72)
    print("FRONTERA DEL DSL  (mocks, 0 llamadas de LLM)")
    print("=" * 72)
    print("  keep_k: conserva los k atributos mas informativos, todos con 'eq'")
    header()

    results = {}
    for k in range(1, 9):
        engine = RuleEngine()
        res = run_shadow(corpus, engine, KeepKProposer(k))
        results[f"keep_k_{k}"] = res.metrics
        print_row(f"keep_k(k={k})", res.metrics)

    print()
    print("  random_k: mismos k pero atributos al azar")
    header()
    for k in (2, 3, 4):
        engine = RuleEngine()
        res = run_shadow(corpus, engine, RandomKProposer(k, seed=args.seed))
        results[f"random_k_{k}"] = res.metrics
        print_row(f"random_k(k={k})", res.metrics)

    print()
    print("  BASELINE OBLIGATORIO: cache semantica (sin reglas, vecino mas cercano)")
    header()
    for d in (0, 1, 2):
        m = run_cache_baseline(corpus, max_dist=d)
        results[f"cache_{d}"] = m
        print(
            f"  {m['name']:<16}{m['n_rules']:>7}{0:>9.3f}"
            f"{(m['silent_error_rate'] or 0):>10.3f}{m['escalation_rate']:>9.3f}"
            f"{0:>10.3f}{m['coverage']:>9.3f}{0:>8}"
        )

    OUT.mkdir(exist_ok=True)
    (OUT / "frontier.json").write_text(json.dumps(
        {"_env": environment(seed=args.seed), "corpus": stats, "results": results},
        indent=2, default=str))
    print(f"\n  -> {OUT/'frontier.json'}")


def cmd_models(args) -> None:
    from harness.proposers import list_openrouter_models
    for mid, price in list_openrouter_models(args.grep):
        print(f"  {mid:<52}{price}")


def cmd_llm(args) -> None:
    corpus = generate_corpus(args.n, seed=args.seed)

    if args.provider == "openrouter":
        from harness.proposers import OpenRouterProposer
        model = args.model or "deepseek/deepseek-v4-flash"
        proposer = OpenRouterProposer(model=model)
    else:
        from harness.proposers import AnthropicProposer
        model = args.model or "claude-haiku-4-5-20251001"
        proposer = AnthropicProposer(model=model)
    engine = RuleEngine()

    print(f"corriendo {args.n} casos con {proposer.name}")
    print("(solo las escalaciones cuestan una llamada; el resto es local)\n")

    def progress(idx, total, n_rules, n_esc):
        if idx % 25 == 0 or idx == total - 1:
            print(f"  caso {idx+1:>5}/{total}   reglas={n_rules:<5} llamadas={n_esc:<5}",
                  end="\r", flush=True)

    res = run_shadow(corpus, engine, proposer, on_progress=progress)
    print("\n")

    m = res.metrics
    print("=" * 60)
    print("RESULTADO")
    print("=" * 60)
    for key in ("reuse_rate", "silent_error_rate", "n_rules",
                "escalation_rate", "final_decile_escalation_rate",
                "coverage", "conflicts", "dead_rules",
                "proposal_action_accuracy", "rejected_rules",
                "failed_proposals", "llm_calls"):
        print(f"  {key:<32}{m.get(key)}")
    print("\n  curva de escalacion por decil:")
    print(f"  {m['escalation_curve_by_decile']}")
    # This used to print "frontier to beat (keep_k k=4): sil.err 0.173 with 113
    # rules". It was withdrawn on August 6, 2026: that frontier was INVALIDATED
    # as a quality reference. The keep_k rules all have k conditions, so their
    # specificity is uniform and arbitration can never invert them; they are
    # immune to the defect that sinks the real policy. keep_k(k=4) scores BETTER
    # than the true policy under this engine (0.173 versus 0.214 silent error).
    # See results/FINDINGS.md.
    print("\n  AVISO: sin el Paso 0 (python3 -m harness.ceiling_check) en ~100%,")
    print("  estas cifras no son interpretables. Techo medido: 58.75%.")

    OUT.mkdir(exist_ok=True)
    (OUT / "llm_run.json").write_text(json.dumps({
        "_env": environment(seed=args.seed, n=args.n, provider=args.provider),
        "model": model,
        "metrics": m,
        "rules": [r.as_dict() for r in res.rules],
        # Raw per-case records. They are not analysed now, but storing them
        # allows any later slicing (error by class, by rule, by decile) without
        # paying for the run again.
        "records": [vars(r) for r in res.records],
    }, indent=2, default=str))
    print(f"\n-> {OUT/'llm_run.json'}  (reglas con su 'note' + registros crudos)")


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("frontier")
    f.add_argument("--n", type=int, default=2000)
    f.add_argument("--seed", type=int, default=17)
    f.set_defaults(func=cmd_frontier)

    l = sub.add_parser("llm")
    l.add_argument("--n", type=int, default=2000)
    l.add_argument("--seed", type=int, default=17)
    l.add_argument("--provider", choices=("openrouter", "anthropic"),
                   default="openrouter")
    l.add_argument("--model", default=None, help="slug exacto; ver subcomando 'models'")
    l.set_defaults(func=cmd_llm)

    mo = sub.add_parser("models", help="buscar el slug exacto en OpenRouter")
    mo.add_argument("grep", nargs="?", default="")
    mo.set_defaults(func=cmd_models)

    args = p.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
