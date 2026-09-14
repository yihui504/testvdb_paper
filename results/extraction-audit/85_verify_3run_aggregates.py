"""Verify the paper's three-run full-stage aggregates against the cleaned pool.

R3 (round-16 review) alleges a parity non-closure: per-run rows sum to 141,
majority 48, agreement 55/81 -> n3 = 33.5. This recomputes every printed
quantity from the raw verdict files so we know whether the finding is real,
and whether "case agreement" is defined or undefined.
"""
import glob
import json
import os
from collections import Counter

BASE = r".paperpilot/phase2-rerun/arms/rq2_3run"
V3 = os.path.join(BASE, "rerun_v3")
GT = json.load(open(os.path.join(BASE, "gt_81.json"), encoding="utf-8"))
COGANCHOR = ["milvus_004", "milvus_006", "milvus_018", "milvus_019",
             "milvus_021", "milvus_027", "qdrant_017"]
IS_C = lambda v: v in ("CONFIRMED", "HUMAN_REVIEW")


def load(paths):
    v = {}
    for f in paths:
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if line:
                j = json.loads(line)
                v[j["defect_id"]] = j["verdict"]
    return v


# verdicts_batch*.jsonl already carry the 10-pack cog-strip merge; the 7
# candidate-anchored cases are then overridden by the coganchor rejudge.
merged = {}
for r in (1, 2, 3):
    v = load(sorted(glob.glob(os.path.join(V3, f"run_full{r}",
                                           "verdicts_batch*.jsonl"))))
    assert len(v) == 81, f"run{r} batch pool is {len(v)}, expected 81"
    rj = load([os.path.join(V3, f"run_full{r}",
                            "verdicts_coganchor_rejudge.jsonl")])
    assert sorted(rj) == sorted(COGANCHOR), f"run{r} rejudge ids drift"
    v.update(rj)
    merged[r] = v

cases = sorted(GT)
print(f"cases: {len(cases)}  (GT T={sum(1 for c in cases if GT[c]=='T')}, "
      f"F={sum(1 for c in cases if GT[c]=='F')})")

print("\n=== per-run raw verdict distribution (cleaned pool) ===")
for r in (1, 2, 3):
    d = Counter(merged[r][c] for c in cases)
    conf = sum(IS_C(merged[r][c]) for c in cases)
    print(f"  run{r}: {dict(d)}   confirmed(C+HR)={conf}")

print("\n=== per-run TP/FPleak/FN/TN under the convention ===")
for r in (1, 2, 3):
    tp = sum(IS_C(merged[r][c]) and GT[c] == "T" for c in cases)
    fp = sum(IS_C(merged[r][c]) and GT[c] == "F" for c in cases)
    fn = sum((not IS_C(merged[r][c])) and GT[c] == "T" for c in cases)
    tn = sum((not IS_C(merged[r][c])) and GT[c] == "F" for c in cases)
    print(f"  run{r}: TP={tp} FPleak={fp} FN={fn} TN={tn}   "
          f"rowsum={tp+fp+fn+tn}  confirmed={tp+fp}  sum_all_runs_so_far="
          f"{'' if r==0 else ''}")

runsum = 0
for r in (1, 2, 3):
    runsum += sum(IS_C(merged[r][c]) for c in cases)
print(f"  SUM of per-run confirmed = {runsum}")

maj_c = {c: sum(IS_C(merged[r][c]) for r in (1, 2, 3)) >= 2 for c in cases}
tp = sum(maj_c[c] and GT[c] == "T" for c in cases)
fp = sum(maj_c[c] and GT[c] == "F" for c in cases)
fn = sum((not maj_c[c]) and GT[c] == "T" for c in cases)
tn = sum((not maj_c[c]) and GT[c] == "F" for c in cases)
print(f"\n=== majority (>=2/3, C+HR) ===\n  TP={tp} FPleak={fp} FN={fn} TN={tn} "
      f"confirmed={tp+fp}")

# --- the parity quantities R3 used -------------------------------------------
nk = Counter(sum(IS_C(merged[r][c]) for r in (1, 2, 3)) for c in cases)
print(f"\n=== n_k = cases confirmed in exactly k runs ===\n  {dict(sorted(nk.items()))}")
print(f"  n0={nk[0]} n1={nk[1]} n2={nk[2]} n3={nk[3]}")
print(f"  check: n1+2n2+3n3 = {nk[1]+2*nk[2]+3*nk[3]} (== per-run sum {runsum})")
print(f"  check: n2+n3 = {nk[2]+nk[3]} (== majority {tp+fp})")

raw_unan = sum(1 for c in cases if len({merged[r][c] for r in (1, 2, 3)}) == 1)
bin_unan = sum(1 for c in cases if len({IS_C(merged[r][c]) for r in (1, 2, 3)}) == 1)
print(f"\n=== agreement, two possible definitions ===")
print(f"  raw three-valued identical in all 3 runs : {raw_unan}/81 = {raw_unan/81:.3f}")
print(f"  binary confirm/not identical in all 3    : {bin_unan}/81 = {bin_unan/81:.3f}")
print(f"  (paper prints 67.9% = 55/81)")

# --- the 24 / 15 split the paper prints --------------------------------------
all3_confirmed = sum(1 for c in cases
                     if all(merged[r][c] == "CONFIRMED" for r in (1, 2, 3)))
any_hr = sum(1 for c in cases
             if maj_c[c] and any(merged[r][c] == "HUMAN_REVIEW" for r in (1, 2, 3)))
hr_maj = sum(1 for c in cases
             if sum(merged[r][c] == "HUMAN_REVIEW" for r in (1, 2, 3)) >= 2)
hr_total = sum(sum(merged[r][c] == "HUMAN_REVIEW" for r in (1, 2, 3))
               for c in cases)
print(f"\n=== 24/15 split ===\n  CONFIRMED in all 3 runs: {all3_confirmed}")
print(f"  majority-confirmed carrying >=1 HR: {any_hr}")
print(f"  HR in >=2 of 3 runs (routed): {hr_maj}")
print(f"  pooled HR verdicts: {hr_total}/243 = {hr_total/243:.3f}")
print(f"  majority-confirmed total: {sum(maj_c.values())}")

print("\n=== the same, restricted to the 39 true-positive confirmations ===")
tp_maj = [c for c in cases if maj_c[c] and GT[c] == "T"]
print(f"  |TP majority| = {len(tp_maj)}")
print(f"  all three runs CONFIRMED      : "
      f"{sum(1 for c in tp_maj if all(merged[r][c]=='CONFIRMED' for r in (1,2,3)))}")
print(f"  carrying >=1 HUMAN_REVIEW     : "
      f"{sum(1 for c in tp_maj if any(merged[r][c]=='HUMAN_REVIEW' for r in (1,2,3)))}")
print(f"  HR in >=2 of 3 runs (routed)  : "
      f"{sum(1 for c in tp_maj if sum(merged[r][c]=='HUMAN_REVIEW' for r in (1,2,3))>=2)}")
print(f"  neither (majority C, no HR)   : "
      f"{sum(1 for c in tp_maj if all(merged[r][c]=='CONFIRMED' for r in (1,2,3))==False and not any(merged[r][c]=='HUMAN_REVIEW' for r in (1,2,3)))}")

print("\n=== leak-side majority confirmations (GT=F) ===")
fp_maj = [c for c in cases if maj_c[c] and GT[c] == "F"]
print(f"  |FP majority| = {len(fp_maj)}: {fp_maj}")

# --- per-case vectors for the confirmations ----------------------------------
print("\n=== per-case confirm vectors (majority-confirmed only) ===")
for c in cases:
    if maj_c[c]:
        vec = "".join("C" if merged[r][c] == "CONFIRMED"
                      else ("H" if merged[r][c] == "HUMAN_REVIEW" else "F")
                      for r in (1, 2, 3))
        print(f"  {c:14s} GT={GT[c]} {vec}")
