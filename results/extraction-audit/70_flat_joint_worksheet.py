"""Verify the flat joint reading under the worksheet's authoritative rulings
(upheld 6, milvus_010 REJECT) vs script 37's set (upheld 7). Both should give
29/51 because milvus_010 already holds a forced majority."""
import glob
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
CASES_FULL = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
              "milvus_021", "milvus_027", "qdrant_017"}
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))
UPHELD_WORKSHEET = {"milvus_033", "milvus_036", "milvus_038", "milvus_043",
                    "qdrant_014", "weaviate_003"}
UPHELD_SCRIPT37 = UPHELD_WORKSHEET | {"milvus_010"}


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


flat = [load(f"run_flat{k}") for k in (1, 2, 3)]
flat_m = {i: sum(is_c(flat[r][i]) for r in range(3)) >= 2 for i in GT}
flat_forced = {i: sum(flat[r][i] == "CONFIRMED" for r in range(3)) >= 2
               for i in GT}
flat_routed = {i for i in GT if flat_m[i]
               and any(flat[r][i] == "HUMAN_REVIEW" for r in range(3))}

for name, upheld in (("worksheet (upheld 6)", UPHELD_WORKSHEET),
                     ("script37  (upheld 7)", UPHELD_SCRIPT37)):
    joint = {}
    for i in GT:
        if not flat_m[i]:
            joint[i] = False
        elif i in flat_routed and not flat_forced[i]:
            joint[i] = i in upheld
        else:
            joint[i] = True
    tp = sum(1 for i in GT if joint[i] and GT[i] == "T")
    fp = sum(1 for i in GT if joint[i] and GT[i] == "F")
    overlap = sorted(i for i in upheld if flat_forced[i])
    print(f"{name}: joint TP {tp}/51 ({tp / 51:.3f})  FP {fp}  "
          f"supp {(30 - fp) / 30:.3f}  overlap-with-forced {overlap}")
