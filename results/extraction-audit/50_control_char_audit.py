"""Audit TestVDB.tex for control characters that a shell heredoc can inject
when a LaTeX backslash escape (\\alpha, \\ref, \\texttt) is interpreted as a
C-style escape. Reports the exact line and surrounding context so the damage
can be repaired, and checks that the intended commands survived."""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = "TestVDB.tex"
s = io.open(P, encoding="utf-8").read()

NAMES = {7: "BEL", 8: "BS", 9: "TAB", 11: "VT", 12: "FF", 13: "CR"}
found = [(i, ord(c)) for i, c in enumerate(s) if ord(c) in NAMES]
print(f"control chars: {len(found)}")
for i, cp in found:
    line = s[:i].count(chr(10)) + 1
    ctx = s[max(0, i - 70):i + 30].replace(chr(10), " / ")
    print(f"  line {line}: {NAMES[cp]} U+{cp:04X}")
    print(f"     ...{ctx}...")

print()
for probe in (r"Section~\ref{sec:eval}",
              r"Section~\ref{subsec:confirmation}",
              r"\texttt{wait=false}",
              r"\alpha{=}0.05",
              r"Section \ref{sec:limitations}"):
    print(f"  {s.count(probe)}x  {probe}")
