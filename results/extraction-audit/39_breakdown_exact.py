"""Exact component breakdown of each arm's convention confirmations, for the
round-15 accounting rewrite."""
import glob
import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
CASES_FULL = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
              "milvus_021", "milvus_027", "qdrant_017"}
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))


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


def breakdown(name, runs):
    conv = [i for i in GT if sum(is_c(runs[k][i]) for k in range(3)) >= 2]
    allc, hr_maj, hr_min = [], [], []
    for i in conv:
        vs = [runs[k][i] for k in range(3)]
        n_hr = sum(1 for v in vs if v == "HUMAN_REVIEW")
        n_c = sum(1 for v in vs if v == "CONFIRMED")
        if n_hr == 0:
            allc.append(i)
        elif n_c < 2:
            hr_maj.append(i)          # majority is HUMAN_REVIEW
        else:
            hr_min.append(i)          # majority CONFIRMED, minority HR
    def tpf(s):
        return (sum(1 for i in s if GT[i] == "T"),
                sum(1 for i in s if GT[i] == "F"))
    print(f"== {name} ==")
    print(f"  convention confirmations: {len(conv)}  (TP/FP {tpf(conv)})")
    print(f"    all-Confirmed (no HR vote): {len(allc)}  (TP/FP {tpf(allc)})")
    print(f"    majority-Human-Review:      {len(hr_maj)}  (TP/FP "
          f"{tpf(hr_maj)})")
    print(f"    Confirmed+minority-HR:      {len(hr_min)}  (TP/FP "
          f"{tpf(hr_min)})")
    print(f"    HR-carrying total:          {len(hr_maj) + len(hr_min)}")
    print(f"    pooled HR verdicts: "
          f"{sum(1 for k in range(3) for i in GT if runs[k][i] == 'HUMAN_REVIEW')}/243")
    print(f"    HR-majority FPs: {sorted(i for i in hr_maj if GT[i] == 'F')}")
    print(f"    HR-majority TPs: {sorted(i for i in hr_maj if GT[i] == 'T')}")
    print(f"    minority-HR TPs: {sorted(i for i in hr_min if GT[i] == 'T')}")
    return conv, allc, hr_maj, hr_min


breakdown("full (cleaned)", full)
breakdown("flat", flat)
