"""Cycle-2 fix verification."""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
s = io.open("TestVDB.tex", encoding="utf-8").read()

MUST_APPEAR = [
    "30 more true bugs than false positives where the flat judge confirms 26",
    "Youden's $J$ 0.465 vs.\\ 0.455",
    "(25 vs.\\ 22; $F_1$ 0.698 vs.\\ 0.651; $J$ 0.422 vs.\\ 0.363)",
    "30 vs.\\ 26 net on the primary family, 25 vs.\\ 22 on the second",
    "Structured-source oracles",
    "the structured protocol escalates to explicit human-review decisions",
    "(the ten affected packs sat in four of the flat arm's six runs",
    "by the authors, non-blind, under the pack-materials rule",
    "one of the 51 maintainer-confirmed bugs",
    "Qdrant \\#9045, where a silently accepted zero-length vector",
    "which now sits among the 30 adjudicated false positives",
    "the clauses below apply in the order given",
    "for reasons that recur across both sides' rejects",
    "no deterministic-oracle family we analyze",
    "whose rows 2--6 are argued from each family's anchoring mechanism",
    "the ``source-only-Qwen'' rows of Table~\\ref{tab:rq2-single}",
]
MUST_BE_GONE = [
    "REST doc/spec-derived oracles",
    "converts the cases both judges find unresolvable",
    "only 2 of the 51 maintainer-confirmed bugs",
    "reclassified the candidate.",
    "4 were rejected on the materials alone---",
]
bad = sum(1 for t in MUST_APPEAR if not s.count(t))
gone = sum(1 for t in MUST_BE_GONE if s.count(t))
for t in MUST_APPEAR:
    if not s.count(t):
        print("FAIL missing:", t[:70])
for t in MUST_BE_GONE:
    if s.count(t):
        print("FAIL still present:", t[:70])
print(f"present {len(MUST_APPEAR) - bad}/{len(MUST_APPEAR)}; "
      f"absent {len(MUST_BE_GONE) - gone}/{len(MUST_BE_GONE)}")
print("RESULT:", "OK" if not bad and not gone else "PROBLEMS")
