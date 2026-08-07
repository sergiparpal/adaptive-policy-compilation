"""
The true hidden policy.

EXPERIMENTAL INVARIANT: this module is the ORACLE. It exists to label the corpus
and to measure offline. It must NEVER be consulted by the rule engine, by the
proposer or by any component of the online loop.

Deliberate structure: priority layers with exceptions, not independent rules.
First match wins. 29 rules.

Every rule is expressible in the harness.dsl DSL (rung 1: realizable).
"""

from __future__ import annotations

from .domain import Case


def _off(c: Case) -> bool:
    return c.off_hours


# Ordered list of (id, predicate, action). First match wins.
HIDDEN_RULES: list[tuple[str, object, str]] = [
    # --- Layer 0: security overrides --------------------------------------
    ("H01", lambda c: c.has_security_keyword and c.customer_tier in ("business", "enterprise"), "SECURITY_INCIDENT"),
    ("H02", lambda c: c.has_security_keyword and c.severity <= 2, "SECURITY_INCIDENT"),
    # exception: low-impact security mentions on small accounts
    ("H03", lambda c: c.has_security_keyword, "T2_TECHNICAL"),

    # --- Layer 1: SLO and on-call ------------------------------------------
    ("H04", lambda c: c.severity == 1 and c.customer_tier == "enterprise", "ONCALL_ESCALATION"),
    ("H05", lambda c: c.severity == 1 and c.customer_tier == "business" and _off(c), "ONCALL_ESCALATION"),
    ("H06", lambda c: c.severity == 1 and c.customer_tier == "business", "T3_ENGINEERING"),
    ("H07", lambda c: c.severity == 1 and c.product == "api", "T3_ENGINEERING"),
    ("H08", lambda c: c.severity == 1, "T2_TECHNICAL"),

    # --- Layer 2: billing ---------------------------------------------------
    ("H09", lambda c: c.product == "billing" and c.customer_tier == "enterprise", "ACCOUNT_MANAGER"),
    ("H10", lambda c: c.product == "billing" and c.severity <= 2, "BILLING_SPECIALIST"),
    ("H11", lambda c: c.product == "billing" and c.prior_tickets_30d >= 3, "BILLING_SPECIALIST"),
    ("H12", lambda c: c.product == "billing", "SELF_SERVICE_DEFLECT"),

    # --- Layer 3: churn risk -----------------------------------------------
    ("H13", lambda c: c.customer_tier == "enterprise" and c.prior_tickets_30d >= 5, "ACCOUNT_MANAGER"),
    ("H14", lambda c: c.customer_tier == "business" and c.prior_tickets_30d >= 8, "ACCOUNT_MANAGER"),

    # --- Layer 4: product routing ------------------------------------------
    ("H15", lambda c: c.product == "api" and c.severity <= 2, "T3_ENGINEERING"),
    ("H16", lambda c: c.product == "api", "T2_TECHNICAL"),
    ("H17", lambda c: c.product == "integrations" and c.severity <= 2, "T3_ENGINEERING"),
    ("H18", lambda c: c.product == "integrations", "T2_TECHNICAL"),
    ("H19", lambda c: c.product == "mobile" and c.severity == 2, "T2_TECHNICAL"),
    ("H20", lambda c: c.product == "dashboard" and c.severity <= 2, "T2_TECHNICAL"),

    # --- Layer 5: language and staffing (long tail) ------------------------
    ("H21", lambda c: c.language == "pt" and c.severity <= 2, "T2_TECHNICAL"),
    ("H22", lambda c: c.channel == "phone" and c.customer_tier == "free", "SELF_SERVICE_DEFLECT"),
    ("H23", lambda c: c.channel == "phone" and _off(c) and c.customer_tier != "enterprise", "T1_GENERAL"),

    # --- Layer 6: deflection ------------------------------------------------
    ("H24", lambda c: c.customer_tier == "free" and c.severity >= 3, "SELF_SERVICE_DEFLECT"),
    ("H25", lambda c: c.customer_tier == "free" and c.prior_tickets_30d == 0, "SELF_SERVICE_DEFLECT"),
    ("H26", lambda c: c.severity == 4 and c.prior_tickets_30d == 0, "SELF_SERVICE_DEFLECT"),

    # --- Layer 7: defaults --------------------------------------------------
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
