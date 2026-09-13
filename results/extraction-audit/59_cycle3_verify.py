"""Cycle-3 fix verification."""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
s = io.open("TestVDB.tex", encoding="utf-8").read()

MUST_APPEAR = [
    "three of the nine already carried a majority",
    "three of the seven already carried a majority",
    r"reads the routing channel as an \emph{upper bound}",
    "catalogue of objective constraint classes",
    "is deterministic and reads no documentation",
    "trace26",
    "among its nine leaks",
    "the reported run's registrations came from",
    "tied with the unconsumed-top-level-field family",
    "the clauses below apply in the order given, and where two fire the earlier governs",
    "carries a source-grounding section",
    "the complete released template space",
    "its API-sequence-mutation stage targets",
    "applying the flagship pair's multiplier~4",
    "never turns that signal into an oracle",
    "induces invariants from observed request/response traffic",
    "for reasons that recur across both sides' rejects",
]
MUST_BE_GONE = [
    "on which our Qdrant defects",
    "the study counts a case the way the deployment resolves it",
    "Every verdict is grounded in the implementation source",
    "the largest single block",
    "AGORA+ infers invariants from observed traffic",
    "includes three candidates the stage confirms",
    "converts the cases both judges find unresolvable",
    "for their endpoint",
]
bad = [t for t in MUST_APPEAR if not s.count(t)]
gone = [t for t in MUST_BE_GONE if s.count(t)]
for t in bad:
    print("FAIL missing:", t[:70])
for t in gone:
    print("FAIL still present:", t[:70])
print(f"present {len(MUST_APPEAR) - len(bad)}/{len(MUST_APPEAR)}; "
      f"absent {len(MUST_BE_GONE) - len(gone)}/{len(MUST_BE_GONE)}")
print("RESULT:", "OK" if not bad and not gone else "PROBLEMS")
