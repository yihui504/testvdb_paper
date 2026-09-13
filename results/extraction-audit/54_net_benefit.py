"""Net-benefit statistics for full vs flat (cycle-2 R1 3.2 / R2 3.4 / R2 Q2):
report TP-FP, F1 over the 81-candidate pool, and Youden's J on both backbones,
so the reader can see whether the structure still pays once leakage is priced."""
import glob
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
CASES_FULL = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
              "milvus_021", "milvus_027", "qdrant_017"}
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))
N_T = sum(1 for v in GT.values() if v == "T")
N_F = sum(1 for v in GT.values() if v == "F")


def load(base, run):
    d = {}
    for f in sorted(glob.glob(f"{ROOT}/{base}/{run}/verdicts_batch*.jsonl")):
        for l in open(f, encoding="utf-8"):
            l = l.strip()
            if not l:
                continue
            o = json.loads(l)
            if o.get("defect_id"):
                d[o["defect_id"]] = o["verdict"]
    return d


def is_c(v):
    return v in ("CONFIRMED", "HUMAN_REVIEW")


def arm(name, runs):
    maj = {i: sum(is_c(runs[k][i]) for k in range(3)) >= 2 for i in GT}
    tp = sum(1 for i in GT if maj[i] and GT[i] == "T")
    fp = sum(1 for i in GT if maj[i] and GT[i] == "F")
    fn = N_T - tp
    tn = N_F - fp
    rec = tp / N_T
    supp = tn / N_F
    prec = tp / (tp + fp)
    f1 = 2 * tp / (2 * tp + fp + fn)
    youden = rec + supp - 1
    print(f"{name:26s} TP {tp:2d} FP {fp:2d} FN {fn:2d} TN {tn:2d}")
    print(f"{'':26s} recall {rec:.3f}  supp {supp:.3f}  prec {prec:.3f}")
    print(f"{'':26s} TP-FP {tp - fp:2d}   F1 {f1:.3f}   "
          f"Youden J {youden:.3f}")
    return tp, fp, f1, youden


full = [load("rerun_v3", f"run_full{k}") for k in (1, 2, 3)]
flat = [load("rerun_v3", f"run_flat{k}") for k in (1, 2, 3)]
for r in range(3):
    p = f"{ROOT}/rerun_v3/run_full{r + 1}/verdicts_coganchor_rejudge.jsonl"
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        o = json.loads(l)
        if o.get("defect_id") in CASES_FULL:
            full[r][o["defect_id"]] = o["verdict"]

print(f"pool: {N_T} true / {N_F} false\n")
print("== primary backbone ==")
a = arm("full (convention)", full)
b = arm("flat (convention)", flat)
print(f"\n  delta TP-FP  {a[0] - a[1] - (b[0] - b[1]):+d}"
      f"   delta F1 {a[2] - b[2]:+.3f}   delta J {a[3] - b[3]:+.3f}")

print("\n== second backbone ==")
fq = [load("rerun_v3", f"run_fullq{k}") for k in (1, 2, 3)]
aq = [load("rerun_v3", f"run_flatq{k}") for k in (1, 2, 3)]
for r in range(3):
    p = f"{ROOT}/rerun_v3/run_fullq{r + 1}/verdicts_coganchor_rejudge.jsonl"
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        o = json.loads(l)
        if o.get("defect_id") in CASES_FULL:
            fq[r][o["defect_id"]] = o["verdict"]
c = arm("full-Qwen (convention)", fq)
d = arm("flat-Qwen (convention)", aq)
print(f"\n  delta TP-FP  {c[0] - c[1] - (d[0] - d[1]):+d}"
      f"   delta F1 {c[2] - d[2]:+.3f}   delta J {c[3] - d[3]:+.3f}")
