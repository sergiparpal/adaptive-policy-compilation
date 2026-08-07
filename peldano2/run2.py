"""
Rung 2, run with the real proposer.

  python3 -m peldano2.run2 --n 100
  python3 -m peldano2.run2 --n 2000 --model deepseek/deepseek-v4-flash

Writes to results2/. Never touches results/.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from harness.domain import generate_corpus
from harness.provenance import environment
from harness.record_guard import FLAG, or_exit, refuse_overwrite

from .engine2 import PriorityEngine, Space
from .proposers2 import OpenRouterProposer2
from .shadow2 import run_shadow2

OUT = Path("results2")

PINNED_SEED = 17


def default_tag(n: int, seed: int, prompt_version: str) -> str:
    """The tag when `--tag` says nothing.

    Until August 8, 2026 it was just `n{n}`, which left out the two other
    things that change what comes out: the seed and the prompt version. So
    `--n 100 --prompt-version v2` — the rung 2 command the README recommends —
    wrote `llm_run2_n100.json`, on top of the v1 record with that same name.

    The rule reproduces the names the eight runs already carry on disk:
    `n100`, `n100_v2`, `n100_seed18`, `n100_v2_seed18`.
    """
    v = "" if prompt_version == "v1" else f"_{prompt_version}"
    s = "" if seed == PINNED_SEED else f"_seed{seed}"
    return f"n{n}{v}{s}"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=2000)
    p.add_argument("--seed", type=int, default=PINNED_SEED)
    p.add_argument("--model", default="deepseek/deepseek-v4-flash")
    p.add_argument("--prompt-version", default="v1", choices=("v1", "v2"))
    p.add_argument("--tag", default=None)
    p.add_argument("--out", default=None,
                   help="fichero de salida; por defecto results2/llm_run2_<tag>.json")
    # Not called --force on purpose: the name says what it does.
    p.add_argument(FLAG, dest="overwrite_record", action="store_true",
                   help="sobrescribir el registro que ya haya en el destino")
    args = p.parse_args()

    # Before generating the corpus and before building the proposer: this run
    # costs money and the destination is checked while nothing has been spent.
    tag = args.tag or default_tag(args.n, args.seed, args.prompt_version)
    destino = or_exit(
        refuse_overwrite,
        Path(args.out) if args.out else OUT / f"llm_run2_{tag}.json",
        overwrite=args.overwrite_record,
        exits=("--out OTRO_FICHERO    escribir en otro sitio",
               "--tag OTRA_ETIQUETA    cambiar solo el sufijo",
               f"{FLAG}    sobrescribir este a proposito"))

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

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps({
        "_env": environment(),
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
    print(f"\n-> {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
