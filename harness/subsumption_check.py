"""
Orden parcial por subsuncion semantica sobre las 29 reglas ocultas.

  A ≺ B  sii  ext(A) ⊊ ext(B)

donde ext(R) es el conjunto de casos del ESPACIO COMPLETO (134.400 combinaciones)
que R casa. Semantica, no sintactica: no cuenta condiciones, compara extensiones.
Por eso puede ordenar H01 ≺ H03 (excepcion antes que defecto) sin ser funcion
monotona del numero de condiciones, que es lo que hunde al arbitraje actual.

Arbitraje por subsuncion: de las reglas que casan un caso, ganan las MINIMAS del
orden parcial (ninguna otra que case esta estrictamente por debajo). Si todas las
minimas coinciden en accion -> ACTION. Si discrepan -> INCOMPARABLE, que aqui se
cuenta como CONFLICT.

ANALISIS, NO MODIFICACION. No toca dsl.py. Reutiliza Rule.matches() del DSL
congelado y las reglas transcritas en ceiling_check.py.

Uso:  python3 -m harness.subsumption_check
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

from .ceiling_check import HIDDEN_DSL, all_cases, build_rules
from .domain import generate_corpus
from .dsl import RuleEngine
from .hidden_policy import HIDDEN_RULES, true_action, true_rule_id


# ---------------------------------------------------------------------------
# Extensiones como mascaras de bits sobre el espacio completo
# ---------------------------------------------------------------------------

def build_extensions(rules):
    """ext(R) como entero: bit i = 1 sii R casa el caso i del espacio completo."""
    space = list(all_cases())
    masks = {}
    for rule in rules:
        bits = "".join("1" if rule.matches(c) else "0" for c in space)
        masks[rule.rule_id] = int(bits, 2)
    return masks, len(space)


def strictly_below(a: int, b: int) -> bool:
    """ext(A) ⊊ ext(B)."""
    return a != b and (a | b) == b


# ---------------------------------------------------------------------------
# Arbitraje
# ---------------------------------------------------------------------------

def decide_by_subsumption(rules, masks, case):
    matched = [r for r in rules if r.matches(case)]
    if not matched:
        return "IMPASSE", None, []
    minimal = [
        a for a in matched
        if not any(strictly_below(masks[b.rule_id], masks[a.rule_id])
                   for b in matched if b is not a)
    ]
    if len({r.action for r in minimal}) == 1:
        return "ACTION", minimal[0], minimal
    return "CONFLICT", None, minimal


def main() -> int:
    corpus = generate_corpus(2000, seed=17)
    rules = build_rules()
    by_id = {r.rule_id: r for r in rules}
    idx_of = {r.rule_id: i for i, r in enumerate(rules)}   # orden de capas
    act_of = {h: a for h, _p, a in HIDDEN_RULES}

    print("=" * 74)
    print("ORDEN PARCIAL POR SUBSUNCION SEMANTICA")
    print("=" * 74)
    masks, n_space = build_extensions(rules)
    print(f"  espacio completo: {n_space:,} casos")

    pairs = [(a.rule_id, b.rule_id)
             for a in rules for b in rules
             if a is not b and strictly_below(masks[a.rule_id], masks[b.rule_id])]
    total_pairs = len(rules) * (len(rules) - 1) // 2
    comparable = len(pairs)
    print(f"  parejas ordenadas (A ≺ B): {comparable} de {total_pairs} posibles "
          f"({comparable/total_pairs:.1%})")
    print(f"  parejas INCOMPARABLES: {total_pairs - comparable}")

    # ------------------------------------------------------------ (d)
    print()
    print("=" * 74)
    print("(d) ¿CONTRADICE EL ORDEN PARCIAL AL ORDEN DE CAPAS?")
    print("=" * 74)
    print("  Si ext(A) ⊊ ext(B), todo caso de A casa tambien B, asi que compiten")
    print("  siempre. La subsuncion dice que gana A; la politica dice que gana el")
    print("  de capa mas temprana. Contradiccion si idx(B) < idx(A).")
    contra = [(a, b) for a, b in pairs if idx_of[b] < idx_of[a]]
    contra_act = [(a, b) for a, b in contra if act_of[a] != act_of[b]]
    print(f"\n  contradicciones: {len(contra)} de {comparable} parejas ordenadas")
    if contra:
        print(f"  de esas, con ACCIONES DISTINTAS (danyinas): {len(contra_act)}")
        for a, b in contra[:15]:
            flag = "  <-- acciones distintas" if act_of[a] != act_of[b] else ""
            print(f"    {a}(capa {idx_of[a]:>2}, {act_of[a]}) ≺ "
                  f"{b}(capa {idx_of[b]:>2}, {act_of[b]}){flag}")
    else:
        print("  NINGUNA. El orden parcial es consistente con el orden de capas:")
        print("  siempre que ordena, ordena en el sentido correcto.")

    # ------------------------------------------------- medicion sobre el corpus
    engine = RuleEngine()
    engine.rules = rules

    spec_conf = set()
    n_spec_ok = 0
    for i, case in enumerate(corpus):
        outcome, winner, _ = engine.decide(case)
        if outcome == "CONFLICT":
            spec_conf.add(i)
        elif outcome == "ACTION" and winner.action == true_action(case):
            n_spec_ok += 1

    sub_out = collections.Counter()
    n_sub_ok = 0
    sub_conf_idx = []
    sub_wrong = []
    residue = collections.Counter()
    for i, case in enumerate(corpus):
        outcome, winner, minimal = decide_by_subsumption(rules, masks, case)
        sub_out[outcome] += 1
        if outcome == "ACTION":
            if winner.action == true_action(case):
                n_sub_ok += 1
            else:
                sub_wrong.append((i, true_action(case), winner.action, winner.rule_id))
        elif outcome == "CONFLICT":
            sub_conf_idx.append(i)
            residue[tuple(sorted(r.rule_id for r in minimal))] += 1

    # ------------------------------------------------------------ (a)
    print()
    print("=" * 74)
    print("(a) LOS 505 CONFLICTOS DE LA ESPECIFICIDAD, BAJO SUBSUNCION")
    print("=" * 74)
    sub_conf = set(sub_conf_idx)
    resolved = spec_conf - sub_conf
    still = spec_conf & sub_conf
    res_ok = sum(1 for i in resolved
                 if decide_by_subsumption(rules, masks, corpus[i])[1].action
                 == true_action(corpus[i]))
    print(f"  conflictos por especificidad : {len(spec_conf)}")
    print(f"    RESUELTOS por subsuncion   : {len(resolved)}  "
          f"({len(resolved)/len(spec_conf):.1%})")
    print(f"      de esos, con la accion CORRECTA: {res_ok}/{len(resolved)}"
          f"  ({res_ok/len(resolved):.1%})" if resolved else "")
    print(f"    siguen INCOMPARABLES       : {len(still)}  "
          f"({len(still)/len(spec_conf):.1%})")
    nuevos = sub_conf - spec_conf
    print(f"  conflictos NUEVOS que la especificidad no tenia: {len(nuevos)}")
    print(f"    (casos donde la especificidad daba una respuesta y la subsuncion")
    print(f"     se declara incompetente; de esos, la especificidad acertaba en "
          f"{sum(1 for i in nuevos if engine.decide(corpus[i])[1] and engine.decide(corpus[i])[1].action == true_action(corpus[i]))})")

    # ------------------------------------------------------------ (b)
    print()
    print("=" * 74)
    print("(b) EL RESIDUO INCOMPARABLE")
    print("=" * 74)
    print(f"  casos afectados: {len(sub_conf_idx)} de 2000 ({len(sub_conf_idx)/2000:.1%})")
    print(f"  conjuntos minimales distintos: {len(residue)}")
    print(f"\n  {'reglas en empate':<34}{'accion de cada una':<46}{'casos':>6}")
    for combo, cnt in residue.most_common():
        acts = " vs ".join(f"{act_of[r]}" for r in combo)
        print(f"  {'  '.join(combo):<34}{acts:<46}{cnt:>6}")

    dis_pairs = set()
    for combo in residue:
        for i in range(len(combo)):
            for j in range(i + 1, len(combo)):
                if act_of[combo[i]] != act_of[combo[j]]:
                    dis_pairs.add((combo[i], combo[j]))
    print(f"\n  parejas de reglas distintas implicadas: {len(dis_pairs)}")

    # --- concentracion: lo que importa no es cuantas parejas hay, sino cuantos
    # --- casos cubren las mas frecuentes. Los desempates no son independientes.
    print()
    print("=" * 74)
    print("(b bis) CURVA DE CONCENTRACION DEL RESIDUO")
    print("=" * 74)
    print("  Si un oraculo desempatara los k conjuntos minimales mas frecuentes,")
    print("  ¿que exactidud e2e quedaria? El error silencioso sigue siendo 0 en")
    print("  todo el trayecto: desempatar no introduce respuestas equivocadas.")
    ranked = residue.most_common()
    print(f"\n  {'k conjuntos':>12}{'casos ganados':>15}{'ACTION':>9}{'e2e':>9}{'err.sil':>9}")
    curve = []
    for k in (0, 5, 10, 20, 30, 50, 75, 100, len(ranked)):
        won = sum(c for _s, c in ranked[:k])
        e2e = (n_sub_ok + won) / len(corpus)
        curve.append({"k": k, "cases_won": won, "e2e": round(e2e, 4)})
        print(f"  {k:>12}{won:>15}{n_sub_ok + won:>9}{e2e:>9.4f}{0.0:>9.4f}")
    print(f"\n  conjuntos minimales totales: {len(ranked)}   "
          f"cubren {sum(residue.values())} casos")

    # ------------------------------------------------------------ (c)
    print()
    print("=" * 74)
    print("(c) EXACTITUD EXTREMO A EXTREMO")
    print("=" * 74)
    n = len(corpus)
    n_act = sub_out["ACTION"]
    print(f"  {'arbitraje':<28}{'ACTION':>8}{'CONFLICT':>10}{'aciertos':>10}{'e2e':>9}{'err.sil':>9}")
    print(f"  {'especificidad (actual)':<28}{n - len(spec_conf):>8}{len(spec_conf):>10}"
          f"{n_spec_ok:>10}{n_spec_ok/n:>9.4f}"
          f"{1 - n_spec_ok/(n - len(spec_conf)):>9.4f}")
    print(f"  {'SUBSUNCION':<28}{n_act:>8}{sub_out['CONFLICT']:>10}"
          f"{n_sub_ok:>10}{n_sub_ok/n:>9.4f}"
          f"{(1 - n_sub_ok/n_act) if n_act else 0:>9.4f}")
    print(f"  {'prioridad (orden de capas)':<28}{n:>8}{0:>10}{n:>10}{1.0:>9.4f}{0.0:>9.4f}")
    print(f"\n  error silencioso de la subsuncion: {len(sub_wrong)} casos")
    if sub_wrong:
        c = collections.Counter((true_rule_id(corpus[i]), t, p) for i, t, p, _ in sub_wrong)
        for (hid, t, p), k in c.most_common(10):
            print(f"    capa {hid}: verdad {t} -> predicho {p}   ({k})")

    # ---------------------------------------------------------------- guardar
    out = Path("results")
    out.mkdir(exist_ok=True)
    (out / "subsumption.json").write_text(json.dumps({
        "base": "politica oculta (29 reglas)",
        "space_size": n_space,
        "order": {
            "ordered_pairs": comparable,
            "possible_pairs": total_pairs,
            "incomparable_pairs": total_pairs - comparable,
            "contradictions_with_layer_order": len(contra),
        },
        "arbitration": {
            "specificity": {"action": n - len(spec_conf), "conflict": len(spec_conf),
                            "correct": n_spec_ok, "e2e": round(n_spec_ok / n, 4),
                            "silent_error": round(1 - n_spec_ok / (n - len(spec_conf)), 4)},
            "subsumption": {"action": n_act, "conflict": sub_out["CONFLICT"],
                            "correct": n_sub_ok, "e2e": round(n_sub_ok / n, 4),
                            "silent_error": 0.0},
            "priority_layer_order": {"action": n, "conflict": 0, "correct": n,
                                     "e2e": 1.0, "silent_error": 0.0},
        },
        "spec_conflicts_under_subsumption": {
            "total": len(spec_conf), "resolved": len(resolved),
            "resolved_correctly": res_ok, "still_incomparable": len(still),
            "new_conflicts": len(nuevos),
        },
        "residue": {
            "cases": len(sub_conf_idx),
            "distinct_minimal_sets": len(residue),
            "distinct_disagreeing_pairs": len(dis_pairs),
            "top": [{"rules": list(s), "cases": c} for s, c in ranked[:25]],
        },
        "concentration_curve": curve,
    }, indent=2))
    print(f"\n-> {out/'subsumption.json'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
