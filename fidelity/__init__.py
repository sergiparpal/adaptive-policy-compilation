"""PLAN_FIDELITY.md — would the model have decided as its rules do?

`plan` holds the gate and the constants; `replay` rebuilds a Stage B record of
PLAN_REUSE.md case by case, and `prompts` builds prompt v1 on the rebuilt base.
The three stages are `sample` (A, free: the checks, the draw and the readout),
`ask` (B, the only one that spends) and `score` (C, free). Nothing here writes a
record while the plan carries a blank signature line.
"""
