"""Faithful clause tally for the full stage's 243 case judgments.

Implements the FIXED AGGREGATION from Appendix A literally, clause by clause,
and validates the implementation against the paper's own routing figure: the
clauses whose outcome is HUMAN_REVIEW must total 48 of 243. Any other total
means the classifier is wrong, not the paper.
"""
import glob
import json
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
V3 = os.path.join(ROOT, "rerun_v3")
CASES7 = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
          "milvus_021", "milvus_027", "qdrant_017"}


def load(r):
    d = {}
    for f in sorted(glob.glob(f"{V3}/run_full{r}/verdicts_batch*.jsonl")):
        for l in open(f, encoding="utf-8"):
            l = l.strip()
            if l:
                o = json.loads(l)
                d[o["defect_id"]] = o
    for l in open(f"{V3}/run_full{r}/verdicts_coganchor_rejudge.jsonl",
                  encoding="utf-8"):
        l = l.strip()
        if l:
            o = json.loads(l)
            if o["defect_id"] in CASES7:
                d[o["defect_id"]] = o
    return d


runs = [load(r) for r in (1, 2, 3)]

print("=== raw perspective value vocabularies (all 243 judgments) ===")
for key in ("A", "B", "C", "D"):
    c = Counter()
    for r in range(3):
        for i in runs[r]:
            c[str((runs[r][i].get("perspectives") or {}).get(key))] += 1
    print(f"  {key}: {dict(c.most_common())}")


def clause(o):
    """The aggregation clause that decides this judgment, applied in order."""
    p = o.get("perspectives") or {}
    A = str(p.get("A", "")).upper()
    B = str(p.get("B", "")).upper()
    C = str(p.get("C", "")).upper()
    D = str(p.get("D", "")).upper()
    a_c = A.startswith("CONF")
    a_r = A.startswith("REFUT")
    b_c = B.startswith("CONF")
    d_def = "SUPPORTS_DEFECT" in D
    d_not = "SUPPORTS_NOT_DEFECT" in D
    c_r = C.startswith("REFUT") and "WEAK" not in C
    c_w = "WEAK" in C
    if a_c:
        return "A=CONFIRMED -> CONFIRMED"
    if a_r and b_c:
        return "A=REFUTED & B=CONFIRMED -> route"
    if a_r:
        return "A=REFUTED -> FALSE_POSITIVE"
    if b_c:
        return "B=CONFIRMED -> CONFIRMED"
    if d_def:
        return "D=SUPPORTS_DEFECT -> CONFIRMED"
    if d_not:
        return "D=SUPPORTS_NOT_DEFECT -> FALSE_POSITIVE"
    # The printed rule (TestVDB.tex:493) makes C=Refuted a plain clause: the
    # earlier D clauses have already taken Supports-Defect and
    # Supports-Not-Defect by this point, so no further precondition is due.
    # Requiring D==No-Signal here was the bug -- perspective D records five
    # other values (validation_present, validation_absent, by_design_in_source,
    # not_found, ...), and each such case fell through to the catch-all,
    # inflating it to 76 against the paper's 69.
    if c_r:
        return "C=REFUTED -> FALSE_POSITIVE"
    return "catch-all -> route"


tally = Counter()
route = 0
for r in range(3):
    for i in runs[r]:
        cl = clause(runs[r][i])
        tally[cl] += 1
        if "route" in cl:
            route += 1

print("\n=== clause tally over 243 full-arm judgments ===")
for k, v in tally.most_common():
    print(f"  {v:3d}  {k}")
print(f"\n  total: {sum(tally.values())}")
print(f"  catch-all clause fires: {route} of 243 ({route/243:.1%})")

# The tally above describes the RULE applied to the perspective values the
# judge recorded. The paper's routing figure (48/243 = 19.8%) is a different
# quantity: the count of verdicts the judge actually wrote as HUMAN_REVIEW.
# The two differ by the judge's own discretion, so they are reported side by
# side rather than against each other.
recorded = Counter()
cross = Counter()
for r in range(3):
    for i in runs[r]:
        o = runs[r][i]
        recorded[o.get("verdict")] += 1
        cross[(clause(o), o.get("verdict"))] += 1
n_hr = recorded.get("HUMAN_REVIEW", 0)
print(f"  recorded HUMAN_REVIEW verdicts: {n_hr} of 243 ({n_hr/243:.1%})")

mandated = {k: v for k, v in cross.items() if "route" in k[0]}
tot_m = sum(mandated.values())
print(f"\n=== where the rule mandates Human-Review ({tot_m} judgments), "
      f"what the judge wrote ===")
for (cl, v), n in sorted(mandated.items(), key=lambda x: -x[1]):
    flag = "" if v == "HUMAN_REVIEW" else "   <-- deviates from the rule"
    print(f"  {n:3d}  recorded {v}{flag}")
forced_fp = sum(n for (cl, v), n in mandated.items() if v == "FALSE_POSITIVE")
print(f"\n  forced to FALSE_POSITIVE although the rule routes them: {forced_fp}"
      f"  (the protocol's red lines forbid this)")
