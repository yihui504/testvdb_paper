"""Repair the three shell-heredoc injuries in TestVDB.tex: a BEL that replaced
the backslash of \\alpha, and the two stray-space Section references."""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = "TestVDB.tex"
s = io.open(P, encoding="utf-8").read()

fixes = [
    ("$" + chr(7) + "lpha{=}0.05$", "$\\alpha{=}0.05$"),
    (r"Section \ref{sec:limitations}", r"Section~\ref{sec:limitations}"),
]
for old, new in fixes:
    n = s.count(old)
    s = s.replace(old, new)
    label = old.replace(chr(7), "<BEL>")
    print(f"{n}x  {label!r} -> {new!r}")

io.open(P, "w", encoding="utf-8").write(s)

s2 = io.open(P, encoding="utf-8").read()
print("\nremaining control chars:",
      sum(1 for c in s2 if ord(c) == 7))
print("\\alpha{=}0.05 :", s2.count("\\alpha{=}0.05"))
print("stray-space refs:", s2.count("Section \ref{sec:limitations}"))
print("tied refs       :", s2.count("Section~\\ref{sec:limitations}"))
