"""Ledger ground truth + arm verdicts for the six 'probe may not have bound'
cases, to cross-reference against the source issues."""
import glob
import json
import sys

import openpyxl

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
CASES = {"milvus_010": 49843, "milvus_027": 50351, "milvus_033": 51085,
         "milvus_036": 52309, "milvus_038": 52311, "milvus_043": 52325}
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))

wb = openpyxl.load_workbook("data/phase1_issue_classification.xlsx",
                            data_only=True)
rows = list(wb["issues"].iter_rows(values_only=True))
hdr = [str(h) for h in rows[0]]
idx = {h: k for k, h in enumerate(hdr)}
by_num = {r[idx["number"]]: r for r in rows[1:] if r and r[idx["number"]]}

print(f"{'case':12s} {'issue':7s} {'GT':4s} {'gt_label':16s} "
      f"{'gt_category':22s} title")
for c, n in CASES.items():
    r = by_num.get(n)
    lab = r[idx["gt_label"]] if r else "?"
    cat = r[idx["gt_category"]] if r else "?"
    ttl = str(r[idx["title"]])[:52] if r else "(not in ledger)"
    print(f"{c:12s} #{n:<6d} {GT[c]:4s} {str(lab):16s} {str(cat):22s} {ttl}")

# per-arm majority verdicts for context
CASES_FULL = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
              "milvus_021", "milvus_027", "qdrant_017"}


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

print(f"\n{'case':12s} {'full (3 runs)':34s} {'flat (3 runs)':34s}")
for c in CASES:
    fv = [full[r][c] for r in range(3)]
    av = [flat[r][c] for r in range(3)]
    print(f"{c:12s} {str(fv):34s} {str(av):34s}")
