"""Reconcile the routing sentence with Table 6's caption: for the full arm's
15 routed true-positive confirmations, what does the flat judge return?"""
import glob
import json
import sys

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

full_m = {i: sum(is_c(full[r][i]) for r in range(3)) >= 2 for i in GT}
flat_m = {i: sum(is_c(flat[r][i]) for r in range(3)) >= 2 for i in GT}

routed_tp = [i for i in GT if GT[i] == "T" and full_m[i]
             and any(full[r][i] == "HUMAN_REVIEW" for r in range(3))]
print(f"full routed TP confirmations: {len(routed_tp)}")
n_fp = n_hr = 0
for i in sorted(routed_tp):
    fv = [flat[r][i] for r in range(3)]
    if not flat_m[i]:
        if all(v == "FALSE_POSITIVE" for v in fv):
            n_fp += 1
            kind = "FP (forced closure)"
        else:
            n_hr += 1
            kind = "not confirmed (flat routed/HR-mixed)"
        print(f"  {i:14s} flat={fv}  -> {kind}")
print(f"\nflat forced-closes as FALSE-POSITIVE: {n_fp}")
print(f"flat leaves unconfirmed by other means : {n_hr}")
