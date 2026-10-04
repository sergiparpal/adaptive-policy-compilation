"""
`PLAN_EDGES.md` — what the edges the proposer declared at write time bought.

Zero API calls. It reads `PLAN_REUSE.md`'s three Stage B records as they stand,
and nothing it writes lands under `results_reuse/` or `results_fidelity/`. Every
writer of the package refuses while the plan is unsigned (`edges/plan.py`).
"""
