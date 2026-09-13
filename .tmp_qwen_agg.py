"""③ cross-family aggregation: qwen source-only arm (run_donlyq1..3) vs GLM d-only arm.

Reads 81/81 per run; computes per-run confusion vs gt_81, majority, unanimity,
and case-level agreement with the GLM d-only arm (majority and per-run).
"""
import json
import glob
import os
import math

BASE = ".paperpilot/phase2-rerun/arms/rq2_3run"
gt = json.load(open(os.path.join(BASE, "gt_81.json"), encoding="utf-8"))
ids = sorted(gt)


def load(pattern):
    out = {}
    for f in sorted(glob.glob(os.path.join(BASE, pattern))):
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if line:
                r = json.loads(line)
                out[r["defect_id"]] = r["verdict"]
    return out


def maj(per):
    return {i: ("CONFIRMED" if sum(1 for r in per if per[r].get(i) == "CONFIRMED") * 2 >= 3
                else "FALSE_POSITIVE") for i in ids}


def conf(v, label):
    have = [i for i in ids if i in v]
    tp = sum(1 for i in have if v[i] == "CONFIRMED" and gt[i] == "T")
    fp = sum(1 for i in have if v[i] == "CONFIRMED" and gt[i] == "F")
    tn = sum(1 for i in have if v[i] == "FALSE_POSITIVE" and gt[i] == "F")
    fn = sum(1 for i in have if v[i] == "FALSE_POSITIVE" and gt[i] == "T")
    print(f"  {label:<24} TP={tp:2d} FP={fp} FN={fn:2d} TN={tn:2d} | recall={tp/max(1,tp+fn):.3f} supp={tn/max(1,tn+fp):.3f} prec={tp/max(1,tp+fp):.3f}")


qruns = {r: load(f"run_donlyq{r}/verdicts_batch*.jsonl") for r in (1, 2, 3)}
gruns = {r: load(f"run_donly{r}/verdicts_batch*.jsonl") for r in (1, 2, 3)}
for r in (1, 2, 3):
    if len(qruns[r]) != 81:
        print(f"  WARNING run{r}: {len(qruns[r])}/81 (missing batches; per-run stats use available cases)")

print("== qwen d-only arm ==")
for r in (1, 2, 3):
    conf(qruns[r], f"qwen run{r}")
qm = maj(qruns)
conf(qm, "qwen majority")
full = [i for i in ids if all(i in qruns[r] for r in (1, 2, 3))]
unan = sum(1 for i in full if len({qruns[r][i] for r in (1, 2, 3)}) == 1)
print(f"  qwen unanimity: {unan}/{len(full)} (cases with all 3 runs)")

print("\n== GLM d-only arm (reference) ==")
gm = maj(gruns)
conf(gm, "GLM majority")

print("\n== cross-family agreement ==")
for r in (1, 2, 3):
    both = [i for i in ids if i in qruns[r] and i in gruns[r]]
    ag = sum(1 for i in both if qruns[r][i] == gruns[r][i])
    print(f"  qwen run{r} vs GLM run{r}: {ag}/{len(both)} ({ag/max(1,len(both)):.1%})")
ag_m = sum(1 for i in ids if qm[i] == gm[i])
print(f"  qwen-majority vs GLM-majority: {ag_m}/81 ({ag_m/81:.1%})")
gt_ag = sum(1 for i in ids if (qm[i] == "CONFIRMED") == (gt[i] == "T"))
glm_gt_ag = sum(1 for i in ids if (gm[i] == "CONFIRMED") == (gt[i] == "T"))
print(f"  correctness vs gt: qwen {gt_ag}/81, GLM {glm_gt_ag}/81")

# case-level flips majority vs majority
flips = [(i, gt[i], gm[i], qm[i]) for i in ids if qm[i] != gm[i]]
print(f"  majority flips ({len(flips)}):")
for i, g, gv, qv in flips:
    print(f"    {i}: gt={g} GLM={gv[:4]} qwen={qv[:4]}")

# ② task2: confirmation rate over the 32 unsubmitted registry-defect packs
t2 = {r: load(f"run_task2/verdicts_run{r}_batch*.jsonl") for r in (1, 2, 3)}
allids = sorted(set().union(*[set(v) for v in t2.values()]))
print(f"\n== ② task2 unsubmitted-stream arm: {len(allids)} cases ==")
for r in (1, 2, 3):
    n = len(t2[r]); c = sum(1 for v in t2[r].values() if v == "CONFIRMED")
    print(f"  run{r}: {c}/{n} CONFIRMED ({c/n:.3f})")
def maj2(per):
    return {i: ("CONFIRMED" if sum(1 for r in per if per[r].get(i) == "CONFIRMED") * 2 >= 3
                else "FALSE_POSITIVE") for i in allids}
m2 = maj2(t2)
c = sum(1 for v in m2.values() if v == "CONFIRMED")
p = c / len(m2)
z = 1.959964; n = len(m2)
d = 1 + z*z/n; ctr = (p + z*z/(2*n))/d
h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
print(f"  majority: {c}/{n} = {p:.3f} Wilson [{max(0,ctr-h):.3f},{min(1,ctr+h):.3f}]")
unan2 = sum(1 for i in allids if len({t2[r].get(i) for r in (1, 2, 3)}) == 1)
print(f"  unanimity: {unan2}/{n}")
