"""Diagnose patch 3 anchor A."""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BS = chr(92)
SC = BS + "textsc{"
old = ("The structured stage recalls 41/51 (0.804, Wilson [0.675, 0.890]) at "
       "suppression 0.800 (Wilson [0.627, 0.905]) and precision 0.872. Of its 41 "
       "confirmations, 24 are " + SC + "Confirmed} in all-component form and 17 "
       "carry at least one " + SC + "Human-Review component---twelve routed by "
       "the majority of their three runs, two more losing their majority under "
       "forced scoring only because a single " + SC + "Human-Review vote splits "
       "the other two, and the remaining three confirmed two-to-one on ordinary "
       "votes with a single " + SC + "Human-Review component alongside. The "
       "three-run case agreement is 70.4" + BS + "% (57 of 81 cases), and 20.6"
       + BS + "% of all full-stage verdicts---50 of the 243 case judgments pooled "
       "across the three runs---route to review.")

txt = open("TestVDB.tex", encoding="utf-8").read()
i = txt.find("The structured stage recalls")
print("start at", i)
seg = txt[i:i + len(old) + 60]
for k in range(len(old) + 1):
    if k == len(old):
        print("FULL MATCH")
        break
    if old[:k + 1] not in seg[:k + 1]:
        print("mismatch at", k)
        print("old:", repr(old[max(0, k - 50):k + 15]))
        print("tex:", repr(seg[max(0, k - 50):k + 15]))
        break
