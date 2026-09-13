"""Per-case pre/post verdicts for the cognition-anchor rejudge, so the miss
decomposition can name the two new false negatives (milvus_004, milvus_006)."""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))
CASES = ["milvus_004", "milvus_006", "milvus_018", "milvus_019",
         "milvus_021", "milvus_027", "qdrant_017"]

for c in CASES:
    print(f"== {c}  (GT={GT[c]}) ==")
    for r in (1, 2, 3):
        p = f"{ROOT}/rerun_v3/run_full{r}/_pre_coganchor.jsonl"
        q = f"{ROOT}/rerun_v3/run_full{r}/verdicts_coganchor_rejudge.jsonl"
        def get(path):
            try:
                for l in open(path, encoding="utf-8"):
                    l = l.strip()
                    if not l:
                        continue
                    o = json.loads(l)
                    if o.get("defect_id") == c:
                        return o
            except FileNotFoundError:
                return None
            return None
        pre, post = get(p), get(q)
        pv = pre.get("verdict") if pre else "-"
        qv = post.get("verdict") if post else "-"
        flag = "  <-- FLIP" if pv != qv else ""
        print(f"   run{r}: {pv:16s} -> {qv:16s}{flag}")
