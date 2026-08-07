"""
Politica verdadera oculta.

INVARIANTE EXPERIMENTAL: este modulo es el ORACULO. Sirve para etiquetar el
corpus y para medir offline. NUNCA debe ser consultado por el motor de reglas,
por el proponente ni por ningun componente del bucle online.

Estructura deliberada: capas de prioridad con excepciones, no reglas
independientes. Primera coincidencia gana. 29 reglas.

Toda regla es expresable en el DSL de harness.dsl (peldano 1: realizable).
"""

from __future__ import annotations

from .domain import Case


def _off(c: Case) -> bool:
    return c.off_hours


# Lista ordenada de (id, predicado, accion). Primera que casa, gana.
HIDDEN_RULES: list[tuple[str, object, str]] = [
    # --- Capa 0: overrides de seguridad -----------------------------------
    ("H01", lambda c: c.has_security_keyword and c.customer_tier in ("business", "enterprise"), "SECURITY_INCIDENT"),
    ("H02", lambda c: c.has_security_keyword and c.severity <= 2, "SECURITY_INCIDENT"),
    # excepcion: menciones de seguridad de bajo impacto en cuentas pequenas
    ("H03", lambda c: c.has_security_keyword, "T2_TECHNICAL"),

    # --- Capa 1: SLO y guardia ---------------------------------------------
    ("H04", lambda c: c.severity == 1 and c.customer_tier == "enterprise", "ONCALL_ESCALATION"),
    ("H05", lambda c: c.severity == 1 and c.customer_tier == "business" and _off(c), "ONCALL_ESCALATION"),
    ("H06", lambda c: c.severity == 1 and c.customer_tier == "business", "T3_ENGINEERING"),
    ("H07", lambda c: c.severity == 1 and c.product == "api", "T3_ENGINEERING"),
    ("H08", lambda c: c.severity == 1, "T2_TECHNICAL"),

    # --- Capa 2: facturacion ------------------------------------------------
    ("H09", lambda c: c.product == "billing" and c.customer_tier == "enterprise", "ACCOUNT_MANAGER"),
    ("H10", lambda c: c.product == "billing" and c.severity <= 2, "BILLING_SPECIALIST"),
    ("H11", lambda c: c.product == "billing" and c.prior_tickets_30d >= 3, "BILLING_SPECIALIST"),
    ("H12", lambda c: c.product == "billing", "SELF_SERVICE_DEFLECT"),

    # --- Capa 3: riesgo de fuga --------------------------------------------
    ("H13", lambda c: c.customer_tier == "enterprise" and c.prior_tickets_30d >= 5, "ACCOUNT_MANAGER"),
    ("H14", lambda c: c.customer_tier == "business" and c.prior_tickets_30d >= 8, "ACCOUNT_MANAGER"),

    # --- Capa 4: enrutado por producto -------------------------------------
    ("H15", lambda c: c.product == "api" and c.severity <= 2, "T3_ENGINEERING"),
    ("H16", lambda c: c.product == "api", "T2_TECHNICAL"),
    ("H17", lambda c: c.product == "integrations" and c.severity <= 2, "T3_ENGINEERING"),
    ("H18", lambda c: c.product == "integrations", "T2_TECHNICAL"),
    ("H19", lambda c: c.product == "mobile" and c.severity == 2, "T2_TECHNICAL"),
    ("H20", lambda c: c.product == "dashboard" and c.severity <= 2, "T2_TECHNICAL"),

    # --- Capa 5: idioma y dotacion (cola larga) ----------------------------
    ("H21", lambda c: c.language == "pt" and c.severity <= 2, "T2_TECHNICAL"),
    ("H22", lambda c: c.channel == "phone" and c.customer_tier == "free", "SELF_SERVICE_DEFLECT"),
    ("H23", lambda c: c.channel == "phone" and _off(c) and c.customer_tier != "enterprise", "T1_GENERAL"),

    # --- Capa 6: deflexion --------------------------------------------------
    ("H24", lambda c: c.customer_tier == "free" and c.severity >= 3, "SELF_SERVICE_DEFLECT"),
    ("H25", lambda c: c.customer_tier == "free" and c.prior_tickets_30d == 0, "SELF_SERVICE_DEFLECT"),
    ("H26", lambda c: c.severity == 4 and c.prior_tickets_30d == 0, "SELF_SERVICE_DEFLECT"),

    # --- Capa 7: defectos ---------------------------------------------------
    ("H27", lambda c: c.severity <= 2, "T2_TECHNICAL"),
    ("H28", lambda c: c.customer_tier in ("business", "enterprise"), "T1_GENERAL"),
    ("H29", lambda c: True, "T1_GENERAL"),
]

HIDDEN_POLICY_SIZE = len(HIDDEN_RULES)


def true_action(case: Case) -> str:
    for _rid, pred, action in HIDDEN_RULES:
        if pred(case):
            return action
    raise AssertionError("politica oculta sin catch-all")


def true_rule_id(case: Case) -> str:
    for rid, pred, _action in HIDDEN_RULES:
        if pred(case):
            return rid
    raise AssertionError("politica oculta sin catch-all")
