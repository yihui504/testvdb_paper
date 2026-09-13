"""Diagnose why patch 2's anchor does not match the tex."""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BS = chr(92)
SC = BS + "textsc{"
old = ("The decomposition, however, locates the mechanism precisely. Under "
       "forced-verdict-only scoring (" + SC + "Human-Review} not counted as "
       "confirmation), the full stage recalls 0.529 (27/51) and the flat judge "
       "0.490 (25/51)---indistinguishable ($p{=}0.51$). The full-vs-flat "
       "separation is therefore carried by the routing channel, not by "
       "forced-verdict accuracy: the structured protocol converts the cases both "
       "judges find unresolvable into explicit human-review decisions (17 of the "
       "full stage's 41 confirmations) instead of forced closures, and the flat "
       "judge---which shares the three-valued verdict space but has no aggregation "
       "rule that mandates routing, and in the primary family routes only 8.6"
       + BS + "% of its verdicts (21 of 243 pooled across its three runs)---closes 10 "
       "of those 17 routed confirmations as " + SC + "False-Positive.")

txt = open("TestVDB.tex", encoding="utf-8").read()
i = txt.find("The decomposition, however")
seg = txt[i:i + len(old) + 80]
for k in range(len(old) + 1):
    if k == len(old):
        print("FULL MATCH at", k)
        break
    if old[:k + 1] not in seg[:k + 1]:
        print("mismatch at", k)
        print("old:", repr(old[max(0, k - 45):k + 12]))
        print("tex:", repr(seg[max(0, k - 45):k + 12]))
        break
