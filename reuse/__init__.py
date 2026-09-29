"""PLAN_REUSE.md — the founding question, on the engine that can answer it.

`plan` holds the gate and the constants, `analysis` the arithmetic of §5.2 and
§5.3, `frontier` the `keep_k` reference, `gates` the blocking checks of §6, and
the three stages are `readout` (A, free), `run` (B, the only one that spends)
and `score` (C, free). Nothing here writes a record while §0 of the plan is
unsigned.
"""
