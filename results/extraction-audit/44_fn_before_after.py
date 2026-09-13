"""Was the 'ten misses' decomposition accurate before the cognition-anchor
rejudge? Compare full-stage majority FN counts pre- and post-rejudge."""
import glob
import json
import sys

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
            if not l or l.startswith("{" ) is False:
                continue
            o = json.loads(l)
            if o.get("defect_id"):
                d[o["defect_id"]] = o["verdict"]
    return d


def is_c(v):
    return v in ("CONFIRMED", "HUMAN_REVIEW")


def fnset(runs):
    maj = {i: sum(is_c(runs[k][i]) for k in range(3)) >= 2 for i in GT}
    return {i for i in GT if GT[i] == "T" and not maj[i]}


pre = [load(f"run_full{k}") for k in (1, 2, 3)]
post = [dict(r) for r in pre]
for r in range(3):
    p = f"{ROOT}/rerun_v3/run_full{r + 1}/verdicts_coganchor_rejudge.jsonl"
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        o = json.loads(l)
        if o.get("defect_id") in CASES_FULL:
            post[r][o["defect_id"]] = o["verdict"]

a, b = fnset(pre), fnset(post)
print(f"pre-rejudge  FN: {len(a)}")
print(f"post-rejudge FN: {len(b)}")
print(f"gained (FN only after rejudge): {sorted(b - a)}")
print(f"lost   (FN only before)       : {sorted(a - b)}")
