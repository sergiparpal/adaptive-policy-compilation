"""
Audit of notes and of attribute usage.

Two things the numeric comparison does not capture:

  * WHICH ATTRIBUTES each base uses. A base that only looks at two attributes
    cannot execute an eight-layer policy, however well arbitrated it is.
  * HOW MANY NOTES ARGUE FOR DISJOINTNESS explicitly. The keyword count is
    crude, so the whole notes are dumped as well: the count orients, the
    quotation is the evidence.

Usage:  python3 -m peldano2.note_audit results2/llm_run2_*.json
"""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

from harness.domain import ATTRIBUTES
from harness.provenance import environment

# Markers of reasoning towards disjointness. Deliberately literal: a bare
# "solape" is not counted, only forms asserting that cases are NOT shared.
# The patterns stay in Spanish: the notes they match are in Spanish.
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
    # Aug 7, 2026: as in compare_runs.py, the list moves to "rows" inside an
    # object so that `_env` can be hung off it, and the record was re-run that
    # same day with the 8 runs: same new shape, same rows. And the same trap:
    # it rewrites with whatever is passed as an argument.
    out.write_text(json.dumps({"_env": environment(), "rows": rows},
                              indent=2, ensure_ascii=False))
    print(f"\n-> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
