"""
Peldano 2, tirada con proponente real.

  python3 -m peldano2.run2 --n 100
  python3 -m peldano2.run2 --n 2000 --model deepseek/deepseek-v4-flash

Escribe en results2/. Nunca toca results/.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from harness.domain import generate_corpus

from .engine2 import PriorityEngine, Space
from .proposers2 import OpenRouterProposer2
from .shadow2 import run_shadow2

OUT = Path("results2")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=2000)
    p.add_argument("--seed", type=int, default=17)
    p.add_argument("--model", default="deepseek/deepseek-v4-flash")
    p.add_argument("--prompt-version", default="v1", choices=("v1", "v2"))
    p.add_argument("--tag", default=None)
    args = p.parse_args()

    corpus = generate_corpus(args.n, seed=args.seed)
    engine = PriorityEngine(space=Space())
    proposer = OpenRouterProposer2(model=args.model,
                                   prompt_version=args.prompt_version)

    print(f"peldano 2: {args.n} casos con {proposer.name}")
    print("(solo las escalaciones cuestan una llamada)\n")

    def progress(idx, total, n_rules, n_esc):
        if idx % 25 == 0 or idx == total - 1:
            print(f"  caso {idx+1:>5}/{total}   reglas={n_rules:<5} llamadas={n_esc:<5}",
                  end="\r", flush=True)

    res = run_shadow2(corpus, engine, proposer, on_progress=progress)
    print("\n")

    m = res.metrics
    print("=" * 62)
    print("RESULTADO")
    print("=" * 62)
    for k in ("n_rules", "reuse_rate", "silent_error_rate", "e2e_accuracy",
              "coverage", "escalation_rate", "final_decile_escalation_rate",
              "impasses", "conflicts", "dead_rules",
              "proposal_action_accuracy", "rejected_rules", "failed_proposals",
              "llm_calls"):
        print(f"  {k:<32}{m.get(k)}")
    print("\n  --- prioridad declarada ---")
    for k in ("edges_proposed", "edges_accepted", "rules_with_edges",
              "subsumption_pairs", "escalations_on_conflict",
              "escalations_with_base_shown"):
        print(f"  {k:<32}{m.get(k)}")
    print(f"  {'edge_reasons':<32}{m.get('edge_reasons')}")
    print(f"\n  curva de escalacion por decil: {m['escalation_curve_by_decile']}")

    OUT.mkdir(exist_ok=True)
    tag = args.tag or f"n{args.n}"
    path = OUT / f"llm_run2_{tag}.json"
    path.write_text(json.dumps({
        "peldano": 2,
        "model": args.model,
        "n": args.n,
        "seed": args.seed,
        "prompt_version": args.prompt_version,
        "system_prompt": proposer.system_prompt,
        "metrics": m,
        "rules": [r.as_dict() for r in res.rules],
        "edge_log": engine.edge_log,
        "records": [vars(r) for r in res.records],
    }, indent=2, default=str))
    print(f"\n-> {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
