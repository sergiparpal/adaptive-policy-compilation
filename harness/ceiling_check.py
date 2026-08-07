"""
Techo del motor: precision maxima alcanzable con la politica PERFECTA cargada.

Codifica las 29 reglas de hidden_policy.py directamente en el DSL y las pasa por
el motor. Ningun LLM interviene. Si el motor no alcanza 1.0 con la politica
verdadera dentro, el techo no lo pone el proponente: lo pone el motor.

Compara dos politicas de arbitraje sobre EXACTAMENTE el mismo conjunto de reglas:

  * especificidad  -- la que implementa RuleEngine.decide: gana la regla con mas
                      condiciones; empate con acciones distintas -> CONFLICT.
  * prioridad      -- gana la regla mas antigua que case (orden de nacimiento),
                      sin mirar especificidad. Con las reglas cargadas en el
                      orden de HIDDEN_RULES esto es exactamente la semantica
                      "primera que casa gana" de la politica oculta.

ANALISIS, NO MODIFICACION. No toca dsl.py: el arbitraje alternativo se
implementa aqui y reutiliza Rule.matches() del DSL congelado, de modo que la
unica diferencia entre las dos mediciones es el arbitraje.

Uso:  python3 -m harness.ceiling_check
"""

from __future__ import annotations

import collections
import itertools
import sys

from .domain import DOMAINS, Case, generate_corpus
from .dsl import Condition, Rule, RuleEngine
from .hidden_policy import HIDDEN_RULES, true_action, true_rule_id


# ---------------------------------------------------------------------------
# Las 29 reglas ocultas, transcritas al DSL
# ---------------------------------------------------------------------------
# Cada entrada es (id, [(attr, op, value), ...], accion) y reproduce LITERALMENTE
# el cuerpo del predicado correspondiente en HIDDEN_RULES, en el mismo orden.
#
# Unica traduccion no literal: H29 es `lambda c: True`, y validate_rule_payload
# exige al menos una condicion. Se codifica como `severity gte 1`, que es cierto
# en todo el dominio (severity in 1..4). verify_encoding() lo comprueba.

HIDDEN_DSL: list[tuple[str, list[tuple[str, str, object]], str]] = [
    # --- Capa 0: overrides de seguridad -----------------------------------
    ("H01", [("has_security_keyword", "eq", True),
             ("customer_tier", "in", ["business", "enterprise"])], "SECURITY_INCIDENT"),
    ("H02", [("has_security_keyword", "eq", True),
             ("severity", "lte", 2)], "SECURITY_INCIDENT"),
    ("H03", [("has_security_keyword", "eq", True)], "T2_TECHNICAL"),

    # --- Capa 1: SLO y guardia ---------------------------------------------
    ("H04", [("severity", "eq", 1), ("customer_tier", "eq", "enterprise")], "ONCALL_ESCALATION"),
    ("H05", [("severity", "eq", 1), ("customer_tier", "eq", "business"),
             ("off_hours", "eq", True)], "ONCALL_ESCALATION"),
    ("H06", [("severity", "eq", 1), ("customer_tier", "eq", "business")], "T3_ENGINEERING"),
    ("H07", [("severity", "eq", 1), ("product", "eq", "api")], "T3_ENGINEERING"),
    ("H08", [("severity", "eq", 1)], "T2_TECHNICAL"),

    # --- Capa 2: facturacion ------------------------------------------------
    ("H09", [("product", "eq", "billing"),
             ("customer_tier", "eq", "enterprise")], "ACCOUNT_MANAGER"),
    ("H10", [("product", "eq", "billing"), ("severity", "lte", 2)], "BILLING_SPECIALIST"),
    ("H11", [("product", "eq", "billing"),
             ("prior_tickets_30d", "gte", 3)], "BILLING_SPECIALIST"),
    ("H12", [("product", "eq", "billing")], "SELF_SERVICE_DEFLECT"),

    # --- Capa 3: riesgo de fuga --------------------------------------------
    ("H13", [("customer_tier", "eq", "enterprise"),
             ("prior_tickets_30d", "gte", 5)], "ACCOUNT_MANAGER"),
    ("H14", [("customer_tier", "eq", "business"),
             ("prior_tickets_30d", "gte", 8)], "ACCOUNT_MANAGER"),

    # --- Capa 4: enrutado por producto -------------------------------------
    ("H15", [("product", "eq", "api"), ("severity", "lte", 2)], "T3_ENGINEERING"),
    ("H16", [("product", "eq", "api")], "T2_TECHNICAL"),
    ("H17", [("product", "eq", "integrations"), ("severity", "lte", 2)], "T3_ENGINEERING"),
    ("H18", [("product", "eq", "integrations")], "T2_TECHNICAL"),
    ("H19", [("product", "eq", "mobile"), ("severity", "eq", 2)], "T2_TECHNICAL"),
    ("H20", [("product", "eq", "dashboard"), ("severity", "lte", 2)], "T2_TECHNICAL"),

    # --- Capa 5: idioma y dotacion (cola larga) ----------------------------
    ("H21", [("language", "eq", "pt"), ("severity", "lte", 2)], "T2_TECHNICAL"),
    ("H22", [("channel", "eq", "phone"), ("customer_tier", "eq", "free")], "SELF_SERVICE_DEFLECT"),
    ("H23", [("channel", "eq", "phone"), ("off_hours", "eq", True),
             ("customer_tier", "neq", "enterprise")], "T1_GENERAL"),

    # --- Capa 6: deflexion --------------------------------------------------
    ("H24", [("customer_tier", "eq", "free"), ("severity", "gte", 3)], "SELF_SERVICE_DEFLECT"),
    ("H25", [("customer_tier", "eq", "free"),
             ("prior_tickets_30d", "eq", 0)], "SELF_SERVICE_DEFLECT"),
    ("H26", [("severity", "eq", 4), ("prior_tickets_30d", "eq", 0)], "SELF_SERVICE_DEFLECT"),

    # --- Capa 7: defectos ---------------------------------------------------
    ("H27", [("severity", "lte", 2)], "T2_TECHNICAL"),
    ("H28", [("customer_tier", "in", ["business", "enterprise"])], "T1_GENERAL"),
    ("H29", [("severity", "gte", 1)], "T1_GENERAL"),   # `True` en todo el dominio
]


def build_rules() -> list[Rule]:
    """Reglas del DSL en el orden de HIDDEN_RULES. born_at = posicion en la capa."""
    rules = []
    for i, (rid, conds, action) in enumerate(HIDDEN_DSL):
        rules.append(Rule(
            rule_id=rid,
            conditions=[Condition(attr=a, op=o, value=v) for a, o, v in conds],
            action=action,
            born_at=i,
            note="transcripcion literal de hidden_policy",
        ))
    return rules


# ---------------------------------------------------------------------------
# Verificacion de la transcripcion: exhaustiva sobre el espacio completo
# ---------------------------------------------------------------------------

def all_cases():
    keys = ["has_security_keyword", "severity", "customer_tier", "product",
            "channel", "prior_tickets_30d", "off_hours", "language"]
    for combo in itertools.product(*(DOMAINS[k] for k in keys)):
        yield Case(**dict(zip(keys, combo)))


def verify_encoding(rules: list[Rule]) -> bool:
    """Cada regla DSL debe ser equivalente a su lambda, y la evaluacion
    primera-que-casa sobre el DSL debe reproducir true_action, en TODO el
    espacio de casos (no solo en el corpus)."""
    n = 0
    per_rule_bad = collections.Counter()
    first_match_bad = 0
    for case in all_cases():
        n += 1
        for rule, (hid, pred, _act) in zip(rules, HIDDEN_RULES):
            if rule.matches(case) != bool(pred(case)):
                per_rule_bad[hid] += 1
        for rule in rules:                      # primera que casa
            if rule.matches(case):
                if rule.action != true_action(case):
                    first_match_bad += 1
                break
        else:
            first_match_bad += 1

    print(f"  espacio completo de casos verificado: {n:,}")
    if per_rule_bad:
        print("  DESACUERDOS por regla (DSL vs lambda):")
        for hid, c in per_rule_bad.most_common():
            print(f"    {hid}: {c:,} casos")
    else:
        print("  las 29 reglas DSL son equivalentes a sus lambdas: OK")
    if first_match_bad:
        print(f"  primera-que-casa NO reproduce true_action en {first_match_bad:,} casos")
    else:
        print("  primera-que-casa sobre el DSL reproduce true_action: OK")
    return not per_rule_bad and not first_match_bad


# ---------------------------------------------------------------------------
# Arbitraje alternativo: prioridad por orden de nacimiento
# ---------------------------------------------------------------------------

def decide_by_priority(rules: list[Rule], case: Case):
    """Gana la regla mas antigua que case. Nunca produce CONFLICT: el orden
    total sobre las reglas desempata siempre. Reutiliza Rule.matches() del DSL."""
    matched = [r for r in rules if r.matches(case)]
    if not matched:
        return "IMPASSE", None, []
    winner = min(matched, key=lambda r: r.born_at)
    return "ACTION", winner, matched


# ---------------------------------------------------------------------------
# Medicion
# ---------------------------------------------------------------------------

def measure(corpus, decide_fn, label):
    out = collections.Counter()
    n_correct = 0
    wrong = []          # (caso, verdad, predicho, regla ganadora)
    conflicts = []      # (caso, verdad, finalistas)
    for case in corpus:
        outcome, winner, matched = decide_fn(case)
        out[outcome] += 1
        truth = true_action(case)
        if outcome == "ACTION":
            if winner.action == truth:
                n_correct += 1
            else:
                wrong.append((case, truth, winner.action, winner.rule_id))
        elif outcome == "CONFLICT":
            conflicts.append((case, truth, [r.rule_id for r in matched]))
    n = len(corpus)
    n_act = out["ACTION"]
    return {
        "label": label,
        "n": n,
        "action": n_act,
        "impasse": out["IMPASSE"],
        "conflict": out["CONFLICT"],
        "coverage": n_act / n,
        "accuracy_on_covered": (n_correct / n_act) if n_act else None,
        "silent_error_rate": (1 - n_correct / n_act) if n_act else None,
        "silent_errors_abs": n_act - n_correct,
        "accuracy_end_to_end": n_correct / n,
        "wrong": wrong,
        "conflicts": conflicts,
    }


def report(m):
    print(f"\n  {m['label']}")
    print(f"    ACTION {m['action']:>5}   IMPASSE {m['impasse']:>4}   CONFLICT {m['conflict']:>4}")
    print(f"    cobertura                {m['coverage']:.4f}")
    print(f"    exactitud sobre cubiertos {m['accuracy_on_covered']:.4f}")
    print(f"    ERROR SILENCIOSO          {m['silent_error_rate']:.4f}   "
          f"({m['silent_errors_abs']} casos)")
    print(f"    exactitud extremo a extremo {m['accuracy_end_to_end']:.4f}")


def main() -> int:
    corpus = generate_corpus(2000, seed=17)
    rules = build_rules()

    print("=" * 74)
    print("VERIFICACION DE LA TRANSCRIPCION")
    print("=" * 74)
    ok = verify_encoding(rules)
    if not ok:
        print("\n  La transcripcion NO es fiel. Los techos de abajo no valen.")
        return 1

    print()
    print("=" * 74)
    print("TECHO DEL MOTOR CON LA POLITICA PERFECTA CARGADA (n=2000, semilla 17)")
    print("=" * 74)
    print("  29 reglas, ningun LLM, ninguna regla aprendida.")

    engine = RuleEngine()
    engine.rules = rules
    m_spec = measure(corpus, engine.decide, "ARBITRAJE POR ESPECIFICIDAD (RuleEngine.decide, el actual)")
    m_prio = measure(corpus, lambda c: decide_by_priority(rules, c),
                     "ARBITRAJE POR PRIORIDAD (orden de nacimiento, primera que casa)")
    report(m_spec)
    report(m_prio)

    # ---- de que se compone el fallo de la especificidad ------------------
    print()
    print("=" * 74)
    print("DESGLOSE DEL FALLO POR ESPECIFICIDAD")
    print("=" * 74)

    print(f"\n  a) CONFLICTOS: {len(m_spec['conflicts'])} casos")
    pairs = collections.Counter(tuple(sorted(c[2])) for c in m_spec["conflicts"])
    for finalists, cnt in pairs.most_common(10):
        acts = {r: a for r, _, a in
                [(rid, None, dict((h, ac) for h, _p, ac in HIDDEN_RULES)[rid]) for rid in finalists]}
        desc = "  vs  ".join(f"{r}->{acts[r]}" for r in finalists)
        print(f"    {cnt:>4}  {desc}")

    print(f"\n  b) ACCION EQUIVOCADA (error silencioso): {len(m_spec['wrong'])} casos")
    conf = collections.Counter((true_rule_id(c), w, p) for c, w, p, _ in
                               [(c, t, p, r) for c, t, p, r in m_spec["wrong"]])
    print(f"    {'capa correcta':<16}{'verdad':<22}{'predicho':<22}{'casos':>6}")
    for (hid, truth, pred), cnt in conf.most_common(12):
        print(f"    {hid:<16}{truth:<22}{pred:<22}{cnt:>6}")

    print(f"\n  c) reglas que ganan indebidamente (por tener mas condiciones):")
    winners = collections.Counter(r for _, _, _, r in m_spec["wrong"])
    h2a = dict((h, ac) for h, _p, ac in HIDDEN_RULES)
    for rid, cnt in winners.most_common(10):
        print(f"    {rid} -> {h2a[rid]:<22}{cnt:>5} casos robados")

    print(f"\n  d) por clase verdadera, cuantos casos pierde la especificidad:")
    per_class_tot = collections.Counter(true_action(c) for c in corpus)
    per_class_bad = collections.Counter(t for _, t, _, _ in m_spec["wrong"])
    per_class_conf = collections.Counter(t for _, t, _ in m_spec["conflicts"])
    print(f"    {'clase':<24}{'corpus':>8}{'err.sil':>9}{'conflicto':>11}{'intactos':>10}")
    for cls in sorted(per_class_tot, key=lambda k: -per_class_tot[k]):
        tot = per_class_tot[cls]
        bad = per_class_bad.get(cls, 0)
        cf = per_class_conf.get(cls, 0)
        print(f"    {cls:<24}{tot:>8}{bad:>9}{cf:>11}{tot-bad-cf:>10}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
