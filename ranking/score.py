"""
Stage C of `PLAN_RANKING.md`: scoring, and the five adjudications. Zero API
calls.

It refuses while the plan is unsigned and while Stage A's record or the
session's is missing, before it measures, builds or writes anything. It refuses
a session record produced under another protocol or behind another Stage A
record. Then it runs `M-g1` to `M-g3` again, all blocking.

WHAT EACH ROW READS (§0 and §9). The unit is one valid ask; `M-b` to `M-e` are
read on the median over the valid asks.

  M-a  over every ask of the session: the share that are valid, against 0.90;
       and `W - A` over the valid ones, against 0.05. Both must hold.
  M-b  the median of `score(r, hibrido · corpus test split 0)`, strictly above
       the cell's born_at floor plus P-d's margin, read from the record.
  M-c  the same median, at or above the cell's published `stage_c`.
  M-d  the median of `predicts(r) − predicts(stage_c)` over the 1,479 declared
       answers of the learned base, at or above 0.00.
  M-e  the median of each ask's reading on `K-b`'s 65 units, strictly above
       the declarations' published reading.
  M-f  reported: §0's list.

A reading compared with a line read from a record is compared at the
precision that record publishes (`plan.at_record_precision`). **With fewer than
`plan.MIN_VALID_ASKS` valid asks, `M-b` to `M-e` are unadjudicable**, and the
record says so. **A verdict is labelled *thin*** when at least one valid ask
falls on the other side of its line from the median; the label does not change
the verdict. Both rules are §0's, settled before the signature.

    python3 -m ranking.score --dry-run              # M-g1..M-g4; writes nothing
    PYTHONHASHSEED=0 python3 -m ranking.score       # refuses while unsigned
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
from typing import Any, Sequence

from harness.provenance import describe, environment

from . import ask as stage_b
from . import gates
from . import instrument as I
from . import plan


# ---------------------------------------------------------------------------
# The arithmetic of §0, on plain values
# ---------------------------------------------------------------------------

def side(value: float, line: float, strict: bool) -> bool:
    return value > line if strict else value >= line


def adjudicate(values: Sequence[float], line: float, strict: bool,
               record_precision: bool) -> dict[str, Any]:
    """A median over the valid asks against a line. `strict` is `>` against
    `>=`; `record_precision` rounds every value as the line's record does."""
    if len(values) < plan.MIN_VALID_ASKS:
        return {"unadjudicable": True, "holds": None, "thin": None,
                "n": len(values), "median": None, "line": line,
                "why": f"fewer than {plan.MIN_VALID_ASKS} valid asks"}
    vs = [plan.at_record_precision(v) for v in values] if record_precision else list(values)
    med = statistics.median(vs)
    holds = side(med, line, strict)
    return {"unadjudicable": False, "holds": holds,
            "thin": any(side(v, line, strict) != holds for v in vs),
            "n": len(vs), "median": med, "line": line,
            "op": ">" if strict else ">=",
            "min": min(vs), "max": max(vs), "values": vs}


def m_a(rows: Sequence[dict]) -> dict[str, Any]:
    """Validity over every ask; the slot over the valid ones."""
    n = len(rows)
    valid = [r for r in rows if r["valid"]]
    share = len(valid) / n if n else 0.0
    gap = I.slot_gap([(r["pid"], r["pass"], r["ranking"]) for r in valid])
    validity_holds = share >= plan.MIN_VALID_SHARE
    slot_holds = gap["gap"] is not None and gap["gap"] <= plan.M_A_MAX_SLOT_GAP
    return {"asks": n, "valid": len(valid), "validity": share,
            "validity_holds": validity_holds, **gap, "slot_holds": slot_holds,
            "holds": validity_holds and slot_holds,
            "line": {"validity": f">= {plan.MIN_VALID_SHARE}",
                     "slot_gap": f"<= {plan.M_A_MAX_SLOT_GAP}"}}


def m_d_values(rankings: Sequence[Sequence[str]], answers: Sequence[I.Answer]
               ) -> tuple[list[float], dict[str, int]]:
    """Each ask's `predicts(r) − predicts(stage_c)`, over the same answers."""
    base, n = I.predicts(I.STAGE_C, answers)
    return [(I.predicts(r, answers)[0] - base) / n for r in rankings], \
        {"stage_c_hits": base, "n": n}


# ---------------------------------------------------------------------------
# One ask, read every way
# ---------------------------------------------------------------------------

def read_ask(inst: I.Instrument, r: Sequence[str], la, ha, er) -> dict[str, Any]:
    return {"scores": I.scores(inst, r),
            "predicts": {"learned": list(I.predicts(r, la)),
                         "hidden": list(I.predicts(r, ha))},
            "k_b_pairs": {key: I.blind_reading(r, er, key)
                          for key in ("space_out", "corpus_out")}}


def call_summary(rows: Sequence[dict]) -> dict[str, Any]:
    atts = [a for r in rows for a in r.get("call_attempts") or []]
    return {"attempts": len(atts),
            "providers": dict(Counter(str(a.get("provider")) for a in atts)),
            "models": dict(Counter(str(a.get("model")) for a in atts)),
            "finish_reasons": dict(Counter(str(a.get("finish_reason")) for a in atts)),
            "native_finish_reasons": dict(Counter(str(a.get("native_finish_reason"))
                                                  for a in atts)),
            "reasoning_tokens": sum(a.get("reasoning_tokens") or 0 for a in atts),
            "errors": dict(Counter(str(a.get("error")) for a in atts if a.get("error")))}


def score_session(inst: I.Instrument, sample: dict, session: dict,
                  percentiles: bool = True) -> dict[str, Any]:
    rows = session["rows"]
    lines = sample["lines"]
    la, ha = I.learned_answers(), I.hidden_answers()
    er = I.blind_edge_rows()
    valid = [r for r in rows if r["valid"]]
    rankings = [r["ranking"] for r in valid]
    asks = [{"pid": r["pid"], "pass": r["pass"], "ranking": r["ranking"],
             "why": (r.get("payload") or {}).get("why"),
             **read_ask(inst, r["ranking"], la, ha, er)} for r in valid]
    signed = I.cell_name(*plan.SIGNED_CELL)

    a = m_a(rows)
    b = adjudicate([x["scores"][signed] for x in asks], lines["M-b"]["line"],
                   strict=True, record_precision=True)
    c = adjudicate([x["scores"][signed] for x in asks], lines["M-c"]["line"],
                   strict=False, record_precision=True)
    d_vals, d_base = m_d_values(rankings, la)
    d = {**adjudicate(d_vals, plan.M_D_MIN_GAP, strict=False, record_precision=False),
         **d_base}
    e = adjudicate([x["k_b_pairs"]["space_out"]["reading"] for x in asks],
                   lines["M-e"]["line"], strict=True, record_precision=True)

    agg = I.borda(rankings) if rankings else None
    stated_share = {f"{x} vs {y}": (sum(I.above(r)[(x, y)] for r in rankings)
                                    / len(rankings) if rankings else None)
                    for x, y in I.QUEUE_PAIRS}
    pct = {}
    if percentiles and asks:
        for pool, surface in I.CELLS:
            dist = I.distribution(inst, pool, surface)
            name = I.cell_name(pool, surface)
            pct[name] = {"asks": [I.percentile(x["scores"][name], dist) for x in asks],
                         "stage_c": I.percentile(I.score(inst, I.STAGE_C, pool, surface),
                                                 dist)}
    m_d_hidden = m_d_values(rankings, ha)
    return {
        "verdicts": {"M-a": a, "M-b": b, "M-c": c, "M-d": d, "M-e": e},
        "M-f": {
            "asks": asks,
            "invalid": [{"pid": r["pid"], "pass": r["pass"], "payload": r["payload"],
                         "raw_answers": r.get("raw_answers"), "failure": r["failure"],
                         "finish_reasons": [x.get("finish_reason")
                                            for x in r.get("call_attempts") or []]}
                        for r in rows if not r["valid"]],
            "per_presentation": {pid: [x["ranking"] for x in asks if x["pid"] == pid]
                                 for pid in sorted({r["pid"] for r in rows})},
            "percentiles": pct,
            "borda": None if agg is None else {"order": agg,
                                                **read_ask(inst, agg, la, ha, er)},
            "stated_against_revealed": {
                "share_of_asks_ranking_the_first_above": stated_share,
                "revealed_learned": sample["revealed"]["learned"]["by_queue_pair"],
                "revealed_hidden": sample["revealed"]["hidden"]["by_queue_pair"],
                "agreement_with_revealed_learned": [
                    I.agreement(r, sample["revealed"]["learned"]["order"])
                    for r in rankings],
                "agreement_with_stage_c": [I.agreement(r, I.STAGE_C) for r in rankings]},
            "m_d_on_the_hidden_policys_pairs": {
                "values": m_d_hidden[0], **m_d_hidden[1],
                "median": statistics.median(m_d_hidden[0]) if m_d_hidden[0] else None},
            "m_e_on_the_corpus": {
                "values": [x["k_b_pairs"]["corpus_out"]["reading"] for x in asks],
                "declarations": sample["declarations"]["corpus_out"]["reading"],
                "stage_c": sample["stage_c"]["k_b_pairs"]["corpus_out"]["reading"]},
            "calls": call_summary(rows),
        },
    }


def load(path, what: str) -> dict:
    if not path.exists():
        sys.exit(f"\nREFUSED: {what} is not there: {path}\n")
    return json.loads(path.read_text())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage C of PLAN_RANKING.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run M-g1 to M-g4 and stop; writes nothing")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_checks(suite=True, progress=True)
        gates.report(checks)
        print("\ndry run: nothing scored, nothing written")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"ranking/score.py writes {plan.SCORE_PATH}")
    sample = load(plan.SAMPLE_PATH, "Stage A's record")
    session = load(plan.ask_path("session"), "the session's record")
    wrong = {k: session.get(k) for k, v in stage_b.protocol().items()
             if session.get(k) != v}
    if wrong:
        sys.exit(f"\nREFUSED: the session was not produced under this protocol: "
                 f"{wrong}\n")
    if session.get("sample_sha256") != stage_b.sample_sha256():
        sys.exit("\nREFUSED: the session was asked behind another Stage A record.\n")
    checks = gates.run_checks(suite=True, progress=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")

    out = score_session(checks.instrument, sample, session)
    for name, v in out["verdicts"].items():
        state = ("unadjudicable" if v.get("unadjudicable") else
                 "holds" if v["holds"] else "refuted")
        thin = ", thin" if v.get("thin") else ""
        print(f"  {name}  {state}{thin}")
    plan.SCORE_PATH.write_text(json.dumps({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "stage": "C",
        "protocol": stage_b.protocol(),
        "sample_sha256": stage_b.sample_sha256(),
        "session_record": str(plan.ask_path("session")),
        "signed_cell": I.cell_name(*plan.SIGNED_CELL),
        "gates": checks.summary(),
        **out,
    }, indent=2, default=str))
    print(f"\n-> {plan.SCORE_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
