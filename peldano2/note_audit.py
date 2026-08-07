"""
Auditoria de notas y de uso de atributos.

Dos cosas que la comparativa numerica no captura:

  * QUE ATRIBUTOS usa cada base. Una base que solo mira dos atributos no puede
    ejecutar una politica de ocho capas, por bien arbitrada que este.
  * CUANTAS NOTAS ARGUMENTAN DISJUNCION explicitamente. El recuento por palabras
    clave es tosco, asi que ademas se vuelcan las notas enteras: el recuento
    orienta, la cita es la prueba.

Uso:  python3 -m peldano2.note_audit results2/llm_run2_*.json
"""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

from harness.domain import ATTRIBUTES
from harness.provenance import environment

# Marcadores de razonamiento hacia la disjuncion. Deliberadamente literales:
# no se cuenta "solape" a secas, solo formas que afirman NO compartir casos.
MARKERS = [
    r"\bdisjunt", r"\bno se solapa", r"\bsin solapa", r"\bno solapa",
    r"\bsin coincidir", r"\bno coincide", r"\bcubre el hueco", r"\bel hueco\b",
    r"\bmutuamente excluyente", r"\bexcluyente", r"\bno cubierto por",
    r"\bno pisa", r"\bevita(r)? solapa",
]
RX = re.compile("|".join(MARKERS), re.IGNORECASE)


def audit(path: Path) -> dict:
    d = json.loads(path.read_text())
    rules = d["rules"]
    used = collections.Counter(c["attr"] for r in rules for c in r["conditions"])
    hits = [r for r in rules if RX.search(r.get("note", "") or "")]
    return {
        "file": path.name,
        "version": d.get("prompt_version", "v1"),
        "seed": d.get("seed"),
        "n_rules": len(rules),
        "attrs_used": {a: used.get(a, 0) for a in ATTRIBUTES},
        "attrs_never_used": [a for a in ATTRIBUTES if not used.get(a)],
        "notes_arguing_disjointness": len(hits),
        "notes_total": len(rules),
        "examples": [{"rule_id": r["rule_id"], "action": r["action"],
                      "conditions": " AND ".join(
                          f"{c['attr']} {c['op']} {c['value']}" for c in r["conditions"]),
                      "fire_count": r["fire_count"],
                      "correct_count": r["correct_count"],
                      "note": r["note"]} for r in hits],
    }


def main(argv: list[str]) -> int:
    rows = [audit(Path(p)) for p in sorted(argv)]

    print("=" * 100)
    print("ATRIBUTOS USADOS POR BASE")
    print("=" * 100)
    print(f"  {'fichero':<30}{'ver':>4}{'sem':>5}{'regl':>6}   " +
          "".join(f"{a[:7]:>9}" for a in ATTRIBUTES))
    for r in rows:
        print(f"  {r['file']:<30}{r['version']:>4}{str(r['seed']):>5}{r['n_rules']:>6}   " +
              "".join(f"{r['attrs_used'][a]:>9}" for a in ATTRIBUTES))
    print("\n  atributos NUNCA usados:")
    for r in rows:
        print(f"    {r['file']:<30}{r['attrs_never_used']}")

    print()
    print("=" * 100)
    print("NOTAS QUE ARGUMENTAN DISJUNCION")
    print("=" * 100)
    for r in rows:
        n, t = r["notes_arguing_disjointness"], r["notes_total"]
        print(f"  {r['file']:<30}{r['version']:>4}  {n:>3}/{t:<4}"
              f"  ({n/t:.0%})" if t else "")

    print("\n  citas literales:")
    for r in rows:
        if not r["examples"]:
            continue
        print(f"\n  --- {r['file']} ({r['version']}, semilla {r['seed']}) ---")
        for e in r["examples"]:
            acc = f"{e['correct_count']}/{e['fire_count']}" if e["fire_count"] else "sin disparos"
            print(f"    [{e['rule_id']}] {e['conditions']} -> {e['action']}   ({acc})")
            print(f"      \"{e['note']}\"")

    out = Path("results2/note_audit.json")
    # 7 ago 2026: igual que en compare_runs.py, la lista pasa a "rows" dentro de
    # un objeto para poder colgar `_env`, y el registro se re-corrio ese mismo
    # dia con las 8 tiradas: misma forma nueva, mismas filas. Y la misma
    # trampa: reescribe con lo que se le pase como argumento.
    out.write_text(json.dumps({"_env": environment(), "rows": rows},
                              indent=2, ensure_ascii=False))
    print(f"\n-> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
