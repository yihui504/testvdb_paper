"""Enumerate the full-stage majority false negatives under the cleaned packs,
with strata and candidate-family labels, so the miss decomposition can be
made exact (round-16 fix; R2 3.6 / R3 3.7)."""
import glob
import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
CASES_FULL = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
              "milvus_021", "milvus_027", "qdrant_017"}
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


runs = [load(f"run_full{k}") for k in (1, 2, 3)]
for r in range(3):
    p = f"{ROOT}/rerun_v3/run_full{r + 1}/verdicts_coganchor_rejudge.jsonl"
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        o = json.loads(l)
        if o.get("defect_id") in CASES_FULL:
            runs[r][o["defect_id"]] = o["verdict"]

maj = {i: sum(is_c(runs[k][i]) for k in range(3)) >= 2 for i in GT}
tp = [i for i in GT if GT[i] == "T"]
fn = [i for i in tp if not maj[i]]
print(f"GT true: {len(tp)};  majority confirmations: "
      f"{sum(1 for i in tp if maj[i])};  FN: {len(fn)}")
print("\nFN cases with per-run verdicts:")
for i in sorted(fn):
    vs = [runs[k][i] for k in range(3)]
    hr = sum(1 for v in vs if v == "HUMAN_REVIEW")
    print(f"  {i:14s} HR votes {hr}/3   {vs}")
print("\nHR-vote histogram over the FN set:", dict(Counter(
    sum(1 for v in [runs[k][i] for k in range(3)] if v == "HUMAN_REVIEW")
    for i in fn)))
