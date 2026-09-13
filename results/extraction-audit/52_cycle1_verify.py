"""Cycle-1 fix verification: every new value must be present and every
superseded value must be gone from TestVDB.tex."""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

s = io.open("TestVDB.tex", encoding="utf-8").read()

MUST_APPEAR = [
    r"\textbf{The twelve misses.}",
    "The full stage's 12 false negatives decompose into four mechanisms",
    "The remaining two are the recall side of the cognition-anchor cleanup",
    "seven upheld---four reusing their earlier hand-outcomes and three newly confirmed",
    "11 routed cases (eight confirmations and three false positives",
    "15 of the full stage's 39 confirmations carry at least one",
    "force-closes 7 of those 15 routed confirmations",
    "figures/pipeline-v10",
    "postdates the pool and contributed none of the 81",
    "The silence is not an artifact of the suite probing only the synchronous",
    r"Section~\ref{sec:eval}",
    r"(Section~\ref{subsec:confirmation}, perspective B)",
    r"$\alpha{=}0.05$",
    "docchecker24",
    "c4rllama25",
    "The ledger is cumulative across the mining rounds and versions of early--mid 2026",
    "survives Holm correction on the confirmed-set unit",
    "the paired difference in \\emph{confirmed sets} is 48 vs.\\ 34",
    "cannot emit \\textsc{Human-Review} and its forced and convention rates coincide",
    "every rate below is computed on the rebuilt, cleaned packs",
    "whose three runs are collapsed to its majority row",
    "a schema bounds field types and, where it declares them, numeric ranges",
]

MUST_BE_GONE = [
    r"\textbf{The ten misses.}",
    "The full stage's 10 false negatives",
    "six upheld",
    "12 of the full stage's 39 confirmations",
    "closes 7 of those 12",
    "figures/pipeline-v9",
    "D-only",
    "and several endpoints serve no schema",
    "An earlier draft attributed the silence",
    "Section 4 is computed",
    "same corrected level as the flagship pair",
    "accumulated across the earlier GLM-5.2 mining rounds plus the reported",
]

bad = 0
for t in MUST_APPEAR:
    n = s.count(t)
    if n == 0:
        print(f"FAIL missing x{n}: {t[:72]}")
        bad += 1
print(f"present checks: {len(MUST_APPEAR) - bad}/{len(MUST_APPEAR)}")

bad2 = 0
for t in MUST_BE_GONE:
    n = s.count(t)
    if n:
        print(f"FAIL still present x{n}: {t[:72]}")
        bad2 += 1
print(f"absent checks: {len(MUST_BE_GONE) - bad2}/{len(MUST_BE_GONE)}")
print("RESULT:", "OK" if bad == 0 and bad2 == 0 else "PROBLEMS")
