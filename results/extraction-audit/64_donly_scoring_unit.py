"""Which scoring unit produces the paper's source-only row (36 TP / 8 leak =
44 confirmations, recall 0.706, suppression 0.733)? Binary CONFIRMED>=2/3
(as donly_arm_analysis.py maps) or is-C >=2/3 (HR counts)?"""
import glob
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))


def load(run):
    d = {}
    for f in sorted(glob.glob(f"{ROOT}/rerun_v3/{run}/verdicts_batch*.jsonl")):
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


runs = [load(f"run_donly{k}") for k in (1, 2, 3)]

for name, pred in (
        ("binary: CONFIRMED >= 2/3", lambda vs: sum(v == "CONFIRMED"
                                                    for v in vs) >= 2),
        ("is-C   : (C or HR) >= 2/3", lambda vs: sum(is_c(v)
                                                     for v in vs) >= 2),
        ("unanimous is-C", lambda vs: all(is_c(v) for v in vs))):
    maj = {i: pred([runs[r][i] for r in range(3)]) for i in GT}
    tp = sum(1 for i in GT if maj[i] and GT[i] == "T")
    fp = sum(1 for i in GT if maj[i] and GT[i] == "F")
    print(f"{name:28s} TP {tp:2d}  FP {fp:2d}  recall {tp / 51:.3f}  "
          f"supp {(30 - fp) / 30:.3f}  prec {tp / (tp + fp) if tp + fp else 0:.3f}")

print("\npaper's row: TP 36, leak 8, recall 0.706, suppression 0.733, "
      "precision 0.818 (36/44)")
